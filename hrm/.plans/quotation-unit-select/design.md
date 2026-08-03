# Chọn ĐVT khi tạo/sửa báo giá (hàng ERP) — Tóm tắt

> Phụ trách: @dnsnamdang · Branch: `tpe-develop-assign`
> Spec đầy đủ: `docs/superpowers/specs/2026-07-12-quotation-unit-select-design.md`

## Mục tiêu
Cho chọn ĐVT cho dòng hàng ERP ở màn Tạo/Sửa báo giá; đổi ĐVT → lấy lại đơn giá bán + giá vốn theo đúng đơn vị (giá lưu theo từng đơn vị bên ERP). Màn Xem chi tiết giữ text.

## Phạm vi (đã chốt)
- CHỈ báo giá **type=2 (tự lập)**.
- CHỈ **hàng ERP đơn** (loại combo cha-con recipe).
- Dropdown = **tất cả `product_units`** của sản phẩm.
- Ngoài phạm vi: type=1 (kế thừa BOM — làm ở BOM phase khác), combo ERP, hàng tạm, dịch vụ.

## Quyết định lớn
1. **BE là nguồn chân lý giá ERP**: `saveDirectProduct` re-derive `quoted_price`/`estimated_price` theo `(erp_product_id, unit_id)` — cả create lẫn update (hiện update không đụng giá → phải sửa).
2. Helper mới `TpProductUnitPrice::getUnitOptions()` (list đơn vị + giá/đơn vị) + `getUnitPrice($erpId,$unitId)` (fallback base). Endpoint mới `POST /assign/quotations/erp-product-units` gate giá vốn theo quyền `Xem giá vốn hàng hoá`.
3. FE `edit.vue`: cột ĐVT → select cho dòng ERP đủ điều kiện; đổi → quy đổi tỷ giá + làm tròn hiện có → gán giá + recompute tổng. Detail giữ text.
4. Không migration/permission mới.

## Rủi ro
- Update path re-derive giá ERP mỗi lần lưu → nếu ERP đổi giá, báo giá nháp đổi giá khi lưu lại (đúng nguyên tắc khoá giá ERP, cần test).
