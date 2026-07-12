import math
import pandas as pd


def calculate_workforce(
    df,
    bu_parameters,
    regional_dc_growth,
    productive_hours,
    working_days,
    target_utilization
):
    results = []

    annual_capacity = productive_hours * working_days * 12
    effective_capacity = annual_capacity * target_utilization / 100

    for _, row in df.iterrows():
        region = row["Region"]
        product = row["Product"]

        params = bu_parameters.get(
            product,
            {
                "BAU": 20,
                "Attrition": 8,
                "DC_Action": "Add Regional DC Growth"
            }
        )

        bau_growth = params["BAU"]
        attrition = params["Attrition"]
        dc_action = params["DC_Action"]

        region_dc_growth = regional_dc_growth.get(region, 0)

        if dc_action == "Add Regional DC Growth":
            applied_dc_growth = region_dc_growth
        elif dc_action == "Do Not Add Regional DC Growth":
            applied_dc_growth = 0
        elif dc_action == "Delete Regional DC Growth":
            applied_dc_growth = -region_dc_growth
        else:
            applied_dc_growth = 0

        total_growth = bau_growth + applied_dc_growth

        current_hours = (
            row["Breakdown_WO"] * row["Breakdown_Hrs"]
            + row["PM_WO"] * row["PM_Hrs"]
            + row["Startup_WO"] * row["Startup_Hrs"]
        )

        future_hours = current_hours * (1 + total_growth / 100)

        required_engineers = future_hours / effective_capacity

        available_engineers = row["Current_SE"] * (1 - attrition / 100)

        additional_required = max(
            math.ceil(required_engineers - available_engineers),
            0
        )

        results.append(
            {
                "Region": region,
                "Product": product,
                "BAU Growth %": bau_growth,
                "Regional DC Growth %": region_dc_growth,
                "BU DC Action": dc_action,
                "Applied DC Growth %": applied_dc_growth,
                "Total Growth %": total_growth,
                "Attrition %": attrition,
                "Productive Hrs/Day": productive_hours,
                "Working Days/Month": working_days,
                "Utilization %": target_utilization,
                "Annual Capacity": round(annual_capacity),
                "Effective Capacity": round(effective_capacity),
                "Current Hours": round(current_hours),
                "Future Hours": round(future_hours),
                "Required Engineers": round(required_engineers, 1),
                "Available Engineers": round(available_engineers, 1),
                "Additional Required": additional_required
            }
        )

    return pd.DataFrame(results)
