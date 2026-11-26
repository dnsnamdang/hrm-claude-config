# #10642 — BBBG: chặn "Ngày bàn giao" từng hàng sai (ERP + HRM)

> Placeholder — sẽ fill sau khi: (1) Explore agent trả nguồn ngày PXK/xuất thẳng theo hàng, (2) user chốt mốc min (sớm/muộn nhất) + phạm vi 2 bên.

## Vấn đề
BBBG (CSKH, `/customer-care/handover_acceptance_records`): cột **Ngày bàn giao** (`serials[].handover_date`) từng dòng hàng cho chọn:
- ngày **tương lai** (sau hôm nay);
- **trước ngày phiếu xuất kho** của hàng đó (xuất thẳng: trước **ngày phiếu xuất hàng**).

## Gốc rễ (đã kiểm tới gốc 2026-11-26)
- **BE ERP** `app/Http/Requests/CustomerCare/HandoverAcceptanceRecordStoreRequest.php` + `...UpdateRequest.php`: `products.*.serials.*.handover_date => 'required'` — không có `before_or_equal:today`, không có mốc min theo ngày xuất.
- **BE HRM** `Modules/CustomerCare/Http/Requests/HandoverAcceptanceRecordRequest.php` (~dòng 87): `handover_date => [required/nullable, date_format:Y-m-d]` — chỉ kiểm định dạng.
- **FE ERP** `resources/views/customercare/handover_acceptance_records/form.blade.php` (dòng 200, 235) + directive `dateForm` (`public/js/angular/app.directive.js:340`): `max-today="true"` chỉ set `maxDate` cho datetimepicker → chặn click lịch, KHÔNG chặn gõ tay; không có `minDate`.
- **Dữ liệu**: product đổ vào form lấy từ `FirmContractService::getProductsSummary()` (`app/Services/Sale/Firm/Contract/FirmContractService.php:1704`) — chỉ tổng SL, KHÔNG có ngày xuất → cần bổ sung lấy ngày PXK/xuất thẳng theo từng hàng.

## Phạm vi
Cả **ERP** (model `Customers\HandoverAcceptanceRecord`) và **HRM** (Module `CustomerCare`) — cùng lỗ hổng.

## Nguồn ngày xuất theo từng hàng (Explore agent, 2026-11-26)
Cho (firm_contract_id = contractable_id của BBBG, product_id):

**a) Hàng QUA KHO → ngày phiếu xuất kho (PXK):** bảng `warehouse_export_tab_products` (cột `warehouse_export_id`, `firm_contract_id`, `product_id`) join `warehouse_exports`. Ngày phiếu = `warehouse_exports.approved_time` (ngày duyệt/thực xuất) hoặc `created_at` (ngày lập) — cast Carbon qua `$dates` ở `ExportModel.php:119`. `warehouse_exports` KHÔNG có cột `date` riêng.

**b) Hàng XUẤT THẲNG → ngày phiếu xuất hàng:** KHÔNG phải loại `type` riêng mà là flag `is_export_direct=1` trên `product_exports`. Bảng dòng hàng `product_export_tab_products` join `product_exports` (where `is_export_direct=1`). Ngày = `product_exports.approved_time`/`created_at` (`ProductExport.php:60`).

Phân biệt: `is_export_direct=0` ⇒ phiếu product_exports gắn 1 PXK thật (`warehouse_export_id` unique); `=1` ⇒ không qua kho.

**Query mẫu** (theo `WarehouseExportsController.php:423-444`): join 2 nguồn, lấy MIN/MAX `approved_time`/`created_at`. Caveat: `we.status`/`pe.status`=1 nghĩa "đã duyệt" (suy từ searchByFilter, CHƯA có bảng hằng số → cần đối chiếu dữ liệu thật); HĐ hãng cũ trước cơ chế tab có thể chỉ có `warehouse_export_lots` + `warehouse_exports.firm_contract_id` (chưa kiểm data lịch sử).

Ghi chú: `resolveHandoverDate`/`resolveDetailHandoverDate` (`HandoverAcceptanceRecord.php:721-759`) hiện KHÔNG lấy ngày từ PXK/PXH — nếu cần dùng làm nguồn/mốc thì bổ sung query ở đây.

## Quyết định đã chốt
1. ✅ Mốc min = ngày xuất **sớm nhất** (A) — 1 mã xuất nhiều đợt chỉ cần bàn giao sau lần xuất ĐẦU TIÊN.
2. ✅ Dùng **`approved_time`** (ngày duyệt/thực xuất) làm ngày phiếu. Nếu `approved_time` null (chưa có) → fallback `created_at`.
3. ✅ Xuất thẳng: nguồn `product_exports` (`is_export_direct=1`) + `product_export_tab_products`.
4. ✅ Làm cả 2 bên ERP + HRM.

## Rule validate chốt (áp cho từng `serials[].handover_date`)
- **Không tương lai:** `handover_date <= hôm nay` (so với ngày máy chủ). (ô `date` biên bản đã có, nay thêm cho từng serial.)
- **Không trước ngày xuất:** `handover_date >= floor(product)` với `floor(product)` = MIN(`approved_time` ?? `created_at`) trên cả 2 nguồn (PXK qua kho + PXH xuất thẳng) của (contract, product), lọc phiếu đã duyệt (`status=1`, đối chiếu dữ liệu thật khi test).
- **Fail-open mốc min:** nếu 1 product KHÔNG tìm thấy phiếu xuất nào (HĐ cũ trước cơ chế tab / chưa xuất) → BỎ check min cho product đó (vẫn check max=today). Tránh chặn nhầm BBBG hợp lệ của dữ liệu lịch sử.
- So sánh theo NGÀY (bỏ giờ). Cho phép bằng (>= / <=).

## Thiết kế cài đặt

### Nguồn floor dùng chung (ERP + HRM đọc cùng bảng do gop_db)
Hàm MỚI (không sửa hàm dùng chung) nhận (firm_contract_id, product_ids[]) → map `product_id => Carbon floor`:
- union 2 query: `warehouse_export_tab_products ⋈ warehouse_exports` và `product_export_tab_products ⋈ product_exports(is_export_direct=1)`, lọc status duyệt, `GROUP BY product_id` lấy `MIN(COALESCE(approved_time, created_at))`.
- ERP: đặt ở service/model Customercare (vd `HandoverAcceptanceRecord::exportDateFloors()` static, hoặc service riêng). HRM: hàm tương ứng trong Module CustomerCare (Service).

### BE validate
- **ERP** `HandoverAcceptanceRecordStoreRequest` + `UpdateRequest`: trong `withValidator()->after()` (đã có vòng lặp products/serials) — thêm: tính floors 1 lần, với mỗi serial add lỗi `products.{k}.serials.{ks}.handover_date` nếu > today hoặc < floor. Thêm message.
- **HRM** `HandoverAcceptanceRecordRequest`: tương tự trong `after()` (đã có sẵn vòng lặp qty).

### FE (chặn thao tác + báo lỗi inline)
- Bơm `export_date_floor` (dạng d/m/Y hoặc ISO) theo từng product vào payload `getDataForHandoverAcceptanceRecord` (ERP) / API nguồn BBBG (HRM) — thêm vào map product đang có.
- ERP `form.blade.php`: input handover_date hiện dùng directive `dateForm` với `max-today="true"`. Cần (a) chặn GÕ TAY ngày tương lai + trước floor, (b) set `minDate` theo floor.
  - ⚠️ **Điểm cần xác nhận khi review:** directive `dateForm` (`app.directive.js`) là **dùng chung**. Phương án đề xuất: thêm hỗ trợ **opt-in** thuộc tính `min-date` (chỉ kích hoạt khi có attr → backward-compatible), và validate giá trị gõ tay trong `$parsers` (reject nếu ngoài [floor, today]). Vì đụng directive dùng chung → chốt lại ở bước duyệt design.
- HRM client (Nuxt): component date-picker của BBBG set `:min`/`:max` + validate — theo convention component có sẵn (không đụng directive Angular).

## Rủi ro / lưu ý
- `status=1` chưa có bảng hằng số khẳng định "đã duyệt" → khi test đối chiếu dữ liệu thật.
- HĐ hãng cũ chỉ có `warehouse_export_lots` (không có tab_products) → floor rỗng → fail-open (đã xử lý).
- Không trust client: floor + rule check LẠI ở BE (authoritative); FE chỉ để UX.
