# Test Workspace

This folder contains all testing assets for TDD and BDD workflows.

Structure:

- `unit/`: unit-level suites for text processing, ingestion, retrieval, embeddings, evaluation.
- `e2e/`: executable API scenarios + BDD assets.
- `data/`: test corpora and evaluation datasets.
- `fixtures/`: reusable deterministic assets.

Run test commands:

- Backend + API e2e: `python -m pytest tests/unit/backend tests/e2e -q`
- Frontend unit tests: `cd frontend && npm run test`
