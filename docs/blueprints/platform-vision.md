# CoWorker AI — Platform Vision & Staged Roadmap

Status: draft · Owner: CKO · Target: a Coworker.ai-class AI coworker for
Uzbekistan SMEs, built in stages from the current working MVP core.

## 1. The target (reference: Coworker.ai)
A multi-model AI coworker platform where a business connects its data sources
and AI agents perform real work — answer questions, generate documents/decks/
sheets, run on schedules/triggers, take meeting notes — grounded in company
knowledge. Observed capabilities:

- **Multi-model routing** (Claude / GPT / Gemini / Kimi) with per-token credits.
- **Company data sources / Company Context** (Drive, Slack, Jira, Notion,
  HubSpot, BigQuery, Gmail, Calendar…).
- **Agent builder**: name, description, triggers (mention / schedule),
  skills (reusable instruction modules), credit limits, data-source scoping,
  on-complete actions.
- **Multi-step task engine**: plans a task list, uses skills, runs Python,
  produces artifacts (sheets, decks, docs) and renders them.
- **Meeting Notetaker**, **artifact gallery** (Slides/Docs/PDFs/Sheets/
  Dashboards/Apps/Websites).

This maps almost 1:1 to the RFC pack (0001–0007). The vision is coherent.

## 2. Honest reality check (read this first)
- Scale: a competitive clone is **10–50 engineer-years**. Coworker.ai is a
  funded, multi-year team.
- **Even mature platforms don't train their own model** — they route to
  Claude/GPT/Gemini/Kimi (see the model picker). Do NOT build a foundation
  model. Route. This is settled.
- The #1 risk is unchanged: **zero validated paying users.** A bigger scope
  does not reduce this risk — it increases burn before proof.
- Rule: **users before cathedral.** Every phase below must ship something a
  real Uzbek SME uses, or it doesn't get built yet.

## 3. Differentiation — localize, don't imitate
Our edge is not matching 20 US integrations. It is fitting the Uzbek SME stack:

| Coworker.ai (US) | CoWorker AI (Uzbekistan) |
|------------------|--------------------------|
| Slack / Jira / Notion | **Telegram** (primary channel) |
| QuickBooks / Xero | **1C, Didox, my.soliq.uz** |
| Gmail / Drive | Google + **Excel** |
| HubSpot | Local CRM / Telegram commerce |
| English-first | **Uzbek / Russian first**, sourced to lex.uz/soliq.uz |

Grounded, sourced, bilingual answers with local compliance = the moat.

## 4. Staged roadmap (each phase ships to real users)

**Phase 0 — Core (DONE).** Knowledge base (RFC-0002/0003), RAG API (/ask,
/generate, /workflows), web UI, quality automation (eval, stale, validators).

**Phase 1 — First usable product (weeks, MVP validation).**
- Live LLM (route to Claude/GPT via API key).
- Telegram bot channel (fastest reach for Uzbek SMEs) + the web UI.
- 30–50 sourced accountant assets.
- 3–5 real businesses using it weekly. **Gate: willingness to pay.**

**Phase 2 — Product depth (post-validation).**
- Multi-model routing (Claude/GPT/Gemini) with a credit/usage meter.
- Artifact generation: real .xlsx / .docx export (invoices, acts, reports).
- Company Context v1: upload company docs → private per-tenant knowledge.
- Auth, tenancy, billing.

**Phase 3 — Agents & automation (RFC-0003 engine, 0004).**
- Workflow/Task engine executes the structured workflows we already author.
- Triggers: schedule + Telegram mention. Skills = reusable instruction modules.
- First integrations: my.soliq.uz calendar, Didox, Excel, Google.

**Phase 4 — Company Brain & DNA (RFC-0005, 0006, 0007).**
- Memory Engine (Company/Learning memory), Company DNA, runtime Knowledge Graph.
- Multi-tenant, embeddings/pgvector at scale, dashboards, notetaker.

## 5. Platform architecture (target)
```
Channels:   Telegram bot · Web (Next.js) · (later) API
                     │
Gateway/API (FastAPI): auth · tenancy · credit metering · routing
                     │
   ┌─────────────────┼───────────────────────────┐
Model Router      RAG / Retrieval            Agent/Task Engine
(Claude/GPT/…)   (pgvector + KB)           (workflows, skills, tools)
                     │                              │
             Company Context             Capabilities (Python, xlsx/docx,
             (per-tenant docs)            web search, doc render)
                     │
   Data: Postgres+pgvector · MinIO(files) · Redis(queue) · Memory Engine
                     │
   Integrations: my.soliq.uz · Didox · 1C · Google · Excel · Telegram
```

## 6. Resourcing reality (solo / small team)
- Solo or 2–3 people: do **not** attempt Phase 2+ breadth. Win Phase 1 in one
  vertical (accountant), one channel (Telegram), one city.
- Hire/expand only after paying users prove the wedge.
- Keep the RFC standards (0002/0003) so today's assets stay forward-compatible
  — that is how a small team builds toward a big platform without rework.

## 7. Immediate next actions (to actually start the "big project")
1. Plug in an LLM key → live grounded answers (turns the demo real).
2. Ship a **Telegram bot** over the existing API (fastest Uzbek reach).
3. Get 3–5 SMEs using it; measure willingness to pay.
4. Only then open Phase 2. The architecture above is the map; users set the pace.
