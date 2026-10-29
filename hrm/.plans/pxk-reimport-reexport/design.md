# Thiết kế: Nhập lại / Xuất lại Phiếu xuất kho (PXK) — port ERP → HRM

**Ngày:** 2026-10-21
**Phân hệ:** module `Assign` (luồng xuất kho). PXK = `WarehouseExport` / bảng `warehouse_exports`.
**Nguồn nghiệp vụ:** ERP TanPhatDev (Laravel 6) — READ-ONLY, bám 1:1.
**Chỉ thị nền (bắt buộc):** "cứ làm giống erp, rủi ro/lỗi cũng không sao, giống erp là được" + "dữ liệu phải được lưu đúng y như ERP làm".

---

## 1. Mục tiêu

Port đầy đủ 2 chức năng cuối của vòng đời PXK từ ERP sang HRM:

- **Nhập lại** (re-import): một *phiếu* độc lập (`WarehouseReImport`, mã `PNL-`) có màn danh sách + tạo + chi tiết. Tạo từ một PXK **bị từ chối** (status 4), hoàn tồn NGAY (cộng lại tồn đã xuất).
- **Xuất lại** (re-export): *hành động* trên PXK, đẻ ra một **PXK con** (`parent_warehouse_export_id`), trừ tồn lại khi gửi.

Bất đối xứng này là ĐÚNG ERP: xuất kho → hàng đi RA; "nhập lại" kéo hàng VÀO lại (phiếu độc lập), "xuất lại" đẩy RA lần nữa (PXK con).

## 2. Vòng trạng thái PXK (ERP-verified)

Hằng `WarehouseExport` (HRM đã khai sẵn, trùng ERP): `1 Đã hạch toán`, `2 Chờ duyệt`, `3 Đang tạo`, `4 Không duyệt`, **`5 Đã nhập lại`**, **`6 Đã xuất lại`**, `7 Đang hạch toán`, `8 Đã hủy`.

```
PXK bị từ chối  → status 4 (Không duyệt)
  → tạo Nhập lại → PXK = 5; phiếu Nhập lại sinh ở status 2; HOÀN TỒN ngay
  → tạo Xuất lại → PXK = 6; phiếu Nhập lại → 1; TRỪ TỒN lại (khi gửi/status 2)
```

**Gate (port y ERP):**
- `WarehouseExport::canReImport()` = (`created_by == Auth::id()` **hoặc** `Super Admin`) **&&** `status == 4`.
- `WarehouseExport::canReExport()` = (… **hoặc** `Super Admin`) **&&** `status == 5`.
- `WarehouseReImport::canReExport()` = `created_by == Auth::id()` **&&** `status == 2` (nút Xuất lại cũng hiện trên chi tiết phiếu Nhập lại — ERP có cả 2 lối vào).
- Xuất lại **bắt buộc đã có** phiếu Nhập lại trước (tuần tự 4→5→6).

## 3. Backend

### 3.1 Entity (port mới, map bảng `warehouse_reimports*` ĐÃ CÓ sẵn trong `erp_hrm_check` — KHÔNG migration)

`Modules/Assign/Entities/Warehouse/`:
- `WarehouseReImport` — table `warehouse_reimports`, `$guarded=[]`; hằng status `1 Đã xuất lại`, `2 Chờ xuất lại` (bám ERP). Quan hệ: `warehouseExport()` (PXK gốc), `products()`→`WarehouseReImportLot`, `tabs()`→`WarehouseReImportTab`, `creator()`. Method: `generateCode()` (prefix `PNL-`), `canView()`, `canReExport()`, `updateWarehouse()`.
- `WarehouseReImportLot` (table `warehouse_reimport_lots`, `parent_id`, `details()`), `WarehouseReImportLotDetail`, `WarehouseReImportTab` (`syncTabProducts()`), `WarehouseReImportTabProduct`.
- Thêm `canReImport()` + `canReExport()` vào `WarehouseExport`.

### 3.2 Nhập lại — Controller + Service

`WarehouseReImportController` (module Assign) + `WarehouseReImportService`:
- `index` — danh sách, **phân quyền theo cấp** (xem §5), dùng lại mẫu `WarehouseExportController::scopedQuery`.
- `show` — chi tiết (gate `canView`).
- `createData($pxkId)` — trả dữ liệu PXK để dựng form (gate `canReImport`).
- `store` — port ERP `WarehouseReImportsController::store` **1:1**:
  1. Validate `warehouse_export_id` required|exists, `note` nullable|max:255.
  2. `$parent = WarehouseExport::findOrFail`; nếu `!canReImport()` → trả lỗi "Không đủ quyền".
  3. Tạo `WarehouseReImport`: `code=randomString(20)`, `type=parent.type`, `warehouse_export_id`, `note`, `status=2`; save; `generateCode()` (PNL-); save.
  4. Copy toàn bộ lô từ `parent->products` sang `WarehouseReImportLot` với **`import_qty = lot->export_qty`**, `warehouse_export_lot_id = lot->id`; copy details sang `WarehouseReImportLotDetail` (`warehouse_export_lot_detail_id = d->id`, giữ `position_id`, `import_lot_id`, `position_code`).
  5. Copy tabs (`WarehouseReImportTab` + `syncTabProducts`).
  6. `updateWarehouse()` → HOÀN TỒN (§3.4).
  7. `parent->status = 5`; save. Tất cả trong 1 transaction.
- **KHÔNG có** `update` / `destroy` (ERP không có) → phiếu Nhập lại không có `is_can_edit` / `is_can_delete`.
- In `PHIEU_NHAP_LAI` + xuất Excel: **HOÃN** (gom với mảng "In biên bản" phase sau).

### 3.3 Xuất lại — bổ sung vào `WarehouseExportController` + `WarehouseExportService`

Port ERP `WarehouseExportsController::reExport` (form) + `reExportStore`:
- `reExportData($pxkId)` — gate `canReExport` (PXK status 5), trả dữ liệu PXK gốc + options (nhân viên, bốc xếp, NCC) để prefill form.
- `reExport($pxkId)` — port `reExportStore` **1:1**:
  1. Gate `canReExport`.
  2. Validate: `status in 2,3`; `receiver_id` required|exists; `lots` required|array|min:1 (+ product/unit/detail_type/details.qty/position_id/import_lot_id); `attachments` **required**|file|mimes:pdf khi `status==2` (ngược lại nullable); `total_packages` nullable; nhánh `arrange_delivery` (bốc xếp/thuê xe) + `executors` theo `rent_type` (1=thuê NV, 2=NCC) — **khớp đúng rule ERP**.
  3. `validateLots`, `checkInventory` (đang kiểm kho), `checkPositionInventory`.
  4. Tạo **PXK con** `WarehouseExport`: copy gần hết field PXK cha (contract linkage `contract_id/wr_service_contract_id/service_contract_id/project_contract_id/firm_contract_id/firm_contract_tab_id`, customer_*, delivery_place, warehouse_id, transition_*…), set **`parent_warehouse_export_id = parent->id`**, `warehouse_export_request_id = parent->warehouse_export_request_id`, department/phone/email người lập, `receiver_id`, `status`.
  5. Copy trips (`ActivityHasDeliveryTrip`), tạo lô (`export_qty = qty*unit_coefficient`, `syncPackages`, chặn "xuất quá tồn" theo `StockPositionDetail`, `XUAT_GHEP` qty phải khớp), validate tabs qty khớp (`syncTabs`).
  6. `WarehouseReImport::where('warehouse_export_id', parent->id)->firstOrFail()->status = 1`.
  7. `parent->status = 6`.
  8. Nếu `status==2` → `updateWarehouse()` (TRỪ tồn — luồng xuất chuẩn) + `send()`. Nếu `status==3` → chỉ lưu nháp.

> **Ruling (SDD):** Xuất lại = TẠO LẠI một PXK. Nên **tái dùng tối đa luồng tạo PXK hiện có của HRM** (`WarehouseExportService` + `exportStock` + `PhysicalStockWriter`), chỉ bổ sung: prefill từ cha, copy field cha + `parent_warehouse_export_id`, và lật trạng thái (reimport→1, parent→6). Các nhánh phụ của ERP (delivery trips, arrange_delivery/executors bốc xếp) được port **đúng tới mức luồng tạo PXK gốc của HRM hiện đã hỗ trợ**; phần nào PXK gốc HRM chưa có thì để sau cùng với phần đó — phải **xác minh năng lực luồng tạo PXK HRM ở bước lập plan** (xem §7).

### 3.4 Hoàn tồn — `WarehouseReImport::updateWarehouse()` (CRUX "lưu đúng y ERP")

Cộng ngược tồn vật lý, **đúng từng bước ERP** (`WarehouseReImport::updateWarehouse` :184-284), tái dùng `Modules/Finance/Services/PhysicalStockWriter::importLot()`:

Với mỗi lô (khóa theo `warehouse_export->warehouse_id` + `product_id`):
- `StockLog`: `change = +import_qty`, `objectable_id = lot->id`, `objectable_type = get_class(WarehouseReImportLot)` (FQN ERP lưu polymorphic); `stocks.total_qty += import_qty`.
- `StockOfCompany` (stock_id + company_id): tạo nếu chưa có, `qty += import_qty`.
- Mỗi detail: `StockPosition` (stock_id+product_id+position_id) `qty += qty*unit_coefficient` + `StockPositionLog`; `StockPositionDetail` (stock_position_id+product_id+position_id+import_lot_id) `qty += qty*unit_coefficient`; `StockPositionOfCompany` tạo-nếu-thiếu `qty +=`; `StockPositionDetailLog` **type `NHAP_THUONG`**, nối chuỗi `qty_before/qty_after` từ log NHAP_THUONG gần nhất, `timestamps=false` + `created_at=now`.
- **KHÔNG** đụng `order_stock`, `prepick`, `accounting_stocks`.

**Bất biến dữ liệu (bắt buộc):** lượng + **pool `company_id`** cộng lại khi Nhập lại phải ĐÚNG pool mà lúc lập PXK đã trừ, để `StockOfCompany` / `StockPositionOfCompany` **net về 0**. ERP lấy `company_id` tự động theo auth; HRM phải truyền `company_id` giải theo **đúng cách `WarehouseExportService::exportStock` của PXK cha đã giải** (xác minh ở plan — đây là bẫy gộp-DB đã gặp ở PXG/hold).

### 3.5 Routes (`Modules/Assign/Routes/api.php`)

- Nhóm `/assign/warehouse-exports`: thêm `GET {id}/re-export-data`, `POST {id}/re-export`.
- Nhóm mới `/assign/warehouse-reimports`: `GET index`, `GET {id}` (show), `GET re-import-data/{pxkId}` (createData), `POST store`.

## 4. Frontend (Nuxt2/Vue2, mượn khung Finance; đặt dưới `pages/finance/warehouse-exports/` + `.../warehouse-reimports/`)

- **Nhập lại — danh sách** `warehouse-reimports/index.vue`: đủ 4 mixin (`PageTitleMixin`, `CheckPermission`, `filterStateMixin`, `columnCustomizationMixin`), `V2BaseSmartFilterPanel` (floating) + `V2BaseDataTable`; cột STT / Mã (nuxt-link, `PNL-`) / Tên / PXK gốc / Người tạo / Ngày tạo / Trạng thái (`V2BaseBadge`) / Hành động; sort mặc định ngày tạo giảm dần; `localStorageKey`/`columnScreenKey` duy nhất. Không có nút Sửa/Xóa.
- **Nhập lại — tạo + chi tiết**: copy khung `pages/finance/warehouse-imports/_id/re-export.vue` (form chuẩn: `V2BaseFormCard` thông tin chung disabled + bảng hàng hóa + ghi chú + `export-actionbar` + `BaseConfirmModal`) và `warehouse-reexports/_id/index.vue` (màn xem).
- **Xuất lại — form trên PXK** `warehouse-exports/_id/re-export.vue`: prefill từ `re-export-data`, nút "Xuất lại" (`BaseConfirmModal`) + "Quay lại"; upload PDF; gọi `$store.dispatch('apiGetMethod'/'apiPostMethod', …)` (PXK không có store riêng).
- **Nút bấm**: danh sách PXK (`warehouse-exports/index.vue` → `getRowActions`) thêm action `re_import` (visible `item.is_can_re_import`) và `re_export` (visible `item.is_can_re_export`), mẫu `warehouse-imports/components/row-actions.js`. Chi tiết PXK (`_id/index.vue` → `.export-actionbar__btns`) thêm nút tương ứng gated `detail.is_can_re_import/re_export` (khớp danh sách). Chi tiết phiếu Nhập lại có nút "Xuất lại" gated `detail.is_can_re_export`.
- **Menu**: KHÔNG thêm mục menu riêng cho Nhập/Xuất lại (là row-action). Màn danh sách Nhập lại: thêm mục menu ở phân hệ luồng xuất kho (sẽ chốt vị trí ở plan theo sheet quy hoạch).
- Thông báo lấy nguyên văn bộ QLDA; nhãn "Người tạo"/"Ngày tạo" (không "Người lập"/"Ngày lập").

## 5. Phân quyền

- **4 quyền mới** `guard = api` cho màn danh sách Nhập lại: `Xem phiếu nhập lại theo tổng công ty / công ty / phòng ban / bộ phận` — khai trong `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (KHÔNG migration), group "Phiếu nhập lại", `type = 8` (cùng phân hệ luồng xuất kho). Dùng `PermissionHelper::checkPermissionListWithColumn(..., 'warehouse_reimports', 'created_by')` trong `index`. Admin tự gán lại.
- **Hành động** tạo Nhập lại / Xuất lại: **không cần quyền mới** — gate theo `created_by == mình || Super Admin` (đúng ERP). BE trả cờ `is_can_re_import` / `is_can_re_export` cho FE.
- `meta.is_all_company` do BE quyết (chỉ người xem được mọi công ty mới thấy ô lọc Công ty).

## 6. Review Focus (edge/correctness dễ cắn người dùng — phải có test)

1. **Net-về-0 tồn theo company**: lập PXK (trừ tồn) → từ chối → Nhập lại (cộng tồn) ⇒ `stocks.total_qty`, `StockOfCompany.qty`, `StockPosition*`, `StockPositionDetail.qty` trở về **đúng bằng** trước khi lập PXK (đặc biệt `company_id` pool). Test khẳng định bất biến này.
2. **Gate tuần tự**: không cho Nhập lại khi PXK.status ≠ 4; không cho Xuất lại khi PXK.status ≠ 5 (chưa có phiếu Nhập lại) → trả lỗi, không ghi gì.
3. **`import_qty = export_qty`**: Nhập lại cộng đúng lượng ĐÃ xuất (không phải qty đặt), theo từng lô/vị trí/`import_lot_id`.
4. **Xuất lại "không xuất quá tồn"**: sau khi đã hoàn tồn, chặn `qty*export_unit_coefficient > StockPositionDetail.qty` (ERP :1812) → rollback toàn bộ.
5. **Phân quyền cấp + ẩn nháp người khác** ở danh sách Nhập lại: người xem theo phòng/bộ phận chỉ thấy phiếu trong phạm vi; Super Admin/tổng công ty không bị bó `company_id`.

## 7. Phải xác minh ở bước lập plan (trước khi code)

- Năng lực luồng tạo PXK hiện tại của HRM (`WarehouseExportService`): đã port trips (`ActivityHasDeliveryTrip`), `arrange_delivery`/`executors` (bốc xếp), `syncPackages`, `syncTabs` chưa? Phần nào thiếu → quyết port kèm hay để sau (ghi Ruling vào ledger).
- Cách `exportStock` của HRM giải `company_id`/`warehouse_id` cho ctx `PhysicalStockWriter` → bảo đảm Nhập lại dùng cùng cách (net-về-0).
- `PhysicalStockWriter::importLot` có ghi đủ `StockPositionDetailLog` loại `NHAP_THUONG` + tạo `StockPositionOfCompany` thiếu giống ERP không; nếu lệch → port đúng bản ERP cho nhánh nhập lại.
- Bảng `warehouse_reimports*` + cột `parent_warehouse_export_id` xác nhận có trong `erp_hrm_check` (đã verify trước đó) — kiểm cột đầy đủ khi viết entity.

## 8. Ngoài phạm vi (phase sau)

- In `PHIEU_NHAP_LAI` + xuất Excel danh sách Nhập lại.
- In 5 biên bản (gate `canDeliveryReport`).
- Đóng gói (packaging) nâng cao, điều chuyển 5/6/7, ghép/tách.

---
**Quy trình:** SDD từng task (implement → test → review độc lập → commit LOCAL). KHÔNG push tới khi user yêu cầu. KHÔNG `git add -A`. KHÔNG sửa ERP. KHÔNG đụng WIP `ProductExportController.php` của đồng đội.
