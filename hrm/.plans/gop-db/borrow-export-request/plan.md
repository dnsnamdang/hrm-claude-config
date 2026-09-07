# Plan — Yêu cầu xuất hàng mượn (ERP → HRM)

> Phụ trách: @khoipv · Nhánh: `gop_db` · Tạo: 2026-09-04
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-09-04-borrow-export-request-design.md`

## Phase 0 — Khảo sát nguồn ERP

- [x] Đọc controller / model / 6 blade / 3 class JS của `borrow_export_requests`
- [x] Đếm dữ liệu thật trên DB gộp (292 phiếu / 686 dòng hàng / 990 dòng chi tiết / 607 pivot)
- [x] Tra vị trí menu ERP (3 chỗ) + chỗ khai sẵn trong menu HRM
- [x] Xác định khuôn HRM để bám: `prepick-extend-requests` (BE + FE) — cùng họ phiếu yêu cầu
- [x] Chốt 4 quyết định với user
- [x] Viết spec chi tiết

## Phase 1 — BE: nền tảng

- [x] Quyền: thêm 3 permission guard `api` id 1565-1567 vào `PermissionsTableSeeder`
- [x] Entity `BorrowExportRequest` — STATUSES, quan hệ, `searchByFilter` (3 preset),
      `canView/canApprove/canEdit`, `statusMeta`, `attachmentList`, `generateCode`
- [x] Entity `BorrowExportRequestProduct` + `BorrowExportRequestProductDetail`
- [x] `BorrowStockService` — hàm DÙNG CHUNG `returningQty()` / `borrowedQty()`
- [x] Đưa `manageableDepartmentIds()` + `sameCompanyAsCurrent()` lên trait
      `ChecksEmployeePermission` (trước đó bị chép ở 3 entity) — **thêm mới, không sửa bản cũ**

## Phase 2 — BE: đọc

- [x] `BorrowExportRequestService::searchByFilter / meta / findForShow / detailData`
- [x] `BorrowExportRequestListResource`
- [x] Controller `index`, `show`
- [x] Popup nguồn: `exportRequestOptions()` + `exportRequestData()`
- [x] Routes (route tĩnh đặt trước `/{id}` — đã test không bị nuốt)

## Phase 3 — BE: ghi

- [x] `BorrowExportRequestStoreRequest` + `BorrowExportRequestRejectRequest`
- [x] `store()` — transaction, tính lại tồn mượn, sinh mã `PYCXHM-`, sync pivot, thông báo
- [x] `reject()` — `lockForUpdate` + kiểm quyền trong transaction, bắt buộc lý do
- [x] `uploadFiles()` — S3, chỉ PDF, ≤ 13 MB
- [x] `BorrowExportRequestNotifyService` — `[YCXHM]`, 2 sự kiện (tạo → Kế toán kho, từ chối → người lập)

## Phase 4 — BE: in + xuất

- [x] Blade `borrow-export-request.blade.php` (A4 dọc, bảng lồng `rowspan` + `page-break-inside: avoid`)
- [x] Blade `borrow-export-request-list.blade.php` (A4 ngang)
- [x] `printData()` / `printListData()` — letterhead theo `company_id` TRÊN PHIẾU
- [x] Chặn trần 2.000 dòng bản in danh sách (trait `LimitsPrintListRows`)
- [x] `exportData()` — dữ liệu thô cho FE

## Phase 5 — FE: danh sách

- [x] `index.vue` — 5 mixin, SmartFilterPanel (9 ô lọc), DataTable 13 cột, ExportFieldsModal,
      popup xem trước bản in, watcher `$route.query.type`
- [x] `components/RejectModal.vue`
- [x] `components/export-excel.js`

## Phase 6 — FE: tạo mới + chi tiết

- [x] `components/ExportRequestPickerModal.vue` (chọn phiếu xuất mượn)
- [x] `components/BorrowExportRequestForm.vue` (bảng lồng rowspan + validate inline + upload PDF)
- [x] `create.vue` (+ `unsavedChildFormMixin`)
- [x] `_id/index.vue` (chi tiết + Từ chối + In)
- [ ] ~~`_id/edit.vue`~~ — KHÔNG làm: ERP đã comment tắt cả route lẫn nút Sửa/Xóa

## Phase 7 — Menu + rà soát

- [x] 2 mục menu: `sale-hub.js` (`?type=all`) · `finance.js` nhóm Mượn hàng (`?type=accounting`)
- [x] **Gỡ** mục `Chờ duyệt → Phê duyệt - Hàng mượn` (user chốt 2026-09-04: HRM bỏ hẳn màn chờ
      duyệt; người duyệt lọc bằng ô Trạng thái). Preset `for-approve` giữ chạy cho link cũ.
- [x] Chạy checklist skill `erp-to-hrm-screen` + 9 lệnh grep tự kiểm → sửa 1 lỗi thật
      (`text-muted` ở dòng "Không có hàng hóa" — class đó bị scss chung ép thành chữ ĐỎ)
- [x] Đối chiếu ngược từng cột / ô lọc / nút với ERP
- [x] Kiểm chứng bằng dữ liệu thật (xem mục dưới)
- [x] **Test Playwright toàn luồng** (user yêu cầu 2026-09-04) — xem mục dưới

## Kiểm chứng đã chạy (dữ liệu thật trên `gop_db`)

| Nội dung | Kết quả |
| --- | --- |
| 11 endpoint qua HTTP kernel | 10× 200; 1× 422 **đúng nghiệp vụ** (tài khoản không phải người lập phiếu mượn) |
| Route tĩnh (`export`, `print-list-data`, `export-request-options`) | không bị `/{id}` nuốt |
| Phạm vi danh sách ↔ `canView()` | thử **60 nhân viên**, khớp 100% (không ai thấy phiếu ở danh sách mà bấm vào bị chặn) |
| Đếm phạm vi vs SQL | 3/3 khớp (Super admin 292 · NV thường 0 · NV thường 36) |
| Vòng đời ghi (transaction rồi rollback) | 7/7 đúng: tạo phiếu · người lập không tự từ chối được · Kế toán kho từ chối được · từ chối lần 2 bị chặn · SL vượt trần bị chặn · tất cả qty=0 bị chặn · chọn phiếu mượn của người khác bị chặn |
| Sau rollback | 292 phiếu / 686 dòng hàng — không để lại rác |
| Công thức "Đang mượn" | 3 nguồn treo đọc đúng dữ liệu thật; ví dụ phiếu PYCXH-35177 có 1 YCXHM chờ duyệt → đang mượn = 0 (đúng) |
| Bản in 1 phiếu | letterhead lấy theo `company_id` TRÊN PHIẾU (công ty 3 → `cn-vinh.png`), 5 nhóm `rowspan`, số dạng `423,148` |
| Bản in danh sách | 292 dòng, `truncated=false`, 294 `<tr>` |
| Xuất Excel | 11 cột, `filter_text` đúng khoảng ngày |
| Giá vốn | `export-request-data` KHÔNG trả `cost_price` |
| Compile FE | 9/9 file hợp lệ (template + babel + cân dấu ngoặc style + import tồn tại) |


## Phase 8 — Test Playwright toàn luồng (2026-09-04)

Chạy trên `localhost:3000` + API `localhost:8000`, **dữ liệu thật** trên `gop_db`.
Đăng nhập bằng cách bơm JWT thật vào `localStorage` để thử được **4 vai** mà không cần mật khẩu.

### 4 LỖI THẬT tìm được và đã sửa

| # | Lỗi | Nguyên nhân | Đã sửa |
| --- | --- | --- | --- |
| 1 | **Sắp xếp cột "Ngày duyệt" không có tác dụng** — bấm xong bảng vẫn nguyên | FE gửi `sort_by=approved_time`, BE khai key `approvedTime` → BE âm thầm rơi về sắp mặc định (đúng bẫy skill list-page) | đổi key cột FE thành `approvedTime` (+ slot `#cell-approvedTime`) |
| 2 | **Tiêu đề tab trình duyệt hiện nguyên thẻ HTML** `...<span style="...">Không duyệt</span>` | nhét `buildStatusTitle()` (trả HTML cho topbar `v-html`) vào `head().title` | tách `documentTitle` (chuỗi thuần) cho tab, `pageTitle` (HTML) cho topbar |
| 3 | **Tên người lập trống** ở đầu màn Tạo (chỉ hiện dấu `–` + ngày) | đọc `$store.state.user.fullname` — khoá đúng là `current_employee_info.fullname` | sửa computed `creatorName` |
| 4 | **Toast lỗi upload ra tiếng Anh** "The given data was invalid." | Laravel 422 để câu tiếng Việt trong `errors`, `message` luôn là câu tiếng Anh | thêm `firstServerError()`, đọc `errors` trước |

### 2 lần "nghi lỗi" hoá ra là bẫy của công cụ test (không phải lỗi sản phẩm)

- Upload PDF tưởng không gắn được → thật ra S3 mất **13,5 giây**, tôi chỉ chờ 2,5s.
- Bấm "Quay lại" tưởng không cảnh báo "chưa lưu" → `fill()` của Playwright không phát sự kiện
  bàn phím nên `unsavedChangesMixin` coi là auto-fill. Gõ thật (`pressSequentially`) thì popup
  "Thông tin chưa lưu / Thoát / Ở lại" hiện đúng.

### Đã bấm thật và ĐỐI CHIẾU VỚI SQL

| Nhóm | Kết quả |
| --- | --- |
| **10/10 bộ lọc** khớp SQL tuyệt đối | Mã phiếu 7 · Trạng thái Đã duyệt 280 / Không duyệt 11 · Người tạo 120 · Người duyệt 109 · Mã hàng 91 · Tên hàng 94 · Khoảng ngày 24 · Công ty 172 · Phòng ban 157 · Tìm nhanh 158 |
| Ô ngày | hiện `dd/mm/yyyy`, **gửi lên ISO** `startDate=2026-07-01` — không dính bẫy `m/d/Y` |
| Khối tổ chức | gửi đúng `company_id` / `department_id`; chọn công ty thì phòng ban lọc 68 → 31 |
| Ô tìm nhanh | KHÔNG tự tìm khi gõ, chỉ chạy khi bấm "Tìm kiếm" |
| Làm mới | xoá hết ô lọc **và** tải lại danh sách |
| Sắp xếp | 3 cột có icon sort (đúng `SORTABLE_COLUMNS`); sort cột mới huỷ sort cột cũ |
| Phân trang | STT trang 3 bắt đầu từ 21; đổi 20 dòng nhảy về trang 1, **chỉ 1 request** (dedupe chạy) |
| Ghi nhớ lọc | vào chi tiết rồi quay lại, `status=4` còn nguyên |
| 3 preset `?type=` | all 292 · accounting 292 · for-approve 1 — watcher `$route.query.type` bắn đúng |
| Cột Hành động | Chờ duyệt: 2 nút (Duyệt là `<a href>` thật + In); Đã duyệt: chỉ In (nút Duyệt **ẩn hẳn**) |
| Badge trạng thái | Chờ duyệt vàng `rgb(217,119,6)` · Không duyệt đỏ `rgb(220,38,38)` — đúng SRS |
| Cấu hình cột | 13 cột; **STT / Mã phiếu / Hành động khoá** không tắt được |
| Xuất Excel | mở popup chọn trường (không tải thẳng), 11 trường, file `.xlsx` tải về thật |
| In phiếu | letterhead **tải được** đúng công ty ghi trên phiếu (cty 1 → `ts-hn.png`, cty 3 → `cn-vinh.png`), số dạng `423,148`, khối ký "Người lập / Kế toán kho" |
| In danh sách | 292 dòng, dưới trần 2.000 nên không cảnh báo |

### Vòng đời ghi — chạy THẬT rồi dọn sạch

1. Tạo phiếu **PYCXHM-00299** (2 Xô 18L, đính kèm PDF) → toast "Yêu cầu của bạn đã được gửi."
2. DB đúng từng cột: mã `PYCXHM-` · status 2 · tổ chức snapshot · `attachments` = URL S3 (đúng cột
   ERP, KHÔNG phải bảng `files`) · `export_price` bình quân 1.073.927,10 · pivot 1 dòng
3. **Trừ chéo đúng**: phiếu chờ duyệt này làm "Đang mượn" của phiếu mượn nguồn giảm **3 → 1**
4. Đổi sang Kế toán kho → **Từ chối thật** → status "Không duyệt", người/ngày duyệt điền,
   lý do hiện, 2 nút duyệt **tự ẩn**
5. Từ chối xong hàng được **giải phóng lại**: "Đang mượn" về **3**
6. Xoá phiếu test → DB về đúng **292 / 686 / 990 / 607** như ban đầu

### Validate + phân quyền

- Form trống → 3 lỗi inline đúng chỗ, viền đỏ, **không gọi API lưu**
- SL vượt "Đang mượn" → lỗi inline "Vượt quá số đang mượn", vẫn **không gọi API lưu**
- Upload `.txt` → BE chặn (`mimes:pdf`), không file nào được gắn
- Popup Từ chối bỏ trống lý do → lỗi inline, **không gọi API**
- Tài khoản 0 quyền: cửa `?type=accounting` ra "Không có dữ liệu phù hợp", **ô lọc Công ty không
  hiện**, mở chi tiết phiếu người khác bằng URL → **403**
- Tài khoản `status = 0` (đã nghỉ): hệ thống chặn từ tầng auth (401)

### Sửa theo yêu cầu giữa chừng của user

**Khối File đính kèm làm giống màn Đề nghị thanh toán** — thay khối chip tự chế bằng **chính
component `AttachmentSection.vue`** của màn đó (lưới STT / Upload / Dung lượng / Xoá, upload ngay
lúc chọn file, có nút Xem trước / Tải xuống / Thay đổi).
Để dùng lại mà KHÔNG chép bản thứ hai, component đó được **tham số hoá** thêm 3 prop
`apiBase` / `allowedExtensions` / `maxSizeMb`, **mặc định đúng giá trị cũ** nên màn Đề nghị thanh
toán không đổi hành vi. Màn này truyền `api-base="finance/borrow-export-requests"` và
`:allowed-extensions="['pdf']"` (ràng buộc của ERP).

⚠️ Còn 2 file PDF test nằm lại trên S3 (`borrow_export_requests/test-dinh-kem*.pdf`) — không phiếu
nào trỏ tới, vô hại, giống ghi chú sẵn có của màn Đề nghị thanh toán.

---

### Checkpoint — 2026-09-04
Vừa hoàn thành: toàn bộ Phase 0-7 (BE 12 file mới + 4 file sửa · FE 7 file mới + 2 file sửa menu)
Đang làm dở: (không)
Bước tiếp theo: user review lại màn (đã test Playwright toàn luồng, xem Phase 8) — phần CHƯA kiểm
chứng được: đổi ĐVT khi hàng có nhiều đơn vị (dữ liệu thật chỉ có 1 ĐVT/hàng), và bản in trên máy
in thật
Blocked: (không)

### Việc treo, cần user quyết
1. `ProductExportRequest::dataForBorrowReturn()` của màn **Yêu cầu nhập hàng** đang THIẾU phép trừ
   `returning_qty` so với ERP → đề xuất trả nhiều hơn số thực còn mượn khi có phiếu khác treo.
   Là màn đang chạy thật → chưa đụng (spec mục 3).
2. Gộp 3 bản chép `manageableDepartmentIds()` ở `PrepickExtendRequest` / `PrepickCancelRequest` /
   `PrepickTransferRequest` về trait dùng chung (đã đưa lên trait, chưa gỡ 3 bản cũ).
3. Nút "Tạo phiếu xuất hàng mượn" hiện chỉ báo "chưa triển khai" — mở được khi port màn
   `borrow_exports` (280 phiếu).

---

## Phase 9 — Popup "Chọn phiếu xuất mượn" dùng khuôn màn Phiếu thu (2026-09-05)

User yêu cầu: popup chọn phiếu ở màn Tạo dùng **cùng khuôn** với popup "Chọn phiếu đề nghị thu"
của màn **Phiếu thu** (`pages/finance/bill-incomes/components/IncomeRequestSearchModal.vue`).
User chốt: **giữ hành vi chọn NHIỀU** (1 yêu cầu xuất hàng mượn gom nhiều phiếu mượn), chỉ lấy
giao diện + phân trang.

- [x] BE `BorrowExportRequestService::exportRequestOptions()` — bỏ `limit(100)`, chuyển
      `paginate()`, trả thêm `total / current_page / per_page`. GIỮ NGUYÊN điều kiện lọc
      (type 3 · status 5 · borrow_status 2 · do mình lập · còn dòng chưa trả hết) và giữ envelope
      `responseJson` sẵn có (KHÔNG copy bản `paginatedResponse` thứ 4 vào Finance)
- [x] FE `ExportRequestPickerModal.vue` — viết lại theo khuôn `IncomeRequestSearchModal`:
      `size="xl"` + `modal-class` thu gọn · mở bằng `:id` + `$bvModal.show()` (nạp ở `@show`) ·
      bộ lọc `V2BaseLabel` + `V2BaseInput` + nút Tìm kiếm/Làm mới · bảng `thead` dính, khung cuộn
      `71vh`, **bấm cả dòng để chọn**, hover `#f0fdf4` · `V2BasePagination` · footer ghim đáy
- [x] 3 chỗ CỐ Ý khác khuôn phiếu thu: (1) chọn xong **không đóng** popup, dòng đã chọn tô nền +
      nhãn "Đã chọn"; (2) **bỏ** ô lọc "Người lập" và cột "Người tạo" — BE đã ép
      `created_by = auth()->id()` nên luôn là chính mình; (3) **không** copy `class="text-muted"`
      (scss chung ép thành chữ ĐỎ), đặt màu `#6b7280` thẳng
- [x] FE `BorrowExportRequestForm.vue` — đổi cách mở popup từ `v-if="showPicker"` sang
      `$bvModal.show(modalId)`
- [x] Kiểm chứng: compile FE + gọi lại API (đếm dòng, đo thời gian). Giao diện **user tự mở
      trình duyệt** xem (không tự chạy Playwright)

---

## Phase 10 — Seeder dữ liệu test (2026-09-05)

User chưa có dữ liệu để test popup mới → viết seeder sinh đủ 3 nhóm.
File: `hrm-api/Modules/Finance/Database/Seeders/BorrowExportRequestTestDataSeeder.php`
(bám khuôn `*TestDataSeeder` sẵn có của module: dry-run mặc định, bật bằng env, tiền tố mã riêng).

- [x] Nhóm A — 25 phiếu xuất mượn nguồn HỢP LỆ (`PYCXH-TEST-001…025`), hàng lấy từ nhóm
      **≥ 2 ĐVT đều có giá** (DB có 351 mặt hàng) ⇒ mở được điểm `plan.md` ghi là chưa kiểm chứng
      được: **đổi ĐVT** trên bảng chi tiết
- [x] Nhóm B — 6 phiếu BẪY, mỗi phiếu sai ĐÚNG 1 điều kiện (type · status · borrow_status ·
      đã trả hết · `need_export=0` · người khác) để chứng minh bộ lọc popup chạy đúng
- [x] Nhóm C — 12 yêu cầu xuất hàng mượn (`PYCXHM-TEST-01…12`) phủ đủ 4 trạng thái, có đính kèm
      + lý do từ chối; 3 phiếu **Chờ duyệt** ghim A21-A23 tạo **TRỪ CHÉO** để test `BorrowStockService`
- [x] Dry-run = dựng thật trong transaction rồi **rollback** (bắt được lỗi NOT NULL/FK, khác kiểu
      "chỉ in ra") · `FINANCE_TEST_CLEAN=1` xoá sạch · chạy lại không nhân bản
- [x] Kiểm chứng sau khi ghi thật: popup trả **25 phiếu / 3 trang**, không trùng không sót ·
      **6/6 phiếu bẫy bị loại** · trừ chéo đúng (A21 đã xuất 33, treo 2 → còn mượn 31; A24 không
      treo → 42) · dropdown ĐVT có 2 lựa chọn · dữ liệu thật nguyên vẹn (35.524 + 292)

---

## Phase 11 — Bảng chi tiết màn Tạo làm Y HỆT ERP (2026-09-05)

User phát hiện chênh: chọn phiếu mượn thì HRM tự sinh dòng hàng, ERP để trống. Truy ra không phải
lỗi dữ liệu — ERP tách 2 mảng (`form.details` = dòng con của phiếu mượn · `form.products` = hàng
hoá do người dùng tự thêm), bảng chỉ lặp trên `form.products`. **User chốt đảo quyết định lớn #6
của `design.md`: làm y hệt ERP.**

⚠️ **Đã đi sai một nhịp rồi sửa:** lần đầu tôi tự dựng popup riêng `ProductPickerModal.vue` +
2 endpoint `product-options` / `product-filter-options`. User chỉ ra **đã có popup CHUNG**
(`QuotationProductSearchModal` của màn Báo giá, màn **Yêu cầu chuyển hàng** đang dùng) → **xoá
popup tự chế + 2 endpoint đó**, chuyển sang dùng popup chung. Bài học vào memory
[[reuse-existing-pickers-and-v2base]]: gặp việc "chọn hàng hoá / KH / hợp đồng" thì **tìm popup
dùng chung TRƯỚC**, đừng dựng mới.

- [x] FE `BorrowExportRequestForm.vue` — thêm kho `sourceDetails` + `groupDetails()` (port ERP);
      nút `+` ở đầu cột cuối đúng vị trí ERP; dòng không khớp phiếu mượn nào bị **khoá + tô mờ**
      (`row-locked`, `rowSpan` tối thiểu 1); bỏ phiếu mượn KHÔNG xoá dòng hàng; số lượng đã gõ
      được giữ lại theo cặp (phiếu mượn, hàng hoá) khi thêm/bớt phiếu
- [x] FE dùng **popup chung** `QuotationProductSearchModal` với `goods-only` +
      `hide-manual-create` + `existing-products` — **y hệt cách màn Yêu cầu chuyển hàng dùng**,
      kể cả câu cảnh báo khi popup trả về hàng tạm (phiếu này chỉ nhận hàng thật)
- [x] BE `productUnits(int $id)` + route `GET /products/{id}/units` — popup chung chỉ trả 1 đơn
      vị, mà bảng này cho ĐỔI ĐVT nên phải nạp cả danh sách. Đặt tên khớp 4 màn Finance đang có
      đúng khuôn này (chuyển hàng · nhập hàng · điều chuyển thẳng · giữ hàng). KHÔNG trả `cost_price`
- [x] Xoá `ProductPickerModal.vue` + `productOptions()` + `productFilterOptions()` + 2 route cũ
- [x] Kiểm chứng: 3/3 file Vue compile · `productUnits` **2,8 ms**, trả đúng 2 ĐVT (Cái hệ số 1 ·
      Thùng hệ số 10) kèm giá, **không** có `cost_price`, id không tồn tại trả `null` → 404 ·
      **store() end-to-end**: gửi 2 dòng (1 hợp lệ + 1 khoá) → DB chỉ ghi **1 dòng hàng + 1 dòng
      chi tiết**, dòng khoá bị bỏ qua đúng thiết kế, chạy trong transaction rồi rollback sạch

---

## Phase 12 — Popup "Chọn phiếu xuất mượn" bỏ nốt điều kiện thừa so với ERP (2026-09-05)

User đối chiếu: popup ERP ra **27** phiếu, HRM ra **25**. Đo trên cùng DB `gop_db` → 2 phiếu chênh
là `PYCXH-TEST-X4` (đã trả hết) và `PYCXH-TEST-X5` (`need_export = 0`) — 2 trong 6 phiếu bẫy của
seeder. Nguyên nhân: HRM lọc thêm `whereExists(need_export = 1 AND base_exported_qty >
borrow_returned_qty)`, còn ERP đặt điều kiện đó ở `getDataForBorrowExport()` (lúc lấy dòng hàng).
**User chốt làm y hệt ERP.**

- [x] BE `exportRequestOptions()` — **bỏ** `whereExists(...)`. Còn đúng 4 điều kiện của ERP:
      `type = 3` · `status = 5` · `borrow_status = 2` · `created_by = mình`
- [x] Docblock ghi RÕ đây là lựa chọn có chủ ý + số đo, kèm câu "ĐỪNG sửa lại cho chặt nếu không
      hỏi user" — chống việc lần sau có người tưởng là sót rồi thêm lại
- [x] Cập nhật seeder: nhóm bẫy giờ chỉ còn **X1 · X2 · X3 · X6** bị popup loại; **X4 · X5 VẪN
      hiện** (đúng ERP), chọn vào ra 0 dòng hàng. Sửa cả docblock + dòng in báo cáo
- [x] Cập nhật `design.md` mục "3 chỗ SỬA so với ERP"
- [x] Kiểm chứng: popup HRM giờ `total = 27`, lật hết trang gom **27 mã không trùng**, và tập mã
      **GIỐNG HỆT** câu truy vấn ERP (so sánh mảng đã sort) · 4 phiếu bẫy còn lại vẫn bị loại ·
      chọn X4/X5 → `exportRequestData` trả **0 dòng hàng**, chọn `PYCXH-TEST-001` → **2 dòng**

---

## Phase 13 — Ô ĐVT dùng `V2BaseSelect` (2026-09-05)

User chỉ ra: ô Đơn vị tính trên bảng chi tiết đang là `<select class="form-control">` **trần**,
không dùng component base.

- [x] Đổi sang `V2BaseSelect` + method `unitOptions(row)` (nhãn kèm `(xHỆ_SỐ)` khi hệ số ≠ 1) —
      bám đúng ô ĐVT của màn **Yêu cầu chuyển hàng**
- [x] ⚠️ **Bẫy đi kèm, không sửa là hỏng ngầm**: `V2BaseSelect` là select2 nên giá trị bắn ra là
      **chuỗi** (`"40"`), còn `units[].unit_id` từ BE là **số** → `currentUnit()` so `===` sẽ không
      bao giờ khớp, ô ĐVT đổi mà **đơn giá / "Đang mượn" / Thành tiền đứng im**. Đã đổi sang so
      `String(...) === String(...)` ở `currentUnit()` và ở chỗ chọn đơn vị mặc định trong
      `loadUnits()` (màn Yêu cầu chuyển hàng cũng so chuỗi ở `selectedUnit()`)
- [x] Compile FE OK; grep lại không còn phép so `unit_id` kiểu strict

### Chưa làm — chờ user quyết

Ô **Số lượng xuất** vẫn là `<input type="number">` trần. Màn Yêu cầu chuyển hàng dùng
`V2BaseCurrencyInput` (có phân cách hàng nghìn, `:precision="0"`, cờ `:invalid`). Đổi thì được
đồng bộ + đúng skill `select-and-input-state` mục 4b, nhưng đụng vào luồng validate hiện đang
chạy đúng (`detailError()` + trần "Đang mượn") nên hỏi trước.

---

## Phase 14 — Gộp 3 ô chi tiết khi dòng hàng chưa có phiếu mượn (2026-09-05)

User: *"3 cột Phiếu mượn / Đang mượn / Xuất nếu chưa có phiếu mượn thì gộp lại thành 1"*.

- [x] Màn **Tạo** — dòng khoá giờ render `<td colspan="3">Chưa có phiếu mượn</td>` thay cho
      3 ô riêng (trước là `Chưa có phiếu mượn | — | —`, vừa rối vừa làm người dùng tưởng ô "Xuất"
      còn nhập được)
- [x] Màn **Chi tiết** (`_id/index.vue`) — áp cùng quy tắc cho đồng bộ: `rowDetails()` trả `[null]`
      thay cho object giả, template gộp `colspan="3"`
- [x] Màu chữ ô gộp đặt THẲNG (`#9ca3af` / `.locked-note`), KHÔNG dùng `text-muted` (scss chung
      ép class đó thành ĐỎ)
- [x] Compile FE OK (2/2 file)

---

## Phase 15 — Nút trong bảng chi tiết dùng `V2BaseIconButton` (2026-09-05)

User: *"button xóa đang chưa được đồng nhất với các màn khác"*. Đúng — nút xóa dòng đang là
`<button class="btn-row-remove">` tự chế + icon `ri-close-line`.

- [x] Nút **Xóa dòng** → `V2BaseIconButton size="sm" danger` + icon **`ri-delete-bin-line`** +
      `v-b-tooltip.hover.top="'Xóa dòng'"` — khớp khuôn `AdditionDetailTable.vue` (màn Đề nghị
      hạch toán bổ sung) và đúng skill `button-convention` mục 3 + 6
- [x] Nút **`+` thêm hàng hóa**: tôi đổi sang `V2BaseIconButton` rồi **user bảo để như cũ** →
      trả lại `<button class="btn-row-add">` kiểu chữ-link xanh. ĐỪNG "chuẩn hoá" lại lần nữa —
      đây là ý user, đã ghi luôn comment cạnh khối CSS
- [x] Xóa khối CSS tự chế `.btn-row-remove` (nút `+` giữ `.btn-row-add`)
- [x] Compile FE OK. `<button>` tự chế còn lại trong màn: đúng **1 cái** là nút `+` (user chốt
      giữ) + nút × chuẩn của `b-modal`

⚠️ Ghi để khỏi chép nhầm: màn **Yêu cầu chuyển hàng** cũng đang dùng `<button class="btn btn-link
text-danger p-0">` tự chế cho nút xóa dòng — **KHÔNG phải khuôn chuẩn**, đừng lấy làm mẫu. Khuôn
chuẩn là `AdditionDetailTable.vue`.

---

## Ghi chú — Khối nút màn Tạo KHÁC ERP có lý do (2026-09-05, user chốt GIỮ NGUYÊN)

User hỏi vì sao ERP là **"Gửi"** mà HRM là **"Gửi duyệt" + "Lưu và tiếp tục"**. Truy ra: khác biệt
này **không phải** quyết định port màn, mà là quy ước SẴN CÓ của HRM.

| Chỗ | ERP (`create.blade.php` :18-28) | HRM | Nguồn |
| --- | --- | --- | --- |
| Nút chính | `Gửi` | **Gửi duyệt** | Bảng chữ chuẩn `button-convention` mục 4.2 ("Gửi đi để duyệt → Gửi duyệt"). **42 file FE** đang dùng chữ này |
| Nút phụ | *(không có)* | **Lưu và tiếp tục** | Redmine **#11177** — chỉ ở màn Tạo mới; có mixin dùng chung `saveAndContinueMixin`, **24 màn** đang dùng |
| Nút thoát | `Hủy` (đỏ) | **Quay lại** (`V2Footer`) | Bảng chữ chuẩn mục 4.2; thoát form không phải thao tác phá huỷ nên không tô đỏ |

**User chốt GIỮ NGUYÊN** (2026-09-05) — sửa riêng màn này thì nó thành cá biệt giữa 42/24 màn kia.
Lần sau đối chiếu ERP thấy lệch chỗ này thì **đừng sửa**, đọc lại bảng trên.

---

## Phase 16 — Section header + bảng chi tiết theo khuôn màn Đề nghị thanh toán (2026-09-05)

User: *"header Thông tin chung / Chi tiết khác các màn khác, sửa cho giống màn Đề nghị thanh toán"*
và *"cả table chi tiết nữa, chưa có scroll trên"*.

Nguyên nhân: màn này tự dựng khối `.c-section` (bo góc 12px, đổ bóng, header nền `#f7f9fc` + icon
tròn màu). Trong khi khối **File đính kèm** lại là component mượn thẳng từ màn Đề nghị thanh toán
(`AttachmentSection.vue`) nên dùng khuôn `card` — 3 khối cạnh nhau mà 2 kiểu.

- [x] **Màn Tạo** — 2 section (`Thông tin chung`, `Chi tiết`) đổi sang khuôn
      `<div class="card"><div class="card-header section-header py-2 …"><h6>`, bỏ icon tròn tự chế;
      style `.card-header.section-header` copy nguyên từ `BillPaymentRequestForm.vue`
- [x] **Màn Chi tiết** (`_id/index.vue`) — 3 section đổi y hệt (Thông tin chung · File đính kèm ·
      Chi tiết), để 2 màn của cùng feature không lệch nhau
- [x] **Bảng chi tiết CẢ 2 MÀN** bọc bằng `V2BaseTableScroll body-class="table-responsive
      table-auto-height"` → có **thanh cuộn ngang ở CẢ TRÊN VÀ DƯỚI**, đúng component bảng chi tiết
      màn Đề nghị thanh toán đang dùng
- [x] Cột nội dung đổi `width` → **`min-width`** (giữ `width` cho cột STT 44px và cột nút 50px):
      `width` chỉ là gợi ý, màn hình hẹp là trình duyệt bóp cột cho vừa khung → chữ ép xuống nhiều
      dòng và **thanh cuộn ngang không bao giờ hiện**
- [x] Style bảng lấy đúng `.detail-table` bên đó: `th` nền `#f5f6f8`, 12px, `nowrap`, padding
      `4px 6px`; `td` 12px. Bỏ `class="bg-light"` trên `<thead>` (nền do CSS lo)
- [x] Xóa toàn bộ style `.c-section` / `.section-header` / `.section-body` / `.sec-goods` /
      `.sec-files` ở cả 2 file
- [x] Compile FE OK (2/2 file); grep lại không còn `c-section` / `bg-light` nào

### Còn 1 điểm khác, CHƯA sửa vì cần user xác nhận bằng mắt

Vỏ trang: màn Đề nghị thanh toán là `<div class="v2-styles"><div class="container-fluid px-0">`,
màn này là `<div class="v2-styles min-vh-100 pt-2"><div class="container-fluid">`. Tức card bên
này **thụt vào 15px hai bên** còn bên kia sát mép. Đổi thì giống hẳn nhưng ảnh hưởng cả padding
trên của trang → chờ user xem rồi quyết.

---

## Phase 17 — Fix: dòng KHOÁ làm lưu phiếu nổ 422 (2026-09-05)

Phát hiện khi soát lại `BorrowExportRequestStoreRequest` để viết hướng dẫn test.

**Lỗi:** từ Phase 11 (bảng chi tiết làm như ERP), người dùng thêm hàng không nằm trên phiếu mượn
nào → dòng KHOÁ, `details = []`. FE vẫn gửi dòng đó lên. Mà rule khai
`products.*.details => required|array|min:1` → **422 ở tầng validate**, chưa kịp tới
`storeProducts()` (chỗ vốn đã biết bỏ qua dòng này). Người dùng chỉ thấy toast lỗi khó hiểu.

Test cũ KHÔNG bắt được vì tôi gọi thẳng `service->store()`, tức **đi vòng qua FormRequest** —
đúng cái tầng đang gây lỗi.

- [x] FE lọc `products` bỏ dòng `details` rỗng trước khi gửi. Không nới rule BE: rule đang đúng,
      lỗi nằm ở chỗ FE gửi rác lên
- [x] Không lo gửi mảng rỗng: `hasBlockingError()` đã chặn khi `totalQty <= 0` nên phiếu chỉ toàn
      dòng khoá không bao giờ gọi API

---

## Phase 18 — Ô "Số lượng xuất" dùng `V2BaseCurrencyInput` (2026-09-05)

User chỉ ra nốt ô cuối cùng còn là thẻ trần (chính chỗ tôi đã ghi "chờ user quyết" ở Phase 13).

- [x] `<input type="number">` → **`V2BaseCurrencyInput`** `size="sm"` `placeholder="0"`
      `:precision="0"` `:invalid` `class="text-right"` — cùng khuôn ô số của bảng chi tiết màn
      Đề nghị thanh toán. `precision = 0` vì số lượng mượn luôn nguyên (`borrowedQty()` làm tròn XUỐNG)
- [x] **CỐ Ý không dùng prop `max`** của component (kẹp trần ngay khi gõ): kẹp thì ô tự kéo số về
      trần mà không nói gì, người dùng không hiểu vì sao. Giữ báo lỗi đỏ inline "Vượt quá số đang
      mượn" như đang chạy
- [x] Compile OK; grep toàn file **không còn `<input>` trần** nào

---

## Phase 19 — Màn Chi tiết dựng giống hẳn form Tạo mới (2026-09-05)

User: *"màn chi tiết form lại khác, sửa lại giống form tạo mới"*.

Gốc rễ: màn Đề nghị thanh toán **không viết màn chi tiết riêng** — nó dùng lại chính component form
với `readonly`, nên Xem và Sửa không bao giờ lệch. Màn này tôi viết 2 file riêng nên trôi mỗi nơi
một kiểu. **User chốt hướng nhẹ**: giữ 2 file, chỉ đồng bộ giao diện (không refactor form đang vừa
tinh chỉnh xong).

- [x] **Thông tin chung**: bỏ lưới `dl / dt / dd` (`kv-grid`), dựng lại bằng **ô-có-nhãn** đúng
      khuôn form Tạo — `form-row` + `V2BaseLabel` + `V2BaseInput :disabled` (`col-md-3`).
      Kiểu ô khoá không tự khai màu: rule chung ở `v2-styles.scss` lo (nền `#f1f5f9`, chữ
      `#475569`, KHÔNG `opacity`) — skill `select-and-input-state` mục 3
- [x] **Trạng thái** giữ `V2BaseBadge` chứ không nhét vào ô khoá (ô khoá sẽ nuốt mất màu do BE trả)
- [x] **Ghi chú** → `V2BaseTextarea :disabled`, **Phiếu xuất mượn** → khung `req-box-view` cùng tông
      với ô khoá, chips vẫn là link mở tab mới sang màn Yêu cầu xuất hàng
- [x] **File đính kèm**: bỏ `<ul>` tự dựng, dùng **chính `AttachmentSection`** của màn Tạo với cờ
      `readonly`. ⚠️ KHÔNG truyền `request-id` — prop đó khiến khối gọi
      `GET {apiBase}/{id}/attachment-sizes`, endpoint màn này CHƯA có
- [x] Đổi tên cột `ĐVT` → `Đơn vị tính` cho khớp bảng bên form
- [x] Dọn style chết: `.kv-grid` / `.kv` / `.kv--block` / `.kv-note` / `.file-list` / `.file-item`
      + 2 media query của `kv-grid`, và method `fileName()` không còn ai gọi
- [x] Compile FE OK (2/2 file)

**Vẫn khác form một cách CÓ CHỦ Ý** (đừng "sửa cho giống"): bảng chi tiết màn Xem có cột
**Xuất / Được duyệt**, form Tạo có **Đang mượn / Xuất** — hai màn hiển thị hai giai đoạn khác nhau
của phiếu. Màn Xem cũng có thêm Mã phiếu · Trạng thái · Người duyệt · Ngày duyệt · Lý do từ chối.

---

## Phase 20 — Màn Chi tiết: cắt về ĐÚNG thông tin ERP hiển thị (2026-09-05)

User: *"xem màn bên ERP để những thông tin gì thì lấy những thông tin đó thôi"* + *"bỏ cái trạng
thái trên title đi"*.

Đối chiếu `warehouse/borrow_export_requests/show.blade.php` của ERP — màn Xem chỉ có:

| ERP có | Ở đâu |
| --- | --- |
| Người lập – Ngày lập | góc phải header card "Thông tin chung" (:19-21) |
| Phiếu xuất mượn (chips link, tab mới) | :24-35 |
| Ghi chú | :36-42 |
| Phòng ban yêu cầu | :43-48 |
| File đính kèm | :49-60 |
| Bảng Chi tiết (Phiếu mượn / Xuất / Được duyệt) | :63-121 |
| **Ghi chú duyệt** — card RIÊNG sau bảng, chỉ hiện khi có | :125-135 |

- [x] **BỎ 7 trường** không có bên ERP: Mã phiếu · Trạng thái · Người tạo · Ngày tạo · Công ty ·
      Người duyệt · Ngày duyệt (BE vẫn trả, chỉ FE không hiện — bản in/Excel còn dùng)
- [x] Thêm **"Người lập – Ngày lập" ở góc phải header** card Thông tin chung, đúng chỗ ERP đặt
- [x] Đổi nhãn `Phòng ban` → **`Phòng ban yêu cầu`** (chữ của ERP), đưa xuống dưới Ghi chú đúng
      thứ tự ERP
- [x] **Lý do từ chối** tách khỏi Thông tin chung → **card riêng "Ghi chú duyệt"** đặt sau bảng
      Chi tiết, `V2BaseTextarea` khoá, chỉ hiện khi có nội dung — đúng ERP
- [x] **Bỏ badge trạng thái trên tiêu đề trang**: `pageTitle` giờ trả chuỗi thuần, gỡ import
      `buildStatusTitle`. `PageTitleMixin` vẫn theo dõi computed cùng tên nên topbar không mất tiêu đề
- [x] Dọn theo: import + đăng ký `V2BaseBadge`, style `.status-cell`, `.approve-note`
- [x] Compile FE OK

⚠️ Sau thay đổi này **màn Xem không còn hiển thị trạng thái ở đâu cả** — giống ERP. Muốn biết trạng
thái thì xem cột Trạng thái ở màn danh sách.

---

## Phase 21 — Loạt sửa nhỏ màn Chi tiết (2026-09-05)

- [x] **Ghi chú + Phòng ban yêu cầu cùng 1 dòng** — cả hai `col-md-6`, giữ thứ tự ERP (Ghi chú trước)
- [x] **Cột "Dung lượng" file không hiện**: `AttachmentSection` lấy dung lượng bằng
      `GET {apiBase}/{id}/attachment-sizes`, mà màn này CHƯA có endpoint đó nên tôi đã cố ý không
      truyền `request-id` → cột trống. Nay **bổ sung endpoint** + truyền `:request-id="id"`.
      BE dùng LẠI `BillPaymentAttachmentService` (`sizes()` chỉ nhận mảng URL, `parse()` static —
      không dính gì tới phiếu chi) thay vì chép bản thứ hai; gate cùng quyền với `show()`.
      Đo thật: phiếu `PYCXHM-TEST-02` → đọc được **240.377 byte (0,23 MB)** từ S3 trong 445 ms
- [x] **Màu nút "Tạo phiếu xuất hàng mượn"**: bỏ `status="success"` (#16a34a — nhóm Mở khóa /
      Khôi phục / Kích hoạt lại). Để `primary` trần ra teal `#1abc9c`, đúng nhóm "hành động chính /
      duyệt" của skill `button-convention` mục 2b
- [x] **Footer đè ra ngoài sidebar**: màn này tự dựng `.export-actionbar`
      (`position: fixed; left: 0` + `padding-left: 80px` bù trừ sidebar CỨNG) nên sidebar mở rộng
      là thanh nút đè lên. Thay bằng **`V2Footer`** như màn Tạo — component đó neo `right: 0` và
      KHÔNG khai `left` nên không bao giờ chạm sidebar, lại tự chừa chỗ đáy bằng class
      `has-v2-footer` trên `<body>`
- [x] Xếp lại thứ tự nút theo skill mục 5: **Tạo phiếu (primary) → In (secondary) → Từ chối
      (danger) → Quay lại (tertiary)**. "Quay lại" do chính `V2Footer` render, không tự thêm
- [x] Dọn theo: style `.export-actionbar*` + media print của nó, method `goBack()`,
      `style="padding-bottom: 72px"` thủ công trên vỏ trang
- [x] Compile FE OK · `php -l` sạch 2 file BE

---

## Phase 22 — Lịch sử thay đổi (2026-09-05)

Theo skill `entity-history`. **0 thay đổi schema** — dùng bảng CHUNG `catalog_histories` như 5 phiếu
Tài chính chị em, KHÔNG tạo `<entity>_history` riêng.

- [x] BE `BorrowExportRequestHistoryService` (trait `LogsCatalogHistory`, khuôn
      `BillIncomeHistoryService`). Theo dõi: `note` · `attachments` · 3 khoá **ẢO**:
      `export_request_codes` (danh sách mã phiếu mượn) · `products_rows` (**BẢNG** — mỗi dòng hàng
      hoá 1 bản ghi) · `product_detail_rows` (**BẢNG cấp 2** — SL xuất theo từng phiếu mượn, tách
      khoá riêng kèm cột "Thuộc hàng hóa", KHÔNG nhét vào chuỗi dòng cha — skill §3b)
- [x] `__key` ghép từ khoá **TỰ NHIÊN** (`product_id`, `product_id|export_request_id`) chứ không
      dùng id dòng: `storeProducts()` tạo mới toàn bộ dòng mỗi lần ghi nên id không bền
- [x] `catalogColumns()` **KHÔNG có `status`** — đổi trạng thái là dòng RIÊNG (skill §3a)
- [x] Điểm gọi: `store()` → `logCatalogCreate` (trong transaction, sau khi có đủ dòng hàng);
      `reject()` → `logCatalogStatus('rejected', 'Chờ duyệt' → 'Không duyệt')` **kèm `note` = lý do**
      (skill §4.1 — lý do đã lưu ở cột `comment` vẫn phải đẩy vào log)
- [x] Khai `borrow_export_requests` + nhãn cột tiếng Việt vào `CatalogHistoryService::TABLES`
      (file dùng chung — chỉ THÊM entry, không đụng logic)
- [x] FE **đủ 2 nơi** (skill §5.1): mục **Lịch sử** trong menu ⋮ màn danh sách →
      `CatalogHistoryModal`; khối **`SystemInfoSection`** trong thân màn chi tiết
      (`endpoint-base="catalog-histories"`), KHÔNG phải nút ở `V2Footer`
- [x] Không gắn quyền riêng — ai vào được màn thì xem được (mặc định skill §0)

### Kiểm chứng (chạy thật rồi rollback sạch)

| Điểm | Kết quả |
| --- | --- |
| Số dòng log sau tạo + từ chối | **2** |
| Thứ tự | **mới → cũ** (Từ chối trên, Tạo mới dưới) |
| Dòng Từ chối | nhóm `status`, nhãn "Từ chối", màu `#dc2626`, **có GHI CHÚ = lý do** |
| Nội dung đổi | `Trạng thái: Chờ duyệt → Không duyệt` (dòng riêng, không lẫn vào "Thay đổi thông tin") |
| Người thực hiện | `DNS01 · DNS Admin · PHÒNG CỘNG TÁC VIÊN_NV` |
| Bộ lọc "Loại hoạt động" | đúng **3 nhóm cố định**: Tạo mới · Thay đổi thông tin · Thay đổi trạng thái |
| Ô "Người thực hiện" | **783 nhân sự** (lấy từ `HistoryPerformerOptions`, KHÔNG suy từ log) |
| Dọn dẹp | `catalog_histories` max id **312 → 312**, phiếu về **305** — DB sạch |
| Compile FE | 2/2 file OK · `php -l` sạch 3 file BE |

⚠️ **292 phiếu cũ không có lịch sử** — không dựng lại được quá khứ. Lịch sử chỉ có từ phiếu tạo
sau khi deploy bản này.
