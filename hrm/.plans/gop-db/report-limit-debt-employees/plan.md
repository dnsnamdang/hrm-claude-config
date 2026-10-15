# Báo cáo hạn mức công nợ nhân viên — plan

> Người phụ trách: @khoipv · Nhánh: `develop` (con của `gop_db`) cả 2 repo
> Design: `design.md` · Spec: `docs/superpowers/specs/gop-db/2026-10-14-report-limit-debt-employees-design.md`

## Quyết định đã chốt (14/10/2026)
- Hạn mức: y ERP `employees.limit_export_debt` (hiện chưa NV nào khai → màn trống).
- Phạm vi: không quyền, xem mọi công ty (y ERP).
- Sửa lỗi ERP như bản KH (công thức sổ 131 chung, ô lọc NV, popup theo KH).

## Phase 1 — Port màn

### BE (`hrm-api/Modules/Finance`)
- [x] `Services/CustomerDebt/ReportLimitDebtEmployeeService.php` — danh sách + lọc + sort + phân trang PHP, công nợ qua `CustomerDebtAggregator` (gom `contract_created_by`), popup theo KH, export-rows
- [x] `Http/Controllers/V1/ReportLimitDebtEmployeeController.php` — index / meta / export-rows / customers
- [x] Route `finance/report-limit-debt-employees` (không checkPermission — ERP không gate)
- [x] Docblock "Nơi đang dùng" của `CustomerDebtAggregator`
- [x] Smoke test service (transaction gán tạm hạn mức 5 NV rồi rollback) + HTTP kernel (200 / 404 / 422)

### FE (`hrm-client`)
- [x] `pages/finance/report-limit-debt-employees/index.vue` — SmartFilterPanel floating (Thời gian · Công ty/PB/BP/NV · Chỉ tiêu) + V2BaseDataTable + Cấu hình cột + Xuất Excel
- [x] `components/DebtByCustomerModal.vue` — popup dư nợ NV theo KH (lọc KH / Số tiền từ / đến)
- [x] Menu `components/subsystem-menu/finance.js` — gắn link mục "Báo cáo hạn mức công nợ nhân viên"
- [x] Compile check (vue-template-compiler + babel) + grep checklist skill

## Phase 2 — Ô nhập "Hạn mức công nợ xuất hàng" ở form Tài khoản nhân viên (user chốt 14/10/2026)

Lý do: ERP đã bỏ ô này khỏi form SỬA tài khoản từ 12/11/2022 (commit `a7e8387700`), chỉ còn ở form Thêm → không ai khai
được, báo cáo trống. Thêm vào form HRM `/human/employee` (Quản trị hệ thống › Người dùng & phân quyền › Tài khoản nhân viên).

- [x] BE `CreateEmployeeRequest` / `UpdateEmployeeRequest` — `limit_export_debt` nullable|numeric|min:0|max + message tiếng Việt
- [x] BE `EmployeeService::createEmployee/updateEmployee` — ghi `employees.limit_export_debt` (update chỉ ghi khi request có key)
- [x] BE lịch sử: thêm `limit_export_debt` vào `buildHistorySnapshot` + điều kiện `$nonStatusChanged`
- [x] FE `components/human-components/employee/EmployeeForm.vue` — ô tiền `V2BaseCurrencyInput` + lỗi inline
- [x] FE `EmployeeHistoryModal.vue` — nhãn trường + định dạng số `1,234,567` + option lọc trường
- [x] Smoke test (transaction rollback) + compile
- [x] (user báo 14/10) Vào `/human/employee/add` tự hiện "0 chức năng khớp <email>": Chrome tự điền tài khoản đã lưu, Email bị `disabled` nên email rơi vào ô "Tìm chức năng…" của `SaleHubSidebar` → 2 ô mật khẩu `autocomplete="new-password"` (lỗi có sẵn, không do Phase 2)
- [x] (user báo 14/10) Dời ô xuống cuối cột trái (sau Mã check in cơm); ép cỡ chữ/cao/padding về đúng `.form-control` (V2BaseCurrencyInput md là 14px/38px, form này 0.8rem)

## Phase 3 — Bộ lọc popup theo khuôn base (user yêu cầu 14/10/2026)

- [x] FE `DebtByCustomerModal.vue` — bỏ lưới ô lọc tự dựng, thay `V2BaseSmartFilterPanel floating in-modal` (skill modal-popup 4c): ô tìm nhanh + Khách hàng (chọn là tìm luôn) + Số tiền từ → đến gộp 1 ô (slot `#field-money_range`, khuôn `bill-adjust-dept-requests`), Enter/Tìm kiếm, Làm mới
- [x] BE `debtByCustomer` — thêm `keyword` (mã / tên KH, không phân biệt hoa thường); options ô Khách hàng vẫn là đủ KH
- [x] Compile + test service (kw mã 1 dòng, kw tên khớp đúng, kw rác 0, kw + số tiền kết hợp)
- [x] (user yêu cầu 14/10) Commit + push `develop` cả 2 repo: API `0b71cfa32`, Client `3da3329aa` (rebase lên origin, không xung đột)

### Checkpoint — 2026-10-14
Vừa hoàn thành: BE + FE + menu. Smoke test (dữ liệu tạm trong transaction, đã rollback): 5 NV ~1,2s; chỉ tiêu Trong 4 / Vượt 1; từ khoá, ô NV, Công ty, Phòng ban, sort đúng; popup 65 KH tổng 167,134,531 = cột chính; lọc Số tiền từ ăn; NV không hạn mức → 404; Đến ngày < Từ ngày → 422 tiếng Việt.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm `/finance/report-limit-debt-employees` (chưa bấm thật). DB không NV nào có hạn mức → muốn thấy dữ liệu phải tự khai `employees.limit_export_debt` cho vài NV.
Blocked:

### Checkpoint — 2026-10-14 (Phase 2)
Vừa hoàn thành: ô "Hạn mức công nợ xuất hàng" ở form Tài khoản nhân viên (`/human/employee` Thêm + Sửa) + ghi lịch sử. Smoke test HTTP (transaction, đã rollback): GET chi tiết trả `limit_export_debt`; nhập -5 → 400 "Hạn mức công nợ xuất hàng không được âm"; lưu 150,000,000 → DB đúng, log `update` 0 → 150000000, báo cáo NV ra 1 dòng; PUT không gửi khoá → giữ nguyên hạn mức. Compile FE pass.
Đang làm dở: —
Bước tiếp theo: user mở `/human/employee` → Sửa 1 tài khoản → nhập hạn mức → Lưu → mở `/finance/report-limit-debt-employees` kiểm (chưa bấm thật trình duyệt).
Blocked:
