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
- [x] Thêm cột **Mã nội bộ** (`internal_code`) cấp mặt hàng + **bộ lọc** lọc theo mã nội bộ. (làm 2026-07-21)
  - BE: `saleProductReport` select thêm `COALESCE(NULLIF(cp.internal_code,''), pr.internal_code) as internal_code`; `buildSaleProductTree` thêm field vào node item.
  - FE: header (+1 th col-info rowspan=2 "Mã nội bộ" đặt ngay sau cột Hạng mục), TỔNG CỘNG (+1 td col-info trống), dòng dữ liệu (+1 td chỉ cấp item), colspan "Chưa có dữ liệu" 19→20; filter input `internal_code` + đưa vào `buildRows`/`reset`/watch; include vào keyword search; export Excel (+1 cột).

## Bổ sung sau (2026-07-17)
- [x] Thêm **2 bộ lọc** cấp mặt hàng: **Nhóm HH** (`product_group_name`) và **Loại HH** (`import_type_id`: 1=Nhập khẩu, 2=Phân phối lại). Lọc client-side trên `rawItems` (dữ liệu đã tải sẵn về, không đổi API).
  - FE: template thêm 2 Select2 trong khối filter (Nhóm HH dùng `productGroupOptions` đã có sẵn, bind `product_group_name`; Loại HH dùng options cố định `importTypeOptions` [{1,Nhập khẩu},{2,Phân phối lại}], bind `import_type_id`). `formFilter` thêm `import_type_id` (product_group_name đã có). Computed `importTypeOptions`. Watcher `import_type_id`. `buildRows` thêm điều kiện lọc `import_type_id` (product_group_name đã lọc sẵn). `reset` thêm `import_type_id: null`.

## Bổ sung sau (2026-07-30)
- [x] Thêm **2 bộ lọc khoảng ngày** (server-side, bấm "Áp dụng" mới lọc): **Ngày ký HĐ** từ→đến và **Ngày kết thúc HĐ** từ→đến. UI: label nhóm phía trên + placeholder trong ô, dùng `<date-picker>` (vue2-datepicker, `type=date` `format=DD/MM/YYYY` `value-type=YYYY-MM-DD` `clearable`) giống pattern `reports/guarantee_contract`.
  - FE: `formFilter` đổi `date_from/date_to` → `sign_date_from/sign_date_to`, thêm `end_date_from/end_date_to`; 4 ô date-picker đặt **ngay trên dòng tiêu đề** (`header-action-row`, luôn hiển thị, không nằm trong panel Bộ lọc) — bar `date-filter-bar`/`date-field`, mỗi ô `@change="getData"` lọc ngay khi chọn; đưa cả 4 vào `serverFilter` của `getData` + `reset`.
  - BE: `saleProductReport` đọc `sign_date_from/sign_date_to` (lọc `c.contract_sign_time`) và `end_date_from/end_date_to` (lọc `c.contract_end_time`). Giữ tương thích: vẫn nhận `date_from/date_to` cũ map vào ngày ký.
  - Thêm nút **reset icon** (`variant=success`, `fa-sync-alt`) cạnh cụm nút Ẩn cột TT / Thu gọn / Bộ lọc trên đầu → gọi `reset()` (xóa toàn bộ filter + tải lại). Bỏ tiêu đề trùng "Báo cáo bán hàng theo mặt hàng" ở dòng này. Cụm nút `size=sm` cho gọn.
- [x] Popup **Chi tiết Hợp đồng**: thêm dòng meta **Ngày kết thúc** (`contract_end_time`, `fmtDate`) ngay sau "Ngày ký".
- [x] Tinh chỉnh UI cụm lọc trên `header-action-row`: 3 nút (Ẩn cột TT / Thu gọn / Bộ lọc) **bỏ text, chỉ hiện tooltip khi hover** (`v-b-tooltip.hover` + `:title`), thu nhỏ `btn-icon-only` (31×31). Nút **reset** cũng thu nhỏ như 2 nút kia và đưa **sát ô "Ngày kết thúc đến"** (`.date-reset` cuối `date-filter-bar`).
- [x] Cho 4 ô date-picker **cao bằng ô input/select bên cạnh**: global `_datepicker.scss` ép `.mx-input` = `$input-height` (~34px, có `!important`) trong khi `.form-control` toàn cục = 38px → date-picker thấp hơn. Fix: `::v-deep .mx-input { height: 38px !important; box-sizing: border-box !important }` (độ đặc hiệu cao hơn + `!important` để thắng rule global). Đã thử ép line-height/wrapper nhưng làm vỡ layout → rút gọn chỉ đổi height.
- [x] **Bật nút Xuất Excel** (trước bị `v-if="false"`): hàm `exportExcel`/`generateWorkbook` (ExcelJS) đã có sẵn, xuất từ `filteredItems` nên **tự động theo trạng thái lọc hiện tại** (cả filter client-side keyword/cột lẫn server-side ngày ký/kết thúc/công ty/khách hàng). Nút để dạng `btn-icon-only` `variant=success`, tooltip "Xuất Excel (theo bộ lọc hiện tại)", có spinner khi đang xuất. Bỏ CSS `.btn-export min-width` thừa.
- [x] **Ngày kết thúc tính cả phụ lục gia hạn thời gian**: khi phụ lục gia hạn được DUYỆT, `ContractAnnexTimeService@approve` update thẳng `contracts.contract_end_time` = ngày mới → bộ lọc `whereDate(c.contract_end_time)` đã tự động đúng, KHÔNG cần sửa. Nhưng popup dùng `ContractDetailResource` trả **bản gốc v0** (ưu tiên `version0Data`) → lệch. Fix (không đụng resource dùng chung): report select thêm `c.contract_end_time as contract_end_time_current` → đưa vào flow (`contract_end_time`); FE `openHDModal(id, endTime)` truyền `overrides` cho `openDocModal` để ghi đè `detail.contract_end_time` bằng ngày hiện hành từ dòng report.

- [x] **Hoán 2 cột hiển thị**: cột cây "Hàng hóa" trước hiện `product_code — product_name` → đổi hiện `product_code — product_trade_name` (tên thương mại). Cột "Tên thương mại" (`product_trade_name`) → đổi **tiêu đề "Mã hàng hóa"** + data hiện `product_code` (bỏ class `col-wrap` vì mã ngắn).
- [x] **Excel xuất dạng cây gộp theo hàng hóa** (thay bảng phẳng): viết lại `generateWorkbook` — bỏ cột "Tên thương mại"/"Tên hàng hóa"/"Khách hàng" riêng, thêm cột **"Hàng hóa"** làm cột cây. 3 tầng giống màn: dòng **TỔNG CỘNG** (đậm, nền xanh nhạt, điền cột số tổng từ `grandTotal`) → dòng **MẶT HÀNG** (STT La Mã, `mã — tên thương mại` + đủ info HH: mã nội bộ/ĐVT/mảng/nhóm/loại/quy cách/hãng, đậm nền `#EEF1F5`, cột số trống) → dòng **KHÁCH HÀNG** (STT `n`, tên khách thụt lề, in nghiêng nền `#F7F9FB`) → dòng **FLOW** (STT `n.m`, mã DT·tên DT thụt lề, các cột DT/BG/GT/HĐ). Helper `styleRow` gán border + căn phải/`#,##0` cho cột số; căn trái cột cây. Vẫn lặp trên `filteredItems` nên tôn trọng bộ lọc. Cột Thực xuất vẫn để trống (scope v1).

## Còn lại (cần user chạy/kiểm)
- [ ] Chạy `npm run dev` client, mở `/contract/reports/sale-product` kiểm thị giao diện + collapse + drill-down + Excel.
- [ ] Gán quyền `Xem báo cáo bán hàng theo mặt hàng` cho role qua UI phân quyền.
- v1 chỉ hiển thị luồng HĐ đã ký (pipeline hoãn).

### Checkpoint — 2026-07-02
Vừa hoàn thành: toàn bộ Task 1–7 (BE verify qua tinker/reflection; FE viết theo pattern report-project-contract)
Đang làm dở: chưa chạy nuxt dev để xác nhận render (Node 14, cần user chạy)
Bước tiếp theo: user chạy client + gán quyền cho role + đối chiếu số liệu
Blocked: 

### Checkpoint — 2026-07-21
Vừa hoàn thành: cột + bộ lọc **Mã nội bộ** (`internal_code`). BE: `saleProductReport` select `COALESCE(NULLIF(cp.internal_code,''), pr.internal_code)`, `buildSaleProductTree` thêm field node. FE: ô lọc input `internal_code`, cột "Mã nội bộ" (col-info) đặt sau Hạng mục, TỔNG CỘNG +1 td, colspan 19→20, watch/reset/buildRows + gộp vào keyword search, export Excel +1 cột.
Đang làm dở: chưa chạy nuxt dev xác nhận render (Node 14, cần user chạy)
Bước tiếp theo: user chạy client mở /contract/reports/sale-product kiểm tra lọc + cột hiển thị + Excel
Blocked:

### Checkpoint — 2026-07-30
Vừa hoàn thành: **2 bộ lọc khoảng ngày server-side** — Ngày ký HĐ (từ→đến) + Ngày kết thúc HĐ (từ→đến).
  - BE `ProjectController@saleProductReport`: đọc `sign_date_from/sign_date_to` (fallback từ `date_from/date_to` cũ) lọc `whereDate(c.contract_sign_time)`; đọc `end_date_from/end_date_to` lọc `whereDate(c.contract_end_time)`.
  - FE `sale-product/index.vue`: đổi field `date_from/date_to`→`sign_date_from/sign_date_to`, thêm `end_date_from/end_date_to`; 4 ô `<date-picker>` (label nhóm phía trên + placeholder) trong khối filter; đưa cả 4 vào `serverFilter` (getData) + `reset`; CSS `.filter-label` + ép `.mx-datepicker` width 100%.
Đang làm dở: chưa chạy nuxt dev xác nhận render (Node 14, cần user chạy)
Bước tiếp theo: user chạy client mở /contract/reports/sale-product → mở Bộ lọc, chọn khoảng ngày ký/kết thúc → bấm Áp dụng, đối chiếu số liệu
Blocked:

### Checkpoint — 2026-07-30 (bổ sung UI)
Vừa hoàn thành: hoàn thiện UI cụm lọc trên dòng tiêu đề — 4 ô ngày đưa lên `header-action-row` chia đều, bỏ tiêu đề trùng; 3 nút icon-only + tooltip hover, thu nhỏ 31×31; nút reset thu nhỏ đặt sát ô "Ngày kết thúc đến"; popup HĐ thêm dòng "Ngày kết thúc" (ghi đè bằng ngày hiện hành từ report — đã bao gồm phụ lục gia hạn); **4 ô date-picker cao bằng ô select2** qua `::v-deep .mx-input` (công thức `calc(1.5em + 0.8rem + 2px)`).
Đang làm dở: không
Bước tiếp theo: user chạy nuxt dev mở /contract/reports/sale-product kiểm tra: 4 ô ngày cùng chiều cao với select cạnh, tooltip 3 nút, reset, popup ngày kết thúc
Blocked:
