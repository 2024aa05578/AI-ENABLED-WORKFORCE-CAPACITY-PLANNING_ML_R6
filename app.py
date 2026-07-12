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
# PRODUCT / BU ATTRITION
# =====================================================

st.sidebar.header("Product Wise Attrition")

bu_parameters = {}

bu_parameters["UPS"] = {
    "Attrition": st.sidebar.slider(
        "UPS Attrition %",
        0,
        30,
        8
    )
}

bu_parameters["Cooling"] = {
    "Attrition": st.sidebar.slider(
        "Cooling Attrition %",
        0,
        30,
        8
    )
}

bu_parameters["Power Products"] = {
    "Attrition": st.sidebar.slider(
        "Power Products Attrition %",
        0,
        30,
        8
    )
}

bu_parameters["Power System"] = {
    "Attrition": st.sidebar.slider(
        "Power System Attrition %",
        0,
        30,
        8
    )
}

bu_parameters["Industrial Automation"] = {
    "Attrition": st.sidebar.slider(
        "Industrial Automation Attrition %",
        0,
        30,
        8
    )
}

# =====================================================
# REGION WISE GROWTH
# =====================================================

st.sidebar.header("Region Wise Growth")

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
# PRODUCTIVITY PARAMETERS
# =====================================================

st.sidebar.header("Workforce Productivity")

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
# MAIN PAGE
# =====================================================

st.title("🚀 AI Enabled Workforce & Capacity Planning")

st.markdown("""
This solution forecasts workforce demand using:

- Breakdown Maintenance Work Orders
- Preventive Maintenance Work Orders
- Startup & Commissioning Work Orders
- Region-wise BAU Growth
- Region-wise Data Center Growth
- Product-wise Attrition
- Productivity & Utilization Factors
""")

# =====================================================
# FILE UPLOAD
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

    result = calculate_workforce(
        df,
        bu_parameters,
        region_parameters,
        productive_hours,
        working_days,
        target_utilization
    )

    st.subheader(
        "Workforce Planning Results"
    )

    st.dataframe(
        result,
        use_container_width=True
    )

    # KPI Section

    total_current = int(
        df["Current_SE"].sum()
    )

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

    # Product Chart

    st.subheader(
        "📦 Hiring Requirement by Product"
    )

    product_summary = (
        result.groupby("Product")
        ["Additional Required"]
        .sum()
    )

    st.bar_chart(product_summary)

    # Region Chart

    st.subheader(
        "🌍 Hiring Requirement by Region"
    )

    region_summary = (
        result.groupby("Region")
        ["Additional Required"]
        .sum()
    )

    st.bar_chart(region_summary)

    # Matrix

    st.subheader(
        "📊 Product vs Region Hiring Matrix"
    )

    matrix = result.pivot_table(
        values="Additional Required",
        index="Product",
        columns="Region",
        fill_value=0,
        aggfunc="sum"
    )

    st.dataframe(
        matrix,
        use_container_width=True
    )

else:

    st.info(
        "Please upload workforce_input.csv to start planning."
    )
