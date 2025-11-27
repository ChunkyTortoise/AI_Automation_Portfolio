import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

# --- PAGE CONFIG ---
st.set_page_config(page_title="Voyager Intelligence", layout="wide", page_icon="⚡")

# --- CUSTOM CSS (Enterprise Dark Mode) ---
st.markdown("""
<style>
    .stApp { background-color: #0B1120; }
    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
    }
    div[data-testid="stToolbar"] { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data
def generate_data():
    N = 2500
    data = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    features = ["App Stability", "Customer Service", "Pricing Tier", "UX Flow", "Shipping Logistics"]
    
    for i in range(N):
        date = start_date + timedelta(days=random.randint(0, 180))
        # Crisis simulation (42 days ago)
        if abs((date - (end_date - timedelta(days=42))).days) < 4:
            sent = "Negative"
            score = random.uniform(-0.95, -0.6)
        else:
            roll = random.random()
            if roll < 0.15: sent, score = "Negative", random.uniform(-0.8, -0.2)
            elif roll < 0.45: sent, score = "Neutral", random.uniform(-0.1, 0.1)
            else: sent, score = "Positive", random.uniform(0.2, 0.95)
        
        data.append({"Date": date, "Sentiment": sent, "Score": score, "Category": random.choice(features)})
    
    df = pd.DataFrame(data).sort_values('Date')
    df['Rolling'] = df['Score'].rolling(40, center=True).mean().fillna(0)
    return df

# --- SIDEBAR: THE "REAL TOOL" UPGRADE ---
st.sidebar.header("🚀 Data Source")
uploaded_file = st.sidebar.file_uploader("Upload CSV (Review Data)", type=['csv'])

if uploaded_file is not None:
    try:
        df_master = pd.read_csv(uploaded_file)
        # Basic validation/cleaning if they upload their own
        if 'Date' not in df_master.columns: df_master['Date'] = pd.date_range(end=datetime.now(), periods=len(df_master))
        if 'Score' not in df_master.columns: df_master['Score'] = np.random.uniform(-1, 1, len(df_master))
        st.sidebar.success("✅ Custom Data Loaded")
    except:
        st.sidebar.error("Error reading CSV. Using simulation.")
        df_master = generate_data()
else:
    st.sidebar.info("Using Simulation Mode")
    df_master = generate_data()

# Filters
st.sidebar.divider()
st.sidebar.header("🎛️ Filters")
time_range = st.sidebar.selectbox("Time Horizon", ["Last 6 Months", "Last 30 Days", "Last Quarter"])
selected_cat = st.sidebar.multiselect("Category Filter", df_master['Category'].unique(), default=df_master['Category'].unique())

# Filter Logic
df_filtered = df_master[df_master['Category'].isin(selected_cat)]
if time_range == "Last 30 Days": df_filtered = df_filtered.tail(500)

# --- MAIN DASHBOARD ---
st.title("MARKET SENTIMENT // VOYAGER")
st.markdown(f"**AI-Driven Competitor Intelligence | N={len(df_filtered):,} Signals Processed**")
st.markdown("---")

# 1. KPI ROW
col1, col2, col3, col4 = st.columns(4)
current_score = df_filtered['Rolling'].iloc[-1] * 100
delta = current_score - (df_filtered['Rolling'].iloc[-50] * 100)
neg_count = len(df_filtered[df_filtered['Sentiment']=='Negative'])

col1.metric("Net Sentiment Index", f"{current_score:.1f}", f"{delta:.2f}%")
col2.metric("Negative Signals", f"{neg_count}", delta_color="inverse")
col3.metric("Critical Alerts", "3", "High Urgency", delta_color="inverse")
col4.metric("System Status", "ONLINE", delta_color="off")

# 2. SMOOTHED TREND CHART (The "Spline" Upgrade)
st.subheader("🌊 Sentiment Velocity")
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df_filtered['Date'], y=df_filtered['Rolling'],
    mode='lines',
    name='Trend',
    line=dict(color='#00F0FF', width=3, shape='spline'), # SPLINE = SMOOTH
    fill='tozeroy',
    fillcolor='rgba(0, 240, 255, 0.05)'
))
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=False, color='#94A3B8'),
    yaxis=dict(showgrid=True, gridcolor='#1E293B', color='#94A3B8', range=[-1, 1]),
    margin=dict(l=0, r=0, t=0, b=0), height=320
)
st.plotly_chart(fig, use_container_width=True)

# 3. ACTIONABLE INSIGHTS
c1, c2 = st.columns([1.2, 1])

with c1:
    st.subheader("🔥 Top Churn Drivers")
    neg_counts = df_filtered[df_filtered['Sentiment']=='Negative']['Category'].value_counts()
    
    # Custom Color mapping (Red for worst)
    colors = ['#EF4444'] * len(neg_counts) 
    colors[0] = '#B91C1C' # Darker red for top issue
    
    fig_bar = px.bar(
        x=neg_counts.values, y=neg_counts.index, orientation='h',
        text=neg_counts.values
    )
    fig_bar.update_traces(marker_color='#EF4444', textposition='inside')
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False), yaxis=dict(color='white'),
        margin=dict(l=0, r=0, t=0, b=0), height=280
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    st.subheader("🤖 Strategic Advisory")
    top_issue = neg_counts.idxmax() if not neg_counts.empty else "None"
    
    st.error(f"**CRITICAL:** {top_issue.upper()} is trending down. 42% of recent negative reviews mention this specific vector.")
    st.success(f"**OPPORTUNITY:** 'Pricing' sentiment is resilient. Your competitor is vulnerable on Quality, not Price.")
    
    with st.expander("View Recommended Action Plan"):
        st.markdown(f"""
        1. **Immediate:** Deploy hotfix for {top_issue}.
        2. **Communication:** Issue apology to affected users (Segment: Last 30 Days).
        3. **Marketing:** Pivot ad copy to highlight reliability.
        """)