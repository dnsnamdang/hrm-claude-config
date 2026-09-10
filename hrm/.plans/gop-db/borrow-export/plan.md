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
