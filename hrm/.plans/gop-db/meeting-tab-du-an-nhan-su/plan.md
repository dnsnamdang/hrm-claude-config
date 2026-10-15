# Plan — Meeting web: tab "Dự án TKT" chỉ xem + tab "Nhân sự tham gia"

Phụ trách: @dnsnamdang · Nhánh `gop_db` · Design: `design.md` · Spec: `docs/superpowers/specs/gop-db/2026-10-14-meeting-tab-du-an-nhan-su-design.md`

> **Chưa được phép code.** Trước khi code hỏi riêng, nêu phạm vi (repo · nhánh · file · migration/DB), chờ câu "làm".

## Phase 1 — BE: lưu meeting chỉ lưu liên kết dự án (hrm-api, không migration)
- [x] `syncProjects`: bỏ tạo dự án, bỏ fill trường dự án + applyCustomerDerivedFields, bỏ đẩy Đang tạo → Thu thập; giữ liên kết (giữ solution/module đang có khi payload không gửi) + snapshot phiếu + answers
- [x] (U1 đã làm) sync xoá liên kết dự án không còn trong payload
- [x] `saveFormAnswersForProject`: bỏ nhánh tạo dự án → ValidationException (controller trả 400 kèm errors)
- [x] 2 Request: `projects.*` chỉ còn prospective_project_id (required|exists) + answers + solution_*; gỡ rule/message trường dự án
- [x] `MeetingController`: gỡ 3 khối kiểm Ứng dụng dự án bị khoá (store + update) + import Applications
- [x] Gỡ `mapMeetingProjectToProspectiveProject` nếu hết nơi dùng
- [x] `MeetingProjectLinkTest` 10 ca — thư mục MeetingTarget 45/45 OK. PHPUnit (MeetingTarget fixture): trường dự án không đổi, không tạo dự án, thiếu trường cũ vẫn lưu, answers lưu, id lạ 422

## Phase 2 — FE: tab "Dự án TKT" (hrm-client)
- [x] `MeetingForm`: nhãn "Dự án TKT", hiện khi `form.projects.length > 0` hoặc `?project_id`; bỏ hết dự án khi đang ở tab → về `info`
- [x] `MeetingProject`: gỡ Thêm dự án / × / addProject / removeProject; tab con = mã dự án; 2 section `is-show` luôn true; phiếu giữ nguyên

## Phase 3 — FE: tab "Nhân sự tham gia"
- [x] `MeetingParticipants.vue` (1 bảng, 2 nhóm, 2 draggable tbody, cột điểm danh theo status, lỗi đúng dòng)
- [x] `GeneralInfo`: gỡ cột phải, cột trái md=12; chuyển PopupStaff + thêm/xoá thành viên sang component mới
- [x] `MeetingForm`: tab `participants` thay `attendance`, ref mới, `tabForErrorKey`, chữ danh sách lỗi Hoàn thành
- [x] Xoá `MeetingAttendance.vue` sau khi grep sạch

## Phase 4 — Kiểm
- [x] Playwright MCP đo DOM theo spec mục 5
- [x] e2e mới `meeting-participants.spec.ts` (4 ca) + sửa ca 1, 4 `meeting-target.spec.ts` → 9/9 pass (--retries=0). Bổ sung e2e + chạy lại TOÀN BỘ `e2e/tests/assign/meeting-*.spec.ts` (đọc dòng tổng kết, không chỉ tìm chữ failed)

Kết quả chạy TOÀN BỘ `tests/assign/meeting-*` (14/10, --retries=0): 25 passed · 9 failed · 70 did not run (serial).
9 ca fail đều CÓ SẴN, không do đợt này (đã đối chiếu):
- 4 ca: fixture `meetingByEmployeesFixture.ts` / `meetingByProjectsFixture.ts` insert `roles.company_id` (bảng ERP không có cột).
- meeting-host.spec 1: còn kỳ vọng checkbox "Meeting theo dự án" — đã gỡ từ trước ở HEAD.
- meeting-host.spec 3: đọc ô chủ trì trước khi detail về (đo: detail về ~23s trên server dev, sau đó hiện ĐÚNG "Lương Văn Đạo").
- meeting-host.api: 403 "không có quyền sửa meeting" (đoạn kiểm quyền không đổi).
- meeting-by-market-grouping: lưu bị chặn "Vui lòng chọn Hợp đồng." (luật meeting theo đối tượng).
- meeting-investment-survey 1: fixture meeting 44/45 lệch DB (44 đang Hoàn thành), dòng loại hệ thống thiếu nút Xem.

### Checkpoint — 2026-10-14 (tối)
Vừa hoàn thành: Phase 1–4 (BE chỉ lưu liên kết + U1, tab Dự án TKT chỉ xem, tab Nhân sự tham gia, PHPUnit MeetingTarget 45/45, e2e 2 spec của màn 9/9).
Đang làm dở: không.
Bước tiếp theo: user review diff (hrm-api + hrm-client + e2e) trên gop_db; quyết định sửa 6+2 fixture e2e/PHPUnit dính `roles.company_id` + các ca e2e meeting cũ lệch (ngoài phạm vi); đồng bộ bản thiết kế app `meeting-mobile.pen`.
Blocked:

### Checkpoint — 2026-10-14 (đêm) — sửa fixture + migration index
Vừa hoàn thành: sửa `roles.company_id` ở 6 fixture PHPUnit + 2 fixture e2e (meetingByEmployees/ByProjects); tạo migration
index `2026_10_14_000001_add_meeting_option_indexes_to_prospective_projects_table.php` (CHƯA migrate).
PHPUnit: MeetingTarget 45 · MeetingByProjects 28 · MeetingByEmployees 41 · ServiceDemand 45 · PotentialCustomerTracking 24 ·
EmployeeWorkPerformance 17 — tất cả OK. e2e `tests/assign/meeting-*` (--retries=0): 49 passed · 6 failed · 49 did not run
(trước sửa: 25 · 9 · 70). 6 ca fail đều có sẵn: meeting-host.api 403; meeting-host.spec 1 (checkbox đã gỡ) + 3 (đọc trước khi
detail về); market-grouping (bắt buộc Hợp đồng); investment-survey 1 (fixture 44/45 lệch); meeting-by-employees 2 (test chờ
"dòng", màn đổi sang "nhân viên" từ commit c86f8a5ca 05/10).
Bước tiếp theo: user quyết chạy migrate vào DB local; sửa 4 file e2e khác cùng lỗi roles.company_id (serviceDemandFixture,
potentialCustomerTrackingFixture, report-meeting-drawer.spec, employee-work-performance.spec); cập nhật 6 ca e2e cũ lệch.
Blocked:

### Checkpoint — 2026-10-14 (khuya) — migrate index + 4 fixture e2e + 6 ca e2e cũ (user cho phép cả 3)
Vừa hoàn thành:
- [x] Chạy migration index `2026_10_14_000001_…` vào `hrm_erp` (chỉ đúng file, `--path`); kiểm DB đủ 7 index.
- [x] Bỏ `roles.company_id` ở 4 file e2e (serviceDemandFixture, potentialCustomerTrackingFixture, report-meeting-drawer, employee-work-performance)
      + fixture PCT ghi thêm `estimated_budget` (báo cáo đọc cột này từ 07/10). 4 nhóm spec: 72 ca → 71 passed · 1 skipped (điều kiện dữ liệu).
- [x] meeting-by-employees ca 2: "dòng" → "nhân viên". meeting-host ca 1 bỏ kiểm checkbox "Meeting theo dự án" đã gỡ; ca 1/3 chờ select hiện tên.
- [x] Util mới `e2e/utils/fixtureMeeting.ts` `requireFixtureMeeting(envKey, code)`: id meeting fixture phải đúng mã E2E + do tài khoản e2e tạo,
      không thì dừng. Gắn vào meeting-host(.api), meeting-by-market-grouping (người mượn lấy theo DB, bỏ id 26), meeting-investment-survey.
      Lý do: sau gộp DB id 44/45/55 trong e2e/.env là meeting THẬT; investment-survey từng xoá dữ liệu khảo sát của 44 (đối chiếu
      hrm_erp_giacty + tpe_10926: vốn rỗng → không mất), market-grouping từng cố lưu đè Thành phần meeting 55 (bị luật HĐ chặn).
Đang làm dở: —
Bước tiếp theo: chờ user cho phép chạy seed `e2e_meeting_survey_seed.php` + `e2e_customer_demand_seed.php` vào hrm_erp rồi ghi id mới vào
      e2e/.env (E2E_SYSTEM/INTERNAL/LOCKED_SCOPE/EDITABLE_MEETING_ID) → chạy lại meeting-host, market-grouping, investment-survey.
Blocked: 3 spec trên dừng ở `requireFixtureMeeting` cho tới khi seed.

### Checkpoint — 2026-10-14 (khuya, 2) — seed fixture meeting trên DB gộp
Vừa hoàn thành:
- [x] Sửa `hrm-api/database/e2e_customer_demand_seed.php` (user cho phép): bỏ `mysql2` → `DB::table('customers')`; `scopes` → `hrm_scopes`.
      Đã chạy: E2E-DEMAND-DONE 6354, E2E-DEMAND-OTHER, E2E-DEMAND-EDITABLE 6356 → `e2e/.env` E2E_EDITABLE_MEETING_ID=6356.
- [x] Chạy `e2e_meeting_survey_seed.php` (CHƯA sửa file): tạo được E2E-SURVEY-SYSTEM 6353 + lĩnh vực LVCTKD.E2E1 (2321) rồi DỪNG ở
      `select company_id from scopes` (DB gộp `scopes` là bảng ERP; nhóm ngành HRM = `hrm_scopes`). Không ghi gì vào `scopes` ERP.
      Cũng không tìm thấy loại "Meeting nội bộ" (DB gộp: "Họp nội bộ phòng ban" id 2) → bỏ qua E2E-SURVEY-INTERNAL. `.env` E2E_SYSTEM_MEETING_ID=6353.
- [x] meeting-host (UI + api): 11 passed · 1 skipped (điều kiện dữ liệu). Ca báo cáo lọc theo ngày + loại của fixture (báo cáo phân trang).
- [x] market-grouping: người mượn lấy theo công ty người tạo; "Mã|Số biên bản"; khối "Theo phòng chủ trì" so với số tổng hero
      (không đếm dòng trang). 20/21 passed — ca còn lại mỗi lượt 1 ca KHÁC timeout `page.goto` 30s (Nuxt dev chậm, API ~0,5s) → chập chờn môi trường.
Bước tiếp theo: xin phép sửa `e2e_meeting_survey_seed.php` (scopes→hrm_scopes, bỏ company_id/department_id nếu cần theo cột hrm_scopes,
      loại nội bộ theo tên DB gộp) + spec investment-survey dòng 190 "Meeting nội bộ" → chạy lại seed, ghi INTERNAL/LOCKED_SCOPE id, chạy investment-survey.
Blocked: chờ user cho phép sửa seed khảo sát.

### Checkpoint — 2026-10-15 — seed khảo sát + investment-survey + 2 spec lệch (user cho phép "có")
Vừa hoàn thành:
- [x] `hrm-api/database/e2e_meeting_survey_seed.php`: `scopes` → `hrm_scopes` (cả join/count); loại nội bộ tìm theo
      "Meeting nội bộ" | "Họp nội bộ phòng ban"; giờ họp fixture = 1 giờ TRƯỚC hiện tại (+ created_at lùi 2 ngày) vì nút
      [Hoàn thành] chỉ bật khi họp đã bắt đầu (Redmine #11357, `Meeting::completeBlockedReason`). Đã chạy vào hrm_erp:
      SYSTEM 6353 · INTERNAL 6603 · LOCKED-SCOPE 6604 · nhóm ngành E2E 36/37/38 (hrm_scopes) · ROW 36 · PARENT 8 → ghi `e2e/.env`.
- [x] `meeting-investment-survey.spec.ts` theo UI hiện tại: ca 1 (màn loại meeting bỏ icon Xem, lọc "nội bộ" vì DB gộp >1 trang) ·
      ca 7 header có `*` · ca 9/19 lỗi chuẩn "Bắt buộc phải nhập" (Redmine #11130) kiểm theo vị trí câu · ngày nhập tính động
      `futureDate()` (ngày cứng 01/10/2026 đã quá hạn) · helper `clickControl()` bấm mép phải-trên ô chọn (tâm ô trúng nút x của chip
      tên dài; góc dưới-phải là tay kéo) · `waitScopesLoaded()` · trần 120s/ca.
      Kết quả: ca 1–12 + 14–19 xanh (18/19). Ca 13 dừng ở chốt fixture.
- [x] `requireFixtureMeeting` thêm `{ ownerEmail }` + mã kết thúc "-" = so tiền tố; ca 13 chốt `E2E_MEETING_ONLY_MEETING_ID`
      (=46 hiện là meeting THẬT "TPE.MET.NB.26.0044" của NV 25).
- [x] Spec dùng chung fixture: meeting-host(.api), my-todo-calendar-scope.api, meeting-target.api → 23 passed · 1 skipped.
- [x] meeting-by-employees ca 13/14: chờ lặp popup dưới lộ lên sau khi popup trên fade xong → 17/17 passed.
- [x] Môi trường: API local chạy lại `PHP_CLI_SERVER_WORKERS=4 php artisan serve` (1 worker xếp hàng ~25 API màn Sửa meeting → 10-20s).
Đang làm dở: —
Bước tiếp theo:
- Ca 13 investment-survey: cần chạy `e2e_meeting_survey_fixture.php` (tạo 2 NV e2e_no_meeting_perm / e2e_meeting_only + role + quyền
  vào hrm_erp; file có insert `roles` — kiểm `company_id` như 4 fixture trước) → CHỜ user cho phép.
- `prospective-projects-filter.spec.ts` (15 ca) kiểm lưới lọc `.filter-grid .ff` đã bị gỡ ở commit 75e1094e3 (21/09, chuyển sang
  `V2BaseSmartFilterPanel`) → phải VIẾT LẠI, chờ user chọn hướng.
- Ghi nhận hiệu năng: màn Sửa meeting gọi ~25 API lúc mở (CLAUDE.md: > 5 API phải nêu ra).
Blocked: 2 việc trên chờ user.

### Checkpoint — 2026-10-15 — fixture ca 13 + viết lại spec bộ lọc Dự án TKT (user: "có, làm cả 2")
Vừa hoàn thành:
- [x] `hrm-api/database/e2e_meeting_survey_fixture.php`: bỏ `roles.company_id` (bảng ERP không có cột) · `department_id` 1 → 5
      (DB gộp không có phòng ban id=1, dùng phòng của e2e_assign) · meeting clone `created_at` lùi 2 ngày (màn Sửa ràng buộc
      start_date >= created_at). Chạy vào hrm_erp: NV 4961 (no perm, role 105442) · NV 4962 (meeting only, role 105443) ·
      meeting E2E-MEETONLY-4962 = 6615 → `e2e/.env` E2E_MEETING_ONLY_MEETING_ID=6615.
- [x] investment-survey ca 13a: toast 403 tới sau ~10,5s (API chi tiết xếp sau ~25 API) → chờ 30s; `openReportTab` click tab
      Biên bản chờ 60s (lớp phủ loading). Chạy TOÀN BỘ spec: **22 passed** (19 ca + 3 setup).
- [x] `e2e/tests/assign/prospective-projects-filter.spec.ts` VIẾT LẠI cho `V2BaseSmartFilterPanel` (bỏ 15 ca đo style lưới cũ,
      bản cũ lưu scratchpad): 1 đủ 17 ô · 2 Khách hàng tìm từ server · 3 ô danh mục đổi là lọc · 4 khoảng Ngày tạo · 5 Làm mới ·
      6 cascade Công ty→Phòng ban→Bộ phận (+ NV KD) · 7a/7b ô ẩn theo quyền (bớt quyền trong response `user-profile` bằng route,
      không đụng DB). Không chạy serial. Kết quả: **8 passed · 3 failed (ca 3, 4, 5)**.
- [x] 3 ca đỏ là LỖI THẬT của màn (có sẵn từ commit fbe304443, 07/09): `filters` dựng bằng `JSON.parse(JSON.stringify(initialStateForm))`
      (index.vue dòng 455 + 1471 `handleReset`) → rơi mọi key `undefined` → `handleFilterChange` gán `this.filters[key]` không
      reactive (Vue 2) → chọn ô select của panel / khoảng ngày KHÔNG tự lọc (phải bấm Tìm kiếm), Làm mới không xoá ô Ngày tạo /
      Nguồn vốn trên giao diện. Đã giả lập bản khai đủ key trong trình duyệt → cả 3 hành vi đúng.
Bước tiếp theo: xin phép sửa `hrm-client/pages/assign/prospective-projects/index.vue` (clone initialStateForm giữ đủ key, dùng ở
      data() + handleReset; hoặc `$set` trong handleFilterChange) → chạy lại prospective-projects-filter.
Blocked: chờ user cho phép sửa màn Dự án TKT.

### Checkpoint — 2026-10-15 — sửa bộ lọc màn Dự án TKT (user: "ok")
Vừa hoàn thành:
- [x] `hrm-client/pages/assign/prospective-projects/index.vue`: thêm `freshFilters()` (bản sao GIỮ đủ key `undefined`, mảng mới
      mỗi lần) thay `JSON.parse(JSON.stringify(initialStateForm))` ở `data()` + `handleReset()`, và thay `{ ...initialStateForm, ...saved }`
      ở `restoreSavedFilters()` (tránh dùng chung mảng của hằng). +16/−3 dòng.
- [x] Kiểm trên trình duyệt: chọn Nguồn vốn → gọi ngay `funding_source_id=2`; vào chi tiết rồi quay lại → khôi phục + đổi Quy mô gọi
      `project_scale_id=1&funding_source_id=2`; Làm mới → request không điều kiện, ô Nguồn vốn trống, 0 ô nhãn nổi.
      (Tải lại trang KHÔNG khôi phục bộ lọc — đúng thiết kế `filterStateMixin`: chỉ lưu ở `beforeRouteLeave`.)
- [x] Thêm ca 8 (vào chi tiết → quay lại) vào `prospective-projects-filter.spec.ts`. Toàn bộ spec: **12 passed** (9 ca + 3 setup).
Đang làm dở: —
Bước tiếp theo: việc tồn từ trước — Phase 3 gỡ `getForMeeting`; đồng bộ `meeting-mobile.pen` (màn 06 chỉ xem, gộp Thành phần + Điểm danh);
      cân nhắc gộp ~25 API lúc mở màn Sửa meeting.
Blocked:

### Checkpoint — 2026-10-15 — wrap up
Vừa hoàn thành: toàn bộ việc user cho phép trong 2 ngày 14–15/10 (đều local, CHƯA commit): 4 phase tab Dự án TKT + Nhân sự tham gia ·
      ràng buộc chọn KH trước → ô Dự án lọc theo KH (FE `GeneralInfo.vue` + `CustomerInfoSection.vue`, BE `ValidatesMeetingTarget`,
      PHPUnit +2 ca) · migrate index · dọn e2e `roles.company_id` + 6 ca cũ + seed nhu cầu/khảo sát + fixture ca 13 ·
      viết lại `prospective-projects-filter.spec.ts` + sửa lỗi reactivity bộ lọc màn Dự án TKT (`freshFilters()`).
      Kết quả e2e cuối: investment-survey 22 passed · prospective-projects-filter 12 passed · meeting-target 7/7 · meeting-by-employees 17/17.
Đang làm dở: —
Bước tiếp theo: user review + quyết commit (hrm-api, hrm-client nhánh gop_db) → Phase 3 gỡ `getForMeeting` (feature meeting-chon-du-an-tkt)
      → đồng bộ `meeting-mobile.pen` (màn 06 chỉ xem, gộp Thành phần + Điểm danh) → đề xuất gộp ~25 API lúc mở màn Sửa meeting.
Blocked: chờ user review / cho phép từng việc tiếp theo.
