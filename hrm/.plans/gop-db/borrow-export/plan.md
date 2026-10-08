# Plan — Phiếu xuất hàng mượn (`borrow_exports` → HRM)

> @khoipv · nhánh `gop_db` (cả 2 repo) · bắt đầu 2026-09-07
> Design: `.plans/gop-db/borrow-export/design.md`
> Spec: `docs/superpowers/specs/gop-db/2026-09-07-borrow-export-design.md`

**Không có migration, không có permission mới.**

---

## Phase 0 — Chuẩn bị

- [x] Khảo sát màn ERP (controller 304 dòng, model 222 dòng, 5 blade, 3 lớp JS)
- [x] Xác nhận 3 bảng có sẵn trên DB gộp: 280 / 655 / 941 dòng
- [x] Xác nhận quyền `Kế toán kho` guard `api` đã có (id 1136) → không sửa seeder
- [x] Đo hành vi `0/0` trên PHP 7.4.3 + MySQL (`NAN` → lưu `0.00`, không crash)
- [x] Xác nhận `ReportTemplate::XUAT_HANG_MUON` **không tồn tại** → route In của ERP là code chết
- [x] Viết design.md + spec chi tiết

---

## Phase 1 — Backend: Entity + đọc dữ liệu

- [x] `Entities/BorrowExport/BorrowExport.php` — `$table`, `STATUSES` (màu theo SRS),
      `SORTABLE_COLUMNS`, quan hệ `parent` / `products` / `employee_create`, `canView()`
- [x] `Entities/BorrowExport/BorrowExportProduct.php` + `BorrowExportProductDetail.php`
- [x] `Services/BorrowExportService.php` — `searchByFilter()` (8 bộ lọc, **bọc ngoặc** nhóm
      `product`), `meta()`, `findForShow()`, `detailData()`
- [x] `Transformers/BorrowExportResource/BorrowExportListResource.php`
- [x] `Http/Controllers/V1/BorrowExportController.php` — `index` / `show`
- [x] `Routes/api.php` — group `finance/borrow-exports`, route tĩnh khai TRƯỚC `/{id}`
- [x] ⚠️ **ĐỔI so với kế hoạch ban đầu**: KHÔNG gate bằng middleware `checkPermission:Kế toán kho`.
      Đo trên DB gộp 07/09: quyền guard `api` id 1136 gán cho **0 role / 0 người** (bản dùng thật là
      ERP guard `web` id 100080, 19 role); middleware gọi spatie `getAllPermissions()` chỉ trả quyền
      cùng guard ⇒ gắn vào là khoá sạch mọi người, super admin cũng 403 (test thật emp 13 role 18).
      → gate bằng `BorrowExport::isAccountant()` (trait 2 guard) ở đầu **cả 7 action** của Controller
- [x] Smoke test: `index` 200, 3 khoá sort đổi đúng thứ tự, key sort lạ + chuỗi tiêm SQL rơi về mặc
      định, 8 ô lọc đều đổi kết quả, `show` 404 khi id không tồn tại

---

## Phase 2 — Backend: màn Tạo (thao tác duyệt)

- [x] `requestOptions()` — popup chọn phiếu yêu cầu (`status = 2`, tầm Kế toán kho)
- [x] `requestData($id)` — bảng hàng + cột **Đang mượn**, gọi
      `BorrowStockService::borrowedQty(..., exceptExportRequestId: $id)`
- [x] `Http/Requests/BorrowExport/BorrowExportStoreRequest.php` — port rule ERP,
      **rethrow `ValidationException`** (không catch chung `Exception`)
- [x] `store()` trong transaction: sinh mã `PXHM-NNNNN` → ghi 2 bảng con (**giữ dòng `qty = 0`**,
      `export_price = $qty > 0 ? … : 0`) → kiểm lại số lượng tầng BE → `updateWarehouse()` →
      duyệt phiếu cha → thông báo
- [x] Cập nhật docblock "Nơi đang dùng" của `BorrowStockService` (thêm 1 dòng, không sửa logic)
- [x] Smoke test `store`: tạo thật → kiểm 5 tác dụng phụ → rollback

---

## Phase 2b — Phát sinh ngoài kế hoạch (đều là điều kiện cần để màn chạy)

- [x] Thêm `onApproved()` vào `BorrowExportRequestNotifyService` — docblock của chính service đó đã
      ghi sẵn "khi port tiếp thì thêm vào đây, đừng viết thông báo rời ở màn kia"
- [x] Thêm hằng `ProductExportRequest::DA_TRA = 3` + ghi rõ ngoại lệ ghi dữ liệu vào docblock
      (model đó khai là CHỈ ĐỌC; việc ghi làm bằng **query builder** trong `updateWarehouse()`,
      không thêm hàm ghi vào model)
- [x] Đăng ký bảng `borrow_exports` vào `CatalogHistoryService::TABLES` — `log()` mở đầu bằng
      `if (!isset(self::TABLES[$table])) return false;` nên **thiếu đăng ký thì log âm thầm không
      ghi**, không lỗi gì (đã dính lúc test: `store()` trả 200 nhưng 0 dòng log)
- [x] Thêm nhãn + màu cho action `approved` vào `CatalogHistoryService` — thiếu thì timeline in ra
      nguyên chuỗi kỹ thuật "approved" và tô xám mặc định
- [x] Gate **đơn giá vốn** (`export_price`) bằng quyền `Xem giá vốn hàng hoá` (1092) ở BE, trả
      `null` khi không quyền + cờ `can_view_cost_price`; FE ẩn cột; bản in bỏ cột;
      **lịch sử KHÔNG log giá vốn** (log là bản chụp vĩnh viễn, không gate lại được lúc đọc)
- [x] Thêm ô tìm nhanh `keyword` (mã phiếu / mã phiếu YC / tên người lập) cho đồng bộ màn Yêu cầu

---

## Phase 3 — Backend: In · Excel · Lịch sử

- [x] `Resources/views/prints/borrow-export.blade.php` (letterhead lấy `company_id` từ **phiếu
      yêu cầu cha** — bảng này không có cột đó)
- [x] `Resources/views/prints/borrow-export-list.blade.php` + `printListData()` (dùng
      `LimitsPrintListRows`)
- [x] `export()` — trả đủ mọi trường có trong `ExportFieldsModal`, kèm `FILTER_TEXT`
- [x] `Services/BorrowExportHistoryService.php` — `catalog_histories`, 2 khoá ảo dạng bảng,
      lọc khoá rỗng trước khi ghi
- [x] Thêm `onApproved()` vào `BorrowExportRequestHistoryService` (**hàm mới**, không sửa hàm cũ)
- [x] Test lại màn *Yêu cầu* sau khi thêm `onApproved()` — không vỡ log cũ

---

## Phase 4 — Frontend

- [x] `pages/finance/borrow-exports/index.vue` — 4 mixin, `V2BaseSmartFilterPanel`,
      `V2BaseRowActions` (`switch (action)` — KHÔNG `action.key`), 9 cột hiện hết mặc định
- [x] `components/BorrowExportRequestPickerModal.vue` — dùng lại khuôn picker có sẵn
- [x] `components/BorrowExportForm.vue` — bảng lồng `rowspan`, validate `qty <= borrowed_qty`
      inline, `can_submit`
- [x] `create.vue` — nhận `?borrow_export_request_id=`, `unsavedChangesMixin` + `markFormSaved()`
- [x] `_id/index.vue` — chỉ đọc + cột Đơn giá vốn, khối Lịch sử, nút In trong `V2Footer`
- [x] `components/export-excel.js` + `ExportFieldsModal`
- [x] `components/subsystem-menu/finance.js:182` — thêm `link` vào slot đã khai sẵn
- [x] `pages/finance/borrow-export-requests/_id/index.vue` — `createBorrowExport()` đổi từ toast
      sang điều hướng `/finance/borrow-exports/create?borrow_export_request_id=<id>`

---

## Phase 5 — Tự kiểm

- [x] Chạy 11 lệnh grep tự kiểm của skill `erp-to-hrm-screen` trên cả thư mục feature
- [x] Đối chiếu ngược ERP: đủ 9 cột · đủ 8 ô lọc · đủ hành động + điều kiện ẩn/hiện
- [x] Compile SFC toàn bộ file FE mới
- [x] Smoke test API qua HTTP kernel trong tinker (`route:list` của repo này luôn nổ)
- [x] Báo user mở trình duyệt nghiệm thu — **không tự test bằng Playwright**

---

## Checkpoint

### Checkpoint — 2026-09-07 (khởi tạo)
Vừa hoàn thành: Phase 0 — khảo sát ERP, đo hành vi PHP/MySQL, chốt 7 quyết định lớn với user,
viết design.md + spec đầy đủ.
Đang làm dở: chưa động code.
Bước tiếp theo: Phase 1 — dựng 3 Entity + Service đọc + Controller index/show + route.
Blocked:

### Checkpoint — 2026-09-07 (code xong)
Vừa hoàn thành: **Phase 1 → 5 xong hết.** BE 9 file mới + 6 file sửa; FE 6 file mới + 2 file sửa.
Không migration, không permission mới.

Kiểm chứng đã chạy (không dùng Playwright — user chốt tự mở trình duyệt):
- `php -l` sạch 13 file PHP; compile SFC sạch 8 file FE (vue-template-compiler + @babel/parser).
- 11 lệnh grep tự kiểm của skill `erp-to-hrm-screen`: chỉ khớp trong CHÚ THÍCH, không vi phạm nào.
- Smoke test API qua HTTP kernel (`route:list` repo này luôn nổ): `index` 200 · 2 khoá sort đổi
  đúng thứ tự · key sort lạ + chuỗi tiêm SQL rơi về mặc định · 8 ô lọc + `keyword` đều đổi kết quả
  · `export` 280 dòng · `print-data` 8.980 byte · `print-list-data` 59.614 byte · `show` id lạ 404.
- Test `store` (tạo thật rồi ROLLBACK, dữ liệu giữ nguyên 280/655/941): sinh đúng `PXHM-NNNNN` ·
  giữ dòng `qty = 0` với `export_price = 0.00` · `approved_qty` ghi ngược · `borrow_returned_qty`
  **và** `returned_by_other` cùng +1 · phiếu YC 2 → 1 kèm approver + approved_time · log `create`
  ở phiếu xuất và log `approved` ("Duyệt", nhóm status, ghi chú kèm mã phiếu xuất) ở phiếu YC.
- 10 nhánh lỗi: SL vượt tồn 422 "Số lượng không hợp lệ" · tất cả SL = 0 → "Không có thay đổi" ·
  SL âm / > 6 chữ số / thiếu products / phiếu YC không tồn tại / ghi chú > 255 → 422 đúng câu ·
  duyệt lại phiếu đã duyệt 422 · `request-data` phiếu đã duyệt 422 · `show` id lạ 404.
- Popup không tin tham số FE: gửi `status=1&type=all` vẫn ra đúng 5 phiếu Chờ duyệt (không phải 285).

Đang làm dở: không.
Bước tiếp theo: **user mở trình duyệt nghiệm thu** — 4 màn (danh sách / tạo / chi tiết / in), luồng
nút "Duyệt" ở màn Yêu cầu, popup Lịch sử ở 2 nơi, Xuất Excel. Chưa commit.
Blocked:

## Fix — 2026-10-05: ô chọn phiếu yêu cầu theo khuôn "Số phiếu đề nghị" (@khoipv)
- [x] FE `BorrowExportForm.vue`: bỏ ô readonly + nút kính lúp, đổi sang `V2BaseInput` readonly bấm thẳng
      mở popup (placeholder "Nhấn vào đây để chọn…", con trỏ tay; giữ viền đỏ `is-invalid` + dòng lỗi `.fld-err` sẵn có của form) —
      khuôn `bill-payments/components/BillPaymentForm.vue:37-51` + style `.picker-input`
- [x] FE `BorrowExportForm.vue`: ô "Phiếu xuất mượn" tụt thấp hơn ô bên cạnh (do `mt-3` + khung tự chế
      cao 38px) → mọi ô section Thông tin chung dùng chung `col-md-6 mb-2` (khuôn màn Chi tiết),
      `.req-box` khớp khung `V2BaseInput sm` bị khoá (cao 34px, viền #e2e8f0, nền #f1f5f9)
- [x] FE `BorrowExportForm.vue`: tên người tạo trên header "Thông tin chung" trống — computed `creatorName`
      đọc `state.user` (không tồn tại) → đổi sang `state.current_employee_info.fullname`
- [x] FE: thêm nút "Lưu và tiếp tục" (secondary, `ri-save-3-line`) ở màn Lập — `saveAndContinueMixin` trong
      `BorrowExportForm.vue` (`afterSaveRedirect`) + `saveAndContinuePageMixin` ở `create.vue` (`:key="formKey"`).
      `create.vue` ghi đè `onSavedAndContinue`: bỏ `?borrow_export_request_id=` trước khi remount (không thì
      form mới nạp lại phiếu YC vừa duyệt → 422)
- [x] FE `index.vue`: cột "Phiếu yêu cầu" ở danh sách mở màn Yêu cầu sang TAB MỚI (`target="_blank"` trên nuxt-link)
- [x] BE `BorrowExport.php` + FE `index.vue`: ô tìm nhanh CHỈ tìm theo mã phiếu / mã phiếu yêu cầu (bỏ tên người lập), sửa placeholder
- [x] FE `index.vue`: bộ lọc nâng cao đổi nhãn "Người lập"→"Người tạo", "Ngày lập"→"Ngày tạo" (cột bảng giữ nguyên)
- [x] FE `BorrowExportForm.vue`: lỗi "chưa nhập SL xuất" báo inline tại từng ô Xuất ("Bắt buộc phải nhập" + viền đỏ)
      thay dòng chữ chung dưới bảng; giữ luật ERP `has_change` (chỉ cần ≥ 1 ô > 0, ô = 0 vẫn hợp lệ)
- [x] FE `BorrowExportForm.vue`: chuẩn hoá validate theo skill form-validate 3d — `validateForm()` (thiếu → toast error
      "Bạn chưa nhập đầy đủ thông tin.", vượt SL → toast `"<hàng>": Không được vượt quá N`) + `scrollToFirstError`;
      lỗi inline đổi `.fld-err` tự chế → `V2BaseError`; bỏ 3 toast warning cũ + computed `hasInvalidQty`
- [x] FE `BorrowExportForm.vue`: ô "Người lập phiếu YC" + "Phòng ban người lập phiếu YC" đổi `readonly` → `:disabled="true"` (nền khoá như màn Chi tiết)
- [x] FE `BorrowExportForm.vue`: toast validate KHÔNG in câu lỗi chi tiết (đã có inline) — vượt SL → "Vui lòng kiểm tra lại thông tin đã nhập"
- [x] FE `BorrowExportForm.vue`: bấm "Lưu" xong về màn danh sách `/finance/borrow-exports` (trước sang màn Chi tiết)
- [x] FE `BorrowExportForm.vue`: nút "Lưu" đổi thành "Lưu và duyệt" (icon `ri-check-line`) — ERP để nút "Duyệt"
- [x] FE `BorrowExportForm.vue`: cột "Phiếu mượn" trong bảng Chi tiết thành link sang phiếu Yêu cầu xuất hàng (tab mới) — đúng ERP
- [x] FE Chi tiết + Form: cột Tên hàng hóa — nhãn "Model/Mã/Thương hiệu" in đậm, giá trị KHÔNG đậm (đảo lại)
- [x] FE `BorrowExportForm.vue`: popup "Thông tin chưa lưu" không bao giờ hiện — 2 lỗi: (1) thiếu override
      `unsavedSnapshotSource()` (mixin theo dõi `formSubmit`, form tên `form`); (2) `loadRequest` gọi `markFormSaved()`
      → tắt cảnh báo vĩnh viễn. Sửa: override trả `this.form`; nạp từ query → `markFormPristine()`; chọn phiếu ở popup
      → đánh dấu bẩn ngay (`unsavedUserChanged = true`, bảng hàng về sau API > 500ms nên mixin không tự nhận)
- [x] FE `BorrowExportForm.vue`: bỏ `min-vh-100` ở khung gốc — form ngắn thì dư khoảng trống dưới bảng Chi tiết (100vh + header + đệm footer); sửa luôn màn Chi tiết `_id/index.vue`
- [x] FE `BorrowExportForm.vue`: ô Xuất điền sẵn `request_qty` (SL đề nghị trên phiếu YC) thay vì 0 — đúng ERP (class JS nhận `qty` của dòng chi tiết)

## Phase 6 — Khoảng trống dưới bảng Chi tiết (2026-10-06)

User báo màn Chi tiết `/finance/borrow-exports/322` có khoảng trống lớn dưới dòng Tổng cộng. Nguyên nhân: `body-class="table-auto-height"` không có rule trong màn này (rule chỉ nằm ở `CustomerForm.vue`, có khi component kia đã nạp) → `min-height: 50vh` global của `.table-responsive` còn hiệu lực.

- [x] FE `_id/index.vue` + `components/BorrowExportForm.vue`: thêm `::v-deep .table-responsive.table-auto-height { min-height: 0 !important; }` (khuôn `borrow-export-requests/_id/index.vue`)
- [ ] User mở trình duyệt kiểm tra (Ctrl+Shift+R)

## Phase 7 — Đồng bộ lề màn Lập / Chi tiết (2026-10-07)

User báo màn Lập phiếu xuất hàng mượn dư lề trên + lề trái so với các màn phiếu khác. Nguyên nhân: khung gốc `v2-styles pt-2` + `container-fluid` (cộng thêm đệm 15px vào đệm sẵn của layout) — các màn phiếu Finance khác (BillPaymentForm, BorrowSellForm, ProductExportRequestForm…) dùng `v2-styles` + `container-fluid px-0`.

- [x] FE `components/BorrowExportForm.vue` + `_id/index.vue`: bỏ `pt-2`, `container-fluid` → `container-fluid px-0`
- [ ] User mở trình duyệt kiểm tra (Ctrl+Shift+R)

## Phase 8 — Ô Xuất phải > 0 (2026-10-07)

User chốt: mọi ô Xuất trong bảng Chi tiết phải lớn hơn 0 (bỏ luật ERP `has_change` "ô = 0 vẫn hợp lệ, chỉ cần ≥ 1 ô > 0").

- [x] FE `components/BorrowExportForm.vue`: `detailError` báo "Phải lớn hơn 0" tại từng ô Xuất ≤ 0 (sau lần bấm Lưu đầu)
- [x] BE `BorrowExportStoreRequest`: `products.*.details.*.qty` `min:0` → `gt:0`, message "Phải lớn hơn 0"
- [ ] User mở trình duyệt kiểm tra

## Phase 9 — Phân trang popup "Chọn phiếu yêu cầu xuất hàng mượn" (2026-10-07)

User yêu cầu phần phân trang popup chọn phiếu YC sửa giống popup "Chọn phiếu xác nhận bảo hành" màn
`finance/addition-accounting-requests/create` (`addition-accounting-requests/components/RecordSearchModal.vue`).

- [x] FE `components/BorrowExportRequestPickerModal.vue`: bỏ bảng tự dựng + `V2BasePagination` → `V2BaseDataTable`
      (`hide-header`, dòng "Hiển thị x–y / n", số dòng/trang 20/50/100, mặc định 20), bấm dòng là chọn (`onTableClick`),
      chặn `page-change` dội lại khi đang tải (`loadingPage`). BE giữ nguyên (trần per_page 100, không sort)
- [ ] User mở trình duyệt kiểm tra (Ctrl+Shift+R)

## Phase 10 — Đổi nhãn cột màn danh sách (2026-10-07)

User chốt: màn danh sách đổi "Người lập" → "Người tạo", "Ngày lập" → "Ngày tạo" (bỏ quyết định giữ nhãn ERP trước đó).

- [x] FE `index.vue`: tiêu đề 2 cột `creator_name` / `createdAt`
- [x] FE `components/export-excel.js`: header 2 cột tương ứng của file Excel danh sách (khối chữ ký "Người lập" cuối file giữ nguyên)
- [ ] User mở trình duyệt kiểm tra (Ctrl+Shift+R)

## Phase 11 — Ô lọc Trạng thái chỉ còn "Đã duyệt" (2026-10-07)

User hỏi phiếu có trạng thái Đang tạo / Chờ duyệt / Không duyệt không (thấy ở bộ lọc). Kiểm: `store()` luôn ghi `status = 1` (Đã duyệt), không luồng đổi trạng thái; DB 282/282 phiếu `status = 1`. User chọn: giữ ô lọc, chỉ còn "Đã duyệt".

- [x] BE `BorrowExportService::meta()`: `statuses` chỉ trả mục `DA_DUYET`; hằng `BorrowExport::STATUSES` giữ đủ 4 mục (badge `statusMeta()` dùng)
- [ ] User mở trình duyệt kiểm tra
