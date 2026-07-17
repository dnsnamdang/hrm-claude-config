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
