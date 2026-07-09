# CoWorker AI — Dashboard Architecture (Phase 1, Module Deep-Dive)

Status: draft · Owner: Chief Product Designer · Scope: Dashboard module only (no UI)
Parent: docs/blueprints/ux-architecture.md §1.2 Module 3
Legend: **P0** live · **P1** MVP+ · **P2** post-validation · **P3** platform phase

---

## 1. Dashboard Purpose

The Dashboard is the employee's home screen — the first surface after login and the
default return point from every module. It answers one question in under five
seconds: **"What do I do right now?"**

It is not a reporting surface. It is not a vanity-metrics screen. It is a
**work-routing surface**: a filtered, prioritized, AI-narrated view of obligations,
AI output awaiting review, and the fastest path into action.

### 1.1 Primary User Goals
- Know what is overdue or due today (deadlines, tasks, approvals) in one glance.
- See what AI coworkers already produced overnight/since last visit, without asking.
- Resume the most recent unfinished conversation or task with one click.
- Start new work (ask, draft, upload, schedule) in one click, from anywhere on the page.
- Trust the numbers: every item traces to a source (KB asset, document, or task).

### 1.2 Success Metrics
- **Time-to-first-action**: seconds from page load to the user clicking a task/action.
- **Zero-click awareness**: % of critical items (deadlines ≤3 days) surfaced without search.
- **Dashboard-originated task completion rate**: tasks created from Dashboard quick actions that reach Completed.
- **Return rate**: % of sessions that start at Dashboard (vs. deep link) — should stay high; a low number means the Dashboard isn't earning the "home screen" role.
- **AI-suggestion acceptance rate**: suggested tasks/coworker actions accepted vs. dismissed.

### 1.3 Daily Workflow (target)
```
Open app → Dashboard loads
   → Greeting + one-line AI morning summary (read, 3 sec)
   → Today's Focus scanned (read, 5 sec)
   → Click top item (deadline or suggested task)
   → Routed to Chat/Calendar/Task with context pre-loaded
   → Work completed → Task marked Completed
   → Return to Dashboard → item gone, next item surfaced
```
The loop is: **surface → act → clear → next**. A well-used Dashboard trends toward
emptiness by end of day, not toward accumulation.

---

## 2. Dashboard Sections

Ordered by default vertical priority (top = most urgent). Each section is an
independently loadable widget (§4).

### 2.1 Greeting
- **Purpose:** orient the user (who, where, when) and set tone; carries the AI morning summary.
- **Displayed information:** time-of-day greeting (uz), user name, workspace name, one-sentence AI-generated summary ("Bugun: QQS muddatiga 3 kun qoldi, 2 ta task sizni kutmoqda, Aziza 1 hujjat tayyorladi").
- **Actions:** click summary → expands into Today's Focus (scrolls down, no navigation).
- **AI features:** summary is generated from Calendar + Tasks + AI Work Log deltas since last visit (P1: template-composed from live data; P2: LLM-narrated).
- **Priority:** P1 (highest — always visible, above the fold).
- **Visibility:** all roles, always.
- **Future expansion:** voice greeting; personalized tone based on Company DNA (P4).

### 2.2 Today's Focus
- **Purpose:** the single ranked list of what needs the user's attention today — the section that actually answers "what do I do."
- **Displayed information:** merged, ranked feed of: deadlines due ≤3 days (Calendar), tasks assigned to me in Running/Waiting/Review, pending approvals, AI-flagged risks. Each row: type icon, title, due/urgency, one-line "why."
- **Actions:** click row → opens Task/Calendar/Approval detail; inline "mark done" / "snooze" / "ask Aziza."
- **AI features:** ranking algorithm (deadline proximity × role relevance × penalty risk); "why" line auto-generated from source asset (e.g. links ACC-KA-004 for a filing-penalty risk).
- **Priority:** P1, section 1 (top of main area).
- **Visibility:** all roles; content scoped to role (Accountant sees tax deadlines first, HR sees onboarding tasks first).
- **Future expansion:** drag-to-reprioritize; team-wide focus view for Managers (P2).

### 2.3 AI Suggestions
- **Purpose:** surface proactive AI recommendations the user did not explicitly ask for — the clearest "AI coworker" moment on the page.
- **Displayed information:** cards like "Aylanma soliq chegarasiga yaqinlashyapsiz — rejimni ko'rib chiqing (ACC-DT-001)" or "3 ta xodim ish joyidan ma'lumotnoma so'ragan — shablonni oldindan tayyorlaymi?"
- **Actions:** Accept (creates Task / opens Chat with pre-filled prompt) · Dismiss (logged, trains suppression) · "Nega?" (shows source reasoning).
- **AI features:** rule-based triggers at P1 (threshold crossings, repeated questions from Analytics gap report); LLM-generated novel suggestions at P2.
- **Priority:** P1, section 2.
- **Visibility:** role-scoped; Owner/Admin additionally see workspace-wide suggestions (billing, compliance).
- **Future expansion:** suggestion feedback loop back into Knowledge Factory gap list.

### 2.4 Recent Activity (AI Work Log excerpt)
- **Purpose:** show what AI already did since the user's last visit — closes the "did anything happen while I was away" gap.
- **Displayed information:** last 5–8 completed AI interactions (chat answers, generated documents, 1C syncs) with coworker avatar, one-line result, source chips.
- **Actions:** click → opens full conversation/document; "View all" → AI Work Log (Tasks module).
- **AI features:** this section *is* AI output — no additional generation, just surfacing (live substrate: Task log, already recording every /ask and /generate).
- **Priority:** P1, section 3.
- **Visibility:** all roles; each user sees own + coworker-broadcasted items (e.g. 1C sync results visible to Accountant+Admin).
- **Future expansion:** filter by coworker; team activity feed for Managers.

### 2.5 Tasks (My Tasks summary)
- **Purpose:** compact status of the user's task load beyond what fit in Today's Focus.
- **Displayed information:** counts by status (Running/Waiting/Review/Completed this week), small list of next 3 non-urgent tasks.
- **Actions:** click count → filtered Task Board; "+ New task."
- **AI features:** none beyond existing auto-logging.
- **Priority:** P2 (secondary — Today's Focus already carries urgent tasks).
- **Visibility:** all roles.
- **Future expansion:** burndown-style mini chart for Managers/Projects (P3).

### 2.6 Approvals
- **Purpose:** items explicitly waiting on this user's decision (documents, expense-adjacent actions, task hand-offs).
- **Displayed information:** requester, item type, age, one-line context.
- **Actions:** Approve / Reject inline (with optional comment); click → full detail.
- **AI features:** AI pre-checks (e.g. "summa fakturaga mos" flag) shown as a badge.
- **Priority:** P2 (P1 if any approvals exist — dynamic priority: a non-empty Approvals section outranks Tasks summary).
- **Visibility:** role- and permission-scoped (only items routed to this user).
- **Future expansion:** delegation ("approve on my behalf while I'm away").

### 2.7 Documents (recent + needs-review)
- **Purpose:** surface newly uploaded/generated/synced documents relevant to the user.
- **Displayed information:** thumbnail/type icon, title, source (upload/generated/1C sync), timestamp.
- **Actions:** open, "ask about this document," archive.
- **AI features:** auto-summary line per document (P2, requires LLM key).
- **Priority:** P2.
- **Visibility:** role-scoped (Accountant sees financial docs, HR sees personnel docs — matches §1.3 access matrix).
- **Future expansion:** OCR-flagged anomalies.

### 2.8 Meetings [P3]
- **Purpose:** today's/upcoming meetings with AI prep.
- **Displayed information:** time, title, attendees, "AI prep ready" badge.
- **Actions:** join link, view AI-prepared brief.
- **AI features:** pre-meeting summary from related documents/tasks.
- **Priority:** P3 (module itself is P3).
- **Visibility:** all roles.
- **Future expansion:** post-meeting action-item sync into Tasks.

### 2.9 Calendar (mini)
- **Purpose:** compact week-at-a-glance, primarily tax/compliance deadlines.
- **Displayed information:** 7-day strip, color-coded by type (deadline/task/meeting), density dots.
- **Actions:** click day → full Calendar module.
- **AI features:** deadline population is auto-generated per company tax regime (ACC-KA-001 + Company Profile) — this is the local killer-feature substrate.
- **Priority:** P1, section 4.
- **Visibility:** all roles; Accountant sees full detail, others see counts only.
- **Future expansion:** ICS export, per-role calendar overlays.

### 2.10 Notifications (digest card)
- **Purpose:** condensed unread-notification count with top 3 items — the Dashboard's mirror of the persistent bell icon.
- **Displayed information:** unread count, top items by urgency.
- **Actions:** click → Notification Center panel.
- **AI features:** digest grouping ("5 ta eslatma: 3 muddat, 2 mention").
- **Priority:** P2.
- **Visibility:** all roles.
- **Future expansion:** none beyond parent module.

### 2.11 Company Health [P2]
- **Purpose:** Owner/Admin-only pulse: compliance status, credit usage, integration health.
- **Displayed information:** filing-on-time streak, credit meter, 1C last-sync status, active coworkers count.
- **Actions:** click metric → Analytics/Billing/Integrations detail.
- **AI features:** anomaly narration ("bu oy 2 marta hisobot kechikdi — sabab: ...").
- **Priority:** P2.
- **Visibility:** Owner, Administrator only.
- **Future expansion:** benchmark against similar businesses (requires cross-tenant aggregation — privacy-gated, P4).

### 2.12 Quick Actions
- **Purpose:** zero-navigation entry point into the most common actions — reduces the "where do I even start" friction.
- **Displayed information:** button row (see §5), not a data widget.
- **Actions:** see §5.
- **AI features:** action set can reorder by usage frequency (P2).
- **Priority:** P1, always visible (persistent, not scrollable away — lives in header or as a floating affordance).
- **Visibility:** role-filtered (Employee doesn't see "Create Invoice").
- **Future expansion:** custom user-defined quick actions.

### 2.13 Pinned Items [P2]
- **Purpose:** user-controlled persistent shortcuts (a specific asset, task, or conversation kept always visible).
- **Displayed information:** small card per pin.
- **Actions:** unpin, open.
- **AI features:** none.
- **Priority:** P2.
- **Visibility:** personal, all roles.
- **Future expansion:** shared team pins (Manager-curated).

### 2.14 Favorite Coworkers
- **Purpose:** one-click resume into the most-used AI coworkers — the "team" is core identity, so it earns Dashboard real estate.
- **Displayed information:** avatar row (Aziza/Malika/Jasur/General today), presence dot, last-interaction time.
- **Actions:** click → opens Chat with that coworker (new or continued thread).
- **AI features:** ordering by usage recency/frequency.
- **Priority:** P1, section 5 (compact, near Quick Actions).
- **Visibility:** all roles; set filtered to workspace-enabled coworkers.
- **Future expansion:** custom coworkers appear here once built (P3).

### 2.15 Recent Conversations
- **Purpose:** resume unfinished chats without hunting through history.
- **Displayed information:** last 3–5 conversations, coworker avatar, last message preview, timestamp.
- **Actions:** click → resumes Conversation.
- **AI features:** none beyond existing thread retrieval.
- **Priority:** P2 (P1 once Chat History/persistence ships — currently Chat has no persisted history).
- **Visibility:** personal, all roles.
- **Future expansion:** cross-device resume.

### 2.16 Analytics (snapshot) [P2]
- **Purpose:** lightweight usage/insight teaser for Managers/Owners — full detail lives in the Analytics module.
- **Displayed information:** 2–3 sparkline stats (questions this week, top topic, gap count).
- **Actions:** click → Analytics module.
- **AI features:** topic clustering.
- **Priority:** P3.
- **Visibility:** Manager, Admin, Owner.
- **Future expansion:** none beyond parent module.

---

## 3. Dashboard Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER  (persistent, not scrollable)                             │
│  workspace switcher · global search/⌘K · Quick Actions ·         │
│  credit meter · notifications bell · avatar                      │
├───────────────────────────────────────────┬───────────────────────┤
│ MAIN AREA (scrollable, widget stack)       │ SIDEBAR (right rail)  │
│                                             │                       │
│  1. Greeting + AI morning summary          │  Favorite Coworkers   │
│  2. Today's Focus  (ranked list)           │  Recent Conversations │
│  3. AI Suggestions (cards)                 │  Calendar (mini)      │
│  4. Approvals            [if non-empty]    │  Notifications digest │
│  5. Recent Activity (AI Work Log excerpt)  │  Pinned Items  [P2]   │
│  6. Tasks summary                          │  Company Health [P2,  │
│  7. Documents (recent + needs-review)      │   Owner/Admin only]   │
│  8. Meetings              [P3]             │                       │
│  9. Analytics snapshot    [P2/P3]          │                       │
│                                             │                       │
├─────────────────────────────────────────────────────────────────┤
│ FOOTER — none. (Enterprise dashboards should not require footer  │
│  scrolling for primary tasks; global nav lives in sidebar/header │
│  per ux-architecture.md §2.)                                      │
└─────────────────────────────────────────────────────────────────┘
```

**Rationale for left-main/right-rail split:** left column carries *what requires
decisions* (time-ordered, action-oriented); right rail carries *fast entry points*
(people/tools-oriented, static position, always reachable without scrolling past
the main feed). This mirrors Linear's issue-list + activity-rail pattern without
copying its visual system.

**Responsive collapse (structural, not visual):** on narrow viewports the right
rail collapses beneath the main area in this order: Favorite Coworkers → Calendar
mini → Recent Conversations → Notifications → Pinned → Company Health.

---

## 4. Widget Architecture

Common contract for every widget below (stated once, applies to all):
- **Loading state:** skeleton row matching final layout (no spinner-only states).
- **Empty state:** short affirmative message + one relevant quick action (never a bare "no data").
- **Permissions:** enforced server-side (API returns only authorized items) and mirrored client-side (widget hidden entirely if role has zero visibility, per §1.3 access matrix).

| Widget | Purpose | Data source | API | Refresh | Empty state | AI integration |
|---|---|---|---|---|---|---|
| Greeting | orient + summarize | Calendar, Tasks, AI Work Log deltas | `GET /dashboard` (aggregator) | on load + on tab focus | "Bugun hech narsa shoshilinch emas — yangi suhbat boshlang" + Quick Action | summary composition (P1 template, P2 LLM) |
| Today's Focus | ranked action list | Calendar, Tasks, Approvals | `GET /dashboard` (aggregator) | on load; live-update via polling P1, websocket P3 | "Barcha ishlar bajarilgan ✓" | ranking algorithm, "why" generation |
| AI Suggestions | proactive recs | Analytics gap report, rule engine | `GET /dashboard/suggestions` | on load, dismiss removes immediately | hidden entirely if none (not shown empty) | rule-based P1, LLM-generated P2 |
| Recent Activity | AI output feed | Task log (existing live substrate) | `GET /tasks?kind=ai&limit=8` | on load + on new item (poll) | "Hali AI faoliyati yo'q — birinchi savolni bering" + Quick Action | none (surfacing only) |
| Tasks summary | task load counts | Tasks | `GET /tasks?summary=true` | on load | "Tasklar yo'q" + "+ New task" | none |
| Approvals | pending decisions | Tasks/Documents routed for approval | `GET /approvals` [P2] | on load; badge live-updates | section hidden if empty | AI pre-check badges [P2] |
| Documents | recent/needs-review files | Documents | `GET /documents?recent=true` | on load | "Hujjat yuklanmagan" + Upload action | auto-summary [P2] |
| Meetings [P3] | today's meetings | Meetings | `GET /meetings?today=true` | on load | "Bugun uchrashuv yo'q" | AI prep brief |
| Calendar mini | week-at-a-glance | Calendar generator (KB deadlines + tasks) | `GET /calendar?range=week` | on load | shows empty week grid | deadline auto-population |
| Notifications digest | unread summary | Notifications | `GET /notifications?unread=true&limit=3` | live (poll/websocket) | "Yangi eslatma yo'q" | digest grouping |
| Company Health [P2] | compliance/usage pulse | Analytics, Billing, Integrations | `GET /brain/health` | on load | n/a (always has data once workspace active) | anomaly narration |
| Quick Actions | action launcher | static config + role filter | n/a (client-side routing) | n/a | n/a | usage-based reorder [P2] |
| Pinned Items [P2] | user shortcuts | user preference store | `GET /pins` | on load | "Hech narsa pin qilinmagan" | none |
| Favorite Coworkers | fast coworker access | Coworkers + usage stats | `GET /coworkers?favorites=true` | on load | shows full default roster (never empty) | usage-based ordering |
| Recent Conversations | resume chats | Conversations [P1 persistence] | `GET /conversations?limit=5` | on load | "Suhbat tarixi yo'q — hamkasbingizga yozing" | none |
| Analytics snapshot [P2] | insight teaser | Analytics | `GET /analytics/snapshot` | on load | "Yetarli ma'lumot yo'q" | topic clustering |

---

## 5. Quick Actions

Fixed, role-filtered action set, always reachable from header (not buried in scroll):

| Action | Result | Roles |
|---|---|---|
| Ask AI | opens Chat composer (coworker picker if none pinned) | all |
| Create Task | inline task-creation modal | all |
| Upload Document | opens uploader, attaches to Documents | all (scope-limited) |
| Generate Report / Document | opens Hujjat-mode composer with template picker | Accountant, HR, Office Manager |
| Create Invoice (schyot-faktura) | pre-fills Hujjat mode with ACC-TPL-001 | Accountant |
| Schedule Meeting [P3] | opens meeting scheduler | Manager, Secretary |
| Search Company Brain | opens ⌘K in search mode | all |

Each Quick Action is also registered as a Command Palette entry (consistent with
ux-architecture.md §2.4/§2.6 — one action registry, two entry surfaces).

---

## 6. AI Features (Dashboard-specific)

| Feature | Description | Trigger | Phase |
|---|---|---|---|
| Morning Summary | one-sentence narrated state of the day | page load, first visit of the day | P1 (template) → P2 (LLM) |
| Today's Priorities | ranking of Today's Focus items | continuous (recomputed on data change) | P1 |
| Risk Detection | flags approaching thresholds (regime limits, filing penalties) using KB rules (e.g. ACC-DT-001, ACC-KA-004) | scheduled check against Company Profile + Calendar | P1 (rule-based) |
| Pending Approvals surfacing | pulls items awaiting this user | on load | P2 |
| Suggested Tasks | proposes tasks from repeated questions / gap report | Analytics gap detection | P2 |
| Meeting Preparation [P3] | pre-brief generation from linked documents/tasks | before meeting start | P3 |
| Document Insights [P2] | auto-summary + anomaly flags on new documents | on upload/sync | P2 |
| Automation Suggestions [P3] | proposes a workflow/trigger for repeated manual patterns | usage-pattern detection | P3 |

All AI-generated text on the Dashboard follows the platform-wide grounding rule:
**no ungrounded claims** — every AI Suggestion and Risk Detection item links to its
source KB asset or data point (consistent with the source-chip pattern already
live in Chat).

---

## 7. Personalization

| Capability | Behavior | Phase |
|---|---|---|
| Move widgets | drag-reorder within main area and right rail independently | P2 |
| Hide widgets | per-widget toggle in a "Customize Dashboard" panel; hidden ≠ deleted, restorable | P2 |
| Pin widgets | force a widget above the ranked/dynamic ones (e.g. always show Calendar mini first) | P2 |
| Resize widgets | 2–3 fixed size presets (compact/standard/expanded), not free-form | P3 |
| Save layouts | one layout per user per workspace, persisted server-side | P2 |
| Dashboard presets | role-based starting layouts (Accountant preset leads with Calendar; Owner preset leads with Company Health) applied on first login, user-customizable after | P1 (fixed presets, no editing) → P2 (editable) |

Personalization never changes *data scope* (permissions are server-enforced,
independent of layout preference) — only *presentation order and visibility*.

---

*Dashboard Blueprint complete. Awaiting approval before proceeding to the next module deep-dive.*
