import streamlit as st
import pandas as pd
from workforce_model import calculate_workforce

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Enabled Workforce & Capacity Planning",
    page_icon="🚀",
    layout="wide"
)

# =====================================================
# BU PARAMETERS
# =====================================================

st.sidebar.title("BU Wise Planning Parameters")

bu_parameters = {}

# UPS
with st.sidebar.expander("UPS", expanded=True):
    bu_parameters["UPS"] = {
        "BAU": st.slider("UPS BAU Growth %", 0, 100, 25, key="ups_bau"),
        "DC": st.slider("UPS DC Growth %", 0, 100, 40, key="ups_dc"),
        "Attrition": st.slider("UPS Attrition %", 0, 30, 8, key="ups_attr")
    }

# Cooling
with st.sidebar.expander("Cooling"):
    bu_parameters["Cooling"] = {
        "BAU": st.slider("Cooling BAU Growth %", 0, 100, 20, key="cool_bau"),
        "DC": st.slider("Cooling DC Growth %", 0, 100, 50, key="cool_dc"),
        "Attrition": st.slider("Cooling Attrition %", 0, 30, 8, key="cool_attr")
    }

# Power Products
with st.sidebar.expander("Power Products"):
    bu_parameters["Power Products"] = {
