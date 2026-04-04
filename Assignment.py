import streamlit as st
import yfinance as yf
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Stock Finder | Analytics",
    page_icon="📈",
    layout="centered"
)

# Refined Light Terminal CSS
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #000000 !important; }
    
    /* White Input Tab with high contrast */
    .stTextInput>div>div>input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
        border-radius: 4px !important;
    }

    /* Metric Boxes with Bold Black Text */
    .metric-box {
        background: #fdfdfd;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #eeeeee;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .metric-label { color: #666666; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; }
    .metric-value { color: #000000; font-size: 22px; font-weight: 900; margin-top: 5px; }

    /* Clean Summary Styling */
    .summary-point {
        padding: 10px 0;
        border-bottom: 1px solid #f0f0f0;
        color: #333333;
        font-size: 15px;
        line-height: 1.6;
    }
    
    h1, h2, h3 { color: #000000 !important; font-weight: 800 !important; }
    label { color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📈 Stock Finder")
st.subheader("Business and Price Overview")
st.markdown("---")

company_input = st.text_input("Enter Company Name:", placeholder="e.g. ITC Ltd, Infosys, Reliance")

if company_input:
    with st.spinner("Fetching Market Intelligence..."):
        try:
            search = yf.Search(company_input, max_results=1)
            if not search.quotes:
                st.error("Entity not found.")
            else:
                ticker_sym = search.quotes[0]['symbol']
                stock = yf.Ticker(ticker_sym)
                info = stock.info
                
                # Header info
                st.markdown(f"### {info.get('longName', ticker_sym)} ({ticker_sym})")
                
                # 1. Sector and Industry (Bold Black)
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f'<div class="metric-box"><div class="metric-label">Sector</div><div class="metric-value">{info.get("sector", "N/A")}</div></div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<div class="metric-box"><div class="metric-label">Industry</div><div class="metric-value">{info.get("industry", "N/A")}</div></div>', unsafe_allow_html=True)

                # 2. Financial Performance Chart (Price Action)
                st.markdown("### 📊 1-Year Price Performance")
                hist = stock.history(period="1y")
                if not hist.empty:
                    st.line_chart(hist['Close'], color="#000000")
                else:
                    st.info("Historical data currently unavailable for this ticker.")

                # 3. Core Business Crux (Point-wise, no tabs)
                st.markdown("### 🎯 Core Business Crux")
                summary = info.get('longBusinessSummary', "")
                if summary:
                    # Logic to get top 5 quality sentences
                    points = [p.strip() for p in summary.replace(';', '.').split('.') if len(p.strip()) > 35]
                    for i, point in enumerate(points[:5]):
                        st.markdown(f'<div class="summary-point"><b>0{i+1}.</b> {point}.</div>', unsafe_allow_html=True)
                else:
                    st.write("Description not available.")

        except Exception as e:
            st.error("Error retrieving data. Ensure the ticker is active and try again.")

st.markdown("---")
st.caption("Data source: Yahoo Finance Intelligence")