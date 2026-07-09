---
id: HR-SOP-002
title: Employee Termination Procedure / Xodimni ishdan bo'shatish tartibi
type: SOP
category: workflow-asset
domain: hr
subdomain: termination
department: Human Resources
role: HR
summary: Compliant procedure for ending employment — notice, order, final settlement, and document handover under the 2023 Labour Code.
source: Mehnat kodeksi (30.04.2023); srsl.uz kadrlar ish yuritish qo'llanmasi
source_url: https://lex.uz/mact/-6257288
tags: [ishdan-boshatish, termination, buyruq, hisob-kitob, mehnat-daftarchasi, SOP]
language: [uz, en]
country: UZ
quality: reviewed
status: Approved
confidence: 0.75
owner: CKO / Knowledge Factory
version: 1.0.0
created: '2026-07-09'
updated: '2026-07-09'
last_review: 2026-07-09
valid_from: 2023-04-30
source_verified: 2026-07-09
review_cycle: semiannual
relationships:
- {type: requires, target: HR-KA-001}
- {type: produces, target: HR-TPL-002}
- {type: references, target: HR-SOP-001}
workflow:
  business_goal: End an employment relationship in full compliance with the Labour Code, avoiding wrongful-dismissal risk.
  difficulty: Medium
  estimated_duration: 1-3 working days
  automation_score: 45
  required_inputs: [Grounds for termination, Employee file, Contract]
  expected_outputs: [Termination order, Final settlement calculation, Work record entry]
  success_criteria: [Legal grounds documented, Employee notified per contract/law, Full final settlement paid on last working day]
  failure_conditions: [No documented grounds, Final settlement delayed past last working day, Work record not updated]
  approval_points: [Director signs the termination order]
  kpis: [Time-to-settle, Dispute rate]
  steps:
  - {number: 1, title: Document the grounds, actor: HR Specialist, ai_capability: Suggest,
     required_docs: [Contract, Supporting evidence if for-cause], expected_result: Written grounds on file,
     validation_rule: Grounds match a Labour Code basis}
  - {number: 2, title: Notify the employee, actor: HR Specialist, ai_capability: Draft,
     required_docs: [Notice letter], expected_result: Signed acknowledgment of notice,
     validation_rule: Notice period per contract/law observed}
  - {number: 3, title: Issue the termination order, actor: HR Specialist, ai_capability: Draft,
     required_docs: [HR-TPL-002], expected_result: Order issued and acknowledged by signature,
     validation_rule: Order references documented grounds}
  - {number: 4, title: Final settlement, actor: Accountant, ai_capability: Automate,
     required_docs: [Payroll records, Unused-leave balance], expected_result: Full payment calculated and paid,
     validation_rule: Paid on or before the last working day}
  - {number: 5, title: Return documents, actor: HR Specialist, ai_capability: Observe,
     required_docs: [], expected_result: Work record / electronic labour book updated and returned,
     validation_rule: Handover confirmed by signature}
---

> ⚠️ Axborot xarakterida; asos va muddatlarni lex.uz va yuristingiz bilan tasdiqlang.

# 🇺🇿 Xodimni ishdan bo'shatish tartibi (SOP)

## Bosqichlar
1. **Asosni hujjatlashtirish** — bo'shatish sababi (o'z xohishi, tomonlar kelishuvi, qonuniy asos) yozma qayd etiladi.
2. **Xodimni xabardor qilish** — shartnoma/qonunda belgilangan muddatda, imzo bilan tanishtiriladi.
3. **Buyruq chiqarish** — hujjatlashtirilgan asosga tayanib (HR-TPL-002).
4. **Yakuniy hisob-kitob** — oxirgi ish kunida to'liq to'lanadi (ish haqi, ishlatilmagan ta'til kompensatsiyasi).
5. **Hujjatlarni topshirish** — mehnat daftarchasi/elektron yozuv yangilanadi va xodimga qaytariladi.

## Xatolardan saqlanish
- Asossiz yoki hujjatlashtirilmagan bo'shatish — nizolashuv xavfi eng yuqori nuqta.
- Yakuniy hisob-kitobni kechiktirish qonunbuzarlik hisoblanadi.

---

# 🇬🇧 Employee Termination Procedure (SOP)

## Steps
1. **Document the grounds** — resignation, mutual agreement, or a legal basis, recorded in writing.
2. **Notify the employee** — within the contractual/legal notice period, acknowledged by signature.
3. **Issue the termination order** — based on the documented grounds (HR-TPL-002).
4. **Final settlement** — paid in full on the last working day (wages, unused-leave compensation).
5. **Return documents** — work record / electronic labour entry updated and handed back.

## Mistakes to avoid
- Undocumented or groundless termination carries the highest dispute risk.
- Delaying the final settlement past the last working day is a violation.
