# Lịch sử thay đổi tab Thông tin chung — Cấu hình phân hệ Giao việc (assign-settings-history)

Người phụ trách: @khoipv
Spec đầy đủ: `docs/superpowers/specs/2026-07-16-assign-settings-history-design.md`

## Mục tiêu

Nút "Lịch sử thay đổi" + modal timeline trên tab **Thông tin chung** màn `/assign/settings`, ghi nhận ai sửa gì (cũ đỏ → mới xanh), lúc nào.

## Quyết định đã chốt (2026-07-16)

- ~~Chỉ track tab Thông tin chung~~ → **Phase 2 (cùng ngày): track CẢ 2 tab**. Tab 1: 23 scalar + 3 list (khung giờ, 2 DS chức vụ). Tab 2 "Giới hạn khoảng cách": 2 trường km + list `places_origin` (item {name, lat, lng} từ bảng `assign_config_place_origins`, so theo nội dung, KHÔNG track cột `place`). Chung 1 bảng log, 1 lần Lưu đổi cả 2 tab = 1 dòng. **Nút lịch sử RIÊNG từng tab — modal scope theo tab** (`open('common')` / `open('places')`), chỉ hiện key thuộc tab mình, dòng không có key → ẩn.
- **Không permission riêng** — ai vào được màn thì xem được.
- **Phương án A — subset-diff mở rộng cho danh sách** (mẫu human-settings-history): bảng `assign_config_history` (module Assign, có `company_id` — config theo từng công ty), old/new = JSON chỉ trường thay đổi; 3 list coi như 3 "trường" (lưu mảng cũ + mới, FE render chip thêm xanh/bớt đỏ, tên chức vụ denormalize tại thời điểm log).
- Chỉ action `update`; first save của công ty → log update với phía cũ = trống.
- Diff theo trạng thái DB trước/sau trong `AssignConfigService::create()`, bọc try/catch \Throwable (đang trong DB::transaction).
- Endpoint `GET assign/configs/histories?company_id=` — đặt TRƯỚC route `/{companyId}`.
- Migration chờ user đồng ý mới chạy. Không backfill, không git.

## Phase 3 (2026-07-16): tab Quản lý dự án → Cấu hình mức độ ưu tiên

- Bảng riêng `priority_level_history` (GLOBAL không company_id, ĐÃ migrate) — full-snapshot per-row 4 trường (KHÔNG sort_order), 4 action create/update/delete/**reorder** (kéo thả = 1 dòng log {"order":[tên]}, priority_level_id NULL). 1 nút chung tab cạnh "Thêm dòng" → modal PriorityLevelHistoryModal.vue (badge tên dòng, swatch mã màu). Endpoint GET assign/priority-levels/histories. Sub-tab "Cấu hình hạn" vẫn ngoài scope.

## Phase 4 (2026-07-16): sub-tab Cấu hình hạn

- 6 trường deadline (task/issue/meeting/solution_due_days + category/people_late_task_threshold) nằm trên `GeneralRegulation` (entity dùng chung — đã có 2 bảng log khác) nhưng lưu qua endpoint riêng `POST assign/my-job/deadline-config` → bảng RIÊNG `assign_deadline_config_history` (ĐÃ migrate) subset-diff trong `MyJobService::saveDeadlineConfig()`, action chỉ `update`, histories scope `current_company_role` (không query param). FE: nút light + `DeadlineConfigHistoryModal.vue`. Đã verify cách ly: không sinh log vào general_regulation_history/human_setting_history.

## Lưu ý

- ⚠️ Bug CÓ SẴN ngoài scope (đã báo): nhánh tạo mới trong `AssignConfigService::create()` thiếu gán `technical_room_double`.
- Liên quan: [[human-settings-history]] (mẫu gần nhất), skill `entity-history`.
