# ⚡ Global Assets Settlement System (GASS) 🇻🇪
### Enterprise-grade Data Pipeline for Multi-Currency Asset Liquidation

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Financial Integration](https://img.shields.io/badge/API-BCV_Real--Time-green?style=for-the-badge)](https://pypi.org/project/pyBCV/)

**GASS** is a specialized financial tool designed to solve the complexity of **Digital Asset Reconciliation** in high-inflation economies. It automates the extraction, transformation, and auditing of asset datasets to calculate precise liquidation values in local currency (VES).

---

### 🛠️ Technical Architecture & Data Engineering
This project demonstrates advanced Python concepts applied to financial data integrity:

* **ETL Pipeline:** * **Extraction:** Dynamic scanning of the `/data` directory using `pathlib` for automated file discovery.
* **Transformation:** Leveraging `Pandas` for vectorized operations to categorize assets into **Type 1 (Micro-points)** and **Type 2 (Nominal USD)**.
* **Loading:** Generation of timestamped, audit-ready reports in `.xlsx` format for financial traceability.
* **API Integration & Error Handling:** Implementation of the `pyBCV` library to fetch official exchange rates with custom logic to handle API latency, data parsing, and connectivity failovers.
* **Modular Financial Logic:** * **Audit Filtering:** Algorithmic exclusion of non-liquidable internal bonuses (Audit Integrity).
* **Market Spread Correction:** Implementation of a **1.824 Spread Factor** to bridge the gap between official BCV rates and real-world P2P market liquidity.

---

### 🔄 Data Lifecycle
1. **Ingestion**: Automated extraction of `.xlsx` datasets from the `/data` directory.
2. **Validation**: API handshake with `pyBCV` for real-time rate acquisition (with manual failover).
3. **Processing**: Vectorized cleaning (removal of non-liquidable bonuses) and currency conversion.
4. **Output**: Generation of persistent audit logs and settlement summaries in `/history_reports`.

---

### 📊 Financial Algorithm Breakdown
To ensure a **75% Liquidity Rate** in secondary markets, the system follows this mathematical pipeline:

| Stage | Logic / Implementation | Technical Context |
| :--- | :--- | :--- |
| **Gross Equity** | `Σ(Type_1 / 100) + Σ(Type_2)` | Multi-denominational asset aggregation. |
| **Market Adjustment** | `Gross * 0.75` | P2P Liquidation Index application. |
| **Net Settlement** | `Adj_Amount * 0.90` | Automatic 10% operational fee deduction. |
| **VES Conversion** | `Net * (BCV_Rate * 1.824)` | Official rate alignment with market spread. |
| **Purchasing Power**| `Final_VES / BCV_Rate` | Real-value KPI for owner transparency. |

---

### 📂 Repository Structure
```text
Global-Assets-Settlement-System-GASS/
├── data/               # Source Excel datasets (Input)
├── history_reports/    # Automated Audit & Payout Reports (Output)
├── main.py             # Entry point: Controller & Financial Logic
├── requirements.txt    # Managed dependencies
└── LICENSE             # MIT License
```

---

### 🚀 Implementation & Usage

1. **Environment Setup:**
```bash
git clone https://github.com/DxGodoy-dev/Global-Assets-Settlement-System-GASS.git
pip install -r requirements.txt
```
2. **Data Standardization:**
The engine expects `.xlsx` files with a schema of `[date, description, amount, platform]`. The system automatically handles data cleaning for missing values.

3. **Execution:**
```bash
python main.py
```

---

### 🧠 Engineering Mindset: Why GASS?
In the Venezuelan fintech landscape, **data accuracy is non-negotiable**. GASS was built to eliminate manual calculation errors in payroll settlement. It demonstrates my ability to:
1. **Handle Real-world Financial APIs:** Seamlessly integrating external data sources into local business logic.
2. **Apply Mathematical Models:** Implementing complex spread and liquidity factors to volatile markets.
3. **Create Scalable CLI Tools:** Developing robust interfaces for efficient data auditing and reporting.

---

### 🔧 Code Highlights & Architecture
- **Vectorized Data Processing:** Utilizes `Pandas` for filtering and aggregating multi-account datasets, ensuring O(n) performance.
- **Resilient API Consumption:** Implements a `try-except` failover system for real-time exchange rate fetching with a manual override fallback.
- **Audit Traceability:** Automatically generates sanitized reports using automated string-stream processing for transparent financial record-keeping.

---
<p align="center">
  <b>Developed by Daniel Godoy</b><br>
  <i>Data Engineer & Python Specialist | Bilingual (EN/ES)</i>
</p>

> [!IMPORTANT]
> **Disclaimer:** This tool is for educational purposes. All financial logic (rates/fees) is based on specific secondary market conditions.