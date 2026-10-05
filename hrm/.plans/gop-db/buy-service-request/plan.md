# Plan — Yêu cầu mua dịch vụ (ERP → HRM)

> Phụ trách: @junfoke · Nhánh: `feat/finance-buy-service-request` (từ `gop_db`) · Tạo: 2026-09-22
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-09-22-buy-service-request-design.md`
> Tóm tắt: `design.md`

## Phase 0 — Khảo sát nguồn ERP

- [x] Đọc model `BuyServiceRequest` (615 dòng) + `BuyServiceRequestDetail`, controller (474 dòng),
      6 blade `orders/buy_service_requests/`
- [x] Đếm dữ liệu thật trên gop_db: **81 phiếu / 98 dòng chi tiết**; trạng thái 7=71, 4=6, 5=3, 6=1
- [x] Verify phụ thuộc: mã phí `costs.kind_of=2` (98/98 dòng) · NCC = `customers.is_supplier`
      (bảng `suppliers` **0 dòng**) · `EmployeeManageDepartment` đã port
- [x] Tra vị trí menu ERP: *Khởi tạo → Mua dịch vụ* (dòng 454) và *Mua hàng → Mua dịch vụ* (dòng 1766)
- [x] Tra chỗ khai sẵn trong menu HRM: `sale-hub.js:153` nhóm `Yêu cầu → Mua dịch vụ` (đang `link: null`)
- [x] Xác định khuôn HRM để bám — **2 lớp, đừng lẫn** (skill `erp-to-hrm-screen` cảnh báo copy màn
      vừa port là nhân bản cái sai):
      · **UI** = `pages/assign/customers/` (Danh mục khách hàng — khuôn chuẩn)
      · **Nghiệp vụ/BE** = `prepick-extend-requests` (phiếu 2 nấc duyệt) + `addition-accounting-requests`
      (tiền lệ cắt luồng, link sang ERP)
- [x] Chốt có làm **Lịch sử thay đổi** (user 2026-09-22) → thêm bảng mới `buy_service_request_history`
- [x] Chốt 8 quyết định với user (module Finance · route `/finance/...` · menu nhóm Mua dịch vụ ·
      giữ nút Lập hợp đồng trỏ ERP · phạm vi đầy đủ · quyền trùng tên ERP · CÓ làm Lịch sử ·
      giữ 3 cửa vào `type=`)
- [x] Viết spec chi tiết

## Phase 1 — BE: nền tảng

- [x] Tạo nhánh `feat/finance-buy-service-request` từ `gop_db` ở **cả 2 repo**
- [x] `BuyServiceRequestPermissionSeeder` — 5 quyền guard `api`, **id 1586-1590**, `type = 23`,
      `group = 'Yêu cầu mua dịch vụ'`, tên **trùng bản ERP** (guard `web`, id 100810-100814);
      gán lại role đang giữ quyền ERP + Super admin (role 18). Bám
      `AdditionAccountingRequestPermissionSeeder`, **không** chạy `PermissionsTableSeeder` toàn bộ
- [~] ~~Migration tạo bảng `buy_service_request_history` + entity `BuyServiceRequestHistory`~~ —
      **ĐÃ GỠ ngày 22/09** khi phát hiện sai khuôn: dùng bảng CHUNG `catalog_histories` (xem Phase 6b).
      `migrate:rollback` sạch, màn này **không còn migration nào**
- [x] Entity `Finance/Entities/BuyServiceRequest/BuyServiceRequest.php` — 8 STATUSES (sửa *Đang tạo*
      sang `draft`), quan hệ, `searchByFilter` (3 preset), `canView/canEdit/canDelete/
      canDepartmentApprove/canKsApprove/canSendKsApproveAgain/canCancel/canCreateContract`,
      `statusMeta`, `attachmentList`, `generateCode`
- [x] Entity `BuyServiceRequestDetail.php` — **không ghi `contracted_qty`**
- [x] Dùng lại trait `ChecksEmployeePermission` (`manageableDepartmentIds` / `sameCompanyAsCurrent`)

## Phase 2 — BE: đọc

- [x] `BuyServiceRequestService::searchByFilter / meta / findForShow / detailData`
- [x] `BuyServiceRequestListResource` (31 trường) — chi tiết trả thẳng từ `detailData()`, không
      cần resource riêng
- [x] Controller `index`, `show`
- [x] Nguồn cho form: `costOptions()` (`kind_of = 2`, `status = 1`, 520 dòng) ·
      `searchSuppliers()` (paginate, 758 dòng ở local)
- [x] Routes (`/costs`, `/suppliers` đặt TRƯỚC `/{id}` — đã verify bằng `app('router')->getRoutes()`;
      `php artisan route:list` KHÔNG chạy được trên project này, lỗi `PermissionHelper` có sẵn khi
      không có user đăng nhập)

## Phase 3 — BE: ghi

- [x] `BuyServiceRequestStoreRequest` — `note` bắt buộc · `details[].cost_id/qty/price/amount` bắt
      buộc · `attachments` bắt buộc khi phiếu chưa có file (pdf/jpg/jpeg/png/doc/docx/xls/xlsx/zip, ≤10MB)
- [x] `store()` / `update()` — transaction, sinh mã `<mã cty>.YCMDV.<năm><seq6>`, `syncDetails()`
      **giữ `contracted_qty`** theo khoá `cost_id|supplier_id`
- [x] `departmentApprove()` — set `CHO_KS_DUYET` + `department_approver_id` + `received_time`,
      qua middleware `CheckDueConfig('Duyệt yêu cầu mua dịch vụ')`
- [x] `ksApprove()` — ghi `price_approve` / `amount_approve` / `ks_comment` / `summary`.
      **Cập nhật TẠI CHỖ theo id dòng**, KHÔNG xoá-tạo-lại như ERP (giữ `contracted_qty`)
- [x] `sendKsApproveAgain()` · `cancel()` · `reject()` · `destroy()` · `deleteFile()`
      (`reject` ghi lý do vào `comment` hay `ks_comment` tuỳ nấc đang đứng)
- [x] `uploadFiles()` — S3, mime ERP + `zip`, ≤10MB; ghi vào cột `attachments` nối bằng `, `
- [x] `BuyServiceRequestNotifyService` — **4 sự kiện**: gửi TP duyệt · gửi KS duyệt · duyệt lại giá
      · **từ chối (BỔ SUNG so với ERP** — ERP không báo gì, người lập không biết phiếu bị trả)

## Phase 4 — BE: in + xuất

> ⚠️ Xuất Excel viết lại theo **4 mắt xích bắt buộc** của skill `list-page` mục 14b (tài liệu
> 21/09), KHÔNG tự chế `exportData()`.

- [x] `ErpReportTemplate` — thêm 2 hằng `PHIEU_YEU_CAU_MUA_DICH_VU = 417` · `DANH_SACH_YEU_CAU_MUA_DICH_VU = 416`
- [x] `printData()` — mẫu **417**, khổ ngang, trả HTML đã `fillReport()` cho FE mở trang in
- [x] `printListData()` — mẫu **416**, khổ ngang; `columns` = cột đang hiện trên danh sách
- [x] Letterhead lấy theo `company_id` **trên phiếu**, không phải công ty người đang xem
- [x] `ExportColumnRegistry::COLUMNS['buy_service_requests']` — key phải khớp key của
      `BuyServiceRequestListResource`, lệch là cột ra rỗng
- [x] `exportRows($request)` trong service — **dùng lại đúng query của màn danh sách**
- [x] `export()` controller — `DynamicExport()->forData()->withColumns(ExportColumnRegistry::resolve(...))->withTitle()`
- [x] Route `/export`, `/print-list-data` khai **TRƯỚC** `/{id}` (đã có tiền lệ nuốt route)
- [x] Kiểm: mở file tải về bằng Excel, **dòng 1 phải là tiêu đề cột tiếng Việt** (thấy `{"data":[…` là gọi nhầm endpoint danh sách)

## Phase 5 — FE: danh sách

- [x] `pages/finance/buy-service-requests/index.vue` — **UI bám `pages/assign/customers/`**
      (khuôn chuẩn), chỉ lấy cấu trúc BE/nghiệp vụ từ `prepick-extend-requests`
- [x] 3 cửa vào bằng `?type=` : `index` (của tôi) · `all` (tổng hợp) · `for-approve` (chờ tôi duyệt)
      + watcher `$route.query.type`
- [x] Cột: STT · Số phiếu · Ngày tạo · Ngày nhận đơn · Ngày duyệt giá · Người yêu cầu · Phòng yêu
      cầu · Người duyệt giá · Trạng thái · Hành động
- [x] `V2BaseSmartFilterPanel` + **`floating`** (bắt buộc, không ngoại lệ) + `filterFields` 8 ô:
      Công ty · Phòng ban · Số phiếu · Tên dịch vụ · Người duyệt giá · Người tạo · Khoảng ngày tạo ·
      Trạng thái. ⚠️ `V2BaseFilterPanel` **đã bị XOÁ khỏi repo 21/09** — đừng copy pattern
      `#advanced-filters` từ git history
- [x] Khuôn tham chiếu panel: **`pages/master-data/product-natures/index.vue`** (đổi 21/09)
- [x] Bộ lọc mở đầu bằng **Công ty → Phòng ban → Bộ phận**; dùng `V2BaseCompanyDepartmentFilter`,
      khai đủ 4 key `company_id`/`department_id`/`part_id`/`employee_id` trong `initialStateForm`
- [x] Luật thao tác: **ô CHỌN → tìm luôn**; **ô GÕ TAY → Enter mới tìm** (khoá ô gõ tay đưa vào
      `ignoredFields` qua `textFilterKeys(this.filterFields)`)
- [x] Slot `#field-*` (nếu có): **KHÔNG tự vẽ `V2BaseLabel`**, không khai `hideLabel` cho ô đơn;
      `V2BaseSelectRemote` trong slot bắt buộc `height="36px"`
- [~] Ô lọc cao **32px, KHÔNG phải 36px** — nhưng **màn khuôn `product-natures` cũng 32px** trên
      đúng bản `gop_db` này (đã đo cả 2 màn cùng phiên). Không tự sửa CSS component dùng chung;
      đã nêu cho user quyết (skill: thấy project có nhiều kiểu thì hỏi, đừng tự chọn)
- [x] Toolbar **bắt buộc đủ**: Tạo mới → Xuất Excel → Tuỳ chỉnh cột (màn này không có Import).
      **Xuất Excel và Tuỳ chỉnh cột KHÔNG gate quyền**; mixin `exportFieldsMixin` +
      `columnCustomizationMixin`; `runExport(type, fields)` nhận **MẢNG key** (đừng destructure)
- [x] Mixin nhớ bộ lọc · header dính · `localStorageKey`/`columnScreenKey` duy nhất
- [x] Badge trạng thái: `V2BaseBadge` + `utils/statusBadgeVariant.js` — **không tự dựng span**
- [x] CSS của màn KHÔNG đặt trong `v2-styles.scss` scoped cho phần tử do component dùng chung render

## Phase 6 — FE: chi tiết + form

- [x] Màn chi tiết: thông tin chung · lưới chi tiết (Mã phí · NCC · SL · Đơn giá · Thành tiền ·
      Đơn giá duyệt · Thành tiền duyệt) · đính kèm · ý kiến TP / KS · lịch sử
- [x] Form tạo/sửa: chọn Mã phí (`V2BaseSelect`) · chọn NCC (`V2BaseSelectRemote`) · nhập SL/Đơn giá
      tự tính Thành tiền · `vat_percent` · upload nhiều file bằng **`components/V2BaseFile.vue`**
      (không tự dựng `<input type="file">`)
- [x] Select chọn 1: **không khai `allowClear`** — `V2BaseSelect` đã mặc định có dấu `×` (chốt 16/09)
- [x] Validate FE: chỉ trường bắt buộc lõi gắn `required`, còn lại để BE trả 422;
      **không truyền message thủ công** cho `required`/`max` — chỉ khai `data-vv-as`
- [x] Số định dạng chuẩn quốc tế `1,234,567.89`; ô rỗng để **TRỐNG** (không in `-`)
- [x] Nút hành động theo `can*` từ BE, nút không dùng được thì **ẩn**
- [x] Nút **"Lập hợp đồng mua dịch vụ"** → mở tab mới sang `ERP_URL` +
      `/admin/orders/buy-service-contract/create?buy_service_request_id=<id>`
- [x] Mixin cảnh báo rời trang khi chưa lưu
- [x] Thao tác xong (duyệt/hủy/từ chối) → quay về danh sách
- [x] Toast dùng nguyên văn bộ QLDA_001…025

## Phase 6b — Lịch sử thay đổi (dùng CƠ CHẾ CHUNG, không đẻ bảng riêng)

> ⚠️ **ĐỔI HƯỚNG 22/09 giữa Phase 6.** Ban đầu bám `PrepickExtendRequestHistory` (bảng history
> riêng cho từng màn) — sai khuôn hiện hành: **mọi màn phiếu Tài chính đã dùng bảng CHUNG
> `catalog_histories`** qua trait `App\Services\Concerns\LogsCatalogHistory` và endpoint dùng chung
> `catalog-histories/{bảng}/{id}`. Đã gỡ bảng riêng, chuyển sang cơ chế chung ⇒ **không còn
> migration nào cho màn này**.

- [x] Gỡ migration + entity + service history riêng, `migrate:rollback` sạch bảng
- [x] Đăng ký `buy_service_requests` vào `CatalogHistoryService::TABLES` (7 cột theo dõi)
- [x] `BuyServiceRequestService` `use LogsCatalogHistory` + `catalogTable/catalogColumns/catalogDisplay`
- [x] `snapshotOf()` bồi 2 khoá ẢO: `attachments_count` (đếm file) và `details_rows` (khoá dạng
      bảng `cost_id|supplier_id`). **KHÔNG chụp `contracted_qty`** — cột do ERP ghi
- [x] Ghi log ở mọi thao tác: `create` · `update` · `change_status` (kèm ý kiến/lý do) · `delete`
- [x] Khối ở màn **chi tiết** — `SystemInfoSection` + `endpoint-base="catalog-histories"`, mặc định ẩn
- [x] Popup ở màn **danh sách** (menu ⋮) — còn lại, dùng `CatalogHistoryModal.vue` như màn danh mục
- [x] Đối chiếu 2 nơi hiển thị y hệt nhau

## Phase 7 — Menu + phân quyền FE

- [x] `sale-hub.js:153` — đổi `'Yêu cầu mua dịch vụ'` thành
      `{ n: 'Yêu cầu mua dịch vụ', link: '/finance/buy-service-requests?type=all' }`
- [x] `sale-hub.js:146` — **bỏ** `'Tổng hợp - YC hạch toán mua DV'` và `'YC hạch toán mua dịch vụ'`
      khỏi nhóm `Dịch vụ` (trùng với nhóm `Mua dịch vụ`; bất biến: 1 link chỉ ở 1 chỗ)
- [ ] Gate quyền cho link trong `SALE_LINK_PERMISSIONS`
- [ ] Audit menu: dump link từng phân hệ, đếm trùng = 0; kiểm `layout` của page khớp phân hệ

## Phase 8 — Kiểm chứng

- [x] Test BE: 3 preset `searchByFilter` · 4 mức phạm vi xem · 2 nấc duyệt · sinh mã · upload/xóa file
- [x] Đối chiếu danh sách HRM vs ERP trên cùng tài khoản: **số phiếu phải khớp 100%**
- [x] Verify trên trình duyệt bằng Playwright (chờ ≥3s khi test bộ lọc), **XEM ẢNH** chứ không chỉ đọc DOM
- [x] Tự kiểm theo checklist 8 nhóm A→H của skill `erp-to-hrm-screen`
- [x] Kiểm phiếu do ERP đổi trạng thái sang 6/7 thì HRM hiển thị đúng

## Checkpoint — 2026-09-22

- **Vừa hoàn thành:** Phase 0 trọn vẹn — khảo sát + spec + design + plan. Chốt 8 quyết định với
  user (thêm: CÓ làm Lịch sử thay đổi, đủ 2 nơi). Đã tạo nhánh
  `feat/finance-buy-service-request` từ `gop_db` ở **cả 2 repo**, cây làm việc sạch.
- **Phase 1 XONG** (22/09): migration `buy_service_request_history` đã chạy · seeder quyền đã chạy
  (id 1586-1590, `type = 23`, gán 5/6/16/16/2 role theo bản ERP + Super admin) · 3 entity
  (`BuyServiceRequest` / `Detail` / `History`) `php -l` sạch.
- **Phase 2 XONG** (22/09), đã smoke-test bằng tinker với user 13 (super admin):
  3 preset `all` = 81 · `index` = 0 · `for-approve` = 0 (đúng — dữ liệu local không có phiếu ở
  trạng thái 2/3); từng ô lọc chạy đúng (`cost_name` "vận chuyển" → 7, `status=4` → 6,
  `start_date` → 31); sort `code asc` đúng; `detailData()` ra đủ 6 file đính kèm, tên TP/KS,
  mốc duyệt, dòng chi tiết và 7 cờ `is_can_*`.
- **Phase 3 XONG** (22/09), test end-to-end bằng script bootstrap Laravel (2 kịch bản, 11 bước):
  tạo → ERP ghi `contracted_qty = 1.5` → sửa+gửi duyệt → TP duyệt → KS duyệt giá — `contracted_qty`
  **giữ nguyên 1.5 qua cả 2 lần ghi**; từ chối ở nấc TP ghi `comment`, ở nấc KS ghi `ks_comment`;
  duyệt lại giá về 3, hủy về 8; xóa file 2→1; lịch sử ra 4 mốc đúng thứ tự mới→cũ với
  `action_group` đúng. Dọn sạch, DB về đúng 81 phiếu / 98 dòng / 0 log mồ côi.
  14 route đã đăng ký, `dueConfig:Duyệt yêu cầu mua dịch vụ,manager` gắn đúng bước TP duyệt.
- **Rà tài liệu pull 22/09** (user yêu cầu): 5 điểm ảnh hưởng, ghi ở `design.md` mục "Cập nhật theo
  tài liệu pull ngày 22/09/2026". Đã sửa ngay phần code bị ảnh hưởng: bỏ `messages()` khỏi 2
  FormRequest + 2 chỗ `validate()` inline, thay bằng `attributes()` (giữ 1 câu nghiệp vụ `status.in`).
  Phase 4/5/6 trong plan này đã cập nhật theo skill mới.
- **Phase 4 XONG** (22/09), verify thật: mẫu in 417 (3.472 ký tự) và 416 (1.566) đều có trên DB;
  `fillReport()` ra 7.452 ký tự, **0 placeholder sót**; phiếu Đã duyệt ra `COLSPAN=9` + đủ cột
  "Giá duyệt", phiếu chưa duyệt ra `COLSPAN=7` và **không** có cột đó; in danh sách lọc `status=4`
  ra đúng **6 dòng** = 6 phiếu trên DB. Xuất Excel: file thật `Microsoft Excel 2007+` 91 KB,
  **dòng tiêu đề là tiếng Việt**, 14 cột đăng ký đều khớp key của Resource (0 cột rỗng),
  `fields=code,status_name,khong_ton_tai` → chỉ lấy 2 key hợp lệ, key lạ bị bỏ.
  3 file dùng chung (`ErpReportTemplate`, `ExportColumnRegistry`, `Routes/api.php`) **chỉ THÊM
  dòng, 0 dòng bị sửa/xoá** (`git diff --numstat` = 6/36/21 insertions, 0 deletions).
- **Phase 5 gần xong** (22/09): đã viết `pages/finance/buy-service-requests/index.vue` (17 cột,
  7 ô lọc + khối tổ chức, 9 hành động dòng), parse sạch bằng `vue-template-compiler` + `@babel/core`.
  Menu đã wire: `sale-hub.js` nhóm *Mua dịch vụ* trỏ `/finance/buy-service-requests?type=all`,
  bỏ 2 mục trùng ở nhóm *Dịch vụ*.
  BE bổ sung: `contract_erp_path` nay ghép sẵn `ERP_URL` (trả rỗng nếu thiếu cấu hình).
  **CÒN LẠI: verify trên trình duyệt** (nghiệm thu FE phải XEM ẢNH, không chỉ đọc DOM).
- **Phase 5 XONG + ĐÃ VERIFY TRÌNH DUYỆT** (22/09, `npm run dev` cổng 50603, đăng nhập thật,
  XEM ẢNH chứ không chỉ đọc DOM):
  · Sidebar hiện **BÁN HÀNG** → `resolveSubsystem` nhận đúng link mới.
  · 16 cột đúng nhãn, badge: "Đã duyệt"/"Đã lập hợp đồng" xanh, "Không duyệt" ĐỎ, đúng SRS.
  · Cột Hành động chỉ hiện nút dùng được (user không phải người tạo → chỉ In + Lịch sử) — ẩn hẳn,
    không có nút xám.
  · 8 ô lọc đủ dữ liệu (Công ty 5, Phòng ban 68, Trạng thái 8, Người duyệt giá/Người tạo 555).
  · **Luật ô lọc đúng chuẩn**: chọn Trạng thái "Đã duyệt" → tự tìm ngay, 81 → **6 dòng**
    (= 6 phiếu status 4 trên DB); gõ Số phiếu xong **chưa Enter vẫn 6 dòng**, bấm Enter → **1 dòng**
    đúng `TPE.YCMDV.2026000083`.
  · Select chọn 1 có sẵn dấu `×` (không phải khai `allowClear`).
  · "Xuất Excel" mở popup **Chọn trường xuất file, tick sẵn 14/14** — không tải thẳng.
  · Hub Bán hàng có mục "Yêu cầu mua dịch vụ", bấm vào ra đúng `/finance/buy-service-requests?type=all`;
    mục trùng "Tổng hợp - YC hạch toán mua DV" đã biến mất.
  · 1 lỗi đã sửa trong lúc verify: `V2BaseDataTable` render `title` làm TIÊU ĐỀ CỘT (không phải
    tooltip) → 2 cột ngày hiện sai chữ, đã cho `title` = `label`.
- **Phase 6 XONG phần chính + ĐÃ VERIFY TRÌNH DUYỆT** (22/09):
  · 6 file FE mới: `create.vue` · `_id/edit.vue` · `_id/index.vue` · `components/BuyServiceRequestForm.vue`
    · `components/BuyServiceDetailTable.vue` · `components/CommentModal.vue`.
  · Màn **Chi tiết** dùng lại chính Form với `readonly` (không dựng khối riêng): ảnh chụp cho thấy
    đủ Thông tin chung, 6 file đính kèm có nút xem/tải, lưới dịch vụ + 3 dòng tổng đúng số
    (489,500,000 / 39,160,000 / 528,660,000 — **định dạng chuẩn quốc tế**), khối Lịch sử thu gọn.
  · Màn **Tạo**: đủ dấu `*` ở trường bắt buộc, nút "Chọn tệp đính kèm" (`V2BaseFile`), 1 dòng dịch
    vụ trống sẵn, footer **Lưu nháp / Gửi duyệt (CAM) / Quay lại** đúng màu nhóm nút.
  · Test BE sau khi đổi cơ chế lịch sử: chạy lại kịch bản end-to-end → 6 mốc log trong
    `catalog_histories` (`create` · `update` · 3× `change_status`), `contracted_qty` vẫn giữ 1.5.
    Dọn sạch: DB về đúng 81 phiếu / 98 dòng / 0 log của màn này.
- **ĐÃ VERIFY TRỌN LUỒNG TRÊN TRÌNH DUYỆT** (23/09, phiếu thật `TPE.YCMDV.2026000093` do chính
  tài khoản test lập, xong dọn sạch — DB về đúng 81 phiếu / 98 dòng / 0 log):
  Sửa → đổi SL 2→5, Thành tiền tự tính 15.000.000 và 3 dòng tổng đổi theo → **Gửi duyệt** (lưu
  thật) → footer đổi đúng nhóm nút → **TP duyệt** (popup ý kiến) → về danh sách → **KS duyệt giá**
  → **In phiếu** (popup xem trước, mẫu ERP 417, đủ 4 cột tiền + khối ký) → **popup Lịch sử ở màn
  danh sách** (mới → cũ, cũ đỏ → mới xanh) → **Xóa** (popup xác nhận, 82 → 81 phiếu).
  Console cuối cùng: **0 lỗi**.

### 5 lỗi THẬT tự phát hiện khi nghiệm thu và đã sửa

| # | Lỗi | Sửa |
| --- | --- | --- |
| 1 | Lịch sử báo nhầm **"xoá sạch file + toàn bộ dòng dịch vụ"** ở mọi lần lưu | `logCatalogUpdate()` của trait tự dựng snapshot SAU bằng `$model->{$column}` nên 2 khoá ẢO ra `null`. Thay bằng `logUpdateWithRows()` tự so 2 snapshot đầy đủ |
| 2 | Cùng một thao tác duyệt sinh **2 mốc trùng nhau**, cả 2 đều in "Trạng thái: A → B" | Bỏ `status` khỏi mốc "Thay đổi thông tin" khi đã có mốc "Thay đổi trạng thái" riêng |
| 3 | **Bản in ra 3 dòng tổng = 0** | Bản in đọc `summary` JSON mà form FE không gửi. BE **tự tính** `buildSummary()` khi lưu, không nhận từ FE |
| 4 | Nút **Xóa bấm không phản ứng**, không lỗi gì | `apiDeleteMethod(context, url)` nhận url dạng **CHUỖI** (khác `apiPost/PutMethod` nhận object) → URL thành `[object Object]` → 404 |
| 5 | 2 cảnh báo Vue **`errors` đã được định nghĩa** | `errors` là computed TOÀN CỤC của vee-validate. Đổi sang `formError` (tên chuẩn CLAUDE.md) và prop `fieldErrors` |

Thêm 1 khiếm khuyết UX đã vá: màn Chi tiết/Sửa **không có trạng thái "đang tải"** nên trong lúc chờ
API hiện "Không có file đính kèm." + "Chưa có dòng dịch vụ nào." màu đỏ, nhìn như phiếu rỗng.

- **Phase 8 XONG** (23/09).

### Đối chiếu phạm vi dữ liệu HRM vs ERP — **292/298 phép so KHỚP**

Script mô phỏng nguyên văn `searchByFilter()` của ERP (quyền chỉ đọc guard `web`) rồi so tập id
với bản HRM, trên **149 nhân viên** (113 người thực sự giữ 1 trong 3 quyền xem theo cấp) × 2 preset.

| Preset | Khớp |
| --- | --- |
| `all` (tổng hợp) | 143/149 |
| `for-approve` (chờ tôi duyệt) | **149/149** |

**1 lỗi tìm ra và đã sửa nhờ phép so này**: preset `for-approve` của tôi ban đầu **không lọc phòng
ban** cho Trưởng phòng, nên TP phòng A nhìn thấy phiếu chờ duyệt của phòng B. Nguyên nhân: ERP tự
mâu thuẫn — `searchByFilter()` CÓ lọc phòng nhưng `canDepartmentApprove()` lại comment tắt đoạn
kiểm đó, và tôi đã bám nhầm vế thứ hai. Đã sửa để khớp ERP ở cả 2 vế.

**6 chỗ còn lệch, đều là hành vi của cơ chế DÙNG CHUNG, không phải lỗi màn:**

| Số người | Nguyên nhân | Kết luận |
| --- | --- | --- |
| 5 | Có role **Super admin (18)** — seeder gán quyền api 1586-1588 cho role này (đúng khuôn `AdditionAccountingRequestPermissionSeeder`), và trait cũng cho Super admin qua mọi cấp | **Chủ ý**, giữ nguyên |
| 1 (#105 Bùi Duy Trước) | Trait `ChecksEmployeePermission::manageableDepartmentIds()` cộng thêm **phòng của chính mình**, ERP chỉ lấy pivot `employee_manage_departments`. #105 quản lý phòng 85 (0 phiếu) nhưng thuộc phòng 95 (51 phiếu) → HRM 51, ERP 0 | **Chờ user quyết** — sửa là đụng trait dùng chung của nhiều màn Finance |

### Checklist tự kiểm

- [x] 8 lệnh grep của skill: **sạch cả 8** (`status-pill` · `disabledTitle` · `action.key ===` ·
      `V2BaseFilterPanel` · `advanced-filters` · autocomplete tự chế · `V2BaseSelectRemote` thiếu
      `height` · slot `#field-*` tự vẽ `V2BaseLabel`)
- [x] Toast dùng **nguyên văn QLDA**: `Thêm mới thành công.` (003) · `Cập nhật thành công.` (004) ·
      `Xóa thành công.` (005) · `Không có dữ liệu phù hợp.` (011)
- [x] Chạy lại 2 kịch bản BE end-to-end sau khi sửa phạm vi: `contracted_qty` vẫn giữ 1.5; từ chối
      ghi đúng `comment`/`ks_comment` theo nấc; duyệt lại giá → 3; hủy → 8; xóa file 2→1.
      Mốc `update` nay **không còn liệt kê "Trạng thái"** (đã tách sang `change_status`)
- [x] Phiếu ERP đổi sang trạng thái 6/7 hiển thị đúng ("Đang lập hợp đồng" / "Đã lập hợp đồng")
- [x] Dọn sạch: DB về **81 phiếu / 98 dòng / 0 log**

### Còn treo, chờ user quyết

1. ✅ **Ô lọc 32px — ĐÃ XỬ LÝ 23/09**: tài liệu sai, không phải code. Chuẩn `--ff-h` hạ 36px → 32px
   bằng commit `2a6e59432` (22/09 **14:28**) trong khi skill viết lúc **10:31** cùng ngày. User chốt
   sửa tài liệu theo code; đã cập nhật `list-page/SKILL.md` + `erp-to-hrm-screen/SKILL.md` +
   `references/khuon-man-mau.md` về 32px, và đổi `height="36px"` → `32px` trong `BuyServiceDetailTable`.
2. ✅ **Phòng của chính mình trong `manageableDepartmentIds()` — user chốt GIỮ NGUYÊN (phương án A,
   23/09)**. Đây là quy ước chung của phân hệ Tài chính (8 entity + 1 service, 3 màn hàng giữ có bản
   chép riêng cũng vậy); sửa là đổi hành vi 9 màn đang chạy → tách việc riêng có QA. Đã ghi vào
   docblock `applyAllScope()`, `design.md` và spec §4.1 để QA không báo nhầm là bug.
3. ⏳ **Cột Nhà cung cấp trống ở local** do dump thiếu `customers`; phải nghiệm thu trên cổng dev.
- **Ghi chú dữ liệu (user xác nhận 22/09):** dump `gop_db` ở máy dev **thiếu dữ liệu `customers`**
  → `supplier_id` của bảng chi tiết chỉ khớp 2/91 dòng ở local (khớp `erp_dev_24_09.customers` 52
  dòng). **KHÔNG phải lỗi dữ liệu thật**, trên dev/prod đủ. Không remap gì cả; khi nghiệm thu cột
  Nhà cung cấp phải test trên cổng dev, đừng kết luận theo local.
- **Blocked:** không.
