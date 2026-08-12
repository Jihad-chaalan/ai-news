import asyncio
import logging

from app.graph.nodes.research_node import research_node
from app.graph.state import NewsState

logging.getLogger("httpx").setLevel(logging.WARNING)
# Set up logging to see output
logging.basicConfig(level=logging.INFO)

async def test_research():
    state: NewsState = {
        "raw_articles": [],
        "errors": [],
    }

    # Run the research node
    updated_state = await research_node(state)

    # Print results
    articles = updated_state.get("raw_articles", [])
    errors = updated_state.get("errors", [])
    print(f"Fetched {len(articles)} articles")
    if errors:
        print("Errors:", errors)
    for i, article in enumerate(articles[:10], 1):
        print(f"{i}. {article.title} ({article.source_name})")

if __name__ == "__main__":
    asyncio.run(test_research())