# Plan — Bảng kê chứng từ theo Mã phí

> Plan chi tiết (task bite-sized): `docs/superpowers/plans/2026-07-21-bang-ke-chung-tu-ma-phi.md`
> Spec: `docs/superpowers/specs/2026-07-21-bang-ke-chung-tu-ma-phi-design.md`
> Nhánh: `tpe-develop-accounting` (hrm-api + hrm-client)

## Phase 1 — Backend base + service

- [x] Task 1: Mở rộng `AccountDetailBaseService::applyFilter()` — filter `type` (ghi nợ/có) + `account_ref_ids` (TK đối ứng) — commit bfd6a5347
- [x] Task 2: Base-hoá subquery TK đối ứng → `accountRefSubSql()`; Sổ NKC print dùng lại — commit 05a9e2847
- [x] Task 3: `CostVoucherService` — query CÓ mã phí (`cost_debt_id>0`) + nhóm mã phí + `getGroupTotals`/`getGrandTotals`/`getPrintData` — commit eac7ff58f (+cleanup 3d9fa6104)

## Phase 2 — Backend API

- [x] Task 4: `CostVoucherController` (index/print/export) + route + permission `Xem bảng kê chứng từ theo mã phí` (id 1108) — commit 42e9b3a32
- [x] Task 5: Excel export `CostVoucherExport` (std/fx) + view cost_voucher.blade — commit 2f72d7bbd
- [x] Task 5b (phát sinh): endpoint `accounting/cost-debts` (Mã phí remote select) — commit acbded47f

## Phase 3 — Frontend

- [x] Task 6: `cost-voucher-columns.js` + `store/accounting/cost-voucher.js` — commit 8e45b76f1
- [x] Task 7: `pages/accounting/cost-vouchers/index.vue` (filter + cascade + row-group hand-rolled + tổng 2 cột độc lập + In/Excel) — commit 68e6cf0b2 (+7b Mã phí remote 62bdfc26e)
- [x] Task 8: `CostVoucherColumnConfigModal.vue` (cấu hình cột) — commit 195b79b24
- [x] Task 9: `pages/accounting/cost-vouchers/print.vue` (In Fast + chữ ký) — commit 6105aa699
- [x] Task 10: Menu phân hệ Kế toán (menu-sidebar.js) — commit 1e0d77c7e

## Checkpoint cuối
- [x] Final whole-branch review (BE+FE, opus) → READY TO MERGE + fix Important (header nhóm đếm full-set: hrm-api a0b96be67 / hrm-client ecd0a1ab5)
- [ ] User: quyết các Minor còn lại (export theo cột hiển thị? format số? fx trong print/excel?)
- [ ] User: gán quyền `Xem bảng kê chứng từ theo mã phí` + browser smoke-test (lọc, nhóm, mẫu FX, In, Excel)
- [ ] User: push + tạo PR (chưa push)

---

### Checkpoint — 2026-07-21 (hoàn tất build)
Vừa hoàn thành: TOÀN BỘ 10 task (+5b, +7b) qua subagent-driven, mỗi task task-reviewed + final whole-branch review (opus) = READY TO MERGE. Đã fix 1 Important (header nhóm đếm full-set).
Đang làm dở: (không) — code xong, chưa push.
HEAD cuối: hrm-api a0b96be67 | hrm-client ecd0a1ab5 (nhánh tpe-develop-accounting).
Bước tiếp theo: user quyết vài Minor (export/format) → gán quyền + browser test → push + PR.
Blocked:
