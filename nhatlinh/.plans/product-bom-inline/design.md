# BOM inline trong Hàng hoá — Tóm tắt

**Spec chi tiết:** `docs/superpowers/specs/2026-06-06-product-bom-inline-design.md`
**Plan:** `.plans/product-bom-inline/plan.md`

## Mục tiêu
Tạo/sửa BOM ngay trong tab BOM của từng hàng hoá, lưu **nested** (chung 1 lần với hàng hoá). **Bỏ hẳn** danh mục BOM riêng (`/category/boms` + menu + route/controller). Mỗi hàng hoá ≤1 BOM = bảng định mức NVL; **bỏ Mã/Tên BOM** khỏi UI; trạng thái BOM theo hàng hoá; **gỡ permission BOM**.

## Quyết định chốt (2026-06-06)
1. Lưu nested (payload hàng hoá thêm `bom_items` + `bom_note`).
2. Bỏ hẳn menu + trang + route/controller BOM.
3. Tab BOM chỉ còn bảng NVL + ghi chú (bỏ Mã/Tên BOM).
4. Gỡ permission BOM (1105 "Quản lý định mức BOM", 1106 "Xem định mức BOM").

## Điểm kỹ thuật
- `boms.code`/`name` tự sinh nội bộ (`BOM-<product_id>` / tên hàng hoá), `status` = status hàng hoá.
- `bom_items` rỗng → xoá BOM + `default_bom_id=null`.
- Lịch sử lấy kèm trong API chi tiết hàng hoá (`boms[0].histories`) → `BomHistoryModal` nhận data trực tiếp, không cần endpoint BOM.
- Giữ entity `Bom/BomItem/BomHistory` + `BomService::syncItems`.
