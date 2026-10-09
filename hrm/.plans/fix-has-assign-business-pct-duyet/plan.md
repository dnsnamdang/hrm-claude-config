# Fix: has_assign_business kẹt = 2 dù PCT đã duyệt (chặn oan nhập KQ bên ERP)

## Triệu chứng
User báo task backfill "cập nhật has_assign_business 2→1 cho phiếu sai" **vẫn chưa được**.
Prod ERP (`erp_new.wr_assign_tasks`): còn **13 phiếu** `has_assign_business=2`.

## Root cause (bằng chứng từ code)
Cờ `has_assign_business` (bảng ERP `wr_assign_tasks`, set từ HRM qua mysql2):
`PCT_DA_DUYET=1`, `PCT_CHUA_DUYET=2`.

Cả **sync** (`AssignRequest::syncWrAssignTask`) lẫn **backfill** chỉ coi PCT "đã duyệt" khi status ∈ `{DA_DUYET=3, DA_NHAP_KET_QUA=5, DA_DUYET_KET_QUA=7}`.
→ **Sót** các trạng thái sau duyệt: `DANG_LAP_HO_SO_THANH_TOAN=8, DA_LAP_HO_SO_THANH_TOAN=9, DANG_LAP_DE_NGHI_THANH_TOAN=10, DA_LAP_DE_NGHI_THANH_TOAN=11` (đều là "Trạng thái phiếu công tác" — PCT phải đã duyệt mới sang được).
PCT đã sang bước thanh toán vẫn bị flag = 2 → ERP chặn oan.
(`KHONG_DUYET=6` = từ chối → vẫn 2, đúng. `DA_LAP_PHIEU_CONG_TAC=4` là của phiếu đề xuất, không tính.)

## Fix
- [x] `AssignRequest`: thêm hằng số dùng chung `PCT_APPROVED_STATUSES = {3,5,7,8,9,10,11}`.
- [x] `syncWrAssignTask` (dòng ~343): dùng `in_array($this->status, self::PCT_APPROVED_STATUSES)`.
- [x] `UpdateDB::backfillPctApprovedHasAssignBusiness`: `$approvedStatuses = AssignRequest::PCT_APPROVED_STATUSES`.
- [x] `php -l` sạch; hằng số resolve đúng `3,5,7,8,9,10,11`.
- [ ] **User chạy backfill trên HRM PROD** (tinker) + đối chiếu 13 phiếu.

## Cách chạy trên PROD (tinker, tại server HRM — nơi mysql trỏ HRM prod & mysql2 trỏ ERP prod)
```
php artisan tinker
>>> (new Database\Seeders\UpdateDB)->backfillPctApprovedHasAssignBusiness()
```
Preview trước khi chạy (xem phiếu nào sẽ được fix):
```php
$ids = \DB::table('assign_business_tasks as abt')
  ->join('assign_requests as ar','ar.id','=','abt.assign_request_id')
  ->where('abt.jobinvoiceable_type', \Modules\Assign\Entities\TpWrAssignTask::class)
  ->where('ar.type', \Modules\Assign\Entities\AssignRequest::PHIEU_CONG_TAC)
  ->whereIn('ar.status', \Modules\Assign\Entities\AssignRequest::PCT_APPROVED_STATUSES)
  ->distinct()->pluck('abt.jobinvoiceable_id');
\Modules\Human\Entities\TpWrAssignTask::whereIn('id',$ids)->where('has_assign_business',2)->get(['id','code','has_assign_business']);
```

## Cập nhật — bug real-time sync khi duyệt (user báo phiếu duyệt sáng nay vẫn =2)
Xác minh trên prod (hrm_2 = HRM prod local, erp_new = ERP prod):
- 13 phiếu kẹt `has_assign_business=2` ĐỀU có PCT `type=2, status=3 (đã duyệt)`, jobinvoiceable_type đúng → bug thật.
- Code hiện tại (5c35d36cf, 03/07) set flag khi duyệt là ĐÚNG; local không tái hiện (0 phiếu kẹt).
- Kết luận: **prod nhiều khả năng chưa deploy 5c35d36cf** (status=3 lưu được ⟹ vòng set flag đáng lẽ đã chạy ⟹ flag phải =1; mà prod vẫn 2). Cần deploy.

### Đã xử lý
- [x] (a) Fix ngay 13 phiếu trên `erp_new`: UPDATE 2→1 (dùng đúng logic backfill: chỉ phiếu có PCT đã duyệt & đang =2). Sau update: không còn dòng nào =2.
- [x] (b) Commit `a5cc316a3` trên `tpe`:
  - Hằng số `AssignRequest::PCT_APPROVED_STATUSES = {3,5,7,8,9,10,11}` (sync + backfill dùng chung).
  - Hardening: vòng set flag ở `store` + `update` query tươi `assignBusinessTasks()->get()` thay vì relation cache.
- [ ] **Deploy `tpe` lên HRM prod** (bắt buộc — để duyệt tự set flag về sau).
- [ ] Xác nhận prod HRM đã có commit set-flag (`git log | grep a5cc316a3` / `5c35d36cf`).

## File
- `Modules/Assign/Entities/AssignRequest.php`
- `database/seeders/UpdateDB.php`
- `Modules/Assign/Http/Controllers/Api/V1/AssignBusinessController.php`
