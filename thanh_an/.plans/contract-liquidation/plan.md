# Thanh lý hợp đồng — Plan

**Phụ trách:** @khoipv

## Phase 1 — Prototype HTML
- [x] Brainstorming + chốt bố cục (tab, có ô nhập tay, không chữ ký)
- [x] Viết spec chi tiết
- [x] Dựng `thanh_ly_demo.html`: CSS + DATA dùng lại từ bbnt_demo (2)
- [x] Bước 1 selector KH→HĐ + tóm tắt + KPI (auto chọn HĐ đầu)
- [x] Bảng danh sách lần nghiệm thu (BBNT)
- [x] Cấu hình thanh lý (ngày thanh lý nhập tay)
- [x] TẬP 1 — Tổng hợp hóa đơn (nhập Giá trị thanh toán → tính Còn chưa TT)
- [x] TẬP 2 — Chi tiết từng hóa đơn (phân bổ slNt vào hóa đơn, cộng theo HĐ)
- [x] TẬP 3 — Tổng hợp hàng hóa (SL HĐ vs thực hiện + chênh lệch)
- [x] Kết luận + banner đối chiếu
- [x] Actions (Lưu/Excel/In — ghost)

### Checkpoint — 2026-06-22
Vừa hoàn thành: dựng xong toàn bộ prototype `thanh_ly_demo.html`
Đang làm dở: không
Bước tiếp theo: user mở file trong trình duyệt verify UI; nếu OK bàn tích hợp BE
Blocked: (không)

## Phase 2 — Chỉnh sửa prototype theo feedback
- [x] Bỏ chữ "TẬP 1 / TẬP 2 / TẬP 3" trên 3 nút tab (giữ tên mô tả)
- [x] Thêm border đầy đủ (viền dọc + ngang) cho các ô th/td trong bảng cho dễ nhìn

## Phase 3 — Xây dựng thật (BE + FE, nối DB, có duyệt)

> Spec: `docs/superpowers/specs/2026-06-24-contract-liquidation-design.md`
> Plan chi tiết: `docs/superpowers/plans/2026-06-24-contract-liquidation.md`

- [x] Brainstorming + chốt 10 quyết định lớn
- [x] Viết spec chi tiết (2026-06-24)
- [x] Viết plan triển khai chi tiết (11 task)
- [x] BE Task 1 — Migration 4 bảng (review clean; 2 Minor: tên liquidation_invoice_id cố ý, gợi ý index để sau)
- [x] BE Task 2 — 4 Entities (review clean, fillable/relation khớp migration)
- [x] BE Task 3 — Service lõi `buildAggregation` (review clean; fix phòng thủ orphan cthd→unbilled; smoke test contract 198 OK, dvt='mL')
- [x] BE Task 4 — Service CRUD (review clean; fix key edit-flow khớp buildAggregation; transaction để controller Task 5)
- [x] BE Task 5 — Request + Controller + Routes (review clean; route:list 9/9; transaction store/update/delete)
- [x] BE Task 6 — Resources (list + detail) (review clean, verbatim BBNT pattern)
- [x] BE Task 7 — Seed 2 quyền (id 509/510, PermissionsTableSeeder + live DB) + smoke test toàn luồng PASS (contract 111: store→snapshot→detail key đúng→approve→selectable loại HĐ; đã cleanup)
- [x] FE Task 8 — helpers.js + Menu (controller tự làm: helpers + 2 menu chèn cạnh BBNT)
- [x] FE Task 9 — Trang danh sách + approve (review clean; mô phỏng BBNT; field khớp resource)
- [x] FE Task 10 — Form orchestrator + add/_id (review clean; fix BE thêm bbnt_list vào detail — verified preview+detail bbnt_list=1)
- [x] FE Task 11 — Components Summary + Tabs (review clean; reactivity + getPayloadInvoices OK)

### Checkpoint — 2026-06-24 (build hoàn tất)
Vừa hoàn thành: TẤT CẢ 11 task (BE 1–7, FE 8–11) + final whole-feature review + fix.
- BE verify end-to-end qua tinker (contract 111): store→snapshot→detail(key+bbnt_list đúng)→approve→selectable loại HĐ; đã cleanup.
- Final review fix: C1 (guard quyền cho `show`), I4 (eager-load `employee_create.info` chống N+1), + fix giữa chừng: orphan cthd→unbilled (Task 3), detail key khớp buildAggregation (Task 4), bbnt_list vào detail (Task 10).
Đang làm dở: không.
Bước tiếp theo (người dùng tự làm):
  1. Chạy `npm run dev` (client) verify UI thật: list, lập mới (chọn HĐ→preview→3 tab→nhập TT→lưu/gửi duyệt), chi tiết, duyệt/từ chối, xóa.
  2. Gán 2 quyền mới (`Duyệt biên bản thanh lý`, `Xem tất cả biên bản thanh lý`) cho role qua màn phân quyền.
  3. Commit (tôi không commit theo CLAUDE.md).
Ghi chú bàn giao (không chặn): I2 (giá trị thanh toán nhập vượt thực hiện không bị chặn — banner vẫn đúng); I3 (bbnt_list ở bản đã duyệt build live, số tài chính vẫn snapshot đúng).
Blocked: (không)

## Phase 4 — Đồng bộ UI form theo Biên bản nghiệm thu (BBNT)

> Yêu cầu user: "dùng form giống biên bản nghiệm thu". Form thanh lý đang dùng Bootstrap-Vue
> trơn (container-fluid + card + b-tabs + b-modal), chưa khớp shell/theme của `AcceptanceReportForm`.

- [x] Task 12 — `ContractLiquidationForm.vue`: đổi shell sang chuẩn BBNT
  - Wrapper `pages-container category-container contract-liquidation-form` + `readonly-view`
  - `PageHeader` + breadcrumb; loading-group
  - Alert "Lý do từ chối" khi status=4
  - 3 thẻ `.step` đánh số (1 chọn HĐ + summary, 2 thông tin BB, 3 đối chiếu + kết luận)
  - Footer `fixed-bottom` + `.footer.project` + `.equal-width`; nút "Lưu"/"Lưu và gửi|duyệt"
  - Modal `ConfirmReasonDeny` thay `b-modal`; mixin CheckPermission cho nhãn nút gửi
  - Bộ SCSS theme copy từ `AcceptanceReportForm` (scope `.contract-liquidation-form`)
- [x] Task 13 — `LiquidationSummary.vue`: dùng `.info` + `.kpi` + `.bar` + bảng BBNT theo theme
- [x] Task 14 — `LiquidationTabs.vue`: đổi `b-tabs`→`.subtabs`, bảng theo theme, banner `.foot/.banner`
- [x] Verify: `npm run dev` quan sát UI (đối chiếu trực quan với màn BBNT) — user verify PASS (2026-06-25)

## Phase 5 — Selector KH→HĐ dùng base-select2 (giống BBNT, như demo)

> Feedback user: demo có cho chọn khách hàng giống BBNT, nhưng form đang chỉ có 1 dropdown HĐ
> bằng `b-form-select` trơn, không dùng `base-select2` và thiếu chọn Khách hàng.

- [x] Task 15 — `ContractLiquidationForm.vue`: thêm cascade Khách hàng → Hợp đồng bằng `base-select2`
  - Thêm `selectedCustomerId` (chỉ để lọc, không gửi BE)
  - `customerOptions` dedupe theo `customer_id` từ `this.contracts` (giống Step1SelectContract BBNT)
  - `contractOptions` lọc theo `selectedCustomerId`, đổi format `{id,text}` cho base-select2
  - `onSelectCustomer(id)` reset HĐ + `loaded=false`; `onSelectContract(id)` nhận id param (ép Number)
  - Đổi 2 select sang `base-select2` (@input), HĐ disabled khi chưa chọn KH
  - API `selectable-contracts` đã trả sẵn `customer_id` + `customer_name` → không cần sửa BE

- [x] Task 16 — "Thời hạn thực hiện HĐ" giống BBNT (ưu tiên `time_progress`)
  - BE: thêm `time_progress` ($contract->time_progress) vào summary ở `ContractLiquidationService` (preview)
    và `ContractLiquidationDetailResource` (detail) — nhất quán preview/detail
  - FE `LiquidationSummary.executionTime`: copy logic BBNT → ưu tiên `time_progress (ngày)`,
    fallback `ngày ký – ngày kết thúc`, rồi `ngày kết thúc`
  - php -l 2 file OK; vue compile OK

## Phase 6 — Fix gốc bên BBNT: chặn trùng số hóa đơn (ảnh hưởng tổng hợp thanh lý)

> User phát hiện: nhập trùng số hóa đơn (vd 9100) ở 2 lần nghiệm thu khác nhau của cùng HĐ →
> dữ liệu tổng hợp bên thanh lý sai. Chốt: chặn trùng **trong cùng 1 hợp đồng**, áp dụng **mọi
> loại có nhập số HĐ** (Tổng HĐ/Chi tiết HĐ: `acceptance_report_invoices.so`; theo hàng/tháng/lũy kế:
> `acceptance_report_items.so_hd`).

- [x] Task 17 — `AcceptanceReportService`: thêm `assertNoDuplicateInvoiceNumbers()` + 2 helper
  (`collectInvoiceNumbers` gom số HĐ theo loại; `existingInvoiceNumbers` truy số đã dùng ở BBNT khác
  cùng HĐ, gồm cả invoices.so lẫn items.so_hd). Bỏ qua BBNT đã từ chối (status=4) và (khi sửa) chính nó.
  - Chặn 2 lớp: trùng trong cùng biên bản + trùng với biên bản khác cùng HĐ
  - Gọi trong `store()` (exclude null) và `update()` (exclude $report->id)
  - php -l OK. Payload luôn có `type` (buildPayload spread formSubmit) → collect đúng nhánh.

- [x] Task 18 — Cảnh báo trùng số HĐ **inline ngay dưới ô số hóa đơn** (real-time, mọi loại)
  - BE: `GET acceptance_reports/contract/{contract}/used-invoice-numbers?exclude_report_id=` →
    `AcceptanceReportService::usedInvoiceNumbers()` (public, bọc `existingInvoiceNumbers`). Route + controller.
  - FE helpers: `normInvoiceNo`, `dupInvoiceNoSet(values, used)` (trùng nội bộ HOẶC đã dùng ở BBNT khác).
  - FE `AcceptanceReportForm`: state `usedInvoiceNos` + `loadUsedInvoiceNos()` gọi ở onContractLoaded (create)
    và loadReport (edit/show, exclude reportId); truyền prop xuống Step3Detail → các form.
  - Inline `is-invalid` + `invalid-feedback`: FormByInvoiceTotal (so), FormByInvoiceDetail (block.so),
    ProductGrid (so_hd cho thang + mathang). Forward prop qua FormByMonth/FormByProduct.
  - Lý do dùng client-side fetch thay vì map lỗi BE theo index: `buildDetailItems()` lọc sl>0 nên
    index submit ≠ index dòng lưới → không map được; client-side real-time chính xác hơn. BE block giữ chốt cứng.
  - php -l 3 file OK; vue compile 7 file OK; helpers.js parse OK.

- [x] Task 19 — Fix tổng hợp thanh lý bỏ sót số HĐ của loại "theo mặt hàng" (mathang)
  - Triệu chứng: BBNT loại mathang nhập so_hd (vd 1972/1978) ở dòng hàng → tab TẬP 1/TẬP 2 thanh lý
    không hiện vì `buildInvoices` dồn toàn bộ mathang vào "chưa gắn hóa đơn", bỏ qua so_hd.
  - Fix `ContractLiquidationService::buildInvoices`: gộp nhánh THANG + MATHANG, gom theo (so_hd + ngày)
    tạo dòng hóa đơn; item thiếu so_hd mới vào "chưa gắn". Chỉ LUYKE (không có so_hd) vào "chưa gắn".
  - Thêm hằng `SRC_MATHANG = 'mathang'` + label "Theo mặt hàng"; cột source_type là string (lưu OK),
    cập nhật comment migration.
  - php -l 2 file OK. (Áp dụng cho preview + lần lưu mới; bản thanh lý đã lưu trước đó cần lập lại.)

- [x] Task 20 — Bổ sung cột bảng hàng hóa thanh lý (TẬP 2 + TẬP 3) giống bảng BBNT
  - BE `ContractLiquidationService`: thêm `productInfoMap($contract)` (code/trade_name/origin_name/spec/dvt
    từ ContractProduct theo product_id). Bơm vào `mapItems` (TẬP 2) + bổ sung field trong `buildGoods` (TẬP 3).
  - Detail (snapshot): enrich live trong `loadAggregateForDetail` (các cột mô tả phi tài chính, không cần thêm cột DB).
  - FE `LiquidationTabs`: TẬP 2 thêm Tên TM / Mã NSX / Hãng-nước SX / ĐVT / Quy cách; TẬP 3 thêm Tên TM /
    Hãng-nước SX / Quy cách. Cập nhật colspan (10 / 13).
  - php -l OK; vue compile OK.

- [x] Task 21 — Thêm cột "SL mua thêm" (= annex_qty) vào TẬP 3 Tổng hợp hàng hóa
  - BE buildGoods: cộng dồn `sl_pl` từ `$cp->annex_qty`. Detail: `annexQtyByProduct()` map live theo product_id
    (lấy từ contract_products hiện tại — theo ghi nhớ không tin snapshot v0). Không thêm cột DB.
  - FE LiquidationTabs TẬP 3: thêm cột "SL mua thêm" sau "SL hợp đồng"; colspan 13→14.
  - php -l OK; vue compile OK.

## Phase 7 — Cập nhật bổ sung (ngày thanh lý + file lưu trữ) giống BBNT

> Yêu cầu user: bổ sung chức năng update bổ sung ngày thanh lý & file lưu trữ ở mọi trạng thái,
> mô phỏng `updateSupplement` của BBNT (independent: chỉ gửi date hoặc chỉ gửi files).

- [x] Task 22 — BE: bảng + entity file
  - Migration `contract_liquidation_files` (đã chạy; cột id, contract_liquidation_id, ten_tai_lieu, link,
    ten_file, ghi_chu, timestamps, index) — verify Schema::hasTable OK
  - Entity `ContractLiquidationFile`; relation `files()` + `canSupplement()` (owner|PERM_APPROVE) trên ContractLiquidation
- [x] Task 23 — BE: service + controller + route + request + resource
  - Service: `updateSupplement` (has() từng phần), `assertCanSupplement`, `saveFiles` (xóa hết + insert lại);
    lưu files trong store + update(has files); delete() xóa files
  - Controller `updateSupplement` (DB::transaction); route POST `/{contract_liquidation}/updateSupplement` (route:list OK)
  - `UpdateContractLiquidationSupplementRequest`; DetailResource thêm `can_supplement` + `files`; show load 'files'
  - Store Request thêm validate `files.*`
- [x] Task 24 — FE: form + component file
  - `LiquidationFiles.vue` (mô phỏng SupplementUpdate.vue; mutate form.files; upload S3)
  - Form: `form.files`, `can_supplement`; computed supplementEditable/showSupplementSave;
    nút "Lưu ngày" + "Lưu file lưu trữ" khi readonly & canSupplement; main submit kèm files; loadDetail nạp files
  - php -l toàn bộ OK; vue compile 2 file OK

### Checkpoint — 2026-06-25 (Phase 7 — cập nhật bổ sung ngày + file)
Vừa hoàn thành: Task 22–24. Build chức năng cập nhật bổ sung ngày thanh lý + file lưu trữ ở mọi trạng thái,
mô phỏng `updateSupplement` của BBNT. BE: bảng+entity file, relation+canSupplement, service updateSupplement/
saveFiles, controller+route+request+resource (can_supplement+files). FE: LiquidationFiles.vue + form (nút Lưu
ngày/Lưu file khi readonly&canSupplement, main submit kèm files). Migration đã chạy, route đăng ký OK.
Bước tiếp theo (người dùng tự làm): npm run dev verify — tạo TL có file → lưu; mở bản đã duyệt → sửa ngày/file
qua nút bổ sung; kiểm tra phân quyền (owner / người có quyền duyệt mới thấy nút).
Blocked: (không)

### Checkpoint — 2026-06-25 (Phase 8 — fix UI + bug lưu thanh toán mathang)
- [x] Task 25 — FE: cột "Giá trị thanh toán" + "Ghi chú" tab Tổng hợp HĐ giống BBNT
  - LiquidationTabs.vue: đổi input number → `currency-input class="text-right w-100"`; ghi chú → `textarea form-control rows=2`
- [x] Task 26 — BE FIX: giá trị thanh toán hóa đơn MATHANG không lưu khi sửa
  - Nguyên nhân: `detailRowKey` chỉ tái tạo key cho THANG, MATHANG rơi vào `'inv:'+null` → không khớp
    key `mathang:<reportId>:<so>|<ngay>` của buildAggregation → snapshot map paid=0 → mất giá trị
  - Sửa: detailRowKey xử lý cả MATHANG (prefix theo source_type). php -l OK
Bước tiếp theo (người dùng tự làm): mở lại TL #3 → nhập lại giá trị TT cho 1972/1978 → lưu → vào lại kiểm tra.

### Checkpoint — 2026-06-25 (Phase 9 — bỏ "đ" bảng hàng hóa + bắt buộc ngày thanh lý)
- [x] Task 27 — FE: bỏ ký tự " đ" mọi giá trị tiền trong bảng hàng hóa (Thành tiền TẬP 2 + TT HĐ/TT thực hiện TẬP 3) → đổi fmtMoney → fmtNum
- [x] Task 28 — Rà soát phân quyền vs nghiệm thu: kết luận đã mirror 1:1 (perm const/seed 509-510, entity, service guard, controller, resource flag, menu isShow, FE v-if). Không thiếu.
- [x] Task 29 — Validate bắt buộc nhập ngày thanh lý (giống nghiệm thu acceptance_date required)
  - BE: StoreContractLiquidationRequest `liquidation_date` → `required|date` + message
  - FE: data.dateError + báo đỏ dưới ô ngày; chặn submit() & saveLiquidationDate() khi rỗng;
    catch 422 map errors.liquidation_date; style .date-invalid .mx-input border đỏ; @change clear lỗi
  - php -l OK; vue compile OK
- [x] Task 30 — Dùng base components cho ô ngày thanh lý (giống Step2Config nghiệm thu)
  - `<date-picker>` → `<base-date-picker>`; label thêm `<Required />` (dấu * đỏ); lỗi dùng `<base-helper-error :error="dateError" />`
  - Gỡ import/registration DatePicker thừa; thêm watch form.liquidation_date clear dateError (base-date-picker emit input, không có change)
  - BE đã enforce `required|date` từ Task 29. vue compile OK
Bước tiếp theo (người dùng tự làm): npm run dev — lưu TL bỏ trống ngày → phải báo "Vui lòng nhập ngày thanh lý".
- [x] Task 31 — Màn danh sách: thêm cột "Người tạo"
  - BE đã sẵn (resource trả `creator`, index eager-load employee_create.info). Chỉ thêm field `creator` vào fields index.vue (giữa Còn nợ và Trạng thái).

### Checkpoint — 2026-06-25 (Phase 5 — selector KH→HĐ base-select2)
Vừa hoàn thành: Task 15. Thêm chọn Khách hàng (cascade KH→HĐ) dùng `base-select2` đúng pattern BBNT
(`Step1SelectContract.vue`): customerOptions dedupe theo customer_id, contractOptions lọc theo KH +
format `{id,text}`, onSelectCustomer reset HĐ, onSelectContract(id) ép Number. Bỏ `b-form-select` trơn.
Verify: vue-template-compiler + new Function(script) compile clean.
Đang làm dở: không.
Bước tiếp theo (người dùng tự làm): `npm run dev` xem lập mới — chọn KH → HĐ lọc đúng → preview.
Blocked: (không)

### Phase 5 — Hiển thị mã KH ở dropdown chọn khách hàng (2026-07-01)
Yêu cầu user (@khoipv): màn `add` — dropdown chọn KH không hiện mã KH; sửa giống màn nghiệm thu ("mã — tên").
Nguyên nhân: endpoint `selectable-contracts` của thanh lý không trả `customer_code`; FE chỉ dùng `customer_name`.
- [x] BE `ContractLiquidationService::selectableContracts`: leftJoin `category_customers as cus` + select `cus.code as customer_code` (đồng nhất `AcceptanceReportService`).
- [x] FE `ContractLiquidationForm.vue`: `customerOptions` dùng `customerLabel(customer_code, customer_name)`; thêm method `customerLabel` (copy từ `Step1SelectContract`).

### Phase 6 — Bỏ điều kiện HĐ phải có BBNT đã duyệt mới được thanh lý (2026-07-01)
Yêu cầu user (@khoipv): màn `add` — cho chọn cả HĐ chưa có biên bản nghiệm thu (bỏ ràng buộc "đã có BBNT đã duyệt"). Giữ các điều kiện khác: do mình lập + chưa thanh lý.
- [x] BE `selectableContracts`: bỏ `whereExists(acceptance_reports DA_DUYET)`.
- [x] BE `store`: bỏ gọi `assertHasApprovedReport`; xóa luôn method (dead code). Import `AcceptanceReport` vẫn giữ (preview tổng hợp còn dùng); HĐ không BBNT → phần tổng hợp = rỗng/0, không lỗi.
- [x] FE `ContractLiquidationForm.vue`: sửa hint còn "Chỉ hiển thị hợp đồng do bạn lập và chưa thanh lý."

### Checkpoint — 2026-06-24 (Phase 4 — đồng bộ form theo BBNT)
Vừa hoàn thành: Task 12–14. Rework 3 file FE form thanh lý sang đúng shell + theme BBNT:
- `ContractLiquidationForm.vue`: `pages-container category-container contract-liquidation-form` +
  `PageHeader`/breadcrumb + loading-group + alert lý do từ chối (status=4) + 3 thẻ `.step` đánh số +
  footer `fixed-bottom .footer.project .equal-width` + modal `ConfirmReasonDeny` (thay `b-modal`) +
  mixin CheckPermission (nhãn "Lưu và duyệt"/"Lưu và gửi") + SCSS theme copy từ AcceptanceReportForm.
- `LiquidationSummary.vue`: `.info` strip + `.kpi` + `.bar` + bảng `.ltable` (bỏ card/b-table/b-progress).
- `LiquidationTabs.vue`: `.subtabs` (thay `b-tabs`) + bảng `.ltable` + input `.cell` + banner `.foot/.banner`.
- Logic giữ nguyên 100% (preview/detail/submit/approve/reject/getPayloadInvoices).
- Verify: vue-template-compiler compile 3 template OK; node --check 3 script OK.
Đang làm dở: không.
Bước tiếp theo (người dùng tự làm): `npm run dev` xem UI form (lập mới + chi tiết + duyệt/từ chối),
đối chiếu trực quan với màn BBNT; gán 2 quyền; commit.
Blocked: (không)
