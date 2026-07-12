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
# REGION WISE GROWTH
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
