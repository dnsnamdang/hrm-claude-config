# Plan — human-settings-history

Người phụ trách: @khoipv
Design: `.plans/human-settings-history/design.md`

## Phase 1 — BE + FE lịch sử thay đổi màn /human/settings

### BE (hrm-api)

- [x] 1. Migration `2026_07_15_000001_create_human_setting_history_table` (module Human): id, general_regulation_id nullable index, insurance_config_id nullable index, company_id nullable index, action, old_value/new_value text nullable, changed_by nullable, changed_at useCurrent, timestamps. PHPDoc up()/down(). **ĐÃ MIGRATE** (targeted `--path`).
- [x] 2. Entity `Modules/Human/Entities/HumanSettingHistory.php` — fillable + `user()` belongsTo Employee + static `log()` try/catch.
- [x] 3. `GeneralRegulationService`: const `HUMAN_SETTING_TRACKED_FIELDS` (4 trường) + `HUMAN_SETTING_BOOLEAN_FIELDS` (using_manpower) + 3 method riêng (snapshot/normalize/logIfChanged) + gọi trong `save()` (2 dòng thêm, không đổi logic cũ).
- [x] 4. `InsuranceConfigService`: const `HISTORY_SNAPSHOT_FIELDS` (11 trường, bỏ 3 tổng) + log full-snapshot 3 action trong `store()` (create/update, không đổi → không log) + `delete()`.
- [x] 5. `HumanSettingHistoryService::histories()` (scope company, sort changed_at ASC + id ASC, trả changed_by_name/changed_at d-m-Y H:i:s/changed_at_raw) + `HumanSettingHistoryController::histories()` + route `GET /human/settings/histories` (auth:api group).

### FE (hrm-client)

- [x] 6. `pages/human/settings/components/HumanSettingHistoryModal.vue` — copy GeneralHistoryModal: 4 nhánh action, FIELD_LABELS khớp BE, using_manpower → nhãn radio, base_salary format số, date → MM/YYYY, cũ đỏ/mới xanh, dot theo action, bộ lọc Thao tác/Người/Từ-Đến ngày.
- [x] 7. `pages/human/settings/index.vue` — nút `V2BaseButton light` + `ri-history-line` size sm (góc phải trên) + mount modal. KHÔNG đụng `model`/watcher auto-save.

### Verify

- [x] 8. `php -l` 7 file sạch + migrate OK + tinker round-trip THẬT (auth TpEmployee id 13, company 1): A đổi 1 trường → 1 log subset đúng by=13; B no-op → 0; C boolean true vs 0/1 → 0; D đổi 2 trường → 1 dòng 2 key; E profit_margin_threshold (ngoài whitelist) → 0; F general_regulation_history delta = 0; G/H/K insurance create/update/delete đúng full-snapshot; I insurance no-op → 0; L histories() count/sort ASC/format/changed_by_name "DNS Admin" đúng. Dọn log test = 0, giá trị khôi phục nguyên.
- [x] 9. Playwright (localhost:3000, user company 4 — seed 4 log mẫu thay vì đổi giá trị thật vì màn AUTO-SAVE): nút hiện đúng vị trí; modal render đủ 4 nhánh (update diff đỏ→xanh gồm Lương cơ bản 1.000.000→1.200.000 + Dùng định biên; create dot xanh + 11 trường + nhãn "Ngày hiệu lực 07/2026"; insurance_update chỉ hiện 1 trường đổi 14→17.5; delete dot đỏ + liệt kê đỏ); sort cũ→mới; scope company đúng (log company 1 không hiện với user company 4); bộ lọc Thao tác=Xóa → còn 1 dòng; network toàn phiên 100% GET — mở/đóng modal + lọc KHÔNG bắn POST. Đã xóa 4 log seed (remaining=0).

### Checkpoint

### Checkpoint — 2026-07-15 15:50
Vừa hoàn thành: Toàn bộ Phase 1 (task 1-9) — CODE DONE + VERIFIED (tinker + Playwright), data test đã dọn sạch.
Đang làm dở: (không có)
Bước tiếp theo: User verify browser bằng mắt trên môi trường thật. KHÔNG commit git (chưa có yêu cầu).
Blocked: (không có)
