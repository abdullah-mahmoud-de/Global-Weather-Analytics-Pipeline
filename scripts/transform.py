
"""
Code to clean the data
"""

import pandas as pd
import json
import os
import glob

def transform_data():
    # Path to your raw data
    input_files = glob.glob('data/bronze/*.json')
    all_dfs = []

    for file_path in input_files:
        with open(file_path, 'r') as f:
            raw_json = json.load(f)
        
        # Get city name from the filename
        city_name = os.path.basename(file_path).split('_raw')[0]
        
        # Extract the hourly data block
        hourly_data = raw_json['hourly']
        
        # Create a DataFrame from the hourly dictionary
        df = pd.DataFrame(hourly_data)
        
        # 1. ADD METADATA: Which city is this?
        df['city'] = city_name
        
        # 2. DATA TYPING: Ensure time is an actual timestamp object
        df['time'] = pd.to_datetime(df['time'])
        
        # 3. DATA CLEANING: Handle missing values (if any)
        # Drop rows where temperature is null
        df = df.dropna(subset=['temperature_2m'])
        
        all_dfs.append(df)

    # Combine all cities into one big table
    final_df = pd.concat(all_dfs, ignore_index=True)

    # Create Silver directory
    os.makedirs('data/silver', exist_ok=True)
    
    # Save as Parquet (The DE standard)
    output_path = 'data/silver/cleaned_weather.parquet'
    final_df.to_parquet(output_path, index=False)
    
    print(f"✅ Transformation complete! {len(final_df)} rows saved to {output_path}")

if __name__ == "__main__":
    transform_data()