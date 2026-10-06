### Task 11: Cập nhật e2e của 2 màn

**Files:** Modify `e2e/tests/assign/customer-market-development.spec.ts` (19 chỗ `cmd-drill`), `e2e/tests/assign/tkt-result-report.spec.ts` (15 chỗ `tkt-drill`)

- [ ] **Step 1:** Đổi tiền tố bằng script, in số chỗ đã đổi.
- [ ] **Step 2:** **Đối chiếu từng selector `report-drill-*` với class/id thật trong nguồn** — danh sách "không tìm thấy nơi định nghĩa" phải RỖNG. Lớp đã gỡ ở Phase 1 ánh xạ như sau: `*-content` → `.report-drill-dialog .modal-content`, `*-footer` → `.report-drill-dialog .modal-footer`, `*-topscroll` → `.v2-table-scroll__top`.
- [ ] **Step 3:** `--list --no-deps` cho cả 2 spec, phải ra đúng 18 và 10 ca.

