# Plan — Góc học tập cá nhân + Tìm kiếm global

- **Người phụ trách:** @junfoke
- **Spec:** `docs/superpowers/specs/2026-06-05-goc-hoc-tap-ca-nhan-design.md`
- **Plan chi tiết (đầy đủ code):** `docs/superpowers/plans/2026-06-05-goc-hoc-tap-ca-nhan.md`
- **Trạng thái:** Plan DONE (16 task) → chờ user chọn cách thực thi.

> Checklist rút gọn dưới đây; chi tiết code + verify từng task ở plan đầy đủ. Verify bằng `npm run lint` + `npm run build` + browser (KHÔNG commit/push, KHÔNG test harness).

## Phase 1 — Trang Góc học tập cá nhân (`/goc-hoc-tap`)
- [x] Cài `apexcharts` + `vue3-apexcharts`, đăng ký ở `main.js`
- [x] Thêm route `my-learning` + nối nút header
- [x] `constants/myLearningMock.js` (bổ sung `slug`)
- [x] `stores/myLearning.js` (state + getters + fetchAll)
- [x] `MyLearningView.vue` + `WorkspaceTabs.vue`
- [x] `OverviewTab.vue` + `ProgressRing.vue` (ApexCharts radialBar)
- [x] `RequirementTab.vue` + `RequirementTable.vue` (2 bảng)
- [x] `LearningTab.vue` + `StudyCard.vue` + filter cục bộ
- [x] `CertificateTab.vue`
- [x] `LearningDetailDrawer.vue`
- [x] Wiring nút → trang thật (detail/learn/certificate)
- [x] Skeleton/empty states

## Phase 2 — Tìm kiếm global (kiểu f8.edu.vn)
- [x] `composables/useDebounce.js` + `useClickOutside.js`
- [x] `stores/search.js` (searchSuggest + searchAll)
- [x] `GlobalSearch.vue` (popup) — thay ô search tĩnh trong `AppHeader.vue`
- [x] Route `search` + `SearchResultView.vue` (`/tim-kiem`)
- [x] Badge lọc loại nội dung + section + "Xem thêm"
- [x] Seed `keyword` từ query ở `LearningByCategoryView` / `LearningPathListView` (useListPage đã tự seed qua `readQueryParams()` — không cần sửa)
- [x] Loading/empty/lỗi states

## Phase 3 — Nối API thật cho 4 tab (2026-06-05)
Quyết định: nối cả 4 tab; cert tự sinh mã + không hết hạn (không bảng mới); deadline giữ UI hiện "—"; vòng tiến độ = % tiến độ tổng thể. Chi tiết: spec mục 10.
- [x] BE: `MyLearningController::learningSpace` + route `GET my/learning-space` (middleware elearning.auth)
- [x] BE: `MyLearningService` — query enrollment status 1/2 (in_progress), status 3 + certificate_enabled (certs), mandatory chưa done (required) qua MandatoryChecker; build shape khớp FE
- [x] BE: map item (RequiredItem/LearningItem/CertItem) — cert sinh mã CERT-KH/LT-<id padded 5>
- [x] FE: `stores/myLearning.js` fetchAll → gọi API thật, map state
- [x] FE: vòng tiến độ = avg progress + label 'Tiến độ tổng thể'; deadline "—" (RequirementTable + OverviewTab.splitDate); upcoming derive từ requirementItems; LearningTab filter ngày dùng new Date() thật
- [x] Verify: php -l sạch + route đăng ký (api/v1/elearning/my/learning-space) + tinker data thật (employee 13: 1 khóa đang học; learner: 1 cert CERT-KH-00006 + 1 khóa đang học, shape khớp FE) + FE lint+build PASS. Browser: chờ user.

## Phase 4 — Hạn hoàn thành (CODE DONE 2026-06-06, chờ user chạy migrate)
Quy tắc: `deadline = enrolled_at + complete_within_days`. Quyết định: Q1 = field chung mới `complete_within_days` (cả subjects + learning_paths); Q2 = item chưa enroll → deadline null ("—"). Chi tiết: spec mục 11.
- [x] BE migration `complete_within_days` (subjects + learning_paths) — TẠO FILE, CHƯA CHẠY (database/migrations/2026_06_06_100000_...). **User chạy `php artisan migrate`**
- [x] BE validate + save: SubjectBuilderRequest + SubjectService + SubjectDetailResource; LearningPathRequest + LearningPathService (store+update) + LearningPathDetailResource
- [x] BE compute deadline ISO trong MyLearningService (computeDeadline = Carbon enrolled_at + N; required chỉ khi đã enroll, in_progress luôn). Graceful pre-migration (field null → deadline null, không crash)
- [x] hrm-client form: Subject TabLearners (field chung, ngoài onboarding) + LP TabResult (prop completeWithinDays + emit). SubjectBuilderForm/LearningPathForm: data + load + keys
- [x] elearning FE: RequirementTable (format dd/mm/yyyy + useDeadline pill); store upcomingDeadlines (format + sort); StudyCard (deadline pill)
- [x] Verify: php -l 8 file sạch; FE lint+build PASS; tinker no-crash pre-migration + Carbon math đúng (2026-05-21+30=2026-06-20)
- [x] Detail page (CODE DONE 2026-06-06): helper chung `Modules/Elearning/Support/DeadlineHelper` (refactor MyLearningService dùng chung). SubjectDetailController (additional `deadline`) + LearningPathDetailController (fetch LP enrollment + inject `deadline`). FE subjectDetail.js + learningPathDetail.js map `deadline` vào entity. DetailEnrollCard + DetailHero: nới điều kiện (chỉ cần `entity.deadline`, bỏ gate isMandatory + subject-only) + format dd/mm/yyyy qua `useDeadline.formatDmy`. Verify php -l + lint + build PASS.
- [x] Browse cards deadline (2026-06-06, user yêu cầu làm): BE PublicBrowseController build `_deadline_map` (helper buildDeadlineMap, tái dùng DeadlineHelper + enrolled_at map per-user) cho subjects + learning-paths; SubjectBrowseResource + LearningPathBrowseResource thêm field `deadline` (safe access tránh notice ở homeContent). FE: LearnCard format ngày (useDeadline.formatDmy) + bật `:show-deadline` ở LearningByCategory/LearningBySkill/SearchResult; PathCard thêm pill deadline (trước đó không có UI). Chỉ hiện item user đã enroll + có cấu hình. Verify php -l + lint + build PASS.

## Phase 5 — Hoàn thành lộ trình + đếm theo đơn vị gốc (2026-06-06)
Phương án user chốt: (1) Đếm "Đang học"/"Đã hoàn thành" = số lộ trình + số khóa lẻ (KHÔNG đếm khóa con của path). (2) Xong cả khóa con → path mới "Đã hoàn thành". (3) Thẻ phân biệt: khóa lẻ `[Khóa học]` "Bài x/y", lộ trình `[Lộ trình]` "Khóa x/y" + nút bung khóa con (inline) + nút chi tiết. (4) Khóa lẻ đã học → enroll path → kế thừa tiến độ + ẩn thẻ lẻ (dedup).
- [x] BE auto-complete lộ trình: LearningSessionService.recalculateCourseProgress → syncLearningPathCompletion (khi khóa DONE → check mọi khóa trong path DONE → set path enrollment DONE + completed_at; ENROLLED→LEARNING nếu mới có tiến độ)
- [x] Backfill script cho dữ liệu cũ (.plans/.../backfill-path-completion.php — **user tự chạy qua tinker**, idempotent)
- [x] BE MyLearningService: dedup khóa con (enrolledPathSubjectIds) khỏi in_progress courses + completed; **path progress = TRUNG BÌNH % khóa con** (tiến độ thực, user đổi ý từ count-based) + nhãn "Khoá x/y" (coursesDone/courses); thêm children[] cho path; thêm lessonsDone cho course; thêm nhóm `completed` (done courses lẻ + done paths, cả khi không có chứng chỉ)
- [x] FE store myLearning: state.completed; overviewStats (learning = in_progress count, done = completed.length); monthPlanPercent gồm completed (=100%)
- [x] FE thẻ StudyCard: nhãn khóa lẻ `[Khoá học]` "Bài x/y" vs lộ trình `[Lộ trình]` (brand) "Khoá x/y"; path card nút "Xem N khoá con" (bung inline accordion + nút Học từng khóa) + Chi tiết + Tiếp tục. UX: user chốt "cả hai" (bung + chi tiết)
- [x] Verify: php -l (LearningSessionService + MyLearningService) sạch; FE lint (0 errors) + build PASS. **Chờ user chạy backfill + verify browser**

## Checkpoint
### Checkpoint — 2026-06-05
Vừa hoàn thành: Brainstorming + spec đầy đủ + plan chi tiết 16 task (docs/superpowers/plans/2026-06-05-goc-hoc-tap-ca-nhan.md).
Đang làm dở: —
Bước tiếp theo: User chọn cách thực thi (subagent-driven / inline) → bắt đầu Task 1 (cài apexcharts).
Blocked:

### Checkpoint — 2026-06-05 (CODE DONE)
Vừa hoàn thành: Implement xong 16/16 task qua subagent-driven (mỗi nhóm qua spec + quality review). Build PASS + Lint PASS (0 errors). Final review: READY TO HANDOFF.
- Phase 1: trang /goc-hoc-tap 4 tab (ApexCharts radialBar, 9 component my-learning + view + store mock + route + nút header).
- Phase 2: tìm kiếm global kiểu f8 (GlobalSearch popup + /tim-kiem + store search + 2 composable). Task 16 không cần sửa (useListPage tự seed keyword).
Đã cài: apexcharts ^5.13 + vue3-apexcharts ^1.11 (trong container Docker).
Đang làm dở: —
Bước tiếp theo: User verify trên browser (Docker, port 3001): vào /goc-hoc-tap (4 tab + chart + filter + drawer + nút điều hướng), gõ tìm kiếm ở header (popup gợi ý + Xem thêm + Xem tất cả → /tim-kiem + badge lọc).
Blocked:
Defer (sau, đúng thiết kế): store myLearning còn mock (TODO(BE) khi có endpoint list cá nhân); tìm kiếm gần đây (localStorage) chưa làm.

### Checkpoint — 2026-06-06
Vừa hoàn thành (tiếp nối Phase 1+2):
- **Phase 3 — Nối API thật cả 4 tab**: BE MyLearningController + MyLearningService + route GET /api/v1/elearning/my/learning-space (elearning.auth) trả required/in_progress/certificates (tái dùng enrollment + MandatoryChecker + certificate_enabled; cert tự sinh mã CERT-KH/LT-<id>; progress path = avg). FE store myLearning gọi API thật; vòng tiến độ = % avg ('Tiến độ tổng thể'); upcoming derive từ items. Verify tinker data thật (employee + learner) + lint + build PASS.
- **Fix banner**: bỏ defaultThumb hardcode; tạo base `CardThumb.vue` (nền gradient + icon theo loại) — đồng nhất 6 chỗ (LearnCard, PathCard, StudyCard, GlobalSearch, DetailHero).
- **Phase 4 — Hạn hoàn thành**: field chung mới `complete_within_days` (subjects + learning_paths), deadline = enrolled_at + N.
  - BE: migration 2026_06_06_100000 (CHƯA CHẠY) + validate/save (Subject+LP request/service/resource) + helper `DeadlineHelper` + compute trong MyLearningService + SubjectDetailController + LearningPathDetailController.
  - hrm-client: input "Hạn hoàn thành sau (ngày)" — Subject TabLearners (ngoài onboarding) + LP TabResult.
  - elearning FE: deadline hiện ở Tôi cần học (RequirementTable: date + useDeadline pill, 1 dòng), Tổng quan timeline, Tôi đang học (StudyCard pill), trang chi tiết khoá/lộ trình (DetailHero + DetailEnrollCard — nới điều kiện chỉ cần deadline + format dd/mm/yyyy via useDeadline.formatDmy). Bỏ dòng "Đúng tiến độ" thừa (màu pill đã đủ). Browse cards chủ ý bỏ qua.
  - Verify: php -l (toàn bộ file BE) + lint + build + tinker (DeadlineHelper) PASS. Graceful pre-migration (field null → deadline null, không crash).
Đang làm dở: —
Bước tiếp theo (việc của user để kích hoạt deadline):
  1. BE: `php artisan migrate` (thêm cột complete_within_days).
  2. hrm-client: chạy dev, vào form khoá/lộ trình nhập "Hạn hoàn thành sau (ngày)".
  3. Verify browser: học viên đã enroll nội dung có cấu hình → thấy hạn ở góc học tập + trang chi tiết.
Blocked:
Defer: store myLearning Phase 3 đã hết mock (dùng API thật); detail-page deadline ĐÃ nối.
- **Tìm kiếm gần đây (localStorage) — ĐÃ LÀM (2026-06-06)**: composable `useRecentSearches` (key elearning_recent_searches, max 6) + GlobalSearch hiện panel "Tìm kiếm gần đây" khi focus + ô trống (click chọn lại / xoá 1 / xoá tất cả); lưu khi click item / Xem thêm / Xem tất cả / Enter. Lint + build PASS.
- Browse cards deadline: tự quyết bỏ qua (cần join enrollment per-user vào SubjectBrowseResource/LearningPathBrowseResource). Chờ user xác nhận có làm không.

### Checkpoint — 2026-06-06 (fix nhỏ)
- **Tìm kiếm gần đây (localStorage)**: composable useRecentSearches + GlobalSearch panel "Tìm kiếm gần đây".
- **Fix bug điều hướng từ popup search → trang chi tiết**: ContentDetailView dùng chung cho route subject-detail + learning-path-detail; khi điều hướng giữa các trang chi tiết, Vue tái dùng component → entityType (set 1 lần) bị stale + chỉ refetch onMounted → URL đổi nhưng màn không load. Fix: thêm `:key="route.path"` cho `<router-view>` ở App.vue (remount khi đổi path; query không đổi key nên list/search giữ state). Lint + build PASS.

### Checkpoint — 2026-06-06 (Phase 5: hoàn thành lộ trình + đếm theo đơn vị gốc)
Vừa hoàn thành:
- **Auto-complete lộ trình (fix gốc)**: `LearningSessionService.syncLearningPathCompletion` — khi khóa đạt DONE, kiểm tra mọi khóa thuộc các lộ trình user đã enroll; đủ 100% → set LearningPathEnrollment = DONE + completed_at (ENROLLED→LEARNING nếu mới có tiến độ). Giải quyết "lộ trình 100% kẹt ở tab Đang học".
- **Backfill** dữ liệu cũ: `.plans/goc-hoc-tap-ca-nhan/backfill-path-completion.php` (idempotent, **user tự chạy qua tinker**).
- **Đếm theo đơn vị gốc**: BE MyLearningService loại khóa con (enrolledPathSubjectIds) khỏi danh sách khóa lẻ (in_progress + completed); thêm nhóm `completed` (done courses lẻ + done paths kể cả không có chứng chỉ); path progress = coursesDone/courses (Khoá x/y); course thêm lessonsDone (Bài x/y); path thêm children[].
- **FE**: store thêm state.completed; overviewStats (Đang học = in_progress count, Đã hoàn thành = completed.length); monthPlanPercent gồm completed=100%. StudyCard: nhãn `[Khoá học]` vs `[Lộ trình]` (brand), tiến độ Bài x/y vs Khoá x/y, nút "Xem N khoá con" bung inline (nút Học từng khóa → route subject-learn) + Chi tiết + Tiếp tục.
- Verify: php -l (2 file BE) sạch; FE lint 0 errors + build PASS.
Đang làm dở: —
Bước tiếp theo (việc của user):
  1. Chạy backfill 1 lần: `php artisan tinker` → `require '<path>/backfill-path-completion.php';` (cập nhật các lộ trình cũ đã đủ 100% sang DONE).
  2. Verify browser: lộ trình hoàn thành rời tab "Đang học" → vào "Chứng chỉ"/ô "Đã hoàn thành"; thẻ lộ trình bung khóa con; khóa con không hiện trùng ở danh sách khóa lẻ; ô Dashboard đếm đúng (path=1, khóa lẻ=1).
Blocked:
Defer: dedup khóa con cho tab "Tôi cần học" (hiện chỉ áp cho Đang học/Đã hoàn thành theo spec) — chờ user xác nhận nếu cần.

### Checkpoint — 2026-06-06 (Phase 5 hoàn tất + backfill đã chạy + đổi cách tính tiến độ)
Vừa hoàn thành:
- **Auto-complete lộ trình (fix gốc)**: LearningSessionService.syncLearningPathCompletion — khóa đạt DONE → kiểm tra mọi khóa thuộc lộ trình đã enroll → đủ → set LearningPathEnrollment=DONE+completed_at. php -l sạch.
- **Backfill ĐÃ CHẠY** (user cho phép): tinker require backfill-path-completion.php → "Đã kiểm tra: 4 enrollment lộ trình. Cập nhật DONE: 2." 2 lộ trình cũ đủ 100% đã chuyển DONE.
- **Đếm theo đơn vị gốc**: MyLearningService loại khóa con (enrolledPathSubjectIds) khỏi khóa lẻ (in_progress+completed); nhóm `completed` (done courses lẻ + done paths kể cả không cert); course có lessonsDone (Bài x/y); path có children[] + coursesDone/courses.
- **Tiến độ path = TRUNG BÌNH % khóa con** (user đổi ý từ count-based vì khóa đang học 88% không được tính): vd khóa 88%+100% → bar 94%, nhãn "Khoá 1/2". Logic hoàn thành vẫn theo status DONE (không đổi).
- **FE**: store completed + overviewStats (Đang học=in_progress count, Đã hoàn thành=completed.length) + monthPlanPercent gồm completed=100%. StudyCard: nhãn [Khoá học]/[Lộ trình] (brand), Bài x/y vs Khoá x/y, nút "Xem N khoá con" bung inline (nút Học/Xem lại từng khóa) + Chi tiết + Tiếp tục.
- Verify: php -l (LearningSessionService + MyLearningService) + FE lint 0 errors + build PASS.
Đang làm dở: —
Bước tiếp theo: user reload /goc-hoc-tap verify (path hoàn thành rời "Đang học", bung khóa con, bar tiến độ thực, Dashboard đếm đúng path=1/khóa lẻ=1).
Blocked:
Defer: dedup khóa con tab "Tôi cần học" (chờ xác nhận); Phase 4 deadline vẫn cần user nhập cấu hình "Hạn hoàn thành sau (ngày)" ở form admin để có dữ liệu.
