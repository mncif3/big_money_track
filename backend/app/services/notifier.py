import httpx
import logging
from app.config import settings

logger = logging.getLogger(__name__)

async def send_feishu(title: str, content: str):
    if not settings.feishu_webhook:
        logger.warning("FEISHU_WEBHOOK not configured")
        return False
    try:
        async with httpx.AsyncClient(timeout=10) as cli:
            r = await cli.post(settings.feishu_webhook, json={
                "msg_type": "interactive",
                "card": {
                    "header": {"title": {"tag": "plain_text", "content": title}},
                    "elements": [{"tag": "markdown", "content": content}]
                }
            })
            return r.status_code == 200
    except Exception as e:
        logger.error(f"Feishu send failed: {e}")
        return False
