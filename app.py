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
# REGIONAL DATA CENTER GROWTH PARAMETERS
# =====================================================

st.sidebar.title("Regional Data Center Growth")

regional_dc_growth = {}

with st.sidebar.expander("Regional DC Growth %", expanded=True):
    regional_dc_growth["North"] = st.slider(
        "North DC Growth %",
        min_value=0,
        max_value=100,
        value=25,
        key="north_dc"
    )

    regional_dc_growth["South"] = st.slider(
        "South DC Growth %",
        min_value=0,
        max_value=100,
        value=40,
        key="south_dc"
    )

    regional_dc_growth["East"] = st.slider(
        "East DC Growth %",
        min_value=0,
        max_value=100,
        value=15,
        key="east_dc"
    )

    regional_dc_growth["West"] = st.slider(
        "West DC Growth %",
        min_value=0,
        max_value=100,
        value=35,
        key="west_dc"
    )


# =====================================================
# BU WISE PARAMETERS
# =====================================================

st.sidebar.title("BU Wise Planning Parameters")

dc_action_options = [
    "Add Regional DC Growth",
    "Do Not Add Regional DC Growth",
    "Delete Regional DC Growth"
]

bu_parameters = {}


# =====================================================
# UPS
# =====================================================

with st.sidebar.expander("UPS", expanded=True):
    bu_parameters["UPS"] = {
        "BAU": st.slider(
            "UPS BAU Growth %",
            min_value=0,
            max_value=100,
            value=25,
            key="ups_bau"
        ),
        "Attrition": st.slider(
            "UPS Attrition %",
            min_value=0,
            max_value=30,
            value=8,
            key="ups_attr"
        ),
        "DC_Action": st.selectbox(
            "UPS Regional DC Treatment",
            dc_action_options,
            index=0,
            key="ups_dc_action"
        )
    }


# =====================================================
# COOLING
# =====================================================

with st.sidebar.expander("Cooling"):
    bu_parameters["Cooling"] = {
        "BAU": st.slider(
            "Cooling BAU Growth %",
            min_value=0,
            max_value=100,
            value=20,
            key="cool_bau"
        ),
        "Attrition": st.slider(
            "Cooling Attrition %",
            min_value=0,
            max_value=30,
            value=8,
            key="cool_attr"
        ),
        "DC_Action": st.selectbox(
            "Cooling Regional DC Treatment",
            dc_action_options,
            index=0,
            key="cool_dc_action"
        )
    }


# =====================================================
# POWER PRODUCTS
# =====================================================

with st.sidebar.expander("Power Products"):
    bu_parameters["Power Products"] = {
        "BAU": st.slider(
            "Power Products BAU Growth %",
            min_value=0,
            max_value=100,
            value=15,
            key="pp_bau"
        ),
        "Attrition": st.slider(
            "Power Products Attrition %",
            min_value=0,
            max_value=30,
            value=8,
            key="pp_attr"
        ),
        "DC_Action": st.selectbox(
            "Power Products Regional DC Treatment",
            dc_action_options,
            index=1,
            key="pp_dc_action"
        )
    }


# =====================================================
# POWER SYSTEM
# =====================================================

with st.sidebar.expander("Power System"):
    bu_parameters["Power System"] = {
        "BAU": st.slider(
            "Power System BAU Growth %",
            min_value=0,
            max_value=100,
            value=18,
            key="ps_bau"
        ),
        "Attrition": st.slider(
            "Power System Attrition %",
            min_value=0,
            max_value=30,
            value=8,
            key="ps_attr"
        ),
        "DC_Action": st.selectbox(
            "Power System Regional DC Treatment",
            dc_action_options,
            index=0,
            key="ps_dc_action"
        )
    }


# =====================================================
# INDUSTRIAL AUTOMATION
# =====================================================

with st.sidebar.expander("Industrial Automation"):
    bu_parameters["Industrial Automation"] = {
        "BAU": st.slider(
            "Industrial Automation BAU Growth %",
            min_value=0,
            max_value=100,
            value=12,
            key="ia_bau"
        ),
        "Attrition": st.slider(
            "Industrial Automation Attrition %",
            min_value=0,
            max_value=30,
            value=8,
            key="ia_attr"
        ),
        "DC_Action": st.selectbox(
            "Industrial Automation Regional DC Treatment",
            dc_action_options,
            index=1,
            key="ia_dc_action"
        )
    }


# =====================================================
# WORKFORCE PRODUCTIVITY PARAMETERS
# =====================================================

st.sidebar.title("Workforce Productivity")

productive_hours = st.sidebar.slider(
    "Productive Hours Per Day",
    min_value=4,
    max_value=10,
    value=7
)

working_days = st.sidebar.slider(
    "Working Days Per Month",
    min_value=15,
    max_value=26,
    value=20
)

target_utilization = st.sidebar.slider(
    "Target Engineer Utilization %",
    min_value=60,
    max_value=100,
    value=90
)


# =====================================================
# MAIN PAGE
# =====================================================

st.title("🚀 AI Enabled Workforce & Capacity Planning")

st.write(
    """
    This application estimates service engineer requirements based on:

    - Current service engineer count
    - Breakdown, preventive maintenance and startup work orders
    - Average hours per work order type
    - BU-wise BAU growth
    - Region-wise Data Center growth
    - BU-wise option to add, ignore, or delete regional DC growth
    - Attrition
    - Engineer productivity assumptions
    """
)


uploaded_file = st.file_uploader(
    "Upload workforce_input.csv",
    type=["csv"]
)


if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    required_columns = [
        "Region",
        "Product",
        "Current_SE",
        "Breakdown_WO",
        "Breakdown_Hrs",
        "PM_WO",
        "PM_Hrs",
        "Startup_WO",
        "Startup_Hrs"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        st.error(f"Missing required columns: {missing_columns}")
        st.stop()

    st.subheader("Input Data")
    st.dataframe(df, use_container_width=True)

    result = calculate_workforce(
        df,
        bu_parameters,
        regional_dc_growth,
        productive_hours,
        working_days,
        target_utilization
    )

    st.subheader("Workforce Planning Results")
    st.dataframe(result, use_container_width=True)

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

    c1.metric("Current SE", total_current)
    c2.metric("Available After Attrition", total_available)
    c3.metric("Required SE", total_required)
    c4.metric("Hiring Gap", total_hiring)
    c5.metric("Hrs/Day", productive_hours)
    c6.metric("Days/Month", working_days)
    c7.metric("Utilization %", target_utilization)

    st.subheader("📦 Hiring by Product Line")

    hiring_by_product = result.groupby("Product")["Additional Required"].sum()

    st.bar_chart(hiring_by_product)

    st.subheader("🌍 Hiring by Region")

    hiring_by_region = result.groupby("Region")["Additional Required"].sum()

    st.bar_chart(hiring_by_region)

    st.subheader("🏢 Applied DC Growth by Product and Region")

    dc_matrix = result.pivot_table(
        values="Applied DC Growth %",
        index="Product",
        columns="Region",
        fill_value=0,
        aggfunc="mean"
    )

    st.dataframe(dc_matrix, use_container_width=True)

    st.subheader("📊 Product vs Region Hiring Matrix")

    hiring_matrix = result.pivot_table(
        values="Additional Required",
        index="Product",
        columns="Region",
        fill_value=0,
        aggfunc="sum"
    )

    st.dataframe(hiring_matrix, use_container_width=True)

    st.subheader("📈 Total Growth by Product and Region")

    growth_matrix = result.pivot_table(
        values="Total Growth %",
        index="Product",
        columns="Region",
        fill_value=0,
        aggfunc="mean"
    )

    st.dataframe(growth_matrix, use_container_width=True)

    csv_output = result.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Workforce Planning Output",
        data=csv_output,
        file_name="workforce_planning_output.csv",
        mime="text/csv"
    )

else:
    st.info("Please upload workforce_input.csv to start workforce planning.")
