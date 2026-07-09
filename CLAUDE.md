# CoWorker AI — Agent Guide

O'zbekiston KO'B (SME) uchun AI hamkasb platformasi. RAG asosidagi, manbaga
tayangan (grounded) javoblar + hujjat generatsiyasi. Chatbot emas — "AI xodim".

## Repo xaritasi (bu yerga qarab ish qil, qidirma)
- `apps/api/` — FastAPI backend (Python). Yagona yuk ko'taruvchi kod shu.
  - `app/api/routes.py` — barcha endpointlar (`/ask` `/generate` `/tasks` `/documents` `/integrations/1c/*` `/models` `/me`).
  - `app/services/knowledge_base.py` — leksik retrieval (uz/ru stemming + sinonim). Embedding YO'Q (ataylab).
  - `app/services/llm.py` — provider routing: anthropic / openai / ollama. Kalit yo'q bo'lsa "retrieval-only" fallback.
  - `app/services/{documents,tasks,onec}.py` — tenant hujjatlari, RFC-0004 tasklar, 1C OData.
  - `app/core/{config.py,tenancy.py}` — sozlama + MODELS registry, X-API-Key tenancy.
  - `scripts/{validate_metadata,validate_workflows,eval_retrieval,check_stale}.py` — sifat nazorati.
- `apps/web/` — Next.js 14 App Router. `app/page.tsx` (Dashboard + Chat), `lib/api.ts`, `app/globals.css`.
- Bilim aktivlari (repo ildizida, markdown + YAML front-matter):
  `knowledge-assets/ faq/ workflow-assets/ templates/ checklists/ business-rules/ decision-trees/ glossary/`
- `docs/blueprints/` — strategiya + UX arxitektura hujjatlari (kod emas, reja).
- `scripts/deploy/setup-vps.sh` — bitta buyruqli VPS deploy (idempotent).
- `datasets/` — eval benchmark, knowledge-graph, training export.

## Ish qoidalari (MUHIM)
- Javob **doim o'zbekcha**. Mulozamat/izoh yo'q, faqat ish.
- Token tejash: keraksiz faylni qayta o'qima. Bu fayldagi xaritaga ishon.
- Yangi bilim aktivi = RFC-0002 front-matter majburiy; SOP = RFC-0003 `workflow:` bloki.
  Namuna sifatida shu turdagi mavjud faylni ko'chir.
- O'zgartirgach shu tekshiruvlarni ishga tushir:
  ```
  cd apps/api
  .venv/bin/python scripts/validate_metadata.py
  .venv/bin/python scripts/validate_workflows.py
  .venv/bin/python scripts/eval_retrieval.py 4      # recall@4 >= 90%
  .venv/bin/python scripts/check_stale.py
  ```
  Bilim bazasi o'zgarsa: `scripts/export_knowledge_graph.py` va `scripts/export_training_data.py` ni qayta ishga tushir.
- Web o'zgarsa: `cd apps/web && npx tsc --noEmit && npm run build`.
- Har javob manbali (source chip) bo'lishi shart. Grounding qoidasi buzilmasin —
  model faqat retrieval kontekstidan javob beradi, aks holda REFUSAL.

## Arxitektura qarorlari (qayta muhokama qilma)
- Embedding/pgvector — ataylab keyinga qoldirilgan. Leksik retrieval yetarli.
- Store'lar in-memory (Task/Tenant/Document) — MVP uchun. Postgres = keyingi bosqich.
- Lokal model: Ollama (OpenAI-mos `/v1`). Faqat VPS resursi yetsa (disk+RAM).
- 20 modulli platforma `docs/blueprints/ux-architecture.md` da — ko'pi hali P1-P3, qurilmagan.

## Git
- Branch: `claude/coworker-knowledge-base-nv7p9b`. Shu yerga commit + push.
- PR faqat so'ralganda.

## Deploy (VPS)
- Yangilash: `git pull && sudo bash scripts/deploy/setup-vps.sh`.
- Disk cheklovi: 7B model ~5GB. Kichik diskda (10GB) yuklama — disk to'ladi.
  Skript disk/RAM tekshiradi; yetmasa lokal modelni o'tkazib yuboradi.
