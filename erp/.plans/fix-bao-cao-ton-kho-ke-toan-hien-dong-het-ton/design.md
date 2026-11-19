# Báo cáo tồn kho kế toán theo mặt hàng hiện dòng đã hết tồn

@junfoke · Repo `TanPhatDev`, nhánh `gop_db` · 2026-10-10

## Hiện tượng
Màn `admin/warehouse/warehouse_reports/accountingWarehouseProductReport` (tính đến 10/10/2026, cty Tân Phát, kho LN02)
hiện 3 dòng SL tồn "-" / Giá trị "-" trong khi Tổng cộng = 0:
SKYO-SHS-210Z-SF:01, DSEN-22-DSM, DSEN-22-DPF.

## Nguyên nhân (code, KHÔNG phải data)
`Product::accountingWarehouseReportProductSearchData` (+ bản sao `ProductTemplate`) lọc dòng bằng
`HAVING SUM(asl.change) > 0 OR SUM(asl.value_after) > 0`.
`asl.value_after` là số dư SAU từng lần nhập/xuất → cộng dồn qua các log gần như luôn > 0 (chỉ cần 1 lần nhập).
Hàng nhập rồi xuất hết (SUM(change)=0) vẫn lọt vế 2. DB: 3 mã mỗi mã 2 log, SUM(change)=0, SUM(value_after)=18.97tr/720k/250k.

## Fix
HAVING theo tồn ĐÃ TÍNH (cùng biểu thức cột hiển thị):
`SUM(asl.change) > 0 OR ABS(SUM(asl.change * COALESCE(giá...))) >= 1`
→ còn SL thì hiện; hết SL nhưng lệch giá trị ≥ 1đ vẫn hiện (để kế toán xử lý); hết cả hai thì ẩn.
⚠️ Không dùng alias (`total_qty`) trong HAVING: câu count của `paginate` (Laravel bản này) bỏ phần select → "Unknown column".

## Phạm vi ảnh hưởng
Màn xem + export (`WarehouseReportsController:1566`) + `AccountingWarehouseProductMailJob`. Summary (Tổng cộng) không có HAVING → không đổi.
