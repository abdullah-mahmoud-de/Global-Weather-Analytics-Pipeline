import duckdb
import os

def create_gold_layer():
    # 1. Connect to DuckDB
    con = duckdb.connect(database='data/weather_warehouse.db')

    # 2. Query the Silver Parquet file directly using SQL
    # We calculate daily stats from the hourly records
    gold_query = """
    CREATE OR REPLACE TABLE daily_weather_summary AS
    SELECT 
        city,
        CAST(time AS DATE) as date,
        MAX(temperature_2m) as max_temp,
        MIN(temperature_2m) as min_temp,
        AVG(temperature_2m) as avg_temp,
        SUM(rain) as total_daily_rain,
        (MAX(temperature_2m) - MIN(temperature_2m)) as temp_range
    FROM 'data/silver/cleaned_weather.parquet'
    GROUP BY city, date
    ORDER BY city, date;
    """
    
    print("🚀 Running Gold Layer transformations...")
    con.execute(gold_query)
    
    # 3. Export to a final CSV for the Dashboard
    os.makedirs('data/gold', exist_ok=True)
    con.execute("COPY daily_weather_summary TO 'data/gold/daily_weather_summary.csv' (HEADER, DELIMITER ',')")
    
    print("✅ Gold Layer created! Summary table saved to data/gold/daily_weather_summary.csv")
    
    # Show a preview in the console
    print("\n--- Preview of Gold Data ---")
    print(con.execute("SELECT * FROM daily_weather_summary LIMIT 5").df())

if __name__ == "__main__":
    create_gold_layer()