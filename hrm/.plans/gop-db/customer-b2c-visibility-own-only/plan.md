# Khách cá nhân chỉ hiện khi liên quan tới mình — @cuong61n

Nhánh `gop_db` (worktree `worktrees/gop_db-api`). Redmine: chưa có số.

## Nghiệp vụ chốt
- Khách tổ chức: hiện đầy đủ.
- Khách cá nhân: hiện sẵn khi mình là người tạo, hoặc mình đã phát sinh chứng từ (báo giá, meeting, dự án TKT, công nợ đầu kỳ).
- Khách cá nhân của người khác: chỉ hiện khi nhập đúng toàn bộ số điện thoại.

## Task
- [x] 1. BE `CustomerService::applyB2cOwnershipVisibility`: bỏ điều kiện hiện theo chứng từ của người khác và theo người khác đăng ký (2026-11-10)
- [x] 2. BE `CustomerOwnership::myInteractionCustomerIds`: thêm công nợ đầu kỳ do mình khai báo, bảng `declare_debt_beginning` (2026-11-10)
- [ ] 3. Chạy thử API với 2 tài khoản: khách cá nhân của người khác không hiện, hiện khi gõ đúng số điện thoại
- [ ] 4. Hỏi lại: khách tổ chức ở màn danh sách chính vẫn bị lọc theo quyền xem (`applyVisibilityScope`), chưa "full" như popup

Trạng thái: đã sửa code trên nhánh `gop_db`, chưa commit, chưa test.

## #12115 — rà lại theo task Redmine (2026-11-10)
- [x] 5. Task ghi "Hợp đồng bán đầu kỳ" (bảng `opening_contracts`), không phải `declare_debt_beginning` → đổi nguồn trong `CustomerOwnership::myInteractionCustomerIds`
- [x] 6. Dropdown chọn khách (`searchForSelect2`, dùng ở form Hợp đồng bán đầu kỳ) chỉ có 1 ô gõ: gõ trọn SĐT (≥ 8 số) thì tìm chính xác để khách cá nhân của người khác hiện ra
- [x] 7. Test local: người tạo thấy khách qua mã; người khác tìm mã/tên không thấy, tìm SĐT thấy; khách tổ chức thấy đủ
- [x] Đã đẩy prod bản đầu (commit 463dddc62). Bản sửa 5–6: đã commit local trên `gop_db`, chờ user cho đẩy
