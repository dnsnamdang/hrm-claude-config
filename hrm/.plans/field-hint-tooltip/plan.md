# Plan — Tooltip ⓘ giải thích thuật ngữ nghiệp vụ

## Phase 1 — Hạ tầng dùng chung

### FE

- [x] Tạo `utils/constants/field-hints.js` — từ điển 5 thuật ngữ + alias nhãn + `getFieldHintByLabel/Term`
- [x] Tạo `components/V2BaseFieldHint.vue` — icon ⓘ, tooltip hover/focus, `white-space: pre-line`, props `label/term/text/extra`
- [x] Sửa `components/V2BaseLabel.vue` — tự tra từ điển theo prop `text` hoặc text node của slot; thêm props `hint`, `hintExtra`, `noHint`
- [x] Sửa `components/assign-components/CascadePairSelect.vue` — `parentTooltip/childTooltip` fallback sang từ điển theo `parentLabel/childLabel`

## Phase 2 — Gắn vào nhãn `<label>` thuần (không dùng V2BaseLabel)

### FE

- [x] `pages/assign/project_phase/components/ProjectPhaseForm.vue` — Nhóm ngành, Nhóm giải pháp, Ứng dụng
- [x] `pages/assign/questions/components/QuestionForm.vue` — Ứng dụng
- [x] `components/human-components/customer/CustomerScopeSelect.vue` — Lĩnh vực khách hàng

## Phase 3 — Dọn tooltip tự chế trùng lặp

### FE

- [x] `components/assign-components/customer/CustomerForm.vue` — bỏ 2 icon `v-b-tooltip` tự gắn (Loại hình HĐ KH, Lĩnh vực KD KH)
- [x] `pages/assign/prospective-projects/components/CustomerBlock.vue` — bỏ `info-tip` + `b-popover` + data `tooltips` + `tipId()` + CSS thừa
- [x] `pages/assign/prospective-projects/components/ProjectInfoSection.vue` — bỏ popover `applicationTooltip` (nội dung cũ) + CSS thừa
- [x] `pages/assign/solutions/components/InfoTab.vue` — gộp ghi chú "liên hệ Master Data" vào tooltip chung qua `hint-extra`, bỏ popover riêng

## Phase 4 — Kiểm thử

- [x] Compile-check 10 SFC đã sửa (vue-template-compiler + @babel/parser) — pass
- [x] Unit-check từ điển: 10 nhãn hợp lệ khớp, 4 nhãn nhiễu (Mã nhóm ngành, Số ứng dụng...) không khớp
- [x] E2E Playwright trên FE :3000 — AC1/AC2/AC3 PASS (14 màn)

## Phase 5 — Fix phát hiện khi E2E

### FE

- [x] `components/modal/application-modal.vue` — gỡ `parentTooltip`/`childTooltip` nội dung cũ (thiếu tiền tố thuật ngữ), để CascadePairSelect fallback từ điển

### Checkpoint — 2026-07-27

Vừa hoàn thành: Phase 1–5, E2E pass toàn bộ AC.
Đang làm dở: không.
Bước tiếp theo: user review + merge.
Blocked:

#### Kết quả E2E (14 màn)

| Màn | Icon tìm thấy |
| --- | --- |
| /assign/industry-groups + popup Tạo mới | Tên nhóm ngành ✓ (hover/blur PASS) |
| /assign/solution-groups + popup | Tên nhóm giải pháp, Nhóm ngành ✓ |
| /assign/application + popup | Tên ứng dụng, Nhóm ngành, Nhóm giải pháp, Loại hình HĐ KH, Lĩnh vực KD KH ✓ |
| /assign/customer-scope-groups + popup | Loại hình hoạt động KH ✓ |
| /assign/customer-scopes + popup | Lĩnh vực KD KH, Loại hình HĐ KH ✓ |
| /assign/customers/add | Loại hình HĐ KH, Lĩnh vực KD KH ✓ (không trùng icon) |
| /human/customers/add | Loại hình HĐ KH, Lĩnh vực KD KH ✓ |
| /assign/prospective-projects (list + add + edit) | Ứng dụng, Loại hình HĐ KH, Lĩnh vực KD KH ✓ |
| Popup Thêm nhanh khách hàng | Loại hình HĐ KH, Lĩnh vực KD KH ✓ |
| /assign/request-solution/add | Ứng dụng, Nhóm ngành, Nhóm giải pháp ✓ |
| /assign/solutions (list + chi tiết) | 5 thuật ngữ ✓ + `hint-extra` gộp ghi chú Master Data đúng |
| /assign/meeting/create → tab Dự án TKT | Loại hình HĐ KH, Lĩnh vực KD KH, Ứng dụng ✓ |
| Báo cáo solutions-work-summary-by-department | Nhóm ngành, Nhóm giải pháp, Ứng dụng ✓ |
| /assign/request-solution/pending | Không có trường nào trong 5 thuật ngữ → không có icon (đúng) |

Tooltip Ứng dụng render đủ 3 dòng (1 định nghĩa + 2 bullet), rộng 340px. `.info-tip` cũ = 0 ở mọi màn (không còn icon trùng).
