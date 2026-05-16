# Plan — Đổi cấp gán Câu hỏi / Phiếu thu thập từ Ứng dụng sang Nhóm giải pháp

**Owner:** @manhcuong
**Spec:** docs/superpowers/specs/2026-04-18-question-form-industry-level-design.md
**Bắt đầu:** 2026-04-18

## Phase 1 — BE migration data (PR1, deploy riêng không gãy UI cũ)

- [x] BE Tạo migration `2026_04_18_100001_backfill_industry_level_for_questions_and_forms.php`
- [x] BE Step 1: backfill `survey_questions.industry_id` và `scope_id` từ pivot (và application nếu pivot null)
- [x] BE Step 2: backfill `form_templates.industry_id` từ `application_industries` nếu null
- [x] BE Step 3: dedupe form_templates Published cùng industry — giữ cái mới nhất, còn lại set status=Locked
- [x] BE Chạy migration local + verify data bằng vài query
- [x] BE Test lại UI cũ (questions, form-templates, prospective-projects) không gãy (data sạch: 0 bản ghi null/duplicate)

## Phase 2 — BE schema + model + service + request (PR2)

- [x] BE Migration drop cột `application_id` + drop 3 pivot tables
- [x] BE `SurveyQuestion.php`: bỏ `application_id`, xoá relationships `scopes/industries/applications/application`
- [x] BE `FormTemplate.php`: bỏ `application_id`, xoá relationship `application()`
- [x] BE `SurveyQuestionService.php`: bỏ 3 method sync pivot, update `index`/`payload`/`store`/`update`/`destroy` sang single field
- [x] BE `FormTemplateService.php`: bỏ `application_id` khỏi payload/index/export CSV
- [x] BE `SurveyQuestionRequest.php`: rule mới theo `application_scope`, dùng single `scope_id`/`industry_id`
- [x] BE `FormTemplateRequest.php`: bỏ rule `application_id`, thêm withValidator check 1 industry - 1 Published khi tạo mới
- [x] BE `SurveyQuestionsResource.php` + `FormTemplatesResource.php`: bỏ output field application
- [x] BE `FormTemplateController@findByCriteria`: bỏ filter application_id (reuse cho endpoint by-industry)
- [x] BE `FormTemplateController@unlock`: đổi check unique theo industry
- [x] BE `ProspectiveProjectService.php`: `findFormTemplate` match theo industry Published
- [x] BE Xoá 3 Entity pivot file `SurveyQuestionScopes/Industries/Applications.php`
- [x] BE `Applications.php`: xoá relationship `formTemplates()`, `surveyQuestions()`, update `isCanDelete`

## Phase 3 — BE downstream hot-fix

- [x] BE Grep `application_id` trong Services/Transformers → không còn ref cũ
- [x] BE Grep `->applications()`, `survey_question_applications`, `FormTemplate::.*application` → clean
- [x] BE Verify `php -l` 11 file touched không lỗi syntax

## Phase 4 — FE màn Câu hỏi

- [x] FE `QuestionForm.vue`: bỏ dropdown Ứng dụng, bỏ field `application_ids`, dùng single `scope_id/industry_id`
- [x] FE `QuestionForm.vue`: đổi label option `Theo ứng dụng` → `Theo nhóm giải pháp`
- [x] FE `QuestionForm.vue`: update watcher/method `onChangeApplicationScope/onChangeScope`
- [x] FE `questions/add.vue`, `_id/edit.vue`, `_id/index.vue`: update `formSubmit` init + payload submit
- [x] FE `questions/index.vue`: bỏ filter + cột `application_id`, đổi label phạm vi, bỏ `formatEntityNames`
- [x] FE `questions/print.vue`: bỏ param + cột Ứng dụng

## Phase 5 — FE màn Mẫu phiếu

- [x] FE `FormMeta.vue`: bỏ cột Ứng dụng, layout còn 3 cột (Tên/Nhóm ngành/Nhóm giải pháp)
- [x] FE `FormBuilder.vue`: bỏ prop/state `applicationsAll`, watcher/handler `appId`, filter lib theo industry + include_all_scope
- [x] FE `FormPreview.vue`: bỏ prop `applicationsName` + cột Ứng dụng
- [x] FE `form-templates/add.vue`, `_id/edit.vue`, `_id/index.vue`: bỏ `application_id`/`appId` khỏi payload và state
- [x] FE `QuestionLibrary.vue`: bỏ prop/watcher `applicationId`
- [x] FE `AddQuestionQuickModal.vue`: đổi label, bỏ `application_id`, xoá comment block cũ
- [x] FE `form-templates/index.vue`: bỏ filter + cột Ứng dụng

## Phase 6 — FE Dự án TKT

- [x] FE không cần sửa: BE tự match form_template theo industry qua `handleFormTemplateSnapshot`. FE chỉ cần truyền industry_id đúng (đã có sẵn)

## Phase 7 — FE Meeting

- [x] FE `MeetingProject.vue`: `loadFormTemplate` chỉ dùng scope_id + industry_id
- [x] FE `MeetingProject.vue`: `onApplicationChange` no-op (không reset form_template)
- [x] FE `MeetingProject.vue`: watcher criteria chỉ theo scope_id + industry_id
- [x] FE `MeetingProject.vue`: UI alert + FormPreview props bỏ `app_id`

## Phase 8 — Test + verify

- [x] Test service-level qua tinker: 14/14 test pass (CRUD câu hỏi, schema, validation rule 1-1, find by industry)
- [x] Hot-fix `SurveyQuestionController@show`: `loadMissing` dùng relationship cũ đã xoá → đổi sang `scope/industry/answers`
- [x] Fix data: 12 câu hỏi `application_scope = null` → set theo scope/industry (bổ sung Step 1.5 vào migration)
- [x] FE syntax: 16/16 file Vue parse OK (template + script)
- [x] User test UI manual: confirm ổn

## Checkpoint

### Checkpoint — 2026-04-18
Vừa hoàn thành: Brainstorming xong, viết spec + design + plan
Đang làm dở: Chờ user review spec/plan
Bước tiếp theo: Bắt đầu Phase 1 — tạo migration BE
Blocked: (không)

### Checkpoint — 2026-04-18 (cuối buổi)
Vừa hoàn thành: Phase 1-7 code xong
- Phase 1: Migration backfill data (0 null, 0 duplicate) — đã run local
- Phase 2: Migration drop cột + pivot — đã run local; model/service/request/resource/controller updated
- Phase 3: Grep clean, 11 file PHP syntax OK
- Phase 4: FE Câu hỏi (6 file) done
- Phase 5: FE Mẫu phiếu (7 file) done
- Phase 6: FE Dự án TKT — không cần sửa (BE tự handle)
- Phase 7: FE Meeting (1 file lớn MeetingProject.vue) done

Đang làm dở: Phase 8 — manual test E2E
Bước tiếp theo: User test local 4 luồng (questions, form-templates, prospective-projects, meeting)
Blocked: (không)

### Checkpoint — 2026-04-18 (wrap up)
Vừa hoàn thành: Toàn bộ 8 Phase + hot-fix trong quá trình test
- 2 migration (backfill data + drop schema) — chạy sạch
- BE: 12 file (model, service, request, resource, controller, entity cleanup) + xoá 3 pivot entity orphan
- FE: 16 file (3 module: questions, form-templates, meeting) + FormPreview layout tự adjust sang 2 col
- 14 service test tinker pass + 16/16 Vue file parse OK
- Hot-fix: `SurveyQuestionController@show` loadMissing relationship cũ
- Data fix: 12 câu hỏi `application_scope = null` → backfill theo scope/industry, bổ sung Step 1.5 vào migration

Đang làm dở: (không)
Bước tiếp theo: Commit code + tạo PR khi sẵn sàng deploy (BE migration data trước → BE+FE drop schema sau, hoặc gộp 1 release)
Blocked: (không)
