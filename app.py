import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(page_title="Global Weather Analytics", layout="wide")
st.title("🌍 Global Weather Insights Dashboard")

@st.cache_data
def load_data():
    # 1. Load Gold layer data
    df = pd.read_csv('data/gold/daily_weather_summary.csv')
    df['date'] = pd.to_datetime(df['date'])
    
    # 2. Load Coordinates from config
    locations = pd.read_csv('config/world_capitals.csv')
    
    # 3. Merge them together based on the 'city' column
    merged_df = pd.merge(df, locations, on='city', how='left')
    return merged_df

df = load_data()

# Get the latest date in the dataset to show current global snapshot
latest_date = df['date'].max()
latest_data = df[df['date'] == latest_date]

st.markdown(f"### 🗺️ Global Temperatures on {latest_date.strftime('%Y-%m-%d')}")

# --- GLOBAL MAP VISUALIZATION ---
fig_map = px.scatter_geo(
    latest_data,
    lat='lat',
    lon='lon',
    color='avg_temp',
    hover_name='city',
    size='total_daily_rain',
    projection='natural earth',
    color_continuous_scale=px.colors.sequential.Plasma
)


fig_map.update_layout(
    height=680,  # Forces the map to be much taller
    margin={"r":0,"t":0,"l":0,"b":0},  # Removes the massive white borders
    paper_bgcolor="rgba(0,0,0,0)",  # Makes the outer background transparent
    geo=dict(
        bgcolor="rgba(0,0,0,0)",    # Makes the map ocean transparent
        landcolor="#2d3035",        # Colors the land a nice dark gray
        showlakes=False
    )
)

st.plotly_chart(fig_map, use_container_width=True)

st.divider()

# --- TOP 10 CHARTS ---
st.markdown("### 📊 Extremes Analysis")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔥 Top Hottest Cities")
    hottest = latest_data.nlargest(10, 'max_temp')
    fig_hot = px.bar(hottest, x='city', y='max_temp', color='max_temp', color_continuous_scale='Reds')
    st.plotly_chart(fig_hot, use_container_width=True)

with col2:
    st.subheader("❄️ Top Coldest Cities")
    coldest = latest_data.nsmallest(10, 'min_temp')
    fig_cold = px.bar(coldest, x='city', y='min_temp', color='min_temp', color_continuous_scale='Blues')
    st.plotly_chart(fig_cold, use_container_width=True)