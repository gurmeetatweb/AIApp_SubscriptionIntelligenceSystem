import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Astro Coach – AI Decision Intelligence",
    layout="wide"
)

# -------------------------------------------------
# STYLE (light polish, safe)
# -------------------------------------------------
st.markdown(
    """
    <style>
    .metric-card {
        background-color: #111827;
        padding: 15px;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# TITLE
# -------------------------------------------------
st.title("🔮 Astro Coach – AI Decision Intelligence Platform")
st.caption("Market Trend Analysis • Conversion Intelligence • Churn Risk Management")

# -------------------------------------------------
# DATA LOADING
# -------------------------------------------------
@st.cache_data
def load_data():
    daily_demand = pd.read_csv("./data/processed/daily_premium_demand.csv")
    forecast = pd.read_csv("./data/processed/premium_demand_forecast.csv")
    feature_importance = pd.read_csv("./data/processed/conversion_feature_importance.csv")
    user_features = pd.read_csv("./data/processed/user_conversion_scores.csv")
    churn_scores = pd.read_csv("./data/processed/premium_churn_scores.csv")
    churn_importance = pd.read_csv("./data/processed/churn_feature_importance.csv")
    return daily_demand, forecast, feature_importance, user_features, churn_scores, churn_importance

daily_demand, forecast, feature_importance, user_features, churn_scores, churn_importance = load_data()

# -------------------------------------------------
# UTILITY — CONFIDENCE SCORE
# -------------------------------------------------
def compute_confidence(num_features):
    coverage = min(1.0, num_features / 5)
    return round((0.5 + 0.5 * coverage) * 100, 1)

# --- Conversion metric ---
high_intent_threshold = 0.7

# --- Freemium users only ---
freemium_users = user_features[user_features["isPremiumUserFlag"] == 0]

# Baseline average conversion probability
baseline_avg_prob = freemium_users["conversion_probability"].mean()

# High-intent users (reuse threshold)
high_intent_users = freemium_users[
    freemium_users["conversion_probability"] >= high_intent_threshold
]

high_intent_avg_prob = high_intent_users["conversion_probability"].mean()

# Conversion lift (safe proxy)
conversion_lift = (
    high_intent_avg_prob / baseline_avg_prob
    if baseline_avg_prob > 0 else 0
)

# --- Churn metric ---
churn_risk_threshold = 0.6

# Ensure churn_scores has premium flag
churn_enriched = churn_scores.merge(
    user_features[["user_id", "isPremiumUserFlag"]],
    on="user_id",
    how="left"
)
churn_risk_threshold = 0.6  # keep consistent with your model logic

premium_users = churn_enriched[
    churn_enriched["isPremiumUserFlag"] == 1
]

if len(premium_users) > 0:
    high_risk_users = premium_users[
        premium_users["churn_probability"] >= churn_risk_threshold
    ]

    churn_risk_pct = (len(high_risk_users) / len(premium_users)) * 100
else:
    churn_risk_pct = 0

# --- Acquisition efficiency proxy ---
targeted_lift_pct = (conversion_lift - 1) * 100


# -------------------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------------------
st.sidebar.title(" Astro Coach Navigation")

section = st.sidebar.radio(
    "Select View",
    [
        "Executive Overview",
        "Market Trend Intelligence",
        "Conversion Intelligence",
        "Targeting Simulator",
        "Churn Early Warning",
        "Event Impact Simulator",
        "Churn Impact Simulator"
    ]
)

# -------------------------------------------------
# STORY / BUSINESS GUIDE (NON-BLOCKING)
# -------------------------------------------------
with st.sidebar.expander("📘 Business Insights Guide"):
    guide_step = st.radio(
        "Select Business Perspective",
        [
            "Business Challenge",
            "Key Analytical Findings",
            "AI-Driven Solution",
            "Strategic Impact"
        ]
    )

    if guide_step == "Business Challenge":
        st.markdown(
            """
            Astro Coach operates in a freemium model where success depends on:
            - Converting free users  
            - Retaining premium users  
            - Timing campaigns effectively  

            The challenge is turning large volumes of behavior data into
            **actionable business decisions**.
            """
        )

    elif guide_step == "Key Analytical Findings":
        st.markdown(
            """
            Analysis shows:
            - Not all engagement leads to revenue  
            - Intent-driven actions predict conversion  
            - Disengagement predicts churn before expiry  
            """
        )

    elif guide_step == "AI-Driven Solution":
        st.markdown(
            """
            The AI system introduces:
            - Demand forecasting with LSTM  
            - Conversion modeling for targeted growth  
            - Churn prediction for proactive retention  
            """
        )

    elif guide_step == "Strategic Impact":
        st.markdown(
            """
            With this system, Astro Coach can:
            - Reduce acquisition cost  
            - Protect recurring revenue  
            - Run smarter, data-led campaigns  
            """
        )

# -------------------------------------------------
# EXECUTIVE OVERVIEW
# -------------------------------------------------
if section == "Executive Overview":
    st.header("📊 Executive Overview")
    st.caption(
        "A consolidated view of demand outlook, revenue levers, and risk signals for leadership decision-making."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Users", len(user_features))

    with col2:
        if "isPremiumUserFlag" in user_features.columns:
            st.metric("Premium Users", int(user_features["isPremiumUserFlag"].sum()))

    with col3:
        st.metric(
            "Forecasted Demand (14 days)",
            int(forecast["predicted_premium_subscriptions"].sum())
        )

    st.markdown("### 🎯 Decision Focus")
    st.caption("Select the primary business objective to surface the most relevant insights.")

    business_focus = st.radio(
        "What is your current business priority?",
        (
            "Improve freemium → premium conversion",
            "Reduce churn / non-payment risk",
            "Reduce acquisition cost"
        ),
        horizontal=True
    )

    st.markdown("---")

    if business_focus == "Improve freemium → premium conversion":
        st.markdown("#### 🔍 Conversion Opportunity")

        st.metric(
            label="High-Intent User Conversion Lift",
            value=f"{conversion_lift:.1f}×",
            delta="vs average users"
        )

        st.info(
            "Users exhibiting high-intent behaviors convert significantly better than "
            "the general freemium population."
        )

        st.success("**Recommended next view:** Conversion Intelligence → High-Intent User Targeting")


    elif business_focus == "Reduce churn / non-payment risk":
        st.markdown("#### ⚠️ Churn Risk Signal")

        st.metric(
                label="Premium Users at High Churn Risk",
                value=f"{churn_risk_pct:.1f}%",
                delta="require proactive retention"
            )

        st.warning(
                "A segment of premium users shows elevated churn risk based on "
                "recent disengagement patterns."
            )

        st.success("**Recommended next view:** Churn Early Warning → At-Risk Premium Users")


    elif business_focus == "Reduce acquisition cost":
        st.markdown("#### 📉 Acquisition Efficiency")

        st.metric(
            label="Targeted Campaign Efficiency",
            value=f"+{(conversion_lift - 1) * 100:.0f}%",
            delta="higher conversion potential"
        )

        st.info(
            "Targeting high-intent user segments can significantly improve "
            "campaign efficiency and reduce acquisition spend."
        )

        st.success("**Recommended next view:** Targeting Simulator → Conversion Probability Ranking")


# -------------------------------------------------
# MARKET TREND INTELLIGENCE
# -------------------------------------------------
elif section == "Market Trend Intelligence":
    st.header("📈 Market Trend Intelligence")

    daily_demand["payment_date"] = pd.to_datetime(daily_demand["payment_date"])

    min_date = daily_demand["payment_date"].min().to_pydatetime()
    max_date = daily_demand["payment_date"].max().to_pydatetime()

    date_range = st.slider(
        "Select analysis window",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date)
    )

    filtered = daily_demand[
        (daily_demand["payment_date"] >= date_range[0]) &
        (daily_demand["payment_date"] <= date_range[1])
    ]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Historical Premium Demand")
        st.line_chart(
            filtered.set_index("payment_date")["premium_subscriptions"]
        )

    with col2:
        st.subheader("14-Day Forecast")
        st.line_chart(
            forecast.set_index("date")["predicted_premium_subscriptions"]
        )

    recent_avg = filtered.tail(7)["premium_subscriptions"].mean()
    earlier_avg = filtered.head(7)["premium_subscriptions"].mean()

    trend_msg = (
        "Premium demand shows **upward momentum**."
        if recent_avg > earlier_avg
        else "Premium demand is currently **flat or soft**."
    )

    st.markdown(
        f"""
        **Trend Signal:**  
        {trend_msg}

        Use this as a **planning signal**, not a precise forecast.
        """
    )

    st.markdown("## 📌 What this shows")
    st.markdown(
        """
        This view combines **historical premium demand** with an AI-based forecast
        to indicate the likely **direction of near-term growth**.
        """
    )

    st.markdown("## 💡 Why this matters")
    st.markdown(
        """
        While exact numbers may vary, understanding the **trend direction**
        helps leadership make better decisions on:
        - Campaign timing  
        - Resource planning  
        - Budget allocation  
        """
    )

    
# -------------------------------------------------
# CONVERSION INTELLIGENCE
# -------------------------------------------------
elif section == "Conversion Intelligence":
    st.header("🎯 Conversion Intelligence")
    st.caption(
        "Negative drivers represent behaviors correlated with engagement but not purchase intent."
    )

    top_n = st.slider("Top drivers to analyze", 5, 15, 10)

    drivers = feature_importance.sort_values(
        by="coefficient", ascending=False
    ).head(top_n)

    positive = drivers[drivers["coefficient"] > 0]
    negative = drivers[drivers["coefficient"] < 0]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(drivers["feature"], drivers["coefficient"])
    ax.axvline(x=0, linestyle="--", linewidth=1)
    ax.invert_yaxis()
    ax.set_xlabel("Impact on Conversion Likelihood")
    ax.set_title("Key Behavioral Drivers of Premium Conversion")
    st.pyplot(fig)

    if not positive.empty:
        st.caption(
            f"Strongest growth signal: **{positive.iloc[0]['feature']}**"
        )

    if not negative.empty:
        st.caption(
            f"Strongest non-revenue signal: **{negative.iloc[-1]['feature']}**"
        )
    st.markdown("## 📌 What this shows")
    st.markdown(
        """
        This analysis identifies which user actions represent **real purchase intent** 
        versus general app usage.
        """
    )
    st.markdown("## 💡 Why this matters")
    st.markdown(
        """
        Not all engagement leads to revenue.  
        This view helps the business **separate activity from intent**, ensuring that
        marketing and product investments focus on actions that truly drive conversion.
        """
    )
    st.markdown("## 🚀 Recommended growth actions")
    st.markdown(
        """
        **How the business can use this**
        - Design onboarding flows around **high-intent actions**  
        - Trigger offers when these behaviors occur  
        - Track them as **leading indicators of revenue growth**  
        """
    )



# -------------------------------------------------
# TARGETING SIMULATOR
# -------------------------------------------------
elif section == "Targeting Simulator":
    st.header("🎯 Targeting Simulator")

    threshold = st.slider(
        "Minimum conversion probability",
        0.1, 0.9, 0.4, 0.05
    )

    max_users = st.selectbox("Maximum users to target", [10, 20, 50, 100], index=1)

    if "conversion_probability" in user_features.columns:
        candidates = user_features[
            (user_features["isPremiumUserFlag"] == 0) &
            (user_features["conversion_probability"] >= threshold)
        ].sort_values(
            by="conversion_probability", ascending=False
        ).head(max_users)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Target Users", len(candidates))
        with col2:
            st.metric(
                "Avg Conversion Probability",
                round(candidates["conversion_probability"].mean(), 2)
            )

        st.dataframe(candidates[["user_id", "conversion_probability"]])

        st.download_button(
            "Download Target List",
            candidates.to_csv(index=False),
            file_name="target_users.csv"
        )
    st.markdown("## 📌 What this shows")
    st.markdown(
        """
        This list identifies **free users with the highest likelihood of converting**
        based on behavioral patterns.
        """
    )
    st.markdown("## 💡 Why this matters")
    st.markdown(
        """
        Instead of mass campaigns, the business can now practice
        **precision targeting**, improving ROI and reducing acquisition cost.
        """
    )
    st.markdown("## 🎯 Recommended growth actions")
    st.markdown(
        """
        **How the business can use this**
        - Run **personalized upgrade offers** for this group  
        - Prioritize them in sales and CRM workflows  
        - Measure conversion uplift from **AI-guided targeting**  
        """
    )


# -------------------------------------------------
# CHURN EARLY WARNING
# -------------------------------------------------
elif section == "Churn Early Warning":
    st.header("⚠️ Churn Early Warning")

    churn_threshold = st.slider(
        "Churn Risk Threshold",
        0.1, 0.9, 0.5, 0.05
    )

    at_risk = churn_scores[
        churn_scores["churn_probability"] >= churn_threshold
    ]

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Premium Users", len(churn_scores))
    with col2:
        st.metric("High-Risk Users", len(at_risk))

    top_churn = churn_importance.sort_values(
        by="coefficient", ascending=False
    ).head(10)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(top_churn["feature"], top_churn["coefficient"])
    ax.axvline(x=0, linestyle="--", linewidth=1)
    ax.invert_yaxis()
    ax.set_xlabel("Impact on Churn Risk")
    ax.set_title("Key Churn Signals")
    st.pyplot(fig)
    st.markdown("## 📌 What this shows")
    st.markdown(
        """
        This chart highlights the **user behaviors most strongly associated with churn risk**.
        Higher values indicate actions that frequently occur before premium users stop renewing.
        """
    )
    st.markdown("## 💡 Why this matters")
    st.markdown(
        """
        These signals act as an **early warning system**.  
        Instead of waiting for cancellations, the business can now:
        - Detect disengagement patterns early  
        - Intervene before revenue is lost  
        """
    )
    st.markdown("## 🛡️ Recommended retention actions")
    st.markdown(
        """
        **How the business can use this**
        - Trigger **retention campaigns** when these signals increase  
        - Alert support teams for **high-risk premium users**  
        - Monitor these behaviors as **leading churn indicators**  
        """
    )



# -------------------------------------------------
# EVENT IMPACT SIMULATOR
# -------------------------------------------------
elif section == "Event Impact Simulator":
    st.header("🧪 Event Impact Simulator")

    all_events = feature_importance.sort_values(
        by="coefficient", ascending=False
    )

    selected_events = st.multiselect(
        "Select behaviors to simulate",
        options=all_events["feature"].tolist(),
        default=all_events.head(3)["feature"].tolist()
    )

    if not selected_events:
        st.warning("Please select at least one behavior.")
        st.stop()

    uplift = st.slider(
        "Expected improvement in selected behaviors (%)",
        5, 50, 15, 5
    )

    uplift_factor = uplift / 100

    selected_df = all_events[
        all_events["feature"].isin(selected_events)
    ].copy()

    selected_df["simulated_impact"] = (
        selected_df["coefficient"] * uplift_factor
    )

    positive_impact = selected_df[
        selected_df["simulated_impact"] > 0
    ]["simulated_impact"].sum()

    negative_impact = selected_df[
        selected_df["simulated_impact"] < 0
    ]["simulated_impact"].sum()

    net_impact = positive_impact + negative_impact

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Selected Behaviors", len(selected_events))
    with col2:
        st.metric("Estimated Conversion Impact", round(net_impact, 3))

    confidence = compute_confidence(len(selected_events))
    st.progress(confidence / 100)
    st.caption(f"Simulation confidence: {confidence}%")

    # Compact confidence guide
    if confidence < 40:
        st.caption("🔴 Low confidence — use for exploration, not execution.")
    elif confidence < 70:
        st.caption("🟡 Moderate confidence — directional guidance.")
    else:
        st.caption("🟢 High confidence — suitable for action.")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(
        selected_df["feature"],
        selected_df["simulated_impact"]
    )
    ax.axvline(x=0, linestyle="--", linewidth=1)
    ax.invert_yaxis()
    ax.set_xlabel("Simulated Change in Conversion Likelihood")
    ax.set_title("What-If Impact of Improving Selected Behaviors")
    st.pyplot(fig)
    st.markdown("## 📌 What this means")

    if net_impact > 0:
        st.success(
            f"""
            Improving the selected behaviors by **{uplift}%** could increase overall
            **conversion likelihood**.

            This suggests that investing in features or campaigns that promote these
            actions is likely to generate **measurable revenue uplift**.
            """
        )
    elif net_impact < 0:
        st.warning(
            """
            The selected behaviors are associated with **lower conversion impact**.

            Improving these may increase engagement, but they should not be treated
            as **primary revenue levers**.
            """
        )
    else:
        st.info(
            """
            The selected behaviors show **neutral impact** on conversion.

            They support engagement but are unlikely to directly influence revenue outcomes.
            """
        )
    st.markdown("## 🚀 Suggested Business Actions")

    if net_impact > 0:
        st.markdown(
            """
            **How to use this insight**
            - Prioritize product changes around **high-impact behaviors**  
            - Trigger campaigns when these actions occur  
            - Track these events as **leading revenue indicators**  
            """
        )
    else:
        st.markdown(
            """
            **How to use this insight**
            - Treat these actions as **experience enhancers**, not growth levers  
            - Avoid heavy spend on campaigns centered only on these behaviors  
            - Combine them with high-intent signals for better ROI  
            """
        )
    st.markdown("## 📋 Simulation Details")

    st.dataframe(
        selected_df[["feature", "coefficient", "simulated_impact"]]
        .rename(columns={
            "feature": "Behavior",
            "coefficient": "Model Impact",
            "simulated_impact": "Simulated Impact"
        }),
        use_container_width=True
    )



# -------------------------------------------------
# CHURN IMPACT SIMULATOR
# -------------------------------------------------
elif section == "Churn Impact Simulator":
    st.header("🛡️ Churn Impact Simulator")

    all_signals = churn_importance.sort_values(
        by="coefficient", ascending=False
    )

    selected_signals = st.multiselect(
        "Select behaviors to influence",
        options=all_signals["feature"].tolist(),
        default=all_signals.head(3)["feature"].tolist()
    )

    if not selected_signals:
        st.warning("Please select at least one behavior.")
        st.stop()

    uplift = st.slider(
        "Expected improvement in selected behaviors (%)",
        5, 50, 15, 5
    )

    uplift_factor = uplift / 100

    selected_df = all_signals[
        all_signals["feature"].isin(selected_signals)
    ].copy()

    # Positive churn coefficient = more churn risk → invert for retention effect
    selected_df["simulated_impact"] = (
        -1 * selected_df["coefficient"] * uplift_factor
    )

    positive_effect = selected_df[
        selected_df["simulated_impact"] > 0
    ]["simulated_impact"].sum()

    negative_effect = selected_df[
        selected_df["simulated_impact"] < 0
    ]["simulated_impact"].sum()

    net_effect = positive_effect + negative_effect

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Selected Behaviors", len(selected_signals))
    with col2:
        st.metric("Estimated Churn Reduction", round(net_effect, 3))

    confidence = compute_confidence(len(selected_signals))
    st.progress(confidence / 100)
    st.caption(f"Simulation confidence: {confidence}%")

    if confidence < 40:
        st.caption("🔴 Low confidence — exploratory insight.")
    elif confidence < 70:
        st.caption("🟡 Moderate confidence — directional guidance.")
    else:
        st.caption("🟢 High confidence — action-ready.")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(
        selected_df["feature"],
        selected_df["simulated_impact"]
    )
    ax.axvline(x=0, linestyle="--", linewidth=1)
    ax.invert_yaxis()
    ax.set_xlabel("Simulated Change in Churn Risk")
    ax.set_title("What-If Impact of Improving Selected Behaviors")
    st.pyplot(fig)
    st.caption(
        "Higher values indicate behaviors commonly observed before non-renewal."
    )

    st.markdown("## 📌 What this means")

    if net_effect > 0:
        st.success(
            f"""
            Improving the selected behaviors by **{uplift}%** could meaningfully
            **reduce churn risk** among premium users.

            This represents a **direct opportunity to protect recurring revenue**.
            """
        )
    elif net_effect < 0:
        st.warning(
                """
                The selected behaviors show **limited impact on churn reduction**.

                Improving them may enhance experience, but they are not strong
                **retention drivers**.
                """ 
            )
    else:
        st.info(
                """
                The selected behaviors have **neutral effect** on churn.

                They support usage but are unlikely to materially change renewal outcomes.
                """
            )
    st.markdown("## 🛡️ Suggested Retention Actions")

    if net_effect > 0:
        st.markdown(
            """
            **How to use this insight**
            - Trigger loyalty offers when these behaviors decline  
            - Build retention journeys around these actions  
            - Monitor them as **early churn-warning signals**  
            """
        )
    else:
        st.markdown(
            """
            **How to use this insight**
            - Use these behaviors to improve satisfaction  
            - Do not rely on them alone for churn prevention  
            - Combine with pricing, support, and lifecycle strategies  
            """
        )
    st.markdown("## 📋 Simulation Details")

    st.dataframe(
        selected_df[["feature", "coefficient", "simulated_impact"]]
            .rename(columns={
                "feature": "User Behavior",
                "coefficient": "Churn Signal Strength",
                "simulated_impact": "Retention Sensitivity"
            }),
            use_container_width=True
    )
    st.caption(
        "Churn Signal Strength indicates how strongly a behavior is associated with churn risk. "
        "Retention Sensitivity shows whether improving the behavior meaningfully reduces churn."
    )




# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown(
    """
    ---
    **Note:** All predictions and simulations are intended for 
    **decision support and scenario planning**, not automated execution.
    Final business decisions should always combine AI insights with
    managerial judgment and domain expertise.
    """
)

st.markdown("---")
st.caption("Astro Coach – AI Decision Intelligence Platform")
