# Progress ledger — BC bảo lãnh xem theo cập nhật (SDD)

Plan: `docs/superpowers/plans/2026-07-09-bc-bao-lanh-xem-theo-cap-nhat.md`
Chế độ: KHÔNG commit (user tự commit) — review diff lấy từ `git diff HEAD` + file mới untracked. Baseline: cả 2 repo sạch trên `thanhan-dev` lúc bắt đầu (2026-07-09).

## Trạng thái task

- Task 1: complete (file mới `ReportGuaranteeFlatResource.php`, php -l pass, review clean — spec ✅, Approved)
- Task 2: complete (ReportService.php +8 dòng nhánh latest_update, php -l pass, review clean — spec ✅, Approved, 0 finding)
- Task 3: complete (ReportsController.php import + phân nhánh resource, php -l + route:list pass, review clean — spec ✅, Approved; minor: thiếu newline cuối file — pre-existing)
- Task 4: complete (index.vue: checkbox + state + mounted merge + watcher + buildRequestParams/getData/reset + buildFlatRows, review clean — spec ✅, Approved)
- Task 5: complete (index.vue: th/td Thời gian cập nhật + columnCount computed 25/26 + colspan Tổng, review clean — spec ✅, Approved, 0 finding; alignment re-derived by reviewer). Snapshot post-task5: hrm-thanhan-client/.superpowers/sdd/index.vue.after-task5
- Task 6: complete (fetchAllPages + generateWorkbook: mapRows theo chế độ, splice cột 4, dịch numberColumnIndices — reviewer verify full column arithmetic, spec ✅, Approved; bonus fix: page ≥2 giờ cũng đi qua buildRequestParams)
- Task 7: complete — VERIFY UI E2E PASS toàn bộ (Playwright MCP, user DNS Admin):
  - Chế độ cũ không đổi: 25 cột, rowspan gom KH, total theo KH
  - Chế độ mới: 26 cột (cột 4 Thời gian cập nhật), sort DESC, KH tách hàng (BLC_BV0158 2 dòng), total 437 dòng
  - Kịch bản chính: Save tab bảo lãnh HD-162/2026 (không đổi data) → lên đầu 09/07/2026 17:03; ví dụ gốc của user HD2600049628_2603121304 đứng thứ 2 (16:04)
  - Trang 2: STT nối tiếp (11), thời gian tiếp tục giảm; hàng Tổng đúng ô
  - Filter "Lào Cai": 26 dòng đúng, vẫn sort; tắt checkbox → 25 cột + gom KH + total 4 KH; Đặt lại → filter trống + checkbox tắt; F5 giữ checkbox
  - Excel: chế độ mới 26 cột/437 dòng/numFmt [7,13,19,20,21,25], chế độ cũ 25 cột/numFmt gốc (parse bằng e2e/scripts/check-guarantee-xlsx.js)
  - Log BE 2026-07-09: không có file log = zero error

## Minor findings Task 4
- `buildFlatRows` thiếu `contract_created_by` (buildTableRows có) — ADJUDICATED: template không đọc field này ở đâu, vô hại; để final review quyết có thêm cho đồng nhất không.
- Watcher có thể fire 1 lần lúc mount khi localStorage có checkbox bật → 2 request — pattern PRE-EXISTING của mọi filter trang này, ngoài scope.

## Final review (Opus, 2026-07-09): READY TO COMMIT
- 0 Critical/Important. Minor: (1) race hiếm khi toggle checkbox lúc request đang bay (debounce thường che); (2) buildFlatRows thiếu contract_created_by — không consumer; (3) N+1 ::find() theo pattern resource cũ. Tất cả không chặn commit.

## Minor findings dồn cho final review

- Task 1: field `_name` trả `code` + `template_guarantee_name` = id + N+1 `::find()` — ĐÃ ADJUDICATE: chủ đích để khớp response nested cũ (resource cũ cũng làm vậy, FE map id template qua `getTemplateGuaranteeText`). Không sửa.
