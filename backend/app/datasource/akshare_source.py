import asyncio
import akshare as ak
import pandas as pd
from .base import FundFlowDataSource

class AkshareSource(FundFlowDataSource):
    name = "akshare"

    async def fetch_sector_flow(self, indicator="今日") -> pd.DataFrame:
        return await asyncio.to_thread(ak.stock_sector_fund_flow_rank, indicator=indicator)

    async def fetch_stock_flow(self, indicator="今日") -> pd.DataFrame:
        return await asyncio.to_thread(ak.stock_individual_fund_flow_rank, indicator=indicator)

    async def fetch_north_summary(self) -> pd.DataFrame:
        return await asyncio.to_thread(ak.stock_hsgt_fund_flow_summary_em)

    async def fetch_south_summary(self) -> pd.DataFrame:
        return await asyncio.to_thread(ak.stock_hsgt_fund_flow_summary_em, market="港股通")

    async def fetch_margin_data(self) -> pd.DataFrame:
        sz = await asyncio.to_thread(ak.stock_margin_sz_detail_em)
        sh = await asyncio.to_thread(ak.stock_margin_sh_detail_em)
        return pd.concat([sz, sh], ignore_index=True)
