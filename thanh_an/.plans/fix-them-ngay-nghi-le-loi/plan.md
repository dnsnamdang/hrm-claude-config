# Fix: Thêm ngày nghỉ lễ báo "Tạo loại nghỉ thất bại" — gửi group_permission_ids toàn null

> Người phụ trách: @khoipv · Bắt đầu: 20/11/2026 · Trạng thái: **Tạm dừng — user tự sửa sau**

## Câu hỏi
`POST /api/v1/timesheet/holiday` (demo) — thêm ngày lễ "Nghỉ lễ ngày văn hóa Việt Nam 24/11/2026", mã `24.11`, tỉ lệ 100,
payload gửi `group_permission_ids: [null × 13]`, không có `description` → báo lỗi, chip Nhóm nghiệp vụ hiện trống.

## Kết luận (đọc code, chưa chạy thử)
1. **Lỗi gốc BE** — `hrm-thanhan-api/Modules/Timesheet/Services/HolidayService.php:43` (sửa) và `:62` (tạo mới) đọc
   `$attributes['description']` trực tiếp. Popup thêm mới khởi tạo `data = {}` (`holiday-modal.vue:116`), bỏ trống Ghi chú
   ⇒ payload không có key → `Undefined index: description` → bị `catch (\Exception)` trong
   `HolidayController.php:82` nuốt, trả `fail` 500, **không ghi log**.
2. **Lỗi kéo theo FE** — `hrm-thanhan-client/components/modal/holiday-modal.vue:135` ghi đè
   `this.data.group_permission_ids = ....map(val => val.id)` lên chính v-model của multiselect.
   Lưu lần 1 lỗi ⇒ v-model thành mảng số (chip mất tên); Lưu lần 2 `(5).id` = undefined ⇒ gửi `[null, ...]`.

Workaround: nhập Ghi chú bất kỳ, đóng popup mở lại, chọn lại nhóm rồi Lưu.

## Task (chưa làm — user tự sửa)
- [ ] BE `HolidayService::save` (cả 2 nhánh): `$attributes['description'] ?? null`, `$attributes['group_permission_ids'] ?? []`, bỏ id null
- [ ] BE `HolidayController::store`: `\Log::error($e)` trong catch
- [ ] FE `holiday-modal.vue`: tạo payload riêng thay vì ghi đè `this.data`; khởi tạo `data = { description: '', group_permission_ids: [] }`
- [ ] Test: thêm mới không ghi chú; Lưu lỗi rồi Lưu lại; sửa ngày lễ có sẵn

### Checkpoint — 20/11/2026
Vừa hoàn thành: trace nguyên nhân
Đang làm dở: —
Bước tiếp theo: user tự sửa theo các task trên
Blocked:
