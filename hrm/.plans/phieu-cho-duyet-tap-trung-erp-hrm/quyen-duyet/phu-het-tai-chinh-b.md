# Phủ hết màn duyệt — Tài chính nhóm B (Kho xuất / Yêu cầu xuất hàng) — @cuong61n

17/11/2026, nhánh gop_db-main, DB local `local_hrm_erp`, manifest `wave2-finance-b.json` (đã clean-test + xoá dòng `approval_inbox_*` thử, xác nhận 0 dòng thử còn lại).

## 1. Kiểm kê

| Luồng | Màn FE | doc_type / lý do bỏ |
|---|---|---|
| Yêu cầu xuất hàng (YCXH) | /finance/product-export-requests/{id} | `product_export_request` (3 cấp) |
| Phiếu xuất kho (PXK) | /finance/warehouse-exports/{id} | `warehouse_export` (st2) |
| Đề nghị xuất kho (ĐNXK) | /finance/warehouse-export-requests/{id} | `warehouse_export_request` (st2, thủ kho) |
| Phiếu yêu cầu chuyển hàng | /finance/product-transfer-requests/{id} | `product_transfer_request` (st2) |
| ĐNXK `cancel` | — | BỎ: chỉ nháp (3) + người lập (`WarehouseExportRequestController::assertCanCancel` :764; FE `is_can_cancel` = isDraft && isCreator, Resource :84) |
| PXK st7 "Đang hạch toán" + nút Từ chối | — | KHÔNG coi là chờ duyệt: sau khi đã lập PXH, không còn nút duyệt, `deny()` chỉ đặt 4 không hoàn tác (`WarehouseExportService::deny` :495). **Cần user chốt** |
| YCXH st14 "Chờ duyệt nhập" | — | BỎ: chỉ trạng thái theo dõi (ProductExportService:1247), không route duyệt trên YCXH; người duyệt là YCNH loại 6 (đã có `product_import_request`) |
| Phiếu xuất hàng (PXH), Phiếu nhập lại, Phiếu xuất lại, Phiếu xuất điều chỉnh kiểm kê | product-exports, warehouse-reimports, warehouse-reexports, inventory-exports | BỎ: không có route approve/reject/deny (Assign/Routes/api.php:850-899; Finance/Routes/api.php:709-718, 960-1000); các cờ chỉ là của người lập (`is_can_re_import/re_export`) |

## 2. Gate từng luồng (đọc từ code đang chạy)

- **YCXH**: st10 TP = mã `finance.xuat_hang_vuot_han_muc_cong_no_truong_phong.approve` + dòng `employee_manage_departments` (công ty GỐC người duyệt, phòng phiếu, so `=`; không phòng ngồi, không cờ all_department, không kiểm công ty phiếu), loại≠3 (`ProductExportRequest::canManagerApprove` :423). st11 BGĐ = mã BGĐ + công ty gốc = công ty phiếu, loại≠3 (:445). st2 KT kho = mã `accounting.ke_toan_kho.manage` + điều kiện công ty "chỉ chặn khi cả hai vế có giá trị và khác": "Không duyệt" so `company_id` (loại 7: `export_company_id`) (:370), lập ĐNXK/PXH xuất thẳng so `company_id` (`WarehouseExportRequestController::assertCanApprove` :908, `ProductExportController::assertCanExportFromRequest` :1731). truth() = canReject() ∨ hai cửa vào controller (gọi bằng reflection). Loại 3 (mượn) ở st10/11: không ai làm được trên HRM ⇒ `approvable=false` + blocked_reason.
- **PXK**: mã KT kho + công ty gốc = công ty phiếu (cờ `is_can_approve`/`is_can_deny` của `WarehouseExportResource` :46-47). truth() = chính hai cờ đó.
- **ĐNXK**: loại≠5 = thủ kho (`warehouse_stockers`) VÀ mã KT kho ở công ty đang làm (route `warehouse-exports` có middleware, Routes:842, + `WarehouseExportController::assertCanCreate` :414); loại 5 = chỉ thủ kho (`canCreateTransfer` Entity :201, POST /finance/warehouse-transfers không middleware) ⇒ liệt kê ở mọi công ty. Không kiểm công ty.
- **Yêu cầu chuyển hàng**: mã KT kho + công ty gốc = `company_id` phiếu (`canApprove` :241); "Không duyệt" và "Tổng hợp" cùng cờ.

## 3. Số phiếu chờ thật (local) và kết quả

| doc_type | Chờ thật | Verify (cặp / cặp duyệt thật / chênh lệch) | Đột biến | Test |
|---|---|---|---|---|
| product_export_request | 23 (st2:20, st10:1 loại mượn, st11:2) | 14.529 / 1.194 / 0 | 14/14 | 6 |
| warehouse_export | 114 | 57.000 / 5.250 / 0 | 6/6 (lần 1: 5/6, sống sót "pendingQuery thêm st7" vì DB không có PXK st7 ⇒ thêm dữ liệu test, bắt được) | 4 |
| warehouse_export_request | 119 | 59.375 / 130 / 0; riêng thủ kho × mọi công ty: 73.750 / 225 / 0 | 6/6 | 4 |
| product_transfer_request | 24 | 14.250 / 562 / 0 | 6/6 | 4 |

API thật: inbox `?doc_type=` trả dòng cho YCXH, PXK, ĐNXK, PYCCH (PYCCH: emp 432 công ty 4, 10 phiếu, `handler_path` `/finance/product-transfer-requests/7302`, API chi tiết 200); mọi `handler_path` có file `hrm-client/pages/finance/.../_id/index.vue`.

## 4. File

- Tạo: `Definitions/Finance/{ProductExportRequest,WarehouseExport,WarehouseExportRequest,ProductTransferRequest}Definition.php`; test `tests/Feature/ApprovalCenter/Finance/{…}DefinitionTest.php`.
- Sửa model (thêm trait + `approvalInboxDocType()`): `Modules/Assign/Entities/Warehouse/{ProductExportRequest,WarehouseExport,WarehouseExportRequest}.php`, `Modules/Finance/Entities/ProductTransferRequest/ProductTransferRequest.php`.
- Sửa code gốc 1 chỗ (query builder): `ProductExportRequestController::reject` — `->update()` hủy phiếu con, thêm `ApprovalInboxService::scheduleSync('product_export_request', $child->id)` cho từng con. Các `DB::table('product_transfer_requests')->update` (status 7/8/11/12: ProductExportService:1372, ProductImport:996/1201, WarehouseImportRequestService:206) chỉ chạm phiếu đã rời st2 (đã "Đã tiếp nhận") nên không cần sync.

## 5. "BE không chốt quyền" / lỗi code gốc (chỉ ghi)

1. ĐNXK: FE hiện nút "Lập phiếu xuất kho" cho mọi thủ kho (`is_can_create_warehouse_export`), nhưng POST đòi thêm mã KT kho. Local: 60 thủ kho, chỉ 8 có mã ⇒ 52 người thấy nút rồi bị 403. Definition theo điều kiện làm được thật (BE).
2. PXK/ĐNXK: API chi tiết lọc theo quyền xem theo cấp (`scopedQuery`: "Xem phiếu xuất kho theo …", `finance.de_nghi_xuat_kho.view`) — người duyệt thiếu quyền xem nhận 404 khi mở từ Trung tâm phê duyệt (YCXH và PYCCH không dính: có `canViewLikeErp`/`canView`). Chưa đo số người bị.
3. PXK: cửa vào BE (`assertCanExportGoods`, `deny`) lỏng hơn cờ FE khi phiếu không có công ty; Definition theo cờ FE.
4. YCXH st2: nút KT kho ở FE không kiểm công ty (chỉ BE kiểm) ⇒ người khác công ty thấy nút nhưng bị chặn khi mở. Loại 7: "Không duyệt" so `export_company_id` còn lập ĐNXK so `company_id` (hai vế lệch nhau nếu khác).
5. YCXH loại 3 (mượn) ở st10/11: HRM không có người duyệt (1 phiếu st10 local) — chỉ duyệt trên ERP.
6. Hạ tầng (cho điều phối): `DeliveryRequestDefinition::watchedTables` có `product_export_requests`; listener `ApprovalInboxRefresher` chạy truy vấn xen giữa INSERT và `lastInsertId()` nên `ProductExportRequest::create()` NGOÀI giao dịch trả `id = 0`. Mọi chỗ tạo YCXH thật đều trong `DB::transaction` nên chưa lỗi, nhưng seed/code mới phải bọc giao dịch.

## 6. Câu hỏi cho user

- PXK st7 "Đang hạch toán" có nút Từ chối cho KT kho: coi là chờ duyệt không? (hiện: không).
- ĐNXK: thủ kho thiếu mã KT kho — cấp mã hay sửa middleware route (BE)?
