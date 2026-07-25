<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:FF6A00,100:1a1a1a&height=180&section=header&text=TransReliant&fontSize=55&fontColor=ffffff&animation=fadeIn&fontAlignY=38" width="100%"/>

<p><em>ML-Based Transport Reliability &amp; Risk Prediction System</em></p>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=20&duration=3000&pause=800&color=FF6A00&center=true&vCenter=true&width=700&lines=Predicting+journey+reliability+before+you+book.;Confirmation+plus+Delay+plus+Reliability+Score.;Deployed+and+live+on+Render" alt="Typing SVG" />

<br/>

<p>
<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
<img src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
<img src="https://img.shields.io/badge/scikit--learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" />
<img src="https://img.shields.io/badge/XGBoost-Model-016A70?style=for-the-badge" />
</p>

<p>
<img src="https://img.shields.io/badge/status-live-brightgreen?style=for-the-badge" />
<img src="https://img.shields.io/website?url=https%3A%2F%2Ftransreliant.onrender.com&style=for-the-badge&label=deployment" />

</p>

<br/>

### 🔗 [**Launch Live App → transreliant.onrender.com**](https://transreliant.onrender.com)

*No signup. No setup. Enter a journey, get a reliability score in seconds.*

</div>

---

## 📖 Overview

**TransReliant** is a Machine Learning + MLOps system that quantifies transport reliability *before* a journey happens. It answers three questions for any user, instantly:

| # | Question | Output |
|---|---|---|
| 1 | Will my ticket get confirmed? | Confirmation probability + label |
| 2 | How delayed will this transport be? | Predicted delay (minutes) + severity |
| 3 | How reliable is this route overall? | Unified Reliability Score (0–100) |

The system combines **classification**, **regression**, and **feature-engineered reliability scoring** into a single served pipeline — trained, containerized, and deployed end-to-end.

---

## 🚀 Live Deployment

| | |
|---|---|
| **Status** | 🟢 Live |
| **URL** | [`transreliant.onrender.com`](https://transreliant.onrender.com) |
| **Hosting** | Render (Docker Web Service) |
| **Frontend** | Served directly from FastAPI (same-origin, single deployment) |
| **API Docs** | [`/docs`](https://transreliant.onrender.com/docs) — interactive Swagger UI |
| **Health Check** | [`/health`](https://transreliant.onrender.com/health) |

> ⚠️ Hosted on Render's free tier — the instance sleeps after ~15 minutes of inactivity. First request after idle may take 30–50s to wake up.

---

## 🏗️ System Architecture

```
┌────────────┐     ┌─────────┐     ┌────────────────┐     ┌──────────────────────┐
│ User Input │ ──▶ │ FastAPI │ ──▶ │ Resolver +      │ ──▶ │    ML Model Layer     │
│ (Frontend) │     │  Route  │     │ Feature Builder │     │ (Classifier + Regressor)│
└────────────┘     └─────────┘     └────────────────┘     └──────────┬────────────┘
                                                                       ▼
                                                            ┌───────────────────────┐
                                                            │  Reliability Engine    │
                                                            │  (weighted scoring)    │
                                                            └──────────┬────────────┘
                                                                       ▼
                                                            ┌───────────────────────┐
                                                            │   JSON Response        │
                                                            └───────────────────────┘
```

> Fully containerized with **Docker**, served as a single deployable unit on Render.

---

## 🤖 ML Models

<table>
<tr>
<th width="50%">🟢 Model 1 — Ticket Confirmation</th>
<th width="50%">🔵 Model 2 — Delay Prediction</th>
</tr>
<tr>
<td valign="top">

**Type:** Classification (`XGBClassifier`)

- GridSearchCV hyperparameter tuning
- OneHot + Ordinal encoding pipeline
- 5-fold cross-validation

**Evaluated on:**
`F1-score` · `Accuracy` · `ROC-AUC`

</td>
<td valign="top">

**Type:** Regression (`XGBRegressor`)

- GridSearchCV hyperparameter tuning
- Consistent preprocessing pipeline
- 5-fold cross-validation

**Evaluated on:**
`MAE` · `MSE`

</td>
</tr>
</table>

---

## 🧬 Feature Engineering

| Feature | Description |
|---|---|
| Waitlist position | Numeric confirmation-risk signal |
| Peak / holiday season flag | Derived from journey month + weekday |
| Seasonality encoding | Month and day-of-week extraction |
| Route-based lookups | Train type, seat availability, distance, station data |
| Reliability weighting | Confirmation, delay, and historical signals combined |

---

## 📊 Reliability Score

A single **0–100 score**, computed from three weighted signals:

```
Reliability Score = 0.5 × confirmation_probability
                   + 0.3 × delay_reliability
                   + 0.2 × historical_score
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/predict` | Full prediction — confirmation, delay, reliability |
| `GET` | `/health` | Service health check |
| `GET` | `/docs` | Interactive Swagger API documentation |

**Example request:**
```bash
curl -X POST https://transreliant.onrender.com/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "user": {
      "train_number": 51450,
      "source_station": "NDLS",
      "destination_station": "CSMT",
      "date_of_journey": "2026-08-15",
      "class_of_travel": "3A",
      "number_of_passengers": 2,
      "waitlist_position": 0
    }
  }'
```

**Example response:**
```json
{
  "ticket": { "confirmation_probability": 66.24, "confirmation_label": "Medium" },
  "delay": { "delay_minutes": 48.04, "delay_readable": "48m", "delay_label": "Moderate" },
  "reliability": { "score": 69.21, "label": "Moderate Reliability" }
}
```

---

## ⚙️ Engineering & MLOps

- ✅ Model persistence via `joblib`
- ✅ Docker containerization, deployed on Render
- ✅ Frontend + backend served from a single container (no CORS overhead)
- ✅ Clean modular repo — routes, services, schemas, core logic separated
- ✅ Pydantic-validated request/response contracts

---

## 📁 Repository Structure

```
TransReliant/
├── backend/
│   ├── api/routes/         # FastAPI route handlers
│   ├── ml/                 # Trained models + training pipeline
│   ├── transport/
│   │   ├── core/           # Reliability scoring logic
│   │   ├── schemas/        # Request / response models
│   │   ├── services/       # Prediction orchestration
│   │   └── utils/          # Resolver, train lookup, encoders
│   ├── data/                # Raw + processed datasets
│   └── config.yaml
├── frontend/
│   └── index.html           # Served directly by FastAPI
├── tests/
├── Dockerfile
└── README.md
```

---

## 🛠️ Tech Stack

`Python` · `FastAPI` · `XGBoost` · `scikit-learn` · `Pandas` · `Docker` · `Render` · `Pydantic`

---

## 💼 Resume Description

> Designed, trained, and deployed a production ML system predicting ticket confirmation probability, delay risk, and a composite transport reliability score — built with FastAPI, XGBoost, and Docker, containerized and live-deployed on Render with a unified frontend + backend architecture.

---

<div align="center">

**Built by [Nithish Kumar](https://github.com/nithishkumar-dev-10)**

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1a1a1a,100:FF6A00&height=100&section=footer&animation=fadeIn" width="100%"/>

</div>
