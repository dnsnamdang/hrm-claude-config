# #10769 — [App] Phiếu giao công tác: thiếu bộ lọc — @cuong61n

- [x] Kiểm 19/10/2026: bộ lọc ĐÃ CÓ từ 07/08/2026 (TPE_APP 602ef9f) — đủ 13 ô như web `/assign/assign_business?type=all` (Công ty, Phòng ban, Phiếu công tác, Loại công tác, Phiếu đề xuất công tác, Phiếu việc cần giao, Phiếu đề xuất công việc, Số hợp đồng, Khách hàng, Trạng thái, Nhân viên, Từ ngày, Đến ngày) + Bộ phận
- [x] Lỗi phát hiện khi test: gõ ký tự đầu vào ô lọc chữ → bàn phím đóng, mất focus. Nguyên nhân `TextInput`/`TextFieldInput` (custom_view/filter_view.dart) đổi suffix null ↔ nút ✕ → `CommonTextField` đổi cấu trúc (TextField trần ↔ Row) → TextField dựng lại. User duyệt sửa TextInput: giữ chỗ `SizedBox(18)` khi trống. Ảnh hưởng mọi bộ lọc chữ dùng TextInput (13 màn)
- [x] `TextInput` mặc định `maxLines = 1` (trước null → nhiều dòng, bấm "Nhập" chèn xuống dòng vào giá trị lọc). Chỉ ô Lý do huỷ phiếu cơm tự truyền maxLines 8
- [x] Test simulator: gõ liền "TEST" giữ bàn phím ✓; "Nhập" đóng bàn phím, không xuống dòng ✓; Áp dụng → `code=TEST` 2 phiếu ✓; thêm Loại công tác kỹ thuật → `business_type=1` 1 phiếu ✓; Làm mới → về mặc định ✓
