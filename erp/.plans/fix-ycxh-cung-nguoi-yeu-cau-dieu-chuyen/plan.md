# Plan — Fix YCXH điều chuyển kho chi nhánh lọt 2 người yêu cầu khác nhau

Repo: `TanPhatDev/`. Fix bug (BE + FE). Màn: Phiếu yêu cầu xuất hàng (YCXH) loại 7 = Xuất điều chuyển kho chi nhánh.

## Bug
Chốt chặn "các phiếu yêu cầu điều chuyển trong 1 YCXH phải cùng 1 người tạo (`created_by`)" bị bọc
trong điều kiện `kind_of_import == 1 || is_export_direct`. Khi phiếu ở chế độ **Nhập về kho
(`kind_of_import = 2`)** và `is_export_direct = 0` → điều kiện false → chốt chặn KHÔNG chạy ở cả FE
lẫn BE → gom được 2 phiếu điều chuyển của 2 người khác nhau vào 1 YCXH.

Hệ quả: `transfer_requester_id = product_transfer_requests()->first()->created_by` chỉ lấy người của
phiếu đầu → màn Đề nghị xuất kho tra "giữ" sai người → hiện giữ nhưng không xuất được.

Ca thực tế xác nhận: phiếu 37984 (`kind_of_import=2`, `is_export_direct=0`) gom ptr 7566 (created_by=829)
+ ptr 7595 (created_by=597).

Bonus: hàm `update` (BE) còn hẹp hơn `store` — chỉ gate `kind_of_import == 1`, thiếu vế `is_export_direct`.

## Fix (đã chốt với user)
Bỏ điều kiện gate `kind_of_import`/`is_export_direct`, áp chốt chặn `created_by` cho **mọi** YCXH
`type == XUAT_DIEU_CHUYEN_KHO_CHI_NHANH (7)`; đồng bộ store = update + FE.

## Tasks
- [x] BE store `ProductExportRequestsController.php:667` — bỏ gate `(kind_of_import==1 || is_export_direct)`, giữ điều kiện `type == XUAT_DIEU_CHUYEN_KHO_CHI_NHANH`
- [x] BE update `ProductExportRequestsController.php:1178` — đồng bộ điều kiện như store
- [x] FE `formJs.blade.php:22` (`updateStock`) — bỏ gate, chỉ còn `form.type == 7`
- [x] FE `formJs.blade.php:219` (`chooseProductTransferRequest`) — bỏ gate, chỉ còn `form.type == 7`
- [ ] Xử lý dữ liệu phiếu 37984 đã lỡ tạo (hỏi user: sửa tay tách phiếu / bỏ 1 ptr)
- [ ] Test tay: chọn 2 ptr khác người ở kind_of_import=2 → bị chặn cả FE (khi chọn) lẫn BE (khi lưu)

## Bug #2 — Màn SỬA đề nghị xuất kho không tra được giữ (giữ hiện "-")
Ca: PDNXK-33142 (YCXH 37973, kho Liên Ninh). SL đang giữ hiện "-" dù người yêu cầu điều chuyển
(emp 828) đang giữ đủ 22 (prepick_details id 57550, company 1, cust 1553, còn hạn).

Root cause: `getDataForWarehouseExportRequest` (tạo mới) gán `parent.transfer_requester_id` = created_by
của phiếu điều chuyển (828). Nhưng `WarehouseExportRequest::getDataForEdit()` chỉ `toArray()`, KHÔNG gán
`transfer_requester_id` → FE `warehouse_export_requests/formJs.blade.php:18`
(`employee_id: form.parent.transfer_requester_id || form.parent.created_by`) rơi về `parent.created_by`
= người tạo YCXH (1119, KHÁC 828) → `getAccountingStockDetail` tra giữ theo 1119 → 0 → "-".
(BE xuất thật đã đúng vì `getTransferRequesterId()` dùng ở dòng 687; chỉ hiển thị màn Sửa sai.)

Fix: inject `transfer_requester_id` vào `parent` trong `getDataForEdit` bằng `getTransferRequesterId()`.

- [x] Điều tra & xác nhận root cause bằng data thật (giữ 57550 emp 828; YCXH created_by 1119)
- [x] FE-data BE `WarehouseExportRequest::getDataForEdit()` — gán `$result['parent']['transfer_requester_id']`
- [ ] Test tay: mở Sửa PDNXK điều chuyển → SL đang giữ hiện đúng theo người yêu cầu điều chuyển
