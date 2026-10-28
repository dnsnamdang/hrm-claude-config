# Báo cáo hạn mức công nợ khách hàng — plan

> Người phụ trách: @khoipv · Nhánh: `develop` (con của `gop_db`) cả 2 repo
> Design: `design.md` · Spec: `docs/superpowers/specs/gop-db/2026-10-13-report-limit-debts-design.md`

## Quyết định đã chốt (13/10/2026)
- Dư nợ: dùng công thức sổ 131 chung `CustomerDebtAggregator` (ERP luôn ra 0 do lỗi gom nhóm).
- Phạm vi: KHÔNG quyền, y ERP — chỉ hạn mức của công ty người đăng nhập.
- Popup chi tiết dư nợ theo NVKD: port và sửa đúng.
- Chỉ màn khách hàng (màn nhân viên làm sau).

## Phase 1 — Port màn

### BE (`hrm-api/Modules/Finance`)
- [x] `Services/CustomerDebt/ReportLimitDebtService.php` — danh sách + lọc + sort + phân trang PHP, dư nợ qua `CustomerDebtAggregator`, popup theo NV, export-rows
- [x] `Http/Controllers/V1/ReportLimitDebtController.php` — index / meta / export-rows / employees
- [x] Route `finance/report-limit-debts` (không checkPermission — ERP không gate)
- [x] Cập nhật docblock "Nơi đang dùng" của `CustomerDebtAggregator`
- [x] Smoke test API (tinker / HTTP kernel)

### FE (`hrm-client`)
- [x] `pages/finance/report-limit-debts/index.vue` — SmartFilterPanel floating + V2BaseDataTable + Cấu hình cột + Xuất Excel (`exportListFile`)
- [x] `pages/finance/report-limit-debts/components/DebtByEmployeeModal.vue` — popup chi tiết dư nợ theo NVKD
- [x] Menu `components/subsystem-menu/finance.js` — gắn link mục "Báo cáo hạn mức công nợ khách hàng"
- [x] Compile check (vue-template-compiler + babel)

### Tài liệu
- [x] design.md + spec chi tiết

### Checkpoint — 2026-10-13
Vừa hoàn thành: BE (service + controller + route) + FE (danh sách + popup NVKD + menu). Smoke test API qua HTTP kernel: danh sách 200 (38 dòng công ty 1, ~0,5s), lọc chỉ tiêu 1-4 / loại hình / từ khoá / sort đúng, 422 khi Đến ngày < Từ ngày, popup NVKD 200 tổng khớp cột Số dư nợ, KH không có hạn mức → 404, export-rows đúng cột theo `fields`. Compile FE pass, grep checklist skill sạch.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm `/finance/report-limit-debts` (chưa bấm thật: bộ lọc, popup, Xuất Excel, Cấu hình cột).
Blocked:

## Phase 2 — Fix Redmine #11766 (2026-10-19)
- [x] BUG 1: ô tìm nhanh bỏ tìm theo SĐT — BE bỏ `orWhere c.mobile`, FE sửa placeholder "Tìm theo mã, tên khách hàng"
- [x] BUG 2: popup chi tiết theo NVKD mở ra KHÔNG sắp sẵn cột Công nợ (y ERP, icon ⇅) — FE `sortField` rỗng mặc định, BE chỉ sort khi có `sort_desc`
- [x] BUG 3a: thứ tự mặc định y ERP = id dòng hạn mức tăng dần (đang created_at giảm dần → ngược)
- [x] BUG 3b: Hạn mức tính lãi / được nợ trống → hiện 0 như ERP (BE trả 0, FE giữ số 0)
- [x] BUG 3c: Số dư nợ hiện tại — GIỮ công thức sổ 131 (ERP lỗi luôn ra 0, user chốt 13/10) → báo lại tester
- [x] Verify: php -l + smoke test API, compile FE

### Checkpoint — 2026-10-19
Vừa hoàn thành: fix #11766 — BE `ReportLimitDebtService` (bỏ tìm SĐT, sort mặc định id tăng dần, hạn mức NULL → 0, popup chỉ sort khi có `sort_desc`); FE `index.vue` (placeholder, hạn mức hiện 0) + `DebtByEmployeeModal.vue` (`sortField` rỗng mặc định). Smoke test service: thứ tự khớp ERP, tìm SĐT = 0 dòng, tìm mã = 1; compile FE pass.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm lại 3 bug; báo tester cột Số dư nợ lệch ERP là CHỦ ĐÍCH (ERP lỗi luôn ra 0).
Blocked:

## Redmine #11777 — lọc "Chỉ tiêu vượt hạn mức" lệch ERP (22/10) — ĐIỀU TRA, CHƯA SỬA
- [x] Điều tra: lệch do quyết định 13/10 (giữ công thức sổ 131). ERP `AccountDetail::getDebtCustomer()` (erp M:2290) chỉ select SUM, KHÔNG select `customer_id` rồi groupBy → mọi KH tra ra rỗng → dư nợ = 0 → "Trong hạn mức tính lãi" = MỌI dòng có hạn mức tính lãi > 0, "Vượt…" luôn rỗng. HRM dùng dư nợ thật nên KH nợ ≥ hạn mức rơi sang "Vượt"
- [x] Dữ liệu ảnh 19/10 (35TNXHA-1…) không còn tra được trên dev (màn Khai báo hạn mức không ra các KH đó; báo cáo chi tiết công nợ trả customer_code null) — chưa đối chiếu được số cụ thể
- [x] User chốt 22/10: "sửa lại giống hệt ERP" → `ReportLimitDebtService`: cột Số dư nợ hiện tại luôn 0 (bỏ `debts()`); `filterTarget()` y ERP với dư nợ 0: chỉ tiêu 1 = dòng có hạn mức tính lãi > 0, chỉ tiêu 2/3/4 luôn rỗng (ERP so cột không tồn tại `limit_export_debt`). Popup NVKD + lọc Khách hàng theo customer_id GIỮ bản sửa 13/10
  - Verify: php -l OK; tinker công ty 1: tất cả 40 dòng, chỉ tiêu 1 = 3 (= số dòng hạn mức tính lãi > 0 trong DB), 2/3/4 = 0, dư nợ ≠ 0: 0 dòng. Chưa mở trình duyệt

## Redmine #11776 — ô lọc Khách hàng không tìm được KH (22/10)
- [x] Nguyên nhân: ô lọc dùng `assign/customers/search` (bó phạm vi xem KH của Giao việc: KH cá nhân chỉ ra cho người phụ trách) → "BÔNG" (67DAONA, cá nhân) không ra. ERP dùng `customers.searchCustomerByKeywords` = toàn bộ bảng customers
- [x] BE: `GET finance/report-limit-debts/customers?q=` → `ReportLimitDebtService::searchCustomers()` y ERP (tên / SĐT / mã, mới tạo trước, < 3 ký tự lấy 20); khác ERP: ≥ 3 ký tự chặn 50 (ERP trả hết — "CÔNG TY" ~11.000 KH)
- [x] FE `index.vue` `searchCustomers()` đổi url sang endpoint mới
  - Verify: php -l ×3, compile FE OK; HTTP kernel: "BÔNG" 8 KH (gồm KH cá nhân 29TPHXCH-9), "CÔNG TY" 50, lọc báo cáo theo customer_id → đúng 1 dòng. Chưa mở trình duyệt
