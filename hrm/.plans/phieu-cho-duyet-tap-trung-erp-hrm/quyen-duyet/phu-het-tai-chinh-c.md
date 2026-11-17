# Phủ hết màn duyệt — Tài chính nhóm C: Xuất mượn / Tách–Ghép / Vận chuyển (17/11/2026) — @cuong61n

Phạm vi: 4 luồng. Cả 4 đều đã ĐĂNG KÝ (không bỏ luồng nào). Manifest dữ liệu thử `wave2-finance-c.json` đã `clean-test` (xem mục 7).
Đường dẫn code: `hrm-api/Modules/Finance/...` (gate), `hrm-api/Modules/ApprovalCenter/Definitions/Finance/...` (Definition), `hrm-api/tests/Feature/ApprovalCenter/Finance/...` (test).

## 1. Bảng kiểm kê

| Luồng | Màn FE (có file) | doc_type | Cấp | Gate (từ code đang chạy) | Pending thật (local) |
|---|---|---|---|---|---|
| Yêu cầu xuất hàng mượn (F19) | `pages/finance/borrow-export-requests/_id/index.vue` (nút `v-if="detail.is_can_approve"` dòng 199, 212; danh sách `index.vue:623`) | `borrow_export_request` | 1 (Chờ duyệt, status 2) | mã `accounting.ke_toan_kho.manage` ở công ty ĐANG LÀM, KHÔNG kiểm công ty phiếu | 1 (PYCXHM-00295) |
| Phiếu yêu cầu xuất tách | `pages/finance/split-export-requests/_id/index.vue` → `components/finance/split-join-export/SplitJoinRequestForm.vue:238,250` | `split_export_request` | 1 (status 2) | mã `accounting.ke_toan_kho.manage` + công ty GỐC của người duyệt = `company_id` phiếu | 0 |
| Phiếu yêu cầu xuất ghép | `pages/finance/join-export-requests/_id/index.vue` (cùng form) | `join_export_request` | 1 (status 2) | như tách (xuất thẳng cùng cờ) | 2 (YCXG-00537, YCXG-00544) |
| Yêu cầu vận chuyển, bốc xếp (F18) | `pages/finance/delivery-requests/_id/index.vue:20,24`; danh sách `index.vue:535` | `delivery_request` | 1 (status 2) | thủ kho của kho trên YCXH nguồn (`warehouse_stockers`), không mã quyền, không công ty | 0 (bảng rỗng) |

Luồng không đăng ký: không có.

## 2. Gate từng luồng (file:dòng)

### 2.1 Yêu cầu xuất hàng mượn
- `BorrowExportRequest::canApprove()` = `status == CHO_DUYET(2) && isAccountant()` — `Modules/Finance/Entities/BorrowExport/BorrowExportRequest.php:264`; `isAccountant()` = `currentEmployeeHasPermission('accounting.ke_toan_kho.manage')` (:225) → `PermissionLookup::currentHas` (quyền theo vai trò ở công ty đang làm, không còn Super Admin).
- Cả 3 chỗ dùng cùng cờ: `is_can_approve` (`Services/BorrowExportRequestService.php:161`, hiện 2 nút "Tạo phiếu xuất hàng mượn" + "Từ chối"); endpoint reject (`BorrowExportRequestController.php:132-138`, `Service::reject:661`); lập Phiếu xuất mượn = duyệt thật (`BorrowExportService.php:370`, ghi `status=1`, `approver_id`, `approved_time` ở :593-595).
- Route reject (`routes/api.php:2167`) không middleware, không dueConfig. Không chặn người lập tự duyệt.
- Lệch có sẵn: tab `for-approve` của danh sách lọc thêm `company_id` = công ty gốc người xem (`BorrowExportRequest.php` hàm `searchByFilter`), nhưng nút/endpoint thì KHÔNG kiểm công ty. Definition theo nút/endpoint (cái quyết định "duyệt được").
- Vòng đời: 2 → 1 Đã duyệt (APPROVED) | 4 Không duyệt (REJECTED, lý do ở `comment`). `3 Đang tạo` chỉ còn ở dữ liệu cũ (không sinh mới).

### 2.2 Tách / Ghép
- Cả 2 Entity dùng trait `SplitJoinExportRequestCommon`: `canApprove()` = `status == CHO_DUYET(2) && sameCompanyAsCurrent($company_id) && isAccountant()` — `Entities/SplitJoinExport/Concerns/SplitJoinExportRequestCommon.php:170`. `sameCompanyAsCurrent` so với công ty GỐC (`employee_infos.company_id`), còn mã quyền theo công ty ĐANG LÀM (kiêm nhiệm: mã ở công ty A, gốc ở B vẫn duyệt được phiếu của B khi đang làm ở A).
- Dùng cho: `is_can_approve` + `approve_link` ("Tạo đề nghị xuất kho" / ghép xuất thẳng "Tạo phiếu xuất hàng") (`Services/SplitJoinExportRequestService.php:112,179,189`); reject (`Controller:187-190`, `Service:801`); lập ĐNXK (`SplitJoinWarehouseExportService.php:92`); PXH xuất thẳng (`Assign/.../ProductExportController.php:1699`). Route còn gắn `checkPermission:accounting.ke_toan_kho.manage` (`routes/api.php:2186-2196`) — cùng mã nên không thu hẹp thêm.
- Từ chối → về `3 Đang tạo` kèm `comment` (`Service::reject:806`), không ghi `approver_id`. Lập ĐNXK → 7/1; PXH thẳng → 8 (`SplitJoinWarehouseExportService.php:296,349,387`).
- Danh sách tab `for_approve` cũng lọc đúng `company_id` = công ty gốc + `isAccountant` ⇒ khớp nút (khác borrow).

### 2.3 Yêu cầu vận chuyển
- `DeliveryRequest::canApprove()` = `status == 2 && isCurrentStocker()` — `Entities/DeliveryRequest/DeliveryRequest.php:430`; `isCurrentStocker()` (:337) = id người đăng nhập ∈ `stockerIdsOfExportRequest(objectable_id)` (:354) = `product_export_requests.warehouse_id` → `warehouse_stockers.stocker_id`. Docblock còn nhắc "hoặc Super admin" nhưng code KHÔNG có nhánh này (đã bỏ).
- Cùng cờ cho `is_can_approve` (`Transformers/DeliveryRequestResource/DeliveryRequestListResource.php:44`, `DetailResource:71`) và endpoint approve/reject (`Controller:149-170`). Không công ty, không mã quyền, không dueConfig.
- Duyệt → 3 (+ ghi `product_export_requests.transition_type = 2` bằng query builder, đó là bảng KHÁC, không phải phiếu nguồn); từ chối → 4 (`approver_comment`).
- `objectable_type` khác chuỗi ERP `App\Model\Warehouse\ProductExportRequest` ⇒ `isCurrentStocker()` false cho mọi người ⇒ Definition trả approvers `[]`.

## 3. Đăng ký (file đã tạo)
- `Definitions/Finance/BorrowExportRequestDefinition.php` — `permissionApprovers(code)` (mọi công ty có người giữ mã).
- `Definitions/Finance/SplitExportRequestDefinition.php`, `JoinExportRequestDefinition.php` + trait `Definitions/Finance/Concerns/SplitJoinExportApprovalSupport.php` (dùng chung vì 2 Entity chung gate) — `sameHomeCompanyApprovers`.
- `Definitions/Finance/DeliveryRequestDefinition.php` — người DÍCH DANH liệt kê cho MỌI công ty (`allCompanyIds()`, mẫu `ProductImportRequestDefinition`), chỉ lấy `stocker_id` có trong `employees` (DB local có 1 dòng `warehouse_stockers` id 75 trỏ nhân viên 654 không tồn tại).
- Model đã gắn trait `SyncsApprovalInbox` + `approvalInboxDocType()`: `BorrowExportRequest`, `SplitExportRequest`, `JoinExportRequest`, `DeliveryRequest`.
- `watchedTables()`: borrow = bộ mặc định + `company_employees`; tách/ghép = mặc định + `company_employees`, `employee_infos`; vận chuyển = `warehouse_stockers`, `product_export_requests` (kho trên YCXH có thể đổi). Lưu ý: `product_export_requests` là bảng ghi nhiều ⇒ mỗi lần ghi chỉ đánh dấu bẩn + sync lại các phiếu vận chuyển đang chờ (ít) sau commit.
- Ghi bằng query builder: đã rà `grep` toàn `app/`, `Modules/` — KHÔNG có chỗ nào ghi trạng thái của 4 bảng này bằng `DB::table()->update` / `Model::query()->update`; mọi đường (Service, Controller Assign, SplitJoinImportService, ProductExportService) đều `$model->status = …; ->save()` ⇒ trait tự sync. Không cần `scheduleSync` tường minh. (Seeder test cũ `BorrowExportRequestTestDataSeeder` dùng `DB::table()->insertGetId` nhưng chỉ chạy tay ở local, không phải đường chạy thật.)
- Không sửa file dùng chung nào của ApprovalCenter. Không chạy migration.

## 4. Kiểm chứng

| doc_type | test | verify (lệnh `approval-inbox:verify`) | cặp / cặp duyệt thật (test) | đột biến |
|---|---|---|---|---|
| borrow_export_request | 4 test OK | 0 chênh lệch (3.325 cặp, 525 dương) | 3.025 / 825 | 8/8 bị bắt |
| split_export_request | 4 test OK | 0 chênh lệch (2.850 cặp, 272 dương) | 3.250 / 205–379 | 8/8 (chạy chung với join) |
| join_export_request | 5 test OK (thêm ca xuất thẳng = thường) | 0 chênh lệch (3.800 cặp, 350 dương) | 3.900 / 303–407 | 8/8 |
| delivery_request | 5 test OK | lệnh verify báo 0 chênh lệch nhưng chỉ chọn người giữ mã + mẫu ngẫu nhiên nên gần như không trúng thủ kho (12 dương) ⇒ dùng `VerifiesWithExplicitTesters` với toàn bộ thủ kho: 3.540 cặp / 260 dương / 0 chênh lệch | 6.790 / 250 | 8/8 |

Lệnh: `cd hrm-api && vendor/bin/phpunit tests/Feature/ApprovalCenter/Finance --filter='BorrowExportRequestDefinitionTest|SplitExportRequestDefinitionTest|JoinExportRequestDefinitionTest|DeliveryRequestDefinitionTest'` → 18 test, 1.459 assertion, OK.

Đột biến (mỗi cái khôi phục file ngay sau, đã `php -l` sau khôi phục):
- Borrow: B1 thêm điều kiện công ty gốc · B2 đổi mã quyền · B3 pendingQuery thêm status 3 · B4 describe bỏ điều kiện trạng thái · B5 chỉ công ty của phiếu · B6 outcome từ chối→duyệt · B7 bật excludeOwn · B8 pendingQuery bỏ điều kiện trạng thái. Lần đầu B3 SỐNG (DB local không có phiếu nháp nên so pendingQuery↔describe không thấy khác biệt) → đã bổ sung ca dựng sẵn mỗi trạng thái 1 phiếu, thử lại bị bắt.
- Tách/Ghép: S1 bỏ công ty gốc · S2 đổi mã · S3 pendingQuery thêm Đang tạo · S4 so công ty bằng phòng ban · S5 describe bỏ điều kiện trạng thái · S6 outcome Đang tạo→duyệt · S7 lọc theo công ty đang làm thay công ty gốc · S8 pendingQuery thêm "Đã đề nghị". Cũng bổ sung dựng sẵn từng trạng thái.
- Vận chuyển: D1 chỉ công ty đầu · D2 bỏ lọc nhân viên tồn tại · D3 thêm người giữ mã KT kho · D4 bỏ kiểm `objectable_type` · D5 pendingQuery thêm nháp · D6 chỉ công ty của phiếu · D7 bỏ theo dõi `warehouse_stockers` · D8 lấy thủ kho theo id phiếu thay vì YCXH nguồn.
- Tổng: 24 thử, 24 bị bắt (sau khi bổ sung ca cho B3).

API thật (`http://127.0.0.1:8000`, JWT mint bằng tinker): `GET /approval-center/inbox?doc_type=borrow_export_request` (nhân viên 13, công ty 1) → 7 phiếu (1 thật + 6 thử), `handler_path=/finance/borrow-export-requests/{id}`; `join_export_request` → 6 phiếu `/finance/join-export-requests/{id}` (nhân viên 13 công ty gốc 1; 2 phiếu thử ở công ty khác không thuộc nhân viên này — đúng gate); `delivery_request` (thủ kho nhân viên 73) → 1 phiếu `/finance/delivery-requests/{id}`; `/inbox/counts` có đúng `by_doc_type`. 4 file `_id/index.vue` đều tồn tại.

## 5. Lỗi / lệch của code gốc (chỉ ghi, không sửa)
1. Docblock `DeliveryRequest.php` (đoạn trên `canApprove`) vẫn ghi "hoặc Super admin như ERP" nhưng code không còn nhánh đó — nên sửa comment.
2. `DeliveryRequest::isCurrentStocker()` memoize trong biến static `$stockerCache` theo "phiếu:nhân viên": tiến trình sống lâu (queue/worker) đổi thủ kho vẫn đọc kết quả cũ; test phải reset bằng reflection.
3. Danh sách tab `for-approve` của Yêu cầu xuất hàng mượn lọc thêm công ty gốc, còn nút Từ chối / lập phiếu xuất mượn thì không — người đúng quyền nhưng khác công ty không thấy phiếu ở tab nhưng vẫn duyệt được nếu có link (và nay thấy ở Trung tâm phê duyệt). Cần user chốt có muốn kiểm công ty ở `canApprove()` không.
4. `warehouse_stockers` local có 1 dòng (id 75, kho 19) trỏ nhân viên 654 không tồn tại.
5. Route xuất mượn/tách/ghép: `checkPermission:accounting.ke_toan_kho.manage` ở route tách/ghép nhưng route reject xuất mượn không gắn middleware (chỉ canApprove trong controller) — vẫn an toàn nhờ canApprove (423), chỉ ghi nhận.

## 6. Danh sách "BE không chốt quyền — điều kiện giao diện"
Không có luồng nào trong nhóm C rơi vào trường hợp này: cả 4 đều có cờ BE `canApprove()` chốt ở endpoint (mục 2).

## 7. Dọn dữ liệu thử
`approval-center:clean-test --manifest=wave2-finance-c.json` → xoá 6+6+6+6 phiếu nguồn; sau đó xoá tay (SQL, chỉ doc_type của tôi + `code like 'TEST.%'`) 24 dòng `approval_inbox_items` trạng thái 5 + 48 dòng `approval_inbox_logs` còn lại (clean-test chỉ đóng chứ không xoá dòng gom). Kiểm: 4 bảng nguồn 0 dòng `TEST`, `delivery_requests` = 0, `warehouse_stockers` = 80 (nguyên), vai trò `TEST-APPROVAL-CENTER*` = 0. Còn lại trong bảng gom chỉ 3 phiếu chờ THẬT (borrow 1, join 2). Có 11.774 dòng `approval_inbox_assignees` mồ côi (item_id 6067–8862) — KHÔNG phải của nhóm này (có từ trước).

## 8. Luồng khác trong nhóm kho thấy có Duyệt/Từ chối (để điều phối, chưa làm)
Tại thời điểm 17/11 chưa thấy Definition (kiểm `ls Definitions/**`; các loại `warehouse_import`, `warehouse_import_request`, `warehouse_transfer`, `product_import_direct_transfer`, `exc_shortage_warehouse_import` đã có người đăng ký):
- Yêu cầu chuyển hàng `product_transfer_requests` — `Finance routes/api.php:346` (reject), gate KT kho + cùng công ty (`ProductTransferRequest.php:241-253` theo báo cáo cũ 14.5).
- YCXH (Assign `product_export_requests`) vượt hạn mức TP/BGĐ (`Assign routes/api.php:794-800`: `reject`, `manager-approve`) và "Không duyệt" bởi KT kho (báo cáo cũ 14.7).
- Phiếu xuất kho `warehouse_exports` có `deny` (`Assign routes/api.php:887`) và Đề nghị xuất kho `warehouse_export_requests` có `cancel` (:846) — kiểm lại xem có thuộc nhóm nào.
- `borrow_exports` / `borrow_sells` (Phiếu xuất hàng mượn / xuất bán hàng mượn) KHÔNG có trạng thái chờ riêng (chỉ list/store/show, `routes/api.php:2227-2245`, `1561-1566`): lập phiếu chính là bước duyệt của phiếu yêu cầu tương ứng ⇒ không cần đăng ký.

## 9. Câu hỏi cho user
1. Xuất hàng mượn: giữ Definition theo nút (không kiểm công ty) hay muốn thêm điều kiện công ty như tab `for-approve`? (hiện đang theo nút, đúng hành vi code.)
2. Vận chuyển: chấp nhận liệt kê thủ kho ở mọi công ty (đúng code) hay muốn giới hạn theo công ty của kho?
