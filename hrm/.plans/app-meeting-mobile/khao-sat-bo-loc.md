# Khảo sát bộ lọc — app mobile (26/10/2026)

Mục tiêu: thiết kế lại MỘT mẫu bộ lọc dùng chung cho toàn bộ app (TPE_APP + bản thiết kế meeting-mobile.pen).

## A. App thật TPE_APP (Flutter)

Widget chung: `lib/custom_view/filter_view.dart` → `FilterView` (dòng 414) = `Drawer` mở từ PHẢI (endDrawer).
- Header navy `#193463` "Bộ lọc" + dòng phụ "N bộ lọc đang áp dụng" (`#FFBC74`, chỉ khi truyền `activeCount`) + nút X.
- Footer 2 nút: Làm mới (viền cam `#E77D00`) · Áp dụng (nền cam).
- Field: `TextFieldInput`/`TextInput`/`TextFieldInput2` · `CalendarInput`/`DateInput`/`DateTimeInput` (flutter_datetime_picker) ·
  `DropDownInput`/`DropDownInput2` (DropdownButton) · `SelectInput<T>` (DropdownSearch có ô tìm). Field có giá trị → chấm cam 6px cạnh nhãn.
- Cách mở: icon filter trên `PrimaryAppBar` → `openEndDrawer()`; badge = chấm cam 8px (không hiện số).

| Pattern | Số màn | Ghi chú |
|---|---|---|
| A. endDrawer `FilterView` | 26 | A1 có `activeCount` ~17 (đào tạo, thi, thanh toán…) · A2 chỉ chấm `isShow` tự tính 7 (nhóm `danh_sach_*` BLoC) · A3 không chỉ báo 2 (suất ăn) |
| B. Trang lọc đẩy lên (bespoke) | 1 | Task (`task_filter_modal.dart`, icon `tune`, cam `#FF7A00`, ô tìm inline + chip quá hạn). `SearchFilterPage` = code chết |
| C. Chỉ ô tìm inline, lọc cục bộ | ~5 | chọn phòng ban / NV / điểm đi, phiếu yêu cầu, duyệt giao CT |
| D. Chip/Tab làm bộ lọc | 0 | không màn danh sách nào dùng; không có bottom sheet lọc |
| E. Chọn tháng | riêng | month_picker suất ăn, dashboard — không qua FilterView |

Vấn đề:
1. Chỉ báo "đang lọc" 3 kiểu (số / chấm / không); sau Áp dụng không thấy đang lọc theo gì (không chip).
2. `isShow`/`activeCount` chép tay từng màn (vd ds_khoa_hoc:205 nối 8 `ref.watch`) → dễ lệch với field thật.
3. Ngày có 4 kiểu render; khoảng ngày tách 2 ô Từ/Đến, nhãn lúc "X: Từ" lúc "Từ ngày".
4. Enum nhỏ (Trạng thái, Hình thức) lúc dropdown thường lúc dropdown-có-tìm; widget trùng đôi (…Input / …Input2).
5. Ô tìm keyword ở `danh_sach_*` bị comment, dời vào drawer thành "Mã phiếu" → chưa có quy ước tìm ở ngoài hay trong.
6. Làm mới: màn chỉ xoá state local, màn gửi event bloc; đóng drawer tuỳ màn.
7. Màu lệch: navy `#193463` vs `#1E3B82`, cam `#E77D00` vs `#FF7A00`; suất ăn tự dựng AppBar.
8. Bộ Công ty / Phòng ban / Nhóm NV / NV lặp gần nguyên khối ở 6 màn HR → ứng viên "preset".

## B. Bản thiết kế meeting-mobile.pen (+ mytodo.pen)

| Màn | Kiểu |
|---|---|
| 01 Lịch meeting | ô tìm + nút ⚙ cạnh ô; tab Tôi chủ trì / Tôi tham gia; 3 thẻ số liệu kiêm chip lọc nhanh |
| 02 Bộ lọc | màn toàn trang (✕ · "Bộ lọc" · Làm mới), 8 dropdown xếp dọc + Ngày từ/đến 2 ô, footer Làm mới / Áp dụng (2) |
| 41 Chọn KH | ô tìm + 2 ô MST / SĐT inline, icon lọc trên header |
| 14 Chọn nhân sự | ô tìm + hàng chip phòng ban (Tất cả (24)) |
| 48 Chọn dự án TKT | ô tìm + dải thông báo phạm vi lọc cố định + chip đã chọn |
| 00j Thông báo | gạt Tất cả/Chưa đọc + chip phân hệ có số đếm, cuộn ngang |
| mytodo B3 | 2 dropdown (Loại chọn-một, Trạng thái khoá tới khi chọn 1 loại) |

Vấn đề: 4–5 kiểu lọc khác nhau ngay trong bộ thiết kế; nút lọc lúc cạnh ô tìm lúc trên header; màn 02 = full page
trong khi app thật = drawer phải; chưa vẽ trạng thái "đang lọc" ngoài danh sách (biến thể 01 bật chip còn nằm ở "Chưa vẽ").

> ⚠️ Mục A khảo sát trên TPE_APP develop eec2f00 (trước khi pull 26/10). Bản 331f51b: ngăn lọc nền trắng + nút theo màu phân hệ, ô tìm đặt cạnh nút lọc; Task vẫn trang lọc riêng; Khoá học có ô "Lọc danh sách" cạnh nút lọc.
