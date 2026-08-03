# Plan — Cho phép chọn Loại tiền tệ khi lập báo giá (chỉ tạo mới)

## Phase 1 — FE edit.vue

- [x] **T1. Template select tiền tệ**: `:disabled="true"` → `:disabled="!isCreateMode"` + `@change="handleChangeCurrency"`. Giữ `:value="form.currency_id"` + `:allowClear="false"`.
- [x] **T2. `handleChangeCurrency`**: sau khi set `form.currency_id`, đồng bộ làm tròn theo tiền tệ mới (`roundingMode = isVndCurrency ? '0' : null`) — nhất quán feature quotation-rounding-vnd.
- [x] **T3. Verify**: kế thừa dự án (selectProject) giữ nguyên; save payload gồm `currency_id` (create + update BE đã lưu). Form Sửa khoá field.
- [ ] **T4. Verify E2E** (user): Tạo báo giá dự án USD → field = USD; chọn lại VND/EUR được; đổi sang VNĐ → làm tròn về Số nguyên; lưu → mở lại đúng currency. Form Sửa → field khoá không đổi.

### Checkpoint — 2026-07-02
Vừa hoàn thành: T1–T3 (enable select chỉ create + wire handleChangeCurrency + sync rounding). FE-only.
Đang làm dở: (không)
Bước tiếp theo: user build FE + E2E (T4).
Blocked:
