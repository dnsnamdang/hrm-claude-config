# Sửa dữ liệu prod theo yêu cầu (không có số Redmine) — @cuong61n

## Phiếu giao việc PGV-32497 — sửa giờ kết thúc (10/11/2026)
- [x] 10/11/2026 — Chấm công báo: chị Thúy lập phiếu giao việc đi ăn (id 32497) nhưng điền nhầm giờ kết thúc 20:00 → hệ thống tính về sớm cho cả 8 nhân sự trong phiếu. Đã sửa trên PROD (hrm_erp_gop):
  - `job_assignment_note_details.id=32621`: `intend_end_at` 2026-11-09 20:00:00 → **17:15:00** (giờ bắt đầu giữ 17:00).
  - `job_assignment_notes.id=32497`: `total_minutes` 3.0 → 0.25 (cột chỉ lưu 1 số thập phân nên hiện 0.3).
  - Đã kiểm: đọc lại 2 bản ghi đúng giá trị mới. UPDATE có WHERE theo id + giá trị cũ.
  - Chờ: người báo xác nhận hết tính về sớm trên bảng công.
