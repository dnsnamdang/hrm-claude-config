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
