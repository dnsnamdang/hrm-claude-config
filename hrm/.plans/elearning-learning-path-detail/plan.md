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
