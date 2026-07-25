<div align="center">

# 🚆 TransReliant

### ML-Based Transport Reliability & Risk Prediction System

<p>
<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=flat-square&logo=fastapi&logoColor=white" />
<img src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat-square&logo=docker&logoColor=white" />
<img src="https://img.shields.io/badge/scikit--learn-ML-F7931E?style=flat-square&logo=scikit-learn&logoColor=white" />
<img src="https://img.shields.io/badge/SHAP-Explainability-8A2BE2?style=flat-square" />
<img src="https://img.shields.io/badge/status-active-success?style=flat-square" />
</p>

*Predicting whether your journey will actually go to plan — before you book it.*

</div>

---

## 📖 Overview

**TransReliant** is a Machine Learning + MLOps based system that quantifies transport reliability before a journey even happens. It answers three questions for a user:

| # | Question | Output |
|---|---|---|
| 1 | Will my ticket get confirmed? | Confirmation probability |
| 2 | How delayed will this transport be? | Delay risk (minutes) |
| 3 | How reliable is this route overall? | Reliability Score (0–100) |

The system combines **classification**, **regression**, **explainability**, and **deployment** into a single served pipeline using FastAPI and Docker.

---

## 🎯 Problem Statement

Public transport systems carry built-in uncertainty — ticket confirmations and delays are unpredictable, and users have no data-backed way to gauge a journey's reliability before planning around it. TransReliant closes that gap with a single predictive reliability metric, generated from historical patterns rather than guesswork.

---

## 🏗️ System Architecture

```
┌────────────┐     ┌─────────┐     ┌────────────────┐     ┌───────────────────┐
│ User Input │ ──▶ │ FastAPI │ ──▶ │ Preprocessing + │ ──▶ │   ML Model Layer   │
└────────────┘     └─────────┘     │Feature Engineer.│     │ (Classify + Regress)│
                                    └────────────────┘     └─────────┬──────────┘
                                                                      ▼
                                                            ┌───────────────────┐
                                                            │  Explainability    │
                                                            │  (SHAP / Feature   │
                                                            │   Importance)      │
                                                            └─────────┬──────────┘
                                                                      ▼
                                                            ┌───────────────────┐
                                                            │  Reliability Index │
                                                            └─────────┬──────────┘
                                                                      ▼
                                                            ┌───────────────────┐
                                                            │ Response + Logging │
                                                            └───────────────────┘
```

> Entire pipeline is containerized with **Docker** for reproducible, portable deployment.

---

## 🤖 ML Models

<table>
<tr>
<th width="50%">🟢 Model 1 — Ticket Confirmation</th>
<th width="50%">🔵 Model 2 — Delay Prediction</th>
</tr>
<tr>
<td valign="top">

**Type:** Classification

- Logistic Regression
- Random Forest
- Gradient Boosting

**Evaluated on:**
`ROC-AUC` · `Precision` · `Recall` · `F1-score`

</td>
<td valign="top">

**Type:** Regression

- Random Forest Regressor
- Gradient Boosting Regressor

**Evaluated on:**
`MAE` · `RMSE` · `Cross-validation`

</td>
</tr>
</table>

---

## 🧬 Feature Engineering

| Feature | Description |
|---|---|
| WL number encoding | Waitlist number transformed into a usable numeric signal |
| Festival indicator | Flags high-demand festival/holiday periods |
| Seasonality encoding | Month and day-of-week cyclic encoding |
| Lag features | Previous delay trends carried forward |
| Historical route confirmation ratio | Past confirmation rate per route |
| Route demand index | Relative demand pressure on a given route |

---

## 🔍 Explainability Layer

Predictions aren't a black box — every response can surface *why* the model decided what it decided.

- Feature importance analysis
- SHAP values *(optional, per-request)*
- Top influencing factors returned directly in the API response

---

## 📊 Reliability Score

A single **0–100 score** computed from three weighted signals:

```
Reliability Score = f(
    confirmation_probability,   # weighted
    delay_reliability,          # converted from predicted delay minutes
    historical_route_reliability
)
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/predict/train` | Predict ticket confirmation probability |
| `POST` | `/predict/delay` | Predict expected delay |
| `GET` | `/health` | Service health check |

---

## ⚙️ MLOps Components

- ✅ Model persistence via `joblib` / `pickle`
- ✅ Docker containerization for deployment
- ✅ Prediction logging for monitoring & retraining
- ✅ Structured, modular repository design

---

## 📁 Repository Structure

```
TransReliant/
├── data/
├── notebooks/
├── src/
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── train.py
│   └── predict.py
├── api/
├── models/
├── Dockerfile
└── README.md
```

---

## 💼 Resume Description

> Designed and deployed a predictive ML + MLOps system estimating ticket confirmation probability, delay risk, and transport reliability score using classification, regression, explainability, FastAPI deployment, and Docker containerization.

---

<div align="center">

**Built by [Nithish Kumar](https://github.com/nithishkumar-dev-10)**

</div>
