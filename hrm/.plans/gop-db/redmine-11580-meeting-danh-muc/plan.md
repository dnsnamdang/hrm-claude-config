# Redmine #11580 — Phân hệ Meeting: dời Danh mục + cột/lọc "Có khách hàng" ở Loại meeting

> Nhánh: gop_db (worktrees/gop_db-api + gop_db-client). Đã chuyển khỏi develop 07/10/2026.

## Phase 1
### FE
- [x] Menu phân hệ Meeting: dời nhóm "Danh mục" xuống cuối sidebar (sau "Cấu hình", đúng mũi tên ảnh task)
- [x] Loại meeting: ô lọc "Có khách hàng" (Có khách hàng / Không có khách hàng)
- [x] Loại meeting: cột "Có khách hàng" trong Tuỳ chỉnh cột (mặc định ẩn) + popup chọn trường Xuất Excel
### BE
- [x] MeetingTypeService::index lọc `has_customer`; Resource trả `has_customer_text`; ExportColumnRegistry thêm cột
- [ ] File import thêm trường mô tả — chờ user chốt (file mẫu + modal + BE đã có cột Mô tả)
- [x] BE lọc chỉ nhận 0/1 (giá trị rác bỏ qua, không hiểu thành "Không")
- [x] Test Playwright 3 mức quyền (admin / chỉ Xem / không quyền): 26/27 đạt, case "giữ bộ lọc khi rời màn" là kỳ vọng sai (mixin chỉ giữ khi vào trang con)

### Checkpoint — 2026-10-07
Vừa hoàn thành: ý 1-3 trên gop_db + test Playwright
Đang làm dở: —
Bước tiếp theo: user chốt ý 4 (file import "trường mô tả"), commit khi được yêu cầu
Blocked: ý 4 chờ chốt
