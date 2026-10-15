# Plan — decision-appendix-print-template (#10894)

Spec: [2026-10-09-decision-appendix-print-template-design.md](../../../docs/superpowers/specs/gop-db/2026-10-09-decision-appendix-print-template-design.md)
Nhánh: `gop_db` (worktree `hrm-api/.worktrees/gop-db`, `hrm-client/.worktrees/gop-db`). Không commit.

## Phase 1 — DB + API mẫu in
- [x] Migration `2026_10_09_000001` `hrm_print_templates.appendix_decision_type` (đã chạy DB local)
- [x] Migration `2026_10_09_000002` `decisions.appendix_print_template_id` + `appendix_print_template` (đã chạy DB local)
- [x] `PrintTemplate` fillable; `PrintTemplateRequest` rule `nullable|in:<4 key AppendixLaborContract::DECISION_TYPE>`;
      `PrintTemplateService` lọc + ép null khi không phải mẫu PLHĐ
- [x] `referencingTables()` cho phép nhiều cột/bảng: `decisions` => `print_template_id`, `appendix_print_template_id`

## Phase 2 — API QĐ
- [x] `DecisionService::updateOrCreate` ghi 2 cột; `DetailDecisionResource` trả 2 field
- [x] 2 hàm autogenous lấy mẫu từ QĐ (bỏ tra code `PHU_LUC_HOP_DONG_LAO_DONG`); thâm niên `updateOrCreate(id_decision, employee_id)`
- [x] 4 controller `toggleApprove`: chặn 422 trước `DB::transaction` khi thiếu mẫu + gọi lại autogenous
      (`AppendixLaborContract::isMissingDecisionPrintTemplate` + `MSG_MISSING_DECISION_PRINT_TEMPLATE`)

## Phase 3 — FE
- [x] `pages/decision/utils/constants.js`: `APPENDIX_DECISION_TYPE_OPTIONS`, `PRINT_TEMPLATE_TYPE_LABOR_CONTRACT`, `PRINT_TEMPLATE_SUB_TYPE_APPENDIX`
- [x] Danh mục mẫu in `add.vue` + `_id/edit.vue`: trường "PLHĐ của quyết định"; `index.vue`: bộ lọc
- [x] Component mới `pages/decision/components/FormAppendixPrintTemplateComponent.vue`
- [x] Tab "Mẫu in PLHĐ" + validate ở `components/FormComponent.vue` của 4 loại QĐ
- [x] Màn duyệt 4 loại (`_id/approve.vue`): lỗi 422 hiện đúng câu API trả về; lỗi khác vẫn "Thao tác thất bại"

## Phase 4 — Verify
- [x] `php -l` sạch; migrate local (chỉ 2 file, `--path`)
- [x] Tinker trong transaction + rollback — thiếu mẫu: 422, trạng thái giữ 3, không sinh PLHĐ; có mẫu: 200, trạng thái 5,
      PLHĐ có `print_template` đúng nội dung QĐ — đạt cho điều chỉnh lương / điều chuyển / bổ nhiệm.
      Tăng lương thâm niên: DB local không có QĐ nào → chưa chạy.
- [x] Tinker API mẫu in: rule nhận 4 loại / chặn loại khác; đổi sang HĐLĐ chính → null; lọc đúng; mẫu QĐ đang chọn → không xoá được (`in_use`)
- [x] Parse 9 file `.vue` + constants (vue-template-compiler + babel): sạch
- [ ] Playwright xem ảnh — bị chặn quyền (không cho tạo/chuyển token đăng nhập sang cổng 3100). Server worktree đang chạy: API :8100, Nuxt :3100

## Checkpoint — 2026-10-09
- Vừa hoàn thành: Phase 1-3 + verify BE.
- Đang làm dở: verify FE trên trình duyệt.
- Bước tiếp theo: user đăng nhập http://127.0.0.1:3100 xem tab / danh mục; chốt việc hiện câu báo lỗi ở màn duyệt; báo HR gắn loại QĐ cho mẫu PLHĐ 17/46.
- Blocked: quyền Playwright đăng nhập.
- Mã PLHĐ sinh bằng `count + 1` → có PLHĐ bị xoá là trùng mã: **chủ ý của PM, không sửa** (user chốt 09/10).

## Phase 5 — Sửa lỗi mất phụ cấp/hỗ trợ "trước thay đổi" của PLHĐ (09/10/2026, user đồng ý)
- [x] `storeRelationAppendixLaborContract`: câu xoá thêm `->where('old_or_new', $type)` (lỗi từ commit `26fded9a2`,
      11/09/2025 — xoá toàn bộ support mỗi lần gọi, mà luôn gọi OLD rồi NEW → mất OLD). Áp cho tạo tay / sửa tay / tự sinh.
- [x] Verify tinker + rollback: duyệt QĐ điều chỉnh lương có OLD 3 / NEW 4 → PLHĐ OLD 3 / NEW 4; ghi lại lần 2 vẫn 3/4
      (không nhân đôi); `old_total_100` có giá trị.
- Dữ liệu cũ: DB local 63/63 PLHĐ tạo từ 11/09/2025 có 0 dòng OLD (trước đó 347/349 có). Cả 63 gắn QĐ → khôi phục được
  từ QĐ gốc; **chưa làm** — để khi HR bắt đầu dùng biến "trước thay đổi" (user chốt). Cần báo anh Cường.
