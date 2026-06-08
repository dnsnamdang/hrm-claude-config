# Plan — Auto-fill chỉ khi còn đúng 1 option (Dự án tiền khả thi)

**Người phụ trách:** @namdang · **Module:** Assign
File: `hrm-client/pages/assign/prospective-projects/components/ProjectInfoSection.vue`
Spec: `docs/superpowers/specs/2026-06-04-prospective-project-autofill-single-option-design.md`

## Phase 1 — FE: gom logic auto-fill về 1 method

- [x] Thêm method `autoFillSingleOptions()`: vòng lặp lan truyền, duyệt 5 field, fill field đang trống khi computed options tương ứng có đúng 1 phần tử; bọc cờ `isAutoFilling`, `$nextTick` tắt cờ; guard `MAX_CASCADE_ITERATIONS` chống lặp vô hạn
- [x] Sửa watcher `application_id`: bỏ gọi `autoFillFromApplication()`, gọi `autoFillSingleOptions()`
- [x] Sửa watcher `industry_id`: bỏ logic `industry.scope_ids[0]`, gọi `autoFillSingleOptions()`
- [x] Sửa watcher `customer_scope_group_id`: bỏ logic lĩnh vực con đầu tiên, gọi `autoFillSingleOptions()`
- [x] Sửa watcher `customer_scope_id`: bỏ logic nhóm cha đầu tiên, gọi `autoFillSingleOptions()`
- [x] Thêm watcher `scope_id`: gọi `autoFillSingleOptions()` (lan truyền khi chọn Nhóm ngành trước), giữ guard `isInitializing/isPopulating/isAutoFilling`
- [x] Xóa method `autoFillFromApplication()` (đã thay thế)
- [x] Giữ nguyên `pruneInvalidCascade()` + watcher `cascadeKey`, các computed options, logic `selectionMode`/`onSelectionModeChange`

## Phase 2 — Kiểm thử thủ công (góc nhìn người dùng cuối)

- [ ] Luồng Nhóm ngành: chọn Ứng dụng nhiều Nhóm giải pháp → để trống; 1 Nhóm giải pháp → tự fill và lan truyền lên Nhóm ngành nếu duy nhất
- [ ] Chọn tay Nhóm ngành trước → chọn Ứng dụng → Nhóm ngành không bị ghi đè
- [ ] Luồng Lĩnh vực KH: chọn Lĩnh vực thuộc nhiều nhóm → để trống Nhóm LVKH; thuộc 1 nhóm → tự fill
- [ ] Đổi qua lại lựa chọn → field không hợp lệ bị xóa, không kẹt giá trị sai
- [ ] Màn xem (isShow) / dự án đã duyệt → không auto-fill
