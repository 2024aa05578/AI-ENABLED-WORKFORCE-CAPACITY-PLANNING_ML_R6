import streamlit as st
import pandas as pd
from workforce_model import calculate_workforce

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI Enabled Workforce & Capacity Planning",
    page_icon="🚀",
    layout="wide"
)

# =====================================================
# REGION GROWTH
# =====================================================

st.sidebar.header("📈 North Region Growth")

north_bau = st.sidebar.slider(
    "North BAU Growth %",
    0, 100, 15,
    key="north_bau"
)

north_dc = st.sidebar.slider(
    "North DC Growth %",
    0, 100, 10,
    key="north_dc"
)

st.sidebar.header("📈 West Region Growth")

west_bau = st.sidebar.slider(
    "West BAU Growth %",
    0, 100, 20,
    key="west_bau"
)

west_dc = st.sidebar.slider(
    "West DC Growth %",
    0, 100, 40,
    key="west_dc"
)

st.sidebar.header("📈 South Region Growth")

south_bau = st.sidebar.slider(
    "South BAU Growth %",
    0, 100, 18,
    key="south_bau"
)

south_dc = st.sidebar.slider(
    "South DC Growth %",
    0, 100, 35,
    key="south_dc"
)

st.sidebar.header("📈 East Region Growth")

east_bau = st.sidebar.slider(
    "East BAU Growth %",
    0, 100, 10,
    key="east_bau"
)

east_dc = st.sidebar.slider(
    "East DC Growth %",
    0, 100, 5,
    key="east_dc"
)

region_parameters = {
    "North": {
        "BAU": north_bau,
        "DC": north_dc
    },
    "West": {
        "BAU": west_bau,
        "DC": west_dc
    },
    "South": {
        "BAU": south_bau,
        "DC": south_dc
    },
    "East": {
        "BAU": east_bau,
        "DC": east_dc
    }
}

# =====================================================
# PRODUCTIVITY
# =====================================================

st.sidebar.header("⚙ Workforce Productivity")

productive_hours = st.sidebar.slider(
    "Productive Hours Per Day",
    4, 10, 7,
    key="productive_hours"
)

working_days = st.sidebar.slider(
    "Working Days Per Month",
    15, 26, 20,
    key="working_days"
)

target_utilization = st.sidebar.slider(
    "Target Utilization %",
    60, 100, 90,
    key="utilization"
)

# =====================================================
# ATTRITION
# =====================================================

st.sidebar.header("👥 Product Wise Attrition")

bu_parameters = {
    "UPS": {
        "Attrition": st.sidebar.slider(
            "UPS Attrition %",
            0, 30, 8,
            key="ups_attr"
        )
    },

    "Cooling": {
