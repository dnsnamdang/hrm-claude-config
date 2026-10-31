# Plan — Phiếu giao việc CSKH (ERP → HRM) — @khoipv

## Phase 0 — Khảo sát
- [x] Khảo sát ERP: danh sách / phạm vi / hành động (controller + model searchByFilter)
- [x] Khảo sát ERP: form tạo (blade + class JS) — 3 agent song song (form · BE lưu · hiện trạng HRM)
- [x] User chốt 6 quyết định (spec mục 0)
- [x] Viết spec + design

## Phase 1 — BE danh sách / chi tiết / xóa (hrm-api)
- [ ] T1 Entity `Modules/CustomerCare/Entities/WrAssignTask/*` (phiếu + 13 bảng con + ATP 4 bảng + AssemblyRequest(+details) + AssignOtherRequest(+details)); không migration
- [ ] T2 Seeder: 3 quyền type 24 `Xem phiếu giao việc theo tổng công ty/công ty/phòng ban` → `permission:sync --dry-run`
- [ ] T3 `WrAssignTaskService`: list (phạm vi 3 type + quyền 3 cấp + lọc 10 ô + sort) · present (cờ hành động) · show (getForShow + canView) · delete (Hủy + dọn tiến độ + sửa lỗi) · lịch sử
- [ ] T4 Controller + route `/v1/customer-care/wr-assign-tasks` (meta, index, export, print, show, destroy) + `ExportColumnRegistry::wr_assign_tasks`
- [ ] T5 Smoke test HTTP kernel: so tập id danh sách với thuật toán ERP chép nguyên (vài NV), show, delete trên bản ghi test (khôi phục)

## Phase 2 — BE tạo phiếu (hrm-api)
- [ ] T6 `WrAssignTaskSourceService`: source-data 3 nguồn (port getForAssignTask / getDataAssignTask) + hàm SL đang giao từ ATP (dùng chung)
- [ ] T7 FormRequest + `WrAssignTaskStoreService::store` (port store, 1 transaction, sửa lỗi BH 500) + route `GET /source-data`, `POST /`
- [ ] T8 Smoke test: source-data so với ERP (cùng HĐ/YC), store trên dữ liệu test rồi xoá theo id

## Phase 3 — FE (hrm-client)
- [ ] T9 `pages/customer-care/wr-assign-tasks/index.vue` (danh sách, 2 lối vào ?type=) + Lịch sử popup + In + Xuất + Cấu hình cột
- [ ] T10 `WrAssignTaskForm.vue` + bảng con (BH, SC, BD, Lắp đặt, Dịch vụ đính kèm, Bán thêm, P3, Tổng hợp) dùng cho create + chi tiết
- [ ] T11 `create.vue` + `_id/index.vue` (footer, Xóa, link ERP, SystemInfoSection)
- [ ] T12 Menu CSKH sau bán › Giao việc (2 mục) + nút Tạo PGV ở màn chờ → HRM + link mã PGV ở Phiếu công tác
- [ ] T13 Verify compile + grep tự kiểm skill erp-to-hrm-screen

## Phase 4 — Vá lỗi ERP (repo erp, nhánh gop_db)
- [x] T14 Vá các lỗi spec mục 8 (controller store/delete, model getForShow, JS removeWorkP3 / note / bảng III / ghi chú show) — 10/10, `php -l` sạch
  - tách `AssemblyRequest::refreshAssignStatus()` dùng chung cho store / update / delete (delete hết đặt cứng "Chờ giao việc")
  - ⚠️ sửa lỗi 500 nhánh chặn BH ⇒ phép kiểm "còn SL bảo hành để giao" nay chạy thật (trước đây HĐ BH đã từng giao đều 500)
  - chưa kiểm trên trình duyệt ERP (8 điểm cần user bấm — xem báo cáo)

### Checkpoint — 2026-10-31 (wrap up)
Vừa hoàn thành: khảo sát + spec/design + 6 quyết định user chốt; Phase 4 vá 10 lỗi ERP (repo erp `gop_db`, chưa commit, chưa bấm thử trình duyệt)
Đang làm dở: Phase 1 BE (T1–T5) — agent đang chạy ở hrm-api, đã sinh: `Modules/CustomerCare/Entities/WrAssignTask/`, `Services/WrAssignTaskService.php`,
  `WrAssignTaskRemainingService.php`, `WrAssignTaskPrintService.php`, `Http/Controllers/V1/WrAssignTaskController.php`; sửa `Routes/api.php`, seeder quyền,
  `ExportColumnRegistry`, `CatalogHistoryService::TABLES` — CHƯA nghiệm thu, chưa smoke test xong
  ⛔ User bảo dừng 31/10 → agent Phase 1 đã DỪNG giữa chừng (đang ở bước smoke test list/show; chưa test delete). `php -l` sạch toàn bộ file;
  DB không có bản ghi test sót. Script test dở ở scratchpad session: pgv_lib.php, pgv_list.php, pgv_show.php, pgv_totals.php
Bước tiếp theo: (mai) rà code Phase 1 agent để lại (đối chiếu spec mục 3–4, 6) → chạy lại smoke test list/show/delete → nhận kết quả Phase 1 → kiểm smoke test (so tập id với ERP) → Phase 2 (source-data + store) song song FE T9 danh sách → T10–T13
Blocked:

