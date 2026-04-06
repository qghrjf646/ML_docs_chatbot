from __future__ import annotations

import json
from pathlib import Path

from app.domain.models import ArxivDocument
from app.services.text_processing import normalize_text


class ArxivCorpusLoader:
    def __init__(self, metadata_dir: str, abstracts_dir: str) -> None:
        self.metadata_dir = Path(metadata_dir)
        self.abstracts_dir = Path(abstracts_dir)

    def load_documents(self, max_docs: int | None = None) -> list[ArxivDocument]:
        if not self.metadata_dir.exists():
            return []

        files = sorted(self.metadata_dir.glob("*.json"))
        if max_docs is not None:
            files = files[: max_docs if max_docs > 0 else 0]

        docs: list[ArxivDocument] = []
        for file_path in files:
            payload = json.loads(file_path.read_text(encoding="utf-8"))
            payload["title"] = normalize_text(payload.get("title", ""))
            payload["summary"] = normalize_text(payload.get("summary", ""))
            docs.append(ArxivDocument(**payload))
        return docs

    def load_abstract_text(self, arxiv_id: str) -> str:
        file_path = self.abstracts_dir / f"{arxiv_id}.md"
        if not file_path.exists():
            return ""
        return file_path.read_text(encoding="utf-8")
