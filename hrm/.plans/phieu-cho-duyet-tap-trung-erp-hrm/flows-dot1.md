# Danh mục luồng đợt 1 — Phiếu chờ duyệt tập trung ERP + HRM

> Soạn 22/10/2026. Chỉ là tài liệu, chưa đụng source, chưa ghi DB (chỉ chạy SELECT trên `hrm_erp_21_10_prod`).
> Đầu vào: [README.md](README.md) (bảng quyết định), [inventory-erp.md](inventory-erp.md) (ERP#1–112), [inventory-hrm.md](inventory-hrm.md) (AS/F/C/M/H).
> Code soát: `ERP/TanPhatDev`, `HRM/hrm-api`, `HRM/hrm-client` (đều nhánh `gop_db`). Registry cũ: `git show 46ab7152:config/approval_inbox.php` (49 loại).

## 0. Quy ước

**Phạm vi đợt 1** (theo README, chốt 22/10):
- Toàn bộ luồng ERP thật (ERP#1–99) và các module HRM: Assign (trừ legacy AS16–AS20, AS22), Finance, CustomerCare, MasterData, Meeting.
- "Chờ duyệt" gồm 3 loại bước: **duyệt** (duyệt/không duyệt), **tiếp nhận**, **lập chứng từ** (lập chứng từ kế tiếp: KT kho lập phiếu xuất, KT lập phiếu chi, làm báo giá…).
- Luồng có 0 phiếu chờ vẫn đưa vào nếu route còn sống. Chỉ loại luồng **chết** (bảng rỗng và route chết), hoặc luồng không phải phiếu chờ.

**Cách đặt khoá và chọn nơi xử lý:**
- `doc_type`: dùng lại khoá registry cũ khi đã có (49 khoá). Khoá mới đặt theo snake_case số ít của bảng.
- **Cấp**: luồng đã có trong registry cũ thì giữ cách đánh số cũ (vd `product_import_request`: 1 = KT kho). Luồng mới đánh theo thứ tự đi của phiếu.
- **handler_system**: nơi làm được **trọn** bước đó. Chọn HRM khi HRM có endpoint + màn làm hết bước, và trạng thái phiếu gốc đi sang đúng giá trị như ERP. Còn lại chọn ERP.
- Đã kiểm từng cấp có handler = HRM bằng code: route HRM, hàm service ghi trạng thái phiếu gốc, trang client gọi tới (xem cột Nguồn và §6).

**Hệ thống sở hữu bảng**: hệ thống có migration tạo bảng.

**Ghi được từ**: hệ thống có code ghi `status` của bảng. "cả 2" = ERP và HRM đều ghi.

**Đường mở**:
- ERP ghi tên route (`*.show`, bỏ tiền tố).
- HRM ghi đường dẫn client (`/finance/...`, có `:id`).

**gate_type** (5 loại gốc + 4 loại mở rộng mà danh mục cần):

| gate_type | Nghĩa |
|---|---|
| `permission` | Có quyền (tên + guard) và đúng phạm vi: `company` = công ty phiếu = công ty đang làm (mặc định); `department` = phòng của phiếu ∈ phòng user quản lý (`employee_manage_departments`) |
| `approver` | Người đích danh ghi trên phiếu (cột ghi rõ) |
| `role` | Vai trò theo TÊN (`Tổng giám đốc`, `Giám đốc`) |
| `dept_manager` | Quản lý phòng (`employee_manage_departments`), không cần quyền |
| `room_manager` | Người phụ trách phòng họp (`meeting_room_managers`) |
| *`warehouse_stocker`* (mới) | Thủ kho của kho trên phiếu (`warehouse_stockers.stocker_id`) |
| *`assigned_buyer`* (mới) | Nhân viên mua hàng/XNK được phân công **hiện hành** theo thương hiệu × hãng × công ty (`assign_histories`, `employee_date_to` NULL) |
| *`source_creator`* (mới) | Người lập phiếu gốc ở bước trước (vd người lập YC SC-BH) |
| *`support_department`* (mới) | Công ty có phòng nằm trong `addition_departments.support_department_id` (duyệt chéo công ty) |

Một dòng có thể kết hợp nhiều gate, viết bằng "+" (VÀ) hoặc "hoặc" (HOẶC).

**Guard của quyền**:
- ERP xét quyền guard `web`.
- HRM có 3 cơ chế xét quyền:
  - **CEP** (`ChecksEmployeePermission`): so theo TÊN, nhận cả `web` lẫn `api`, thấy mọi `model_type`.
  - **MW** (middleware `checkPermission`) và **HLP** (helper `isCurrentEmployeeHasPermission`): spatie guard `api`, không thấy role `App\Employee`.

Cột "Gate chi tiết" ghi cơ chế đang dùng ở màn gốc. **Không có ngoại lệ Super Admin**: các nhánh vượt quyền của SA trong code gốc không đưa vào gate.

**Số phiếu chờ**: `COUNT(*)` toàn bảng theo điều kiện chờ, DB `hrm_erp_21_10_prod` (dump 21/10). Đã chạy lại SELECT ngày 22/10 cho các bảng có nhiều cấp, kết quả khớp kiểm kê.

---

## 1. Bảng danh mục chính

### 1.1 Hợp đồng · báo giá · bàn giao (bán hàng)

| doc_type | Tên loại phiếu | Bảng | Sở hữu | Ghi được từ | Cấp | Trạng thái chờ | Bước | handler | Đường mở | gate_type | Gate chi tiết | Chờ | Nguồn |
|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| `firm_contract` | HĐ bán hàng + phụ lục (HĐ, PLBS, PLG, HĐ dự án, ĐHNT, bản `zt`) | firm_contracts | ERP | ERP | 1 | `status=2`, `type≠7` | duyệt | ERP | firmContract.show (route theo type: firmContractAdditionAnnexes.show / firmContractAnnexes.show / zt.*) | approver hoặc dept_manager+permission | `approver_id` nếu >0; nếu không thì quản lý phòng `department_id` + quyền `Duyệt hợp đồng` (web) | **14** (rà lại 22/10: bản trước đếm sai 11) | ERP#1 |
| `firm_contract` | ↳ biến thể HĐ nguyên tắc | firm_contracts | ERP | ERP | 1 | `status=2`, `type=7` | duyệt | ERP | principleContract.show | permission | `Duyệt hợp đồng nguyên tắc` hoặc `Ban giám đốc duyệt hợp đồng` (web), company | 3 | ERP#1 |
| `principle_contract_extend` | Gia hạn HĐ nguyên tắc | firm_contracts | ERP | ERP | 1 | `status=11` | duyệt | ERP | principleContract.show | permission | `Duyệt hợp đồng nguyên tắc` (web), company | 0 | ERP#2 |
| `project_quotation` | Báo giá dự án — duyệt nội dung | project_quotations | ERP | ERP | 1 | `status=4` | duyệt | ERP | ProjectQuotation.show | approver hoặc permission hoặc role | `approver_id` hoặc `Duyệt báo giá dự án` (web) hoặc vai trò `Tổng giám đốc` / `Giám đốc` (`ProjectQuotation.php:1961`) | 0 | ERP#3 |
| `project_quotation` | Báo giá dự án — duyệt hiệu lực | project_quotations | ERP | ERP | 2 | `status=2` | duyệt | ERP | ProjectQuotation.show | approver hoặc role | `valid_approver_id` hoặc vai trò `Tổng giám đốc` / `Giám đốc` (`:1985`). Quyền `Duyệt hiệu lực báo giá dự án` có trong DB nhưng code không dùng | 0 | ERP#4 |
| `liquidation_record` | Biên bản thanh lý HĐ | liquidation_records | ERP | ERP | 1 | `status=2` | duyệt | ERP | liquidationRecord.show | permission | `Duyệt biên bản thanh lý hợp đồng` (web), company | 3 | ERP#5 |
| `hand_over_work` | Phiếu bàn giao công việc (ERP) | hand_over_works | ERP | ERP | 1 | `status=2` | duyệt | ERP | handOverWork.show | dept_manager | Quản lý phòng `department_id`, không cần quyền (`HandOverWork.php:147`) | 0 | ERP#6 |
| `hand_over_work` | ↳ phòng nhận tiếp nhận | hand_over_works | ERP | ERP | 2 | `status=4` + `hand_over_work_detail_employees.is_acceptance=0` | tiếp nhận | ERP | handOverWork.show | dept_manager | Quản lý **phòng nhận** (`department_receiver_id` còn `is_acceptance=0`, `:152`) | 5 | ERP#6 |
| `service_export_request` | Yêu cầu làm dịch vụ | service_export_requests | ERP | ERP | 1 | `status=2` | duyệt | ERP | serviceExportRequest.show | permission | `Duyệt yêu cầu làm dịch vụ` (web), company | 0 | ERP#8 |

### 1.2 Kế hoạch · chỉ tiêu kinh doanh

| doc_type | Tên loại phiếu | Bảng | Sở hữu | Ghi được từ | Cấp | Trạng thái chờ | Bước | handler | Đường mở | gate_type | Gate chi tiết | Chờ | Nguồn |
|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| `sales_employee_plan` | KH bán hàng nhân viên — TP duyệt | sales_employee_plans | ERP | ERP | 1 | `status=2` | duyệt | ERP | plan_sale_employee.show | dept_manager hoặc permission | Quản lý phòng của người lập, hoặc `Trưởng phòng duyệt kế hoạch bán hàng nhân viên` (web) + cùng phòng người lập (`SalesEmployeePlan.php:521`) | 1 | ERP#9 |
| `sales_department_plan` | KH bán hàng phòng | sales_department_plans | ERP | ERP | 1 | `status=2` | duyệt | ERP | plan_sale_department.show | permission | `Duyệt kế hoạch bán hàng phòng` (web), department. Duyệt xong đẩy các KH NV `status 3→5` | 0 | ERP#10 |
| `sales_company_plan` | KH bán hàng công ty | sales_company_plans | ERP | ERP | 1 | `status=2` | duyệt | ERP | plan_sale_company.show | permission | `Duyệt kế hoạch bán hàng công ty` (web), company | 0 | ERP#11 |
| `market_employee_plan` | KH phát triển thị trường NV — TP duyệt | market_employee_plans | ERP | ERP | 1 | `status=2` | duyệt | ERP | plan_market_employee.show | dept_manager hoặc permission | Quản lý phòng người lập, hoặc `Trưởng phòng duyệt kế hoạch thị trường nhân viên` (web) + cùng phòng (`MarketEmployeePlan.php:285`) | 0 | ERP#12 |
| `market_department_plan` | KH phát triển thị trường phòng | market_department_plans | ERP | ERP | 1 | `status=2` | duyệt | ERP | plan_market_department.show | permission | `Duyệt kế hoạch phát triển thị trường phòng` (web), department. Duyệt xong đẩy KH NV `3→5` | 0 | ERP#13 |
| `market_company_plan` | KH phát triển thị trường công ty | market_company_plans | ERP | ERP | 1 | `status=2` | duyệt | ERP | plan_market_company.show | permission | `Duyệt kế hoạch phát triển thị trường công ty` (web), company | 0 | ERP#14 |
| `business_target_company` | Chỉ tiêu KD theo phòng ban | business_target_companies | ERP | ERP | 1 | `status=2` | duyệt | ERP | target_business_company.show | permission | `Duyệt chỉ tiêu kinh doanh theo phòng ban` (web), company | 0 | ERP#15 |
| `business_target_for_department` | Chỉ tiêu KD theo nhân viên | business_target_for_departments | ERP | ERP | 1 | `status=2` | duyệt | ERP | target_business_department.show | permission | `Duyệt chỉ tiêu kinh doanh theo phòng ban` (web), company (`withPermissionRole` theo công ty, `BusinessTargetForDepartment.php:164`). Thẻ `approveList` dùng nhầm quyền `…theo nhân viên` | 0 | ERP#16 |
| `division_market_employee` | Phân chia thị trường theo NV | division_market_department_employees | ERP | ERP | 1 | `status=3` (2 = đã duyệt) | duyệt | ERP | division_market_employee.show | permission | `Duyệt phiếu phân chia thị trường theo nhân viên` (web), company | 0 | ERP#17 |

### 1.3 Dự án · giải pháp · báo giá BOM (HRM Assign)

| doc_type | Tên loại phiếu | Bảng | Sở hữu | Ghi được từ | Cấp | Trạng thái chờ | Bước | handler | Đường mở | gate_type | Gate chi tiết | Chờ | Nguồn |
|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| `bom_quotation` | Báo giá BOM — TP duyệt giá | quotations | HRM | HRM | 1 | `is_summary=0`, `status=2` | duyệt | HRM | `/assign/quotations/:id` | permission | `Trưởng phòng duyệt giá Bom giải pháp` (api, MW+HLP) + department (`ensureTpCanApprove`) | 35 | AS1 |
| `bom_quotation` | Báo giá BOM — BGĐ duyệt giá | quotations | HRM | HRM | 2 | `is_summary=0`, `status=3` | duyệt | HRM | `/assign/quotations/:id` | permission | `Ban giám đốc duyệt giá Bom giải pháp` (api, MW+HLP), company | 0 | AS1 |
| `summary_quotation` | Báo giá tổng hợp | quotations | HRM | HRM | 1 | `is_summary=1`, `status=2` | duyệt | HRM | `/assign/summary-quotations/:id` | permission | `Trưởng phòng duyệt giá Bom giải pháp` (api) + department | 0 | AS2 |
| `prospective_project_extension` | Gia hạn dự án TKT — TP | prospective_project_extension_requests | HRM | HRM | 1 | `status=1` | duyệt | HRM | `/assign/prospective-projects/extension-requests` | permission | `Trưởng phòng duyệt gia hạn dự án TKT` (api, MW+HLP) + department. ⚠ Quyền có 0 role | 1 | AS3 |
| `prospective_project_extension` | Gia hạn dự án TKT — BGĐ | prospective_project_extension_requests | HRM | HRM | 2 | `status=2` | duyệt | HRM | như trên | permission | `Ban giám đốc duyệt gia hạn dự án TKT` (api), company. ⚠ 0 role | 0 | AS3 |
| `hrm_contract` | Hợp đồng HRM | hrm_contracts | HRM | HRM | 1 | `status=2` | duyệt | HRM | `/assign/contracts/:id` | permission | `Duyệt hợp đồng` (**api**, MW+HLP). ⚠ Bản api có 0 role, bản web có 21 role | 0 | AS4 |
| `handover` | Bàn giao công việc (HRM) — TP duyệt | handovers | HRM | HRM | 1 | `status=2` | duyệt | HRM | `/assign/handover/:id` | permission | `Duyệt bàn giao công việc` (api, MW) + department (danh sách chờ lọc theo phòng; API duyệt chưa lọc) | 0 | AS5 |
| `handover_item` | Mục bàn giao chờ tiếp nhận | handover_items | HRM | HRM | 1 | `receive_status=0` và phiếu cha `status=3` | tiếp nhận | HRM | `/assign/handover/:id/receive` | approver | `handover_items.receiver_id` | 0 | AS6 |
| `request_solution` | Yêu cầu làm giải pháp | request_solutions | HRM | HRM | 1 | `status=2` | tiếp nhận | HRM | `/assign/request-solution/:id` | permission | `Tiếp nhận yêu cầu làm giải pháp` (api, MW) + `receive_dept` ∈ phòng quản lý | 9 | AS7 |
| `solution_adjustment_request` | Yêu cầu điều chỉnh giải pháp | solution_adjustment_requests | HRM | HRM | 1 | `status=1` | duyệt | HRM | `/assign/prospective-projects/:id/manager` (tab Điều chỉnh) | approver hoặc dept_manager | PM giải pháp (`solutions.pm_id`) hoặc quản lý phòng nhận (accessor `is_can_accept`). ⚠ BE không chốt (fail-open), gate chỉ có ở FE | 1 | AS8 |
| `solution_review_profile` | Hồ sơ trình duyệt giải pháp | solution_review_profiles | HRM | HRM | 1 | `status='pending'` | duyệt | HRM | `/assign/solutions/:id/manager` | approver | `solutions.created_by` của giải pháp (`SolutionService:2697`) | 0 | AS9 |
| `solution_module_review_profile` | Hồ sơ trình duyệt hạng mục | solution_module_review_profiles | HRM | HRM | 1 | `status='pending'` | duyệt | HRM | `/assign/solution-modules/:id/manager` | approver | PM giải pháp hoặc PM ghi trên hồ sơ (`SolutionModuleService:1397`) | 0 | AS10 |
| `solution` | Giải pháp chờ PM tiếp nhận | solutions | HRM | HRM | 1 | `status=3` | tiếp nhận | HRM | `/assign/solutions/:id/manager` | approver | `pm_id` (`Solution::canEdit`) | 1 | AS11 |
| `solution` | Giải pháp chờ Leader hạng mục | solutions | HRM | HRM | 2 | `status=5` | tiếp nhận | HRM | như trên | approver | `solution_modules.leader_id` của hạng mục chưa duyệt (+ `pm_id`) | 0 | AS11 |
| `solution` | Giải pháp chờ duyệt (phòng nhận) | solutions | HRM | HRM | 3 | `status=9` | duyệt | HRM | như trên | permission | `Tiếp nhận yêu cầu làm giải pháp` (api, HLP) + `request_solutions.receive_dept` ∈ phòng quản lý (`Solution.php:228`) | 0 | AS11 |
| `task` | Task — duyệt triển khai | tasks | HRM | HRM | 1 | `status=2` | duyệt | HRM | `/assign/tasks` (modal) | permission | `Duyệt triển khai task` (api, HLP) + quản lý phòng của người xử lý (`Task::canStartApprove`) | 0 | AS12 |
| `task` | Task — duyệt kết quả | tasks | HRM | HRM | 2 | `status=6` | duyệt | HRM | `/assign/tasks` (modal) | approver | `tasks.approver_id` | 2 | AS12 |
| `issue` | Issue — xác nhận đã xử lý | issues | HRM | HRM | 1 | `status='resolved'` | duyệt | HRM | panel Issue | approver | `issues.approver_id` | 0 | AS15 |
| `hrm_settlement_contract` | Quyết toán công theo HĐ (HRM) — TP | hrm_settlement_contracts | HRM | HRM | 1 | `status=2` | duyệt | HRM | `/assign/settlement_contract/:id/show` | permission | `TP duyệt quyết toán hợp đồng` (api, HLP), company (code không lọc phòng) | 0 | AS21 |
| `hrm_settlement_contract` | ↳ KT | hrm_settlement_contracts | HRM | HRM | 2 | `status=3` | duyệt | HRM | như trên | permission | `KT duyệt quyết toán hợp đồng` (api, HLP), company | 0 | AS21 |

### 1.4 Hàng hoá · hỏi giá · tính giá (đã chuyển sang HRM)

| doc_type | Tên loại phiếu | Bảng | Sở hữu | Ghi được từ | Cấp | Trạng thái chờ | Bước | handler | Đường mở | gate_type | Gate chi tiết | Chờ | Nguồn |
|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| `price_asking_request` | Yêu cầu hỏi giá — PTKD duyệt | price_asking_requests | ERP | cả 2 (ERP bị `productMovedToHrm` chặn) | 1 | `status=2` | duyệt | HRM | `/sale/price-asking-requests/:id` | permission | `PTKD duyệt yêu cầu hỏi giá` (api, MW+HLP), company (`PriceAskingAccess::canPtkd`) | 5 | ERP#35, M1 |
| `price_asking_temp_product` | Hàng tạm trong YCHG — PTKD đồng ý | product_company_coefficients | ERP (cột `status` do HRM thêm) | HRM | 1 | `status=6` | duyệt | HRM | `/sale/price-asking-requests/:id/temp/:productId` | permission | `PTKD duyệt yêu cầu hỏi giá` (api, MW), company của phiếu | 1 | M2 (thay ERP#19) |
| `price_asking_request_group` | Nhóm hàng YCHG — XNK duyệt | price_asking_request_groups | HRM | HRM | 1 | `status=5` (phiếu cha ∈ `ASKING_STATUSES`) | duyệt | HRM | `/sale/price-asking-requests/:id` | permission + assigned_buyer | `XNK xử lý yêu cầu hỏi giá` (api, MW) + XNK được phân công hiện hành (`isGroupXnk`) | 24 | M3 (thay cấp 2 cũ của `price_asking_request`) |
| `price_asking_request_group` | Nhóm hàng YCHG — lập YCTG | price_asking_request_groups | HRM | HRM | 2 | `status=1` | lập chứng từ | HRM | `/sale/price-calculate-requests` (lập từ `pending-groups`) | permission + assigned_buyer | Như cấp 1 (route `price-calculate-requests` POST gắn `XNK xử lý yêu cầu hỏi giá`) | 51 | M3 |
| `price_calculate_request` | Yêu cầu tính giá — chờ lập phiếu tính giá | price_calculate_requests | ERP | cả 2 (ERP bị chặn) | 1 | `status=2` | lập chứng từ | HRM | `/sale/price-calculate-requests/:id` | permission | `Tính giá bán hàng hoá` (api, MW), company (`canReject`) | 5 | ERP#36, M4 |
| `product_price_approval` | Duyệt giá bán (hàng × ĐVT × công ty) | product_approves | ERP | cả 2 (ERP: `ManufactureExpectPriceMailJob` xoá) | 1 | có dòng = đang chờ (xong thì **xoá cứng**) | duyệt | HRM | `/finance/product-price-approvals` | permission | `Duyệt giá bán hàng hoá` (api, MW), `pa.company_id` = công ty đang làm | 1 | ERP#18, M5 |

### 1.5 Đặt mua hàng (trong nước · ngoài · nhập khẩu)

| doc_type | Tên loại phiếu | Bảng | Sở hữu | Ghi được từ | Cấp | Trạng thái chờ | Bước | handler | Đường mở | gate_type | Gate chi tiết | Chờ | Nguồn |
|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| `root_order_request` | Yêu cầu đặt hàng — TP | root_order_requests | ERP | ERP | 1 | `status=2` | duyệt | ERP | rootOrderRequest.show | permission | `Trưởng phòng duyệt yêu cầu đặt hàng` (web), department | 5 | ERP#20 |
| `root_order_request` | ↳ NV mua hàng | root_order_requests | ERP | ERP | 2 | `status=3` | duyệt | ERP | rootOrderRequest.show | assigned_buyer | NV mua hàng phụ trách thương hiệu × hãng × công ty, không cần quyền | 209 | ERP#20 |
| `inland_order_request` | YCĐH ngoài — TP | inland_order_requests | ERP | ERP | 1 | `status=6` | duyệt | ERP | inlandOrderRequest.show | permission | `Duyệt yêu cầu đặt hàng ngoài` (web), department | 8 | ERP#21 |
| `inland_order_request` | ↳ Kiểm soát | inland_order_requests | ERP | ERP | 2 | `status=2` | duyệt | ERP | inlandOrderRequest.show | permission | `Kiểm soát yêu cầu đặt hàng ngoài` (web), company của người lập | 2 | ERP#21 |
| `inland_order_summary_new` | Đơn hỏi hàng – PO trong nước | inland_order_summary_news | ERP | ERP | 1 | `status=5` (type 1, 2) | duyệt | ERP | inlandOrderSummaryNew.show | permission | `Duyệt đơn hỏi hàng - PO trong nước` (web), company | 24 | ERP#22 |
| `inland_purchase_invoice` | PI trong nước | inland_purchase_invoices | ERP | ERP | 1 | `status=2` | duyệt | ERP | inlandPurchaseInvoice.show | permission | `Duyệt PI mua hàng trong nước` (web), company | 5 | ERP#23 |
| `inland_buy_contract` | HĐ mua hàng trong nước + PLBS + ĐH nguyên tắc | inland_buy_contract_news | ERP | ERP | 1 | `status=2` (type 1–5) | duyệt | ERP | inlandBuyContractNew.show | permission | `Duyệt hợp đồng mua hàng trong nước` (web), company | 29 | ERP#24 |
| `rule_inland_buy_contract` | HĐ nguyên tắc đặt hàng trong nước | rule_inland_buy_contracts | ERP | ERP | 1 | `status=2` | duyệt | ERP | ruleInlandBuyContract.show | permission | `Duyệt hợp đồng mua hàng trong nước` (web), company | 0 | ERP#25 |
| `inland_buy_contract_old` | HĐĐH ngoài (mẫu cũ) | inland_buy_contracts | ERP | ERP | 1 | `status=2` | duyệt | ERP | inlandBuyContract.show | permission + approver | `Duyệt hợp đồng đặt hàng ngoài` (web) + đúng `approver_id` | 3 | ERP#26 |
| `inland_buy_contract_annex` | Phụ lục HĐ mua hàng ngoài | inland_buy_contract_annexes | ERP | ERP | 1 | `status=2` | duyệt | ERP | inlandBuyContractAnnex.show | permission + approver | như trên | 0 | ERP#27 |
| `inland_buy_contract_annex2` | Phụ lục giảm HĐ mua hàng ngoài | inland_buy_contract_annex2 | ERP | ERP | 1 | `status=2` | duyệt | ERP | inlandBuyContractAnnex2.show | permission + approver | như trên | 0 | ERP#28 |
| `buy_contract2` | HĐ đặt hàng nhập khẩu | buy_contract2 | ERP | ERP | 1 | `status=2` | duyệt | ERP | buyContract2.show | permission | `Duyệt hợp đồng mua hàng nhập khẩu` (web), company | 1 | ERP#29 |
| `buy_contract_annex2` | Phụ lục HĐ mua hàng nhập khẩu | buy_contract_annex2 | ERP | ERP | 1 | `status=2` | duyệt | ERP | buyContractAnnex2.show | permission | `Duyệt phụ lục hợp đồng mua hàng` (web), company | 1 | ERP#30 |
| `order_summary2` | Đơn hỏi hàng – PO nhập khẩu | order_summary2 | ERP | ERP | 1 | `status=5` | duyệt | ERP | orderSummary2.show | permission | `Duyệt đơn hỏi hàng - PO nhập khẩu` (web), company | 0 | ERP#31 |
| `purchase_invoice` | PI nhập khẩu | purchase_invoices | ERP | ERP | 1 | `status=2` | duyệt | ERP | purchaseInvoice.show | permission | `Duyệt PI mua hàng nhập khẩu` (web), company | 0 | ERP#32 |
| `custom_declaration` | Tờ khai hải quan | custom_declarations | ERP | ERP | 1 | `status=2` | duyệt | ERP | customDeclaration.show | permission | `Duyệt tờ khai hải quan` (web), company | 0 | ERP#33 |
| `order_import_request` | Tổng hợp chi phí nhập khẩu | order_import_requests | ERP | ERP | 1 | `status=2` | duyệt | ERP | orderImportRequest.show | permission | `Kế toán mua hàng` (web), company của người lập | 0 | ERP#34 |
| `delivery_cost_asking_request` | Yêu cầu hỏi giá vận chuyển | delivery_cost_asking_requests | ERP | ERP | 1 | `status=2` | duyệt | ERP | DeliveryCostAskingRequest.show | permission | `Mua hàng` (web), company | 0 | ERP#37 |
| `assign_department_ballot` | Phân công phòng phụ trách thương hiệu – hãng | assign_department_ballots | ERP | ERP | 1 | `status=2` | duyệt | ERP | assign-department-brand.show | permission | `Duyệt phiếu phân công phòng phụ trách thương hiệu hãng sản xuất` (web), company | 7 | ERP#41 |

### 1.6 Mua dịch vụ

| doc_type | Tên loại phiếu | Bảng | Sở hữu | Ghi được từ | Cấp | Trạng thái chờ | Bước | handler | Đường mở | gate_type | Gate chi tiết | Chờ | Nguồn |
|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| `buy_service_request` | Yêu cầu mua dịch vụ — TP | buy_service_requests | ERP | cả 2 | 1 | `status=2` | duyệt | HRM | `/finance/buy-service-requests/:id` | permission | `Trưởng phòng duyệt yêu cầu mua dịch vụ` (chỉ có guard web, CEP). ⚠ HRM không lọc phòng/công ty; thẻ ERP lọc department ⇒ registry nên dùng department | 0 | ERP#38, F20 |
| `buy_service_request` | ↳ Ban kiểm soát | buy_service_requests | ERP | cả 2 | 2 | `status=3` | duyệt | HRM | như trên | permission | `Ban kiểm soát duyệt giá mua dịch vụ` (chỉ web, CEP), company | 0 | ERP#38, F20 |
| `buy_service_contract` | Hợp đồng mua dịch vụ | buy_service_contracts | ERP | ERP | 1 | `status=2` | duyệt | ERP | buyServiceContract.show | permission | `Duyệt hợp đồng mua dịch vụ` (web), company | 0 | ERP#39 |
| `buy_service_accounting_request` | YC hạch toán mua dịch vụ | buy_service_accounting_requests | ERP | cả 2 | 1 | `status=2` | lập chứng từ | HRM | `/finance/buy-service-accounting-requests/:id` → `/finance/buy-service-accountings/create` | permission | `Hạch toán mua dịch vụ` (MW api **và** CEP), company. ⚠ Lớp MW chỉ cho 2/41 người qua | 2 | ERP#40, F21 |

### 1.7 Kho — xuất · nhập · chuyển

| doc_type | Tên loại phiếu | Bảng | Sở hữu | Ghi được từ | Cấp | Trạng thái chờ | Bước | handler | Đường mở | gate_type | Gate chi tiết | Chờ | Nguồn |
|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| `product_export_request` | YC xuất hàng — KT kho lập ĐNXK / phiếu xuất thẳng | product_export_requests | ERP | cả 2 | 1 | `status=2` | lập chứng từ | HRM ⚠ | `/finance/product-export-requests/:id` | permission | `Kế toán kho` + company. HRM chốt bằng **HLP** (`isCurrentEmployeeHasPermission`, guard api), ⚠ chỉ 3/75 người giữ quyền qua được | 16 | ERP#42, F25/AS14 |
| `product_export_request` | ↳ TP duyệt vượt hạn mức / hàng mượn | product_export_requests | ERP | ERP | 2 | `status=10` | duyệt | ERP | productExportRequest.show | permission | type ≠ mượn: `Trưởng phòng duyệt xuất hàng vượt hạn mức công nợ`; type mượn: `Trưởng phòng duyệt hàng mượn` (web), department | 1 | ERP#42 |
| `product_export_request` | ↳ BGĐ | product_export_requests | ERP | ERP | 3 | `status=11` | duyệt | ERP | productExportRequest.show | permission | `Ban giám đốc duyệt xuất hàng vượt hạn mức công nợ` / `Ban giám đốc duyệt hàng mượn` (web), company | 0 | ERP#42 |
| `product_import_request` | YC nhập hàng — KT kho lập ĐNNK / phiếu nhập thẳng | product_import_requests | ERP | cả 2 | 1 | `status=2` | lập chứng từ | HRM | `/finance/product-import-requests/:id` | permission | `Kế toán kho` (CEP). ⚠ Nhánh ĐNNK của HRM không lọc công ty (nhánh nhập thẳng có lọc) | 27 | ERP#43, F5 |
| `product_import_request` | ↳ TP | product_import_requests | ERP | cả 2 | 2 | `status=12` | duyệt | HRM | như trên | permission | `Trưởng phòng duyệt yêu cầu nhập hàng` (CEP). ⚠ HRM không lọc phòng/công ty; thẻ ERP lọc department ⇒ registry dùng department | 9 | ERP#43, F5 |
| `product_import_request` | ↳ Ban kiểm soát | product_import_requests | ERP | cả 2 | 3 | `status=10` | duyệt | HRM | như trên | permission | `Ban kiểm soát duyệt giá nhập hàng trả lại` (CEP), company | 0 | ERP#43, F5 |
| `product_import_request` | ↳ BGĐ | product_import_requests | ERP | cả 2 | 4 | `status=11` | duyệt | HRM | như trên | permission | `BGD duyệt giá nhập hàng trả lại` (CEP), company | 0 | ERP#43, F5 |
| `warehouse_export_request` | Đề nghị xuất kho — thủ kho lập phiếu xuất kho | warehouse_export_requests | ERP | cả 2 (HRM chỉ sửa/huỷ) | 1 | `status=2` | lập chứng từ | ERP | warehouseExportRequest.show | warehouse_stocker | Thủ kho của `warehouse_id` (`isWarehouseStocker`). Thẻ ERP cần thêm quyền `Thủ kho` | 84 | ERP#45 |
| `warehouse_export` | Phiếu xuất kho — KT kho lập phiếu xuất hàng | warehouse_exports | ERP | cả 2 | 1 | `status=2` | lập chứng từ | HRM ⚠ | `/finance/product-exports/create` (từ phiếu xuất kho) | permission | `Kế toán kho` (HLP, guard api) + company. ⚠ Cùng khe HLP như `product_export_request` cấp 1 | 70 | ERP#44 |
| `warehouse_import_request` | Đề nghị nhập kho — thủ kho lập phiếu nhập kho | warehouse_import_requests | ERP | cả 2 | 1 | `status=2` | lập chứng từ | HRM | `/finance/warehouse-import-requests/:id` → `/finance/warehouse-imports/create` | warehouse_stocker | Thủ kho của `warehouse_id` (`assertCanCreateFrom`), không cần quyền | 50 | ERP#47, F6 |
| `warehouse_import` | Phiếu nhập kho — KT kho lập phiếu nhập hàng | warehouse_imports | ERP | cả 2 | 1 | `status=2` | lập chứng từ | HRM | `/finance/warehouse-imports/:id` → `/finance/product-imports/create` | permission | `Kế toán kho` (CEP), company, type ≠ 5 | 12 | ERP#46, F7 |
| `product_transfer_request` | Yêu cầu chuyển hàng — KT kho lập YCXH loại 7 | product_transfer_requests | ERP | cả 2 | 1 | `status=2` | lập chứng từ | HRM | `/finance/product-transfer-requests/:id` | permission | `Kế toán kho` (CEP), company. ⚠ `store` không kiểm lại từng id (chỉ popup lọc) | 9 | ERP#48, F1 |
| `join_export_request` | Yêu cầu xuất ghép | join_export_requests | ERP | ERP | 1 | `status=2` | lập chứng từ | ERP | joinExportRequest.show | permission | `Kế toán kho` (web), company | 1 | ERP#49 |
| `split_export_request` | Yêu cầu xuất tách | split_export_requests | ERP | ERP | 1 | `status=2` | lập chứng từ | ERP | splitExportRequest.show | permission | `Kế toán kho` (web), company | 1 | ERP#50 |
| `product_import_direct_transfer` | Điều chuyển hàng nhập thẳng | product_import_direct_transfers | ERP | cả 2 | 1 | `status=2` | duyệt | HRM | `/finance/product-import-direct-transfers/:id` | permission | `Kế toán kho` (CEP), company | 1 | ERP#59, F10 |
| `exc_shortage_warehouse_import` | Báo thừa / thiếu nhập kho | exc_shortage_warehouse_imports | ERP | ERP | 1 | `status=2` | duyệt | ERP | warehouseImport.excShortage.show | permission | `Duyệt phiếu báo hàng thừa, thiếu nhập kho` (web), company | 10 | ERP#60 |
| `inventory_discrepancy_handling_import` | Xử lý hàng thiếu nhập kho | inventory_discrepancy_handling_imports | ERP | ERP | 1 | `status=4` | duyệt | ERP | inventory.discrepancy.show | permission | `Duyệt phiếu xử lý hàng thiếu nhập kho` (web), company | 0 | ERP#61 |
| `delivery_request` | Yêu cầu vận chuyển — thủ kho duyệt | delivery_requests | ERP | cả 2 | 1 | `status=2` | duyệt | HRM | `/finance/delivery-requests/:id` | warehouse_stocker | Thủ kho các kho trong YCXH nguồn (`isCurrentStocker`). Bảng rỗng, route sống ở cả 2 nơi | 0 | F18 (ERP web.php:6459) |

### 1.8 Hàng mượn · hàng giữ

| doc_type | Tên loại phiếu | Bảng | Sở hữu | Ghi được từ | Cấp | Trạng thái chờ | Bước | handler | Đường mở | gate_type | Gate chi tiết | Chờ | Nguồn |
|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| `borrow_export_request` | Yêu cầu xuất mượn — KT kho lập phiếu xuất mượn | borrow_export_requests | ERP | cả 2 | 1 | `status=2` | lập chứng từ | HRM | `/finance/borrow-export-requests/:id` → `/finance/borrow-exports/create` | permission | `Kế toán kho` (CEP). ⚠ HRM không lọc công ty | 0 | ERP#51, F19 |
| `borrow_sell_request` | YC xuất bán hàng mượn — KT kho lập phiếu | borrow_sell_requests | ERP | cả 2 | 1 | `status=2` | lập chứng từ | **ERP** | borrowSellRequest.show | permission | `Kế toán kho` (web), company. HRM chỉ làm được type 1 (hàng thường); type 2 (KM) bị từ chối ở `BorrowSellService:89` ⇒ chưa trọn | 0 | ERP#52, F16 |
| `borrow_sell_request` | ↳ TP | borrow_sell_requests | ERP | cả 2 | 2 | `status=10` | duyệt | HRM | `/finance/borrow-sell-requests/:id` | permission | `Trưởng phòng duyệt xuất hàng vượt hạn mức công nợ` (CEP), department | 0 | ERP#52, F16 |
| `borrow_sell_request` | ↳ BGĐ | borrow_sell_requests | ERP | cả 2 | 3 | `status=11` | duyệt | HRM | như trên | permission | `Ban giám đốc duyệt xuất hàng vượt hạn mức công nợ` (CEP), company | 0 | ERP#52, F16 |
| `borrow_extend_request` | Gia hạn hàng mượn — TP | borrow_extend_requests | ERP | cả 2 | 1 | `status=4` | duyệt | HRM | `/finance/borrow-extend-requests/:id` | permission | `Trưởng phòng duyệt hàng mượn` (chỉ web, CEP), department + company | 0 | ERP#53, F17 |
| `borrow_extend_request` | ↳ BGĐ | borrow_extend_requests | ERP | cả 2 | 2 | `status=5` | duyệt | HRM | như trên | permission | `Ban giám đốc duyệt hàng mượn` (chỉ web, CEP), company | 1 | ERP#53, F17 |
| `borrow_extend_request` | ↳ KT kho | borrow_extend_requests | ERP | cả 2 | 3 | `status=2` | duyệt | HRM | như trên | permission | `Kế toán kho` (CEP), company | 1 | ERP#53, F17 |
| `product_prepick_request` | YC xuất giữ — TP | product_prepick_requests | ERP | cả 2 | 1 | `status=6` | duyệt | HRM | `/finance/product-prepick-requests/:id` | permission | `Trưởng phòng duyệt hàng giữ` (chỉ web, CEP), department + company | 2 | ERP#54, F13 |
| `product_prepick_request` | ↳ BGĐ | product_prepick_requests | ERP | cả 2 | 2 | `status=4` | duyệt | HRM | như trên | permission | `Ban giám đốc duyệt hàng giữ` (chỉ web, CEP), company | 1 | ERP#54, F13 |
| `product_prepick_request` | ↳ KT lập phiếu xuất giữ | product_prepick_requests | ERP | cả 2 | 3 | `status=2` | lập chứng từ | HRM | `/finance/warehouse-prepick-requests/create` | permission | `Kế toán duyệt hàng giữ` (chỉ web, CEP), company | 3 | ERP#54, F13 |
| `warehouse_prepick_request` | Phiếu xuất giữ — BKS duyệt | warehouse_prepick_requests | ERP | cả 2 (HRM chỉ lập/sửa) | 1 | `status=4` | duyệt | ERP | warehousePrepickRequest.show | permission | `Ban kiểm soát duyệt giữ hàng` (web), company. HRM không có route BKS | 0 | ERP#55 |
| `prepick_transfer2` | Điều chuyển hàng giữ — TP | prepick_transfer2 | ERP | cả 2 | 1 | `status=5` | duyệt | HRM | `/finance/prepick-transfer-requests/:id` | permission | `Trưởng phòng duyệt hàng giữ` (chỉ web, CEP) + phòng của **NV nhận** (`to_employee_id`) | 1 | ERP#56, F14 |
| `prepick_transfer2` | ↳ BGĐ | prepick_transfer2 | ERP | cả 2 | 2 | `status=4` | duyệt | HRM | như trên | permission | `Ban giám đốc duyệt hàng giữ` (CEP), company | 0 | ERP#56, F14 |
| `prepick_transfer2` | ↳ KT | prepick_transfer2 | ERP | cả 2 | 3 | `status=2` | duyệt | HRM | như trên | permission | `Kế toán duyệt hàng giữ` (CEP), company | 1 | ERP#56, F14 |
| `prepick_extend_request` | Gia hạn hàng giữ — TP | prepick_extend_requests | ERP | cả 2 | 1 | `status=5` | duyệt | HRM | `/finance/prepick-extend-requests/:id` | permission | `Trưởng phòng duyệt hàng giữ` (CEP), department + company | 0 | ERP#57, F12 |
| `prepick_extend_request` | ↳ BGĐ | prepick_extend_requests | ERP | cả 2 | 2 | `status=4` | duyệt | HRM | như trên | permission | `Ban giám đốc duyệt hàng giữ` (CEP), company | 1 | ERP#57, F12 |
| `prepick_extend_request` | ↳ KT | prepick_extend_requests | ERP | cả 2 | 3 | `status=2` | duyệt | HRM | như trên | permission | `Kế toán duyệt hàng giữ` (CEP), company | 3 | ERP#57, F12 |
| `prepick_cancel_request` | Yêu cầu huỷ hàng giữ — lập phiếu huỷ giữ | prepick_cancel_requests | ERP | cả 2 | 1 | `status=2` | lập chứng từ | HRM | `/finance/prepick-cancel-requests/:id` → `/finance/prepick-cancels/create` | permission | `Quản lý giữ hàng` (chỉ web, CEP). ⚠ HRM không lọc công ty | 1 | ERP#58, F11 |

### 1.9 Kiểm kê

| doc_type | Tên loại phiếu | Bảng | Sở hữu | Ghi được từ | Cấp | Trạng thái chờ | Bước | handler | Đường mở | gate_type | Gate chi tiết | Chờ | Nguồn |
|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| `self_inventory` | Kiểm kê theo hàng hoá — BKS duyệt kết quả | self_inventories | ERP | cả 2 | 1 | `status=2` | duyệt | HRM | `/warehouse/self-inventories/:id` | permission | `Ban kiểm soát duyệt kết quả kiểm kê` (CEP), company (cả ERP lẫn HRM đều không lọc công ty) | 0 | ERP#64, F8 |
| `position_inventory_result` | Kết quả kiểm kê vị trí | position_inventories (type 1) | ERP | cả 2 | 1 | `status=2` | duyệt | HRM | `/warehouse/position-inventory-results/:id` | permission | `Ban kiểm soát duyệt kết quả kiểm kê` (CEP), company | 0 | ERP#65, F9 |
| `warehouse_inventory_import` | Nhập kho điều chỉnh kiểm kê | warehouse_inventory_imports | ERP | ERP | 1 | `status=1` | duyệt | ERP | warehouseInventoryImport.show | permission | `Kế toán kho` (web), company | 0 | ERP#62 |
| `warehouse_inventory_export` | Xuất kho điều chỉnh kiểm kê | warehouse_inventory_exports | ERP | ERP | 1 | `status=1` | duyệt | ERP | warehouseInventoryExport.show | permission | `Kế toán kho` (web), company | 0 | ERP#63 |
| `inventory_audit_report` | Biên bản xử lý thừa thiếu sau kiểm kê | inventory_audit_reports | ERP | ERP | 1 | `status=1` | duyệt | ERP | inventoryAuditReport.show | permission | `Duyệt biên bản xử lý hàng thừa, thiếu sau kiểm kê` (web), company. Bảng rỗng, route sống | 0 | ERP#67 |

### 1.10 Thu chi

| doc_type | Tên loại phiếu | Bảng | Sở hữu | Ghi được từ | Cấp | Trạng thái chờ | Bước | handler | Đường mở | gate_type | Gate chi tiết | Chờ | Nguồn |
|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| `bill_payment_request` | Đề nghị thanh toán — TP | bill_payment_requests | ERP | cả 2 | 1 | `status=2` | duyệt | HRM | `/finance/bill-payment-requests/:id` | permission | `Trưởng phòng duyệt đề nghị thanh toán` (CEP) + department + company (`canApproveAtCurrentStatus`) | 8 | ERP#68, F15 |
| `bill_payment_request` | ↳ KT công nợ | bill_payment_requests | ERP | cả 2 | 2 | `status=3` | duyệt | HRM | như trên | permission | `Kế toán công nợ duyệt đề nghị thanh toán` (CEP), company | 60 | ERP#68, F15 |
| `bill_payment_request` | ↳ KT trưởng | bill_payment_requests | ERP | cả 2 | 3 | `status=4` | duyệt | HRM | như trên | permission | `Kế toán trưởng duyệt đề nghi thanh toán` (CEP), company | 70 | ERP#68, F15 |
| `bill_payment_request` | ↳ BGĐ | bill_payment_requests | ERP | cả 2 | 4 | `status=5` | duyệt | HRM | như trên | permission | `Ban giám đốc duyệt đề nghi thanh toán` (CEP), company | 1 | ERP#68, F15 |
| `bill_payment_request` | ↳ KT thanh toán lập phiếu chi / UNC | bill_payment_requests | ERP | cả 2 | 5 | `status=6` | lập chứng từ | HRM | `/finance/bill-payments/create` hoặc `/finance/bill-payment-authorizations/create` | permission | `Kế toán thanh toán` (CEP, `isAccountant`), company | 56 | ERP#68, F15 |
| `bill_payment` | Phiếu chi — Thủ quỹ | bill_payments | ERP | cả 2 | 1 | `status=2` | duyệt | HRM | `/finance/bill-payments/:id` | permission | `Thủ quỹ duyệt phiếu chi` (CEP), company | 2 | ERP#69, F4 |
| `bill_payment` | ↳ KT trưởng (nhánh B, type 4) | bill_payments | ERP | cả 2 | 2 | `status=5` | duyệt | HRM | như trên | permission | `Kế toán trưởng duyệt phiếu chi` (CEP), company | 0 | ERP#69, F4 |
| `bill_income` | Phiếu thu — Thủ quỹ | bill_incomes | ERP | cả 2 | 1 | `status=2` | duyệt | HRM | `/finance/bill-incomes/:id` | permission | `Thủ quỹ duyệt phiếu thu` (CEP), company (HRM chưa so công ty) | 0 | ERP#70, F2 |
| `bill_income_request` | Đề nghị thu tiền — KT lập phiếu thu | bill_income_requests | ERP | cả 2 | 1 | `status=2` | lập chứng từ | HRM | `/finance/bill-income-requests/:id` → `/finance/bill-incomes/create` | permission | `Kế toán thanh toán` (CEP), company. ERP còn nhận `Kế toán`; HRM chỉ nhận `Kế toán thanh toán` | 3 | ERP#71, F22 |
| `bill_adjust_dept_request` | YC điều chỉnh công nợ — KT lập phiếu điều chỉnh | bill_adjust_dept_requests | ERP | cả 2 | 1 | `status=2` | lập chứng từ | HRM ⚠ | `/finance/bill-adjust-dept-requests/:id` → `/finance/bill-adjust-depts/create` | permission | `Kế toán thanh toán` (MW api + CEP), company. ⚠ Lớp MW chỉ thấy role HRM-type (2/55 người) | 26 | ERP#72, F23 |
| `addition_accounting_request` | YC hạch toán bổ sung — KT lập phiếu điều chỉnh | addition_accounting_requests | ERP | cả 2 | 1 | `status=2` | lập chứng từ | HRM ⚠ | `/finance/addition-accounting-requests/:id` → `/finance/bill-adjust-depts/create` | permission hoặc support_department | type ≠ 7: `Kế toán thanh toán` / `Kế toán` (CEP), company. type 7: support_department. ⚠ Lớp MW như dòng trên. Chưa xác nhận HRM lập được phiếu chéo công ty cho type 7 | **38** (rà lại 22/10: type 7 phải có phòng hỗ trợ — #2017 không ai thấy) | ERP#73, F24 |

### 1.11 Hạch toán · quyết toán

| doc_type | Tên loại phiếu | Bảng | Sở hữu | Ghi được từ | Cấp | Trạng thái chờ | Bước | handler | Đường mở | gate_type | Gate chi tiết | Chờ | Nguồn |
|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| `settlement_contract` | Quyết toán HĐ — TP | settlement_contracts | ERP | ERP | 1 | `status=2` | duyệt | ERP | settlementContract.show | permission | `Trưởng phòng duyệt quyết toán hợp đồng` (web), department | 18 | ERP#75 |
| `settlement_contract` | ↳ BGĐ | settlement_contracts | ERP | ERP | 2 | `status=3` | duyệt | ERP | settlementContract.show | approver | `valid_approver_id` | 0 | ERP#75 |
| `settlement_contract` | ↳ KT | settlement_contracts | ERP | ERP | 3 | `status=4` | duyệt | ERP | settlementContract.show | permission | `Kế toán duyệt quyết toán hợp đồng` (web), company | 204 | ERP#75 |
| `service_accounting_request` | Hạch toán yêu cầu làm dịch vụ | service_accounting_requests | ERP | ERP | 1 | `status=2` | duyệt | ERP | serviceAccountingRequest.show | permission | `Hạch toán yêu cầu làm dịch vụ` (web), company của người lập | 11 | ERP#7 |
| `monthly_commission_accounting_request` | YC hạch toán hoa hồng tháng | monthly_commission_accounting_requests | ERP | cả 2 | 1 | `status=2` | duyệt | ERP | monthlyCommissionAccountingRequest.show | permission | `Duyệt yêu cầu hạch toán hoa hồng tháng` (web), company. HRM có đường ghi qua `bill-adjust-depts` nhưng không có màn nào dẫn tới ⇒ ERP. Bảng rỗng | 0 | ERP#76 |
| `bill_commission_settlement_quarter` | Quyết toán hoa hồng quý | bill_commission_settlement_quarters | ERP | ERP | 1 | `status=2` | duyệt | ERP | bill_commission_settlement_quarters.show | permission | `Duyệt quyết toán hoa hồng quý` (web), company | 0 | ERP#77 |
| `bill_productivity_settlement_quarter` | Quyết toán năng suất quý | bill_productivity_settlement_quarters | ERP | ERP | 1 | `status=2` | duyệt | ERP | bill_productivity_settlement_quarters.show | permission | `Duyệt quyết toán hoa hồng quý` (web, dùng chung), company | 0 | ERP#78 |
| `bill_commission_settlement_month` | Quyết toán hoa hồng tháng | bill_commission_settlement_months | ERP | ERP | 1 | `status=2` | duyệt | ERP | bill_commission_settlement_months.show | permission | `Duyệt quyết toán hoa hồng quý` (web), company. Bảng rỗng | 0 | ERP#79 |
| `bill_bonus_business` | Quyết toán thưởng kinh doanh | bill_bonus_business | ERP | ERP | 1 | `status=2` | duyệt | ERP | bill_bonus_business.show | permission | `Duyệt quyết toán hoa hồng quý` (web), company. Bảng rỗng | 0 | ERP#80 |
| `bonus_end_year_settlement` | Quyết toán thưởng cuối năm | bonus_end_year_settlements | ERP | ERP | 1 | `status=2` | duyệt | ERP | bonus_end_year_settlements.show | permission | `BGĐ duyệt quyết toán năm` (web), company. Bảng rỗng | 0 | ERP#81 |
| `business_payment_profile` | Hồ sơ thanh toán phiếu công tác (ERP) | assign_business (type HO_SO_THANH_TOAN) | ERP | ERP | 1 | `status=2` | duyệt | ERP | payment-profile.show | permission | `Duyệt hồ sơ thanh toán phiếu công tác` (web), company | 0 | ERP#82 |
| `insurance_principle_accounting_request` | YC hạch toán dịch vụ cần mua (bảo hiểm) | insurance_principle_accounting_requests | ERP | ERP | 1 | `status=2` | duyệt | ERP | insurance.principleAccountingRequest.show | permission | `Duyệt yêu cầu hạch toán dịch vụ cần mua` (web), company. Bảng rỗng | 0 | ERP#83 |

### 1.12 Bảo hành · sửa chữa · CSKH

| doc_type | Tên loại phiếu | Bảng | Sở hữu | Ghi được từ | Cấp | Trạng thái chờ | Bước | handler | Đường mở | gate_type | Gate chi tiết | Chờ | Nguồn |
|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| `warranty_repair_request` | YC sửa chữa – bảo hành — phòng tiếp nhận lập phiếu xử lý | warranty_repair_requests | ERP | cả 2 | 1 | `status=2` + chưa có `warranty_repair_handle_requests` | lập chứng từ | HRM ⚠ | `/customer-care/warranty-repair-requests/:id` → `/customer-care/warranty-repair-handle-requests/create` | permission | `Xử lý yêu cầu sửa chữa` + `department_reception_id` = phòng user. HRM chốt bằng WRP (spatie, guard api): ⚠ 0 người HRM-type. `store` không kiểm lại (chỉ `prefill` kiểm) | 137 | C1 (ERP 7b) |
| `warranty_repair_handle_request` | Phiếu xử lý YC — lập phiếu cung cấp thông tin | warranty_repair_handle_requests | ERP | cả 2 | 1 | `status=2` | lập chứng từ | HRM ⚠ | `/customer-care/warranty-repair-handle-requests/:id` → `/customer-care/wr-information-requests/create` | permission | `Tạo phiếu cung cấp thông tin` (MW api + WRP). ⚠ 0 người HRM-type | 27 | C2 (ERP 7b) |
| `wr_information_request` | Phiếu cung cấp thông tin — chờ làm báo giá | wr_service_quotations (`type=0`) | ERP | cả 2 | 1 | `status=2` **VÀ** có thiết bị sửa chữa (`wr_service_quotation_products.handle_type=1`) hoặc thiết bị bảo dưỡng (`wr_service_quotation_extend_products`) | lập chứng từ | HRM | `/customer-care/wr-information-requests/:id` → `/customer-care/wr-quotations/create` | source_creator | `warranty_repair_requests.created_by` của YC gốc, không cần quyền (`canCreateQuotation`) | **188** (sửa 22/10 — bản trước đếm 4.686 do bỏ điều kiện thiết bị; 4.520 phiếu thuần bảo hành không cần báo giá) | C3 (ERP 7b) |
| `wr_service_contract` | HĐ dịch vụ sửa chữa | wr_service_contracts (`type=1`) | ERP | cả 2 | 1 | `status=2` | duyệt | HRM ⚠ | `/customer-care/wr-service-contracts/:id` | approver hoặc dept_manager | `approver_id` nếu >0, nếu không thì quản lý phòng `department_id`, không cần quyền. ⚠ HRM duyệt **không nhập dữ liệu "Hỗ trợ hạch toán"** như ERP (cố ý, ghi ở entity :372) | 0 | ERP#84, C4 |
| `wr_service_contract` | ↳ PL bổ sung | wr_service_contracts (`type=3`) | ERP | ERP | 1 | `status=2` | duyệt | ERP | WarrantyRepairContractAdditionAnnex.show | approver hoặc dept_manager | `approver_id`, hoặc quản lý phòng + `!is_market` + hạn mức `department.max_value_contract` ≥ `total_after_vat` | 1 | ERP#84 |
| `wr_service_contract` | ↳ PL giảm | wr_service_contracts (`type=4`) | ERP | ERP | 1 | `status=2` (PLG_CHO_DUYET) | duyệt | ERP | WarrantyRepairContractAnnex.show | dept_manager | Quản lý phòng `department_id`. Nhánh quyền `Duyệt PL giảm HDDV` chết (quyền không tồn tại) | 0 | ERP#84 |
| `wr_import_result` | Nhập kết quả giao việc | wr_import_results | ERP | ERP | 1 | `status=2` | duyệt | ERP | WrImportResults.show | permission | `Duyệt phiếu nhập kết quả` (web), company | 290 | ERP#85 |
| `wr_assign_task_result` | BKS duyệt kết quả giao việc | wr_assign_tasks (có `parent_id`) | ERP | ERP | 1 | `status=4` | duyệt | ERP | WrApproveResults.show | permission | `Ban kiểm soát duyệt kết quả giao việc` (web), company | 0 | ERP#86 |
| `wr_accounting_service_request` | Hạch toán dịch vụ (kho) | wr_accounting_service_requests | ERP | ERP | 1 | `status=2` | duyệt | ERP | WrAccountingServiceRequest.show | permission | `Kế toán kho` (web), company | 3 | ERP#87 |
| `assembly_request` | YC lắp đặt, bàn giao | assembly_requests | ERP | ERP | 1 | `status=6` | duyệt | ERP | assemblyRequest.show | permission | `Trưởng phòng duyệt yêu cầu lắp đặt, bàn giao` (web), department | 0 | ERP#88 |
| `firm_warranty_request` | YC hãng bảo hành | firm_warranty_requests | ERP | ERP | 1 | `status=2` | duyệt | ERP | firmWarrantyRequest.show | assigned_buyer | NV mua hàng phân công theo thương hiệu × hãng × `send_company_id` | 11 | ERP#89 |
| `firm_warranty` | Thư yêu cầu hãng bảo hành — xác nhận hãng đã nhận | firm_warranties | ERP | ERP | 1 | `status=2` (DA_GUI_NCC) | tiếp nhận | ERP | firmWarranty.show | permission | `Lập phiếu xác nhận bảo hành` (web), company | 7 | ERP#90 |
| `firm_warranty_confirm` | Phiếu xác nhận bảo hành | firm_warranty_confirms | ERP | ERP | 1 | `status=2` | duyệt | ERP | firmWarrantyConfirm.show | permission | `Duyệt phiếu xác nhận bảo hành` (web), company | 0 | ERP#91 |

### 1.13 Vận chuyển

| doc_type | Tên loại phiếu | Bảng | Sở hữu | Ghi được từ | Cấp | Trạng thái chờ | Bước | handler | Đường mở | gate_type | Gate chi tiết | Chờ | Nguồn |
|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| `summary_shipping_price` | Tổng hợp giá VC quốc tế — TP | summary_shipping_prices | ERP | ERP | 1 | `status=2` | duyệt | ERP | delivery_international_general.show | permission | `Trưởng phòng duyệt giá vận chuyển quốc tế` (web), department | 0 | ERP#92 |
| `summary_shipping_price` | ↳ Ban kiểm soát | summary_shipping_prices | ERP | ERP | 2 | `status=3` | duyệt | ERP | delivery_international_general.show | permission | `Ban kiểm soát duyệt giá vận chuyển quốc tế` (web), company | 0 | ERP#92 |
| `other_delivery_trip` | Chuyến xe khác | other_delivery_trips | ERP | ERP | 1 | `status=5` | duyệt | ERP | otherDeliveryTrip.show | permission | `Duyệt chuyến xe khác` (web), company | 0 | ERP#93 |
| `delivery_cost_summary` | Tổng hợp giá vận chuyển đề xuất | delivery_cost_summaries | ERP | ERP | 1 | `status=2` | duyệt | ERP | DeliveryCostSummary.show | permission | `Duyệt giá vận chuyển` (web), company | 0 | ERP#94 |
| `delivery_contract` | Hợp đồng / phụ lục vận chuyển | delivery_contracts | ERP | ERP | 1 | `status=2` | duyệt | ERP | deliveryContract.show | permission | `Duyệt giá vận chuyển` (web), company | 0 | ERP#95 |
| `summary_order_shipping_price` | Đơn hàng vận chuyển quốc tế | summary_order_shipping_prices | ERP | ERP | 1 | `status=2` | duyệt | ERP | delivery_international_order.show | permission | `Lập đơn hàng vận chuyển quốc tế` (web), company (dùng quyền "Lập" để duyệt — giữ như code). Bảng rỗng | 0 | ERP#96 |
| `delivery_payment_request` | ĐN thanh toán chi phí vận chuyển | delivery_payment_requests | ERP | ERP | 1 | `status=2` | duyệt | ERP | deliveryPaymentRequest.show | permission | `Kế toán kho` (web), company. Bảng rỗng | 0 | ERP#97 |
| `employee_delivery_payment` | Thanh toán vận chuyển cho NV | employee_delivery_payments | ERP | ERP | 1 | `status=2` | duyệt | ERP | employeeDeliveryPayment.show | permission | `Kế toán kho` (web), company. Bảng rỗng | 0 | ERP#98 |
| `other_delivery_payment_request` | ĐN thanh toán chuyến xe khác | other_delivery_payment_requests | ERP | ERP | 1 | `status=2` | duyệt | ERP | otherDeliveryPaymentRequest.show | permission | `Kế toán kho` (web), company. Bảng rỗng | 0 | ERP#99 |

### 1.14 Họp (HRM Meeting)

| doc_type | Tên loại phiếu | Bảng | Sở hữu | Ghi được từ | Cấp | Trạng thái chờ | Bước | handler | Đường mở | gate_type | Gate chi tiết | Chờ | Nguồn |
|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| `meeting_room_booking` | Phiếu đặt phòng họp | meeting_room_bookings | HRM | HRM | 1 | `status=1` | duyệt | HRM | `/meeting/bookings` | room_manager hoặc permission | Người phụ trách đúng phòng (`meeting_room_managers`) hoặc `Duyệt phiếu đặt phòng họp` (api) (`canActOnApprovalByRoom`) | 0 | H16 |

---

## 2. Chờ nghiệp vụ chốt (chưa đưa vào danh mục)

| # | Luồng | Bảng · trạng thái | Chờ | Lý do |
|---|---|---|---:|---|
| N1 | KH phát triển thị trường NV — cấp 2 | market_employee_plans `status=3` | 13 | `MarketEmployeePlan::canApprove()` :299 trả `true` cho **mọi người** ở status 3. Thực tế hàm này chỉ dùng trong `canView`. Bước "cấp 2" thật là **duyệt KH phòng** (`market_department_plans`, đã có trong danh mục): duyệt xong tự đẩy KH NV 3→5. Đề xuất: **không tạo doc_type riêng**, coi 13 phiếu là "chờ KH phòng được duyệt". Cần nghiệp vụ xác nhận. |
| N2 | KH bán hàng NV — cấp 2 | sales_employee_plans `status=3` | 10 | `canApprove()` :499 so `approver_id`, nhưng **bảng không có cột `approver_id`** (đã kiểm `information_schema`). Nhánh còn lại = quyền TP + cùng phòng, không xét status. Hàm chỉ dùng trong `canView`. Bước thật là duyệt KH bán hàng phòng (cascade 3→5). Đề xuất như N1. |
| N3 | Yêu cầu dịch vụ trên phiếu đặt phòng | meeting_room_bookings `service_status=1` | 0 | Gate rõ (người phụ trách phòng), nhưng đây là việc chuẩn bị dịch vụ chứ không phải duyệt phiếu. Kiểm kê đề xuất không đưa vào. Cần chốt có tính là "tiếp nhận" không. (H17) |
| N4 | Báo giá BOM cấp 1 — người lập tự duyệt | quotations `is_summary=0, status=1, price_approval_level=1` | 0 | Trùng với bản nháp của chính người lập. Có hiện "chờ tự duyệt" không? (AS1) |
| N5 | Các mục ERP 7b có tính chất "lập chứng từ kế tiếp" | `delivery_trips` status 1 chờ hạch toán (91); chuyến xe khác chờ hạch toán; DS cần hạch toán chi phí VC nhanh; `wr_assign_tasks` KQ chờ hạch toán DV; phiếu chờ giao việc; hàng nhập thẳng cần xuất | — | Khảo sát trước xếp là "việc", không phải phiếu duyệt. Định nghĩa mới (22/10) có gồm "lập chứng từ kế tiếp", nên cần nghiệp vụ chốt lại từng mục. **C1/C2/C3 đã đưa vào** vì README nêu rõ C3 là ví dụ. |
| N6 | HĐ dịch vụ SC-BH type 1 — chọn nơi xử lý | wr_service_contracts type 1 st2 | 0 | Đã khai HRM, nhưng HRM duyệt **bỏ bước nhập "Hỗ trợ hạch toán"** mà ERP bắt buộc. Nếu nghiệp vụ coi dữ liệu này là một phần của bước duyệt thì phải đổi handler sang ERP. |

**Không còn luồng nào trong phạm vi có gate "mọi người duyệt" ngoài N1, N2.** AS8 (điều chỉnh giải pháp) bị fail-open ở BE nhưng màn gốc có gate (PM / TP phòng nhận) nên vẫn đưa vào danh mục.

---

## 3. Loại khỏi đợt 1

| Nhóm | Luồng | Phiếu chờ | Lý do |
|---|---|---:|---|
| Đợt 2 (nhân sự) | Timesheet H1–H11 · Human H12–H13 · Payroll H14–H15 · Training H18–H26 · Decision QĐ1–QĐ22 | ~5.000 (gồm H22 3.631) | README: đợt 2 |
| Assign legacy | AS16 phiếu đề xuất/công tác (118) · AS17 đề xuất công việc (20) · AS18 giao việc (13) · AS19 hồ sơ thanh toán (292) · AS20 đề nghị thanh toán công tác (1.041) · AS22 gia hạn/kết thúc sớm (97) | 1.581 | README: để riêng |
| Trùng | AS14 YCXH "Không duyệt" phía HRM | — | Trùng `product_export_request` cấp 1 (F25) |
| Trạng thái phản chiếu (sinh ra do chứng từ hạ nguồn, việc duyệt nằm ở doc_type khác) | `bill_payment_requests` status 7 (2) — chờ duyệt phiếu chi/UNC ⇒ đã có `bill_payment` · `product_export_requests` status 14 (1) — YC nhập hàng đẩy về ⇒ `product_import_request` · `price_calculate_requests` status 6 (0) — PTG chờ duyệt giá ⇒ `product_price_approval` · `price_asking_requests` status 5/7 cũ (18/9) — "Đang hỏi giá" ⇒ `price_asking_request_group` | 30 | Tránh đếm 2 lần |
| Thay thế | `tmp_products` status 2 (ERP#19, 0) | 0 | Route ERP bị `productMovedToHrm` chặn; HRM thay bằng `price_asking_temp_product` |
| Route chết / không còn bước chờ | UNC `bill_payment_authorizations` (ERP#74, tạo ra là đã duyệt) · Kế hoạch kiểm kê vị trí type 0 (ERP#66: route `stockApprove` trỏ hàm không tồn tại, bước thật là thủ kho nhập kết quả kiểm) · ERP#100–112 (module cũ, bảng rỗng, route trỏ hàm không tồn tại, không có trạng thái chờ) | 1 (rác 2024) | Chết |
| **Chờ giao việc** (user chốt 22/10: tính chất khác — là hàng đợi điều phối công việc theo số lượng còn lại, không phải chờ duyệt/lập chứng từ) | `wr_service_contract_reception` HĐ dịch vụ chờ giao việc (C5, 428) · PL bổ sung chờ giao việc (24) · HĐ bảo hành chờ giao việc (`type=2,status=2`, list 561 / thẻ 4.544) · YC lắp đặt / YC khác chờ giao việc | ~1.000 | Vẫn xử lý ở màn "Phiếu chờ giao việc" gốc |
| Không phải phiếu duyệt | AS13 duyệt bình luận task · AS23 duyệt loại giảm giá · `DeliveryTrip` status 2 (người tạo tự xác nhận) · `SelfInventoryRequest` status 1 (chốt của người lập) · ERP 7b: hàng chờ nhập thông tin bán hàng, hàng không được duyệt giá, hàng mượn/giữ hết hạn, tài khoản chưa phân quyền, BillAssign, cảnh báo phân công NV phụ trách hãng | — | Cảnh báo/việc cá nhân |

---

## 4. Bản đồ hook model (`saved` event)

**Cách tìm** (script trong scratchpad, chỉ đọc):
- Lớp model: lấy theo `protected $table`, có kế thừa bảng của lớp cha. Lớp không khai `$table` thì suy theo tên.
- Call-site bỏ qua event: câu lệnh có `->update(` mà gốc chuỗi là `DB::table('<bảng>')` hoặc `<Model>::where…/query()/whereIn…` (không qua `first/find/get`). Ở `product_approves` tính thêm `->delete()`, vì xoá dòng = hết chờ.
- Bổ sung: grep `$x->relation()->update(['status'…])`, vì update qua quan hệ cũng bỏ qua event.

**Giới hạn của cách tìm:**
- Chưa bắt được kiểu `$q = Model::where(…); …; $q->update()` ở câu lệnh tách rời.
- Đã loại seeder/migration/test.

**Lưu ý thiết kế:**
- Nhiều lớp ERP kế thừa cùng bảng (vd các lớp HĐ trên `firm_contracts`). Đặt listener trong `booted()` của lớp cha bằng `static::saved` thì áp cho cả lớp con. Lớp con có `boot()` riêng phải gọi `parent::boot()`.
- **Mọi call-site ở cột cuối phải gọi push thủ công** (hoặc đổi sang update qua instance), nếu không registry sẽ lệch.

| Bảng | Model ERP | Entity HRM | Call-site bỏ qua event (file:dòng) |
|---|---|---|---|
| firm_contracts | `App\Model\Sale\Firm\Contract\FirmContract` (+ lớp con HĐ/PL/HĐNT/zt) | `Modules\Finance\Entities\Contract\FirmContract`, `App\Models\TpContract`, `Modules\Human\Entities\TpFirmContract` (chỉ đọc) | HRM `Modules/Assign/Services/SettlementContractService.php:118` (TpContract con, type 2) |
| project_quotations | `App\Model\Sale\ProjectQuotation` | — | — |
| liquidation_records | `App\Model\Sale\LiquidationRecord` | — (chỉ đọc) | — |
| hand_over_works | `App\Model\Sale\HandOverWork` | — | — |
| service_export_requests · service_accounting_requests | `App\Model\Sale\ServiceExportRequest` · `ServiceAccountingRequest` | — | — |
| sales_*_plans · market_*_plans (6 bảng) | `App\Model\Plan\SalesEmployeePlan` / `SalesDepartmentPlan` / `SalesCompanyPlan`, `App\Model\Plan\Market\MarketEmployeePlan` / `MarketDepartmentPlan` / `MarketCompanyPlan` | — | Cascade KH NV 3→5 trong `SaleDepartmentPlanController@approve` (~:691-697) và `MarketDepartmentPlanController` (:649-654). Cần kiểm là update qua instance hay query khi làm hook |
| business_target_companies · business_target_for_departments | `App\Model\Target\BusinessTargetCompany` · `Target\Department\BusinessTargetForDepartment` | — | — |
| division_market_department_employees | `App\Model\Division\Employee\DivisionMarketDepartmentEmployee` | — | — |
| quotations | (`App\Quotation` + lớp con: mẫu cũ, đọc nhầm bảng HRM; không hook) | `Modules\Assign\Entities\Quotation` | HRM `Modules/Assign/Http/Controllers/Api/V1/QuotationController.php:1112`, `Modules/Assign/Services/ProspectiveProjectService.php:2107` (`Quotation::whereIn(...)->update`) |
| prospective_project_extension_requests | — | `Modules\Assign\Entities\ProspectiveProjectExtensionRequest` | — |
| hrm_contracts | `App\Model\Hrm\HrmContract`, `App\Model\Assign\HrmContract` (chỉ đọc) | `Modules\Assign\Entities\Contract\Contract` | — |
| handovers · handover_items | — | `Modules\Assign\Entities\Handover` · `HandoverItem` | — |
| request_solutions | — | `Modules\Assign\Entities\RequestSolution` | HRM `Modules/Assign/Services/ProspectiveProjectService.php:2403` |
| solution_adjustment_requests | — | `Modules\Assign\Entities\SolutionAdjustmentRequest` | — |
| solution_review_profiles | — | `Modules\Assign\Entities\SolutionReviewProfile` | HRM `Modules/Assign/Services/SolutionService.php:2913` |
| solution_module_review_profiles | — | `Modules\Assign\Entities\SolutionModuleReviewProfile` | HRM `Modules/Assign/Services/SolutionModuleService.php:1232` |
| solutions | — | `Modules\Assign\Entities\Solution` | HRM `Modules/Assign/Services/QuotationService.php:4095`, `ProspectiveProjectService.php:2046`, `PricingRequestService.php:208` (`$request->solution()->update`), `SolutionService.php:562` (bảng version, không phải `solutions`) |
| tasks | — | `Modules\Assign\Entities\Task\Task` | HRM `SolutionService.php:3110`, `SolutionModuleService.php:1551` (chỉ cột `weight`, không đổi trạng thái) |
| issues · hrm_settlement_contracts | — | `Modules\Assign\Entities\Issue` · `SettlementContract\SettlementContract` | — |
| price_asking_requests | `App\Model\Order\PriceAskingRequest` | `Modules\MasterData\Entities\PriceCalculation\PriceAskingRequest` | HRM `Modules/MasterData/Services/PriceCalculation/PriceAskingStaleCloser.php:76` |
| price_asking_request_groups | — | `…\PriceCalculation\PriceAskingRequestGroup` | HRM `PriceAskingStaleCloser.php:58` |
| price_calculate_requests | `App\Model\Order\PriceCalculateRequest` | `…\PriceCalculation\PriceCalculateRequest` | HRM `PriceCalculateFinalizer.php:284`, `PriceAskingGroupBackfill.php:159, :164` |
| product_company_coefficients | `App\Model\Product\ProductCompanyCoefficient` | `Modules\MasterData\Entities\Product\ProductCompany` | HRM (ghi `status`): `ProductLifecycleService.php:261, :392, :437`; `TempProductService.php:76`; `ProductPriceApprovalService.php:639`; `PriceCalculateWriter.php:223, :474`; `PriceCalculateFinalizer.php:223, :267`; `PriceAskingRequestWriter.php:417, :645`; `ProductWriteService.php:260, :800` — **toàn bộ ghi bằng `DB::table`, Entity không bắn event** |
| product_approves | `App\ProductApprove` | `Modules\MasterData\Entities\Product\ProductApprove` | Xoá cứng: ERP `ProductsController.php:3090`, `Jobs/ManufactureExpectPriceMailJob.php:78`; HRM `ProductLifecycleService.php:243`, `ProductPriceSetWriter.php:94`, `ProductPriceApprovalSubmitter.php:111` (+ update :119), `ProductPriceApprovalService.php:619, :764`, `ProductPriceWriter.php:228`. ⇒ Nên hook ở nơi ghi (service) chứ không hook ở model |
| root_order_requests · inland_order_requests · inland_purchase_invoices · rule_inland_buy_contracts · inland_buy_contract_annexes · inland_buy_contract_annex2 · buy_contract_annex2 · order_summary2 · purchase_invoices · order_import_requests · delivery_cost_asking_requests · assign_department_ballots | `App\Model\Order\{RootOrderRequest, InlandOrderRequest, InlandPurchaseInvoice, RuleInlandBuyContract, InlandBuyContractAnnex, InlandBuyContractAnnex2, BuyContractAnnex2, OrderSummary2, PurchaseInvoice, DeliveryCostAskingRequest}`, `App\Model\Warehouse\OrderImportRequest`, `App\Model\Order\AssignDepartmentBallot\AssignDepartmentBallot` | — | — |
| inland_order_summary_news | `App\Model\Order\InlandOrderSummaryNew` | — | ERP `app/Http/Controllers/Order/InlandPurchaseInvoiceController.php:277, :419, :769` (`$x->inland_order_summary_new()->update(['status'…])`) |
| inland_buy_contract_news · inland_buy_contracts · buy_contract2 | `App\Model\Order\InlandBuyContractNew` · `InlandBuyContract` · `BuyContract2` | `Modules\Finance\Entities\Contract\…` (chỉ đọc) | — |
| custom_declarations | `App\Model\Warehouse\CustomDeclaration` | — | ERP `app/Http/Controllers/Warehouse/OrderImportRequestController.php:259, :540, :607` |
| buy_service_requests | `App\Model\Sale\BuyServiceRequest` | `Modules\Finance\Entities\BuyServiceRequest\BuyServiceRequest` | — |
| buy_service_contracts | `App\Model\Sale\BuyServiceContract` | `Modules\Finance\Entities\Contract\BuyServiceContract` | — |
| buy_service_accounting_requests | `App\Model\Sale\BuyServiceAccountingRequest` | `Modules\Finance\Entities\BuyServiceAccountingRequest\BuyServiceAccountingRequest` | (chỉ migration backfill `updated_by`) |
| product_export_requests | `App\Model\Warehouse\ProductExportRequest` | `Modules\Assign\Entities\Warehouse\ProductExportRequest`, `Modules\Finance\Entities\ProductImportRequest\ProductExportRequest` | ERP `app/Model/Sale/SettlementContract.php:670, :686, :702` (`$this->product_export_request()->update`), `app/Model/Tech/InstallRequest.php:183, :200` (cột install). HRM `Modules/Assign/Http/Controllers/Api/V1/ProductExportRequestController.php:2010`; `Modules/Finance/Services/WarehouseImportWriteService.php:805, :1346`; `ProductImportService.php:3353, :3452`; `BorrowExportService.php:578`, `BorrowSell/BorrowSellService.php:438`, `BorrowExtendRequestService.php:545` (`borrow_status`); `DeliveryRequestWriteService.php:209` (`transition_type`) |
| product_import_requests | `App\Model\Warehouse\ProductImportRequest` | `Modules\Finance\Entities\ProductImportRequest\ProductImportRequest` | HRM `Modules/Finance/Services/ProductImportService.php:2335, :3388` |
| warehouse_exports | `App\Model\Warehouse\WarehouseExport` | `Modules\Assign\Entities\Warehouse\WarehouseExport`, `Modules\Finance\Entities\Contract\WarehouseExport` | ERP `app/Http/Controllers/HomeController.php:205` (cột `company_id`) |
| warehouse_export_requests | `App\Model\Warehouse\WarehouseExportRequest` | `Modules\Assign\Entities\Warehouse\WarehouseExportRequest` | ERP `HomeController.php:206` (cột `company_id`) |
| warehouse_imports | `App\Model\Warehouse\WarehouseImport` | `Modules\Finance\Entities\WarehouseImport\WarehouseImport`, `…\Contract\WarehouseImport` | HRM `ProductImportService.php:2312`, `Modules/Finance/Entities/ProductImport/ProductImport.php:603` |
| warehouse_import_requests | `App\Model\Warehouse\WarehouseImportRequest` | `Modules\Finance\Entities\WarehouseImportRequest\WarehouseImportRequest` | HRM `ProductImportService.php:2321`, `ProductImport.php:612` |
| product_transfer_requests | `App\Model\Warehouse\ProductTransferRequest` | `Modules\Finance\Entities\ProductTransferRequest\ProductTransferRequest` | ERP `app/Model/Warehouse/ProductExportRequest.php:2574`; HRM `Modules/Assign/Services/ProductExportRequestService.php:2483`, `Modules/Finance/Services/WarehouseImportWriteService.php:801` |
| join_export_requests · split_export_requests | `App\Model\Warehouse\JoinExportRequest` · `SplitExportRequest` | — | — |
| borrow_export_requests · borrow_extend_requests · prepick_extend_requests · prepick_cancel_requests · product_import_direct_transfers · warehouse_prepick_requests | `App\Model\Warehouse\{BorrowExportRequest, BorrowExtendRequest, PrepickExtendRequest, PrepickCancelRequest, ProductImportDirectTransfer, WarehousePrepickRequest}` | `Modules\Finance\Entities\{BorrowExport\BorrowExportRequest, BorrowExtend\BorrowExtendRequest, PrepickExtend\PrepickExtendRequest, PrepickCancel\PrepickCancelRequest, ProductImportDirectTransfer\…, PrepickExport\WarehousePrepickRequest}` | — |
| borrow_sell_requests | `App\Model\Warehouse\BorrowSellRequest` | `Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequest` | ERP `app/Model/Sale/SettlementContract.php:673, :689, :705` |
| product_prepick_requests | `App\Model\Warehouse\ProductPrepickRequest` | `Modules\Finance\Entities\PrepickExport\ProductPrepickRequest` | — |
| prepick_transfer2 | `App\Model\Warehouse\PrepickTransfer2` | `Modules\Finance\Entities\PrepickTransfer\PrepickTransferRequest` | — |
| exc_shortage_warehouse_imports | `App\Model\Warehouse\ExcShortageWarehouseImport` | — | — |
| inventory_discrepancy_handling_imports | `App\Model\Warehouse\InventoryDiscrepancyHandlingImport` | `Modules\Finance\Entities\Contract\InventoryDiscrepancyHandlingImport` (đọc) | (chỉ seeder test) |
| warehouse_inventory_imports · warehouse_inventory_exports · inventory_audit_reports | `App\Model\Warehouse\Inventory\{WarehouseInventoryImport, WarehouseInventoryExport, InventoryAuditReport}` | — | — |
| self_inventories | `App\Model\Warehouse\SelfInventory` | `Modules\Finance\Entities\SelfInventory\SelfInventory` | — |
| position_inventories | `App\Model\Warehouse\PositionInventory` | `Modules\Finance\Entities\PositionInventory\PositionInventory`, `PositionInventoryResult` (global scope type 1) | — |
| delivery_requests | `App\Model\Warehouse\DeliveryRequest` | `Modules\Finance\Entities\DeliveryRequest\DeliveryRequest` | — |
| bill_payment_requests | `App\Model\IncomeExpenditure\BillPaymentRequest` | `Modules\Finance\Entities\BillPaymentRequest\BillPaymentRequest` | ERP `app/Http/Controllers/IncomeExpenditure/BillPaymentController.php:264, :277`, `BillPaymentAuthorizationController.php:211`, `app/Model/IncomeExpenditure/BillPaymentAuthorization.php:394, :565`, `BillPayment.php:735`. HRM `Modules/Finance/Services/BillPaymentAuthorizationWriteService.php:295`, `BillPaymentApprovalFlowService.php:255, :350`, `BillPaymentWriteService.php:369` — **mọi chuyển 6→7→8 đều đi đường này** |
| bill_payments | `App\Model\IncomeExpenditure\BillPayment` | `Modules\Finance\Entities\BillPayment\BillPayment` | ERP `BillPayment.php:442` (cột tiền); HRM `BillPaymentWriteService.php:570` |
| bill_incomes | `App\Model\IncomeExpenditure\BillIncome` | `Modules\Finance\Entities\BillIncome\BillIncome` | — |
| bill_income_requests | `App\Model\IncomeExpenditure\BillIncomeRequest` | `Modules\Finance\Entities\BillIncomeRequest\BillIncomeRequest` | ERP `BillIncomeController.php:213, :223`, `app/Model/IncomeExpenditure/BillIncome.php:508`. HRM `Modules/Finance/Services/BillIncomeWriteService.php:98`, `BillIncomeApprovalService.php:85, :172` |
| bill_adjust_dept_requests | `App\Model\IncomeExpenditure\BillAdjustDeptRequest` | `Modules\Finance\Entities\BillAdjustDeptRequest\BillAdjustDeptRequest` | ERP `BillAdjustDeptController.php:250, :353, :367, :396`, `app/Model/IncomeExpenditure/BillAdjustDept.php:563`. HRM `Modules/Finance/Services/BillAdjustDeptSourceService.php:860` |
| addition_accounting_requests | `App\Model\IncomeExpenditure\AdditionAccountingRequest` | `Modules\Finance\Entities\AdditionAccountingRequest\AdditionAccountingRequest` | ERP `BillAdjustDeptController.php:264`. HRM `BillAdjustDeptSourceService.php:724, :831` |
| monthly_commission_accounting_requests | `App\Model\Sale\MonthlyCommissionAccountingRequest` | — | ERP `BillAdjustDeptController.php:257, :403`. HRM `BillAdjustDeptSourceService.php:730, :812, :837` |
| settlement_contracts | `App\Model\Sale\SettlementContract` | — (chỉ đọc) | — |
| bill_commission_settlement_quarters · bill_productivity_settlement_quarters · bill_commission_settlement_months · bill_bonus_business · bonus_end_year_settlements | `App\Model\Accounting\{BillCommissionSettlementQuarter, BillProductivitySettlementQuarter, BillCommissionSettlementMonth, BillBonusBusiness, BonusEndYearSettlement}` | — | — |
| assign_business | `App\Model\Assign\AssignBusiness` | `Modules\Assign\Entities\TpAssignBusiness` (đọc) | ERP `app/Http/Controllers/Assign/PaymentProfileController.php:251` (`$assignBusiness->parent()->update`) |
| insurance_principle_accounting_requests | `App\Model\Insurance\InsurancePrincipleAccountingRequest` | — | — |
| warranty_repair_requests | `App\Model\Customers\WarrantyRepairRequest` | `Modules\CustomerCare\Entities\WarrantyRepairRequest\WarrantyRepairRequest` | — (chuyển 2→7/8 nằm trong `WarrantyRepairHandleRequestService.php:509-513`, cần kiểm có qua instance không) |
| warranty_repair_handle_requests | `App\Model\Customers\WarrantyRepairHandleRequest` | `Modules\CustomerCare\Entities\WarrantyRepairHandleRequest\WarrantyRepairHandleRequest` | — (chuyển trạng thái ở `WrServiceQuotationService.php:1316-1317`, cần kiểm) |
| wr_service_quotations | `App\Model\Customers\WrServiceQuotation` | `Modules\CustomerCare\Entities\WrServiceQuotation\WrServiceQuotation` | ERP `app/Console/Commands/UpdateQuotationExpried.php:60` (type báo giá, hết hạn) |
| wr_service_contracts | `App\Model\Customers\WrServiceContract` | `Modules\CustomerCare\Entities\WrServiceContract\WrServiceContract`, `Modules\Finance\Entities\Contract\WrServiceContract`, `Modules\Assign\Entities\TpWrServiceContract`, `Modules\Human\Entities\TpWrServiceContract`, `App\Models\TpWrContract` | HRM `Modules/CustomerCare/Services/WrServiceContractService.php:1612` (PL theo `parent_id`), `Modules/Assign/Services/SettlementContractService.php:109` |
| wr_import_results · wr_assign_tasks | `App\Model\Customers\WrImportResult` · `WrAssignTask` | `Modules\Assign\Entities\TpWrImportResult` · `TpWrAssignTask`, `Modules\Human\Entities\TpWrAssignTask` (HRM chỉ tạo/sửa ở trạng thái nháp) | — |
| wr_accounting_service_requests · assembly_requests | `App\Model\Customers\WrAccountingServiceRequest` · `AssemblyRequest` | — · `Modules\Assign\Entities\TpAssemblyRequest` (đọc) | — |
| firm_warranty_requests · firm_warranties · firm_warranty_confirms | `App\Model\Order\FirmWarrantyRequests\FirmWarrantyRequest` · `FirmWarrantys\FirmWarranty` · `FirmWarrantyConfirms\FirmWarrantyConfirm` | — · — · `Modules\Finance\Entities\Contract\FirmWarrantyConfirm` (đọc) | — |
| summary_shipping_prices · other_delivery_trips · delivery_cost_summaries · delivery_contracts · summary_order_shipping_prices · delivery_payment_requests · employee_delivery_payments · other_delivery_payment_requests | `App\Model\ShippingQuote\SummaryShippingPrice`, `Common\OtherDeliveryTrip`, `Common\DeliveryCostSummary`, `Common\DeliveryContract`, `ShippingQuote\SummaryOrderShippingPrice`, `Warehouse\DeliveryPaymentRequest`, `Warehouse\EmployeeDeliveryPayment`, `Common\OtherDeliveryPaymentRequest` | `Modules\Finance\Entities\Delivery\OtherDeliveryTrip` (đọc) | — |
| meeting_room_bookings | — | `Modules\Meeting\Entities\MeetingRoomBooking` | HRM `app/Console/Commands/SendMeetingRoomBookingReminders.php:194` (cột nhắc lịch, không đổi `status`) |

---

## 5. Tổng hợp số

Số liệu dưới đây tính bằng script từ bảng §1.

| Chỉ số | Số |
|---|---:|
| `doc_type` khác nhau | **116** (bỏ `wr_service_contract_reception` 22/10) |
| Dòng doc_type × cấp (kể cả biến thể `firm_contract` HĐNT và 3 type của `wr_service_contract`) | **154** |
| — handler **ERP** | 81 |
| — handler **HRM** | 74. Trong đó 7 dòng có ⚠: gate HRM đang chặn phần lớn người duyệt thật (xem §7) |
| Theo bước: duyệt / tiếp nhận / lập chứng từ | 125 / 6 / 24 |
| Khoá registry cũ | 49/49 vẫn dùng (xem 4 ghi chú dưới bảng) |
| Dòng có phiếu chờ > 0 | 73 |
| **Tổng phiếu chờ trong danh mục** | **1.925** (bỏ C5 chờ giao việc 428 — user chốt 22/10; trước đó 2.353 — rà lại toàn bộ 22/10 theo điều kiện màn gốc: C3 4.686→188, C5 243→428, HĐ bán 11→14, hạch toán bổ sung 39→38; bản đầu ghi 6.664) |
| — chia theo handler | ERP 962 · HRM 963 |
| Chờ nghiệp vụ chốt | 6 mục (N1–N6), trong đó N1 + N2 có 23 phiếu |
| Loại khỏi đợt 1 | đợt 2 (5 module) · Assign legacy 6 luồng (1.581 phiếu) · 4 trạng thái phản chiếu (30 phiếu) · ERP#66, #74, #100–112 (chết) · các mục không phải phiếu duyệt |

4 khoá registry cũ dùng với nghĩa khác trước:
- `price_asking_request`: chỉ còn cấp PTKD; bước XNK chuyển sang `price_asking_request_group`.
- `price_calculate_request`: bước đổi thành "lập chứng từ" (lập phiếu tính giá).
- `sales_employee_plan`: chỉ còn cấp 1 (cấp 2 → N2).
- `wr_service_contract`: tách theo type (type 1 = HRM, PL = ERP).

## 6. Kiểm chứng handler = HRM (tóm tắt bằng chứng)

HRM chỉ được chọn khi có cả 3 thứ:
1. Route HRM.
2. Service ghi trạng thái phiếu gốc **đúng giá trị như ERP**.
3. Trang client gọi tới service đó.

| doc_type · cấp | Route HRM | Ghi trạng thái phiếu gốc | ERP tương ứng |
|---|---|---|---|
| `product_transfer_request` 1 | `POST /assign/product-export-requests` (Assign api:732) | `ProductExportRequestService::syncTransferRequests` :734 → 1 | `ProductExportRequest::syncProductTransferRequests` :2105 → 1 |
| `product_import_request` 1 | `POST /product-import-requests/{id}/warehouse-import-requests` (Finance api:582); `POST /product-imports` (:516) | `WarehouseImportRequestService` :194/:198 → 7/1; `ProductImportService::markParentUsed` :2300 → 7 | `ProductImportRequest::approve` :1549 |
| `product_import_request` 2/3/4 | Finance api:576/577/578 | `ProductImportRequestService` :626 / :655 / :684 / :712 | `controlDepartmentManagerApprove` / `controlBoardApprove` / `boardOfManagerApprove` |
| `warehouse_import_request` 1 | `POST /warehouse-imports` (:637) | `WarehouseImportWriteService::approveRequest` :787 (WIR→1, PIR→4) | `WarehouseImportRequest::approve` :435 |
| `warehouse_import` 1 | `POST /product-imports` (:516) | `ProductImportService::markParentUsed` (WI→7, WIR→7, PIR→9) | `WarehouseImport::approve` :1567 |
| `warehouse_export` 1 | `POST /assign/warehouse-exports/{id}/product-exports` (Assign api:814) | `ProductExportService::createFromWarehouseExport` :352/:357/:364 | `ProductExportsController@store` :859 |
| `product_export_request` 1 | Assign api:737 (ĐNXK), :742 (xuất thẳng) | `WarehouseExportRequestService` :242/:246; `ProductExportService` :674 | `ProductExportRequest::approve` :2844 |
| `prepick_cancel_request` 1 | `POST /prepick-cancels` (:1034) | `PrepickCancelService` :352 → 1 | `PrepickCancelsController@store` :158 |
| `product_prepick_request` 1/2/3 | `POST /product-prepick-requests/{id}/approve` (:949); `POST /warehouse-prepick-requests` (:978) | `ProductPrepickRequestService::approve` :839; `WarehousePrepickRequestService` :504 → 1 | `approve` + `WarehousePrepickRequestsController@store` :219 |
| `borrow_export_request` 1 | `POST /borrow-exports` (:1518) | `BorrowExportService::approveParent` :594 | `BorrowExportController@store` :220 |
| `borrow_sell_request` 2/3 | Finance api:1245–1247 | `BorrowSellRequestService` :579/:592/:605 | `managerApprove` |
| `borrow_extend_request`, `prepick_extend_request`, `prepick_transfer2` | :1326 / :909 / :1013 | service `approve` :549 / :763 / :828 | ERP `approve` |
| `product_import_direct_transfer`, `self_inventory`, `position_inventory_result`, `delivery_request` | :845 / :718 / :766 / :1351 | service `approve` | ERP `approve` |
| `buy_service_request` 1/2 | :1547 / :1549 | `BuyServiceRequestService` :395 / :437 | `departmentApprove` / `ksApprove` |
| `buy_service_accounting_request` 1 | `POST /buy-service-accountings` (:1603) | `BuyServiceAccountingService::afterSave` :900-921 → 3/4 | `BuyServiceAccountingController@store` |
| `bill_payment_request` 1–4 | `POST /bill-payment-requests/{id}/approve` (:1093) | `BillPaymentApprovalService::approve` ~:124 | `BillPaymentRequestController::update` :255 |
| `bill_payment_request` 5 | `POST /bill-payments` + `/{id}/submit` (:452/:457); `POST /bill-payment-authorizations` (:484) | `BillPaymentWriteService::submit` :369 → 7; UNC :295 → 8 | `BillPaymentController::store` :175 / UNC :394 |
| `bill_payment` 1/2 | `POST /bill-payments/{id}/approve` (:458) | `BillPaymentApprovalFlowService` ~:205 / ~:232 | `BillPaymentController::update` :246-272 |
| `bill_income` 1 | `POST /bill-incomes/{id}/approve` (:402) | `BillIncomeApprovalService` :76/:85 | `BillIncomeController::update` :209 |
| `bill_income_request` 1 | `POST /bill-incomes` (:398) | `BillIncomeWriteService` :98 → 3 | `BillIncome::updateStatusAndSendNotifyBillIncomeRequest` :508 |
| `bill_adjust_dept_request` 1, `addition_accounting_request` 1 | `POST /bill-adjust-depts` (:1169) | `BillAdjustDeptSourceService` :717-777 / :860 | `BillAdjustDeptController@store` :249-270 |
| `warranty_repair_request` 1 | `POST /warranty-repair-handle-requests` (CC api:293) | `WarrantyRepairHandleRequestService` :509-513 → 7/8 | `WarrantyRepairHandleRequestsController@store` :170 |
| `warranty_repair_handle_request` 1 | `POST /wr-information-requests` (CC api:324) | `WrServiceQuotationService` :1316-1317 | `WarrantyRepairInformationRequestsController@store` :348 |
| `wr_information_request` 1 | `POST /wr-quotations` (CC api:409) | `WrQuotationService` :324/:337 | `WarrantyRepairServiceQuotationsController@store` :317-341 |
| `wr_service_contract` 1 (type 1) | `POST /wr-service-contracts/{id}/approve` (CC api:369) | `WrServiceContractService` :1563 → 3 | `WarrantyRepairContractsController@approve` :725 |
| MasterData (5 doc_type) | MasterData api:371–448 | service MasterData | Route ERP đã bị `productMovedToHrm` chặn |

**Đã kiểm và chọn ERP** (HRM chưa làm trọn bước):
- `product_export_request` cấp 2/3: HRM không có route.
- `warehouse_export_request`: HRM không lập được `warehouse_exports`.
- `join_export_request`, `split_export_request`: HRM không có code.
- `borrow_sell_request` cấp 1: HRM chưa làm type KM.
- `warehouse_prepick_request` BKS: HRM không có route.
- `wr_service_contract` type 3/4: HRM chỉ duyệt type 1.
- `wr_service_contract_reception`: HRM không tạo được phiếu giao việc.
- `monthly_commission_accounting_request`: không có màn HRM dẫn tới.
- Mọi bảng ERP còn lại: không có endpoint HRM nào ghi trạng thái.

## 7. Rủi ro phải xử lý trước khi khai handler = HRM (dòng có ⚠)

Registry sẽ tính người duyệt theo gate trong danh mục. Nếu màn HRM chốt bằng spatie guard `api` (MW/HLP/WRP), người duyệt thật mang role `App\Employee` thấy phiếu trong hộp nhưng bấm vào bị 403. Các luồng bị ảnh hưởng:

| doc_type · cấp | Cơ chế chặn | Người qua được / người giữ quyền |
|---|---|---|
| `product_export_request` 1, `warehouse_export` 1 | HLP `Kế toán kho` | 3/75 |
| `bill_adjust_dept_request` 1, `addition_accounting_request` 1 | MW `Kế toán thanh toán` | 2/55 |
| `buy_service_accounting_request` 1 | MW `Hạch toán mua dịch vụ` | 2/41 |
| `warranty_repair_request` 1, `warranty_repair_handle_request` 1 | WRP / MW | 0/41 |
| MasterData (PTKD 26/105 · XNK 17/84 · Tính giá 22/63 · Duyệt giá bán 9/26) | MW + HLP | một phần |

**Cách xử lý** (chọn một): sửa gate HRM sang CEP, hoặc gán lại role HRM-type. Trong lúc chưa sửa, tạm khai các dòng này **handler = ERP** (riêng MasterData không lùi được vì ERP đã chặn).

Ngoài ra, các gate HRM còn hẹp/rộng hơn ERP (ghi ở cột Gate). Registry nên dùng phạm vi của danh mục, đồng thời ghi thành việc cần vá ở HRM:
- Không lọc công ty: PIR → ĐNNK, huỷ giữ, xuất mượn, `bill_income`.
- Không lọc phòng: TP nhập hàng, TP mua dịch vụ.
- `store` không kiểm lại quyền: YCXH loại 7, phiếu xử lý SC-BH.


## 8. Kết quả rà lại theo điều kiện màn gốc (22/10)

Chi tiết từng dòng (điều kiện thật kèm file:dòng, số mới, số >30 ngày, mốc tính): [recheck-A.md](recheck-A.md) (§1.1–1.4, 1.14) ·
[recheck-B.md](recheck-B.md) (§1.5–1.9) · [recheck-C.md](recheck-C.md) (§1.10–1.13). **Khi viết khai báo `pending_levels`, lấy điều
kiện ở 3 file này làm chuẩn**, không lấy cột "Trạng thái chờ" ở §1 (đã sửa số, chưa chép hết điều kiện chặt).

**Đổi số (đã sửa ở §1):** C3 4.686→188 · C5 243→428 (sau đó **loại khỏi đợt 1** — xem §3) · `firm_contract` cấp 1 11→14 · `addition_accounting_request` 39→38.

**Đổi điều kiện, số không đổi:** `price_asking_temp_product`, `price_asking_request_group` cấp 2, `price_calculate_request`,
`principle_contract_extend`, `root_order_request` cấp 2, `inland_buy_contract` (type 1–5), `warehouse_export`/`warehouse_import`
(`type<>5`), `product_prepick_request` cấp 3, `prepick_cancel_request`, `position_inventory_result` (`type=1`),
`settlement_contract` (`parent_id IS NULL`).

**Gate sai/thiếu:** HĐNT (quản lý phòng + quyền), HĐ type≠7 (`is_market=0`, hạn mức `max_value_contract`), `liquidation_record`
(người lập ∈ thành viên phòng người duyệt), `request_solution` (implementation_type=2 → phòng của user), `service_export_request`
(công ty theo người lập), `task` cấp 1 (gồm phòng của user), `buy_contract_annex2` (bảng không có company_id),
`delivery_cost_asking_request` (đích danh, rỗng thì quyền `Mua hàng`, không lọc công ty), `bill_adjust_dept_request` (công ty
theo người lập — list ERP và thẻ lệch nhau).

**Nghi rác — chờ nghiệp vụ xác nhận (không sửa dữ liệu):** `inland_buy_contract` 27/29 mã đuôi "ĐỂ XÓA" · `assign_department_ballot`
7 (3 đã có phiếu mới hơn) · `exc_shortage_warehouse_import` 10 · prepick TP #1939, transfer2 TP #208 · C2 27 (YC gốc đã xử lý
xong) · `firm_warranty` 7 · biên bản thanh lý 3 · bàn giao ERP 5 · KH bán hàng NV 2023 · YC giải pháp #14 #27 · điều chỉnh GP #1 ·
báo giá BOM #17 #22 #108 · 48/51 nhóm YCHG cấp 2 có phiếu cha status=1.

**Nhóm "chờ giao việc"** (C5, PL bổ sung, HĐ bảo hành, lắp đặt, YC khác): **loại khỏi hộp duyệt** (user chốt 22/10 — tính chất khác), xem §3.

**Tồn đọng thật (không phải rác):** `root_order_request` cấp 2 209 (129 >30 ngày) · `settlement_contract` 204 (2 >30 ngày) ·
`wr_import_result` 290 (151 >30 ngày) · C1 137 (110 >30 ngày).
