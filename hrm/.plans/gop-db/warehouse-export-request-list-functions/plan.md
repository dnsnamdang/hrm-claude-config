# Plan — Bổ sung 4 chức năng màn "Danh sách đề nghị xuất kho"

Ticket: **[ERP => HRM] Đề nghị xuất kho - Danh sách - Thiếu chức năng** — thêm 4 chức năng:
Cài đặt bộ lọc · Xuất excel danh sách · In bộ giấy tờ đi đường · In đề nghị.
Màn: `hrm-client/pages/finance/warehouse-export-requests/index.vue` (module Assign).
Khuôn mirror: `product-export-requests` (STATUS `product-export-request-print-export`).

Xem `design.md` cho khảo sát ERP + quyết định pending. **CHỜ user chốt cách port "In bộ giấy tờ
đi đường" (design §Quyết định #1) trước khi code phần 3.**

## Task

### 1. Cài đặt bộ lọc — FE (migrate V2BaseSmartFilterPanel)
- [x] Đổi `V2BaseFilterPanel` + `#advanced-filters` → `V2BaseSmartFilterPanel` + schema `filterFields`
      (bật `floating`); giữ V2BaseCompanyDepartmentFilter (org). 9 field: product_name, code (mã phiếu),
      type, product_export_request (mã YCXH), requester, created_by, customer, status, approver + range ngày lập.
- [x] Placeholder không lặp nhãn; ô tìm nhanh "Tìm theo …" đúng trường BE lọc.
- [x] `initialFilters` khai đủ key mới; `resetKeys` cho khối org.
- [x] BE `WarehouseExportRequestController::index()` + query scope: nhận thêm các param lọc mới
      (đối chiếu ERP `searchByFilter`). — BE làm ở session trước; verify runtime `code=` → 200.

### 2. Xuất excel danh sách — toolbar
- [x] FE: nút "Xuất Excel" (`secondary status="success"`, `ri-file-excel-2-line`) → `ExportFieldsModal`
      chọn trường → dựng file ExcelJS (mirror `product-export-requests` export-excel.js). 12 cột (design §2).
- [x] BE `GET warehouse-export-requests/export` → JSON theo filter hiện tại (route static TRƯỚC `/{id}`). — BE session trước.
- [x] Thứ tự toolbar: (Tạo mới nếu có) → Xuất Excel → Cấu hình cột.

### 3. In bộ giấy tờ đi đường — row action  ✅ CHỐT hướng A+A1 (design §Quyết định đã chốt)
- [x] BE `WarehouseExportRequestMovePrintService::render()`: blade Lệnh điều động (luôn) + Phiếu xuất
      kho đi đường (chỉ khi có warehouse_id), nối bằng page-break. BỎ passport PDF. — BE session trước.
- [x] BE `printMoveData($id)` (scopedQuery) + route `GET .../{id}/print-move-data`. — BE session trước.
- [x] FE: row action "In giấy tờ đi đường" `ri-truck-line` → `loadPrintPreview` → ReportPrintPreviewModal.

### 4. In đề nghị — row action
- [x] BE `GET warehouse-export-requests/{id}/print-data` → `WarehouseExportRequestPrintService::render()`
      (blade Đề nghị xuất kho, letterhead theo company_id trên phiếu). — BE session trước.
- [x] FE: row action "In đề nghị" `ri-printer-line` → `reportPrintPreviewMixin.openPrintDetail`.
- [x] Thêm `reportPrintPreviewMixin` + `ReportPrintPreviewModal` vào màn.

### 5. Dọn vi phạm quy ước liền kề (khi rework file — design §2)
- [x] Ô rỗng `{{ x || '—' }}` → `{{ x || '' }}`.
- [x] Cột Mã: bỏ `font-weight-bold text-dark`, chuyển `<nuxt-link>` vào chi tiết.
- [x] `confirmCancel`: `$bvModal.msgBoxConfirm` → `$confirm()` (nêu tên phiếu).
- [x] Bỏ row-action "Xem chi tiết"; row actions: Sửa → In đề nghị → In giấy tờ đi đường → Tạo phiếu xuất kho → Hủy.

### Verify
- [x] `php -l` sạch (4 file: Controller, Entity, 2 PrintService — 0 lỗi cú pháp); file BE giữ LF (CR=0). Export inline trong `export()` (FE dựng file), không có class `*Export`.
- [x] Playwright 127.0.0.1:3000 — ĐÃ verify: màn render đủ (11 ô lọc floating, cột giữ contract_code,
      toolbar Xuất Excel + Cấu hình cột, không Tạo mới, empty state, phân trang 20, head() title đúng);
      API index/type-options/column+filter-customization đều 200; ô lọc "Mã phiếu" → param `code=` khớp
      BE `applyFilters`; org block KHÔNG hiện là ĐÚNG fail-closed (user DNS Admin thiếu 4 quyền
      "Xem đề nghị xuất kho theo …", perm names 1531-1534 tồn tại + đúng); console error duy nhất là
      `GET /menu-settings 400` — global layout, KHÔNG phải màn này.
- [x] Playwright — data-dependent (đã verify qua 3 phiếu tạm 35230/35232/35235, mutation đã revert):
      • **In đề nghị** (`print-data`): 2 phiếu 35235 & 35230 đều trả HTTP 200, template HTML hợp lệ —
        "PHIẾU ĐỀ NGHỊ XUẤT KHO", đúng letterhead công ty trên phiếu (Tân Phát, có `<img>`),
        No: PDNXK-xxxxx, đủ dòng hàng (17-18 `<tr>`).
      • **In giấy tờ đi đường** (`print-move-data`): HTTP 200, template gồm **2 tài liệu** nối bằng
        `page-break-before:always` — (1) LỆNH ĐIỀU ĐỘNG HÀNG (luôn có), (2) PHIẾU XUẤT KHO (phiếu
        xuất kho đi đường, do phiếu có warehouse_id). Đúng thiết kế §3.
      • **Xuất Excel**: BE `GET /export` HTTP 200 trả `{rows, filter_text}`, mỗi row đúng **11 field**
        khớp `WAREHOUSE_EXPORT_REQUEST_EXPORT_COLUMNS`; dựng file bằng chính ExcelJS (node_modules) →
        đọc lại: title merge 12 cột, header STT + 11 cột đúng thứ tự, 3 dòng data đầy đủ, STT 1/2/3,
        ô rỗng TRỐNG hẳn, ngày `dd/mm/yyyy HH:mm`, width khớp spec, toàn ô chuỗi (không "stored as text").
      • **Đối chiếu filter keys** (static, tin hơn click từng ô): 12 key `filterFields` + `keyword`
        đều có nhánh trong BE `applyFilters` (code, product_export_request_code, customer_id,
        product_name, type, status, requester, created_by, approver, start_date, end_date, org→
        company_id/department_id/part_id/employee_id, keyword) — 100% khớp, không key mồ côi.
- [x] Dọn DB: đã revert `created_by` 3 phiếu tạm về gốc (35230→205, 35232→318, 35235→209), verify
      lại DB đúng; reload màn → list về rỗng (fail-closed cho user 13) → môi trường sạch.
- [x] Commit + push (user duyệt 18/09/2026, chọn "Tất cả thay đổi"). API `6c49752a4`
      (commit feature `077e5ddce`), Client `a83e986b9` (commit feature `821fa4865`). Cả 2 repo
      đã fetch + merge `origin/gop_db` (không conflict; incoming client có PR normalize-eol
      502k dòng là của team) rồi push thành công.

## Checkpoint
### Checkpoint — bắt đầu (2026-09-18)
Vừa hoàn thành: Bước 1 khảo sát ERP (4 chức năng) qua Explore agent; xác nhận sibling
product-export-requests đã có đủ 4 pattern; đọc full index.vue hiện tại (deficiencies + violations);
viết design.md + plan.md.
Đang làm: chờ user chốt cách port "In bộ giấy tờ đi đường" (design §1) trước khi code.
Bước tiếp theo: code phần 1-2-4-5 (không phụ thuộc quyết định), phần 3 sau khi chốt.
Blocked: quyết định §1 (multi-document set + passport PDF).

### Checkpoint — TẠM DỪNG (2026-09-18, user yêu cầu lưu lại)
Vừa hoàn thành:
- BE (session trước) đã xong cả 4 chức năng + route. FE `index.vue` viết lại xong (rewrite hoàn
  chỉnh, LF, 0 CRLF) + `components/export-excel.js` (149 dòng, LF). Cả 5 nhóm task 1-5 = [x].
- Playwright verify runtime OK: xem chi tiết ở mục Verify [x] phía trên. Chốt 3 loose-end cũ:
  (a) org block không hiện = ĐÚNG (fail-closed, DNS Admin thiếu quyền — KHÔNG phải bug);
  (b) console error = `GET /menu-settings 400` global, không liên quan màn;
  (c) ô lọc "Mã phiếu" gửi param `code=` khớp BE.
- PHÁT HIỆN (không phải bug mới): bấm "Tìm kiếm" bắn 2 request index trùng nhau. Nguyên nhân: panel
  emit CẢ `@filter-change` (→ watcher `filters` deep → fetchData) LẪN `@search` (→ handleSearch →
  fetchData). Đây là pattern DÙNG CHUNG với canonical `product-export-requests` (cùng handler + cùng
  watcher `suppressFilterWatch`) → KHÔNG phải regression mình gây ra. Nếu muốn tối ưu thì phải sửa ở
  cả 2 màn (out of scope ticket này) — GHI LẠI để hỏi user, đừng tự sửa lệch 1 màn.

Đang làm dở: verify runtime phần cần DATA THẬT (list đang rỗng):
  1. Click-through các ô lọc còn lại (type/status/customer remote/date range) → đối chiếu Network param
     với BE `applyFilters` keys: `type`, `status`, `customer_id`, `product_export_request_code`,
     `product_name`, `requester`, `created_by`, `approver`, `start_date`/`end_date`, `company_id`…
  2. Xuất Excel: bấm nút → ExportFieldsModal → chọn trường → tải file → ĐỌC LẠI bằng PhpSpreadsheet
     (script scratchpad) kiểm ô/format. Hiện chưa bấm thử.
  3. In đề nghị (`goPrint`→ `openPrintDetail` → print-data) + In giấy tờ đi đường (`goPrintMove`→
     `loadPrintPreview` → print-move-data): cần ≥1 phiếu để bấm row-action.
  → Cần tìm/tạo 1 đề nghị xuất kho có dữ liệu (hoặc bỏ filter, đổi công ty) để có dòng test.

Bước tiếp theo (khi user quay lại): tạo/tìm 1 phiếu → chạy 3 mục verify còn lại → `php -l` lại các
file BE → cập nhật STATUS. KHÔNG commit/push.
Blocked: không.
Ghi chú giữ nguyên: FE files đều LF (giữ LF); KHÔNG commit/push; chưa tạo bản ghi test nào trong DB.

### Checkpoint — HOÀN TẤT VERIFY (2026-09-18)
Vừa hoàn thành: chạy nốt toàn bộ verify data-dependent còn treo, bằng 3 phiếu tạm reassign
`created_by=13` (35230/35232/35235) rồi **revert về gốc**:
- In đề nghị (print-data) + In giấy tờ đi đường (print-move-data): cả 2 endpoint HTTP 200, template
  HTML hợp lệ, đúng nội dung (đề nghị 1 tài liệu có letterhead; move 2 tài liệu Lệnh điều động +
  Phiếu xuất kho nối page-break). Chi tiết ở mục Verify [x].
- Xuất Excel: BE `/export` trả đúng 11 field khớp FE columns; dựng file thật bằng ExcelJS đọc lại
  đúng cấu trúc/format/dữ liệu.
- Filter keys: đối chiếu tĩnh 12 key FE ↔ BE `applyFilters` — khớp 100%.
- `php -l` sạch 4 file BE, LF giữ nguyên.
- DB: đã revert `created_by` (35230→205, 35232→318, 35235→209), verify lại DB đúng, list về rỗng.
Đang làm dở: không. Toàn bộ task 1-5 [x] + Verify [x] (trừ mục "KHÔNG commit/push" là ràng buộc).
Bước tiếp theo: chờ user duyệt để commit/push (chưa được phép). Không còn việc kỹ thuật tồn đọng.
Blocked: không.

### Checkpoint — ĐÃ COMMIT + PUSH (2026-09-18)
Vừa hoàn thành: user duyệt (chọn "Tất cả thay đổi") → commit + push cả 2 repo lên `gop_db`.
- hrm-api: commit feature `077e5ddce`, sau merge origin thành `6c49752a4` → push OK
  (`253d5594e..6c49752a4`). Kèm thay đổi liền kề WarehouseImportRequestResource (is_can_deny
  loại type 11).
- hrm-client: commit feature `821fa4865`, sau merge origin thành `a83e986b9` → push OK
  (`f88a52931..a83e986b9`). Kèm thay đổi liền kề product-export-requests (tách
  ProductExportRequestForm.vue, rút gọn _id/index.vue).
- Merge `origin/gop_db` cả 2 repo KHÔNG conflict; incoming client có PR normalize-eol (502k dòng)
  là của team, file feature của mình đều LF sẵn nên không bị nhiễu. Commit feature giữ nguyên
  đúng 4 file mỗi repo.
Đang làm dở: không. Feature HOÀN TẤT.
Bước tiếp theo: không còn. Có thể chuyển STATUS sang "Hoàn thành".
Blocked: không.

### Checkpoint — Ticket theo dõi "Sửa UI Bộ lọc" (2026-09-19)
Ticket Redmine mới "[ERP => HRM] Phiếu đề nghị xuất kho - Danh sách: Sửa UI Bộ lọc"
(Nguyễn Minh Hằng → Trần Cư), URL `/finance/warehouse-export-requests`. 4 yêu cầu:
- [x] (1) Ẩn bộ lọc Bộ phận + Nhân viên → ĐÃ CÓ SẴN (`V2BaseCompanyDepartmentFilter`
  `:disable_part` + `:disable_employee` = true, index.vue ~dòng 31-32). Làm sẵn ở phase #11394.
- [x] (2) Thêm bộ lọc Người yêu cầu / Người tạo / Khách hàng / Người duyệt → ĐÃ CÓ SẴN
  (`requester` / `created_by` "Người lập" / `customer_id` / `approver`, index.vue ~334-336, 330).
  Giữ nhãn "Người lập" cho `created_by` (khớp cột bảng `creator_name`), không đổi thành "Người tạo".
- [x] (3) Sửa text "Ngày lập đến" → **"Ngày tạo đến"** (và "Ngày lập từ" → "Ngày tạo từ" cho nhất
  quán; BE lọc `whereDate(created_at)` nên "Ngày tạo" mới đúng). SỬA 3 chỗ dùng chung `created_at`:
  `index.vue:337-338` (filter label), `components/export-excel.js:29` (header cột Excel), comment BE
  controller dòng 99. Cột bảng `created_at` vốn đã là "Ngày tạo" (index.vue ~360) — nay đồng bộ.
- [x] (4) Thêm dấu x khi ô search có ký tự → ĐÃ CÓ SẴN ở component dùng chung: quick search
  `V2BaseSmartFilterPanel.vue:90-91` (`btn-clear-quick-search` + `clearQuickSearch`), và ô lọc text
  `V2BaseFilterFieldControl.vue:58-66` (`filter-text-field__clear`, làm từ Redmine #11170).
Đang làm dở: chưa verify Playwright (server :8000/:3000 chưa chạy). Thay đổi chỉ là đổi chuỗi label
tĩnh trong mảng `filterFields` + header Excel → rủi ro ~0, nhưng theo CLAUDE.md cần chạy live check.
Bước tiếp theo: bật server → Playwright mở panel lọc xác nhận nhãn "Ngày tạo từ/đến"; hoặc user tự
kiểm. LF giữ nguyên cả 3 file. KHÔNG commit/push tới khi user duyệt.
Blocked: không.

---

## Ticket theo dõi "Bảng danh sách - 8 cải tiến" (2026-09-19)

Ticket Redmine **"[ERP => HRM] Phiếu đề nghị xuất kho - Danh sách"** (Nguyễn Minh Hằng → Trần Cư).
Màn `/finance/warehouse-export-requests`. 8 yêu cầu cho "Bảng danh sách". Greenlight user:
"1 ok, 2 làm trọn, 3 ok" (Q1 đổi cả cột + filter; Q2 làm TRỌN tính năng lịch sử; Q3 item 8 nhắm màn
danh sách, verify Playwright). Làm thẳng trên `gop_db`, KHÔNG commit/push tới khi user duyệt.

### Task
- [x] (1) Đổi nhãn cột "Người lập" → "Người tạo" VÀ đổi luôn nhãn bộ lọc `created_by` tương ứng
      (index.vue filter label ~335 + column `creator_name` label/title).
- [x] (2) Thêm 4 cột: Ngày cập nhật · Người cập nhật · Người yêu cầu · Người duyệt.
      - BE: Entity `updater()` relation (`updated_by`→Employee); Resource trả `updater_name` /
        `requester_name` (= creator YCXH nguồn `productExportRequest.creator`) / `updated_at`;
        controller eager-load `updater.info` + `productExportRequest.creator.info`.
      - FE: 4 cell template + 4 cột giữa `created_at` và `status` (`{{ item.x || '' }}`).
- [x] (3) Ẩn nút "Xem chi tiết" → click link cột Mã phiếu (đã xong ở phase #11394).
- [x] (4) "Xem lịch sử" ở CẢ danh sách VÀ chi tiết — làm TRỌN (skill entity-history §5.1):
      - BE service `WarehouseExportRequestService`: trait `LogsCatalogHistory`; `catalogTable`/`catalogColumns`
        (KHÔNG có `status`) / `catalogDisplay` / `detailRows` (`__key=product_id|unit_id`) / `logStatusChanged`;
        gắn log ở `createFromExportRequest` (create), `updateDraft` (update + change_status), `cancel` (change_status).
      - BE `CatalogHistoryService::TABLES` thêm `warehouse_export_requests` (nhãn cột tiếng Việt).
      - FE danh sách: row-action "Xem lịch sử" (`ri-history-line`) → `CatalogHistoryModal.open('warehouse_export_requests', id, code)`.
      - FE chi tiết: `SystemInfoSection` (entity-type `warehouse_export_requests`, endpoint `catalog-histories`)
        nhúng trong thân màn `_id/index.vue`.
- [x] (5) Bỏ sort cột Trạng thái (`status` bỏ `sortable`).
- [x] (6) Thêm sort cột Mã YCXH · Khách hàng · Loại. BE `$sortMap` (V2BaseDataTable emit `column.key`):
      `code`/`created_at`/`customer_name`→cột thật; `type_name`→`type`; `product_export_request_code`→leftJoin `per.code`.
- [x] (7) Bỏ icon cột Mã YCXH → màu + gạch chân như cột Mã phiếu (`v2-cell-link field-line`, bỏ `ri-external-link-line`).
- [x] (8) Ô trống hiển thị "" (không "—") ở màn danh sách — verify bằng Playwright.

### Verify
- [x] `php -l` sạch 5 file BE (Service, CatalogHistoryService, Entity, Resource, Controller).
- [x] Playwright 127.0.0.1:3000 (user emp 48 Trần Văn Đức): ĐÃ verify đầy đủ —
      • Header đủ 15 cột, "Người tạo" (item 1), 4 cột mới Người/Ngày cập nhật + Người yêu cầu + Người duyệt (item 2).
      • Sort caret ở Mã phiếu/Loại/Mã YCXH/Khách hàng/Ngày tạo; KHÔNG có ở Trạng thái (item 5,6).
      • Sort "Loại" → request `sort_field=type_name` HTTP 200, rows đúng thứ tự type 3→14→21 (BE `$sortMap`→`.type`).
      • Mã YCXH cell = `<a class="v2-cell-link field-line">`, màu xanh #28539d, weight 400, KHÔNG icon (item 7).
      • Ô trống render "" không "—": Khách hàng/Số hợp đồng (PDNXK-31063), Người duyệt (PDNXK-31049) (item 8).
      • Popup Lịch sử (danh sách): mở đúng, label "Đề nghị xuất kho: PDNXK-31063", `catalog-histories/.../31063` + filter-options HTTP 200 (item 4a).
      • Mục Lịch sử (chi tiết `_id/index.vue`): SystemInfoSection có, mở "Xem lịch sử" → 2 request catalog-histories HTTP 200 (item 4b).
      • Empty-state "Chưa có lịch sử" là ĐÚNG (bản ghi cũ có trước feature); write-path (create/update/cancel) verify tĩnh (grep 3 điểm log + php -l).
      • Verify data-dependent chạy bằng 3 phiếu reassign `created_by=48` (31063/31055/31049), đã **REVERT về gốc** (13/13/202) + xác nhận `catalog_histories` 0 dòng (chỉ đọc, không ghi).
- FE files (index.vue danh sách + _id/index.vue) đều LF — giữ LF. KHÔNG commit/push tới khi user duyệt.

### Checkpoint — 8 cải tiến Bảng danh sách: CODE + VERIFY XONG (2026-09-19)
Vừa hoàn thành: toàn bộ code 8 item (BE 5 file + FE 2 file) + verify Playwright đầy đủ (mục Verify [x]).
Item 4 làm ĐỦ 2 nơi (popup danh sách + SystemInfoSection chi tiết), cả 2 gọi catalog-histories 200.
DB test đã revert sạch, 0 dòng catalog_histories.
Đang làm dở: không.
Bước tiếp theo: chờ user duyệt để commit/push cả 2 repo lên `gop_db` (chưa được phép).
Blocked: không.
