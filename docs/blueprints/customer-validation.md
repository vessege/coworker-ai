# Customer Validation Kit — Accountant MVP

Goal: before building more, confirm 3–5 real Uzbek SMEs/accountants have this
pain and would use (and pay for) the product. Do this in Week 1.

## Who to talk to (5 people)
- SME chief accountants (savdo, xizmat, ishlab chiqarish).
- Sole proprietors (YaTT) who do their own accounting.
- Office managers who handle documents + coordinate with an accountant.
- Outsourced accounting firms (they feel the pain at scale).

## Interview rules
- 20–30 min. Ask about their **real past behaviour**, not hypotheticals.
- Do NOT pitch first. Listen. Pitch only in the last 5 minutes.
- Record: exact words for pains, current tools, what they'd pay.

## Interview questions (uz)
1. Oxirgi marta soliq muddatini o'tkazib yuborganmisiz yoki xavotir olganmisiz? Nima bo'lgan?
2. Hozir muddatlarni qanday eslab qolasiz? (kalendar, buxgalter, telefon, hech narsa?)
3. Bir oyda qancha schyot-faktura / akt tayyorlaysiz? Qancha vaqt ketadi?
4. Hujjat to'ldirishda eng ko'p qaysi xato / bosh og'rig'i bo'ladi?
5. Soliq savoli tug'ilsa kimdan so'raysiz? Qancha kutasiz? Pul to'laysizmi?
6. Hozir qanday dastur/xizmatlardan foydalanasiz? (1C, Didox, my.soliq, Excel?)
7. Agar o'zbekcha savolga manba bilan javob beradigan, hujjat tayyorlaydigan
   AI yordamchi bo'lsa — sinab ko'rasizmi? Nima uchun ha/yo'q?
8. Bunga oyiga qancha to'lardingiz? (jim turing, javobni kuting)

## Signals to look for
| Kuchli signal (davom et) | Zaif signal (qayta o'yla) |
|--------------------------|---------------------------|
| "Ha, o'tkazib yuborganman, jarima to'laganman" | "Yo'q, muammo yo'q" |
| Hozir vaqt/pul sarflayapti | Befarq |
| "Qachon tayyor bo'ladi?" | "Qiziq ekan" (lekin harakat yo'q) |
| Pilotga rozi + kontakt beradi | Narxdan qochadi |

## Demo script (5 min, hozirgi API ustida)
1. **Deadline savol:** `POST /ask` → *"QQS hisobotini qachon topshiraman?"*
   → manba (ACC-FAQ-001) bilan javob. "Har javob manbaga bog'langan, xayolot yo'q."
2. **Hujjat:** `POST /generate` → *"Schyot-faktura tayyorla, sotuvchi ..."*
   → rasmiy formada to'ldirilgan hujjat (ACC-TPL-001).
3. **Xavfsizlik:** mavzudan tashqari savol → "bilmayman, buxgalter bilan tasdiqlang."
   → "AI o'zidan soliq qoidasi to'qimaydi."

## Decision after 5 interviews
- ≥ 3 kuchli signal → 15 ta asst + web UI ga o'tamiz.
- < 3 → scope/roldan qaytamiz (masalan boshqa vazifa yoki rol).

## Log template (har suhbat uchun)
```
Sana / Kim / Biznes turi:
Eng og'riqli gap (aynan so'zlari):
Hozirgi yechim:
To'lashga tayyor summa:
Signal: kuchli / o'rta / zaif
Keyingi qadam:
```
