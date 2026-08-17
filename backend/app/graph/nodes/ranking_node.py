import asyncio
import logging
import random
from typing import List, Dict, Any

from app.graph.state import NewsState
from app.models.story_score import StoryScore
from app.ports.illm_provider import ILLMProvider
from app.adapters.llm.groq_provider import GroqProvider

logger = logging.getLogger(__name__)

SELECT_COUNT = 5
MAX_CONCURRENT = 1
REQUEST_DELAY = 8.0          # 8 seconds per request => 7.5 requests/min, safe below 8k TPM
MAX_RETRIES = 3
BASE_BACKOFF = 5


def build_prompt(story: Dict[str, Any]) -> str:
    title = story.get("title", "Unknown title")
    description = story.get("description", "No description available")
    # Truncate description to reduce tokens
    if len(description) > 200:
        description = description[:200] + "..."
    source_count = story.get("source_count", 1)
    published_at = ""
    if story.get("sources") and len(story["sources"]) > 0:
        published_at = story["sources"][0].get("published_at", "")

    prompt = f"""
Title: {title}
Description: {description}
Sources: {source_count}
Published: {published_at}

Score this AI news story on the 5 criteria.
"""
    return prompt


async def score_story_with_retry(
    llm_provider: ILLMProvider,
    story: Dict[str, Any],
    semaphore: asyncio.Semaphore,
    delay: float
) -> Dict[str, Any]:
    async with semaphore:
        await asyncio.sleep(delay)  # spread requests
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                prompt = build_prompt(story)
                # Pass max_tokens=512 to the provider
                score = await llm_provider.generate_structured(
                    prompt, StoryScore, temperature=0.3, max_tokens=512
                )
                story_copy = story.copy()
                story_copy["score"] = score
                story_copy["scoring_error"] = None
                return story_copy
            except Exception as e:
                is_429 = False
                if hasattr(e, "response") and e.response.status_code == 429:
                    is_429 = True
                elif isinstance(e, Exception) and ("429" in str(e) or "rate" in str(e).lower()):
                    is_429 = True

                if is_429 and attempt < MAX_RETRIES:
                    wait_time = BASE_BACKOFF * (2 ** (attempt - 1)) + random.uniform(0, 1)
                    logger.warning(
                        f"Rate limit hit for story '{story.get('title', '')[:40]}...', "
                        f"retrying in {wait_time:.1f}s (attempt {attempt}/{MAX_RETRIES})"
                    )
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    logger.error(f"LLM scoring failed for story '{story.get('title', '')[:40]}...': {e}")
                    story_copy = story.copy()
                    story_copy["score"] = StoryScore(
                        industry_impact=0,
                        technical_significance=0,
                        audience_interest=0,
                        novelty=0,
                        overall_importance=0,
                        reason="Scoring failed"
                    )
                    story_copy["scoring_error"] = str(e)
                    return story_copy

        story_copy = story.copy()
        story_copy["score"] = StoryScore(
            industry_impact=0,
            technical_significance=0,
            audience_interest=0,
            novelty=0,
            overall_importance=0,
            reason="Max retries exceeded"
        )
        story_copy["scoring_error"] = "Max retries exceeded"
        return story_copy


async def ranking_node(state: NewsState) -> NewsState:
    stories = state.get("deduplicated_stories", [])
    if not stories:
        logger.warning("No stories to rank.")
        state["selected_stories"] = []
        return state

    llm_provider = GroqProvider()
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)

    tasks = [
        score_story_with_retry(llm_provider, story, semaphore, REQUEST_DELAY)
        for story in stories
    ]
    scored_stories = await asyncio.gather(*tasks)

    sorted_stories = sorted(
        scored_stories,
        key=lambda x: x["score"].overall_importance,
        reverse=True
    )

    selected = sorted_stories[:SELECT_COUNT]
    state["selected_stories"] = selected

    logger.info(f"Ranking complete. Selected {len(selected)} out of {len(stories)} stories.")
    for i, s in enumerate(selected, 1):
        logger.info(f"  #{i}: {s['title']} (score: {s['score'].overall_importance:.1f})")

    return state