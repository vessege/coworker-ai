---
id: OM-SOP-002
title: Outgoing Document Preparation & Dispatch / Chiquvchi hujjatlarni tayyorlash va jo'natish
type: SOP
category: workflow-asset
domain: office-management
subdomain: document-flow
department: Administration
role: Office Manager
summary: Procedure for drafting, approving, registering and dispatching outgoing letters per O'zDSt 1157:2008.
source: O'zDSt 1157:2008; umumiy ish yuritish amaliyoti
source_url: https://lex.uz/uz/docs/-5529263; https://standart.uz
tags: [chiquvchi-hujjat, xat, jonatish, royxatga-olish, SOP, ish-yuritish]
language: [uz, en]
country: UZ
quality: reviewed
status: Approved
confidence: 0.85
owner: CKO / Knowledge Factory
version: 1.0.0
created: '2026-07-07'
updated: '2026-07-07'
last_review: 2026-07-07
valid_from: 2026-01-01
source_verified: 2026-07-07
review_cycle: semiannual
relationships:
- {type: references, target: OM-TPL-001}
- {type: references, target: OM-BR-001}
- {type: extends, target: OM-SOP-001}
workflow:
  business_goal: Produce and dispatch a correct, registered outgoing document with full traceability.
  difficulty: Low
  estimated_duration: 15-40 min per document
  automation_score: 70
  required_inputs: [Purpose/request for the letter, Addressee details, Letterhead]
  expected_outputs: [Signed outgoing letter, Register entry with outgoing number, Dispatch confirmation]
  success_criteria: [Requisites match O'zDSt 1157:2008, Unique outgoing number assigned, Copy filed]
  failure_conditions: [Dispatched without registration, Signed by unauthorized person, No file copy retained]
  approval_points: [Authorized signatory signs before dispatch]
  kpis: [Turnaround time, Return/error rate]
  steps:
  - {number: 1, title: Draft the letter, actor: AI Assistant, ai_capability: Draft,
     required_docs: [Letter template OM-TPL-001], expected_result: Draft with correct requisites,
     validation_rule: One letter — one matter; formal style}
  - {number: 2, title: Internal review, actor: Office Manager, ai_capability: Review,
     required_docs: [], expected_result: Content and addressee verified,
     validation_rule: Attachments listed if present}
  - {number: 3, title: Signature, actor: Manager, ai_capability: Observe,
     required_docs: [], expected_result: Signed by an authorized person,
     validation_rule: Signer has signing authority}
  - {number: 4, title: Register, actor: Office Manager, ai_capability: Automate,
     required_docs: [Outgoing register], expected_result: Sequential outgoing number + date assigned,
     validation_rule: Number unique, never reused (OM-BR-001/BR-2)}
  - {number: 5, title: Dispatch, actor: Office Manager, ai_capability: Execute,
     required_docs: [], expected_result: Sent via post/courier/e-channel; proof kept,
     validation_rule: Dispatch method and date recorded}
  - {number: 6, title: File the copy, actor: Office Manager, ai_capability: Automate,
     required_docs: [], expected_result: Copy filed per nomenclature,
     validation_rule: Case index recorded in the register}
---

# 🇺🇿 Chiquvchi hujjatlarni tayyorlash va jo'natish (SOP)

## Bosqichlar
1. **Loyiha tayyorlash** — OM-TPL-001 shabloni bo'yicha; bitta xat — bitta masala.
2. **Ichki tekshiruv** — mazmun, adresat, ilovalar.
3. **Imzolash** — faqat vakolatli shaxs.
4. **Ro'yxatga olish** — chiquvchi jurnaldan ketma-ket, **noyob raqam** va sana (raqam qayta ishlatilmaydi).
5. **Jo'natish** — pochta/kuryer/elektron; usul va sana qayd etiladi, dalil saqlanadi.
6. **Nusxani tikish** — nomenklatura bo'yicha ishga; jurnalda ish indeksi ko'rsatiladi.

## Xatolardan saqlanish
- Ro'yxatga olinmagan xat jo'natilmaydi.
- Imzosiz/vakolatsiz imzoli xat — yaroqsiz.
- Nusxasiz jo'natish — keyin isbot yo'q.

---

# 🇬🇧 Outgoing Document Preparation & Dispatch (SOP)

## Steps
1. **Draft** — using OM-TPL-001; one letter — one matter.
2. **Internal review** — content, addressee, attachments.
3. **Signature** — authorized signatory only.
4. **Register** — sequential **unique number** + date from the outgoing register (numbers never reused).
5. **Dispatch** — post/courier/e-channel; method and date recorded, proof kept.
6. **File the copy** — into the case per nomenclature; case index noted in the register.

## Mistakes to avoid
- Never dispatch unregistered letters.
- Unsigned / unauthorized-signature letters are void.
- No retained copy = no proof later.
