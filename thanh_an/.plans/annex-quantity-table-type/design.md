# Phụ lục thay đổi số lượng — Hỗ trợ 2 kiểu bảng

## Mục tiêu
Cho phép mỗi phụ lục thay đổi số lượng chọn 1 trong 2 kiểu bảng hàng hóa:
- **Kiểu A** (cũ): SL trên HĐ | SL sau đ/c | Đơn giá | Thành tiền trên hđ | Thành tiền sau đ/c
- **Kiểu B** (mới): SL trên HĐ | SL điều chỉnh (+) | Đơn giá | Thành tiền (đơn giá × SL điều chỉnh)

## Scope
- Thêm `table_type` vào `data` JSON của `contract_annexes`
- FE: toggle kiểu bảng trên ProductComponent, ẩn/hiện cột tương ứng
- BE: print template render theo kiểu bảng
- Phụ lục cũ → Kiểu A. Phụ lục mới → mặc định Kiểu B.

## Quyết định lớn
- Lưu `table_type` trong `data` JSON (không migration)
- SL điều chỉnh chỉ nhập số dương
- Chuyển kiểu → reset số lượng về 0 (có confirm)

## Spec chi tiết
→ `docs/superpowers/specs/2026-05-08-annex-quantity-table-type-design.md`
