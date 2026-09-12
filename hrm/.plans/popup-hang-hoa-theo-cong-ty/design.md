# Design — Popup chọn hàng hoá theo công ty (Báo giá + Bomlist + ERP)

Redmine #11286 (http://quanly.dnsmedia.vn/issues/11286) — phụ trách @khoipv
Spec chi tiết: `docs/superpowers/specs/2026-09-11-popup-hang-hoa-theo-cong-ty-design.md`

## Mục tiêu

Popup "Chọn hàng hoá" ở 3 nơi (Báo giá HRM, Bomlist HRM, Báo giá ERP):

1. Thêm cột **Nguồn hàng** — `products.company_id` → `companies.code` (TPE, TPSG, TPV…).
2. Thêm cột **Lĩnh vực** + **Chương** — suy từ nhóm hàng qua `product_group_classifies`
   (cột "Loại hàng hoá" đã có sẵn, không sửa).
3. Thêm **bộ lọc theo Công ty** (lọc nguồn hàng).
4. **Giá bán theo công ty** — mỗi mặt hàng chỉ một mức giá, là giá của công ty người đăng nhập.

## Quyết định lớn

- **Không tạo bảng cấu hình danh mục theo công ty.** Lĩnh vực/Chương không có `company_id` trong
  DB ERP; 3 cột lấy thẳng từ dữ liệu hàng hoá (user chốt 11/09).
- **Bộ lọc dùng tham số riêng `source_company_id`**, KHÔNG tái dùng `company_id`. `company_id` bên ERP
  đang mang nghĩa "công ty dùng để tính giá" (join `product_company_coefficients`); dùng chung sẽ làm
  người dùng nhìn thấy giá của công ty khác khi lọc.
- **Gộp nhiều Lĩnh vực/Chương trong một ô** — 68 nhóm hàng có nhiều dòng phân loại.
- **Không đổi schema HRM**, không migration; 3 thông tin mới chỉ hiển thị trong popup, không lưu vào
  dòng báo giá/BOM, không lên bản in và Excel.

## Hiện trạng cần biết

Hai popup chạy hai đường khác nhau:

| Popup | Đường đi | Đã có giá theo công ty? |
|---|---|---|
| Báo giá HRM | gọi API nội bộ ERP `/api/v1/hrm/products/search` → `SearchController::searchProductStockBuyerApi` | **Có sẵn** — ERP nhân hệ số theo `company_id` HRM truyền lên |
| Bomlist HRM | query thẳng DB ERP qua `BomListController::searchErpProducts` | **Chưa** — lấy giá gốc `TpProductUnitPrice::getRetailPrices()` |
| Báo giá ERP | `searchProductStockBuyer` + blade/JS popup | Có sẵn |

Độ phủ dữ liệu (DB `erp_new_11032026`): 98,2% hàng hoá suy được Lĩnh vực/Chương;
`products.company_id` chỉ có 2 giá trị thực tế (TPE 23.435 SP, Sài Gòn 495 SP).

## Rủi ro môi trường

ERP và HRM phải cùng trỏ một DB ERP (hiện cùng `erp_new_11032026`). Dữ liệu báo giá cũ trong
`hrm_production_18072026` nhập từ thời `gop_db` nên `erp_product_id` trỏ sai: 867/1.074 dòng sang
mặt hàng khác, 207 dòng mất id. Khi kiểm thử phải tạo báo giá mới, không mở-rồi-lưu báo giá cũ.
