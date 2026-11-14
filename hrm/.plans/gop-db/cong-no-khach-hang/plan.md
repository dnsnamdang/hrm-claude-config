# Plan — Công nợ khách hàng

## Màn 1 — Sổ chi tiết công nợ phải thu KH (XONG 10/11/2026)

- [x] Tách `PartnerLedgerService` từ `SupplierDebtDetailService` (NCC giữ nguyên hành vi — test NCC xanh)
- [x] `CustomerLedgerDetailService` + `CustomerLedgerDetailController` + route `/customer-ledger-details`
- [x] Catalog: mã `accounting.so_chi_tiet_cong_no_phai_thu_khach_hang.view` thêm `hrm`
- [x] Sửa nền test công nợ (`EmployeeDebtDetailTestCase`) gán quyền theo RBAC (seeder/bảng cũ không còn) — 37 test cũ xanh lại
- [x] Test `CustomerLedgerDetailTest` 5 ca (chỉ local, `.git/info/exclude`)
- [x] FE `pages/finance/customer-ledger-details` (khuôn NCC) + nhận bộ lọc qua query + menu `codes`
- [x] Đối chiếu ERP (`DetailDebtCustomerService`) 8 ca + bấm thật local

## Màn 2 — Bảng cân đối phát sinh công nợ KH (XONG 10/11/2026)

- [x] Tách `AccountBalanceService` từ `EmployeeDebtBalanceService` (NV giữ nguyên số — test + so JSON trước/sau)
- [x] `CustomerDebtBalanceService` + controller + route `/customer-debt-balances`; Catalog thêm `hrm`
- [x] Sổ chi tiết KH: bộ lọc tổ chức (Phòng ban / Bộ phận) + nhận qua link, BE lọc `ad.department_id` / `ad.part_id`
- [x] Test `CustomerDebtBalanceTest` 6 ca (chỉ local); 48 test nhóm công nợ xanh
- [x] FE `pages/finance/customer-debt-balances` + menu `codes`; đối chiếu ERP 8 ca khớp; bấm thật (drill, In, Excel, Ngoại tệ)

## Phase 3 — Chuyển 3 màn NV/NCC sang kiểm quyền theo mã + lên develop (10/11/2026)

- [x] `AccountDebtCommon` đọc phạm vi theo mã (4 = Tổng công ty, 3 = Công ty), mỗi màn khai mã của mình; 2 màn KH bỏ đoạn kiểm quyền riêng, dùng chung
- [x] Test: `EmployeeDebtDetailTestCase` cấp quyền theo mã (commit kèm), 5 file test NV/NCC đổi hằng cũ `PERM_ALL`/`PERM_COMPANY` ⇒ `[mã => phạm vi]`; 48 test công nợ xanh
- [x] Menu Sổ chi tiết công nợ NCC ẩn/hiện theo mã (2 mục NV vẫn hiện mọi người như ERP)
- [x] Commit api `6a2785167`, client `ea2efdf91`; merge develop + push: api `df407199e`, client `39c427075` (giữ 3 bản sửa QA #12069 / #12068 / #12063 khi giải xung đột)
- [x] Kiểm trên dev-hrm: 2 màn KH mở được, TK 131 năm 2026 ra 3.994 dòng, quyền sync đã chạy

## Ghi chép ngày (note cuối ngày)

- [x] 10/11/2026 — Làm chuyển đổi erp->hrm: Sổ chi tiết công nợ phải thu khách hàng - 100% (`/finance/customer-ledger-details`, đã lên develop/dev)
- [x] 10/11/2026 — Làm chuyển đổi erp->hrm: Bảng cân đối phát sinh công nợ khách hàng - 100% (`/finance/customer-debt-balances`, đã lên develop/dev)
- [x] 10/11/2026 — Xử lý chuyển 3 màn Sổ chi tiết công nợ NV, Bảng cân đối công nợ NV, Sổ chi tiết công nợ NCC sang kiểm quyền theo mã Catalog; sửa nền test công nợ (37 test đỏ sẵn từ khi lên RBAC)
- [x] 10/11/2026 — Xử lý sắp lại worktree hrm-api/hrm-client (`.worktrees/develop`, `.worktrees/gop_db`), gỡ nhánh feat đang track nhầm `origin/gop_db`/`origin/develop` + đặt `branch.autoSetupMerge = simple` ở 4 repo (tránh nút Sync đẩy nhầm)
- [ ] 12/11/2026 — Lỗi #12142 (Bảng cân đối phát sinh công nợ KH): Số tiền gộp 1 ô "từ → đến" như màn NV; ô lọc đổi nhãn "KH/NCC" + gợi ý "Nhập tên, số điện thoại hoặc mã KH/NCC để tìm kiếm", tối thiểu 2 ký tự (BE vốn đã tìm theo mã/tên/SĐT); Excel tiêu đề chỉ tên báo cáo, dòng "Từ ngày … đến ngày …" chữ nhỏ nghiêng bên dưới; cột "Mã KH/NCC", "Tên KH/NCC" ở màn, Excel, In. Đã kiểm local bằng ảnh + mở file Excel. **Chưa commit** (worktree `.worktrees/develop`).
- [ ] 12/11/2026 — Lỗi #12140 (Sổ chi tiết công nợ phải thu KH): ô Khách hàng tối thiểu 2 ký tự; Số tiền gộp 1 ô; Excel có dòng kỳ báo cáo dưới tiêu đề, cột Đơn hàng/Hợp đồng, Ngày hạch toán, Tài khoản đối ứng đủ rộng; dấu ":" thẳng hàng trên bản In (khối dùng chung ⇒ sửa cả 6 màn công nợ KH/NCC/NV). Helper `utils/export/listExportFile.js` thêm tuỳ chọn `docSubtitle` (user đồng ý; màn khác không truyền thì như cũ). **Chưa commit** (develop). Bộ test BE công nợ không chạy được local (DB test thiếu mã quyền).
- [x] 13/11/2026 — Commit #12140 + #12142 (phần ghi 12/11 ở trên): api `262a691a0`, client `a286586df` (develop, đã push).
