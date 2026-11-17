# Phủ hết màn duyệt — Tài chính / Kho NHẬP (wave2-finance-a) — @cuong61n

Ngày 17/11/2026, nhánh gop_db-main, DB local `local_hrm_erp`. Mọi gate đọc lại từ code đang chạy. Manifest `wave2-finance-a.json` đã `clean-test` (0 phiếu thử, 0 dòng bảng gom mã `TEST.*`).

## 1. Bảng kiểm kê luồng → doc_type

| Luồng | Màn FE (có file) | doc_type / lý do bỏ | Cấp | Phiếu chờ THẬT local |
|---|---|---|---|---|
| Đề nghị nhập kho (F6) | `/warehouse/import-requests/{id}` (`/finance/warehouse-import-requests` chỉ redirect 301) | `warehouse_import_request` | 1 (status 2) | 30 |
| Phiếu nhập kho (F7) | `/finance/warehouse-imports/{id}` | `warehouse_import` | 1 (status 2) | 32 |
| Chuyển hàng nhập thẳng (F10) | `/finance/product-import-direct-transfers/{id}` | `product_import_direct_transfer` | 1 (status 2) | 1 |
| Phiếu báo hàng thừa, thiếu nhập kho | `/warehouse/exc-shortage-imports/{id}` | `exc_shortage_warehouse_import` | 1 (status 2) | 3 |
| Phiếu nhập kho điều chỉnh kiểm kê (phát hiện thêm) | `/warehouse/inventory-imports/{id}` | `warehouse_inventory_import` | 1 (status 1) | 0 |
| Hàng đợi "Phiếu nhập kho chờ báo thừa, thiếu" | `/warehouse/import-discrepancies` | BỎ: hàng đợi công việc, query = PNK đã hạch toán chưa có phiếu báo (`ExcShortageService.php:46-70`), `routes api.php:895-897` chỉ GET, FE chỉ có hành động "Báo hàng thừa thiếu" (`import-discrepancies/index.vue:303`), không Duyệt/Từ chối | — | — |
| Phiếu nhập hàng (`product_imports`) | `/finance/product-imports/{id}` | BỎ: chỉ 2 trạng thái Đang tạo(3)/Đã hoàn thành(1), không bước chờ (`ProductImport.php:58-71`) | — | — |
| Phiếu nhập hàng điều chỉnh kiểm kê (`inventory_imports`) | `/finance/inventory-imports/{id}` | BỎ: Đang tạo → "Lưu và duyệt" bởi chính người lập, không bước chờ (`InventoryImport.php:14-29`) | — | — |
| Phiếu nhập lại điều chỉnh sai số liệu | `/finance/warehouse-reimports` | BỎ: màn xem; nút duy nhất "Tạo phiếu xuất lại" là việc của người lập (`WarehouseImport::canReExport` = created_by + status 4) | — | — |
| Điều chuyển kho | — | không làm (người điều phối) | — | — |

## 2. Gate từng loại (đọc từ code)

- **warehouse_import_request**: người duyệt = thủ kho của kho phiếu (`warehouse_stockers.stocker_id = employees.id`). Cờ FE `is_can_create_warehouse_import` (Duyệt thật "Tạo phiếu nhập kho") và `is_can_deny` (Từ chối) — `WarehouseImportRequestResource.php:74-76,142-160`; endpoint deny gate `assertCanStockerApprove` `WarehouseImportRequestController.php:1030`. KHÔNG mã quyền, KHÔNG công ty ⇒ liệt kê ở mọi công ty. Loại 11 ẩn nút Từ chối nhưng vẫn có "Tạo phiếu nhập kho" ⇒ vẫn là người duyệt. Bỏ Super Admin. `truth()` = `toArray()` của Resource (2 cờ). watchedTables chỉ `warehouse_stockers`.
- **warehouse_import**: `canApprove()` (`WarehouseImport.php:258`) = loại ≠ 5 + status 2 + `accounting.ke_toan_kho.manage` (công ty đang làm) + công ty GỐC = `company_id` phiếu. `canDeny()` = canApprove trừ loại 5/6/8/10 (loại 6/8/10 chỉ còn nút Tạo phiếu nhập hàng nhưng vẫn là người duyệt). Loại 5 (điều chuyển cùng thủ kho): `approvable=false` + blocked_reason (không ai bấm được — canApprove loại trừ). Gate tạo phiếu nhập hàng `ProductImportService::resolveParent:1663` khớp. `truth()` = canApprove || canDeny.
- **product_import_direct_transfer**: `canApprove()` (`ProductImportDirectTransfer.php`) = status 2 + `accounting.ke_toan_kho.manage` + công ty gốc = company_id. Route approve/reject gate canApprove (Controller:161,179). "Người nhận" KHÔNG có bước xác nhận (xác minh lại: không route/cờ nào) — có test.
- **exc_shortage_warehouse_import**: `canApprove()` = status 2 + `warehouse.phieu_bao_hang_thua_thieu_nhap_kho.approve` + `canView()` ⇒ (người lập | công ty gốc = company_id | phạm vi xem `warehouse.xu_ly_thua_thieu_nhap_kho.view` ≥ Tổng công ty ở công ty đang làm). Cờ FE `is_can_reject`/`is_can_process` (Xử lý = mở ERP) cùng điều kiện. Bước "Đã xử lý" (3) do ERP ghi, backfill định kỳ sẽ đóng.
- **warehouse_inventory_import**: `canCreateProductImport()` = status 1 ("Chờ duyệt") + `accounting.ke_toan_kho.manage`; KHÔNG kiểm công ty. HRM không có nút Không duyệt cho phiếu này. Đăng ký theo nguyên tắc "nghi ngờ thì đăng ký" — **cần điều phối xác nhận** đây có tính là "duyệt" (nút "Tạo phiếu nhập hàng" của Kế toán kho, status tên "Chờ duyệt").

Tất cả: không chặn người lập tự duyệt (excludeOwn=false).

## 3. Kết quả kiểm chứng

| doc_type | test | Cặp (so) / cặp được duyệt thật / chênh lệch (dữ liệu local thật + phiếu thử) | Đột biến bị bắt/thử |
|---|---|---|---|
| warehouse_import_request | 6 test, 861 assertion | script riêng (toàn bộ thủ kho + 40 người ngẫu nhiên × 10 công ty × 36 phiếu): 33.480 / 2.370 / 0; test: 17.710 / 2.030 / 0 | 6/6 (đã thay 1 đột biến tương đương) |
| warehouse_import | 6 test, 561 | `approval-inbox:verify` 8.550 / 1.499 / 0 | 5/6 (1 tương đương: `approvers()` không được gọi khi approvable=false) |
| product_import_direct_transfer | 6 test, 521 | 1.575 / 326 / 0 (test 4.125 / 651) | 4/4 |
| exc_shortage_warehouse_import | 4 test, 156 | 1.953 / 411 / 0 (test 4.539 / 703) | 6/6 |
| warehouse_inventory_import | 4 test, 128 | 1.350 / 450 / 0 (test 3.300 / 900) | 4/4 |

Ghi chú: `approval-inbox:verify` không trúng thủ kho (chỉ thử người giữ mã + mẫu ngẫu nhiên) nên với `warehouse_import_request` dùng `VerifiesWithExplicitTesters` + script riêng với đúng danh sách thủ kho; test còn gọi trực tiếp `assertCanStockerApprove` (endpoint deny) bằng reflection để chốt endpoint khớp cờ.
API thật (JWT nhân viên 336, công ty 1): `GET /approval-center/inbox?doc_type=warehouse_import_request` trả 10 dòng/trang, `/inbox/counts` ra `warehouse_import_request: 18`; `handler_path` `/warehouse/import-requests/{id}` — file `pages/warehouse/import-requests/_id/index.vue` tồn tại. 4 handler_path còn lại đã kiểm file tồn tại, chưa gọi API riêng.

## 4. File tạo / sửa

Tạo: `Definitions/Finance/{WarehouseImportRequest,WarehouseImport,ProductImportDirectTransfer,ExcShortageWarehouseImport,WarehouseInventoryImport}Definition.php`, `Definitions/Finance/Concerns/WarehouseInSeedSupport.php`, 5 test `tests/Feature/ApprovalCenter/Finance/*DefinitionTest.php`.
Sửa (thêm trait `SyncsApprovalInbox` + `approvalInboxDocType()`): `WarehouseImportRequest`, `WarehouseImport`, `ProductImportDirectTransfer`, `ExcShortageWarehouseImport`, `WarehouseInventoryImport` (Modules/Finance/Entities/...).
Sửa `Modules/Finance/Services/ProductImportService.php::markParentUsed` — thêm `scheduleSync('warehouse_import', …)` (ghi `warehouse_imports.status = 7` bằng query builder: chính là bước DUYỆT THẬT của Phiếu nhập kho) và `scheduleSync('warehouse_import_request', …)` sau update WIR→7.
Đã rà, không cần thêm: `ProductImport.php:657-666` (WI 7→1, WIR→4: phiếu đã rời hộp chờ), `WarehouseTransferService.php:448` (WIR→7 sau khi PNK lưu qua Eloquent). Mọi nơi khác ghi bằng Eloquent `save()` nên trait tự đồng bộ.
Không chạy migration.

## 5. Lỗi / điểm cần lưu ý của code gốc

1. Route `POST /warehouse-import-requests/{id}/deny` KHÔNG chặn loại 11 ở BE (`assertCanStockerApprove` không loại trừ), chỉ FE ẩn nút (`Resource:76`).
2. `warehouse_import_requests`/`warehouse_imports`: bước Duyệt thật không có route HRM (mở màn tạo PNK / tạo phiếu nhập hàng); Định kỳ phải dựa trên đổi status do chính các màn đó.
3. Phiếu báo thừa thiếu: "Đã xử lý" (3) chỉ ERP ghi ⇒ phiếu nằm hộp chờ đến khi backfill định kỳ thấy status đổi; không có `updated_by`.
4. `ProductImportService::markParentUsed` ghi trạng thái bằng query builder, không để lại `updated_by` (outcome PNK dùng `approver_id`).
5. Màn Phiếu nhập kho: phiếu loại 5 ở "Chờ duyệt" không ai duyệt được trên màn này (đi qua điều chuyển kho) — đang `approvable=false`.

## 6. "BE không chốt quyền — người duyệt lấy theo điều kiện giao diện"

Không có luồng nào trong nhóm này rơi vào trường hợp đó: cả 5 đều có gate ở BE (entity/controller/service). Riêng `warehouse_import_request` BE chốt qua bảng thủ kho (không mã quyền) và route `deny` không gắn `checkPermission` — chỉ gate trong Controller.

## 7. Câu hỏi cho user / điều phối

1. `warehouse_inventory_import` (Kế toán kho "Tạo phiếu nhập hàng" ở trạng thái "Chờ duyệt", không có Từ chối): giữ trong Trung tâm phê duyệt không?
2. Label `Phiếu đề nghị nhập kho` / `Phiếu nhập kho` đặt `sourceSubsystem = warehouse` (menu Kho › Nhập kho), trong khi menu Tài chính cũng có cùng màn — điều phối cho biết nếu muốn gom vào `finance`.
