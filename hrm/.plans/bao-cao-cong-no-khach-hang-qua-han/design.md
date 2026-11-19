# Báo cáo công nợ khách hàng quá hạn — port ERP → HRM

Ngày: 19/11/2026 · Nhánh: `develop` (hrm-api + hrm-client) · KHÔNG sửa ERP.

## 1. Mục đích

Port màn ERP **"Báo cáo công nợ quá hạn"** (`/report/handle-debt-overdue`) sang HRM, đổi tên thành
**"Báo cáo công nợ khách hàng quá hạn"**, giúp kinh doanh/kế toán thấy HĐ nào còn nợ và đã quá hạn bao nhiêu
ngày theo **quy chế** (mốc để HĐ được hưởng đủ 100% thưởng năng suất).

Yêu cầu gốc chia 2 chỉ tiêu:
- **Chỉ tiêu 1 – Xét theo HĐ** (điều kiện thanh toán trên HĐ): **anh Nam tự thiết kế và làm sau → KHÔNG làm.**
- **Chỉ tiêu 2 – Xét theo quy chế**: form như ERP + 2 cột mới ở dòng HĐ → **phạm vi của đợt này.**

## 2. Quyết định đã chốt (user)

| # | Nội dung | Chốt |
|---|---|---|
| Q1 | Ô chọn chỉ tiêu | **Chưa hiện ô chọn / tab** — màn chỉ có form "Xét theo quy chế". Anh Nam thêm sau. |
| Q2 | Nhãn ô "Báo cáo theo" (ERP ghi lệch: "Khách hàng" ra cây Phòng→NV→KH→HĐ, "Nhân viên" ra cây KH→HĐ) | **Đặt lại nhãn đúng**: `1` = "Theo phòng ban – nhân viên", `2` = "Theo khách hàng". Số liệu giữ nguyên. |
| Q3 | Dòng HĐ gộp HĐ gốc + phụ lục — Ngày BGNT / Quy chế lấy đâu | **Theo HĐ gốc** (đúng mã HĐ đang hiển thị trên dòng). |

## 3. Nguồn ERP (chỉ đọc)

- Controller `ReportController::handleDebtOverDue*` (dòng ~5262), Service `app/Services/Reports/HandleDebtOverDueService.php`,
  Blade `resources/views/reports/handle_debt_over_due.blade.php`, Excel `HandleDebtOverDueExcel`.
- ERP **không gate vào màn**; quyền `sale.bao_cao_xu_ly_no_qua_han.view` chỉ mở rộng phạm vi.

## 4. Số liệu — giữ y công thức ERP

**Truy vấn trong** (`account_details`, gom theo `contractable_id + contractable_type`):
- `account_id = 22` (giữ đúng ERP — lưu ý khác `CustomerDebtAggregator::ACCOUNT_131_ID = 21`; KHÔNG đổi).
- `contractable_type IN (FirmContract, WrServiceContract)` (chuỗi class ERP), `invoiceable_date_accounting <= Đến ngày`.
- HĐ gốc: `firm.parent_contract_id` (khi `firm.type != 8`) / `wr.parent_id`; KH, NV lập (`created_by`), phòng theo NV lập.
- `begin` = Nợ − Có trước Từ ngày · `debt` = Nợ trong kỳ · `has` = Có trong kỳ.
- `type` = giảm khi `firm.type IN (3,6,10)` hoặc `wr.type = 4`, ngược lại tăng.
- `number_overdue` = DATEDIFF(Đến ngày, COALESCE(firm, wr).payment_overdue_date), `HAVING >= 0`.

**Truy vấn ngoài** (gom theo HĐ gốc + loại): cộng có dấu theo `type`; `number_overdue` chỉ cộng dòng tăng;
`HAVING (begin + debt − has) > 0 AND number_overdue > 0`; sắp `department_id desc`.

**Dòng khai công nợ đầu kỳ** (`declare_debt_beginning`, `is_overdue = 1`, `acceptance_handover_date < Đến ngày`):
`begin` = `dept_value` (âm nếu `type_dept = 2`), `number_overdue` = số ngày từ `acceptance_handover_date` tới Đến ngày,
quy về NV lập HĐ; bỏ HĐ đã có ở nguồn chính (khoá `id-type`). Gộp rồi sắp lại theo phòng.

Khác ERP có chủ đích (chỉ kỹ thuật, không đổi số): ngày truyền qua binding (ERP ghép chuỗi → lỗ SQL injection);
phạm vi quyền áp cho CẢ dòng lẫn dòng tổng.

## 5. Hai cột mới (chỉ ở dòng HĐ)

| Cột | Nguồn | Ghi chú |
|---|---|---|
| **Ngày BGNT** | `handover_date` của **HĐ gốc** (`firm_contracts` / `wr_service_contracts`). Dòng khai đầu kỳ: `acceptance_handover_date`. | ERP tính `payment_overdue_date = handover_date + over_date` (`FirmContract::updateHandoverDate`, seeder `UpdateHandoverDate`). Hiển thị `dd/mm/yyyy`; null → trống. |
| **Quy chế** (ngày) | `over_date` của **HĐ gốc** — số ngày `to_day` của mốc `receive_percent = 100` trong `conditions_commissions` của quy chế, chốt lúc duyệt HĐ (`FirmSupportAccountingService` dòng ~155). Dòng khai đầu kỳ: trống. | Số nguyên; null/0 → trống. |

Dòng Phòng / NV / KH và dòng TỔNG CỘNG: 2 ô này để trống. Có ở cả màn, bản in và Excel.

## 6. Phân quyền

- Dùng lại mã ERP **`sale.bao_cao_xu_ly_no_qua_han.view`**: Catalog `app/Support/Permissions/Catalog/sale.php` thêm `'hrm'`
  vào `platforms` → `php artisan permission:catalog-sync`. Không tạo mã mới.
- **Không gate vào màn.** Phạm vi qua `Modules\Finance\Services\CustomerDebt\CustomerDebtScope` (đã dùng cho các báo cáo
  công nợ KH): Tổng công ty = tất cả · Công ty · Phòng ban · Bộ phận · không quyền = chỉ HĐ mình lập (mọi cấp OR thêm HĐ mình lập).
  Cột NV lập để lọc phạm vi = `created_by` của HĐ (con), cột công ty/phòng/bộ phận như ERP.

## 7. Màn hình (FE `pages/sale/customer-debt-overdue`)

- Menu: `components/subsystem-menu/sale-hub.js`, nhóm "Báo cáo công nợ", thay mục chữ trơn `'Công nợ quá hạn'`
  bằng link `{ n: 'Công nợ KH quá hạn', link: '/sale/customer-debt-overdue' }`.
- Bộ lọc (như ERP): Công ty / Phòng ban / Bộ phận / Nhân viên (`V2BaseCompanyDepartmentFilter` như các báo cáo công nợ KH khác),
  Từ ngày – Đến ngày (bắt buộc), Báo cáo theo (Q2), Khách hàng (search server-side), Hợp đồng (gõ mã, like trên mã HĐ gốc).
- Nút: Lọc, Làm mới, In, Xuất Excel (theo `button-convention`, `report-styles`).
- Bảng:
  - Kiểu 1 (Phòng → NV → KH → HĐ): STT · Tên · **Ngày BGNT** · **Quy chế** · Giá trị HĐ thực tế · Số dư quá hạn đầu kỳ ·
    Phát sinh tăng · Phát sinh giảm (hiện −has) · Số dư quá hạn cuối kỳ (begin+debt−has) · Số ngày quá hạn.
  - Kiểu 2 (KH → HĐ): như trên + cột Nhân viên sau Hợp đồng.
  - Dòng TỔNG CỘNG ở đầu (tổng toàn bộ theo lọc), phân trang theo dòng HĐ, mã HĐ là link (HĐ hãng/DV → màn HRM tương ứng
    nếu có, không có thì link ERP tab mới — copy cách `MonitorContractTable.vue`).
- Số `en-US`, ô 0 hiện `-`; ngày `dd/mm/yyyy`.
- In: màn `print.vue` khổ ngang theo `print-page` skill. Excel: dựng ở FE bằng ExcelJS, ô số thật + `'#,##0;-#,##0;""'`
  (khuôn `pages/sale/monitor-contract-implement/components/export-excel.js`).

## 8. BE (`Modules/Finance`, prefix `finance/customer-debt-overdue`)

- `GET /` (dữ liệu trang + tổng), `GET /export-rows` (dòng phẳng phân trang cho Excel/In), `GET /meta` nếu cần option.
- Service mới `Modules/Finance/Services/CustomerDebt/CustomerDebtOverdueReportService.php`; controller
  `Modules/Finance/Http/Controllers/V1/CustomerDebtOverdueController.php`. Chỉ đọc.

## 9. Ngoài phạm vi

- Chỉ tiêu 1 "Xét theo HĐ" và ô chọn chỉ tiêu (anh Nam).
- Sửa ERP. Đổi công thức tiền/ngày quá hạn so với ERP.

## 10. Để builder tự quyết

- Chia file component, tên biến; cách cache tổng; khuôn popup (không có popup chi tiết ở ERP — không thêm).
- Đối chiếu: chạy cùng bộ lọc trên ERP và HRM (DB chung) — số tiền, số ngày quá hạn, số dòng phải khớp 100%.

## 11. Đối chiếu ERP ↔ HRM (19/11/2026, DB `erp_hrm_check`)

Chạy `HandleDebtOverDueService::getData()` của ERP (toàn hệ thống) và `CustomerDebtOverdueReportService::rows()` của HRM (phạm vi Tổng công ty) với cùng bộ lọc, so theo khoá `loại-id HĐ`:

| Kỳ | ERP | HRM | Chỉ ERP | Chỉ HRM | Lệch (đầu kỳ · tăng · giảm · số ngày QH · giá trị HĐ · mã HĐ · NV · KH) |
|---|---|---|---|---|---|
| 01/10 → 31/10/2026 | 2,210 | 2,210 | 0 | 0 | 0 |
| 01/01 → 19/11/2026 | 2,210 | 2,210 | 0 | 0 | 0 |

→ Khớp 100%. Ngày BGNT / Quy chế là cột mới (ERP không có) nên chỉ kiểm bằng test.
