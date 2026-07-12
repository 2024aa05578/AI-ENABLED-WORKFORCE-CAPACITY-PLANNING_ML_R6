import streamlit as st
import pandas as pd

from workforce_model import calculate_workforce
from ml_forecast import forecast_work_orders

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI Enabled Workforce & Capacity Planning",
    page_icon="🚀",
    layout="wide"
)

# =====================================================
# SIDEBAR PARAMETERS
# =====================================================

st.sidebar.title("BU Wise Planning Parameters")

bu_parameters = {}

# UPS

with st.sidebar.expander("UPS", expanded=True):

    bu_parameters["UPS"] = {
        "BAU": st.slider(
            "UPS BAU Growth %",
            0, 100, 25,
            key="ups_bau"
        ),
        "DC": st.slider(
            "UPS Data Center Growth %",
            0, 100, 40,
            key="ups_dc"
        ),
        "Attrition": st.slider(
            "UPS Attrition %",
            0, 30, 8,
            key="ups_attr"
        )
    }

# Cooling

with st.sidebar.expander("Cooling"):

    bu_parameters["Cooling"] = {
        "BAU": st.slider(
            "Cooling BAU Growth %",
            0, 100, 20,
            key="cool_bau"
        ),
        "DC": st.slider(
            "Cooling Data Center Growth %",
            0, 100, 50,
            key="cool_dc"
        ),
        "Attrition": st.slider(
            "Cooling Attrition %",
            0, 30, 8,
            key="cool_attr"
        )
    }

# Power Products

with st.sidebar.expander("Power Products"):

    bu_parameters["Power Products"] = {
        "BAU": st.slider(
            "Power Products BAU Growth %",
            0, 100, 15,
            key="pp_bau"
        ),
        "DC": st.slider(
            "Power Products DC Growth %",
            0, 100, 10,
            key="pp_dc"
        ),
        "Attrition": st.slider(
            "Power Products Attrition %",
            0, 30, 8,
            key="pp_attr"
        )
    }

# Power System

with st.sidebar.expander("Power System"):

    bu_parameters["Power System"] = {
        "BAU": st.slider(
            "Power System BAU Growth %",
            0, 100, 18,
            key="ps_bau"
        ),
        "DC": st.slider(
            "Power System DC Growth %",
            0, 100, 20,
            key="ps_dc"
        ),
        "Attrition": st.slider(
            "Power System Attrition %",
            0, 30, 8,
            key="ps_attr"
        )
    }

# Industrial Automation

with st.sidebar.expander("Industrial Automation"):

    bu_parameters["Industrial Automation"] = {
        "BAU": st.slider(
            "Industrial Automation BAU Growth %",
            0, 100, 12,
            key="ia_bau"
        ),
        "DC": st.slider(
            "Industrial Automation DC Growth %",
            0, 100, 5,
            key="ia_dc"
        ),
        "Attrition": st.slider(
            "Industrial Automation Attrition %",
            0, 30, 8,
            key="ia_attr"
        )
    }

# =====================================================
# PRODUCTIVITY PARAMETERS
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
# MAIN HEADER
# =====================================================

st.title("🚀 AI Enabled Workforce & Capacity Planning")

st.markdown("""
This solution forecasts manpower demand using:

- Installed Base
- Breakdown Work Orders
- PM Work Orders
- Startup Work Orders
- BAU Growth
- Data Center Growth
- Attrition
- Productivity
- Utilization
- Machine Learning Based Forecasting
""")

# =====================================================
# SECTION 1
# WORKFORCE INPUT
# =====================================================

st.header("📂 Step 1 - Upload Workforce Data")

workforce_file = st.file_uploader(
    "Upload workforce_input.csv",
    type=["csv"]
)

if workforce_file is not None:

    df = pd.read_csv(workforce_file)

    st.subheader("Workforce Input Data")

    st.dataframe(
        df,
        use_container_width=True
    )

    result = calculate_workforce(
        df,
        bu_parameters,
        productive_hours,
        working_days,
        target_utilization
    )

    st.subheader("Workforce Planning Results")

    st.dataframe(
        result,
        use_container_width=True
    )

    # KPI SECTION

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
        total_current
    )

    c2.metric(
        "Available After Attrition",
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

    # BU Chart

    st.subheader("📦 Hiring Requirement by Business Unit")

    product_summary = (
        result.groupby("Product")
        ["Additional Required"]
        .sum()
    )

    st.bar_chart(product_summary)

    # Region Chart

    st.subheader("🌍 Hiring Requirement by Region")

    region_summary = (
        result.groupby("Region")
        ["Additional Required"]
        .sum()
    )

    st.bar_chart(region_summary)

    # Matrix

    st.subheader("📊 Product vs Region Matrix")

    pivot = result.pivot_table(
        values="Additional Required",
        index="Product",
        columns="Region",
        aggfunc="sum",
        fill_value=0
    )

    st.dataframe(
        pivot,
        use_container_width=True
    )

# =====================================================
# SECTION 2
# ML FORECAST
# =====================================================

st.header("📈 Step 2 - ML Forecast")

historical_file = st.file_uploader(
    "Upload historical_workload.csv",
    type=["csv"],
    key="historical_file"
)

if historical_file is not None:

    historical_df = pd.read_csv(
        historical_file
    )

    st.subheader("Historical Data")

    st.dataframe(
        historical_df,
        use_container_width=True
    )

    selected_product = st.selectbox(
        "Select Product",
        historical_df["Product"].unique()
    )

    forecast_df = forecast_work_orders(
        historical_df,
        selected_product
    )

    st.subheader(
        f"Future Forecast for {selected_product}"
    )

    st.dataframe(
        forecast_df,
        use_container_width=True
    )

else:

    st.info(
        "Upload historical_workload.csv to run Machine Learning forecasting."
    )
