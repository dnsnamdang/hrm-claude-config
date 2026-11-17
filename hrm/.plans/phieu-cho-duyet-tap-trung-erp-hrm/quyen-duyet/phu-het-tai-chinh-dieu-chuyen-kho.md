# Điều chuyển kho (`warehouse_transfer`) — Trung tâm phê duyệt, đợt 2 — @cuong61n

17/11/2026. Nhóm Tài chính / Kho. Definition `hrm-api/Modules/ApprovalCenter/Definitions/Finance/WarehouseTransferDefinition.php`, test `tests/Feature/ApprovalCenter/Finance/WarehouseTransferDefinitionTest.php`, trait `SyncsApprovalInbox` đã gắn vào `Modules/Finance/Entities/WarehouseTransfer/WarehouseTransfer.php`.

## Luồng thật (đọc từ code đang chạy)
- Thủ kho lập phiếu từ Đề nghị xuất kho loại 5 (`WarehouseTransferService::store`, dòng ~69): phiếu sinh ra ĐÃ Ở "Chờ duyệt" (status 2), tồn đã di chuyển ngay.
- Kế toán kho của kho NGUỒN bấm Duyệt: `WarehouseTransferController::approve` (Finance/Routes/api.php:727) → service `approve` (2 → 1, đẩy PXK / ĐNXK / YCXH sang "Đang hạch toán"). KHÔNG có nút Từ chối.
- FE `hrm-client/pages/finance/warehouse-transfers/_id/index.vue:93,164` hiện nút Duyệt theo cờ `is_can_approve` (Controller `show`, dòng 267) = `isAccountantOf(kho nguồn) && status == 2`.
- Gate thật của endpoint (thứ tự): (1) phiếu nằm trong `scopedQuery()` = `checkPermissionListWithColumn` với 4 tên "Xem phiếu điều chuyển kho theo tổng công ty / công ty / phòng ban / bộ phận" (chọn MỨC CAO NHẤT đạt được, không cộng dồn; hết mức thì chỉ phiếu do mình lập); (2) `isAccountantOf(from_warehouse_id)` = có dòng trong bảng `warehouse_accountants` (accountant_id = employees.id); (3) status = 2. Không kiểm mã "Kế toán kho", không kiểm công ty phiếu ngoài phạm vi xem.

## Cách Definition mô phỏng
- `truth()` gọi NGUYÊN VĂN hai hàm private của controller (`scopedQuery`, `isAccountantOf`) qua reflection → luôn đúng với code gốc, không tự viết lại.
- `approvers()` = kế toán kho của kho nguồn × từng công ty đang làm (10 công ty) × phiếu có nằm trong phạm vi xem của họ ở công ty đó (mức xem lấy từ `PermissionLookup::holders` 4 tên; phòng / bộ phận quản lý lấy từ `manageDepartmentIdsOf` / `managePartIdsOf`, kể cả cờ "quản lý tất cả phòng ban"; người lập luôn thấy phiếu mình lập ở mọi công ty).
- `watchedTables`: `warehouse_accountants`, `employee_manage_departments`, `company_employees`, `employee_infos` + bộ bảng phân quyền chung. `sourceSubsystem` = `warehouse` (menu Kho › Điều chuyển).

## LỖI CODE GỐC (chỉ ghi, không sửa)
1. Gate đọc bảng `warehouse_accountants` — **RỖNG 0 dòng** ở DB gộp local (bảng sống là `accounting_warehouse_accountants`, 235 dòng / 30 người; `PrepickCancelRequestService.php:718-730` đã ghi nhận). Hệ quả: HIỆN KHÔNG AI duyệt được phiếu Điều chuyển kho trên HRM; `warehouse_transfers` cũng 0 dòng ⇒ chưa phát hiện. Definition vẫn đăng ký theo ĐÚNG gate thật (người duyệt rỗng khi chưa có dữ liệu) và ghi `gate_blocker` để màn hình nói rõ. **Cần user/người phụ trách Kho quyết**: đổi gate sang `accounting_warehouse_accountants` hay nạp dữ liệu `warehouse_accountants` (khi sửa: tăng `version()` của Definition).
2. `PhysicalWarehouseService.php:201` còn ghi/xoá `warehouse_accountants` (danh mục kho), `WarehouseImportWriteService.php:1343` và `ProductImportRequestService.php:796,1978` cũng đọc bảng này để báo thông báo ⇒ cùng gốc lỗi dữ liệu.
3. `scopedQuery` dùng tên quyền cũ + cờ `true` fallback "phiếu mình lập": kế toán kho KHÔNG có quyền xem nào chỉ thấy/duyệt được phiếu do chính mình lập (kế toán kho thường không phải người lập, thủ kho lập) ⇒ kể cả sau khi nạp bảng kế toán, phải cấp mã `warehouse.phieu_dieu_chuyen_kho.view` cho kế toán kho thì họ mới duyệt được.

## Kiểm chứng
- PHPUnit `WarehouseTransferDefinitionTest` 5 test / 76 assertion xanh. Dữ liệu dựng trong giao dịch: 4 mức xem × (kế toán / không) × (quản lý phòng của phiếu / phòng khác / bộ phận qua `part_ids`) × (công ty phiếu / công ty khác) × người lập chính mình (3 mức), người xem tổng công ty nhưng không phải kế toán, kế toán của kho khác. Số liệu: 250 cặp / 14 cặp duyệt thật (ca ma trận), 1.380 cặp / 8 cặp (6 phiếu × 3 kho), 0 chênh lệch.
- **Đột biến 7/7 bị bắt**: bỏ nhánh "phiếu mình lập" (M1), mức công ty bỏ so công ty phiếu (M2), mức phòng ban bỏ so phòng (M3), đọc mọi kế toán không lọc kho (M4), bỏ mức tổng công ty (M5), mức bộ phận bỏ phiếu mình lập (M6 — ban đầu test KHÔNG bắt được, đã bổ sung ca "xem theo bộ phận/phòng/công ty nhưng không quản lý gì, phiếu do mình lập"), bỏ mức bộ phận (M7).
- `approval-center:seed-test warehouse_transfer --count=6 --manifest=wave2-finance.json` (ghi dòng `warehouse_accountants` đánh dấu `created_at = 2001-01-01` cho kế toán kho thật) → `approval-inbox:verify warehouse_transfer --sample=300`: **18.120 cặp, 0 chênh lệch**; API thật `GET /api/v1/approval-center/inbox?doc_type=warehouse_transfer` (JWT kế toán kho id 34, công ty 1) trả 2 phiếu, `handler_path` = `/finance/warehouse-transfers/{id}` (file FE có thật). Đã `clean-test` + xoá dòng `approval_inbox_*` đóng của phiếu thử + `warehouse_accountants` về 0 dòng.
- Số phiếu chờ THẬT local: 0 (bảng rỗng).
- Điểm ghi bằng query builder: `WarehouseTransferService::approve` dùng Eloquent `save()` nên trait tự đồng bộ; các `update()` trên PXK/ĐNXK/YCXH không đụng bảng này ⇒ không cần `scheduleSync` thêm.
