# Plan — Cho phép trùng hàng hóa (NT theo tháng)

**Phụ trách:** @khoipv · **Phạm vi:** thuần FE — `FormByMonth.vue`

## FE — `pages/contract/acceptance_report/components/forms/FormByMonth.vue`
- [x] Bỏ computed `excludeIds` + bỏ attribute `:excludeIds` ở `<GoodsPickerModal>`
- [x] `onPickerConfirm`: bỏ dedup theo `product_id`, luôn push dòng mới + gán `uid`
- [x] Thêm cơ chế sinh `uid` (counter); gán `uid` cả ở `buildRows` (prefill)
- [x] Đổi `:key="row.product_id"` → `:key="row.uid"`
- [x] Thêm `consumedBefore`/`rowEffNt`/`rowRemain`/`isOver(ri,row)` — "Còn lại"/"Đã NT" trừ dần theo dòng
- [x] Cột "Còn lại" + "Đã NT" + "SL nghiệm thu" dùng giá trị trừ dần (giống FormByInvoiceDetail)
- [x] `emitUpdate.hasQtyError`: theo `isOver` trừ dần (tương đương tổng cộng dồn)

## FE — trùng theo cặp (mặt hàng + số hóa đơn)
- [x] Bỏ `dupInvoiceNoSet`; thêm `dupPairSet` + `usedSet`
- [x] `isDupRow(row)` (cặp trong bảng HOẶC số HĐ ở BBNT khác) + `dupMsg(row)`; template dùng 2 hàm này
- [x] `emitUpdate` emit `hasDupError`
- [x] `AcceptanceReportForm`: nhận `hasDupError`, `submitForm` chặn mềm + thêm vào init/reset summary

## BE — `AcceptanceReportService`
- [x] `assertNoDuplicateInvoiceNumbers`: với `TYPE_THANG` dùng cặp (product_id, so_hd); loại khác giữ nguyên
- [x] Thêm helper `duplicateProductInvoiceNos()`
- [x] Cross-report intersect giữ nguyên (khóa theo số hóa đơn)

## Kiểm thử tay (sau khi code)
- [ ] Chọn lại mặt hàng đã có → ra 2 dòng
- [ ] 2 mặt hàng khác nhau cùng 1 số HĐ → lưu OK (không báo trùng)
- [ ] Cùng mặt hàng + cùng số HĐ → báo trùng + chặn (FE + BE)
- [ ] Còn lại/Đã NT trừ dần đúng giữa các dòng cùng mặt hàng
- [ ] Edit biên bản đã lưu 2 dòng cùng mặt hàng → prefill đủ
