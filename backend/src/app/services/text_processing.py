from __future__ import annotations

import math
import re


TOKEN_RE = re.compile(r"[a-zA-Z0-9]{2,}")


def normalize_text(value: str) -> str:
    return " ".join(value.split())


def tokenize(value: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(value)]


def split_into_chunks(text: str, *, chunk_size: int = 120, overlap: int = 20) -> list[str]:
    words = text.split()
    if not words:
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be < chunk_size")

    chunks: list[str] = []
    step = chunk_size - overlap
    for start in range(0, len(words), step):
        chunk_words = words[start : start + chunk_size]
        if not chunk_words:
            continue
        chunks.append(" ".join(chunk_words))
        if start + chunk_size >= len(words):
            break
    return chunks


def hash_embedding(text: str, dim: int) -> list[float]:
    if dim <= 0:
        raise ValueError("dim must be > 0")

    vec = [0.0] * dim
    for token in tokenize(text):
        idx = hash(token) % dim
        vec[idx] += 1.0

    norm = math.sqrt(sum(v * v for v in vec))
    if norm == 0:
        return vec
    return [v / norm for v in vec]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if len(a) != len(b) or not a:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def jaccard_similarity(a_tokens: set[str], b_tokens: set[str]) -> float:
    if not a_tokens or not b_tokens:
        return 0.0
    inter = len(a_tokens.intersection(b_tokens))
    union = len(a_tokens.union(b_tokens))
    if union == 0:
        return 0.0
    return inter / union
