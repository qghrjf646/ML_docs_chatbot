#!/usr/bin/env python3
"""Fetch an ArXiv corpus with PDFs and rich metadata for Graph RAG ingestion.

This script downloads:
- one metadata JSON file per paper
- one abstract markdown file per paper
- one PDF file per paper
- one global index file for quick ingestion
"""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path


ARXIV_API = "https://export.arxiv.org/api/query"


@dataclass
class PaperRecord:
    arxiv_id: str
    title: str
    summary: str
    published: str
    updated: str
    authors: list[str]
    categories: list[str]
    primary_category: str
    pdf_url: str
    abs_url: str
    doi: str | None
    journal_ref: str | None
    comment: str | None


def sanitize_filename(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]", "_", value)


def parse_entry(entry: ET.Element, ns: dict[str, str]) -> PaperRecord:
    entry_id = entry.findtext("atom:id", default="", namespaces=ns).strip()
    arxiv_id = entry_id.rsplit("/", 1)[-1]

    title = " ".join(
        entry.findtext("atom:title", default="", namespaces=ns).split()
    )
    summary = " ".join(
        entry.findtext("atom:summary", default="", namespaces=ns).split()
    )
    published = entry.findtext("atom:published", default="", namespaces=ns)
    updated = entry.findtext("atom:updated", default="", namespaces=ns)

    authors = [
        " ".join(author.findtext("atom:name", default="", namespaces=ns).split())
        for author in entry.findall("atom:author", namespaces=ns)
    ]

    categories = [
        c.attrib.get("term", "")
        for c in entry.findall("atom:category", namespaces=ns)
        if c.attrib.get("term")
    ]

    primary = ""
    primary_node = entry.find("arxiv:primary_category", namespaces=ns)
    if primary_node is not None:
        primary = primary_node.attrib.get("term", "")

    doi = entry.findtext("arxiv:doi", default=None, namespaces=ns)
    journal_ref = entry.findtext("arxiv:journal_ref", default=None, namespaces=ns)
    comment = entry.findtext("arxiv:comment", default=None, namespaces=ns)

    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    abs_url = f"https://arxiv.org/abs/{arxiv_id}"

    return PaperRecord(
        arxiv_id=arxiv_id,
        title=title,
        summary=summary,
        published=published,
        updated=updated,
        authors=authors,
        categories=categories,
        primary_category=primary,
        pdf_url=pdf_url,
        abs_url=abs_url,
        doi=doi,
        journal_ref=journal_ref,
        comment=comment,
    )


def fetch_feed(search_query: str, start: int, max_results: int, sort_by: str, sort_order: str) -> str:
    params = {
        "search_query": search_query,
        "start": str(start),
        "max_results": str(max_results),
        "sortBy": sort_by,
        "sortOrder": sort_order,
    }
    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ML_docs_chatbot/1.0 (Graph-RAG corpus fetcher)"},
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read().decode("utf-8")


def download_file(url: str, output_path: Path) -> bool:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ML_docs_chatbot/1.0 (Graph-RAG corpus fetcher)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            output_path.write_bytes(response.read())
        return True
    except Exception:
        return False


def write_abstract_markdown(record: PaperRecord, output_path: Path) -> None:
    lines = [
        f"# {record.title}",
        "",
        f"- arXiv ID: {record.arxiv_id}",
        f"- Published: {record.published}",
        f"- Updated: {record.updated}",
        f"- Authors: {', '.join(record.authors)}",
        f"- Categories: {', '.join(record.categories)}",
        f"- Primary category: {record.primary_category}",
        f"- Abstract page: {record.abs_url}",
        f"- PDF: {record.pdf_url}",
        "",
        "## Abstract",
        "",
        record.summary,
        "",
    ]
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch ArXiv docs with metadata")
    parser.add_argument("--count", type=int, default=50, help="Minimum number of docs")
    parser.add_argument(
        "--query",
        type=str,
        default="cat:cs.AI OR cat:cs.LG OR cat:cs.CL",
        help="ArXiv search query",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/arxiv"),
        help="Output root directory",
    )
    parser.add_argument(
        "--sort-by",
        type=str,
        default="submittedDate",
        choices=["relevance", "lastUpdatedDate", "submittedDate"],
    )
    parser.add_argument(
        "--sort-order",
        type=str,
        default="descending",
        choices=["ascending", "descending"],
    )
    args = parser.parse_args()

    output_root = args.output_dir
    metadata_dir = output_root / "metadata"
    abstracts_dir = output_root / "abstracts"
    pdf_dir = output_root / "pdfs"
    for folder in (metadata_dir, abstracts_dir, pdf_dir):
        folder.mkdir(parents=True, exist_ok=True)

    page_size = min(max(args.count, 50), 100)
    feed_xml = fetch_feed(args.query, start=0, max_results=page_size, sort_by=args.sort_by, sort_order=args.sort_order)

    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom",
    }
    root = ET.fromstring(feed_xml)
    entries = root.findall("atom:entry", namespaces=ns)

    records: list[PaperRecord] = []
    for entry in entries:
        records.append(parse_entry(entry, ns))
        if len(records) >= args.count:
            break

    if len(records) < args.count:
        raise RuntimeError(
            f"Requested {args.count} docs but only found {len(records)} entries for query '{args.query}'."
        )

    downloaded = 0
    for idx, record in enumerate(records, start=1):
        safe_id = sanitize_filename(record.arxiv_id)

        metadata_path = metadata_dir / f"{safe_id}.json"
        abstract_path = abstracts_dir / f"{safe_id}.md"
        pdf_path = pdf_dir / f"{safe_id}.pdf"

        metadata_path.write_text(
            json.dumps(asdict(record), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        write_abstract_markdown(record, abstract_path)

        if download_file(record.pdf_url, pdf_path):
            downloaded += 1
        else:
            # Keep metadata and abstract even if PDF fails.
            if pdf_path.exists():
                pdf_path.unlink()

        if idx % 10 == 0:
            time.sleep(1)

    index = {
        "source": "arxiv",
        "query": args.query,
        "requested_count": args.count,
        "fetched_entries": len(records),
        "pdf_downloaded": downloaded,
        "generated_at_epoch": int(time.time()),
        "records": [asdict(r) for r in records],
    }
    (output_root / "arxiv_index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(
        f"Fetched {len(records)} records, downloaded {downloaded} PDFs, output dir: {output_root}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
