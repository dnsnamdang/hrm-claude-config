# Phủ hết màn duyệt — Tài chính nhóm D: Hạch toán dịch vụ / Phiếu báo có / Quyết toán quý — @cuong61n

Ngày 17/11/2026. Nhánh `gop_db-main`, DB local `local_hrm_erp`. Mọi gate đọc lại từ code đang chạy (Entity, Controller, Service, Route, FE hrm-client). Đường dẫn BE tính từ `hrm-api/Modules/Finance/`.

## 1. Bảng kiểm kê 6 luồng

| # | Luồng | Màn FE | doc_type / kết luận | Cấp | Gate (BE chốt quyền) | Phiếu chờ THẬT (local) |
|---|---|---|---|---|---|---|
| 1 | Yêu cầu hạch toán mua dịch vụ (F21) | `/finance/buy-service-accounting-requests/{id}` | `buy_service_accounting_request` (ĐĂNG KÝ) | 1 cấp: st2 Chờ duyệt | `status==2` + `company_id` phiếu == công ty GỐC người duyệt + mã `sale.hach_toan_mua_dich_vu.create` (công ty đang làm). 2 lớp trùng nhau: middleware route `checkPermission` cùng mã (`Routes/api.php:2301-2302`) + `canAccounting()` (`Entities/BuyServiceAccountingRequest/BuyServiceAccountingRequest.php:303-308`; controller `BuyServiceAccountingRequestController.php:239-256`) | 2 |
| 2 | Yêu cầu hạch toán dịch vụ HDDV | `/finance/wr-accounting-service-requests/{id}` | `wr_accounting_service_request` (ĐĂNG KÝ) | 1 cấp: st2 Chờ duyệt (bộ mã NGƯỢC: 1 Đã duyệt, 3 Đang tạo) | `status==2` + `company_id` == công ty gốc + mã `accounting.hach_toan_dich_vu_hddv.manage`; `canAccounting()` (`Entities/WrAccountingServiceRequest/WrAccountingServiceRequest.php:~192-197`), middleware reject `Routes/api.php:2344-2345`, controller `WrAccountingServiceRequestController.php:138-155` | 6 (còn 867 đã duyệt, 4 đang tạo) |
| 3 | Yêu cầu hạch toán dịch vụ HĐBH | `/finance/service-accounting-requests/{id}` | `service_accounting_request` (ĐĂNG KÝ) | 1 cấp: st2 Chờ duyệt (3 Không duyệt, 4 Đã duyệt không có đường ghi, 5 Đã hạch toán) | `status==2` + mã `accounting.hach_toan_yeu_cau_lam_dich_vu.create`; KHÔNG kiểm công ty/phòng phiếu (bảng không có cột công ty). Route reject khai bằng TÊN CŨ `Hạch toán yêu cầu làm dịch vụ` (`Routes/api.php:2367-2368`) — alias → mã trên (tên CÓ trong Catalog, không phải lỗi cấu hình). `canAccounting()` `Entities/ServiceAccountingRequest/ServiceAccountingRequest.php:175-179` | 17 (còn 1.275 đã hạch toán) |
| 4 | Phiếu báo có (F3) `bill_income_reports` | `/finance/bill-income-reports` | BỎ — người lập tự duyệt phiếu nháp của chính mình, không có bước chờ | Đang tạo(1) → Đã duyệt(2); không có trạng thái chờ | — (xem 2.4) | 0 (3.825/3.825 đã duyệt) |
| 5 | Quyết toán thưởng năng suất QUÝ | `/finance/bill-productivity-settlement-quarters` | BỎ — người lập tự duyệt, không có trạng thái chờ | Đang tạo(1) → Đã hạch toán(3); `st 2 Chờ duyệt` chỉ để hiển thị phiếu ERP cũ, không đường code nào đặt | — (xem 2.5) | 0 (19/19 đã hạch toán) |
| 6 | Luồng kế toán khác trong Finance | — | Không còn luồng nào chưa đăng ký (xem mục 3) | | | |

## 2. Chi tiết từng luồng

### 2.1 `buy_service_accounting_request`
- Cấp: `STATUSES` (`BuyServiceAccountingRequest.php:71-77`): 1 Đang tạo · 2 Chờ duyệt `#D97706` · 3 Đang hạch toán · 4 Đã hạch toán · 5 Không duyệt `#DC2626`. Gửi duyệt = người lập lưu với status 2 (`WRITABLE_STATUSES`, Service `afterSentForApproval` dòng ~1050).
- "Duyệt thật" = nút **Hạch toán** (`goToAccounting`, `_id/index.vue:26`) mở `/finance/buy-service-accountings`; `BuyServiceAccountingService::store` kiểm lại `$source->canAccounting()` (`Services/BuyServiceAccountingService.php:564`) rồi đặt YC → 3/4 (`setSourceStatus` :925). "Không duyệt" = `POST /{id}/reject` (lý do bắt buộc) → 5 (`BuyServiceAccountingRequestService::reject` :761-784), người lập sửa và gửi lại (5 là `isEditableStatus`).
- Hai nút FE cùng cờ `is_can_accounting` (danh sách `index.vue:641-642`, chi tiết `_id/index.vue:26,30`) ⇒ danh sách và chi tiết khớp nhau.
- Menu không gate; phạm vi danh sách: người có mã Hạch toán thấy thêm phiếu st2 cùng công ty gốc (`searchByFilter` ~dòng 366-380) — khớp gate duyệt.
- Phiếu `created_by` là VARCHAR(255) ⇒ Definition ép số cho `requester_id`.
- Không chặn người lập tự xử lý ⇒ `excludeOwn()` = false.

### 2.2 `wr_accounting_service_request`
- `STATUSES` (`WrAccountingServiceRequest.php`): 1 Đã duyệt · 2 Chờ duyệt · 3 Đang tạo. Reject → 3 (`WrAccountingServiceRequestService::reject`, lý do ở `comment`, `approver_id`/`approved_at`). "Duyệt thật" = lập Phiếu hạch toán HDDV + ghi sổ (`WrAccountingServiceService.php:~95-118`) → YC thành 1 `DA_DUYET` + `approver_id` + `approved_at`.
- Comment ở route `Routes/api.php:2331-2334` và docblock Entity ("Hạch toán chi phí = placeholder, CHƯA PORT") đã LỖI THỜI: FE `_id/index.vue:127-131` đã chuyển sang `/finance/wr-accounting-services/create?wr_accounting_service_request_id=` và màn `wr-accounting-services` có thật (menu `finance.js:317`).
- Mã quyền: Entity khai tên cũ `Hạch toán dịch vụ HDDV`, route khai mã `accounting.hach_toan_dich_vu_hddv.manage` — alias cùng 1 quyền (DB `permission_aliases`).

### 2.3 `service_accounting_request`
- Bảng KHÔNG có `company_id/department_id/part_id/customer_id` (`Entities/ServiceAccountingRequest/ServiceAccountingRequest.php:20-26`) ⇒ tổ chức của dòng bảng gom lấy theo người lập (`employeeOrg`).
- Hai nút cùng `is_can_accounting` (danh sách `index.vue:600-601`, chi tiết `_id/index.vue:24,28`): "Hạch toán dịch vụ" (mở `/finance/service-accounting/create?service_accounting_request_id=`; ở đó `store` đòi THÊM mã `customer_care.hach_toan_dich_vu_hdbh.manage`, `Routes/api.php:2396`) và "Không duyệt" (`ServiceAccountingRequestService::reject` :597-617 → 3, `comment`/`approver_id`/`approved_at`). Hạch toán xong YC thành 5 (`ServiceAccountingService.php:395-399`; `lockAccountableRequest` :270 đòi st2).
- Người duyệt của Definition = người giữ mã Hạch toán YC (đủ để "Không duyệt" và thấy nút "Hạch toán"); riêng người chỉ có mã này mà thiếu `customer_care.hach_toan_dich_vu_hdbh.manage` sẽ bị 403 khi bấm "Hạch toán dịch vụ" (lệch có sẵn, mục 4.3).
- 12/1.315 dòng có `contractable_type = NULL` (ERP cũ): `contractCode()` (`morphTo` không kiểu) sinh SQL lỗi `where service_accounting_requests.`` = 0`. Definition chỉ gọi khi có kiểu (đã có test `phieu_khong_co_kieu_hop_dong_van_mo_ta_duoc`); danh sách gốc eager-load nên không sập.
- `outcome`: 3 → từ chối; 4/5 → duyệt; phiếu thật không có đường đặt 4 (grep `DA_DUYET` không có chỗ ghi), vẫn ánh xạ phòng khi ERP ghi.

### 2.4 Phiếu báo có `bill_income_reports` — BỎ (có cân nhắc kỹ)
Bằng chứng:
1. Không có trạng thái chờ: `STATUS_CREATING = 1` Đang tạo, `STATUS_APPROVED = 2` Đã duyệt (`Entities/BillIncomeReport/BillIncomeReport.php:80-91`); lưu tạo mới luôn `status=1` rồi `doApprove` nếu bấm "Lưu và duyệt" (`Services/BillIncomeReportWriteService.php:42-60`). Không có bước "gửi duyệt".
2. BE `canApprove()` = `status==1 && can_manage` KHÔNG đòi là người lập (`Entities/BillIncomeReport/BillIncomeReportAccess.php:72-76`; `POST /{id}/approve` không middleware `Routes/api.php:476`; `BillIncomeReportController.php:115-126`) — nên về kỹ thuật kế toán khác giữ `finance.phieu_bao_co.manage` gọi API duyệt được.
3. NHƯNG phiếu Đang tạo của người khác KHÔNG ai thấy trên HRM: danh sách ẩn (`Services/BillIncomeReportService.php:52-77`, `status != 1 OR (status==1 AND created_by==me)`), chi tiết chặn (`BillIncomeReportAccess::canView` dòng 30-32 → 403; `show` `BillIncomeReportController.php:54-63`). Nút Duyệt (`is_can_approve`, list `index.vue:731-734`, chi tiết `_id/index.vue:75`) chỉ tới tay chính người lập ⇒ người bấm Duyệt == người lập (đúng quy tắc "người lập tự duyệt, không bước chờ" của phụ lục brief).
4. Nếu đăng ký: mọi phiếu NHÁP (kể cả đang soạn dở) sẽ hiện trong "Chờ tôi duyệt" của chính người soạn — sai nghĩa "chờ duyệt".
5. DB local: 3.825/3.825 phiếu đã duyệt ⇒ không có phiếu nào để thử.
Ghi nhận cho người phụ trách module: endpoint `approve` (và `toggleNotReportMoney` có kiểm canView nên ổn) nên thêm kiểm `created_by` cho khớp UI (lỗ hổng nhỏ: người có mã quản lý duyệt được phiếu nháp của người khác nếu biết id). **Câu hỏi cho user**: giữ BỎ, hay đăng ký như "BE không chốt người lập" (người duyệt = người giữ mã) — chỉ nên làm nếu nghiệp vụ muốn kế toán khác duyệt phiếu nháp (UI hiện không cho).

### 2.5 Quyết toán thưởng năng suất QUÝ `bill_productivity_settlement_quarters` — BỎ
1. `FORM_STATUSES = [1 Đang tạo, 3 Đã hạch toán]` — "Màn mới không có bước Chờ duyệt" (`Entities/BillProductivitySettlementQuarter/BillProductivitySettlementQuarter.php:38-39`; Request `Rule::in(FORM_STATUSES)` `Http/Requests/BillProductivitySettlementQuarter/BillProductivitySettlementQuarterStoreRequest.php:33`). `STATUS_WAITING_APPROVE = 2` chỉ để hiển thị phiếu ERP cũ; không đường code nào ghi 2 (grep).
2. `canApprove() = canEdit() && canCreate()` (cùng file :127-130) mà `canEdit()` = đang tạo + CHÍNH người tạo (:112-118). Middleware `CheckBillProductivitySettlementQuarterEditable` chặn mọi người không phải người tạo (403) và phiếu không còn Đang tạo (423) (`Http/Middleware/CheckBillProductivitySettlementQuarterEditable.php:22-27`), gắn vào `approve` (`Routes/api.php:1401-1402`). `WriteService::approve` (:91-97) đặt thẳng 1 → 3.
3. `canView` (dòng 84-95): phiếu Đang tạo chỉ người tạo thấy. Local: 19/19 đã hạch toán.
4. Đối chiếu sibling NĂM (`bonus_end_year_settlement`, đã đăng ký): bên đó có bước "Chờ BGĐ duyệt" (status 2) do người khác (BGĐ) duyệt; quý thì không.

## 3. Rà luồng kế toán khác trong Finance (mục 6)
Quét mọi route BE `approve|reject|deny|cancel|…` trong `Routes/api.php` và mọi trang `hrm-client/pages/finance/**` có chữ Duyệt/Từ chối:
- Đã đăng ký đợt 1/2 (không làm lại): `bill_income`, `bill_income_request`, `bill_payment`, `bill_payment_request`, `bill_adjust_dept_request`, `addition_accounting_request`, `bonus_end_year_settlement`, `buy_service_request`.
- Không có bước duyệt (bằng chứng): `bill-payment-authorizations` (UNC) — `pages/finance/bill-payment-authorizations/_id/index.vue:25-27` "KHÔNG có Duyệt / Hủy … màn này không có bước duyệt (RULING U-UNC-6)", không route approve; `closing-entries` (Routes 1407-1416 chỉ store, ghi thẳng sổ); `bill-adjust-depts` (phiếu kế toán — chỉ sửa khi nháp, không route approve); `buy-service-accountings`/`wr-accounting-services`/`service-accounting` (Phiếu hạch toán: "Lưu và duyệt" của chính người lập, `BuyServiceAccountingForm.vue:231`; không route approve riêng); `accounting-prepick-cancels` (store = duyệt hủy, `AccountingPrepickCancelForm.vue:288`; route chỉ `POST /`).
- Thuộc nhóm kho / bán hàng, không thuộc phiên này (các agent khác đang đăng ký, đã thấy file Definition): `product_transfer_request`, `warehouse_transfer`, `delivery_request`, `split/join_export_request`, `borrow_export_request`, `product_import_direct_transfer`, `exc_shortage`(reject), `sale/market-plan-employees`.
- Phiếu hạch toán (voucher) các loại KHÔNG phải màn duyệt của người khác.

## 4. Lỗi / lệch code gốc phát hiện (chỉ ghi, không sửa)
1. **HĐBH: `canView()` không tính `canAccounting()`** (khác 2 màn kia): người chỉ giữ mã Hạch toán YC mà không có quyền xem theo cấp thì mở phiếu bị 403 `show` (`Entities/ServiceAccountingRequest/ServiceAccountingRequest.php:229-266`, `ServiceAccountingRequestController::show`) và danh sách không chứa phiếu (`applyAllScope` :319-352). Đo local: 17 phiếu chờ thật × 986 cặp (người duyệt × công ty) trong bảng gom — **211 cặp (17 người) sẽ 403 khi mở**. Definition theo gate BE (`canAccounting()`), vì endpoint reject cho phép.
2. HĐBH: nút "Hạch toán dịch vụ" hiện theo mã `accounting.hach_toan_yeu_cau_lam_dich_vu.create` nhưng bước lập phiếu đòi thêm `customer_care.hach_toan_dich_vu_hdbh.manage` (`Routes/api.php:2396`) ⇒ có thể hiện nút mà bấm 403.
3. HĐBH: 12 dòng `contractable_type NULL` (xem 2.3); `ServiceAccountingRequest::contractCode()` gọi trần trên dòng này sẽ lỗi SQL.
4. Báo có: `POST bill-income-reports/{id}/approve` không đòi người lập / quyền xem (xem 2.4).
5. HDDV: comment route + docblock Entity ghi "màn Hạch toán CHƯA PORT / placeholder" nhưng đã port (xem 2.2). `WrAccountingServiceRequest` docblock còn nhắc seeder đã gỡ.
6. Buy: docblock Entity còn "id 1699-1702 trong PermissionsTableSeeder" (seeder đã gỡ 06/11/2026) — chỉ là tài liệu cũ.
7. Không có luồng nào chặn người lập tự xử lý YC ⇒ `excludeOwn()` false cả 3.

## 5. "BE không chốt quyền — người duyệt lấy theo điều kiện giao diện"
Không có loại nào phải dùng điều kiện giao diện: cả 3 loại đăng ký đều có gate BE ở endpoint reject (middleware + `canAccounting()` trong controller) và ở bước lập phiếu hạch toán. Danh sách này để TRỐNG. (Ghi chú: HĐBH có lệch xem/xử lý, mục 4.1.)

## 6. File đã tạo / sửa
- Mới: `hrm-api/Modules/ApprovalCenter/Definitions/Finance/BuyServiceAccountingRequestDefinition.php`, `WrAccountingServiceRequestDefinition.php`, `ServiceAccountingRequestDefinition.php`.
- Mới (test): `hrm-api/tests/Feature/ApprovalCenter/Finance/BuyServiceAccountingRequestDefinitionTest.php`, `WrAccountingServiceRequestDefinitionTest.php`, `ServiceAccountingRequestDefinitionTest.php` (16 test, 1.112 assertion, xanh).
- Sửa (chỉ thêm `use SyncsApprovalInbox` + `approvalInboxDocType()`): `Modules/Finance/Entities/BuyServiceAccountingRequest/BuyServiceAccountingRequest.php`, `WrAccountingServiceRequest/WrAccountingServiceRequest.php`, `ServiceAccountingRequest/ServiceAccountingRequest.php`.
- Chỗ ghi bằng query builder: KHÔNG có. Mọi ghi trạng thái của 3 bảng đều qua Eloquent (`->save()` / `forceFill()->save()`; các `lockForUpdate()->find…` chỉ để khoá rồi save): `BuyServiceAccountingRequestService` :734/766/(store/update), `BuyServiceAccountingService::setSourceStatus` :925-950, `WrAccountingServiceRequestService` :166/201, `WrAccountingServiceService` :115-120, `ServiceAccountingRequestService::reject` :597, `ServiceAccountingService` :395-399. (ERP ghi thẳng DB thì ngoài phạm vi; lệnh `approval-inbox:backfill` vớt.)
- Không chạy migration nào.

## 7. Kiểm chứng
- `vendor/bin/phpunit tests/Feature/ApprovalCenter/Finance --filter='BuyServiceAccountingRequestDefinitionTest|WrAccountingServiceRequestDefinitionTest|ServiceAccountingRequestDefinitionTest'` → OK (16 tests, 1.112 assertions).
- Phép so cờ thật (`assertDefinitionMatchesTruth`): Buy 4.320 cặp / 456 duyệt thật / 0 lệch · HDDV 4.840 / 290 / 0 · HĐBH 7.998 / 1.798 / 0.
- `approval-inbox:verify <doc_type>` với phiếu thử: Buy 3.520 cặp / 0 lệch · HDDV 5.040 / 0 · HĐBH 10.534 / 0 (CLI không in positives; positives > 0 do test).
- Đột biến (script ngoài repo, khôi phục file sau mỗi lần): Buy 7/8 bị bắt · HDDV 7/7 · HĐBH 8/8 ⇒ **22/23**. 1 lọt (Buy "bỏ ép số requester_id") là đột biến tương đương: cột `approval_inbox_items.requester_id` là số nên MySQL tự ép lại. Các kiểu đã thử: bỏ lọc công ty gốc; đổi mã quyền sang mã khác; so công ty ĐANG LÀM thay vì công ty GỐC; `pendingQuery` thêm trạng thái; `outcome` sai trạng thái từ chối/duyệt; `truth` lệch (thêm `canView`, bỏ `canAccounting`); bỏ bảng `employee_infos` khỏi `watchedTables`; bật `excludeOwn`; bỏ guard `contractable_type`; chuyển HĐBH sang lọc công ty.
- API thật (JWT nhân viên id 13 ở công ty 1, mint bằng `/tmp/mintd.php`): `GET /api/v1/approval-center/inbox?doc_type=…` trả đúng dòng (`status_text` "Chờ duyệt", `handler_path` `/finance/buy-service-accounting-requests/39`, `/finance/wr-accounting-service-requests/863`, `/finance/service-accounting-requests/3022`); `inbox/counts` có đủ 3 doc_type với nhãn + phân hệ (sale / finance / finance). 3 file `_id/index.vue` của FE tồn tại.
- Phiếu chờ THẬT trong bảng gom sau dọn: buy 2 · wr 6 · service 17 (khớp nguồn).
- Dọn: `approval-center:clean-test --manifest=wave2-finance-d.json` xoá 6+6+6 phiếu nguồn; xoá thêm 18 dòng `approval_inbox_items` trạng thái `closed` (+ assignees/logs) mang mã `TEST.YCHT%`; và 12 phiếu thử rơi vãi của `service_accounting_requests` (id 3613-3624, sinh ra do lần seed đầu lỗi `contractable_type`). Còn lại 0 dòng thử ở 3 bảng nguồn và 3 doc_type. (Có 11.774 assignee / 399 log "mồ côi" trong bảng gom — do agent khác xoá item, KHÔNG phải của phiên này.)

## 8. Câu hỏi cho user / điều phối
1. `sourceSubsystem`: Buy = `sale` (menu chính ở sale-hub › Mua dịch vụ, như `buy_service_request`); HDDV + HĐBH = `finance` (menu finance.js "Bán Dịch vụ", mã `accounting.*`) dù cũng có lối ở sale-hub › Dịch vụ. Cần user chốt nếu muốn gộp về `sale`.
2. HĐBH: giữ theo gate BE (hiện cả người không xem được phiếu — 211/986 cặp 403) hay thu hẹp thành `canAccounting() && canView()` cho đúng "thấy nút"? Cần 1 trong 2: sửa BE `canView()` thêm `|| canAccounting()` (như 2 màn kia) hoặc thu hẹp người duyệt trong Definition.
3. Báo có: giữ BỎ (khuyến nghị) hay đăng ký như phiếu "BE không chốt người lập"?
4. Chuyển người phụ trách module Finance vá: 4.1, 4.2, 4.4, 4.5.
5. Cập nhật `plan.md` / `STATUS.md` của feature do điều phối làm (phiên này không đụng file chung).
