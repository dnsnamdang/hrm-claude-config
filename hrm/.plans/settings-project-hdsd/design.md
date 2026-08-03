# Design — HDSD tab "Quản lý dự án" màn Cấu hình chung (/assign/settings)

## Mục tiêu
HDSD Word cho 2 tab con trong tab "Quản lý dự án" của màn "Cấu hình chung" (title: Cấu hình phân hệ giao việc): Cấu hình mức độ ưu tiên + Cấu hình hạn.

## Hiện trạng (khảo sát 03/07/2026)
- FE: `hrm-client/pages/assign/settings/index.vue` (2044 dòng). Menu "Cấu hình" > "Cấu hình chung", `isShow: ['Cấu hình phân hệ giao việc/ công tác']`. 3 tab cấp 1; tab "Quản lý dự án" (dòng ~768-1217) có 2 tab con, LƯU ĐỘC LẬP (khác 2 tab đầu dùng submitSave chung).
- **Mức độ ưu tiên**: bảng `priority_levels` (KHÔNG seeder — rỗng ban đầu; không lọc company → GLOBAL). API `assign/priority-levels` (index/getAll/store/update/destroy/bulk-update-sort-order), KHÔNG checkPermission (chỉ auth:api). Inline edit theo dòng (view/edit/new + snapshot + "Chưa lưu"), kéo thả vuedraggable đổi sort_order. Validate FE: name required ≤20, days required ≥0, hours 0-23, color #RRGGBB; BE PriorityLevelStoreRequest: name unique. Xóa chặn bởi isCanDelete (!projectPhases exists) → "Dữ liệu đang được sử dụng, vui lòng tải lại".
- **Tiêu thụ priority**: project_phase_modal (dropdown "Mức độ ưu tiên" BẮT BUỘC, options getAll theo sort_order); RequestSolutionService::calculateNeedReceiveDate (hạn tiếp nhận = sent_date + response_days + response_hours, bỏ ngày lễ, days=0 → null, KHÔNG hồi tố); filter priority_level_id ở Solution/MyJob.
- **Cấu hình hạn**: 6 field lưu vào `general_regulations` THEO company_id (updateOrCreate; task/issue/meeting/solution_due_days + category/people_late_task_threshold, default 0). API `assign/my-job/deadline-config` GET/POST, KHÔNG validate FE+BE. Tiêu thụ: MyJobService (Sắp tới hạn [now, now+N ngày] + thông báo), SolutionService::getCategoriesWithLateTasks + SolutionModuleService (task trễ ≥ max(threshold,1)).
- Edge: API không kiểm quyền (chỉ menu FE chặn); ưu tiên global vs hạn theo công ty; không có "tắt mềm" ưu tiên.

## Cách dựng
1 agent Opus đọc đủ luồng; Playwright chụp 6 ảnh dev-hrm namdangit (thao tác Sửa đều Huỷ, dòng thêm mới đã xóa — không đổi dữ liệu). Generator `gen_settings_project.py` + hdsd_lib.

## Output
- `HDSD_luongchinh/HDSD_CauHinhQuanLyDuAn.docx` — 6 Heading 1 (TỔNG QUAN + PHẦN 1-3), 6 hình, 4 bảng, ~0.5MB, broken=0.
- Ảnh: `hdsd_settings_project_shots/`.
