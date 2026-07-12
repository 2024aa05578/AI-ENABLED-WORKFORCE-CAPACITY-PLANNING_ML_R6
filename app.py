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

with st.sidebar.expander("UPS", expanded=True):
    bu_parameters["UPS"] = {
        "BAU": st.slider("UPS BAU Growth %", 0, 100, 25),
        "Attrition": st.slider("UPS Attrition %", 0, 30, 8)
    }

with st.sidebar.expander("Cooling"):
    bu_parameters["Cooling"] = {
        "BAU": st.slider("Cooling BAU Growth %", 0, 100, 20),
        "Attrition": st.slider("Cooling Attrition %", 0, 30, 8)
    }

with st.sidebar.expander("Power Products"):
    bu_parameters["Power Products"] = {
        "BAU": st.slider("Power Products BAU Growth %", 0, 100, 15),
        "Attrition": st.slider("Power Products Attrition %", 0, 30, 8)
    }

with st.sidebar.expander("Power System"):
    bu_parameters["Power System"] = {
        "BAU": st.slider("Power System BAU Growth %", 0, 100, 18),
        "Attrition": st.slider("Power System Attrition %", 0, 30, 8)
    }

with st.sidebar.expander("Industrial Automation"):
    bu_parameters["Industrial Automation"] = {
        "BAU": st.slider("Industrial Automation BAU Growth %", 0, 100, 12),
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
# MAIN PAGE
# =====================================================

st.title("🚀 AI Enabled Workforce & Capacity Planning")

st.markdown("""
Forecast workforce demand using:

- Breakdown Work Orders
- PM Work Orders
- Startup Work Orders
- BU-wise BAU Growth
- Region-wise Data Center Growth
- Attrition
- Productivity
- Utilization
""")

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
        region_dc_growth,
        productive_hours,
        working_days,
        target_utilization
    )

    st.subheader("Workforce Planning Results")
    st.dataframe(result)

    total_current = df["Current_SE"].sum()

    total_available = round(
        result["Available Engineers"].sum(),
        1
    )

    total_required = round(
        result["Required Engineers"].sum(),
        1
    )

    total_hiring = int(
        result["Additional Required"].sum()
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Current Engineers",
        int(total_current)
    )

    c2.metric(
        "Available Engineers",
        total_available
    )

    c3.metric(
        "Required Engineers",
        total_required
    )

    c4.metric(
        "Hiring Gap",
        total_hiring
    )

    st.subheader("📦 Hiring Requirement by BU")

    st.bar_chart(
        result.groupby("Product")[
            "Additional Required"
        ].sum()
    )

    st.subheader("🌍 Hiring Requirement by Region")

    st.bar_chart(
        result.groupby("Region")[
            "Additional Required"
        ].sum()
    )

    st.subheader(
        "📊 Product vs Region Matrix"
    )

    matrix = result.pivot_table(
        values="Additional Required",
        index="Product",
        columns="Region",
        fill_value=0,
        aggfunc="sum"
    )

    st.dataframe(matrix)

else:

    st.info(
        "Upload workforce_input.csv"
    )
