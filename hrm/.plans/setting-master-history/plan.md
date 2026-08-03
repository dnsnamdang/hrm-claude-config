# Plan — setting-master-history

Người phụ trách: @khoipv

## Phase 1 — Lịch sử thay đổi màn Cài đặt (setting-master)

### BE
- [x] T1. Migration `master_setting_history` (PHPDoc up/down, không company_id/entity_id) — ĐÃ migrate
- [x] T2. Model `App\Models\MasterSettingHistory` (+ quan hệ user → Employee)
- [x] T3. `MasterSettingService`: TRACKED_FIELDS(8) + BOOLEAN_TRACKED_FIELDS(5) + normalizeTrackedValue + buildTrackedSnapshot + logHistoryIfChanged; sửa `store()` diff; thêm `histories()` sort cũ→mới
- [x] T4. `MasterSettingController::histories()`
- [x] T5. Route `GET /v1/master-settings/histories` (auth:api) — đặt TRƯỚC GET '/', giữ index/store public

### FE
- [x] T6. `components/setting/master/MasterSettingHistoryModal.vue` (FIELD_LABELS 8, boolean Có/Không, logo render 2 ảnh viền đỏ/xanh, bộ lọc client-side)
- [x] T7. `pages/timesheet/setting/setting-master/index.vue`: nút light ri-history-line + gắn modal

### Verify
- [x] T8. `php -l` sạch + tinker: đổi 1 trường→1 log subset; không đổi→0 log; ngoài whitelist→0 log; boolean true vs "1"→0 rác; 2 trường→1 dòng 2 key; histories() format + sort cũ→mới. + store() write-path THẬT (auth id13 → changed_by=13, name "DNS Admin", revert khôi phục đúng)
- [x] T9. Playwright: mở modal → GET histories 200, KHÔNG POST; render 2 log sort cũ→mới, Tiêu đề/ERP đỏ→xanh, Có/Không đúng, logo 2 ảnh load; 0 lỗi console
- [x] T10. Dọn log test bằng tinker (history=0), title nguyên vẹn, không ghi nhầm master_settings

### Checkpoint — 2026-07-14 15:03 (inline Opus 4.8)
Vừa hoàn thành: toàn bộ Phase 1 — CODE DONE + VERIFIED (tinker + Playwright).
Đang làm dở: (không)
Bước tiếp theo: user verify browser bằng mắt (hard-refresh màn Cài đặt) + quyết định merge/commit (chưa git theo quy tắc).
Blocked:
