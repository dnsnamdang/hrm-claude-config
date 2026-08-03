# Plan — BC bảo lãnh: chế độ xem theo thời gian cập nhật

> Plan chi tiết 7 task (full code): `docs/superpowers/plans/2026-07-09-bc-bao-lanh-xem-theo-cap-nhat.md`
> Ledger thực thi SDD: `.plans/bc-bao-lanh-xem-theo-cap-nhat/progress-ledger.md`

## Phase 0 — Brainstorming
- [x] Khảo sát màn guarantee_contract hiện tại (FE + BE)
- [x] Chốt phương án thiết kế với user (phương án A, 2026-07-09)
- [x] Viết spec chi tiết (`docs/superpowers/specs/2026-07-09-bc-bao-lanh-xem-theo-cap-nhat-design.md`)
- [x] User review spec (OK 2026-07-09)
- [x] Viết plan chi tiết (writing-plans)

## Phase 1 — BE (subagent-driven, mỗi task có review)
- [x] Task 1: Resource phẳng `ReportGuaranteeFlatResource` (spec ✅, Approved)
- [x] Task 2: `ReportService` nhánh `view_mode=latest_update` — sort updated_at DESC + id DESC (spec ✅, Approved)
- [x] Task 3: `ReportsController` phân nhánh resource (spec ✅, Approved)

## Phase 2 — FE
- [x] Task 4: Checkbox + filter state + `buildRequestParams` + `buildFlatRows` + getData/reset/mounted/watcher (spec ✅, Approved)
- [x] Task 5: Template cột "Thời gian cập nhật" + columnCount computed 25/26 (sửa luôn bug lệch 24) + colspan hàng Tổng (spec ✅, Approved)
- [x] Task 6: Excel theo chế độ — mapRows + splice cột 4 + dịch numberColumnIndices (spec ✅, Approved)

## Phase 3 — Verify
- [x] Task 7: Verify UI E2E PASS (chi tiết trong progress-ledger.md) — kịch bản chính: save tab bảo lãnh HD-162/2026 → lên đầu với timestamp mới; chế độ cũ không regression; Excel 2 chế độ parse đúng; log BE sạch
- [x] Final whole-feature review (Opus): READY TO COMMIT — 0 Critical/Important; 3 minor note (race toggle nhanh khi request in-flight, buildFlatRows thiếu contract_created_by (không ai đọc), N+1 find theo pattern cũ)

### Checkpoint — 2026-07-09 17:10
Vừa hoàn thành: Toàn bộ 7 task + final review PASS. Code nằm ở working tree 2 repo (CHƯA commit — user tự commit).
Đang làm dở: (không)
Bước tiếp theo: User review + tự commit (API: 2 file sửa + 1 file mới; Client: 1 file sửa).
Blocked: (không)

Người phụ trách: @khoipv
