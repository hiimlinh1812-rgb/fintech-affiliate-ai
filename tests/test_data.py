"""
Unit tests for data loading and data cleaning modules.
Complies with Section 23 of requirements.
"""

import unittest
import pandas as pd
from services.data_cleaner import clean_and_normalize
from services.data_loader import load_affiliate_data


class TestDataProcessing(unittest.TestCase):

    def test_clean_and_normalize_basic(self):
        records = [
            {
                "product_id": "SP001",
                "product_name": "  Tai nghe Bluetooth  ",
                "category": "Electronics",
                "price": 500000,
                "clicks": 1000,
                "orders": 50,
                "revenue": 25000000,
                "commission": 2500000,
                "ad_cost": 1000000,
                "platform": "shopee",
                "region": "Hanoi",
                "date": "2026-10-05"
            }
        ]
        df = clean_and_normalize(records)
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["platform"], "Shopee")
        self.assertEqual(df.iloc[0]["product_name"], "Tai nghe Bluetooth")
        self.assertEqual(df.iloc[0]["roi"], 2.5)
        self.assertEqual(df.iloc[0]["profit"], 1500000)
        self.assertEqual(df.iloc[0]["conversion_rate"], 5.0)

    def test_handle_negative_and_missing(self):
        records = [
            {
                "product_id": "SP002",
                "product_name": "Sản phẩm lỗi",
                "price": -100,
                "clicks": -50,
                "orders": None,
                "revenue": -5000000,
                "commission": -200000,
                "ad_cost": 0,
                "platform": "tiktok_shop",
                "date": "invalid-date"
            }
        ]
        df = clean_and_normalize(records)
        self.assertEqual(len(df), 1)
        # Should enforce non-negative values
        self.assertGreaterEqual(df.iloc[0]["revenue"], 0)
        self.assertGreaterEqual(df.iloc[0]["commission"], 0)
        self.assertGreaterEqual(df.iloc[0]["clicks"], 0)
        self.assertEqual(df.iloc[0]["platform"], "TikTok Shop")
        self.assertEqual(df.iloc[0]["roi"], 0.0)

    def test_deduplication(self):
        record = {
            "product_id": "SP_DUP",
            "product_name": "Trùng lặp",
            "price": 100000,
            "clicks": 100,
            "orders": 5,
            "revenue": 500000,
            "commission": 50000,
            "ad_cost": 10000,
            "platform": "Lazada",
            "region": "Hanoi",
            "date": "2026-10-01"
        }
        df = clean_and_normalize([record, record, record])
        self.assertEqual(len(df), 1)

    def test_data_loader_local_fallback(self):
        df, meta = load_affiliate_data(platform="All", region="All", month="All")
        self.assertFalse(df.empty)
        self.assertGreaterEqual(len(df), 100)
        self.assertIn("revenue", df.columns)


if __name__ == "__main__":
    unittest.main()
