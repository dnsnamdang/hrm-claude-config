# Biên bản xử lý hàng thừa, thiếu sau kiểm kê — Plan

> @khoipv · nhánh `feat/chuyen-doi-hang-hoa` (từ `gop_db`) · Spec: `docs/superpowers/specs/gop-db/2026-10-21-bien-ban-xu-ly-thua-thieu-kiem-ke-design.md`
> Khuôn: màn anh em **Phiếu kiểm kê theo hàng hóa** (`Modules/Finance/*SelfInventory*`, `pages/warehouse/self-inventories`).

## Phase 0 — Khảo sát
- [x] Đọc controller / model / blade / JS class ERP `inventory_audit_reports` (danh sách, form, chi tiết, duyệt + bút toán, in, quyền)
- [x] User chốt Q1–Q4 (spec mục 2)
- [x] Đọc dữ liệu thật + schema: local `inventory_audit_reports` RỖNG (0 dòng); nguồn có 1 phiếu nhập + 1 phiếu xuất KK (phiếu KK 575, kho 5)

## Phase 1 — BE (`Modules/Finance`)
- [x] B1. 3 quyền seeder (type 8) + `permission:sync --dry-run`
- [x] B2. Entities: phiếu (STATUSES màu SRS, quyền, `scopedQuery`, `canView/canEdit/canApprove`, `generateCode` BBXLKKHH-NNNNN) + chi tiết
- [x] B3. `InventoryAuditReportService`: list/filter/sort, filter-options, export-rows, detail, `sourceData` (port `getData`)
- [x] B4. `InventoryAuditReportWriteService`: form-options, store/update (lưu nháp / gửi duyệt + thông báo), approve (+ bút toán, rollback khi lỗi), file đính kèm, lịch sử
- [x] B5. FormRequest + Controller + routes + `catalog_histories` GATED
- [x] B6. In phiếu (mẫu 304) / In danh sách (303) + Xuất Excel phiếu
- [x] B7. Smoke test HTTP kernel (transaction rollback)

### Checkpoint — 2026-10-21 (Phase 1 BE xong)
Vừa hoàn thành: B1–B7 — 3 quyền seeder (dry-run: thêm đúng 3, CHƯA sync thật); Entities `InventoryAuditReport/*`; 4 service
(`InventoryAuditReport{Service,WriteService,PrintService,AttachmentService}`), 2 FormRequest, controller + 16 route
`/inventory-audit-reports`, GATED `inventory_audit_reports`, Export + blade. Smoke HTTP kernel (transaction rollback) 33/33 PASS:
lấy dữ liệu (4 dòng, đủ phiếu xử lý + mã kho), 422 thiếu lý do / dữ liệu đổi, lưu nháp → gửi duyệt → 409 sửa lại → duyệt (8 vế
bút toán 3381/3341/711 + 3341/1381/811 đúng số) → 409 duyệt lại, in / xuất / in DS / lịch sử, NV thường 404 / 403.
Đang làm dở: —
Bước tiếp theo: Phase 2 FE.
Blocked:

## Phase 2 — FE (`pages/finance/inventory-audit-reports`)
- [x] F1. Danh sách + row-actions + export-excel + In danh sách + Lịch sử
- [x] F2. Form dùng chung: thông tin chung, file đính kèm, Lấy dữ liệu, khối phiếu kiểm kê (tick), 2 tab Thừa / Thiếu, tính chi phí
- [x] F3. create / _id/edit / _id/index + footer (Lưu / Lưu và gửi duyệt / Lưu và tiếp tục / Duyệt / In / Xuất / Sửa)
- [x] F4. Menu `finance.js` erpPath → link
- [x] F5. Grep checklist skill + compile

### Checkpoint — 2026-10-21 (Phase 2 FE xong, chưa mở trình duyệt)
Vừa hoàn thành: F1–F5 — `pages/finance/inventory-audit-reports/` (index + create + _id/edit + _id/index, components:
InventoryAuditReportForm, row-actions, export-excel). Dùng lại KHÔNG sửa: `AttachmentSection` (api-base), `SystemInfoSection`,
`CatalogHistoryModal`, `V2BaseTabNavigation` (2 tab có cờ lỗi). Menu Tài chính › Kiểm kê: `erpPath` → `link`.
Grep checklist skill sạch; parse vue-template-compiler + @babel/parser 8 file OK; nuxt dev :3000 trả 200 cả 4 trang.
Đang làm dở: —
Bước tiếp theo: V1 — user `php artisan permission:sync` (3 quyền mới) + gán quyền; mở trình duyệt kiểm toàn luồng (Lấy dữ liệu kho 5
01–31/10/2025 → 4 dòng, tick/bỏ tick phiếu, Lưu / Lưu và gửi duyệt, Duyệt, In ngang, Xuất Excel, Lịch sử, NV thường).
Blocked:

## Phase 3 — Kiểm chứng
- [x] V1. Playwright e2e 21/10 (user yêu cầu) — `e2e/tests/finance/inventory-audit-report.spec.ts` **7/7 passed** (Node 24, DNS Admin):
  danh sách (cột, toolbar, 1 request), validate trống inline, tạo (Lấy dữ liệu kho 5 → 1 thừa + 3 thiếu, tính CP 60/40, lưu và gửi
  duyệt), chi tiết (sửa % rồi Duyệt → 8 bút toán đúng số), In ngang + Xuất Excel + Lịch sử, 404. Dữ liệu dọn theo id — DB về mốc.
  Chạy: `PATH=nvm/v24.6.0 node node_modules/@playwright/test/cli.js test tests/finance/inventory-audit-report.spec.ts --project=chromium --workers=1`
- [ ] V2. Chờ user chốt: cột chi phí `double(8,2)` bị cắt ≥ 1 triệu (spec mục 5)

## Phase 4 — Redmine #11829 (QA 22/10/2026)
- [x] Bug 1 — file .pdf hợp lệ đuôi bị báo "Chỉ nhận file pdf…": `uploadFiles` bỏ `mimes:` (đoán theo nội dung) → kiểm theo đuôi (khuôn #11262/#11313)
- [x] Bug 2 — Đơn giá vốn / Thành tiền vốn = 0 hiện trống → hiện `0` như ERP (`formatNumber` chỉ trống khi chưa có giá trị)
- [x] Bug 3 — danh sách: bỏ sort Ngày tạo / Người tạo / Người duyệt / Trạng thái, mặc định không mũi tên; sort cũ trong localStorage về mặc định (màn Phiếu kiểm kê theo hàng hoá đã sửa ở #11819/#11823/#11857)
- [x] Bug 4 — Chi tiết: bỏ ô Số phiếu, dấu (*) hiện cả ở màn chi tiết (Từ ngày, Đến ngày, Kho vật lý, Chi tiết, Lý do, Giá xử lý, % CP NV, NV chịu)
- [x] Bug 5 — Duyệt: xoá (x) Giá xử lý bị bỏ qua → giữ giá mặc định; nay về trống để validate chặn; ô trống gửi `null` (không `Number('')=0`) để BE `required` cũng chặn
- [x] Bug 6 — In: tiêu đề "Tab1/Tab2" chữ 13px in đậm (thay `<h4>`)

### Checkpoint — 2026-10-26
Vừa hoàn thành: 6 bug #11829 (FE `InventoryAuditReportForm.vue`, `index.vue`; BE `InventoryAuditReportController::uploadFiles`, `InventoryAuditReportPrintService::table`). Compile FE OK, `php -l` OK, test Validator: file .pdf nội dung lạ — rule cũ trượt, rule mới qua, .exe vẫn chặn.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm lại 6 điểm; commit khi user yêu cầu.
Blocked:

## Phase 5 — Redmine #11831 (QA 22/10/2026)
- [x] Validate tại ô, không sót trường: Giá xử lý xoá (x) giờ về trống → viền đỏ + câu lỗi (đi cùng bug 5 #11829); % Chi phí công ty thêm `*` + lỗi riêng `details.{i}.company_cost_percent` (chỉ FE — BE tự tính 100 − %NV)
- [x] Chi phí lệch ERP (999,999.99 × 50% → ERP 499,999.995, HRM 500,000): bỏ `round2` ở thành tiền / chi phí, format tối đa 3 số lẻ như filter `number` Angular. BE lưu vẫn round 2 (cột double(8,2) — y ERP), bản in / Excel in giá trị đã lưu

### Checkpoint — 2026-10-26 (#11831)
Vừa hoàn thành: 2 điểm #11831 trong `InventoryAuditReportForm.vue`; compile OK.
Đang làm dở: —
Bước tiếp theo: user kiểm trình duyệt #11829 + #11831; commit khi user yêu cầu.
Blocked:

## Phase 6 — Redmine #11832 (QA 22/10/2026)
- [x] Danh sách: Hàng thừa / Hàng thiếu = 0 hiện `0` như ERP — màn, Xuất Excel (ô số 0), In danh sách
- [x] Sort làm cột nhảy / vỡ layout: bảng chưa khai bề rộng (table-layout auto, tính theo dữ liệu từng lần) → `fixed-layout` + `width`/`minWidth` đủ 11 cột, cột chữ `text-wrap clamp-2` (skill list-page §15b). BE sort đã có `id` chốt thứ tự
- [x] In phiếu: Mã hàng dài không dấu cách đè sang cột Mã kho → ô in `word-break: break-word; overflow-wrap: anywhere` (không áp cho Excel)

### Checkpoint — 2026-10-26 (#11832)
Vừa hoàn thành: 3 điểm #11832 (`index.vue`, `export-excel.js`, `InventoryAuditReportPrintService`); compile FE + `php -l` OK.
Đang làm dở: —
Bước tiếp theo: user kiểm trình duyệt #11829 + #11831 + #11832; commit khi user yêu cầu.
Blocked:
