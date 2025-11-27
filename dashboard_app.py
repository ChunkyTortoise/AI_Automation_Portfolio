import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

# --- 1. CONFIGURATION & CSS ---
st.set_page_config(page_title="Voyager Intelligence", layout="wide", page_icon="⚡")

# Injecting "Glassmorphism" CSS
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #080A10;
    }
    
    /* Metrics Styling */
    div[data-testid="stMetric"] {
        background-color: #11151C;
        border: 1px solid #1F2937;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    [data-testid="stMetricLabel"] {
        color: #9CA3AF;
        font-size: 0.9rem;
    }
    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        color: #F3F4F6;
        font-weight: 700;
    }
    
    /* Chart Containers */
    .plot-container {
        border: 1px solid #1F2937;
        border-radius: 12px;
        padding: 10px;
        background-color: #11151C;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. DATA ENGINE (Fixed Math) ---
@st.cache_data
def generate_data():
    N = 3500
    data = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    features = ["App Stability", "Customer Service", "Pricing Tier", "UX Flow", "Shipping Logistics", "Onboarding"]
    
    # Weighted Randomness for realism
    for i in range(N):
        date = start_date + timedelta(days=random.randint(0, 180))
        # Simulated Crisis (42 days ago)
        if abs((date - (end_date - timedelta(days=42))).days) < 5:
            sent = "Negative"
            score = random.uniform(-0.95, -0.6)
        else:
            roll = random.random()
            if roll < 0.18: sent, score = "Negative", random.uniform(-0.85, -0.2)
            elif roll < 0.45: sent, score = "Neutral", random.uniform(-0.1, 0.1)
            else: sent, score = "Positive", random.uniform(0.25, 0.95)
        
        data.append({"Date": date, "Sentiment": sent, "Score": score, "Category": random.choice(features)})
    
    df = pd.DataFrame(data).sort_values('Date')
    # Use a wider window for smoother lines
    df['Rolling'] = df['Score'].rolling(100, center=True).mean().fillna(method='bfill')
    return df

df_master = generate_data()

# --- 3. SIDEBAR ---
with st.sidebar:
    st.header("🎛️ Control Panel")
    st.info("Simulating Live Connection...")
    time_range = st.selectbox("Time Horizon", ["Last 6 Months", "Last 30 Days"])
    selected_cat = st.multiselect("Category Filter", df_master['Category'].unique(), default=df_master['Category'].unique())
    st.divider()
    st.caption(f"System Version: v2.4.1\nLast Sync: {datetime.now().strftime('%H:%M:%S')}")

# Filter Logic
df_filtered = df_master[df_master['Category'].isin(selected_cat)]
if time_range == "Last 30 Days": df_filtered = df_filtered.tail(600)

# --- 4. MAIN DASHBOARD ---

# Header
c1, c2 = st.columns([3, 1])
with c1:
    st.title("MARKET SENTIMENT // VOYAGER")
    st.markdown(f"**AI-Driven Competitor Intelligence | N={len(df_filtered):,} Signals**")
with c2:
    st.markdown("##") # Spacing
    st.download_button("📥 Export CSV", df_filtered.to_csv(), "report.csv", "text/csv", use_container_width=True)

st.markdown("---")

# KPI Grid (4 Columns)
k1, k2, k3, k4 = st.columns(4)

# Calculate KPIs (Preventing 0.0 bug by taking mean of last 50, not just last 1)
current_score = df_filtered['Rolling'].iloc[-50:].mean() * 100
prev_score = df_filtered['Rolling'].iloc[-200:-150].mean() * 100
delta = current_score - prev_score
neg_count = len(df_filtered[df_filtered['Sentiment']=='Negative'])

k1.metric("Net Sentiment Index", f"{current_score:.1f}", f"{delta:.1f}%")
k2.metric("Negative Signals", f"{neg_count}", delta_color="inverse")
k3.metric("Critical Alerts", "5", "High Urgency", delta_color="inverse")
k4.metric("Market Health", "VOLATILE" if current_score < 15 else "STABLE", delta_color="off")

# --- CHART ROW ---
st.subheader("🌊 Sentiment Velocity")

fig_trend = go.Figure()
fig_trend.add_trace(go.Scatter(
    x=df_filtered['Date'], y=df_filtered['Rolling'],
    mode='lines',
    name='Trend',
    line=dict(color='#3B82F6', width=3), # Modern Blue
    fill='tozeroy',
    fillcolor='rgba(59, 130, 246, 0.1)' # Gradient Fill
))

fig_trend.update_layout(
    paper_bgcolor='#11151C', # Matches Card CSS
    plot_bgcolor='#11151C',
    xaxis=dict(showgrid=False, color='#6B7280'),
    yaxis=dict(showgrid=True, gridcolor='#1F2937', color='#6B7280', range=[-1, 1]),
    margin=dict(l=20, r=20, t=20, b=20),
    height=350,
    hovermode="x unified"
)
st.plotly_chart(fig_trend, use_container_width=True)

# --- INSIGHTS ROW ---
c_left, c_right = st.columns([1.5, 1])

with c_left:
    st.subheader("🔥 Top Churn Drivers")
    neg_counts = df_filtered[df_filtered['Sentiment']=='Negative']['Category'].value_counts().sort_values(ascending=True)
    
    # Gradient Color Scale (Light Red -> Dark Red)
    fig_bar = px.bar(
        x=neg_counts.values, y=neg_counts.index, orientation='h',
        text=neg_counts.values,
        color=neg_counts.values,
        color_continuous_scale=['#FCA5A5', '#EF4444', '#7F1D1D'] # Gradient
    )
    
    fig_bar.update_layout(
        paper_bgcolor='#11151C', plot_bgcolor='#11151C',
        xaxis=dict(visible=False), 
        yaxis=dict(color='#F3F4F6', tickfont=dict(size=14)),
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=0, b=0), height=320
    )
    fig_bar.update_traces(textposition='inside')
    st.plotly_chart(fig_bar, use_container_width=True)

with c_right:
    st.subheader("🤖 Strategic Advisory")
    
    # Custom HTML Card for Recommendations
    top_issue = neg_counts.index[-1] if not neg_counts.empty else "None"
    
    st.markdown(f"""
    <div style="background-color: #1F2937; padding: 20px; border-radius: 10px; border-left: 5px solid #EF4444;">
        <h4 style="color: #EF4444; margin:0;">⚠️ CRITICAL PRIORITY: {top_issue.upper()}</h4>
        <p style="color: #D1D5DB; font-size: 14px; margin-top: 10px;">
            Correlation with recent v4.2 update is <strong>High (0.88)</strong>. 
            42% of negative reviews in the last 7 days mention this specific vector.
        </p>
    </div>
    <div style="margin-top: 15px;"></div>
    <div style="background-color: #1F2937; padding: 20px; border-radius: 10px; border-left: 5px solid #10B981;">
        <h4 style="color: #10B981; margin:0;">💡 OPPORTUNITY: PRICING</h4>
        <p style="color: #D1D5DB; font-size: 14px; margin-top: 10px;">
            Sentiment for 'Pricing' is <strong>+12%</strong> vs Competitor B. 
            Recommendation: Increase ad spend on value-based messaging.
        </p>
    </div>
    """, unsafe_allow_html=True)