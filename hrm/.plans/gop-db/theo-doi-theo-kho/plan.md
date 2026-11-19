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

## Fix #11931 — Theo dõi theo kho: link tab mới + sort vỡ layout (30/10/2026)

- [x] FE: bấm Mã / Tên kho mở màn Hoạt động kho ở TAB MỚI (`target="_blank"`), không chuyển trong cùng trang
- [x] FE: sort vỡ layout — cột chỉ khai `width` → khai `width` + `minWidth` mọi cột qua helper `w(px)` (khuôn #11763/#11904); BE đã có cột phụ `w.id desc` nên thứ tự ổn định
- [x] Verify: compile template

## Tài liệu SRS / HDSD / Testcase (10/11/2026) @khoipv

Khuôn: `../hoat-dong-kho/` (10/11, cùng bảng hoạt động, cùng `WarehouseActivityService::listForWarehouses()`, cùng `components/warehouse/activity/*`). Không sửa code / dữ liệu / skill chung.

- [x] Đọc code FE (`pages/warehouse/warehouse-tracking/{index,_id/index}.vue`, `components/warehouse/activity/*`, filterStateMixin, exportFieldsMixin, middleware checkPermission) + BE (`WarehouseTrackingService`, `WarehouseTrackingController`, route `checkPermission:warehouse.kho.manage`, `WarehouseCatalogScope` mã `warehouse.kho_tat_ca_cong_ty.view`)
- [x] Chụp ảnh dev (`tdtk_shots/_capture/capture.js` + `export_empty.js`, DNS Admin, dữ liệu thật, chặn mọi yêu cầu ghi — 0 lọt; không bấm Lưu Cấu hình cột)
- [x] Đối soát dev (`_capture/probe.js`, chỉ GET): trang 1 = 22 kho = Kho vật lý 21 Hoạt động + 1 Khóa (MT-KNXT), đúng từng mã; trang 2 PTT 55 = 40 ĐNXK + 15 ĐNNK = đúng từng mã ở 2 màn danh sách (Chờ duyệt + Đang xuất/nhập kho); MT 5 = 1 + 4; KTCN 2 = 2 + 0; ô tổng hợp = số dòng; thứ tự đúng; kho 999999 → 404. (Sáng 10/11 bộ Hoạt động kho đo PTT 54 — thêm PDNXK-39058 gửi 11:12)
- [x] `gen_srs.py` → `SRS - Theo dõi theo kho.docx` (64 trang, 8 chức năng, selfcheck khớp mẫu; metrics ui 13.1 / ev 4.2 / evch 860 / intro 1904)
- [x] `gen_hdsd.py` → `HDSD_Theo doi theo kho.docx` (12 trang, 6 phần)
- [x] `gen_testcase.py` → `testcase.xlsx` (loai `bao_cao`, 130 TC, 8 nhóm, P0 44.6%, check_tc 0 lỗi)
- [x] `gen_checklist.py` → `Đối chiếu checklist.xlsx` (Testcase 117 có TC / 207 N/A; SRS 88 có mục / 75 N/A)
- [x] Ghi nhận (KHÔNG sửa): (1) bấm Mã/Tên mở TAB MỚI (fix #11931) — khác design.md "mở cùng tab"; tài liệu viết theo code; (2) quyền đã chuyển sang mã: route `checkPermission:warehouse.kho.manage`, Super Admin xem mọi công ty nhờ mã `warehouse.kho_tat_ca_cong_ty.view` (dev đúng: 22 kho + ô Công ty) — không dính lỗi mất nhánh Super Admin của Hoạt động kho; (3) menu còn khai `isShow: ['Quản lý kho']` theo tên cũ, chưa có `codes: ['warehouse.kho.manage']` như 7 màn Danh mục kho — khi gỡ tên cũ menu sẽ ẩn; (4) Xuất Excel 2 trang lệch nhau: trang 1 rỗng không tạo file + tích theo cột đang hiện, trang 2 rỗng vẫn tạo file + luôn tích đủ 10

### Checkpoint — 10/11/2026
Vừa hoàn thành: bộ SRS + HDSD + Testcase + Đối chiếu checklist màn Theo dõi theo kho.
Đang làm dở: —
Bước tiếp theo: user xem tài liệu; quyết định có thêm `codes` cho mục menu và có thống nhất hành vi Xuất Excel rỗng giữa 2 trang không.
Blocked:
