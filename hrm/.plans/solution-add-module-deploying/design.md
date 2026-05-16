# Design: Thêm hạng mục khi đang triển khai

## Bối cảnh

Ở trạng thái DANG_TRIEN_KHAI (7), modules bị disabled. Yêu cầu: PM có thể thêm hạng mục mới và bấm "Lưu và duyệt" để auto-approve hạng mục mới.

## UI

Ở DANG_TRIEN_KHAI, hiện 2 button song song:
- "Tạo hồ sơ trình duyệt giải pháp" — giữ nguyên
- "Lưu và duyệt" — lưu + auto-approve hạng mục mới

## Thay đổi

### Frontend
- `edit.vue`: Thêm button "Lưu và duyệt" khi status = DANG_TRIEN_KHAI
- `ModulesTab.vue`: Cho phép PM thêm hạng mục mới khi DANG_TRIEN_KHAI

### Backend
- `SolutionService.php`: Khi update ở DANG_TRIEN_KHAI, sau syncModules → set các module mới (status=CHUA_DUYET) thành DA_DUYET + approved_at = today

## Không thay đổi
- Logic "Tạo hồ sơ trình duyệt giải pháp" giữ nguyên
- Hạng mục cũ giữ nguyên status
