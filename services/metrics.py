"""
Financial & Performance Metrics Calculation Module
Implements KPI formulas as defined in report CNDVTC.docx (Section 6.3 & Section 8).
Ensures safe division by zero and consistency throughout the system.
"""

from typing import Dict, Any, Union
import pandas as pd
import numpy as np


def safe_divide(numerator: Union[int, float], denominator: Union[int, float], default: float = 0.0) -> float:
    """Safe division avoiding ZeroDivisionError or NaN/Inf."""
    if denominator is None or denominator == 0 or np.isnan(denominator):
        return default
    if numerator is None or np.isnan(numerator):
        return default
    return float(numerator / denominator)


def calculate_conversion_rate(orders: Union[int, float], clicks: Union[int, float]) -> float:
    """
    Conversion Rate (CR %):
    CR = (Orders / Clicks) * 100
    """
    res = safe_divide(orders, clicks, 0.0) * 100.0
    return round(res, 2)


def calculate_roi(commission: Union[int, float], ad_cost: Union[int, float]) -> float:
    """
    Return On Investment (ROI):
    For affiliate marketing, ROI is defined as Commission earned divided by Ad Cost.
    ROI = Commission / Ad_Cost
    """
    res = safe_divide(commission, ad_cost, 0.0)
    return round(res, 2)


def calculate_net_profit(commission: Union[int, float], ad_cost: Union[int, float], other_cost: Union[int, float] = 0) -> float:
    """
    Net Affiliate Profit:
    Profit = Commission - Ad_Cost - Other_Cost
    """
    c = commission if commission is not None and not np.isnan(commission) else 0
    a = ad_cost if ad_cost is not None and not np.isnan(ad_cost) else 0
    o = other_cost if other_cost is not None and not np.isnan(other_cost) else 0
    return float(c - a - o)


def calculate_gross_profit(revenue: Union[int, float], ad_cost: Union[int, float]) -> float:
    """
    Gross Profit:
    Profit = Revenue - Ad_Cost
    """
    r = revenue if revenue is not None and not np.isnan(revenue) else 0
    a = ad_cost if ad_cost is not None and not np.isnan(ad_cost) else 0
    return float(r - a)


def compute_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes overall summary KPIs for the dashboard.
    Mandatory KPIs (Section 8):
      1. Total Revenue
      2. Total Commission
      3. Total Profit
      4. Average ROI
    Supplementary KPIs:
      - Total Orders
      - Conversion Rate
      - Total Clicks
      - Total Ad Cost
    """
    if df is None or df.empty:
        return {
            "total_revenue": 0,
            "total_commission": 0,
            "total_profit": 0,
            "avg_roi": 0.0,
            "total_orders": 0,
            "total_clicks": 0,
            "conversion_rate": 0.0,
            "total_ad_cost": 0,
            "count": 0
        }

    total_revenue = float(df["revenue"].sum()) if "revenue" in df.columns else 0.0
    total_commission = float(df["commission"].sum()) if "commission" in df.columns else 0.0
    total_ad_cost = float(df["ad_cost"].sum()) if "ad_cost" in df.columns else 0.0
    total_profit = float(df["profit"].sum()) if "profit" in df.columns else (total_commission - total_ad_cost)
    total_orders = int(df["orders"].sum()) if "orders" in df.columns else 0
    total_clicks = int(df["clicks"].sum()) if "clicks" in df.columns else 0

    # Average ROI weighted by ad spend or column mean
    if total_ad_cost > 0:
        avg_roi = round(total_commission / total_ad_cost, 2)
    elif "roi" in df.columns and len(df["roi"].dropna()) > 0:
        avg_roi = round(float(df["roi"].mean()), 2)
    else:
        avg_roi = 0.0

    # Overall conversion rate
    overall_cr = round((total_orders / total_clicks * 100.0), 2) if total_clicks > 0 else 0.0

    return {
        "total_revenue": total_revenue,
        "total_commission": total_commission,
        "total_profit": total_profit,
        "avg_roi": avg_roi,
        "total_orders": total_orders,
        "total_clicks": total_clicks,
        "conversion_rate": overall_cr,
        "total_ad_cost": total_ad_cost,
        "count": len(df)
    }
