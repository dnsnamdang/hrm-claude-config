# ERP Cost Catalog — Phase 3: Tách Dịch vụ & Chi phí khác thành nhóm/bảng riêng trên BOM

## Mục tiêu
Đồng nhất việc xây dựng dịch vụ/chi phí giữa **BOM** và **Báo giá tự tạo**: cả hai đều có nhóm "Dịch vụ & Chi phí khác" lưu **bảng riêng**, gắn danh mục `costs` ERP (kind_of=2). Bỏ mô hình trộn `product_type=2` vào `bom_list_products`.

## Quyết định (chốt qua brainstorming)
- BOM có bảng riêng `bom_list_service_items` (mirror `quotation_service_items`, **cost-only** — chỉ giá vốn).
- **Không migrate** dữ liệu cũ — chỉ áp dụng từ giờ. BOM cũ có dòng `product_type=2` vẫn render trong products (không mất dữ liệu); dịch vụ mới đi vào bảng mới. *(Nếu sau muốn ẩn/migrate → bổ sung.)*
- Giá: BOM service chỉ `estimated_price` (giá vốn) + `vat_percent` (từ cost). Giá bán nhập ở báo giá.

## Backend (hrm-api)

### B1. Migration `bom_list_service_items`
Cột: `id, bom_list_id (FK, index), cost_id (nullable, FK costs ERP), name, code (nullable), qty default 1, estimated_price decimal(15,2) default 0, vat_percent decimal(5,2) default 0, note text nullable, sort_order int default 0, created_by, updated_by, timestamps`.

### B2. Entity `Modules/Assign/Entities/BomListServiceItem.php`
- `$guarded=[]`, `$table='bom_list_service_items'`.
- `BomList::serviceItems()` hasMany.

### B3. Request `BomListStoreRequest`
Thêm:
```
'service_items' => 'sometimes|array',
'service_items.*.id' => 'nullable|integer',
'service_items.*.cost_id' => 'nullable|integer',
'service_items.*.name' => 'required|string|max:255',
'service_items.*.estimated_price' => 'nullable|numeric|min:0',
'service_items.*.vat_percent' => 'nullable|numeric|min:0|max:100',
'service_items.*.note' => 'nullable|string',
'service_items.*.sort_order' => 'nullable|integer|min:0',
```

### B4. `BomListService` (store + update)
- Sau khi sync products: **sync serviceItems** vào `bom_list_service_items` (delete items không còn trong payload → upsert: có id→update, không→create với qty=1, code tự sinh nếu cần).
- KHÔNG tạo `product_type=2` trong `bom_list_products` nữa (luồng mới).

### B5. Resource `DetailBomListResource`
Thêm khối `service_items` (id, cost_id, name, code, qty, estimated_price, vat_percent, note, sort_order).

### B6. Downstream `QuotationService::createFromBom` (BOM→báo giá)
Sau khi copy products → copy `bomList->serviceItems` sang `quotation_service_items`: map `cost_id`, `name`, `qty=1`, `estimated_price` (giá vốn từ BOM), `vat_percent`; `quoted_price` để 0 (nhập ở báo giá). Giữ cơ chế hiện có cho hàng hoá.

## Frontend (hrm-client)

### F1. `BomBuilderEditor`
- Data thêm `serviceItems: []` — load từ `detail.service_items` (mapServiceItemRow).
- `handleAddProductApply`: item `product_type===2`/`cost_id` → push vào `serviceItems` (không vào groups). Hàng hoá giữ nguyên.
- `buildSavePayload`: thêm `service_items: this.serviceItems.map(...)` (cost_id, name, qty=1, estimated_price, vat_percent, note). Orphan-safety-net hàng hoá KHÔNG đụng serviceItems.
- Xoá/sửa service item (reuse pattern).

### F2. `BomBuilderTableCard`
- Render **section "Dịch vụ & Chi phí khác"** riêng (cuối bảng, nền xanh nhẹ `#e2f5ee`/`#eef9f4`), nút "Thêm mới" riêng (emit `open-service` hoặc `open-pick` chế độ service). Cột: STT, tên, SL(=1), giá vốn, VAT, thành tiền + sửa/xoá.
- Bỏ render dòng product_type=2 trong nhóm hàng hoá (dịch vụ mới ở section riêng). Dữ liệu cũ product_type=2 (nếu có) vẫn render trong nhóm (không mất).

### F3. `BomBuilderAddProductModal`
- `onServiceSelected`: emit service item (cost_id, name, estimated_price=giá vốn từ cost, vat_percent) → editor push vào serviceItems; **không cần chọn nhóm hàng hoá**.
- Tái dùng `CostCatalogPanel` (đã chung) → UX thêm dịch vụ giống Báo giá.

## Verify
1. Migration chạy; `Schema::hasTable('bom_list_service_items')`.
2. BOM: thêm dịch vụ → vào section riêng → lưu/reload → đúng (bảng mới).
3. Hàng hoá BOM vẫn theo nhóm như cũ.
4. BOM→báo giá: dịch vụ BOM chảy sang dịch vụ báo giá (cost_id + giá vốn), giá bán nhập ở báo giá.
5. Backward-compat: BOM cũ mở vẫn OK.
