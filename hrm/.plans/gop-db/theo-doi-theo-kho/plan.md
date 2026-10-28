# Plan — Theo dõi theo kho

> Phụ trách: @khoipv · Tạo 27/10/2026 · nhánh `develop` (cả 2 repo, con của `gop_db`)
> Design: `.plans/gop-db/theo-doi-theo-kho/design.md` · Spec: `docs/superpowers/specs/gop-db/2026-10-27-theo-doi-theo-kho-design.md`

## Chốt với user (27/10/2026)

- Quyền: dùng lại quyền HRM **"Quản lý kho"** (y ERP, đang gate 7 màn Danh mục kho) — không tạo quyền mới.
- Phạm vi: y ERP theo công ty — `WarehouseCatalogScope` (Super Admin mọi công ty + ô lọc Công ty; người khác khoá công ty mình).
- Được sửa phần dùng chung của màn Hoạt động kho, giữ nguyên hành vi màn cũ.
- 2 trang như ERP: danh sách kho → trang hoạt động của 1 kho.

## Phase 1 — BE

- [x] `WarehouseActivityService`: tách `listForWarehouses(?array $ids, Request)`; `list()` gọi lại với kho thủ kho (hành vi cũ giữ nguyên)
- [x] `WarehouseTrackingService`: `list()` phân trang (keyword mã/tên, nhóm, công ty; sort code/name/created_at), `exportRows()`, `filterOptions()`, `activities($id)` (ngoài phạm vi → 404)
- [x] `WarehouseTrackingController` + route `finance/warehouse-tracking` gắn `checkPermission:Quản lý kho`
- [x] Smoke test API qua tinker (list / filter-options / activities / 404)

## Phase 2 — FE

- [x] Dời `ActivitySummary.vue` + `export-excel.js` sang `components/warehouse/activity/` (thêm prop nội dung info / tiêu đề file); thêm `activity-table.js` (cột, tô màu dòng, link phiếu) dùng chung
- [x] Màn Hoạt động kho đổi import sang chỗ mới, hành vi giữ nguyên
- [x] `pages/warehouse/warehouse-tracking/index.vue` — danh sách kho (STT, Mã, Tên, Nhóm, Công ty), lọc, Cấu hình cột, Xuất Excel
- [x] `pages/warehouse/warehouse-tracking/_id/index.vue` — bảng hoạt động 1 kho, khối tổng hợp, tô màu, tự tải lại 60s, Xuất Excel, 404
- [x] Menu `subsystem-menu/warehouse.js`: mục "Theo dõi theo kho" (isShow `Quản lý kho`)
- [x] Compile check các file .vue

## Phase 3 — Nghiệm thu

- [ ] User mở trình duyệt bấm thật 2 màn mới + màn Hoạt động kho (không đổi)

### Checkpoint — 2026-10-27
Vừa hoàn thành: Phase 1 BE + Phase 2 FE. API đã smoke test qua HTTP kernel: Super Admin (19 kho, lọc/sort/xuất, kho 4 có dữ liệu, id lạ 404); người công ty 2 (nv 333) chỉ thấy 4 kho của công ty mình, `company_id=1` bị bỏ qua, mở kho công ty khác 404; `/warehouse-activities` cũ vẫn 200. Quyền gán tạm cho nv 13/333 đã gỡ.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt bấm thật `/warehouse/warehouse-tracking`, `/warehouse/warehouse-tracking/4` và `/warehouse/activities`. Tài khoản test cần quyền "Quản lý kho" (id 1840 trên DB local chưa gán cho role nào — kể cả Super admin).
Blocked: chưa bấm thật trên trình duyệt

### Checkpoint — 28/10/2026 (wrap up)
Vừa hoàn thành: ĐÃ PUSH `develop` 28/10 — api `1731d3a4c`, client `6f0ece1ba` (gộp cùng fix Hoạt động kho #11894 màu dòng · #11895 Excel giãn dòng · #11904 width cột sort, xem `.plans/gop-db/hoat-dong-kho/plan.md`).
Đang làm dở: —
Bước tiếp theo: Phase 3 — user bấm thật 2 màn trên dev; deploy cần quyền "Quản lý kho" có trong seeder + gán role.
Blocked: chưa bấm thật trên trình duyệt
