import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Astro Coach – AI Market Analysis", layout="wide")

st.title("🔮 Astro Coach – AI-Based Market Trend & Conversion Analysis")

st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Go to",
    ["Market Trend", "Conversion Drivers", "High-Potential Users", "Churn Risk"]
)


# Load data

daily_demand = pd.read_csv("./data/processed/daily_premium_demand.csv")
forecast = pd.read_csv("./data/processed/premium_demand_forecast.csv")
feature_importance = pd.read_csv("./data/processed/conversion_feature_importance.csv")
user_features = pd.read_csv("./data/processed/user_conversion_scores.csv")
churn_scores = pd.read_csv("./data/processed/premium_churn_scores.csv")
churn_importance = pd.read_csv("./data/processed/churn_feature_importance.csv")

# -------------------------------
# SECTION 1: Market Trend
# -------------------------------
if section == "Market Trend":
    st.header("📈 Premium Subscription Trend & Forecast")

    col1, col2 = st.columns(2)

    with col1:
        
        st.subheader("Historical Demand")
        st.caption("Shows daily count of premium subscriptions.")
        st.line_chart(
            daily_demand.set_index("payment_date")["premium_subscriptions"]
        )

    with col2:
        st.subheader("14-Day Demand Forecast")
        st.caption("Predicted premium subscriptions for the next 14 days.")
        st.line_chart(
            forecast.set_index("date")["predicted_premium_subscriptions"]
        )

    st.markdown(
        """
    **Insight:**  
    Premium subscription demand shows an upward trend, indicating growing user willingness
    to upgrade. This presents an opportunity for targeted campaigns.
    """
    )
    

# -------------------------------
# SECTION 2: Conversion Drivers
# -------------------------------
elif section == "Conversion Drivers":
    st.header("🎯 Key Events Driving Premium Conversion")

    top_features = feature_importance.sort_values(
        by="coefficient", ascending=False
    ).head(10)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(top_features["feature"], top_features["coefficient"])
    ax.invert_yaxis()
    ax.set_xlabel("Impact on Conversion")
    ax.set_title("Top Conversion Drivers")

    st.pyplot(fig)

    st.markdown(
        """
    **Insight:**  
    Intent-driven interactions such as paywall views, prediction exploration, and calendar
    selection are strong indicators of purchase intent.
    """
    )

# -------------------------------
# SECTION 3: High-Potential Users
# -------------------------------
elif section == "High-Potential Users":
    st.header("🧠 High-Potential Free Users for Targeted Offers")

    threshold = st.slider(
        "Conversion Probability Threshold",
        min_value=0.1,
        max_value=0.9,
        value=0.4,
        step=0.05
    )

    if "conversion_probability" in user_features.columns:
        candidates = user_features[
            (user_features["isPremiumUserFlag"] == 0) &
            (user_features["conversion_probability"] >= threshold)
        ]

        st.write(f"Identified **{len(candidates)}** high-potential users")

        st.dataframe(
            candidates[["user_id", "conversion_probability"]]
            .sort_values(by="conversion_probability", ascending=False)
            .head(20)
        )
        st.download_button(
            "Download High-Potential Users",
            candidates.to_csv(index=False),
            file_name="high_potential_users.csv"
        )
    else:
        st.error(
        "Conversion probabilities are missing. Please run the modeling pipeline "
        "to generate `user_conversion_scores.csv`."
        )

    st.markdown(
        """
    **Business Action:**  
    These users should be prioritized for targeted discounts, personalized notifications,
    or limited-time premium offers.
    """
    )

# -------------------------------
# SECTION 4: Premium Churn Risk
# -------------------------------
elif section == "Churn Risk":
    st.header("⚠️ Premium User Churn Risk")

    st.markdown(
        """
    This section identifies premium users who are at risk of not renewing
    their subscription based on declining engagement patterns.
    """
    )
    col1, col2 = st.columns(2)

    with col1:
        total_premium = len(churn_scores)
        st.metric("Total Premium Users", total_premium)

    with col2:
        high_risk = (churn_scores["churn_probability"] >= 0.5).sum()
        st.metric("High Churn Risk Users", high_risk)
    st.subheader("📉 Key Drivers of Churn")

    top_churn_drivers = churn_importance.sort_values(
        by="coefficient", ascending=False
    ).head(10)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(top_churn_drivers["feature"], top_churn_drivers["coefficient"])
    ax.axvline(x=0, linestyle="--", linewidth=1)
    ax.invert_yaxis()
    ax.set_xlabel("Impact on Churn Risk")
    ax.set_title("Top Churn Risk Signals")

    st.pyplot(fig)
    st.subheader("🧠 Premium Users at Risk")

    churn_threshold = st.slider(
        "Churn Risk Threshold",
        min_value=0.1,
        max_value=0.9,
        value=0.5,
        step=0.05
    )

    at_risk_users = churn_scores[
        churn_scores["churn_probability"] >= churn_threshold
    ]

    st.write(f"Identified **{len(at_risk_users)}** premium users at risk")

    st.dataframe(
        at_risk_users[["user_id", "churn_probability"]]
        .sort_values(by="churn_probability", ascending=False)
        .head(20)
    )
    st.download_button(
            "Download premium users at risk",
            at_risk_users.to_csv(index=False),
            file_name="premium_users_at_risk.csv"
        )
    st.markdown(
        """
    **Recommended Actions:**
    - Send renewal reminders to high-risk users
    - Offer loyalty discounts or extended trials
    - Trigger personalized content notifications
    - Prioritize retention before expiry dates
    """
    )


# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown("**Astro Coach AI Project | Market Trend Analysis & User Conversion**")
