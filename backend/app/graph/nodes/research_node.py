import asyncio
import logging
import re
from typing import List, Set

from app.adapters.news.apitube_provider import APITubeProvider
from app.adapters.news.newsdata_provider import NewsDataProvider
from app.config import settings
from app.models.article import Article
from app.ports.inews_provider import INewsProvider
from app.graph.state import NewsState

logger = logging.getLogger(__name__)

# ----- AI keyword lists (single words and multi-word phrases) -----
AI_SINGLE_WORDS: Set[str] = {
    "ai", "openai", "anthropic", "google", "gemini", "claude", "deepmind",
    "chatgpt", "copilot", "llama", "mistral", "stablediffusion",
    "llm", "gpt", "bert", "transformer", "neural", "nlp",
    "generative", "inference", "finetuning", "prompt",
    "nvidia", "gpu", "tpu", "deepseek", "kimi"
}

AI_PHRASES: Set[str] = {
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "large language",
    "neural network",
    "natural language processing"
}

def is_ai_related(title: str) -> bool:
    """Return True if the title contains AI keywords as whole words or phrases."""
    if not title:
        return False
    title_lower = title.lower()
    
    # Check for multi-word phrases first
    for phrase in AI_PHRASES:
        if phrase in title_lower:
            return True
    
    # Split into tokens (remove punctuation)
    tokens = re.findall(r'\b[a-z0-9]+\b', title_lower)
    return any(token in AI_SINGLE_WORDS for token in tokens)


async def research_node(state: NewsState) -> NewsState:
    """
    LangGraph node that:
      1. Fetches articles from all enabled news providers in parallel.
      2. Filters out articles whose titles contain no AI keywords (exact word matching).
      3. Deduplicates by exact article ID.
    """
    # 1. Build provider instances
    provider_map = {
        "apitube": APITubeProvider,
        "newsdata": NewsDataProvider,
    }

    providers: List[INewsProvider] = []
    for name in settings.ENABLED_NEWS_PROVIDERS:
        if name in provider_map:
            providers.append(provider_map[name]())
        else:
            logger.warning(f"Unknown news provider: {name}")

    if not providers:
        raise RuntimeError("No news providers enabled.")

    # 2. Run all providers concurrently
    tasks = [
        provider.search(
            query=settings.NEWS_QUERY,
            date_range=settings.NEWS_DATE_RANGE,
            limit=settings.NEWS_LIMIT_PER_PROVIDER
        )
        for provider in providers
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    all_articles: List[Article] = []
    for idx, result in enumerate(results):
        provider_name = providers[idx].__class__.__name__
        if isinstance(result, Exception):
            logger.error(f"Provider {provider_name} failed: {result}")
            state.setdefault("errors", []).append(f"{provider_name}: {str(result)}")
        else:
            all_articles.extend(result)
            logger.info(f"Provider {provider_name} returned {len(result)} articles")

    logger.info(f"Total articles before filter: {len(all_articles)}")

    # 3. Apply strict title filter (whole‑word matching)
    filtered_articles = [
        article for article in all_articles
        if is_ai_related(article.title)
    ]

    filtered_out_count = len(all_articles) - len(filtered_articles)
    if filtered_out_count > 0:
        # Log a sample of removed titles for debugging
        removed_titles = []
        for article in all_articles:
            if not is_ai_related(article.title):
                removed_titles.append(article.title)
                if len(removed_titles) >= 5:
                    break
        logger.info(
            f"Filtered out {filtered_out_count} non-AI articles. "
            f"Examples: {removed_titles}"
        )
    else:
        logger.info("All articles passed the AI title filter.")

    # 4. Deduplicate by exact ID
    seen = set()
    unique = []
    for article in filtered_articles:
        if article.id not in seen:
            seen.add(article.id)
            unique.append(article)

    state["raw_articles"] = unique
    logger.info(f"Research complete. Final unique articles: {len(unique)}")
    return state