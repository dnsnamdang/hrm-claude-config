# Plan — Phiếu giao việc CSKH (ERP → HRM) — @khoipv

## Phase 0 — Khảo sát
- [x] Khảo sát ERP: danh sách / phạm vi / hành động (controller + model searchByFilter)
- [x] Khảo sát ERP: form tạo (blade + class JS) — 3 agent song song (form · BE lưu · hiện trạng HRM)
- [x] User chốt 6 quyết định (spec mục 0)
- [x] Viết spec + design

## Phase 1 — BE danh sách / chi tiết / xóa (hrm-api)
- [x] T1 Entity `Modules/CustomerCare/Entities/WrAssignTask/*` — 24 file: WrAssignTask + 13 bảng con + ATP 4 bảng + AssemblyRequest(+Detail) + AssignOtherRequest(+Detail); `$fillable` theo ERP, bỏ cột ERP khai mà bảng không có (`customer_code` phiếu, `unit_*` dòng thiết bị, `total` YC GVK); không migration
- [x] T2 Seeder: 3 quyền type 24 group "Phiếu giao việc" (cạnh khối Phiếu chờ giao việc) → `permission:sync --dry-run`: thêm 3 (+3 quyền HDDV của nhánh khác đang chờ) — CHƯA sync thật
- [x] T3 `WrAssignTaskService` (list/present theo lô/show/canView/delete/lịch sử) + `WrAssignTaskRemainingService` (dùng chung theo chủ đề: SL đang giao lắp đặt, tính lại trạng thái YC lắp đặt, `canAssignTaskWarranty`) + `WrAssignTaskPrintService`; đăng ký `wr_assign_tasks` vào `CatalogHistoryService::TABLES`
- [x] T4 `WrAssignTaskController` + route `/v1/customer-care/wr-assign-tasks` (meta, index, export, export-rows, print, show, destroy) + `ExportColumnRegistry::wr_assign_tasks` (11 cột)
- [x] T5 Smoke test HTTP kernel (scratchpad `pgv_*.php`) — kết quả dưới

### Kết quả smoke test T5 — 02/11/2026
- **Danh sách = ERP 100%**: so TẬP id với bản chép nguyên `searchByFilter` (pluck mảng như ERP) — 6 cấu hình × 3 type × 14 bộ lọc (10 ô + kết hợp), FAIL = 0:
  NV 13 Super admin all 7.745 · NV 240 (executor) all 583 / chờ nhập KQ 583 · NV 240 ép quyền công ty 7.231 · NV 240 ép quyền phòng ban 0 · NV 242 all 4.352 / chờ nhập KQ 13 / index 4.341 · NV 364 ép phòng ban all 2.425 / index 1.222.
  (3 quyền mới chưa sync → nhánh công ty/phòng ban test bằng ép cờ ở lớp con test, cả 2 phía dùng cùng cờ.)
- Phân trang (p1/p2 không trùng, total/lastPage đúng), trang 1 đúng thứ tự ERP `created_at desc`; sort 5 cột × asc/desc đúng. Thời gian/trang 20 dòng: 120–360 ms (lần đầu có boot ~1 s).
- Cờ hành động (nhập KQ, xóa, xem phiếu nhập KQ + id, xem phiếu duyệt KQ + id) so với tính từng dòng kiểu ERP: 4 lượt × 60 dòng, khớp hết.
- Show: 5 type → 200 (~250 ms); NV 240 phiếu không liên quan → 403; phiếu con / phiếu đã hủy / id không có → 404. Tổng công định mức BE so giá trị lưu: 481/491 khớp — 10 lệch 0,02–0,13 đều là lắp đặt cũ (cột `wr_assign_task_assembles.rate_effort` double(8,2) lưu đã làm tròn, ERP show cũng ra như HRM).
- Delete trên dữ liệu test tự INSERT (dọn theo id, còn sót 0): GVK → 9 + YC GVK về 1 + xoá ATP + log "Chờ thực hiện → Hủy"; gọi lại → 409; lắp đặt → YC tính lại 5 (còn PGV khác giao đủ) / 1 (còn SL), ATP 1 dòng trả về REQUEST_TASK, ATP 2 dòng thì xoá; BH → xoá 4 loại ATP + `is_assign` tính lại = 1; phiếu đã có PCT → 409; NV khác → 403; id lạ → 404.
- Export `/export` (DynamicExport) 200 nhưng **20 s / 825 dòng, 59 s / 7.745 dòng** (sát `max_execution_time` 60 s) → thêm `/export-rows` (FE dựng file, list-page 14c): 2–4,5 s / 2.000 dòng, ô "Tổng công định mức" là số. Print 200: 825 dòng 1,7 s; 7.745 dòng → `truncated=true` (trần 2.000).
- `laravel.log` không có lỗi mới.

### Checkpoint — 02/11/2026 09:10
Vừa hoàn thành: Phase 1 (T1–T5) BE danh sách / chi tiết / xóa / in / xuất
Đang làm dở: —
Bước tiếp theo: Phase 2 T6 `source-data` (mở rộng `WrAssignTaskRemainingService`), hoặc FE T9 dùng `/export-rows` thay `/export`
Blocked: 3 quyền mới chưa sync DB (chờ deploy / admin gán)

## Phase 2 — BE tạo phiếu (hrm-api)
- [x] T6 `WrAssignTaskSourceService` (mới): source-data 3 nguồn, port `getForAssignTask` / `AssemblyRequest|AssignOtherRequest@getDataAssignTask` + mặc định class JS ERP (qty = SL còn, ĐM công `recipe_work_norm || 0`, hệ số `benefit_coefficient || 1`, bảo dưỡng `quota_work || 1`, bán thêm qty 0) — JSON cùng khuôn `show` + `available_qty` / `source_id`; quyền y `canAssignTask` (403 "Không có quyền!"), HĐ gọi `checkCreate` (422)
  - `WrAssignTaskRemainingService` (+): SL đang giao SC / BH (thiết bị, dịch vụ, vật tư), bảo dưỡng (`extendAssignedData` + 3 hàm đọc), bán thêm; `assemblyAssigningQtyMap` (1 query / YC — bảng không index, gọi lẻ 25 ms/dòng) dùng cho cả `recalcAssemblyRequestStatus` (Phase 1)
  - `WrAssignTaskService`: `people()` / `totals()` → public, thêm `logCreated()`
  - ⚠️ `|| 1` của JS với cột DECIMAL: về JS là chuỗi → "0.00" vẫn truthy → giữ 0 (hệ số lắp đặt `tech_coefficient` 0 ở 11.224 SP)
- [x] T7 `Http/Requests/WrAssignTask/WrAssignTaskStoreRequest` (rule ERP WithPlace bỏ khối chết + định dạng SL/ĐM công; `withValidator` gom lỗi vượt SL cùng lượt) + `WrAssignTaskStoreService::store()` (1 transaction, khoá chứng từ nguồn, dựng dòng từ nguồn — FE chỉ đổi SL / ghi chú / ĐM công GVK / P3; ATP 5 nhánh; YC lắp đặt tính lại trạng thái; GVK → 2; BH `is_assign`; lịch sử "Tạo mới") + route `GET /source-data`, `POST /` (`checkPermission:Tạo phiếu giao việc` + `dueConfig:Tạo phiếu giao việc,manager`)
- [x] T8 Smoke test (scratchpad `pgv2_*.php`) — kết quả dưới

### Kết quả smoke test T8 — 02/11/2026
- **source-data = ERP 100%** (bản chép nguyên `getForAssignTask` / `getDataAssignTask` chạy cùng DB, so từng dòng: tập dòng, `available_qty`, `qty` mặc định, ĐM công, hệ số, `worker_qty`):
  lấy từ màn chờ: HĐ 40 (33 còn dòng, 71 dòng cấp 1) · PL 22 (14 dòng) · BH 40 (50 dòng) · LĐ 40 YC (235 dòng) — FAIL 0;
  lấy mới nhất: HĐ 60 · PL 30 · BH 60 · LĐ 60 YC (309 dòng) · GVK 20 — FAIL 0 (lần đầu LĐ lệch 3 YC ở hệ số 0 → đã sửa theo JS truthy).
- **store 6 phiếu** (HĐ có bảo dưỡng · PL có vật tư · HĐ có 9 dòng bán thêm · BH · LĐ 53 hàng · GVK 3 dịch vụ) trong `DB::beginTransaction` → rollBack:
  số dòng 13 bảng con + ATP (theo request_type/type) + tiến độ dịch vụ / vật tư / vật tư bảo dưỡng = kỳ vọng theo store ERP — KHỚP 6/6 (đối chiếu thêm cấu trúc PGV ERP thật mỗi type: HĐ chép 5 chi phí, bán thêm lưu cả dòng qty 0, LĐ 1 ATP/hàng);
  mã `TPE.PGV.2026{id 6}`, type đúng nguồn, công ty / phòng người tạo, `sum_amount_rate_effort` = totals + P3 (+ ĐM GVK), `places = "null"`, `product_export_requests = "[]"` như ERP;
  LĐ: 53 ATP mới (đã có ≥ 2 dòng / dòng đã gắn PGV → thêm), YC 1 → 5; GVK 1 → 2; BH `is_assign` 1 → 0; lịch sử "create".
  Gọi lại nguồn sau khi tạo: SL còn giảm đúng 77/77 dòng. Thời gian store 40–900 ms (LĐ 53 hàng 7 s → 0,3–0,5 s sau khi gom query), source-data 16–600 ms.
- **422**: thiếu hết → 6 key "Bắt buộc phải nhập" (+ chứng từ nguồn); ngày quá khứ / kết thúc < bắt đầu → 2 câu nguyên văn ERP; d/m/Y → "Định dạng không hợp lệ";
  vượt SL `product_repairs.0.qty` / `product_repairs.0.services.0.qty` / `merchandises.1.qty` "Giá trị nhập vào không được vượt quá N." CÙNG lượt với SL âm + P3 thiếu tên/ĐM; dòng không có trong nguồn → vượt quá 0;
  lưu 1 phần rồi lưu lại payload cũ → vượt quá 0 đúng 3 dòng; BH đã giao hết → 422 "Không có sản phẩm bảo hành để giao" (message); PL giảm chờ duyệt → 422 cả source-data lẫn store.
- **403 / 409 / 404** (NV 240 phòng 50, mỗi vai 1 tiến trình, quyền qua role tạm theo công ty — rollback): không quyền → source-data HĐ/BH 403 "Không có quyền!", LĐ/GVK phòng mình 200 (ERP không đòi quyền), POST 403 middleware;
  có quyền → HĐ phòng mình 200 + store 200 (created_by 240, phòng 50), HĐ / LĐ phòng khác 403 (kể cả payload vượt SL — không lộ SL); GVK đã giao → source 403 / store 409; id lạ 404; thiếu tham số 422.
- Dọn: không còn bản ghi test (PGV / ATP / lịch sử / role tạm / PL giảm tạm = 0, nguồn giữ trạng thái cũ); auto-increment `wr_assign_tasks` bị tiêu id 14583–14623 (rollback). `laravel.log` không có dòng mới.

### Checkpoint — 02/11/2026 (Phase 2 BE xong)
Vừa hoàn thành: T6–T8 BE tạo phiếu (source-data + store) + smoke test
Đang làm dở: —
Bước tiếp theo: FE T9–T11 (form dùng chung create/show: đọc `GET /source-data`, gửi JSON body y ERP submit_data + `source_id` mỗi dòng, map 422 theo key)
Blocked: ~~quyền "Tạo phiếu giao việc" chặn POST cả nhánh LĐ/GVK~~ → user chốt 02/11 "y ERP, kiểm theo loại": bỏ `checkPermission` ở route POST, StoreService kiểm theo loại (giữ `dueConfig`)

## Phase 3 — FE (hrm-client)
- [x] T9 `pages/customer-care/wr-assign-tasks/index.vue` (danh sách, 2 lối vào ?type=) + Lịch sử popup + In + Xuất + Cấu hình cột (02/11)
  - Đã bám `warranty-repair-handle-requests/index.vue` ở khối vỏ trang + filterStateMixin + Xuất `exportListFile` (/export-rows) + In (`reportPrintPreviewMixin` + `ReportPrintPreviewModal`, xử lý `truncated`) + popup Lịch sử `CatalogHistoryModal`; bám `waiting-assign-tasks/components/WaitingAssignTaskList.vue` ở khối lọc Khách hàng `V2BaseSelectRemote` 32px, link HĐ bán ERP qua `contractLink(FirmContract)`, phân trang chống lỗi b-pagination (`requestedPage` + `loadSeq`), `openErp` cho nút sang ERP; toolbar bám `assign/customers` (`V2BaseIconButton` Cấu hình cột)
  - 3 lối vào → khoá riêng `wr_assign_tasks_all` / `_waiting_import_result` / `_index` (localStorage + cấu hình cột + cài đặt bộ lọc); watcher `$route.query.type` → `switchScope()` (bỏ lọc lối cũ, nạp lọc + cột lối mới)
  - Cột y spec 3.2 (hiện hết), sort code / expected_time_text / sum_amount_rate_effort / status / created_at; 8 ô lọc nâng cao (Thời gian dự kiến gộp 1 ô khoảng ngày) + tìm nhanh số phiếu; hành động Nhập KQ · Xóa · Xem phiếu nhập KQ · Xem phiếu duyệt KQ · Lịch sử
  - Verify: vue-template-compiler + babel OK; grep tự kiểm skill sạch (còn fallback lỗi "Xóa không thành công" khớp câu BE). Chưa mở trình duyệt
- [x] T10 `WrAssignTaskForm.vue` + bảng con (BH, SC, BD, Lắp đặt, Dịch vụ đính kèm, Bán thêm, P3, Tổng hợp) dùng cho create + chi tiết (02/11)
  - `components/`: `WrAssignTaskForm.vue` (khối Thông tin KH + 2 chế độ create/show + validate + lưu + xoá + footer + Lịch sử) ·
    `WrAssignTaskDeviceTable.vue` (A - BẢO HÀNH và I - Dịch vụ sửa chữa, prop `listKey`, SC khoá ô khi `available_qty <= 0`) · `WrAssignTaskMaintainTable.vue` (II + Tổng I+II) ·
    `WrAssignTaskAssemblyTable.vue` · `WrAssignTaskRevenueCostTable.vue` · `WrAssignTaskMerchandiseTable.vue` · `WrAssignTaskP3WorkTable.vue` · `WrAssignTaskSummarySection.vue` (I/II/III/V) ·
    `WrAssignTaskNumberCell.vue` (ô số tách component — gõ phím không vẽ lại cả bảng) · `wrAssignTaskCalc.js` (công thức getter ERP + gộp bảng II/III) · `wrAssignTaskLinks.js` (link nguồn HRM/ERP, URL ERP Nhập/Xem KQ, hằng URL)
  - Đã bám `warranty-repair-handle-requests/components/WarrantyRepairHandleRequestForm.vue` ở khối vỏ form (`V2BaseFormSection` + `CreatorInfoLine` #actions, `.v2-linked-field`, `V2Footer` #custom-actions, `SystemInfoSection catalog-histories`, `$safeLoading*`, 404 chi tiết) ·
    `wr-service-contracts/components/WrContractLinesTable.vue` ở bảng thiết bị nhiều tầng (dòng đầu thiết bị đậm + dòng phụ xám, i.1/i.2/i.3, dòng tổng nền `#f8fafc`, `sourceLabel` tp/tpc/ncck) ·
    `bill-adjust-depts/components/AccountingDetailTable.vue` ở nút "Thêm dòng" · `finance/borrow-sell-requests/_id/index.vue` ở tiêu đề `buildStatusTitle` · `finance/borrow-export-requests/_id/index.vue` ở `beforeRouteEnter` (Quay lại về nơi đi vào)
  - Validate FE = BE (`WrAssignTaskStoreRequest`): ngày bắt buộc / ≥ hôm nay / kết thúc ≥ bắt đầu (câu ERP) + `disabled-date` trên lịch · P3 tên + ĐM công bắt buộc · SL ≤ SL còn (báo đỏ realtime, không tự kéo về) · ghi chú dòng / tên công phụ ≤ 255 · SL cột `int` chỉ nhận số nguyên. Mọi lỗi cùng lúc + `scrollToFirstError`; 422 map đúng khoá, khoá không có ô (dữ liệu chép từ nguồn) → toast nói rõ thiếu gì
  - Sửa lỗi ERP phía FE: xoá đúng dòng P3 (truyền index + `removeRowErrors`), gửi `note` cấp thiết bị, bảng III là computed (đổi SL bán thêm cập nhật), Ghi chú khoá ở chi tiết; bảng II tách khoá `cost:` / `service:` (ERP gộp chung 1 khoá → `cost_id` trùng số `service_id` bị cộng nhầm); sửa typo "trền" / "Modle"
  - Đối khớp key: gọi thật `source-data` (YC lắp đặt 1441, YC GVK 2627, HĐ 6780, PL 6760 — Super admin, chỉ GET) + `show` 5 type → `computeTotals()` FE = `totals` BE ở cả 8 mẫu
- [x] T11 `create.vue` + `_id/index.vue` (footer, Xóa, link ERP, SystemInfoSection) (02/11)
  - create: query nguồn sai/thiếu → `/pages/extras/404`; lỗi source-data → toast câu BE + về màn chờ đúng tab; "Lưu & duyệt" (validate → `$confirm` → POST → `markFormSaved` → toast "Tạo phiếu giao việc thành công." → chi tiết phiếu mới); Quay lại → màn chờ `?tab=` theo nguồn
  - chi tiết: tiêu đề "Chi tiết phiếu giao việc: {code}" + badge trạng thái; Nhập KQ / Xem phiếu nhập KQ / Xem phiếu duyệt KQ (ERP tab mới, cùng cờ danh sách) · Xóa (`$confirm` → DELETE → "Xóa thành công." → `?type=all`, 409 toast câu BE) · Quay lại về nơi đi vào. Không nút Sửa
  - Verify: vue-template-compiler + babel OK 13 file; grep tự kiểm skill sạch. CHƯA mở trình duyệt, CHƯA POST thật
- [x] T12 Menu CSKH sau bán › Giao việc (2 mục) + nút Tạo PGV ở màn chờ → HRM + link mã PGV ở Phiếu công tác (02/11)
  - `subsystem-menu/customer-care.js` (+2 mục, giữ `?type=` ERP) · `WaitingAssignTaskList.vue::openCreateAssignTask` → `$router.push` form HRM
  - `assign/assign_business/index.vue::generateLink` mã `TPE./TPSG.PGV.` → `/customer-care/wr-assign-tasks/{id}` (bỏ import `ERP_URL` thừa)
  - ⚠️ form HRM chưa dựng (T10/T11) → tới lúc đó nút Tạo PGV ở màn chờ ra 404
- [x] T13 Verify compile + grep tự kiểm skill erp-to-hrm-screen (02/11): 14 file .vue + 3 file .js compile OK; bộ grep skill sạch trên cả thư mục; `php -l` sạch toàn bộ BE
  - ⚠️ CHƯA mở trình duyệt; CHƯA POST/DELETE thật qua FE; 3 quyền mới chưa `permission:sync` thật ở local

- [x] T15 Playwright local (02/11) — script `scratchpad/pw_pgv.js` (có cửa sổ, khung bước trên trang, log `pw_pgv_out/progress.log`), NV 13 Super admin
  | Nhóm | PASS | FAIL | SKIP | Ghi chú |
  |---|---|---|---|---|
  | A Danh sách `?type=all` | 30 | 0 | 1 | menu hub (tìm chức năng) đúng; 13 cột "Người tạo"; 1 request khi vào / tìm nhanh / trang 2 / đổi số dòng; 7 ô lọc + Làm mới; sort 5 cột asc↔desc; Cấu hình cột; Xuất Excel 7.749 dòng đúng heading; In có bảng; Lịch sử; link Số phiếu → chi tiết → Quay lại giữ lọc. SKIP Người thực hiện (dòng đầu trống — lượt trước PASS). Ô "Thời gian dự kiến": chọn 2 ngày lên đúng, request gửi cả 2 tham số chưa xác nhận lại (Nuxt chết giữa chừng) |
  | B `?type=waiting_import_result` | 5 | 0 | 0 | tiêu đề đúng, bộ lọc tách riêng, chuyển lối 1 request |
  | C Chi tiết type 1–5 + phiếu LĐ mới | 13 | 0 | 0 | đúng khối, ô khoá, không nút Sửa, có Lịch sử, tiêu đề "Chi tiết phiếu giao việc: …", Tổng công ĐM form = danh sách; id lạ → `/pages/extras/404` |
  | D Tạo từ màn chờ (HĐ, PL, BH, LĐ, GVK) | 5/5 nguồn lưu được | 0 | — | lỗi đỏ 2 ô ngày + không POST; SL vượt → "Giá trị nhập vào không được vượt quá 1."; P3 thêm 2 xoá dòng 1 còn dòng 2; lưu → toast → chi tiết; DB số dòng bảng con = form, ATP đúng (HĐ 7 · PL 1 · BH 1 type 5 · GVK 1 type 6 · LĐ gắn ATP sẵn có), BH `is_assign` 1→0, LĐ 1→5, GVK 1→2; phiếu mới đầu danh sách |
  | E Xóa + cảnh báo chưa lưu | 7 | 0 | 0 | xoá từ danh sách + từ chi tiết: popup → "Xóa thành công." → biến mất; DB 9, GVK về 1, LĐ về 1 (ATP trả REQUEST_TASK); Quay lại khi đã đổi ngày → popup "Thông tin chưa lưu" |
  | F Phiếu công tác | — | — | 1 | Nuxt dev chết trước bước này → chỉ đọc code: `generateLink` trỏ `/customer-care/wr-assign-tasks/{id}` cho `TPE.`/`TPSG.PGV.` — ⚠️ bỏ sót tiền tố công ty khác (DB có `TPV.PGV.…`) → rơi xuống link `/assign/job_requests` |
  - Không lỗi console / API ≥ 400 do feature; `laravel.log` không có dòng mới
  - ⚠️ Môi trường: renderer Chromium crash 3 lần sau ~20 bước dài (sau Xuất Excel 7.749 dòng dựng trên trình duyệt + In), cuối cùng tiến trình Nuxt dev :3000 chết hẳn (ERR_CONNECTION_REFUSED, không còn node) — chưa khởi động lại
  - Dữ liệu: tạo 5 phiếu 14624–14628 → đã xoá cứng theo id (+ 9 ATP, 7 dòng `catalog_histories`), khôi phục nguồn; snapshot trước/sau khớp 100% (`scratchpad/snap_before.txt` = `snap_after.txt`)
- [x] T16 User yêu cầu (02/11): màn Chi tiết bỏ ô "Trạng thái" trong khối Thông tin khách hàng (trạng thái đã có ở badge tiêu đề) — `WrAssignTaskForm.vue` (+ bỏ import `V2BaseBadge`, CSS `.wr-at-status`); compile OK, đã thấy trên trình duyệt
- [x] T17 `assign/assign_business/index.vue::generateLink` nhận mọi `{cty}.PGV.` bằng `/^[A-Z0-9]+\.PGV\./` (vd `TPV.PGV.…`) — chính dòng mình sửa ở T12 nên sửa luôn (02/11); compile OK, chưa bấm trên trình duyệt (Nuxt chết)
- [x] T18 Commit + push `develop` (02/11, user yêu cầu): hrm-api `4053ab27c`, hrm-client `50491b5bc` (pull --rebase trước khi push; KHÔNG kèm 2 file Phiếu xuất kho đang sửa dở: `InventoryExportWriteService.php`, `InventoryExportForm.vue`)

### Checkpoint — 02/11/2026 (hoàn thành)
Vừa hoàn thành: test Playwright A–E + push 2 repo
Đang làm dở: —
Bước tiếp theo: `php artisan permission:sync` thật cho 3 quyền xem; commit repo ERP Phase 4 khi user yêu cầu
Blocked:

### Checkpoint — 02/11/2026 (code xong, chờ user test trình duyệt)
Vừa hoàn thành: Phase 1–4 code xong (BE list/show/delete/print/export + source-data/store; FE danh sách + form create/show; menu + nối màn chờ; vá ERP)
Đang làm dở: —
Bước tiếp theo: chạy `php artisan permission:sync` ở local + gán 3 quyền xem cho role cần test → user mở trình duyệt test luồng: màn chờ → Tạo PGV → chi tiết → danh sách → Xóa; ERP: 8 điểm bấm thử
Blocked:

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


## Redmine #11978 — Tạo phiếu giao việc (tab Giao việc khác): nút + required + thiếu Lưu / Lưu và tiếp tục (2026-11-02, @khoipv)
- [x] Nút "Lưu & duyệt" → khuôn nút "Lưu và duyệt" của `finance/inventory-exports` (icon `ri-checkbox-circle-line` 15px, chữ
      "Lưu và duyệt"; popup xác nhận đổi chữ theo) — `WrAssignTaskForm.vue`
- [x] Dấu * (màn Tạo, `V2BaseLabel :required="!readonly"`): mọi ô chứng từ nguồn (Phiếu YC giao việc khác / HĐ / PL / phiếu BH /
      YC lắp đặt / HĐ bán) + Khách hàng + Người liên hệ — đúng ERP `form.blade.php` (`required-label`). Màn chi tiết không hiện *
- [x] Verify: vue-template-compiler + babel sạch
- [x] "Lưu" + "Lưu và tiếp tục": KHÔNG thêm — user chốt 02/11 (giữ 1 nút như ERP, trả lời QA) — `wr_assign_tasks` (HRM + ERP) không có trạng thái nháp (1 Chờ thực
      hiện … 9 Hủy), Lưu = tạo phiếu đã duyệt ngay (sinh ATP, đổi trạng thái chứng từ nguồn: GVK 1→2, LĐ 1→5, BH is_assign 1→0);
      spec mục 8 đã chốt không có nháp / tiếp tục. Thêm nháp = trạng thái mới trên DB chung (ERP chưa hiểu) + màn Sửa (chưa port)
      + dời mọi tác động phụ sang lúc duyệt
- [ ] Chưa kiểm trên trình duyệt (user tự mở)

## Redmine #11980 — Phiếu giao việc: sort Trạng thái · lịch sử trống · Nhập kết quả lỗi · lọc Người yêu cầu (2026-11-02, @khoipv)
- [x] Bỏ sort cột Trạng thái: FE `index.vue` bỏ `sortable` · BE `WrAssignTaskService::SORTABLE` gỡ `status`
- [x] Lọc Người yêu cầu rỗng: BE chỉ lọc người tạo HĐ/BH/PL (y lỗi ERP) trong khi cột hiển thị lấy HĐ → YC giao việc khác → YC
      lắp đặt (`presentBase`) ⇒ phiếu từ YC lắp đặt (vd TPE.PGV.2026017772 / TPV.YCLĐBG.2026001755) lọc ra rỗng. Sửa
      `filteredQuery()` lọc theo CÙNG thứ tự. Verify: 4 người yêu cầu (có người tạo YC lắp đặt, YC GVK) — tập phiếu lọc ra = tập
      phiếu cột hiển thị tên đó (33/33 · 59/59 · 52/52 · 0/0)
- [x] Lịch sử trống (CHECK, chưa sửa): local ghi + đọc đúng (logCreated → catalog_histories → API 200 có dòng "Tạo mới").
      Dev: 18699 (14:49, sau push 13:59) và 18698 (09:40, TRƯỚC push ⇒ tạo từ ERP, ERP không ghi catalog_histories) đều rỗng.
      Chưa xác định 18699 tạo từ HRM hay ERP (2 bên ghi giống hệt cột) — nhờ QA tạo 1 phiếu MỚI từ HRM rồi xem lịch sử.
      Phiếu tạo từ ERP / trước khi port sẽ không có lịch sử (như các màn port khác)
- [x] Nhập kết quả lỗi (user gửi lỗi 02/11: ERP `wr_import_results/create?wr_assign_task_id=18697` → "Trying to get property
      'code' of non-object"): PGV 18697 trỏ `customer_id = 42247` không còn trong `customers` (HRM hiện tên trơn, không mã).
      Vá repo ERP (nhánh `develop_02`, CHƯA commit) `WrAssignTask::getForDataImportResult()`: `optional($task->customer)->code ?? ''`
      + `optional()` 10 chỗ `->product->product_type/group_id` (hàng bị xoá cũng nổ y vậy). Verify tinker: trỏ customer_id sang
      KH không tồn tại (transaction + rollback) — bản cũ NOTICE đúng câu lỗi tại dòng 1905, bản vá render view create sạch
- [ ] (ghi chú cũ) Nút Nhập kết quả: KHÔNG sửa ở đây — nút đang trỏ ERP `wr_import_results/create`; feature phieu-nhap-ket-qua T13 (đang làm
      dở, chưa commit) chuyển nút sang màn HRM `/customer-care/wr-import-results/create` — sửa cùng `index.vue`, tránh đè
- [x] Verify: `php -l` · vue-template-compiler + babel sạch. Chưa kiểm trên trình duyệt

## Redmine #11988 — Form Tạo phiếu giao việc: placeholder · số liệu lệch ERP · dấu * · in đậm Mã hàng (2026-11-03, @khoipv)
Mục 3-5 của #11988 (mục 1-2 ở `.plans/gop-db/phieu-cho-giao-viec/plan.md`).
- [x] Mục 3 — Placeholder 7 ô số còn thiếu (`WrAssignTaskNumberCell`): SL bàn giao ("Nhập SL bàn giao"), SL thiết bị / dịch vụ /
      vật tư (bảng BH-SC), SL gói + hàng bảo dưỡng, SL vật tư bán thêm ("Nhập số lượng"). Ô chọn ngày / ghi chú đã có sẵn
- [x] Mục 4 — Định mức công hiện 1.3 / 0.02, ERP 1.302 / 0.019 → hiện đủ số lẻ như ERP; thêm (*) đỏ: Phiếu YC lắp đặt bàn giao,
      Hợp đồng, Khách hàng, Người liên hệ, cột Hàng hóa (như ERP)
- [x] Mục 5 — In đậm nhãn "Mã hàng:" dưới tên hàng (ERP `<b>Mã hàng:</b>`)
      → Định mức công bảng lắp đặt dùng `fmtRaw` mới (số thô, ERP không qua filter); dấu * 4 ô đầu form ĐÃ có từ commit
      `a9100f111` (02/11 16:52 — sau lúc QA chụp 16:01), chỉ cần deploy; thêm * cột "Hàng hóa" (lắp đặt) + "Tên vật tư" (vật tư bán thêm) như ERP
      → "Mã hàng:" in đậm ở bảng lắp đặt, bảo dưỡng, khối tổng hợp
- [x] Verify: vue-template-compiler + babel sạch. Chưa kiểm trên trình duyệt
- Ghi chú (chưa sửa, QA chưa báo): ĐM công bảng BH / sửa chữa ERP dùng filter `number` (3 số lẻ: 0.019), HRM `fmt` 2 số lẻ (0.02)

## Redmine #11984 — PGV thiếu lọc Công ty/Phòng ban · placeholder · tạo xong về danh sách · validate từ chối tiếp nhận (2026-11-03, @khoipv)
- [x] Bug 1 — Danh sách PGV thiếu bộ lọc Công ty, Phòng ban dù tài khoản có quyền (ERP KHÔNG có ô này — QA yêu cầu thêm):
      BE `WrAssignTaskService::meta()` trả `scope` {is_all_company, is_company, is_department} theo 3 quyền xem; `filteredQuery()`
      lọc thêm `company_id` / `department_id` (trong phạm vi `applyScope`, không nới quyền — in / xuất dùng chung query).
      FE `index.vue` ô `org` (`V2BaseCompanyDepartmentFilter`, khuôn warranty-repair-handle-requests) chỉ ở lối vào `?type=all`
      khi có ≥1 quyền; `scopeFlags` mặc định false (fail-closed); `inputCount` 2/1 theo is_all_company
- [x] Bug 2 — Tạo PGV từ tab Hợp đồng: placeholder các ô nhập (SL giao lần này bảng sửa chữa) — đã làm trong #11988 mục 3
- [x] Bug 3 — Tạo PGV xong quay về màn DANH SÁCH `?type=all` như ERP `create.blade.php` (trước: mở chi tiết) — `WrAssignTaskForm.vue` save()
- [x] Bug 4 — Popup Từ chối tiếp nhận xử lý (màn chờ, tab HĐ + PL bổ sung): `$confirm` thêm `requiredInput` → dấu * + lỗi đỏ dưới ô,
      popup không đóng khi trống (trước: đóng popup rồi toast). Áp luôn popup Hủy duyệt HĐ cùng màn (cùng lỗi)
- [x] Verify: `php -l` · HTTP kernel (DNS Admin): meta trả scope đủ 3 cờ; type=all 7745 · company 1 = 7231 · + phòng 51 = 2425
      — khớp đếm DB. FE vue-template-compiler + babel sạch. Chưa kiểm trên trình duyệt

## Redmine #11991 — Danh sách PGV: giãn cột Số hợp đồng, dài thì xuống dòng (2026-11-03, @khoipv)
- [x] `index.vue` `allColumns()`: cột `contract_code` 200px → 260px + `cellClass: 'text-wrap'` (V2BaseDataTable: `white-space: normal`
      + `overflow-wrap: anywhere` — số HĐ nối bằng `_` không có khoảng trắng nên phải bẻ giữa chữ). Link HĐ vẫn giữ nguyên
- [x] Verify: vue-template-compiler + babel sạch. Chưa kiểm trên trình duyệt

## Redmine #11998 — Cột Hành động "Xem phiếu nhập kết quả" mở ERP ra 404 (2026-11-04, @khoipv)
PGV TPE.PGV.2026018146, phiếu nhập KQ id 9116 tạo trên cổng HRM. Ảnh QA: `dev-erp.../admin/customer-care/wr_import_results/9116/show` → 404.
- [x] Điều tra: ERP `WrImportResultsController@show` → `WrImportResult::getForEdit()` dùng `findOrFail($id)` → 404 = DB của dev-erp (suy luận, chưa vào được DB dev để kiểm)
      KHÔNG có dòng 9116 (phiếu tạo ở HRM nằm DB gộp, dev-erp đọc DB khác) — không phải lỗi code ERP
- [x] Phía HRM đã sửa sẵn trong commit `44f138085` (03/11 14:14, đã lên origin/develop + origin/gop_db): `wrAssignTaskLinks.js`
      `importResultShowUrl()` → HRM `/customer-care/wr-import-results/{id}` (trước trỏ ERP `.../wr_import_results/{id}/show`);
      dùng ở cột Hành động (`index.vue:632`) + nút ở form chi tiết (`WrAssignTaskForm.vue:251`). QA chụp 16:05 — bản dev chưa deploy
- [x] Rà toàn hrm-client: không còn chỗ nào trỏ ERP `wr_import_results/{id}/show`. Không sửa code → chỉ cần deploy dev-hrm rồi QA test lại
