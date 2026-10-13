# Chuyển giao khách hàng (YCCGKH) — Phase 1 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) hoặc superpowers:executing-plans để thực thi từng task. Steps dùng checkbox `- [x]`.

**Goal:** Xây module phiếu YCCGKH (7 màn) cho phép chuyển KH của HĐ (Vật tư/Dự án/Dịch vụ) từ KH cũ → KH mới; khi duyệt ghi đè snapshot KH trên chính HĐ, hủy duyệt revert.

**Architecture:** 1 bảng phiếu polymorphic (`contractable_id/type` = FirmContract|WrServiceContract) + snapshot JSON `old_customer_data`/`new_customer_data`. Mirror module mẫu **`bill_adjust_dept_requests`** (controller+model+views). Service `CustomerHandoverService::applyToContract/revertContract` map snapshot → cột KH trên HĐ. Không lan 13 luồng (Phase sau).

**Tech Stack:** Laravel 6, PHP 7.4, MySQL; Blade + AngularJS 1.3.9 (`<% %>`); Yajra DataTables server-side; ResponseTrait; bảng `files` chung; permission qua `PermissionsTableSeeder`.

## Global Constraints
- KHÔNG commit/push khi user chưa yêu cầu.
- KHÔNG có test tự động → verify mỗi task bằng `php -l` (BE) + **test browser trên dev**.
- KHÔNG đọc/sửa `vendor/`, `node_modules/`.
- Form validate: BE rethrow `ValidationException` (không catch chung); FE inline `is-invalid` + `invalid-feedback`.
- Loại HĐ: FirmContract `HOP_DONG(1)`/`HOP_DONG_DU_AN(4)` + WrServiceContract; loại trừ nguyên tắc (7/8).
- Mã phiếu: `TPE.YCCGKH.mmyy.NNNNN` (mã cty + YCCGKH + mmyy + 5 số tịnh tiến), sinh khi gửi duyệt.
- Trạng thái: 1 Đang tạo, 2 Chờ duyệt, 3 Đã duyệt, 4 Không duyệt, 5 Hủy duyệt.
- Mirror pattern: đọc `app/Http/Controllers/IncomeExpenditure/BillAdjustDeptRequestController.php`, `app/Model/IncomeExpenditure/BillAdjustDeptRequest.php`, `resources/views/income_expenditure/bill_adjust_dept_requests/*` trước khi viết phần tương ứng.

---

## File Structure
- Create migration: `..._create_customer_handover_requests_table.php`, `..._create_customer_handover_request_histories_table.php`.
- Create `app/Model/Sale/CustomerHandoverRequest.php`, `app/Model/Sale/CustomerHandoverRequestHistory.php`.
- Create `app/Services/Sale/CustomerHandoverService.php`.
- Create `app/Http/Requests/CustomerHandoverStoreRequest.php`.
- Create `app/Http/Controllers/Sale/CustomerHandoverRequestController.php`.
- Create `app/ExcelExports/CustomerHandoverRequestExport.php`.
- Create views `resources/views/sale/customer_handover_requests/` (index, approved, create, edit, show, form, formJs, formShow, approve, partials/).
- Modify `routes/web.php`, `database/seeds/PermissionsTableSeeder.php`.
- Modify `app/Model/Sale/Firm/Contract/FirmContract.php`, `app/Model/Customers/WrServiceContract.php` (accessor `can_handover` + relation `handover_request`).
- Modify `resources/views/sale/firm/contracts/index.blade.php`, `.../show.blade.php` (+ WrServiceContract views) — action + lịch sử.
- Modify `app/Http/Controllers/HomeController.php` + dashboard blade — box đếm chờ duyệt.
- Modify sidebar menu blade — mục Đơn hàng hợp đồng + Chờ duyệt.

---

### Task 1: DB + Model + generateCode
**Files:** 2 migration; `app/Model/Sale/CustomerHandoverRequest.php`, `CustomerHandoverRequestHistory.php`.
**Produces:** STATUS const `DANG_TAO=1,CHO_DUYET=2,DA_DUYET=3,KHONG_DUYET=4,HUY_DUYET=5` + STATUSES[]; `generateCode():string`; relations `contractable(morphTo)`, `histories`, `files`, `creator/approver/old_customer/new_customer`; cast json→array.

- [x] Step 1: Migration bảng chính (cột theo design-phase1.md §2.1).
- [x] Step 2: Migration histories (`customer_handover_request_id, created_by, action, content, created_at`).
- [x] Step 3: Model chính — fillable/casts/const/relations + `generateCode()` (mirror `BillAdjustDeptRequest::generateCode()` L1068 + `ClosingEntry::generateCode()` L139; prefix mã cty + `.YCCGKH.` + mmyy + 5 số max+1 trong tháng).
- [x] Step 4: Model history — fillable + `creator`.
- [x] Step 5: `php -l` 2 model + `grep DB_ .env` (xác nhận dev) + `php artisan migrate`.
- [x] Step 6: Verify tinker — tạo record, `generateCode()` ra `TPE.YCCGKH.0726.00001`.

---

### Task 2: Permission + Route + Menu
**Files:** `database/seeds/PermissionsTableSeeder.php`, `routes/web.php`, sidebar menu.
**Produces:** 5 quyền: `Xem danh sách phiếu chuyển giao khách hàng theo tổng công ty|công ty|phòng ban|bộ phận`, `Duyệt phiếu YC chuyển giao khách hàng`. Route name prefix `customerHandover.*`.

- [x] Step 1: Seed 5 quyền (mirror block trong PermissionsTableSeeder) → `php artisan db:seed --class=PermissionsTableSeeder`.
- [x] Step 2: Routes `Route::prefix('sale/customer-handover-requests')`: index, all, searchData, searchDataApprove, create, store, edit, update, show, approve, reject, cancelApprove, export, searchContract, searchCustomer, searchContact; `checkPermission` cho store/approve/reject/cancelApprove/export.
- [x] Step 3: Menu Kinh doanh → Đơn hàng hợp đồng + nhánh Chờ duyệt (hiện theo quyền).
- [x] Step 4: Verify `php artisan route:list | grep customer-handover` + menu hiện.

---

### Task 3: Tiền điều kiện + action trên HĐ + lịch sử  ⚠️ CHẶN: chốt model "đề nghị xuất hóa đơn" trước
**Files:** `FirmContract.php`, `WrServiceContract.php`; `sale/firm/contracts/index.blade.php`, `show.blade.php` (+ WrServiceContract views).
**Produces:** `getCanHandoverAttribute():bool`, `handover_request()` hasOne.

- [x] Step 0 (CHẶN): grep tìm model "đề nghị xuất hóa đơn" của HĐ (`billable`/`invoice request`); nếu không rõ → **hỏi user** trước khi code accessor.
- [x] Step 1: accessor `can_handover` — type ∈{1,4}/WrServiceContract, status Có hiệu lực, `created_by==auth id`, **chưa có** đề nghị xuất HĐ, **chưa có** `handover_request`, loại trừ nguyên tắc.
- [x] Step 2: action "Chuyển giao khách hàng" ở DS HĐ theo `can_handover` → link `customerHandover.create?contractable_id=&contractable_type=`; TH đã có đề nghị xuất HĐ → msg vàng.
- [x] Step 3: khu "Lịch sử duyệt" dưới màn view HĐ (từ `handover_request.histories`); ẩn action khi đã Đã duyệt.
- [x] Step 4: `php -l` + Verify browser (đủ điều kiện thấy action; nguyên tắc/đã có ĐNXHĐ/không phải người tạo → không).

---

### Task 4: Controller + List (index + searchData + phân quyền)
**Files:** `CustomerHandoverRequestController.php`; `index.blade.php`.
**Produces:** `searchData(Request)` Yajra; `applyPermissionScope($query)`.

- [x] Step 1: Controller skeleton (`use ResponseTrait`; index/all/searchData/searchDataApprove) — mirror BillAdjustDeptRequestController.
- [x] Step 2: `searchData` — `DataTables::of(query->with([contractable,creator,approver,old_customer,new_customer]))`; editColumn code(link)/KH mới/KH cũ/số HĐ(link)/người-ngày/status(badge)/action(theo status+quyền); rawColumns; áp bộ lọc + `applyPermissionScope`.
- [x] Step 3: `applyPermissionScope` — phân cấp theo 4 quyền (mirror `filterAcc`/`searchByFilter` module phân cấp + `EmployeeManageDepartment`); không quyền → `where created_by=auth id`.
- [x] Step 4: index.blade — DataTable khung chuẩn (mirror bill_adjust_dept_requests/index.blade): bộ lọc, cột, phân trang, nút Tạo mới + Xuất excel; `initSearchColumn`/`mergeSearch`.
- [x] Step 5: `php -l` + Verify browser (DS + lọc + phân quyền).

---

### Task 5: Tạo mới + Store (2 tab, popup, file, code gen)
**Files:** `CustomerHandoverStoreRequest.php`; views `create/form/formJs/partials(search_contract/customer/contact)`; controller `create/store/searchContract/searchCustomer/searchContact`.
**Produces:** `store` tạo phiếu; snapshot `old_customer_data` từ HĐ, `new_customer_data` từ input.

- [x] Step 1: FormRequest — rules (contractable required+exists; new customer_id required+exists; reason required; field bắt buộc theo case DN/CN; file ≥1 ≤60MB); messages inline; `failedValidation` JSON (BaseRequest); rethrow ValidationException.
- [x] Step 2: `create()` — 2 nguồn: (a) từ action HĐ (query contractable) prefill; (b) tạo mới → popup tìm HĐ; truyền HĐ + snapshot KH cũ + DS đại diện/địa chỉ/TK/liên hệ/hãng.
- [x] Step 3: `store()` — validate; build old/new customer_data; lưu files (bảng `files`); nút "Lưu&gửi" → Chờ duyệt + `generateCode()` + log; "Lưu" → Đang tạo; `responseSuccess`.
- [x] Step 4: form 2 tab + formJs — Tab thay đổi (Số HĐ, Lý do; KH trước readonly | KH sau: popup KH + đại diện + địa chỉ giao/sửa + TK NH + liên hệ + hãng; 4 case DN/CN; 2 template HĐ bán & HĐDV; file bắt buộc; validate inline) + Tab Thông tin HĐ + mẫu in. Mirror popup báo giá + logic mới (KH cá nhân show sẵn).
- [x] Step 5: popup searchContract/searchCustomer/searchContact (mirror báo giá; searchContract chỉ HĐ đủ tiền điều kiện).
- [x] Step 6: `php -l` + Verify browser (Lưu→Đang tạo; Lưu&gửi→Chờ duyệt+code; validate; file>60MB; KH ngoài thị trường chặn).

---

### Task 6: Sửa + Update
**Files:** `edit.blade.php`; controller `edit/update`.
- [x] Step 1: `edit()` — chỉ Đang tạo & người tạo; prefill.
- [x] Step 2: `update()` — như store; giữ/đổi status; Lưu&gửi → Chờ duyệt + code + log.
- [x] Step 3: `php -l` + Verify browser (sửa Đang tạo OK; ≥Chờ duyệt không cho sửa).

---

### Task 7: Service apply/revert + Duyệt/Không duyệt/Hủy duyệt
**Files:** `CustomerHandoverService.php`; controller `approve/reject/cancelApprove`; `approve.blade.php`.
**Produces:** `applyToContract($req)`, `revertContract($req)`, `snapshotContractCustomer($contractable):array`, `log($req,$action,$content)`.

- [x] Step 1: `snapshotContractCustomer` — đọc cụm cột KH của HĐ (FirmContract vs WrServiceContract) → array chuẩn (§2.2).
- [x] Step 2: `applyToContract` — map `new_customer_data` → cột KH trên HĐ theo loại (§5); transaction; save.
- [x] Step 3: `revertContract` — map `old_customer_data` → cột KH trên HĐ.
- [x] Step 4: `approve()` — quyền Duyệt + phạm vi; chỉ Chờ duyệt; applyToContract + Đã duyệt + approved_by/at + log. Rethrow ValidationException.
- [x] Step 5: `reject()` — `reject_reason` bắt buộc → Không duyệt + log; không đổi HĐ.
- [x] Step 6: `cancelApprove()` — chỉ Đã duyệt + quyền; guard (HĐ chưa có ĐNXHĐ sau chuyển giao) → revertContract + Hủy duyệt + log; fail → responseErrors.
- [x] Step 7: approve.blade — 2 cột KH trước/sau + nút Duyệt / Không duyệt (popup lý do).
- [x] Step 8: `php -l` + Verify browser (duyệt→HĐ đổi KH mới; không duyệt→giữ; hủy duyệt→về KH cũ; guard chặn).

---

### Task 8: Xem chi tiết + lịch sử duyệt
**Files:** `show.blade.php`, `formShow.blade.php`; controller `show`.
- [x] Step 1: `show()` — load phiếu + files + histories + contractable.
- [x] Step 2: show.blade — readonly theo case, tải file, bảng lịch sử duyệt.
- [x] Step 3: Verify browser (chi tiết đúng trạng thái; tải file; lịch sử đủ mốc).

---

### Task 9: DS chờ duyệt + Dashboard box
**Files:** `approved.blade.php`; `HomeController` + dashboard blade.
- [x] Step 1: `all()` + `searchDataApprove` — DS status Chờ duyệt (menu Chờ duyệt) + cột action Duyệt.
- [x] Step 2: Dashboard box — `HomeController::approveList()` thêm ô đếm status Chờ duyệt (group Quản lý hợp đồng, đơn hàng), link `customerHandover.all`; hiện theo quyền Duyệt (mirror box dashboard khác).
- [x] Step 3: `php -l` + Verify browser (box đúng số + quyền + link).

---

### Task 10: Xuất Excel
**Files:** `app/ExcelExports/CustomerHandoverRequestExport.php`; controller `export`.
- [x] Step 1: Export class (maatwebsite) — tên màn + ngày xuất + cột như DS phiếu; nhận điều kiện lọc.
- [x] Step 2: `export()` — cùng bộ lọc + `applyPermissionScope`, trả file.
- [x] Step 3: `php -l` + Verify browser (xuất đúng theo lọc).

---

## Self-Review
**1. Spec coverage:** §2 DB→T1; §3 luồng→T5/6/7; §4 tiền điều kiện+action→T3; §5 apply/revert→T7; §6 BE→T4-10; §7 FE 7 màn→T4/5/6/7/8/9/10; §8 phân quyền→T2+applyPermissionScope(T4); §9 edge cases→T3/5/7. Gap đã flag: model "đề nghị xuất hóa đơn" (T3 Step0 — câu hỏi chặn).
**2. Placeholder scan:** không TBD trong bước code; các bước "mirror module" chỉ file cụ thể. Điểm mở duy nhất đã đánh dấu chặn T3.
**3. Type consistency:** STATUS const (T1) dùng nhất quán T5/6/7/9; `applyToContract/revertContract/snapshotContractCustomer` (T7) khớp `old/new_customer_data` (T1 cast array); `can_handover`/`handover_request` (T3) dùng ở T4/HĐ view.

## Lưu ý thực thi
- Verify không dùng unit test — mỗi task kết bằng `php -l` (BE) + checklist test browser dev.
- Thứ tự: T1→2→3 (nền) rồi 4→10.
- **Chặn T3**: chốt model "đề nghị xuất hóa đơn" trước khi code accessor.
- Tạo branch riêng khi bắt đầu code (hỏi tên nhánh).

---
## Checkpoint — 2026-07-03 (dừng cuối ngày, subagent-driven, nhánh task_10696)
Vừa hoàn thành:
- Task 1 (DB+Model): ✅ DONE + review clean. Commits `61a2ead..446827c`.
- Task 2 (Permission+Route+Menu): commit `2e543d2`; review 1 CRITICAL (id 1037 trùng) → fix subagent đang đổi id→1042-1046.
Đang làm dở: fix Task 2 (đổi id permission) — mai xác nhận commit fix + dev có 5 perm id 1042-1046.
Bước tiếp theo:
1. Xác nhận Task 2 fix xong → review lại nhanh → Task 2 DONE.
2. Task 4 (Controller+List) — làm ngay, độc lập Task 3.
3. **Task 3 chờ user**: model "đề nghị xuất hóa đơn" của HĐ bán (tiền điều kiện can_handover + guard hủy duyệt).
4. Sau đó Task 5→10.
Blocked: Task 3 (chờ user trả lời "đề nghị xuất hóa đơn" là màn/bảng nào).
Ledger chi tiết: `TanPhatDev/.superpowers/sdd/progress.md`.

---
## Checkpoint — 2026-07-04 (TẠM DỪNG theo yêu cầu user)
Nhánh `task_10696`, HEAD `17577e9`.
Đã xong: Task 1 (DB+Model), 2 (Perm/Route/Menu), 3 (action `can_handover`+lịch sử trên HĐ), 4 (List+phân quyền cấp), 5a (BE tạo/lưu).
Đang dở: Task 5b (FE form 2 tab + popups) — agent chạy nền lúc pause; khi resume kiểm `git log` xem commit 5b đã có chưa (xem `.superpowers/sdd/task-5b-report.md`).
Còn lại: Task 6 (Sửa+Update), 7 (Duyệt/Không duyệt/Hủy duyệt + Service apply/revert **áp cả phụ lục PLG/PLBS**), 8 (Chi tiết+lịch sử), 9 (Dashboard+DS chờ duyệt), 10 (Export).
Blocked/chờ user: (a) file bắt buộc cả khi lưu nháp — nới không? (b) WrServiceContract giới hạn type action? (c) wire placeholder `hasInvoiceExportRequest` khi merge nhánh "đề nghị xuất hóa đơn".
Chi tiết resume: `TanPhatDev/.superpowers/sdd/progress.md` (PAUSE CHECKPOINT).

---
## Checkpoint — 2026-07-04 (PHASE 1 HOÀN TẤT — subagent-driven)
Nhánh `task_10696`, range `61a2ead..20ba036` (19 commit), CHƯA push.
Vừa hoàn thành: TẤT CẢ 10 task (1→10) + final whole-branch review (opus, KHÔNG Critical) + fix commit `20ba036` (Excel trạng thái, menu chờ duyệt→customerHandover.all, xóa dead approve.blade, validate delivery_place_id/deputy_id).
Đang làm dở: (không) — chờ user test browser toàn luồng.
Bước tiếp theo:
1. USER test browser toàn luồng (tạo từ action HĐ & DS, 4 case DN/CN, popup HĐ/KH/liên hệ, file, lưu nháp/gửi, duyệt/không duyệt/hủy duyệt, chi tiết, dashboard, export).
2. Wire `hasInvoiceExportRequest()` (hiện placeholder=false) khi merge nhánh "đề nghị xuất hóa đơn".
3. Fix E (defer): chặn "KH không thuộc thị trường được phân công" — cần BA xác nhận rule (tham khảo marketDivisionContract() trong FirmQuotationService).
4. Merge/push khi user duyệt.
Blocked: (không, chỉ chờ user test + quyết định merge)
Ledger: `TanPhatDev/.superpowers/sdd/progress.md`.

---
### Task 11 (Fix E — final review): Chặn "KH không thuộc thị trường được phân công"
**Files:** `app/Services/Sale/CustomerHandoverService.php` (thêm `assertNewCustomerInMarket`); `app/Http/Controllers/Sale/CustomerHandoverRequestController.php` (gọi trong store/update khi gửi duyệt).
**Quyết định user (khuyến nghị):** 1a đầy đủ như báo giá (ward+hãng+bypass nhóm KH/phòng ban+Config+Super Admin bỏ qua) | 2a chỉ khi "Lưu & gửi duyệt" | 3a HĐ hãng theo is_equipment(type1)/is_project(type4), HĐ dịch vụ bỏ qua.
- [x] Step 1: `assertNewCustomerInMarket($contractable,$newCustomerId)` — chỉ FirmContract; Super Admin/phòng ban bypass/Config tắt → return; tái dùng `FirmQuotationService::marketDivisionContract` + `marketDivisionCustomerContract` qua object mock (ward=customer.ward_id); fail → throw ValidationException key new_customer_id.
- [x] Step 2: gọi trong store() + update() khi `$isSend`.
- [x] Step 3: `php -l` + verify.

---

## Fix sau test browser (2026-07-06)

### FixT1 — Vỡ popup "Tìm khách hàng mới" (form tạo)
Root cause: `searchCustomerModal.blade.php` dùng class `modal-xl` — Bootstrap 4 của dự án KHÔNG hỗ trợ (0 CSS định nghĩa; convention dự án là `modal-content-large` (63 file) / `modal-lg`). → modal rớt về width mặc định ~500px → bảng 5 cột (địa chỉ dài) tràn + bị cắt.
- [x] `modal-xl` → `modal-lg` (đồng bộ với sibling `searchContractModal`).
- [x] Cột "Loại" hiện số → thêm `addColumn('customer_type_text')` (accessor `Customer::getCustomerTypeTextAttribute`) ở `searchCustomer()`; FE column đổi `customer_type` → `customer_type_text`.
- [ ] User reload trang tạo (Ctrl+F5) → mở lại popup xác nhận hết vỡ + cột Loại ra chữ.
Files: `resources/views/sale/customer_handover_requests/partials/searchCustomerModal.blade.php`, `formJs.blade.php`, `app/Http/Controllers/Sale/CustomerHandoverRequestController.php`. `php -l` sạch. CHƯA commit.

### FixT2 — Chỉnh form Tạo/Sửa khớp mockup Excel (sheet "3. Tạo mới - sửa")
Mockup: scratchpad image5/7/8 (đã trích từ file Excel v1.1). User chốt: làm cả A+B; GIỮ tab "Thông tin HĐ + mẫu in"; CÓ nút "+ Thêm mới KH" trong popup; file 60→50MB.

**A. Form (`form.blade.php` + `formJs.blade.php`)** — subagent-driven, review clean
- [x] Restructure Tab 1: cột trái card `border-success` "Khách hàng hoàn tất thủ tục chuyển giao" (field-label, bỏ bảng); cột phải card `border-primary` 3 nhóm badge số ① Thông tin KH · ② Tài khoản NH · ③ Liên hệ.
- [x] File đính kèm chuyển vào nhóm ①, note 50MB, nút "Tải tệp". Giữ nguyên ng-model/ng-if/validate.

**B. Popup tìm KH — TÁI DÙNG popup chuẩn `partials.modals.searchCustomer`** (khớp mockup 100% + có sẵn tab Tổ chức/Cá nhân, đủ filter, 7 cột, "+ Thêm mới KH")
- [x] `create/edit.blade`: bỏ popup custom, thêm `@include('partials.modals.searchCustomer')` + `createHamlet` + `@include('partials.classes.sale.Customer')`.
- [x] `formJs`: xóa block popup custom; thêm `openSearchCustomer` (mở `#searchCustomer`), `setCustomer(basic)` → AJAX `customerHandover.getCustomerData` → `applyNewCustomer` (map deputies/delivery_places/contacts/accounts); include locationJs + searchCustomerJs + createHamletJs (đúng pattern báo giá).
- [x] BE: thêm `getCustomerData($id)` (eager-load quan hệ + append accessor `address`/`customer_type_text`) + route `customerHandover.getCustomerData`. Giữ `searchCustomer` cũ (unused).

**C. File limit**
- [x] `CustomerHandoverStoreRequest`: max 61440→51200 (50MB) + message "50MB".

Verify: `php -l` sạch (controller+routes), wiring match pattern báo giá, không double-include. **CHƯA commit.**
- [x] **User test browser**: đã test, phát sinh FixT3 (khớp 4 TH mockup + màu + file).

### FixT3 — Khớp mockup 4 TH + màu tiêu đề + khối file (design đã duyệt)
Nguồn: Excel sheet 3 (HĐ vật tư) + 4 (HĐDV), mockup TH1 (DN→DN) + TH2 (DN→CN); TH3/4 "tương tự". 1 form ng-if đủ 4 TH. Quyết định user: file 50MB; thêm "Loại hình tổ chức"+"Tỉnh/TP"; liên hệ DN=search / CN=label tên KH.

**A. Field structure (form.blade.php 2 cột + formJs)**
- [ ] Gộp "Mã số thuế"/"CCCD" → **1 field "CMND/MST (*)"** cho cả DN+CN (readonly; DN→customer_tax_code, CN→customer_identity). Áp cả cột trái (oldCustomerData) + phải (new_customer_data).
- [ ] "Ngày cấp"/"Nơi cấp": hiện cho **cả DN và CN** (bỏ ng-if isIndividual).
- [ ] Giữ "Người đại diện*"/"Chức vụ" chỉ DN; "Fax" chỉ DN; "Hãng" theo showVehicleManufact.
- [ ] Thêm **"Loại hình tổ chức"** (readonly) 2 cột: trái map `customerTypeText(oldCustomerData.customer_type)`; phải `newCustomer.customer_type_text`.
- [ ] Nhóm ② thêm **"Tỉnh/TP"** (readonly) — bind province name từ account (nếu có).
- [ ] Nhóm ③ Liên hệ: **DN** → nút search (openSearchContact); **CN** → input readonly = tên KH (không search); Điện thoại | Địa chỉ liên hệ.
- [ ] formJs: thêm hàm `customerTypeText(t)`; khi `isIndividualNew` set contact_name = tên KH.

**B. Màu tiêu đề chuẩn project**
- [ ] Card header: **nền trong suốt** (`card-header` mặc định) + `<h4>` #333 (thay `bg-white` + `<strong>`); giữ viền accent trái xanh dương / phải xanh lá + badge HIỆN TẠI (info) / CẬP NHẬT (success). Vòng số ①②③ xanh dương đặc (badge-primary). Nhãn field giữ màu xanh custom-group.

**C. Khối File đính kèm — pattern chuẩn `document-item`**
- [ ] Thay Bootstrap `custom-file` (xấu) bằng `document-item` (icon file fa-3x + tên + nút xoá X + nút "+", input ẩn `.handover-file`), mirror `sale/firm/quotations/form.blade.php:192-220`. Giữ ghi chú "PDF, DOCX, JPG… tối đa 50 MB". Giữ handler JS `.handover-file` + addFile/removeFile.

Verify: `php -l` (không có PHP đổi), `<div>` cân bằng, user test 4 TH browser. CHƯA commit.

---

## Phase — Tab "Mẫu in" (sửa mẫu in HĐ, áp khi duyệt)
Spec: `design-tab-mau-in.md`. Chốt: sửa tay CKEditor · lưu nháp trên phiếu (`new_template_print`) · áp vào HĐ chính khi **Đã duyệt** · cả FirmContract (`template_print_product`) + WrServiceContract (`template`) · không đụng phụ lục · prefill mẫu hiện tại.
Dự án không có test tự động → mỗi task verify bằng `php -l` (PHP) / cân bằng `<div>` (blade) + test tay browser.

### Task 1 — DB + Model (cột nháp)
**Files:** Create `database/migrations/<ts>_add_new_template_print_to_customer_handover_requests.php`; Modify `app/Model/Sale/CustomerHandoverRequest.php`
- [ ] Migration: `Schema::table('customer_handover_requests', fn($t) => $t->longText('new_template_print')->nullable()->after('new_customer_data'));` (kèm `down()` dropColumn).
- [ ] Model: thêm `'new_template_print'` vào `$fillable` (KHÔNG thêm vào `$casts`).
- [ ] Verify: `php -l` model sạch; `grep DB_ .env` trước khi `php artisan migrate` (xác nhận DB đích local), rồi `php artisan migrate`.

### Task 2 — Service: helper lấy mẫu in HĐ + áp khi duyệt
**Files:** Modify `app/Services/Sale/CustomerHandoverService.php`
- [ ] Thêm helper:
```php
public function getContractTemplate($contractable): ?string
{
    if ($contractable instanceof FirmContract) return $contractable->template_print_product;
    if ($contractable instanceof WrServiceContract) return $contractable->template;
    return null;
}
```
- [ ] Trong `applyToContract($handover)`, NGAY SAU `$this->mapCustomerDataToContract($c, $data);` (áp HĐ chính, TRƯỚC vòng phụ lục):
```php
$tpl = $handover->new_template_print;
if ($tpl !== null && $tpl !== '') {
    if ($c instanceof FirmContract) {
        $c->template_print_product = $tpl;
    } elseif ($c instanceof WrServiceContract) {
        $c->template = $tpl;
    }
    $c->save();
}
```
- [ ] Verify: `php -l` service sạch. (Chỉ HĐ chính — KHÔNG thêm vào vòng phụ lục.)

### Task 3 — Controller: prefill (create/edit) + lưu (store/update)
**Files:** Modify `app/Http/Controllers/Sale/CustomerHandoverRequestController.php`
- [ ] `create()`: tính `$currentTemplate = $contractable ? $service->getContractTemplate($contractable) : null;` và `compact(..., 'currentTemplate')` xuống view.
- [ ] `edit()`: truyền `$currentTemplate` (từ `$handover->contractable`) để formJs fallback khi `new_template_print` rỗng.
- [ ] `store()` + `update()`: lưu `new_template_print` từ request vào phiếu (nằm trong `$request->all()` hoặc gán tường minh `$obj->new_template_print = $request->new_template_print;`). Giữ guard status `DANG_TAO` + đúng người tạo.
- [ ] Verify: `php -l` controller sạch.

### Task 4 — FE: tab Mẫu in (CKEditor + prefill) + include ckeditor
**Files:** Modify `resources/views/sale/customer_handover_requests/form.blade.php`, `create.blade.php`, `edit.blade.php`, `formJs.blade.php`
- [ ] `form.blade.php` `#tab-contract` nhánh `@if($contractable)`: giữ bảng info HĐ; thêm dưới:
```html
<div class="form-group mt-3">
    <label class="form-label">Mẫu in hợp đồng</label>
    <textarea ng-model="form.new_template_print" ck-editor-print rows="20" class="form-control"></textarea>
</div>
```
- [ ] `create.blade.php` + `edit.blade.php`: trong `@section('script')` (trước controller) thêm `<script src="{{ asset('pages/ckeditor/ckeditor.js') }}"></script>` (nếu chưa có) — kiểm bằng grep trước khi thêm để không trùng.
- [ ] `formJs.blade.php`: prefill — thêm `$scope.currentTemplate = @json($currentTemplate ?? null);` và khởi tạo:
  - Create: `if (!$scope.form.new_template_print) $scope.form.new_template_print = $scope.currentTemplate || '';`
  - Edit: giữ `new_template_print` đã có; nếu rỗng → `= $scope.currentTemplate`.
- [ ] Verify: `<div>`/`<textarea>` cân bằng; test tay: mở tab Mẫu in thấy CKEditor prefill mẫu HĐ (Ctrl+F5).

### Task 5 — Show: preview mẫu in (read-only)
**Files:** Modify `resources/views/sale/customer_handover_requests/show.blade.php`
- [ ] Tab Mẫu in ở màn xem: hiển thị `new_template_print` read-only (dùng cách preview HTML sẵn có trong dự án — vd render `{!! $handover->new_template_print !!}` trong khung, hoặc iframe/preview như chỗ in HĐ). Nếu rỗng → "Không thay đổi mẫu in".
- [ ] Verify: test tay màn show phiếu Đã duyệt hiển thị đúng mẫu.

### Kiểm thử tổng (test tay, sau khi deploy)
- [ ] Tạo phiếu chuyển giao từ 1 HĐ Hãng → tab Mẫu in prefill mẫu HĐ → sửa → lưu nháp → DB `new_template_print` có nội dung; HĐ chưa đổi.
- [ ] Duyệt phiếu → HĐ `template_print_product` = mẫu đã sửa; màn view + in HĐ hiển thị mẫu mới.
- [ ] Lặp lại với 1 HĐ Dịch vụ (WrServiceContract → `template`).
- [ ] Trường hợp không sửa (prefill nguyên) → duyệt ghi lại y nguyên (no-op).

CHƯA commit (theo quy tắc không tự commit).

---

## Phase 2 — Cập nhật phiếu liên quan khi chuyển giao KH

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) hoặc superpowers:executing-plans để thực thi từng task. Steps dùng checkbox `- [ ]`.
> Spec đầy đủ: `design-cap-nhat-phieu-lien-quan.md`.

**Goal:** Khi duyệt phiếu YCCGKH, lan KH mới xuống toàn bộ 32 bảng phiếu nghiệp vụ sinh từ HĐ; khi hủy duyệt thì revert về KH cũ; ghi audit từng lần.

**Architecture:** 1 service mới `CustomerHandoverDocumentSync` với registry cấu hình tập trung + resolver `cột→$data` dùng chung (DRY). Mass `UPDATE ... WHERE <link>` theo 5 kiểu link. Gọi trong transaction sẵn có của `approve()`/`cancelApprove()`. Không đụng `CustomerHandoverService`.

**Tech Stack:** PHP 7.4, Laravel 6, MySQL. PHPUnit ^8 (`tests/Unit`) cho logic thuần; tinker cho integration DB.

### Global Constraints (copy verbatim từ spec)
- Morph class prod: FirmContract = `App\Model\Sale\Firm\Contract\FirmContract`; WrServiceContract = `App\Model\Customers\WrServiceContract`. KHÔNG có morphMap → dùng `get_class($contractable)`.
- Nguồn dữ liệu: `$data` = `new_customer_data` (apply) / `old_customer_data` (revert), cấu trúc của `snapshotContractCustomer()` (phẳng `customer_*` + `account{}` + `contact{}`).
- Cột KHÔNG map (giữ nguyên): `delivery_place_id`, `receiver_id`, `receiver_name`, `receiver_phone`.
- Legacy `contract_id` đã verify trên prod = `firm_contracts.id` (addition_accounting_requests 35/35, handover_acceptance_product_records 8/8) → `legacy_contract_id` chỉ áp cho HĐ Firm.
- Mass update bằng `DB::table()->update()` (không loop model, không kích observer).
- Toàn bộ trong transaction; KHÔNG tự commit git (chờ user yêu cầu).

---

### Task 1 — Migration bảng log `customer_handover_sync_logs`

**Files:**
- Create: `TanPhatDev/database/migrations/2026_07_10_100000_create_customer_handover_sync_logs_table.php`

**Interfaces:**
- Produces: bảng `customer_handover_sync_logs(id, customer_handover_request_id, direction, table_name, link_type, contract_id, rows_affected, created_by, created_at)`.

- [ ] **Step 1: Viết migration**

```php
<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateCustomerHandoverSyncLogsTable extends Migration
{
    public function up()
    {
        Schema::create('customer_handover_sync_logs', function (Blueprint $t) {
            $t->bigIncrements('id');
            $t->unsignedBigInteger('customer_handover_request_id')->index();
            $t->string('direction', 10);            // apply | revert
            $t->string('table_name', 100);
            $t->string('link_type', 20);            // firm_fk|wr_fk|dual|polymorphic|legacy_contract_id
            $t->unsignedBigInteger('contract_id');
            $t->integer('rows_affected')->default(0);
            $t->unsignedBigInteger('created_by')->nullable();
            $t->timestamp('created_at')->nullable();
        });
    }

    public function down()
    {
        Schema::dropIfExists('customer_handover_sync_logs');
    }
}
```

- [ ] **Step 2: Kiểm `.env` trỏ DB local trước khi migrate**

Run: `cd TanPhatDev && grep -E '^DB_(HOST|DATABASE)=' .env`
Expected: `DB_HOST=127.0.0.1`, `DB_DATABASE=dev_erp_2` (KHÔNG được là prod `erp_new`). Nếu là prod → DỪNG.

- [ ] **Step 3: Chạy migrate trên dev**

Run: `cd TanPhatDev && php artisan migrate`
Expected: `Migrated: 2026_07_10_100000_create_customer_handover_sync_logs_table`

- [ ] **Step 4: Xác nhận bảng tồn tại**

Run: `cd TanPhatDev && php artisan tinker --execute="echo Schema::hasTable('customer_handover_sync_logs') ? 'OK' : 'MISSING';"`
Expected: `OK`

---

### Task 2 — Service: resolver `cột → $data` (`buildSet` + `aliasValue`) — Unit test

**Files:**
- Create: `TanPhatDev/app/Services/Sale/CustomerHandoverDocumentSync.php`
- Test: `TanPhatDev/tests/Unit/CustomerHandoverDocumentSyncTest.php`

**Interfaces:**
- Produces:
  - `public static function buildSet(array $columns, array $data, ?string $shortName = null): array` — trả `['cột'=>giá trị]` cho các cột map được; bỏ cột không map.
  - `private static function aliasValue(string $col, array $data, ?string $shortName): array` — trả `[bool $has, mixed $val]`.

- [ ] **Step 1: Viết test thất bại cho `buildSet`**

```php
<?php
namespace Tests\Unit;

use App\Services\Sale\CustomerHandoverDocumentSync;
use Tests\TestCase;

class CustomerHandoverDocumentSyncTest extends TestCase
{
    private function sampleData(): array
    {
        return [
            'customer_id' => 99, 'customer_code' => 'KH99', 'customer_name' => 'Cty Mới',
            'customer_type' => 2, 'customer_address' => 'Địa chỉ mới', 'customer_mobile' => '0900',
            'customer_fax' => 'F1', 'customer_tax_code' => 'T1', 'customer_identity' => 'CC1',
            'delivery_place' => 'Kho A', 'deputy_name' => 'Ông A',
            'contact' => ['id' => 7, 'name' => 'LH Mới', 'address' => 'ĐC LH', 'phone' => '0911'],
        ];
    }

    public function test_build_set_maps_known_columns_and_skips_unknown()
    {
        $cols = ['customer_id','customer_name','customer_contact_name','contact_address',
                 'customer_contact_phone','customer_contact_phones','identity_card_number',
                 'delivery_place','customer_short_name','receiver_id','delivery_place_id'];
        $set = CustomerHandoverDocumentSync::buildSet($cols, $this->sampleData(), 'TÊN NGẮN');

        $this->assertSame(99, $set['customer_id']);
        $this->assertSame('Cty Mới', $set['customer_name']);
        $this->assertSame('LH Mới', $set['customer_contact_name']);
        $this->assertSame('ĐC LH', $set['contact_address']);
        $this->assertSame('0911', $set['customer_contact_phone']);
        $this->assertSame('0911', $set['customer_contact_phones']);
        $this->assertSame('CC1', $set['identity_card_number']);
        $this->assertSame('Kho A', $set['delivery_place']);
        $this->assertSame('TÊN NGẮN', $set['customer_short_name']);
        // cột không phải danh tính KH → KHÔNG có trong set
        $this->assertArrayNotHasKey('receiver_id', $set);
        $this->assertArrayNotHasKey('delivery_place_id', $set);
    }
}
```

- [ ] **Step 2: Chạy test — phải fail (class chưa có)**

Run: `cd TanPhatDev && ./vendor/bin/phpunit --filter test_build_set_maps_known_columns_and_skips_unknown`
Expected: FAIL — `Class 'App\Services\Sale\CustomerHandoverDocumentSync' not found`.

- [ ] **Step 3: Viết service với `aliasValue` + `buildSet`**

```php
<?php

namespace App\Services\Sale;

use App\Model\Sale\Customer;
use App\Model\Sale\Firm\Contract\FirmContract;
use Illuminate\Support\Facades\DB;

class CustomerHandoverDocumentSync
{
    /** Map tên cột thực → giá trị trong $data. Trả [bool $has, mixed $val]. */
    private static function aliasValue(string $col, array $data, ?string $shortName): array
    {
        $contact = $data['contact'] ?? [];
        switch ($col) {
            case 'customer_id':             return [true, $data['customer_id'] ?? null];
            case 'customer_code':           return [true, $data['customer_code'] ?? null];
            case 'customer_name':           return [true, $data['customer_name'] ?? null];
            case 'customer_type':           return [true, $data['customer_type'] ?? null];
            case 'customer_address':        return [true, $data['customer_address'] ?? null];
            case 'customer_mobile':         return [true, $data['customer_mobile'] ?? null];
            case 'customer_fax':            return [true, $data['customer_fax'] ?? null];
            case 'customer_tax_code':       return [true, $data['customer_tax_code'] ?? null];
            case 'identity_card_number':
            case 'customer_identity':       return [true, $data['customer_identity'] ?? null];
            case 'customer_short_name':     return [true, $shortName];
            case 'delivery_place':          return [true, $data['delivery_place'] ?? null];
            case 'deputy_name':             return [true, $data['deputy_name'] ?? null];
            case 'customer_contact_id':     return [true, $contact['id'] ?? null];
            case 'customer_contact_name':   return [true, $contact['name'] ?? null];
            case 'contact_address':         return [true, $contact['address'] ?? null];
            case 'customer_contact_phone':
            case 'customer_contact_phones': return [true, $contact['phone'] ?? null];
            default:                        return [false, null]; // cột không map → giữ nguyên
        }
    }

    /** Dựng mảng ['cột'=>giá trị] để UPDATE, chỉ gồm cột map được. */
    public static function buildSet(array $columns, array $data, ?string $shortName = null): array
    {
        $set = [];
        foreach ($columns as $col) {
            [$has, $val] = self::aliasValue($col, $data, $shortName);
            if ($has) {
                $set[$col] = $val;
            }
        }
        return $set;
    }
}
```

- [ ] **Step 4: Chạy test — phải pass**

Run: `cd TanPhatDev && ./vendor/bin/phpunit --filter test_build_set_maps_known_columns_and_skips_unknown`
Expected: PASS (1 test, nhiều assertion).

---

### Task 3 — Service: `resolveLink()` (5 kiểu link × Firm/Wr) — Unit test

**Files:**
- Modify: `TanPhatDev/app/Services/Sale/CustomerHandoverDocumentSync.php`
- Test: `TanPhatDev/tests/Unit/CustomerHandoverDocumentSyncTest.php`

**Interfaces:**
- Produces: `public static function resolveLink(string $link, bool $isFirm, int $cid, string $morphClass): ?array` — trả `null` (không áp cho loại HĐ này) hoặc `['column'=>string, 'value'=>int, 'needsType'=>bool]`.

- [ ] **Step 1: Viết test thất bại**

```php
    public function test_resolve_link_per_contract_type()
    {
        $S = \App\Services\Sale\CustomerHandoverDocumentSync::class;
        // firm_fk: chỉ Firm
        $this->assertSame(['column'=>'firm_contract_id','value'=>5,'needsType'=>false], $S::resolveLink('firm_fk', true, 5, 'X'));
        $this->assertNull($S::resolveLink('firm_fk', false, 5, 'X'));
        // wr_fk: chỉ Wr
        $this->assertSame(['column'=>'wr_service_contract_id','value'=>5,'needsType'=>false], $S::resolveLink('wr_fk', false, 5, 'X'));
        $this->assertNull($S::resolveLink('wr_fk', true, 5, 'X'));
        // dual: đổi cột theo loại
        $this->assertSame('firm_contract_id', $S::resolveLink('dual', true, 5, 'X')['column']);
        $this->assertSame('wr_service_contract_id', $S::resolveLink('dual', false, 5, 'X')['column']);
        // polymorphic: cả 2, needsType=true
        $this->assertSame(['column'=>'contractable_id','value'=>5,'needsType'=>true], $S::resolveLink('polymorphic', true, 5, 'X'));
        $this->assertSame(['column'=>'contractable_id','value'=>5,'needsType'=>true], $S::resolveLink('polymorphic', false, 5, 'X'));
        // legacy_contract_id: chỉ Firm
        $this->assertSame(['column'=>'contract_id','value'=>5,'needsType'=>false], $S::resolveLink('legacy_contract_id', true, 5, 'X'));
        $this->assertNull($S::resolveLink('legacy_contract_id', false, 5, 'X'));
    }
```

- [ ] **Step 2: Chạy test — phải fail**

Run: `cd TanPhatDev && ./vendor/bin/phpunit --filter test_resolve_link_per_contract_type`
Expected: FAIL — `Call to undefined method ...::resolveLink()`.

- [ ] **Step 3: Thêm `resolveLink()` vào service**

```php
    /**
     * Trả câu điều kiện WHERE theo kiểu link + loại HĐ.
     * null = entry không áp cho loại HĐ hiện tại (bỏ qua).
     */
    public static function resolveLink(string $link, bool $isFirm, int $cid, string $morphClass): ?array
    {
        switch ($link) {
            case 'firm_fk':
                return $isFirm ? ['column' => 'firm_contract_id', 'value' => $cid, 'needsType' => false] : null;
            case 'wr_fk':
                return !$isFirm ? ['column' => 'wr_service_contract_id', 'value' => $cid, 'needsType' => false] : null;
            case 'dual':
                return $isFirm
                    ? ['column' => 'firm_contract_id', 'value' => $cid, 'needsType' => false]
                    : ['column' => 'wr_service_contract_id', 'value' => $cid, 'needsType' => false];
            case 'polymorphic':
                return ['column' => 'contractable_id', 'value' => $cid, 'needsType' => true];
            case 'legacy_contract_id':
                return $isFirm ? ['column' => 'contract_id', 'value' => $cid, 'needsType' => false] : null;
            default:
                return null;
        }
    }
```

- [ ] **Step 4: Chạy test — phải pass**

Run: `cd TanPhatDev && ./vendor/bin/phpunit --filter test_resolve_link_per_contract_type`
Expected: PASS.

---

### Task 4 — Service: `registry()` 32 bảng — Unit test cấu trúc

**Files:**
- Modify: `TanPhatDev/app/Services/Sale/CustomerHandoverDocumentSync.php`
- Test: `TanPhatDev/tests/Unit/CustomerHandoverDocumentSyncTest.php`

**Interfaces:**
- Produces: `public function registry(): array` — mảng entry `['table'=>string,'link'=>string,'columns'=>string[]]`.

- [ ] **Step 1: Viết test thất bại (cấu trúc hợp lệ + đếm)**

```php
    public function test_registry_structure_valid()
    {
        $sync = new \App\Services\Sale\CustomerHandoverDocumentSync();
        $reg = $sync->registry();
        $validLinks = ['firm_fk','wr_fk','dual','polymorphic','legacy_contract_id'];

        $this->assertCount(32, $reg);
        $tables = [];
        foreach ($reg as $e) {
            $this->assertArrayHasKey('table', $e);
            $this->assertArrayHasKey('link', $e);
            $this->assertArrayHasKey('columns', $e);
            $this->assertNotEmpty($e['table']);
            $this->assertContains($e['link'], $validLinks);
            $this->assertNotEmpty($e['columns']);
            $tables[] = $e['table'];
        }
        // không trùng bảng
        $this->assertSame(count($tables), count(array_unique($tables)));
        // vài bảng chốt phải có mặt
        $this->assertContains('warehouse_exports', $tables);
        $this->assertContains('borrow_sell_requests', $tables);
        $this->assertContains('account_details', $tables);
        $this->assertContains('handover_acceptance_product_records', $tables);
    }
```

- [ ] **Step 2: Chạy test — phải fail**

Run: `cd TanPhatDev && ./vendor/bin/phpunit --filter test_registry_structure_valid`
Expected: FAIL — `Call to undefined method ...::registry()`.

- [ ] **Step 3: Thêm `registry()` (32 entry, đúng §4 spec)**

```php
    /** 32 bảng ACTIVE cần đồng bộ KH. Xem design-cap-nhat-phieu-lien-quan.md §4. */
    public function registry(): array
    {
        $full = ['customer_id','customer_name','customer_type','customer_address','customer_mobile',
                 'customer_contact_name','contact_address','customer_contact_phone','delivery_place'];
        $idCodeName = ['customer_id','customer_code','customer_name'];
        $idName = ['customer_id','customer_name'];
        $bienBan = ['customer_id','customer_name','customer_address','customer_mobile','identity_card_number'];

        return [
            // KHO / XUẤT
            ['table' => 'warehouse_exports',          'link' => 'dual',        'columns' => $full],
            ['table' => 'warehouse_export_requests',  'link' => 'dual',        'columns' => $full],
            ['table' => 'product_exports',            'link' => 'dual',        'columns' => $full],
            ['table' => 'product_export_requests',    'link' => 'dual',        'columns' => array_merge($full, ['customer_short_name','identity_card_number'])],
            ['table' => 'product_prepick_requests',   'link' => 'polymorphic', 'columns' => $full],
            ['table' => 'product_import_requests',    'link' => 'dual',        'columns' => ['customer_id']],
            ['table' => 'product_imports',            'link' => 'dual',        'columns' => ['customer_id']],
            ['table' => 'warehouse_import_requests',  'link' => 'dual',        'columns' => ['customer_id']],
            ['table' => 'warehouse_imports',          'link' => 'dual',        'columns' => ['customer_id']],
            // MƯỢN BÁN
            ['table' => 'borrow_sell_requests',       'link' => 'polymorphic', 'columns' => $full],
            // BẢO HÀNH
            ['table' => 'firm_warranty_products',         'link' => 'polymorphic', 'columns' => $idCodeName],
            ['table' => 'firm_warranty_request_products', 'link' => 'polymorphic', 'columns' => $idCodeName],
            ['table' => 'firm_warranty_confirm_products', 'link' => 'polymorphic', 'columns' => $idCodeName],
            // BIÊN BẢN / NGHIỆM THU / THANH LÝ / QUYẾT TOÁN
            ['table' => 'handover_acceptance_records',         'link' => 'polymorphic',        'columns' => $bienBan],
            ['table' => 'handover_acceptance_product_records', 'link' => 'legacy_contract_id',  'columns' => ['customer_id','customer_name','customer_address','customer_type','customer_identity']],
            ['table' => 'liquidation_records',                 'link' => 'polymorphic',        'columns' => $bienBan],
            ['table' => 'settlement_contracts',                'link' => 'polymorphic',        'columns' => $bienBan],
            // LẮP RÁP / GIAO VIỆC
            ['table' => 'assembly_requests',     'link' => 'firm_fk', 'columns' => ['customer_id','customer_code','customer_name','customer_address','customer_contact_id','customer_contact_name','customer_contact_phones','delivery_place']],
            ['table' => 'assign_other_requests', 'link' => 'firm_fk', 'columns' => ['customer_id','customer_code','customer_name','customer_address','customer_contact_id','customer_contact_name','customer_contact_phones','delivery_place']],
            ['table' => 'wr_assign_tasks',       'link' => 'wr_fk',   'columns' => ['customer_id','customer_name','customer_mobile','customer_contact_id','customer_contact_name','customer_contact_phones','delivery_place']],
            ['table' => 'wr_import_results',     'link' => 'firm_fk', 'columns' => ['customer_id','customer_code','customer_name','customer_contact_name','customer_contact_phones','delivery_place']],
            // KẾ TOÁN / CÔNG NỢ
            ['table' => 'wr_accounting_service_requests', 'link' => 'wr_fk',              'columns' => $idName],
            ['table' => 'wr_accounting_services',         'link' => 'wr_fk',              'columns' => $idName],
            ['table' => 'addition_accounting_requests',   'link' => 'legacy_contract_id', 'columns' => $idCodeName],
            ['table' => 'contract_waiting_monthly_accounting', 'link' => 'polymorphic',   'columns' => $idCodeName],
            ['table' => 'contract_waiting_settlements',        'link' => 'polymorphic',   'columns' => $idCodeName],
            ['table' => 'account_details',                     'link' => 'polymorphic',   'columns' => ['customer_id']],
            ['table' => 'bill_payment_details',                'link' => 'polymorphic',   'columns' => $idCodeName],
            ['table' => 'bill_payment_request_details',        'link' => 'polymorphic',   'columns' => $idCodeName],
            ['table' => 'bill_adjust_dept_details',            'link' => 'polymorphic',   'columns' => $idCodeName],
            ['table' => 'bill_productivity_settlement_quarter_contracts', 'link' => 'polymorphic', 'columns' => $idCodeName],
            ['table' => 'bill_commission_settlement_quarter_contracts',   'link' => 'polymorphic', 'columns' => $idCodeName],
        ];
    }
```

- [ ] **Step 4: Chạy test — phải pass**

Run: `cd TanPhatDev && ./vendor/bin/phpunit --filter test_registry_structure_valid`
Expected: PASS.

---

### Task 5 — Service: `sync()` orchestrator (DB update + audit log)

**Files:**
- Modify: `TanPhatDev/app/Services/Sale/CustomerHandoverDocumentSync.php`

**Interfaces:**
- Consumes: `resolveLink()`, `buildSet()`, `registry()` (Task 2-4); bảng log (Task 1).
- Produces: `public function sync($contractable, array $data, string $direction, $handover): void`.

- [ ] **Step 1: Thêm `sync()` vào service**

```php
    /**
     * Lan $data (KH) xuống mọi phiếu liên quan của HĐ.
     * @param FirmContract|\App\Model\Customers\WrServiceContract $contractable
     * @param array  $data      new_customer_data (apply) | old_customer_data (revert)
     * @param string $direction 'apply' | 'revert' (ghi log)
     * @param \App\Model\Sale\CustomerHandoverRequest $handover
     */
    public function sync($contractable, array $data, string $direction, $handover): void
    {
        if (empty($data) || empty($contractable)) {
            return;
        }

        $isFirm     = $contractable instanceof FirmContract;
        $morphClass = get_class($contractable);
        $cid        = (int) $contractable->id;

        // short_name KH mới (query 1 lần, dùng cho product_export_requests)
        $shortName = null;
        if (!empty($data['customer_id'])) {
            $cust = Customer::find($data['customer_id']);
            $shortName = $cust ? $cust->short_name : null;
        }

        foreach ($this->registry() as $e) {
            $link = self::resolveLink($e['link'], $isFirm, $cid, $morphClass);
            if ($link === null) {
                continue; // entry không áp cho loại HĐ này
            }

            $set = self::buildSet($e['columns'], $data, $shortName);
            if (empty($set)) {
                continue;
            }

            $q = DB::table($e['table'])->where($link['column'], $link['value']);
            if ($link['needsType']) {
                $q->where('contractable_type', $morphClass);
            }
            $rows = $q->update($set);

            DB::table('customer_handover_sync_logs')->insert([
                'customer_handover_request_id' => $handover->id,
                'direction'     => $direction,
                'table_name'    => $e['table'],
                'link_type'     => $e['link'],
                'contract_id'   => $cid,
                'rows_affected' => $rows,
                'created_by'    => auth()->id(),
                'created_at'    => now(),
            ]);
        }
    }
```

- [ ] **Step 2: Lint**

Run: `cd TanPhatDev && php -l app/Services/Sale/CustomerHandoverDocumentSync.php`
Expected: `No syntax errors detected`.

- [ ] **Step 3: Chạy lại toàn bộ Unit test (không hồi quy)**

Run: `cd TanPhatDev && ./vendor/bin/phpunit --filter CustomerHandoverDocumentSyncTest`
Expected: PASS 3 test.

---

### Task 6 — Tích hợp controller `approve()` / `cancelApprove()`

**Files:**
- Modify: `TanPhatDev/app/Http/Controllers/Sale/CustomerHandoverRequestController.php`

**Interfaces:**
- Consumes: `CustomerHandoverDocumentSync::sync()`.

- [ ] **Step 1: `approve()` — gọi sync sau `applyToContract` (trong transaction), trước khi set trạng thái**

Trong `approve($id)`, khối `try` (ngay sau dòng `$service->applyToContract($handover);`), thêm:

```php
            (new \App\Services\Sale\CustomerHandoverDocumentSync())
                ->sync($handover->contractable, $handover->new_customer_data ?? [], 'apply', $handover);
```

- [ ] **Step 2: `cancelApprove()` — gọi sync revert sau `revertContract`**

Trong `cancelApprove($id)`, khối `try` (ngay sau dòng `$service->revertContract($handover);`), thêm:

```php
            (new \App\Services\Sale\CustomerHandoverDocumentSync())
                ->sync($handover->contractable, $handover->old_customer_data ?? [], 'revert', $handover);
```

- [ ] **Step 3: Lint**

Run: `cd TanPhatDev && php -l app/Http/Controllers/Sale/CustomerHandoverRequestController.php`
Expected: `No syntax errors detected`.

---

### Task 7 — Integration verify trên dev (tinker) + review

**Files:** không đổi (chỉ chạy kiểm thử).

- [ ] **Step 1: Chọn 1 HĐ Firm trên dev có phiếu downstream**

Run:
```
cd TanPhatDev && php artisan tinker --execute="
\$c = App\Model\Sale\Firm\Contract\FirmContract::whereHas('warehouse_exports')->first() ?? App\Model\Sale\Firm\Contract\FirmContract::first();
echo 'contract_id='.\$c->id.PHP_EOL;
echo 'warehouse_exports='.DB::table('warehouse_exports')->where('firm_contract_id',\$c->id)->count().PHP_EOL;
"
```
Expected: in id HĐ + số phiếu. Ghi lại id để dùng ở Step 2-3. (Nếu quan hệ `warehouse_exports` không tồn tại, dùng `FirmContract::first()` và tra count bằng `DB::table`.)

- [ ] **Step 2: Chạy `sync` apply với KH giả + kiểm log** (ghi thật lên dev, revert ở Step 3)

Run (thay `PUT_ID` = id ở Step 1):
```
cd TanPhatDev && php artisan tinker --execute="
\$c = App\Model\Sale\Firm\Contract\FirmContract::find(PUT_ID);
\$h = new stdClass(); \$h->id = 999999;
\$data = ['customer_id'=>App\Model\Sale\Customer::value('id'),'customer_name'=>'ZZZ TEST','customer_code'=>'ZZZ','customer_type'=>2,'customer_address'=>'A','customer_mobile'=>'0','contact'=>['name'=>'c','address'=>'ca','phone'=>'cp']];
(new App\Services\Sale\CustomerHandoverDocumentSync())->sync(\$c, \$data, 'apply', \$h);
echo 'logs_rows='.DB::table('customer_handover_sync_logs')->where('customer_handover_request_id',999999)->sum('rows_affected').PHP_EOL;
echo 'we_name='.DB::table('warehouse_exports')->where('firm_contract_id',\$c->id)->value('customer_name').PHP_EOL;
"
```
Expected: `we_name=ZZZ TEST` (nếu HĐ có warehouse_exports); có dòng log.

- [ ] **Step 3: `sync` revert đưa lại KH cũ + dọn log test**

Run (thay `PUT_ID`):
```
cd TanPhatDev && php artisan tinker --execute="
\$c = App\Model\Sale\Firm\Contract\FirmContract::find(PUT_ID);
\$h = new stdClass(); \$h->id = 999999;
\$old = (new App\Services\Sale\CustomerHandoverService())->snapshotContractCustomer(\$c);
(new App\Services\Sale\CustomerHandoverDocumentSync())->sync(\$c, \$old, 'revert', \$h);
DB::table('customer_handover_sync_logs')->where('customer_handover_request_id',999999)->delete();
echo 'reverted_we_name='.DB::table('warehouse_exports')->where('firm_contract_id',\$c->id)->value('customer_name').PHP_EOL;
"
```
Expected: `customer_name` về giá trị KH gốc; log test đã xóa.

- [ ] **Step 4: Self-review + spec coverage**
- [ ] Registry 32 bảng khớp §4 spec; không đụng `CustomerHandoverService`.
- [ ] Cả 2 lời gọi `sync` nằm TRONG transaction (`approve`/`cancelApprove`).

- [ ] **Step 5: Kiểm thử tay end-to-end (sau deploy)**
- [ ] Tạo + gửi duyệt 1 phiếu YCCGKH cho HĐ Firm có sẵn phiếu xuất kho/bảo hành → **Duyệt** → mọi phiếu đổi sang KH mới; `customer_handover_sync_logs` có dòng `direction=apply`.
- [ ] **Hủy duyệt** phiếu đó → mọi phiếu về KH cũ; log có dòng `direction=revert`.
- [ ] Lặp với 1 HĐ Wr (WrServiceContract) → chỉ bảng `wr_fk`/`polymorphic` bị đụng.

CHƯA commit (theo quy tắc không tự commit).

---

## Fix (2026-07-23) — box dashboard "YC chuyển giao khách hàng chờ duyệt" count sai scope
Box đã có (HomeController::approveList ~2617, group QUAN_LY_HOP_DONG, quyền `Duyệt phiếu YC chuyển giao khách hàng`) nhưng count hard-code `where('company_id', công ty user)` → KHÔNG khớp scope thực của DS chờ duyệt (applyPermissionScope: tổng cty/cty/phòng ban quản lý/bộ phận quản lý) → count sai (0/lệch), box không hiện đúng theo spec ("trong công ty/phòng ban/bộ phận người đó quản lý").

- [x] Model `CustomerHandoverRequest`: thêm query scope `scopeApprovableForUser($query,$user)` (DRY nguồn scope duy nhất).
- [x] Controller `applyPermissionScope` → delegate `$query->approvableForUser(auth()->user())` (giữ hành vi, hết trùng logic).
- [x] HomeController box: `CustomerHandoverRequest::approvableForUser($logged_user)->where('status',CHO_DUYET)->count()` — khớp DS chờ duyệt.
- [x] php -l sạch 3 file. home.blade render box động (ng-repeat) → box hiện khi count>0.
- [ ] Verify data (DB có migrate customer_handover_requests — erp_new prod chưa có bảng) + commit. Branch: task_10696.
