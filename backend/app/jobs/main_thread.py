import logging
from app.services.main_thread import get_top_sectors

logger = logging.getLogger(__name__)

async def compute_main_thread_job():
    try:
        result = await get_top_sectors(top_n=3)
        logger.info(f"Main thread computed: {len(result.get('top_sectors', []))} sectors")
    except Exception as e:
        logger.error(f"compute_main_thread: {e}")
