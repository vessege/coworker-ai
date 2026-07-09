# CoWorker AI — API (RAG core)

Grounded Q&A over the CoWorker AI knowledge base. Answers come **only** from
retrieved KB assets, with sources cited; off-topic questions are refused.
See `docs/blueprints/mvp-accountant.md`.

## Run
```bash
cd apps/api
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# optional: enable the LLM (otherwise runs in retrieval-only mode)
export ANTHROPIC_API_KEY=sk-...          # LLM_MODEL default: claude-sonnet-5
uvicorn app.main:app --reload
```

## Endpoints (prefix `/api/v1`)
| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | status + number of assets loaded |
| GET | `/assets` | list loaded assets |
| POST | `/ask` | `{"question": "..."}` → grounded answer + sources |

## How it works
1. `KnowledgeBase` loads markdown assets from the repo KB dirs, parses
   front-matter, indexes tokens (title/tags weighted).
2. `search()` returns the top-k assets by lexical overlap (MVP; swap for
   pgvector embeddings later).
3. `LLMEngine` answers strictly from retrieved context and cites sources.
   Without `ANTHROPIC_API_KEY` it returns retrieved context (retrieval-only
   mode) so the pipeline is demonstrable offline.

## Guardrails
- No retrieved match → refusal ("verify with soliq.uz / your accountant").
- Answers cite asset id + `source_url` + verified date.
- Informational only, not official tax advice.

## Next
- Embeddings + pgvector retrieval · `/generate` for document templates ·
  auth · web UI.
