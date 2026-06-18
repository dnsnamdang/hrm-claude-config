# BillAdjustDept — validate trùng cặp: bỏ qua khi không có hợp đồng

## Yêu cầu
Trong `validateDetails()` của phiếu điều chỉnh công nợ (`bill_adjust_dept/create`), rule "Không trùng cặp (account_id – objectable – contractable) trong cùng nhóm" **chỉ áp dụng khi dòng CÓ hợp đồng**. Dòng không có hợp đồng (`contractable_id` rỗng) thì **không bắt trùng**.

## Fix
File: `app/Model/IncomeExpenditure/BillAdjustDept.php` — method `validateDetails()`.
- [x] Bọc đoạn check trùng cặp trong `if (!empty($detail['contractable_id'])) { ... }` → không có hợp đồng thì bỏ qua (không tính pairKey, không chặn).
- [x] `php -l` sạch.

## Kiểm thử (user)
- [ ] Cùng nhóm định khoản, 2 dòng cùng account_id + cùng khách nhưng **không có hợp đồng** → lưu được (không báo trùng).
- [ ] 2 dòng cùng account_id + khách + **cùng hợp đồng** → vẫn báo trùng như cũ.
- [ ] Các rule khác (tổng nợ=có, nhập nợ/có, vượt báo có…) giữ nguyên.

### Checkpoint — 2026-06-10
Vừa hoàn thành: bỏ qua check trùng cặp khi không có hợp đồng
Bước tiếp theo: user test
Blocked:
