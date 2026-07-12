import pandas as pd
import math


def calculate_workforce(
    df,
    bu_parameters,
    productive_hours,
    working_days,
    target_utilization
):

    results = []

    # Annual engineer capacity
    annual_capacity = (
        productive_hours *
        working_days *
        12
    )

    # Effective capacity after utilization
    effective_capacity = (
        annual_capacity *
        target_utilization / 100
    )

    for _, row in df.iterrows():

        product = row["Product"]

        params = bu_parameters.get(
            product,
            {
                "BAU": 20,
                "DC": 20,
                "Attrition": 8
            }
        )

        bau_growth = params["BAU"]
        dc_growth = params["DC"]
        attrition = params["Attrition"]

        # Current workload hours

        current_hours = (
            row["Breakdown_WO"] * row["Breakdown_Hrs"]
            +
            row["PM_WO"] * row["PM_Hrs"]
            +
            row["Startup_WO"] * row["Startup_Hrs"]
        )

        # Future workload

        future_hours = (
            current_hours *
            (
                1
                + (bau_growth / 100)
                + (dc_growth / 100)
            )
        )

        # Required engineers

        required_engineers = (
            future_hours /
            effective_capacity
        )

        # Available engineers after attrition

        available_engineers = (
            row["Current_SE"] *
            (
                1 -
                (attrition / 100)
            )
        )

        # Hiring requirement

        additional_required = max(
            math.ceil(
                required_engineers -
                available_engineers
            ),
            0
        )

        results.append({

            "Region":
            row["Region"],

            "Product":
            row["Product"],

            "BAU Growth %":
            bau_growth,

            "DC Surge %":
            dc_growth,

            "Attrition %":
            attrition,

            "Productive Hrs/Day":
            productive_hours,

            "Working Days/Month":
            working_days,

            "Utilization %":
            target_utilization,

            "Annual Capacity":
            round(annual_capacity),

            "Effective Capacity":
            round(effective_capacity),

            "Current Hours":
            round(current_hours),

            "Future Hours":
            round(future_hours),

            "Required Engineers":
            round(required_engineers, 1),

            "Available Engineers":
            round(available_engineers, 1),

            "Additional Required":
            additional_required

        })

    return pd.DataFrame(results)
