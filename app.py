import streamlit as st
import pandas as pd
from workforce_model import calculate_workforce

st.set_page_config(
    page_title="AI Enabled Workforce & Capacity Planning",
    page_icon="🚀",
    layout="wide"
)

# ===============================
# REGION GROWTH
# ===============================

st.sidebar.header("Region Growth")

region_parameters = {

    "North": {
        "BAU": st.sidebar.slider(
            "North BAU %",
            0, 100, 15,
            key="north_bau"
        ),
        "DC": st.sidebar.slider(
            "North DC %",
            0, 100, 10,
            key="north_dc"
        )
    },

    "West": {
        "BAU": st.sidebar.slider(
            "West BAU %",
            0, 100, 20,
            key="west_bau"
        ),
        "DC": st.sidebar.slider(
            "West DC %",
            0, 100, 40,
            key="west_dc"
        )
    },

    "South": {
        "BAU": st.sidebar.slider(
            "South BAU %",
            0, 100, 18,
            key="south_bau"
        ),
        "DC": st.sidebar.slider(
            "South DC %",
            0, 100, 35,
            key="south_dc"
        )
    },

    "East": {
        "BAU": st.sidebar.slider(
            "East BAU %",
            0, 100, 10,
            key="east_bau"
        ),
        "DC": st.sidebar.slider(
            "East DC %",
            0, 100, 5,
            key="east_dc"
        )
    }

}

# ===============================
# PRODUCTIVITY
# ===============================

st.sidebar.header("Productivity")

productive_hours = st.sidebar.slider(
    "Productive Hours/Day",
    4,
    10,
    7,
    key="productive"
)

working_days = st.sidebar.slider(
    "Working Days/Month",
    15,
    26,
    20,
    key="days"
)

target_utilization = st.sidebar.slider(
    "Utilization %",
    60,
    100,
    90,
    key="util"
)

# ===============================
# ATTRITION
# ===============================

st.sidebar.header("Product Attrition")

bu_parameters = {

    "UPS": {
        "Attrition": st.sidebar.slider(
            "UPS Attrition",
            0, 30, 8,
            key="ups"
        )
    },

    "Cooling": {
        "Attrition": st.sidebar.slider(
            "Cooling Attrition",
            0, 30, 8,
            key="cool"
        )
    },

    "Power Products": {
        "Attrition": st.sidebar.slider(
            "Power Products Attrition",
            0, 30, 8,
            key="pp"
        )
    },

    "Power System": {
        "Attrition": st.sidebar.slider(
            "Power System Attrition",
            0, 30, 8,
            key="ps"
        )
    },

    "Industrial Automation": {
        "Attrition": st.sidebar.slider(
            "Industrial Automation Attrition",
            0, 30, 8,
            key="ia"
        )
    }

}

# ===============================
# MAIN PAGE
# ===============================

st.title(
    "🚀 AI Enabled Workforce & Capacity Planning"
)

uploaded_file = st.file_uploader(
    "Upload workforce_input.csv",
    type=["csv"]
)

if uploaded_file:

    try:

        df = pd.read_csv(uploaded_file)

        result = calculate_workforce(
            df,
            bu_parameters,
            region_parameters,
            productive_hours,
            working_days,
            target_utilization
        )

        st.dataframe(result)

        st.subheader(
            "Product vs Region Hiring Matrix"
        )

        matrix = result.pivot_table(
            values="Additional Required",
            index="Product",
            columns="Region",
            fill_value=0,
            aggfunc="sum"
        )

        matrix["Total"] = matrix.sum(
            axis=1
        )

        matrix.loc["Total"] = matrix.sum(
            axis=0
        )

        st.dataframe(matrix)

    except Exception as e:

        st.error(
            f"Error : {e}"
        )

else:

    st.info(
        "Upload workforce_input.csv"
    )
