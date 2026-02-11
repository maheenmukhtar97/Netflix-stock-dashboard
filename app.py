import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Netflix Stock Dashboard", layout="wide")

# ================== CUSTOM UI ==================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

/* Global */
html, body, [class*="st-"], [class*="css"]  {
    background-color: #0F1C2E !important;
    color: #E6EDF6 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

.block-container {
    padding-top: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* Headings */
h1 {
    font-size: 36px !important;
    font-weight: 700 !important;
    color: #E50914 !important;
    letter-spacing: 1px;
}


p {
    color: #9FB3C8 !important;
}

/* Card Style */
.card {
    background: #16263D;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.06);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111C2D !important;
}

/* Multiselect */
div[data-baseweb="select"] > div {
    background-color: #16263D !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}

span[data-baseweb="tag"] {
    background-color: #3B82F6 !important;
    color: white !important;
    border-radius: 6px !important;
}

/* Buttons */
.stButton>button {
    background-color: #16263D;
    color: #E6EDF6;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px;
}

.stButton>button:hover {
    border: 1px solid #3B82F6;
    color: #3B82F6;
}

/* Metrics */
[data-testid="stMetric"] {
    background: #16263D;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.06);
}
</style>
""", unsafe_allow_html=True)

# ================== LOAD DATA ==================
df = pd.read_csv("data/NFLX.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# ================== HEADER ==================
st.title("🎬 Netflix Stock Analysis")
st.markdown("Analyze Netflix stock performance with a professional fintech dashboard UI.")

# ================== LAYOUT ==================
left, right = st.columns([1, 3])

# ================== LEFT PANEL ==================
with left:
    st.subheader("Time Horizon")

    time_option = st.selectbox(
        "",
        ["1 Month", "3 Months", "6 Months", "1 Year", "5 Years", "All"]
    )

    if time_option != "All":
        months_map = {
            "1 Month": 1,
            "3 Months": 3,
            "6 Months": 6,
            "1 Year": 12,
            "5 Years": 60,
        }
        months = months_map[time_option]
        cutoff = df["Date"].max() - pd.DateOffset(months=months)
        filtered_df = df[df["Date"] >= cutoff]
    else:
        filtered_df = df

    latest_close = filtered_df["Close"].iloc[-1]
    previous_close = filtered_df["Close"].iloc[-2]
    change = latest_close - previous_close
    percent_change = (change / previous_close) * 100

    st.subheader("Stock Summary")

    st.metric("Latest Close", f"${latest_close:.2f}")
    st.metric("Daily Change", f"${change:.2f}", f"{percent_change:.2f}%")
    st.metric("Highest Price", f"${filtered_df['High'].max():.2f}")
    st.metric("Lowest Price", f"${filtered_df['Low'].min():.2f}")

# ================== RIGHT PANEL ==================
with right:

    # Main Price Chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=filtered_df["Date"],
        y=filtered_df["Close"],
        mode="lines",
        name="Close Price",
        line=dict(width=3)
    ))

    fig.update_layout(
        paper_bgcolor="#16263D",
        plot_bgcolor="#16263D",
        font=dict(color="#E6EDF6"),
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)")
    )

    st.plotly_chart(fig, use_container_width=True)

    # Volume Chart
    st.subheader("Trading Volume")

    vol_fig = go.Figure()

    vol_fig.add_trace(go.Bar(
        x=filtered_df["Date"],
        y=filtered_df["Volume"],
        name="Volume"
    ))

    vol_fig.update_layout(
        paper_bgcolor="#16263D",
        plot_bgcolor="#16263D",
        font=dict(color="#E6EDF6"),
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)")
    )

    st.plotly_chart(vol_fig, use_container_width=True)