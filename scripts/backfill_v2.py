#!/usr/bin/env python3
"""回填脚本 — 用 akshare 拉历史资金流写入 187 PostgreSQL"""
import time, sys
from datetime import date
import psycopg2
import akshare as ak

# ── Config ──
PG_HOST = "192.168.31.187"
PG_PORT = 5432
PG_USER = "capflow"
PG_PASS = "CapFlow2026!"
PG_DB   = "capflow"

# Well-known industry names that work with fund_flow_hist
# These are申万 industry names
INDUSTRY_NAMES = [
    "半导体", "银行", "证券", "白酒", "软件开发", "汽车整车", "光伏设备",
    "电力", "房地产开发", "化学制药", "通信设备", "IT服务", "医疗器械",
    "食品饮料", "计算机设备", "有色金属", "钢铁", "煤炭开采", "物流",
    "生物制品", "通用设备", "专用设备", "汽车零部件", "消费电子",
    "小金属", "化学制品", "建筑材料", "环保", "服装家纺", "中药",
    "电网设备", "电池", "军工电子", "农化制品", "包装印刷", "塑料制品",
    "养殖业", "农产品加工", "零售", "旅游及景区", "酒店餐饮", "航空机场",
    "航运港口", "铁路公路", "高速公路", "多元金融", "保险", "互联网电商",
    "广告营销", "影视院线", "游戏", "教育", "其他"
]

def connect_pg():
    return psycopg2.connect(
        host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASS, dbname=PG_DB,
        connect_timeout=10
    )

def upsert_sector(conn, name):
    """Insert sector metadata"""
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO sectors (sector_code, sector_name, sector_type) VALUES (%s,%s,'industry') ON CONFLICT (sector_code) DO NOTHING",
            (name, name)
        )
        conn.commit()

def backfill_sector(conn, name):
    """Fetch and insert historical fund flow for one sector"""
    try:
        df = ak.stock_sector_fund_flow_hist(symbol=name)
    except Exception as e:
        print(f"  {name}: API ERROR - {type(e).__name__}")
        return 0

    if df is None or df.empty:
        print(f"  {name}: empty response")
        return 0

    count = 0
    with conn.cursor() as cur:
        for _, row in df.iterrows():
            td = row.get("日期", None)
            if td is None:
                continue
            if hasattr(td, "date"):
                td = td.date()
            if not isinstance(td, date) or td < date(2025, 1, 1):
                continue

            cur.execute("""
                INSERT INTO sector_fund_flow_daily
                    (trade_date, sector_code, data_source,
                     main_net_inflow, main_net_ratio,
                     super_large_net, large_net,
                     medium_net, small_net,
                     close_pct, turnover)
                VALUES (%s,%s,'akshare',%s,%s,%s,%s,%s,%s,0,0)
                ON CONFLICT (trade_date, sector_code) DO NOTHING
            """, (
                td, name,
                float(row.get("主力净流入-净额", 0) or 0),
                float(row.get("主力净流入-净占比", 0) or 0),
                float(row.get("超大单净流入-净额", 0) or 0),
                float(row.get("大单净流入-净额", 0) or 0),
                float(row.get("中单净流入-净额", 0) or 0),
                float(row.get("小单净流入-净额", 0) or 0),
            ))
            count += 1
        conn.commit()

    return count


def main():
    conn = connect_pg()
    print(f"Connected to PG @ {PG_HOST}:{PG_PORT}")

    total = 0
    ok = 0
    fail = 0

    for i, name in enumerate(INDUSTRY_NAMES):
        try:
            upsert_sector(conn, name)
            n = backfill_sector(conn, name)
            if n > 0:
                ok += 1
                total += n
                print(f"[{i+1}/{len(INDUSTRY_NAMES)}] {name}: {n} rows ✓")
            else:
                fail += 1
                print(f"[{i+1}/{len(INDUSTRY_NAMES)}] {name}: 0 rows ✗")
        except Exception as e:
            fail += 1
            print(f"[{i+1}/{len(INDUSTRY_NAMES)}] {name}: ERROR - {type(e).__name__}")
            conn.rollback()
            try:
                conn = connect_pg()  # reconnect
            except:
                pass

        # LONG delay to avoid rate limiting
        time.sleep(10)

    conn.close()
    print(f"\nDone! {ok} sectors OK, {fail} failed, {total} total rows inserted")


if __name__ == "__main__":
    main()
