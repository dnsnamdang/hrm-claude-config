# Plan — BBNT lấy đơn giá theo product_id + unit_id

**Phụ trách:** @khoipv · **Phạm vi:** BE + FE + migration

## BE — `Modules/Category`
- [x] Migration thêm cột `unit_id` (nullable, index, không FK) vào `acceptance_report_items` + chạy migrate
- [x] Entity `AcceptanceReportItem`: thêm `unit_id` vào `$fillable`
- [x] `productQtyMap()`: groupBy `product_id, unit_id`, key `"pid|unit"`, giá theo từng đơn vị
- [x] `productPriceByUnit()` + `resolvePriceName()` (fallback theo product_id)
- [x] `saveItems()` / `saveInvoiceBlocks()`: dùng resolvePriceName + lưu `unit_id`
- [x] `AcceptanceReportDetailResource`: trả thêm `unit_id`

## FE — `pages/contract/acceptance_report`
- [x] `AcceptanceReportForm.vue`: tra `quantities` theo `product_id|unit_id`
- [x] `ProductGrid.vue`: prefill khớp pid|unit (fallback pid) + gửi `unit_id`
- [x] `FormByMonth.vue`: prefill khớp pid|unit (fallback pid) + gửi `unit_id` + consumedBefore theo unit
- [x] `FormByInvoiceDetail.vue`: prefill khớp pid|unit (fallback pid) + gửi `unit_id` + consumedBefore theo unit

## Kiểm thử tay
- [ ] HĐ 2 product 26: dòng mL = 30.000, dòng Hộp = 1.500.000; SL thầu đúng (250 mL / 12 Hộp)
- [ ] Lưu → tổng danh sách = tổng chi tiết
- [ ] Sửa lại → prefill đúng đơn vị
- [ ] tonghd/cthd/mathang/luyke vẫn bình thường
- [ ] Mở report 23 sửa & lưu lại → rà product 26 cho đúng đơn vị

## Ghi chú
- `accumulatedQty` giữ theo product_id (hạn chế multi-unit đã biết, ngoài phạm vi).
- Biên bản cũ (unit_id NULL) cần mở sửa & lưu lại mới tính đúng.
