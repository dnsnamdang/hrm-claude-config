# Plan — Meeting: tải danh sách Dự án TKT phân trang

Phụ trách: @dnsnamdang · Nhánh `gop_db` · Design: `design.md`

> **Chưa được phép code.** Trước mỗi phase phải hỏi riêng, nêu phạm vi (repo · nhánh · file · migration/DB), chờ câu "làm".

## Phase 1 — BE (`hrm-api`, không migration)

- [x] Scope dùng chung phạm vi người dùng (tạo / làm giải pháp / hỗ trợ) trên `ProspectiveProject`; `getForMeeting` dùng lại scope này (hành vi không đổi)
- [x] `ProspectiveProjectService::optionsForMeeting()` — search mã/tên, lọc `customer_id`, `paginate` (20, trần 50), select cột gọn, sắp `id desc`
- [x] Resource gọn `MeetingProjectOptionResource` (status_name / status_color do BE trả)
- [x] `optionsForMeetingDetail($id)` — full resource, cùng phạm vi, ngoài phạm vi → 404
- [x] Route `options-for-meeting` + `options-for-meeting/{id}` (đặt TRƯỚC route `{id}` nếu có)
- [x] Migration `Modules/Assign/Database/Migrations/2026_10_14_000001_add_meeting_option_indexes_to_prospective_projects_table.php` (7 index, kiểm tồn tại trước khi thêm) — ĐÃ TẠO 14/10, CHƯA chạy migrate. Kiểm: index trên `prospective_projects(status)`, `created_by`, `solution_employee_id`, `customer_id`
- [x] `tests/Feature/MeetingTarget/MeetingProjectOptionsTest.php` — 9/9 OK (14/10). PHPUnit: phạm vi (3 vai trò + người ngoài), dải 2–10, search, customer_id, phân trang, trần per_page, detail 404

Phát hiện khi chạy test (14/10, CHƯA sửa — ngoài phạm vi):
- [x] `MeetingTargetFixture::grantPermission()` insert `roles.company_id` (bảng ERP không có cột này) → ĐÃ SỬA 14/10, thư mục `tests/Feature/MeetingTarget` 35/35 OK (gồm 3 ca getForMeeting).
- [x] (14/10 đã sửa, PHPUnit 6 bộ OK — 200 test) 6 fixture KHÁC dính cùng lỗi: MeetingByProjects/MeetingFixture, MeetingByEmployees/MeetingFixture, ServiceDemand/MeetingViewPermissionTest, ServiceDemand/ReportApiTest, EmployeeWorkPerformance/ReportApiTest, PotentialCustomerTracking/TrackingFixture.
- `route:list` lỗi sẵn (`PermissionHelper` gọi `auth()->user()` trong constructor 1 controller khác) — không liên quan.

## Phase 2 — FE web (`hrm-client`)

- [x] Dùng `V2BaseSelectRemote` nguyên trạng (multiple + fetchFn), KHÔNG tạo component mới, KHÔNG sửa file dùng chung (user chốt 14/10). Không có cuộn tải thêm: 20 dòng đầu, gõ để thu hẹp
- [x] `GeneralInfo.vue`: bỏ `getForMeeting?per_page=10000` + `prospectiveProjects`; fetchFn gọi `options-for-meeting` (kèm `customer_id` nếu đã chọn KH); chọn thêm → `options-for-meeting/{id}` (cache `projectDetails`) rồi mới gắn vào form
- [x] Dự án đã gắn: tag lấy từ `form.projects` (`initialOption`); `handleProjectChange` giữ nguyên object cũ khi không có chi tiết; `autoSelectProjectFromQuery` gọi chi tiết
- [x] Playwright MCP: tạo (chọn / bỏ chọn, chỉ gọi options + detail), chi tiết meeting 845 (dự án 327 ngoài phạm vi vẫn hiện tag, ô khoá), giữ dữ liệu dự án cũ khi thêm dự án mới
- [x] e2e `tests/assign/meeting-target.spec.ts`: sửa ca 4 (bỏ `.sp-clear` → nút × tag select2) + thêm ca 5 tìm phía server — 8 passed (3 setup + 5)

## Phase 3 — Dọn

- [x] Gỡ `getForMeeting` sau khi grep không còn nơi gọi
  Rà 15/10: không còn nơi gọi ở hrm-client, TPE_APP (`app/lib`), ERP. Chỉ còn route + controller + service + 4 ca PHPUnit + comment.
- [x] BE: xoá route `GET /assign/prospective-projects/getForMeeting` (`Routes/api.php:368`), `ProspectiveProjectController::getForMeeting`,
      `ProspectiveProjectService::getForMeeting` (giữ `meetingProjectFullQuery` — còn dùng cho `optionForMeetingDetail`)
- [x] PHPUnit: `MeetingTargetSourceTest` bỏ 3 ca getForMeeting (dải 2–10 đã có ca tương đương ở `MeetingProjectOptionsTest`;
      include_ids / meeting_id không còn ý nghĩa vì dự án đã gắn lấy từ chi tiết meeting) · `MeetingProjectOptionsTest` bỏ ca so khớp phạm vi
- [x] Sửa comment nhắc tên cũ: `ProspectiveProject.php:139`, controller `:75`, service `:513`, `GeneralInfo.vue:263`
- [x] e2e `meeting-target.spec.ts`: bỏ assert "không gọi getForMeeting" (route không còn) → chạy lại toàn bộ spec + PHPUnit MeetingTarget

## Phase 4 — Bug: KH ↔ Dự án TKT (user chốt 14/10/2026: chọn KH TRƯỚC, dự án load theo KH)
Lỗi: chọn dự án → gọi `assign/customers/{id}` để tự điền KH → 403 (không quyền xem KH) → ô KH trống; user chọn KH khác →
hàm chọn KH ghi đè customer_id của dự án; BE không kiểm → lưu "thành công" dù dự án lệch KH.
- [x] FE `GeneralInfo.vue`: loại có KH → ô Dự án TKT khoá tới khi có KH (placeholder "Chọn khách hàng trước")
- [x] FE: đổi / xoá KH → bỏ các dự án đã chọn (watcher `form.customer_id`, như HĐ); bỏ tự điền KH khi chọn dự án (trừ luồng `?project_id`)
- [x] FE: hàm chọn KH không ghi đè KH của dự án gắn từ Dự án TKT
- [x] BE `ValidatesMeetingTarget`: dự án phải cùng `customer_id` với meeting → 400
- [x] (thêm, user cho phép) `prospective-projects/components/CustomerInfoSection.vue`: popup chọn KH / Thêm nhanh KH chỉ gắn khi
      `!isShow` — GỐC lỗi "báo thành công nhưng không lấy data": tab Dự án TKT của meeting gắn popup CÙNG id
      `choose-erp-customer` → $bvModal.show mở cả 2, cú chọn KH rơi vào section dự án, KH meeting không đổi
- [x] PHPUnit `MeetingTargetSaveTest` +2 ca (47/47); MeetingByProjects 28 · ByEmployees 41 · ServiceDemand 45 · PCT 24 · ReportMeetingView 6
- [x] e2e `meeting-target.spec.ts`: ca 5 chọn KH trước; ca 6 mới (khoá/lọc/đổi KH bỏ dự án); `pickType` riêng (pickSelect2 gõ vào
      ô tìm đầu tiên trong DOM = ô dự án đang khoá) → 6/6
- [x] Chạy lại toàn bộ e2e meeting + prospective-project (15,5 phút): 76 passed · 13 failed · 42 did not run · 1 skipped.
      10/13 là timeout mở trang (Nuxt dev quá tải) — chạy riêng: meeting-participants 7/7, report-meeting-drawer 9/9 xanh.
      Còn lệch CÓ SẴN, không do Phase 4: investment-survey (chờ seed INTERNAL), prospective-projects-filter (spec chờ
      `.filter-grid .ff`, markup đổi từ 37b73a236 12/10), meeting-by-employees ca 13 (thứ tự chồng popup báo cáo). (khoá khi chưa KH, lọc theo KH, đổi KH bỏ dự án); chạy lại toàn bộ e2e meeting

### Checkpoint — 2026-10-14
Vừa hoàn thành: Phase 1 BE — scope `selectableForMeetingBy`, `options-for-meeting` (+ `/{id}`), `MeetingProjectOptionResource`, PHPUnit 9/9.
Đang làm dở: không.
Bước tiếp theo: user review diff hrm-api; quyết định index (migration) + sửa fixture; rồi hỏi phép Phase 2 FE web (component mới).
Blocked:

### Checkpoint — 2026-10-14 (chiều)
Vừa hoàn thành: sửa fixture MeetingTarget (35/35), Phase 2 FE web (V2BaseSelectRemote), e2e meeting-target 8 passed.
Đang làm dở: migration index — bản nháp `migration-index-draft.md`, chưa tạo file.
Bước tiếp theo: user cho phép ghi file migration → tạo + hỏi có chạy `migrate` vào `local_hrm_erp` không; Phase 3 gỡ `getForMeeting` (FE đã hết nơi gọi).
Blocked: tạo file migration bị chặn quyền ghi.

- [x] (user cho phép) Luồng tạo meeting từ Dự án (`?project_id`): `autoSelectCustomerFromProject` — chi tiết KH lỗi/403 thì
      dựng KH từ dữ liệu trên dự án (mã, tên, MST, SĐT, email, địa chỉ) rồi đi tiếp điền liên hệ + Nhóm/Lĩnh vực.
      Tái hiện trước: dự án 47 gắn, 3 lần customers/23699 → 403, ô KH trống. Sau: ô KH = ĐẶNG BÁ THÁI đủ thông tin.
      Luồng HĐ không đổi (object truyền vào không có customer_id). e2e meeting-target +1 ca → 7/7.

### Checkpoint — 2026-10-14 (đêm) — Phase 4 KH ↔ Dự án TKT
Vừa hoàn thành: Phase 4 (GeneralInfo + CustomerInfoSection + ValidatesMeetingTarget + PHPUnit + e2e meeting-target 6/6)
Đang làm dở: —
Bước tiếp theo: user review diff; quyết sửa seed khảo sát (investment-survey); 2 spec lệch có sẵn (prospective-projects-filter,
  meeting-by-employees ca 13). Luồng ?project_id đã xử lý (fallback KH từ dự án).
Blocked:

### Checkpoint — 2026-10-15 — Phase 3 gỡ getForMeeting (user: "làm 1"; app mobile mới ở bước design, chưa code)
Vừa hoàn thành: xoá route + controller + service `getForMeeting` (giữ `meetingProjectFullQuery`); bỏ 4 ca PHPUnit gọi endpoint cũ
      (3 ở MeetingTargetSourceTest, 1 ở MeetingProjectOptionsTest); sửa comment ở Entity / controller / service / `GeneralInfo.vue`;
      e2e meeting-target bỏ assert endpoint cũ. Kiểm: grep `getForMeeting` toàn hrm-api/hrm-client/e2e → rỗng · gọi thử
      `/prospective-projects/getForMeeting` → 404, `options-for-meeting` → 200 · PHPUnit MeetingTarget **43/43** (47 − 4 ca gỡ) ·
      e2e meeting-target **10 passed** (7 ca + 3 setup).
Đang làm dở: —
Bước tiếp theo: user review + commit; việc 2 (đồng bộ `meeting-mobile.pen`), việc 3 (gộp ~25 API màn Sửa meeting) — chờ user.
Blocked:
