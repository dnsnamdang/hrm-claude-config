# Design — 3 báo cáo công nợ khách hàng

> Phụ trách: @junfoke · Tạo 2026-10-06 · nhánh `develop`
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-10-06-sale-customer-debt-reports-design.md`

## Mục tiêu

Port 3 báo cáo công nợ KH của ERP sang hub Bán hàng › Báo cáo công nợ, dùng chung 1 hàm tính công nợ. Chỉ đọc.

## Quyết định chính (user 2026-10-06)

| Vấn đề | Chốt |
|---|---|
| Quyền | 4 cấp/màn y ERP (12 quyền 1683-1694, type 23); ai cũng vào, không quyền → HĐ của mình |
| Số liệu | Giữ y ERP, chỉ sửa lỗi bảo mật |
| Excel | Chuẩn HRM; màn Theo NV giữ thêm mẫu in |
| Thứ tự | Hàm chung + Chi tiết → Theo NV → Đối chiếu |

## Code

- BE `Modules/Finance/Services/CustomerDebt/`:
  - dùng chung: `CustomerDebtAggregator` (công thức), `CustomerDebtScope` (4 cấp), `AbstractCustomerDebtReportService` (lọc, dư đầu kỳ);
  - 3 màn: `CustomerDebtDetailReportService`, `CustomerDebtByEmployeeReportService`, `CustomerDebtCompareReportService`;
  - controller `Http/Controllers/V1/CustomerDebt{Detail,ByEmployee,Compare}Controller.php`;
  - route `/v1/finance/customer-debt-{details,by-employee,compare}`.
- FE:
  - `pages/sale/customer-debt-{details,by-employee,compare}/`;
  - `utils/invoiceable-link.js`, `utils/finance/customerDebtContractLink.js`;
  - menu `sale-hub.js` › Báo cáo công nợ.
