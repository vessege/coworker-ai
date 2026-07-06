---
id: OM-BR-001
title: Document Registration & Indexing Rules / Hujjatlarni ro'yxatga olish va indekslash qoidalari
category: business-rule
domain: office-management
source: O'zDSt 1157:2008; umumiy ish yuritish amaliyoti
source_url: https://lex.uz/uz/docs/-5529263; https://standart.uz
tags: [business-rule, ro'yxatga-olish, indeks, hujjat-raqami, nazorat, qoida]
quality: production-ready
language: [uz, en]
country: UZ
version: 1.0.0
last_review: 2026-07-06
---

# 🇺🇿 Hujjatlarni ro'yxatga olish va indekslash qoidalari

Mashina o'qiy oladigan biznes-qoidalar. `AGAR ... UNDA ...` ko'rinishida.

| # | Qoida (AGAR → UNDA) | Asos |
|---|---------------------|------|
| BR-1 | AGAR hujjat tashqaridan kelgan bo'lsa → UNDA u ijrochiga berishdan **oldin** kiruvchi jurnalga ro'yxatga olinadi. | Ish yuritish tartibi |
| BR-2 | AGAR hujjatga chiquvchi raqam kerak bo'lsa → UNDA raqam chiquvchi jurnaldan **ketma-ket va noyob** beriladi; raqam qayta ishlatilmaydi. | O'zDSt 1157:2008 |
| BR-3 | AGAR bir hujjat elektron va qog'ozda mavjud bo'lsa → UNDA ikkalasi **bir xil** ro'yxat raqami ostida bog'lanadi. | Yagona nazorat |
| BR-4 | AGAR hujjat "shaxsan" belgisi bilan kelgan bo'lsa → UNDA konvert ochilmaydi, to'g'ridan-to'g'ri adresatga uzatiladi. | Maxfiylik |
| BR-5 | AGAR hujjatda ijro muddati ko'rsatilmagan bo'lsa → UNDA ichki reglamentdagi standart muddat (odatda 10 ish kuni) qo'llanadi. | Ichki reglament |
| BR-6 | AGAR hujjat fuqaro murojaati bo'lsa → UNDA qonuniy muddatlar va tartib qo'llanadi (alohida SOP). | Murojaatlar qonuni |
| BR-7 | AGAR ijro muddati tugashiga ≤ 1 kun qolgan va hujjat yopilmagan bo'lsa → UNDA ijrochi va rahbarga eslatma yuboriladi. | Ijro nazorati |
| BR-8 | AGAR hujjat ijrosi tugagan bo'lsa → UNDA "ijro etildi" belgisi qo'yiladi va nomenklatura bo'yicha tegishli ishga tikiladi. | Arxivlash tartibi |
| BR-9 | AGAR hujjat adashib kelgan bo'lsa → UNDA ro'yxatga olinmasdan jo'natuvchiga qaytariladi. | Ish yuritish tartibi |

## Indeks (raqam) tarkibi
Tavsiya etilgan format: `[ish indeksi]-[ketma-ket raqam]` (masalan `01-12/45`),
bunda `01-12` — nomenklatura bo'yicha ish indeksi, `45` — jurnal bo'yicha tartib raqami.
Aniq format tashkilotning ish nomenklaturasi bilan belgilanadi.

---

# 🇬🇧 Document Registration & Indexing Rules

Machine-readable business rules in `IF ... THEN ...` form.

| # | Rule (IF → THEN) | Basis |
|---|------------------|-------|
| BR-1 | IF a document arrives from outside → THEN it is registered in the incoming register **before** being handed to an assignee. | Record-keeping order |
| BR-2 | IF a document needs an outgoing number → THEN the number is assigned **sequentially and uniquely** from the outgoing register; numbers are not reused. | O'zDSt 1157:2008 |
| BR-3 | IF a document exists in both electronic and paper form → THEN both are linked under the **same** registration number. | Single point of control |
| BR-4 | IF a document is marked "personal" → THEN the envelope is not opened and it is forwarded directly to the addressee. | Confidentiality |
| BR-5 | IF no execution deadline is stated → THEN the standard internal deadline applies (commonly 10 working days). | Internal regulation |
| BR-6 | IF the document is a citizen's appeal → THEN statutory deadlines and procedure apply (separate SOP). | Law on appeals |
| BR-7 | IF ≤ 1 day remains before the deadline and the document is not closed → THEN a reminder is sent to assignee and manager. | Execution control |
| BR-8 | IF execution is complete → THEN mark "executed" and file it into the correct case per the nomenclature of files. | Archiving order |
| BR-9 | IF a document is misdelivered → THEN it is returned to sender without registration. | Record-keeping order |

## Index (number) composition
Recommended format: `[case index]-[sequential number]` (e.g. `01-12/45`),
where `01-12` is the case index per the nomenclature and `45` is the register
sequence number. The exact format is set by the organization's file nomenclature.
