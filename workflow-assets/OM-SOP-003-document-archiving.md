---
id: OM-SOP-003
title: Document Archiving Procedure / Hujjatlarni arxivga topshirish tartibi
type: SOP
category: workflow-asset
domain: office-management
subdomain: records-management
department: Administration
role: Office Manager
summary: Year-end procedure for closing document files and transferring them to the archive per record-keeping rules.
source: O'zDSt 1157:2008 — Tashkiliy-farmoyish hujjatlari tizimi; umumiy ish yuritish amaliyoti
source_url: https://lex.uz/uz/docs/-5529263; https://standart.uz
tags: [arxiv, ish-yuritish, delovodstvo, hujjat-aylanishi, saqlash-muddati, SOP]
language: [uz, en]
country: UZ
quality: reviewed
status: Approved
confidence: 0.8
owner: CKO / Knowledge Factory
version: 1.0.0
created: '2026-07-09'
updated: '2026-07-09'
last_review: 2026-07-09
valid_from: 2008-01-01
source_verified: 2026-07-09
review_cycle: annual
relationships:
- {type: references, target: OM-SOP-001}
- {type: references, target: OM-BR-001}
workflow:
  business_goal: Close the year's document files correctly and transfer them to the archive without loss or premature destruction.
  difficulty: Low
  estimated_duration: 1-2 working days
  automation_score: 40
  required_inputs: [Nomenklatura (file list/index), Year's registered documents]
  expected_outputs: [Closed and labeled files, Archive inventory, Transfer act]
  success_criteria: [Every file labeled with retention period, Inventory matches nomenklatura, Transfer act signed]
  failure_conditions: [Files transferred without labeling, Retention period missing, No transfer act]
  approval_points: [Head of office/administration signs the transfer act]
  kpis: [Files processed on time, Retrieval time for archived documents]
  steps:
  - {number: 1, title: Close the year's files, actor: Office Manager, ai_capability: Suggest,
     required_docs: [Nomenklatura], expected_result: Files finalized, no further documents added,
     validation_rule: Matches the approved nomenklatura}
  - {number: 2, title: Label retention periods, actor: Office Manager, ai_capability: Suggest,
     required_docs: [], expected_result: Each file marked with its legal retention period,
     validation_rule: Every file has a retention label}
  - {number: 3, title: Build the archive inventory, actor: Office Manager, ai_capability: Draft,
     required_docs: [], expected_result: Inventory list of transferred files,
     validation_rule: Inventory count matches physical files}
  - {number: 4, title: Sign the transfer act, actor: Head of Administration, ai_capability: Observe,
     required_docs: [Archive inventory], expected_result: Signed transfer act,
     validation_rule: Act references the inventory}
---

> ⚠️ Axborot xarakterida; saqlash muddatlarini rasmiy me'yoriy hujjatlar bilan tasdiqlang.

# 🇺🇿 Hujjatlarni arxivga topshirish tartibi (SOP)

## Bosqichlar
1. **Ishlarni yopish** — yil davomida to'plangan hujjat ishlari (nomenklatura bo'yicha) yakunlanadi, yangi hujjat qo'shilmaydi.
2. **Saqlash muddatini belgilash** — har bir ish papkasiga saqlash muddati yozib qo'yiladi.
3. **Ro'yxat (inventar) tuzish** — arxivga topshirilayotgan ishlar ro'yxati tayyorlanadi.
4. **Topshirish dalolatnomasi** — mas'ul rahbar imzosi bilan rasmiylashtiriladi.

## Xatolardan saqlanish
- Saqlash muddati yozilmagan hujjatni arxivga topshirish — keyinchalik yo'qotish xavfi.
- Ro'yxatsiz (dalolatnomasiz) topshirish nazoratni yo'qotadi.

---

# 🇬🇧 Document Archiving Procedure (SOP)

## Steps
1. **Close the year's files** — files accumulated per the nomenklatura are finalized; no new documents are added.
2. **Label retention periods** — each file is marked with its retention period.
3. **Build the inventory** — a list of files being transferred to the archive is prepared.
4. **Sign the transfer act** — formalized with the responsible head's signature.

## Mistakes to avoid
- Archiving a file without a retention label risks losing it later.
- Transferring without an inventory/act loses control of the paper trail.
