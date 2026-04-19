# Design: "Lưu và duyệt" khi giải pháp không có hạng mục

## Bối cảnh

Ở trạng thái `CHO_PM_DUYET (3)`, hiện tại luôn hiện button "Giao cho Leader". Yêu cầu: khi `has_modules = false`, hiện button "Lưu và duyệt" và chuyển thẳng sang `DANG_TRIEN_KHAI (7)`.

## Luồng

```
CHO_PM_DUYET (3)
  ├── has_modules = true  → "Giao cho Leader"  → CHO_LEADER_DUYET (5) [giữ nguyên]
  └── has_modules = false → "Lưu và duyệt"     → DANG_TRIEN_KHAI (7) + set start_date
```

## Thay đổi

### Frontend (`pages/assign/solutions/_id/edit.vue`)
- `submitButtonText`: khi status = CHO_PM_DUYET và has_modules = false → "Lưu và duyệt"
- `nextStatus`: khi status = CHO_PM_DUYET và has_modules = false → DANG_TRIEN_KHAI (7)
- Validation hạng mục chỉ chạy khi has_modules = true (đã đúng sẵn)

### Backend (`Modules/Assign/Services/SolutionService.php`)
- Thêm case: CHO_PM_DUYET → DANG_TRIEN_KHAI khi has_modules = false → cho phép, set start_date cho version hiện tại

## Không thay đổi
- Luồng có hạng mục giữ nguyên
- Không thêm trạng thái mới
- Không đổi permission/canEdit
