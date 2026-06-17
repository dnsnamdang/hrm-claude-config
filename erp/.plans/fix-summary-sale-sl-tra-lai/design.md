# Design — Fix báo cáo Tổng hợp bán hàng: cột "SL trả lại" không hiện

## Mục tiêu
Báo cáo `admin/reports/summary_sale?type=all` (và các type khác dùng chung `getData`) đang để cột **SL trả lại** = 0 → FE hiển thị `-`. Cần tính đúng SL trả lại + trừ vào SL/tiền bán thực tế.

## Hiện trạng (root cause)
- `SummarySaleReportService::getData()` lấy dữ liệu từ **phiếu xuất thực tế** (`product_export_details` ped, `borrow_sell_products` bsp). 2 bảng này KHÔNG có cột `returned_qty`.
- Cả 2 nhánh union đều hard-code `DB::raw('0 as returned_qty')` (dòng 68, 83, 177, 192) → SL trả lại luôn 0, `real_qty = exported_qty`.
- SL trả lại thực tế được ghi nhận qua **phiếu nhập trả lại**: `product_imports.type IN (BAN_TRA_LAI=4, NHAP_BAN_MUON_TRA_LAI=9)`, status=1, chi tiết ở `product_import_details` (pid).

## Quyết định (chốt với user)
1. Nguồn SL trả lại: phiếu nhập trả lại type 4 + 9 (status=1). ✅
2. SL bán thực tế = SL bán − SL trả lại. ✅
3. Lọc trả lại **theo khoảng ngày** của report (`pi.created_at`). ✅
4. Netting **đầy đủ**: trả lại trừ cả Thành tiền bán / net / vốn / Lãi lỗ; Đơn giá = Thành tiền / SL thực tế. ✅ (giống `SaleProductReportService`)

## Giải pháp
Thêm nhánh union thứ 3 (`$return`) vào `getData()` **chỉ ở path không-detail** (path tạo aggregate group theo product — đây là path mà `summary_sale?type=all` dùng):

- Nguồn: `product_import_details pid` JOIN `product_imports pi` (type 4|9, status 1).
- **Định giá bằng dòng xuất gốc**: JOIN `product_export_details oped` ON `oped.id = pid.product_export_detail_id` → tái sử dụng đúng `allocated_price`, `price`, `export_price`, `unit_coefficient` + `sale_max_percent` (qua `fctp`/`wrsci`) như nhánh xuất bán. Đảm bảo netting khớp với "SL bán".
- Đóng góp cột (đúng thứ tự 12 cột của nhánh xuất để union hợp lệ):
  - `real_qty = -SUM(pid.qty)`
  - `exported_qty = 0`
  - `returned_qty = SUM(pid.qty)`
  - `allocated_price_amount`, `net_price_amount`, `export_price_amount` = **âm** theo công thức giống nhánh xuất nhưng nhân `pid.qty`.
- Lọc ngày + product: dùng lại `$this->filter($return, $request, 'pi', 'oped', 'p', [...])`.
- Phân quyền: theo `em_info` (join `employees`→`employee_infos` qua `pi.employee_created_request_id`), mirror nhánh borrow.
- `union` thêm `$return` trước khi bọc `DB::table(... 'result')`.

## Phạm vi ảnh hưởng
- Hàm `SummarySaleReportService::getData()` dùng chung: màn báo cáo (`summarySaleSearchData`), in (`summarySalePrint`), export Excel (`summarySaleExport`) → cả 3 được fix đồng thời.
- Path `type='detail'` (getReportSaleDetail) GIỮ NGUYÊN ở bước này (chỉ sửa path tổng hợp). Nếu cần trả lại ở detail sẽ làm phase sau.

## Rủi ro / cần verify khi test
- **Đơn vị của `pid.qty`**: giả định cùng đơn vị bán như `ped.export_qty` (để `pid.qty / oped.unit_coefficient` khớp). Cần đối chiếu số thực tế 1 mã có trả lại.
- **Type 9 (bán mượn trả lại)**: chỉ được định giá nếu `pid.product_export_detail_id` có trỏ tới `ped`. Dùng INNER JOIN trên `oped` → phiếu trả lại không link sẽ bị loại (tránh số rác). Cần verify với dữ liệu thật.
