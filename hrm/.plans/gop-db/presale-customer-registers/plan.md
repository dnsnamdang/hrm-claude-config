# Plan — Danh sách đăng ký khách hàng toàn công ty

> @junfoke · 2026-10-08 · nhánh `develop` · Design: `.plans/gop-db/presale-customer-registers/design.md`

- [x] BE service + controller + resource + route (gate quyền 1526) + cột xuất Excel
- [x] FE màn danh sách chuẩn (lọc, tìm nhanh, sắp xếp, cấu hình cột, Xuất Excel) + menu presale
- [x] Đối chiếu ERP `CustomerRegister::searchByFilter`: không lọc 2.071 dòng; tên KH 284; số báo giá 1.278; NV 65 → 333;
      NV 84 + hết hạn 36; + số báo giá 14 — khớp md5 (không lọc: cùng tập dòng, 1 cặp trùng giờ đổi chỗ vì HRM thêm `id`)
- [x] Không quyền → API 403. Playwright (quyền cấp tạm rồi gỡ): lọc Thời hạn, Người đăng ký, Số báo giá + Enter,
      tìm nhanh, Làm mới, sắp xếp, chuyển trang, Xuất Excel (đọc lại file 2.071 dòng)

## Checkpoint — 2026-10-08

- **Vừa hoàn thành:** cả màn, CHƯA commit (nhánh `develop`).
- **Bước tiếp theo:** admin gán quyền 1526 cho vai trò cần xem (hiện chưa vai trò nào có).
- **Blocked:** không.

## Ngày 23/11/2026 (@junfoke) — phản hồi bổ sung (không có task Redmine)
- [x] 23/11/2026 — Khảo sát yêu cầu bổ sung từ bảng phản hồi chuyển đổi: đăng ký KH theo báo giá + dự án TKT; thời hạn mặc định theo cấu hình, sửa phải duyệt TP → BGĐ; In / Excel / lịch sử; cấu hình "Thông báo hết hạn đăng ký KH" ở tab Báo giá – Hợp đồng; gia hạn qua TP → BGĐ. ERP: đăng ký chỉ sinh từ báo giá, thời hạn 1 số chung (`configs.customer_register_expiry`, 30 ngày), không có sửa/gia hạn/duyệt/lịch sử/cron; bảng `customer_registers` local 2,143 dòng, 11 còn hạn. HRM: màn hiện chỉ xem; tab Báo giá – Hợp đồng đã có ô "Thời gian đăng ký KH"; dự án TKT có luồng gia hạn TP → BGĐ làm khuôn được.
- [x] 23/11/2026 — User chốt **Cách A** (ERP giữ nguyên logic): bảng chung `customer_registers` không đổi cấu trúc; đăng ký đúng thời hạn mặc định ghi thẳng bảng chung (như nút ERP); thời hạn khác mặc định / gia hạn tạo phiếu yêu cầu ở bảng riêng HRM, duyệt xong mới ghi sang bảng chung. Thông báo hết hạn: gửi **người đăng ký**, trước **3 ngày** (ô cấu hình mới cạnh "Thời gian đăng ký KH"), tác vụ hằng ngày gửi chuông + push, bấm mở đúng đăng ký có nút Gia hạn.
- [x] 23/11/2026 — User đồng ý phạm vi xem: có quyền Xem ⇒ theo mức PB / Công ty / Tổng công ty; không quyền ⇒ chỉ đăng ký của mình; 2 tab Đăng ký KH + Phiếu yêu cầu.
- [x] 26/11/2026 — User chốt: KH tổ chức bắt buộc chọn người liên hệ khi đăng ký từ báo giá; báo giá Đã duyệt + Trúng thầu được đăng ký. Spec `docs/superpowers/specs/gop-db/2026-11-26-dang-ky-khach-hang-bo-sung-design.md` — user DUYỆT 26/11.

---

# Giai đoạn 2 — Đăng ký / đổi thời hạn / gia hạn khách hàng trên HRM — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Nhân viên KD đăng ký khách hàng từ báo giá / dự án TKT trên HRM; đổi thời hạn và gia hạn đi phiếu duyệt TP → BGĐ; nhắc hết hạn; màn danh sách có 2 tab, In, Excel, Lịch sử — ERP không đổi.

**Architecture:** `customer_registers` (bảng ERP) là nguồn DUY NHẤT của "đăng ký có hiệu lực" và chỉ được ghi qua một service (`CustomerRegisterWriteService`). Phiếu chờ duyệt, liên kết nguồn, lịch sử nằm ở 3 bảng mới của HRM. Luồng duyệt chép khuôn `ProspectiveProjectExtensionService`.

**Tech Stack:** Laravel 8 / PHP 7.4 (hrm-api, module `Assign`), Nuxt 2 / Vue 2 (hrm-client, `V2Base*`), PHPUnit `DatabaseTransactions` trên DB local `gop_db_rbac`.

**Spec:** `docs/superpowers/specs/gop-db/2026-11-26-dang-ky-khach-hang-bo-sung-design.md` (đọc kèm, các § dưới đây trỏ vào đó).

## Global Constraints

- KHÔNG sửa repo ERP `TanPhatDev`; KHÔNG thêm/đổi cột `customer_registers`; KHÔNG ghi `customer_registers` khi phiếu chưa BGĐ duyệt.
- "Còn hạn" ⇔ `expired_date >= hôm nay` (so theo NGÀY, như màn hiện có).
- `customer_registers.employee_id` = `App\Helpers\ErpPermissionHelper::erpEmployeeId()` (DB gộp: = `auth()->id()`); không dùng `info->id`.
- Thời hạn mặc định = `App\Support\CompanyConfig::value('customer_register_expiry')` (theo công ty đang thao tác); thiếu ⇒ 30.
- Báo giá được đăng ký: `created_by` = mình, `status ∈ {Quotation::STATUS_DA_DUYET (4), Quotation::STATUS_TRUNG_THAU (7)}`.
- Dự án TKT được đăng ký: `created_by` = mình, có `customer_id`, `status ∉ {11, 12}`.
- KH tổ chức ⇔ `customers.customer_type > 1` ⇒ `customer_contact_id` bắt buộc; KH cá nhân ⇒ NULL.
- Câu báo nguyên văn ERP: "Không có quyền đăng ký khách hàng này!", "Bạn đã đăng ký khách hàng này rồi!". Câu mới: "Khách hàng đang có yêu cầu đăng ký chờ duyệt".
- Màu: Chờ TP duyệt `#D97706`, Chờ BGĐ duyệt `#D97706`, Đã duyệt `#16A34A`, Từ chối `#DC2626`; Còn hạn `#16A34A`, Hết hạn `#6B7280`.
- Mã quyền mới: `presale.dang_ky_khach_hang_truong_phong.approve`, `presale.dang_ky_khach_hang_ban_giam_doc.approve` (kind approve, platforms ['hrm'], cùng `subsystem_group`/`subsystem`/`feature` với 2 mã `presale.gia_han_du_an_tkt_*`).
- **Hỏi user trước khi:** chạy migration, chạy `permission:catalog-sync`, merge / push.
- Nhánh: `dang-ky-khach-hang` tách từ `origin/develop`, worktree `.worktrees/dang-ky-khach-hang` (2 repo), không track nhánh chung.
- FE: mọi ô form `V2Base*`, popup `V2BaseModal`, select trong popup `V2BaseSelectInModal`, badge `V2BaseBadge` màu BE trả, nút theo `button-convention`, nút không dùng được thì ẨN.

## Review Focus

1. ERP Hủy (xoá cứng) dòng gốc khi phiếu gia hạn đang chờ ⇒ duyệt báo lỗi rõ, không 500; lịch sử / phiếu vẫn mở được — test ở Task 3.
2. Trong lúc phiếu Đăng ký chờ, người khác đăng ký bên ERP ⇒ BGĐ duyệt bị chặn bởi kiểm tra §5.3 — test ở Task 3.
3. Bấm đăng ký 2 lần / 2 người cùng lúc cho cùng KH ⇒ chỉ 1 dòng hiệu lực (kiểm lại trong transaction + `lockForUpdate` dòng `customers`) — test ở Task 2.
4. Gia hạn đăng ký đã hết hạn khi duyệt ⇒ hạn mới = hôm nay + số ngày — test ở Task 3.
5. Tác vụ nhắc chạy 2 lần cùng ngày / chạy bù ⇒ mỗi mốc hạn chỉ báo 1 lần — test ở Task 5.

---

### Task 1: Bảng mới, entity, mã quyền, cấu hình số ngày báo trước

**Files:**
- Create: `hrm-api/Modules/Assign/Database/Migrations/2026_11_26_000001_create_customer_register_requests_table.php`, `..._000002_create_customer_register_links_table.php`, `..._000003_create_customer_register_histories_table.php`
- Create: `hrm-api/Modules/Assign/Entities/CustomerRegisterRequest.php`, `CustomerRegisterLink.php`, `CustomerRegisterHistory.php`
- Modify: `hrm-api/app/Support/Permissions/Catalog/presale.php` (2 mã, ngay sau 2 mã `gia_han_du_an_tkt_*`)
- Modify: `hrm-api/Modules/MasterData/Support/RegulationTabRegistry.php` (tab `baogia`) + `hrm-client/components/regulation-config/data.js` (tab `baogia`)
- Test: `hrm-api/Modules/Assign/Tests/Feature/CustomerRegisterSchemaTest.php`

**Interfaces — Produces:**
- `customer_register_requests`: id, code (unique), type tinyint (1 Đăng ký, 2 Gia hạn), customer_register_id NULL (không FK), customer_id, customer_contact_id NULL, source_type varchar(30) NULL ('quotation' | 'prospective_project'), source_id NULL, days smallint, note text, old_expired_date date NULL, new_expired_date date NULL, status tinyint, reject_reason text NULL, tp_approved_by/at, approved_by/at, rejected_by/at, company_id, department_id, part_id, created_by, updated_by, timestamps. Index (status), (customer_id, customer_contact_id), (customer_register_id).
- `customer_register_links`: id, customer_register_id (unique, không FK), source_type, source_id, created_by, timestamps.
- `customer_register_histories`: id, customer_register_id NULL, customer_register_request_id NULL, action varchar(30), old_value / new_value json NULL, note text NULL, created_by, created_at. Index 2 cột id.
- `CustomerRegisterRequest extends BaseModel`: `TYPE_DANG_KY=1, TYPE_GIA_HAN=2`; `STATUS_CHO_TP_DUYET=1, STATUS_CHO_BGD_DUYET=2, STATUS_DA_DUYET=3, STATUS_TU_CHOI=4`; `STATUSES` (id, name, color); `PENDING_STATUSES`; `PERMISSION_TP`, `PERMISSION_BGD`; `static getNextCode(): string` → `YCDK-YYYY-NNNNN` (khuôn `ProspectiveProjectExtensionRequest::getNextCode`).
- `CustomerRegisterHistory` action: `register`, `request`, `tp_approve`, `bgd_approve`, `reject`, `change_expiry`, `remind` (hằng `ACTION_*`).
- Cấu hình `customer_register_notify_days` (label "Thông báo hết hạn đăng ký khách hàng", unit "ngày", integer, mặc định 3). **Store: chờ user chốt ở Step 4** — đề xuất cột mới `configs.customer_register_notify_days` (unsignedSmallInteger nullable default 3; ERP không đọc ⇒ không đổi hành vi ERP) để đi đúng `store => 'config'` của registry (có sẵn lịch sử, hẹn ngày). User không cho thêm cột vào `configs` ⇒ dùng `general_regulations` (bảng HRM), ô vẫn hiện ở tab Báo giá – Hợp đồng.

- [ ] **Step 1:** Test `CustomerRegisterSchemaTest`: `test_tables_exist`, `test_request_next_code_format` (`/^YCDK-\d{4}-\d{5}$/`), `test_statuses_have_standard_colors`, `test_catalog_has_two_approve_codes` (kind approve, platforms ['hrm']), `test_registry_has_notify_days_field`.
- [ ] **Step 2:** `php vendor/bin/phpunit Modules/Assign/Tests/Feature/CustomerRegisterSchemaTest.php` → FAIL.
- [ ] **Step 3:** Viết migration, entity, catalog, registry, `data.js` (`num('Thông báo hết hạn đăng ký khách hàng', 'ngày', 3)` ngay dưới "Thời gian đăng ký khách hàng").
- [ ] **Step 4:** **HỎI USER** (danh sách bảng/cột + store cấu hình) → chạy migration local, `php artisan permission:catalog-sync --dry-run`, rồi chạy thật.
- [ ] **Step 5:** Test → PASS. Commit `feat(presale): bảng phiếu yêu cầu / liên kết / lịch sử đăng ký KH + 2 mã duyệt + cấu hình nhắc hết hạn`.

### Task 2: Service lõi — đăng ký trực tiếp hoặc tạo phiếu

**Files:**
- Create: `hrm-api/Modules/Assign/Services/CustomerRegister/CustomerRegisterWriteService.php`, `CustomerRegisterHistoryService.php`
- Test: `hrm-api/Modules/Assign/Tests/Feature/CustomerRegisterWriteServiceTest.php`

**Interfaces — Consumes:** entity Task 1. **Produces:**
- `CustomerRegisterWriteService::defaultDays(?int $companyId = null): int`
- `::eligibility(int $customerId, ?int $contactId, int $employeeId, bool $includePending = true, ?int $ignoreRequestId = null): ?string` — câu lỗi hoặc null. Thứ tự: mình đã còn hạn → "Bạn đã đăng ký…"; người khác còn hạn (cá nhân theo customer_id; tổ chức theo customer_id + contact) → "Không có quyền…"; `$includePending` + có phiếu Đăng ký đang chờ cùng KH (+contact), trừ `$ignoreRequestId` → "Khách hàng đang có yêu cầu đăng ký chờ duyệt".
- `::sourceFromQuotation(Quotation $q): array` / `::sourceFromProject(ProspectiveProject $p): array` → `['source_type','source_id','source_code','customer_id','customer_contact_id','can' => bool,'reason' => ?string]`.
- `::register(array $source, ?int $contactId, int $days, string $note): array` → `['mode' => 'registered'|'requested', 'register_id' => ?int, 'request' => ?CustomerRegisterRequest]`. Transaction + `lockForUpdate` dòng `customers`, kiểm `eligibility`. KH tổ chức thiếu contact ⇒ `ValidationException` trường `customer_contact_id`. `days == defaultDays()` ⇒ `insertActive`; khác ⇒ phiếu `TYPE_DANG_KY` Chờ TP (company/department/part của người tạo).
- `::insertActive(int $customerId, ?int $contactId, int $employeeId, int $days, string $note, ?string $sourceType, ?int $sourceId, ?Carbon $from = null): int` — điểm ghi DUY NHẤT vào `customer_registers`. Báo giá có `erp_firm_quotation_id` ⇒ ghi `firm_quotation_id`, ngược lại `quotation_id`; dự án ⇒ 2 cột NULL + dòng `customer_register_links`. Ghi lịch sử `register`. Gửi thông báo y ERP cho người có quyền xem danh sách đăng ký (`PermissionLookup::holders(<mã xem>, $companyId)`), link danh sách `?register_id=`.
- `::setExpiry(int $registerId, Carbon $newDate): void` — điểm sửa DUY NHẤT `expired_date`; lịch sử `change_expiry` (cũ → mới).
- `CustomerRegisterHistoryService::log(?int $registerId, ?int $requestId, string $action, $old = null, $new = null, ?string $note = null): void`; `::forRegister(int $registerId): array` (mới → cũ; thiếu dòng `register` ⇒ thêm dòng suy từ `created_at` + `employee_id`, note "Đăng ký từ ERP").

- [ ] **Step 1:** Test: `test_default_days_registers_directly` (1 dòng bảng chung, `expired_date = today + N`, `employee_id = auth()->id()`, có lịch sử register); `test_custom_days_creates_pending_request_without_register`; `test_blocks_when_other_employee_active`; `test_blocks_when_self_active`; `test_blocks_when_pending_request_exists`; `test_org_customer_requires_contact`; `test_org_customer_other_contact_is_allowed`; `test_synced_quotation_writes_firm_quotation_id`; `test_project_source_writes_link_row`; `test_quotation_status_closed_cannot_register` (status 5 ⇒ `can = false`); `test_double_submit_creates_one_row`.
- [ ] **Step 2:** FAIL. **Step 3:** cài đặt. **Step 4:** PASS.
- [ ] **Step 5:** Commit `feat(presale): service đăng ký khách hàng — ghi trực tiếp / tạo phiếu, chặn trùng y ERP`.

### Task 3: Gia hạn + duyệt TP → BGĐ + Từ chối

**Files:**
- Create: `hrm-api/Modules/Assign/Services/CustomerRegister/CustomerRegisterRequestService.php`
- Test: `hrm-api/Modules/Assign/Tests/Feature/CustomerRegisterRequestServiceTest.php`

**Interfaces — Consumes:** Task 2. **Produces:**
- `storeExtension(int $registerId, int $days, string $reason): CustomerRegisterRequest` — chỉ người đăng ký, đăng ký còn hạn, chưa có phiếu Gia hạn chờ; `old_expired_date` = hạn hiện tại.
- `canExtend(object $registerRow, array $pendingRegisterIds): bool`
- `tpApprove(CustomerRegisterRequest $r)` — quyền TP + `department_id ∈ QuotationService::managedDepartmentIdsOf(me)`; status 1 → 2; báo người có quyền BGĐ cùng công ty.
- `bgdApprove(CustomerRegisterRequest $r)` — quyền BGĐ + cùng công ty; status 2 → 3 và áp dụng:
  - Đăng ký: `eligibility(..., includePending: true, ignoreRequestId: $r->id)` lỗi ⇒ `ValidationException`, phiếu giữ status 2; hợp lệ ⇒ `insertActive(..., from: today)`, ghi `customer_register_id`, `new_expired_date`.
  - Gia hạn: dòng gốc không còn ⇒ lỗi "Đăng ký đã bị hủy, vui lòng từ chối yêu cầu"; đã hết hạn mà người khác đang giữ khách ⇒ lỗi; hạn mới = `max(expired_date, today) + days` ⇒ `setExpiry`.
- `reject(CustomerRegisterRequest $r, string $reason)` — TP ở status 1 / BGĐ ở status 2; lý do bắt buộc.
- `pendingQuery()` — khuôn `ProspectiveProjectExtensionService::pendingQuery`.
- Mỗi bước ghi lịch sử + thông báo (`NotificationMeta::build`, skill `notification-convention`): tạo phiếu → TP phòng; TP duyệt → BGĐ; BGĐ duyệt / Từ chối → người tạo.

- [ ] **Step 1:** Test: `test_extension_only_owner_and_active`; `test_one_pending_extension_per_register`; `test_tp_cannot_approve_other_department`; `test_full_flow_register_request_inserts_on_bgd` (sau TP: 0 dòng bảng chung; sau BGĐ: 1 dòng, `expired_date = today + days`); `test_bgd_blocked_when_other_registered_meanwhile`; `test_extension_of_expired_register_counts_from_today`; `test_extension_when_register_deleted_by_erp`; `test_reject_requires_reason_and_ends_flow`; `test_history_rows_written_each_step`.
- [ ] **Step 2:** FAIL. **Step 3:** cài đặt. **Step 4:** PASS.
- [ ] **Step 5:** Commit `feat(presale): phiếu đổi thời hạn / gia hạn đăng ký KH — duyệt TP → BGĐ`.

### Task 4: API, phạm vi xem, cột mới ở danh sách

**Files:**
- Modify: `hrm-api/Modules/Assign/Routes/api.php` (nhóm `/assign/report/customer-registers`, dòng ~1110), `Services/Report/CustomerRegisterService.php`, `Http/Controllers/Api/V1/CustomerRegisterController.php`, `Transformers/CustomerRegisterResource/CustomerRegisterResource.php`, `app/ExcelExport/ExportColumnRegistry.php`
- Create: `Http/Controllers/Api/V1/CustomerRegisterRequestController.php`, `Transformers/CustomerRegisterResource/CustomerRegisterRequestResource.php`, `Http/Requests/CustomerRegister/{RegisterCustomerRequest,ExtendRegisterRequest,RejectRegisterRequest}.php` (chỉ `rules()`)
- Test: `hrm-api/Modules/Assign/Tests/Feature/CustomerRegisterApiTest.php`

**Interfaces — Produces (FE dùng):**
- `GET /assign/quotations/{id}/register-customer-info`, `POST /assign/quotations/{id}/register-customer` `{customer_contact_id?, days, note}`; `GET|POST /assign/prospective-projects/{id}/register-customer(-info)` (contact lấy từ dự án). Info: `{can, reason, customer:{id,code,name,is_organization}, contact:{id,name,role}|null, contacts:[{id,name,role,phone}], suggested_contact_id, default_days, source:{type,code}}` (`contacts` chỉ khi nguồn báo giá + KH tổ chức; `suggested_contact_id` khớp tên hoặc SĐT). POST trả `{mode, message}`.
- `GET /assign/report/customer-registers` bỏ middleware cứng; scope theo `CurrentPermission::scope(<mã xem>)` → PB / Công ty / Tổng công ty; không quyền ⇒ `employee_id = mình`. Dòng thêm `status_text`, `status_color`, `source_type`, `source_code`, `source_link` (HRM: `quotation_id`, hoặc tra `quotations.erp_firm_quotation_id = firm_quotation_id`; dự án qua `customer_register_links`), `can_extend`, `has_pending_extension`. `meta.can_view_all`.
- `GET /assign/report/customer-registers/{id}/histories`, `POST /assign/report/customer-registers/{id}/extend` `{days, reason}`.
- `GET /assign/customer-register-requests` (lọc `status`, `type`, `created_by`, `pending_mine=1`, `keyword`; phạm vi: của mình ∪ `pendingQuery()` ∪ phạm vi quyền Xem), `GET /export`, `GET /{id}`, `GET /{id}/histories`, `POST /{id}/approve` (chọn bước theo status), `POST /{id}/reject` `{reason}`. Resource có `can_approve`, `can_reject`, `status_text`, `status_color`.
- Phạm vi quyền Xem: `master_data.khach_hang_da_dang_ky.view` hiện `scopes => []`. Kiểm thêm `scopes [2,3,4]` có đổi kết quả `can()` bên ERP / grant hiện có (scope NULL) không. Không đổi ⇒ thêm vào mã cũ. Có đổi ⇒ DỪNG, báo user, dùng mã HRM mới `presale.dang_ky_khach_hang.view` (scopes [2,3,4], platforms ['hrm']).

- [ ] **Step 1:** Kiểm vụ quyền Xem như trên; ghi kết luận vào plan.
- [ ] **Step 2:** Test: `test_list_without_permission_shows_only_mine`; `test_list_with_company_scope_shows_company`; `test_list_row_has_status_and_source`; `test_quotation_register_info_org_customer_returns_contacts_and_suggestion`; `test_register_endpoints_return_mode`; `test_request_list_pending_mine`; `test_approve_endpoint_picks_step_by_status`; `test_approve_403_without_permission`; `test_request_resource_flags_by_step`; `test_quotation_list_flag_only_for_creator_and_status_4_7`.
- [ ] **Step 3:** FAIL. **Step 4:** cài đặt (gồm cờ `can_register_customer` trên resource danh sách / chi tiết báo giá + dự án TKT, nạp gộp 1 lần theo trang — không N+1). **Step 5:** chạy toàn bộ test Task 2–4 → PASS.
- [ ] **Step 6:** Commit `feat(presale): API đăng ký / gia hạn / duyệt đăng ký KH + phạm vi xem danh sách`.

### Task 5: Nhắc hết hạn hằng ngày

**Files:**
- Create: `hrm-api/app/Console/Commands/Assign/RemindCustomerRegisterExpiryCommand.php` (khuôn `AutoCloseProspectiveProjectsCommand`)
- Modify: `hrm-api/app/Console/Kernel.php` (hằng ngày 07:30, `withoutOverlapping()`)
- Test: `hrm-api/Modules/Assign/Tests/Feature/CustomerRegisterRemindTest.php`

**Interfaces — Produces:** `assign:remind-customer-register-expiry {--dry-run} {--register=}`. Chọn đăng ký `today <= expired_date <= today + N` (N = cấu hình theo công ty của người đăng ký, thiếu ⇒ 3), CHƯA có lịch sử `remind` với `new_value.expired_date` = hạn hiện tại ⇒ chuông + push cho `employee_id`, deep-link `/assign/report/customer-registers?register_id={id}`, ghi lịch sử `remind`. Ghi chú: tên KH, hạn, "Gửi gia hạn sớm — yêu cầu đang chờ duyệt không giữ hạn".

- [ ] **Step 1:** Test: `test_reminds_within_window_once`; `test_reminds_again_after_extension`; `test_skips_expired_and_far_registers`; `test_catch_up_run_still_reminds`.
- [ ] **Step 2:** FAIL. **Step 3:** cài đặt. **Step 4:** PASS. **Step 5:** commit `feat(presale): nhắc hết hạn đăng ký khách hàng hằng ngày`.

### Task 6: FE — popup đăng ký ở Báo giá và Dự án TKT

**Files:**
- Create: `hrm-client/components/assign/customer-register/RegisterCustomerModal.vue` (`V2BaseModal`, `unsavedModalMixin`)
- Modify: `hrm-client/pages/assign/quotations/index.vue` (cột Hành động), `pages/assign/quotations/_id/index.vue` (`V2Footer` `#custom-actions`), `pages/assign/prospective-projects/_id/index.vue` (+ `index.vue` nếu có cột Hành động)

**Interfaces — Consumes:** API Task 4. Props `{ visible: Boolean, sourceType: 'quotation'|'prospective_project', sourceId: Number }`, emit `saved({ mode })`.
Popup: Số báo giá / Mã dự án, Khách hàng, Người đăng ký (chỉ đọc); Người liên hệ (`V2BaseSelectInModal` bắt buộc khi KH tổ chức + nguồn báo giá, điền `suggested_contact_id`; nguồn dự án chỉ đọc); Thời hạn (ngày) số nguyên ≥ 1 điền `default_days`, dòng xám "Khác {default_days} ngày phải qua Trưởng phòng → BGĐ duyệt"; Ghi chú bắt buộc ≤ 255. Nút "Đăng ký" (thành "Gửi duyệt" khi khác mặc định). Toast: "Đăng ký khách hàng thành công" / "Đã gửi yêu cầu duyệt thời hạn đăng ký".

- [ ] **Step 1:** Cài đặt; nút ẩn khi `!can_register_customer`, danh sách và chi tiết cùng cờ.
- [ ] **Step 2:** Playwright (`playwright-b`, 1366px, chờ ≥ 3s): báo giá Trúng thầu của mình có nút; KH tổ chức bỏ trống người liên hệ ⇒ đỏ ô; đăng ký mặc định ⇒ dòng mới ở danh sách đăng ký; đổi 45 ngày ⇒ phiếu ở tab Phiếu yêu cầu; dự án TKT đăng ký được. Chụp và XEM ảnh. Đóng browser.
- [ ] **Step 3:** Commit 2 repo `feat(presale): nút Đăng ký khách hàng ở báo giá và dự án TKT`.

### Task 7: FE — danh sách 2 tab, Gia hạn, Duyệt, Lịch sử, In, Excel

**Files:**
- Modify: `hrm-client/pages/assign/report/customer-registers/index.vue` (vỏ 2 tab; tab đăng ký giữ `columnScreenKey`, bộ lọc cũ)
- Create: `pages/assign/report/customer-registers/components/RegisterListTab.vue`, `RequestListTab.vue` (bộ lọc tab lưu localStorage khoá riêng — khuôn `pages/assign/my-job/components/CustomerDemandsTab.vue`)
- Create: `components/assign/customer-register/ExtendRegisterModal.vue`, `RequestDetailModal.vue`, `CustomerRegisterHistoryModal.vue` (khuôn `components/assign/quotation/QuotationHistoryModal.vue`, skill `entity-history`)
- Modify: `components/subsystem-menu/presale.js` (bỏ gate quyền mục menu — phạm vi do BE)

**Interfaces — Consumes:** API Task 4. `?register_id=` (deep-link) ⇒ lọc đúng dòng + mở Gia hạn nếu `can_extend`; `?tab=requests&pending_mine=1` ⇒ tab phiếu lọc chờ tôi duyệt.
- Tab Đăng ký: thêm cột Nguồn (link), Trạng thái (`V2BaseBadge`), Hành động Gia hạn (`can_extend && !has_pending_extension`) / Lịch sử; ô lọc Người đăng ký ẩn khi `!meta.can_view_all`; toolbar In danh sách (`$printPreview`, khuôn `pages/assign/report/customer-development/index.vue`), Xuất Excel, Cấu hình cột.
- Tab Phiếu yêu cầu: cột theo spec §5.7, sort Ngày tạo giảm dần, lọc Trạng thái / Loại / Người tạo / "Chờ tôi duyệt"; hành động Xem, Duyệt (`can_approve`), Từ chối (`can_reject`, popup lý do bắt buộc), Lịch sử; In + Xuất Excel; cấu hình cột `columnScreenKey` mới `customer_register_requests`.
- Popup Gia hạn: Khách hàng, Hạn hiện tại, Số ngày gia hạn (≥ 1, bắt buộc), Hạn mới dự kiến (chỉ đọc, `max(hạn, hôm nay) + số ngày`), Lý do (bắt buộc); nút "Gửi duyệt".

- [ ] **Step 1:** Cài đặt.
- [ ] **Step 2:** Playwright đủ luồng: NV gửi gia hạn → TK quyền TP duyệt → TK BGĐ duyệt ⇒ hạn đổi + lịch sử đủ; Từ chối có lý do; In xem trước; Xuất Excel đọc lại file; không quyền Xem chỉ thấy của mình; deep-link `?register_id=`. Cấp quyền tạm rồi gỡ. Chụp + XEM ảnh 2 tab, 3 popup, bản in ở 1366px. Đóng browser.
- [ ] **Step 3:** Commit 2 repo `feat(presale): danh sách đăng ký KH — tab phiếu yêu cầu, gia hạn, duyệt, lịch sử, in`.

### Task 8: Rà soát cuối + tài liệu

- [ ] Đối chiếu ngang 2-3 màn HRM cùng loại (skill `erp-to-hrm-screen` Bước 5b), ghi "đã bám màn X ở khối Y".
- [ ] Tự kiểm: grep HTML thô trong file FE mới rỗng; `toLocaleString('vi-VN')` cho số rỗng.
- [ ] Toàn bộ test `Modules/Assign/Tests/Feature/CustomerRegister*` PASS.
- [ ] ERP không đổi: `git -C TanPhatDev status` sạch; đăng ký mới từ HRM hiện ở ERP `CustomerRegister::searchByFilter` (script đối chiếu).
- [ ] Ghi chú deploy: migration (3 bảng + cột cấu hình nếu chốt), `permission:catalog-sync`, lịch `assign:remind-customer-register-expiry`, admin cấp 2 mã duyệt.
- [ ] Cập nhật spec nếu lệch, STATUS, checkpoint. **Hỏi user** trước khi merge / push.

## Ngày 26/11/2026 (@junfoke) — tiến độ Giai đoạn 2
- [x] 26/11/2026 — Hoàn thiện spec Giai đoạn 2 (Phương án A: ERP giữ nguyên, phiếu chờ duyệt ở bảng mới HRM; đăng ký từ báo giá HRM Đã duyệt/Trúng thầu, KH tổ chức bắt buộc chọn người liên hệ; từ dự án TKT chưa Đóng/Kết thúc; khác thời hạn mặc định hoặc gia hạn ⇒ duyệt TP → BGĐ; nhắc hết hạn trước 3 ngày; màn danh sách 2 tab) — agent đọc kiểm, user chốt 2 câu hỏi và DUYỆT spec; viết plan 8 task (phần "Giai đoạn 2" ở trên).
- [ ] 26/11/2026 — Thực thi plan trong session (executing-plans + TDD), worktree `dang-ky-khach-hang` (tách `develop`, 2 repo): Task 1 code xong (migration 3 bảng, entity, 2 mã quyền duyệt, ô cấu hình), 4/5 test qua, test còn lại chờ tạo bảng ⇒ **dừng hỏi user trước khi chạy migration** local. Chưa commit.
