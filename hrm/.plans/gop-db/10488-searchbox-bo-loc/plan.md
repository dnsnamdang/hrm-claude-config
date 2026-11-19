# #10488 — [App Đào tạo + QL cơm] Combobox bộ lọc không có ô tìm kiếm — @cuong61n (Redmine đang giao Nguyễn Văn Tú)

Hiện trạng 19/10/2026: commit 05f82a3 (TuJobs 27/05/2026) đã đổi các combobox lấy từ dữ liệu (Công ty/Phòng ban/Nhân viên bên cơm; Khoá học/Loại đào tạo/Giảng viên/Người phụ trách bên đào tạo) sang `SelectInput` (có ô tìm kiếm). CÒN SÓT các combobox danh sách cố định:
- QL cơm: "Loại phiếu" ở bộ lọc phiếu ĐK dài ngày (`DropDownInput2`)
- Đào tạo: 16 ô `DropDownInput` (Hình thức học, Nền tảng học, trạng thái…) ở 11 màn bộ lọc

- [x] `long_term_right_menu.dart`: "Loại phiếu" → `SelectInput`
- [x] `custom_view/filter_view.dart` `DropDownInput`: vẽ bằng `SelectInput` (nhãn lấy từ `Text` của item), giữ nguyên tham số → 16 ô đào tạo có ô tìm kiếm, không sửa từng màn. `DropDownInput` chỉ dùng trong các bộ lọc đào tạo
- [x] Test simulator: Khoá học đã tham gia → Hình thức học có "Tìm kiếm", gõ "Off" lọc còn 2, chọn Offline → `platform=2` ✓; QL cơm → Loại phiếu có "Tìm kiếm", chọn khách dài ngày → `register_rice_type=3`, danh sách đúng loại ✓
- Không đổi: `DropDownInput2` ở form tạo phiếu / đặt cơm (không phải bộ lọc)
