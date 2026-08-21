import logging
from app.models.story_summary import StorySummary  
from app.adapters.llm.groq_provider import GroqProvider

logger = logging.getLogger(__name__)


def build_summary_prompt(story: dict) -> str:
    title = story.get("title", "Unknown title")
    description = story.get("description", "No description available")
    source_count = story.get("source_count", 1)
    return f"""
You are an expert AI news editor. Write a compelling summary for this AI news story.

Title: {title}
Description: {description}
Sources covering this story: {source_count}

Generate a structured summary with:
- A concise, catchy title (may be slightly different from original)
- A 2-3 sentence summary
- Why this matters for the AI industry (1-2 sentences)
- 3 key points

Return JSON with fields: title, summary, why_it_matters, key_points (array of strings).
"""


async def summary_node(state: dict) -> dict:
    """
    Generate summaries for all pending stories.
    """
    # Initialise pending_stories from selected_stories if empty
    if not state.get("pending_stories") and state.get("selected_stories"):
        state["pending_stories"] = state["selected_stories"].copy()
        state["validated_stories"] = []
        state["retry_counts"] = {
            story.get("id", story.get("title", str(i))): 0
            for i, story in enumerate(state["selected_stories"])
        }
        logger.info(f"Initialised pending_stories: {len(state['pending_stories'])} stories")

    pending = state.get("pending_stories", [])
    if not pending:
        return state

    llm = GroqProvider()
    for story in pending:
        try:
            prompt = build_summary_prompt(story)
            summary = await llm.generate_structured(
                prompt,
                StorySummary,           
                temperature=0.5,
                max_tokens=2048        
            )
            story["summary"] = summary.model_dump()
            story["summary_error"] = None
        except Exception as e:
            logger.error(f"Summary failed for '{story.get('title', '')[:40]}...': {e}")
            story["summary"] = None
            story["summary_error"] = str(e)

    return state