# 🏦 Insure360 AI

Customer Intelligence & Next Best Action Copilot powered by Snowflake Cortex AI, CoCo CLI, Semantic Views, Cortex Agent, and Streamlit in Snowflake.

## 🚀 Overview

Insure360 AI is an AI-powered Customer 360 platform that combines structured and unstructured insurance data to provide actionable customer insights and explainable next best actions.

The solution helps insurance teams:

- Understand customer health
- Analyze customer sentiment
- Review claims and payment history
- Track customer journeys
- Generate AI-powered executive briefs
- Generate AI interaction digests
- Receive explainable Next Best Action recommendations
- Approve or reject recommended actions
- Interact using a grounded Customer Copilot

---

## 🎯 Business Problem

Insurance customer information is often spread across multiple systems, making it difficult for agents to quickly understand customer status and make informed decisions.

Agents frequently switch between policy systems, claims systems, payment systems, and customer interaction records before determining the right customer action.

Insure360 AI centralizes customer intelligence into a single AI-powered decision workspace.

---

## 🏗️ Solution Architecture

### Structured Data

- Customers
- Policies
- Claims
- Payments

### Unstructured Data

- Customer Call Transcripts

### Customer Intelligence Layer

- Customer 360
- Customer Journey Timeline
- Portfolio Dashboard
- Portfolio Analytics

### AI Layer

- Snowflake Cortex AI
- AI Executive Brief
- AI Interaction Digest
- Grounded Customer Copilot
- Semantic View
- Cortex Agent

### Decision Layer

- Next Best Action Engine
- Priority Scoring
- Confidence Scoring
- Business Impact Scoring
- Approval Workflow
- Audit Trail

### Frontend

- Streamlit in Snowflake

---

## ✨ Key Features

### 📊 Portfolio Dashboard

View portfolio-level metrics including:

- Customer health
- Churn risk
- Claims performance
- Payment performance
- Upcoming renewals
- Portfolio KPIs

---

### 📈 Portfolio Analytics

Visual insights into:

- Customer churn distribution
- Claim status distribution
- Payment status distribution
- Renewal pipeline
- Portfolio segmentation

---

### 👤 Customer 360

Unified customer profile including:

- Customer Health Score
- Churn Risk
- Sentiment Analysis
- Lifetime Value
- Policy Information
- Claims History
- Payment History

---

### 📅 Customer Journey Timeline

Complete customer history across:

- Policies
- Claims
- Payments
- Customer Interactions
- Escalations

---

### 🤖 AI Interaction Digest

Generates AI-powered summaries from customer interactions and transcripts to quickly understand customer concerns.

---

### 📋 Executive Brief

Generates executive-level customer summaries including:

- Risk Level
- Priority
- Business Impact
- Revenue Impact
- Recommended Action

---

### 🎯 Next Best Action Engine

Provides explainable recommendations based on deterministic business rules.

Capabilities include:

- Rule-based recommendations
- Priority scoring
- Confidence scoring
- Estimated business impact
- Recommendation reasoning

Example actions:

- Retention Call
- Payment Assistance Plan
- Claim Escalation
- Coverage Review
- Loyalty Recognition

---

### 💬 Grounded Customer Copilot

Natural language interface powered by Snowflake Cortex AI.

Example questions:

- Which customers have high churn risk?
- Show me all platinum customers.
- What is our fraud exposure?
- Which claims require immediate attention?

Responses are grounded using Customer 360 data and protected with anti-hallucination safeguards.

---

### ✅ Action Approval Workflow

Captures approval and rejection of recommendations to ensure governance and accountability.

---

### 🕘 Audit Trail

Tracks:

- Action Approvals
- Action Rejections
- User Actions
- Timestamps
- Action History

---

## 🛠️ Technology Stack

- Snowflake
- Snowflake Cortex AI
- CoCo CLI / Cortex Code
- Semantic View
- Cortex Agent
- Streamlit in Snowflake
- SQL
- Python

---

## 🧠 CoCo CLI Usage

CoCo CLI and Cortex Code were used across the complete solution lifecycle.

### Planning

- Solution architecture design
- Customer 360 design
- Data model exploration

### Development

- SQL artifact generation
- View creation
- Semantic View implementation
- Cortex Agent implementation
- Streamlit application generation

### Validation

- KPI validation
- Business rule validation
- Data quality checks
- Anti-hallucination testing
- Regression testing

### Deployment

- Streamlit deployment
- Runtime troubleshooting
- Compatibility remediation

---

## 📊 Dataset

### Current Portfolio

| Dataset | Count |
|----------|-------|
| Customers | 24 |
| Policies | 34 |
| Claims | 15 |
| Payments | 244 |
| Call Transcripts | 30 |

### Recommendation Metrics

| Metric | Count |
|----------|-------|
| Next Best Actions | 37 |
| Business Rules | 8 |
| Journey Events | 328 |

---

## 📸 Screenshots

### Portfolio Dashboard

screenshots/01_Portfolio_Dashboard.png

### Portfolio Analytics

screenshots/02_Portfolio_Analytics.png

### Customer 360

screenshots/03_Customer360.png

### Customer Journey Timeline

screenshots/04_Customer_Timeline.png

### Next Best Action Engine

screenshots/05_Next_Best_Action.png

### Action Approval & Audit Trail

screenshots/06_Action_Audit.png

### AI Executive Brief

screenshots/07_AI_Executive_Brief.png

### Grounded Customer Copilot

screenshots/08_Customer_Copilot.png

---

## 🏗️ Solution Architecture

docs/SolutionArchitecture.png

---

## 🌟 Business Benefits

- Faster customer understanding
- Explainable recommendations
- Improved customer retention
- Reduced churn risk
- AI-assisted decision making
- Unified customer intelligence
- Better claims visibility
- Improved operational efficiency
- Governance through approval workflows
- Complete auditability

---

## 👨‍💻 Author

Manideep Marka

Built for the Snowflake CoCo CLI Hackathon (GCC Edition).

Powered by Snowflake Cortex AI, CoCo CLI, Semantic Views, Cortex Agent and Streamlit in Snowflake.
