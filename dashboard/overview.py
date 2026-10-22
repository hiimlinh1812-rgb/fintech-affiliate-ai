"""
Dashboard Overview Page
Displays KPI cards, interactive Plotly charts, and detailed data table with search & sort.
Complies with Section 7, 8, 9, 10 of requirements and Chapter 3 of CNDVTC.docx.
"""

import streamlit as st
import pandas as pd

from services.metrics import compute_kpis
from services.analytics import aggregate_by_platform, aggregate_by_month, get_top_products
from dashboard.charts import (
    create_platform_bar_chart,
    create_top_products_bar_chart,
    create_platform_pie_chart,
    create_revenue_trend_line_chart,
    create_combo_revenue_profit_chart,
    format_currency_vnd
)


def render_overview_page(df: pd.DataFrame, filters: dict):
    """Renders the main KPI Dashboard."""
    st.markdown("## 📊 Tổng Quan Hiệu Suất Tiếp Thị Liên Kết (Affiliate Dashboard)")
    st.caption("Nguyên mẫu Fintech AI phân tích xu hướng và tối ưu chiến dịch đa nền tảng (Demo Học Thuật)")

    if df.empty:
        st.warning("⚠️ Không có dữ liệu phù hợp với bộ lọc hiện tại. Vui lòng thay đổi tùy chọn trên thanh Sidebar.")
        return

    # Calculate KPIs
    kpis = compute_kpis(df)
    platform_summary = aggregate_by_platform(df)
    month_summary = aggregate_by_month(df)

    # 1. KPI CARDS (Section 8: 4 main KPIs + supplementary)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(
            label="Tổng Doanh Thu (GMV)",
            value=format_currency_vnd(kpis["total_revenue"]),
            help="Tổng giá trị đơn hàng bán ra qua liên kết affiliate"
        )
    with c2:
        st.metric(
            label="Tổng Hoa Hồng Nhận Được",
            value=format_currency_vnd(kpis["total_commission"]),
            help="Thu nhập hoa hồng ước tính từ sàn"
        )
    with c3:
        st.metric(
            label="Tổng Lợi Nhuận Ròng",
            value=format_currency_vnd(kpis["total_profit"]),
            delta=f"{kpis['total_profit'] / kpis['total_commission'] * 100:.1f}% biên hoa hồng" if kpis["total_commission"] > 0 else None,
            help="Lợi nhuận ròng = Hoa hồng - Chi phí quảng cáo"
        )
    with c4:
        st.metric(
            label="Hệ Số ROI Trung Bình",
            value=f"{kpis['avg_roi']:.2f}x",
            delta="Hiệu quả cao" if kpis["avg_roi"] >= 2.0 else "Cần tối ưu",
            delta_color="normal" if kpis["avg_roi"] >= 2.0 else "inverse",
            help="ROI = Hoa hồng / Chi phí quảng cáo"
        )

    # Secondary KPIs
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.metric(label="Tổng Chi Phí Ads", value=format_currency_vnd(kpis["total_ad_cost"]))
    with s2:
        st.metric(label="Tổng Số Đơn Hàng", value=f"{kpis['total_orders']:,} đơn")
    with s3:
        st.metric(label="Tổng Lượt Nhấp (Clicks)", value=f"{kpis['total_clicks']:,} lượt")
    with s4:
        st.metric(label="Tỷ Lệ Chuyển Đổi (CR)", value=f"{kpis['conversion_rate']:.2f}%")

    st.markdown("---")

    # 2. CHARTS SECTION (Section 9)
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        # Platform comparison bar chart
        metric_choice = st.selectbox(
            "Chỉ số so sánh nền tảng:",
            options=["revenue", "commission", "profit", "ad_cost"],
            format_func=lambda x: {
                "revenue": "Doanh thu (GMV)",
                "commission": "Hoa hồng",
                "profit": "Lợi nhuận ròng",
                "ad_cost": "Chi phí Ads"
            }[x],
            key="bar_metric_sel"
        )
        fig_bar = create_platform_bar_chart(platform_summary, metric=metric_choice)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_chart2:
        # Platform share pie chart
        pie_metric = st.selectbox(
            "Tỷ trọng phân bổ theo:",
            options=["revenue", "commission"],
            format_func=lambda x: "Doanh thu (GMV)" if x == "revenue" else "Hoa hồng nhận được",
            key="pie_metric_sel"
        )
        fig_pie = create_platform_pie_chart(platform_summary, metric=pie_metric)
        st.plotly_chart(fig_pie, use_container_width=True)

    # Trend Charts
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        fig_line = create_revenue_trend_line_chart(month_summary)
        st.plotly_chart(fig_line, use_container_width=True)

    with t_col2:
        fig_combo = create_combo_revenue_profit_chart(month_summary)
        st.plotly_chart(fig_combo, use_container_width=True)

    st.markdown("---")

    # 3. TOP PRODUCTS & DETAILED DATA TABLE (Section 10)
    st.subheader("📋 Bảng Dữ Liệu Chiến Dịch Chi Tiết")
    
    # Search and Sort Controls
    f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
    with f_col1:
        search_kw = st.text_input("🔍 Tìm kiếm tên sản phẩm hoặc mã:", placeholder="Nhập từ khóa...")
    with f_col2:
        sort_col = st.selectbox(
            "Sắp xếp theo:",
            options=["revenue", "commission", "profit", "roi", "orders", "clicks"],
            format_func=lambda x: {
                "revenue": "Doanh thu",
                "commission": "Hoa hồng",
                "profit": "Lợi nhuận",
                "roi": "ROI",
                "orders": "Đơn hàng",
                "clicks": "Lượt click"
            }[x]
        )
    with f_col3:
        sort_asc = st.radio("Thứ tự:", ["Giảm dần", "Tăng dần"], horizontal=True) == "Tăng dần"

    display_df = df.copy()
    if search_kw:
        mask = (
            display_df["product_name"].str.contains(search_kw, case=False, na=False) |
            display_df["product_id"].str.contains(search_kw, case=False, na=False)
        )
        display_df = display_df[mask]

    display_df = display_df.sort_values(by=sort_col, ascending=sort_asc)

    # Required columns in Section 10: Product, Platform, Revenue, Commission, Profit, ROI, Clicks, Orders, CR, Region, Date
    table_cols = [
        "product_id", "product_name", "category", "platform",
        "revenue", "commission", "ad_cost", "profit", "roi",
        "clicks", "orders", "conversion_rate", "region", "date"
    ]
    
    # Clean display copy with formatted currencies
    formatted_table = display_df[table_cols].copy()
    formatted_table.columns = [
        "Mã SP", "Tên Sản Phẩm", "Ngành Hàng", "Sàn TMĐT",
        "Doanh Thu (₫)", "Hoa Hồng (₫)", "Chi Phí Ads (₫)", "Lợi Nhuận (₫)", "ROI",
        "Clicks", "Đơn", "CR (%)", "Khu Vực", "Ngày"
    ]

    st.dataframe(
        formatted_table,
        use_container_width=True,
        hide_index=True,
        height=350
    )
    st.caption(f"Hiển thị {len(display_df):,} / {len(df):,} bản ghi phù hợp.")
