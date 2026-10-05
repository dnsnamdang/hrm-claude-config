# Dữ liệu tạo cho SRS Báo giá (local DB local_hrm_erp, 05/10/2026)

Tạo qua API :8003 bằng tài khoản admin (employees.id 13 — Sale phụ trách dự án 154), script `make_data.py`.
Dự án dùng chung: prospective_projects.id 154 (CTV_NV.UD.0101.2026.DA002 — Thần Châu Garage), báo giá tự lập.

| quotations.id | Mã | Trạng thái cuối | Ghi chú |
|---|---|---|---|
| 92 | BG-2026-00092 | Đang tạo | Bản nháp; shoot đã Lưu lại khi chụp Gửi duyệt → giá nhập vận chuyển = 40,000,000 (để ra C3) |
| 93 | BG-2026-00093 | Đang tạo (bị từ chối) | Gửi duyệt C2 rồi Từ chối, lý do "Giá kích cá sấu thấp hơn mức sàn…" |
| 94 | BG-2026-00094 | Chờ TP duyệt (C3) | |
| 95 | BG-2026-00095 | Chờ BGĐ duyệt (C3) | TP đã duyệt & chuyển BGĐ |
| 96 | BG-2026-00096 | Đã duyệt (C1 tự duyệt) | Có Ghi chú kinh doanh |
| 97 | BG-2026-00097 | Trúng thầu | Chốt kèm file xác nhận (bảng files, table=quotations) |
| 98 | BG-2026-00098 | Chờ TP duyệt (C2) | |

Kèm theo: quotation_groups 2 nhóm/báo giá, quotation_product_prices (6 dòng/báo giá, hàng tạm mã HHBG0018xx),
quotation_service_items (2 dòng/báo giá), quotation_histories, thông báo duyệt.

Hiệu ứng phụ do nghiệp vụ tự cascade (không sửa tay): dự án 154 bị đổi tiến trình sang "Thương thảo giá" (tự
duyệt 96) rồi "Thương thảo dự án/hợp đồng" (chốt 97). ID 99–… có thể bị "tiêu" bởi preview-submit (rollback).
