"""Apply the RFC-0003 (Workflow Asset Standard) structured `workflow` block to
WORKFLOW/SOP assets. Machine-parseable spec in front-matter; the bilingual prose
body stays for humans. Idempotent. Run from repo root.
"""

from __future__ import annotations

from pathlib import Path

import frontmatter

ROOT = Path(__file__).resolve().parents[1]

WORKFLOWS: dict[str, dict] = {
    "OM-SOP-001": {
        "business_goal": "Register and route every incoming document without loss and track it to completion.",
        "difficulty": "Low",
        "estimated_duration": "5-15 min per document",
        "automation_score": 60,
        "required_inputs": ["Incoming document (paper/electronic)", "Incoming register or EDMS access"],
        "expected_outputs": ["Registered document with unique incoming number", "Routing to assignee", "Execution record"],
        "success_criteria": ["Unique incoming number assigned", "Assignee and deadline recorded", "Execution closed and filed"],
        "failure_conditions": ["Document routed before registration", "Duplicate number assigned", "Deadline missed without reminder"],
        "approval_points": ["Manager writes the resolution (assignee + deadline)"],
        "kpis": ["Registration time", "% overdue documents", "Lost-document rate"],
        "steps": [
            {"number": 1, "title": "Receive", "actor": "Office Manager", "ai_capability": "Observe",
             "required_docs": ["Incoming document"], "expected_result": "Document accepted; integrity checked",
             "validation_rule": "Items marked 'personal' are not opened"},
            {"number": 2, "title": "Initial review", "actor": "Office Manager", "ai_capability": "Suggest",
             "required_docs": ["Incoming document"], "expected_result": "Belongs to org and attachments present",
             "validation_rule": "Misdelivered items returned to sender, not registered"},
            {"number": 3, "title": "Register", "actor": "Office Manager", "ai_capability": "Automate",
             "required_docs": ["Incoming register / EDMS"], "expected_result": "Unique incoming number + register entry",
             "validation_rule": "Number is sequential and unique"},
            {"number": 4, "title": "Present to manager", "actor": "Office Manager", "ai_capability": "Draft",
             "required_docs": [], "expected_result": "Manager receives registered document",
             "validation_rule": "Only registered documents are presented"},
            {"number": 5, "title": "Record resolution", "actor": "Manager", "ai_capability": "Observe",
             "required_docs": [], "expected_result": "Assignee and deadline captured",
             "validation_rule": "Resolution must name assignee and deadline"},
            {"number": 6, "title": "Hand over to assignee", "actor": "Office Manager", "ai_capability": "Execute",
             "required_docs": [], "expected_result": "Assignee receives document against signature",
             "validation_rule": "Handover is logged"},
            {"number": 7, "title": "Execution control", "actor": "AI Assistant", "ai_capability": "Automate",
             "required_docs": [], "expected_result": "Reminder sent before deadline",
             "validation_rule": "Reminder fires when <=1 day remains"},
            {"number": 8, "title": "Close execution", "actor": "Office Manager", "ai_capability": "Review",
             "required_docs": [], "expected_result": "Marked executed and filed per nomenclature",
             "validation_rule": "Cannot close without execution mark"},
        ],
    },
    "ACC-SOP-001": {
        "business_goal": "Close the accounting month error-free and file all tax reports by their deadlines.",
        "difficulty": "Medium",
        "estimated_duration": "1-3 working days per month",
        "automation_score": 45,
        "required_inputs": ["Invoices, acts, bank statements", "Payroll data", "Personal cabinet (my.soliq.uz) access"],
        "expected_outputs": ["Reconciled ledgers", "Filed tax declarations", "Payment confirmations", "Archived documents"],
        "success_criteria": ["All primary documents collected", "Reports match primary documents", "Filed by deadline"],
        "failure_conditions": ["Report prepared without primary documents", "Filing >5 working days late", "Amounts not reconciled"],
        "approval_points": ["Chief accountant reviews before filing"],
        "kpis": ["On-time filing rate", "Reconciliation error rate", "Days to close"],
        "steps": [
            {"number": 1, "title": "Collect primary documents", "actor": "Accountant", "ai_capability": "Automate",
             "required_docs": ["Invoices", "Acts", "Bank statements"], "expected_result": "Complete document set",
             "validation_rule": "No report without primary documents"},
            {"number": 2, "title": "Reconcile", "actor": "Accountant", "ai_capability": "Review",
             "required_docs": ["Bank statements", "Counterparty records"], "expected_result": "Balances reconciled",
             "validation_rule": "Bank and cash balances match"},
            {"number": 3, "title": "Payroll & contributions", "actor": "Accountant", "ai_capability": "Draft",
             "required_docs": ["Payroll data"], "expected_result": "Wages and contributions calculated",
             "validation_rule": "Social contributions register prepared"},
            {"number": 4, "title": "Calculate taxes", "actor": "Accountant", "ai_capability": "Suggest",
             "required_docs": [], "expected_result": "VAT / profit / turnover amounts computed",
             "validation_rule": "Rates match ACC-KA-003"},
            {"number": 5, "title": "Prepare reports", "actor": "Accountant", "ai_capability": "Draft",
             "required_docs": ["Personal cabinet"], "expected_result": "Declarations filled",
             "validation_rule": "All required declarations present"},
            {"number": 6, "title": "Review", "actor": "Accountant", "ai_capability": "Review",
             "required_docs": [], "expected_result": "Amounts verified against primary documents",
             "validation_rule": "Report totals equal ledger totals"},
            {"number": 7, "title": "File & pay", "actor": "Accountant", "ai_capability": "Execute",
             "required_docs": [], "expected_result": "Filed and paid by deadline",
             "validation_rule": "Deadlines per ACC-KA-001; never >5 working days late"},
            {"number": 8, "title": "Archive", "actor": "AI Assistant", "ai_capability": "Automate",
             "required_docs": [], "expected_result": "Documents and reports stored",
             "validation_rule": "Retention period respected"},
        ],
    },
}


def main() -> None:
    n = 0
    for md in ROOT.glob("*/*.md"):
        post = frontmatter.load(md)
        aid = str(post.metadata.get("id", ""))
        if aid in WORKFLOWS:
            post.metadata["workflow"] = WORKFLOWS[aid]
            md.write_text(frontmatter.dumps(post) + "\n")
            n += 1
            print(f"  applied RFC-0003 to {aid}")
    print(f"Done. {n} workflow assets structured.")


if __name__ == "__main__":
    main()
