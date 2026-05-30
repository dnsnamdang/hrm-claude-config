# Plan — Tab Thuế TNCN lưu cả bảng 1 lần

**Spec:** `docs/superpowers/specs/2026-05-26-employee-tax-bulk-save-design.md`
**Plan chi tiết (TDD steps):** `docs/superpowers/plans/2026-05-26-employee-tax-bulk-save.md`

## Phase 1 — Backend

- [ ] Task 1: Tạo `BulkEmployeeTaxRequest` (validate chồng lấn + 2 row open)
- [ ] Task 2: Thêm `bulkSave()` vào `EmployeeTaxService` (transaction)
- [ ] Task 3: Thêm method `bulk()` vào `EmployeeTaxController`
- [ ] Task 4: Đăng ký route `POST /human/employee_tax/bulk`
- [ ] Task 5: Manual test BE (curl) — happy + 2 case validate

## Phase 2 — Frontend

- [ ] Task 6: Refactor `EmployeeTaxTab.vue` (bỏ edit per-row, thêm nút Lưu chung)
- [ ] Task 7: Manual test FE end-to-end (9 case) trên `employee_info/42/edit`

## Phase 3 — Wrap up

- [ ] Task 8: Cập nhật STATUS.md + plan checkpoint
