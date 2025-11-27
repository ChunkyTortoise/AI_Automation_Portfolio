import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Voyager Intelligence", 
    layout="wide", 
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

# --- ENTERPRISE-GRADE CUSTOM CSS WITH GLASSMORPHISM ---
st.markdown("""
<style>
    /* Import Modern Font Stack */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&display=swap');
    
    /* Global Background & Typography */
    .stApp {
        background: linear-gradient(135deg, #0B1120 0%, #1a1f3a 50%, #0d1625 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Glassmorphic Card Effect for Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2.8rem !important;
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        background: linear-gradient(135deg, #00F0FF 0%, #7000FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        filter: drop-shadow(0 0 20px rgba(0, 240, 255, 0.4));
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 1rem !important;
        font-weight: 600;
    }
    
    /* Glassmorphic Container for Metrics */
    [data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37),
                    inset 0 1px 0 0 rgba(255, 255, 255, 0.05);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 48px 0 rgba(0, 240, 255, 0.25);
        border-color: rgba(0, 240, 255, 0.3);
    }
    
    /* Sidebar Styling - Native App Look */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(11, 17, 32, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
        backdrop-filter: blur(40px);
        border-right: 1px solid rgba(112, 0, 255, 0.2);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
    }
    
    /* Sidebar Headers with Glow */
    .sidebar .element-container h2,
    [data-testid="stSidebar"] h2 {
        color: #00F0FF;
        font-weight: 700;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 0 20px rgba(0, 240, 255, 0.6);
        margin-bottom: 1.5rem;
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #7000FF 0%, #00F0FF 100%);
        border: none;
        border-radius: 12px;
        font-weight: 600;
        padding: 0.75rem 2rem;
        box-shadow: 0 4px 20px rgba(112, 0, 255, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(112, 0, 255, 0.6);
    }
    
    /* Glassmorphic Chart Containers */
    [data-testid="stPlotlyChart"] {
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    /* Enhanced Subheaders */
    .stApp h2, .stApp h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: #E2E8F0;
        letter-spacing: -0.5px;
    }
    
    /* Title with Gradient Glow */
    .stApp h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        font-size: 3.5rem !important;
        background: linear-gradient(135deg, #00F0FF 0%, #FFFFFF 50%, #7000FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 60px rgba(0, 240, 255, 0.5);
        letter-spacing: -2px;
        margin-bottom: 0.5rem !important;
    }
    
    /* Alert Boxes with Glassmorphism */
    .stAlert {
        background: rgba(15, 23, 42, 0.6) !important;
        backdrop-filter: blur(20px);
        border-radius: 12px;
        border-left: 4px solid #00F0FF;
    }
    
    /* Enhanced Dataframe */
    [data-testid="stDataFrame"] {
        background: rgba(15, 23, 42, 0.5);
        backdrop-filter: blur(16px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 16px;
    }
    
    /* Remove Streamlit Branding */
    div[data-testid="stToolbar"],
    footer,
    #MainMenu {
        visibility: hidden;
        height: 0;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: rgba(112, 0, 255, 0.15);
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #7000FF, #00F0FF);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #00F0FF, #7000FF);
    }
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
        
        data.append({
            "Date": date, 
            "Sentiment": sent, 
            "Score": score, 
            "Category": random.choice(features),
            "Volume": random.randint(50, 500)
        })
    
    df = pd.DataFrame(data).sort_values('Date')
    df['Rolling'] = df['Score'].rolling(40, center=True).mean().fillna(0)
    df['Volatility'] = df['Score'].rolling(20).std().fillna(0)
    return df

# --- ENHANCED SIDEBAR ---
with st.sidebar:
    st.markdown("### 🚀 DATA SOURCE")
    uploaded_file = st.file_uploader(
        "Upload CSV (Review Data)", 
        type=['csv'],
        help="Upload your own sentiment data"
    )
    
    if uploaded_file is not None:
        try:
            df_master = pd.read_csv(uploaded_file)
            if 'Date' not in df_master.columns: 
                df_master['Date'] = pd.date_range(end=datetime.now(), periods=len(df_master))
            if 'Score' not in df_master.columns: 
                df_master['Score'] = np.random.uniform(-1, 1, len(df_master))
            st.success("✅ Custom Data Loaded")
        except:
            st.error("⚠️ Error reading CSV. Using simulation.")
            df_master = generate_data()
    else:
        st.info("📊 Simulation Mode Active")
        df_master = generate_data()
    
    st.divider()
    st.markdown("### 🎛️ FILTERS")
    
    time_range = st.selectbox(
        "Time Horizon",
        ["Last 6 Months", "Last 30 Days", "Last Quarter"],
        help="Select time window for analysis"
    )
    
    selected_cat = st.multiselect(
        "Category Filter",
        df_master['Category'].unique(),
        default=df_master['Category'].unique(),
        help="Filter by feedback category"
    )
    
    st.divider()
    st.markdown("### ⚙️ DISPLAY OPTIONS")
    show_raw = st.checkbox("Show Raw Data", value=False)
    chart_style = st.radio("Chart Theme", ["Neon", "Classic"], index=0)

# Filter Logic
df_filtered = df_master[df_master['Category'].isin(selected_cat)]
if time_range == "Last 30 Days": 
    df_filtered = df_filtered.tail(500)

# --- MAIN DASHBOARD ---
st.title("VOYAGER // INTELLIGENCE")
st.markdown(f"**AI-Driven Competitor Intelligence** • **{len(df_filtered):,}** Signals Processed • Last Updated: {datetime.now().strftime('%I:%M %p')}")
st.markdown("")

# 1. ENHANCED KPI ROW
col1, col2, col3, col4 = st.columns(4)

current_score = df_filtered['Rolling'].iloc[-1] * 100
delta = current_score - (df_filtered['Rolling'].iloc[-50] * 100)
neg_count = len(df_filtered[df_filtered['Sentiment']=='Negative'])
volatility = df_filtered['Volatility'].iloc[-1] * 100

with col1:
    st.metric(
        "Net Sentiment Index", 
        f"{current_score:.1f}", 
        f"{delta:.2f}%",
        delta_color="normal"
    )

with col2:
    st.metric(
        "Negative Signals", 
        f"{neg_count:,}", 
        f"{-neg_count/len(df_filtered)*100:.1f}%",
        delta_color="inverse"
    )

with col3:
    st.metric(
        "Volatility Score", 
        f"{volatility:.1f}%", 
        "High Risk" if volatility > 30 else "Stable",
        delta_color="off"
    )

with col4:
    st.metric(
        "System Status", 
        "ONLINE", 
        "All Systems Operational",
        delta_color="off"
    )

st.markdown("")

# 2. LUXURY TREND CHART WITH GLOW EFFECT
st.subheader("🌊 Sentiment Velocity Stream")

# Color scheme based on selection
colors_neon = {
    'primary': '#00F0FF',
    'secondary': '#7000FF',
    'critical': '#FF0055'
}
colors_classic = {
    'primary': '#3B82F6',
    'secondary': '#8B5CF6',
    'critical': '#EF4444'
}

color_scheme = colors_neon if chart_style == "Neon" else colors_classic

fig = go.Figure()

# Add glowing background trace for neon effect
if chart_style == "Neon":
    fig.add_trace(go.Scatter(
        x=df_filtered['Date'], 
        y=df_filtered['Rolling'],
        mode='lines',
        name='Glow Layer',
        line=dict(
            color=color_scheme['primary'], 
            width=12, 
            shape='spline'
        ),
        opacity=0.15,
        showlegend=False,
        hoverinfo='skip'
    ))

# Main trend line with enhanced styling
fig.add_trace(go.Scatter(
    x=df_filtered['Date'], 
    y=df_filtered['Rolling'],
    mode='lines',
    name='Sentiment Trend',
    line=dict(
        color=color_scheme['primary'], 
        width=3, 
        shape='spline'
    ),
    fill='tozeroy',
    fillcolor=f'rgba(0, 240, 255, 0.08)' if chart_style == "Neon" else 'rgba(59, 130, 246, 0.08)',
    hovertemplate='<b>%{x|%b %d}</b><br>Score: %{y:.2f}<extra></extra>'
))

# Critical threshold line
fig.add_hline(
    y=-0.3, 
    line_dash="dash", 
    line_color=color_scheme['critical'], 
    line_width=2,
    annotation_text="Critical Threshold",
    annotation_position="right"
)

fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(
        showgrid=False,
        color='#94A3B8',
        showline=False,
        zeroline=False
    ),
    yaxis=dict(
        showgrid=False,
        gridcolor='rgba(148, 163, 184, 0.1)',
        color='#94A3B8',
        range=[-1, 1],
        showline=False,
        zeroline=True,
        zerolinecolor='rgba(148, 163, 184, 0.3)'
    ),
    margin=dict(l=20, r=20, t=20, b=20),
    height=380,
    hovermode='x unified',
    font=dict(family="Inter, sans-serif", size=12)
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("")

# 3. ACTIONABLE INSIGHTS SECTION
c1, c2 = st.columns([1.3, 1])

with c1:
    st.subheader("🔥 Critical Churn Vectors")
    neg_counts = df_filtered[df_filtered['Sentiment']=='Negative']['Category'].value_counts().head(5)
    
    fig_bar = go.Figure()
    
    # Add glow effect for bars
    if chart_style == "Neon":
        fig_bar.add_trace(go.Bar(
            x=neg_counts.values,
            y=neg_counts.index,
            orientation='h',
            marker=dict(
                color=color_scheme['critical'],
                opacity=0.3,
                line=dict(width=0)
            ),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Main bars
    fig_bar.add_trace(go.Bar(
        x=neg_counts.values,
        y=neg_counts.index,
        orientation='h',
        text=neg_counts.values,
        textposition='inside',
        textfont=dict(size=14, color='white', family='Inter', weight='bold'),
        marker=dict(
            color=color_scheme['critical'],
            line=dict(width=0)
        ),
        showlegend=False,
        hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>'
    ))
    
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False, showgrid=False),
        yaxis=dict(
            color='#E2E8F0',
            showgrid=False,
            showline=False
        ),
        margin=dict(l=0, r=20, t=10, b=10),
        height=300,
        font=dict(family="Inter, sans-serif", size=13)
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    st.subheader("🤖 Strategic Advisory")
    top_issue = neg_counts.idxmax() if not neg_counts.empty else "None"
    
    st.error(f"""
    **⚠️ CRITICAL ALERT**  
    *{top_issue.upper()}* is experiencing severe degradation. 
    **{int(neg_counts.iloc[0]/neg_count*100)}%** of negative signals trace to this vector.
    """)
    
    st.success(f"""
    **✨ OPPORTUNITY DETECTED**  
    Competitor vulnerability identified in Quality metrics. 
    Your pricing resilience provides strategic advantage.
    """)
    
    with st.expander("📋 View Action Plan"):
        st.markdown(f"""
        #### Immediate Response Protocol
        
        1. **Deploy Hotfix** — Address {top_issue} within 48h
        2. **Customer Outreach** — Segment: Last 30 days affected users
        3. **Marketing Pivot** — Shift messaging to reliability
        4. **Monitor Competitor** — Track their response velocity
        
        **Estimated Impact:** +12% retention, -8% churn risk
        """)

# 4. CONDITIONAL FORMATTED DATA TABLE
if show_raw:
    st.markdown("")
    st.subheader("📊 Raw Intelligence Feed")
    
    # Create summary table with conditional formatting
    summary_df = df_filtered.groupby('Category').agg({
        'Score': ['mean', 'std', 'count'],
        'Sentiment': lambda x: (x == 'Negative').sum()
    }).round(3)
    
    summary_df.columns = ['Avg Score', 'Volatility', 'Total Signals', 'Negative Count']
    summary_df['Risk Level'] = summary_df['Avg Score'].apply(
        lambda x: '🔴 High' if x < -0.2 else ('🟡 Medium' if x < 0.2 else '🟢 Low')
    )
    summary_df = summary_df.reset_index()
    
    # Display with custom configuration
    st.dataframe(
        summary_df,
        column_config={
            "Category": st.column_config.TextColumn("Category", width="medium"),
            "Avg Score": st.column_config.ProgressColumn(
                "Avg Score",
                format="%.3f",
                min_value=-1,
                max_value=1,
            ),
            "Volatility": st.column_config.NumberColumn("Volatility", format="%.3f"),
            "Total Signals": st.column_config.NumberColumn("Total Signals", format="%d"),
            "Negative Count": st.column_config.NumberColumn("Negative Count", format="%d"),
            "Risk Level": st.column_config.TextColumn("Risk Level"),
        },
        hide_index=True,
        use_container_width=True
    )
