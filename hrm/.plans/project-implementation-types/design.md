# Design: Cập nhật luồng triển khai Dự án TKT

## Mục đích
Bổ sung 3 cách triển khai dự án TKT (`implementation_type`), thay đổi luồng giải pháp + báo giá theo từng loại.

## Scope tổng thể (4 Phase)

| Phase | Nội dung | Trạng thái |
|-------|---------|-----------|
| **A** | KD tự triển khai: tạo báo giá từ BOM (bỏ PricingRequest) + permission xem giá vốn + lock giá bán ERP | Done |
| **B** | Type 2: Phân quyền XD giá theo phòng/công ty + lọc duyệt BG theo dept/company | Đang làm |
| **C** | Báo giá trực tiếp (không GP, không BOM) — Type 1 tạo BG từ tab Dự án, form gộp sản phẩm+giá | Đang làm |
| **D** | (Dự phòng cho yêu cầu mở rộng) | Chưa làm |

## Hiện trạng đã implement

### DB + Entity
- Field `implementation_type` (tinyint, default=3) trên `prospective_projects`
- Constants: SELF=1, BY_DEPT=2, CROSS_DEPT=3
- FE: radio chọn trên form tạo/sửa dự án (ProjectInfoSection.vue)
- Lock: không đổi type khi đã có Solution/RequestSolution

### Type 1 (Tự triển khai) — đã có
- Chặn tạo YC làm GP (RequestSolutionService:185)
- KD tạo Solution: pm_id=self, has_modules=false, skip duyệt PM/Leader → nhảy "Đang triển khai"
- Hồ sơ phê duyệt GP: submit → auto approved
- Tiến trình dự án: dựa trên Solution status, không cần RequestSolution

### Type 2 (Triển khai theo phòng) — đã có
- Lock receive_dept = phòng KD phụ trách
- DS YC làm GP filter theo phòng
- Solution canReceive() check phòng

## Quyết định thiết kế
1. Giá niêm yết = giá Bán lẻ (price_type_id=1) từ bảng `product_unit_prices` trên ERP DB
2. Join: BomListProduct.erp_product_id → products.id → product_units(is_base=1) → product_unit_prices(price_type_id=1)
3. Permission-based ẩn giá vốn (không phụ thuộc implementation_type)
4. Lock giá bán hàng ERP áp dụng tất cả type (không chỉ type 1)
5. Hàng tạm = BomListProduct có erp_product_id = NULL → user toàn quyền giá
