# Fix: Sửa HĐLĐ chọn lại mẫu in nhưng lưu vẫn giữ nội dung cũ — @khoipv

URL lỗi: `/human/employment-contract/145/edit` — chọn mẫu "Hợp đồng lao động_kxđ" (`/human/report_templates/9`) nhưng bản in Điều 1 vẫn ghi "Hợp đồng lao động xác định thời hạn".

## Phase 1 — Điều tra (XONG)

- [x] FE `components/EmploymentContract.vue`: chọn Mẫu in → `onChangeTemplate()` tải `human/print-templates/{id}` → gán `form.print_template` (HTML) → CKEditor hiện đúng. Trang `_id/edit.vue` gửi cả `form` (có `print_template`) lên `PUT human/employment-contracts/{id}` → FE đúng.
- [x] BE `EmploymentContractService::update()` chỉ `update($request->only([...]))` với danh sách cột, **thiếu `print_template`** → bản HTML mới bị bỏ qua, chỉ lưu `print_template_id`.
- [x] BE `EmploymentContractController::print()`: ưu tiên `employment_contracts.print_template` (bản chụp), chỉ fallback `print_templates` khi bản chụp rỗng → luôn in bản chụp cũ.
- [x] `store()` dùng `$request->all()` nên lúc tạo có lưu bản chụp → HĐ 145 giữ bản chụp lúc tạo (lúc đó mẫu 9 còn nội dung "xác định thời hạn" hoặc người tạo chọn mẫu khác rồi đổi ID), sửa bao nhiêu lần cũng không ghi đè được.
- [x] DB local (`thanhan_stag_07052026`): mẫu 9 hiện đúng "không xác định thời hạn"; không có HĐ 145 (bản sao cũ, max id 87) — chưa xem được bản chụp HĐ 145 trên demo.
- [x] Thiếu sót từ feature `employment-contract-print-template` (plan cũ không thêm `print_template` vào whitelist update).

## Phase 2 — Fix

- [x] BE `Modules/Human/Services/EmploymentContractService.php` `update()`: thêm `'print_template'` vào `$request->only([...])`
- [x] `php -l` OK
- [x] Commit `3299db91` + push `origin/master` (repo `hrm-thanhan-api`) — theo yêu cầu user
- [ ] User test: vào sửa HĐ 145 → chọn lại mẫu kxđ → Lưu → In → Điều 1 ra "không xác định thời hạn"

## Checkpoint — 2026-11-13 (wrap up)

Vừa hoàn thành: thêm `print_template` vào whitelist update, commit `3299db91` đã push `origin/master`
Đang làm dở: —
Bước tiếp theo: deploy BE lên demo → sửa lại HĐ 145 (chọn lại mẫu → Lưu) → In kiểm tra; các HĐ khác từng đổi mẫu khi sửa cũng phải lưu lại như vậy
Blocked:
