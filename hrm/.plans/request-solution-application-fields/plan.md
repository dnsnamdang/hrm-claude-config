# Plan — request-solution-application-fields

@manhcuong · Spec: docs/superpowers/specs/2026-06-26-request-solution-application-fields-design.md

## Phase 1 — Backend ✅

- [x] Migration `request_solutions`: thêm `scope_id` (nullable, comment "Nhóm ngành"), `industry_id` (nullable, comment "Nhóm giải pháp") — KHÔNG bọc DB::transaction
- [x] Model `RequestSolution`: thêm relation `scope()` + `industry()`
- [x] `RequestSolutionRequest`: thêm rule `scope_id`/`industry_id` nullable|exists + `withValidator` kiểm tra thuộc mapping Ứng dụng của dự án (project_key)
- [x] `RequestSolutionService::store()` + `update()`: thêm `scope_id`/`industry_id` vào mảng `$data` (+ show() eager-load scope/industry)
- [x] `DetailRequestSolutionResource`: thêm `application_id`/`application_name` (derive từ project), `scope_id`/`scope_name`, `industry_id`/`industry_name`
- [x] `php artisan migrate --path=...` (chỉ migration này, tránh chạy nhầm pending khác) + verify 2 cột tồn tại (Schema::hasColumn PASS)

## Phase 2 — Frontend ✅ (code done)

- [x] `RequestSolutionForm.vue`: thêm `scope_id`/`industry_id` vào `request` + map trong `loadRequestSolution()` + truyền `:application-id="tktForm.application_id"` xuống RequestTab
- [x] `RequestTab.vue`: prop `applicationId`; computed `applicationName`/`appScopeOptions`/`appIndustryOptions` (rỗng khi không có app); 3 field UI (Ứng dụng readonly, 2 select allow-clear); mounted dispatch fetchApplications/fetchScopes/fetchIndustries; watcher clear scope/industry khi đổi app (bỏ qua lần nạp đầu oldVal rỗng)
- [x] Trang chi tiết `_id/index.vue` dùng RequestSolutionForm mode show → 3 trường tự render readonly; modal Phê duyệt mở đè (AC4)

## Phase 3 — Verify

- [x] BE tinker (project 1, app 222, scope[6]/industry[9]): persistence PASS; resource trả application_name/scope_name/industry_name + id PASS; validation valid PASS / scope ngoài app bị chặn PASS / cả 2 rỗng PASS (đã khôi phục id=1)
- [x] UI Playwright (login namdangit token-injection, project 4 app 222): AC1 Ứng dụng tự điền "Áp dụng công việc tại Tân Phát" PASS; AC2 Nhóm ngành chỉ "Đào tạo"(scope 6) PASS; AC3 Nhóm giải pháp chỉ "Dịch vụ đào tạo"(industry 9) PASS; AC4 màn chi tiết (show, = nền màn Phê duyệt) hiển thị đủ 3 trường đúng PASS (tạo bản ghi test id=3 qua tinker → verify render → đã xóa, còn 2 bản gốc)
- [~] Edge dự án không có app: KHÔNG có dữ liệu test (mọi dự án đều có app) → nhánh withValidator chỉ review code, chưa test runtime

## Checkpoint — 2026-06-26
Vừa hoàn thành: BE + FE code done + verified (tinker BE + Playwright UI AC1-4 PASS). Migration đã chạy thật. Dọn sạch bản ghi test.
Đang làm dở: không.
Bước tiếp theo: user review trên browser nếu cần; CHƯA commit/git (theo quy ước).
Blocked: không. (Nhánh "dự án không có Ứng dụng" chưa test runtime do thiếu dữ liệu — chỉ review code.)
