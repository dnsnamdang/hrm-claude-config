# Luồng Import Excel CHUẨN cho SRS (chốt với user 2026-09-24)

Mọi màn dùng `components/V2BaseImportModal.vue` + `V2BaseImportToolbar.vue` + `V2BaseImportTable.vue`
chạy ĐÚNG luồng dưới đây. SRS phải mô tả theo cái NGƯỜI DÙNG thấy (nút nào bấm được lúc nào),
không mô tả theo mã phản hồi máy chủ.

## Sự thật từ code
- Nút **Import** chỉ bấm được khi: đã Validate **VÀ** không còn dòng lỗi **VÀ** có ≥ 1 dòng hợp lệ
  (`V2BaseImportToolbar.vue`: `hasValidatedRows && invalidCount === 0 && validCount > 0`).
- Nút **Bỏ dòng lỗi** (dưới bảng xem trước): loại các dòng lỗi khỏi bảng, báo
  “Đã bỏ x dòng lỗi. Còn lại y dòng hợp lệ.”; chưa Validate mà bấm → “Hãy Validate trước rồi mới bỏ dòng lỗi.”
- Nút **Xoá trạng thái validate**: bỏ đánh dấu hợp lệ/lỗi, mở khoá mọi dòng để sửa, phải Validate lại.
- Bấm Import chỉ gửi các dòng hợp lệ. Máy chủ kiểm tra lại; chỉ khi dữ liệu thay đổi giữa lúc Validate
  và Import (vd người khác vừa tạo bản ghi trùng mã) mới có kết quả một phần / thất bại.

## Khuôn chữ (thay <đối tượng> và câu thông báo bằng đúng chữ trong handler của màn)

**Dòng sự kiện chính**
1. Người dùng bấm Import Excel.
2. (Tuỳ chọn) Bấm “Tải file mẫu” để lấy tệp mẫu.
3. Bấm “Chọn file Excel”, chọn tệp đã điền dữ liệu.
4. Bấm “Load lên bảng” để đọc tệp ra bảng xem trước.
5. Bấm “Validate” → hệ thống kiểm tra từng dòng, đánh dấu dòng hợp lệ / lỗi kèm lý do; dòng hợp lệ bị khóa không sửa được.
6. Nếu còn dòng lỗi: sửa trực tiếp các dòng lỗi rồi Validate lại, hoặc bấm “Bỏ dòng lỗi” để loại các dòng lỗi khỏi bảng.
7. Khi đã Validate và không còn dòng lỗi, nút Import mới bấm được. Bấm “Import” → hệ thống ghi các dòng, thông báo “<câu thành công>”, đóng cửa sổ và nạp lại danh sách.

**Dòng sự kiện phụ**
- Chưa Validate, hoặc còn dòng lỗi → nút Import bị khóa, không bấm được.
- Mọi dòng đều lỗi → sau khi bỏ dòng lỗi bảng không còn dòng nào, nút Import vẫn khóa; không import được.
- Bấm “Bỏ dòng lỗi” → “Đã bỏ x dòng lỗi. Còn lại y dòng hợp lệ.”
- Bấm “Xoá trạng thái validate” → bỏ đánh dấu, mở khóa các dòng để sửa; phải Validate lại.
- Dữ liệu thay đổi giữa lúc Validate và Import (vd người khác vừa tạo bản ghi trùng mã): còn ghi được một phần → “<câu một phần>”, đóng cửa sổ; không ghi được dòng nào → báo lỗi ngay trong cửa sổ, cửa sổ giữ nguyên.
- (giữ các nhánh riêng của màn: quá 500 dòng, Chỉ dòng lỗi, Làm mới…)

**Bảng giao diện** — nút Import: Trạng thái `Enable / Disable`, Giá trị ban đầu `Disable`, Mô tả
“Chỉ bấm được khi đã Validate và không còn dòng lỗi.”. Thêm 2 dòng:
- `Nút Bỏ dòng lỗi` · Button · Enable / Disable · Disable khi chưa có dữ liệu · … · “Loại các dòng lỗi khỏi bảng xem trước.”
- `Nút Xoá trạng thái validate` · Button · Enable / Disable · Disable khi chưa có dữ liệu · … · “Bỏ kết quả Validate để sửa lại dữ liệu.”

**Bảng event**
- Thêm event “Bấm Bỏ dòng lỗi” (Click): Before: chưa Validate → “Hãy Validate trước rồi mới bỏ dòng lỗi.”
  After: loại các dòng lỗi khỏi bảng; thông báo “Đã bỏ x dòng lỗi. Còn lại y dòng hợp lệ.”; nút Import mở nếu còn ≥ 1 dòng.
- Event “Bấm Import”: Before thêm “– Nút chỉ bấm được khi đã Validate và không còn dòng lỗi.”;
  During “– Máy chủ kiểm tra lại các dòng gửi lên như bước Validate.”; After viết theo 3 kết quả:
  tất cả thành công / một phần (dữ liệu thay đổi giữa 2 bước) / không dòng nào (báo lỗi trong cửa sổ, cửa sổ giữ nguyên).
