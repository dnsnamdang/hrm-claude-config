# Luồng QUYỀN DUYỆT — nhóm Tài chính / Kho (đọc từ code đang chạy) — @cuong61n

Ngày khảo sát 16/11/2026, nhánh `gop_db-main` (commit `44819ec83`), chỉ đọc code, không chạy DB. Mọi dòng dẫn theo `file:dòng` thật.

Ký hiệu đường dẫn: `F/` = `hrm-api/Modules/Finance/` · `A/` = `hrm-api/Modules/Assign/` · `M/` = `hrm-api/Modules/MasterData/` · `APP/` = `hrm-api/app/` · `FE/` = `hrm-client/`.
"Công ty đang làm" = `auth()->user()->current_company_role` (= `employee_infos.company_role ?: company_id`, `APP/Models/TpEmployee.php:97-113`). "Công ty của tôi" trong các hàm `sameCompanyAsCurrent` / `currentCompanyId()` = `info->company_id` (`F/Entities/Concerns/ChecksEmployeePermission.php:51-57, 85-90`). Hai khái niệm này có thể lệch nhau với người có `company_role` khác `company_id` (chưa xác minh trên dữ liệu thật).

---

## 0. PHÁT HIỆN CHUNG (đọc trước)

### 0.1 Tài liệu nền `inventory-hrm.md` phần Finance đã LỖI THỜI ở các điểm sau

| Tài liệu nền nói | Code hiện tại | Dẫn chứng |
|---|---|---|
| CEP query thẳng 3 bảng spatie, có đường `Super admin (role 18)` vượt quyền ở ~17 luồng | **Không còn.** Mọi câu hỏi quyền đi qua `PermissionLookup` → `PermissionChecker` theo Vai trò của người dùng **ở công ty đang làm**; trait ghi rõ "không còn quyền gán thẳng, không còn nhánh Super admin" | `F/Entities/Concerns/ChecksEmployeePermission.php:7-24`; `APP/Support/Permissions/PermissionLookup.php:23-31` |
| CEP "KHÔNG lọc `role_has_permissions.company_id`" — cấp ở công ty A dùng được ở mọi công ty | Quyền được xét **theo công ty đang làm** (`PermissionChecker::for(employee, company)`); đổi công ty đang làm là đổi tập quyền | `APP/Support/Permissions/CurrentPermission.php:26-39`; `PermissionLookup.php:55-64` |
| MW `checkPermission` + HLP `isCurrentEmployeeHasPermission` "sót role `App\Employee`" (spatie `getAllPermissions()`) | **Đã sửa:** cả middleware lẫn helper đều gọi `CurrentPermission::has()` (không còn spatie). Các docblock/comment "spatie bỏ sót" trong Controller/Routes là **cũ** | `APP/Http/Middleware/CheckPermission.php:9-30`; `APP/Helper/PermissionHelper.php:14-22` |
| F21 "2 lớp gate, MW chỉ cho 2/41 người" ; F25 "HLP chỉ thấy 3/75" | Lỗ hổng spatie đã hết; F21 nay là middleware mã `sale.hach_toan_mua_dich_vu.create` + `canAccounting()` cùng mã | `F/Routes/api.php:2301-2302`; `F/Entities/BuyServiceAccountingRequest/BuyServiceAccountingRequest.php:303-308` |
| Quyền "chỉ guard web" không cấp được ở màn phân quyền HRM (Quản lý giữ hàng, TP/BGĐ/KT hàng giữ, hàng mượn, mua dịch vụ…) | Code nay dùng **mã quyền** `finance.*`/`sale.*`/`accounting.*` (ví dụ `finance.hang_giu_truong_phong.approve`); `PermissionLookup` tra cả guard api+web qua alias | `F/Entities/PrepickExtend/PrepickExtendRequest.php:48-50` |
| F25 YCXH: "TP/BGĐ HRM KHÔNG có route", phiếu st10 chỉ duyệt trên ERP | **Đã có:** `switch-board-of-manager` (TP chuyển BGĐ 10→11) và `manager-approve` (BGĐ duyệt 11→2) | `A/Routes/api.php:797-800`; `A/Http/Controllers/Api/V1/ProductExportRequestController.php:1648, 1688` |
| F4 Phiếu chi "Cấp 2 thủ quỹ / cấp 5 KT trưởng" | Đúng nhưng **cấp 5 chỉ phát sinh ở loại chi 4 (Chi thu nhập NV, "nhánh B")**; loại chi khác đi thẳng cấp 2 | `F/Services/BillPaymentWriteService.php:355-358` |
| F15 "Cùng 1 người có thể giữ nhiều vai" | Đúng, và xem mục 0.4 — **hệ thống không chặn, không nhảy cấp, phải bấm từng cấp** | `F/Entities/BillPaymentRequest/BillPaymentRequest.php:928-945` |
| F1/F7/F10/F19/F22… "Super admin vượt cả điều kiện công ty" | Không còn nhánh SA. Điều kiện công ty còn lại tuỳ luồng (xem từng mục) | — |
| Docblock còn nói "Super Admin bỏ qua" (CheckDueConfig, canTPApprove, DeliveryRequest::canApprove…) | **Chỉ là comment cũ**, code không có nhánh SA | `F/Http/Middleware/CheckDueConfig.php:24`; `F/Entities/PrepickExtend/PrepickExtendRequest.php:224-228`; `F/Entities/DeliveryRequest/DeliveryRequest.php:420` |

### 0.2 FE không tự quyết quyền — mọi nút duyệt đến từ cờ BE (fail-closed)

- FE chỉ vẽ nút khi BE trả `is_can_approve` / `is_can_reject` / `is_can_deny` (≈70 file trong `FE/pages/finance` + `FE/pages/warehouse` dùng các cờ này). Ví dụ `FE/pages/finance/bill-payment-requests/components/ApproveActions.vue:31-32, 84, 97`; `FE/pages/finance/bill-payment-requests/index.vue:845`; `FE/pages/finance/product-import-requests/_id/index.vue:415, 443`.
- Mọi endpoint duyệt đều có gate BE (entity `canX()` hoặc middleware `checkPermission`). **Không phát hiện luồng nào CHỈ FE ẩn nút (fail-open)** trong nhóm khảo sát. Điểm yếu thật không nằm ở FE mà ở **độ chặt của gate BE** (thiếu kiểm công ty/phòng ban, mục 0.5).
- Menu: các lối "chờ duyệt" ở `FE/components/subsystem-menu/finance.js:640-715` và `sale-hub.js:360-364` gate bằng `codes: [...]` của **mã quyền**; riêng Đề nghị thanh toán, Hạch toán bổ sung KHÔNG gate (BE tự lọc theo vai).

### 0.3 Bốn kiểu "QUẢN LÝ" khác nhau cho cùng chữ "Trưởng phòng duyệt"

| Kiểu | Cách lấy "phòng tôi quản lý" | Dùng ở |
|---|---|---|
| **K1 — chỉ pivot, bỏ cờ `all_department`** | `employee_manage_departments` theo công ty của tôi, KHÔNG cộng phòng mình ngồi, KHÔNG xét "quản lý tất cả phòng ban" | Đề nghị thanh toán TP (`BillPaymentRequest.php:430-441, 898-905`); YCXH TP (`A/.../ProductExportRequest.php:423-441`); Mua dịch vụ **(không kiểm phòng khi duyệt)** |
| **K2 — pivot + phòng mình ngồi** (hàm `manageableDepartmentIds()`) | pivot **cộng** `info->department_id` của chính mình. Docblock gọi đây là "quy ước chung phân hệ Tài chính, user chốt 23/09/2026" | Gia hạn/Xuất giữ/Điều chuyển hàng giữ: `PrepickExtendRequest.php:289-306`, `ProductPrepickRequest.php:~440-460`, `PrepickTransferRequest.php:~325-345`; `BuyServiceRequest.php:455-471` (chỉ cho **danh sách**) |
| **K3 — như K2 nhưng có cờ `all_department`** | `manageDepartmentIdsOf()` + phòng mình ngồi | **Chỉ** Gia hạn hàng mượn: `BorrowExtendRequest.php:304-319` |
| **K4 — `currentManagedDepartmentIds()`** | pivot theo công ty của tôi, KHÔNG có phòng mình ngồi | Xuất bán hàng mượn TP: `BorrowSellRequest.php:160-169`; `ChecksEmployeePermission.php:62-76` |

Hệ quả: người được tích "Quản lý tất cả phòng ban" chỉ duyệt được ở Gia hạn hàng mượn (K3); các luồng khác họ không thấy/không duyệt được phiếu của phòng khác (K1/K2/K4 chỉ đọc pivot theo `department_id`). Người giữ quyền TP nhưng **không phải quản lý** vẫn duyệt được phiếu **phòng mình ngồi** ở nhóm hàng giữ (K2) — kể cả phiếu do chính mình lập.

### 0.4 "MỘT NGƯỜI NHIỀU CẤP" — quy luật chung của nhóm Tài chính/Kho

1. **Không có luồng nào tự nhảy cấp** và **không có luồng nào chặn** người giữ nhiều cấp. Mỗi lần gọi API chỉ xử lý đúng cấp ứng với **trạng thái hiện tại** (`nextStatuses()` / `if ($current === CHO_TP…)` / `canApprove()` theo `status`). Người giữ 2 cấp liên tiếp phải bấm Duyệt lần lượt, mỗi lần đóng dấu id của mình vào cột người duyệt của cấp đó (ví dụ `BillPaymentApprovalService.php:261-273`, `PrepickExtendRequestService.php:716-720, 745-750, 763-770`).
2. **Không có luồng nào cấm người LẬP phiếu tự duyệt**, trừ **Kế hoạch bán hàng / phát triển thị trường NV** (`EmployeePlan`, mục 18): nhánh `applyForApproveScope` loại `created_by = tôi` và `isHeadOfPlan()` đòi `!isOwner()` (`EmployeePlan.php:257-270, 280-283`).
3. Có **đúng 1 chỗ tự nhảy cấp theo người lập**: Kế hoạch NV — người lập là trưởng phòng của phòng phiếu thì gửi duyệt đi thẳng `1 → 4 (Chờ BGĐ)`, bỏ cấp TP (`F/Services/EmployeePlan/EmployeePlanService.php:484-486`; `creatorIsHead()` `EmployeePlan.php:363-369`).
4. Một số luồng không có bước "chờ" thật: người lập có quyền thì **lưu là duyệt luôn** (Quyết toán thưởng năng suất quý, mục 15).
5. Rẽ cấp (có/không qua BGĐ) **không do người chọn** mà do dữ liệu: nhóm hàng giữ theo công thức hợp đồng/giá trị (`F/Services/PrepickApprovalRouteService.php:75, 112`), Gia hạn hàng mượn theo `Σ(đã xuất − đã trả) × giá > companies.borrow_limit_value` (`BorrowExtendRequestService.php:634-643`). Ngoại lệ do **người chọn**: KT trưởng chọn "Duyệt" (→ chờ tạo phiếu chi) hoặc "Chuyển duyệt BGĐ" (Đề nghị thanh toán — không có ngưỡng tiền, `BillPaymentRequestApproveRequest.php:rules`, `FE/.../ApproveActions.vue:62-68`); TP xuất bán hàng mượn chọn "Duyệt" hoặc "Chuyển BGĐ" (`BorrowSellRequestController.php:192, 203`); BKS yêu cầu nhập hàng chọn duyệt / chuyển BGĐ / từ chối (`ProductImportRequestController.php:422-436`).

### 0.5 Các điểm gate BE yếu / lệch cần nêu cho bảng gom

| # | Điểm | Dẫn chứng |
|---|---|---|
| Y1 | Duyệt cấp **không kiểm công ty của phiếu**: Phiếu thu (thủ quỹ), Yêu cầu nhập hàng (cả 4 cấp), YC mua dịch vụ cấp TP, Yêu cầu huỷ giữ, YC xuất mượn (KT kho), Kiểm kê hàng hoá/vị trí (BKS), Biên bản thừa thiếu, Quyết toán thưởng năm (BGĐ), Phân chia thị trường (phòng ban), Xuất bán hàng mượn (TP/BGĐ/KT), Không duyệt Đề nghị thu tiền | các mục tương ứng |
| Y2 | Cấp TP **không kiểm phòng ban của phiếu**: Yêu cầu nhập hàng (`ProductImportRequest.php:1106-1110`), YC mua dịch vụ (`BuyServiceRequest.php:285-299`, ghi rõ "bám ERP") | — |
| Y3 | Cấp TP kiểm phòng nhưng **cộng phòng mình ngồi** (K2) → người không quản lý vẫn duyệt được phiếu phòng mình, kể cả phiếu của mình | mục 0.3 |
| Y4 | Danh sách chờ duyệt **rộng hơn** quyền duyệt: Xuất bán hàng mượn `waiting_approve` trả mọi phiếu `CHO_KE_TOAN_KHO` của công ty cho **bất kỳ ai** (không kiểm quyền KT kho) (`BorrowSellRequest.php:268-281`); Yêu cầu nhập hàng preset `for_approve` (status 2 + công ty) không kiểm quyền KT kho (`ProductImportRequest.php:1243-1251`) | — |
| Y5 | Danh sách chờ duyệt **hẹp hơn** quyền duyệt: Phiếu thu/Phiếu chi không có chế độ "chờ tôi duyệt", người duyệt chỉ thấy qua quyền xem theo cấp (`BillIncomeService.php:61-85`, `BillPayment.php:337-370`); Kiểm kê vị trí `scopedQuery` không có nhánh người duyệt dù `canView` có (`PositionInventoryResult.php:164-190, 193-205`) | — |
| Y6 | TP kiểm phòng **bằng cách khác** ở danh sách và ở nút duyệt: Yêu cầu nhập hàng (list có `manageDepartmentIds`, duyệt không kiểm phòng); Mua dịch vụ (list `manageableDepartmentIds`, duyệt không kiểm) | `ProductImportRequest.php:1269-1275` vs `:1106` |
| Y7 | Không duyệt Đề nghị thu tiền: **controller chỉ kiểm `isAccountant()`**, docblock service nói `canReject()` nhưng không gọi → không kiểm công ty của phiếu, không kiểm trạng thái ngoài so `status==2` thủ công | `F/Http/Controllers/V1/BillIncomeRequestController.php:195-210` |
| Y8 | `dueConfig:…,manager` chặn **mọi cấp** có đặt middleware (kể cả KT trưởng, BGĐ) nếu người bấm **quản lý phòng** có nhân viên còn hàng quá hạn — kiểm theo pivot `employee_manage_departments` (không có phòng mình ngồi, không có `all_department`) | `F/Services/DueConfigBlockService.php:171-205` |
| Y9 | Cờ `all_department` bị bỏ sót ở 8/9 luồng TP (xem 0.3) | — |

### 0.6 Chặn thêm "hàng quá hạn" (`dueConfig`, mục f chung)

Middleware `dueConfig:<thao tác>,manager` (423 + `show_overdue_modal`) gắn ở: Đề nghị thanh toán `store/update/approve` (`F/Routes/api.php:1287-1292`), Yêu cầu nhập hàng 3 cấp (`:615-617`), Gia hạn hàng giữ approve (`:1108`), Xuất giữ approve (`:1149`), Điều chuyển hàng giữ approve (`:1212`), Xuất bán hàng mượn TP (`:1549`), Gia hạn hàng mượn approve (`:1727`), Mua dịch vụ TP (`:2267`). **Các route reject KHÔNG có middleware.** Điều kiện chặn: người bấm quản lý (pivot) phòng nào đó có nhân viên còn hàng giữ / hàng mượn / hàng nhập thẳng quá hạn, và công ty đã bật `company_due_configs` cho thao tác đó (`DueConfigBlockService.php:171-205, 268-285`). Docblock "Super Admin bỏ qua" là sai với code.

---

## 1. Đề nghị thanh toán (`bill_payment_requests`) — 5 cấp

Entity `F/Entities/BillPaymentRequest/BillPaymentRequest.php`; mã quyền `:193-199`.

### a) Các cấp (BE trả chữ ở `STATUSES` `:~82-93`)

| status | Chữ BE | Điều kiện chuyển | Chuyển tới |
|---|---|---|---|
| 1 | Đang tạo | người lập gửi | 2 |
| 2 | Chờ TP duyệt | TP duyệt | 3 |
| 3 | Chờ kế toán công nợ duyệt | KT công nợ duyệt | 4 |
| 4 | Chờ kế toán trưởng duyệt | **KT trưởng chọn**: "Duyệt" → 6, "Chuyển duyệt BGĐ" → 5 (không có ngưỡng tiền) | 5 hoặc 6 |
| 5 | Chờ ban giám đốc duyệt | BGĐ duyệt | 6 |
| 6 | Chờ tạo phiếu chi | kế toán thanh toán lập Phiếu chi (không phải nút duyệt trong màn này, `BillPaymentRequestListResource.php:113-121` loại st6 khỏi `is_can_approve`) | 7/8/9 (phiếu chi) |
| 10 | Không duyệt | Không duyệt: ở st2 → về **1 Đang tạo**, ở st3/4/5/6 → **10** (`BillPaymentApprovalService.php:197-200`) | — |

Nguồn `nextStatuses()`: `BillPaymentRequest.php:928-945`; service `approve()` chặn nhảy cóc `:87-96`.

### b) Ai duyệt từng cấp (`canApproveAtCurrentStatus()` `:887-917`)

| Cấp | Mã quyền | Quản lý? | Công ty |
|---|---|---|---|
| Chờ TP (2) | `finance.de_nghi_thanh_toan_truong_phong.approve` | **Có — K1**: phòng của phiếu ∈ pivot `employee_manage_departments` của tôi (`:896-905`); phòng của phiếu = phòng **người lập lúc tạo** (hook `creating` `:255-267`) | phiếu = công ty tôi (`:889-892`) |
| Chờ KT công nợ (3) | `finance.de_nghi_thanh_toan_ke_toan_cong_no.approve` | Không | cùng công ty |
| Chờ KT trưởng (4) | `finance.de_nghi_thanh_toan_ke_toan_truong.approve` | Không | cùng công ty |
| Chờ BGĐ (5) | `finance.de_nghi_thanh_toan_ban_giam_doc.approve` | Không | cùng công ty |
| Chờ tạo phiếu chi (6) | `finance.ke_toan_thanh_toan.manage` | Không | cùng công ty |

### c) Kiểm ở đâu / danh sách chờ

- `POST /{id}/approve` → `BillPaymentRequestController.php:149-160` kiểm `canApproveAtCurrentStatus()`; `POST /{id}/change-status` (Không duyệt) → `:163-175` kiểm `canCancel()` (= `canApproveAtCurrentStatus()`, `:919-922`). Không dùng `checkPermission`. Chặn 423 `dueConfig:Duyệt đề nghị thanh toán,manager` ở `store/update/approve` (`F/Routes/api.php:1287-1292`).
- Danh sách chờ `?mode=pending` → `searchByFilter($r,'pending')` `:425-460`: cùng công ty **và** (TP: có mã TP + `status=2` + `department_id ∈ pivot`) hoặc (cấp 3/4/5/6: có mã + `status` tương ứng); không mã nào → `1 = 0`. **Khớp 1-1 với gate duyệt** (cùng điều kiện, cùng K1). Điều kiện "ai thấy" = "ai duyệt" → tốt cho bảng gom.
- FE: `index.vue:845` `visible: !!item.is_can_approve`; `ApproveActions.vue:62-68` nút theo trạng thái, chỉ render khi `canApprove`.

### d) Người lập tự duyệt?

Không chặn. `canApproveAtCurrentStatus()` không xét `created_by`. Người lập giữ mã TP và quản lý phòng của chính phiếu có thể gửi (st2) rồi tự duyệt cấp TP. Tương tự các cấp 3–6 nếu giữ mã.

### e) Một người nhiều cấp

Phải bấm tuần tự từng cấp; mỗi lần `stampApprover` ghi id vào cột cấp đó (`BillPaymentApprovalService.php:261-273`). Một người giữ mã cấp 3,4,5 → 3 lần duyệt, mỗi lần mở lại phiếu (sau duyệt FE quay về danh sách). Số tiền duyệt từng cấp được sửa tại bước đó, không trần theo cấp trước (`:77-85`).

### f) Khoá / đặc thù

`dueConfig` manager (mục 0.6) áp lên **cả KT trưởng, BGĐ…** nếu họ quản lý phòng có hàng quá hạn. Hạn mức tiền: không có trần nào ở BE (`BillPaymentRequestApproveRequest.php` chỉ `numeric|min:0`).

### g) Đánh giá cho bảng gom

Định nghĩa cần: **bản đồ `status → {mã quyền, cờ "quản lý phòng của phiếu (K1)", cùng công ty}`**. Cột gate đơn giản (1 mã) KHÔNG đủ: 5 cấp = 5 mã khác nhau + 1 cấp đòi quản lý phòng. Biểu diễn được bằng danh sách `{status, code, require_manage_department, same_company}`.

---

## 2. Đề nghị thu tiền (`bill_income_requests`)

`F/Entities/BillIncomeRequest/BillIncomeRequest.php`.

| status | Chữ BE | Ai duyệt | Gate |
|---|---|---|---|
| 1 | Đang tạo | người lập | — |
| 2 | Chờ KT duyệt | **Kế toán thanh toán** `finance.ke_toan_thanh_toan.manage` (`:90`) | `isAccountantActionable()` = `status==2 && isAccountant()` `:644-647` |
| 3 | Đã tạo phiếu thu | "Duyệt" thực chất là **lập Phiếu thu** (`BillIncomeWriteService.php` đặt `BillIncomeRequest` → 3, `:99-106`) | `canCreateBillIncome()` `:626-641` (+ chưa có phiếu thu) |
| 6 | Không duyệt | Không duyệt `POST /{id}/change-status` | — |

- **Quản lý?** Không. **Công ty?** Danh sách pending lọc `company_id = công ty tôi` (`:295-298`); nhưng **gate `changeStatus` không kiểm công ty phiếu** (`BillIncomeRequestController.php:195-210` chỉ `isAccountant()` + `status==2`). `canReject()` (`:611`) có tồn tại nhưng Controller KHÔNG gọi (docblock service `:410-416` nói có gọi → lệch). `pending()` gate 403 bằng `isAccountant()` (`:56-60`).
- (d) Người lập tự duyệt: không chặn (chỉ cần có mã kế toán thanh toán).
- (e) 1 cấp, không có chuyện nhiều cấp.
- Menu gate `codes: ['finance.ke_toan_thanh_toan.manage']` (`FE/components/subsystem-menu/finance.js:648-654`).
- (g) Gate đơn giản: 1 mã + `status=2` + công ty (danh sách). Biểu diễn được bằng 1 cột gate. Lưu ý: gate duyệt lỏng hơn gate danh sách (Y7).

---

## 3. Yêu cầu hạch toán bổ sung (`addition_accounting_requests`)

`F/Entities/AdditionAccountingRequest/AdditionAccountingRequest.php`.

| status | Chữ BE | Ai | Gate |
|---|---|---|---|
| 1 Đang tạo | người lập | `canEdit` `:659` |
| 2 Chờ duyệt | **Từ chối**: `finance.ke_toan_thanh_toan.manage` (`:229`) + `matchesCompanyOrSupportScope` (`canReject` `:687-694`); từ chối → về **1 Đang tạo** (`nextStatuses`, `WriteService:289`) | |
| 2 → (lập phiếu kế toán) | `canCreateAccountingBill()` `:700-718` |
| 3/4 | ngoài phạm vi, chỉ hiển thị |

- Loại 1–6 (`!= TYPE_COORDINATION`): "lập phiếu" = `isAccountant()` + phiếu cùng công ty.
- **Loại 7 (điều phối, hỗ trợ nhiều phòng)**: **hai mã khác nhau trong cùng 1 phiếu**: Từ chối cần `finance.ke_toan_thanh_toan.manage` tại công ty hỗ trợ (`canReject`); **Lập phiếu cần `accounting.ke_toan.manage`** (`PERMISSION_ACCOUNTANT_SUPPORT` `:232`) và công ty tôi ∈ công ty của các phòng hỗ trợ (`:709-714`). Danh sách pending: `isAccountant() || isSupportAccountant()` thấy phiếu loại 1–6 cùng công ty **hoặc** loại 7 có phòng hỗ trợ thuộc công ty mình (`applyCompanyOrSupportScope` `:404-427`, `:333-342`); người không phải kế toán chỉ thấy phiếu **của mình** chờ duyệt.
- (d) người lập tự từ chối/lập phiếu: không chặn nếu giữ mã.
- (g) **Không biểu diễn được bằng 1 mã**: loại 7 cần OR của 2 mã tuỳ hành động (từ chối ≠ lập phiếu) và "công ty tôi ∈ công ty các phòng hỗ trợ (bảng con `additionDepartments`)". Cần cấu trúc `status + type → {mã, phạm vi công ty phụ thuộc bảng con}`.

---

## 4. Yêu cầu điều chỉnh công nợ (`bill_adjust_dept_requests`)

`F/Entities/BillAdjustDeptRequest/BillAdjustDeptRequest.php`.

- Cấp: 1 Đang tạo → 2 **Chờ tạo phiếu kế toán** (`:102`) → 6 Không duyệt (từ chối) / "Tạo phiếu kế toán" (màn khác, st3/4).
- Ai: `finance.ke_toan_thanh_toan.manage` (`:139`) **và** `company_id` phiếu = công ty tôi (`canReject` `:472-483`; `canCreateAccounting()` `:498` dùng lại cùng hàm).
- Kiểm ở: `WriteService:253` (`canReject()` khi chuyển sang `REJECT`).
- **Lệch giữa gate duyệt và danh sách chờ:** pending lọc theo **công ty của người lập** (`whereHas('employee_create.info', company_id = tôi)` `:248-250`) trong khi `canReject()` lọc theo `company_id` ghi trên phiếu → có thể lệch nếu người lập đổi công ty sau khi lập.
- (d) tự duyệt: không chặn. (e) 1 cấp. (g) 1 mã + công ty phiếu; biểu diễn được bằng 1 cột gate (ưu tiên `company_id` trên phiếu).

---

## 5. Duyệt giá bán hàng hoá (`product_approves`, MasterData)

- Mã `finance.gia_ban_hang_hoa.approve` (`APP/Support/Permissions/Catalog/finance.php:848`). Một cấp. Route group gắn `checkPermission:finance.gia_ban_hang_hoa.approve` cho cả `index/approve/reject/bulk` (`M/Routes/api.php:493-504`).
- Phạm vi: `product_approves.company_id = công ty đang làm` (`M/Services/ProductPrice/ProductPriceApprovalService.php:272`; `companyId()` `:87-90`). Yêu cầu của công ty khác không thấy.
- Không kiểm "quản lý", không loại người đề xuất (`proposer = updated_by`, cột `:351-354, 416`), **người đề xuất có mã thì tự duyệt được**.
- Danh sách chờ = chính màn Duyệt giá bán (`/finance/product-price-approvals`), gate menu cùng mã (`FE/.../finance.js:522, 690`) → "ai thấy" = "ai duyệt".
- (g) Biểu diễn bằng 1 cột gate: mã + công ty đang làm = `product_approves.company_id`. Ngoại lệ dữ liệu: hàng khoá (🔒) vẫn hiện, có kiểm `assertNotLocked` khi duyệt (`:487-505`).

---

## 6. Gia hạn hàng mượn (`borrow_extend_requests`) — 3 cấp

`F/Entities/BorrowExtend/BorrowExtendRequest.php`; mã `:58-63`.

| status | Chữ BE | Ai duyệt | Quản lý | Công ty |
|---|---|---|---|---|
| 4 Chờ TP duyệt | `finance.hang_muon_truong_phong.approve` | **K3**: pivot (kể cả `all_department`) **+ phòng mình ngồi** (`canTPApprove` `:240-251`, `manageableDepartmentIds` `:304-319`) | cùng công ty |
| 5 Chờ BGĐ duyệt | `finance.hang_muon_ban_giam_doc.approve` (`canBGDApprove` `:226-231`) | không | cùng công ty |
| 2 Chờ KT duyệt | **`accounting.ke_toan_kho.manage`** (`canApprove` `:218-223`) | không | cùng công ty |
| 1 Đã duyệt / 3 Không duyệt | | | |

- Rẽ cấp: sau TP, `needBoardApprove` = `Σ(xuất − trả) × giá` của YC xuất hàng nguồn `> companies.borrow_limit_value` ⇒ qua BGĐ (st5) còn không đi thẳng KT (st2) (`BorrowExtendRequestService.php:634-643`, gọi `:467`).
- Kiểm ở: `POST /{id}/approve` có `dueConfig:Duyệt gia hạn hàng mượn,manager` (`F/Routes/api.php:1727`); gate từng cấp trong service (`:~455-480`); `reject` dùng `canApproveAnyLevel()` (`BorrowExtendRequestService.php:587`).
- Danh sách chờ `?type=for-approve` (`PRESET_FOR_APPROVE` `:336`): bó công ty, đúng vai (đã verify docblock `:380`). Menu gate `Kế toán kho` nhưng BE tự lọc theo vai (`FE/.../finance.js:700-708`) → **TP/BGĐ không có mã KT kho không thấy mục menu** dù duyệt được (menu hẹp hơn quyền).
- (d) tự duyệt: không chặn. (e) tuần tự. (f) `dueConfig` manager.
- (g) status→{mã, quản lý K3}; cấp 5 có thể bị bỏ qua do dữ liệu (không ảnh hưởng gate vì gate đọc `status`).

---

## 7. Hàng giữ — 4 màn

Dùng chung 3 mã `finance.hang_giu_truong_phong.approve` · `finance.hang_giu_ban_giam_doc.approve` · `finance.hang_giu_ke_toan.approve` (`PrepickExtendRequest.php:48-50`, `ProductPrepickRequest.php:68-70`, `PrepickTransferRequest.php:53-55`) và mã xem `finance.phieu_hang_giu.view`.

### 7.1 Gia hạn hàng giữ (`prepick_extend_requests`)

| status | Chữ BE | Ai duyệt | Ghi chú |
|---|---|---|---|
| 3 Đang tạo | người lập | |
| 5 Chờ TP duyệt | `canTPApprove` `:229-241`: mã TP + cùng công ty + **phòng phiếu ∈ K2** (pivot + phòng mình ngồi) | |
| 4 Chờ BGĐ duyệt | `canBKSApprove` `:218-227`: mã BGĐ + cùng công ty | **chỉ khi** `needBoardApprove` (`Service:948-961`) |
| 2 Chờ KT duyệt | `canApprove` `:210-216`: mã KT + cùng công ty; bước này **ghi tồn giữ** (`Service:~750-770`) | |
| 1 Đã duyệt | | |

- Một endpoint `approve` cho 3 cấp, service rẽ theo `status` (`Service:694-775`), gate từng cấp bằng đúng hàm của cấp đó. `reject` dùng `canApproveAnyLevel()` (`:898`), từ chối → **3 Đang tạo**.
- Danh sách chờ: `orWhereApprovable` `:414-470` — mỗi mã mở đúng 1 status; TP lọc `department_id ∈ K2`; cùng công ty. **Khớp gate duyệt.**

### 7.2 Yêu cầu xuất giữ (`product_prepick_requests`)

- status 6 Chờ TP → 4 Chờ BGĐ (nếu `needBoardApprove` theo **hợp đồng ở đầu phiếu** `Service:950`) → 2 Chờ KT. **TP xét phòng GHI TRÊN PHIẾU** (`canManagerApprove` `:376-390`, K2 `:456`). BGĐ: mã BGĐ + cùng công ty (`:365-373`). **Cấp KT không có nút Duyệt:** KT lập **Phiếu xuất giữ** (`warehouse-prepick-requests`) và chính phiếu đó ghi tồn (`canApprove` `:357-363`, docblock).
- Từ chối ở cả 3 cấp (`canReject` `:399-402` = TP|BGĐ|KT) → về **3 Đang tạo** + `comment` (`F/Routes/api.php:1117-1121`).
- `dueConfig:Duyệt yêu cầu xuất giữ,manager` ở approve (`:1149`); cũng chặn **mở lập** (`dueConfig:Lập yêu cầu xuất giữ`).

### 7.3 Điều chuyển hàng giữ (`prepick_transfer2` / `PrepickTransferRequest`)

- status 5 Chờ TP → 4 Chờ BGĐ → 2 Chờ KT; từ chối → **3 Không duyệt** (`Service:987`). **Khác 7.1/7.2:** TP xét phòng của **nhân viên NHẬN** (`toEmployeeDepartmentId` `:276-281`, `canTPApprove` `:260-273`) — không phải phòng của người lập.
- Danh sách `is_can_approve` = `canApproveAnyLevel()` (`PrepickTransferRequestListResource.php:69`).

### 7.4 Yêu cầu huỷ giữ (`prepick_cancel_requests`)

- 1 cấp: status **CHO_DUYET** → quyền `finance.giu_hang.manage` ("Quản lý giữ hàng") — **không kiểm công ty trên phiếu** (`canApprove` `:213-217`, docblock "giữ nguyên hành vi ERP"); `reject` (`PrepickCancelRequestController.php:184-197`) gate bằng `canApprove()`; "Duyệt" = lập Phiếu huỷ giữ, kiểm `canApprove()` trong transaction (`PrepickCancelService.php:277-297`).
- Danh sách `waitingRequests`: phải là `isPrepickManager()` và **lọc công ty** (`PrepickCancelService.php:227-243`) → danh sách chặt hơn gate duyệt.
- Quản lý: **không**. Tự duyệt: không chặn (`finance.giu_hang.manage` có 584 người trên DB theo tài liệu nền).

### (d)(e)(f)(g) chung nhóm hàng giữ

- (d) Không chặn người lập (đặc biệt K2: người lập là NV ngồi phòng đó và có mã TP ⇒ duyệt được phiếu của chính mình).
- (e) Người giữ 2–3 mã duyệt tuần tự.
- (f) `dueConfig` manager.
- (g) status→{mã, quản lý K2 theo phòng **phiếu** (7.1, 7.2) hoặc phòng **người nhận** (7.3)}; riêng huỷ giữ chỉ 1 mã. **Phòng đích của TP lấy từ 2 nguồn khác nhau** → cột gate cần `manager_scope = {doc.department | to_employee.department}`.

---

## 8. Yêu cầu xuất bán hàng mượn (`borrow_sell_requests`)

`F/Entities/BorrowSellRequest/BorrowSellRequest.php`; mã `:56-62`.

| status | Chữ BE | Ai | Gate |
|---|---|---|---|
| 10 Chờ TP duyệt | `finance.xuat_hang_vuot_han_muc_cong_no_truong_phong.approve` + phòng phiếu ∈ **K4** (pivot, không phòng mình ngồi) — **không kiểm công ty phiếu** (`canManagerApprove` `:160-169`) | TP chọn **"Duyệt"** → 2 (`Service:621`) hoặc **"Chuyển BGĐ"** → 11 (`:634`) |
| 11 Chờ BGĐ duyệt | `finance.xuat_hang_vuot_han_muc_cong_no_ban_giam_doc.approve` — **không kiểm công ty** (`:171-175`) | → 2 (`:647`) |
| 2 Chờ KT kho | `accounting.ke_toan_kho.manage` (`canApprove` `:154-158`); "duyệt" = lập Phiếu xuất bán hàng mượn (`BorrowSell::userCanCreate` `BorrowSell.php:290`) | |
| 4 Không duyệt | `deny`: `canDeny` = 1 trong 3 cấp (`:177-180`) | |

- Route: `deny/manager-approve/switch-board-of-manager/board-of-manager-approve` **không có `checkPermission`**, chỉ `canX()` ở Controller (`BorrowSellRequestController.php:181-223`); duy nhất `manager-approve` có `dueConfig:Duyệt yêu cầu xuất bán hàng mượn,manager` (`F/Routes/api.php:1549`) — `switch-board-of-manager` KHÔNG chặn.
- Danh sách chờ `type=waiting_approve` (`:268-281`): TP lọc phòng K4, BGĐ không công ty, và nhánh `CHO_KE_TOAN_KHO + công ty` **không kiểm quyền** ⇒ bất kỳ ai gọi `?type=waiting_approve` thấy mọi phiếu chờ KT kho của công ty (Y4). Màn này chỉ có trang, không có mục menu (theo tài liệu nền, chưa xác minh lại).
- (d) tự duyệt: không chặn. (e) TP nhiều cấp: TP và BGĐ là 2 mã tách; 1 người có cả 2 mã đi 2 lần. (f) dueConfig chỉ trên `manager-approve`.
- (g) status→{mã, K4 (cấp TP), công ty (không)}. Cấp KT kho = gate "mã" nhưng danh sách không gate theo mã.

---

## 9. Yêu cầu nhập hàng (`product_import_requests`)

`F/Entities/ProductImportRequest/ProductImportRequest.php`; mã `:32-37`.

| status | Chữ BE | Ai | Ghi chú |
|---|---|---|---|
| 12 Chờ TP duyệt | `finance.yeu_cau_nhap_hang.approve` (`canApproveByManager` `:1106-1110`) — **không kiểm phòng, không công ty** | chỉ loại **4 (bán trả lại)** và **9 (nhập bán mượn trả lại)** vào st12 (`Service:1957-1972`) → TP duyệt → st2 |
| 10 Chờ BKS duyệt | `finance.gia_nhap_hang_tra_lai_ban_kiem_soat.approve` (`:1115-1120`) — không công ty | vào st10 khi người lập gửi thẳng, **chỉ khi** hợp đồng đã quyết toán (`guardControlBoardStatus` `Service:1256-1275`). BKS chọn duyệt / **chuyển BGĐ** / từ chối (`Controller:422-436`) |
| 11 Chờ BGĐ duyệt | `finance.gia_nhap_hang_tra_lai_ban_giam_doc.approve` (`:1124-1129`) — không công ty | duyệt / từ chối |
| 2 Chờ duyệt (KT kho) | **`accounting.ke_toan_kho.manage`** (`canApprove` `:1071-1100`) | Duyệt = lập Phiếu nhập kho. **Ngoại lệ định danh:** loại 7 → **người tạo YCXH nguồn** cũng được (`:1076-1086`); loại 6 (điều chuyển nội bộ) → **chỉ người tạo** (`:1095-1097`); phiếu `is_import_direct` → dùng `canProductImport` |
| 3 Đang tạo / 6 Đã huỷ… | | |

- Từ chối: `canDeny` (`:1147-1151`), bắt buộc ghi chú.
- Danh sách chờ (preset): `for_approve` = status 2 + công ty (**không kiểm quyền KT kho**, `:1243-1251`), `managerApprove` (BKS/BGĐ theo mã, nếu không có mã nào thì thấy phiếu mình, `:1252-1268`), `departmentManagerApprove` (TP: st12 + phòng ∈ `manageDepartmentIds` — pivot theo công ty tôi (+ phòng ngồi, chưa xác minh), `:1269-1275`).
- Thông báo cho TP dùng `tpApproverIdsForDepartment` (pivot **hoặc** cùng phòng) nhưng **gate duyệt không kiểm phòng** (`:1730-1765` vs `:1106`) → Y2/Y6.
- `dueConfig` manager ở cả 3 route duyệt (`F/Routes/api.php:615-617`).
- (d) không chặn người tạo (trừ loại 6 buộc chính người tạo mới duyệt). (e) tuần tự; các cấp 10/11 chỉ cho loại trả lại có quyết toán.
- (g) **Phức tạp**: gate phụ thuộc `status` **và** `type` **và** định danh (người tạo YCXH / người tạo phiếu) — không biểu diễn được bằng cột gate đơn giản cho cấp KT kho.

---

## 10. Phiếu thu / Phiếu chi

### 10.1 Phiếu thu (`bill_incomes`) — 1 cấp

- status 1 Đang tạo → **2 Chờ duyệt** → 3 Đã duyệt / 4 Hủy (`BillIncome.php:63-66`).
- Ai: `finance.phieu_thu.approve` (Thủ quỹ) (`:78`; `BillIncomeAccess::canApprove` `:62-66` = `status==2 && is_treasurer`). **Không kiểm công ty phiếu.** Duyệt ghi sổ cái; kiểm lại `isTreasurer()` và khoá dòng (`BillIncomeApprovalService.php:38-60`), `approved_id = auth()->id()` (`:80`); route không có `checkPermission` (`F/Routes/api.php:448-449`).
- Danh sách: **không có chế độ "chờ tôi duyệt"** (Y5): `applyScope` chỉ theo quyền xem `finance.phieu_thu.view` (tổng công ty / công ty / chỉ phiếu mình lập) (`BillIncomeService.php:61-85`). Thủ quỹ có `approve` mà không có `view` công ty thì **không thấy** phiếu cần duyệt (chi tiết `canView` cũng không mở theo `is_treasurer`, `BillIncomeAccess.php:16-45`).
- (d) Người lập tự duyệt: không chặn. (g) 1 mã nhưng **gate "ai thấy" ≠ gate "ai duyệt"** (thấy theo `view` + phạm vi, duyệt theo `approve`).

### 10.2 Phiếu chi (`bill_payments`) — 1 hoặc 2 cấp

- Cấp: **loại chi ≠ 4**: 2 Chờ chi tiền → 3 Đã duyệt. **Loại chi 4 (Chi thu nhập nhân viên, nhánh B)**: **5 Chờ KT trưởng duyệt** → 2 Chờ chi tiền (chưa ghi sổ) → 3 Đã duyệt (`BillPaymentWriteService.php:355-358`; `BillPaymentApprovalFlowService.php:197-221`).
- Ai: st5 `finance.phieu_chi_ke_toan_truong.approve`, st2 `finance.phieu_chi_thu_quy.approve` + **cùng công ty phiếu** (`BillPaymentAccess::canApprove` `:156-172`, `isSameCompanyAsCurrentEmployee` `:215-225`). Gate đặt trong service **sau khi khoá dòng** (`ApprovalFlowService.php:171-195`: 409 nếu đã duyệt trước, 403 nếu thiếu quyền), không ở controller (`BillPaymentController.php` docblock).
- Người lập: phải là `finance.ke_toan_thanh_toan.manage` (`canEdit` `:119-128`).
- **Nhiều cấp 1 người (nhánh B):** KT trưởng duyệt (5→2, `accounting_approved_id = tôi`, sửa lỗi ERP #8 `:201-207`), sau đó **thủ quỹ duyệt (2→3)**; cùng 1 người có cả 2 mã vẫn phải duyệt 2 lần, không chặn. Người lập loại 4 có thể là kế toán thanh toán + KT trưởng + thủ quỹ → tự duyệt cả 3 chặng.
- Danh sách chờ: `applyScope` `BillPayment.php:337-370` **không có nhánh người duyệt đúng cấp** (Y5) dù `canView` (`BillPaymentAccess.php:55-109`) mở cho thủ quỹ/KT trưởng đúng cấp → bấm thông báo mở được nhưng không thấy trong danh sách nếu thiếu quyền xem.
- (g) status→{mã, cùng công ty}; `type` quyết định phiếu có vào st5 hay không (phụ thuộc dữ liệu, không ảnh hưởng gate vì gate đọc `status`).

---

## 11. Quyết toán thưởng năng suất quý (`bill_productivity_settlement_quarters`)

- **KHÔNG có bước Chờ duyệt** (đã sửa 15/11): `FORM_STATUSES = [1 Đang tạo, 3 Đã hạch toán]` (`BillProductivitySettlementQuarter.php:39`); hằng `STATUS_WAITING_APPROVE = 2` chỉ để hiển thị phiếu cũ. Không đường code nào đặt st2 (grep `STATUS_WAITING_APPROVE` chỉ có ở BonusEndYear).
- "Duyệt" = `canApprove()` = `canEdit() && canCreate()` (`:127-130`): **người lập phiếu Đang tạo + có mã `Tạo/Duyệt quyết toán thưởng năng suất quý`** (`:41`) tự bấm "Lưu và duyệt". → **tự duyệt theo thiết kế**, route `approve` (`BillProductivitySettlementQuarterController.php:165-171`) không gate ở controller (gate trong `writeService->approve`, chưa đọc chi tiết → ghi "chưa xác minh").
- Gate: hợp nhất 1 mã `Tạo/Duyệt`; mã tên cũ qua alias.

---

## 12. Quyết toán thưởng cuối năm (`bonus_end_year_settlements`) — 1 cấp BGĐ

- 1 Đang tạo → **2 Chờ BGĐ duyệt** → 3 Đã duyệt / 4 Không duyệt (`BonusEndYearSettlement.php:87-96`).
- Ai: mã tên cũ `BGĐ duyệt quyết toán thưởng năm` (`:136`; `canApprove` `:259-263` = `status==2` + mã). **Không kiểm công ty** (`created_company_id`), **không kiểm phòng** (chưa chuyển sang mã `phan_he.doi_tuong.hanh_dong`, đang qua alias tên cũ). Controller `approve` kiểm `canApprove()` `:233-239`; nhận `is_approve` (duyệt / không duyệt) + sửa số duyệt từng dòng.
- Danh sách: `scopeVisibleTo` theo 3 quyền xem (công ty/phòng/tổng) (`:~320-345`) **không có nhánh "BGĐ chờ duyệt"** → BGĐ cần quyền xem tương ứng mới thấy phiếu (Y5) dù duyệt được bằng URL.
- (d) Người lập (có mã tạo) tự duyệt nếu cũng giữ mã BGĐ: không chặn.
- (g) 1 mã, không công ty; danh sách khác gate duyệt.

---

## 13. Yêu cầu mua dịch vụ (`buy_service_requests`) — 2 cấp

`F/Entities/BuyServiceRequest/BuyServiceRequest.php`.

| status | Chữ BE | Ai | Gate |
|---|---|---|---|
| 2 Chờ TP duyệt | `sale.yeu_cau_mua_dich_vu_truong_phong.approve` | `canDepartmentApprove` `:294-298`: **chỉ mã, không phòng, không công ty** (docblock `:285-293` "ERP đã comment tắt kiểm phòng — giữ nguyên, user chốt bám ERP") |
| 3 Chờ KS duyệt | `sale.gia_mua_dich_vu_ban_kiem_soat.approve` | `canKsApprove` `:301-307`: mã + **cùng công ty**; ghi giá duyệt từng dòng (`Service:417+`) |
| 5 Không duyệt / 4 Đã duyệt | | |

- TP duyệt luôn → st3 (không rẽ cấp) (`Service:390-407`). Từ chối cả 2 cấp: `reject` `Controller:312-324`. `dueConfig` manager ở `department-approve` (`F/Routes/api.php:2266-2267`).
- Danh sách `for-approve` (`applyWaitingApproveScope` `:473-498`): TP lọc `department_id ∈ K2` ⇒ **hẹp hơn** gate duyệt (Y6); KS lọc công ty khớp gate.
- (d) tự duyệt: không chặn. (e) tuần tự. (g) cấp TP: 1 mã không công ty; cấp KS: mã + công ty.

---

## 14. Điều chuyển kho (`warehouse_transfers`) + các phiếu kho cùng nhóm

### 14.1 Điều chuyển kho

- status 3 Đang tạo → **2 Chờ duyệt** → 1 Đã duyệt (`WarehouseTransfer.php:20-22`). **Chỉ có "Duyệt", không có "Từ chối"** (Route `:727`).
- Ai: **Kế toán kho của KHO NGUỒN** = người có dòng trong `warehouse_accountants (accountant_id = tôi, warehouse_id = from_warehouse_id)` — **không dùng mã quyền** (`WarehouseTransferController.php:392-410, 418-429`); **không kiểm công ty**; thêm: phiếu phải nằm trong `scopedQuery` (quyền xem theo cấp với **tên cũ** `Xem phiếu điều chuyển kho theo …`, hoặc chính mình lập, `:55-64`) ⇒ kế toán kho nhưng không có quyền xem phiếu → **404** dù đúng kho.
- (g) Gate = **định danh (bảng phân công kho)** + điều kiện xem. Không biểu diễn bằng mã quyền.

### 14.2 Đề nghị nhập kho (`warehouse_import_requests`)

- 2 Chờ duyệt (đã gửi thủ kho): **thủ kho của kho nhập** (`warehouse_stockers.stocker_id = tôi` AND `warehouse_id` = kho phiếu) — không mã, không công ty, không loại người lập (`WarehouseImportRequestController.php:1030-1049`; flag FE `WarehouseImportRequestResource.php:~190-200`). Từ chối bắt lý do (`:720-740`). "Duyệt" thực chất là lập Phiếu nhập kho trên ERP (comment `:706-711`).
- Danh sách chờ **khớp gate**: `≠ Đang tạo` và `warehouse_id ∈ kho tôi là thủ kho` (`:53-70`).

### 14.3 Phiếu nhập kho (`warehouse_imports`) — Không duyệt

- 2 Chờ duyệt: `accounting.ke_toan_kho.manage` + **cùng công ty** (`canApprove` `:258-265`, `canDeny` `:267-270` trừ loại `NO_DENY_TYPES`).

### 14.4 Yêu cầu vận chuyển (`delivery_requests`)

- 2 Chờ duyệt: **thủ kho của kho trên YCXH nguồn** (`isCurrentStocker` `:329-345`; `canApprove` `:422-426`). Docblock `:420` nhắc SA nhưng code không có. Bảng rỗng trên DB (tài liệu nền).

### 14.5 Phiếu chuyển hàng nhập thẳng (`product_import_direct_transfers`) / Yêu cầu chuyển hàng (`product_transfer_requests`)

- 2 Chờ duyệt: `accounting.ke_toan_kho.manage` + **cùng công ty** (`ProductImportDirectTransfer.php:194-205`; `ProductTransferRequest.php:241-253`). Route `approve/reject` của cả 2 chỉ kiểm `canApprove()` (`ProductImportDirectTransferController.php:161, 179`; `ProductTransferRequestController.php:214`).

### 14.6 Yêu cầu xuất mượn (`borrow_export_requests`)

- 2 Chờ duyệt: `accounting.ke_toan_kho.manage` — **không công ty** (`canApprove` `:256-259`); `reject` kiểm `canApprove()` → 423 (`BorrowExportRequestController.php:132-141`).

### 14.7 YC xuất hàng — YCXH (`product_export_requests`, Assign) vượt hạn mức công nợ

- 10 Đợi TP duyệt: `finance.xuat_hang_vuot_han_muc_cong_no_truong_phong.approve` (middleware `switch-board-of-manager` `A/Routes/api.php:797-798`) + **phòng phiếu ∈ pivot K1 (`:423-441`)**; loại mượn (3) bị loại khỏi luồng này. TP **chỉ chuyển BGĐ** (10→11), không duyệt thẳng (`Controller:1648-1686`).
- 11 Đợi BGĐ duyệt: `finance.xuat_hang_vuot_han_muc_cong_no_ban_giam_doc.approve` (middleware `manager-approve` `:799-800`) + cùng công ty (`:445-458`); → 2.
- 2 Chờ duyệt: **không duyệt** (reject) bởi `accounting.ke_toan_kho.manage` + cùng công ty (loại 7 theo `export_company_id`) (`canReject` `:370-398`); "Duyệt" = lập Đề nghị xuất kho.
- `canReject` còn mở cho TP/BGĐ đúng cấp (`:371-373`).

---

## 15. Kiểm kê + Biên bản xử lý thừa thiếu

### 15.1 Phiếu kiểm kê theo hàng hoá (`self_inventories`)

- 3 Đang tạo / 1 Đang kiểm / **2 Chờ KT duyệt** / 4 Chờ xử lý / 5 Đang xử lý / 6 Hoàn thành / 7 Không duyệt (`SelfInventory.php:35-41`).
- Duyệt/không duyệt kết quả: `canApprove` = st2 + mã **`warehouse.ket_qua_kiem_ke.approve`** (BKS) (`:227-231`); **không công ty** (docblock `:146-152` "không bó công ty — như ERP"). Xử lý (st4/5): `warehouse.phieu_kiem_ke_hang_hoa.update` (`:233-237`). Duyệt/reject: `WriteService` `lockOrConflict($obj,'canApprove')` (`:839, 870`).
- Danh sách `type=wait-approve` (`scopedQuery` `:157-190`): BKS thấy **mọi** phiếu st2 mọi công ty; menu `FE/.../finance.js:359-361`.

### 15.2 Kết quả kiểm kê theo vị trí (`position_inventories`, type 1)

- 2 Chờ duyệt → mã `warehouse.ket_qua_kiem_ke.approve` (`PositionInventoryResult.php:227-231`), **không công ty**; xử lý (st4) `warehouse.phieu_kiem_ke_vi_tri.update`. `WriteService:462, 497`.
- Danh sách `scopedQuery` (`:164-190`) **không có nhánh BKS chờ duyệt** (Y5) nhưng `canView` có (`:193-205`) → vào được từ thông báo, không thấy trong danh sách trừ khi có quyền xem.

### 15.3 Biên bản xử lý thừa thiếu sau kiểm kê (`inventory_audit_reports`)

- 1 Chờ duyệt → 2 Đã duyệt (`InventoryAuditReport.php:35-36`). Duyệt: mã `warehouse.bien_ban_xu_ly_hang_thua_thieu_sau_kiem_ke.approve` (`canApproveAny` `:129-132`, `canApprove` `:~190-195`) — **không công ty**. Danh sách có nhánh "người duyệt thấy mọi biên bản Chờ duyệt" (`scopedQuery` `:141-165`) → **danh sách khớp gate** (cả 2 không bó công ty). Người tạo: `accounting.ke_toan_kho.manage` (`PERMISSION_CREATE` `:51`); tự duyệt: không chặn.

- (d) tự duyệt (cả 3): không chặn. (e) 1 cấp. (g) 1 mã không công ty ⇒ biểu diễn được bằng 1 cột gate; lưu ý "mọi công ty".

---

## 16. Chỉ tiêu kinh doanh (phòng ban / nhân viên)

Trait `F/Entities/BusinessTarget/Concerns/HasBusinessTargetAccess.php`; 2 entity: `BusinessTargetCompany` (màn **phòng ban**, mã `sale.chi_tieu_kinh_doanh_phong_ban.approve` `BusinessTargetCompany.php:40`) và `BusinessTargetForDepartment` (màn **nhân viên**, mã `sale.chi_tieu_kinh_doanh_nhan_vien.approve` `BusinessTargetForDepartment.php:38`). Xem chung `sale.chi_tieu_kinh_doanh.view`.

- 1 Đang tạo → **2 Chờ duyệt (`STATUS_PENDING`)** → 3 Đã duyệt / 5 Huỷ; từ chối → về Đang tạo (reason bắt buộc).
- Ai duyệt: `canApprove()` = `status==2 && hasApprovePermission() && cùng công ty phiếu` (`:127-140`; `canActAsApprover` `:112-115`). Route gắn **thêm** `checkPermission` cùng mã (`F/Routes/api.php:1810-1811, 1824-1830`, tức 2 lớp: middleware + entity). Cả `un-approve` (Huỷ duyệt, st3 → …) cùng gate `canUnApprove()`.
- Danh sách chờ: `?type=for-approve` → `applyForApproveScope` = st2 + công ty tôi + có mã (`:79-91`); `applyViewScope` thêm nhánh "người duyệt thấy phiếu st2 cùng công ty" (`:47-77`) → **khớp gate**. Menu `sale-hub.js:363-364` gate bằng `codes` của mã duyệt.
- (d) Người lập tự duyệt: **không chặn** (`canApprove` không xét `created_by`; người lập cần mã `create`, người duyệt mã `approve`, có thể cùng 1 người).
- (e) 1 cấp. (f) không `dueConfig`.
- (g) 1 mã + công ty phiếu + status → 1 cột gate đủ.

---

## 17. Phân chia thị trường

### 17.1 Theo phòng ban (`division_market_departments`)

- Chỉ **2 trạng thái**: 1 Đang tạo → 2 Đã duyệt (**không có Chờ duyệt**) (`DivisionMarketDepartment.php:31-32`). "Duyệt" = người có mã (`Duyệt phiếu phân chia thị trường theo phòng ban`, tên cũ `:41`) bấm trên phiếu chưa duyệt: `canApprove` = `!isApproved() && mã` (`:182-185`) — **không công ty, không trạng thái chờ**. Middleware `checkPermission` cùng mã (`F/Routes/api.php:1757-1758`). → không có "phiếu chờ duyệt" để gom theo trạng thái; chỉ có "phiếu chưa duyệt".

### 17.2 Theo nhân viên (`division_market_department_employees`)

- 1 Đang tạo → **3 Chờ duyệt** → 2 Đã duyệt; từ chối → về Đang tạo; thu hồi/huỷ duyệt (`DivisionMarketDepartmentEmployee.php:31-33, 235-248`).
- Ai: mã tên cũ `Duyệt phiếu phân chia thị trường theo nhân viên` **và cùng công ty phiếu** (`allowed()` `:203-210`). Middleware cùng mã (`F/Routes/api.php:1782-1785`).
- Danh sách: `applyViewScope` có nhánh người duyệt thấy phiếu st3 cùng công ty (`:152-182`) → khớp gate.
- (d) tự duyệt: không chặn. (g) 17.2: 1 mã + công ty + status; 17.1: không có trạng thái chờ → **không đưa vào bảng gom được** (hoặc phải quy ước "status = Đang tạo" là chờ — chưa có chốt nghiệp vụ).

---

## 18. Kế hoạch bán hàng / phát triển thị trường NV (phát hiện thêm, `EmployeePlan`)

`F/Entities/EmployeePlan/EmployeePlan.php`; mã `sale.ke_hoach_ban_hang_nhan_vien.approve` / `sale.ke_hoach_phat_trien_thi_truong_nhan_vien.approve` (`SaleEmployeePlan.php:15`, `MarketEmployeePlan.php:15`).

| status | Chữ BE | Ai | Gate |
|---|---|---|---|
| 2 Chờ TP duyệt | mã duyệt NV **và** (phòng phiếu ∈ pivot **hoặc** = phòng mình ngồi) **và KHÔNG là người lập** (`canApprove` `:322-325`, `isHeadOfPlan` `:280-283`, `approvableDepartmentIds` `:198-209`) | duy nhất luồng cấm tự duyệt |
| 3 TP đã duyệt | cùng người đó "Gửi BGĐ" (`canSendDirector` `:332-335`) → 4 | |
| 4 Chờ BGĐ duyệt | **HRM không có bước BGĐ duyệt** — "chưa có màn BGĐ duyệt" (`Service:526-527` docblock) | chưa xác minh phía ERP |
| 5 BGĐ đã duyệt | | |

- Người lập là TP của phòng phiếu: **gửi duyệt đi thẳng st4 (nhảy cấp)** (`EmployeePlanService.php:484-486`).
- `form_version=1` (phiếu ERP) HRM chỉ xem (`canApprove` đòi `isHrmForm()`).
- (g) gate = mã + (quản lý-hoặc-cùng-phòng) + **KHÔNG phải người lập**; cần cột "loại trừ người lập" mới đủ.

---

## 19. Phiếu thu/chi, nhập/xuất kho cần bước duyệt khác (đã rà)

| Loại | Kết quả |
|---|---|
| Phiếu báo có (`bill_income_reports`) | tài liệu nền: duyệt từ "Đang tạo", quyền `Quản lý phiếu báo có` — **chưa đọc lại code trong phiên này** (chưa xác minh) |
| Ủy nhiệm chi (`bill_payment_authorizations`) | `BillPaymentAuthorizationDetailResource.php:22` ghi rõ "KHÔNG có `is_can_approve`" — không có bước duyệt |
| Hạch toán mua dịch vụ (YC) | 2 Chờ duyệt: mã `sale.hach_toan_mua_dich_vu.create` + cùng công ty, 2 lớp (middleware reject + `canAccounting`) (`BuyServiceAccountingRequest.php:303-308`; `Routes:2301`) |
| Xuất bán hàng mượn thực tế (PXBHM) / phiếu xuất giữ / phiếu huỷ giữ | là **bước lập chứng từ** của KT kho (`BorrowSell::userCanCreate` mã `accounting.ke_toan_kho.manage`), không phải "chờ duyệt" riêng |

---

## 20. ĐÁNH GIÁ TỔNG HỢP CHO BẢNG GOM — Definition phải khai những gì

### 20.1 Các kiểu gate thực tế đã gặp

| Kiểu | Mô tả | Loại phiếu |
|---|---|---|
| **G1** | mã quyền + công ty phiếu = công ty tôi (theo status) | Đề nghị thanh toán (cấp 3-6), Phiếu chi, Gia hạn hàng giữ/xuất giữ/điều chuyển (BGĐ, KT), Gia hạn hàng mượn (BGĐ, KT), Mua dịch vụ (KS), Hạch toán mua DV, Chuyển hàng nhập thẳng, Yêu cầu chuyển hàng, Phiếu nhập kho, Điều chỉnh công nợ, Hạch toán bổ sung (1–6), Chỉ tiêu KD, PCTT theo NV, YCXH (BGĐ + reject KT) |
| **G2** | mã quyền, **không** kiểm công ty | Phiếu thu, Không duyệt đề nghị thu, Yêu cầu nhập hàng (4 cấp), Mua DV (TP), Huỷ giữ, Xuất mượn, Kiểm kê (2 loại), Biên bản thừa thiếu, Quyết toán thưởng năm, PCTT phòng ban, Xuất bán hàng mượn (TP, BGĐ, KT), Duyệt giá bán (công ty theo bộ giá) |
| **G3** | mã quyền + "quản lý phòng của phiếu" | Đề nghị thanh toán TP (K1); Gia hạn/Xuất giữ/Điều chuyển TP (K2; điều chuyển theo phòng người **nhận**); Gia hạn hàng mượn TP (K3); Xuất bán hàng mượn TP (K4); YCXH TP (K1); Kế hoạch NV (K2 + loại người lập) |
| **G4** | định danh theo bảng phân công kho, không dùng mã | Đề nghị nhập kho (thủ kho), Yêu cầu vận chuyển (thủ kho của kho YCXH), Điều chuyển kho (KT kho nguồn) |
| **G5** | hỗn hợp/AND-OR/định danh người tạo | Hạch toán bổ sung loại 7 (2 mã + công ty qua bảng con); Yêu cầu nhập hàng KT kho (mã **hoặc** người tạo YCXH nguồn; loại 6 chỉ người tạo); Kế hoạch NV (loại người lập; nhảy cấp theo người lập); Xuất bán hàng mượn `waiting_approve` (KT kho không kiểm mã) |

### 20.2 Cột gate đơn giản có đủ không?

**Không đủ nếu chỉ 1 cột mã.** Tối thiểu mỗi định nghĩa phải khai **một danh sách theo status**, mỗi phần tử:
`{ status, code (mã quyền, có thể >1 OR), company_check (none | doc.company = current), manager_check (none | doc.department ∈ K1 | K2 | K3 | K4 | to_employee.department), exclude_creator (bool), identity_check (none | warehouse_stockers | warehouse_accountants | creator | source_creator) }`.

Trường hợp **không biểu diễn được bằng cấu hình thuần** (phải gọi hàm entity / `canXxx()` từng dòng):
1. Hạch toán bổ sung loại 7 (2 mã khác nhau cho 2 hành động, phạm vi công ty lấy từ bảng con phòng hỗ trợ).
2. Yêu cầu nhập hàng cấp KT kho (OR người tạo YCXH nguồn, ràng buộc người tạo loại 6, `is_import_direct`).
3. Điều chuyển kho: phụ thuộc cả `warehouse_accountants` lẫn phạm vi xem tên cũ.
4. Điều chuyển hàng giữ: phòng đích lấy từ NV nhận (quan hệ `to_employee.info.department_id`).
5. Kế hoạch NV: loại người lập + nhảy cấp theo `creatorIsHead()`.
6. Phiếu chi: rẽ có/không st5 theo `type` (không ảnh hưởng gate đọc theo status nhưng ảnh hưởng "đường đi").

Khuyến nghị cho thiết kế bảng gom (đối chiếu `design.md`): **bước lọc thô bằng SQL** (`status ∈ …`, `company_id`, nhóm theo mã) + **bước lọc chính xác bằng chính hàm `canXxx()` của entity trên trang hiện tại** (đã có sẵn và đã được FE tin dùng). Đừng tái cài logic quyền vào Definition mới vì (a) có ≥4 biến thể "quản lý", (b) gate duyệt ≠ gate danh sách ở ≥8 luồng (Y4–Y7), (c) cờ `all_department` bị xử lý không đồng đều (Y9).

### 20.3 Người nhận thông báo ≠ người duyệt được

Thông báo "có việc cần duyệt" tính bằng `employeeInfoIdsHavingPermission(mã, công ty phiếu)` (ví dụ `BillPaymentRequestNotifyService.php:149-165`), **không lọc theo quản lý phòng**, trong khi cấp TP chỉ duyệt được khi quản lý phòng. Ngược lại `tpApproverIdsForDepartment` (`ProductImportRequest.php:1730-1765`) lọc theo phòng nhưng gate duyệt không lọc. Bảng gom không nên dùng danh sách người nhận thông báo làm nguồn gate.

---

## 21. Mục "chưa xác minh" / cần hỏi nghiệp vụ

1. `current_company_role` vs `info->company_id` lệch nhau cho ai (dữ liệu thật) — ảnh hưởng mọi so sánh công ty (mục 0 đầu trang).
2. Bước duyệt trong `BillProductivitySettlementQuarterWriteService::approve` (gate thật) — chưa đọc.
3. Phiếu báo có (`bill_income_reports`) — chưa đọc lại code.
4. Quyết toán thưởng năm, PCTT, Điều chuyển kho, Quyết toán quý còn dùng **tên quyền cũ** (không phải mã) — qua alias; cần xác nhận alias đã đủ ở prod (`permission_aliases`).
5. Kế hoạch NV: bước BGĐ duyệt ở ERP (HRM chỉ gửi BGĐ) — chưa xác minh phía ERP.
6. Xuất bán hàng mượn `?type=waiting_approve` còn lộ phiếu KT kho cho mọi người cùng công ty (Y4) — cần user chốt có sửa không.
7. PCTT phòng ban (17.1): không có trạng thái "chờ duyệt" — có đưa vào bảng gom không (nghiệp vụ).
8. Có cần chặn người lập tự duyệt ở Đề nghị thanh toán / Phiếu thu-chi / Hàng giữ không (hiện KHÔNG chặn ở bất kỳ luồng nào trừ Kế hoạch NV) — **câu hỏi nghiệp vụ cần chốt**.
