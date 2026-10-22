"""
Fintech Affiliate AI Dashboard - Main Application Entry Point
Based on Academic Report CNDVTC.docx (Banking Academy of Vietnam)
"""

from datetime import datetime, timedelta
import streamlit as st
import pandas as pd

from services.data_loader import (
    load_affiliate_data,
    trigger_simulation_tick,
    check_api_health
)
from dashboard.overview import render_overview_page
from dashboard.revenue_report import render_revenue_report_page
from dashboard.ai_forecast_page import render_ai_forecast_page
from dashboard.chatbot_page import render_chatbot_page
from dashboard.legal_tax_page import render_legal_tax_page

# Page Configuration
st.set_page_config(
    page_title="Fintech Affiliate AI Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for modern Fintech aesthetic
st.markdown(
    """
    <style>
    .main {
        background-color: #F8FAFC;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
        font-weight: 700;
        color: #1E3A8A;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        color: #64748B;
        font-weight: 500;
    }
    .status-badge-online {
        background-color: #DEF7EC;
        color: #03543F;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
    .status-badge-offline {
        background-color: #FEF08A;
        color: #713F12;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def main():
    # SIDEBAR SETUP (Section 7, 21)
    with st.sidebar:
        st.title("🎯 Fintech Affiliate AI")
        st.caption("Nền tảng phân tích & tối ưu chiến dịch cá nhân")

        # System connection status
        api_online = check_api_health()
        if api_online:
            st.markdown(
                '<div class="status-badge-online">🟢 Mock API Đang Kết Nối (8001)</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="status-badge-offline">🟡 Chế Độ Mô Phỏng Độc Lập</div>',
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Simulation Tick Button (Section 12: Cơ chế cập nhật dữ liệu 15 phút)
        if st.button("🔄 Làm mới / Mô phỏng cập nhật API", use_container_width=True, help="Mô phỏng thay đổi thị trường ngẫu nhiên 1.01-1.05"):
            tick_res = trigger_simulation_tick()
            st.success(f"Đã cập nhật: {tick_res.get('message', 'Thành công')}")
            st.rerun()

        st.markdown("---")

        # Navigation
        st.subheader("🧭 Điều Hướng")
        nav_choice = st.radio(
            "Chọn khu vực làm việc:",
            options=[
                "📊 1. Tổng Quan Hiệu Suất",
                "📑 2. Báo Cáo Doanh Thu",
                "🤖 3. AI Dự Báo & Tối Ưu",
                "💬 4. Trợ Lý AI Chatbot",
                "⚖️ 5. Pháp Lý & Thuế"
            ],
            label_visibility="collapsed"
        )

        st.markdown("---")

        # Global Filters (Section 7 & 8)
        st.subheader("🔍 Bộ Lọc Dữ Liệu")

        platform_filter = st.selectbox(
            "Nền tảng (Platform):",
            options=["Tất cả", "Shopee", "Lazada", "TikTok Shop"],
            index=0
        )

        now_dt = datetime.now()
        dynamic_months = ["Tất cả"] + [
            (now_dt - timedelta(days=i*30)).strftime("%Y-%m")
            for i in range(6)
        ]
        # Deduplicate while preserving order
        month_options = []
        for m in dynamic_months:
            if m not in month_options:
                month_options.append(m)

        month_filter = st.selectbox(
            "Tháng (Month):",
            options=month_options,
            index=0
        )

        region_filter = st.selectbox(
            "Khu vực (Region):",
            options=["Tất cả", "Hanoi", "Ho Chi Minh", "Da Nang", "Can Tho", "Hai Phong"],
            index=0
        )

    # LOAD DATA (Tách data processing khỏi UI - Section 24)
    filters_dict = {
        "platform": platform_filter,
        "month": month_filter,
        "region": region_filter
    }

    df, meta = load_affiliate_data(
        platform=platform_filter,
        region=region_filter,
        month=month_filter
    )

    # RENDER VIEW ACCORDING TO NAVIGATION
    if "1. Tổng Quan" in nav_choice:
        render_overview_page(df, filters_dict)
    elif "2. Báo Cáo Doanh Thu" in nav_choice:
        render_revenue_report_page(df, filters_dict)
    elif "3. AI Dự Báo" in nav_choice:
        render_ai_forecast_page(df, filters_dict)
    elif "4. Trợ Lý AI Chatbot" in nav_choice:
        render_chatbot_page(df, filters_dict)
    elif "5. Pháp Lý & Thuế" in nav_choice:
        render_legal_tax_page(df)


if __name__ == "__main__":
    main()
