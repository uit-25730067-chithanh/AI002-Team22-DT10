<div align="center">
  <img src="docs/assets/hero-banner.png" alt="AI Coffee Farming Banner" width="100%" style="border-radius: 8px;">

  # AI-Powered Agricultural Market Analysis (DT10)

  **University Project - Artificial Intelligence Thinking (AI002)**  
  *Topic DT10: AI predicting crop planning and coffee prices for farmers.*

  [![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
  [![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

<br/>

## Table of Contents
- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Team Structure](#team-structure)

---

## Overview

This project implements an **Artificial Intelligence model** designed to analyze and predict agricultural market prices, specifically focusing on **coffee**. By leveraging historical price data and environmental factors, the system assists farmers in making data-driven farming and financial decisions.

> **Deep Dive Documentation:**
> For an in-depth look at our core system design, including the **5 Pillars of Sustainable AI**, rationale behind our architecture, and detailed team workflows, please refer to our **[Project Design Report (PDR)](./docs/project-overview-pdr.md)**.

---

## Tech Stack

| Category | Technologies |
| :--- | :--- |
| **Backend / API** | ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi) ![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python) |
| **Machine Learning** | ![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white) ![XGBoost](https://img.shields.io/badge/XGBoost-111111?style=flat-square&logo=xgboost) ![Prophet](https://img.shields.io/badge/Prophet-00A9E0?style=flat-square) |
| **Data Processing** | ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas) ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy) |
| **Frontend / Crawler** | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3) ![Vanilla JS](https://img.shields.io/badge/Vanilla_JS-F7DF1E?style=flat-square&logo=javascript&logoColor=black) |
| **Storage** | ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite) ![CSV](https://img.shields.io/badge/CSV-107C41?style=flat-square&logo=microsoftexcel&logoColor=white) |

---

## Project Structure

```text
AI002_PROJECT/
│
├── docs/                           # Documentation (PDR, Slides, References)
├── data/                           # Datasets (Ignored in Git)
│   ├── raw/                        # Raw scraped data
│   ├── processed/                  # Cleaned & processed data
│   └── external/                   # External data sources
│
├── crawler/                        # Data crawling & scraping scripts
├── notebooks/                      # Jupyter Notebooks for EDA & Prototyping
│
├── model/                          # AI/ML Core (Team 2)
│   ├── training/                   # Model training scripts
│   ├── evaluation/                 # Model evaluation metrics
│   └── saved/                      # Serialized models (.pkl, .joblib)
│
├── backend/                        # API Server (Team 2)
│   ├── main.py                     # FastAPI entry point
│   ├── api/                        # Route definitions
│   └── services/                   # Business & inference logic
│
└── frontend/                       # Web Interface (Team 1)
```

> *For detailed team responsibilities across these modules, see the [Team Workflows](./docs/project-overview-pdr.md#4-phân-công-công-việc).*

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

Start the FastAPI server:
```bash
cd backend
uvicorn main:app --reload
```
**Tip:** Once running, navigate to `http://localhost:8000/docs` to interact with the auto-generated Swagger UI and test the prediction endpoints.

### 4. Running the Web UI

Simply open `frontend/index.html` in your preferred web browser to view the dashboard.

---

## Team Structure (Team 10)

| Team | Members | Responsibilities |
| :---: | :--- | :--- |
| **Team 1** | Phúc & Thịnh | Data Crawling, Frontend UI Development, Presentation Slides |
| **Team 2** | Thanh & Sơn | Core ML Engineering, Model Training & Evaluation, Backend API |

<br/>

<div align="center">
  <i>Built with passion for Sustainable Agriculture.</i>
</div>
