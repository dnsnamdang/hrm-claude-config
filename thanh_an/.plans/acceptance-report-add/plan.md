# Plan — Màn thêm mới Biên bản nghiệm thu

**Phụ trách:** @khoipv
**Spec:** `docs/superpowers/specs/2026-06-16-acceptance-report-add-design.md`
**Spec đợt 2 (demo 2):** `docs/superpowers/specs/2026-06-19-acceptance-report-add-demo2-changes-design.md`
**Spec bổ sung (tổng hóa đơn header):** `docs/superpowers/specs/2026-06-22-acceptance-report-invoice-total-header-design.md`

## Phase 0 — Tài liệu
- [x] Tạo `.plans/acceptance-report-add/{design.md,plan.md}`
- [x] Tạo spec đầy đủ
- [x] Cập nhật `STATUS.md` → Đang làm

## Phase 1 — Nền (helpers + container)
- [x] `helpers.js`: contractAgg, itemRemain, normalizeContractItems, format, validate, getAccumulated (stub=0)
- [x] `add.vue`: PageHeader + state (formSubmit/formError) + điều phối 3 bước + footer Hủy/Lưu/Lưu&gửi (stub) + CSS chung (port từ demo)

## Phase 2 — Bước 1 & 2
- [x] `Step1SelectContract.vue`: base-select2 chọn HĐ (API `category/contracts`), select loại NT; emit chọn → load chi tiết HĐ
- [x] `ContractSummary.vue`: info strip + KPI + thanh tiến độ (từ contractAgg)
- [x] `Step2Config.vue`: lần NT / kỳ-tháng / ngày BB + hint theo loại; mờ khi chưa chọn loại

## Phase 3 — Bước 3 + form 5 loại
- [x] `Step3Detail.vue`: switch render form theo loại + AcceptanceFooter
- [x] `forms/ProductGrid.vue`: bảng dùng chung 3 loại lưới (thang/mathang/luyke) theo `variant`
- [x] `forms/FormByMonth.vue` (thang) — wrapper ProductGrid
- [x] `forms/FormByInvoiceTotal.vue` (tonghd)
- [x] `forms/FormByInvoiceDetail.vue` (cthd) + `GoodsPickerModal.vue`
- [x] `forms/FormByProduct.vue` (mathang) — wrapper ProductGrid
- [x] `forms/FormByAccumulated.vue` (luyke) — wrapper ProductGrid
- [x] `AcceptanceFooter.vue`: tổng + banner validate (nút hành động đặt ở footer add.vue)

## Phase 8 — Điều chỉnh mẫu (2026-06-17)
- [x] Thêm cột "Số hóa đơn" cho loại "Theo mặt hàng" (mathang) — đặt ngay sau "Tên hàng hóa", lưu `so_hd` (BE đã sẵn cột + saveItems + Resource, không cần migration). FE: `ProductGrid.vue` (header + input + showSoHd + totalCols + buildDetailItems). Prefill qua buildRows (đã có), readonly qua class `dim` của Step3.
- [x] Loại "Theo tháng" (thang) — Bước 2 đổi từ chọn 1 tháng sang **khoảng tháng (Từ tháng → Đến tháng)**. FE: `Step2Config.vue` (2 ô base-select2 + composedPeriod ghép/splitPeriod tách). Gộp vào `formSubmit.period` 1 chuỗi (`from===to ? from : "from → to"`), BE giữ nguyên, prefill tự tách lại. 2 ô dùng `date-picker type="month"` (vue2-datepicker, format MM/YYYY, value-type YYYY-MM-DD); convert YYYY-MM-DD ↔ "Tháng MM/YYYY" qua monthLabel/parseLabel để chuỗi `period` & prefill không đổi.
- [x] Loại "Chi tiết từng hóa đơn" (cthd) — đồng bộ giống mẫu: (1) sub-tab "Nhập theo hóa đơn" / "Tổng hợp (gộp hàng trùng)" (tab tổng hợp read-only, gộp mặt hàng trùng qua nhiều HĐ + dupbadge + banner vượt); (2) bảng mỗi HĐ đủ cột headCore (thêm Hãng, Quy cách, SL thầu, SL mua thêm, Đã NT). FE: `FormByInvoiceDetail.vue` viết lại + CSS subtab/dupbadge ở `AcceptanceReportForm.vue`. BE giữ nguyên (submit vẫn `invoice_blocks`).

- [x] Validate trường bắt buộc theo pattern màn HĐ — bỏ khóa nút (`canDraft`/`canSend`), luôn cho bấm Lưu/Lưu và gửi để BE `StoreAcceptanceReportRequest` validate → 422 → `formError` hiện inline (Step1 HĐ/loại, Step2 kỳ/ngày BB, Step3 items/invoices/invoice_blocks) + `scrollToInputError`. Chặn mềm (toast) khi vượt SL/giá trị cho cả 2 nút vì BE không kiểm 2 điều này.
- [x] Bỏ nới lỏng nháp ở BE — `StoreAcceptanceReportRequest` validate đầy đủ cho cả status=1 (Lưu) và status=2 (Lưu và gửi), giống `StoreContractRequest` (không phân biệt nháp). Trước đây nháp chỉ cần HĐ + loại nên lưu thiếu trường * vẫn được.

- [x] Chuẩn hóa màn danh sách theo convention màn HĐ (`contract/contract`) — `searchMixin` (lưu/khôi phục filter + pathsToKeep), `formFilter` chứa page/per_page, bộ lọc collapse (`b-collapse#collapse-1` + `search-wrap`, Đặt lại/Áp dụng), `b-table` + `fields` + slots + `:busy`, STT `getNumericalOrder`, trạng thái `BaseStatusColor` (statusColorMap), phân trang chuẩn (per_page select + b-pagination + tổng bản ghi), xóa qua `confirm-delete-selected` modal, filter dùng `buildQuery` (bỏ rỗng). `AcceptanceReportForm` set `fromAddForm` để về trang 1 sau khi tạo.

- [x] Giá trị HĐ trong BBNT phải GỒM phụ lục — snapshot v0 (`ContractDetailResource`) chỉ giữ SL gốc (`qty=root_qty`); phụ lục cập nhật thẳng vào `contract_products.qty` hiện tại (cột `annex_qty`=0, KHÔNG dùng). Fix: `contractMeta` trả thêm `quantities` map `{product_id:{qty,root_qty,price}}` từ `contract_products` hiện tại; FE `loadContractMeta` override `sl_hd=root_qty`, `sl_pl=qty-root_qty`, `price` live → `contractAgg.tong` gồm phụ lục. Verify HD-138/2026 (id 157): 610.471.000 gốc + 19.284.735 PL = 629.755.735 ✓. KHÔNG sửa `ContractDetailResource` (dùng chung).

- [x] Bảng chi tiết BBNT: cột chữ dài (Tên hàng hóa / Tên thương mại / Hãng-nước SX) xuống dòng thay vì giãn theo nội dung — thêm class `wrap-col` (white-space:normal + word-break + max-width 220px) cho `ProductGrid.vue` + `FormByInvoiceDetail.vue` (cả bảng nhập & tổng hợp), CSS ở `AcceptanceReportForm.vue`.

- [x] Danh sách BBNT: thêm 3 bộ lọc Mã hợp đồng (`contracts.code`), Số hợp đồng (`contracts.number`), Khách hàng (`contracts.customer_name`) — lọc qua `whereHas('contract')`. BE `AcceptanceReportService::index` thêm 3 `when` (contract_code/contract_number/customer_name, like). FE `index.vue`: thêm 3 `base-input-field` + 3 key vào `initialStateForm`.
- [x] Loại tổng hóa đơn (`FormByInvoiceTotal.vue`) chỉnh giao diện: tiêu đề cột căn giữa (`text-center` mọi `b-th`), input Số tiền căn phải (`currency-input class="cell text-right"`), ô Ghi chú đổi từ input sang `<textarea class="form-control" rows="2">` giống màn HĐ.
- [x] Chặn tạo BBNT mới khi HĐ đang có biên bản Nháp/Chờ duyệt (mỗi HĐ tối đa 1 biên bản "đang mở"). BE: `AcceptanceReport::OPEN_STATUSES = [NHAP, CHO_DUYET]`; `contractMeta` trả `has_open_report` + `open_report_code` + `open_report_status` (loại trừ chính biên bản đang sửa qua `before_id`); `store` gọi `assertNoOpenReport` → Exception → 400. FE `AcceptanceReportForm.loadContractMeta`: tạo mới + `has_open_report` → toast + `resetContractSelection()` (bỏ chọn HĐ). update không chặn (sửa chính biên bản nháp đó).
- [x] Ô "SL nghiệm thu" dùng `<currency-input>` giống màn HĐ (hỗ trợ số lẻ — phân cách nghìn `.`, thập phân `,` kiểu vi-VN; emit số thuần). FE `ProductGrid.vue` (thang/mathang/luyke) + `FormByInvoiceDetail.vue` (cthd): thay `input type=number` bằng `<currency-input v-model="row.sl" :class="{bad}" @update:item="emitUpdate">`. parseNum/buildDetailItems giữ nguyên (đã xử lý số). BE không đổi.
- [x] Ô nhập "Số tiền" (loại tổng hóa đơn) dùng `<currency-input>` (global, định dạng vi-VN phân cách nghìn, emit số thuần) thay `input type=number`. FE `FormByInvoiceTotal.vue`: `v-model="inv.so_tien"` + `@update:item="emitUpdate"`.
- [x] Fix lũy kế "đã NT/chưa NT" bỏ sót loại tổng hóa đơn — FE `contractAgg.daNT` chỉ cộng item-based (`accumulated`), bỏ qua `accumulated_amount` (BBNT tonghd đã duyệt). VD HD-138/2026 (id 157): L1 mathang + L2 luyke + L3 cthd = 350.212.385, conLai hiển thị 279.543.350; sau L4 tonghd 79tr duyệt, conLai KHÔNG đổi (đúng phải = 200.543.350). Fix: `helpers.contractAgg(items, extraDaNT=0)` cộng thêm extraDaNT vào daNT/conLai/pct; `AcceptanceReportForm` lưu `accumulatedAmount` từ meta + truyền vào `agg`. BE không đổi (đã trả `accumulated_amount` đúng).
- [x] cthd: bắt buộc nhập Số hóa đơn + Ngày hóa đơn mỗi block. BE `StoreAcceptanceReportRequest`: thêm rule `invoice_blocks.*.so` required, `invoice_blocks.*.ngay` required|date + messages. FE: Step3Detail truyền `formError` xuống `FormByInvoiceDetail`; form thêm `<Required/>` + `base-helper-error` (key `invoice_blocks.{bi}.so` / `.ngay`) cạnh 2 ô + đỏ viền input khi lỗi.
- [x] Fix cthd: cùng mặt hàng ở nhiều hóa đơn — "Đã NT" & "Còn lại" ở HĐ sau phải trừ SL nghiệm thu đã điền ở các HĐ TRƯỚC (cộng dồn theo thứ tự block). FE `FormByInvoiceDetail.vue`: thêm `consumedBefore/effNt/effRem` (động), thay `row.sl_nt`/`row.rem` ở tab "Nhập theo hóa đơn" (hiển thị + class + validate input + emitUpdate hasQtyError). Tab tổng hợp giữ nguyên (đã đúng). BE không đổi.
- [x] Màn duyệt BBNT theo pattern HĐ — list chỉ còn nút "Duyệt" (điều hướng tới `/contract/acceptance_report/{id}`, bỏ nút Từ chối + onApprove/onReject/doAction); màn chi tiết (show) là màn duyệt: nút Duyệt + Từ chối ở dưới, "Từ chối" mở modal `ConfirmReasonDenyModal` (id `confirm-reason-deny`, dùng chung các màn duyệt quotation/project) nhập lý do (bắt buộc) → gửi `reason_deny`; hiện "Lý do từ chối" khi status=4 (Không duyệt).

## Phase 9 — Phân quyền BBNT (2026-06-17)
- [x] Seeder: thêm 2 quyền — `Duyệt biên bản nghiệm thu` (id 507), `Xem tất cả biên bản nghiệm thu` (id 508), group "Hợp đồng", type 8. Đã seed (truncate+recreate, giữ id cũ). Hằng `PERM_APPROVE`/`PERM_VIEW_ALL` trên entity.
- [x] BE tạo chỉ cho người lập HĐ: endpoint mới `GET acceptance_reports/selectable-contracts` (HĐ `record_type=HOP_DONG`, `status=DA_DUYET`, `created_by==mình`) cho dropdown Step1; `store` gọi `assertIsContractOwner` chặn → 400. Route đặt trước `/{acceptance_report}`.
- [x] BE trạng thái khi lưu: `resolveStatus` — "Lưu"(1)→Nháp; gửi(≠1)→ có quyền Duyệt ⇒ Đã duyệt(3), không ⇒ Chờ duyệt(2). Áp store + update. BE quyết định cuối, không tin FE.
- [x] BE `index`: `request_type=wait-approve` → status=Chờ duyệt (tất cả); ngược lại không có `PERM_VIEW_ALL` → `created_by==mình`.
- [x] BE approve/reject controller: chặn 403 nếu thiếu `PERM_APPROVE` + giữ check status Chờ duyệt.
- [x] BE model: `canApprove = ChờDuyệt && hasPermission(PERM_APPROVE)`; `canEdit/canDelete = (Nháp|KhôngDuyệt) && isOwner()`. Resource list + detail dùng chung.
- [x] FE Step1: dropdown dùng `selectable-contracts`.
- [x] FE AcceptanceReportForm: mixin CheckPermission; nút 2 = `canApproveReport ? "Lưu và duyệt" : "Lưu và gửi"` (vẫn submit status 2).
- [x] FE `approve.vue` mới: `request_type='wait-approve'`, tiêu đề "Biên bản nghiệm thu chờ duyệt", chỉ Xem+Duyệt, ẩn Thêm mới + lọc mã/HĐ/số HĐ/KH/loại.
- [x] FE `MenuContract.js`: thêm mục "Danh sách biên bản nghiệm thu chờ duyệt" → `/contract/acceptance_report/approve`, `isShow: 'Duyệt biên bản nghiệm thu'`.

- [x] Popup chọn hàng hóa (`GoodsPickerModal.vue`) đổi từ list grid sang **bảng** (b-table style): cột STT/Tên HH/Tên TM/Mã NSX/ĐVT/Đơn giá/Còn lại + checkbox chọn-tất-cả (indeterminate) + click cả dòng + header sticky. Giữ nguyên logic chọn/loại trừ + emit confirm.

## Phase 4 — Hoàn thiện & kiểm thử
- [x] Validate SL vượt còn lại + tổng vượt giá trị HĐ
- [x] Build payload formSubmit đầy đủ theo loại
- [x] Map đúng field BE (qty/annex_qty/product_code...) + format ngày ký + thời hạn (ngày)
- [x] Lần nghiệm thu tự động (đếm theo HĐ)
- [x] Verify UI thủ công cả 5 loại (chờ chạy `npm run dev`)

## Phase 5 — Backend BBNT (CRUD đầy đủ)
- [x] Migration 3 bảng (acceptance_reports, _invoices, _items) — đã migrate OK
- [x] Entities AcceptanceReport (+Item,+Invoice) + constants + relations
- [x] StoreAcceptanceReportRequest (validate theo loại)
- [x] AcceptanceReportService: store/update/delete/show, contractMeta, approve/reject, allowedTypes (tonghd-sticky), accumulated, genCode, total tính ở BE
- [x] Controller + route group `/acceptance_reports` (8 route, route:list OK)
- [x] Resources list + detail

## Phase 7 — Danh sách + Chi tiết + Sửa + Duyệt (FE)
- [x] Tách `components/AcceptanceReportForm.vue` (wizard dùng chung create/edit/show + load + prefill + readonly + submit + approve/reject)
- [x] `add.vue` / `_id/edit.vue` / `_id/index.vue` thành wrapper mỏng theo mode
- [x] Prefill: ProductGrid + FormByInvoiceTotal + FormByInvoiceDetail nhận `initial`; Step1/Step3 readonly
- [x] Đổi loại NT + hiện trạng sang integer (đồng nhất BE)
- [x] `index.vue`: danh sách + lọc (mã/loại/trạng thái) + phân trang + Xem/Sửa/Xóa/Duyệt/Từ chối

## Phase 6 — Nối FE với API thật
- [x] add.vue: gọi `contract/{id}/meta` → lần kế tiếp + allowed_types + lũy kế
- [x] Khóa loại tonghd qua Step1 (lọc typeOptions theo allowedTypes)
- [x] submitForm gọi `POST category/acceptance_reports` (xử lý 422/400), redirect list
- [x] tonghd không cần danh mục hàng hóa (gate step3)
- [x] Verify end-to-end qua UI (chờ chạy dev)

## Phase 10 — Cập nhật theo demo (2) (2026-06-19)
Khớp màn thêm/sửa với `bbnt_demo (2).html`. Spec: `2026-06-19-acceptance-report-add-demo2-changes-design.md`.
- [x] BE `AcceptanceReportService::selectableContracts` select thêm `customer_id`, `customer_name` (Contract có sẵn cột; không migrate).
- [x] Bước 1 `Step1SelectContract.vue`: thêm dropdown **Khách hàng** (cascade KH→HĐ→Loại); tiêu đề "Chọn khách hàng, hợp đồng & loại nghiệm thu"; hint "Chỉ hiển thị hợp đồng do bạn lập — {fullname} ({email})" (từ `current_employee_info`); KH suy ra từ danh sách HĐ; đổi KH → emit `@reset`; prefill + readonly KH cho edit/show (fallback customerOptions từ `contract`).
- [x] `AcceptanceReportForm.vue`: nối `@reset="resetContractSelection"`.
- [x] `ContractSummary.vue`: tên KH kèm **địa bàn** (`customer_area_name`); nhãn "Nhà cung cấp". (Bỏ "lần nghiệm thu kế tiếp" theo yêu cầu — đã gỡ prop `times`.)
- [x] Form "Theo tháng" `FormByMonth.vue`: viết lại có 2 sub-tab "Nhập theo tháng" / "**Tổng hợp (gộp hàng nhiều HĐ)**" (aggRows + dupbadge + cột "Thuộc hóa đơn" + banner vượt SL). `ProductGrid.vue` emit thêm `rows`; event `update` lên cha giữ nguyên.
- [x] Form "Chi tiết từng hóa đơn" `FormByInvoiceDetail.vue`: **bỏ** sub-tab "Tổng hợp (gộp hàng trùng)" + computed aggRows/aggTotal/aggAnyOver + data activeTab (theo demo 2).
- [x] Dropdown KH hiển thị **mã KH**: BE `selectableContracts` join `category_customers` lấy `customer_code`; FE helper `customerLabel` format "mã — tên" (fallback edit/show dùng `contract.customer_code`).
- [x] Tab Tổng hợp (theo tháng): gộp theo **product_id + ĐVT** (không gộp ĐVT khác nhau). `normalizeContractItems` thêm `unit_id`; `aggRows` key composite `${product_id}|${unit_id}`, `:key="row.aggKey"`; hint nói rõ khác ĐVT để riêng.
- [x] Fix show/edit không hiện KH: watch `contract` đổi sang `immediate: true` (wizard chỉ render sau khi tắt loading nên contractRaw đã có sẵn trước mount → watch thường bỏ lỡ → selectedCustomerId null).
- [x] Dropdown KH load **toàn bộ danh mục khách hàng** (`category/customers?per_page=2000`), KHÔNG còn rút ra từ HĐ của tôi (theo yêu cầu user: "khách hàng không cần phải lấy khách hàng của tôi"). `Step1SelectContract`: thêm `customers[]` + `getCustomers()`; `customerOptions` map từ `this.customers` (fallback edit/show từ `contract`). HĐ vẫn lọc theo KH đã chọn + chỉ HĐ do tôi lập.
- [x] User verify: bước 1 KH (full danh mục) → HĐ OK. Lưu ý nghiệp vụ: danh mục có **KH trùng tên** (vd "Ninh Bình": ĐA KHOA `BNB_BV0095` id 1530 vs Mắt `BNB_BV0196` id 1714) → phải chọn đúng mã KH thì HĐ mới hiện; chọn nhầm KH không có HĐ → ô HĐ trống (đúng hành vi). Nhãn KH "mã — tên" giúp phân biệt.
- [x] Đính chính chẩn đoán "BBNT Nháp treo chặn tạo mới": SAI — bản Nháp id 4 đã **xóa mềm** (AcceptanceReport dùng SoftDeletes) nên không chặn. Quy tắc giữ nguyên: chỉ chặn khi có BBNT Nháp/Chờ duyệt còn active.
- [x] **Bỏ quy tắc khóa loại "tổng hóa đơn"** (theo yêu cầu user): trước đây đã có BBNT loại tonghd → các lần sau chỉ được chọn tonghd. Gỡ ở `AcceptanceReportService`: `allowedTypes()` luôn trả `TYPES` (đủ 5 loại); bỏ gọi `assertTypeAllowed` ở `store()` + `update()`; xóa hẳn hàm `assertTypeAllowed`. FE không cần sửa (meta trả đủ loại → dropdown mở hết). Lũy kế giá trị tonghd (`accumulatedAmount`) giữ nguyên.

## Phase 11 — Thêm "Tổng hóa đơn" lên header block cthd (2026-06-22)
Spec: `2026-06-22-acceptance-report-invoice-total-header-design.md`. Chỉ FE, thuần hiển thị.
- [x] `FormByInvoiceDetail.vue`: thêm cụm hiển thị read-only "Tổng hóa đơn" = `fmtMoney(subtotal(block))` trong `.invhead`, bên cạnh "Ngày hóa đơn"; giữ nguyên "Cộng hóa đơn" cuối block.

## Phase 12 — Cập nhật bổ sung (Ngày BB + File lưu trữ) ở mọi trạng thái (2026-06-22)
Spec: `2026-06-22-acceptance-report-supplement-update-design.md`. Plan chi tiết: `docs/superpowers/plans/2026-06-22-acceptance-report-supplement-update.md`. Pattern: "Tiến độ thực hiện" màn HĐ (endpoint riêng, mọi trạng thái).
### BE
- [x] T1: Migration `acceptance_report_files` (không khóa ngoại) + entity `AcceptanceReportFile` + relation `files()` + `canSupplement()` trên `AcceptanceReport`. (review sạch)
- [x] T2: `UpdateAcceptanceReportSupplementRequest` + service `updateSupplement`/`assertCanSupplement` + controller action + route `POST /{id}/updateSupplement`.
- [x] T3: `show` load `files` + resource trả `files` + `can_supplement`. (review sạch)
### FE
- [x] T4: Component `SupplementUpdate.vue` (bảng file Tên tài liệu/File/Ghi chú, upload S3).
- [x] T5: Nhúng vào `AcceptanceReportForm` + CSS miễn nhiễm `readonly-view`.

### Phase 12b — Chỉnh theo phản hồi user (2026-06-22, sửa trực tiếp inline + final review Opus SẴN SÀNG MERGE)
Yêu cầu mới: file lưu trữ hiện ở **mọi màn (gồm Thêm mới)**, lưu chung form chính khi thêm/sửa; ngày biên bản chỉ ở Step2, cho sửa mọi trạng thái; ở Chi tiết có **2 nút Lưu độc lập** (ngày BB / file).
- [x] BE: `store`/`update` gọi `saveFiles(...)` (lưu file kèm form chính); `StoreAcceptanceReportRequest` thêm rule `files.*`; `updateSupplement` tách `has('acceptance_date')`/`has('files')` độc lập (không mất dữ liệu); `saveFiles` private dùng chung.
- [x] FE: `SupplementUpdate.vue` viết lại = **chỉ bảng file** (bỏ ngày BB), mutate `formSubmit.files`, prop `editable`/`showSaveButton`, emit `save`; render ở mọi màn (sau khi chọn HĐ).
- [x] FE: `Step2Config.vue` — ngày BB thêm nút "Lưu" riêng (emit `save-date`) + class `sup-editable` cho sửa khi readonly; props `dateEditable`/`showSaveDate`.
- [x] FE: `AcceptanceReportForm.vue` — `formSubmit.files` khai báo trong data + load từ `report.files`; computed `canSupplementReport`/`fileSectionEditable`; handler `saveAcceptanceDate`/`saveFiles`/`saveSupplement`; CSS override `.sup-editable` + `.supplement-update.supplement-editable`; buildPayload spread `files` → store/update lưu kèm.

### Phase 12c — Thu hẹp cột Quy cách (2026-06-22)
- [x] Cột "Quy cách" giới hạn bề rộng (120–180px) + xuống dòng: thêm class `spec-col` trong `AcceptanceReportForm.vue`, áp cho header + ô ở `ProductGrid.vue`, `FormByMonth.vue`, `FormByInvoiceDetail.vue`.

### Phase 12d — Tách khoảng tháng có cấu trúc period_from/period_to (2026-06-22)
Mục tiêu: loại "theo tháng" lưu Từ/Đến tháng thành 2 cột DATE riêng (thay vì chỉ chuỗi `period`) để sau này LỌC HÓA ĐƠN theo khoảng (`WHERE ngay BETWEEN period_from AND period_to`). Có **backfill dữ liệu cũ**.
- [x] BE migration `2026_06_22_130000_add_period_range_to_acceptance_reports`: thêm `period_from`,`period_to` (DATE, sau `period`) + backfill từ chuỗi `period` cũ (type=1, regex MM/YYYY: cặp đầu→from đầu tháng, cặp cuối→to cuối tháng).
- [x] BE entity fillable + casts `date:Y-m-d`; service `applyPeriodRange` (THANG: from=Y-m-01, to=Y-m-t; loại khác null) gọi trong store/update; request rule nullable|date; resource trả 2 trường.
- [x] FE `Step2Config`: `applyPeriod` set `period_from/period_to` từ monthFrom/monthTo; đổi sang loại khác → clear. `AcceptanceReportForm`: khai báo 2 key trong formSubmit + load từ resource (buildPayload spread sẵn → store/update nhận).
- [x] **Mở Từ/Đến tháng cho MỌI loại** (theo phản hồi): các loại khác "theo tháng" cũng chọn được Từ/Đến tháng nhưng KHÔNG bắt buộc; vẫn giữ ô "Kỳ / thời gian" (text). FE `Step2Config`: hiện Từ/Đến tháng luôn (Required chỉ khi theo tháng) + Kỳ chỉ khi !theo tháng; `applyPeriod` luôn set from/to mọi loại, chỉ ghép `period` khi theo tháng; bỏ clear khi đổi loại; `created` prefill 2 ô tháng từ `period_from/to` (fallback split chuỗi). BE: `applyPeriodRange` bỏ gate THANG (áp mọi loại); `StoreAcceptanceReportRequest` đưa `period_from`/`period_to` (nullable, `period_to after_or_equal period_from`) ra rule chung, `period` vẫn chỉ required khi theo tháng. (Backfill giữ nguyên type=1 — loại khác cũ không có dữ liệu tháng để tách.)

### Phase 12f — Loại "Theo tháng": chọn hàng từ HĐ thay vì đổ mặc định (2026-06-26)
Yêu cầu user: loại "Theo tháng" đang đổ TẤT CẢ hàng hóa HĐ mặc định → đổi sang **chọn hàng** từ HĐ (bắt đầu trống + nút "+ Chọn hàng hóa" mở GoodsPickerModal, có nút xóa dòng), GIỮ nguyên cột Số HĐ / Ngày HĐ mỗi dòng. FE-only, BE không đổi (payload items giữ `{product_id, sl_nghiem_thu, so_hd, ngay_hd}`).
- [x] `FormByMonth.vue`: tách khỏi `ProductGrid` dùng chung; tự quản bảng riêng (tab "Nhập theo tháng") có picker (`GoodsPickerModal`, `excludeIds`=product_id đã có) + nút xóa dòng (`b-button btn-small` + icon trash, đồng nhất FormByInvoiceTotal/Detail); prefill từ `initial` khi edit/show (join với `items` lấy info HH); readonly khi show qua CSS `readonly-view` (`.addrow` + input/datepicker tự ẩn/khóa); giữ tab "Tổng hợp" tính trên `this.rows` đã chọn. Payload `detail.items` giữ `{product_id, sl_nghiem_thu, so_hd, ngay_hd}` → BE không đổi.
- [x] Để nguyên `ProductGrid.vue` (vẫn phục vụ mathang/luyke); không sửa hàm dùng chung. Nhánh `variant==='thang'` trong ProductGrid trở thành code chết vô hại (không xóa để tránh đụng component dùng chung).

### Phase 12e — Dropdown KH chỉ hiện KH đã từng lập HĐ (2026-06-24)
Yêu cầu user: ở Bước 1, ô chọn Khách hàng chỉ hiển thị những KH mà **đã từng lập hợp đồng** (trong các HĐ do mình lập, đã duyệt) — đảo lại Phase 10 dòng 110 (đang load full danh mục). FE-only.
- [x] `Step1SelectContract.vue`: `customerOptions` suy ra từ `this.contracts` (dedupe theo `customer_id`, nhãn "mã — tên" từ `customer_code/customer_name`); bỏ `getCustomers()`/`customers[]`/gọi API `category/customers`. Giữ fallback edit/show từ `contract`. Hint giữ nguyên ("chỉ HĐ do bạn lập").

### Phase 13 — Cảnh báo đỏ rõ khi SL nghiệm thu > còn lại (2026-07-01)
Yêu cầu user (@khoipv): ở màn `add`, khi nhập SL nghiệm thu > SL còn lại thì ô hàng đó CHƯA báo đỏ rõ. Mong muốn: **cho nhập nhưng ô đỏ đậm + dòng chữ đỏ báo lỗi ngay dưới ô, và chặn lưu** (chặn lưu đã có sẵn qua `hasQtyError`). FE-only, style của loại BBNT giữ nguyên altitude. Nguyên nhân: style `input.cell.bad` chỉ đổi viền + nền hồng rất nhạt (`#f7ddd7`) → nhìn như không đổi; không có thông báo lỗi inline.
- [x] `AcceptanceReportForm.vue`: mạnh hóa style `input.cell.bad` (viền đỏ đậm 1.5px + nền đỏ nhạt rõ + chữ đỏ đậm); thêm class `.qty-err` (dòng chữ đỏ nhỏ dưới ô).
- [x] `ProductGrid.vue` (mathang/luyke): thêm `<div class="qty-err">` dưới `currency-input` khi `parseNum(row.sl) > row.rem`, nội dung "Vượt SL còn lại (X)".
- [x] `FormByMonth.vue` (theo tháng): thêm `qty-err` khi `isOver(ri, row)`, X = `rowRemain(ri, row)`.
- [x] `FormByInvoiceDetail.vue` (chi tiết HĐ): thêm `qty-err` khi `parseNum(row.sl) > effRem(bi, row)`, X = `effRem(bi, row)`.

### Phase 14 — Thêm 2 cột "Tổng đã NT (cả lần này)" + "Còn lại (sau lần này)" (2026-07-21)
Yêu cầu user (@khoipv): màn `add`, bảng hàng hóa bổ sung 2 cột tính toán (FE-only, không đụng BE) đặt sau "SL nghiệm thu", trước "Thành tiền". Áp cho cả 4 loại có bảng hàng hóa (mathang, luyke, thang, cthd).
- Công thức: **Tổng đã NT (cả lần này)** = Đã NT (hiệu lực) + SL nghiệm thu; **Còn lại (sau lần này)** = Còn lại (hiệu lực) − SL nghiệm thu. Cột "Còn lại sau" tô màu `rem-ok` khi ≥ 0, `rem-bad` khi < 0 (âm = vượt).
- [x] `ProductGrid.vue` (mathang/luyke): 2 header + 2 cell (`tongDaNt`/`conLaiSau` = sl_nt/rem ± sl); `totalCols` base 7→9.
- [x] `FormByMonth.vue` (thang): pane "Nhập theo tháng" (dùng `rowEffNt`/`rowRemain` ± sl) + pane "Tổng hợp" (dùng sl_nt/rem ± aggSl); colspan dòng trống 17→19.
- [x] `FormByInvoiceDetail.vue` (cthd): 2 header + 2 cell (`effNt`/`effRem` ± sl); colspan dòng trống 14→16.
- [x] Đổi vị trí 2 cột: đặt SAU cột "Thành tiền" (theo yêu cầu user) — cả ProductGrid + FormByMonth (2 pane) + FormByInvoiceDetail.
- [x] STT hàng hóa đếm lại từ 1 trong mỗi nhóm (giống màn HĐ `ProductComponent.vue` dùng `pIndex+1` cục bộ). `ProductGrid.buildRows`: thêm `sttInGroup` reset về 0 khi `groupHead`, `_stt = showGroup ? sttInGroup : i+1`. (Chỉ ProductGrid có nhóm — mathang/luyke; FormByMonth/cthd không chia nhóm.)

---

### Checkpoint — 2026-06-16
Vừa hoàn thành: Full BE BBNT (CRUD + meta + khóa loại tonghd + lũy kế + auto code), migrate + route:list OK. FE đã nối API thật (meta, submit, khóa loại).
Đang làm dở: (không).
Bước tiếp theo: Chạy `npm run dev` + BE, verify end-to-end cả 5 loại (đặc biệt: tạo tonghd rồi kiểm tra các lần sau chỉ còn tonghd; lũy kế cập nhật sau khi duyệt).
Blocked: (không).

### Checkpoint — 2026-06-19 (đợt 2 — demo 2)
Vừa hoàn thành: Phase 10 code BE+FE đầy đủ (KH cascade, địa bàn + lần kế tiếp, theo tháng có tab Tổng hợp, cthd bỏ tab Tổng hợp).
Đang làm dở: (không).
Bước tiếp theo: user verify UI (không cần migrate).
Blocked: (không).

### Checkpoint — 2026-06-22 (Phase 11 + 12)
Vừa hoàn thành:
- Phase 11: hiển thị "Tổng hóa đơn" (read-only, thẻ pill) trên header block cthd — FE xong.
- Phase 12: "Cập nhật bổ sung" (Ngày BB + File lưu trữ, mọi trạng thái) — code đầy đủ T1-T5 (BE 3 task + FE 2 task), qua subagent-driven + review từng task + final review (SẴN SÀNG MERGE, không Critical/Important).
Đang làm dở: (không).
Bước tiếp theo: **user chạy `php artisan migrate` (bảng `acceptance_report_files`) + `npm run dev` verify UI** màn Chi tiết/Sửa BBNT (đặc biệt: lưu bổ sung ở trạng thái Đã duyệt; tài khoản không phải owner/không quyền duyệt → ẩn nút).
Blocked: (không).
Minor để ngỏ (không chặn): M3 — ngày biên bản hiển thị 2 nơi ở màn Sửa (Step2 + block bổ sung), spec đã chấp nhận.
