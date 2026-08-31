import logging
from app.services.cleanup_service import CleanupService

logger = logging.getLogger(__name__)

async def cleanup_node(state: dict) -> dict:
    """Delete old briefings (older than 7 days) and their images."""
    service = CleanupService()
    deleted = await service.delete_old_briefings(retention_days=7)
    state["cleanup_deleted"] = deleted
    logger.info(f"Cleanup complete: {deleted} old briefings deleted.")
    return state