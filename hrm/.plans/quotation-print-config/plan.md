# Plan — Popup cấu hình in báo giá: cột hiển thị

## Fix: Bỏ mặc định checked cột "Mã hàng hoá" (2026-07-13)

File: `hrm-client/components/assign/quotation/QuotationPrintConfigModal.vue`

- [x] Tách logic: mặc định (mounted / mở modal / đổi discountMethod) chọn tất cả cột TRỪ `code` (Mã hàng hoá) — method `selectDefault()`
- [x] Giữ nút "Chọn tất cả" (`toggleCheckAll` → `selectAll()`) vẫn chọn hết mọi cột (kể cả `code`)
- [x] User vẫn tự tích `code` được nếu muốn (checkbox v-model selectedColumns)

Cách: thêm `defaultUncheckedColumns: ['code']`, method `selectDefault()` (all trừ code) dùng cho mặc định; `selectAll()` giữ nguyên cho toggle.

### Checkpoint — 2026-07-13
Vừa hoàn thành: Bỏ mặc định tích cột "Mã hàng hoá" trong popup cấu hình in báo giá (thêm `defaultUncheckedColumns` + `selectDefault()`). FE-only.
Đang làm dở: (không)
Bước tiếp theo: user build FE + test (mở popup → "Mã hàng hoá" chưa tích; "Chọn tất cả" vẫn lấy hết; tự tích lại được).
Blocked: (không)
