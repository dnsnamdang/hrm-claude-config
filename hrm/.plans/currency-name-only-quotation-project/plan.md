# Plan — Hiển thị Loại tiền tệ chỉ "Tên" + bổ sung Ngày/Người lập báo giá

Phạm vi: FE-only (chỉ đổi cách hiển thị, không đụng payload/BE).

## Phase 1 — Currency chỉ hiển thị Tên (AC1) + info báo giá (AC2)

### FE — AC1: Loại tiền tệ chỉ hiện Tên (bỏ "Mã - ")
- [x] Báo giá tạo/sửa: `quotations/_id/edit.vue` loadCurrencies label `${code} - ${name}` → `name` (giữ field `code` cho currencyCode)
- [x] Báo giá xem chi tiết: `quotations/_id/index.vue` `currency.code + ' - ' + currency.name` → `currency.name`
- [x] Dự án TKT tạo/sửa/xem: `prospective-projects/components/FinanceSection.vue` loadCurrencies text `${code} - ${name}` → `name` (component dùng chung cho add/edit/detail isShow)

### FE — AC2: Bổ sung Ngày lập + Người lập báo giá (màn xem chi tiết)
- [x] `quotations/_id/index.vue`: thêm dòng info-table "Ngày lập báo giá" (`created_at`) + "Người lập báo giá" (`creator_name`) trong khu Thông tin chung

### Verify (AC3: lưu/cập nhật vẫn chạy)
- [x] Playwright: currency chỉ hiện Tên ở báo giá (create) + dự án TKT (detail) + báo giá detail; detail hiện Ngày/Người lập báo giá
- [x] AC3: thay đổi chỉ ở label/text hiển thị của option; value=currency_id giữ nguyên, field `code` trong option (edit.vue) vẫn giữ cho currencyCode → payload/lưu không đổi

### Checkpoint — 2026-07-08
Vừa hoàn thành: toàn bộ Phase 1 — CODE DONE + VERIFIED (Playwright)
Verify:
- AC1: options tiền tệ báo giá create = [AUD,CHF,CNY,EURO,GBP,IDR,RUPEE,JPY,KWR,USD,VNĐ] (không còn "EUR - EURO"); dự án TKT detail id=32 giống vậy, selected "VNĐ"; báo giá detail id=10 "Loại tiền tệ: VNĐ"
- AC2: báo giá detail id=10 hiện "Ngày lập báo giá: 07/07/2026" + "Người lập báo giá: Trần Văn Đức" trong Thông tin chung (ảnh xác nhận)
- AC3: display-only, value binding theo id → lưu/cập nhật không ảnh hưởng
Files sửa: quotations/_id/edit.vue (loadCurrencies label→name), quotations/_id/index.vue (currency name-only + 2 dòng Ngày/Người lập), prospective-projects/components/FinanceSection.vue (text→name)
Đang làm dở: không
Bước tiếp theo: user verify browser + xác nhận lưu thực tế 1 lần cho chắc AC3
Blocked:
