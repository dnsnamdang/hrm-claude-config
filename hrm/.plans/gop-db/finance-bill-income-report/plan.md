# Plan — Phiếu báo có (ERP → HRM)

> Phụ trách: @khoipv · Nhánh: `gop_db` (cả 2 repo) · Tạo: 2026-08-24
> Design: `design.md` · Spec: `docs/superpowers/specs/gop-db/2026-08-24-finance-bill-income-report-design.md`
> **Trạng thái: HOÀN THÀNH — user xác nhận xong (2026-08-24).**

---

## Phase 0 — Khảo sát & chốt yêu cầu

- [x] Khảo sát màn ERP gốc (routes, controller, model, blade, JS class, import job, export Excel)
- [x] Đo dữ liệu thật trên `gop_db` (3.832 phiếu / 10.199 dòng chi tiết / phân bố loại thu)
- [x] Brainstorming — user chốt 4 quyết định lớn
- [x] Viết spec chi tiết + design tóm tắt + plan

## Phase 1 — Backend: nền tảng + CRUD

- [x] Entity `BillIncomeReport` (`Modules/Finance/Entities/BillIncomeReport/`) — hằng trạng thái,
      loại thu, tên quyền, hook `creating` gán đơn vị tổ chức, `applyScope`, `canView/canEdit/canDelete`
- [x] Entity `BillIncomeReportDetail` — quan hệ `parent`, `customer`, `supplier`, `objectable` (morph),
      `productExport`, `exportRequestable`
- [x] Sinh mã `{CTY}.PBC{mmyy}.{5 số}` có `lockForUpdate` (đặt trong Entity, không tách service riêng)
- [x] `BillIncomeReportService` — danh sách + lọc + phân trang + sắp xếp
- [x] `BillIncomeReportWriteService` — tạo / sửa / xóa / đồng bộ dòng chi tiết
- [x] `BillIncomeReportAccountingService` — `buildEntries()` thuần + `persist()` idempotent
- [x] Request `BillIncomeReportStoreRequest` (+ rethrow `ValidationException`)
- [x] Transformer: `BillIncomeReportListResource`, `BillIncomeReportDetailResource`
- [x] Controller `BillIncomeReportController` + routes (`Modules/Finance/Routes/api.php`)
- [x] 3 quyền vào `PermissionsTableSeeder` (guard `api`, tên trùng ERP)
- [x] Seeder dữ liệu test (phiếu *Đang tạo*, đủ 3 loại thu)

## Phase 2 — Backend: tra cứu & màn phụ

- [x] `GET /accounts`, `GET /banks` (ngân hàng + số TK công ty)
- [x] ~~`GET /search-contracts` riêng~~ → dùng lại endpoint sẵn có `/bill-income-requests/search-contracts`
      (đã lấy nguồn `hrm_contracts`) + `/search-suppliers`, đúng nguyên tắc không dựng lại popup đã có
- [x] `GET /search-product-exports` — phiếu xuất hàng theo NCC
- [x] `GET /search-export-requests` — phiếu YCXH theo hợp đồng
- [x] `POST /{id}/approve` — duyệt + ghi sổ cái
- [x] `POST /{id}/details/{detailId}/not-report-money`
- [x] `BillIncomeReportSummarizeService` — màn Tổng hợp tiền về ngân hàng (lọc TK 1311/1312/3311,
      phiếu Đã duyệt, `is_not_report_money = 0`, theo công ty)
- [x] Xuất Excel màn tổng hợp (class `*Export` + blade `exports/`, theo skill `export-excel`)

## Phase 3 — Backend: Import Excel + Lịch sử

- [x] Import Excel sao kê — validate từng dòng, tạo phiếu + dòng chi tiết + ghi sổ, trả kết quả đồng bộ
- [x] File mẫu import
- [x] ~~Bảng lịch sử riêng~~ → dùng bảng CHUNG `catalog_histories` + trait `LogsCatalogHistory`
      như 3 phiếu tài chính đã port ⇒ **feature không có thay đổi schema nào** (migration đã rollback + xóa)
- [x] `BillIncomeReportHistoryService` (trait `LogsCatalogHistory`, khoá ảo `details_rows` dạng BẢNG)
      + khai `bill_income_reports` vào whitelist `CatalogHistoryService::TABLES`; đọc qua endpoint chung
      `catalog-histories/bill_income_reports/{id}`

## Phase 4 — Frontend: danh sách + form + chi tiết

- [x] Menu `components/subsystem-menu/finance.js` — 2 mục
- [x] `pages/finance/bill-income-reports/index.vue` — 4 mixin, `V2BaseSmartFilterPanel`, cấu hình cột
- [x] `components/BillIncomeReportForm.vue` + `BillIncomeReportDetailTable.vue`
- [x] Popup chọn: khách hàng · NCC · hợp đồng · phiếu xuất hàng · phiếu YCXH (ưu tiên dùng lại popup có sẵn)
- [x] `create.vue` + `_id/edit.vue` — `unsavedChangesMixin`, nút Lưu / Lưu và duyệt
- [x] `_id/index.vue` — chi tiết + cờ "Không báo tiền về" + nút sang Điều chỉnh công nợ + Lịch sử

## Phase 5 — Frontend: Tổng hợp tiền + Import

- [x] `summarize-money.vue` — bảng + tick chọn (chặn 2 phiếu khác nhau) + sang màn Điều chỉnh công nợ
- [x] Xuất Excel qua `ExportFieldsModal`
- [x] `ImportBillIncomeReportModal.vue` (`V2BaseImportModal` + file mẫu)

## Phase 6 — Đối chiếu & nghiệm thu

- [x] Đối chiếu ngược với ERP: đủ cột / đủ ô lọc / đủ hành động + điều kiện ẩn hiện
- [x] Chạy checklist `.claude/skills/erp-to-hrm-screen/SKILL.md` (A→H) + grep tự kiểm
- [x] Đối chiếu `buildEntries()` với bút toán ERP thật — 7 phiếu / 38 bút toán / 24 cột: **khớp 100%**
- [x] Smoke test endpoint qua HTTP kernel trong tinker
- [x] Compile FE (vue-template-compiler + babel) — 9/9 file sạch
- [ ] **Bấm thật trên trình duyệt (user thực hiện)** — phần CHƯA kiểm chứng, xem checkpoint

## Phase 7 — Chỉnh UI bảng Chi tiết (user yêu cầu 2026-08-24)

- [x] Bảng Chi tiết trong `BillIncomeReportForm.vue`: đổi `<th style="width:">` → `min-width`
      để bảng tràn ngang thật → `V2BaseTableScroll` hiện đủ thanh cuộn TRÊN + DƯỚI
      (khuôn: `pages/customer-care/warranty-repair-requests/.../WarrantyRepairRequestForm.vue`)
- [x] Giãn cột: Khách hàng 200→240 · Tên KH 180→220 · Số đơn hàng/HĐ 210→280 · Số tiền 160→190 · Diễn giải 220→320
- [x] Compile lại file FE (vue-template-compiler + babel: sạch)

## Phase 8 — Sửa theo phản hồi user (2026-08-28) — chỉ MÀN DANH SÁCH

- [x] BE `BillIncomeReportService::searchByFilter()`: eager load thêm `employeeUpdate.info`
- [x] BE `BillIncomeReportListResource`: trả thêm `updated_by_name`
- [x] FE `index.vue`: đổi tiêu đề cột `createdAt` "Ngày lập" → "Ngày tạo"
- [x] FE `index.vue`: đổi tiêu đề cột `createdByName` "Người lập" → "Người tạo"
- [x] FE `index.vue`: đổi nhãn + placeholder ô lọc `created_by` → "Người tạo"
- [x] FE `index.vue`: đổi nhãn nhóm lọc `created_range` → "Khoảng ngày tạo" + 2 ô "Ngày tạo từ/đến"
- [x] FE `index.vue`: thêm cột `updatedByName` "Người cập nhật" (mặc định ẩn) + template cell
- [x] FE `index.vue`: giữ cột `updatedAt` "Ngày cập nhật" mặc định ẩn (đã có, xác nhận hiện trong popup Cấu hình cột)
- [x] FE `index.vue`: đổi "Diễn giải" → "Ghi chú" (tiêu đề cột `note` + nhãn/placeholder ô lọc)
- [x] FE `summarize-money.vue`: đổi "Diễn giải" → "Ghi chú" (cột + ô lọc) cho đồng bộ
- [x] Compile lại FE (vue-template-compiler + babel)
- [x] Smoke test API danh sách: `updated_by_name` trả đúng

> Phạm vi user chốt 2026-08-28: "Ngày tạo/Người tạo" CHỈ áp màn danh sách Phiếu báo có —
> `summarize-money.vue`, form Tạo/Sửa và popup chọn Phiếu xuất kho GIỮ NGUYÊN "Người lập"/"Ngày lập".

### Checkpoint — 2026-08-28
Vừa hoàn thành: **Phase 8 — sửa 3 phản hồi của user trên MÀN DANH SÁCH Phiếu báo có.**

BE (2 file sửa): `BillIncomeReportService` eager load thêm `employeeUpdate.info` ·
`BillIncomeReportListResource` trả thêm `updated_by_name`.
FE (2 file sửa): `index.vue` — "Ngày lập"→"Ngày tạo", "Người lập"→"Người tạo" (cột + ô lọc +
nhóm khoảng ngày + placeholder), "Diễn giải"→"Ghi chú" (cột + ô lọc), thêm cột `updatedByName`
"Người cập nhật" (mặc định ẩn) + template cell · `summarize-money.vue` — đổi "Diễn giải"→"Ghi chú"
(cột + ô lọc), GIỮ "Người lập" theo phạm vi user chốt.

Kiểm chứng đã chạy:
- Compile 2 file FE (vue-template-compiler + babel): sạch.
- `php -l` 2 file BE: sạch.
- Tinker: Resource trả `updated_by_name` đúng tên nhân viên trên 3 phiếu mẫu.
- SQL trên 3.831 phiếu thật: `updated_by` 0 dòng null/0/mồ côi, 0 dòng thiếu `fullname`
  ⇒ cột "Người cập nhật" luôn có dữ liệu, không ra "—".

Đang làm dở: —
Bước tiếp theo: **user bấm thật trên trình duyệt** — kiểm 3 điểm: nhãn cột/ô lọc đã đổi;
popup Cấu hình cột có đủ "Ngày cập nhật" + "Người cập nhật" (tick lên thì bảng hiện đúng);
ô lọc "Ghi chú" gõ chữ lọc ra đúng phiếu.
Blocked:

---

### Checkpoint — 2026-08-24 (2)
Vừa hoàn thành: **toàn bộ BE + FE của feature.**

BE (13 file): 3 entity + lớp quyền thuần · 7 service (danh sách / ghi / ghi sổ cái / tra cứu /
tổng hợp / import / lịch sử) · Request · 2 Resource · Controller + **17 route** · Export Excel +
blade · Seeder dữ liệu test · 3 quyền (seeder + DB dev) · morphMap · whitelist catalog history.
**Không có migration nào** — lịch sử dùng bảng chung `catalog_histories`.

FE (9 file): `index.vue` (13 cột, 12 ô lọc, popup lịch sử, import) · `create.vue` · `_id/edit.vue` ·
`_id/index.vue` (chi tiết + cờ "Không báo tiền về" + khối Lịch sử + cửa sang Điều chỉnh công nợ) ·
`summarize-money.vue` (tick chọn + xuất Excel chọn trường) · `BillIncomeReportForm.vue` ·
2 popup mới (phiếu xuất / phiếu YCXH) · modal Import · 2 mục menu.

Kiểm chứng đã chạy:
- **Ghi sổ cái khớp 100% với ERP**: 7 phiếu thật / 38 bút toán / 24 cột denormalize + số refs.
- 11 endpoint GET trả 200; luồng ghi tạo → sửa → duyệt (cân Nợ = Có) → 423 khi sửa/xóa phiếu đã
  duyệt → 403 khi duyệt lại → cờ "Không báo tiền về" → 4 dòng lịch sử đúng subset-diff.
- Import Excel: validate bắt đủ 5 lỗi/dòng sai, 2 dòng hợp lệ tạo phiếu + ghi sổ cân đối;
  `parseDate` chặn được ngày không tồn tại (31/02) và serial Excel; `toNumber` đọc đúng
  "1.500.000" / "1,234.56".
- File Excel tổng hợp: **0 ô chuỗi-nhìn-như-số**, tiền kiểu `n` + `#,##0`, 1 drawing letterhead,
  bề rộng cột đúng.
- Compile FE 9/9 file sạch; grep tự kiểm theo skill erp-to-hrm-screen: sạch toàn bộ.
- Mọi dữ liệu test đã DỌN SẠCH (0 phiếu, 0 bút toán, 0 dòng lịch sử còn sót).

Đang làm dở: —
Bước tiếp theo: **user bấm thật trên trình duyệt** (phần chưa kiểm chứng: bố cục thật của form
3 loại thu, 5 popup chọn đối tượng, luồng import qua UI, xuất Excel qua UI). Dữ liệu để bấm thử:
chạy `php artisan db:seed --class="Modules\Finance\Database\Seeders\BillIncomeReportTestDataSeeder"`
(đã chạy sẵn — 3 phiếu `TEST.PBC.*` trạng thái Đang tạo).
Blocked:

### Checkpoint — 2026-08-24 (1)
Vừa hoàn thành: Phase 0 + Phase 1 + phần lớn Phase 2 + phần lịch sử của Phase 3.
BE đã có: 4 entity, 5 service, Request, 2 Resource, Controller + 15 route, 3 quyền (seeder + DB dev),
morphMap `BillIncomeReport`, bảng `bill_income_report_history` (đã migrate).
Kiểm chứng đã chạy:
  - 7 endpoint GET trả 200 qua HTTP kernel.
  - **Ghi sổ cái: 7/7 phiếu thật (38 bút toán) khớp 100% với bút toán ERP đã ghi** — so 24 cột
    denormalize + số `account_detail_refs`. Khác biệt duy nhất là định dạng `invoiceable_date_accounting`
    (`Y-m-d` vs cột datetime `Y-m-d 00:00:00`) — không phải lệch dữ liệu.
  - Luồng ghi: tạo nháp -> sửa -> duyệt (cân Nợ = Có = 2.500) -> sửa/xóa phiếu đã duyệt trả 423 ->
    duyệt lại trả 403 -> cờ "Không báo tiền về" -> 4 dòng lịch sử đúng subset-diff. Đã DỌN SẠCH
    dữ liệu test (0 phiếu, 0 bút toán, 0 dòng lịch sử còn sót).
Đang làm dở: chưa làm màn Tổng hợp tiền về ngân hàng + xuất Excel + import Excel + toàn bộ FE.
Bước tiếp theo: `BillIncomeReportSummarizeService` + xuất Excel (skill export-excel).
Blocked:

## Phase F — Tinh chỉnh hiển thị bảng chi tiết (2026-09-03)

- [x] FE `BillIncomeReportForm.vue`: cột **Số tài khoản có** chỉ hiện số hiệu (bỏ phần " - tên")
      → thêm computed `accountNumberOptions` map từ `identify_number`
- [x] FE `BillIncomeReportForm.vue`: cột **Tên tài khoản** chỉ hiện tên (bỏ số hiệu)
      → `loadAccounts()` giữ thêm `account_name` (tên thuần từ BE), `accountName()` trả `account_name`
- [x] Giữ nguyên select **Tài khoản nợ** ở phần đầu phiếu (vẫn "số - tên", vì không có cột tên đi kèm)
- [x] Compile FE sạch (vue-template-compiler + babel)
- [x] FE component DÙNG CHUNG `components/modal/base-confirm-modal.vue`: nút xác nhận tự ra ĐỎ
      khi `text-accept` bắt đầu bằng "Xóa"/"Xoá" (trừ "Xóa trắng") — sửa 1 chỗ, đúng cho cả
      ~101 popup xóa đang thiếu `danger` trên toàn hệ thống. Prop `danger` đổi mặc định
      `false` → `null` (= chưa chỉ định) nên màn nào truyền thẳng vẫn được tôn trọng.
      User chốt sửa ở component chung thay vì vá từng màn (2026-09-03).
- [x] BE `BillIncomeReportStoreRequest`: cột **Số tiền** ở bảng chi tiết không bao giờ báo lỗi
      bắt buộc — rule cũ `required|numeric|min:0` mà FE quy ô rỗng thành `0`, Laravel coi `0` là
      "có nhập" nên `required` luôn qua. Đổi thành `required|numeric|gt:0` + message
      "Số tiền phải lớn hơn 0". Khớp với luồng import (đã chặn `money <= 0`) và dữ liệu thật
      (10.207 dòng, 0 dòng `money = 0`). FE không phải sửa — đã nối sẵn
      `hasFieldError('details.N.money')` + `V2BaseError`.
- [x] FE `BillIncomeReportForm.vue` (dùng chung cho cả Chi tiết / Sửa): mở phiếu đã bị xóa ở
      tab khác -> BE trả **404** (`findOrFail` + `Handler::render`), toast đổi thành
      **"Không tìm thấy dữ liệu"**. Lỗi khác (mạng / 500) giữ câu cũ "Không tải được phiếu báo có".
- [x] BE file mẫu import (`BillIncomeReportController::importTemplate()` +
      `BillIncomeReportImportService::COLUMNS` / `templateSampleRow()`): dựng lại cho gọn —
      kẻ viền cả bảng, tiêu đề nền teal `#1ABC9C` chữ trắng đậm căn giữa, bề rộng cột theo
      từng cột (22 đều → 12-42), canh ô theo kiểu dữ liệu, ô Số tiền là **số thật**
      `#,##0`, ngày ví dụ đổi sang **dd/mm/yyyy**.
      Ô ngày + mã NH + số TK giữ kiểu CHUỖI: FE đọc file bằng `XLSX.read()` không bật
      `cellDates` nên ô ngày thật sẽ ra serial `46264`, còn số TK kiểu số ra `1.16E+11`.
- [x] FE `_id/index.vue`: nút **Duyệt** ở màn chi tiết đang `primary status="success"`
      (xanh lá `#16a34a`) → bỏ `status`, về teal `#1abc9c` đúng skill `button-convention`
      mục 2b (nhóm Duyệt cùng tông với V2Footer). 2 nút màu khác trong feature đã kiểm:
      Import (secondary warning) + Xuất Excel (secondary success) đều đúng skill.
- [x] FE điều hướng: từ Chi tiết phiếu báo có bấm "Tạo phiếu yêu cầu điều chỉnh công nợ" thì
      nút **Quay lại** ở màn tạo mới phải về lại đúng phiếu báo có (trước đây luôn về danh sách
      phiếu điều chỉnh công nợ). Cách làm: `_id/index.vue` mang thêm `?back_url=` (theo tên tham số
      đã có sẵn ở màn Training), `BillAdjustDeptRequestForm.vue` đổi `url-back` cứng thành computed
      `backUrl` — chỉ nhận path nội bộ (`/`, không `//`), còn lại về danh sách như cũ.
      Không dùng `$router.go(-1)`: mở link ở tab mới thì lịch sử trắng, `V2Footer` sẽ đá về trang chủ.
- [x] FE `BillIncomeReportForm.vue`: nút thứ 2 của form đang hiện **"Lưu và gửi duyệt"** trong khi
      việc thật là DUYỆT LUÔN + ghi bút toán sổ cái. Nguyên nhân: `footerMenu` khai cờ
      `save_and_submit_approve`, `V2Footer` gắn nhãn theo cờ. Đổi sang `save_and_approve`
      (+ listener `@saveAndApprove`) → nhãn "Lưu và duyệt", popup "Xác nhận lưu và duyệt",
      khớp ERP `bill_income_reports/create.blade.php:26`.
- [x] Ô **Diễn giải đầu phiếu** (`form.note`) thiếu chỗ hiện lỗi: FE không có `:invalid` cũng
      không có `<V2BaseError>` nên rule `note => nullable|max:255` (đã có sẵn ở BE) chỉ ra toast
      chung. Thêm `:invalid` + `V2BaseError`, và bổ sung message tiếng Việt `note.max` =
      "Tối đa 255 ký tự" (trước đó rơi về câu mặc định tiếng Anh của Laravel).
      Ô Diễn giải trong BẢNG CHI TIẾT là cột khác (`bill_income_report_details.note`, kiểu TEXT)
      — đã có sẵn lỗi inline.
- [x] **Nới trần Diễn giải lên 500 ký tự cho CẢ 2 ô** (user chốt 2026-09-03):
      migration `2026_09_03_000001_widen_note_on_bill_income_reports_table` đổi
      `bill_income_reports.note` từ `varchar(255)` → `varchar(500)` (đã chạy, 0 dòng bị ảnh hưởng —
      dài nhất đang là 128); rule `note => nullable|max:500` và `details.*.note => required|max:500`
      + message "Tối đa 500 ký tự". Cột chi tiết là TEXT nên không cần migration.
      ERP không có rule độ dài nào cho 2 trường này — 255 cũ chỉ là bề rộng cột ERP để lại.
- [ ] User mở trình duyệt xác nhận hiển thị 2 cột + màu nút Xóa (kiểm cả vài màn khác
      dùng chung popup: Khóa/Mở khóa/Duyệt phải KHÔNG đổi màu) + lỗi inline cột Số tiền

### Checkpoint — 2026-09-03 (đợt sửa lỗi Phase F)
Vừa hoàn thành: 9 việc trong Phase F — 2 việc hiển thị (tách cột số/tên tài khoản; nút Duyệt về teal),
3 việc validate (Số tiền `gt:0`; Diễn giải hiện lỗi inline; nới trần 2 ô Diễn giải lên 500 + migration),
2 việc chữ/thông báo (nút "Lưu và duyệt" thay "Lưu và gửi duyệt"; toast 404 "Không tìm thấy dữ liệu"),
1 việc file mẫu import (viền + tiêu đề teal + bề rộng cột + ngày dd/mm/yyyy + ô tiền kiểu số),
1 việc điều hướng (`?back_url=` để nút Quay lại của màn Điều chỉnh công nợ về đúng phiếu báo có).
Kèm 1 sửa **component dùng chung** `base-confirm-modal.vue` (nút xác nhận tự đỏ khi `text-accept`
là "Xóa") — ảnh hưởng ~101 popup xóa toàn hệ thống, xem mục cảnh báo ở STATUS.
Đã kiểm chứng: `php -l` + compile SFC toàn bộ file đụng tới · chạy thật validator ở mốc biên
(0/''/null/-5/1.5tr cho Số tiền; 255/500/501 cho Diễn giải) · chạy thật `isDanger()` trên toàn bộ chữ
`text-accept` đang có trong code · dựng file mẫu import thật rồi đọc lại bằng PhpSpreadsheet (kiểu ô,
mã định dạng, bề rộng, chiều cao) và cho dòng ví dụ chạy qua `validateRows()` (1 hợp lệ / 0 lỗi) ·
migration đã chạy, `note` = `varchar(500)`, 0 dòng bị ảnh hưởng.
Đang làm dở: —
Bước tiếp theo: **user mở trình duyệt xác nhận** — 2 cột tài khoản ở bảng chi tiết · màu nút Xóa trong
popup (và kiểm vài màn khác: Khóa/Mở khóa/Duyệt phải KHÔNG đổi màu) · lỗi inline cột Số tiền và 2 ô
Diễn giải · nhãn nút "Lưu và duyệt" · file mẫu import · luồng Quay lại từ màn Điều chỉnh công nợ.
Blocked:
