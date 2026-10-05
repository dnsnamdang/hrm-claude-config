### Task 9: Chuyển `DevelopmentDrillModal` (lọc client-side → vỏ + mixin)

**Files:** Modify `pages/assign/report/customer-market-development/components/DevelopmentDrillModal.vue`

- [ ] **Step 1:** Thay vỏ bằng `V2BaseReportModal`; `lead` đặt theo ngữ cảnh màn ("Bạn đang xem phát triển thị trường:"), `meta` ghép từ dòng meta hiện có.
- [ ] **Step 2:** Adapter cột: `columns` computed map `id → key`, `width` số → chuỗi `px`.
- [ ] **Step 3:** Gắn `reportDrillListMixin`; popup này lọc **client-side** nên `onFilterChange()` chỉ cần `this.page = 1`, và `rows` truyền vào Base lấy từ `pagedRows` chạy trên `applyLocalFilters(rows)`.
- [ ] **Step 4:** Giữ nguyên luật riêng: ô lọc theo đối tượng đang xem bị ẩn VÀ bị xoá giá trị (không lọc ngầm).
- [ ] **Step 5:** Đổi toàn bộ tiền tố `cmd-drill-*` → `report-drill-*`; lớp nào trùng tên với lớp Base thì XOÁ khỏi popup (Base lo).
- [ ] **Step 6:** Lập bảng đối chiếu class khai/dùng — phải rỗng.
- [ ] **Step 7:** Chạy `measure-popup.mjs` so với `baseline-cmd.json`; lệch khoá nào ngoài 2 khoá footer đã biết thì sửa code, KHÔNG sửa baseline.

