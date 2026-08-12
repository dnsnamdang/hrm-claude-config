# Plan — Cảnh báo "Thông tin chưa lưu" cho màn danh mục (đợt 1)

**Phụ trách:** @junfoke · **Nhánh:** `gop_db` · Chỉ FE (`hrm-client`), không đụng BE.

## Phase 1 — Hạ tầng

- [x] T1.1 Tạo `hrm-client/utils/mixins/unsavedModalMixin.js` (file MỚI, không sửa `unsavedChangesMixin.js`)

## Phase 2 — 9 modal danh mục

- [x] T2.1 `components/modal/customer-care/level-modal.vue` — Cấp dịch vụ bảo dưỡng
- [x] T2.2 `components/modal/customer-care/note-maintenance-modal.vue` — Ghi chú kiểm tra bảo dưỡng
- [x] T2.3 `components/modal/customer-care/cost-modal.vue` — Dịch vụ SC & chi phí khác
- [x] T2.4 `components/modal/finance/currency-modal.vue` — Tiền tệ
- [x] T2.5 `components/modal/finance/type-account-modal.vue` — Loại tài khoản
- [x] T2.6 `pages/finance/cost-debts/CostDebtModal.vue` — Mã phí
- [x] T2.7 `pages/finance/works/WorkModal.vue` — Vụ việc
- [x] T2.8 `pages/finance/source-capitals/SourceCapitalModal.vue` — Nguồn vốn
- [x] T2.9 `pages/finance/account-banks/AccountBankModal.vue` — Tài khoản ngân hàng ⚠️ feature của @khoipv

## Phase 3 — 9 file form dạng trang (dùng `unsavedChangesMixin` có sẵn)

- [x] T3.1 `pages/customer-care/service-price-config/index.vue` (lưu xong ở lại màn → `markFormPristine`)
- [x] T3.2 `pages/customer-care/device-errors/create.vue`
- [x] T3.3 `pages/customer-care/device-errors/_id/edit.vue`
- [x] T3.4 `pages/finance/accounts/add.vue`
- [x] T3.5 `pages/finance/accounts/_id/edit.vue`
- [x] T3.6 `pages/customer-care/services/create.vue` ⚠️ @khoipv
- [x] T3.7 `pages/customer-care/services/_id/edit.vue` ⚠️ @khoipv
- [x] T3.8 `pages/finance/product-transfer-requests/create.vue` ⚠️ @khoipv
- [x] T3.9 `pages/finance/product-transfer-requests/_id/edit.vue` ⚠️ @khoipv

## Phase 4 — Kiểm thử + tài liệu

- [ ] T4.1 **CHƯA TEST TRÊN TRÌNH DUYỆT** — mới chỉ parse được toàn bộ 24 file (template + script).
      Cần test 4 ca/màn: không sửa gì → thoát thẳng · sửa 1 trường → hiện popup ·
      Ở lại giữ nguyên dữ liệu · lưu xong → không hỏi
- [x] T4.2 Cập nhật `.claude/skills/unsaved-changes/SKILL.md` bổ sung mục modal

## Phát sinh khi làm

- Thêm mixin thứ 3 `unsavedChildFormMixin.js`: 4 màn (device-errors, services, accounts,
  product-transfer-requests) có form nằm ở component CON, mà `beforeRouteLeave` của vue-router
  chỉ chạy trên component của route → trang vỏ phải uỷ quyền `isFormDirty()` cho con.
- `ProductTransferRequestForm.vue` vốn đã có `buildSnapshot()/isDirty()` riêng cho nút Hủy
  (wording khác chuẩn). Đã bỏ cặp này + confirm riêng ở `cancel()` để không hỏi 2 lần;
  giờ toàn bộ đi qua popup chuẩn.
- `serials` không có form Thêm/Sửa → bỏ khỏi phạm vi (15 màn → 14 màn thực làm).

## Checkpoint

### Checkpoint — 2026-08-12

Vừa hoàn thành: Phase 1-3 (2 mixin mới + 9 modal + 9 file form trang) và T4.2.
Đang làm dở: không.
Bước tiếp theo: T4.1 — chạy `npm run dev` test tay 14 màn; sau đó chốt với anh Nam
phương án gộp `unsavedModalMixin` vào `unsavedChangesMixin` trước khi làm đợt 2.
Blocked: 4 file thuộc feature của @khoipv (account-banks, services ×2 wrapper + form,
product-transfer-requests) — đã sửa theo yêu cầu, cần báo lại chủ feature.
