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
