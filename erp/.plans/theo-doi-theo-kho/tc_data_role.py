# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Theo doi theo kho'."""

MENU = "Bấm menu \"Theo dõi theo kho\" trên thanh menu chính"

# Danh muc kho mau
KHO = ("Danh mục kho:\n"
       "- K1 \"Kho Hà Nội\", nhóm Kho thành phẩm, công ty TPE, Hoạt động, thủ kho QL-1\n"
       "- K2 \"Kho Bắc Ninh\", nhóm Kho vật tư, công ty TPE, Hoạt động, thủ kho TK-2\n"
       "- K4 \"Kho cũ\", nhóm Kho vật tư, công ty TPE, Khóa\n"
       "- K5 \"Kho HCM\", nhóm Kho thành phẩm, công ty TPC, Hoạt động")

# Du lieu de nghi mau (hom nay 30/10/2026)
DATA = ("Các đề nghị đã được kế toán kho gửi thủ kho:\n"
        "- DX-01: xuất kho K1, Xuất hàng thường, người yêu cầu NV-B, Công ty vận chuyển; nhận 08:00 hôm nay, "
        "duyệt 08:05, hoàn thành 08:35\n"
        "- DX-02: xuất kho K1, Xuất mượn, NV-C, Tự vận chuyển; nhận 09:00 hôm nay, chưa duyệt\n"
        "- DN-01: nhập kho K1, Nhập hàng mua trong nước, NV-D; nhận 08:30 hôm nay, duyệt 08:40, chưa hoàn thành\n"
        "- DX-04: xuất kho K1, Xuất hàng thường, NV-B; nhận 15:00 hôm qua, duyệt 15:10 hôm qua, chưa hoàn thành\n"
        "- DX-05: xuất kho K1; nhận và hoàn thành hôm qua\n"
        "- DX-03: xuất kho K2; nhận 08:15 hôm nay, chưa duyệt")

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Theo dõi theo kho (tiêu đề \"Theo dõi hoạt động kho\"): danh sách kho để người quản lý chọn một kho và "
     "xem trực tiếp hoạt động nhập / xuất của riêng kho đó.\n"
     "Bấm Mã hoặc Tên kho mở tab mới \"Hoạt động nhập/xuất kho <mã> - <tên>\": các đề nghị xuất kho và đề nghị "
     "nhập kho đã gửi thủ kho của kho đó, đã nhận lúc nào, duyệt lúc nào, hoàn thành lúc nào, mất bao lâu; "
     "bảng tự cập nhật kèm âm báo.\n"
     "Màn chỉ xem: không thêm, sửa, xóa kho, không xuất file."),

    ("2. Đối tượng được tính / hiển thị",
     "- Danh sách kho: mọi kho của công ty người dùng, cả kho Hoạt động lẫn kho Khóa; Tổng giám đốc thấy kho "
     "của mọi công ty.\n"
     "- Bảng hoạt động của kho: đề nghị xuất / nhập của đúng kho đó, đang chờ thủ kho duyệt hoặc đã duyệt "
     "chưa hoàn thành (kể cả nhận từ hôm trước), cộng các đề nghị đã hoàn thành có Thời gian nhận hôm nay."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Danh sách kho: kho của công ty khác (trừ Tổng giám đốc).\n"
     "- Bảng hoạt động: đề nghị của kho khác; đề nghị bị thủ kho từ chối hoặc đã hủy; đề nghị kế toán chưa gửi "
     "thủ kho; đề nghị đã hoàn thành nhưng nhận từ hôm trước."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Không có bộ lọc thời gian. Mốc \"hôm nay\" chỉ dùng để giữ lại đề nghị đã hoàn thành có Thời gian nhận "
     "trong ngày."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Danh sách kho: STT, Mã, Tên, Nhóm, Công ty; dưới tiêu đề cột có ô gõ tìm Mã, Tên (bấm Enter) và ô chọn "
     "Nhóm, Công ty; phân trang, chọn số dòng mỗi trang; sắp xếp được theo Mã, Tên.\n"
     "Bảng hoạt động: khung tổng (Tổng số phiếu nhận, Tổng hoàn thành chữ xanh, Tổng chưa xử lý chữ đỏ) và "
     "bảng STT, Phiếu đề nghị, Loại, Người yêu cầu, Hình thức vận chuyển, Kho, Thời gian nhận, Thời gian "
     "lấy/xếp hàng, Thời gian hoàn thành, Trạng thái, Tổng thời gian xử lý.\n"
     "Trạng thái: \"Đã nhận đề nghị\", \"Đang lấy hàng\" (xuất đã duyệt), \"Đang xếp hàng\" (nhập đã duyệt), "
     "\"Đã hoàn thành\"."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Mỗi đề nghị là 1 dòng; đề nghị xuất và nhập trùng số thứ tự vẫn là 2 dòng.\n"
     "- Tổng thời gian xử lý = Thời gian hoàn thành trừ Thời gian nhận, dạng \"x ngày y giờ z phút\" (bỏ phần "
     "bằng 0), dưới 1 phút ghi \"Vài giây\", chưa hoàn thành để trống.\n"
     "Với dữ liệu mẫu: DX-01 = \"35 phút\"."),

    ("7. Phân quyền cấp",
     "- Danh sách kho và bảng hoạt động từng kho cần quyền \"Quản lý kho\"; không có quyền thì ra trang không "
     "tìm thấy.\n"
     "- Có quyền thì xem được bảng hoạt động của mọi kho trong danh sách, không cần là thủ kho.\n"
     "- Tự cập nhật trực tiếp chỉ nhận thay đổi của kho mà người dùng là thủ kho."),

    ("8. Cách tính các ô thống kê",
     "- Tổng số phiếu nhận = số dòng; Tổng hoàn thành = số dòng Đã hoàn thành; Tổng chưa xử lý = hiệu hai số.\n"
     "- Khi mở: dòng chưa hoàn thành lên trên, rồi dòng đã hoàn thành; trong mỗi nhóm Thời gian nhận mới nhất "
     "lên trước. Dòng hoàn thành trong lúc đang mở giữ nguyên chỗ cho tới khi tải lại.\n"
     "- Màu: hoàn thành nền xanh lá; chưa hoàn thành nhận quá 10 phút nền vàng, quá 20 phút nền đỏ (tính lại "
     "mỗi phút); dòng vừa thay đổi nhấp nháy xanh khoảng 10 giây.\n"
     "Với dữ liệu mẫu, bảng kho K1 lúc 09:05: Tổng số phiếu nhận 4, Tổng hoàn thành 1, Tổng chưa xử lý 3."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- Dán đường dẫn bảng hoạt động của kho công ty khác vẫn mở được dù danh sách không có kho đó.\n"
     "- Ô chọn Công ty liệt kê mọi công ty, chọn công ty khác thì danh sách trống.\n"
     "- Kho không phụ trách: bảng không tự cập nhật, phải tải lại.\n"
     "- Bảng đang trống mà có đề nghị mới: tổng tăng nhưng dòng không hiện.\n"
     "- Đề nghị nhận hôm qua, hoàn thành hôm nay: tải lại thì biến mất.\n"
     "- Đề nghị nhập vừa hoàn thành: Tổng thời gian xử lý tự cập nhật tính từ lúc duyệt, tải lại tính từ lúc "
     "nhận."),
]


ROLE_TCS = [
    ("00", "Không có quyền Quản lý kho thì không mở được màn", "P0",
     "NV-A không có quyền \"Quản lý kho\"",
     "1. Đăng nhập NV-A\n"
     "2. " + MENU,
     "Tài khoản: NV-A",
     "- Ra trang không tìm thấy"),

    ("01", "Có quyền Quản lý kho mở được màn", "P0",
     "QL-1 có quyền \"Quản lý kho\", thuộc TPE; " + KHO,
     "1. Đăng nhập QL-1\n"
     "2. " + MENU,
     "Tài khoản: QL-1",
     "- Mở màn \"Theo dõi hoạt động kho\", có danh sách kho"),

    ("02", "Thủ kho không có quyền Quản lý kho cũng không mở được", "P0",
     "TK-2 là thủ kho K2, không có quyền \"Quản lý kho\"",
     "1. Đăng nhập TK-2, " + MENU,
     "Tài khoản: TK-2",
     "- Ra trang không tìm thấy (thủ kho dùng màn Hoạt động kho)"),

    ("03", "Dán đường dẫn bảng hoạt động một kho khi không có quyền", "P0",
     "NV-A không có quyền \"Quản lý kho\"; QL-1 đã copy đường dẫn bảng hoạt động kho K1",
     "1. Đăng nhập NV-A, dán đường dẫn",
     "Tài khoản: NV-A",
     "- Ra trang không tìm thấy, không thấy đề nghị nào của K1"),

    ("04", "Có quyền nhưng không phải thủ kho vẫn xem được kho", "P0",
     "QL-1 có quyền \"Quản lý kho\", không phải thủ kho K2; " + KHO + "\n" + DATA,
     "1. Đăng nhập QL-1, " + MENU + "\n"
     "2. Bấm mã kho K2",
     "—",
     "- Mở tab mới \"Hoạt động nhập/xuất kho K2 - Kho Bắc Ninh\"\n"
     "- Bảng có DX-03"),

    ("05", "Dán đường dẫn bảng hoạt động của kho công ty khác", "P1",
     "QL-1 có quyền \"Quản lý kho\", thuộc TPE (không phải Tổng giám đốc); có sẵn đường dẫn bảng hoạt động kho "
     "K5 của TPC",
     "1. Đăng nhập QL-1, dán đường dẫn",
     "—",
     "- Mong đợi: không mở được vì K5 không có trong danh sách kho của QL-1\n"
     "- Lưu ý: theo code hiện tại vẫn mở được và thấy đề nghị của K5 - ghi Failed"),

    ("06", "Bị gỡ quyền khi đang mở màn", "P1",
     "QL-1 đang mở danh sách kho; quản trị gỡ quyền \"Quản lý kho\" của QL-1",
     "1. QL-1 bấm sang trang 2 của danh sách\n"
     "2. Bấm tên một kho",
     "—",
     "- Bước 1: không tải được trang 2\n"
     "- Bước 2: tab mới ra trang không tìm thấy"),
]
