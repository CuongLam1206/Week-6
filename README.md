# Báo cáo Tổng quan Kỹ thuật & Độ khả thi Dự án AI Video

## 1. Danh sách Công nghệ sử dụng (Tech Stack)

Hệ thống được xây dựng trên mô hình Microservices để tách biệt các thành phần xử lý:

*   **Backend chính (Main API):** Node.js với framework Express.
*   **Cơ sở dữ liệu:** SQLite (sử dụng Sequelize ORM) để lưu trữ thông tin người dùng, avatar và trạng thái video.
*   **Frontend (Dashboard):** React.js (Vite) cung cấp giao diện quản lý video và cấu hình avatar.
*   **Xử lý AI (Self-hosted):** Python (Wav2Lip model) được đóng gói thành một service riêng để thực hiện lip-sync.
*   **Xử lý Video:** FFmpeg đóng vai trò cốt lõi trong việc ghép âm thanh, cắt clip và chuyển đổi định dạng.
*   **Tích hợp:** Office.js cho Outlook Add-in, cho phép sử dụng tính năng ngay trong email.
*   **Cloud API:** HeyGen V2 API cho lựa chọn tạo video chất lượng studio từ điện toán đám mây.
*   **Triển khai (DevOps):** Docker & Docker Compose để quản lý các container độc lập.

## 2. Triển khai Hệ thống (Implementation Detail)

Hệ thống được triển khai qua các bước cụ thể:

*   **Đóng gói Container:** Mỗi thành phần (API, Client, AI-Service) chạy trong một container riêng biệt. Điều này giúp dễ dàng nâng cấp hoặc thay đổi mô hình AI mà không ảnh hưởng đến logic nghiệp vụ.
*   **Giao thức kép (Dual-Protocol):** 
    *   Sử dụng **HTTPS (Cổng 3001)** để tương thích với các chính sách bảo mật khắt khe của Microsoft Outlook.
    *   Sử dụng **HTTP (Cổng 3005)** để Dashboad nội bộ hoạt động mượt mà, tránh lỗi chứng chỉ SSL trên môi trường local.
*   **Quy trình xử lý Video tự động:**
    1.  Người dùng upload ảnh và ghi âm.
    2.  Hệ thống convert âm thanh sang chuẩn MP3.
    3.  Asset được đẩy vào volume dùng chung (Shared Volume).
    4.  Service AI nhận lệnh, chạy model Wav2Lip trên server để tạo video.
    5.  FFmpeg ghép hậu kỳ và trả kết quả về database.

## 3. Bảo mật và Phân quyền (Security & Authorization)

Hệ thống đã được thiết kế với các lớp bảo mật tiêu chuẩn:

*   **Xác thực (Authentication):** Sử dụng cơ chế **JWT (JSON Web Token)**. Mọi yêu cầu truy cập API (trừ đăng nhập/đăng ký) đều yêu cầu Token hợp lệ gửi qua Header.
*   **Phân quyền dữ liệu (Data Isolation):**
    *   Mỗi User chỉ có quyền truy cập, chỉnh sửa hoặc tạo video dựa trên **Avatar và dữ liệu của chính mình**.
    *   Hệ thống kiểm tra `userId` trong mọi câu lệnh truy vấn database (`Avatar.findOne({ where: { userId: req.user.id } })`), đảm bảo không có hiện tượng rò rỉ dữ liệu giữa các tài khoản khác nhau.
*   **Quản lý vai trò (RBAC):** Cấu trúc Database đã có sẵn trường `role` (Admin, User) để sẵn sàng mở rộng các tính năng quản trị cao cấp (như quản lý dùng chung avatar theo công ty) trong tương lai.
*   **Bảo mật đường truyền:** Triển khai SSL cho các endpoint nhạy cảm (Cổng 3001) để bảo vệ dữ liệu trên hạ tầng mạng.

## 4. Ghi chú các phần chưa hoàn thiện & Lỗi hiện tại

Dưới đây là danh sách các hạng mục vẫn đang trong quá trình xử lý hoặc gặp rào cản kỹ thuật:

| Hạng mục | Trạng thái | Chi tiết lỗi / Ghi chú |
| :--- | :--- | :--- |
| **Tích hợp HeyGen V2** | ⚠️ Lỗi (Fixing) | Endpoint `/v2/video/generate` đôi khi báo lỗi 400 hoặc 404 do thay đổi cấu hình tài sản (Asset) phía HeyGen. Đang chuyển sang quy trình rút gọn (Simplified Flow). |
| **Tốc độ Render nội bộ** | ⚠️ Hạn chế | Luồng Wav2Lip chạy quá chậm (300s cho 2s video) do chưa kết nối được GPU vào Container Docker. |
| **Avatar từ Ảnh tĩnh** | ❌ Chưa xong | Hiện tại demo vẫn dùng video quay sẵn làm gốc. Khả năng sinh từ 1 ảnh tĩnh duy nhất vẫn đang phụ thuộc vào việc fix xong API HeyGen. |
| **Giao diện Phân quyền** | ❌ Giai đoạn 2 | Mặc dù backend đã có logic phân quyền, nhưng giao diện Admin để quản lý toàn bộ User chưa được triển khai. |
| **Preview Video Outlook** | ⚠️ Hạn chế | Một số phiên bản Outlook Desktop cũ có thể không hiển thị được video do chính sách bảo mật IFRAME, hiện đang dùng link thumbnail dự phòng (fallback). |

## 5. Báo cáo Độ khả thi (Feasibility Report)

### 5.1. Những gì đã thực hiện được
- **Hạ tầng ổn định:** Toàn bộ tech stack đã được deploy thành công qua Docker. Hệ thống API xác thực JWT đã hoạt động thông suốt giữa Dashboard và Outlook.
- **Xác thực Luồng tạo video nội bộ (Flow 2):** Đã chạy thành công quy trình tạo video từ ảnh và voice ngay trên hạ tầng server.
- **Gửi Mail & Preview:** Video sau khi tạo đã có thể xem trực tiếp và gửi đi dưới dạng link nhúng trong email Outlook.

### 5.2. Khả năng khắc phục
- **Tốc độ:** **CÓ THỂ KHẮC PHỤC** bằng cách cấu hình NVIDIA Docker để render qua GPU. Thời gian dự kiến có thể giảm xuống dưới 120 giây.
- **API HeyGen:** **CÓ THỂ KHẮC PHỤC** bằng cấu hình "Simplified V2 Flow" (đã có phương án triển khai).
- **Avatar từ Ảnh:** Sẽ được giải quyết sau khi kết nối thành công HeyGen V1/V2 ổn định.

## 6. Kết luận
Dự án đã có nền tảng bảo mật và kiến trúc tốt. Thử thách hiện tại nằm ở **Tối ưu hóa phần cứng (GPU)** và **Đồng bộ API**. Đây đều là các vấn đề kỹ thuật có thể xử lý được trong các sprint tiếp theo.
## 7. Demo những gì đã có:
Link: https://drive.google.com/file/d/1S4VXxAAbnTZFoii2Ikhn9_mujasQTmL5/view?usp=drive_link
