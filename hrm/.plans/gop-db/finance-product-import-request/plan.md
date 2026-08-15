# Plan — Phiếu Yêu cầu nhập hàng (ERP → HRM)

> @junfoke · nhánh `feat/finance-product-import-request` (từ `gop_db`) · design: `./design.md`

## Phase 0 — Chuẩn bị

- [x] Tạo worktree 2 repo (`hrm-api` + `hrm-client`), nhánh `feat/finance-product-import-request`
- [x] Khảo sát ERP: controller/model/blade, 12 status, 8+4 type, 5 màn list, lối vào menu + dashboard
- [x] Tra DB `gop_db` bảng `permissions` — xác định guard `web` của 7 quyền liên quan
- [x] Viết `design.md`
- [x] `composer install` (api, 105 package) + `npm install` (client, 1768 package) trong worktree
- [x] Copy `.env` sang cả 2 worktree (file gitignore nên worktree không có)
- [x] Baseline: `php artisan --version` OK (Laravel 8.83.29).
      ⚠️ `php artisan route:list` lỗi `Trying to get property 'employee_info_id' of non-object`
      (`app/Helper/PermissionHelper.php:23` — `isCurrentEmployeeHasPermission()` gọi lúc đăng ký route
      trong `Modules/Timesheet/.../RequestUpdateTimeSheetController.php:51`, CLI không có auth user).
      **Lỗi có sẵn trên `gop_db` gốc, không phải do worktree** — đã đối chiếu. Không chặn việc code.

## Phase 1 — BE nền

- [x] Merge `gop_db` (8 commit mới) vào nhánh feature ở cả 2 repo — sạch, không conflict
- [x] Tạo `Modules/Finance/Entities/ProductImportRequest/` — 5 model Phase 1:
      `ProductImportRequest` · `ProductImportRequestDetail` · `ProductImportRequestDetailCustomer` ·
      `Supplier` (bảng `customers` dùng chung NCC+KH) · `Warehouse`. KHÔNG `mysql2`.
      `Tab` / `TabProduct` / `Version` / `History` để Phase 3-4 (form + lịch sử) mới cần.
      `EmployeeManagePart` tái dùng bản của `ProductTransferRequest`, không nhân bản.
- [x] Port `searchByFilter` 4 preset: `all` / `for_approve` / `managerApprove` / `departmentManagerApprove`
      (giá trị lạ tự quy về `all`). Bỏ `accounting` + nhánh mặc định như đã chốt.
- [x] Vá lỗ hổng phạm vi: nhánh `all` `orWhere` thêm phiếu user có quyền duyệt (status 10/11 theo
      quyền BKS/BGĐ; status 12 giới hạn theo phòng ban mình quản lý)
- [x] Port 9 cờ hành động (`canView` `canEdit` `canCancel` `canApprove` `canApproveByManager`
      `canControlBoardApprove` `canBoardOfManagerApprove` `canProductImport` `canDeny`)
      + 3 cờ cấp `isBigBoss`/`isBoss`/`isManager`
- [x] `ProductImportRequestListResource` (12 cột đúng màn ERP `all`) + `ProductImportRequestDetailResource`
- [x] `ProductImportRequestService` — paginate `per_page`, `meta()`, `findForShow()`, `warehouseOptions()`
- [x] Route `GET /v1/finance/product-import-requests` + `/warehouses` + `/{id}` — KHÔNG middleware quyền,
      gate trong Entity/Controller (theo precedent; xem design mục Phân quyền)
- [x] Thêm **7** bản ghi quyền `guard_name='api'`, `type=8`, group `Yêu cầu nhập hàng` vào
      `PermissionsTableSeeder`, id **1148-1154** (seeder đang tới 1147) — 100874-877, 100984,
      100339, 100340; `Kế toán kho` đã có bản api id 1136 nên không khai lại.
      Group `Yêu cầu nhập hàng` đã kiểm: không trùng group nào (ERP dùng `Quản lý yêu cầu nhập hàng`).
- [x] Verify HTTP + đối chiếu DB — xem checkpoint bên dưới

## Phase 2 — FE danh sách

- [x] BE bổ sung phục vụ FE:
      - `GET /partners?q=&include_id=` — NCC/KH cho select2 remote (bảng `customers` rất lớn →
        tìm rồi trả tối đa 30 dòng, KHÔNG nạp cả bảng như ERP)
      - `meta` thêm 4 cờ quyền duyệt (`can_approve_accounting`, `can_control_board_approve`,
        `can_board_of_manager_approve`, `can_department_manager_approve`) → FE quyết định hiện tab nào
      - `searchByFilter` nhận thêm tên tham số kiểu HRM (`company_id`/`department_id`/
        `start_date`/`end_date`) song song tên cũ ERP, + ô tìm nhanh `keyword` (mã phiếu HOẶC tên người lập)
- [x] `pages/finance/product-import-requests/index.vue` — V2 list, preset qua `filters.type`, mặc định `all`
- [x] **Tab preset theo quyền** (`V2BaseTabNavigation`): Tất cả · Chờ tôi duyệt · Chờ BKS/BGĐ duyệt ·
      Chờ TP duyệt — chỉ hiện tab người dùng có quyền tương ứng; 1 quyền cũng không có thì ẩn hẳn
      thanh tab. Tab lưu trong `filters` nên `filterStateMixin` nhớ luôn khi quay lại từ chi tiết.
- [x] Bộ lọc 13 ô bám ERP: loại (12 giá trị), trạng thái (12), NCC, KH, kho hàng, tên/mã hàng hoá,
      số hợp đồng, người lập, người duyệt, ngày lập từ–đến, công ty/phòng ban (theo phạm vi quyền)
- [x] **Cấu hình cột hiển thị** — `columnCustomizationMixin`, `columnScreenKey =
      finance_product_import_requests`, 11 cột; `locked`: STT + Mã phiếu (cột gánh nút hành động)
- [x] Áp 4 bài học phân trang màn danh sách V2 (ép `Number`, `page`/`per_page` ngoài `filters`,
      `DedupeLoadMixin`, nút Làm mới TỰ nạp lại danh sách) + `filterStateMixin` giữ bộ lọc khi quay lại
- [x] Auto-search khi đổi filter (deep watcher), riêng ô tìm nhanh chờ bấm nút — skill `list-page`
- [x] Fill slot menu `components/subsystem-menu/finance.js` → `/finance/product-import-requests`
- [x] Nút hành động: **disable chứ không ẩn**, bọc `<span>` giữ tooltip khi nút bị khoá
- [x] Verify trình duyệt (Nuxt dev :3099 + API :8199) — xem checkpoint Phase 2 bên dưới

## Phase 3a — Form tạo/sửa (4 loại lấy nguồn từ phiếu YC xuất hàng)

> ⚠️ Phát hiện khi khảo sát: **hàng hoá KHÔNG nhập tay**. Cả 8 loại đều bắt buộc chọn 1 chứng
> từ nguồn rồi kéo hàng hoá từ đó xuống. Xem mục "Phát hiện 2026-08-14" trong `design.md`.

- [x] BE — `ProductExportRequest` + `ProductExportRequestDetail` (chỉ đọc): popup lọc theo loại
      (port 4 nhánh `searchData` của ERP) + 3 hàm dựng dữ liệu `dataForBorrowReturn` /
      `dataForSaleReturn` / `dataForOther`
- [x] BE — 2 endpoint: `GET /export-requests` (popup) và `GET /export-requests/{id}/source`
- [x] BE — `ProductImportRequestRequest`: rule 4 loại, câu lỗi tiếng Việt, decode `products` JSON
      từ multipart trong `prepareForValidation`
- [x] BE — `store` / `update`: chặn nghiệp vụ (loại 3 không trả trùng hàng, loại 4 hợp đồng phải
      hỗ trợ hạch toán + chưa quyết toán), `syncProducts` snapshot tên/mã/ĐVT, upload S3
      (`product_import_requests`), chép hợp đồng/KH từ phiếu nguồn
- [x] BE — luồng gửi duyệt: loại 4 → status 12 + báo TP; loại còn lại → `received_time` + báo Kế toán kho
- [x] BE — hook `creating`/`updating` gắn `created_by` + `company_id`/`department_id`/`part_id`
- [x] FE — `components/ProductImportRequestForm.vue` (form dùng chung cho tạo + sửa)
- [x] FE — `components/ExportRequestSearchModal.vue` (popup chọn phiếu YC xuất hàng, có phân trang)
- [x] FE — `create.vue` + `_id/edit.vue` (trang vỏ + `unsavedChildFormMixin`)
- [x] FE — trường hiện/ẩn theo loại: Kho nhập (khi không nhập thẳng) · Khách hàng (loại 14) ·
      NCC + Nhân viên (loại 99) · Vận chuyển + Số km (loại 3/4/99 khi không nhập thẳng)
- [x] FE — validate: chỉ rule ĐỊNH DẠNG chạy realtime ở FE, required do BE quyết theo `status`
      rồi trả 422 → map `formErrors` hiện inline (skill `form-validate`)
- [x] FE — `unsavedChangesMixin` + `markFormSaved()` + `markFormPristine()` cuối `loadDetail`
- [x] FE — `POST` tạo / `POST + _method=PUT` sửa (multipart), đính kèm nhiều file
- [ ] **Chưa làm (chuyển Phase 3b)**: tab "Chi phí nội địa" (ERP `has_inland_cost` = type != 3) —
      BE đã có rule `inland_costs.*`, FE chưa dựng UI
- [ ] **Chưa làm**: Huỷ phiếu nháp theo `canCancel()` — để cùng Phase 4 (chi tiết + duyệt)

## Phase 3b — 3 loại còn lại + chi phí nội địa

> ⚠️ **Loại 11 (mua nước ngoài mới) BỊ LOẠI khỏi form**, không phải hoãn: 634/634 phiếu loại này
> trên DB đều do `OrderImportRequest` sinh tự động (`OrderImportRequest.php:745`), status chỉ
> 1/4/5 (không bao giờ 3 = nháp), ERP không có nhánh `store()` cho nó và loại trừ nó khỏi
> `canEdit`/`canCancel`/`canDeny`. Nó chỉ còn sót trong dropdown ERP. → HRM chỉ hiển thị ở
> danh sách/chi tiết. Vậy tổng số loại lập được từ HRM là **7**.

- [x] BE — `BorrowSellRequest` (loại 9): popup lọc theo `canReturn()` (status 1/13, chưa có phiếu
      nhập dở, còn dòng chưa trả hết) + `dataForImport()`
- [x] BE — `InlandProductArrivedNew` (loại 15): popup lọc `status = DA_GUI` + của chính mình;
      `dataForImport()` gộp dòng theo `product_id-price-vat`, giữ `details[]` (dòng con khách hàng),
      gộp tiếp hàng khuyến mại, kèm `contract_costs`; `markRequested()` đánh dấu nguồn đã dùng
- [x] BE — `ProductArrivedNotify` (loại 2): popup lọc `canProductImportRequest()`;
      `dataForImport()` lấy dòng hợp đồng + ghi đè SL bằng `qty_arrived` (bỏ dòng SL 0), gộp KM;
      trả cờ `products_readonly` vì ERP KHÔNG cho sửa SL loại này
- [x] BE — Service điều phối 4 loại nguồn qua `TYPE_SOURCE_KIND` + `SOURCE_KIND_COLUMN`
      (mỗi nguồn lưu vào 1 cột khác nhau: `product_export_request_id` / `inland_product_arrived_new_id`
      / `notify_id` / `borrow_sell_request_id`)
- [x] BE — `source_id` thành tham số CHUNG cho mọi loại nguồn (giữ `product_export_request_id`
      cho tương thích Phase 3a); `SOURCE_TABLE_BY_TYPE` cho rule `exists`
- [x] BE — `fillFromExportRequest` mở rộng: loại 15 lấy NCC từ hợp đồng mua; loại 2 lấy NCC +
      tiền tệ từ hợp đồng mua trong nước; loại 9 chép hợp đồng đa hình (`FirmContract` /
      `WrServiceContract`) + khách hàng
- [x] BE — `syncDetailCustomers()` lưu dòng con khách hàng vào `product_import_request_detail_customers`
- [x] BE — `syncInlandCosts()` + endpoint `GET /costs` (589 danh mục chi phí)
- [x] FE — dropdown 7 loại; nhãn + placeholder + tiêu đề popup ĐỔI THEO LOẠI (`sourceLabel`)
- [x] FE — bảng hàng hoá chỉ-đọc cho loại 2; dòng con khách hàng hiện dưới dòng hàng (chỉ xem)
- [x] FE — khối "Chi phí nội địa" (ẩn với loại 3 theo ERP `has_inland_cost`), tự đổ sẵn chi phí
      hợp đồng từ chứng từ nguồn
- [ ] **Chưa port**: file đính kèm của TỪNG dòng chi phí nội địa (ERP bắt buộc) — cần thống nhất
      cách gửi multipart lồng nhau; hiện lưu chi phí không kèm file
- [ ] **Chưa port**: các khối chi phí quốc tế / NCC / phân bổ thuế của loại nhập khẩu (loại 1, 11)
      — không thuộc 7 loại lập được từ HRM

## Phase 4 — Chi tiết + duyệt

- [x] `_id/index.vue` — thông tin chung + 2 tab (Hàng hoá / Chi phí nội địa) + 3 dòng tổng cộng + lịch sử
- [x] 4 luồng duyệt: Kế toán kho (status 2) · BKS (10) · BGĐ (11) · TP (12)
- [x] Từ chối (`deny`) + chuyển BGĐ (`switch`) + 2 luồng reject (BKS/BGĐ gộp `approverReject`)
- [x] Nút hành động hiện/ẩn đúng theo cờ BE trả về
- [x] Thông báo qua `EmployeeInfoService::sendNotification` (như Phase 3)
- [x] Tab lịch sử (`product_import_request_versions` + `_histories`) — sắp mới → cũ

### Quyết định Phase 4

- **Giữ giống ERP** (user chốt): duyệt phải vào màn chi tiết, KHÔNG duyệt hàng loạt ở màn danh sách.
- **Không có nút "Huỷ phiếu"**: `cancel()` có trong Controller ERP nhưng KHÔNG view nào gọi
  (`grep productImportRequest.cancel` trong `resources/views` = 0 kết quả) → không port.
- **2 nút dẫn sang màn chưa port** (Tạo đề nghị nhập kho / Tạo phiếu nhập hàng, phân hệ Kho):
  render nhưng DISABLE kèm tooltip chỉ sang cổng ERP — theo quy ước "disable chứ không ẩn".
- **Siết 1 lỗ hổng của ERP**: `controlDepartmentManagerApprove` của ERP gán thẳng
  `$request->status` nên TP bắn giá trị bất kỳ là phiếu nhảy trạng thái sai. Bản port chỉ nhận
  2 giá trị 2 (duyệt) / 3 (không duyệt), khác đi trả 422.
- **Validate**: `ApiController` của phân hệ kế thừa `Illuminate\Routing\Controller` trần, KHÔNG
  có trait `ValidatesRequests` → dùng `validateOrFail()` cục bộ (Validator facade + ném
  ValidationException) thay vì `$this->validate()`.

### Vá 2 lỗ hổng của Phase 3b (phát hiện khi dựng màn chi tiết)

1. `DetailResource` chỉ trả `product_export_request_id` → mở Sửa phiếu loại **2 / 9 / 15** là mất
   liên kết chứng từ nguồn (3 loại đó lưu ở cột khác). Đã thêm `source_id` / `source_code` /
   `source_info` dùng chung cho cả 7 loại.
2. `DetailResource` không trả `inland_costs` mà submit luôn gửi mảng này và BE xoá-ghi lại toàn bộ
   → mở phiếu ra bấm Lưu là **mất sạch chi phí nội địa**. Đã trả về + nạp lại trong `loadDetail()`.
3. Đơn giá hiển thị là `supplier_price` (ERP dùng cột này), không phải `price`/`price_buy`.
   Cột `vat_cost` trên DB luôn rỗng (ERP không ghi, cũng không có accessor) → FE tự tính lại.

### Checkpoint — 14/08/2026 (Phase 4)

Vừa hoàn thành: toàn bộ Phase 4 + verify.

Đã verify trên trình duyệt (phiếu thật 12200 + phiếu test 12240 đã xoá sạch):
- Màn chi tiết loại 15: đúng đơn giá / thành tiền / tiền VAT / 3 dòng tổng, dòng con khách hàng,
  ô chỉ-đọc "Hợp đồng mua", file đính kèm có preview. Console 0 lỗi.
- **Không duyệt** (Kế toán kho): chặn ghi chú rỗng → nhập ghi chú → status 2 → 3, ghi chú chuyển
  sang khối chỉ-đọc, lịch sử ghi 2 dòng (Ghi chú duyệt + Thời gian trả lại).
- **BGĐ duyệt**: hiện 2 cột giá duyệt + ô nhập, chặn giá rỗng, thành tiền tính realtime,
  status 11 → 2, `price_buy_approve` 95.000 → `amount_price_buy_approve` 190.000.

Đã verify server-side bằng tài khoản có quyền thật (TP=82, BKS=147), 9 kịch bản đúng hết:
| Thao tác | Kết quả |
| TP duyệt (status 2) | 200, 12 → 2 |
| TP không duyệt, thiếu ghi chú | 422 |
| TP không duyệt, có ghi chú | 200, 12 → 3 |
| TP bắn status lạ (7) | 422 "Thao tác không hợp lệ" |
| BKS duyệt | 200, 10 → 2 |
| BKS chuyển BGĐ | 200, 10 → 11 |
| BKS không duyệt, thiếu ghi chú | 422 |
| BKS không duyệt, có ghi chú | 200, 10 → 3 |
| TP bấm nhầm endpoint BKS | 403 |

Bước tiếp theo: Phase 5 (in mẫu 44 + xuất Excel + xoá file S3).

## Phase 5 — In / Export / File

- [x] In mẫu `ReportTemplate` id 44 + `fillReport()` — BE `/{id}/print-data`, FE `_id/print.vue`
- [x] Export Excel danh sách (route `/export` khai TRƯỚC `/{id}`) — 11 cột như ERP
- [x] Đính kèm S3: xoá 1 file qua `DELETE /{id}/files`

### Quyết định Phase 5

- **Bug `deleteFile` của ERP: KHÔNG port.** ERP chạy `unlink(public_path() . $file)` trong khi file
  nằm trên S3 — vô nghĩa và có nguy cơ xoá nhầm. Bản HRM gọi `CmcS3Helper::deleteFile()`, lỗi S3
  chỉ ghi log chứ không chặn việc gỡ file khỏi phiếu.
- **`file` gửi qua QUERY param** (không phải body): axios bản này KHÔNG gửi `config.data` cho
  DELETE, và `apiDeleteMethod` của store chỉ nhận 1 tham số qua `dispatch`. Đã gặp y hệt ở
  precedent phiếu chuyển hàng.
- **Không port nhánh >2000 dòng gửi mail** (`ProductImportRequestMailJob` của ERP): HRM chưa có
  job/mail tương ứng, hàng đợi mail là hạ tầng riêng — cần chốt trước khi làm.
- **Mẫu 44 không cần `applyLetterheadHeader`** như precedent: template đã dùng `{{HEADER}}` là ảnh
  letterhead full-width ngay từ đầu.
- **Bảng hàng hoá bản in đọc snapshot** `brand_name`/`unit_name` trên dòng chi tiết thay vì quan hệ
  `$product->brand->name` như ERP — ERP **nổ 500** khi hàng hoá đã bị xoá khỏi danh mục. Mọi giá
  trị đều qua `e()` (tên hàng có `&`/`<` sẽ phá HTML bản in).

### Checkpoint — 14/08/2026 (Phase 5)

Vừa hoàn thành: toàn bộ Phase 5 + verify. Dữ liệu test (12240, 12241) đã xoá sạch.

Đã verify:
- **In**: `/12200/print` ra đúng mẫu ERP — tiêu đề, No, Ngày lập/Người lập, Loại yêu cầu, Kho nhập,
  Ghi chú, bảng 7 cột đủ 2 dòng hàng, khối ký tên. Không còn placeholder `{{...}}`. Console 0 lỗi.
- **Xuất Excel**: HTTP 200, content-type xlsx, file mở được. Kiểm tra ô: dòng 2 tiêu đề, dòng 3
  "Từ ngày 28/07/2026 đến ngày 28/07/2026", dòng 4 đủ 11 header, dòng 5 dữ liệu đúng
  (`PYCNH-12230 | Nhập hàng bán trả lại | ... | HN_DA - Đào Phúc Sơn | ...`).
- **Xoá file**: xoá đúng file và giữ file còn lại; URL không thuộc phiếu → 422; bấm từ UI (modal
  xác nhận → danh sách rỗng → cột `attachments` về NULL). Console 0 lỗi.

⚠️ **Món nợ verify trên dev** (dữ liệu local thiếu, KHÔNG phải lỗi code):
`customers` trên snapshot local có id nhỏ nhất là **14849**, trong khi phiếu ERP trỏ
`supplier_id`/`customer_id` = 34/45/59… → cột **Nhà cung cấp / Khách hàng luôn rỗng** ở danh sách,
chi tiết, bản in và Excel. Đã đối chiếu: ERP `ProductImportRequest::customer()` →
`App\Model\Sale\Customer` (không khai `$table` → suy ra `customers`), tức bản port map ĐÚNG bảng.
Phải xem lại trên dev/prod.

Bước tiếp theo: Phase 6 (verify đối chiếu 2 cổng + nhánh vá lỗ hổng phạm vi xem của người duyệt).

## Phase 6 — Verify

- [x] HTTP toàn bộ route — 16/16 route trả đúng mã
- [x] Playwright: 4 preset + tạo/sửa/gửi duyệt/chi tiết/in/export
- [x] Đối chiếu 2 cổng **ở mức code** (xem hạn chế bên dưới)
- [x] DB nguyên trạng — 0 migration, chỉ 2 file sửa (route + seeder quyền)
- [x] **Đã TRẢ món nợ Phase 1**: chứng minh được nhánh vá phạm vi xem của người duyệt
### Checkpoint — 14/08/2026 (Phase 6)

Vừa hoàn thành: toàn bộ Phase 6. Dữ liệu test (12242, 12243) đã xoá sạch, id cao nhất về lại 12230.

**1. HTTP — 16/16 route.** GET danh sách (4 preset + preset lạ tự quy về `all`), warehouses,
partners, costs, export, export-requests (+ loại không lập được → 422), show, histories,
print-data, id không tồn tại → 404, không token → 401. POST/PUT/DELETE: thiếu ghi chú → 422,
sai vai trò → 403, id lạ → 404.

**2. Luồng end-to-end trên trình duyệt** (tạo phiếu PYCNH-12242 loại 99):
chọn phiếu nguồn từ popup (33.865 phiếu, phân trang) → hàng hoá tự nạp → Lưu nháp (status 3) →
mở Sửa: **chứng từ nguồn + hàng hoá hiện lại đúng** (bản vá Phase 3b hoạt động) → sửa ghi chú →
Lưu và gửi duyệt (status 2, đóng dấu `received_time`) → màn chi tiết hiện đúng trạng thái, ghi chú,
**lịch sử 2 mốc sắp mới→cũ** → In ra đúng mẫu 44. Console 0 lỗi ở mọi bước.
Nút hành động đổi đúng theo cờ: phiếu nhập thẳng → **"Tạo phiếu nhập hàng"** chứ không phải
"Tạo đề nghị nhập kho" (khớp `canProductImport` vs `canApprove` của ERP).

**3. Đối chiếu 2 cổng — HẠN CHẾ CÓ THẬT:** không so cạnh nhau được ở máy local vì cổng ERP trỏ DB
`erp_dev_30_01_26`, còn HRM trỏ `gop_db` (2 bộ dữ liệu khác nhau); cổng ERP cũng không chạy.
Đã đối chiếu ở **mức code** bằng script so 2 codebase:
- 12/12 trạng thái trùng khớp cả **tên lẫn màu** (`STATUSES`).
- 17/17 tên loại phiếu trùng khớp (ERP `ImportModel::TYPES` vs HRM `TYPE_NAMES`).
- 20/20 hằng số loại + trạng thái trùng giá trị số.
- Dùng CHUNG bản ghi mẫu in `report_templates` id 44 và chung công thức sinh mã `PYCNH-xxxxx`.
→ **Vẫn phải so cạnh nhau trên dev** trước khi bàn giao.

**4. Món nợ Phase 1 — ĐÃ TRẢ.** Dựng được kịch bản thật để chạy nhánh `orWhereApprovable()`:
TP **emp 105** (phòng của mình = 95, quản lý thêm phòng **85**, quyền xem chỉ ở cấp phòng ban).
Tạo phiếu status 12 ở phòng 85 do người khác lập → nằm NGOÀI mọi nhánh quyền xem của TP 105.
Kết quả: TP 105 **thấy phiếu** ở cả preset `all` lẫn `departmentManagerApprove`, `canView()` = true,
`canApproveByManager()` = true. Ca âm tính: TP 233 (không quản lý phòng 85) **không thấy** phiếu.
→ Nhánh vá chạy đúng. Ghi chú: trên dữ liệu gộp hiện tại **mọi TP đều đã có ít nhất 1 quyền xem
theo cấp** (37 TP / 118 người có quyền xem, giao = 37) nên lỗ hổng chưa xảy ra thực tế — nhánh này
là phòng vệ, không phải sửa lỗi đang cháy.

### ⚠️ 2 việc cần user chốt / chuyển tiếp

**(a) Lỗ hổng phân quyền CÓ SẴN TRONG ERP — bản port giữ nguyên.**
`canApproveByManager()` của ERP chỉ kiểm tra `status == 12 && có quyền 'Trưởng phòng duyệt yêu cầu
nhập hàng'` — **KHÔNG kiểm tra phòng ban**. Đã đo thực tế: TP 233 không quản lý phòng 85 nhưng
`canView()` và `canApproveByManager()` trên phiếu của phòng 85 đều trả **true**. Tức bất kỳ TP nào
biết id phiếu đều **vào xem và duyệt được phiếu của phòng ban khác** (danh sách có lọc, nhưng link
trực tiếp thì không). **User đã chốt 14/08/2026: TẠM GIỮ NGUYÊN NHƯ ERP.** Không siết theo `manage_departments`.

**(b) NCC / KH rỗng — vấn đề TOÀN CỤC của DB gộp local, không riêng màn này.**
Số liệu đo được trên `gop_db`:
- 3.679 phiếu có `supplier_id`, chỉ **474 (12,9%)** tra được tên trên bảng `customers`.
- 2.234 phiếu có `customer_id`, chỉ **236 (10,6%)** tra được tên.
- `customers` chỉ chứa dải id **14849–32200** (12.675 dòng); dữ liệu ERP trỏ id nhỏ hơn nhiều.
- Không riêng màn này: **8.135** bản ghi `firm_contracts` cũng trỏ `customer_id < 14849`.
Đã đối chiếu: ERP `ProductImportRequest::customer()` → `App\Model\Sale\Customer`, class không khai
`$table` → suy ra bảng `customers`. Bản port map **đúng bảng**.
**User xác nhận 14/08/2026: chỉ DB local thiếu bản ghi, trên dev đủ → KHÔNG phải lỗi, đóng mục này.**

---

### Checkpoint — 2026-08-14

Vừa hoàn thành: **Phase 1 (BE nền) — XONG**. 8 file mới + 2 file sửa trong worktree `hrm-api`:

| File | Vai trò |
| --- | --- |
| `Modules/Finance/Entities/ProductImportRequest/ProductImportRequest.php` | Entity chính (~700 dòng): 12 status, 17 tên loại + 8 loại tạo / 12 loại lọc, 4 preset, 9 cờ hành động, helper quyền query pivot + memoize |
| `.../ProductImportRequestDetail.php` | Dòng hàng hoá |
| `.../ProductImportRequestDetailCustomer.php` | Dòng con khách hàng (FK `product_import_request_detail_id`) |
| `.../Supplier.php` | NCC + KH — chung bảng `customers` |
| `.../Warehouse.php` | Kho hàng |
| `Modules/Finance/Services/ProductImportRequestService.php` | paginate, meta, findForShow, warehouseOptions |
| `Modules/Finance/Http/Controllers/V1/ProductImportRequestController.php` | index / warehouses / show |
| `Modules/Finance/Transformers/ProductImportRequestResource/{List,Detail}Resource.php` | 12 cột danh sách + chi tiết |
| `Modules/Finance/Routes/api.php` (sửa) | 3 route, `/warehouses` khai TRƯỚC `/{id}` |
| `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (sửa) | 7 quyền id 1148-1154 |

Kết quả verify (server `php artisan serve --port=8199`, DB `gop_db`, user `namdangit@gmail.com` id 13 = Super admin):

| Kiểm tra | Bản port | Đối chiếu SQL thuần | |
| --- | --- | --- | --- |
| preset `all` | 12.111 | 12.111 | ✅ |
| preset `for_approve` | 31 | 31 | ✅ |
| preset `managerApprove` | 0 | 0 (DB không có status 10/11) | ✅ |
| preset `departmentManagerApprove` | 0 | 0 (4 phiếu status 12 ở phòng 120, user không quản lý) | ✅ |
| lọc `import_type=4&status=5` | 1.171 | 1.171 | ✅ |
| `GET /warehouses` | 7 kho | 7 (company 1, status 1) | ✅ |
| `GET /{id}` | đủ header + 7 dòng hàng | | ✅ |

Chạy thêm dưới 5 danh tính khác nhau (Super admin / xem theo bộ phận / BKS / TP duyệt / nhân viên
thường) — **mọi nhánh phạm vi đều sinh SQL hợp lệ, không lỗi**. Nhánh nhân viên thường chỉ thấy
phiếu của mình (2 phiếu), đúng ERP.

2 điểm đáng lưu ở bản port (đã ghi docblock tại chỗ):
- `department` vừa là CỘT varchar (phòng ban nhập tay) vừa suýt là tên quan hệ → đổi quan hệ thành
  `departmentInfo()`, Resource trả 2 trường riêng `department_text` và `department_name`.
  Dữ liệu thật chứng minh 2 giá trị này KHÁC nhau (PYCNH-12222: text "PHÒNG XUẤT NHẬP KHẨU"
  vs danh mục "PHÒNG KẾ TOÁN TÀI VỤ").
- Bảng ERP `buy_contract2` là **số ít**, không theo quy ước Laravel.

Đang làm dở: (không có)
Bước tiếp theo: **Phase 2 — FE màn danh sách** `pages/finance/product-import-requests/index.vue`
Blocked: (không có)

---

### Checkpoint — 2026-08-14 (Phase 2)

Vừa hoàn thành: **Phase 2 (FE màn danh sách) — XONG, ĐÃ VERIFY TRÌNH DUYỆT**.

File: `hrm-client/pages/finance/product-import-requests/index.vue` (mới, ~530 dòng) +
`components/subsystem-menu/finance.js` (fill slot). BE bổ sung: endpoint `/partners`,
4 cờ quyền duyệt trong `meta()`, nhận thêm tên tham số kiểu HRM, ô tìm nhanh `keyword`.

Môi trường verify: Nuxt dev `:3099` + API `php artisan serve :8199` (KHÔNG đụng cổng 3000/8000
của máy dev), DB `gop_db`, tài khoản `namdangit@gmail.com` (Super admin).

| Kiểm tra | Kết quả |
| --- | --- |
| Vào màn | 11 cột đúng thứ tự ERP · 10 dòng · **1 request duy nhất** |
| Tổng số bản ghi | "Hiển thị 1–10 / 12111 phiếu" — khớp API + SQL |
| 4 tab preset | Hiện đủ (Super admin có cả 4 quyền duyệt) |
| Đổi trang → trang 3 | "21–30 / 12111", **1 request**, KHÔNG nhảy về trang 1 |
| Tab "Chờ tôi duyệt" | 31 phiếu, toàn bộ trạng thái "Chờ duyệt", **1 request**, tự về trang 1 |
| Ô tìm nhanh `PYCNH-12222` | tab Chờ tôi duyệt → 0 (đúng: phiếu đó status "Đã đề nghị"); tab Tất cả → 1 |
| Nút Làm mới | Xoá hết ô lọc + nạp lại 12111, giữ nguyên tab đang đứng |
| Cấu hình cột | Modal 11 cột; STT + Mã phiếu **disabled** (locked); tắt "Khách hàng" → bảng còn 10 cột, STT vẫn đầu |
| Menu Tài chính | `Hàng hoá - DV - VC > Nhập hàng > Yêu cầu nhập hàng` điều hướng đúng |
| Console | **0 lỗi** |

Tổng cộng 6 thao tác → 6 request, **không có request lặp nào** (4 bẫy phân trang V2 đã tránh được).

⚠️ **1 lỗi hiển thị đã phát hiện và sửa khi verify**: cột "Loại" chỉ khai `width` mà thiếu
`minWidth` → bảng vẫn co cột lại, chữ xuống dòng từng KÝ TỰ ("Nhậ p hàn g bán trả lại"), dòng cao
~140px. Đã thêm `minWidth` cho toàn bộ cột chữ dài → dòng còn 65px, cột Loại 215px hiện đủ 1 dòng.
Bài học: **cột chữ dài phải khai cả `width` LẪN `minWidth`**, không chỉ `width`.

Đang làm dở: (không có)
Bước tiếp theo: **Phase 3 — Form tạo/sửa** (8 loại, popup chọn hàng hoá, `unsavedChangesMixin`).
Lưu ý: nút "Sửa" và link Mã phiếu ở màn danh sách trỏ tới `/create`, `/{id}/edit`, `/{id}` —
các trang này ra ở Phase 3 và Phase 4, hiện bấm vào sẽ 404.
Blocked: (không có)

---

### Checkpoint — 2026-08-14 (Phase 3a)

Vừa hoàn thành: **Phase 3a (form tạo/sửa, 4 loại lấy nguồn từ phiếu YC xuất hàng) — XONG,
ĐÃ VERIFY TRÌNH DUYỆT.**

File mới: BE 3 (`ProductExportRequest`, `ProductExportRequestDetail`,
`ProductImportRequestRequest`) + FE 4 (`ProductImportRequestForm.vue`,
`ExportRequestSearchModal.vue`, `create.vue`, `_id/edit.vue`). Sửa: Service, Controller, Routes,
Entity chính, DetailResource.

| Kiểm tra (Nuxt :3099 + API :8199, user Super admin) | Kết quả |
| --- | --- |
| Popup chọn phiếu nguồn | 10 dòng/trang, tổng 33.865 = SQL ✅ |
| Chọn phiếu → kéo hàng hoá | 1 dòng, đủ tên/mã/model/ĐVT/SL đề xuất ✅ |
| Lưu nháp từ trình duyệt | PYCNH-12235, `created_by=13`, `company_id=1`, `department_id=111` ✅ |
| Màn Sửa nạp lại | Loại + nút chọn nguồn bị khoá, mã nguồn hiện đúng, SL đúng ✅ |
| Sửa + Lưu và gửi duyệt | status 3 → 2, `received_time` set, `updated_by=13` ✅ |
| Validate: bấm Lưu khi form trống | 422 → 3 lỗi tiếng Việt hiện inline ✅ |
| Chưa lưu → Quay lại | Hiện popup "Thông tin chưa lưu"; chọn Ở lại thì dữ liệu còn nguyên ✅ |
| Không sửa gì → Quay lại | Thoát thẳng, không hỏi ✅ |
| Lưu thành công → chuyển trang | Không hỏi "chưa lưu" ✅ |
| Console | 0 lỗi (2 lỗi khi test 422 là `console.error` cố ý) ✅ |

**6 lỗi phát hiện khi verify — đã sửa hết:**

1. **Thiếu hook `creating`** → `created_by = 0`, `company_id`/`department_id` NULL. Entity extends
   `Model` trần nên không ai tự điền. Hậu quả: phiếu nháp vừa tạo đã KHÔNG sửa được (`canEdit()`
   so `created_by`) và phạm vi danh sách theo cấp lọc sai.
2. **Cột hệ số đơn vị là `unit_coefficient`**, không phải `coefficient` → 500 khi lưu.
3. **Không ghi được thông báo kiểu ERP**: `notifications` trên DB gộp mang cấu trúc Laravel của
   HRM, phía ERP cũng đã tắt thông báo. → chuyển sang `EmployeeInfoService::sendNotification`
   (đúng kết luận precedent D9), bọc try/catch để lỗi gửi không phá giao dịch lưu phiếu.
4. **Không cảnh báo "chưa lưu"** dù đã chọn nguồn + có hàng: `unsavedChangesMixin` chỉ tính bẩn
   khi snapshot đổi trong ~500ms sau thao tác chuột/phím, mà hàng hoá về sau `await` API (vài
   giây) → bị coi là auto-fill. Khắc phục bằng `markUserEdited()` dời lại mốc thao tác ngay
   trước khi ghi dữ liệu; KHÔNG sửa mixin dùng chung.
5. **Khoảng trắng gần nửa màn hình dưới bảng hàng hoá**: `default.scss` áp global
   `min-height: 50vh` cho MỌI `.table-responsive`. Override cục bộ `.pir-form .table-responsive`.
6. **Checkbox "Nhập thẳng" render ra khối rỗng 0x0**: `V2BaseCheckbox` tính
   `singleMode = options.length === 0 && !$slots.default` → truyền default slot lại rơi vào nhánh
   "nhiều lựa chọn" với 0 option. Phải dùng prop `label` (như `AccountFormComponent`).

Đã xoá 3 phiếu test (12233, 12234, 12235) sau khi kiểm tra.

Đang làm dở: (không có)
Bước tiếp theo: **Phase 4 — Chi tiết + 4 luồng duyệt + từ chối + lịch sử**, hoặc Phase 3b tuỳ ưu tiên.
Blocked: (không có)

---

### Checkpoint — 2026-08-14 (Phase 3b)

Vừa hoàn thành: **Phase 3b — XONG**. Form giờ lập được **7/8 loại**; loại 11 bị loại có chủ đích
(xem ghi chú đầu Phase 3b).

File mới: `BorrowSellRequest.php`, `InlandProductArrivedNew.php`, `ProductArrivedNotify.php`.
Sửa: Service (điều phối nguồn + dòng con KH + chi phí nội địa), FormRequest (`source_id` chung),
Controller (+ `/costs`), Routes, `ProductImportRequestForm.vue`.

| Kiểm tra | Kết quả |
| --- | --- |
| Popup loại 9 | 4.245 = SQL ✅ |
| Popup loại 15 / loại 2 | 0 với user 13 — ĐÚNG, ERP lọc `created_by = mình` (toàn hệ thống: 6 / 33) ✅ |
| Nguồn loại 15 (id 681) | 10 dòng = 4 nhóm + 6 KM, khớp SQL ✅ |
| Nguồn loại 2 (id 1939) | 1 dòng, `products_readonly = true` ✅ |
| Lưu loại 9 (trình duyệt) | `borrow_sell_request_id=4386`, chép `firm_contract_id` + `customer_id` ✅ |
| Lưu loại 15 (script) | 10 dòng hàng · **4 dòng con khách hàng** · 1 dòng chi phí nội địa · NCC lấy từ hợp đồng mua · nguồn đổi status 1→2 ✅ |
| Lưu loại 2 (script) | `notify_id` + NCC + tiền tệ đúng; nguồn đổi status 2→1 ✅ |
| FE dropdown | Đúng 7 loại, KHÔNG có loại 11 ✅ |
| FE nhãn nguồn | Đổi theo loại (loại 9 → "Phiếu yêu cầu xuất bán hàng mượn") ✅ |
| FE tab Chi phí nội địa | Hiện với loại ≠ 3 ✅ |
| Console | 0 lỗi ✅ |

Đã xoá 3 phiếu test (12236-12238) **và khôi phục trạng thái 2 chứng từ nguồn** đã bị đánh dấu
khi test (`inland_product_arrived_news` 681 về 1, `product_arrived_notifies` 1939 về 2).

⚠️ Lưu ý cho người test sau: tạo phiếu loại 2 / 15 sẽ **ĐỔI TRẠNG THÁI chứng từ nguồn** (đúng như
ERP, để 1 phiếu báo hàng về không lập được 2 phiếu nhập). Test xong nhớ khôi phục.

Đang làm dở: (không có)
Bước tiếp theo: **Phase 4 — Chi tiết + 4 luồng duyệt + từ chối + huỷ phiếu nháp + lịch sử**
Blocked: (không có)

---

### Checkpoint bổ sung — 2026-08-14 (chỉnh giao diện form)

User báo giao diện màn Thêm mới "chưa chỉn chu, font chữ chưa chuẩn". Truy ra **2 nguyên nhân
gốc, đều là bẫy dùng chung của FE**:

1. **Bộ class khung form KHÔNG nằm trong `v2-styles.scss`.** `form-header`, `header-icon`,
   `header-title`, `header-sub`, `form-card`, `form-card-head`, `form-card-body`,
   `readonly-cell` chỉ được khai trong `<style>` RIÊNG của `ProductTransferRequestForm.vue`
   (~dòng 1156). Tôi mượn tên class mà không chép CSS → form render "trần": header không khung,
   ô chỉ-đọc (Ngày lập / Người lập) trông y hệt ô nhập được, cỡ chữ lệch.
   → Đã chép nguyên bộ CSS vào `<style>` của form, scoped dưới `.pir-form`, giữ **đúng cùng giá
   trị** với màn Phiếu YC chuyển hàng để 2 màn nhìn như một.
   (`btn-compact` thì không được định nghĩa ở đâu cả — class chết, để nguyên cho đồng nhất.)

2. **`text-muted` bị ép thành ĐỎ.** 4 file scss dùng chung (`custom.scss:241`,
   `custom-theme.scss:190`, `custom-assign.scss:12`, `custom-timesheet.scss:16`) đều có
   `.text-muted { color: #dc3545 !important }` → dòng "Chưa có chi phí nội địa" / "Chọn phiếu…
   để lấy danh sách hàng hoá" hiện **đỏ như báo lỗi** (đo được `rgb(220,53,69)`).
   → Thay bằng `.text-soft` khai trong màn. Popup dùng style **KHÔNG scoped** bọc theo id modal
   vì bootstrap-vue render modal ra ngoài component.

Bổ sung luôn: cỡ chữ bảng trong form (13px), padding ô, viền đỏ `is-invalid` tô xuống control con
(select2 / datepicker), `padding-bottom: 90px` chừa chỗ cho `V2Footer` (fixed).

Đã đo lại trên trình duyệt: `readonly-cell` nền `#f8fafc` cao 30.5px chữ 13px · card head nền
`#f9fafb` chữ 12px · chữ phụ `rgb(107,114,128)` · khối cuối trang kết ở 762px trong khi footer bắt
đầu 826px → **không bị che**. Console 0 lỗi.

### Checkpoint bổ sung 2 — 2026-08-14 (gom bố cục form theo ERP)

User đối chiếu với ERP: "bên ERP khá gọn gàng, sang HRM tách riêng tốn dòng". Đúng — bản đầu của
tôi xếp **4 card dọc** (Thông tin chung / Hàng hoá / Chi phí nội địa / File đính kèm) trong khi
ERP chỉ có **2 khối**. Đã gom lại bám đúng ERP:

| Trước | Sau |
| --- | --- |
| 4 card xếp dọc, phải cuộn | **2 card**, form vừa 1 màn hình |
| "Ngày lập" + "Người lập" chiếm 2 ô form | Dồn vào **góc phải tiêu đề khối** (`DNS Admin · 14/08/2026`) — bỏ 2 ô |
| "File đính kèm" là 1 card riêng chỉ chứa 1 nút | Ô **"+"** gọn nằm trong khối Thông tin chung, file đã chọn hiện dạng chip |
| Hàng hoá và Chi phí nội địa là 2 card | 1 khối **"Chi tiết"** với **2 tab** (`b-tabs nav-class="nav-tabs nav-bordered"` — khuôn `PaymentBusinessRequestForm.vue`) |

Tab "Chi phí nội địa" vẫn ẩn hẳn với loại 3 (ERP `has_inland_cost`).

Verify lại sau khi gom: 2 card · 2 tab · chuyển tab ra đúng 7 cột chi phí · nút "+" đính kèm có ·
chạy lại trọn luồng chọn nguồn → Lưu nháp vẫn tạo được phiếu (PYCNH-12239, đã xoá) · console 0 lỗi.

### Checkpoint bổ sung 3 — 2026-08-14 (UI nguồn + đính kèm + xem trước file)

User góp ý 3 điểm, đã sửa hết:

1. **Nút "Chọn" dính sát ô chứng từ nguồn** — do dùng `input-group` (dán 2 phần tử và cắt bo góc).
   → Đổi sang flex có `gap: 8px` (`.source-picker`), 2 phần tử tách rời, bo góc nguyên vẹn.
2. **File đính kèm chỉ có dấu "+" bé tí** → thay bằng **vùng kéo-thả cao 84px** ("Kéo thả file vào
   đây hoặc chọn từ máy" + gợi ý định dạng), hỗ trợ cả bấm chọn lẫn thả file. Danh sách file bên
   dưới có icon theo loại, tên file, nhãn **MỚI** cho file chưa lưu, nút Xem + nút Bỏ.
3. **Ghi chú lệch độ rộng** — trước để 8-4 nên ô ghi chú dài lê thê còn cột file gần như trống.
   → Chia đôi **6-6**, cân với hàng 4 ô ở trên.

**Thêm tính năng theo yêu cầu: XEM TRƯỚC file.** Tái dùng `components/modal/FilePreviewModal.vue`
+ `utils/file-preview.js` có sẵn của dự án (KHÔNG tự viết): `getFileIconClass` cho icon theo loại,
`canPreviewFile` để mờ nút Xem với định dạng không xem được, `openFilePreviewModal` để mở.
Modal nhận cả `file_path` (URL đã lưu trên S3) LẪN `File` vừa chọn → **xem được trước khi bấm Lưu**.

Verify: vùng thả cao 84px · khoảng cách ô nguồn ↔ nút Chọn = 8px · cột Ghi chú 702px (6/12) ·
chọn 2 file `anh-test.png` + `tai-lieu.pdf` → icon ra đúng `ri-image-line` / `ri-file-pdf-line`,
đều gắn nhãn MỚI · bấm Xem ảnh → modal hiện ảnh qua `blob:` kèm dung lượng + nút Tải xuống ·
console 0 lỗi.

### Checkpoint bổ sung 4 — 2026-08-14 (ô hợp đồng theo nguồn + dấu (*) khớp ERP)

User đối chiếu ERP và chỉ ra 2 thiếu sót, đã soát lại `form.blade.php` (dòng 36-360) và sửa:

**a) Thiếu các ô CHỈ ĐỌC lấy theo chứng từ nguồn** — đúng như user nói. Bổ sung theo đúng ERP:

| Loại | Ô chỉ đọc | Điều kiện hiện |
| --- | --- | --- |
| 15 | **Hợp đồng mua** *(có dấu \*)* | luôn hiện |
| 2 | **Hợp đồng** + **Nhà cung cấp** | luôn hiện |
| 4, 9 | **Hợp đồng** + **Ngày xuất** | CHỈ khi hợp đồng đã quyết toán (`is_settlement`) |

BE bổ sung `contract_code` / `supplier_name` / `date_accounting` / `is_settlement` vào payload
nguồn. Đã test: loại 15 → `DHNT-000496`; loại 2 → `HDMN-00011-…` + `CÔNG TY TNHH CAO SU NHỰA VIỆT NAM`.

**b) Dấu (\*) trên ô chứng từ nguồn không khớp ERP.** Bảng `required-label` thật của ERP:

| Loại | ERP có (\*) ? |
| --- | --- |
| 2, 9, 15 | **CÓ** |
| 3, 4, 14, 99 | KHÔNG |

Trước đó tôi để (\*) cho mọi loại trừ 99 → sai. Đã sửa đúng bảng trên (`SOURCE_REQUIRED_MARK_TYPES`).

⚠️ **Ghi nhận mâu thuẫn của ERP** (giữ nguyên, không tự sửa): với loại 3 / 4 / 14, BE của ERP
**VẪN bắt buộc** `product_export_request_id` (và `customer_id` với loại 14) nhưng FE không đánh
dấu (\*). Tức người dùng bỏ trống sẽ bị 422 ở một ô không có dấu sao. Bản port giữ giống ERP để
2 cổng nhìn như nhau, câu lỗi vẫn hiện inline ngay dưới ô. **Cần user chốt** có muốn thêm (\*)
cho đúng thực tế không.

**c) Loại 11 (mua nước ngoài mới)** — user hỏi lại. Đã kiểm chứng thêm: `grep "type == 11"` trong
`form.blade.php` ra **0 kết quả** — ERP có loại này trong dropdown nhưng KHÔNG có khối trường nào,
không chọn được chứng từ nguồn, `store()` cũng không có nhánh xử lý. Chọn vào là form trống.
634/634 phiếu loại 11 do `OrderImportRequest` sinh tự động. → Giữ nguyên quyết định KHÔNG đưa vào
dropdown HRM.

Verify 7 loại trên trình duyệt: dấu (\*) và ô chỉ-đọc ra đúng bảng trên · console 0 lỗi.

### Chốt sau Checkpoint bổ sung 4 (14/08/2026)

User chốt: **HRM đánh dấu (*) cho đủ**, không bám theo chỗ ERP quên.
- `isExportRequestRequired` đổi thành `!SOURCE_OPTIONAL_TYPES.includes(type)` → có (*) với 2/3/4/9/14/15, không có với 99.
- Ô "Khách hàng" loại 14 vốn đã `required` sẵn, không phải sửa.
- Đây là điểm **lệch có chủ ý** so với ERP, đã ghi chú ngay trên computed.

## Phase 7 — Áp chuẩn UI mới (14/08/2026)

Nhánh `gop_db` của cả 2 repo vừa cập nhật + 4 skill mới (`button-convention`, `list-page`,
`modal-popup`, `info-icon-tooltip`). Đã rà 3 màn của feature theo bộ chuẩn mới.

### Đã sửa (không cần merge)

- [x] **Popup xác nhận xoá file**: bỏ `$bvModal.msgBoxConfirm()` → dùng đúng component chung
      `base-confirm-modal` (id `confirm-delete-pir-file`). CLAUDE.md + `modal-popup` mục 3a.
- [x] **Thứ tự request khi vào màn danh sách** (`list-page` mục 8): `loadData()` bắn NGAY, không
      `await` cấu hình cột / kho hàng nữa; `loading` khởi tạo `true` để bảng hiện spinner từ đầu.
- [x] **Thứ tự + căn lề + bộ cột mặc định** (`list-page` mục 4, 6, 15): cột Trạng thái chuyển
      `align: center` + `width 130px` và dời về **ngay trước** cột Hành động; Người lập / Ngày lập
      đứng cuối nhóm dữ liệu; 3 cột duyệt (Người duyệt, Ngày nhận, Ngày duyệt) để `isVisible: false`
      → mặc định hiện **9 cột** (7 chuẩn + Loại + Khách hàng, theo ngoại lệ của mục 6).
- [x] **Tiêu đề màn chi tiết** (`list-page` mục 7.1): `Chi tiết phiếu yêu cầu nhập hàng: <mã>`
      (dấu `:`, không phải `·`).
- [x] **Chuẩn nút** (`button-convention`): `Thêm mới` → **`Tạo mới`**; nút Xuất Excel thêm
      `status="success"` (xanh lá); icon xoá `ri-delete-bin-6-line` → **`ri-delete-bin-line`**;
      chữ `Xoá` → **`Xóa`** (quy tắc bỏ dấu kiểu mới).

### Đã merge `gop_db` + áp nốt (user duyệt 14/08/2026)

Merge `gop_db` vào `feat/finance-product-import-request` ở **cả 2 repo** — fast-forward, **0 conflict**
(code của feature còn ở dạng untracked nên không đụng gì). API +31 commit, client +19 commit.

- [x] **Cột "Hành động" ở CUỐI bảng** dùng `V2BaseRowActions`: 2 nút **Sửa** (khai `to` để chuột
      phải mở tab mới; `interactable` theo cờ `is_can_edit`, fail-closed) + **In**. Bỏ hẳn hàng nút
      cũ nằm dưới cột Mã. Màn này KHÔNG có Xóa/Khóa (ERP cũng không) nên slot 2 dành cho "In".
- [x] **Link mã phiếu** đổi sang class chuẩn `.v2-cell-link` — đã đo màu ra navy `#28539d`.
- [x] **Dòng đếm** bỏ đuôi "phiếu": nay hiện `Hiển thị 1–10 / 12111` (`V2BaseDataTable` bản mới).
- [x] **Sắp xếp theo độ khớp** (`list-page` mục 3b) — port `applyRelevanceOrder` rút gọn:
      chỉ chấm điểm trên **mã phiếu** (tên người lập nằm ở bảng khác → skill quy định không chấm),
      ranh giới từ là dấu `-` của `PYCNH-xxxxx`; bỏ qua khi user đã tự sort hoặc từ khoá < 2 ký tự;
      chốt `created_at DESC` + `id DESC` để lật trang không lặp/mất bản ghi.
      Đã test: gõ `1223` → `PYCNH-12230` (khớp ngay sau dấu `-`) đứng trên `PYCNH-11223` / `PYCNH-01223`.

⚠️ **`plugins/confirm-dialog.js` (`$confirm()`) CHƯA tồn tại trên `gop_db`** — skill `modal-popup`
mục 3a viết trước khi code có. Không ảnh hưởng: đã dùng **cách 1** (đặt `BaseConfirmModal` trong
template), là cách skill ghi "phổ biến".

⚠️ **Sau merge, `gop_db` có migration chưa chạy trên DB local** (`filter_customizations`,
`hrm_contracts`, `add_customers_to_column_customizations`…). KHÔNG tự chạy `migrate` — việc của
người phụ trách nhánh gộp. Màn này không dùng `V2BaseSmartFilterPanel` nên không bị ảnh hưởng.

### Chưa áp — cần PR riêng cho component dùng chung

- **Text nút "Không duyệt" → "Từ chối"** theo bảng text chuẩn của `button-convention`: chữ này nằm
  trong `V2Footer` (component DÙNG CHUNG toàn dự án) nên KHÔNG tự sửa ở feature này.

### Merge `gop_db` đợt 2 — 14/08/2026 (màn "Phiếu đề nghị thu tiền" vào chung phân hệ)

`gop_db` thêm 1 commit ở API + 2 ở client. Lần này **CÓ CONFLICT** vì màn mới đụng đúng 2 file
dùng chung mà feature này cũng sửa.

**1. `Modules/Finance/Routes/api.php`** — cả 2 nhóm route cùng thêm vào cuối group `/v1/finance`.
Giải quyết: **giữ CẢ HAI** (`bill-income-requests` rồi `product-import-requests`), không bên nào mất.

**2. `PermissionsTableSeeder.php` — conflict NGHIỆP VỤ, không phải conflict văn bản.**
Cả 2 màn cùng chiếm dải id **1148-1152**. Màn Đề nghị thu tiền vào `gop_db` trước → giữ nguyên
1148-1152; **quyền của màn này đánh số lại 1148-1154 → 1153-1159**.
Đã kiểm tra: code của màn KHÔNG hard-code id quyền ở đâu (resolve theo TÊN qua
`currentEmployeeHasPermission`) nên đổi số không ảnh hưởng logic.
⚠️ Bài học lặp lại của `project_export_bill_permission_id_branch_drift`: 2 nhánh song song cùng
lấy id tiếp theo trong seeder thì kiểu gì cũng đụng — ai merge sau phải đánh số lại.

**3. Dùng lại trait dùng chung `Entities/Concerns/ChecksEmployeePermission`.**
Màn Đề nghị thu tiền đã tách 2 method kiểm tra quyền (`currentEmployeeHasPermission`,
`currentEmployeeIsSuperAdmin`) thành trait — trùng khít bản mà màn này tự viết. Đã **bỏ bản riêng**
(75 dòng: 2 method + 2 property cache + const `SUPER_ADMIN_ROLE_ID`) và `use` trait, đúng quy tắc
mới của CLAUDE.md "có sẵn thì dùng lại, không tự phát minh kiểu mới". Hành vi giữ nguyên — đã test
lại `canView()`, `approvalFlags()`, `employeeIdsHavingPermission()`, phạm vi danh sách của TP 105.

**4. `plugins/confirm-dialog.js` NAY ĐÃ CÓ** (client, đã đăng ký trong `nuxt.config.js`) → `$confirm()`
dùng được. Popup xoá file của màn này **giữ nguyên cách 1** (đặt `BaseConfirmModal` trong template)
vì nó gọi từ method của chính component có template — cách 2 dành cho code ngoài template.

**Verify sau merge**: 8 route API + màn `bill-income-requests` của người khác đều 200; màn danh
sách 9 cột + cột Hành động + link `.v2-cell-link`; màn chi tiết tiêu đề `: PYCNH-12200` với đủ 4
nút. Console 0 lỗi.
