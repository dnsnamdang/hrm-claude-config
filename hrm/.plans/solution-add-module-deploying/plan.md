# Plan: Thêm hạng mục khi đang triển khai

## Trạng thái
- Bắt đầu: 2026-04-07
- Tiến độ: 3/3 task ✅

## Phase 1: Cho phép PM thêm hạng mục + auto-approve (DONE)

### FE — ModulesTab
- [x] Task 1: Sửa `isManager` cho phép PM quản lý hạng mục khi DANG_TRIEN_KHAI + `isModuleDisabled` chỉ disable module cũ (có id), module mới cho sửa + button xoá chỉ hiện khi module không disabled

### FE — Button "Lưu và duyệt"
- [x] Task 2: Thêm button "Lưu và duyệt" song song với button hiện tại trong `edit.vue` khi status = DANG_TRIEN_KHAI + method `submitFormSaveAndApprove` gửi flag `auto_approve_new_modules`

### BE — Auto-approve hạng mục mới
- [x] Task 3: Trong `SolutionService.php`, sau syncModules khi DANG_TRIEN_KHAI + flag `auto_approve_new_modules` → set module có status=CHUA_DUYET thành DA_DUYET + approved_at = today

## Checkpoint

### Checkpoint — 2026-04-07
Vừa hoàn thành: Implement xong 3/3 task
- FE: `ModulesTab.vue` — isManager, isModuleDisabled, button xoá
- FE: `edit.vue` — button "Lưu và duyệt" + method submitFormSaveAndApprove
- BE: `SolutionService.php` — auto-approve modules mới khi có flag
Đang làm dở: không
Bước tiếp theo: Test thủ công
Blocked: không
