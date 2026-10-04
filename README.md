For the README of the current CoCo/Cortex-built version, I'd use this:

🏦 Insure360 AI

Unified Customer 360 & Next Best Action Copilot built with Snowflake Cortex AI, CoCo CLI, Semantic Views, Cortex Agent, and Streamlit in Snowflake.

🚀 Overview

Insure360 AI is an intelligent insurance customer engagement platform that unifies structured and unstructured customer information into a single Customer 360 experience.

The solution combines:

Customer data
Policy data
Claims data
Payment history
Customer call transcripts

to help service agents, claims teams, retention specialists, and business stakeholders make faster and more informed decisions.

Using Snowflake Cortex AI and CoCo CLI, the platform generates explainable recommendations, executive summaries, customer insights, and grounded natural-language responses.

🎯 Business Problem

Insurance organizations often struggle with fragmented customer information distributed across policies, claims, payments, and customer interactions.

As a result:

Agents spend time gathering customer context
Customer issues are discovered too late
Retention opportunities are missed
Decisions vary by individual interpretation
Executive reviews require manual preparation

Insure360 AI centralizes customer context, explains customer risk, recommends the next best action, and captures action decisions in a governed workflow.

🏗️ Solution Architecture
Structured Data
Customers
Policies
Claims
Payments
Unstructured Data
Customer Call Transcripts
Customer Intelligence Layer
Customer 360 View
Customer Journey Timeline
Policy Lifecycle Analytics
Claims Workflow Analytics
Portfolio KPI Dashboard
Portfolio Breakdown Analytics
AI Layer
Snowflake Cortex AI
AI Interaction Digest
AI Executive Brief
Grounded Customer Copilot
Semantic View
Cortex Agent
Decision Layer
Explainable Next Best Action Engine
Priority Scoring
Confidence Scoring
Estimated Business Impact
Approval Workflow
Audit Trail
Experience Layer
Streamlit in Snowflake
Portfolio Dashboard
Customer 360
Timeline View
AI Insights
Customer Copilot
✨ Key Features
📊 Portfolio Dashboard

Provides portfolio-level visibility into:

Customer portfolio health
Claims performance
Payment health
Renewal pipeline
Risk indicators
📈 Portfolio Analytics

Interactive visual analytics for:

Customer Churn Risk Distribution
Claims Status Distribution
Payment Status Distribution
Renewal Pipeline Analysis
👤 Customer 360

Unified customer profile including:

Customer Health Score
Churn Risk
Customer Value
Lifetime Value
Policies
Claims
Payments
Customer Engagement
📅 Customer Journey Timeline

Single chronological view of:

Policy Events
Claims Events
Payments
Customer Interactions
Escalations
🎯 Next Best Action Engine

Explainable recommendation framework with:

8 Deterministic Business Rules
Priority Levels
Confidence Scores
Estimated Business Impact
Action Reasoning

Sample actions:

Retention Call with Loyalty Discount
Offer Payment Assistance Plan
Escalate Claim and Send Status Update
Personalized Coverage Review
Loyalty Recognition and Reward
📋 Executive Brief

AI-generated executive summaries including:

Risk Level
Business Impact
Priority
Recommended Action
Revenue / Retention Impact
🤖 AI Interaction Digest

Automatically summarizes customer interaction history by analyzing customer transcripts and identifying:

Customer concerns
Sentiment trends
Escalation patterns
Risk indicators
💬 Grounded Customer Copilot

Natural language interface built using Snowflake Cortex AI.

Example questions:

Which customers have high churn risk?
Show me all platinum customers.
What is our fraud exposure?
Which claims need immediate attention?

Responses are grounded using Customer 360 context and anti-hallucination safeguards.

✅ Action Approval Workflow

Recommended actions can be:

Approved
Rejected
Audited

to maintain governance and explainability.

🕘 Audit Trail

Captures:

Approved Actions
Rejected Actions
User Decisions
Timestamps
Action History
🛠️ Technology Stack
Snowflake
Tables
Views
Stored Procedures
Internal Stages
Streamlit in Snowflake
AI
Snowflake Cortex AI
Semantic Views
Cortex Agent
Grounded AI Responses
Executive Brief Generation
Development
CoCo CLI / Cortex Code
Snowflake AI Assistant
SQL
Python
Streamlit
🧠 CoCo CLI Usage

CoCo CLI and Cortex Code were used across the complete prototype lifecycle.

Planning
Solution Design
Customer 360 Architecture
Data Model Design
Implementation Roadmap
Development
SQL Artifact Generation
View Generation
Semantic View Creation
Cortex Agent Creation
Streamlit Application Generation
Testing & Validation
Referential Integrity Validation
KPI Validation
Business Rule Validation
Anti-Hallucination Testing
Regression Testing
Deployment
Streamlit Deployment
Runtime Troubleshooting
Compatibility Fixes
📊 Dataset
Current Portfolio
Dataset	CountCustomers	24
Policies	34
Claims	15
Payments	244
Call Transcripts	30
Recommendations
Metric	ValueNext Best Actions	37
Business Rules	8
Journey Events	328
📸 Screenshots
Portfolio Dashboard

screenshots/portfolio_dashboard.png

Portfolio Analytics

screenshots/portfolio_analytics.png

Customer 360

screenshots/customer_360.png

Customer Journey Timeline

screenshots/customer_timeline.png

Next Best Action

screenshots/next_best_action.png

Action Approval & Audit Trail

screenshots/action_workflow.png

AI Executive Brief

screenshots/executive_brief.png

Grounded Customer Copilot

screenshots/customer_copilot.png

🌟 Business Benefits
Faster customer understanding
Explainable recommendations
Reduced churn risk
Improved retention outcomes
Better claims visibility
Improved payment recovery
Increased operational consistency
Executive-level customer intelligence
Governed decision-making
Complete auditability
👨‍💻 Author

Manideep Marka

Built for the Snowflake CoCo CLI Hackathon (GCC Edition) using Snowflake Cortex AI, CoCo CLI, Semantic Views, Cortex Agent and Streamlit in Snowflake. 🏆🚀
