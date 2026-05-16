# Design — Tách cột Excel xuất Ứng dụng

**Ngày:** 2026-04-16 | **Phụ trách:** @manhcuong
**Spec chi tiết:** [docs/superpowers/specs/2026-04-16-application-export-split-columns-design.md](../../docs/superpowers/specs/2026-04-16-application-export-split-columns-design.md)

## Mục tiêu

Thay đổi cấu trúc file Excel xuất từ màn `/assign/application` — từ 7 cột (2 cột gộp nhiều thông tin) sang **12 cột**, mỗi field 1 cột riêng biệt.

## Scope

- Sửa blade template + check export class + eager-load
- Không đụng DB, API, filter, Service query logic
- Không ảnh hưởng màn danh sách / form detail

## 12 cột mới

STT → Mã ứng dụng → Tên ứng dụng → Mô tả → Nhóm ngành → Nhóm giải pháp → Lĩnh vực khách hàng → Trạng thái → Người tạo → Ngày tạo → Người cập nhật → Ngày cập nhật

## Quyết định chính

- **Giữ file `.xls`** và tên `danh_sach_ung_dung.xls` (không đổi)
- **Nhóm ngành/giải pháp/lĩnh vực KH (M2M)**: nối chuỗi bằng `, ` trong 1 ô
- **Ngày**: format `DD/MM/YYYY` (không có giờ)
- **Trạng thái**: hiển thị text (`Hoạt động` / `Khóa`)
- **Filter export**: giữ nguyên tất cả filter hiện tại

## File sửa

1. `hrm-api/resources/views/exports/applications.blade.php` — viết lại header + body
2. `hrm-api/app/ExcelExport/ApplicationsExport.php` — check data truyền vào blade
3. `hrm-api/Modules/Assign/Services/ApplicationService.php` — check eager-load
4. `hrm-api/Modules/Assign/Http/Controllers/Api/V1/ApplicationsController.php` — check method `export()`

## Ước lượng

~1 giờ (30p code + 30p test)
