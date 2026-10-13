# Hệ số công nghệ theo nhóm hàng hóa — chuyển từ ERP sang HRM

Người phụ trách: @khoipv · Nhánh: `develop` (checkout từ `gop_db`, cả 2 repo) · Bắt đầu: 13/10/2026
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-10-13-benefit-rates-design.md`

## Mục tiêu
Port màn ERP `benefit_rates.index` (QTTT › Cấu hình ERP › "Hệ số công nghệ theo nhóm hàng hóa") sang HRM,
đặt ở phân hệ **Quản trị hệ thống**, ngay dưới "Danh sách loại phiếu hạch toán" (cùng nhóm bên ERP).

## Quyết định đã chốt (user 13/10/2026)
| Vấn đề | Chốt |
|---|---|
| Menu | Quản trị hệ thống, cạnh "Danh sách loại phiếu hạch toán" |
| Quyền | **Không gate** như ERP — không tạo quyền mới, không middleware `checkPermission` |
| Phạm vi | **Như ERP**: mọi người chỉ thấy/sửa bản ghi thuộc công ty của mình (`company_id` người đăng nhập) |
| Xoá / Khoá | **Như ERP**: xoá hẳn không điều kiện (không bảng nào trỏ id tới `benefit_rates` — phiếu chỉ chép SỐ hệ số); không thêm cột Trạng thái / Khoá |

## Phạm vi
- Bảng ERP sẵn có trên DB gộp: `benefit_rates` + `benefit_rate_has_group_products` — **không migration**.
- Màn danh sách + popup Thêm / Sửa / Xem (giống ERP dùng popup), Xuất Excel, Cấu hình cột, Lịch sử
  (bộ bắt buộc của HRM). Không Import (ERP không có).
- KHÔNG đụng màn cũ `/assign/settings/benefit_rate` (bảng khác `assign_benefit_rate_configs`, đã ẩn menu).

## Nghiệp vụ (lấy từ ERP)
- Trường: Loại hệ số* (không trùng trong công ty) · Hệ số* (số, 2 số lẻ, decimal(8,2)) ·
  Nhóm hàng hóa áp dụng* (chọn nhiều; **mỗi nhóm chỉ thuộc 1 loại hệ số** — ERP kiểm toàn bảng,
  không theo công ty, giữ nguyên vì `getCoefficientOfProduct()` của ERP tra theo nhóm toàn cục).
- Ghi như ERP: `company_id/department_id/part_id` = của người tạo; `created_by/updated_by` NOT NULL.
- Lọc ERP: Loại hệ số · Người tạo · Người sửa (+ Công ty — bỏ, xem spec §Lọc).
