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
# BU PARAMETERS
# =====================================================

st.sidebar.title("BU Wise Planning Parameters")

bu_parameters = {}

with st.sidebar.expander("UPS", expanded=True):
    bu_parameters["UPS"] = {
        "BAU": st.slider("UPS BAU Growth %", 0, 100, 25),
        "DC": st.slider("UPS DC Growth %", 0, 100, 40),
        "Attrition": st.slider("UPS Attrition %", 0, 30, 8)
    }

with st.sidebar.expander("Cooling"):
    bu_parameters["Cooling"] = {
        "BAU": st.slider("Cooling BAU Growth %", 0, 100, 20),
        "DC": st.slider("Cooling DC Growth %", 0, 100, 50),
        "Attrition": st.slider("Cooling Attrition %", 0, 30, 8)
    }

with st.sidebar.expander("Power Products"):
    bu_parameters["Power Products"] = {
        "BAU": st.slider("Power Products BAU Growth %", 0, 100, 15),
        "DC": st.slider("Power Products DC Growth %", 0, 100, 10),
        "Attrition": st.slider("Power Products Attrition %", 0, 30, 8)
    }

with st.sidebar.expander("Power System"):
    bu_parameters["Power System"] = {
        "BAU": st.slider("Power System BAU Growth %", 0, 100, 18),
        "DC": st.slider("Power System DC Growth %", 0, 100, 20),
        "Attrition": st.slider("Power System Attrition %", 0, 30, 8)
    }

with st.sidebar.expander("Industrial Automation"):
    bu_parameters["Industrial Automation"] = {
        "BAU": st.slider("Industrial Automation BAU Growth %", 0, 100, 12),
        "DC": st.slider("Industrial Automation DC Growth %", 0, 100, 5),
        "Attrition": st.slider("Industrial Automation Attrition %", 0, 30, 8)
    }

# =====================================================
# REGION DC GROWTH
# =====================================================

st.sidebar.title("Region Wise DC Growth")

region_dc_growth = {}

region_dc_growth["North"] = st.sidebar.slider(
    "North DC Growth %",
    0,
    100,
    10
)

region_dc_growth["West"] = st.sidebar.slider(
    "West DC Growth %",
    0,
    100,
    40
)

region_dc_growth["South"] = st.sidebar.slider(
    "South DC Growth %",
    0,
    100,
    35
)

region_dc_growth["East"] = st.sidebar.slider(
    "East DC Growth %",
    0,
    100,
    5
)

# =====================================================
# PRODUCTIVITY
# =====================================================

st.sidebar.title("Workforce Productivity")

productive_hours = st.sidebar.slider(
    "Productive Hours Per Day",
    4,
    10,
    7
)

working_days = st.sidebar.slider(
    "Working Days Per Month",
    15,
    26,
    20
)

target_utilization = st.sidebar.slider(
    "Target Engineer Utilization %",
    60,
    100,
    90
)

# =====================================================
# MAIN
# =====================================================

st.title("🚀 AI Enabled Workforce & Capacity Planning")

uploaded_file = st.file_uploader(
    "Upload workforce_input.csv",
    type=["csv"]
)

