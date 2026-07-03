# ERP Cost Catalog — Spec Frontend (Phase 2)

> Mọi đường dẫn tương đối với `hrm-client/`. **Đọc skill `modal-popup` + `button-convention` trước khi code.**

## 1. Component dùng chung — `pages/assign/components/cost/`

### `CostPickerModal.vue`
- **Props:** `visible` (Boolean), `kindFilter` (Number|null — mặc định null = cả 2 loại).
- **UI:**
  - Ô tìm kiếm (debounce 300ms) → gọi `apiGetMethod('assign/erp-costs?keyword=&kind_of=')`.
  - Filter loại: nút/segment "Tất cả · Dịch vụ · Chi phí khác".
  - List kết quả: tên + **badge kind_of** (DV xanh / Chi phí cam) + VAT%.
  - Nút **"+ Tạo nhanh"** → mở `CostQuickCreateModal`.
- **Emit:** `select(cost)` (cost = object từ API: id, name, kind_of, vat_percent...), `hidden`.

### `CostQuickCreateModal.vue` (mirror popup ERP)
- **UI động theo Loại (`kind_of`):**
  - Radio Loại: Dịch vụ (2) / Chi phí khác (1).
  - **kind_of=2 (Dịch vụ):** Tên\* · Tỷ lệ giá vốn\* · % VAT\* · ☑ Tính doanh thu. *(Bỏ Chiết khấu — không ghi company_costs.)*
  - **kind_of=1 (Chi phí):** Tên\* · Tên tiếng Anh · Loại chi phí\* (select 1–8).
- **Validate inline:** `is-invalid` + `invalid-feedback`, flag `touched` (chỉ hiện lỗi sau submit đầu). Map lỗi BE trả về (vd `name` đã tồn tại).
- **Submit:** `apiPostMethod('assign/erp-costs', payload)` → emit `created(cost)` → picker tự chọn cost mới.
- **Emit:** `created(cost)`, `hidden`.

## 2. Store
- Dùng `apiGetMethod` / `apiPostMethod` có sẵn — KHÔNG thêm action mới.

## 3. Quotation — `pages/assign/quotations/_id/edit.vue`
- Modal "Thêm dịch vụ bổ sung" (~dòng 767):
  - Thay input **Tên** free-text → ô readonly + nút "Chọn từ danh mục" mở `CostPickerModal`.
  - Khi `select(cost)`: set `newServiceItem.name = cost.name`, `cost_id = cost.id`, `vat_percent = cost.vat_percent` (cho sửa).
  - **Bỏ field ĐVT** (`unit_id`) trong modal + cột ĐVT trong bảng dịch vụ.
  - **SL (`qty`) mặc định = 1, KHÓA không cho sửa** (input readonly/disabled, không hiện nút tăng giảm). Bỏ rule nhập SL.
- `serviceItemErrors` (computed ~1039): bỏ rule `unit_id` + rule `qty`; thêm yêu cầu đã chọn từ danh mục (có `cost_id`) — *hoặc* vẫn cho nhập tay nếu cần (xác nhận: mặc định bắt chọn từ danh mục).
- Payload `service_items.map` (~dòng 1967): thêm `cost_id: s.cost_id || null`, `qty: 1` (cố định), bỏ `unit_id`.
- `resolveServiceItems` trả `cost_id` → khi load lại hiển thị đúng (badge loại nếu có `kind_of`).

## 4. BOM — `pages/assign/bom-list/components/BomBuilderAddProductModal.vue`
- Nhánh `isService` (~dòng 157):
  - Thay input **Tên dịch vụ** + **ĐVT** → ô chọn từ danh mục (`CostPickerModal`).
  - Khi `select(cost)`: `newProduct.name = cost.name`, `newProduct.cost_id = cost.id`; **SL (`qty_needed`) = 1, KHÓA không cho sửa**; giữ rule strip model/brand/origin + no children (đã có).
- Goods (`product_type=1`): **giữ nguyên** luồng chọn ERP product hiện tại.
- Payload thêm `cost_id` cho dòng service; resource BOM trả `cost_id`.

## 4b. Hợp nhất popup (Phase F4)

Gộp 2 popup (Thêm hàng hoá + Chọn dịch vụ) → **1 popup BOM** "Thêm hàng hoá / dịch vụ" với 2 tab:
- **Tab Hàng hoá**: list ERP (search + multi-select) + nút "Thêm hàng tạm" → popup `BomProductCreateModal` (form hàng hoá thủ công).
- **Tab Dịch vụ & Chi phí**: panel `CostCatalogPanel` (search costs + lọc loại + "Thêm mới" → `CostQuickCreateModal`). Chọn mục → emit apply (product_type=2, cost_id, qty=1).

**Component tách dùng chung:**
- `CostCatalogPanel.vue` (inline): search + list + badge + nút "Thêm mới" (mở `CostQuickCreateModal`); emit `select(cost)`. Là ruột chung.
- `CostPickerModal.vue`: rút gọn → b-modal mỏng bọc `CostCatalogPanel` (Quotation dùng).
- `BomProductCreateModal.vue`: form tạo hàng hoá thủ công (tách từ tab "Tạo mới", bỏ radio dịch vụ).
- `BomBuilderAddProductModal.vue`: 2 tab như trên; bỏ radio + bỏ `CostPickerModal` lồng.

→ Quotation add-service: không đổi hành vi (CostPickerModal vẫn hoạt động, chỉ thay ruột bằng panel).

## 4c. Phase F6 — Đồng nhất sửa hàng/dịch vụ ở Báo giá (approach B)

Bảng chi tiết chỉ hiển thị + sửa inline SL/giá; danh tính sửa qua popup (giống BOM `open-edit`).

**Component mới:** `pages/assign/quotations/components/QuotationProductEditModal.vue`
- Props: `show`, `product` (object dòng), `unitOptions`.
- Sửa **hàng tạm (non-ERP)**: Tên, Mã, ĐVT (`V2BaseSelect`), Model/Hãng/Xuất xứ (`V2BaseSelectRemote` tự fetch `assign/product-projects/get-model|get-brand|get-origin`), Đặc điểm (spec).
- KHÔNG sửa SL/giá (inline trong bảng).
- Emit `save(fields)` + `close`. Validate inline (is-invalid + touched).

**Tái dùng:** `CostPickerModal.vue` (đang orphan) cho **sửa dịch vụ/chi phí** → chọn lại mục danh mục → thay `cost_id` + `name` + `vat_percent`.

**edit.vue:**
- Dòng hàng tạm (`isDirectQuotation && canEdit && !isErpProduct && product_type!=2`): nút **Sửa** cạnh "Thêm con" → `openProductEdit(product)`. Save → `Object.assign(product, fields)`.
- Dòng dịch vụ (canEdit): nút **Sửa** cạnh nút xoá → mở `CostPickerModal` → `onServiceReselect(svc, cost)` → cập nhật svc.
- ERP product: không nút Sửa.

**Data flow:** popup → emit field → cha merge vào dòng → lưu trong payload `products`/`service_items` như hiện tại.

## 5. Edge / backward-compat
- Dòng dịch vụ cũ (`cost_id=null`, có tên free-text + có thể có unit_id): vẫn render & lưu bình thường; không ép chọn lại danh mục khi edit.
- Khi tạo nhanh trùng tên (cùng type) → BE trả lỗi → hiện inline tại field Tên trong `CostQuickCreateModal`.
