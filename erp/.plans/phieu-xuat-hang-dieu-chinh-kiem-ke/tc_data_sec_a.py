# -*- coding: utf-8 -*-
"""Section I, II, III, IV - hien thi, bo loc, danh sach, lap phieu tu phieu xuat kho."""
from tc_data_role import MENU, MENU_PXK, PKK, GIA, KKT, KT1, TAO

SEC_I = [
    ("001", "Vào màn từ menu Kế toán", "P0",
     KT1 + ", đã lập ít nhất 1 phiếu",
     "1. " + MENU + "\n"
     "2. Quan sát tiêu đề và bảng",
     "—",
     "- Tiêu đề \"Phiếu xuất hàng điều chỉnh kiểm kê\"\n"
     "- Bảng tải dữ liệu, không báo lỗi"),

    ("002", "Bố cục mặc định của màn danh sách", "P0",
     "KT-1 đã lập 12 phiếu",
     "1. Mở màn từ menu\n"
     "2. Quan sát từ trên xuống",
     "—",
     "- Hàng nút: Bộ lọc, Tạo mới, In, Xuất excel\n"
     "- Bảng có cột: STT, Số phiếu, Phiếu xuất kho, Phiếu kiểm kê, Kho, Người lập, Ngày lập, Trạng thái, "
     "Hành động\n"
     "- 10 dòng mỗi trang, phiếu mới lập nhất lên đầu"),

    ("003", "Nhãn trạng thái đúng màu", "P2",
     "Có phiếu Đang tạo và phiếu Đã hạch toán",
     "1. Quan sát cột Trạng thái",
     "—",
     "- Đang tạo: nhãn đỏ\n"
     "- Đã hạch toán: nhãn xanh"),

    ("004", "Bấm Số phiếu mở màn Chi tiết", "P0",
     "PXH-2 Đã hạch toán do KT-1 lập từ PXK-1 (PKK-1), kho K1",
     "1. Bấm Số phiếu PXH-2",
     "—",
     "- Có ô Phiếu xuất kho (liên kết PXK-1), Phiếu kiểm kê (liên kết PKK-1), Kho K1, Thủ kho TK-1, Nhân "
     "viên, Ghi chú, File đính kèm\n"
     "- Bảng chi tiết có thêm cột Đơn giá vốn, Thành tiền vốn; không có cột SL được xuất\n"
     "- Mọi ô bị khóa, không có nút thêm file; cuối trang chỉ có Quay lại"),

    ("005", "Bấm liên kết Phiếu xuất kho ở Chi tiết", "P2",
     "Đang ở Chi tiết PXH-2",
     "1. Bấm PXK-1",
     "—",
     "- Mở Chi tiết PXK-1 ở tab mới"),

    ("006", "Bấm liên kết Phiếu kiểm kê ở Chi tiết", "P2",
     "Đang ở Chi tiết PXH-2",
     "1. Bấm PKK-1",
     "—",
     "- Mở Chi tiết PKK-1 ở tab mới"),

    ("007", "Quay lại từ Chi tiết", "P2",
     "Đang ở Chi tiết PXH-2",
     "1. Bấm Quay lại",
     "—",
     "- Về màn danh sách"),

    ("008", "Liên kết cột Phiếu xuất kho, Phiếu kiểm kê trên danh sách", "P1",
     "PXH-2 lập từ PXK-1, PKK-1",
     "1. Bấm PXK-1 ở cột Phiếu xuất kho\n"
     "2. Quay lại, bấm PKK-1 ở cột Phiếu kiểm kê",
     "—",
     "- Bước 1 mở Chi tiết PXK-1\n"
     "- Bước 2 mở Chi tiết PKK-1"),

    ("009", "Mở file đính kèm ở Chi tiết", "P2",
     "PXH-2 có file bb-thieu.pdf (từ PXK-1)",
     "1. Bấm biểu tượng file bb-thieu.pdf",
     "—",
     "- Mở file ở tab mới"),
]


SEC_II = [
    ("001", "Khối tìm kiếm đủ các ô lọc", "P0",
     "KT-3 có quyền theo tổng công ty, mở màn từ menu",
     "1. Bấm Bộ lọc",
     "—",
     "- Có ô: Mã phiếu, Kho, Trạng thái (Đang tạo, Đã hạch toán), Người tạo, Nhập mã hàng hóa, Nhập tên "
     "hàng hóa, Từ ngày, Đến ngày, Công ty, Phòng ban"),

    ("002", "Lọc theo Mã phiếu gõ một phần", "P0",
     "Có PXHĐCKK-00012 và PXHĐCKK-00013",
     "1. Nhập 00012 vào Mã phiếu, tìm",
     "Mã phiếu: 00012",
     "- Chỉ còn PXHĐCKK-00012"),

    ("003", "Lọc theo Trạng thái", "P0",
     "Có phiếu Đang tạo (của mình) và Đã hạch toán",
     "1. Chọn Trạng thái Đã hạch toán, tìm",
     "—",
     "- Chỉ còn phiếu Đã hạch toán"),

    ("004", "Lọc theo Người tạo", "P1",
     "KT-1 lập PXH-2, KT-2 lập PXH-4 (đều Đã hạch toán), người xem có quyền theo công ty",
     "1. Chọn Người tạo KT-2, tìm",
     "—",
     "- Chỉ còn PXH-4"),

    ("005", "Lọc theo mã hàng hóa", "P1",
     "PXH-2 có H1, PXH-4 chỉ có H7",
     "1. Nhập mã hàng của H1, tìm",
     "—",
     "- Chỉ còn PXH-2"),

    ("006", "Lọc theo tên hàng hóa gõ một phần", "P1",
     "PXH-2 có H1 tên \"Máy bơm X\", PXH-4 chỉ có H7 tên \"Ống nhựa\"",
     "1. Nhập \"bơm\" vào tên hàng hóa, tìm",
     "Tên hàng: bơm",
     "- Chỉ còn PXH-2"),

    ("007", "Lọc theo Kho", "P0",
     "PXH-2 kho K1, PXH-4 kho K2",
     "1. Chọn Kho K2, tìm",
     "—",
     "- Mong đợi: chỉ còn PXH-4\n"
     "- Lưu ý: theo code hiện tại vẫn ra cả PXH-2 và PXH-4 - ghi Failed"),

    ("008", "Lọc theo Từ ngày / Đến ngày", "P1",
     "PXH-2 lập ngày 01/10/2026, PXH-4 lập ngày 20/10/2026",
     "1. Chọn Từ ngày 15/10/2026, Đến ngày 31/10/2026, tìm",
     "—",
     "- Mong đợi: chỉ còn PXH-4\n"
     "- Lưu ý: theo code hiện tại vẫn ra cả 2 phiếu - ghi Failed"),

    ("009", "Lọc theo Công ty", "P1",
     "KT-3 có quyền theo tổng công ty; PXH-2 của TPE, PXH-5 của TPC",
     "1. Chọn Công ty TPC, tìm",
     "—",
     "- Chỉ còn PXH-5"),

    ("010", "Lọc theo Phòng ban", "P2",
     "KT-2 có quyền theo công ty; PXH-2 do thủ kho phòng Kho miền Bắc, PXH-6 do thủ kho phòng Kho miền "
     "Nam (cùng TPE)",
     "1. Chọn Phòng ban Kho miền Nam, tìm",
     "—",
     "- Chỉ còn PXH-6"),

    ("011", "Không có quyền xem thì không có ô Công ty, Phòng ban", "P2",
     "NV-A không có quyền xem",
     "1. Bấm Bộ lọc",
     "—",
     "- Không có ô Công ty, Phòng ban"),

    ("012", "Không có kết quả", "P2",
     "—",
     "1. Nhập Mã phiếu XYZ, tìm",
     "Mã phiếu: XYZ",
     "- Bảng báo không có dữ liệu"),
]


SEC_III = [
    ("001", "Phiếu Đang tạo của mình có Sửa và In", "P0",
     "KT-1 có PXH-3 Đang tạo",
     "1. KT-1 mở nút Hành động của PXH-3",
     "—",
     "- Có Sửa, In; không có Xóa"),

    ("002", "Phiếu Đã hạch toán chỉ có In", "P0",
     "KT-1 có PXH-2 Đã hạch toán",
     "1. KT-1 mở nút Hành động của PXH-2",
     "—",
     "- Chỉ có In"),

    ("003", "Bấm Sửa mở màn Sửa", "P0",
     "KT-1 có PXH-3 Đang tạo",
     "1. Mở Hành động > Sửa của PXH-3",
     "—",
     "- Mở màn Sửa với dữ liệu đã lưu; có nút Lưu, Lưu và duyệt, Hủy"),

    ("004", "Phân trang danh sách", "P2",
     "Có 12 phiếu nhìn thấy",
     "1. Chuyển sang trang 2",
     "—",
     "- Trang 2 có 2 phiếu, STT tiếp từ 11"),

    ("005", "Sắp theo Số phiếu", "P2",
     "Có nhiều phiếu",
     "1. Bấm tiêu đề cột Số phiếu",
     "—",
     "- Bảng sắp lại theo Số phiếu"),

    ("006", "Nút Tạo mới mở form không có phiếu xuất kho", "P2",
     "—",
     "1. Bấm Tạo mới\n"
     "2. Bấm Lưu",
     "—",
     "- Mong đợi: không có nút Tạo mới hoặc dẫn sang danh sách Phiếu xuất kho điều chỉnh kiểm kê\n"
     "- Lưu ý: theo code hiện tại form trống, bấm Lưu báo \"Tạo thất bại!\" - ghi Failed"),

    ("007", "Danh sách mặc định không có tham số loại thì chỉ phiếu mình lập", "P2",
     "KT-3 có quyền theo tổng công ty; có PXH-2 do KT-1 lập",
     "1. KT-3 mở đường dẫn danh sách nhưng bỏ phần \"?type=all\"",
     "—",
     "- Chỉ có phiếu KT-3 lập, không có PXH-2"),
]


SEC_IV = [
    ("001", "Nút Tạo phiếu xuất hàng chỉ ở phiếu xuất kho Chờ duyệt", "P0",
     PKK + "; PXK-2 Đang tạo, PXK-3 Đã hạch toán; " + KT1,
     "1. KT-1 " + MENU_PXK + "\n"
     "2. Mở Hành động của PXK-1, PXK-2, PXK-3",
     "—",
     "- Chỉ PXK-1 có \"Tạo phiếu xuất hàng\""),

    ("002", "Form lập lấy đủ thông tin từ phiếu xuất kho", "P0",
     PKK + "; " + GIA + "; " + KT1,
     "1. " + TAO,
     "—",
     "- Phiếu xuất kho = PXK-1 (liên kết), Phiếu kiểm kê = PKK-1, Kho = K1, Thủ kho = TK-1\n"
     "- Bảng có 2 dòng: H1 SL xuất 3, H2 SL xuất 1\n"
     "- File đính kèm có bb-thieu.pdf"),

    ("003", "Đơn giá xuất điền sẵn theo đơn giá bán của phiếu xuất kho", "P0",
     PKK + "; " + GIA,
     "1. " + TAO + "\n"
     "2. Quan sát Đơn giá xuất, Thành tiền xuất",
     "—",
     "- H1: 150,000 và 450,000\n"
     "- H2: 500,000 và 500,000"),

    ("004", "SL xuất không sửa được", "P0",
     "Đang ở form lập từ PXK-1",
     "1. Bấm vào ô SL xuất của H1",
     "—",
     "- SL xuất chỉ hiển thị, không nhập được"),

    ("005", "Sửa Đơn giá xuất thì Thành tiền xuất đổi", "P1",
     "Đang ở form lập từ PXK-1",
     "1. Sửa Đơn giá xuất H1 thành 120000",
     "Đơn giá: 120000",
     "- Ô hiện 120,000; Thành tiền xuất H1 = 360,000"),

    ("006", "Thêm file đính kèm", "P1",
     "Đang ở form lập từ PXK-1",
     "1. Bấm dấu + ở File đính kèm, chọn file bien-ban.pdf\n"
     "2. Bấm dấu x ở file vừa thêm",
     "File: bien-ban.pdf",
     "- Bước 1: hiện tên bien-ban.pdf\n"
     "- Bước 2: file bị bỏ"),

    ("007", "Kho kế toán chỉ có kho gắn với kho của phiếu, cùng công ty", "P0",
     PKK + "; " + KKT + "; kho K2 gắn KKT-C; K1 gắn KKT-D của TPC",
     "1. " + TAO + "\n"
     "2. Mở ô Kho kế toán của H1",
     "—",
     "- Chỉ có KKT-A, KKT-B; không có KKT-C, KKT-D"),

    ("008", "Hủy ở form lập", "P2",
     "Đang ở form lập từ PXK-1",
     "1. Bấm Hủy",
     "—",
     "- Về danh sách Phiếu xuất hàng điều chỉnh kiểm kê, không tạo phiếu"),

    ("009", "Mở form lập khi không có quyền Kế toán kho", "P1",
     PKK + "; NV-A không có quyền Kế toán kho",
     "1. NV-A dán đường dẫn \"Tạo phiếu xuất hàng\" của PXK-1",
     "—",
     "- Báo \"Không có quyền!\", form không có dòng hàng"),

    ("010", "Mở form lập từ phiếu xuất kho đã hạch toán", "P1",
     "PXK-3 Đã hạch toán; " + KT1,
     "1. KT-1 dán đường dẫn \"Tạo phiếu xuất hàng\" của PXK-3",
     "—",
     "- Báo \"Không có quyền!\", form không có dòng hàng"),
]
