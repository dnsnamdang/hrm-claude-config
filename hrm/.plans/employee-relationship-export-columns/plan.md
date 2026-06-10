# Plan — Chọn cột khi xuất Excel màn employee-relationships

Người phụ trách: @khoipv
Ngày tạo: 2026-06-09

## Phase 1 — FE chọn cột khi xuất Excel

### Backend
- [x] Không cần sửa — controller `EmployeeController::exportEmployeeRelationships` đã nhận `visible_fields[]`, blade `employee_relationship_report.blade.php` đã render đủ 14 cột tuỳ chọn.

### Frontend
- [x] T1. Tạo component `pages/human/employee-relationships/components/ExportRelationshipModal.vue` — modal chọn cột (Select2 multi + checkbox "Chọn tất cả"), mirror pattern `components/modal/export-list-employee-modal.vue`. Options lấy từ prop `fields` (14 cột trong "Tuỳ chỉnh cột"). Bắt đầu trống. Bấm "Xuất excel" → emit `export` kèm mảng key đã chọn rồi đóng modal.
- [x] T2. `pages/human/employee-relationships/index.vue` — đổi nút "Xuất excel": bỏ `@click="exportEx()"` → mở modal (`$bvModal.show('modal-export-relationship')`).
- [x] T3. `index.vue` — import + đăng ký + render `<ExportRelationshipModal :fields="fields" @export="exportEx" />`.
- [x] T4. `index.vue` — sửa `exportEx(selectedKeys)` để dùng `selectedKeys` (từ modal) thay cho `this.visibleFields` của bảng (decouple export khỏi cột bảng).
- [ ] T5. Verify browser: mở modal → chọn vài cột → xuất ra file có đúng cột; không chọn cột nào vẫn xuất được 6 cột cố định; filter (công ty/phòng/quan hệ/ngày sinh) vẫn áp đúng vào file.

## Checkpoint
(điền khi wrap up)
