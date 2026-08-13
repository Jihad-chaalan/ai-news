import logging
import re
from collections import defaultdict
from typing import List, Dict, Any

import numpy as np
from sentence_transformers import SentenceTransformer

from app.models.article import Article
from app.graph.state import NewsState

logger = logging.getLogger(__name__)

# Global model cache – load only once
_MODEL = None


def get_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer('all-MiniLM-L6-v2')  
    return _MODEL


def normalize_title(title: str) -> str:
    """
    Clean the title for better embedding comparison.
    """
    if not title:
        return ""
    title = title.lower()
    # Remove punctuation (keep only letters, digits and spaces)
    title = re.sub(r'[^\w\s]', '', title)
    # Remove common stopwords (very short list to avoid over‑filtering)
    stopwords = {"a", "an", "the", "to", "for", "of", "on", "at", "with", "by", "from", "up", "about", "into", "through", "during", "including"}
    words = [w for w in title.split() if w not in stopwords]
    return " ".join(words)


async def deduplication_node(state: NewsState) -> NewsState:
    """
    Clusters articles by semantic similarity of their titles.
    """
    articles = state.get("raw_articles", [])
    if not articles:
        logger.warning("No articles to deduplicate.")
        state["deduplicated_stories"] = []
        return state

    # 1. Normalise titles
    norm_titles = [normalize_title(article.title) for article in articles]

    # 2. Generate embeddings
    model = get_model()
    embeddings = model.encode(norm_titles, convert_to_numpy=True)

    # 3. Compute cosine similarity matrix
    # Since the embeddings are normalised, dot product equals cosine similarity.
    sim_matrix = np.inner(embeddings, embeddings)

    # 4. Clustering with threshold
    threshold = 0.80 
    n = len(articles)
    visited = [False] * n
    clusters = []

    for i in range(n):
        if visited[i]:
            continue
        # Start a new cluster with article i
        cluster_indices = [i]
        visited[i] = True
        for j in range(i + 1, n):
            if not visited[j] and sim_matrix[i][j] >= threshold:
                cluster_indices.append(j)
                visited[j] = True
        clusters.append(cluster_indices)

    # 5. Build deduplicated stories
    deduplicated_stories = []
    for cluster_idx, indices in enumerate(clusters):
        cluster_articles = [articles[idx] for idx in indices]
        # Pick the first article as the representative
        representative = cluster_articles[0]
        story = {
            "id": f"story_{cluster_idx}",
            "title": representative.title,
            "description": representative.description,
            "sources": [
                {
                    "url": a.url,
                    "source_name": a.source_name,
                    "published_at": a.published_at.isoformat() if a.published_at else None
                }
                for a in cluster_articles
            ],
            "source_count": len(cluster_articles),
            "articles": cluster_articles,  # keep full objects for later ranking
        }
        deduplicated_stories.append(story)

    state["deduplicated_stories"] = deduplicated_stories
    logger.info(f"Deduplication complete: {len(articles)} articles → {len(deduplicated_stories)} unique stories")
    return state