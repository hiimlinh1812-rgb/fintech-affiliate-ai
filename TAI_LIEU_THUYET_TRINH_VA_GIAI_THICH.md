# TÀI LIỆU GIẢI THÍCH & HƯỚNG DẪN THUYẾT TRÌNH DỰ ÁN
## ĐỀ TÀI: GIẢI PHÁP FINTECH ỨNG DỤNG TRÍ TUỆ NHÂN TẠO (AI) TRONG PHÂN TÍCH XU HƯỚNG VÀ TỐI ƯU CHIẾN DỊCH TIẾP THỊ LIÊN KẾT (AFFILIATE MARKETING) CHO CÁ NHÂN

*Tài liệu dành cho thành viên nhóm nghiên cứu và trình bày báo cáo với Giảng viên hướng dẫn*  
*Học phần: Công nghệ Dịch vụ Tài chính – Khoa CNTT & Kinh tế số, Học viện Ngân hàng*  
*Thời gian thực hiện: Năm học 2026*

---

## MỤC LỤC
1. [Tổng Quan Đề Tài & Bài Toán Thực Tiễn](#1-tổng-quan-đề-tài--bài-toán-thực-tiễn)
2. [Kiến Trúc Kỹ Thuật 3 Lớp (3-Layer Architecture)](#2-kiến-trúc-kỹ-thuật-3-lớp-3-layer-architecture)
3. [Kịch Bản Demo Chi Tiết Từng Tính Năng Trên Web](#3-kịch-bản-demo-chi-tiết-từng-tính-năng-trên-web)
4. [Bộ Câu Hỏi & Trả Lời Phản Biện Của Giảng Viên (Q&A)](#4-bộ-câu-hỏi--trả-lời-phản-biện-của-giảng-viên-qa)
5. [Hướng Dẫn Thao Tác Chạy Ứng Dụng (Cheatsheet)](#5-hướng-dẫn-thao-tác-chạy-ứng-dụng-cheatsheet)

---

## 1. TỔNG QUAN ĐỀ TÀI & BÀI TOÁN THỰC TIỄN

### 1.1. Bối cảnh & Vấn đề thực tế (Pain Points)
Tiếp thị liên kết (Affiliate Marketing) tại Việt Nam đang bùng nổ mạnh mẽ, đặc biệt trên các sàn thương mại điện tử lớn: **Shopee, Lazada, TikTok Shop**. Tuy nhiên, các cá nhân làm affiliate (Publisher / KOC) đang đối mặt với 3 thách thức tài chính lớn:
1. **Dữ liệu phân tán, thiếu cái nhìn tổng thể:** Mỗi sàn có một trang quản trị riêng với cấu trúc báo cáo khác nhau. Người làm affiliate phải tải file Excel từ từng sàn về để tổng hợp thủ công, rất tốn thời gian và dễ nhầm lẫn.
2. **Khó đo lường Lợi nhuận ròng & ROI thực tế:** Các sàn chỉ hiển thị Doanh thu (GMV) và Hoa hồng ước tính, không theo dõi chi phí chạy quảng cáo (Facebook Ads, TikTok Ads, Google Ads). Người làm affiliate không biết chính xác mình đang **lãi hay lỗ** trên từng sản phẩm.
3. **Thiếu công cụ dự báo và tối ưu thông minh:** Quyết định chọn sản phẩm để đẩy số hoặc phân bổ ngân sách quảng cáo chủ yếu dựa vào cảm tính hoặc kinh nghiệm cá nhân mà thiếu vắng các mô hình phân tích dữ liệu và AI hỗ trợ.

### 1.2. Mục tiêu của Giải pháp
Xây dựng một nguyên mẫu **Fintech Dashboard cục bộ** đóng vai trò như một **"Bộ não tài chính" (Financial Brain)**:
- Tự động chuẩn hóa dữ liệu từ các sàn về một hệ quy chuẩn thống nhất.
- Đo lường minh bạch các chỉ số tài chính cốt lõi: **Doanh thu (GMV), Hoa hồng, Chi phí quảng cáo, Lợi nhuận ròng, ROI, Tỷ lệ chuyển đổi (CR)**.
- Ứng dụng Trí tuệ Nhân tạo (Machine Learning & NLP) để **dự báo doanh thu tháng tới**, **gợi ý phân bổ ngân sách**, và hỗ trợ **hỏi đáp tự nhiên qua Chatbot**.

---

## 2. KIẾN TRÚC KỸ THUẬT 3 LỚP (3-LAYER ARCHITECTURE)

Hệ thống được thiết kế phân tầng rõ ràng, đảm bảo tính mô-đun và dễ bảo trì:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        TẦNG 3: HIỂN THỊ & BÁO CÁO                      │
│                  (Streamlit :8501 + Plotly Charts)                     │
│  - Dashboard KPI               - Báo Cáo Doanh Thu (Excel/PDF Export)  │
│  - AI Dự Báo & Gợi Ý Chiến Dịch - Chatbot NLP Hỏi Đáp Tự Nhiên         │
└───────────────────────────────────▲────────────────────────────────────┘
                                    │
┌───────────────────────────────────┴────────────────────────────────────┐
│                    TẦNG 2: PHÂN TÍCH & TRÍ TUỆ NHÂN TẠO                │
│                         (Analytics & AI Layer)                         │
│  - AI Linear Regression: Dự báo doanh số (Scikit-learn, MAE/RMSE/R²)   │
│  - Chatbot NLP Engine: Phân loại ý định TF-IDF + Cosine Similarity     │
│  - Rule-based Engine: Phát hiện sản phẩm ngôi sao, cảnh báo chi phí ads │
│  - Financial Metrics Engine: Tính toán ROI, Net Profit, CR an toàn     │
└───────────────────────────────────▲────────────────────────────────────┘
                                    │
┌───────────────────────────────────┴────────────────────────────────────┐
│                       TẦNG 1: DỮ LIỆU & GIAO TIẾP API                  │
│                             (Data Layer)                               │
│  - Mock API Server (FastAPI :8001): Endpoint Shopee, Lazada, TikTok    │
│  - Cơ chế mô phỏng 15 phút: Tự động cập nhật biến động (1.01 - 1.05)   │
│  - Data Cleaner: Chống trùng lặp, xử lý null, kiểm soát không âm       │
│  - Fallback Cache Engine: Chống crash tuyệt đối nếu tắt API server     │
└────────────────────────────────────────────────────────────────────────┘
```

### Các công nghệ chủ đạo:
- **Ngôn ngữ:** Python 3.12 (tiêu chuẩn khoa học dữ liệu hiện đại).
- **Backend API:** FastAPI + Uvicorn (chuẩn RESTful, thời gian phản hồi ~0.15s).
- **Frontend Dashboard:** Streamlit (tương tác thời gian thực, giao diện chuẩn Fintech).
- **Trực quan hóa:** Plotly Express & Plotly Graph Objects (biểu đồ động, hover xem tiền VND).
- **AI & Học máy:** Scikit-learn (Linear Regression, TF-IDF Vectorizer).
- **Xử lý dữ liệu:** Pandas, NumPy.
- **Kết xuất báo cáo:** OpenPyXL (Excel đa sheet có màu sắc thương hiệu), ReportLab (PDF bảng biểu chuẩn in).

---

## 3. KỊCH BẢN DEMO CHI TIẾT TỪNG TÍNH NĂNG TRÊN WEB

Khi trình chiếu trước giáo viên hoặc chia sẻ với các bạn, hãy dẫn dắt lần lượt qua 5 phân hệ sau:

### 3.1. Thanh Sidebar – Trung tâm Điều khiển & Bộ lọc
- **Huy hiệu trạng thái kết nối:**
  - `🟢 Mock API Đang Kết Nối (8001)`: Báo hiệu hệ thống đang giao tiếp thông suốt với máy chủ FastAPI qua giao thức HTTP.
  - `🟡 Chế Độ Mô Phỏng Độc Lập`: Nếu tắt server FastAPI, ứng dụng tự kích hoạt cache nội bộ, đảm bảo demo không bao giờ bị lỗi.
- **Nút "🔄 Làm mới / Mô phỏng cập nhật API":** Thể hiện cơ chế biến động thị trường sau mỗi 15 phút (Mục 2.3.5 trong báo cáo) – dữ liệu được nhân ngẫu nhiên hệ số `1.01 - 1.05` để mô phỏng sự tăng trưởng doanh số thực tế.
- **Bộ lọc động:** Cho phép lọc theo **Nền tảng** (*Shopee, Lazada, TikTok Shop*), **Tháng** (*2026-05 đến 2026-10*), và **Khu vực**. Khi đổi bộ lọc, toàn bộ số liệu và biểu đồ cập nhật tức thì.

### 3.2. Tab 1: Tổng Quan Hiệu Suất (Overview Dashboard)
- **4 Thẻ KPI Cốt Lõi:**
  - **Tổng Doanh Thu (GMV):** Tổng giá trị đơn hàng khách hàng đã mua qua liên kết.
  - **Tổng Hoa Hồng:** Tiền hoa hồng sàn chi trả cho publisher.
  - **Tổng Lợi Nhuận Ròng:** Tiền túi thực nhận = $\text{Hoa Hồng} - \text{Chi Phí Ads}$.
  - **Hệ Số ROI:** Đo lường hiệu quả vốn quảng cáo = $\frac{\text{Hoa Hồng}}{\text{Chi Phí Ads}}$. (Ví dụ ROI = 2.5 nghĩa là bỏ 1 đồng quảng cáo thu về 2.5 đồng hoa hồng).
- **4 Thẻ KPI Bổ trợ:** Chi Phí Ads, Tổng Đơn Hàng, Tổng Lượt Nhấp, Tỷ Lệ Chuyển Đổi (CR).
- **Hệ Thống Biểu Đồ Plotly Tương Tác:**
  - *Biểu đồ cột (Bar Chart):* So sánh Doanh thu / Hoa hồng / Chi phí ads giữa các sàn.
  - *Biểu đồ tròn (Donut Chart):* Xem tỷ trọng đóng góp của Shopee, Lazada, TikTok Shop.
  - *Biểu đồ đường (Line Chart):* Xu hướng tăng trưởng doanh thu theo tháng.
  - *Biểu đồ kết hợp (Combo Bar & Line Chart):* Cột thể hiện doanh thu, đường thể hiện ROI (chuẩn theo Hình 5 báo cáo CNDVTC).
- **Bảng Dữ Liệu Chiến Dịch Chi Tiết:**
  - Có thanh tìm kiếm theo tên hoặc mã sản phẩm.
  - Có các nút radio sắp xếp theo Doanh thu, Hoa hồng, ROI, Đơn hàng (tăng/giảm dần).

### 3.3. Tab 2: Báo Cáo Doanh Thu (Revenue Report & Export)
- Bảng tổng kết số liệu tài chính theo từng tháng (có tính % tăng trưởng MoM) và theo từng sàn.
- **Hai nút xuất báo cáo:**
  - **Nút "Tải Báo Cáo Excel (.xlsx)":** Tạo file Excel gồm 4 Sheet (*Tổng quan, Theo sàn, Theo tháng, Dữ liệu chi tiết*), định dạng tiêu đề xanh navy sang trọng, căn chỉnh tự động độ rộng cột.
  - **Nút "Tải Báo Cáo PDF (.pdf)":** Tạo văn bản PDF hoàn chỉnh bằng ReportLab với đầy đủ bảng biểu số liệu và phần tuyên bố miễn trừ trách nhiệm học thuật.

### 3.4. Tab 3: AI Dự Báo Doanh Thu & Gợi Ý Chiến Dịch
- **Mô hình Hồi quy Tuyến tính (Linear Regression):**
  - Huấn luyện trên chuỗi 6 tháng gần nhất để ngoại suy dự báo doanh thu cho **tháng kế tiếp (2026-11)**.
  - Trình bày công khai các thước đo sai số thực nghiệm: **MAE** (Sai số tuyệt đối trung bình), **RMSE** (Căn bậc hai sai số trung bình), và **R²** (Hệ số xác định).
  - Vẽ đồ thị gồm 3 thành phần: *Đường doanh thu thực tế lịch sử (Xanh dương)*, *Đường hồi quy khớp fitted line (Xanh lá)*, và *Điểm ngôi sao dự báo tương lai (Đỏ)*.
- **Hệ thống Gợi ý Chiến dịch (Rule-based AI):**
  - Tự động nhận diện *"Sản phẩm ngôi sao"* (ROI cao $\ge 2.5$ + Doanh thu top 25%) để đề xuất tăng ngân sách.
  - Bật cờ *"Cảnh báo chi phí ads"* khi sản phẩm có doanh số cao nhưng ROI thấp ($< 1.3$).
  - Bật cờ *"Tối ưu Landing Page"* khi lượt nhấp (Clicks) cao nhưng tỷ lệ chuyển đổi (CR) thấp.
- **Đặc Tả Kiến Trúc Deep Neural Network (DNN):** Trình bày tài liệu thiết kế mạng nơ-ron nhiều tầng dạng `Future Extension` để trả lời câu hỏi mở rộng của giảng viên.

### 3.5. Tab 4: Trợ Lý AI Chatbot (NLP Assistant)
- Cho phép người dùng gõ câu hỏi bằng tiếng Việt tự nhiên hoặc bấm vào 4 nút câu hỏi gợi ý nhanh.
- Chatbot sử dụng thuật toán **TF-IDF + Cosine Similarity** phân loại đúng 5 nhóm câu hỏi:
  1. *Doanh thu/Lợi nhuận* $\rightarrow$ Đọc trực tiếp thẻ KPI.
  2. *Top sản phẩm* $\rightarrow$ Tìm sản phẩm có doanh thu/ROI cao nhất.
  3. *So sánh sàn* $\rightarrow$ So sánh Shopee vs Lazada vs TikTok Shop.
  4. *Dự báo tương lai* $\rightarrow$ Trích xuất kết quả dự báo từ Linear Regression.
  5. *Tư vấn tối ưu* $\rightarrow$ Trả về danh mục các gợi ý chiến lược.
- **Điểm ưu việt:** Câu trả lời lấy trực tiếp từ dữ liệu thực tế của Dashboard, không gọi OpenAI, không tốn phí và không bao giờ bịa đặt số liệu.

### 3.6. Tab 5: Hỗ Trợ Pháp Lý & Chính Sách Thuế
- Hướng dẫn quy định thuế TNCN tiếp thị liên kết theo **Thông tư 40/2021/TT-BTC** (tạm khấu trừ 10% tại nguồn cho khoản chi trả từ 2.000.000đ trở lên).
- Nhắc nhở các mốc quyết toán thuế quan trọng (31/03 và 30/04).
- Có khung cảnh báo miễn trừ trách nhiệm pháp lý rõ ràng, khẳng định đây là thông tin mẫu, không thay thế cơ quan thuế.

---

## 4. BỘ CÂU HỎI & TRẢ LỜI PHẢN BIỆN CỦA GIẢNG VIÊN (Q&A)

Dưới đây là 5 câu hỏi giảng viên rất hay hỏi khi bảo vệ đồ án/bài kiểm tra và cách trả lời chuẩn nhất:

#### Câu 1: "Tại sao nhóm không kết nối API thật của Shopee, Lazada hay TikTok Shop mà lại dùng Mock API?"
> **Trả lời:**  
> *"Dạ thưa Thầy/Cô, việc sử dụng Mock API là tuân thủ chặt chẽ nguyên tắc nghiên cứu nguyên mẫu (Prototype) vì các lý do sau:*  
> *1. **Chính sách bảo mật & Pháp lý:** Để được cấp Open API chính thức từ Shopee hay TikTok Shop, cá nhân phải có doanh nghiệp đăng ký kinh doanh và được sàn phê duyệt đối tác kỹ thuật (ISV Partner).*  
> *2. **Bảo mật dữ liệu:** Hệ thống demo không được phép lưu trữ thông tin nhạy cảm của người dùng thực tế.*  
> *3. **Kiến trúc mô phỏng tiêu chuẩn:** Server FastAPI của nhóm được xây dựng theo đúng chuẩn RESTful trả về schema JSON chuyên nghiệp. Khi đưa vào môi trường sản xuất thực tế, hệ thống chỉ cần thay thế URL endpoint mà không cần thay đổi bất kỳ logic xử lý hay giao diện nào ở các tầng trên."*

#### Câu 2: "AI trong hệ thống này hoạt động như thế nào? Có phải các em dùng số liệu giả để lừa người xem không?"
> **Trả lời:**  
> *"Dạ thưa Thầy/Cô, nhóm cam kết tính trung thực học thuật 100%:*  
> *- Phần Dự báo doanh thu sử dụng thuật toán **Linear Regression thực tế của thư viện Scikit-learn**. Mô hình trực tiếp học hệ số góc và điểm chặn trên chuỗi 6 tháng lịch sử gần nhất, hiển thị đầy đủ các chỉ số đánh giá sai số thực tế như MAE, RMSE và R².*  
> *- Phần Chatbot sử dụng thuật toán vector hóa văn bản **TF-IDF kết hợp tính độ tương đồng Cosine Similarity**. Chatbot phân tích câu hỏi của người dùng và trích xuất số liệu thực tế từ dữ liệu đang hiển thị trên Dashboard chứ không dùng bất kỳ kịch bản bịa đặt nào."*

#### Câu 3: "Công thức tính ROI của nhóm là gì? Tại sao lại lấy Hoa hồng chia cho Chi phí Ads mà không lấy Doanh thu?"
> **Trả lời:**  
> *"Dạ thưa Thầy/Cô, đây là đặc thù nghiệp vụ cốt lõi của Tiếp thị Liên kết (Affiliate Marketing) phân biệt với Bán hàng trực tiếp (Dropshipping/E-commerce):*  
> *- Doanh thu (GMV) là số tiền người mua hàng trả cho sàn và chủ shop, người làm affiliate **không được nhận khoản này**.*  
> *- Dòng tiền thực tế người làm affiliate nhận về là **Hoa hồng (Commission)**.*  
> *- Chi phí người làm affiliate bỏ ra là **Tiền chạy quảng cáo (Ad Cost)**.*  
> *Do đó, đối với cá nhân làm affiliate, tỷ suất sinh lời thực tế trên vốn đầu tư phải được tính bằng: $\text{ROI} = \frac{\text{Hoa Hồng}}{\text{Chi Phí Quảng Cáo}}$. Chỉ số này cho biết cứ 1 đồng tiền quảng cáo bỏ ra thì thu về được bao nhiêu đồng tiền hoa hồng."*

#### Câu 4: "Cơ chế cập nhật dữ liệu 15 phút được hiện thực như thế nào?"
> **Trả lời:**  
> *"Dạ thưa Thầy/Cô, theo Mục 2.3.5 trong báo cáo, thị trường affiliate luôn biến động theo thời gian. Nhóm hiện thực tính năng này thông qua endpoint `/api/refresh` trên FastAPI và nút bấm trên thanh Sidebar. Khi kích hoạt, hệ thống mô phỏng việc thị trường nhảy số mới bằng cách nhân doanh số với hệ số ngẫu nhiên từ 1.01 đến 1.05, đồng thời cập nhật timestamp mới nhất mà không làm gián đoạn ứng dụng."*

#### Câu 5: "Hệ thống này có gì vượt trội hơn trang quản trị có sẵn của sàn Shopee hay AccessTrade?"
> **Trả lời:**  
> *"Dạ thưa Thầy/Cô, các nền tảng hiện tại có 3 hạn chế lớn:*  
> *1. Dữ liệu bị 'đóng băng' trong từng sàn riêng biệt, không có cái nhìn tổng hợp đa kênh.*  
> *2. Không cho phép nhập và trừ đi chi phí quảng cáo bên ngoài để tính Lợi nhuận ròng cá nhân.*  
> *3. Không tích hợp AI dự báo xu hướng chuỗi thời gian và không có trợ lý phân tích ngôn ngữ tự nhiên.*  
> *Hệ thống của nhóm khắc phục trọn vẹn cả 3 điểm này trong một giao diện duy nhất."*

---

## 5. HƯỚNG DẪN THAO TÁC CHẠY ỨNG DỤNG (CHEATSHEET)

### Yêu cầu tiên quyết:
- Đã cài Python 3.10 trở lên trên máy tính.

### Các lệnh thực thi trong Terminal:

```powershell
# Di chuyển vào thư mục dự án
cd C:\Users\Admin\.gemini\antigravity\scratch\fintech_affiliate_ai

# 1. Cài đặt các thư viện cần thiết (chỉ chạy lần đầu)
pip install -r requirements.txt

# 2. Khởi chạy Mock API Server (Terminal 1)
python -m uvicorn api.mock_api:app --reload --port 8001

# 3. Khởi chạy Giao diện Dashboard (Terminal 2)
python -m streamlit run app.py

# 4. Chạy kiểm thử tự động toàn bộ 18 ca test
python -m unittest discover -s tests -p "test_*.py"
```

- **Địa chỉ truy cập Web:** [http://localhost:8501](http://localhost:8501)
- **Địa chỉ Swagger API Docs:** [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)
