# Plan — Section "Bạn cần học" (trang chủ elearning) lấy data thật

> Phụ trách: @khoipv · Spec: .plans/elearning-home-need-to-learn/design.md

**Goal:** Section "Bạn cần học" ở trang chủ elearning (3001) hiển thị khóa học + lộ trình thật từ BE (trộn, tối đa 4, mới nhất trước), theo quy tắc khách=public / nhân viên HRM=đang dùng.

**Kiến trúc:** Thêm 1 endpoint BE `public/home-content` (optional auth) tái dùng 2 resource có sẵn (`SubjectBrowseResource`, `LearningPathBrowseResource`), chuẩn hóa learn-item, trộn + sort + cắt 4. FE: store gọi endpoint, HomeView render LearnCard (mở rộng type='path'), điều hướng theo type.

**Tech:** Laravel 8 (Module Elearning) · Vue 3 + Pinia (TPE-Elearing)

---

## Phase 1 — Backend

- [x] **Task 1.1** Thêm route `public/home-content` + optional auth
  File: `hrm-api/Modules/Elearning/Routes/api.php` (sau dòng `public/learning-paths`)
  ```php
  Route::get('public/home-content', [PublicBrowseController::class, 'homeContent'])->middleware('elearning.auth.optional');
  ```

- [x] **Task 1.2** Thêm method `homeContent()` vào `PublicBrowseController`
  File: `hrm-api/Modules/Elearning/Http/Controllers/Api/V1/PublicBrowseController.php` (thêm method mới, cuối class)
  ```php
  public function homeContent(Request $request)
  {
      try {
          $isHrmEmployee = $request->attributes->get('user_type') === 'employee';
          $limit = 4;

          // ─── Khóa học (Subject) ───
          $subjects = Subject::where('status', Subject::HOAT_DONG)
              ->when(!$isHrmEmployee, function ($q) {
                  $q->where('is_public', 1);
              })
              ->with([
                  'trainingType:id,name',
                  'subjectLessons.lesson:id,duration',
              ])
              ->withCount(['subjectLessons'])
              ->addSelect([
                  'subjects.*',
                  DB::raw('(SELECT COUNT(*) FROM subject_enrollments WHERE subject_enrollments.subject_id = subjects.id) as subject_enrollments_count'),
              ])
              ->orderByDesc('updated_at')
              ->limit($limit)
              ->get();

          // ─── Lộ trình (LearningPath) ───
          $paths = LearningPath::where('status', LearningPath::STATUS_ACTIVE)
              ->when(!$isHrmEmployee, function ($q) {
                  $q->where('is_public', 1);
              })
              ->with([
                  'trainingType:id,name',
                  'learningPathSubjects.subject.subjectLessons.lesson:id,duration',
              ])
              ->withCount(['learningPathSubjects'])
              ->addSelect([
                  'learning_paths.*',
                  DB::raw('(SELECT COUNT(*) FROM learning_path_enrollments WHERE learning_path_enrollments.learning_path_id = learning_paths.id) as learning_path_enrollments_count'),
              ])
              ->orderByDesc('updated_at')
              ->limit($limit)
              ->get();

          // is_mandatory không dùng ở section này → _user_profile null
          $request->merge(['_user_profile' => null]);

          $subjectItems = SubjectBrowseResource::collection($subjects)->toArray($request);

          // Lộ trình: bổ sung type='path' + minutes (từ total_duration)
          $pathItems = array_map(function ($it) {
              $it['type'] = 'path';
              $it['minutes'] = $it['total_duration'] ?? 0;
              return $it;
          }, LearningPathBrowseResource::collection($paths)->toArray($request));

          // Trộn + sort mới nhất trước (updated_at dạng Y-m-d) + cắt 4
          $items = array_merge($subjectItems, $pathItems);
          usort($items, function ($a, $b) {
              return strcmp($b['updated_at'] ?? '', $a['updated_at'] ?? '');
          });
          $items = array_slice($items, 0, $limit);

          return $this->responseJson('Thành công', 200, [
              'items' => $items,
          ]);
      } catch (\Exception $e) {
          Log::error('Elearning PublicBrowse homeContent error: ' . $e->getMessage(), [
              'trace' => $e->getTraceAsString(),
          ]);
          return $this->responseJson('Đã có lỗi xảy ra', 500);
      }
  }
  ```

- [x] **Task 1.3** Lint BE
  Run: `php -l` cho 2 file trên — Expected: "No syntax errors detected".

- [x] **Task 1.4** Verify nhanh data bằng tinker (giả lập guest = bắt is_public)
  Run kiểm tra: Subject HOAT_DONG+public count, LearningPath ACTIVE+public count > 0 (đảm bảo có data để hiện).

## Phase 2 — Frontend

- [x] **Task 2.1** Store: gọi endpoint thật cho `needToLearn`
  File: `TPE-Elearing/src/stores/elearning.js`
  - Thêm import: `import { api } from '@/services/api'`
  - Thêm `needToLearn: []` vào `state`.
  - XÓA getter `needToLearn` (lọc mock theo isMandatory) — chuyển thành state.
  - Sửa `fetchHomeData()`:
  ```js
  async fetchHomeData() {
    this.courses = COURSES
    this.subjects = SUBJECTS
    this.categories = CATEGORIES
    this.hallOfFame = HALL_OF_FAME
    this.recentActivities = RECENT_ACTIVITIES
    try {
      const res = await api.get('/api/v1/elearning/public/home-content')
      this.needToLearn = res.data?.items || res.items || []
    } catch (e) {
      console.error('fetchHomeData home-content error:', e)
      this.needToLearn = []
    }
  },
  ```

- [x] **Task 2.2** HomeView: điều hướng theo type + ẩn section khi rỗng + sửa subtitle
  File: `TPE-Elearing/src/views/home/HomeView.vue`
  - SectionBlock "Bạn cần học": thêm `v-if="store.needToLearn.length"`, đổi subtitle:
    `subtitle="Khoá học và lộ trình học dành cho bạn."`, bỏ `:show-deadline="true"`.
  - Sửa `openLearn`:
  ```js
  function openLearn(item) {
    if (item.type === 'path') {
      router.push({ name: 'learning-path-detail', params: { slug: item.slug } })
    } else if (item.slug) {
      router.push({ name: 'subject-detail', params: { slug: item.slug } })
    } else {
      toast.show('Mở chi tiết: ' + (item.title || ''))
    }
  }
  ```

- [x] **Task 2.3** LearnCard: hỗ trợ type='path'
  File: `TPE-Elearing/src/components/base/LearnCard.vue`
  ```js
  const kindLabel = computed(() => {
    if (props.item.type === 'path') return 'Lộ trình'
    if (props.item.type === 'subject') return 'Môn học'
    return 'Khoá học'
  })
  const kindIcon = computed(() => {
    if (props.item.type === 'path') return 'ri-road-map-line'
    if (props.item.type === 'subject') return 'ri-book-2-line'
    return 'ri-stack-line'
  })
  const kindPillClass = computed(() => {
    if (props.item.type === 'path') return 'bg-blue-500/25 border-blue-500/20'
    if (props.item.type === 'subject') return 'bg-green-500/25 border-green-500/20'
    return 'bg-violet-500/25 border-violet-500/20'
  })
  ```

## Phase 3 — Verify

- [ ] **Task 3.1** Chạy elearning + mở `/` ở chế độ khách (không token) → section "Bạn cần học" chỉ hiện khóa/lộ trình public, tối đa 4, mới nhất trước.
- [ ] **Task 3.2** Đăng nhập SSO từ HRM → section hiện thêm khóa/lộ trình "đang dùng" chưa public.
- [ ] **Task 3.3** Click card khóa học → vào subject-detail; click card lộ trình → vào learning-path-detail.
- [ ] **Task 3.4** Check `laravel-2026-06-04.log` không có lỗi homeContent.

## Phase 4 — Fix bug thời lượng card (phát hiện khi verify)

Triệu chứng: lộ trình NPK chi tiết ghi 30s nhưng card ngoài hiện 3 phút.
Nguyên nhân: 2 resource dùng chung cộng `ceil(duration/60)` cho TỪNG bài rồi mới cộng → phồng số (3 bài 10s → 3 phút).
Quyết định (user duyệt): sửa resource dùng chung + card hiển thị mm:ss khớp trang chi tiết.

- [x] **Task 4.1** `SubjectBrowseResource`: cộng tổng giây (`$totalSeconds`) rồi `ceil/60`; thêm field `duration_seconds`.
- [x] **Task 4.2** `LearningPathBrowseResource`: tương tự — `$totalSeconds` + `total_duration` tính lại + field `duration_seconds`.
- [x] **Task 4.3** `LearnCard.vue`: thêm computed `durationText` — có `duration_seconds>0` → `formatLearnDuration` (<1 phút "30s", còn lại "3 phút"/"1 giờ 7 phút"), else fallback `formatMinutes` (giữ nguyên section mock). Thêm helper `formatLearnDuration` vào `utils/lessonMappers.js`.
- [x] **Task 4.4** Lint BE + verify endpoint: "Lộ trình 36669" 20s → minutes=1/duration_seconds=20 (trước phồng thành 2 phút). NPK 30s → "0:30".

### Checkpoint — 2026-06-04
Vừa hoàn thành: Phase 1+2 (endpoint + FE) + Phase 4 (fix bug làm tròn thời lượng ở 2 resource dùng chung + card hiển thị mm:ss). Lint + verify tinker PASS.
Đang làm dở: không
Bước tiếp theo: Phase 3 — user chạy elearning trên browser verify (khách vs SSO HRM, thời lượng card khớp chi tiết) + click card điều hướng.
Blocked:

## Phase 5 — 3 section còn lại lấy data thật (Khuyến nghị / Phổ biến / Mới)

> Phụ trách: @junfoke · Ngày: 2026-06-08
> Mở rộng endpoint `home-content` → trả nhiều section trong 1 call. Bỏ mock cho 3 section:
> "Khuyến nghị cho bạn", "Nội dung nhiều người học", "Nội dung mới".

**Quyết định nghiệp vụ (user chốt):**
- Gộp vào 1 endpoint `home-content`, response đổi từ `{items}` → `{need_to_learn, recommend, popular, newest}`.
- **Khuyến nghị**: lọc theo đối tượng khuyến nghị khớp profile user — subject `subject_assignees.is_mandatory=0`, path `learning_path_assignees.assignment_mode='recommended'`. Sắp theo đánh giá cao.
  - Fallback (guest/learner/nhân viên không có dept-position-capability, hoặc match rỗng): nội dung public đánh giá cao nhất (trộn khóa+lộ trình).
- **Phổ biến**: order theo lượt ghi danh (enrolled_count) desc.
- **Mới**: order theo `updated_at` desc (giống need_to_learn hiện tại).

### Backend
- [x] **Task 5.1** Refactor `PublicBrowseController@homeContent` trả 4 section + thêm helper `buildHomeSection()`, `applyAssigneeProfileFilter()`, `homeSectionComparator()`.
  File: `hrm-api/Modules/Elearning/Http/Controllers/Api/V1/PublicBrowseController.php`
- [x] **Task 5.2** Lint BE (`php -l`) → "No syntax errors detected".

### Frontend
- [x] **Task 5.3** Store: chuyển 3 getter `recommendToLearn`/`popularMix`/`newestMix` (mock từ `mixAll`) → state array, fill từ response mới. Giữ `mixAll`+`categoryCount` cho section Danh mục (vẫn mock).
  File: `elearning/src/stores/elearning.js`
- [x] **Task 5.4** HomeView: thêm `v-if="store.xxx.length"` ẩn 3 section khi rỗng. Binding `openLearn` giữ nguyên (điều hướng theo `type`).
  File: `elearning/src/views/home/HomeView.vue`

### Verify
- [ ] **Task 5.5** User chạy browser: guest thấy khuyến nghị = đánh giá cao; SSO HRM có dept/position thấy khuyến nghị khớp đối tượng; Phổ biến sắp theo lượt ghi danh; Mới theo updated_at.

### Checkpoint — 2026-06-08
Vừa hoàn thành: Phase 5 — `home-content` đổi response thành 4 section (`need_to_learn`/`recommend`/`popular`/`newest`). BE thêm helper `buildHomeSection` + lọc khuyến nghị theo assignee (subject `is_mandatory=0`, path `assignment_mode='recommended'`) + fallback đánh giá cao. FE store fill 4 mảng từ 1 call, HomeView thêm `v-if` ẩn section rỗng. Lint BE PASS.
Đang làm dở: không
Bước tiếp theo: Task 5.5 — user verify trên browser (guest vs SSO HRM).
Blocked:

## Phase 6 — "Bạn cần học" = nội dung BẮT BUỘC của user

> @junfoke · 2026-06-08. User chốt: "Bạn cần học" hiện nội dung **bắt buộc** khớp profile;
> user ngoài/guest (không profile) → ẩn section.

- [x] **Task 6.1** Thêm mode `mandatory` vào `buildHomeSection`: lọc `subject_assignees.is_mandatory=1` / `learning_path_assignees.assignment_mode='mandatory'` khớp profile (`applyAssigneeProfileFilter`). Không có profile → trả `[]` (KHÔNG fallback). Order `updated_at` desc. Eager-load assignee bắt buộc cho cả base query → badge "Bắt buộc" hiển thị đúng. Đổi `need_to_learn` trong `homeContent` sang mode `mandatory`.
  File: `hrm-api/.../PublicBrowseController.php` — Lint PASS.
- [x] **Task 6.2** FE: HomeView đổi subtitle "Bạn cần học" → "Khoá học và lộ trình bắt buộc dành cho bạn." (`v-if="store.needToLearn.length"` đã có → tự ẩn khi rỗng). Store không đổi.
  File: `elearning/src/views/home/HomeView.vue`
- [ ] **Task 6.3** User verify: nhân viên SSO có nội dung bắt buộc → section hiện; user ngoài/guest → section ẩn hẳn.
- [x] **Task 6.4** Fix banner giả: bỏ fallback `pickThumb` (ảnh mock ngẫu nhiên) cho 4 section data thật trong `fetchHomeData` — giữ nguyên `thumb`(banner_url) từ BE, rỗng → `CardThumb` hiện placeholder trung tính. `pickThumb` giữ lại cho section Danh mục (mock).
  File: `elearning/src/stores/elearning.js`

### Checkpoint — 2026-06-08 (P6)
Vừa hoàn thành: "Bạn cần học" chuyển từ "mới nhất" → nội dung BẮT BUỘC khớp profile user (mode `mandatory`). User ngoài/guest không profile → section ẩn. Eager-load assignee để badge "Bắt buộc" đúng. Lint BE PASS.
Đang làm dở: không
Bước tiếp theo: user verify browser (SSO HRM thấy bắt buộc / guest ẩn section).
Blocked:

## Phase 7 — Card hiển thị trạng thái học (Học tiếp / Xem lại)

> @junfoke · 2026-06-08. Card trang chủ luôn hiện "Chi tiết" dù user đã hoàn thành / đang học.
> Nguyên nhân: (1) `home-content` chưa trả trạng thái học từng item, (2) LearnCard đọc `learnStatus`(camel) nhưng BE trả `learn_status`(snake).

- [x] **Task 7.1** `SubjectBrowseResource`: thêm `progress`/`learn_status`/`is_enrolled` (đọc `_subject_progress_map`, mặc định not_enrolled — an toàn cho endpoint `subjects()` không set map).
- [x] **Task 7.2** `PublicBrowseController`: thêm `buildSubjectProgressMap` (status enrollment 1/2/3 + progress → enrolled/learning/done) + merge `_subject_progress_map` & `_progress_map` (path tái dùng `buildUserProgressMap`) trong `buildHomeSection` trước transform. Lint PASS.
- [x] **Task 7.3** `LearnCard.vue`: đọc `learn_status` (cả camel mock cũ); nút theo trạng thái (learning→"Học tiếp" ri-play-circle-line, done→"Xem lại" ri-restart-line, else→"Chi tiết"); thêm badge trạng thái góc phải thumbnail (Đã hoàn thành / Đang học X%).
  File: `elearning/src/components/base/LearnCard.vue`
- [ ] **Task 7.4** User verify: khoá đang học → "Học tiếp" + badge "Đang học X%"; khoá đã xong → "Xem lại" + badge "Đã hoàn thành"; chưa ghi danh → "Chi tiết".

### Checkpoint — 2026-06-08 (P7)
Vừa hoàn thành: card phản ánh đúng trạng thái học. BE dựng map progress/learn_status cho cả subject + path trong home-content; SubjectBrowseResource thêm 3 field. FE LearnCard đổi nút động + badge trạng thái. Lint BE PASS.
Đang làm dở: không
Bước tiếp theo: user verify browser 3 trạng thái card.
Blocked:

## Phase 8 — Khuyến nghị loại nội dung đã hoàn thành + sửa text subtitle

> @junfoke · 2026-06-08. (1) Học xong rồi không khuyến nghị nữa. (2) Subtitle sai "gồm cả khoá và khoá".

- [x] **Task 8.1** BE: thêm helper `resolveOwner()` (dùng lại cho buildSubjectProgressMap). Mode recommend loại item đã hoàn thành: subject (`status=DONE` hoặc `progress>=100`) + path (`status=DONE`) → `whereNotIn` (áp cả nhánh lọc đối tượng lẫn fallback đánh giá cao). Lint PASS.
  File: `hrm-api/.../PublicBrowseController.php`
- [x] **Task 8.2** FE: sửa subtitle 3 section "gồm cả khoá và khoá" → "gồm cả khoá học và lộ trình".
  File: `elearning/src/views/home/HomeView.vue`
- [ ] **Task 8.3** User verify: section Khuyến nghị không còn card "Đã hoàn thành"; subtitle hiển thị đúng.

### Checkpoint — 2026-06-08 (P8)
Vừa hoàn thành: Khuyến nghị loại nội dung user đã hoàn thành (subject DONE/100%, path DONE); sửa text subtitle 3 section. Lint BE PASS.
Đang làm dở: không
Bước tiếp theo: user verify browser.
Blocked:

## Phase 9 — Màn "Xem tất cả" (cả khóa + lộ trình, có phân trang)

> @junfoke · 2026-06-08. User chốt: tạo màn mới hiển thị đầy đủ cả khóa + lộ trình theo từng section.

### Backend
- [x] **Task 9.1** Refactor `PublicBrowseController`: tách helper dùng chung `sectionBaseQueries` / `applySectionConstraints` / `transformSectionItems` / `recommendExcludeIds` / `profileHasScope` / `emptyPage`. `buildHomeSection` (trang chủ) dùng lại các helper này.
- [x] **Task 9.2** Thêm endpoint `homeSection` (phân trang trộn 2 bảng: fetch top page*per_page mỗi bên đã sort → trộn → cắt trang; total = đếm 2 bảng). Validate `type` ∈ mandatory/recommend/popular/newest. Mandatory không profile → trang rỗng. Recommend fallback đánh giá cao khi không match.
  File: `hrm-api/.../PublicBrowseController.php` — Lint PASS.
- [x] **Task 9.3** Route `GET public/home-section` (elearning.auth.optional).
  File: `hrm-api/Modules/Elearning/Routes/api.php`

### Frontend
- [x] **Task 9.4** Màn mới `HomeSectionView.vue` (route `/noi-dung/:type`, name `home-section`, public): header theo type, grid LearnCard (cả course+path), phân trang (per_page=12), loading skeleton + empty state, openLearn điều hướng theo type.
  File: `elearning/src/views/browse/HomeSectionView.vue` + `router/index.js`
- [x] **Task 9.5** HomeView: 4 nút "Xem tất cả" → `router.push({name:'home-section', params:{type}})` (mandatory/recommend/popular/newest) thay toast demo.
  File: `elearning/src/views/home/HomeView.vue`
- [x] **Task 9.7** URL tiếng Việt: slug `bat-buoc`/`khuyen-nghi`/`pho-bien`/`moi` ↔ apiType mandatory/recommend/popular/newest. Tách `constants/homeSections.js` (HOME_SECTIONS keyed slug + SECTION_SLUG map). HomeSectionView đọc slug→apiType; HomeView push slug.
  File: `elearning/src/constants/homeSections.js` + `HomeSectionView.vue` + `HomeView.vue`
- [x] **Task 9.8** Đổi UX từ phân trang số trang → "Xem thêm" (load more): vào hiện 12, nút "Xem thêm" tải tiếp 12 nối vào (page tăng dần), ẩn nút khi `items.length >= total`, hiện "Đã hiển thị X/Y", spinner khi đang tải thêm. Bỏ component Pagination khỏi màn này.
  File: `elearning/src/views/browse/HomeSectionView.vue`
- [ ] **Task 9.6** User verify: nhấn "Xem tất cả" mỗi section → URL tiếng Việt (vd /noi-dung/pho-bien), hiện 12 + nút "Xem thêm" tải tiếp; card course/path mở đúng chi tiết.

### Checkpoint — 2026-06-08 (P9)
Vừa hoàn thành: màn "Xem tất cả" cho 4 section (cả khóa + lộ trình, phân trang). BE refactor helper dùng chung + endpoint `home-section` phân trang trộn 2 bảng. FE màn `HomeSectionView` + route + wire 4 nút. Lint BE PASS.
Đang làm dở: không
Bước tiếp theo: user verify browser.
Blocked:
