# Fix: Tạo/Sửa HĐLĐ — lỗi 422 chỉ hiện ở vài trường — @khoipv

Màn: `/human/employment-contract/add`, `/human/employment-contract/{id}/edit` (dùng chung `components/EmploymentContract.vue`).

## Phase 1 — Điều tra (XONG)

- [x] BE `StoreEmployeeContractRequest` có rule cho 10 trường: `employee_id`, `contracting_unit_id`, `contract_number`, `effective_date`, `sign_day`, `contract_type`, `expiration_date`, `print_type`, `print_template_id`, `print_template`. Message tiếng Việt không kèm tên trường ("Bắt buộc phải nhập", "Không hợp lệ") → phải hiện ngay dưới ô, toast liệt kê không có nghĩa.
- [x] FE chỉ đọc `errorsMsg.contract_number`; 9 trường còn lại chỉ hiện lỗi vee-validate phía client → lỗi server (VD `date` sai định dạng, `unique`, `expiration_date` theo loại HĐ) không hiện.
- [x] Watcher `form` (deep) emit `update:errorsMsg {}` mỗi khi bất kỳ ô nào đổi → sửa 1 ô là mất hết lỗi các ô khác.
- [x] Lỗi ở tab "Mẫu in" (`print_type`, `print_template_id`, `print_template`) không thấy được khi đang đứng ở tab "Thông tin hợp đồng".
- [x] `_id/edit.vue` khởi tạo `errorsMsg: []` (mảng) thay vì `{}`.

## Phase 2 — Fix FE (`components/EmploymentContract.vue`, `_id/edit.vue`)

- [x] Thêm method `serverError(field)` lấy message đầu tiên từ `errorsMsg`
- [x] Hiện lỗi server dưới đủ 10 trường (thêm span lỗi dưới editor `print_template`)
- [x] Thay watcher deep `form` bằng watcher từng trường → đổi ô nào chỉ xoá lỗi ô đó
- [x] `b-tabs` có `v-model`: có lỗi (server hoặc client) → tự nhảy sang tab chứa lỗi đầu tiên; tiêu đề tab có lỗi tô đỏ
- [x] `_id/edit.vue`: `errorsMsg: {}`
- [x] Compile thử template + script bằng `vue-template-compiler` → không lỗi
- [x] Commit `982bfffd` + push `origin/master` (repo `hrm-thanhan-client`) — theo yêu cầu user
- [ ] User test: Sửa HĐ → để trống/nhập sai các trường ở cả 2 tab → Lưu → lỗi hiện đủ dưới từng ô, tự nhảy tab

## Checkpoint — 2026-11-13 (wrap up)

Vừa hoàn thành: sửa FE hiện đủ lỗi 422, commit `982bfffd` đã push `origin/master`
Đang làm dở: —
Bước tiếp theo: deploy FE lên demo → user test tay màn Sửa/Tạo HĐLĐ
Blocked:
