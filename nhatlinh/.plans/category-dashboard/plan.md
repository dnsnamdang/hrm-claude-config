# Plan — Dashboard phân hệ Danh mục

- Spec: `docs/superpowers/specs/2026-07-03-category-dashboard-design.md`
- Plan chi tiết (bite-sized, cho executor): `docs/superpowers/plans/2026-07-03-category-dashboard.md`
- Design tóm tắt: `.plans/category-dashboard/design.md`
- Người phụ trách: @manhcuong

## Phase 1 — Backend

- [x] T1: Permission `1142 Xem dashboard danh mục` (seeder, type=8 nhóm "Danh mục chung") + insert tay DB dev + gán role 1 (review OK; lệnh `permission:cache-reset` warning "Unable to flush cache" nhưng registrar flush chạy được — role 1 hasPermissionTo YES đã verify)
- [x] T2: `CategoryDashboardService` (kpis + 5 phân bố + data_quality 4 loại cảnh báo, chỉ tính bản ghi Hoạt động, items ≤10/loại) + smoke test tinker khớp query tay 100% (review: fix 1 Important `!$row->name`→`=== null`; 3 Minor để final review: magic number classification 2, 3 khối lặp dataQuality, labels status không dùng Product::STATUSES)
- [x] T3: `DashboardController` (thay stub) + route gắn `checkPermission:Xem dashboard danh mục` (review: controller+middleware đúng 100%; finding "sửa route khác" là false positive — price-tiers là uncommitted change của feature cũ, đã xác minh với HEAD)

## Phase 2 — Frontend

- [x] T4: store `category-dashboard.js` (apiGetMethod, không tham số) (review Approved)
- [x] T5: `pages/category/dashboard.vue` (thay stub — 5 KPI card + bar nhóm hàng + 2 donut phân loại/trạng thái + bar NCC theo nhóm + bar hãng SX⇄xuất xứ toggle + khối cảnh báo 4 tab, style copy dashboard kho) — review Approved; verify tĩnh template+script+scss OK; apexchart đăng ký local như dashboard kho (project không có global registration)
- [x] T6: menu "Tổng quan" thêm `isShow: ['Xem dashboard danh mục']` + `/category` redirect sang dashboard khi có quyền (review Approved; ⚠️ menu "Kho" biến mất / isShow các mục khác = uncommitted change của feature cũ, đã xác minh với HEAD + STATUS.md — không phải lỗi task này)

## Checkpoint

### Checkpoint — 2026-07-03 (CODE HOÀN THÀNH 6/6 TASK + FINAL REVIEW: SẴN SÀNG BÀN GIAO)
Vừa hoàn thành: Toàn bộ 6 task (subagent-driven, mỗi task review riêng) + final review model mạnh nhất — 0 Critical/Important. Chưa commit.
- BE: permission 1142 (seeder + insert tay DB dev + gán role 1, registrar flush verify hasPermissionTo YES), CategoryDashboardService (kpis + 5 phân bố + 4 cảnh báo, smoke test tinker khớp query tay 100%, warning_count=108 trên DB dev), DashboardController + route checkPermission.
- FE: store category-dashboard, pages/category/dashboard.vue (5 KPI + bar nhóm hàng + 2 donut + bar NCC/nhóm + bar hãng SX⇄xuất xứ toggle + 4 tab cảnh báo; apexchart local import như dashboard kho), menu "Tổng quan" isShow 1142, /category redirect khi có quyền.
- Fix trong quá trình: 1 Important T2 (`!$row->name` → `=== null` trong topWithUnclassified). 2 finding reviewer là false positive do working tree chứa uncommitted change feature cũ (price-tiers routes, menu Kho) — đã xác minh với HEAD.
- Minor để sau (final review triage): magic number classification `2` (thêm const cần hỏi vì sửa entity chung), productByStatus tự khai labels thay vì Product::STATUSES; bỏ qua: gộp helper dataQuality, mixin CheckPermission thừa trong dashboard.vue.
Đang làm dở: —
Bước tiếp theo (user): test trình duyệt — 5 KPI + 4 chart render, toggle Hãng SX⇄Xuất xứ, click card cảnh báo cuộn xuống, tab count=0 hiện bảng rỗng, phân quyền 2 chiều (menu ẩn + URL thẳng → 404, /category redirect 2 chiều — lưu ý có thể flash welcome ~vài trăm ms do redirect ở mounted), API lỗi có toast; rồi commit 2 repo khi muốn. Deploy: seeder đã có 1142, DB đang chạy insert tay + gán role + permission:cache-reset.
Blocked:
