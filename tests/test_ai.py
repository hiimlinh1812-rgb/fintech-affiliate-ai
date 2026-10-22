"""
Unit tests for AI modules: Linear Regression forecasting and NLP Chatbot.
Complies with Section 23 of requirements.
"""

import unittest
import pandas as pd
from ai.linear_regression import train_and_forecast_monthly_revenue
from ai.chatbot import AffiliateChatbotAssistant


class TestAIModules(unittest.TestCase):

    def test_forecast_sufficient_data(self):
        # 6 months of historical data
        month_data = pd.DataFrame([
            {"month": "2026-05", "revenue": 100000000},
            {"month": "2026-06", "revenue": 110000000},
            {"month": "2026-07", "revenue": 125000000},
            {"month": "2026-08", "revenue": 140000000},
            {"month": "2026-09", "revenue": 155000000},
            {"month": "2026-10", "revenue": 170000000},
        ])
        res = train_and_forecast_monthly_revenue(month_data)
        self.assertTrue(res["success"])
        self.assertEqual(res["next_month"], "2026-11")
        self.assertGreater(res["forecast_value"], 170000000)
        self.assertIsNotNone(res["mae"])
        self.assertIsNotNone(res["rmse"])
        self.assertIsNotNone(res["r2"])
        self.assertEqual(res["trend_direction"], "Tăng trưởng")

    def test_forecast_insufficient_data(self):
        # Only 2 months of data (must reject)
        short_data = pd.DataFrame([
            {"month": "2026-09", "revenue": 100000000},
            {"month": "2026-10", "revenue": 120000000},
        ])
        res = train_and_forecast_monthly_revenue(short_data)
        self.assertFalse(res["success"])
        self.assertIn("Không đủ dữ liệu", res["message"])
        self.assertIsNone(res["forecast_value"])

    def test_chatbot_intent_classification(self):
        bot = AffiliateChatbotAssistant()

        # Revenue query
        intent, _ = bot.identify_intent("Doanh thu tháng này là bao nhiêu?")
        self.assertEqual(intent, "revenue_query")

        # Product query
        intent, _ = bot.identify_intent("Sản phẩm nào bán chạy nhất?")
        self.assertEqual(intent, "product_comparison")

        # Platform query
        intent, _ = bot.identify_intent("So sánh Shopee và Lazada?")
        self.assertEqual(intent, "platform_comparison")

        # Forecast query
        intent, _ = bot.identify_intent("Dự đoán doanh số tháng tới?")
        self.assertEqual(intent, "forecast_query")

        # Recommendation query
        intent, _ = bot.identify_intent("Gợi ý tối ưu chi phí quảng cáo?")
        self.assertEqual(intent, "campaign_recommendation")


if __name__ == "__main__":
    unittest.main()
