# Plan — Elearning Học theo danh mục (trộn)

**Owner:** @junfoke
**Plan chi tiết:** [docs/superpowers/plans/2026-07-27-elearning-category-contents.md](../../docs/superpowers/plans/2026-07-27-elearning-category-contents.md)

## Task 1 — BE endpoint gộp (branch tpe-develop-elearning) — ✅ DONE (review clean)
- [x] Thêm route `public/contents` (Routes/api.php)
- [x] Thêm helper `applyContentFilters()` + `contentOrder()` vào PublicBrowseController
- [x] Thêm public method `contents()` (tái dùng sectionBaseQueries/transformSectionItems/buildDeadlineMap)
- [x] php -l sạch (chưa test curl live — chờ user verify browser)

## Task 2 — FE view + route — ✅ DONE (review clean)
- [x] Thêm route `learning-contents` (/hoc-theo-danh-muc) vào router
- [x] Tạo `CategoryContentsView.vue` (clone LearningByCategoryView, grid LearnCard, filter loại đào tạo/tên/trạng thái)
- [ ] Verify browser (user)

## Task 3 — Nối HomeView — ✅ DONE (verified)
- [x] `openCategory` + "Xem tất cả" trỏ sang `learning-contents`
- [ ] Verify luồng đầy đủ browser (user)

## Minor deferred (backlog, không chặn merge)
- buildDeadlineMap tính trên tập fetch rộng (page*per_page) thay vì sau array_slice — tối ưu.
- training_type_id='0' edge case kế thừa từ subjects()/learningPaths() — không phải regression.
- CategoryContentsView.openItem nhánh path push không guard item.slug (nhánh course có guard).

## Task 4 — Ẩn badge loại ở màn đơn-loại — ✅ DONE
- [x] LearnCard: thêm prop `show-kind` (default true), badge kind `v-if="showKind"`
- [x] PathCard: thêm prop `show-kind` (default true), badge "Lộ trình học" `v-if`, "Bắt buộc" thêm `ml-auto` giữ canh phải khi ẩn
- [x] `:show-kind="false"` ở LearningByCategoryView (Học theo loại đào tạo) + LearningBySkillView (Học theo kỹ năng) + LearningPathListView (Lộ trình học tập)
- [x] Màn trộn giữ nguyên badge: HomeView, CategoryContentsView (Học theo danh mục), HomeSectionView, SearchResultView (default true)
- [ ] Verify browser (user)

## Task 5 — Filter "Loại nội dung" (lọc riêng lộ trình / khóa học) ở màn Học theo danh mục — ✅ DONE
- [x] CategoryContentsView: thêm filter block `type` (Lộ trình / Khoá học) → map thẳng param `type` của endpoint contents (BE đã hỗ trợ sẵn `path`|`course`)
- [x] Cập nhật filterSelected + appliedGroups (chip "Loại nội dung") + handleReset + initFilters(['type',...])
- [x] Chọn 1 loại → chỉ loại đó; chọn cả 2 / không chọn → hiển thị cả hai
- [ ] Verify browser (user)

## Task 6 — Đếm đúng số "N nội dung" trên card danh mục (cộng cả lộ trình) — ✅ DONE
- [x] HomeCategoryService::build() cộng thêm pathCounts (LearningPath STATUS_ACTIVE) theo training_type_id, khớp màn Học theo danh mục trộn 2 loại
- [x] Cập nhật docblock (bỏ ghi chú "chỉ đếm subjects"); tái dùng countBy() (is_public gate cho guest/learner)
- [x] php -l sạch
- [ ] Verify browser (user)

## Task 7 — Card lộ trình: thêm thẻ kỹ năng + ẩn thẻ theo bộ lọc — ✅ DONE
- [x] PathCard: thêm thẻ kỹ năng (skill_name, icon ri-brain-line) cạnh thẻ loại đào tạo; props showTrainingType (default true) + showSkill (default false — giữ nguyên màn tìm kiếm)
- [x] LearningPathListView: showTrainingTypeTag = !lọc loại đào tạo; showSkillTag = !lọc kỹ năng → lọc TT chỉ hiện thẻ kỹ năng, lọc kỹ năng chỉ hiện thẻ TT, lọc cả 2 ẩn hết, không lọc hiện cả 2
- [x] item lộ trình đã có sẵn training_type_name + skill_name (LearningPathBrowseResource) — không đụng BE
- [ ] Verify browser (user)

## Task 8 — Thẻ loại đào tạo/kỹ năng cho 2 màn khóa học (LearnCard) + chống tràn tên dài — ✅ DONE
- [x] LearnCard: thêm thẻ training_type/skill (props showTrainingType/showSkill mặc định false — màn trộn không đổi); text bọc truncate + max-w-full + min-w-0 chống vỡ layout khi tên dài
- [x] LearningByCategoryView (Học theo loại đào tạo) → `:show-skill="true"` (hiện thẻ kỹ năng)
- [x] LearningBySkillView (Học theo kỹ năng) → `:show-training-type="true"` (hiện thẻ loại đào tạo)
- [x] PathCard: bổ sung truncate/max-w-full cho 2 thẻ (đồng nhất chống tràn)
- [x] Subject item đã có sẵn training_type_name + skill_name (SubjectBrowseResource) — không đụng BE
- [ ] Verify browser (user)

### Checkpoint — 2026-07-27
Vừa hoàn thành: CODE DONE 3/3 task (subagent-driven, implement haiku, review sonnet). Final review = SẴN SÀNG MERGE, 0 Critical/Important. php -l sạch. Không migration. KHÔNG commit git.
Đang làm dở: (không)
Bước tiếp theo: user verify browser (localhost:3001/hoc-theo-danh-muc?training_type_id=<id>) → quyết review/merge (mình không commit git).
Blocked:
