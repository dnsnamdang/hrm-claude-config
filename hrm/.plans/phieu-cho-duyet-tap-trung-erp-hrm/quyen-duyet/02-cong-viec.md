# Quyền duyệt — nhóm CÔNG VIỆC (Modules/Assign, pages/assign) — @cuong61n

Điều tra CHỈ ĐỌC code đang chạy, nhánh `hrm-api` = `gop_db-main` (16/11/2026). Mọi khẳng định có `file:dòng`.
Ký hiệu đường dẫn: **A:** = `hrm-api/Modules/Assign/` · **H:** = `hrm-api/` · **C:** = `hrm-client/`.
Chỗ không xác minh được ghi **"chưa xác minh"**.

> Tài liệu nền (`inventory-hrm.md` AS1–AS23, `danh-gia-tung-phieu.md` mục 2) ghi quyền theo TÊN CŨ và số dòng đã trôi. Code hiện kiểm theo MÃ quyền (Catalog `H:app/Support/Permissions/Catalog/{assign,presale,sale}.php`). Bảng đối chiếu tên cũ → mã nằm ở từng mục.

---

## 0. Nền chung — "có quyền" và "là quản lý" nghĩa là gì trong code

| Khái niệm | Hàm / nơi | Nghĩa chính xác |
|---|---|---|
| Có quyền | `isCurrentEmployeeHasPermission($mã)` `H:app/Helper/PermissionHelper.php:20` → `CurrentPermission::has` `H:app/Support/Permissions/CurrentPermission.php` | Vai trò của người đăng nhập, **tại công ty đang làm việc** (`current_company_role`), có mã. Không đăng nhập / không có công ty ⇒ false (fail-closed). Mọi mã duyệt nhóm này trong Catalog đều `'scopes' => []` (không có phạm vi 1–4) — `Catalog/presale.php:164,260,213`, `Catalog/assign.php:156,600,840,233`, `Catalog/sale.php:275`. |
| Middleware route | `checkPermission:<mã>[\|<mã>]` `H:app/Http/Middleware/CheckPermission.php:26-34` | Có 1 mã là qua. Chỉ kiểm quyền, không kiểm phạm vi. |
| QUẢN LÝ phòng (chặt) | `manageDepartmentIdsOf($empId,$companyId)` `H:app/Helper/PermissionHelper.php:100-114`; `listManageDepartmentIds()` `:209`; `TpEmployee::manager_departments` `H:app/Models/TpEmployee.php:116-120` | Bảng `employee_manage_departments` (dòng có `department_id`) HOẶC cờ "quản lý tất cả phòng ban" (`company_employees.all_department` chỉ cho công ty của chính NV, hoặc `employee_manage_departments.all_department` theo từng công ty — `:66-88`). Tính theo công ty đang làm việc. |
| QUẢN LÝ ∪ phòng của mình | `listManageDepartmentIdsWithOwn()` `H:app/Helper/PermissionHelper.php:220-230` | Như trên + `employee_infos.department_id` của chính người đó. **Không cần là quản lý** — thuộc phòng đó là đủ. |
| Công ty | 2 kiểu lệch nhau: `auth()->user()->current_company_role` (công ty đang làm việc) và `auth()->user()->info->company_id` (công ty hồ sơ nhân viên) | Mỗi luồng dùng 1 kiểu (xem từng mục). Người làm việc ở công ty khác công ty hồ sơ có thể bị lệch. |
| `department_id` trên phiếu | `BaseModel` creating-hook `H:app/Models/BaseModel.php:122-125,147-150` | Nếu không gán tường minh = **phòng của NGƯỜI TẠO tại lúc tạo** (`employee_infos.department_id`). Báo giá, phiếu công tác, giao việc, đề xuất công việc, hợp đồng… đều dùng cột này, KHÔNG phải phòng thực hiện. |
| Bypass Super Admin | Không có trong `CurrentPermission`/`CheckPermission` (đã đọc) | Đúng quy ước CLAUDE.md (không bypass). Chưa kiểm vai trò Super Admin trên DB. |

Hai middleware "hạn mức quá hạn" khác nhau (mục f):

* `dueConfig:<tên>[,manager]` — `H:Modules/Finance/Http/Middleware/CheckDueConfig.php:38-55` → `DueConfigBlockService::managerBlockedReason` `H:Modules/Finance/Services/DueConfigBlockService.php:171-211`: chạy trong DB HRM, trả **423** + `show_overdue_modal`. Mode `manager` chỉ xét `employee_manage_departments` có `department_id` (**không** tính cờ all_department — lệch với `manageDepartmentIdsOf`).
* `checkDueConfigsManager:<tên>` — `H:app/Http/Middleware/CheckDueConfigsManager.php:21-52`: gọi API ERP `/api/v1/due-configs/check-manager-block`, trả **403**; **fail-open** khi tắt `use_erp` (`:25`) hoặc ERP lỗi/không kết nối (`:51-56`).

---

## 1. Đề xuất gia hạn dự án TKT (AS3, #11153)

**Cấp** (`A:Entities/ProspectiveProjectExtensionRequest.php:51-57,70-73`):

| status | BE trả (`status_name`) | Cấp |
|---|---|---|
| 1 | Chờ TP duyệt | Cấp TP |
| 2 | Chờ BGĐ duyệt | Cấp BGĐ (chỉ khi số ngày xin > ngưỡng) |
| 3 / 4 | Đã duyệt / Từ chối | Cuối |

**Điều kiện chuyển cấp**: lúc tạo, `days > project_extension_tp_max_days` ⇒ `approval_level = LEVEL_BGD(2)` else `LEVEL_TP(1)` — `A:Services/ProspectiveProjectExtensionService.php:51-55`. Ngưỡng theo công ty của dự án, mặc định **30 ngày** `A:Services/ProjectCloseConfigService.php:26`. TP duyệt xong ở `LEVEL_BGD` ⇒ `status=2` (`:130-144`), còn `LEVEL_TP` ⇒ duyệt luôn + cộng `extended_days` (`applyApproval :203-242`).

| Cấp | Ai duyệt | Mã quyền | Điều kiện "quản lý/phạm vi" | Kiểm ở đâu |
|---|---|---|---|---|
| TP | NV có quyền + **quản lý** phòng của đề xuất | `presale.gia_han_du_an_tkt_truong_phong.approve` (tên cũ "Trưởng phòng duyệt gia hạn dự án TKT") `A:Entities/...Request.php:60,64` | `ensureTpCanApprove`: `department_id` của đề xuất ∈ `QuotationService::managedDepartmentIdsOf` (= `manageDepartmentIdsOf`, **chặt, không "own"**) `A:Services/ProspectiveProjectExtensionService.php:313-318,333-338`. `department_id` đề xuất = `main_sale_department_id` của dự án (`:68`), không phải phòng người bấm. | Route `checkPermission` `A:Routes/api.php:538-539`; service `ensurePermission`+`ensureTpCanApprove` `:119-125` |
| BGĐ | NV có quyền + cùng công ty | `presale.gia_han_du_an_tkt_ban_giam_doc.approve` ("Ban giám đốc duyệt gia hạn dự án TKT") | `ensureBgdCanApprove`: `request.company_id == info.company_id` `:321-327,340-345` (**kiểu `info.company_id`**) | Route `:540-541`; service `:156-162` |
| Từ chối | Cấp nào đang chờ thì người cấp đó | cả 2 mã (route) | như duyệt cấp tương ứng, lý do bắt buộc | route `:542-543`; service `:167-178` |

* **c) Hàng chờ**: `GET /assign/prospective-project-extensions/pending-approval` `A:Routes/api.php:536-537`, `pendingQuery` `A:Services/...Service.php:252-300`: TP ⇒ status 1 + `department_id ∈ managed`; BGĐ ⇒ status 2 + `company_id`. **Khớp** tiêu chí duyệt. Cờ nút ở Resource `A:Transformers/ProjectExtension/ProspectiveProjectExtensionResource.php:52-57` (quyền + phạm vi, cùng chốt BE) → FE `C:pages/assign/prospective-projects/extension-requests/index.vue:373-375,391-393`. Không fail-open.
* **d) Người tạo tự duyệt?** Người tạo bắt buộc là `main_sale_employee_id` của dự án (`:45-47`). **Không có chặn** người tạo = người duyệt: nếu NV KD phụ trách dự án đồng thời quản lý phòng và có quyền TP thì tự duyệt (không có `created_by != me` trong `tpApprove`/`bgdApprove`).
* **e) Một người nhiều cấp**: người giữ cả 2 mã TP+BGĐ (và quản lý phòng + cùng công ty) phải bấm **2 lần riêng** (`tp-approve` rồi `bgd-approve`) — KHÔNG tự nhảy cấp; **không có chặn** "người đã duyệt TP không được duyệt BGĐ" (`bgdApprove :154-165` không đọc `tp_approved_by`). Hàng chờ của người này hiện cả 2 nhóm (`pendingQuery :263-282`).
* **f)** Điều kiện đặc thù: dự án phải không ở trạng thái 9/10/11, chưa quá hạn đóng, chưa có đề xuất đang chờ (`:96-113`); không dùng dueConfig.
* Thông báo: gửi cho **mọi** người có quyền cùng công ty người thao tác (`EmployeeInfoService::listEmployeeInfoByPermission` `H:Modules/Timesheet/Services/EmployeeInfoService.php:561-568`), KHÔNG lọc theo phòng → TP phòng khác nhận thông báo nhưng bị 403 khi duyệt.

---

## 2. Báo giá (AS1) — Cấp 1 tự duyệt · TP · TP→BGĐ

**Cấp** (`A:Entities/Quotation.php:11-26`): status 1 Đang tạo · 2 **Chờ TP duyệt** · 3 **Chờ BGĐ duyệt** · 4 Đã duyệt · … Cấp duyệt `price_approval_level` 1/2/3.

**Điều kiện chuyển cấp**: lúc Gửi duyệt, `calculateLevel` `A:Services/QuotationService.php:3597-3615` = `max(cấp theo giá trị đơn, cấp theo tỷ suất lợi nhuận, cấp theo tỷ suất hàng tạm)` (`A:Services/BomPriceApprovalConfigService.php:70-98`, bảng `bom_price_approval_configs`; không khớp ngưỡng ⇒ cấp 3). Báo giá "sạch" (`isAutoApprovable` `:3622+`: toàn hàng ERP, đơn giá > 1.000, không giảm giá) bị **đè về cấp 1**. Submit `:4036-4070`: cấp 1 ⇒ ở lại status 1 (`can_self_approve`), cấp 2/3 ⇒ status 2.

| Cấp | Ai duyệt | Mã quyền | Quản lý / phạm vi | Kiểm ở đâu |
|---|---|---|---|---|
| Cấp 1 | **Chính người lập** | không cần mã | `ensureEditableByCreator`: status=1 và `created_by == auth()->id()` `A:Services/QuotationService.php:4872-4880`; `price_approval_level==1` `:4078` | `selfApprove` `:4076`; route `A:Routes/api.php:697` không gắn checkPermission |
| TP (cấp 2; hoặc bước 1 của cấp 3) | NV có quyền + quản lý phòng báo giá | `presale.gia_bom_giai_phap_truong_phong.approve` (tên cũ "Trưởng phòng duyệt giá Bom giải pháp") | `ensureTpCanApprove`: `quotations.department_id` (= phòng NGƯỜI LẬP lúc tạo) ∈ `manageDepartmentIdsOf` `A:Services/QuotationService.php:5106-5112,5083-5104` (chặt) | Route `A:Routes/api.php:698-699`; service `:4115-4119` |
| BGĐ (bước 2 của cấp 3) | NV có quyền + cùng công ty | `presale.gia_bom_giai_phap_ban_giam_doc.approve` ("Ban giám đốc duyệt giá Bom giải pháp") | `ensureBgdCanApprove`: `quotation.company_id == info.company_id` `:5114-5120` | Route `:700-701`; service `:4168-4173` |
| Từ chối | TP khi status 2, BGĐ khi status 3 | 1 trong 2 mã (route `:702-703`) + kiểm lại theo trạng thái `:4228-4242` | như duyệt | Từ chối ⇒ về **Đang tạo**, xoá `tp_approved_by`, `price_approval_level` `:4244-4256` |

* **c)** Hàng chờ `applyPendingApprovalScope` `A:Services/QuotationService.php:4522-4572` (dùng chung danh sách + màn chi tiết `findViewableQuotation`): TP ⇒ status 2 ∧ `department_id ∈ managed`; BGĐ ⇒ status 3 ∧ `company_id = info.company_id`; loại `is_summary`. **Khớp** tiêu chí duyệt. FE chi tiết chỉ ẩn/hiện nút theo quyền + status (`C:pages/assign/quotations/_id/index.vue:1282-1288,824-831,1496-1497`), không kiểm phòng — BE chặn.
* **d) Người tạo tự duyệt?** Cấp 1: được (chủ ý). Cấp 2/3: **không chặn** — `tpApprove` không so `created_by` với người duyệt; TP lập báo giá của phòng mình, báo giá thuộc cấp 2 ⇒ tự duyệt được (vì `department_id` = phòng của chính họ).
* **e) Một người nhiều cấp**: TP kiêm BGĐ với báo giá cấp 3: `tpApprove` đưa sang status 3 rồi dừng (`:4126-4137`) — phải bấm `bgd-approve` lần 2; **không tự nhảy cấp, không chặn** cùng người duyệt 2 cấp (`tp_approved_by` chỉ ghi, không kiểm ở `bgdApprove`). Hàng chờ của người này hiện cả 2 nhóm.
* **f)** `dueConfig:Lập báo giá` chỉ ở bước LẬP/SỬA (`A:Routes/api.php:650,683,688,689`), KHÔNG chặn bước duyệt. Duyệt xong đồng bộ ERP `syncToErpAfterApproval` `:4150-4160`.
* Thông báo đúng người: TP = người thuộc/quản lý phòng báo giá có quyền (`tpApproverInfoIds :5168`), BGĐ = người có quyền ở công ty báo giá (`bgdApproverInfoIds :5185`) — khớp tiêu chí duyệt.

### 2b. Báo giá tổng hợp (AS2) — 1 cấp, status 2 "Chờ duyệt"

TP duyệt giá, mã `presale.gia_bom_giai_phap_truong_phong.approve` (route `A:Routes/api.php:627-630`) + `ensureCanApprove` quản lý phòng `A:Services/SummaryQuotationService.php:1064-1090` (cùng helper chặt). Không có BGĐ. Không chặn người lập tự duyệt. Hàng chờ riêng: **không có** (bị loại khỏi pending-approval bằng `is_summary=false` `A:Services/QuotationService.php:4533`) — duyệt trên màn chi tiết. Thông báo: `employeeIdsManagingDepartment` (không lọc quyền ở đoạn đã đọc `:1092+`; chưa xác minh phần còn lại).

---

## 3. Yêu cầu làm giải pháp (AS7) — Tiếp nhận / Từ chối

**Cấp**: 1 cấp. status 2 "Chờ tiếp nhận" → 3 "Đã tiếp nhận" / 4 "Từ chối" (`A:Entities/RequestSolution.php:21-26`, tên `:45-95`).

| Bước | Ai | Mã | Quản lý / phạm vi | Kiểm ở đâu |
|---|---|---|---|---|
| Tiếp nhận / Từ chối | NV có quyền, phòng = `receive_dept` | `presale.yeu_cau_lam_giai_phap.confirm` ("Tiếp nhận yêu cầu làm giải pháp") | **CHỈ FE/cờ**: `isCanReceive` = quyền ∧ status 2 ∧ `receive_dept ∈ listManageDepartmentIdsWithOwn` `A:Entities/RequestSolution.php:288-317` | BE route chỉ `checkPermission` `A:Routes/api.php:450-453`; controller `receive` chỉ khoá dòng + kiểm status `A:Http/Controllers/Api/V1/RequestSolutionController.php:118-141`. **Không kiểm `receive_dept`** ⇒ người có quyền ở phòng A gọi API tiếp nhận được YC phòng B. |

* **c) Hàng chờ** `RequestSolutionService::pending` `A:Services/RequestSolutionService.php:163-216` — nhánh YC `implementation_type` = Liên phòng ban / NULL ⇒ `receive_dept ∈ managed ∪ own`; nhánh `BY_DEPT` (type 2) ⇒ `receive_dept == phòng của chính mình` (chỉ own, KHÔNG managed). Lệch với `isCanReceive` (managed ∪ own cho mọi type) ⇒ quản lý phòng B (không thuộc phòng B) thấy nút Tiếp nhận ở màn danh sách chung nhưng không thấy dòng trong màn Chờ tiếp nhận nếu YC thuộc kiểu Triển khai theo phòng. Không quyền ⇒ query rỗng `:182-184`.
* **d)** Người tạo yêu cầu cũng được tiếp nhận nếu có quyền + phòng khớp (không có chặn `created_by`). Hủy yêu cầu thì chỉ người tạo (`isCanCancel :270-285`).
* **e)** 1 cấp ⇒ không phát sinh.
* **f)** Tiếp nhận bắt buộc chọn PM + ngày dự kiến (Request `RequestSolutionReceiveRequest`, chưa mở); từ chối ⇒ kéo dự án về "Thu thập thông tin" (`:rejects revertProjectToInfoCollecting` `A:Services/RequestSolutionService.php:484-540`).

---

## 4. Đề xuất công tác (AS16, `assign_requests.type=1`) và Giao công tác / Phiếu công tác (AS16, `type=2`)

Cùng bảng `assign_requests`, entity `A:Entities/AssignRequest.php` (status 1 Đang tạo · 2 Chờ duyệt · 3 Đã duyệt · 4 Đã lập phiếu công tác · 5 Đã nhập kết quả · 6 Không duyệt · 7 Đã duyệt kết quả… `:31-45`). Chữ trạng thái do FE map (chưa xác minh nguồn BE).

### 4a. Đề xuất công tác (type=1) — "Duyệt" = Lập phiếu công tác

| Bước | Mã | Quản lý/phạm vi | Kiểm ở đâu |
|---|---|---|---|
| "Duyệt" / Lập phiếu công tác từ đề xuất (status 2→4 khi phiếu công tác có `parent_id` được tạo `A:Services/AssignBusinessService.php:468-470`) | `assign.phieu_de_xuat_di_cong_tac.manage` ("Quản lý phiếu đi công tác") | **Không** kiểm phòng ở BE. FE nút Duyệt: `item.status==2 && canCreateAssignBusiness` (= có mã) `C:pages/assign/assign_requests/index.vue:137,147`, cờ từ `A:Http/Controllers/Api/V1/AssignRequestController.php:54` | `AssignRequestController::update`/`store` KHÔNG có kiểm quyền; `status_request` do client gửi và được ghi nguyên `A:Services/AssignRequestService.php:136,179`. |
| "Không duyệt" | cờ FE `isApprove=true` **hard-code** `C:pages/assign/assign_requests/_id/index.vue:6` (nút luôn hiện ở status 2) → gọi `assign_business/{id}/deny` | **Mã `assign.phieu_giao_cong_tac.approve` + quản lý phòng** (`canApproveAssignBusiness`, xem 4b) — KHÁC mã `.manage` dùng để hiện nút Duyệt `A:Http/Controllers/Api/V1/AssignBusinessController.php:908-913` | Lệch: người có `.manage` mà không có `.approve` thấy "Không duyệt" nhưng 403. |

* **c) Hàng chờ** `type=waiting` `A:Services/AssignRequestService.php:69-79`: người có `.manage` thấy **mọi** phiếu status 2 trong phạm vi xem `assign.danh_sach_phieu_de_xuat_di_cong_tac.view` (không lọc theo phòng quản lý); không có `.manage` thì chỉ thấy phiếu mình tạo / mình đi.
* **d)** Người đề xuất có `.manage` ⇒ tự lập phiếu công tác từ đề xuất của chính mình (không chặn).
* Thông báo: `listEmployeeInfoHasPermission('...manage', người gửi, phòng phiếu)` ⇒ người **quản lý phòng của phiếu hoặc quản lý-tất-cả** có `.manage` (`H:Modules/Timesheet/Services/EmployeeInfoService.php:544-558`) `A:Http/Controllers/Api/V1/AssignRequestController.php:175,276`.

### 4b. Giao công tác / Phiếu công tác (type=2, AS16) — Duyệt và Duyệt kết quả

| Cấp | Mã | Điều kiện quản lý | Kiểm ở đâu |
|---|---|---|---|
| **Duyệt phiếu** (status 2 → 3; cho cả status 1) | `assign.phieu_giao_cong_tac.approve` ("Trưởng phòng duyệt phiếu giao công tác") | `canApproveAssignBusiness` `A:Entities/AssignRequest.php:792-801`: status ∈ {Đang tạo, Chờ duyệt} ∧ quyền ∧ `department_id` (phòng người lập) ∈ `manager_departments` (**chặt**, không own) | BE update `A:Http/Controllers/Api/V1/AssignBusinessController.php:476-480` (`status_request==3` cần `canApprove… \|\| canAddEmployee`), deny `:908-913`; route chỉ `checkDueConfigsManager:Duyệt kết quả công tác trên HRM` (gắn cho MỌI `POST /{id}`) `A:Routes/api.php:1355` |
| **Lưu và duyệt ngay** (người tạo duyệt 1 lượt, bỏ qua cấp 2) | `assign.phieu_giao_cong_tac.create` ("Trưởng phòng giao đi công tác") | FE nút `canHasPermissionAssignBusiness` `C:components/assign-components/assign-business/AssignBusinessForm.vue:2226-2237,2585` | **BE `store` KHÔNG kiểm gì khi `status_request==3`** `A:Http/Controllers/Api/V1/AssignBusinessController.php:368-372` (chỉ validate trùng lịch `:320-331`). Fail-open: bất kỳ người đăng nhập POST `status_request=3` là phiếu ở trạng thái Đã duyệt + đồng bộ ERP. |
| **Nhập kết quả** (status 3 → 5) | `assign.ket_qua_cong_tac.create` ("Nhập kết quả công tác") HOẶC trưởng nhóm phiếu | `canImportResultAssignBusiness` `A:Entities/AssignRequest.php:809-831`: `business_type==1 ∧ jobassign_type==2`, status 3, và (trưởng nhóm ∨ quyền ∧ `department_id ∈ manager_departments`) | update action `import_result` `A:Http/Controllers/Api/V1/AssignBusinessController.php:462-467` |
| **Duyệt kết quả** (status 5 → 7), **không có Từ chối** | `assign.ket_qua_cong_tac.approve` ("Trưởng phòng duyệt kết quả công tác") | `canApproveResultAssignBusiness` `A:Entities/AssignRequest.php:838-847`: status 5 ∧ quyền ∧ `department_id ∈ manager_departments` | update action `approve_result` `A:Http/Controllers/Api/V1/AssignBusinessController.php:468-473`. `deny` (`:908`) dùng `canApproveAssignBusiness` (chỉ status 1/2) ⇒ không có đường từ chối kết quả. |
| Gia hạn thêm NV sau duyệt | người tạo | `canAddEmployee` = creator ∧ status 3 ∧ chưa hết hạn… `A:Entities/AssignRequest.php:261-265` | update `status_request==3` cũng cho `canAddEmployee` qua (`:477`) — người tạo "duyệt lại" được phần thêm |

* **c) Hàng chờ**: `type=waiting` (`A:Services/AssignBusinessService.php:202-214`, bản dùng cho export `:1376-1388`): có quyền `.approve` ⇒ status 2 ∧ (`department_id ∈ manager_departments` **∨ do mình tạo ∨ mình là người đi**) — rộng hơn tiêu chí duyệt (người tạo/người đi thấy dòng nhưng không duyệt được nếu không quản lý). **Không có quyền `.approve`** ⇒ không lọc status: thấy mọi phiếu mình tạo/mình đi (`:211-214`). Hàng chờ kết quả: màn riêng gọi `assign/assign_business?status=5` (`C:pages/assign/assign_waiting_approve_result/index.vue`, chưa mở), phạm vi chỉ là phạm vi XEM `assign.danh_sach_phieu_giao_cong_tac.view` (`A:Services/AssignBusinessService.php:77-114`) — không lọc "phòng mình quản lý + quyền duyệt kết quả" ⇒ người xem thấy cả phiếu mình không duyệt được.
* **d) Người tạo tự duyệt?** Không chặn: `canApproveAssignBusiness` không so `created_by`; TP lập phiếu cho phòng mình rồi tự "Duyệt" hoặc "Lưu và duyệt" (cần `.create`).
* **e) Một người nhiều cấp**: 3 quyền độc lập `.create` / `.approve` / `.ket_qua.create` / `.ket_qua.approve`. Cùng người giữ cả chuỗi (lập + duyệt phiếu + nhập KQ + duyệt KQ) làm được hết, mỗi bước 1 lần gọi, **không chặn**.
* **f)** Trùng lịch: `validateAssignBusiness` (PCT đã duyệt status 3 chồng khoảng from–to của cùng NV; PCT kỹ thuật chỉ bị chặn bởi PCT khác `business_type=2`, có xét gia hạn đang chờ) + `validateAssignBusinessVsTimesheet` (loại 2) — chạy khi **tạo** `status_request 2/3` `A:Http/Controllers/Api/V1/AssignBusinessController.php:320-331` và khi **sửa/duyệt** `:692-704`; trả 424 `conflict_assign_business`. Cơm: `checkDuplicateTimeWithRiceRegistration` trả 423 hỏi xác nhận (`:305-317,438-451`). `checkDueConfigsManager:Tạo phiếu công tác (phân hệ giao việc)` ở `POST /` `A:Routes/api.php:1354`; `...:Duyệt kết quả công tác trên HRM` ở `POST /{id}` `:1355` (ERP API, fail-open).
* Bug nhỏ: `deny` gọi `canApproveAssignBusiness()` trước khi kiểm `null` `A:Http/Controllers/Api/V1/AssignBusinessController.php:910-916` (lỗi 500 khi id không tồn tại).

---

## 5. Đề xuất công việc (AS17, `job_requests`) — Duyệt → Giao việc

**Cấp** (`A:Entities/JobRequest.php:17-22`): 1 Đang tạo · 2 **Chờ duyệt** · 3 **Chờ giao việc** · 4 Từ chối · 5 Đã giao công tác · 6 Đã giao việc.

| Cấp | Mã | Quản lý | Kiểm ở đâu |
|---|---|---|---|
| Duyệt (2→3) | `assign.phieu_de_xuat_cong_viec.approve` ("Trưởng phòng duyệt phiếu đề xuất công việc") | `canApprove` `A:Entities/JobRequest.php:89-94`: status 2 ∧ quyền ∧ `department_request_id` (phòng ĐỀ XUẤT, **tường minh**, không phải phòng người tạo) ∈ `manager_departments` (chặt) | `update` với `status_request==3` `A:Http/Controllers/Api/V1/JobRequestController.php:191-195`; `deny` `:306-309` |
| Giao việc/giao đi công tác (3→5/6) | `assign.phieu_giao_cong_tac.create` ("Trưởng phòng giao đi công tác") | `canAssign` `:101-107`: status 3 ∧ quyền ∧ `department_implement_id` ∈ `manager_departments` | thực hiện bằng cách lập phiếu công tác từ phiếu này (FE `this.form.canAssign`, `C:components/assign-components/assign-business/AssignBusinessForm.vue:2215-2223`); BE `store` không kiểm (xem 4b) |

* **c)** Hàng chờ `type=waiting` `A:Services/JobRequestService.php:77-86`: có quyền `.approve` ⇒ **mọi** phiếu status 2 trong phạm vi xem `assign.danh_sach_phieu_de_xuat_cong_viec_can_lam.view` — KHÔNG lọc theo `department_request_id ∈ managed` ⇒ lệch với tiêu chí duyệt (thấy phiếu phòng khác, bấm duyệt bị 403). Thông báo "Chờ duyệt" lọc đúng: `listEmployeeInfoHasPermission(.approve, …, department_request_id)` `A:Http/Controllers/Api/V1/JobRequestController.php:377-381`.
* **d)** FE cho "Lưu và duyệt" 1 lượt khi `currentUserInfo.department_id == form.department_request_id` ∧ có `.approve` `C:components/assign-components/job-requests/JobRequestForm.vue:265-278` — dùng **phòng của mình**, không đòi là quản lý. **BE `store` không chặn `status_request==3`** `A:Http/Controllers/Api/V1/JobRequestController.php:99-165` (không gọi `canApprove`; chỉ `update` mới kiểm `:191-195`). Fail-open khi tạo.
* **e)** Cùng người có `.approve` (phòng đề xuất) và `.create` (phòng thực hiện) làm được cả duyệt lẫn giao, không chặn.
* Thông báo "Chờ xử lý" cho người giao: `listEmployeeInfoHasPermission('assign.phieu_giao_cong_tac.create', …, department_implement_id)` `:413-417`.

---

## 6. Giao việc (AS18, `assign_jobs`) và Duyệt kết quả giao việc

**Cấp** (`A:Entities/AssignJob.php:17-22`): 1 Đang tạo · 2 Chờ duyệt · 3 Đã duyệt · 4 Từ chối · 5 Đã nhập kết quả · 6 Đã duyệt kết quả.

| Cấp | Mã | Điều kiện quản lý (ý đồ) | Kiểm ở BE? |
|---|---|---|---|
| Duyệt phiếu giao việc (2→3) | `assign.phieu_giao_cong_viec.approve` ("Trưởng phòng duyệt phiếu giao công việc") | `canApprove` `A:Entities/AssignJob.php:89-95`: quyền ∧ `department_id` (phòng NGƯỜI TẠO — comment ghi "phòng thực hiện" nhưng cột là `department_id`) ∈ `manager_departments` | **KHÔNG.** `AssignJobController::update` (`A:Http/Controllers/Api/V1/AssignJobController.php:214+`), `approveResult` (`:424`), `deny` (`:531`) không gọi `canApprove()`/`canApproveResult()`. Chỉ `Resource` trả cờ cho FE (`A:Transformers/AssignJobResource/AssignJobListResource.php:35`, `show :83-85`). |
| Duyệt kết quả (5→6) | `assign.ket_qua_cong_viec.approve` ("Trưởng phòng duyệt kết quả công việc") | `canApproveResult` `:97-103` cùng kiểu | **KHÔNG** (route chỉ `checkDueConfigsManager:Duyệt kết quả công tác trên HRM` `A:Routes/api.php:1518`, ERP, fail-open) |
| Nhập kết quả | `assign.ket_qua_cong_viec.create` | `A:Http/Controllers/Api/V1/AssignJobController.php:48,85` | cờ FE; `importResult :335` chưa mở |

* **c)** `type=waiting` `A:Services/AssignJobService.php:92-100`: có quyền `.approve` ⇒ **mọi** phiếu status 2 trong phạm vi xem `assign.danh_sach_phieu_giao_viec.view` (không lọc theo phòng). Hàng chờ kết quả: `C:pages/assign/assign_job_waiting_approve_result/index.vue:438` (`status:'5'`) cùng phạm vi xem.
* **FE** gate nút Duyệt = quyền + status, không kiểm phòng (`C:components/assign-components/assign-jobs/AssignJobForm.vue:514,522,817`; duyệt KQ `AssignJobApproveResult.vue:424`). "Lưu và duyệt" 1 lượt: `currentUserInfo.department_id == form.department_request_id` ∧ quyền `AssignJobForm.vue:490-498`.
* **d/e)** Hoàn toàn không chặn: BE không biết ai được duyệt; mọi nhân viên đăng nhập gọi được `POST assign_jobs/{id}` (đổi status), `approveResult`, `deny` (cả `deny` không kiểm gì, `A:Http/Controllers/Api/V1/AssignJobController.php:531-560`). **Rủi ro bảo mật lớn nhất của nhóm** (khớp tài liệu nền AS18, nhưng rộng hơn: deny cũng hở).
* **f)** Công khoán: `contract_work_approve` bắt buộc khi `is_contract_work` (validate trong `approveResult :429-462`).

---

## 7. Bàn giao công việc (AS5) — TP duyệt, rồi người nhận tiếp nhận (AS6)

| Cấp | Mã / điều kiện | Quản lý | Kiểm ở đâu |
|---|---|---|---|
| Duyệt / Từ chối phiếu (status 2 "Chờ duyệt" → 3 "Đã duyệt" / 4 "Từ chối") `A:Entities/Handover.php:40-44` | `assign.ban_giao_cong_viec.approve` ("Duyệt bàn giao công việc") | **BE không kiểm phòng.** `HandoverService::approve/reject` chỉ kiểm status `A:Services/HandoverService.php:852-856,928-932`; route `checkPermission` `A:Routes/api.php:1576-1579` | FE nút: status 2 ∧ quyền (`C:pages/assign/handover/_id/index.vue:118-122`) |
| Người nhận tiếp nhận từng mục | không cần mã | `item.receiver_id == auth()->user()->id` `A:Services/HandoverService.php:955-958` | service |

* **c) Hàng chờ** `HandoverService::pending` `A:Services/HandoverService.php:137-156`: cần quyền ∧ status 2 ∧ `handover.department_id ∈ managed ∪ own` (`department_id` = phòng của NV BÀN GIAO, `:715-716`). Tiêu chí XEM rộng hơn tiêu chí DUYỆT (BE duyệt không kiểm phòng) — người xem được dòng thì duyệt được; người không thấy dòng vẫn gọi API duyệt được nếu biết id.
* **d)** Không chặn: `created_by` / người bàn giao có quyền + cùng phòng ⇒ tự duyệt phiếu của mình (không có so sánh trong `approve`).
* **e)** TP duyệt có thể sửa người nhận/ghi chú/tiến độ/hạn trước khi duyệt (`:861-897`). Từ chối bắt lý do ≥ 10 ký tự (HandoverRejectRequest, chưa mở).
* Thông báo đúng: thành viên + quản lý phòng của phiếu có quyền `A:Services/HandoverService.php:1370-1391`.

---

## 8. Gia hạn / kết thúc sớm công tác (AS22)

| Cấp | Mã | Phạm vi | Kiểm ở đâu |
|---|---|---|---|
| 1 cấp: status 2 Chờ duyệt → 3 Đã duyệt / 4 Từ chối `A:Entities/ExtendEndSoonRequest.php:43-46` | `assign.phieu_giao_cong_tac.approve` (dùng lại mã duyệt phiếu công tác) `:112-114` | **KHÔNG kiểm phòng/công ty** — chỉ `status==2 ∧ quyền` | `approve`/`reject` `A:Http/Controllers/Api/V1/ExtendEndSoonRequestController.php:224-228,256-260`; route approve có `checkDueConfigsManager:Chặn gia hạn và kết thúc phiếu công tác (phân hệ giao việc)` `A:Routes/ExtendEndSoonRequest/api.php:26` |

* **c)** Danh sách: chỉ phạm vi XEM `assign.danh_sach_gia_han_ket_thuc_som.view` + `phiếu mình tạo / mình đi` (`A:Repositories/Criteria/ExtendEndSoonRequestCriteria.php:40-66`), **không có hàng chờ riêng, không lọc theo người duyệt**. Cờ nút `canApprove` ở Transformer `:43`.
* **d)** Người tạo có `.approve` ⇒ tự duyệt (không chặn). **e)** 1 cấp.
* Thông báo gửi `listEmployeeInfoHasPermission(.approve, người tạo)` ⇒ chỉ quản lý phòng người tạo; nhưng duyệt được cho bất kỳ ai có mã ⇒ lệch. Duyệt xong ghi đè `assign_business.to_time` (`:232-235`).

---

## 9. Đề nghị thanh toán công tác phí (AS20) — TP → KT

**Cấp** (`A:Entities/PaymentBusinessRequest/PaymentBusinessRequest.php`, status `CHO_TP_DUYET`=2, `CHO_KT_DUYET`=3, `DA_DUYET`, `KHONG_DUYET`; chữ FE).

| Cấp | Mã | Phạm vi | Kiểm ở đâu |
|---|---|---|---|
| TP (2→3) | `assign.de_nghi_thanh_toan_truong_phong.approve` ("TP Duyệt đề nghị thanh toán") | `canTpApprove` `:190-194`: status ∧ quyền; **không kiểm phòng/công ty** | `approve` `A:Http/Controllers/Api/V1/PaymentBusinessRequestController.php:330-334`; `disApprove :379-383`; route approve có `checkDueConfigsManager:Duyệt đề nghị thanh toán HRM` `A:Routes/PaymentBusinessRequest/api.php:25` |
| KT (3→duyệt) | `assign.de_nghi_thanh_toan_ke_toan.approve` ("KT Duyệt đề nghị thanh toán") | `canKtApprove` `:196-199` cùng kiểu | `ktApprove :405-409`; `ktDisApprove :454-458` |

* TP được sửa số ngày/đêm và chi phí lúc duyệt (`:337-345`), lưu `approver_id`/`approved_time` (`:352-353`); KT lưu `kt_approver_id` (`:427-428`).
* **c)** Danh sách: phạm vi XEM `assign.danh_sach_de_nghi_thanh_toan.view` + phiếu mình lập/đi (`A:Repositories/Criteria/PaymentBusinessRequestCriteria.php:46-72`), ẩn "Đang tạo" của người khác `:73-80`. **Không có hàng chờ lọc theo cấp/quyền duyệt**. Cờ `canTpApprove/canKtApprove` cho nút ở Transformer `A:Transformers/PaymentBusinessRequest/PaymentBusinessRequestTransformer.php:99-100`.
* **d)** Người lập có mã TP hoặc KT ⇒ tự duyệt (không so `created_by`). Lập phiếu cần `assign_business->canCreatePaymentBusinessRequest()` (`:96-101`).
* **e) Một người nhiều cấp**: người giữ cả mã TP và KT duyệt cả 2 cấp liền (2 lần gọi), **không chặn** `approver_id == kt_approver_id`.
* Phạm vi phòng: không có ⇒ TP phòng khác duyệt được nếu biết id.

---

## 10. Quyết toán công khoán theo hợp đồng (AS21) — TP → KT

| Cấp | Mã | Phạm vi | Kiểm ở đâu |
|---|---|---|---|
| TP (status 2 → 3) `A:Entities/SettlementContract/SettlementContract.php:59-63` | `assign.quyet_toan_hop_dong_truong_phong.approve` ("TP duyệt quyết toán hợp đồng") | `canTpApprove :110-113` ∧ không kiểm phòng | `A:Http/Controllers/Api/V1/SettlementContractController.php:360-364`; route `checkDueConfigsManager:Duyệt quyết toán công theo HĐ` `A:Routes/SettlementContract/api.php:27`; từ chối `tpReject :428` |
| KT (3 → 4) | `assign.quyet_toan_hop_dong_ke_toan.approve` | `canKtApprove :115-118` | `ktApprove :394-398`; `ktReject :459` |

* Điều kiện đặc thù: công khoán TP nhập **không được vượt** công khoán đã duyệt (`normErrors(... 'work_tp_approve' ...)` `:365-367`; lúc tạo `'work_request'` `:104`). Lập chỉ cho NV được giao QTC (`:93-101`).
* Lịch sử duyệt `settlement_contract_history_approves` (`:386`, `storeHistoryApprove :541`).
* **c)** Danh sách `index` theo view scope (chưa mở criteria); cờ `canTpApprove/canKtApprove` `A:Transformers/SettlementContractTransformer.php:78-79`. **Không có hàng chờ lọc theo người duyệt.**
* **d/e)** Như mục 9: không chặn tự duyệt, không chặn cùng người TP+KT.
* **Lỗi thông báo**: khi tạo/sửa, người nhận được lấy bằng `listEmployeeInfoByPermission('Duyệt quyết toán hợp đồng')` `A:Http/Controllers/Api/V1/SettlementContractController.php:117,160` — tên này **không có** trong Catalog (mã đúng là `assign.quyet_toan_hop_dong_truong_phong.approve` với legacy "TP duyệt quyết toán hợp đồng", `Catalog/assign.php:398-409`) ⇒ rất có thể không ai nhận thông báo (chưa chạy thử để xác nhận).

---

## 11. Hồ sơ thanh toán công tác (AS19, legacy)

1 cấp: `assign.ho_so_thanh_toan.approve` ("Duyệt hồ sơ thanh toán") — `canApprove` `A:Entities/PaymentProfile.php:135-138` (status 2 ∧ quyền, **không phòng/công ty**); `approve` `A:Http/Controllers/Api/V1/PaymentProfileController.php:162-166`; route `checkDueConfigsManager:Duyệt hồ sơ thanh toán` `A:Routes/PaymentProfile/api.php:24`. **Không có route từ chối.** Người duyệt được sửa số đêm/phòng/chi phí duyệt (`:173-177`). Người tạo tự duyệt không bị chặn.

---

## 12. Hợp đồng TKT (HĐ bán hàng, AS4) — TP → Pháp chế (tuỳ cờ) → BGĐ (đích danh)

**Cấp** (`A:Entities/Contract/Contract.php:21-24,272-282,312-340`): status 2 **Chờ TP duyệt** → 14 **Chờ pháp chế duyệt** (chỉ khi `need_legal_approval=1`) → 15 **Chờ BGĐ duyệt** (chỉ khi có điều kiện BGĐ và đã "Chuyển duyệt") → 16 Chờ KH ký. Từ chối ở bất kỳ bước ⇒ "Không duyệt" (sửa + gửi lại từ đầu). *(Tài liệu nền AS4 ghi "1 cấp, `STATUS_CHO_DUYET=2`, mã 'Duyệt hợp đồng' không kiểm phòng" — ĐÃ LỖI THỜI.)* Trạng thái 21 `GIA_HAN_CHO_DUYET` có tên nhưng không dùng ở đâu khác (grep `GIA_HAN_CHO_DUYET` chỉ thấy khai báo).

| Cấp | Mã | Điều kiện | Kiểm ở đâu |
|---|---|---|---|
| TP (`approvalStep()='tp'`) | `sale.hop_dong_du_an_tkt.approve` ("Trưởng phòng duyệt hợp đồng bán hàng") `A:Services/ContractService.php:758` | `contract.department_id` (phòng người lập) ∈ `listManageDepartmentIds()` (chặt) `:790-798` | **Nguồn duy nhất** `canActOnApprovalStep` `:788-807` → dùng cho cờ Resource `A:Transformers/DetailContractResource.php:529-546`, chốt chặn `assertCanActOnApprovalStep :815-822` (ném 403), mở chi tiết `isViewableByAccessGrant` `A:Http/Controllers/Api/V1/ContractController.php:138-153` |
| Pháp chế (`'legal'`) | `sale.hop_dong_du_an_tkt_phap_che.approve` `:760` | quyền ∧ `contract.company_id == current_company_role` `:799-800` | như trên |
| BGĐ (`'bgd'`) | `sale.hop_dong_du_an_tkt_ban_giam_doc.approve` `:762` | quyền ∧ cùng công ty (current) ∧ **`bgd_approver_id == auth()->id()`** (người được TP/Pháp chế chọn khi "Chuyển duyệt") `:801-805` | như trên |
| Chuyển duyệt BGĐ | người duyệt bước cuối trước BGĐ (Pháp chế nếu có cờ, không thì TP) | chọn 1 người có quyền BGĐ ở công ty HĐ `bgdApproverIds :991-997` (**không loại chính mình**) | `transferToBgd :952-975`; route `A:Routes/api.php:954` |

* **Điều kiện đi BGĐ** `bgdReasons :1128+`: vượt `max_extra_price_percent` phòng, quy chế có `change_approver`, bán dưới giá net có thưởng, HTHT đổi so quy chế (bước Pháp chế). Bước cuối trước BGĐ + dính điều kiện ⇒ `assertNoBgdNeeded :1200-1210` chặn Duyệt (bắt Chuyển duyệt) **trừ khi người duyệt có quyền BGĐ**.
* **c) Màn "chờ duyệt"**: **không có màn riêng**. Danh sách hợp đồng theo phạm vi XEM `sale.hop_dong_du_an_tkt.view` (`A:Http/Controllers/Api/V1/ContractController.php:56-62`, `PresaleViewScope::applyWithColumn`) + lọc status; người duyệt đích danh/Pháp chế ngoài phạm vi xem vẫn **mở được** HĐ qua `isViewableByAccessGrant` (vào từ thông báo) nhưng **không thấy trong danh sách** (BGĐ được chọn chỉ có `bgd_approver_id`, danh sách không xét cột này).
* **d)** Gửi duyệt: chỉ người lập `isCreator` `A:Services/ContractService.php:825-829`. Duyệt: **không chặn** người lập = TP duyệt (nếu người lập quản lý phòng mình và có mã TP).
* **e) Một người nhiều cấp** — chặt nhất nhóm nhưng có 3 hiệu ứng:
  1. TP đồng thời giữ mã BGĐ ⇒ bước cuối trước BGĐ bấm **Duyệt** được dù dính điều kiện BGĐ ⇒ nhảy thẳng Chờ KH ký, **bỏ qua cấp BGĐ** (`assertNoBgdNeeded :1202`, `DetailContractResource.php:545 is_bgd_required`). Đây là "tự nhảy cấp" duy nhất trong nhóm, có chủ đích ("người có quyền BGĐ vẫn Duyệt thẳng", `DetailContractResource.php:524`).
  2. TP/Pháp chế giữ mã BGĐ và tự chọn mình khi Chuyển duyệt ⇒ vừa chuyển vừa duyệt BGĐ, không chặn.
  3. Pháp chế = TP cùng người (đủ mã + quản lý phòng + cùng công ty): duyệt bước TP rồi bước Pháp chế liên tiếp, không chặn.
* **f)** `dueConfig:Duyệt hợp đồng bán,manager` ở route Duyệt và Chuyển BGĐ `A:Routes/api.php:944,954` (423 + popup hàng quá hạn; mode manager ⇒ chỉ xét `employee_manage_departments`). Chặn Duyệt khi hàng thiếu giá vốn công ty `assertProductCostsAvailable :930+`; còn ý kiến Pháp chế chưa Đạt ⇒ chặn (`assertLegalNotesPassed :920-927`). Hủy duyệt (Chờ KH ký → Không duyệt): chỉ người duyệt bước cuối (`canCancelApprove :1054-1059`); Đóng HĐ: người lập ∨ quản lý phòng ∨ người duyệt cuối (`canClose :1065-1078`).

---

## 13. Duyệt trong dự án / giải pháp / task (AS8–AS12, và gia hạn nhiệm vụ)

| Loại | Cấp & ai duyệt | Quản lý/phạm vi | Kiểm ở BE? |
|---|---|---|---|
| **Yêu cầu điều chỉnh giải pháp** (AS8) status 1 Đã gửi → 2 Tiếp nhận / 3 Từ chối `A:Entities/SolutionAdjustmentRequest.php:30-32` | PM của giải pháp (`solution.pm_id == me`) ∨ `receive_dept` của YC làm giải pháp ∈ `listManageDepartmentIdsWithOwn` — **không có mã quyền** `:96-113` | cờ `is_can_accept`/`is_can_reject` chỉ trả cho FE `:84-92` → FE `C:pages/assign/prospective-projects/components/SolutionAdjustmentTab.vue:45,158` | **KHÔNG**: `accept`/`reject` `A:Services/SolutionAdjustmentRequestService.php:56-79` và controller `:63-87` không kiểm quyền, không kiểm status; routes `A:Routes/api.php:438-439` không middleware ⇒ fail-open, cả phiếu đã xử lý |
| **Hồ sơ trình duyệt giải pháp** (AS9) `solution_review_profiles` status 'pending' | **Người tạo giải pháp** (`solution.created_by == auth()->id()`) | — | CÓ: `SolutionService::reviewSolutionProfileDecision` `A:Services/SolutionService.php:2706-2735` (ValidationException). Dự án tự triển khai không có bước này `:2709-2714` |
| **Hồ sơ trình duyệt hạng mục** (AS10) | PM giải pháp hoặc PM ghi trên hồ sơ `A:Services/SolutionModuleService.php:1412-1424` | — | CÓ |
| **Task — duyệt triển khai** (status 2 "Chờ phê duyệt triển khai" → 3/10) | `assign.trien_khai_task.approve` ∧ phòng người xử lý ∈ **managed ∪ own** `A:Entities/Task/Task.php:253-290` | quản lý-hoặc-thuộc-phòng | CÓ: `TaskService` kiểm `getAllowedNextStatuses` `A:Services/TaskService.php:606` ← `isStartApproverForAssignee` `Task.php:658` |
| **Task — duyệt kết quả** (status 6 "Hoàn thành - Chờ duyệt" → 8/7) | **người đích danh** `approver_id == auth()->id()` `Task.php:292-295,686-710` | — | CÓ (cùng `:606`). **Không có chặn `approver_id == assignee_id`** (`TaskStoreRequest.php:69` chỉ `exists`) ⇒ người làm tự duyệt kết quả của chính mình nếu được đặt làm người duyệt. |
| **Gia hạn nhiệm vụ** (mục MỚI, không có trong tài liệu nền) | người giao (`task.created_by == auth()->id()`) `A:Services/TaskExtensionService.php:123-128` | — | CÓ: `TaskExtensionService::approve/reject` + `TaskAccess::assertWritable` `A:Http/Controllers/Api/V1/TaskController.php:276-293`, route `A:Routes/api.php:1200-1202` |
| **Giải pháp chờ PM/Leader** (AS11) | PM/Leader qua `Solution::canEdit` (chưa mở; nêu đúng là bước phân công hơn là duyệt) | — | chưa xác minh |
| **BOM tổng hợp duyệt** | KHÔNG phải luồng riêng: `BomListService::syncStatusFromSubmission` đổi trạng thái BOM theo kết quả hồ sơ trình duyệt AS9 `A:Services/SolutionService.php:2756-2758` | = AS9 | — |
| **Hàng hoá dự án** (`/assign/product-project`) | **Không có bước duyệt riêng** — là view union của BOM tổng hợp duyệt + báo giá (xem memory `reference_hang_hoa_du_an_union_view`); không tìm thấy route approve trong `A:Routes/api.php` (`:531` chỉ `create-unit`) | — | — |
| **Yêu cầu XD giá** (`pricing-requests`) | Chỉ có `send` (`A:Routes/api.php:587-596`), **không có bước duyệt** | — | — |
| **Duyệt loại giảm giá** (AS23) | `assign.danh_muc_loai_giam_gia.manage` `A:Routes/api.php:1177` | — | route |
| **Issue** (AS15) | `approver_id` — chưa xác minh trong phiên này | — | chưa xác minh |

* **d/e)** Task: người giao (creator) có quyền duyệt triển khai + quản lý phòng ⇒ tự duyệt task mình giao (`PENDING_APPROVAL` cho phép `isStartApproverForAssignee` bất kể creator). Người làm = người duyệt kết quả ⇒ chuyển REVIEW rồi tự DONE (hai nhánh `getAllowedNextStatuses` độc lập `Task.php:687-710`).
* Hàng chờ Task: `SolutionService::getPendingApprovals` `A:Services/SolutionService.php:1706-1738` lọc đúng 2 tiêu chí (kết quả: `approver_id == me`; triển khai: quyền + phòng managed∪own) — khớp.

---

## 14. Ma trận "một người nhiều cấp" (tổng hợp)

| Loại | Hệ thống xử lý khi cùng người giữ nhiều cấp |
|---|---|
| Gia hạn dự án TKT | Bấm 2 lần (TP rồi BGĐ), không tự nhảy, **không chặn** |
| Báo giá cấp 3 | Bấm 2 lần (TP→BGĐ), không tự nhảy, **không chặn**; cấp 1 người lập tự duyệt |
| Yêu cầu làm giải pháp | 1 cấp |
| Phiếu công tác | `.create` "Lưu và duyệt" bỏ qua cấp duyệt; duyệt/nhập KQ/duyệt KQ độc lập, **không chặn** |
| Đề xuất công việc / Giao việc | "Lưu và duyệt" 1 lượt (FE: phòng mình + quyền), BE `store` không chặn; update giao việc không kiểm gì |
| Bàn giao | 1 cấp; tự duyệt phiếu mình không chặn |
| Đề nghị thanh toán / Quyết toán | TP rồi KT liên tiếp, **không chặn** `approver_id == kt_approver_id` |
| **Hợp đồng TKT** | TP+BGĐ ⇒ **tự nhảy cấp** (Duyệt thẳng, bỏ BGĐ); tự chọn mình khi Chuyển duyệt; TP+Pháp chế duyệt liên tiếp |
| Task | người làm = người duyệt KQ không chặn |

---

## 15. ĐÁNH GIÁ CHO BẢNG GOM (g) — Definition phải khai gì để biết "X thấy phiếu này ở cấp hiện tại"

Quan sát chính: **không có một công thức chung**. Cột gate đơn giản (mã quyền + phạm vi) đủ cho ~60% loại; còn lại cần thêm 3 trục.

Bốn kiểu gate:

1. **Mã quyền (không scope)** — luôn có (trừ nhóm 3): gate tối thiểu = `permission_code` + `status → cấp`.
2. **Quản lý phòng** — trục cần thêm: `dept_column` (cột trên phiếu: `department_id` / `department_request_id` / `department_implement_id` / `receive_dept` / `main_sale_department_id`/ phòng người xử lý task / phòng NV bàn giao) và `manager_mode`: `managed` (chặt, `manageDepartmentIdsOf`) hoặc `managed_or_own` (`listManageDepartmentIdsWithOwn`). Hai chế độ khác nhau theo loại:
   * `managed`: Báo giá TP, Gia hạn TKT TP, Phiếu công tác (duyệt/KQ), Đề xuất công việc, Hợp đồng TP, Giao việc (ý đồ).
   * `managed_or_own`: Bàn giao, Yêu cầu làm giải pháp, Task triển khai, YC điều chỉnh giải pháp.
3. **Công ty**: `company_match` kiểu `current_company_role` (Hợp đồng pháp chế/BGĐ, Phiếu công tác) hay `info.company_id` (Báo giá BGĐ, Gia hạn TKT BGĐ).
4. **Đích danh**: cột chứa người duyệt trên phiếu — Hợp đồng `bgd_approver_id`; Task `approver_id`; Gia hạn nhiệm vụ `task.created_by`; Hồ sơ giải pháp `solution.created_by`; Hồ sơ hạng mục `solution.pm_id ∨ profile.pm_id`.

Biểu diễn được bằng cột gate (`permission_code` + `dept_column|company_column|assignee_column` + `manager_mode`):
Gia hạn TKT (2 cấp), Báo giá (2 cấp), Yêu cầu làm giải pháp, Phiếu công tác duyệt & duyệt KQ, Đề xuất công việc (duyệt), Hợp đồng bước TP/Pháp chế/BGĐ (gate cấp 3 = `bgd_approver_id`), Bàn giao, Task, Đề nghị thanh toán/Quyết toán/Hồ sơ thanh toán/Gia hạn kết thúc sớm (chỉ mã, vì BE không kiểm phạm vi).

**Không biểu diễn được bằng một cột gate đơn giản** (cần xử lý riêng / quyết định nghiệp vụ):

* **Quyền "ở cấp nào" phụ thuộc dữ liệu động**: Hợp đồng — số bước có Pháp chế/BGĐ phụ thuộc `need_legal_approval` và `bgdReasons()` tính từ giá/HTHT (`A:Services/ContractService.php:1128+`); Báo giá cấp 3 phụ thuộc `price_approval_level`; Gia hạn TKT phụ thuộc ngưỡng ngày theo công ty. Definition chỉ cần map `status → cấp` (các status đã mã hoá cấp), không cần tính lại.
* **Gate theo ĐA điều kiện OR không có mã**: YC điều chỉnh giải pháp (PM ∨ phòng nhận, không mã quyền); Hồ sơ hạng mục (PM giải pháp ∨ PM hồ sơ).
* **Không phân cấp theo phòng ở BE nhưng danh sách có lọc**: Bàn giao (BE không kiểm), Đề xuất công việc/Giao việc (hàng chờ không lọc phòng) ⇒ cột gate cho Definition phải quyết định theo **tiêu chí DUYỆT thật (ý đồ nghiệp vụ)** chứ không lấy theo hàng chờ cũ, nếu không bảng gom sẽ hiện phiếu cho người sẽ bị 403.
* **Fail-open ở BE** (không có chốt thật): Giao việc (AS18), YC điều chỉnh giải pháp (AS8), `store` phiếu công tác/đề xuất công việc với `status_request=3`, YC làm giải pháp (không kiểm phòng) — bảng gom chỉ "hiện đúng người" thôi; muốn chặn thật phải vá BE từng chỗ (ngoài phạm vi bảng gom).
* **Cùng 1 phiếu ở 2 pha, 2 bộ người** — Đề xuất công việc: pha 1 duyệt `department_request_id` + `.approve`, pha 2 giao việc `department_implement_id` + `.create`: cần 2 cấp (2 dòng Definition) trên cùng bảng.
* **Chuỗi "TP rồi KT"** (Đề nghị thanh toán, Quyết toán): 2 cấp theo status 2/3, mỗi cấp 1 mã, không phạm vi — biểu diễn được; nhưng không có chặn "cùng người" ⇒ bảng gom có thể hiện 2 lần cho cùng người ở 2 thời điểm (bình thường).
* **Danh sách lệch với duyệt**: bảng gom nên dùng điều kiện DUYỆT làm chuẩn (vd `ensureTpCanApprove`), không lấy `type=waiting` của màn cũ.

Đề xuất schema Definition (mức gợi ý): `permission_codes[]` (hoặc 1 mã/cấp) · `level` (suy từ status) · `dept_column` · `manager_mode` ∈ {`managed`,`managed_or_own`,`none`} · `company_column` + `company_mode` ∈ {`current_company_role`,`info.company_id`,`none`} · `assignee_column` (cho đích danh) · `extra_or[]` (cờ thủ công cho các ca OR không mã quyền). Chưa cần "người đích danh cứng" kiểu cấu hình tay.

---

## 16. Mâu thuẫn / cập nhật so với tài liệu nền

1. **AS4 Hợp đồng**: nền ghi 1 cấp "Duyệt hợp đồng", không kiểm phòng, 0 role. Code hiện là **3 bước** (TP/Pháp chế/BGĐ đích danh), mã `sale.hop_dong_du_an_tkt{,_phap_che,_ban_giam_doc}.approve`, TP kiểm phòng quản lý, status 2/14/15/16 (`A:Services/ContractService.php:758-807`).
2. **AS18 Giao việc**: nền nói update/approveResult/deny không gọi `canApprove`; xác nhận **và** `deny` hoàn toàn không kiểm (kể cả đăng nhập bất kỳ) `A:Http/Controllers/Api/V1/AssignJobController.php:531-560`.
3. **AS16/AS17 `store` với `status_request=3`** (lập và duyệt 1 lượt) không kiểm quyền ở BE — nền chỉ nhắc `update` (JobRequest `:205`).
4. **AS16 Đề xuất công tác**: nền không nêu 2 mã khác nhau cho "Duyệt" (`.manage`) và "Không duyệt" (`.approve`) + cờ FE `isApprove` hard-code `true` (`C:pages/assign/assign_requests/_id/index.vue:6`).
5. **AS7** xác nhận "receive/reject không kiểm phòng"; bổ sung: hàng chờ lệch `isCanReceive` ở YC kiểu Triển khai theo phòng (managed vs own).
6. **AS3**: nền chỉ nêu dữ liệu 0 role; code xác nhận quyền (TP chặt `managed`, BGĐ `info.company_id`); bổ sung ngưỡng 30 ngày/công ty và việc thông báo gửi không lọc phòng.
7. **AS21**: thông báo dùng tên quyền không còn trong Catalog (`Duyệt quyết toán hợp đồng`) — nền không nêu.
8. **AS22**: xác nhận không kiểm phòng/công ty; bổ sung danh sách không có hàng chờ.
9. **danh-gia §2** "Duyệt kết quả công tác: không có từ chối" — xác nhận (không có đường `deny` cho status 5).
10. Mục mới ngoài nền: **Gia hạn nhiệm vụ** (người giao duyệt), **hai kiểu "quản lý"** (`managed` vs `managed_or_own`), **hai kiểu "công ty"** (`current_company_role` vs `info.company_id`), `dueConfig` (DB) khác `checkDueConfigsManager` (ERP, fail-open).
11. Số dòng trong nền (`api.php:505…1213…`) đã trôi so với file hiện tại; dùng số dòng trong tài liệu này.

### Chưa xác minh

* Chữ trạng thái BE trả cho phiếu legacy (`assign_requests`, `job_requests`, `assign_jobs`, `payment_business_requests`, `settlement_contracts`): hằng số có, chữ do FE map.
* Issue (AS15), Giải pháp chờ PM/Leader (AS11), Request validate của Handover/RequestSolution, `PaymentBusinessRequestService`, màn `assign_waiting_approve_result`.
* Việc vai trò Super Admin có được seed đủ mã nhóm này không (quyền là dữ liệu vai trò, không có bypass trong code).
