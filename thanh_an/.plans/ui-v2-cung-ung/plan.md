# Plan — Chuẩn hóa UI V2 cho phân hệ Cung ứng (port V2Base + skill từ hrm)

> Phụ trách: @khoipv · Ngày tạo: 2026-09-28
> Spec: [docs/superpowers/specs/2026-09-28-ui-v2-cung-ung-design.md](../../docs/superpowers/specs/2026-09-28-ui-v2-cung-ung-design.md)
> Design tóm tắt: [design.md](design.md)
> Nguồn chuẩn: `D:\laragon\www\hrm\hrm-client` (component `components/V2Base*.vue`, skill `hrm-claude-config/hrm/.claude/skills/`)

**Mục tiêu:** đưa bộ component V2Base + quy ước UI của hrm sang `hrm-thanhan-client`, viết lại skill cho dns, rồi chuyển UI phân hệ Cung ứng sang V2 (bắt đầu bằng 1 màn thí điểm).

**Ràng buộc chung:**
- Chỉ THÊM file mới — KHÔNG sửa component/plugin/service dùng chung khi chưa hỏi (CLAUDE.md).
- `.v2-styles` là class bọc trang → màn cũ không đổi giao diện.
- Remixicon dns là v2.4.0 → icon mới của hrm (4.x) phải đổi sang icon có trong 2.4.
- Migration chỉ index, không khóa ngoại. Không commit / push. Không chạy E2E khi chưa được bảo.

---

## Phase 0 — Khảo sát & chốt phạm vi
- [x] So sánh package.json, plugin, store, utils hai client
- [x] Lập danh sách file phải port + điểm không tương thích (xem spec §3)
- [x] Tạo plan/design/spec + STATUS.md

## Phase 1 — Nền V2 phía FE (hrm-thanhan-client)
### Task 1.1 — Utils / mixin
- [x] `utils/mixins/v2ValidateMixin.js`, `utils/select2LockedOption.js`, `utils/constants/field-hints.js`, `utils/select2-focus-search.js`, `utils/select2DropdownSearch.js`, `utils/employeeOptionText.js`, `utils/import-helper.js`, `utils/filterAutoSearch.js`, `utils/download-excel.js`
- [x] Mixin màn danh sách: `utils/mixins/filterStateMixin.js`, `utils/mixins/columnCustomizationMixin.js` (trỏ modal V2 mới), `utils/mixins/exportFieldsMixin.js`
- [x] `utils/common.js`: THÊM hàm mới `mergeKnownFilters` (không sửa hàm cũ)
### Task 1.2 — Component
- [x] 39 file `components/V2Base*.vue` + `V2Footer.vue` (bỏ `V2BaseCompanyDepartmentFilter`, `V2BaseFieldCategoryApplicationFilter` — xem spec §3.3)
- [x] `components/modal/V2BaseModal.vue`, `V2BaseRejectApproveModal.vue`, `filter-customization-modal.vue`, `base-confirm-modal.vue`, `export-fields-modal.vue`, `v2-column-customization-modal.vue` (bản hrm, đặt tên mới để không đè modal cũ), ~~`HistoryApproveModal`~~ → bỏ import module Quyết định trong `V2Footer`, chỉ emit `showDecisionHistoryApprove` cho màn cha tự mở
### Task 1.3 — Thích nghi
- [x] Thay `$safeLoadingStart/Finish` → `$nuxt.$loading.start/finish` (dns không có plugin safe-loading)
- [x] Đổi 4 icon không có trong remixicon 2.4 (`ri-check-circle-line`, `ri-draggable`, `ri-filter-off-line`, `ri-shield-check-line`)
- [x] Rà `apiGetMethod` truyền object (dns chỉ nhận chuỗi URL)
### Task 1.4 — Style
- [x] `assets/scss/v2-styles.scss` (+ phần rule ngoài khối `.v2-styles`)
- [x] Kiểm build không lỗi import — compile thử 58 file mới (template + babel + node-sass) bằng script scratchpad: 0 lỗi; mọi import `@/...` đều tồn tại
- [x] Ghi chú: hrm KHÔNG nạp `v2-styles.scss` global — mỗi màn V2 tự `@import '@/assets/scss/v2-styles.scss';` trong `<style lang="scss">` (không scoped)

## Phase 2 — Backend lưu cấu hình bộ lọc (hrm-thanhan-api)
- [x] Migration `filter_customizations` (unique `created_by + table`, không FK)
- [x] Entity `FilterCustomization`, Service, Request `UpdateFilterCustomizationRequest`, Controller
- [x] Route `human/filter-customizations` (POST `/`, GET `/detail`)
- [x] Chạy migrate + gọi thử API — migration `database/migrations/2026_09_28_100000_create_filter_customizations_table.php` (đặt ở `database/migrations` theo quy ước dns); tinker: lưu 2 lần → 1 bản ghi (unique user+table), đọc lại đúng config, validate báo lỗi tiếng Việt; đã xóa bản ghi thử

## Phase 3 — Skill cho dns (`.claude/skills/`)
- [x] `button-convention` — viết lại: Phần A (V2BaseButton / V2BaseRowActions) + Phần B (chuẩn cũ)
- [x] `list-page` — Phần A V2 (SmartFilterPanel, DataTable, filterStateMixin, cột, xuất Excel, màn chi tiết) + Phần B cũ; giữ phân quyền theo cấp của dns
- [x] `modal-popup` (mới) — V2BaseModal, V2BaseSelectInModal, BaseConfirmModal, popup có bảng
- [x] `form-validate` (mới) — formValidateMixin, V2BaseError, rowFieldErrors, vmId: null, cuộn tới lỗi
- [x] `select-and-input-state` (mới) — danh mục khoá 🔒, allowClear, chip, ô disabled, nhãn nhân viên
- [x] Port thêm util: `utils/rowFieldErrors.js`, `utils/scrollToFirstError.js`, `utils/mixins/formValidateMixin.js` (sửa: cuộn bằng `scrollToFirstError`, đọc thêm 422 `data.error_messages`)
- [x] Danh mục V2Base (props chính) nằm trong skill `list-page`/`modal-popup`
- [x] Cập nhật bảng "Skill bắt buộc đọc" trong CLAUDE.md + memory (`project_v2_ui_convention`, phạm vi base-select2 / Required)

## Phase 4 — Màn thí điểm: Danh sách Đơn mua hàng
**BE**
- [x] `PurchaseOrderService::getList`: thêm tìm nhanh `keyword` (mã đơn, mã/tên NCC, tên người tạo — whereExists), lọc nhiều NCC `supplier_ids[]` (vẫn nhận `supplier_id` cũ), eager load `employee_create.info` + `withCount('products')` (bỏ N+1), luôn chốt `id desc`
- [x] Sửa lỗi sort: `(bool) 'false'` = true → dùng `filter_var(..., FILTER_VALIDATE_BOOLEAN)` (trước đây sort tăng dần không chạy)
- [x] `PurchaseOrder::STATUSES` thêm `color` (mã màu badge V2), giữ `text_type`
- [x] `PurchaseOrderResource` thêm `supplier_code`, `status_hex`, `creator_name` (chỉ tên), `created_at_text` (d/m/Y H:i) — giữ nguyên key cũ
- [x] Migration `2026_09_28_100000_add_supply_purchase_orders_to_column_customizations_table` (json nullable, không FK) + cast `supply_purchase_orders` trong `Human/Entities/ColumnCustomization` — đã chạy

**FE**
- [x] Helper mới `utils/format-number.js` (`formatMoney`, rỗng → '')
- [x] `constants.js` thêm `PERM_APPROVE`
- [x] `pages/supply/purchase_orders/index.vue` → V2: SmartFilterPanel floating (Trạng thái, NCC chọn nhiều, Loại đơn, Ngày đặt hàng gộp 1 ô, Mã đơn) + tìm nhanh; DataTable fixed-layout 11 cột; cấu hình cột; Xuất Excel qua popup chọn trường (FE, `exportSupplyGoods`); RowActions Duyệt(→ chi tiết)/Sửa/Xóa; BaseConfirmModal `confirm-delete-purchase-order`; filterStateMixin
- [x] Giữ nguyên API, quyền, `is_can_*` hiện có (Duyệt thêm điều kiện quyền `Duyệt đơn mua hàng` cho khớp màn chi tiết)
- [x] Chạy bộ tự kiểm A15 (grep) — sạch
- [x] Sửa lọc nhiều NCC: `buildQueryString` lặp khoá (`a=1&a=2`) nên PHP chỉ nhận giá trị cuối → FE gửi `supplier_ids` dạng `1,2,3`, BE nhận cả mảng lẫn chuỗi phân tách dấu phẩy
- [x] Kiểm tra trên trình duyệt (lọc, sắp xếp, phân trang, xóa, cấu hình cột, xuất Excel, giữ bộ lọc khi quay lại) — đạt
- [ ] User duyệt màn thí điểm (chờ phản hồi các điểm cần xác nhận của Phase 4)

### Checkpoint — 2026-09-28 23:45
Vừa hoàn thành: Kiểm tra màn thí điểm Đơn mua hàng trên trình duyệt — lọc (tìm nhanh, trạng thái, 1/nhiều NCC, ngày đặt hàng), sort tăng/giảm, phân trang, popup xóa, cấu hình cột lưu + F5, xuất Excel đúng cột, giữ bộ lọc khi vào chi tiết rồi quay lại
Đang làm dở: —
Bước tiếp theo: Chờ user duyệt màn thí điểm + trả lời Q1–Q4 → Phase 5
Blocked: Chờ user duyệt

### Bổ sung 30/09 — Bộ lọc đủ mọi cột của danh sách (user yêu cầu)
> Quy tắc: popup "Cài đặt bộ lọc" phải có ĐỦ trường lọc tương ứng mọi cột dữ liệu trên bảng, mặc định bật hết — **TRỪ cột tiền** (user: "những cái liên quan đến tiền thì bỏ").
- [x] BE `PurchaseOrderService::getList`: lọc `products_count_from/to` (has products, `filled()` để 0 vẫn lọc), `created_by_ids` (nhiều người, chuỗi `1,2`), `created_at_from/to`; tách helper private `parseIdList` (dùng chung cho `supplier_ids`)
- [x] BE endpoint `GET supply/purchase-orders/creators` — người đã tạo đơn (còn hiệu lực) → option bộ lọc Người tạo
- [x] FE `purchase_orders/index.vue`: thêm Số dòng hàng (khoảng số, slot `V2BaseCurrencyInput :precision="0"`, chờ Enter), Người tạo (chọn nhiều, nạp cùng NCC khi mở panel), Ngày tạo (khoảng ngày) + `initialStateForm`, `buildApiParams`, `handleReset`
- [x] ~~Tổng tiền (khoảng)~~ — đã làm rồi bỏ theo yêu cầu user (cả FE + BE)
- [x] Skill `list-page` A3 + A15: quy tắc "bộ lọc đủ mọi cột, trừ cột tiền"
- [x] Kiểm tra: tinker (creators, lọc SL dòng/người tạo/ngày tạo) + trình duyệt (8 ô hiện đủ, popup cài đặt tick hết, request đúng tham số, gõ số không gọi API từng phím, Làm mới xoá sạch)

### Checkpoint — 2026-09-30 09:25
Vừa hoàn thành: Bộ lọc màn Đơn mua hàng đủ mọi cột (trừ tiền), ghi quy tắc vào skill list-page
Đang làm dở: —
Bước tiếp theo: Chờ user duyệt màn thí điểm + Q1–Q4 → Phase 5 (bắt đầu Danh sách HĐ mua)
Blocked:

## Phase 5 — Chuyển các màn còn lại (sau khi user duyệt màn thí điểm)
- [ ] Danh sách: HĐ mua, Đề xuất cung ứng, Phiếu xử lý, HĐ kết xuất (contract_render)
- [ ] Form + chi tiết: Đơn mua, HĐ mua
  ### 5.1 — Form Đơn mua hàng (user yêu cầu 30/09 — dùng chung add / edit / show)
  - [x] `PurchaseOrderForm.vue`: bọc `.v2-styles` + import `v2-styles.scss`; `b-tabs` → `V2BaseTabNavigation` (+ `v-show`, tab có lỗi hiện ⚠); footer → `V2BaseButton` (Lưu · Lưu và gửi duyệt · Quay lại); `formValidateMixin` (`formError` → `formErrors`, `applyServerErrors`, cuộn `scrollToFirstError`); `$nuxt?.$loading?.` + `:interactable`; hỏi xác nhận `BaseConfirmModal` id riêng trước khi Gửi duyệt
  - [x] `GeneralTab.vue`: 3 khối `V2BaseFormSection`; `V2BaseLabel`/`Input`/`Select`/`DatePicker`/`Textarea`/`Error`; ô tự lấy → `disabled`; nút thêm nhanh liên hệ / địa chỉ → `V2BaseIconButton`
  - [x] `PaymentTab.vue`: `V2BaseFormSection` + `V2BaseSelect` (hình thức TT) + `V2BaseButton` Thêm dòng; bảng đợt: `V2BaseInput`/`CurrencyInput`/`DatePicker` + `V2BaseIconButton` xóa (dọn lỗi dòng `progress.*`); bảng theo đơn: `V2BaseCheckbox` + `V2BaseInput`/`CurrencyInput`; `V2BaseTextarea` ghi chú; lỗi `progress_total` → `V2BaseError`
  - [x] `ProductsTab.vue`: nút Chọn hàng hóa → `V2BaseButton`; cột Thao tác → `V2BaseIconButton`; ĐVT / Cty mua → `V2BaseSelect`; SL mua, SL theo phiếu, SL gốc → `V2BaseInput`; Đơn giá → `V2BaseCurrencyInput`; Ngày cần → `V2BaseDatePicker`; Ghi chú → `V2BaseInput`; lỗi → `V2BaseError`; xóa / thêm dòng dọn lỗi `products.*` (emit ra Form); chỉnh CSS bảng cho khớp
  - [x] Kiểm tra trình duyệt: `/supply/purchase_orders/add` (nhập, lỗi 422 nhảy đúng tab + cuộn, lưu), `/_id/edit`, `/_id` (xem) — đã kiểm: 422 nhảy đúng tab + ⚠, lỗi dòng dời đúng khi xoá dòng, tổng tiền cập nhật, chế độ xem khoá hết ô; KHÔNG bấm lưu thật trên dữ liệu
  - [x] Bảng hàng: layout ép `.default-layout input {height:35px}` → thu ô trong bảng về 28px (SL theo phiếu 22px); Cty mua / Ngày cần dùng size `xs`
  - Tồn đọng cần hỏi user: `V2BaseCurrencyInput` (component chung) hiện `1,000,000` (bảng dùng `1.000.000`) và `:focus` viền xanh đè viền đỏ lỗi; footer trang `/_id` vẫn nút cũ (slot trong `_id/index.vue`)
  - Chưa làm ở lượt này: các popup (Chọn hàng hóa, Đổi hàng, chi tiết phiếu/HĐ, NCC đã mua) — làm sau theo skill `modal-popup`
### Checkpoint — 2026-09-30 09:50
Vừa hoàn thành: 5.1 Form Đơn mua hàng (Form + 3 tab) chuyển V2, đã kiểm trên trình duyệt add / edit / show
Đang làm dở: —
Bước tiếp theo: chờ user duyệt giao diện + trả lời 2 điểm về V2BaseCurrencyInput; sau đó chuyển footer trang chi tiết và các popup của đơn mua
Blocked: sửa V2BaseCurrencyInput là component chung → cần user xác nhận

  ### 5.2 — Màn chi tiết Đơn mua hàng `/_id` (user yêu cầu 06/10 — "V2Base hết")
  - [x] `_id/index.vue`: footer → `V2Footer` (menu edit / approve / reject_approve, cùng cờ `is_can_*` với danh sách); bỏ `msgBoxConfirm` (V2Footer đã hỏi duyệt); popup Từ chối → `V2BaseRejectApproveModal` id riêng; lỗi tải → `/extras/404` (`replace`); lớp tải `$nuxt?.$loading` khi ghi; khung tải V2 (không `text-muted`)
  - [x] Lý do từ chối: đưa vào trong khung `.v2-styles` của form (slot `notice`), style V2
  - [x] `PurchaseOrderForm.vue`: tiêu đề `Chi tiết đơn mua hàng: <mã>`; slot `footer` ở chế độ xem render trần (V2Footer là thanh fixed); bỏ `text-muted` ô đang tải
  - [x] Popup xem: `SupplyDocDetailModal`, `ContractDetailModal` → `V2BaseModal`
  - [x] `purchase_contracts/components/SupplierHistoryModal.vue` (dùng chung với HĐ mua — user đồng ý sửa bản chung) → `V2BaseModal`
  - [x] `ProductsTab.vue`: `msgBoxConfirm` (xóa dòng / bỏ phiếu) → `BaseConfirmModal` id riêng
  - [x] Tab dùng chung add/sửa/xem (`GeneralTab`, `PaymentTab`, `ProductsTab`): bỏ `text-muted` (→ màu #6b7280), ô rỗng để trống thay `—` (giữ nguyên phép so `!== '—'` với dữ liệu cũ đã lưu sẵn dấu gạch)
  - [~] Kiểm tra compile ✅ (9 file) · trình duyệt ❌ chưa chạy — token `e2e/.env` hết hạn (401)
  - [ ] Hỏi user: lỗi trong component chung `V2BaseRejectApproveModal` (`:disabled` vô tác dụng, `::rows`, `*` trần, nút "Đồng ý" thiếu `primary`) + `V2Footer` (câu hỏi duyệt chung chung, nhãn "Không duyệt")

  ### Checkpoint — 06/10/2026
  Vừa hoàn thành: 5.2 màn chi tiết Đơn mua hàng lên V2 (trang `_id`, form, 3 popup xem, confirm trong ProductsTab, dọn text-muted/`—` ở 3 tab)
  Đang làm dở: không
  Bước tiếp theo: user làm mới `ACCESS_TOKEN` trong `e2e/.env` → kiểm trên trình duyệt :3001 (duyệt / từ chối / mở 3 popup); chốt việc sửa component chung
  Blocked: token e2e hết hạn
  ### 5.3 — Chuyển TOÀN BỘ màn Cung ứng còn lại sang V2 (user yêu cầu 06/10 — "sửa hết", chạy song song theo module)
  Quyết định user 06/10: sửa component chung · ô tiền kiểu VN · làm song song 4 agent theo module.
  **Chung (làm trước):**
  - [x] `V2BaseRejectApproveModal` dựng lại trên `V2BaseModal` (giữ API `id` + `@confirm`): `:rows`, `V2BaseLabel required`, nút Xác nhận `primary danger` khoá bằng `:interactable` + chặn bấm kép, Hủy cuối
  - [x] `V2Footer`: nhãn "Từ chối"; prop `confirm-message` (câu hỏi nêu tên phiếu, trống = câu cũ); `text-accept` đúng chữ nút; popup xác nhận id riêng `v2-footer-confirm-<uid>` (hết bẫy trùng id `confirm`); bỏ console.log
  - [x] `V2BaseCurrencyInput`: hiển thị `1.234.567,89` (khớp `formatMoney`); viền đỏ lỗi thắng viền focus
  - [x] Màn chi tiết đơn mua dùng nút `reject_approve` có sẵn + `confirm-message`
  - [x] Migration `2026_10_06_100000_add_supply_lists_to_column_customizations_table` (5 cột json) + cast — đã chạy
  **Theo module (agent song song):**
  - [x] A — HĐ mua `purchase_contracts/*` (danh sách, chi tiết, form + 4 tab, popup chọn hàng) + `purchase_orders/components/GoodsPickerModal.vue` — BE: lọc từng cột + `GET purchase-contracts/creators`
  - [x] B — Đề xuất cung ứng `supply_proposals/*` (danh sách, hộp thư, form, components) — BE: `list-creators`, `list-customers`; `listHelpers.js` mới
  - [x] C — Phiếu xử lý `supply_handlings/*` (danh sách, form, components) — BE: lọc + `GET supply-handlings/creators`
  - [x] D — HĐ kết xuất `contract_render/*` + Báo cáo nhu cầu mua `reports/purchase-demand` (Dashboard để nguyên) — BE: `GET rendered-contracts/filter-options`
  - [x] Rà chéo kết quả 4 agent: compile 40/41 OK (dashboard chỉ lỗi giả do style rỗng), php -l sạch, route tĩnh trước `{id}`; grep A15 còn sót 2 file ↓
  - [x] Dọn nốt `supply_proposals/components/GoodsPickerModal.vue` (dùng ở Đề xuất + Phiếu xử lý) sang V2 — xong (phân trang đổi 25 → 20/50/100, chờ user xác nhận)
  - [x] Đổi 7 icon `mdi` còn sót ở 2 ProductsTab (HĐ mua, Đơn mua) sang Remixicon 2.4.0 (`ri-corner-*` không có ở 2.4 → dùng `ri-arrow-right-down-line`)
  - [x] Rà cuối: 42/42 file `.vue` trong `pages/supply` compile OK (trừ dashboard — lỗi giả do style rỗng), grep mẫu cũ sạch
  - [x] Dọn nốt `purchase_orders/components/ProductsTab.vue` (bộ lọc b-form-*, ô chiết khấu base-input-field, 3 ô tổng currency-input) — xong, compile OK
  - [x] Báo cáo nhu cầu mua: header bảng chính nền `#f5f8f7` gần trùng nền trang → đổi nền xanh ngọc nhạt `#eaf4f2` (bản `#d9ebe7` user chê đậm quá), chữ `#1f4f49`, viền `#d3e4e0` (user báo 06/10)
  - [x] Báo cáo nhu cầu mua: ô tích cột chọn căn giữa dọc (lệch xuống giữa dòng gộp, không ngang số STT) + cột 34px còn padding 10px làm checkbox bootstrap lệch → căn đỉnh, bỏ padding ngang, căn giữa cột (user báo 06/10)
  - [x] HĐ kết xuất: cột Phiếu đề xuất hiện `[]` khi HĐ chưa có phiếu — gốc slot `#cell-proposal_items` có `v-if` → Vue 2 render nội dung mặc định (giá trị thô). Bỏ `v-if` ở gốc; đã quét toàn `pages/supply`, chỉ có chỗ này; ghi bẫy vào skill list-page A9 (user báo 06/10)
  - [x] Rà soát toàn client lỗi ô hiện giá trị thô (`[]`): quét bằng AST vue-template-compiler mọi slot `#cell-*` có thể render rỗng → thêm 2 chỗ: Đề xuất `inbox.vue` cột File, `index.vue` cột Phiếu xử lý (gốc `v-for`) → bọc `<div>`; xác nhận mọi cột bảng V2 đều có slot; các chỗ `{{ x }}` in thẳng đều là chuỗi (user yêu cầu 06/10)
  - [x] Mất ô tick "Hiện cả dòng đã mua đủ" / "Chỉ mã chưa có HĐ / đơn mua" (Báo cáo nhu cầu mua) + "Không có phiếu đề xuất mua" (tab Hàng hóa HĐ mua): `V2BaseCheckbox` truyền chữ qua slot → `singleMode=false` → chế độ nhiều ô với `options` rỗng, không render gì. Đổi sang prop `label`; sửa cả khối lọc đang ẩn của Đơn mua; quét AST toàn client sạch (user báo 06/10)
  - [x] Báo cáo nhu cầu mua: chuyển 2 ô tick "Hiện cả dòng đã mua đủ" / "Chỉ mã chưa có HĐ / đơn mua" từ header bộ lọc vào khối Tìm kiếm nâng cao (field `hideLabel` + slot `#field-*`) (user yêu cầu 06/10)
  - [x] Chi tiết HĐ (`contract/contract/_id`, ?from=supply_render): bỏ dòng "Người tiếp nhận: … — ngày giờ" (giữ `receiveInfo` cho các nút) (user yêu cầu 06/10)
  - [ ] Kiểm trên trình duyệt (chờ user làm mới token e2e)
- [x] Form: Đề xuất cung ứng, Phiếu xử lý (gộp vào 5.3)
- [x] Báo cáo nhu cầu mua, Dashboard (gộp vào 5.3)

## Cần user xác nhận (hàm dùng chung)
- [ ] (Q1) Cập nhật plugin `select2-custom.js` / `select2-focus.js` theo bản hrm (id duy nhất cho select2, focus ô tìm kiếm, bấm × không mở dropdown) — ảnh hưởng mọi màn
- [ ] (Q2) Đổi `ColumnCustomizationService` sang bảng key-value `user_column_settings` như hrm (hiện mỗi màn phải thêm 1 cột vào `column_customizations`)
- [ ] (Q3) Port plugin `safe-loading.js` (+ `store/loading.js`) và `confirm-dialog.js` (`this.$confirm`) của hrm — hiện màn V2 dùng `$nuxt.$loading` + `BaseConfirmModal`
- [ ] (Q4) Thêm ~14 rule vee-validate custom của hrm (`positive_integer`, `greater_than`, `date_greater_than`…) vào `plugins/vee-validate.js`

---

### Checkpoint — 06/10/2026 (5.3 chuyển toàn bộ Cung ứng sang V2)
Vừa hoàn thành: 4 module A–D + dọn nốt popup chọn hàng Đề xuất, tab Hàng hóa Đơn mua, icon mdi; compile 42/42, php -l sạch, route tĩnh đặt trước `{id}`
Đang làm dở: không
Bước tiếp theo: user trả lời các câu hỏi nghiệp vụ (xem báo cáo chat 06/10) → kiểm trên trình duyệt khi có token e2e mới
Blocked: token e2e hết hạn (401) — cần làm mới `ACCESS_TOKEN` trong `dns/e2e/.env`

