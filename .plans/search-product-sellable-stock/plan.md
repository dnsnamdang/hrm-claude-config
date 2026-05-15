# Plan: Đổi tồn kho popup searchProduct sang tồn có thể bán

## Trạng thái
- Bắt đầu: 2026-05-06
- Người phụ trách: @nguyentrancu97
- Code DONE: 2026-05-06

### Checkpoint — 2026-05-06
Vừa hoàn thành: 6/6 task — đổi tồn kho popup searchProduct sang tồn có thể bán
Bước tiếp theo: user test trên các màn dùng popup searchProduct (YCXK, nhập kho, ...)

## Tasks

- [x] Task 1: Thay subquery tồn kho — dùng `accounting_stocks` + `accounting_warehouses` thay `stocks` + `stock_of_companies`, loại trừ kho KM
- [x] Task 2: Thêm subquery `hold_details` (group by product_id, company_id)
- [x] Task 3: Thêm subquery `warehouse_export_request_details` chưa xuất (is_complete=false, status NOT IN 3,5, need_export=true)
- [x] Task 4: Đổi select `in_stock` = COALESCE(accounting_qty) - prepick - hold - werd
- [x] Task 5: Cập nhật filter `has_stock` dùng tồn có thể bán thay vì accounting_qty
- [x] Task 6: Giữ nguyên logic cũ cho `is_self_inventory` (kiểm kê tự kiểm)
