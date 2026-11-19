# -*- coding: utf-8 -*-
"""Section I, II, III, IV - hien thi, bo loc, danh sach, lap phieu tu phieu nhap kho."""
from tc_data_role import MENU, MENU_PNK, PKK, GIA, KKT, KT1, TAO

SEC_I = [
    ("001", "Vào màn từ menu Kế toán", "P0",
     KT1 + ", đã lập ít nhất 1 phiếu",
     "1. " + MENU + "\n"
     "2. Quan sát tiêu đề và bảng",
     "—",
     "- Mở màn danh sách phiếu nhập hàng điều chỉnh kiểm kê\n"
     "- Bảng tải dữ liệu, không báo lỗi"),

    ("002", "Bố cục mặc định của màn danh sách", "P0",
     "KT-1 đã lập 12 phiếu",
     "1. Mở màn từ menu\n"
     "2. Quan sát từ trên xuống",
     "—",
     "- Hàng nút: Bộ lọc, Tạo mới, In, Xuất excel\n"
     "- Bảng có cột: STT, Số phiếu, Phiếu nhập kho, Phiếu kiểm kê, Kho, Người lập, Ngày lập, Trạng thái, "
     "Hành động\n"
     "- 10 dòng mỗi trang, phiếu mới lập nhất lên đầu"),

    ("003", "Tiêu đề trang khớp tên menu", "P2",
     "—",
     "1. Mở màn từ menu, quan sát tiêu đề tab trình duyệt",
     "—",
     "- Mong đợi: \"Phiếu nhập hàng điều chỉnh kiểm kê\"\n"
     "- Lưu ý: theo code hiện tại ghi \"Nhập điều chỉnh sau kiểm kho\" - ghi Failed"),

    ("004", "Nhãn trạng thái đúng màu", "P2",
     "Có phiếu Đang tạo và phiếu Đã hạch toán",
     "1. Quan sát cột Trạng thái",
     "—",
     "- Đang tạo: nhãn đỏ\n"
     "- Đã hạch toán: nhãn xanh"),

    ("005", "Bấm Số phiếu mở màn Chi tiết", "P0",
     "PNH-2 Đã hạch toán do KT-1 lập từ PNK-1 (PKK-1), kho K1",
     "1. Bấm Số phiếu PNH-2",
     "—",
     "- Có ô Phiếu nhập kho (liên kết PNK-1), Phiếu kiểm kê (liên kết PKK-1), Kho K1, Thủ kho TK-1, Nhân "
     "viên, Ghi chú\n"
     "- Bảng chi tiết, ô đơn giá và kho kế toán bị khóa\n"
     "- Không có nút thêm file; cuối trang chỉ có Quay lại"),

    ("006", "Bấm liên kết Phiếu nhập kho ở Chi tiết", "P2",
     "Đang ở Chi tiết PNH-2",
     "1. Bấm PNK-1",
     "—",
     "- Mở Chi tiết PNK-1 ở tab mới"),

    ("007", "Bấm liên kết Phiếu kiểm kê ở Chi tiết", "P2",
     "Đang ở Chi tiết PNH-2",
     "1. Bấm PKK-1",
     "—",
     "- Mở Chi tiết PKK-1 ở tab mới"),

    ("008", "Quay lại từ Chi tiết", "P2",
     "Đang ở Chi tiết PNH-2",
     "1. Bấm Quay lại",
     "—",
     "- Về màn danh sách"),

    ("009", "Liên kết cột Phiếu nhập kho, Phiếu kiểm kê trên danh sách", "P1",
     "PNH-2 lập từ PNK-1, PKK-1",
     "1. Bấm PNK-1 ở cột Phiếu nhập kho\n"
     "2. Quay lại, bấm PKK-1 ở cột Phiếu kiểm kê",
     "—",
     "- Bước 1 mở Chi tiết PNK-1\n"
     "- Bước 2 mở Chi tiết PKK-1"),
]


SEC_II = [
    ("001", "Khối tìm kiếm đủ các ô lọc", "P0",
     "Mở màn từ menu",
     "1. Bấm Bộ lọc",
     "—",
     "- Có ô: Mã phiếu, Kho, Trạng thái (Đang tạo, Đã hạch toán), Người tạo, Nhập mã hàng hóa, Nhập tên "
     "hàng hóa, Từ ngày, Đến ngày"),

    ("002", "Lọc theo Mã phiếu tìm gần đúng", "P0",
     "Có PNHĐCKK-00007 và PNHĐCKK-00008",
     "1. Nhập \"00007\" vào ô Mã phiếu",
     "Mã phiếu: 00007",
     "- Chỉ còn PNHĐCKK-00007"),

    ("003", "Lọc theo Trạng thái", "P0",
     "KT-1 có 2 phiếu Đang tạo, 3 phiếu Đã hạch toán",
     "1. Chọn Trạng thái \"Đã hạch toán\"",
     "—",
     "- Còn đúng 3 phiếu Đã hạch toán"),

    ("004", "Lọc theo Người tạo", "P0",
     "KT-3 xem theo tổng công ty; KT-1 lập 3 phiếu, KT-2 lập 2 phiếu (đều Đã hạch toán)",
     "1. KT-3 chọn Người tạo KT-2",
     "—",
     "- Còn đúng 2 phiếu của KT-2"),

    ("005", "Lọc theo Kho", "P0",
     "PNH-2 kho K1, PNH-6 kho K2",
     "1. Chọn Kho K2",
     "—",
     "- Mong đợi: chỉ còn PNH-6\n"
     "- Lưu ý: theo code hiện tại danh sách không đổi (vẫn có PNH-2) - ghi Failed"),

    ("006", "Lọc theo mã hàng hóa", "P0",
     "PNH-2 có H4 (mã MH-H4), PNH-6 chỉ có H7",
     "1. Nhập \"MH-H4\" vào ô Nhập mã hàng hóa",
     "Mã hàng: MH-H4",
     "- Mong đợi: chỉ còn PNH-2\n"
     "- Lưu ý: theo code hiện tại vẫn hiện cả PNH-6 - ghi Failed"),

    ("007", "Lọc theo tên hàng hóa", "P1",
     "PNH-2 có \"Van khóa D20\", PNH-6 chỉ có \"Ống nhựa\"",
     "1. Nhập \"Van\" vào ô Nhập tên hàng hóa",
     "Tên hàng: Van",
     "- Mong đợi: chỉ còn PNH-2\n"
     "- Lưu ý: theo code hiện tại vẫn hiện cả PNH-6 - ghi Failed"),

    ("008", "Lọc theo Từ ngày / Đến ngày", "P1",
     "PNH-2 lập ngày 01/10/2026, PNH-6 lập ngày 20/10/2026",
     "1. Chọn Từ ngày 15/10/2026, Đến ngày 25/10/2026",
     "—",
     "- Mong đợi: chỉ còn PNH-6\n"
     "- Lưu ý: theo code hiện tại vẫn hiện cả PNH-2 - ghi Failed"),

    ("009", "Lọc theo Công ty / Phòng ban", "P2",
     "KT-3 xem theo tổng công ty; PNH-2 của TPE, PNH-5 của TPC",
     "1. Chọn Công ty TPC (nếu có ô)",
     "—",
     "- Mong đợi: chỉ còn PNH-5\n"
     "- Lưu ý: theo code hiện tại không lọc - ghi Failed"),

    ("010", "Kết hợp Mã phiếu và Trạng thái", "P1",
     "PNHĐCKK-00007 Đang tạo, PNHĐCKK-00017 Đã hạch toán (đều của KT-1)",
     "1. Nhập Mã phiếu \"0007\", chọn Trạng thái Đã hạch toán",
     "—",
     "- Còn đúng PNHĐCKK-00017"),

    ("011", "Lọc không có kết quả", "P2",
     "—",
     "1. Nhập Mã phiếu \"XYZ999\"",
     "—",
     "- Bảng báo không có dữ liệu"),
]


SEC_III = [
    ("001", "Thứ tự dòng mới nhất lên đầu", "P1",
     "KT-1 lập PNH-2 ngày 01/10, PNH-6 ngày 20/10",
     "1. Mở màn từ menu",
     "—",
     "- PNH-6 nằm trên PNH-2"),

    ("002", "Hành động của phiếu Đang tạo do mình lập", "P0",
     "PNH-3 Đang tạo do KT-1 lập",
     "1. KT-1 mở nút Hành động của PNH-3",
     "—",
     "- Có Sửa, In\n"
     "- Không có Xóa"),

    ("003", "Hành động của phiếu Đã hạch toán", "P0",
     "PNH-2 Đã hạch toán do KT-1 lập",
     "1. KT-1 mở nút Hành động của PNH-2",
     "—",
     "- Chỉ có In"),

    ("004", "Phân trang", "P2",
     "KT-1 có 25 phiếu",
     "1. Bấm sang trang 3",
     "—",
     "- Trang 3 có 5 dòng, STT 21 đến 25"),

    ("005", "Cột Kho, Người lập, Ngày lập", "P1",
     "PNH-2 do KT-1 lập ngày 05/10/2026, kho K1",
     "1. Quan sát dòng PNH-2",
     "—",
     "- Kho: tên kho K1\n"
     "- Người lập: KT-1\n"
     "- Ngày lập: 05/10/2026"),

    ("006", "Nút Tạo mới trên danh sách", "P1",
     "—",
     "1. Bấm Tạo mới\n"
     "2. Bấm Lưu",
     "—",
     "- Mong đợi: không có nút Tạo mới (phiếu chỉ lập từ phiếu nhập kho)\n"
     "- Lưu ý: theo code hiện tại mở form trống, không có hàng; bấm Lưu báo \"Tạo thất bại!\" - ghi Failed"),
]


SEC_IV = [
    ("001", "Lập phiếu từ Phiếu nhập kho Chờ duyệt", "P0",
     PKK + "; " + KT1,
     "1. " + TAO,
     "—",
     "- Mở form lập phiếu nhập hàng\n"
     "- Phiếu nhập kho = PNK-1 (liên kết), Phiếu kiểm kê = PKK-1, Kho = K1, Thủ kho = TK-1 (đều không sửa)"),

    ("002", "Bảng chi tiết lấy đúng hàng của phiếu nhập kho", "P0",
     PKK + "; " + GIA,
     "1. " + TAO + "\n"
     "2. Quan sát bảng Chi tiết",
     "—",
     "- 2 dòng: H4 SL nhập 4, H5 SL nhập 2, ĐVT Cái\n"
     "- SL nhập không sửa được"),

    ("003", "Đơn giá nhập điền sẵn theo lần nhập gần nhất", "P0",
     PKK + "; " + GIA,
     "1. " + TAO,
     "—",
     "- H4: Đơn giá 120,000; Thành tiền 480,000\n"
     "- H5: Đơn giá 300,000; Thành tiền 600,000"),

    ("004", "Hàng chưa từng nhập thì Đơn giá bằng 0", "P1",
     "PNK-2 Chờ duyệt có H9 chưa từng có trên Phiếu nhập hàng nào",
     "1. KT-1 lập phiếu từ PNK-2",
     "—",
     "- Dòng H9: Đơn giá 0, Thành tiền 0"),

    ("005", "Sửa Đơn giá thì Thành tiền tính lại", "P0",
     "Đang ở form lập từ PNK-1",
     "1. Sửa Đơn giá H4 thành 150000",
     "Đơn giá H4: 150000",
     "- Ô hiện 150,000; Thành tiền H4 = 600,000"),

    ("006", "Mỗi dòng có sẵn 1 dòng kho kế toán đủ SL", "P0",
     "Đang ở form lập từ PNK-1",
     "1. Quan sát cột Kho kế toán, Số lượng",
     "—",
     "- H4: 1 dòng \"Chọn kho kế toán\", Số lượng 4\n"
     "- H5: 1 dòng \"Chọn kho kế toán\", Số lượng 2"),

    ("007", "Danh sách kho kế toán chỉ gồm kho gắn với kho K1, cùng công ty", "P0",
     KKT + "; kho K2 có KKT-C; TPC có KKT-D gắn kho K1",
     "1. Mở ô Kho kế toán dòng H4",
     "—",
     "- Chỉ có KKT-A, KKT-B"),

    ("008", "Ô Nhân viên ban đầu trống, bắt buộc", "P1",
     "Đang ở form lập từ PNK-1",
     "1. Quan sát ô Nhân viên",
     "—",
     "- Ô trống, có dấu bắt buộc, chọn được nhân viên trong danh sách"),

    ("009", "File của phiếu nhập kho hiện sẵn", "P1",
     PKK,
     "1. " + TAO + ", quan sát khu File đính kèm",
     "—",
     "- Có file bb-thua.pdf, bấm mở được\n"
     "- Có nút dấu cộng để thêm file"),

    ("010", "Phiếu nhập kho không còn Chờ duyệt thì không mở form", "P0",
     "PNK-1 đã Đang hạch toán (đã có PNH-3 Đang tạo)",
     "1. KT-1 dán đường dẫn \"Tạo phiếu nhập hàng\" của PNK-1",
     "—",
     "- Báo \"Không có quyền!\"\n"
     "- Bảng chi tiết trống"),

    ("011", "Phiếu nhập kho Đang hạch toán không còn nút Tạo phiếu nhập hàng", "P0",
     "PNK-1 Đang hạch toán",
     "1. KT-1 " + MENU_PNK + ", mở nút Hành động của PNK-1",
     "—",
     "- Không có \"Tạo phiếu nhập hàng\""),

    ("012", "Hủy ở form lập", "P2",
     "Đang ở form lập từ PNK-1",
     "1. Bấm Hủy",
     "—",
     "- Về danh sách phiếu nhập hàng điều chỉnh kiểm kê; không tạo phiếu, PNK-1 vẫn Chờ duyệt"),
]
