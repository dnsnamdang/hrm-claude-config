# Fix — Cảnh báo hàng mượn/giữ hết hạn không theo config warning_day

## Triệu chứng
Widget "Cảnh báo hàng mượn, hàng giữ hết hạn" trên dashboard (tab Phê duyệt) đếm số "Hàng mượn hết hạn" / "Hàng giữ hết hạn" KHÔNG theo cấu hình "Số ngày cảnh báo (mượn/giữ hàng)" (`warning_day`, đang = 7).

## Root cause
`app/Http/Controllers/HomeController.php` (method `approveList`, ~dòng 2270-2308): 2 query lọc theo hôm nay, bỏ qua `warning_day`:
- Hàng mượn: `->where('per.return_date', '<=', $now)`
- Hàng giữ: `->where('pds.expire_date', '<=', $now)`

Trong khi pattern chuẩn ở 3 nơi khác đều cộng `warning_day`:
- `BorrowIndexReportService.php:241`, `PrepickIndexReportService.php:203`, `WarehouseInfosController.php:749`: `<= addDays(now()->startOfDay(), $config->warning_day)`
- Cron `BorrowWarning`/`PrepickWarning` cũng dùng `now + warning_day`.

→ Dashboard chỉ đếm hàng đã quá hạn tính tới hôm nay, không tính theo cửa sổ cảnh báo cấu hình.

## Fix (HomeController, method approveList)
- [x] Nạp config: `$config = \App\Model\Common\Config::getConfig();` + `$warning_date = addDays(Carbon::now()->startOfDay(), $config->warning_day)->format('Y-m-d');`
- [x] Hàng mượn: `per.return_date <= $warning_date` (thay `$now`)
- [x] Hàng giữ: `pds.expire_date <= $warning_date` (thay `$now`)
- [x] Giữ nguyên `$now` cho biểu thức CASE tính `status` (1 chưa đến hạn / 2 quá hạn / 3 đúng hạn) — đúng theo ngày hiện tại.
- [x] `php -l` sạch.

## Kiểm thử (user)
- [ ] Đổi `warning_day` ở cấu hình → số đếm 2 widget thay đổi tương ứng (gồm hàng sắp hết hạn trong N ngày).
- [ ] Đối chiếu số đếm với màn báo cáo hàng mượn/giữ (BorrowIndexReport/PrepickIndexReport) — phải khớp logic.

### Checkpoint — 2026-06-09
Vừa hoàn thành: sửa 2 filter dùng warning_date theo config; lint sạch
Bước tiếp theo: user kiểm thử đổi warning_day + đối chiếu báo cáo
Blocked:
