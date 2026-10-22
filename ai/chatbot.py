"""
Chatbot AI / NLP Assistant Module (Prototype)
Answers natural language queries using TF-IDF, Cosine Similarity, and dynamic data binding.
Complies with Section 16 of requirements and Section 1.3.7, 2.3.4 of CNDVTC.docx.
Extracts facts strictly from active dashboard data without fabricating numbers.
"""

import re
from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from services.metrics import compute_kpis
from services.analytics import aggregate_by_platform, get_top_products
from ai.linear_regression import train_and_forecast_monthly_revenue


# Intent training corpus with representative Vietnamese phrases
INTENT_SAMPLES = {
    "revenue_query": [
        "doanh thu tháng này là bao nhiêu",
        "tổng doanh thu hiện tại",
        "tổng hoa hồng nhận được là bao nhiêu",
        "tình hình doanh số và lợi nhuận",
        "tổng tiền hoa hồng và chi phí quảng cáo",
        "cho tôi biết doanh thu",
        "báo cáo doanh thu và hoa hồng"
    ],
    "product_comparison": [
        "sản phẩm nào bán tốt nhất",
        "top sản phẩm bán chạy",
        "sản phẩm nào có doanh thu cao nhất",
        "mặt hàng nào có hoa hồng cao nhất",
        "sản phẩm nào có roi cao nhất",
        "đánh giá hiệu quả từng sản phẩm",
        "sản phẩm hot nhất hiện nay"
    ],
    "platform_comparison": [
        "nền tảng nào đang có doanh thu cao nhất",
        "so sánh shopee và lazada",
        "tiktok shop có hiệu quả không",
        "sàn nào có roi tốt nhất",
        "sàn nào mang lại nhiều hoa hồng nhất",
        "so sánh các sàn thương mại điện tử",
        "tỷ trọng doanh số giữa shopee và tiktok"
    ],
    "forecast_query": [
        "dự đoán doanh thu tháng tới",
        "dự báo doanh số tháng sau",
        "xu hướng doanh thu trong tương lai",
        "tháng tới có tăng trưởng không",
        "mô hình ai dự đoán thế nào",
        "dự báo hoa hồng tháng tiếp theo"
    ],
    "campaign_recommendation": [
        "nên tập trung vào sản phẩm nào",
        "gợi ý tối ưu chiến dịch",
        "cần cắt giảm chi phí quảng cáo ở đâu",
        "làm sao để tăng roi",
        "chiến lược phân bổ ngân sách marketing",
        "tư vấn chiến dịch affiliate hiệu quả"
    ]
}


class AffiliateChatbotAssistant:
    """
    Academic NLP Assistant using TF-IDF and live dashboard data binding.
    """

    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.corpus_texts = []
        self.corpus_intents = []

        for intent, phrases in INTENT_SAMPLES.items():
            for phrase in phrases:
                self.corpus_texts.append(self._preprocess(phrase))
                self.corpus_intents.append(intent)

        self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus_texts)

    def _preprocess(self, text: str) -> str:
        """Simple text normalization for Vietnamese queries."""
        text = text.lower().strip()
        text = re.sub(r"[^\w\s]", " ", text)
        return re.sub(r"\s+", " ", text)

    def identify_intent(self, query: str) -> Tuple[str, float]:
        """Classifies user intent using Cosine Similarity on TF-IDF vectors."""
        clean_q = self._preprocess(query)
        if not clean_q:
            return "unknown", 0.0

        q_vec = self.vectorizer.transform([clean_q])
        similarities = cosine_similarity(q_vec, self.tfidf_matrix)[0]

        best_idx = int(np.argmax(similarities))
        best_score = float(similarities[best_idx])

        # Keyword boost heuristics
        if any(w in clean_q for w in ["dự đoán", "dự báo", "tháng tới", "tháng sau", "tương lai"]):
            return "forecast_query", max(best_score, 0.75)
        if any(w in clean_q for w in ["so sánh", "shopee", "lazada", "tiktok", "sàn nào", "nền tảng"]):
            return "platform_comparison", max(best_score, 0.75)
        if any(w in clean_q for w in ["sản phẩm", "bán chạy", "top", "mặt hàng"]):
            return "product_comparison", max(best_score, 0.75)
        if any(w in clean_q for w in ["gợi ý", "tối ưu", "ngân sách", "lời khuyên", "chiến dịch", "chiến lược"]):
            return "campaign_recommendation", max(best_score, 0.75)
        if any(w in clean_q for w in ["doanh thu", "hoa hồng", "lợi nhuận", "tiền"]):
            return "revenue_query", max(best_score, 0.75)

        if best_score < 0.2:
            return "unknown", best_score

        return self.corpus_intents[best_idx], best_score

    def answer_query(self, query: str, df: pd.DataFrame, month_summary: pd.DataFrame) -> Dict[str, Any]:
        """Generates dynamic, fact-based answers from active data."""
        intent, confidence = self.identify_intent(query)
        kpis = compute_kpis(df)
        plat_summary = aggregate_by_platform(df)
        top_prods = get_top_products(df, top_n=5)

        if df.empty:
            return {
                "intent": intent,
                "confidence": round(confidence, 2),
                "answer": "Hiện tại không có dữ liệu phù hợp với bộ lọc đã chọn để trả lời câu hỏi của bạn. Vui lòng kiểm tra lại bộ lọc.",
                "disclaimer": "Prototype NLP Assistant (Data-Bound)"
            }

        if intent == "revenue_query":
            answer = (
                f"📊 **Báo cáo Doanh thu & Lợi nhuận:**\n"
                f"- **Tổng doanh thu (GMV):** {int(kpis['total_revenue']):,} VND\n"
                f"- **Tổng hoa hồng thực nhận:** {int(kpis['total_commission']):,} VND\n"
                f"- **Tổng chi phí quảng cáo:** {int(kpis['total_ad_cost']):,} VND\n"
                f"- **Lợi nhuận ròng của bạn:** {int(kpis['total_profit']):,} VND\n"
                f"- **ROI trung bình:** {kpis['avg_roi']:.2f}x\n"
                f"- **Tổng đơn hàng:** {kpis['total_orders']:,} đơn (Tỷ lệ chuyển đổi: {kpis['conversion_rate']}%)"
            )

        elif intent == "product_comparison":
            if not top_prods.empty:
                top_1 = top_prods.iloc[0]
                answer = (
                    f"🏆 **Sản phẩm dẫn đầu doanh số:**\n"
                    f"- **Tên sản phẩm:** {top_1['product_name']}\n"
                    f"- **Nền tảng:** {top_1['platform']} ({top_1['category']})\n"
                    f"- **Doanh thu:** {int(top_1['revenue']):,} VND\n"
                    f"- **Hoa hồng mang lại:** {int(top_1['commission']):,} VND\n"
                    f"- **Hệ số ROI:** {top_1['roi']:.2f}x\n\n"
                    f"Các sản phẩm tiếp theo trong top 3 gồm: "
                    + ", ".join([f"**{r['product_name'][:25]}** ({int(r['revenue']):,} ₫)" for _, r in top_prods.iloc[1:3].iterrows()])
                )
            else:
                answer = "Chưa có đủ dữ liệu sản phẩm để xếp hạng."

        elif intent == "platform_comparison":
            if not plat_summary.empty:
                lines = ["🏢 **So sánh hiệu quả giữa các sàn TMĐT:**"]
                for _, r in plat_summary.iterrows():
                    lines.append(
                        f"- **{r['platform']}:** Doanh thu: {int(r['revenue']):,} VND | "
                        f"Hoa hồng: {int(r['commission']):,} VND | ROI: {r['roi']:.2f}x"
                    )
                top_p = plat_summary.iloc[0]
                lines.append(f"\n💡 **Nhận xét:** Sàn **{top_p['platform']}** đang đóng góp lớn nhất vào thu nhập của bạn.")
                answer = "\n".join(lines)
            else:
                answer = "Chưa có dữ liệu nền tảng."

        elif intent == "forecast_query":
            forecast = train_and_forecast_monthly_revenue(month_summary)
            if forecast.get("success"):
                answer = (
                    f"📈 **Dự báo Doanh thu Tháng Kế Tiếp ({forecast['next_month']}):**\n"
                    f"- **Doanh thu dự báo:** ~{int(forecast['forecast_value']):,} VND\n"
                    f"- **Xu hướng:** {forecast['trend_direction']} "
                    f"({'+' if forecast['monthly_trend_delta'] > 0 else ''}{int(forecast['monthly_trend_delta']):,} ₫/tháng)\n"
                    f"- **Độ tin cậy mô hình:** R² = {forecast['r2']:.2f} | MAE = {int(forecast['mae']):,} VND\n"
                    f"*(Dự báo bằng mô hình Scikit-learn Linear Regression trên chuỗi lịch sử)*"
                )
            else:
                answer = f"⚠️ {forecast.get('message', 'Không đủ dữ liệu lịch sử để dự báo.')}"

        elif intent == "campaign_recommendation":
            from services.recommendation import generate_recommendations
            recs = generate_recommendations(df, plat_summary, month_summary)
            lines = ["💡 **Gợi ý Tối ưu Chiến dịch từ Hệ thống (Rule-based AI):**"]
            for idx, r in enumerate(recs[:3], 1):
                lines.append(f"**{idx}. [{r['tag']}] {r['title']}**\n   {r['description']}")
            answer = "\n\n".join(lines)

        else:
            answer = (
                "👋 Tôi là **Trợ lý Phân tích Fintech Affiliate** (Prototype NLP Assistant).\n\n"
                "Bạn có thể hỏi tôi về:\n"
                "- Doanh thu và hoa hồng hiện tại\n"
                "- Sản phẩm nào bán tốt nhất\n"
                "- So sánh hiệu quả Shopee, Lazada và TikTok Shop\n"
                "- Dự báo doanh thu tháng tới bằng Linear Regression\n"
                "- Gợi ý tối ưu chi phí quảng cáo và chiến lược kinh doanh"
            )

        return {
            "intent": intent,
            "confidence": round(confidence, 2),
            "answer": answer,
            "disclaimer": "Dữ liệu được trích xuất trực tiếp từ Dashboard hiện tại. Mô hình demo học thuật."
        }
