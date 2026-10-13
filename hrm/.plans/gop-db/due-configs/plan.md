# Plan — Cấu hình chặn luồng hàng quá hạn (@khoipv)

## Phase 1 — Port màn
### BE (`hrm-api`)
- [x] Quyền 1706 `Cấu hình chặn luồng hàng quá hạn` (type 10) vào `PermissionsTableSeeder` + insert DB local (chưa gán vai trò nào)
- [x] `Modules/Finance/Services/DueConfigService.php` (show: mục theo tab + công ty `status=1` + mục đang tích; update: diff từng công ty, ghi pivot, ghi log)
- [x] `Modules/Finance/Http/Controllers/V1/DueConfigController.php` + route `GET/PUT /v1/finance/due-configs` (checkPermission)
- [x] Đăng ký `CatalogHistoryService::TABLES['company_due_configs']` + nhãn nhóm trong `rowItemLabel()` (thuần thêm)
- [x] Migration dữ liệu `2026_10_13_000001_move_due_config_histories_to_catalog_histories` — đã chạy local: 204 dòng ERP → 212 log, đọc ngược đủ 922 thay đổi
- [x] Smoke test API qua HTTP kernel: không quyền 403 (GET/PUT); có quyền GET 200 (3 nhóm/21 mục, 31 mục, 5 công ty); PUT đổi → 200 + log đúng (+/−); PUT y nguyên → không log; công ty lạ / đã ngừng → 422; payload rỗng → 422; hoàn tác cấu hình công ty 3 về nguyên trạng. Đã xoá 2 log test (id 953, 954) + gỡ quyền tạm.
### FE (`hrm-client`)
- [x] `pages/admin/due-configs/index.vue` — V2BaseFormSection + 2 tầng V2BaseTabNavigation + V2BaseCheckbox + V2Footer (Lưu) + SystemInfoSection theo công ty; unsavedChangesMixin
- [x] Menu `components/subsystem-menu/admin.js` dưới "Hệ số công nghệ theo nhóm hàng hóa", `isShow` theo quyền mới
- [x] Compile FE (vue-template-compiler + babel): OK
- [ ] User gán quyền 1706 cho vai trò rồi mở trình duyệt kiểm (CHƯA bấm thật)

### Checkpoint — 2026-10-13
Vừa hoàn thành: BE + FE + migration lịch sử, smoke test API pass, compile FE pass. Đã push develop (api de0a3a485, client 03d265cd9).
Đang làm dở: không.
Bước tiếp theo: admin gán quyền "Cấu hình chặn luồng hàng quá hạn" → mở `/admin/due-configs` kiểm tích/bỏ tích, Lưu, lịch sử từng công ty, cảnh báo chưa lưu.
Blocked:
