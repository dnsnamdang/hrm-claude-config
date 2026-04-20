# Plan: Cấu hình chặn luồng quá hạn — Tab 2 chặn TP + Lịch sử chỉnh sửa

## Trạng thái
- Bắt đầu: 2026-04-20
- Tiến độ: chưa bắt đầu

## Phase 1: DB + Seed + UI config
- [ ] Task 1: Migration thêm cột `tab` vào `due_configs`
- [ ] Task 2: Migration tạo bảng `due_config_histories`
- [ ] Task 3: Seed 30 records tab=2 (danh sách phiếu duyệt theo spec)
- [ ] Task 4: Model `DueConfigHistory` + update `DueConfigs` model
- [ ] Task 5: View `edit.blade.php` — thêm Tab 2 + bảng lịch sử
- [ ] Task 6: Controller `update()` — ghi log lịch sử

## Phase 2: Logic chặn TP
- [ ] Task 7: Service `DueConfigBlockService::isManagerBlocked()`
- [ ] Task 8: API endpoint `check-manager-block` cho HRM gọi

## Phase 3: Hook routes
- [ ] Task 9: Middleware `checkDueConfigsManager` cho routes ERP
- [ ] Task 10: HRM (hrm-api) gọi API ERP trước khi approve

## Checkpoint
(chưa có)
