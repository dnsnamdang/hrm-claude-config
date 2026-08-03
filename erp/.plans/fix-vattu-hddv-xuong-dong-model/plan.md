# Fix UI: vật tư HĐ dịch vụ — Model xuống dòng dưới Mã hàng

## Bug
Danh sách vật tư trong HĐ dịch vụ (warranty_repair_contracts) hiển thị 'Mã hàng: ... - Model: ...' cùng 1 dòng (nối bằng ' - '). Cần Model xuống dòng riêng.

## Fix
File: resources/views/customercare/warranty_repair_contracts/form.blade.php dòng 506 — đổi <span> - </span> thành <br>.

## Tasks
- [ ] Sửa dòng 506 (separator ' - ' → <br>)
- [ ] User reload màn HĐ dịch vụ kiểm tra Model đã xuống dòng

### Checkpoint — 2026-06-30
Vừa hoàn thành: `warranty_repair_contracts/form.blade.php` dòng 506 — đổi separator " - " thành `<br>` để Model xuống dòng dưới Mã hàng (danh sách vật tư HĐ dịch vụ).
Đang làm dở: không.
Bước tiếp theo: USER reload màn HĐ dịch vụ kiểm tra Model đã xuống dòng → rồi commit.
Blocked:
