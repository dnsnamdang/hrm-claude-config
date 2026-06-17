# Plan — Fix: bug "Vui lòng chuyển duyệt..." khi duyệt hỗ trợ hạch toán

## Bối cảnh
Màn `admin/sale/principle-contracts/{id}/support-accounting`. Người duyệt không phải Giám đốc/BGD
(vd Nguyễn Đình Đông = "Giám đốc chi nhánh") bị chặn duyệt với toast "Vui lòng chuyển duyệt để được
phê duyệt đề xuất mới của bạn", dù đề xuất KHÔNG lệch quy chế. Admin (BGD) duyệt được vì `isBigBoss`.

## Root cause
`getKeysChanged` (FirmSupportAccountingDepartment.blade.php) so `self.month_employee_percent` với
`self.regulation.employee_percent`. Nhưng dòng 19 gán `this.regulation = details.find(type===1)` — dòng
detail chỉ có cột `month_employee_percent/month_part_lead_percent/month_department_lead_percent`, KHÔNG có
`employee_percent/part_percent/department_percent` → so với `undefined` → `Number(x) != NaN` luôn true →
`keyChanged=true` → chặn người không phải BGD.

Kiểm chứng DB (HĐ 20479): department 24259, regulation_id=480, details type=1/2 đều = 1/2/88/0/12,
khớp 100% quy chế 480 ⇒ đúng ra `keyChanged=false`.

## Task
- [x] Sửa `getKeysChanged`: lấy `self.regulation[value]`, fallback `self.regulation[key]` khi undefined/null
- [x] Bỏ `console.log(this.regulation)` thừa (dòng 20)
- [x] Sanity: không phá trường hợp đề xuất lệch quy chế thật (vẫn true)

## Kiểm thử thủ công (chờ user)
- [ ] Đông duyệt HĐ 20479 → không còn toast "Vui lòng chuyển duyệt...", duyệt thành công
- [ ] HĐ có đề xuất lệch quy chế thật + người không phải BGD → vẫn báo cần chuyển duyệt

## Ảnh hưởng
Hàm dùng chung — include bởi nhiều màn (firm contracts/orders/annexes/principle, insurance).
Fix làm so sánh đúng theo cả 2 schema (quy chế / detail), không đổi hành vi khi dữ liệu lệch thật.

### Checkpoint — 2026-06-09
Vừa hoàn thành: khảo sát root cause (DB + FE), được duyệt sửa
Đang làm dở: áp dụng edit getKeysChanged
Bước tiếp theo: sửa file blade
Blocked:
