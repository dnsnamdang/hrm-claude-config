# Báo cáo hạn mức công nợ nhân viên — design (tóm tắt)

> Người phụ trách: @khoipv · Nhánh: `develop` (con của `gop_db`) cả 2 repo
> Spec chi tiết: `docs/superpowers/specs/gop-db/2026-10-14-report-limit-debt-employees-design.md`
> Màn chị em (đã port 13/10): `.plans/gop-db/report-limit-debts/` (Báo cáo hạn mức công nợ khách hàng)

## Mục tiêu
Chuyển màn ERP "Báo cáo hạn mức công nợ nhân viên" (`report_limit_debts.index?type=employee`, menu Kế toán › Kế toán
Công nợ › Nhân viên) sang HRM: `/finance/report-limit-debt-employees`, gắn link vào mục menu có sẵn ở
`components/subsystem-menu/finance.js`.

## Phạm vi
- Màn chỉ đọc: NV có `employees.limit_export_debt > 0` + tổng công nợ KH hiện tại (sổ 131, HĐ do NV tạo).
- Popup "Thông tin chi tiết hạn mức dư nợ nhân viên theo khách hàng" (bấm mã NV) — lọc KH / Số tiền từ / đến.
- Xuất Excel (chọn trường) + Cấu hình cột — bộ bắt buộc của HRM. Ô tìm nhanh mã/tên NV (chuẩn HRM).

## Quyết định (user chốt 14/10/2026)
1. **Nguồn hạn mức**: y ERP — `employees.limit_export_debt`. DB hiện KHÔNG NV nào > 0 và HRM chưa có ô nhập →
   màn trống tới khi có dữ liệu. ERP bỏ ô nhập khỏi form Sửa tài khoản từ 2022 → **Phase 2** thêm ô "Hạn mức công nợ
   xuất hàng" vào form Tài khoản nhân viên HRM (`/human/employee`, Thêm + Sửa, có ghi lịch sử).
2. **Phạm vi**: y ERP — không quyền, xem mọi công ty; lọc Công ty / Phòng ban / Bộ phận / Nhân viên tuỳ ý.
3. **Sửa lỗi ERP** như bản KH: công nợ = `CustomerDebtAggregator` gom theo `contract_created_by`, dư cuối kỳ tới
   Đến ngày; ô lọc Nhân viên ăn thật (ERP ô chết); popup tách đúng theo KH (ERP cộng dồn + Đến ngày = Từ ngày).

## Thành phần
- BE: `Modules/Finance/Services/CustomerDebt/ReportLimitDebtEmployeeService.php`,
  `Http/Controllers/V1/ReportLimitDebtEmployeeController.php`, route `finance/report-limit-debt-employees`
  (`/`, `/meta`, `/export-rows`, `/employees/{id}/customers`).
- FE: `pages/finance/report-limit-debt-employees/index.vue` + `components/DebtByCustomerModal.vue` — bám màn chị em.
- Không migration, không quyền mới.
