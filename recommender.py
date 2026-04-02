from datetime import datetime, timezone
from math import exp

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def _hours_since(timestamp: str) -> float:
    try:
        dt = datetime.fromisoformat(timestamp)
    except ValueError:
        return 168.0
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    delta = datetime.now(timezone.utc) - dt.astimezone(timezone.utc)
    return max(delta.total_seconds() / 3600.0, 0.0)


def rank_news(user_interest: str, news_items: list[dict], top_k: int = 5) -> list[dict]:
    if not news_items:
        return []

    model = get_model()
    docs = [f"{n['title']}. {n['summary']}" for n in news_items]
    text_vectors = model.encode(docs, normalize_embeddings=True)
    query_vec = model.encode([user_interest], normalize_embeddings=True)

    similarities = cosine_similarity(query_vec, text_vectors)[0]

    hours = np.array([_hours_since(n["published_at"]) for n in news_items], dtype=np.float32)
    freshness = np.exp(-hours / 72.0)

    # Weighted score: semantic relevance + freshness bonus.
    score = 0.75 * similarities + 0.25 * freshness

    ranked_idx = np.argsort(score)[::-1][:top_k]
    results = []
    for idx in ranked_idx:
        item = dict(news_items[idx])
        item["score"] = float(score[idx])
        item["similarity"] = float(similarities[idx])
        results.append(item)
    return results
