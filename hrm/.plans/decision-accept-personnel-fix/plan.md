# Plan — Fix màn Quyết định tiếp nhận nhân sự (accept-personnel edit)

Phụ trách: @namdangit

## Bối cảnh
Màn `/decision/accept-personnel/{id}/edit`:
- API `all-employee-infos-accept` chậm (đo: 1.87s / 1.8MB / 389 record) + bị gọi 2 lần.
- Đổi "Người được tiếp nhận" ở edit không load lại các ô input.

## Root cause
- BE: N+1 trong `EmployeeInfoAcceptResource` — dòng 24 query `GeneralRegulation` mỗi record; dòng 25 `$rank->group` không eager-load.
- FE: `mounted()` + watch `immediate` cùng gọi `getEmployeeInfoAccept()` → 2 request.
- FE: `setEmployeeInfo` chỉ `Object.assign` khi `!route.params.id` → edit đổi người không cập nhật.

## Phase 1 — Fix

### BE
- [x] `AcceptPersonnelController::getAllEmployeeInfoAccept`: eager-load thêm `workPosition.ranks.group`; fetch GeneralRegulation 1 lần inject vào resource
- [x] `EmployeeInfoAcceptResource`: dùng `static::$generalRegulation` (set từ controller) thay query per-record; gỡ import thừa
- [x] `Competency::getBaseSalaryAttribute` (model dùng chung, ĐÃ XIN PHÉP): memo GeneralRegulation theo request → bỏ ~4900 query

### FE (FormComponent.vue)
- [x] `getEmployeeInfoAccept`: memo hoá promise → chống gọi trùng (mounted + watch dùng chung 1 request)
- [x] `data()`: thêm `employeeInfoAcceptPromise: null`
- [x] watch `recipient_employee_info_id`: truyền `isUserChange` (dựa oldVal !== undefined)
- [x] `setEmployeeInfo`: edit + user đổi người → `Object.assign` autofill (loại `id`,`text`); create giữ nguyên hành vi cũ
- [x] Test (Playwright + curl): 1 request (từ 2), 1.87s×2 → ~0.7s×1; đổi người ở edit các ô cập nhật đúng

## Kết quả đo
- Query transform: 5948 → 1003 (bỏ ~4945 query general_regulations)
- Số lần gọi API: 2 → 1
- Thời gian: ~1.87s×2 (≈3.7s) → ~0.7s×1
- Còn lại (tuỳ chọn): 778 query từ helper dùng chung `Helper::getCurrentSeniorityMonths` (master_settings + suspend_labor_contracts per-record)

## Checkpoint — 2026-07-01
Vừa hoàn thành: fix N+1 (transformer + Competency memo) + bỏ gọi trùng + fix reload input khi đổi người; test Playwright pass
Đang làm dở: không
Bước tiếp theo: (tuỳ chọn) tối ưu N+1 trong getCurrentSeniorityMonths nếu muốn nhanh hơn nữa
Blocked:
