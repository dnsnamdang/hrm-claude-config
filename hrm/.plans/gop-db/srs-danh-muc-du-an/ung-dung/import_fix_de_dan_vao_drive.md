# Sửa mục 2.11 Import Excel — SRS Danh mục ứng dụng (bản trên Drive)

Bản trên Drive đã được sửa tay nên KHÔNG ghi đè bằng generator. Người viết tự dán các đoạn dưới đây
vào đúng chỗ trong mục **2.11 Import Excel**. Nội dung khớp với `ung-dung/gen_srs.py` (bản local).

## Vì sao phải sửa 2 câu đang có trên Drive

1. **“Có dòng lỗi → bỏ các dòng lỗi và import, thông báo ‘Import thành công x/y ứng dụng. z ứng dụng thất bại.’”** — SAI so với màn thật:
   - Còn dòng lỗi thì nút **Import bị khóa**, không bấm được (`V2BaseImportToolbar.vue`: Import chỉ mở khi
     đã Validate **và** số dòng lỗi = 0 **và** có ≥ 1 dòng hợp lệ). Hệ thống không tự bỏ dòng lỗi rồi import.
   - Muốn import phần hợp lệ, người dùng phải **tự bấm “Bỏ dòng lỗi”** (dưới bảng xem trước) trước, rồi mới bấm Import.
   - Câu “Import thành công x/y ứng dụng. z ứng dụng thất bại.” chỉ xuất hiện khi **dữ liệu thay đổi giữa
     lúc Validate và lúc Import** (vd người khác vừa tạo ứng dụng trùng tên) — máy chủ kiểm tra lại và loại
     bớt dòng. Luồng bình thường sẽ luôn ra “Import thành công <n> ứng dụng”.
2. **“Mọi dòng đều lỗi → Nút import không cho chọn”** — đúng ý, chỉ cần viết rõ hơn: sau khi bỏ dòng lỗi
   bảng không còn dòng nào nên nút Import vẫn khóa.

Câu thông báo lấy nguyên văn từ `pages/assign/application/index.vue` → `handleImportApplications()`
(và thông báo lỗi “Import thất bại” từ `ApplicationsController::import()` ở máy chủ);
câu “Bỏ dòng lỗi” từ `components/V2BaseImportModal.vue` → `handleRemoveInvalid()`.

---

## 1. Dòng sự kiện chính (thay nguyên ô)

1. Người dùng bấm Import Excel.
2. (Tuỳ chọn) Bấm “Tải file mẫu” để lấy tệp Mau_Import_UngDung_FN.xlsx.
3. Bấm “Chọn file Excel”, chọn tệp đã điền dữ liệu.
4. Bấm “Load lên bảng” để đọc tệp ra bảng xem trước.
5. Bấm “Validate” → hệ thống kiểm tra từng dòng, đánh dấu dòng hợp lệ / lỗi kèm lý do; dòng hợp lệ bị khóa không sửa được.
6. Nếu còn dòng lỗi: sửa trực tiếp các dòng lỗi rồi Validate lại, hoặc bấm “Bỏ dòng lỗi” để loại các dòng lỗi khỏi bảng.
7. Khi đã Validate và không còn dòng lỗi, nút Import mới bấm được. Bấm “Import” → hệ thống ghi các dòng, thông báo “Import thành công <n> ứng dụng”, đóng cửa sổ và nạp lại danh sách.

## 2. Dòng sự kiện phụ (thay nguyên ô)

• Chưa Validate, hoặc còn dòng lỗi → nút Import bị khóa, không bấm được.
• Mọi dòng đều lỗi → sau khi bỏ dòng lỗi bảng không còn dòng nào, nút Import vẫn khóa; không import được.
• Bấm “Bỏ dòng lỗi” → “Đã bỏ x dòng lỗi. Còn lại y dòng hợp lệ.”
• Bấm “Xoá trạng thái validate” → bỏ đánh dấu, mở khóa các dòng để sửa; phải Validate lại.
• Dữ liệu thay đổi giữa lúc Validate và Import (vd người khác vừa tạo ứng dụng trùng tên): còn ghi được một phần → “Import thành công x/y ứng dụng. z ứng dụng thất bại.”, đóng cửa sổ; không ghi được dòng nào → báo lỗi “Import thất bại”, cửa sổ giữ nguyên.
• Tệp quá 500 dòng → “Mỗi lần import tối đa 500 dòng (file đang có N dòng), vui lòng tách file và import nhiều lần.”
• Bật “Chỉ dòng lỗi” để lọc bảng xem trước chỉ còn dòng lỗi.
• Bấm Làm mới → xóa dữ liệu đã nạp để chọn tệp khác.

## 3. Bảng Mô tả chi tiết giao diện (mục 2.11.4)

Sửa dòng **Nút Import**, và chèn 2 dòng mới ngay sau nó. Thứ tự cột như bảng hiện có:
Tên trường · Kiểu · Trạng thái · Định dạng / Giá trị · Bắt buộc · Giá trị ban đầu · Mô tả.

| Tên trường | Kiểu | Trạng thái | Định dạng | Bắt buộc | Giá trị ban đầu | Mô tả |
|---|---|---|---|---|---|---|
| Nút Import | Button | Enable / Disable | – | – | Disable | Chỉ bấm được khi đã Validate và không còn dòng lỗi. |
| Nút Bỏ dòng lỗi | Button | Enable / Disable | – | – | Disable khi chưa có dữ liệu | Loại các dòng lỗi khỏi bảng xem trước. |
| Nút Xoá trạng thái validate | Button | Enable / Disable | – | – | Disable khi chưa có dữ liệu | Bỏ kết quả Validate để sửa lại dữ liệu. |

## 4. Bảng event (mục 2.11.5)

### Event “Bấm Import” — Click (thay nguyên ô xử lý)

Before:
– Kiểm tra quyền Q1.
– (giữ nguyên câu báo thiếu quyền đang có)
– Nút chỉ bấm được khi đã Validate và không còn dòng lỗi.
During:
– Chỉ gửi các dòng hợp lệ trên bảng xem trước.
– Máy chủ kiểm tra lại các dòng gửi lên như bước Validate.
After:
– Mã chưa có → thêm mới (mã chuyển chữ in hoa), ghi lịch sử “Tạo mới”.
– Mã đã có → cập nhật tên, mô tả, trạng thái và thay toàn bộ các cặp theo tệp, ghi lịch sử các trường đã đổi.
– Tất cả các dòng ghi được → thông báo “Import thành công <n> ứng dụng”, đóng cửa sổ, nạp lại danh sách.
– Chỉ ghi được một phần (dữ liệu thay đổi giữa lúc Validate và Import, vd người khác vừa tạo ứng dụng trùng tên) → thông báo “Import thành công x/y ứng dụng. z ứng dụng thất bại.”, đóng cửa sổ, nạp lại danh sách.
– Không ghi được dòng nào → báo lỗi “Import thất bại”; cửa sổ giữ nguyên, không ghi dữ liệu.

### Event MỚI “Bấm Bỏ dòng lỗi” — Click (chèn ngay sau event Bấm Import)

Before:
– Chưa Validate → “Hãy Validate trước rồi mới bỏ dòng lỗi.” và dừng xử lý.
After:
– Loại các dòng lỗi khỏi bảng xem trước; thông báo “Đã bỏ x dòng lỗi. Còn lại y dòng hợp lệ.”
– Còn ≥ 1 dòng hợp lệ → nút Import mở cho bấm.
