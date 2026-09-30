# Design (tóm tắt) — Import nội dung mẫu khảo sát từ Excel

- **Feature**: `form-template-import` · **Owner**: @junfoke · **Redmine**: #10548 · **Nhánh**: `tpe`
- **Spec chi tiết**: `docs/superpowers/specs/2026-08-27-form-template-import-design.md`

## Mục tiêu
Thêm nút **Import Excel** vào màn **Tạo mẫu phiếu thu thập thông tin** (`/assign/form-templates/add`): nạp nhanh Section + câu hỏi khảo sát từ Excel, validate chi tiết theo dòng, chống trùng câu hỏi trong Ngân hàng câu hỏi (`survey_questions`) theo tổ hợp 4 yếu tố.

## Quyết định đã chốt
1. Ghi câu hỏi vào ngân hàng **khi bấm LƯU form** (không ghi lúc Import). Modal chỉ parse + validate + nạp builder.
2. Nạp builder = **APPEND** Section vào cuối.
3. Chỉ màn **Tạo mới**.
4. Validate theo **chuẩn chung** skill `import-excel` (có API validate BE + preview dedup).

## Đối chiếu thuật ngữ (issue → code)
- "Nhóm giải pháp" = **Ứng dụng** (`application_id`). "Nhóm ngành" đã bị bỏ khỏi schema → không thêm.
- "Phạm vi câu hỏi": Tất cả = `application_scope=1`; **Theo ứng dụng** = `application_scope=2` (dùng application_id đang chọn). Nhãn Excel dùng "Theo ứng dụng" (bỏ "Theo nhóm giải pháp" cũ, vẫn nhận alias).
- Loại câu hỏi → `data_type` chuỗi: short_text/long_text/number/dropdown/radio/checkbox/date/file/yes_no.

## Kiến trúc (đường ngắn)
```
Excel → V2BaseImportModal (parse+validate+preview group theo Section)
      → "Nạp vào form": câu hỏi mang cờ _import{data_type,application_scope,answers} (không libraryId)
      → APPEND vào FormBuilder.sections
      → LƯU → BE store pre-pass: resolveOrCreate(dedup 4 yếu tố) → gán libraryId+code=cau_hoi_{id}
      → tạo form_sections/form_questions/options như cũ
```

## Thay đổi chính
- **FE**: nút Import ở `FormMeta.vue` (disable khi chưa chọn Ứng dụng); `V2BaseImportModal` group theo Section trong FormBuilder; transform dòng → câu hỏi builder có `_import`; append sections; download template.
- **BE**:
  - `SurveyQuestionService::resolveOrCreate()` (mới) — dedup 4 yếu tố, trùng → tái dùng ID, không trùng → tạo mới + answers.
  - `FormTemplateService::store()` — thêm pre-pass `resolveImportedQuestions()` gán libraryId/code cho câu `_import` (additive, không đổi câu thư viện, không đụng update).
  - `FormTemplateController::validateImport()` + `importTemplate()` (mới) + 2 route đặt trước `/{formTemplate}`.
- **Không** thêm bảng/cột/permission mới. Không đụng schema.

## Chống trùng (3 case AC3)
1. scope=1 trùng trong nhóm chung → tái dùng ID.
2. scope=2 trùng cùng application → tái dùng ID.
3. scope=2 trùng ở application khác → tạo mới (gắn ứng dụng hiện tại).

## Ngoài phạm vi
Import màn Sửa; import câu hỏi phân cấp (hierarchy); khôi phục "Nhóm ngành".
