# Astro Coach — AI for Market Trend Analysis  
**AI-Driven Subscription Intelligence System**

---

## 1. Project Overview

This project builds an **end-to-end AI system** to support data-driven decision-making for **Astro Coach**, a freemium mobile application that provides astrology services to users.

The system analyzes historical user behavior, payment records, and in-app events to:

- Forecast **premium subscription demand**
- Identify **behavioral drivers of conversion**
- Predict **churn risk** among premium users
- Enable **targeted promotions and retention strategies**

The emphasis of this project is not on perfect accuracy, but on **correct execution of the full AI lifecycle** — from data preparation to actionable business insights.

---

## 2. Business Objectives

The project addresses three core business questions:

1. **Growth Planning**  
   *Is premium demand increasing, and how should campaigns be timed?*

2. **Targeted Acquisition**  
   *Which free users are most likely to subscribe if given the right offer?*

3. **Revenue Protection**  
   *Which premium users are at risk of churn and need early intervention?*

---

## 3. Data Sources

Three datasets are used:

1. **User Subscription Data**  
2. **Payment History**  
3. **User Analytics / Event Logs**

Together, these datasets provide a complete view of:
- User lifecycle  
- Engagement behavior  
- Monetization outcomes  

---

## 4. Event Consolidation Strategy

Raw application events are often **highly correlated** and represent the same underlying user behavior.  
To reduce redundancy and improve interpretability, events are consolidated into **behavioral signals**:

| Behavioral Feature | Raw Events Grouped |
|-------------------|------------------|
| `engagement_activity` | app background/foreground, splash screen, home screen |
| `player_interaction` | Player_DwnS, Player_Dwn, meditation track selection |
| `prediction_engagement` | daily prediction view, prediction expand |
| `navigation_intent` | calendar/day selection |

---

## 5. Modeling Approach

### 5.1 Conversion Prediction
- **Model:** Logistic Regression  
- **Purpose:** Identify high-intent free users  

### 5.2 Premium Demand Forecasting
- **Model:** LSTM (7-day sliding window)  
- **Purpose:** Capture trend direction  

### 5.3 Churn Risk Prediction
- **Model:** Logistic Regression  
- **Purpose:** Identify premium users at risk  

---

## 6. Outputs Generated

| File | Purpose |
|------|---------|
| `user_engagement_features.csv` | Behavioral features |
| `user_conversion_scores.csv` | Conversion probabilities |
| `premium_churn_scores.csv` | Churn risk |
| `daily_premium_demand.csv` | Historical demand |
| `premium_demand_forecast.csv` | Demand forecast |

---

## 7. Project Structure
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
│       ├── user_features.csv
│       └── training_data.csv
│
├── notebooks/
│   ├── data.ipynb           # Data Preparation & EDA
│   └── model.ipynb          # Model Development & Training
│
├── app/
│   └── streamlit_app.py     # Interactive Dashboard
│
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
└── README.md               # Project documentation
```



## 8. How to Run

### Install dependencies
```bash
pip install -r requirements.txt
```
### Run Streamlit app

```bash
streamlit run app/streamlit_app.py
```
### 9. Evaluation Philosophy

- This project prioritizes:

- Explainability over black-box accuracy

- Business relevance over technical complexity

- End-to-end AI lifecycle execution

