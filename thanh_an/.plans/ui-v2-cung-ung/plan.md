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

## Phase 5 — Chuyển các màn còn lại (sau khi user duyệt màn thí điểm)
- [ ] Danh sách: HĐ mua, Đề xuất cung ứng, Phiếu xử lý, HĐ kết xuất (contract_render)
- [ ] Form + chi tiết: Đơn mua, HĐ mua
- [ ] Form: Đề xuất cung ứng, Phiếu xử lý (logic phức tạp — làm cuối)
- [ ] Báo cáo nhu cầu mua, Dashboard

## Cần user xác nhận (hàm dùng chung)
- [ ] (Q1) Cập nhật plugin `select2-custom.js` / `select2-focus.js` theo bản hrm (id duy nhất cho select2, focus ô tìm kiếm, bấm × không mở dropdown) — ảnh hưởng mọi màn
- [ ] (Q2) Đổi `ColumnCustomizationService` sang bảng key-value `user_column_settings` như hrm (hiện mỗi màn phải thêm 1 cột vào `column_customizations`)
- [ ] (Q3) Port plugin `safe-loading.js` (+ `store/loading.js`) và `confirm-dialog.js` (`this.$confirm`) của hrm — hiện màn V2 dùng `$nuxt.$loading` + `BaseConfirmModal`
- [ ] (Q4) Thêm ~14 rule vee-validate custom của hrm (`positive_integer`, `greater_than`, `date_greater_than`…) vào `plugins/vee-validate.js`

---
