# Cấu hình trang chủ Elearning — Plan

- **Owner**: @junfoke | **Ngày**: 2026-07-23
- **Plan chi tiết**: [docs/superpowers/plans/2026-07-23-cau-hinh-trang-chu-elearning.md](../../docs/superpowers/plans/2026-07-23-cau-hinh-trang-chu-elearning.md)
- **Spec**: [docs/superpowers/specs/2026-07-23-cau-hinh-trang-chu-elearning-design.md](../../docs/superpowers/specs/2026-07-23-cau-hinh-trang-chu-elearning-design.md)

## Phase 1 — BE Elearning (lưu + đọc)
- [x] Task 1: Migration `elearning_home_settings` + Entity `HomeSetting` (current/default + normalizedHeroSources)
- [x] Task 2: Endpoint public `GET /v1/elearning/public/site-config` + route

## Phase 2 — BE Training (ghi cấu hình)
- [x] Task 3: `HomeConfigController` (index/updateHero/updateFooter) + nhóm route `elearning-home-config` + checkPermission
- [x] Task 4: Thêm quyền `Quản lý cấu hình trang chủ elearning` vào PermissionsTableSeeder (user chạy lại seeder)

## Phase 3 — FE admin (hrm-client)
- [x] Task 5: Màn `/training/home_config` (2 tab Hero/Footer, lỗi inline 422) + menu item

## Phase 4 — FE portal (elearning)
- [x] Task 6: Store `useSiteConfigStore` + fetch lúc app init
- [x] Task 7: Refactor `buildHeroSlides` theo cấu hình + getter `heroSlides` (+ badge newest); TDD hàm thuần rồi xóa test
- [x] Task 8: `AppFooter` đọc store (ẩn dòng rỗng / tắt giới thiệu)

## Ghi chú
- KHÔNG tự migrate/seed/git. User chạy migration + PermissionsTableSeeder + gán quyền.
- Verify: BE php -l + tinker; UI Playwright (dev account); hero.spec là test tạm → xóa sau.

## Checkpoint — 2026-07-23
Vừa hoàn thành: CODE DONE 8/8 task (subagent-driven Opus điều phối; implement haiku/sonnet; final review Opus = SẴN SÀNG MERGE, 0 Critical/Important). php -l sạch mọi file BE; buildHeroSlides verify 8/8 (test tạm đã xóa).
Đang làm dở: (không) — chờ user chạy migrate/seed + verify browser.
Bước tiếp: user (1) migrate `elearning_home_settings`; (2) chạy lại PermissionsTableSeeder (quyền id 1084); (3) gán quyền `Quản lý cấu hình trang chủ elearning` cho role; (4) verify browser admin `/training/home_config` + portal hero/footer.
Blocked: (không)

## Bổ sung QUOTA — fix winner-takes-all (2026-07-27, user feedback)
- [x] Lỗi logic: thuật toán cũ "lấp theo ưu tiên từ trên xuống, hết mới nhảy nguồn" → nguồn ưu tiên 1 đủ data chiếm HẾT slot, nguồn dưới không bao giờ hiện (winner-takes-all). User đề xuất chuyển sang "phân bổ tỷ trọng (slot allocation)".
- [x] Giải pháp: thêm `max_slots` (quota) mỗi nguồn + thuật toán 2-pass: Pass1 lấy tối đa max_slots/nguồn theo ưu tiên tới đủ tổng; Pass2 bù chỗ trống từ item dư nếu nguồn trên thiếu data. Mặc định quota need=2/recommend=1/popular=2/newest=2.
- [x] UI: đổi ▲▼ → KÉO-THẢ (vuedraggable ^2.24.3 có sẵn); thêm cột "Số lượng tối đa" (ô số/nguồn, disable khi tắt); đổi label "Tổng số slide tối đa hiển thị"; note giải thích quota+bù. Tag màu Nội bộ(cam)/Mọi người(xanh) gom 1 cột.
- Files: BE Entity HomeSetting (DEFAULT_HERO_SOURCES + max_slots, normalizedHeroSources, MAX_SLOTS_PER_SOURCE=10); HomeConfigController (validate/return/save max_slots); PublicBrowseController siteConfig (sources đổi string[]→[{key,max_slots}]). FE elearning heroSlides.js (thuật toán 2-pass), siteConfig.js (default object). FE admin home_config/index.vue (draggable + cột quota + bỏ moveSource, sort_order theo index mảng). KHÔNG migration (hero_sources là JSON).
- VERIFIED: php -l sạch; unit test buildHeroSlides 8/8 (winner-takes-all fixed, bù chỗ trống, quota tỷ lệ, khử trùng, fallback) — file test đã xóa. Playwright: màn admin cột quota + badge + kéo-thả OK; lưu quota=3 persist; reorder (popular lên đầu) qua vm→save→siteConfig persist đúng; portal bundle mới OK (không fallback, đọc object sources). Khôi phục default sau test. LƯU Ý: Playwright synthetic drag KHÔNG kích được sortablejs (giới hạn tool, không phải bug) — verify reorder qua Vue instance + save path.

## Bổ sung UX (2026-07-23, user feedback)
- [x] Màn Hero khó hiểu "mỗi nguồn bao nhiêu slide" → thêm hộp giải thích cơ chế (tối đa N + lấp theo ưu tiên từ trên xuống + cá nhân hoá, không cố định slide/nguồn) + badge "Chỉ nhân viên nội bộ" (need/recommend) vs "Mọi người" (popular/newest) + mô tả từng nguồn. Chỉ sửa FE hrm-client pages/training/home_config/index.vue (thêm sourceMeta + metaOf + CSS). KHÔNG đụng DB/BE. VERIFIED Playwright: hiển thị đúng, 0 lỗi console.
- Xác nhận câu hỏi user: học viên ngoài KHÔNG vỡ — need/recommend rỗng (chỉ nội bộ), hero tự lấp từ popular/newest (công khai); tắt hết → fallback slide. (BE buildHomeSection dòng 806-825 + sectionBaseQueries is_public.)

## 4 Minor để sau (không chặn merge)
1. HomeConfigController dùng magic property `$request->max_slides`/`->intro_enabled` — style.
2. updateHero không ràng buộc 4 sort_order phân biệt (chỉ 4 key) — FE luôn gán 1..4.
3. home_config max_slides chỉ min/max HTML, không clamp trước submit (dựa 422 BE).
4. buildHeroSlides `maxSlides || 5` → maxSlides:0 fallback 5 (vô hại, BE min 1).
