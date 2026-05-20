#!/usr/bin/env python3
"""历史数据回填"""
import time, requests, json
from datetime import date, datetime
from sqlalchemy import create_engine, text

engine = create_engine("postgresql://capflow:CapFlow2026!@localhost:5432/capflow")
H = {"User-Agent": "Mozilla/5.0", "Referer": "https://data.eastmoney.com/"}

# Get sector codes
r = requests.get(
    "https://push2.eastmoney.com/api/qt/clisting/get",
    params={"pn": "1", "pz": "500", "po": "1", "np": "1", "fltt": "2",
            "fid": "f3", "fs": "m:90+t2", "fields": "f12,f14"},
    headers=H, timeout=15)

data = json.loads(r.text)
sectors = data.get("data", {}).get("diff", [])
print(f"Got {len(sectors)} sectors")

for sec in sectors[:10]:
    code, name = sec["f12"], sec["f14"]
    # Save sector
    with engine.connect() as conn:
        conn.execute(text(
            "INSERT INTO sectors (sector_code, sector_name, sector_type) VALUES (:c,:n,:t) ON CONFLICT (sector_code) DO NOTHING"),
            {"c": code, "n": name, "t": "industry"})
        conn.commit()
    
    # Fetch history
    try:
        r = requests.get(
            "https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get",
            params={"lmt": "500", "klt": "101", "secid": f"90.{code}",
                    "fields1": "f1,f2,f3,f7",
                    "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65"},
            headers=H, timeout=15)
        resp = r.json()
        klines = resp.get("data", {}).get("klines", [])
    except Exception as e:
        print(f"  {code} {name}: API error - {e}")
        time.sleep(3)
        continue
    
    count = 0
    for line in klines:
        parts = line.split(",")
        if len(parts) < 10:
            continue
        try:
            td = datetime.strptime(parts[0], "%Y-%m-%d").date()
        except:
            continue
        if td < date(2025, 1, 1):
            continue
        
        vals = {
            "trade_date": td, "sector_code": code, "data_source": "akshare",
            "close_pct": float(parts[9] or 0),
            "main_net_inflow": float(parts[4] or 0),
            "main_net_ratio": float(parts[8] or 0),
            "super_large_net": float(parts[2] or 0),
            "large_net": float(parts[3] or 0),
            "medium_net": float(parts[5] or 0),
            "small_net": float(parts[6] or 0),
            "turnover": float(parts[7] or 0),
        }
        cols = ", ".join(vals.keys())
        ph = ", ".join(f":{k}" for k in vals)
        with engine.connect() as conn:
            conn.execute(text(f"INSERT INTO sector_fund_flow_daily ({cols}) VALUES ({ph}) ON CONFLICT DO NOTHING"), vals)
            conn.commit()
        count += 1
    
    print(f"  {code} {name}: {count} rows")
    time.sleep(2)

print("Done!")
