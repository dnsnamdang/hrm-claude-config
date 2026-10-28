# Meeting — hợp đồng API cho app (trích từ hrm-api, 22/10/2026)

# Meeting module API contract (for reuse by the Flutter app)

All paths start with `/api`. The meeting routes are pulled in by `Modules/Assign/Routes/api.php:1481` (`require .../Routes/Meeting/api.php`) under `auth:api`. None of the `v1/assign/meeting/*` routes has a `checkPermission` middleware. Access is checked inside the controller instead.

Three files hold most of what is cited below:
- **Controller:** `/Users/manhcuong/Desktop/dns/HRM/hrm-api/Modules/Assign/Http/Controllers/Api/V1/MeetingController.php`
- **Service:** `/Users/manhcuong/Desktop/dns/HRM/hrm-api/Modules/Assign/Services/MeetingService.php`
- **Entity:** `/Users/manhcuong/Desktop/dns/HRM/hrm-api/Modules/Assign/Entities/Meeting/Meeting.php`

---

## 0. Response envelopes (they differ between endpoints)

| Helper | Shape | Used by |
|---|---|---|
| `responseSuccess($d)` (`app/Http/Controllers/Api/Traits/ResponseTrait.php:28`) | `{meta:{code,message,total}, data:<d>}` | show, store, update, change-status, calendar, attendance-*, getList* |
| `responseJson(msg,code,d)` (`ResponseTrait.php:125`) | `{code, message, data}` (HTTP status = code) | 423/400 business errors, investment-scopes, print, prospective-project and contract options |
| `responseErrors(code,msg)` | `{meta:{code,message}, data:null}` | 403/404/500 |
| `apiGetList(Resource::apiPaginate())` (`ResponseTrait.php:161`, `Modules/Assign/Transformers/ApiResource.php:20`) | `{code:200, message:"success", data:[...], links:{first,last,prev,next}, meta:{current_page,from,last_page,path,per_page,to,total}}` | index, my-job, catalog indexes |
| FormRequest validation failure (`app/Http/Requests/ApiBaseRequest.php:34`) | HTTP **400** `{meta:{code:400, message:{field: firstMsg}}, data:{field:[msgs]}}` | store/update |
| `ValidationException` thrown from the service (re-thrown) | Laravel default HTTP **422** `{message, errors:{field:[...]}}` | store/update (investment_demands guard, expired temp file) |

---

## 1. Constants

**Meeting status** (`Meeting.php:192-196`, names at `:258`, colors at `:225`)

| value | name | meaning |
|---|---|---|
| 0 `DANG_TAO` | Đang tạo | Draft. Only the creator or host sees it in the list. |
| 1 `LEN_LICH` | Lên lịch | Scheduled |
| 2 `CHOT_LICH` | Chốt lịch | Confirmed |
| 3 `HOAN_THANH` | Hoàn thành | Completed (locked) |
| 4 `HUY` | Hủy | Cancelled (locked) |

**Other enums**

- **Mode** `mode_id` (`:234`): 1 = Trực tiếp (in person), 2 = Online.
- **Member type** (`meeting_employees.type`): 1 = company side (`company_members`), 2 = customer side (`customer_members`).
- **Attendance** `attendance_status` (`MeetingEmployee.php:21-30`):
  - 0 = pending
  - 1 = present (có mặt)
  - 2 = absent with reason (vắng có lý do)
  - 3 = absent without reason (vắng không lý do)
  - Self-confirm only accepts 1 or 2.
- **Attachment type** (`MeetingAttachment.php:18-21`): 1 = report documents (tab Biên bản), 2 = preparation documents (tab Thông tin).
- **Report proposer/executor type** (`MeetingReport.php:17`): 1 = company, 2 = customer.
- **MeetingType:**
  - status 1 = active, 2 = locked.
  - `code = 'HOP_TIM_HIEU_GIOI_THIEU_SP'` turns on the survey block.
  - `target_type`: 1 = prospective project (Dự án TKT) required, 2 = contract required (`MeetingType.php:12-40`).
  - `has_customer`: customer-side fields are required when true.
- **Meeting code** is generated `[Company].MET.[KH|NB].[YY].[NNNN]` (`Meeting.php:925`).

---

## 2. Permissions (in the Entity, not middleware)

| Method | Rule | Gates |
|---|---|---|
| `canView()` `:647` | creator, host, company member, the "Xem danh sách meeting theo tổng công ty / công ty / phòng ban / bộ phận" permissions, or several report-scope rules | show (403) |
| `canManage()` `:618` | `created_by == me` only | change-status, delete |
| `canEdit()` `:585` | canManage or host | update |
| `canDelete()` `:606` | canManage and status = 0 | delete |
| `canBookRoom()` `:598` | canEdit and status is 1 or 2 | room booking button |
| `completeBlockedReason()` `:358` | status must be 1 or 2, and now ≥ start_date | complete |
| `cancelBlockedReason()` `:384` | status must be 1 or 2, and now < start_date | cancel |
| `attendanceConfirmBlockedReason()` `:843` | user is a company member, status is 1 or 2, and now < start_date | self-confirm |
| `isReportLocked()` `:496` | status is 3 or 4, or (status is 1/2 and now > end_date + lock_days) | minutes tab locked |

The report deadline is `end_date + lock_days`. `lock_days` comes from `GeneralRegulation.meeting_report_lock_days` and defaults to 1 day. The warning lead time defaults to 3 hours (`:189,424-470`). A cron job auto-cancels overdue meetings (`MeetingService.php:1766`).

---

## 3. Routes: `v1/assign/meeting`

### 3.1 `GET /api/v1/assign/meeting` (index)
`MeetingController.php:92`, criteria `Modules/Assign/Repositories/Criteria/MeetingCriteria.php`.

**Scope**
- Drafts are visible only to their creator or host.
- Other meetings: the permission-scoped id set, OR I created it, OR I host it, OR I am a company member.

**Query params**
- `keyword` (code/name LIKE), `code`
- `status` (int, `isset`, so 0 is valid), `meeting_type_id`, `mode_id`
- `customer_id`, `project_id` (prospective project)
- `company_id`, `department_id`, `part_id`
- `employee_create` (employee_info_id), `created_by`, `updated_by` (employee id)
- `has_minutes`: 1 = has reports, 2 = none
- `from_date` → `start_date >= from_date`
- `to_date` → `end_date <= to_date`. This is "fully inside" filtering, so send `YYYY-MM-DD 23:59:59`.
- `is_assign_business`
- `sort_field`: `start_date|startDate|created_at|createdAt|updated_at|updatedAt|code|meetingCode|name|meetingName`
- `sort_dir`: `asc|desc`. Default is `created_at desc, id desc`.
- `per_page` (default 10), `page`

There is no "mine/all" flag. For "mine", use `created_by=<my employee id>`, or use the calendar or my-job endpoints.

**Row fields** (`MeetingResource.php`)
- Identity and type: `id, name, code, meeting_type_id, meeting_type_name, has_customer`
- Mode and place: `mode_id, mode_name, mode_color, online_link, location, meeting_room_id, meeting_room_name`
- Time:
  - `start_date` and `end_date` come back already formatted by `Helper::formatDate` (date only, no time).
  - `start_time` and `end_time` are `H:i`.
  - `duration_minutes`
- Customer: `customer` (full customer object with `contacts`, phone masked), `customer_id, customer_name, customer_code, customer_contact_{id,name,code,phone,role}`
- Content: `content`
- Audit: `creator, updater_name` ("Name - DeptCode"), `created_at, updated_at` (`d/m/Y H:i`)
- Status: `status, status_name, status_color`
- Members: `has_minutes` (bool), `company_members[], customer_members[], company_member_count, customer_member_count`
- Children: `reports[], projects[], attachments[]`, `prepare_attachments` (only when loaded)
- Unused here: `solution_version_code, module_version_code`
- Report deadline: `report_deadline` (`d/m/Y H:i`), `report_deadline_raw, is_report_locked, is_report_pending, report_lock_days, report_warning_hours`
- Flags: `can_edit, canEdit, can_manage, can_book_room`
- Cancel/complete: `cancel_reason_id, cancel_reason_text, can_complete, complete_blocked_reason, can_cancel, cancel_blocked_reason`

### 3.2 `GET /api/v1/assign/meeting/calendar` (`:149`)
- **Scope:** meetings where I am in `company_members` (the host is always auto-added). Drafts appear only if I created them. Criteria: `MeetingCalendarCriteria.php`.
- **Params:** `from_date`, `to_date` (overlap filter: `COALESCE(end,start) >= from AND start <= to`, see `MeetingCalendarRangeCriteria.php`), `meeting_type_id`, `status`.
- **Paging:** none. Sorted by start_date.
- **Response:** `{meta, data:[{id,name,code,meeting_type_id,meeting_type_name,status,status_name,start_date,end_date (raw Y-m-d H:i:s),mode_id,location,online_link,customer_name}]}`

### 3.3 `GET /api/v1/assign/meeting/{id}` (show)
`:190`, `MeetingService::getDataForShow` `:943`, `MeetingTransformer.php:99`.

- 403 if `!canView()`.
- A non-existent id crashes with 500, because `$entity->id` is read on null at `MeetingService.php:952`.
- Response: `{meta, data:{...}}`

**Basic fields**
- `id, name, code, meeting_type_id, meeting_type_name, meeting_type_code, is_customer_meeting` (bool: internal vs. external classification)
- `mode_id, online_link, location, location_lat, location_lng, location_input_mode`
- `meeting_room_id`, and `meeting_room`, which is `null` or `{id,code,name,location,is_locked,booking_id,booking_code,booking_status,booking_status_text,booking_status_color,reject_reason}`

**Time**
- `start_date, end_date`: raw `Y-m-d H:i:s`
- `start_time, end_time`: `H:i`
- `duration_minutes`

**Host and audit**
- `host_employee_id, host_name`
- `created_by, creator, creator_label, created_at` (`d-m-Y`), `created_at_full` (`d-m-Y H:i`)
- `updated_by, updater, updater_label, updated_at` (`d-m-Y H:i:s`)

**Customer**
- `customer` (object or null), `customer_id, customer_name, customer_code`
- `customer_contact_{id,name,code,role}`, and `customer_contact_phone`, which is masked to `"-"` without permission

**Content**
- `content` (legacy)
- `note`: the objective/content field (Mục tiêu / Nội dung), HTML
- `conclusion`: HTML

**Status and permission flags**
- `status, status_color`
- `can_manage, can_edit, canEdit, can_book_room`
- `can_complete, complete_blocked_reason, can_cancel, cancel_blocked_reason`
- `is_report_locked, is_report_pending, report_deadline, report_deadline_raw, report_lock_days, report_warning_hours`
- There is **no** `is_can_delete` flag. Derive it as `can_manage && status==0`.

**Attendance**
- `attendance_confirm`: `{is_member, can_confirm, blocked_reason, my_status, my_note}` (`Meeting.php:871`)
- `company_members[]`: `{id, meeting_id, employee_id, name, role, phone, type:1, attendance_status, attendance_note, sort_order, created_at, updated_at, employee_info_id, employee_code, department_code}`
- `customer_members[]`: the same columns with `type:2`, phone masked

**Minutes** (`reports[]`)
- `{id, meeting_id, content, solution, proposer_id, proposer_name, proposer_type, executor_id, executor_name, executor_type, expected_deadline}`
- `executors:[{id,name,type}]`
- `assigned_task_count`
- `assigned_tasks:[{id,code,title,status,status_text}]`

**Projects** (`projects[]`, a flattened prospective project, `MeetingService.php:979-1097`)
- `id, prospective_project_id, code, name, status, status_name, status_color`
- `form_template_id, form_template_snapshot_id`
- `answers` (form answers)
- `solution_id/name, solution_module_id/name`
- `scope_name, main_sale_employee_label`
- plus about 50 customer and project fields

**Files**
- `attachments[]` (type 1) and `prepare_attachments[]` (type 2): `{id, meeting_id, type, name, file, file_name, file_size, file_path, created_at,...}`

**Survey**
- `has_investment_demand, has_maintenance_demand`
- `investment_demands[]`: `{id, internal_business_scope_id/name, scope_id, scope_name, expected_amount, expected_start_date, status, status_text, status_color, prospective_project_id, owner_employee_id, ...}`
- `investment_scopes[]`: `{internal_business_scope_id, internal_business_scope_name, position}`

**Cancellation**
- `cancel_reason` (free-text note), `cancel_reason_id, cancel_reason_name`
- `cancel_reason_text` ("Name — note")
- `cancelled_at` (`d/m/Y H:i`), `cancelled_by_name`

**Contract and project link**
- `has_prospective_project`, `contract_id`
- `contract`: `{id, code, customer_name, status_name, status_color}` or null

### 3.4 `POST /api/v1/assign/meeting` (store, `:207`)
Request class: `MeetingCreateApiRequest` (`Modules/Assign/Http/Requests/Meeting/MeetingCreateApiRequest.php`).

**Top-level fields** (the whitelist is at `:223-254`)

| field | type | rule |
|---|---|---|
| `name` | string ≤255 | **required** |
| `meeting_type_id` | int | **required**. 423 if the type is missing or locked (`:209-218`). |
| `status` | int 0/1/(2) | not validated. FE sends 0 (draft) or 1 (Lưu và Lên lịch). |
| `start_date` | datetime | **required**, ≥ now |
| `end_date` | datetime | **required**, ≥ now and > start |
| `host_employee_id` | int | **required**, must exist in employees |
| `mode_id` | 1 / 2 | not validated |
| `location` | string | required only when status ≥ 2, mode = 1, and no `meeting_room_id` |
| `meeting_room_id` | int | nullable, must exist in meeting_rooms. A model hook creates the room booking. |
| `online_link` | url | nullable, url |
| `location_lat`, `location_lng`, `location_input_mode` | – | not validated |
| `is_customer_meeting` | bool | optional; inferred from `type.has_customer` if missing |
| `customer_id` | int (merged `customers` table) | if the customer is an individual (`customer_type` 1) registered by another sales rep, the error goes on `customer_id` |
| `customer_type` | 1 = individual | used for validation only |
| `customer_name`, `customer_code` | string | `customer_name` is **required if type.has_customer** |
| `customer_contact_id`, `customer_contact_name`, `customer_contact_code`, `customer_contact_phone`, `customer_contact_role` | – | name and phone are required when the customer is a business (`customer_type` ≠ 1). Phone regex `^0[0-9]{9,11}$`. |
| `contract_id` | int | required when `type.target_type = 2`. The contract must not be status draft or liquidated, and must belong to the same customer (`ValidatesMeetingTarget.php:692`). |
| `content`, `note`, `conclusion` | HTML string | `conclusion` is `required_if:status,3` |
| `has_investment_demand`, `has_maintenance_demand` | bool | survey type only |
| `send_notification` | bool, default true | only affects report-executor notifications on store |

**Nested arrays** (each block is replaced in full when present; see 3.5)
- `company_members` (**required array**, so it cannot be empty): `[{employee_id?, name*, role?, phone?, attendance_status?, attendance_note?}]`. Array order becomes `sort_order`. The host is auto-appended if missing (`MeetingService.php:94`).
- `customer_members` (when has_customer): `[{id?, name*, role?, phone?, attendance_status?, attendance_note?}]`
- `reports` (minutes rows): `[{content* ≤1000, solution? ≤2000, proposer_type 1|2, proposer_id, proposer_name, executor_name*, executors:[{id,name,type}], expected_deadline* (≥ today)}]`
  - The server rebuilds `executor_name/id/type` from `executors`, but `executor_name` is still validated as required.
  - When `proposer_type=2`, `proposer_name` must exactly match a `customer_members[].name`. Otherwise the request fails with 500 (`MeetingService.php:183-185`).
- `projects` (when has_customer): `[{prospective_project_id*, solution_id?, solution_module_id?, form_template_id?, form_template_data?, answers?{localId:value, "<localId>_note":...}}]`. When `target_type=1` at least one is required, project status must be 2–10, and the project must belong to the same customer.
- `attachments` / `prepare_attachments`: `[{name* ≤255, file_path (URL from upload), file_name, file_size}]`
- `investment_demands` (survey type only): `[{scope_id* distinct, scope_name, internal_business_scope_id, internal_business_scope_name, expected_amount ≥0, expected_start_date ≥ today}]`
- `investment_scopes`: `[{internal_business_scope_id* distinct, internal_business_scope_name}]`

The legacy `employees.*` rules are dead and can be ignored.

**Response:** the full show payload (`respondAfterCommit` at `:888`). If building the transformer fails after commit, you get `{meta, data:{id, code}}` instead.

**Drafts:** you **cannot** save a draft with only a few fields. Status 0 needs the same required set: name, type, start/end ≥ now, host, ≥1 company member, and customer_name for customer types. Only `location` (status ≥ 2) and `conclusion` (status 3) are conditional.

### 3.5 `POST /api/v1/assign/meeting/{id}` (update, `:536`)
Request class: `MeetingUpdateApiRequest`.

**Rejections**
- 403 if `!canEdit()`.
- 423 if the current status is 3 or 4 (`:557`).
- 423 if status is 1/2 and the report is overdue (`:561`).
- 423 if the user changes to a locked or missing meeting type.

**Rules (same as store, with these differences)**
- `status` is **required**.
- `start_date`:
  - must be ≥ now if the current status is 1;
  - otherwise it must be ≥ the meeting's `created_at`.
- `end_date` must be ≥ start.
- `reports.*.expected_deadline` must be ≥ today only while the current status is 1.
- For the survey type, `has_investment_demand` and `has_maintenance_demand` are `required_if:status,3`. At status 3 with has_investment_demand=1, at least one scope and one demand are required, and each demand needs `expected_amount` and `expected_start_date` (`MeetingUpdateApiRequest.php:476-544`).
- Phone `"-"` (the mask) is restored to the stored value (`:261`).

**Replace semantics: per block, not a whole-form replace**
- **Scalars:** only keys you send are written (`$request->only`). Validation still forces name, type, start, end, host, status, and company_members.
- **`company_members`:** always required, so it is always fully replaced (delete everything, then insert).
- **`customer_members`, `reports`, `projects`:** if the key is absent or null, the block is left untouched. If present, it is fully replaced. `projects` deletes links that are not in the list.
- **`attachments`, `prepare_attachments`:** absent means untouched. Present (including an empty string) means replace, and removed S3 files are deleted after commit (`:877`).
- **Pitfall: `investment_demands`, `investment_scopes`.** If the stored `has_investment_demand` is not 1, all rows are deleted. If it is 1 and the key is **absent**, it is treated as `[]` and all rows are deleted. Removing a demand that is linked to a project throws 422. Always send these for the survey type.
- **`contract_id`:** recomputed on every save. If the type is not a contract type it becomes null, unless the type is unchanged and a contract is already stored.

**Completing through update (`status=3`)**
1. `completeBlockedReason` must be null (status 1/2 and started); otherwise 400.
2. Every company and customer member must have `attendance_status` in 1–3; otherwise 400 "Vui lòng hoàn thành điểm danh…".
3. `conclusion` is required.
4. The survey rules above apply.

On completion the server also snapshots demand due days, creates the service demand, and records demands.

**Response:** the show payload.

### 3.6 `POST /api/v1/assign/meeting/{id}/change-status` (`:328`)
- **Body:** `status` (int), `cancel_reason_id` (required when status = 4, must be an active reason), `cancel_reason` (optional note).
- **Checks:**
  - 404 if not found.
  - 403 if `!canManage()` (creator only).
  - status 3 → 4 returns 400.
  - Cancel: `cancelBlockedReason` must be null, meaning status 1/2 and **before** start; otherwise 400.
- **Writes:** `cancel_reason_id, cancel_reason, cancelled_at, cancelled_by`.
- **Gap:** for `status=3` this endpoint runs **no** attendance, conclusion, or start-time checks. The code comment says it is meant only for cancel. Use update to complete.
- **Response:** the show payload.

### 3.7 Delete: `POST /api/v1/assign/meeting/{id}/delete` (`:740`)
- 403 unless `canManage()`. 400 unless status = 0.
- Deletes members, reports, executors, attachments (and S3 files), project links, and form answers.
- Response: `{meta, data:null}`.

### 3.8 Attendance self-confirm (`:437`, `:472`)
- **`GET .../attendance-confirm-states?meeting_ids=1,2,3`** (max 50 ids)
  - Response: `{meta, data:{"<id>":{is_member, can_confirm, blocked_reason, my_status, my_note}}}`
  - Empty input returns `data: []`.
- **`POST .../{id}/attendance-confirm`**
  - Body: `attendance_status` (1 or 2), `attendance_note` (required when 2).
  - Errors: 403 if not a company member; 400 with `blocked_reason` text (wrong status, or already started); 400 for an invalid status or a missing note.
  - Response: `{meta, data:{meeting_id, employee_id, attendance_status, attendance_note}}`.
  - It updates only my own row (`MeetingService.php:1587`). Choosing 1 clears the note. No notification is sent.
- **Host roll call** (attendance for everyone) is not a separate endpoint. It goes through update, using `company_members[].attendance_status` and `customer_members[].attendance_status`.

### 3.9 Other meeting routes
| Route | Params | Response |
|---|---|---|
| `GET .../investment-scopes` (`:808`) | `include_ids`, `include_group_ids` (array or CSV) | `{code,message,data:[{id,name,is_locked,industry_groups:[{id,name,is_locked}]}]}` |
| `GET .../task-options` (`:1165`) | `keyword`, `include_id`, `limit` ≤200 (default 50) | `{meta,data:[{id,code,name,start_date}]}`, my meetings only |
| `GET .../getListCustomer` (`:914`) | `q` | `{meta,data:[customer + contacts[] + full_address]}`, limit 20, `is_customer=1` |
| `GET .../getListEmployee` (`:966`) | `keyword, department_id, part_id, company_id, working_position_id, employee_role_id, per_page, page, get_all=1` (≤5000, not paginated) | `{meta,data:<paginator {current_page,data:[{id,code,name,telephone,email,working_position_name,department_name,department_code,part_name,title_name}],total,...}>}` |
| `GET .../getListMeetingProject` | – | `{meta,data:[{id,name}]}` (all projects) |
| `GET .../customer-history` (`:1044`) | `customer_id`* plus `keyword,status,mode_id,meeting_type_id,from_date,to_date,prospective_project_id,per_page` (default 10) | paginator rows `{id,code,name,start_date,end_date ("d/m/Y H:i"),meeting_type_name,mode_id,status,status_name,projects[{id,code,name}],project_name,has_report,cancel_reason}` |
| `GET .../export` | same filters as index, plus `fields` | `.xlsx` download |
| `POST .../addContact` (`:1200`) | `name*`, `phone*` (regex), `role*`, `customer_id` (not validated) | `{meta,data:{id,fullname,role,phones,email}}` |
| `GET .../{id}/print` (`:1347`) | `only_present=1` prints only members marked present | `{code,message,data:{template:"<html>"}}` (print template `BIEN_BAN_CUOC_HOP`) |
| `POST .../{id}/project/{projectIndex}/save-form-answers` (`:1398`) | body `{form_template_id?, form_template_data?, answers:{...}}`. `projectIndex` is the 0-based order of project links by id. | `{code,message,data:{form_template_snapshot_id}}`. **No permission check.** It also moves a project in status 1 to status 2. |

---

## 4. Related routes in `Modules/Assign/Routes/api.php` (prefix `/api/v1`, `auth:api`)

| Route | Middleware | Params | Response |
|---|---|---|---|
| `GET /assign/prospective-projects/options-for-meeting` (`:370`, ctrl `ProspectiveProjectController.php:60`, svc `ProspectiveProjectService.php:456`) | none | `search` (code/name), `customer_id`, `page`, `per_page` (default 20, max 50) | apiGetList rows `{id,code,name,customer_id,customer_code,customer_name,status,status_name,status_color,is_parent}`. Scope: status 2–10 and (I created it, or I am the solution employee, or I am a support-department employee) (`ProspectiveProject.php:142`). |
| `GET /assign/prospective-projects/options-for-meeting/{id}` (`:371`) | none | – | `{code,message,data:ProspectiveProjectResource}` (id, code, name, status*, customer_*, customer_contact_*, customer_benefit_*, scope/industry/application ids and names, budget, dates, solution_*, can_edit, can_delete, …). 404 if outside scope. |
| `GET /assign/prospective-projects/meeting-options` (`:377`, svc `:1029`) | none | `customer_id`, `project_id` | `{code,message,data:[{id,code,name,customer_id,customer_name,status,is_personal_customer,is_linked}]}`. This is for the project form, not the meeting form. |
| `GET /assign/contracts/for-meeting` (`:826`, `ContractController.php:243`) | none | `customer_id`, `include_id` | `{code,message,data:[{id,code,customer_id,customer_code,customer_name,customer_contact_name,status,status_name,status_color}]}`. Excludes draft and liquidated contracts. No phone returned. |
| `GET /assign/customers/{id}/contacts` (`:192`, `CustomerService.php:1250`) | none | `phone` (exact match on one number) | `{code,message,data:[{id,fullname,role,phones,email,locked,locked_message}]}`. Returns only contacts I created, used in my projects/meetings/quotations, or registered. `locked` means another sales rep has registered the contact. |
| `POST /assign/customers/{id}/contacts` (`:194`) | `customerNotLocked` | `name, phone, role` (AddContactApiRequest) | `{code,message,data:{contact}}` |
| `GET /assign/meeting_types` (`:1048`) | **`checkPermission:Quản lý danh mục loại meeting\|Xem danh mục loại meeting`** | `name, keyword, status, has_customer (0/1), target_type (0/1/2), updated_from/to, created_by, updated_by, sort_field/dir, per_page` | apiGetList rows `{id,code,is_system,name,description,has_customer,has_customer_text,target_type,target_type_text,status,is_locked,status_text,created_at,updated_at,creator_name,updater_name,is_can_edit,...}` |
| **Use instead on mobile:** `GET /assign/meeting_types/getAll` (`:1049`) | none | `include_ids` (keeps locked types already in use) | `{code,message,data:[same shape]}`, active types only |
| `GET /assign/meeting_cancel_reasons` (`:1149`) | **`checkPermission:Quản lý danh mục lý do hủy cuộc họp\|Xem …`** | `keyword, status, created_by, updated_by, per_page` | apiGetList rows `{id,name,description,status,status_text,created_at,updated_at,creator_name,updater_name,is_can_edit,is_can_delete}` |
| **Use instead on mobile:** `GET /assign/meeting_cancel_reasons/getAll` (`:1148`) | none | – | `{code,message,data:[raw rows: id,name,description,status,...]}`, active only (status 1) |
| `GET /assign/my-job/meeting-upcoming-schedule` (`:1401`, `MyJobService.php:45`) | none | `keyword,status,meeting_type_id,project_id,customer_id,mode_id,has_minutes(1/other),updated_by,sort_field(start_date\|created_at),sort_dir` (default start asc), `per_page,page` | apiGetList of `MeetingResource` rows (see 3.1). Scope: status 1/2, I am a company member, and `now < start_date ≤ now + GeneralRegulation.meeting_due_days` (end of that day). |

The two catalog index routes require catalog-admin permissions that ordinary users probably lack. Use the `getAll` variants listed under each.

---

## 5. File uploads
There is no multipart upload inside the meeting store. The flow is two steps:
1. `POST /api/v1/files/upload` (Human module, `Modules/Human/Routes/api.php:260`, `FileController::uploadImage`), sent as multipart with `attachments[]` (files) and `temporary=1`. It returns `{meta, data:["https://...s3 url", ...]}` with URLs in the same order as the files.
2. Put each returned URL into `attachments[].file_path` or `prepare_attachments[].file_path`, along with `name`, `file_name`, and `file_size` supplied by the client.

On save, temporary URLs are moved to the permanent folder (`MeetingService.php:891`). An expired temporary file returns 422 on `attachments.N.file_path`.

---

## 6. Status flow and locking
- **Create:** status 0 (draft) or 1 (scheduled). Status 2 is not blocked by the server.
- **0 → 1 → 2:** via update. There is no transition guard, so any status value is accepted while the current status is 0–2.
- **1/2 → 3:** via update, with the guards in 3.5.
- **1/2 → 4:** via change-status. Creator only, before start, and a cancel reason is required. The cron also auto-cancels when minutes are overdue.
- **Delete:** status 0 and creator only.
- **Locks:**
  - At status 3 or 4 the whole form is read-only (update returns 423).
  - An overdue report also blocks update (423).
  - `is_report_locked` tells the minutes tab to go read-only.
  - There is no per-field lock flag. The only flags are `can_edit, can_manage, can_book_room, can_complete, can_cancel, is_report_locked, attendance_confirm.can_confirm`.

---

## 7. Notifications
Every notification payload includes `{url:'/assign/meeting/{id}/show', title, type:'meeting', id}`.

**Store**
- With status 1, all company members get "[MET] Tạo mới: …". With status 2, they get "[MET] Cập nhật: …". Both carry `attendance_confirm:true, meeting_id, meeting_start_date` (`MeetingService.php:1616`).
- Status 0 sends nothing.

**Update** (unless `send_notification=0`)
- If the status changed, the same status 1/2 notifications as on store are sent.
- If the status stayed at 1/2, notifications depend on what changed (`:1681`):
  - Time changed: remaining members get "Thay đổi lịch".
  - Members added: they get "Bạn được thêm vào cuộc họp".
  - Members removed: they get "Bạn đã được đưa ra khỏi cuộc họp".
- If the meeting is now status 3, internal report executors and proposers get "Bạn được giao N nhiệm vụ", with the url `?active_tab=reports` (`:1872`).

**Other actions**
- **Change-status to cancel:** every internal member gets "<name> đã bị <user> huỷ. Lý do: …" (`MeetingController.php:1243`).
- **Cron:** the creator gets a deadline reminder ("Nhắc báo cáo"). On auto-cancel, members and the creator get "Hủy: Quá hạn nhập biên bản" (`:1731`, `:1766`).
- **No notification:** attendance-confirm, delete, save-form-answers.

---

## 8. Backend issues found while tracing (things the mobile client must work around)
1. `GET /{id}` with an unknown id returns 500 instead of 404 (`MeetingService.php:952`).
2. A minutes row with `proposer_type=2` whose `proposer_name` does not match a customer member returns 500 (`MeetingService.php:185`).
3. On update, leaving out `investment_demands` or `investment_scopes` deletes them when `has_investment_demand=1` (`MeetingService.php:268`).
4. `change-status` with status 3 skips every completion guard (`MeetingController.php:328-399`).
5. In the status 1/2 notification text the mode ("Hình thức") part is always empty, because the code reads `$meeting->mode` but the column is `mode_id` (`MeetingService.php:1623`).
6. `save-form-answers` does no permission check (`MeetingController.php:1398`).
7. The index filter `to_date` compares against `end_date <= to_date`, so a date-only value drops meetings that end later that same day. Send `YYYY-MM-DD 23:59:59`.