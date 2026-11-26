# #10642 — HRM Plan: chặn Ngày bàn giao BBBG

Rule: `handover_date` từng serial `<= hôm nay` và `>= floor(product)` (floor = MIN(approved_time) PXK qua kho + PXH xuất thẳng, chỉ HĐ hãng). Design: `design.md` (+ ERP design cho nền nghiệp vụ). Plan tổng gộp cả ERP ở `ERP/.plans/10642-.../plan.md`.

## Tasks (HRM)
- [x] **T5 (BE):** `HandoverAcceptanceRecord::exportDateFloors()` + `applyHandoverDateValidation($validator,$source,$contractId,$products)` (guard `$source!=='firm'`). Gọi cuối `HandoverAcceptanceRecordRequest::after()`. `php -l` sạch.
- [x] **T6 (FE):**
  - [x] `HandoverContractSourceService::withExportFloor()` bơm `export_date_floor` (Y-m-d) theo product; gọi ở `contractData()` (chọn HĐ) + `HandoverAcceptanceRecordService::detail()` (Sửa).
  - [x] `handoverBuild.makeProduct` giữ `export_date_floor`.
  - [x] `HandoverProductTable.vue`: `:disabled-date="disabledDateFor(product)"` (chặn tương lai + trước floor); lỗi inline từ BE.

## Verify
- [x] **BE verified qua tinker + DB thật `erp_hrm_check`** (26/11): `exportDateFloors(9816,...)` = MIN(approved_time) startOfDay, bỏ hàng không có phiếu; nhánh xuất thẳng (contract 1838) trả floor đúng. `applyHandoverDateValidation` 5 ca: tương lai→chặn, trước floor→chặn kèm (23/12/2025), hợp lệ→OK, nguồn hrm→fail-open OK, hàng không phiếu→fail-open OK. `withExportFloor` trả `export_date_floor` Y-m-d / null đúng.
- [x] **FE verified qua Playwright MCP** (26/11, màn `/assign/handover-acceptance-records/create`): chọn HĐ hãng 9816 → API `contract-data?source=firm&contractable_id=9816` trả `export_date_floor` đúng từng product (vd 3978-3980 + 3987 "Lơ via móc lốp" = `2025-12-23`, hàng chưa có phiếu = `null`). Gọi thẳng `disabledDateFor(product)` của `HandoverProductTable.vue` trên state Vue thật (hôm nay 2026-11-26): product floor 2025-12-23 → disable 2027-01-01 (tương lai) + 2025-12-22 (trước floor), CHO chọn 2025-12-23 (đúng floor)/2026-01-15/hôm nay; product null floor → chỉ disable tương lai, 2025-12-22 cho chọn (fail-open). Khớp thiết kế 100%.
- [ ] ERP: chưa kiểm qua form Angular.

## Checkpoint — 2026-11-26 (cập nhật)
Vừa hoàn thành: T5+T6 HRM (BE+FE); plan ERP [x] T1-T4 + Ruling approved_time; **BE HRM verified full qua tinker/DB thật** (5 ca + 2 nguồn floor); **FE HRM verified qua Playwright MCP** (API bơm floor đúng + `disabledDateFor` chặn đúng trên state thật — xem mục Verify).
Đang làm dở: ERP form check (Angular) — chưa chạy.
Bước tiếp theo: kiểm ERP qua form Angular (reproduce #10642 trên màn ERP); rồi chờ user duyệt push/gop_db.
Blocked: (trống) — chờ user duyệt trước khi push/gop_db.

### Checkpoint — 2026-11-26 (wrap up cuối ngày)
Vừa hoàn thành: commit + push hrm-api develop `df7be0839c`, hrm-client develop `684050fc97` (pull --rebase, không force; ERP `533499f2b7`).
Đang làm dở: (không, phía HRM) — ERP chưa kiểm form Angular.
Bước tiếp theo: gop_db khi user yêu cầu; cập nhật Redmine #10642.
Blocked: (không) — CHƯA gop_db.
