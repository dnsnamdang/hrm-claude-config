# Nhóm hàng hoá — Đổi tên + Phân cấp (Tóm tắt)

**Ngày:** 2026-06-04
**Phụ trách:** @manhcuong
**Spec chi tiết:** `docs/superpowers/specs/2026-06-04-product-type-hierarchy-design.md`
**Thuộc:** MODULE 1 — Danh mục & Cấu hình (DM-03)

## Scope

Hoàn thiện DM-03 trong checklist:
1. Đổi tên "Loại hàng hoá" → "Nhóm hàng hoá" (menu, FE, permission, export).
2. Thêm phân cấp cha-con (không giới hạn cấp), hiển thị tree-table.

Module: Category (BE `Modules/Category`, FE `pages/category/product-types`).

## Quyết định chính

- Mã prefix `LHH` → `NHH` (dữ liệu cũ giữ nguyên).
- Phân cấp **không giới hạn cấp**.
- Danh sách hiển thị **tree-table** (dùng slot `V2BaseDataTable`, KHÔNG sửa component chung).
- Permission: đổi tên + update DB theo `id` (giữ role assignment).
- `is_can_delete`: cấm xóa nếu còn sản phẩm HOẶC còn nhóm con.
- Gán sản phẩm: bất kỳ cấp (cha/con).
- Import: thêm cột "Mã nhóm cha" (optional).
- URL `/category/product-types` giữ nguyên.

## Thay đổi chính

- DB: thêm `parent_id` (nullable) vào `product_types`.
- BE: parent/children/getDescendantIds, isCanDelete, Request chống chu trình, Service tree + import parent_code.
- FE: tree-table + field "Nhóm cha" trong modal.
