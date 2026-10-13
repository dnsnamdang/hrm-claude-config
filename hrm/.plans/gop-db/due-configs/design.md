# Cấu hình chặn luồng hàng quá hạn — chuyển từ ERP sang HRM

Người phụ trách: @khoipv · Nhánh: `develop` (checkout từ `gop_db`, cả 2 repo) · Bắt đầu: 13/10/2026
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-10-13-due-configs-design.md`

## Mục tiêu
Port màn ERP `due_configs.edit` (QTTT › Cấu hình ERP › "Cấu hình chặn luồng hàng quá hạn") sang HRM, phân hệ
**Quản trị hệ thống**, cạnh "Hệ số công nghệ theo nhóm hàng hóa". Màn chỉ là nơi BẬT/TẮT cấu hình; phần
chặn thật đã có sẵn ở `Modules/Finance/Services/DueConfigBlockService.php` (đọc cùng bảng) — không đổi.

## Quyết định đã chốt (user 13/10/2026)
| Vấn đề | Chốt |
|---|---|
| Menu | Quản trị hệ thống, ngay dưới "Hệ số công nghệ theo nhóm hàng hóa" — `/admin/due-configs` |
| Quyền | Tạo quyền MỚI `Cấu hình chặn luồng hàng quá hạn` (guard api, type 10, id 1706), gate cả xem + lưu. ERP gate bằng `Cấu hình hệ thống` |
| Lịch sử | Chuẩn HRM `catalog_histories` + khối `SystemInfoSection`; **chuyển 204 dòng lịch sử ERP cũ** (`due_config_histories`) sang bằng migration dữ liệu |

## Phạm vi
- Bảng ERP sẵn có: `due_configs` (52 mục, tab 1 = chặn nhân viên 21 mục / 3 nhóm, tab 2 = chặn TP duyệt 31 mục),
  `company_due_configs` (pivot công ty × mục, không id). Không migration schema.
- Màn: 2 tab chính (1. Chặn nhân viên · 2. Chặn trưởng phòng duyệt) × tab công ty (công ty `status = 1`, sắp tên).
  Tab 1 chia nhóm thu gọn được, đếm số mục đang tích; tab 2 có "Tích tất cả / Bỏ tích tất cả". Nút Lưu + Quay lại.
- Lịch sử theo TỪNG công ty (`table_name = company_due_configs`, `table_id = company_id`), 2 khoá ảo dạng bảng
  "Danh sách chặn nhân viên" / "Danh sách chặn trưởng phòng duyệt" → hiện "Mục … thêm mới / đã xóa".
