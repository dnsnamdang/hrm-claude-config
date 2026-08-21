# Design — Cho phép khóa/mở khóa danh mục dự án dù đã được sử dụng

## Mục tiêu
Các màn danh mục trong phân hệ Giao việc (Giai đoạn dự án, Loại meeting, Loại tài liệu) hiện chặn
khóa/mở khóa khi bản ghi đã được dùng ở chỗ khác. Yêu cầu: cho phép khóa/mở khóa tự do, **vẫn giữ chặn Xóa**.

## Quyết định chính
- Chuẩn hóa `isCanLockUpdate()` của 3 model về pattern `status == STATUS_ACTIVE` (giống `ProjectItem`,
  `ReasonProjectFailure` vốn đã đúng). Guard này chỉ chống khóa trùng, không còn ràng buộc "đã sử dụng".
- FE bỏ điều kiện `:disabled` theo usage trên nút khóa/mở khóa; nút luôn bấm được, title đổi theo trạng thái.
- KHÔNG đụng `isCanDelete` / checkbox / edit → Xóa vẫn bị chặn khi có dữ liệu liên kết.

## Tham chiếu pattern
Tương tự feature `banks-lock-used-catalog` (đã làm trước đó cho danh mục ngân hàng).

## Downstream
Không ảnh hưởng dữ liệu; chỉ nới lỏng điều kiện thao tác khóa. Endpoint lock/unlock giữ nguyên middleware quyền
`Quản lý danh mục ...`.
