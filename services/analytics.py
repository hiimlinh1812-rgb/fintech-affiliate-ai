"""
Analytics & Aggregation Service
Computes multi-dimensional performance statistics across platforms, months,
categories, and regions.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np


def aggregate_by_platform(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates metrics grouped by Platform."""
    if df.empty or "platform" not in df.columns:
        return pd.DataFrame()

    agg = df.groupby("platform").agg(
        revenue=("revenue", "sum"),
        commission=("commission", "sum"),
        ad_cost=("ad_cost", "sum"),
        profit=("profit", "sum"),
        orders=("orders", "sum"),
        clicks=("clicks", "sum"),
    ).reset_index()

    # Derived metrics
    agg["roi"] = np.where(agg["ad_cost"] > 0, np.round(agg["commission"] / agg["ad_cost"], 2), 0.0)
    agg["cr"] = np.where(agg["clicks"] > 0, np.round(agg["orders"] / agg["clicks"] * 100.0, 2), 0.0)
    agg["profit_margin"] = np.where(agg["revenue"] > 0, np.round(agg["profit"] / agg["revenue"] * 100.0, 2), 0.0)

    return agg.sort_values(by="revenue", ascending=False).reset_index(drop=True)


def aggregate_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates metrics grouped by Month (chronological order)."""
    if df.empty or "month" not in df.columns:
        return pd.DataFrame()

    agg = df.groupby("month").agg(
        revenue=("revenue", "sum"),
        commission=("commission", "sum"),
        ad_cost=("ad_cost", "sum"),
        profit=("profit", "sum"),
        orders=("orders", "sum"),
        clicks=("clicks", "sum")
    ).reset_index()

    agg = agg.sort_values(by="month").reset_index(drop=True)
    agg["roi"] = np.where(agg["ad_cost"] > 0, np.round(agg["commission"] / agg["ad_cost"], 2), 0.0)
    agg["cr"] = np.where(agg["clicks"] > 0, np.round(agg["orders"] / agg["clicks"] * 100.0, 2), 0.0)

    # Month-over-Month Revenue Growth (%)
    agg["revenue_growth_%"] = agg["revenue"].pct_change().fillna(0).round(4) * 100.0

    return agg


def aggregate_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates metrics by product category."""
    if df.empty or "category" not in df.columns:
        return pd.DataFrame()

    agg = df.groupby("category").agg(
        revenue=("revenue", "sum"),
        commission=("commission", "sum"),
        profit=("profit", "sum"),
        orders=("orders", "sum"),
        clicks=("clicks", "sum")
    ).reset_index()

    agg["roi"] = np.where(agg["profit"] > 0, np.round(agg["commission"] / (agg["commission"] - agg["profit"]), 2), 0.0)
    return agg.sort_values(by="revenue", ascending=False).reset_index(drop=True)


def aggregate_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates metrics by geographic region."""
    if df.empty or "region" not in df.columns:
        return pd.DataFrame()

    agg = df.groupby("region").agg(
        revenue=("revenue", "sum"),
        commission=("commission", "sum"),
        profit=("profit", "sum"),
        orders=("orders", "sum"),
        clicks=("clicks", "sum")
    ).reset_index()

    return agg.sort_values(by="revenue", ascending=False).reset_index(drop=True)


def get_top_products(df: pd.DataFrame, top_n: int = 10, sort_by: str = "revenue") -> pd.DataFrame:
    """Returns top performing products aggregated across campaigns."""
    if df.empty or "product_name" not in df.columns:
        return pd.DataFrame()

    agg = df.groupby(["product_id", "product_name", "category", "platform"]).agg(
        revenue=("revenue", "sum"),
        commission=("commission", "sum"),
        profit=("profit", "sum"),
        ad_cost=("ad_cost", "sum"),
        orders=("orders", "sum"),
        clicks=("clicks", "sum")
    ).reset_index()

    agg["roi"] = np.where(agg["ad_cost"] > 0, np.round(agg["commission"] / agg["ad_cost"], 2), 0.0)
    agg["cr"] = np.where(agg["clicks"] > 0, np.round(agg["orders"] / agg["clicks"] * 100.0, 2), 0.0)

    if sort_by in agg.columns:
        agg = agg.sort_values(by=sort_by, ascending=False)
    return agg.head(top_n).reset_index(drop=True)
