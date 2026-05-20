from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

def setup_scheduler() -> AsyncIOScheduler:
    sched = AsyncIOScheduler(timezone="Asia/Shanghai")

    # P0: daily jobs
    from app.jobs.sector_flow import daily_sector_flow_job
    from app.jobs.stock_flow import daily_stock_flow_job
    sched.add_job(daily_sector_flow_job, CronTrigger(hour=15, minute=35, day_of_week="mon-fri"), id="daily_sector")
    sched.add_job(daily_stock_flow_job, CronTrigger(hour=15, minute=40, day_of_week="mon-fri"), id="daily_stock")

    # P3: north/south/margin
    from app.jobs.north import daily_north_summary_job
    from app.jobs.south import daily_south_summary_job
    from app.jobs.margin import daily_margin_job
    sched.add_job(daily_north_summary_job, CronTrigger(hour=15, minute=50, day_of_week="mon-fri"), id="daily_north")
    sched.add_job(daily_south_summary_job, CronTrigger(hour=15, minute=50, day_of_week="mon-fri"), id="daily_south")
    sched.add_job(daily_margin_job, CronTrigger(hour=16, minute=30, day_of_week="mon-fri"), id="daily_margin")

    # P2: main thread
    from app.jobs.main_thread import compute_main_thread_job
    sched.add_job(compute_main_thread_job, CronTrigger(hour=16, minute=5, day_of_week="mon-fri"), id="main_thread")

    return sched
