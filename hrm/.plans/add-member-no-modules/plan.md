# Plan — Add Member Modal hỗ trợ no-modules

## Phase 1 — BE ✅ DONE 2026-05-22

- [x] Sửa `AddMemberRequest`: `solution_module_id` từ `required|integer` → `nullable|integer`
- [x] Sửa `SolutionService::addMember`: wrap `DB::transaction`, rẽ nhánh theo `$solution->has_modules`
  - [x] Nhánh has_modules=true: validate module thuộc solution + check trùng + insert `solution_module_members`
  - [x] Nhánh has_modules=false: check trùng `member_id` trong `solution_members` + insert
  - [x] Return payload tương ứng (`solution_module_id` = null khi no-modules)
- [x] Sửa `SolutionController::addMember`: catch `ValidationException` → `responseUnprocessableEntity($message, $errors)`, giữ catch `\Exception` cho lỗi khác

## Phase 2 — FE ✅ DONE 2026-05-22

- [x] Title modal động theo `solution.has_modules`
- [x] Bọc block field "Hạng mục" trong `v-if="solution.has_modules"`
- [x] `openAddMemberModal`: chỉ gọi `loadModules()` khi `has_modules`
- [x] Computed `availableMembersOptions`: thêm nhánh `!has_modules` filter theo `humanResourcesFromApi` toàn solution
- [x] Field "Thành viên": placeholder + `disabled` phụ thuộc `has_modules`
- [x] `submitAddMember`: không gửi `solution_module_id` khi `!has_modules`

### Checkpoint — 2026-05-22
Vừa hoàn thành: Phase 1 BE + Phase 2 FE, đã spec-review PASS cả 2.
Đang làm dở: —
Bước tiếp theo: user test 9 case (spec section 6).
Blocked: —

## Phase 3 — Fix bug footer modal ✅ DONE 2026-07-03

- [x] Fix modal `add-member-modal` (HumanResourceTab.vue): nút "Thêm nhân sự"/"Huỷ" đặt trong slot `#modal-footer` nhưng modal có `hide-footer` → footer không render, popup không có nút. Chuyển 2 nút thành `<div class="modal-footer">` trong body theo skill modal-popup.

## Phase 4 — Test

- [ ] Test solution has_modules=true: flow cũ vẫn hoạt động (chọn hạng mục → chọn thành viên → submit)
- [ ] Test solution has_modules=false: modal không có field hạng mục, chọn thành viên trực tiếp, submit OK, hiển thị trong tree + table
- [ ] Test trùng nhân sự (no-modules): hiện lỗi inline `member_id`
- [ ] Test validate ngày bắt đầu < hôm nay
