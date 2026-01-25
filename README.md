# 🤖 HaUI Smart Assistant: Agentic RAG System
> **Framework nghiên cứu và triển khai Chatbot thông minh hỗ trợ giải đáp quy chế đào tạo tại Trường Đại học Công nghiệp Hà Nội.**

[![Framework](https://img.shields.io/badge/Architecture-Agentic--RAG-blue.svg)](#)
[![LLM](https://img.shields.io/badge/LLM-OpenAI%20%7C%20Ollama%20%7C%20Gemini-green.svg)](#)
[![Retrieval](https://img.shields.io/badge/Search-Hybrid--7%3A3-orange.svg)](#)
[![OCR](https://img.shields.io/badge/OCR-Paddle%20%7C%20Docling-red.svg)](#)

---

## 📖 Mục tiêu dự án
Dự án tập trung vào việc xây dựng một hệ thống **Retrieval-Augmented Generation (RAG)** tiên tiến, có khả năng tự điều hướng (**Agentic**) để xử lý các tài liệu quy phạm pháp luật và đào tạo phức tạp. Hệ thống không chỉ trả lời các câu hỏi thông thường mà còn có khả năng trích xuất chính xác các phụ lục, biểu mẫu và tự học các từ chuyên môn đặc thù của HaUI.

---

## 🌟 Đặc điểm kỹ thuật nổi bật

### 1. Kiến trúc Agentic Đa tầng
Hệ thống sử dụng một chuỗi các tác nhân thông minh (Agents) để xử lý yêu cầu:
- **Router**: Phân loại ý định người dùng (Hỏi đáp, Chào hỏi, Dạy từ viết tắt, Trích xuất tài liệu).
- **Rewriter**: Tinh chỉnh câu hỏi dựa trên lịch sử hội thoại để tăng độ chính xác tìm kiếm.
- **Grader & Reranker**: Đánh giá và sắp xếp lại tài liệu để đảm bảo thông tin phù hợp nhất được đưa vào mô hình ngôn ngữ.
- **Hallucination Checker**: Kiểm tra tính thực tế để đảm bảo câu trả lời hoàn toàn dựa trên bằng chứng từ tài liệu.

### 2. Xử lý tài liệu chuyên sâu
- **Legal-specific Chunking**: Chia tài liệu theo logic "Điều/Khoản/Phụ lục" giúp bảo toàn ngữ cảnh pháp lý tuyệt đối.
- **Hybrid Retrieval**: Kết hợp Search ngữ nghĩa (Vector) và Search từ khóa (BM25) theo tỉ lệ vàng 7:3.
- **Advanced OCR Pipeline**: Tích hợp PaddleOCR và Docling để xử lý chính xác các văn bản scan, bảng biểu phức tạp.

---

## 🏗️ Kiến trúc hệ thống (High-Level Architecture)

```mermaid
graph TB
    User[👤 Người dùng] --> UI[Gradio Web UI]
    UI --> Router{Router Agent}
    
    %% Branching logic
    Router -->|Greeting/OOS| Gen[Direct Response]
    Router -->|Learn Slang| Slang[Slang Manager]
    Router -->|Q&A| Pipeline[Agentic Pipeline]

    subgraph "🤖 Agentic RAG Pipeline"
        Pipeline --> Rewriter[Query Rewriter]
        Rewriter --> Retrieval[Hybrid Retrieval<br/>(Vector + BM25)]
        Retrieval --> Filter[Metadata Filter / Grader]
        Filter --> Rerank[Cross-Encoder Reranker]
        Rerank --> Generator[LLM Synthesis]
        Generator --> HallCheck{Hallucination Check}
        HallCheck -->|Failed| Pipeline
        HallCheck -->|Passed| Final[Final Answer]
    end
    
    Final --> UI
    Gen --> UI
    Slang --> UI
```

---

## 🔄 Quy trình xử lý chi tiết (Workflows)

### Workflow 1: Trích xuất Phụ lục & Biểu mẫu
*Dành cho các câu hỏi dạng: "Cho tôi xem phụ lục 07"*
1. **Router**: Nhận diện đây là `document_generation`.
2. **Retrieval**: Sử dụng query nguyên bản (không rewrite) để tìm kiếm chính xác từ khóa.
3. **Filtering**: Áp dụng Metadata Filter dựa trên số hiệu Điều/Phụ lục đã được trích xuất khi indexing.
4. **Output**: Trích xuất nguyên văn khối nội dung (không qua LLM tóm tắt) để đảm bảo tính pháp lý.

### Workflow 2: Hỏi đáp tổng hợp (General Q&A)
*Dành cho các câu hỏi dạng: "Điều kiện xét tốt nghiệp KLTN là gì?"*
1. **Rewriting**: "KLTN" được Slang Manager giải mã và tích hợp vào query mới.
2. **Grading**: Loại bỏ các đoạn văn bản có điểm tương đồng thấp hoặc thông tin nhiễu.
3. **Synthesis**: LLM tổng hợp thông tin từ nhiều nguồn tài liệu để đưa ra câu trả lời tự nhiên, chính xác.
4. **Verification**: Hallucination Checker so khớp câu trả lời với tài liệu gốc trước khi hiển thị.

---

## 🛠️ Thành phần cốt lõi (`src/`)

| Thành phần | Đường dẫn | Chức năng |
|:---|:---|:---|
| **Agents** | `src/agents/` | Chứa logic của Router, Rewriter, Grader, Reranker, Generator. |
| **Legal Chunker** | `src/legal_chunker.py` | Chia tài liệu theo định dạng văn bản luật (Điều, Phụ lục). |
| **Slang Manager** | `src/slang_manager.py` | Quản lý và lưu trữ các từ viết tắt cục bộ (data/custom_abbreviations.json). |
| **Vector Store** | `src/vector_store.py` | Quản lý ChromaDB và tích hợp Hybrid Search. |
| **OCR Utility** | `src/document_loader.py` | Pipeline xử lý file PDF/DOCX tích hợp PaddleOCR. |

---

## 🚀 Hướng dẫn triển khai

### 1. Thiết lập môi trường
Khuyến khích sử dụng Conda để quản lý môi trường ổn định nhất trên Windows:
```bash
# Sử dụng script tự động
setup_conda.bat
```
Hoặc cài đặt thủ công:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Cấu hình hệ thống
Tạo file `.env` và điền các thông tin cần thiết:
```env
LLM_PROVIDER=openai  # Hoặc ollama, gemini
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
MONGO_URI=mongodb://localhost:27017/  # Lưu lịch sử chat
ENABLE_HALLUCINATION_CHECK=True
```

### 3. Khởi chạy
- **Bước 1: Indexing tài liệu** (Run một lần khi có file mới trong `data/documents/`):
  ```bash
  python initialize.py
  ```
- **Bước 2: Chạy ứng dụng**:
  ```bash
  python demo.py
  ```

---

## 📁 Cấu trúc thư mục
```text
agentic_chatbot/
├── src/
│   ├── agents/          # Các nhân tố AI định hướng workflow
│   ├── legal_chunker.py # Phân tách tài liệu theo cấu trúc pháp lý
│   └── vector_store.py  # Engine tìm kiếm Hybrid
├── data/
│   ├── documents/       # Kho tài liệu (Markdown, PDF, Docx)
│   └── slang.json       # Từ điển viết tắt tùy chỉnh
├── vector_db/           # Database lưu trữ vector embeddings
├── demo.py              # Giao diện người dùng Gradio
└── config.py            # Cài đặt hệ thống (K, Threshold, v.v.)
```

---

## 👥 Đội ngũ thực hiện
- **Tác giả**: [Họ tên của bạn]
- **Tổ chức**: Trường Đại học Công nghiệp Hà Nội (HaUI)
- **Liên hệ**: [Email/GitHub]

---
*Dự án được phát triển với mục đích nâng cao trải nghiệm tra cứu quy định đào tạo cho sinh viên.*
