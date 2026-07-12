import streamlit as st
import pandas as pd
from workforce_model import calculate_workforce

# -----------------------------------------------------
# Page Configuration
# -----------------------------------------------------

st.set_page_config(
    page_title="AI Enabled Workforce & Capacity Planning",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------------------------------
# Region Growth Parameters
# -----------------------------------------------------

st.sidebar.header("North Region Growth")

north_bau = st.sidebar.slider(
    "North BAU Growth %",
    0, 100, 15
)

north_dc = st.sidebar.slider(
    "North DC Growth %",
    0, 100, 10
)

st.sidebar.header("West Region Growth")

west_bau = st.sidebar.slider(
    "West BAU Growth %",
    0, 100, 20
)

west_dc = st.sidebar.slider(
    "West DC Growth %",
    0, 100, 40
)

st.sidebar.header("South Region Growth")

south_bau = st.sidebar.slider(
    "South BAU Growth %",
    0, 100, 18
)

south_dc = st.sidebar.slider(
    "South DC Growth %",
    0, 100, 35
)

st.sidebar.header("East Region Growth")

east_bau = st.sidebar.slider(
    "East BAU Growth %",
    0, 100, 10
)

east_dc = st.sidebar.slider(
    "East DC Growth %",
    0, 100, 5
)

region_parameters = {
    "North": {
        "BAU": north_bau,
        "DC": north_dc
    },
    "West": {
        "BAU": west_bau,
        "DC": west_dc
    },
    "South": {
        "BAU": south_bau,
        "DC": south_dc
    },
    "East": {
        "BAU": east_bau,
        "DC": east_dc
    }
}

# -----------------------------------------------------
# Productivity
# -----------------------------------------------------

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

# -----------------------------------------------------
# Attrition
# -----------------------------------------------------

st.sidebar.header("Product Wise Attrition")

bu_parameters = {
    "UPS": {
        "Attrition": st.sidebar.slider(
            "UPS Attrition %",
            0,
            30,
            8
        )
    },

    "Cooling": {
        "Attrition": st.sidebar.slider(
            "Cooling Attrition %",
            0,
            30,
            8
        )
    },

    "Power Products": {
        "Attrition": st.sidebar.slider(
            "Power Products Attrition %",
            0,
            30,
            8
        )
    },

    "Power System": {
        "Attrition": st.sidebar.slider(
            "Power System Attrition %",
            0,
            30,
            8
        )
    },

    "Industrial Automation": {
        "Attrition": st.sidebar.slider(
            "Industrial Automation Attrition %",
            0,
            30,
            8
        )
    }
}

# -----------------------------------------------------
# Main Page
# -----------------------------------------------------

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
    )

    st.subheader("Workforce Planning Results")
    st.dataframe(result)

    total_current = int(df["Current_SE"].sum())

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

    st.subheader("📦 Hiring Requirement by Product")

    product_summary = (
        result.groupby("Product")
        ["Additional Required"]
        .sum()
    )

    st.bar_chart(product_summary)

    st.subheader("🌍 Hiring Requirement by Region")

    region_summary = (
        result.groupby("Region")
        ["Additional Required"]
        .sum()
    )

    st.bar_chart(region_summary)

    st.subheader("📊 Product vs Region Hiring Matrix")

    matrix = result.pivot_table(
        values="Additional Required",
        index="Product",
        columns="Region",
        aggfunc="sum",
        fill_value=0
    )

    matrix["Total"] = matrix.sum(axis=1)

    matrix.loc["Total"] = matrix.sum(axis=0)

    st.dataframe(matrix)

else:

    st.info(
        "Please upload workforce_input.csv"
    )
