from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_env: str
    neo4j_uri: str
    neo4j_user: str
    neo4j_password: str
    hf_token: str
    hf_model_id: str
    arxiv_metadata_dir: str
    arxiv_abstracts_dir: str
    retrieval_top_k: int
    embedding_dim: int


settings = Settings(
    app_env=os.getenv("APP_ENV", "development"),
    neo4j_uri=os.getenv("NEO4J_URI", "bolt://neo4j:7687"),
    neo4j_user=os.getenv("NEO4J_USER", "neo4j"),
    neo4j_password=os.getenv("NEO4J_PASSWORD", "neo4jpassword"),
    hf_token=os.getenv("HF_TOKEN", ""),
    hf_model_id=os.getenv("HF_MODEL_ID", "google/gemma-4-31b-it"),
    arxiv_metadata_dir=os.getenv("ARXIV_METADATA_DIR", "docs/arxiv/metadata"),
    arxiv_abstracts_dir=os.getenv("ARXIV_ABSTRACTS_DIR", "docs/arxiv/abstracts"),
    retrieval_top_k=int(os.getenv("RETRIEVAL_TOP_K", "5")),
    embedding_dim=int(os.getenv("EMBEDDING_DIM", "64")),
)
