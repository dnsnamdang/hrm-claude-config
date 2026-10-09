# Fix ngày hạch toán phiếu quyết toán năng suất quý (BillProductivitySettlementQuarter)

## Vấn đề
account_details của phiếu bị hạch toán theo ngày TẠO (updated_at = hôm nay) thay vì
`date_accounting` ghi trên phiếu.
- Prod: phiếu date_accounting=2026-06-30 → account_details.invoiceable_date_accounting=2026-07-02.

## Root cause
`AccountDetail::saveAccountDetail` (app/Model/Accounting/AccountDetail.php ~187-194) chọn field ngày
theo LOẠI phiếu. `BillProductivitySettlementQuarter` KHÔNG có trong whitelist dùng `date_accounting`
→ rơi vào `else` dùng `$invoiceable->updated_at`.

## Fix
- [x] Thêm `BillProductivitySettlementQuarter::class` vào list nhánh `date_accounting` (dòng 188).
      Cùng namespace App\Model\Accounting → không cần use. php -l sạch.
- [ ] User test: tạo/hạch toán lại phiếu → account_details.invoiceable_date_accounting = date_accounting phiếu.
- [x] Chuẩn bị fix data cũ: (a) file SQL `fix-data-prod.sql`; (b) method `UpdateDB::fixProductivitySettlementQuarterAccountingDate()` (idempotent). php -l sạch.
- [x] BUG method fix (lần 1): `$bill->date_accounting` qua accessor trả d/m/Y ("30/06/2026") → update() lưu 0000-00-00.
      Đã sửa: lấy RAW `$bill->getAttributes()['date_accounting']` + `Carbon::parse()->format('Y-m-d 00:00:00')`.
      SQL file: dùng `DATE(b.date_accounting)`.
- [ ] Chạy LẠI fix data trên prod (WRITE) — user tự chạy: `php artisan tinker >>> (new \UpdateDB)->fixProductivitySettlementQuarterAccountingDate()`
      (method update TẤT CẢ dòng của phiếu → tự sửa 52 dòng 0000-00-00 hiện tại về 2026-06-30 00:00:00)

## Lưu ý
- Đây là sửa HÀM DÙNG CHUNG (saveAccountDetail) nhưng chỉ THÊM 1 class vào whitelist → chỉ ảnh hưởng
  đúng phiếu năng suất quý, không đụng phiếu khác.
- Code hạch toán (`saveAccountDetail`) ĐÚNG: dòng 196-197 có preg_match chuyển d/m/Y → Y-m-d. Bug chỉ ở
  method data-fix (bỏ qua preg_match đó).

## Branch: master
