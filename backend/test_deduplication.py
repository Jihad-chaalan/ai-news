import asyncio
import logging

# Suppress httpx logs to hide API keys
logging.getLogger("httpx").setLevel(logging.WARNING)

from app.graph.nodes.research_node import research_node
from app.graph.nodes.deduplication_node import deduplication_node
from app.graph.state import NewsState

logging.basicConfig(level=logging.INFO)


async def test_deduplication():
    state: NewsState = {"raw_articles": [], "errors": []}

    # 1. Research
    state = await research_node(state)
    print(f"Raw articles: {len(state.get('raw_articles', []))}")

    # 2. Deduplicate
    state = await deduplication_node(state)

    stories = state.get("deduplicated_stories", [])
    print(f"\nClustered into {len(stories)} unique stories")
    for i, story in enumerate(stories[:5], 1):
        print(f"{i}. {story['title']} ({story['source_count']} sources)")
        for src in story['sources']:
            print(f"   - {src['source_name']}: {src['url']}")


if __name__ == "__main__":
    asyncio.run(test_deduplication())