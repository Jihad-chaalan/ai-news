from typing import TypedDict, List, Dict, Any, Optional
from app.models.article import Article

class NewsState(TypedDict, total=False):
    raw_articles: List[Article]
    deduplicated_stories: List[Dict[str, Any]]
    ranked_stories: List[Dict[str, Any]]
    selected_stories: List[Dict[str, Any]]
    summaries: Dict[str, Any]
    image_prompts: Dict[str, str]
    generated_images: Dict[str, str]
    validation_results: Dict[str, bool]
    retry_counts: Dict[str, int]
    final_briefing: Dict[str, Any]
    errors: List[str]