import pandas as pd
import math



def calculate_workforce(
    df,
    bu_parameters,
    region_parameters,
    productive_hours,
    working_days,
    target_utilization
):


    results = []

    annual_capacity = (
        productive_hours *
        working_days *
        12
    )

    effective_capacity = (
        annual_capacity *
        target_utilization / 100
    )

    for _, row in df.iterrows():

        region = row["Region"]
        product = row["Product"]

        region_growth = region_parameters.get(
            region,
            {
                "BAU": 15,
                "DC": 10
            }
        )

        product_attrition = bu_parameters.get(
            product,
            {
                "Attrition": 8
            }
        )

        bau_growth = region_growth["BAU"]

        dc_growth = region_growth["DC"]

        attrition = (
            product_attrition["Attrition"]
        )

        current_hours = (

            row["Breakdown_WO"]
            *
            row["Breakdown_Hrs"]

            +

            row["PM_WO"]
            *
            row["PM_Hrs"]

            +

            row["Startup_WO"]
            *
            row["Startup_Hrs"]

        )

        future_hours = (

            current_hours *

            (
                1
                + bau_growth / 100
                + dc_growth / 100
            )

        )

        required_engineers = (
            future_hours /
            effective_capacity
        )

        available_engineers = (

            row["Current_SE"]

            *

            (
                1 -
                attrition / 100
            )
        )

        additional_required = max(
            math.ceil(
                required_engineers
                - available_engineers
            ),
            0
        )

        results.append({

            "Region":
            region,

            "Product":
            product,

            "BAU Growth %":
            bau_growth,

            "DC Growth %":
            dc_growth,

            "Attrition %":
            attrition,

            "Current Hours":
            round(current_hours),

            "Future Hours":
            round(future_hours),

            "Required Engineers":
            round(
                required_engineers,
                1
            ),

            "Available Engineers":
            round(
                available_engineers,
                1
            ),

            "Additional Required":
            additional_required

        })

    return pd.DataFrame(results)
