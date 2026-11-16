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
- [x] (#11972, 02/11 — còn index chờ chốt) Hiệu năng tab HĐ: ~3,5 s/trang 10 dòng (đếm 1 s + accessor `is_can_close`/`is_can_un_approve` ~110 ms/dòng — bảng `product_export_requests`/`product_import_requests` không có index `wr_service_contract_id`) → chờ user chốt

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

## Redmine #11975 — cột Mã phiếu bị cắt `…`, không đọc hết mã (2026-11-02, @khoipv)
QA: mã HĐ dài (`HDDV_TPE_HN_CSKH_26_0385…`) bị cắt ở mọi tab, yêu cầu giãn cột, dài quá thì xuống dòng.
Nguyên nhân: `COL_CODE` rộng 190px trong bảng `fixed-layout` ⇒ ô `.field-line` bị `overflow: hidden; text-overflow: ellipsis`.
- [x] `tabConfigs.js` `COL_CODE`: width/minWidth 190 → 250px + `cellClass: 'text-wrap'` (td `white-space: normal` +
      `overflow-wrap: anywhere` ⇒ mã không có khoảng trắng vẫn ngắt dòng, không cắt). Áp cả 5 tab (tab Lắp đặt / Giao việc khác
      "Số phiếu" kế thừa qua `COL_REQ_CODE`). Không kẹp 2 dòng (`clamp-2`) vì QA muốn thấy hết mã
- [x] Verify: babel parse sạch; V2BaseDataTable gắn `column.cellClass` lên td (cả cột sticky)
- [ ] Chưa kiểm trên trình duyệt (user tự mở) — cột Số hợp đồng (tab Lắp đặt / Giao việc khác) giữ 190px, chưa đụng

## Redmine #11972 — Performance: chuyển tab tải chậm (2026-11-02, @khoipv)
Đo service (Super admin, 10 dòng/trang) TRƯỚC: Hợp đồng **4,29 s / 163 query** · PL 0,40 s · Bảo hành 0,16 s · Lắp đặt 0,41 s · Khác 0,06 s.
Nguyên nhân chính: tab HĐ gọi accessor `is_can_close` / `is_can_un_approve` của model TỪNG DÒNG — mỗi cờ ~8 query (phụ lục,
PGV, `product_export_requests` 35k dòng / `product_import_requests` 12k dòng KHÔNG có index `wr_service_contract_id` ⇒ quét cả
bảng ~150 ms/lần, `isSuperAdmin()` không cache).
- [x] BE `WaitingAssignTaskService::contractCloseFlags()`: tính 2 cờ cho cả trang bằng 6 query gộp (phụ lục · PGV · YC xuất kho ·
      YC nhập kho · hạch toán DV · phòng quản lý trong công ty), điều kiện Y HỆT accessor (ghi chú: sửa accessor thì sửa cả đây).
      `actionFlags()` đọc từ map này, không gọi accessor nữa. Không đụng model / hàm dùng chung
- [x] Verify khớp accessor: so toàn bộ HĐ của tab — Super admin 400 dòng, người thường (id 59, quản lý phòng) 44 dòng ⇒ 0 lệch
- [x] SAU: Hợp đồng **1,16 s / 24 query** (còn count 0,6 s của lọc "còn số lượng để giao") · PL 0,38 · Bảo hành 0,03 · Lắp đặt 0,23 · Khác 0,02
- [x] FE: đổi tab chỉ gọi meta (hằng, rẻ) + data + cấu hình cột — không thừa, không sửa
- [ ] Chưa làm (chờ user chốt): thêm index cho bảng ERP để hạ tiếp count tab HĐ — `wr_assign_task_products/_product_services/
      _extend_product_services.wr_assign_task_id`, `wr_assign_tasks.wr_service_contract_id`, `product_export_requests` /
      `product_import_requests` / `wr_accounting_service_requests.wr_service_contract_id`
- [ ] Chưa kiểm trên trình duyệt (user tự mở)

## Redmine #11973 — "Số bản ghi các tab không khớp ERP" (2026-11-02, @khoipv) — CHECK, chưa sửa code
QA: số bản ghi tab Hợp đồng, Lắp đặt bàn giao… lệch giữa HRM và ERP dev; ERP dev lỗi "Trying to get property 'code' of
non-object" ở tab PL / BH / Giao việc khác (phần lỗi ERP user báo ĐÃ SỬA — ERP `1ad0620592` thêm optional()).
- [x] Đối chiếu bằng CHÍNH code ERP (repo `develop_02` = origin, đã có fix null) trên cùng DB local `gop_db`:
      DNS Admin (id 13, có quyền xem tổng cty ở cả 2 bên) — HĐ 380=380 · PL 22=22 · BH 405=405 · Lắp đặt 160=160 · Khác 792=792,
      diff từng id = 0. Người thường id 59 (không quyền tổng cty, lọc phòng tiếp nhận) — HĐ 11=11 · PL 0=0 · Lắp đặt 0=0
- [x] `origin/develop` ERP khác `develop_02` ở các file màn này CHỈ phần hiển thị (optional()), điều kiện lọc giống nhau
- [x] Số HRM dev (API dev, DNS Admin): HĐ 462 · PL 24 · BH 561 · Lắp đặt 141 · Khác 930. Chưa lấy được số ERP dev — ERP dev
      đăng nhập SSO qua cookie `jwt_token`, curl không giữ được phiên
- Kết luận: logic HRM = ERP. Lệch trên dev nhiều khả năng do môi trường: ERP dev / HRM dev không cùng DB hoặc dữ liệu,
      hoặc quyền "Xem danh sách phiếu chờ giao việc theo tổng công ty" khác nhau giữa 2 hệ thống (ERP `can()` vs HRM role theo công ty)
- [ ] Chờ QA gửi số ERP dev từng tab (+ 1 mã phiếu có ở bên này mà không có ở bên kia) để chỉ ra đúng dòng lệch

## Redmine #11985 — Tab Phiếu bảo hành › Xem chi tiết (`pages/customer-care/wr-warranties/_id/index.vue`) (2026-11-02, @khoipv)
Màn chi tiết phiếu BH (dev khác làm) mở từ tab BH của màn chờ — sửa theo ERP `wr_warrantys/form.blade.php` (màn show ERP vẫn hiện *).
- [x] Dấu *: Số phiếu cung cấp thông tin · Số phiếu bảo hành · Địa chỉ sửa chữa · Khách hàng · Địa chỉ · Phòng tiếp nhận xử lý ·
      Tên liên hệ · Địa chỉ liên hệ · Điện thoại (`V2BaseLabel required`) + tiêu đề cột bảng A "Chi phí được bảo hành", "Loại công
      việc" (kiểu `<span class="text-danger">*</span>` như cột "Tên chi phí" bảng B đã có). Tài khoản / Ký duyệt / Chức vụ ERP có *
      nhưng màn HRM không có khối đó
- [x] In đậm tên thiết bị + "Serial: …" ở dòng thiết bị bảng A
- [x] Khối C dòng VAT (%): thêm ô `vat_percent` ở cột "Chi phí được bảo hành" (ERP: ô VAT % khoá) — API đã trả `vat_percent`
- [x] Khối D dòng cuối không đậm: HTML có `<strong>` nhưng `_reboot.scss` ép `strong, b` = 500; đoạn soạn bằng Times New Roman
      không có nét 500 ⇒ hiện chữ thường. Scoped `.footer-html ::v-deep strong, b { font-weight: 700 }`
- [x] Verify: vue-template-compiler + babel sạch. Chưa kiểm trên trình duyệt
- Ghi chú (chưa sửa, QA chưa báo): điều khoản còn nguyên chuỗi `{{VAT_NOTE}}` chưa thay — cả ERP cũng hiện vậy

## Redmine #11988 — Xuất Excel các tab · In tab Lắp đặt bàn giao (2026-11-03, @khoipv)
Mục 1-2 của #11988 (mục 3-5 là form Tạo PGV → ghi ở `.plans/gop-db/phieu-giao-viec/plan.md`).
- [x] Mục 1 — Xuất Excel 5 tab: banner (ảnh `info-tpe.jpg` HTML reader chèn đúng 1600px gốc) rộng hơn bảng → giãn banner bằng
      đúng bề rộng bảng. Lớp con `Modules/Assign/Exports/WaitingAssignTaskExport` (khuôn `WarehouseCatalogExport::stretchBanner`),
      KHÔNG sửa `DynamicExport` dùng chung
- [x] Mục 2 — Tab Lắp đặt bàn giao › In: đang mở tab ERP `assembly_requests/{id}/print` → popup `$printPreview({ url })`.
      BE `GET assign/waiting-assign-tasks/assembly/{id}/print-data` port ERP `AssemblyRequestController@print` (mẫu 368,
      letterhead theo `company_id` của phiếu YC)
- [x] Verify: `php -l` sạch · HTTP kernel (DNS Admin): print-data phiếu 1441 → 200, đủ biến + letterhead công ty 1; id không có → 404;
      export assembly / contract / warranty → 200, ảnh banner = đúng bề rộng bảng (1386 / 1849 / 1246 px), dòng 1 nới theo ảnh.
      FE vue-template-compiler + babel sạch. Chưa kiểm trên trình duyệt (user tự mở)
- Ghi chú: Xuất Excel 1 phiếu (icon cạnh nút In ở tab Lắp đặt) VẪN mở ERP — #11988 chỉ nêu In. `DynamicExport` dùng chung (82 màn)
      cùng lỗi banner; chưa sửa lớp cha (cần hỏi)

## Check — Phiếu chờ giao việc có trạng thái "Đang thực hiện" không? (2026-11-03, @khoipv)
- [x] Chỉ điều tra, không sửa code. Kết luận: danh sách KHÔNG BAO GIỜ ra dòng "Đang thực hiện" — mỗi tab BE lọc cứng 1 trạng thái
      (`WaitingAssignTaskService`): HĐ / PL bổ sung = 3 "Có hiệu lực" · Phiếu BH = 2 "Đã duyệt" (+ `is_assign=1`) ·
      Lắp đặt / Giao việc khác = 1 "Chờ giao việc"
- Ghi chú: ô lọc Trạng thái tab Phiếu BH vẫn liệt kê đủ `STATUSES_WARRANTY` (có 3 "Đang thực hiện") → chọn là 0 dòng; tab HĐ / PL /
      Giao việc khác tương tự (dropdown đủ trạng thái, chỉ 1 giá trị có dữ liệu). Chưa sửa — chờ user chốt

## Tài liệu SRS / HDSD / Testcase (12/11/2026) @khoipv

Khuôn: `../bien-ban-ban-giao-nghiem-thu/` (10/11). Không sửa code / dữ liệu / skill chung. Nhánh develop cả 2 repo.

- [x] Đọc code FE (`pages/customer-care/waiting-assign-tasks/**`, menu `customer-care.js` nhóm "Giao việc", `base-confirm-modal`) + BE
      (`WaitingAssignTaskService` / Controller / route, `WrServiceContractController` từ chối / đóng / hủy duyệt, `WrAssignTaskStoreService`,
      Catalog `customer_care.phieu_cho_giao_viec.view` mức 3-4 + `customer_care.phieu_giao_viec.create` + `sale.hop_dong_an_gia.view`)
- [x] Chụp ảnh dev (`pcgv_shots/_capture/capture.js`, DNS Admin, chặn mọi yêu cầu ghi — 0 lọt). GIẢ cờ nút dòng 1 trên trình duyệt
      (DNS Admin không thuộc phòng tiếp nhận nào): 01b_row_more, 01c_pl_actions, 01d_assembly_actions, 30/30b/31/32/33. Đã xóa file lưu đăng nhập
- [x] Đối soát dev (`_capture/doisoat.js`, chỉ GET): tab Giao việc khác 931 = Phiếu YC giao việc khác "Chờ giao việc" ở màn nguồn 931;
      PBH TPE.PBH.2026.008226 màn Tạo PGV nạp đúng 1 thiết bị còn chưa giao. Tổng dev: HĐ 463 · PL 24 · BH 560 · LĐ 141 · GVK 931
- [x] `gen_srs.py` → `SRS - Phiếu chờ giao việc.docx` (84 trang, 12 chức năng, selfcheck khớp mẫu; metrics ui 12.8 / ev 4.8 / evch 945 / intro 1768)
- [x] `gen_hdsd.py` → `HDSD_Phieu cho giao viec.docx` (17 trang, 11 phần)
- [x] `gen_testcase.py` → `testcase.xlsx` (loai `phieu`, 131 TC, 10 nhóm, P0 44%, check_tc 0 lỗi)
- [x] `gen_checklist.py` → `Đối chiếu checklist.xlsx` (Testcase 125 có TC / 199 N/A; SRS 94 có mục / 69 N/A)
- [x] Ghi nhận lệch design (code hiện tại là chuẩn): Tạo phiếu giao việc nay mở màn HRM (design: ERP); tab Giao việc khác link chi tiết HRM;
      In tab Lắp đặt là popup HRM (#11988); lọc Ngày tạo tab Lắp đặt / Giao việc khác theo ngày tạo (design: thời gian dự kiến);
      nút Tạo PGV / Từ chối HĐ-PL không còn đặc cách Super admin; menu thật là CSKH sau bán → Giao việc (không phải Công việc)
- [x] Ghi nhận nghi lỗi (KHÔNG sửa): (1) quyền Xem mức Công ty không có tác dụng (code chỉ đọc mức Tổng công ty); (2) ô Trạng thái liệt kê
      đủ trạng thái nhưng chỉ 1 ra dữ liệu (đã ghi 03/11); (3) Từ chối tiếp nhận PL không ghi lịch sử, thông báo trỏ màn ERP; (4) xuất Excel
      rỗng vẫn ra file + báo thành công; (5) tab BH luôn hiện nút Tạo PGV cho cả người không có quyền (giữ như ERP)

### Checkpoint — 12/11/2026
Vừa hoàn thành: bộ SRS + HDSD + Testcase + Đối chiếu checklist màn Phiếu chờ giao việc.
Đang làm dở: —
Bước tiếp theo: user xem tài liệu; quyết định các nghi lỗi (mức Công ty của quyền Xem, ô Trạng thái, lịch sử từ chối PL).
Blocked:
