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

## Phase 5 — Đợt bổ sung (@khoipv, 2026-08-12)

User yêu cầu bổ sung popup cho 4 màn: danh mục ngân hàng · danh mục tài khoản ngân hàng ·
danh mục gói bảo dưỡng · yêu cầu chuyển hàng.
Rà lại thì **3/4 màn đã làm ở đợt 1** → chỉ còn màn ngân hàng (`/human/banks`) là chưa có.

- [x] T5.1 `pages/human/banks/components/BankModel.vue` — modal Tạo mới/Sửa/Xem ngân hàng
      (`unsavedModalMixin`, snapshot `this.data` mặc định, ref `my-modal` mặc định → không phải override)
- [x] T5.2 `pages/human/banks/components/BankBranchesAddModel.vue` — modal Thêm/Sửa chi nhánh
      (như trên)
- [x] T5.3 Rà 3 màn đợt 1 user nêu tên — **đã đúng khuôn, không phải sửa gì**:
      `finance/account-banks/AccountBankModal.vue` (3 sự kiện + `markFormPristine` cuối `loadDetail`
      vì `open()` show trước khi load) · `customer-care/services/*` (`unsavedChildFormMixin` ở
      create/edit + `unsavedChangesMixin` ở `ServiceFormComponent`, snapshot gộp `form` + `maintains`
      + `levelCols` + `groups` + `attachmentsList` + `newFiles.length`) ·
      `finance/product-transfer-requests/*` (cùng khuôn, `markFormSaved()` ở cả 2 nhánh lưu)
- [x] T5.4 Verify parse template + script 5 file (vue-template-compiler + @babel/parser) → PASS
- [x] T5.6 User báo popup xác nhận ở màn ngân hàng **to hơn** popup màn dự án tiền khả thi.
      Truy ra: 2 màn vốn dùng CHUNG đúng 1 popup (`$bvModal.msgBoxConfirm`, options y hệt ở cả
      `unsavedChangesMixin` lẫn `unsavedModalMixin`) — thủ phạm là CSS khung modal của chính màn
      ngân hàng khai `::v-deep .modal-dialog { min-width: 600px; max-width: 800px }` **trần**,
      phủ luôn popup mở chồng lên. Fix: tách khối CSS khung modal sang block `<style>` KHÔNG scoped,
      bọc trong id modal (`#modal-bank` / `#modal-bank-branches` / `#modal-bank-branches-add`)
      → popup về 500px mặc định. Sửa 3 file, gồm cả `BankBranchesModel.vue` (không gắn guard
      nhưng CSS cũng leak).
      ⚠️ Lưu ý chung cho các đợt sau: modal nào khai `::v-deep .modal-dialog/.modal-header/...`
      trần đều làm popup xác nhận méo — rà khi gắn guard.
- [ ] T5.5 **CHƯA TEST TRÌNH DUYỆT** — 5 ca/modal cho 2 modal màn ngân hàng + xác nhận kích thước popup

**Ngoài phạm vi T5:** `BankBranchesModel.vue` (modal danh sách chi nhánh) — chỉ có ô lọc
Tỉnh/TP + Tên chi nhánh, không phải form nhập liệu lưu DB → không gắn guard.

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
