# Plan — Phiếu chờ giao việc (ERP → HRM) — @khoipv

## Phase 1 — Danh sách 5 tab

### Khảo sát
- [x] Khảo sát màn ERP `WrAssignTasks.wait` (5 tab, nguồn dữ liệu từng tab, hành động + điều kiện)
- [x] Rà menu HRM — chưa có mục chờ; user chốt đặt ở Công việc → Tiếp nhận công việc

### BE (hrm-api)
- [x] Seeder: 2 quyền type 24 — CSKH sau bán ("Xem danh sách phiếu chờ giao việc theo tổng công ty", "Tạo phiếu giao việc") — dry-run OK
- [x] `WaitingAssignTaskService`: query 5 tab + "còn số lượng" bằng SQL + phạm vi + lọc + sort + present + cờ hành động
  - bản đầu dùng subquery tương quan → tab HĐ 18,5 s, tab Lắp đặt treo → đổi sang GROUP BY + LEFT JOIN như ERP
- [x] `WaitingAssignTaskController` + route: meta / index / export / check-create / reject-reception (PL)
- [x] `ExportColumnRegistry` 5 khoá `waiting_assign_tasks_<tab>`
- [x] Smoke test HTTP kernel + so tập id với thuật toán ERP chép nguyên — KHỚP 100% (NV 34: HĐ 356 · PL 22 · Lắp đặt 160 · GV khác 792 · BH 405); lọc / sort / check-create / export 200
- [ ] Hiệu năng tab HĐ: ~3,5 s/trang 10 dòng (đếm 1 s + accessor `is_can_close`/`is_can_un_approve` ~110 ms/dòng — bảng `product_export_requests`/`product_import_requests` không có index `wr_service_contract_id`) → chờ user chốt

### FE (hrm-client)
- [x] `pages/customer-care/waiting-assign-tasks/index.vue` (tab trên URL) + `tabConfigs.js` — khuôn `pages/lookup/product-arrived-notifies`
- [x] `components/WaitingAssignTaskList.vue` (khuôn ArrivedNotifyList): lọc, cột, Cấu hình cột, Xuất Excel, hành động
- [x] Menu ~~Công việc → Tiếp nhận công việc~~ → user đổi 31/10: **CSKH sau bán → Giao việc** (`subsystem-menu/customer-care.js`), quyền đổi type 4 → 24, trang chuyển sang `/customer-care/waiting-assign-tasks`
- [x] Verify compile (vue-template-compiler + babel parse) + grep tự kiểm skill erp-to-hrm-screen
- [x] Playwright có cửa sổ (31/10, NV 13 DNS Admin, local): 27/29 PASS — 2 FAIL là lỗi của script / HMR dev, không phải của màn
  - Bắt + sửa lỗi THẬT: sang trang 2 không tải (b-pagination ghi thẳng `currentPage` trước khi emit `page-change`)
    → so với `requestedPage`; khuôn `ArrivedNotifyList.vue` (Phiếu báo hàng về) dính cùng lỗi, CHƯA sửa
  - Nới cột Hành động 110 → 130px (tab Lắp đặt 3 nút bị cắt)
- [x] Check "số lượng các tab lệch ERP" (31/10, chỉ điều tra): NV 13 HRM = HĐ 314 · PL 22 · BH 405 · LĐ 101 · GVK 792;
  nếu xem tất cả (như Super Admin bên ERP, Gate::before cho qua mọi quyền) = HĐ 380 · LĐ 160 (3 tab còn lại không đổi).
  Nguyên nhân 1: HRM chưa có / chưa gán quyền "Xem danh sách phiếu chờ giao việc theo tổng công ty" → bị bó theo 24 phòng quản lý.
  Nguyên nhân 2: DB local là bản chụp (HĐ mới nhất 18/08/2026, YC lắp đặt 28/07/2026) — so với ERP thật thì lệch cả 5 tab.
  → user chọn chạy sync + cấp quyền ở local
- [x] Local 31/10: `permission:sync` (thêm 36 quyền, trong đó id 2237/2238 type 24) + gán 2 quyền cho role 18 Super admin ở 5 công ty
  (1,2,3,4,8). NV 13 sau khi cấp: HĐ 380 · PL 22 · BH 405 · LĐ 160 · GVK 792 — khớp số "xem toàn bộ" như ERP; nút Tạo PGV / Từ chối đã hiện

### Checkpoint — 2026-10-31
Vừa hoàn thành: user test OK → commit + push develop: hrm-api `997a67f7f` (rebase lên 10 commit upstream, sạch), hrm-client `d2ddb8e27`
Đang làm dở: —
Bước tiếp theo: chạy `permission:sync` trên dev/prod + admin gán 2 quyền; (tuỳ user) tối ưu tab HĐ, sửa lỗi phân trang ở `ArrivedNotifyList.vue`
Blocked:
