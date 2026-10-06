# #11566 — [ERP => HRM] FB: Người tạo/cập nhật + thứ tự cột + mã tối đa 50
@namdangit · nhánh `gop_db` · Redmine http://quanly.dnsmedia.vn/issues/11566

## Yêu cầu (nguyên văn task)
1. Trường người tạo/người sửa/người cập nhật trên tất cả màn danh sách để định dạng Tên NV_Mã phòng.
2. Danh sách KHÔNG có tuỳ chỉnh cột: cột Người tạo/Ngày tạo đứng trước Người sửa(cập nhật)/Ngày sửa(cập nhật).
3. Mã chưa có giới hạn ký tự thì mặc định max 50.

## Quyết định đã chốt (03/10/2026)
- Định dạng hiển thị: `Tên NV - Mã phòng` (ngăn cách ` - `, không dùng `_`). Thiếu phần nào bỏ phần đó.
- BE sửa THẲNG accessor `BaseModel::employee_create_name / employee_update_name` (+ bản `...HasTime`) → ảnh hưởng cả màn cũ, user đồng ý. Helper mới `employeeAuditLabel()` trong `app/Helper/FormatHelper.php`. Resource của màn mới tự ghép `fullname` → chuyển sang helper.
- Phạm vi màn: màn mới (có `<V2Base*>`) theo skill `new-screens-sweep`; vùng xám: popup chọn phiếu CÓ, bảng con trong form KHÔNG.
- Mã max 50: chỉ ô mã user tự nhập, FE (`max:50`) + BE (`max:50` FormRequest), chỉ nơi chưa có giới hạn.
