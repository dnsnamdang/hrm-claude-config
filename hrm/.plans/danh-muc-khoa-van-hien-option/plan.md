# Plan — Danh mục bị khoá vẫn hiện ở bản ghi đang dùng

## Phase 1 — Giai đoạn dự án (màn dự án tiềm năng)
### BE
- [x] `ProjectPhaseService::getAll` nhận `include_ids` → `where(status=ACTIVE) orWhereIn('id', $includeIds)`

### FE
- [x] `store/optionsSelect.js`: `fetchProjectPhases({ includeIds })` — refetch khi id đang dùng thiếu trong cache, merge options, giữ nguyên tên gốc + cờ `is_locked` (không thêm hậu tố)
- [x] `ProgressFinanceSection.vue`: truyền `includeIds` khi load; watcher `project_phase_id` nạp lại nếu id không có trong options

### Khác
- [x] Thêm quy tắc chung vào `CLAUDE.md` (mục Nguyên tắc chung)

## Phase 2 — 🔒 ở ô đã chọn + chỉ hiện danh mục khoá khi đang dùng (2026-08-20)
### FE
- [x] `utils/select2LockedOption.js`: gắn 🔒 cả `templateSelection` (ô/chip giá trị đã chọn); thêm `filterUnusedLockedOptions` (ẩn option khoá không được dùng) + `mergeLockedOptions`
- [x] `V2BaseSelect` / `V2BaseSelectInModal`: lọc options qua `filterUnusedLockedOptions` trước khi render
- [x] `DescriptionInfoSelect.vue`: tự gắn 🔒 ở `templateSelection` (wrapper có `templateResult` riêng)
- [x] `store/optionsSelect.js`: `fetchProjectPhases` chỉ cache giai đoạn CÒN HOẠT ĐỘNG (bỏ merge), trả về danh sách đầy đủ cho màn dùng
- [x] Thêm `utils/mixins/projectPhaseOptionsMixin.js` (`projectPhaseOptions` + `loadProjectPhaseOptions`)
- [x] Áp mixin: prospective-projects (add/edit qua `ProgressFinanceSection`, index), solutions/index, quotations (index + _id/edit), request-solution (index, pending, RequestTab), my-job/SolutionUpcomingModal
- [x] Dùng giá trị trả về của action: report/meeting-by-projects, report/prospective-projects
- [x] `meeting/index.vue`: bộ lọc Loại meeting gửi `include_ids` theo giá trị đang lọc

### Khác
- [x] Cập nhật `.claude/skills/select-and-input-state/SKILL.md` mục 1 + `CLAUDE.md` (quy tắc 🔒 và cấm cache danh mục khoá vào store)

## Phase 3 — Phản hồi QA Redmine #11063 (2026-09-16, nhánh tpe)
### Kiểm chứng lại 4 điểm QA nêu
- [x] Điểm 2 (Xem chi tiết có 🔒) — đã đúng, không phải sửa
- [x] Điểm 3 (dropdown Giai đoạn dự án có 🔒) — đã đúng, không phải sửa
- [x] Điểm 4 (đổi giai đoạn xong vẫn thấy giai đoạn khoá cũ) — không tái hiện, option biến mất ngay
- Cả 3 điểm do commit `d1dc896c5` (2026-08-20) xử lý, đúng ngày QA phản hồi → QA test bản chưa có

### Điểm 1 — message lỗi khi Lưu (CÓ THẬT, đã sửa)
- [x] `utils/helpers.js`: thêm `SAVE_CONFLICT_MESSAGE`, `saveErrorMessage()`, `hasVisibleFieldError()`
- [x] `prospective-projects/_id/edit.vue`: bỏ message cứng, phân loại lỗi + cuộn tới ô lỗi
- [x] `prospective-projects/_id/index.vue`: như trên
- [x] Test: 422 có ô đỏ → "Bạn chưa nhập đầy đủ thông tin" + cuộn; 422 lỗi trường ẩn → "Dữ liệu đã thay đổi, vui lòng tải lại"; 404 → như trên; 403 → "Bạn không có quyền..."; 423 → message BE
- [ ] `prospective-projects/add.vue` chưa đồng bộ (đã xử lý riêng, thiếu nhánh 404 + 422-không-ô-đỏ) — chờ user chốt

### Checkpoint — 2026-09-16
Vừa hoàn thành: fix điểm 1 + kiểm chứng 3 điểm còn lại
Bước tiếp theo: user chốt có đồng bộ add.vue không; phản hồi lại QA về 3 điểm không tái hiện
Blocked:

## Redmine #11063 phản hồi #8 (16/10/2026, nhánh develop) — cache giai đoạn dự án cũ
- [x] `optionsSelect/fetchProjectPhases` nhận `force: true` bỏ qua cache; `projectPhaseOptionsMixin.loadProjectPhaseOptions(ids, { force })`
- [x] Form dự án TKT (`ProgressFinanceSection`) luôn nạp lại giai đoạn → BUG 1 (giai đoạn khoá sau khi cache nạp không có 🔒) + BUG 2 (mở khoá xong dropdown không hiện lại)
- [x] Màn danh mục Giai đoạn dự án: Khoá / Mở khoá / Xoá xong thì xoá cache store
- [x] Test Playwright local 16/10: mở form Sửa DA 155 (GĐ3) → khoá GĐ3 + mở khoá GĐ16 qua API → điều hướng trong app quay lại form: ô hiện `🔒 3.Chọn giải pháp…`, dropdown có lại GĐ16. Đã trả trạng thái GĐ3/GĐ16. Ảnh test-11063/
