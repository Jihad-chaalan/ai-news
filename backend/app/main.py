import asyncio
import logging

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("groq").setLevel(logging.INFO)

from app.graph.graph import get_graph
from app.graph.state import NewsState

async def main():
    state: NewsState = {
        "raw_articles": [],
        "errors": [],
        "deduplicated_stories": [],
        "ranked_stories": [],
        "selected_stories": [],
        "summaries": {},
        "image_prompts": {},
        "generated_images": {},
        "validation_results": {},
        "retry_counts": {},
        "final_briefing": None,
        "pending_stories": [],
        "validated_stories": [],
    }

    graph = get_graph()
    final_state = await graph.ainvoke(state)

    validated = final_state.get("validated_stories", [])
    if validated:
        print(f"\n✅ {len(validated)} stories passed validation:\n")
        for i, story in enumerate(validated, 1):
            summary = story.get("summary", {})
            print(f"{i}. {summary.get('title', story.get('title', 'No title'))}")
            print(f"   Summary: {summary.get('summary', 'N/A')}")
            print(f"   Why: {summary.get('why_it_matters', 'N/A')}")
            print(f"   Key points: {summary.get('key_points', [])}")
            print(f"   Image prompt: {story.get('image_prompt', 'N/A')[:200]}...")
            print()
    else:
        print("❌ No stories passed validation.")

if __name__ == "__main__":
    asyncio.run(main())