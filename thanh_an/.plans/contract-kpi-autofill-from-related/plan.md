# Plan — Tự gắn hàng hóa từ HĐ liên quan vào KPI

**Người phụ trách:** @khoipv
**File chính:** `hrm-thanhan-client/pages/contract/contract/components/GeneralComponent.vue` (dùng chung add + edit)
**Spec:** `docs/superpowers/specs/2026-06-30-contract-kpi-autofill-from-related-design.md`
**Plan chi tiết (4 task):** `docs/superpowers/plans/2026-06-30-contract-kpi-autofill-from-related.md`

## Phase 1 — FE (GeneralComponent.vue)
- [x] Task 1: Thêm state `isLoadingKpiAutofill` + helper `mapProductToKpi()`
- [x] Task 2: Thêm `removeAutofilledKpiGroups()`, `applyKpiAutofillFromRelated()`, 2 handler `onHasKpiChange`/`onRelatedContractChange`
- [x] Task 3: Bind `@input` trên 2 select `has_kpi` + `related_contract_id` (+ `allowClear` + placeholder cho related)

## Phase 2 — Verify (UI)
- [ ] Task 4: Kiểm thử 9 kịch bản (xuôi/ngược, append, cộng dồn, bỏ chọn, tắt KPI, lưu+reload edit, rỗng, lỗi)

## Checkpoint

### Checkpoint — 2026-06-30
Vừa hoàn thành: code Task 1-3 (implementer subagent) + review (spec ✅, quality Approved) + áp finding Minor (placeholder cho allowClear)
Đang làm dở: không
Bước tiếp theo: user verify trên app (Task 4 — 9 kịch bản)
Blocked:
