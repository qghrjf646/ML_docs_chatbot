from __future__ import annotations

from huggingface_hub import InferenceClient

from app.domain.models import DocumentMatch


class LLMService:
    def __init__(self, model_id: str, token: str) -> None:
        self.model_id = model_id
        self.token = token

    def generate_answer(self, question: str, matches: list[DocumentMatch]) -> tuple[str, str]:
        context_blocks = []
        for idx, match in enumerate(matches, start=1):
            context_blocks.append(
                (
                    f"[DOC {idx}] {match.title} ({match.arxiv_id})\n"
                    f"Categories: {', '.join(match.categories)}\n"
                    f"Snippet: {match.snippet}\n"
                    f"Source: {match.abs_url}"
                )
            )

        context = "\n\n".join(context_blocks) if context_blocks else "No matched context."
        prompt = (
            "You are a Graph RAG assistant. "
            "Answer using ONLY the provided context snippets. "
            "If context is insufficient, say so explicitly. "
            "At the end, include a 'Citations' section with arXiv IDs.\n\n"
            f"Question:\n{question}\n\n"
            f"Context:\n{context}\n\n"
            "Answer:"
        )

        if not self.token:
            return self._fallback_answer(question, matches), "fallback_no_token"

        try:
            client = InferenceClient(model=self.model_id, token=self.token)
            generated = client.text_generation(
                prompt,
                max_new_tokens=420,
                temperature=0.2,
                return_full_text=False,
            )
            answer = generated.strip() if isinstance(generated, str) else str(generated)
            if not answer:
                return self._fallback_answer(question, matches), "fallback_empty"
            return answer, "hf_text_generation"
        except Exception:
            return self._fallback_answer(question, matches), "fallback_error"

    def _fallback_answer(self, question: str, matches: list[DocumentMatch]) -> str:
        if not matches:
            return (
                "I could not find enough grounded evidence in the current corpus to answer this "
                "question reliably.\n\n"
                "Citations: none"
            )

        bullets = "\n".join(
            f"- {m.title} ({m.arxiv_id})" for m in matches[:5]
        )
        return (
            "Fallback mode (LLM unavailable): here are the most relevant matched documents "
            f"for your question '{question}'.\n\n"
            f"{bullets}\n\n"
            "Use these citations as grounded references for manual review.\n\n"
            "Citations: "
            + ", ".join(m.arxiv_id for m in matches[:5])
        )
