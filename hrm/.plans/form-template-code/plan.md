# Plan — Bổ sung mã cho mẫu phiếu thu thập thông tin

Mã tự sinh `PTT-YYYY-NNNNN`, không cho sửa tay. Hiển thị: danh sách (dưới tên mẫu phiếu, cạnh ngày tạo) + tìm kiếm nhanh, xuất Excel, mẫu phiếu in.

## Phase 1 — Mã mẫu phiếu

### BE

- [x] Migration thêm cột `code` vào `form_templates` (varchar 50, nullable, unique) + backfill mã cho bản ghi cũ theo năm tạo
- [x] `FormTemplate`: thêm `code` vào `$fillable` + `getNextCode()` (pattern `PTT-YYYY-NNNNN`)
- [x] `FormTemplateService::store()` sinh mã khi tạo; `update()` không cho đổi mã
- [x] `FormTemplatesResource` trả thêm `code`
- [x] `FormTemplateService::index()` — tìm kiếm nhanh theo cả mã và tên
- [x] Blade `exports/form_templates` + `FormTemplateService::export()` (CSV) thêm cột Mã

### FE

- [x] `pages/assign/form-templates/index.vue`: hiện mã dưới tên mẫu phiếu (cùng dòng Người tạo/Ngày tạo), placeholder tìm kiếm nhanh nêu rõ tìm theo mã
- [x] Mẫu phiếu in: đã sẵn field "Mã mẫu phiếu" (`header.formCode`) — chỉ cần BE trả `code`

### Checkpoint — 2026-08-06
Vừa hoàn thành: toàn bộ Phase 1 (BE + FE)
Đang làm dở: —
Bước tiếp theo: chạy `php artisan migrate` và kiểm tra màn danh sách / in / xuất Excel
Blocked:
