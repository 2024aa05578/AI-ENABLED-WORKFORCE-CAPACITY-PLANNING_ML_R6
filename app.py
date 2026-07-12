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
    0, 100, 15
)

north_dc = st.sidebar.slider(
    "North DC Growth %",
    0, 100, 10
)

st.sidebar.header("📈 West Region Growth")

west_bau = st.sidebar.slider(
    "West BAU Growth %",
    0, 100, 20
)

west_dc = st.sidebar.slider(
    "West DC Growth %",
    0, 100, 40
)

st.sidebar.header("📈 South Region Growth")

south_bau = st.sidebar.slider(
