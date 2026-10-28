# -*- coding: utf-8 -*-
"""Section IV, V — tao / sua / xem; dieu chuyen & tac dong ton, lien ket kiem ke."""
from tc_data_role import DATA

SEC_IV = [
    ("001", "Bố cục màn Tạo mới", "P0",
     "TK1 có quyền Điều chuyển vị trí, là thủ kho K1",
     "1. Bấm Tạo mới trên danh sách\n"
     "2. Quan sát",
     "—",
     "- Tiêu đề \"Tạo phiếu điều chuyển vị trí\"\n"
     "- Khối Thông tin chung: ô Chọn kho, ô Ghi chú, khối \"File đính kèm (PDF)\" có dấu +\n"
     "- Bảng Chi tiết: STT, Tên hàng hóa, Model, Mã hàng hóa, Đơn vị tính, Vị trí xuất, Lô xuất, SL tồn, Vị trí nhập, SL; "
     "hiện \"Chưa có hàng hóa\"\n"
     "- Nút + thêm hàng bị khóa khi chưa chọn kho\n"
     "- Cuối trang: In dự kiến, Lưu, Điều chuyển, Hủy"),

    ("002", "Thêm hàng hóa", "P0",
     DATA,
     "1. Chọn kho K1, bấm dấu + ở bảng Chi tiết\n"
     "2. Tìm HH-0091, chọn",
     "Hàng: HH-0091",
     "- Thông báo \"Thêm thành công\"\n"
     "- Thêm 1 dòng, Đơn vị tính tự chọn đơn vị đầu tiên của hàng\n"
     "- Vị trí xuất, Lô xuất, Vị trí nhập trống; SL tồn hiện \"-\""),

    ("003", "Chọn Vị trí xuất chỉ thấy vị trí có tồn", "P0",
     DATA,
     "1. Ở dòng HH-0091 bấm nút kính lúp của Vị trí xuất\n"
     "2. Quan sát hộp \"Chọn vị trí\", bấm mã P1",
     "—",
     "- Hộp có cột STT, Vị trí, Nhà, Dãy, Khoang, Tồn; lọc được theo Nhà, Dãy, Khoang, mã vị trí\n"
     "- Có P1 (Tồn 15 Cái), KHÔNG có P4 (trống)\n"
     "- Chọn xong: Vị trí xuất = P1, Lô xuất bị xóa trắng để chọn lại"),

    ("004", "Chọn Lô xuất", "P0",
     DATA,
     "1. Sau khi chọn Vị trí xuất P1, bấm kính lúp của Lô xuất\n"
     "2. Chọn L02",
     "—",
     "- Hộp \"Chọn lô\" có cột STT, Số lô, Ngày nhập, Tồn\n"
     "- Chọn L02: Lô xuất = L02, SL tồn = 15"),

    ("005", "Nút Lô xuất bị khóa khi chưa chọn Vị trí xuất", "P1",
     "Dòng HH-0091 chưa có Vị trí xuất",
     "1. Thử bấm kính lúp của Lô xuất và của Vị trí nhập",
     "—",
     "- Cả hai nút bị khóa"),

    ("006", "Chọn Vị trí nhập", "P0",
     DATA,
     "1. Bấm kính lúp của Vị trí nhập\n"
     "2. Chọn P4",
     "—",
     "- Hộp hiện mọi vị trí của kho K1, kể cả vị trí trống P4\n"
     "- Vị trí nhập = P4"),

    ("007", "Không cho vị trí xuất và nhập trùng nhau", "P0",
     "Dòng đã có Vị trí xuất P1",
     "1. Chọn Vị trí nhập = P1\n"
     "2. Đặt Vị trí nhập P4, rồi đổi Vị trí xuất thành P4",
     "—",
     "- Cả hai lần cảnh báo \"Không thể xuất và nhập cùng một vị trí!\", hộp chọn không đóng, giá trị cũ giữ nguyên"),

    ("008", "SL tồn đổi theo Đơn vị tính", "P0",
     DATA,
     "1. Dòng P1 / L02, đơn vị Cái: đọc SL tồn\n"
     "2. Đổi Đơn vị tính sang Thùng",
     "Đơn vị tính: Cái rồi Thùng",
     "- Cái: SL tồn = 15\n"
     "- Thùng: SL tồn = 1.25"),

    ("009", "SL vượt SL tồn thì dòng đỏ và khóa nút Điều chuyển", "P0",
     DATA,
     "1. Nhập SL = 16 (đơn vị Cái)\n"
     "2. Sửa lại SL = 15",
     "SL: 16 rồi 15",
     "- SL 16: dòng tô nền đỏ nhạt, nút \"Điều chuyển\" bị khóa\n"
     "- SL 15: hết đỏ, nút mở lại"),

    ("010", "Xóa dòng hàng", "P1",
     "Bảng có 2 dòng",
     "1. Bấm dấu - đỏ ở dòng 1",
     "—",
     "- Còn 1 dòng, STT đánh lại"),

    ("011", "Đổi kho khi đã có hàng", "P0",
     "Đã chọn K1, có 2 dòng hàng; TK1 là thủ kho K1, K2",
     "1. Đổi Chọn kho sang K2\n"
     "2. Ở hộp xác nhận bấm \"Hủy\"\n"
     "3. Đổi lại sang K2, bấm \"Xác nhận\"",
     "Kho: K1 rồi K2",
     "- Hộp \"Nếu bạn thay đổi kho, danh sách hàng hóa sẽ được làm mới!\", nội dung \"Bạn có chắc chắn muốn thực hiện?\"\n"
     "- Hủy: kho về K1, 2 dòng còn nguyên\n"
     "- Xác nhận: kho K2, bảng trống"),

    ("012", "Đính kèm file PDF", "P1",
     "Màn Tạo mới",
     "1. Bấm dấu + ở khối File đính kèm, chọn bienban.pdf\n"
     "2. Bấm thêm dấu +, rồi bấm X ở ô thứ 2",
     "File: bienban.pdf",
     "- Ô 1 hiện tên bienban.pdf\n"
     "- Hộp chọn file chỉ cho chọn PDF\n"
     "- Ô 2 bị bỏ"),

    ("013", "Bấm Lưu tạo phiếu nháp", "P0",
     DATA,
     "1. Chọn K1, Ghi chú \"Dồn hàng\", thêm dòng HH-0091 P1 / L02 > P4, SL 5\n"
     "2. Bấm \"Lưu\"\n"
     "3. Xem danh sách và tồn ở P1, P4",
     "Ghi chú: Dồn hàng\n"
     "SL: 5",
     "- \"Lưu thành công\", về danh sách\n"
     "- Phiếu mới: Mã phiếu PĐCVT-<5 chữ số>, Ngày lập hôm nay, Kho K1, Đang tạo, Người lập TK1\n"
     "- Tồn P1 vẫn 15, P4 vẫn 0"),

    ("014", "Lưu nháp không bắt buộc đủ thông tin dòng", "P1",
     "Màn Tạo mới, chọn K1, Ghi chú \"Nháp\", thêm hàng HH-0091 chưa chọn vị trí, lô, SL",
     "1. Bấm \"Lưu\"\n"
     "2. Mở Sửa phiếu vừa lưu",
     "—",
     "- Lưu được, không bắt chọn file\n"
     "- Màn Sửa có lại dòng HH-0091 còn trống các ô"),

    ("015", "Bấm Điều chuyển trực tiếp", "P0",
     DATA,
     "1. Chọn K1, Ghi chú \"Dồn hàng\", dòng HH-0091 P1 / L02 > P4, SL 5, đính kèm bienban.pdf\n"
     "2. Bấm \"Điều chuyển\"",
     "SL: 5",
     "- \"Điều chuyển thành công\", về danh sách\n"
     "- Phiếu mới Đã chuyển, Mã phiếu bấm được"),

    ("016", "Mở Sửa phiếu nháp", "P0",
     "PĐ-1 Đang tạo kho K1, có 1 dòng, 1 file",
     "1. Bấm bánh răng PĐ-1 > Sửa",
     "—",
     "- Tiêu đề \"Điều chuyển vị trí <Mã phiếu>\"\n"
     "- Ô Chọn kho bị khóa\n"
     "- Ghi chú, các dòng, file đã lưu hiện lại đúng\n"
     "- Có In dự kiến, Lưu, Điều chuyển, Hủy"),

    ("017", "Sửa nháp rồi Lưu", "P1",
     "PĐ-1 Đang tạo",
     "1. Đổi Ghi chú, thêm 1 dòng, bấm \"Lưu\"",
     "—",
     "- \"Lưu thành công\", vẫn Đang tạo, mã phiếu không đổi, dữ liệu mới được giữ"),

    ("018", "Sửa nháp rồi Điều chuyển", "P0",
     "PĐ-1 Đang tạo, 1 dòng hợp lệ SL 5, đã có 1 file",
     "1. Mở Sửa PĐ-1, bấm \"Điều chuyển\" (không chọn file mới)",
     "—",
     "- \"Điều chuyển thành công\"\n"
     "- PĐ-1 Đã chuyển; không bắt đính kèm lại vì đã có file"),

    ("019", "Xóa file đã lưu ở màn Sửa", "P1",
     "PĐ-1 Đang tạo có bienban.pdf",
     "1. Mở Sửa, bấm X trên bienban.pdf",
     "—",
     "- Thông báo \"Xóa thành công\", file biến mất\n"
     "- Nếu bấm Điều chuyển sau đó thì phải chọn file mới"),

    ("020", "Nút Hủy chỉ quay về danh sách", "P2",
     "Đang ở màn Tạo mới đã nhập dữ liệu",
     "1. Bấm \"Hủy\"",
     "—",
     "- Về danh sách, không tạo phiếu nào"),

    ("021", "Bấm Điều chuyển liên tiếp", "P1",
     "Dữ liệu hợp lệ",
     "1. Bấm \"Điều chuyển\" 2 lần thật nhanh",
     "—",
     "- Nút bị khóa trong lúc xử lý; chỉ 1 phiếu, tồn chỉ trừ 1 lần"),
]


SEC_V = [
    ("001", "Điều chuyển trừ vị trí xuất, cộng vị trí nhập", "P0",
     DATA,
     "1. Điều chuyển HH-0091 P1 / L02 > P4, SL 5 Cái\n"
     "2. Xem tồn theo vị trí của HH-0091 (màn tra cứu tồn theo vị trí, hoặc mở hộp Chọn vị trí ở một phiếu mới)",
     "SL: 5",
     "- P1 còn 10, P4 có 5\n"
     "- Lô của P4 là L02, công ty TPE (giữ nguyên lô và công ty)\n"
     "- Tồn tổng của kho K1 không đổi"),

    ("002", "Điều chuyển theo ĐVT lớn quy về ĐVT cơ bản", "P0",
     "P1 lô L02 = 30 cái; Thùng hệ số 12",
     "1. Điều chuyển HH-0091 P1 / L02 > P4, Đơn vị tính Thùng, SL 2",
     "Đơn vị tính: Thùng\n"
     "SL: 2",
     "- P1 còn 6 cái, P4 có 24 cái"),

    ("003", "Một lô chia sang nhiều vị trí nhập", "P1",
     "P1 lô L02 = 15",
     "1. Thêm 2 dòng HH-0091 P1 / L02: dòng 1 > P4 SL 5, dòng 2 > P5 SL 4\n"
     "2. Bấm Điều chuyển",
     "—",
     "- P1 còn 6, P4 có 5, P5 có 4"),

    ("004", "Nhiều dòng cùng lô cộng dồn vượt tồn", "P0",
     "P1 lô L02 = 15",
     "1. Thêm 2 dòng HH-0091 P1 / L02: dòng 1 > P4 SL 10, dòng 2 > P5 SL 10\n"
     "2. Bấm Điều chuyển",
     "—",
     "- Từng dòng không đỏ (mỗi dòng 10 nhỏ hơn 15)\n"
     "- Bấm Điều chuyển: thông báo \"Dữ liệu hàng hóa vượt quá tồn: HH-0091\", không tạo phiếu, tồn không đổi"),

    ("005", "Trừ phần hàng của phiếu nhập kho chưa hoàn tất", "P1",
     "P1 tồn HH-0091 = 15, trong đó 5 cái thuộc một phiếu nhập kho chưa hoàn tất",
     "1. Điều chuyển HH-0091 P1 > P4, SL 12",
     "SL: 12",
     "- Thông báo \"Dữ liệu hàng hóa vượt quá tồn: HH-0091\" (chỉ được chuyển tối đa 10)"),

    ("006", "Chặn khi vị trí đang kiểm kê theo kế hoạch", "P0",
     "Kế hoạch kiểm kê KH-3 Đang kiểm có vị trí P1",
     "1. Điều chuyển HH-0091 từ P1 > P4",
     "—",
     "- Thông báo \"Vị trí P1 đang kiểm kho\", không tạo phiếu"),

    ("007", "Chặn khi vị trí nhập đang trong phiếu kiểm kê chờ duyệt", "P0",
     "Phiếu kiểm kê KK-1 Chờ duyệt kết quả có vị trí P4",
     "1. Điều chuyển HH-0091 từ P1 > P4",
     "—",
     "- Thông báo \"Vị trí P4 đang kiểm kho\""),

    ("008", "Không chặn khi kế hoạch đã sang Đã lập kiểm kê nhưng phiếu kiểm kê còn nháp", "P2",
     "KH-12 Đã lập kiểm kê, phiếu kiểm kê KK-4 Đang tạo, cùng có vị trí P1",
     "1. Điều chuyển HH-0091 từ P1 > P4",
     "—",
     "- Điều chuyển được\n"
     "- Lưu ý: hàng bị chuyển giữa lúc đang lập phiếu kiểm kê — ghi nhận cho nghiệp vụ"),

    ("009", "Chặn khi hàng đang kiểm kê theo hàng hóa", "P0",
     "Kế hoạch / phiếu kiểm kê theo hàng hóa của kho K1 đang mở, có HH-0091",
     "1. Điều chuyển HH-0091 trong kho K1",
     "—",
     "- Thông báo \"Hàng <tên HH-0091> đang kiểm kho\""),

    ("010", "Lưu nháp cũng bị chặn khi vị trí đang kiểm kê", "P2",
     "KH-3 Đang kiểm có P1",
     "1. Tạo dòng P1 > P4, bấm \"Lưu\"",
     "—",
     "- Báo \"Vị trí P1 đang kiểm kho\", không lưu được nháp"),

    ("011", "Điều chuyển đủ dòng thiếu thì phiếu kiểm kê và kế hoạch tự Hoàn thành", "P0",
     "KK-2 Chờ xử lý, lập từ KH-11, có DUY NHẤT 1 dòng thiếu 2 cái (kiểm theo Cái), ở P1 lô L02",
     "1. XL bấm \"Tạo phiếu điều chuyển vị trí\" trên KK-2\n"
     "2. Chọn Vị trí nhập P4, đính kèm file, bấm \"Điều chuyển\"\n"
     "3. Xem KK-2 và KH-11",
     "Vị trí nhập: P4",
     "- \"Điều chuyển thành công\"\n"
     "- KK-2 chuyển Hoàn thành, KH-11 chuyển Hoàn thành (không cần bấm nút Hoàn thành)\n"
     "- Cột Phiếu kiểm kê của phiếu điều chuyển (xem TC_01.008)"),

    ("012", "Còn dòng thiếu khác thì phiếu kiểm kê vẫn Chờ xử lý", "P0",
     "KK-2 có 2 dòng thiếu: P1 / L02 thiếu 2, P2 / L05 thiếu 3",
     "1. Tạo phiếu điều chuyển từ KK-2, xóa dòng P2 / L05, chọn Vị trí nhập cho dòng P1\n"
     "2. Bấm Điều chuyển, mở lại KK-2",
     "—",
     "- KK-2 vẫn Chờ xử lý, vẫn còn nút Tạo phiếu điều chuyển vị trí\n"
     "- Bấm lại nút chỉ còn dòng P2 / L05"),

    ("013", "Dòng thiếu kiểm theo ĐVT lớn", "P1",
     "KK-13 Chờ xử lý: dòng P1 / L02 kiểm theo Thùng, thiếu 1 Thùng (12 cái)",
     "1. Tạo phiếu điều chuyển từ KK-13, chọn Vị trí nhập, Điều chuyển\n"
     "2. Mở lại KK-13",
     "—",
     "- Mong đợi: dòng được coi là đã xử lý, KK-13 Hoàn thành\n"
     "- Lưu ý: code so số đã chuyển (theo Cái) với số thiếu (theo Thùng), có thể KHÔNG khớp nên KK-13 vẫn Chờ "
     "xử lý — nếu vậy ghi Failed"),

    ("014", "Lưu nháp từ phiếu kiểm kê rồi Sửa và Điều chuyển", "P0",
     "KK-2 có 2 dòng thiếu như TC_05.012",
     "1. Tạo phiếu điều chuyển từ KK-2, xóa dòng P2 / L05, bấm \"Lưu\"\n"
     "2. Mở Sửa phiếu nháp, chọn Vị trí nhập, đính kèm file, bấm \"Điều chuyển\"\n"
     "3. Xem KK-2",
     "—",
     "- Mong đợi: KK-2 vẫn Chờ xử lý vì còn dòng P2 / L05\n"
     "- Lưu ý: code hiện tại đặt KK-2 và kế hoạch Hoàn thành ngay — nếu vậy ghi Failed"),

    ("015", "Điều chuyển từ phiếu kiểm kê theo hàng hóa", "P1",
     "Phiếu kiểm kê theo hàng hóa KKHH-1 đang xử lý, có 1 dòng cần chuyển",
     "1. Tạo phiếu điều chuyển từ KKHH-1, chọn Vị trí nhập, Điều chuyển\n"
     "2. Xem KKHH-1",
     "—",
     "- Chuyển đủ thì KKHH-1 Hoàn thành; chưa đủ thì Đang xử lý"),

    ("016", "Phiếu đã chuyển không sửa, không xóa", "P0",
     "PĐ-3 Đã chuyển",
     "1. Bấm bánh răng PĐ-3",
     "—",
     "- Chỉ có In phiếu"),
]
