# Fix: Báo cáo Luân chuyển hàng hóa — "tồn kho bán được" dôi ảo khi KHÔNG chọn công ty

> File: `app/Services/OrderReports/StockTransferReportService.php`
> Route: `stock_transfer_report.searchData` → `StockTransferReportController@searchData` → `StockTransferReportService::getData`

## Triệu chứng
Không chọn công ty → cột "SL tồn kho bán được" (`stock_can_sale`) > 0 dù thực tế hết. Chọn từng công ty thì mỗi công ty đều = 0. (Case: JONN-JAT-501, product 5331: gộp báo 11, mỗi cty báo 0.)

## Nguyên nhân gốc
`getData` có 2 nhánh tính tồn/giữ (if/else tại ~dòng 1088):
- **Chọn công ty** → subquery INLINE (1089-1178). Phần PXK (`werd`) **KHÔNG** join `product_export_requests` (đã comment).
- **Không chọn công ty** → helper `buildWarehouseExportRequestSubQuery` (~6350). Phần PXK **CÓ INNER JOIN `product_export_requests`** (`wer.product_export_request_id = pr.id`).

→ Helper loại mọi PXK giữ hàng không có `product_export_request_id` (vd phiếu giữ tạo trực tiếp). Với 5331: 1 PXK cty1 giữ total=11 (product_export_request_id NULL) bị rớt → phần "giữ" trừ thiếu 11 → bán được = tồn(21) − prepick(10) − 0 = 11 (đáng lẽ 0).

Ngoài ra helper thiếu quy đổi `unit_coefficient` (inline có), lệch với đơn vị khác đơn vị gốc.

## Fix
Sửa `buildWarehouseExportRequestSubQuery` cho khớp inline:
- [x] Bỏ `->join('product_export_requests as pr', ...)`.
- [x] Thêm `->join('product_units as pu', ...)` (pu.product_id=werd.product_id AND pu.unit_id=werd.unit_id).
- [x] Nhân `export_total_qty/prepick_qty/hold_qty` với `COALESCE(pu.unit_coefficient, 1)`.

## Verify (erp_new, tinker)
- [x] `php -l` sạch.
- [x] Helper đã sửa: `wer_total` cho 5331 = 11 (trước = 0).
- [x] `stock_can_sale` (không chọn cty) = 21 − 0(km) − 0(hold) − 10(prepick) − (11 − 0 − 0 − 0) = **0** → khớp per-company.
- [ ] (khuyến nghị) E2E browser: mở báo cáo không chọn cty + lọc JONN-JAT-501 → "SL tồn kho bán được" = "-"/0.

## Ghi chú
- Nhánh `wer_km` (werd_type, ~1190) join pr type=XUAT_KM_HD_HANG là chủ đích (KM), không đụng.
- Các helper còn lại (Stock/Km/Hold) đã khớp inline, không cần sửa.
- Chưa commit (chờ user).

### Checkpoint — 2026-07-23
Vừa hoàn thành: sửa helper buildWarehouseExportRequestSubQuery (bỏ join pr + thêm unit_coefficient). Verify tinker ra 0.
Bước tiếp theo: user E2E browser + commit.
Blocked:
