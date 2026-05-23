# Add Member Modal — hỗ trợ Solution không có hạng mục

## Mục tiêu

Sửa popup "Thêm nhân sự" trong `HumanResourceTab.vue` để xử lý đúng cả 2 case: solution có hạng mục (`has_modules = true`) và không có hạng mục (`has_modules = false`).

## Hiện trạng (bug)

- FE: popup luôn render field "Hạng mục" + disable "Thành viên" cho đến khi chọn hạng mục → khi solution không có hạng mục, user không thể thêm nhân sự.
- BE: `POST assign/solutions/{id}/manager/members` (SolutionController:475 + AddMemberRequest + SolutionService:2322) bắt buộc `solution_module_id`, chỉ ghi vào `solution_module_members`. Không xử lý case `has_modules = false`.
- BE đã có sẵn bảng `solution_members` (migration 2026_04_02_000002) và relationship `Solution::members()` dùng trong `getHumanResources` nhánh `!has_modules` để hiển thị → chỉ thiếu luồng ghi.

## Quyết định

- FE: ẩn hoàn toàn field "Hạng mục" khi `!has_modules`, đổi title modal, cho chọn "Thành viên" ngay, lọc trùng theo toàn solution.
- BE: route POST dùng chung 1 endpoint; service rẽ nhánh theo `solution->has_modules`:
  - Có module → giữ logic cũ, ghi `solution_module_members`.
  - Không module → ghi `solution_members` (đã có sẵn schema đủ cột).
- Validation: `solution_module_id` đổi thành `nullable`; ràng buộc cứng + check trùng `member_id` xử lý trong service, throw `ValidationException`.
- Không cần migration.

## Scope

- FE: `hrm-client/pages/assign/solutions/components/manager/HumanResourceTab.vue`
- BE: `Modules/Assign/Http/Requests/Solution/AddMemberRequest.php`, `Modules/Assign/Services/SolutionService.php` (method `addMember`), `Modules/Assign/Http/Controllers/Api/V1/SolutionController.php` (method `addMember` — rethrow ValidationException).

## Không thuộc scope

- Sửa luồng xoá / sửa nhân sự đã thêm.
- Sửa endpoint `SolutionModuleController::addMember` (route `/solutions/{id}/modules/{module}/members`).
- Sửa UI tree / bảng hiển thị (đã chạy đúng cho cả 2 case).

Spec chi tiết: `docs/superpowers/specs/2026-05-22-add-member-no-modules-design.md`
