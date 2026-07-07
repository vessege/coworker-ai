---
category: decision-tree
confidence: 0.8
country: UZ
created: '2026-01-01'
department: Finance & Accounting
domain: accounting
id: ACC-DT-001
language:
- uz
- en
last_review: 2026-07-06
owner: CKO / Knowledge Factory
quality: reviewed
relationships:
- target: ACC-KA-002
  type: related_to
- target: ACC-KA-003
  type: related_to
review_cycle: quarterly
role: Accountant
source: ACC-KA-002 asosida (buxgalter.uz; azma.uz)
source_url: https://buxgalter.uz/oz/publish/doc/text212722_sk-2026_yakka_tartibdagi_tadbirkorlar_va_uzini_uzi_band_qilgan_shahslar_uchun_aylanmadan_olinadigan_soliq_buyicha_uzgarishlar
source_verified: 2026-07-06
status: Approved
subdomain: tax-regimes
summary: Decision tree for choosing between the turnover-tax and general tax regimes.
tags:
- decision-tree
- soliq-rejimi
- aylanma-soliq
- QQS
- umumiy-rejim
- tanlov
title: Tax Regime Selection Decision Tree / Soliq rejimini tanlash qaror daraxti
type: DECISION
updated: '2026-07-06'
valid_from: 2026-01-01
version: 1.0.0
---

> ⚠️ Bu daraxt yo'naltiruvchi. Yakuniy qarorni buxgalter va soliq.uz bilan tasdiqlang.

# 🇺🇿 Soliq rejimini tanlash — qaror daraxti

```
1. Aksiz mahsuloti / foydali qazilma / davlat ulushi bormi?
   ├─ HA  → Umumiy rejim (QQS 12% + foyda solig'i 15%). Chegara qo'llanmaydi.
   └─ YO'Q → 2-savolga o'ting

2. Yillik aylanmangiz chegaradan oshadimi?
   (YaTT: 1 mlrd; yuridik shaxs: 5 mlrd — 2026, soliq.uz da tasdiqlang)
   ├─ HA  → Umumiy rejim (QQS + foyda solig'i)
   └─ YO'Q → 3-savolga o'ting

3. Mijozlaringiz QQSli hisobvaraq-faktura talab qiladimi?
   ├─ HA  → Umumiy rejim afzalroq (ixtiyoriy QQS ro'yxati)
   └─ YO'Q → 4-savolga o'ting

4. Siz YaTT/o'zini-o'zi band qilganmisiz?
   ├─ HA  → Aylanma soliq 1% (≤1 mlrd) + oyiga 1 BHM ijtimoiy soliq
   └─ YO'Q (yuridik shaxs) → Aylanma soliq 4% (bazaviy)
```

## Natijalar qisqacha
- **Umumiy rejim:** QQS 12% + foyda solig'i 15%. QQS hisobvaraq-fakturalar, murakkabroq hisobot.
- **Aylanma soliq (soddalashtirilgan):** yuridik shaxs 4%, YaTT 1%. Soddaroq, choraklik hisobot.

---

# 🇬🇧 Tax Regime Selection — Decision Tree

```
1. Excise goods / minerals / state share involved?
   ├─ YES → General regime (VAT 12% + profit tax 15%). Threshold N/A.
   └─ NO  → go to 2

2. Does annual turnover exceed the threshold?
   (sole proprietor: 1 bln; legal entity: 5 bln — 2026, verify on soliq.uz)
   ├─ YES → General regime (VAT + profit tax)
   └─ NO  → go to 3

3. Do your clients require VAT invoices?
   ├─ YES → General regime is preferable (voluntary VAT registration)
   └─ NO  → go to 4

4. Are you a sole proprietor / self-employed?
   ├─ YES → Turnover tax 1% (≤1 bln) + 1 base amount/month social tax
   └─ NO (legal entity) → Turnover tax 4% (base)
```

## Outcomes in brief
- **General regime:** VAT 12% + profit tax 15%. VAT invoices, more complex reporting.
- **Turnover tax (simplified):** legal entity 4%, sole proprietor 1%. Simpler, quarterly reporting.
