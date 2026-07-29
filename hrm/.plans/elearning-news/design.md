# elearning-news — Tóm tắt thiết kế

- **Người phụ trách**: @junfoke
- **Ngày tạo**: 2026-07-17
- **Spec đầy đủ**: [docs/superpowers/specs/2026-07-17-elearning-news-design.md](../../docs/superpowers/specs/2026-07-17-elearning-news-design.md)

## Mục tiêu
Mục "Tin tức, Thông báo" trên portal elearning = **CMS tin bài một chiều** (như trang tin website). Chỉ admin đăng, học viên chỉ xem.

## Quyết định lớn (brainstorming)
- **Chỉ admin đăng bài** (học viên không đăng, không bình luận ở phase đầu).
- **Quản trị trong hrm-client** (hệ ERP); BE ở `Modules/Elearning`; portal elearning hiển thị.
- **Có danh mục** (`news_categories`).
- **Có bài nổi bật** (`is_featured`) + **đếm lượt xem** (`view_count`) ngay phase đầu.

## Cấu trúc
- 2 bảng mới: `news_categories`, `news_articles` (theo convention DB: solution_version_id NOT NULL, created_by/updated_by, không SoftDeletes).
- API admin `/api/v1/elearning/admin/news*` (checkPermission), API portal `/api/v1/elearning/news*` (chỉ trả published).
- Quyền mới: **"Quản lý tin tức elearning"** trong PermissionsTableSeeder.

## Phase
1. **BE** — migration + entities + API admin/portal + validation + quyền.
2. **FE Admin (hrm-client)** — danh sách + form bài viết + màn danh mục.
3. **FE Portal (elearning)** — route `/tin-tuc` + `/tin-tuc/:slug` + service + views + menu header.

## Ngoài phạm vi (để sau)
Bình luận, học viên đăng bài, hẹn giờ phát hành, push/email thông báo.
