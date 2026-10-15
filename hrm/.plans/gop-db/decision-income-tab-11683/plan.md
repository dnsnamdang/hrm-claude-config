# Redmine #11683 (nhánh gop_db — worktrees/gop_db-client) — Tab Thu nhập QĐ bổ nhiệm / điều chuyển / điều chỉnh lương (@cuong61n)

## Phase 1 — Fix
### FE
- [x] QĐ bổ nhiệm: chọn NV → ô tick BHXH/công đoàn + tham gia BH/thuế TNCN từng khoản (thâm niên, P1, P2, P3) cột "Sau" lấy theo thu nhập hiện tại (điều chuyển/điều chỉnh lương đã copy nguyên data cũ sẵn)
- [x] 3 màn: bọc 12 bảng tab Thu nhập bằng V2BaseTableScroll + fieldset min-width:0 (hết bảng đè sang cột bên kia), ô Bậc năng lực P2 min-width 200px
- [ ] Hỗ trợ theo quy chế (xăng xe…): chờ tester trả lời câu A–D (using_manpower, support_other, bảng nào, khớp theo chức vụ)
