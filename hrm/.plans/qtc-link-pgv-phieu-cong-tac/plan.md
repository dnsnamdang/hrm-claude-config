# QTC: thêm link tới chi tiết Phiếu giao việc + Phiếu công tác

## Bối cảnh
Màn Quyết toán công (settlement_contract), bảng "III. Chi tiết quyết toán theo phiếu giao việc" (`DetailAssignTaskComponent.vue`) đang hiển thị mã "Phiếu giao việc" (`wr_assign_task_code`) và "Phiếu công tác" (`assign_business_code`) dạng **text tĩnh**, thiếu link mở màn xem chi tiết.

## Route (đã xác nhận)
- Phiếu giao việc (PGV, wr_assign_task): `/assign/assign_tasks/${wr_assign_task_id}/show`
- Phiếu công tác (assign business): `/assign/assign_business/${assign_business_id}/show`

Data có sẵn trên object `assign`: `wr_assign_task_id/code`, `assign_business_id/code` (từ `getDataForSettlementContract`).

## Tasks
- [x] Xác định component + route + id có sẵn
- [x] FE: `DetailAssignTaskComponent.vue` dòng 9-10 → bọc `nuxt-link` (target=_blank), fallback text nếu thiếu id
- [x] FE: `AssignTaskComponent.vue` (bảng II) dòng 34-35 → bọc `nuxt-link` (target=_blank), fallback text
- [ ] User verify: click mở đúng màn chi tiết PGV + phiếu công tác (tab mới) ở cả bảng II và III

## Ghi chú
- Mở tab mới (`target="_blank"`) đồng nhất với màn danh sách assign_tasks.
- Chỉ FE, không đụng BE/API. Branch `tpe`.
- Đã thêm link cho CẢ bảng II ("Quyết toán theo phiếu giao việc") và bảng III ("Chi tiết quyết toán theo phiếu giao việc").
