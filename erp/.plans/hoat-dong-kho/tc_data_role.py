# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Hoat dong kho'."""

MENU = "Bấm menu \"Hoạt động kho\" trên thanh menu chính"
MENU_KHO = "Bấm menu \"Theo dõi theo kho\" trên thanh menu chính"

# Du lieu mau dung chung (hom nay 27/10/2026)
DATA = ("Thủ kho TK-1 phụ trách kho K1, K2 (không phụ trách K3). Các đề nghị đã được kế toán kho gửi thủ kho:\n"
        "- DX-01: xuất kho K1, Xuất hàng thường, người yêu cầu NV-B, Công ty vận chuyển; nhận 08:00 hôm nay, "
        "thủ kho duyệt 08:05, hoàn thành 08:35\n"
        "- DX-02: xuất kho K1, Xuất mượn, NV-C, Tự vận chuyển; nhận 09:00 hôm nay, chưa duyệt\n"
        "- DN-01: nhập kho K2, Nhập hàng mua trong nước, NV-D; nhận 08:30 hôm nay, duyệt 08:40, chưa hoàn thành\n"
        "- DX-04: xuất kho K1, Xuất hàng thường, NV-B; nhận 15:00 hôm qua, duyệt 15:10 hôm qua, chưa hoàn thành\n"
        "- DX-05: xuất kho K1; nhận và hoàn thành hôm qua\n"
        "- DX-03: xuất kho K3; nhận 08:15 hôm nay")

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Hoạt động kho (tiêu đề \"Hoạt động nhập/xuất\"): bảng theo dõi trực tiếp các đề nghị xuất kho và đề nghị "
     "nhập kho đã gửi tới thủ kho của các kho mà người dùng phụ trách: đã nhận lúc nào, thủ kho duyệt (bắt đầu "
     "lấy / xếp hàng) lúc nào, hoàn thành lúc nào, mất bao lâu. Màn tự cập nhật khi có thay đổi, không cần tải "
     "lại trang, kèm âm báo.\n"
     "Màn \"Theo dõi theo kho\": danh sách kho, bấm mã hoặc tên kho để mở bảng hoạt động của riêng kho đó.\n"
     "Màn chỉ xem, không có bộ lọc, không phân trang, không xuất file."),

    ("2. Đối tượng được tính / hiển thị",
     "- Đề nghị xuất kho và đề nghị nhập kho thuộc kho mà người dùng là thủ kho (tài khoản quản trị cao nhất "
     "thấy mọi kho).\n"
     "- Đề nghị đang chờ thủ kho duyệt hoặc đã duyệt nhưng chưa hoàn thành: luôn hiện, kể cả nhận từ những "
     "ngày trước.\n"
     "- Đề nghị đã hoàn thành: chỉ hiện nếu Thời gian nhận là hôm nay."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Đề nghị của kho người dùng không phụ trách.\n"
     "- Đề nghị bị thủ kho từ chối hoặc đã hủy.\n"
     "- Đề nghị đã hoàn thành nhưng nhận từ hôm trước.\n"
     "- Đề nghị kế toán chưa gửi thủ kho."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Không có bộ lọc. Mốc \"hôm nay\" chỉ dùng để giữ lại các đề nghị đã hoàn thành có Thời gian nhận trong "
     "ngày."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Khung tổng: Tổng số phiếu nhận, Tổng hoàn thành (chữ xanh), Tổng chưa xử lý (chữ đỏ).\n"
     "Bảng: STT, Phiếu đề nghị (số phiếu), Loại (loại xuất / loại nhập), Người yêu cầu (người lập yêu cầu "
     "xuất / nhập hàng gốc), Hình thức vận chuyển (chỉ đề nghị xuất), Kho (mã - tên), Thời gian nhận, Thời "
     "gian lấy/xếp hàng, Thời gian hoàn thành, Trạng thái, Tổng thời gian xử lý. Ngày giờ dạng "
     "ngày/tháng/năm giờ:phút:giây.\n"
     "Trạng thái: \"Đã nhận đề nghị\" (chưa duyệt), \"Đang lấy hàng\" (đề nghị xuất đã duyệt) hoặc \"Đang xếp "
     "hàng\" (đề nghị nhập đã duyệt), \"Đã hoàn thành\" (phiếu xuất / nhập kho đã hoàn thành)."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Mỗi đề nghị là 1 dòng; đề nghị xuất và nhập trùng số thứ tự vẫn là 2 dòng riêng.\n"
     "- Tổng thời gian xử lý = Thời gian hoàn thành trừ Thời gian nhận, ghi dạng \"x ngày y giờ z phút\" (bỏ "
     "phần bằng 0); dưới 1 phút ghi \"Vài giây\"; chưa hoàn thành thì để trống.\n"
     "Với dữ liệu mẫu: DX-01 = \"35 phút\"."),

    ("7. Phân quyền cấp",
     "- Màn Hoạt động kho: mọi tài khoản đăng nhập mở được; chỉ thấy đề nghị của kho mình là thủ kho. Không "
     "phải thủ kho kho nào thì bảng trống.\n"
     "- Màn Theo dõi theo kho và bảng hoạt động từng kho: cần quyền \"Quản lý kho\"; xem được mọi kho.\n"
     "- Tự cập nhật trực tiếp chỉ nhận thay đổi của kho mà người dùng là thủ kho."),

    ("8. Cách tính các ô thống kê",
     "- Tổng số phiếu nhận = số dòng đang hiện; Tổng hoàn thành = số dòng Đã hoàn thành; Tổng chưa xử lý = "
     "hiệu hai số trên.\n"
     "- Sắp xếp: dòng chưa hoàn thành lên trên, rồi tới dòng đã hoàn thành; trong mỗi nhóm Thời gian nhận mới "
     "nhất lên trước.\n"
     "- Màu: dòng hoàn thành nền xanh lá; dòng chưa hoàn thành nhận quá 10 phút nền vàng, quá 20 phút nền đỏ "
     "(tự đổi màu mỗi phút).\n"
     "- Dòng vừa thay đổi nhấp nháy xanh khoảng 10 giây.\n"
     "Với dữ liệu mẫu, TK-1 lúc 09:05: Tổng số phiếu nhận 4, Tổng hoàn thành 1, Tổng chưa xử lý 3."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- Đề nghị nhận hôm qua nhưng hoàn thành hôm nay: tải lại trang thì biến mất.\n"
     "- Đề nghị nhập vừa hoàn thành: Tổng thời gian xử lý tự cập nhật tính từ lúc duyệt; tải lại trang lại "
     "tính từ lúc nhận, hai số khác nhau.\n"
     "- Bảng đang trống mà có đề nghị mới gửi tới: tổng số tăng nhưng dòng không hiện cho tới khi tải lại.\n"
     "- Màn Theo dõi theo kho của kho mình không phụ trách: không tự cập nhật.\n"
     "- Mới được phân làm thủ kho: phải đăng nhập lại mới nhận tự cập nhật."),
]


ROLE_TCS = [
    ("00", "Không phải thủ kho kho nào thì bảng trống", "P0",
     "NV-A đăng nhập được, không phụ trách kho nào; " + DATA,
     "1. Đăng nhập NV-A\n"
     "2. " + MENU,
     "Tài khoản: NV-A",
     "- Mở được màn \"Hoạt động nhập/xuất\"\n"
     "- Bảng không có dòng nào; Tổng số phiếu nhận 0, Tổng hoàn thành 0, Tổng chưa xử lý 0"),

    ("01", "Thủ kho chỉ thấy đề nghị của kho mình phụ trách", "P0",
     DATA,
     "1. Đăng nhập TK-1 lúc 09:05\n"
     "2. " + MENU,
     "Tài khoản: TK-1",
     "- Có DX-01, DX-02, DN-01, DX-04\n"
     "- Không có DX-03 (kho K3), không có DX-05"),

    ("02", "Thủ kho kho khác không thấy đề nghị của K1, K2", "P0",
     "TK-2 chỉ phụ trách K3; " + DATA,
     "1. Đăng nhập TK-2, " + MENU,
     "Tài khoản: TK-2",
     "- Chỉ có DX-03; Tổng số phiếu nhận 1, Tổng chưa xử lý 1"),

    ("03", "Tài khoản quản trị cao nhất thấy mọi kho", "P1",
     "QT-1 là quản trị cao nhất; " + DATA,
     "1. Đăng nhập QT-1, " + MENU,
     "Tài khoản: QT-1",
     "- Có DX-01, DX-02, DN-01, DX-04, DX-03; Tổng số phiếu nhận 5"),

    ("04", "Không có quyền Quản lý kho thì không mở được Theo dõi theo kho", "P0",
     "TK-1 không có quyền \"Quản lý kho\"",
     "1. Đăng nhập TK-1\n"
     "2. " + MENU_KHO,
     "Tài khoản: TK-1",
     "- Ra trang không tìm thấy"),

    ("05", "Mở thẳng bảng hoạt động một kho khi không có quyền Quản lý kho", "P1",
     "TK-1 không có quyền \"Quản lý kho\"; QL-1 đã copy đường dẫn bảng hoạt động kho K1",
     "1. Đăng nhập TK-1, dán đường dẫn",
     "—",
     "- Không mở được, giống TC trên"),

    ("06", "Có quyền Quản lý kho xem được kho không phụ trách", "P1",
     "QL-1 có quyền \"Quản lý kho\", không phải thủ kho K3; " + DATA,
     "1. Đăng nhập QL-1, " + MENU_KHO + "\n"
     "2. Bấm mã kho K3",
     "—",
     "- Mở tab mới, tiêu đề có mã và tên kho K3\n"
     "- Bảng có DX-03"),
]
