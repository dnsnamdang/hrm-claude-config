# Plan — Redmine #11058 Icon Info + Tooltip mô tả cho Giai đoạn dự án

Nguồn: http://quanly.dnsmedia.vn/issues/11058 — nhánh `tpe-develop-assign`.
Tiền lệ: #11045 (Loại meeting) — `components/MeetingTypeSelect.vue` + `utils/meetingTypeInfoTooltip.js`.
Ghi chú phạm vi: màn Báo giá và Yêu cầu làm giải pháp ban đầu **chưa có trường Giai đoạn dự án** → đã bổ sung ở [#11016](../redmine-11016-giai-doan-du-an-bao-gia-ycgp/plan.md), và mọi ô chọn ở đó dùng luôn `ProjectPhaseSelect` nên có sẵn icon Info + tooltip.

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

## FE — Báo giá & Yêu cầu làm giải pháp (sau khi #11016 bổ sung trường)
- [x] Báo giá: form Tạo mới/Sửa, màn chi tiết (icon Info + `b-popover`), bộ lọc danh sách
- [x] Yêu cầu làm giải pháp: form Tạo mới/Sửa/Chi tiết, bộ lọc danh sách + màn chờ tiếp nhận

## Kiểm thử (Playwright trên dev :3000 ↔ :8000)
- [x] AC1: chưa chọn giai đoạn → ô chỉ có placeholder, KHÔNG có icon
- [x] AC2: mở dropdown → 8/8 dòng có icon ở cuối; hover ra popover `.info-popover` đúng mô tả, nằm trong viewport, z-index 10050 (không bị dropdown che)
- [x] AC3: chọn xong → icon nằm cạnh text trong ô, giữ đúng mô tả
- [x] AC4: chi tiết Dự án TKT / Báo giá / YCGP / Giải pháp đều hiện giai đoạn kèm icon + tooltip; bộ lọc ở 5 màn danh sách + báo cáo đều có icon
- [x] Regression màn Meeting: dropdown Loại meeting đủ icon, chọn xong bắn đúng `meeting_type_id`, 0 lỗi console

### Checkpoint — 2026-08-15
Vừa hoàn thành: toàn bộ code FE + BE của #11058, đã check cú pháp (node --check phần script các SFC/JS), diff sạch không lệch CRLF.
Đang làm dở: chưa chạy test UI thật.
Bước tiếp theo: chạy dev server + Playwright kiểm AC1-AC4 và regression màn Meeting (chờ user xác nhận).
Blocked:
