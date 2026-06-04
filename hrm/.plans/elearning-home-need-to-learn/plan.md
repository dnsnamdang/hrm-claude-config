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
