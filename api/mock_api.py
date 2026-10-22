"""
Mock API Server for Fintech Affiliate Marketing AI Prototype
Simulates affiliate reporting APIs from Shopee, Lazada, TikTok Shop.
Complies with specifications in CNDVTC.docx (Academic Demo).
"""

import os
import json
import random
from datetime import datetime
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Fintech Affiliate Mock API",
    description="Mock API Server simulating e-commerce affiliate data for academic demo.",
    version="1.0.0"
)

# Enable CORS for local cross-origin calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "sample")

# In-memory storage loaded from sample JSON files
_DATA_CACHE: Dict[str, Dict[str, Any]] = {}
_LAST_UPDATE_TIME: datetime = datetime.now()


def _load_platform_data(platform_key: str) -> Dict[str, Any]:
    """Loads sample JSON for a given platform into memory cache."""
    file_map = {
        "shopee": "shopee.json",
        "lazada": "lazada.json",
        "tiktok-shop": "tiktok_shop.json",
        "tiktok_shop": "tiktok_shop.json"
    }
    
    file_name = file_map.get(platform_key.lower())
    if not file_name:
        raise HTTPException(status_code=404, detail=f"Platform '{platform_key}' not found.")
    
    file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=500, detail=f"Data file for '{platform_key}' missing at {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def init_cache():
    """Initializes in-memory cache on startup."""
    global _DATA_CACHE, _LAST_UPDATE_TIME
    for p in ["shopee", "lazada", "tiktok-shop"]:
        norm_key = "tiktok-shop" if "tiktok" in p else p
        _DATA_CACHE[norm_key] = _load_platform_data(p)
    _LAST_UPDATE_TIME = datetime.now()


# Load cache initially
init_cache()


@app.get("/")
def root():
    """Root info endpoint."""
    return {
        "message": "Fintech Affiliate Mock API Server is running",
        "academic_note": "Demo data only. No connection to real e-commerce APIs.",
        "platforms": ["/api/shopee", "/api/lazada", "/api/tiktok-shop", "/api/all"],
        "last_updated": _LAST_UPDATE_TIME.isoformat()
    }


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/api/shopee")
def get_shopee_data(region: Optional[str] = Query(None), month: Optional[str] = Query(None)):
    """Returns simulated affiliate data for Shopee."""
    return _filter_data("shopee", region, month)


@app.get("/api/lazada")
def get_lazada_data(region: Optional[str] = Query(None), month: Optional[str] = Query(None)):
    """Returns simulated affiliate data for Lazada."""
    return _filter_data("lazada", region, month)


@app.get("/api/tiktok-shop")
@app.get("/api/tiktok_shop")
def get_tiktok_data(region: Optional[str] = Query(None), month: Optional[str] = Query(None)):
    """Returns simulated affiliate data for TikTok Shop."""
    return _filter_data("tiktok-shop", region, month)


@app.get("/api/all")
def get_all_data(region: Optional[str] = Query(None), month: Optional[str] = Query(None)):
    """Returns merged simulated affiliate data across all platforms."""
    combined = []
    for p in ["shopee", "lazada", "tiktok-shop"]:
        res = _filter_data(p, region, month)
        combined.extend(res.get("data", []))
    return {
        "platform": "All",
        "count": len(combined),
        "updated_at": _LAST_UPDATE_TIME.isoformat(),
        "data": combined
    }


@app.post("/api/refresh")
@app.get("/api/refresh")
def trigger_refresh_simulation():
    """
    Simulates the 15-minute dynamic data update described in report CNDVTC.docx (Section 2.3.5).
    Applies a random multiplier (1.01 - 1.05) to latest records to simulate market fluctuation.
    """
    global _DATA_CACHE, _LAST_UPDATE_TIME
    factor = round(random.uniform(1.01, 1.05), 4)
    updated_count = 0
    
    for platform_key, payload in _DATA_CACHE.items():
        records = payload.get("data", [])
        # Find latest month in records (typically 2025-11)
        if not records:
            continue
        max_date = max(r.get("date", datetime.now().strftime("%Y-%m-%d")) for r in records)
        latest_month = max_date[:7]
        
        for r in records:
            if r.get("date", "").startswith(latest_month):
                r["clicks"] = int(r["clicks"] * factor)
                r["orders"] = max(1, int(r["orders"] * factor))
                r["conversion_rate"] = round((r["orders"] / r["clicks"]) * 100, 2)
                r["revenue"] = int(r["revenue"] * factor)
                r["commission"] = int(r["commission"] * factor)
                r["ad_cost"] = int(r["ad_cost"] * factor)
                r["profit"] = r["commission"] - r["ad_cost"]
                r["roi"] = round(r["commission"] / r["ad_cost"], 2) if r["ad_cost"] > 0 else 0.0
                updated_count += 1
                
        payload["updated_at"] = datetime.now().isoformat()

    _LAST_UPDATE_TIME = datetime.now()
    return {
        "status": "success",
        "message": f"Simulated 15-minute market tick applied with factor {factor} (+{round((factor-1)*100, 2)}%)",
        "records_updated": updated_count,
        "updated_at": _LAST_UPDATE_TIME.isoformat()
    }


def _filter_data(platform_key: str, region: Optional[str] = None, month: Optional[str] = None) -> Dict[str, Any]:
    if platform_key not in _DATA_CACHE:
        _DATA_CACHE[platform_key] = _load_platform_data(platform_key)
        
    source = _DATA_CACHE[platform_key]
    items = source.get("data", [])
    
    if region and region.lower() != "all" and region.lower() != "tất cả":
        items = [i for i in items if i.get("region", "").lower() == region.lower()]
        
    if month and month.lower() != "all" and month.lower() != "tất cả":
        items = [i for i in items if i.get("date", "").startswith(month)]
        
    return {
        "platform": source.get("platform", platform_key.capitalize()),
        "count": len(items),
        "updated_at": source.get("updated_at", _LAST_UPDATE_TIME.isoformat()),
        "data": items
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("mock_api:app", host="127.0.0.1", port=8001, reload=True)
