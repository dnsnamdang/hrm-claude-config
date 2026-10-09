# Fix — Sửa PCT đã duyệt bị reset has_assign_business về "chưa duyệt"

## Bối cảnh / Bug
Phiếu giao việc ERP `TPE.PGV.2026013585`: PCT (phiếu giao công tác) đã duyệt nhưng ERP `wr_assign_tasks.has_assign_business = 2` (PCT_CHUA_DUYET) → nút "Nhập kết quả" bị ẩn, NV có quyền 418 vẫn không nhập được.

## Root cause
`AssignRequest::syncWrAssignTask()` (`Modules/Assign/Entities/AssignRequest.php` ~337-341) set `has_assign_business = PCT_CHUA_DUYET (2)` **vô điều kiện** mỗi lần sync. Hàm này chạy qua `syncAssignBusinessErp()` ở `AssignBusinessController:785` — nhánh **"sửa phiếu sau khi đã duyệt"** (`status == DA_DUYET`) — và nhánh này KHÔNG flip lại về 1. Nên: tạo→2, duyệt→1, **sửa PCT đã duyệt→bị ghi đè về 2** dù vẫn đang duyệt.

## Fix (A — code HRM)
- [x] Trong `syncWrAssignTask()`: set `has_assign_business` theo trạng thái duyệt hiện tại của PCT:
  - status ∈ {DA_DUYET(3), DA_NHAP_KET_QUA(5), DA_DUYET_KET_QUA(7)} → PCT_DA_DUYET(1)
  - còn lại → PCT_CHUA_DUYET(2)
- [ ] `php -l` file.

## Fix (B — backfill data qua tinker)
- [x] Thêm method `backfillPctApprovedHasAssignBusiness()` vào `database/seeders/UpdateDB.php`: duyệt các PCT (assign_requests type=PHIEU_CONG_TAC) status ∈ {3,5,7}, với mỗi assignBusinessTask (jobinvoiceable=TpWrAssignTask) → nếu ERP `has_assign_business == 2` thì set = 1. Chỉ flip 2→1 (không đụng 0). `php -l` sạch.
- [x] **Rewrite set-based (2026-07-07)**: bản cũ lặp `find()` từng task qua kết nối ERP (~7000+ round-trip) → "đứng im" (thực ra chỉ rất chậm, không treo). Đổi sang: 1 truy vấn HRM (join assign_business_tasks+assign_requests) lấy id → UPDATE hàng loạt qua `TpWrAssignTask::query()->whereIn()->update()` (bulk, không per-row). `php -l` sạch.
- [x] Trạng thái prod (2026-07-07): `wr_assign_tasks.has_assign_business` — 0:6586, 1:7009, **2: chỉ 2 dòng**; phiếu **13585 đã = 1** (chị Hiền hết bị chặn). Không có trigger trên bảng.
- [ ] User chạy lại bản mới trên **HRM production**: `php artisan tinker` → `(new \Database\Seeders\UpdateDB)->backfillPctApprovedHasAssignBusiness()` (giờ chạy trong vài giây).

## File
- `hrm-api/Modules/Assign/Entities/AssignRequest.php` (syncWrAssignTask — fix reset)
- `hrm-api/database/seeders/UpdateDB.php` (method backfill)
