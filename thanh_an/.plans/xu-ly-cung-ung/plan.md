# Plan — Xử lý cung ứng (build thật)

> Phụ trách: @namdangit · Ngày: 2026-07-08
> Spec: `docs/superpowers/specs/2026-07-08-xu-ly-cung-ung-design.md`
> Plan chi tiết (9 task): `docs/superpowers/plans/2026-07-08-xu-ly-cung-ung.md`

## Phase 0 — Brainstorm & chốt design

- [x] 0.1 Chốt mô hình phản hồi + duyệt nội bộ + lưu phân bổ (không sinh chứng từ thật) + 3 màn tách riêng
- [x] 0.2 Fill spec đầy đủ + design.md + plan chi tiết

## BE

- [x] 1 Refactor đề xuất (rejections + trạng thái suy ra + reject behavior + resource) — review clean; guard `class_exists(SupplyHandling)` tránh crash forward-ref. Minor: show() chưa eager-load rejections (fold sau).
- [x] 2 Migrations + entities phiếu xử lý (supply_handlings + _products) — review clean 100%, guard Task 1 mở
- [x] 3 Permission 515 Duyệt phiếu xử lý cung ứng — verify: thêm đúng sau 514, group Cung ứng type 7, gán Admin
- [x] 4 Phiếu xử lý CRUD + approve + inbox (gộp) — review Approved (opus). Verify vòng đời KH→5/nội bộ 3→5, inbox, handle_status dangxl. Fix Important: N+1 do responses trên list đề xuất (eager-load handlings.products/rejections + relationLoaded + withCount).

## FE

- [x] 5 Menu +2 mục + inbox đề xuất (supply_proposals/inbox.vue) — review clean. Note: list resource thiếu files/sent_at (dùng created_at, bỏ cột file).
- [x] 6 Danh sách phiếu xử lý (supply_handlings/index.vue + constants.js) — verify OK (badge/cờ/shape/path). Minor→Task 8: nút Duyệt gate thừa `hasAPermission(PERM_HANDLE)` (nên chỉ `can_approve`).
- [x] 7 Form phiếu xử lý (add.vue + HandlingGoodsTable) — review Approved (opus): không mất field, công thức đúng. Fix Important: edit phiếu KH truyền customer_id top-level để pool không rỗng.
- [x] 8 Tabs tổng hợp + validate + duyệt — review Approved (opus). Fix Important: SimpleQtyTable dùng `template:` string crash runtime → tách SFC. Fix Minor: responses key (handler_name/reason/code), red logic conLai<0, dọn import.
- [x] 9 Bổ sung đề xuất (phản hồi) + E2E + wrap up — review clean. Badge đề xuất dùng handle_status khi đã gửi; khối "Phản hồi xử lý" ở chi tiết.

## Checkpoint — 2026-07-08

Vừa hoàn thành: Toàn bộ 9 task (BE Task 1-4 + FE Task 5-9) — code xong, mỗi task đã review (nhiều opus + đối chiếu BE thật, fix các blocker/important). Chờ final whole-branch review + user verify UI E2E.
Bước tiếp theo: User seed lại `PermissionsTableSeeder` (quyền 515) + migrate (nếu máy khác) + `npm run dev`, verify E2E theo checklist (`scratchpad/xl-task-9-report.md`). Gán quyền 513/514/515 cho user test.
Blocked: (trống)

## Final whole-branch review (opus) — không blocker

- Nhất quán BE↔FE ✅ · không regression đề xuất ✅ · spec đủ ✅ · guard nhất quán ✅.
- Fixed: M1 (N+1 `employee_create` trong buildResponses → eager-load handlings/rejections.employee_create.info), M2 (dropdown filter đề xuất bỏ 7/9).
- Để cleanup sau: M3 (inbox thêm filter Khách hàng — BE đã hỗ trợ customer_id), M4 (nút Tạo/Từ chối hiện cả khi đã từ chối — BE báo lỗi khi bấm lại).

## Chỉnh theo feedback UI (2026-07-09)

- Nút hành động màn Danh sách đề xuất (inbox): "Thao tác"→"Hành động", nút chữ "Tạo phiếu xử lý"/"Từ chối" nằm ngang, dùng btn sm gốc (không CSS riêng).
- Bảng phân bổ (HandlingGoodsTable): thu ô nhập 84→62px, font 12.5px canh giữa (số không còn bé). Màu bảng làm lại: header nhóm chữ đậm + màu theo nhóm, zebra + hover, cột Kết quả nền tím, ô nhập có viền + focus. **Cột "Số liệu nguồn": user chốt hiện đủ 6 cột như demo** (Còn lại HĐ + Tồn kho/Đang mua/Hàng vay/Hàng gửi/Hàng đổi — 5 cột sau chưa wire, = 0) → chấp nhận kéo ngang.
- Gộp bảng phân bổ + "Tổng hợp xử lý" thành **1 bộ tab** như demo: HandlingSummaryTabs thêm tab đầu "Xử lý cung ứng hàng" qua slot `main`; add.vue gộp 2 card → 1 card. Đổi tên tab khớp demo (Phiếu đề nghị xuất kho / Phiếu đề nghị mua hàng).
- Tab "Tham chiếu hợp đồng bán" (phiếu xử lý) bổ sung đủ cột như bên đề xuất (Số HĐ, Thời gian ký/kết thúc, Cty thực hiện, SL hợp đồng/phụ lục/đã thực hiện/còn lại). Mang field HĐ qua 3 map FE (proposal/pool/handling) + `DetailSupplyHandlingResource` nạp lại qua `contractRefMap()` khi mở lại phiếu.

## Bổ sung bám demo (2026-07-09, sau đối chiếu 2 file demo)

- **Mục 2 — Số phiếu xử lý dự kiến**: BE `SupplyHandlingService::previewNextCode()` + `SupplyHandlingController::nextCode()` + route `/next-code` (trước wildcard). FE add.vue hiện field "Số phiếu xử lý" ở cả mode Lập (gọi next-code → previewCode `PXL-YYYY-####`).
- **Mục 3 — Header dự kiến tab phiếu**: HandlingSummaryTabs thêm `.dukien-head` (Số phiếu dự kiến "Sinh khi lưu" · Ngày lập = hôm nay · Kho xuất/Bộ phận tiếp nhận/Hình thức) cho 4 tab: Đề nghị xuất kho, Đề nghị mua hàng, Xuất gửi, Trả vay.
- **Mục 4 — Popup chọn hàng**: GoodsPickerModal thêm checkbox "Chỉ hiện hàng còn SL theo HĐ" (type=1, lọc `in_contract && sl_con_lai_hd>0`) + nút "Chọn tất cả / Bỏ chọn tất cả" ở footer.
- **Mục 1 — Cột "File đính kèm" ở màn Danh sách đề xuất (inbox)**: BE `SupplyProposalResource` trả thêm mảng `files` (guard `relationLoaded`); `index()`+`inbox()` eager-load `files` (tránh N+1). FE inbox.vue thêm cột với chip icon-theo-loại-file + bấm mở `FilePreviewModal` (dùng chung).

## Chỉnh luồng trạng thái phiếu xử lý (2026-07-10, user chốt)

- Vấn đề: phiếu KH không có bước duyệt nhưng mượn nhãn "Đã duyệt" (status 5) + owner luôn sửa/xóa được → nhìn như "đã duyệt mà vẫn sửa/xóa".
- User chốt: **Đổi nhãn + khóa sau lưu** — phiếu KH lưu là chốt.
- BE `SupplyHandling`: `is_can_edit`/`is_can_delete` = owner && status == CHO_DUYET (bỏ nhánh KH luôn true → phiếu KH khóa ngay khi lưu); thêm `statusDisplay()` — KH + status 5 hiển thị "Đã xử lý" (nội bộ giữ "Đã duyệt"). 2 resource dùng nhãn mới; update()/destroy() tự khóa qua guard sẵn có.
- FE `constants.js`: dropdown lọc status 5 → "Đã duyệt / Đã xử lý". Nút Sửa/Xóa index gate theo flag BE (tự đúng).
- Luồng chốt: **Đề xuất** 1 Nháp (sửa/gửi/xóa) → 3 Đã gửi (xóa nếu chưa có PXL; handle_status: cho/dangxl/tuchoi). **PXL nội bộ** 3 Chờ duyệt (sửa/xóa bởi owner) → duyệt 5 / từ chối 7 (khóa). **PXL KH** lưu → 5 "Đã xử lý" (khóa ngay, chỉ Xem).

## Trạng thái "Đã xử lý xong" + trừ SL đã xử lý (2026-07-10, user chốt)

- **Rule 1 — Đề xuất tự chuyển "Đã xử lý xong"** (suy ra, không lưu cột): khi tổng SL đã phân bổ **KHÔNG tính cột 'mua'** (user chỉnh: chuyển mua chưa coi là đã xử lý — nhất quán cột "Đã xử lý" của bảng PXL; các PXL status != 7 — chờ duyệt vẫn tính, từ chối duyệt không tính) ≥ tổng SL đề xuất (> 0). Đề xuất chỉ mô tả lời → giữ "Đang xử lý". BE: `HANDLE_XONG` + `totalProposedQty()/totalHandledQty()/isFullyHandled()` trong entity; inbox filter thêm case xong/dangxl bằng whereRaw subquery (khớp accessor); eager thêm `products` ở index/inbox. FE: dropdown inbox thêm "Đã xử lý xong". Verify tinker: DXCU-2026-0001 (đề xuất 7 / xử lý-không-mua 6) → dangxl ✓; filter xong=0/dangxl=1 ✓.
- **Rule 2 — PXL mới trừ phần đã xử lý**: service `handledQtyByProduct($proposalId, $excludeHandlingId)` (1 query group by product). Detail đề xuất trả `sl_da_xu_ly`/dòng; detail PXL trả `sl_da_xl_truoc` (loại chính phiếu). FE prefill `dat_don = max(0, quantity − sl_da_xu_ly)`; bảng phân bổ thêm cột "Đã XL trước" (nhóm Số liệu nguồn). Giới hạn: hàng chọn thêm từ pool → sl_da_xl_truoc = 0 (pool không gắn đề xuất).

## Bổ sung theo spec ảnh (2026-07-10) — màn Lập phiếu xử lý

User chốt: export/import Excel để sau; tab "Thông tin hàng hóa" chỉ xem (join DB).
- BE: `SupplyHandlingService::productInfoMap($items)` join products + contract_products + ProductChemical/Device (whereIn, không N+1) → map product_id ⇒ {import_type, trade_name, contract_trade_name, specification, producer_country, note_quotation/bid_package/contract, special_note, chem_device}. Endpoint `POST supply/supply-handlings/product-info` (trước wildcard). Proposal DetailResource + Handling DetailResource(proposal) trả thêm `created_by_name` (show() eager `proposal.employee_create.info`).
- FE add.vue: `productInfoMap` nạp qua loadProductInfo (mounted + sau onPickConfirm); truyền xuống 2 component. Thêm field **Người đề xuất** (proposal.created_by_name).
- HandlingGoodsTable: đổi "Tên hàng"→**Tên thương mại** (dữ liệu phần mềm, hiện trade_name); thêm nhóm cột **Hàng hóa = NK/PPL** (pill); colspan tfoot +1.
- HandlingSummaryTabs: tab Tham chiếu HĐ thêm **Mã hàng hóa** + đổi tên→Tên thương mại (HĐ chuyển sang); **tab mới "Thông tin hàng hóa"** (Quy cách/Hãng nước SX/ghi chú báo giá-thầu-HĐ-đặc biệt/hóa chất-thiết bị).
- Verify: tinker productInfoMap trả data thật; route:list product-info trước wildcard; compile 3 file OK.
- TODO còn: **export/import Excel** bảng xử lý (tách task).

## Known limitations (có chủ đích)

- Số liệu nguồn hàng hóa (tồn kho/đang mua/vay/gửi/đổi) + `contract_code`/`sl_con_lai_hd` khi mở lại phiếu = 0/—; validate vượt HĐ chưa kích hoạt thực tế (chưa persist/chưa có nguồn). Wire sau.
- Chưa sinh chứng từ thật (xuất kho/mua/hóa đơn/xuất gửi) — chỉ lưu phân bổ + tab tổng hợp.
- Inbox list resource thiếu `files`/`sent_at` (dùng created_at, bỏ cột file ở inbox — người xử lý xem file ở màn tạo phiếu).
- Thông báo click chưa route tới màn chi tiết.
- `reason_deny`/`STATUS_TU_CHOI=7` của đề xuất giữ (deprecated, không set nữa).

## UI Polish (2026-07-13)

> Spec: `docs/superpowers/specs/2026-07-13-supply-ui-polish-design.md`

- [x] Polish `HandlingGoodsTable.vue`: bỏ 5-6 nền pastel nhóm cột → nền xám đồng nhất + gạch chân 2px theo nhóm (nguồn=cam, đặt đơn=xanh dương, xử lý=xanh lá, kết quả=tím); bỏ nền tím cột Kết quả; căn số nhất quán (mọi cột SL + input căn phải, header căn giữa).
- [x] `supply_handlings/add.vue`: ẩn `validationBanner` khi `isShow`.
- [x] Screenshot preview màn xử lý → user duyệt (2026-07-13, verify Playwright :8001).
- [x] Export Excel đẹp: thay `xlsx` (SheetJS, không style) → helper chung `utils/supply-excel-export.js` (ExcelJS, style theo Báo cáo bảo lãnh: tiêu đề merge, header xanh #4F81BD chữ trắng, viền mảnh, cột số căn phải #,##0, dòng tổng).
- [x] Export ĐỦ CỘT khớp bảng chi tiết: thêm Hàng hóa (NK/PPL) + nhóm Số liệu nguồn + header nhóm 2 tầng (Định danh/Số liệu nguồn/Xử lý cung ứng/Kết quả) qua `column.group` + merge. Tách `buildHandlingSrcCols`/`buildProposalSrcCols` ra constants dùng chung component (chống lệch cột). Verify file: xử lý 23 cột, đề xuất 9 cột, merge + dòng tổng khớp footer.
- [x] Header cột phân bổ thêm mô tả phụ (Mua hàng "chuyển đề xuất mua", Bán hàng "xuất HĐơn · xuất kho"...) — tách `allocColSub` ra constants dùng chung.
- [x] Đổi vị trí nút Export: từ trên thanh tab (hiện ở mọi tab) → vào TRONG tab đầu (Xử lý cung ứng hàng / Hàng hóa đề xuất), góc phải. Các tab khác không còn nút. Verify Playwright: hiện tab1, ẩn tab khác.

## Bugfix

- [x] Nút Export Excel màn chi tiết "không hiện": ROOT CAUSE = theme đặt `$secondary: $white` → `variant="outline-secondary"` render viền + chữ TRẮNG trên nền trắng = vô hình. Fix: đổi về `variant="secondary"` + đặt nút trên hàng `d-flex justify-content-end mb-2` ngay trên `HandlingSummaryTabs`, gỡ CSS cũ. Đã verify bằng Playwright (PXL-2026-0001) — nút hiện rõ, enabled.

## Bổ sung cột Đơn giá báo giá — tab Thông tin hàng hóa (2026-07-29)

- [x] Tab "Thông tin hàng hóa" (HandlingSummaryTabs) thêm cột **Đơn giá báo giá (gồm VAT)** — canh phải, chỉ loại KH (`!isInternal`), fmtNum, rỗng → '—'. Nguồn: `contract_products.price_quotation` (nhãn "Đơn giá báo giá (gồm VAT)" — snapshot báo giá trong HĐ).
- [x] BE `SupplyHandlingService::productInfoMap` — thêm `price_quotation` vào query contract_products + map trả về (`$cp ? $cp->price_quotation : null`). Chỉ có giá trị khi dòng gắn HĐ; hàng ngoài HĐ / nội bộ = null → FE hiện '—'.
- Ghi chú: ban đầu làm theo "Giá kế hoạch" (`bid_package_products.price_plan`) → user đổi sang "Đơn giá báo giá".

## Popup chi tiết phiếu — BC nhu cầu mua hàng (2026-07-29)

> Màn: `supply/reports/purchase-demand`. Cột "Phiếu đề xuất mua" có 2 mã: PXL (`handling_code`) + đề xuất gốc (`proposal_code`).

- [x] User chốt: bấm **cả 2 mã** đều mở popup chi tiết.
- [x] BE `SupplyReportService::purchaseDemand` — select thêm `sh.id as handling_id`, `sp.id as proposal_id`; mỗi `line` trả thêm `handling_id` + `proposal_id`.
- [x] FE `purchase-demand/index.vue`: 2 mã thành link (`.lnk`). Bấm PXL → `openHandlingDetail(id)` gọi `GET supply/supply-handlings/{id}` → modal `pdr-handling-modal` (header + bảng hàng hóa: đặt đơn / đề xuất mua / đã xử lý). Bấm đề xuất → `openProposalDetail(id)` gọi `GET supply/supply-proposals/{id}` → modal `pdr-proposal-modal` (header + bảng: SL đề xuất / đã xử lý). Có trạng thái loading, đọc `res.data.data`. Route show 2 endpoint không gắn permission → truy cập được.
- [x] Sửa giao diện popup theo mẫu `sale/report-project-contract`: dùng `b-modal` + `b-table-simple` (`modal-sticky-table`, header sticky), khối meta 2 cột (`popup-meta` — bảng `table-sm table-borderless`), khung cuộn `modal-table-scroll`, footer tổng số mặt hàng `modal-table-footer`. Thêm computed `handlingProducts`/`proposalProducts`. Bỏ CSS cũ `pdr-modal-loading`; thêm block non-scoped `.pdr-drill-modal .modal-body`.
- [x] Popup đề xuất đổi `size="lg"` → `size="xl"` cho bằng popup phiếu xử lý.

## Thêm 3 cột báo cáo — BC nhu cầu mua hàng (2026-07-29)

> Màn: `supply/reports/purchase-demand`, nhóm cột "Chi tiết đề xuất mua". Thêm: Mục đích, Cty thực hiện, Ngày đề xuất.

- [x] User chốt: **Cty thực hiện = công ty Bên A (main_company) của HĐ BÁN liên kết theo dòng** (`shp.contract_id` → `contracts.main_company.code`, = `contract_company`). Không dùng `company_id` trên phiếu (luôn null vì không set khi tạo).
- [x] BE `SupplyReportService::purchaseDemand`: select thêm `shp.contract_id`, `sp.purpose`, `sp.created_at as proposal_created_at`. Enrich `$companyByContract` = map contract_id → `optional(main_company)->code` (eager load `Contract::with('main_company')`, connection mysql2). Mỗi `line` trả thêm `purpose_name` (helper `purposeName` map `SupplyProposal::PURPOSES` 1 Tặng/2 Mượn, KH rỗng), `company_name`, `proposal_date` (`fmtDate` của created_at).
- [x] FE `purchase-demand/index.vue`: group header colspan 6→9; thêm 3 `<th>` (Mục đích / Cty thực hiện / Ngày đề xuất) + 3 `<td>` (`line.purpose_name` / `line.company_name` / `line.proposal_date`). Colspan dòng rỗng 15→18, 16→19. Excel export thêm 3 cột tương ứng (`purpose_name`, `company_name`, `proposal_date`).

## Link mã trong list PXL — supply_handlings (2026-07-29)

> Màn: `supply/supply_handlings` (list). Thêm link cho cột Mã PXL + Đề xuất gốc.

- [x] `SupplyHandlingResource` (list) sẵn có `supply_proposal_id` → dùng để link đề xuất gốc.
- [x] FE `supply_handlings/index.vue`: thêm cell template `code` (link `<a>` → `onViewClick` mở chi tiết PXL) và `proposal_code` (link → `onViewProposalClick` → `/supply/supply_proposals/add?mode=show&id={supply_proposal_id}`, guard theo `supply_proposal_id`, không có thì hiện text/'—'). Style `text-primary` mirror màn đề xuất.
