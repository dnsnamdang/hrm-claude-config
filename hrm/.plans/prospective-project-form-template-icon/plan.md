# Plan — Icon mẫu phiếu thu thập cạnh Nhóm giải pháp

Feature: @manhcuong · Spec: docs/superpowers/specs/2026-06-17-prospective-project-form-template-icon-design.md

## Phase 1 — FE (ProjectInfoSection.vue)

### FE
- [x] Thêm icon `ri-file-text-line` trong `<V2BaseLabel>` của trường "Nhóm giải pháp" + `b-popover` tooltip
- [x] Thêm state `formTemplate { checking, exists, id }` + computed màu/cursor/tooltip
- [x] Watcher `formTemplateCriteriaKey` (immediate) gọi `find-by-criteria?industry_id=...`, xử lý 200/404, chống race (seq)
- [x] Handler click: chỉ khi exists → `window.open('/assign/form-templates/'+id,'_blank')`
- [x] Style 3 trạng thái (xám #94a3b8 disabled / xanh #16a34a clickable)

### Test (UI người dùng cuối)
- [ ] AC1: mở Tạo mới → icon xám, không click
- [ ] AC2: chọn đủ 2 field, nhóm GP chưa có mẫu → xám + tooltip "Chưa cấu hình..."
- [ ] AC3: chọn đủ 2 field, nhóm GP có mẫu Published → xanh + tooltip "Xem chi tiết..."
- [ ] AC4: click icon xanh → mở tab mới `/assign/form-templates/:id`
- [ ] Màn Cập nhật prefill: icon tính trạng thái đúng khi mở

## Checkpoint — 2026-06-17
Vừa hoàn thành: CODE DONE Phase 1 FE. Sửa 1 file `ProjectInfoSection.vue` (icon + import buildQuery + state formTemplate + 3 computed + watcher immediate + 2 method checkFormTemplate/openFormTemplate + style). Verify vue-template-compiler + @babel/parser PASS. BE không đổi (tái dùng find-by-criteria).
Đang làm dở: (không)
Bước tiếp theo: user chạy hrm-client (npm dev) verify browser AC1–AC4 + màn Cập nhật prefill.
Blocked: (không)
