import logging
from app.models.image_prompt import ImagePrompt
from app.adapters.llm.groq_provider import GroqProvider

logger = logging.getLogger(__name__)


def build_image_prompt_prompt(story: dict) -> str:
    title = story.get("title", "Unknown title")
    summary = story.get("summary", {}).get("summary", "No summary")
    description = story.get("description", "No description")
    return f"""
You are a creative director. Generate an editorial image prompt.

Title: {title}
Summary: {summary}
Description: {description}

Generate a detailed prompt for an AI image generator.
Return JSON with a single field: "prompt".
"""


async def image_prompt_node(state: dict) -> dict:
    pending = state.get("pending_stories", [])
    if not pending:
        return state

    llm = GroqProvider()
    for story in pending:
        # Skip if no summary available
        summary = story.get("summary")
        if not summary or not summary.get("summary"):
            logger.warning(f"Skipping image prompt for '{story.get('title', '')[:40]}...' – no summary available.")
            continue

        try:
            prompt = build_image_prompt_prompt(story)
            image_prompt = await llm.generate_structured(
                prompt, ImagePrompt, temperature=0.7, max_tokens=512   # increased
            )
            story["image_prompt"] = image_prompt.prompt
            story["prompt_error"] = None
        except Exception as e:
            logger.error(f"Image prompt failed for '{story.get('title', '')[:40]}...': {e}")
            story["image_prompt"] = None
            story["prompt_error"] = str(e)

    return state