# Plan — Tên hồ sơ cho Hồ sơ trình duyệt

## Phase 1 — Database
- [x] Migration thêm `name` VARCHAR(255) nullable vào `solution_review_profiles` (sau `code`)
- [x] Migration thêm `name` VARCHAR(255) nullable vào `solution_module_review_profiles` (sau `code`)
- [x] Chạy migrate + verify 2 cột tồn tại (KHÔNG bọc DDL trong transaction)

## Phase 2 — Backend
- [x] `StoreSolutionReviewProfileRequest`: rule `name` required|string|max:255 + message
- [x] `StoreReviewProfileRequest` (SolutionModule): rule `name` required|string|max:255 + message
- [x] `SolutionService::storeSolutionReviewProfile`: `$payload['name']` + store return + transformSolutionReviewProfile + transformModuleReviewProfile
- [x] `SolutionModuleService::storeReviewProfile`: `$payload['name']` + store return + getSolutionModuleReviewProfiles list transform
- [x] `ProspectiveProjectService::getReviewProfiles`: transform thêm `'name'`
- [x] `php -l` các file sửa (sạch)

## Phase 3 — Frontend form
- [x] `SolutionApprovalModal.vue`: input "Tên hồ sơ*" trên Nội dung + reviewForm.name + getDefaultReviewForm + open() prefill + buildPayload + formErrors.name + import V2BaseInput
- [x] `ModuleApprovalModal.vue`: y hệt (2 luồng load open()/openWithProfile)

## Phase 4 — Frontend danh sách (cột "Tên hồ sơ")
- [x] `solutions/components/manager/ReviewProfilesTab.vue`: cột + slot cell
- [x] `solution-modules/_id/components/ReviewProfilesTab.vue`: cột + slot cell
- [x] `prospective-projects/components/ProspectiveProjectReviewProfilesTab.vue`: cột + slot cell

## Phase 5 — Verify
- [x] Tinker: validate rule name → 422 + message "Vui lòng nhập tên hồ sơ."; store thật (solution 1) persist name → list transform trả name
- [x] Playwright (NV 145 = PM solution 1): AC1 label "Tên hồ sơ *" ✓, AC2 lỗi inline "Vui lòng nhập tên hồ sơ." + không lưu ✓, AC4 cột "Tên hồ sơ" đứng sau "Mã / Nội dung hồ sơ" ✓
- [ ] (Chưa test live) Phía Hạng mục — local không có hạng mục Đã duyệt; code đối xứng solution, lint sạch

---
### Checkpoint — 2026-07-06
Vừa hoàn thành: Toàn bộ Phase 1-5. Thêm trường "Tên hồ sơ" (bắt buộc, validate BE) vào form Tạo/Sửa hồ sơ trình duyệt cấp Giải pháp + Hạng mục + cột "Tên hồ sơ" ở 3 tab danh sách. Verify BE end-to-end (solution) + Playwright AC1/AC2/AC4 PASS trên UI thật.
Đang làm dở: (không)
Bước tiếp theo: User verify browser + test phía Hạng mục khi có dữ liệu hạng mục Đã duyệt. Migration đã chạy trên local (production cần chạy 2 migration).
Blocked:
