
"""
Code to talk to the API

fetch weather data for 3 different cities [London, New_York, Tokyo]

"""

import requests
import json
import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
CONFIG_FILE = 'config/world_capitals.csv'
BRONZE_DIR = 'data/bronze'
MAX_WORKERS = 5 # Number of concurrent API requests

def fetch_and_save(city, lat, lon):
    """Fetches weather data for a single city and saves it to the Bronze layer."""
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": "2024-01-01",
        "end_date": "2024-01-10",
        "hourly": ["temperature_2m", "relative_humidity_2m", "rain"],
        "timezone": "auto"
    }
    
    try:
        # Added a timeout so the script doesn't hang forever if the API is slow
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            os.makedirs(BRONZE_DIR, exist_ok=True)
            path = os.path.join(BRONZE_DIR, f'{city}_raw.json')
            
            with open(path, 'w') as f:
                json.dump(response.json(), f)
            return f"✅ Success: {city}"
        else:
            return f"❌ Failed API [{response.status_code}]: {city}"
            
    except requests.exceptions.RequestException as e:
        return f"⚠️ Network Error for {city}: {e}"

def main():
    print(f"Loading cities from {CONFIG_FILE}...")
    try:
        df_cities = pd.read_csv(CONFIG_FILE)
    except FileNotFoundError:
        print(f"Error: Could not find {CONFIG_FILE}. Please create it.")
        return

    print(f"Starting extraction for {len(df_cities)} cities using {MAX_WORKERS} workers...\n")
    
    # This is the Multithreading magic
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all tasks to the executor
        future_to_city = {
            executor.submit(fetch_and_save, row['city'], row['lat'], row['lon']): row['city']
            for _, row in df_cities.iterrows()
        }
        
        # Process results as they complete
        for future in as_completed(future_to_city):
            result = future.result()
            print(result)

    print("\n✅ Extraction Phase Complete!")

if __name__ == "__main__":
    main()
