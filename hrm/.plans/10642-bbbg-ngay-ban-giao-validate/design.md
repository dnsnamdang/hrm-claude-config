# #10642 — HRM: chặn Ngày bàn giao BBBG (nghiệm thu)

> Fix song song ERP + HRM. Design nghiệp vụ đầy đủ ở **ERP**: `ERP/.plans/10642-bbbg-ngay-ban-giao-validate/design.md`. File này chỉ ghi phần HRM khác nền.

## Vấn đề
Biên bản bàn giao nghiệm thu (BBBG, màn `/assign/handover-acceptance-records`, entity `Modules\CustomerCare\...\HandoverAcceptanceRecord`): ô **Ngày bàn giao** từng serial (`products[].serials[].handover_date`) đang cho chọn:
- ngày **tương lai** (ca #10642: PULI-KPL-U-D45:09 chọn 17/06/2026, BBBG lập 13/4/2026);
- ngày **trước ngày xuất** (MITU-511-713-20 xuất 11/03/2026 nhưng bàn giao 28/01/2026).

Cần chặn: `floor(product) <= handover_date <= hôm nay`.

## Floor = mốc ngày xuất sớm nhất của hàng
Do **gop_db**, HRM đọc chung bảng ERP, khoá theo `firm_contract_id` + `product_id`:
- Xuất **qua kho**: `warehouse_export_tab_products ⋈ warehouse_exports`;
- Xuất **thẳng** (`product_exports.is_export_direct = 1`): `product_export_tab_products ⋈ product_exports`.

Chỉ phiếu **đã duyệt** = `approved_time IS NOT NULL`; floor = `MIN(approved_time)` gộp 2 nguồn. (Ruling giống ERP — xem plan.md.)

## Quyết định đã chốt
1. **Chỉ áp HĐ hãng (`source = 'firm'`).** HĐ HRM (`source = 'hrm'`, `Modules\Assign\...\Contract`) → fail-open, KHÔNG tính floor. Lý do: id HĐ HRM nằm **chung không gian** với `firm_contract_id` ở các bảng phiếu xuất (va chạm id → floor sai); và luồng xuất HRM chưa ghi ngược dữ liệu phiếu xuất về các bảng bridge (comment đầu `HandoverContractSourceService`). Đây là HRM-analogue của guard `FirmContract` bên ERP.
2. **Fail-open khi hàng chưa có phiếu duyệt** → giữ sửa được BBBG của HĐ cũ.
3. **Câu lỗi:** tương lai dùng lại câu chuẩn `date.before` của màn ("Ngày bàn giao không được lớn hơn ngày hiện tại"); trước floor là câu **nghiệp vụ** riêng ("Ngày bàn giao không được trước ngày xuất kho/xuất hàng (dd/mm/yyyy)") — được phép vì không phải rule phổ biến.
4. **FE:** chặn trên lịch bằng `:disabled-date` (không tương lai + không trước floor); BE validate là chốt chặn thật, trả lỗi inline từng ô.

## Chạm file HRM
- BE entity: `Modules/CustomerCare/Entities/HandoverAcceptanceRecord/HandoverAcceptanceRecord.php` — `exportDateFloors()`, `applyHandoverDateValidation()`.
- BE request: `Modules/CustomerCare/Http/Requests/HandoverAcceptanceRecordRequest.php` — gọi ở cuối `after()`.
- BE service: `Modules/CustomerCare/Services/HandoverContractSourceService.php` — `withExportFloor()` (bơm floor khi chọn HĐ); `HandoverAcceptanceRecordService.php::detail()` — bơm floor khi Sửa.
- FE: `pages/assign/handover-acceptance-records/components/handoverBuild.js` (`makeProduct` giữ `export_date_floor`), `HandoverProductTable.vue` (`disabledDateFor`).
