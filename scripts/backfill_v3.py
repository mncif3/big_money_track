#!/usr/bin/env python3
"""历史资金流回填 — 从东方财富页面抓取代码映射，调 API 写入 187 PG"""
import requests, re, time, json
import psycopg2
from datetime import date, datetime
from collections import OrderedDict

PG = {
    "host": "192.168.31.187", "port": 5432,
    "user": "capflow", "password": "CapFlow2026!", "dbname": "capflow"
}

H = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://data.eastmoney.com/bkzj/hy.html"
}

# ── Step 1: Get code→name mapping from webpage ──
print("Fetching sector code mapping from eastmoney...")
r = requests.get("https://data.eastmoney.com/bkzj/hy.html", headers=H, timeout=15)
pairs = re.findall(r'href="[^"]*?(BK\d{4})[^"]*?"[^>]*>([^<]+)', r.text)
code_map = OrderedDict((code, name.strip()) for code, name in pairs)
print(f"Got {len(code_map)} sector mappings")

# ── Step 2: Connect to PG ──
conn = psycopg2.connect(**PG, connect_timeout=10)
print(f"Connected to PG @ {PG['host']}")

# ── Step 3: Backfill ──
total_rows = 0
ok_count = 0
fail_count = 0

for i, (code, name) in enumerate(code_map.items()):
    try:
        # Insert sector
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO sectors (sector_code, sector_name, sector_type) VALUES (%s,%s,'industry') "
                "ON CONFLICT (sector_code) DO UPDATE SET sector_name=EXCLUDED.sector_name",
                (code, name)
            )
            conn.commit()

        # Fetch history
        resp = requests.get(
            "https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get",
            params={
                "lmt": "500", "klt": "101", "secid": f"90.{code}",
                "fields1": "f1,f2,f3,f7",
                "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65"
            },
            headers=H, timeout=20
        )

        if resp.status_code != 200:
            fail_count += 1
            print(f"[{i+1}/{len(code_map)}] {code} {name}: HTTP {resp.status_code} ✗")
            time.sleep(15)
            continue

        data = resp.json()
        klines = data.get("data", {}).get("klines", [])
        if not klines:
            fail_count += 1
            print(f"[{i+1}/{len(code_map)}] {code} {name}: empty ✗")
            time.sleep(10)
            continue

        # Parse and insert
        count = 0
        with conn.cursor() as cur:
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
                        (trade_date, sector_code, data_source,
                         main_net_inflow, main_net_ratio,
                         super_large_net, large_net,
                         medium_net, small_net,
                         close_pct, turnover)
                    VALUES (%s,%s,'akshare',%s,%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (trade_date, sector_code) DO NOTHING
                """, (
                    td, code,
                    float(parts[1] or 0),   # f52 = main_net_inflow
                    float(parts[6] or 0),   # f57 = main_net_ratio
                    float(parts[2] or 0),   # f53 = super_large_net
                    float(parts[3] or 0),   # f54 = large_net
                    float(parts[4] or 0),   # f55 = medium_net
                    float(parts[5] or 0),   # f56 = small_net
                    float(parts[12] or 0),  # f63 = close_pct
                    float(parts[11] or 0),  # f62 = turnover
                ))
                count += 1
            conn.commit()

        ok_count += 1
        total_rows += count
        print(f"[{i+1}/{len(code_map)}] {code} {name}: {count} rows ✓")

    except Exception as e:
        fail_count += 1
        err_name = type(e).__name__
        print(f"[{i+1}/{len(code_map)}] {code} {name}: {err_name} ✗")
        conn.rollback()

    # Dynamic delay - longer for failures
    if fail_count > 0 and fail_count % 3 == 0:
        print(f"  ... cooling down 60s after {fail_count} failures ...")
        time.sleep(60)
    else:
        time.sleep(8)

conn.close()
print(f"\n{'='*50}")
print(f"DONE: {ok_count} OK, {fail_count} failed, {total_rows} rows inserted")
