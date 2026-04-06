from __future__ import annotations

import math

import pytest

from app.services.text_processing import (
    cosine_similarity,
    hash_embedding,
    jaccard_similarity,
    split_into_chunks,
    tokenize,
)


def test_split_into_chunks_returns_empty_on_empty_input() -> None:
    assert split_into_chunks("") == []


def test_split_into_chunks_raises_on_invalid_overlap() -> None:
    with pytest.raises(ValueError):
        split_into_chunks("a b c", chunk_size=5, overlap=5)


def test_split_into_chunks_with_overlap() -> None:
    text = " ".join(f"tok{i}" for i in range(15))
    chunks = split_into_chunks(text, chunk_size=6, overlap=2)
    assert len(chunks) == 4
    assert chunks[0].split()[:2] == ["tok0", "tok1"]
    assert chunks[1].split()[:2] == ["tok4", "tok5"]


def test_hash_embedding_is_normalized_for_non_empty_text() -> None:
    vec = hash_embedding("Graph rag retrieval", dim=32)
    norm = math.sqrt(sum(v * v for v in vec))
    assert len(vec) == 32
    assert pytest.approx(norm, rel=1e-6) == 1.0


def test_hash_embedding_handles_empty_text() -> None:
    vec = hash_embedding("", dim=16)
    assert vec == [0.0] * 16


def test_cosine_similarity_handles_zero_vectors() -> None:
    assert cosine_similarity([0.0, 0.0], [0.0, 0.0]) == 0.0


def test_cosine_similarity_matches_parallel_vectors() -> None:
    assert pytest.approx(cosine_similarity([1.0, 2.0], [2.0, 4.0]), rel=1e-6) == 1.0


def test_jaccard_similarity_basic() -> None:
    a = set(tokenize("graph rag"))
    b = set(tokenize("graph neural network"))
    assert jaccard_similarity(a, b) == pytest.approx(1 / 4)
