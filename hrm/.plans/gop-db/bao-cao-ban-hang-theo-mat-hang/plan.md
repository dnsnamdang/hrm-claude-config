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
