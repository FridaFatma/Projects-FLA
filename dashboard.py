import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# -------------------------------------------------------------
# 1. PAGE CONFIG
# -------------------------------------------------------------
st.set_page_config(
    page_title="PT X - Beauty Management Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# 2. LIVE GOOGLE SHEETS DATA ENGINE
# -------------------------------------------------------------
SPREADSHEET_ID = "1aiOOaoXg_Yo00xh-X5A29W3NlfAm0xWq5nNYB1a-co4"

@st.cache_data(ttl=600)
def load_gsheet_data(sheet_name="Sheet1"):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        return pd.read_csv(url)
    except Exception as e:
        return None

df_live = load_gsheet_data()

# -------------------------------------------------------------
# 3. FULLY RESPONSIVE CSS OVERRIDE (AUTO-ADAPT TO SCREEN SIZE)
# -------------------------------------------------------------
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&display=swap');

    :root {
        --primary-color: #013AC9 !important;
        --background-color: #EEF2F6 !important;
        --secondary-background-color: #FFFFFF !important;
        --text-color: #1E293B !important;
    }

    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main, * {
        font-family: 'DM Sans', sans-serif !important;
        box-sizing: border-box !important;
    }

    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #EEF2F6 !important;
        color: #1E293B !important;
    }

    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* CONTAINER RESPONSIVE PADDING */
    .main .block-container {
        padding-top: 1.2rem !important;
        padding-left: clamp(1rem, 2vw, 2rem) !important;
        padding-right: clamp(1rem, 2vw, 2rem) !important;
        background-color: #EEF2F6 !important;
        max-width: 100% !important;
    }

    /* SIDEBAR RESPONSIVE */
    section[data-testid="stSidebar"] {
        background-color: #013AC9 !important;
        border: none !important;
        width: clamp(210px, 16vw, 255px) !important;
        min-width: 200px !important;
    }

    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }

    /* NAV SIDEBAR BUTTONS */
    [class*="st-key-navrow_"] {
        position: relative !important;
        margin-bottom: 4px !important;
    }
    .nav-row {
        position: relative;
        z-index: 1;
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 14px;
        border-radius: 12px;
        color: #FFFFFF;
        font-size: clamp(12px, 0.9vw, 13.5px);
        font-weight: 500;
        pointer-events: none;
        white-space: nowrap;
    }
    .nav-row svg { flex-shrink: 0; }
    .nav-row.active {
        background-color: #CCFF00;
        color: #013AC9 !important;
        font-weight: 700;
    }
    .nav-row.active span,
    .nav-row.active svg {
        color: #013AC9 !important;
        stroke: #013AC9 !important;
    }

    [class*="st-key-navrow_"] div[data-testid="stButton"] {
        position: absolute !important;
        inset: 0 !important;
        margin: 0 !important;
        z-index: 2 !important;
    }
    [class*="st-key-navrow_"] div[data-testid="stButton"] button {
        width: 100% !important;
        height: 100% !important;
        opacity: 0 !important;
        border: none !important;
        background: transparent !important;
        cursor: pointer !important;
        padding: 0 !important;
    }

    /* SELECTBOX STYLING */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 2px 6px !important;
    }
    div[data-baseweb="select"] * {
        color: #1E293B !important;
    }

    /* SLIDER STYLING */
    div[data-baseweb="slider"] [role="slider"] {
        background-color: #013AC9 !important;
        border: 2px solid #FFFFFF !important;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.15) !important;
    }
    div[data-baseweb="slider"] div[style*="background"] {
        background-color: #013AC9 !important;
    }
    div[data-baseweb="slider"] div {
        background-color: #013AC9 !important;
    }
    div[data-testid="stWidgetLabel"] p {
        color: #1E293B !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }

    /* CARDS UI & RESPONSIVE METRICS */
    .ui-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0;
        border-radius: 20px;
        padding: clamp(14px, 1.5vw, 22px);
        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.02);
        margin-bottom: 16px;
        width: 100% !important;
    }

    .alert-card {
        background-color: #013AC9 !important;
        border-radius: 20px;
        padding: clamp(14px, 1.5vw, 20px);
        color: white;
        height: 100%;
    }
    .alert-title { font-size: 14px; font-weight: 700; color: #CCFF00; margin-bottom: 8px; }
    .alert-body { font-size: 11.5px; line-height: 1.5; color: #FFFFFF; margin-bottom: 16px; }
    .alert-btn { background: rgba(255, 255, 255, 0.2); color: white; padding: 8px 14px; border-radius: 10px; font-size: 11px; font-weight: 600; display: inline-block; }

    .kpi-card { 
        background: #FFFFFF !important; 
        border: 1px solid #E2E8F0; 
        border-radius: 20px; 
        padding: clamp(12px, 1.2vw, 18px); 
        height: 100%; 
    }
    .kpi-label { font-size: 11.5px; color: #64748B; font-weight: 500; }
    /* Dynamic Font Size agar Angka KPI Tidak Pernah Pindah Baris */
    .kpi-value { 
        font-size: clamp(18px, 1.8vw, 26px) !important; 
        font-weight: 700; 
        color: #013AC9; 
        margin: 4px 0px; 
        white-space: nowrap !important;
    }

    .custom-table { width: 100%; border-collapse: collapse; font-family: 'DM Sans', sans-serif !important; }
    .custom-table th { text-align: left; font-size: 11px; font-weight: 600; color: #94A3B8; padding: 10px 6px; border-bottom: 1px solid #F1F5F9; }
    .custom-table td { padding: 10px 6px; font-size: 12px; color: #1E293B; border-bottom: 1px solid #F8FAFC; vertical-align: middle; }

    .badge { padding: 4px 8px; border-radius: 12px; font-size: 10px; font-weight: 600; display: inline-block; white-space: nowrap; }
    .badge-danger { background-color: #FEE2E2; color: #991B1B; border: 1px solid #FECACA; }
    .badge-warning { background-color: #FEF3C7; color: #92400E; border: 1px solid #FDE68A; }
    .badge-info { background-color: #DBEAFE; color: #013AC9; border: 1px solid #BFDBFE; }
    .badge-gray { background-color: #F1F5F9; color: #475569; border: 1px solid #E2E8F0; }

    .st-key-filter_card > div,
    .st-key-chart_card > div,
    .st-key-progress_card > div,
    .st-key-slider_card > div {
        border: none !important;
    }
    .st-key-chart_card,
    .st-key-progress_card,
    .st-key-slider_card {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 20px !important;
        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.02) !important;
        padding: 6px !important;
    }

    .st-key-filter_card {
        background-color: #F3F6FE !important;
        border: 1px solid #DCE4FA !important;
        border-left: 4px solid #013AC9 !important;
        border-radius: 14px !important;
        box-shadow: none !important;
        padding: 8px 14px 4px 14px !important;
        margin-bottom: 16px !important;
    }
    .st-key-filter_card [data-testid="stWidgetLabel"] p {
        text-transform: uppercase !important;
        letter-spacing: 0.4px !important;
        font-size: 10.5px !important;
        color: #64748B !important;
        font-weight: 700 !important;
    }
    .filter-bar-tag {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
        color: #013AC9;
        text-transform: uppercase;
        margin-bottom: 4px;
    }

    /* MEDIA BREAKPOINTS UNTUK MONITORS / LAPTOPS */
    @media (max-width: 1200px) {
        .kpi-value { font-size: 18px !important; }
        .alert-title { font-size: 13px; }
        .alert-body { font-size: 11px; }
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 4. SIDEBAR HEADER & NAVIGATION
# -------------------------------------------------------------
ICON_SVG = {
    "Stock & Returns": '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>',
    "Safety Stock Alerts": '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"></path><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"></path>',
    "Product Lifecycle": '<polyline points="23 4 23 10 17 10"></polyline><polyline points="1 20 1 14 7 14"></polyline><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>',
    "Ad Spend & Cap": '<line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>',
    "Margin Simulator": '<line x1="19" y1="5" x2="5" y2="19"></line><circle cx="6.5" cy="6.5" r="2.5"></circle><circle cx="17.5" cy="17.5" r="2.5"></circle>',
    "Settings": '<circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"></path>',
}
NAV_ITEMS = list(ICON_SVG.keys())

if "selected_module" not in st.session_state:
    st.session_state.selected_module = NAV_ITEMS[0]

with st.sidebar:
    st.markdown("""<div style="display: flex; align-items: center; gap: 12px; padding: 10px 0px 25px 0px;">
            <div style="width: 38px; height: 38px; background-color: #CCFF00; border-radius: 10px; flex-shrink:0;"></div>
            <div>
                <div style="font-size: 17px; font-weight: 700; line-height: 1.1; color: #FFFFFF;">PT X</div>
                <div style="font-size: 9.5px; font-weight: 600; letter-spacing: 1px; color: #CCFF00;">DASHBOARD</div>
            </div>
        </div>""", unsafe_allow_html=True)

    for i, label in enumerate(NAV_ITEMS):
        is_active = st.session_state.selected_module == label
        slug = f"navrow_{i}"
        with st.container(key=slug):
            st.markdown(f'''<div class="nav-row {"active" if is_active else ""}"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="{"#013AC9" if is_active else "#FFFFFF"}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICON_SVG[label]}</svg><span>{label}</span></div>''', unsafe_allow_html=True)
            if st.button(label, key=f"nav_btn_{i}", use_container_width=True):
                st.session_state.selected_module = label
                st.rerun()

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("""<div style='font-size: 13px; font-weight: 600; opacity: 0.85; padding-left: 10px; display: flex; align-items: center; gap: 8px;'>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
            Log Out
        </div>""", unsafe_allow_html=True)

selected_module = st.session_state.selected_module

# -------------------------------------------------------------
# 5. HEADER BUILDER
# -------------------------------------------------------------
def render_header(title, subtitle):
    col_t, col_s = st.columns([3, 1])
    with col_t:
        st.markdown("<span style='color:#64748B; font-size:13px; font-weight:500;'>Hi Gigi,</span>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='color:#013AC9; font-size:clamp(20px, 2vw, 26px); font-weight:700; margin-top:-6px;'>{title}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#64748B; font-size:12.5px; margin-top:-10px;'>{subtitle}</p>", unsafe_allow_html=True)
    with col_s:
        st.text_input("Search", placeholder="🔍 Search...", label_visibility="collapsed")

# -------------------------------------------------------------
# MODUL 1: STOCK & RETURNS TRACKING
# -------------------------------------------------------------
if selected_module == "Stock & Returns":
    render_header("Stock & Return Tracking", "Monitor real-time stockout, overstock & return rates per SKU and foundation shade")

    with st.container(border=True, key="filter_card"):
        st.markdown('<div class="filter-bar-tag"> Filters</div>', unsafe_allow_html=True)
        f1, f2, f3 = st.columns(3)
        with f1: st.selectbox("Timeframe", ["All-time", "H1 2026", "FY 2025"])
        with f2: st.selectbox("SKU", ["All", "Z Soft Matte Foundation", "Z Hybrid Cushion"])
        with f3: st.selectbox("Channels", ["All", "Marketplace A", "Social Commerce"])

    c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1])
    with c1:
        st.markdown("""<div class="alert-card">
            <div class="alert-title">Executive Alert</div>
            <div class="alert-body">Hero SKU (Medium Warm) stockout hit <b style="color:#CCFF00;">22%</b> while Tan/Deep overstock reached <b style="color:#CCFF00;">26%</b></div>
            <div class="alert-btn">Action: Rebalance PO</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="kpi-card">
            <div class="kpi-label">Avg Stockout Rate</div>
            <div class="kpi-value">16%</div>
            <div style="font-size:11px; color:#DC2626; font-weight:600;">Touching danger ceiling</div>
            <div style="font-size:11px; color:#64748B; margin-top:6px;">Critical in: <b>Medium Warm (22%)</b></div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="kpi-card">
            <div class="kpi-label">Avg Overstock Rate</div>
            <div class="kpi-value">21%</div>
            <div style="font-size:11px; color:#DC2626; font-weight:600;">At risk ceiling</div>
            <div style="font-size:11px; color:#64748B; margin-top:6px;">Excess in: <b>Tan/Deep (26%)</b></div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""<div class="kpi-card">
            <div class="kpi-label">Avg Return Rate</div>
            <div class="kpi-value">8.2%</div>
            <div style="font-size:11px; color:#DC2626; font-weight:600;">+1.7% above safe limit</div>
            <div style="font-size:11px; color:#64748B; margin-top:6px;">Primary driver: <b>65% Shade Mismatch</b></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1.4, 1.1])
    with col_left:
        st.markdown("""<div class="ui-card">
            <h3 style="font-size:15px; color:#013AC9; margin-bottom:14px; font-weight:600;">SKU & Shade Health Matrix</h3>
            <table class="custom-table">
                <tr><th>Shade</th><th>Share</th><th>Stockout</th><th>Overstock</th><th>Return</th></tr>
                <tr><td><span style="color:#F3E5D8;">●</span> <b>Light Neutral</b></td><td>22%</td><td><span class="badge badge-danger">18%</span></td><td>8%</td><td>5%</td></tr>
                <tr><td><span style="color:#E2C4A8;">●</span> <b>Medium Warm</b></td><td>31%</td><td><span class="badge badge-danger">22%</span></td><td>6%</td><td>6%</td></tr>
                <tr><td><span style="color:#D4B293;">●</span> <b>Medium Neutral</b></td><td>25%</td><td>14%</td><td>7%</td><td>5.5%</td></tr>
                <tr><td><span style="color:#A07855;">●</span> <b>Tan / Deep</b></td><td>12%</td><td>5%</td><td><span class="badge badge-warning">26%</span></td><td><span class="badge badge-danger">11%</span></td></tr>
                <tr><td><span style="color:#B8976C;">●</span> <b>Olive</b></td><td>10%</td><td>7%</td><td><span class="badge badge-warning">22%</span></td><td><span class="badge badge-warning">10.5%</span></td></tr>
            </table>
        </div>""", unsafe_allow_html=True)

    with col_right:
        with st.container(border=True, key="chart_card"):
            st.markdown("""<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 5px; padding:8px 8px 0 8px;">
                <b style="font-size:15px; font-weight:600; color:#013AC9;">Return Reasons</b>
                <span class="badge badge-gray">Today</span>
            </div>""", unsafe_allow_html=True)

            fig = go.Figure(data=[go.Pie(
                labels=['Shade Mismatch', 'Product Defect', 'Fulfillment Error', 'Buyer Remorse'],
                values=[65, 15, 12, 8],
                hole=.65,
                marker=dict(colors=['#CCFF00', '#002B7F', '#013AC9', '#94A3B8']),
                textinfo='percent',
                textposition='inside',
                insidetextorientation='radial',
                textfont=dict(color=['#0F172A', '#FFFFFF', '#FFFFFF', '#FFFFFF'], size=10)
            )])

            fig.update_layout(
                showlegend=True,
                height=230,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                legend=dict(
                    orientation="h",
                    y=-0.15,
                    x=0.5,
                    xanchor="center",
                    font=dict(color="#475569", size=9)
                )
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# -------------------------------------------------------------
# MODUL 2: SAFETY STOCK ALERTS
# -------------------------------------------------------------
elif selected_module == "Safety Stock Alerts":
    render_header("Safety Stocks Alert", "Track low stock levels & estimated stockout time.")

    with st.container(border=True, key="filter_card"):
        st.markdown('<div class="filter-bar-tag"> Filters</div>', unsafe_allow_html=True)
        f1, f2, f3 = st.columns(3)
        with f1: st.selectbox("Timeframe", ["All-time"])
        with f2: st.selectbox("SKU", ["All"])
        with f3: st.selectbox("Status", ["All"])

    c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1])
    with c1:
        st.markdown("""<div class="alert-card">
            <div class="alert-title">Executive Alert</div>
            <div class="alert-body">2 SKU/shade combinations require immediate <b>reorder action</b>. Z Soft Matte Foundation (Medium Warm) is at <b>22%</b> of safety threshold.</div>
            <div class="alert-btn">Action: Create Purchase Order</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="kpi-card">
            <div class="kpi-label">Active Alert</div>
            <div class="kpi-value">2</div>
            <div style="font-size:11px; color:#DC2626; font-weight:600;">Critical low stock</div>
            <div style="font-size:11px; color:#64748B; margin-top:6px;">Critical in: <b>Medium Warm (22%)</b></div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="kpi-card">
            <div class="kpi-label">Avg Days to Stockout</div>
            <div class="kpi-value">6</div>
            <div style="font-size:11px; color:#DC2626; font-weight:600;">Approaching threshold</div>
            <div style="font-size:11px; color:#64748B; margin-top:6px;">Lowest Stock: <b>Medium Warm</b></div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""<div class="kpi-card">
            <div class="kpi-label">Reorder Success (30d)</div>
            <div class="kpi-value">85%</div>
            <div style="font-size:11px; color:#166534; font-weight:600;">+1.7% vs last month</div>
            <div style="font-size:11px; color:#64748B; margin-top:6px;">Target Rate: <b>85%</b></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1.4, 1.2])
    with col_l:
        st.markdown("""<div class="ui-card">
            <h3 style="font-size:15px; color:#013AC9; margin-bottom:14px; font-weight:600;">SKU & Shade Status</h3>
            <table class="custom-table">
                <tr><th>SKU</th><th>Shade</th><th>Stock</th><th>Threshold</th><th>Status</th></tr>
                <tr><td>Z Soft Matte Foundation</td><td>Light Neutral</td><td>470</td><td>550</td><td><span class="badge badge-warning">Approaching</span></td></tr>
                <tr><td>Z Hybrid Cushion</td><td>Medium Warm</td><td>180</td><td>800</td><td><span class="badge badge-danger">Below Safety</span></td></tr>
                <tr><td>Z Soft Matte Foundation</td><td>Medium Neutral</td><td>620</td><td>650</td><td><span class="badge badge-info">Safety</span></td></tr>
                <tr><td>Z Soft Matte Foundation</td><td>Tan / Deep</td><td>380</td><td>300</td><td><span class="badge badge-warning">Overstock</span></td></tr>
                <tr><td>Z Hybrid Cushion</td><td>Olive</td><td>540</td><td>400</td><td><span class="badge badge-warning">Overstock</span></td></tr>
            </table>
        </div>""", unsafe_allow_html=True)

    with col_r:
        with st.container(border=True, key="progress_card"):
            st.markdown('<div style="padding:8px 8px 0 8px;"><b style="font-size:15px; font-weight:600; color:#013AC9;">Stock vs. Threshold Progress</b></div><br>', unsafe_allow_html=True)
            shades = [
                {"name": "Light Neutral", "val": 470, "max": 550, "status": "Approaching", "clr": "#F59E0B"},
                {"name": "Medium Warm", "val": 180, "max": 800, "status": "Below Safety", "clr": "#EF4444"},
                {"name": "Medium Neutral", "val": 620, "max": 650, "status": "Safety", "clr": "#013AC9"},
                {"name": "Tan / Deep", "val": 380, "max": 300, "status": "Overstock", "clr": "#F59E0B"},
                {"name": "Olive", "val": 540, "max": 400, "status": "Overstock", "clr": "#F59E0B"}
            ]
            rows_html = ""
            for s in shades:
                pct = min(int((s["val"] / s["max"]) * 100), 100)
                rows_html += f'<div style="margin-bottom:12px;"><div style="display:flex; justify-content:space-between; font-size:11px;"><span><b>{s["name"]}</b> ({s["val"]}/{s["max"]} units)</span><span style="color:{s["clr"]}; font-weight:700;">{s["status"]}</span></div><div style="background:#F1F5F9; border-radius:4px; height:8px; width:100%; margin-top:3px;"><div style="background:{s["clr"]}; border-radius:4px; height:8px; width:{pct}%;"></div></div></div>'
            st.markdown(f'<div style="padding:0 8px 8px 8px;">{rows_html}</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# MODUL 3: PRODUCT LIFECYCLE
# -------------------------------------------------------------
elif selected_module == "Product Lifecycle":
    render_header("Product Lifecycle", "Classify SKU performance to scale, bundle, or hold.")

    with st.container(border=True, key="filter_card"):
        st.markdown('<div class="filter-bar-tag"> Filters</div>', unsafe_allow_html=True)
        f1, f2, f3 = st.columns(3)
        with f1: st.selectbox("Timeframe", ["All-time"])
        with f2: st.selectbox("SKU", ["All"])
        with f3: st.selectbox("Shade Group", ["All"])

    c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1])
    with c1:
        st.markdown("""<div class="alert-card">
            <div class="alert-title">Executive Alert</div>
            <div class="alert-body">Olive shade falls into hold category due to high <b>overstock & return</b>.</div>
            <div class="alert-btn">Action: View Bundling</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="kpi-card">
            <div class="kpi-label">Keep / Scale</div>
            <div class="kpi-value">1 SKU</div>
            <div style="font-size:11px; color:#166534; font-weight:600;">Top Prioritize</div>
            <div style="font-size:11px; color:#64748B; margin-top:6px;">Top Performer: <b>Z Soft Matte</b></div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="kpi-card">
            <div class="kpi-label">Bundle Candidates</div>
            <div class="kpi-value">1 SKU</div>
            <div style="font-size:11px; color:#92400E; font-weight:600;">Follow Up</div>
            <div style="font-size:11px; color:#64748B; margin-top:6px;">Slow mover: <b>Z Hybrid Cushion</b></div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""<div class="kpi-card">
            <div class="kpi-label">Hold Candidates</div>
            <div class="kpi-value">2 Shades</div>
            <div style="font-size:11px; color:#DC2626; font-weight:600;">Reduce Production</div>
            <div style="font-size:11px; color:#64748B; margin-top:6px;">Critical: <b>Olive & Tan/Deep</b></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1.4, 1.2])
    with col_l:
        st.markdown("""<div class="ui-card">
            <h3 style="font-size:15px; color:#013AC9; margin-bottom:14px; font-weight:600;">SKU & Shade Status</h3>
            <table class="custom-table">
                <tr><th>SKU</th><th>Shade</th><th>Sales Share</th><th>Overstock</th><th>Status</th></tr>
                <tr><td>Z Soft Matte Foundation</td><td>Light Neutral</td><td>28%</td><td>7.0%</td><td><span class="badge badge-info">Keep</span></td></tr>
                <tr><td>Z Hybrid Cushion</td><td>Medium Warm</td><td>18%</td><td>9.0%</td><td><span class="badge badge-warning">Bundle</span></td></tr>
                <tr><td>Z Soft Matte Foundation</td><td>Medium Neutral</td><td>12%</td><td>8.5%</td><td><span class="badge badge-gray">Routine</span></td></tr>
                <tr><td>Z Soft Matte Foundation</td><td>Tan / Deep</td><td>12%</td><td>26.0%</td><td><span class="badge badge-danger">Hold</span></td></tr>
                <tr><td>Z Hybrid Cushion</td><td>Olive</td><td>10%</td><td>22.0%</td><td><span class="badge badge-danger">Hold</span></td></tr>
            </table>
        </div>""", unsafe_allow_html=True)

    with col_r:
        st.markdown("""<div class="ui-card">
            <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                <b style="font-size:15px; font-weight:600; color:#013AC9;">Classification Share</b>
                <span class="badge badge-gray">All-time</span>
            </div>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:8px; height:170px;">
                <div style="background:#CCFF00; padding:12px; border-radius:12px; grid-row: span 2;">
                    <b style="font-size:12px; color:#0F172A;">Hold / Cut</b>
                    <div style="font-size:24px; font-weight:800; color:#0F172A;">40%</div>
                    <div style="font-size:10px; color:#334155; margin-top:35px;">2 Shades</div>
                </div>
                <div style="background:#002B7F; color:white; padding:10px; border-radius:10px;">
                    <b style="font-size:10px;">Keep / Scale</b>
                    <div style="font-size:16px; font-weight:700;">20%</div>
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:4px;">
                    <div style="background:#013AC9; color:white; padding:6px; border-radius:8px; font-size:9px;">
                        <b>Bundle</b><br><b>20%</b>
                    </div>
                    <div style="background:#94A3B8; color:white; padding:6px; border-radius:8px; font-size:9px;">
                        <b>Routine</b><br><b>20%</b>
                    </div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

# -------------------------------------------------------------
# MODUL 4: AD SPEND & CAP
# -------------------------------------------------------------
elif selected_module == "Ad Spend & Cap":
    render_header("Ad Spend & Cap", "Monitor ad spend ratio across channels vs. threshold caps")

    with st.container(border=True, key="filter_card"):
        st.markdown('<div class="filter-bar-tag"> Filters</div>', unsafe_allow_html=True)
        f1, f2, f3 = st.columns(3)
        with f1: st.selectbox("Timeframe", ["Period H1 2026"])
        with f2: st.selectbox("Channel", ["All"])
        with f3: st.selectbox("Campaign Type", ["All"])

    c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1])
    with c1:
        st.markdown("""<div class="alert-card">
            <div class="alert-title">Executive Alert</div>
            <div class="alert-body">Marketplace A ad spend ratio exceeded cap for 3 consecutive days (<b style="color:#CCFF00;">13.4% vs 12% cap</b>).</div>
            <div class="alert-btn">Action: Review Budget</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="kpi-card">
            <div class="kpi-label">Channels Above Cap</div>
            <div class="kpi-value">2 of 5</div>
            <div style="font-size:11px; color:#DC2626; font-weight:600;">Above Cap</div>
            <div style="font-size:11px; color:#64748B; margin-top:6px;">Most Automated: <b>Marketplace A</b></div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="kpi-card">
            <div class="kpi-label">Set Cap Limit</div>
            <div class="kpi-value">12.0%</div>
            <div style="font-size:11px; color:#64748B;">Standard threshold</div>
            <div style="font-size:11px; color:#64748B; margin-top:6px;">Automated Channels: <b>2 of 5</b></div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""<div class="kpi-card">
            <div class="kpi-label">Highest Ratio</div>
            <div class="kpi-value">15%</div>
            <div style="font-size:11px; color:#DC2626; font-weight:600;">Approaching Limit</div>
            <div style="font-size:11px; color:#64748B; margin-top:6px;">Most Severe: <b>Platform O</b></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1.4, 1.2])
    with col_l:
        st.markdown("""<div class="ui-card">
            <h3 style="font-size:15px; color:#013AC9; margin-bottom:14px; font-weight:600;">Ad Spend per Channel</h3>
            <table class="custom-table">
                <tr><th>Channel</th><th>Ad Spend Ratio</th><th>Cap</th><th>Status</th><th>Data Source</th></tr>
                <tr><td>Marketplace A</td><td>13%</td><td>12%</td><td><span class="badge badge-danger">Above Cap</span></td><td>Automated</td></tr>
                <tr><td>Platform O Social Commerce</td><td>15%</td><td>12%</td><td><span class="badge badge-danger">Above Cap</span></td><td>Manual</td></tr>
                <tr><td>Website / CRM</td><td>8%</td><td>12%</td><td><span class="badge badge-info">Safe</span></td><td>Automated</td></tr>
                <tr><td>Offline & Specialty Retail</td><td>5%</td><td>12%</td><td><span class="badge badge-info">Safe</span></td><td>Manual</td></tr>
                <tr><td>Community / Reseller</td><td>6%</td><td>12%</td><td><span class="badge badge-info">Safe</span></td><td>Manual</td></tr>
            </table>
        </div>""", unsafe_allow_html=True)

    with col_r:
        with st.container(border=True, key="progress_card"):
            st.markdown('<div style="padding:8px 8px 0 8px;"><b style="font-size:15px; font-weight:600; color:#013AC9;">Ad Spend Ratio vs. Cap Limit</b></div><br>', unsafe_allow_html=True)
            channels_cap = [
                {"name": "Marketplace A", "ratio": 13, "status": "Above Cap", "clr": "#EF4444"},
                {"name": "Platform O Social Commerce", "ratio": 15, "status": "Above Cap", "clr": "#EF4444"},
                {"name": "Website / CRM", "ratio": 8, "status": "Safe", "clr": "#013AC9"},
                {"name": "Offline & Specialty Retail", "ratio": 5, "status": "Safe", "clr": "#013AC9"},
                {"name": "Community / Reseller", "ratio": 6, "status": "Safe", "clr": "#013AC9"}
            ]
            rows_html = ""
            for ch in channels_cap:
                rows_html += f'<div style="margin-bottom:12px;"><div style="display:flex; justify-content:space-between; font-size:11px;"><span><b>{ch["name"]}</b> (Ratio: {ch["ratio"]}% / Cap 12.0%)</span><span style="color:{ch["clr"]}; font-weight:700;">{ch["status"]}</span></div><div style="background:#F1F5F9; border-radius:4px; height:8px; width:100%; margin-top:3px;"><div style="background:{ch["clr"]}; border-radius:4px; height:8px; width:{min(ch["ratio"]*5, 100)}%;"></div></div></div>'
            st.markdown(f'<div style="padding:0 8px 8px 8px;">{rows_html}</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# MODUL 5: CAMPAIGN MARGIN SIMULATOR
# -------------------------------------------------------------
elif selected_module == "Margin Simulator":
    render_header("Campaign Margin Simulator", "Estimate a campaign's impact on contribution margin before launch")

    SKU_ECONOMICS = {
        "Z Soft Matte Foundation": {"asp": 149000, "cogs": 58000},
        "Z Hybrid Cushion": {"asp": 159000, "cogs": 66000},
    }

    with st.container(border=True, key="filter_card"):
        st.markdown('<div class="filter-bar-tag"> Filters</div>', unsafe_allow_html=True)
        f1, f2 = st.columns(2)
        with f1: target_sku = st.selectbox("SKU", list(SKU_ECONOMICS.keys()))
        with f2: compare_camp = st.selectbox("Compare with", ["Double Date", "Pay Day", "Website/CRM Bundle"])

    col_input, col_kpi = st.columns([1.5, 1])

    with col_input:
        with st.container(border=True, key="slider_card"):
            st.markdown('<div style="padding:8px 8px 0 8px;"><b style="font-size:14px; color:#013AC9; font-weight:600;">Campaign Assumptions & Media Levers</b></div><br>', unsafe_allow_html=True)

            disc_val = st.slider("Campaign Discount", 0, 50, 10, format="%d%% Off")
            sales_lift = st.slider("Target Sales Lift", 0, 100, 20, format="+%d%% Volume")
            ad_spend = st.slider("Campaign Ad Spend (% of GMV)", 0, 30, 20, format="%d%% of GMV")

    econ = SKU_ECONOMICS[target_sku]
    ASP, COGS = econ["asp"], econ["cogs"]

    base_cm = 16.8
    base_units = 100
    units = base_units * (1 + sales_lift / 100)
    revenue = ASP * (1 - disc_val / 100) * units
    cogs_total = COGS * units
    ad_cost = revenue * (ad_spend / 100)
    contribution = revenue - cogs_total - ad_cost
    calculated_cm = round((contribution / revenue) * 100, 1) if revenue > 0 else 0
    margin_diff = round(calculated_cm - base_cm, 1)

    with col_kpi:
        k1, k2 = st.columns(2)
        with k1:
            st.markdown(f"""<div class="kpi-card">
                <div class="kpi-label">Current CM</div>
                <div class="kpi-value">{base_cm}%</div>
            </div>""", unsafe_allow_html=True)
        with k2:
            badge_clr = "#DC2626" if calculated_cm < base_cm else "#166534"
            st.markdown(f"""<div class="kpi-card">
                <div class="kpi-label">Scenario CM</div>
                <div class="kpi-value" style="color:{badge_clr};">{calculated_cm}%</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        k3, k4 = st.columns(2)
        with k3:
            st.markdown(f"""<div class="kpi-card">
                <div class="kpi-label">Est. Revenue</div>
                <div class="kpi-value">Rp{revenue/1000:,.0f}rb</div>
            </div>""", unsafe_allow_html=True)
        with k4:
            badge_clr = "#DC2626" if margin_diff < 0 else "#166534"
            st.markdown(f"""<div class="kpi-card">
                <div class="kpi-label">Delta vs Baseline</div>
                <div class="kpi-value" style="color:{badge_clr};">{margin_diff} pt</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f"""<div class="ui-card">
        <h3 style="font-size:15px; color:#013AC9; margin-bottom:14px; font-weight:600;">Historical Benchmark</h3>
        <table class="custom-table">
            <tr><th>Campaign Type</th><th>Discount</th><th>ROAS</th><th>Repeat Purchase</th><th>Historical CM</th></tr>
            <tr><td>Double Date</td><td>24%</td><td>2.1x</td><td>18%</td><td><span class="badge badge-danger">Low (12.4%)</span></td></tr>
            <tr><td>Pay Day</td><td>9%</td><td>3x</td><td>27%</td><td><span class="badge badge-warning">Medium (18.1%)</span></td></tr>
            <tr><td>Website/CRM Bundle</td><td>11%</td><td>3.4x</td><td>34%</td><td><span class="badge badge-info">High (21.5%)</span></td></tr>
            <tr style="background:#EFF6FF; font-weight:600;">
                <td style="color:#013AC9;">Your Scenario</td>
                <td>{disc_val}%</td>
                <td>-</td>
                <td>-</td>
                <td><span class="badge {'badge-danger' if calculated_cm < base_cm else 'badge-info'}">{'Low' if calculated_cm < base_cm else 'Good'} ({calculated_cm}%)</span></td>
            </tr>
        </table>
    </div>""", unsafe_allow_html=True)

# -------------------------------------------------------------
# MODUL 6: SETTINGS
# -------------------------------------------------------------
else:
    render_header("Settings", "System configuration and data dictionary mapping")

    sync_status = "Active Syncing (Real-time)" if df_live is not None else "Connection Warning (Using Fallback)"
    status_color = "#166534" if df_live is not None else "#DC2626"

    st.markdown(f"""<div class="ui-card">
        <h3 style="font-size:15px; color:#013AC9; margin-bottom:14px; font-weight:600;">System Settings & Governance</h3>
        <p style="font-size:13px; color:#64748B;">Kelola integrasi data API, threshold alert stok, dan pemetaan data dictionary.</p>
        <hr style="border:none; border-top:1px solid #E2E8F0; margin:15px 0;">
        <div style="font-size:12px; color:#1E293B; line-height: 1.8;">
            <b>Connected Data Engine:</b> Google Sheets API (Live CSV Sync)<br>
            <b>Spreadsheet ID:</b> <code>1aiOOaoXg_Yo00xh-X5A29W3NlfAm0xWq5nNYB1a-co4</code><br>
            <b>Status:</b> <span style="color:{status_color}; font-weight:700;">{sync_status}</span>
        </div>
    </div>""", unsafe_allow_html=True)
