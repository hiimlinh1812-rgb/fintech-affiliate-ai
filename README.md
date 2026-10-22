# Fintech Affiliate Marketing AI Prototype (Local Academic Demo)

## 1. Giới thiệu đề tài
Hệ thống **"Giải pháp Fintech ứng dụng Trí tuệ Nhân tạo (AI) trong phân tích xu hướng và tối ưu chiến dịch Tiếp thị Liên kết (Affiliate Marketing) cho cá nhân"** được phát triển dưới dạng nguyên mẫu chạy cục bộ (local prototype), phục vụ mục đích trình diễn và nghiên cứu học thuật dựa trên nội dung báo cáo nghiệp vụ `CNDVTC.docx` (Khoa Công nghệ Thông tin & Kinh tế số – Học viện Ngân hàng).

### ⚠️ Cam kết & Giới hạn Nguyên Mẫu (Academic Principles)
- **Dữ liệu hoàn toàn là dữ liệu mô phỏng (Mock Data)**. Không sử dụng dữ liệu người dùng thật.
- **Không kết nối API thật** của Shopee, Lazada, TikTok Shop hay bất kỳ sàn TMĐT nào; không yêu cầu API key thật.
- **Không tích hợp thanh toán thật**, ví điện tử, ngân hàng.
- **Không kết nối cơ quan thuế thật**, không khai/nộp thuế thật.
- **Tính trung thực AI**: Mô hình dự báo sử dụng thuật toán **Linear Regression (Scikit-learn)** với các độ đo sai số thực nghiệm (MAE, RMSE, R²). Chatbot NLP sử dụng cơ chế **TF-IDF + Cosine Similarity** trích xuất sự thật trực tiếp từ dữ liệu đang hiển thị, không bịa đặt số liệu.

---

## 2. Kiến trúc Hệ thống (3 Tầng)

```text
fintech_affiliate_ai/
│
├── app.py                      # Giao diện chính Streamlit & Điều hướng
│
├── api/
│   ├── __init__.py
│   └── mock_api.py             # Máy chủ FastAPI giả lập API Shopee, Lazada, TikTok Shop (Port 8001)
│
├── data/
│   ├── raw/                    # Dữ liệu API thô
│   ├── sample/                 # Dữ liệu JSON mô phỏng đa kênh
│   └── processed/              # Dữ liệu sau khi làm sạch & chuẩn hóa
│
├── services/
│   ├── __init__.py
│   ├── data_loader.py          # Nạp dữ liệu từ FastAPI (hoặc fallback cache tự động)
│   ├── data_cleaner.py         # Làm sạch, chống trùng lặp, chặn doanh thu âm
│   ├── analytics.py            # Phân tích theo Nền tảng, Tháng, Khu vực, Top sản phẩm
│   ├── metrics.py              # Công thức tính ROI, Profit, CR, KPI chuẩn xác
│   ├── reporting.py            # Xuất báo cáo chuyên nghiệp Excel (.xlsx) và PDF (.pdf)
│   └── recommendation.py       # Hệ gợi ý tối ưu chiến dịch (Rule-based)
│
├── ai/
│   ├── __init__.py
│   ├── linear_regression.py    # Huấn luyện mô hình hồi quy tuyến tính & dự báo doanh thu tháng tới
│   ├── dnn_placeholder.py      # Tài liệu đặc tả kiến trúc Deep Neural Network (Future Extension)
│   └── chatbot.py              # Trợ lý NLP hỏi đáp dữ liệu (TF-IDF + Cosine Similarity)
│
├── dashboard/
│   ├── __init__.py
│   ├── overview.py             # Dashboard KPI, biểu đồ Plotly, bảng dữ liệu lọc/tìm kiếm
│   ├── revenue_report.py       # Khu vực Báo cáo doanh thu & Nút Export Excel/PDF
│   ├── ai_forecast_page.py     # Trang AI Dự báo doanh thu & Chiến lược tối ưu
│   ├── chatbot_page.py         # Trang giao diện hội thoại Chatbot tương tác
│   ├── legal_tax_page.py       # Thông tin hướng dẫn pháp lý & chính sách thuế mẫu
│   └── charts.py               # Thư viện biểu đồ tương tác Plotly
│
├── tests/
│   ├── __init__.py
│   ├── test_data.py            # Kiểm thử nạp, làm sạch và xử lý dữ liệu
│   ├── test_metrics.py         # Kiểm thử các công thức tài chính và chia cho 0
│   ├── test_api.py             # Kiểm thử các endpoint FastAPI
│   └── test_ai.py              # Kiểm thử mô hình hồi quy và Chatbot Intent
│
├── requirements.txt            # Danh sách thư viện phụ thuộc
├── README.md                   # Tài liệu hướng dẫn sử dụng
└── .gitignore
```

---

## 3. Hướng dẫn Cài đặt & Khởi chạy

### Bước 1: Cài đặt môi trường
Đảm bảo đã cài đặt Python 3.10 trở lên. Chạy lệnh cài đặt các thư viện:
```bash
pip install -r requirements.txt
```

### Bước 2: Khởi chạy Mock API Server (FastAPI)
Mở một cửa sổ dòng lệnh (Terminal 1) tại thư mục `fintech_affiliate_ai`:
```bash
python -m uvicorn api.mock_api:app --reload --port 8001
```
(hoặc `uvicorn api.mock_api:app --reload --port 8001`)

- API Docs tương tác (Swagger UI): `http://127.0.0.1:8001/docs`
- Endpoint kiểm tra sức khỏe: `http://127.0.0.1:8001/health`
- Endpoints nền tảng:
  - `http://127.0.0.1:8001/api/shopee`
  - `http://127.0.0.1:8001/api/lazada`
  - `http://127.0.0.1:8001/api/tiktok-shop`
  - `http://127.0.0.1:8001/api/refresh` (Mô phỏng thay đổi thị trường sau 15 phút)

### Bước 3: Khởi chạy Web Dashboard (Streamlit)
Mở một cửa sổ dòng lệnh khác (Terminal 2):
```bash
python -m streamlit run app.py
```
(hoặc `streamlit run app.py`)
Ứng dụng sẽ tự động mở trên trình duyệt tại địa chỉ:
```text
http://localhost:8501
```

> **Lưu ý linh hoạt:** Nếu không chạy Mock API server, ứng dụng Streamlit sẽ tự động kích hoạt **Chế độ mô phỏng độc lập (Local Cache Fallback)** để đảm bảo trải nghiệm demo không bao giờ bị gián đoạn hay crash!

---

## 4. Chạy Kiểm Thử Tự Động (Unit Tests)
Để chạy toàn bộ test suite gồm 18 ca kiểm thử:
```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## 5. Các Tính Năng Đã Triển Khai
1. **Thu thập & Giả lập Đa Sàn**: Kết nối FastAPI cho Shopee, Lazada, TikTok Shop.
2. **Cơ chế mô phỏng cập nhật 15 phút**: Nút cập nhật áp dụng biến động thị trường ngẫu nhiên (1.01–1.05) và cập nhật timestamp.
3. **Bộ lọc tương tác Sidebar**: Lọc theo Sàn, Tháng, Khu vực hoặc "Tất cả".
4. **4 KPI Cốt lõi**: Tổng Doanh thu, Tổng Hoa hồng, Tổng Lợi nhuận ròng, ROI trung bình cùng các KPI bổ trợ (Đơn hàng, Lượt nhấp, CR).
5. **Biểu đồ Plotly động**: Bar chart (theo sàn/sản phẩm), Donut pie chart (tỷ trọng doanh thu/hoa hồng), Line chart (xu hướng thời gian), Combo Bar & Line chart (Doanh thu & Lợi nhuận gộp theo thời gian).
6. **Bảng dữ liệu chi tiết**: Đầy đủ 14 cột nghiệp vụ, hỗ trợ tìm kiếm sản phẩm và sắp xếp đa chiều.
7. **Báo cáo Doanh thu & Export**: Trang báo cáo tổng hợp theo tháng và nền tảng; hỗ trợ xuất **Excel (.xlsx)** đa sheet và **PDF (.pdf)** hoàn chỉnh.
8. **AI Dự báo Hồi quy tuyến tính (Linear Regression)**: Dự báo doanh thu tháng tiếp theo, hiển thị MAE, RMSE, R² và đường khớp đồ thị.
9. **Hệ gợi ý chiến lược (Rule-based AI)**: Đề xuất sản phẩm ngôi sao, cảnh báo chi phí quảng cáo cao, tối ưu tỷ lệ chuyển đổi.
10. **Trợ lý Chatbot NLP**: Hỏi đáp tự nhiên về số liệu tài chính trực tiếp từ dashboard hiện hành.
11. **Cẩm nang Pháp lý & Thuế**: Cung cấp thông tin tham khảo về thuế TNCN và chính sách tiếp thị liên kết.
