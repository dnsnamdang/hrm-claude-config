# Meeting — nghiệp vụ màn web (trích từ hrm-client, 22/10/2026)

# Meeting feature (web): business behavior for the mobile port

All FE paths are relative to `/Users/manhcuong/Desktop/dns/HRM/hrm-client/`. BE paths are relative to `/Users/manhcuong/Desktop/dns/HRM/hrm-api/Modules/Assign/`.

**Before you start:**
- A mobile design for this already exists in `/Users/manhcuong/Desktop/dns/HRM/.plans/app-meeting-mobile/` (50 screens, delivered 16/09/2026). It was drawn before the "meeting by object" change of 08/10/2026, so it does not include the Contract (Hợp đồng) target. See §8.
- Three plan folders you named do not exist on disk: `meeting-form-redesign`, `meeting-chon-du-an-tkt` and `meeting-tab-du-an-nhan-su`. Code comments still refer to them. Their decisions can only be read from the code.

---

## 1. Screens

| Screen | File | Notes |
|---|---|---|
| List | `pages/assign/meeting/index.vue` | Smart filter panel, data table, row actions |
| Create | `pages/assign/meeting/create.vue` | Wraps `MeetingForm`. Saves with `POST assign/meeting` (:100), then goes back to the list |
| Edit | `pages/assign/meeting/_id/edit.vue` | Loads `GET assign/meeting/{id}`. If `can_edit===false` it redirects to `/show` (edit.vue ~:50). Saves with `POST assign/meeting/{id}` |
| Detail (view) | `pages/assign/meeting/_id/show.vue` | `MeetingForm :isShow=true` plus a History block (`SystemInfoSection entity-type="meeting"`) and printing |
| Print | `components/assign/meeting/MeetingPartsConfigModal.vue` then `MeetingPrintPreview.vue` | Two steps: choose parts (+ option "only present attendees"), then preview. Uses `GET assign/meeting/{id}/print` with print template `BIEN_BAN_CUOC_HOP` (MeetingPrintPreview.vue:6) |
| Excel export of minutes | `MeetingReport.vue:657` | Built on the client with ExcelJS |
| Collection-form print/input | `_id/survey-input.vue`, `_id/survey-print.vue` | For the TKT project's "Phiếu thu thập thông tin" |
| Calendar | `pages/assign/my-todo/components/calendar/WorkCalendarTab.vue` | `GET assign/my-todo/calendar` (:207). Drawer → `assign/meeting/{id}`. It is not under `/assign/meeting`. BE also has `GET assign/meeting/calendar` (`Routes/Meeting/api.php`) |
| My-job tab | `pages/assign/my-job/components/MeetingsTab.vue` | `GET assign/my-job/meeting-list` |

**Statuses** (`MeetingForm.vue:290`):

| Code | Name |
|---|---|
| 0 | Nháp / Đang tạo |
| 1 | Lên lịch |
| 2 | Đã chốt lịch |
| 3 | Hoàn thành |
| 4 | Hủy |

**Meeting code format:** `[Company].MET.[KH|NB].[yy].[seq]` (`Entities/Meeting/Meeting.php:917`).

### List page (`index.vue`)

**Quick search:** meeting code or name.

**Filters** (:495-549):
- Company / Department / Part
- Loại meeting
- Dự án tiền khả thi: `assign/meeting/getListMeetingProject`
- Khách hàng: remote search on `assign/customers/search`
- Hình thức: Trực tiếp / Online
- Trạng thái
- Biên bản: Đã lập / Chưa lập
- Người tạo, Người cập nhật
- Ngày họp từ / đến (the "from" date must be ≤ the "to" date)

**Data scope** depends on four permissions, "Xem danh sách meeting theo tổng công ty / công ty / phòng ban / bộ phận" (:836).

**Columns** (:620-786):
- STT
- Mã meeting (link to `/show`)
- Tên, Ngày họp, Thời lượng
- Loại, Hình thức (badge)
- Khách hàng (+ contact)
- Dự án TKT
- Địa điểm, Phòng họp
- Thành phần tham dự
- Trạng thái (badge; colour comes from BE)
- Biên bản: a "Xem biên bản" link, shown only when `has_minutes`
- Người tạo / Ngày tạo / Người cập nhật / Ngày cập nhật
- Hành động

**Header buttons:** Tạo meeting, Đăng ký phòng họp, Xuất Excel, column config.

**Row actions** (`getRowActions` :1187):

| Action | Visible when |
|---|---|
| Sửa | `status ∉ {3,4}` and `can_manage` |
| Xóa | `status==0` and `can_manage`. Calls `POST assign/meeting/{id}/delete` |
| In biên bản | Always |
| Tạo phiếu công tác khác | `status ∉ {3,4}` |
| Lịch sử | Always |
| Đăng ký / Đổi phòng họp | `can_book_room===true` |

**Inconsistency:** the list uses `can_manage` (creator only) to show Sửa (:1197), but the form and the BE use `can_edit` (creator **or host**). A host who did not create the meeting sees no Sửa in the list, yet can edit from the detail page.

---

## 2. Create/edit form: tabs → sections → fields

**Tabs** (`MeetingForm.vue:423`):
- **Thông tin**
- **Nhân sự tham gia** (with a count)
- **Biên bản**
- **Nhiệm vụ**: detail page only
- **Dự án TKT**: only when at least one project is attached

A tab that contains an error gets a red flag, and the form jumps to the first error.

### Tab Thông tin (`GeneralInfo.vue`)

The sections are numbered dynamically.

**① Loại meeting** (:9-30)

| Field | Req | Input | Source / rule |
|---|---|---|---|
| Phân loại họp | – | segmented: Đối tác / Nội bộ | Stored in `is_customer_meeting` (:839). It filters the type list by `has_customer`. Changing it clears a type that no longer matches (:1151) |
| Loại meeting | * | select with lock icon and info tooltip | `GET assign/meeting_types/getAll[?include_ids=current]` (:1309) |

**② Khách hàng & đối tượng** (:33-271)
- Shown when: scope is Đối tác and the form is editable, or the type has a customer, or the meeting already has a customer, project or contract (:867).
- It is locked with a note until a type is chosen (:877).

| Field | Req | Input | Source / rule |
|---|---|---|---|
| Khách hàng | * when the type has `has_customer` | Read-only picker. Opens `ChooseErpCustomerModal` (`GET assign/customers?status=1&all_business=1…`). After choosing, a customer card appears with actions Lịch sử meeting / Đổi / Bỏ chọn | Detail comes from `GET assign/customers/{id}?all_business=1` (silent on 403) (:2015). Then scope is filled from ERP. The first visible contact is auto-filled. "Thêm nhanh KH" (`QuickAddCustomerModal`) is shown only if `GET assign/customers/my-permissions` returns `.create` |
| Người liên hệ | Hidden for an individual customer (`customer_type==1`). The UI shows no `*`, but the BE requires name + phone for a business customer (`MeetingCreateApiRequest.php:139`) | Remote select | `GET assign/customers/{id}/contacts[?phone=]` (:2140). A contact marked `locked` (owned by another Sales) is rejected with a toast. Choosing a contact also adds a row to the customer-side members |
| Quick add contact: Họ tên / Chức vụ / SĐT | all * | inline form | `POST assign/meeting/addContact` (:2309) |
| Dự án TKT | * when `target_type==1` | multi remote select, plus a collapsible Giải pháp / Hạng mục per project | `GET assign/prospective-projects/options-for-meeting?search&customer_id&per_page=20` (:1379) and `/options-for-meeting/{id}` (:1390). Solutions come from `assign/solutions/getAll`. Disabled until a customer is chosen (:1028), and disabled when the form was opened from a project (`?project_id`) |
| Hợp đồng | * when `target_type==2` | single SearchPicker | `GET assign/contracts/for-meeting[?include_id]` (:1339). Filtered by the chosen customer. Choosing a contract first fills the customer and contact name (:1349) |

**③ Nội dung cuộc họp**

| Field | Req | Input | Notes |
|---|---|---|---|
| Tên meeting | * | text | "Gợi ý tên" button fills `[Type] Project/Contract – Customer` (:2129) |
| Mục tiêu / Nội dung (`note`) | – | rich text editor | |

**④ Thời gian, địa điểm & chủ trì**

| Field | Req | Input | Notes |
|---|---|---|---|
| Bắt đầu, Kết thúc | * | datetime | Past dates are blocked only on create or when status is 1 (:1246). BE: on create, start must be ≥ now and end must be after start. On update the `now` check applies only when status is 1; otherwise the date is compared with `created_at` (`MeetingUpdateApiRequest.php:86`) |
| Người chủ trì | * | select | Store `activeCompanyEmployeeOptions`. Defaults to the current user. Changing the host adds the new host to the company members and removes the old one (unless the old one is the creator) (:2246) |
| Hình thức | – | segmented: Trực tiếp (1) / Online (2) | |
| Link họp | – (must be a valid URL) | text | Only when mode is Online |
| Phòng họp | – | room box + "Đăng ký / Đổi phòng" and "Hủy đăng ký" | Booking needs a saved meeting, status ≥ 1 and not 3/4, and `can_book_room` (:721). Uses `BookingFormModal`, `meeting/rooms/bookable` and `POST meeting/room-bookings/unassign-meeting`. When blocked, a text reason is shown instead of the button (:728) |
| Địa điểm meeting | * only when mode is Trực tiếp and status ≥ 2 and no room (:451; BE `MeetingCreateApiRequest.php:43`) | segmented Nhập / Bản đồ: free text, or a GoogleMap / OSM picker | Hidden once a room is set. Switching the mode clears the value |

**⑤ Tài liệu chuẩn bị cho buổi họp** (`prepare_attachments`)
- `FileAttachmentTable` with temporary upload.
- Each row needs a name (`prepare_attachments.*.name` is required on the BE).

**Right column**
- Attendance confirm block: detail page only (§5).
- "Thông tin bản ghi": code, status, creator, dates.
- "Tóm tắt cuộc họp": a checklist with % of required items (:917).
- A cancelled meeting shows a red banner "Lý do hủy" (`MeetingForm.vue:31`).

### Tab Nhân sự tham gia (`MeetingParticipants.vue`)

**Phía Công ty**
- "Thêm nhân sự" opens `PopupStaff` (multi-select, whole group, via `getListEmployee`).
- Rows can be reordered by drag and drop.
- The host row has a "Chủ trì" badge and cannot be deleted.
- At least one member is required (BE `company_members required`).

**Phía Khách hàng**
- Only when `hasCustomer`.
- "Thêm dòng" adds a manual row: Họ tên * / Chức vụ / SĐT.
- The phone must match `^0[0-9]{9,11}$`.
- For an individual customer, the customer row is fixed: the name is locked and the row cannot be deleted.

**Attendance columns**
- Shown only when status is 2 or 3 (:269).
- Editable only on the edit page with status 2 (:273).
- Values: Có mặt (1) / Vắng có lý do (2) / Vắng không lý do (3) as segmented buttons, plus a free note.
- "Tất cả có mặt" button. The header shows count badges, which ignore the customer side for internal meetings.

### Tab Biên bản (`MeetingReport.vue`)

The tab opens with a deadline banner when the meeting has ended and minutes are still pending (`is_report_pending`):
- Yellow: "Hạn nhập biên bản …"
- Red, when `is_report_locked`: the meeting will be auto-cancelled (:537).

Sections:

1. **I–III Thông tin chung** – information only. These parts are added automatically when printing. In / Xuất Excel buttons appear only when `form.id` exists.
2. **IV/ Nội dung meeting**
   - **1/ Khảo sát nhu cầu khách hàng** – only for the system type `MEETING_TYPE_PRODUCT_INTRO` (see §4). Component `MeetingInvestmentSurvey.vue`:
     - Câu 1: Có/Không *
     - Câu 2 (if Câu 1 = Có): Lĩnh vực » Nhóm ngành, cascade multi-select *. Options from `optionsSelect/fetchInvestmentScopes`.
     - Câu 3: per selected industry group, Mức đầu tư (VNĐ) * + Thời gian khánh thành *
     - Câu 4: bảo trì Có/Không *
     - All required only on Hoàn thành (BE `required_if:status,3`, `MeetingUpdateApiRequest.php:171`).
   - **Các nội dung khác** * – a table of rows:
     - Nội dung / Vấn đề trao đổi * (max 1000)
     - Phương án xử lý (max 2000)
     - Người đề xuất (single, `PopupStaff`; company or customer staff)
     - Người thực hiện * (multi)
     - Hạn dự kiến * (date ≥ today)
     - Buttons: Thêm dòng / Xóa hết.
     - On the detail page each saved row has "Giao": it creates a task via `CreateTaskModal` and shows "Đã giao N nhiệm vụ".
   - **Tài liệu đính kèm** – rows of Tên * + File *. Allowed types: jpg/png/doc/xls/pdf. Uploaded immediately with `POST files/upload` (`temporary=1`).
3. **V/ Kết luận** * – rich text, required only on Hoàn thành (BE `required_if:status,3`).

### Tab Dự án TKT (`MeetingProject.vue`)

The tab is view-only, except for the collection form.

- One chip per attached project, each with two sub-tabs.
- **Thông tin chung**: a read-only summary.
  - Project fields: Mã, Tên, Ứng dụng, Nhóm ngành, NV KD, Quy mô, Phân loại đầu tư, Cách triển khai, Địa điểm.
  - Customer fields: Loại hình, Lĩnh vực, Người liên hệ.
  - "Xem chi tiết" opens the project.
- **Phiếu thu thập thông tin**:
  - The template is resolved with `assign/form-templates/find-by-criteria` (or by id or snapshot).
  - Rendered by `FormPreview`.
  - Buttons: Xem bản in nhập, Xem bản in, Lưu phiếu (`POST assign/meeting/{id}/project/{idx}/save-form-answers`, :904).
  - If the project has no application, a note says to set one.

---

## 3. Buttons by status (`MeetingForm.vue:304-416`)

Mapping from code names to footer labels: draft = "Lưu nháp", save = "Lưu", schedule = "Lưu và Lên lịch", confirm = "Lưu và Chốt lịch". A `reset` button is in the list but is never mapped to the footer, so "Làm mới" never shows.

| Context | Buttons |
|---|---|
| Create, or edit at status 0 | Lưu nháp, Lưu và Lên lịch, Lưu và Chốt lịch, Quay lại |
| Edit at status 1 | Lưu, Lưu và Lên lịch, Lưu và Chốt lịch, Hủy, Quay lại |
| Edit at status 2 | Lưu, Hoàn thành, Hủy, Quay lại |
| Edit at status 3 or 4 | Quay lại (and the BE returns 423 anyway) |
| Detail | Sửa (status ∉ 3,4), Xóa (status 0), Hủy (status 1,2), Tạo phiếu công tác khác (status ∉ 3,4), In (any saved meeting), Quay lại |

**Permission filters**
- Without `can_edit`, only Quay lại is shown.
- With `can_edit` but without `can_manage` (host who is not the creator), Hủy and Xóa are removed (:312-322).

**Disabled states with tooltips (flags from the BE)**
- Hoàn thành: `can_complete` / `complete_blocked_reason`.
- Hủy: `can_cancel` / `cancel_blocked_reason`.

**API per action**
- Lưu nháp, Lên lịch, Chốt lịch, Hoàn thành and Lưu all send the full form as one multipart payload. Only `status` changes (0/1/2/3).
  - Create: `POST assign/meeting`
  - Update: `POST assign/meeting/{id}`
  - Lên lịch also sends `send_notification:1` (:897).
- Lưu at status 1 keeps status 1.
- Lưu at status 2 when the time changed opens a confirm modal "Xác nhận thay đổi thời gian" ("…gửi lịch họp mới đến tất cả thành viên…") and then saves with status 2 (:1027-1041). This is the only "đổi thời gian" flow; there is no separate button.
- Hủy opens `CancelMeetingModal`:
  - Lý do: required select from `assign/meeting_cancel_reasons/getAll`. Error text: "Vui lòng chọn lý do hủy cuộc họp".
  - Ghi chú: optional, max 1000.
  - Calls `POST assign/meeting/{id}/change-status {status:4, cancel_reason_id, cancel_reason}` (:925).
- Xóa: confirm, then `POST assign/meeting/{id}/delete`.
- In: config modal, then preview.

**Validation on Hoàn thành**

The FE checks run first (`collectMissingForComplete` :1069). The toast is generic, "Vui lòng kiểm tra lại dữ liệu nhập", and each missing field gets the inline error "Bắt buộc phải nhập". The checks are:
- Every member has attendance 1, 2 or 3. Customer members count only when `hasCustomer`.
- Survey questions 1–4 (product-intro type only).
- At least one minutes row, and each row has content + executor + deadline.
- Each attachment row has a name and a file.
- Conclusion is filled.

The BE then checks:
- `completeBlockedReason`: status must be 1 or 2, and the start time must have passed. Message: "Chỉ được xác nhận hoàn thành khi cuộc họp đã bắt đầu" (`Meeting.php:358`).
- All members attended. Message: "Vui lòng hoàn thành điểm danh cho tất cả thành viên trước khi chốt biên bản và hoàn thành cuộc họp." (`MeetingController.php:643-654`).

**Cancel rule:** only at status 1 or 2, and before the start time. Message: "Cuộc họp đã đến giờ bắt đầu, không hủy được nữa" (`Meeting.php:384`).

**Draft rules are not relaxed:** the FE runs no validation on Lưu nháp (`validate()` is commented out, :773). The BE applies the same required rules to drafts: name, type, dates, host, company_members.

**Errors after a save:** 422 and 400 fill `formError` inline. 403 shows "Bạn không có quyền…". 423 shows the BE message.

---

## 4. Classification rules

**Customer vs internal**
- Comes from `meeting_type.has_customer`, mirrored in `is_customer_meeting`.
- For internal meetings:
  - Section ② is hidden.
  - The customer-side member table is hidden.
  - Customer attendance is not required.
- Switching to a type without a customer clears all customer fields and customer members, unless the type has a target or the meeting has projects / came from a project (:1171-1200).

**Online vs in-person**
- Online shows the Link họp field.
- In-person requires a location from status 2 (Chốt lịch) onward, unless a room is booked.
- A room can be used in both modes.

**Target type (`meeting_types.target_type`)**

| target_type | Meaning | Rules |
|---|---|---|
| 0 | None | – |
| 1 | Dự án TKT | `projects` required (BE `ValidatesMeetingTarget.php`). Projects must be in progress 2–10 and belong to the chosen customer. Error texts: "Vui lòng chọn Dự án TKT." / "…không ở tiến trình được gắn meeting." / "…không thuộc khách hàng đã chọn." |
| 2 | Hợp đồng | `contract_id` required. The contract must not be in status 3 (Đang tạo) or 10 (Đã thanh lý) and must belong to the same customer. Changing the type away from 2 clears the contract |

- The project picker is also shown, but not required, when the meeting already has projects or comes from `?project_id`. In the second case the picker is locked (:1007).
- The Dự án TKT tab appears only when at least one project is attached.

**Product-intro system type (`code === MEETING_TYPE_PRODUCT_INTRO`)**
- Adds the survey block in Biên bản.
- Adds the "survey" print part.

**Result form (#11130):** the "phiếu tổng hợp kết quả" assigned on the meeting type is designed (`.plans/meeting-type-result-form/design.md`) but not implemented in the FE (no `has_result_form` usage).

---

## 5. Attendance confirm (`components/assign/MeetingAttendanceConfirm.vue`)

**Where it appears**
- The detail page, right column, when `attendance_confirm.is_member` is true (`MeetingForm.vue:91`).
- The notification bell, in compact mode.

**Data:** the detail API returns `attendance_confirm {is_member, can_confirm, blocked_reason, my_status, my_note}` (`Meeting.php:871`).

**When the buttons show:** `can_confirm` is true, status is 1 or 2, and now is before the start time. Otherwise the locked reason is shown and the buttons are hidden, not disabled.

BE `attendanceConfirmBlockedReason` (`Meeting.php:843`) returns one of:
- "Bạn không nằm trong Thành phần tham gia nội bộ…"
- "Cuộc họp không ở trạng thái Lên lịch / Chốt lịch…"
- "Cuộc họp đã đến giờ bắt đầu, việc chốt điểm danh thuộc về người chủ trì."

**Actions**
- **Có mặt**: `POST assign/meeting/{id}/attendance-confirm {attendance_status:1, attendance_note:''}`. Toast: "Xác nhận tham dự thành công".
- **Vắng có lý do**: opens a modal "Báo vắng mặt cuộc họp" with a required reason ("Vui lòng nhập lý do vắng mặt"), then sends status 2 with the note. Toast: "Đã báo vắng mặt".
- The button for the current choice is hidden. At status 2 a pencil icon lets the user edit the reason.

**Badge text:**
- "Đã xác nhận: Có mặt"
- "Đã báo: Vắng có lý do - {note}"
- "Vắng không lý do"
- "Chưa phản hồi"

**How it connects to attendance**
- It writes the same `meeting_employees.attendance_status/note` that the host uses for roll call, so the host can override it later.
- Guests cannot choose status 3 (Vắng không lý do).
- The detail page updates the user's own row through `onAttendanceConfirmed` (`MeetingForm.vue:1238`), and an event `meeting-attendance-confirmed` keeps the bell and the page in sync.

---

## 6. Locking and view-only

**View-only mode** (`isShow`) disables every input and hides add/delete controls.

**Edit page**
- Without `can_edit` the edit page redirects to the detail page.
- `can_edit` = creator OR host (`Meeting.php:585`).
- `can_manage` = creator only; it controls Hủy, Xóa and change-status (`Meeting.php:618`, `MeetingController.php:336`).

**BE update guards** (`MeetingController.php:536-570`)
- Status 3 or 4 returns 423: "Thao tác không thành công. Dữ liệu đã được thay đổi…".
- Waiting for minutes (status 1/2) and past the report deadline also returns 423: "Đã quá hạn nhập biên bản cuộc họp (…)". The deadline is `end_date + lock_days` (company setting), and a job auto-cancels the meeting after it.
- `is_report_locked` = status 3/4 or overdue (`Meeting.php:496`).
- A locked meeting type is rejected only when newly chosen, or when the meeting is a draft.

**Other locks**
- Hoàn thành → Hủy is blocked.
- Delete only at status 0.
- Room booking is not allowed at status 0, 3 or 4.

**Past dates** are blocked only on create or at status 1.

---

## 7. Endpoint summary

All in `Routes/Meeting/api.php`, prefix `v1/assign/meeting`:
- `GET /` (list), `/calendar`, `/{id}`, `/{id}/print`, `/getListCustomer`, `/getListEmployee`, `/getListMeetingProject`, `/customer-history`, `/attendance-confirm-states`, `/investment-scopes`, `/export`
- `POST /` (create), `/{id}` (update), `/{id}/change-status`, `/{id}/attendance-confirm`, `/{id}/delete`, `/addContact`, `/{id}/project/{idx}/save-form-answers`

Others used by the form:
- `assign/meeting_types/getAll`
- `assign/meeting_cancel_reasons/getAll`
- `assign/prospective-projects/options-for-meeting[/{id}]`
- `assign/contracts/for-meeting`
- `assign/customers…`
- `files/upload`
- `meeting/rooms/bookable`, `meeting/room-bookings/unassign-meeting`

---

## 8. Decisions already made in `.plans`

**`app-meeting-mobile/design.md`, `plan.md`, `api-luu-tung-phan.md`** (design work only, no code)
- Navigation is a hub: the meeting detail lists 9 blocks, each opening a sub-screen. The 4 web tabs are not copied.
- Scope is "mine" only: two tabs, Tôi chủ trì / Tôi tham gia. No company or department filter. Use `MeetingCalendarCriteria`, not `MeetingCriteria`.
- Customer, contact and TKT project each get their own picker screen plus quick add.
- Messages use one in-flow strip style in three colours (red error, grey locked, green info). No toasts.
- The `*` marks follow the status of each screen. The "hồ sơ" completeness bar counts the blocks needed for Hoàn thành.
- Proposed partial-save endpoints, not built yet:
  - `PATCH /{id}/info|projects|members|attendance|reports|prepare-attachments|attachments|survey|conclusion`
  - Extend `change-status` to statuses 1, 2 and 3.
  - Add an `updated_at` check that returns 409.
  - Interim fallback: send the full `POST /{id}`.
- Cancel-reason catalogue (§7 of that file): required `cancel_reason_id` plus an optional note. This is now built (#11357).
- Open BE items:
  - `customerMeetingHistory` filters on the wrong user.
  - `customer-history` needs `host_name` and `end_date`.
  - The employee API should return `company_code`.
- Questions still open with the client:
  - Single vs multiple solutions per project.
  - A multi-project solution tree.
  - Whether a contact created in the app is auto-added to the members.
  - Whether contact row 1 can be deleted.
  - The #11130 result form is not drawn.

**`gop-db/meeting-theo-doi-tuong/design.md`** (08–09/10/2026)
- The "Meeting theo dự án" checkbox is replaced by `meeting_types.target_type` (1 = TKT, 2 = Contract).
- TKT: multiple projects, progress 2–10. Contract: a single HRM contract, any status except 3 and 10; the contract list ignores contract permissions and returns no amounts or phone numbers.
- A chosen customer filters contracts and projects. Choosing a contract first fills the customer.
- Old meetings keep their existing project or contract even if it is now out of range.
- A meeting type that is already in use can only change its target.
- The note says the mobile design still needs updating for this.

**`meeting-attendance-confirm/design.md`** (#11369)
- No new DB column; it reuses `attendance_status/note`.
- A dedicated endpoint, so plain guests can confirm without `canEdit`.
- Buttons are hidden, not disabled.
- One component is shared by the detail page and the bell.
- Guests cannot choose "Vắng không lý do".

**`meeting-nguoi-tham-gia-diem-danh/design.md`**
- At least one company member is required.
- Guest name is required. The phone must start with 0 and have 10–12 digits.
- Drag and drop only within each side.
- Roll call only on edit with status 2.

**`meeting-type-result-form/design.md`** (#11130)
- A meeting type can be assigned an existing form template.
- It would render at the top of Biên bản and block Hoàn thành on required questions.
- It runs alongside the hard-coded investment survey.
- Not built in the FE yet.

**`redmine-11291-meeting-lien-don-vi/design.md`**
- Member and executor pickers cover the whole group.
- Only bell notifications. Only newly assigned executors are notified, and not when the meeting is a draft or cancelled.

**`gop-db/meeting-hoan-thanh-loi-inline/plan.md`**
- Hoàn thành shows inline red errors per missing field plus the generic toast, and jumps to the error on every click.
- An individual customer is added automatically as a fixed customer-side member.

**`lich-meeting-tab/design.md`**
- The calendar shows only meetings where the user is a company-side member.
- Drafts are visible only to their creator. Cancelled meetings stay on the calendar.
- Colours: grey for draft and Lên lịch, blue for Chốt lịch, green for Hoàn thành, red for Hủy.

**`gop-db/meeting-list-page-standard/design.md`**
- 18 columns, with Mã meeting as the link column.
- Sửa and Xóa are the main buttons; the rest go into the `⋮` menu.
- The list scope uses the four tiered view permissions.