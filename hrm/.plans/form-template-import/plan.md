# Plan — Import nội dung mẫu khảo sát từ Excel (#10548)

Feature: `form-template-import` · Owner: @junfoke · Nhánh: `tpe` (hrm-api + hrm-client)
Spec: `docs/superpowers/specs/2026-08-27-form-template-import-design.md`

## Phase 1 — Backend: resolve-or-create + store pre-pass ✅
- [x] 1.1 `SurveyQuestionService::resolveOrCreate()` + `findDuplicateId()` (read-only, dùng chung) + `normalizeAnswerKey`.
- [x] 1.2 `FormTemplateService::resolveImportedQuestions()` + `resolveImportedQuestionList()` (đệ quy, gán libraryId+code).
- [x] 1.3 `store()` gọi pre-pass; guard scope=2 thiếu application_id → throw Exception (store bắt → 400 kèm message).
- [x] 1.4 Câu hỏi thư viện (có libraryId) đi đường cũ; `findInvalidSurveyQuestionMessage` bỏ qua câu _import (không code). php -l sạch.

## Phase 2 — Backend: validate + template endpoints ✅
- [x] 2.1 `FormTemplateController::validateImport()` — validate từng row + dedup preview (willReuse/reuseId).
- [x] 2.2 `FormTemplateController::importTemplate()` + `applyListValidation()` — PhpSpreadsheet, 6 cột + dropdown C/D/F + 3 dòng ví dụ.
- [x] 2.3 Routes `/import-template` (GET) + `/import/validate` (POST) đặt trước `/{formTemplate}`, cùng middleware permission.

## Phase 3 — Frontend: modal import + tích hợp builder ✅
- [x] 3.1 `FormMeta.vue`: nút "Import Excel" cạnh Ứng dụng, disable khi chưa chọn application + hint; emit `open-import`.
- [x] 3.2 `FormBuilder.vue`: chứa `<V2BaseImportModal>`; mở modal khi nhận `open-import` (guard chọn Ứng dụng).
- [x] 3.3 `importColumns` (6 cột) + `requiredFields` + `importValidationRules` (client, dự phòng) + map nhãn→mã (DATA_TYPE_BY_LABEL, BUILDER_TYPE_BY_DATA_TYPE). Quyết định: yêu cầu Tên Section mọi dòng.
- [x] 3.4 `handleValidateImportData` → POST `assign/form-templates/import/validate` → cập nhật modal (rows/validCount/step 3), lỗi theo dòng qua getImportValidationMessage.
- [x] 3.5 `handleImportQuestions` → transform dòng hợp lệ → câu hỏi builder có `_import` → gom theo Section → **APPEND** vào sections + hide modal + toast.
- [x] 3.6 `handleDownloadImportTemplate` → tải blob `assign/form-templates/import-template` (giữ đúng đuôi .xlsx).

## Phase 4 — Verify (Playwright localhost:3000 + DB + API) ✅ PASS (2026-08-27, data thật)
- [x] 4.1 Tải template: HTTP 200, xlsx hợp lệ, sheet=Data, 6 cột + 3 dòng ví dụ.
- [x] 4.2 Import file (2 section, 4 câu) → preview đúng 6 cột → Validate 4/4 hợp lệ → Import nạp vào builder (Section A/B) → Lưu (PTT-2026-00001) → DB: 3 survey_questions + 4 form_questions link đúng survey_question_id + code=cau_hoi_{id}, required/type/answers đúng.
- [x] 4.3 Câu "Tên công ty là gì?" trùng 2 lần (Tất cả) trong cùng file → chỉ tạo 1 sq (id=1), cả 2 form_question link id=1 (dedup idempotent). API preview willReuse=true reuseId=1.
- [x] 4.4 App khác (app=3) câu radio trùng → willReuse=false (tạo mới); cùng app=2 → willReuse=true reuseId=2.
- [x] 4.5 File lỗi (loại sai / radio thiếu đáp án) → validate trả isValid=false + errors kèm "row" (số dòng Excel).
- [x] 4.6 Chưa chọn Ứng dụng → nút Import disable + hint. Alignment nút đã sửa (thêm nhãn spacer, thẳng hàng ô select).
- [x] Dọn data test: DB trả về trống (0 sq, 0 ft).

---

### Checkpoint — 2026-08-27
Vừa hoàn thành: Phase 1+2 (BE) + Phase 3 (FE) — code xong toàn bộ luồng import.
- BE: `SurveyQuestionService::resolveOrCreate/findDuplicateId/normalizeAnswerKey`; `FormTemplateService::resolveImportedQuestions/resolveImportedQuestionList` + gọi trong `store()`; `FormTemplateController::validateImport/importTemplate/applyListValidation`; 2 route. php -l sạch.
- FE: `FormMeta.vue` nút Import (disable khi chưa chọn Ứng dụng); `FormBuilder.vue` tích hợp V2BaseImportModal + importColumns + handlers (validate BE + append builder + tải template blob). JS parse rough OK.
Đang làm dở: —
Bước tiếp theo: Phase 4 — verify E2E (cần user bật `php artisan serve` cho hrm-api + `npm run dev` hrm-client, hoặc Claude tự bật) → tải template, import file, Lưu, kiểm DB dedup. Chưa commit git.
Blocked: Verify E2E cần server chạy.

### Checkpoint — 2026-08-27 (rename scope label)
Vừa hoàn thành: đổi nhãn phạm vi "Theo nhóm giải pháp" → **"Theo ứng dụng"** cho nhất quán (hệ thống đã bỏ nhóm giải pháp, xử lý theo Ứng dụng).
- BE: template dropdown F + dòng ví dụ + message guard (Controller) + message store (Service).
- FE: FormBuilder message validate; **vẫn nhận alias "theo nhóm giải pháp"** để file cũ không vỡ.
- Docs: spec + design cập nhật. php -l sạch, FE parse OK.
Lưu ý: API dev 8000 đã tắt lúc kiểm lại nên chưa re-hit endpoint sau đổi nhãn — thay đổi chỉ là swap chuỗi trong đúng luồng đã verify đầy đủ trước đó.
Bước tiếp: (tuỳ chọn) user bật lại `php artisan serve` → tải lại template xem dropdown "Theo ứng dụng". Chưa commit git.

## Phase 5 — Fix bug #11285 (nhánh task_10548, merge vào tpe-develop-assign sau)
- [x] 5.1 Bug 1 — Bỏ dòng ghi chú dưới nút Import + căn nút thẳng ô Ứng dụng (FormMeta.vue). Nhãn spacer text-only render cao 14px (khác nhãn thật 18px) → nút lệch lên 27px. Fix đúng: nhân bản NHÃN THẬT `<V2BaseLabel text="Ứng dụng" :required>` bọc `visibility:hidden` (giữ chỗ). Verify pixel trên build task_10548 (dev riêng cổng 62215): button_top=select_top=166, button_bottom=select_bottom=198, diff=0. ✅ CĂN CHUẨN.
- [x] 5.2 Bug 2a — Đổi tiêu đề popup → "Import form thu thập thông tin" (FormBuilder.vue).
- [x] 5.2 Bug 2b — Cột STT bảng preview từ 1: **sửa đúng pattern BOM** — `V2BaseImportModal.handleLoadExcel` gán lại `__row = idx+1` sau parseExcelFile (giống BomImportModal:742). ĐÃ HOÀN TÁC sửa V2BaseImportTable (giữ nguyên hiển thị `__row`). Nay `__row` nhất quán cả cột STT lẫn thông báo, và mọi màn dùng V2BaseImportModal đều 1-based như BOM.
- [x] 5.3 Bug 3 — Không nhập "Bắt buộc" vẫn qua: FE gửi thêm `required_label`, BE validateImport check ∈ {Có,Không}.
- [x] 5.4 Bug 4 — 2 dòng y hệt nhau không báo trùng: BE validateImport thêm chống trùng chữ ký cả dòng (Section+Nội dung+Loại+Bắt buộc+Phạm vi+Đáp án) → dòng sau báo "Trùng với dòng X".
- [x] 5.5 Đồng bộ rename "Theo nhóm giải pháp" → "Theo ứng dụng" trên nhánh task_10548 (template dropdown/ví dụ, message Controller + Service, message FE). php -l sạch, FE parse OK.
- [x] 5.6 Verify API (task_10548, port 8000): bug3 báo lỗi Bắt buộc, bug4 báo "Trùng với dòng 2", template dropdown "Tất cả, Theo ứng dụng".
- [x] 5.8 Bug 5 (#11285 bổ sung) — **Import lần 2 cùng file vào cùng form vẫn thành công → lặp Section/câu hỏi**. Nguyên nhân: validate chỉ chặn trùng TRONG 1 file, chưa đối chiếu câu hỏi ĐÃ CÓ trong biểu mẫu. Fix FE `FormBuilder.vue`: thêm `buildQuestionKey()` (4 yếu tố) + `existingQuestionKeys()` (quét sections/groups/children, lấy data_type từ `_import` hoặc map ngược `DATA_TYPE_BY_BUILDER_TYPE`, có biến thể không kèm phạm vi để bắt câu kéo từ thư viện); `handleValidateImportData` gắn lỗi "Câu hỏi này đã có trong biểu mẫu" và tự tính lại validCount/invalidCount.
  Verify E2E bằng **stack riêng** (API 8010 + client 3006 từ task_10548, vì 8000/3000 của user là project khác), file thật của user: lần 1 import OK (Section A+B); lần 2 cùng file → Tổng 3/**Hợp lệ 0/Lỗi 3**, mỗi dòng báo trùng, nút Import khoá; biểu mẫu vẫn chỉ A+B, không lặp. ✅
- [x] 5.7 Verify UI Playwright (2026-09-04, data thật): Bug 1 nút thẳng hàng + không còn ghi chú; Bug 2a tiêu đề "Import form thu thập thông tin"; Bug 2b STT 1/2/3/4; Bug 3 dòng thiếu Bắt buộc báo "Bắt buộc chỉ nhận: Có / Không"; Bug 4 dòng trùng báo "Trùng với dòng 3...". Summary Tổng 4/Hợp lệ 2/Lỗi 2. ✅ TẤT CẢ PASS.

### Checkpoint — 2026-08-27 (testcase QA)
Vừa hoàn thành: xuất testcase Excel cho chức năng Import (`.plans/form-template-import/testcase.xlsx`, generator `gen_testcase.py`).
36 TC (P0 56%), ngôn ngữ nghiệp vụ (bộ kiểm tra thuật ngữ = OK-sạch). 9 nhóm: Phân quyền + I Hiển thị/truy cập, II Tải file mẫu, III Chọn & đọc file, IV Kiểm tra dữ liệu (validate), V Nạp vào biểu mẫu, VI Lưu & chống trùng (đủ 3 case dedup), VII Ràng buộc nhập liệu, VIII Luồng đầu-cuối.
