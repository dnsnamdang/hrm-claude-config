# Báo cáo tổng hợp nhu cầu mua hàng — Plan

- **Spec:** `docs/superpowers/specs/2026-07-13-bao-cao-nhu-cau-mua-design.md`
- **Plan chi tiết:** `docs/superpowers/plans/2026-07-13-bao-cao-nhu-cau-mua.md`
- **Người phụ trách:** @namdangit

## Phase 1 — Backend: quyền + tổng hợp
- [x] 1.1 Seed quyền mới id 517 "Xem báo cáo tổng hợp nhu cầu mua hàng"
- [x] 1.2 `SupplyReportService::purchaseDemand()` — gom `alloc_mua>0` từ phiếu xử lý status=5, group theo mã hàng, KPI, filter options

## Phase 2 — Backend: API
- [x] 2.1 `SupplyReportController` + route `GET supply/reports/purchase-demand` (checkPermission)

## Phase 3 — Frontend
- [x] 3.1 Thêm mục menu vào `MenuSupply.js`
- [x] 3.2 Trang `pages/supply/reports/purchase-demand/index.vue` — khung + fetch + KPI + filter
- [x] 3.3 Bảng khối/mã hàng (rowspan) + popup chi tiết + tooltip + cột chừa chỗ `—`
- [x] 3.4 Xuất Excel FE (ExcelJS)

## Phase 4 — Wrap up
- [x] 4.1 Cập nhật plan/STATUS (chờ user verify UI E2E)

## Phase 5 — Chuẩn hoá bộ lọc theo base project (2026-07-20)
- [x] 5.1 Viết lại khối bộ lọc `index.vue` theo base `contract/contract`: thanh action phải + nút "Bộ lọc" toggle `b-collapse`, panel `search-wrap` grid `col-md-3`, placeholder làm label, cặp nút Đặt lại / Áp dụng
- [x] 5.2 Chuyển các nút report-specific (Xuất excel, Tạo YCGH, Lập HĐ mua) + checkbox "Chỉ mã chưa có HĐ mua" vào layout base
- [x] 5.3 Dọn style `pdr-bar`/`pdr-chk`… không dùng nữa (giữ `.pdr-btn` vì modal còn dùng)
- [x] 5.4 Tách 1 nút "Lập HĐ mua / Đơn mua" thành 2 nút riêng **Lập HĐ mua** (`openLapHdMua('hd')`) + **Lập đơn mua** (`openLapHdMua('don')`); modal bỏ dropdown "Hình thức" (chỉ hiển thị loại đã chọn), tiêu đề động theo `kind`

### Checkpoint — 2026-07-20
Vừa hoàn thành: chuẩn hoá bộ lọc màn `supply/reports/purchase-demand` theo base project (tham chiếu `contract/contract`).
- Thay `pdr-bar` custom → `card > card-body` + thanh action `dataTables_filter text-md-right` (Xuất excel, Tạo YCGH, Lập HĐ mua, nút "Bộ lọc" toggle) + `b-collapse#collapse-1 visible` chứa `search-wrap` form grid `col-md-3`.
- Các select đổi placeholder làm label (bỏ `<label>` + bỏ `@input="fetchReport"`); tìm kiếm Enter = Áp dụng; checkbox "Chỉ mã chưa có HĐ mua" đưa vào lưới lọc; cặp nút **Đặt lại** (`btn-reset` → `resetFilter`) / **Áp dụng** (submit → `applyFilter`).
- Thêm method `applyFilter()`; xoá style `pdr-bar/pdr-fields/fld/pdr-input/pdr-controls/pdr-chk/pdr-actions`.
Đang làm dở: —
Bước tiếp theo: user chạy client verify UI (`/supply/reports/purchase-demand`) — mở/đóng "Bộ lọc", đổi filter + Áp dụng, Đặt lại, các nút action ẩn/hiện đúng.
Blocked: —

## Ghi chú
- Không migration, không commit git, không test tự động (verify tinker/route:list/UI).
- Cột tồn kho/tồn thầu/HĐ mua NCC + 2 nút hành động: chừa chỗ, chờ module.

## Sửa trong lúc review (so với plan gốc)
- **Nhóm hàng**: dùng `products.product_group_id → product_groups.name` (KHÔNG phải `import_type_id` như plan phác — import_type chỉ NK/PPL, sai nghĩa "nhóm hàng").
- **Tên người đề xuất**: `created_by` thực chất map `Employee.id` (quan hệ `belongsTo(Employee,'created_by','id')`), tên = `employee_infos.code - fullname` (khớp `getEmployeeCreateNameAttribute`), KHÔNG phải users.id như comment migration.
- **Filter options**: lấy từ tập gốc (`buildFilterOptions()`, chỉ ràng buộc status=5/alloc_mua>0) để dropdown Nhóm hàng/Khách hàng không tự thu hẹp khi chọn.
- **FE**: thêm `@input="fetchReport"` cho 3 select để đổi filter là gọi lại API (lọc server-side).
- Excel filename có hậu tố timestamp (`bao_cao_nhu_cau_mua_YYYY-MM-DD_HH-mm-ss.xlsx`) — lệch nhỏ so với tên literal trong spec, chấp nhận.
- **(Bổ sung theo yêu cầu user 2026-07-13)** Thêm lại checkbox "Chỉ mã chưa có HĐ mua" (lúc đầu ẩn theo scope). Lọc client-side theo `purchase_contracts` rỗng (`displayRows`), áp cho cả bảng + Excel, reset khi Xóa lọc.
- **(Rework UI 2026-07-13 — user thấy bản đầu xấu + thiếu thao tác)** Viết lại toàn bộ `index.vue` bám aesthetic demo (KPI dải liền, filter bar labeled, bảng teal rowspan/tag/lnk/info-tooltip) và KHÔI PHỤC đầy đủ thao tác theo demo:
  - Thêm lại 2 filter **NCC (HĐ mua)** + **Hợp đồng mua** (options `report.filters.suppliers`/`purchase_contracts` — BE trả rỗng, chờ module HĐ mua).
  - Tick "Chỉ mã chưa có HĐ mua" → hiện **cột tick chọn** (+ chọn tất cả) + nút **📝 Lập HĐ mua / Đơn mua** → modal (chọn hình thức HĐ/Đơn, NCC, ngày cần, SL đặt mua sửa được) → xác nhận **mô phỏng** (toast "chưa ghi dữ liệu thật").
  - Chọn Hợp đồng mua → nút **🚚 Tạo yêu cầu giao hàng** → modal mô phỏng (dormant tới khi có dữ liệu HĐ mua).
  - `picked` seed lại mỗi lần fetch (object mới → reactive cho v-model + allPicked).
  - BE `buildFilterOptions()` trả thêm `suppliers: []`, `purchase_contracts: []` cho khớp contract FE.
- **(KPI align demo 2026-07-13)** Đổi 4 nhãn KPI về đúng demo: "Mã hàng đang thiếu (cần mua)" (đỏ) · "Đơn đặt mua chờ xử lý (từ ĐX cung ứng)" · "Dòng đặt mua chờ xử lý" · "Mã hàng theo dõi". BE thêm `so_ma_theo_doi` = `Product` active count (`countTrackedProducts()`). Lưu ý: chưa có tồn kho/tồn thầu nên "đang thiếu" = mọi mã có nhu cầu mua (net thật tính được khi có module tồn kho).

### Checkpoint — 2026-07-13
Vừa hoàn thành: code xong toàn bộ 9 task (BE: quyền 517 + service + controller + route; FE: menu + trang báo cáo đầy đủ KPI/filter/bảng rowspan/popup/tooltip/Excel). Đã review + sửa 4 điểm (nhóm hàng, tên người đề xuất, filter options, filter change handler).
Đang làm dở: —
Bước tiếp theo: user chạy verify runtime — `php artisan db:seed --class="Modules\Timesheet\Database\Seeders\PermissionsTableSeeder"`, gán quyền 517 cho role, `php artisan route:list --path=supply/reports`, rồi mở `/supply/reports/purchase-demand` verify UI E2E (cần có Phiếu xử lý cung ứng status=5 có dòng Mua hàng).
Blocked: —

## Cố định cột khi cuộn ngang (2026-09-08, @khoipv)

- [x] FE `index.vue`: gắn class cho cột STT + 4 cột "Thông tin hàng hóa" (`th-stt/td-stt`, `th-code1/td-code1`, `th-code2/td-code2`, `th-name/td-name`, `th-unit/td-unit`; header nhóm `th-goods` colspan 4)
- [x] FE: `position: sticky` + bề rộng cố định + mốc `left` lũy tiến cho vùng cột đóng băng (kể cả cột tick chọn khi bật lọc "Chỉ mã chưa có HĐ mua" — table thêm class `has-pick`)
- [x] FE: vẽ lại border của ô sticky bằng `box-shadow` inset (vì `border-collapse: collapse` làm mất border ô sticky khi cuộn) — mép phải vùng cố định để border mảnh như các cột khác, KHÔNG dùng vạch đậm/đổ bóng (user yêu cầu 2026-09-08)
- [x] Verify compile FE (`/supply/reports/purchase-demand` HTTP 200)
- [x] (2026-09-08) User đổi ý 2 lần: bỏ ĐVT ra rồi đưa lại vào vùng cố định → chốt **cố định cả ĐVT**, giữ nguyên header gộp `Thông tin hàng hóa` colspan 4 (biên vùng cố định trùng khít mép phải ô gộp)
- [x] FE: fix hover chỉ sáng dòng đầu của mã hàng — `tr:hover` không phủ được ô `rowspan` (ô rowspan thuộc dòng đầu). Gom mỗi mã hàng thành 1 `<tbody class="grp">` riêng, đổi rule thành `tbody.grp:hover td`

## Fix mã hàng hóa sai do snapshot HĐ bán (2026-09-14, @khoipv)

**Hiện tượng:** hàng "Cóng đựng mẫu bệnh phẩm" (mã nội bộ `VT-XN-001`, mã HH hiện hành `315-613V1`)
sang báo cáo tổng hợp nhu cầu mua lại hiện mã HH `315-448`.

**Root cause:** `contract_products` snapshot mã HH tại thời điểm ký HĐ (HD-002/2025, 13/11/2025 → `315-448`);
hàng hóa sau đó đổi mã (14/04/2026 → `315-613V1`) nhưng snapshot không đổi. Popup chọn hàng lấy mã HH từ
snapshot HĐ → chép xuống PXL → báo cáo. Toàn DB có 33 dòng `contract_products` lệch mã HH so với danh mục.
Báo cáo còn khuếch đại lỗi: gộp theo `product_id` nhưng lấy mã của dòng ĐẦU TIÊN (đúng dòng sai).

**Chốt với user:** làm cả A + B, KHÔNG đụng dữ liệu `contract_products` (giữ nguyên bản ký kết).

- [x] A.1 `SupplyReportService::purchaseDemand()` — lấy `internal_code`/`product_code` từ bảng `products`
      (query làm giàu sẵn có) thay vì tin snapshot `shp.product_code`/`shp.product_hh_code`
- [x] A.2 Bộ lọc từ khóa của báo cáo tìm thêm theo mã hiện hành trong `products` (nếu không, gõ mã mới
      sẽ không ra mã hàng mà mọi dòng PXL đều đang giữ mã cũ)
- [x] B.1 `SupplyProposalService::contractRow()` — mã nội bộ + mã HH lấy theo danh mục hiện hành
      (cache `liveCodeCache`, warm theo lô để không N+1); SL/giá/tên vẫn giữ theo dòng HĐ
- [x] B.2 Verify: dữ liệu báo cáo của `VT-XN-001` ra `315-613V1`; popup chọn hàng HĐ-002/2025 ra mã mới
- [x] B.3 Verify không đụng dữ liệu: `contract_products` giữ nguyên 33 dòng lệch

### Checkpoint — 2026-09-14
Vừa hoàn thành: fix mã hàng hóa sai do snapshot HĐ bán (A + B).
- `SupplyReportService.php`: query làm giàu lấy thêm `internal_code`/`product_code` từ `products`; dòng báo cáo
  dùng mã danh mục hiện hành, chỉ fallback snapshot khi hàng hóa không còn trong danh mục; bộ lọc từ khóa
  tìm thêm theo mã hiện hành (`orWhereIn shp.product_id` subquery trên `products`).
- `SupplyProposalService.php`: thêm cache `liveCodes` + `warmLiveCodes()` (nạp theo lô, tránh N+1);
  `contractRow()` lấy mã nội bộ + mã HH theo danh mục, giữ nguyên SL/giá/tên theo dòng HĐ;
  warm 1 query cho toàn bộ HĐ ở `goodsPool()` và 1 query/HĐ ở `contractProductRows()`.
- Verify tinker: báo cáo VT-XN-001 → `315-613V1`; popup HĐ-002/2025 → `315-613V1`;
  `contract_products` vẫn giữ nguyên 33 dòng lệch (không đụng dữ liệu HĐ).
Đang làm dở: —
Bước tiếp theo: user verify UI `/supply/reports/purchase-demand` + popup chọn hàng của Đề xuất cung ứng.
Blocked: —

## Màn chi tiết phiếu cũng đổi sang mã hiện hành (2026-09-14, user chốt)

- [x] `SupplyProposalService::liveCodeMap()` — helper public trả `product_id => [internal_code, product_code]`
      (dùng lại cache `liveCodes` + `warmLiveCodes`, 1 query cho cả phiếu)
- [x] `DetailSupplyProposalResource` — mã hàng của dòng phiếu đề xuất lấy theo danh mục hiện hành
- [x] `DetailSupplyHandlingResource` — tương tự cho phiếu xử lý
- [x] Verify: PXL-2026-0001 / PXL-2026-0004 / DXCU-2026-0001 / DXCU-2026-0011 đều ra `315-613V1`,
      snapshot `supply_handling_products` trong DB vẫn nguyên (`315-448` ở dòng id 1, 11)

### Checkpoint — 2026-09-14 (lần 2)
Vừa hoàn thành: đổi mã hiển thị của màn chi tiết phiếu đề xuất / phiếu xử lý sang mã danh mục hiện hành.
Đang làm dở: —
Bước tiếp theo: user verify UI (báo cáo nhu cầu mua + mở lại PXL-2026-0001 / DXCU-2026-0001 + popup chọn hàng).
Blocked: —

**Lưu ý:** mở phiếu cũ rồi bấm **Lưu** thì FE gửi lại mã hiện hành → snapshot trong `supply_proposal_products`
/ `supply_handling_products` sẽ được ghi đè bằng mã mới. Đây là hệ quả tự nhiên, không phải lỗi.

**Cố ý KHÔNG đổi:** `contract_products` (dữ liệu HĐ bán), popup "chi tiết HĐ bán" ở DMH
(`PurchaseOrderController::saleContractInfo`), và detail HĐ mua / Đơn mua — đều là chứng từ đã ký, hiển thị
đúng nội dung bản ký kết.

## Bỏ ĐVT quy đổi trên báo cáo (2026-09-16, @khoipv)

Yêu cầu: màn `/supply/reports/purchase-demand` bỏ cột **ĐVT** + cột **SL đề xuất mua**, không quy đổi ĐVT
nữa — SL hiển thị đúng như trên phiếu xử lý, kèm ĐVT ngay sau số. Popup "Đang đề xuất mua" bỏ luôn.
Chốt thêm: phần nạp sang **Lập HĐ mua / Lập đơn mua** vẫn giữ số đã quy đổi như cũ.

- [x] BE1 `SupplyReportService::purchaseDemand()` — mỗi `line` trả thêm `raw_quantity` + `raw_unit_name`
      (SL/ĐVT snapshot trên PXL, không quy đổi); bỏ `origin_quantity` / `origin_unit_name`
- [x] BE2 Giữ nguyên `buildUnitPlans()` + `total_buy_qty` + `unit_id`/`unit_name` của khối (seeding HĐ/đơn mua)
- [x] FE1 Bảng chính: bỏ cột ĐVT (+ cảnh báo ⚠) và cột SL đề xuất mua, chỉnh colspan nhóm header + dòng rỗng
- [x] FE2 Cột "Số lượng" → "Số lượng (ĐVT)", giá trị hiện `SL + ĐVT` của chính dòng phiếu
- [x] FE3 Bỏ popup `pdr-detail-modal` + `openDetail()` + `selectedRow` + `qtyTitle()`
- [x] FE4 Excel: bỏ cột ĐVT khối + SL đề xuất mua, thêm cột ĐVT ngay sau cột Số lượng (theo từng dòng phiếu)
- [x] FE5 Dọn CSS `.th-unit/.td-unit/.col-propose/.unit-warn` + ghi chú cuối bảng
- [ ] FE6 Verify UI

### Checkpoint — 2026-09-16
Vừa hoàn thành: bỏ quy đổi ĐVT trên màn báo cáo nhu cầu mua.
- BE `SupplyReportService.php`: mỗi `line` thêm `raw_quantity` / `raw_unit_id` / `raw_unit_name`
  (SL + ĐVT nguyên trạng trên PXL); bỏ `origin_quantity` / `origin_unit_name`.
  `quantity` (đã quy đổi) giữ lại vì `total_buy_qty` + seeding Lập HĐ mua / Lập đơn mua vẫn dùng.
- FE `pages/supply/reports/purchase-demand/index.vue`: bỏ cột ĐVT (kèm cảnh báo ⚠ thiếu hệ số) và
  cột SL đề xuất mua; colspan nhóm 4→3, dòng rỗng 18/19→16/17; cột "Số lượng (ĐVT)" hiện
  `raw_quantity` + `raw_unit_name`; bỏ popup `pdr-detail-modal` + `openDetail` + `selectedRow` + `qtyTitle`;
  Excel bỏ cột ĐVT khối + SL đề xuất mua, thêm cột ĐVT ngay sau cột Số lượng (giữ ô SL là number);
  dọn CSS `.th-unit/.td-unit/.col-propose/.unit-warn`, thêm `.unit-inline`.
- Verify BE (php -r + service thật): HC-SH-3307 / PXL-2026-0011 trước hiện 300 Hộp (quy đổi) → nay 600 mL
  đúng như phiếu; `total_buy_qty` của mã vẫn 450 Hộp cho seeding HĐ/đơn mua.
- Verify FE: vue-template-compiler compile template không lỗi, script parse OK.
Đang làm dở: —
Bước tiếp theo: user mở `/supply/reports/purchase-demand` xem bảng + xuất Excel để xác nhận.
Blocked: —
