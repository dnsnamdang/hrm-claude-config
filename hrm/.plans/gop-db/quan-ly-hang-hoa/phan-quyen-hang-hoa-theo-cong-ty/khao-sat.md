# Phase 3 — "Phân quyền hàng hoá theo công ty" — khảo sát 13/10/2026 (chỉ đọc)

> A7. Kết luận: nội dung gốc của Phase 3 **đã được hấp thụ hết** vào các đợt sau — không còn việc code riêng.

## Phase 3 gốc nghĩa là gì
Không phải "phân quyền" hẹp, mà là **dữ liệu hàng hoá theo công ty**: tab 5 (Dữ liệu quản trị) + tab 6 (Giá bán) "theo từng công ty"
được tách khỏi Phase 2 ngày 21/09 (`man-danh-muc-hang-hoa/design.md` §2, lý do ERP đọc giá / tồn tối thiểu ở 119 + 33 + 42 file), cộng câu
"`products.company_id` quản thế nào sau khi bỏ lan truyền từ Hãng SX" (`chuyen-danh-muc-lien-quan/plan.md:2928`).

## Đã làm ở đâu
| Hạng mục Phase 3 gốc | Đã làm | Mốc |
|---|---|---|
| Tab Quản trị theo công ty (công ty nào khai của công ty đó) | §23 "Đảo lại §2" (user) ⇒ 2-A nền `product_company_coefficients` + 4 ô quản trị, `product_suppliers.company_id`, `product_business_catalogs` theo công ty; 2-C form + tab Quản trị theo công ty đang làm việc; công ty lấy về chỉ sửa tab Quản trị | 2-A, 2-C1/2-C2 |
| Quyền theo CÔNG TY ĐANG LÀM VIỆC (không phải công ty bất kỳ) | R22: 1652 / 1653 / 1655 / giá 1657–1658 kiểm `isCurrentEmployeeHasPermission` theo `current_company_role` | 2-C, Phase 8 |
| Trạng thái hàng theo công ty (Nhập thông tin · Chờ/Đang tính giá · Đang KD · Ngừng KD · hàng tạm) | `pcc.status` 1–8, các màn lọc theo công ty, khoá / mở khoá theo công ty | 2-B, 2-C4, P6, P7 |
| Giá bán / giá vốn theo công ty | Phase 8 G1–G6 (bộ giá + giá vốn theo công ty, duyệt giá theo công ty) + luồng tính giá P7 | `gia-theo-cong-ty/` |
| ERP đọc giá theo công ty | G3 (`DocumentCompany`, `ProductPriceService`) | G3 |
| ERP đọc bảo hành / tồn tối thiểu theo công ty | C-e (N1) | `ngoai-luong/ce-plan.md` |
| `products.company_id` sau khi bỏ lan truyền từ Hãng SX | = **công ty tạo hàng** (chủ), gán lúc tạo ở HRM, không đổi; ERP `ManufacturesController` thôi ghi lan (2-D1 N2) | 2-C1, 2-D1 |
| Danh mục phân loại (Phase 0) | Chốt từ đầu: dùng chung toàn hệ thống, KHÔNG theo công ty | Phase 0 |

## Còn lại — đều đã có chỗ ghi, không thuộc Phase 3 mới
- A6 Báo cáo hàng hoá theo công ty (ma trận mã × công ty) — ⏸ user để sau (04/10).
- A5 Bỏ hẳn hệ số giá theo công ty cũ — ⏸ user "chuyển sau" (09/10).
- N90 Báo cáo CSKH + Tổng hợp bán hàng đọc bảo hành cột chung — user tính sau (C-e-2).
- N91 Luật đọc HRM `AdminData::source` với dòng hệ số cũ status NULL lệch ERP (23 dòng).

## Đề xuất
Đóng Phase 3 = "đã hấp thụ vào 2-A/2-C/Phase 8/C-e", không mở nhánh, không code.
