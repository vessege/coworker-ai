# CoWorker AI — RFC Pack (0001–0007)

> Source of truth for the knowledge architecture. RFC-0002 is adopted; see docs/blueprints/mvp-accountant.md for the phased roadmap.

RFC-0001 — Knowledge Factory Identity

Identity

You are not a chatbot.

You are the Chief Knowledge Officer (CKO) of the CoWorker AI project.

Your only responsibility is to continuously transform high-quality public knowledge into
structured enterprise knowledge that can improve CoWorker AI.

You never answer like ChatGPT.

You never produce long essays.

You never generate unnecessary explanations.

Everything you produce must become reusable knowledge for CoWorker AI.

---

Mission

Your mission is to build the world's highest quality enterprise knowledge factory.

Every document you process must increase one or more of these assets:

- Company Brain
- Workflow Library
- Knowledge Objects
- Templates
- Checklists
- Best Practices
- Training Dataset

If your output cannot improve one of these assets, it should not be produced.

---

Long-term Goal

The final objective is not to answer users.

The final objective is to create the world's best AI coworker for businesses.

Everything you create today will eventually be used to train CoWorker Foundation Models.

---

Core Philosophy

Knowledge is more valuable than text.

Workflow is more valuable than knowledge.

Experience is more valuable than workflow.

Company DNA is more valuable than experience.

Every processed document must move upward through these layers.

---

Absolute Rules

Never hallucinate.

Never invent workflows.

Never create fake templates.

Never produce duplicated knowledge.

Never lose the original source.

Always preserve traceability.

Always prefer structured output over natural language.

Always think as a knowledge engineer, never as a chatbot.
RFC-0002 — Knowledge Asset Standard (KAS) v1.0

Status

Draft

Owner

CoWorker AI Architecture Team

Purpose

This RFC defines the canonical structure of every Knowledge Asset (KA) inside the
CoWorker AI ecosystem.

Knowledge Assets are the fundamental building blocks of Company Brain, Knowledge
Factory, Workflow Engine, Memory Engine, RAG, and future CoWorker Foundation Models.

This standard is mandatory for every AI worker participating in the Knowledge Factory.

---

1. Design Philosophy

CoWorker AI is not building a document database.

CoWorker AI is building reusable business knowledge.

Every Knowledge Asset must satisfy the following principles.

1.1 Atomic

A Knowledge Asset must describe exactly one business concept.

Good:

- Employee Onboarding
- Monthly Tax Report
- Customer Invoice Approval

Bad:

- Everything about HR
- Accounting Guide
- Company Management

---

1.2 Business-Oriented

Every asset must solve a real business task.

Technology itself is not knowledge.

Example:

Bad:
How SMTP works.

Good:
How to send customer invoices automatically via email.

---

1.3 Reusable

Every asset should be reusable by:

- Chat Assistant
- Manager Agent
- Accountant Agent
- HR Agent
- Company Brain
- Workflow Engine
- Future Foundation Models

---

1.4 Traceable

Every fact must have a verifiable source.

No orphan knowledge is allowed.

---

1.5 Versioned

Knowledge evolves.

Every asset must maintain version history.

---

1.6 Composable

Multiple Knowledge Assets should combine into:

Workflow

↓

Department Knowledge

↓

Company Brain

---

1.7 Human-Centered

Every asset must answer one question:

"What business activity becomes easier because of this knowledge?"

If no answer exists, reject the asset.

---

2. Knowledge Asset Types

Every asset belongs to exactly one primary type.

FACT

A verified business fact.

RULE

A business rule or regulation.

WORKFLOW

A sequence of business actions.

SOP

Standard Operating Procedure.

CHECKLIST

Step verification list.

TEMPLATE

Reusable business template.

POLICY

Company or legal policy.

DECISION

Decision-making guidance.

BEST_PRACTICE

Industry recommendations.

FAQ

Frequently asked business questions.

---

3. Asset Metadata

Every Knowledge Asset MUST contain:

- Asset ID
- Title
- Type
- Department
- Business Role
- Country
- Language
- Summary
- Content
- Tags
- Source
- Version
- Confidence Score
- Owner
- Created Date
- Updated Date
- Last Reviewed Date

---

4. Semantic Relationships

Knowledge Assets are connected.

Supported relationships include:

requires

references

depends_on

uses

produces

extends

updates

replaces

related_to

This enables Company Brain to become a Knowledge Graph rather than a collection of
isolated documents.

---

5. Knowledge Hierarchy

CoWorker searches knowledge using the following priority:

Level 1

Company Knowledge

↓

Level 2

Uzbekistan Business Knowledge

↓

Level 3

Global Business Knowledge

Global knowledge never overrides company knowledge.

---

6. Quality Requirements

Every asset receives an automatic quality evaluation.

Metrics:

Accuracy

Completeness

Freshness

Business Relevance

Traceability

Reusability

Clarity

Overall Quality Score

Assets scoring below the minimum quality threshold must be returned to Knowledge Factory
for revision.

---

7. Asset Lifecycle

Draft

↓

Review

↓

Approved

↓

Published

↓

Deprecated

↓

Archived

Only Approved or Published assets may be used by Company Brain.

---

8. Source Policy

Preferred sources:

Government documentation

Official vendor documentation

International standards

Product manuals

Academic publications

Verified industry documentation

Avoid:

Random blogs

Forum opinions

Unverified AI-generated content

Social media posts

---

9. Business First Rule

Knowledge is evaluated from a business perspective.

Bad examples:

"What is SQL JOIN?"

"What is SMTP?"

"What is JSON?"

Good examples:

"Generate monthly sales report."

"Prepare VAT declaration."

"Create employee onboarding checklist."

"Approve purchase request."

The objective is to improve business execution, not teach programming.

---

10. Company DNA Compatibility

Every Knowledge Asset should support future Company DNA generation.

Whenever possible identify:

Communication Style

Decision Style

Approval Chain

Reporting Style

Meeting Style

Risk Level

Organizational Behavior

These attributes will later become Company DNA.

---

11. Future Compatibility

Knowledge Assets must remain compatible with:

Company Brain

Workflow Engine

Memory Engine

Knowledge Graph

RAG

Agent System

Fine-tuning Dataset

Foundation Models

No asset should depend on a specific LLM vendor.

The standard must remain model-agnostic.

---

12. Acceptance Rule

Before publishing any Knowledge Asset, validate the following question:

"Does this asset help a real employee complete a real business task faster, better, or with
fewer mistakes?"

If the answer is NO,

the asset MUST NOT enter Company Brain.

---

Final Principle

CoWorker AI does not collect documents.

CoWorker AI creates business knowledge assets.

Knowledge is not the final product.

Better business execution is the final product.

RFC-0003 — Workflow Asset Standard (WAS) v1.0

Status

Draft

Owner

CoWorker AI Architecture Team

Purpose

This RFC defines the canonical structure of Workflow Assets (WA) inside the CoWorker AI
ecosystem.

A Workflow Asset represents how work is performed.

Knowledge explains.

Workflow executes.

CoWorker AI exists to execute work, not merely explain it.

---

1. Design Philosophy

A Workflow Asset is not documentation.

It is an executable representation of business work.

Every workflow should be understandable by:

• Humans

• AI Agents

• Workflow Engine

• Future CoWorker Foundation Models

---

2. Core Principles

Task-Oriented

Every workflow starts with a business task.

Examples:

Prepare monthly payroll.

Approve purchase request.

Hire a new employee.

Register a new supplier.

Generate VAT report.

---

Outcome-Oriented

Every workflow must produce a measurable outcome.

Bad:

Read accounting guide.

Good:

Generate completed payroll report.

---

Atomic

Each workflow solves only one business process.

Complex business operations must be divided into multiple workflows.

---

Reusable

The same workflow should be reusable across companies whenever possible.

Company-specific customization must be layered on top rather than modifying the base
workflow.

---

Observable

Every step should produce an observable result.

Hidden actions are prohibited.

---

Human-in-the-loop

AI assists.

AI automates.

AI recommends.

Humans approve critical decisions.

---

3. Workflow Structure

Every Workflow Asset contains:

Workflow ID

Title

Business Goal

Department

Business Role

Difficulty

Estimated Duration

Required Inputs

Workflow Steps

Expected Outputs

Success Criteria

Failure Conditions

Dependencies

Related Knowledge Assets

Related Templates

Automation Opportunities

Approval Points

KPIs

Version

Owner

---

4. Workflow Steps

Each workflow consists of ordered steps.

Each step contains:

Step Number

Step Title

Description

Required Knowledge

Required Documents

Responsible Actor

Estimated Time

Possible AI Actions

Expected Result

Validation Rule

---

5. Actors

Every workflow identifies who performs each step.

Supported actors include:

Human Employee

Manager

Accountant

HR Specialist

Director

Customer

Government System

External Service

AI Assistant

AI Agent

---

6. AI Capabilities

Each step must classify AI involvement.

Possible values:

Observe

Suggest

Draft

Automate

Execute

Review

Escalate

AI should never exceed the permitted capability defined for that step.

---

7. Decision Points

Business processes contain decisions.

Every decision node must define:

Condition

Possible Outcomes

Responsible Person

AI Recommendation Logic

Escalation Rule

---

8. Inputs

Inputs may include:

Knowledge Assets

Documents

Forms

Company Policies

External APIs

ERP Data

Accounting Data

CRM Data

Human Instructions

---

9. Outputs

Outputs may include:

Reports

Emails

Invoices

Meeting Minutes

Payroll Files

Checklists

Company Records

Knowledge Updates

Completed Tasks

---

10. Automation Score

Every workflow receives an automation score.

0%
Fully Human

100%
Fully Autonomous

Most enterprise workflows are expected to remain partially automated.

---

11. Workflow Lifecycle

Draft

↓

Simulation

↓

Internal Review

↓

Approved

↓

Production

↓

Deprecated

↓

Archived

Only Approved workflows may execute inside Company Brain.

---

12. Company DNA Integration

Each workflow learns:

Preferred communication style

Approval sequence

Meeting habits

Risk tolerance

Document preferences

Business culture

Over time workflows adapt to each company.

---

13. Success Metrics

Each workflow defines measurable KPIs.

Examples:

Execution Time

Approval Time

Error Rate

Manual Work Reduced

Automation Percentage

Customer Satisfaction

Compliance Rate

---

14. Workflow Relationships

Workflow Assets may:

Require other workflows

Call sub-workflows

Update Knowledge Assets

Generate Templates

Trigger AI Agents

Update Company Brain

---

15. Future Compatibility

Workflow Assets must remain compatible with:

Workflow Engine

Company Brain

Knowledge Graph

Memory Engine

Agent Orchestrator

Foundation Models

No workflow may depend on a specific AI provider.

---

Final Principle

Knowledge tells people what to do.

Workflow tells CoWorker how to work.

The purpose of CoWorker AI is not to answer questions.

The purpose of CoWorker AI is to complete business work.

RFC-0004 — Task Asset Standard (TAS) v1.0

Status

Draft

Owner

CoWorker AI Architecture Team

Purpose

This RFC defines the Task Asset (TA), the executable work unit of the CoWorker AI
ecosystem.

Knowledge Assets define what is known.

Workflow Assets define how work is performed.

Task Assets define what must be completed now.

Every interaction with CoWorker AI ultimately becomes one or more Task Assets.

---

1. Design Principles

Task-Driven

Every Task Asset represents a real business objective.

A task must always have a clear outcome.

Examples:

Prepare weekly report.

Analyze uploaded contracts.

Generate customer proposal.

Review employee CVs.

Create meeting summary.

---

Time-Bound

Every task exists within a time context.

Tasks may include:

Deadline

Priority

Estimated duration

Execution status

---

Context-Aware

A task is never isolated.

Every task may reference:

Company Knowledge

Knowledge Assets

Workflow Assets

Company DNA

Uploaded Documents

Previous Tasks

Conversation Context

---

Human-Centered

AI performs work.

Humans remain responsible for business decisions.

Approval points must always be respected.

---

2. Task Metadata

Every Task Asset contains:

Task ID

Title

Description

Business Goal

Role

Department

Priority

Status

Deadline

Estimated Time

Requester

Assigned Agent

Related Workflow

Related Knowledge

Related Documents

Expected Deliverables

Success Criteria

Failure Conditions

Version

Created At

Updated At

---

3. Task States

Created

↓

Planned

↓

Running

↓

Waiting

↓

Review

↓

Completed

↓

Archived

Cancelled tasks remain available for learning purposes.

---

4. Task Priority

Critical

High

Normal

Low

Background

Priority influences planning but never overrides approval rules.

---

5. Deliverables

Every task must define expected outputs.

Examples:

Executive Summary

Business Report

Email Draft

Checklist

Presentation

Spreadsheet

Meeting Minutes

Risk Analysis

Knowledge Update

---

6. AI Execution

AI may perform:

Planning

Reading

Analyzing

Summarizing

Comparing

Writing

Generating

Suggesting

Validating

Escalating

AI must never execute actions beyond its assigned permissions.

---

7. Learning Rule

Every completed Task Asset becomes a learning opportunity.

The system should automatically generate:

Workflow improvements

Knowledge updates

Training samples

Quality metrics

Future automation opportunities

No completed task should be discarded.

---

8. Company DNA Integration

Tasks continuously reveal company behavior.

The system should learn:

Preferred writing style

Approval behavior

Meeting habits

Reporting preferences

Communication patterns

Business terminology

These observations contribute to Company DNA.

---

9. Future Compatibility

Task Assets must remain compatible with:

Workflow Engine

Knowledge Graph

Memory Engine

Agent System

Company Brain

Foundation Models

No task definition may depend on a specific AI provider.

---

Final Principle

Knowledge explains.

Workflow organizes.

Task executes.

CoWorker AI exists to complete business tasks efficiently, consistently, and safely.

RFC-0005 — Memory Engine Standard (MES) v1.0

Status

Draft

Purpose

This RFC defines how memory is stored, organized, updated and retrieved inside the
CoWorker AI ecosystem.

Memory is not conversation history.

Memory is structured organizational intelligence.

---

Core Principles

Memory exists to improve future work.

Every stored memory must have future value.

If information cannot improve future execution, it should not become memory.

---

Memory Types

Working Memory

Temporary information required to complete the current task.

Characteristics:

- Short lifetime
- Task-specific
- Automatically discarded after completion unless promoted.

---

Session Memory

Stores context produced during one work session.

Examples:

Documents opened

Reports generated

Questions answered

Decisions made

---

Company Memory

Persistent organizational memory.

Examples:

Policies

Standard procedures

Department rules

Reporting preferences

Approved templates

Business terminology

Company Memory changes only after validation.

---

Learning Memory

Generated automatically after completed tasks.

Contains:

Successful workflows

Common mistakes

Execution statistics

Reusable solutions

Automation opportunities

Learning Memory continuously improves CoWorker AI.

---

Memory Lifecycle

Capture

↓

Validate

↓

Classify

↓

Store

↓

Retrieve

↓

Update

↓

Archive

---

Promotion Rules

Not every piece of information becomes permanent memory.

Promotion requires one of:

Repeated usage

Explicit user approval

Administrative approval

Verified business importance

Otherwise information remains temporary.

---

Retrieval Priority

1. Working Memory

2. Company Memory

3. Learning Memory

4. Global Knowledge

Conversation history should never have higher priority than Company Memory.

---

Memory Quality

Each memory item maintains:

Confidence

Freshness

Source

Owner

Version

Usage Frequency

Validation Status

---

Security

Memory belongs to the company.

Memory must never leak across tenants.

Every memory item inherits company access permissions.

---

Future Compatibility

Memory Engine must integrate with:

Knowledge Assets

Workflow Assets

Task Assets

Company Brain

Knowledge Graph

Agent System

Foundation Models

---

Final Principle

CoWorker AI should not remember everything.

CoWorker AI should remember only what makes the company work better.

RFC-0006 — Company DNA Standard (CDS) v1.0

Status

Draft

Owner

CoWorker AI Architecture Team

Purpose

This RFC defines the Company DNA system inside the CoWorker AI ecosystem.

Company DNA represents the unique operational identity of a company.

It is not documentation.

It is not memory.

It is the behavioral model that explains how a company works.

Company DNA allows CoWorker AI to adapt to each organization instead of forcing
organizations to adapt to AI.

---

1. Core Philosophy

Every company operates differently.

Different approval chains.

Different reporting styles.

Different communication styles.

Different decision-making processes.

Different cultures.

The objective of Company DNA is to learn these differences automatically.

---

2. Design Principles

Adaptive

Company DNA evolves continuously.

It is never static.

---

Evidence-Based

Every DNA trait must originate from observed company behavior.

No assumptions are allowed.

---

Explainable

Every learned preference must include evidence explaining why it exists.

---

Non-Intrusive

Company DNA must never modify company behavior.

It adapts to the company.

---

Tenant-Isolated

Every company owns its own DNA.

No DNA information may cross company boundaries.

---

3. Company DNA Domains

The DNA model consists of independent domains.

Communication DNA

Preferred tone

Preferred language

Preferred email structure

Greeting style

Closing style

Response length

Internal communication style

External communication style

---

Document DNA

Preferred report format

Preferred templates

Document naming conventions

Brand terminology

Writing conventions

Approval formatting

---

Workflow DNA

Approval sequence

Task assignment behavior

Meeting routines

Escalation paths

Review patterns

Automation preferences

---

Decision DNA

Decision makers

Approval thresholds

Risk tolerance

Exception handling

Delegation patterns

---

Organizational DNA

Departments

Hierarchy

Business units

Internal vocabulary

Business abbreviations

Team structure

---

Performance DNA

KPIs

Reporting cadence

Preferred dashboards

Review frequency

Success metrics

---

4. DNA Learning Sources

Company DNA may only learn from:

Approved documents

Approved workflows

Completed tasks

Validated meetings

Explicit administrator settings

Confirmed user corrections

Conversation history alone is insufficient evidence.

---

5. Confidence Model

Each DNA trait stores:

Confidence Score

Observation Count

First Observed

Last Observed

Supporting Evidence

Review Status

DNA evolves as confidence increases.

---

6. DNA Lifecycle

Observe

↓

Validate

↓

Learn

↓

Apply

↓

Monitor

↓

Update

↓

Retire

---

7. Safety Rules

AI must never invent company behavior.

If confidence is below the required threshold:

Ask the user.

Never guess.

---

8. Company Adaptation

The AI should gradually personalize:

Reports

Emails

Meeting summaries

Task execution

Recommendations

Document generation

Approval flows

without requiring manual configuration whenever reliable evidence exists.

---

9. Future Compatibility

Company DNA integrates with:

Knowledge Assets

Workflow Assets

Task Assets

Memory Engine

Knowledge Graph

Agent Engine

Foundation Models

Company Brain

---

10. Business Rule

Company DNA exists to reduce organizational friction.

The objective is not personalization for convenience.

The objective is operational consistency across the organization.

---

Final Principle

Knowledge teaches the AI.

Workflows organize the AI.

Memory preserves the AI.

Company DNA transforms the AI into a true digital coworker that works like a member of the
company rather than an external assistant.

RFC-0007 — Capability & Enterprise Knowledge Graph (CEKG) v1.0

Status

Draft

Purpose

This RFC defines how CoWorker AI understands relationships between knowledge,
workflows, tasks, company memory, company DNA, and AI capabilities.

The Enterprise Knowledge Graph is the reasoning layer of CoWorker AI.

Capabilities are the execution layer.

Together they transform isolated information into executable organizational intelligence.

---

Core Philosophy

Knowledge alone cannot execute work.

Capabilities alone cannot reason.

The Enterprise Knowledge Graph connects business knowledge.

Capabilities perform business actions.

Both are required.

---

Enterprise Knowledge Graph

The graph connects all organizational assets.

Supported node types:

Knowledge Assets

Workflow Assets

Task Assets

Memory

Company DNA

Documents

Departments

Business Roles

People

Projects

Meetings

Templates

Policies

Business Rules

External Systems

Every relationship must be explicit.

---

Supported Relationships

requires

references

depends_on

produces

updates

uses

belongs_to

assigned_to

created_from

validated_by

approved_by

related_to

Relationships must be directional and traceable.

---

Capability Engine

Capabilities describe what CoWorker AI can perform.

Examples:

Read PDF

Read DOCX

Read XLSX

OCR

Search Knowledge

Generate Report

Generate Email

Compare Documents

Risk Analysis

Meeting Summarization

Template Generation

Workflow Planning

Knowledge Extraction

Translation

Reasoning

Tool Execution

API Integration

Future capabilities may be added without changing existing architecture.

---

Capability Selection

Every task should automatically determine:

Required Knowledge

Required Workflow

Required Memory

Required Company DNA

Required Capabilities

Only the minimum required capabilities should execute.

---

Reasoning Process

Task

↓

Knowledge Graph Retrieval

↓

Memory Retrieval

↓

Workflow Selection

↓

Capability Planning

↓

Execution

↓

Validation

↓

Learning

---

Graph Update Rules

Every completed task may create:

New relationships

New workflow statistics

New business terminology

New company preferences

New reusable knowledge

The graph continuously evolves.

---

Security

Every graph node inherits tenant permissions.

Cross-company relationships are prohibited.

Capabilities execute only within assigned permissions.

---

Future Compatibility

The Enterprise Knowledge Graph integrates with:

Knowledge Assets

Workflow Assets

Task Assets

Memory Engine

Company DNA

Agent Engine

Knowledge Factory

Foundation Models

---

Final Principle

The Enterprise Knowledge Graph decides what should happen.

Capabilities decide what can happen.

Agents decide what will happen.

Together they form the operational intelligence of CoWorker AI.
