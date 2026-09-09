# Plan — Phiếu kế toán (ERP `bill_adjust_dept` → HRM)

> Phụ trách: @khoipv · Nhánh: `gop_db` (cả 2 repo) · Bắt đầu: 2026-08-28
> Design: `design.md` · Spec: `docs/superpowers/specs/gop-db/2026-08-28-finance-bill-adjust-dept-design.md`

---

## Phase 1 — Nền BE (entity, morphMap, quyền, route)

- [x] 1.1 Entity `BillAdjustDept` — bảng `bill_adjust_depts`, hằng trạng thái (Đang tạo = **xám**), quan hệ, accessor `is_can_view/is_can_edit/is_can_delete/status_text/status_type`
- [x] 1.2 Entity `BillAdjustDeptDetail` — bảng `bill_adjust_dept_details`, morphTo `contractable` + `objectable`
- [x] 1.3 Sinh mã `<mã cty>.PKT<mm><yy>.<5 số>` bọc transaction + `lockForUpdate`
- [x] 1.4 Bổ sung **4 morphMap** `objectable`: Customer / Supplier / Employee / Department
- [x] 1.5 Thêm **2 quyền guard `api`** vào `PermissionsTableSeeder` (tổng công ty / công ty)
- [x] 1.6 Khai 15 route (route tĩnh đặt TRƯỚC `/{id}`), gắn `checkPermission:Kế toán thanh toán` cho route ghi

## Phase 2 — Đọc: danh sách + chi tiết

- [x] 2.1 `BillAdjustDeptService::search()` — 12 ô lọc + phạm vi quyền 2 cấp + ẩn phiếu *Đang tạo* của người khác
- [x] 2.2 `BillAdjustDeptResource` (danh sách) + `DetailBillAdjustDeptResource` (chi tiết)
- [x] 2.3 `show()` gate bằng `is_can_view`, không qua → 403
- [x] 2.4 Kiểm chứng phạm vi quyền bằng SQL đếm theo 3 nhánh, so với số dòng API trả

## Phase 3 — Ghi: tạo / sửa / xóa (chưa duyệt)

- [x] 3.1 `BillAdjustDeptStoreRequest` + `UpdateRequest`
- [x] 3.2 `BillAdjustDeptWriteService::validateDetails()` — 5 luật theo nhóm định khoản
- [x] 3.3 `syncDetails()` — ghi 38 cột chi tiết + tính `total_amount`
- [x] 3.4 `store()` / `update()` — validate **trước** khi tạo phiếu; chặn nhảy cóc trạng thái
- [x] 3.5 `destroy()` — gate `is_can_delete`, trả trạng thái phiếu nguồn về *Chờ duyệt*
- [x] 3.6 Đính kèm file S3 (nối attachment của đề nghị nguồn khi có)
- [x] 3.7 Test 5 luật validate × ca đúng/sai

## Phase 4 — Ghi sổ cái (phần rủi ro nhất)

- [x] 4.1 `BillAdjustDeptAccountingService::buildEntries()` — **hàm thuần**, không DB / không `auth()`
- [x] 4.2 `persist()` — chỉ insert `account_details` + `account_detail_refs`
- [x] 4.3 3 nhánh `billable_*` (đầu kỳ / ProductExport / BorrowSell) — kiểm null từng bước
- [x] 4.4 `syncAdjustedMoneyBillIncomeReport()` — cộng `money_adjusted` cho dòng Phiếu báo có
- [x] 4.5 `processApproved()` — 5 bước đúng thứ tự ERP, bọc 1 transaction
- [x] 4.6 `BillAdjustDeptNotifyService` — thông báo chuông theo template `[PREFIX] {Nhóm hành động}: {Tên}. {Ghi chú}`
- [x] 4.7 **Unit test `buildEntries()`** với nhóm định khoản lấy từ phiếu ERP thật, so từng dòng sổ cái
- [x] 4.8 Chạy thử vòng đời đầy đủ trên dữ liệu thật, **bọc transaction rồi rollback**

## Phase 5 — Số dư lẻ + 5 cửa vào

- [x] 5.1 `BillAdjustDeptOddBalanceService::check()` — gom nhóm, so `companies.adjust_odd_balance`
- [x] 5.2 Sinh cặp bút toán đề xuất (Nợ 811/Có 1311 · Nợ 1311/Có 711), gắn `cost_debt` `DCSDCNKH`
- [x] 5.3 Cửa vào 2 — nạp từ Phiếu YCĐC, mặc định TK 1311, ẩn cột nhóm định khoản
- [x] 5.4 Cửa vào 3 — nạp từ Hạch toán bổ sung, copy `type`, ẩn cột phiếu YCXH khi `type = 7`
- [x] 5.5 Cửa vào 4 — nạp từ Hạch toán hoa hồng tháng *(màn nguồn chưa port — chỉ deep-link)*
- [x] 5.6 Cửa vào 5 — nạp từ Chi phí giao nhanh + cập nhật cờ đã hạch toán *(màn nguồn chưa port)*
- [x] 5.7 3 endpoint popup: `search-objects` · `search-contracts` (gộp `hrm_contracts` + `firm_contracts` + 6 loại ERP) · `search-export-requests`

## Phase 6 — In & xuất Excel

- [x] 6.1 `BillAdjustDeptPrintService` — letterhead theo **`company_id` trên chứng từ** (khuôn `BillIncomePrintService::headerUrl()`)
- [x] 6.2 `BillAdjustDeptExport` — Excel chi tiết 1 phiếu, ô tiền dạng số + data-format
- [x] 6.3 `BillAdjustDeptListExport` — Excel danh sách, BE trả đủ trường của `ExportFieldsModal`

## Phase 7 — FE màn danh sách

- [x] 7.1 `pages/finance/bill-adjust-depts/index.vue` — 4 mixin, `localStorageKey` + `columnScreenKey` duy nhất
- [x] 7.2 12 ô lọc bằng `V2BaseSmartFilterPanel` + schema `filterFields`
- [x] 7.3 11 cột + căn lề SRS + `V2BaseBadge` qua `utils/statusBadgeVariant.js`
- [x] 7.4 `getRowActions()` — Sửa → Xóa → In → Xuất Excel, gate bằng cờ BE, handler `switch (action)`
- [x] 7.5 Toolbar: Tạo mới → Xuất Excel → Cấu hình cột (không có Import)
- [x] 7.6 Thêm mục menu vào `components/subsystem-menu/`

## Phase 8 — FE form + chi tiết + in

- [x] 8.1 `BillAdjustDeptForm.vue` — dùng chung cho tạo / sửa / chi tiết
- [x] 8.2 Khối thông tin chung + đổi loại tiền → tính lại toàn bộ cột quy đổi
- [x] 8.3 Bảng chi tiết 18 cột, header 2 tầng khi ngoại tệ, nhập Nợ tự xóa Có
- [x] 8.4 3 popup — select trong popup dùng `V2BaseSelectInModal`
- [x] 8.5 Khối tick "số dư lẻ"
- [x] 8.6 `create.vue` · `_id/index.vue` · `_id/edit.vue` (3 file mỏng) + `unsavedChangesMixin`
- [x] 8.7 `_id/print.vue` — khổ ngang, bố cục mẫu ERP id 208
- [x] 8.8 Cờ quyền **fail-closed** — mọi cờ khởi tạo `false`, chỉ set từ `$store.state.permissions` hoặc field BE

## Phase 9 — Kiểm chứng & dọn

- [x] 9.1 Seeder dữ liệu test (khuôn `TEST.DNDCCN.*`) — có phiếu *Đang tạo* để bấm thử sửa/xóa
- [x] 9.2 Chạy 6 lệnh grep tự kiểm của skill `erp-to-hrm-screen` trên cả thư mục feature
- [x] 9.3 Compile sạch toàn bộ file FE (`vue-template-compiler` + babel — repo **không có ESLint config**)
- [x] 9.4 Đối chiếu ngược với ERP: đủ cột / đủ ô lọc / đủ hành động **và điều kiện ẩn hiện**
- [x] 9.5 Bàn giao user mở trình duyệt bấm thật — báo rõ phần chưa kiểm chứng

---

## Checkpoint — 2026-08-28

Vừa hoàn thành: **toàn bộ BE + FE của màn Phiếu kế toán** (Phase 1-9, trừ 9.1 và 9.5).

**Đã kiểm chứng bằng dữ liệu thật:**
- **Ghi sổ cái**: `buildEntries()` chạy trên **150 phiếu ERP ngẫu nhiên / 403 dòng bút toán**,
  so **33 cột** + toàn bộ `account_detail_refs` → **khớp tuyệt đối 150/150**.
  (Vòng đối chiếu đầu bắt được 2 lỗi thật, đã sửa: `optional(null)` trả object nên nhánh dự phòng
  người lập không chạy — 58 dòng lệch `company_id`/`department_id`; và entity hợp đồng của HRM
  không có quan hệ `employee_create` như `App\BaseModel` của ERP nên `created_by` lấy nhầm người
  lập phiếu — 280 dòng lệch.)
- **Phạm vi quyền**: 3 nhánh (tổng công ty / công ty / chỉ phiếu mình lập) + Super admin đối chiếu
  SQL → khớp 6/6 nhân viên thật.
- **Vòng đời**: lưu nháp → sửa → duyệt (ghi 2 bút toán + 2 dòng đối ứng) → chặn sửa/xoá phiếu đã
  duyệt (403). Bọc transaction rồi rollback, 0 dòng sót lại.
- **4/5 luật validate** nhóm định khoản: chặn đúng, ca hợp lệ lưu được. Luật 2 (vượt tiền Phiếu
  báo có) chưa dựng được ca thật.
- **10 endpoint** smoke test qua HTTP kernel: 200 hết. Popup hợp đồng trả đúng 372 hợp đồng
  (368 HĐ bán + 4 nguồn khác) cho khách hàng có dữ liệu.
- **FE**: 9/9 file compile sạch (`vue-template-compiler` + babel); 5 lệnh grep tự kiểm của skill
  `erp-to-hrm-screen` sạch tuyệt đối.

Đang làm dở: không có.

Bước tiếp theo: **9.5** user mở trình duyệt bấm thật. Seeder đã chạy: 5 phiếu `TEST.PKT.0000x`
trạng thái *Đang tạo* gán cho NV #13 (tài khoản dev), mỗi phiếu 1 nhóm định khoản đã cân sẵn nên
mở ra bấm "Lưu và duyệt" được ngay. 0 bút toán nào được ghi vào sổ cái.

Blocked: [để trống]

### Phần CHƯA kiểm chứng được (ghi rõ để không nhầm là đã xong)
| Hạng mục | Lý do |
| --- | --- |
| Nhánh `exportable_*` (phiếu YC xuất hàng) | `exportable_type` NULL ở **33.409/33.409** dòng thật — code chết của ERP |
| Nhánh `is_begin` (số dư đầu kỳ) khi ghi sổ | `is_begin = 1` ở **0/33.409** dòng thật |
| Cửa vào 4 — Hạch toán hoa hồng tháng | bảng nguồn **0 dòng**, màn nguồn chưa port |
| Cửa vào 5 — Chi phí giao nhanh | màn nguồn chưa port; `fast_delivery_employee_id` do service báo cáo ERP tính, HRM chưa có nguồn nên để null |
| Nghiệp vụ số dư lẻ | chưa dựng được hợp đồng có dư lẻ trong ngưỡng để chạy thật |
| Toàn bộ thao tác FE | chưa mở trình duyệt — user tự bấm |


---

## Phase 10 — Kiểm thử Playwright + đối chiếu trực tiếp với ERP (2026-08-28)

Chạy thật trên trình duyệt: HRM `localhost:3000` ↔ ERP `127.0.0.1:8002`, cùng tài khoản, cùng DB.

- [x] 10.1 Đối chiếu **20 bộ lọc** giữa 2 API (không lọc · mã phiếu · mã YCĐC · 3 trạng thái ·
      tài khoản theo số và theo tên · mã hợp đồng · 2 khoảng tiền · ngân hàng · 2 người lập ·
      2 khoảng ngày · 2 NVKD · khách hàng · kết hợp 2 điều kiện) → **20/20 khớp tuyệt đối**
- [x] 10.2 Đối chiếu danh sách trang 1: 11 cột × 10 dòng, tổng số bản ghi
- [x] 10.3 Bấm thật: sort 2 chiều + hủy sort cột cũ · phân trang · ghi nhớ bộ lọc khi quay lại ·
      popup "Cài đặt bộ lọc" · Cấu hình cột
- [x] 10.4 Nút hành động theo trạng thái: phiếu *Đang tạo* có Sửa/Xóa, phiếu *Đã duyệt* ẩn hẳn
- [x] 10.5 Màn chi tiết + màn sửa: nạp đúng dữ liệu, badge đúng màu, cảnh báo "chưa lưu" khi thoát
- [x] 10.6 Bảng định khoản: nhập Nợ tự xóa Có · cột quy đổi tự tính · **Thêm dòng tự điền chênh
      lệch** để nhóm cân · cảnh báo nhóm lệch
- [x] 10.7 3 popup: chọn đối tượng (tìm theo mã/tên, 3 loại KH/NCC/NV, chọn xong **reset sạch 6
      trường hợp đồng**) · chọn hợp đồng (nhánh KH 372 HĐ, nhánh NCC 104 HĐ) · phiếu YC xuất hàng
- [x] 10.8 Cửa vào 2 (từ Phiếu YCĐC): so **từng dòng** với `getDataForBillAdjustDept` của ERP →
      khớp tuyệt đối 3/3 dòng (tài khoản, số tiền, nhóm, đối tượng, hợp đồng, ngày hạch toán)
- [x] 10.9 **Duyệt qua giao diện** trên phiếu TEST → ghi đúng 2 bút toán + 2 dòng đối ứng chéo
      nhau; **đã dọn sạch**, sổ cái về đúng 972.053 dòng / max id 1001536 như trước khi test
- [x] 10.10 Xóa phiếu qua giao diện → phiếu + dòng chi tiết sạch
- [x] 10.11 Bản in: so ảnh chụp với bản in ERP cùng phiếu
- [x] 10.12 Xuất Excel 1 phiếu (có letterhead, ô tiền kiểu SỐ + `#,##0`) và Excel danh sách

### 7 lỗi tìm được và đã sửa

| # | Lỗi | Bằng chứng | Đã sửa |
| --- | --- | --- | --- |
| 1 | Cột **Phòng ban** ở danh sách/Excel lấy phòng ban NGƯỜI LẬP. ERP lấy của **phiếu YCĐC nguồn** — người lập luôn là kế toán nên cột đó thành vô nghĩa | lệch 4/10 dòng trang đầu so ERP | `BillAdjustDeptService::attachRequestDepartment()` |
| 2 | Màn **chi tiết** vẫn render `<input>` ở cột Mã khách + Đơn hàng/Hợp đồng | 2 ô nhập còn sót khi `readonly` | `AccountingDetailTable.vue` tách nhánh `v-if/v-else` |
| 3 | **Popup chọn hợp đồng trả `created_by` = ID**, trong khi cột `contract_created_by` là `varchar` chứa **TÊN** (18.149/18.149 dòng ERP đều là chữ) → NVKD hiện ra con số | ERP `searchAllContract` trả `fullname` | `BillAdjustDeptPickerService::loadCreatorNames()` |
| 4 | **Ô lọc NVKD chết hoàn toàn** — lọc id trên cột chứa tên | ERP: 84 và 25 phiếu · HRM: 0 và 0 | `searchByFilter()` quay về `whereHasMorph` như ERP |
| 5 | **Excel danh sách chỉ ra 2 cột**, mất 9 cột — `buildQueryString()` (util dùng chung) serialize mảng thành `fields=a&fields=b`, PHP chỉ nhận giá trị cuối | file tải về chỉ có STT + Trạng thái | FE gửi chuỗi `a,b,c`; BE `forData()` nhận cả 2 dạng |
| 6 | **Bản in lệch ERP**: thiếu cột NVKD, thừa cột Nhóm, tách đôi cột Tài khoản, thiếu ô ký BAN GIÁM ĐỐC, ghi "Cộng" thay vì "Tổng", dòng ngày sai định dạng, số tiền xuống dòng giữa con số | so ảnh 2 bản in cùng phiếu | `print.vue` dựng lại theo đúng 9 cột + 3 ô ký của ERP |
| 7 | Popup "Chọn trường xuất" không tự đóng sau khi xuất xong | quan sát trực tiếp | `index.vue` gọi `$bvModal.hide()` sau khi tải xong |

### Lỗi của ERP mà HRM sửa (đã chứng minh trên giao diện ERP thật)

| Lỗi ERP | Bằng chứng | HRM |
| --- | --- | --- |
| Ô lọc **"STK ngân hàng"** lọc cột `account_number` — cột KHÔNG TỒN TẠI trên `bill_adjust_dept_details` | ERP trả **HTTP 500** `Unknown column 'account_number'` | lọc đúng cột `bank_account_number` → ra 15 phiếu |
| Xoá phiếu kế toán không trả trạng thái cho Yêu cầu hạch toán bổ sung | đọc code `delete()` :344-366 | trả về *Chờ duyệt* |

### Vẫn CHƯA kiểm chứng được (không đổi so với trước)

Nhánh `exportable_*` và `is_begin` khi ghi sổ (0 dòng dữ liệu thật) · cửa vào Hoa hồng tháng
(bảng nguồn 0 dòng) và Giao nhanh (màn nguồn chưa port) · nghiệp vụ số dư lẻ (chưa dựng được hợp
đồng có dư lẻ trong ngưỡng) · phiếu **ngoại tệ** ở màn tạo/sửa (chưa có phiếu ngoại tệ nháp để bấm).

---

## Phase 11 — Rà chuẩn UI (soát lại 2026-09-05)

Kết quả soát toàn màn theo skill `button-convention` / `modal-popup` / `list-page` +
memory dùng chung. User chốt làm 2 việc trước: **màu nút footer** và **khối File đính kèm**.

### 11.1 Màu nút ở footer (skill button-convention §2b)

- [x] `BillAdjustDeptForm.vue:186` nút **Lưu**: `secondary` + icon `ri-draft-line`
      → `primary` (teal `#1abc9c`) + icon `ri-save-3-line`
- [x] `BillAdjustDeptForm.vue:194` nút **Lưu và duyệt**: bỏ `status="success"` (`#16a34a`)
      → `primary` trần = teal `#1abc9c`, đúng nhóm Duyệt (chốt 2026-08-20, cùng màu `V2Footer`)
- [x] `_id/index.vue` footer màn chi tiết: icon Xóa `ri-delete-bin-6-line` → `ri-delete-bin-line`,
      text nút **"In phiếu"** → **"In"** (bảng text chuẩn §4.2)
- [x] Thay `:disabled="saving"` → `:interactable="!saving"` trên cả 2 nút — `V2BaseButton`
      KHÔNG có prop `disabled` (`components/V2BaseButton.vue:24-49`), nút vẫn bấm được
- [x] Thêm `$safeLoadingStart()` / `$safeLoadingFinish()` (finally) + guard `if (this.saving) return`
      vào `submit()` — hiện bấm Lưu 2 lần tạo 2 phiếu, bấm Lưu và duyệt 2 lần ghi 2 bộ bút toán

### 11.2 File đính kèm — dùng lại khối của màn Đề nghị thanh toán

Bỏ `<input type="file">` + `<ul><li>` tự chế (form dòng 106-131), dùng
`pages/finance/bill-payment-requests/components/AttachmentSection.vue` qua prop `api-base`
(đúng cách màn `borrow-export-requests` đã làm 2026-09-04).

**BE** — khối này cần 3 endpoint theo khuôn `{apiBase}`:

- [x] Thêm `BillAdjustDeptAttachmentService::sizes()` (copy `BillPaymentAttachmentService::sizes()` —
      `Http::pool` HEAD lấy `Content-Length`)
- [x] Thêm `BillAdjustDeptController::attachmentSizes()` + route `GET /{id}/attachment-sizes`
- [x] Đổi route xoá file `POST /{id}/delete-file` → `DELETE /{id}/files` cho khớp 3 màn anh em
      (`bill-payment-requests` :689, `addition-accounting-requests` :794). Controller `deleteFile()`
      giữ nguyên — `$request->input('file_url')` đọc được cả query string của DELETE

**FE**:

- [x] `BillAdjustDeptForm.vue`: thay khối tự chế bằng `<AttachmentSection>` với
      `:files` / `:pending-files` / `:request-id` / `api-base` / `:error-message` / `:readonly`
- [x] Thêm 4 handler `onAddUploadedFile` / `onRemovePendingFile` / `onReplacePendingFile` /
      `onRemoveSavedFile` + state `pendingFiles`; `attachment_urls` khi lưu = files đã lưu + pending
- [x] Cập nhật `unsavedSnapshotSource()` cho khớp state mới
- [x] Bỏ `onFilesChosen()` / `removeAttachment()` / `fileName()` cũ

### 11.2b Bảng — thanh cuộn ngang ở CẢ TRÊN VÀ DƯỚI (skill list-page §3b-1)

- [x] `AccountingDetailTable.vue`: bỏ `<div class="table-responsive">`, bọc `<V2BaseTableScroll>`
      (trần, đúng như `bill-adjust-dept-requests/components/AdjustDetailTable.vue`)
      · bảng 17 cột, tổng min-width ~2.580px (VNĐ) / ~2.860px (ngoại tệ) → LUÔN tràn ngang, mà
        trước đó chỉ có thanh cuộn ĐÁY: phải kéo qua hết mọi dòng định khoản mới với tới nó
      · bỏ `.table-responsive` còn thoát rule global `assets/scss/default.scss:85`
        (`min-height: 50vh`) vốn kéo bảng 1-2 dòng lên hơn 400px

**Đã rà, KHÔNG phải sửa:**

- `index.vue` dùng `V2BaseDataTable`, prop `enableScrollSync` mặc định `true` → đã có thanh trên
- 3 bảng trong popup (`ObjectSearchModal` 4 cột / `ContractPickerModal` 4 cột / `ExportRequestSearchModal`
  3 cột, mỗi bảng chỉ 1 cột co giãn, modal `lg`/`xl`) → không tràn ngang, `V2BaseTableScroll` có bọc
  cũng tự ẩn thanh trên
- `_id/print.vue` dùng `<table>` trần — ĐÚNG: scoped CSS và component không sang được cửa sổ in
  (skill print-page §1)

### 11.3 Còn nợ (đã báo user, CHƯA làm)

`text-muted` ra chữ ĐỎ ở 14 chỗ (layout `default-sidebar` bọc `.training-layout`, import
`custom-assign.scss` ép `#dc3545 !important`) · 3 popup tự chế phân trang thay vì `V2BasePagination`
· card thiếu `card-header section-header` (lệch 2 màn anh em) · `<span class="text-danger">*</span>`
thay cho `<Required />` · 2 `BaseConfirmModal` xóa thiếu prop `danger` · popup duyệt thiếu mã phiếu ·
2 hàm xóa thiếu lớp tải · 6 nút phân trang popup thiếu icon + `:disabled` chết ·
ô Loại tiền chỉ báo lỗi bằng toast · `thead` bảng định khoản chưa sticky (17 cột, cuộn dọc là mất tiêu đề).

### Checkpoint — 2026-09-05

Vừa hoàn thành: Phase 11.1 (màu nút footer) + 11.2 (khối File đính kèm dùng chung) — BE 3 file sửa,
FE 3 file sửa. Compile sạch 4/4 file `.vue`; 2 route mới đã đăng ký (`GET /{id}/attachment-sizes`,
`DELETE /{id}/files`); `sizes()` / `attachmentSizes()` / `deleteFile()` đều resolve qua reflection.

Đang làm dở: không có.

Bước tiếp theo: user mở trình duyệt kiểm 4 việc chưa tự kiểm chứng được —
(a) 2 nút footer ra cùng teal `#1abc9c`,
(b) upload file ở màn Tạo → lưu → mở lại thấy file + đúng dung lượng,
(c) màn Sửa bấm Xóa file (popup xác nhận) → file mất hẳn, không quay lại sau khi Lưu,
(d) màn Chi tiết khối file ở chế độ chỉ đọc (không có nút Thêm tài liệu / Xóa).

Blocked: không có.

### ⚠️ Lỗi cũ mà việc thay khối đính kèm vừa sửa luôn

Khối tự chế gửi `attachment_urls` = TOÀN BỘ danh sách, trong khi BE
`BillAdjustDeptAttachmentService::uploadAttachments()` **NỐI** vào chuỗi cũ chứ không ghi đè
(`mergeSourceAttachments()` cuối cùng còn `array_unique`). Hệ quả: ở màn Sửa, **gỡ file rồi bấm Lưu
thì file quay trở lại** — chuỗi cũ trong DB vẫn còn URL đó. Khối dùng chung xoá file đã lưu bằng
`DELETE {api-base}/{id}/files` ngay lúc bấm nên hết lỗi này; `attachment_urls` giờ chỉ gồm file
chờ lưu.

---

## Phase 12 — Bố cục màn TẠO lệch ERP (user báo 2026-09-05)

User: *"bố cục màn tạo phiếu kế toán khác với bên erp, ví dụ không có phiếu yêu cầu điều chỉnh
công nợ"*. Đối chiếu `erp/resources/views/income_expenditure/bill_adjust_depts/form.blade.php`
(:100-220) + `create.blade.php` + `formJs.blade.php`.

### Bảng đối chiếu khối "Thông tin chung"

| # | ERP | HRM trước | Kết luận |
| --- | --- | --- | --- |
| 1 | **Phiếu yêu cầu điều chỉnh công nợ** — ô chỉ đọc + **nút kính lúp mở popup chọn**, hiện khi KHÔNG đến từ 3 nguồn kia (`form.blade.php` :100-113) | chỉ `v-if="form.bill_adjust_dept_request_code"` → màn Tạo mới **không có ô này, cũng không có đường chọn** | ❌ THIẾU HẲN — đúng cái user chỉ ra |
| 2 | **Tỷ giá** LUÔN hiện, khoá khi `type_money_id == 1`, kèm nút hiện tên tiền tệ (:153-166) | `v-if="isForeign"` → phiếu VNĐ không thấy tỷ giá | ❌ lệch |
| 3 | **Loại tiền** khoá khi đã có phiếu YCĐC (`ng-disabled="form.bill_adjust_dept_request_id"`, :141) | không khoá | ❌ lệch |
| 4 | Header card `Thông tin chung` + góc phải `<% form.creator %> - <% form.created_time %>` (:92-97) | card trần, không header; Trạng thái là 1 ô riêng trong lưới | ❌ lệch (cũng là mục 11.3 đã ghi) |
| 5 | Header card `Chi tiết` + nút "Thêm chi tiết" ở góc phải (:233-238) | `.section-title` tự chế trong card-body | ❌ lệch |
| 6 | Thứ tự hàng 1: nguồn → Ngày hạch toán → Loại tiền → Tỷ giá | Mã phiếu đứng đầu, đẩy lệch cả hàng | ❌ lệch |
| 7 | Không có ô Mã phiếu / Phòng ban | có (thông tin hữu ích, đúng khuôn HRM) | ✅ GIỮ, dồn xuống hàng 2 |
| 8 | Diễn giải `col-md-12`, File đính kèm `col-md-12` | giống | ✅ |

### Popup "Yêu cầu điều chỉnh công nợ" (ERP `formJs.blade.php` :66-89)

Nguồn `bill_adjust_dept_request.searchData` + ép `status = 2`
(= `STATUS_AWAITING_APPROVE` — *"Chờ tạo phiếu kế toán"*).
Cột: **STT · Mã phiếu · Ngày lập**. Ô tìm: **Mã phiếu** (text).
Chọn xong → `getDataForBillAdjustDept` điền: `bill_adjust_dept_request_id/code` · `note` ·
`details` · `date_accounting` · loại tiền + tỷ giá (**chỉ khi `request_type = 2` (NCC)**, YC khách
hàng ép về VNĐ).

→ HRM **KHÔNG cần BE mới**: `GET /finance/bill-adjust-dept-requests/pending` đã có sẵn và khớp
tuyệt đối (gate `isAccountant()` như middleware ERP, ép `status = STATUS_AWAITING_APPROVE`, giới hạn
theo công ty, hỗ trợ lọc `code`) — hiện chưa màn nào gọi. Nạp dữ liệu sau khi chọn dùng lại
`GET /finance/bill-adjust-depts/source-data?bill_adjust_dept_request_id=`.

### Task

- [x] 12.1 Tạo `components/BillAdjustDeptRequestPickerModal.vue` — khuôn `ObjectSearchModal.vue`
      (V2BaseModal), gọi `/finance/bill-adjust-dept-requests/pending`, 3 cột đúng ERP
- [x] 12.2 Ô "Phiếu yêu cầu điều chỉnh công nợ" + nút kính lúp; hiện khi không đến từ 3 nguồn kia
- [x] 12.3 Chọn xong → nạp `/source-data` (tách `loadSourceData` thành hàm nhận params dùng chung
      cho cả cửa vào bằng query lẫn popup)
- [x] 12.4 Tỷ giá LUÔN hiện, khoá khi VNĐ, hậu tố tên tiền tệ
- [x] 12.5 Loại tiền khoá khi đã có phiếu YCĐC
- [x] 12.6 Thêm `card-header section-header` cho 2 card ("Thông tin chung" + "Định khoản"),
      góc phải card 1 = badge trạng thái + "{Người lập} - {Ngày lập}" (khuôn
      `BillAdjustDeptRequestForm.vue` :17-37) — bỏ ô Trạng thái trong lưới
- [x] 12.7 Xếp lại hàng 1 đúng ERP: nguồn → Ngày hạch toán → Loại tiền → Tỷ giá;
      Mã phiếu / Người lập / Phòng ban xuống hàng 2

- [x] 12.8 Màn XEM: ô nguồn chỉ hiện khi phiếu THỰC SỰ có YCĐC và hiện dạng **link** sang phiếu
      yêu cầu (ERP `formShow.blade.php` :98-109) — không hiện ô rỗng kèm chữ "Chọn phiếu…"
- [x] 12.9 Đổi phiếu nguồn NCC (ngoại tệ) → phiếu KH: đặt lại `exchange_rate = 1` khi BE không trả
      trường này. `onCurrencyChange()` chỉ chạy khi user tự đổi ô, không chạy lúc gán bằng code →
      giữ tỷ giá cũ là nhân sai toàn bộ cột quy đổi (ERP cũng dính, HRM sửa)

### Checkpoint — 2026-09-05 (Phase 12)

Vừa hoàn thành: dựng lại bố cục màn Tạo theo ERP. 1 file FE mới
(`BillAdjustDeptRequestPickerModal.vue`) + 2 file sửa (`BillAdjustDeptForm.vue`,
`AccountingDetailTable.vue`). **0 file BE** — `GET /finance/bill-adjust-dept-requests/pending`
đã có sẵn và khớp đúng cái ERP làm.

Kiểm chứng bằng HTTP kernel (nhân viên id 13, có quyền *Kế toán thanh toán*):
`GET /bill-adjust-dept-requests/pending?per_page=3` → **HTTP 200, total 44 phiếu**, trả đủ
`code` + `created_at`; `GET /bill-adjust-depts/source-data?bill_adjust_dept_request_id=6890` →
**HTTP 200**, header 5 khoá + 2 dòng chi tiết. Compile sạch 3/3 file `.vue`.

Đang làm dở: không có.

Bước tiếp theo: user mở trình duyệt kiểm —
(a) `/finance/bill-adjust-depts/create` có ô "Phiếu yêu cầu điều chỉnh công nợ" + nút kính lúp,
(b) chọn 1 phiếu trong popup → điền mã phiếu + diễn giải + ngày hạch toán + bảng định khoản,
(c) phiếu VNĐ vẫn thấy ô Tỷ giá (khoá, hậu tố "VNĐ"),
(d) chọn phiếu YCĐC xong thì ô Loại tiền bị khoá,
(e) 2 card có tiêu đề "Thông tin chung" / "Định khoản", góc phải card 1 có badge + "{Người lập} - {Ngày lập}".

Blocked: không có.

### Chưa làm (khác biệt ERP đã cân nhắc rồi GIỮ nguyên bản HRM)

- Nút "Thêm dòng" — ERP ghi *"Thêm chi tiết"*; giữ chữ HRM theo bảng text chuẩn `button-convention` §4.2
- Tiêu đề khối bảng — ERP ghi *"Chi tiết"*; HRM để *"Định khoản"* (nói rõ nội dung khối hơn)
- Ô **Mã phiếu / Phòng ban** — ERP không có (ERP còn comment hẳn ô Mã phiếu ở `formShow`);
  HRM giữ vì hữu ích, dồn xuống hàng 2 để hàng 1 khớp ERP
- Popup chọn phiếu YCĐC dùng `V2BasePagination` (có cả chọn số dòng/trang) thay cặp nút
  "Trang trước / Trang sau" của ERP — HRM là nguồn của giao diện (skill `erp-to-hrm-screen`)

### 12.10 Đồng bộ ô chọn phiếu YCĐC theo khuôn màn Phiếu thu tiền (user chốt 2026-09-05)

User: *"chỗ chọn phiếu yêu cầu điều chỉnh công nợ sử dụng giống như chọn phiếu đề nghị của màn
finance/bill-incomes/create"*. Khuôn gốc: `bill-incomes/components/BillIncomeForm.vue` :14-30 +
`IncomeRequestSearchModal.vue`.

- [x] Ô nhập: **bỏ nút kính lúp riêng**, bấm THẲNG vào ô để mở popup; placeholder đổi thành
      *"Nhấn vào đây để chọn phiếu yêu cầu điều chỉnh công nợ"*; thêm class `.picker-input`
      (con trỏ bàn tay + nền TRẮNG dù `readonly`, copy :1295-1312 của màn kia)
- [x] Popup: thêm ô lọc **Người lập** (`V2BaseSelectInModal` — bắt buộc trong modal),
      dòng phụ ở header *"Chỉ phiếu đang Chờ tạo phiếu kế toán"*, `size="xl"`,
      bảng 4 cột (STT · Mã phiếu yêu cầu · Người lập · Ngày lập), bấm CẢ DÒNG để chọn
      (`.tr-hover` + `title`), `per_page` mặc định 10 như màn kia
- [x] `modalId` đổi thành `choose-bill-adjust-dept-request` cho cùng lối đặt tên
      (`choose-income-request`)

**Khác 1 điểm CÓ CHỦ ĐÍCH**: popup mới dựng trên `V2BaseModal`, không tự khai `b-modal` + header +
footer như `IncomeRequestSearchModal`. Skill `modal-popup` §0 chốt popup MỚI phải dùng khuôn chung;
bản ở màn Phiếu thu tiền có TRƯỚC khuôn đó nên còn tự dựng — chép lại là nhân thêm nợ kỹ thuật.

Kiểm chứng (HTTP kernel, nhân viên id 13 có quyền *Kế toán thanh toán*):
`/bill-adjust-dept-requests/pending` → HTTP 200, `per_page=10` ra 44 phiếu ·
`code=DNDCCN` ra 44 · `created_by=13` ra 4 — cả 3 ô lọc đều ăn, dòng trả về đủ
`code` / `created_by_name` / `created_at`. Compile sạch 2/2 file.

### 12.11 Bỏ ô KHÔNG có trong ERP (user chốt 2026-09-05 — *"bám sát erp cho tôi"*)

Đếm lại nhãn trong `erp/.../bill_adjust_depts/form.blade.php` (file này dùng cho **cả create lẫn
edit** — `edit.blade.php` không khai thêm nhãn nào): khối "Thông tin chung" có ĐÚNG **6 nhãn** —
phiếu nguồn · Ngày hạch toán * · Loại tiền * · Tỷ giá * · Diễn giải * · File đính kèm.
`formShow.blade.php` còn **comment hẳn** ô Mã phiếu (:92-96) và **không có trạng thái** ở bất kỳ đâu.

- [x] Bỏ 3 ô HRM tự thêm: **Mã phiếu · Người lập · Phòng ban**
- [x] Bỏ **badge trạng thái** ở góc phải đầu card — ERP không có trạng thái trong form lẫn màn xem.
      Góc phải giữ đúng 1 thứ ERP có: dòng `{Người lập} - {Ngày lập}`
      (`<% form.creator %> - <% form.created_time %>`)
- [x] Bỏ lệnh gọi `GET /finance/bill-adjust-depts/generate-code` ở màn tạo — ERP không xem trước mã,
      và mã thật do BE sinh lúc lưu (`BillAdjustDeptWriteService` :71), **không** nhận từ FE
      (`BillAdjustDeptStoreRequest` không có rule `code` cấp phiếu). Route BE giữ nguyên, nay không
      còn FE nào gọi
- [x] Dọn import chết theo: `V2BaseBadge`, `statusBadgeVariant`

⚠️ **Hệ quả cần user biết**: màn **Sửa / Chi tiết** giờ KHÔNG còn chỗ nào hiện trạng thái phiếu
(trước đây có badge). Trạng thái vẫn xem được ở cột "Trạng thái" ngoài màn danh sách. Đúng như ERP,
nhưng nếu muốn giữ badge riêng cho màn HRM thì báo để bật lại.

📝 User tự sửa trong lúc làm: nhãn ô tỷ giá đổi thành **"Tỷ giá (VND)"** và bỏ hậu tố tên loại tiền
(giữ nguyên, chỉ sửa lại comment cho khỏi mô tả sai).

**Khối "Thông tin chung" sau khi sửa — khớp 1-1 với ERP:**

| Vị trí | Ô | ERP |
| --- | --- | --- |
| đầu card | `Thông tin chung` + góc phải `{Người lập} - {Ngày lập}` | :92-97 |
| 1 | Phiếu yêu cầu điều chỉnh công nợ (hoặc 1 trong 3 nguồn kia) | :100-127 |
| 2 | Ngày hạch toán * | :131 |
| 3 | Loại tiền * | :140 |
| 4 | Tỷ giá * | :155 |
| 5 | Diễn giải * (`col-12`) | :170 |
| 6 | File đính kèm (`col-12`) | :180 |

### 12.12 Bảng chi tiết — cột nào CHO SỬA, cột nào CHỈ HIỂN THỊ (user báo 2026-09-05)

User: *"tiêu đề là chi tiết mà; cột mã khách hàng, phát sinh nợ, phát sinh có, đơn hàng/hợp đồng
bên erp chỉ hiển thị thôi, có cho chọn đâu"*.

Đọc `form.blade.php` :279-437. ERP gate từng ô bằng **điều kiện THEO DÒNG**, không phải theo phiếu:

```
rowLocked = form.bill_adjust_dept_request_id && !detail.fast_delivery_id
```

| Cột | `rowLocked` | không khoá | HRM trước |
| --- | --- | --- | --- |
| Số tài khoản | **select** (vẫn sửa) | select | ✅ đúng |
| **Mã khách** (:296-307) | **text** | ô + nút chọn | ❌ luôn cho chọn |
| **Phát sinh nợ / có** (:313-334) | **text** | input | ❌ luôn cho nhập |
| Diễn giải (:336) | **input** (vẫn sửa) | input | ✅ đúng |
| **Đơn hàng/Hợp đồng** (:343-357) | **text** | ô + nút — CHỈ khi `type` ∉ {1,5,7} | ❌ luôn cho chọn |
| checkbox `is_begin` (:361) | **disabled** | bật | ❌ chỉ khoá theo `readonly` |
| Phiếu YCXH (:369-378) | **text** | ô + nút khi `has_exportable && !is_begin` | ❌ chỉ gate `contract_type == 3` |
| Mã phí · Mã vụ việc | **select** (vẫn sửa) | select | ✅ đúng |

- [x] 12.12a Đổi tiêu đề khối bảng **"Định khoản" → "Chi tiết"** (ERP `<h4>Chi tiết</h4>` :235)
- [x] 12.12b Thêm prop `requestLocked` + `sourceType`; dựng `isRowLocked(row)` rồi gate đúng 4 cột
      user chỉ ra + checkbox `is_begin` + Phiếu YCXH
- [x] 12.12c Dòng tổng ghi **"Tổng"** thay vì "Cộng" (ERP :440)

### ⚠️ 2 khác biệt KHÁC phát hiện khi đọc, CHƯA làm — chờ user quyết

1. **Thiếu hẳn cột "Mã khế ước"**: ERP có `<th rowspan="2">Mã khế ước</th>` (:264) nhưng ô dữ liệu
   là `<td class="text-left v-align-middle"></td>` (:407) — **cột luôn RỖNG**. Thêm vào thì bảng 17
   cột thành 18 cột mà không có dữ liệu gì.
2. **Ngân hàng + STK ngân hàng: ERP cho CHỌN, HRM chỉ hiển thị chữ.** ERP là 2 `select`
   (:409-428): chọn ngân hàng (`banks`) thì xoá trắng STK, rồi chọn STK trong
   `detail.company_accounts`. HRM render `{{ row.bank_name }}` / `{{ row.bank_account_number }}`
   dạng chữ. Đây là **thiếu chức năng thật**, không phải lệch giao diện — cần BE trả thêm danh mục
   ngân hàng + tài khoản công ty theo dòng.

### Checkpoint — 2026-09-05 (12.12)

Vừa hoàn thành: gate 4 cột theo ĐIỀU KIỆN TỪNG DÒNG. Thêm 2 prop `requestLocked` / `sourceType`
và 3 helper `isRowLocked()` / `canPickContract()` / `canPickExportable()` trong
`AccountingDetailTable.vue`; thêm `fast_delivery_id: null` vào `normalizeRow()` để Vue 2 reactive
được khoá đó. Tiêu đề khối → **"Chi tiết"**, dòng tổng → **"Tổng"**.

Compile sạch 5/5 file. Chưa mở trình duyệt.

Bước tiếp theo: user quyết 2 việc ở mục ⚠️ trên — cột "Mã khế ước" (ERP có header nhưng ô luôn
rỗng) và Ngân hàng/STK (ERP cho CHỌN, HRM đang chỉ hiển thị chữ — thiếu chức năng thật, cần BE trả
thêm danh mục ngân hàng + tài khoản công ty theo dòng).

### 12.13 Khối "Số dư nợ đầu kì" hiện sai chỗ (user báo 2026-09-05)

User: *"sao bên hrm lại hiển thị Số dư nợ đầu kì: 0 ở chỗ đơn hàng vậy, bên erp có hiện đâu"*.

**Nguyên nhân:** HRM gate khối này bằng `v-if="row.contractable_id"` — tức **bất kỳ hợp đồng nào**
được chọn cũng hiện. ERP gate bằng `ng-if="detail.has_exportable"` (`form.blade.php` :359), mà
`has_exportable` là getter trong `partials/classes/IncomeExpenditure/BillAdjustDeptDetail.blade.php`
:14-17:

```js
get has_exportable() {
    if (this.contract_type == 3) return true;
    return false;
}
```

→ chỉ hợp đồng **loại 3** mới có khối này. Hợp đồng loại khác thì ERP không hiện gì, HRM hiện
"Số dư nợ đầu kì: 0" (số 0 vì `debt_begin` mặc định 0).

- [x] Thêm helper `hasExportable(row)` = `Number(row.contract_type) === 3` — mirror đúng tên getter
      của ERP; dùng cho CẢ khối checkbox lẫn `canPickExportable()` (trước đó `canPickExportable`
      đã đúng luật này rồi, chỉ khối checkbox lệch → 2 chỗ cùng 1 luật mà viết 2 kiểu)
- [x] Nhân tiện bỏ `class="text-muted"` trên nhãn đó → đặt màu thẳng `#6b7280`
      (style dùng chung ép `.text-muted { color: #dc3545 !important }` nên chữ đang ra ĐỎ)

### 12.14 Popup YCĐC lệch số phiếu: ERP 53 · HRM 44 (user báo 2026-09-05)

**Số liệu thật** (`bill_adjust_dept_requests`, `status = 2`): tổng **53** — công ty 1: **44**,
công ty 4: **9**. Chia theo `company_id` của phiếu và theo công ty người tạo cho **cùng kết quả**.

**Nguyên nhân:** ERP `BillAdjustDeptRequest::searchByFilter()` đặt TOÀN BỘ khối phân quyền trong
`if ($request->_type === 'all')` (:156-196), còn lọc công ty nằm riêng ở
`if ($request->_type == 'for-accounting')` (:200-204). Popup chỉ gửi `d.status = 2`,
**không gửi `_type`** → không nhánh nào chạy → ERP trả cả 53 phiếu của mọi công ty.
HRM gọi preset `pending` vốn lọc theo công ty người đăng nhập → 44.

**User chốt: bỏ lọc công ty, y hệt ERP (53 phiếu).**

- [x] Thêm `BillAdjustDeptPickerService::searchAdjustRequests()` + `searchRequests()` ở Controller
      + route `GET /finance/bill-adjust-depts/search-requests` (đặt TRƯỚC `/{id}`), cùng chỗ với
      3 popup còn lại của màn
- [x] FE trỏ sang endpoint mới (shape `{ data: { data, meta } }` như 3 popup kia)

**Vì sao KHÔNG sửa thẳng preset `pending`:** `pending` là quy ước chung toàn dự án cho **màn chờ
duyệt** — `BillIncomeRequest` :296, `BillPaymentRequest` :349-355, `AdditionAccountingRequest` :318
đều dùng nghĩa "cùng công ty + đúng quyền duyệt". Đổi nghĩa nó cho riêng màn này thì màn chờ duyệt
của Yêu cầu điều chỉnh công nợ (chưa làm) sẽ sai phạm vi mà không ai biết.

**VẪN gate `isAccountant()`**: ERP đặt `checkPermission:Kế toán thanh toán` trên chính route
`bill_adjust_dept.create` chứa popup, nên bỏ luôn gate là mở rộng hơn cả ERP.

Kiểm chứng (HTTP kernel, nhân viên id 13): `search-requests` → HTTP 200,
`per_page=5` ra **total = 53** (đúng bằng ERP) · `code=DNDCCN` ra 53 · `created_by=13` ra 4.

### ⚠️ RỦI RO ĐÃ BÁO USER, user chấp nhận

`BillAdjustDeptWriteService` :75 đặt `company_id` của phiếu kế toán theo **NGƯỜI LẬP**, không theo
phiếu YCĐC nguồn. Nên kế toán công ty 1 chọn 1 trong 9 phiếu của công ty 4 sẽ sinh phiếu kế toán
mang `company_id = 1` cho nghiệp vụ công nợ của công ty 4 → **bản in ra letterhead sai công ty**
(CLAUDE.md: letterhead lấy theo `company_id` ghi trên chứng từ) và **bút toán ghi thẳng vào sổ cái
`account_details` dùng chung với cổng ERP**.

Nếu về sau muốn vừa đủ 53 phiếu vừa không sai công ty → sửa `:75` lấy `company_id` từ phiếu nguồn.

---

## Phase 13 — Rà màn DANH SÁCH (user báo 2026-09-05)

### Đã sửa (5/7)

- [x] 13.1 **Đổi "Người lập"/"Ngày lập" → "Người tạo"/"Ngày tạo"** ở bộ lọc + bảng + popup chọn
      trường xuất + nhãn cột trong `BillAdjustDeptListExport::FIELDS`
- [x] 13.2 **Thêm cột Ngày cập nhật · Người cập nhật**
      · BE: `BillAdjustDeptListResource` trả `updated_at` (`d/m/Y H:i`) + `updated_by` +
        `updated_by_name`; thêm quan hệ `BillAdjustDept::employee_update()` (chưa hề có);
        eager-load `employee_update.info` ở CẢ 2 truy vấn (`searchByFilter` phân trang và
        `allForExport`) để không N+1
      · FE: 2 cột đặt ngay sau cặp cột tạo, thêm vào popup chọn trường xuất
- [x] 13.3 **Ô trống để TRỐNG**, bỏ hết dấu `—` (10 chỗ trong `index.vue`)
- [x] 13.4 **Chưa có tiêu đề trang** — `index.vue` khai `mixins: [PageTitleMixin]` nhưng
      **thiếu computed `pageTitle`**. Mixin theo dõi đúng computed đó rồi commit vào store để
      layout dựng tiêu đề; chỉ khai `head()` là mới đổi được `<title>` của trình duyệt.
      Khuôn: `bill-adjust-dept-requests/index.vue` :409-411
- [x] 13.5 **Placeholder chữ to chữ bé** — `V2BaseCurrencyInput` ở `size="sm"` để **13px**
      (`components/V2BaseCurrencyInput.vue` :252) trong khi `V2BaseInput` :126 /
      `V2BaseSelect` :490 / `V2BaseDatePicker` :288 cùng `size="sm"` đều **12px** → 2 ô
      "Số tiền từ/đến" to hơn hẳn. Sửa bằng style scoped ở màn (3 lớp selector để thắng rule
      `[data-v-comp]` của component). **Chưa sửa component dùng chung** — CLAUDE.md bắt hỏi trước.

### KHÔNG làm được / không phải lỗi (2/7)

- [ ] 13.6 **Ngày hạch toán thêm giờ — KHÔNG LÀM ĐƯỢC.** Cột `bill_adjust_depts.date_accounting`
      kiểu **`date`**, không phải `datetime`; đo thật: **0/12.632 dòng có giờ**. Thêm giờ vào chỉ
      ra `00:00` cho mọi phiếu. Muốn có giờ thật phải đổi kiểu cột — mà cột này **dùng chung với
      cổng ERP**, đổi là đụng cả 2 hệ thống. Chờ user quyết.
- [ ] 13.7 **Bộ lọc Công ty — KHÔNG PHẢI LỖI CODE.**
      `V2BaseCompanyDepartmentFilter.vue` :8 chỉ render ô Công ty khi `permissions['is_all_company']`.
      Đo thật với tài khoản đang test (nhân viên id 13, DNS Admin):
      `can_view_all_company = false`, `can_view_company = true` → đúng thiết kế, người chỉ xem được
      1 công ty thì không cần ô chọn công ty (và cho chọn là fail-open).
      Muốn thấy ô đó phải cấp quyền **"Xem tất cả phiếu kế toán của tổng công ty"** (id 1551, guard
      `api`). Ô Phòng ban vẫn hiện vì nó chỉ cần `is_company`.

Kiểm chứng: `GET /finance/bill-adjust-depts?per_page=2` → HTTP 200, mỗi dòng có đủ
`created_at`/`created_by_name` và `updated_at`/`updated_by_name`. Compile sạch `index.vue`.

### 13.6b Ngày hạch toán thêm giờ — ĐÃ LÀM theo yêu cầu user (2026-09-05, user nhắc lại)

Đã báo trước rằng cột `bill_adjust_depts.date_accounting` kiểu **`date`** (0/12.632 dòng có giờ);
user vẫn yêu cầu → `BillAdjustDeptListResource` đổi sang `d/m/Y H:i`, cột nới 140px → 150px.

Kết quả thật đúng như đã cảnh báo: `hach toan: 28/08/2026 00:00` cho **mọi** phiếu, trong khi
`tao: 28/08/2026 12:04` có giờ thật. Muốn giờ thật phải đổi kiểu cột sang `datetime` — cột dùng
chung với cổng ERP nên đụng cả 2 hệ thống.

### 13.1b Bỏ sót khi đổi tên (user chỉ ra)

Lượt trước mới đổi ô lọc `created_by` và 2 cột bảng; còn sót 3 nhãn, nay đã đổi:
`Ngày lập từ` → **Ngày tạo từ** · `Ngày lập đến` → **Ngày tạo đến** ·
`Khoảng ngày lập` → **Khoảng ngày tạo**. Đã grep lại: `index.vue` không còn chuỗi
"Ngày lập" / "Người lập".

### 13.5b Placeholder datepicker — theo CSS thì KHÔNG to hơn

Truy lại toàn bộ rule cỡ chữ ở `size="sm"`:

| Component | Dòng | font-size |
| --- | --- | --- |
| `V2BaseDatePicker` (base `.mx-input`) | :181 | 12px `!important` |
| `V2BaseDatePicker` (`--sm`) | :288 | 12px `!important` |
| `V2BaseInput` | :126 | 12px |
| `V2BaseSelect` | :490 | 12px `!important` |
| `V2BaseCurrencyInput` | :252 | **13px** ← thủ phạm, ĐÃ sửa ở 13.5 |

Không có rule toàn cục nào đè `.mx-input` (chỉ `custom-theme.scss` :230 và `v2-styles.scss` :47,
đều là `:disabled`). `font-size: 15px` ở `V2BaseFilterFieldControl` :89 là của **nút × xoá nhanh**,
không phải placeholder.

→ Ô to hơn là cặp **"Số tiền từ / Số tiền đến"** (`V2BaseCurrencyInput`), không phải cặp ngày.
Nếu sau khi Ctrl+Shift+R mà vẫn thấy lệch thì đo bằng snippet ở mục dưới rồi báo lại số đo.
