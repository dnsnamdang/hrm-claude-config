# Nhà cung cấp (Supplier) — Tóm tắt

**Ngày:** 2026-06-05
**Phụ trách:** @manhcuong
**Spec chi tiết:** `docs/superpowers/specs/2026-06-05-supplier-category-design.md`
**Thuộc:** MODULE 1 — Danh mục & Cấu hình (DM-04)

## Scope

Tạo MỚI 2 danh mục trong module Category (nền cho module Mua hàng sau này):
1. **Nhóm nhà cung cấp** (`supplier_groups`) — CRUD đơn giản (copy Manufacturer).
2. **Nhà cung cấp** (`suppliers`) — có bảng con `supplier_contacts` (nhiều liên hệ).

Giữ `Manufacturer` làm "Hãng sản xuất" (không đụng).

## Quyết định chính

- 3 bảng: `supplier_groups`, `suppliers`, `supplier_contacts`.
- Mã: NCC.xxxx (suppliers), NNCC.xxxx (supplier_groups) — nhập tay, regex như manufacturer.
- Nhà cung cấp: MST, nhóm NCC, địa chỉ (Tỉnh→Phường/Xã cascading + ô số nhà/đường), SĐT, email, ghi chú + nhiều liên hệ (tên/chức vụ/SĐT/email).
- **Xóa:** nhóm NCC cấm xóa nếu còn NCC; NCC **cấm xóa** (chỉ Khóa/Mở khóa).
- Bỏ đánh giá NCC; lịch sử giao dịch chờ module Mua hàng.
- Form NCC: modal size xl (địa chỉ cascading + bảng liên hệ động).
- Import NCC: trường phẳng, không import liên hệ.
- 4 permission mới; menu thêm "Nhà cung cấp" + "Nhóm nhà cung cấp".

## Thứ tự build
① Nhóm NCC (supplier_groups) → ② NCC + liên hệ (suppliers + supplier_contacts).
