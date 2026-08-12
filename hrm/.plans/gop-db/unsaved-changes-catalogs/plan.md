# Plan — Cảnh báo "Thông tin chưa lưu" cho màn danh mục (đợt 1)

**Phụ trách:** @junfoke · **Nhánh:** `gop_db` · Chỉ FE (`hrm-client`), không đụng BE.

## Phase 1 — Hạ tầng

- [ ] T1.1 Tạo `hrm-client/utils/mixins/unsavedModalMixin.js` (file MỚI, không sửa `unsavedChangesMixin.js`)

## Phase 2 — 9 modal danh mục

- [ ] T2.1 `components/modal/customer-care/level-modal.vue` — Cấp dịch vụ bảo dưỡng
- [ ] T2.2 `components/modal/customer-care/note-maintenance-modal.vue` — Ghi chú kiểm tra bảo dưỡng
- [ ] T2.3 `components/modal/customer-care/cost-modal.vue` — Dịch vụ SC & chi phí khác
- [ ] T2.4 `components/modal/finance/currency-modal.vue` — Tiền tệ
- [ ] T2.5 `components/modal/finance/type-account-modal.vue` — Loại tài khoản
- [ ] T2.6 `pages/finance/cost-debts/CostDebtModal.vue` — Mã phí
- [ ] T2.7 `pages/finance/works/WorkModal.vue` — Vụ việc
- [ ] T2.8 `pages/finance/source-capitals/SourceCapitalModal.vue` — Nguồn vốn
- [ ] T2.9 `pages/finance/account-banks/AccountBankModal.vue` — Tài khoản ngân hàng ⚠️ feature của @khoipv

## Phase 3 — 9 file form dạng trang (dùng `unsavedChangesMixin` có sẵn)

- [ ] T3.1 `pages/customer-care/service-price-config/index.vue` (lưu xong ở lại màn → `markFormPristine`)
- [ ] T3.2 `pages/customer-care/device-errors/create.vue`
- [ ] T3.3 `pages/customer-care/device-errors/_id/edit.vue`
- [ ] T3.4 `pages/finance/accounts/add.vue`
- [ ] T3.5 `pages/finance/accounts/_id/edit.vue`
- [ ] T3.6 `pages/customer-care/services/create.vue` ⚠️ @khoipv
- [ ] T3.7 `pages/customer-care/services/_id/edit.vue` ⚠️ @khoipv
- [ ] T3.8 `pages/finance/product-transfer-requests/create.vue` ⚠️ @khoipv
- [ ] T3.9 `pages/finance/product-transfer-requests/_id/edit.vue` ⚠️ @khoipv

## Phase 4 — Kiểm thử + tài liệu

- [ ] T4.1 Test 4 ca/màn: không sửa gì → thoát thẳng · sửa 1 trường → hiện popup · Ở lại giữ nguyên dữ liệu · lưu xong → không hỏi
- [ ] T4.2 Cập nhật `.claude/skills/unsaved-changes/SKILL.md` bổ sung mục modal

## Checkpoint
