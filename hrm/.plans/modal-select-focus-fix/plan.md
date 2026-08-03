# Fix focus dropdown trong popup (V2BaseSelect trong b-modal)

## Bug
Trong Bootstrap `<b-modal>`, dùng `V2BaseSelect` → dropdown select2 gắn `<body>` (ngoài `.modal-content`) → `enforceFocus` của Bootstrap giật focus về modal → ô search không nhận bàn phím, user phải click mới gõ. `V2BaseSelectInModal` set `dropdownParent=.modal-content` (tự nhận biết: full-page thì null → chạy như thường) nên không bị.

## Fix — đổi V2BaseSelect → V2BaseSelectInModal (5 file)
- [x] `components/assign-components/customer/CustomerForm.vue` — 22 select (popup Thêm nhanh KH + 9 trang full-page). Đã test cả 2 ngữ cảnh.
- [x] `components/FileAttachmentTable.vue` — 2 select (2 approval modal + trang).
- [x] `components/V2BaseImportTable.vue` — 1 select (V2BaseImportModal).
- [x] `components/V2BaseCompanyDepartmentFilter.vue` — 4 select: component đã có sẵn conditional `v-if="isModal"`→InModal / `v-else`→V2BaseSelect nhưng caller (my-job modals) KHÔNG truyền isModal → v-else lỗi. Gộp về InModal-only (bỏ phụ thuộc isModal, robust mọi ngữ cảnh).
- [x] `pages/assign/tasks/components/CreateTaskModal.vue` — 2 select nằm trong khối comment (code chết, UI thật dùng SearchPicker) → REVERT, không đụng.

Nuxt `components: true` (auto-import) → InModal tự resolve kể cả file chưa import.
Lưu ý: import `V2BaseSelect` cũ ở 4 file thành unused (vô hại, chưa dọn).

## Test (Playwright, :3000)
- [x] Popup Thêm nhanh KH (b-modal): mở select "Loại hình tổ chức" → dropdown NẰM TRONG modal-content, ô search được focus, gõ "c" trực tiếp OK. (trước fix: activeElement = modal-content, không gõ được)
- [x] Full-page /assign/customers/add (CustomerForm): select focus+gõ OK, dropdown gắn body → KHÔNG regression.
- [x] Full-page /assign/prospective-projects (V2BaseCompanyDepartmentFilter): 4 select render, "Công ty" focus+gõ OK, 0 lỗi.
- [x] Trang /assign/tasks (import filter): 0 lỗi compile.
- [ ] (chưa UI-test, dùng chung component đã verify): FileAttachmentTable trong approval modal, V2BaseImportTable trong import modal.

### Checkpoint — 2026-07-24
Vừa xong: fix + test 5 file. Bước tiếp: (tuỳ chọn) dọn import V2BaseSelect unused; UI-test 2 modal còn lại nếu cần.
