# Bổ sung Phần 5 (màn hình tham chiếu dữ liệu danh mục) cho 15 SRS danh mục — @namdangit

Khuôn: SRS - Danh mục quốc gia (bản QA) — bảng 4 cột STT | Nhóm | Màn hình | Đường dẫn.

## Phase 1 (05/10/2026)
- [x] 3 agent dò code → refs/*.json; 1 agent chuẩn hoá (mỗi lối vào 1 dòng, đường dẫn theo thanh bên thật) → refs_final/*.json
- [x] insert_phan5.py: chèn vào BẢN ĐANG TRÊN DRIVE (drive/), nhân bản style Phần 4, lặp tiêu đề bảng, không cắt dòng → out/
- [x] Word cập nhật mục lục, gỡ font nhúng, so ảnh/chữ với bản Drive (không mất gì)
- [x] Ghi đè 15 file theo ID (giữ link); kiểm ModTime trước khi đẩy — không ai sửa sau lúc tải

## Phase 2 (06/10/2026) — folder SRS chuyển đổi 1QiH3sLYHOuxtj28RJKS_VPHXn592_plo
- [x] Kiểm 20 SRS danh mục: đã có Phần 5 = quốc gia, Tỉnh-TP, khu vực → còn 17
- [x] 4 agent dò code gop_db → refs2/*.json (khách hàng dùng lại refs_final/khach-hang.json); chuẩn hoá: tên phân hệ ngắn (Danh mục, Thông tin NS), Tài chính thêm cấp hubGroup, bỏ màn chờ duyệt chỉ đọc, giữ Hồ sơ cá nhân gửi duyệt (Menu tài khoản)
- [x] SET=2 insert_phan5.py → out2/, Word cập nhật mục lục, so ảnh/chữ (ảnh vắng duy nhất = ảnh Tuỳ chỉnh cột cũ mồ côi, không còn tham chiếu)
- [x] Ghi đè 16 docx theo ID (kiểm ModTime, 16/16 khớp kích thước)
- [x] "Dịch vụ sửa chữa và chi phí khác" (Google Doc gốc) → Playwright: gõ heading + copy định dạng Phần 4, dán bảng HTML, ghim hàng tiêu đề, cập nhật mục lục

### Checkpoint — 06/10/2026 17:25
Vừa hoàn thành: Phần 5 cho 17 SRS danh mục folder chuyển đổi
Đang làm dở: —
Bước tiếp theo: chờ user phản hồi (Danh mục khu vực có Phần 5 dở dang, mục lục thiếu dòng — chưa đụng)
Blocked:
