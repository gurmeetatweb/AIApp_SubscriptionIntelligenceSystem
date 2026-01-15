# Astro Coach — AI Decision Intelligence Platform  
**AI-Driven Subscription Intelligence System**

---

## 1. Project Overview

This project delivers an **AI-powered Decision Intelligence Platform** for **Astro Coach**, a freemium mobile application offering astrology services.

Unlike traditional analytics dashboards that only report historical performance, Astro Coach transforms data into **actionable business decisions** by combining:

- Predictive analytics  
- Behavioral intelligence  
- Scenario-based simulations  

The system enables leadership teams to **anticipate outcomes, evaluate strategies, and act with confidence**.

---

## 2. Business Objectives

The platform addresses three strategic business challenges:

1. **Growth Planning**  
   *How will premium demand evolve, and when should campaigns be launched?*

2. **Targeted Acquisition**  
   *Which free users show the highest likelihood of conversion?*

3. **Revenue Protection**  
   *Which premium users are at risk of churn, and how early can intervention begin?*

---

## 3. Data Sources

Three primary datasets power the system:

1. **User Subscription Data**  
2. **Payment History**  
3. **User Analytics / Event Logs**

Together, they provide a comprehensive view of:

- User lifecycle  
- Engagement behavior  
- Monetization outcomes  

---

## 4. Event Consolidation Strategy

Raw application events are often **highly correlated** and represent similar user behaviors.  
To improve interpretability and reduce noise, events are consolidated into **behavioral signals**.

| Behavioral Feature | Raw Events Grouped |
|-------------------|------------------|
| `engagement_activity` | app background/foreground, splash screen, home screen |
| `player_interaction` | Player_DwnS, Player_Dwn, meditation track selection |
| `prediction_engagement` | daily prediction view, prediction expand |
| `navigation_intent` | calendar/day selection |

This approach ensures that the AI models focus on **intent**, not just activity volume.

---

## 5. Modeling Approach

### 5.1 Conversion Intelligence
- **Model:** Logistic Regression  
- **Purpose:** Identify free users with high probability of upgrading  

### 5.2 Premium Demand Forecasting
- **Model:** Time-series forecasting (LSTM for modeling, trend-focused outputs in dashboard)  
- **Purpose:** Capture short-term demand direction for campaign planning  

### 5.3 Churn Risk Prediction
- **Model:** Logistic Regression  
- **Purpose:** Flag premium users showing early disengagement signals  

---

## 6. Decision Intelligence Layer

Beyond predictions, Astro Coach introduces a **Decision Intelligence layer** that supports leadership thinking through:

- **Targeting Simulator** – selects optimal free-user segments for campaigns  
- **Event Impact Simulator** – evaluates how changes in user behavior affect conversions  
- **Churn Impact Simulator** – estimates retention gains from intervention strategies  

These modules transform AI outputs into **strategy-testing tools** for business teams.

---

## 7. Outputs Generated

| File | Purpose |
|------|---------|
| `user_engagement_features.csv` | Consolidated behavioral signals |
| `user_conversion_scores.csv` | Conversion probability by user |
| `premium_churn_scores.csv` | Churn risk by premium user |
| `daily_premium_demand.csv` | Historical premium demand |
| `premium_demand_forecast.csv` | Short-term demand forecast |
| `conversion_feature_importance.csv` | Key drivers of conversion |
| `churn_feature_importance.csv` | Key drivers of churn |

---

## 8. Platform Capabilities

The Streamlit dashboard includes:

- **Executive Overview** – business KPIs and outlook  
- **Market Trend Intelligence** – historical demand and forecasts  
- **Conversion Intelligence** – behavioral drivers of purchase intent  
- **Targeting Simulator** – precision campaign planning  
- **Churn Early Warning** – proactive risk detection  
- **Event Impact Simulator** – what-if conversion analysis  
- **Churn Impact Simulator** – retention strategy testing  

Each module is mapped to a **specific leadership decision**.

---

## 9. Project Structure

```text
astro-coach-ai/
│
├── data/
│   ├── raw/
│   │   ├── subscribed_users.csv
│   │   ├── payment_history.csv
│   │   └── analytics_events.csv
│   └── processed/
│       ├── daily_premium_demand.csv
│       ├── user_conversion_scores.csv
│       ├── premium_churn_scores.csv
│       ├── conversion_feature_importance.csv
│       └── churn_feature_importance.csv
│
├── notebooks/
│   ├── data.ipynb           # Data preparation & EDA
│   └── model.ipynb          # Model development & training
│
├── app/
│   └── streamlit_app.py     # Decision intelligence dashboard
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 10. How to Run

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run the Streamlit app
```bash
streamlit run app/streamlit_app.py
```

---

## 11. Evaluation Philosophy

This project prioritizes:

- **Explainability over black-box accuracy**  
- **Business relevance over technical complexity**  
- **Decision support over automation**  
- **End-to-end AI lifecycle execution**  

Astro Coach is designed as a **leadership enablement platform**, not merely a predictive model.
