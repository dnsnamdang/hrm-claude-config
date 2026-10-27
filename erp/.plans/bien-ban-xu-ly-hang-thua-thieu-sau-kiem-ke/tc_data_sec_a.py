# -*- coding: utf-8 -*-
"""Section I, II, III - hien thi & loi vao, bo loc, danh sach."""
from tc_data_role import MENU

SEC_I = [
    ("001", "Vào màn từ menu Kế toán", "P0",
     "KT-1 có quyền Kế toán kho, đã lập ít nhất 1 biên bản",
     "1. " + MENU + "\n"
     "2. Quan sát tiêu đề và bảng",
     "—",
     "- Tiêu đề trang \"Biên bản xử lý hàng thừa, thiếu sau kiểm kê\"\n"
     "- Bảng tải dữ liệu, không báo lỗi"),

    ("002", "Bố cục mặc định của màn danh sách", "P0",
     "KT-1 đã lập 12 biên bản",
     "1. Mở màn từ menu\n"
     "2. Quan sát từ trên xuống",
     "—",
     "- Hàng nút: Bộ lọc, Tạo mới, In, Xuất excel\n"
     "- Bảng có cột: STT, Số phiếu, Ngày lập, Kho, Hàng thừa, Hàng thiếu, Người lập, Người duyệt, Ngày "
     "duyệt, Trạng thái, Hành động\n"
     "- 10 dòng mỗi trang, biên bản mới lập nhất lên đầu"),

    ("003", "Mục menu bị lặp", "P2",
     "—",
     "1. Mở menu Kế toán > mục \"Kiểm kê\" > cột \"Theo vị trí\"",
     "—",
     "- Mong đợi: mục \"Biên bản xử lý hàng thừa, thiếu sau kiểm kê\" hiện 1 lần\n"
     "- Lưu ý: theo code hiện tại mục này hiện 2 lần liền nhau - ghi Failed"),

    ("004", "Màn không có ở menu Kho", "P2",
     "—",
     "1. Mở menu Kho > nhóm \"Kiểm kho\", đọc các mục",
     "—",
     "- Không có mục Biên bản xử lý hàng thừa, thiếu; chỉ vào được từ menu Kế toán"),

    ("005", "Nhãn trạng thái hiển thị đúng màu", "P1",
     "KT-1 có biên bản ở cả 3 trạng thái Đang tạo, Chờ duyệt, Đã duyệt",
     "1. Mở màn từ menu, quan sát cột Trạng thái",
     "—",
     "- Đã duyệt: nhãn xanh\n"
     "- Đang tạo, Chờ duyệt: nhãn đỏ"),

    ("006", "Bấm Số phiếu mở màn Chi tiết", "P0",
     "BB-2 Chờ duyệt do KT-1 lập; KT-1 không có quyền duyệt",
     "1. Bấm Số phiếu BB-2",
     "—",
     "- Tiêu đề \"Biên bản xử lý hàng sau kiểm kê hàng hóa BBXLKKHH-...\"\n"
     "- Mọi ô bị khóa, không có nút Lấy dữ liệu, không có ô thêm file\n"
     "- Cuối trang chỉ có nút Quay lại"),

    ("007", "Bấm Tạo mới mở form trống", "P0",
     "KT-1 có quyền Kế toán kho",
     "1. Bấm Tạo mới",
     "—",
     "- Từ ngày, Đến ngày, Kho vật lý trống; khung Phiếu kiểm kê trống\n"
     "- Tab Hàng thừa và Hàng thiếu đều ghi \"Không có dữ liệu\"\n"
     "- Nút Lưu, Lưu và gửi duyệt bị mờ; có nút Hủy"),

    ("008", "Hủy ở màn Tạo mới", "P2",
     "Đang ở form Tạo mới, đã chọn kho và lấy dữ liệu",
     "1. Bấm Hủy",
     "—",
     "- Về màn danh sách, không có biên bản mới"),
]


SEC_II = [
    ("001", "Khối tìm kiếm đủ các ô lọc", "P0",
     "—",
     "1. Bấm Bộ lọc",
     "—",
     "- Có ô: Mã phiếu, Kho, Trạng thái (3 lựa chọn Đang tạo, Chờ duyệt, Đã duyệt), Người tạo, Người duyệt\n"
     "- Không có ô Từ ngày / Đến ngày, không có ô Công ty, Phòng ban"),

    ("002", "Lọc theo Mã phiếu tìm gần đúng", "P0",
     "KT-1 có BBXLKKHH-00007 và BBXLKKHH-00008",
     "1. Nhập \"00007\" vào ô Mã phiếu",
     "Mã phiếu: 00007",
     "- Chỉ hiện BBXLKKHH-00007"),

    ("003", "Lọc theo Trạng thái", "P0",
     "KT-1 có 2 biên bản Đang tạo, 3 Chờ duyệt, 1 Đã duyệt",
     "1. Chọn Trạng thái \"Chờ duyệt\"\n"
     "2. Đổi sang \"Đã duyệt\"",
     "—",
     "- Bước 1: đúng 3 biên bản\n"
     "- Bước 2: đúng 1 biên bản"),

    ("004", "Lọc theo Kho", "P1",
     "KT-1 có BB-5 kho K1, BB-6 kho K2",
     "1. Chọn Kho \"K1\"",
     "Kho: K1",
     "- Mong đợi: hiện BB-5, không hiện BB-6\n"
     "- Lưu ý: theo code hiện tại vẫn hiện cả hai - ghi Failed"),

    ("005", "Lọc theo Người duyệt", "P1",
     "KT-1 có BB-3 do DUYET-1 duyệt, BB-4 do DUYET-2 duyệt",
     "1. Chọn Người duyệt DUYET-1",
     "—",
     "- Mong đợi: chỉ hiện BB-3\n"
     "- Lưu ý: theo code hiện tại vẫn hiện cả hai - ghi Failed"),

    ("006", "Lọc theo Người tạo", "P2",
     "KT-1 đăng nhập",
     "1. Chọn Người tạo KT-2\n"
     "2. Chọn Người tạo KT-1",
     "—",
     "- Bước 1: bảng trống (lối vào menu chỉ có biên bản của mình)\n"
     "- Bước 2: hiện đủ biên bản của KT-1"),

    ("007", "Kết hợp nhiều ô lọc", "P1",
     "—",
     "1. Nhập Mã phiếu \"0000\", chọn Trạng thái Chờ duyệt",
     "—",
     "- Chỉ hiện biên bản thỏa cả 2 điều kiện"),

    ("008", "Xóa bộ lọc", "P2",
     "Đang lọc Trạng thái Đã duyệt",
     "1. Bấm nút xóa bộ lọc",
     "—",
     "- Các ô trở về trống, số tổng như lúc mới vào"),

    ("009", "Không có kết quả", "P2",
     "—",
     "1. Nhập Mã phiếu \"KHONGTONTAI\"",
     "—",
     "- Bảng báo không có dữ liệu, tổng = 0"),
]


SEC_III = [
    ("001", "Phân trang và STT liên tục", "P1",
     "KT-1 có 25 biên bản",
     "1. Chuyển sang trang 3",
     "—",
     "- STT từ 21 đến 25, dòng dưới bảng \"Hiển thị 21 đến 25 của 25\""),

    ("002", "Sắp xếp theo Số phiếu", "P2",
     "Có ít nhất 5 biên bản",
     "1. Bấm tiêu đề cột Số phiếu 2 lần",
     "—",
     "- Lần 1 tăng dần, lần 2 giảm dần\n"
     "- Các cột khác không sắp xếp được"),

    ("003", "Menu bánh răng theo trạng thái", "P0",
     "KT-1 có quyền duyệt; BB-1 Đang tạo, BB-2 Chờ duyệt, BB-3 Đã duyệt đều do KT-1 lập",
     "1. Bấm bánh răng ở từng biên bản",
     "—",
     "- BB-1: Sửa, In, Xuất Excel\n"
     "- BB-2: Duyệt, In, Xuất Excel\n"
     "- BB-3: In, Xuất Excel\n"
     "- Không dòng nào có Xóa"),

    ("004", "Cột Hàng thừa, Hàng thiếu là tổng số lượng", "P0",
     "BB-5 gồm H1 thừa 3, H2 thiếu 2, H3 thiếu 1",
     "1. Đọc cột Hàng thừa, Hàng thiếu của BB-5",
     "—",
     "- Hàng thừa: 3\n"
     "- Hàng thiếu: 3"),

    ("005", "Cột Người duyệt, Ngày duyệt sau khi duyệt", "P0",
     "BB-2 vừa được DUYET-1 duyệt hôm nay",
     "1. KT-1 tìm BB-2, đọc cột Người duyệt, Ngày duyệt, Trạng thái",
     "—",
     "- Người duyệt: DUYET-1\n"
     "- Ngày duyệt: hôm nay\n"
     "- Trạng thái: Đã duyệt (nhãn xanh)"),

    ("006", "Định dạng Số phiếu và Ngày lập", "P1",
     "KT-1 vừa lưu biên bản đầu tiên trong ngày 22/10",
     "1. Đọc dòng đầu bảng",
     "—",
     "- Số phiếu dạng BBXLKKHH-xxxxx (5 chữ số, không có mã công ty)\n"
     "- Ngày lập 22/10/2026"),
]
