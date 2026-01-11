import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Astro Coach – AI Decision Intelligence",
    layout="wide"
)

st.title("🔮 Astro Coach – AI Decision Intelligence Platform")
st.caption("Market Trend Analysis • Conversion Intelligence • Churn Risk Management")

# -------------------------
# DATA LOADING
# -------------------------
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

# -------------------------
# SIDEBAR NAVIGATION
# -------------------------
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Select View",
    [
        "Executive Overview",
        "Market Trend Intelligence",
        "Conversion Intelligence",
        "Targeting Simulator",
        "Churn Early Warning"
    ]
)
with st.sidebar.expander("📊 Decision Context & Interpretation"):
    story_step = st.radio(
        "Select Business Perspective",
        [
            "Business Challenge",
            "Key Analytical Findings",
            "AI-Driven Solution",
            "Strategic Impact"
        ]

    )

    if story_step == "Business Challenge":
        st.markdown(
            """
        **Why this system exists**

        Astro Coach operates in a freemium model where success depends on:
        - Converting free users  
        - Retaining premium users  
        - Timing campaigns correctly  

        The challenge is transforming behavioral data into
        **actionable business decisions**.
        """
        )

    elif story_step == "Key Analytical Findings":
        st.markdown(
            """
        **What analysis reveals**

        - Not all engagement leads to revenue  
        - Intent-driven actions predict conversion  
        - Disengagement predicts churn well before expiry  
        """
        )

    elif story_step == "AI-Driven Solution":
        st.markdown(
            """
        **How AI changes the game**

        - LSTM forecasts demand direction  
        - Conversion models enable targeted growth  
        - Churn prediction enables proactive retention  
        """
        )

    elif story_step == "Strategic Impact":
        st.markdown(
            """
        **What the business gains**

        - Smarter campaign planning  
        - Lower acquisition cost  
        - Protected recurring revenue  
        """
        )



# -------------------------
# EXECUTIVE OVERVIEW
# -------------------------
if section == "Executive Overview":
    st.header("📊 Executive Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Users", len(user_features))

    with col2:
        if "isPremiumUserFlag" in user_features.columns:
            st.metric("Premium Users", user_features["isPremiumUserFlag"].sum())

    with col3:
        st.metric("Forecasted Demand (14 days)",
                  int(forecast["predicted_premium_subscriptions"].sum()))

    st.markdown(
        """
    ### What this system delivers
    - **Forecasts** premium demand to guide campaign timing  
    - **Identifies** free users most likely to convert  
    - **Flags** premium users at risk of churn  
    - **Transforms analytics into action** through targeting and retention insights  
    """
    )

# -------------------------
# MARKET TREND INTELLIGENCE
# -------------------------
elif section == "Market Trend Intelligence":
    st.header("📈 Market Trend Intelligence")

    st.markdown(
        """
    This section explains **how premium demand is evolving over time**
    and what it means for campaign planning.
    """
    )

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

    # -------------------------
    # Dynamic Interpretation
    # -------------------------
    st.subheader("📌 What the trend shows")

    recent_avg = filtered.tail(7)["premium_subscriptions"].mean()
    earlier_avg = filtered.head(7)["premium_subscriptions"].mean()

    if recent_avg > earlier_avg:
        trend_msg = "Premium demand is showing an **upward momentum**."
    else:
        trend_msg = "Premium demand is currently **flat or declining**."

    st.markdown(
        f"""
    **Trend Signal:**  
    {trend_msg}

    Short-term volatility exists, but the overall pattern helps identify
    **when marketing pressure is most effective**.
    """
    )

    # -------------------------
    # Business Meaning
    # -------------------------
    st.subheader("💼 Business Interpretation")

    st.markdown(
        """
    Demand forecasting here is used as a **planning signal**, not a precise number.

    It helps answer:
    - *When should we launch promotions?*  
    - *When should we avoid campaign fatigue?*
    """
    )

    # -------------------------
    # Recommended Actions
    # -------------------------
    st.subheader("🚀 Recommended Actions")

    st.success(
        """
    **Campaign Playbook**
    - Schedule major promotions during rising demand windows  
    - Use low-demand periods for product education  
    - Avoid heavy discounts during flat demand phases  
    """
    )


# -------------------------
# CONVERSION INTELLIGENCE
# -------------------------
elif section == "Conversion Intelligence":
    st.header("🎯 Conversion Intelligence")

    st.markdown(
        """
    This section explains **why users convert to premium** based on
    behavioral patterns learned by the model — not just what happened,
    but **what drives purchase intent**.
    """
    )

    # -------------------------
    # Controls
    # -------------------------
    top_n = st.slider(
        "Number of top behavioral drivers to analyze",
        min_value=5, max_value=15, value=10
    )

    # -------------------------
    # Prepare data
    # -------------------------
    drivers = feature_importance.sort_values(
        by="coefficient", ascending=False
    ).head(top_n)

    positive = drivers[drivers["coefficient"] > 0]
    negative = drivers[drivers["coefficient"] < 0]

    # -------------------------
    # Visualization
    # -------------------------
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(drivers["feature"], drivers["coefficient"])
    ax.axvline(x=0, linestyle="--", linewidth=1)
    ax.invert_yaxis()
    ax.set_xlabel("Impact on Conversion Likelihood")
    ax.set_title("Key Behavioral Drivers of Premium Conversion")

    st.pyplot(fig)

    # -------------------------
    # Dynamic Interpretation
    # -------------------------
    st.subheader("📌 What the model is telling us")

    if not positive.empty:
        top_positive = positive.iloc[0]["feature"]
        st.markdown(
            f"""
    **Strongest positive signal:**  
    Users who frequently perform **{top_positive}** actions show the
    highest likelihood of upgrading to premium.

    This indicates **intent-building behavior** rather than casual browsing.
    """
        )

    if not negative.empty:
        top_negative = negative.iloc[-1]["feature"]
        st.markdown(
            f"""
    **Strongest negative signal:**  
    High frequency of **{top_negative}** is associated with **lower conversion
    probability**, suggesting passive usage without purchase intent.
    """
        )

    # -------------------------
    # Business Interpretation
    # -------------------------
    st.subheader("💼 Business Interpretation")

    st.markdown(
        """
    The model distinguishes between **engagement** and **intent**.

    - Engagement = user is active  
    - Intent = user is preparing to buy  

    The strongest conversion drivers come from:
    - Navigation actions (e.g., day/calendar selection)  
    - Prediction exploration  
    - Purposeful feature interaction  

    Mere app usage (open/close patterns) does **not** reliably predict revenue.
    """
    )

    # -------------------------
    # Recommended Actions
    # -------------------------
    st.subheader("🚀 Recommended Actions")

    st.success(
        """
    **Growth Playbook**
    - Trigger premium offers when users perform:
        • Prediction expansion  
        • Day/calendar navigation  
    - Avoid generic campaigns for users showing only:
        • App foreground/background behavior  
    - Design onboarding flows that **force exposure** to high-intent actions.
    """
    )

    # -------------------------
    # Evidence Table
    # -------------------------
    st.subheader("📊 Evidence: Driver Strength")

    st.dataframe(
        drivers.rename(
            columns={
                "feature": "Behavior",
                "coefficient": "Impact Score"
            }
        ),
        use_container_width=True
    )

# -------------------------
# TARGETING SIMULATOR
# -------------------------
elif section == "Targeting Simulator":
    st.header("🎯 Targeting Simulator")

    st.markdown(
        """
    Use this tool to simulate marketing strategies based on
    predicted conversion probability.
    """
    )

    threshold = st.slider(
        "Minimum Conversion Probability",
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
            st.metric("Avg Conversion Probability",
                      round(candidates["conversion_probability"].mean(), 2))

        st.dataframe(candidates[["user_id", "conversion_probability"]])

        st.download_button(
            "Download Target List",
            candidates.to_csv(index=False),
            file_name="target_users.csv"
        )

        st.success(
            """
        **Strategy Tip:**  
        Use these users for limited-time offers or personalized push notifications.
        """
        )
    else:
        st.error("Conversion probabilities not found.")

# -------------------------
# CHURN EARLY WARNING
# -------------------------
elif section == "Churn Early Warning":
    st.header("⚠️ Churn Early Warning System")

    st.markdown(
        """
    This section identifies **premium users at risk of leaving**
    and explains **why** they are at risk.
    """
    )

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

    # -------------------------
    # Churn Drivers
    # -------------------------
    st.subheader("📊 What drives churn risk")

    top_churn = churn_importance.sort_values(
        by="coefficient", ascending=False
    ).head(10)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(top_churn["feature"], top_churn["coefficient"])
    ax.axvline(x=0, linestyle="--", linewidth=1)
    ax.invert_yaxis()
    ax.set_xlabel("Impact on Churn Risk")
    ax.set_title("Key Behavioral Signals of Churn")

    st.pyplot(fig)

    # -------------------------
    # Dynamic Interpretation
    # -------------------------
    st.subheader("📌 What the model is telling us")

    top_signal = top_churn.iloc[0]["feature"]

    st.markdown(
        f"""
    **Primary churn signal:**  
    Users showing **{top_signal}** patterns have the highest risk of not renewing.

    This usually reflects **disengagement before expiry**, not dissatisfaction
    at the moment of renewal.
    """
    )

    # -------------------------
    # Business Interpretation
    # -------------------------
    st.subheader("💼 Business Interpretation")

    st.markdown(
        """
    Churn is rarely sudden.  
    It builds gradually as users reduce interaction with core features.

    The system detects this **early**, giving the business a chance to act
    before revenue is lost.
    """
    )

    # -------------------------
    # Retention Actions
    # -------------------------
    st.subheader("🚀 Retention Playbook")

    st.warning(
        """
    **Retention Strategy**
    - Trigger renewal nudges 7 days before expiry  
    - Offer loyalty benefits to high-risk users  
    - Re-engage with personalized predictions  
    """
    )

    # -------------------------
    # Evidence Table
    # -------------------------
    st.subheader("📋 Users at Risk")

    st.dataframe(
        at_risk[["user_id", "churn_probability"]]
        .sort_values(by="churn_probability", ascending=False)
        .head(30),
        use_container_width=True
    )

    st.download_button(
        "Download At-Risk Users",
        at_risk.to_csv(index=False),
        file_name="premium_users_at_risk.csv"
    )


# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.markdown("**Astro Coach – AI Decision Intelligence Platform**")
st.caption("Market Trend Analysis | Conversion Intelligence | Churn Risk Management")
