import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

# --- PAGE CONFIG ---
st.set_page_config(page_title="Voyager Intelligence", layout="wide", page_icon="⚡")

# Custom CSS for "SaaS" look
st.markdown("""
<style>
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        color: #00F0FF;
    }
    div[data-testid="stToolbar"] {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data
def generate_data():
    # ... (Same generation logic as before, just ensuring we have it) ...
    # For brevity in this upgrade, assuming data generation stays similar
    # but we ensure 'Category' and 'Date' are robust.
    N = 3000
    data = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    features = ["App Stability", "Customer Service", "Pricing", "UX Flow", "Shipping"]
    
    for i in range(N):
        date = start_date + timedelta(days=random.randint(0, 180))
        # Crisis simulation
        if abs((date - (end_date - timedelta(days=42))).days) < 3:
            sent = "Negative"
            score = random.uniform(-0.9, -0.6)
        else:
            roll = random.random()
            if roll < 0.2: sent, score = "Negative", random.uniform(-0.9, -0.2)
            elif roll < 0.5: sent, score = "Neutral", random.uniform(-0.1, 0.1)
            else: sent, score = "Positive", random.uniform(0.2, 0.9)
        
        data.append({"Date": date, "Sentiment": sent, "Score": score, "Category": random.choice(features)})
    
    df = pd.DataFrame(data).sort_values('Date')
    df['Rolling'] = df['Score'].rolling(50).mean().fillna(0)
    return df

df_master = generate_data()

# --- SIDEBAR FILTERS (The "Tool" Feel) ---
st.sidebar.header("🎛️ Control Panel")
time_range = st.sidebar.selectbox("Time Horizon", ["Last 6 Months", "Last 30 Days", "Last 7 Days"])
selected_cat = st.sidebar.multiselect("Filter by Category", df_master['Category'].unique(), default=df_master['Category'].unique())

# Filter Logic
df_filtered = df_master[df_master['Category'].isin(selected_cat)]
if time_range == "Last 30 Days": df_filtered = df_filtered.tail(500)
elif time_range == "Last 7 Days": df_filtered = df_filtered.tail(100)

# --- MAIN DASHBOARD ---
st.title("MARKET SENTIMENT // VOYAGER")
st.markdown(f"**Real-time Competitor Intelligence | N={len(df_filtered):,} Data Points**")

# KPI ROW
col1, col2, col3, col4 = st.columns(4)
current_score = df_filtered['Rolling'].iloc[-1] * 100
delta = current_score - (df_filtered['Rolling'].iloc[-50] * 100)

col1.metric("Net Sentiment", f"{current_score:.1f}", f"{delta:.2f}%")
col2.metric("Negative Signals", len(df_filtered[df_filtered['Sentiment']=='Negative']), delta_color="inverse")
col3.metric("Critical Alerts", random.randint(3, 12), "High Urgency", delta_color="inverse")
col4.metric("Market Health", "VOLATILE" if current_score < 20 else "STABLE", delta_color="off")

# --- INTERACTIVE CHART (PLOTLY) ---
st.subheader("🌊 Sentiment Velocity")
fig = go.Figure()

# The "Glow" Line
fig.add_trace(go.Scatter(
    x=df_filtered['Date'], y=df_filtered['Rolling'],
    mode='lines',
    name='Sentiment Trend',
    line=dict(color='#00F0FF', width=3),
    fill='tozeroy',
    fillcolor='rgba(0, 240, 255, 0.1)'
))

fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=False, color='#94A3B8'),
    yaxis=dict(showgrid=True, gridcolor='#334155', color='#94A3B8'),
    margin=dict(l=0, r=0, t=0, b=0),
    height=350
)
st.plotly_chart(fig, use_container_width=True)

# --- SPLIT VIEW: CATEGORIES & RECOMMENDATIONS ---
c1, c2 = st.columns([1, 1])

with c1:
    st.subheader("🔥 Churn Drivers by Category")
    neg_counts = df_filtered[df_filtered['Sentiment']=='Negative']['Category'].value_counts()
    fig_bar = px.bar(
        x=neg_counts.values, y=neg_counts.index, orientation='h',
        color=neg_counts.values, color_continuous_scale='reds'
    )
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis_visible=False, yaxis=dict(color='white'),
        coloraxis_showscale=False, margin=dict(l=0, r=0, t=0, b=0), height=300
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    st.subheader("🤖 Strategic Recommendations")
    st.info("💡 **Opportunity:** 'Pricing' complaints are down 15%. Increase ad spend on value propositions.")
    st.error("⚠️ **Critical:** 'App Stability' spikes correlate with v4.2 update. Rollback recommended.")
    
    # THE "BUSINESS VALUE" BUTTON
    csv = df_filtered.to_csv().encode('utf-8')
    st.download_button(
        label="📥 Download Executive Report (CSV)",
        data=csv,
        file_name='voyager_intelligence_export.csv',
        mime='text/csv',
    )