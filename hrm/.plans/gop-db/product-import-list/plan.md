# Plan — Phiếu nhập hàng: quyền 4 mức + lọc + tùy chỉnh cột

## Phase 1 — BE Quyền 4 mức
- [x] 1.1 Seeder: thêm dòng `Permission::create` id **1546** "Xem phiếu nhập hàng theo bộ phận" (guard api, group 'Phiếu nhập hàng', sort_order 4) ngay sau 1545.
- [x] 1.2 Chèn thẳng vào DB gộp 4 dòng id 1543/1544/1545/1546 (guard api) — khớp seeder.
- [x] 1.3 `ProductImport`: thêm hằng `PERMISSION_VIEW_PART`, import `EmployeeManagePart`, thêm `$managePartCache`, method `isPartManager()` + `managePartIds()` (mirror ProductImportRequest).
- [x] 1.4 `ProductImport::applyViewScope()`: thêm nhánh `elseif isPartManager → whereIn('part_id', managePartIds()) `.
- [x] 1.5 `ProductImport::canView()` (single record): thêm nhánh part.
- [x] 1.6 `php -l` sạch.

## Phase 2 — BE Bộ lọc mở rộng
- [x] 2.1 `ProductImportService::searchByFilter`: nhận thêm `company_id`, `department_id`, `part_id`, `employee_id`(=created_by), `start_date`/`end_date` (created_at), giữ type/status/code. `applyViewScope` vẫn chạy (AND). Thêm `->with('creator.info')` cho cột Người lập.
- [x] 2.2 Type options cho FE — route `GET finance/product-imports/filter-options` (`ProductImportController::filterOptions()` trả `types` + `statuses`). `ProductImportListResource` thêm `creator_name`.
- [x] 2.3 `php -l` sạch.

## Phase 3 — FE Bộ lọc
- [x] 3.1 `pages/finance/product-imports/index.vue`: thay `V2BaseSmartFilterPanel` → `V2BaseFilterPanel` + slot `#advanced-filters` mirror màn xuất (keyword, `V2BaseCompanyDepartmentFilter` công ty/phòng ban/bộ phận + người lập, loại, trạng thái, khoảng ngày).
- [x] 3.2 buildParams gửi đủ param mới; thêm `filterStateMixin` key `finance_product_imports` + `CheckPermission`; `permissions` build từ 4 quyền "Xem phiếu nhập hàng theo …"; `fetchTypeOptions()` gọi `/filter-options`.

## Phase 4 — FE Tùy chỉnh cột
- [x] 4.1 Thêm `ColumnCustomizationModal` (`table=finance_product_imports`), nút cấu hình cột trong `#actions`.
- [x] 4.2 `getFields()` GET `human/column-customizations/detail`, `defaultTableColumns`/`tableColumns` với `isVisible`/`locked` (STT + Hành động locked), thêm cột `creator_name` (Người lập). Giữ đúng biến pagination `currentPage/pageSize` của màn nhập.

## Phase 5 — BE Bỏ role-18 bypass (thống nhất 1 cơ chế 4 quyền)
- [x] 5.1 `ProductImport::canView()`: bỏ nhánh `if (currentEmployeeIsSuperAdmin()) return true;`.
- [x] 5.2 `isBigBoss()/isBoss()/isManager()/isPartManager()`: bỏ vế `currentEmployeeIsSuperAdmin() ||` — chỉ còn 4 quyền `PERMISSION_VIEW_*`. Giữ trait `ChecksEmployeePermission` làm hàm đọc quyền (đúng cho gop_db, KHÔNG đổi sang helper global bị bug model_type).
- [x] 5.3 `php -l` sạch. Hệ quả: role 18 (DNS admin) KHÔNG còn tự thấy hết — phải gán "Xem phiếu nhập hàng theo tổng công ty" qua màn Phân quyền.

## Phase 6 — Rebase gop_db + đồng bộ DB (đổi id do đụng dải với đồng nghiệp)
- [x] 6.1 Rebase `origin/gop_db` (cả 2 repo): resolve 3 conflict hrm-api (FinanceServiceProvider + Routes/api.php additive; seeder đụng id). Đồng nghiệp đã chiếm dải 1539-1556 → **dời 2 nhóm của mình: Đề nghị nhập kho 1539-1542 → 1557-1560, Phiếu nhập hàng 1543-1546 → 1561-1564** (gate theo TÊN nên id đổi không ảnh hưởng phân quyền). Push xong cả 3 repo.
- [x] 6.2 Re-seed `PermissionsTableSeeder` trên DB gộp `erp_hrm_check` để DB khớp code: backup 2 bảng `permissions`+`role_has_permissions` ra scratchpad trước; api perms 699→722 (bổ sung quyền đồng nghiệp thiếu ở local), pivot giữ nguyên 5458. Nhóm "Phiếu nhập hàng" nay ở **1561-1564**.
- [x] 6.3 Dọn 2 dòng gán rác của role 18 (id cũ 1539/1543 sau reseed trỏ nhầm sang quyền đồng nghiệp) → pivot 5458→5456.

## Phase 7 — UI Redmine #11401 (Phiếu nhập hàng: Lỗi UI)

> Redmine #11401 `[ERP => HRM] - Kế toán - HH-DV-VC - Nhập hàng - Phiếu nhập hàng: Lỗi UI`.
> Màn `/finance/product-imports` (danh sách + chi tiết).
>
> **Quyết định mapping 3 "người" (theo từ vựng nghiệp vụ + chuỗi chứng từ nguồn):**
> - **Người tạo** = người lập Phiếu nhập hàng (`product_imports.created_by`) — ĐỔI NHÃN từ "Người lập".
> - **Người yêu cầu** = người lập **Yêu cầu nhập hàng (YCNH)** nguồn = `product_import_requests.created_by`.
>   Đường B (`is_import_direct=1`): qua `product_import_request_id`. Đường A: qua chuỗi
>   `warehouse_import → warehouse_import_request → product_import_request` (mirror `resolveSourcePir`).
> - **Người đề nghị** = người lập **Đề nghị nhập kho (ĐNNK)** nguồn = `warehouse_import_requests.created_by`
>   (đường A: qua `warehouse_import.warehouse_import_request_id`). Đường B không có ĐNNK → null.
> - **Phòng ban yêu cầu** = `department_id` của YCNH nguồn.

### Phase 7 BE
- [x] 7.1 `ProductImport` entity: thêm quan hệ đọc tên: `updater()` (`updated_by`→Employee), `customer()`
      (`customer_id`), `warehouse()` (`warehouse_id`→bảng `warehouses`), `warehouse_import()`
      (`warehouse_import_id`). Thêm helper resolve chuỗi nguồn: `sourceRequest()` (YCNH — đường B trực
      tiếp, đường A truy ngược qua WI→WIR), lấy `requester` (YCNH.creator) + `requester_department_id`;
      `sourceProposal()` (ĐNNK — đường A qua WI.warehouse_import_request_id), lấy `proposer`
      (ĐNNK.creator). Đọc bằng `DB::table` cho bảng READ-ONLY (WI/WIR `$guarded=['*']`).
      > **LỆCH KHỎI PLAN (đã chốt lúc code):** entity CHỈ thêm quan hệ `updater()`. Các tên còn lại
      > (customer/warehouse/warehouse_import + chuỗi nguồn requester/proposer/phòng ban) resolve
      > **BATCH bằng `DB::table` trong Service** (`enrichListData()` + `pluckByIds()` +
      > `applySourcePirFilter()`), KHÔNG thêm 4 quan hệ + `sourceRequest()`/`sourceProposal()` như plan
      > viết literal. Lý do: tránh N+1 trên danh sách phân trang; né gotcha bảng-trùng-tên của gop_db;
      > theo tiền lệ `DB::table` sẵn có trong `ProductImportDetailResource`.
- [x] 7.2 `ProductImportService::searchByFilter`: bổ sung filter mới (AND, trong `applyViewScope`):
      `warehouse_id` (kho hàng), `end_date` đã có → thêm alias "Ngày tạo đến", `product_keyword`
      (tên-mã hàng hóa — `whereHas` dòng `products.request_detail` theo `product_name`/`code` LIKE, hoặc
      subquery `product_import_details`+`product_import_request_details`), `partner_id`/`customer_id`
      (đối tác), `proposer_id` (Người đề nghị — lọc theo ĐNNK.created_by qua join WI→WIR),
      `requester_id` (Người yêu cầu — lọc theo YCNH.created_by), `requester_department_id` (Phòng ban
      yêu cầu — YCNH.department_id), `contract_code` (số hợp đồng — LIKE trên chứng từ HĐ nguồn),
      `warehouse_import_code` (mã phiếu nhập kho — LIKE `warehouse_imports.code`). Giữ type/status/code/
      company/department/part/employee(created_by)/start_date.
- [x] 7.3 `searchByFilter`: thêm **sort** (`sort_by` + `sort_dir`) cho cột `code` (Mã YCXH/Mã phiếu),
      `customer` (Khách hàng), `type` (Loại) — whitelist cột, mặc định `orderByDesc('id')`.
- [x] 7.4 `searchByFilter`: thêm eager-load cho các field mới của Resource (`creator.info`, `updater.info`,
      quan hệ warehouse/customer) — tránh N+1 (CLAUDE.md hiệu năng).
- [x] 7.5 `ProductImportListResource`: ĐỔI `creator_name` giữ nguyên (Người tạo); thêm `updater_name`,
      `requester_name`, `proposer_name`, `requester_department_name`, `customer_name`/`partner_name`,
      `contract_code`, `warehouse_name`, `warehouse_import_code`. Thêm **`status_text` + `status_color`**
      (hex 9 màu chuẩn: DA_HOAN_THANH=1→`#16A34A`, DANG_TAO=3→`#64748B`) cho V2BaseBadge. Bỏ phụ thuộc
      FE map số→màu. `status_name` model đã trả "Đã hoàn thành" (đúng yêu cầu đổi chữ).
- [x] 7.6 `ProductImportController::filterOptions()`: bổ sung nguồn option cho filter mới (kho hàng,
      đối tác, người yêu cầu/đề nghị, phòng ban yêu cầu) — hoặc để FE dùng API danh mục dùng chung sẵn có
      (quyết định lúc code theo pattern màn `warehouse-import-requests`). `php -l` sạch.
      > **CHỐT:** theo mirror sibling — `filterOptions()` (đẩy logic xuống `ProductImportService::filterOptions()`
      > cho controller MỎNG) trả **SCOPED-DISTINCT**: chỉ giá trị CÓ THẬT trong phiếu thuộc phạm vi quyền
      > (`applyViewScope`) → `warehouses`/`partners`/`requesters`/`proposers`/`requester_departments`
      > (+ `types`/`statuses` cũ). Danh sách gọn nên FE KHÔNG cần search server-side. Người tạo vẫn qua khối
      > Công ty–Phòng ban (org filter), KHÔNG trả riêng. Nhãn NV chuẩn qua `employeeOptionLabel()`.
- [x] 7.7 `ProductImportDetailResource`/`getData($id)`: eager-load + trả thêm updater_name/requester/
      proposer cho màn chi tiết (đủ dữ liệu render nhãn mới + đồng bộ với danh sách).

### Phase 7 FE — danh sách `pages/finance/product-imports/index.vue`
- [x] 7.8 Đổi nhãn cột: "Người lập"→**"Người tạo"** (`creator_name`, dòng ~241), "Ngày lập"→**"Ngày tạo"**
      (`created_at`, dòng ~242).
- [x] 7.9 Thêm cột (khai `defaultTableColumns` + slot cell): **Ngày cập nhật** (`updated_at`),
      **Người cập nhật** (`updater_name`), **Người yêu cầu** (`requester_name`), **Người đề nghị**
      (`proposer_name`). Cột mặc định ẩn/hiện theo `ColumnCustomizationModal` như các cột hiện có.
- [x] 7.10 **Sort**: bật sort cho cột `code` (Mã), `customer` (Khách hàng), `type` (Loại) — dùng cơ chế
      sort của `V2BaseDataTable`, `buildParams` gửi `sort_by`/`sort_dir`.
- [x] 7.11 **Migrate status-pill → `V2BaseBadge`**: thay `<span class="status-pill">` (dòng ~87-91) bằng
      `<V2BaseBadge :color="item.status_color">{{ item.status_text }}</V2BaseBadge>`; gỡ `statusPillClass()`
      + CSS `.status-pill`. Sửa `statusOptions` label "Hoàn thành"→"Đã hoàn thành" (đồng bộ BE).
- [x] 7.12 **Filter**: bổ sung ô lọc (khai `filterFields` + `buildParams`): Kho hàng, Loại yêu cầu
      (=type), Tên-mã hàng hóa, Đối tác, Người đề nghị, Người yêu cầu, Phòng ban yêu cầu, Ngày tạo đến,
      Số hợp đồng, Mã phiếu nhập kho. Giữ Công ty/Phòng ban/Người tạo/Trạng thái. Placeholder theo skill
      `list-page` (đã bật floating → bỏ placeholder trùng nhãn). Select nhân viên theo khuôn
      `employeeOptionText` (skill select-and-input-state).

### Phase 7 FE — chi tiết `pages/finance/product-imports/_id/index.vue`
- [x] 7.13 Đổi nhãn "Ngày lập"→"Ngày tạo" (dòng ~15, ~61); thêm nhãn **Người tạo** (`creator_name`),
      **Ngày cập nhật**, **Người cập nhật**, **Người yêu cầu**, **Người đề nghị** vào khối "Thông tin chung"
      (khớp cột màn danh sách — CLAUDE.md: chi tiết khớp danh sách).

## Phase 8 — Lịch sử thay đổi (skill entity-history)

> Làm ĐỦ 2 NƠI (§5.1): popup ở màn danh sách + mục "Lịch sử" ở màn chi tiết. Dùng biến thể
> `catalog_histories` dùng chung (`LogsCatalogHistory` trait + `CatalogHistoryService`), KHÔNG route
> đọc mới (endpoint `catalog-histories/{table}/{id}` + `/filter-options` đã có). Mirror sibling
> `WarehouseImportRequestService` + màn `warehouse-import-requests`.

### Phase 8 BE
- [x] 8.1 `ProductImportService`: `use LogsCatalogHistory;` + `catalogTable()` = `'product_imports'` +
      `catalogColumns()` = `['type', 'warehouse_id', 'note', 'details_rows']` (**KHÔNG có `status`** — §3a).
- [x] 8.2 `catalogDisplay()`: `details_rows`→`is_array?:[]`; `type`→`ProductImport::TYPE_NAMES`;
      `warehouse_id`→`warehouses.name`; `note` nguyên. Helper `detailRows(ProductImport)`: đọc
      `product_import_details` (parent_id) JOIN `product_import_request_details`
      (`product_import_request_detail_id`) lấy `product_name`/`code`/`unit_name`/`unit_id`; `__key` =
      `product_id|unit_id`, `__name`=product_name, cột `Mã hàng`/`ĐVT`/`Số lượng` (numText). `numText()`
      + `statusText()` (từ `ProductImport::STATUSES`) + `logStatusChanged()` (§3a) — copy khuôn sibling.
- [x] 8.3 Hook log vào `store()`: sau khi dựng dòng hàng (trước `return $obj->fresh()`), gán
      `$obj->details_rows = $this->detailRows($obj)` (khoá ẢO — KHÔNG save) rồi `logCatalogCreate($obj)`;
      nếu tạo thẳng trạng thái hoàn thành thì `logStatusChanged` từ 0. (§3)
- [x] 8.4 Hook log vào `update()`: chụp `$before = catalogSnapshot()` (+`$before['details_rows']=detailRows`)
      và `$statusBefore` TRƯỚC `fill`; sau khi save + rebuild dòng: gán `details_rows` mới,
      `logCatalogUpdate($obj, $before)` + `logStatusChanged($obj, $statusBefore)`.
- [x] 8.5 `CatalogHistoryService::TABLES`: thêm `'product_imports' => ['label' => 'phiếu nhập hàng',
      'columns' => ['type'=>'Loại nhập','warehouse_id'=>'Kho nhập','note'=>'Ghi chú',
      'details_rows'=>'Bảng chi tiết hàng hóa']]`. `php -l` sạch.

### Phase 8 FE
- [x] 8.6 Danh sách `index.vue`: import `CatalogHistoryModal`, khai `<CatalogHistoryModal ref="historyModal"
      modal-id="history-product-import" record-prefix="Phiếu nhập hàng" />`; thêm item ⋮
      `{key:'history', title:'Xem lịch sử', icon:'ri-history-line'}` (luôn hiện, không gate) vào
      `getRowActions`; `handleRowAction` thêm case `history` → `this.$refs.historyModal.open('product_imports', item.id, item.code)`.
- [x] 8.7 Chi tiết `_id/index.vue`: import `SystemInfoSection`, chèn
      `<SystemInfoSection class="mb-3 d-print-none" entity-type="product_imports" :entity-id="importId"
      endpoint-base="catalog-histories" />` trước thanh hành động.

### Phase 7+8 kiểm thử
- [x] V.1 `php -l` toàn bộ file BE sửa (ProductImportService + CatalogHistoryService: sạch).
- [x] V.2 Playwright MCP (`http://127.0.0.1:3000`) — ĐỌC/UI verified 2026-09-28:
      - Danh sách `/finance/product-imports`: đủ cột (STT, Mã phiếu, Loại, Đối tác, Người tạo, Ngày tạo,
        Người yêu cầu, Người đề nghị, Người cập nhật, Ngày cập nhật, Ngày duyệt, Trạng thái, Hành động);
        icon sort trên Mã/Loại/Đối tác; badge "Đã hoàn thành" (V2BaseBadge, màu BE); placeholder
        "Tìm theo mã phiếu"; hành động ⋮ "Xem lịch sử" → modal `Lịch sử thay đổi: PNH-14585` mở OK,
        endpoint `catalog-histories/product_imports/{id}` + `/filter-options` = 200.
      - Chi tiết `/finance/product-imports/14585`: nhãn "Người tạo/Ngày tạo/Người cập nhật/Ngày cập nhật/
        Người yêu cầu/Người đề nghị/Ngày duyệt" đúng; badge tiêu đề "Đã hoàn thành"; mục "Lịch sử" nhúng
        (SystemInfoSection) bấm "Xem lịch sử" → fetch 200, có nút "Làm mới"/"Thu gọn".
      - Bản ghi cũ (PNH-14585, tạo trước khi thêm log) hiển thị "Chưa có lịch sử thao tác nào." — ĐÚNG.
- [x] V.2b Live write-path — ĐÃ chạy thật trên DB local (`erp_new` @127.0.0.1, root/no-pw) 2026-09-28,
      user đồng ý "test trên db local thì cứ làm". Không dựng phiếu mới (data toàn status=1 đã hoàn thành,
      tạo mới sẽ ghi tồn/hạch toán) — thay vào đó gọi thẳng các method Phase 8 (detailRows/catalogSnapshot/
      logCatalogCreate/logCatalogUpdate/logStatusChanged) qua reflection trên phiếu PNH-14585, ghi THẬT vào
      `catalog_histories` rồi xoá sạch. KẾT QUẢ đúng chuẩn skill:
        • create → snapshot đầy đủ, `type` dịch ra tên, `details_rows` = mảng bản ghi (__key `product_id|unit_id`
          + __name + Mã hàng/ĐVT/Số lượng) cho 5 dòng hàng.
        • change_status → dòng RIÊNG "Đang tạo → Đã hoàn thành" (không lẫn nhóm "Thay đổi thông tin").
        • update → chỉ liệt kê trường đổi (Ghi chú null→mới); details_rows giữ nguyên → KHÔNG sinh diff.
      Không lỗi runtime (set `details_rows` ảo lên model không save → không "Unknown column"; catalogDisplay
      trả mảng OK). changed_by rỗng do tinker không login được (không phải lỗi code; HTTP thật có auth()->id()).
      Đã xoá 3 dòng test, `catalog_histories` (product_imports) về 0 như baseline.

## Phase 9 — UI Redmine #11402 (Phiếu nhập hàng: Lỗi UI 2)

> Redmine #11402 — follow-up 5 lỗi UI màn `/finance/product-imports` (giao "Trần Cư").
> **Quyết định (user 2026-09-28):** Bug 2 = thêm nút "Tạo mới" **làm y ERP** (form trống + chọn nguồn
> ngay trong form, ĐỦ 2 nguồn: phiếu yêu cầu nhập hàng + phiếu nhập kho). Bug 4 = tái dùng cơ chế in
> popup có sẵn (ReportPrintPreviewModal + reportPrintPreviewMixin). Bug 1/3/5 tự quyết theo đề nghị.
> Mẫu để copy: sibling `product-import-requests` (list + detail + service + controller + routes).
> **Lưu ý phát sinh (khảo sát):** nguồn 2 (`warehouse_imports`) HRM CHƯA có endpoint list → phải viết mới.

### Bug 1 — Đồng bộ danh sách "Loại phiếu nhập hàng" theo ERP (bỏ id 1/5/12/13/16)
- [x] 9.1 BE `ProductImportService::filterOptions()` (dòng ~608): thêm hằng
      `FILTER_TYPE_IDS = [2,3,4,6,7,8,9,10,11,14,15,99]` (= tập hiệu lực ERP `ALL_IMPORT_TYPES` trong
      `ERP/public/js/constant.js:241-251`, giao với `ProductImport::TYPE_NAMES` — bỏ 5 loại chết
      1/5/12/13/16). Đổi `'types' => optionListFromMap(TYPE_NAMES)` → lọc TYPE_NAMES theo `FILTER_TYPE_IDS`
      (giữ thứ tự). **GIỮ NGUYÊN `TYPE_NAMES` đầy đủ** để `getTypeNameAttribute` (dòng ~223) vẫn hiển thị
      đúng tên loại của phiếu cũ mang loại chết. FE (`index.vue:473` map `d.types`) KHÔNG đụng. `php -l`.
      > id 20 (loại sinh từ HĐ HRM) hiện KHÔNG có trong HRM `TYPE_NAMES` → ngoài phạm vi ticket, không thêm.

### Bug 5 — Thêm sort cột "Ngày" (Mã/Loại đã có ở Phase 7)
- [x] 9.2 BE `ProductImportService::searchByFilter` whitelist sort (7.3): thêm khoá `created_at` (Ngày).
      FE `index.vue`: bật sortable cho cột `created_at` (Ngày tạo) + `buildParams` map `sortKeyMap`
      thêm `created_at:'created_at'`. Mã (`code`)/Loại (`type`)/Đối tác (`customer`) đã bật ở Phase 7.

### Bug 3 — "Xuất Excel toàn bộ danh sách" (copy sibling product-import-requests)
- [x] 9.3 BE route `Modules/Finance/Routes/api.php` nhóm `/product-imports` (dòng ~451-468): thêm
      `Route::get('/export-rows', [ProductImportController::class, 'exportRows'])` **TRƯỚC** `/{id}`.
- [x] 9.4 BE `ProductImportController::exportRows()` — copy khuôn `ProductImportRequestController:386-406`
      (page≥1, limit=min(5000,max(1,input('limit',2000))), parse `fields` CSV, trả
      `{headings,widths,rows,total,page,limit}`).
- [x] 9.5 BE `ProductImportService`: thêm `const EXPORT_COLUMNS` + `exportRows(Request,$fields,$page,$limit)`
      — copy khuôn `ProductImportRequestService:262/313-354`, dùng `searchByFilter()` (giữ applyViewScope),
      cột theo `enrichListData()` hiện có của màn nhập (Mã/Loại/Đối tác/Người tạo/Ngày tạo/Người yêu cầu/
      Người đề nghị/Trạng thái…), STT chạy tiếp qua trang. `php -l`.
- [x] 9.6 FE `index.vue`: import `exportListFile` từ `@/utils/export/listExportFile`; state `exporting`+
      `exportProgress`; computed `exportButtonText`; nút `V2BaseButton` (icon `ri-file-excel-2-line`) trong
      `#actions`; method `exportExcel()` gọi `exportListFile({store,endpoint:'finance/product-imports/export-rows',
      filters,...})` — copy `product-import-requests/index.vue:82-94/679-718`. **Dùng `buildParams()` làm
      filters (map keyword→code, sort_by→token) rồi xoá page/per_page**, không dùng `{...this.filters}` thô.

### Bug 4 — Nút In popup (action column danh sách + màn chi tiết)
- [x] 9.7 BE route: thêm `Route::get('/{id}/print-data', [ProductImportController::class, 'printData'])`
      TRƯỚC `/{id}` (nhóm `/product-imports`).
- [x] 9.8 BE `ProductImportController::printData($id)` — copy khuôn `ProductImportRequestController:435-448`
      (findForShow → canView 403 → service->printData 404 → `['template'=>$html]`).
- [x] 9.9 BE `ProductImportService`: `const PRINT_TEMPLATE_ID = 47` (= ERP `ReportTemplate::PHIEU_NHAP_HANG`,
      `ERP/app/Model/Common/ReportTemplate.php:55`); `printData($model)` load `report_templates` id 47 +
      `fillReport()`; `buildPrintData()` **port từ ERP `app/Model/Warehouse/ProductImport.php`
      `getPrintDataAttribute()`** (đọc placeholder lúc code); letterhead: template 47 nếu có `{{HEADER}}` thì
      đổ `erpAssetUrl($company->header)` theo công ty người tạo (khuôn `ProductImportRequestService:483-501`);
      nếu template KHÔNG có `{{HEADER}}` → dùng trait `PrintsCompanyLetterhead::headerUrl()` (khuôn
      `BillIncomePrintService`). Quyết định lúc đọc template. `php -l`.
- [x] 9.10 FE `index.vue`: import + đăng ký `ReportPrintPreviewModal` + `reportPrintPreviewMixin`; render
      `<ReportPrintPreviewModal>`; `getRowActions()` thêm `{key:'print',title:'In',icon:'ri-printer-line'}`;
      `handleRowAction()` case `print` → `openPrintDetail('finance/product-imports', item.id, 'Xem trước phiếu nhập hàng')`.
- [x] 9.11 FE chi tiết `_id/index.vue`: import + mixin + modal; thêm nút In (`V2BaseButton secondary size="sm"`,
      icon `ri-printer-line`) vào thanh hành động (`.export-actionbar`, không phải V2Footer — màn này dùng
      actionbar tự dựng); method `printImport()` → `openPrintDetail('finance/product-imports', importId, ...)`.
      Nút In luôn hiện (thao tác chỉ đọc), khớp cột Hành động danh sách. Khuôn
      `product-import-requests/_id/index.vue:385/900`.

### Bug 2 — Nút "Tạo mới" + chọn nguồn trong form (làm y ERP)
> ERP: nút "Tạo mới" → form trống; trong form chọn nguồn qua popup — `is_import_direct=0` chọn "Phiếu nhập
> kho" (`warehouse_imports`), `is_import_direct=1` chọn "Phiếu yêu cầu nhập hàng" (`product_import_requests`).
> `is_import_direct` do client gửi; BE store đã validate `required_if` chéo sẵn (ProductImportStoreRequest:53-60).
- [x] 9.12 **BE nguồn 2 (warehouse_imports list picker):** route
      `GET /product-imports/warehouse-import-sources` → `ProductImportController::warehouseImportSources`;
      `ProductImportService::warehouseImportSources(Request)` list/search `warehouse_imports` (Eloquent
      `WarehouseImport::query()` select cột cần), lọc đủ điều kiện lập tương đương guard ERP
      `WarehouseImport::canApprove()` (type != NHAP_DIEU_CHUYEN, status=2, cùng company_id người đăng nhập,
      superadmin || quyền "Kế toán kho") + ô lọc mã + phân trang. Map row {id, code, type_name, warehouse_name,
      supplier_name, created_at} + helper `sourcePerPage/sourcePage/emptySourcePage`. `php -l` sạch.
      **Đổi so với spec:** map ngay trong service (không tạo `WarehouseImportSourceResource` riêng) cho gọn.
- [x] 9.13 **BE nguồn 1 (PIR list picker):** `ProductImportService::productImportRequestSources(Request)` +
      route `GET /product-imports/product-import-request-sources` + controller. Lọc `status=CHO_DUYET` +
      `is_import_direct=1` + quyền (superadmin || KE_TOAN_KHO), mirror `ProductImportRequest::canProductImport()`
      inline (đối xứng với warehouseImportSources). Map {id, code, warehouse_name, customer_name, created_at}.
      **Đổi so với spec:** KHÔNG sửa hàm dùng chung `ProductImportRequestService::searchByFilter` (CLAUDE.md:
      "hỏi trước khi sửa hàm dùng chung"). Method riêng vừa tránh đụng hàm chung, vừa đối xứng nguồn 2, vừa an
      toàn hơn — nằm trong quyền tự quyết vì đây là hướng TRÁNH sửa hàm chung. `php -l` sạch.
- [x] 9.14 FE `index.vue`: thêm nút **"Tạo mới"** (`V2BaseButton primary` trong `#actions`) →
      `createItem()` = `$router.push('/finance/product-imports/create')` (KHÔNG param). Gỡ comment "cố ý bỏ nút".
      Khớp pattern `product-import-requests/index.vue` (ungated — BE + popup nguồn tự enforce quyền/điều kiện).
- [x] 9.15 FE `ProductImportForm.vue`: thêm data `sourcePickerMode:false`; tách `loadForCreate()` thành
      `loadFromWarehouseImport(id)` (đường A) + `loadFromRequest(id)` (đường B); vào /create THIẾU cả 2 tham số
      → `sourcePickerMode=true` (KHÔNG loadError). Template nhánh `v-else-if="sourcePickerMode"`: card "Chọn phiếu
      nguồn" + 2 nút mở popup (Chọn phiếu YC nhập hàng / Chọn phiếu nhập kho) + Quay lại. Handler
      `onChooseWarehouseImport/onChooseProductImportRequest` gọi load method → loadAccountingWarehouses →
      markFormPristine. Đăng ký 2 modal trong `components:`. Luồng URL param GIỮ NGUYÊN. SCSS `.picker-hint/.picker-actions`.
- [x] 9.16 FE popup nguồn 2: `WarehouseImportSearchModal.vue` — copy khuôn `ExportRequestSearchModal.vue`
      (b-modal, ô lọc mã + Tìm, bảng click-chọn-hàng, phân trang Trước/Sau), API
      `finance/product-imports/warehouse-import-sources`, cột STT/Mã/Loại/Kho/Nhà cung cấp/Ngày, emit `choose(item)`.
- [x] 9.17 FE popup nguồn 1: `ProductImportRequestSearchModal.vue` — cùng khuôn, API
      `finance/product-imports/product-import-request-sources` (endpoint riêng, KHÔNG dùng
      `product-import-requests?only_can_product_import=1` — theo đổi ở 9.13), cột STT/Mã/Kho/Khách hàng/Ngày.

### Phase 9 kiểm thử
- [x] 9.V1 `php -l` toàn bộ file BE sửa (service + controller + routes) — sạch.
- [x] 9.V2 Playwright MCP (`http://127.0.0.1:3000`): nút Tạo mới → form vào chế độ chọn nguồn (2 nút); mở
      popup "Chọn phiếu nhập kho" (đường A) → chọn 1 phiếu hợp lệ → LOAD 200 + form populate. **BUG 422 đã fix
      + verify** (xem checkpoint dưới).
  - [x] 9.V2a Đường B picker "Chọn phiếu YC nhập hàng" → chọn 1 PYCNH → LOAD 200 + form populate. PASS (2026-09-29).
  - [x] 9.V2b In (xem trước): (1) nút In ở dòng danh sách PNH-14585 → `product-imports/14585/print-data` 200 → modal
        "Xem trước phiếu nhập hàng" render đủ; (2) nút In ở footer màn chi tiết `/finance/product-imports/14585` →
        `print-data` 200 → cùng modal render đủ (letterhead Tân Phát, tiêu đề "PHIẾU NHẬP HÀNG No: PNH-14585",
        bảng 5 SP có cột Thương hiệu, khối chữ ký). PASS (2026-09-29).
  - [x] 9.V2c Xuất Excel: nút "Xuất Excel" → `companies/letterhead` 200 → `export-rows` trang 1–8 (limit 2000, đều 200)
        → tải `Danh-sach-phieu-nhap-hang-2026-09-29.xlsx`. PASS (2026-09-29).
  - [x] 9.V2d Filter "Loại" không có loại chết: 12 loại sạch, không loại rác. PASS.

### 9.FIX Bug 422 khi chọn phiếu nhập kho nguồn (đường A) — ROOT CAUSE + FIX
- [x] Root cause: LIST picker `warehouseImportSources()` tái dùng điều kiện `WarehouseImport::canApprove()`
      (type != 5, status=2, quyền, company) nhưng đường A CÒN cần truy ngược được PHIẾU YÊU CẦU NHẬP HÀNG nguồn
      (WI → WIR → PIR). Phiếu như "Nhập tách" (type 10) thoả canApprove nhưng `WIR.product_import_request_id=NULL`
      → lọt vào picker → chọn → `getWarehouseImportSource()`→`resolveSourcePir()` ném **422** (và store cũng
      `findOrFail` PIR, kể cả ERP gốc). LIST rộng hơn LOAD+STORE = mâu thuẫn.
- [x] Fix: thêm vào query LIST `->whereHas('warehouseImportRequest', fn => whereNotNull('product_import_request_id')
      ->whereHas('productImportRequest'))` — đồng bộ điều kiện LIST với LOAD/STORE, khớp hành vi ERP (picker
      inner-join PIR). `whereHas` (subquery tự scope) tránh bẫy ambiguous-column của gộp DB.
      File: `hrm-api/Modules/Finance/Services/ProductImportService.php` `warehouseImportSources()`. `php -l` sạch.
- [x] Verify tinker (SELECT-only): company 1 picker 8→7 dòng, loại đúng WI 10599 (Nhập tách, WIR không có PIR).
- [x] Verify Playwright: picker hiện đúng 7 phiếu (không còn PNK-10599); chọn PNK-10582 →
      `GET warehouse-import-source?warehouse_import_id=10582` **200 OK** (+ accounting-warehouses 200) → form populate.

### Khoá đường B (PYCNH) theo công ty — đồng bộ với đường A (2026-09-29)
- Lý do: rà điều kiện 2 picker "Tạo mới" phát hiện BẤT ĐỐI XỨNG — đường A (phiếu nhập kho) lọc
  `company_id = công ty đang đăng nhập` ở CẢ picker LIST lẫn store (`resolveParent` nhánh WI mirror
  `WarehouseImport::canApprove()`), còn đường B (PYCNH) KHÔNG kiểm công ty ở đâu cả → user công ty A
  có quyền "Kế toán kho" lập được phiếu nhập hàng từ PYCNH của công ty B. User chốt: "khoá đường B
  theo công ty giống A".
- [x] Picker LIST `productImportRequestSources()`: derive `$currentCompanyId`, trả `emptySourcePage`
      khi `!$hasPermission || $currentCompanyId === null`, thêm `->where('company_id', $currentCompanyId)`.
      File: `hrm-api/Modules/Finance/Services/ProductImportService.php`.
- [x] Store `resolveParent()` nhánh `$isImportDirect`: sau check `canProductImport()`, thêm guard công ty
      INLINE (`$currentCompanyId` + `(int)$parent->company_id === (int)$currentCompanyId`), ném
      `ValidationException` trên `product_import_request_id` khi lệch/null. KHÔNG sửa `canProductImport()`
      dùng chung (còn dùng ở FE flags, `canDeny()`, luồng ERP-origin).
- [x] `php -l` sạch + verify tinker SELECT-only (đăng nhập giả, không ghi DB):
      · picker: emp cty1 total=9 (đúng 9 phiếu cty1, trước fix là 12), emp cty4-có-quyền total=3, emp cty4-không-quyền total=0
      · store `resolveParent`: cùng cty → trả parent; PYCNH cty4 + user cty1 → ném ValidationException "Không đủ quyền!".

### Bug #11403 — Phiếu YC nhập hàng: sau "Lưu và gửi duyệt" giá tiền không hiển thị (2026-09-29)
- Redmine #11403: màn chi tiết PYCNH hiện Đơn giá = "—", Thành tiền = 0, Tổng sau thuế = 0 sau khi lưu.
- Root cause (đã xác minh 4 tầng, KHÔNG phải lỗi lưu):
  · Data lưu đủ — PYCNH-12253 local `product_import_request_details.supplier_price = 480,158.67`.
  · `ProductImportRequestDetailResource.php:24,114` gate `supplier_price` (+ price/price_buy/allocated_price/
    extra_price/rebate_price/…) sau `currentEmployeeHasPermission('Xem giá vốn hàng hoá')` → thiếu quyền trả null.
  · Người lập PYCNH-12253 (employee 147) KHÔNG có quyền đó; quyền id 1092 guard `api` chỉ 3 role có.
  · FE màn này KHÔNG có khái niệm quyền giá vốn (form gõ tự do, detail đọc thẳng `supplier_price`) → null = "—", tổng = 0.
  · Đối chiếu ERP `warehouse/product_import_requests/show.blade.php` + controller `show()`: KHÔNG gate giá theo
    quyền cost-price nào (chỉ `canView()`); ERP không có quyền "Xem giá vốn hàng hoá". → gate là REGRESSION khi port.
- Quyết định (user chốt Hướng A 2026-09-29): bỏ gate `$canViewCostPrice` trong resource này để khớp ERP —
  `canView()` là chốt duy nhất, ai xem được phiếu thấy đủ giá.
- [x] Bỏ `$canViewCostPrice` + mọi `$canViewCostPrice ? ... : null` trong `ProductImportRequestDetailResource.php`
      (trả thẳng giá trị các cột giá: price/supplier_price/price_buy/amount_price_buy/vat_cost/allocated_price/
      extra_price/rebate_price/price_buy_approve/amount_price_buy_approve + customer.price). Đã gỡ luôn
      `use ChecksEmployeePermission` (namespace import + trait) vì không còn dùng chỗ nào trong file.
- [x] `php -l` sạch + verify tinker: render resource PYCNH-12253 khi auth=NULL (không đăng nhập = không quyền gì)
      → `supplier_price='480158.67'`, ThanhTien = 480158.67×5 = 2,400,793.35 (trước fix trả null → 0). Không ghi DB.

## Checkpoint
### Checkpoint — 2026-09-29 (đóng feature: commit fix + chạy nốt 4 kiểm thử phụ)
Vừa hoàn thành: fix bug 422 đã COMMIT (hrm-api `d096544c9`, hrm-client `1e9c7d3cf`). Chạy nốt 4 kiểm thử
phụ qua Playwright MCP để đóng feature — TẤT CẢ PASS:
  - Đường B picker (PYCNH) → LOAD 200, form populate.
  - In (xem trước): cả dòng danh sách PNH-14585 lẫn footer màn chi tiết → `print-data` 200 → modal
    "Xem trước phiếu nhập hàng" render đủ (letterhead Tân Phát, tiêu đề, bảng 5 SP, chữ ký).
  - Xuất Excel: `export-rows` trang 1–8 (đều 200) → tải file .xlsx thành công.
  - Filter "Loại": 12 loại sạch, không loại chết.
Nhiễu môi trường (không phải bug feature): socket.io :8891 ERR_CONNECTION_REFUSED (server notify không chạy),
logo :8001 ERR_BLOCKED_BY_ORB (CORS local upload-server).
Đang làm dở: (trống)
Bước tiếp theo: Feature "phiếu nhập hàng" HOÀN THÀNH. Không còn việc tồn.
Blocked: (trống)

### Checkpoint — 2026-09-28 (fix bug 422 chọn phiếu nhập kho nguồn — đường A)
Vừa hoàn thành: root-cause + fix bug 422 khi chọn phiếu nguồn ở picker "Tạo mới" (đường A). Sửa
`ProductImportService::warehouseImportSources()` — thêm ràng buộc `whereHas('warehouseImportRequest' →
product_import_request_id NOT NULL → whereHas('productImportRequest'))` để LIST khớp điều kiện LOAD+STORE
(WI phải truy ngược được PIR nguồn). Verify tinker (8→7 dòng, loại WI 10599 "Nhập tách") + Playwright
(chọn PNK-10582 → LOAD 200, form populate).
Đang làm dở: (trống)
Bước tiếp theo: CHƯA commit fix này — chờ user xác nhận commit. Các mục 9.V2 còn lại (đường B picker, In
preview, Xuất Excel tải file, filter Loại không loại chết) nên chạy lại 1 lượt nếu muốn đóng feature trọn vẹn.
Blocked: (trống)

### Checkpoint — 2026-09-28 (Phase 7+8 + verify UI)
Vừa hoàn thành: toàn bộ Phase 7 (đổi nhãn Người tạo/Ngày tạo, thêm cột Người yêu cầu/Người đề nghị/
Người cập nhật/Ngày cập nhật, sort Mã/Loại/Đối tác, badge V2BaseBadge, relabel "Đã hoàn thành") + Phase 8
(Lịch sử thay đổi qua `catalog_histories`/LogsCatalogHistory ở CẢ list modal + detail SystemInfoSection;
BE store/update hook + logStatusChanged; đăng ký `product_imports` trong `CatalogHistoryService::TABLES`).
V.1 `php -l` sạch. V.2 verify ĐỌC/UI bằng Playwright MCP: list + detail + history modal/section đều OK,
endpoint catalog-histories = 200; bản ghi cũ hiện empty-state đúng.
Đang làm dở: (trống)
Bước tiếp theo: V.2b ĐÃ xong (write-path verified thật trên DB local, đã dọn dòng test). Toàn bộ Phase 7+8
đã commit + push lên origin/gop_db (api 9e454a1f5, client 2bb5e43f2). Sẵn sàng đóng feature / chờ QA.
Blocked: (trống)

### Checkpoint — 2026-09-03 (đồng bộ DB sau rebase)
Vừa hoàn thành: re-seed permission trên `erp_hrm_check`, DB khớp code (Phiếu nhập hàng = 1561-1564, Đề nghị nhập kho = 1557-1560; không mất gán quyền). Đã backup + dọn 2 dòng rác role 18.
Đang làm dở: (trống — chờ user QA trên UI)
Bước tiếp theo: user QA màn `/finance/product-imports` (lọc theo cấp tổ chức, tuỳ chỉnh cột, cột Người lập) + gán 4 quyền "Xem phiếu nhập hàng theo…" cho role qua màn Phân quyền.
Blocked: (trống)

### Checkpoint — 2026-08-28 (hoàn thành code)
Vừa hoàn thành: toàn bộ Phase 1-4. BE (quyền 4 cấp id 1543-1546 + seeder + `applyViewScope`/`canView` nhánh bộ phận; searchByFilter mở rộng filter + creator_name; route `/filter-options`) — `php -l` sạch, 4 dòng quyền đã có trong DB gộp. FE (`index.vue` viết lại: bộ lọc mirror màn xuất + tuỳ chỉnh cột + filterStateMixin).
Đang làm dở: (trống — chờ test trên UI)
Bước tiếp theo: user kiểm thử màn Phiếu nhập hàng (bộ lọc theo cấp tổ chức, tuỳ chỉnh cột, cột Người lập). Nếu cần gán quyền cho role khác 18 → gán qua màn phân quyền (nay đã hiện nhóm "Phiếu nhập hàng").
Blocked: (trống)
