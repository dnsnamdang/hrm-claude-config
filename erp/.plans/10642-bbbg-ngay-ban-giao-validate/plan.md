# #10642 — Plan: chặn Ngày bàn giao BBBG (ERP + HRM)

Rule: `handover_date` từng serial phải `<= hôm nay` và `>= floor(product)` (floor = MIN(approved_time) trên PXK qua kho + PXH xuất thẳng; không có phiếu → bỏ check min). Chi tiết: design.md.

> **Ruling (chốt khi code, lệch design):** floor chỉ tính phiếu đã duyệt bằng **`approved_time IS NOT NULL`** rồi `MIN(approved_time)`, KHÔNG dùng `COALESCE(approved_time, created_at)` + `status=1` như design gốc. Lý do: cột `status` là số nghĩa mơ hồ theo từng loại phiếu; `approved_time` = `now()` đặt đúng lúc duyệt (mốc thực xuất). Hàng chưa có phiếu duyệt → không có floor → fail-open (không chặn), giữ sửa được BBBG của HĐ cũ. Cost nếu sai: phiếu duyệt nhưng thiếu `approved_time` (dữ liệu rất cũ) sẽ không tạo floor cho hàng đó → bỏ sót chặn 1 chiều (an toàn, không chặn nhầm).

## ERP
- [x] **T1 (BE-floor):** `Customers\HandoverAcceptanceRecord::exportDateFloors($firmContractId, $productIds)` → map `product_id => Carbon`. Union `warehouse_export_tab_products⋈warehouse_exports` + `product_export_tab_products⋈product_exports(is_export_direct=1)`, `whereNotNull(approved_time)`, `MIN(approved_time)`.
- [x] **T2 (BE-validate):** `HandoverAcceptanceRecord::applyHandoverDateValidation($validator, $data)` — guard `strpos(contractable_type,'FirmContract')`. Gọi ở cuối `after()` của `HandoverAcceptanceRecordStoreRequest` (dòng 98-99) + `UpdateRequest` (dòng 106-107). Mỗi serial add lỗi nếu `> today` hoặc `< floor` ("...không được trước ngày xuất kho/xuất hàng (dd/mm/yyyy)").
- [x] **T3 (FE-payload):** `HandoverAcceptanceRecordsController::getDataForHandoverAcceptanceRecord` — bơm `export_date_floor` (Y-m-d) theo từng product.
- [x] **T4 (FE-enforce):** `form.blade.php` 2 input handover_date thêm `min-date="<% product.export_date_floor %>"`; directive `dateForm` (`app.directive.js`) thêm `validateOnBlur:true, allowBlank:true` + block observe `attrs.minDate` (opt-in, backward-compatible). **Đã hỏi & được duyệt phương án opt-in cho directive dùng chung.**

## HRM
- [x] **T5 (BE):** `Modules\CustomerCare\Entities\HandoverAcceptanceRecord\HandoverAcceptanceRecord::exportDateFloors()` + `applyHandoverDateValidation($validator, $source, $contractId, $products)` (guard `$source !== 'firm'` → fail-open; HĐ HRM id trùng không gian `firm_contract_id`). Gọi ở cuối `HandoverAcceptanceRecordRequest::after()`. `php -l` sạch.
- [x] **T6 (FE):** `HandoverContractSourceService::withExportFloor()` bơm `export_date_floor` (Y-m-d) theo product cho cả nguồn chọn HĐ (`contractData`) lẫn màn Sửa (`HandoverAcceptanceRecordService::detail`). `handoverBuild.makeProduct` giữ `export_date_floor`. `HandoverProductTable.vue` đổi `:disabled-date="disabledDateFor(product)"` (chặn tương lai + trước floor trên lịch) + câu lỗi inline từ BE validate.

## Verify
- [ ] Tái hiện ca #10642 (TPE.BBBG.01600): mã PULI-KPL-U-D45:09 chọn 17/06/2026 (tương lai) → chặn; MITU-511-713-20 chọn 28/01/2026 (trước ngày xuất 11/03/2026) → chặn; ngày hợp lệ → lưu được.
- [ ] Đối chiếu `status`/floor bằng dữ liệu thật (tinker/DB). Regression: BBBG hàng không có phiếu xuất (HĐ cũ) vẫn lưu được.
- [ ] Verify cả ERP + HRM.

### Checkpoint — 2026-11-26 (wrap up cuối ngày)
Vừa hoàn thành: ERP T1–T4 code xong; push ERP develop_02 `533499f2b7` (HRM: hrm-api `df7be0839c`, hrm-client `684050fc97`, cùng đợt). HRM đã verify đầy đủ BE+FE (xem `HRM/.plans/10642-bbbg-ngay-ban-giao-validate/plan.md`).
Đang làm dở: Verify phía ERP — chưa kiểm form Angular (3 mục Verify ở trên còn [ ] cho ERP).
Bước tiếp theo: tái hiện ca TPE.BBBG.01600 trên màn ERP; gop_db khi user yêu cầu; cập nhật Redmine.
Blocked: (không) — CHƯA gop_db.
