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
