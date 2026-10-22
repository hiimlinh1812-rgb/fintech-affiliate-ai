"""
Unit tests for FastAPI Mock Server endpoints.
Complies with Section 23 of requirements.
"""

import unittest
from fastapi.testclient import TestClient
from api.mock_api import app


class TestMockAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_check(self):
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json().get("status"), "healthy")

    def test_shopee_endpoint(self):
        res = self.client.get("/api/shopee")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get("platform"), "Shopee")
        self.assertGreater(data.get("count", 0), 0)
        self.assertTrue(len(data.get("data", [])) > 0)
        # Check first item schema
        item = data["data"][0]
        self.assertIn("product_id", item)
        self.assertIn("revenue", item)
        self.assertIn("commission", item)

    def test_lazada_endpoint(self):
        res = self.client.get("/api/lazada")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get("platform"), "Lazada")
        self.assertGreater(data.get("count", 0), 0)

    def test_tiktok_endpoint(self):
        res = self.client.get("/api/tiktok-shop")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("TikTok", data.get("platform", ""))
        self.assertGreater(data.get("count", 0), 0)

    def test_simulate_refresh_endpoint(self):
        res = self.client.post("/api/refresh")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get("status"), "success")
        self.assertIn("factor", data.get("message", ""))


if __name__ == "__main__":
    unittest.main()
