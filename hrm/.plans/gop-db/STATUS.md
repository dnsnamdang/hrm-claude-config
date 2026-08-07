# STATUS.md — Phần GỘP DATABASE (nhánh `gop_db`)

> File này chỉ theo dõi các feature làm trên nhánh `gop_db` (hoặc nhánh checkout ra từ `gop_db`).
> Feature trên nhánh khác → ghi ở `.plans/STATUS.md`.

## ⚠️ Nền tảng — đọc TRƯỚC khi làm việc trên nhánh `gop_db`

**`.plans/gop-db/design.md`** — nhánh `gop_db` (cả 2 repo) gộp DB ERP + HRM thành DB duy nhất `local_hrm_erp`.
Ảnh hưởng tới MỌI feature làm trên nhánh này: bảng trùng tên ưu tiên bản ERP (bản HRM đổi tên `hrm_*`, 24 bảng),
`roles`/`permissions`/`files`/`groups` là của **ERP** — dữ liệu HRM nằm ở `hrm_*`;
riêng **`employees` + `employee_infos` đã gộp chung từ 2026-08-03** → `auth()->user()->id` là id nhân viên
duy nhất, `hrm_employees` là bảng cũ bỏ đi (xem mục 0b của design.md);
`mysql2` vẫn trỏ DB ERP CŨ (nguồn bug id lệch); kèm 7 gotcha bắt buộc biết khi port màn ERP → HRM.
Việc gộp DB **không có migration trong repo** → không tái tạo được từ code, phải xin dump.

**Quy tắc bắt buộc (chi tiết ở `CLAUDE.md` mục "Phần GỘP DATABASE"):**
- Nhận biết bằng **nhánh git đang đứng**, không đoán theo tên feature: đang ở `gop_db` hoặc nhánh checkout ra từ `gop_db` → áp dụng quy tắc này
- Tài liệu: feature làm trên nhánh đó nằm trong **`.plans/gop-db/[feature]/`**, spec chi tiết ở `docs/superpowers/specs/gop-db/`
- Code: chỉ làm **trên nhánh `gop_db`** hoặc nhánh **checkout ra từ `gop_db`**, merge trả về `gop_db`
- KHÔNG dùng `mysql2` / `DB_CONNECTION_SECOND` cho tính năng mới

## Đang làm

- customer-cut-mysql2 → .plans/gop-db/customer-cut-mysql2/plan.md
  Trạng thái: **HOÀN TẤT + ĐÃ TEST** (2026-08-01, nhánh `gop_db`). Khách hàng còn ĐÚNG 1 luồng `/assign/customers`.
  Gồm: cắt hết `mysql2` khỏi luồng KH (35 file) · xoá 6 bảng `hrm_customer_*` + migration `2026_08_01_000001_drop_hrm_customer_tables` (đã test round-trip) ·
  gỡ toàn bộ tầng sync 2 chiều · xoá màn `/human/customers` + `/timesheet/setting/customers` · chuyển 10 picker sang luồng mới · thêm `GET assign/customers/search`.
  Test: 52/52 endpoint HTTP + 12 màn browser + luồng ghi (tạo/sửa/thêm liên hệ, có rollback). **7 lỗi thật đã sửa** (xem plan.md Phase 11-12).
  ⚠️ Đọc trước khi làm tiếp trên nhánh này: `.plans/gop-db/design.md`.

## Hoàn thành

- customer-care-serial-catalog → @junfoke → .plans/gop-db/customer-care-serial-catalog/plan.md
  Trạng thái: **CODE DONE + ĐÃ VERIFY (BE + trình duyệt)** (2026-08-06).
  Scope: chuyển "Danh mục serial thiết bị làm dịch vụ" (`serials`, 21.632 dòng) từ ERP sang **CSKH**
  — 1 màn danh sách READ-ONLY + Xuất Excel, 2 route `/v1/customer-care/serials`, quyền mới **1126**.
  Màn danh mục thứ 5 của phân hệ.
  ⚠️ GOTCHA: 7/9 route của `SerialController` ERP **không thuộc màn này** (thuộc màn Quản lý khách
  hàng, HRM đã có) → không port. Xuất Excel **dựng ở FE** (ExcelJS + fetch theo lô), BE không có
  route export vì 21 nghìn dòng dựng ở BE sẽ timeout trên server.
  Còn treo: user rà bằng mắt; chốt cách lọc 13 bản ghi `status` 0/3 (xem design.md).
  Spec: docs/superpowers/specs/gop-db/2026-08-06-customer-care-serial-catalog-design.md | Tóm tắt: .plans/gop-db/customer-care-serial-catalog/design.md

- chuyen-code-phan-he → @junfoke → .plans/gop-db/chuyen-code-phan-he/plan.md
  Trạng thái: **XONG 3 phân hệ, ĐÃ VERIFY TRÌNH DUYỆT** (2026-08-05) — giai đoạn 2 của
  `tach-phan-he-erp-hrm`: đưa **code** màn về đúng phân hệ, không chỉ menu.
  Scope: 3 phân hệ ở trạng thái "menu đã chuyển, code chưa chuyển" →
  **Danh mục chung** 10 màn (122 route `/v1/master-data/*`),
  **Bảo hiểm xã hội** 7 màn (38 route `/v1/insurance/*`),
  **Bán hàng** 27 màn qua 3 đợt — Danh mục+Thiết lập 11 → Báo cáo 8 → Dự án TKT+Phê duyệt 8
  (313 route `/v1/sale/*`). Tổng **98 cặp redirect** giữ URL cũ sống, **6 migration quyền**.
  Chốt xuyên suốt: chuyển cả 3 lớp (FE route + BE module + dọn quyền), giữ nguyên tên đoạn cuối
  route cho dễ đối chiếu, redirect vĩnh viễn ở `nuxt.config.js::extendRoutes`, verify sau mỗi đợt.
  Kèm 2 việc chuẩn hoá: **layout hub (kiểu MISA) thành chuẩn chung** cho phân hệ mới —
  sidebar + màn Tổng quan đều dùng component chung, thêm phân hệ chỉ cần khai `key` trong
  `HUB_SUBSYSTEMS`; và **tách quyền / đưa 10 quyền khách hàng về đúng phân hệ**.
  ⚠️ 3 route `/v1/assign/quotations/erp-contract/*` **cố ý giữ URL cũ** — hợp đồng tích hợp với
  codebase ERP ngoài repo, đổi là ERP gọi hỏng.
  Đã sửa 10 lỗi trong quá trình làm (6 lỗi có sẵn chặn màn + 4 lỗi tự gây) — chi tiết ở plan.md.
  Còn nợ: 7 màn địa lý-ngân hàng chưa có permission nào; bộ quyền KH cũ của HRM (id 166-169)
  còn song song, chưa quyết gộp/bỏ; verify màn Tạo phiếu BH ở môi trường có thông báo còn hiệu lực.
  Bước tiếp: các phân hệ còn lại chưa tới lượt chuyển code.
  **Phase 17-19 (2026-08-06), ĐÃ VERIFY TRÌNH DUYỆT**: chuẩn hub phủ **14/17 phân hệ** (thêm CSKH,
  Tài chính + 9 phân hệ mới); menu Tài chính gom 24 → 11 nhóm bám mega-menu `Kế toán` của ERP qua
  cờ `hubGroup`; sửa 3 lỗi có sẵn — sidebar hub không lọc quyền, `deriveHubGroups()` nuốt `erpPath`,
  icon rail hardcode túi Bán hàng.
  ⚠️ GOTCHA: gate quyền Bán hàng nằm ở `sale-hub.js::SALE_LINK_PERMISSIONS`, không phải `sale.js`.
  Còn nợ: `master-data` mới gate 2/10 màn (7 màn địa lý-ngân hàng chưa có permission nào trong DB).
  Spec: docs/superpowers/specs/gop-db/2026-08-04-chuyen-code-phan-he-master-data-insurance-design.md
  và docs/superpowers/specs/gop-db/2026-08-06-hub-menu-customer-care-finance-design.md | Tóm tắt: .plans/gop-db/chuyen-code-phan-he/design.md

- customer-care-cost-catalog → @junfoke → .plans/gop-db/customer-care-cost-catalog/plan.md
  Trạng thái: **BE + FE DONE, verify BE xong** (2026-08-03) — chuyển "Danh mục dịch vụ sửa chữa và
  chi phí khác" (`costs`, `kind_of=2`, 524 dòng) sang phân hệ CSKH. 8 route
  `/v1/customer-care/costs`, quyền 1119/1120.
  Màn này khác 3 màn trước ở 4 điểm: (1) **1 màn ERP phục vụ 3 mục menu** qua `?kind_of=`;
  (2) cột Chiết khấu nằm ở `company_costs` **theo từng công ty** — lấy theo
  `auth()->user()->current_company_role`, dùng selectSub để sort/lọc được trên SQL;
  (3) `status` là **1 = Hoạt động / 0 = Khóa**, khác các danh mục khác dùng 1/2;
  (4) xóa thực chất là **"khóa hoặc xóa"** — đã phát sinh ở báo giá/hợp đồng hãng thì chỉ set
  `status=0`. `canEdit`/`canDelete` của ERP **chặn cứng theo TÊN** ("Chi phí đi lại",
  "Chi phí vận chuyển").
  User chốt: bỏ hẳn phần đồng bộ CRM có trong model ERP; làm `kind_of=2` trước, `kind_of=1`
  (Chi phí phải trả / Chi phí bán hàng) tạm gác.
  🐛 Lỗi tự gây đã sửa: copy `prepareForValidation` từ màn Tiền tệ nên strip dấu phẩy → tỷ lệ
  `12,5` lưu thành **125**. 3 trường ở màn này đều là phần trăm (≤100) nên dấu phẩy là dấu thập
  phân → đổi `,` thành `.`.
  **Phase 5 (2026-08-03)** — cắt luôn `erp-cost-catalog` (@dnsnamdang) sang dùng luồng mới: gom
  `TpCost` thành alias `@deprecated` của `Cost` (giữ hằng cũ để nhánh kia merge vào vẫn chạy), đổi
  7 file sang `Cost`, **bỏ `mysql2` khỏi 4 file** của luồng danh mục chi phí. Phát hiện **3 lỗi
  thật**: transaction mở trên `mysql2` trong khi model ghi connection mặc định (không rollback);
  `findOrCreateCosts` insert thiếu `kind_of` NOT NULL → dòng tạo ra `kind_of=0` không hiện ở màn nào;
  `resolveOrCreateCost` ghi `type=1` cho `kind_of=2` làm lọt kiểm trùng tên. Đã ghi chú đầy đủ cho
  @dnsnamdang ở cuối `.plans/erp-cost-catalog/plan.md`.
  ⚠️ **Còn nhiều chỗ dùng `mysql2` ngoài phạm vi danh mục chi phí** (AssignBusinessController 15 chỗ,
  QuotationService, ProductProjectController…) — vẫn đọc DB ERP CŨ trên nhánh này, cần rà riêng.
  Bước tiếp: user verify bằng mắt `/customer-care/costs`.
  Spec: docs/superpowers/specs/gop-db/2026-08-03-customer-care-cost-catalog-design.md | Tóm tắt: .plans/gop-db/customer-care-cost-catalog/design.md

- finance-product-transfer-request → @khoipv → .plans/gop-db/finance-product-transfer-request/plan.md
  Trạng thái: **HOÀN THÀNH — user xác nhận xong (2026-08-07).** Code Phase 1–7 (D1–D17) + final review + fix wave, **đã commit**: `hrm-api 3a0acce08` · `hrm-client ed0abb049` (+ `690515fc4` fix bug), nhánh `gop_db`.
  Đã xong: BE (3 entity + searchByFilter phân quyền 4 cấp + CRUD + reject + notification chuông HRM + in template 87 + export Excel + 4 API phụ trợ form) · FE (list + form create/edit + chi tiết + print + menu finance.js:134) · Phase 7 (dùng chung QuotationProductSearchModal của màn báo giá, dọn conflict marker subsystems.js, `testcase.xlsx` 127 TC). Verify D12: ma trận quyền 6 nhóm × 6 action khớp SQL, Playwright toàn luồng PASS, round-trip 2 cổng tầng dữ liệu PASS, DB nguyên trạng. Ledger: sdd-progress.md.
  User đã xử lý xong (2026-08-07): verify browser bằng mắt · 5 mục "Chờ xác nhận PO" trong plan.md (thông báo cổng ERP, scope canView B1, SL lẻ, template 87, task rà quyền) · ENV DEPLOY `ERP_URL` cả 2 repo · **SQL DEPLOY đã chạy môi trường thật** (INSERT quyền 1129-1133 + `UPDATE permissions SET type = NULL WHERE id IN (100878,100879,100880,100881)`).
  ⚠️ Phát hiện quan trọng — **CHƯA mở task, còn nợ team**: middleware `CheckPermission` hỏng trên gop_db (spatie bỏ sót role gán từ ERP do model_type mismatch) → route reject của feature này phải bỏ middleware, chặn bằng `canApprove()`. Cần TASK RIÊNG rà mọi route khác đang gắn `checkPermission` + mapping quyền FE (accounts/currencies/account-banks 404 với mọi user — lỗi có sẵn của môi trường, không phải regression).
  Tồn: nội dung chốt của 5 mục PO chưa ghi ngược vào plan.md (mục "Chờ xác nhận PO / task riêng" vẫn đang để dạng câu hỏi).
  — Bối cảnh port gốc: màn ERP `admin/warehouse/product_transfer_requests?type=all`, 3 bảng, mã `PYCCH-xxxxx`, 13 trạng thái → phân hệ **Tài chính** → nhóm **Xuất hàng** (slot `finance.js:134`).
  **HRM là bản thay thế lâu dài**, 2 cổng song song cùng bảng, KHÔNG đổi schema. HRM chỉ ghi status 2↔3; 1, 4–12 do chuỗi kho ERP đẩy.
  Chốt 6 QĐ: port đầy đủ (nút Tổng hợp mở tab ERP) · dùng lại quyền ERP + "Kế toán kho" · 1 màn list duy nhất (=type=all) · form đủ popup hàng + Xem tồn + giá/ĐVT · xóa giữ ERP (status=3 + người tạo) · nới validate after:today khi sửa.
  Spec: docs/superpowers/specs/gop-db/2026-08-05-finance-product-transfer-request-design.md | Tóm tắt: .plans/gop-db/finance-product-transfer-request/design.md

- customer-care-services-catalog → @khoipv → .plans/gop-db/customer-care-services-catalog/plan.md
  Trạng thái: **CODE DONE P1–P5, user xác nhận xong (2026-08-05)** — port trọn màn "Danh mục gói
  bảo dưỡng" (ERP `Sale\ServiceController`, `services` 207 dòng + 5 bảng con) sang
  `/customer-care/services`: BE `Modules/CustomerCare` (4 entity + ServiceRequest + ServiceService +
  resource/export + controller, 12 route), FE list + form 5 khối (ma trận bảo dưỡng × cấp, giá vốn
  theo công ty, popup hàng hóa/nhóm theo UX popup báo giá với 17 bộ lọc, đính kèm S3), in template 191.
  Phase 5: 7 cụm chỉnh theo user (bỏ cột Hành động, VAT nullable, copy giữ đính kèm, fix auto-print…).
  🐛 Đã sửa 2 lỗi CRITICAL `key_word` shape `{text}` (88/207 gói có nguy cơ hỏng màn báo giá DV ERP).
  ⚠️ Bug HỆ THỐNG chưa sửa (file chung, cần báo team): `V2BaseSelect.vue:59` rớt option id=0.
  F3 (sửa gói xóa hết dòng ma trận = no-op im lặng) giữ nguyên theo ERP — user ruling trong sdd-progress.md.
  ⚠️ **Khi DEPLOY phải chạy tay 3 SQL** (chi tiết sdd-progress.md Task 1.5): UPDATE permissions
  type=24 (101023-101025) · mirror `employee_has_roles` sang model_type HRM · INSERT
  `role_has_permissions` cho Super admin; DB local còn thiếu quyền CSKH 1115-1120 của 2 feature trước.
  Tồn: checklist "Verify tổng thể" cuối plan.md chưa tick (regression 4 màn CSKH cũ, round-trip ERP↔HRM 2 chiều).
  Spec: docs/superpowers/specs/gop-db/2026-08-04-customer-care-services-catalog-design.md | Ledger: .plans/gop-db/customer-care-services-catalog/sdd-progress.md

- bo-sung-menu-phan-he → @junfoke → .plans/gop-db/bo-sung-menu-phan-he/plan.md
  Trạng thái: **CODE DONE + KIỂM THỬ TỰ ĐỘNG PASS** (2026-08-03) — Phase 0-9 xong.
  Khai 355 mục menu trên 14 phân hệ theo sheet `Gộp phân hệ ERP-HRM` (10 mục link thật sang ERP, 345 mục xám mờ),
  Chỉ đụng `hrm-client`. Kiểm thử bằng cách render THẬT `Sidebar.vue`
  qua `vue-server-renderer`; regression 11 bộ menu cũ cho kết quả render-identical với bản `git show HEAD`.
  Phase 8 đã sửa trực tiếp sheet gộp (đã sao lưu bản gốc trước khi sửa).
  **PHASE 9 (2026-08-03, user đổi ý)**: Mua hàng / Kho / Vận chuyển **KHÔNG ẩn nữa** — vẫn hiện card ở màn chọn phân hệ + dropdown, bấm vào thì **điều hướng sang ERP**. Bỏ cờ `hidden`, dùng `external: true` + `erpPath`; `openERP()` ở `pages/index.vue` và `SubsystemSwitcher.vue` nhận tham số subsystem để ghép `ERP_URL + erpPath`; `getPermissionSubsystemGroups()` đổi `!s.hidden` → `!s.external` (3 phân hệ này không còn khối quyền ở màn Phân quyền, nhưng GIỮ NGUYÊN `permissionType` 20/21/22). ⚠️ **ERP không có trang landing riêng cho 3 phân hệ này** (topmenubar ERP chỉ có Danh mục/Khởi tạo/Kinh doanh/Kế toán/CSKH/QTTT) nên `erpPath` phải trỏ MÀN ĐẠI DIỆN: Mua hàng → `/admin/orders/inland_order_summary_new`, Kho → `/admin/warehouse/product_import_requests/all`, Vận chuyển → `/admin/warehouse/delivery_trips/all`. Card ERP tổng không khai `erpPath` → vẫn về trang chủ ERP.
  ⚠️ **BUG PHÁT HIỆN KHI KIỂM THỬ — CHƯA SỬA, không thuộc feature này**: sau commit `564125504 gop database khach hang`, mục "Khách hàng" ở `subsystem-menu/master-data.js` đổi link sang `/assign/customers`, **trùng** với mục "Khách hàng" nhóm Danh mục của `subsystem-menu/sale.js`. Vi phạm bất biến *mỗi link chỉ thuộc đúng 1 phân hệ* mà `resolveSubsystem()` dựa vào → mở `/assign/customers` giờ LUÔN hiện sidebar **Danh mục chung** (đứng trước trong mảng `SUBSYSTEMS`), không bao giờ ra Bán hàng. Cần bỏ 1 trong 2 mục.
  Bước tiếp: **Phase 10 — verify browser thật, CHƯA LÀM** (độ mờ mục xám, sidebar Bán hàng 184 mục / Tài chính 104 mục).
  8 gotcha + bài học (ẩn phân hệ làm khuất màn phân hệ khác, bẫy khớp dòng trong sheet, `Sidebar.vue` chỉ render `router-link`…): xem plan.md.
  Spec: docs/superpowers/specs/gop-db/2026-08-01-bo-sung-menu-phan-he-design.md | Tóm tắt: .plans/gop-db/bo-sung-menu-phan-he/design.md

- customer-care-maintenance-catalogs → @junfoke → .plans/gop-db/customer-care-maintenance-catalogs/plan.md
  Trạng thái: **CODE DONE + VERIFIED (BE)** (2026-08-03) — chuyển "Cấp dịch vụ bảo dưỡng" (`levels`)
  + "Danh mục ghi chú kiểm tra bảo dưỡng" (`note_maintenances`) từ ERP sang **phân hệ CSKH**; là 2 màn ĐẦU TIÊN của
  phân hệ này (`Modules/CustomerCare` trước đó rỗng, chưa có quyền `type=24` nào).
  BE 13 file + 16 route `/v1/customer-care`, quyền 1115-1118, FE 2 màn danh sách + 2 modal.
  Sửa 2 lỗi ERP: `levels` chỉ kiểm 1/6 bảng khi xóa, `note_maintenances` không chặn xóa gì.
  ⚠️ Phát sinh: **ERP + HRM đã gộp chung `employees` / `employee_infos`** → gỡ toàn bộ lớp map ERP employee id
  khỏi Finance + CSKH (Phase 1 trong plan.md). Còn nợ: `ErpPermissionHelper` + `Modules/Assign` vẫn qua `mysql2`.
  Bước tiếp: user verify bằng mắt `/customer-care/levels` + `/customer-care/note-maintenances`.
  Spec: docs/superpowers/specs/gop-db/2026-08-03-customer-care-maintenance-catalogs-design.md | Tóm tắt: .plans/gop-db/customer-care-maintenance-catalogs/design.md

- finance-currency-catalog → @junfoke → .plans/gop-db/finance-currency-catalog/plan.md
  Trạng thái: **CODE DONE + VERIFIED (BE + cron)** (2026-08-03) — màn thứ 3 của phân hệ Tài chính.
  Bám sát ERP (danh sách + modal CRUD + xóa + lọc + Xuất Excel), không đổi schema `currencies`.
  8 route, quyền 1113/1114. Chuyển luôn cron tỷ giá sang HRM (`finance:update-exchange-rate`, 03:00)
  và **đã tắt lịch bên ERP** → HRM là nơi duy nhất chạy tự động.
  Sửa 4 lỗi của cron ERP, nặng nhất: đồng tiền đứng ĐẦU file XML không bao giờ được cập nhật (AUD đứng im ~16 tháng).
  ⚠️ Trước khi lên thật: `hrm-api/.env` chưa cấu hình mail nên `emailOutputTo` chưa gửi được.
  Bước tiếp: user verify bằng mắt `/finance/currencies`.
  Spec: docs/superpowers/specs/gop-db/2026-08-03-finance-currency-catalog-design.md | Tóm tắt: .plans/gop-db/finance-currency-catalog/design.md

- finance-account-catalog → @junfoke → .plans/gop-db/finance-account-catalog/plan.md
  Trạng thái: **PHASE 1-6 + 8 CODE DONE + VERIFIED** (2026-08-01) — 2 màn "Danh mục tài khoản" +
  "Danh mục loại tài khoản" từ ERP sang phân hệ **Tài chính**; là màn đầu tiên của phân hệ nên phải dựng luôn khung
  `Modules/Finance` + `components/subsystem-menu/finance.js`.
  Port trọn bộ: CRUD + khóa/mở + lịch sử + Xuất/Import Excel + In danh sách (template DB id 459).
  26 route, quyền 1107-1110 (`type=8`). Verify HTTP thật 33 case + browser Playwright toàn luồng, DB trả nguyên trạng.
  Bước tiếp: Phase 7 đối chiếu 2 cổng (cần bật ERP local) + tạo 2 file mẫu Excel trong `hrm-client/static/`.
  Toàn bộ gotcha/bài học (4 lỗi FE khi chạy thật, 4 bài học phân trang, icon phải lấy từ codebase,
  tên `group` permission phải duy nhất…): xem plan.md.
  Spec: docs/superpowers/specs/gop-db/2026-07-30-finance-account-catalog-design.md | Tóm tắt: .plans/gop-db/finance-account-catalog/design.md

- tach-phan-he-erp-hrm → @junfoke → .plans/gop-db/tach-phan-he-erp-hrm/plan.md
  Trạng thái: **XONG GIAI ĐOẠN 1 (khung phân hệ + menu) — 2026-07-30.** Đã test thật 9 màn trên dev. Tồn: user test 17 màn edit/detail. Giai đoạn 2 (di chuyển code màn sang route mới) chưa bắt đầu — xem Phase 7 trong plan.md.
  Scope: Quy hoạch lại phân hệ ERP + HRM theo Sơ đồ tổng thể v1.6 → 24 phân hệ / 5 nhóm. Dựng base 17 phân hệ mới (BE 17 module skeleton, FE registry `components/subsystems.js` + menu + dashboard stub + icon SVG), dựng lại màn chọn phân hệ + menu chuyển nhanh, phân hệ mới đi menu dọc (`layouts/subsystem.vue`).
  ⚠️ GOTCHA: (1) mỗi link chỉ được thuộc ĐÚNG 1 phân hệ, trùng là `resolveSubsystem` trả sai. (2) layout dùng SidebarMenu phải có method `toggleMenu`, thiếu thì bấm thu gọn menu ra trang 404. (3) item menu không có `subItems` phải khai `isShow: true`, quên thì sidebar rỗng. (4) dự án nạp 2 bản Remix Icon xung đột codepoint → icon phân hệ dùng SVG tự vẽ.
  Spec: docs/superpowers/specs/gop-db/2026-07-30-tach-phan-he-erp-hrm-design.md | Tóm tắt: .plans/gop-db/tach-phan-he-erp-hrm/design.md
