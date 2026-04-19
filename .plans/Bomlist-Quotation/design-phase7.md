# Design: BOM List — Phase 7: Cập nhật theo yêu cầu khách hàng

## Ngày: 2026-04-08
## Người phụ trách: @dnsnamdang

---

## 1. Popup "Thêm hàng hoá" gộp

### Mục đích
Gộp BomBuilderPickModal + BomBuilderQuickCreateModal thành 1 popup duy nhất "Thêm hàng hoá" với 2 tab.

### Tab 1: Tìm hàng hoá có sẵn
- Thanh tìm kiếm theo mã/tên hàng
- Gộp 2 nguồn hiển thị chung 1 danh sách:
  - **Hàng từ ERP** (`erp2326.products` join `product_units` where `is_base=1`) — đánh tag "ERP"
  - **Hàng từ BOM hiện tại** (`bom_list_products` where `bom_list_id` = BOM đang edit) — đánh tag "BOM"
- Cột hiển thị: Mã | Tên | Model | Thương hiệu | Xuất xứ | ĐVT | Nguồn
- Multi-select checkbox + nhập số lượng cho mỗi dòng chọn

### Tab 2: Tạo mới hàng hoá
- Form tạo nhanh (giống BomBuilderQuickCreateModal hiện tại)
- Lưu trực tiếp vào `bom_list_products` với `erp_product_id = null`

### Logic chọn hàng ERP
- Khi chọn hàng từ ERP → tạo record `bom_list_products`:
  - Copy fields: `name, code, model_id, brand_id, origin_id, product_attributes`
  - `unit_id` = lấy từ `product_units` where `product_id` = product.id AND `is_base = 1`
  - `erp_product_id` = product.id (đánh dấu nguồn)
- **Đồng bộ khi lưu BOM**: tất cả record có `erp_product_id != null` → re-fetch từ ERP `products` và cập nhật lại `name, code, model_id, brand_id, origin_id, product_attributes, unit_id`

### Mapping fields: ERP products → bom_list_products
| ERP products | bom_list_products |
|---|---|
| id | erp_product_id |
| code | code |
| name | name |
| model_id | model_id |
| brand_id | brand_id |
| origin_id | origin_id |
| product_attributes | product_attributes |
| product_units.unit_id (is_base=1) | unit_id |

---

## 2. Cấp nhóm hàng (Grouping)

### Bảng mới: `bom_list_groups`
| Field | Type | Note |
|---|---|---|
| id | bigint unsigned PK | auto_increment |
| bom_list_id | int | FK → bom_lists.id |
| name | varchar(255) | Tên nhóm |
| sort_order | int | Thứ tự hiển thị |
| created_at | timestamp | |
| updated_at | timestamp | |

### Thêm field vào `bom_list_products`
- `bom_list_group_id` (int, nullable) — FK → bom_list_groups.id

### Cấu trúc hiển thị
```
I    → Group 1 (chỉ tên nhóm, không có giá/thông số)
  1  → Hàng cha (STT reset mỗi nhóm)
    1.1 → Hàng con
    1.2 → Hàng con
  2  → Hàng cha
II   → Group 2
  1  → Hàng cha
    1.1 → Hàng con
```

### Quy tắc
- STT nhóm: I, II, III, IV...
- STT hàng cha: reset về 1 cho mỗi nhóm
- STT hàng con: X.1, X.2... (giữ nguyên logic cũ)
- Khi BOM có group → **tất cả hàng hoá phải thuộc 1 group**
- Row nhóm: bold, background khác biệt, không hiển thị cột giá/thông số
- Button "Tạo nhóm" ở header cột STT
- Hỗ trợ drag-drop: đổi thứ tự group, kéo hàng giữa các group

---

## 3. Validate BOM tổng hợp

### Unique constraint khi lưu (store/update)
- 1 cặp (`solution_id`, `solution_module_id`) chỉ tồn tại **1 BOM tổng hợp** (type=2)
- Nếu `solution_module_id = null` → check unique theo `solution_id` alone
- Khi update: exclude BOM đang edit ra khỏi check
- Lỗi trả về: "Giải pháp [X] / Hạng mục [Y] đã có BOM tổng hợp: [tên BOM existing]"

### Popup chọn BOM thành phần (SubBomModal)
- Chỉ hiển thị BOM thành phần (type=1) thuộc cùng `solution_id` + `solution_module_id`
- Loại trừ BOM có status=1 (Nháp/Đang tạo)

---

## 4. Thay đổi Database

### Migration 1: Tạo bảng `bom_list_groups`
```sql
CREATE TABLE bom_list_groups (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    bom_list_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    sort_order INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP NULL,
    updated_at TIMESTAMP NULL
);
```

### Migration 2: Thêm fields vào `bom_list_products`
```sql
ALTER TABLE bom_list_products 
    ADD COLUMN erp_product_id BIGINT UNSIGNED NULL AFTER product_project_id,
    ADD COLUMN bom_list_group_id INT NULL AFTER parent_id;
```

---

## 5. Backend mới / cập nhật

### Models mới (mysql2 connection)
- `TpProduct` → bảng `products` (erp2326)
- `TpProductUnit` → bảng `product_units` (erp2326)

### Entity mới (HRM DB)
- `BomListGroup` — relationships: belongsTo BomList, hasMany BomListProduct

### Cập nhật Entity
- `BomListProduct` — thêm: `erp_product_id`, `bom_list_group_id`, relationship `erpProduct()`, `group()`
- `BomList` — thêm relationship `groups()`

### API endpoint mới
- `GET /assign/bom-lists/erp-products?keyword=` — search products từ ERP, join product_units (is_base=1), trả về danh sách gộp

### Cập nhật Service
- `syncProducts()` — đồng bộ ERP fields khi lưu (re-fetch products by erp_product_id)
- `store()` / `update()` — validate unique BOM tổng hợp trước khi lưu
- Thêm `syncGroups()` — tạo/cập nhật groups
- Cập nhật `loadDetail()` — eager load groups

### Cập nhật SubBom filter
- Filter BOM thành phần theo `solution_id` + `solution_module_id`, exclude status=1

---

## 6. Frontend cập nhật

### Component mới
- `BomBuilderAddProductModal.vue` — popup gộp 2 tab (thay thế PickModal + QuickCreateModal)

### Component cập nhật
- `BomBuilderTableCard.vue` — thêm row nhóm (I, II, III), button "Tạo nhóm", STT reset mỗi nhóm
- `BomBuilderEditor.vue` — quản lý data groups, gọi API ERP products, logic đồng bộ
- `BomBuilderSubBomModal.vue` — filter theo solution/module, exclude nháp
- `BomBuilderInfoCard.vue` — hiển thị lỗi validate unique BOM tổng hợp

### Xoá component
- `BomBuilderPickModal.vue` — thay thế bởi AddProductModal
- `BomBuilderQuickCreateModal.vue` — gộp vào AddProductModal
