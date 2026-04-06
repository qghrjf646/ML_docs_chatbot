from __future__ import annotations

import json

from app.services.arxiv_loader import ArxivCorpusLoader


def _metadata_payload(arxiv_id: str) -> dict:
    return {
        "arxiv_id": arxiv_id,
        "title": "  A   spaced   title  ",
        "summary": "  A summary   with  extra spaces. ",
        "published": "2026-01-01T00:00:00Z",
        "updated": "2026-01-01T00:00:00Z",
        "authors": ["Alice", "Bob"],
        "categories": ["cs.AI"],
        "primary_category": "cs.AI",
        "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
        "abs_url": f"https://arxiv.org/abs/{arxiv_id}",
        "doi": None,
        "journal_ref": None,
        "comment": None,
    }


def test_load_documents_with_normalization(tmp_path) -> None:
    metadata_dir = tmp_path / "metadata"
    abstracts_dir = tmp_path / "abstracts"
    metadata_dir.mkdir()
    abstracts_dir.mkdir()

    (metadata_dir / "1.json").write_text(json.dumps(_metadata_payload("1111.00001v1")), encoding="utf-8")
    (metadata_dir / "2.json").write_text(json.dumps(_metadata_payload("1111.00002v1")), encoding="utf-8")

    loader = ArxivCorpusLoader(str(metadata_dir), str(abstracts_dir))
    docs = loader.load_documents(max_docs=1)

    assert len(docs) == 1
    assert docs[0].title == "A spaced title"
    assert docs[0].summary == "A summary with extra spaces."


def test_load_abstract_text_returns_empty_if_missing(tmp_path) -> None:
    loader = ArxivCorpusLoader(str(tmp_path / "metadata"), str(tmp_path / "abstracts"))
    assert loader.load_abstract_text("missing") == ""


def test_load_abstract_text_reads_file(tmp_path) -> None:
    metadata_dir = tmp_path / "metadata"
    abstracts_dir = tmp_path / "abstracts"
    metadata_dir.mkdir()
    abstracts_dir.mkdir()

    (abstracts_dir / "1111.00001v1.md").write_text("# Abstract", encoding="utf-8")
    loader = ArxivCorpusLoader(str(metadata_dir), str(abstracts_dir))

    assert loader.load_abstract_text("1111.00001v1") == "# Abstract"
