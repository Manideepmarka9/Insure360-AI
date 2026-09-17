import streamlit as st
from snowflake.snowpark.context import get_active_session

st.set_page_config(
    page_title="Insure360 AI",
    page_icon="🏦",
    layout="wide"
)

session = get_active_session()


def escape_sql(value):
    if value is None:
        return ""
    return str(value).replace("'", "''")


# =========================================================
# HEADER
# =========================================================

st.title("🏦 Insure360 AI")
st.subheader("Customer Intelligence & Next Best Action Copilot")
st.caption(
    "Powered by Snowflake, Snowflake Cortex AI, "
    "and Streamlit"
)


# =========================================================
# PORTFOLIO OVERVIEW
# =========================================================

st.divider()
st.subheader("📊 Portfolio Overview")

kpi_df = session.sql("""
SELECT
    TOTAL_CUSTOMERS,
    HIGH_RISK_CUSTOMERS,
    UNRESOLVED_CLAIM_CUSTOMERS,
    PAYMENT_ISSUE_CUSTOMERS,
    UPCOMING_RENEWAL_CUSTOMERS
FROM HACKATHON_C360.APP.V_PORTFOLIO_KPI
""").to_pandas()

if not kpi_df.empty:
    kpi = kpi_df.iloc[0]

    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = (
        st.columns(5)
    )

    with kpi_col1:
        st.metric(
            "Total Customers",
            int(kpi["TOTAL_CUSTOMERS"])
        )

    with kpi_col2:
        st.metric(
            "High Risk",
            int(kpi["HIGH_RISK_CUSTOMERS"])
        )

    with kpi_col3:
        st.metric(
            "Unresolved Claims",
            int(kpi["UNRESOLVED_CLAIM_CUSTOMERS"])
        )

    with kpi_col4:
        st.metric(
            "Payment Issues",
            int(kpi["PAYMENT_ISSUE_CUSTOMERS"])
        )

    with kpi_col5:
        st.metric(
            "Upcoming Renewals",
            int(kpi["UPCOMING_RENEWAL_CUSTOMERS"])
        )

else:
    st.warning("Portfolio KPI information is unavailable.")


# =========================================================
# PORTFOLIO ANALYTICS
# =========================================================

st.divider()
st.subheader("📈 Portfolio Analytics")

risk_df = session.sql("""
SELECT
    RISK_LEVEL,
    CUSTOMER_COUNT
FROM HACKATHON_C360.APP.V_RISK_DISTRIBUTION
ORDER BY
    CASE
        WHEN RISK_LEVEL = 'HIGH' THEN 1
        WHEN RISK_LEVEL = 'MEDIUM' THEN 2
        ELSE 3
    END
""").to_pandas()

claim_df = session.sql("""
SELECT
    CLAIM_STATUS,
    CLAIM_COUNT
FROM HACKATHON_C360.APP.V_CLAIM_DISTRIBUTION
ORDER BY CLAIM_STATUS
""").to_pandas()

payment_df = session.sql("""
SELECT
    PAYMENT_STATUS,
    PAYMENT_COUNT
FROM HACKATHON_C360.APP.V_PAYMENT_DISTRIBUTION
ORDER BY PAYMENT_STATUS
""").to_pandas()

renewal_df = session.sql("""
SELECT
    RENEWAL_BUCKET,
    POLICY_COUNT
FROM HACKATHON_C360.APP.V_RENEWAL_PIPELINE
ORDER BY RENEWAL_BUCKET
""").to_pandas()

analytics_col1, analytics_col2 = st.columns(2)

with analytics_col1:
    st.markdown("#### Customer Risk Distribution")

    if not risk_df.empty:
        st.bar_chart(
            risk_df.set_index("RISK_LEVEL"),
            use_container_width=True
        )
    else:
        st.info("Risk-distribution data is unavailable.")

    st.markdown("#### Payment Status")

    if not payment_df.empty:
        st.bar_chart(
            payment_df.set_index("PAYMENT_STATUS"),
            use_container_width=True
        )
    else:
        st.info("Payment-distribution data is unavailable.")


with analytics_col2:
    st.markdown("#### Claims Status")

    if not claim_df.empty:
        st.bar_chart(
            claim_df.set_index("CLAIM_STATUS"),
            use_container_width=True
        )
    else:
        st.info("Claim-distribution data is unavailable.")

    st.markdown("#### Renewal Pipeline")

    if not renewal_df.empty:
        st.bar_chart(
            renewal_df.set_index("RENEWAL_BUCKET"),
            use_container_width=True
        )
    else:
        st.info("Renewal-pipeline data is unavailable.")


# =========================================================
# CUSTOMER SELECTION
# =========================================================

st.divider()
st.subheader("👤 Customer 360")

customer_list_df = session.sql("""
SELECT
    CUSTOMER_ID,
    CUSTOMER_NAME
FROM HACKATHON_C360.APP.CUSTOMERS
ORDER BY CUSTOMER_ID
""").to_pandas()

if customer_list_df.empty:
    st.warning("No customers are available.")

else:
    customer_options = {
        f'{customer_record["CUSTOMER_ID"]} | '
        f'{customer_record["CUSTOMER_NAME"]}':
        customer_record["CUSTOMER_ID"]
        for _, customer_record in customer_list_df.iterrows()
    }

    selected_customer = st.selectbox(
        "Select Customer",
        list(customer_options.keys())
    )

    customer_id = customer_options[selected_customer]
    safe_customer_id = escape_sql(customer_id)


    # =====================================================
    # LOAD CUSTOMER 360 RECORD
    # =====================================================

    customer_df = session.sql(f"""
    SELECT *
    FROM HACKATHON_C360.APP.V_CUSTOMER_360_FINAL
    WHERE CUSTOMER_ID = '{safe_customer_id}'
    """).to_pandas()

    if customer_df.empty:
        st.warning(
            "Customer 360 information is unavailable."
        )

    else:
        row = customer_df.iloc[0]

        customer_name = str(
            row["CUSTOMER_NAME"]
        )

        customer_value_score = float(
            row["CUSTOMER_VALUE_SCORE"]
        )

        sentiment = str(
            row["SENTIMENT"]
        ).upper()

        recommended_action = str(
            row["RECOMMENDED_ACTION"]
        )

        action_reason = str(
            row["ACTION_REASON"]
        )

        ai_summary = str(
            row["AI_SUMMARY"]
        )

        if sentiment == "NEGATIVE":
            churn_risk = "HIGH"

        elif sentiment == "NEUTRAL":
            churn_risk = "MEDIUM"

        else:
            churn_risk = "LOW"

        sentiment_display = {
            "NEGATIVE": "🔴 NEGATIVE",
            "NEUTRAL": "🟡 NEUTRAL",
            "POSITIVE": "🟢 POSITIVE"
        }

        risk_display = {
            "HIGH": "🔴 HIGH",
            "MEDIUM": "🟡 MEDIUM",
            "LOW": "🟢 LOW"
        }


        # =================================================
        # CUSTOMER METRICS
        # =================================================

        metric_col1, metric_col2, metric_col3, metric_col4 = (
            st.columns(4)
        )

        with metric_col1:
            st.metric(
                "Customer",
                customer_name
            )

        with metric_col2:
            st.metric(
                "Value Score",
                customer_value_score
            )

        with metric_col3:
            st.metric(
                "Sentiment",
                sentiment_display.get(
                    sentiment,
                    sentiment
                )
            )

        with metric_col4:
            st.metric(
                "Churn Risk",
                risk_display.get(
                    churn_risk,
                    churn_risk
                )
            )


        # =================================================
        # CUSTOMER TIMELINE
        # =================================================

        st.divider()
        st.subheader("📅 Customer Timeline")

        st.caption(
            "Chronological view of policy, claim, payment, "
            "interaction, and approved-action events."
        )

        timeline_df = session.sql(f"""
        SELECT
            EVENT_DATE,
            EVENT_TYPE,
            EVENT_DESCRIPTION
        FROM HACKATHON_C360.APP.V_CUSTOMER_TIMELINE
        WHERE CUSTOMER_ID = '{safe_customer_id}'
        ORDER BY EVENT_DATE DESC
        """).to_pandas()

        if not timeline_df.empty:
            timeline_df["EVENT_DATE"] = (
                timeline_df["EVENT_DATE"].astype(str)
            )

            st.dataframe(
                timeline_df,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info(
                "No timeline events are available "
                "for this customer."
            )


        # =================================================
        # AI CONVERSATION SUMMARY
        # =================================================

        st.divider()
        st.subheader("🤖 AI Conversation Summary")

        if (
            ai_summary
            and ai_summary.lower() not in (
                "none",
                "nan"
            )
        ):
            st.markdown(ai_summary)

        else:
            st.info(
                "AI conversation summary is unavailable."
            )


        # =================================================
        # RULE-BASED NEXT BEST ACTION
        # =================================================

        st.divider()
        st.subheader("🎯 Recommended Next Action")

        if recommended_action == "No Immediate Action":
            st.info(recommended_action)
        else:
            st.success(recommended_action)

        st.subheader("📋 Recommendation Reason")
        st.write(action_reason)


        # =================================================
        # AI-ASSISTED NEXT BEST ACTION
        # =================================================

        st.divider()
        st.subheader("🧠 AI-Assisted Recommendation")

        ai_nba_df = session.sql(f"""
        SELECT
            AI_RECOMMENDATION
        FROM HACKATHON_C360.APP.V_AI_NBA
        WHERE CUSTOMER_ID = '{safe_customer_id}'
        """).to_pandas()

        if not ai_nba_df.empty:
            st.info(
                str(
                    ai_nba_df.iloc[0][
                        "AI_RECOMMENDATION"
                    ]
                )
            )

        else:
            st.info(
                "AI-assisted recommendation is unavailable."
            )


        # =================================================
        # EXECUTIVE BRIEF
        # =================================================

        st.divider()
        st.subheader("📋 Executive Brief")

        st.caption(
            "Generate an executive-level customer risk "
            "and action summary."
        )

        if st.button(
            "Generate Executive Brief",
            key=f"brief_{customer_id}",
            use_container_width=True
        ):
            brief_df = session.sql(f"""
            SELECT
                EXECUTIVE_BRIEF
            FROM HACKATHON_C360.APP.V_EXECUTIVE_BRIEF
            WHERE CUSTOMER_ID = '{safe_customer_id}'
            """).to_pandas()

            if not brief_df.empty:
                st.markdown(
                    str(
                        brief_df.iloc[0][
                            "EXECUTIVE_BRIEF"
                        ]
                    )
                )

            else:
                st.warning(
                    "Executive brief is unavailable "
                    "for this customer."
                )


        # =================================================
        # ASK CUSTOMER 360 COPILOT
        # =================================================

        st.divider()
        st.subheader("💬 Ask Customer 360")

        st.caption(
            "Ask about customer risk, concerns, policies, "
            "claims, payments, or the recommended next action."
        )

        question = st.text_input(
            "Ask a question about this customer",
            placeholder=(
                "Example: Why does this customer need attention?"
            )
        )

        if question:
            context_df = session.sql(f"""
            SELECT
                CUSTOMER_NAME,
                CUSTOMER_VALUE_SCORE,
                SENTIMENT,
                RECOMMENDED_ACTION,
                ACTION_REASON,
                AI_SUMMARY,
                TRANSCRIPT_TEXT
            FROM HACKATHON_C360.APP.V_CUSTOMER_CONTEXT
            WHERE CUSTOMER_ID = '{safe_customer_id}'
            """).to_pandas()

            if not context_df.empty:
                context_row = context_df.iloc[0]

                prompt = (
                    "You are an insurance customer relationship "
                    "advisor. Answer the user question using only "
                    "the supplied customer context. If the answer "
                    "is not present, state clearly that the "
                    "information is not available. Do not invent "
                    "or assume facts. Provide a concise explanation "
                    "and recommend an action only when relevant."
                    "\n\n"
                    f"Customer ID: {customer_id}\n"
                    f"Customer Name: "
                    f"{context_row['CUSTOMER_NAME']}\n"
                    f"Customer Value Score: "
                    f"{context_row['CUSTOMER_VALUE_SCORE']}\n"
                    f"Sentiment: "
                    f"{context_row['SENTIMENT']}\n"
                    f"Churn Risk: {churn_risk}\n"
                    f"Recommended Action: "
                    f"{context_row['RECOMMENDED_ACTION']}\n"
                    f"Recommendation Reason: "
                    f"{context_row['ACTION_REASON']}\n"
                    f"AI Summary: "
                    f"{context_row['AI_SUMMARY']}\n"
                    f"Call Transcript: "
                    f"{context_row['TRANSCRIPT_TEXT']}\n\n"
                    f"User Question: {question}"
                )

                safe_prompt = escape_sql(prompt)

                with st.spinner(
                    "Analyzing Customer 360 context..."
                ):
                    response_df = session.sql(f"""
                    SELECT
                        SNOWFLAKE.CORTEX.COMPLETE(
                            'llama3.1-8b',
                            '{safe_prompt}'
                        ) AS AI_RESPONSE
                    """).to_pandas()

                if not response_df.empty:
                    st.subheader(
                        "🤖 Customer 360 Copilot Answer"
                    )

                    st.markdown(
                        str(
                            response_df.iloc[0][
                                "AI_RESPONSE"
                            ]
                        )
                    )

                else:
                    st.warning(
                        "The Copilot could not generate "
                        "an answer."
                    )

            else:
                st.warning(
                    "Customer context is unavailable."
                )


        # =================================================
        # ACTION APPROVAL
        # =================================================

        st.divider()
        st.subheader("✅ Action Approval")

        st.caption(
            "This records human acceptance of the recommendation "
            "in Action History for audit and follow-up. "
            "It does not automatically contact the customer, "
            "change a policy, approve a claim, or alter pricing."
        )

        if st.button(
            "Execute Recommended Action",
            type="primary",
            key=f"action_{customer_id}",
            use_container_width=True
        ):
            safe_action = escape_sql(
                recommended_action
            )

            safe_reason = escape_sql(
                action_reason
            )

            session.sql(f"""
            INSERT INTO HACKATHON_C360.APP.ACTION_HISTORY
            SELECT
                UUID_STRING(),
                '{safe_customer_id}',
                '{safe_action}',
                '{safe_reason}',
                CURRENT_TIMESTAMP()
            """).collect()

            st.success(
                "✅ Action successfully recorded "
                "in Action History."
            )


        # =================================================
        # RECENT ACTION HISTORY
        # =================================================

        st.divider()
        st.subheader("🕘 Recent Action History")

        history_df = session.sql(f"""
        SELECT
            RECOMMENDED_ACTION,
            ACTION_REASON,
            CREATED_AT
        FROM HACKATHON_C360.APP.ACTION_HISTORY
        WHERE CUSTOMER_ID = '{safe_customer_id}'
        ORDER BY CREATED_AT DESC
        LIMIT 5
        """).to_pandas()

        if not history_df.empty:
            st.dataframe(
                history_df,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info(
                "No actions have been recorded "
                "for this customer."
            )