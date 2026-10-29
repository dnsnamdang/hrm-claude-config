# Plan — Phiếu YC nhập trả lại điều chuyển nội bộ tự sinh → "Chờ duyệt"

**Nhánh:** `gop_db` · **Người phụ trách:** @namdangit

## Tasks

- [x] **T1 — Điều tra sự cố 14632** (systematic-debugging): xác định phiếu hoàn trả ĐÃ tự sinh
  (`PYCNH-14530`), gốc lỗi = `createReturnImportRequest()` hard-code `status=3` (DANG_TAO) →
  bị màn list ẩn với người khác người tạo.
- [x] **T2 — Fix code (cả 2 luồng):** `ProductImport::createReturnImportRequest()` đổi
  `status = 3` → `status = ProductImportRequest::CHO_DUYET` (áp cho luồng SL thực nhập < SL xuất
  và luồng hủy đề nghị nhập điều chuyển). `php -l` sạch.
- [x] **T3 — Fix data phiếu 14530:** thêm `UpdateDB::fixReturnTransferRequestStatusChoDuyet_20261005`
  (dry-run pattern), chạy dry-run (quét=1) → chạy thật `(false)` → verify `PYCNH-14530` status=2.
- [x] **T4 — Commit + push nhánh `gop_db`** (commit `10fb09222d`):
  `app/Model/Warehouse/ProductImport.php`, `database/seeds/UpdateDB.php`.
- [x] **T5 — Fix JS crash màn list khi hiện phiếu type 17:** sau khi 14530 hiện ở
  `/product_import_requests/all`, cột "Loại" render `findType(ALL_IMPORT_TYPES, data).name` crash
  (`Cannot read properties of undefined (reading 'name')`) vì `ALL_IMPORT_TYPES` thiếu id 17 →
  cả DataTable không render. Thêm `{id:17, name:"Nhập trả lại điều chuyển"}` (tên chuẩn
  `ImportModel.php:55`) vào `public/js/constant.js`. Constant dùng chung → sửa 1 chỗ, mọi màn list
  dùng `findType(ALL_IMPORT_TYPES,...)` hết crash + lọc được. `node --check` OK.
- [ ] **T6 — Commit + push T5.** Cần deploy để màn live dev-erp hết lỗi.

## Tasks — Đợt 2 (người lập + khoá kho DNNK, 2026-10-05)

- [x] **T7 — "Người lập" phiếu YCNH trả lại điều chuyển tự sinh = kinh doanh lập YCXH:**
  `ProductImport::createReturnImportRequest()` gán tường minh TRƯỚC `save()`:
  `created_by = $product_export_request->created_by` + `department` / `employee_phone` /
  `employee_email` lấy theo `employee_create->info` của YCXH (null-check PHP 7.4). Nhờ guard
  `!$model->created_by` của `BaseModel::creating`, giá trị gán tay không bị `Auth::id()` ghi đè.
  Áp cho cả 2 caller (SL thực nhập < xuất + hủy đề nghị nhập điều chuyển). `php -l` sạch.
- [x] **T8 — Org (cty/phòng/bộ phận) của phiếu type 17 cũng theo người lập YCXH:**
  `ProductImportRequest::boot()` hook `created` — thêm `NHAP_TRA_LAI_DIEU_CHUYEN` vào nhánh
  lấy org từ `product_export_request->employee_create->info` (trước đó chỉ
  `NHAP_DIEU_CHUYEN_KHO_CHI_NHANH`, type 17 rơi vào else = org người thao tác). `php -l` sạch.
- [x] **T9 — Khoá "Chọn kho nhập" trên màn DNNK (WarehouseImportRequest) cho type 17:**
  gốc lỗi = select kho ở `warehouse_import_requests/form.blade.php` KHÔNG bind getter
  `can_change_warehouse` (getter class JS đã có sẵn, trả `arrayInclude([11,7], type)` → false cho
  17) nên luôn cho sửa. Thêm `ng-disabled="!form.can_change_warehouse"` — khớp pattern 3 màn
  xuất + tiền lệ `select2 + ng-disabled` ở bill_commission/bill_bonus. `warehouse_id` kế thừa từ
  YCNH qua `set_on_parent` và gửi từ `submit_data` (object JS, không scrape DOM) nên vẫn submit dù
  select bị khoá.
- [x] **T10 — Commit + push T7-T9** (commit `e4eba915a8`, gộp chung với T11-T12): 3 file —
  `app/Model/Warehouse/ProductImport.php`, `app/Model/Warehouse/ProductImportRequest.php`,
  `resources/views/warehouse/warehouse_import_requests/form.blade.php`.

## Tasks — Đợt 3 (chặn hủy DNNK + PNK luồng trả lại điều chuyển, 2026-10-05)

- [x] **T11 — Chặn hủy DNNK (WarehouseImportRequest) type 17:** `canCancel()` là gate DUY NHẤT dùng
  cho cả FE (ẩn nút "Hủy đề nghị" ở action column, Controller:162) lẫn BE (chặn endpoint
  `warehouseImportRequest.cancel`, Controller:595). Thêm `$this->type != self::NHAP_TRA_LAI_DIEU_CHUYEN`
  vào chuỗi loại trừ (đã có sẵn 3 loại điều chuyển + NHAP_TACH + MUA_HANG_NUOC_NGOAI_MOI). `php -l` sạch.
- [x] **T12 — Chặn hủy PNK (WarehouseImport) type 17:** `canCancel()` cũng là gate DUY NHẤT (FE ẩn
  nút "Hủy" Controller:325, BE chặn endpoint `warehouseImport.cancel` Controller:1853). Thêm
  `self::NHAP_TRA_LAI_DIEU_CHUYEN` vào mảng blacklist `in_array` (đã có các loại điều chuyển +
  NHAP_GHEP + NHAP_TACH). PNK kế thừa `type` từ DNNK cha (`$object->type = $parent->type`,
  Controller:626 & 1596) nên type 17 truyền sang PNK. `WarehouseImport extends ImportModel` → có
  sẵn hằng. `php -l` sạch.
- [x] **T13 — Commit + push T11-T12** (commit `e4eba915a8` trên `gop_db`): 2 file —
  `app/Model/Warehouse/WarehouseImportRequest.php`, `app/Model/Warehouse/WarehouseImport.php`.

## Tasks — Đợt 4 (chọn sẵn kho nhập + kế thừa "xuất thẳng" → "nhập thẳng", 2026-10-05)

- [x] **T14 — Kho nhập của DNNK trả lại điều chuyển = kho xuất YCXH điều chuyển nội bộ (chọn sẵn, khoá):**
  rà soát xác nhận ĐÃ THOẢ từ đợt trước, KHÔNG phải sửa gì. `createReturnImportRequest()` gán
  `warehouse_id = $from_warehouse_id` (kho xuất lấy từ `WarehouseExportRequest` theo YCXH, fallback
  `product_export->warehouse_id`) — ProductImport.php:1855,1863. Endpoint
  `getDataForWarehouseImportRequest` trả `$req->toArray()` có `warehouse_id` → FE copy qua
  `set_on_parent` → form DNNK pre-select `ng-selected="form.warehouse_id == w.id"`, và T9 đã khoá
  (`can_change_warehouse`=false cho type 17). Dropdown dùng `Warehouse::getByCompany()` (kho cùng
  công ty) — điều chuyển nội bộ cùng công ty nên kho nguồn luôn có trong list.
- [x] **T15 — YCXH điều chuyển nội bộ "xuất thẳng" → YCNH trả lại tự sinh cũng "nhập thẳng":**
  `ProductImport::createReturnImportRequest()` thêm `is_import_direct = (bool) $product_export_request->is_export_direct`
  trước `save()` (ProductImport.php, sau khối thông tin người lập). Trước đó `is_import_direct` không
  bao giờ được set → luôn 0 (luồng nhập thường qua DNNK). Giờ YCXH xuất thẳng thì YCNH trả lại nhập
  thẳng (bỏ qua bước DNNK, kế toán kho nhập thẳng PNK sau duyệt — gate ở
  ProductImportRequest.php:1480/1495/1513). Áp cho cả 2 caller (SL thực nhập < xuất + hủy DNNK điều
  chuyển; riêng caller hủy DNNK chỉ xảy ra ở luồng KHÔNG nhập thẳng). `php -l` sạch.
- [x] **T16 — Commit + push T15** (commit `1e1c25d204` trên `gop_db`): `app/Model/Warehouse/ProductImport.php`.

### Checkpoint — 2026-10-05 (đợt 4)
Vừa hoàn thành: T14 (xác nhận kho nhập đã chọn sẵn + khoá, không cần sửa) + T15 (kế thừa xuất thẳng →
nhập thẳng cho YCNH trả lại tự sinh).
Đang làm dở: (không có)
Bước tiếp theo: user deploy + kiểm trình duyệt — YCXH điều chuyển nội bộ loại "xuất thẳng" → sau khi
xuất/hủy, YCNH trả lại tự sinh phải có cờ "nhập thẳng" (vào thẳng luồng kế toán kho nhập PNK, không
hiện bước lập DNNK). YCXH thường → vẫn qua DNNK, ô "Chọn kho nhập" chọn sẵn kho xuất + khoá.
Blocked:

## Tasks — Đợt 5 (sửa bộ trạng thái theo dõi YCXH điều chuyển nội bộ về đúng mốc, 2026-10-06)

**Bối cảnh:** bộ trạng thái "nhập về" của YCXH type 6 (`XUAT_DIEU_KHO_NOI_BO`) gắn SAI mốc ở khúc giữa:
- Mốc **15** "Đang đề nghị nhập" KHÔNG BAO GIỜ được set (store/update DNNK chỉ xử lý
  `BAN_TRA_LAI` / `NHAP_BAN_MUON_TRA_LAI`, bỏ qua type 6).
- Mốc **16** "Đã đề nghị nhập" set QUÁ SỚM ngay lúc phiếu xuất hạch toán tự sinh YCNH
  (`ProductExport:1898`), trong khi spec muốn 16 = lúc **DNNK ở "Chờ duyệt"**.
- Các mốc **14** (phiếu xuất hạch toán), **17** (bắn qua `WarehouseImportRequest::approve()` — hàm
  này CHỈ được gọi từ `WarehouseImportsController::store():790`, tức ĐÚNG lúc tạo PNK), **18**
  (`WarehouseImport::send()`), **19** (phiếu nhập hàng Đang tạo), **5** (terminal) đã ĐÚNG → KHÔNG đụng.

**Ánh xạ mốc đúng (user chốt "ok làm"):** 14 phiếu xuất (ProductExport) đã hạch toán · 15 DNNK
(WarehouseImportRequest) "Đang tạo" · 16 DNNK "Chờ duyệt" · 17 PNK (WarehouseImport) "Đang tạo" ·
18 PNK "Chờ duyệt" · 19 phiếu nhập hàng (ProductImport) "Đang tạo" · 5 "Đã hạch toán".

- [x] **T17 — Gỡ set mốc 16 quá sớm ở ProductExport:** bỏ
  `$product_export_request->status = ProductExportRequest::DA_DE_NGHI_NHAP; save();` tại
  `app/Model/Warehouse/ProductExport.php:1898-1899` (GIỮ NGUYÊN khối tự sinh YCNH). Sau hạch toán
  phiếu xuất, YCXH giữ mốc 14 cho tới khi kế toán kho lập DNNK. `php -l` sạch.
- [x] **T18 — Thêm mốc 15/16 vào DNNK store()+update() cho type 6:** trong
  `WarehouseImportRequestsController` (CẢ `store()` lẫn `update()`): nhánh `status==3` → YCXH =
  `DANG_DE_NGHI_NHAP` (15); nhánh `status==2` → YCXH = `DA_DE_NGHI_NHAP` (16). Chỉ áp khi
  `$import_request->type == NHAP_DIEU_CHUYEN_KHO_NOI_BO` và YCXH `type == XUAT_DIEU_KHO_NOI_BO`.
  Thêm `use App\Model\Warehouse\ProductExportRequest;`. `php -l` sạch.
- [x] **T19 — Xác nhận không đụng 17/18:** 17 ở `WarehouseImportRequest::approve():472` (bắn khi
  tạo PNK qua `$parent->approve()` tại PNK `store():790`) — giữ nguyên. 18 ở
  `WarehouseImport::send():1644` (PNK Chờ duyệt) — giữ nguyên. Không có route duyệt DNNK độc lập.

### Checkpoint — 2026-10-06 (đợt 5)
Vừa hoàn thành: T17 (gỡ set 16 sớm ở ProductExport:1898) + T18 (thêm 15/16 vào DNNK store+update
cho type 6, thêm `use ProductExportRequest`) + T19 (xác nhận 17/18 giữ nguyên). `php -l` sạch 2 file:
`app/Model/Warehouse/ProductExport.php`, `app/Http/Controllers/Warehouse/WarehouseImportRequestsController.php`.
Quyết định data: user CHỐT KHÔNG backfill phiếu dở dang — chỉ sửa code, phiếu mới chạy đúng mốc.
Đang làm dở: (không có)
Bước tiếp theo: user deploy + kiểm trình duyệt chuỗi trạng thái 14→15→16→17→18→19→5 trên 1 YCXH điều
chuyển nội bộ thường (qua DNNK: lưu nháp → gửi → kế toán kho tạo PNK → gửi PNK → hạch toán nhập).
Chưa commit (chờ user yêu cầu).
Blocked:

## Tasks — Đợt 6 (fix NHẬP TRẢ LẠI ĐIỀU CHUYỂN "nhập thẳng" không cộng direct-stock cho NV, 2026-10-09)

**Bối cảnh / bug:** PNH-14638 (type 17 `NHAP_TRA_LAI_DIEU_CHUYEN`, `is_import_direct=1`, đã hạch toán)
trả lại mã CH-SHE-4351 (product 21060) nhưng **"Báo cáo tồn hàng nhập xuất thẳng theo nhân viên"**
KHÔNG cộng SL trả về cho NV nguồn (Nguyễn Văn Mạnh, emp 30): hiện 7, đúng 9 (thiếu +2).

**Root cause (systematic-debugging Phase 1-3):** `ProductImport::updateWarehouse()` chỉ tạo
`product_import_direct_details` (pool tồn thẳng theo NV) ở các nhánh type cụ thể (KHAC/ZITEC/GHÉP,
is_return, NHAP_DIEU_CHUYEN_KHO_CHI_NHANH). Phiếu trả lại điều chuyển nội bộ type 17 có
`has_product_import_request=true` nhưng `is_return=false` → vào hàm nhưng KHÔNG có nhánh tạo
direct-detail → SL trả về chỉ vào tồn kho kế toán, mất ở report (report = SUM direct_details).
Đối xứng: lúc XUẤT điều chuyển đã TRỪ direct-stock của NV này (`ProductExport::updateWarehouse` nhánh
`is_export_direct`, resolve NV = `product_export_request->created_by` tại :1248).

- [x] **T20 — Thêm nhánh type 17 is_import_direct vào `ProductImport::updateWarehouse()`:**
  sau khối `NHAP_DIEU_CHUYEN_KHO_NOI_BO` (chèn sau dòng ~1813), nếu
  `type == NHAP_TRA_LAI_DIEU_CHUYEN && is_import_direct && $product_export_request` → với mỗi product
  gọi `$this->productImportDirectDetail($product, $product_export_request->created_by)` (cộng lại cho
  NV nguồn, đối xứng chiều xuất). `php -l` sạch.
- [x] **T21 — Backfill phiếu cũ (user chốt "2 có"):** method
  `\UpdateDB::backfillDirectStockReturnTransfer_20261009($dryRun=true)` — quét mọi PNH type 17
  is_import_direct đã hạch toán (status=1) thiếu direct-detail (idempotent: bỏ qua detail đã có dòng),
  resolve NV = `product_export_request->created_by`, tái dùng `productImportDirectDetail`. Dry-run trên
  `hrm_erp_test` ra đúng 1 phiếu: PNH-14638 detail#46274 (+2 NV 30). ĐÃ COMMIT `(false)` trên
  `hrm_erp_test`. Verify: product 21060/NV 30 tổng = 9.00 (4 dòng) → report hiện đúng 9.

### Checkpoint — 2026-10-09 (đợt 6)
Vừa hoàn thành: T20 (code fix nhánh type 17 is_import_direct trong `ProductImport::updateWarehouse`,
`php -l` sạch) + T21 (backfill `\UpdateDB::backfillDirectStockReturnTransfer_20261009`, ĐÃ ghi thật
hrm_erp_test, PNH-14638 +2 NV 30, verify tổng=9).
Đang làm dở: (không có)
Bước tiếp theo: user kiểm trình duyệt "Báo cáo tồn hàng nhập xuất thẳng theo nhân viên" — Nguyễn Văn
Mạnh / CH-SHE-4351 phải hiện SL tồn 9. Code `ProductImport.php` + `UpdateDB.php` CHƯA commit git (chờ
user yêu cầu).
Blocked:
