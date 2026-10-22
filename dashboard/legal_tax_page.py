"""
Legal & Tax Information Page
Provides educational guidelines and regulatory policies for Affiliate Marketing in Vietnam.
Complies with Section 18 of requirements and Section 1.3.5 of CNDVTC.docx.
Includes prominent academic disclaimers.
"""

import streamlit as st


def render_legal_tax_page():
    """Renders educational information regarding taxes and affiliate compliance."""
    st.markdown("## ⚖️ Hỗ Trợ Pháp Lý & Chính Sách Thuế Affiliate")
    st.caption("Thông tin mẫu và cẩm nang tuân thủ nghĩa vụ thuế cho cá nhân làm tiếp thị liên kết")

    st.warning(
        "⚠️ **TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM PHÁP LÝ (LEGAL DISCLAIMER):**\n\n"
        "Các nội dung dưới đây chỉ mang tính chất **thông tin tham khảo và giáo dục học thuật**, "
        "được tổng hợp từ các quy định pháp luật hiện hành tại Việt Nam. "
        "Hệ thống **KHÔNG PHẢI là văn phòng tư vấn pháp lý**, **KHÔNG tự động khai báo hay nộp thuế thay cho người dùng**, "
        "và **KHÔNG kết nối trực tiếp với cổng thông tin Tổng cục Thuế**.\n\n"
        "Người làm Affiliate cần liên hệ trực tiếp với cơ quan thuế địa phương hoặc chuyên gia kế toán để được hướng dẫn cụ thể theo trường hợp cá nhân."
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📚 1. Quy Định Thuế Tiếp Thị Liên Kết Cá Nhân")
        st.markdown(
            """
            Theo quy định của Luật Quản lý Thuế và **Thông tư 40/2021/TT-BTC**:
            
            - **Thuế Thu Nhập Cá Nhân (TNCN):**
              - Khoản thu nhập hoa hồng từ các sàn thương mại điện tử (Shopee, Lazada, TikTok Shop) được coi là tiền công, tiền thù lao từ hoạt động kinh doanh/dịch vụ.
              - Nếu cá nhân cư trú không ký hợp đồng lao động hoặc hợp đồng dịch vụ dưới 3 tháng có mức chi trả từ **2.000.000 đồng/lần trở lên**, sàn thường khấu trừ tạm tính **10%** trước khi chuyển tiền hoa hồng.
            - **Hộ Kinh Doanh Cá Thể:**
              - Trường hợp cá nhân đăng ký kinh doanh ngành tiếp thị liên kết: Nếu tổng doanh thu trong năm dương lịch từ **100 triệu đồng trở xuống** thì thuộc diện không phải nộp thuế GTGT và thuế TNCN.
              - Nếu doanh thu trên 100 triệu đồng/năm: Áp dụng tỷ lệ thuế GTGT (5%) và thuế TNCN (2%) trên tổng doanh thu dịch vụ.
            """
        )

        st.subheader("🗓️ 2. Các Mốc Thời Gian Quan Trọng Cần Lưu Ý")
        st.markdown(
            """
            - **Ngày 31/03:** Hạn cuối quyết toán thuế TNCN đối với tổ chức, cá nhân ủy quyền quyết toán.
            - **Ngày 30/04:** Hạn cuối quyết toán thuế TNCN đối với cá nhân trực tiếp quyết toán thuế với cơ quan thuế.
            - **Chứng từ khấu trừ thuế:** Hãy yêu cầu các sàn TMĐT cung cấp chứng từ điện tử khấu trừ thuế TNCN vào cuối năm tài chính để làm thủ tục hoàn thuế nếu nộp thừa.
            """
        )

    with col2:
        st.subheader("🛡️ 3. Chính Sách Cộng Đồng Của Các Sàn TMĐT")
        st.markdown(
            """
            - **Shopee Affiliate Program:**
              - Nghiêm cấm hành vi tự đặt hàng qua link affiliate của chính mình (Self-referral fraud).
              - Không được dùng các kỹ thuật spam link, cookie stuffing hoặc mua từ khóa thương hiệu "Shopee" trên Google Ads mà không được phép.
            - **TikTok Shop Affiliate:**
              - Tuân thủ chính sách tiêu chuẩn cộng đồng video, gắn nhãn nội dung trả phí / liên kết rõ ràng.
              - Nghiêm cấm các video giật gân, thông tin sai sự thật về công dụng sản phẩm.
            - **Lazada Affiliate:**
              - Tuân thủ quy định về hình ảnh bản quyền và khuyến mãi chính hãng.
            """
        )

        st.subheader("📖 4. Cẩm Nang Tối Ưu Quản Lý Tài Chính Cho Cá Nhân")
        st.markdown(
            """
            1. **Tách biệt tài khoản ngân hàng:** Dùng riêng một tài khoản ngân hàng cho các dòng tiền Affiliate (hoa hồng nhận về và chi phí chạy quảng cáo).
            2. **Lưu trữ hóa đơn quảng cáo:** Tải đầy đủ hóa đơn GTGT điện tử từ Meta Ads, Google Ads, TikTok Ads để làm căn cứ hạch toán chi phí hợp lệ nếu mở hộ kinh doanh.
            3. **Theo dõi tỷ lệ ROI thực sau thuế:** Tính toán biên lợi nhuận ròng có trừ đi khoản tạm khấu trừ thuế TNCN 10%.
            """
        )
