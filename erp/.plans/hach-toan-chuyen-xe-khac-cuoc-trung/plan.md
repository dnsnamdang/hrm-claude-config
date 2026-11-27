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

### Checkpoint — 2026-11-27 17:18 (wrap up cuối ngày)
Vừa hoàn thành: Fix `mergeRequestActivities()` + mô phỏng đúng — CHƯA commit (` M app/Http/Controllers/Warehouse/OtherDeliveryTripAccountingController.php` trên develop_02).
Đang làm dở: User hỏi 17:10 "sửa lại dữ liệu chưa": tra hrm_erp_gop phiếu 447 (NV request 127, NV chuyến 408/407) không tái tạo được 45/45/310/310 theo giả thuyết — nghi phiếu tạo từ HRM; điều tra dở, CHƯA sửa dữ liệu.
Bước tiếp theo: Xác minh nguồn tạo phiếu 447 (HRM?) → nếu bug ở HRM thì fix bên HRM; kiểm màn thật; commit + push fix ERP; user quyết cách sửa phiếu cũ.
Blocked: Chờ user quyết cách sửa dữ liệu
