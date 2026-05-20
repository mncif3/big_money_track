"""应用配置"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://capflow:capflow@localhost:5432/capflow"
    redis_url: str = "redis://localhost:6379/0"
    proxy_pool_url: str = "http://localhost:5010"
    feishu_webhook: str = ""
    tz: str = "Asia/Shanghai"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
