# Phủ hết màn duyệt — Tài chính (E): Kế hoạch NV · Phân chia thị trường phòng ban · Rà 18 loại đợt 1 — @cuong61n

Ngày 17/11/2026. Manifest dọn thử: `wave2-finance-e.json`. Không chạy migration nào. Không Playwright.

## 1. Phần 1 + 2 — đã có người làm song song (nhóm Bán hàng A), chỉ đối chiếu

Khi bắt đầu, `Definitions/Sale/` đã có `SaleEmployeePlanDefinition`, `MarketEmployeePlanDefinition` (+ trait `Support/EmployeePlanApproval.php`) và test `tests/Feature/ApprovalCenter/Sale/EmployeePlanDefinitionTest.php`. Báo cáo của họ: `phu-het-ban-hang-a-ke-hoach-nv.md` (đã chạy migration `2026_11_14_000001_add_hrm_columns_to_employee_plans`). **Không làm trùng.** Việc tôi làm:

- **`sale_plan_employee` / `market_plan_employee`** — đọc lại `EmployeePlan.php` đang chạy (`canApprove` :331, `canSendDirector` :341, `canView` :294, `approvableDepartmentIds` :207, `isHeadOfPlan` :289) đối chiếu `EmployeePlanApproval.php`: 2 cấp (Chờ TP duyệt = Duyệt/Từ chối; TP đã duyệt = Gửi BGĐ + `canView`), chỉ phiếu `form_version = 2`, loại người lập, phòng = (dòng `employee_manage_departments` ở bất kỳ công ty) ∪ (phòng đang ngồi), mã duyệt ở công ty đang làm. **Khớp code.** Cấp BGĐ (status 4/5) không có màn HRM (route chỉ `send/approve/reject/send-director/cancel`, api.php ~1869-1871) ⇒ đúng khi không đăng ký. Pending thật local = **0** (toàn bộ 1.250 phiếu là `form_version = 1` của ERP).
- **`division_market_department`** (Phân chia thị trường theo phòng ban): tôi phân tích song song và **tới cùng kết luận ĐĂNG KÝ**, thậm chí tôi đã viết `DivisionMarketDepartmentDefinition.php` trước khi thấy nhóm Bán hàng cũng thêm trait vào model — họ giữ nguyên file đó và viết test (`Sale/DivisionMarketDepartmentDefinitionTest.php`), nên tôi không sửa thêm. Lập luận (code đang chạy):
  - Phiếu chỉ có `1 Đang tạo → 2 Đã duyệt` (`DivisionMarketDepartment.php` STATUS_*), route `approve`/`un-approve` chỉ gắn `checkPermission` mã duyệt (api.php 1758-1759), `changeStatus` KHÔNG kiểm canView / công ty (Controller `changeStatus`).
  - Nút **Duyệt** (list `divisionMarketActionsMixin.js:25`, chi tiết `DivisionMarketDepartmentForm.vue:385`) = `is_can_approve` = `canApprove()` = chưa duyệt + mã `sale.phan_chia_thi_truong_phong_ban.approve` ở công ty đang làm, **trên mọi phiếu Đang tạo**, và chỉ hiện nếu người dùng THẤY phiếu (`canView`/`applyViewScope`: xem tổng công ty · người lập · xem công ty + công ty gốc). Người duyệt có thể ≠ người lập ⇒ đăng ký, `truth = canView() && canApprove()`.
  - Menu không gắn quyền (`sale-hub.js` ~326).
  - **Điều phối cần chốt**: bản nháp người lập chưa xong cũng nằm trong hàng chờ (BE không có bước "gửi duyệt"); muốn thu hẹp phải thêm bước gửi duyệt ở BE. Pending thật local: 0 (13 phiếu đều Đã duyệt).
  - BE không chốt quyền (approve không kiểm canView/công ty phiếu) ⇒ người duyệt lấy theo điều kiện giao diện — đã ghi trong docblock.

## 2. Phần 3 — rà 18 loại đợt 1 so với code đang chạy

Cách rà: (a) chạy lại toàn bộ test nhóm Finance trên code hiện tại (88 test, mọi loại đợt 1 vẫn khớp `truth()` — riêng `WarehouseTransferDefinitionTest` là của agent khác); (b) đọc lại từng Entity `can*()` / Controller endpoint / Resource `is_can_*` / nút FE và so với tập trạng thái chờ + cổng trong Definition; (c) quét mọi chỗ ghi bằng query builder vào 18 bảng nguồn; (d) kiểm `watchedTables()`; (e) kiểm `handler_path` tồn tại trong `hrm-client/pages` (cả 18 + 3 loại Bán hàng đều có `_id/index.vue`).

| # | doc_type | Đã kiểm gì | Kết quả |
|---|---|---|---|
| 1 | `addition_accounting_request` | st2; nút Từ chối (`canReject` :694) + Lập phiếu KT (`canCreateAccountingBill` :707) = truth; ghi builder `BillAdjustDeptSourceService` :766/:875 đã `scheduleSync` | Đúng |
| 2 | `bill_adjust_dept_request` | st2; `canReject` :479 / `canCreateAccounting` :505; ghi builder :905 đã `scheduleSync` | Đúng |
| 3 | `bill_income` (Phiếu thu) | st2; `canApprove` :217 | Đúng + **thêm `company_employees` vào watchedTables** |
| 4 | `bill_income_request` (**F22**) | HRM CÓ cả 2 hướng: **Duyệt = Tạo phiếu thu** (`canCreateBillIncome` :633 ⊂ `canReject`) và **Không duyệt** (`changeStatus`, Controller :195). truth = `canReject` (:618) bao cả hai (phiếu đã có phiếu thu nháp vẫn Không duyệt được). Ghi builder `BillIncomeWriteService` :99 đã sync; `BillIncomeApprovalService` :85/:172 chỉ chạy khi phiếu đã rời st2 | **Đủ** + thêm watch `company_employees` |
| 5 | `bill_payment` (Phiếu chi) | st5 KT trưởng → st2 Thủ quỹ; `canApprove` | Đúng (đã có watch) |
| 6 | `bill_payment_request` | st2→st5 đủ; **st6 "Chờ tạo phiếu chi"**: đợt 1 bỏ vì "không có nút Duyệt" — nhưng chi tiết CÓ **Từ chối** (`is_can_cancel` = `canCancel()` = `canApproveAtCurrentStatus()`, `BillPaymentRequestForm.vue:289`, endpoint `changeStatus`) và **Tạo phiếu chi / Tạo ủy nhiệm chi** (`:262/:271`) cho kế toán thanh toán ⇒ cùng khuôn F22 | **ĐÃ SỬA v2**: thêm bước 5 (st6): `finance.ke_toan_thanh_toan.manage` + cùng công ty gốc (khớp `canApproveAtCurrentStatus` st6), tiền = cột `payment_money_chief_accountant`; sửa `outcome`/`lastAction`. Thêm 3 chỗ `scheduleSync` (xem mục 4) |
| 7 | `bonus_end_year_settlement` | st2 BGĐ, tên quyền cũ qua alias, `canApprove` :266 | Đúng + thêm watch `company_employees` |
| 8 | `borrow_extend_request` | st4 TP (K3) → st5 BGĐ → st2 KT kho; `canApproveAnyLevel` :261 | Đúng |
| 9 | `borrow_sell_request` (**F16**) | Đọc lại `BorrowSellRequest.php` 143-190 + Controller 181-220: st10 TP (`canManagerApprove` K4 `currentManagedDepartmentIds`, nút Duyệt + Chuyển BGĐ `switch-board-of-manager`) · st11 BGĐ (`canBoardOfManagerApprove`) · st2 KT kho (`canApprove`, = lập phiếu xuất bán hàng mượn) · Không duyệt = `canDeny` (hợp 3). Cả 3 cấp có trên HRM | **Đủ** — không cần sửa |
| 10 | `buy_service_request` | st2 TP (`canDepartmentApprove`) + st3 KS (`canKsApprove`, cùng công ty gốc); `reject` Controller :312 dùng đúng 2 cờ. `send-ks-approve-again`, `cancel`, "Lập hợp đồng" là việc của người lập (`created_by`) ⇒ không phải duyệt | Đúng |
| 11 | `inventory_audit_report` | st1 "Chờ duyệt" `canApprove` :199 | Đúng + thêm watch |
| 12 | `position_inventory_result` | st2 `canApprove` :234. st4 "Chờ xử lý"/st5 "Đang xử lý" chỉ có `canHandle` (:240) / `canTransfer` (:262) / `is_can_complete` (`PositionInventoryResultService.php:218`) = hàng đợi công việc (lập phiếu điều chuyển/nhập/xuất điều chỉnh, bấm Hoàn thành), **không có Duyệt/Từ chối** | Đúng (phần xử lý bỏ có bằng chứng) + thêm watch |
| 13 | `prepick_cancel_request` (**F11**) | Đọc lại `PrepickCancelRequest.php` :215-224 + routes api.php 1059-1083 + `PrepickCancelRequestController::reject` :184: **Duyệt = Lập phiếu hủy giữ** (`POST /prepick-cancels`, `PrepickCancelService::store` kiểm lại `canApprove`), **Không duyệt = `/reject`**; FE nút Duyệt (`PrepickCancelRequestForm.vue:346`, list :630) + Không duyệt. `canView` luôn đúng với người có mã ở phiếu ≠ Đang tạo. Ghi `PrepickCancelService` :357 qua Eloquent | **Đủ** + thêm watch |
| 14 | `prepick_extend_request` | 3 cấp TP (K2) → BGĐ → KT; `canApproveAnyLevel` :250 | Đúng |
| 15 | `prepick_transfer_request` | như trên, TP xét phòng NGƯỜI NHẬN | Đúng |
| 16 | `product_import_request` | 4 cấp st12/st10/st11/st2 + nhập thẳng + ngoại lệ định danh loại 6/7: khớp `canApprove` :1078, `canApproveByManager` :1113, `canControlBoardApprove` :1122, `canBoardOfManagerApprove` :1131, `canProductImport` :1140, `canDeny` :1154; `canSupplierReturn` :939 là của người lập (Đã hạch toán) ⇒ không phải duyệt; builder `ProductImportService` :2581/:3657 đã sync | Đúng + thêm watch |
| 17 | `product_prepick_request` | 3 cấp; truth = `canReject` :406 (= mọi cấp ∪ KT st2 Lập phiếu xuất giữ / Từ chối); st5 "Đang xuất giữ" là xử lý kho | Đúng |
| 18 | `self_inventory` | st2 `canApprove` :234. st4/st5 = hàng đợi xử lý chênh lệch (`canHandle` :240, `canTransfer`, `canInventoryImport/Export`), không Duyệt/Từ chối | Đúng + thêm watch |

**Phát hiện chung (lỗi của đợt 1, đã sửa)**: 8/18 Definition (`bill_income`, `bill_income_request`, `bonus_end_year_settlement`, `inventory_audit_report`, `position_inventory_result`, `prepick_cancel_request`, `product_import_request`, `self_inventory`) **không khai `watchedTables()`** nên mặc định chỉ nghe bảng vai trò/quyền. Người duyệt tính bằng `PermissionLookup::holders()` → `PermissionChecker::holdersQuery` JOIN `company_employees` (chỉ tính người ĐANG LÀM việc ở công ty có Vai trò). Thêm / bớt nhân viên khỏi công ty ⇒ bảng gom KHÔNG đổi theo. Đã thêm `watchedTables() = parent + ['company_employees']` cho cả 8 (không đổi cách tính ⇒ không tăng `version()`).

## 3. File đã tạo / sửa

Sửa (Definition, chỉ nhóm tôi):
- `Modules/ApprovalCenter/Definitions/Finance/BillPaymentRequestDefinition.php` — v2, bước 5.
- `Definitions/Finance/{BillIncome,BillIncomeRequest,BonusEndYearSettlement,InventoryAuditReport,PositionInventoryResult,PrepickCancelRequest,ProductImportRequest,SelfInventory}Definition.php` — thêm `watchedTables()`.

Sửa (code nghiệp vụ — chỉ thêm `scheduleSync`, không đổi hành vi):
- `Modules/Finance/Services/BillPaymentWriteService.php` (sau `update` → st7 "Chờ duyệt phiếu chi", ~:373)
- `Modules/Finance/Services/BillPaymentApprovalFlowService.php` (2 chỗ: → st8 ~:259, → st9 Hủy ~:356)
- `Modules/Finance/Services/BillPaymentAuthorizationWriteService.php` (→ st8 ~:299)

Đây là 4 chỗ ghi `bill_payment_requests.status` bằng `BillPaymentRequest::query()->…->update()`. Đợt 1 không cần (phiếu đã rời hộp chờ ở st6) nhưng nay st6 là một cấp chờ nên phải sync khi rời st6.

Test:
- `tests/Feature/ApprovalCenter/Finance/BillPaymentRequestDefinitionTest.php` — cập nhật vòng đời (st6 = cấp 5 rồi st7 đóng), thêm ca `cap_5_cho_tao_phieu_chi_chi_gom_ke_toan_thanh_toan_cung_cong_ty_goc_va_tu_choi_dong_phieu` (3 người dựng bằng `grantRole`: KTTT cùng công ty gốc / KTTT công ty gốc khác / chỉ có mã KT trưởng; đối soát `assertEmployeeMatchesTruth`), mở rộng phép so sang 5 cấp.
- `tests/Feature/ApprovalCenter/Finance/FinanceWatchCompanyEmployeesTest.php` (MỚI): (1) tĩnh — 18 loại đều có `company_employees` trong `watchedTables()`; (2) hành vi thật — bớt/thêm dòng `company_employees` của 1 người duyệt rồi `ApprovalInboxRefresher::refreshNow()` ⇒ phiếu mất / hiện lại (đại diện `bill_income_request`, `self_inventory`; ghi + sync nhiều loại rất nặng trên DB dùng chung nên chỉ thử 2 loại).

## 4. Số liệu kiểm chứng

- `bill_payment_request` (loại duy nhất đổi logic): `approval-center:seed-test … --count=10 --manifest=wave2-finance-e.json` rồi `approval-inbox:verify bill_payment_request` ⇒ **75.558 cặp / 147 phiếu chờ / chênh lệch 0** (phép so PHPUnit: 23.868 cặp, 2.146 cặp được duyệt thật).
- API thật (JWT nhân viên 13, công ty 1): `GET /api/v1/approval-center/inbox?doc_type=bill_payment_request` = 130 phiếu (80 cấp 5 "Chờ tạo phiếu chi", 15 cấp 3, 5 cấp 2…), `handler_path` = `/finance/bill-payment-requests/{id}` (có `pages/finance/bill-payment-requests/_id/index.vue`); `/inbox/counts` → `by_doc_type.bill_payment_request.count = 130`.
- Phiếu chờ THẬT trong DB local (không tính phiếu thử): đề nghị thanh toán **133** (trước 40: +93 phiếu st6), hạch toán bổ sung 45, điều chỉnh công nợ 49, yêu cầu nhập hàng 35, phiếu thu 8, xuất giữ 8, điều chuyển hàng giữ 4, thu tiền 4, gia hạn hàng mượn 3, gia hạn hàng giữ 3, phiếu chi 2, xuất bán hàng mượn 1; còn lại (quyết toán thưởng, mua dịch vụ, kiểm kê ×2, biên bản, hủy giữ) 0; kế hoạch NV ×2 và phân chia TT phòng ban 0.

## 5. Kiểm thử đột biến (khôi phục file sau mỗi lần, `diff` xác nhận)

| Đột biến | Test | Kết quả |
|---|---|---|
| Bước 5 bỏ kiểm công ty gốc (dùng `permissionApprovers`) | BillPaymentRequestDefinitionTest | BẮT (2 fail) |
| Bước 5 đổi mã sang KT trưởng | idem | BẮT (2 fail) |
| Bỏ bước 5 khỏi STEPS | idem | BẮT (1 fail + 1 error) |
| Bỏ `company_employees` khỏi BillIncomeRequest | FinanceWatchCompanyEmployeesTest (tĩnh) | BẮT |
| Bỏ `company_employees` khỏi ProductImportRequest | idem | BẮT |
| Bỏ `company_employees` khỏi SelfInventory | idem (hành vi thật) | BẮT |

**6/6 bị bắt.** (Phần 1–2 do nhóm Bán hàng đã đột biến: 6/6 và 4/4, xem báo cáo của họ.)

## 6. Chỗ ghi bằng query builder đã xử lý

Đã có từ đợt 1 (rà lại bằng script quét mọi `Model::query()->…->update/…` và `table('…')->update/insert/delete` của 18 bảng — không phát hiện chỗ mới): `BillIncomeWriteService` :99, `BillAdjustDeptSourceService` :766/:875/:905, `ProductImportService` :2581/:3657. Mới trong lần này: 4 chỗ `bill_payment_requests` ở mục 3. Còn lại hợp lệ không cần: `BillIncomeApprovalService` :85/:172 (phiếu đã rời st2), `BillPaymentWriteService` :572 (cột tổng).

## 7. Lỗi / lệch code gốc (chỉ ghi, không sửa)

1. Đề nghị thanh toán st6: `canApproveAtCurrentStatus()` đúng cho kế toán thanh toán nhưng danh sách (`BillPaymentRequestListResource` ~:113) loại st6 khỏi `is_can_approve` ⇒ danh sách không có nút Duyệt/Từ chối ở st6, chỉ chi tiết mới có "Từ chối" — lệch giữa danh sách và chi tiết (skill list-page 7.2).
2. Đề nghị thu tiền `changeStatus` (Controller :195) chỉ kiểm `isAccountant()` + st2, không gọi `canReject()` / công ty (đã nêu đợt 1).
3. Docblock Entity còn ghi "Super Admin bỏ qua ràng buộc phòng ban" (`PrepickExtendRequest` :234, `PrepickTransferRequest` :265, `ProductPrepickRequest` :381) trong khi code đã bỏ đặc quyền — chỉ là chú thích lạc hậu.
4. `division_market_departments`: endpoint approve/un-approve không kiểm công ty phiếu / canView, chỉ checkPermission.
5. Thiếu watch `company_employees` ở 8 Definition đợt 1 (đã sửa, mục 2).

## 8. Việc cần người điều phối quyết

- **Đề nghị thanh toán st6**: số phiếu chờ thật tăng từ 40 → 133 (93 phiếu st6, phần lớn là phiếu cũ từ ERP chưa lập phiếu chi). Nếu không muốn phiếu cũ ngập hộp chờ thì cần giới hạn theo ngày — chưa tự làm vì không có căn cứ trong code gốc.
- **`division_market_department`**: nháp chưa gửi cũng vào hàng chờ (xem mục 1) — quyết giữ hay thêm bước "Gửi duyệt" ở BE.
- **Position/Self inventory st4–st5 "Chờ xử lý / Đang xử lý"**: tôi bỏ (hàng đợi công việc thuần, không Duyệt/Từ chối). Nếu muốn hiện "việc cần xử lý" trong Trung tâm phê duyệt phải quyết thêm.
- Không cần sửa file dùng chung nào của module ApprovalCenter.
- Test hành vi `FinanceWatchCompanyEmployeesTest` mất ~2 phút trên DB chung nhiều agent (mỗi lần `refreshNow` đồng bộ lại nhiều loại); nếu thấy chậm thì chỉ chạy ca tĩnh `--filter=moi_loai_deu_theo_doi`.

## 9. Kết quả chạy cuối + dọn dữ liệu thử

- `phpunit tests/Feature/ApprovalCenter/Finance --filter='AdditionAccounting|BillAdjustDept|BillIncome|BillPayment|BonusEnd|BorrowExtend|BorrowSell|BuyServiceRequest|InventoryAudit|PositionInventory|Prepick|ProductImport|ProductPrepick|SelfInventory|FinanceWatch'`: 93 test, 92 xanh; 1 lỗi duy nhất là `ProductImportDirectTransferDefinitionTest` (của agent khác, `Lock wait timeout` 1205 do nhiều agent chạy song song trên cùng DB — va chạm tạm, không thuộc phần này).
- `php artisan approval-center:clean-test --manifest=wave2-finance-e.json` → xoá 10 phiếu thử `bill_payment_request`; đã xoá thêm 10 dòng `approval_inbox_*` (state đóng) trỏ tới 10 phiếu thử đó. Xác nhận: không còn phiếu / chi tiết / vai trò `TEST-APPROVAL-CENTER` của phiên này. Còn 4 phiếu `TEST.DNTT.*` (id 4882–4885, tạo 16/11 19:25 theo `e2e-seed.json` từ trước) — KHÔNG phải của phiên này nên không đụng.
- `php -l` toàn bộ file Definition / service / test đã đụng: sạch. File đột biến đều đã khôi phục (`diff` rỗng).
