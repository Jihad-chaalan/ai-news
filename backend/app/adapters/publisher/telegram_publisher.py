import httpx
import asyncio
import logging
from app.ports.ipublisher import IPublisher
from app.config import settings

logger = logging.getLogger(__name__)

class TelegramPublisher(IPublisher):
    async def publish(self, briefing_data: dict) -> bool:
        """Send each story as a separate Telegram message."""
        bot_token = settings.TELEGRAM_BOT_TOKEN
        chat_id = settings.TELEGRAM_CHAT_ID
        if not bot_token or not chat_id:
            logger.warning("Telegram credentials missing – skipping.")
            return False

        api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        date_str = briefing_data["date"].strftime("%B %d, %Y")

        success = True
        for idx, story in enumerate(briefing_data["stories"], 1):
            # Build the message for this story
            title = story.get("title", "No title")
            summary = story.get("summary", "No summary")
            why = story.get("why_it_matters", "")
            key_points = story.get("key_points", [])
            image_url = story.get("image_url")
            sources = story.get("sources", [])

            # Format key points as bullet list
            points_text = "\n".join([f"• {pt}" for pt in key_points]) if key_points else ""

            # Format sources as clickable links (publisher name → URL)
            sources_text = ""
            if sources:
                src_links = []
                for src in sources[:3]:  # limit to 3 sources per story
                    pub = src.get("publisher", "Source")
                    url = src.get("url")
                    if url:
                        src_links.append(f"[{pub}]({url})")
                if src_links:
                    sources_text = f"📎 Sources: {', '.join(src_links)}"

            message = f"📰 *AI Daily News – {date_str}*\n\n"
            message += f"*{idx}. {title}*\n"
            message += f"{summary}\n"
            if why:
                message += f"\n*Why it matters:* {why}\n"
            if points_text:
                message += f"\n*Key points:*\n{points_text}\n"
            if image_url:
                message += f"\n🖼️ [View Image]({image_url})\n"
            if sources_text:
                message += f"\n{sources_text}\n"

            # Add a separator between stories (optional)
            if idx < len(briefing_data["stories"]):
                message += "\n---\n"

            payload = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "Markdown",
                "disable_web_page_preview": False,
            }

            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(api_url, json=payload)
                    response.raise_for_status()
                    logger.info(f"Sent story {idx}/{len(briefing_data['stories'])} to Telegram.")
            except Exception as e:
                logger.error(f"Failed to send story {idx}: {e}")
                success = False

            # Delay between messages (avoid rate limits)
            if idx < len(briefing_data["stories"]):
                await asyncio.sleep(2.0)  # 2 seconds between messages

        return success