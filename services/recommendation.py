"""
Campaign Optimization & Recommendation Engine (Rule-based AI Prototype)
Generates actionable strategic suggestions based on live data patterns.
Strictly labeled as Rule-based Prototype in accordance with Section 17 & 29.
"""

from typing import List, Dict, Any
import pandas as pd
import numpy as np


def generate_recommendations(df: pd.DataFrame, platform_summary: pd.DataFrame, month_summary: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Evaluates current campaign metrics and generates concrete optimization rules:
      1. High ROI Star Products (scale budget)
      2. High Revenue but low ROI (ad cost caution)
      3. Low CR but high clicks (landing/content review)
      4. Fastest Growing Platform (channel allocation)
      5. Top category potential
    """
    recommendations = []

    if df.empty:
        return [{
            "type": "info",
            "tag": "DỮ LIỆU",
            "title": "Chưa có đủ dữ liệu",
            "description": "Vui lòng chọn bộ lọc khác hoặc tải lại dữ liệu để nhận phân tích gợi ý.",
            "impact": "Neutral"
        }]

    # 1. Check Highest Performing Platform
    if not platform_summary.empty and len(platform_summary) > 1:
        top_plat = platform_summary.iloc[0]
        recommendations.append({
            "type": "success",
            "tag": "TĂNG TRƯỞNG KÊNH",
            "title": f"Ưu tiên ngân sách cho sàn {top_plat['platform']}",
            "description": (
                f"Sàn {top_plat['platform']} đang dẫn đầu với doanh thu {int(top_plat['revenue']):,} ₫ "
                f"và ROI đạt {top_plat['roi']:.2f}x. "
                f"Khuyến nghị duy trì và gia tăng 15–20% ngân sách quảng bá vào nền tảng này trong tháng tới."
            ),
            "impact": "Tích cực"
        })

    # 2. Identify High ROI + High Revenue Products (Stars)
    if "roi" in df.columns and "revenue" in df.columns:
        prod_agg = df.groupby(["product_name", "platform"]).agg(
            revenue=("revenue", "sum"),
            commission=("commission", "sum"),
            ad_cost=("ad_cost", "sum"),
            orders=("orders", "sum"),
            clicks=("clicks", "sum")
        ).reset_index()
        prod_agg["roi"] = np.where(prod_agg["ad_cost"] > 0, np.round(prod_agg["commission"] / prod_agg["ad_cost"], 2), 0.0)
        prod_agg["cr"] = np.where(prod_agg["clicks"] > 0, np.round(prod_agg["orders"] / prod_agg["clicks"] * 100.0, 2), 0.0)

        # Star products: ROI >= 2.5 and revenue in top 25%
        rev_threshold = prod_agg["revenue"].quantile(0.75) if len(prod_agg) > 4 else prod_agg["revenue"].mean()
        stars = prod_agg[(prod_agg["roi"] >= 2.5) & (prod_agg["revenue"] >= rev_threshold)]

        if not stars.empty:
            star_sample = stars.sort_values(by="revenue", ascending=False).iloc[0]
            recommendations.append({
                "type": "success",
                "tag": "SẢN PHẨM NGÔI SAO",
                "title": f"Tập trung đẩy mạnh: {star_sample['product_name']}",
                "description": (
                    f"Sản phẩm đạt hiệu quả vượt trội trên {star_sample['platform']} với ROI {star_sample['roi']:.2f}x "
                    f"và doanh thu {int(star_sample['revenue']):,} ₫. Đề xuất tiếp tục nhân rộng nội dung video/bài viết ngắn."
                ),
                "impact": "Tăng trưởng cao"
            })

        # 3. High Revenue but Low ROI (Ad cost alert)
        ad_alert = prod_agg[(prod_agg["revenue"] >= rev_threshold) & (prod_agg["roi"] < 1.3)]
        if not ad_alert.empty:
            alert_prod = ad_alert.sort_values(by="revenue", ascending=False).iloc[0]
            recommendations.append({
                "type": "warning",
                "tag": "CẢNH BÁO CHI PHÍ ADS",
                "title": f"Tối ưu chi phí quảng cáo cho: {alert_prod['product_name']}",
                "description": (
                    f"Sản phẩm tạo ra doanh số lớn ({int(alert_prod['revenue']):,} ₫) nhưng ROI chỉ đạt {alert_prod['roi']:.2f}x "
                    f"do chi phí quảng cáo ({int(alert_prod['ad_cost']):,} ₫) chiếm tỷ trọng quá cao trong hoa hồng. "
                    f"Cần rà soát từ khóa và giảm giá thầu bid CPC."
                ),
                "impact": "Tiết kiệm chi phí"
            })

        # 4. Low Conversion Rate but high clicks
        click_threshold = prod_agg["clicks"].quantile(0.7) if len(prod_agg) > 4 else prod_agg["clicks"].mean()
        low_cr = prod_agg[(prod_agg["clicks"] >= click_threshold) & (prod_agg["cr"] < 3.0)]
        if not low_cr.empty:
            sample_cr = low_cr.sort_values(by="clicks", ascending=False).iloc[0]
            recommendations.append({
                "type": "info",
                "tag": "TỐI ƯU CHUYỂN ĐỔI (CR)",
                "title": f"Cải thiện nội dung Landing: {sample_cr['product_name']}",
                "description": (
                    f"Chiến dịch thu hút {sample_cr['clicks']:,} lượt click nhưng tỷ lệ chuyển đổi chỉ đạt {sample_cr['cr']:.2f}%. "
                    f"Nên kiểm tra lại tính hấp dẫn của mã giảm giá, hình ảnh sản phẩm hoặc tệp người xem mục tiêu."
                ),
                "impact": "Tối ưu hiệu suất"
            })

    # 5. Month-over-Month Revenue Trend Alert
    if not month_summary.empty and len(month_summary) >= 2:
        latest_growth = month_summary.iloc[-1].get("revenue_growth_%", 0)
        latest_month = month_summary.iloc[-1]["month"]
        if latest_growth > 5:
            recommendations.append({
                "type": "success",
                "tag": "XU HƯỚNG TỔNG QUAN",
                "title": f"Đà tăng trưởng tích cực trong tháng {latest_month}",
                "description": (
                    f"Doanh số tháng {latest_month} tăng trưởng {latest_growth:.1f}% so với tháng trước. "
                    f"Chiến lược kết hợp đa sàn đang phát huy hiệu quả tốt."
                ),
                "impact": "Tích cực"
            })
        elif latest_growth < -5:
            recommendations.append({
                "type": "warning",
                "tag": "XU HƯỚNG TỔNG QUAN",
                "title": f"Doanh số có dấu hiệu chững lại trong tháng {latest_month}",
                "description": (
                    f"Doanh số giảm {abs(latest_growth):.1f}% so với tháng trước. "
                    f"Đề xuất làm mới danh mục sản phẩm affiliate và tham gia các ngày hội siêu sale sàn."
                ),
                "impact": "Cần can thiệp"
            })

    return recommendations
