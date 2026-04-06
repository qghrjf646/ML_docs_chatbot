import { FormEvent, useEffect, useMemo, useState } from "react";
import { buildApiUrl } from "./lib/api";

type MatchDoc = {
  doc_id: string;
  arxiv_id: string;
  title: string;
  score: number;
  published: string;
  categories: string[];
  abs_url: string;
  pdf_url: string;
  snippet: string;
};

type ChatResponse = {
  answer: string;
  matched_documents: MatchDoc[];
  retrieval_mode: string;
  model_status: string;
  latency_ms: number;
};

type EvaluationSummary = {
  retrieval_recall_at_k: number;
  answer_faithfulness: number;
  answer_relevance: number;
  citation_precision: number;
  latency_p95_ms: number;
  total_interactions: number;
  status: string;
};

type IngestionReport = {
  requested: number;
  ingested_documents: number;
  generated_chunks: number;
  topology_embeddings: number;
  status: string;
  message: string;
};

const tabs = ["Overview", "Retrieval", "Generation", "End-to-End"] as const;

const formatPercent = (value: number) => `${(value * 100).toFixed(1)}%`;

function App() {
  const [question, setQuestion] = useState(
    "What are current trends in robust LLM evaluation metrics?"
  );
  const [answer, setAnswer] = useState<string>("");
  const [matches, setMatches] = useState<MatchDoc[]>([]);
  const [activeTab, setActiveTab] = useState<(typeof tabs)[number]>("Overview");
  const [chatMeta, setChatMeta] = useState<{ mode: string; model: string; latency: number } | null>(null);
  const [evaluation, setEvaluation] = useState<EvaluationSummary | null>(null);
  const [ingestion, setIngestion] = useState<IngestionReport | null>(null);
  const [loadingChat, setLoadingChat] = useState(false);
  const [loadingIngestion, setLoadingIngestion] = useState(false);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    void refreshEvaluation();
  }, []);

  const cards = useMemo(() => {
    return [
      {
        label: "Recall@K",
        value: evaluation ? formatPercent(evaluation.retrieval_recall_at_k) : "0.0%",
        note: "retrieval coverage"
      },
      {
        label: "Faithfulness",
        value: evaluation ? formatPercent(evaluation.answer_faithfulness) : "0.0%",
        note: "groundedness"
      },
      {
        label: "Citation Precision",
        value: evaluation ? formatPercent(evaluation.citation_precision) : "0.0%",
        note: "evidence quality"
      },
      {
        label: "Latency P95",
        value: evaluation ? `${evaluation.latency_p95_ms.toFixed(1)} ms` : "0 ms",
        note: "response speed"
      }
    ];
  }, [evaluation]);

  async function refreshEvaluation() {
    try {
      const response = await fetch(buildApiUrl("/api/v1/evaluation/summary"));
      if (!response.ok) {
        throw new Error(`Evaluation request failed with ${response.status}`);
      }
      const payload = (await response.json()) as EvaluationSummary;
      setEvaluation(payload);
    } catch (err) {
      setError((err as Error).message);
    }
  }

  async function handleIngestion() {
    setLoadingIngestion(true);
    setError("");
    try {
      const response = await fetch(buildApiUrl("/api/v1/ingestion/arxiv?max_docs=55"), {
        method: "POST"
      });
      if (!response.ok) {
        throw new Error(`Ingestion failed with ${response.status}`);
      }
      const payload = (await response.json()) as IngestionReport;
      setIngestion(payload);
      await refreshEvaluation();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoadingIngestion(false);
    }
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!question.trim()) {
      return;
    }

    setLoadingChat(true);
    setError("");
    try {
      const response = await fetch(buildApiUrl("/api/v1/chat"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ question })
      });

      if (!response.ok) {
        throw new Error(`Chat request failed with ${response.status}`);
      }

      const payload = (await response.json()) as ChatResponse;
      setAnswer(payload.answer);
      setMatches(payload.matched_documents);
      setChatMeta({
        mode: payload.retrieval_mode,
        model: payload.model_status,
        latency: payload.latency_ms
      });

      await refreshEvaluation();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoadingChat(false);
    }
  }

  return (
    <div className="page">
      <header className="hero">
        <p className="eyebrow">Graph RAG POC</p>
        <h1>Neo4j + Hugging Face Graph Chatbot</h1>
        <p>
          Corpus ArXiv charge, extraction metadata vers graphe, retrieval hybride,
          et tableau d&apos;evaluation continu.
        </p>

        <div className="hero-actions">
          <button
            type="button"
            className="primary-btn"
            onClick={handleIngestion}
            disabled={loadingIngestion}
          >
            {loadingIngestion ? "Ingestion en cours..." : "Ingest 55 ArXiv docs"}
          </button>
          {ingestion ? (
            <p className="status">
              {ingestion.ingested_documents} docs, {ingestion.generated_chunks} chunks,
              {" "}{ingestion.topology_embeddings} embeddings
            </p>
          ) : null}
        </div>
      </header>

      <main className="grid">
        <section className="panel">
          <h2>Chat</h2>
          <p className="muted">Pose une question pour interroger le graphe.</p>

          <form className="chat-form" onSubmit={handleSubmit}>
            <textarea
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              rows={5}
              placeholder="Ask a question about the ingested research corpus..."
            />
            <button type="submit" className="primary-btn" disabled={loadingChat}>
              {loadingChat ? "Generation..." : "Ask"}
            </button>
          </form>

          <div className="answer-box">
            <h3>Answer</h3>
            <p>{answer || "No answer yet."}</p>
          </div>

          {chatMeta ? (
            <div className="meta-row">
              <span>Mode: {chatMeta.mode}</span>
              <span>Model: {chatMeta.model}</span>
              <span>Latency: {chatMeta.latency.toFixed(1)} ms</span>
            </div>
          ) : null}
        </section>

        <section className="panel">
          <h2>Matched Documents</h2>
          <p className="muted">Sources retenues par le retrieval graph-aware.</p>

          <div className="doc-list">
            {matches.length === 0 ? (
              <p className="muted">Aucun document matche pour le moment.</p>
            ) : (
              matches.map((doc) => (
                <article className="doc-card" key={doc.doc_id}>
                  <p className="doc-title">{doc.title}</p>
                  <p className="doc-meta">
                    {doc.arxiv_id} • score {doc.score.toFixed(3)} • {doc.categories.join(", ")}
                  </p>
                  <p className="doc-snippet">{doc.snippet}</p>
                  <div className="doc-links">
                    <a href={doc.abs_url} target="_blank" rel="noreferrer">Abstract</a>
                    <a href={doc.pdf_url} target="_blank" rel="noreferrer">PDF</a>
                  </div>
                </article>
              ))
            )}
          </div>
        </section>

        <section className="panel wide">
          <h2>Evaluation Tabs</h2>
          <p className="muted">Mesures retrieval, generation et experience E2E.</p>

          <div className="tabs">
            {tabs.map((tab) => (
              <button
                type="button"
                key={tab}
                className={`tab ${activeTab === tab ? "active" : ""}`}
                onClick={() => setActiveTab(tab)}
              >
                {tab}
              </button>
            ))}
          </div>

          <div className="cards">
            {cards.map((metric) => (
              <article className="metric" key={metric.label}>
                <p>{metric.label}</p>
                <strong>{metric.value}</strong>
                <span>{metric.note}</span>
              </article>
            ))}
          </div>

          <div className="eval-panel">
            {activeTab === "Overview" ? (
              <p>
                Interactions observees: <strong>{evaluation?.total_interactions ?? 0}</strong>. Etat:
                <strong> {evaluation?.status ?? "cold_start"}</strong>.
              </p>
            ) : null}

            {activeTab === "Retrieval" ? (
              <p>
                Recall@K: <strong>{evaluation ? formatPercent(evaluation.retrieval_recall_at_k) : "0.0%"}</strong>.
                Cette mesure suit la presence de documents preuves dans les reponses.
              </p>
            ) : null}

            {activeTab === "Generation" ? (
              <p>
                Faithfulness: <strong>{evaluation ? formatPercent(evaluation.answer_faithfulness) : "0.0%"}</strong>;
                Relevance: <strong>{evaluation ? formatPercent(evaluation.answer_relevance) : "0.0%"}</strong>.
              </p>
            ) : null}

            {activeTab === "End-to-End" ? (
              <p>
                Latency P95: <strong>{evaluation ? `${evaluation.latency_p95_ms.toFixed(1)} ms` : "0 ms"}</strong>;
                Citation precision: <strong>{evaluation ? formatPercent(evaluation.citation_precision) : "0.0%"}</strong>.
              </p>
            ) : null}
          </div>
        </section>
      </main>

      {error ? <p className="error">Error: {error}</p> : null}
    </div>
  );
}

export default App;
