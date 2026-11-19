# -*- coding: utf-8 -*-
"""Section I - IX cho man Hoat dong kho."""
from tc_data_role import MENU, MENU_KHO, DATA

OPEN = "Đăng nhập TK-1 lúc 09:05, " + MENU
LIVE = ("Trình duyệt A: TK-1 đang mở màn Hoạt động kho. Trình duyệt B: kế toán kho KT-A và thủ kho TK-1 thao "
        "tác trên đề nghị")

SEC_I = [
    ("001", "Bố cục màn Hoạt động kho", "P0",
     DATA,
     "1. " + OPEN + "\n"
     "2. Quan sát từ trên xuống",
     "—",
     "- Tiêu đề trang \"Hoạt động nhập/xuất\"\n"
     "- Khung tổng bên phải: Tổng số phiếu nhận, Tổng hoàn thành (chữ xanh), Tổng chưa xử lý (chữ đỏ)\n"
     "- Bảng có cột STT, Phiếu đề nghị, Loại, Người yêu cầu, Hình thức vận chuyển, Kho, Thời gian nhận, Thời "
     "gian lấy/xếp hàng, Thời gian hoàn thành, Trạng thái, Tổng thời gian xử lý\n"
     "- Không có bộ lọc, phân trang, nút xuất file"),

    ("002", "Tiêu đề bảng đứng yên khi cuộn", "P2",
     "TK-1 có nhiều hơn 30 đề nghị đang hiện",
     "1. Mở màn, cuộn xuống cuối bảng",
     "—",
     "- Dòng tiêu đề cột vẫn hiện ở đầu màn hình"),

    ("003", "Mở lại màn lấy số liệu mới nhất", "P1",
     DATA,
     "1. " + OPEN + "\n"
     "2. Ở tab khác thủ kho duyệt DX-02\n"
     "3. Tải lại trang Hoạt động kho",
     "—",
     "- DX-02 có Thời gian lấy/xếp hàng, Trạng thái \"Đang lấy hàng\""),
]


SEC_II = [
    ("001", "Đề nghị chờ duyệt luôn hiện", "P0",
     DATA,
     "1. " + OPEN,
     "—",
     "- DX-02 hiện, Trạng thái \"Đã nhận đề nghị\""),

    ("002", "Đề nghị đã duyệt từ hôm trước vẫn hiện", "P0",
     DATA,
     "1. " + OPEN,
     "—",
     "- DX-04 hiện, Thời gian nhận là ngày hôm qua 15:00:00, Trạng thái \"Đang lấy hàng\""),

    ("003", "Đề nghị hoàn thành trong ngày hiện", "P0",
     DATA,
     "1. " + OPEN,
     "—",
     "- DX-01 hiện, Trạng thái \"Đã hoàn thành\""),

    ("004", "Đề nghị hoàn thành từ hôm qua không hiện", "P0",
     DATA,
     "1. " + OPEN,
     "—",
     "- Không có DX-05"),

    ("005", "Đề nghị nhận hôm qua, hoàn thành hôm nay", "P1",
     DATA,
     "1. Ở tab khác hoàn thành phiếu xuất kho của DX-04\n"
     "2. " + OPEN,
     "—",
     "- Mong đợi: DX-04 vẫn hiện vì hoàn thành trong ngày\n"
     "- Lưu ý: theo code hiện tại DX-04 biến mất (chỉ giữ đề nghị hoàn thành có ngày nhận là hôm nay) - "
     "ghi Failed nếu nghiệp vụ cần giữ"),

    ("006", "Đề nghị bị thủ kho từ chối không hiện", "P0",
     "DX-06: xuất kho K1, đã nhận hôm nay, thủ kho TK-1 đã từ chối",
     "1. " + OPEN,
     "—",
     "- Không có DX-06"),

    ("007", "Đề nghị kế toán chưa gửi thủ kho không hiện", "P0",
     "DX-07: đề nghị xuất kho K1 kế toán vừa lưu, chưa gửi thủ kho",
     "1. " + OPEN,
     "—",
     "- Không có DX-07"),

    ("008", "Đề nghị bị từ chối rồi gửi lại thì hiện lại", "P1",
     "DX-06 bị từ chối; kế toán sửa và gửi lại lúc 10:00",
     "1. Đăng nhập TK-1 lúc 10:01, " + MENU,
     "—",
     "- DX-06 hiện, Thời gian nhận 10:00, Trạng thái \"Đã nhận đề nghị\""),

    ("009", "Có cả đề nghị xuất và đề nghị nhập", "P0",
     DATA,
     "1. " + OPEN,
     "—",
     "- DN-01 (đề nghị nhập kho K2) hiện chung bảng với các đề nghị xuất"),
]


SEC_III = [
    ("001", "Cột của đề nghị xuất", "P0",
     DATA,
     "1. " + OPEN + "\n"
     "2. Xem dòng DX-01",
     "—",
     "- Phiếu đề nghị DX-01, Loại \"Xuất hàng thường\", Người yêu cầu NV-B, Hình thức vận chuyển \"Công ty "
     "vận chuyển\", Kho \"K1 - <tên kho K1>\"\n"
     "- Thời gian nhận 27/10/2026 08:00:00, Thời gian lấy/xếp hàng 27/10/2026 08:05:00, Thời gian hoàn thành "
     "27/10/2026 08:35:00"),

    ("002", "Cột của đề nghị nhập", "P0",
     DATA,
     "1. " + OPEN + "\n"
     "2. Xem dòng DN-01",
     "—",
     "- Loại \"Nhập hàng mua trong nước\", Người yêu cầu NV-D, Hình thức vận chuyển để trống, Kho K2\n"
     "- Thời gian lấy/xếp hàng 27/10/2026 08:40:00, Thời gian hoàn thành trống"),

    ("003", "Trạng thái Đã nhận đề nghị", "P0",
     DATA,
     "1. " + OPEN,
     "—",
     "- DX-02: Thời gian lấy/xếp hàng và Thời gian hoàn thành trống, Trạng thái \"Đã nhận đề nghị\""),

    ("004", "Trạng thái Đang lấy hàng của đề nghị xuất", "P0",
     DATA,
     "1. " + OPEN,
     "—",
     "- DX-04 Trạng thái \"Đang lấy hàng\""),

    ("005", "Trạng thái Đang xếp hàng của đề nghị nhập", "P0",
     DATA,
     "1. " + OPEN,
     "—",
     "- DN-01 Trạng thái \"Đang xếp hàng\""),

    ("006", "Trạng thái Đã hoàn thành", "P0",
     DATA,
     "1. " + OPEN,
     "—",
     "- DX-01 Trạng thái \"Đã hoàn thành\", cả dòng nền xanh lá chữ trắng"),

    ("007", "Loại đề nghị khác hiện đúng tên", "P1",
     "Đề nghị xuất kho K1 đang chờ duyệt có các loại: Xuất điều chuyển kho nội bộ, Xuất bảo hành, Xuất bán "
     "hợp đồng; đề nghị nhập loại Nhập hàng bán trả lại",
     "1. " + OPEN,
     "—",
     "- Cột Loại hiện đúng 4 tên trên, màn không lỗi"),

    ("008", "Hình thức vận chuyển Khách hàng vận chuyển", "P2",
     "DX-08: xuất kho K1, yêu cầu xuất hàng chọn Khách hàng vận chuyển, đang chờ duyệt",
     "1. " + OPEN,
     "—",
     "- DX-08 Hình thức vận chuyển \"Khách hàng vận chuyển\""),

    ("009", "Đề nghị không có yêu cầu gốc thì Người yêu cầu trống", "P2",
     "DX-09: đề nghị xuất ghép kho K1 (không đi từ yêu cầu xuất hàng), đang chờ duyệt",
     "1. " + OPEN,
     "—",
     "- DX-09 hiện, Người yêu cầu và Hình thức vận chuyển trống, màn không lỗi"),
]


SEC_IV = [
    ("001", "Tổng thời gian xử lý tính từ lúc nhận tới lúc hoàn thành", "P0",
     DATA,
     "1. " + OPEN,
     "—",
     "- DX-01 Tổng thời gian xử lý \"35 phút\" (từ Thời gian nhận 08:00 tới hoàn thành 08:35)"),

    ("002", "Chưa hoàn thành thì Tổng thời gian xử lý trống", "P0",
     DATA,
     "1. " + OPEN,
     "—",
     "- DX-02, DN-01, DX-04 cột Tổng thời gian xử lý trống"),

    ("003", "Thời gian xử lý qua ngày", "P1",
     LIVE + "; DX-04 nhận 15:00 hôm qua",
     "1. Trình duyệt B: hoàn thành phiếu xuất kho của DX-04 lúc 09:20 hôm nay\n"
     "2. Trình duyệt A: xem dòng DX-04, không tải lại trang",
     "—",
     "- Tổng thời gian xử lý \"18 giờ 20 phút\""),

    ("004", "Hoàn thành trong chưa tới 1 phút", "P2",
     "DX-11: xuất kho K1, nhận 09:00:00, hoàn thành 09:00:40 hôm nay",
     "1. " + MENU,
     "—",
     "- Tổng thời gian xử lý \"Vài giây\""),

    ("005", "Đúng số giờ chẵn không ghi phút", "P2",
     "DX-12: nhận 07:00, hoàn thành 09:00 hôm nay",
     "1. " + MENU,
     "—",
     "- Tổng thời gian xử lý \"2 giờ\""),

    ("006", "Đề nghị nhập: thời gian xử lý lúc tải trang và lúc tự cập nhật phải bằng nhau", "P1",
     LIVE + "; DN-01 nhận 08:30, duyệt 08:40",
     "1. Trình duyệt B: hoàn thành phiếu nhập kho của DN-01 lúc 09:10\n"
     "2. Trình duyệt A: xem Tổng thời gian xử lý của DN-01\n"
     "3. Trình duyệt A: tải lại trang, xem lại",
     "—",
     "- Mong đợi: cả bước 2 và bước 3 đều \"40 phút\"\n"
     "- Lưu ý: theo code hiện tại bước 2 ra \"30 phút\" (tính từ lúc duyệt), bước 3 ra \"40 phút\" - ghi "
     "Failed"),
]


SEC_V = [
    ("001", "Ô tổng khi mở màn", "P0",
     DATA,
     "1. " + OPEN,
     "—",
     "- Tổng số phiếu nhận 4, Tổng hoàn thành 1, Tổng chưa xử lý 3"),

    ("002", "Dòng chưa hoàn thành lên trên, mới nhận lên trước", "P0",
     DATA,
     "1. " + OPEN,
     "—",
     "- Thứ tự: DX-02 (09:00), DN-01 (08:30), DX-04 (hôm qua 15:00), cuối cùng DX-01 (đã hoàn thành)\n"
     "- STT 1 đến 4"),

    ("003", "Nhiều dòng hoàn thành sắp theo Thời gian nhận mới nhất", "P1",
     DATA + "\nThêm DX-13: nhận 08:20 hôm nay, hoàn thành 08:50",
     "1. " + OPEN,
     "—",
     "- Nhóm hoàn thành ở cuối: DX-13 trước, DX-01 sau"),

    ("004", "Không phân trang", "P1",
     "TK-1 có 60 đề nghị đang hiện",
     "1. " + MENU,
     "—",
     "- Cả 60 dòng trên 1 trang, STT 1 đến 60, Tổng số phiếu nhận 60"),
]


SEC_VI = [
    ("001", "Chưa hoàn thành dưới 10 phút không tô màu", "P1",
     "DX-14: nhận lúc 09:00, chưa duyệt",
     "1. Mở màn lúc 09:05",
     "—",
     "- Dòng DX-14 nền trắng"),

    ("002", "Chưa hoàn thành quá 10 phút tô vàng", "P0",
     "DX-14: nhận lúc 09:00, chưa duyệt",
     "1. Mở màn lúc 09:15",
     "—",
     "- Dòng DX-14 nền vàng chữ trắng"),

    ("003", "Chưa hoàn thành quá 20 phút tô đỏ", "P0",
     DATA,
     "1. " + OPEN,
     "—",
     "- DN-01 (nhận 08:30) và DX-04 (nhận hôm qua) nền đỏ chữ trắng"),

    ("004", "Màu tự đổi khi để màn mở", "P1",
     "DX-14: nhận lúc 09:00, chưa duyệt",
     "1. Mở màn lúc 09:05, không tải lại trang\n"
     "2. Quan sát lúc 09:12 và 09:22",
     "—",
     "- 09:12 dòng chuyển vàng; 09:22 chuyển đỏ (trễ tối đa 1 phút)"),

    ("005", "Đã hoàn thành thì không còn vàng / đỏ", "P0",
     LIVE + "; DX-04 đang nền đỏ",
     "1. Trình duyệt B: hoàn thành phiếu xuất kho của DX-04\n"
     "2. Trình duyệt A: chờ khoảng 1 phút",
     "—",
     "- Dòng DX-04 nền xanh lá, không còn đỏ"),
]


SEC_VII = [
    ("001", "Đề nghị mới gửi tự hiện lên đầu bảng", "P0",
     LIVE + "; " + DATA,
     "1. Trình duyệt B: KT-A gửi thủ kho đề nghị xuất DX-15 kho K1 lúc 09:10\n"
     "2. Trình duyệt A: quan sát, không tải lại trang",
     "—",
     "- Có âm báo; DX-15 hiện ở dòng đầu, nhấp nháy xanh khoảng 10 giây, Trạng thái \"Đã nhận đề nghị\"\n"
     "- STT đánh lại 1 đến 5; Tổng số phiếu nhận 5, Tổng chưa xử lý 4"),

    ("002", "Thủ kho duyệt thì dòng tự đổi trạng thái", "P0",
     LIVE + "; " + DATA,
     "1. Trình duyệt B: TK-1 duyệt đề nghị DX-02 lúc 09:12\n"
     "2. Trình duyệt A: quan sát",
     "—",
     "- Dòng DX-02 nhấp nháy, Thời gian lấy/xếp hàng 27/10/2026 09:12, Trạng thái \"Đang lấy hàng\"\n"
     "- Ô tổng không đổi"),

    ("003", "Hoàn thành thì dòng chuyển xuống cuối", "P0",
     LIVE + "; " + DATA,
     "1. Trình duyệt B: hoàn thành phiếu xuất kho của DX-04 lúc 09:15\n"
     "2. Trình duyệt A: quan sát khoảng 10 giây",
     "—",
     "- Dòng DX-04 có Thời gian hoàn thành, Trạng thái \"Đã hoàn thành\", Tổng thời gian xử lý tính từ 15:00 "
     "hôm qua\n"
     "- Sau khoảng 10 giây dòng chuyển xuống cuối bảng, nền xanh lá; STT đánh lại\n"
     "- Tổng hoàn thành 2, Tổng chưa xử lý 2"),

    ("004", "Thủ kho từ chối thì dòng tự mất", "P0",
     LIVE + "; " + DATA,
     "1. Trình duyệt B: TK-1 từ chối DX-02 (nhập lý do)\n"
     "2. Trình duyệt A: quan sát",
     "—",
     "- Có âm báo, dòng DX-02 biến mất; STT đánh lại\n"
     "- Tổng số phiếu nhận 3, Tổng chưa xử lý 2"),

    ("005", "Thay đổi của kho không phụ trách không tới", "P0",
     LIVE + "; " + DATA,
     "1. Trình duyệt B: thủ kho K3 duyệt DX-03\n"
     "2. Trình duyệt A: quan sát",
     "—",
     "- Không có âm báo, bảng và ô tổng không đổi"),

    ("006", "Đề nghị nhập mới tự hiện", "P1",
     LIVE + "; " + DATA,
     "1. Trình duyệt B: KT-A gửi thủ kho đề nghị nhập DN-02 kho K2\n"
     "2. Trình duyệt A: quan sát",
     "—",
     "- DN-02 hiện ở dòng đầu, Loại là loại nhập, Hình thức vận chuyển trống"),

    ("007", "Bảng đang trống nhận đề nghị mới", "P1",
     "Trình duyệt A: TK-2 (kho K3) đang mở màn, bảng trống vì chưa có đề nghị nào",
     "1. Trình duyệt B: gửi thủ kho đề nghị xuất DX-16 kho K3\n"
     "2. Trình duyệt A: quan sát, không tải lại trang",
     "—",
     "- Mong đợi: DX-16 hiện trong bảng; Tổng số phiếu nhận 1\n"
     "- Lưu ý: theo code hiện tại ô tổng lên 1 nhưng bảng vẫn trống, phải tải lại trang mới thấy - ghi "
     "Failed"),

    ("008", "Mới được phân làm thủ kho", "P2",
     "TK-3 đang đăng nhập và mở màn; quản lý vừa thêm TK-3 làm thủ kho K2",
     "1. TK-3 tải lại trang\n"
     "2. Gửi thủ kho đề nghị nhập mới của K2, quan sát màn TK-3",
     "—",
     "- Bước 1: thấy đề nghị của K2\n"
     "- Bước 2: mong đợi tự hiện; nếu chỉ hiện sau khi đăng nhập lại thì ghi nhận lại để nghiệp vụ quyết"),

    ("009", "Nhiều thay đổi liên tiếp", "P2",
     LIVE + "; " + DATA,
     "1. Trình duyệt B: trong 5 giây gửi DX-15, duyệt DX-02, hoàn thành DN-01",
     "—",
     "- Cả 3 dòng cập nhật đúng; ô tổng: Tổng số phiếu nhận 5, Tổng hoàn thành 2, Tổng chưa xử lý 3"),
]


SEC_VIII = [
    ("001", "Danh sách kho ở Theo dõi theo kho", "P0",
     "QL-1 có quyền \"Quản lý kho\"",
     "1. Đăng nhập QL-1\n"
     "2. " + MENU_KHO,
     "—",
     "- Tiêu đề \"Theo dõi hoạt động kho\"\n"
     "- Bảng kho: STT, Mã, Tên, Nhóm, Công ty; có ô tìm theo Mã, Tên và chọn Nhóm, Công ty dưới tiêu đề cột"),

    ("002", "Tìm kho theo mã", "P1",
     "QL-1 có quyền \"Quản lý kho\"",
     "1. " + MENU_KHO + "\n"
     "2. Gõ \"K1\" vào ô dưới cột Mã, bấm Enter",
     "—",
     "- Chỉ còn các kho có mã chứa K1"),

    ("003", "Lọc kho theo công ty", "P2",
     "QL-1 có quyền \"Quản lý kho\"",
     "1. " + MENU_KHO + "\n"
     "2. Chọn Công ty TPE",
     "—",
     "- Chỉ còn kho thuộc TPE"),

    ("004", "Mở bảng hoạt động của một kho", "P0",
     "QL-1 có quyền \"Quản lý kho\", là thủ kho K1; " + DATA,
     "1. " + MENU_KHO + "\n"
     "2. Bấm tên kho K1",
     "—",
     "- Mở tab mới, tiêu đề \"Hoạt động nhập/xuất kho K1 - <tên kho K1>\"\n"
     "- Chỉ có DX-02, DX-04, DX-01 (không có DN-01 của K2); Tổng số phiếu nhận 3, Tổng hoàn thành 1"),

    ("005", "Bảng từng kho tự cập nhật đúng kho", "P0",
     "QL-1 là thủ kho K1, K2, đang mở bảng hoạt động kho K1",
     "1. Tab khác gửi thủ kho đề nghị xuất DX-15 kho K1\n"
     "2. Gửi thủ kho đề nghị nhập DN-02 kho K2",
     "—",
     "- Bước 1: DX-15 hiện ở đầu bảng\n"
     "- Bước 2: bảng kho K1 không thêm DN-02"),

    ("006", "Bảng từng kho: hoàn thành không chuyển xuống cuối", "P2",
     "QL-1 là thủ kho K1, đang mở bảng hoạt động kho K1",
     "1. Tab khác hoàn thành phiếu xuất kho của DX-04",
     "—",
     "- DX-04 nền xanh lá, Trạng thái \"Đã hoàn thành\"\n"
     "- Dòng giữ nguyên vị trí cho tới khi tải lại trang (khác màn Hoạt động kho)"),

    ("007", "Bảng kho không phụ trách không tự cập nhật", "P1",
     "QL-1 có quyền \"Quản lý kho\", không phải thủ kho K3, đang mở bảng hoạt động kho K3",
     "1. Tab khác gửi thủ kho đề nghị xuất DX-16 kho K3\n"
     "2. Quan sát, không tải lại trang",
     "—",
     "- Mong đợi: DX-16 tự hiện\n"
     "- Lưu ý: theo code hiện tại chỉ thấy sau khi tải lại trang - ghi Failed nếu người quản lý cần theo dõi "
     "trực tiếp"),
]


SEC_IX = [
    ("001", "Luồng xuất kho đầu - cuối", "P0",
     "TK-1 đang mở màn Hoạt động kho; bảng đang có ít nhất 1 dòng",
     "1. Kế toán lập đề nghị xuất kho DX-20 kho K1 từ yêu cầu xuất hàng của NV-B, gửi thủ kho lúc 10:00\n"
     "2. TK-1 duyệt DX-20 lúc 10:05\n"
     "3. TK-1 hoàn thành phiếu xuất kho của DX-20 lúc 10:25",
     "—",
     "- Sau bước 1: DX-20 ở đầu bảng, \"Đã nhận đề nghị\", Người yêu cầu NV-B\n"
     "- Sau bước 2: \"Đang lấy hàng\", Thời gian lấy/xếp hàng 10:05\n"
     "- Sau bước 3: \"Đã hoàn thành\", Tổng thời gian xử lý \"25 phút\", dòng xuống cuối bảng, nền xanh lá"),

    ("002", "Luồng nhập kho đầu - cuối", "P0",
     "TK-1 đang mở màn Hoạt động kho; bảng đang có ít nhất 1 dòng",
     "1. Kế toán gửi thủ kho đề nghị nhập kho DN-20 kho K2 lúc 10:00\n"
     "2. TK-1 duyệt lúc 10:10\n"
     "3. TK-1 hoàn thành phiếu nhập kho lúc 10:40\n"
     "4. Tải lại trang",
     "—",
     "- Sau bước 2: \"Đang xếp hàng\"\n"
     "- Sau bước 4: \"Đã hoàn thành\", Tổng thời gian xử lý \"40 phút\""),

    ("003", "Luồng từ chối rồi gửi lại", "P1",
     "TK-1 đang mở màn Hoạt động kho",
     "1. Kế toán gửi đề nghị xuất DX-21 kho K1\n"
     "2. TK-1 từ chối DX-21\n"
     "3. Kế toán sửa, gửi lại DX-21",
     "—",
     "- Sau bước 2: DX-21 mất khỏi bảng\n"
     "- Sau bước 3: DX-21 hiện lại ở đầu bảng với Thời gian nhận mới; ô tổng đếm DX-21 một lần"),

    ("004", "Đối chiếu ô tổng với số dòng", "P0",
     DATA,
     "1. " + OPEN + "\n"
     "2. Đếm số dòng và số dòng nền xanh lá",
     "—",
     "- Tổng số phiếu nhận bằng số dòng; Tổng hoàn thành bằng số dòng Đã hoàn thành; Tổng chưa xử lý bằng "
     "hiệu hai số"),

    ("005", "Sang ngày mới", "P1",
     DATA,
     "1. Ngày 28/10/2026 đăng nhập TK-1, " + MENU,
     "—",
     "- Không còn DX-01 (hoàn thành ngày hôm trước)\n"
     "- DX-02, DN-01, DX-04 vẫn hiện nếu chưa hoàn thành"),
]
