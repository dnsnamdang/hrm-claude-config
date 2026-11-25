# Điều chỉnh công nợ NCC — cho chọn trùng HĐ mua khi khác NCC (25/11/2026)

Yêu cầu: luồng mua nhập khẩu, 1 tổng hợp chi phí NK có nhiều NCC → nhiều NCC cùng công nợ trên 1 HĐ mua.
Màn `bill_adjust_dept_requests/create` báo "Hợp đồng mua điều chuyển đến trùng với điều chuyển từ" khi
Từ (NCC A, HĐ X) → Đến (NCC B, HĐ X). Cần cho phép.

Hạch toán (`BillAdjustDeptRequest` saveAccounts) đã tách theo customer_id + contract → không cần sửa.

- [x] BE `BillAdjustDeptRequestController::validateRequest` — nhánh NCC chỉ chặn khi cùng HĐ mua **và** cùng NCC (cả 2 nhánh is_begin)
- [x] FE `formJs.blade.php` applyBuyContracts (Chọn nhanh HĐ) — xoá dòng cũ theo khoá NCC+HĐ thay vì chỉ HĐ
- [x] ĐÃ push develop_02 `5e9a228a93` + gop_db `67a2947007` (25/11)
- [ ] Kiểm thử trên màn thật (chưa chạy)
