# Design — Bỏ bắt buộc Ngày sinh & SĐT cho giảng viên thuê ngoài

Nguồn: Redmine #11409 (link màn: /training/teachers/add).

## Vấn đề
Màn Danh mục giảng viên đang bắt buộc **Ngày sinh** và **Số điện thoại** cho cả 2 hình thức.
Với **Giảng viên thuê ngoài** (`type = 2`) hai thông tin này không phải lúc nào cũng có.

## Quyết định
- Hai trường chỉ bắt buộc khi `type = 1` (Giảng viên nội bộ) — bám đúng pattern đã có sẵn trong
  cùng form cho Số CCCD / Email / Trình độ (`required_if:type,1` ở BE, `<Required v-if="form.type == 1" />` ở FE).
- Regex số điện thoại vẫn áp dụng khi có nhập; kiểm tra trùng "tên + SĐT" bỏ qua khi SĐT rỗng.
- Cột DB `teachers.birthday` / `teachers.telephone` đang NOT NULL → thêm migration cho nullable.
- Mọi chỗ format ngày sinh phải chặn `Carbon::parse(null)` (nếu không sẽ hiển thị ngày hôm nay):
  `TeacherResource` (list + màn in) và blade export Excel.

## Ngoài phạm vi
Màn Danh mục giám khảo (`ExaminerController`, `ExaminerListResource`) có validate tương tự
nhưng issue không đề cập — giữ nguyên.
