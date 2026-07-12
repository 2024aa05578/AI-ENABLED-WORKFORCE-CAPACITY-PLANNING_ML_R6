import math
import pandas as pd


def calculate_workforce(
    df,
    growth_parameters,
    attrition_parameters,
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

        region_product_params = growth_parameters.get(region, {}).get(
            product,
            {
                "BAU": 20,
                "DC": 0
            }
        )

