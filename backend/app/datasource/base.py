from abc import ABC, abstractmethod
import pandas as pd

class FundFlowDataSource(ABC):
    name: str

    @abstractmethod
    async def fetch_sector_flow(self, indicator: str = "今日") -> pd.DataFrame: ...

    @abstractmethod
    async def fetch_stock_flow(self, indicator: str = "今日") -> pd.DataFrame: ...

    @abstractmethod
    async def fetch_north_summary(self) -> pd.DataFrame: ...

    @abstractmethod
    async def fetch_south_summary(self) -> pd.DataFrame: ...

    @abstractmethod
    async def fetch_margin_data(self) -> pd.DataFrame: ...
