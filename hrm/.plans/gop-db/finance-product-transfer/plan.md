# Plan — Port màn Phiếu điều chuyển hàng (ERP → HRM)

**Người phụ trách:** @junfoke — 2026-09-04
**Nhánh:** `feat/finance-product-transfer` (hrm-api + hrm-client)
**Design:** [design.md](./design.md) · **Khảo sát:** [khao-sat.md](./khao-sat.md)

Quy ước: `[ ]` chưa làm · `[x]` xong · mỗi task ghi rõ file đụng tới.

---

## Phase 0 — Chuẩn bị

- [x] 0.1 Khảo sát ERP + xác định trùng tên menu → `khao-sat.md`
- [x] 0.2 Trả mục menu *Phiếu yêu cầu chuyển hàng* về nhóm *Xuất hàng*, giải phóng mục
      *Phiếu điều chuyển hàng* ở nhóm *Điều chuyển* — `components/subsystem-menu/finance.js`
- [x] 0.3 Sửa 2 rule đã lỗi thời trong skill `erp-to-hrm-screen` (SKILL.md :204-205): số theo chuẩn
      quốc tế `1,234,567.89`, ô rỗng để trống — cho khớp `export-excel` / `print-page` / `list-page`.
      → user duyệt 2026-09-04, đã sửa `SKILL.md` :204-205 (rà cả `references/`, không còn chỗ nào sót)
- [ ] 0.4 Viết spec đầy đủ `docs/superpowers/specs/gop-db/2026-09-04-finance-product-transfer-design.md`

## Phase 1 — Tách FIFO ra service dùng chung (làm TRƯỚC, có test hồi quy)

- [x] 1.1 Dựng bộ số liệu gốc — `fifoValue()` là hàm CHỈ ĐỌC nên test trực tiếp trên dữ liệu thật,
      không cần chạy phiếu (không ghi DB, chạy lại bao nhiêu lần cũng được): **60 ca `fifoValue`**
      (log xuất thật, đúng bộ tham số `updateWarehouse` dùng) + **25 ca `layerQtyPrice`** phủ **đủ 4
      nhánh** `objectable_type`. Script: `scratchpad/fifo_baseline.php` → `fifo_before.json`
- [x] 1.2 Tạo `Modules/Assign/Services/StockValueFifoService`: bê **nguyên khối** `fifoValue()` +
      `layerQtyPrice()` từ `WarehouseExportAccountingService` (:150-211) + 4 hằng FQN.
      Không đổi tham số / kiểu trả về. Docblock có mục **"Nơi đang dùng"**
- [x] 1.3 `WarehouseExportAccountingService`: 2 method cũ thành **wrapper 1 dòng** gọi service mới →
      `ProductExportService.php:245` không phải sửa
- [x] 1.4 **Test hồi quy PASS**: chạy lại đúng bộ ở 1.1 sau khi tách → `fifo_after.json` **giống hệt**
      `fifo_before.json` (diff sạch). Kiểm thêm: gọi qua wrapper vs gọi thẳng service mới lệch
      **0/25 ca**; 4 hằng FQN khớp; `ProductExportService` resolve OK; `php -l` sạch 2 file

## Phase 2 — Backend: đọc (danh sách + chi tiết)

- [x] 2.1 Entity `ProductTransfer` + `ProductTransferDetail` (`Modules/Finance/Entities/ProductTransfer/`)
      — `canView/canEdit/canCreate`. Trạng thái: Resource trả **`status_text` + `status_color` (mã hex)**
      theo CLAUDE.md (chữ VÀ màu do BE quyết, FE chỉ hiển thị) — *Đang tạo* = `#64748B` (nháp/xám),
      *Đã hạch toán* = `#16A34A` (hoàn thành). ERP để "Đang tạo" = `danger` (ĐỎ) → **không bê sang**
- [x] 2.2 `ProductTransferService::searchByFilter` — phạm vi quyền áp **vô điều kiện** (bỏ bọc
      `if type == 'all'` của ERP); lọc đủ: mã phiếu · kho vật lý · trạng thái · người tạo ·
      mã hàng hoá · tên hàng hoá · khoảng ngày. **Bỏ** lọc *Người duyệt*
- [x] 2.3 `index` + `show` + 2 Resource (`ProductTransferListResource` / `...DetailResource`);
      `show` chặn `canView()` → **verify: phiếu của mình 200, phiếu người khác 403**
- [x] 2.4 Dropdown: kho vật lý (`warehouses`) + kho kế toán lọc `company_id` + `status=1` +
      `warehouse_id`; kho đã khoá đang gắn phiếu vẫn trả về (cờ 🔒)
- [x] 2.5 `stock` — tồn theo hàng hoá: gọi `AccountingStockService::detail()` **nguyên trạng**, tự
      query `in_acc_warehouse`, tự ghép `in_stock = min(khả dụng, in_acc_warehouse, in_warehouse)`
      (nhánh kho khuyến mại: `min(in_acc_warehouse, in_promotion)`)
- [x] 2.6 `productUnits` — thay `$product->data` (accessor hỏng trên `gop_db`) bằng select field cụ thể
- [x] 2.7 Route (không gắn `checkPermission`), route tĩnh khai TRƯỚC `/{id}`. ⚠️ `api.php` là CRLF —
      chèn bằng script phải giữ `

`, `git diff --stat` ra đúng **19 dòng thêm**, không phình cả file

### Kiểm chứng Phase 2 (2026-09-04)

- **Phạm vi quyền — 4 nhánh, 0 dòng DB bị sửa** (`JWTAuth::fromUser`, nhánh "quyền công ty" cấp tạm
  trong transaction rồi rollback): Super admin 309/309 · quyền tổng công ty 309/309 ·
  **quyền công ty 186/309 khớp công thức** · không quyền 2/309 (đúng số phiếu tự lập).
  → xác nhận đã bịt lỗ ERP "vào URL trần thấy phiếu mọi công ty".
- **Tồn kho khớp ERP TUYỆT ĐỐI** — chạy thẳng `ProductTransfersController::getAccountingStockDetail()`
  của ERP trên cùng `gop_db` (`DB_DATABASE=gop_db php artisan tinker`) rồi so 4 con số, cả 2 nhánh:
  · kho khuyến mại (sp 11186 / kho 4): acc 830 · wh 884 · promo 830 · **in_stock 830**
  · kho thường (sp 38464 / kho 3): acc 2144 · wh 2270 · promo 54 · **in_stock 2144** (hệ số 6)
  · kho thường (sp 7357 / kho 3): acc 331 · wh 465 · promo 139 · **in_stock 331**
- **5 endpoint smoke test qua HTTP thật** (kernel + JWT): danh sách 200 (total 309, `can_create`,
  badge `#16A34A`) · chi tiết 200 · dropdown 200 (7 kho vật lý / 3 kho kế toán) · ĐVT 200 · tồn kho 200.
- 🐛 Dính lại bẫy cũ: `$request->get()` **không đọc JSON body** → API POST `/stock` trả 422 oan.
  Đã đổi sang `input()` ([[project_laravel_request_get_khong_doc_json]]).
- 🆕 Phát hiện thêm lỗi ERP (#14, chưa có trong khảo sát): ERP trả `in_stock` theo **đơn vị cơ bản**
  nhưng FE so thẳng `qty > in_stock` với số user nhập theo **đơn vị đã chọn** → hệ số ≠ 1 là chặn sai
  (BE ERP lúc validate thì chia đúng). HRM trả thêm `in_stock_by_unit` để FE/BE so cùng đơn vị.

## Phase 3 — Backend: ghi (tạo / sửa / xoá)

- [x] 3.1 FormRequest: `status` `in:1,2` · `qty` `gt:0` (bỏ `min:1`) · kho xuất ≠ kho nhập ·
      đính kèm `mimes:pdf,png,jpg,jpeg`
- [x] 3.2 `store` / `update` — gate `canCreate()` / `canEdit()` **ở BE**, sinh mã `PDCH-`,
      `syncDetails`, upload S3
- [x] 3.3 Validate tồn: vượt tồn thì **trả 422 báo đỏ**, KHÔNG tự kẹp giá trị như ERP
- [x] 3.4 `destroy` — `canEdit()`, dọn file S3, trả JSON (ERP redirect kiểu web)
- [x] 3.5 `deleteFile`

## Phase 4 — Backend: hạch toán (phần rủi ro nhất)

- [x] 4.1 `ProductTransferAccountingService::post()` — port `updateWarehouse()`: trừ kho xuất /
      cộng kho nhập, ghi `accounting_stock_logs`, `objectable_type` = FQN ERP
      `App\Model\Warehouse\ProductTransferDetail` (để ERP đọc lại được)
- [x] 4.2 Giá vốn qua `StockValueFifoService`; **fix bug ERP**: reset `export_price` mỗi vòng,
      `qty = 0` → `0` (ERP ăn giá dòng trước)
- [x] 4.3 Bút toán Nợ 156 / Có 156 qua `AccountDetail::createDataSaveDept` + `saveAccountDetail`
- [x] 4.4 Chuyển trạng thái → *Đã hạch toán*, ghi `date_accounting`, khoá sửa/xoá
- [x] 4.5 **Đối chiếu ERP — KHỚP TUYỆT ĐỐI**, xem khối kiểm chứng dưới

### Kiểm chứng Phase 3 + 4 (2026-09-04)

**Hạch toán: chạy CÙNG 1 phiếu trên HRM và trên CODE GỐC ERP, cùng DB `gop_db`, cùng rollback.**
Script: `scratchpad/hrm_post.php` + `erp_post.php` (ERP chạy bằng `DB_DATABASE=gop_db php artisan
tinker` trong `TanPhatDev`). Ca test: sp 3998, 7 cái, kho vật lý 1, kho xuất 3 → kho nhập 5.

| So sánh | Kết quả |
|---|---|
| Tồn trước / tồn sau (`accounting_stocks` + `stocks.accounting_qty`) | **KHỚP** |
| 2 dòng `accounting_stock_logs` (qty_before/change/qty_after/type/**value_before/value_after**/objectable_type/company_id) | **KHỚP** |
| Dòng hàng (`export_price` 792.71 · `amount_export_price` 5548.97) | **KHỚP** |
| 2 dòng `account_details` (Nợ 156 / Có 156, 5548.97, `invoiceable_type` FQN ERP) | **KHỚP** |

Giá vốn FIFO chạy thật: `value_before` 52,804,592.00 − `value_after` 52,799,043.03 = 5,548.97 → chia
7 = **792.71/cái**; kho nhận nhận đúng layer 5,548.97.

⚠️ Lần chạy đầu lệch 1 cột: em tự thêm `product_id` vào dòng sổ cái (ERP để NULL). **Đã bỏ** — đó là
đổi dữ liệu kế toán ngoài phạm vi được giao, báo cáo lọc theo `account_details.product_id` sẽ đổi kết quả.

**Validate — 7 ca qua HTTP thật, rollback sạch:**

| Ca | Kết quả |
|---|---|
| Kho xuất = kho nhập | 422 "Kho xuất, kho nhập không được trùng nhau" |
| `status = 9` (ERP nhận bừa) | 422 |
| Vượt tồn | 422 **tại đúng dòng** `products.0.qty` — "…vượt quá số lượng tồn (còn 66,200)" |
| Trùng hàng hoá (ERP chỉ chặn ở FE) | 422 tại `products.1.product_id` |
| `qty = 0` | 422 "Số lượng chuyển phải lớn hơn 0" |
| `qty = 0.5` (ERP `min:1` chặn oan) | **200** — đã cho số lẻ |
| Phiếu hợp lệ | 200 |

**Vòng đời:** tạo nháp 200 → sửa 200 (qty ghi đúng) → xoá 200 (dòng hàng cascade sạch) ·
phiếu **đã hạch toán**: sửa **403**, xoá **403**.

🐛 **Dính lại bẫy `get()` vs `input()` lần thứ 2** — lần này trong `FormRequest::withValidator()`:
2 luật "kho xuất = kho nhập" và "trùng hàng hoá" **im lặng cho qua** vì `$this->get()` không đọc JSON
body. `rules()` thì không sao (Laravel validate trên `$this->all()`). Đã đổi hết sang `input()` và ghi
cảnh báo vào docblock của FormRequest.

## Phase 5 — Backend: in / xuất Excel / lịch sử

- [x] 5.1 `print-data` — mẫu in ERP **388**; `export-list-print` — mẫu **387** (qua `ErpReportTemplate`)
- [x] 5.2 Xuất Excel 1 phiếu + xuất danh sách; BE trả **đủ** field có trong `ExportFieldsModal`
      (kể cả cột đang ẩn ở danh sách)
- [x] 5.3 ~~Migration `product_transfer_history`~~ → **ĐÃ HUỶ, rollback + xoá file**. Dùng bảng CHUNG
      `catalog_histories` qua trait `LogsCatalogHistory` — **feature này KHÔNG có thay đổi schema nào**
- [x] 5.4 `ProductTransferHistoryService` — nay chỉ là **adapter mỏng** của `CatalogHistoryService`:
      khai `catalogTable`/`catalogColumns`/`catalogDisplay` + khoá ảo dạng bảng `products_rows`
- [x] 5.5 ~~Endpoint lịch sử riêng~~ → **ĐÃ GỠ**. Dùng endpoint CHUNG
      `GET /v1/catalog-histories/product_transfers/{id}` + `/filter-options`; đăng ký bảng vào
      `CatalogHistoryService::TABLES` (11 dòng, thêm mới — không sửa logic sẵn có)

### Kiểm chứng Phase 5 (2026-09-04)

- **Bản in 1 phiếu (mẫu ERP 388)**: 200, HTML 5.343 ký tự, **0 placeholder còn sót**.
  Bảng chi tiết so với `ProductTransfer::getPrintDataAttribute()` của ERP → **giống TỪNG KÝ TỰ**
  (phải bỏ `text-align: left` em thêm dư: ERP không in thuộc tính này cho ô căn trái).
  4 biến `SO_PHIEU` / `KHO_VAT_LY` / `KHO_XUAT` / `KHO_NHAP` / `GHI_CHU` đều khớp.
- **Bản in danh sách (mẫu 387)**: 200. **Xuất Excel**: 9 cột trong popup, chọn 3 cột → trả đúng 3 cột × 309 dòng.
- **Lịch sử**: tạo phiếu → 1 dòng "Tạo mới"; sửa → thêm 1 dòng, diff đúng 3 trường
  (Kho nhập · Ghi chú · **Hàng hóa điều chuyển** dạng bảng, bắt được đổi số lượng 5 → 8).
  Bộ lọc: **3 nhóm cố định** + **783 người thực hiện** (đủ nhân sự cùng công ty, không suy từ log).
- Migration chạy riêng bằng `--path` (xem trước bằng `--pretend`) để không kéo theo migration tồn
  đọng của người khác trên nhánh `gop_db`.

🆕 **Lỗi ERP thứ 15 + 16** (phát hiện khi làm bản in, chưa có trong khảo sát):
15. `{{NGUOI_LAP}}` nằm ngay dưới chữ "Người lập" trong ô ký của **cả 2 mẫu in**, nhưng
    `getPrintDataAttribute()` của ERP **không set biến này** → `clearNull()` xoá trắng, bản in ERP
    ra **ô ký trống tên**. HRM điền tên người lập.
16. `HEADER` — ERP lấy letterhead theo **người đang đăng nhập**; kế toán công ty A in phiếu công ty
    B là ra sai đầu trang. HRM lấy theo `company_id` **ghi trên chứng từ** (rule CLAUDE.md,
    khuôn `BillIncomePrintService::headerUrl()`).

### Rà lại theo skill vừa cập nhật (2026-09-04, user nhắc trước khi làm FE)

6 skill vừa đổi; 3 thay đổi **đánh trúng phần backend em vừa làm xong**, đã sửa lại:

**1. Lịch sử — em đã làm SAI hạ tầng.** Bản đầu tự dựng bảng `product_transfer_history` + service
riêng + 2 endpoint riêng. Skill `erp-to-hrm-screen` bổ sung hẳn mục **E1** trỏ sang
`entity-history/ui-base.md`, và hoá ra HRM đã có `App\Services\CatalogHistoryService` +
trait `LogsCatalogHistory` dùng chung (4 phiếu Tài chính chị em đều dùng). DTO em tự trả còn
**thiếu `actor_id` / `created_at_raw` / `action_group`** nên `SystemInfoSection` lọc không nổi.
→ Đã rollback + xoá migration, viết lại thành adapter mỏng, đăng ký bảng vào `TABLES`.
→ Kết quả sau khi sửa: log trả đủ `actor_id` · `actor_name` · `created_at_raw` · `action_group`;
  bảng con ra đúng 3 nhóm có nhãn (`added_rows` / `removed_rows` / `changed`), nhãn
  "Hàng hóa thêm mới / đã xóa / sửa thông tin"; `filter-options` 3 nhóm + 783 người.

🐛 Dính đúng bẫy skill đã ghi sẵn: gán khoá ảo `products_rows` **lên model** → `save()` ném
`Unknown column 'products_rows'` (500). Phải giữ ở **thuộc tính của service**
(`$productRowsForLog`), như `WarrantyRepairRequestService` đã cảnh báo.

**2. In danh sách phải có TRẦN 2.000 dòng** (`LimitsPrintListRows`, chốt 2026-08-24/26).
`printListData()` của em đang `->get()` không giới hạn — đúng nguyên nhân "nhiều máy in không được"
đã đo ở màn CSKH (4.980 dòng → 3,84 MB HTML → treo trình duyệt). Màn này 309 phiếu đã 350 KB.
→ Đã `use LimitsPrintListRows`, trả `template` / `total` / `limit` / `truncated`.

**3. Khoá response phải là `template`, không phải `html`** — hợp đồng của `reportPrintPreviewMixin`.
Sai tên thì popup xem trước hiện TRẮNG mà không báo lỗi gì. Đã đổi cả 2 endpoint in.
Verify: 1 phiếu → `template` 5.139 ký tự · danh sách → `total=309 limit=2000 truncated=false`.

**Ảnh hưởng Phase 6 (chưa code):** bỏ `_id/print.vue` khỏi kế hoạch — skill `print-page` §8 chốt
2026-08-22 **bản in mở bằng POPUP, không mở trang riêng** (`ReportPrintPreviewModal` +
`reportPrintPreviewMixin`); 2 màn mẫu `/print` cũ đã bị xoá. Route BE em đặt sẵn đã đúng quy ước
mixin (`{base}/{id}/print-data` · `{base}/print-list-data`), không phải sửa.
2 skill còn lại (`list-page`, `import-excel`, `info-icon-tooltip`) chỉ đổi `—` → `''`, đã theo sẵn.

## Phase 6 — Frontend

- [x] 6.1 `index.vue` — `V2BaseSmartFilterPanel` + `filterFields`, 4 mixin bắt buộc
      (`PageTitleMixin` · `CheckPermission` · `filterStateMixin` · `columnCustomizationMixin`),
      `localStorageKey`/`columnScreenKey` duy nhất, sort mặc định ngày tạo giảm dần
- [x] 6.2 Cột: STT · Số phiếu (`<nuxt-link>`) · Ngày hạch toán · Kho vật lý · Kho xuất · Kho nhập ·
      Người lập · Ngày lập · Trạng thái (`<V2BaseBadge :color="item.status_color">{{ item.status_text }}`
      — KHÔNG map số→chữ, KHÔNG tự chọn màu ở FE) · Hành động
- [x] 6.3 `V2BaseRowActions` — ⚠️ emit **CHUỖI key**, handler `switch (action)`; nút không dùng được
      thì **ẩn** (`visible`), không xám
- [x] 6.4 `ProductTransferForm.vue` — kho vật lý → kho xuất/nhập (đổi kho vật lý xoá sạch lựa chọn
      dưới), ghi chú, đính kèm, bảng chi tiết + popup tìm hàng dùng chung.
      **Chỉ dùng `V2Base*`, cấm HTML thô**: `V2BaseSelect`/`V2BaseInput`/`V2BaseLabel`/`V2BaseButton`;
      đính kèm dùng `V2BaseFile`; khối nhóm dùng `V2BaseFormSection`; bảng tràn ngang bọc
      `V2BaseTableScroll`. Tự kiểm bằng lệnh grep ở CLAUDE.md mục V2Base
- [x] 6.5 Vượt tồn: viền đỏ + báo lỗi dưới ô, **không tự sửa số**; `unsavedChangesMixin` +
      `markFormSaved()`
- [x] 6.6 `_id/index.vue` (chi tiết, có mục *Lịch sử* bằng `SystemInfoSection`) · `_id/edit.vue` ·
      `create.vue`; nút trong `V2Footer`. **KHÔNG dựng `_id/print.vue`** — bản in mở bằng POPUP
      `ReportPrintPreviewModal` + `reportPrintPreviewMixin` (print-page §8, chốt 2026-08-22)
- [x] 6.7 Lịch sử **đủ 2 nơi**: popup ở màn danh sách + khối ở màn chi tiết. Dùng
      `components/modal/CatalogHistoryModal.vue` (bọc chính `SystemInfoSection`, 76 dòng) với
      `endpoint-base="catalog-histories"`, `entity-type="product_transfers"` — KHÔNG chép
      `CustomerHistoryModal.vue` (bản viết tay có trước) và KHÔNG tự dựng timeline
- [x] 6.8 Xuất Excel qua `ExportFieldsModal`, tự gắn token `Authorization`. Đo thời gian: > 2s thì đổi
      sang `GET /export-rows` phân trang + dựng file ở FE bằng `utils/export/listExportFile.js`
      (CLAUDE.md mục hiệu năng), không để `DynamicExport` chạy đồng bộ
- [x] 6.9 Gắn link vào mục menu `Điều chuyển > Phiếu điều chuyển hàng` (đang là placeholder)

### Kiểm chứng Phase 6 (2026-09-04)

**5 file FE mới** (`pages/finance/product-transfers/`): `index.vue` · `create.vue` · `_id/index.vue`
· `_id/edit.vue` · `components/ProductTransferForm.vue`; + gắn link mục menu.

- Cú pháp `.vue` verify bằng `vue-template-compiler` (repo không có eslint) — **5/5 OK**.
- **9 lệnh grep tự kiểm của skill đều SẠCH**: `status-pill` · `interactable:` · `action.key ===` ·
  `V2BaseFilterPanel` · `advanced-filters` · dấu `—` còn sót · `log.action !==` ·
  `toLocaleString('vi-VN')` cho số · HTML thô thay vì `V2Base*`.
- Menu: nạp thật `financeItems` → *Điều chuyển* có **1** mục trỏ `/finance/product-transfers`,
  và vẫn đúng **1** mục trỏ `/finance/product-transfer-requests` ở nhóm Xuất hàng (không trùng).

🐛 **3 lỗi tự bắt được trước khi chạy trình duyệt** — cả 3 đều thuộc loại "hỏng im lặng":

1. `apiPostMethod` nhận `{ url, **payload** }` chứ không phải `{ url, data }`. Đặt sai tên khoá thì
   body gửi đi là `undefined` — BE nhận rỗng mà **không báo lỗi gì**. Dính 2 chỗ (lấy tồn + lưu phiếu).
2. **Vuex `dispatch` chỉ chuyển 1 payload**, tham số thứ 3 không tới action → `apiDeleteMethod`
   không bao giờ nhận `options`, và axios bản cũ cũng không gửi `config.data` cho DELETE.
   → `file_url` phải đi qua **QUERY param** (đúng tiền lệ đã ghi trong màn Phiếu yêu cầu chuyển hàng).
   Verify BE: xoá file có thật → 200 (chuỗi `attachments` còn đúng file kia) · file không thuộc
   phiếu → 404 · phiếu đã hạch toán → 403.
3. `V2BaseInput` **không có prop `tooltip`** — icon ⓘ của ô khoá phải đặt trên `V2BaseLabel :hint`.

**2 quyết định UI cần anh xác nhận (skill thắng spec):**
- Nút hạch toán: ERP đặt tên **"Duyệt"**; `V2Footer` chuẩn không có nhãn này cho hành vi lưu-rồi-duyệt
  nên dùng **"Lưu và duyệt"** (`save_and_approve`, có popup xác nhận trước khi ghi sổ).
- Nút "Thêm hàng hóa" khi chưa chọn đủ 3 kho: **ẩn hẳn** (rule "không dùng được thì ẩn"), thay bằng
  một dòng hướng dẫn xám trong khối để user biết vì sao.

## Phase 7 — Nghiệm thu

- [x] 7.1 Chạy checklist A→H của skill `erp-to-hrm-screen`
- [x] 7.2 Grep tự kiểm: `status-pill` · `interactable:` · `action.key ===` · `V2BaseFilterPanel` ·
      `advanced-filters` · câu toast tự chế · `—` còn sót
- [x] 7.3 **Bấm thật từng ô lọc** (chờ ≥3s mỗi lần — [[feedback_playwright_cho_3s_khi_test_bo_loc]])
      và **từng nút** trong cột Hành động, kể cả trong menu "…"
- [x] 7.4 Test phân quyền bằng `JWTAuth::fromUser` — đủ nhánh: tổng công ty / công ty / không quyền /
      không phải người lập ([[reference_test_phan_quyen_bang_jwt_fromuser]])
- [x] 7.5 Đối chiếu ngược ERP (bước 5 của skill): đủ cột · đủ ô lọc · đủ hành động **và điều kiện ẩn/hiện**

### Nghiệm thu trên trình duyệt (2026-09-04)

Dev server tự dựng **cổng riêng**: API `127.0.0.1:8001` + Nuxt `127.0.0.1:3000`
(⚠️ cổng 8000 đang phục vụ project khác `D:\CompanyProject\hrm-cursor` — KHÔNG đụng vào).
Đăng nhập bằng cách nạp JWT (`JWTAuth::fromUser`) vào `localStorage.access_token`, không cần mật khẩu.

**9/9 ô lọc khớp SQL 100%** (chờ ≥3s mỗi lần đổi):

| Ô lọc | UI | SQL |
|---|---|---|
| Mã phiếu `PDCH-0104` | 4 | 4 |
| Kho vật lý `CSKH` | 0 | 0 |
| Kho xuất `HN-NXT` | 0 | 0 |
| Trạng thái *Đang tạo* / *Đã hạch toán* | 0 / 309 | 0 / 309 |
| Mã hàng hoá `TATE` | 0 | 0 |
| Tên hàng hoá `Áo mưa` | 11 | 11 |
| Ngày lập từ 01/07/2026 | 12 | 12 |
| Ngày hạch toán đến 31/12/2025 | 146 | 146 |
| Sau khi bấm **Làm mới** | 309 | 309 |

**Bấm thật các nút:** In phiếu (popup xem trước, có bảng chi tiết, **tên người lập đã hiện** — lỗi ERP
#15 đã vá) · Lịch sử (popup + 6 ô lọc) · menu **"Hành động khác"** (In phiếu / Lịch sử) · Sửa · Xóa
(popup xác nhận → xoá thật). Phiếu *Đã hạch toán* chỉ còn In + Lịch sử, **Sửa/Xóa ẩn hẳn** — đúng rule.
Badge *Đang tạo* ra **xám `rgb(100,116,139)`** đúng chuẩn (ERP để đỏ).

**Vòng đời đầy đủ trên UI:** chọn kho vật lý → 2 ô kho kế toán mở ra đúng 3 kho của kho đó → thêm hàng
(tự nạp ĐVT + **SL tồn 66.200 khớp SQL**) → nhập 999.999 → **báo đỏ ngay dưới ô** "…vượt quá số lượng
tồn (còn 66,200)", **số user gõ giữ nguyên**, không điều hướng → sửa còn 3 → Lưu → về danh sách, phiếu
`PDCH-01060` đứng đầu → Sửa (nạp lại đúng dữ liệu cũ) đổi SL 3→7 → Lưu → lịch sử ghi đúng 2 dòng
(`create` + `update` chỉ chứa trường đổi) → Xóa → tổng về 309.

**DB sạch sau nghiệm thu:** 309 phiếu như trước, 0 dòng hàng mồ côi, **0 bút toán / 0 log tồn kho phát
sinh** (chỉ dùng nút *Lưu*, không bấm *Lưu và duyệt*), log lịch sử của phiếu test đã dọn.

🐛 **4 lỗi tự bắt được khi bấm thật** — cả 4 đều KHÔNG báo lỗi gì trên màn:

1. **2 ô lọc Kho xuất / Kho nhập rỗng** — endpoint chỉ trả kho kế toán khi có `warehouse_id`, mà màn
   danh sách không truyền. Đúng loại "ô lọc chết" skill cảnh báo. → thêm
   `ProductTransferService::accWarehouseFilterOptions()` (mọi kho của công ty).
2. **`V2BaseError` dùng prop `message`, không phải `error`** → lỗi 422 về đúng nhưng **không hiện dưới
   ô**. Sai 8 chỗ.
3. **`base-confirm-modal` chỉ emit `event` KHI ĐÃ XÁC NHẬN**, payload là chuỗi lý do (rỗng) chứ không
   phải cờ `true/false` → `if (!accepted) return` chặn luôn: **bấm Xóa xong không có gì xảy ra**.
   Sai 3 chỗ (danh sách, chi tiết, form).
4. (đã ghi ở Phase 6) `apiPostMethod` dùng khoá `payload`; `dispatch` không chuyển tham số thứ 3.

- [ ] 7.6 Tài liệu test case cho QA (skill `testcase-documenter`) — ghi rõ các điểm **cố ý khác ERP**
      để QA không báo nhầm lỗi

---

## Checkpoint — 2026-09-04

**Vừa hoàn thành:** khảo sát ERP đầy đủ (`khao-sat.md`); phát hiện + sửa xong lỗi nhãn menu gán nhầm
màn *Phiếu yêu cầu chuyển hàng* vào mục *Phiếu điều chuyển hàng* (Task 0.2); tách nhánh riêng
`feat/finance-product-transfer` từ `gop_db` cho cả 2 repo; chốt 5 quyết định với user; viết
`design.md` + `plan.md`.

**Đang làm dở:** chưa có dòng code nghiệp vụ nào.

**Bước tiếp theo:** Task 0.4 (spec) → Phase 1 (tách FIFO + test hồi quy màn Phiếu xuất hàng).

**Blocked:**

- Task 0.3 chờ user duyệt sửa skill `erp-to-hrm-screen` (tài sản chung, repo `hrm-claude-config`).
- §5 design: 4 câu trả lời cho skill `entity-history` đang là **đề xuất của em**, chờ user xác nhận
  (nhất là: track những trường nào, và có cần ghi log khi xoá phiếu không).
