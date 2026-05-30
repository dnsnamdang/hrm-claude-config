# Hạn mức công nợ theo từng khách hàng — Design (Tóm tắt)

**Phụ trách:** @khoipv | **Ngày:** 2026-05-19
**Spec chi tiết:** [`docs/superpowers/specs/2026-05-19-customer-credit-limit-design.md`](../../docs/superpowers/specs/2026-05-19-customer-credit-limit-design.md)
**Thay thế:** Spec cũ `2026-05-18-customer-group-credit-limit-design.md` (hạn mức ở nhóm KH)

## Mục tiêu

Chuyển hạn mức công nợ từ cấp **nhóm khách hàng** (`customer_groups`) xuống cấp **từng khách hàng** (`category_customers`). Nhóm KH chỉ còn là danh mục phân loại.

## Phạm vi

| Layer | Thay đổi |
|---|---|
| DB | Migration 1: thêm `max_debt_limit` (decimal 18,2 nullable) + `is_debt_limit_active` (tinyint default 0) vào `category_customers` |
| DB | Migration 2: xóa 2 cột tương ứng khỏi `customer_groups` |
| BE Customer | Thêm validation, filter, 2 field trong store/update, resource, log mapping |
| BE Customer Group | Xóa validation, filter, 2 field trong CRUD, resource, log mapping |
| FE Form KH | Thêm toggle switch + number input format VND (style giống nhóm KH cũ) |
| FE List KH | Thêm 2 cột + filter "Áp dụng hạn mức" |
| FE Nhóm KH | Xóa toggle + input trong modal, xóa 2 cột + filter trong list |
| Specs | Cập nhật 2 spec (payment terms, debt violation rules) tham chiếu `category_customers` thay vì `customer_groups` |

## Quyết định lớn

- **Xóa hoàn toàn** 2 cột khỏi `customer_groups` — không giữ lại
- **Không auto-copy** data từ nhóm KH sang KH — tất cả KH bắt đầu sạch
- **UI giống hệt** nhóm KH cũ: toggle iOS + input format VNĐ + disable khi toggle OFF
- **2 migration riêng** (thêm trước, xóa sau) — an toàn hơn gộp 1
