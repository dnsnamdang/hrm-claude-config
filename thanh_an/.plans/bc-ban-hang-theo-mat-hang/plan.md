# Báo cáo bán hàng theo mặt hàng — Plan

> @khoipv · Plan chi tiết: `docs/superpowers/plans/2026-07-02-bc-ban-hang-theo-mat-hang.md`
> Spec: `docs/superpowers/specs/2026-07-02-bc-ban-hang-theo-mat-hang-design.md`

## Phase 0 — Brainstorming ✅
- [x] Chốt scope (A1 Thực xuất để trống, A2 1 quyền, A3 Excel, không lọc cấp, loại HĐ hủy)
- [x] Viết spec chi tiết
- [x] User review spec + duyệt ("cứ làm đi")
- [x] Lập plan triển khai

## Phase 1 — Backend
- [x] Task 1 — Quyền `Xem báo cáo bán hàng theo mặt hàng` (seeder tổng id=511 + seeder idempotent, đã chạy & verify OK)
- [x] Task 2 — Endpoint `ProjectController@saleProductReport` + route + helper dựng cây (show-once BG/Thầu). Verify: 1442 dòng→707 MH, KPI đúng, tree JSON hợp lệ

## Phase 2 — Frontend
- [x] Task 3 — Trang khung + KPI + bộ lọc
- [x] Task 4 — Bảng cây flatten + collapse (2 tầng header, Thực xuất `–`)
- [x] Task 5 — Drill-down modal (mở thẳng chi tiết DT/BG/GT/HĐ, tái dùng endpoint)
- [x] Task 6 — Xuất Excel (ExcelJS)
- [x] Task 7 — Gắn `isShow` menu

## Đã dùng thực tế (khác plan gốc)
- Dùng snapshot info trên `contract_products` (product_code/name/unit_id/array/group/producer) thay vì join product master → chính xác hơn.
- HĐ hủy = `status = 5` (Contract::HUY), không phải 18.
- Endpoint thực tế: `category/projects/reports/sale-product` (route nằm trong group /projects).
- Drill-down mở thẳng modal chi tiết (không qua bước list) vì flow đã có sẵn id.

## Bổ sung sau (2026-07-02)
- [x] Phân trang client-side ở cấp mặt hàng (giống UI `plan/detail-report`: chọn số dòng/trang + `b-pagination` + "Tổng số mặt hàng"). KPI/Tổng cộng vẫn tính trên toàn bộ; Excel vẫn xuất tất cả trang. Tách `buildRows` (lọc + reset trang) và `renderRows` (dựng dòng theo trang), thêm computed `pagedItems`/`totalRows`/`currentPage`, `onPageChange`, watcher `per_page`.

## Bổ sung sau (2026-07-03)
- [x] Fix border bảng "chưa rõ" so với `sale/report-project-contract`. Gốc rễ: `custom-table.scss` có `.basic-table .table { border-collapse: collapse }` (import vào scoped) thắng specificity so với selector `.banhang-table` → bảng bị `collapse` → viền ô sticky (header + cột đầu) không hiển thị. Sửa: đổi selector `::v-deep .banhang-table` → `::v-deep .basic-table-border .banhang-table` để `border-collapse: separate` có hiệu lực (giống cách report-project-contract dùng `.basic-table-border .table`).

- [x] Fix tên hàng hóa dài bị tràn đè cột ĐVT/Mảng HH/Hãng-Nước SX. Gốc rễ: rule `th, td { white-space: nowrap }` (cho cột số) đè lên cột Hạng mục sticky làm text không ngắt dòng. Sửa: nâng specificity selector cột Hạng mục → `::v-deep .basic-table-border .banhang-table td.gh-sticky` + thêm `word-break: break-word; overflow-wrap: anywhere` để tên dài ngắt dòng trong ô (max-width 480px).

- [x] Fix dòng mặt hàng (lvl-item) bị lệch màu: ô Hạng mục sticky nền trắng còn các ô khác nền xám. Do lần fix border trước nâng specificity `.basic-table-border .banhang-table td.gh-sticky` (nền trắng) thắng rule `tr.lvl-item td.gh-sticky`. Sửa: prefix cả 2 rule nền dòng item thành `.basic-table-border .banhang-table tr.lvl-item td[.gh-sticky]` để nền xám #eef1f5 phủ đều toàn dòng.

## Bổ sung sau (2026-07-04)
- [x] Thêm 3 cột info cấp mặt hàng: **Nhóm HH** (`product_group_name`), **Loại HH** (`import_type_id`: 1=Nhập khẩu, 2=Phân phối lại/PPL), **Quy cách** (`specification`). Đặt sau cột "Mảng HH", nhóm chung khối phân loại. Đều nằm trong nhóm `col-info` (ẩn/hiện theo nút "Ẩn cột TT").
  - BE: `saleProductReport` select thêm `cp.import_type_id`, `cp.specification`; `buildSaleProductTree` thêm 2 field vào node (product_group_name đã có sẵn).
  - FE: header 2 dòng (+3 th rowspan=2), hàng TỔNG CỘNG (+3 td col-info trống), dòng dữ liệu (+3 td, chỉ hiện ở cấp item), colspan "Chưa có dữ liệu" 15→18, helper `importTypeText`, export Excel (+3 cột).

- [x] Popup "Chi tiết Hợp đồng": mã HĐ ngay trên **tiêu đề popup** là link mở **tab mới** sang màn chi tiết HĐ (`/contract/contract/{id}`) — không thêm dòng meta thừa. FE: computed `modalTitleParts` (tách prefix/code/href, chỉ hd-detail có href); slot `#modal-title` render code bằng `<b-link :to target="_blank">`. (Giữ nhánh `m.href` trong template meta như capability chung.)

## Bổ sung sau (2026-07-09)
- [x] Thêm cột **Tên thương mại** (`product_trade_name`) cấp mặt hàng + **bộ lọc** tương ứng.
  - BE: `saleProductReport` select thêm `COALESCE(NULLIF(cp.product_trade_name,''), pr.trade_name) as product_trade_name`; `buildSaleProductTree` thêm field vào node item.
  - FE: header (+1 th col-info rowspan=2 "Tên thương mại"), TỔNG CỘNG (+1 td col-info trống), dòng dữ liệu (+1 td chỉ cấp item), colspan "Chưa có dữ liệu" 18→19; filter Select2 `trade_name` (uniqueOptions) + đưa vào `buildRows`/`reset`/watch; include vào keyword search; export Excel (+1 cột).

## Bổ sung sau (2026-07-13)
- [ ] Thêm cột **Mã nội bộ** (`internal_code`) cấp mặt hàng + **bộ lọc** lọc theo mã nội bộ.
  - BE: `saleProductReport` select thêm `COALESCE(NULLIF(cp.internal_code,''), pr.internal_code) as internal_code`; `buildSaleProductTree` thêm field vào node item.
  - FE: header (+1 th col-info rowspan=2 "Mã nội bộ" đặt ngay sau cột Hạng mục), TỔNG CỘNG (+1 td col-info trống), dòng dữ liệu (+1 td chỉ cấp item), colspan "Chưa có dữ liệu" 19→20; filter input `internal_code` + đưa vào `buildRows`/`reset`/watch; include vào keyword search; export Excel (+1 cột).

## Còn lại (cần user chạy/kiểm)
- [ ] Chạy `npm run dev` client, mở `/contract/reports/sale-product` kiểm thị giao diện + collapse + drill-down + Excel.
- [ ] Gán quyền `Xem báo cáo bán hàng theo mặt hàng` cho role qua UI phân quyền.
- v1 chỉ hiển thị luồng HĐ đã ký (pipeline hoãn).

### Checkpoint — 2026-07-02
Vừa hoàn thành: toàn bộ Task 1–7 (BE verify qua tinker/reflection; FE viết theo pattern report-project-contract)
Đang làm dở: chưa chạy nuxt dev để xác nhận render (Node 14, cần user chạy)
Bước tiếp theo: user chạy client + gán quyền cho role + đối chiếu số liệu
Blocked: 
