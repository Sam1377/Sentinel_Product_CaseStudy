import streamlit as st
import requests
import json
import time
import numpy as np
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="Sentinel AI Terminal",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Institutional FinTech Theme CSS Injections
st.markdown("""
    <style>
        /* Base Dark Palette & Clean Typography */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #080b10 !important;
            color: #adbac7 !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        }
        
        /* Header Customization */
        [data-testid="stHeader"] {
            background-color: rgba(8, 11, 16, 0.8) !important;
            backdrop-filter: blur(12px);
        }
        
        /* Premium Solid Containers */
        .terminal-card {
            background-color: #0d1117;
            border: 1px solid #21262d;
            border-radius: 6px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        }
        
        /* Clean Technical Navigation Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #0d1117;
            border-radius: 6px;
            padding: 4px;
            border: 1px solid #21262d;
            gap: 4px;
        }
        .stTabs [data-baseweb="tab"] {
            color: #768390 !important;
            font-weight: 600;
            padding: 10px 20px;
            border-radius: 4px;
            transition: all 0.2s ease;
        }
        .stTabs [aria-selected="true"] {
            color: #58a6ff !important;
            background-color: #1c2128 !important;
        }
        
        /* Dynamic Risk Alert Blocks */
        .intercept-card-high {
            background-color: #1f1212;
            border: 1px solid #ff6b6b;
            border-radius: 6px;
            padding: 20px;
            color: #ff9b9b;
        }
        
        .intercept-card-moderate {
            background-color: #1e1710;
            border: 1px solid #d48a37;
            border-radius: 6px;
            padding: 20px;
            color: #f0b36a;
        }

        /* Orderbook Typography */
        .ob-bid { color: #26a641; font-family: monospace; text-align: left; }
        .ob-ask { color: #ff6b6b; font-family: monospace; text-align: left; }
        .ob-hdr { color: #768390; font-family: monospace; font-size: 11px; text-transform: uppercase; }
        
        /* Metric Adjustments */
        div[data-testid="stMetric"] {
            background-color: #0d1117;
            padding: 14px;
            border-radius: 6px;
            border: 1px solid #21262d;
        }
        div[data-testid="stMetricValue"] {
            color: #58a6ff !important;
            font-family: 'SF Mono', Courier, monospace;
            font-size: 1.6rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Top Banner & Brand HUD Layout
col_logo, col_market_ticker = st.columns([2, 5])
with col_logo:
    st.markdown("<h3 style='margin:0; color:#ffffff; letter-spacing:-0.5px;'>SENTINEL SYSTEM <span style='color:#58a6ff; font-weight:300;'>AI</span></h3>", unsafe_allow_html=True)
    st.caption("Pre-Trade Risk Management Infrastructure")

with col_market_ticker:
    st.markdown(
        "<div style='text-align: right; font-family: monospace; font-size: 12px; color: #768390; padding-top: 8px;'>"
        "<span style='color:#26a641;'>NIFTY 50: 23,512.40 (+0.42%)</span> | "
        "<span style='color:#26a641;'>BANKNIFTY: 52,240.15 (+0.68%)</span> | "
        "<span style='color:#ff6b6b;'>INDIA VIX: 13.42 (-2.15%)</span>"
        "</div>", 
        unsafe_allow_html=True
    )

st.write("---")

tab_terminal, tab_analytics = st.tabs(["LIVE TRADING HUB", "PLATFORM PERFORMANCE MONITOR"])

with tab_terminal:
    col_control, col_display = st.columns([4, 5], gap="large")
    
    with col_control:
        st.markdown("<div class='terminal-card'>", unsafe_allow_html=True)
        st.markdown("<h5 style='margin-top:0; color:#ffffff; border-bottom: 1px solid #21262d; padding-bottom:8px;'>Order Configurator</h5>", unsafe_allow_html=True)
        
        user_id = st.text_input("Demat Account Identifier", "USR-705844")
        instrument = st.selectbox("Derivative Target Asset Chain", [
            "BANKNIFTY 25 JUN 52200 CE (Weekly Option Contract)",
            "NIFTY 25 JUN 23500 PE (Near-The-Money Option)",
            "RELIANCE CASH INTRADAY (High Liquidity Equity)"
        ])
        
        order_mode = st.radio("Execution Routing Mode", ["MARKET", "LIMIT"], horizontal=True)
        
        st.markdown("<br><b style='color:#adbac7; font-size:14px;'>Position Parameters</b>", unsafe_allow_html=True)
        quantity = st.slider("Order Sizing Scale (Lots / Units)", min_value=15, max_value=750, value=75, step=15)
        price = st.number_input("Limit Strike Boundary Price (INR)", min_value=1.0, value=312.45, step=5.0)
        
        st.markdown("<br>", unsafe_allow_html=True)
        submit_order = st.button("Transmit Order Intention Vector", type="primary", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # INTERACTIVE MATRIX MODULE: Real-Time Interactive Orderbook HUD generator
        st.markdown("<div class='terminal-card'>", unsafe_allow_html=True)
        st.markdown("<h6 style='margin-top:0; color:#ffffff;'>Real-Time Market Depth (L2 Query Mirror)</h6>", unsafe_allow_html=True)
        
        # Dynamic layout changing depending completely on the chosen menu item
        if "BANKNIFTY" in instrument:
            bids = [(312.45, 1200), (312.30, 850), (312.15, 2100)]
            asks = [(315.65, 450), (315.90, 1100), (316.45, 900)]
            spread_str = "1.02% (Wide Spread Flag)"
        elif "NIFTY" in instrument:
            bids = [(142.10, 3400), (142.00, 5100), (141.85, 4200)]
            asks = [(142.95, 1200), (143.15, 2300), (143.50, 1800)]
            spread_str = "0.60% (Moderate Spread)"
        else:
            bids = [(2845.10, 8900), (2844.75, 12400), (2844.20, 15100)]
            asks = [(2845.45, 7600), (2845.90, 9300), (2846.15, 11200)]
            spread_str = "0.01% (Highly Liquid)"
            
        col_b, col_a = st.columns(2)
        with col_b:
            st.markdown("<span class='ob-hdr'>Bid Price (Qty)</span>", unsafe_allow_html=True)
            for b_p, b_q in bids:
                st.markdown(f"<div class='ob-bid'>{b_p:.2f} <span style='color:#768390; font-size:11px;'>({b_q})</span></div>", unsafe_allow_html=True)
        with col_a:
            st.markdown("<span class='ob-hdr'>Ask Price (Qty)</span>", unsafe_allow_html=True)
            for a_p, a_q in asks:
                st.markdown(f"<div class='ob-ask'>{a_p:.2f} <span style='color:#768390; font-size:11px;'>({a_q})</span></div>", unsafe_allow_html=True)
                
        st.markdown(f"<p style='font-size:11px; color:#768390; margin-top:8px; margin-bottom:0;'>Calculated Instrument Implied Spread: {spread_str}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_display:
        st.markdown("<h5 style='margin-top:0; color:#ffffff;'>Telemetry Intercept Pipeline Output</h5>", unsafe_allow_html=True)
        
        if submit_order:
            payload = {
                "instrument": instrument,
                "order_type": order_mode,
                "quantity": int(quantity),
                "price": float(price),
                "user_id": user_id
            }
            
            try:
                response = requests.post("http://127.0.0.1:8001/api/v1/risk/evaluate", json=payload)
                data = response.json()
                
                score = data["risk_score"]
                classification = data["risk_classification"]
                latency = data["latency_ms"]
                
                if classification == "HIGH":
                    st.markdown(f"""
                        <div class='intercept-card-high'>
                            <h4 style='margin-top:0; font-weight:700;'>SYSTEM REJECTION CHECKPOINT ENGAGED</h4>
                            <p style='font-size:14px; margin: 4px 0;'><b>Composite Risk Metric Score:</b> {score} / 100</p>
                            <p style='font-size:13px; opacity:0.9;'><b>Trigger Constraint Vector:</b> {data.get('primary_risk_driver', 'BEHAVIORAL_REVENGE_TRADING')}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.error("Pre-Trade Guardrail Breach: This instruction matches localized revenge scaling profiles. Account execution matrix locked down.")
                    
                    progress_text = "System friction protocol sequence active. Stabilizing client state..."
                    progress_bar = st.progress(0, text=progress_text)
                    for pct in range(100):
                        time.sleep(0.02)
                        progress_bar.progress(pct + 1, text=progress_text)
                    st.toast("Friction constraint loop completed.", icon="⚠️")
                    
                elif classification == "MODERATE":
                    st.markdown(f"""
                        <div class='intercept-card-moderate'>
                            <h4 style='margin-top:0; font-weight:700;'>SLIPPAGE EXPOSURE ADVISORY WARNING</h4>
                            <p style='margin:0;'><b>Composite Risk Score:</b> {score} / 100</p>
                        </div>
                    """, unsafe_allow_html=True)
                    st.warning("Microstructure Health Warning: Executing volume market instructions inside wide spread order books generates instant execution drag. Limit modification recommended.")
                else:
                    st.markdown(f"""
                        <div class='terminal-card' style='border-color: #26a641; background-color: #0f1912;'>
                            <h4 style='color: #26a641; margin-top:0;'>TRANSACTION VALIDATION COMPLIANT</h4>
                            <p style='margin:0; color:#adbac7;'><b>Risk Compliance Score:</b> {score} / 100</p>
                        </div>
                    """, unsafe_allow_html=True)
                    st.success("Order payload structural configuration within parameter limits. Routed directly to core broker match systems.")

                # Interactive Bar Chart Output Module
                st.markdown("<br><h6 style='color:#ffffff;'>Quantitative Index Distribution Matrix</h6>", unsafe_allow_html=True)
                breakdown_data = data["breakdown"]
                chart_df = pd.DataFrame({
                    "Risk Metric Category": list(breakdown_data.keys()),
                    "Stress Level Value": list(breakdown_data.values())
                })
                st.bar_chart(chart_df, x="Risk Metric Category", y="Stress Level Value", color="#58a6ff", use_container_width=True)
                
                st.metric(label="Pre-Trade Gateway processing Latency", value=f"{latency} ms")
                
            except requests.exceptions.ConnectionError:
                st.error("Connection Refused. Please verify background microservice engine process ('core_engine/main.py') is active on port 8001.")
        else:
            st.info("Awaiting execution vector trigger. Adjust configurations and transmit to evaluate performance metrics.")

with tab_analytics:
    st.markdown("<h5 style='color:#ffffff; margin-top:0;'>Product Operations & Experiment Tracking Cockpit</h5>", unsafe_allow_html=True)
    st.caption("Measuring engine algorithmic reliability parameters alongside customer preservation outcomes.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_k1, col_k2, col_k3 = st.columns(3)
    with col_k1:
        st.metric(label="Trader Capital Survival Velocity (North Star)", value="+44.8 Business Days", delta="Strategic Account Retention")
    with col_k2:
        st.metric(label="High-Risk Parameter Override Dropout Rate", value="36.2%", delta="14.5% Improvement MoM")
    with col_k3:
        st.metric(label="p99 System Pre-Trade Validation Latency", value="3.140 ms", delta="Within 8ms SLA Limit")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("<div class='terminal-card'>", unsafe_allow_html=True)
        st.markdown("<h6 style='margin-top:0; color:#ffffff;'>Cohort Survival Trajectory (Simulated 60-Day Window)</h6>", unsafe_allow_html=True)
        
        chart_days = np.arange(1, 61)
        sentinel_cohort_survival = 100 * np.exp(-0.008 * chart_days)
        standard_cohort_survival = 100 * np.exp(-0.021 * chart_days)
        
        cohort_df = pd.DataFrame({
            "Active Trading Session Days": chart_days,
            "With Sentinel Protection Layer (%)": sentinel_cohort_survival,
            "Standard Unprotected Accounts (%)": standard_cohort_survival
        }).set_index("Active Trading Session Days")
        st.line_chart(cohort_df, color=["#58a6ff", "#ff6b6b"])
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_g2:
        st.markdown("<div class='terminal-card'>", unsafe_allow_html=True)
        st.markdown("<h6 style='margin-top:0; color:#ffffff;'>System Architecture Pipeline Architecture</h6>", unsafe_allow_html=True)
        st.markdown(
            "<div style='font-size:13px; line-height:1.6; color:#adbac7;'>"
            "1. UDP Multicast Direct Exchange ticks stream directly into Apache Kafka cluster queues.<br>"
            "2. Distributed Flink cluster engine tracks dynamic sliding loss boundaries and velocity vectors.<br>"
            "3. State snapshots are loaded out-of-band directly into memory cache tables via Redis clusters.<br>"
            "4. The Risk Evaluator intercepts order hooks, matching parameters completely inside memory maps within 8 milliseconds."
            "</div>",
            unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
