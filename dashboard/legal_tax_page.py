"""
Legal & Tax Information Page
Provides educational guidelines, regulatory policies, and interactive tax calculation
aligned with Law on Personal Income Tax No. 109/2025/QH15 and Law on E-Commerce No. 122/2025/QH15.
Complies with Section 1.1.2 of revised research objectives.
"""

import streamlit as st
import pandas as pd


def render_legal_tax_page(df: pd.DataFrame = None, *args, **kwargs):
    """Renders educational information and simulation for tax obligations."""
    if df is None:
        try:
            from services.data_loader import load_affiliate_data
            df, _ = load_affiliate_data()
        except Exception:
            df = pd.DataFrame()
    st.markdown("## ⚖️ Hỗ Trợ Pháp Lý & Module Cảnh Báo Thuế TNCN")
    st.caption("Căn cứ theo Luật Thuế TNCN số 109/2025/QH15 và Luật Thương mại điện tử số 122/2025/QH15")

    st.warning(
        "⚠️ **TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM PHÁP LÝ (LEGAL DISCLAIMER):**\n\n"
        "Các nội dung dưới đây và công cụ tính toán chỉ mang tính chất **mô phỏng, hỗ trợ phân tích và giáo dục học thuật**, "
        "dựa trên các ngưỡng quy định mới của **Luật Thuế TNCN số 109/2025/QH15** và **Luật TMĐT số 122/2025/QH15**.\n"
        "Hệ thống **KHÔNG PHẢI là cơ quan thuế chính thức**, **KHÔNG tự động kê khai hay nộp thuế thay người dùng**, "
        "và **KHÔNG kết nối trực tiếp với cổng thông tin Tổng cục Thuế**.\n\n"
        "Người làm Affiliate cần liên hệ trực tiếp với cơ quan thuế quản lý hoặc chuyên gia kế toán để được hướng dẫn quyết toán theo hồ sơ thực tế."
    )

    st.markdown("---")

    # 1. LIVE TAX SIMULATION & ALERT MODULE (Mục tiêu 1.1.2)
    st.subheader("🧮 1. Module Mô Phỏng & Cảnh Báo Nghĩa Vụ Thuế TNCN Tự Động")
    st.caption("Hệ thống tự động tính toán nghĩa vụ thuế tạm tính dựa trên số liệu hoa hồng đang lọc trên Dashboard")

    total_commission = float(df["commission"].sum()) if (df is not None and not df.empty and "commission" in df.columns) else 0.0
    total_revenue = float(df["revenue"].sum()) if (df is not None and not df.empty and "revenue" in df.columns) else 0.0

    t_col1, t_col2, t_col3 = st.columns(3)
    with t_col1:
        st.metric(
            label="Tổng Hoa Hồng Nhận Được",
            value=f"{int(total_commission):,} ₫",
            help="Thu nhập chịu thuế từ hoạt động dịch vụ tiếp thị liên kết"
        )

    # Tax calculation based on withholding rule (10% withholding at source for service commissions)
    estimated_tax_withheld = int(total_commission * 0.10)
    net_commission_after_tax = int(total_commission - estimated_tax_withheld)

    with t_col2:
        st.metric(
            label="Thuế TNCN Tạm Khấu Trừ (10%)",
            value=f"{estimated_tax_withheld:,} ₫",
            help="Khoản thuế các sàn TMĐT (Shopee, Lazada, TikTok Shop) tạm khấu trừ tại nguồn theo Luật 109/2025/QH15 và Luật TMĐT 122/2025/QH15"
        )

    with t_col3:
        st.metric(
            label="Hoa Hồng Thực Nhận Sau Thuế",
            value=f"{net_commission_after_tax:,} ₫",
            delta=f"Biên thực nhận: {((total_commission - estimated_tax_withheld)/total_commission*100):.0f}%" if total_commission > 0 else "0%",
            help="Thu nhập khả dụng thực tế sau khi sàn hoàn thành khấu trừ thuế tại nguồn"
        )

    # Compliance Alert Banner
    if total_commission > 100_000_000:
        st.warning(
            f"🔔 **CẢNH BÁO NGHĨA VỤ THUẾ (Luật 109/2025/QH15 & Luật TMĐT 122/2025/QH15):**\n\n"
            f"Thu nhập hoa hồng tích lũy của bạn đạt **{int(total_commission):,} ₫** (vượt ngưỡng 100 triệu đồng/năm). "
            f"Bạn thuộc diện bắt buộc phải tổng hợp chứng từ khấu trừ thuế TNCN điện tử từ các sàn để thực hiện **Quyết toán thuế TNCN cuối năm** trước ngày 30/04."
        )
    else:
        st.info(
            f"ℹ️ **TRẠNG THÁI NGHĨA VỤ THUẾ:**\n\n"
            f"Thu nhập hoa hồng hiện tại là **{int(total_commission):,} ₫**. Các sàn TMĐT đã tự động thực hiện khấu trừ tạm tính 10% tại nguồn theo từng kỳ đối soát. "
            f"Hãy lưu giữ các chứng từ khấu trừ điện tử gửi qua email từ Shopee, Lazada và TikTok Shop."
        )

    st.markdown("---")

    # 2. LEGAL FRAMEWORK DETAILS
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📚 2. Khung Pháp Lý Mới Nhất Cho Tiếp Thị Liên Kết")
        st.markdown(
            """
            - **Luật Thuế TNCN số 109/2025/QH15:**
              - Quy định rõ thu nhập từ hoạt động tiếp thị liên kết, livestream bán hàng hưởng hoa hồng là thu nhập từ tiền lương, tiền công hoặc dịch vụ kinh doanh trực tuyến.
              - Nâng cao tính tự động hóa trong quản lý thuế đối với kinh tế số; xác định rõ trách nhiệm của cá nhân trong việc kê khai bổ sung nếu có nhiều nguồn thu nhập cùng lúc từ nhiều nền tảng.
            - **Luật Thương mại điện tử số 122/2025/QH15:**
              - Quy định rõ trách nhiệm của chủ quản sàn giao dịch TMĐT (Shopee, Lazada, TikTok Shop) trong việc:
                1. Khấu trừ, kê khai và nộp thuế thay cho cá nhân kinh doanh / cá nhân làm tiếp thị liên kết.
                2. Cung cấp dữ liệu giao dịch định kỳ cho cơ quan quản lý nhà nước qua cổng điện tử.
                3. Xuất chứng từ khấu trừ thuế điện tử cho cá nhân làm căn cứ quyết toán thuế.
            """
        )

        st.subheader("🗓️ 3. Các Mốc Quyết Toán & Lưu Ý Thực Tiễn")
        st.markdown(
            """
            - **Ngày 31/03:** Hạn cuối sàn TMĐT cấp chứng từ khấu trừ thuế TNCN điện tử cho cá nhân.
            - **Ngày 30/04:** Hạn cuối nộp hồ sơ tự quyết toán thuế TNCN đối với cá nhân có thu nhập vãng lai từ nhiều sàn.
            - **Xử lý hoàn thuế:** Nếu trong năm mức giảm trừ gia cảnh hoặc chi phí hợp lý lớn hơn số thuế đã tạm khấu trừ 10%, bạn có quyền nộp đơn xin hoàn lại tiền thuế đã nộp thừa trực tiếp trên ứng dụng eTax Mobile.
            """
        )

    with col2:
        st.subheader("🛡️ 4. Quy Định Cộng Đồng & Chống Gian Lận (Anti-Fraud)")
        st.markdown(
            """
            - **Shopee Affiliate Program:**
              - Nghiêm cấm hành vi tự đặt hàng qua link affiliate của chính mình (Self-referral fraud).
              - Không được dùng các kỹ thuật spam link, cookie stuffing hoặc bid từ khóa nhãn hiệu trái phép.
            - **TikTok Shop Creator/Affiliate:**
              - Bắt buộc gắn nhãn nội dung được tài trợ / liên kết thương mại theo quy định minh bạch thông tin của Luật TMĐT 122/2025/QH15.
              - Nghiêm cấm quảng bá sản phẩm không rõ nguồn gốc xuất xứ hoặc thổi phồng công dụng.
            - **Lazada Affiliate Program:**
              - Đảm bảo tuân thủ bản quyền hình ảnh merchant và quy định tỷ lệ hoa hồng từng ngành hàng.
            """
        )

        st.subheader("💡 5. Khuyến Nghị Quản Lý Tài Chính & Dòng Tiền")
        st.markdown(
            """
            1. **Tách biệt dòng tiền:** Mở tài khoản ngân hàng riêng biệt phục vụ thu nhập Affiliate và chi phí quảng cáo.
            2. **Thu thập hóa đơn điện tử hợp lệ:** Yêu cầu hóa đơn GTGT khi chi tiền cho Facebook Ads, Google Ads, TikTok Ads để làm căn cứ giải trình chi phí.
            3. **Theo dõi ROI thực sau thuế:** Luôn tính toán hệ số sinh lời trên cơ sở hoa hồng thực nhận sau khi đã tạm trừ 10% thuế TNCN.
            """
        )
