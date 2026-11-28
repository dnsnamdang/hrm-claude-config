# Phiếu hạch toán chuyến xe khác — cước dòng này bị ghi bằng cước dòng khác — plan

Báo 27/11/2026: TPV_HTCXK_00447 (`/admin/warehouse/other_delivery_trip_accounting/447`).
- Chi tiết: PNK-12679 = 200k, PNK-12680 = 45k, PNK-12688 = 45k, PNK-12690 = 310k.
- Hạch toán Nợ 6427: 45k, 45k, 310k, 310k (Có 3311 = 758k). Dòng 200k thành 310k.

## Nguyên nhân
`OtherDeliveryTripAccountingController::store()` và `update()` ghép `$deliveryTrip->activities` với `$request->activities`.
- Mỗi khối `if (isset(warehouse_export_id) && $a->warehouse_export_id) … elseif (employee_id khớp)` rơi vào nhánh `elseif`, nhánh này CHỈ so nhân viên.
- Hệ quả: mọi dòng request cùng nhân viên đều ghi đè lên dòng đó, dòng cuối cùng thắng.
- Bảng `activity_has_other_delivery_trip_accountings` lưu đúng từng dòng, chỉ phần hạch toán sai.

Đã kiểm bằng cách mô phỏng đúng vòng lặp (scratchpad `sim.php`):
- 4 dòng cùng `employee_id` → cả 4 dòng = 310k.
- 2 dòng 45k mang `employee_id` khác → ra 45/45/310/310, khớp ảnh. Suy ra phiếu 447 có 2 `employee_id` cho cùng 1 tên.
- Chưa kiểm được trên dữ liệu thật vì local là `hrm_erp_test`, không có phiếu 447.

## Tasks
- [x] Tách hàm `mergeRequestActivities()`: ghép theo nhân viên + đúng phiếu.
  - Dòng có PXK → khớp `warehouse_export_id`.
  - Dòng có PNK → khớp `warehouse_import_id`.
  - Dòng không có phiếu → chỉ khớp dòng request không có phiếu.
  - Gặp dòng khớp đầu tiên thì dừng. Dùng cho cả `store` và `update`.
- [x] Mô phỏng lại: 200/45/45/310 ra đúng.
- [ ] Kiểm màn thật: tạo hoặc sửa 1 phiếu có nhiều PNK cùng nhân viên khác cước.
- [ ] Phiếu cũ đã hạch toán sai (447 và các phiếu khác): Sửa → Lưu lại để hạch toán lại, hoặc viết script — chờ user quyết.

## Kiểm trên prod hrm_erp_gop (27/11/2026, chỉ SELECT)
- Cột `activity_has_other_delivery_trip_accounting.employee_id` là TINYINT → 408/407 lưu thành 127. Request lúc lưu vẫn mang id thật, nên nguyên nhân ở trên đúng. Fix có so nhân viên vẫn đúng.
- Script `detect_odta.php` (scratchpad) mô phỏng vòng ghép cũ trên dữ liệu thật:
  - 72 phiếu khớp chính xác (09/2025 → 27/11/2026).
  - 7 phiếu lệch vì lý do khác, KHÔNG thuộc lỗi này: 137, 178, 180, 256, 352, 414, 442.
- Dry-run `dryrun_odta.php`:
  - 70 phiếu sửa thẳng được: 245 dòng Nợ 6427/33481 + 1 dòng Có 3311 mỗi phiếu. Tài khoản 6427/33481 đều đúng, chỉ sai tiền.
  - 2 phiếu có thêm dòng công lái xe (249, 380), cần xem tay.
  - Tổng Có 3311: tăng 110,790,000, giảm 55,704,000.
- 447: dòng 1339969 45k→200k, 1339971 310k→45k, Có 3311 1339974 758k→648k.
- [x] 28/11/2026 ĐÃ SỬA phiếu 447 trên hrm_erp_gop (user duyệt "chỉ sửa 447"): 1 transaction, kiểm giá trị cũ trước khi update. Kết quả Nợ 200/45/45/310 + 1331 48k = Có 3311 648k. Backup: scratchpad `backup_447_account_details.json`.
- [x] 28/11/2026 ĐÃ SỬA 69 phiếu còn lại (user duyệt): 1 transaction, kiểm giá trị cũ + Nợ=Có từng phiếu. 240 dòng 6427 + 69 dòng Có 3311. Backup `backup_69_account_details.json` (412 dòng), danh sách `danh_sach_phieu_da_sua.csv` (scratchpad).
- [ ] 249, 380 (có dòng công lái xe): xem tay.
- [x] 28/11/2026 push: develop_02 a5615c740f, gop_db 0b21160845 (cherry-pick). Chưa kiểm màn thật.

### Checkpoint — 2026-11-28 17:30 (wrap up cuối ngày)
Vừa hoàn thành:
- Commit + push fix `mergeRequestActivities()` (chỉ 1 file `OtherDeliveryTripAccountingController.php`): develop_02 `a5615c740f` ✓push origin; gop_db `0b21160845` (cherry-pick qua worktree tạm, đã xoá) ✓push origin.
- Sửa dữ liệu hrm_erp_gop: phiếu 447 (08:41) + 69 phiếu còn lại (08:57) = 70 phiếu, đều Nợ = Có. Đọc lại prod: cả 70 phiếu khớp số mới.
- Xuất Excel `danh-sach-phieu-da-sua.xlsx` (thư mục này; 2 sheet: tổng hợp theo phiếu + 315 dòng chi tiết).
- Đánh giá ảnh hưởng sửa thẳng: không đổi 1331/33481/dữ liệu chuyến xe/BC HRM; đổi chi phí 6427 tháng 09/2025→11/2026 và công nợ 3311 của 2 nhà xe (233460: dư Nợ 7,100,000 → 0; 14059: 333,173,666 → 285,187,666, phần còn lại không do lỗi này).
- Xác nhận lỗi phát sinh ở bước sinh bút toán của phiếu hạch toán (chuyến xe + bảng chi tiết lưu đúng). 70 phiếu sai đều do Cao Thị Thùy Linh lập (TPV), lỗi do code nên ai ghép nhiều phiếu kho/NV cũng bị.
Đang làm dở: TPHP_HTCXK_00249, 00380 (có dòng công lái xe) chưa sửa — xem tay.
Bước tiếp theo: Xem tay 249/380; kiểm màn thật tạo/sửa phiếu nhiều PNK cùng NV khác cước; báo kế toán chi phí 6427 các tháng cũ đã đổi + đối chiếu dư Nợ nhà xe 14059.
Blocked:

### Checkpoint — 2026-11-27 17:18 (wrap up cuối ngày)
Vừa hoàn thành: Fix `mergeRequestActivities()` + mô phỏng đúng — CHƯA commit (` M app/Http/Controllers/Warehouse/OtherDeliveryTripAccountingController.php` trên develop_02).
Đang làm dở: User hỏi 17:10 "sửa lại dữ liệu chưa": tra hrm_erp_gop phiếu 447 (NV request 127, NV chuyến 408/407) không tái tạo được 45/45/310/310 theo giả thuyết — nghi phiếu tạo từ HRM; điều tra dở, CHƯA sửa dữ liệu.
Bước tiếp theo: Xác minh nguồn tạo phiếu 447 (HRM?) → nếu bug ở HRM thì fix bên HRM; kiểm màn thật; commit + push fix ERP; user quyết cách sửa phiếu cũ.
Blocked: Chờ user quyết cách sửa dữ liệu
