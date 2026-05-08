# 🌍 End-to-End Weather Data Engineering Pipeline

An automated data pipeline that fetches, cleans, and analyzes global weather patterns using a **Medallion Architecture**. This project demonstrates the full lifecycle of data—from raw API ingestion to interactive visualization.

![Image](https://github.com/user-attachments/assets/49b05989-3313-45db-b02f-0bccf697ea42)

## 🚀 Project Highlights

* **Automated Ingestion:** Fetches real-time weather data (temperature, rain, wind) for multiple global cities via REST API.
* **Medallion Architecture:** Implements a structured data lake approach with Bronze (Raw), Silver (Cleaned), and Gold (Aggregated) layers.
* **Storage Optimization:** Converts nested JSON data into **Apache Parquet** format for efficient columnar storage and high-speed querying.
* **Analytical Engine:** Utilizes **DuckDB** for high-performance SQL transformations and KPI generation.
* **Data Visualization:** Built an interactive **Streamlit** dashboard for business-ready insights.

## 🛠 Tech Stack

* **Language:** Python 3.x
* **Data Ingestion:** Requests (REST API)
* **Data Processing:** Pandas, PyArrow
* **Database & SQL:** DuckDB
* **Visualization:** Streamlit, Plotly
* **API:** Open-Meteo Historical/Forecast API

## 🏗 Pipeline Architecture

1. **Bronze Layer:** Raw data ingestion. The script handles API requests and saves raw JSON responses to ensure data provenance.
2. **Silver Layer:** Data cleaning and schema enforcement. Nested JSON is flattened into a tabular format, timestamps are standardized, and data is stored as Parquet.
3. **Gold Layer:** Business logic and aggregations. SQL queries calculate daily metrics like temperature ranges and rainfall totals.

---

## ⚙️ How It Works (Under the Hood)

This pipeline is built using modular Python scripts, ensuring that each step of the ETL process is isolated, idempotent, and easy to debug.

### 1. The Ingestion Engine (`extract.py`)

To handle API rate limits and ensure we capture the raw state of the data, the ingestion script uses the `requests` library to fetch nested JSON data.

* **Idempotency:** The script dynamically generates filenames based on the city. If run multiple times, it safely overwrites the raw file rather than creating duplicates.
* **Error Handling:** It validates the HTTP response status (`200 OK`) before attempting to parse and save the data to the `data/bronze/` directory.

### 2. The Transformation Logic (`transform.py`)

APIs rarely return data in a database-ready format. The Open-Meteo API returns timestamps and temperatures in separate, parallel arrays.

* **Flattening:** We use **Pandas** to extract the `hourly` dictionary and automatically align the parallel arrays into tabular columns.
* **Feature Engineering & Typing:** We dynamically inject the `city` name derived from the file name, and explicitly cast the `time` string into a native Pandas `datetime` object.
* **Columnar Storage:** Instead of saving as a bulky CSV, the cleaned DataFrame is serialized into **Apache Parquet**. This reduces file size significantly and optimizes it for analytical queries.

### 3. The Analytical Engine (`analytics.py`)

Rather than loading the data into a heavy database server, we use **DuckDB**—an in-process SQL OLAP database.

* **Direct-to-Parquet Querying:** DuckDB executes SQL *directly* against the `cleaned_weather.parquet` file without needing an intermediate database load step.
* **Aggregations:** We use SQL `GROUP BY` clauses to roll up thousands of hourly rows into daily summaries, calculating the `MAX`, `MIN`, and `AVG` temperatures, alongside `SUM` for total daily rainfall.
* **Materialization:** The final aggregated query is materialized into a lightweight CSV in the `data/gold/` layer, optimized specifically for the dashboard to read quickly.

### 4. The Dashboard (`app.py`)

The frontend is built with **Streamlit**.

* **Performance:** It uses the `@st.cache_data` decorator to cache the Gold layer data in memory, preventing the app from reloading the dataset every time a user clicks a filter.
* **Interactivity:** We use **Plotly Express** to render responsive, interactive charts that allow users to hover over data points for exact metrics.

---

## 📂 Repository Structure

```text
├── data/               # Local data lake (Bronze, Silver, Gold folders)
├── scripts/
│   ├── extract.py      # Stage 1: API Ingestion
│   ├── transform.py    # Stage 2: Data Cleaning & Parquet conversion
│   └── analytics.py    # Stage 3: SQL Aggregations & KPIs
├── app.py              # Streamlit Dashboard application
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation

```

## 📊 Business Insights

The final dashboard answers critical questions:

* **Volatility:** Which cities experience the highest daily temperature swings?
* **Resource Planning:** Tracking total rainfall patterns for agricultural or logistics planning.
* **Trend Analysis:** Comparing average temperature shifts across different global regions.

---
## 📊 Key Insights Delivered

* Daily temperature volatility (Max vs Min spread).
* Comparative rainfall analysis across different global time zones.
* Automated KPI calculation for average monthly climate shifts.

---

## 🚀 How to Run

1. **Clone the repo:** `git clone https://github.com/AbdullahMahmoud23/Global-Weather-Analytics-Pipeline.git`
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Run Ingestion:** `python scripts/extract.py`
4. **Run Transformation:** `python scripts/transform.py`
5. **Run Analytics:** `python scripts/analytics.py`
6. **Launch Dashboard:** `streamlit run app.py`

