# Export ảnh nhân viên vào Excel — Tóm tắt

**Feature:** export-anh-nhan-vien-excel · **@namdangit** · 2026-07-01
**Spec chi tiết:** `docs/superpowers/specs/2026-07-01-export-anh-nhan-vien-excel-design.md`

## Mục tiêu
Nhúng ảnh chân dung nhân viên vào file Excel xuất từ màn `/human/employee_info` (hiện chỉ có text).

## Quyết định chốt
- Đổi định dạng file `.xls` → `.xlsx` (bắt buộc để nhúng ảnh).
- Cột "Ảnh" cố định đầu bảng (không theo checkbox chọn trường).
- Xử lý đồng bộ, chấp nhận chậm khi danh sách lớn.

## Cách làm (tóm tắt)
- **Controller** `getEmployeeByField`: thêm `image` vào `$result`, đổi tên file `.xlsx`, tăng time/memory limit.
- **Blade** `employee_info_report`: thêm cột "Ảnh" (header + cell rỗng) đầu bảng, sửa `colspan +2`.
- **Export class** `EmployeeInfoExport`: implement `WithDrawings` + `WithColumnWidths` + `WithEvents`; `drawings()` tải ảnh (MemoryDrawing) neo vào ô `A{3+index}`; ảnh lỗi/thiếu → bỏ qua.
- **FE** `export-list-employee-modal.vue`: đổi tên file tải xuống sang `.xlsx`.

## Cần verify khi implement
`WithDrawings`+`FromView` neo đúng ô; GD extension; định dạng `image` (URL vs S3 path).

## Ngoài phạm vi
`EmployeeResignedExport`, permission, queue job.
