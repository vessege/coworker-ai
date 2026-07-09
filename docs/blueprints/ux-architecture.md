# CoWorker AI — Product UX Architecture (Phase 1)

Status: draft · Owner: Chief Product Designer · Scope: product structure only (no UI)
Approval gates: §1 Structure & Modules → §2 Navigation → §3 App Flow → §4 Page Inventory

Legend for build phase: **P0** = live today · **P1** = MVP+ (next) · **P2** = post-validation · **P3** = platform phase

---

## §1.0 Structural Hierarchy

```
APPLICATION  (CoWorker AI — one web app)
   ↓
WORKSPACE    (= one company/tenant; users join with a role; all data scoped here)
   ↓
MODULES      (20 functional areas, below)
   ↓
PAGES        (each module owns child pages; inventory in §4)
   ↓
COMPONENTS   (shared: coworker card, chat thread, source chip, asset card,
              task row, doc preview, credit meter, command palette)
   ↓
USER FLOWS   (task-first: every flow ends in a completed Task Asset — RFC-0004)
   ↓
PERMISSIONS  (role × module matrix, §1.3; page-level in §4)
```

**Architecture principles applied**
- **AI-first:** every module exposes a contextual "Ask coworker" action; AI output is always grounded + source-cited.
- **Task-first:** any AI interaction or human action can become a Task (RFC-0004 Learning Rule already logs every /ask & /generate).
- **Chat is a surface, not the product:** conversations spawn Tasks, Documents, Calendar entries.
- **Workspace isolation:** tenancy already enforced at API level (X-API-Key → tenant).

---

## §1.1 Workspace Layer

| Aspect | Decision |
|--------|----------|
| Definition | 1 workspace = 1 company (MChJ/YaTT). A user may belong to several workspaces (accounting firms!). |
| Onboarding | Owner registers → company profile (name, STIR, regime, industry) → invites members → picks active coworkers. Company profile feeds AI context. |
| Data scoping | Knowledge (shared platform KB) + Company Context (private: documents, 1C data, tasks, chats, memory). |
| Switcher | Top-left workspace switcher (multi-company accountants are a core persona). |

---

## §1.2 Module Architecture (20 modules)

### 1. Authentication — P1
- **Purpose:** secure entry; invite-based membership.
- **Target user:** all, incl. Guest.
- **Features:** email+password login, registration, invitation accept, password reset, session mgmt; (P3: SSO, 2FA).
- **Child pages:** Login · Register · Invite Accept · Forgot Password · Workspace Select.
- **Navigation:** pre-app surface; redirects to last workspace → Dashboard.
- **Dependencies:** Workspace.
- **API:** /auth/register /auth/login /auth/invite /auth/reset. *(Today: static X-API-Key — to be replaced.)*
- **DB entities:** User, Session, Invitation.
- **AI:** none.

### 2. Workspace — P1
- **Purpose:** company identity & membership management.
- **Target:** Owner, Administrator.
- **Features:** company profile (STIR, tax regime, industry — feeds AI), member list, role assignment, workspace creation/switch.
- **Child pages:** Company Profile · Members · Create Workspace.
- **Navigation:** avatar menu + switcher.
- **Dependencies:** Authentication.
- **API:** /workspaces, /workspaces/{id}/members.
- **DB:** Workspace, Membership(role), CompanyProfile.
- **AI:** onboarding assistant ("tell me about your business" → fills profile, suggests coworkers).

### 3. Dashboard — P1
- **Purpose:** "My Day" — what needs attention now (task-first, not analytics-first).
- **Target:** all roles.
- **Features:** upcoming deadlines (tax calendar!), my open tasks, recent conversations, notification digest, quick actions (ask/draft/upload), AI daily briefing.
- **Child pages:** Home (single).
- **Navigation:** default landing after login.
- **Dependencies:** Tasks, Calendar, Chat, Notifications.
- **API:** /dashboard (aggregator over /tasks /calendar /conversations).
- **DB:** none new (aggregation).
- **AI:** daily briefing generation ("bugun: QQS topshirishga 3 kun qoldi; 2 task muddati yaqin").

### 4. Chat — P0 (live)
- **Purpose:** conversation surface with a selected coworker; grounded answers + document generation.
- **Target:** all roles.
- **Features (live):** per-coworker thread, Savol/Hujjat modes, source chips, model picker, role-boosted retrieval. **(P1):** persistent history, multi-turn context, spawn Task/Document from a message. **(P2):** attach file to chat.
- **Child pages:** Coworker Picker (current home) · Conversation · History list (P1).
- **Navigation:** sidebar item + "New chat" quick action; deep-linked from every module.
- **Dependencies:** AI Coworkers, Knowledge, Documents.
- **API (live):** POST /ask · POST /generate · GET /models. **(P1):** /conversations CRUD.
- **DB:** Conversation, Message (today: in-memory task log only).
- **AI:** grounded Q&A, document drafting, refusal guardrails (live).

### 5. AI Coworkers — P0 partial
- **Purpose:** the roster of AI employees; the product's identity.
- **Target:** all (use); Owner/Admin (configure).
- **Features (live):** 4 coworkers (Aziza-Accountant, Malika-HR, Jasur-Office-Manager, General). **(P2):** coworker profile (knowledge scope, model, tone), enable/disable per workspace. **(P3):** custom coworker builder — triggers (schedule/mention), skills, credit limit, data-source scoping (Coworker.ai-style agent builder; executes RFC-0003 workflows).
- **Child pages:** Roster · Coworker Profile · (P3) Coworker Builder.
- **Navigation:** sidebar "Team"; picking one opens Chat.
- **Dependencies:** Chat, Knowledge, Tasks, Integrations.
- **API:** GET /coworkers (P1; today hardcoded in web) · (P3) /coworkers CRUD, /triggers.
- **DB:** Coworker, CoworkerConfig, Trigger(P3).
- **AI:** role-scoped retrieval boost (live); autonomous scheduled runs (P3).

### 6. Company Brain — P2
- **Purpose:** umbrella view of "what the AI knows about OUR company": stats, coverage, memory, DNA readiness.
- **Target:** Owner, Manager.
- **Features:** knowledge coverage per domain, uploaded-context inventory, memory items (P3, RFC-0005), Company DNA traits (P4, RFC-0006), gaps report (unanswered questions).
- **Child pages:** Overview · Memory (P3) · Company DNA (P4).
- **Navigation:** sidebar section header grouping Knowledge/Documents/Factory.
- **Dependencies:** Knowledge, Documents, Analytics.
- **API:** /brain/overview (aggregator).
- **DB:** MemoryItem(P3), DnaTrait(P4).
- **AI:** gap detection from grounded=false answers.

### 7. Knowledge — P0 API / P1 UI
- **Purpose:** browse the curated knowledge base (30 assets, RFC-0002).
- **Target:** all (read); Admin (manage via Factory).
- **Features:** asset list w/ filters (role/type/domain), asset detail (source, verified date, version, relationships), "ask about this asset".
- **Child pages:** Asset Library · Asset Detail.
- **Navigation:** sidebar; also reached from source chips in Chat.
- **Dependencies:** Knowledge Factory (authoring), Search.
- **API (live):** GET /assets · GET /workflows.
- **DB:** KnowledgeAsset (today markdown files — P2 moves index to DB).
- **AI:** related-asset suggestions (knowledge-graph edges exist).

### 8. Documents — P0 API / P1 UI
- **Purpose:** Company Context — private uploads + generated documents archive.
- **Target:** all roles (upload scoped by permission).
- **Features (live API):** upload text/md, list, retrieval into /ask. **(P1 UI):** upload page, doc list, preview, delete; generated-docs archive with re-download. **(P2):** PDF/DOCX parsing, .docx/.xlsx export.
- **Child pages:** Library · Upload · Document View · Generated Archive.
- **Navigation:** sidebar; attach action inside Chat.
- **Dependencies:** Chat (grounding), Integrations (1C sync writes here).
- **API (live):** POST/GET /documents.
- **DB:** Document, GeneratedDocument.
- **AI:** extraction Q&A over own docs (live, retrieval); summarization (P1 w/ LLM key).

### 9. Tasks — P0 API / P1 UI
- **Purpose:** executable work units (RFC-0004); audit trail of all AI work.
- **Target:** all roles.
- **Features (live API):** create, list, state machine, priorities, auto-log of every AI interaction. **(P1 UI):** board by status, task detail, assign to coworker/human. **(P3):** AI executes task via workflow engine.
- **Child pages:** Board · Task Detail · AI Work Log.
- **Navigation:** sidebar; "create task" from any chat message.
- **Dependencies:** Chat, AI Coworkers, Projects.
- **API (live):** /tasks CRUD + /tasks/{id}/status.
- **DB:** Task (today in-memory → P1 Postgres).
- **AI:** auto-logging (live); planning & execution (P3).

### 10. Projects — P3
- **Purpose:** group tasks toward business outcomes.
- **Target:** Manager, Owner.
- **Features:** project list, task grouping, progress, AI status summary.
- **Child pages:** Projects · Project Detail.
- **Dependencies:** Tasks.
- **API:** /projects. **DB:** Project. **AI:** progress narration, risk flags.

### 11. Meetings — P3
- **Purpose:** meeting notes → knowledge & tasks.
- **Target:** all.
- **Features:** upload/record minutes, AI summary, action items → Tasks, decisions → Company Memory.
- **Child pages:** Meetings List · Meeting Detail.
- **Dependencies:** Tasks, Company Brain, Calendar.
- **API:** /meetings. **DB:** Meeting, ActionItem. **AI:** summarization, action extraction.

### 12. Calendar — P1 ⭐ (local killer feature)
- **Purpose:** one calendar of business obligations: tax deadlines (from KB!), task due dates, meetings.
- **Target:** all; Accountant primary.
- **Features:** month/list view, tax-deadline auto-population per company regime (ACC-KA-001), reminders → Notifications, "why this deadline?" → asset link.
- **Child pages:** Calendar · Deadline Detail.
- **Dependencies:** Knowledge (deadline assets), Notifications, Tasks.
- **API:** /calendar (generator from KB + tasks).
- **DB:** CalendarItem, ReminderRule.
- **AI:** deadline sentinel ("QQSga 3 kun qoldi — jarima: ACC-KA-004").

### 13. Notifications — P1
- **Purpose:** timely pull→push of what matters.
- **Target:** all.
- **Features:** in-app center, unread badge, deadline/task/mention events; (P2) email digest.
- **Child pages:** Notification Center (panel, not page).
- **Dependencies:** Calendar, Tasks, Admin.
- **API:** /notifications. **DB:** Notification, NotificationPref.
- **AI:** digest summarization.

### 14. Search — P2
- **Purpose:** one search across assets, documents, tasks, chats.
- **Target:** all.
- **Features:** global search bar + command palette (⌘K) with actions ("yangi task", "Azizaga yoz"); scoped filters.
- **Child pages:** Search Results (overlay-first).
- **Dependencies:** all content modules; embeddings (P2 pgvector).
- **API:** /search. **DB:** SearchIndex (pgvector).
- **AI:** semantic ranking; answer-style preview.

### 15. Admin — P2
- **Purpose:** workspace governance.
- **Target:** Owner, Administrator.
- **Features:** member/role management (deep), usage overview, audit log (task log is the substrate — live), data export/delete.
- **Child pages:** Users · Audit Log · Data Controls.
- **Dependencies:** Workspace, Tasks, Billing.
- **API:** /admin/*. **DB:** AuditEvent.
- **AI:** anomaly notes on usage.

### 16. Settings — P1
- **Purpose:** personal + workspace preferences.
- **Target:** all (personal); Admin (workspace).
- **Features:** profile, language (uz/ru), theme, default model, notification prefs; workspace: model keys, default coworkers.
- **Child pages:** Profile · Preferences · Workspace Settings · Model & Keys.
- **API:** /settings. **DB:** UserPref, WorkspaceSetting.
- **AI:** none.

### 17. Billing — P2
- **Purpose:** plan & credits.
- **Target:** Owner.
- **Features:** current plan, credit usage meter (tenant.used — live at API), invoices, upgrade; local payments (Payme/Click) P2.
- **Child pages:** Plan · Usage · Invoices.
- **Dependencies:** Admin.
- **API (partial live):** GET /me (credits) · /billing/*. **DB:** Plan, UsageRecord, Invoice.
- **AI:** usage forecast.

### 18. Knowledge Factory — P0 scripts / P2 UI
- **Purpose:** content-ops pipeline: author → review → approve assets; quality gates. (RFC-0001/0002 operationalized.)
- **Target:** Administrator / CKO role.
- **Features (live as scripts/CI):** RFC-0002/0003 validators, stale-review queue (check_stale), retrieval eval (45 golden cases), knowledge-graph export, **training-data export (144 instruct pairs)**. **(P2 UI):** review queue, asset editor, publish workflow, eval dashboard.
- **Child pages:** Review Queue · Asset Editor · Quality Dashboard · Training Exports.
- **Dependencies:** Knowledge, Analytics.
- **API:** /factory/* (P2). **DB:** AssetRevision, ReviewTask.
- **AI:** draft-asset generation from sources; stale-diff suggestions.

### 19. Analytics — P2
- **Purpose:** learn from usage; feed the Knowledge Factory and the future own-model dataset.
- **Target:** Owner, Admin.
- **Features:** questions volume, top topics, **unanswered (grounded=false) report → KB gap list**, per-coworker load, answer-quality evals.
- **Child pages:** Overview · Questions · Gaps · Quality.
- **Dependencies:** Tasks (interaction log — live substrate), Knowledge Factory.
- **API:** /analytics/*. **DB:** EventLog (from Task log).
- **AI:** insight narration ("eng ko'p so'ralgan, javobsiz mavzu: ish haqi hisoblash").

### 20. Integrations — P0 partial
- **Purpose:** connect the Uzbek SME stack.
- **Target:** Owner, Administrator.
- **Features (live):** **1C connector (OData, read-only sync → Company Context)**. **(P2):** Didox (EHF), my.soliq.uz calendar, Google Drive/Sheets, Excel import; per-connector config/status/sync pages. **(P3):** Telegram notifications channel.
- **Child pages:** Catalog · Connector Config · Sync Status.
- **Dependencies:** Documents, Calendar.
- **API (live):** /integrations/1c/{config,status,sync} · (P2) per-connector.
- **DB:** IntegrationConfig, SyncRun.
- **AI:** answers grounded in synced data (live).

---

## §1.3 Role × Module Access Matrix

Levels: **F** full/manage · **U** use · **V** view · **—** none

| Module | Owner | Admin | Manager | Accountant | HR | Secretary | Employee | Guest |
|---|---|---|---|---|---|---|---|---|
| Authentication | F | F | U | U | U | U | U | U |
| Workspace | F | F | V | V | V | V | V | — |
| Dashboard | U | U | U | U | U | U | U | — |
| Chat | U | U | U | U | U | U | U | V* |
| AI Coworkers | F | F | U | U | U | U | U | — |
| Company Brain | F | F | V | V | V | — | — | — |
| Knowledge | U | F | U | U | U | U | U | V |
| Documents | F | F | U | U (fin) | U (hr) | U | V | — |
| Tasks | F | F | F | U | U | U | U | — |
| Projects | F | F | F | U | U | U | U | — |
| Meetings | U | U | F | U | U | F | U | — |
| Calendar | U | U | U | F | U | U | V | — |
| Notifications | U | U | U | U | U | U | U | — |
| Search | U | U | U | U | U | U | U | — |
| Admin | F | F | — | — | — | — | — | — |
| Settings | F | F | U | U | U | U | U | — |
| Billing | F | V | — | — | — | — | — | — |
| Knowledge Factory | V | F | — | V | V | — | — | — |
| Analytics | F | F | V | V | V | — | — | — |
| Integrations | F | F | — | V | — | — | — | — |

\* Guest: shared conversation links only. Department scoping (Accountant→financial docs, HR→personnel docs) enforced at Documents entity level.

---

*Awaiting approval of §1 before proceeding to §2 (Navigation Tree, Sidebar, Command Palette, Notifications strategy), §3 (Application Flow), §4 (Complete Page Inventory).*

---

## §2. Navigation Architecture

### §2.1 Navigation Tree
```
[Workspace Switcher]
├── Dashboard                    (landing)
├── Chat
│   ├── New conversation (pick coworker)
│   └── History
├── Team (AI Coworkers)
│   └── Coworker Profile → opens Chat
├── Work
│   ├── Tasks (board / list / AI work log)
│   ├── Projects              [P3]
│   ├── Calendar  ⭐
│   └── Meetings              [P3]
├── Brain
│   ├── Knowledge (asset library)
│   ├── Documents (company context + generated)
│   ├── Company Brain overview [P2]
│   └── Knowledge Factory      [admin, P2]
├── Insights
│   └── Analytics              [P2]
├── Integrations
└── [bottom] Notifications · Search(⌘K) · Settings · Admin · Billing · Profile
```

### §2.2 Sidebar
- Collapsible, two states: icons-only / expanded. Order fixed (consistency > personalization at MVP).
- Sections: **Asosiy** (Dashboard, Chat, Team) · **Ish** (Tasks, Calendar, Projects, Meetings) · **Brain** (Knowledge, Documents, Factory) · **Boshqaruv** (Analytics, Integrations, Admin) — items hidden per role matrix (§1.3).
- Active coworker presence: mini-avatars of enabled coworkers pinned under "Team" (1-click to chat).

### §2.3 Top Navigation
Left: workspace switcher + breadcrumb. Center: global search field (expands to ⌘K palette). Right: credit meter (compact) · notifications bell · model indicator · user avatar menu.

### §2.4 Quick Actions (global "+")
One global create button, context-aware ordering: Ask coworker · Draft document · New task · Upload document · New meeting note. Every quick action is also a palette command.

### §2.5 Breadcrumb Strategy
`Workspace / Module / Page / Item` — max 4 levels; module name always clickable; item level shows entity id (e.g. TASK-0012, ACC-KA-003). Chat is breadcrumb-free (conversation header instead).

### §2.6 Global Search & Command Palette (⌘K)
- One surface, two modes: type text → search (assets, docs, tasks, chats); type ">" → commands ("yangi task", "Azizaga savol", "schyot-faktura tayyorla", "1C sync").
- Results grouped by entity type with permission filtering; Enter on a knowledge result opens asset, ⇥ asks the coworker about it.
- P2: semantic (pgvector); MVP: lexical (existing engine).

### §2.7 Notification System
- **Levels:** Critical (deadline ≤3 days, credit exhausted) → badge + banner; Normal (task assigned, sync done, mention) → badge; Digest (daily briefing) → Dashboard card.
- **Rules engine:** CalendarItem/Task/SyncRun/Billing emit events → NotificationPref filters per user.
- **Channels:** in-app (P1) → email (P2) → Telegram (P3).
- No noisy AI chatter: coworker replies never notify unless user left the conversation.

---

## §3. Application Flow (canonical)

```
Login ──► Workspace select (skip if one) ──► Dashboard
                                                │  sees: deadline "QQS — 3 kun"
                                                ▼
                                        Module (Calendar)
                                                │  opens deadline → "Aziza yordami"
                                                ▼
                                        AI Assistance (Chat, context = deadline+company profile)
                                                │  Aziza: checklist ACC-CHK-001 + drafts report steps
                                                ▼
                                        Task created (TASK-00xx, Running)
                                                │  human completes filing on my.soliq.uz
                                                ▼
                                        Completion (task → Completed; doc archived;
                                        interaction logged → Learning/Analytics; calendar item closed)
```
Rule: **every flow terminates in a recorded Task Asset** — nothing the platform helps with is lost (RFC-0004).

Secondary flows: (a) Document-first: Upload → auto-suggested questions → Chat; (b) Chat-first: question → answer → "save as task/doc"; (c) Integration-first: 1C sync → changed data → proactive insight (P3).

---

## §4. Complete Page Inventory

| # | Page | Purpose | Module | Key components | Perm (min) | API | Future |
|---|------|---------|--------|----------------|-----------|-----|--------|
| 1 | Login | authenticate | Auth | auth form | Guest | /auth/login | SSO |
| 2 | Register | create account | Auth | form | Guest | /auth/register | phone OTP |
| 3 | Invite Accept | join workspace | Auth | token form | Guest | /auth/invite | — |
| 4 | Password Reset | recover | Auth | form | Guest | /auth/reset | — |
| 5 | Workspace Select | pick tenant | Auth | workspace cards | Employee | /workspaces | — |
| 6 | Create Workspace | new company | Workspace | profile wizard | Owner | /workspaces | industry packs |
| 7 | Company Profile | company data (STIR, regime) | Workspace | form, AI-fill | Admin | /workspaces/{id} | auto from soliq.uz |
| 8 | Members | manage users | Workspace | member table, invite | Admin | /members | groups |
| 9 | Dashboard | My Day | Dashboard | deadline cards, task list, briefing, quick actions | Employee | /dashboard | per-role layouts |
| 10 | Coworker Picker | choose AI coworker | Chat | coworker cards | Employee | /coworkers | custom order |
| 11 | Conversation | chat with coworker | Chat | thread, composer, source chips, model picker | Employee | /ask /generate /models | voice input |
| 12 | Chat History | past conversations | Chat | list, search | Employee | /conversations | share link |
| 13 | Coworker Roster | team overview | AI Coworkers | roster grid, status | Employee | /coworkers | marketplace |
| 14 | Coworker Profile | scope & config | AI Coworkers | skills list, knowledge scope, model | Admin(edit) | /coworkers/{id} | builder P3 |
| 15 | Coworker Builder | create custom agent | AI Coworkers | trigger/skill/limits editor | Admin | /coworkers /triggers | P3 |
| 16 | Brain Overview | what AI knows | Company Brain | coverage stats, gaps | Manager | /brain/overview | P2 |
| 17 | Memory | company memory items | Company Brain | memory list, promote/retire | Admin | /memory | P3 (RFC-0005) |
| 18 | Company DNA | learned behavior traits | Company Brain | trait cards + evidence | Owner | /dna | P4 (RFC-0006) |
| 19 | Asset Library | browse KB | Knowledge | filterable asset cards | Employee | /assets | collections |
| 20 | Asset Detail | one asset | Knowledge | body, metadata, relations, "ask" | Employee | /assets/{id} | versions view |
| 21 | Document Library | company files | Documents | doc table, filters | Employee | /documents | folders |
| 22 | Upload Document | add context | Documents | uploader, type tag | Employee | POST /documents | PDF/DOCX parse |
| 23 | Document View | preview + ask | Documents | preview, Q&A panel | Employee | /documents/{id} | annotations |
| 24 | Generated Archive | AI outputs | Documents | list, re-export | Employee | /generated | .docx/.xlsx |
| 25 | Task Board | work by status | Tasks | kanban/list toggle, filters | Employee | /tasks | swimlanes |
| 26 | Task Detail | one task | Tasks | state controls, links, history | Employee | /tasks/{id} | comments |
| 27 | AI Work Log | auto-logged interactions | Tasks | log table, sources | Manager | /tasks?kind=ai | export |
| 28 | Projects | project list | Projects | project cards | Manager | /projects | P3 |
| 29 | Project Detail | tasks in project | Projects | task group, progress | Manager | /projects/{id} | P3 |
| 30 | Meetings | meeting list | Meetings | list, upload minutes | Employee | /meetings | P3 |
| 31 | Meeting Detail | summary & actions | Meetings | summary, action items→tasks | Employee | /meetings/{id} | recorder P4 |
| 32 | Calendar | obligations view | Calendar | month/list, deadline chips | Employee | /calendar | ICS export |
| 33 | Deadline Detail | one obligation | Calendar | rule source, checklist link, "Aziza yordami" | Employee | /calendar/{id} | auto-file P4 |
| 34 | Notification Center | all alerts | Notifications | grouped feed, prefs link | Employee | /notifications | — |
| 35 | Search Results | global results | Search | grouped results | Employee | /search | semantic P2 |
| 36 | Admin Users | governance | Admin | role editor | Admin | /admin/users | SCIM |
| 37 | Audit Log | who did what | Admin | event table | Admin | /admin/audit | export |
| 38 | Data Controls | export/delete tenant data | Admin | actions + confirmations | Owner | /admin/data | retention |
| 39 | Profile Settings | personal prefs | Settings | profile, language uz/ru, theme | Employee | /settings/me | — |
| 40 | Workspace Settings | defaults, keys | Settings | model keys, coworker toggles | Admin | /settings/workspace | — |
| 41 | Billing Plan | plan & upgrade | Billing | plan cards | Owner | /billing/plan | Payme/Click |
| 42 | Usage | credit consumption | Billing | usage chart, meter | Owner | /me /billing/usage | forecasts |
| 43 | Factory Review Queue | asset lifecycle | Knowledge Factory | Draft→Review→Approve queue | Admin | /factory/queue | P2 |
| 44 | Asset Editor | author/edit asset | Knowledge Factory | metadata form, body editor, validators | Admin | /factory/assets | AI draft |
| 45 | Quality Dashboard | evals & stale | Knowledge Factory | recall@k, stale list, gaps | Admin | /factory/quality | LLM-judge |
| 46 | Training Exports | SFT datasets | Knowledge Factory | export runs, download | Owner | /factory/exports | own-model P3 |
| 47 | Analytics Overview | usage insight | Analytics | volumes, topics, coworker load | Manager | /analytics | P2 |
| 48 | Gap Report | unanswered questions | Analytics | grounded=false list → "create asset" | Admin | /analytics/gaps | auto-draft |
| 49 | Integration Catalog | available connectors | Integrations | connector cards (1C live) | Admin | /integrations | Didox, soliq.uz |
| 50 | Connector Config | credentials & scope | Integrations | config form, test | Admin | /integrations/1c/config | per-connector |
| 51 | Sync Status | runs & errors | Integrations | run history | Admin | /integrations/1c/status | schedules |

---

*End of Phase 1 — Product UX Architecture. Phase 2 (UI design) starts only after this document is approved.*
