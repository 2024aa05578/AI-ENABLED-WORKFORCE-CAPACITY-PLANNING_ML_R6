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
# BU ATTRITION
# =====================================================

st.sidebar.title("BU Wise Attrition")

bu_parameters = {}

for product in [
    "UPS",
    "Cooling",
    "Power Products",
    "Power System",
    "Industrial Automation"
]:

    bu_parameters[product] = {
        "Attrition": st.sidebar.slider(
            f"{product} Attrition %",
            0,
            30,
            8
        )
    }

# =====================================================
# REGION GROWTH
# =====================================================

st.sidebar.title("Region Wise Growth")

region_parameters = {}

region_parameters["North"] = {
    "BAU": st.sidebar.slider(
        "North BAU Growth %",
        0,
        100,
        15
    ),
    "DC": st.sidebar.slider(
        "North DC Growth %",
        0,
        100,
        10
    )
}

region_parameters["West"] = {
    "BAU": st.sidebar.slider(
        "West BAU Growth %",
        0,
        100,
        20
    ),
    "DC": st.sidebar.slider(
        "West DC Growth %",
        0,
        100,
        40
    )
}

region_parameters["South"] = {
    "BAU": st.sidebar.slider(
        "South BAU Growth %",
        0,
        100,
        18
    ),
    "DC": st.sidebar.slider(
        "South DC Growth %",
        0,
        100,
        35
    )
}

region_parameters["East"] = {
    "BAU": st.sidebar.slider(
        "East BAU Growth %",
        0,
        100,
        10
    ),
    "DC": st.sidebar.slider(
        "East DC Growth %",
        0,
        100,
        5
    )
}

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
    "Target Utilization %",
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

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.subheader("Input Data")
    st.dataframe(df)

    result = calculate_workforce(
        df,
        bu_parameters,
        region_parameters,
        productive_hours,
        working_days,
        target_utilization
