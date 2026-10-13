### Task 10: Chuyển `ProjectListModal` (server-side → CHỈ vỏ, không mixin)

**Files:** Modify `pages/assign/report/prospective-project-results/components/ProjectListModal.vue`

- [ ] **Step 1:** Thay vỏ bằng `V2BaseReportModal`. **KHÔNG gắn mixin** — popup tự `fetchList()`, lọc/sắp/phân trang đều ở BE.
- [ ] **Step 2:** Truyền `current-page` / `current-page-size` / `total-rows` từ response API; `@page-change`/`@page-size-change` gọi lại `fetchList()`.
- [ ] **Step 3:** Adapter cột: `columnDefs` map `align → cellClass`.
- [ ] **Step 4:** `@sort` nối vào cơ chế sắp xếp BE sẵn có (không dùng sort client của mixin).
- [ ] **Step 5:** Đổi tiền tố `tkt-drill-*` → `report-drill-*`, xoá lớp trùng với Base.
- [ ] **Step 6:** Bảng đối chiếu class khai/dùng — rỗng.
- [ ] **Step 7:** So với `baseline-tkt.json`.

