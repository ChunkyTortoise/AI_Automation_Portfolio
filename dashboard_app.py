
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Competitor Intel", layout="wide", page_icon="📊")

# Custom CSS for "Fintech" Look
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .metric-box {
        background-color: #1E293B;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #334155;
    }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.title("⚙️ Simulation Settings")
n_records = st.sidebar.slider("Data Volume", 500, 5000, 2843)
market_event = st.sidebar.checkbox("Simulate 'Viral Incident'", value=True)

@st.cache_data
def generate_data(n, incident):
    data = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    incident_date = end_date - timedelta(days=42)
    features = ["App Stability", "Customer Service", "Pricing Tier", "API Latency", "Shipping", "UX Flow", "Onboarding"]

    for i in range(n):
        date = start_date + timedelta(days=random.randint(0, 180), hours=random.randint(0, 23))
        days_from_incident = (date - incident_date).days
        
        if incident and abs(days_from_incident) < 4:
            if random.random() < 0.85: sentiment="Negative"; score=random.uniform(-0.98, -0.65)
            else: sentiment="Neutral"; score=random.uniform(-0.2, 0.2)
        else:
            roll = random.random()
            if roll < 0.18: sentiment="Negative"; score=random.uniform(-0.8, -0.2)
            elif roll < 0.40: sentiment="Neutral"; score=random.uniform(-0.15, 0.15)
            else: sentiment="Positive"; score=random.uniform(0.25, 0.98)
        data.append({"Date": date, "Sentiment": sentiment, "Score": score, "Category": random.choice(features)})
    
    df = pd.DataFrame(data).sort_values('Date')
    df['Rolling'] = df['Score'].rolling(50, center=True).mean().fillna(0)
    return df

df = generate_data(n_records, market_event)

st.title("Market Sentiment // VOYAGER")
st.markdown("**AI-Driven Competitor Intelligence & Risk Monitoring**")

col1, col2, col3 = st.columns(3)
recent_avg = df['Rolling'].tail(50).mean() * 100
col1.metric("Net Sentiment Index", f"{recent_avg:.2f}", "-3.42%")
col2.metric("Total Data Points", f"{len(df):,}")
col3.metric("Critical Flags", f"{len(df[df['Sentiment']=='Negative'])}")

st.subheader("Sentiment Velocity (6-Month Lookback)")
fig, ax = plt.subplots(figsize=(10, 4))
fig.patch.set_facecolor('#0E1117')
ax.set_facecolor('#0E1117')
ax.plot(df['Date'], df['Rolling'], color='#00F0FF', linewidth=2)
ax.fill_between(df['Date'], df['Rolling'], -1, color='#00F0FF', alpha=0.1)
ax.axhline(0, color='grey', linestyle='--', alpha=0.3)
ax.axis('off')
st.pyplot(fig)

st.subheader("🚨 Strategic Recommendations")
st.error("1. IMMEDIATE PRIORITY: APP STABILITY. Correlation with recent update is high.")
st.warning("2. RECOMMENDED ACTION: Rollback recent push or deploy hotfix.")
