# MVP Blueprint — Accountant AI Coworker (Uzbekistan SME)

Status: draft · Owner: CKO · Last update: 2026-07-06 · Target: MVP in 1–2 months

## 1. One-line definition
An AI coworker for Uzbek SME accountants/office managers that answers **tax
deadline** questions and **generates common accounting documents**, with every
answer sourced and dated. Not a chatbot, not tax advice — a grounded assistant.

## 2. MVP scope (locked)
- **Role:** Accountant
- **First task:** Tax calendar (deadlines Q&A) **+** documents (generation)
- **Interface:** web (built LAST; core logic + knowledge first)
- **Explicitly out of scope for MVP:** own foundation model, full 13-category
  Company Brain, all roles, live tax-rate advice, filing on the user's behalf.

## 3. Why this scope
- Highest willingness to pay (tax/compliance pain).
- Deadlines + document generation are the most **stable** and **demonstrable**
  accountant tasks (tax *rates* are volatile in 2026 → deferred).

## 4. Architecture (MVP)
```
User (web, later)  ──►  API (apps/api, FastAPI)  ──►  Claude API (LLM engine)
                                │
                                ▼
                        RAG retrieval over Knowledge Base
                        (knowledge-assets/, faq/, templates/ …)
                                │
                                ▼
                        Postgres + pgvector (embeddings)  ·  MinIO (files)
```
- **LLM:** Claude API (do NOT train a model). Model = engine; our KB = knowledge.
- **RAG:** embed KB markdown → retrieve top-k → answer strictly from retrieved
  context + cite `source_url` and `valid_from`.
- **Infra:** already scaffolded (apps/api, Postgres, Redis, MinIO in docker-compose).

## 5. Sourcing policy (critical for accountant domain)
Priority: lex.uz / soliq.uz (official) > buxgalter.uz (authoritative secondary)
> spot.uz / gazeta.uz / azma.uz (news/expert).
- Every tax asset carries `source_url`, `source_verified`, `valid_from`,
  `review_cycle: monthly`.
- **lex.uz is blocked in the current build environment** → legal citations must
  be re-verified on lex.uz before production release.
- Conflicting sources are shown openly (see ACC-KA-001 threshold note), never hidden.

## 6. Safety guardrails (non-negotiable)
1. Answer only from retrieved KB context — no free-form tax opinions.
2. If the KB lacks a confident, in-date answer → say so and recommend confirming
   with soliq.uz / the user's accountant.
3. Every answer shows source + "verified as of" date.
4. Stale asset (past `review_cycle`) → flagged for review, downranked.

## 7. Knowledge assets built so far
- `knowledge-assets/ACC-KA-001` — recurring tax reporting/payment calendar
- `faq/ACC-FAQ-001` — tax deadline FAQ
- (planned) `templates/ACC-TPL-001` — schyot-faktura (VAT invoice) — needs form sourcing
- (planned) `templates/ACC-TPL-002` — bajarilgan ishlar dalolatnomasi (act)
- (planned) `workflow-assets/ACC-SOP-001` — monthly closing / reporting workflow

## 8. Milestones
| Wk | Goal |
|----|------|
| 1 | Validate with 3–5 real accountants/SMEs. Lock the 10–15 assets MVP actually needs. |
| 2–3 | RAG API endpoint over KB (Q&A + document generation) in apps/api. |
| 3–4 | Build the ~15 sourced accountant assets (deadlines + core documents). |
| 5–6 | Pilot with 3–5 businesses; collect feedback; fix accuracy. |
| 7–8 | Minimal web UI; polish; prepare to charge. |

## 9. Success criteria (MVP)
- ≥ 3 real SMEs use it weekly.
- ≥ 90% of deadline answers correct & sourced (spot-checked vs soliq.uz).
- At least 2 document types generated in correct Uzbek format.
- One willing-to-pay signal.

## 10. Open decisions
- Language of the product UI/answers: uz / ru / both? (assets currently uz+en).
- Which document forms first: schyot-faktura vs akt vs shartnoma.
- Web now or Telegram bot as faster pilot channel?
