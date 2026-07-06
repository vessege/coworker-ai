---
id: ACC-TPL-001
title: Invoice (Schyot-faktura / Hisobvaraq-faktura) / Hisobvaraq-faktura
category: template
domain: accounting
subdomain: primary-documents
source: VM qarori №522, 25.06.2019 (elektron hisobvaraq-fakturalar); moysklad.uz; norma.uz
source_url: https://lex.uz/uz/docs/-4386769; https://www.norma.uz/oz/qonunchilikda_yangi/hisobvaraq-faktura_rasmiylashtirish_taqdim_etish_va_qabul_qilish; https://www.moysklad.uz/uz/poleznoe/formy-dokumentov/schet-faktura-uzbekistan/
tags: [schyot-faktura, hisobvaraq-faktura, EHF, invoice, QQS, birlamchi-hujjat, template]
quality: reviewed
language: [uz, en]
country: UZ
version: 1.0.0
valid_from: 2026-07-01
source_verified: 2026-07-06
last_review: 2026-07-06
review_cycle: quarterly
related: [ACC-KA-001, ACC-TPL-002]
---

> ⚠️ O'zbekistonda hisobvaraq-faktura **2020-yildan majburiy elektron shaklda** (EHF)
> soliq axborot tizimi orqali rasmiylashtiriladi. Quyidagi shablon — **maydonlar
> tuzilmasi** (matn/tayyorgarlik uchun); yakuniy hujjat rasmiy tizimda (my.soliq.uz /
> Didox va sh.k.) ERI bilan tasdiqlanadi. Aniq formani soliq.uz da tekshiring.

# 🇺🇿 Hisobvaraq-faktura — maydonlar tuzilmasi

## Sarlavha qismi
| Maydon | Qiymat |
|--------|--------|
| Hisobvaraq-faktura № | `[raqam]` |
| Sana | `[KK.OO.YYYY]` (tovar jo'natilgan / xizmat ko'rsatilgan sana) |
| Shartnoma | `[shartnoma № va sana]` |
| **Sotuvchi** | nomi, manzili, **STIR**, QQS ro'yxat kodi, h/r, bank, MFO |
| **Xaridor** | nomi, manzili, **STIR**, QQS ro'yxat kodi, h/r, bank, MFO |

## Jadval qismi
| № | Tovar/xizmat nomi | MXIK (IKPU) kodi | O'lchov birligi | Miqdor | Narx (QQSsiz) | Qiymat (QQSsiz) | QQS stavkasi | QQS summasi | Jami (QQS bilan) |
|---|-------------------|------------------|-----------------|--------|---------------|-----------------|--------------|-------------|-------------------|
| 1 | `[...]` | `[...]` | `[dona/kg/...]` | `[...]` | `[...]` | `[...]` | `[12%/0%/...]` | `[...]` | `[...]` |
| | **Jami** | | | | | `[∑]` | | `[∑]` | `[∑]` |

## Imzolar
- Tashkilot rahbari: `[F.I.Sh.]` _______ (ERI)
- Bosh buxgalter: `[F.I.Sh.]` _______ (ERI)
- Yoki YaTT / ishonchnomaga ega vakolatli xodim.

## To'ldirish qoidalari
- **Sana** = tovar jo'natilgan yoki xizmat ko'rsatilgan kun.
- **MXIK (IKPU)** — tovar/xizmatning yagona identifikatsiya kodi (majburiy).
- **QQS stavkasi** faoliyat/rejimga bog'liq; QQS to'lovchi bo'lmasangiz alohida tartib.
- Har bir qatorda: Qiymat = Narx × Miqdor; QQS summasi = Qiymat × stavka.

---

# 🇬🇧 Invoice (Schyot-faktura) — field structure

## Header section
| Field | Value |
|-------|-------|
| Invoice No. | `[number]` |
| Date | `[DD.MM.YYYY]` (date goods shipped / service rendered) |
| Contract | `[contract No. and date]` |
| **Seller** | name, address, **tax ID (STIR)**, VAT reg. code, account, bank, MFO |
| **Buyer** | name, address, **tax ID (STIR)**, VAT reg. code, account, bank, MFO |

## Table section
| # | Item/service | IKPU (MXIK) code | Unit | Qty | Price (excl. VAT) | Value (excl. VAT) | VAT rate | VAT amount | Total (incl. VAT) |
|---|--------------|------------------|------|-----|-------------------|-------------------|----------|------------|-------------------|
| 1 | `[...]` | `[...]` | `[pcs/kg/...]` | `[...]` | `[...]` | `[...]` | `[12%/0%/...]` | `[...]` | `[...]` |
| | **Total** | | | | | `[∑]` | | `[∑]` | `[∑]` |

## Signatures
- Head of organization: `[Full name]` _______ (e-signature)
- Chief accountant: `[Full name]` _______ (e-signature)
- Or sole proprietor / authorized employee with power of attorney.

## Fill-in rules
- **Date** = day goods were shipped or the service was rendered.
- **IKPU (MXIK)** = the unified identification code of the item/service (mandatory).
- **VAT rate** depends on activity/regime; a separate procedure applies if you are not a VAT payer.
- Per row: Value = Price × Qty; VAT amount = Value × rate.
