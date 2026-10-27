# -*- coding: utf-8 -*-
"""Section I, II, III - hien thi & truy cap, bo loc & danh sach, chon phieu nhap kho."""
from tc_data_role import MENU, NK1

SEC_I = [
    ("001", "Vào màn từ menu Kho", "P0",
     "TK-1 đã lập 3 phiếu xuất lại",
     "1. Đăng nhập TK-1\n"
     "2. " + MENU,
     "—",
     "- Tiêu đề \"Danh sách phiếu xuất lại\"\n"
     "- Bảng tải dữ liệu, có 3 phiếu"),

    ("002", "Bố cục mặc định của màn danh sách", "P0",
     "TK-1 đã lập 12 phiếu xuất lại",
     "1. Mở màn từ menu\n"
     "2. Quan sát từ trên xuống",
     "—",
     "- Hàng nút: Bộ lọc, Xuất excel (không có Tạo mới, không có In)\n"
     "- Cột: STT, Mã phiếu, Phiếu NK, Ngày lập, Người lập, Trạng thái, Hành động\n"
     "- 10 dòng mỗi trang, phiếu mới tạo nhất lên đầu"),

    ("003", "Nhãn trạng thái đúng màu", "P1",
     "TK-1 có PXL-1 Chờ nhập lại, PXL-2 Đã nhập lại",
     "1. Quan sát cột Trạng thái",
     "—",
     "- PXL-1: \"Chờ nhập lại\" nhãn đỏ\n"
     "- PXL-2: \"Đã nhập lại\" nhãn xanh"),

    ("004", "Bấm Mã phiếu mở chi tiết", "P0",
     "PXL-1 do TK-1 lập",
     "1. Đăng nhập TK-1, bấm Mã phiếu PXL-1",
     "—",
     "- Mở màn chi tiết PXL-1, mọi ô bị khóa, cuối trang chỉ có nút Quay lại"),

    ("005", "Bấm Phiếu NK mở phiếu nhập kho gốc", "P1",
     "PXL-1 xuất lại từ NK-1",
     "1. Bấm NK-1 ở cột Phiếu NK",
     "—",
     "- Mở màn chi tiết phiếu nhập kho NK-1"),

    ("006", "Cột Hành động khi phiếu nhập gốc đã xuất lại", "P0",
     "PXL-1 do TK-1 lập từ NK-1; NK-1 đang \"Đã xuất lại\"",
     "1. Đăng nhập TK-1, bấm nút bánh răng dòng PXL-1",
     "—",
     "- Có mục \"Tạo phiếu nhập lại\""),

    ("007", "Cột Hành động khi đã nhập lại", "P1",
     "PXL-2 Đã nhập lại (NK-2 đã \"Đã nhập lại\")",
     "1. Bấm nút bánh răng dòng PXL-2",
     "—",
     "- Danh sách thao tác trống, không có \"Tạo phiếu nhập lại\""),

    ("008", "Người xem không phải người lập không thấy Tạo phiếu nhập lại", "P1",
     "TP-1 thấy PXL-1 (TK-1 lập, NK-1 Đã xuất lại)",
     "1. Đăng nhập TP-1, bấm bánh răng dòng PXL-1",
     "—",
     "- Không có mục \"Tạo phiếu nhập lại\""),

    ("009", "Màn không có Sửa, Xóa, Duyệt", "P1",
     "PXL-1 Chờ nhập lại do TK-1 lập",
     "1. Đăng nhập TK-1, mở bánh răng và màn chi tiết PXL-1",
     "—",
     "- Không có thao tác Sửa, Xóa, Gửi duyệt, Duyệt ở bất kỳ đâu"),

    ("010", "Lối vào tạo phiếu xuất lại từ Phiếu nhập kho", "P0",
     NK1,
     "1. Đăng nhập TK-1, mở Kho > Nhập kho > Phiếu nhập kho\n"
     "2. Bấm bánh răng dòng NK-1",
     "—",
     "- Có mục \"Tạo phiếu xuất lại\"\n"
     "- Bấm mục này mở form tạo, ô phiếu nhập kho đã điền NK-1"),
]

SEC_II = [
    ("011", "Lọc theo Mã phiếu", "P0",
     "Có PXL-00012, PXL-00013, PXL-00120",
     "1. Bấm Bộ lọc, nhập \"0012\" ở ô Mã phiếu",
     "Mã phiếu: 0012",
     "- Ra PXL-00012 và PXL-00120, không có PXL-00013"),

    ("012", "Lọc theo Phiếu NK", "P0",
     "PXL-1 từ NK-00051, PXL-2 từ NK-00077",
     "1. Nhập \"00051\" ở ô Phiếu NK",
     "Phiếu NK: 00051",
     "- Chỉ ra PXL-1"),

    ("013", "Lọc theo Trạng thái Chờ nhập lại", "P0",
     "Có 2 phiếu Chờ nhập lại, 1 phiếu Đã nhập lại",
     "1. Chọn Trạng thái \"Chờ nhập lại\"",
     "—",
     "- Ra đúng 2 phiếu Chờ nhập lại"),

    ("014", "Lọc theo Trạng thái Đã nhập lại", "P1",
     "Như trên",
     "1. Chọn Trạng thái \"Đã nhập lại\"",
     "—",
     "- Ra đúng 1 phiếu"),

    ("015", "Lọc theo Người lập", "P1",
     "TP-1 thấy PXL-1 (TK-1 lập) và PXL-3 (TK-3 lập)",
     "1. Đăng nhập TP-1, chọn Người lập TK-1",
     "Người lập: TK-1",
     "- Mong đợi: chỉ ra PXL-1\n"
     "- Lưu ý: theo code hiện tại vẫn ra cả PXL-3 (ô Người lập không có tác dụng) - ghi Failed"),

    ("016", "Trưởng phòng lọc theo Bộ phận", "P1",
     "TP-1 là trưởng phòng, ô Bộ phận hiện trên bộ lọc",
     "1. Chọn 1 bộ phận bất kỳ",
     "—",
     "- Mong đợi: ra phiếu của người thuộc bộ phận đó\n"
     "- Lưu ý: theo code hiện tại bảng báo lỗi, không tải được - ghi Failed"),

    ("017", "Tổng giám đốc lọc theo Công ty", "P1",
     "TGD-1 có quyền Xem tất cả phiếu; PXL-1 của TPE, PXL-5 của TPC",
     "1. Chọn Công ty TPC",
     "—",
     "- Chỉ ra PXL-5"),

    ("018", "Lọc theo Phòng ban", "P2",
     "GD-1 có quyền Xem tất cả phiếu của công ty; PXL-1 phòng Kho, PXL-6 phòng Kinh doanh",
     "1. Chọn Phòng ban Kho",
     "—",
     "- Chỉ ra PXL-1"),

    ("019", "Kết hợp nhiều điều kiện lọc", "P1",
     "PXL-00012 Chờ nhập lại từ NK-00051; PXL-00120 Đã nhập lại",
     "1. Nhập Mã phiếu \"0012\", chọn Trạng thái Chờ nhập lại",
     "—",
     "- Chỉ ra PXL-00012"),

    ("020", "Lọc không có kết quả", "P2",
     "—",
     "1. Nhập Mã phiếu \"KHONGCO\"",
     "Mã phiếu: KHONGCO",
     "- Bảng báo không có dữ liệu, không lỗi"),

    ("021", "Lọc ký tự đặc biệt", "P2",
     "—",
     "1. Nhập Mã phiếu \"%_'\"",
     "Mã phiếu: %_'",
     "- Không báo lỗi, bảng trống hoặc ra đúng phiếu chứa chuỗi"),
]

SEC_III = [
    ("022", "Sắp xếp theo Mã phiếu", "P2",
     "Có 5 phiếu",
     "1. Bấm tiêu đề cột Mã phiếu 2 lần",
     "—",
     "- Lần 1 tăng dần, lần 2 giảm dần"),

    ("023", "Sắp xếp theo Ngày lập", "P2",
     "Có phiếu tạo ngày 01/10, 15/10, 20/10",
     "1. Bấm tiêu đề cột Ngày lập",
     "—",
     "- Sắp đúng thứ tự ngày"),

    ("024", "Phân trang", "P1",
     "TK-1 có 12 phiếu",
     "1. Chuyển sang trang 2",
     "—",
     "- Trang 2 có 2 phiếu, STT 11 và 12"),

    ("025", "Mở form tạo trống", "P0",
     "TK-1 đăng nhập",
     "1. Mở đường dẫn tạo phiếu xuất lại (không kèm phiếu nhập)",
     "—",
     "- Tiêu đề \"Tạo phiếu xuất lại\"\n"
     "- Ô Chọn phiếu nhập kho trống có dấu (*); Người lập, Người giao hàng trống\n"
     "- Khung Chi tiết ghi \"Chưa chọn phiếu nhập kho\"\n"
     "- Có nút Xuất lại, Hủy"),

    ("026", "Cửa sổ tìm chỉ có phiếu nhập Không duyệt của mình", "P0",
     NK1 + "\nTK-1 còn NK-2 Chờ duyệt, NK-3 Đã hạch toán",
     "1. Bấm kính lúp ở ô Chọn phiếu nhập kho",
     "—",
     "- Cửa sổ \"Phiếu nhập kho\" chỉ có NK-1\n"
     "- Cột STT, Mã phiếu, Người tạo, Ngày tạo"),

    ("027", "Chọn phiếu nhập điền dữ liệu", "P0",
     NK1 + "\nNK-1 người giao hàng \"Anh Bình\"",
     "1. Bấm kính lúp, chọn NK-1",
     "—",
     "- Cửa sổ đóng; ô phiếu nhập kho = NK-1; Người lập = TK-1; Người giao hàng = Anh Bình\n"
     "- Tab Hàng hóa: H1 Tổng SL 10, P1 = 6, P2 = 4; H2 ĐVT Thùng Tổng SL 2, P3 = 2"),

    ("028", "Phiếu nhập có phụ lục hợp đồng hiện thêm tab", "P1",
     "NK-4 Không duyệt do TK-1 lập, nhập cho hợp đồng HD-01 có phụ lục \"PL 01\"",
     "1. Chọn NK-4",
     "—",
     "- Ngoài tab Hàng hóa có thêm tab \"PL 01\" liệt kê hàng và SL của phụ lục"),

    ("029", "Tìm phiếu trong cửa sổ theo mã", "P2",
     "TK-1 có NK-1, NK-5 đều Không duyệt",
     "1. Mở cửa sổ, nhập mã NK-5",
     "—",
     "- Chỉ còn NK-5"),

    ("030", "Đổi sang phiếu nhập khác", "P1",
     "TK-1 có NK-1 và NK-5 Không duyệt",
     "1. Chọn NK-1\n"
     "2. Mở lại cửa sổ, chọn NK-5",
     "—",
     "- Ô phiếu, người giao hàng và bảng hàng đổi hết theo NK-5, không còn hàng của NK-1"),

    ("031", "Không sửa được số lượng, vị trí khi tạo", "P0",
     NK1,
     "1. Chọn NK-1\n"
     "2. Thử bấm vào ô SL, Vị trí trong bảng",
     "—",
     "- Không có ô nhập; số lượng và vị trí lấy y nguyên từ phiếu nhập"),

    ("032", "Bấm Hủy ở form tạo", "P2",
     "Đang ở form tạo",
     "1. Bấm Hủy",
     "—",
     "- Mong đợi: quay về danh sách phiếu xuất lại\n"
     "- Lưu ý: theo code hiện tại chuyển sang danh sách Phiếu xuất kho - ghi Failed nếu nghiệp vụ yêu cầu "
     "về danh sách phiếu xuất lại"),
]
