"""
Linear Regression Forecasting Module
Implements Scikit-learn LinearRegression for monthly revenue prediction.
Complies with Section 14 of requirements and Section 2.3.2 of CNDVTC.docx.
Evaluates actual MAE and RMSE without fabricated metrics.
"""

from typing import Dict, Any, Tuple, Optional
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def train_and_forecast_monthly_revenue(month_summary: pd.DataFrame) -> Dict[str, Any]:
    """
    Fits a Linear Regression model on historical monthly revenue data
    and forecasts the revenue for the upcoming month.
    
    Validates minimum data requirements (at least 3 data points).
    Returns forecast value, model metrics (MAE, RMSE, R2), and fitted line points.
    """
    if month_summary is None or len(month_summary) < 3:
        return {
            "success": False,
            "message": "Không đủ dữ liệu lịch sử để dự báo. Cần tối thiểu 3 tháng dữ liệu liên tiếp.",
            "forecast_value": None,
            "next_month": None,
            "mae": None,
            "rmse": None,
            "r2": None,
            "history_df": pd.DataFrame()
        }

    df = month_summary.sort_values(by="month").copy().reset_index(drop=True)
    df["time_idx"] = np.arange(len(df))

    # Features: time index, and optional ad_cost if available
    X = df[["time_idx"]].values
    y = df["revenue"].values

    model = LinearRegression()
    model.fit(X, y)

    # In-sample predictions
    y_pred = model.predict(X)
    df["fitted_revenue"] = np.round(y_pred, 0)

    # Calculate actual metrics
    mae = float(mean_absolute_error(y, y_pred))
    rmse = float(np.sqrt(mean_squared_error(y, y_pred)))
    r2 = float(r2_score(y, y_pred)) if len(df) > 1 else 1.0

    # Next month index
    next_idx = np.array([[len(df)]])
    next_rev = float(model.predict(next_idx)[0])
    # Enforce non-negative revenue prediction
    next_rev = max(0.0, next_rev)

    # Calculate next month label
    last_month_str = df.iloc[-1]["month"]
    try:
        y_val, m_val = map(int, last_month_str.split("-"))
        if m_val == 12:
            next_month_str = f"{y_val + 1}-01"
        else:
            next_month_str = f"{y_val}-{m_val + 1:02d}"
    except Exception:
        next_month_str = "Tháng kế tiếp"

    trend_direction = "Tăng trưởng" if model.coef_[0] > 0 else "Giảm sút"
    monthly_change_est = float(model.coef_[0])

    return {
        "success": True,
        "message": "Dự báo tuyến tính thành công (Scikit-learn LinearRegression Prototype).",
        "forecast_value": round(next_rev, 0),
        "next_month": next_month_str,
        "monthly_trend_delta": round(monthly_change_est, 0),
        "trend_direction": trend_direction,
        "mae": round(mae, 0),
        "rmse": round(rmse, 0),
        "r2": round(r2, 4),
        "history_df": df
    }
