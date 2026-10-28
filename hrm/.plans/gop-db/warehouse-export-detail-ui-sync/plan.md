# Plan — Đồng bộ UI màn chi tiết Đề nghị xuất kho (ĐNXK)

> Phụ trách: @namdangit · Nhánh: `develop` (con của `gop_db`)
> Màn: `pages/finance/warehouse-export-requests/_id/index.vue` (Đề nghị xuất kho)
> Màn tham chiếu style tiêu đề: `pages/finance/product-export-requests/create.vue` ("Lập/Sửa đề nghị xuất kho" cũng để tiêu đề chuỗi trơn)

## Bối cảnh

Màn chi tiết ĐNXK đã chuyển gần hết sang UI chung (V2BaseFormCard). Còn 3 điểm lệch cần đồng bộ cho khớp màn create/edit cùng phân hệ:

1. **Ẩn Trạng thái ở tiêu đề** — `pageTitle()` đang dùng `buildStatusTitle(...)` → có pill trạng thái (nền màu + bo góc) lệch với create/edit (tiêu đề chuỗi trơn).
2. **Thêm link vào Số hợp đồng** — hiện chỉ link HĐ HRM (`is_hrm_contract` → `/assign/contracts/`), HĐ ERP (firm/bảo dưỡng…) ra `<span>` trơn, không bấm được.
3. **Đồng bộ nền + bo góc tiêu đề** — chính là hệ quả của #1: gỡ pill thì tiêu đề về chuỗi trơn như create/edit.

## Phase 1 — Đồng bộ tiêu đề (gộp #1 + #3)

- [x] Đổi `pageTitle()` từ `buildStatusTitle('Chi tiết đề nghị xuất kho', status_name, status_color)` → chuỗi trơn `Chi tiết đề nghị xuất kho: <mã>` (ghép mã theo convention khi có `detail.code`). Gỡ import `buildStatusTitle` không còn dùng.
  - File: `pages/finance/warehouse-export-requests/_id/index.vue:224`
  - Lý do gộp: pill là thứ DUY NHẤT tạo nền + bo góc ở tiêu đề → gỡ pill giải quyết cả #1 lẫn #3, khớp màn create ("Lập đề nghị xuất kho") + edit ("Sửa đề nghị xuất kho").

## Phase 2 — Link số hợp đồng (#2)

- [x] Dùng helper chung `utils/contract-link.js` (`contractLink(type, id)` → `{to}` nuxt-link / `{href}` ERP tab mới / null chữ trơn) — KHÔNG tự chế link theo từng loại.
  - **Quyết định (FE-only, không sửa BE):** BE ĐNXK (`WarehouseExportRequestResource`) KHÔNG trả `contract_morph_type`/`firm_contract_id`/`wr_service_contract_id` riêng — chỉ có `contract_id` (đã là id đúng theo loại), `contract_code`, `is_hrm_contract`, `type`. Suy morph-class ở FE: `is_hrm_contract` → HĐ HRM (`Modules\Assign\Entities\Contract\Contract`); loại 14/15 → `App\Model\Sale\Firm\Contract\FirmContract` (ERP); loại 17 → `App\Model\Customers\WrServiceContract` (màn HRM /customer-care). Loại 19 firm/wr không HRM không phân biệt được ở FE → `null` = chữ trơn (giữ nguyên hành vi cũ, không hồi quy).
  - Lý do không sửa BE: session hrm-api đang ở worktree `.worktrees/dstc-nature` (nhánh `feat/chuyen-doi-hang-hoa`, task DSTC khác), không phải nhánh `gop_db` nơi màn ĐNXK sống → sửa BE ở đó lạc nhánh. FE-only tự chứa trên nhánh gop_db FE.
  - File: `pages/finance/warehouse-export-requests/_id/index.vue` — thêm 2 computed `contractMorphType` + `contractLinkInfo`, import `contractLink`, thay khối "Số hợp đồng".

## Kiểm thử

- [x] Playwright MCP tại `http://127.0.0.1:3000/finance/warehouse-export-requests/<id>` — đã verify 2026-10-19:
  - Tiêu đề top-menu KHÔNG còn pill: `$store.state.pageTitle` = chuỗi trơn `Chi tiết đề nghị xuất kho: PDNXK-31048` (không markup `<span>`), nền + bo góc đồng bộ create/edit.
  - Số hợp đồng bấm được, đủ 3 ca:
    - HRM contract (id 31054, type 20, `is_hrm_contract`) → nuxt-link `/assign/contracts/15`.
    - Firm ERP (id 31049, type 14) → `<a target="_blank">` `http://127.0.0.1:8001/admin/sale/firm-contracts/24888`.
    - WrService HRM (id 31048, type 17) → nuxt-link `/customer-care/wr-service-contracts/6780`.
  - Record không HĐ (id 31109, type 3) → ô "Số hợp đồng" chữ trơn, không lỗi console.

## Phase 3 — Làm gọn bố cục cột theo phong cách YCXH (màn `product-export-requests` readonly)

- [x] Khối "Thông tin chung": đổi cột `col-md-4` (3 ô/hàng) → `col-md-3` + class `fld` (4 ô/hàng) cho khớp màn YCXH readonly.
- [x] Bỏ ô "Mã phiếu" khỏi lưới — mã đã hiển thị ở tiêu đề màn (`Chi tiết đề nghị xuất kho: <mã>`), mirror YCXH ("Mã phiếu đã hiển thị ở tiêu đề màn nên bỏ khỏi đây").
- [x] Gộp thông tin khách hàng (Khách hàng / SĐT / Người liên hệ / Địa chỉ / Địa chỉ giao) vào panel `ro-panel` "Thông tin khách hàng" dùng `ro-lbl` + `ro-value` + `ro-empty` — thay cho các ô `V2BaseInput` rời rạc col-md-8/col-12. Giữ nguyên các `showField(...)` guard.
- [x] Thêm CSS scoped `.fld` / `.ro-panel` / `.ro-lbl` / `.ro-value` (sao từ YCXH).
  - File: `pages/finance/warehouse-export-requests/_id/index.vue`
- [x] Verify Playwright 2026-10-19:
  - id 31054 (type 20, có KH): lưới col-md-3 (4 ô/hàng), KHÔNG còn "Mã phiếu", panel "Thông tin khách hàng" đủ 5 trường (Khách hàng/SĐT/Người liên hệ/Địa chỉ/Địa chỉ giao), ô rỗng dùng `ro-empty`. 0 lỗi console.
  - id 31109 (type 3, không KH): 5 ô col-md-3, KHÔNG hiện panel khách hàng, tiêu đề có mã. 0 lỗi console.

## Phase 4 — "KD chịu vận chuyển" đổi thành checkbox giống ERP

- [x] Thay ô `V2BaseInput` hiển thị "Có"/"Không" bằng checkbox chỉ-đọc — dùng khuôn `switch-line switch-line--no-label switch-line--disabled` của YCXH (ô "Xuất thẳng"), `<input type="checkbox" :checked="!!detail.bear_the_shipping" disabled />` + `<span>KD chịu vận chuyển</span>`. Thêm CSS scoped `.switch-line` (copy từ YCXH).
  - File: `pages/finance/warehouse-export-requests/_id/index.vue`
  - Lý do: ERP thể hiện trường này là checkbox; YCXH readonly cũng dùng checkbox chỉ-đọc cho cờ "Xuất thẳng" → bám đúng pattern sẵn có, không tự chế.
- [x] Verify Playwright 2026-10-19: id 31054 (`bear_the_shipping`=0) → checkbox KHÔNG tick, `disabled`; set reactive `bear_the_shipping`=1 → checkbox TICK, vẫn `disabled`. Nhãn cũ `V2BaseLabel` đã biến mất. 0 lỗi console.

## Phase 5 — Cột Hành động màn DANH SÁCH ĐNXK về quy tắc chung (tham chiếu YCXH)

> Màn: `pages/finance/warehouse-export-requests/index.vue` (danh sách)
> Tham chiếu: `pages/finance/product-export-requests/index.vue` (YCXH) + skill `list-page` §1/§2

- [x] Đổi tiêu đề cột `label`/`title` từ `'Thao tác'` → `'Hành động'` (cột key `action`).
- [x] Thay khối 6 `V2BaseIconButton` thẳng hàng bằng `<V2BaseRowActions :actions="getRowActions(item)" @action="handleRowAction(...)">` — component tự cắt 2 nút chính + gom phần còn lại vào menu `⋮` khi > 3 hành động. Thêm import + đăng ký `V2BaseRowActions`, gỡ `V2BaseIconButton` (không còn dùng trực tiếp).
- [x] `getRowActions(item)` thứ tự: `edit` (is_can_edit) · `create-warehouse-export` (is_can_create_warehouse_export) · `print` · `print-move` · `history` — "Lịch sử" LUÔN cuối (rơi vào menu `⋮` khi có menu). `handleRowAction` switch theo chuỗi key.
- [x] **Bỏ "Hủy" khỏi danh sách** (skill list-page §1 dòng 238: "Hủy phiếu"/"Không duyệt" chỉ đặt ở màn CHI TIẾT) — gỡ luôn method `confirmCancel` mồ côi.
- [x] Verify Playwright 2026-10-19 (`http://127.0.0.1:3000/finance/warehouse-export-requests`):
  - Header cột = "Hành động" (không còn "Thao tác"). 20 dòng render OK.
  - 31109 (4 hành động): inline = Sửa + In đề nghị, menu ⋮ = [In giấy tờ đi đường, **Lịch sử**] → Lịch sử cuối.
  - 31049 (edit ẩn, có "Tạo phiếu xuất kho"): inline = Tạo phiếu xuất kho + In đề nghị, menu ⋮ = [In giấy tờ đi đường, **Lịch sử**].
  - 31063/31055 (3 hành động): hiện thẳng 3 nút, KHÔNG có ⋮.
  - KHÔNG còn nút "Hủy" (ri-close-circle-line) ở bất kỳ dòng nào. 0 lỗi console từ thay đổi (chỉ noise HMR dev-mode của component khác).

## Phase 6 — Khoá ô "Kho xuất" ở màn Tạo/Sửa ĐNXK (bám ERP)

> Màn: `pages/finance/warehouse-export-requests/create.vue` + `_id/edit.vue`
> Bug user: "Trên ERP Kho xuất đang không cho sửa nhưng HRM vẫn sửa được — màn sửa, tạo đề nghị xuất kho loại xuất mượn."

**Đã trace (bug-fixer §3, không đoán):**
- ERP `WarehouseExportRequest.blade.php`: `get can_change_warehouse() { return this.type == 7; }` → chỉ **điều chuyển kho chi nhánh (type 7)** mới cho sửa kho; mọi loại khác (gồm **xuất mượn = type 3**) **khoá**. `form.blade.php` dòng 95 + 216: `<select ng-model="form.warehouse_id" ng-disabled="!form.can_change_warehouse">`.
- ERP lấy `warehouse_id` kế thừa từ YCXH cha (`set_on_parent` chứa `'warehouse_id'`) rồi khoá lại.
- **CHỐT lại (đọc `ProductExportRequestController.php:1617-1621`): HRM YCXH (`product_export_requests`) CÓ lưu `warehouse_id` cho type 3** → kế thừa được như ERP. (Giả định trước đó "HRM không có kho để kế thừa" là SAI — đã tự sửa khi đọc code.)
- HRM `edit.vue` `fetchData()` ĐÃ load `warehouse_id` từ bản ghi đã lưu → khoá được FE-only.

**Quyết định (CHỐT 2026-10-19 — user chọn Hướng B "làm đúng theo ERP" ở CẢ 2 màn):**
Khoá ô "Kho xuất" cho mọi loại trừ type 7 (điều chuyển kho chi nhánh), kế thừa `warehouse_id` từ YCXH.

- [x] **BE** `WarehouseExportRequestController@warehouseExportData` (màn Tạo):
  - Trả `warehouse_id` kế thừa từ YCXH vào payload `request` (`'warehouse_id' => $req->warehouse_id ? (int) $req->warehouse_id : null`).
  - Append phòng thủ: nếu kho YCXH đã ngừng hoạt động mà không có trong `$warehouses` → push thêm để ô khoá vẫn hiện đúng tên (quy tắc "danh mục khoá vẫn hiện").
- [x] **FE Tạo** `create.vue`: thêm computed `canChangeWarehouse` (`fieldCtx.type === 7`); prefill `form.warehouse_id` từ `data.request.warehouse_id` trong `fetchData()` (watcher tự chạy `fetchStock`, `markFormPristine` coi là sạch); `:disabled="!canChangeWarehouse"` + `:allowClear="canChangeWarehouse"` trên `V2BaseSelect` "Kho xuất".
- [x] **FE Sửa** `_id/edit.vue`: thêm computed `canChangeWarehouse` (`fieldCtx.type === 7`); `:disabled="!canChangeWarehouse"` + `:allowClear="canChangeWarehouse"` trên `V2BaseSelect` "Kho xuất" (warehouse_id đã load sẵn).
- [x] Verify Playwright MCP tại `http://127.0.0.1:3000` — đã verify 2026-10-19:
  - **Màn Sửa, type 3 (xuất mượn)** ĐNXK id 31109 (status 3): `canChangeWarehouse=false`, select2 `--disabled`, `nativeDisabled=true`, giá trị "Liên Ninh" (kho kế thừa) hiển thị đúng.
  - **Màn Tạo, type 3 (xuất mượn)** từ YCXH request_id 39304 (wh=2): `fieldCtxType=3`, `canChangeWarehouse=false`, `formWarehouseId=2`, ô khoá (`isSelect2Disabled=true`, `nativeDisabled=true`), hiển thị "Liên Ninh" — prefill + khoá đúng.
  - **Type 7 (điều chuyển kho)**: dữ liệu thật không có bản ghi type 7 ở trạng thái load được (ĐNXK type 7 trả 422 edit-data; YCXH type 7 còn "đang tạo" không lập được ĐNXK) → chứng minh nhánh editable trực tiếp trên màn Tạo 39304 bằng cách set reactive `info.type=7`: `canChangeWarehouse` lật `false→true`, select2 bỏ `--disabled` (`isSelect2Disabled=false`, `nativeDisabled=false`) → ô chọn được. Binding `:disabled="!canChangeWarehouse"` khớp đúng ERP `ng-disabled="!form.can_change_warehouse"` (editable ⇔ type===7). 0 lỗi console.

## Phase 7 — Bảng chi tiết ĐNXK: chia 2 tab + cột "Hình ảnh tham khảo" (Tạo + Sửa) — bám ERP

> Màn: `pages/finance/warehouse-export-requests/create.vue` + `_id/edit.vue`
> Bug user: "Bảng chi tiết đang chưa chia 2 tab như erp + Bảng thiếu cột hình ảnh" → user chốt **"cứ làm như erp đi"** (port đủ 2 tab + cột ảnh ở cả Tạo lẫn Sửa).

**Đã trace ERP** `warehouse_export_requests/form.blade.php`:
- Khối chính (type ≠ 9,10) có `<ul class="nav nav-tabs">` (dòng 277-301): tab **"Hàng hóa (*)"** active + tab **"Danh sách tổng hợp"** (`ng-if type != 18 && != 19`). Tab "Phụ kiện đi kèm" đã COMMENT.
- Tab "Hàng hóa" (303-362): cột cuối là **"Hình ảnh tham khảo"** `<img width="50" height="50" ng-src="<% product.avatar %>">`.
- **Quan trọng:** khối chính KHÔNG có pane `id="tong_hop"` (header render nhưng rỗng — vestigial ở ERP). Pane `tong_hop` thật chỉ nằm trong khối type 9 (556-580) + type 10 (712): cột `STT | Tên hàng hóa | Mã hàng hóa | Đơn vị tính | Tồn | Yêu cầu xuất`, read-only, `ng-repeat="p in form.products"`.

**Quyết định đã chốt (ghi design.md):**
- GIỮ nguyên bộ cột tab "Hàng hóa" hiện có của HRM (user chỉ phàn nàn thiếu tab + thiếu ảnh, không yêu cầu đổi/sắp lại cột) — chỉ **thêm cột "Hình ảnh tham khảo" làm cột CUỐI** dùng `<img v-if="row.avatar" :src="row.avatar" class="er-ref-img">` (copy pattern YCXH `ProductExportRequestForm.vue:1316` + CSS `.er-ref-img` dòng 4140).
- Tab "Danh sách tổng hợp" KHÔNG port theo kiểu rỗng-vestigial của ERP mà **điền read-only hợp nhất** theo pattern pane tong_hop type 9/10: `STT | Tên hàng hóa | Mã hàng hóa | ĐVT | SL được xuất | SL xuất kho` (`SL được xuất`=`row._available`, `SL xuất kho`=`row._qty` live, highlight đỏ khi `_available < _qty` như ERP `ng-class invalid`). Hiển thị TẤT CẢ dòng (bám ERP `form.products`, không lọc `_checked`).
- Dùng `b-tabs` `nav-class="nav-tabs nav-bordered"` (khuôn YCXH `ProductExportRequestForm.vue:528`).

- [x] **BE** `WarehouseExportRequestController@warehouseExportData`: thêm `'avatar'` vào `->get([...])` của `product_export_request_details`; thêm helper `buildProductAvatarUrl()` (copy nguyên văn từ `ProductExportRequestController.php:717`, vì là `private` khác class → nhân bản, KHÔNG sửa hàm dùng chung); map `avatar` qua helper vào payload mỗi product.
- [x] **FE Tạo** `create.vue`: thêm `avatar` vào row map (`fetchData`); bọc bảng chi tiết trong `b-tabs` 2 tab ("Hàng hóa" = bảng hiện tại + cột ảnh cuối; "Danh sách tổng hợp" = bảng read-only hợp nhất); thêm method `sumRowInvalid`; thêm CSS `.er-ref-img` + `tr.invalid > td` + `.wer-tabs` scoped.
- [x] **FE Sửa** `_id/edit.vue`: y hệt create.vue (row map + 2 tab + cột ảnh + `sumRowInvalid` + CSS).
- [x] Verify Playwright MCP `http://127.0.0.1:3000` — đã verify 2026-10-20:
  - **Màn Sửa** (`/warehouse-export-requests/31109/edit`, PDNXK-31109 "Đang tạo", dữ liệu thật 1 dòng): tab `["Hàng hóa (*)", "Danh sách tổng hợp"]`; tab Hàng hóa 12 cột, cột cuối "Hình ảnh tham khảo" → avatar null hiện `<span class="er-muted">—</span>`; tab tổng hợp read-only 6 cột (STT/Tên/Mã/ĐVT/SL được xuất=5/SL xuất kho=1), `invalid=false` vì 5≥1; chuyển tab OK; **0 lỗi console**.
  - **Màn Tạo** (`/warehouse-export-requests/create?request_id=39303`): cấu trúc 2 tab + cột "Hình ảnh tham khảo" render đúng; YCXH 39303 đã lập hết ĐNXK nên không còn dòng xuất → hiện dòng rỗng `colspan=12` đúng; **0 lỗi console lúc load** (lỗi 422 duy nhất là BE `warehouse-export-data` trả 422 vì YCXH đã tiêu thụ hết — trạng thái nghiệp vụ của chính YCXH đó, KHÔNG phải lỗi UI/code mới).

## Phase 8 — Màn CHI TIẾT ĐNXK: chia 2 tab + cột "Hình ảnh tham khảo" (bám ERP `show.blade.php`)

> Màn: `pages/finance/warehouse-export-requests/_id/index.vue`
> Bug user: xem màn Chi tiết thấy "không khác gì" vì Phase 7 chỉ làm Tạo/Sửa → user chốt **"làm màn chi tiết nữa"**.

**Đã trace ERP** `warehouse_export_requests/show.blade.php`:
- Tab "Hàng hóa" (#hang_hoa active) có cột cuối **"Hình ảnh tham khảo"** `<img width="50" height="50" ng-src="<% product.avatar %>">`.
- Tab "Danh sách tổng hợp" (#tong_hop): `STT | Tên hàng hóa | Mã hàng hóa | Đơn vị tính | Yêu cầu xuất` (`ng-repeat="p in form.all_products"`, `p.qty | numberOrHyphen`).

**Đã xác minh dữ liệu (DB `erp_hrm_check`):**
- Bảng `warehouse_export_request_details` CÓ sẵn cột `avatar` (đã lưu URL S3 tuyệt đối lúc lập ĐNXK, trùng `products.avatar`) → đọc thẳng `$p->avatar`, không cần join `products`.

**Quyết định đã chốt (ghi design.md):**
- GIỮ nguyên bộ cột + thứ tự của tab "Hàng hóa" hiện có (STT | Mã | Tên hàng | Thương hiệu | Model | ĐVT | SL xuất kho | Đơn giá | Thành tiền) + GIỮ dòng tổng tiền; chỉ **thêm cột "Hình ảnh tham khảo" làm cột CUỐI** (`er-ref-img`, null → `<span class="er-muted">—</span>`). Bọc trong `b-tabs` `nav-class="nav-tabs nav-bordered"` giống Phase 7.
- Tab "Danh sách tổng hợp": read-only `STT | Tên hàng hóa | Mã hàng hóa | ĐVT | SL xuất kho`. **KHÔNG** có cột tồn/SL được xuất và **KHÔNG** highlight đỏ — màn chi tiết là dữ liệu đã xuất, chỉ đọc (khác màn Tạo/Sửa live).

- [x] **BE** `WarehouseExportRequestController@show`: sau `attachSourcePrices`, chuẩn hoá `$p->avatar = $this->buildProductAvatarUrl($p->avatar ?? null)` cho từng dòng `products` (helper đã có sẵn trong class). Resource `WarehouseExportRequestResource`: thêm `'avatar' => $p->avatar ?? null` vào map products.
- [x] **FE Chi tiết** `_id/index.vue`: `this.products = detail.products` giữ nguyên object nên đã có `avatar` (không cần map lại); bọc bảng chi tiết trong `b-tabs` 2 tab ("Hàng hóa" = bảng hiện tại + cột ảnh cuối + giữ dòng tổng; "Danh sách tổng hợp" = read-only STT/Tên/Mã/ĐVT/SL xuất kho); thêm CSS `.er-ref-img` + `.wer-tabs` scoped (`.er-muted` đã có sẵn).
- [x] Verify Playwright MCP — đã verify 2026-10-20 trên `http://127.0.0.1:3000/finance/warehouse-export-requests/31109` (PDNXK-31109, 1 dòng Ốc vít CH-251314-2):
  - tab `["Hàng hóa", "Danh sách tổng hợp"]`; tab "Hàng hóa" 10 cột, cột cuối "Hình ảnh tham khảo" → **ảnh S3 load thật** (`naturalWidth=482`), dòng tổng "Tổng thành tiền" colspan 8 + giá trị + ô ảnh rỗng đúng.
  - tab "Danh sách tổng hợp" read-only 5 cột (STT/Tên hàng hóa/Mã hàng hóa/ĐVT/SL xuất kho = 1), chuyển tab OK.
  - **0 lỗi console** (769 dòng log còn lại là Vuex log/warning, không có error).

## Phase 9 — Gỡ mục "File đính kèm" ở màn TẠO + SỬA ĐNXK

> User chốt **"Thừa mục file đính kèm ở màn tạo, sửa"** (2026-10-20) → gỡ khối File đính kèm khỏi `create.vue` và `_id/edit.vue`.
> Phạm vi CHỈ Tạo + Sửa (đúng chữ user). Màn CHI TIẾT `_id/index.vue` GIỮ NGUYÊN card File đính kèm.
> Ghi chú lệch ERP: ERP `form.blade.php` VÀ `show.blade.php` đều CÓ khối "File đính kèm" — đây là lệch có chủ đích theo lệnh trực tiếp của user (lệnh trực tiếp thắng spec), đã nêu lại cho user.

- [x] **FE Tạo** `create.vue`: gỡ khối `<V2BaseFormCard title="File đính kèm">`; gỡ data `pendingFiles`; gỡ dòng `files: ...` trong `unsavedSnapshotSource()`; gỡ các method `onPickFiles`/`removePendingFile`/`humanSize`/`uploadPendingFiles`; gỡ `uploadPendingFiles(newId)` trong submit; gỡ CSS `.file-list`/`.file-item`.
- [x] **FE Sửa** `_id/edit.vue`: gỡ khối `<V2BaseFormCard title="File đính kèm">`; gỡ data `files`/`fileUploading`; gỡ `this.files = (data.files||[]).slice()` trong fetchData; gỡ method `onPickFiles`/`removeExistingFile`/`humanSize`; gỡ CSS `.file-list`/`.file-item`. Đã grep xác nhận không còn tham chiếu `files`/`fileUploading`/`humanSize`/`onPickFiles`/`removeExistingFile`/`attachments` ở cả 2 file.
- [x] Verify Playwright MCP `http://127.0.0.1:3000` — đã verify 2026-10-20:
  - **Màn Sửa** (`/warehouse-export-requests/31109/edit`): KHÔNG còn "File đính kèm"/"Chọn tệp"; chỉ còn 2 card "Thông tin chung" + "Danh sách hàng hoá", 2 tab "Hàng hóa (*)" / "Danh sách tổng hợp" nguyên vẹn; **0 lỗi console**.
  - **Màn Tạo** (`/warehouse-export-requests/create?request_id=39303`): KHÔNG còn "File đính kèm"/"Chọn tệp"; 2 card + 2 tab nguyên vẹn; lỗi console duy nhất là 422 BE `warehouse-export-data` (YCXH 39303 đã tiêu thụ hết — trạng thái nghiệp vụ, KHÔNG phải lỗi code mới).
  - Màn Chi tiết `_id/index.vue` KHÔNG đụng → vẫn còn card File đính kèm.

## Phase 10 — Đổi nút "Đóng" → "Quay lại" + đưa xuống cuối (màn Tạo + Sửa ĐNXK)

> User chốt 2026-10-20: nút back ở footer đổi tên thành **"Quay lại"** và đưa **xuống vị trí cuối cùng** (bám quy ước `V2Footer` — "Quay lại" luôn ở cuối).

- [x] **FE Sửa** `_id/edit.vue`: đổi nút đầu "Đóng" (`tertiary` + `fas fa-arrow-left`) → "Quay lại" (`light` + `ri-arrow-left-line mr-1`, đồng bộ create.vue) và chuyển xuống cuối cụm. Thứ tự mới: Lưu nháp → Gửi thủ kho → Quay lại.
- [x] **FE Tạo** `create.vue`: giữ nhãn "Quay lại" (đã đúng), chuyển từ đầu xuống cuối cụm. Thứ tự mới: Lưu nháp → Gửi thủ kho → Quay lại.
- [x] Verify Playwright MCP 2026-10-20 — cả Sửa (`/31109/edit`) lẫn Tạo (`/create?request_id=39303`): thứ tự nút `["Lưu nháp","Gửi thủ kho","Quay lại"]`, không còn "Đóng". Sửa 0 lỗi console; Tạo chỉ lỗi 422 nghiệp vụ YCXH 39303 (đã tiêu thụ hết), không phải lỗi code.

## Phase 11 — Lưu nháp KHÔNG validate kho xuất (màn Tạo + Sửa ĐNXK) — ❌ HỦY (user chốt không sửa 2026-10-20)

> User ban đầu: **"Bấm Lưu nháp đang validate kho xuất. K cần validate kho xuất thì đã có mã pycxh màn tạo"**.
> **Phát hiện khi verify**: cột `warehouse_export_requests.warehouse_id` là **NOT NULL** (bảng ERP dùng chung, 30.957 dòng, 0 null/0, không FK). Nới validate FE+BE xong vẫn 422 ở tầng DB (`Column 'warehouse_id' cannot be null`) vì service insert null.
> Ca này **chỉ xảy ra với loại 7 (điều chuyển chi nhánh)** — `canChangeWarehouse` chỉ `true` khi `type===7`; các loại khác kho kế thừa từ YCXH + khoá sẵn (prefill) nên Lưu nháp vốn không vướng.
> Muốn lưu nháp loại 7 chưa chọn kho ⇒ phải cho cột nullable (migration bảng ERP dùng chung). Đã trình 3 hướng A/B/C cho user.
> **User chốt 2026-10-20: "vậy thôi cái này ko cần sửa nữa"** → **KHÔNG sửa**, đã REVERT toàn bộ: BE 2 block validate (store+update) về `required`, FE create.vue + _id/edit.vue `submit()` về `if (!this.form.warehouse_id)`. Trạng thái code = như trước Phase 11.

- [x] ~~BE nới nullable khi nháp~~ — đã revert.
- [x] ~~FE skip validate kho khi status=3~~ — đã revert.
- [x] REVERT hoàn tất, verify: kho NOT NULL nên không khả thi mà không đổi schema bảng dùng chung.

## Phase 12 — Dropdown "Kho xuất" hiển thị dạng `mã kho - tên kho` (màn Tạo + Sửa ĐNXK)

> User chốt 2026-10-20: **"Drpdown khi xuất để dạng mã kho - tên kho"** — mỗi option kho hiển thị `<code> - <name>` (vd `KHO01 - Liên Ninh`) thay vì chỉ tên.
> `V2BaseSelect` dùng `opt.name` làm text hiển thị, `opt.id` làm value (`components/V2BaseSelect.vue:131`). Chỉ cần ghép code vào `name` khi map options; value (`id`) giữ nguyên.
> 2 màn dùng 2 endpoint khác nhau, đều phải select thêm `code`: Tạo dùng `warehouseExportData` (`get(['id','name'])` → thiếu cả `status`, nên create.vue trước đây không có `is_locked`); Sửa dùng `editData` (`get(['id','name','status'])` → đã có `status`, `is_locked` vốn chạy đúng). Cột `warehouses.code` là `varchar UNIQUE NOT NULL`, luôn có giá trị.

- [x] **BE** `warehouseExportData` (dòng ~740 + ~744 — endpoint màn Tạo): thêm `'code'` và `'status'` vào cả `get([...])` (query chính) lẫn `first([...])` (query kho khoá bổ sung).
- [x] **BE** `editData` (dòng ~464 — endpoint màn Sửa): thêm `'code'` vào `get(['id','name','status'])`.
- [x] **FE Tạo** `create.vue` (dòng ~302): map `name: w.code ? \`${w.code} - ${w.name}\` : w.name`, bổ sung `is_locked: Number(w.status) !== 1` (nay BE trả `status`).
- [x] **FE Sửa** `_id/edit.vue` (dòng ~295): map `name: w.code ? \`${w.code} - ${w.name}\` : w.name` (giữ `is_locked` sẵn có).
- [x] Verify Playwright MCP `http://127.0.0.1:3000` 2026-10-20 (employee 13 / cty 1):
  - **Sửa** `/31109/edit` (ĐNXK type 3): ô đang chọn hiển thị `LN - Liên Ninh`; cả 18 option đều dạng `mã - tên` (`CB - Cát Bà`, `CSKH - Chăm sóc khách hàng`…); `is_locked=false` toàn bộ kho hoạt động (không 🔒 nhầm); 0 lỗi console.
  - **Tạo** `/create?request_id=35673`: API `warehouse-export-data` trả đủ `code`+`status`; `warehouseOptions` 18 dòng đều `mã - tên` (`allFormattedAsCodeName=true`), `is_locked=false`; 0 lỗi console.

## Phase 13 — Đồng bộ màn TẠO ĐNXK đúng ERP theo từng loại xuất (hiển thị field per-type)

> Carried request: **"kiểm tra lại màn tạo xem đã đúng với erp về các thông tin cần thiết để hiển thị với các loại khác nhau chưa"**.
> User chốt: **"ok, C làm đủ giống erp"** (duyệt mục C đầy đủ + khuyến nghị tổng thể #1/#2/#3/D, giữ B nguyên) và qua AskUserQuestion: **"CÓ thêm lại file đính kèm"** (khôi phục File đính kèm cho loại 18/19 — đảo một phần Phase 9, CHỈ cho 2 loại này, CHỈ màn Tạo).
> Đối chiếu ERP `WarehouseExportRequest.blade.php` + `warehouse_export_requests/form.blade.php`: has_customer/has_contract = {1,2,8,14}; can_export_prepick ("SL đang giữ") = {7,14,17}; is_warehouse_transfer ("Kho nhập") = {5,6}; can_change_warehouse = type==7; loại 18/19 = ẩn khối khách hàng + ẩn bear_the_shipping, HIỆN "Loại xuất" + File đính kèm.
> Loại có thật trong DB: 3,4,6,7,12,14,15,17,18,19,20,21,99. #1 chỉ cần fallback 14/15→firmContract->code (các loại 1,2,8,11,13 không có trong DB); #7 chỉ loại 6 có mặt (vẫn dựng cho {5,6} để parity).
> **Quyết định đã chốt (ghi design.md):** C làm đủ giống ERP; #6b dùng chính file đính kèm của ĐNXK (bảng `files` table='warehouse_export_requests'), KHÔNG phải của YCXH cha; upload file lưu NGAY trong `storeWarehouseExportRequest` (multipart) sau khi tạo — atomic, chạy cho cả Lưu nháp (3) lẫn Gửi thủ kho (2), tránh vướng guard `assertCanEdit` (chỉ nháp) của endpoint `/attachments`. Giữ B nguyên (FULL_CUSTOMER+{20,21}, NO_BEAR+{9,10}, fallback hiện-khi-có-data).

- [x] **BE** `warehouseExportData` (~719): eager load `firmContract`, `wrServiceContract`; `request` trả thêm:
  - `emplement_contract_code` = `$req->emplement_contract_code ?: (optional($req->firmContract)->code ?: optional($req->wrServiceContract)->code)` (#1 hướng A — 14/15 lấy mã HĐ hãng).
  - `customer_type` = `$req->customer_type ? (int) $req->customer_type : null` (#2 — để ô "Người liên hệ" hiện đúng theo customerType>1).
  - `type_name` = `WarehouseExportRequest::getTypeName($req->type)` (#6a).
  - `import_warehouse_id` + `import_warehouse_name` (`mã - tên`) join `warehouses` theo `$req->import_warehouse_id` (#7, loại 5/6).
- [x] **BE** `editData` (~447): `request` trả thêm `type` = `(int) $dnxk->type` + `customer_type` = `$dnxk->customer_type ? (int) $dnxk->customer_type : null` (D — để edit.vue tính per-type visibility đúng; cột có thật trên `warehouse_export_requests`).
- [x] **BE** `storeWarehouseExportRequest` (~788): tách helper `private function storeAttachments($dnxk, $files)` (bê thân `uploadAttachments` phần S3 + `TableFileHelper::createForTable`); sau `createFromExportRequest`, nếu `$request->file('files')` có → gọi `storeAttachments($dnxk, $files)` (bất kể status, vì vừa tạo bởi chính người lập). `uploadAttachments` dùng lại helper. Validate store giữ nguyên (products là array, multipart vẫn parse được).
- [x] **FE** `field-relevance.js`: thêm `import_warehouse_id: (c) => c.type === 5 || c.type === 6` (#7). `export_type_name` (18/19) đã có sẵn.
- [x] **FE** `create.vue`:
  - #6a: thêm ô "Loại xuất" `V2BaseInput disabled` gated `showField('export_type_name')`, bind `info.type_name`.
  - #7: thêm ô "Kho nhập" `V2BaseInput disabled` gated `showField('import_warehouse_id')`, bind `info.import_warehouse_name` (đã `mã - tên`).
  - #6b: thêm card `V2BaseFormCard title="File đính kèm"` gated `showField('export_type_name')` (18/19) dùng `V2BaseFile multiple :autoUpload="false"` → `@change` gom FileList vào `pendingFiles`; data `pendingFiles: []`; trong `submit()` gửi `FormData` (append products[], files[]) khi có file, ngược lại giữ JSON; thêm `files` vào `unsavedSnapshotSource`.
  - #3: gate cột "SL đang giữ" (th + td) bằng computed `showHoldColumn` = `[7,14,17].includes(fieldCtx.type)`; chỉnh `colspan` dòng rỗng theo số cột thực tế.
- [x] Verify Playwright MCP `http://127.0.0.1:3000` — đã verify 2026-10-20 (tạm bật status=2 cho 3 YCXH id 31348/30796/35660 để màn Tạo nạp data, ĐÃ REVERT về 5/5/1 xong):
  - **Loại 14** (PYCXH-39253): "Số hợp đồng" = `HĐ_TPE_HN_DAU_25_1000_24122025-C` (firmContract resolve đúng), khối khách hàng đầy đủ (KH "CÔNG TY TNHH DẦU MỠ P&T", SĐT 0913291688, "Người liên hệ" = Trịnh Quốc Thắng · 0913291688 vì customerType>1), có "SL đang giữ", KHÔNG card File. 0 lỗi.
  - **Loại 17**: khối khách hàng hiện theo fallback B (có data), có "SL đang giữ". 0 lỗi.
  - **Loại 18/19**: có "Loại xuất" + card "File đính kèm", ẩn khối khách hàng + bear_the_shipping, KHÔNG "SL đang giữ". 0 lỗi.
  - **Loại 6**: có "Kho nhập", KHÔNG khối khách hàng, KHÔNG card File, KHÔNG "SL đang giữ". 0 lỗi.
  - **Loại 7** (id 35665): "Kho xuất" editable (1 select bật, canChangeWarehouse), có "SL đang giữ", KHÔNG card File. 0 lỗi. ("Kho nhập" hiện do fallback B có data — divergence cố ý, giữ nguyên.)

## Phase 15 — Deep-link PXK/PXH sang ERP báo "Chưa cấu hình địa chỉ ERP (TP_URL)" trên môi trường chỉ khai ERP_URL

> Yêu cầu user: bấm "Phiếu xuất kho" (PXK) ở màn Danh sách phiếu xuất hàng báo đỏ **"Chưa cấu hình địa chỉ ERP (TP_URL)"**, trong khi các chỗ khác bấm "hợp đồng" nhảy ERP vẫn bình thường.
> Nguyên nhân: nuxt.config khai 2 biến — `tp_url = process.env.TP_URL` và `ERP_URL = process.env.ERP_URL || process.env.TP_URL`. Mọi deep-link ERP đang chạy (menu/hub/sidebar/hợp đồng) đều dùng `process.env.ERP_URL || process.env.ADMIN_URL`, CÓ fallback. Riêng 5 helper `goErp*` ở phân hệ finance chỉ đọc `process.env.tp_url` → môi trường chỉ cấu hình `ERP_URL`/`ADMIN_URL` (prod) mà không có `TP_URL` thì `base` rỗng → báo lỗi. Local có `TP_URL=http://127.0.0.1:8001` nên không tái hiện.

- [x] Sửa 5 helper deep-link finance dùng chuỗi fallback như link hợp đồng: `process.env.ERP_URL || process.env.tp_url || process.env.ADMIN_URL`, đổi message lỗi → `(ERP_URL)`:
  - `product-exports/index.vue:654` (goErpWarehouseExport), `product-exports/_id/index.vue:582`, `product-imports/_id/index.vue:922`, `warehouse-export-requests/index.vue:600`, `warehouse-export-requests/_id/index.vue:398`.
- [x] Verify Playwright MCP `http://127.0.0.1:3000/finance/product-exports`: patch `window.open`, click PXK-30303 → mở `http://127.0.0.1:8001/admin/warehouse/warehouse_exports/30303/show`, KHÔNG toast lỗi (ERP_URL inline đúng).

### Checkpoint — 2026-10-20 (Phase 15)
Vừa hoàn thành: **Phase 15 XONG** — 5 helper deep-link ERP ở finance (product-exports list+detail, product-imports detail, warehouse-export-requests list+detail) đổi từ `process.env.tp_url` đơn độc sang fallback `ERP_URL || tp_url || ADMIN_URL` (đồng bộ pattern link hợp đồng/menu). Đây là lỗi ENV-specific (prod chỉ khai ERP_URL, thiếu TP_URL), code local không tái hiện. Verify Playwright PASS (click PXK mở đúng URL ERP, không toast lỗi).
Đang làm dở: (không).
Bước tiếp theo: Chờ user duyệt commit. CHỈ sửa hrm-client (5 file finance). Khuyên deploy: đảm bảo env prod có `ERP_URL` (đã có vì link hợp đồng chạy) — không cần thêm `TP_URL`.
Blocked:

## Phase 14 — Hủy ĐNXK bắt buộc nhập lý do + hiển thị lý do ở Lịch sử

> Yêu cầu user: **"hủy đề nghị đang k có popup yêu cầu nhập lý do. ghi lý do xong phải hiển thị lý do ở lịch sử. lý do là bắt buộc"**.
> Hiện trạng: nút "Hủy đề nghị" ở màn chi tiết ĐNXK (`_id/index.vue:359 confirmCancel`) chỉ mở popup xác nhận trơn, KHÔNG có ô nhập; service `cancel()` gọi `logStatusChanged($dnxk, $statusBefore)` KHÔNG kèm note → Lịch sử không có lý do.
> Chuỗi hiển thị đã xác minh: reason → controller → `service->cancel($dnxk, $reason)` → `logStatusChanged(..., $reason)` → `logCatalogStatus(..., $note)` → `CatalogHistoryService::logStatus(..., $note)` → `SystemInfoSection` render `log.note` (dòng 218). `base-confirm-modal` đã có sẵn `showInput` + `requiredInput` (chặn đóng khi trống, báo lỗi inline) + `$confirm` trả thẳng chuỗi đã gõ (plugin dòng 52).

- [x] **FE** `_id/index.vue` `confirmCancel()` (~359): thêm `showInput: true, requiredInput: true, inputType: 'textarea', inputLabel: 'Lý do hủy', inputPlaceholder: 'Nhập lý do hủy đề nghị'` vào `$confirm`; biến trả về giờ là chuỗi lý do (hoặc `false` khi đóng) → đổi `if (!ok) return` thành `const reason = ...; if (!reason) return`; gửi `payload: { reason }`.
- [x] **BE** controller `cancel()` (~543): thêm `Request $request` (đầu tham số), `$request->validate(['reason' => 'required|string|max:1000'])` (dùng message chuẩn lang `required`, validate NGOÀI try để ValidationException trả 422 có cấu trúc), truyền `$service->cancel($dnxk, $request->input('reason'))`.
- [x] **BE** service `cancel()` (~453): đổi chữ ký `cancel(WarehouseExportRequest $dnxk, ?string $reason = null)`, `use ($dnxk, $reason)`, dòng 479 → `$this->logStatusChanged($dnxk, $statusBefore, $reason)`.
- [x] `php -l` cả 2 file BE.
- [x] Verify Playwright MCP `http://127.0.0.1:3000`: (a) hủy để trống lý do → chặn, báo đỏ inline "Vui lòng nhập nội dung"; (b) nhập lý do → hủy thành công (0 lỗi console); (c) lý do hiện ở khối Lịch sử màn chi tiết.

### Checkpoint — 2026-10-20 (Phase 14)
Vừa hoàn thành: **Phase 14 XONG** — hủy ĐNXK bắt buộc nhập lý do + hiển thị lý do ở Lịch sử. FE `confirmCancel()` dùng `$confirm({ showInput, requiredInput, inputType:'textarea', inputLabel:'Lý do hủy' })` trả thẳng chuỗi lý do; BE controller `cancel()` validate `reason required|string|max:1000` NGOÀI try (rethrow ValidationException → 422), service `cancel($dnxk, $reason)` thread `reason` vào `logStatusChanged()` → note hiện ở `SystemInfoSection`. `php -l` pass cả 2 file BE. Verify Playwright PASS đủ 3 tiêu chí (trống → chặn + báo đỏ inline; nhập → hủy OK; lý do hiện ở Lịch sử). Rác test (ĐNXK 31109→5, YCXH 39303→6/completed, 2 dòng catalog_histories 5215/5216) đã REVERT về trạng thái gốc (31109→3, 39303→7/is_completed 0, xóa 2 dòng history).
Đang làm dở: (không) — Phase 14 hoàn tất.
Bước tiếp theo: Chờ user. CHƯA commit/push (đợi yêu cầu rõ ràng). Nếu user duyệt → commit nhánh gop_db: hrm-api (WarehouseExportRequestController + WarehouseExportRequestService) + hrm-client (`_id/index.vue`).
Blocked:

### Checkpoint — 2026-10-20 (Phase 13)
Vừa hoàn thành: **Phase 13 XONG** — toàn bộ BE (warehouseExportData/editData/storeWarehouseExportRequest+storeAttachments) + FE (field-relevance.js + create.vue: ô Loại xuất, ô Kho nhập, card File đính kèm cho 18/19, cột SL đang giữ gate {7,14,17}) đã code + `php -l` pass + verify Playwright 6 loại (14/17/18/19/6/7) đều 0 lỗi console. 3 bản ghi tạm flip status đã REVERT (31348→5, 30796→5, 35660→1).
Đang làm dở: (không) — Phase 13 hoàn tất.
Bước tiếp theo: Chờ user. CHƯA commit/push (đợi yêu cầu rõ ràng). Nếu user duyệt → commit nhánh gop_db cả hrm-api (controller) lẫn hrm-client (create.vue + field-relevance.js).
Blocked:

## Phase 16 — Màn TẠO phiếu xuất hàng về UI form cũ giống ERP (gỡ 2-card picker)

> Yêu cầu user: **"màn tạo phiếu xuất hàng làm giống hệt erp [ảnh ERP][ảnh HRM], khác là có thêm ô chọn phiếu yêu cầu xuất hàng nhưng form ban đầu thì phải giống"** + ghi chú QA trên ảnh: **"Đưa về UI cũ nha a, họ bắt sửa hết giống hệt form cũ"**.
> Hiện trạng (trước sửa): vào `/finance/product-exports/create` không kèm query → hiện màn "Chọn chứng từ nguồn" gồm 2 CARD lớn (Chọn phiếu xuất kho / Chọn phiếu YCXH xuất thẳng), chọn xong mới ra form + nút "Đổi phiếu". ERP KHÔNG có bước 2-card này — form hiện NGAY với 2 input-group loại trừ nhau ("Chọn phiếu xuất kho" + ô "Xuất thẳng" + "Chọn phiếu yêu cầu xuất hàng"), bấm kính lúp mở popup chọn.
> Quyết định: bỏ bước 2-card, đưa form về dạng ERP hiện ngay; điểm KHÁC DUY NHẤT so với ERP (được phép) = HRM có thêm ô "Phiếu yêu cầu xuất hàng". Copy pattern ô chọn chứng từ nguồn inline `.source-select` từ **`pages/finance/product-imports/components/ProductImportForm.vue:50-91`** (computed `canChangeSource`/`sourceCode`, method `openSourcePicker`/`clearSource`, SCSS `.source-select` 3821-3882).
> Deep-link (Luồng 2: `?warehouse_export_id=` / `?product_export_request_id=`) GIỮ NGUYÊN — vào thẳng form đã nạp data.

- [x] **FE** `create.vue` template: gỡ hẳn khối `V2BaseFormCard v-else-if="sourcePickerMode"` (2 card `.source-card`); `<template v-else>` giờ là nhánh ngay sau `loadError` → form hiện ngay.
- [x] **FE** `create.vue` `#meta`: gỡ nút "Đổi phiếu" (`repick`), chỉ còn `<CreatorInfoLine :is-create="true" />`.
- [x] **FE** `create.vue` tab "Thông tin chung": thay 2 ô readonly (Phiếu xuất kho `V2BaseInput` + Chọn phiếu YCXH `V2BaseInput`) bằng 2 ô `.source-select` inline — PXK (kính lúp → `openWarehouseExportModal`) + YCXH (kính lúp → `openProductExportRequestModal`), nút × → `clearSource`. Loại trừ nhau: chưa chọn → cả 2 ô hiện; chọn rồi → chỉ còn ô tương ứng (gate bằng computed `showPxkPicker`/`showYcxhPicker`, KHÔNG theo `is_export_direct` vì info rỗng lúc đầu sẽ chỉ hiện PXK).
- [x] **FE** `create.vue` computed MỚI: `noSource`/`hasPxkSource`/`hasYcxhSource`/`showPxkPicker`/`showYcxhPicker`/`pxkCode`/`ycxhCode`.
- [x] **FE** `create.vue` methods: thêm `clearSource()` (đưa về no-source + `resetSourceState`); gỡ `repick()`; `onChoose*` bỏ `sourcePickerMode=false`.
- [x] **FE** `create.vue` `mounted()` Luồng 1: bỏ `sourcePickerMode=true`, chỉ `this.loading=false` (form hiện ngay).
- [x] **FE** `create.vue` data: gỡ `sourcePickerMode`.
- [x] **FE** `create.vue` SCSS: gỡ `.source-picker`/`.source-card`, thêm `.source-select` (copy ProductImportForm.vue:3821-3882).
- [x] Verify Playwright MCP `http://127.0.0.1:3000/finance/product-exports/create` — đã verify 2026-10-20 (0 lỗi console suốt các luồng):
  - **Luồng 1 (không query)**: (a) form hiện NGAY với CẢ 2 ô "Phiếu xuất kho" + "Phiếu yêu cầu xuất hàng", KHÔNG còn bước 2-card ✅; (b) bấm ô PXK → popup PXK mở ✅; (c) chọn PXK-30296 → form nạp đủ header + 4 dòng hàng + tổng tiền, ô YCXH ẩn, ô PXK hiện mã + nút × ✅; (d) bấm × → về 2 ô rỗng, data/dòng hàng được xoá ✅; (e) bấm ô YCXH → popup YCXH mở ✅.
  - **Luồng 2 (deep-link `?warehouse_export_id=30296`)**: vào thẳng form đã nạp data PXK-30296 — Loại xuất "Xuất bán hợp đồng", ô Phiếu xuất kho hiện "PXK-30296", đủ 4 dòng hàng (TATE-TBTE-05/03/02/01) + tổng thành tiền bán 14,550,000 / VAT 1,164,000 / sau VAT 15,714,000, KHÔNG có bước 2-card ✅. (f) 0 lỗi console ✅.

## Phase 17 — 2 popup chọn chứng từ nguồn (PXK + YCXH) về khuôn popup chọn hợp đồng bên YCXH

> Yêu cầu user: **"sửa 2 cái popup chọn phiếu xuất kho, chọn phiếu yêu cầu xuất hàng cho giống các cái popup chọn hợp đồng bên yêu cầu xuất hàng"**.
> Hiện trạng (trước sửa): `product-exports/components/WarehouseExportSearchModal.vue` + `ProductExportRequestSearchModal.vue` dùng `b-modal size="lg"` + header mặc định + `<table class="er-table">` tự dựng tay + phân trang "Trước/Sau".
> **ĐÍNH CHÍNH khuôn mẫu (2026-10-20):** popup chọn hợp đồng loại 19 "Xuất bán hợp đồng" bên YCXH mở qua ref `hrmContractModal` là **`product-export-requests/components/HrmContractSearchModal.vue`** (KHÔNG phải `EmplementContractSearchModal.vue` như ghi trước đó). Mẫu thật là popup **GỌN** `V2BaseModal size="xl"` + bảng thường (`<table class="table table-bordered table-sm">`) bọc `V2BaseTableScroll`, KHÔNG phải b-modal full-width 95vw với `<b-table :fields>`. Bản rewrite full-width + `<b-table :fields>` làm trước đó vừa sai bề rộng, vừa gây `[Vue warn] "fields" is already defined as a prop` (b-table tự khai prop `fields`) → đã loại bỏ hẳn `<b-table>`.
> Quyết định: restyle 2 popup đích theo **đúng khuôn `HrmContractSearchModal.vue`** (copy pattern): `V2BaseModal size="xl"` + bộ lọc `form-row` (Mã phiếu + Làm mới) + bảng thường bọc `V2BaseTableScroll max-height=60vh` + `V2BasePagination` + footer "Đóng" mặc định của V2BaseModal (KHÔNG khai footer riêng). GIỮ NGUYÊN phần nghiệp vụ của popup đích: API endpoint (`warehouse-export-sources` / `product-export-request-sources`), response phẳng (`body.data/currentPage/perPage/total`), API đối ngoại `show()`/`hide()`/`@choose`, 6 cột (STT, Mã phiếu, Loại, Kho, Khách hàng, Ngày tạo), câu empty riêng, KHÔNG sort server-side.
> Copy pattern từ `pages/finance/product-export-requests/components/HrmContractSearchModal.vue` (V2BaseModal size xl + form-row filter + bảng thường bọc V2BaseTableScroll + V2BasePagination + footer mặc định).

- [x] **FE** `WarehouseExportSearchModal.vue` — rewrite theo khuôn `HrmContractSearchModal`: `<V2BaseModal modal-id="warehouse-export-search-modal" title="Chọn phiếu xuất kho" icon="ri-file-list-3-line" size="xl">`; bộ lọc `form-row` (V2BaseLabel "Mã phiếu" + V2BaseInput debounce 300ms + V2BaseButton tertiary "Làm mới"); `<table class="table table-bordered table-sm source-table">` 6 cột bọc `V2BaseTableScroll max-height="60vh"` (dòng loading/empty dùng `.empty-cell #6b7280`, hover `#f0fdf4`, cell Mã thường không đậm); `V2BasePagination v-if="total>0"`. GIỮ `show()/hide()/@choose(item)`, endpoint `assign/product-exports/warehouse-export-sources`, parse `body.data/currentPage/perPage/total`. Empty "Không có phiếu xuất kho đủ điều kiện lập phiếu xuất hàng".
- [x] **FE** `ProductExportRequestSearchModal.vue` — y hệt, đổi `modal-id="product-export-request-search-modal"` + title "Chọn phiếu yêu cầu xuất hàng" + endpoint `assign/product-exports/product-export-request-sources` + empty "Không có phiếu yêu cầu xuất hàng đủ điều kiện lập phiếu xuất hàng"; `item.id` = product_export_request_id.
- [x] Verify Playwright MCP `http://127.0.0.1:3000/finance/product-exports/create` 2026-10-20 — **CẢ 2 popup PASS, 0 lỗi console** (cảnh báo `fields already defined` đã biến mất):
  - PXK (`WarehouseExportSearchModal`): V2BaseModal gọn/giữa, header xanh "Chọn phiếu xuất kho" + ×, bộ lọc "Mã phiếu" + "Làm mới", bảng 6 cột 10/86 bản ghi thật (PXK-30296…), cuộn ngang trên+dưới, phân trang "Hiển thị 1–10 / 86 phiếu", footer "← Đóng" ghim. Ảnh `wes-v2-modal.png`.
  - YCXH (`ProductExportRequestSearchModal`): cùng khuôn gọn, header "Chọn phiếu yêu cầu xuất hàng", 2 bản ghi thật (PYCXH-35623/35622), phân trang "Hiển thị 1–2 / 2 phiếu", footer "Đóng". Ảnh `per-v2-modal.png`.
  - Row-select wiring nguyên vẹn: mỗi dòng `@click="choose(item)"` → `$emit('choose', item)` + `hide()`; create.vue lắng `@choose` qua `$refs.warehouseExportModal`/`$refs.requestModal`.

### Checkpoint — 2026-10-20
Vừa hoàn thành: **Phase 17 XONG** — 2 popup chọn chứng từ nguồn (PXK + YCXH) ở màn Lập phiếu xuất hàng đã rewrite về đúng khuôn popup chọn hợp đồng (`HrmContractSearchModal.vue`): V2BaseModal size xl gọn/giữa + bảng thường bọc V2BaseTableScroll + V2BasePagination + footer mặc định. Bỏ hẳn b-modal full-width + `<b-table :fields>` (nguồn gốc cảnh báo `fields already defined` + sai bề rộng). Verify Playwright PASS cả 2 popup, 0 lỗi console, data thật, row-select nguyên vẹn.
Đang làm dở: không.
Bước tiếp theo: chờ user quyết commit — Phase 17 (2 file popup) chưa commit; Phase 15 (5 helper ERP_URL) + Phase 16 (create.vue revert inline form) cũng đã xong-verify nhưng CHƯA commit, chờ user đồng ý.
Blocked:

## Phase 18 — Thiết kế lại tab "Thông tin chung" màn Lập phiếu xuất hàng cho GỌN theo khuôn YCXH

> Yêu cầu user: **"thiết kế lại cái thông tin chung cho gọn tương tự yêu cầu xuất hàng"** — làm tab "Thông tin chung" của màn Lập phiếu xuất hàng (`pages/finance/product-exports/create.vue`) gọn lại, bám đúng bố cục form "Thông tin chung" bên Yêu cầu xuất hàng (`product-export-requests/components/ProductExportRequestForm.vue`). Chỉ refactor BỐ CỤC/mật độ, GIỮ NGUYÊN mọi trường, nghiệp vụ, gate `showField(...)`, picker, khối hạch toán, component V2Base*.
> Copy pattern từ `pages/finance/product-export-requests/components/ProductExportRequestForm.vue` (lưới `col-md-3 mb-2 fld` 4 ô/hàng; khối recap khách hàng `.ro-panel` "Thông tin khách hàng" gom các ô chỉ-đọc Khách hàng/SĐT/Người liên hệ/Địa chỉ KH/Địa chỉ giao vào 1 col-12 với `.ro-lbl` + `.ro-value`/`.ro-empty`; style `.fld`/`.ro-panel`/`.ro-value`/`.ro-lbl` dòng 3858-3908 + 4038-4078).

- [x] **FE** `create.vue` tab "Thông tin chung": đổi các ô thông tin từ `col-md-4 mb-2` → `col-md-3 mb-2 fld` (4 ô/hàng); ô "Xuất thẳng" thêm `d-flex flex-column justify-content-end` như YCXH; Địa chỉ KH từ `col-md-8` → vào panel.
- [x] **FE** `create.vue`: gom 5 ô chỉ-đọc khách hàng (Khách hàng, SĐT, Người liên hệ, Địa chỉ KH, Địa chỉ giao) thành 1 khối `.ro-panel` "Thông tin khách hàng" (col-12) — nested `form-row` col-md-6/col-md-3 với `.ro-lbl` + `.ro-value` (`.ro-empty` khi rỗng); panel gate bằng OR của 5 `showField(...)`, mỗi dòng giữ `showField` riêng.
- [x] **FE** `create.vue`: Ghi chú thêm class `fld` (col-12 mb-2 fld). Port style `.fld`/`.ro-panel`/`.ro-value`/`.ro-lbl` từ YCXH vào `<style>` scoped (giữ nguyên `.fld-err`/`.source-select` sẵn có).
- [x] Verify Playwright MCP `http://127.0.0.1:3000/finance/product-exports/create` (0 lỗi console): deep-link PXK-30296 (Xuất bán hợp đồng) → panel "Thông tin khách hàng" hiện đủ Khách hàng/SĐT/Người liên hệ/Địa chỉ KH; 8 ô `col-md-3` đều rộng 229px (4 ô/hàng); 0 lỗi console. CHƯA commit.

## Quyết định đã chốt — 2026-10-20

- **NVKD trống ở loại 14 (Xuất bán hãng) là ĐÚNG, KHÔNG sửa code.** ERP `WarehouseExport::getDataForProductExport` chỉ set `employee_create_contract` cho loại 1/2/8, KHÔNG set cho 14 (HĐ hãng). HRM `ProductExportController::fillContractDisplay` với `DISPLAY_SALE_EMPLOYEE_TYPES = [1,2,8]` khớp ERP. HĐ hãng không có khái niệm NVKD → ô NVKD trống là bám đúng ERP. User chốt giữ nguyên (A).

## Phase 19 — Popup "Chọn phiếu xuất kho": link mã phiếu + bộ lọc/cột Người tạo + sắp xếp

> Yêu cầu user: **"sửa popup chọn phiếu kho xuất: Thêm link vào mã phiếu, Thêm bộ lọc Người tạo và cột Người tạo như erp, Thêm sort vào mã phiếu, người tạo, ngày tạo, khách hàng"**. CHỈ áp cho popup PXK (`WarehouseExportSearchModal.vue`), KHÔNG đụng popup YCXH.
> ERP đối chiếu: `Warehouse/WarehouseExportsController::searchData` render cột Người tạo = `employee_create->fullname` (dòng 103-104). Sort server-side bám khuôn `BorrowPickerModal.vue` (sortable `<th>` + `sort_by`/`sort_desc`, sao từ `BillAdjustDeptRequestPickerModal`/`V2BaseDataTable`). Select người tạo dùng `V2BaseSelectInModal` (select trong modal) + nhãn `employeeOptionText` (Tên - Mã phòng - Mã NV). Nguồn NV lấy từ prop `employees` create.vue đã nạp sẵn (tránh gọi API lần nữa).

- [x] **BE** `ProductExportController::warehouseExportSources`: thêm lọc `created_by`; thêm `creator_name` vào row map (resolve theo LÔ qua `resolveEmployeeNames()` — tránh N+1); thêm `applySourceSort()` whitelist `code`/`customer_name`/`created_at` (orderBy cột) + `created_by` (leftJoin employees→employee_infos, sort theo `fullname`), mặc định `id desc`; qualify cột select `warehouse_exports.*` cho an toàn khi join; thêm `created_by` vào select.
- [x] **FE** `WarehouseExportSearchModal.vue`: (1) mã phiếu → `<nuxt-link :to="/finance/warehouse-exports/${item.id}" class="v2-cell-link" target="_blank" @click.native.stop>`; (2) prop `employees` + ô lọc "Người tạo" `V2BaseSelectInModal` (options = `employeeOptionText`), `@change` reload trang 1; (3) cột "Người tạo" (`item.creator_name`); (4) `<th>` bấm sắp xếp (code, customer_name, created_by, created_at) theo khuôn `BorrowPickerModal` (`toggleSort`/`sortIcon` + `sort_by`/`sort_desc`); `show()`/`resetSearch()` reset filter+sort.
- [x] **FE** `create.vue`: truyền `:employees="employees"` xuống `<WarehouseExportSearchModal>`.
- [x] **FIX khi verify** `create.vue`: ô lọc "Người tạo" rỗng vì `employees` chỉ nạp trong `loadArrangeCatalogs()` (chạy SAU khi chọn PXK), còn popup mở TRƯỚC khi chọn. Thêm `ensureEmployeesLoaded()` (guard `employees.length`, gọi `assign/tasks/employees` 1 lần) → `openWarehouseExportModal()` `await` trước `show()`; `loadArrangeCatalogs()` tái dùng cùng hàm nên không gọi lại API.
- [x] **FIX khi verify** `ProductExportController::warehouseExportSources`: `created_at` trả `->toDateTimeString()` (ISO) thay vì `->format('d/m/Y H:i')` — FE `dayjs().format('DD/MM/YYYY')` không parse được chuỗi `d/m/Y H:i` → cột Ngày tạo hiện "Invalid Date". (Popup YCXH anh em có cùng bug tiềm ẩn nhưng KHÔNG đụng — ngoài phạm vi yêu cầu + không bị kích hoạt.)
- [x] Verify Playwright MCP `http://127.0.0.1:3000/finance/product-exports/create` 2026-10-20 (0 lỗi console suốt): link mã phiếu = `<nuxt-link>` `/finance/warehouse-exports/:id` + `target="_blank"` (không trigger choose); ô lọc Người tạo nạp 392 NV (format `Tên - Mã phòng - Mã NV`), chọn DNS Admin → gửi `created_by=13` → 86→1 phiếu (PXK-30296); cột Người tạo hiện tên; sort `created_by` ASC đúng theo fullname (DNS Admin→Hồ Chí Dũng, leftJoin employee_infos), `created_at` ASC/DESC đúng; cột Ngày tạo hiện 19/08/2026… (hết "Invalid Date"); mỗi lần bấm/chọn gọi API đúng 1 lần.

## Phase 20 — BUG cột "SL thực xuất" hiện ĐV CƠ BẢN thay vì ĐV CHỌN (map đúng cột theo loại xuất, HRM bám ERP)

> User: *"cột SL thực xuất hình như đang hiện sl xuất theo dv cơ bản, map lại cho đúng các cột cho từng loại xuất map hrm theo erp, rà soát cho tất cả 3 màn tạo sửa chi tiết"* (ảnh màn hình 2026-10-21 10.18.40 — màn Lập phiếu, chọn PXK-35559, SL thực xuất = 4 Can thay vì 1 Thùng).

### Chẩn đoán (ERP = nguồn nghiệp vụ)
- ERP `ProductExportsController::store` 812-819: `qty = l['qty']` = **SL thực xuất = ĐV CHỌN**; `export_qty = l['qty'] × unit_coefficient` = **SL theo ĐV cơ bản**. Cột "SL thực xuất" LUÔN là ĐV chọn, mọi loại xuất.
- HRM FE `create.vue` bảng hàng: ĐVT=`row.unit_name` (ĐV chọn, Thùng), SL đề nghị=`row.request_qty` (ĐV chọn), **SL thực xuất=`row.qty`** → phải là ĐV chọn cho nhất quán.
- **ROOT CAUSE** `create.vue:904` prefill: `qty: Number(p.export_qty || p.qty) || 0`. Nguồn PXK (`warehouse_export_lots`, controller dòng 747 select cả `qty` lẫn `export_qty`): `p.export_qty`=ĐV cơ bản (4 Can) được ưu tiên → SL thực xuất hiện 4. Nguồn YCXH xuất thẳng (`product_export_request_details`, dòng 1178) KHÔNG có `export_qty` → fallback `p.qty` → đang đúng.
- Lỗi lan xuống DB: `buildProductsPayload` (1242-1248) gửi `qty: Number(r.qty)` → BE `ProductExportService` lưu `qty=4` + `export_qty=4×coef=16` (double-sai). Màn chi tiết `_id/index.vue` đọc `row.qty` qua `ProductExportResource` (`'qty'=>(float)$p->qty`) ĐÚNG → nếu phiếu tạo bằng FE lỗi thì chi tiết cũng hiện ĐV cơ bản (hệ quả data, không phải lỗi code màn chi tiết).
- Cột kho-KT "SL xuất" (`acc.qty`, user tự nhập, tổng = row.qty theo ĐV chọn) GIỮ NGUYÊN — ERP/Resource cố ý để kho-KT theo ĐV cơ bản ở màn chi tiết.
- KHÔNG có `edit.vue` — sửa phiếu không phải màn riêng. Chỉ 2 màn có bảng: `create.vue` + `_id/index.vue`.

### Việc
- [ ] **FE** `create.vue:904`: `qty: Number(p.export_qty || p.qty) || 0` → `qty: Number(p.qty) || 0` (SL thực xuất = ĐV chọn). Giữ `request_qty` dòng 905 nguyên.
- [ ] Verify Playwright 127.0.0.1:3000 màn Lập phiếu: chọn PXK có SP quy đổi hệ số>1 → SL thực xuất = ĐV chọn (khớp ĐVT + SL đề nghị), 0 lỗi console.
- [ ] Chi tiết `_id/index.vue`: xác nhận đọc `row.qty` đúng (code không đổi); lỗi còn hiện ở phiếu CŨ chỉ do data đã ghi sai.

### MỞ — chờ user
- Phiếu đã tạo bằng FE lỗi có `product_export_details.qty` lưu ĐV cơ bản → có backfill không? (cần kiểm data thật trước, user thường KHÔNG backfill systemic).
