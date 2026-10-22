"""
Revenue Report Page & Export Center
Displays monthly and platform summaries, financial charts, and handles Excel & PDF exports.
Complies with Section 11 of requirements and Chapter 3 (Demo Báo cáo doanh số) of CNDVTC.docx.
"""

from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from services.analytics import aggregate_by_platform, aggregate_by_month, aggregate_by_category
from services.reporting import export_to_excel, export_to_pdf
from dashboard.charts import (
    create_platform_pie_chart,
    create_revenue_trend_line_chart,
    format_currency_vnd,
    FINTECH_COLORS
)


def render_revenue_report_page(df: pd.DataFrame, filters: dict):
    """Renders dedicated Revenue Report page with Excel and PDF download triggers."""
    st.markdown("## 📑 Báo Cáo Doanh Thu & Hiệu Quả Đa Kênh")
    st.caption("Báo cáo định kỳ phân bổ doanh số, hoa hồng và lợi nhuận ròng cá nhân")

    if df.empty:
        st.warning("⚠️ Không có dữ liệu để lập báo cáo với bộ lọc hiện tại.")
        return

    platform_summary = aggregate_by_platform(df)
    month_summary = aggregate_by_month(df)
    cat_summary = aggregate_by_category(df)

    # 1. EXPORT ACTION BUTTONS (Section 11)
    st.markdown("### 📥 Xuất Báo Cáo Định Dạng Chuẩn")
    exp_col1, exp_col2, exp_col3 = st.columns([1, 1, 2])

    with exp_col1:
        excel_bytes = export_to_excel(df, platform_summary, month_summary, filters)
        st.download_button(
            label="📊 Tải Báo Cáo Excel (.xlsx)",
            data=excel_bytes,
            file_name=f"Bao_Cao_Affiliate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    with exp_col2:
        pdf_bytes = export_to_pdf(df, platform_summary, filters)
        st.download_button(
            label="📄 Tải Báo Cáo PDF (.pdf)",
            data=pdf_bytes,
            file_name=f"Bao_Cao_Affiliate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    with exp_col3:
        st.info(
            f"ℹ️ Dữ liệu xuất bao gồm **{len(df):,}** bản ghi tương ứng bộ lọc hiện tại: "
            f"Sàn: **{filters.get('platform', 'Tất cả')}** | Tháng: **{filters.get('month', 'Tất cả')}**"
        )

    st.markdown("---")

    # 2. TỔNG HỢP THEO THÁNG (Section 11)
    st.subheader("📅 1. Bảng Tổng Hợp Doanh Thu Theo Tháng")
    if not month_summary.empty:
        month_display = month_summary.copy()
        month_display["Doanh Thu (GMV)"] = month_display["revenue"].apply(format_currency_vnd)
        month_display["Hoa Hồng"] = month_display["commission"].apply(format_currency_vnd)
        month_display["Chi Phí Ads"] = month_display["ad_cost"].apply(format_currency_vnd)
        month_display["Lợi Nhuận Ròng"] = month_display["profit"].apply(format_currency_vnd)
        month_display["ROI"] = month_display["roi"].apply(lambda x: f"{x:.2f}x")
        month_display["Tăng Trưởng Doanh Thu"] = month_display["revenue_growth_%"].apply(lambda x: f"{x:+.1f}%")

        st.dataframe(
            month_display[["month", "Doanh Thu (GMV)", "Hoa Hồng", "Chi Phí Ads", "Lợi Nhuận Ròng", "ROI", "Tăng Trưởng Doanh Thu"]].rename(
                columns={"month": "Tháng"}
            ),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.write("Không có dữ liệu theo tháng.")

    # 3. TỔNG HỢP THEO PLATFORM (Section 11)
    st.subheader("🏢 2. Bảng So Sánh Hiệu Quả Các Nền Tảng")
    if not platform_summary.empty:
        plat_display = platform_summary.copy()
        plat_display["Doanh Thu (GMV)"] = plat_display["revenue"].apply(format_currency_vnd)
        plat_display["Hoa Hồng Nhận"] = plat_display["commission"].apply(format_currency_vnd)
        plat_display["Chi Phí Ads"] = plat_display["ad_cost"].apply(format_currency_vnd)
        plat_display["Lợi Nhuận Ròng"] = plat_display["profit"].apply(format_currency_vnd)
        plat_display["ROI"] = plat_display["roi"].apply(lambda x: f"{x:.2f}x")
        plat_display["CR (%)"] = plat_display["cr"].apply(lambda x: f"{x:.2f}%")

        st.dataframe(
            plat_display[["platform", "Doanh Thu (GMV)", "Hoa Hồng Nhận", "Chi Phí Ads", "Lợi Nhuận Ròng", "ROI", "CR (%)"]].rename(
                columns={"platform": "Nền Tảng"}
            ),
            use_container_width=True,
            hide_index=True
        )

    st.markdown("---")

    # 4. BIỂU ĐỒ BÁO CÁO (Section 11: Pie, Bar so sánh lợi nhuận, Line xu hướng)
    st.subheader("📈 3. Biểu Đồ Phân Tích Chuyên Sâu")
    b_col1, b_col2 = st.columns(2)

    with b_col1:
        # Pie chart phân bổ doanh thu theo nền tảng
        fig_pie = create_platform_pie_chart(platform_summary, metric="revenue", title="Phân Bổ Doanh Thu Theo Sàn TMĐT")
        st.plotly_chart(fig_pie, use_container_width=True)

    with b_col2:
        # Bar chart so sánh lợi nhuận giữa các nền tảng
        colors = [FINTECH_COLORS.get(p, "#10B981") for p in platform_summary["platform"]]
        fig_profit_bar = go.Figure(
            go.Bar(
                x=platform_summary["platform"],
                y=platform_summary["profit"],
                text=[format_currency_vnd(v) for v in platform_summary["profit"]],
                textposition="auto",
                marker=dict(color=colors),
                hovertemplate="<b>%{x}</b><br>Lợi nhuận ròng: %{y:,.0f} ₫<extra></extra>"
            )
        )
        fig_profit_bar.update_layout(
            title="So Sánh Lợi Nhuận Ròng Giữa Các Sàn",
            xaxis_title="Nền tảng",
            yaxis_title="Lợi nhuận (VND)",
            template="plotly_white",
            height=380,
            margin=dict(l=40, r=30, t=50, b=40)
        )
        st.plotly_chart(fig_profit_bar, use_container_width=True)

    # Line chart xu hướng doanh thu
    fig_trend = create_revenue_trend_line_chart(month_summary)
    st.plotly_chart(fig_trend, use_container_width=True)
