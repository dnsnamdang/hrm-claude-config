# Sửa mục 2.10 Import Excel — SRS Danh mục nhóm ngành (bản trên Drive đã sửa tay, dán thủ công)

Lý do: nút Import chỉ bấm được khi đã Validate VÀ không còn dòng lỗi. Còn dòng lỗi thì người dùng phải
sửa rồi Validate lại, hoặc bấm “Bỏ dòng lỗi”. Thông báo “x/y … thất bại” chỉ xuất hiện khi dữ liệu thay
đổi giữa lúc Validate và Import.

## 2.10.2 Giới thiệu — ô “Dòng sự kiện chính” (thay bước 6, 7)
6. Nếu còn dòng lỗi: sửa trực tiếp các dòng lỗi rồi Validate lại, hoặc bấm “Bỏ dòng lỗi” để loại các dòng lỗi khỏi bảng.
7. Khi đã Validate và không còn dòng lỗi, nút Import mới bấm được. Bấm “Import” → hệ thống thêm các dòng, thông báo “Import thành công <n> nhóm ngành”, đóng cửa sổ và nạp lại danh sách.

## Ô “Dòng sự kiện phụ” (thay 2 gạch đầu dòng đầu tiên, giữ các dòng 500 dòng / Chỉ dòng lỗi / Làm mới)
• Chưa Validate, hoặc còn dòng lỗi → nút Import bị khóa, không bấm được.
• Mọi dòng đều lỗi → sau khi bỏ dòng lỗi bảng không còn dòng nào, nút Import vẫn khóa; không import được.
• Bấm “Bỏ dòng lỗi” → “Đã bỏ x dòng lỗi. Còn lại y dòng hợp lệ.”
• Bấm “Xoá trạng thái validate” → bỏ đánh dấu, mở khóa các dòng để sửa; phải Validate lại.
• Dữ liệu thay đổi giữa lúc Validate và Import (vd người khác vừa tạo nhóm ngành trùng mã): còn ghi được một phần → “Import thành công x/y nhóm ngành. z nhóm ngành thất bại.”, đóng cửa sổ; không ghi được dòng nào → báo lỗi, cửa sổ giữ nguyên.

## 2.10.4 Bảng giao diện
- Dòng “Nút Import”: Trạng thái `Enable / Disable` · Giá trị ban đầu `Disable` · Mô tả “Chỉ bấm được khi đã Validate và không còn dòng lỗi.”
- Thêm dòng: Nút Bỏ dòng lỗi · Button · Enable / Disable · – · – · Disable khi chưa có dữ liệu · Loại các dòng lỗi khỏi bảng xem trước.
- Thêm dòng: Nút Xoá trạng thái validate · Button · Enable / Disable · – · – · Disable khi chưa có dữ liệu · Bỏ kết quả Validate để sửa lại dữ liệu.

## 2.10.5 Bảng event
Thêm event **Bấm Bỏ dòng lỗi** (Click):
Before:
– Chưa Validate → “Hãy Validate trước rồi mới bỏ dòng lỗi.”
After:
– Loại các dòng lỗi khỏi bảng; thông báo “Đã bỏ x dòng lỗi. Còn lại y dòng hợp lệ.”
– Còn ít nhất 1 dòng thì nút Import mở.

Thay nội dung event **Bấm Import**:
Before:
– Nút chỉ bấm được khi đã Validate và không còn dòng lỗi.
– Kiểm tra quyền Q1.
– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng xử lý.
During:
– Máy chủ kiểm tra lại các dòng gửi lên như bước Validate.
After:
– Thêm mới các dòng, mã chuyển sang chữ in hoa; ghi lịch sử “Thêm mới” từng dòng.
– Tất cả thành công → “Import thành công <n> nhóm ngành”, đóng cửa sổ, nạp lại danh sách.
– Dữ liệu thay đổi giữa lúc Validate và Import: còn ghi được một phần → “Import thành công x/y nhóm ngành. z nhóm ngành thất bại.”, đóng cửa sổ, nạp lại danh sách; không ghi được dòng nào → báo lỗi (“Không có dữ liệu hợp lệ để import” hoặc lỗi chi tiết), cửa sổ giữ nguyên.
