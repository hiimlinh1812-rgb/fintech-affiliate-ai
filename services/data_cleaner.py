"""
Data Cleaning & Normalization Module
Standardizes and validates affiliate data across multi-channel platforms.
Complies with Section 6 of requirements and Section 1.4 (Step 2) of CNDVTC.docx.
"""

from typing import List, Dict, Any
import pandas as pd
import numpy as np


STANDARD_COLUMNS = [
    "product_id",
    "product_name",
    "category",
    "price",
    "clicks",
    "orders",
    "conversion_rate",
    "revenue",
    "commission",
    "ad_cost",
    "profit",
    "roi",
    "platform",
    "region",
    "date",
    "month"
]

PLATFORM_NORMALIZATION_MAP = {
    "shopee": "Shopee",
    "lazada": "Lazada",
    "tiktok": "TikTok Shop",
    "tiktok shop": "TikTok Shop",
    "tiktok_shop": "TikTok Shop",
    "tiktok-shop": "TikTok Shop"
}


def clean_and_normalize(records: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Cleans raw multi-platform records into a standardized Pandas DataFrame.
    
    Steps:
      1. Converts to DataFrame
      2. Handles missing columns
      3. Standardizes platform names
      4. Strips and cleans product names
      5. Normalizes dates & generates 'month' field
      6. Enforces non-negative values for revenue, commission, clicks, ad_cost
      7. Re-calculates and validates CR, Profit, and ROI
      8. Removes duplicates
    """
    if not records:
        return pd.DataFrame(columns=STANDARD_COLUMNS)

    df = pd.DataFrame(records)

    # 1. Standardize platform names
    if "platform" in df.columns:
        df["platform"] = df["platform"].astype(str).str.strip()
        df["platform"] = df["platform"].apply(lambda p: PLATFORM_NORMALIZATION_MAP.get(p.lower(), p))
    else:
        df["platform"] = "Unknown"

    # 2. Standardize product names and IDs
    if "product_name" in df.columns:
        df["product_name"] = df["product_name"].astype(str).str.strip().str.replace(r"\s+", " ", regex=True)
    else:
        df["product_name"] = "Unknown Product"

    if "product_id" not in df.columns:
        df["product_id"] = [f"PRD_{i:04d}" for i in range(len(df))]
    else:
        df["product_id"] = df["product_id"].astype(str).str.strip()

    if "category" not in df.columns:
        df["category"] = "General"
    else:
        df["category"] = df["category"].fillna("General").astype(str).str.strip()

    if "region" not in df.columns:
        df["region"] = "Nationwide"
    else:
        df["region"] = df["region"].fillna("Nationwide").astype(str).str.strip()

    # 3. Clean and standardize dates (dynamically defaults to current date)
    now_ts = pd.Timestamp.now()
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        # Fill missing dates with today
        df["date"] = df["date"].fillna(now_ts)
        df["month"] = df["date"].dt.strftime("%Y-%m")
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    else:
        df["date"] = now_ts.strftime("%Y-%m-%d")
        df["month"] = now_ts.strftime("%Y-%m")

    # 4. Numerical columns validation & non-negative enforcement
    num_cols = ["price", "clicks", "orders", "revenue", "commission", "ad_cost"]
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
            # Ensure no negative values (Section 6.1: Không để doanh thu âm)
            df[col] = df[col].apply(lambda x: max(0, x))
        else:
            df[col] = 0

    # Ensure integers for counts
    df["clicks"] = df["clicks"].astype(int)
    df["orders"] = df["orders"].astype(int)
    df["price"] = df["price"].astype(int)
    df["revenue"] = df["revenue"].astype(int)
    df["commission"] = df["commission"].astype(int)
    df["ad_cost"] = df["ad_cost"].astype(int)

    # 5. Recompute financial & performance fields consistently
    # Conversion rate (%)
    df["conversion_rate"] = np.where(
        df["clicks"] > 0,
        np.round((df["orders"] / df["clicks"]) * 100.0, 2),
        0.0
    )

    # Profit = Commission - Ad Cost
    df["profit"] = df["commission"] - df["ad_cost"]

    # ROI = Commission / Ad Cost
    df["roi"] = np.where(
        df["ad_cost"] > 0,
        np.round(df["commission"] / df["ad_cost"], 2),
        0.0
    )

    # 6. Deduplication
    df = df.drop_duplicates(subset=["product_id", "platform", "date", "region"])

    # 7. Select standard columns order
    for col in STANDARD_COLUMNS:
        if col not in df.columns:
            df[col] = None

    return df[STANDARD_COLUMNS].reset_index(drop=True)
