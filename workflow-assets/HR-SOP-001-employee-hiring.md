---
id: HR-SOP-001
title: Employee Hiring & Formalization / Xodimni ishga qabul qilish va rasmiylashtirish
type: SOP
category: workflow-asset
domain: hr
subdomain: hiring
department: Human Resources
role: HR
summary: Legally compliant hiring procedure under the 2023 Labour Code — documents, written contract, order, records.
source: Mehnat kodeksi (30.04.2023); srsl.uz kadrlar ish yuritish qo'llanmasi
source_url: https://lex.uz/mact/-6257288
tags: [ishga-qabul, hiring, mehnat-shartnomasi, buyruq, kadrlar, SOP]
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
valid_from: 2023-04-30
source_verified: 2026-07-07
review_cycle: semiannual
relationships:
- {type: requires, target: HR-KA-001}
- {type: produces, target: HR-TPL-001}
- {type: references, target: OM-CHK-001}
workflow:
  business_goal: Hire and formalize an employee in full compliance with the 2023 Labour Code.
  difficulty: Medium
  estimated_duration: 1-2 working days
  automation_score: 55
  required_inputs: [Candidate documents, Approved staffing table position, Contract template]
  expected_outputs: [Signed employment contract (2 copies), Hiring order, Personnel record]
  success_criteria: [Written contract signed before work starts, Probation within legal limits, Order issued and acknowledged]
  failure_conditions: [Work started without a written contract, Probation over 3 months (6 for heads/chief accountant), Missing mandatory documents]
  approval_points: [Director signs the contract and hiring order]
  kpis: [Time-to-formalize, Compliance error rate]
  steps:
  - {number: 1, title: Collect documents, actor: HR Specialist, ai_capability: Suggest,
     required_docs: [Passport/ID, Diploma if required, Employment history], 
     expected_result: Complete candidate file, validation_rule: Only legally allowed documents are requested}
  - {number: 2, title: Draft the employment contract, actor: AI Assistant, ai_capability: Draft,
     required_docs: [Contract template], expected_result: Contract draft with position, pay, probation,
     validation_rule: Probation <=3 months (<=6 for heads/chief accountant)}
  - {number: 3, title: Sign the contract, actor: Director, ai_capability: Observe,
     required_docs: [], expected_result: Written contract in 2 copies before work starts,
     validation_rule: Each party keeps one signed copy}
  - {number: 4, title: Issue the hiring order, actor: HR Specialist, ai_capability: Draft,
     required_docs: [Signed contract], expected_result: Order (buyruq) issued and acknowledged by signature,
     validation_rule: Order matches contract terms}
  - {number: 5, title: Register in records, actor: HR Specialist, ai_capability: Automate,
     required_docs: [], expected_result: Entry in personnel records / electronic labour book,
     validation_rule: Record created on or before start date}
  - {number: 6, title: Hand over to onboarding, actor: HR Specialist, ai_capability: Suggest,
     required_docs: [], expected_result: Office-manager onboarding started (OM-CHK-001),
     validation_rule: Onboarding checklist assigned}
---

> ⚠️ Axborot xarakterida; huquqiy tafsilotlarni lex.uz va yuristingiz bilan tasdiqlang.

# 🇺🇿 Xodimni ishga qabul qilish va rasmiylashtirish (SOP)

## Bosqichlar
1. **Hujjatlarni yig'ish** — pasport/ID, ma'lumot (lavozim talab qilsa), mehnat daftarchasi. Qonunda nazarda tutilmagan hujjat talab qilinmaydi.
2. **Shartnoma loyihasi** — lavozim, ish haqi, sinov muddati (≤3 oy; rahbar/bosh buxgalter ≤6 oy).
3. **Imzolash** — yozma, **2 nusxa**, ish boshlashdan **oldin**; bir nusxa xodimda qoladi.
4. **Buyruq chiqarish** — shartnoma asosida; xodim imzo bilan tanishadi (HR-TPL-001).
5. **Ro'yxatga olish** — kadrlar hisobi / elektron mehnat daftarchasi.
6. **Onboardingga topshirish** — ofis-menejer checklisti (OM-CHK-001) ishga tushadi.

## Xatolardan saqlanish
- Shartnomasiz ishga chiqarish — eng katta xato (jarima xavfi).
- Sinov muddatini shartnomada yozmasangiz — sinov yo'q hisoblanadi.

---

# 🇬🇧 Employee Hiring & Formalization (SOP)

## Steps
1. **Collect documents** — passport/ID, diploma (if the position requires), employment history. Do not request documents not allowed by law.
2. **Draft the contract** — position, pay, probation (≤3 months; heads/chief accountant ≤6).
3. **Sign** — written, **2 copies**, **before** work starts; the employee keeps one.
4. **Issue the hiring order** — based on the contract; acknowledged by signature (HR-TPL-001).
5. **Register** — personnel records / electronic labour book.
6. **Hand over to onboarding** — office-manager checklist (OM-CHK-001) starts.

## Mistakes to avoid
- Letting work start without a signed contract is the top violation (fine risk).
- Probation not written into the contract = no probation at all.
