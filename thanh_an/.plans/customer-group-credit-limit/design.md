# Hạn mức công nợ cho nhóm khách hàng — Design (Tóm tắt)

**Phụ trách:** @khoipv | **Ngày:** 2026-05-18
**Spec chi tiết:** [`docs/superpowers/specs/2026-05-18-customer-group-credit-limit-design.md`](../../docs/superpowers/specs/2026-05-18-customer-group-credit-limit-design.md)

## Mục tiêu

Bổ sung 2 trường vào màn `pages/category/customer_groups`:
1. **Hạn mức công nợ tối đa (VNĐ)** — số tiền tối đa cho nhóm KH này
2. **Trạng thái áp dụng hạn mức** — toggle bật/tắt việc áp dụng

## Phạm vi

| Layer | Thay đổi |
|---|---|
| DB | Migration thêm 2 cột `max_debt_limit` (decimal 18,2 nullable) + `is_debt_limit_active` (tinyint default 0) vào `customer_groups` |
| BE | Reuse endpoint hiện có, thêm validation `required_if`, thêm filter `is_debt_limit_active` |
| FE Modal | Thêm toggle switch + number input có format VND, input disable khi toggle OFF nhưng giữ giá trị |
| FE List | Thêm 2 cột hiển thị + filter "Áp dụng hạn mức", map tên VN cho log lịch sử |

## Quyết định lớn

- **Toggle switch** (iOS style) thay vì Select dropdown
- **Disable + giữ giá trị** khi toggle OFF — không clear data
- **Validate `> 0`** khi toggle ON
- **Hiển thị `—`** trong list khi toggle OFF (không show số mờ)
- CSS toggle viết scoped trong modal, không tạo component chung
