# Elearning — Learning Path Detail

> Owner: @junfoke
> Plan chi tiết: `docs/superpowers/plans/2026-05-19-elearning-learning-path-detail.md`
> Spec: `docs/superpowers/specs/2026-05-19-elearning-learning-path-detail-design.md`

---

## Phase 1: Backend — Learner Endpoints

- [x] Task 1: Routes + Controller methods (3 routes: builder/public/enroll)
- [x] Task 2: LearningPathLearnerResource (có progress + enrollment)
- [x] Task 3: LearningPathPublicResource (không progress)
- [x] Task 4: Enroll service method (enrollPath)

## Phase 2: Frontend — Constants + Store

- [x] Task 5: Constants file (`learningPathDetail.js`)
- [x] Task 6: Pinia store (`learningPathDetail.js`)

## Phase 3: Frontend — Components

- [x] Task 7: PathHero.vue
- [x] Task 8: PathEnrollCard.vue
- [x] Task 9: PathOverview.vue
- [x] Task 10: PathRequirements.vue
- [x] Task 11: PathOutline.vue
- [x] Task 12: PathDiscussion.vue

## Phase 4: Frontend — View + Route

- [x] Task 13: LearningPathDetailView.vue + Route `/lo-trinh/:slug`

## Phase 5: Mở rộng Discussion composable

- [x] Task 14: useDiscussion hỗ trợ entityType (`learning_path`)

## Phase 6: Kiểm tra & hoàn thiện

- [x] Task 15: Vite build verify — pass, 0 errors

## Phase 7: Bảng enrollment riêng cho LP

- [x] Task 16: Migration `learning_path_enrollments`
- [x] Task 17: Model `LearningPathEnrollment`
- [x] Task 18: Cập nhật `enrollPath()` dùng bảng mới
- [x] Task 19: Cập nhật `LearningPathLearnerResource` query enrollment
- [x] Task 20: Thêm relationship `enrollments()` vào LearningPath model

## Phase 8: Slug URL cho Learning Path

- [x] Task 21: Migration `add_slug_to_learning_paths_table` — thêm cột `slug`, backfill LP cũ bằng `Str::slug(name)`
- [x] Task 22: Model `LearningPath` — thêm `boot()` auto sinh slug khi save, `generateUniqueSlug()`
- [x] Task 23: Controller `showBuilder`, `showPublic`, `enroll` — đổi từ implicit binding sang manual find bằng slug
- [x] Task 24: Thêm endpoint `resolveSlug($id)` — nhận id, trả slug (cả auth + public route)
- [x] Task 25: Resource `LearnerResource` + `PublicResource` — thêm trường `slug` trong response
- [x] Task 26: Route BE — `{slug}/builder`, `{slug}/enroll`, `public/{slug}`, `resolve-slug/{id}`
- [x] Task 27: FE Router — đổi `/lo-trinh/:id` → `/lo-trinh/:slug`
- [x] Task 28: FE Store — `fetchPath(slug)`, `enrollPath()` dùng `path.slug`
- [x] Task 29: FE `LearningPathDetailView` — watch route.params.slug, auto redirect nếu param là số (gọi resolve-slug)
- [x] Task 30: FE `LearningPathRedirectView` — route `/learning-path/:id` redirect sang `/lo-trinh/:slug`

## Phase 9: Discussion, Banner, Overview, UI polish

- [x] Task 31: BE `LearningPathCommentController` — 6 method (index/store/update/destroy/like/report), `commentable_type = LearningPath::class`, tìm LP bằng slug
- [x] Task 32: BE routes comments — 6 route `/{slug}/comments` trong group `/learning-paths`
- [x] Task 33: FE `PathDiscussion` — sửa prop `:comment` → `:node`, wrap event handler `@reply`/`@report`
- [x] Task 34: FE `PathOverview` — đổi `{{ }}` sang `v-html` cho 3 block overview (fix HTML entities), thêm scoped style cho list/paragraph
- [x] Task 35: FE Store `mapPath` — map `thumbnail` từ `data.banner_url` (fix banner không hiển thị)
- [x] Task 36: BE `LearningPathCommentController@index` — thêm phân trang (`paginate($perPage)`), trả `total/page/last_page`; thêm `->when($request->rate, ...)` filter theo sao
- [x] Task 37: FE Composable `useDiscussion` — thêm `loadMore()`, `hasMore`, `remainingCount`, `loadingMore` cho paginated mode (learning_path only, subject giữ nguyên)
- [x] Task 38: FE `LearningPathDiscussionView` — trang thảo luận riêng `/lo-trinh/:slug/thao-luan`, load 5 + nút xem thêm + form bình luận
- [x] Task 39: FE `PathDiscussion` — hiện 5 comment preview + form bình luận + nút "Xem thêm X bình luận" redirect sang trang thảo luận; sau khi post cắt danh sách còn 5
- [x] Task 40: FE Router — thêm route `learning-path-discussion`
- [x] Task 41: Thu gọn chiều cao AppHeader (giảm padding, logo, button, nav)
- [x] Task 42: Tăng font nav header lên 14px (text-sm) để phân cấp với nội dung 13px
- [x] Task 43: Thêm context banner vào trang thảo luận (thumbnail + tên lộ trình + thông tin phụ + nút quay lại)
- [x] Task 44: Thêm rating summary (điểm TB + bar chart phân bố sao) vào trang thảo luận
- [x] Task 45: Thêm filter pills lọc bình luận theo số sao
- [x] Task 46: Composable `useDiscussion` — thêm `loadRatingSummary()`, `setFilterStar()`, `ratingSummary` ref
- [x] Task 47: Refactor `views/` — nhóm theo folder chức năng (`home/`, `learning-path/`, `subject/`), cập nhật router imports

### Checkpoint — 2026-05-20 (4)
Vừa hoàn thành: Phase 9 — Discussion BE+FE (comment CRUD + phân trang + trang riêng), banner fix, overview v-html fix, header compact, rating summary/filter, views folder restructure
Đang làm dở: không
Bước tiếp theo: Test rating summary + filter theo sao trên browser, kiểm tra trang chi tiết LP vẫn hoạt động bình thường
Blocked: không

## Phase 10: Fix bug trạng thái & vào học (2026-06-03)

- [x] Task 48: BE `LearningPathLearnerResource::mapSubjectWithProgress` — bỏ hardcode `learn_status='todo'`/`locked=false`, load `EnrollmentLessonProgress` theo subject enrollment → map trạng thái thật từng bài (todo/learning/done). Reorder: query enrollment trước khi map lesson.
- [x] Task 49: BE `LearningPathLearnerResource::checkPathDone` — sửa MIN_PERCENT đếm `learn_status='done'` (trước dùng 'pass' không bao giờ khớp).
- [x] Task 50: FE `PathOutline.vue` — badge trạng thái khoá: đổi `c.status === 'pass'` → `'done'` (khoá đã xong hiện đúng "Đạt", trước hiện nhầm "Chưa học").
- [x] Task 51: FE `learningPathDetail.js` — đổi label `EVAL_MODE_BADGE` thành "ĐG: Hoàn thành"/"ĐG: Thi"/"ĐG: Khác" để phân biệt badge chế độ đánh giá với trạng thái học.
- [x] Task 52: FE `ContentDetailView.handleOpenLesson` (nhánh path) — bấm "Vào học" 1 bài → vào thẳng màn học `subject-learn` (slug khoá + lessonId), guard locked/đăng nhập/chưa tham gia lộ trình (trước chỉ toast hoặc đẩy sang subject-detail).
- [x] Task 53: FE `useContentDetail.handleStartLearn` — FIX 404: nút "Tiếp tục học" lộ trình trước đẩy `route.params.slug` (slug LỘ TRÌNH) vào route `/khoa-hoc/:slug/hoc` → "Không tìm thấy khoá học". Nay nhánh path chọn khoá đầu tiên chưa `done` (hoặc khoá đầu) rồi push subject-learn với slug khoá đó.
- [x] Task 54: BE `LearningPathLearnerResource` — đổi % tiến độ lộ trình từ `số khoá done / tổng khoá` sang TRUNG BÌNH % từng khoá (`$mappedSubjects->avg('progress')`). Học dở 1 khoá vẫn được tính (vd xong khoá 1 + nửa khoá 2 = (100+50)/2 = 75%).

### Checkpoint — 2026-06-03 (5)
Vừa hoàn thành: Phase 10 — fix trạng thái từng bài (BE), trạng thái khoá pass→done (FE), label badge đánh giá, nút "Vào học" vào thẳng màn học.
Đang làm dở: không
Bước tiếp theo: User verify browser — (1) bấm "Vào học" 1 bài trong LP → vào màn học + tracking, (2) khoá đã xong hiện "Đạt", (3) bài đã học hiện đúng "Đã xong"/"Đang học".
Blocked: không

## Phase 11: Hiển thị Chương + Quy đổi giờ-phút + Badge + Fix trạng thái môn (2026-06-03)

**Quy đổi giờ-phút (helper chung)**
- [x] Task 55: Helper `formatMinutes()` trong `elearning/src/utils/lessonMappers.js` (vd 67 → "1 giờ 7 phút", <60 giữ "X phút"). Áp vào: `PathOutline`, `PathRequirements`, `ContentDetailView` (tổng + badge), `DetailHero`, `SubjectOutline`, `SubjectRequirements`, `SubjectDiscussionView`, `base/LearnCard` (bỏ in thô `{{ x }} phút`).

**Hiển thị cấp Chương — Trang học viên (elearning)**
- [x] Task 56: BE `LearningPathLearnerResource::mapSubjectWithProgress` — tách closure `$mapLesson` (thêm `chapter_id`), build `chapters[]` (group theo `subject_chapters`, mỗi chương có total_lessons/total_minutes/lessons) + `loose_lessons` (bài null-chapter); giữ `lessons` phẳng.
- [x] Task 57: BE `Elearning/LearningPathDetailController` — eager-load thêm `learningPathSubjects.subject.chapters`.
- [x] Task 58: FE store `learningPathDetail.js` — tách `mapLesson`, map `chapters` + `looseLessons`, thêm action `toggleChapter(ci, chi)`.
- [x] Task 59: FE `PathOutline.vue` — render Khoá → Chương (collapse riêng) → Bài; bài null-chapter hiện thẳng dưới khoá; fallback khoá chưa cấu hình chương dùng lessons phẳng. Tách component `PathLessonRow.vue` dùng lại.
- [x] Task 60: FE `ContentDetailView` — truyền `@toggle-chapter` cho PathOutline.

**Hiển thị cấp Chương — Builder lộ trình (hrm-client)**
- [x] Task 61: BE `LearningPathController::show` + `showBuilder` — eager-load thêm `learningPathSubjects.subject.chapters`.
- [x] Task 62: BE `LearningPathDetailResource` — thêm `chapter_id` cho mỗi lesson + `chapters[]` cho subject.
- [x] Task 63: BE `SubjectController::getAll` — load thêm `chapters` (flow thêm khoá từ ngân hàng).
- [x] Task 64: FE `learning-path/components/TabInfo.vue` — giữ `chapter_id` khi map lesson (getSubjectLessons/addSubject), helper `getSubjectChapters`/`getLooseLessons`/`getSubjectRows`, render header Chương (collapse, mặc định mở) + bài thụt lề; CSS `.chapter-head`/`.lesson-row--nested`.

**Badge tổng + gộp nút**
- [x] Task 65: FE `PathOutline.vue` — badge "X khoá • Y bài • giờ-phút" (computed `totalMinutes`/`totalLessons`) cạnh nút "Mở tất cả khoá".
- [x] Task 66: FE `ContentDetailView` (subject) — gộp badge "X chương • giờ-phút" + nút "Mở tất cả chương" cùng 1 dòng header; bỏ nút toggle khỏi `SubjectOutline` (dọn `allOpen`/emit thừa).

**Fix trạng thái bài/chương — Chi tiết môn học**
- [x] Task 67: BE `Elearning/SubjectDetailController` — thêm `attachLessonLearnStatus()`: load `EnrollmentLessonProgress` theo enrollment → đính `learn_status` (todo/learning/done) cho từng SubjectLesson (cả nhánh chương & flat).
- [x] Task 68: BE `SubjectDetailResource::mapSubjectLessons` — emit thêm `learn_status`.
- [x] Task 69: FE `subjectDetail.js` — `mapLesson` đọc `sl.learn_status` thật; thêm `deriveChapterStatus()` (pass = mọi bài bắt buộc done; learning = có bài done/đang học; còn lại todo). Fix bug "đã xong vẫn hiện Chưa học".

**Overview placeholder**
- [x] Task 70: FE `DetailOverview.vue` — 3 thẻ overview hiện "Chưa có thông tin." khi `what_includes/for_who/will_learn` rỗng (trước để trống trông như lỗi).

### Checkpoint — 2026-06-03 (6)
Vừa hoàn thành: Phase 11 — hiển thị cấp Chương (learner + builder), quy đổi giờ-phút toàn bộ, badge tổng + gộp nút, fix trạng thái bài/chương màn chi tiết môn, placeholder overview.
Đang làm dở: không
Bước tiếp theo: User verify browser (Docker, Node ≥18) — (1) lộ trình & môn hiện đúng Chương → Bài + thời lượng giờ-phút, (2) builder lộ trình hiện Chương, (3) bài đã học xong hiện "Đã xong" + chương hiện "Đạt", (4) overview rỗng hiện placeholder.
Lưu ý/Defer: status chương kiểu thi (exam) mới derive theo tiến độ bài, chưa tính kết quả bài thi; PathOutline (learner) lesson learn_status đã fix ở Phase 10 nhưng vẫn theo từng subject enrollment.
Blocked: không
