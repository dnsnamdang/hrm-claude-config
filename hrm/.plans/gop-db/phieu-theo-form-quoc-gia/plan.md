# Plan — Sửa SRS + HDSD 16 màn "DNS đang fix" theo form Danh mục quốc gia

**Người phụ trách:** @junfoke — 2026-10-28
Chuẩn: `CHECKLIST.md` (từ 2 file mẫu `mau/` + góp ý TPE trên SRS/HDSD quốc gia) · Brief agent: `BRIEF_AGENT.md` · File giao: `giao/<STT>/`

## Ngày 28/10/2026 (@junfoke)

- [x] 28/10/2026 — Rà 32 file (SRS + HDSD của 16 màn) so với form quốc gia: SRS khung đã đúng, chỉ lỗi lặt vặt; HDSD cả 16 file còn dạng dài kiểu cũ (văn xuôi, bảng mô tả trường, còn URL, thiếu sơ đồ chức năng, không có dòng "Bước n").
- [x] 28/10/2026 — Đọc góp ý TPE trên bản SRS/HDSD quốc gia → viết `CHECKLIST.md`.
- [x] 28/10/2026 — Làm mẫu màn 27 Phiếu chuyển hàng nhập thẳng: SRS 60 tr (vá trên bản Drive 07/10, giữ phần người khác sửa tay), HDSD gọn ~29 → 21 tr. Đổi chụp ảnh tài liệu sang dev-hrm thay local cho nhanh.
- [x] 28/10/2026 — 15 màn còn lại chạy 8 agent song song (tải sẵn bản Drive mới nhất, mỗi agent 1 trình duyệt dev-hrm, chép khuôn màn 27) → xong 16 màn / 32 file trong `giao/`, PDF xem nhanh trong `out/` từng màn. Màn: 26, 27, 31, 32, 33, 48, 49, 160, 161, 162, 163, 187, 188, 191, 232, 233.
- [x] Tải 32 file lên Drive đúng tên (29/10).

## Checkpoint — 2026-10-28

- **Vừa hoàn thành:** 16 màn SRS + HDSD theo form mới, nằm ở `giao/`.
- **Bước tiếp theo:** user soát → tải lên Drive.
- **Blocked:** —

## Ngày 29/10/2026 (@junfoke)
- [x] 29/10/2026 — Cài rclone + kết nối Drive; script `push_drive.py` đẩy hàng loạt, ghi đè theo ID file (link trên sheet giữ nguyên), tự bỏ qua file có người sửa sau lần đẩy gần nhất hoặc đang có comment. Chạy thử: `python push_drive.py`; đẩy: `--go` (hoặc `--go 26 49`).
- [x] 29/10/2026 — Đẩy cả 32 file SRS + HDSD lên Drive, khớp MD5 với bản local; vài lần Google báo 403 giới hạn tốc độ, script tự chờ thử lại, không bỏ file nào.
- [ ] Đổi cột trạng thái 16 dòng trên sheet theo dõi (đang "DNS đang fix") — chờ user.
