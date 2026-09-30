# HSNS — Cho phép xóa file đã upload (CCCD / Hộ chiếu / Bằng cấp)

Người phụ trách: @junfoke · Ngày: 2026-09-23

## Vấn đề
Màn Hồ sơ nhân sự (`/human/employee_info/{id}`) cho upload đính kèm nhưng **không có cách gỡ file ra**:
component dùng chung `components/common/AttachmentGallery.vue` chỉ render thumbnail + mở popup xem trước,
không có nút xóa. Upload nhầm file là phải giữ nguyên.

Ảnh hưởng 3 chỗ trong `EmployeeInfoForm.vue`: Đính kèm CCCD (2 mặt), Đính kèm Hộ chiếu (2 mặt),
file Bằng cấp ở bảng Học vấn.

## Hướng xử lý
- `AttachmentGallery` thêm prop `deletable` (mặc định `false`, không đổi hành vi các chỗ chỉ để xem)
  và emit `remove(index)`. Nút ✕ ở góc trên phải thumbnail, dùng đúng icon/kiểu nút xóa của
  `components/V2BaseFile.vue` để thống nhất toàn hệ thống. `@click.stop` để bấm ✕ không mở popup xem trước.
- `EmployeeInfoForm.vue` xử lý `remove`: splice khỏi `form.id_images` / `form.passport_images`
  (kèm mảng preview tương ứng), bằng cấp thì set `attachments = null`.
- Reset `input[type=file].value` sau mỗi lần upload và sau khi xóa — nếu không, chọn lại đúng file
  vừa xóa sẽ không kích hoạt `@change` (trình duyệt coi là không đổi).

## Quyết định đã chốt
- **Không** dùng popup xác nhận xóa: file mới chỉ nằm trong form, chỉ mất hẳn khi bấm Lưu —
  giống cách `V2BaseFile` đang làm. Xác nhận ở đây sẽ lệch với phần còn lại của hệ thống.
- Giấy khám SK và Ảnh chân dung không đụng tới: giấy khám SK đã dùng `base-upload-file` (có sẵn xóa),
  ảnh chân dung là ảnh đơn, upload đè lên.
