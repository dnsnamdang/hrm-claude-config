# -*- coding: utf-8 -*-
"""Section I, II, III, IV - hien thi & loi vao, bo loc, danh sach, tao moi."""
from tc_data_role import MENU, MENU_CHO_DUYET, PKK, TON_KT, TK1, KT1, TAO

SEC_I = [
    ("001", "Vào màn từ menu Kho", "P0",
     TK1 + ", đã lập ít nhất 1 phiếu",
     "1. " + MENU + "\n"
     "2. Quan sát tiêu đề và bảng",
     "—",
     "- Tiêu đề trang \"Phiếu xuất kho điều chỉnh kiểm kê\"\n"
     "- Bảng tải dữ liệu, không báo lỗi"),

    ("002", "Bố cục mặc định của màn danh sách", "P0",
     "TK-1 đã lập 12 phiếu",
     "1. Mở màn từ menu\n"
     "2. Quan sát từ trên xuống",
     "—",
     "- Hàng nút: Bộ lọc, Tạo mới, In, Xuất excel\n"
     "- Bảng có cột: STT, Số phiếu, Ngày kiểm kê, Kho, Trạng thái, Người lập, Hành động\n"
     "- 10 dòng mỗi trang, phiếu mới lập nhất lên đầu"),

    ("003", "Vào màn Chờ duyệt", "P0",
     KT1 + "; có 2 phiếu Chờ duyệt, 1 phiếu Đang hạch toán",
     "1. " + MENU_CHO_DUYET,
     "—",
     "- Chỉ có 2 phiếu Chờ duyệt"),

    ("004", "Mục Chờ duyệt ẩn với người không có quyền Kế toán kho", "P1",
     "TK-1 không có quyền Kế toán kho",
     "1. Mở menu Chờ duyệt > \"Hàng hóa – dịch vụ – vận chuyển\" > nhóm \"Xuất hàng\"",
     "—",
     "- Không có mục \"Phiếu xuất kho điều chỉnh kiểm kê chờ duyệt\""),

    ("005", "Ô đếm phiếu chờ duyệt trên trang chủ", "P1",
     KT1 + "; TPE có 2 phiếu Chờ duyệt, TPC có 1 phiếu Chờ duyệt",
     "1. KT-1 mở trang chủ, tìm ô \"Phiếu xuất kho điều chỉnh kiểm kê chờ duyệt\"\n"
     "2. Bấm vào ô",
     "—",
     "- Ô ghi 2\n"
     "- Mong đợi: màn mở ra có 2 phiếu\n"
     "- Lưu ý: theo code hiện tại màn mở ra có 3 phiếu (gồm cả của TPC) - ghi Failed"),

    ("006", "Nhãn trạng thái hiển thị đúng màu", "P2",
     "Có phiếu ở cả 4 trạng thái",
     "1. Mở màn từ menu, quan sát cột Trạng thái",
     "—",
     "- Đã hạch toán: nhãn xanh\n"
     "- Đang tạo, Chờ duyệt, Đang hạch toán: nhãn đỏ"),

    ("007", "Bấm Số phiếu mở màn Chi tiết", "P0",
     "PX-2 Chờ duyệt do TK-1 lập từ PKK-1",
     "1. Bấm Số phiếu PX-2",
     "—",
     "- Tiêu đề \"Phiếu xuất kho điều chỉnh kiểm kê PXKĐCKK-...\"\n"
     "- Có ô Phiếu kiểm kho là liên kết PKK-1, Kho, Ghi chú bị khóa, các file đã đính kèm\n"
     "- Không có nút thêm file; cuối trang chỉ có nút Quay lại"),

    ("008", "Bấm liên kết phiếu kiểm kê ở Chi tiết", "P2",
     "Đang ở Chi tiết PX-2",
     "1. Bấm PKK-1 ở ô Phiếu kiểm kho",
     "—",
     "- Mở Chi tiết PKK-1 ở tab mới"),

    ("009", "Quay lại từ Chi tiết", "P2",
     "Đang ở Chi tiết PX-2",
     "1. Bấm Quay lại",
     "—",
     "- Về màn danh sách Tất cả"),
]


SEC_II = [
    ("001", "Khối tìm kiếm đủ các ô lọc", "P0",
     "Mở màn từ menu Kho",
     "1. Bấm Bộ lọc",
     "—",
     "- Có ô: Mã phiếu, Kho, Trạng thái (Đang tạo, Chờ duyệt, Đang hạch toán, Đã hạch toán), Người tạo, "
     "Nhập mã hàng hóa, Nhập tên hàng hóa, Từ ngày, Đến ngày\n"
     "- Có thêm ô Phòng ban (và Công ty nếu có quyền xem nhiều công ty)"),

    ("002", "Lọc theo Mã phiếu tìm gần đúng", "P0",
     "Có PXKĐCKK-00007 và PXKĐCKK-00008",
     "1. Nhập \"00007\" vào ô Mã phiếu",
     "Mã phiếu: 00007",
     "- Chỉ còn PXKĐCKK-00007"),

    ("003", "Lọc theo Trạng thái", "P0",
     "Có 3 phiếu Chờ duyệt, 2 phiếu Đã hạch toán",
     "1. Chọn Trạng thái \"Đã hạch toán\"",
     "—",
     "- Còn đúng 2 phiếu Đã hạch toán"),

    ("004", "Lọc theo Người tạo", "P0",
     "KT-3 xem theo tổng công ty; TK-1 lập 3 phiếu, TK-2 lập 2 phiếu (đều Chờ duyệt)",
     "1. KT-3 chọn Người tạo TK-2",
     "—",
     "- Còn đúng 2 phiếu của TK-2"),

    ("005", "Lọc theo mã hàng hóa", "P0",
     "PX-2 có hàng H1 (mã MH-H1), PX-4 chỉ có H2",
     "1. Nhập \"MH-H1\" vào ô Nhập mã hàng hóa",
     "Mã hàng: MH-H1",
     "- Chỉ còn PX-2"),

    ("006", "Lọc theo tên hàng hóa tìm gần đúng", "P1",
     "PX-2 có hàng \"Máy bơm A\", PX-4 chỉ có \"Ống nhựa\"",
     "1. Nhập \"bơm\" vào ô Nhập tên hàng hóa",
     "Tên hàng: bơm",
     "- Chỉ còn PX-2"),

    ("007", "Lọc theo Kho", "P0",
     "PX-2 kho K1, PX-6 kho K2",
     "1. Chọn Kho K2",
     "—",
     "- Mong đợi: chỉ còn PX-6\n"
     "- Lưu ý: theo code hiện tại danh sách không đổi (vẫn có PX-2) - ghi Failed"),

    ("008", "Lọc theo Từ ngày / Đến ngày", "P1",
     "PX-2 lập ngày 01/10/2026, PX-4 lập ngày 20/10/2026",
     "1. Chọn Từ ngày 15/10/2026, Đến ngày 25/10/2026",
     "—",
     "- Mong đợi: chỉ còn PX-4\n"
     "- Lưu ý: theo code hiện tại vẫn hiện cả PX-2 - ghi Failed"),

    ("009", "Lọc theo Phòng ban / Công ty", "P2",
     "KT-3 xem theo tổng công ty; PX-2 của TPE, PX-5 của TPC",
     "1. Chọn Công ty TPC",
     "—",
     "- Mong đợi: chỉ còn PX-5\n"
     "- Lưu ý: theo code hiện tại vẫn hiện cả PX-2 - ghi Failed"),

    ("010", "Kết hợp nhiều ô lọc", "P1",
     "PX-2 (TK-1, Chờ duyệt, có H1), PX-4 (TK-1, Đã hạch toán, có H1), PX-7 (TK-2, Chờ duyệt, có H1)",
     "1. Chọn Người tạo TK-1, Trạng thái Chờ duyệt, nhập mã hàng MH-H1",
     "—",
     "- Chỉ còn PX-2"),

    ("011", "Lọc không có kết quả", "P2",
     "—",
     "1. Nhập Mã phiếu \"XYZ999\"",
     "—",
     "- Bảng báo không có dữ liệu, không lỗi"),
]


SEC_III = [
    ("001", "Giá trị các cột trên một dòng", "P0",
     "PX-2 do TK-1 lập ngày 26/10/2026, kho K1, Chờ duyệt",
     "1. Mở màn từ menu, đọc dòng PX-2",
     "—",
     "- Số phiếu PXKĐCKK-..., Ngày kiểm kê 26/10/2026 (là ngày lập phiếu xuất), Kho K1, Trạng thái Chờ "
     "duyệt, Người lập TK-1"),

    ("002", "Nút Hành động theo trạng thái", "P0",
     "TK-1 là người lập PX-3 (Đang tạo), PX-2 (Chờ duyệt), PX-4 (Đã hạch toán)",
     "1. TK-1 mở nút Hành động của từng phiếu",
     "—",
     "- PX-3: Sửa, In\n"
     "- PX-2, PX-4: chỉ In"),

    ("003", "Không có chức năng Xóa", "P2",
     "PX-3 Đang tạo do TK-1 lập",
     "1. TK-1 mở nút Hành động của PX-3",
     "—",
     "- Không có Xóa; phiếu Đang tạo không xóa được"),

    ("004", "Phân trang", "P1",
     "TK-1 có 25 phiếu",
     "1. Mở màn, bấm sang trang 3",
     "—",
     "- Trang 3 có 5 phiếu, STT 21 đến 25"),

    ("005", "Màn mở không kèm loại danh sách chỉ hiện phiếu của mình", "P2",
     "KT-3 có quyền theo tổng công ty, chưa lập phiếu nào",
     "1. Dán đường dẫn danh sách bỏ phần \"type=all\"",
     "—",
     "- Bảng không có phiếu nào"),
]


SEC_IV = [
    ("001", "Nút lập phiếu trên phiếu kiểm kê có hàng thiếu", "P0",
     TK1 + "\n" + PKK,
     "1. TK-1 mở Chi tiết PKK-1, xem các nút cuối trang",
     "—",
     "- Có nút \"Tạo phiếu xuất kho điều chuyển\""),

    ("002", "Mở form từ phiếu kiểm kê tự lấy dữ liệu", "P0",
     TK1 + "\n" + PKK,
     "1. Bấm \"Tạo phiếu xuất kho điều chuyển\"",
     "—",
     "- Ô Phiếu kiểm kho = PKK-1, Kho tự chọn K1\n"
     "- Bảng Chi tiết có 2 dòng: H1 vị trí P1 lô L01 SL xuất 5; H2 vị trí P2 lô L02 SL xuất 2\n"
     "- Nút Lưu, Gửi duyệt, Hủy"),

    ("003", "Đơn giá bán và Thành tiền bán", "P0",
     PKK,
     "1. Mở form từ PKK-1, đọc cột Đơn giá bán và Thành tiền bán",
     "—",
     "- H1: 150,000 và 750,000\n"
     "- H2: 250,000 và 500,000\n"
     "- Ô Đơn giá bán bị khóa"),

    ("004", "Hàng lệch tổng bằng 0 không vào phiếu xuất", "P0",
     PKK,
     "1. Mở form từ PKK-1, tìm H3",
     "—",
     "- Không có H3 (thuộc Phiếu điều chuyển vị trí)"),

    ("005", "Hàng thừa không vào phiếu xuất", "P0",
     PKK,
     "1. Mở form từ PKK-1, tìm H4",
     "—",
     "- Không có H4 (thuộc Phiếu nhập kho điều chỉnh kiểm kê)"),

    ("006", "Hàng thiếu ở vị trí này, thừa ít hơn ở vị trí khác", "P1",
     "PKK-3 kho K1: H5 vị trí P1 thiếu 5, vị trí P2 thừa 2 (tổng lệch -3)",
     "1. Mở form từ PKK-3",
     "—",
     "- Có 1 dòng H5 vị trí P1 SL xuất 5 (số thiếu của vị trí, không phải tổng lệch 3)"),

    ("007", "Kiểm kê nhiều kho: đổi kho tải lại hàng", "P0",
     "PKK-4 kiểm kê K1 và K2: K1 thiếu H1 = 5; K2 thiếu H6 = 1",
     "1. Mở form từ PKK-4\n"
     "2. Đổi Kho sang K2",
     "—",
     "- Ô Kho chỉ có K1, K2\n"
     "- Bước 1: bảng có H1 = 5\n"
     "- Bước 2: bảng đổi thành H6 = 1"),

    ("008", "Kho không có hàng thiếu", "P1",
     "PKK-4 kiểm kê K1 và K2; K2 không thiếu hàng nào",
     "1. Mở form từ PKK-4, chọn Kho K2",
     "—",
     "- Bảng Chi tiết trống"),

    ("009", "Phiếu kiểm kê đã có phiếu xuất thì ẩn nút", "P0",
     "PKK-1 đã có PX-3 (Đang tạo)",
     "1. TK-1 mở Chi tiết PKK-1",
     "—",
     "- Không còn nút \"Tạo phiếu xuất kho điều chuyển\""),

    ("010", "Phiếu kiểm kê không có hàng thiếu thì không có nút", "P1",
     "PKK-5 chỉ có hàng thừa",
     "1. TK-1 mở Chi tiết PKK-5",
     "—",
     "- Không có nút \"Tạo phiếu xuất kho điều chuyển\""),

    ("011", "Phiếu kiểm kê chưa tới bước xử lý", "P1",
     "PKK-6 có hàng thiếu, đang Chờ kế toán duyệt kết quả",
     "1. TK-1 mở Chi tiết PKK-6",
     "—",
     "- Không có nút \"Tạo phiếu xuất kho điều chuyển\""),

    ("012", "Bấm Tạo mới từ màn danh sách", "P2",
     TK1,
     "1. Ở màn danh sách bấm Tạo mới\n"
     "2. Chọn Kho K1",
     "—",
     "- Mong đợi: báo cần lập từ phiếu kiểm kê, hoặc không có nút Tạo mới\n"
     "- Lưu ý: theo code hiện tại mở form không có Phiếu kiểm kho, chọn kho không ra hàng, bấm Lưu bị báo "
     "lỗi - ghi Failed"),

    ("013", "Hủy ở form tạo", "P2",
     "Đang ở form tạo từ PKK-1",
     "1. Bấm Hủy",
     "—",
     "- Về màn danh sách Tất cả, không có phiếu mới"),

    ("014", "Nhãn nút trên phiếu kiểm kê", "P2",
     PKK,
     "1. TK-1 mở Chi tiết PKK-1, đọc nhãn nút",
     "—",
     "- Mong đợi: \"Tạo phiếu xuất kho điều chỉnh kiểm kê\"\n"
     "- Lưu ý: hiện ghi \"Tạo phiếu xuất kho điều chuyển\" - ghi Failed nếu nghiệp vụ yêu cầu đổi"),
]
