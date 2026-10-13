# Báo cáo hạn mức công nợ khách hàng — design (tóm tắt)

> Người phụ trách: @khoipv · Nhánh: `develop` (con của `gop_db`) cả 2 repo
> Spec chi tiết: `docs/superpowers/specs/gop-db/2026-10-13-report-limit-debts-design.md`

## Mục tiêu
Chuyển màn ERP "Báo cáo hạn mức công nợ khách hàng" (`report_limit_debts.index`, menu Kế toán › Kế toán Công nợ ›
Khách hàng) sang HRM: `/finance/report-limit-debts`, gắn link vào mục menu đã khai sẵn ở `components/subsystem-menu/finance.js`.

## Phạm vi
- Màn chỉ đọc: danh sách KH có hạn mức (tính lãi / được nợ > 0) của công ty người đăng nhập + số dư nợ hiện tại.
- Popup "Chi tiết hạn mức dư nợ khách hàng theo NVKD" (ⓘ cạnh mã KH).
- Xuất Excel (chọn trường) + Cấu hình cột — bộ bắt buộc của HRM.
- KHÔNG làm: "Báo cáo hạn mức công nợ nhân viên" (`?type=employee`) — feature riêng sau.

## Quyết định (user chốt 13/10/2026)
1. **Số dư nợ**: ERP luôn ra 0 (lỗi gom nhóm). HRM dùng công thức sổ 131 chung `CustomerDebtAggregator` — dư cuối kỳ
   tới "Đến ngày" (trống = hôm nay), khớp Báo cáo chi tiết công nợ KH.
2. **Phân quyền**: không quyền, y ERP — bó theo công ty người đăng nhập.
3. **Popup NVKD**: port và sửa đúng (ERP truyền nhầm id, cộng dồn sai).
4. Chỉ màn khách hàng.

## Thành phần
- BE: `Modules/Finance/Services/CustomerDebt/ReportLimitDebtService.php`, `Http/Controllers/V1/ReportLimitDebtController.php`,
  route `finance/report-limit-debts` (`/`, `/meta`, `/export-rows`, `/customers/{id}/employees`).
- FE: `pages/finance/report-limit-debts/index.vue` + `components/DebtByEmployeeModal.vue`. Khuôn: `pages/admin/benefit-rates`.
- Không migration, không quyền mới.
