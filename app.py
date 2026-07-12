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
# SIDEBAR
# =====================================================

st.sidebar.title("BU Wise Planning Parameters")

bu_parameters = {}

# UPS

with st.sidebar.expander("UPS", expanded=True):

    bu_parameters["UPS"] = {

        "BAU": st.slider(
            "UPS BAU Growth %",
            0,
            100,
            25,
            key="ups_bau"
        ),

        "DC": st.slider(
            "UPS Data Center Surge %",
            0,
            100,
            40,
            key="ups_dc"
        ),

        "Attrition": st.slider(
            "UPS Attrition %",
            0,
            30,
            8,
            key="ups_attr"
        )
    }

# Cooling

with st.sidebar.expander("Cooling"):

    bu_parameters["Cooling"] = {

        "BAU": st.slider(
            "Cooling BAU Growth %",
            0,
            100,
            20,
            key="cool_bau"
        ),

        "DC": st.slider(
            "Cooling Data Center Surge %",
            0,
            100,
            50,
            key="cool_dc"
        ),

        "Attrition": st.slider(
            "Cooling Attrition %",
            0,
            30,
            8,
            key="cool_attr"
        )
    }

# Power Products

with st.sidebar.expander("Power Products"):

    bu_parameters["Power Products"] = {

        "BAU": st.slider(
            "Power Products BAU Growth %",
            0,
            100,
            15,
            key="pp_bau"
        ),

        "DC": st.slider(
            "Power Products DC Growth %",
            0,
            100,
            10,
            key="pp_dc"
        ),

        "Attrition": st.slider(
            "Power Products Attrition %",
            0,
            30,
            8,
            key="pp_attr"
        )
    }

# Power System

with st.sidebar.expander("Power System"):

    bu_parameters["Power System"] = {

        "BAU": st.slider(
            "Power System BAU Growth %",
            0,
            100,
            18,
            key="ps_bau"
        ),

        "DC": st.slider(
            "Power System DC Growth %",
            0,
            100,
            20,
            key="ps_dc"
        ),

        "Attrition": st.slider(
            "Power System Attrition %",
            0,
            30,
            8,
            key="ps_attr"
        )
    }

# Industrial Automation

with st.sidebar.expander("Industrial Automation"):

    bu_parameters["Industrial Automation"] = {

        "BAU": st.slider(
            "Industrial Automation BAU Growth %",
            0,
            100,
            12,
            key="ia_bau"
        ),

        "DC": st.slider(
            "Industrial Automation DC Growth %",
            0,
            100,
            5,
            key="ia_dc"
        ),

        "Attrition": st.slider(
            "Industrial Automation Attrition %",
            0,
            30,
            8,
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
# MAIN PAGE
# =====================================================

st.title("🚀 AI Enabled Workforce & Capacity Planning")

st.markdown("""
This solution forecasts workforce requirements using:

- Installed Base
- Breakdown Work Orders
- PM Work Orders
- Startup Work Orders
- BAU Growth
- Data Center Growth
- Attrition
- Engineer Productivity
- Engineer Utilization
- Machine Learning Forecasting
""")

# =====================================================
# LOAD WORKFORCE DATA
# =====================================================

uploaded_file = st.file_uploader(
    "Upload workforce_input.csv",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.subheader("Input Data")

    st.dataframe(
        df,
        use_container_width=True
    )

    # =====================================================
    # WORKFORCE CALCULATION
    # =====================================================

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

    # =====================================================
    # KPI SECTION
    # =====================================================

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

    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)

    c1.metric(
        "Current SE",
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

    c5.metric(
        "Hrs/Day",
        productive_hours
    )

    c6.metric(
        "Days/Month",
        working_days
    )

    c7.metric(
        "Utilization %",
        target_utilization
    )

    # =====================================================
    # HIRING BY BU
    # =====================================================

    st.subheader("📦 Hiring Requirement by Business Unit")

    product_summary = (
        result.groupby("Product")
        ["Additional Required"]
        .sum()
    )

    st.bar_chart(product_summary)

    # =====================================================
    # HIRING BY REGION
    # =====================================================

    st.subheader("🌍 Hiring Requirement by Region")

    region_summary = (
        result.groupby("Region")
        ["Additional Required"]
        .sum()
    )

    st.bar_chart(region_summary)

    # =====================================================
    # PRODUCT REGION MATRIX
    # =====================================================

    st.subheader("📊 Product vs Region Hiring Matrix")

    matrix = result.pivot_table(
        values="Additional Required",
        index="Product",
        columns="Region",
        aggfunc="sum",
        fill_value=0
    )

    st.dataframe(
        matrix,
        use_container_width=True
    )

    # =====================================================
    # MACHINE LEARNING FORECAST
    # =====================================================

    st.subheader("📈 Machine Learning Forecast")

    try:

        historical_df = pd.read_csv(
            "data/historical_workload.csv"
        )

        selected_product = st.selectbox(
            "Select Product",
            historical_df["Product"].unique()
        )

        forecast_df = forecast_work_orders(
            historical_df,
            selected_product
        )

        st.dataframe(
            forecast_df,
            use_container_width=True
        )

    except Exception as e:

        st.warning(
            "historical_workload.csv not found. "
            "ML forecast section skipped."
        )

        st.text(str(e))

else:

    st.info(
        "Upload workforce_input.csv to start planning."
    )
