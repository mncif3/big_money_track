#!/usr/bin/env python3
"""回填脚本 — 跳过已有数据的 sector，继续填充剩余"""
import requests, re, time, psycopg2, sys
from datetime import date, datetime

PG = {"host":"192.168.31.187","port":5432,"user":"capflow","password":"CapFlow2026!","dbname":"capflow"}
H = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)","Referer":"https://data.eastmoney.com/bkzj/hy.html"}

# Get code mapping
r = requests.get("https://data.eastmoney.com/bkzj/hy.html", headers=H, timeout=15)
pairs = re.findall(r'href="[^"]*?(BK\d{4})[^"]*?"[^>]*>([^<]+)', r.text)
all_codes = [(c, n.strip()) for c, n in pairs]

# Check which already have data
conn = psycopg2.connect(**PG, connect_timeout=10)
cur = conn.cursor()
cur.execute("SELECT distinct sector_code FROM sector_fund_flow_daily")
done = set(r[0] for r in cur.fetchall())
cur.close()

pending = [(c, n) for c, n in all_codes if c not in done]
print(f"Total: {len(all_codes)}, Done: {len(done)}, Pending: {len(pending)}")

if not pending:
    print("All sectors already have data!")
    conn.close()
    sys.exit(0)

# Process in sub-batches of 20 with cooldown
BATCH_SIZE = 20
COOLDOWN = 30  # seconds between batches
DELAY = 10     # seconds between sectors

total = 0
ok = 0
fail = 0

for batch_start in range(0, len(pending), BATCH_SIZE):
    batch = pending[batch_start:batch_start + BATCH_SIZE]
    print(f"\n--- Batch {batch_start//BATCH_SIZE + 1}/{(len(pending)-1)//BATCH_SIZE + 1} "
          f"({len(batch)} sectors) ---")

    for code, name in batch:
        try:
            # Insert sector metadata
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO sectors (sector_code,sector_name,sector_type) VALUES (%s,%s,'industry') "
                "ON CONFLICT (sector_code) DO NOTHING",
                (code, name))
            conn.commit()
            cur.close()

            resp = requests.get(
                "https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get",
                params={"lmt":"500","klt":"101","secid":f"90.{code}",
                        "fields1":"f1,f2,f3,f7",
                        "fields2":"f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65"},
                headers=H, timeout=20)

            if resp.status_code != 200:
                fail += 1
                print(f"  {code} {name}: HTTP{resp.status_code} ✗")
                time.sleep(DELAY)
                continue

            data = resp.json()
            klines = data.get("data", {}).get("klines", [])
            if not klines:
                fail += 1
                print(f"  {code} {name}: empty ✗")
                time.sleep(DELAY)
                continue

            count = 0
            cur = conn.cursor()
            for line in klines:
                parts = line.split(",")
                if len(parts) < 14:
                    continue
                try:
                    td = datetime.strptime(parts[0], "%Y-%m-%d").date()
                except ValueError:
                    continue
                if td < date(2025, 1, 1):
                    continue

                cur.execute("""
                    INSERT INTO sector_fund_flow_daily
                        (trade_date,sector_code,data_source,
                         main_net_inflow,main_net_ratio,
                         super_large_net,large_net,medium_net,small_net,
                         close_pct,turnover)
                    VALUES (%s,%s,'akshare',%s,%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT DO NOTHING
                """, (
                    td, code,
                    float(parts[1] or 0), float(parts[6] or 0),
                    float(parts[2] or 0), float(parts[3] or 0),
                    float(parts[4] or 0), float(parts[5] or 0),
                    float(parts[12] or 0), float(parts[11] or 0),
                ))
                count += 1
            conn.commit()
            cur.close()

            ok += 1
            total += count
            print(f"  {code} {name}: {count} rows ✓")

        except Exception as e:
            fail += 1
            print(f"  {code} {name}: {type(e).__name__} ✗")
            try:
                conn.rollback()
            except:
                pass

        time.sleep(DELAY)

    # Cooldown between batches
    if batch_start + BATCH_SIZE < len(pending):
        print(f"  ... cooling down {COOLDOWN}s ...")
        time.sleep(COOLDOWN)

conn.close()
print(f"\n{'='*50}")
print(f"DONE: {ok} OK, {fail} failed, {total} new rows")
