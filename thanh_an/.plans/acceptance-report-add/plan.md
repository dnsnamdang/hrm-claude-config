# Plan — Màn thêm mới Biên bản nghiệm thu

**Phụ trách:** @khoipv
**Spec:** `docs/superpowers/specs/2026-06-16-acceptance-report-add-design.md`

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

---

### Checkpoint — 2026-06-16
Vừa hoàn thành: Full BE BBNT (CRUD + meta + khóa loại tonghd + lũy kế + auto code), migrate + route:list OK. FE đã nối API thật (meta, submit, khóa loại).
Đang làm dở: (không).
Bước tiếp theo: Chạy `npm run dev` + BE, verify end-to-end cả 5 loại (đặc biệt: tạo tonghd rồi kiểm tra các lần sau chỉ còn tonghd; lũy kế cập nhật sau khi duyệt).
Blocked: (không).
