import asyncio
import logging

logging.getLogger("httpx").setLevel(logging.WARNING)

from app.graph.nodes.research_node import research_node
from app.graph.nodes.deduplication_node import deduplication_node
from app.graph.nodes.ranking_node import ranking_node
from app.graph.state import NewsState

logging.basicConfig(level=logging.INFO)

async def test_ranking():
    state: NewsState = {"raw_articles": [], "errors": []}

    # 1. Research
    state = await research_node(state)
    print(f"Raw articles: {len(state.get('raw_articles', []))}")

    # 2. Deduplicate
    state = await deduplication_node(state)
    stories = state.get("deduplicated_stories", [])
    print(f"Deduplicated stories: {len(stories)}")

    # 3. Rank
    state = await ranking_node(state)
    selected = state.get("selected_stories", [])
    print(f"\n--- Top {len(selected)} stories ---")
    for i, s in enumerate(selected, 1):
        score = s.get("score")
        print(f"{i}. {s['title']}")
        if score:
            print(f"   Importance: {score.overall_importance:.1f}")
            print(f"   Reason: {score.reason}")
        print()

if __name__ == "__main__":
    asyncio.run(test_ranking())