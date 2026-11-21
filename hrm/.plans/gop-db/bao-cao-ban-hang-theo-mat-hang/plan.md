# Plan — Báo cáo bán hàng theo từng mặt hàng

> @khoipv · nhánh `develop` (hrm-api + hrm-client) · spec `docs/superpowers/specs/gop-db/2026-11-13-bao-cao-ban-hang-theo-mat-hang-design.md`

## Phase 1 — Port màn

### BE (hrm-api)
- [x] T1 Catalog quyền: thêm `hrm` vào platforms mã `accounting.bao_cao_ban_hang_theo_mat_hang.view`
- [x] T2 `SaleByProductReportService`: phạm vi 5 mức, union 3 nhánh (+ HĐ HRM), gộp theo hàng, tồn đầu/cuối batch, filter-options, item-list (NVKD + lọc)
- [x] T3 `SaleByProductReportPrintService` + blade in + Excel (bảng chính + popup)
- [x] T4 Controller + route `/v1/finance/sale-by-product-report`
- [x] T5 Smoke test HTTP kernel (tinker) — đối chiếu tổng với ERP query gốc trên cùng kỳ

### FE (hrm-client)
- [x] T6 `pages/sale/sale-by-product-report/index.vue` (bộ lọc floating, kỳ, In/Excel)
- [x] T7 `components/SaleByProductSummary.vue` + `SaleByProductTable.vue`
- [x] T8 `components/SaleByProductDetailModal.vue` (popup: lọc, NVKD, In, Excel)
- [x] T9 Menu `sale-hub.js` → link + codes
- [x] T10 Parse template + babel; báo user phần chưa kiểm trình duyệt

### Kết quả verify (13/11/2026)
- BE: `php -l` sạch; HTTP kernel 7 endpoint 200 (`/`, `filter-options`, `item-list`, `print-list-data`, `item-list/print-list-data`,
  `export`, `item-list/export`), kỳ sai → 422. Ép 5 mức phạm vi + từng bộ lọc (tháng 6/2026): không lỗi SQL; Xuất bán 189.741 +
  KM 4.115 = tổng 193.856 SL thực tế; Excel mở được, `data-format` từng ô.
- FE: parse template + babel 4 file + `sale-hub.js` OK. CHƯA mở trình duyệt (user tự test).
- HĐ HRM: local 0 phiếu xuất kho loại 21 → nhánh HĐ HRM mới kiểm bằng SQL, chưa có số thật.
- Deploy: chạy `php artisan permission:catalog-sync` (bật platform hrm cho mã `accounting.bao_cao_ban_hang_theo_mat_hang.view`).

### Checkpoint — 2026-11-13
Vừa hoàn thành: T1–T10 (BE + FE + menu), code CHƯA commit (hrm-api + hrm-client nhánh develop)
Đang làm dở: —
Bước tiếp theo: user mở `/sale/sale-by-product-report` trên trình duyệt (tài khoản có mã quyền 4 mức) — bấm Mã hàng mở popup, lọc popup, In / Excel 2 nơi
Blocked:

### T11 — Test Playwright trình duyệt thật (13/11/2026, user yêu cầu, chạy --headed) — [x]
- Spec: `e2e/tests/sale/sale-by-product-report.spec.ts` + fixture `e2e/utils/saleByProductFixture.ts` (vai trò quyền tạm + 1 phiếu xuất
  HĐ HRM tạm gắn HĐ #44 + tạm đặt ĐMGG 10% — dọn đúng id / trả NULL ở afterAll, đã kiểm DB sạch).
- Kết quả: **16/16 đạt** (8,3 phút). Phủ: 16 cột (không còn Bảo hành / ĐMGG), số bảng + dòng TỔNG + khối tổng hợp = API, phân trang
  1 request/thao tác, tìm nhanh chờ Enter, nhánh HĐ HRM (giá net theo ĐMGG dòng HĐ, chênh lệch âm đỏ), popup (NVKD, link HĐ HRM →
  /assign/contracts/44, lọc tìm / KH / NVKD, sắp xếp, xoá lọc), In + Excel ở popup và màn chính (mở file kiểm), giữ bộ lọc, Xóa lọc,
  5 mức phạm vi + BE bỏ qua company_id gửi lén.
- **Lỗi thật bắt được + đã sửa:** "In danh sách" trong popup hiện danh sách cột của báo cáo chính → `index.vue` thêm computed
  `printModalColumns` (cột popup khi in từ popup).
- Ghi nhận component chung (không sửa): `V2BasePagination` in tổng số dòng không dấu phân cách ("/ 1832 mặt hàng").

### Checkpoint — 2026-11-13 17:00
Vừa hoàn thành: T1–T11 — port xong BE + FE + menu; test Playwright trình duyệt thật 16/16 đạt; sửa lỗi chọn cột In danh sách của popup (`printModalColumns`)
Đang làm dở: —
Bước tiếp theo: user review + commit 2 repo (hrm-api, hrm-client nhánh develop; e2e spec + fixture nếu muốn giữ); deploy chạy `php artisan permission:catalog-sync`
Blocked:

### Checkpoint — 2026-11-13 (push)
Vừa hoàn thành: commit + rebase lên origin/develop + push — hrm-api `6ce0a92ab`, hrm-client `fb38e3761`; smoke test lại sau rebase đạt
Đang làm dở: —
Bước tiếp theo: deploy chạy `php artisan permission:catalog-sync`; merge develop → gop_db khi team duyệt
Blocked:

### Ghi chú 14/11/2026 — quyền test LOCAL (user yêu cầu, chưa gỡ)
Vai trò **100224** "Test - Xem BC bán hàng theo mặt hàng" (công ty 1) cấp mã `accounting.bao_cao_ban_hang_theo_mat_hang.view` phạm vi 4,
gán user 13. Gỡ:
`DELETE FROM employee_has_roles WHERE role_id = 100224; DELETE FROM role_has_permissions WHERE role_id = 100224; DELETE FROM roles WHERE id = 100224;`

## Phase 2 — Ô lọc danh mục khoá 🔒 (#11736) + đều bề rộng ô lọc (user yêu cầu 14/11/2026)
- [x] T12 BE `filterOptions()`: cờ quyền cho `V2BaseCompanyDepartmentFilter`; Thương hiệu / Hãng SX / Nhóm hàng / Kho qua `LockedCatalogOptions::activeOrUsed` (đã dùng = phiếu báo cáo cộng)
- [x] T13 FE: ô tổ chức → `V2BaseCompanyDepartmentFilter` (công tắc 🔒); danh mục `keepLockedOptions`; bỏ `col` tự đặt
- [x] T14 Playwright: sửa bước lọc tổ chức + kiểm 🔒, chạy lại headed
- [x] T15 Ghi chú skill (erp-to-hrm-screen + report-styles)

### Kết quả Phase 2 (14/11/2026)
- Ô lọc đều bề rộng (bỏ `col` tự đặt). Công ty / Phòng ban / Bộ phận / NV → `V2BaseCompanyDepartmentFilter` (công tắc 🔒).
  Thương hiệu / Hãng SX / Nhóm hàng / Kho: BE `LockedCatalogOptions::activeOrUsed` (dùng = phiếu xuất 14/15/17/21 + bán mượn), FE
  `keepLockedOptions` — ô chọn nhiều nên luôn hiện mục khoá kèm 🔒 (ngoại lệ đã chốt ở #11736 Phase 3). Local: hãng "LIOA",
  kho "MT-KNXT" khoá còn phiếu dùng.
- Lỗi thật lộ ra + đã sửa: (1) BE bỏ qua `department_id` ở phạm vi phòng ban, `part_id` ở phạm vi bộ phận → nay nhận theo đúng ô
  component hiện; (2) Tính chất / Loại hàng hóa map theo `x.id` trong khi API trả `{ value, name }` → ô lọc chết, nay `value ?? id`.
- Sửa `model_type` dòng gán vai trò test 100224 (mất dấu `\` khi escape trong shell).
- Playwright headed: **18/18 đạt** (thêm 01b bề rộng + 🔒, 08b Tính chất / Loại; 15 theo quy ước component).
- Skill: `erp-to-hrm-screen` (checklist A) + `report-styles` (mục 3, 5b).

### Checkpoint — 2026-11-14
Vừa hoàn thành: Phase 2 (T12–T15), test 18/18
Đang làm dở: — (code Phase 2 CHƯA commit: hrm-api `SaleByProductReportService.php`, hrm-client `index.vue`)
Bước tiếp theo: user review → commit + push develop (chỉ 2 file trên, KHÔNG lẫn file báo cáo CSKH install-delivery của phiên khác)
Blocked:

### Phase 3 — Popup chi tiết (user yêu cầu 14/11/2026)
- [x] T16 Bỏ dòng "Tổng cộng: SL bán … Chênh lệch …" trong popup (giữ nút In / Xuất Excel ở chân popup — user chốt để nguyên)
- [x] T17 Phân trang popup theo cấu hình gốc `V2BasePagination` (10 dòng, chọn 5/10/20/50/100)
- Verify: parse template + babel OK; Playwright bước 06 (không còn Tổng cộng) đạt. User dừng test Playwright từ đây — chỉ sửa
  (phiên khác chạy Playwright song song làm hỏng lượt chạy).
- Code Phase 2 + 3 CHƯA commit: hrm-api `SaleByProductReportService.php`; hrm-client `index.vue`, `SaleByProductDetailModal.vue`.
- [x] T18 Phân trang bảng chính giống màn `customer-care/warranty-repair-requests` (khối phân trang của V2BaseDataTable): component
      `components/SaleByProductPagination.vue` (chép markup V2BaseDataTable), mặc định 10 dòng, chọn 5/10/20/50/100. Parse OK, không test Playwright (user dừng).
- [ ] T19 Popup chi tiết: vẫn là V2BasePagination do vỏ chung `V2BaseReportModal` tự vẽ — đổi cần thêm slot vào vỏ chung, chờ user duyệt
- [x] T19 Popup: thêm slot `pagination` vào vỏ chung `components/report/V2BaseReportModal.vue` (user đồng ý 14/11/2026; mặc định vẫn
      V2BasePagination → ~25 popup khác không đổi; slot truyền `onPageChange` / `onPageSizeChange` của vỏ để giữ cuộn-về-đầu). Popup dùng
      `SaleByProductPagination`. Tiêu đề popup chỉ còn TÊN hàng (bỏ mã). Parse OK, không test Playwright.
- [x] T20 Khối tổng hợp: dòng phụ thẻ 'SL bán thực tế' tràn khỏi thẻ khi số lớn → cho xuống dòng (flex-wrap), không nowrap

## Phase 4 — Redmine #12175 (tester 16/11/2026)
- [x] T21 Bug 1 + 4: ~~đổi sang V2BasePagination~~ → user bác 17/11: GIỮ NGUYÊN `SaleByProductPagination` (bảng chính + popup), chỉ tăng cỡ số trong ô "Số dòng/trang" lên 13px (class `sbp-page-size`; áp luôn cho `warranty-repair-by-customer-report` vì dùng chung component)
- [x] T22 Bug 2: ô tìm trong popup chi tiết có nút × xoá nhanh (2 ô chọn đã có × sẵn)
- [x] T23 Bug 3: bỏ chữ "Chi tiết phát sinh của" ở tiêu đề popup (chỉ còn tên hàng)
- [x] T24 Ảnh phụ: bỏ cột NVKD ở popup (ERP không có) — kèm ô lọc NVKD; bỏ cột NVKD khỏi In / Excel popup (BE `DETAIL_COLUMNS`)
- Verify: parse template + babel OK (2 file FE), `php -l` OK. Chưa mở trình duyệt (user tự kiểm).
- `SaleByProductPagination.vue` GIỮ LẠI — `warranty-repair-by-customer-report` (WrcTable, WrcVisitModal) còn import.
- BE vẫn nhận `p_sale_employee_id` + trả `sale_employees` (không ai gửi/đọc nữa, vô hại) — để nguyên.

## Phase 5 — Redmine #12176 (tester 16/11/2026)
- [x] T25 Cột "Chênh lệch" = 0 đang để trống (ERP hiện `0`) → hiện `0`. Nguyên nhân: hàm định dạng tiền `m()` (FE) / `num()` (BE) coi 0 là ô trống. Sửa riêng cột Chênh lệch, các cột tiền/SL khác GIỮ trống như cũ (ERP vẫn in "-" ở SL trả lại):
  - FE: thêm hàm `d()` ở `SaleByProductDetailModal.vue` (popup) + `SaleByProductTable.vue` (bảng chính, gồm dòng Tổng cộng — ERP bảng chính cũng hiện 0)
  - BE `SaleByProductReportPrintService`: cột `diff` đổi kiểu `money` → `diff` (làm tròn như tiền, 0 vẫn in "0") → In + Excel cả bảng chính lẫn popup; chặn "-0" của PHP 7.4
- Verify: parse template + babel OK (2 file FE), `php -l` OK. Chưa mở trình duyệt (user tự kiểm).

## Phase 6 — Redmine #12178 (tester 16/11/2026, bảng chính)
- [x] T26 Ý 1: cột Chênh lệch bảng chính = 0 để trống → đã xử lý chung ở T25 (`d()` trong `SaleByProductTable.vue`, cả dòng Tổng cộng)
- [x] T27 Ý 2: icon ⓘ cạnh "Từ ngày … đến ngày …" lệch xuống. Đo trên dev-hrm (headless, chỉ đọc): hộp icon đã căn giữa dòng, nhưng chữ hoa/số của tiêu đề nằm px 5–14 (tâm 9.5) còn vòng icon px 6–17 (tâm 11.5) → `.rsum-goal > .rsum-tip { transform: translateY(-2px) }` trong `SaleByProductSummary.vue`; tiêm thử CSS trên dev → icon px 4–15, trùng tâm chữ
- Verify: parse template OK. Chưa xem bằng mắt trên trình duyệt (user tự kiểm).

### Checkpoint — 2026-11-17
Vừa hoàn thành: #12175 (T21–T24), #12176 (T25), #12178 (T26–T27)
Đang làm dở: — (CHƯA commit: hrm-client `SaleByProductDetailModal.vue`, `SaleByProductPagination.vue`, `SaleByProductTable.vue`, `SaleByProductSummary.vue`; hrm-api `SaleByProductReportPrintService.php`)
Bước tiếp theo: user mở màn kiểm → commit (KHÔNG lẫn file self-inventory-report đang sửa dở của phiên khác)
Blocked:

## Phase 7 — Redmine #12182 (tester 16/11/2026)
- [x] T28 Bug 1: ô Kỳ thiếu nút × xoá nhanh (các ô chọn khác đã có sẵn) → bỏ `allowClear: false`; bấm × thì watcher đưa Kỳ về mặc
      định "Tháng này" (BE thiếu `period` cũng tính tháng này — để ô trống là lệch số). Bộ lọc lưu cũ có Kỳ rỗng cũng về Tháng này.
- [x] T29 Bug 2 (user chốt 17/11: "chi tiết phát sinh mọi hàng, có dòng trả lại"): 5 số ở khối tổng hợp (≠ 0) bấm được (gạch chân
      nét đứt, khuôn DrillNum) → popup mới `components/SaleByProductAllItemsModal.vue`: từng dòng xuất bán / bán mượn / NHẬP TRẢ của
      mọi mặt hàng theo bộ lọc báo cáo; cột Ngày · Mã hàng (+ nhãn "Trả lại") · Tên hàng · Số HĐ · KH · ĐVT · SL bán / trả / thực tế ·
      đơn giá + thành tiền bán / net · Chênh lệch; dải TỔNG trên bảng; tìm (mã / tên hàng, số HĐ, KH) + lọc KH; In + Xuất Excel.
  - BE `SaleByProductReportService::allItems()` + route `all-items`, `all-items/print-list-data`, `all-items/export`;
    `branchReturn(..., $detail)`; select chi tiết của 2 nhánh kia thêm `product_id`, `line_type`, `returned_qty` (itemList cũ không đổi).
  - Dòng trả lại định giá ÂM theo đơn giá bình quân bán / net của hàng trong kỳ → tổng popup KHỚP thẻ (đo local T6/2026: 6.149 dòng,
    SL / tiền bán / net / chênh lệch khớp tới đồng; T1–T7 lọc HT bán: 33.610 dòng khớp).
  - Lọc / sắp / phân trang ở BE (1 tháng ~5–6 nghìn dòng). Danh mục KH chỉ dựng khi `with_options=1` (lần mở). Tốc độ local: mở
    popup T6 ~7,8s, đổi trang / lọc ~1,5–2,5s.
  - In / Excel: `SaleByProductReportPrintService::ALL_COLUMNS` + `allItemsPrintHtml()` / `allItemsExcelData()`.
- [x] T30 Bug 3: bảng chính 2.140px → ~1.550px (thu hẹp cột, padding 8px); Mã / Tên hàng / Thương hiệu / Hãng SX / ĐVT xuống dòng
      (bỏ cắt "…"), tiêu đề cột xuống dòng. Bản in / Excel không đổi.
- Verify: `php -l` 3 file BE OK; smoke HTTP kernel 5 endpoint 200 (all-items, lọc q, print-list-data, export, item-list cũ); parse
  template + babel 6 file FE OK. CHƯA mở trình duyệt (user tự kiểm).

### Checkpoint — 2026-11-17
Vừa hoàn thành: #12182 (T28–T30)
Đang làm dở: — (CHƯA commit. hrm-api: `SaleByProductReportService.php`, `SaleByProductReportPrintService.php`,
`SaleByProductReportController.php`, `Routes/api.php`; hrm-client: `index.vue`, `SaleByProductSummary.vue`, `SaleByProductTable.vue`,
`SaleByProductAllItemsModal.vue` (mới) — cộng các file Phase 4–6 chưa commit)
Bước tiếp theo: user mở màn kiểm (bấm × ô Kỳ, bấm số thẻ tổng hợp, bảng chính không cuộn ngang) → commit
Blocked:

### 2026-11-17 — #12200 Đổi nút "Xóa lọc" → "Làm mới"
- [x] Bỏ `reset-button-text="Xóa lọc"` ở `pages/sale/sale-by-product-report/index.vue` → dùng mặc định `V2BaseSmartFilterPanel` ("Tìm kiếm" / "Làm mới"), hành vi giữ nguyên
- Kiểm: compile template OK; chưa mở trình duyệt. CHƯA commit.

### 2026-11-17 — #12214 QA: không có quyền vẫn vào xem được màn
- [x] User chốt 17/11 đổi quyết định 13/11 ("ai cũng vào y ERP") → CHẶN khi không có mã `accounting.bao_cao_ban_hang_theo_mat_hang.view` (ERP `ReportController@summarySale` không chặn — lệch ERP có chủ đích)
- [x] BE: group route `/finance/sale-by-product-report` gắn `checkPermission:accounting.bao_cao_ban_hang_theo_mat_hang.view` (mọi endpoint: màn, filter-options, in, Excel, popup) — `Modules/Finance/Routes/api.php`
- [x] FE: menu `sale-hub.js` khai `codes` → ẩn menu + middleware `checkPermission` đẩy link trực tiếp về 404
- [x] Sửa ghi chú cũ "ai cũng vào" ở Catalog / Controller / Service / page index.vue. Mức phạm vi 4 mức giữ nguyên; nhánh `own` của `scopeLevel()` nay không còn tới được (giữ, vô hại)
- Kiểm: `php -l` 4 file; HTTP kernel: user 13 (vai trò test 100224 có mã) 200 ở index / filter-options / export; user 658 (không vai trò) 403 cả 3. Chưa mở trình duyệt. CHƯA commit.
- Lưu ý deploy: trên dev vai trò Super admin (DNS DÙNG) đang "Không xem" mã này (ảnh QA) → sau deploy ai cần xem phải được cấp mã ở `/admin/roles`

### 2026-11-18 — #12175 phản hồi tester: số ở khối tổng hợp hơi to
- [x] `components/sale-by-product-report/SaleByProductSummary.vue` `.sbp-card__value` font-size 20px → 16px (khuôn report-styles 15px). Áp cả màn "Báo cáo tổng hợp bán hàng" (dùng chung component)
- Kiểm: chỉ đổi 1 dòng CSS; chưa mở trình duyệt. CHƯA commit.
- [x] Bấm số ở khối tổng hợp mở popup "Chi tiết phát sinh bán hàng" → lỗi SQL 1222 (UNION lệch số cột). Nguyên nhân: commit 7db9fb3 (16/11, chế độ
      Báo cáo tổng hợp bán hàng) thêm `export_price_amount` vào nhánh chi tiết xuất bán / bán mượn, còn nhánh chi tiết nhập trả (T29, 17/11) không có.
      Sửa `SaleByProductReportService::branchReturn()` nhánh `$detail` thêm `0 as export_price_amount` (khớp nhánh gộp). Popup, In, Excel đều dùng chung câu này.
- Kiểm: `php -l` OK; HTTP kernel `GET /api/v1/finance/sale-by-product-report/all-items` T6/2026 → 200, 6.149 dòng (khớp số đo 17/11), SL trả 2.063. CHƯA commit.
- [x] User 18/11: bỏ dải TỔNG (SL bán / SL trả lại / SL bán thực tế / Thành tiền bán / Thành tiền net / Chênh lệch) ở đầu popup "Chi tiết phát sinh bán hàng"
      — `SaleByProductAllItemsModal.vue` xoá khối `.sbp-all-total` + số "N dòng" (`.report-drill-count`) + CSS. BE vẫn trả `summary` (dùng cho chữ "Đang tải…"); bản In / Excel popup không đổi.
- Kiểm: compile template + babel OK. Chưa mở trình duyệt. CHƯA commit.

### 2026-11-18 — #12221 Bấm × ô Kỳ rồi click ra ngoài, nhãn "Kỳ" vẫn nổi trên viền, ô trống
- [x] Nguyên nhân: watcher `filters` (T28 #12182) đặt lại `period = 'month'` ngay cùng nhịp với lúc × đặt `''` → prop `value` của V2BaseSelect
      đứng yên 'month' (Vue gộp) → select2 không đồng bộ, ô hiện rỗng mà panel thấy `period` có giá trị nên giữ nhãn nổi
- [x] User 18/11 đổi quyết định T28: bấm × → Kỳ để TRỐNG, bảng trống, PHẢI chọn Kỳ mới ra dữ liệu (không phải "toàn bộ thời gian").
      `SaleByProductReportScreen.vue`: bỏ watcher reset "Tháng này" + bỏ ép Kỳ mặc định khi khôi phục bộ lọc lưu; thêm computed `periodMissing`
      → `loadData` / `handleSearch` không gọi API (giống kỳ Tuỳ chọn thiếu ngày), bảng hiện "Chọn Kỳ để xem dữ liệu.", In / Xuất Excel báo toast.
      Không sửa BE. Áp cả màn "Báo cáo tổng hợp bán hàng" (dùng chung component). "Làm mới" vẫn đưa Kỳ về Tháng này.
- Kiểm: compile template + babel OK. Chưa mở trình duyệt. CHƯA commit.

### 2026-11-21 — Note 20/11: đổi ô lọc phân loại hàng
- [x] Màn "Báo cáo bán hàng theo từng mặt hàng" (mode `product`): bỏ ô **Nhóm hàng hóa** + **Loại hàng hóa**, thay bằng 3 ô dây chuyền
      **Nhóm chức năng › Nhóm sản phẩm › Loại sản phẩm** (chọn nhiều, ô dưới thu theo ô trên). Màn "Báo cáo tổng hợp bán hàng" (mode `summary`) giữ nguyên
- [x] BE `SaleByProductReportService`: `filter-options` trả `product_classes` (loại SP đang hoạt động + đã khoá mà hàng đã bán còn dùng, kèm path); nhận
      `product_function_group_ids` / `product_family_ids` / `product_type_ids` → lọc `products.product_type_id` (không sửa hàm chung `applyProductFilters`)
- [x] FE `SaleByProductReportScreen.vue`: 3 ô mới, đổi ô cha thì bỏ giá trị con không còn thuộc; mode product xoá `group_ids`/`product_cates` lưu cũ
- Kiểm: `php -l` OK; compile template + babel OK. HTTP kernel (transaction tạo tạm 1 nhánh phân loại + gán 1 hàng đã bán, ROLLBACK sau test):
  `filter-options` trả `product_classes` đúng path; lọc từng cấp / kết hợp cấp ra đúng 1 hàng, id lạ ra 0; popup `all-items` lọc theo. Chưa mở trình duyệt. CHƯA commit.
- ⚠️ Local 3 bảng `product_function_groups` / `product_families` / `product_types` đều 0 dòng, `products.product_type_id` toàn NULL → 3 ô trống,
  chọn vào lọc ra 0 hàng. Trên dev/prod hàng nào chưa gắn Loại sản phẩm sẽ không lọt khi chọn các ô này.

### Checkpoint — 2026-11-21
Vừa hoàn thành: Note 20/11 — đổi ô lọc phân loại màn mặt hàng
Đang làm dở: — (CHƯA commit: hrm-api `SaleByProductReportService.php`; hrm-client `SaleByProductReportScreen.vue`)
Bước tiếp theo: user mở màn kiểm trên môi trường có dữ liệu phân loại → commit
Blocked:
