"""Set curated one-line summaries (RFC-0002) per asset id. Idempotent."""

from __future__ import annotations

from pathlib import Path

import frontmatter

ROOT = Path(__file__).resolve().parents[1]

SUMMARIES = {
    "ACC-KA-001": "Recurring monthly, quarterly and annual tax reporting and payment deadlines for legal entities.",
    "ACC-KA-002": "Uzbek SME tax regimes: simplified turnover tax vs general (VAT + profit tax), thresholds, and how to choose.",
    "ACC-KA-003": "Key 2026 Uzbek tax rates: VAT 12%, profit 15%, turnover 4%/1%, sole-proprietor social tax.",
    "ACC-KA-004": "Penalties for late tax filing and payment, including 2026 small-business relief.",
    "ACC-FAQ-001": "Common questions on Uzbek tax filing and payment deadlines.",
    "ACC-FAQ-002": "Common questions on Uzbek tax rates and regime selection.",
    "ACC-SOP-001": "Step-by-step monthly accounting close and tax-reporting procedure.",
    "ACC-TPL-001": "Field structure of the Uzbek electronic VAT invoice (schyot-faktura) per decree No.522.",
    "ACC-TPL-002": "Template for a two-party act of completed works/services.",
    "ACC-TPL-003": "General service contract (shartnoma) template for Uzbek SMEs.",
    "ACC-DT-001": "Decision tree for choosing between the turnover-tax and general tax regimes.",
    "ACC-GLO-001": "Bilingual glossary of Uzbek accounting and tax terms.",
    "OM-SOP-001": "Procedure for registering and routing incoming documents (record-keeping).",
    "OM-TPL-001": "Template for an official outgoing business letter per O'zDSt 1157:2008.",
    "OM-CHK-001": "Office-manager checklist for coordinating new-employee onboarding.",
    "OM-BR-001": "IF/THEN business rules for document registration and indexing.",
    "OM-GLO-001": "Bilingual glossary of office-management and record-keeping terms.",
}


def main() -> None:
    n = 0
    for md in ROOT.glob("*/*.md"):
        if md.name.lower() == "readme.md":
            continue
        post = frontmatter.load(md)
        aid = str(post.metadata.get("id", ""))
        if aid in SUMMARIES:
            post.metadata["summary"] = SUMMARIES[aid]
            md.write_text(frontmatter.dumps(post) + "\n")
            n += 1
    print(f"Updated {n} summaries.")


if __name__ == "__main__":
    main()
