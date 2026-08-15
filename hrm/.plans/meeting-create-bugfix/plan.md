# Plan — Fix bug màn tạo meeting (?project_id)

## Phase 2 — Bugfix 400 "projects.0.address: Bắt buộc phải nhập" (2026-07-23)

### Nguyên nhân
- Form nhập dự án TKT trong meeting (ProjectInfoSection dùng chung) bind địa điểm vào `project_address`; field `address` khởi tạo rỗng ở `addProject()` và không được sync khi submit.
- `getProjectData()` (MeetingProject.vue) spread nguyên object → gửi `projects[0][address]=''` trong khi BE `MeetingCreateApiRequest` validate `projects.*.address => required` → 400 dù user đã nhập địa điểm.
- Các flow khác (saveFormAnswersForProject, loadProspectiveProjectFromQuery) đã có sync `address = project_address || address` — riêng getProjectData thiếu.

### FE (hrm-client)
- [x] `getProjectData()` trong `pages/assign/meeting/components/MeetingProject.vue`: sync `address`/`project_address` (lấy `project_address || address`) trước khi push vào payload — giống pattern dòng 947-948

### Verify
- [x] Replay API trên dev-hrm (curl, tài khoản namdangit): payload gốc của user → 400 `projects.0.address`; thêm `projects[0][address]` (như FE sau fix) → validate pass, meeting tạo thành công (id 48, 49 — đã xóa qua API delete)
- [x] Compile check MeetingProject.vue: vue-template-compiler 0 lỗi template + babel parse script OK
- [ ] Verify UI trên browser sau khi deploy code FE lên dev: tạo meeting có dự án TKT nhập tay → lưu thành công

### Checkpoint — 2026-07-23
Vừa hoàn thành: fix sync address trong getProjectData() (MeetingProject.vue) + verify API dev
Đang làm dở: (không)
Bước tiếp theo: user deploy hrm-client lên dev + verify UI tạo meeting
Blocked: (không)

## Phase 1 — Bugfix

### FE (hrm-client)
- [x] Bug 1: Bỏ filter `has_customer` theo `isFromProject` trong `meetingTypeOptions` (GeneralInfo.vue) → luôn hiện tất cả loại meeting kể cả khi vào kèm `?project_id`
- [x] Bug 2: Đồng bộ `customer_email` xuống từng project trong 2 vòng sync KH (`autoSelectCustomerFromProject` + `handleCustomerEvent`) → tab "Dự án tiền khả thi" hiện đúng Email khách hàng
- [x] Bug 3: Lỗi 400 `projects.0.is_intermediary_customer must be true or false` khi tạo meeting từ dự án. Nguyên nhân: `buildFormData` ép JS boolean thành chuỗi `"false"/"true"` khi build FormData, rule `boolean` của Laravel không nhận. Fix: trong `buildFormData` convert boolean → `1/0` trước khi `append`. Sửa 3 bản copy: `create.vue`, `_id/edit.vue`, `components/MeetingForm.vue`

### Verify
- [ ] Mở `/assign/meeting/create?project_id=112`: dropdown loại meeting đủ như khi không có project_id; Email khách hàng hiện đúng ở tab dự án
- [ ] Tạo meeting từ `?project_id=38` lưu thành công, không còn lỗi 400 `is_intermediary_customer`

### BE (hrm-api) — bổ sung 2026-07-17
- [x] Bug 4: Email khách hàng nhập ở màn sửa meeting không lưu vào dự án TKT khi customer chỉ tồn tại ở ERP (chưa sync sang bảng `customers` HRM). Nguyên nhân: `MeetingService::mapMeetingProjectToProspectiveProject` chỉ gán `customer_email/phone/tax_code/address` khi `Customer::find($resolvedCustomerId)` tìm thấy; nếu null → bỏ qua toàn bộ → mất dữ liệu user nhập. Fix: luôn ưu tiên giá trị FE gửi lên, `optional($customer)` chỉ để fallback khi FE bỏ trống.

### Verify (bổ sung)
- [ ] Tạo dự án TKT từ màn sửa meeting với KH (nhập Email KH) → mở chi tiết dự án: Email khách hàng hiển thị đúng giá trị đã nhập (kể cả KH ERP-only)

### BE (hrm-api) — bổ sung 2026-08-10
- [x] Bug 5: 1 hành động (Lên lịch / Chốt lịch ở màn Sửa) bắn 2 thông báo nội dung khác nhau. Nguyên nhân: `MeetingController::update()` gọi cả `MeetingService::sendMeetingNotification()` (thêm 04/02/2026, commit 20c8ca50e) lẫn hàm private `sendMeetingNotification()` cùng tên của controller (có từ 23/12/2025) — người thêm sau không xoá lời gọi cũ. Fix: bỏ lời gọi hàm private ở `update()`, chỉ giữ 1 nguồn là Service (dùng chung với `store()`); tiện thể dời lời gọi ra sau `DB::commit()` để không bắn noti khi rollback. Hàm private giữ nguyên vì vẫn phục vụ luồng Huỷ (`changeStatus`).

### Verify (bổ sung)
- [ ] Màn Sửa meeting → bấm "Lên lịch hẹn": thành viên chỉ nhận 1 thông báo (`[Meeting]: <tên>. Thời gian dự kiến ...`)
- [ ] Màn Sửa meeting → bấm "Đã chốt lịch": chỉ 1 thông báo
- [ ] Huỷ meeting: vẫn nhận đúng 1 thông báo `<tên> đã bị <người huỷ> huỷ. Lý do: ...`
- [ ] Tài liệu tham chiếu: `.plans/meeting-create-bugfix/thong-bao-meeting.xlsx`
- [x] Bug 6: Bấm "Lưu" khi meeting ĐÃ CHỐT LỊCH mà không đổi giờ vẫn bắn lại thông báo chốt lịch cho toàn bộ thành viên. Fix FE `MeetingForm.vue:767-781` (`handleSave`): nhánh else gửi kèm `send_notification: 0`; đồng thời ép `Number(this.form.status)` khi so sánh để không lọt trường hợp status là chuỗi. Luồng đổi giờ (popup xác nhận → `confirmTimeChange`) giữ nguyên: vẫn gửi thông báo với giờ mới.
- [ ] Verify: meeting status 2 → sửa ghi chú/biên bản/điểm danh → bấm Lưu: thành viên KHÔNG nhận thông báo; đổi giờ → xác nhận popup: nhận đúng 1 thông báo với giờ mới

### FE (hrm-client) — bổ sung 2026-08-11
- [x] Thêm radio "Phân loại họp" (Họp khách hàng / Họp nội bộ) ở tab Thông tin chung màn tạo/sửa meeting (`pages/assign/meeting/components/GeneralInfo.vue`): lọc dropdown "Loại meeting" theo `has_customer`; đổi radio thì bỏ loại đang chọn nếu không khớp; màn sửa/xem tự set radio theo loại meeting đang có
- [x] Lưu phân loại họp xuống DB: migration `2026_08_11_090000_add_is_customer_meeting_to_meetings_table` (cột `is_customer_meeting` boolean default 1, backfill theo `meeting_types.has_customer`); fillable Meeting; rule `nullable|boolean` ở Meeting Create/Update Request; gán ở `MeetingController::store/update` (ưu tiên FE gửi, fallback theo loại meeting); trả về ở `MeetingTransformer`; FE bind radio vào `form.is_customer_meeting`
- [x] Verify (Playwright, FE :3000 / BE :8000): migrate OK (cột `is_customer_meeting` tinyint default 1, backfill 13 nội bộ / 2 KH); tạo mới chọn "Họp nội bộ" → dropdown chỉ 5 loại nội bộ, lưu `is_customer_meeting=0` (meeting id 17 — dữ liệu test); màn Sửa nạp lại đúng radio; đổi radio sang "Họp khách hàng" + chọn loại + chọn KH → lưu `is_customer_meeting=1`

### BE + FE — Thông báo theo thay đổi thực tế (2026-08-11)
> Lưu ý: 2 fix ngày 10/08 (bỏ bắn trùng ở `update()`, tắt noti khi lưu meeting đã chốt) không còn trong working tree khi bắt đầu task này — đã áp lại cùng logic mới.
- [x] BE `MeetingService::notifyMeetingChanges()` (mới): so sánh snapshot trước/sau khi lưu → đổi thời gian họp báo toàn bộ thành viên nội bộ đang ở trong meeting (`Thay đổi lịch`); người được thêm nhận `Cập nhật: … Bạn được thêm vào cuộc họp. Thời gian: …`; người bị xoá nhận `Cập nhật: … Bạn đã được đưa ra khỏi cuộc họp.` Người vừa thêm KHÔNG nhận thêm noti đổi lịch. Không đổi gì → không báo ai.
- [x] BE helper trong MeetingService: `buildMeetingNotificationContent()` theo chuẩn `.claude/skills/notification-convention` (`[MET] {Nhóm hành động}: <b>{Tên ≤50}</b>. {Ghi chú}`, tổng ≤120, cắt ghi chú trước), `formatMeetingTimeRange()`, `isSameDateTime()` (Carbon::parse, chịu lệch format), `notifyMeetingEmployees()`
- [x] BE `MeetingController::update()`: snapshot `start_date/end_date/company_members` TRƯỚC khi sync (syncCompanyMembers xoá sạch rồi tạo lại); sau `DB::commit()` — đổi trạng thái (nút Lên lịch/Chốt lịch) → báo toàn bộ như cũ, giữ nguyên trạng thái (nút Lưu) → gọi `notifyMeetingChanges`. Gộp về 1 nguồn gửi (bỏ lời gọi hàm private gây bắn trùng), gửi sau commit
- [x] FE `MeetingForm.vue` `handleSave()`: bỏ cờ `send_notification` (BE tự quyết), ép `Number(status)` khi so sánh để không lọt popup xác nhận đổi giờ khi status là chuỗi

### Verify (bổ sung)
- [ ] Meeting status 1 hoặc 2 → sửa ghi chú/biên bản, không đổi giờ, không đổi thành viên → bấm Lưu: KHÔNG ai nhận thông báo
- [ ] Đổi giờ họp → Lưu: toàn bộ thành viên nội bộ nhận `[MET] Thay đổi lịch: …. Thời gian mới: …`
- [ ] Thêm 1 người nội bộ → Lưu: chỉ người đó nhận `[MET] Cập nhật: …. Bạn được thêm vào cuộc họp. Thời gian: …`
- [ ] Bớt 1 người nội bộ → Lưu: chỉ người bị xoá nhận `[MET] Cập nhật: …. Bạn đã được đưa ra khỏi cuộc họp.`
- [ ] Vừa đổi giờ vừa thêm người → người mới chỉ nhận 1 noti "được thêm vào", người cũ nhận noti đổi lịch
- [ ] Nút "Lên lịch hẹn" / "Đã chốt lịch": vẫn báo toàn bộ thành viên, mỗi người đúng 1 noti

### Merge tpe-develop-assign → tpe (2026-08-14)
- [x] Fix conflict `MeetingController.php` (khối gửi thông báo ở `update()`) và `MeetingForm.vue` (conflict cả file do nhánh dev đổi LF→CRLF — merge lại 3-way sau khi chuẩn hoá LF, còn đúng 1 conflict thật ở `handleSave()`)
- [x] Chốt giữ luồng thông báo của `tpe-develop-assign`: BE khôi phục snapshot + nhánh `notifyMeetingChanges`; FE `handleSave()` bỏ cờ `send_notification` (nút Lưu báo đúng người bị ảnh hưởng)
- [x] So sánh trạng thái ở `handleSave()` dùng `==` (không dùng `Number(...) === `) theo yêu cầu
- [x] Xuất lại `.plans/meeting-create-bugfix/thong-bao-meeting.xlsx` theo hành vi sau merge (17 hành động + quy tắc chung + tham chiếu code); xác nhận KHÔNG còn lặp thông báo
- [ ] Còn tồn: `store()` vẫn gửi thông báo TRƯỚC `DB::commit()` (MeetingController:180 vs 182) — nên chuyển xuống sau commit như `update()`
- [ ] Còn tồn: trạng thái Hoàn thành (3) không bắn thông báo cho ai — cần xác nhận nghiệp vụ
