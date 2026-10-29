# Plan — Redmine #11016 Bổ sung Giai đoạn dự án cho Báo giá & Yêu cầu làm giải pháp (+ đồng bộ về dự án)

Nguồn: http://quanly.dnsmedia.vn/issues/11016 — nhánh `tpe-develop-assign`.
Là **task nền** của [#11058](../redmine-11058-icon-info-giai-doan-du-an/plan.md): 2 màn này trước đó không có trường Giai đoạn dự án nên không có chỗ gắn icon Info.

Quyết định thiết kế: **bắt buộc khi GỬI** (Báo giá: Trình duyệt; YCGP: status = 2 Chờ tiếp nhận), **không chặn Lưu nháp** — theo convention của project (BE quyết theo status, trả 422/lỗi nghiệp vụ → FE hiện inline).

## BE
- [x] Migration `2026_08_15_100000_...` — thêm `project_phase_id` (nullable + index) vào `quotations`, `request_solutions`; đã chạy trên DB local
- [x] Entity `Quotation`, `RequestSolution` — relation `projectPhase()`
- [x] `ProspectiveProjectService::syncProjectPhase()` — đồng bộ giai đoạn (+ mức ưu tiên theo giai đoạn) về dự án gốc
- [x] `QuotationService`: `create()` fill + kế thừa giai đoạn dự án, `update()` whitelist, `submit()` chặn thiếu giai đoạn, sync sau create/update
- [x] `RequestSolutionService`: `store()`/`update()` lưu + sync sau khi lưu
- [x] `QuotationStoreRequest` / `QuotationUpdateRequest` — rule `nullable|exists:project_phases,id`
- [x] `RequestSolutionRequest` — `required` khi status = 2, kèm message tiếng Việt
- [x] Resource: `QuotationResource`, `DetailQuotationResource`, `RequestSolutionResource`, `DetailRequestSolutionResource` trả `project_phase_id/name/description`
- [x] Eager load `projectPhase` ở list/detail 2 màn (tránh N+1)
- [x] Bộ lọc `project_phase_id` cho danh sách Báo giá (`applyListFilters`) và YCGP (`index` + `pending`)

## FE
- [x] Báo giá `quotations/_id/edit.vue` (dùng chung cho Tạo mới + Sửa): ô chọn trong Thông tin chung, prefill giai đoạn của dự án khi chọn dự án, validate khi Trình duyệt, watcher nạp lại options khi giai đoạn đã khoá
- [x] Báo giá `quotations/_id/index.vue` (chi tiết): hiển thị + icon Info `b-popover`
- [x] Báo giá `quotations/index.vue`: bộ lọc Giai đoạn dự án
- [x] YCGP `request-solution/components/RequestTab.vue`: ô chọn (required) + watcher options; `RequestSolutionForm.vue` thêm field vào state/load/prefill (chi tiết dùng chung form ở mode `show`)
- [x] YCGP `request-solution/index.vue` + `pending.vue`: bộ lọc + cột Giai đoạn ưu tiên dữ liệu của chính yêu cầu
- [x] Mọi ô chọn dùng `ProjectPhaseSelect` (#11058) → có sẵn icon Info + tooltip mô tả

## Kiểm thử
Script test BE: `scratchpad/test_11016.php` + `test_11016b.php` (chạy trong transaction, rollback cuối) — **35/35 pass**.
- [x] BE: sync về dự án (kèm mức ưu tiên), giữ nguyên khi phase null / id rác, chứng từ lưu sau thắng, create kế thừa giai đoạn dự án, submit chặn thiếu giai đoạn, rule required theo status, resource trả đủ field, bộ lọc lọc đúng bản ghi, 20 dòng danh sách = 25 query (không N+1)
- [x] AC1 (UI): tạo YCGP để trống giai đoạn → lỗi inline "Vui lòng chọn giai đoạn dự án." ngay tại ô
- [x] AC2 (UI): báo giá BG-2026-00251 chọn "3.Chọn giải pháp…" + Lưu nháp → dự án 81 đổi phase 4→3, priority→7
- [x] AC3 (UI): tạo YCGP TPE.YCP.TC.26.0012 chọn "5. CĐT duyệt danh mục đầu tư" → dự án 105 phase NULL→5, priority→6; màn chi tiết dự án hiển thị đúng
- [x] Chi tiết Báo giá / chi tiết YCGP hiển thị giai đoạn (disabled) + icon Info, hover ra tooltip
- [x] Bộ lọc Giai đoạn dự án chạy đúng ở: danh sách Báo giá, danh sách YCGP, danh sách Dự án TKT, danh sách Giải pháp, báo cáo Dự án TKT
- [x] Regression màn Meeting: dropdown Loại meeting vẫn đủ icon, chọn xong bắn đúng `meeting_type_id=2`, 0 lỗi console

### Checkpoint — 2026-08-15
Vừa hoàn thành: toàn bộ BE + FE #11016 + test BE (35/35) và test UI end-to-end AC1-AC3.
Đang làm dở: —
Bước tiếp theo: chờ user xác nhận có xoá dữ liệu test trên DB local (YCGP #12) không, rồi chuyển trạng thái Redmine sang "Code xong chờ test".
Blocked:

### Fix bổ sung — 2026-08-19
- [x] `QuotationService::copy()` copy thiếu `project_phase_id` → bản sao mất Giai đoạn dự án (BG-2026-00111 → 00122). Copy y nguyên, KHÔNG gọi `syncProjectPhase()` (bản sao không phải chứng từ đổi giai đoạn).
- [x] Rà cùng lượt: `copyGroups()` không copy `parent_id` → cây nhóm bị bẹt (22/24 nhóm mất cha ở BG 122); `copyServiceItems()` không remap `quotation_group_id`. Đã sửa cả 2.

## Phản hồi #12 (2026-10-16, nhánh develop)
- [x] BE: rule dùng chung `Modules/Assign/Rules/ActiveProjectPhase` — chọn mới phải là giai đoạn Hoạt động, giữ nguyên giai đoạn đã lưu (nay khoá) vẫn cho lưu; gắn vào QuotationStore/UpdateRequest, RequestSolutionRequest, ProspectiveProjectRequest (BUG 1, 2)
- [x] FE: form báo giá + yêu cầu giải pháp nạp lại giai đoạn `force: true` khi mở (BUG 1, 2)
- [x] FE: đổi dự án → giai đoạn lấy theo dự án mới — báo giá `selectProject()` ghi đè; YCGP chỉ ghi đè khi watcher thấy đổi A→B, mở phiếu không đè (BUG 3)
- [x] FE báo giá: lỗi 422 trước đây chỉ toast "The given data was invalid." → thêm `applyServerValidationErrors()` đưa lỗi xuống dưới ô (+ toast câu BE), dùng ở `save()` và `previewSubmitOnCreate()`; đổi giai đoạn thì xoá dòng lỗi cũ
- [x] Test 16/10 (API + Playwright local), đạt hết:
  - BE: tạo báo giá / YCGP / dự án TKT với GĐ khoá → 422 "đã bị khoá"; GĐ hoạt động qua; sửa báo giá đổi sang GĐ khoá → 422, dữ liệu không đổi; rule 5 nhánh (tinker)
  - Báo giá: chọn DA097 (GĐ3) → đổi DA093 → GĐ1 (BUG 3); khoá GĐ trong lúc form mở → Lưu nháp báo lỗi dưới ô, không tạo bản ghi; đổi GĐ khác → lỗi mất, Lưu nháp OK; sửa báo giá đang giữ GĐ khoá → hiện 🔒, Lưu nháp OK
  - YCGP: chọn DA091 (GĐ1 khoá) → 🔒 1; đổi dự án 142 → GĐ3, GĐ1 biến khỏi list (BUG 3); khoá GĐ3 khi form mở → Lưu nháp báo lỗi dưới ô (BUG 2); mở Sửa phiếu 34 có GĐ khác dự án → giữ nguyên
  - Dự án TKT 155 giữ GĐ3 đã khoá → Lưu OK (hồi quy rule mới)
  - Đã trả: GĐ1/2/3 mở khoá, DA142 created_by=774, YCGP 34 GĐ1, xoá BG-2026-00123
- Ghi nhận (cũ, chưa sửa): `scrollToFirstError()` báo giá cuộn ngang `.content-page` 50px ở màn hẹp 1200px
