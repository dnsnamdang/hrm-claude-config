# Plan — Thanh lý HĐ: Giá trị thực tế & chặn thanh lý

> @khoipv · 2026-07-01 · Spec: `docs/superpowers/specs/2026-07-01-contract-liquidation-actual-value-design.md`
> Plan chi tiết (7 task, step-by-step): `docs/superpowers/plans/2026-07-01-contract-liquidation-actual-value.md`

## Phase 1 — Backend
- [x] Migration thêm cột `actual_value` vào `contract_liquidations` (migrate OK)
- [x] Model `ContractLiquidation`: `$fillable` + cast `actual_value`
- [x] `StoreContractLiquidationRequest`: rule `actual_value` required + message
- [x] Service: guard `assertActualValueOk` + gán `actual_value` ở `store`/`update` + `snapshot` nhận `$agg`
- [x] Detail resource: trả `actual_value`

## Phase 2 — Frontend
- [x] `ContractLiquidationForm.vue`: state `actual_value` + map ở `loadDetail`/`buildPayload`
- [x] UI ô "Giá trị thực tế" ở Bước 2
- [x] Computed `hasBBNT`/`actualValueViolated` + banner cảnh báo
- [x] Validate trong `submit()` (required + chặn khi vi phạm)

## Phase 1b — Fix từ review tổng
- [x] [I-1] DetailResource: `total_performed`/`total_contract` tính TƯƠI khi `canEdit()` (tránh chặn nhầm ở màn Sửa); biên bản đã chốt giữ snapshot

## Phase 1c — Bổ sung theo quyết định user
- [x] Chặn cả khi DUYỆT: Controller `approve()` bọc try/catch (400); Service `approve()` guard tươi; DetailResource hiện số liệu tươi khi `canApprove()`; FE `approve()` chặn sớm banner/toast
- Giữ cho phép `actual_value = 0` (không siết > 0) — theo quyết định user

## Phase 3 — Verify
- [ ] User verify UI + các edge case (chưa có BBNT / đã có BBNT / vi phạm / để trống / sửa biên bản không duyệt)

### Checkpoint — 2026-07-01
Vừa hoàn thành: Code xong 7 task (BE+FE) qua subagent-driven; mỗi task review pass; review tổng Opus phát hiện + đã fix [I-1] (false-block màn Sửa). Chưa commit git (user tự commit).
Đang làm dở: (không)
Bước tiếp theo: User verify UI trên app + commit 2 repo (api, client).
Blocked: Cần user quyết Minor: có siết "bắt buộc > 0" và có chặn cả nút Duyệt không.
