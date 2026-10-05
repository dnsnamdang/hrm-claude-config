# Bổ sung Phần 5 (màn hình tham chiếu dữ liệu danh mục) cho 15 SRS danh mục — @namdangit

Khuôn: SRS - Danh mục quốc gia (bản QA) — bảng 4 cột STT | Nhóm | Màn hình | Đường dẫn.

## Phase 1 (05/10/2026)
- [x] 3 agent dò code → refs/*.json; 1 agent chuẩn hoá (mỗi lối vào 1 dòng, đường dẫn theo thanh bên thật) → refs_final/*.json
- [x] insert_phan5.py: chèn vào BẢN ĐANG TRÊN DRIVE (drive/), nhân bản style Phần 4, lặp tiêu đề bảng, không cắt dòng → out/
- [x] Word cập nhật mục lục, gỡ font nhúng, so ảnh/chữ với bản Drive (không mất gì)
- [x] Ghi đè 15 file theo ID (giữ link); kiểm ModTime trước khi đẩy — không ai sửa sau lúc tải
