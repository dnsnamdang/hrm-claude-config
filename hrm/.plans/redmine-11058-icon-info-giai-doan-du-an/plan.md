# Plan — Redmine #11058 Icon Info + Tooltip mô tả cho Giai đoạn dự án

Nguồn: http://quanly.dnsmedia.vn/issues/11058 — nhánh `tpe-develop-assign`.
Tiền lệ: #11045 (Loại meeting) — `components/MeetingTypeSelect.vue` + `utils/meetingTypeInfoTooltip.js`.
Ghi chú phạm vi: màn **Báo giá không có trường Giai đoạn dự án** (đã grep `quotations`, `summary-quotations`) → không có gì để áp.

## FE — Component dùng chung
- [x] Tách ruột `MeetingTypeSelect.vue` → `components/DescriptionInfoSelect.vue` (select + icon Info theo `description` của option)
- [x] `MeetingTypeSelect.vue` → wrapper mỏng (giữ nguyên API props/event, 8 màn meeting không phải sửa)
- [x] Tạo `components/ProjectPhaseSelect.vue` — wrapper mỏng, placeholder "Chọn giai đoạn dự án"
- [x] `utils/meetingTypeInfoTooltip.js` — export thêm `buildInfoIconHtml()` + `escapeHtmlText()` (dùng chung cho select và chỗ chỉ nhận chuỗi HTML)
- [x] `store/optionsSelect.js:fetchProjectPhases` — map thêm `description`

## FE — Thay select ở các màn
- [x] `prospective-projects/components/ProgressFinanceSection.vue` (phủ Tạo/Sửa/Chi tiết dự án TKT + tab TKT của Yêu cầu giải pháp)
- [x] `prospective-projects/index.vue` — filter danh sách
- [x] `report/prospective-projects/components/ProspectiveProjectsFilter.vue` — filter báo cáo
- [x] `solutions/index.vue` — filter danh sách Giải pháp
- [x] `report/meeting-by-projects/index.vue` — filter báo cáo meeting theo dự án
- [x] `my-job/components/SolutionUpcomingModal.vue` — filter modal (`:inModal="true"`)

## BE + FE — Chỗ hiển thị readonly (AC4)
- [x] `SolutionResource.php` — trả thêm `project_phase_description` (dùng lại relation `projectPhase` sẵn có, không thêm query)
- [x] `solutions/components/SolutionForm.vue` — map `project_phase_description` khi lấy từ dự án
- [x] `solutions/components/InfoTab.vue` — icon Info cạnh tên giai đoạn (computed `projectPhaseHtml` + `isHtml`)
- [x] ~~`request-solution/components/FormTab.vue`~~ — BỎ: chỗ này là dữ liệu header của **phiếu in** (`SurveyPrintSheet`), không phải màn xem chi tiết; chèn icon vào bản in là sai chuẩn. Màn chi tiết Yêu cầu giải pháp xem giai đoạn ở tab TKT (`ProgressFinanceSection`) — đã có icon.

## Kiểm thử
- [ ] AC1-AC4 theo issue (chưa chọn không icon / dropdown có icon cuối dòng / đã chọn có icon trong ô / chi tiết + filter)
- [ ] Regression màn Meeting (do đổi ruột `MeetingTypeSelect`)

### Checkpoint — 2026-08-15
Vừa hoàn thành: toàn bộ code FE + BE của #11058, đã check cú pháp (node --check phần script các SFC/JS), diff sạch không lệch CRLF.
Đang làm dở: chưa chạy test UI thật.
Bước tiếp theo: chạy dev server + Playwright kiểm AC1-AC4 và regression màn Meeting (chờ user xác nhận).
Blocked:
