# Sales Contract (Module 2) — Plan

> Phạm vi: HD-01 (Danh sách) + HD-02 (Tạo/sửa). Plan chi tiết (code đầy đủ): `docs/superpowers/plans/2026-06-08-sales-contract.md`.
> Spec: `docs/superpowers/specs/2026-06-08-sales-contract-design.md`. Phụ trách: @manhcuong.
> KHÔNG commit git. Test: BE `php -l` + smoke in-process; FE compile.

## Phase 0 — Scaffold module `Sale`
- [x] Task 1: module.json + composer.json + Config + 2 Provider + Routes rỗng + `modules_statuses.json` (Sale:true) + dump-autoload → module Enabled

## Phase 1 — Database
- [x] Task 2: 3 migration (sale_contracts, sale_contract_items, sale_contract_payment_terms) + migrate OK

## Phase 2 — Entities
- [x] Task 3: SaleContractItem + SaleContractPaymentTerm
- [x] Task 4: SaleContract (STATUSES, HasStatusBadge, getNextCode→HĐ.00001, isCan*)

## Phase 3 — Request + Service
- [x] Task 5: SaleContractRequest (validate items≥1, tổng %=100, messages)
- [x] Task 6: SaleContractService (index scope công ty + nháp riêng tư, computeItemTotals, sync items/terms, submit/approve/cancel/delete)

## Phase 4 — Resources + Controller + Routes
- [x] Task 7: SaleContractResource (list) + DetailSaleContractResource (status_name/color, is_can_*, items/terms/files)
- [x] Task 8: SaleContractExport (Excel, FromView + blade exports.sale_contracts)
- [x] Task 9: SaleContractController
- [x] Task 10: Routes/api.php (/v1/sale/contracts + submit/approve/cancel) — 10 route đăng ký

## Phase 5 — Permissions
- [x] Task 11: Seeder thêm 1105 Quản lý / 1106 Duyệt / 1107 Xem HĐ bán hàng + insert DB + gán Super admin (role 18)

## Phase 6 — FE Danh sách (HD-01)
- [x] Task 12: pages/sale/contracts/index.vue (list + filter + export + V2BaseBadge) — compile OK
- [x] Task 13: (tiện ích) script compile FE

## Phase 7 — FE Form (HD-02)
- [x] Task 14: ContractForm.vue + create/edit/view wrappers (hạng mục + đợt TT + V2Footer Lưu nháp/Trình duyệt/Duyệt/Huỷ + validate inline) — 4 file compile OK
- [x] Task 15: Menu sale.js + đăng ký layout/default.vue + checkPermission.js (isShow 'Xem hợp đồng bán hàng') + **switcher BasicSubsystem.vue** (ô "Bán hàng" → /sale/contracts — nếu thiếu thì menu mồ côi)

## Phase 8 — Smoke test + checkpoint
- [x] Task 16: BE smoke test in-process — PASS 8/8 (create HĐ.00001 total 2.200.000, show badge/items/terms, submit→approve, chặn xoá HĐ đã duyệt 400, items rỗng 422, %≠100 422, list)
- [x] Task 17: Cập nhật plan.md + STATUS.md + báo chat

## Còn lại (user)
- User test UI trên trình duyệt (tạo/sửa/duyệt/huỷ HĐ, lọc, xuất Excel).
- Commit git (tôi không commit).
- Đợt sau: HD-03 timeline, HD-04 phụ lục, HD-05 báo cáo (khi có module PO/LSX/giao/thu).
