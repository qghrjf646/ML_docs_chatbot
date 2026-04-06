# Frontend

React + Vite frontend for the Graph RAG chatbot.

Current state:

- Functional chat request flow to backend.
- Matched document evidence rendering with source links.
- Evaluation dashboard tabs bound to API metrics.
- Ingestion trigger for arXiv corpus loading.

Network behavior:

- The app uses relative API URLs and Vite proxy by default.
- This prevents `localhost` browser resolution errors in remote environments (Codespaces/github.dev).
- Proxy target is configured through `VITE_BACKEND_PROXY_TARGET`.

Design direction:

- Light-blue technical visual identity.
- Modern, clean, and readable structure.
