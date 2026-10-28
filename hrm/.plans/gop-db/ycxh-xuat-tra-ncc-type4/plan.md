# YCXH loại 4 — Xuất trả nhà cung cấp (XUAT_TRA_NCC) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Thêm loại xuất 4 (Xuất trả nhà cung cấp) vào luồng YCXH của HRM, port 1:1 từ ERP, cả 2 chuỗi direct + non-direct, nguồn YCNH, hạch toán Nợ 3311/Có 156/Có 33311.

**Architecture:** Nguồn = `Modules/Finance` ProductImportRequest (YCNH). YCXH `Modules/Assign` gắn `product_import_request_id`. Giá vốn dùng `WarehouseExportAccountingService` sẵn có; hạch toán thêm nhánh loại 4 trong `ProductExportPostingService`; side-effect trả hàng chèn ở 2 đường finalize `ProductExportService`.

**Tech Stack:** PHP 7.4 / Laravel 8 (hrm-api), Nuxt 2 / Vue 2 (hrm-client), MySQL `erp_hrm_check` (local).

**Spec:** `docs/superpowers/specs/gop-db/2026-10-17-ycxh-xuat-tra-ncc-type4-design.md`

## Global Constraints

- **LÀM ĐÚNG ERP, KHÔNG TỰ BỔ SUNG** — mỗi code path port verbatim theo dòng ERP đã dẫn; ERP lệch/thiếu ở đâu thì HRM lệch/thiếu y hệt. Không lấp khoảng trống, không thêm nhánh/loại/field ngoài ERP.
- **canSupplierReturn chỉ 5 loại YCNH {1 NGOAI, 2 TRONG_NUOC, 12 TRONG_NUOC_MOI, 13 HDNT, 15 TU_DO}** — không thêm loại 11.
- **DB prod `hrm_erp_gop` CHỈ ĐỌC.** Mọi ghi/test chỉ trên `erp_hrm_check`. Trước mọi tinker: `grep DB_DATABASE .env`. Mọi script test: transaction + rollback + guard `if (DB::connection()->getDatabaseName() !== 'erp_hrm_check') exit(1);`.
- **Không migration, không quyền mới, không `mysql2`/`DB_CONNECTION_SECOND`.** Bảng trùng tên ưu tiên bản ERP.
- **Không commit/push** tới khi user yêu cầu.
- **FE theo skill UI HRM**: `V2Base*`, `V2BaseFormCard` cho nhóm kho/xuất nhập, badge màu BE trả, nút ẩn-hẳn theo điều kiện, số định dạng quốc tế (`,` nghìn `.` thập phân), tiếng Việt.
- Atomic `increment`/`decrement` cho mọi thay đổi tồn/qty (bài học lost-update BorrowSell).
- `UpdateDB` global namespace: `new \UpdateDB` khi cần script data.

## Review Focus

1. **Trả quá SL còn lại khi SỬA phiếu** (bug I-1 loại 15): per-line guard phải loại self (`excludeRequestId = $req->id` ở update, `null` ở create) → không tự chặn/tự đếm phiếu đang sửa. (Task 4)
2. **YCNH loại 12/13 side-effect**: loại 12 phải trừ CẢ `arrived_qty` lẫn `allocated_qty`; loại 13 chỉ `allocated_qty`; loại 1/2/15 KHÔNG đụng arrived/allocated. Quên = tồn/phân bổ drift. (Task 5)
3. **VAT = 0**: dòng `vat_percent = 0` KHÔNG sinh bút toán Có 33311, Nợ 3311 chỉ = giá vốn. (Task 6)
4. **supplier_id direct vs non-direct**: resolve qua 2 path (`warehouse_export->warehouse_export_request->product_export_request->...` khi non-direct; `product_export_request->...` khi direct) → sai path = dimension NCC NULL, lệch công nợ. (Task 6, 7)
5. **Giá vốn loại 4 bị ép 0**: nếu nhánh tạo dòng dùng chung với loại 15 (`export_price => 0` tại `ProductExportRequestService.php:1609`) thì loại 4 phải đi nhánh riêng giữ giá vốn bình quân. (Task 3, 4)

---

## Lưu ý về "test" trong codebase này

HRM không chạy TDD PHPUnit cho luồng này. **Bước "test" = script tinker trên `erp_hrm_check`** (transaction + rollback + guard), hoặc **gọi HTTP có JWT**, hoặc **Playwright MCP** cho FE — đúng cách loại 15 đã verify. Mỗi task nêu rõ script/kịch bản kiểm. Script test ghi vào scratchpad `scratchpad/sdd-type4/`, KHÔNG vào `.plans/`.

Khi port: implementer **BẮT BUỘC mở file ERP tại dòng đã dẫn và port verbatim**, chỉ đổi: namespace, tên model Eloquent HRM, tên quan hệ/cột HRM. Không diễn giải lại logic.

---

### Task 1: `canSupplierReturn()` + `getDataForReturn()` trên Finance ProductImportRequest

**Files:**
- Modify: `Modules/Finance/Entities/ProductImportRequest/ProductImportRequest.php`
- Test script: `scratchpad/sdd-type4/t4-task1.php`

**Interfaces:**
- Produces: `ProductImportRequest::canSupplierReturn(): bool`; `ProductImportRequest::getDataForReturn(): array|Collection` (mỗi phần tử có `product_id, unit_id, order_import_detail_id, inland_notify_detail_id, rule_inland_notify_detail_id, vat_percent, qty, allocated_price`).
- Consumes: quan hệ sẵn có `products()` (:852), `supplier()` (:894), hằng trạng thái (:57+), hằng loại mua hàng (MUA_HANG_NUOC_NGOAI=1, MUA_HANG_TRONG_NUOC=2, MUA_HANG_TRONG_NUOC_MOI=12, MUA_HANG_TRONG_NUOC_HDNT=13, MUA_HANG_TRONG_NUOC_TU_DO=15), status DA_HACH_TOAN=5.

- [x] **Step 1: Mở ERP source** `TanPhatDev/app/Model/Warehouse/ProductImportRequest.php:1536-1549` (canSupplierReturn) và `:784-847` (getDataForReturn). Mở mẫu HRM `Modules/Finance/Entities/ProductImportRequest/ProductExportRequest.php:195-216` để bám style.

- [x] **Step 2: Port `canSupplierReturn()`** — trả true khi: `is_complete` && `status == 5` && `created_by == auth()->id()` && `type ∈ {1,2,12,13,15}` && KHÔNG tồn tại YCXH `product_export_requests.type=4 AND product_import_request_id=$this->id AND is_completed=0`. Dùng `\Modules\Assign\Entities\Warehouse\ProductExportRequest` để đếm YCXH dở.

- [x] **Step 3: Port `getDataForReturn()`** — lặp `products()`: CHỈ dòng `imported_qty > returned_qty`; `qty = imported_qty - returned_qty`; map `product_id, unit_id, order_import_detail_id, inland_notify_detail_id, rule_inland_notify_detail_id, vat_percent`, `allocated_price = supplier_price`.

- [x] **Step 4: Viết test** `t4-task1.php` (guard + transaction + rollback): lấy 1 YCNH status 5 loại ∈ {1,2,12,13,15} của 1 emp → `Auth::loginUsingId(created_by)` → assert `canSupplierReturn()===true`; lấy 1 YCNH loại 11 → assert `false`; `getDataForReturn()` chỉ trả dòng `imported_qty>returned_qty` và có đủ 3 cột khóa.
  - BẪY: phải `Auth::login` trước vì canSupplierReturn so `created_by` với `auth()->id()`.

- [x] **Step 5: Chạy test** `php artisan tinker --execute="require 'scratchpad/sdd-type4/t4-task1.php';"` (sau khi `grep DB_DATABASE .env` = erp_hrm_check). Expected: 3 assert PASS, rollback.

---

### Task 2: API `data-for-supplier-return` + search YCNH đủ điều kiện

**Files:**
- Modify: `Modules/Finance/Http/Controllers/.../ProductImportRequestController.php` (+ `Routes/api.php` của Finance)
- Test script: gọi HTTP (curl + JWT)

**Interfaces:**
- Consumes: `ProductImportRequest::canSupplierReturn()`, `getDataForReturn()` (Task 1).
- Produces: `GET .../product-import-requests/{id}/data-for-supplier-return` → `{supplier, products:[...]}`; endpoint search YCNH (type order, status 5, của người lập) cho modal.

- [x] **Step 1: Mở ERP** `ProductImportRequestsController.php:1375` (getDataForSupplierReturn) + search `create.blade.php:454-486` để biết filter.

- [x] **Step 2: Thêm route + method** `dataForSupplierReturn($id)`: load YCNH, nếu `!canSupplierReturn()` → `abort(422,'Không thể trả hàng cho yêu cầu này!')`; else trả `getDataForReturn()` + thông tin NCC. Gắn middleware auth sẵn có của module; KHÔNG thêm quyền mới.

- [x] **Step 3: Thêm/điều chỉnh search** YCNH đủ điều kiện (reuse search có sẵn + filter `status=5`, `created_by=auth`, loại ∈ {1,2,12,13,15}).

- [x] **Step 4: Test HTTP** — lấy JWT 1 emp có YCNH hợp lệ, `curl` endpoint → 200 + products đúng; gọi với YCNH không hợp lệ → 422. Ghi lệnh vào `scratchpad/sdd-type4/t4-task2.sh`.

---

### Task 3: `CREATABLE_TYPE_IDS += 4` + `createFromSupplierReturn` (tạo YCXH loại 4)

**Files:**
- Modify: `Modules/Assign/Entities/Warehouse/ProductExportRequest.php` (CREATABLE_TYPE_IDS :73)
- Modify: `Modules/Assign/Services/ProductExportRequestService.php` (createFromRequest :309-330)
- Test script: `scratchpad/sdd-type4/t4-task3.php`

**Interfaces:**
- Consumes: YCXH đã có `XUAT_TRA_NCC=4` (:25), quan hệ `productImportRequest()` (:306).
- Produces: `createFromSupplierReturn($data)` — tạo YCXH type 4 với `product_import_request_id`, kho thường, dòng chi tiết đủ 3 cột khóa + `vat_percent`, **export_price giữ giá trị nguồn (KHÔNG ép 0)**.

- [x] **Step 1: Thêm `4` vào `CREATABLE_TYPE_IDS`** (:73).

- [x] **Step 2: Mở ERP** `ProductExportRequest::syncProducts:2170-2220` (ghi 3 cột khóa) + rule store `ProductExportRequestsController.php:461, ~470-490` (require product_import_request_id; transition_type khi non-direct + có giao hàng).

- [x] **Step 3: Thêm nhánh `createFromSupplierReturn`** trong `createFromRequest` cho `type == 4` (trước khi rơi vào `createManual`). Ghi dòng kèm `order_import_detail_id, inland_notify_detail_id, rule_inland_notify_detail_id, vat_percent`. `warehouse_id` lấy từ danh sách kho thường (`ProductExportRequestController.php:199-215`), KHÔNG `promoWarehouseOptions`. KHÔNG ép `export_price=0` (khác loại 15 :1609).

- [x] **Step 4: Rule non-direct + giao hàng** — nếu `!is_export_direct` && loại 4 có giao hàng ⇒ bắt `transition_type` (port rule ERP).

- [x] **Step 5: Test** `t4-task3.php` (guard+transaction+rollback): dựng payload từ `getDataForReturn()` của 1 YCNH hợp lệ → gọi create → assert YCXH.type=4, `product_import_request_id` đúng, chi tiết có đủ 3 cột khóa + vat, `warehouse_id` thuộc kho thường, `export_price != 0`. Rollback.

---

### Task 4: Guard gửi duyệt + per-line SL (loại self khi sửa)

**Files:**
- Modify: `Modules/Assign/Services/ProductExportRequestService.php`
- Test script: `scratchpad/sdd-type4/t4-task4.php`

**Interfaces:**
- Consumes: `createFromSupplierReturn` (Task 3), `canSupplierReturn` (Task 1).
- Produces: `assertSupplierReturnCanExport($req)`; `assertSupplierReturnLineQtyWithinRemaining($line, $pir, ?int $excludeRequestId)`.

- [x] **Step 1: Mở khuôn loại 15** `assertFirmContractCanExportPromotion:1629`, `assertComboLineQtyWithinRemaining:1669`, `comboInFlightQtyByRow:1750`. Mở ERP guard `validateProducts:2026`.

- [x] **Step 2: `assertSupplierReturnCanExport`** — gate cấp phiếu: YCNH nguồn `canSupplierReturn()`; có ≥1 dòng need_export qty>0. Lỗi → ValidationException (rethrow, không catch chung).

- [x] **Step 3: `assertSupplierReturnLineQtyWithinRemaining`** — mỗi dòng tìm `ProductImportRequestDetail` theo parent YCNH + product_id + unit_id + 3 cột khóa; lỗi nếu `!found || imported_qty - returned_qty - inFlight < qty` → "Số lượng xuất không hợp lệ!". `inFlight` = tổng qty các YCXH loại 4 khác CHƯA hoàn tất trên cùng dòng, **loại self qua `excludeRequestId`**.

- [x] **Step 4: Gắn guard vào create (excludeRequestId=null) và update (excludeRequestId=$req->id)** — đúng pattern fix I-1: ở update `$req->save()` ghi status trước khi xóa dòng cũ nên phải loại self.

- [x] **Step 5: Test** `t4-task4.php`: (a) dòng qty > (imported-returned) → THROW; (b) đúng remaining → PASS; (c) **sửa phiếu đang giữ remaining**: excludeRequestId=null → THROW (tái hiện bug), excludeRequestId=self → PASS (fix). Rollback.

---

### Task 5: Side-effect finalize PXH (cả 2 đường)

**Files:**
- Modify: `Modules/Assign/Services/ProductExportService.php`
- Test script: `scratchpad/sdd-type4/t4-task5.php`

**Interfaces:**
- Consumes: PXH loại 4 tạo từ YCXH (Task 3), `$isFinalize` (:203).
- Produces: side-effect khi finalize — `returned_qty +=`, type12 `arrived_qty/allocated_qty -=`, type13 `allocated_qty -=`, `exported_qty +=`, YCXH status 5.

- [x] **Step 1: Mở ERP** `ProductExport::updateWarehouse:1803-1830`. Mở HRM 2 đường: non-direct `createFromWarehouseExport` finalize `:371-428` (loại 15 ghi exported_qty :400-419); direct `createFromProductExportRequest` finalize `:672-693`.

- [x] **Step 2: Chèn khối loại 4** ngay sau bước loại 20 ở **cả hai** đường, chạy khi `$isFinalize && type==4`. Mỗi dòng PXH khớp YCNH theo product_id + unit_id + 3 cột khóa:
  - `ProductImportRequestDetail::where(...)->increment('returned_qty', $qty)` (mọi loại);
  - YCNH loại 12: `contract_detail->decrement('arrived_qty',$qty)` + `decrement('allocated_qty',$qty)` (summary_detail/summary_product — port đúng quan hệ ERP);
  - YCNH loại 13: `decrement('allocated_qty',$qty)`;
  - `ProductExportRequestDetail->increment('exported_qty',$qty)`;
  - YCXH `status=5` + `is_completed=1`.
  - Dùng atomic increment/decrement.

- [x] **Step 3: Test** `t4-task5.php` (guard+transaction+rollback): finalize 1 PXH loại 4 nguồn YCNH loại 2 → assert `returned_qty += qty`, `exported_qty += qty`, YCXH status=5, arrived/allocated KHÔNG đổi. Lặp với YCNH loại 12 → arrived & allocated giảm; loại 13 → chỉ allocated giảm. Rollback.

---

### Task 6: Hạch toán loại 4 (`ProductExportPostingService`) + map HĐ 2/15

**Files:**
- Modify: `Modules/Assign/Services/ProductExportPostingService.php` (getDataProductExportAccounting :259-311, throw :309)
- Modify: `Modules/Assign/Http/Controllers/.../ProductExportController.php` (map HĐ sau updateWarehouse)
- Test script: `scratchpad/sdd-type4/t4-task6.php`

**Interfaces:**
- Consumes: PXH loại 4 đã trừ kho + có `export_price` (via `WarehouseExportAccountingService::updateWarehouse`).
- Produces: nhánh hạch toán type 4 → mảng accounts Nợ 3311/Có 156/Có 33311.

- [x] **Step 1: Mở ERP** `ProductExport.php:764-786` (accounting loại 4) + `ProductExportsController.php:868-880, 1479-1490` (map HĐ). Mở HRM `getDataProductExportAccounting:259-311`, mẫu dimension supplier `:222-228`, nhánh loại 15 `:294` + `costAccounting:353`.

- [x] **Step 2: Thêm nhánh type 4** (cạnh :294, bỏ throw :309 cho type 4). Mỗi dòng: `supplier_id` resolve = non-direct `warehouse_export->warehouse_export_request->product_export_request->product_import_request->supplier_id`, direct `product_export_request->product_import_request->supplier_id`; `giamua = export_price*qty*unit_coefficient`; `vat = vat_percent>0 ? giamua*vat_percent/100 : 0`:
  - `createDataSaveDept($accounts, 3311, giamua+vat, TYPE_DEPT, [156,33311], ['supplier_id'=>supplier_id])`;
  - `createDataSaveDept($accounts, 156, giamua, TYPE_HAS, [3311], ['product_id'=>product_id])`;
  - nếu `vat_percent>0`: `createDataSaveDept($accounts, 33311, vat, TYPE_HAS, [3311])`.
  - (Số hiệu TK theo đúng ERP; không tra config công ty.)

- [x] **Step 3: Map HĐ hạch toán** sau `updateWarehouse` — CHỈ: loại 2 → `InlandBuyContract` (product_arrived_notify->inland_buy_contract_id); loại 15 → `InlandBuyContractNew` (inland_product_arrived_new->inland_buy_contract_new_id). Loại 1/12/13 KHÔNG map.

- [x] **Step 4: Test** `t4-task6.php` (guard+transaction+rollback): build accounting cho PXH loại 4 (1 dòng vat>0, 1 dòng vat=0) → assert: có Nợ 3311 = Σ(giamua+vat) dim supplier; Có 156 = Σgiamua dim product; Có 33311 = Σvat (dòng vat=0 KHÔNG sinh 33311); không có 511/632. Rollback.

---

### Task 7: hiển thị loại 4 — helper resolve HĐ+NCC (2/15) ✅ XONG

> **RULING T7-R-display-type:** plan gốc ghi "2/12" là LỖI. ERP `ProductExportsController.php:1701-1712` chỉ map loại nhập 1/2/15 (KHÔNG 12); modal YCXH loại 4 chỉ surface YCNH {2,15}; map hạch toán Task 6 cũng 2/15 → helper resolve **2/15**, bỏ nhánh 12 (code pre-existing lệch ERP + chết cho loại 4).

**Files:**
- Modify: `Modules/Assign/Http/Controllers/.../ProductExportController.php` (khối fillContractDisplay loại 4 :587-611 + helper mới)

**Interfaces:**
- Consumes: PXH loại 4 (quan hệ product_import_request).
- Produces: `supplier_code, supplier_name, contract_code` cho loại 4 (KHÔNG contract_link).

- [x] **Step 1: Đọc ERP** show loại 4 (:1701-1712) + HRM khối cũ :587-611 (type 2 → inland_buy_contracts; type 12 SAI → thay bằng 15).

- [x] **Step 2: Tách helper** `resolveSupplierReturnInfo($productImportRequestId)`: supplier từ `customers` qua YCNH.supplier_id; contract_code theo loại **2** (notify_id→product_arrived_notifies.inland_buy_contract_id→inland_buy_contracts.code) / **15** (inland_product_arrived_new_id→inland_product_arrived_news.inland_buy_contract_new_id→inland_buy_contract_news.code). KHÔNG `contract_link`.

- [x] **Step 3: Gọi helper** trong khối loại 4 của fillContractDisplay, giữ `displayFillMissing`.

- [x] **Step 4: Test** `scratchpad/sdd-type4/t4-task7.php` (Reflection, guard erp_hrm_check, CHỈ ĐỌC): PASS 4/4 (loại 2, loại 15, id=0, id=null). Review 2 verdict APPROVED, 0 finding.

---

### Task 8: FE — form YCXH loại 4 + modal chọn YCNH + field-relevance

**Files:**
- Modify: `pages/finance/product-export-requests/components/ProductExportRequestForm.vue`
- Modify: `pages/finance/product-export-requests/field-relevance.js`
- Modify: `pages/finance/warehouse-export-requests/create.vue` (nếu chuỗi non-direct cần)
- Modal chọn YCNH (component theo khuôn modal HRM)

**Interfaces:**
- Consumes: API `data-for-supplier-return` + search YCNH (Task 2); show (Task 7).

- [x] **Step 1: Mở khuôn loại 15** (`ProductExportRequestForm.vue`, `field-relevance.js`) để bám. Đọc skill `.claude/skills/erp-to-hrm-screen/SKILL.md`, `modal-popup`, `form-validate`, `select-and-input-state`.

- [x] **Step 2: Dropdown loại** thêm option `{id:4,'Xuất trả nhà cung cấp'}`.

- [x] **Step 3: Modal chọn YCNH** (dùng `V2BaseModal` + `V2BaseSelectInModal`): search YCNH đủ điều kiện → chọn → gọi `data-for-supplier-return` → đổ bảng hàng trả (SL ≤ imported-returned, hiển thị NCC, giá hiển thị). Select server-side có limit (hiệu năng).

- [x] **Step 4: `field-relevance.js`** khai field hiện cho type 4 (nguồn YCNH, NCC, bảng hàng, kho thường, transition_type nếu non-direct).

- [x] **Step 5: Validate realtime** `V2Base*` + vee-validate; SL vượt remaining → đỏ dưới ô, KHÔNG tự kéo min/max. Nút ẩn-hẳn theo điều kiện.

- [x] **Step 6: Test Playwright MCP** (`http://127.0.0.1:3000`): tạo YCXH loại 4 từ 1 YCNH hợp lệ → lưu nháp → gửi duyệt; kiểm modal YCNH lọc đúng, bảng hàng đúng remaining, submit về danh sách.

---

## Checkpoint cuối

- [x] **Final whole-branch review** (subagent, model mạnh nhất): rà toàn diff loại 4 — Review Focus 1-5, parity ERP (không tự thêm nhánh/loại), guard self-exclude, side-effect per-type, VAT=0, supplier resolve 2 đường, giá vốn ≠ 0.
- [x] Dọn test records trên `erp_hrm_check` (script có guard), cập nhật `plan.md` [x] + STATUS + checkpoint.
- [x] Chờ user duyệt commit → ĐÃ commit+push develop: hrm-api b17e77e6a, hrm-client 24a03e33e (17/10).

---

### Checkpoint — 2026-10-17
Vừa hoàn thành: Toàn bộ YCXH loại 4 (Xuất trả nhà cung cấp) port ERP→HRM — Task 1-8 + helper hiển thị (Task 7). Final whole-branch review (opus) **APPROVED spec-compliance + APPROVED code-quality**, 0 Critical / 0 Important / 2 Minor. Adjudication: M1 (applyAllScope ẩn phiếu boss cross-company) → **BÁC** (ERP `searchData` cũng dùng `searchByFilter` áp cùng scope ở ProductImportRequest.php:1233-1333 → HRM mirror 1:1, bỏ sẽ lệch ERP); M2 (EP2 `dataForSupplierReturn` trim NCC lệch `supplierReturnSourceInfo`) → **FIX** gỡ trim ở `Modules/Finance/Http/Controllers/V1/ProductImportRequestController.php:112` → `'name' => $supplier->fullname` thô (khớp ERP + Assign ctrl), `php -l` sạch. Smoke test UI loại 4 PASS (bug render nghi trước đó = báo động giả, form.type=4 + isSupplierReturnType=true chuẩn). Đã dọn record test 39371 + detail (parent_id) trên erp_hrm_check.
Đang làm dở: (không) — tính năng loại 4 đóng.
Bước tiếp theo: CHỜ user duyệt commit/push (chưa commit). Sau loại 4: loại 17 (XUAT_BD_SC / SC-BD) — KHÔNG bắt đầu khi user chưa yêu cầu.
Blocked: (không)
