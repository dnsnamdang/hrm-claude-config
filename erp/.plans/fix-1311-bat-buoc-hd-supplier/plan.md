# Fix: TK 1311/1312 luôn bắt buộc chọn HĐ/Đơn hàng kể cả đối tượng Supplier

## Bối cảnh
Phiếu điều chỉnh công nợ phòng ban (bill_adjust_dept). Rule "1311/1312 (account_id 22/23) bắt buộc `contractable_id`" trong `BillAdjustDeptStoreRequest` (dòng ~85) bị chặn bởi điều kiện `objectable_type == Customer::class`. Nhưng nhiều dòng lưu đối tượng là `Supplier` (cùng bảng customers, is_supplier) → rule bị lọt → 1311 lưu được không cần HĐ (phiếu 12581 dòng 33259).
Quyết định user (2026-07-30): **1311/1312 LUÔN bắt buộc HĐ/đơn hàng, kể cả Supplier.**

## Tasks
- [ ] Store: mở rộng điều kiện dòng 85 → `in_array(objectable_type, [Customer, Supplier])`
- [ ] Thêm message `details.*.contractable_id.required`
- [ ] Update request: rà + đồng bộ logic (đang ép contract_id required luôn — kiểm khác biệt)
- [ ] FE create/edit: đảm bảo hiện lỗi inline tại ô Đơn hàng/HĐ (is-invalid + invalid-feedback)
- [ ] php -l + verify

### Checkpoint — 2026-07-30
Vừa hoàn thành (BillAdjustDeptStoreRequest — dùng cho cả store & update):
- Điều kiện require contractable_id cho 1311/1312 (account_id 22/23): objectable_type mở rộng `in_array([Customer, Supplier])` (trước chỉ Customer → Supplier bị lọt).
- Miễn trừ: CHỈ còn "KHÁCH KHÔNG RÕ" — đã BỎ hard-code `objectable_id == 10929`.
- Thêm message `details.*.contractable_id.required` = "Bắt buộc chọn Đơn hàng/Hợp đồng".
- FE có sẵn ô lỗi inline (bill_adjust_depts/form.blade.php:366). BillAdjustDeptUpdateRequest = dead code, không đụng.
php -l sạch. CHƯA commit.
Lưu ý: giữ CẢ 1311(22) và 1312(23) — user chỉ nhắc 1311 nhưng không yêu cầu bỏ 1312 (bỏ sẽ là regression). Nếu chỉ muốn 1311 thì báo.
Bước tiếp: user test màn tạo/sửa phiếu điều chỉnh công nợ (1311 + Supplier bỏ trống HĐ → báo đỏ).

### Checkpoint — 2026-07-30 (v2: bỏ điều kiện objectable_type)
User làm rõ: KHÔNG quan tâm objectable_type. Chỉ cần account_id ∈ {22,23} và KHÁC "KHÁCH KHÔNG RÕ" → bắt buộc contractable_id.
Đã bỏ toàn bộ điều kiện objectable_type (Customer/Supplier). Logic mới: if account 22/23 && !là khách không rõ → require. php -l sạch.
