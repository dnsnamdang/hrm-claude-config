# Nhắc việc cá nhân — Cải tiến form (tóm tắt)

**Phụ trách:** @khoipv | **Ngày:** 2026-07-17 | **Module:** Assign (`pages/assign/my-todo`)
**Spec đầy đủ:** `docs/superpowers/specs/2026-07-17-my-todo-form-enhance-design.md`

## Mục tiêu
Cải tiến form/modal Nhắc việc cá nhân (Lịch làm việc của tôi) — 3 thay đổi:

1. **Nút "Lưu và tiếp tục"** — chỉ ở màn Tạo mới. Lưu → toast → reset toàn bộ field về trống → giữ modal mở để nhập tiếp. Nút "Lưu"/"Tạo nhắc việc" giữ hành vi cũ (lưu + đóng).
2. **Danh sách bắt buộc** — sao đỏ (*), placeholder "-- Chọn danh sách --", validate inline (viền đỏ + text lỗi, cờ `submitted`). BE: `UpdatePersonalTodoRequest` đổi `list_id` nullable → required cho đồng nhất với Store.
3. **Giờ hạn 24h** — đổi `<input type="time">` native (hiển thị AM/PM theo locale) sang `vue2-datepicker type="time" format="HH:mm" value-type="HH:mm"`. Giá trị lưu vẫn `HH:mm` → BE không đổi.

## Quyết định đã chốt (user)
- Widget Giờ hạn: **vue2-datepicker** (không giữ input native — không ép được 24h mọi trình duyệt).
- "Lưu và tiếp tục": **chỉ màn Tạo mới**.
- Sau "Lưu và tiếp tục": **reset trống hết** (kể cả Danh sách).

## Phạm vi
Chỉ FE + 1 sửa BE validation. **KHÔNG** migration / route / service / model / quyền / data-fix.

## Files
- `hrm-client/pages/assign/my-todo/components/TodoFormModal.vue` (chính)
- `hrm-client/pages/assign/my-todo/index.vue` (`onSaveTodo` + ref + reset)
- `hrm-api/Modules/Assign/Http/Requests/MyTodo/UpdatePersonalTodoRequest.php` (list_id required)

## AC
AC1 sao đỏ + giờ 24h · AC2 bỏ trống Danh sách → chặn · AC3 Lưu và tiếp tục (modal mở + reset) · AC4 Lưu → đóng · AC5 màn Sửa đồng nhất.
