"""
Unit tests for financial and KPI metrics calculations.
Complies with Section 23 of requirements.
"""

import unittest
import pandas as pd
from services.metrics import (
    calculate_conversion_rate,
    calculate_roi,
    calculate_net_profit,
    calculate_gross_profit,
    compute_kpis,
    safe_divide
)


class TestMetrics(unittest.TestCase):

    def test_safe_divide(self):
        self.assertEqual(safe_divide(10, 2), 5.0)
        self.assertEqual(safe_divide(10, 0), 0.0)
        self.assertEqual(safe_divide(0, 0), 0.0)
        self.assertEqual(safe_divide(10, None), 0.0)

    def test_conversion_rate(self):
        # 85 orders out of 1200 clicks = 7.08%
        cr = calculate_conversion_rate(85, 1200)
        self.assertEqual(cr, 7.08)

        # Zero clicks
        self.assertEqual(calculate_conversion_rate(5, 0), 0.0)

    def test_roi(self):
        # Commission 4,250,000 / Ad Cost 1,500,000 = 2.83
        roi = calculate_roi(4250000, 1500000)
        self.assertEqual(roi, 2.83)

        # Zero ad cost
        self.assertEqual(calculate_roi(4250000, 0), 0.0)

    def test_profit_calculations(self):
        net = calculate_net_profit(commission=5000000, ad_cost=2000000, other_cost=300000)
        self.assertEqual(net, 2700000.0)

        gross = calculate_gross_profit(revenue=50000000, ad_cost=2000000)
        self.assertEqual(gross, 48000000.0)

    def test_compute_kpis_empty(self):
        empty_kpi = compute_kpis(pd.DataFrame())
        self.assertEqual(empty_kpi["total_revenue"], 0)
        self.assertEqual(empty_kpi["avg_roi"], 0.0)

    def test_compute_kpis_populated(self):
        sample_df = pd.DataFrame([
            {"revenue": 1000000, "commission": 100000, "ad_cost": 40000, "profit": 60000, "orders": 5, "clicks": 100, "roi": 2.5},
            {"revenue": 2000000, "commission": 200000, "ad_cost": 60000, "profit": 140000, "orders": 10, "clicks": 200, "roi": 3.33}
        ])
        kpis = compute_kpis(sample_df)
        self.assertEqual(kpis["total_revenue"], 3000000.0)
        self.assertEqual(kpis["total_commission"], 300000.0)
        self.assertEqual(kpis["total_ad_cost"], 100000.0)
        self.assertEqual(kpis["total_profit"], 200000.0)
        self.assertEqual(kpis["avg_roi"], 3.0)  # 300,000 / 100,000 = 3.0
        self.assertEqual(kpis["total_orders"], 15)
        self.assertEqual(kpis["total_clicks"], 300)
        self.assertEqual(kpis["conversion_rate"], 5.0)


if __name__ == "__main__":
    unittest.main()
