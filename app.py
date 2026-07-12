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

st.sidebar.header("📈 Region Wise Growth")

north_bau = st.sidebar.slider(
    "North BAU Growth %",
    0, 100, 15,
    key="north_bau"
)

north_dc = st.sidebar.slider(
    "North DC Growth %",
    0, 100, 10,
    key="north_dc"
)

west_bau = st.sidebar.slider(
    "West BAU Growth %",
    0, 100, 20,
    key="west_bau"
)

west_dc = st.sidebar.slider(
    "West DC Growth %",
    0, 100, 40,
    key="west_dc"
)

south_bau = st.sidebar.slider(
    "South BAU Growth %",
    0, 100, 18,
    key="south_bau"
)

south_dc = st.sidebar.slider(
    "South DC Growth %",
    0, 100, 35,
    key="south_dc"
)

east_bau = st.sidebar.slider(
    "East BAU Growth %",
    0, 100, 10,
    key="east_bau"
)

east_dc = st.sidebar.slider(
    "East DC Growth %",
    0, 100, 5,
    key="east_dc"
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

# =====================================================
# PRODUCTIVITY
# =====================================================

st.sidebar.header("⚙ Workforce Productivity")

productive_hours = st.sidebar.slider(
    "Productive Hours Per Day",
    4,
    10,
    7,
    key="productive_hours"
)

working_days = st.sidebar.slider(
    "Working Days Per Month",
    15,
    26,
    20,
    key="working_days"
)

target_utilization = st.sidebar.slider(
    "Target Utilization %",
    60,
    100,
    90,
    key="target_utilization"
)

# =====================================================
# PRODUCT WISE ATTRITION
# =====================================================

st.sidebar.header("👥 Product Wise Attrition")

bu_parameters = {
    "UPS": {
        "Attrition": st.sidebar.slider(
            "UPS Attrition %",
            0, 30, 8,
            key="ups_attr"
        )
    },

    "Cooling": {
        "Attrition": st.sidebar.slider(
            "Cooling Attrition %",
            0, 30, 8,
            key="cool_attr"
        )
    },

    "Power Products": {
        "Attrition": st.sidebar.slider(
            "Power Products Attrition %",
            0, 30, 8,
            key="pp_attr"
        )
    },

    "Power System": {
        "Attrition": st.sidebar.slider(
            "Power System Attrition %",
            0, 30, 8,
            key="ps_attr"
        )
    },

    "Industrial Automation": {
        "Attrition": st.sidebar.slider(
            "Industrial Automation Attrition %",
            0, 30, 8,
            key="ia_attr"
        )
    }
}

# =====================================================
# MAIN PAGE
# =====================================================

st.title("🚀 AI Enabled Workforce & Capacity Planning")

st.markdown("""
### Workforce Planning Dashboard

This solution estimates workforce demand using:

- Region Wise BAU Growth
- Region Wise Data Center Growth
- Product Wise Attrition
- Productivity
- Utilization
""")

uploaded_file = st.file_uploader(
    "Upload workforce_input.csv",
    type=["csv"]
)

if uploaded_file is not None:

    try:

        df = pd.read_csv(uploaded_file)

        st.subheader("📂 Input Data")

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
            "📊 Workforce Planning Results"
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

        matrix["Total"] = matrix.sum(axis=1)

        matrix.loc["Total"] = matrix.sum(axis=0)

        st.dataframe(
            matrix,
            use_container_width=True
        )

    except Exception as e:

        st.error(f"Application Error: {e}")

else:

    st.info(
        "Please upload workforce_input.csv to continue."
    )
