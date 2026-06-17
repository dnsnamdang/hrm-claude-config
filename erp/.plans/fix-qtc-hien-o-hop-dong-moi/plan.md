# Fix — Hợp đồng mới hiện sẵn Nhân viên/Phòng QTC

## Triệu chứng
Lập HĐ mới (`admin/sale/firm-contracts/create`) đã thấy "Nhân viên QTC" (và hiển thị "Phòng QTC") có giá trị, dù là HĐ mới chưa quyết toán công.

## Root cause
`resources/views/sale/firm/contracts/form.blade.php:325` — `ng-selected` của option "Nhân viên QTC" dùng **phép gán** `form.employee_qtc_id = e.id` thay vì **so sánh** `==`. Khi Angular render `ng-repeat` các option, biểu thức gán này set `form.employee_qtc_id` = id nhân viên (option cuối được đánh giá) → HĐ mới bị set sẵn NV QTC, và sẽ LƯU SAI vào `employee_qtc_id` nếu submit.

Đối chiếu: dòng Phòng QTC (313) cùng file dùng `==` đúng; 2 form khác (addition_annexes, warranty_repair_contracts) đều `==` đúng → đây là typo cô lập 1 dòng. "Phòng QTC = BAN ĐIỀU HÀNH" chỉ là option đầu select hiển thị khi `department_qtc_id` null (không phải dữ liệu lưu).

## Kết luận về logic lưu QTC (HRM → ERP)
Logic `syncEmployeeQtcContractErp` (HRM) ghi `employee_qtc_id`/`department_qtc_id` về HĐ khi quyết toán công — KHÔNG liên quan triệu chứng này. HĐ mới có `employee_qtc_id` null trong DB; lỗi hiển thị/ghi sai hoàn toàn do typo FE. Sau fix, HĐ mới hiển thị trống đúng.

## Fix
- [x] `form.blade.php:325`: `form.employee_qtc_id = e.id` → `form.employee_qtc_id == e.id`

## Kiểm thử (user)
- [ ] Mở lập HĐ mới → Nhân viên QTC trống (không auto chọn)
- [ ] HĐ đã quyết toán công → vẫn hiện đúng NV/Phòng QTC đã lưu
- [ ] Lưu HĐ mới → DB `employee_qtc_id` null (không bị set bừa)

### Checkpoint — 2026-06-09
Vừa hoàn thành: fix typo ng-selected dòng 325
Bước tiếp theo: user kiểm thử lập HĐ mới
Blocked:
