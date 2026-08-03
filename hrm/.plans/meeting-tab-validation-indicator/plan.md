# Plan — Đánh dấu tab chứa lỗi validate (màn Tạo/Sửa cuộc họp)

Phụ trách: @namdangit

## Mục tiêu
Khi Lưu cuộc họp mà thiếu field bắt buộc ở nhiều tab: tiêu đề tab chứa lỗi hiển thị đỏ + icon cảnh báo; tự nhảy tới tab lỗi đầu tiên và focus field lỗi; badge tự mất khi hết lỗi (sau khi sửa và Lưu lại).

## Phạm vi
CHỈ FE. 2 file:
- `hrm-client/components/V2BaseTabNavigation.vue` (dùng chung — sửa cộng thêm, opt-in)
- `hrm-client/pages/assign/meeting/components/MeetingForm.vue`
Không BE / migration / permission / git.

## Quyết định
- Kiểu hiển thị: chữ đỏ + icon cảnh báo (`ri-error-warning-fill`). Tab lỗi đang active: nền xanh + viền đỏ.
- Dò tab lỗi bằng DOM: quét mỗi panel có `.v2-error` (marker của V2BaseError) → tự khớp field lỗi thuộc tab nào, không cần map key thủ công.
- `formError` (Vuex `paymentProfile`) chỉ refresh khi Lưu → badge mất sau lần Lưu kế tiếp (nhất quán với lỗi inline hiện tại). Live-clear theo từng phím gõ = task riêng nếu cần.

## Task

### FE — V2BaseTabNavigation.vue
- [x] Thêm hỗ trợ `tab.hasError`: class `has-error` + icon cảnh báo, opt-in (màn khác không truyền → giữ nguyên)
- [x] CSS trạng thái lỗi: chữ đỏ khi không active, viền đỏ khi active

### FE — MeetingForm.vue
- [x] Thêm ref cho panel Điểm danh (`meetingAttendance`) + Biên bản (`meetingReport`)
- [x] Computed `formError` (map từ store), data `tabErrorFlags`
- [x] `tabs` computed gắn `hasError` từng tab
- [x] Methods: `getPanelEl`, `recomputeTabErrors` (quét `.v2-error`), `jumpToFirstError`, `focusFirstError`
- [x] Watch `formError` deep → recompute cờ + nhảy tab lỗi đầu + focus
- [ ] Verify E2E: submit thiếu field ở nhiều tab → tab đỏ + nhảy tab + focus; sửa xong Lưu lại → badge mất (cần dev server FE + tài khoản)

### Fix — 2026-07-24
- [x] Bug popup thêm nhanh KH: trường "Công ty mẹ" (V2BaseSelectRemote) không search được trong modal → set `dropdownParent` về `.modal-content` (xem plan meeting-quick-add-customer)

### Checkpoint — 2026-07-24
Vừa hoàn thành: Toàn bộ code 2 file (tab error indicator + auto-jump + focus).
Đang làm dở: chưa verify trên browser.
Bước tiếp theo: user bật FE dev server → verify luồng submit thiếu field nhiều tab.
Blocked: cần môi trường FE chạy để verify.
