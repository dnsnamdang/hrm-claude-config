# Design tóm tắt — Trường "Bảng giá" cho Báo giá

> Spec đầy đủ: `docs/superpowers/specs/2026-07-17-baogia-bang-gia-design.md`

## Mục tiêu
Thêm dropdown "Bảng giá" (6 loại ERP) vào form Tạo/Sửa/Xem báo giá `/assign/quotations`. Chọn/đổi bảng giá → tự áp đơn giá BÁN của hàng ERP theo bảng giá, tính lại tổng.

## Bối cảnh
Giá bán ERP = `product_unit_prices.price` theo `price_type_id` (1-6, danh mục `price_types` mysql2). HRM đang hard-code =1 (Bán lẻ). Giá vốn (`product_units.cost_price`) không theo bảng giá. Không có cột "hiệu lực" → giá hiện hành = giá đang lưu.

## 9 quyết định chốt
1. Dropdown Bảng giá bắt buộc, 6 loại từ ERP, mặc định **Bán lẻ**.
2. Đổi bảng giá → **chỉ đổi giá BÁN** hàng ERP; giá vốn giữ nguyên.
3. Giữ GG user nhập tay + giá hàng tạm; chỉ re-price dòng ERP; tính lại tổng.
4. Không có giá ở bảng giá đã chọn → đơn giá = 0.
5. Chỉ đổi được khi **Đang tạo** (khoá sau gửi duyệt).
6. Mở Sửa → tự lấy giá ERP mới nhất theo bảng giá (AC4).
7. Xem chi tiết → hiển thị bảng giá đã áp.
8. Đồng bộ ngược ERP gửi đúng price_type_id.
9. Báo giá cũ (null) → coi như Bán lẻ.

## Thay đổi chính
- **DB**: 1 migration `quotations.price_type_id`.
- **BE**: `TpProductUnitPrice` tham số hoá `priceTypeId` (default 1); `ErpProductSearchService` search theo price_type; `QuotationService` áp giá + endpoint `/reprice`; `QuotationErpSyncService` gửi đúng price_type; Resource trả price_type_name; endpoint `/price-types`; validation.
- **FE**: `edit.vue` dropdown Bảng giá + `handleChangePriceType` (re-price) + loadDetail re-price khi mở Sửa; màn Xem hiển thị.

## AC
AC1 dropdown 6 loại · AC2 áp giá Bán lẻ · AC3 đổi Đại lý → giá đổi + tính lại · AC4 mở Sửa lấy giá mới ERP · AC5 Xem hiển thị bảng giá.

## Ngoài scope
Quản lý bảng giá (ERP) · cột hiệu lực · đổi sau gửi duyệt · giá nhập theo bảng giá.
