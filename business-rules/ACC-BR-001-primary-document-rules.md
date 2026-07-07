---
id: ACC-BR-001
title: Primary Document Rules / Birlamchi hujjatlar qoidalari
type: RULE
category: business-rule
domain: accounting
subdomain: primary-documents
department: Finance & Accounting
role: Accountant
summary: IF/THEN rules for issuing and accepting primary accounting documents (EHF, act, contract linkage).
source: VM qarori №522 (EHF); Mehnat/Soliq amaliyoti; ACC-TPL-001/002/003 bilan bog'liq
source_url: https://lex.uz/uz/docs/-4386769
tags: [business-rule, birlamchi-hujjat, EHF, schyot-faktura, akt, IKPU, qoida]
language: [uz, en]
country: UZ
quality: reviewed
status: Approved
confidence: 0.8
owner: CKO / Knowledge Factory
version: 1.0.0
created: '2026-07-07'
updated: '2026-07-07'
last_review: 2026-07-07
valid_from: 2026-01-01
source_verified: 2026-07-07
review_cycle: quarterly
relationships:
- {type: references, target: ACC-TPL-001}
- {type: references, target: ACC-TPL-002}
- {type: references, target: ACC-SOP-001}
---

# 🇺🇿 Birlamchi hujjatlar qoidalari (AGAR → UNDA)

| # | Qoida | Asos |
|---|-------|------|
| BR-1 | AGAR tovar jo'natildi / xizmat ko'rsatildi → UNDA hisobvaraq-faktura **elektron** (EHF) rasmiylashtiriladi — 2020-yildan majburiy. | VM №522 |
| BR-2 | AGAR EHF tuzilmoqda → UNDA sana = tovar jo'natilgan/xizmat ko'rsatilgan kun. | VM №522 |
| BR-3 | AGAR jadval qatori to'ldirilmoqda → UNDA **MXIK (IKPU) kodi majburiy**; Qiymat = Narx × Miqdor. | EHF tartibi |
| BR-4 | AGAR xizmat/ish qabul qilindi → UNDA ikki tomonlama **akt** tuziladi va summalari fakturaga mos bo'ladi. | Amaliyot |
| BR-5 | AGAR hujjat imzolanmoqda → UNDA imzolovchi vakolatli bo'lishi kerak (rahbar/bosh buxgalter/YaTT yoki ishonchnomali xodim). | VM №522 |
| BR-6 | AGAR faktura, akt va shartnoma bitta bitimga tegishli → UNDA ular **bir-biriga havola** qilinadi (shartnoma № va sanasi ko'rsatiladi). | Amaliyot |
| BR-7 | AGAR to'lov korporativ karta orqali bo'lsa → UNDA EHF xaridor so'ragan sanada, lekin **oy oxiridan kechikmay** beriladi. | VM №522 |
| BR-8 | AGAR hisobot davri yopilmoqda → UNDA birlamchi hujjatsiz operatsiya hisobga olinmaydi. | ACC-SOP-001 |

---

# 🇬🇧 Primary Document Rules (IF → THEN)

| # | Rule | Basis |
|---|------|-------|
| BR-1 | IF goods shipped / service rendered → THEN issue the invoice **electronically** (EHF) — mandatory since 2020. | Decree 522 |
| BR-2 | IF creating an EHF → THEN its date = shipment/service date. | Decree 522 |
| BR-3 | IF filling a table row → THEN the **IKPU (MXIK) code is mandatory**; Value = Price × Qty. | EHF procedure |
| BR-4 | IF work/services accepted → THEN a two-party **act** is drawn up, amounts matching the invoice. | Practice |
| BR-5 | IF signing → THEN the signer must be authorized (head/chief accountant/sole proprietor or employee with power of attorney). | Decree 522 |
| BR-6 | IF invoice, act and contract belong to one deal → THEN they **cross-reference** each other (contract No. and date). | Practice |
| BR-7 | IF payment is by corporate card → THEN the EHF is issued by the buyer's requested date, **no later than month-end**. | Decree 522 |
| BR-8 | IF closing the period → THEN no transaction is booked without its primary document. | ACC-SOP-001 |
