# Kiểm kê luồng phê duyệt ERP (TanPhatDev, nhánh `gop_db`)

> Ngày soát: 22/10/2026 · Code: working tree `ERP/TanPhatDev` nhánh `gop_db` (HEAD `9ed92a68e2`) ·
> DB: `hrm_erp_21_10_prod` (dump prod 21/10, chỉ chạy SELECT) · Không sửa source, không ghi DB.
>
> Phục vụ: hộp "Phiếu chờ duyệt tập trung" dùng chung ERP + HRM (1 DB MySQL).

## 0. Cách soát và nguồn đối chiếu

- **Registry 49 loại** = `config/approval_inbox.php` ở commit `46ab7152` (nhánh `develop_01`). Điều kiện "đang
  chờ" lấy từ `BackfillApprovalInbox.php` cùng commit, rồi **đối chiếu lại với code `gop_db`**: `canApprove*()`
  trong model, `HomeController@approveList` (dòng 493–2541), `routes/web.php`.
- **Quan trọng:** commit `46ab7152` **KHÔNG nằm trong `gop_db`** (`git merge-base --is-ancestor` → không). Trên
  `gop_db` chưa có `config/approval_inbox.php`, và DB prod chưa có bảng `approval_inbox`/`approval_inbox_logs`.
  Prod hiện chỉ có màn tổng hợp cũ `approveList` (đếm theo thẻ).
- Tìm luồng sót theo: route có `approve|reject|deny|duyet|accept|confirm|changeStatus`, mọi hàm
  `can*Approve*()` trong `app/Model`, hằng số `CHO_*DUYET|AWAIT*|WAIT*|PENDING`, và các quyền guard `web` có chữ
  "duyệt / kiểm soát / xác nhận / tiếp nhận" trong bảng `permissions`.
- Số phiếu đang chờ = `COUNT(*)` toàn bảng (không lọc công ty) theo đúng điều kiện chờ. "Gần nhất" = `MAX(created_at)`
  của các phiếu đang chờ. Bảng 0 dòng ghi rõ "bảng rỗng".
- Tên quyền ghi đúng như trong DB (guard `web`, id 100xxx trên DB gộp). Đã kiểm: mọi tên quyền ghi trong bảng đều
  tồn tại, **trừ** `Duyệt PL giảm HDDV` và `Duyệt PI` (không có trong bảng `permissions` → nhánh code đó chết).
- Quy ước cột "Route duyệt/từ chối": tên route, bỏ tiền tố chung. `update` = duyệt bằng nút trên form/màn show
  (gọi `canApprove()` trong `update`), `deny` = từ chối/trả lại.

Ký hiệu cột Registry: `doc_type` nếu đã có trong 49 loại; **chưa** nếu chưa đăng ký.

---

## 1. Bán hàng (hợp đồng, báo giá, kế hoạch, chỉ tiêu)

| STT | Tên luồng | Bảng | Model | Trạng thái chờ (cột `status`) | Quyền duyệt từng cấp / người duyệt | Route duyệt / từ chối | URL chi tiết | Đang chờ | Gần nhất | Registry | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Hợp đồng bán hàng + phụ lục (HĐ, PLBS, PLG, HĐ dự án + PL, HĐ nguyên tắc, ĐH nguyên tắc + PLG, bản nha khoa `is_zt=1`) | firm_contracts | Sale\Firm\Contract\FirmContract | 2 = CHO_DUYET (mọi `type` 1–10) | Cấp 1: trưởng phòng của `department_id` (EmployeeManageDepartment) khi `approver_id` trống, cần `Duyệt hợp đồng`. Cấp 2: người đích danh `approver_id`. Riêng HĐNT (type 7): `Duyệt hợp đồng nguyên tắc` hoặc `Ban giám đốc duyệt hợp đồng` | firmContract.approve, firmContractAdditionAnnexes.approve, firmContractAnnexes.approve, principleContract.approve / .denyApprove, zt.firmContract.approve, zt.firmContractAdditionAnnexes.approve, zt.firmContractAnnexes.approve, zt.principleContract.approve / .denyApprove | firmContract.show (+ firmContractAdditionAnnexes/Annexes.show, principleContract.show, zt.*) | **17** (HĐ 8 · PLBS 3 · PLG 1 · HĐNT 3 · ĐHNT 2) | 2026-10-21 19:58 | firm_contract | 1 doc_type gánh 10 type + bản nha khoa. `approveList` tách 11 thẻ theo type và `is_zt`. `canApprove()` có nhánh bỏ qua quyền cho Super Admin |
| 2 | Gia hạn HĐ nguyên tắc | firm_contracts | FirmContract | 11 = GIA_HAN_CHO_DUYET | `Duyệt hợp đồng nguyên tắc` (+ Super Admin bypass) | principleContract.approvedExtend, zt.principleContract.approvedExtend | principleContract.show | 0 | — | **chưa** | Cùng bảng với dòng 1 nhưng là bước duyệt khác. `approveList` có thẻ "HĐ nguyên tắc gia hạn cần duyệt" |
| 3 | Báo giá dự án (duyệt nội dung) | project_quotations | Sale\ProjectQuotation | 4 = CHO_DUYET | `approver_id` đích danh, HOẶC quyền `Duyệt báo giá dự án`, HOẶC vai trò "Tổng giám đốc"/"Giám đốc" | update (nút Duyệt) · ProjectQuotation.rejectApprove | ProjectQuotation.show | 0 (bảng chỉ 6 dòng, đều status 3) | — | project_quotation | **Lệch:** thẻ `approveList` dùng quyền `Duyệt báo giá` + `status=2` (là CHO_HIEU_LUC), không phải 4. Có duyệt theo **vai trò** (không qua quyền) |
| 4 | Duyệt hiệu lực báo giá dự án | project_quotations | ProjectQuotation | 2 = CHO_HIEU_LUC | `valid_approver_id` đích danh hoặc vai trò TGĐ/GĐ (quyền `Duyệt hiệu lực báo giá dự án` có trong DB nhưng code không dùng) | ProjectQuotation.sendApproveValid → .approveValid / .rejectValid | ProjectQuotation.show | 0 | — | **chưa** | Cấp thứ 2 của báo giá dự án, registry chưa có |
| 5 | Biên bản thanh lý hợp đồng | liquidation_records | Sale\LiquidationRecord | 2 = CHO_DUYET | `Duyệt biên bản thanh lý hợp đồng` | liquidationRecord.approve (gửi `status`=3 duyệt / 4 từ chối) | liquidationRecord.show | **3** | 2026-05-09 10:53 | **chưa** | Không có thẻ trong `approveList` → đang "chìm". 13.546 biên bản khác đã duyệt (status 3) |
| 6 | Phiếu bàn giao công việc (2 bước: TP duyệt → phòng nhận tiếp nhận) | hand_over_works | Sale\HandOverWork | 2 = CHO_TP_DUYET; 4 = CHO_TIEP_NHAN | Bước 1: trưởng phòng của `department_id` (EmployeeManageDepartment, không xét quyền) hoặc Super Admin. Bước 2: các phòng nhận trong `hand_over_work_detail_employees` còn `is_acceptance=0` | handOverWork.approve / .reject · handOverWork.acceptance | handOverWork.show | **5** (TP 0 · chờ tiếp nhận 5) | 2026-05-06 13:38 | **chưa** | Luồng "tiếp nhận" chứ không phải "duyệt" ở bước 2. Không có thẻ `approveList`. HRM đang có feature "Bàn giao công việc" riêng — cần quyết định bên nào giữ |
| 7 | Hạch toán yêu cầu làm dịch vụ | service_accounting_requests | Sale\ServiceAccountingRequest | 2 = CHO_DUYET | `Hạch toán yêu cầu làm dịch vụ` (lọc cùng công ty người tạo) | update · serviceAccountingRequest.reject | serviceAccountingRequest.show | **11** | 2026-10-21 15:50 | service_accounting_request | |
| 8 | Yêu cầu làm dịch vụ | service_export_requests | Sale\ServiceExportRequest | 2 = CHO_DUYET | `Duyệt yêu cầu làm dịch vụ` | serviceExportRequest.approve | serviceExportRequest.show | 0 | — | **chưa** | Bảng đứng từ 2024-08 (phiếu cuối 22/08/2024) — có thể đã ngừng dùng |
| 9 | Kế hoạch bán hàng của nhân viên (2 cấp) | sales_employee_plans | Plan\SalesEmployeePlan | 2 = CHO_TP_DUYET; 3 = TP_DA_DUYET (chờ `approver_id`) | Cấp 1: trưởng phòng của phòng người tạo, hoặc `Trưởng phòng duyệt kế hoạch bán hàng nhân viên` + cùng phòng. Cấp 2: `approver_id` đích danh | plan_sale_employee.departmentApprove · (cấp 2) update · .cancelApprove | plan_sale_employee.show | **11** (cấp 1: 1 · cấp 2: 10) | cấp 1: 2023-12-20 · cấp 2: 2026-05-21 | sales_employee_plan (chỉ cấp 1) | Registry + `approveList` chỉ đếm status 2. `canApprove()` có nhánh trả true cho TP **bất kể status** (lỗi). Phiếu cấp 1 duy nhất từ 2023 → rác |
| 10 | Kế hoạch bán hàng phòng | sales_department_plans | Plan\SalesDepartmentPlan | 2 = CHO_DUYET | `Duyệt kế hoạch bán hàng phòng` (+ Super Admin bypass) | plan_sale_department.approve / .cancelApprove | plan_sale_department.show | 0 | — | **chưa** | |
| 11 | Kế hoạch bán hàng công ty | sales_company_plans | Plan\SalesCompanyPlan | 2 = CHO_DUYET | `Duyệt kế hoạch bán hàng công ty` (theo công ty của role) | plan_sale_company.approve / .cancelApprove | plan_sale_company.show | 0 | — | **chưa** | |
| 12 | Kế hoạch phát triển thị trường của nhân viên (2 cấp) | market_employee_plans | Plan\Market\MarketEmployeePlan | 2 = CHO_TP_DUYET; 3 = TP_DA_DUYET | Cấp 1: TP phòng người tạo hoặc `Trưởng phòng duyệt kế hoạch thị trường nhân viên`. Cấp 2: status 3 (code trả true cho **mọi người**) | plan_market_employee.departmentApprove · (cấp 2) update · .cancelApprove | plan_market_employee.show | **13** (cấp 1: 0 · cấp 2: 13) | 2026-05-21 18:02 | **chưa** | **Lệch quyền:** thẻ `approveList` kiểm `Trưởng phòng duyệt kế hoạch bán hàng nhân viên`, model dùng `…thị trường nhân viên`. Cấp 2 không có gate thật → cần nghiệp vụ chốt ai duyệt |
| 13 | Kế hoạch phát triển thị trường phòng | market_department_plans | Plan\Market\MarketDepartmentPlan | 2 = CHO_DUYET | `Duyệt kế hoạch phát triển thị trường phòng` | plan_market_department.approve / .cancelApprove | plan_market_department.show | 0 | — | **chưa** | |
| 14 | Kế hoạch phát triển thị trường công ty | market_company_plans | Plan\Market\MarketCompanyPlan | 2 = CHO_DUYET | `Duyệt kế hoạch phát triển thị trường công ty` | plan_market_company.approve / .cancelApprove | plan_market_company.show | 0 | — | **chưa** | |
| 15 | Chỉ tiêu kinh doanh theo phòng ban (cấp công ty) | business_target_companies | Target\BusinessTargetCompany | 2 = CHO_DUYET | `Duyệt chỉ tiêu kinh doanh theo phòng ban` | target_business_company.approve / .cancelApprove | target_business_company.show | 0 | — | **chưa** | Không có thẻ `approveList` |
| 16 | Chỉ tiêu kinh doanh theo nhân viên | business_target_for_departments | Target\Department\BusinessTargetForDepartment | 2 = CHO_DUYET | Model: `Duyệt chỉ tiêu kinh doanh theo phòng ban`; thẻ `approveList`: `Duyệt chỉ tiêu kinh doanh theo nhân viên` | target_business_department.approve / .cancelApprove | target_business_department.show | 0 | — | **chưa** | **Lệch quyền** giữa thẻ và gate thật |
| 17 | Phân chia thị trường theo nhân viên | division_market_department_employees | Division\Employee\DivisionMarketDepartmentEmployee | **3** = CHO_DUYET (2 là ĐÃ duyệt) | `Duyệt phiếu phân chia thị trường theo nhân viên` (+ Super Admin bypass) | division_market_employee.approve | division_market_employee.show | 0 | — | **chưa** | Thẻ `approveList` viết `where('status',[CHO_DUYET])` — chạy được nhưng dễ đọc nhầm |
| 18 | Duyệt giá hàng hoá | product_approves | ProductApprove | Không có cột trạng thái: mọi dòng = đang chờ | `Duyệt giá hàng hoá` | products.approveSubmit / .notApproveSubmit (bị middleware `productMovedToHrm:price-approve` chặn) | → HRM `price-approve` | **1** | 2026-10-12 15:30 | **chưa** | Màn ERP đã chuyển sang HRM (Duyệt giá bán HRM). Thuộc phía HRM khi đăng ký |
| 19 | Hàng tạm | tmp_products | Product\TmpProduct | 2 = STATUS_PENDING | `Duyệt hàng tạm` | tmpProductApprove / tmpProductReject (bị chặn `productMovedToHrm:temp-list`) | → HRM | 0 | — | **chưa** | Đã chuyển HRM (Phase 6 T8 bỏ thẻ ERP). Thuộc phía HRM |

## 2. Mua hàng / đặt hàng

| STT | Tên luồng | Bảng | Model | Trạng thái chờ | Quyền duyệt từng cấp / người duyệt | Route duyệt / từ chối | URL chi tiết | Đang chờ | Gần nhất | Registry | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 | Yêu cầu đặt hàng (2 cấp) | root_order_requests | Order\RootOrderRequest | 2 = CHO_TP_DUYET; 3 = CHO_DUYET | Cấp 1: `Trưởng phòng duyệt yêu cầu đặt hàng` + phòng quản lý. Cấp 2: **người mua hàng đích danh** theo `assign_histories` (brand × hãng × công ty, `employee_date_to` null) — không có quyền | rootOrderRequest.departmentApprove · .approve · .updateApproverComment | rootOrderRequest.show | **214** (TP 5 · NV mua hàng 209) | 2026-10-21 17:36 | root_order_request | Cấp 2 người duyệt tính động từ phân công hãng |
| 21 | YCĐH ngoài (2 cấp) | inland_order_requests | Order\InlandOrderRequest | 6 = CHO_TP_DUYET; 2 = CHO_DUYET | Cấp 1: `Duyệt yêu cầu đặt hàng ngoài` + phòng quản lý. Cấp 2: `Kiểm soát yêu cầu đặt hàng ngoài` (cùng công ty người tạo) | inlandOrderRequest.departmentApprove · .approve · .reject · .backApproveSm | inlandOrderRequest.show | **10** (TP 8 · Kiểm soát 2) | 2026-10-20 16:18 | inland_order_request | |
| 22 | Đơn hỏi hàng – PO trong nước (tự do / theo hãng) | inland_order_summary_news | Order\InlandOrderSummaryNew | 5 = CHO_DUYET (type 1, 2) | `Duyệt đơn hỏi hàng - PO trong nước` | inlandOrderSummaryNew.firstApprove / .approve / .reject / .cancelApprove | inlandOrderSummaryNew.show | **24** (tự do 24 · hãng 0) | 2026-10-21 17:57 | inland_order_summary_new | Có quyền "Tự Duyệt đơn hỏi hàng - PO trong nước" (tự duyệt khi lập) |
| 23 | PI trong nước (tự do / theo hãng) | inland_purchase_invoices | Order\InlandPurchaseInvoice | 2 = CHO_DUYET (type 1, 2) | `Duyệt PI mua hàng trong nước` | inlandPurchaseInvoice.approve / .reject | inlandPurchaseInvoice.show | **5** (tự do 5) | 2026-10-21 15:35 | inland_purchase_invoice | |
| 24 | HĐ mua hàng trong nước + PLBS (tự do / theo hãng) | inland_buy_contract_news | Order\InlandBuyContractNew | 2 = CHO_DUYET (type 1, 2, 4, 5) | `Duyệt hợp đồng mua hàng trong nước` | inlandBuyContractNew.approve | inlandBuyContractNew.show | **29** (HĐ tự do 28 · HĐ hãng 1 · PL 0) | 2026-10-21 16:05 | inland_buy_contract | Type 3 (đơn hàng nguyên tắc) dùng chung gate; quyền `Duyệt đơn hàng nguyên tắc mua hàng trong nước` chỉ xuất hiện ở model, không gate |
| 25 | HĐ nguyên tắc đặt hàng trong nước | rule_inland_buy_contracts | Order\RuleInlandBuyContract | 2 | `Duyệt hợp đồng mua hàng trong nước` | ruleInlandBuyContract.approve | ruleInlandBuyContract.show | 0 | — | **chưa** | Có thẻ `approveList` |
| 26 | HĐĐH ngoài (mẫu cũ) | inland_buy_contracts | Order\InlandBuyContract | 2 | `Duyệt hợp đồng đặt hàng ngoài` + **đúng `approver_id`** | inlandBuyContract.approve | inlandBuyContract.show | **3** | 2026-10-20 16:51 | inland_buy_contract_old | Vẫn đang phát sinh phiếu |
| 27 | Phụ lục HĐ mua hàng ngoài | inland_buy_contract_annexes | Order\InlandBuyContractAnnex | 2 | `Duyệt hợp đồng đặt hàng ngoài` + đúng `approver_id` | inlandBuyContractAnnex.approve | inlandBuyContractAnnex.show | 0 | — | **chưa** | Có thẻ `approveList` |
| 28 | Phụ lục giảm HĐ mua hàng ngoài | inland_buy_contract_annex2 | Order\InlandBuyContractAnnex2 | 2 | `Duyệt hợp đồng đặt hàng ngoài` + đúng `approver_id` | inlandBuyContractAnnex2.approve | inlandBuyContractAnnex2.show | 0 | — | **chưa** | Bảng 2 dòng, cuối 07/2026 |
| 29 | HĐ đặt hàng nhập khẩu | buy_contract2 | Order\BuyContract2 | 2 | `Duyệt hợp đồng mua hàng nhập khẩu` (cùng công ty) | buyContract2.approve | buyContract2.show | **1** | 2026-10-21 15:18 | buy_contract2 | |
| 30 | Phụ lục HĐ mua hàng nhập khẩu | buy_contract_annex2 | Order\BuyContractAnnex2 | 2 = CHO_DUYET | `Duyệt phụ lục hợp đồng mua hàng` | buyContractAnnex2.approve | buyContractAnnex2.show | **1** | 2026-06-01 16:37 | **chưa** | **Không có thẻ `approveList`** → phiếu treo từ 01/06 không ai thấy |
| 31 | Đơn hỏi hàng – PO nhập khẩu | order_summary2 | Order\OrderSummary2 | 5 = CHO_DUYET | `Duyệt đơn hỏi hàng - PO nhập khẩu` | orderSummary2.approve / .reject / .cancelApprove | orderSummary2.show | 0 | — | **chưa** | Có quyền "Tự Duyệt …" → phần lớn tự duyệt khi lập |
| 32 | PI nhập khẩu | purchase_invoices | Order\PurchaseInvoice | 2 = CHO_DUYET | `Duyệt PI mua hàng nhập khẩu` | purchaseInvoice.approve / .reject | purchaseInvoice.show | 0 | — | purchase_invoice | Khối thẻ `Duyệt PI` trong `approveList` là chết (quyền không tồn tại) |
| 33 | Tờ khai hải quan | custom_declarations | Warehouse\CustomDeclaration | 2 = CHO_DUYET | `Duyệt tờ khai hải quan` | customDeclaration.approve / .reject | customDeclaration.show | 0 | — | **chưa** | |
| 34 | Tổng hợp chi phí nhập khẩu | order_import_requests | Warehouse\OrderImportRequest | 2 | `Kế toán mua hàng` (cùng công ty người tạo) | orderImportRequest.approve / .reject | orderImportRequest.show | 0 | — | order_import_request | |
| 35 | Yêu cầu hỏi giá (2 cấp) | price_asking_requests | Order\PriceAskingRequest | 2 = CHO_DUYET; 5 = CHO_XNK_DUYET | Cấp 1: `PTKD duyệt yêu cầu hỏi giá`. Cấp 2: `XNK duyệt yêu cầu hỏi giá` + người phụ trách hãng (AssignHistory) | PriceAskingRequest.approve / .reject / .approveXNK / .rejectXNK / .cancelApprove (đều bị `productMovedToHrm:asking-*` chặn) | → HRM | **23** (PTKD 5 · XNK 18) | 2026-10-21 16:39 | price_asking_request | **Đã chuyển sang HRM** (Phase 7 T7 bỏ thẻ ERP). Khi đăng ký phải tính là phiếu của HRM. Status 7 = CHO_TINH_GIA là việc, không phải duyệt |
| 36 | Yêu cầu tính giá | price_calculate_requests | Order\PriceCalculateRequest | 2 = CHO_DUYET | `Kế toán mua hàng` | PriceCalculateRequest.reject (duyệt qua update) — bị chặn `productMovedToHrm:calc-*` | → HRM | **5** | 2026-10-21 16:12 | price_calculate_request | Đã chuyển HRM, như dòng 35 |
| 37 | Yêu cầu hỏi giá vận chuyển | delivery_cost_asking_requests | Order\DeliveryCostAskingRequest | 2 = CHO_DUYET | `Mua hàng` | update | DeliveryCostAskingRequest.show | 0 (bảng 1 dòng) | — | delivery_cost_asking_request | Gần như không dùng |
| 38 | Yêu cầu mua dịch vụ (2 cấp) | buy_service_requests | Sale\BuyServiceRequest | 2 = CHO_TP_DUYET; 3 = CHO_KS_DUYET | Cấp 1: `Trưởng phòng duyệt yêu cầu mua dịch vụ` (+ phòng quản lý ở thẻ). Cấp 2: `Ban kiểm soát duyệt giá mua dịch vụ` (cùng công ty) | buyServiceRequest.departmentApprove · .ksApprove · .reject · .sendKsApproveAgain | buyServiceRequest.show | 0 | — | **chưa** | Có thẻ `approveList` |
| 39 | Hợp đồng mua dịch vụ | buy_service_contracts | Sale\BuyServiceContract | 2 = CHO_DUYET | `Duyệt hợp đồng mua dịch vụ` (cùng công ty) | buyServiceContract.approve | buyServiceContract.show | 0 | — | **chưa** | |
| 40 | Yêu cầu hạch toán mua dịch vụ | buy_service_accounting_requests | Sale\BuyServiceAccountingRequest | 2 = CHO_DUYET | `Hạch toán mua dịch vụ` | update · buyServiceAccountingRequest.reject | buyServiceAccountingRequest.show | **2** | 2026-10-19 10:53 | buy_service_accounting_request | |
| 41 | Phân công phòng phụ trách thương hiệu – hãng | assign_department_ballots | Order\AssignDepartmentBallot\AssignDepartmentBallot | 2 = CHO_DUYET | `Duyệt phiếu phân công phòng phụ trách thương hiệu hãng sản xuất` | assign-department-brand.approve → .submitApprove | assign-department-brand.show | **7** | 2026-09-21 09:19 | assign_department_ballot | |

## 3. Kho

| STT | Tên luồng | Bảng | Model | Trạng thái chờ | Quyền duyệt từng cấp / người duyệt | Route duyệt / từ chối | URL chi tiết | Đang chờ | Gần nhất | Registry | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 42 | Yêu cầu xuất hàng (3 cấp) | product_export_requests | Warehouse\ProductExportRequest | 2 = CHO_DUYET; 10 = DOI_TP_DUYET; 11 = DOI_BGD_DUYET | KTK: `Kế toán kho`. TP: `Trưởng phòng duyệt xuất hàng vượt hạn mức công nợ` (type ≠ mượn) / `Trưởng phòng duyệt hàng mượn` (type mượn) + phòng quản lý. BGĐ: `Ban giám đốc duyệt xuất hàng vượt hạn mức công nợ` / `Ban giám đốc duyệt hàng mượn` | update (KTK) · productExportRequest.managerApprove (TP/BGĐ) · .deny | productExportRequest.show | **17** (KTK 16 · TP 1 · BGĐ 0) | 2026-10-21 15:45 | product_export_request | Status 14 = CHO_DUYET_NHAP (1 phiếu) **do phiếu YC nhập hàng hạ nguồn đẩy về** — việc duyệt nằm ở dòng 43, không đăng ký riêng |
| 43 | Yêu cầu nhập hàng (tới 3 cấp) | product_import_requests | Warehouse\ProductImportRequest | 2 = CHO_DUYET; 12 = CHO_TP_DUYET; 10 = CHO_BAN_KIEM_SOAT_DUYET; 11 = CHO_BGD_DUYET | KTK: `Kế toán kho`. TP: `Trưởng phòng duyệt yêu cầu nhập hàng` + phòng quản lý. BKS: `Ban kiểm soát duyệt giá nhập hàng trả lại`. BGĐ: `BGD duyệt giá nhập hàng trả lại` | update · .controlDepartmentManagerApprove · .controlBoardApprove / .controlBoardManagerReject · .boardOfManagerApprove / .boardOfManagerReject · .deny | productImportRequest.show | **36** (KTK 27 · TP 9 · BKS 0 · BGĐ 0) | 2026-10-21 19:10 | product_import_request | |
| 44 | Phiếu xuất kho | warehouse_exports | Warehouse\WarehouseExport | 2 | `Kế toán kho` (cùng công ty; nếu gắn chuyến xe thì chuyến phải status 1) | update · warehouseExport.deny | warehouseExport.show | **70** | 2026-10-21 16:17 | warehouse_export | Thẻ cũ loại type 5 (xuất điều chuyển cùng thủ kho) — hiện không có phiếu type 5 chờ |
| 45 | Đề nghị xuất kho | warehouse_export_requests | Warehouse\WarehouseExportRequest | 2 | **Thủ kho** của kho (`isWarehouseStocker(warehouse_id)`; thẻ cần thêm quyền `Thủ kho`) | update · warehouseExportRequest.deny | warehouseExportRequest.show | **84** | 2026-10-21 18:01 | warehouse_export_request | Người duyệt theo kho, không theo công ty |
| 46 | Phiếu nhập kho | warehouse_imports | Warehouse\WarehouseImport | 2 | `Kế toán kho` | update · warehouseImport.deny | warehouseImport.show | **12** | 2026-10-21 16:39 | warehouse_import | |
| 47 | Đề nghị nhập kho | warehouse_import_requests | Warehouse\WarehouseImportRequest | 2 | Thủ kho của kho | update · warehouseImportRequest.deny | warehouseImportRequest.show | **50** | 2026-10-21 19:05 | warehouse_import_request | |
| 48 | Yêu cầu chuyển hàng | product_transfer_requests | Warehouse\ProductTransferRequest | 2 | `Kế toán kho` (cùng công ty) | update · productTransferRequest.reject | productTransferRequest.show | **9** | 2026-10-21 15:58 | product_transfer_request | |
| 49 | Yêu cầu xuất ghép | join_export_requests | Warehouse\JoinExportRequest | 2 = CHO_DUYET | `Kế toán kho` (cùng công ty) | update · joinExportRequest.deny | joinExportRequest.show | **1** | 2026-10-21 09:45 | join_export_request | |
| 50 | Yêu cầu xuất tách | split_export_requests | Warehouse\SplitExportRequest | 2 = CHO_DUYET | `Kế toán kho` (cùng công ty) | update · splitExportRequest.deny | splitExportRequest.show | **1** | 2026-09-30 10:57 | **chưa** | Có thẻ `approveList` (link `splitExportRequest.all`). Sót khỏi registry |
| 51 | Yêu cầu xuất hàng mượn | borrow_export_requests | Warehouse\BorrowExportRequest | 2 | `Kế toán kho` | update · borrowExportRequest.deny | borrowExportRequest.show | 0 | — | **chưa** | |
| 52 | Yêu cầu xuất bán hàng mượn (3 cấp) | borrow_sell_requests | Warehouse\BorrowSellRequest | 2; 10 = CHO_TP_DUYET; 11 = CHO_BGD_DUYET | KTK `Kế toán kho` · TP `Trưởng phòng duyệt xuất hàng vượt hạn mức công nợ` + phòng · BGĐ `Ban giám đốc duyệt xuất hàng vượt hạn mức công nợ` | update · borrowSellRequest.managerApprove · .deny | borrowSellRequest.show | 0 | — | borrow_sell_request | |
| 53 | Gia hạn hàng mượn (3 cấp) | borrow_extend_requests | Warehouse\BorrowExtendRequest | 4 (TP) → 5 (BGĐ) → 2 (KTK) | `Trưởng phòng duyệt hàng mượn` + phòng · `Ban giám đốc duyệt hàng mượn` · `Kế toán kho` | borrowExtendRequest.approve / .deny | borrowExtendRequest.show | **2** (TP 0 · BGĐ 1 · KTK 1) | 2026-10-21 09:28 | borrow_extend_request | Thứ tự cấp ngược thứ tự số status |
| 54 | Yêu cầu xuất giữ (3 cấp) | product_prepick_requests | Warehouse\ProductPrepickRequest | 6 (TP) → 4 (BGĐ) → 2 (KT) | `Trưởng phòng duyệt hàng giữ` + phòng · `Ban giám đốc duyệt hàng giữ` · `Kế toán duyệt hàng giữ` | productPrepickRequest.approve / .deny | productPrepickRequest.show | **6** (TP 2 · BGĐ 1 · KT 3) | 2026-10-21 16:15 | product_prepick_request | |
| 55 | Phiếu xuất giữ – BKS duyệt | warehouse_prepick_requests | Warehouse\WarehousePrepickRequest | 4 | `Ban kiểm soát duyệt giữ hàng` | warehousePrepickRequest.approve | warehousePrepickRequest.show | 0 | — | warehouse_prepick_request | Thẻ `approveList` còn đếm status 3 (đang tạo, của chính người có `Trưởng phòng kế toán`) — 10 phiếu status 3 là nháp, không tính |
| 56 | Điều chuyển hàng giữ (3 cấp) | prepick_transfer2 | Warehouse\PrepickTransfer2 | 5 (TP) → 4 (BGĐ) → 2 (KT) | `Trưởng phòng duyệt hàng giữ` (theo NV nhận `to_employee_id` thuộc phòng) · `Ban giám đốc duyệt hàng giữ` · `Kế toán duyệt hàng giữ` | PrepickTransfer2.approve / .checkSwitchApprove | PrepickTransfer2.show | **2** (TP 1 · KT 1) | 2026-10-21 11:45 | prepick_transfer2 | Phiếu TP từ 2025-10-27 → có thể treo |
| 57 | Gia hạn hàng giữ (3 cấp) | prepick_extend_requests | Warehouse\PrepickExtendRequest | 5 (TP) → 4 (BGĐ) → 2 (KT) | như dòng 54 | prepickExtendRequest.approve / .deny | prepickExtendRequest.show | **4** (KT 3 · BGĐ 1) | 2026-10-21 15:40 | prepick_extend_request | |
| 58 | Yêu cầu huỷ hàng giữ | prepick_cancel_requests | Warehouse\PrepickCancelRequest | 2 | `Quản lý giữ hàng` (thẻ đặt trong khối `Kế toán kho`) | update · prepickCancelRequest.deny | prepickCancelRequest.show | **1** | 2026-10-20 11:26 | **chưa** | Có thẻ `approveList`. Sót khỏi registry |
| 59 | Điều chuyển hàng nhập thẳng | product_import_direct_transfers | Warehouse\ProductImportDirectTransfer | 2 = CHO_DUYET | `Kế toán kho` | productImportDirectTransfers.approve | productImportDirectTransfers.show | **1** | 2026-10-21 15:20 | product_import_direct_transfer | |
| 60 | Báo thừa / thiếu nhập kho | exc_shortage_warehouse_imports | Warehouse\ExcShortageWarehouseImport | 2 = CHO_DUYET | `Duyệt phiếu báo hàng thừa, thiếu nhập kho` | warehouseImport.excShortage.approve | warehouseImport.excShortage.show | **10** | 2026-09-24 14:00 | exc_shortage_warehouse_import | |
| 61 | Xử lý hàng thiếu nhập kho | inventory_discrepancy_handling_imports | Warehouse\InventoryDiscrepancyHandlingImport | **4** = CHO_DUYET | `Duyệt phiếu xử lý hàng thiếu nhập kho` (+ Super Admin bypass) | inventory.discrepancy.approve | inventory.discrepancy.show | 0 | — | **chưa** | |
| 62 | Nhập kho điều chỉnh kiểm kê | warehouse_inventory_imports | Warehouse\Inventory\WarehouseInventoryImport | **1** = CHO_DUYET | `Kế toán kho` | update (màn forApprover) | warehouseInventoryImport.show | 0 | — | **chưa** | |
| 63 | Xuất kho điều chỉnh kiểm kê | warehouse_inventory_exports | Warehouse\Inventory\WarehouseInventoryExport | **1** = CHO_DUYET | `Kế toán kho` | update (màn forApprover) | warehouseInventoryExport.show | 0 | — | **chưa** | |
| 64 | Kiểm kê hàng hoá | self_inventories | Warehouse\SelfInventory | 2 = CHO_KT_DUYET | `Ban kiểm soát duyệt kết quả kiểm kê` | self_inventory.approve / .unApprove | self_inventory.show | 0 | — | **chưa** | |
| 65 | Kết quả kiểm kê vị trí | position_inventories (type 1) | Warehouse\PositionInventory | 2 = KK_CHO_DUYET | `Ban kiểm soát duyệt kết quả kiểm kê` | positionInventoryResult.approve / .unApprove | positionInventoryResult.show | 0 | — | **chưa** | Cùng bảng với dòng 66 |
| 66 | Kế hoạch kiểm kê vị trí | position_inventories (type 0) | Warehouse\PositionInventory | 1 = DANG_KIEM | Thủ kho của kho trong kế hoạch (`warehouse_stockers`) + quyền thẻ `Lập phiếu kiểm kê kho theo vị trí` | positionInventory.stockApprove | positionInventory.show | 0 | — | **chưa** | "Duyệt" ở đây là thủ kho xác nhận kế hoạch — cần nghiệp vụ xác nhận có tính là phiếu chờ duyệt |
| 67 | Biên bản xử lý hàng thừa, thiếu sau kiểm kê | inventory_audit_reports | Warehouse\Inventory\InventoryAuditReport | 1 = CHO_DUYET | `Duyệt biên bản xử lý hàng thừa, thiếu sau kiểm kê` | inventoryAuditReport.approve | inventoryAuditReport.show | 0 (bảng rỗng) | — | **chưa** | Chưa từng dùng |

## 4. Kế toán / thu chi / quyết toán

| STT | Tên luồng | Bảng | Model | Trạng thái chờ | Quyền duyệt từng cấp / người duyệt | Route duyệt / từ chối | URL chi tiết | Đang chờ | Gần nhất | Registry | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 68 | Đề nghị thanh toán (4 cấp duyệt) | bill_payment_requests | IncomeExpenditure\BillPaymentRequest | 2 (TP) · 3 (KT công nợ) · 4 (KT trưởng) · 5 (BGĐ) | `Trưởng phòng duyệt đề nghị thanh toán` + phòng · `Kế toán công nợ duyệt đề nghị thanh toán` · `Kế toán trưởng duyệt đề nghi thanh toán` · `Ban giám đốc duyệt đề nghi thanh toán` | bill_payment_request.changeStatus | bill_payment_request.show | **139** (TP 8 · KTCN 60 · KTT 70 · BGĐ 1) | 2026-10-21 17:58 | bill_payment_request | Ngoài 4 cấp: **status 6** = chờ `Kế toán thanh toán` lập phiếu chi (**56** phiếu; thẻ `approveList` CÓ đếm) — là việc, không phải duyệt; **status 7** = chờ duyệt phiếu chi/UNC (**2**) — trạng thái do phiếu chi/UNC hạ nguồn đẩy về. Cần chốt có hiện 6/7 không |
| 69 | Phiếu chi (2 cấp) | bill_payments | IncomeExpenditure\BillPayment | 2 (thủ quỹ) · 5 (KT trưởng) | `Thủ quỹ duyệt phiếu chi` · `Kế toán trưởng duyệt phiếu chi` | update (màn bill_payment.forApproved) | bill_payment.show | **2** (thủ quỹ 2 · KTT 0) | 2026-10-19 13:23 | bill_payment | Thẻ `approveList` không lọc công ty |
| 70 | Phiếu thu | bill_incomes | IncomeExpenditure\BillIncome | 2 | `Thủ quỹ duyệt phiếu thu` | update (bill_income.forApproved) | bill_income.show | 0 | — | bill_income | |
| 71 | Đề nghị thu tiền | bill_income_requests | IncomeExpenditure\BillIncomeRequest | 2 | `Kế toán thanh toán` hoặc `Kế toán` | bill_income_request.changeStatus | bill_income_request.show | **3** | 2026-10-21 19:53 | bill_income_request | |
| 72 | YC điều chỉnh công nợ | bill_adjust_dept_requests | IncomeExpenditure\BillAdjustDeptRequest | 2 | `Kế toán thanh toán` hoặc `Kế toán` | bill_adjust_dept_request.changeStatus | bill_adjust_dept_request.show | **26** | 2026-10-21 19:50 | bill_adjust_dept_request | |
| 73 | YC hạch toán bổ sung | addition_accounting_requests | IncomeExpenditure\AdditionAccountingRequest | 2 = CHO_DUYET | type ≠ 7: `Kế toán thanh toán`/`Kế toán` cùng công ty. type 7 (hỗ trợ): công ty có phòng trong `addition_departments.support_department_id` | update · additionAccountingRequest.reject | additionAccountingRequest.show | **39** (type 7: 3 · loại khác 36) | 2026-10-21 16:23 | addition_accounting_request | Type 7 duyệt chéo công ty |
| 74 | Uỷ nhiệm chi | bill_payment_authorizations | IncomeExpenditure\BillPaymentAuthorization | 2 = STATUS_AWAITING_APPROVE | — (khối duyệt trong controller bị comment) | — | bill_payment_authorization.show | 0 (3.263 phiếu đều status 3) | — | **chưa** | **Luồng duyệt đã chết**: tạo ra là đã duyệt. Không đăng ký |
| 75 | Quyết toán hợp đồng (3 cấp) | settlement_contracts | Sale\SettlementContract | 2 (TP) → 3 (BGĐ) → 4 (KT) | TP: `Trưởng phòng duyệt quyết toán hợp đồng` (NV trong phòng) · BGĐ: **`valid_approver_id` đích danh** · KT: `Kế toán duyệt quyết toán hợp đồng` | settlementContract.approve · .changeValidApprover | settlementContract.show | **222** (TP 18 · BGĐ 0 · KT 204) | 2026-10-21 16:40 | settlement_contract | Quyền `Ban giám đốc duyệt quyết toán hợp đồng` có trong DB nhưng thẻ BGĐ lọc theo `valid_approver_id` |
| 76 | YC hạch toán hoa hồng tháng | monthly_commission_accounting_requests | Sale\MonthlyCommissionAccountingRequest | 2 = CHO_DUYET | `Duyệt yêu cầu hạch toán hoa hồng tháng` | update · monthlyCommissionAccountingRequest.reject | monthlyCommissionAccountingRequest.show | 0 (bảng rỗng) | — | **chưa** | Có thẻ `approveList` nhưng chưa từng dùng |
| 77 | Quyết toán hoa hồng quý | bill_commission_settlement_quarters | Accounting\BillCommissionSettlementQuarter | 2 | `Duyệt quyết toán hoa hồng quý` | update · bill_commission_settlement_quarters.deny | bill_commission_settlement_quarters.show | 0 | — | **chưa** | 98 phiếu, cuối 04/2026 |
| 78 | Quyết toán năng suất quý | bill_productivity_settlement_quarters | Accounting\BillProductivitySettlementQuarter | 2 | `Duyệt quyết toán hoa hồng quý` (dùng chung) | update · bill_productivity_settlement_quarters.deny | bill_productivity_settlement_quarters.show | 0 | — | **chưa** | Không có thẻ `approveList`. 36 phiếu, cuối 09/10/2026 |
| 79 | Quyết toán hoa hồng tháng | bill_commission_settlement_months | Accounting\BillCommissionSettlementMonth | 2 | `Duyệt quyết toán hoa hồng quý` | update | bill_commission_settlement_months.show | 0 (bảng rỗng) | — | **chưa** | |
| 80 | Quyết toán thưởng kinh doanh | bill_bonus_business | Accounting\BillBonusBusiness | 2 | `Duyệt quyết toán hoa hồng quý` | update | bill_bonus_business.show | 0 (bảng rỗng) | — | **chưa** | |
| 81 | Quyết toán thưởng cuối năm | bonus_end_year_settlements | Accounting\BonusEndYearSettlement | 2 = STATUS_WAITING_APPROVE | `BGĐ duyệt quyết toán năm` | bonus_end_year_settlements.approve → .processApprove | bonus_end_year_settlements.show | 0 (bảng rỗng) | — | **chưa** | Mới, chưa phát sinh |
| 82 | Hồ sơ thanh toán phiếu công tác | assign_business (type = HO_SO_THANH_TOAN) | Assign\AssignBusiness | 2 | `Duyệt hồ sơ thanh toán phiếu công tác` | payment-profile.approved → .submitApproved | payment-profile.show | 0 (163 dòng, đều status 1, cuối 04/2024) | — | **chưa** | Có vẻ đã ngừng dùng |
| 83 | YC hạch toán dịch vụ cần mua (bảo hiểm) | insurance_principle_accounting_requests | Insurance\InsurancePrincipleAccountingRequest | 2 = CHO_DUYET | `Duyệt yêu cầu hạch toán dịch vụ cần mua` | update · insurance.principleAccountingRequest.reject | insurance.principleAccountingRequest.show | 0 (bảng rỗng) | — | **chưa** | Chưa từng dùng |

## 5. Bảo hành / CSKH / dịch vụ sửa chữa

| STT | Tên luồng | Bảng | Model | Trạng thái chờ | Quyền duyệt từng cấp / người duyệt | Route duyệt / từ chối | URL chi tiết | Đang chờ | Gần nhất | Registry | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 84 | HĐ dịch vụ sửa chữa + PLBS + PL giảm | wr_service_contracts | Customers\WrServiceContract | type 1/3: 2 = CHO_DUYET · type 4: 2 = PLG_CHO_DUYET | `Duyệt hợp đồng` + trưởng phòng `department_id` hoặc `approver_id` đích danh. PL giảm: thẻ thêm `Duyệt PL giảm HDDV` (quyền **không tồn tại**) | WarrantyRepairContracts.approve / .reject · WarrantyRepairContractAdditionAnnex.approve / .reject · WarrantyRepairContractAnnex.approve / .reject | WarrantyRepairContracts.show (+ 2 màn PL) | **1** (HĐ 0 · PLBS 1 · PLG 0) | 2026-10-21 19:16 | wr_service_contract | **Bẫy:** type 2 (bảo hành) status 2 = BH_DA_DUYET (4.544 dòng) — phải lọc theo type |
| 85 | Nhập kết quả giao việc | wr_import_results | Customers\WrImportResult | 2 = CHO_DUYET_KET_QUA | `Duyệt phiếu nhập kết quả` (cùng công ty) | update · WrImportResults.reject | WrImportResults.show | **290** | 2026-10-21 16:02 | wr_import_result | Nhiều nhất toàn hệ thống |
| 86 | BKS duyệt kết quả giao việc | wr_assign_tasks (có `parent_id`) | Customers\WrAssignTask | 4 = KQ_CHO_BKS_DUYET | `Ban kiểm soát duyệt kết quả giao việc` | WrApproveResults.store/update · .bksUnApprove | WrApproveResults.show | 0 | — | **chưa** | Có thẻ `approveList` |
| 87 | Hạch toán dịch vụ (kho) | wr_accounting_service_requests | Customers\WrAccountingServiceRequest | 2 = CHO_DUYET | `Kế toán kho` | WrAccountingServiceRequest.approve / .reject | WrAccountingServiceRequest.show | **3** | 2026-10-20 15:41 | wr_accounting_service_request | |
| 88 | YC lắp đặt, bàn giao | assembly_requests | Customers\AssemblyRequest | 6 = CHO_TP_DUYET | `Trưởng phòng duyệt yêu cầu lắp đặt, bàn giao` (thẻ lọc thêm phòng quản lý; `canApprove()` không lọc phòng) | assemblyRequest.approve / .unApprove · .changeDepartmentApprove | assemblyRequest.show | 0 | — | assembly_request | |
| 89 | YC hãng bảo hành | firm_warranty_requests | Order\FirmWarrantyRequests\FirmWarrantyRequest | 2 = CHO_DUYET | **NV mua hàng đích danh** theo `assign_histories` (brand × hãng × `send_company_id`), không quyền | firmWarrantyRequest.approve / .unApprove | firmWarrantyRequest.show | **11** | 2026-10-16 10:17 | firm_warranty_request | |
| 90 | Thư yêu cầu hãng bảo hành | firm_warranties | Order\FirmWarrantys\FirmWarranty | 2 = DA_GUI_NCC | `Lập phiếu xác nhận bảo hành` (+ Super Admin bypass) | firmWarranty.approve | firmWarranty.show | **7** | 2026-08-20 15:01 | firm_warranty | "Duyệt" = xác nhận hãng đã nhận; phiếu treo từ 08/2026 |
| 91 | Phiếu xác nhận bảo hành | firm_warranty_confirms | Order\FirmWarrantyConfirms\FirmWarrantyConfirm | 2 = CHO_DUYET | `Duyệt phiếu xác nhận bảo hành` (+ Super Admin bypass) | firmWarrantyConfirm.approve / .notApprove | firmWarrantyConfirm.show | 0 | — | **chưa** | Có thẻ `approveList` |

## 6. Vận chuyển

| STT | Tên luồng | Bảng | Model | Trạng thái chờ | Quyền duyệt từng cấp / người duyệt | Route duyệt / từ chối | URL chi tiết | Đang chờ | Gần nhất | Registry | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 92 | Tổng hợp giá vận chuyển quốc tế (2 cấp) | summary_shipping_prices | ShippingQuote\SummaryShippingPrice | 2 = CHO_TP_DUYET; 3 = TP_DA_DUYET | `Trưởng phòng duyệt giá vận chuyển quốc tế` + phòng · `Ban kiểm soát duyệt giá vận chuyển quốc tế` | delivery_international_general.approve | delivery_international_general.show | 0 | — | summary_shipping_price | 419 phiếu đều đã duyệt |
| 93 | Chuyến xe khác | other_delivery_trips | Common\OtherDeliveryTrip | 5 = chờ duyệt | `Duyệt chuyến xe khác` (cùng công ty) | otherDeliveryTrip.approve → .submitApprove · .denyApprove | otherDeliveryTrip.show | 0 | — | other_delivery_trip | Status 1 "chờ hạch toán" là việc, không tính |
| 94 | Tổng hợp giá vận chuyển đề xuất | delivery_cost_summaries | Common\DeliveryCostSummary | 2 | `Duyệt giá vận chuyển` | DeliveryCostSummary.approve | DeliveryCostSummary.show | 0 | — | **chưa** | Có thẻ `approveList` |
| 95 | Hợp đồng / phụ lục vận chuyển | delivery_contracts | Common\DeliveryContract | 2 | `Duyệt giá vận chuyển` | deliveryContract.approve | deliveryContract.show | 0 | — | **chưa** | Không có thẻ `approveList` |
| 96 | Đơn hàng vận chuyển quốc tế | summary_order_shipping_prices | ShippingQuote\SummaryOrderShippingPrice | 2 = CHO_DUYET | `Lập đơn hàng vận chuyển quốc tế` (+ Super Admin bypass) | delivery_international_order.approve | delivery_international_order.show | 0 (bảng rỗng) | — | **chưa** | Quyền "Lập…" mà dùng để duyệt — nghi lỗi |
| 97 | Đề nghị thanh toán chi phí vận chuyển | delivery_payment_requests | Warehouse\DeliveryPaymentRequest | 2 | `Kế toán kho` | deliveryPaymentRequest.approveForm → .approve · .reject | deliveryPaymentRequest.show | 0 (bảng rỗng) | — | **chưa** | Chưa từng dùng |
| 98 | Thanh toán vận chuyển cho nhân viên | employee_delivery_payments | Warehouse\EmployeeDeliveryPayment | 2 | `Kế toán kho` | employeeDeliveryPayment.approveForm → .approve | employeeDeliveryPayment.show | 0 (bảng rỗng) | — | **chưa** | Chưa từng dùng |
| 99 | Đề nghị thanh toán chuyến xe khác | other_delivery_payment_requests | Common\OtherDeliveryPaymentRequest | 2 | `Kế toán kho` | otherDeliveryPaymentRequest.approveForm → .approve | otherDeliveryPaymentRequest.show | 0 (bảng rỗng) | — | **chưa** | Chưa từng dùng |

## 7. Hệ thống / khác — luồng cũ, chết, hoặc không phải phiếu duyệt

### 7a. Luồng có code duyệt nhưng bảng rỗng / module cũ (không đề xuất đăng ký)

| STT | Luồng | Bảng | Model | Chờ | Tổng dòng | Ghi chú |
|---|---|---|---|---|---|---|
| 100 | HĐ / báo giá / đơn hàng mẫu cũ (`contracts`): NormalContract, SaleOrder, RuleContract, ContractAdditionAnnex, RuleContractAnnex, LiquidationContract, LiquidationOrder | contracts | App\Contract + các lớp con `$table='contracts'` | 1 (status 2) | 1 (2024-01-11) | Module cũ (`contract.*`, `saleOrder.*`, `ruleContract.*`, `liquidationContract.*`…), thay bằng FirmContract. 1 phiếu rác 2024 |
| 101 | Báo giá mẫu cũ (`App\Quotation`, NormalQuotation, LiquidationQuotation, CostFixingQuotation) | quotations | App\Quotation | — | 288 | **Bảng `quotations` trên DB gộp là của HRM** (`Modules/Assign/Entities/Quotation`, cột `pricing_request_id`, `tp_approved_by`…). Code ERP cũ đọc nhầm dữ liệu HRM nếu được gọi. Không đăng ký từ phía ERP |
| 102 | ServiceContract, ServiceQuotation, ContractAnnex, ServiceContractAnnex, ContractTermAnnex, ServiceContractAdditionAnnex | service_contracts, service_quotations, contract_annexes, service_contract_annexes, contract_term_annexes | Sale\* | 0 | 0 | Bảng rỗng |
| 103 | Phân tích dự án, HĐ dự án (cũ) | project_analysis, project_contracts | Sale\ProjectAnalysis\ProjectAnalysis, Sale\ProjectContract | 0 | 0 | Bảng rỗng |
| 104 | Yêu cầu thiết kế / sản xuất nha khoa | design_requirements, manufacture_requirements | Sale\Firm\Design\* | 0 | 0 | Bảng rỗng; quyền `Duyệt yêu cầu thiết kế` |
| 105 | Lắp đặt: dự toán, tạm ứng, yêu cầu | install_estimates, install_advances, install_requests | Tech\* | 0 | 0 | Bảng rỗng; quyền `Kiểm soát chi phí lắp đặt`, `Duyệt đề nghị tạm ứng chi phí lắp đặt`, `Quản lý lịch lắp đặt` |
| 106 | Đặt hàng mẫu cũ: OrderRequest, OrderSummary, SummaryAnnex, BuyRequest, BuyContract, BuyContractAnnex, ImportRecord, InlandBuyContract2, InlandOrderSummary2, InlandOrderRequest2 | order_requests, order_summaries, summary_annexs, buy_requests, buy_contracts, buy_contract_annexs, import_records, inland_buy_contract2, inland_order_summary2, inland_order_request2 | Order\* | 0 | 0 | Bảng rỗng |
| 107 | YCĐH con sinh từ YC đặt hàng gốc: InlandOrderRequestNew, OrderRequest2 | inland_order_request_news, order_request2 | Order\* | 0 | 5.804 / 4.071 | Có route `approve/departmentApprove` nhưng mọi dòng status 0/1 — không còn bước chờ |
| 108 | Điều chuyển hàng giữ mẫu cũ, điều chuyển kho, kiểm kê kế toán, kiểm kê cũ, biên bản bàn giao kho, yêu cầu giao hàng | prepick_transfers, warehouse_transfers, accounting_inventories, inventories, handover_records, delivery_requests | Warehouse\* | 0 | 0 | Bảng rỗng (quyền `Duyệt yêu cầu điều chuyển hàng giữ` còn trong DB) |
| 109 | Bảo hành mẫu cũ: WarrantyRequest, WarrantyWork, WarrantyReport, WarrantyPayment, WarrantyPaymentRequest | warranty_* | Customers\* | 0 | 0 | Bảng rỗng |
| 110 | Giao việc khác — route `assignOtherRequest.approve` | assign_other_requests | Customers\AssignOtherRequest | — | 3.044 | Route trỏ method **không tồn tại** trong controller → chết |
| 111 | Biên bản nghiệm thu bàn giao | handover_acceptance_records | Customers\HandoverAcceptanceRecord | 0 (CHO_DUYET=3) | 8.267 (status 1/2) | Có hằng CHO_DUYET nhưng không có route duyệt; dữ liệu không có status 3 |
| 112 | Phiếu phân công NV phụ trách hãng | assign_employee_ballots | Assign\AssignEmployeeBallot | — | 1.166 | Không có trạng thái chờ (đang tạo → đã duyệt do người lập); không phải phiếu chờ người khác |

### 7b. Mục trong `approveList` nhưng KHÔNG phải ký duyệt (giữ quyết định loại trừ của khảo sát trước)

Chuyến xe chở hàng chờ hạch toán (`delivery_trips` status 1: 91) · Chuyến xe khác chờ hạch toán · Danh sách cần
hạch toán chi phí vận chuyển nhanh · Kết quả giao việc chờ hạch toán dịch vụ (`WrAssignTask` KQ_CHO_HACH_TOAN) ·
Yêu cầu sửa chữa – bảo hành cần xử lý (`warranty_repair_requests` status 2: 137) · YC xử lý SC–BH cần cung cấp
thông tin · Phiếu cung cấp thông tin cần làm báo giá · Phiếu chờ giao việc · Hàng hoá chờ nhập thông tin bán
hàng · Hàng không được duyệt giá bán · Hàng nhập thẳng cần xuất · Hàng mượn / hàng giữ hết hạn · Tài khoản chưa
phân quyền · Thông báo hoàn thiện hồ sơ (BillAssign) · Cảnh báo phân công NV phụ trách hãng.

Thêm từ lần soát này: `DeliveryTrip` status 2 (**51** chuyến) có `canApprove()` nhưng là **người tạo tự xác
nhận** chuyến xong → không phải chờ người khác duyệt. `SelfInventoryRequest` status 1 (1 phiếu, 07/2026) "approve" =
chốt kiểm của người lập. `ProductExportRequest` status 14 (xem dòng 42).

---

## 8. Tổng kết

**Tổng số luồng phê duyệt thật được kiểm kê: 99** (dòng 1–99). Ngoài ra 13 nhóm luồng cũ/chết (dòng 100–112) và
các mục 7b không tính.

| Chỉ số | Số luồng | Phiếu đang chờ |
|---|---:|---:|
| Đã có trong registry 49 loại | 49 luồng (registry 49 `doc_type` ánh xạ đủ vào 49 dòng) | **1.399** (riêng các cấp đã khai trong registry) |
| — trong đó pending > 0 | 39 | |
| — pending = 0 | 10 (project_quotation, bill_income, purchase_invoice, order_import_request, delivery_cost_asking_request, warehouse_prepick_request, borrow_sell_request, summary_shipping_price, other_delivery_trip, assembly_request) | |
| **Chưa có trong registry** | **50** luồng | **25** |
| — trong đó pending > 0 | **7**: Thanh lý HĐ (3), Bàn giao công việc (5), KH PTTT nhân viên (13), Duyệt giá hàng hoá (1 — HRM), PL HĐ nhập khẩu (1), YC xuất tách (1), YC huỷ hàng giữ (1) | |
| — pending = 0 | 43 (trong đó 10 luồng bảng rỗng — chưa từng dùng) | |
| Tổng pending > 0 | **46** luồng | **1.424** |

Ngoài các cấp registry, còn phiếu "lơ lửng" chưa được tính vào bất kỳ dòng nào: KH bán hàng NV cấp 2 (status 3:
10), Đề nghị thanh toán status 6 (56) và 7 (2).

**Top khối lượng:** wr_import_result 290 · settlement_contract 222 · root_order_request 214 · bill_payment_request
139 (+58 ở status 6/7) · warehouse_export_request 84 · warehouse_export 70 · warehouse_import_request 50.

**Registry 49 loại lệch với code `gop_db` ở các điểm:**
1. Registry chưa vào `gop_db`, DB prod chưa có bảng → toàn bộ phải port (xem `ERP/.plans/phieu-cho-duyet-tap-trung/port-gop-db.md`).
2. `price_asking_request`, `price_calculate_request` (28 phiếu đang chờ) đã **chuyển sang HRM** trên `gop_db` (route ERP bị
   `productMovedToHrm` chặn, thẻ ERP đã bỏ). Hai loại này phải chuyển sang phía HRM đăng ký, ERP không được đẩy nữa.
3. `project_quotation` chỉ có cấp "duyệt nội dung" (status 4), thiếu cấp "duyệt hiệu lực" (status 2, `valid_approver_id`).
4. `sales_employee_plan` chỉ có cấp TP (status 2), thiếu cấp 2 (status 3, `approver_id`) đang giữ 10 phiếu.
5. `firm_contract` thiếu bước "gia hạn HĐ nguyên tắc" (status 11).
6. Nhiều `canApprove()` còn nhánh **Super Admin bypass** (FirmContract, FirmWarranty, FirmWarrantyConfirm, các kế
   hoạch, DivisionMarket, InventoryDiscrepancy, SummaryOrderShippingPrice…), trong khi đã chốt bỏ ngoại lệ Super Admin
   ở registry → hộp tập trung sẽ hiện ít hơn những gì Super Admin bấm duyệt được trên màn gốc.

## 9. Điểm cần nghiệp vụ quyết định

1. **Đề nghị thanh toán status 6** (chờ Kế toán thanh toán lập phiếu chi, 56 phiếu) và **status 7** (chờ duyệt phiếu
   chi/UNC, 2 phiếu): có đưa vào hộp "chờ duyệt" không? `approveList` hiện đếm status 6.
2. **Bàn giao công việc (ERP `hand_over_works`)**: bước 2 là "tiếp nhận" chứ không phải "duyệt". Có đưa vào hộp không, và
   HRM đã có feature Bàn giao công việc riêng — luồng ERP có còn dùng không (phiếu cuối 06/05/2026)?
3. **KH phát triển thị trường NV cấp 2** (13 phiếu status 3) và **KH bán hàng NV cấp 2** (10 phiếu): cấp 2 ai duyệt?
   Code MarketEmployeePlan trả "được duyệt" cho mọi người ở status 3; thẻ cấp 1 dùng sai tên quyền. Cần chốt người
   duyệt trước khi đăng ký, hay coi 23 phiếu này là rác (đều tạo trước 22/05/2026).
4. **Chỉ tiêu KD theo NV**: thẻ dùng `Duyệt chỉ tiêu kinh doanh theo nhân viên`, gate thật dùng `…theo phòng ban`. Hộp
   tập trung theo quyền nào?
5. **Báo giá dự án**: cả 2 cấp duyệt theo **vai trò** "Tổng giám đốc"/"Giám đốc" (không qua quyền) + người đích danh.
   Hộp tập trung có hỗ trợ lọc theo vai trò không, hay chỉ người đích danh + quyền `Duyệt báo giá dự án`?
6. **Duyệt giá hàng hoá, hàng tạm, hỏi giá, tính giá**: xác nhận đều do HRM sở hữu khi đăng ký (ERP không push).
7. **Kế hoạch kiểm kê vị trí** (thủ kho xác nhận) và **Thư yêu cầu hãng bảo hành** (`DA_GUI_NCC` → xác nhận): có coi là
   "phiếu chờ duyệt" không?
8. **Đơn hàng vận chuyển quốc tế** gate bằng quyền `Lập đơn hàng vận chuyển quốc tế` — đúng ý hay lỗi?
9. **Luồng bảng rỗng / ngừng dùng** (dòng 8, 76, 79–83, 96–99): có đăng ký sẵn cho đủ không, hay bỏ? Đề xuất: chỉ
   đăng ký luồng còn route sống và có dữ liệu trong 12 tháng qua.
10. **Phiếu treo lâu** cần xử lý dữ liệu trước khi backfill: PL HĐ nhập khẩu (01/06/2026, không có thẻ nên không ai
    thấy), Thanh lý HĐ (09/05/2026), KH bán hàng NV cấp 1 (2023), Điều chuyển hàng giữ chờ TP (27/10/2025), Thư hãng
    bảo hành (08/2026).
