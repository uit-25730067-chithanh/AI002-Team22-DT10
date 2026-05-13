<div align="center">
  <img src="docs/assets/hero-banner.png" alt="AI Coffee Farming Banner" width="100%" style="border-radius: 8px;">

# AI-Powered Agricultural Market Analysis (DT10)

**University Project - Artificial Intelligence Thinking (AI002)**  
 _Topic DT10: AI predicting crop planning and coffee prices for farmers._

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

<br/>

## Table of Contents

- [Overview](#overview)
- [Data-to-AI Flow](#data-to-ai-flow)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Team Structure](#team-structure-team-10)

---

## Overview

This project implements an **Artificial Intelligence model** designed to analyze and predict agricultural market prices, specifically focusing on **coffee**. By leveraging historical price data and environmental factors, the system assists farmers in making data-driven farming and financial decisions.

> **Deep Dive Documentation:**
> For an in-depth look at our core system design, including the **5 Pillars of Sustainable AI**, rationale behind our architecture, and detailed team workflows, please refer to our **[Project Design Report (PDR)](./docs/project-overview-pdr.md)**.

---

## Data-to-AI Flow

Luồng hiện tại dùng dữ liệu thật đã xử lý theo tháng để train baseline Random Forest. Raw data crawl rất nhiều nhưng nằm trong `data/raw/` và bị gitignore, nên model trong repo không train trực tiếp từ raw file. Team 2 chọn `data/processed/monthly/coffee_environment_all_areas_monthly_2022_2025.csv` vì độ phủ giá thật ổn định hơn, dễ giải thích hơn và phù hợp mục tiêu KISS của môn học.

```mermaid
flowchart TD
    A[Phúc và Thịnh crawl giá cà phê] --> B[Raw daily price data]
    C[Dữ liệu thời tiết theo khu vực] --> D[Daily weather features]
    E[Thông tin đất theo khu vực] --> F[Static soil features]

    B --> G[Build processed datasets]
    D --> G
    F --> G

    G --> H[Weekly processed dataset]
    G --> I[Monthly processed dataset]
    G --> J[Area real price ranking]

    H --> K[Tham khảo và future experiment]
    J --> L[Kiểm tra coverage theo khu vực]
    I --> M[Thanh train baseline Random Forest]

    M --> N[model/best_model]
    N --> O[FastAPI /predict]
    O --> P[Frontend demo]
```

### Dataset chính hiện tại

| Mục                 | Giá trị                                                                     |
| :------------------ | :-------------------------------------------------------------------------- |
| File train chính    | `data/processed/monthly/coffee_environment_all_areas_monthly_2022_2025.csv` |
| Số dòng             | 576                                                                         |
| Số cột              | 16                                                                          |
| Tần suất            | Monthly                                                                     |
| Train/Test          | Train 2022-2024, Test 2025                                                  |
| Model baseline      | `RandomForestRegressor`                                                     |
| Best model metadata | `model/best_model/metadata.json`                                            |

### Trách nhiệm theo team

```mermaid
flowchart LR
    A[Team 1: Phúc và Thịnh<br/>Crawler + Frontend] --> B[Processed datasets]
    B --> C[Thanh<br/>Preprocess + Train RF + API contract]
    C --> D[Sơn<br/>Evaluation + Robustness + 5 Pillars]
    C --> E[Frontend gọi /predict]
    D --> F[Báo cáo kỹ thuật]
    E --> G[Demo end-to-end]
    F --> G
```

Tài liệu chi tiết:

- [Team data flow roadmap](./docs/discussions/2026-05-13-team-data-flow-roadmap.md)
- [Project roadmap](./docs/project-roadmap.md)
- [API handoff real data model](./docs/discussions/2026-05-13-api-handoff-team2-real-data.md)
- [Sơn evaluation pack summary](./docs/discussions/2026-05-13-son-evaluation-pack-summary.md)
- [5 Pillars checkpoint](./docs/discussions/5-pillars-checkpoint.md)

---

## Tech Stack

| Category               | Technologies                                                                                                                                                                                                                                                                   |
| :--------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Backend / API**      | ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi) ![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)                                                                                                  |
| **Machine Learning**   | ![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white) ![XGBoost](https://img.shields.io/badge/XGBoost-111111?style=flat-square&logo=xgboost)                                                                  |
| **Data Processing**    | ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas) ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy)                                                                                                           |
| **Frontend / Crawler** | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3) ![Vanilla JS](https://img.shields.io/badge/Vanilla_JS-F7DF1E?style=flat-square&logo=javascript&logoColor=black) |
| **Storage**            | ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite) ![CSV](https://img.shields.io/badge/CSV-107C41?style=flat-square&logo=microsoftexcel&logoColor=white)                                                                                      |

---

## Project Structure

```text
AI002_PROJECT/
│
├── docs/                           # Documentation (PDR, Slides, References)
├── data/                           # Datasets (Ignored in Git)
│   ├── raw/                        # Raw scraped data (gitignored)
│   ├── processed/                  # Cleaned & processed data
│   └── external/                   # Optional external data sources
│
├── crawler/                        # Data crawling & scraping scripts
├── notebooks/                      # Jupyter Notebooks for EDA & Prototyping
│
├── model/                          # AI/ML Core (Team 2)
│   ├── preprocess.py               # Data cleaning, feature engineering, temporal split
│   ├── train_rf.py                 # Random Forest baseline training + evaluation
│   ├── train_xgboost.py            # Optional XGBoost comparison (requires venv)
│   ├── stress_test.py              # Robustness stress test (Black Swan scenarios)
│   └── best_model/                 # Promoted model metadata and .pkl artifact
│
├── backend/                        # API Server (Team 2)
│   ├── main.py                     # FastAPI entry point
│   ├── api/routes.py               # Endpoints: /health, /predict, /model/info
│   ├── schemas/prediction.py       # Pydantic request/response validation
│   └── services/predictor.py       # Model loading, inference, explanations
│
├── tests/ai-tests/                 # Pytest suite
│   └── test_predictor_service.py   # PredictorService unit tests
│
└── frontend/                       # Web Interface (Team 1)
```

> _For detailed team responsibilities across these modules, see the [Team Workflows](./docs/project-overview-pdr.md#4-phân-công-công-việc)._

---

## Getting Started

### 1. Prerequisites

Ensure you have the following installed:

- **Python 3.9+**
- **Git**

### 2. Installation

Clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd AI002_PROJECT

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Running the Backend API

Start the FastAPI server (supports running from project root or `backend/`):

```bash
uvicorn backend.main:app --reload
# or: cd backend && uvicorn main:app --reload
```

**API Endpoints:**

| Endpoint      | Method | Description                                                  |
| :------------ | :----- | :----------------------------------------------------------- |
| `/health`     | GET    | Check API status and model load state                        |
| `/predict`    | POST   | Predict coffee price with confidence interval + explanations |
| `/model/info` | GET    | Model metadata (version, features, training timestamp)       |

**Tip:** Navigate to `http://localhost:8000/docs` for interactive Swagger UI.

### 4. Running Tests

```bash
# Predictor service tests (skip gracefully if model not yet trained)
python3 -m pytest tests/ai-tests/test_predictor_service.py -q
```

### 5. Training the Baseline Model

```bash
# Train Random Forest baseline trên data thật monthly
python3 model/train_rf.py --data data/processed/monthly/coffee_environment_all_areas_monthly_2022_2025.csv --tag rf_real_monthly

# Optional only: XGBoost comparison (install in a separate venv)
python3 model/train_xgboost.py --data data/processed/monthly/coffee_environment_all_areas_monthly_2022_2025.csv

# Xem lịch sử experiments
cat model/experiments.csv
```

### 6. Running the Web UI

Simply open `frontend/index.html` in your preferred web browser to view the dashboard.

---

## Team Structure (Team 10)

|    Team    | Members      | Responsibilities                                              |
| :--------: | :----------- | :------------------------------------------------------------ |
| **Team 1** | Phúc & Thịnh | Data Crawling, Frontend UI Development, Presentation Slides   |
| **Team 2** | Thanh & Sơn  | Core ML Engineering, Model Training & Evaluation, Backend API |

<br/>

<div align="center">
  <i>Built with passion for Sustainable Agriculture.</i>
</div>
