import asyncio
import logging
from typing import List

from app.adapters.news.apitube_provider import APITubeProvider
from app.adapters.news.newsdata_provider import NewsDataProvider
from app.config import settings
from app.models.article import Article
from app.ports.inews_provider import INewsProvider
from app.graph.state import NewsState

logger = logging.getLogger(__name__)


async def research_node(state: NewsState) -> NewsState:
    """
    LangGraph node that fetches articles from all enabled news providers in parallel.
    """
    # Map provider names to classes
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

    # Run all providers concurrently
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

    # Deduplicate by exact ID (same article from the same provider)
    seen = set()
    unique = []
    for article in all_articles:
        if article.id not in seen:
            seen.add(article.id)
            unique.append(article)

    state["raw_articles"] = unique
    logger.info(f"Research complete. Total unique articles: {len(unique)}")
    return state