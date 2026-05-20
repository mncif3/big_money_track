from typing import List
import logging

logger = logging.getLogger(__name__)

class DataSourceManager:
    def __init__(self):
        self.sources = []

    def register(self, source):
        self.sources.append(source)

    def init_default(self):
        from app.datasource.akshare_source import AkshareSource
        self.sources = [AkshareSource()]

    async def call(self, method_name: str, *args, **kwargs):
        last_err = None
        for src in self.sources:
            try:
                method = getattr(src, method_name)
                df = await method(*args, **kwargs)
                if df is not None and not df.empty:
                    return df, src.name
            except Exception as e:
                logger.warning(f"[{src.name}.{method_name}] failed: {e}")
                last_err = e
        raise RuntimeError(f"All sources failed for {method_name}: {last_err}")
