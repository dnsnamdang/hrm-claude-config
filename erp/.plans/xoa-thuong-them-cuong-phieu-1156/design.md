# Xóa thưởng thêm của Nguyễn Phú Cường trong phiếu chi 1156 (prod)

> Thao tác data-fix PRODUCTION (erp.eteksofts.com). Tinker: `UpdateDB::removeExtraBonusCuongBillPayment1156`.

## Yêu cầu
Xóa dữ liệu **thưởng thêm** của Nguyễn Phú Cường (employee 485) trong phiếu chi **1156** (`TPE.PC0626.00022`, đã duyệt) + bản ghi hạch toán thưởng thêm tương ứng.

## Dữ liệu (điều tra prod 2026-07-04)
- **bill_payment_detail id 6368** (employee 485): thưởng thêm = `commission_bonus_quarter` = `payment_commission_bonus_quarter` = **-3.626.264** (âm, đang TRỪ vào tổng). Cùng detail còn: thưởng NS tháng 3.174.014, NS quý 4.021.071, chênh lệch NV 16.751.287. Tổng `payment_money_request/approve/approve_exchange` = **20.320.108** (đã gồm khoản trừ -3.6M).
- **Hạch toán thưởng thêm**: `account_details` id **895818** (account 116, work 9 = TT, type 1, +3.626.264) — duy nhất, chỉ Cường. Có ref `account_detail_refs` id **941191** (account_ref_id=2).

## Quyết định (user xác nhận 2026-07-04)
1. **Phạm vi**: set `commission_bonus_quarter` + `payment_commission_bonus_quarter` của detail 6368 về **0** (giữ nguyên các thưởng khác) + xóa account_detail 895818.
2. **Tổng (2b)**: cập nhật lại `payment_money_request/approve/approve_exchange` = **23.946.372** (= 20.320.108 + 3.626.264, do bỏ khoản trừ âm).
3. **Không** đối chiếu sổ 116 / báo cáo.
4. (Bổ sung khi implement) Xóa kèm `account_detail_refs` 941191 để tránh mồ côi (thuộc bản ghi hạch toán bị xóa).

## Implement
`database/seeds/UpdateDB.php::removeExtraBonusCuongBillPayment1156($doUpdate=false)`:
- Guard: detail đúng employee/bill_payment; thưởng thêm còn = -3.626.264 (chống chạy lại/dữ liệu đổi).
- Preview khi không tham số; thực hiện trong transaction khi truyền `true`.
- Dùng `DB::table` (không kích hoạt model observer). php -l sạch.

Chạy trên prod (LƯU Ý: class `UpdateDB` ở **global namespace**, không có `Database\Seeds\` — gọi `\UpdateDB`):
```
php artisan tinker
>>> (new \UpdateDB)->removeExtraBonusCuongBillPayment1156();      // preview
>>> (new \UpdateDB)->removeExtraBonusCuongBillPayment1156(true);  // thực hiện
```
Nếu vẫn "Class not found" sau khi deploy: `composer dump-autoload` (autoload kiểu classmap cho database/seeds).

## Trạng thái
- Code XONG, **đã commit + push `master`** (commit 51553d47, `5c5a6a30..51553d47`).
- Deploy master lên prod → chạy tinker (preview trước, rồi `true`). Chưa chạy — user tự thực hiện trên prod.
