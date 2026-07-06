# CoWorker AI — Company Brain / Knowledge Base

Enterprise knowledge base for CoWorker AI (Uzbekistan SME AI Coworker platform).
Every file is a single, self-contained, reusable knowledge asset in Markdown.

## Asset categories & directories

| Directory | Category | Description |
|-----------|----------|-------------|
| `knowledge-assets/` | Knowledge Asset | Reference knowledge, concepts, explanations |
| `workflow-assets/` | Workflow / SOP | Step-by-step procedures |
| `checklists/` | Checklist | Verifiable task lists |
| `templates/` | Template | Ready-to-fill document skeletons |
| `policies/` | Policy | Internal rules & governance |
| `business-rules/` | Business Rule | Machine-parseable decision rules |
| `decision-trees/` | Decision Tree | Branching logic |
| `glossary/` | Business Vocabulary | Term definitions |
| `faq/` | FAQ | Question–answer pairs |

## Metadata schema (required front-matter)

```yaml
---
id:            # unique, e.g. OM-SOP-001
title:         # human title
category:      # one of the categories above
domain:        # e.g. office-management
source:        # source name
source_url:    # traceable URL (or "vendor-neutral best practice")
tags:          # list
quality:       # draft | reviewed | production-ready
language:      # [uz, en]
country:       # UZ
version:       # semver
last_review:   # YYYY-MM-DD
---
```

## ID scheme

`<ROLE>-<TYPE>-<NNN>` — e.g. `OM-SOP-001`.
Role prefixes: `OM` Office Manager, `ACC` Accountant, `HR`, `SAL` Sales,
`SEC` Secretary, `CS` Customer Support, `DIR` Director, `OPS` Operations.
Type prefixes: `SOP`, `CHK` checklist, `TPL` template, `BR` business rule,
`DT` decision tree, `GLO` glossary, `KA` knowledge asset, `POL` policy, `FAQ`.

## Principles

1. Never hallucinate. Official sources first. Every statement traceable.
2. Bilingual (Uzbek + English) parallel sections for training-data alignment.
3. Vendor-neutral where possible.
4. One asset per file. Production-ready.

## Sources verification note

Uzbek legal/standard references are grounded in official designations
(e.g. **O'zDSt 1157:2008**, laws on lex.uz). Where a live official URL could
not be fetched in the build environment, the source designation is cited and
must be re-verified against lex.uz / standart.uz before production release.
