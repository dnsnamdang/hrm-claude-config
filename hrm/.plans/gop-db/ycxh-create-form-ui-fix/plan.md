# Plan — Sửa UI màn Tạo Yêu cầu xuất hàng (`/finance/product-export-requests/create`)

> Phụ trách: @namdangit · Nhánh: `gop_db` · Tạo: 2026-09-15
> Chuẩn tham chiếu ("làm chuẩn"): `/finance/bill-payment-requests/create`
> File chính FE: `hrm-client/pages/finance/product-export-requests/components/ProductExportRequestForm.vue`
> File chính BE: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/ProductExportRequestController.php`

Nguồn: Redmine + 4 ảnh chụp màn. 3 nhóm bug.

## Fix #2 — Thanh nút form (viền trắng đè menu + thứ tự "Quay lại")
- [x] FE: thay khối tự dựng `.export-actionbar` (`position:fixed; left:0; right:0; padding-left:80px`) bằng `<V2Footer>` — footer chuẩn `right:0` content-width, KHÔNG đè sidebar, tự render "Quay lại" ở CUỐI (đúng skill list-page 7.2 + button-convention).
  - menu: `{ submit_and_draft: true, save_and_submit_approve: true, submit_and_continue: !isEdit }`
  - `@submitAndDraft="onSubmitClick(3)"` · `@saveAndSubmitApprove="onSubmitClick(2)"` · `@submitAndContinue="onSubmitClick(3, true)"` · `@goBack="$emit('back')"`
- [x] FE: bỏ inline `padding-bottom: 72px` ở div gốc (V2Footer tự thêm spacer `body.has-v2-footer`).
- [x] FE: gỡ SCSS `.export-actionbar` (đã chết).
- [x] FE: import + đăng ký `V2Footer`.

## Fix #3 — "Kho xuất" hiển thị "Mã - tên" (đang chỉ hiện tên)
- [x] BE `createData()`: `->get(['id', 'name'])` → `->get(['id', 'code', 'name'])`.
- [x] BE `editData()`: dựng nhãn kho merge = `"<code> - <name>"` (áp cho cả Kho xuất + Kho nhập, giữ được kho đã khoá).
- [x] FE `fetchWarehouses()`: label = `w.code ? \`${w.code} - ${w.name}\` : w.name` (null-guard). Áp cho cả 2 select (Kho xuất + Kho nhập, chung `warehouseOptions`).

## Fix #1 — Section header + form đính kèm theo chuẩn bill-payment
**Hướng đã chốt: Cách A** — bê nguyên `AttachmentSection` (prop `apiBase` nên BE-agnostic) + 3 endpoint BE; section header đổi từ `.c-section`/icon badge màu sang `V2BaseFormSection` (nền trắng, icon xanh brand) như bill-payment.

- [x] BE `ProductExportRequestController`: thêm `uploadFiles` (`POST /upload-files` → `CmcS3Helper::putFiles` trả mảng URL), `attachmentSizes` (`GET /{id}/attachment-sizes` → map `{file_path: file_size}` từ bảng `files`), `deleteFile` (`DELETE /{id}/files?file_url=` → gate canEdit, xoá row `files` theo file_path + object S3). Const `S3_FOLDER`.
- [x] BE `store`/`update`: sau khi lưu gọi `persistAttachmentUrls($id, attachment_urls)` — ghi URL vào bảng `files` (append, bỏ URL đã có, tên suy từ basename). Thêm rule `attachment_urls`/`attachment_urls.*` vào base `rulesForType`.
- [x] BE Routes: `POST /upload-files` (tĩnh, TRƯỚC `/{id}`), `GET /{id}/attachment-sizes`, `DELETE /{id}/files`. Giữ lại route `/{id}/attachments` cũ (không dùng nữa nhưng vô hại).
- [x] FE `ProductExportRequestForm`: thay khối `.attach-block` tự dựng bằng `<AttachmentSection api-base="assign/product-export-requests">` (khối riêng, sibling — không lồng trong "Thông tin chung"); `pendingFiles` đổi thành `[{url,name,size}]`; computed `attachmentFileUrls`; handlers `onAddUploadedFile`/`removePendingAttachment`/`replaceAttachment`/`removeSavedAttachment`; payload thêm `attachment_urls`; gỡ 4 method + SCSS `.attach-*` cũ. Import + đăng ký `AttachmentSection`.
- [x] FE section header: 2 khối `.c-section` → `<V2BaseFormSection>` với `#title` (icon xanh brand + text) + `#actions` (meta người tạo / nút "Thêm hàng hoá"). Gỡ SCSS `.c-section`/`.section-header`/`.sec-goods`/`.section-body`, thêm `.text-brand` + `.header-meta`. Import + đăng ký `V2BaseFormSection`.
- [x] FE `create.vue` + `_id/edit.vue`: gỡ lời gọi `uploadPendingFiles(id)` sau lưu (đính kèm nay gửi kèm `attachment_urls[]`).

### Checkpoint — 2026-09-15 (Fix #1 code xong + verify tĩnh)
Vừa hoàn thành: Fix #1 (Cách A) — BE 3 endpoint + persist attachment_urls, FE AttachmentSection + V2BaseFormSection. Cả 3 fix đã code xong.
Đã verify (mức tối đa môi trường cho phép):
- FE: 5 SFC (form, create, edit, AttachmentSection, V2BaseFormSection) compile SẠCH bằng `vue-template-compiler` của chính project (Node 14). CR=0.
- FE: dev server :3000 phục vụ route `/finance/product-export-requests/create` HTTP 200, không có marker "Failed to compile / Build error".
- BE: routes `upload-files` (dòng 689, tĩnh — trước `/{id}`), `attachment-sizes` (705), `files DELETE` (706) có mặt; methods `uploadFiles/attachmentSizes/deleteFile/persistAttachmentUrls` + const `S3_FOLDER` + rule `attachment_urls` có mặt; `php -l` sạch cả Routes + Controller.
BLOCKED — verify Playwright trực quan CHƯA chạy được: checkout này KHÔNG có Playwright MCP, KHÔNG có thư mục `e2e/`, và máy chỉ có Node 12/14 (harness cần Node 20). Cần user chạy `--project=setup` + bộ e2e trên môi trường có Node 20, hoặc tự mắt nhìn tại http://127.0.0.1:3000/finance/product-export-requests/create (2 dev server đang chạy).
Bước tiếp theo: chờ user xác nhận cách verify trực quan (mở trình duyệt xem, hoặc bổ sung harness Playwright).

## Fix #4 — Đưa ô "Xuất thẳng" lên ngang hàng với "Loại yêu cầu" (2026-10-15)
Yêu cầu user (kèm screenshot màn tạo loại "Xuất điều chuyển kho nội bộ"): checkbox "Xuất thẳng" đang chiếm 1 hàng riêng bên dưới → đưa lên **ngang cạnh "Loại yêu cầu"**.

- [x] FE `ProductExportRequestForm.vue`: di chuyển block `<div v-if="showField('is_export_direct')" ... Xuất thẳng>` từ vị trí cũ (sau cụm Thông tin khách hàng, trước "Cần lắp đặt") lên **ngay sau ô "Loại yêu cầu"** (sau `errorFields.type`, trước ô "Hợp đồng"). Giữ nguyên `col-md-3 ... d-flex flex-column justify-content-end` (checkbox canh đáy, thẳng hàng với các ô có nhãn). "Cần lắp đặt" (loại HĐ 20/21) giữ nguyên vị trí cũ.
- [x] Verify Playwright MCP tại `http://127.0.0.1:3000/finance/product-export-requests/create`:
  - Loại "Xuất điều chuyển kho nội bộ": hàng 1 = Loại yêu cầu · **Xuất thẳng** · Kho xuất · Kho nhập; Vận chuyển xuống hàng 2 — khớp yêu cầu.
  - Loại "Xuất bán hàng" (type 14, có Hợp đồng hãng/Nhóm VAT/Cần lắp đặt): "Xuất thẳng" cạnh Loại yêu cầu, các ô còn lại xếp gọn 4 ô/hàng, "Cần lắp đặt" cuối hàng 2 — không vỡ layout.
- Chỉ đổi thứ tự markup 1 field, không đổi logic hiển thị (`showField('is_export_direct')` giữ nguyên = type ≠ 3 (mượn) và ≠ 15 (KM hãng)).
- [x] FE (bổ sung theo yêu cầu tiếp): dời luôn block "Cần lắp đặt" (`v-if="isContractType || isFirmContractType"`, radio `need_repair`) lên **ngay sau "Xuất thẳng"**. Trước đó nó nằm sau panel "Thông tin khách hàng" (col-12) nên rơi xuống 1 hàng riêng; nay 2 ô toggle (Xuất thẳng + Cần lắp đặt) đứng cạnh nhau cạnh "Loại yêu cầu".
  - Verify loại "Xuất bán hàng" (type 14): hàng 1 = Loại yêu cầu · Xuất thẳng · **Cần lắp đặt** · Hợp đồng hãng; hàng 2 = Nhóm VAT · Chọn nhóm hàng hóa · Kho xuất · Vận chuyển — gọn, không còn hàng lẻ.

## Fix #5 — Ô "Số km dự kiến" khác size/bo góc/font so với select "Vận chuyển" (2026-10-15)
Yêu cầu user (kèm screenshot): "Trường số km dự kiến điều chỉnh size + bo góc cho giống ô vận chuyển + Tăng size chữ cho bằng mục chọn vận chuyển".

- Nguyên nhân: ô km là `<input type="number" class="form-control form-control-sm">` THÔ (vi phạm quy ước V2Base*). Đo thực tế: font **10.24px**, bo góc **3.2px**, height 36px — lệch hẳn select "Vận chuyển" (font 12px, bo góc 5px, height 32px).
- [x] FE `ProductExportRequestForm.vue`: thay raw `<input type="number">` bằng `<V2BaseInput type="number" size="sm" min="0" step="any" placeholder="Nhập số km" v-model.number="form.total_km_expected" :class="{ 'is-invalid': errorFields.total_km_expected }" />`. Component đã được import (dòng 1217) + đăng ký (dòng 1271) sẵn → không thêm import.
  - Chọn `size="sm"` vì đo khớp select: `.v2-input--sm` font 12px + base radius 5px → render ra đúng font **12px**, bo góc **5px**, height **32px** = KHỚP TUYỆT ĐỐI select "Vận chuyển".
- [x] Verify Playwright MCP (loại "Xuất điều chuyển kho nội bộ", transition_type=2 để ô km hiện):
  - Đo `getComputedStyle`: km {font 12px, height 32px, radius 5px} = select {font 12px, height 32px, radius 5px} — khớp cả 3 chỉ số.
  - `v-model.number` giữ nguyên: gõ "21345" → `form.total_km_expected = 21345` (type number) — binding OK.
  - Screenshot: ô km ngang hàng Vận chuyển, cùng chiều cao/bo góc/cỡ chữ.
- Dọn luôn 1 vi phạm quy ước V2Base* (raw `<input>`) ở field này. Các raw input khác trong thư mục (checkbox dạng switch-line, ô SL trong bảng hàng hoá, select trong modal) là pattern CÓ SẴN, ngoài phạm vi yêu cầu — không đụng.

## Fix #6 — Đặt tên cột thao tác cuối bảng chi tiết hàng hoá = "Hành động" (2026-10-15)
Yêu cầu user (kèm screenshot, chỉ vào cột cuối có nút): "Đổi nút Xóa thành Hành động" — loại nào có nút ở cuối dòng thì đổi header cột đó thành "Hành động".

- Rà soát: trong màn tạo YCXH, chỉ `ManualLinesTable.vue` (dùng cho loại nhập tay 3/6/7/12/18/99) có cột cuối chứa NÚT thao tác (nút ＋ thêm + nút 🗑 xoá). Header cột này trước để TRỐNG. Các bảng còn lại không đổi: isContractType (20/21) + isFirmContractType (14) dùng checkbox chọn dòng, cột cuối là "Hình ảnh"/"Thành tiền sau VAT" (không có nút); isBranchTransfer (7) read-only.
- [x] FE `ManualLinesTable.vue` dòng 23: `<th style="width: 70px"></th>` → `<th class="text-center" style="width: 90px">Hành động</th>` (nới 70→90px cho đủ chữ + 2 nút, canh giữa).
- Số cột vẫn 12 → colspan hàng "Tổng cộng" (6+1+2+1+2) và hàng rỗng (colspan 12) không đổi.
- [x] Verify Playwright MCP (loại "Xuất điều chuyển kho nội bộ" type 6, inject 1 dòng hàng): header cuối = "Hành động", cột vẫn chứa đúng 2 nút `ri-add-line` + `ri-delete-bin-line`. Screenshot xác nhận.

## Fix #7 — Màn CHI TIẾT: đưa "Xuất thẳng" + "Cần lắp đặt" lên ngay cạnh "Loại yêu cầu" cho mọi loại (2026-10-15)
Yêu cầu user (nguyên văn): "màn chi tiết yêu cầu xuất hàng tất cả các loại đều phải để xuất thẳng và cần lắp đặt lên cạnh loại yêu cầu xuất giống màn tạo, sửa".

- Hiện trạng: trên nhánh render `detail` (read-only) của `ProductExportRequestForm.vue`, block "Xuất thẳng" + "Cần lắp đặt" đang nằm Ở CUỐI (sau panel Thông tin khách hàng, sau Kho xuất/Vận chuyển...). Màn tạo/sửa đã đặt 2 ô này ngay sau "Loại yêu cầu" (Fix #4) → chi tiết lệch.
- [x] FE `ProductExportRequestForm.vue`: di chuyển 2 `<div>` block ("Xuất thẳng" switch-line--disabled + "Cần lắp đặt" `V2BaseRadio` disabled) từ vị trí cũ (sau panel Thông tin khách hàng) lên NGAY SAU ô "Loại yêu cầu" (trước ô "Hợp đồng"). Chỉ đổi THỨ TỰ, giữ nguyên markup disabled/read-only + điều kiện v-if sẵn có:
  - Xuất thẳng: `v-if="showField('is_export_direct') || detailIsBorrow"`.
  - Cần lắp đặt: `v-if="detailShowNeedRepair || detailIsBorrow"`.
- [x] Verify Playwright MCP tại màn chi tiết, 3 loại đại diện — thứ tự hàng đầu đúng cho mọi loại:
  - Loại 6 "Xuất điều chuyển kho nội bộ" (39305): Mã phiếu · Loại yêu cầu · **Xuất thẳng** · Kho xuất · Kho nhập... (loại này không có Cần lắp đặt — đúng, need_repair chỉ loại HĐ/borrow).
  - Loại 3 "Xuất mượn" (39304, detailIsBorrow): Mã phiếu · Loại yêu cầu · **Xuất thẳng · Cần lắp đặt** · Kho xuất · Ngày cần mượn...
  - Loại 14 "Xuất bán hàng" HĐ hãng (39254): Mã phiếu · Loại yêu cầu · **Xuất thẳng · Cần lắp đặt** · Hợp đồng hãng · Nhóm VAT...
  - Cả 3 loại: 2 ô đứng sát ngay sau "Loại yêu cầu", không bị ô type-specific chen vào giữa = khớp màn tạo/sửa.

## Fix #8 — Loại "Xuất điều chuyển kho chi nhánh" (type 7): ô chọn "Phiếu yêu cầu chuyển hàng" theo kiểu ERP (2026-10-15)
Yêu cầu user (kèm 3 screenshot): màn tạo/sửa YCXH loại type 7, khối chọn "Phiếu yêu cầu chuyển hàng" sửa lại theo kiểu bên ERP.

- Đối chiếu ERP (`resources/views/warehouse/product_export_requests/form.blade.php:250-273`): 1 ô viền (`form-control`) gom TẤT CẢ chip + nút ＋ trên cùng 1 hàng; chip dạng badge có nút ✕; khi chưa chọn hiện chữ "Chưa chọn phiếu yêu cầu chuyển hàng"; nút ＋ luôn ở cuối để mở modal chọn.
- HRM trước đây: chip rời (`.transfer-chips`) + nút full-width dạng dotted "Chọn thêm phiếu"/"Chọn phiếu yêu cầu chuyển hàng" (`.contract-choose`) nằm DƯỚI — khác hẳn ERP.
- [x] FE `ProductExportRequestForm.vue` (nhánh create/sửa, block `v-if="isBranchTransfer"`): thay bằng ô viền `.transfer-box` gom:
  - placeholder `.transfer-box__empty` "Chưa chọn phiếu yêu cầu chuyển hàng" khi `!transferRequests.length`;
  - `v-for` chip `.transfer-chip` (giữ nguyên style cũ: pill indigo + nút ✕ `.transfer-chip__del`, ẩn khi `transferLocked`);
  - nút ＋ vuông `.transfer-add` (indigo #4f46e5 khớp accent chip, 26×26, radius 5px) mở `openTransferModal`, ẩn khi `transferLocked`.
  - Lỗi validate: `.transfer-box--invalid` (viền đỏ #dc3545) + `.fld-err` giữ nguyên.
- [x] CSS mới: `.transfer-box` (border #cbd5e1 + radius 5px khớp V2BaseInput, min-height 32px, flex-wrap), `.transfer-box--invalid`, `.transfer-box__empty` (#6b7280 xám), `.transfer-add`. Giữ `.transfer-chips`/`.transfer-chip`/`.transfer-chip__del` (chip read-only màn chi tiết vẫn dùng `.transfer-chips`). `.contract-choose` vẫn dùng ở khối chọn hợp đồng khác → không xoá.
- [x] Verify Playwright MCP tại `/_id/edit` loại type 7 (39284):
  - Khi rỗng: ô viền hiện "Chưa chọn phiếu yêu cầu chuyển hàng" + nút ＋ (khớp ERP screenshot 3).
  - Inject 2 phiếu: chip `PYCCH-08114 ×` · `PYCCH-08115 ×` rồi nút ＋, tất cả trong 1 ô viền 1 hàng (khớp ERP screenshot 2). Box {border #cbd5e1, radius 5px}, nút ＋ {bg #4f46e5, 26×26, radius 5px}, chip {bg #eef0fe, color #4f46e5, pill}.
- Màn chi tiết (read-only) giữ nguyên `.transfer-chips` (chip chỉ đọc, không có nút chọn) — user chỉ yêu cầu "chỗ chọn" = màn tạo/sửa.

## Fix #9 — Modal "Chọn phiếu yêu cầu chuyển hàng": link mã phiếu + checkbox chọn tất cả ở tiêu đề (2026-10-15)
Yêu cầu user (kèm screenshot, khoanh đỏ header "Chọn"): (1) thêm link vào cột mã phiếu; (2) đổi tiêu đề cột "Chọn" thành checkbox, click chọn tất cả bản ghi.

- File `TransferRequestSearchModal.vue` (popup multi-select loại 7).
- [x] Cột "Mã phiếu": `{{ t.code }}` → `<nuxt-link :to="/finance/product-transfer-requests/${t.id}" target="_blank" rel="noopener" class="code-link" @click.native.stop>`. `@click.native.stop` chặn nổi bọt lên `@click="toggle(t)"` của hàng (bấm link mở tab mới, KHÔNG tick chọn). CSS `.code-link` (indigo #4f46e5, bold, underline khi hover).
- [x] Header cột "Chọn": chữ "Chọn" → `<input type="checkbox" :checked="allChecked" :disabled="!rows.length" title="Chọn tất cả" @click="toggleAll" />`.
  - computed `allChecked` = `rows.length > 0 && rows.every(isChecked)`.
  - method `toggleAll()`: đang chọn hết → lọc bỏ mọi dòng hiển thị khỏi `checked`; chưa đủ → push các dòng chưa tick. Thao tác theo `rows` hiện tại (an toàn khi đã search lọc).
- [x] Verify Playwright MCP (modal mở từ edit type 7 phiếu 39284, 2 dòng PYCCH-06924/06859):
  - Link mã phiếu: href `/finance/product-transfer-requests/6924` + `6859`, target `_blank`, màu xanh.
  - Click header checkbox: 2 dòng tick hết, footer "Chọn (2)". Click lại: bỏ hết, footer "Chọn (0)" (xác nhận sau nextTick).
  - Screenshot khớp screenshot user (header là checkbox, mã phiếu là link).

## Fix #10 — Modal "Chọn phiếu yêu cầu chuyển hàng": đổi "Người yêu cầu" → "Người tạo" + bộ lọc Người tạo (dropdown) + cột "Số dòng" → "Ngày tạo" (2026-10-15)
Yêu cầu user (kèm 2 screenshot, khoanh đỏ header "Người yêu cầu" và "Số dòng hàng"): (1) đổi cột "Người yêu cầu" → "Người tạo"; (2) thêm bộ lọc "Người tạo" dạng dropdown; (3) đổi cột "Số dòng hàng" → "Ngày tạo".

- 2 repo: BE `hrm-api` (bổ sung `created_at` vào payload) + FE `hrm-client` (`TransferRequestSearchModal.vue`).
- [x] BE `Modules/Assign/Http/Controllers/Api/V1/ProductExportRequestController.php` method `transferRequestOptions()` (~dòng 1089): thêm vào map payload `'created_at' => $t->created_at ? Carbon::parse($t->created_at)->format('d/m/Y H:i') : null,` (sau `creator_name`). Carbon đã import sẵn (dùng ở dòng 334). Payload giờ trả: id, code, company_id, created_by, creator_name, created_at, products[].
- [x] FE `TransferRequestSearchModal.vue`:
  - Hàng search: col-md-6/6 → col-md-4 (keyword) / col-md-4 (dropdown "Người tạo": `V2BaseSelect v-model="creatorFilter" :options="creatorOptions" placeholder="Tất cả người tạo" size="sm"`) / col-md-4 (nút Tìm kiếm + Làm mới).
  - Header: "Người yêu cầu" → "Người tạo"; "Số dòng hàng" (width 100px) → "Ngày tạo" (width 120px, text-center).
  - Cell cuối: `{{ (t.products && t.products.length) || 0 }}` → `{{ t.created_at || '—' }}`.
  - Script: import + đăng ký `V2BaseSelect`. Data: `rows: []` → `rawRows: []`, thêm `creatorFilter: null`. Computed mới `rows()` (lọc rawRows theo creatorFilter; null/'' = tất cả), `creatorOptions()` (distinct created_by → [{value, text: creator_name}]). `allChecked` dùng `this.rows` (filtered). `watch show` + `resetSearch()`: reset creatorFilter=null. `fetch()`: gán `this.rawRows` (cả success + catch); guard: creatorFilter không còn trong rawRows mới → reset null (không ẩn sạch bảng).
- [x] Verify Playwright MCP (modal mở từ edit type 7 phiếu 39284):
  - Header: STT · Mã phiếu · **Người tạo** · **Ngày tạo** ✓.
  - BE trả `created_at` dạng `d/m/Y H:i`: PYCCH-06924 "10/06/2026 14:42" / PYCCH-06859 "04/06/2026 10:35" ✓ (PHP reload per-request, BE đổi có hiệu lực ngay).
  - Dropdown "Người tạo" render 2 option: {986 Bùi Tiến Nam, 31 Đặng Đình Sứng}; placeholder "Tất cả người tạo".
  - Lọc: creatorFilter=31 → 1 dòng (Đặng Đình Sứng); reset null → 2 dòng. Screenshot khớp.

## Fix #11 — Modal "Chọn phiếu yêu cầu chuyển hàng": sort 3 cột + phân trang (2026-10-15)
Yêu cầu user (nguyên văn): "Thêm sort cho mã, người tạo, ngày tạo + Thêm phân trang".

- Chỉ FE `TransferRequestSearchModal.vue` — KHÔNG đụng BE.
- **Quyết định (ruling): sort + phân trang CLIENT-SIDE.** Endpoint `transferRequestOptions()` đã trần 100 dòng + lọc `canApprove()` per-row sau truy vấn → dữ liệu đã về hết FE, không có server-side để kẹp. Sort/phân trang trên tập đã có là đúng và rẻ nhất.
- **Chọn-tất-cả (Fix #9) đổi phạm vi theo trang:** header checkbox giờ tick/bỏ các dòng của TRANG HIỆN TẠI (`pagedRows`), không phải toàn bộ filtered — chuẩn UX bảng phân trang (tránh tick ngầm dòng không nhìn thấy).
- Rà pattern có sẵn trước khi làm:
  - Phân trang: `components/V2BasePagination.vue` (`V2BasePagination`) — props `:current-page`/`:current-page-size`/`:total-rows` + `item-label` + `:page-size-options`; emit `page-change`/`page-size-change` (KHÔNG v-model); tự ẩn khi `totalRows===0`.
  - Hằng popup: `utils/pickerPagination.js` → `PICKER_PAGE_SIZE_OPTIONS=[10,20,50,100]`, `PICKER_DEFAULT_PAGE_SIZE=10`.
  - Sort bảng tay: mẫu `pages/customer-care/wr-quotations/components/InformationRequestSearchModal.vue` — `.sortable-header` + icon Remix `ri-arrow-up-down-line`/`ri-arrow-up-line`/`ri-arrow-down-line`.
  - SKILL `modal-popup` mục 5: dưới bảng popup dùng `V2BasePagination` (KHÔNG V2BaseDataTable), số dòng/trang `[10,20,50,100]` mặc định 10.
- [x] FE `TransferRequestSearchModal.vue`:
  - Template: 3 header Mã phiếu/Người tạo/Ngày tạo bọc `<span class="sortable-header" @click="toggleSort('code'|'creator_name'|'created_at')">…<i :class="sortIcon(...)"/></span>`. `v-for="(t,i) in pagedRows"`, STT `{{ pageOffset + i + 1 }}`, empty check vẫn `!rows.length`. Header checkbox `:disabled="!pagedRows.length"` title "Chọn tất cả trang này". Thêm `<V2BasePagination :current-page="safePage" :current-page-size="perPage" :total-rows="rows.length" :page-size-options="pickerPageSizeOptions" item-label="phiếu" @page-change="onPageChange" @page-size-change="onPageSizeChange" />` sau `.contract-table-wrap`.
  - Script: import + đăng ký `V2BasePagination`; import `{ PICKER_PAGE_SIZE_OPTIONS, PICKER_DEFAULT_PAGE_SIZE }`. Data thêm `sortField:'created_at'`, `sortType:'desc'` (mặc định Ngày tạo mới nhất), `currentPage:1`, `perPage:PICKER_DEFAULT_PAGE_SIZE`, `pickerPageSizeOptions:PICKER_PAGE_SIZE_OPTIONS`.
  - Computed thêm: `sortedRows()` (sort `rows.slice()`; ô trống xuống cuối; `created_at` dùng `dateSortKey`; số trừ số, chuỗi `localeCompare('vi')`; sign theo asc/desc), `pageCount`, `safePage` (kẹp [1,pageCount]), `pageOffset`, `pagedRows` (slice). `allChecked` đổi dùng `pagedRows`.
  - Watch: `show` reset thêm sortField/sortType/currentPage=1; watch `creatorFilter` → currentPage=1.
  - Methods: `dateSortKey(s)` (regex `d/m/Y H:i` → `Date.getTime()`, 0 nếu không khớp), `toggleSort(field)` (đảo chiều nếu cùng cột đang asc, else asc; currentPage=1), `sortIcon(field)`, `onPageChange`/`onPageSizeChange` (perPage=size, currentPage=1). `search()`/`resetSearch()`/`fetch()` reset currentPage=1. `toggleAll()` đổi dùng `pagedRows`.
  - CSS scoped: `.sortable-header` (inline-flex, cursor pointer, user-select none) + `.sortable-header i` (font-size 12px, margin-left 4px, color #9ca3af).
- [x] Verify Playwright MCP (modal mở từ edit type 7 phiếu 39284):
  - 2 dòng thật: mặc định sort created_at desc (06924 "10/06" trước 06859 "04/06"); pagination "Hiển thị 1–2 / 2 phiếu"; header icon = [up-down, up-down, down].
  - Inject 25 dòng giả: total 25, pageCount 3 (10/10/5), trang 3 "Hiển thị 21–25 / 25 phiếu".
  - Sort đúng trên 25 dòng: codeAsc/codeDesc/dateAsc/dateDesc đều đúng; creator asc nhóm đúng locale Việt (9 Bùi → 9 Đặng → 7 Trần). (`creatorAscSorted:false` của test là artefact do helper so sánh dùng `<=` trên Unicode "Đ"=U+0110 thay vì `localeCompare('vi')`, KHÔNG phải bug sort.)
  - Screenshot cuối: header "Mã phiếu ↕ / Người tạo ↕ / Ngày tạo ↓", bảng 10 dòng, thanh phân trang + chọn số dòng/trang 10 + trang 1/2/3.

## Fix #12 — Link vào phiếu yêu cầu chuyển hàng đã chọn (chip ngoài form) — cả tạo/sửa/chi tiết (2026-10-15)
Yêu cầu user (kèm screenshot chip "PYCCH-06924" icon xe tải + nút ✕ + nút ＋): "thêm link vào phiếu yêu cầu chuyển hàng đã được chọn ra ngoài màn hình. thêm cả ở tạo, sửa, chi tiết".

- Chỉ FE `hrm-client/pages/finance/product-export-requests/components/ProductExportRequestForm.vue` — KHÔNG đụng BE. (Form này DÙNG CHUNG cho tạo/sửa + chi tiết.)
- Dùng lại pattern link đã có ở Fix #9 (`.code-link` trong modal): biến mã trong chip "Phiếu yêu cầu chuyển hàng đã chọn" thành `nuxt-link` mở `/finance/product-transfer-requests/<id>` tab mới.
- [x] Chip tạo/sửa (nhánh `isBranchTransfer`): wrap `{{ t.code }}` → `<nuxt-link :to="/finance/product-transfer-requests/${t.id}" target="_blank" rel="noopener" class="transfer-chip__link" @click.native.stop>{{ t.code }}</nuxt-link>`. Giữ nguyên `<i class="ri-truck-line">` trước và nút `.transfer-chip__del` (✕) sau. `@click.native.stop` chặn nổi bọt (bấm link KHÔNG kích thao tác chip).
- [x] Chip chi tiết read-only (nhánh `Number(detail.type)===7 && detailTransferRequests.length`): wrap tương tự NHƯNG KHÔNG có `@click.native.stop` (read-only, không có nút ✕).
- [x] CSS scoped thêm `.transfer-chip__link { color: inherit; text-decoration: none; }` + `:hover { text-decoration: underline; }` (ngay trước `.transfer-chip__del`). Chip sẵn bg #eef0fe color #4f46e5 font-weight 600 → link kế thừa màu indigo (không tô đỏ, đúng quy ước màu).
- [x] Verify Playwright MCP:
  - Tạo/sửa (edit type 7 phiếu 39284, inject 2 transferRequests): 2 chip link href `/finance/product-transfer-requests/6924` + `/6859`, target `_blank`, rel `noopener`, color rgb(79,70,229)=#4f46e5; chip vẫn là link xanh + ✕ + nút ＋. (Tạo dùng chung markup nhánh isBranchTransfer → verify luôn.)
  - Chi tiết (detail type 7 phiếu 39284, inject `detail.product_transfer_requests`): 2 chip link href `/finance/product-transfer-requests/6924` + `/6859`, target `_blank`, rel `noopener`, và KHÔNG có nút ✕ (read-only). ✓

## Fix #13 — Chi tiết vẫn hiện "thông tin vận chuyển" sau khi sửa Không xuất thẳng → Xuất thẳng (2026-10-15)
Yêu cầu user (nguyên văn): "Tạo mới = không xuất thẳng → vào sửa lại thành xuất thẳng → vào xem lại chi tiết vẫn đang hiển thị thông tin vận chuyển" (phiếu 39306).

- **Root cause (2 tầng):**
  1. BE `ProductExportRequestService` ghi `transition_type` = `!empty($data['transition_type']) ? (int)$data['transition_type'] : 1` ở MỌI đường ghi (store/update) → **ép mặc định 1**, không bao giờ null. Khi sửa sang Xuất thẳng, FE không gửi `transition_type` (vì `needTransition=false`) → BE lấy mặc định 1. (ERP chỉ set `transition_type` khi `!is_export_direct && hasDeliveryTypes`, còn lại không đụng → ẩn ở blade theo `is_export_direct`.)
  2. FE màn chi tiết: `showField('transition_type_name')` dùng `makeFieldVisibility` có fallback "hiện khi liên-quan HOẶC có-data". Khi Xuất thẳng, relevance=false (`HAS_DELIVERY && !isDirect`) NHƯNG `transition_type_name` còn giá trị ("Nhân viên vận chuyển") → fallback has-data bật → field vẫn hiện.
  - `warehouse_name` KHÔNG dính vì `warehouse_id` được clear null khi bật Xuất thẳng (onExportDirectChange dòng ~2071), nên nó rỗng → fallback không bật.
- **Quyết định (ruling): fix FE display, khớp ERP** (ERP để data sót nhưng ẩn ở view theo `is_export_direct`). Đưa `transition_type_name` + `total_km_expected` vào `flagKeys` của `makeFieldVisibility` → **relevance-only, bỏ fallback has-data** (đúng cơ chế đã dùng sẵn cho `is_export_direct`; comment trong flow-field-visibility.js đã nêu "cờ luôn có value → fallback làm field luôn hiện ở loại không liên quan"). KHÔNG sửa BE 5 đường ghi (rủi ro cao, ERP cũng để data sót).
- Chỉ FE `hrm-client/pages/finance/product-export-requests/components/ProductExportRequestForm.vue` (computed `showField`, ~dòng 1399). Form tạo/sửa dùng `needTransition` (không qua showField) → chỉ ảnh hưởng màn chi tiết read-only. Type 18 relevance luôn true → không bị ẩn nhầm.
- [x] Verify Playwright MCP:
  - 39306 (type 7, is_export_direct=1, transition_type=1): nhãn "Vận chuyển" + "Số km dự kiến" ĐÃ ẨN; chỉ còn Mã phiếu/Loại/Xuất thẳng/Gửi đến công ty/Chọn kiểu nhập kho/Phòng ban/Ghi chú ✓.
  - 39305 (type 6, is_export_direct=0, transition_type=2, km=234): "Vận chuyển" + "Số km dự kiến" VẪN HIỆN ✓ (regression không vỡ).

## Fix #14 — Chọn khách hàng (loại 12 Xuất hàng gửi) chuyển sang dạng popup (2026-10-15)
Yêu cầu user (nguyên văn): "Chọn khách hàng chuyển về dạng show popup như màn https://dev-hrm.eteksofts.com/finance/bill-income-requests/create" (kèm screenshot màn Tạo YCXH).

- **Approach (ruling):** tái dùng `SourcePicker.vue` (trigger ô readonly nhất quán với các ô HĐ cùng form) + mở modal global `@/components/modals/ChooseErpCustomerModal.vue` (nhất quán với màn Thu tiền `bill-income-requests/create`). KHÔNG đụng BE.
- Chỉ FE `hrm-client/pages/finance/product-export-requests/components/ProductExportRequestForm.vue` (dùng chung tạo/sửa/chi tiết). Field "Khách hàng *" chỉ hiện với `needCustomer` = `Number(form.type) === 12`.
- [x] Template: thay `V2BaseSelect` (bound `form.customer_id` + `customerOptions`) bằng khối `.cost-pick` gồm `SourcePicker :value="{ code: customerPickerText }" :invalid="!!errorFields.customer_id" placeholder="Nhấn vào đây để chọn khách hàng" @open="openCustomerModal"` + `V2BaseIconButton v-if="form.customer_id" danger @click="clearCustomer"` (nút xóa). Giữ `.fld-err`.
- [x] Thêm `<ChooseErpCustomerModal v-if="needCustomer" @event="onCustomerEvent" />` (sau `TransferRequestSearchModal`). Import + register component.
- [x] Computed `customerPickerText()`: rỗng nếu chưa chọn, else `"<code> - <name>"` (code từ `customerInfo.customer_code`, name từ `form.customer_name`).
- [x] Thay `fetchCustomers()` + `onCustomerChange()` bằng: `openCustomerModal()` (`$bvModal.show('choose-erp-customer')`); `onCustomerEvent(result)` (guard type `choiceCustomer`, set `form.customer_id/customer_name` + `customerInfo` từ record, xóa errorFields); `clearCustomer()` (reset customer_id/name + customerInfo={}).
- [x] Gỡ `fetchCustomers()` ở onTypeChange; initForm nhánh edit bỏ `fetchCustomers()`+`mergeOption`, thay bằng dựng `customerInfo` từ `d.customer_*`. Gỡ `customerOptions: []` khỏi data.
- [x] Verify Playwright MCP (create, type=12):
  - `needCustomer=true`, picker render INPUT readonly placeholder "Nhấn vào đây để chọn khách hàng", `customerPickerText=""`.
  - Click picker → modal `#choose-erp-customer` mở, tải 10/11082 khách, có bộ lọc Tên/Mã + MST + SĐT + bảng + phân trang (giống màn Thu tiền).
  - Chọn dòng → `customer_id=43709`, `customer_name="CÔNG TY TNHH HUAZHI MATERIALS VIỆT NAM"`, `customerPickerText="15TPHPTA - CÔNG TY TNHH HUAZHI MATERIALS VIỆT NAM"`, customerInfo đầy đủ (code/tax/address), callout "Thông tin khách hàng" hiện, nút xóa xuất hiện, popup tự đóng (screenshot xác nhận).
  - Bấm xóa (`clearCustomer`) → customer_id/name=null, customerInfo={}, customerPickerText="" ✓.

## Fix #15 — Cột "Hình ảnh" ở bảng Chi tiết hàng hoá không hiện (2026-10-15)
Yêu cầu user (nguyên văn): "cột hình ảnh ở màn tạo không thấy hiện, kiểm tra cả màn sửa, chi tiết ở tất cả các loại" (kèm screenshot màn Tạo YCXH loại 12, cột Hình ảnh toàn "—").

- **Bảng liên quan:** `ManualLinesTable.vue` (loại nhập tay 3/6/12/18/19/99) render `<img v-if="row.avatar_url">` else "—" (dòng 56-59). Màn chi tiết read-only render `row.avatar` từ `detailProducts` (Form dòng 1065/1097/1115).
- **Dữ liệu (query DB read-only):** `products.avatar` VÀ `product_export_request_details.avatar` đều là URL S3 tuyệt đối (`https://...`) → `buildProductAvatarUrl` giữ nguyên.
- **3 bug, mỗi mode 1 nguyên nhân:**
  1. **TẠO (hỏng):** modal dùng chung `assign/quotations/components/QuotationProductSearchModal.vue` hàm `applySelection()` map item emit KHÔNG kèm `avatar_url` dù item nguồn CÓ (dòng 153). Form `onProductsApply` đọc `it.avatar_url` (dòng 2577) → luôn null.
  2. **SỬA (hỏng):** BE `editData` nhánh nhập tay `->get([...])` (dòng 1522) KHÔNG select cột `avatar` → FE initForm map `avatar_url: p.avatar` = null (dòng 2523/2546).
  3. **CHI TIẾT (đã chạy):** BE `show` (dòng 1664) ĐÃ select `avatar` (URL đầy đủ) → render được. Chuẩn hoá qua `buildProductAvatarUrl` cho nhất quán + an toàn path tương đối (không bắt buộc để hiện).
- **Ruling sửa hàm dùng chung:** thêm `avatar_url` vào payload emit của `QuotationProductSearchModal.applySelection` là THUẦN ADDITIVE (màn báo giá bỏ qua field thừa) → non-breaking, an toàn. Đây là đường DUY NHẤT sửa được màn Tạo.
- [x] FE modal `applySelection()`: thêm `avatar_url: item.avatar_url || null` vào object map (dòng ~1218).
- [x] BE `editData` (dòng 1522): thêm `'avatar'` vào select + map `avatar` qua `buildProductAvatarUrl` sau `->get()`.
- [x] BE `show` (dòng 1664→1673): map `avatar` của `$products` qua `buildProductAvatarUrl` trước khi gán.
- [x] Verify Playwright MCP (2026-10-15):
  - **TẠO** (type 12): modal tải 26887 hàng kèm `avatar_url` S3; chọn hàng → `manualRows[0].avatar_url` = URL S3, DOM `<img.ycxh-thumb>` render đúng src ✓.
  - **SỬA** (39305 type 6, 2 dòng, created_by=13): `editData` trả `avatar`, 2 `manualRows` có `avatar_url`, 2 `<img.ycxh-thumb>` render ✓.
  - **CHI TIẾT** (39305): `detailProducts[].avatar` = URL S3 (qua buildProductAvatarUrl), 2 `<img.er-ref-img>` render, `naturalWidth` 482 & 2216 (ảnh load thật), 0 lỗi console ✓.

## Fix #16 — Popup "Chọn hợp đồng / đơn hàng" (loại 19) đồng bộ layout CSS với popup chọn khách hàng (2026-10-15)
Yêu cầu user (nguyên văn): "cái popup này nên sử dụng layout css giống popup chọn khách hàng lúc nãy" (kèm screenshot popup "Chọn hợp đồng / đơn hàng" cũ: header icon phẳng, select native, footer "Đóng" trôi, modal size xl hẹp).

- **Component:** `hrm-client/pages/finance/product-export-requests/components/EmplementContractSearchModal.vue` (modal chọn HĐ cho YCXH **loại 19** "Xuất thực hiện hợp đồng"; nguồn UNION ERP firm_contracts + wr_service_contracts qua `assign/product-export-requests/emplement-contracts`, phân trang + sort server-side). Chỉ dùng ở `ProductExportRequestForm.vue` (`:show` + `@close` + `@select`) — KHÔNG shared rộng → rewrite presentation an toàn.
- **Target khuôn:** `components/modals/ChooseErpCustomerModal.vue`.
- **Ruling khuôn:** rewrite từ `V2BaseModal` + `V2BaseDataTable` sang `b-modal` full-width + `b-table` theo khuôn customer modal. Giữ **sort server-side** bằng `b-table no-local-sorting` + `@sort-changed` (map field key → khoá BE qua SORT_KEYS) để KHÔNG mất mũi tên sort (customer modal gốc không có sort). Đổi native `<select>` Loại hợp đồng → `V2BaseSelectInModal` (tuân CLAUDE.md "Select trong modal dùng V2BaseSelectInModal"). Giữ nguyên contract props/emit (`show`/`close`/`select`), logic fetch + SORT_KEYS + linkOf + pick.
- [x] Rewrite template: `b-modal` id `emplement-contract-search-modal`, `hide-footer size="xl" modal-class="modal-full-width-emplement" content-class="shadow" body-class="p-0"`; custom `#modal-header` icon tròn (`ri-file-text-line`, nền `rgba(22,163,74,0.1)` xanh #16a34a) + title 14px/800 + nút X; `.choose-contract-body` flex column.
- [x] Bộ lọc `.picker-filter`: `V2BaseSelectInModal` (Loại HĐ, `@change=onContractTypeChange`) + 2 `V2BaseInput` (Số HĐ, Khách hàng, `@keyup.enter.native=search`) + nút Tìm kiếm (primary, `mr-2`) + Làm mới (tertiary).
- [x] `.table-shell` (viền #e5e7eb, radius 8px): `.table-top-scroll` (cuộn ngang TRÊN) + `.table-wrapper` chứa `b-table` (`data-table` min-width 1100px, sticky thead, hover #f0fdf4, `@row-clicked=pick`, `no-local-sorting` + `:sort-by.sync`/`:sort-desc.sync` + `@sort-changed=onSortChanged`). Cột: STT/Ngày lập/Loại HĐ/Số HĐ/Khách hàng/Tổng thanh toán/Ngày duyệt/Người duyệt; sortable = created_at/type_name/code/total/approved_time. Scroll 2 chiều đồng bộ qua `createScrollSyncHandlers` + `syncTopScrollWidth`.
- [x] `V2BasePagination` (item-label "hợp đồng", PICKER_PAGE_SIZE_OPTIONS) + `.modal-footer` ghim đáy nút "Đóng" (tertiary, `fas fa-arrow-left`).
- [x] Script: thêm `onModalShow`(resetSearch)/`onModalShown`(bindScrollSync)/scroll handlers/`closeModal`/`onContractTypeChange`/`onSortChanged`/`handlePageChange`/`handlePageSizeChange`; watch `show` → `$bvModal.show/hide(MODAL_ID)`; `@hidden` → emit close; pick → emit select + hide.
- [x] CSS: `.modal-full-width-emplement` (dialog 95vw, ≥1400px cap 1350px; content 94vh flex column; header padding 8px 16px; body flex padding 0) + col width classes; **col-code thêm `overflow-wrap: anywhere` + `word-break: break-word`** (mã HĐ toàn dấu `_` không khoảng trắng, không thì tràn đè cột Khách hàng).
- [x] Verify Playwright MCP (2026-10-15, type=19):
  - Layout: dialog 1140px = 95vw (viewport ~1200), content 840px ≈ 94vh, header icon tròn xanh, footer "Đóng" ghim đáy phải — khớp customer modal ✓.
  - Top-scroll đồng bộ: `topInnerWidth=1226px` = `tableScrollWidth`, cuộn ngang TRÊN + DƯỚI đều hiện ✓.
  - Sort server-side 2 chiều: total asc → [0,0,0,0,0]; total desc → [111.7 tỷ, 104.9 tỷ, ...] ✓.
  - Filter Loại HĐ (wr-1): total 1005, chỉ "Hợp đồng sửa chữa - bảo dưỡng - bảo trì", source=wr, object_type `App\Model\Customers\WrServiceContract` ✓.
  - Chọn dòng: parent `selectedEmplementContract` = {code HDDV_TPSG_SG_CSKH_26_0155_07584, KH VĂN THÀNH HIỆP}, modal tự đóng (showFlag false) ✓.
  - Mã HĐ dài ngắt dòng trong ô, không đè cột Khách hàng ✓.
- **Chưa làm (chờ user quyết):** `FirmContractSearchModal.vue` (loại 14 HĐ hãng) + `TransferRequestSearchModal.vue` cùng khuôn cũ `V2BaseModal`+`V2BaseDataTable` — user CHƯA yêu cầu đổi; đề xuất đồng bộ luôn cho nhất quán, chờ xác nhận.

## Fix #17 — Popup "Chọn hợp đồng chi phí" (loại 99) đồng bộ layout CSS như Fix #16 (2026-10-15)
Yêu cầu user (nguyên văn): "chọn chi phí hợp đồng loại xuất khác popup sửa tương tự" (kèm screenshot popup "Chọn hợp đồng chi phí").

- **Component:** `hrm-client/pages/finance/product-export-requests/components/ContractCostModal.vue` (modal chọn HĐ chi phí cho YCXH **loại 99** "Ghi nhận chi phí hợp đồng"). Dùng duy nhất ở `ProductExportRequestForm.vue` (ref `costModal`, mở bằng `openCostModal()` → `$refs.costModal.show(contract_costable_key)`; `@select="onCostContractSelect"`; props `sources`=`costContractSources`, `customerId`). Nguồn: ERP cost-contracts qua `assign/product-export-requests/cost-contracts` (contract_type + customer_id + code + customer + sort_by + sort_desc + page + per_page), có select "Loại hợp đồng" chọn bảng nguồn (11 nhóm: contracts/service/project/opening/hrm…).
- **Hiện trạng trước fix:** đã dùng `V2BaseSelectInModal` cho "Loại hợp đồng" nhưng vẫn dựng trên `V2BaseModal` (size xl) + `V2BaseDataTable` — CHƯA full-width như popup khách hàng/emplement.
- **Ruling:** rewrite presentation từ `V2BaseModal`+`V2BaseDataTable` sang `b-modal` full-width + `b-table` theo khuôn `ChooseErpCustomerModal.vue` (giống Fix #16). **GIỮ NGUYÊN interface ref-based** (`show(currentKey)`/`hide()`, emit `select({id,code,key})`, props `sources`/`customerId`, watcher sources+sourceKey, SORT_KEYS code/customer_name, logic fetch + guard `loadingPage`/`key!==sourceKey`). KHÔNG đổi `:show` prop (parent gọi qua ref).
- [x] Rewrite template: `b-modal` id `contract-cost-modal` `modal-class="modal-full-width-cost-contract"` + custom `#modal-header` icon tròn xanh (`ri-file-text-line`) + title "Chọn hợp đồng chi phí" 14px/800 + nút X; `.choose-contract-body` flex column.
- [x] Bộ lọc `.picker-filter`: `V2BaseSelectInModal` (Loại HĐ, `v-model="sourceKey"` `allowClear=false` — luôn phải chọn 1 nhóm, không có "Tất cả") + 2 `V2BaseInput` (Số HĐ / Khách hàng, `@keyup.enter.native=search`) + nút Tìm kiếm + Làm mới.
- [x] `.table-shell` + `.table-top-scroll` (cuộn ngang TRÊN) + `.table-wrapper` chứa `b-table` (`no-local-sorting` + `:sort-by.sync`/`:sort-desc.sync` + `@sort-changed=onSortChanged` + `@row-clicked=pick`); cột STT/Mã hợp đồng(sort)/Khách hàng(sort)/Địa chỉ; scroll 2 chiều đồng bộ `createScrollSyncHandlers` + `syncTopScrollWidth`; cell() default '—' cho ô rỗng.
- [x] `V2BasePagination` (item-label "hợp đồng") + `.modal-footer` ghim đáy nút "Đóng" (tertiary, `fas fa-arrow-left`).
- [x] Script: bỏ V2BaseModal/V2BaseDataTable/onTableClick; thêm `onModalShown`(bindScrollSync+syncWidth)/scroll handlers/`onSortChanged`/`handlePageChange`(giữ guard loadingPage)/`handlePageSizeChange`; `show()`/`hide()` chuyển sang `$bvModal.show/hide(MODAL_ID)`; `pick` emit `{id,code,key}` + hide.
- [x] CSS: `.modal-full-width-cost-contract` (dialog 95vw ≤1350px, content 94vh flex column, header/body padding) + **col-code `overflow-wrap: anywhere` + `word-break: break-word`** (mã HĐ toàn dấu `_`); data-table min-width 700px (4 cột).
- [x] Verify Playwright MCP (2026-10-15, type=99):
  - Layout: dialog 1140px = 95vw (viewport 1200), content 840px = 94vh, header icon tròn xanh, footer "Đóng" ghim đáy — khớp customer modal ✓.
  - Top-scroll đồng bộ: `topInnerWidth=1106px` = `wrapperScrollW` ✓.
  - Render dữ liệu (bơm 3 dòng vì DB rỗng thật): STT + mã HĐ dài ngắt 2 dòng không đè cột KH + ô rỗng hiện '—' ✓; phân trang "Hiển thị 1–10 / 23 hợp đồng", trang 1/2/3 ✓.
  - Sort server-side: `onSortChanged({sortBy:'code',sortDesc:true})` → URL `cost-contracts?...&sort_by=code&sort_desc=1` ✓.
  - Chọn dòng: `pick(rows[1])` → parent `form.contract_costable_id=102`, `contract_costable_key="1"`, `costContractCode="HD_TPSG_0002"`, modal đóng ✓.
  - Endpoint cost-contracts trả 200 total=0 cho mọi nhóm (user/công ty test không có HĐ chi phí) — điều kiện dữ liệu BE, KHÔNG phải bug FE; bản cũ cũng rỗng.

## Fix #18 — Popup "Chọn hợp đồng chi phí" (loại 99): bỏ auto-chọn loại HĐ + thêm cột Loại HĐ / Tổng thanh toán + "Số hợp đồng" có link (2026-10-15)
Yêu cầu user (nguyên văn): (1) "yêu cầu xuất hàng loại xuất khác, popup chọn hợp đồng chi phí, loại hợp đồng đang mặc định chọn hợp đồng" → chốt qua AskUserQuestion: **"Không chọn sẵn, để trống"** (placeholder "Chọn loại hợp đồng", bảng chưa tải tới khi user tự chọn 1 nhóm). (2) "Thêm cột loại hợp đồng, tổng thanh toán vào bảng". (3) "đồng bộ mã hợp đồng thành số hợp đồng" (đổi tiêu đề cột "Mã hợp đồng" → "Số hợp đồng"). (4) "Thêm link vào số hợp đồng".

- **Component:** `ContractCostModal.vue` (loại 99). **BE:** `ProductExportRequestPickerService::costContracts()` + rows raw của controller `costContracts`.
- **Research (đã chốt):**
  - **Tổng thanh toán = cột `payed_cost`** (ERP `SearchController@searchContract`). Schema DB (kiểm information_schema): `contracts`/`service_contracts`/`project_contracts` CÓ `payed_cost`; `hrm_contracts` KHÔNG có `payed_cost` → dùng `total_after_vat` (giá trị HĐ); `opening_contracts` không có cột tiền → `0`.
  - **Link theo nhóm (sourceKey)** — 1 nhóm/lần nên FE tự dựng từ sourceKey + id (không cần BE trả): '1'-'7' = `contracts.type` (chép `Contract::getLinkAttribute` ERP) → `admin/contracts/{id}/show`·`sale/sale_orders`·`sale/rule_contracts`·`sale/liquidation_contracts`·`sale/liquidation_orders`·`sale/contract_addition_annexes`·`sale/rule_contract_annexes`; services→`sale/service_contracts/{id}/show`; projects→`sale/project_contracts/{id}`; opening_contract→`accounting/opening-contracts/{id}/show`; hrm→nuxt-link `/assign/contracts/{id}`. HĐ HRM mở nội bộ, còn lại mở ERP tab mới qua `erpUrl()`.
  - **Ruling link:** dựng map link CỤC BỘ trong modal (`COST_CONTRACT_LINKS`), KHÔNG sửa util chung `contract-link.js` — vì App\Contract cần phân nhánh theo type mà `contractLink(class,id)` không nhận type; cục bộ tránh đổi signature hàm dùng chung. Chỉ import `erpUrl` (gọi, không sửa).
- [x] BE `costContracts()`: thêm `$payedExpr` per-table (contracts/service/project=`c.payed_cost`, hrm=`c.total_after_vat`, opening=`0`) + `->selectRaw($payedExpr.' as payed_cost')`. Controller trả `$page->items()` raw → payed_cost lọt thẳng FE (không Resource lọc).
- [x] FE select "Loại hợp đồng": bỏ `:allowClear="false"`, đổi comment; **bỏ watcher `sources` auto-pick** list[0]; `show()` bỏ `first`, `want = currentKey khớp ? currentKey : null` → mở popup để trống, `fetch()` guard sourceKey==null dọn bảng.
- [x] FE fields: `code` label "Mã hợp đồng" → **"Số hợp đồng"**; thêm cột `contract_type_label` (Loại hợp đồng) + `payed_cost` (Tổng thanh toán, `text-right`).
- [x] FE cell slots: `#cell(code)` link (nuxt-link `to` / `a href` / span, `.stop` vì row-clicked=pick); `#cell(contract_type_label)` = `currentSourceLabel` (1 nhóm/lần → mọi dòng cùng loại); `#cell(payed_cost)` = `formatMoney` (`toLocaleString('en-US')`).
- [x] FE: import `erpUrl`, const `COST_CONTRACT_LINKS`, computed `currentSourceLabel`, methods `linkOf`/`formatMoney`; CSS min-width 700→1000px + `col-type` 170px + `col-money` 150px.
- [x] Verify Playwright MCP (type=99): để trống loại HĐ khi mở (sourceKey=null, 0 dòng, placeholder "Chọn loại hợp đồng"); 6 cột đúng thứ tự STT/Số hợp đồng/Loại hợp đồng/Khách hàng/Địa chỉ/Tổng thanh toán; link số HĐ (type1→ERP /admin/contracts/{id}/show, type2→sale_orders, projects→project_contracts/{id} không /show, opening→opening-contracts/{id}/show, hrm→nuxt /assign/contracts/{id}); tổng thanh toán "1,234,567.89" & "0"; ô Địa chỉ rỗng hiện "—". PASS 2026-10-15.

## Fix #19 — Popup "Chọn hợp đồng hãng" (loại 14 "Xuất bán hàng") đồng bộ layout full-width như Fix #16 (2026-10-15)
Yêu cầu user (nguyên văn): "chọn hợp đồng phiếu yêu cầu xuất hàng loại bán hàng sửa lại giống các popup khác" (kèm screenshot popup "Chọn hợp đồng hãng" cũ: khuôn `V2BaseModal` + `V2BaseDataTable`, icon phẳng, cột "Mã hợp đồng", 4 cột STT/Mã HĐ/Khách hàng/Địa chỉ).

- **Component:** `hrm-client/pages/finance/product-export-requests/components/FirmContractSearchModal.vue` (modal chọn HĐ cho YCXH **loại 14** "Xuất bán hàng"; nguồn ERP `firm_contracts` qua `assign/product-export-requests/firm-contracts`, lọc `status=3` CO_HIEU_LUC + `created_by=auth()->id()`, phân trang + sort server-side). Dùng duy nhất ở `ProductExportRequestForm.vue` (`v-if="isFirmContractType && canChangeSource"`, `:show` + `@close` + `@select="onFirmContractPicked"`) — KHÔNG shared rộng → rewrite presentation an toàn.
- **Target khuôn:** `EmplementContractSearchModal.vue` (khuôn full-width đã làm ở Fix #16).
- **Cột chốt (user trả lời AskUserQuestion bằng screenshot):** giống popup loại 19 nhưng BỎ "Loại hợp đồng" (HĐ hãng chỉ 1 loại) + BỎ "Địa chỉ" → **7 cột: STT · Ngày lập · Số hợp đồng · Khách hàng · Tổng thanh toán · Ngày duyệt · Người duyệt**. Sort: Ngày lập, Số hợp đồng, Tổng thanh toán, Ngày duyệt (KHÔNG sort Khách hàng, Người duyệt).
- **Ruling:** rewrite từ `V2BaseModal`+`V2BaseDataTable` sang `b-modal` full-width + `b-table` theo khuôn Emplement. Giữ **sort server-side** (`no-local-sorting` + `@sort-changed`, SORT_KEYS={created_at,code,total,approved_time}). Giữ nguyên props/emit `:show`/`@close`/`@select` + `pick(c)` emit nguyên object `c` (cha auto-fill KH + địa chỉ — BE vẫn trả `customer_address`). Link số HĐ luôn mở ERP tab mới qua `contractLink(FIRM_CONTRACT_TYPE, row.id)` (util `contract-link.js`, KHÔNG sửa).
- **Research cột (bảng `firm_contracts`):** Ngày lập=`created_at`, Số HĐ=`code`, Khách hàng=`customer_name`, Tổng thanh toán=`total_after_vat` (alias `total`), Ngày duyệt=`approved_time`, Người duyệt = join `employees ae` ON `ae.id=c.approver_id` → `employee_infos ai` ON `ai.id=ae.employee_info_id` → `ai.fullname as approver_name`.
- [x] BE `ProductExportRequestController::firmContracts()`: `DB::table('firm_contracts as c')` + 2 leftJoin (`employees as ae`, `employee_infos as ai`); where đổi qualify `c.`; sortMap thêm `created_at`=>`c.created_at`, `total`=>`c.total_after_vat`, `approved_time`=>`c.approved_time` (giữ `code`, `customer_name`); orderByDesc `c.id`; select thêm `c.created_at`, `c.total_after_vat as total`, `c.approved_time`, `ai.fullname as approver_name` (giữ `c.id`, `c.code`, `c.customer_name`, `c.customer_address`).
- [x] Rewrite FE template: `b-modal` id `firm-contract-search-modal` `modal-class="modal-full-width-firm"` + custom `#modal-header` icon tròn xanh (`ri-file-text-line`, nền `rgba(22,163,74,0.1)`) + title "Chọn hợp đồng hãng" 14px/800 + nút X; bộ lọc `.picker-filter` chỉ 2 `V2BaseInput` (Số HĐ, Khách hàng — bỏ select Loại HĐ vì 1 nguồn) + nút Tìm kiếm + Làm mới.
- [x] `.table-shell` + `.table-top-scroll` + `.table-wrapper` chứa `b-table` (`no-local-sorting` + `:sort-by.sync`/`:sort-desc.sync` + `@sort-changed=onSortChanged` + `@row-clicked=pick`); 7 cột như trên; `#cell(code)` link `<a :href target=_blank @click.stop>`; `#cell(created_at)`/`#cell(approved_time)` formatDate; `#cell(total)` formatMoney text-right; cell() default '—'. Scroll 2 chiều `createScrollSyncHandlers`.
- [x] `V2BasePagination` (item-label "hợp đồng") + `.modal-footer` ghim đáy nút "Đóng". Script: watch show→show/hide(MODAL_ID), onModalShow(resetSearch)/onModalShown(bindScrollSync)/scroll handlers/onSortChanged/handlePageChange/handlePageSizeChange; fetch đọc `res.data.data` + `res.data.meta`; pick emit select(c)+hide. CSS `.modal-full-width-firm` (dialog 95vw ≤1350px, content 94vh flex col) + col-code `overflow-wrap:anywhere`.
- [x] Verify Playwright MCP (2026-10-15, type=14): tiêu đề "Chọn hợp đồng hãng" + icon `ri-file-text-line` vòng tròn (bg `rgba(22,163,74,0.1)`, radius 999px); 7 cột đúng thứ tự STT/Ngày lập/Số hợp đồng/Khách hàng/Tổng thanh toán/Ngày duyệt/Người duyệt; sort đúng 4 cột (Ngày lập/Số HĐ/Tổng thanh toán/Ngày duyệt), KHÔNG sort Khách hàng/Người duyệt; dữ liệu ngày `24/12/2025`, tiền `539,396,280` (en-US), người duyệt "Trần Thị Thu Hương"; link số HĐ → `http://127.0.0.1:8001/admin/sale/firm-contracts/10627` target `_blank`; dialog full-width 1140px/1200 viewport. PASS.
- **Chưa làm (chờ user quyết):** `TransferRequestSearchModal.vue` (popup chị em còn lại cùng khuôn cũ) — user chưa yêu cầu đổi; đề xuất đồng bộ cho nhất quán, chờ xác nhận.

## Fix #20 — Popup "Chọn phiếu yêu cầu chuyển hàng" (loại 7 "Xuất điều chuyển kho chi nhánh") đồng bộ layout full-width (2026-10-16)
Yêu cầu user (nguyên văn): "ok đồng bộ nốt" (tiếp Fix #19 — đồng bộ popup chị em còn lại `TransferRequestSearchModal.vue`).

- **Component:** `hrm-client/pages/finance/product-export-requests/components/TransferRequestSearchModal.vue` (modal chọn phiếu YC chuyển hàng cho YCXH **loại 7**; nguồn HRM `transfer-request-options`, chỉ phiếu status=2 chưa gắn phiếu xuất + đủ quyền tiếp nhận, BE lọc quyền per-row sau truy vấn → **trần 100 dòng**). Dùng duy nhất ở `ProductExportRequestForm.vue` (dòng 712, `v-if="isBranchTransfer && !transferLocked"`, `:show`/`:selectedIds`/`@close`/`@select="onTransferRequestsSelected"`).
- **KHÁC bản chất 3 popup kia:** đây là **MULTI-SELECT** (checkbox từng dòng + "chọn tất cả trang" + nút "Chọn (N)" → emit `select(array)`), và **phân trang + sort đều CLIENT-SIDE** (dữ liệu đã về hết, BE không phân trang). → rewrite CHỈ presentation, **giữ nguyên** toàn bộ logic multi-select + client-side.
- **Ruling:** rewrite từ `V2BaseModal`(cũ thực ra là `b-modal` size xl `modal-compact-contract` + `<table>` tay) sang `b-modal` full-width `modal-full-width-transfer` + `b-table` theo khuôn `ChooseErpCustomerModal`/Fix #19. Giữ MULTI-SELECT (cột checkbox `#head(select)`/`#cell(select)`, row-clicked=toggle, footer "Chọn (N)"). Giữ sort client-side: `no-local-sorting` + `@sort-changed=onSortChanged` set `sortBy`/`sortDesc`, tự sort qua `sortedRows` (created_at so bằng `dateSortKey` parse chuỗi dd/mm/yyyy HH:mm). Giữ phân trang client-side (`safePage`/`pagedRows`/`pageOffset`). Đổi `V2BaseSelect` → `V2BaseSelectInModal` (CLAUDE.md: select trong modal). Giữ nguyên props/emit `:show`/`:selectedIds`/`@close`/`@select`.
- [x] Rewrite template: `b-modal` id `transfer-request-search-modal` + `#modal-header` icon tròn (`ri-truck-line`, nền `rgba(22,163,74,0.1)` xanh #16a34a — màu chuẩn như các popup kia, icon truck giữ ngữ nghĩa phiếu chuyển) + title "Chọn phiếu yêu cầu chuyển hàng" + nút X; bộ lọc `.picker-filter` (Mã phiếu `V2BaseInput` + Người tạo `V2BaseSelectInModal` + Tìm kiếm/Làm mới).
- [x] `.table-shell` + `.table-top-scroll` + `.table-wrapper` chứa `b-table` (`:items="pagedRows"` đã sort+cắt trang client; `no-local-sorting` + `:sort-by.sync`/`:sort-desc.sync` + `@sort-changed` + `@row-clicked=toggle`); 5 cột: checkbox(select-all)/STT/Mã phiếu(sort,nuxt-link tab mới)/Người tạo(sort)/Ngày tạo(sort); scroll 2 chiều `createScrollSyncHandlers`.
- [x] `V2BasePagination` (total=rows.length, client-side) + `.modal-footer` ghim đáy: nút "Chọn (N)" (`:interactable="!!checked.length"`) + "Đóng".
- [x] Script: chuyển `:visible`/`@change` → watch show → `$bvModal.show/hide(MODAL_ID)` + `@hidden` emit close; `onModalShow`(reset checked/filter/sort/page + resetSearch)/`onModalShown`(bindScrollSync)/scroll handlers; `sortField`/`sortType` → `sortBy`/`sortDesc` (khớp b-table sync); giữ `dateSortKey`/`sortedRows`/`toggle`/`toggleAll`/`isChecked`/`confirm`/`creatorOptions`/`fetch`(đọc `data.items`). CSS `.modal-full-width-transfer` (dialog 95vw ≤1350px, content 94vh flex col) + col-code `overflow-wrap:anywhere`, data-table min-width 760px.
- [x] Verify Playwright MCP (2026-10-16, type=7): khuôn full-width 1140px/1200 viewport; icon `ri-truck-line` vòng tròn xanh (bg `rgba(22,163,74,0.1)`, radius 999px); 5 cột đúng (checkbox select-all + STT + Mã phiếu + Người tạo + Ngày tạo), sort đúng 3 cột (Mã phiếu/Người tạo/Ngày tạo), checkbox/STT không sort; dữ liệu thật PYCCH-06924 · Bùi Tiến Nam · 10/06/2026 14:42; link mã phiếu nội bộ `/finance/product-transfer-requests/6924` target `_blank`; footer "Chọn (0)"+"Đóng"; scroll sync 1106=1106. **Hành vi multi-select + sort client giữ nguyên:** toggle 2 dòng→checked=2; select-all đảo đúng; sort Mã phiếu đảo asc↔desc (06859↔06924); sort Ngày tạo đúng mốc thời gian (asc 04/06 cũ nhất ↔ desc 10/06 mới nhất). PASS.
- **Hoàn tất bộ 4 popup chọn nguồn của YCXH** (loại 14 hãng / 19 emplement / 99 chi phí / 7 chuyển hàng) — tất cả cùng khuôn full-width `ChooseErpCustomerModal`.

## Ghi chú
- Line ending: file FE + BE đều LF → giữ LF.
- Draft = status 3, Gửi duyệt = status 2 (khác bill-payment draft=1, không đổi).
