# Design — Popup cấu hình in báo giá: mặc định cột hiển thị

## Mục tiêu
Popup "Cấu hình in báo giá" → "Chọn cột hiển thị": bỏ tích mặc định cột "Mã hàng hoá" (user vẫn tự tích được).

## Scope (FE-only, `hrm-client/components/assign/quotation/QuotationPrintConfigModal.vue`)
- Thêm data `defaultUncheckedColumns: ['code']`.
- Thêm method `selectDefault()`: chọn tất cả cột TRỪ các key trong `defaultUncheckedColumns`.
- Đổi 3 chỗ tạo mặc định (`mounted`, watcher `show`, watcher `discountMethod`): `selectAll()` → `selectDefault()`.
- Giữ nguyên `selectAll()` cho nút "Chọn tất cả" (`toggleCheckAll`) → vẫn tích hết mọi cột kể cả `code`.

## Quyết định
- Chỉ đổi trạng thái mặc định, không xoá cột khỏi danh sách → "Mã hàng hoá" vẫn hiện và tích được thủ công.
- Checkbox "Chọn tất cả" mặc định không tích (vì thiếu 1 cột) — nhất quán logic hiện có.

## Trạng thái
CODE DONE 2026-07-13, FE-only, chờ user build + test.
