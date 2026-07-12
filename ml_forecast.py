import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    r2_score,
    mean_absolute_error
)


def forecast_work_orders(
        historical_df,
        product):

    data = historical_df[
        historical_df["Product"] == product
    ]

    forecasts = []

    metrics = ["Breakdown_WO",
               "PM_WO",
               "Startup_WO"]

    for metric in metrics:

        X = data[["Year"]]
        y = data[metric]

        model = LinearRegression()

        model.fit(X, y)

        train_pred = model.predict(X)

        r2 = r2_score(y, train_pred)

        mae = mean_absolute_error(
            y,
            train_pred
        )

        future_years = pd.DataFrame(
            {
                "Year": [
                    2026,
                    2027,
                    2028
                ]
            }
        )

        predictions = model.predict(
            future_years
        )

        temp = future_years.copy()

        temp["Metric"] = metric

        temp["Prediction"] = (
            predictions.round().astype(int)
        )

        temp["R2 Score"] = round(
            r2,
            3
        )

        temp["MAE"] = round(
            mae,
            2
        )

        forecasts.append(temp)

    return pd.concat(
        forecasts,
        ignore_index=True
    )
