# Plan — Cho phép Khóa danh mục ngân hàng đã được sử dụng

Phụ trách: @khoipv

## Phase 1 — FE: tách điều kiện nút Khóa khỏi can_delete

- [x] Sửa `hrm-client/pages/human/banks/index.vue`: điều kiện nút "Khóa" từ `status == 1 && item.can_delete` → chỉ `status == 1`
- [ ] Verify: ngân hàng đã dùng vẫn hiện Khóa, ẩn Xóa; ngân hàng chưa dùng hiện cả hai

## Ghi chú
- `can_delete = false` khi ngân hàng đang được dùng ở `employee_bank_accounts` / `employee_authorized_bank_accounts` (`Bank::canDelete()`).
- BE `BankController::lock` không chặn ngân hàng đã dùng → không cần sửa BE.
