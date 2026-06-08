# Quản lý BOM — Plan

> **Checkpoint 2026-06-05: HOÀN THÀNH** (BE+FE, chạy main chưa commit). BE smoke-test pass (default toggle, isCanDelete=!is_default, syncItems, history). Permission 1105-1106. FE: list (xóa chỉ khi !default, không import) + modal xl (bảng NVL động + default + lịch sử). Còn: user test UI.

> Subagent-driven. KHÔNG commit.
> **Spec:** `docs/superpowers/specs/2026-06-05-product-bom-design.md`

## Phase 1 — BE

- [ ] 3 migration (boms, bom_items, bom_histories)
- [ ] 3 entity (Bom isCanDelete=!is_default, BomItem, BomHistory)
- [ ] Request (items array validate)
- [ ] Service (syncItems + default toggle + history snapshot, getAllByProduct)
- [ ] Transformers (items + histories)
- [ ] Controller + Routes + 2 permission + export

## Phase 2 — FE

- [ ] Menu "BOM"
- [ ] index.vue (xóa chỉ khi !default, filter sản phẩm)
- [ ] AddBomModal (sản phẩm + bảng NVL động + default + lịch sử)

## Phase 3 — Test

- [ ] 2 BOM/1 product, đổi default, xóa default bị chặn, history, syncItems

---

## Phase 4 — Tab BOM trong form Hàng hoá (CHỌN BOM có sẵn, KHÔNG tạo mới)

> **Checkpoint 2026-06-05: HOÀN THÀNH** (BE+FE, chạy main chưa commit).
> **ĐỔI HƯỚNG theo user**: ban đầu làm nested (tạo BOM ngay trong form, lưu 1 lần) → user yêu cầu "bom không được tạo mới từ hàng hoá mà chỉ chọn bom đã được tạo ra" → **REVERT nested**, tab BOM giờ là **danh sách BOM đã có của SP (chỉ đọc) + radio chọn 1 BOM mặc định** + link sang trang `/category/boms` để tạo BOM.
> Full HTTP-stack test PASS: product POST bỏ qua `boms[]` (không tạo nested); tạo BOM qua endpoint riêng; PUT product set `default_bom_id` OK; show trả `boms` list + default_bom_id đúng; getAllByProduct=2. FE compile sạch. Còn: user test UI.
> **Spec:** `docs/superpowers/specs/2026-06-05-product-bom-nested-design.md` (mục "ĐỔI HƯỚNG")

### BE

- [x] Product entity: thêm quan hệ `boms()` hasMany (giữ — dùng để show list)
- [x] ProductController::show load `boms.items`; DetailProductResource trả `boms` (đọc danh sách)
- [x] ProductRequest: ĐÃ GỠ rules nested `boms.*` (revert); giữ `default_bom_id` exists:boms
- [x] ProductService: ĐÃ GỠ `syncBoms()` + inject BomService (revert); `default_bom_id` set thẳng từ request

### FE

- [x] ProductForm: chia 2 tab (Thông tin chung / Định mức BOM), bỏ ô "BOM mặc định" cũ ở tab 1
- [x] Tab BOM: danh sách chỉ đọc `productBoms` (getAllByProduct) — radio chọn mặc định (set `default_bom_id`), cột mã/tên/số NVL/trạng thái; nút "Bỏ chọn mặc định"; link sang trang Định mức để tạo BOM
- [x] Create mode: hiện hướng dẫn "Lưu SP trước rồi tạo BOM"; classification!=2 hiện ghi chú
- [x] Payload: gửi `default_bom_id` (bỏ `boms[]`); load edit gọi getAllByProduct

### Test

- [x] Product POST bỏ qua boms rác (không tạo nested); BOM tạo qua endpoint riêng OK
- [x] PUT set default_bom_id → show đúng; getAllByProduct list đúng

---

## Phase 5 — Mỗi sản phẩm chỉ 1 BOM, bỏ "Đặt làm mặc định"

> **Checkpoint 2026-06-05: HOÀN THÀNH** (BE+FE, chạy main chưa commit).
> User chốt: "mỗi hàng hoá chỉ có 1 BOM duy nhất, bỏ checkbox Đặt làm mặc định."
> Full HTTP-stack test PASS: tạo BOM 1 → product.default_bom_id auto set; tạo BOM 2 cùng SP → 422; sửa chính BOM đó → 200; xoá BOM → default_bom_id về null. FE compile sạch (ProductForm, AddBomModal, boms/index).

### BE

- [x] BomRequest: bỏ rule `is_default`; thêm withValidator chặn 1 SP >1 BOM (loại trừ id chính nó)
- [x] BomService: bỏ set `is_default` + bỏ toggle default; tự đồng bộ `products.default_bom_id` = BOM khi create/update, gỡ về null khi delete; bỏ chặn xoá theo default
- [x] Bom::isCanDelete() → luôn true
- [x] ProductService: bỏ set `default_bom_id` ở cả updateOrCreate + update (BomService quản lý)

### FE

- [x] AddBomModal: bỏ checkbox "Đặt làm mặc định" + mọi ref `is_default`; thêm hint "Mỗi SP chỉ 1 BOM"
- [x] boms/index.vue: bỏ cột + badge "Mặc định"
- [x] ProductForm tab BOM: hiển thị 1 BOM duy nhất (chỉ đọc, link sang trang BOM), bỏ radio chọn mặc định + nút bỏ chọn; bỏ gửi `default_bom_id` trong payload

### Bổ sung — tab BOM hiển thị ĐẦY ĐỦ thông tin BOM gắn với SP

- [x] ProductController show: load `boms.items.material` + `boms.items.unit`
- [x] DetailProductResource: items thêm `material_code/material_name/unit_name`
- [x] ProductForm: dùng `data.boms` từ show (bỏ getAllByProduct riêng); tab hiển thị header BOM (mã/tên/trạng thái/ghi chú) + bảng NVL đầy đủ (NVL, ĐVT, định mức, hao hụt, tổng/1SP, ghi chú) — chỉ đọc
- [x] Test: show trả boms[0] kèm material_name/unit_name OK

### Bổ sung — bỏ cột Tổng/1SP + norm_quantity/waste_percent là số nguyên
- [x] Migration bom_items: `norm_quantity` + `waste_percent` đổi `decimal` → `integer`; đã ALTER bảng hiện có sang INT
- [x] BomRequest: validate `integer` cho norm_quantity (required) + waste_percent (nullable, max 100) + message tiếng Việt
- [x] AddBomModal: bỏ cột "Tổng/1SP" + method calcTotal; input norm/waste thêm step="1" min/max
- [x] ProductForm tab BOM: bỏ cột "Tổng/1SP" + method bomItemTotal
- [x] Test: decimal→422 "phải là số nguyên"; integer→200 lưu đúng INT

### Bổ sung — Modal xem lịch sử thay đổi BOM (giống màn assign/tasks)
- [x] BE: DetailBomResource histories thêm `snapshot` (decode) + sort theo id
- [x] FE: tạo `pages/category/boms/components/BomHistoryModal.vue` (timeline ho-timeline giống TaskHistoryModal) — diff snapshot liên tiếp: code/name/status/note + NVL (added/removed, resolve tên qua products/units getAll); bản đầu = "Tạo BOM", mới nhất lên đầu
- [x] FE: ProductForm tab BOM thêm nút "Xem lịch sử" (icon ri-history-line) mở modal với productBom
- [x] Test: BOM show trả histories kèm snapshot (2 bản, diff name/note/norm OK)
