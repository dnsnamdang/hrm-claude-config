# elearning-news — Progress Ledger

Plan: docs/superpowers/plans/2026-07-17-elearning-news.md
Bắt đầu execute: 2026-07-17 (subagent-driven, không git)

## Trạng thái task
- Task 1 (migration): XONG (file tạo, php -l sạch, khớp spec)
- Task 2 (entities): XONG (2 file, BaseModel đúng, php -l sạch)
- Task 3 (permission seeder): XONG (id 1083, guard 'api', type 5; php -l sạch). CHỜ user seed lại + gán quyền.
- Task 4 (NewsCategoryController + route): XONG (import d9, group d149; php -l sạch). route:list fail do bug Decision có sẵn → verify route ở Task 7.
- Task 5 (NewsArticleController + route): XONG (import d10, group d162, /categories trước /{id}; php -l sạch)
- Task 6 (PublicNews service/controller/route): XONG (import d16, route d57-59; php -l sạch)
- Task 7 (verify tinker): XONG (2026-07-17). User đã migrate + gán quyền. Tinker PASS: slug unique (bai-test-1→-2), list chỉ published, view_count tăng, related loại draft, categories active. Đã dọn data test (0 bản ghi còn).
  >>> PHASE 1 BE HOÀN TẤT + VERIFIED.
- Task 8 (FE danh mục): XONG theo V2Base (user chọn style V2Base). Modal add_news_category_modal.vue + categories.vue: V2BaseButton/V2BaseIconButton + modal V2Base (hide-footer, header icon tròn), list b-table. API theo BE hall_of_fame (apiPost addNewsCategory id-in-body, lỗi data.error_messages, apiGet toggle, apiDelete). Action addNewsCategory thêm vào store/actions.js (additive). CHỜ verify browser.
- Task 9 (FE bài viết): XONG + VERIFIED browser. index.vue + add_news_article_modal.vue (V2Base, CKEditor V2BaseHtmlEditor, upload ảnh files/upload). Action addNewsArticle additive. Verify: tạo bài (CKEditor gõ thật), validate inline "Bắt buộc nhập nội dung" (422 map đúng), toggle-status Nháp→Đã đăng OK.
  >>> BUG FIX trong verify: published_at KHÔNG cast datetime → cột Ngày đăng trống + portal format lỗi. Đã thêm 'published_at'=>'datetime' vào $casts NewsArticle. Verify lại: Carbon OK, format 17/07/2026 OK.
  >>> Rename data.fields → tableFields (categories.vue + index.vue) để bớt warning; còn 1 warning BTable-fields là PRE-EXISTING toàn app (hall_of_fame cũng có).
  >>> Data test còn: category "Thông báo" (id1) + bài "Khai giảng khóa đào tạo an toàn lao động Q3" (id3, published, featured, chưa gán category). Dùng cho verify portal.
  >>> BUG FIX 2 (verify edit): modal Sửa mở form TRỐNG do openEdit set editId + show cùng tick → @show đọc this.id stale. Fix: openCreate/openEdit dùng $nextTick trước show (index.vue). Verify lại: Sửa nạp đủ data + chọn danh mục qua dropdown + Lưu OK (Danh mục="Thông báo").
- Task 10-12 (FE portal): XONG + VERIFIED browser (3001). api.get inline (như HomeSectionView, api.js giữ nguyên), routes /tin-tuc + /tin-tuc/:slug, NewsListView (pills danh mục + card nổi bật + grid + Xem thêm + placeholder ảnh trung tính), NewsDetailView (breadcrumb + badge + v-html + related + 404 + watch slug), AppHeader menu <a demo>→<router-link to=/tin-tuc>. Helper newsFormat.js, component NewsCard/NewsFeaturedCard. Verify: list hiện bài featured, detail tăng view_count (1→3), menu điều hướng OK.

- BỔ SUNG (user báo thiếu): thêm 2 mục vào menu sidebar Đào tạo (components/menu-sidebar.js, cạnh Vinh danh học viên): "Tin tức - Bài viết" (/training/elearning-news) + "Tin tức - Danh mục" (/training/elearning-news/categories), gate isShow ['Quản lý tin tức elearning']. Verified DOM có link đúng.

- REWORK UI ADMIN (user yêu cầu làm như Kỹ năng/Bài học/Khoá học — chuẩn V2Base đầy đủ):
  2 màn index.vue + categories.vue rewrite dùng V2BaseFilterPanel (chỉ bài viết) + V2BaseDataTable (cả 2) như skills/attachment-type. Bỏ b-table + PageHeader. Giữ nguyên 2 modal đã verified. Article giữ $nextTick openCreate/openEdit. BE NewsArticleController::index bổ sung current_page/per_page/last_page/from/to để feed pagination V2BaseDataTable. Verified browser: filter panel + data table + phân trang render đúng, 0 lỗi console (warning BTable biến mất), modal mở OK. Cũng đã thêm menu sidebar (menu-sidebar.js).

- FIX màn Danh mục (user báo 3 lỗi): (1) BE NewsCategoryController::toggle chặn khóa khi articles_count>0 (422) + FE disable nút khóa; (2) nhãn trạng thái đổi "Đang bật/Đã tắt" → "Hoạt động/Khóa" (icon check/lock) như attachment-type; (3) title bảng "Danh mục tin tức"→"Danh sách danh mục tin tức" hết lặp với nav pageTitle. Verified browser.

- FIX vòng 2 (user review UI, 2026-07-17):
  * Trạng thái BÀI VIẾT: đổi "Nháp/Đã đăng" → "Hoạt động/Khóa" (published→Hoạt động, draft→Khóa) ở list + modal + filter options. Giữ nguyên giá trị BE draft/published (portal chỉ hiện published).
  * Modal bài viết: đưa Trạng thái + Nổi bật LÊN TRÊN cùng Tiêu đề/Danh mục (trước nội dung), không để dưới CKEditor nữa.
  * Danh mục: kéo-thả sắp thứ tự như training_types/hall_of_fame — BE NewsCategoryController::updateSortOrder + route POST elearning-news-categories/sort-order + index orderBy CASE sort_order=0 xuống cuối; FE modal sort_news_category_modal.vue (vuedraggable) + nút "Sắp xếp"; bỏ ô "Thứ tự" thủ công trong modal thêm/sửa. Verified: kéo + Lưu persist đúng (Thông báo=1, Sự kiện=2).
  * Đã verify không có icon lạ ở cột Tên (DOM chỉ 2 nút trong cột Hành động).
  Data test giờ: 2 danh mục (Thông báo, Sự kiện) + 1 bài (Khai giảng…).

- FIX view_count off-by-one (user báo): PublicNewsService::detail dùng `increment()` (đã cập nhật DB+model) NHƯNG trả `view_count + 1` → detail dư 1 so với list. Bỏ `+ 1`, trả `(int)$article->view_count`. Verify tinker: DETAIL_RETURN == DB_AFTER.

- REDESIGN portal list (user review):
  * Bỏ header lớn thừa (icon loa + title + subtitle) — đã có ở menu + breadcrumb.
  * Layout 70/30: trái (lg:col-span-8) danh sách bài + PHÂN TRANG SỐ (1,2,3 + prev/next, chỉ hiện khi >1 trang) thay cho "Xem thêm"; phải (lg:col-span-4) aside sticky "Tin nổi bật" ghim bài is_featured.
  * BE PublicNewsService::list thêm param `featured` (lấy riêng tin nổi bật cho sidebar). FE fetch featured riêng.
  * Menu portal (AppHeader): thêm active-state — helper navCls(path, exact) làm nổi bật mục trang đang xem (Trang chủ exact, còn lại startsWith để /tin-tuc/:slug vẫn active). Verified: trên /tin-tuc chỉ Tin tức ACTIVE.

=== HOÀN TẤT TOÀN BỘ FEATURE (2026-07-17) — verified 3 tầng BE+Admin+Portal ===
Test data còn trong DB dev: category "Thông báo"(id1) + bài "Khai giảng..."(id3, published/featured, nội dung test hơi lặp do gõ verify). User có thể xoá/sửa qua UI admin.
Bug đã fix trong verify: (1) published_at cast datetime; (2) $nextTick modal sửa. Warning BTable-fields là pre-existing toàn app (hall_of_fame cũng có).
