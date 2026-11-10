# Công nợ khách hàng — 2 màn ERP nhóm Kế toán công nợ › Khách hàng

Nhánh `feat/cong-no-khach-hang` (hrm-api + hrm-client, tách từ `gop_db` 10/11/2026). Làm từng màn (user chốt 10/11/2026).

| # | Màn | ERP | HRM | Spec |
|---|-----|-----|-----|------|
| 1 | Sổ chi tiết công nợ phải thu khách hàng | `account_details?type=customer` | `/finance/customer-ledger-details` | `docs/superpowers/specs/gop-db/2026-11-10-so-chi-tiet-cong-no-kh-design.md` |
| 2 | Bảng cân đối phát sinh công nợ khách hàng | `account_details/balance-debt` | `/finance/customer-debt-balances` | `docs/superpowers/specs/gop-db/2026-11-10-bang-can-doi-cong-no-kh-design.md` |

## Quyết định user (10/11/2026)

1. Sổ chi tiết KH lọc theo Loại tiền như NCC (màn / Excel / In cùng số; khác màn ERP ở KH có bút toán ngoại tệ).
2. Khách hàng chỉ lọc `ad.customer_id` (y màn ERP) — để Bảng cân đối bấm sang Sổ chi tiết khớp số.
3. Tách lớp cha dùng chung cho bảng cân đối (Bảng cân đối NV chuyển sang dùng) — làm ở màn 2.
4. Được sửa Catalog quyền dùng chung (`app/Support/Permissions/Catalog/accounting.php`) thêm `hrm`.

## Khung code

- `Services/AccountDebt/AccountLedgerService` (khung sổ chi tiết) ← `PartnerLedgerService` (đối tác KH / NCC, tách 10/11 từ
  NCC) ← `SupplierDebtDetailService`, `CustomerDebt\CustomerLedgerDetailService`.
- `Services/AccountDebt/AccountBalanceService` (khung bảng cân đối, tách 10/11 từ NV) ← `EmployeeDebtBalanceService`,
  `CustomerDebt\CustomerDebtBalanceService`.
- Màn KH kiểm quyền theo MÃ (`CurrentPermission::scope`), menu `codes`; 3 màn cũ (NV, NCC) vẫn theo tên cũ qua alias.
