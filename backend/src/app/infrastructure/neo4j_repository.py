from __future__ import annotations

from neo4j import GraphDatabase

from app.core.config import Settings
from app.domain.models import ArxivDocument, ChunkPayload


class Neo4jRepository:
    def __init__(self, settings: Settings) -> None:
        self._driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password),
        )

    def close(self) -> None:
        self._driver.close()

    def ping(self) -> bool:
        try:
            with self._driver.session() as session:
                session.run("RETURN 1 AS ok").single()
            return True
        except Exception:
            return False

    def ensure_schema(self) -> None:
        statements = [
            "CREATE CONSTRAINT document_doc_id IF NOT EXISTS FOR (d:Document) REQUIRE d.doc_id IS UNIQUE",
            "CREATE CONSTRAINT chunk_chunk_id IF NOT EXISTS FOR (c:Chunk) REQUIRE c.chunk_id IS UNIQUE",
            "CREATE CONSTRAINT author_name IF NOT EXISTS FOR (a:Author) REQUIRE a.name IS UNIQUE",
            "CREATE CONSTRAINT category_code IF NOT EXISTS FOR (c:Category) REQUIRE c.code IS UNIQUE",
            "CREATE CONSTRAINT source_source_id IF NOT EXISTS FOR (s:Source) REQUIRE s.source_id IS UNIQUE",
        ]
        with self._driver.session() as session:
            for stmt in statements:
                session.run(stmt)

    def upsert_document(
        self,
        doc: ArxivDocument,
        chunks: list[ChunkPayload],
        base_embedding: list[float],
    ) -> None:
        payload = {
            "doc_id": doc.doc_id,
            "arxiv_id": doc.arxiv_id,
            "title": doc.title,
            "summary": doc.summary,
            "published": doc.published,
            "updated": doc.updated,
            "primary_category": doc.primary_category,
            "pdf_url": doc.pdf_url,
            "abs_url": doc.abs_url,
            "doi": doc.doi,
            "journal_ref": doc.journal_ref,
            "comment": doc.comment,
            "base_embedding": base_embedding,
            "authors": doc.authors,
            "categories": doc.categories,
            "chunks": [chunk.model_dump() for chunk in chunks],
        }

        with self._driver.session() as session:
            session.run(
                """
                MERGE (s:Source {source_id: 'arxiv'})
                SET s.name = 'arXiv', s.kind = 'open-source repository'
                MERGE (d:Document {doc_id: $doc_id})
                SET d.arxiv_id = $arxiv_id,
                    d.title = $title,
                    d.summary = $summary,
                    d.published = $published,
                    d.updated = $updated,
                    d.primary_category = $primary_category,
                    d.pdf_url = $pdf_url,
                    d.abs_url = $abs_url,
                    d.doi = $doi,
                    d.journal_ref = $journal_ref,
                    d.comment = $comment,
                    d.base_embedding = $base_embedding
                MERGE (d)-[:FROM_SOURCE]->(s)
                """,
                payload,
            )

            session.run(
                """
                MATCH (d:Document {doc_id: $doc_id})
                UNWIND $authors AS author_name
                MERGE (a:Author {name: author_name})
                MERGE (d)-[:AUTHORED_BY]->(a)
                """,
                payload,
            )

            session.run(
                """
                MATCH (d:Document {doc_id: $doc_id})
                UNWIND $categories AS category_code
                MERGE (c:Category {code: category_code})
                MERGE (d)-[:IN_CATEGORY]->(c)
                """,
                payload,
            )

            session.run(
                """
                MATCH (d:Document {doc_id: $doc_id})-[r:HAS_CHUNK]->(c:Chunk)
                DELETE r, c
                """,
                payload,
            )

            session.run(
                """
                MATCH (d:Document {doc_id: $doc_id})
                UNWIND $chunks AS chunk
                MERGE (c:Chunk {chunk_id: chunk.chunk_id})
                SET c.text = chunk.text,
                    c.position = chunk.position,
                    c.token_count = chunk.token_count
                MERGE (d)-[:HAS_CHUNK]->(c)
                """,
                payload,
            )

            session.run(
                """
                MATCH (d:Document {doc_id: $doc_id})-[:HAS_CHUNK]->(c:Chunk)
                WITH d, c
                ORDER BY c.position
                WITH collect(c) AS chunks
                UNWIND range(0, size(chunks)-2) AS i
                WITH chunks[i] AS c1, chunks[i+1] AS c2
                MERGE (c1)-[:NEXT]->(c2)
                """,
                payload,
            )

    def set_topology_embeddings(self, embeddings: dict[str, list[float]]) -> int:
        rows = [{"doc_id": doc_id, "embedding": embedding} for doc_id, embedding in embeddings.items()]
        if not rows:
            return 0
        with self._driver.session() as session:
            session.run(
                """
                UNWIND $rows AS row
                MATCH (d:Document {doc_id: row.doc_id})
                SET d.topology_embedding = row.embedding
                """,
                {"rows": rows},
            )
        return len(rows)

    def fetch_documents(self, limit: int = 500) -> list[dict]:
        query = """
        MATCH (d:Document)
        WITH d
        RETURN d {
            .*,
            authors: [(d)-[:AUTHORED_BY]->(a:Author) | a.name],
            categories: [(d)-[:IN_CATEGORY]->(cat:Category) | cat.code],
            chunks: [(d)-[:HAS_CHUNK]->(c:Chunk) | c { .chunk_id, .text, .position, .token_count }],
            graph_degree: size((d)--())
        } AS doc
        ORDER BY d.published DESC
        LIMIT $limit
        """
        with self._driver.session() as session:
            result = session.run(query, {"limit": limit})
            return [record["doc"] for record in result]

    def graph_stats(self) -> dict[str, int]:
        query = """
                CALL {
                    MATCH (d:Document)
                    RETURN count(d) AS documents
                }
                CALL {
                    MATCH (c:Chunk)
                    RETURN count(c) AS chunks
                }
                CALL {
                    MATCH (a:Author)
                    RETURN count(a) AS authors
                }
                CALL {
                    MATCH (cat:Category)
                    RETURN count(cat) AS categories
                }
                CALL {
                    MATCH ()-[r]-()
                    RETURN count(r) AS relationships
                }
                RETURN documents, chunks, authors, categories, relationships
        """
        with self._driver.session() as session:
            row = session.run(query).single()
            if row is None:
                return {
                    "documents": 0,
                    "chunks": 0,
                    "authors": 0,
                    "categories": 0,
                    "relationships": 0,
                }
            return {
                "documents": int(row["documents"]),
                "chunks": int(row["chunks"]),
                "authors": int(row["authors"]),
                "categories": int(row["categories"]),
                "relationships": int(row["relationships"]),
            }
