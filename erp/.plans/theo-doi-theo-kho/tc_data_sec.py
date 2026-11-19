# -*- coding: utf-8 -*-
"""Section I - IX cho man Theo doi theo kho."""
from tc_data_role import MENU, KHO, DATA

OPEN_LIST = "Đăng nhập QL-1, " + MENU
OPEN_K1 = "Đăng nhập QL-1 lúc 09:05, " + MENU + ", bấm tên kho K1"
PRE = "QL-1 có quyền \"Quản lý kho\", thuộc TPE, là thủ kho K1; "
LIVE = ("Trình duyệt A: QL-1 (thủ kho K1) đang mở bảng hoạt động kho K1. Trình duyệt B: kế toán kho KT-A và "
        "thủ kho thao tác trên đề nghị")

SEC_I = [
    ("001", "Bố cục danh sách kho", "P0",
     PRE + KHO,
     "1. " + OPEN_LIST + "\n"
     "2. Quan sát",
     "—",
     "- Tiêu đề trang \"Theo dõi hoạt động kho\"\n"
     "- Bảng có cột STT, Mã, Tên, Nhóm, Công ty\n"
     "- Dưới tiêu đề: ô gõ ở cột Mã, Tên; ô chọn ở cột Nhóm, Công ty\n"
     "- Không có nút Thêm mới, Sửa, Xóa, Xuất file"),

    ("002", "Dữ liệu từng cột của một kho", "P0",
     PRE + KHO,
     "1. " + OPEN_LIST + "\n"
     "2. Xem dòng kho K1",
     "—",
     "- Mã K1, Tên \"Kho Hà Nội\", Nhóm \"Kho thành phẩm\", Công ty TPE\n"
     "- Mã và Tên là đường dẫn bấm được"),

    ("003", "Kho chưa gán nhóm", "P2",
     PRE + "kho K6 của TPE chưa chọn nhóm",
     "1. " + OPEN_LIST,
     "—",
     "- Dòng K6 cột Nhóm để trống, không báo lỗi"),

    ("004", "Thứ tự mặc định", "P1",
     PRE + "K5 tạo trước, K1 tạo sau, K2 tạo mới nhất",
     "1. " + OPEN_LIST,
     "—",
     "- Kho tạo mới nhất ở trên cùng: K2, K1, ...; STT tăng dần từ 1"),

    ("005", "Kho mới tạo xuất hiện trong danh sách", "P1",
     PRE + KHO,
     "1. Vào danh mục kho tạo kho K7 cho TPE\n"
     "2. " + MENU,
     "—",
     "- K7 ở đầu danh sách"),
]


SEC_II = [
    ("001", "Tìm theo Mã", "P0",
     PRE + KHO,
     "1. " + OPEN_LIST + "\n"
     "2. Gõ \"K1\" vào ô dưới cột Mã, bấm Enter",
     "Mã: K1",
     "- Chỉ còn các kho có mã chứa \"K1\""),

    ("002", "Tìm theo một phần Tên", "P0",
     PRE + KHO,
     "1. " + OPEN_LIST + "\n"
     "2. Gõ \"Bắc\" vào ô dưới cột Tên, bấm Enter",
     "Tên: Bắc",
     "- Chỉ còn K2 \"Kho Bắc Ninh\""),

    ("003", "Gõ mà chưa bấm Enter", "P2",
     PRE + KHO,
     "1. " + OPEN_LIST + "\n"
     "2. Gõ \"K2\" vào ô Mã, không bấm Enter",
     "—",
     "- Danh sách chưa đổi; bấm Enter thì mới lọc"),

    ("004", "Lọc theo Nhóm", "P1",
     PRE + KHO,
     "1. " + OPEN_LIST + "\n"
     "2. Chọn Nhóm \"Kho vật tư\"",
     "—",
     "- Chỉ còn K2, K4"),

    ("005", "Lọc theo Công ty của mình", "P1",
     PRE + KHO,
     "1. " + OPEN_LIST + "\n"
     "2. Chọn Công ty TPE",
     "—",
     "- Còn K1, K2, K4"),

    ("006", "Ô Công ty liệt kê công ty không được xem", "P2",
     PRE + KHO + "\nQL-1 không phải Tổng giám đốc",
     "1. " + OPEN_LIST + "\n"
     "2. Mở ô chọn Công ty, chọn TPC",
     "—",
     "- Mong đợi: ô chỉ có công ty QL-1 được xem\n"
     "- Lưu ý: theo code hiện tại ô có mọi công ty, chọn TPC thì danh sách trống - ghi Failed nếu nghiệp vụ "
     "không chấp nhận"),

    ("007", "Kết hợp nhiều điều kiện", "P1",
     PRE + KHO,
     "1. " + OPEN_LIST + "\n"
     "2. Chọn Nhóm \"Kho thành phẩm\", gõ Tên \"Hà\", bấm Enter",
     "—",
     "- Chỉ còn K1"),

    ("008", "Không có kết quả", "P1",
     PRE + KHO,
     "1. " + OPEN_LIST + "\n"
     "2. Gõ Mã \"ZZZ\", bấm Enter",
     "—",
     "- Bảng báo không có dữ liệu, không lỗi"),

    ("009", "Bỏ điều kiện tìm", "P2",
     PRE + KHO,
     "1. Đang lọc Mã \"K1\"\n"
     "2. Xóa chữ trong ô Mã, bấm Enter",
     "—",
     "- Hiện lại đủ kho"),

    ("010", "Sắp xếp theo Mã, Tên", "P2",
     PRE + KHO,
     "1. " + OPEN_LIST + "\n"
     "2. Bấm tiêu đề cột Mã, bấm lần nữa\n"
     "3. Bấm tiêu đề cột Tên",
     "—",
     "- Bước 2: Mã tăng dần rồi giảm dần\n"
     "- Bước 3: Tên theo A đến Z\n"
     "- Cột Nhóm, Công ty, STT không sắp xếp được"),

    ("011", "Phân trang và số dòng mỗi trang", "P1",
     PRE + "TPE có 25 kho",
     "1. " + OPEN_LIST + "\n"
     "2. Bấm sang trang 2\n"
     "3. Đổi \"Xem ... mục\" sang 50",
     "—",
     "- Bước 2: STT tiếp nối trang trước\n"
     "- Bước 3: cả 25 kho trên một trang"),

    ("012", "Ký tự đặc biệt trong ô tìm", "P2",
     PRE + KHO,
     "1. Gõ Tên \"%'\", bấm Enter",
     "Tên: %'",
     "- Không lỗi, bảng trống hoặc chỉ ra kho có đúng các ký tự đó"),
]


SEC_III = [
    ("001", "Chỉ liệt kê kho của công ty mình", "P0",
     PRE + KHO,
     "1. " + OPEN_LIST,
     "—",
     "- Có K1, K2, K4; không có K5 (TPC)"),

    ("002", "Tổng giám đốc thấy kho mọi công ty", "P0",
     "TGD-1 là Tổng giám đốc, có quyền \"Quản lý kho\"; " + KHO,
     "1. Đăng nhập TGD-1, " + MENU,
     "Tài khoản: TGD-1",
     "- Có K1, K2, K4, K5"),

    ("003", "Kho bị Khóa vẫn có trong danh sách", "P1",
     PRE + KHO,
     "1. " + OPEN_LIST,
     "—",
     "- Có K4 \"Kho cũ\" (đang Khóa); danh sách không có cột Trạng thái nên không phân biệt được kho Khóa"),

    ("004", "Chuyển công ty thì danh sách đổi theo", "P1",
     PRE + KHO,
     "1. Quản trị chuyển QL-1 sang TPC\n"
     "2. QL-1 tải lại màn",
     "—",
     "- Chỉ còn K5"),

    ("005", "Sửa tên kho ở danh mục", "P2",
     PRE + KHO,
     "1. Vào danh mục kho đổi tên K1 thành \"Kho Hà Nội 1\"\n"
     "2. Tải lại màn Theo dõi theo kho",
     "—",
     "- Dòng K1 hiện tên mới"),
]


SEC_IV = [
    ("001", "Bấm Tên kho mở bảng hoạt động", "P0",
     PRE + KHO + "\n" + DATA,
     "1. " + OPEN_LIST + "\n"
     "2. Bấm tên \"Kho Hà Nội\"",
     "—",
     "- Mở tab mới, danh sách kho vẫn ở tab cũ\n"
     "- Tiêu đề \"Hoạt động nhập/xuất kho K1 - Kho Hà Nội\""),

    ("002", "Bấm Mã kho mở cùng bảng", "P0",
     PRE + KHO + "\n" + DATA,
     "1. " + OPEN_LIST + "\n"
     "2. Bấm mã K1",
     "—",
     "- Giống bấm Tên: tab mới, cùng tiêu đề và cùng dữ liệu"),

    ("003", "Bố cục bảng hoạt động", "P0",
     PRE + DATA,
     "1. " + OPEN_K1,
     "—",
     "- Khung tổng bên phải: Tổng số phiếu nhận, Tổng hoàn thành (chữ xanh), Tổng chưa xử lý (chữ đỏ)\n"
     "- Bảng có cột STT, Phiếu đề nghị, Loại, Người yêu cầu, Hình thức vận chuyển, Kho, Thời gian nhận, Thời "
     "gian lấy/xếp hàng, Thời gian hoàn thành, Trạng thái, Tổng thời gian xử lý\n"
     "- Không có bộ lọc, phân trang, xuất file"),

    ("004", "Mở 2 kho cùng lúc", "P1",
     PRE + DATA,
     "1. " + OPEN_LIST + "\n"
     "2. Bấm K1, quay lại tab danh sách bấm K2",
     "—",
     "- 2 tab riêng: tab K1 có các đề nghị K1, tab K2 có DX-03; không lẫn"),

    ("005", "Kho không có đề nghị nào", "P1",
     PRE + KHO + "; K4 không có đề nghị",
     "1. " + OPEN_LIST + ", bấm K4",
     "—",
     "- Bảng trống; Tổng số phiếu nhận 0, Tổng hoàn thành 0, Tổng chưa xử lý 0"),

    ("006", "Đường dẫn kho không tồn tại", "P2",
     PRE + "có đường dẫn bảng hoạt động của một kho đã bị xóa hẳn",
     "1. Dán đường dẫn",
     "—",
     "- Ra trang không tìm thấy, không lỗi hệ thống"),

    ("007", "Tiêu đề cột đứng yên khi cuộn", "P2",
     PRE + "kho K1 có hơn 30 đề nghị đang hiện",
     "1. " + OPEN_K1 + ", cuộn xuống cuối",
     "—",
     "- Dòng tiêu đề cột vẫn ở đầu màn hình"),
]


SEC_V = [
    ("001", "Chỉ có đề nghị của kho đã chọn", "P0",
     PRE + DATA,
     "1. " + OPEN_K1,
     "—",
     "- Có DX-01, DX-02, DN-01, DX-04\n"
     "- Không có DX-03 (kho K2)\n"
     "- Cột Kho mọi dòng là \"K1 - Kho Hà Nội\""),

    ("002", "Đề nghị chờ duyệt hiện", "P0",
     PRE + DATA,
     "1. " + OPEN_K1,
     "—",
     "- DX-02 hiện, Trạng thái \"Đã nhận đề nghị\""),

    ("003", "Đề nghị đã duyệt từ hôm trước vẫn hiện", "P0",
     PRE + DATA,
     "1. " + OPEN_K1,
     "—",
     "- DX-04 hiện, Thời gian nhận ngày hôm qua 15:00:00, Trạng thái \"Đang lấy hàng\""),

    ("004", "Đề nghị hoàn thành trong ngày hiện", "P0",
     PRE + DATA,
     "1. " + OPEN_K1,
     "—",
     "- DX-01 hiện, Trạng thái \"Đã hoàn thành\""),

    ("005", "Đề nghị hoàn thành từ hôm qua không hiện", "P0",
     PRE + DATA,
     "1. " + OPEN_K1,
     "—",
     "- Không có DX-05"),

    ("006", "Đề nghị nhận hôm qua, hoàn thành hôm nay", "P1",
     PRE + "DX-06 kho K1 nhận 16:00 hôm qua, hoàn thành 08:10 hôm nay",
     "1. " + OPEN_K1,
     "—",
     "- Mong đợi: DX-06 hiện vì hoàn thành trong ngày\n"
     "- Lưu ý: theo code hiện tại không hiện - ghi Failed nếu nghiệp vụ cần thấy"),

    ("007", "Đề nghị bị thủ kho từ chối không hiện", "P0",
     PRE + "DX-07 kho K1 đã gửi thủ kho rồi bị từ chối",
     "1. " + OPEN_K1,
     "—",
     "- Không có DX-07"),

    ("008", "Đề nghị đã hủy không hiện", "P0",
     PRE + "DX-08 kho K1 đã hủy",
     "1. " + OPEN_K1,
     "—",
     "- Không có DX-08"),

    ("009", "Đề nghị kế toán chưa gửi thủ kho không hiện", "P0",
     PRE + "DX-09 kho K1 kế toán mới lưu, chưa gửi thủ kho",
     "1. " + OPEN_K1,
     "—",
     "- Không có DX-09"),

    ("010", "Đề nghị nhập và xuất trùng số thứ tự", "P2",
     PRE + "đề nghị xuất và đề nghị nhập cùng kho K1, cùng số thứ tự nội bộ",
     "1. " + OPEN_K1,
     "—",
     "- Hiện 2 dòng riêng, mỗi dòng đúng số phiếu của mình"),
]


SEC_VI = [
    ("001", "Cột của đề nghị xuất", "P0",
     PRE + DATA,
     "1. " + OPEN_K1 + "\n"
     "2. Xem dòng DX-01",
     "—",
     "- Phiếu đề nghị DX-01, Loại \"Xuất hàng thường\", Người yêu cầu NV-B, Hình thức vận chuyển \"Công ty vận "
     "chuyển\", Kho \"K1 - Kho Hà Nội\"\n"
     "- Thời gian nhận 30/10/2026 08:00:00, Thời gian lấy/xếp hàng 30/10/2026 08:05:00, Thời gian hoàn thành "
     "30/10/2026 08:35:00"),

    ("002", "Cột của đề nghị nhập", "P0",
     PRE + DATA,
     "1. " + OPEN_K1 + "\n"
     "2. Xem dòng DN-01",
     "—",
     "- Loại \"Nhập hàng mua trong nước\", Người yêu cầu NV-D, Hình thức vận chuyển để trống\n"
     "- Thời gian hoàn thành trống, Trạng thái \"Đang xếp hàng\""),

    ("003", "Trạng thái theo từng bước", "P0",
     PRE + DATA,
     "1. " + OPEN_K1,
     "—",
     "- DX-02 \"Đã nhận đề nghị\", DX-04 \"Đang lấy hàng\", DN-01 \"Đang xếp hàng\", DX-01 \"Đã hoàn thành\""),

    ("004", "Người yêu cầu là người lập yêu cầu gốc", "P1",
     PRE + "DX-10 kho K1 do kế toán KT-A lập từ yêu cầu xuất hàng của NV-E, đã gửi thủ kho",
     "1. " + OPEN_K1,
     "—",
     "- Người yêu cầu của DX-10 là NV-E, không phải KT-A"),

    ("005", "Tổng thời gian xử lý của đề nghị đã hoàn thành", "P0",
     PRE + DATA,
     "1. " + OPEN_K1,
     "—",
     "- DX-01: \"35 phút\"\n"
     "- DX-02, DN-01, DX-04: để trống"),

    ("006", "Tổng thời gian có giờ", "P1",
     PRE + "DX-11 kho K1 nhận 07:00, hoàn thành 08:30 hôm nay",
     "1. " + OPEN_K1,
     "—",
     "- DX-11: \"1 giờ 30 phút\""),

    ("007", "Tổng thời gian dưới 1 phút", "P2",
     PRE + "DX-12 kho K1 nhận 08:00:00, hoàn thành 08:00:40 hôm nay",
     "1. " + OPEN_K1,
     "—",
     "- DX-12: \"Vài giây\""),

    ("008", "Đề nghị nhập vừa hoàn thành: tự cập nhật và tải lại", "P1",
     LIVE + "; DN-01 nhận 08:30, duyệt 08:40",
     "1. Trình duyệt B: hoàn thành phiếu nhập kho của DN-01 lúc 09:10\n"
     "2. Trình duyệt A: xem cột Tổng thời gian xử lý của DN-01\n"
     "3. Tải lại trang",
     "—",
     "- Mong đợi: bước 2 và bước 3 cùng \"40 phút\" (tính từ lúc nhận)\n"
     "- Lưu ý: theo code hiện tại bước 2 ra \"30 phút\" (tính từ lúc duyệt) - ghi Failed"),
]


SEC_VII = [
    ("001", "Ô tổng khi mở bảng", "P0",
     PRE + DATA,
     "1. " + OPEN_K1,
     "—",
     "- Tổng số phiếu nhận 4, Tổng hoàn thành 1, Tổng chưa xử lý 3"),

    ("002", "Thứ tự dòng khi mở", "P0",
     PRE + DATA,
     "1. " + OPEN_K1,
     "—",
     "- Thứ tự: DX-02 (09:00), DN-01 (08:30), DX-04 (hôm qua), rồi DX-01 (đã hoàn thành) ở cuối\n"
     "- STT 1 đến 4"),

    ("003", "Màu dòng đã hoàn thành", "P0",
     PRE + DATA,
     "1. " + OPEN_K1,
     "—",
     "- DX-01 nền xanh lá, chữ trắng"),

    ("004", "Màu dòng chờ quá 10 phút", "P0",
     PRE + "DX-13 kho K1 nhận 09:00, chưa hoàn thành",
     "1. Đăng nhập QL-1 lúc 09:15, mở bảng kho K1",
     "—",
     "- DX-13 nền vàng"),

    ("005", "Màu dòng chờ quá 20 phút", "P0",
     PRE + "DX-13 kho K1 nhận 09:00, chưa hoàn thành",
     "1. Đăng nhập QL-1 lúc 09:25, mở bảng kho K1",
     "—",
     "- DX-13 nền đỏ"),

    ("006", "Dòng đổi màu khi để màn mở", "P1",
     PRE + "DX-13 kho K1 nhận 09:00, chưa hoàn thành",
     "1. Mở bảng kho K1 lúc 09:05, để nguyên không tải lại\n"
     "2. Chờ tới 09:12\n"
     "3. Chờ tới 09:22",
     "—",
     "- Bước 1: nền trắng\n"
     "- Bước 2: nền vàng (chậm tối đa 1 phút)\n"
     "- Bước 3: nền đỏ"),

    ("007", "Đúng mốc 10 phút chưa đổi màu", "P2",
     PRE + "DX-13 kho K1 nhận 09:00:00",
     "1. Mở bảng kho K1 lúc 09:10:00",
     "—",
     "- Nền trắng; sang 09:11 mới vàng"),

    ("008", "Dòng chưa hoàn thành từ hôm trước", "P1",
     PRE + DATA,
     "1. " + OPEN_K1,
     "—",
     "- DX-04 nền đỏ"),
]


SEC_VIII = [
    ("001", "Đề nghị mới gửi tới kho đang xem", "P0",
     LIVE + "; " + DATA,
     "1. Trình duyệt B: KT-A gửi thủ kho đề nghị xuất DX-15 kho K1 lúc 09:10\n"
     "2. Trình duyệt A: quan sát, không tải lại",
     "—",
     "- Có âm báo; DX-15 hiện ở đầu bảng, nhấp nháy xanh khoảng 10 giây, Trạng thái \"Đã nhận đề nghị\"\n"
     "- STT đánh lại từ 1; Tổng số phiếu nhận 5, Tổng chưa xử lý 4"),

    ("002", "Đề nghị gửi tới kho khác không vào bảng", "P0",
     LIVE + "; QL-1 cũng là thủ kho K2; " + DATA,
     "1. Trình duyệt B: gửi thủ kho đề nghị nhập DN-02 kho K2",
     "—",
     "- Bảng kho K1 không thêm DN-02, ô tổng không đổi"),

    ("003", "Thủ kho duyệt đề nghị", "P0",
     LIVE + "; " + DATA,
     "1. Trình duyệt B: thủ kho duyệt DX-02 lúc 09:12",
     "—",
     "- Dòng DX-02 nhấp nháy, Thời gian lấy/xếp hàng 30/10/2026 09:12:00, Trạng thái \"Đang lấy hàng\"\n"
     "- Ô tổng không đổi"),

    ("004", "Hoàn thành phiếu xuất kho", "P0",
     LIVE + "; " + DATA,
     "1. Trình duyệt B: hoàn thành phiếu xuất kho của DX-04",
     "—",
     "- DX-04 có Thời gian hoàn thành, Trạng thái \"Đã hoàn thành\", sau khoảng 10 giây nền xanh lá\n"
     "- Dòng giữ nguyên vị trí cho tới khi tải lại\n"
     "- Tổng hoàn thành 2, Tổng chưa xử lý 2"),

    ("005", "Thủ kho từ chối đề nghị", "P0",
     LIVE + "; " + DATA,
     "1. Trình duyệt B: thủ kho từ chối DX-02",
     "—",
     "- DX-02 mất khỏi bảng, STT đánh lại; Tổng số phiếu nhận 3"),

    ("006", "Bảng đang trống có đề nghị mới", "P1",
     "QL-1 là thủ kho K4, đang mở bảng hoạt động kho K4 (bảng trống)",
     "1. Tab khác gửi thủ kho đề nghị xuất DX-16 kho K4\n"
     "2. Quan sát, không tải lại",
     "—",
     "- Mong đợi: DX-16 hiện\n"
     "- Lưu ý: theo code hiện tại Tổng số phiếu nhận thành 1 nhưng bảng vẫn trống tới khi tải lại - ghi Failed"),

    ("007", "Kho không phụ trách không tự cập nhật", "P1",
     "QL-1 có quyền \"Quản lý kho\", không phải thủ kho K2, đang mở bảng hoạt động kho K2",
     "1. Tab khác gửi thủ kho đề nghị xuất DX-17 kho K2\n"
     "2. Quan sát, không tải lại\n"
     "3. Tải lại trang",
     "—",
     "- Bước 2 mong đợi: DX-17 tự hiện; theo code hiện tại không hiện - ghi Failed nếu người quản lý cần theo "
     "dõi trực tiếp\n"
     "- Bước 3: DX-17 hiện"),

    ("008", "Mở cả màn Hoạt động kho và bảng kho K1", "P2",
     LIVE + "; QL-1 mở thêm màn Hoạt động kho ở tab khác",
     "1. Trình duyệt B: gửi thủ kho DX-18 kho K1",
     "—",
     "- Cả 2 tab cùng hiện DX-18, mỗi tab đếm đúng một lần"),

    ("009", "Nhiều thay đổi liên tiếp", "P2",
     LIVE + "; " + DATA,
     "1. Trình duyệt B: trong 5 giây gửi DX-19 kho K1, duyệt DX-02, hoàn thành DN-01",
     "—",
     "- Cả 3 dòng cập nhật đúng; Tổng số phiếu nhận 5, Tổng hoàn thành 2, Tổng chưa xử lý 3"),
]


SEC_IX = [
    ("001", "Người quản lý theo dõi một đề nghị xuất từ đầu tới cuối", "P0",
     LIVE + "; bảng kho K1 đang có ít nhất 1 dòng",
     "1. KT-A lập đề nghị xuất DX-20 kho K1 từ yêu cầu xuất hàng của NV-B, gửi thủ kho lúc 10:00\n"
     "2. Thủ kho duyệt DX-20 lúc 10:05\n"
     "3. Thủ kho hoàn thành phiếu xuất kho lúc 10:25\n"
     "4. Tải lại trang",
     "—",
     "- Sau bước 1: DX-20 ở đầu bảng, \"Đã nhận đề nghị\", Người yêu cầu NV-B\n"
     "- Sau bước 2: \"Đang lấy hàng\", Thời gian lấy/xếp hàng 10:05\n"
     "- Sau bước 3: \"Đã hoàn thành\", Tổng thời gian xử lý \"25 phút\", nền xanh lá\n"
     "- Sau bước 4: DX-20 nằm trong nhóm đã hoàn thành ở cuối bảng"),

    ("002", "Luồng nhập kho đầu - cuối", "P0",
     LIVE + "; bảng kho K1 đang có ít nhất 1 dòng",
     "1. KT-A gửi thủ kho đề nghị nhập DN-20 kho K1 lúc 10:00\n"
     "2. Thủ kho duyệt lúc 10:10\n"
     "3. Thủ kho hoàn thành phiếu nhập kho lúc 10:40\n"
     "4. Tải lại trang",
     "—",
     "- Sau bước 2: \"Đang xếp hàng\"\n"
     "- Sau bước 4: \"Đã hoàn thành\", Tổng thời gian xử lý \"40 phút\""),

    ("003", "Từ chối rồi gửi lại", "P1",
     LIVE,
     "1. KT-A gửi thủ kho DX-21 kho K1\n"
     "2. Thủ kho từ chối DX-21\n"
     "3. KT-A sửa, gửi lại DX-21",
     "—",
     "- Sau bước 2: DX-21 mất khỏi bảng\n"
     "- Sau bước 3: DX-21 hiện lại ở đầu bảng với Thời gian nhận mới, ô tổng đếm một lần"),

    ("004", "Đối chiếu bảng kho với màn Hoạt động kho", "P0",
     PRE + "QL-1 chỉ là thủ kho K1; " + DATA,
     "1. QL-1 mở màn Hoạt động kho\n"
     "2. Mở bảng hoạt động kho K1 ở Theo dõi theo kho",
     "—",
     "- Hai màn có cùng các dòng, cùng ô tổng: 4 / 1 / 3"),

    ("005", "Đối chiếu ô tổng với số dòng", "P0",
     PRE + DATA,
     "1. " + OPEN_K1 + "\n"
     "2. Đếm số dòng và số dòng nền xanh lá",
     "—",
     "- Tổng số phiếu nhận bằng số dòng; Tổng hoàn thành bằng số dòng Đã hoàn thành; Tổng chưa xử lý bằng "
     "hiệu hai số"),

    ("006", "Sang ngày mới", "P1",
     PRE + DATA,
     "1. Ngày 31/10/2026 đăng nhập QL-1, mở bảng kho K1",
     "—",
     "- Không còn DX-01\n"
     "- DX-02, DN-01, DX-04 vẫn hiện nếu chưa hoàn thành"),
]
