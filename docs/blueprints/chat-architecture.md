# CoWorker AI — Chat Architecture (Phase 1, Module Deep-Dive)

Status: draft · Owner: Chief Product Designer · Scope: Chat module only (no UI)
Parent: docs/blueprints/ux-architecture.md §1.2 Module 4 (P0, live)
Legend: **P0** live · **P1** MVP+ · **P2** post-validation · **P3** platform phase

---

## 1. Chat Purpose

Chat is the primary work surface of CoWorker AI — the place where a human and an
AI coworker actually do the work, not a settings screen or a report. Every other
module (Dashboard, Tasks, Documents, Calendar) exists to **route the user into
Chat** or to **record what happened in Chat**. It is the only module today with a
real, load-bearing backend (`POST /ask`, `POST /generate`) and it is the module
every Task Asset traces back to.

It is not a general-purpose chatbot. It is a **grounded conversation with a named
AI coworker**, scoped to a role, backed by retrieval, and incapable of answering
outside what the Company Brain actually contains.

### 1.1 Primary User Goals
- Get a trustworthy, sourced answer to a work question in one exchange.
- Generate a ready-to-use document (invoice, order, memo) without leaving chat.
- Know *why* the AI said what it said — see the source, not just the claim.
- Talk to the right specialist (Aziza for tax, Malika for HR) without hunting for a menu.
- Resume a conversation instead of restarting context every time (P1 — not live yet).

### 1.2 Success Metrics
- **Grounded-answer rate**: % of answers backed by ≥1 source chip vs. refusal/fallback.
- **Refusal correctness**: refusals only fire on genuinely out-of-scope questions (tracked via eval set, not vibes).
- **Time-to-answer**: question submit → rendered response.
- **Document-generation completion rate**: Hujjat-mode requests that produce a usable draft vs. NO_TEMPLATE fallback.
- **Task-creation rate**: % of chat exchanges that convert into a Task Asset (today: 100%, every /ask and /generate auto-logs — this metric becomes interesting once *manual* task creation from chat exists in P1).
- **Return-to-coworker rate**: % of users who message the same coworker again within 7 days (loyalty to a specific AI teammate, not just the product).

### 1.3 Daily Workflow (target)
```
Pick a coworker (or arrive via deep link from Dashboard/Task/Calendar)
   → Ask a question (Savol mode) or request a document (Hujjat mode)
   → Retrieval runs against Knowledge Base + tenant Documents (role-boosted)
   → Model answers, grounded in retrieved sources; source chips rendered
   → Task Asset auto-logged (Learning Rule, RFC-0004)
   → User acts: copies doc, asks follow-up, opens source, or leaves
   → (P1) Convert exchange into a tracked Task with one click
```
The loop is: **ask → ground → answer → trace**. Every answer must survive the
question "prove it" — that proof is the source chip.

---

## 2. Chat Sections

Ordered by vertical position in the conversation surface. Each is independently
addressable (§4).

### 2.1 Coworker Picker (current home)
- **Purpose:** entry point into Chat; the roster *is* the product's identity, so this doubles as a light "AI Coworkers" module view.
- **Displayed information:** coworker cards — avatar/emoji, name, role title, one-line description, 2–3 example questions per coworker.
- **Actions:** click card → opens Conversation with that coworker; click example chip → opens Conversation and pre-fills the question.
- **AI features:** none (static roster today); usage-based reordering (P2).
- **Priority:** P0 (live) — this is the app's current home screen.
- **Visibility:** all roles; roster filtered to workspace-enabled coworkers (P2 — today all 4 always shown).
- **Future expansion:** "General" coworker becomes a real router that recommends a specialist (P2); custom coworkers appear here once built (P3, ties to AI Coworkers module).

### 2.2 Conversation Header
- **Purpose:** orient the user inside a thread — who they're talking to and how to leave.
- **Displayed information:** coworker avatar + name + role title, back-to-picker control.
- **Actions:** back to picker (P0); (P1) rename thread, view thread info, switch coworker mid-context.
- **AI features:** none.
- **Priority:** P0 (live).
- **Visibility:** all roles.
- **Future expansion:** presence/typing state for multi-user shared threads (P3).

### 2.3 Message Thread
- **Purpose:** the conversation itself — the core value surface of the entire product.
- **Displayed information:** alternating user/AI bubbles; AI bubbles carry source chips and a grounded/fallback indicator; typing indicator while awaiting response.
- **Actions:** click a source chip → view source asset/document (P1 — today chips are informational only, not yet clickable through to a detail view); (P1) copy message, regenerate, follow-up quoting a prior message.
- **AI features:** this section *is* the AI output — grounded Q&A and document drafting, with an explicit refusal path (`REFUSAL`/`NO_TEMPLATE` constants) when retrieval finds nothing usable, rather than a hallucinated answer.
- **Priority:** P0 (live) — persistent, single-page thread (this exact behavior was a direct fix for a UX complaint: "har savolga boshqa pagega o'tyapti chat bo'lmayapti").
- **Visibility:** all roles; content scoped by whatever role-boosted retrieval surfaces.
- **Future expansion:** message-level actions (turn into Task, pin, share); inline document preview instead of raw markdown (P2).

### 2.4 Source Chips
- **Purpose:** the trust mechanism — every grounded claim must point at where it came from.
- **Displayed information:** compact chip per retrieved asset/document: id, title, small relevance/type indicator.
- **Actions:** (P1) click → opens asset detail (Knowledge module) or document detail (Documents module) in a side panel, without leaving the thread.
- **AI features:** chips are a direct rendering of the `/ask` and `/generate` response's `sources` array (live, real retrieval hits — not decorative).
- **Priority:** P0 (live).
- **Visibility:** all roles; a message with zero sources is visibly marked "ungrounded/retrieval-only" rather than presented as equally authoritative.
- **Future expansion:** confidence score display; "sources used vs. sources considered" toggle for power users (P2).

### 2.5 Mode Toggle (Savol / Hujjat)
- **Purpose:** disambiguate intent up front — answering a question and drafting a document need different prompting and different downstream handling.
- **Displayed information:** two-state toggle in the composer bar; current mode affects placeholder text and endpoint routed to.
- **Actions:** switch between Savol (`POST /ask`) and Hujjat (`POST /generate`).
- **AI features:** routes to different system prompts (`SYSTEM_PROMPT` vs `GENERATE_SYSTEM`) and different guardrail fallbacks (`REFUSAL` vs `NO_TEMPLATE`).
- **Priority:** P0 (live).
- **Visibility:** all roles; Hujjat mode's available templates are role-scoped (e.g. Create Invoice quick action pre-fills ACC-TPL-001 for Accountant).
- **Future expansion:** auto-detect intent and suggest the mode switch instead of requiring manual toggle (P2).

### 2.6 Model Selector
- **Purpose:** let the user (or workspace policy) choose the LLM handling the request — cost/quality tradeoff exposed, not hidden.
- **Displayed information:** dropdown of models from `GET /models` (MODELS registry: claude-sonnet-5, claude-opus-4-8, claude-haiku-4-5, gpt-5.5, gpt-5), each with a label.
- **Actions:** select model → subsequent messages in this composer use it; falls back to `DEFAULT_MODEL` if unset.
- **AI features:** direct routing control via `LLMEngine._resolve`.
- **Priority:** P0 (live).
- **Visibility:** all roles today (P2: restrict expensive models to Admin/Owner-approved plans, tied to Billing).
- **Future expansion:** per-workspace default model policy (P2); automatic model selection by task complexity (P3).

### 2.7 Example Chips (starter prompts)
- **Purpose:** cold-start help — show, don't tell, what this coworker is good for.
- **Displayed information:** 2–3 example questions per coworker, shown on entering an empty conversation.
- **Actions:** click → fills composer and can auto-send.
- **AI features:** none (static per-coworker list today); could be generated from real usage/eval data (P2).
- **Priority:** P0 (live).
- **Visibility:** all roles; disappears once the thread has messages.
- **Future expansion:** personalized examples based on role + recent Tasks (P2).

### 2.8 Composer Bar
- **Purpose:** the single, sticky input surface — always reachable, never requires scrolling to find.
- **Displayed information:** textarea, mode toggle (§2.5), model selector (§2.6), send control.
- **Actions:** type + Enter to send (Shift+Enter for newline — P1 if not already); (P1) attach file directly into the message (today, attaching happens via the separate Documents upload flow, not inline).
- **AI features:** none itself — it's the trigger for §2.3/§2.4.
- **Priority:** P0 (live).
- **Visibility:** all roles.
- **Future expansion:** slash-commands (`/invoice`, `/summarize`) as a fast path into Hujjat mode with a specific template (P2).

### 2.9 Conversation History [P1]
- **Purpose:** resume any past thread instead of losing it on refresh — the single biggest gap between today's Chat and a "real" product.
- **Displayed information:** list of past conversations per coworker: preview of last message, timestamp.
- **Actions:** click → reopens thread with full message history.
- **AI features:** none required; unlocks Dashboard's Recent Conversations widget becoming fully live.
- **Priority:** P1 — currently threads are in-memory/client-side only and do not survive navigation away from the picker in a durable way; this is the top of the Chat backlog.
- **Visibility:** personal, all roles.
- **Future expansion:** cross-device resume, shared/team threads (P3).

### 2.10 Turn Into Task [P1]
- **Purpose:** make the existing auto-logging *actionable* — every exchange already becomes a Task Asset server-side (Learning Rule), but there is no UI to act on that from within the thread yet.
- **Displayed information:** inline action on a message ("Task qilib belgilash").
- **Actions:** promotes the auto-logged Completed task into a Running/tracked one, or creates a new linked task (e.g. "follow up on this invoice").
- **AI features:** none new — surfaces the existing `TaskStore` write.
- **Priority:** P1.
- **Visibility:** all roles.
- **Future expansion:** auto-suggest task creation when a message implies a deliverable (P2).

### 2.11 Attach Document [P2]
- **Purpose:** ground a question in a specific just-uploaded file without a separate trip to Documents.
- **Displayed information:** attach control in composer; attached file shown as a small chip above the input.
- **Actions:** upload inline → indexed into tenant `DocumentStore` → included in retrieval for this message onward.
- **AI features:** reuses the existing reserved-slot retrieval logic (tenant documents already get priority slots ahead of generic KB results).
- **Priority:** P2.
- **Visibility:** all roles (upload permission-gated).
- **Future expansion:** OCR/structured extraction on attach (ties to 1C/Documents modules).

---

## 3. Chat Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER  (persistent)                                              │
│  ← back to picker · coworker avatar + name + role · (P1) rename   │
├─────────────────────────────────────────────────────────────────┤
│ MESSAGE THREAD (scrollable, grows downward)                       │
│                                                                     │
│   [empty state]  Example chips (2-3 starter questions)            │
│                                                                     │
│   user bubble  ─────────────────────────────────►                 │
│                          ◄───────────────  AI bubble               │
│                                             + source chips          │
│                                             + grounded/fallback tag │
│   ...                                                               │
│                                             typing indicator        │
│                                             (while awaiting reply)  │
├─────────────────────────────────────────────────────────────────┤
│ COMPOSER BAR  (sticky, always visible, never scrolls away)        │
│  [Savol|Hujjat toggle]  [textarea..............]  [model ▾] [Send] │
└─────────────────────────────────────────────────────────────────┘
```

**Rationale for single-thread + sticky composer:** this was a direct correction of
early feedback — per-question page navigation broke the sense of an ongoing
conversation with a coworker. A persistent thread with a fixed composer is the
minimum bar for "this feels like messaging a colleague," which is the entire
product thesis (AI Coworker, not AI chatbot).

**Responsive collapse:** header shrinks to icon-only back control; composer mode
toggle and model selector collapse into a single overflow menu on narrow
viewports; message bubbles go full-width.

---

## 4. Component Architecture

Common contract for every component below:
- **Loading state:** typing indicator (three-dot), never a blank gap.
- **Empty state:** example chips, never a bare empty thread.
- **Grounding state:** every AI bubble is visibly tagged grounded (has sources) or fallback/refusal (does not) — never presented identically.

| Component | Purpose | Data source | API | Refresh | Empty state | AI integration |
|---|---|---|---|---|---|---|
| Coworker Picker | entry roster | static config (`COWORKERS`) | n/a (P1: `GET /coworkers`) | on load | n/a (always populated) | none |
| Conversation Header | orientation | selected coworker state | n/a | on coworker switch | n/a | none |
| Message Thread | conversation record | client-side message array (P1: `GET /conversations/{id}`) | `POST /ask`, `POST /generate` | on each send | example chips shown | grounded Q&A / document drafting |
| Source Chips | trust/provenance | `AskResponse.sources` / `GenerateResponse.sources` | (embedded in ask/generate response) | per message | hidden if no sources; message tagged fallback instead | direct retrieval-hit rendering |
| Mode Toggle | intent routing | client UI state | routes to `/ask` or `/generate` | on toggle | n/a | selects system prompt/guardrail |
| Model Selector | LLM choice | `GET /models` | `GET /models` | on load | falls back to `DEFAULT_MODEL` | routes `LLMEngine._resolve` |
| Example Chips | cold-start guidance | static per-coworker list | n/a | on entering empty thread | n/a (this *is* the empty state) | none |
| Composer Bar | input | client UI state | triggers `/ask` or `/generate` | n/a | n/a | none |
| Conversation History [P1] | thread resume | Conversation store [P1] | `GET /conversations` [P1] | on load | "Suhbat tarixi yo'q" | none |
| Turn Into Task [P1] | task promotion | existing Task log | `PATCH /tasks/{id}/status` (existing) | on click | n/a | surfaces Learning Rule output |
| Attach Document [P2] | inline grounding | tenant DocumentStore | `POST /documents` (existing) | on upload | n/a | reserved-slot retrieval (existing logic) |

---

## 5. AI Features (Chat-specific)

| Feature | Description | Trigger | Phase |
|---|---|---|---|
| Grounded Q&A | retrieval-augmented answer over Knowledge Base + tenant Documents, role-boosted | every `/ask` | P0 (live) |
| Document Generation | drafts a document from instruction + retrieved template/reference assets | every `/generate` | P0 (live) |
| Refusal Guardrail | returns explicit `REFUSAL`/`NO_TEMPLATE` instead of an ungrounded answer when retrieval finds nothing usable | no sufficient sources found | P0 (live) |
| Role-Boosted Retrieval | +2.0 score boost for assets matching the active coworker's role | every `/ask`/`/generate` with a role param | P0 (live) |
| Reserved Document Slots | guarantees tenant-uploaded documents aren't crowded out by generic KB assets | every retrieval call with tenant documents present | P0 (live) |
| Auto Task Logging (Learning Rule) | every exchange becomes a Completed Task Asset linked to its sources | every `/ask`/`/generate` | P0 (live) |
| Multi-Model Routing | dispatches to Anthropic/OpenAI per selected model, with retrieval-only fallback when no provider key configured | every request | P0 (live) |
| Follow-up Context | model considers prior turns in the same thread, not just the latest message | multi-turn | P1 (today: single-turn; conversation history not yet threaded into the prompt) |
| Suggested Follow-ups | proposes 2-3 next questions after an answer | after each AI bubble | P2 |
| Auto Task Suggestion | detects when a message implies unfinished work and offers to create a Task | message analysis | P2 |

All Chat AI output follows the platform-wide grounding rule established here
first and reused everywhere else (Dashboard AI Suggestions, Risk Detection):
**no ungrounded claims** — every answer is either sourced or explicitly marked
as not sourced. This rule originates in Chat and is inherited by every other
module that generates AI text.

---

## 6. Personalization

| Capability | Behavior | Phase |
|---|---|---|
| Pin a coworker | keeps a coworker at the top of the picker / Dashboard Favorite Coworkers | P2 |
| Default model preference | remembers last-selected model per user, applied on next visit | P1 |
| Default mode preference | remembers Savol/Hujjat last used per coworker | P2 |
| Thread density | compact vs. comfortable bubble spacing | P3 |
| Language preference | uz/ru response language override (content is already bilingual-sourced) | P2 |

Personalization affects presentation and defaults only — grounding, permissions,
and retrieval scope are always server-enforced, never client-configurable.

---

*Chat Blueprint complete. Awaiting approval before proceeding to the next module deep-dive.*
