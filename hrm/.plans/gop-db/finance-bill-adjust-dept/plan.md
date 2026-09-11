# Plan — Phiếu kế toán (ERP `bill_adjust_dept` → HRM)

> Phụ trách: @khoipv · Nhánh: `gop_db` (cả 2 repo) · Bắt đầu: 2026-08-28
> Design: `design.md` · Spec: `docs/superpowers/specs/gop-db/2026-08-28-finance-bill-adjust-dept-design.md`

---

## Phase 1 — Nền BE (entity, morphMap, quyền, route)

- [x] 1.1 Entity `BillAdjustDept` — bảng `bill_adjust_depts`, hằng trạng thái (Đang tạo = **xám**), quan hệ, accessor `is_can_view/is_can_edit/is_can_delete/status_text/status_type`
- [x] 1.2 Entity `BillAdjustDeptDetail` — bảng `bill_adjust_dept_details`, morphTo `contractable` + `objectable`
- [x] 1.3 Sinh mã `<mã cty>.PKT<mm><yy>.<5 số>` bọc transaction + `lockForUpdate`
- [x] 1.4 Bổ sung **4 morphMap** `objectable`: Customer / Supplier / Employee / Department
- [x] 1.5 Thêm **2 quyền guard `api`** vào `PermissionsTableSeeder` (tổng công ty / công ty)
- [x] 1.6 Khai 15 route (route tĩnh đặt TRƯỚC `/{id}`), gắn `checkPermission:Kế toán thanh toán` cho route ghi

## Phase 2 — Đọc: danh sách + chi tiết

- [x] 2.1 `BillAdjustDeptService::search()` — 12 ô lọc + phạm vi quyền 2 cấp + ẩn phiếu *Đang tạo* của người khác
- [x] 2.2 `BillAdjustDeptResource` (danh sách) + `DetailBillAdjustDeptResource` (chi tiết)
- [x] 2.3 `show()` gate bằng `is_can_view`, không qua → 403
- [x] 2.4 Kiểm chứng phạm vi quyền bằng SQL đếm theo 3 nhánh, so với số dòng API trả

## Phase 3 — Ghi: tạo / sửa / xóa (chưa duyệt)

- [x] 3.1 `BillAdjustDeptStoreRequest` + `UpdateRequest`
- [x] 3.2 `BillAdjustDeptWriteService::validateDetails()` — 5 luật theo nhóm định khoản
- [x] 3.3 `syncDetails()` — ghi 38 cột chi tiết + tính `total_amount`
- [x] 3.4 `store()` / `update()` — validate **trước** khi tạo phiếu; chặn nhảy cóc trạng thái
- [x] 3.5 `destroy()` — gate `is_can_delete`, trả trạng thái phiếu nguồn về *Chờ duyệt*
- [x] 3.6 Đính kèm file S3 (nối attachment của đề nghị nguồn khi có)
- [x] 3.7 Test 5 luật validate × ca đúng/sai

## Phase 4 — Ghi sổ cái (phần rủi ro nhất)

- [x] 4.1 `BillAdjustDeptAccountingService::buildEntries()` — **hàm thuần**, không DB / không `auth()`
- [x] 4.2 `persist()` — chỉ insert `account_details` + `account_detail_refs`
- [x] 4.3 3 nhánh `billable_*` (đầu kỳ / ProductExport / BorrowSell) — kiểm null từng bước
- [x] 4.4 `syncAdjustedMoneyBillIncomeReport()` — cộng `money_adjusted` cho dòng Phiếu báo có
- [x] 4.5 `processApproved()` — 5 bước đúng thứ tự ERP, bọc 1 transaction
- [x] 4.6 `BillAdjustDeptNotifyService` — thông báo chuông theo template `[PREFIX] {Nhóm hành động}: {Tên}. {Ghi chú}`
- [x] 4.7 **Unit test `buildEntries()`** với nhóm định khoản lấy từ phiếu ERP thật, so từng dòng sổ cái
- [x] 4.8 Chạy thử vòng đời đầy đủ trên dữ liệu thật, **bọc transaction rồi rollback**

## Phase 5 — Số dư lẻ + 5 cửa vào

- [x] 5.1 `BillAdjustDeptOddBalanceService::check()` — gom nhóm, so `companies.adjust_odd_balance`
- [x] 5.2 Sinh cặp bút toán đề xuất (Nợ 811/Có 1311 · Nợ 1311/Có 711), gắn `cost_debt` `DCSDCNKH`
- [x] 5.3 Cửa vào 2 — nạp từ Phiếu YCĐC, mặc định TK 1311, ẩn cột nhóm định khoản
- [x] 5.4 Cửa vào 3 — nạp từ Hạch toán bổ sung, copy `type`, ẩn cột phiếu YCXH khi `type = 7`
- [x] 5.5 Cửa vào 4 — nạp từ Hạch toán hoa hồng tháng *(màn nguồn chưa port — chỉ deep-link)*
- [x] 5.6 Cửa vào 5 — nạp từ Chi phí giao nhanh + cập nhật cờ đã hạch toán *(màn nguồn chưa port)*
- [x] 5.7 3 endpoint popup: `search-objects` · `search-contracts` (gộp `hrm_contracts` + `firm_contracts` + 6 loại ERP) · `search-export-requests`

## Phase 6 — In & xuất Excel

- [x] 6.1 `BillAdjustDeptPrintService` — letterhead theo **`company_id` trên chứng từ** (khuôn `BillIncomePrintService::headerUrl()`)
- [x] 6.2 `BillAdjustDeptExport` — Excel chi tiết 1 phiếu, ô tiền dạng số + data-format
- [x] 6.3 `BillAdjustDeptListExport` — Excel danh sách, BE trả đủ trường của `ExportFieldsModal`

## Phase 7 — FE màn danh sách

- [x] 7.1 `pages/finance/bill-adjust-depts/index.vue` — 4 mixin, `localStorageKey` + `columnScreenKey` duy nhất
- [x] 7.2 12 ô lọc bằng `V2BaseSmartFilterPanel` + schema `filterFields`
- [x] 7.3 11 cột + căn lề SRS + `V2BaseBadge` qua `utils/statusBadgeVariant.js`
- [x] 7.4 `getRowActions()` — Sửa → Xóa → In → Xuất Excel, gate bằng cờ BE, handler `switch (action)`
- [x] 7.5 Toolbar: Tạo mới → Xuất Excel → Cấu hình cột (không có Import)
- [x] 7.6 Thêm mục menu vào `components/subsystem-menu/`

## Phase 8 — FE form + chi tiết + in

- [x] 8.1 `BillAdjustDeptForm.vue` — dùng chung cho tạo / sửa / chi tiết
- [x] 8.2 Khối thông tin chung + đổi loại tiền → tính lại toàn bộ cột quy đổi
- [x] 8.3 Bảng chi tiết 18 cột, header 2 tầng khi ngoại tệ, nhập Nợ tự xóa Có
- [x] 8.4 3 popup — select trong popup dùng `V2BaseSelectInModal`
- [x] 8.5 Khối tick "số dư lẻ"
- [x] 8.6 `create.vue` · `_id/index.vue` · `_id/edit.vue` (3 file mỏng) + `unsavedChangesMixin`
- [x] 8.7 `_id/print.vue` — khổ ngang, bố cục mẫu ERP id 208
- [x] 8.8 Cờ quyền **fail-closed** — mọi cờ khởi tạo `false`, chỉ set từ `$store.state.permissions` hoặc field BE

## Phase 9 — Kiểm chứng & dọn

- [x] 9.1 Seeder dữ liệu test (khuôn `TEST.DNDCCN.*`) — có phiếu *Đang tạo* để bấm thử sửa/xóa
- [x] 9.2 Chạy 6 lệnh grep tự kiểm của skill `erp-to-hrm-screen` trên cả thư mục feature
- [x] 9.3 Compile sạch toàn bộ file FE (`vue-template-compiler` + babel — repo **không có ESLint config**)
- [x] 9.4 Đối chiếu ngược với ERP: đủ cột / đủ ô lọc / đủ hành động **và điều kiện ẩn hiện**
- [x] 9.5 Bàn giao user mở trình duyệt bấm thật — báo rõ phần chưa kiểm chứng

---

## Checkpoint — 2026-08-28

Vừa hoàn thành: **toàn bộ BE + FE của màn Phiếu kế toán** (Phase 1-9, trừ 9.1 và 9.5).

**Đã kiểm chứng bằng dữ liệu thật:**
- **Ghi sổ cái**: `buildEntries()` chạy trên **150 phiếu ERP ngẫu nhiên / 403 dòng bút toán**,
  so **33 cột** + toàn bộ `account_detail_refs` → **khớp tuyệt đối 150/150**.
  (Vòng đối chiếu đầu bắt được 2 lỗi thật, đã sửa: `optional(null)` trả object nên nhánh dự phòng
  người lập không chạy — 58 dòng lệch `company_id`/`department_id`; và entity hợp đồng của HRM
  không có quan hệ `employee_create` như `App\BaseModel` của ERP nên `created_by` lấy nhầm người
  lập phiếu — 280 dòng lệch.)
- **Phạm vi quyền**: 3 nhánh (tổng công ty / công ty / chỉ phiếu mình lập) + Super admin đối chiếu
  SQL → khớp 6/6 nhân viên thật.
- **Vòng đời**: lưu nháp → sửa → duyệt (ghi 2 bút toán + 2 dòng đối ứng) → chặn sửa/xoá phiếu đã
  duyệt (403). Bọc transaction rồi rollback, 0 dòng sót lại.
- **4/5 luật validate** nhóm định khoản: chặn đúng, ca hợp lệ lưu được. Luật 2 (vượt tiền Phiếu
  báo có) chưa dựng được ca thật.
- **10 endpoint** smoke test qua HTTP kernel: 200 hết. Popup hợp đồng trả đúng 372 hợp đồng
  (368 HĐ bán + 4 nguồn khác) cho khách hàng có dữ liệu.
- **FE**: 9/9 file compile sạch (`vue-template-compiler` + babel); 5 lệnh grep tự kiểm của skill
  `erp-to-hrm-screen` sạch tuyệt đối.

- [x] Ô **Tỷ giá** ở khối thông tin ép `text-align: left` (user chốt 2026-09-07): ô kiểu số nên
      Excel tự canh phải, lệch khỏi cột giá trị của các dòng thông tin bên trên. GIỮ ô kiểu số +
      `data-format`, chỉ đổi canh lề — đừng đổi sang chuỗi để canh trái.

- [x] Header "Thông tin chung" nền xám trên server, trắng ở local (user báo 2026-09-07):
      `BillAdjustDeptForm.vue` dùng class `card-header section-header` nhưng KHÔNG khai rule.
      Rule chỉ nằm ở `V2BaseFormSection.vue` / `CustomerForm.vue` (style non-scoped = toàn cục
      nhưng chỉ nạp khi component đó được load) — kiểm 4 bundle nền của server: 0/4 có rule.
      Đi từ màn khác sang thì rule đã nằm sẵn trong DOM (local), mở thẳng URL thì không (server).
      Sửa: khai rule trong scoped style của chính màn, y như `AccountingDetailTable.vue` :508.
      ⚠️ CÒN 5 FILE cùng lỗi, chưa sửa (chờ user quyết): 3 file màn Đề nghị hạch toán bổ sung
      (`AdditionAccountingRequestForm` · `AdditionDetailTable` · `CoordinationDetail`) và 2 file
      màn Báo cáo phiếu thu (`BillIncomeReportForm` · `bill-income-reports/_id/index.vue`).

- [x] Nút **"Lưu" → "Lưu nháp"**; lưu nháp chỉ bắt buộc **Ngày hạch toán** (user chốt 2026-09-07).
      Chỗ chặn thật nằm ở `BillAdjustDeptWriteService::store()/update()` gọi `validateDetails()`
      cho MỌI trạng thái → nháp chưa thêm dòng nào cũng 422 *"phải có ít nhất một dòng định
      khoản"*. Sửa: tách `validateDetailsWhenApproving()`, 5 luật cân bút toán chỉ chạy khi
      `status = 2`. Kèm: `type_money_id` + `exchange_rate` chỉ bắt buộc khi duyệt;
      `headerAttributes()` đổi sang `?:` để `null` FE gửi lên không thành `0` ở 2 cột NOT NULL
      (mặc định VNĐ + tỷ giá 1). FE bỏ chặn Loại tiền ở nhánh nháp.
      Kiểm bằng API: nháp chỉ có ngày → 200 (DB ra VNĐ/1/note rỗng/0 dòng) · nháp gửi null → 200 ·
      thiếu ngày → 422 · duyệt phiếu rỗng → 422 · duyệt lệch nợ/có → 422.
      ⚠️ GIỮ NGUYÊN `details.*.account_id` required: cột NOT NULL trên bảng dùng chung ERP, bỏ rule
      là nổ SQL 500 thay vì 422. Muốn nháp lưu được dòng chưa chọn TK thì phải migration.

- [x] Bảng Chi tiết ở màn Thêm mới (`AccountingDetailTable.vue`) — user yêu cầu 2026-09-07:
      · thêm cột **Mã khế ước** giữa *Mã vụ việc* và *Ngân hàng* (đúng vị trí ERP `form.blade.php`
        :266). Ô ĐỂ TRỐNG vì ERP cũng để trống cứng (:407 `<td></td>`, không input, không dữ liệu)
        — khớp luôn với file Excel chi tiết. `columnCount` 16 → 17.
      · **ghim 3 cột đầu** (STT · Số tài khoản · Tên tài khoản) theo khuôn `BomBuilderTableCard.vue`
        :1356: bề rộng chốt cứng 50/170/200px (left cộng dồn — để min-width là 2 cột ghim chồng
        nhau), nền đục + `background-clip: padding-box`, vạch ngăn 2px ở cột Tên tài khoản.
      Đã đếm lại ô: thead hàng 1 và mỗi dòng body khớp 18 cột (VNĐ) / 20 cột (ngoại tệ).
      Bản in KHÔNG đổi — mẫu in ERP (report_templates 208) chỉ 9 cột, không có Mã khế ước.

- [x] Tải file đính kèm luôn 422 `{"files":["Bắt buộc phải nhập"]}` (user báo 2026-09-07):
      `BillAdjustDeptController::uploadFiles()` validate khoá **`files`**, trong khi khối đính kèm
      là component DÙNG CHUNG `bill-payment-requests/components/AttachmentSection.vue` gửi
      **`attachments[]`**. Kèm lỗi thứ 2 ngay sau đó (chưa lộ vì bị chặn trước): BE trả
      `data.urls[]` còn component đọc `response.data[0]` → "Upload không trả về đường dẫn file".
      Sửa cả 2 theo khuôn `BillPaymentRequestController::uploadFiles()`: nhận `attachments[]`,
      message tiếng Việt, trả THẲNG mảng URL vào `data`.
      Kiểm bằng multipart thật: `attachments[]` → 200 kèm URL S3 · `files[]` → 422. File test đã
      xoá khỏi S3. CHỈ sửa BE, FE không phải build lại.

- [x] Hiển thị lỗi dùng BASE CHUNG + validate Diễn giải dòng (user yêu cầu 2026-09-07):
      · thay 5 khối tự chế `<div class="invalid-feedback d-block">` bằng **`V2BaseError`**
        (3 ở `BillAdjustDeptForm`, 2 ở `AccountingDetailTable`). Quan trọng ngoài thẩm mỹ:
        `utils/scrollToFirstError` tìm ô lỗi theo class `.v2-error`, khối tự chế nó KHÔNG thấy.
      · ô **Diễn giải** trong bảng chi tiết: header có dấu `*` từ đầu nhưng KHÔNG chỗ nào kiểm.
        Nay FE tô đỏ + `V2BaseError` theo dòng khi `touched`, chặn sớm ở `validateBeforeSubmit`;
        BE `details.*.note` bắt buộc KHI DUYỆT (ERP bắt buộc luôn), nháp vẫn trống được.

- [x] ⚠️ LỖI NẶNG lộ ra khi kiểm chứng: **"Lưu và duyệt" bỏ qua TOÀN BỘ rule `required`**.
      `BillAdjustDeptStoreRequest::rules()` đọc trạng thái bằng `$this->get('status')` — `get()`
      của Symfony KHÔNG đọc JSON body (FE gửi JSON) → luôn null → rơi về mặc định "Đang tạo" →
      `$isDraft = true` → `note` / `type_money_id` / `details` min:1 / `details.*.note` / tỷ giá
      ngoại tệ đều bị nới. Đo thật: duyệt phiếu có dòng trống diễn giải → HTTP 200 + GHI SỔ CÁI.
      Sửa: `$this->input(...)`. Kiểm lại: duyệt thiếu diễn giải → 422 `details.0.note`; nháp → 200.
      Cùng bẫy đã ghi ở `ProductTransferFormRequest` :33.
      ⚠️ CÒN **18 FormRequest** khác toàn dự án vẫn dùng `$this->get()` (Finance 7 · CustomerCare 7
      · Payroll 4), ít nhất 5 file dùng để tính `$isDraft` — KHÔNG sửa (màn của người khác), cần
      báo team.
      Dọn dẹp: phiếu duyệt lọt `TPE.PKT0926.00002` đã xoá kèm 2 dòng `account_details`
      (id 1001586-1001587, lọc theo `invoiceable_code`). Còn phiếu nháp `TPE.PKT0926.00001`
      (id 12862) — KHÔNG xoá, nghi là phiếu user tự bấm thử trên trình duyệt.

- [x] Popup "Chọn phiếu YCĐC": lọc theo Người lập rồi XOÁ lọc → lăn chuột **giật giật / không
      cuộn được**, F5 mới hết (user báo + quay video 2026-09-07). Sửa ở **component DÙNG CHUNG**
      `components/V2BaseSelectInModal.vue` (user đồng ý).
      **Nguyên nhân gốc** — select2 4.0.13 `dropdown/attachBody` (:4441-4451): khi MỞ dropdown nó
      ghi lại vị trí cuộn của mọi cha có thanh cuộn rồi gắn `scroll.select2.<id>` để **kéo về vị
      trí đó mỗi lần cuộn** (cho dropdown khỏi trôi), chỉ gỡ ở sự kiện `close` (:4348). Mà
      `_detachPositioningHandler` lọc lại cha bằng `Utils.hasScroll` (:712-735) — hàm này tính theo
      NỘI DUNG TẠI THỜI ĐIỂM GỌI. Chuỗi gây lỗi:
        1. mở dropdown lúc danh sách còn dài → `.v2-modal-body` có cuộn → GẮN handler ghim
        2. chọn 1 người lập → còn 1 dòng → `.v2-modal-body` HẾT cuộn
        3. select2 đóng dropdown → `hasScroll` không thấy `.v2-modal-body` → **KHÔNG gỡ**
        4. bỏ lọc → danh sách dài lại → handler cũ ghim `scrollTop` → giật giật
      `b-modal` giữ DOM popup nên mở lại popup vẫn dính, chỉ F5 mới sạch.
      **Cách sửa**: thêm `releaseScrollLock()` — đóng dropdown nếu còn mở, rồi
      `$(this.$el).parents().off('scroll.select2')` (quét MỌI cha, KHÔNG lọc theo `hasScroll` —
      lọc là dính đúng cái bẫy trên), có guard bỏ qua khi còn dropdown khác đang mở. Gọi ở
      `onClose` (hoãn 1 nhịp), `beforeDestroy`, và trước `renderKey++`.
      **Đo trên trình duyệt** (local, viewport ép 1280×560 cho popup phải cuộn):
        · trước sửa: đặt `scrollTop = 50` → đọc 43 → 700ms sau về **0**; lăn 8 nấc × 60px vẫn 0
        · sau sửa: đặt 50 → 700ms sau vẫn **50**; lăn chuột thật `scrollTop = 200`; lặp 3 vòng
          chọn-xoá vẫn sạch
        · hồi quy: dropdown ĐANG MỞ vẫn ghim cuộn (đúng hành vi gốc select2), chọn option bình thường
      ⚠️ `V2BaseSelect.vue` / `V2BaseSelectRemote.vue` (select NGOÀI modal) dùng cùng select2 nên
      về lý thuyết dính y hệt khi đặt trong vùng cuộn co giãn — CHƯA sửa, chờ user quyết.

- [x] Popup "Chọn phiếu YCĐC" — 3 yêu cầu nhỏ của user (2026-09-07):
      · đổi nhãn **Người lập → Người tạo**, **Ngày lập → Ngày tạo** (ô lọc + 2 cột + placeholder)
      · thêm **nút ×** ở ô "Mã phiếu yêu cầu", chỉ hiện khi có chữ; dựng bằng slot `suffix` +
        `has-suffix` sẵn có của `V2BaseInput`, kiểu dáng bám `V2BaseFilterFieldControl` :30-37.
        Bấm × là xoá + TÌM LẠI luôn (đồng nhất với ô Người tạo). Kiểm: ô trống→không nút ·
        gõ "PYC"→hiện · bấm ×→ô rỗng, nút biến mất, danh sách về đủ 10 dòng.
      · thêm **sort cột Mã phiếu + Ngày tạo**. BE `BillAdjustDeptPickerService::searchAdjustRequests()`
        whitelist `code` / `createdAt`, nhận `sort_by` + `sort_desc`, GIỮ chốt `r.id DESC` cuối
        (3 phiếu cùng `17/08/2026 16:45` — thiếu chốt là lật trang thấy lặp/mất). FE dựng tiêu đề
        bấm được sao y `V2BaseDataTable` :90-99 + :746-757; mở popup / Làm mới thì xoá sắp xếp.
        Kiểm thật: mã ↑ `TEST...00002→00004→00005`, mã ↓ `TPSG...176→175→174`,
        ngày ↑ `04/04→16/04 16:39→16/04 18:00`, ngày ↓ `24/08→17/08→17/08`.
      Cột Người tạo CHƯA có sort (user chỉ yêu cầu 2 cột) — thêm 1 dòng whitelist là xong.

- [x] Màn CHI TIẾT — hàng "phiếu nguồn" (user 2026-09-07, chốt qua 2 lượt):
      Ô **Phiếu yêu cầu điều chỉnh công nợ** trước đây render `nuxt-link` chữ trần, đứng cạnh 3 ô
      `V2BaseInput` cùng hàng nên chỏi hẳn. Bản CUỐI theo user: **ô `disabled`** (nền `#f1f5f9`
      chuẩn ô khoá) + **chữ mang kiểu link của màn danh sách** (navy `#28539d` + gạch chân nét đứt,
      hover teal — khuôn `a.v2-cell-link`), bọc `nuxt-link` ra ngoài ô.
      Cùng lượt: ô **Phiếu yêu cầu hạch toán bổ sung** cũng gắn link
      (`/finance/addition-accounting-requests/{id}`, lấy theo `SOURCE_ROUTES` của màn danh sách
      `index.vue` :304-307 để 2 màn không trỏ 2 nơi); 3 ô luôn-chỉ-đọc (bổ sung / hoa hồng tháng /
      vận chuyển nhanh) đổi `readonly` → **`disabled`** cho đồng bộ cả hàng.
      Ô **hoa hồng tháng KHÔNG có link** — HRM chưa port màn đó (`SOURCE_ROUTES` cũng bỏ trống);
      có màn rồi thì thêm y hệt, đã ghi chú tại chỗ.
      ⚠️ 3 điểm kỹ thuật bắt buộc, đừng gỡ:
        · `pointer-events: none` cho `input:disabled` — thẻ input bị disable KHÔNG phát sự kiện
          chuột, thiếu dòng này thì bấm giữa ô không đi đâu, chỉ mép ngoài mới ăn link;
        · `color: #28539d !important` — rule ô khoá dùng chung (`v2-styles.scss` :41-56) khai
          `color: #475569 !important`, không `!important` thì chữ ra xám, nhìn không ra là link
          (lần đo đầu đã dính đúng chỗ này);
        · gạch chân bằng `text-decoration: underline dashed`, KHÔNG `border-bottom` — `border-bottom`
          kẻ hết bề ngang ô, trông như ô bị gạch chứ không phải link.
      Kiểm thật: `/finance/bill-adjust-depts/12851` → href `/finance/bill-adjust-dept-requests/10217`,
      bấm giữa ô mở đúng tab mới; `/finance/bill-adjust-depts/12852` → href
      `/finance/addition-accounting-requests/1994`, ô `disabled`, nền `#f1f5f9`, chữ `#28539d`,
      gạch `underline/dashed`, bấm giữa ô mở đúng tab mới.

Đang làm dở: không có.

Bước tiếp theo: **9.5** user mở trình duyệt bấm thật. Seeder đã chạy: 5 phiếu `TEST.PKT.0000x`
trạng thái *Đang tạo* gán cho NV #13 (tài khoản dev), mỗi phiếu 1 nhóm định khoản đã cân sẵn nên
mở ra bấm "Lưu và duyệt" được ngay. 0 bút toán nào được ghi vào sổ cái.

Blocked: [để trống]

### Phần CHƯA kiểm chứng được (ghi rõ để không nhầm là đã xong)
| Hạng mục | Lý do |
| --- | --- |
| Nhánh `exportable_*` (phiếu YC xuất hàng) | `exportable_type` NULL ở **33.409/33.409** dòng thật — code chết của ERP |
| Nhánh `is_begin` (số dư đầu kỳ) khi ghi sổ | `is_begin = 1` ở **0/33.409** dòng thật |
| Cửa vào 4 — Hạch toán hoa hồng tháng | bảng nguồn **0 dòng**, màn nguồn chưa port |
| Cửa vào 5 — Chi phí giao nhanh | màn nguồn chưa port; `fast_delivery_employee_id` do service báo cáo ERP tính, HRM chưa có nguồn nên để null |
| Nghiệp vụ số dư lẻ | chưa dựng được hợp đồng có dư lẻ trong ngưỡng để chạy thật |
| Toàn bộ thao tác FE | chưa mở trình duyệt — user tự bấm |


---

## Phase 10 — Kiểm thử Playwright + đối chiếu trực tiếp với ERP (2026-08-28)

Chạy thật trên trình duyệt: HRM `localhost:3000` ↔ ERP `127.0.0.1:8002`, cùng tài khoản, cùng DB.

- [x] 10.1 Đối chiếu **20 bộ lọc** giữa 2 API (không lọc · mã phiếu · mã YCĐC · 3 trạng thái ·
      tài khoản theo số và theo tên · mã hợp đồng · 2 khoảng tiền · ngân hàng · 2 người lập ·
      2 khoảng ngày · 2 NVKD · khách hàng · kết hợp 2 điều kiện) → **20/20 khớp tuyệt đối**
- [x] 10.2 Đối chiếu danh sách trang 1: 11 cột × 10 dòng, tổng số bản ghi
- [x] 10.3 Bấm thật: sort 2 chiều + hủy sort cột cũ · phân trang · ghi nhớ bộ lọc khi quay lại ·
      popup "Cài đặt bộ lọc" · Cấu hình cột
- [x] 10.4 Nút hành động theo trạng thái: phiếu *Đang tạo* có Sửa/Xóa, phiếu *Đã duyệt* ẩn hẳn
- [x] 10.5 Màn chi tiết + màn sửa: nạp đúng dữ liệu, badge đúng màu, cảnh báo "chưa lưu" khi thoát
- [x] 10.6 Bảng định khoản: nhập Nợ tự xóa Có · cột quy đổi tự tính · **Thêm dòng tự điền chênh
      lệch** để nhóm cân · cảnh báo nhóm lệch
- [x] 10.7 3 popup: chọn đối tượng (tìm theo mã/tên, 3 loại KH/NCC/NV, chọn xong **reset sạch 6
      trường hợp đồng**) · chọn hợp đồng (nhánh KH 372 HĐ, nhánh NCC 104 HĐ) · phiếu YC xuất hàng
- [x] 10.8 Cửa vào 2 (từ Phiếu YCĐC): so **từng dòng** với `getDataForBillAdjustDept` của ERP →
      khớp tuyệt đối 3/3 dòng (tài khoản, số tiền, nhóm, đối tượng, hợp đồng, ngày hạch toán)
- [x] 10.9 **Duyệt qua giao diện** trên phiếu TEST → ghi đúng 2 bút toán + 2 dòng đối ứng chéo
      nhau; **đã dọn sạch**, sổ cái về đúng 972.053 dòng / max id 1001536 như trước khi test
- [x] 10.10 Xóa phiếu qua giao diện → phiếu + dòng chi tiết sạch
- [x] 10.11 Bản in: so ảnh chụp với bản in ERP cùng phiếu
- [x] 10.12 Xuất Excel 1 phiếu (có letterhead, ô tiền kiểu SỐ + `#,##0`) và Excel danh sách

### 7 lỗi tìm được và đã sửa

| # | Lỗi | Bằng chứng | Đã sửa |
| --- | --- | --- | --- |
| 1 | Cột **Phòng ban** ở danh sách/Excel lấy phòng ban NGƯỜI LẬP. ERP lấy của **phiếu YCĐC nguồn** — người lập luôn là kế toán nên cột đó thành vô nghĩa | lệch 4/10 dòng trang đầu so ERP | `BillAdjustDeptService::attachRequestDepartment()` |
| 2 | Màn **chi tiết** vẫn render `<input>` ở cột Mã khách + Đơn hàng/Hợp đồng | 2 ô nhập còn sót khi `readonly` | `AccountingDetailTable.vue` tách nhánh `v-if/v-else` |
| 3 | **Popup chọn hợp đồng trả `created_by` = ID**, trong khi cột `contract_created_by` là `varchar` chứa **TÊN** (18.149/18.149 dòng ERP đều là chữ) → NVKD hiện ra con số | ERP `searchAllContract` trả `fullname` | `BillAdjustDeptPickerService::loadCreatorNames()` |
| 4 | **Ô lọc NVKD chết hoàn toàn** — lọc id trên cột chứa tên | ERP: 84 và 25 phiếu · HRM: 0 và 0 | `searchByFilter()` quay về `whereHasMorph` như ERP |
| 5 | **Excel danh sách chỉ ra 2 cột**, mất 9 cột — `buildQueryString()` (util dùng chung) serialize mảng thành `fields=a&fields=b`, PHP chỉ nhận giá trị cuối | file tải về chỉ có STT + Trạng thái | FE gửi chuỗi `a,b,c`; BE `forData()` nhận cả 2 dạng |
| 6 | **Bản in lệch ERP**: thiếu cột NVKD, thừa cột Nhóm, tách đôi cột Tài khoản, thiếu ô ký BAN GIÁM ĐỐC, ghi "Cộng" thay vì "Tổng", dòng ngày sai định dạng, số tiền xuống dòng giữa con số | so ảnh 2 bản in cùng phiếu | `print.vue` dựng lại theo đúng 9 cột + 3 ô ký của ERP |
| 7 | Popup "Chọn trường xuất" không tự đóng sau khi xuất xong | quan sát trực tiếp | `index.vue` gọi `$bvModal.hide()` sau khi tải xong |

### Lỗi của ERP mà HRM sửa (đã chứng minh trên giao diện ERP thật)

| Lỗi ERP | Bằng chứng | HRM |
| --- | --- | --- |
| Ô lọc **"STK ngân hàng"** lọc cột `account_number` — cột KHÔNG TỒN TẠI trên `bill_adjust_dept_details` | ERP trả **HTTP 500** `Unknown column 'account_number'` | lọc đúng cột `bank_account_number` → ra 15 phiếu |
| Xoá phiếu kế toán không trả trạng thái cho Yêu cầu hạch toán bổ sung | đọc code `delete()` :344-366 | trả về *Chờ duyệt* |

### Vẫn CHƯA kiểm chứng được (không đổi so với trước)

Nhánh `exportable_*` và `is_begin` khi ghi sổ (0 dòng dữ liệu thật) · cửa vào Hoa hồng tháng
(bảng nguồn 0 dòng) và Giao nhanh (màn nguồn chưa port) · nghiệp vụ số dư lẻ (chưa dựng được hợp
đồng có dư lẻ trong ngưỡng) · phiếu **ngoại tệ** ở màn tạo/sửa (chưa có phiếu ngoại tệ nháp để bấm).

---

## Phase 11 — Rà chuẩn UI (soát lại 2026-09-05)

Kết quả soát toàn màn theo skill `button-convention` / `modal-popup` / `list-page` +
memory dùng chung. User chốt làm 2 việc trước: **màu nút footer** và **khối File đính kèm**.

### 11.1 Màu nút ở footer (skill button-convention §2b)

- [x] `BillAdjustDeptForm.vue:186` nút **Lưu**: `secondary` + icon `ri-draft-line`
      → `primary` (teal `#1abc9c`) + icon `ri-save-3-line`
- [x] `BillAdjustDeptForm.vue:194` nút **Lưu và duyệt**: bỏ `status="success"` (`#16a34a`)
      → `primary` trần = teal `#1abc9c`, đúng nhóm Duyệt (chốt 2026-08-20, cùng màu `V2Footer`)
- [x] `_id/index.vue` footer màn chi tiết: icon Xóa `ri-delete-bin-6-line` → `ri-delete-bin-line`,
      text nút **"In phiếu"** → **"In"** (bảng text chuẩn §4.2)
- [x] Thay `:disabled="saving"` → `:interactable="!saving"` trên cả 2 nút — `V2BaseButton`
      KHÔNG có prop `disabled` (`components/V2BaseButton.vue:24-49`), nút vẫn bấm được
- [x] Thêm `$safeLoadingStart()` / `$safeLoadingFinish()` (finally) + guard `if (this.saving) return`
      vào `submit()` — hiện bấm Lưu 2 lần tạo 2 phiếu, bấm Lưu và duyệt 2 lần ghi 2 bộ bút toán

### 11.2 File đính kèm — dùng lại khối của màn Đề nghị thanh toán

Bỏ `<input type="file">` + `<ul><li>` tự chế (form dòng 106-131), dùng
`pages/finance/bill-payment-requests/components/AttachmentSection.vue` qua prop `api-base`
(đúng cách màn `borrow-export-requests` đã làm 2026-09-04).

**BE** — khối này cần 3 endpoint theo khuôn `{apiBase}`:

- [x] Thêm `BillAdjustDeptAttachmentService::sizes()` (copy `BillPaymentAttachmentService::sizes()` —
      `Http::pool` HEAD lấy `Content-Length`)
- [x] Thêm `BillAdjustDeptController::attachmentSizes()` + route `GET /{id}/attachment-sizes`
- [x] Đổi route xoá file `POST /{id}/delete-file` → `DELETE /{id}/files` cho khớp 3 màn anh em
      (`bill-payment-requests` :689, `addition-accounting-requests` :794). Controller `deleteFile()`
      giữ nguyên — `$request->input('file_url')` đọc được cả query string của DELETE

**FE**:

- [x] `BillAdjustDeptForm.vue`: thay khối tự chế bằng `<AttachmentSection>` với
      `:files` / `:pending-files` / `:request-id` / `api-base` / `:error-message` / `:readonly`
- [x] Thêm 4 handler `onAddUploadedFile` / `onRemovePendingFile` / `onReplacePendingFile` /
      `onRemoveSavedFile` + state `pendingFiles`; `attachment_urls` khi lưu = files đã lưu + pending
- [x] Cập nhật `unsavedSnapshotSource()` cho khớp state mới
- [x] Bỏ `onFilesChosen()` / `removeAttachment()` / `fileName()` cũ

### 11.2b Bảng — thanh cuộn ngang ở CẢ TRÊN VÀ DƯỚI (skill list-page §3b-1)

- [x] `AccountingDetailTable.vue`: bỏ `<div class="table-responsive">`, bọc `<V2BaseTableScroll>`
      (trần, đúng như `bill-adjust-dept-requests/components/AdjustDetailTable.vue`)
      · bảng 17 cột, tổng min-width ~2.580px (VNĐ) / ~2.860px (ngoại tệ) → LUÔN tràn ngang, mà
        trước đó chỉ có thanh cuộn ĐÁY: phải kéo qua hết mọi dòng định khoản mới với tới nó
      · bỏ `.table-responsive` còn thoát rule global `assets/scss/default.scss:85`
        (`min-height: 50vh`) vốn kéo bảng 1-2 dòng lên hơn 400px

**Đã rà, KHÔNG phải sửa:**

- `index.vue` dùng `V2BaseDataTable`, prop `enableScrollSync` mặc định `true` → đã có thanh trên
- 3 bảng trong popup (`ObjectSearchModal` 4 cột / `ContractPickerModal` 4 cột / `ExportRequestSearchModal`
  3 cột, mỗi bảng chỉ 1 cột co giãn, modal `lg`/`xl`) → không tràn ngang, `V2BaseTableScroll` có bọc
  cũng tự ẩn thanh trên
- `_id/print.vue` dùng `<table>` trần — ĐÚNG: scoped CSS và component không sang được cửa sổ in
  (skill print-page §1)

### 11.3 Còn nợ (đã báo user, CHƯA làm)

`text-muted` ra chữ ĐỎ ở 14 chỗ (layout `default-sidebar` bọc `.training-layout`, import
`custom-assign.scss` ép `#dc3545 !important`) · 3 popup tự chế phân trang thay vì `V2BasePagination`
· card thiếu `card-header section-header` (lệch 2 màn anh em) · `<span class="text-danger">*</span>`
thay cho `<Required />` · 2 `BaseConfirmModal` xóa thiếu prop `danger` · popup duyệt thiếu mã phiếu ·
2 hàm xóa thiếu lớp tải · 6 nút phân trang popup thiếu icon + `:disabled` chết ·
ô Loại tiền chỉ báo lỗi bằng toast · `thead` bảng định khoản chưa sticky (17 cột, cuộn dọc là mất tiêu đề).

### Checkpoint — 2026-09-05

Vừa hoàn thành: Phase 11.1 (màu nút footer) + 11.2 (khối File đính kèm dùng chung) — BE 3 file sửa,
FE 3 file sửa. Compile sạch 4/4 file `.vue`; 2 route mới đã đăng ký (`GET /{id}/attachment-sizes`,
`DELETE /{id}/files`); `sizes()` / `attachmentSizes()` / `deleteFile()` đều resolve qua reflection.

Đang làm dở: không có.

Bước tiếp theo: user mở trình duyệt kiểm 4 việc chưa tự kiểm chứng được —
(a) 2 nút footer ra cùng teal `#1abc9c`,
(b) upload file ở màn Tạo → lưu → mở lại thấy file + đúng dung lượng,
(c) màn Sửa bấm Xóa file (popup xác nhận) → file mất hẳn, không quay lại sau khi Lưu,
(d) màn Chi tiết khối file ở chế độ chỉ đọc (không có nút Thêm tài liệu / Xóa).

Blocked: không có.

### ⚠️ Lỗi cũ mà việc thay khối đính kèm vừa sửa luôn

Khối tự chế gửi `attachment_urls` = TOÀN BỘ danh sách, trong khi BE
`BillAdjustDeptAttachmentService::uploadAttachments()` **NỐI** vào chuỗi cũ chứ không ghi đè
(`mergeSourceAttachments()` cuối cùng còn `array_unique`). Hệ quả: ở màn Sửa, **gỡ file rồi bấm Lưu
thì file quay trở lại** — chuỗi cũ trong DB vẫn còn URL đó. Khối dùng chung xoá file đã lưu bằng
`DELETE {api-base}/{id}/files` ngay lúc bấm nên hết lỗi này; `attachment_urls` giờ chỉ gồm file
chờ lưu.

---

## Phase 12 — Bố cục màn TẠO lệch ERP (user báo 2026-09-05)

User: *"bố cục màn tạo phiếu kế toán khác với bên erp, ví dụ không có phiếu yêu cầu điều chỉnh
công nợ"*. Đối chiếu `erp/resources/views/income_expenditure/bill_adjust_depts/form.blade.php`
(:100-220) + `create.blade.php` + `formJs.blade.php`.

### Bảng đối chiếu khối "Thông tin chung"

| # | ERP | HRM trước | Kết luận |
| --- | --- | --- | --- |
| 1 | **Phiếu yêu cầu điều chỉnh công nợ** — ô chỉ đọc + **nút kính lúp mở popup chọn**, hiện khi KHÔNG đến từ 3 nguồn kia (`form.blade.php` :100-113) | chỉ `v-if="form.bill_adjust_dept_request_code"` → màn Tạo mới **không có ô này, cũng không có đường chọn** | ❌ THIẾU HẲN — đúng cái user chỉ ra |
| 2 | **Tỷ giá** LUÔN hiện, khoá khi `type_money_id == 1`, kèm nút hiện tên tiền tệ (:153-166) | `v-if="isForeign"` → phiếu VNĐ không thấy tỷ giá | ❌ lệch |
| 3 | **Loại tiền** khoá khi đã có phiếu YCĐC (`ng-disabled="form.bill_adjust_dept_request_id"`, :141) | không khoá | ❌ lệch |
| 4 | Header card `Thông tin chung` + góc phải `<% form.creator %> - <% form.created_time %>` (:92-97) | card trần, không header; Trạng thái là 1 ô riêng trong lưới | ❌ lệch (cũng là mục 11.3 đã ghi) |
| 5 | Header card `Chi tiết` + nút "Thêm chi tiết" ở góc phải (:233-238) | `.section-title` tự chế trong card-body | ❌ lệch |
| 6 | Thứ tự hàng 1: nguồn → Ngày hạch toán → Loại tiền → Tỷ giá | Mã phiếu đứng đầu, đẩy lệch cả hàng | ❌ lệch |
| 7 | Không có ô Mã phiếu / Phòng ban | có (thông tin hữu ích, đúng khuôn HRM) | ✅ GIỮ, dồn xuống hàng 2 |
| 8 | Diễn giải `col-md-12`, File đính kèm `col-md-12` | giống | ✅ |

### Popup "Yêu cầu điều chỉnh công nợ" (ERP `formJs.blade.php` :66-89)

Nguồn `bill_adjust_dept_request.searchData` + ép `status = 2`
(= `STATUS_AWAITING_APPROVE` — *"Chờ tạo phiếu kế toán"*).
Cột: **STT · Mã phiếu · Ngày lập**. Ô tìm: **Mã phiếu** (text).
Chọn xong → `getDataForBillAdjustDept` điền: `bill_adjust_dept_request_id/code` · `note` ·
`details` · `date_accounting` · loại tiền + tỷ giá (**chỉ khi `request_type = 2` (NCC)**, YC khách
hàng ép về VNĐ).

→ HRM **KHÔNG cần BE mới**: `GET /finance/bill-adjust-dept-requests/pending` đã có sẵn và khớp
tuyệt đối (gate `isAccountant()` như middleware ERP, ép `status = STATUS_AWAITING_APPROVE`, giới hạn
theo công ty, hỗ trợ lọc `code`) — hiện chưa màn nào gọi. Nạp dữ liệu sau khi chọn dùng lại
`GET /finance/bill-adjust-depts/source-data?bill_adjust_dept_request_id=`.

### Task

- [x] 12.1 Tạo `components/BillAdjustDeptRequestPickerModal.vue` — khuôn `ObjectSearchModal.vue`
      (V2BaseModal), gọi `/finance/bill-adjust-dept-requests/pending`, 3 cột đúng ERP
- [x] 12.2 Ô "Phiếu yêu cầu điều chỉnh công nợ" + nút kính lúp; hiện khi không đến từ 3 nguồn kia
- [x] 12.3 Chọn xong → nạp `/source-data` (tách `loadSourceData` thành hàm nhận params dùng chung
      cho cả cửa vào bằng query lẫn popup)
- [x] 12.4 Tỷ giá LUÔN hiện, khoá khi VNĐ, hậu tố tên tiền tệ
- [x] 12.5 Loại tiền khoá khi đã có phiếu YCĐC
- [x] 12.6 Thêm `card-header section-header` cho 2 card ("Thông tin chung" + "Định khoản"),
      góc phải card 1 = badge trạng thái + "{Người lập} - {Ngày lập}" (khuôn
      `BillAdjustDeptRequestForm.vue` :17-37) — bỏ ô Trạng thái trong lưới
- [x] 12.7 Xếp lại hàng 1 đúng ERP: nguồn → Ngày hạch toán → Loại tiền → Tỷ giá;
      Mã phiếu / Người lập / Phòng ban xuống hàng 2

- [x] 12.8 Màn XEM: ô nguồn chỉ hiện khi phiếu THỰC SỰ có YCĐC và hiện dạng **link** sang phiếu
      yêu cầu (ERP `formShow.blade.php` :98-109) — không hiện ô rỗng kèm chữ "Chọn phiếu…"
- [x] 12.9 Đổi phiếu nguồn NCC (ngoại tệ) → phiếu KH: đặt lại `exchange_rate = 1` khi BE không trả
      trường này. `onCurrencyChange()` chỉ chạy khi user tự đổi ô, không chạy lúc gán bằng code →
      giữ tỷ giá cũ là nhân sai toàn bộ cột quy đổi (ERP cũng dính, HRM sửa)

### Checkpoint — 2026-09-05 (Phase 12)

Vừa hoàn thành: dựng lại bố cục màn Tạo theo ERP. 1 file FE mới
(`BillAdjustDeptRequestPickerModal.vue`) + 2 file sửa (`BillAdjustDeptForm.vue`,
`AccountingDetailTable.vue`). **0 file BE** — `GET /finance/bill-adjust-dept-requests/pending`
đã có sẵn và khớp đúng cái ERP làm.

Kiểm chứng bằng HTTP kernel (nhân viên id 13, có quyền *Kế toán thanh toán*):
`GET /bill-adjust-dept-requests/pending?per_page=3` → **HTTP 200, total 44 phiếu**, trả đủ
`code` + `created_at`; `GET /bill-adjust-depts/source-data?bill_adjust_dept_request_id=6890` →
**HTTP 200**, header 5 khoá + 2 dòng chi tiết. Compile sạch 3/3 file `.vue`.

Đang làm dở: không có.

Bước tiếp theo: user mở trình duyệt kiểm —
(a) `/finance/bill-adjust-depts/create` có ô "Phiếu yêu cầu điều chỉnh công nợ" + nút kính lúp,
(b) chọn 1 phiếu trong popup → điền mã phiếu + diễn giải + ngày hạch toán + bảng định khoản,
(c) phiếu VNĐ vẫn thấy ô Tỷ giá (khoá, hậu tố "VNĐ"),
(d) chọn phiếu YCĐC xong thì ô Loại tiền bị khoá,
(e) 2 card có tiêu đề "Thông tin chung" / "Định khoản", góc phải card 1 có badge + "{Người lập} - {Ngày lập}".

Blocked: không có.

### Chưa làm (khác biệt ERP đã cân nhắc rồi GIỮ nguyên bản HRM)

- Nút "Thêm dòng" — ERP ghi *"Thêm chi tiết"*; giữ chữ HRM theo bảng text chuẩn `button-convention` §4.2
- Tiêu đề khối bảng — ERP ghi *"Chi tiết"*; HRM để *"Định khoản"* (nói rõ nội dung khối hơn)
- Ô **Mã phiếu / Phòng ban** — ERP không có (ERP còn comment hẳn ô Mã phiếu ở `formShow`);
  HRM giữ vì hữu ích, dồn xuống hàng 2 để hàng 1 khớp ERP
- Popup chọn phiếu YCĐC dùng `V2BasePagination` (có cả chọn số dòng/trang) thay cặp nút
  "Trang trước / Trang sau" của ERP — HRM là nguồn của giao diện (skill `erp-to-hrm-screen`)

### 12.10 Đồng bộ ô chọn phiếu YCĐC theo khuôn màn Phiếu thu tiền (user chốt 2026-09-05)

User: *"chỗ chọn phiếu yêu cầu điều chỉnh công nợ sử dụng giống như chọn phiếu đề nghị của màn
finance/bill-incomes/create"*. Khuôn gốc: `bill-incomes/components/BillIncomeForm.vue` :14-30 +
`IncomeRequestSearchModal.vue`.

- [x] Ô nhập: **bỏ nút kính lúp riêng**, bấm THẲNG vào ô để mở popup; placeholder đổi thành
      *"Nhấn vào đây để chọn phiếu yêu cầu điều chỉnh công nợ"*; thêm class `.picker-input`
      (con trỏ bàn tay + nền TRẮNG dù `readonly`, copy :1295-1312 của màn kia)
- [x] Popup: thêm ô lọc **Người lập** (`V2BaseSelectInModal` — bắt buộc trong modal),
      dòng phụ ở header *"Chỉ phiếu đang Chờ tạo phiếu kế toán"*, `size="xl"`,
      bảng 4 cột (STT · Mã phiếu yêu cầu · Người lập · Ngày lập), bấm CẢ DÒNG để chọn
      (`.tr-hover` + `title`), `per_page` mặc định 10 như màn kia
- [x] `modalId` đổi thành `choose-bill-adjust-dept-request` cho cùng lối đặt tên
      (`choose-income-request`)

**Khác 1 điểm CÓ CHỦ ĐÍCH**: popup mới dựng trên `V2BaseModal`, không tự khai `b-modal` + header +
footer như `IncomeRequestSearchModal`. Skill `modal-popup` §0 chốt popup MỚI phải dùng khuôn chung;
bản ở màn Phiếu thu tiền có TRƯỚC khuôn đó nên còn tự dựng — chép lại là nhân thêm nợ kỹ thuật.

Kiểm chứng (HTTP kernel, nhân viên id 13 có quyền *Kế toán thanh toán*):
`/bill-adjust-dept-requests/pending` → HTTP 200, `per_page=10` ra 44 phiếu ·
`code=DNDCCN` ra 44 · `created_by=13` ra 4 — cả 3 ô lọc đều ăn, dòng trả về đủ
`code` / `created_by_name` / `created_at`. Compile sạch 2/2 file.

### 12.11 Bỏ ô KHÔNG có trong ERP (user chốt 2026-09-05 — *"bám sát erp cho tôi"*)

Đếm lại nhãn trong `erp/.../bill_adjust_depts/form.blade.php` (file này dùng cho **cả create lẫn
edit** — `edit.blade.php` không khai thêm nhãn nào): khối "Thông tin chung" có ĐÚNG **6 nhãn** —
phiếu nguồn · Ngày hạch toán * · Loại tiền * · Tỷ giá * · Diễn giải * · File đính kèm.
`formShow.blade.php` còn **comment hẳn** ô Mã phiếu (:92-96) và **không có trạng thái** ở bất kỳ đâu.

- [x] Bỏ 3 ô HRM tự thêm: **Mã phiếu · Người lập · Phòng ban**
- [x] Bỏ **badge trạng thái** ở góc phải đầu card — ERP không có trạng thái trong form lẫn màn xem.
      Góc phải giữ đúng 1 thứ ERP có: dòng `{Người lập} - {Ngày lập}`
      (`<% form.creator %> - <% form.created_time %>`)
- [x] Bỏ lệnh gọi `GET /finance/bill-adjust-depts/generate-code` ở màn tạo — ERP không xem trước mã,
      và mã thật do BE sinh lúc lưu (`BillAdjustDeptWriteService` :71), **không** nhận từ FE
      (`BillAdjustDeptStoreRequest` không có rule `code` cấp phiếu). Route BE giữ nguyên, nay không
      còn FE nào gọi
- [x] Dọn import chết theo: `V2BaseBadge`, `statusBadgeVariant`

⚠️ **Hệ quả cần user biết**: màn **Sửa / Chi tiết** giờ KHÔNG còn chỗ nào hiện trạng thái phiếu
(trước đây có badge). Trạng thái vẫn xem được ở cột "Trạng thái" ngoài màn danh sách. Đúng như ERP,
nhưng nếu muốn giữ badge riêng cho màn HRM thì báo để bật lại.

📝 User tự sửa trong lúc làm: nhãn ô tỷ giá đổi thành **"Tỷ giá (VND)"** và bỏ hậu tố tên loại tiền
(giữ nguyên, chỉ sửa lại comment cho khỏi mô tả sai).

**Khối "Thông tin chung" sau khi sửa — khớp 1-1 với ERP:**

| Vị trí | Ô | ERP |
| --- | --- | --- |
| đầu card | `Thông tin chung` + góc phải `{Người lập} - {Ngày lập}` | :92-97 |
| 1 | Phiếu yêu cầu điều chỉnh công nợ (hoặc 1 trong 3 nguồn kia) | :100-127 |
| 2 | Ngày hạch toán * | :131 |
| 3 | Loại tiền * | :140 |
| 4 | Tỷ giá * | :155 |
| 5 | Diễn giải * (`col-12`) | :170 |
| 6 | File đính kèm (`col-12`) | :180 |

### 12.12 Bảng chi tiết — cột nào CHO SỬA, cột nào CHỈ HIỂN THỊ (user báo 2026-09-05)

User: *"tiêu đề là chi tiết mà; cột mã khách hàng, phát sinh nợ, phát sinh có, đơn hàng/hợp đồng
bên erp chỉ hiển thị thôi, có cho chọn đâu"*.

Đọc `form.blade.php` :279-437. ERP gate từng ô bằng **điều kiện THEO DÒNG**, không phải theo phiếu:

```
rowLocked = form.bill_adjust_dept_request_id && !detail.fast_delivery_id
```

| Cột | `rowLocked` | không khoá | HRM trước |
| --- | --- | --- | --- |
| Số tài khoản | **select** (vẫn sửa) | select | ✅ đúng |
| **Mã khách** (:296-307) | **text** | ô + nút chọn | ❌ luôn cho chọn |
| **Phát sinh nợ / có** (:313-334) | **text** | input | ❌ luôn cho nhập |
| Diễn giải (:336) | **input** (vẫn sửa) | input | ✅ đúng |
| **Đơn hàng/Hợp đồng** (:343-357) | **text** | ô + nút — CHỈ khi `type` ∉ {1,5,7} | ❌ luôn cho chọn |
| checkbox `is_begin` (:361) | **disabled** | bật | ❌ chỉ khoá theo `readonly` |
| Phiếu YCXH (:369-378) | **text** | ô + nút khi `has_exportable && !is_begin` | ❌ chỉ gate `contract_type == 3` |
| Mã phí · Mã vụ việc | **select** (vẫn sửa) | select | ✅ đúng |

- [x] 12.12a Đổi tiêu đề khối bảng **"Định khoản" → "Chi tiết"** (ERP `<h4>Chi tiết</h4>` :235)
- [x] 12.12b Thêm prop `requestLocked` + `sourceType`; dựng `isRowLocked(row)` rồi gate đúng 4 cột
      user chỉ ra + checkbox `is_begin` + Phiếu YCXH
- [x] 12.12c Dòng tổng ghi **"Tổng"** thay vì "Cộng" (ERP :440)

### ⚠️ 2 khác biệt KHÁC phát hiện khi đọc, CHƯA làm — chờ user quyết

1. **Thiếu hẳn cột "Mã khế ước"**: ERP có `<th rowspan="2">Mã khế ước</th>` (:264) nhưng ô dữ liệu
   là `<td class="text-left v-align-middle"></td>` (:407) — **cột luôn RỖNG**. Thêm vào thì bảng 17
   cột thành 18 cột mà không có dữ liệu gì.
2. **Ngân hàng + STK ngân hàng: ERP cho CHỌN, HRM chỉ hiển thị chữ.** ERP là 2 `select`
   (:409-428): chọn ngân hàng (`banks`) thì xoá trắng STK, rồi chọn STK trong
   `detail.company_accounts`. HRM render `{{ row.bank_name }}` / `{{ row.bank_account_number }}`
   dạng chữ. Đây là **thiếu chức năng thật**, không phải lệch giao diện — cần BE trả thêm danh mục
   ngân hàng + tài khoản công ty theo dòng.

### Checkpoint — 2026-09-05 (12.12)

Vừa hoàn thành: gate 4 cột theo ĐIỀU KIỆN TỪNG DÒNG. Thêm 2 prop `requestLocked` / `sourceType`
và 3 helper `isRowLocked()` / `canPickContract()` / `canPickExportable()` trong
`AccountingDetailTable.vue`; thêm `fast_delivery_id: null` vào `normalizeRow()` để Vue 2 reactive
được khoá đó. Tiêu đề khối → **"Chi tiết"**, dòng tổng → **"Tổng"**.

Compile sạch 5/5 file. Chưa mở trình duyệt.

Bước tiếp theo: user quyết 2 việc ở mục ⚠️ trên — cột "Mã khế ước" (ERP có header nhưng ô luôn
rỗng) và Ngân hàng/STK (ERP cho CHỌN, HRM đang chỉ hiển thị chữ — thiếu chức năng thật, cần BE trả
thêm danh mục ngân hàng + tài khoản công ty theo dòng).

### 12.13 Khối "Số dư nợ đầu kì" hiện sai chỗ (user báo 2026-09-05)

User: *"sao bên hrm lại hiển thị Số dư nợ đầu kì: 0 ở chỗ đơn hàng vậy, bên erp có hiện đâu"*.

**Nguyên nhân:** HRM gate khối này bằng `v-if="row.contractable_id"` — tức **bất kỳ hợp đồng nào**
được chọn cũng hiện. ERP gate bằng `ng-if="detail.has_exportable"` (`form.blade.php` :359), mà
`has_exportable` là getter trong `partials/classes/IncomeExpenditure/BillAdjustDeptDetail.blade.php`
:14-17:

```js
get has_exportable() {
    if (this.contract_type == 3) return true;
    return false;
}
```

→ chỉ hợp đồng **loại 3** mới có khối này. Hợp đồng loại khác thì ERP không hiện gì, HRM hiện
"Số dư nợ đầu kì: 0" (số 0 vì `debt_begin` mặc định 0).

- [x] Thêm helper `hasExportable(row)` = `Number(row.contract_type) === 3` — mirror đúng tên getter
      của ERP; dùng cho CẢ khối checkbox lẫn `canPickExportable()` (trước đó `canPickExportable`
      đã đúng luật này rồi, chỉ khối checkbox lệch → 2 chỗ cùng 1 luật mà viết 2 kiểu)
- [x] Nhân tiện bỏ `class="text-muted"` trên nhãn đó → đặt màu thẳng `#6b7280`
      (style dùng chung ép `.text-muted { color: #dc3545 !important }` nên chữ đang ra ĐỎ)

### 12.14 Popup YCĐC lệch số phiếu: ERP 53 · HRM 44 (user báo 2026-09-05)

**Số liệu thật** (`bill_adjust_dept_requests`, `status = 2`): tổng **53** — công ty 1: **44**,
công ty 4: **9**. Chia theo `company_id` của phiếu và theo công ty người tạo cho **cùng kết quả**.

**Nguyên nhân:** ERP `BillAdjustDeptRequest::searchByFilter()` đặt TOÀN BỘ khối phân quyền trong
`if ($request->_type === 'all')` (:156-196), còn lọc công ty nằm riêng ở
`if ($request->_type == 'for-accounting')` (:200-204). Popup chỉ gửi `d.status = 2`,
**không gửi `_type`** → không nhánh nào chạy → ERP trả cả 53 phiếu của mọi công ty.
HRM gọi preset `pending` vốn lọc theo công ty người đăng nhập → 44.

**User chốt: bỏ lọc công ty, y hệt ERP (53 phiếu).**

- [x] Thêm `BillAdjustDeptPickerService::searchAdjustRequests()` + `searchRequests()` ở Controller
      + route `GET /finance/bill-adjust-depts/search-requests` (đặt TRƯỚC `/{id}`), cùng chỗ với
      3 popup còn lại của màn
- [x] FE trỏ sang endpoint mới (shape `{ data: { data, meta } }` như 3 popup kia)

**Vì sao KHÔNG sửa thẳng preset `pending`:** `pending` là quy ước chung toàn dự án cho **màn chờ
duyệt** — `BillIncomeRequest` :296, `BillPaymentRequest` :349-355, `AdditionAccountingRequest` :318
đều dùng nghĩa "cùng công ty + đúng quyền duyệt". Đổi nghĩa nó cho riêng màn này thì màn chờ duyệt
của Yêu cầu điều chỉnh công nợ (chưa làm) sẽ sai phạm vi mà không ai biết.

**VẪN gate `isAccountant()`**: ERP đặt `checkPermission:Kế toán thanh toán` trên chính route
`bill_adjust_dept.create` chứa popup, nên bỏ luôn gate là mở rộng hơn cả ERP.

Kiểm chứng (HTTP kernel, nhân viên id 13): `search-requests` → HTTP 200,
`per_page=5` ra **total = 53** (đúng bằng ERP) · `code=DNDCCN` ra 53 · `created_by=13` ra 4.

### ⚠️ RỦI RO ĐÃ BÁO USER, user chấp nhận

`BillAdjustDeptWriteService` :75 đặt `company_id` của phiếu kế toán theo **NGƯỜI LẬP**, không theo
phiếu YCĐC nguồn. Nên kế toán công ty 1 chọn 1 trong 9 phiếu của công ty 4 sẽ sinh phiếu kế toán
mang `company_id = 1` cho nghiệp vụ công nợ của công ty 4 → **bản in ra letterhead sai công ty**
(CLAUDE.md: letterhead lấy theo `company_id` ghi trên chứng từ) và **bút toán ghi thẳng vào sổ cái
`account_details` dùng chung với cổng ERP**.

Nếu về sau muốn vừa đủ 53 phiếu vừa không sai công ty → sửa `:75` lấy `company_id` từ phiếu nguồn.

---

## Phase 13 — Rà màn DANH SÁCH (user báo 2026-09-05)

### Đã sửa (5/7)

- [x] 13.1 **Đổi "Người lập"/"Ngày lập" → "Người tạo"/"Ngày tạo"** ở bộ lọc + bảng + popup chọn
      trường xuất + nhãn cột trong `BillAdjustDeptListExport::FIELDS`
- [x] 13.2 **Thêm cột Ngày cập nhật · Người cập nhật**
      · BE: `BillAdjustDeptListResource` trả `updated_at` (`d/m/Y H:i`) + `updated_by` +
        `updated_by_name`; thêm quan hệ `BillAdjustDept::employee_update()` (chưa hề có);
        eager-load `employee_update.info` ở CẢ 2 truy vấn (`searchByFilter` phân trang và
        `allForExport`) để không N+1
      · FE: 2 cột đặt ngay sau cặp cột tạo, thêm vào popup chọn trường xuất
- [x] 13.3 **Ô trống để TRỐNG**, bỏ hết dấu `—` (10 chỗ trong `index.vue`)
- [x] 13.4 **Chưa có tiêu đề trang** — `index.vue` khai `mixins: [PageTitleMixin]` nhưng
      **thiếu computed `pageTitle`**. Mixin theo dõi đúng computed đó rồi commit vào store để
      layout dựng tiêu đề; chỉ khai `head()` là mới đổi được `<title>` của trình duyệt.
      Khuôn: `bill-adjust-dept-requests/index.vue` :409-411
- [x] 13.5 **Placeholder chữ to chữ bé** — `V2BaseCurrencyInput` ở `size="sm"` để **13px**
      (`components/V2BaseCurrencyInput.vue` :252) trong khi `V2BaseInput` :126 /
      `V2BaseSelect` :490 / `V2BaseDatePicker` :288 cùng `size="sm"` đều **12px** → 2 ô
      "Số tiền từ/đến" to hơn hẳn. Sửa bằng style scoped ở màn (3 lớp selector để thắng rule
      `[data-v-comp]` của component). **Chưa sửa component dùng chung** — CLAUDE.md bắt hỏi trước.

### KHÔNG làm được / không phải lỗi (2/7)

- [ ] 13.6 **Ngày hạch toán thêm giờ — KHÔNG LÀM ĐƯỢC.** Cột `bill_adjust_depts.date_accounting`
      kiểu **`date`**, không phải `datetime`; đo thật: **0/12.632 dòng có giờ**. Thêm giờ vào chỉ
      ra `00:00` cho mọi phiếu. Muốn có giờ thật phải đổi kiểu cột — mà cột này **dùng chung với
      cổng ERP**, đổi là đụng cả 2 hệ thống. Chờ user quyết.
- [ ] 13.7 **Bộ lọc Công ty — KHÔNG PHẢI LỖI CODE.**
      `V2BaseCompanyDepartmentFilter.vue` :8 chỉ render ô Công ty khi `permissions['is_all_company']`.
      Đo thật với tài khoản đang test (nhân viên id 13, DNS Admin):
      `can_view_all_company = false`, `can_view_company = true` → đúng thiết kế, người chỉ xem được
      1 công ty thì không cần ô chọn công ty (và cho chọn là fail-open).
      Muốn thấy ô đó phải cấp quyền **"Xem tất cả phiếu kế toán của tổng công ty"** (id 1551, guard
      `api`). Ô Phòng ban vẫn hiện vì nó chỉ cần `is_company`.

Kiểm chứng: `GET /finance/bill-adjust-depts?per_page=2` → HTTP 200, mỗi dòng có đủ
`created_at`/`created_by_name` và `updated_at`/`updated_by_name`. Compile sạch `index.vue`.

### 13.6b Ngày hạch toán thêm giờ — ĐÃ LÀM theo yêu cầu user (2026-09-05, user nhắc lại)

Đã báo trước rằng cột `bill_adjust_depts.date_accounting` kiểu **`date`** (0/12.632 dòng có giờ);
user vẫn yêu cầu → `BillAdjustDeptListResource` đổi sang `d/m/Y H:i`, cột nới 140px → 150px.

Kết quả thật đúng như đã cảnh báo: `hach toan: 28/08/2026 00:00` cho **mọi** phiếu, trong khi
`tao: 28/08/2026 12:04` có giờ thật. Muốn giờ thật phải đổi kiểu cột sang `datetime` — cột dùng
chung với cổng ERP nên đụng cả 2 hệ thống.

### 13.1b Bỏ sót khi đổi tên (user chỉ ra)

Lượt trước mới đổi ô lọc `created_by` và 2 cột bảng; còn sót 3 nhãn, nay đã đổi:
`Ngày lập từ` → **Ngày tạo từ** · `Ngày lập đến` → **Ngày tạo đến** ·
`Khoảng ngày lập` → **Khoảng ngày tạo**. Đã grep lại: `index.vue` không còn chuỗi
"Ngày lập" / "Người lập".

### 13.5b Placeholder datepicker — theo CSS thì KHÔNG to hơn

Truy lại toàn bộ rule cỡ chữ ở `size="sm"`:

| Component | Dòng | font-size |
| --- | --- | --- |
| `V2BaseDatePicker` (base `.mx-input`) | :181 | 12px `!important` |
| `V2BaseDatePicker` (`--sm`) | :288 | 12px `!important` |
| `V2BaseInput` | :126 | 12px |
| `V2BaseSelect` | :490 | 12px `!important` |
| `V2BaseCurrencyInput` | :252 | **13px** ← thủ phạm, ĐÃ sửa ở 13.5 |

Không có rule toàn cục nào đè `.mx-input` (chỉ `custom-theme.scss` :230 và `v2-styles.scss` :47,
đều là `:disabled`). `font-size: 15px` ở `V2BaseFilterFieldControl` :89 là của **nút × xoá nhanh**,
không phải placeholder.

→ Ô to hơn là cặp **"Số tiền từ / Số tiền đến"** (`V2BaseCurrencyInput`), không phải cặp ngày.
Nếu sau khi Ctrl+Shift+R mà vẫn thấy lệch thì đo bằng snippet ở mục dưới rồi báo lại số đo.

---

## Phase 14 — Redmine #11306 [ERP => HRM] Phiếu kế toán - Xuất Excel (@khoipv, 2026-09-07)

Nguồn: `http://quanly.dnsmedia.vn/issues/11306` (Nguyễn Minh Hằng, 04/09/2026). 3 lỗi.

**Đo thật trước khi sửa** (DB local 12.632 phiếu, CLI bỏ giới hạn thời gian) — chứng minh lỗi #1
là do BE dựng cả file trong 1 request đồng bộ, KHÔNG phải lỗi query:

| Bước | Thời gian | Đỉnh RAM |
| --- | --- | --- |
| `allForExport()` (get toàn bộ + eager load) | 9,4s | 96 MB |
| `BillAdjustDeptListResource::toArray()` | 24,0s | 120 MB |
| Blade `FromView` render (HTML 22,7 MB) | 25,4s | 168 MB |
| PhpSpreadsheet ghi file | **157,9s** | 230 MB |

`max_execution_time` của dự án là 60s → request chết trước khi trả file ⇒ "lỗi máy chủ".

**Quyết định của user (2026-09-07):**
1. Excel CHI TIẾT: làm **giống ERP**, chỉ khác là HRM **có thêm logo/letterhead** theo skill
   `export-excel` mục 4. Ô tiền vẫn giữ **số thật + `data-format`** (không bê lỗi "formatted as
   text" của ERP).
2. Trường lệch: **cứ làm như ERP** — Mã khách/Tên khách, có cột *Mã khế ước* (ERP luôn để trống),
   BỎ cột *Số phiếu YC xuất hàng*, BỎ Ngày lập / Trạng thái / Số tiền bằng chữ, dòng tổng ghi
   **Tổng**, thêm dòng *- Tỷ giá ngoại tệ*, 5 ô chữ ký.
3. Xuất DANH SÁCH: theo khuôn **màn Khách hàng** — tải theo trang + dựng file ở trình duyệt.

### 14.1 BE — endpoint khuôn mới cho danh sách

- [x] `BillAdjustDeptService::exportColumns()` — danh mục cột (key/label/width), nguồn DUY NHẤT cho
      popup chọn trường; khoá khớp `BillAdjustDeptListResource`
- [x] `BillAdjustDeptService::exportRows(Request, array $fields, int $page, int $limit)` — trả
      `{headings, widths, rows, total}`; STT chạy tiếp qua trang; **đếm `total` chỉ ở trang 1**
      (khuôn `CustomerService::exportRows`, COUNT có scope quyền khá nặng)
- [x] Thứ tự cột bám **đúng thứ tự `fields` user gửi** (không bám thứ tự khai) — popup ghi rõ
      "thứ tự cột chạy theo thứ tự bạn chọn"
- [x] Cột `total_amount` trả **`float`**, KHÔNG ép `(string)` (skill export-excel mục 4c), ô rỗng
      trả `null`
- [x] Controller `exportColumns()` + `exportRows()` (trần `limit` 5.000) + 2 route GET
- [x] GIỮ `export-list` + `BillAdjustDeptListExport` cũ (chưa xoá, để quay lại được — giống màn KH)

### 14.2 FE — index.vue dùng khuôn mới

- [x] Thay `downloadExcel(...export-list)` bằng `exportListFile` (`utils/export/listExportFile.js`)
- [x] Nạp cột xuất từ `export-columns`, bỏ mảng `exportFieldOptions` cứng
- [x] Truyền `:default-selected="visibleExportFields"` → **mở popup là tick sẵn đúng cột đang hiện
      trên màn** (yêu cầu chính của lỗi #2), user vẫn thêm/bớt được
- [x] Dùng `exportFieldsMixin`; nút Xuất Excel hiện tiến độ "Đang tải 4.000/12.630…" → "Đang dựng
      file…" (thông báo đợi + loading như issue yêu cầu)
- [x] Khai `exportFieldKeyMap` cho các khoá lệch giữa bảng và file (`billStatus` → `status_name`,
      `sourceCode` → `source_code`, …)

### 14.3 BE — Excel CHI TIẾT dựng lại theo ERP

- [x] `bill_adjust_dept.blade.php`: tiêu đề + *Ngày {d} Tháng {m} Năm {Y}* (theo **ngày tạo**, như
      ERP), khối thông tin **2 cột** (Mã phiếu | Mã phiếu YCĐC · Người tạo | Phòng ban ·
      Loại tiền | Tỷ giá · Diễn giải) — Loại tiền/Tỷ giá hiện CẢ khi VNĐ
- [x] Bảng: `Mã khách` / `Tên khách`, bỏ `Số phiếu YC xuất hàng`, thêm `Mã khế ước` (để trống như
      ERP), dòng tổng ghi **Tổng** căn giữa
- [x] Dưới bảng: dòng *- Tỷ giá ngoại tệ: N* (chỉ phiếu ngoại tệ) + **5 ô chữ ký** (Ban giám đốc /
      Kế toán trưởng / Người nộp tiền / Người lập phiếu / Thủ quỹ), bỏ "Số tiền bằng chữ"
- [x] `BillAdjustDeptExport::columnWidths()` trả **2 bộ** theo loại tiền (16 cột VNĐ / 18 cột ngoại
      tệ) đúng bề rộng ERP — hiện đang trả cứng 18 cột nên phiếu VNĐ bị lệch bề rộng
- [x] GIỮ letterhead (`WithDrawings`) + ô tiền số thô `data-format` (khác ERP có chủ ý, user chốt)
- [x] ⚠️ Lệch ERP có chủ ý: dòng *- Tỷ giá ngoại tệ* lấy **tỷ giá ghi trên phiếu**, không lấy tỷ
      giá hiện hành của danh mục tiền tệ như ERP (ERP in 2 số khác nhau cho cùng 1 phiếu cũ)

### 14.4 Kiểm chứng

- [x] Dựng file thật 3 ca: phiếu VNĐ · phiếu ngoại tệ · phiếu không có phiếu nguồn; đọc lại bằng
      PhpSpreadsheet: kiểu ô (`n` cho tiền), `data-format`, bề rộng cột, `drawings` = 1
- [x] So từng ô với ảnh ERP trong issue (phiếu `TPE.PKT0726.00565`)
- [x] Đo `export-rows` 1 trang 2.000 dòng < 2s — **1,33s** (trang 1, có COUNT) / **0,49s** (trang 7)
- [ ] Xuất đủ 12.630 dòng trên TRÌNH DUYỆT — chờ user mở màn thử (phần dựng file chạy ở FE)
- [x] Bản IN `print.vue` KHÔNG đổi (2 nhánh dùng chung `printService->data()`)
- [x] FE compile sạch

---

## 15. Redmine #11307 — Bản IN: chuyển sang POPUP + bám đúng mẫu ERP 208 (@khoipv)

Issue: `http://quanly.dnsmedia.vn/issues/11307` — "[ERP => HRM] Phiếu kế toán - In".
Đối chiếu bản in thật cùng phiếu `TPE.PKT0826.00003` (id 12855) trên 2 cổng dev:
`screenshots/redmine-11307-erp-mau-dung.png` vs `screenshots/redmine-11307-hrm-hien-tai.png`.

Nguyên nhân chung: màn này dựng bản in **bằng tay trong Vue** (`_id/print.vue`, 447 dòng) từ trước
khi chuẩn popup được chốt (skill `print-page` §8, 22/08), nên vừa không phải popup vừa trôi dần
khỏi mẫu ERP `report_templates` id 208. Cách sửa: copy nguyên khuôn màn anh em
**Đề nghị điều chỉnh công nợ** (`bill-adjust-dept-requests`) — BE trả HTML đã fill, FE dùng popup
dùng chung, bỏ hẳn trang `/print` để không còn 2 nguồn CSS cho cùng một bản in (§8a).

### 15.1 BE — dựng HTML bản in ở server

- [x] `Modules/Finance/Resources/views/prints/bill-adjust-dept.blade.php` bám mẫu ERP 208:
      nhãn `<strong>` (Mã phiếu / Mã phiếu yêu cầu điều chỉnh công nợ / Người tạo / Phòng ban /
      Loại tiền / **Diễn giải nằm CÙNG HÀNG với Loại tiền, cột phải**), tiêu đề + dòng
      *Ngày … Tháng … Năm …* theo **ngày tạo**, dòng *- Tỷ giá ngoại tệ* (chỉ phiếu ngoại tệ),
      khối ký 3 ô Ban giám đốc / Kế toán trưởng / Người lập phiếu
- [x] Bảng chi tiết theo `getBillAdjustDeptTableAttribute()` (9 cột) và
      `getBillAdjustDeptWithExchangeRateTableAttribute()` (11 cột, mỗi bên tách ngoại tệ + VND)
- [x] Bảng chi tiết để **AUTO-LAYOUT như ERP** (không `table-layout: fixed`, không `<colgroup>` %).
      Đây chính là "text bị chèn": trang cũ khai `fixed` + cột tiền **9%** + `white-space: nowrap`
      → `1,800,000,000,000` không xuống dòng được nên tràn ra và ĐÈ LÊN ô bên cạnh.
      `nowrap` giữ nguyên (không được cắt đôi con số) — nó chỉ hại khi đi kèm `fixed`
- [x] `BillAdjustDeptPrintService::render()` trả chuỗi HTML (dùng lại `data()` sẵn có)
- [x] `BillAdjustDeptController::printData()` trả `['template' => …]`
- [x] GIỮ NGUYÊN `BillAdjustDeptPrintService::data()` — `BillAdjustDeptExport` (Excel 1 phiếu)
      đang dùng chung, đụng vào là lệch số Excel
- [x] Dòng *- Tỷ giá ngoại tệ* in **2 số lẻ** (282.64), KHÔNG làm tròn kiểu ERP (in ra "283"):
      khớp với file Excel 1 phiếu của HRM (`exports/bill_adjust_dept.blade.php` :200)
- [x] Dòng *- Tỷ giá ngoại tệ* **căn TRÁI** (user chốt 07/09) — khai `text-align: left !important`
      cho `.bkt-rate`, không dựa vào kế thừa (nền chung đặt `text-align: left` ở gốc không `!important`)
- [x] Bỏ tên người duyệt / người lập dưới khối ký (trang `/print.vue` cũ tự thêm, mẫu ERP không có)

### 15.2 FE — popup xem trước, bỏ trang /print

- [x] `index.vue` + `_id/index.vue`: `reportPrintPreviewMixin` + `ReportPrintPreviewModal`,
      thay `window.open('/finance/bill-adjust-depts/{id}/print')`
- [x] Gọi thẳng `loadPrintPreview(url, title, true)` — **khổ NGANG**; `openPrintDetail()` của mixin
      cứng khổ dọc (đúng cách màn Đề nghị đang làm)
- [x] Xoá `pages/finance/bill-adjust-depts/_id/print.vue`

### 15.3 Kiểm chứng

- [x] BE render thật 2 ca trên `gop_db`: phiếu VNĐ id 12855 (9 cột) + phiếu ngoại tệ id 12852
      RUPEE (11 cột, tách RUPEE/VND mỗi bên) — HTML đúng cấu trúc mẫu ERP
- [x] Nhãn đầu mục ra `<strong>`, "Diễn giải" cùng hàng "Loại tiền"
- [x] FE compile sạch (vue-template-compiler + babel), không còn tham chiếu nào tới trang `/print`
- [ ] **Xem bằng mắt trên trình duyệt** (user tự mở): popup mở đúng khổ ngang, không còn số tiền
      đè lên ô bên cạnh, letterhead hiện đúng công ty trên phiếu, nút In trong popup chạy
- [ ] Excel 1 phiếu mở lại 1 file để chắc không đổi (dùng chung `data()`, chỉ đọc)

### Checkpoint — 2026-09-07
Vừa hoàn thành: toàn bộ 15.1 + 15.2, kiểm chứng BE/compile ở 15.3.
Đang làm dở: không.
Bước tiếp theo: user mở trình duyệt nghiệm thu bản in (mục còn `[ ]` ở 15.3) rồi phản hồi Redmine #11307.
Blocked:

### Checkpoint — 2026-09-07 (cuối phiên)

Vừa hoàn thành: Redmine #11306 (3 lỗi xuất Excel) + 8 việc phát sinh trong phiên.

**Đụng vào những file nào**

| Repo | File |
| --- | --- |
| hrm-api | `Exports/BillAdjustDeptExport.php` · `Resources/views/exports/bill_adjust_dept.blade.php` · `Services/BillAdjustDeptPrintService.php` · `Services/BillAdjustDeptService.php` · `Services/BillAdjustDeptWriteService.php` · `Services/BillAdjustDeptPickerService.php` · `Http/Controllers/V1/BillAdjustDeptController.php` · `Http/Requests/BillAdjustDept/BillAdjustDeptStoreRequest.php` · `Routes/api.php` |
| hrm-client | `pages/finance/bill-adjust-depts/index.vue` · `components/BillAdjustDeptForm.vue` · `components/AccountingDetailTable.vue` · `components/BillAdjustDeptRequestPickerModal.vue` · **`components/V2BaseSelectInModal.vue` (DÙNG CHUNG — user đồng ý sửa)** |

**2 lỗi NẶNG lộ ra khi kiểm chứng, không nằm trong issue gốc**
1. `$this->get('status')` không đọc JSON body ⇒ **"Lưu và duyệt" bỏ qua TOÀN BỘ rule `required`**,
   duyệt lọt phiếu thiếu dữ liệu và GHI THẲNG SỔ CÁI. Đã sửa; còn **18 FormRequest** khác toàn dự
   án dùng `$this->get()` — chưa đụng, cần báo team.
2. select2 ghim cuộn của vùng cuộn cha và **gỡ hụt khi danh sách bị lọc ngắn lại** ⇒ popup cuộn
   giật giật tới khi F5. Đã vá ở `V2BaseSelectInModal`.

Đang làm dở: không có.

Bước tiếp theo:
1. User rà lại trên local (Ctrl+Shift+R) — nhất là 2 việc chỉ trình duyệt mới chốt được: xuất Excel
   danh sách >12.000 dòng (tiến độ + file đủ cột) và popup tick sẵn đúng cột đang hiện.
2. Deploy 1 lượt cả 2 repo. ⚠️ Bản vá `V2BaseSelectInModal` là component dùng chung — sau khi lên
   nên bấm thử vài popup có ô select ở màn khác.
3. Quyết 3 việc đang treo: ô "Số phiếu YC xuất hàng" có đổi sang kiểu bấm-thẳng-vào-ô không ·
   có vá `$this->get()` cho 18 FormRequest còn lại không · có rà `V2BaseSelect` /
   `V2BaseSelectRemote` cùng lỗi ghim cuộn không.

Blocked: không.

