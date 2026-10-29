# Sửa cột "Thưởng thêm" — cộng Có trừ Nợ (báo cáo Tổng hợp thu nhập từ bán hàng)

## Bối cảnh
Báo cáo `/admin/reports/commission-settlement-quarter` ("Bảng tổng hợp thu nhập từ bán hàng"),
service `app/Services/Reports/CommissionSettlementQuarterReportService.php`.

Cột **"Thưởng thêm"** = field `commission_bonus_quarter`, lấy từ `account_details`:
- `account_id = 117` (TK 3351 "Chi phí phải trả ngắn hạn")
- `work_id = $works['TT']` (công việc code "TT" = "Thưởng thêm", id=9)
- loại trừ phiếu: `whereNotIn invoiceable_type [BillPayment, BillPaymentAuthorization, ClosingEntry]`
- lọc ngày theo `invoiceable_date_accounting`, lọc NV theo `employee_id`.

## Vấn đề
Hiện cột này **chỉ cộng bên Có** (`type = 2`), KHÔNG trừ bên Nợ (`type = 1`) — khác với các cột
liền kề (`diff_employee_amount`, `commission_month`, `commission_quarter`) đều dùng
`(SUM Có − SUM Nợ)`. → khi có bút toán điều chỉnh ghi Nợ TK 3351 work TT, cột thưởng thêm không
giảm tương ứng → sai số.

## Yêu cầu (user chốt)
Sửa `commission_bonus_quarter` thành **cộng bên Có (type=2) − trừ bên Nợ (type=1)**,
**vẫn giữ nguyên** các điều kiện loại trừ phiếu như hiện tại.

## Phạm vi
- Chỉ 2 dòng `DB::raw` trong service (dòng 54 nhánh FirmContract, dòng 214 nhánh WrServiceContract).
- KHÔNG đổi where loại trừ, KHÔNG đổi cột ngày, KHÔNG đụng print/export (dùng chung data từ service).
- KHÔNG ghi DB. DB = PROD hrm_erp_gop → chỉ sửa code.

## Thiết kế
Đổi (cả 2 chỗ) từ:
```php
DB::raw("SUM(CASE WHEN ac.account_id = 117 AND ac.type = 2 AND ac.work_id = ".$works['TT']." THEN ac.money_value_exchange ELSE 0 END) as commission_bonus_quarter"),
```
thành (khớp pattern các cột liền kề):
```php
DB::raw("(SUM(CASE WHEN ac.account_id = 117 AND ac.type = 2 AND ac.work_id = ".$works['TT']." THEN ac.money_value_exchange ELSE 0 END)
- SUM(CASE WHEN ac.type = 1 AND ac.account_id = 117 AND ac.work_id = ".$works['TT']." THEN ac.money_value_exchange ELSE 0 END)) as commission_bonus_quarter"),
```
