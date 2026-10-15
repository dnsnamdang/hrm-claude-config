# SRS màn Báo giá (`Danh sách báo giá` — CSKH trước bán) — @cuong61n

Nhánh: `gop_db` (worktree gop_db-client :3002 / gop_db-api :8003)

## Phase 1 — Tài liệu SRS
- [x] Rà code BE/FE (danh sách, quyền, duyệt, xoá, form tạo/sửa/sao chép, công thức, import, xuất, in, lịch sử)
- [x] Chụp ảnh thật + icon menu (`quotation_shots/`, không commit)
- [x] Viết `gen_srs.py` → `SRS - Báo giá.docx` (24 chức năng + Phụ lục bảng công thức PL-1…PL-7)
- [x] Chạy selfcheck (khớp bản mẫu), soát sơ đồ tổng quan

### Checkpoint — 13/10/2026 19:00
Vừa hoàn thành: SRS - Báo giá.docx (selfcheck đạt; 24 mục giao diện = 24 mục event = 24 chức năng)
Đang làm dở: —
Bước tiếp theo: user duyệt nội dung; chốt các điểm code lệch nêu khi bàn giao; đẩy Drive nếu user yêu cầu
Blocked:
Ghi chú: ảnh `quotation_shots/` từng bị xoá khi tạm dừng (phiên khác dọn file) → đã chụp lại; sinh lại: `python3 gen_srs.py` (hoặc `SRS_SHOTS=<thư mục ảnh> python3 gen_srs.py`)
