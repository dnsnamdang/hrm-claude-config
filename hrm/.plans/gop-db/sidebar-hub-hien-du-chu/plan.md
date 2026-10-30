# Thanh menu hub bị cắt chữ — hiện đủ tên (phản hồi nhóm chat, chưa có số Redmine) — @cuong61n

Phản hồi 30/10/2026 (ảnh chụp PROD `/human/self-notification`): menu trái phân hệ hub mất chữ — "VĂN BẢN - HỒ SƠ PHÁ…", "Quản lý thông báo nội …", "Quản trị hành chín…", panel nhóm con "Quyết định về nhân…". Yêu cầu hiển thị hết.
Nhánh: `gop_db` (worktree `worktrees/gop_db-client`, test cổng 3002), chưa commit.

## Phase 1 — Hiện đủ chữ
### FE (hrm-client)
- [x] 30/10/2026 `components/sale/SaleHubSidebar.vue` (khung chung mọi phân hệ hub): rail bung 220px trước ép `nowrap + ellipsis` → cho xuống dòng; khoá bề rộng khối chữ (tên phân hệ 150px, mục rail 134px) để lúc animate rail chữ không nhảy dòng. Tên phân hệ giữ tối đa 2 dòng (ô logo cao 60px).
- [x] 30/10/2026 Panel nhóm con `.scat-nm`: bỏ `ellipsis`, cho xuống dòng.
- [x] 30/10/2026 Test Playwright cổng 3002 (1440px), phân hệ Văn bản - HS pháp lý: trước sửa 6 mục rail bị cắt; sau sửa 0 mục cắt, tên phân hệ 2 dòng đủ chữ, panel "Quản trị hành chính - nhân sự" 6 nhóm không nhóm nào cắt; rail thu gọn 58px vẫn ẩn chữ đúng. ĐẠT.
- [ ] Commit + push `gop_db`, deploy PROD.
