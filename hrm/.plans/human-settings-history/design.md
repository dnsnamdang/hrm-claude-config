# human-settings-history — Lịch sử thay đổi màn Cấu hình nhân sự

Người phụ trách: @khoipv

## Mục tiêu

Thêm "Lịch sử thay đổi" (audit log ai sửa gì, cũ → mới, lúc nào) cho màn **Cấu hình** module Nhân sự (`/human/settings`).

## Scope (user đã chốt 2026-07-15)

- Track **CẢ 2 phần** của màn:
  1. **4 trường cấu hình chung** (lưu qua endpoint dùng chung `POST general-regulations`): `base_salary` (Lương cơ bản), `tang_tham_nien` (% tăng lương thâm niên), `seniority_cycle` (Chu kỳ xét thâm niên tháng), `using_manpower` (Dùng định biên — boolean radio).
  2. **Bảng Tỉ lệ đóng BHXH** (`insurance_configs`, CRUD `human/insurance_config`): thêm/sửa/xóa dòng — track 11 trường nhập (date + 5 tỉ lệ NSDLĐ + 5 tỉ lệ NLĐ), **bỏ 3 cột tổng tự tính** (employer_total, worker_total, total).
- **TÁCH RIÊNG hoàn toàn khỏi bên Chấm công**: bảng history riêng `human_setting_history` (module Human), KHÔNG đụng `general_regulation_history` / TRACKED_FIELDS hiện có của màn Quy định chung.
- **KHÔNG permission riêng** — ai vào được màn thì xem được lịch sử.

## Quyết định thiết kế

- **1 bảng chung cho cả màn** `human_setting_history` (theo precedent overtime_regulation_history gộp nhiều loại action): cột `general_regulation_id` nullable (action=update) + `insurance_config_id` nullable (action=insurance_*), `company_id`, action, old/new JSON, changed_by/changed_at.
- 4 trường config: biến thể **subset-diff** (BE diff, JSON chỉ gồm trường đổi), action `update`. Log trong `GeneralRegulationService::save()` bằng bộ method RIÊNG (`buildHumanSettingSnapshot`/`normalizeHumanSettingValue`/`logHumanSettingHistoryIfChanged`) — không sửa logic timesheet hiện có, endpoint dùng chung nên trường ngoài whitelist không sinh log.
- Bảng BHXH: biến thể **full-snapshot** (skill: entity nhiều action) — `insurance_create` (new=full), `insurance_update` (old+new full, FE diff, không đổi → không log), `insurance_delete` (old=full). Log qua helper static `HumanSettingHistory::log()` try/catch (không làm hỏng luồng lưu).
- Endpoint `GET /v1/human/settings/histories` (auth:api, scope company, sort cũ→mới) — controller + service mới trong module Human.
- FE: nút `V2BaseButton light` + `ri-history-line` góc phải trên card; modal `pages/human/settings/components/HumanSettingHistoryModal.vue` (copy GeneralHistoryModal): cũ ĐỎ → mới XANH, dot create xanh/update amber/delete đỏ, bộ lọc Thao tác/Người/Từ-Đến ngày, insurance hiện "Ngày hiệu lực MM/YYYY" làm nhãn dòng.
- ⚠️ Màn AUTO-SAVE (watcher deep trên `model`) — nút + modal tự chứa state, không đụng `model`.

Spec chi tiết: `docs/superpowers/specs/2026-07-15-human-settings-history-design.md`
