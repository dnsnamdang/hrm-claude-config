# Bảng kê chứng từ theo Mã phí — Tóm tắt

> Spec đầy đủ: `docs/superpowers/specs/2026-07-21-bang-ke-chung-tu-ma-phi-design.md`
> Nhánh: `tpe-develop-accounting` (hrm-api + hrm-client). Phụ trách: @namdangit.

## Mục tiêu
Báo cáo kế toán mới: liệt kê dòng `account_details` **có Mã phí** (`cost_debt_id ≠ null`) trong kỳ, **nhóm theo Mã phí**, đủ 2 vế Nợ/Có, tổng nhóm + tổng cộng cân đối. Đọc ERP qua `mysql2`. Tái dùng base `AccountDetailBaseService` của Sổ NKC.

## Quyết định lớn
- **TK đối ứng** ← `account_detail_refs` (giống print Sổ NKC).
- **Bộ lọc đơn vị**: cascade 4 cấp Cty→PB→BP→NV (dùng lại `AccountingOrgCascade`).
- **Phân quyền**: 1 quyền riêng `Xem bảng kê chứng từ theo mã phí`, không phân cấp.
- **Mẫu báo cáo**: cả Chuẩn + Ngoại tệ.
- **Cột "Mã ct"**: bỏ; chỉ giữ "Số ct" = `invoiceable_code`.
- **Số CT NKC**: text, chưa link.
- **Diễn giải**: `accounting_note` (fallback `service_name`).
- **Lọc Mã phí**: chọn 1.
- PS Nợ/Có (chuẩn) = `money_value_exchange` (VND); PS Nợ nt/Có nt = `money_value`.

## Base dùng chung (mở rộng, không phá Sổ NKC)
1. `applyFilter()` thêm nhánh `type` (ghi nợ/có) + `account_ref_ids` (lọc TK đối ứng).
2. Base hoá subquery TK đối ứng → `AccountDetailBaseService::accountRefSubSql()` (Sổ NKC print đổi sang dùng chung).
3. `CostVoucherService` mới: nhóm theo mã phí + tổng nhóm (`getGroupTotals`) + tổng cộng (`getGrandTotals`).

## Cấu trúc code
**BE (Module Accounting):** mở rộng `AccountDetailBaseService`, thêm `CostVoucherService` + `CostVoucherController` + route + permission seeder. Cascade dùng lại `AccountingOrgController`.
**FE (`pages/accounting/cost-vouchers/`):** clone `general-journal/` — index.vue (filter panel + cascade + row-group table + tổng trong card), `cost-voucher-columns.js`, `CostVoucherColumnConfigModal.vue`, `store/accounting/cost-voucher.js`, `print.vue` (layout Fast + chữ ký), menu.

## Trạng thái
DESIGN DONE + duyệt (2026-07-21). Bước tiếp: writing-plans → plan chi tiết.
