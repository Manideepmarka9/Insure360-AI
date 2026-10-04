"""
INSURE360 AI — Streamlit-in-Snowflake Application (Hackathon-Final)
File: insure360_app.py
Purpose: Multi-page dashboard for Insurance Customer 360
Deploy: CREATE STREAMLIT in INSURANCE_C360.C360
"""

import streamlit as st
import json
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="Insure360 AI", layout="wide")
session = get_active_session()

# ── Sidebar Navigation ──────────────────────────────────────
st.sidebar.title("Insure360 AI")
st.sidebar.markdown("Insurance Customer 360 Platform")
page = st.sidebar.radio("Navigate", [
    "Portfolio Dashboard",
    "Customer 360",
    "Customer Timeline",
    "Next Best Action",
    "AI Insights",
    "Customer Copilot",
])

# ── Helpers ──────────────────────────────────────────────────
def run_query(sql):
    return session.sql(sql).to_pandas()

def color_badge(label, color):
    colors = {
        "green": "#16a34a", "amber": "#d97706", "red": "#dc2626",
        "blue": "#2563eb", "purple": "#7c3aed", "gray": "#6b7280",
        "platinum": "#6b7280", "gold": "#d97706", "silver": "#94a3b8", "bronze": "#b45309"
    }
    bg = colors.get(color, "#6b7280")
    return f'<span style="background:{bg};color:white;padding:2px 10px;border-radius:12px;font-weight:600;font-size:0.85em">{label}</span>'

def safe_int(val, default=0):
    try:
        import math
        if val is None or (isinstance(val, float) and math.isnan(val)):
            return default
        return int(val)
    except (ValueError, TypeError):
        return default

def safe_float(val, default=0.0):
    try:
        import math
        if val is None or (isinstance(val, float) and math.isnan(val)):
            return default
        return float(val)
    except (ValueError, TypeError):
        return default

def safe_str(val, default="Unknown"):
    if val is None:
        return default
    s = str(val)
    if s in ("nan", "NaN", "None", ""):
        return default
    return s

def health_bar(score):
    score = safe_float(score, 0.0)
    if score >= 70:
        color = "#16a34a"
    elif score >= 40:
        color = "#d97706"
    else:
        color = "#dc2626"
    pct = min(score, 100)
    return f'''<div style="background:#e5e7eb;border-radius:8px;height:22px;width:100%;position:relative">
<div style="background:{color};border-radius:8px;height:22px;width:{pct}%;display:flex;align-items:center;justify-content:center">
<span style="color:white;font-size:0.75em;font-weight:700">{score:.0f}/100</span>
</div></div>'''

def churn_badge(risk):
    cmap = {"LOW": "green", "MEDIUM": "amber", "HIGH": "red", "CHURNED": "gray"}
    return color_badge(risk, cmap.get(risk, "gray"))

def sentiment_indicator(val):
    val = safe_float(val, 0.0)
    if val > 0.3:
        return color_badge(f"Positive ({val:.2f})", "green")
    elif val >= -0.3:
        return color_badge(f"Neutral ({val:.2f})", "amber")
    else:
        return color_badge(f"Negative ({val:.2f})", "red")

def segment_badge(seg):
    cmap = {"PLATINUM": "platinum", "GOLD": "gold", "SILVER": "silver", "BRONZE": "bronze"}
    return color_badge(seg, cmap.get(seg, "gray"))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE 1: PORTFOLIO DASHBOARD
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if page == "Portfolio Dashboard":
    st.title("Portfolio Dashboard")
    kpi = run_query("SELECT * FROM INSURANCE_C360.C360.V_PORTFOLIO_KPI")

    if kpi.empty:
        st.warning("No portfolio data available.")
    else:
        row = kpi.iloc[0]

        st.subheader("Customer & Policy Overview")
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total Customers", safe_int(row["TOTAL_CUSTOMERS"]))
        c2.metric("Active Policies", safe_int(row["ACTIVE_POLICIES"]))
        c3.metric("Gross Written Premium", f"${safe_float(row['GROSS_WRITTEN_PREMIUM']):,.0f}")
        c4.metric("Avg NPS", f"{safe_float(row['AVG_NPS_SCORE']):.1f}")
        c5.metric("Renewal Pipeline", safe_int(row["POLICIES_IN_RENEWAL_WINDOW"]))

        st.subheader("Claims & Risk")
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total Claims", safe_int(row["TOTAL_CLAIMS"]))
        c2.metric("Open Claims", safe_int(row["OPEN_CLAIMS"]))
        c3.metric("Loss Ratio", f"{safe_float(row['LOSS_RATIO_PCT']):.1f}%")
        c4.metric("Avg Days to Settle", f"{safe_float(row['AVG_DAYS_TO_SETTLE']):.0f}")
        c5.metric("SIU Referrals", safe_int(row["SIU_REFERRALS"]))

        st.subheader("Payments & Customer Engagement")
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Premiums Collected", f"${safe_float(row['PREMIUMS_COLLECTED']):,.0f}")
        c2.metric("On-Time Payment Rate", f"{safe_float(row['PAYMENT_ON_TIME_RATE_PCT']):.1f}%")
        c3.metric("Avg Sentiment", f"{safe_float(row['AVG_SENTIMENT']):.3f}")
        c4.metric("Avg CSAT", f"{safe_float(row['AVG_CSAT']):.1f}")
        c5.metric("Escalations", safe_int(row["ESCALATIONS"]))

        # Portfolio Breakdown Charts
        breakdowns = run_query("SELECT * FROM INSURANCE_C360.C360.V_PORTFOLIO_BREAKDOWN")

        bd1, bd2 = st.columns(2)
        with bd1:
            st.subheader("Customer Churn Risk Distribution")
            churn = breakdowns[breakdowns["DIMENSION"] == "CHURN_RISK_DISTRIBUTION"][["CATEGORY", "ITEM_COUNT", "TOTAL_PREMIUM"]].copy()
            churn.columns = ["Churn Risk", "Customers", "Premium at Risk ($)"]
            risk_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
            churn["_sort"] = churn["Churn Risk"].map(risk_order)
            churn = churn.sort_values("_sort").drop(columns=["_sort"])
            st.bar_chart(churn.set_index("Churn Risk")["Customers"])
            st.dataframe(churn.reset_index(drop=True), use_container_width=True)

        with bd2:
            st.subheader("Claims Status Distribution")
            claims = breakdowns[breakdowns["DIMENSION"] == "CLAIMS_STATUS"][["CATEGORY", "ITEM_COUNT", "TOTAL_PREMIUM"]].copy()
            claims.columns = ["Status", "Count", "Total Amount ($)"]
            claims = claims.sort_values("Count", ascending=False)
            st.bar_chart(claims.set_index("Status")["Count"])
            st.dataframe(claims.reset_index(drop=True), use_container_width=True)

        bd3, bd4 = st.columns(2)
        with bd3:
            st.subheader("Payment Status Distribution")
            pay = breakdowns[breakdowns["DIMENSION"] == "PAYMENT_STATUS"][["CATEGORY", "ITEM_COUNT", "TOTAL_PREMIUM"]].copy()
            pay.columns = ["Status", "Count", "Total Amount ($)"]
            st.bar_chart(pay.set_index("Status")["Count"])
            st.dataframe(pay.reset_index(drop=True), use_container_width=True)

        with bd4:
            st.subheader("Renewal Pipeline")
            ren = breakdowns[breakdowns["DIMENSION"] == "RENEWAL_PIPELINE"][["CATEGORY", "ITEM_COUNT", "TOTAL_PREMIUM"]].copy()
            ren.columns = ["Expiry Window", "Policies", "Premium at Risk ($)"]
            st.bar_chart(ren.set_index("Expiry Window")["Policies"])
            st.dataframe(ren.reset_index(drop=True), use_container_width=True)

        st.subheader("Customer Segment Distribution")
        seg = run_query("""
            SELECT CUSTOMER_SEGMENT, COUNT(*) AS CUSTOMER_COUNT,
                   ROUND(AVG(CUSTOMER_HEALTH_SCORE), 1) AS AVG_HEALTH,
                   ROUND(AVG(LIFETIME_VALUE), 0) AS AVG_LTV,
                   SUM(TOTAL_ANNUAL_PREMIUM) AS TOTAL_PREMIUM
            FROM INSURANCE_C360.C360.V_CUSTOMER_360
            GROUP BY CUSTOMER_SEGMENT ORDER BY TOTAL_PREMIUM DESC
        """)
        st.dataframe(seg.reset_index(drop=True), use_container_width=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE 2: CUSTOMER 360 (Enhanced with visual indicators)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "Customer 360":
    st.title("Customer 360 Profile")

    customers = run_query("""
        SELECT CUSTOMER_ID, FULL_NAME, CUSTOMER_SEGMENT, CHURN_RISK
        FROM INSURANCE_C360.C360.V_CUSTOMER_360 ORDER BY FULL_NAME
    """)
    options = {f"{r['FULL_NAME']} ({r['CUSTOMER_ID']}) -- {r['CUSTOMER_SEGMENT']}": r["CUSTOMER_ID"]
               for _, r in customers.iterrows()}
    selected = st.selectbox("Select Customer", list(options.keys()))

    if selected:
        cid = options[selected]
        cust = run_query(f"SELECT * FROM INSURANCE_C360.C360.V_CUSTOMER_360 WHERE CUSTOMER_ID = '{cid}'")
        if not cust.empty:
            r = cust.iloc[0]

            # Visual indicator header
            st.markdown("#### Status Indicators")
            ic1, ic2, ic3, ic4 = st.columns(4)
            with ic1:
                st.markdown("**Health Score**")
                st.markdown(health_bar(r['CUSTOMER_HEALTH_SCORE']), unsafe_allow_html=True)
            with ic2:
                st.markdown("**Churn Risk**")
                st.markdown(churn_badge(r['CHURN_RISK']), unsafe_allow_html=True)
            with ic3:
                st.markdown("**Sentiment**")
                st.markdown(sentiment_indicator(r['AVG_SENTIMENT']), unsafe_allow_html=True)
            with ic4:
                st.markdown("**Customer Value**")
                st.markdown(segment_badge(r['CUSTOMER_SEGMENT']), unsafe_allow_html=True)

            st.markdown("---")

            # Key metrics
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Health Score", f"{safe_float(r['CUSTOMER_HEALTH_SCORE']):.0f}/100")
            c2.metric("Lifetime Value", f"${safe_float(r['LIFETIME_VALUE']):,.0f}")
            c3.metric("Active Policies", safe_int(r["ACTIVE_POLICIES"]))
            c4.metric("Annual Premium", f"${safe_float(r['TOTAL_ANNUAL_PREMIUM']):,.0f}")
            c5.metric("NPS", safe_int(r["NPS_SCORE"]))

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Demographics")
                st.write(f"**Email:** {safe_str(r['EMAIL'])}")
                st.write(f"**Location:** {safe_str(r['CITY'])}, {safe_str(r['STATE'])} {safe_str(r['ZIP_CODE'])}")
                st.write(f"**Age:** {safe_int(r['AGE'])} | **Tenure:** {safe_int(r['CUSTOMER_TENURE_MONTHS'])} months")
                st.write(f"**Segment:** {safe_str(r['CUSTOMER_SEGMENT'])} | **Preferred Contact:** {safe_str(r['PREFERRED_CONTACT'])}")

                st.subheader("Policy Summary")
                st.write(f"**Types:** {safe_str(r['POLICY_TYPES_HELD'])}")
                st.write(f"**Multi-line:** {'Yes' if r['IS_MULTI_LINE'] else 'No'}")
                st.write(f"**Upcoming Renewals:** {safe_int(r['UPCOMING_RENEWALS'])}")

            with col2:
                st.subheader("Claims Summary")
                st.write(f"**Total Claims:** {safe_int(r['TOTAL_CLAIMS'])} | **Open:** {safe_int(r['OPEN_CLAIMS'])}")
                st.write(f"**Total Claimed:** ${safe_float(r['TOTAL_CLAIMED']):,.0f}")
                st.write(f"**Paid:** ${safe_float(r['TOTAL_CLAIMS_PAID']):,.0f}")
                st.write(f"**Fraud Flags:** {safe_int(r['FRAUD_FLAGS'])} (Score: {safe_float(r['MAX_FRAUD_SCORE'])})")

                st.subheader("Engagement")
                st.write(f"**Interactions (90d):** {safe_int(r['INTERACTIONS_LAST_90D'])}")
                st.write(f"**Avg Sentiment:** {safe_float(r['AVG_SENTIMENT']):.2f}")
                st.write(f"**Escalations:** {safe_int(r['ESCALATION_COUNT'])}")
                st.write(f"**Payment Reliability:** {safe_float(r['PAYMENT_RELIABILITY_PCT'])}%")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE 3: CUSTOMER TIMELINE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "Customer Timeline":
    st.title("Customer Journey Timeline")

    customers = run_query("SELECT DISTINCT CUSTOMER_ID FROM INSURANCE_C360.C360.V_CUSTOMER_JOURNEY ORDER BY CUSTOMER_ID")
    cid = st.selectbox("Select Customer ID", customers["CUSTOMER_ID"].tolist())

    if cid:
        name_row = run_query(f"SELECT FIRST_NAME || ' ' || LAST_NAME AS NAME FROM INSURANCE_C360.C360.CUSTOMERS WHERE CUSTOMER_ID = '{cid}'")
        if not name_row.empty:
            st.subheader(f"Timeline for {name_row.iloc[0]['NAME']} ({cid})")

        categories = ["All", "POLICY", "CLAIM", "PAYMENT", "INTERACTION"]
        cat_filter = st.multiselect("Filter by Category", categories, default=["All"])

        where_clause = f"WHERE CUSTOMER_ID = '{cid}'"
        if "All" not in cat_filter and cat_filter:
            cat_list = ",".join([f"'{c}'" for c in cat_filter])
            where_clause += f" AND EVENT_CATEGORY IN ({cat_list})"

        events = run_query(f"""
            SELECT EVENT_DATE, EVENT_CATEGORY, EVENT_TYPE, EVENT_DESCRIPTION,
                   COALESCE(SENTIMENT_SCORE::VARCHAR, '-') AS SENTIMENT
            FROM INSURANCE_C360.C360.V_CUSTOMER_JOURNEY
            {where_clause} ORDER BY EVENT_DATE DESC
        """)

        if events.empty:
            st.info("No events found for this customer.")
        else:
            st.dataframe(events, use_container_width=True, height=500)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE 4: NEXT BEST ACTION (Enhanced with business-friendly names)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "Next Best Action":
    st.title("Next Best Action Queue")
    st.caption("Deterministic rule-based recommendations -- not AI-generated")

    col1, col2, col3 = st.columns(3)
    with col1:
        priority_filter = st.selectbox("Max Priority", [1, 2, 3, 4, 5], index=4)
    with col2:
        category_options = ["All", "RETENTION", "GROWTH", "SERVICE", "RISK_MITIGATION"]
        cat_filter = st.selectbox("Category", category_options)
    with col3:
        segment_options = ["All", "PLATINUM", "GOLD", "SILVER", "BRONZE"]
        seg_filter = st.selectbox("Segment", segment_options)

    where_parts = [f"PRIORITY <= {priority_filter}"]
    if cat_filter != "All":
        where_parts.append(f"CATEGORY = '{cat_filter}'")
    if seg_filter != "All":
        where_parts.append(f"CUSTOMER_SEGMENT = '{seg_filter}'")

    nba = run_query(f"""
        SELECT CUSTOMER_ID, FULL_NAME, CUSTOMER_SEGMENT, ACTION_LABEL,
               PRIORITY, CONFIDENCE, RULE_ID, CATEGORY, ESTIMATED_IMPACT, REASONING
        FROM INSURANCE_C360.C360.V_NEXT_BEST_ACTION
        WHERE {' AND '.join(where_parts)}
        ORDER BY PRIORITY ASC, CONFIDENCE DESC
    """)

    st.metric("Total Actions", len(nba))
    if not nba.empty:
        st.dataframe(nba, use_container_width=True, height=400)

        st.subheader("Take Action")
        action_idx = st.number_input("Row # to act on (0-based)", min_value=0,
                                      max_value=max(0, len(nba)-1), value=0)
        if action_idx < len(nba):
            sa = nba.iloc[action_idx]
            st.info(f"**{sa['ACTION_LABEL']}** for {sa['FULL_NAME']}\n\n"
                    f"**Impact:** {sa['ESTIMATED_IMPACT']}\n\n{sa['REASONING']}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Approve", type="primary"):
                    action_id = f"ACT-{sa['CUSTOMER_ID']}-{sa['RULE_ID']}"
                    session.sql(f"""
                        CALL INSURANCE_C360.C360.SP_NBA_ACTION(
                            '{action_id}', '{sa['CUSTOMER_ID']}',
                            '{sa['ACTION_LABEL'][:50].replace("'", "''")}', '{sa['RULE_ID']}',
                            '{sa['REASONING'][:500].replace("'", "''")}',
                            'APPROVED', {sa['PRIORITY']}, {sa['CONFIDENCE']},
                            '{sa['CATEGORY']}', 'PHONE',
                            CURRENT_USER(), CURRENT_USER(), NULL, 'Approved via Insure360 AI'
                        )
                    """).collect()
                    st.success(f"Action {action_id} approved!")
            with col2:
                reject_reason = st.text_input("Rejection reason")
                if st.button("Reject"):
                    action_id = f"ACT-{sa['CUSTOMER_ID']}-{sa['RULE_ID']}"
                    session.sql(f"""
                        CALL INSURANCE_C360.C360.SP_NBA_ACTION(
                            '{action_id}', '{sa['CUSTOMER_ID']}',
                            '{sa['ACTION_LABEL'][:50].replace("'", "''")}', '{sa['RULE_ID']}',
                            '{sa['REASONING'][:500].replace("'", "''")}',
                            'REJECTED', {sa['PRIORITY']}, {sa['CONFIDENCE']},
                            '{sa['CATEGORY']}', 'PHONE',
                            CURRENT_USER(), CURRENT_USER(),
                            '{reject_reason.replace("'", "''")}', 'Rejected via Insure360 AI'
                        )
                    """).collect()
                    st.warning(f"Action {action_id} rejected.")

    st.subheader("Action Audit History")
    audit = run_query("""
        SELECT ACTION_ID, CUSTOMER_ID, ACTION_TYPE, STATUS, PRIORITY,
               ASSIGNED_TO, APPROVED_BY, CREATED_AT, UPDATED_AT
        FROM INSURANCE_C360.C360.NBA_ACTIONS ORDER BY UPDATED_AT DESC LIMIT 50
    """)
    if audit.empty:
        st.info("No actions taken yet.")
    else:
        st.dataframe(audit, use_container_width=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE 5: AI INSIGHTS (Enhanced executive brief display)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "AI Insights":
    st.title("AI-Powered Insights")
    st.warning("Content below is **AI-generated advisory** -- verify before action.")

    customers = run_query("SELECT CUSTOMER_ID, FULL_NAME FROM INSURANCE_C360.C360.V_CUSTOMER_360 ORDER BY FULL_NAME")
    options = {f"{r['FULL_NAME']} ({r['CUSTOMER_ID']})": r["CUSTOMER_ID"]
               for _, r in customers.iterrows()}
    selected = st.selectbox("Select Customer", list(options.keys()))

    if selected:
        cid = options[selected]

        st.subheader("Executive Brief")
        brief = run_query(f"""
            SELECT CUSTOMER_ID, FULL_NAME, CUSTOMER_SEGMENT, CHURN_RISK,
                   CUSTOMER_HEALTH_SCORE, RISK_LEVEL, PRIORITY_TIER,
                   REVENUE_IMPACT, AI_EXECUTIVE_BRIEF, DISCLAIMER
            FROM INSURANCE_C360.C360.V_AI_EXECUTIVE_BRIEF
            WHERE CUSTOMER_ID = '{cid}'
        """)
        if not brief.empty:
            b = brief.iloc[0]

            # Structured header cards
            hc1, hc2, hc3, hc4 = st.columns(4)
            risk_color = {"HIGH": "red", "MEDIUM": "amber", "LOW": "green"}.get(b["RISK_LEVEL"], "gray")
            priority_color = {"URGENT": "red", "HIGH": "amber", "MODERATE": "blue", "LOW": "green"}.get(b["PRIORITY_TIER"], "gray")
            hc1.markdown(f"**Risk Level:** {color_badge(b['RISK_LEVEL'], risk_color)}", unsafe_allow_html=True)
            hc2.markdown(f"**Priority:** {color_badge(b['PRIORITY_TIER'], priority_color)}", unsafe_allow_html=True)
            hc3.markdown(f"**Revenue Impact:** {b['REVENUE_IMPACT']}")
            hc4.markdown(f"**Health Score:** {b['CUSTOMER_HEALTH_SCORE']}/100")

            st.markdown("---")
            st.markdown(b["AI_EXECUTIVE_BRIEF"])
            st.caption(b["DISCLAIMER"])
        else:
            st.info("No executive brief available.")

        st.subheader("Interaction Digest")
        digest = run_query(f"""
            SELECT AI_INTERACTION_DIGEST, INTERACTION_COUNT, AVG_SENTIMENT,
                   LAST_INTERACTION, DISCLAIMER
            FROM INSURANCE_C360.C360.V_AI_CUSTOMER_INTERACTION_DIGEST
            WHERE CUSTOMER_ID = '{cid}'
        """)
        if not digest.empty:
            d = digest.iloc[0]
            c1, c2, c3 = st.columns(3)
            c1.metric("Interactions", safe_int(d["INTERACTION_COUNT"]))
            c2.metric("Avg Sentiment", f"{safe_float(d['AVG_SENTIMENT']):.3f}")
            c3.metric("Last Contact", str(d["LAST_INTERACTION"])[:10])
            st.markdown(d["AI_INTERACTION_DIGEST"])
            st.caption(d["DISCLAIMER"])
        else:
            st.info("No interaction history for this customer.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE 6: CUSTOMER COPILOT (Grounded via Cortex Complete)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "Customer Copilot":
    st.title("Customer Copilot")
    st.caption("Ask questions about customers, policies, claims, and recommendations. "
               "Grounded in verified data — answers are generated from real Customer 360 queries.")

    @st.cache_data(ttl=300)
    def get_grounding_context():
        ctx = run_query("""
            SELECT
                (SELECT COUNT(*) FROM INSURANCE_C360.C360.CUSTOMERS) AS TOTAL_CUSTOMERS,
                (SELECT COUNT(*) FROM INSURANCE_C360.C360.V_CUSTOMER_360 WHERE CHURN_RISK = 'HIGH') AS HIGH_RISK,
                (SELECT COUNT(*) FROM INSURANCE_C360.C360.V_CUSTOMER_360 WHERE CHURN_RISK = 'MEDIUM') AS MED_RISK,
                (SELECT COUNT(*) FROM INSURANCE_C360.C360.V_NEXT_BEST_ACTION) AS NBA_COUNT
        """)
        cust = run_query("""
            SELECT CUSTOMER_ID, FULL_NAME, CUSTOMER_SEGMENT, CHURN_RISK,
                   CUSTOMER_HEALTH_SCORE, TOTAL_ANNUAL_PREMIUM, LIFETIME_VALUE,
                   ACTIVE_POLICIES, POLICY_TYPES_HELD, TOTAL_CLAIMS, OPEN_CLAIMS,
                   FRAUD_FLAGS, MAX_FRAUD_SCORE, AVG_SENTIMENT, PAYMENT_RELIABILITY_PCT
            FROM INSURANCE_C360.C360.V_CUSTOMER_360
        """)
        nba = run_query("""
            SELECT CUSTOMER_ID, FULL_NAME, ACTION_LABEL, PRIORITY, CONFIDENCE,
                   ESTIMATED_IMPACT, CATEGORY
            FROM INSURANCE_C360.C360.V_NEXT_BEST_ACTION
            ORDER BY PRIORITY ASC, CONFIDENCE DESC
        """)
        return ctx, cust, nba

    ctx, cust_df, nba_df = get_grounding_context()
    cust_text = cust_df.to_string(index=False, max_rows=10)
    nba_text = nba_df.to_string(index=False, max_rows=15)

    grounding_prompt = (
        'You are Insure360 AI, a grounded insurance analytics assistant. '
        'You MUST answer ONLY from the data provided below. '
        'If the question cannot be answered from this data, respond: '
        '"I can only answer questions about our insurance customer data — '
        'customer profiles, policies, claims, payments, interactions, and next-best-action recommendations. '
        'This question falls outside the scope of our Customer 360 platform." '
        'NEVER fabricate, guess, or provide information not present in the data. '
        'When presenting data, include Customer ID and Name. Format numbers with $, %, or counts.\n\n'
        'CUSTOMER 360 DATA:\n' + cust_text + '\n\n'
        'NEXT BEST ACTIONS:\n' + nba_text + '\n\n'
    )

    if "copilot_history" not in st.session_state:
        st.session_state.copilot_history = []

    # Display conversation history
    for msg in st.session_state.copilot_history:
        role_label = "You" if msg["role"] == "user" else "Insure360 AI"
        if msg["role"] == "user":
            st.markdown(f"**{role_label}:** {msg['content']}")
        else:
            st.info(f"**{role_label}:**\n\n{msg['content']}")

    # Input area using compatible widgets
    st.markdown("---")
    user_input = st.text_area("Ask Insure360 AI a question:", height=80, key="copilot_input")
    ask_col, clear_col = st.columns([1, 1])
    ask_clicked = ask_col.button("Ask", type="primary", key="copilot_ask")
    clear_clicked = clear_col.button("Clear History", key="copilot_clear")

    if clear_clicked:
        st.session_state.copilot_history = []
        st.info("Conversation history cleared.")

    if ask_clicked and user_input and user_input.strip():
        st.session_state.copilot_history.append({"role": "user", "content": user_input.strip()})
        st.markdown(f"**You:** {user_input.strip()}")

        with st.spinner("Querying Insure360 AI..."):
            try:
                safe_input = user_input.strip().replace("'", "''")
                safe_prompt = grounding_prompt.replace("'", "''")
                result = session.sql(f"""
                    SELECT SNOWFLAKE.CORTEX.COMPLETE(
                        'llama3.1-70b',
                        '{safe_prompt}User question: {safe_input}'
                    ) AS RESPONSE
                """).to_pandas()
                response = result.iloc[0]["RESPONSE"]
                st.info(f"**Insure360 AI:**\n\n{response}")
                st.caption("Grounded in Customer 360 data. AI-generated — verify before action.")
                st.session_state.copilot_history.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown("---")
    st.subheader("Suggested Questions")
    quick_qs = [
        "Which customers have high churn risk?",
        "What are the most urgent next best actions?",
        "What is our fraud exposure?",
        "Show me all platinum customers",
        "Which customers need a coverage review?",
    ]
    cols = st.columns(len(quick_qs))
    for i, q in enumerate(quick_qs):
        if cols[i].button(q, key=f"qq_{i}"):
            st.session_state.copilot_history.append({"role": "user", "content": q})
            st.markdown(f"**You:** {q}")
            with st.spinner("Querying Insure360 AI..."):
                try:
                    safe_input = q.replace("'", "''")
                    safe_prompt = grounding_prompt.replace("'", "''")
                    result = session.sql(f"""
                        SELECT SNOWFLAKE.CORTEX.COMPLETE(
                            'llama3.1-70b',
                            '{safe_prompt}User question: {safe_input}'
                        ) AS RESPONSE
                    """).to_pandas()
                    response = result.iloc[0]["RESPONSE"]
                    st.info(f"**Insure360 AI:**\n\n{response}")
                    st.caption("Grounded in Customer 360 data. AI-generated — verify before action.")
                    st.session_state.copilot_history.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error: {e}")
