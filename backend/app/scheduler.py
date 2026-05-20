from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

def setup_scheduler() -> AsyncIOScheduler:
    sched = AsyncIOScheduler(timezone="Asia/Shanghai")
    # P0: Jobs registered here as they are implemented
    # P0: daily_sector_flow at 15:35
    # P0: daily_stock_flow at 15:40
    # P3: south/margin at 15:50/16:30
    return sched
