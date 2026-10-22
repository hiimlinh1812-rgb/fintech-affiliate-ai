"""
AI Forecast & Campaign Optimization Page
Implements Linear Regression forecasting, model evaluation (MAE/RMSE),
rule-based strategic recommendations, and DNN architecture documentation.
Complies with Section 13, 14, 15, 17 of requirements and Chapter 2 of CNDVTC.docx.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from services.analytics import aggregate_by_month, aggregate_by_platform
from services.recommendation import generate_recommendations
from ai.linear_regression import train_and_forecast_monthly_revenue
from ai.dnn_placeholder import get_dnn_architecture_spec
from dashboard.charts import format_currency_vnd


def render_ai_forecast_page(df: pd.DataFrame, filters: dict):
    """Renders the AI Forecast and Campaign Optimization Page."""
    st.markdown("## 🤖 AI Dự Báo Doanh Thu & Gợi Ý Tối Ưu Chiến Dịch")
    st.caption("Ứng dụng Hồi quy tuyến tính (Linear Regression) & Hệ luật chuyên gia (Rule-based AI)")

    st.info(
        "💡 **Ghi chú về tính trung thực của Demo học thuật:**\n"
        "- Mô hình dự báo sử dụng thuật toán **Linear Regression (Scikit-learn)** được huấn luyện trên chuỗi dữ liệu thực tế đang lọc.\n"
        "- Đánh giá mô hình hiển thị đúng giá trị sai số thực nghiệm **MAE, RMSE, R²**.\n"
        "- Các khuyến nghị chiến lược được sinh bởi hệ luật kinh doanh (Rule-based), không giả xưng là Reinforcement Learning."
    )

    if df.empty:
        st.warning("⚠️ Không có dữ liệu để thực hiện dự báo. Vui lòng mở rộng bộ lọc.")
        return

    month_summary = aggregate_by_month(df)
    platform_summary = aggregate_by_platform(df)

    # 1. LINEAR REGRESSION FORECAST SECTION (Section 14)
    st.markdown("### 📈 1. Dự Báo Doanh Thu Tháng Tiếp Theo (Linear Regression)")

    forecast_result = train_and_forecast_monthly_revenue(month_summary)

    if not forecast_result["success"]:
        st.warning(f"⚠️ {forecast_result['message']}")
    else:
        # Display forecast KPI highlights
        next_month = forecast_result["next_month"]
        fc_val = forecast_result["forecast_value"]
        delta_val = forecast_result["monthly_trend_delta"]
        mae = forecast_result["mae"]
        rmse = forecast_result["rmse"]
        r2 = forecast_result["r2"]

        f1, f2, f3, f4 = st.columns(4)
        with f1:
            st.metric(
                label=f"Dự Báo Doanh Thu ({next_month})",
                value=format_currency_vnd(fc_val),
                delta=f"{'+' if delta_val > 0 else ''}{int(delta_val):,} ₫/tháng",
                help="Giá trị dự báo ngoại suy tuyến tính cho tháng kế tiếp"
            )
        with f2:
            st.metric(
                label="Hệ Số Xác Định R²",
                value=f"{r2:.4f}",
                help="Mức độ phù hợp của đường hồi quy tuyến tính với dữ liệu lịch sử"
            )
        with f3:
            st.metric(
                label="Sai Số Tuyệt Đối (MAE)",
                value=format_currency_vnd(mae),
                help="Mean Absolute Error thực tế giữa giá trị quan sát và đường khớp"
            )
        with f4:
            st.metric(
                label="Căn Bậc Hai Sai Số (RMSE)",
                value=format_currency_vnd(rmse),
                help="Root Mean Squared Error thực tế trên tập huấn luyện"
            )

        # Plot Historical vs Fitted vs Forecast
        hist_df = forecast_result["history_df"]
        fig_fc = go.Figure()

        # Actual Historical Line
        fig_fc.add_trace(
            go.Scatter(
                x=hist_df["month"],
                y=hist_df["revenue"],
                mode="lines+markers",
                name="Doanh thu thực tế lịch sử",
                line=dict(color="#2563EB", width=3),
                marker=dict(size=8, symbol="circle"),
                hovertemplate="<b>Tháng %{x}</b><br>Thực tế: %{y:,.0f} ₫<extra></extra>"
            )
        )

        # Fitted Regression Line
        fig_fc.add_trace(
            go.Scatter(
                x=hist_df["month"],
                y=hist_df["fitted_revenue"],
                mode="lines",
                name="Đường khớp hồi quy (Fitted Line)",
                line=dict(color="#10B981", width=2, dash="dash"),
                hovertemplate="Khớp tuyến tính: %{y:,.0f} ₫<extra></extra>"
            )
        )

        # Forecasted Next Month Point
        fig_fc.add_trace(
            go.Scatter(
                x=[next_month],
                y=[fc_val],
                mode="markers+text",
                name=f"Dự báo {next_month}",
                text=[format_currency_vnd(fc_val)],
                textposition="top center",
                marker=dict(color="#EF4444", size=14, symbol="star"),
                hovertemplate=f"<b>Dự báo {next_month}</b>: " + "%{y:,.0f} ₫<extra></extra>"
            )
        )

        # Connect last historical to forecast with a dotted projection line
        fig_fc.add_trace(
            go.Scatter(
                x=[hist_df.iloc[-1]["month"], next_month],
                y=[hist_df.iloc[-1]["fitted_revenue"], fc_val],
                mode="lines",
                name="Khoảng ngoại suy dự báo",
                line=dict(color="#EF4444", width=2, dash="dot"),
                showlegend=False
            )
        )

        fig_fc.update_layout(
            title=f"Đồ Thị Hồi Quy Tuyến Tính & Dự Báo Doanh Thu Tháng {next_month}",
            xaxis_title="Thời gian (Tháng)",
            yaxis_title="Doanh thu (VND)",
            template="plotly_white",
            height=420,
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_fc, use_container_width=True)

    st.markdown("---")

    # 2. STRATEGIC RECOMMENDATIONS (Section 17)
    st.markdown("### 💡 2. Gợi Ý Tối Ưu Hóa Chiến Dịch & Phân Bổ Ngân Sách")
    st.caption("Các đề xuất tự động được tính toán dựa trên quy tắc nghiệp vụ ROI, CR và chi phí quảng cáo")

    recommendations = generate_recommendations(df, platform_summary, month_summary)

    for rec in recommendations:
        box_type = rec.get("type", "info")
        title = rec.get("title", "")
        desc = rec.get("description", "")
        tag = rec.get("tag", "CHIẾN DỊCH")

        if box_type == "success":
            st.success(f"**[{tag}] {title}**\n\n{desc}")
        elif box_type == "warning":
            st.warning(f"**[{tag}] {title}**\n\n{desc}")
        else:
            st.info(f"**[{tag}] {title}**\n\n{desc}")

    st.markdown("---")

    # 3. DNN ARCHITECTURE PLACEHOLDER (Section 15: OPTIONAL / FUTURE EXTENSION)
    st.markdown("### 🧠 3. Thiết Kế Mạng Nơ-ron Học Sâu (DNN) – Hướng Mở Rộng Tương Lai")
    with st.expander("🔍 Xem thông số kiến trúc Deep Neural Network (Future Extension - CNDVTC Mục 2.3.3)"):
        dnn_spec = get_dnn_architecture_spec()
        st.markdown(f"**Trạng thái triển khai:** `{dnn_spec['status']}`")
        st.markdown(f"**Công nghệ:** `{dnn_spec['framework']}` | **Loại mô hình:** `{dnn_spec['model_type']}`")
        st.markdown(f"**Mục đích:** {dnn_spec['purpose']}")

        col_dnn1, col_dnn2 = st.columns(2)
        with col_dnn1:
            st.markdown("**Cấu trúc các lớp (Layers):**")
            st.code(
                "Input Layer (Features chuẩn hóa: Ads, Clicks, Platform, Category, Seasonality)\n"
                "   ↓\n"
                "Hidden Layer 1: Dense(64 units, activation='relu') + Dropout(0.2)\n"
                "   ↓\n"
                "Hidden Layer 2: Dense(32 units, activation='relu') + Dropout(0.1)\n"
                "   ↓\n"
                "Output Layer: Dense(1 unit, activation='linear') [Dự báo Doanh Thu/Lợi Nhuận]",
                language="text"
            )
        with col_dnn2:
            st.markdown("**Thông số huấn luyện đề xuất:**")
            st.write(dnn_spec["training_spec"])
            st.caption(dnn_spec["academic_note"])
