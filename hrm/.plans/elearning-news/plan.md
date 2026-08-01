# elearning-news — Plan

- **Người phụ trách**: @junfoke
- **Ngày tạo**: 2026-07-17
- **Design**: [design.md](design.md) | **Spec**: [../../docs/superpowers/specs/2026-07-17-elearning-news-design.md](../../docs/superpowers/specs/2026-07-17-elearning-news-design.md)
- **Plan chi tiết**: [../../docs/superpowers/plans/2026-07-17-elearning-news.md](../../docs/superpowers/plans/2026-07-17-elearning-news.md)

## Phase 1 — Backend
- [x] Task 1: Migration 2 bảng `elearning_news_categories` + `elearning_news_articles`
- [x] Task 2: Entities `NewsCategory` + `NewsArticle` (scope published, makeUniqueSlug)
- [x] Task 3: Thêm quyền "Quản lý tin tức elearning" vào PermissionsTableSeeder (id 1083, guard api) — chờ user seed
- [x] Task 4: Admin `NewsCategoryController` + route (Modules/Training, prefix training/elearning-news-categories)
- [x] Task 5: Admin `NewsArticleController` + route (training/elearning-news)
- [x] Task 6: Portal `PublicNewsService` + `PublicNewsController` + route (elearning/public/news)
- [x] Task 7: Verify BE end-to-end bằng tinker — PASS

## Phase 2 — FE Admin (hrm-client) — theo V2Base (user chọn)
- [x] Task 8: Màn quản lý danh mục `pages/training/elearning-news/categories.vue` + modal — verified browser
- [x] Task 9: Màn danh sách bài `pages/training/elearning-news/index.vue` + modal form (CKEditor + upload ảnh) — verified browser (fix published_at cast + $nextTick modal sửa)

## Phase 3 — FE Portal (elearning)
- [x] Task 10: api.get inline + routes /tin-tuc, /tin-tuc/:slug (api.js giữ nguyên theo convention thực tế)
- [x] Task 11: `NewsListView.vue` (featured + card + lọc danh mục) — verified browser
- [x] Task 12: `NewsDetailView.vue` + nối menu header "Tin tức, Thông báo" — verified browser

**→ HOÀN TẤT (2026-07-17): verified 3 tầng BE + Admin (hrm-client) + Portal (elearning). User đã migrate + gán quyền. 2 bug fix trong verify (published_at cast, $nextTick modal sửa).**

---

## Phase 4 — Fix bug khóa danh mục (2026-07-20)
Quy tắc user chốt: **giữ ràng buộc không cho khóa danh mục còn bài viết**; đảm bảo **mở khóa luôn chạy được** + **ẩn bài của danh mục đã khóa khỏi portal**.

- [x] Task 13: Reproduce bằng Playwright — xác nhận nút mở khóa danh mục "ddd" (0 bài, Khóa) bị disabled do **dev server chạy bundle stale**; code đã commit (`:disabled="item.is_active && item.articles_count > 0"`) vốn đã đúng. Recompile → mở khóa chạy đúng (ddd → Hoạt động). Bug 2 & 3 KHÔNG phải lỗi code, chỉ do bundle cũ.
- [x] Task 14: FE `categories.vue` — hardening `!!item.is_active` + comment ghi rõ quy tắc (không đổi hành vi, giúp rõ intent + buộc recompile).
- [x] Task 15: BE `NewsArticleController::store()` — chặn gán bài vào danh mục đã khóa (khi tạo mới hoặc đổi sang danh mục khóa khác) → trả 422 `category_id`. (Bug 1)
- [x] Task 16: BE `PublicNewsService` (list + detail + related) — ẩn bài viết thuộc danh mục đã khóa khỏi portal (bài không có danh mục vẫn hiển thị). (Bug 1)
- [x] Task 17: Verify end-to-end bằng Playwright + curl:
  - Mở khóa "ddd" (Khóa→Hoạt động) chạy đúng sau recompile.
  - Khóa "ddd" → dropdown Tạo bài loại đúng "ddd" (còn lại 4 danh mục active).
  - Portal `list` / `detail` / `categories` trả 200, không lỗi SQL sau khi thêm filter.
  - `php -l` 2 file BE: no syntax errors.

### Checkpoint — 2026-07-20
Vừa hoàn thành: Fix bug khóa danh mục tin tức. Bug 2&3 (không mở khóa được) là **stale dev bundle**, code commit vốn đúng — recompile là hết. Bug 1 fix ở BE: `store()` chặn danh mục khóa + `PublicNewsService` ẩn bài của danh mục khóa khỏi portal.
Đang làm dở: (không)
Bước tiếp theo: User seed/deploy BE; nếu FE production cũng dính stale thì build lại. Cân nhắc có nên đổi rule "đếm bài" chỉ tính bài đang hiển thị (published) thay vì mọi bài — hiện `withCount('articles')` đếm cả bài Khóa (draft).
Blocked: 

---

## Đã xong (user thực hiện)
- [x] `php artisan migrate` (Task 1)
- [x] Seed lại PermissionsTableSeeder + gán quyền "Quản lý tin tức elearning" (Task 3)
