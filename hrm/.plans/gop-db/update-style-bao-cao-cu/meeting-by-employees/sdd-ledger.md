# SDD ledger — plan: /Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/gop-db/update-style-bao-cao-cu/meeting-by-employees/plan.md

Spec: /Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/docs/superpowers/specs/gop-db/2026-10-05-update-style-bao-cao-meeting-theo-nhan-vien-design.md
Worktrees: /Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-update-style-mbe/{hrm-api,hrm-client} · branch gop_db-update-style-meeting-by-employees · base api 8de764f79 / client 2f04d1dfb
Servers: api 8019 (php@7.4 artisan serve) · client 3019 (nuxt, node 12)
Ruling: Workspace SDD đặt ở .plans/…/meeting-by-employees/sdd/ vì HRM/ không phải repo git (script sdd-workspace fail) — nếu sai: chỉ là chỗ để file.
Ruling: Task 1 (worktree) controller tự làm — dựng môi trường, không code — nếu sai: không ảnh hưởng code.
Task 1: complete (worktree, vendor/node_modules copy từ wt-update-style-mbp, autoload trỏ wt-update-style-mbe, .env client 3019/8019)

## Pre-flight scan

Quét 05/10/2026 trên plan.md + spec + design.md (19 câu), đối chiếu code nền worktree `wt-update-style-mbe` (api 8de764f79, client 2f04d1dfb) + DB local `hrm_erp` (chỉ SELECT).

### A. Cặp task dùng chung file / interface

| # | Bên tạo → bên dùng | Interface | Phát hiện |
|---|---|---|---|
| A1 | T2 → T3 | `leaves(Request,bool)`, `leafQuery(Request,array,bool)`, `participantKeys(array)`, `meetingDetails(array,array)`, `meetingRow(array,array)`, `viCompare` | khớp: tên, chữ ký, thứ tự tham số đều đúng; T3 `companyMembers` gọi `leafQuery($r, [], false)` đúng chữ ký |
| A2 | T2 → T4 | `leafQuery($r, $skip, false)`, `viCompare`, `MODES`, `PERM_ALL` | khớp |
| A3 | T2/T3 → T5 | `index($r,true)`, `itemRows()->all()`, `participantRows`, `employeeRows`, `period`, `PRINT_COLUMNS`, `breakdownText/typeText/timeText` | khớp; `index` trả `groups[].departments[].employees[].meetings[]` đúng như `renderSummary/renderDetail` duyệt |
| A4 | T2 → T6 | `hasReportPermission()`, `applyEmployeeScope($q,'i','e')` public | khớp |
| A5 | T2 (controller tối thiểu) → T4 (thay) | `filterOptions` route `-v2/filter-options` | khớp; test T2 chỉ đọc `can_change_company` mà bản tối thiểu có trả |
| A6 | T2/T3/T5 route → T9 đổi tên | 2 + 3 + 5 = 10 route `-v2` | khớp với "đổi 10 route" và `grep -c = 10` sau khi xoá 6 route cũ (api.php hiện có đúng 6 dòng `meeting-by-employees` 1197–1202) |
| A7 | T2/T3/T5 (BE) → T7/T8 (FE) | `summary{employees,meetings,duration,participants,by_status,by_mode,by_type}`, `groups`, `meta{total,per_page,current_page,period_label,from,to}`, `item-list meta.minutes`, `employees[].in_scope` | khớp với khoá FE dùng |
| A8 | T7 → T8 | emit `drill`, `drill-people`, `drill-employees`, `open-meeting`, `open-minutes`; stub `onDrillEmployees` | khớp |
| A9 | T8 PrintOptionsModal → T8 index | `print({mode, columns[]})` → `columns.join(',')` → BE `columns` chuỗi khoá `PRINT_COLUMNS` | khớp (khác nền MBP emit `print(mode)` chuỗi — plan đã đổi cả 2 đầu) |
| A10 | T5 PrintService → test T5 | override `protected function printListPayload(string $html, int $total): array` | khớp chữ ký trait `LimitsPrintListRows` (protected, cùng kiểu); `printListMaxRows()` public static |
| A11 | T5 controller → `MeetingByProjectsParticipantExport` (có sẵn) | `(new …)->forRows($data, string $letterhead, string $scopeLabel = '', array $meta = [])`, constructor rỗng | khớp; blade chỉ nhắc "dự án" ở comment |
| A12 | T5 Report Export → test T5 | `forReport(array $report, string $letterhead, string $scopeLabel)` | khớp khuôn MBP `forReport($data, string, string='')`; bố cục dòng 6 TỔNG / 7 I / 8 "1" / 9 "1.1" khớp assert `A6`, `G6`, `A9` |
| A13 | T2 Fixture → T3/T4/T5/T6 tests | `day`, `employeeWhere`, `freshCustomers`, `makeProject`, `makeMeeting`, `emp`, `grant`, `manageDepartment`, `actAs`, `cleanupMeetingFixture` | khớp; cùng file trait dùng chung |
| A14 | T6 `Meeting::canView` ↔ T8 Playwright (1058 mở meeting không tham gia) | thứ tự: T6 trước T8 | khớp |
| A15 | T9 "Modify tests: URL (4 file)" ↔ test thực có `URL` | ReportApiTest, DrillApiTest, ExportPrintTest (MeetingCanViewTest không có URL) | lệch nhỏ: 3 file chứ không phải 4. Đề xuất ruling: sửa 3 file có `URL` — chỉ là đếm sai trong plan — giá nếu sai: 0 |

### B. Tự nhất quán từng task

| Task | Phát hiện |
|---|---|
| T2 | Nhất quán. 12 test khớp "Expected 12 PASS". Số kỳ vọng tính lại khớp fixture: 210 = 60×3+30; phòng 42 = 150; phòng 5 = 60; Hủy 0 phút → 60; người tham gia 4 (A, B, NV cty 2, KH). DB đã kiểm: 27/28 công ty 1 phòng 42, 1180 công ty 1 phòng 5, 28 chỉ có quyền 1004 (không có 1057–1059), 28 không quản lý phòng nào, công ty 2 có 14 NV, `meeting_types.id=2` status 1, có cột `description`, `code` ở companies/departments, `employee_work_position_id`. Có 1 lệch nhỏ với spec (C-x1 bên dưới). |
| T3 | Nhất quán. 4 test → tổng 16 khớp. `minutes` 120 = 0 (Hủy) + 60 + 60; `scope_employee_id=B` → 2; cờ `in_scope` [A=>true, c2=>false] đúng thứ tự `sort_order`; participant 4 / company 2 / meeting m1 3 / scope B 3 khớp khoá `MeetingParticipantCounter::key`; employee A {2, 90}, Σ 150 = summary. `eq` = mã 1180 "E2E-ASSIGN" (duy nhất). |
| T4 | Nhất quán. 1 test → 17. `employeeOptionLabel()` nhận mảng có `fullname/code/department_code` (FormatHelper:1254 — đúng). `current_company_role` của 28 = `company_role ?: company_id` = 1 → `companies` = [1] đúng. |
| T5 | Nhất quán. 4 test → 21. Print service + 4 blade + 3 export + 5 route khớp file map. Tên view `prints.assign.meeting_by_projects_participants` có sẵn. |
| T6 | Nhất quán. 3 test → 24. Mốc `assertFalse` trước khi cấp đã kiểm DB: 28 không có quyền "Xem danh sách meeting …", meeting fixture `created_by/host` = 27, meeting không gắn dự án → `canViewByMeetingByProjectsReport` false. `canView()` hiện tại đúng 4 nhánh như plan chép lại (Meeting.php:639). |
| T7 | Nhất quán. File copy nguồn đều tồn tại (`meeting-by-projects/{api.js,format.js,components/DrillNum,InfoTip,MeetingSummary,MeetingTree}`), template `TrackingTable.vue` có padding 30/52/74/96px, mockup `COLS` ở dòng 2811–2825, `V2BasePagination` có `itemLabel` + `pageSizeOptions`. Tài khoản kiểm: `e2e_cmd_noperm@test.local` (id 1184) có trong DB; 1180 có 1057/1058/1059. |
| T8 | Nhất quán. CSS `.mbe-print-cols / .column-list / .fixed-columns-note` có trong `mk-extra-css` của mockup (dòng 2601–2607). |
| T9 | Nhất quán trừ đếm "4 file" test (A15). Danh sách xoá khớp spec §4: 5 Transformer chỉ còn `ReportController` dùng (đã grep), 6 method + DI `meetingByEmployeesService` (dòng 41–47). Comment `BaseMeetingChart.vue:132` và `CareTrackingTable.vue:25` đúng dòng. |
| T10 | Nhất quán; chỉ viết, không chạy; truyền env cổng 8019/3019. |

### C. Đối chiếu plan ↔ spec ↔ design.md

| # | Quyết định | Plan | Phát hiện |
|---|---|---|---|
| C1 | #2 #11145, Hủy 0 phút | `applyMeetingFilters` + `CASE WHEN status=HUY THEN 0` | khớp |
| C2 | #2 "thiếu giờ bắt đầu → Hoàn thành/Hủy" | R2: thiếu `start_date` không vào kỳ → không tính | lệch design ↔ spec, KHÔNG phải lỗi plan (spec §3.1 + R2 đã chốt, local 0 dòng). Đề xuất ruling: giữ R2 theo spec — spec thắng, local 0 meeting thiếu giờ — giá nếu sai: thêm 1 nhánh OR trong `applyMeetingFilters` |
| C3 | #12 phút-người | `totals.duration = Σ leaves`, test Σ con = cha | khớp |
| C4 | #13 popup NV | `employee-list` 7 cột (T3 BE + T8 FE), test số dòng = `summary.employees` | khớp |
| C5 | #14 in đậm NV trong phạm vi | `companyMembers` + `in_scope` theo phạm vi báo cáo (R4), FE `<b>` | khớp |
| C6 | #15 chọn cột cả 2 bản + Chi tiết NV×meeting | `columns()` áp summary + detail, `renderDetail` NV×meeting có Công ty/Phòng/NV, test 2 bản | khớp |
| C7 | #16 KH meeting fallback dự án | `meetingDetails` fallback + lọc `m.customer_id OR pp.customer_id` + test meeting không dự án | khớp phần cột + lọc. Lệch nhỏ: ô tìm `q` chỉ dò `m.customer_name/code`, không dò KH dự án khi meeting thiếu KH. Đề xuất ruling: thêm `pp.customer_code/pp.customer_name` vào `orWhereExists` của `q` — cột KH hiện KH dự án thì tìm cũng phải ra (#16) — giá nếu sai: tìm theo tên KH bỏ sót meeting chỉ có KH qua dự án (hiện 0 dòng local) |
| C8 | #17 Excel cây 13 cột, không popup | Report Export A..M 13 cột, `/export` không `mode/columns` | khớp |
| C9 | #18 danh mục chỉ có meeting trong kỳ, giữ mục đang chọn | `filterOptions` từ `leafQuery` (bỏ khoá đơn vị) + FE `keepSelectedOptions`, `loadOptions` khi đổi Kỳ/Công ty | khớp |
| C10 | #19 quyền 1059 giữ cũ | `applyEmployeeScope` phòng/bộ phận quản lý, không cộng chính mình; test 1059 | khớp với bản cũ `buildMemberPermissionConstraint` |
| C11 | #4 phân trang theo NV 20/trang, dòng cha tổng đủ, mặc định bung tới NV | `index` + test trang 2; FE `level: 3`, `perPage: 20` | khớp |
| C12 | #5/#6/#8/#10/#11/#3/#9 | khối tổng hợp 2 khối, 13 cột, 9 ô lọc, PrintOptionsModal + chọn cột, đơn vị hiện tại, bỏ chart, nới canView | khớp |
| C13 | spec §3.2 "department_id 0 = chưa có phòng" | `applyEmployeeFilters` dùng `where('i.department_id', 0)` — không khớp NULL | lệch nhỏ (C-x1). Đề xuất ruling: dùng `whereIdOrUnset` cho `department_id` của bộ lọc báo cáo — spec §3.2 ghi rõ, hàm đã có sẵn — giá nếu sai: hiện FE không gửi 0 (danh mục bỏ phòng rỗng) nên chỉ lộ khi gọi API tay |
| C14 | spec §6 "Excel … SĐT là chuỗi" | không có assert SĐT trong test MBE | lệch nhỏ: plan dựa vào `MeetingByProjectsParticipantExport` (đã có test chuỗi ở MBP). Đề xuất ruling: chấp nhận, không thêm test — class dùng lại nguyên, đã được test MBP phủ — giá nếu sai: 0 (cùng class) |
| C15 | Trạng thái tài liệu | plan dòng 6 ghi "ĐƯỢC PHÉP CODE — user trả lời 'làm' 05/10/2026"; design.md dòng 5–7 vẫn ghi "Chưa code — cần câu 'làm' riêng" và "15 câu" (bảng đã 19) | lệch tài liệu. Đề xuất ruling: controller xác nhận câu "làm" có thật trong hội thoại trước khi dispatch Task 2, rồi sửa dòng trạng thái design.md — CLAUDE.md bắt buộc sự cho phép rõ ràng — giá nếu sai: code khi chưa được phép (vi phạm quy tắc gốc) |

### D. Chỗ review dễ bắt lỗi / gọi API không tồn tại

| # | Điểm | Kiểm ở worktree | Phát hiện |
|---|---|---|---|
| D1 | `MeetingByProjectsReportService::period()` | public, `Request → [Carbon from, Carbon to, string label]`, custom sai → `ValidationException` (422) | tồn tại, khớp |
| D2 | `MeetingByProjectsReportService::MODES / UNSET_TYPE_NAME / UNSET_MODE_NAME` | `const` (public) | tồn tại |
| D3 | `MeetingParticipantCounter::keys(array)` | trả Collection `{meeting_id:int, key:string}`; `listFor(array $ids, array $customerNameByMeeting)` trả mảng `{side,name,position,unit,phone,meeting_count}` | khớp đúng plan dùng |
| D4 | `isCurrentEmployeeHasPermission`, `listManageDepartmentIds`, `listManagePartIds` | helper global ở `app/Helper/PermissionHelper.php` (20, 244, 273) | tồn tại |
| D5 | `htmlToText`, `employeeOptionLabel` | `app/Helper/FormatHelper.php:1215, 1254` | tồn tại |
| D6 | `Meeting::{HOAN_THANH,HUY,CHOT_LICH,LEN_LICH,PAST_REPORT_STATUSES,FUTURE_REPORT_STATUSES,resolveStatusName,resolveStatusColor}`, `ProspectiveProject::STATUS_DANG_TAO` | Meeting.php 186–252, ProspectiveProject.php:112 | tồn tại |
| D7 | `ApiController::responseJson` bọc `data`; `TpEmployee` (bảng `employees`, có `current_company_role`); `RequestCache::flush`; guard mặc định `api` | đã đọc | tồn tại → test đọc `json('data')` và gọi service trực tiếp sau `actAs` đều chạy |
| D8 | `PrintsCompanyLetterhead` (Modules/Assign/Services/Concerns), `LimitsPrintListRows` (Modules/CustomerCare/Services/Concerns) | đã có | tồn tại |
| D9 | Nhân bản code | `typeText()` + `timeText()` của plan chép gần nguyên `MeetingByProjectsReportService::typeText/timeText` (public static) | review sẽ bắt. Đề xuất ruling: `timeText` uỷ quyền `MeetingByProjectsReportService::timeText($m)`; `typeText` uỷ quyền tương tự (tên nhóm 0 đã là UNSET ở leaf) — giữ `breakdownText` riêng vì nhãn "Đã hủy" khác — tránh nhân bản — giá nếu sai: 2 bản lệch nhau khi sửa 1 chỗ |
| D10 | Hiệu năng `participantRows` | gọi `meetingDetails($ids, [])` (nạp content + `htmlToText` + dự án cho MỌI meeting) chỉ để lấy tên KH | review có thể bắt (spec §3.6: chi tiết chỉ nạp cho meeting trên trang). Đề xuất ruling: chấp nhận ở plan, implementer có thể tách 1 query nhẹ `id → customer_name (fallback dự án)` nếu gọn — popup người tham gia vốn lấy trọn tập — giá nếu sai: chậm hơn chút khi kỳ lớn, không sai số |
| D11 | Test không assert gì / assert yếu | `test_ban_in_vuot_tran_thi_bi_chan` giả `printListPayload` (trần 0) → chỉ chứng minh 5 chế độ đi qua payload, không chứng minh trần thật | chấp nhận (khuôn MBP y hệt). Không có test rỗng assert |
| D12 | Bộ lọc `q` của MBP không escape `%/_` | `MeetingByProjectsReportService::meetingQuery` dòng ~98 | ngoài luồng (báo cáo 1), plan MBE đã escape. Ghi danh sách ngoài luồng, không vá trong đợt này |
| D13 | `me.type` là varchar | `where('me.type', 1)` loại 5 dòng `'company'` (MySQL ép 'company' → 0) | khớp spec §3 (loại như bản cũ) |

## Rulings sau pre-flight
Ruling: Câu "làm" có thật — user trả lời "Làm" cho câu hỏi phạm vi (worktree, nhánh, commit nhánh, PHPUnit DB local) 05/10 — design.md cập nhật trạng thái — nếu sai: không áp dụng.
Ruling: C13 lọc department_id=0 dùng whereIdOrUnset (khớp NULL hoặc 0) theo spec §3.2 — spec thắng plan — nếu sai: chỉ lộ khi gọi API tay.
Ruling: C7/#16 ô tìm q dò cả pp.customer_code/name (KH dự án fallback) — cột hiện gì thì tìm ra cái đó — nếu sai: thừa 1 điều kiện OR.
Ruling: D9 typeText/timeText uỷ quyền sang MeetingByProjectsReportService (public static), giữ breakdownText riêng (nhãn "Đã hủy") — tránh nhân bản — nếu sai: đổi lại copy, rẻ.
Ruling: A15 Task 9 đổi URL ở 3 file test có URL (không phải 4) — đúng thực tế — giá 0.
Ruling: C14 không thêm test SĐT chuỗi ở báo cáo này — dùng lại MeetingByProjectsParticipantExport đã có test MBP — nếu sai: thiếu 1 test trùng.
Ruling: D10 participantRows chấp nhận nạp meetingDetails; implementer được tách query nhẹ nếu gọn — nếu sai: chậm chút, không sai số.
Ruling: C2 meeting thiếu start_date KHÔNG tính (spec R2 thắng design #2; local 0 dòng; không có kỳ nào chứa được nó) — nếu sai: thêm 1 nhánh OR.
Note NGOÀI LUỒNG: MeetingByProjectsReportService::meetingQuery ô q không escape %/_ (báo cáo 1, đã merge) — báo user, không vá.
Task 2: dispatched (BASE api 8de764f79, opus)
Task 2: implementer DONE_WITH_CONCERNS 4d6a35f06 — dept=0 chưa có dữ liệu thật; sort SQL collation (Collator chỉ by_type)
Task 2: review dispatched (opus)
Ruling: ⚠️ nhóm đơn vị 0 (NULL/0) chấp nhận qua đọc code (whereIdOrUnset, cùng hàm đã test ở MBP); bổ sung fixture NULL ở đợt fix cuối nếu final review yêu cầu — nếu sai: lọc "Chưa xác định" ra rỗng, chỉ khi có NV thiếu phòng.
Task 2: minor (deferred): test 1059 chưa chứng minh loại chính mình (#19) + chưa phủ nhánh quản lý bộ phận (part)
Ruling: Lọc KH khớp meeting.customer OR project.customer trong khi ô hiện meeting.customer trước — meeting có KH X, dự án KH Y lọc Y vẫn ra dòng hiện X — chấp nhận: meeting đó đúng là "gắn" KH Y qua dự án — nếu sai: user thấy dòng hiện KH khác ô lọc; sửa ô hiện cả 2.
Task 2: minor (deferred): MBP::timeText dùng !$m['start_date'] (undefined index nếu thiếu khoá; hiện luôn có)
Task 2: minor (deferred): TDD RED giả (đổi route); test R2/escape không có RED thật
Task 2: minor (deferred): index nạp mọi lá của kỳ, tính PHP — đo tải năm/1057 trước Task 9
Task 2: complete (commits 8de764f79..4d6a35f06, review clean)
Task 3: dispatched (BASE 4d6a35f06, sonnet)
Task 3: implementer DONE e659a9b8f (18+28 tests xanh); review dispatched (opus)
Ruling: ⚠️ keys() vs listFor() của MeetingParticipantCounter gộp cùng cách — đã chốt bởi test MBP + fixture 4==4 ở đây; lộ tên NV ngoài quyền đã ghi ở design #14 — nếu sai: popup lệch ô tổng hợp, e2e bắt được.
Task 3: minor (deferred): usort người tham gia thiếu tiebreak (phone/unit) → thứ tự Excel/in đổi giữa lần gọi
Task 3: minor (deferred): participantRows nạp meetingDetails đầy đủ chỉ để lấy tên KH (nặng kỳ năm)
Task 3: minor (deferred): per_page = 0 khi rỗng → max(1, …)
Task 3: minor (deferred): DrillApiTest thiếu scope_*=0, side=customer/pq, ca KHÔNG quyền cho drill
Task 3: complete (commits 4d6a35f06..e659a9b8f, review clean)
Task 4: dispatched (BASE e659a9b8f, sonnet)
Task 4: implementer DONE e966ac4ac (20+28 xanh); review dispatched (sonnet)
Ruling: ⚠️ scope 1059 + NV đã nghỉ trong filter-options — đi qua cùng leafQuery/applyEmployeeScope đã test ở Task 2 (1059) — chấp nhận — nếu sai: danh mục rộng hơn bảng, không lộ số.
Task 4: minor (deferred): customer_id = 0 lọt option ma → where > 0
Task 4: minor (deferred): danh sách dự án khi đã chọn dự án chỉ bỏ project_id (khác $linked) — lệch nhẹ
Task 4: minor (deferred): không có option nhóm "chưa có phòng/bộ phận" dù BE nhận 0
Task 4: minor (deferred): loại meeting chỉ status=1 → loại đã khoá có meeting trong kỳ vắng khỏi ô lọc (cần giữ như skill select-and-input-state)
Task 4: minor (deferred): company/type sort SQL không Collator; test mỏng (parts, types, 1059, kỳ, KH dự án, can_change_company=true); test hard-code id 5/1
Task 4: complete (commits e659a9b8f..e966ac4ac, review clean)
Task 5: dispatched (BASE e966ac4ac, sonnet)
Task 5: implementer DONE_WITH_CONCERNS 3b20db8a4 (27+28 xanh) — chưa tải xlsx thật soi logo/định dạng (kiểm ở Task 8 qua FE); BE columns rỗng/lạ → in đủ cột (FE chặn rỗng)
Task 5: review dispatched (opus)
Task 5: review — Important: Excel cột Nội dung thiếu nl2br(e()) (export-excel §1b) → nhiều dòng dính liền; kèm minor sửa luôn: blade in summary/detail nl2br, colspan dòng rỗng detail thừa +1
Task 5: minor (deferred): logic Dự án/KH chép 5 blade + 3 Export gần giống nhau (theo khuôn MBP); test tạo xlsx tạm 2 kiểu
Ruling: ⚠️ tải xlsx thật qua ?token= kiểm logo/định dạng → làm ở Task 8 (FE) bằng Playwright — nếu sai: lỗi định dạng lộ khi user tải.
Task 5: fix round 1/5 dispatched (resume implementer, FIX_BASE 3b20db8a4)
Task 5: fix round 1 implementer DONE b843ed83e (28+28 xanh); re-review dispatched (sonnet)
Task 5: fix round 1/5 (3 addressed, 0 open; commits 3b20db8a4..b843ed83e)
Task 5: complete (commits e966ac4ac..b843ed83e, review clean)
Task 6: dispatched (BASE b843ed83e, sonnet)
Task 6: implementer DONE 52db7dab8 (31+28+76 xanh); review dispatched (sonnet)
Ruling: ⚠️ EOL Meeting.php — controller kiểm numstat (chỉ dòng sửa) ; fixture helper có từ Task 2 — chấp nhận.
Task 6: minor (deferred): test 1059 chưa phủ nhánh part_id + quản lý đồng thời là thành viên
Task 6: complete (commits b843ed83e..52db7dab8, review clean)
Task 7: dispatched (client BASE 2f04d1dfb, api HEAD 52db7dab8, opus)
Task 7: implementer DONE_WITH_CONCERNS bb9e9ed82 — đo DOM đạt (thụt 30/52/74/96, sticky, 619 meeting = TỔNG, trang 2 tổng đủ); concerns: filter-options nạp lại mọi lần đổi ô; STT La Mã theo trang; InfoTip mục đích dùng câu brief không dùng mockup
Ruling: filter-options nạp lại mỗi lần đổi ô (BE lọc chéo theo ô khác, #18) — đúng hành vi danh mục chéo — nếu sai: thừa request, keepSelectedOptions giữ mục chọn.
Task 7: review dispatched (opus)
Task 7: review — Important: (1) STT đánh lại theo trang trái mockup j (công ty lặp trang 2 phải giữ "II", phòng "2"); (2) InfoTip mục đích dùng câu brief, không theo 4 dòng mockup
Ruling: STT liên tục giữa các trang theo mockup j — BE index trả company_no/department_no (vị trí trong danh sách đủ đã sắp) + employee_no (thứ tự NV trong phòng trên toàn tập); FE dùng số đó — mockup đã duyệt thắng brief; mở lại file Task 2 (cùng service, thêm test) — nếu sai: chỉ là số STT.
Ruling: InfoTip mục đích dùng 4 dòng mockup, NHƯNG dòng #11145 bỏ vế "thiếu giờ bắt đầu → Hoàn thành/Hủy" vì ruling C2 (không tính meeting thiếu start_date) — nếu sai: đổi 1 câu chữ.
Task 7: minor (deferred): goal meta thiếu "· n phòng ban" (thêm nếu summary có); loadOptions nuốt lỗi im lặng
Ruling: ⚠️ ca không quyền thấy dòng của chính mình chưa chứng minh trên UI (1184 không có meeting) — đã có test BE Task 2; e2e Task 10 phải seed — nếu sai: lỗi fail-closed quá chặt, không lộ dữ liệu.
Task 7: fix round 1/5 dispatched (resume implementer, FIX_BASE client bb9e9ed82 / api 52db7dab8)
Task 7: fix round 1 implementer DONE api ebc0b2090 client 2892c3fef (32 tests xanh); re-review dispatched (sonnet)
Task 7: fix round 1/5 (2 addressed, 0 open; commits api 52db7dab8..ebc0b2090, client bb9e9ed82..2892c3fef)
Task 7: complete (client 2f04d1dfb..2892c3fef, api ..ebc0b2090, review clean)
Task 8: dispatched (client BASE 2892c3fef, api HEAD ebc0b2090, opus)
Task 8: implementer DONE_WITH_CONCERNS c86f8a5ca — popup = ô bấm (9 ô tổng hợp, phòng, NV, loại, người 706), in đậm đúng in_scope, in chọn cột đúng, Excel #,##0 + chuỗi; concerns: Excel cắt chữ dài (cột tên/loại/NV tham gia không wrap), logo không kiểm được (ảnh letterhead thiếu ở local), tiêu đề popup lặp "Người tham gia: Người tham gia", chưa thử 1058
Task 8: review dispatched (opus)
Task 8: review Approved; Important (vùng Task 5 BE): Excel cắt chữ dài (cây B, loại H, popup NV tham gia I, J/K, công ty popup NV) → wrap + vertical top — coi là gap thật, sửa ngay
Ruling: sửa Excel wrap trong vòng fix của Task 8 (implementer Task 8 đã soi xlsx thật) dù code ở hrm-api — người có dữ liệu đo nắm rõ nhất — nếu sai: không ảnh hưởng.
Ruling: ⚠️ kiểm UI bằng tài khoản chỉ 1058 cần tạo role tạm vào DB local — ngoài phạm vi user cho phép (chỉ PHPUnit fixture) → dựa test BE Task 6 (1058 canView) + báo user — nếu sai: drawer 403 với user 1058, e2e/QA bắt.
Ruling: ⚠️ logo Excel/in không kiểm được ở local (ảnh letterhead thiếu trên đĩa) — môi trường, kiểm trên staging — báo user.
Task 8: minor gộp vào fix: tiêu đề popup từ khối tổng hợp ("Tất cả meeting"/"toàn bộ báo cáo" theo mockup) + default 'Tất cả meeting'; bỏ listener open-minutes chết
Task 8: minor (deferred): khối sortedRows chép 3 modal (giống MBP); z-order preview in trên popup chưa đo → e2e Task 10
Task 8: fix round 1/5 dispatched (resume implementer; FIX_BASE client c86f8a5ca, api ebc0b2090)
Task 8: fix round 1 implementer DONE api 518a268dc client e599c3917 (33 tests; xlsx cắt chữ 2085/2/1 → 0); re-review dispatched (sonnet)
Note NGOÀI LUỒNG: MeetingByProjectsParticipantExport (dùng chung 2 báo cáo) cột Đơn vị bị SĐT đè — sửa sẽ đổi cả báo cáo 1 → báo user, không vá
Task 8: fix round 1/5 (3 addressed, 0 open; api ebc0b2090..518a268dc, client c86f8a5ca..e599c3917)
Task 8: minor (deferred): trait WrapsTableTextColumns tìm "STT" cột A, không thấy thì im lặng bỏ wrap
Task 8: complete (client 2892c3fef..e599c3917, api ..518a268dc, review clean)
Task 9: dispatched (api BASE 518a268dc, client BASE e599c3917, sonnet)
Task 9: implementer DONE api 52f31f9c2 client e32b1862e (33 + 97 tests xanh, 10 route, nuxt 3019 restart PID 15595); review dispatched (sonnet)
Task 9: minor (deferred): comment PrintOptionsModal.vue:5 còn "-v2/print-list-data"; comment dòng 39/259 trỏ file đã gỡ
Task 9: complete (api 518a268dc..52f31f9c2, client e599c3917..e32b1862e, review clean)
Task 10: dispatched (sonnet) — e2e chỉ viết, không chạy
Task 10: implementer DONE_WITH_CONCERNS (Step 1-2) — 10 api + 11 ui ca, --list 24 tests OK; selector popup/In chưa kiểm thật; UI cô lập bằng kỳ 15/03/2001; không quyền = NV fixture không role
Task 10: review dispatched (sonnet, đọc file — e2e ngoài git không có diff)
Final review: dispatched (opus) — api 8de764f79..HEAD, client 2f04d1dfb..HEAD
Task 10: review — Important: ca API 1 assert filter-options rỗng cho người không quyền — sai (phạm vi = chính mình → employees=[viewer]) → cả suite serial "did not run"
Task 10: minor gộp vào fix: fixture hard-code đường dẫn worktree (ưu tiên API_REPO, fail rõ); ca 10 dùng mã NV thay tên
Task 10: fix round 1/5 dispatched (resume implementer)
Task 10: fix round 1/5 (3 addressed, 0 open; e2e ngoài git)
Task 10: complete (Step 1-2; e2e CHƯA chạy theo quy tắc)
Final review: With fixes — I1 ô tìm popup meeting (FE lọc dự án đầu/KH hiện) lệch BE q (mọi dự án gắn + KH dự án) → In/Excel popup ra dòng màn không hiện; I2 sort người tham gia thiếu tiebreak; I3 loại meeting đã khoá biến mất khỏi ô lọc; I4 thiếu test quyền cho drill + 1059 (tự thấy mình / part)
Ruling: I1 sửa bằng cách BE item-list trả thêm search_text (mã+tên MỌI dự án gắn + KH meeting + KH dự án) cho mỗi dòng, FE lọc trên trường đó — giữ ngữ nghĩa BE q (đã test), 2 phía khớp — nếu sai: thừa vài trường JSON.
Ruling: Minor 1 applyEmployeeScope dùng whereRaw('1=0') thay [0] khi không quản lý gì — chặn rò nếu prod có part_id/department_id = 0 — nếu sai: không ảnh hưởng.
Final fix wave: dispatched (opus) — FIX_BASE api 52f31f9c2 client e32b1862e
Final fix wave: implementer DONE api 5b7934f3e client b442bc862 (40 + 97 xanh); report ghi bởi controller; scoped re-review dispatched (sonnet)
Final fix: re-review all addressed (api 52f31f9c2..5b7934f3e, client e32b1862e..b442bc862; 40 + 97 tests green)
Final fix: minor (deferred): search_text nối ' | ' có thể khớp xuyên trường; e2e chưa có ca tìm mã dự án thứ 2 + option 🔒 ô Loại
