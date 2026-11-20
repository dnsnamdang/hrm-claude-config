# Báo cáo tồn kho hàng hóa theo kho — Plan

> Người phụ trách: @khoipv · Bắt đầu: 20/11/2026
> Design: `.plans/bao-cao-ton-kho-theo-kho/design.md` · Spec: `docs/superpowers/specs/2026-11-20-bao-cao-ton-kho-theo-kho-design.md`

## Phase 0 — Thiết kế
- [x] 1. Tạo bộ khung feature (.plans, spec, STATUS.md) @khoipv
- [x] 2. Đọc kỹ demo `bc_ton_kho_theo_kho.html` (bộ lọc, KPI, bảng mã → kho → lô/seri, cảnh báo date, in, xuất Excel) @khoipv
- [x] 3. Khảo sát dữ liệu: `stock_balances`, `stock_serials`, `stock_ledgers`, hàng hóa (nhóm / hãng / nước SX), kho @khoipv
- [x] 4. Chốt câu hỏi với user (phân quyền theo cấp, nguồn bộ lọc, mốc cận date, tối ưu DB) @khoipv
  - 20/11: user bảo "tiếp tục" chưa trả lời phân quyền → đề xuất mặc định như Cung ứng (có quyền xem = thấy mọi kho, không phân cấp), chờ user sửa
  - 20/11: trình 3 hướng dữ liệu (A đọc thẳng `stock_balances` + nối seri bằng `balance_id` · B thêm bảng tổng hợp · C tính từ `stock_ledgers`), đề xuất A, chờ user chọn
  - 20/11: **user chốt A + phân quyền như Cung ứng** (có quyền xem = mọi kho, không phân cấp). User hỏi "sai khi HSD trống" → giải thích: SQL `NULL = NULL` không khớp → seri không HSD rơi khỏi lô (DB stag: 8/10 dòng tồn, 3/3 seri không HSD); thêm cả lỗi thiếu `hold_contract_id` ở seri → chốt dùng `balance_id`
- [x] 5. Viết spec chi tiết + design tóm tắt @khoipv
  - 20/11: đã viết spec (DB `balance_id` + index + sửa KH thiếu `customer_id`, quyền, 4 API, luật date, UI V2, Excel, In, edge case) + design tóm tắt; đang chạy reviewer đọc thử spec → gom câu hỏi còn lại cho user
  - 20/11: user bảo push → đã commit + push API (c6ad4ec0), client (f3f568b6), config (af6074f). Spec nằm trong `docs/superpowers/` bị `.gitignore` của config → không lên git
  - 20/11: reviewer hỏi 3 câu, trình user: (1) ĐVT sổ tồn — stag 2/6 dòng PNK nhập khác ĐVT gốc (vd "Chiếc" vs "Hộp"), `writeStock` ghi qty theo ĐVT dòng, không quy đổi → cộng tổng sai; (2) lọc cảnh báo date / tìm nhanh theo mã hay theo lô; (3) mục giữ KH chỉ có tên (không customer_id, không contract_id)
  - 20/11: user bảo "tiếp tục làm" không trả lời → theo đề xuất: (1) sổ tồn theo **ĐVT cơ bản**, hệ số = `order_qty_base / order_qty` của đơn mua (stag: mã 145 nhập 2 Hộp = 102 mL); (2) lọc như demo: Kho + KH cắt lô, ô khác chỉ chọn mã; (3) dò KH: HĐ bán → tên khớp đúng 1 `category_customers` (stag 3/3 tên khớp duy nhất) → không ra thì chặn Duyệt. Đã ghi vào spec 3.3, 3.3b, 5.1

## Kế hoạch code

Toàn cục:
- Test BE = script PHP ở scratchpad, chạy trong `DB::beginTransaction()` + `rollBack()`, chỉ khi tên DB chứa `stag`.
- Test FE = `vuecheck.js` (kiểm cú pháp) + test luật thuần bằng node.
- Không chạy Playwright, không commit khi chưa được bảo.
- Migration chỉ dùng index, không khoá ngoại; số decimal từ API luôn ép `Number()`.
- Cố định các giá trị: `NEAR_DAYS = 90`; quyền `'Xem báo cáo tồn kho'`; config `warehouse.stock_report_open_permission` (mặc định `true`); `columnScreenKey`, bộ lọc `table` và `localStorageKey` đều là `warehouse_stock_report`; route FE `/warehouse/reports/stock-by-warehouse`.

Chỗ dễ sai cần soi kỹ khi review:
- Lô không HSD + có seri → seri phải hiện dưới đúng lô.
- Mã nhập bằng 2 ĐVT → tổng tồn đúng theo ĐVT cơ bản.
- Lọc KH X → tổng / KPI chỉ còn phần của X.
- Tìm theo seri → hiện đủ lô của mã.
- Hàng xoá mềm còn tồn → vẫn hiện.

### Phase 1 — BE: sổ tồn đúng (sửa PNK + migration)
- [x] 1.1 `WarehouseReceiptService`: thêm `resolvePurposeCustomers(array $purposes): array`
  - Dò theo thứ tự: `customer_id` → `contracts.customer_id` → tên khớp đúng 1 `category_customers.name`.
  - Gom truy vấn, không N+1.
  - Gọi trong `buildPurposes` và trong `writeStock`.
  - `validateForApprove`: mục hold có SL nhập > 0 mà không có KH → lỗi "Dòng X: mục đích giữ cho '<tên>' chưa xác định được khách hàng, sửa lại đơn mua".
  - Test: mục chỉ có `contract_id` 2 → KH 2; mục chỉ tên "BỆNH VIỆN ĐA KHOA KHU VỰC TIÊN YÊN" → 3217; tên lạ / tên trùng → null và chặn Duyệt.
- [x] 1.2 `writeStock`: quy ĐVT cơ bản
  - `unitFactor(WarehouseReceiptItem $it): float` = `pop.order_qty_base / pop.order_qty`; `order_qty` ≤ 0 hoặc không có đơn mua → 1.
  - Balance / ledger ghi `round(qty × hệ số, 3)`; ledger `price / hệ số`.
  - `StockSerial` ghi `balance_id`.
  - Test: dòng mã 145 (2 Hộp) → balance 102; seri có `balance_id` đúng.
- [x] 1.3 Migration `Modules/Warehouse/Database/Migrations/2026_11_20_000001_add_stock_report_support.php`
  - `stock_serials.balance_id` + index (`balance_id`, `status`).
  - Index `stock_balances` (`warehouse_id`, `exp_date`) và (`hold_customer_id`).
  - Seed quyền "Xem báo cáo tồn kho" (group Kho, type 7, guard api) + forget cache spatie.
  - Bù dữ liệu trong transaction:
    - (a) snapshot `purposes` của PNK: điền `customer_id`;
    - (b) dựng lại `stock_balances` / `stock_ledgers` / `hold_customer_id` từ các PNK đã duyệt (quy ĐVT + KH), gộp dòng trùng khoá;
    - (c) `stock_serials.balance_id` + `hold_customer_id`.
  - In số dòng sửa ở từng bảng.
  - `down()`: bỏ cột / index / quyền (không hoàn dữ liệu).
  - `database/migrations/2026_11_20_000002_add_warehouse_stock_report_to_column_customizations_table.php`
  - Test: chạy migrate trên stag trong transaction → tổng ledger theo khoá = balance; 3/3 seri có `balance_id`.
- [x] 1.4 Chạy lại `test_pnk.php` (32 check) + `test_blank_full.php` → đều pass
  - 20/11: `test_stock.php` (scratchpad) 28/28 pass trong transaction; migrate thật trên stag bằng `--path` (2 file mới, KHÔNG chạy migration cũ `2026_11_07_000003` đang treo): sổ tồn 10 · thẻ kho 10 · seri 3 (đủ `balance_id`); mã 145 = 102, mã 86 = 30; quyền id 528. `test_pnk` 32/32, `test_blank_full` 3/3
  - Ruling: `unitFactors($items): array [item_id => hệ số]` gom 1 truy vấn thay cho `unitFactor($it)` từng dòng — tránh N+1 — sai thì chỉ là đổi tên hàm
  - Ruling: dựng lại sổ tồn = hàm `WarehouseReceiptService::rebuildStockFromReceipts()` gọi từ migration (ghi lại bằng chính `writeStock`, người ghi = `approved_by`, `created_at` thẻ kho = `approved_at`) — migration phụ thuộc code service; sau này đổi `writeStock` thì chạy lại migration trên DB mới sẽ ra theo luật mới (chấp nhận, chỉ chạy 1 lần)
  - Ruling: chỉ dựng lại khi thẻ kho toàn PNK và mọi seri còn trong kho; ngược lại bỏ qua + in lý do — tránh xóa chứng từ xuất sau này
  - Ruling: `writeStock` ghi luôn snapshot `purposes` đã dò KH vào dòng PNK khi duyệt — để chi tiết phiếu khớp sổ tồn

### Phase 2 — BE: API báo cáo
- [x] 2.1 `Services/StockReportService.php`
  - `filtered(Request $r): Builder` — subquery `b`, áp phạm vi tồn.
  - `productScope(Request $r, Builder $b): Builder` — áp các ô chọn mã.
  - `list(Request $r): array` (data + meta + kpi + today + near_days).
  - `lots(Request $r): array`.
  - `rows(Request $r): array` — trần 20.000 dòng, vượt thì ném lỗi 422.
  - `filterOptions(): array`.
  - `dateStatus(?string $exp): array{status, days_left}` (`expired` / `near` / `ok` / `none`).
  - `ensureCanView()` — 403 khi thiếu quyền và config tắt.
  - Giữ đúng 6 bước truy vấn ở spec 5.2.
- [x] 2.2 `Http/Controllers/Api/V1/StockReportController.php`
  - `index`, `lots`, `rows`, `filterOptions`.
  - Routes nhóm `/stock-report` trong `Routes/api.php`; `filter-options` khai trước các route khác.
  - Thêm `stock_report_open_permission` vào `Config/config.php`.
- [ ] 2.3 Test script trên stag:
  - Tổng KPI = `SUM(qty)` balance > 0.
  - Lọc `hold=common` → chỉ `hold_customer_id = 0`.
  - `keyword` = seri → mã đó, đủ lô.
  - `date_warn=near` → chỉ mã có lô ≤ 90 ngày.
  - `total_from=0` vẫn lọc.
  - Seri hiện dưới lô không HSD.
- [x] 2.3 → scratchpad `test_stock_report.php`: **48/48 pass** (thêm: phân trang, sort, sort lạ, kho dạng chuỗi, seri đã xuất không ra, keyword %/_, đúng 90 ngày = gần, total_to=0, ĐVT cơ bản, lots thiếu kho 422, rows = KPI, 403 khi tắt config). `test_stock.php` vẫn 28/28.
  - Ruling: sort nhận `sort_by` / `sort_desc` (nếp V2 của dns) thay vì `sort` trong spec, whitelist `internal_code|product_name|total`, lạ → mã nội bộ tăng dần — sai thì FE đổi tên tham số
  - Ruling: 403 / 422 của báo cáo dùng lại `WarehouseReceiptException` (cùng module, đã có `forbidden()` + `getHttpCode()`) thay vì tạo exception mới — chỉ là tên class
  - Ruling: `keyword` lọc qua HAVING `MAX(... LIKE)` trên chính tập lô trong phạm vi (seri qua `EXISTS balance_id`, chỉ seri còn trong kho) → mã khớp vẫn hiện đủ lô — truy vấn nặng hơn WHERE, stag 5 lần ~65 ms
  - Ruling: `per_page` tối đa 2000; `hold` nhận `common` hoặc id số, giá trị lạ bỏ qua; `warehouse_ids` nhận mảng hoặc chuỗi "1,2"
  - Ruling: list trả thêm `lot_count` / `near_count` / `expired_count` ở cấp mã và `warehouse_code` ở cấp kho (spec không ghi) — FE cần cho badge cảnh báo dòng mã

### Phase 3 — FE: màn báo cáo
- [x] 3.1 Menu `utils/MenuWarehouse.js`: nhóm "Báo cáo" → "Tồn kho theo kho".
- [x] 3.2 `pages/warehouse/reports/stock-by-warehouse/index.vue`
  - Vỏ V2, KPI, `V2BaseSmartFilterPanel` (đủ ô theo spec 7.2), `filterStateMixin`.
  - `V2BaseDataTable` trải phẳng mã × kho + `cellSpan` + `row-expand`, `columnCustomizationMixin`.
  - Nút: Bung / Thu tất cả · Xuất Excel · In · Cấu hình cột.
- [x] 3.3 `components/LotDetail.vue` (`V2BaseFormTable`, chip seri "+n", badge date), cache `/lots` theo `product_id|warehouse_id`.
- [x] 3.4 `exportStockReport.js` — ExcelJS theo spec 7.5 (1 dòng / lô, ô số là số).
- [x] 3.5 `printStockReport.js` + popup chọn 2 chế độ (A4 ngang).
- [x] 3.6 Kiểm: `vuecheck` các file; test thuần node cho hàm trải phẳng + `cellSpan` (mã 2 kho → rowspan 2 rồi 0).
  - Kết quả 3.6: vuecheck `index.vue` + `LotDetail.vue` OK; `test_stock_fe.mjs` (helper `stockReport.js`) 22/22 pass.
  - Ruling: `warehouse_ids` gửi dạng chuỗi "1,2" — `buildQueryString` lặp `k=v&k=v` không có `[]`, PHP chỉ giữ giá trị cuối; BE `intList` nhận chuỗi phẩy — nếu sai: lọc nhiều kho chỉ ra kho cuối.
  - Ruling: In mở cửa sổ NGAY khi bấm (trước khi gọi API), ghi HTML sau — mở sau `await` bị trình duyệt chặn popup — nếu sai: thấy tab "Đang tải…" trống khi API lỗi (đã đóng tab trong catch).
  - Ruling: In "Bảng tồn theo kho" tối đa 2000 mã (BE chặn per_page ≤ 2000), vượt thì báo lọc bớt; In chi tiết / Xuất Excel dùng `/rows` (BE chặn 20000 dòng lô) — nếu sai: kho rất lớn phải lọc mới in được.
  - Ruling: Không làm ô lọc "SL tồn" theo từng kho — ô "Tổng tồn" + lọc Kho đã thay (tổng tồn tính trên kho đang lọc) — nếu sai: thêm 1 ô range nữa ở BE + FE.
  - Ruling: "Bung tất cả" mở tối đa 20 dòng kho / lần (mỗi dòng 1 request `/lots`), bấm lại để bung tiếp — nếu sai: user phải bấm nhiều lần ở trang 100 dòng.
  - Ruling: Xuất Excel dùng `dayjs` thay `moment` — client không khai `moment` trực tiếp (chỉ `@nuxtjs/moment`).
  - Ruling: Nhóm cột hàng hóa luôn đứng trước nhóm cột kho dù user kéo đổi thứ tự (`orderColumns`) — rowspan chỉ đúng khi ô gộp nằm bên trái dòng chi tiết — nếu sai: user không đưa được cột Kho lên đầu.
  - Ruling: Test helper FE viết sau code (không RED trước) — helper thuần, đã chạy đủ ca biên.
- [ ] 3.7 Báo user test tay trên trình duyệt (user tự test)

### Final review (reviewer opus, 20/11/2026) — 0 Critical, 2 Important, 9 Minor
- [x] Final: fixed I-1 rebuild biến mục giữ KH chưa dò được KH thành tồn chung (kèm HĐ) — `rebuildStockFromReceipts` rà phiếu đã duyệt trước khi xóa, còn mục giữ KH (lô có SL) không ra KH → throw `WarehouseReceiptException` liệt kê "mã PNK dòng n: 'tên'" (transaction rollback); `writeStock` không có KH thì `hold_contract_id = 0` — test_stock mục 6 + 7 RED→GREEN, suite BE 34/34 · 48/48 · 32/32 · 3/3
- [x] Final: fixed I-2 rebuild bị bỏ qua vẫn sửa snapshot `purposes` → lệch sổ tồn — kiểm điều kiện bỏ qua lên TRƯỚC bước (a) — test_stock mục 5 RED→GREEN
- [x] Final: fixed M-1 (nâng lên Important: file Excel / bản in lọc khác bảng đang thấy) — lưu bản chụp `applied` khi tải bảng thành công; bung lô / Xuất Excel / In / dòng "Đang xem" / mô tả bộ lọc dùng bản chụp; helper `snapshotFilters` + `filterParams` (stockReport.js) — test_stock_fe 3 ca mới RED→GREEN, 25/25; vuecheck OK
  - Ruling: Rebuild gặp mục giữ KH không dò ra KH thì THROW (migration dừng, rollback phần dựng lại) thay vì bỏ qua — buộc sửa đơn mua trước, cùng luật với duyệt PNK — nếu sai: deploy DB khác stag bị chặn tới khi sửa đơn mua (stag hiện 10/10 mục đã có KH).
  - Ruling: Cache lô (`lotState`) xóa mỗi lần tải bảng (không chỉ khi đổi bộ lọc) — đi kèm sửa M-1 cho gọn, đồng thời hết luôn M-2 — tốn thêm vài request `/lots` khi đổi trang.
  - Ruling: Reviewer nhắc ruling "không lọc SL tồn từng kho" lệch memory "bộ lọc đủ mọi cột" — giữ, cần user xác nhận.
- Final: minor (deferred): M-3 ô "Số seri" Excel có thể vượt 32.767 ký tự khi 1 lô ~3.000 seri.
- Final: minor (deferred): M-4 `writeStock` bỏ qua lô khi `round(qty × hệ số, 3) <= 0` (hệ số quá nhỏ) — mất seri lặng lẽ.
- Final: minor (deferred): M-5 truyền mảng vào tham số chuỗi (`keyword[]=x`) → 400 "Array to string conversion".
- Final: minor (deferred): M-6 Excel / In chi tiết luôn xếp theo mã nội bộ, không theo sắp xếp trên màn.
- Final: minor (deferred): M-7 `filterOptions` `whereIn` cả danh sách product_id có tồn (nên đổi subquery).
- Final: minor (deferred): M-8 menu báo cáo chưa ẩn theo quyền (các menu kho khác cũng chưa; config mở quyền đang bật).
- Final: minor (deferred): M-9 màu số KPI "Lô hết hạn" `#b02e20` lệch spec `#DC2626`.

### Ghi chú khảo sát 20/11/2026
- Demo: mỗi mã hàng 1 khối (gộp ô) → mỗi dòng con = 1 kho → bung chi tiết lô / seri (NSX, HSD, cảnh báo, mục đích, SL). Bộ lọc: Kho (chọn nhiều), Nhóm hàng, Hãng SX, Nước SX, Khách hàng (tồn chung / giữ KH), Hàng hóa (tên/mã/lô/seri/KH), Chỉ mã có cảnh báo date. KPI: số mã, tổng tồn, giữ KH, số lô cận date / hết hạn. In 2 chế độ (bảng tồn / chi tiết lô-seri), Xuất Excel từng lô/seri.
- Demo còn "quản lý theo lô / seri / lô+seri" → đã bỏ (chốt 19/11), chi tiết dùng 1 dạng chung.
- DB hàng hóa: Mã nội bộ = `internal_code`, Mã thương mại (NSX) = `product_code`, tên TM = `trade_name`, Nhóm hàng = `product_groups`. **Hãng SX + Nước SX là 1 trường gộp** `producer_country_id` → `producer_countries.name` dạng "Hãng/ Nước" (320 dòng).
- Sổ tồn `stock_balances` (kho×hàng×lô×HSD×KH×HĐ) đủ cho báo cáo; `stock_serials` thiếu liên kết về dòng sổ tồn (chỉ khớp được bằng kho+hàng+lô+HSD+KH, HSD null so sánh lệch, không có HĐ).
- **Bug dữ liệu**: 6/32 mục đích giữ KH ở đơn mua cũ chỉ có tên KH + `contract_id`, không có `customer_id` → duyệt PNK ghi `hold_customer_id = 0` (thành tồn chung). Sửa: suy KH từ `contracts.customer_id`.
- `V2BaseDataTable` có sẵn `cellSpan` (gộp ô) + slot `row-expand` → làm được bảng như demo, không cần sửa base chung.

### Chỉnh UI 20/11/2026 (@khoipv)
- [x] Dòng "Đang xem: … · Mốc tính hạn dùng … · Cận date … · SL theo ĐVT cơ bản" → bỏ dòng chữ, gom vào icon ⓘ (`ReportInfoTip`, tiêu đề "Phạm vi báo cáo") cạnh tiêu đề trang (dựng lại markup PageHeader tại màn vì component chung không có slot) — computed `contextLines`; vuecheck OK
- [x] 5 ô KPI → khối tổng hợp `.rsum` theo skill hrm `report-styles` (copy CSS `template/components/TrackingSummary.vue` + `DrillNum.vue`): `components/StockSummary.vue` — dòng "Tồn kho tính đến … · N mã hàng · kho", nút Thu gọn; khối TỒN KHO (Mã hàng có tồn · Tổng SL tồn · Giữ cho KH ẩn khi 0) + khối CẢNH BÁO HẠN DÙNG (Lô cần chú ý = cận + hết hạn · Cận date cam · Hết hạn đỏ #DC2626, ẩn khi 0); xoá CSS `.sr-kpi` — vuecheck OK, FE 25/25
  - Ruling: báo cáo không có popup drill → chỉ số lô cảnh báo bấm được (`DrillNum`), bấm = đặt ô lọc "Cảnh báo date" (any/near/expired); số tồn để chữ thường — nếu sai: thêm popup drill riêng.
  - Ruling: ô "Hết hạn" dùng đỏ `#DC2626` (khuôn chỉ có tông cam) — đồng thời hết M-9.
- [x] Nút "Bung tất cả / Thu tất cả" → đổi chữ theo demo: "Mở tất cả chi tiết / Thu gọn chi tiết" (+ toast giới hạn 20 dòng đổi "bung" → "mở chi tiết")
- [x] Nút Mở tất cả / Thu gọn chi tiết: thay icon remixicon `ri-expand/contract-up-down-line` (không có trong bản font đang dùng → không hiện) bằng SVG mũi tên kép y demo (`.sr-expand-icon` 14px); vuecheck OK
- [x] User hỏi "Lô cần chú ý" vs "Lô cận date" bấm ra giống nhau (stag: hết hạn = 0 nên cần chú ý = cận date, cùng tập lọc) → bỏ ô "Lô cần chú ý"; khối Cảnh báo luôn hiện đủ "Lô cận date" + "Lô hết hạn" (0 thì không tô màu, không bấm) — vuecheck OK
  - Ruling: 2 ô cảnh báo hiện cả khi = 0 (lệch luật "ẩn ô 0" của khuôn rsum) — theo demo gốc, để user thấy rõ "không có lô hết hạn" — nếu sai: thêm `if (x > 0)` như ô Giữ cho KH.
- [x] Bảng chi tiết lô bị cắt + cuộn ngang bên trong (Screenshot_56) → hiện đủ như demo: `LOT_COLUMNS` (stockReport.js) bề rộng cố định, thứ tự + nhãn theo demo (Số lô · Ngày sản xuất · Hạn sử dụng · Mục đích nhập · Cảnh báo · SL tồn · Số seri); có dòng chi tiết đang mở (`anyExpanded`) → cột "Chi tiết" nới theo `detailColWidth()` để nhóm cột kho chứa đủ bảng lô (bảng ngoài cuộn ngang thay vì bảng trong); lề + ray teal trái như `.lotrow` demo — FE 29/29, vuecheck OK
  - Ruling: nới cột "Chi tiết" khi có dòng mở thay vì cho dòng chi tiết trải hết bề ngang bảng — cột thông tin hàng đang gộp dọc (rowspan) phủ cả dòng chi tiết, trải ngang phải bỏ gộp; demo cũng giãn đúng nhóm cột kho — nếu sai: đổi rowspan dừng trước dòng chi tiết.
  - Ruling: không sửa `V2BaseFormTable`/`V2BaseDataTable` (dùng chung) — chỉ tính bề rộng ở màn — nếu sai: thêm prop tắt cuộn trong cho V2BaseFormTable (phải hỏi).
  - Ruling: Số seri vẫn để cột cuối của bảng lô (demo chế độ lô+seri gộp rowspan theo lô; dữ liệu BE đã gom seri theo dòng tồn nên giữ dạng chip) — nếu sai: tách 1 dòng / seri như demo.

### Test E2E Playwright 20/11/2026 (@khoipv) — user yêu cầu
- [x] Viết `e2e/tests/warehouse/bao-cao-ton-kho-theo-kho.spec.js` (chỉ đọc, không ghi DB; số liệu so với API thật): tải màn + khối tổng hợp khớp `kpi`, tooltip phạm vi, mở chi tiết 1 dòng (bảng lô đủ 7 cột, không cuộn ngang bên trong, cột Chi tiết nới/thu), Mở tất cả / Thu gọn chi tiết, drill Lô cận date, tìm nhanh + Enter, Xuất Excel, In
- [x] Chạy test: 9/9 pass (gồm setup) trên stag 6 mã hàng — lần đầu 8/9, test In fail do selector (tên nút có ký tự icon remixicon ở đầu, `^In$` không khớp) → đổi sang `getByTitle('In báo cáo')`, không phải lỗi màn
