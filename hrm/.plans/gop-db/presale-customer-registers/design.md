# Design — Danh sách đăng ký khách hàng toàn công ty

> Phụ trách: @junfoke · Tạo 2026-10-08 · nhánh `develop`

## Mục tiêu

Port màn ERP `customerRegister.index` (Kinh doanh › Báo cáo thị trường) sang CSKH trước bán › Báo cáo thị trường
(`/assign/report/customer-registers`). Danh sách CHỈ ĐỌC bảng ERP `customer_registers` (đăng ký sinh từ nút
"Đăng ký khách hàng" của báo giá hãng bên ERP).

## Quyết định (user 2026-10-08)

| Vấn đề | Chốt |
|---|---|
| Menu | CSKH trước bán › Báo cáo thị trường (`presale.js`) |
| Quyền | Dùng lại quyền HRM có sẵn 1526 `Xem danh sách khách hàng đã đăng ký` — gate route + menu, có quyền là xem toàn công ty (y ERP) |
| Màn cá nhân (`forEmployee`, nút Hủy đăng ký) | Chưa làm |
| Còn hạn / Hết hạn | So theo NGÀY: hết hạn hôm nay vẫn "Còn hạn" (ERP so giờ hiện tại); khớp `CustomerOwnership` |

## Khác ERP

- Thêm theo chuẩn HRM: ô tìm nhanh (KH, người liên hệ, người đăng ký, số báo giá), sắp xếp Ngày đăng ký / Thời hạn,
  Cấu hình cột, Xuất Excel chọn trường (ERP không có).
- Số báo giá: báo giá thường mở màn HRM `/assign/quotations/{id}`; báo giá hãng mở ERP (ERP tự kiểm quyền xem báo giá
  khi mở — ERP màn danh sách chỉ hiện link khi có quyền).

## Code

- BE `Modules/Assign/Services/Report/CustomerRegisterService.php`, `Http/Controllers/Api/V1/CustomerRegisterController.php`,
  `Transformers/CustomerRegisterResource/`, route `/assign/report/customer-registers` (+ `/export`),
  `ExportColumnRegistry::COLUMNS['customer_registers']`
- FE `pages/assign/report/customer-registers/index.vue`, menu `components/subsystem-menu/presale.js`

## Giai đoạn 2 — Bổ sung luồng đăng ký / đổi thời hạn / gia hạn (phản hồi QA 23/11/2026, không có task Redmine)

Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-11-26-dang-ky-khach-hang-bo-sung-design.md` — CHỜ USER DUYỆT.

- Phương án A (user chọn 23/11): bảng ERP `customer_registers` giữ nguyên, ERP không sửa; HRM thêm bảng phiếu yêu cầu /
  liên kết nguồn / lịch sử; chỉ ghi bảng chung khi đăng ký có hiệu lực (thời hạn mặc định) hoặc phiếu đã BGĐ duyệt.
- Đăng ký từ báo giá HRM (Đã duyệt + Trúng thầu; KH tổ chức bắt buộc chọn người liên hệ) và dự án TKT.
- Thời hạn khác mặc định / gia hạn ⇒ phiếu duyệt TP → BGĐ (khuôn gia hạn dự án TKT).
- Cấu hình mới "Thông báo hết hạn đăng ký khách hàng" (mặc định 3 ngày) — người đăng ký nhận.
- Màn danh sách: 2 tab Đăng ký / Phiếu yêu cầu, In, Excel, Lịch sử; không quyền Xem ⇒ chỉ thấy đăng ký của mình.
