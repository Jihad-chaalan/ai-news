import logging
from datetime import date
from app.adapters.repository.supabase_repository import SupabaseRepository
from app.adapters.publisher.telegram_publisher import TelegramPublisher

logger = logging.getLogger(__name__)

def ensure_str(value):
    return str(value) if value else None

async def publish_node(state: dict) -> dict:
    validated = state.get("validated_stories", [])
    if not validated:
        logger.warning("No stories to publish.")
        state["final_briefing"] = None
        state["publish_status"] = {"db": False, "telegram": False}
        return state

    briefing_data = {
        "date": date.today(),
        "stories": []
    }

    for story in validated:
        ai_summary = story.get("summary", {})
        image_url = ensure_str(story.get("image_url"))

        sources = []
        for src in story.get("sources", []):
            url = ensure_str(src.get("url"))
            sources.append({
                "url": url,
                "publisher": url,   # <-- store the full URL directly
                "published_at": src.get("published_at"),
            })

        briefing_data["stories"].append({
            "title": ai_summary.get("title", story.get("title", "No title")),
            "summary": ai_summary.get("summary", "No summary available"),
            "why_it_matters": ai_summary.get("why_it_matters", ""),
            "key_points": ai_summary.get("key_points", []) or [],
            "image_url": image_url,
            "importance_score": story.get("score", {}).overall_importance if story.get("score") else 0,
            "sources": sources
        })

    repo = SupabaseRepository()
    db_success = await repo.save_briefing(briefing_data)

    publisher = TelegramPublisher()
    tg_success = await publisher.publish(briefing_data)

    state["final_briefing"] = briefing_data
    state["publish_status"] = {"db": db_success, "telegram": tg_success}

    return state