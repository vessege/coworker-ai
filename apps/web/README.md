# CoWorker AI — Web (Next.js)

Uzbek-first web UI for the accountant AI coworker. Two features:
**Savol berish** (grounded Q&A via `/ask`) and **Hujjat tayyorlash**
(document generation via `/generate`). Every answer shows its source.

## Run
```bash
# 1) start the API first (see apps/api/README.md), then:
cd apps/web
cp .env.local.example .env.local     # point NEXT_PUBLIC_API_URL at the API
npm install
npm run dev                          # http://localhost:3000
```

The API must allow the web origin via CORS (`cors_origins`, default
`http://localhost:3000`).

## Stack
- Next.js 14 (App Router), React 18, TypeScript. No UI framework — plain CSS,
  theme-aware (light/dark), mobile-friendly.
- API calls in `lib/api.ts`; UI in `app/page.tsx`.

## Notes
- Without `ANTHROPIC_API_KEY` on the API, answers come back in retrieval-only
  mode (raw context) — the UI still works for demos.
- Informational only; not official tax advice.
