# Design: Xuất ghép từ hàng giữ (TanPhatDev)

## Bối cảnh
YCXG (Yêu cầu xuất ghép) hiện chỉ xuất từ tồn thường. Yêu cầu mới: cho lấy nguyên liệu từ kho hàng đang giữ của KH; khi nhập ghép thì thành phẩm vẫn giữ cho NV yêu cầu + KH đó.

## Quy tắc đã chốt

### Hiển thị (tab Danh sách tổng hợp YCXG)
- Tồn có thể bán = `in_stock - in_promotion_stock` (từ API `POST /admin/warehouse_infos/stockOfProducts`)
- Đang giữ = `prepick_qty` của Auth user (không truyền `customer_id`)
- Validation BE: `qty <= in_stock + prepick_qty` (đơn giản, vì `in_stock` đã clamp `max(0, min(...))`)
- Cột "Từ xuất giữ": input + nút search → popup `searchPrepickDetail`. BẮT BUỘC chọn 1 record nếu `qty > tồn có thể bán`.

### Customer constraint
- **Per-parent** (per "Hàng cần ghép"): các recipe có `from_prepick_detail` trong cùng parent phải cùng KH. Parent khác có thể khác KH.

### Cascade khi nhập ghép
- Bất kỳ 1 recipe của parent có `from_prepick_detail` → toàn bộ qty thành phẩm parent đó được giữ cho `(employee_id = YCXG.created_by, customer_id = customer của prepick)`.
- Default `expire_date` = `today + Config::getConfig('max_prepick_date')` ngày, user sửa được trên tab Phân bổ hàng giữ.

### Xuất thẳng (`is_export_direct`)
- Hỗ trợ cả 2 chế độ.
- Tái sử dụng pattern hiện có:
  - `warehouse_export_request_details.export_prepick_qty / export_hold_qty / export_total_qty`
  - `WarehouseExportRequest::updateWarehouse()` (L880-927) tự tính qty từ giữ/từ tồn
  - `ProductExport` (L1365-1413) FIFO consume `prepick_detail` theo `expire_date ASC` cho `(product, employee, customer)`
- KHÔNG cần track `from_prepick_detail_id` xuyên chain — chỉ cần truyền `customer_id` + flag `can_export_from_prepick = true` xuống cascade.

## Thay đổi (dự kiến)

### Migration
- `join_export_request_product_recipes`: thêm `from_prepick_detail_id` (BIGINT NULL, indexed)
- Thêm `customer_id` ở YCXG — vị trí TBD (Q6: parent vs recipe vs cả 2)
- Có thể thêm `customer_id` ở `warehouse_export_request_details` nếu chọn 1 wer cho >1 customer (Q6)

### Backend
- `JoinExportRequestsController`: validation rule mới (qty ≤ in_stock + prepick_qty, customer per-parent), syncProducts lưu from_prepick_detail_id + customer_id
- `WarehouseExportRequestsController` / hoặc service tạo wer: nhận customer_id từ YCXG cascade
- `ProductImportsController`: thêm xử lý tab `phan_bo_hang_giu` cho `type=8` (NHAP_GHEP) — store/update + tạo `prepick_detail` mới cho thành phẩm
- `ProductExport` xuất thẳng (`is_export_direct && type=XUAT_GHEP`): bổ sung tạo `prepick_detail` mới ngay khi xuất (không qua nhập ghép)

### Frontend — YCXG
- `warehouse/join_export_requests/form.blade.php` (tab Danh sách tổng hợp): thêm 3 cột Tồn có thể bán / Đang giữ / Từ xuất giữ
- `partials/classes/warehouse/JoinExportRequest.blade.php`: gọi API `stockOfProducts` để fill `in_stock`, `in_promotion_stock`, `prepick_qty`
- `JoinExportRequestProductRecipe`: thêm field `from_prepick_detail`, getter `prepick_detail_name`
- `formJs.blade.php`: include `searchPrepickDetailJs`, hàm `choosePrepickDetail(recipe)`, `selectPrepickDetail(detail)`, enforce per-parent customer

### Frontend — Phiếu nhập ghép (type=8)
- `warehouse/product_imports/form.blade.php`: thêm nhánh mới `<div ng-if="form.type == 8">` cho tab `phan_bo_hang_giu`. KHÔNG chạm 3 nhánh hiện có (`form.is_foreign`, `type==15`, `type==2`).
- Cột: Tên hàng (label), ĐVT (label), SL (label), Kinh doanh (mã KH - tên KH - số YCXG - số phiếu xuất ghép - tên NV yêu cầu - mã PB), Link xem YCXG/phiếu xuất, SL yêu cầu, SL giữ, Hạn giữ (input editable, default `today + max_prepick_date`)

## Không thay đổi
- 3 nhánh tab `phan_bo_hang_giu` hiện có cho `form.is_foreign`, `type==15`, `type==2` — giữ nguyên
- Pattern FIFO consume `prepick_detail` ở `ProductExport` — giữ nguyên
- `warehouse_export_request_details.export_*` columns — chỉ tận dụng, không đổi schema

## Pending (chưa hỏi xong)
- **Q6**: Customer_id lưu ở cấp nào (parent vs recipe vs cả 2)? Cascade khi YCXG có >1 customer → 1 wer hay nhiều wer?
- **Q7**: Validation hạn giữ trong nhập ghép (`> today` và `<= today + max_prepick_date`?)
- **Q8**: Approval flow kế toán kho — có sửa/từ chối "Từ xuất giữ" được không?
- **Q9**: YCXG status pending có khoá `prepick_detail` không?
- **Q10**: Popup `searchPrepickDetail` lọc Auth user only hay tất cả NV?
- **Q11**: Edit/Cancel YCXG sau khi tạo — behavior với from_prepick đã chọn?
