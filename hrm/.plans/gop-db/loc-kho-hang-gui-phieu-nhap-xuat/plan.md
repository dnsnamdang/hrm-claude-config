# Plan — Lọc kho hàng gửi ở phiếu/yêu cầu nhập–xuất

## Phase 0 — Xác minh (xong)
- [x] Xác nhận type gửi: ERP nhập 14/xuất 12; HRM NHAP_GUI=14, export ===12
- [x] Xác nhận mẫu ERP `getPromoWarehouse()` + accessor `promo_warehouse_ids`
- [x] Xác nhận mẫu HRM `ProductTransferService::warehouseOptions/accWarehouseOptions`
- [x] Cả 3 repo trên nhánh `gop_db`

## Phase 1 — ERP (model + blade Angular filter) — XONG (ERP subagent)
- [x] `Company.php`: accessor get/set `consignment_warehouse_ids` (JSON) — mirror promo
- [x] `Warehouse.php`: `getConsignmentWarehouse()` — kho vật lý gắn kho hàng gửi (mirror getPromoWarehouse); KHÔNG lọc company kho vật lý (đích cross-company)
- [x] `AccountingWarehouse.php`: `consignmentIds($company_id=null)` — id kho kế toán hàng gửi theo công ty (verify tinker cty1=[13,35])
- [x] Partial mới `warehouse/partials/consignment_warehouse_js.blade.php` — `window.CONSIGNMENT_AW_IDS` + `consignmentAccOk(awId,type)`; @include vào @section('script') 4 màn phiếu TRƯỚC controller
- [x] product_import_requests (create/edit): $watch form.type — loại 14 → kho vật lý = getConsignmentWarehouse
- [x] warehouse_import_requests (đề nghị nhập, create/edit): $watch form.type — loại 14 → kho vật lý lọc (else @json($warehouses)=getByCompany)
- [x] product_export_requests (create/edit): create mở rộng $watch + edit thêm $watch — loại 12 → kho vật lý lọc
- [x] warehouse_export_requests (đề nghị xuất, create/edit): $watch form.type — loại 12 → kho vật lý lọc
- [x] product_imports (create/edit): kho kế toán — append `&& consignmentAccOk(val.id, form.type)` (4 site: create:123,162 / edit:75,77)
- [x] product_exports (create/edit): kho kế toán — append `&& consignmentAccOk(val.id, form.type)` (4 site: create:140,206,229 / edit:69,71)
- [x] Verify: 13 blade compile clean (Blade::compileString + php -l); php -l 3 model OK

## Phase 2 — HRM-api (service/controller options)
- [x] Helper dùng chung đọc consignment_ids theo công ty hiện tại — `app/Helper/ConsignmentWarehouseHelper.php` (`consignmentWarehouseIds()`, `isConsignmentVoucherType()`), đăng ký composer + dump-autoload; verify tinker OK. Data test cty1=[13,35] (aw Hàng gửi SG/HP).
- [x] ProductImportRequestService::warehouseOptions(+ Controller::warehouses) — lọc kho vật lý theo type (14) [rule A]
- [x] WarehouseImportRequestController::warehouseImportData — lọc kho vật lý theo `$req->type` (14) [rule B]
- [x] WarehouseImportRequestController::editData — cùng lọc consignment cho form SỬA nháp (14), giữ kho đang chọn [rule B]
- [x] ProductImportController::accountingWarehouses — kho kế toán: 14 chỉ consignment / khác loại trừ [rule E]
- [x] ProductExportRequestController::warehouses — kho vật lý theo type (12) [rule C]
- [x] WarehouseExportRequestController::warehouseExportData — kho vật lý theo `$req->type` (12) [rule D]
- [x] WarehouseExportRequestController::editData — cùng lọc consignment cho form SỬA nháp (12), giữ kho đang chọn [rule D]
- [x] ProductExportController::productExportData — kho kế toán: 12 chỉ consignment / khác loại trừ [rule F]

## Phase 3 — HRM-client (FE truyền type + phản ứng đổi type)
- [x] product-import-requests form (ProductImportRequestForm.vue): loadWarehouses truyền `type`; watch form.type → refetch + clear warehouse_id [rule A]
- [x] product-export-requests form (ProductExportRequestForm.vue): fetchWarehouses truyền `type` (create-data); onTypeChange → refetch + clear warehouse_id [rule C]
- [x] warehouse-import-requests form — KHÔNG cần FE: type suy từ YC nguồn ở BE [rule B]
- [x] product-imports form — KHÔNG cần FE: type suy từ chứng từ nguồn ở BE (accountingWarehouses) [rule E]
- [x] warehouse-export-requests form — KHÔNG cần FE: type suy từ YC nguồn ở BE [rule D]
- [x] product-exports form — KHÔNG cần FE: type suy từ chứng từ nguồn ở BE (productExportData) [rule F]

## Phase 4 — Kiểm thử
- [x] Query-level verify (tinker, cty1=[13,35]): rule A → kho vật lý 4(SG)/7(HP) cross-company; rule E → nhập gửi chỉ aw#13, loại thường 0 (loại trừ hàng gửi)
- [x] Playwright HRM YC nhập hàng: chọn "Nhập gửi" → GET warehouses?type=14 → Kho nhập chỉ [HP, SG]; 0 lỗi liên quan
- [x] Playwright HRM YC xuất hàng: chọn "Xuất gửi" → GET create-data?type=12 → Kho xuất chỉ [HP, SG]
- [~] Console errors còn lại đều là cảnh báo prop `rows="2"` (String vs Number) của V2BaseTextarea — CÓ SẴN, không liên quan feature
- [x] ERP code xong (16 file: 3 model + 1 partial mới + 12 blade) — blade compile clean; data verify cty1=[13,35]→kho vật lý 4/7
- [x] Review diff ERP (main): 3 model đúng (getConsignmentWarehouse KHÔNG lọc company kho vật lý → cross-company OK; consignmentIds lọc accounting theo company OK); partial consignmentAccOk gửi=chỉ hàng gửi/khác=loại trừ; 8 site accounting product_imports/exports + 12 $watch kho vật lý (create+edit) đúng; 13 view compile clean; tinker cty1 consignmentIds=[13,35]→vật lý [4,7]
- [x] ERP smoke test qua trình duyệt (:8001, Playwright MCP) — 6/6 rule đạt:
      • A YC nhập hàng: type 14 → kho [SG,HP]; đổi type 2 → khôi phục 7 kho
      • C YC xuất hàng: type 12 → kho [SG,HP]; đổi type khác → 7 kho
      • B Đề nghị nhập kho: type 14 → [SG,HP] / type thường → 7
      • D Đề nghị xuất kho: type 12 → [SG,HP] / type thường → 7
      • E phiếu nhập: consignmentAccOk(13,14)=true, (13,2)=false, (1,14)=false, (1,2)=true
      • F phiếu xuất: consignmentAccOk(13,12)=true, (13,16)=false, (1,12)=false; CONSIGNMENT_AW_IDS=[13,35]
      Lưu ý: ERP chạy port :8001 (KHÔNG phải :8000 — đó là HRM-API)

## Ghi chú kỹ thuật (bẫy đã xử lý)
- Kho hàng gửi (accounting) thuộc CÔNG TY khai báo, nhưng kho vật lý ĐÍCH có thể ở công ty khác
  (aw#13 cty1 → kho SG cty4; aw#35 cty1 → kho HP cty2). Vì vậy filter kho VẬT LÝ cho loại gửi
  KHÔNG được lọc thêm theo company_id của bảng `warehouses` (mirror ERP getPromoWarehouse).
  Đã sửa `ProductImportRequestService::warehouseOptions` tách nhánh gửi (bỏ company filter kho vật lý).
  B/C/D vốn không lọc company kho vật lý nên đúng sẵn. E/F lọc accounting theo company là ĐÚNG
  (accounting thuộc công ty).
- Form SỬA nháp (editData) của Đề nghị nhập/xuất kho ban đầu KHÔNG lọc consignment (chỉ create-data
  lọc) → lỗ hổng cho phép chọn kho ngoài phạm vi khi sửa nháp loại 14/12. Đã bổ sung cùng bộ lọc vào
  `WarehouseImportRequestController::editData` + `WarehouseExportRequestController::editData`, GIỮ kho
  đang chọn qua `orWhere('id', warehouse_id)`. Bên ERP tương đương: `$watch('form.type')` chạy cả lúc
  load form edit → tự thu hẹp kho vật lý về getConsignmentWarehouse cho loại gửi (không cần sửa thêm).
