# Phase 1 — Chuyển 11 danh mục liên quan hàng hoá sang HRM

> Thuộc feature lớn `.plans/gop-db/quan-ly-hang-hoa/` · Nhánh `gop_db` (cả 2 repo) · @namdangit
> Bắt đầu 20/09/2026 · **CODE XONG 20/09/2026** (11/11 màn) — nhánh `feat/p1-danh-muc-hang-hoa`
> **Spec đầy đủ**: `docs/superpowers/specs/gop-db/2026-09-20-chuyen-danh-muc-lien-quan-design.md`
> **Khảo sát nghiệp vụ ERP**: `khao-sat.md` (cùng thư mục)

## Mục tiêu

Dựng 11 màn danh mục bên HRM trên **đúng 11 bảng ERP đang chạy** — các danh mục mà màn Hàng hoá
(Phase 2) sẽ phụ thuộc vào. **Không migration bảng mới**; DB đã gộp nên HRM và ERP dùng chung y hệt
một bảng. Chỉ 1 migration thêm 22 quyền.

| Màn | Bảng | Dòng | Slug HRM |
|---|---|---|---|
| Danh mục model | `product_models` | 39.796 | `/master-data/product-models` |
| Danh mục code đặt hàng | `barcodes` | 8.664 | `/master-data/order-codes` |
| Danh mục đơn vị tính | `units` | 145 | `/master-data/units` |
| Danh mục thuộc tính | `attributes` | 446 | `/master-data/attributes` |
| Danh mục đơn vị thuộc tính | `unitteches` | 103 | `/master-data/attribute-units` |
| Danh mục thương hiệu | `brands` | 1.250 | `/master-data/brands` |
| Danh mục hãng sản xuất | `manufactures` | 1.071 | `/master-data/manufacturers` |
| Danh mục xuất xứ | `origins` | 113 | `/master-data/origins` |
| Danh mục file đính kèm | `attachment_types` | 8 | `/master-data/attachment-types` |
| Danh mục mã màu | `code_colors` | **0** | `/master-data/color-codes` |
| Danh mục thuế suất | `tax_rates` | 40 | `/master-data/tax-rates` |

## 8 quyết định user chốt 20/09/2026

1. **Trạng thái giữ nguyên 0/1 trong DB**, HRM quy đổi ở tầng model/resource — ERP không bị đụng.
2. **2 quyền/màn** (Xem + Quản lý) = 22 quyền, guard `api`, id **1590-1611**, group
   `'Danh mục hàng hóa'`. Không đụng 11 bộ quyền guard `web` của ERP.
3. **Hãng sản xuất chỉ CRUD** — 3 màn con KPI/cấu hình ở lại ERP.
4. **Giữ nguyên màn ERP cũ** — Phase 1 không đụng repo ERP dòng nào.
5. **Có Lịch sử thay đổi, đủ 2 nơi** (popup ở danh sách + khối ở popup Xem).
6. **Cả 11 màn đều có Import + Xuất Excel**; bỏ CSV/PDF của ERP.
7. **Cách A — mở rộng nền Phase 0** thay vì dựng nền thứ hai: sửa **11 chỗ trong 5 file**
   `BaseCatalog*` (bản đếm đầu ghi 5 chỗ/4 file là SAI — xem §4 của spec). Đổi lại phải chứng minh 6 màn Phase 0 không vỡ.
8. **Hãng sản xuất KHÔNG ghi đè `company_id` sang `products`** — lệch có chủ ý so với ERP.

## 3 chỗ lệch CÓ CHỦ Ý so với ERP

1. **Hãng sản xuất không lan truyền `company_id`.** ERP mỗi lần Lưu hãng ghi lại `company_id` cho
   mọi hàng hoá của hãng (hãng `#394` = **4.514 dòng**), và **367 hàng hoá** đang lệch sẵn → port
   nguyên là âm thầm đổi công ty của 367 dòng. HRM chỉ ghi bảng `manufactures`; chuyện
   `products.company_id` để Phase 3 quyết.
2. **Màn Thuộc tính bỏ trường "Nhóm hàng hoá"** (pivot `attribute_groups`, 2.434 dòng, trỏ bảng
   `groups` nằm trong nhóm BỎ). Vai trò đó đã được Phase 0 thay bằng `product_type_attributes`,
   khai từ phía Loại sản phẩm. Cột này trên danh sách ERP cũng đã bị comment sẵn.
3. **Thuế suất**: `created_by`/`updated_by` là **varchar** → ép kiểu khi join, không khai
   `belongsTo`. Không migration đổi kiểu vì ERP đang ghi.

## Thứ tự làm — 3 đợt

| Đợt | Nội dung |
|---|---|
| **1** | Sửa 5 chỗ nền + 3 màn đơn giản nhất: **Xuất xứ · Đơn vị thuộc tính · Model** |
| **2** | **Đơn vị tính · Thuộc tính · Thương hiệu · Hãng sản xuất → rồi Code đặt hàng** (`barcodes.manufacture_id` NOT NULL) |
| **3** | **File đính kèm · Mã màu · Thuế suất** (3 màn nhóm `Common`, mỗi màn một đặc thù) |

Đợt 1 là chốt chặn: chứng minh nền mở rộng chạy được mà không vỡ Phase 0 trước khi nhân ra 8 màn còn lại.

## Ngoài phạm vi Phase 1

3 màn con Hãng sản xuất (Kế hoạch mua hàng · KPI bán hàng · Cấu hình nhân viên) · khối "Chi phí
tính giá hàng hóa" (`manufacture_costs` **0 dòng**) · 4 cột `since_*` (đã bị comment trong ERP) ·
route `unit.updateEnglishName` · `codeColor.printList` · xuất CSV/PDF · cột chết
`attributes.attributeset_id` · cột `icon`/`image` không màn nào dùng.
