"""
Chatbot NLP Assistant Page
Provides conversational query interface for financial and performance questions.
Complies with Section 16 of requirements and Section 1.3.7, 2.3.4 of CNDVTC.docx.
"""

import streamlit as st
import pandas as pd

from services.analytics import aggregate_by_month
from ai.chatbot import AffiliateChatbotAssistant


@st.cache_resource
def get_chatbot_instance() -> AffiliateChatbotAssistant:
    """Caches chatbot NLP vectorizer and intent corpus."""
    return AffiliateChatbotAssistant()


def render_chatbot_page(df: pd.DataFrame, filters: dict):
    """Renders the interactive AI Assistant conversational interface."""
    st.markdown("## 💬 Trợ Lý AI Phân Tích Dữ Liệu (Fintech NLP Assistant)")
    st.caption("Nguyên mẫu trợ lý hỏi đáp tự nhiên dựa trên dữ liệu thời gian thực của Dashboard")

    st.info(
        "🤖 **Cơ chế hoạt động:** Trợ lý sử dụng kỹ thuật xử lý ngôn ngữ tự nhiên "
        "**TF-IDF + Cosine Similarity** để phân loại ý định người dùng và trích xuất câu trả lời "
        "trực tiếp từ tập dữ liệu đang lọc. Không gọi API bên thứ ba, không bịa đặt số liệu."
    )

    chatbot = get_chatbot_instance()
    month_summary = aggregate_by_month(df)

    # Initialize chat history in session state
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": (
                    "Xin chào! Tôi là **Trợ lý Fintech Affiliate**. "
                    "Tôi có thể giúp bạn kiểm tra doanh thu, tìm sản phẩm bán chạy, "
                    "so sánh sàn Shopee/Lazada/TikTok Shop hoặc dự đoán doanh thu tháng tới. "
                    "Bạn muốn hỏi gì hôm nay?"
                )
            }
        ]

    # Sample prompt buttons
    st.markdown("**Gợi ý câu hỏi nhanh:**")
    q_col1, q_col2, q_col3, q_col4 = st.columns(4)

    prompt_to_send = None
    with q_col1:
        if st.button("📊 Doanh thu hiện tại?", key="btn_q1", use_container_width=True):
            prompt_to_send = "Doanh thu tháng này là bao nhiêu?"
    with q_col2:
        if st.button("🏆 Top sản phẩm bán chạy?", key="btn_q2", use_container_width=True):
            prompt_to_send = "Sản phẩm nào bán tốt nhất?"
    with q_col3:
        if st.button("🏢 So sánh các sàn?", key="btn_q3", use_container_width=True):
            prompt_to_send = "So sánh hiệu quả giữa Shopee và Lazada?"
    with q_col4:
        if st.button("📈 Dự đoán tháng tới?", key="btn_q4", use_container_width=True):
            prompt_to_send = "Dự đoán doanh thu tháng tới?"

    # Display existing chat messages
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle user text input
    user_input = st.chat_input("Nhập câu hỏi của bạn tại đây...")
    query = prompt_to_send or user_input

    if query:
        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        # Generate response
        response = chatbot.answer_query(query, df, month_summary)
        answer_text = response["answer"]

        # Append metadata
        intent_tag = f"\n\n*(Ý định nhận diện: `{response['intent']}` - Độ tin cậy: {response['confidence']*100:.0f}%)*"
        full_answer = answer_text + intent_tag

        st.session_state.chat_messages.append({"role": "assistant", "content": full_answer})
        with st.chat_message("assistant"):
            st.markdown(full_answer)
            st.caption(response["disclaimer"])
