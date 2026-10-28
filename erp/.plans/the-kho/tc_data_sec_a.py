# -*- coding: utf-8 -*-
"""Section I - IV: hien thi, bo loc hang / cong ty / kho, loc vi tri, loc thoi gian & loai bao cao."""
from tc_data_role import MENU, H1, LOC

SEC_I = [
    ("001", "Bố cục mặc định của màn", "P0",
     "TK-1 có quyền Thủ kho",
     "1. " + MENU + "\n"
     "2. Quan sát từ trên xuống",
     "—",
     "- Khung Bộ lọc: Hàng hóa (bắt buộc), Tồn theo công ty, Kho, Công ty thuê kho, Từ ngày, Đến ngày, Loại "
     "báo cáo (mặc định Tất cả), 4 khung Nhà, Dãy, Khoang, Vị trí\n"
     "- Nút Lọc (mờ khi chưa chọn hàng), Xuất excel, In\n"
     "- Bảng Chi tiết có cột: STT, Ngày chứng từ, Số chứng từ, Diễn giải, Nhập, Xuất, Lô, Vị trí, SL theo "
     "vị trí, SL tồn, NVKD"),

    ("002", "Thu gọn, mở lại khung Bộ lọc", "P2",
     "—",
     "1. Bấm mũi tên góc phải khung Bộ lọc 2 lần",
     "—",
     "- Lần 1 khung thu gọn, lần 2 mở lại, giá trị đã chọn còn nguyên"),

    ("003", "Chọn hàng hóa qua cửa sổ tìm hàng", "P0",
     "Có hàng H1 mã \"CN-2900\"",
     "1. Bấm nút tìm ở ô Hàng hóa\n"
     "2. Gõ \"CN-2900\", chọn H1",
     "Hàng hóa: CN-2900",
     "- Cửa sổ đóng, ô Hàng hóa hiện tên H1\n"
     "- Nút Lọc sáng lên"),

    ("004", "Lọc lần đầu hiện khối tổng hợp", "P0",
     H1,
     "1. " + LOC,
     "—",
     "- Khối tổng hợp nền xanh nhạt gồm: Đơn vị tính (chọn sẵn Cái), Tồn đầu kỳ, Nhập trong kỳ, Xuất trong "
     "kỳ, Tồn cuối kỳ\n"
     "- Dưới là các dòng chứng từ"),

    ("005", "Biểu tượng đang tải", "P2",
     H1,
     "1. Bấm Lọc, quan sát ngay",
     "—",
     "- Nút Lọc hiện vòng xoay và bị mờ, bảng hiện \"Đang tải dữ liệu\" cho tới khi có kết quả"),

    ("006", "Chọn hàng đã ngừng sử dụng", "P1",
     "Hàng H9 đã bị xóa khỏi danh mục nhưng còn lịch sử nhập xuất ở K1",
     "1. Mở cửa sổ tìm hàng, tìm H9\n"
     "2. Chọn H9, bấm Lọc",
     "—",
     "- H9 vẫn tìm và chọn được\n"
     "- Thẻ kho hiện đủ lịch sử của H9"),
]


SEC_II = [
    ("001", "Đổi Tồn theo công ty đổi danh sách kho", "P0",
     "TK-2 có quyền tổng công ty, được phân kho K1 (TPE) và K5 (công ty TPC)",
     "1. Mở ô Kho khi đang chọn TPE\n"
     "2. Đổi Tồn theo công ty sang TPC, mở lại ô Kho",
     "Tồn theo công ty: TPC",
     "- Bước 1: chỉ có K1\n"
     "- Bước 2: chỉ có K5, kho đã chọn trước đó bị bỏ"),

    ("002", "Không chọn kho thì lấy mọi kho của công ty", "P0",
     H1 + "\nCông ty TPE có thêm kho K2: H1 nhập 5 Cái ngày 02/02 (phiếu NK-2)",
     "1. Chọn H1, để trống Kho, Từ ngày 01/01, bấm Lọc",
     "—",
     "- Có cả NK-2 của K2 và các chứng từ của K1\n"
     "- Nhập trong kỳ 65"),

    ("003", "Chọn một kho", "P0",
     H1 + "\nKho K2: H1 nhập 5 Cái ngày 02/02 (NK-2)",
     "1. " + LOC,
     "Kho: K1",
     "- Không có NK-2\n"
     "- Nhập trong kỳ 60"),

    ("004", "Chọn nhiều kho", "P1",
     H1 + "\nKho K2: H1 nhập 5 Cái ngày 02/02 (NK-2)",
     "1. Chọn Kho K1 và K2, bấm Lọc",
     "Kho: K1, K2",
     "- Có NK-2 và các chứng từ của K1, sắp theo thời gian ghi nhận\n"
     "- Nhập trong kỳ 65"),

    ("005", "Chọn kho tự chọn hết Công ty thuê kho", "P0",
     "Kho K1 có 2 công ty thuê kho TPE, TPC",
     "1. Chọn Kho K1\n"
     "2. Mở ô Công ty thuê kho",
     "—",
     "- Ô Công ty thuê kho tự có TPE, TPC đều được chọn"),

    ("006", "Bỏ một Công ty thuê kho", "P0",
     H1 + "\nKho K1 có thêm phần tồn của công ty thuê kho TPC: 03/03 nhập 8 Cái (NK-3)",
     "1. Chọn H1, Kho K1, bỏ TPC ở ô Công ty thuê kho, bấm Lọc\n"
     "2. Chọn lại TPC, bấm Lọc",
     "—",
     "- Bước 1: không có NK-3, Nhập trong kỳ 60\n"
     "- Bước 2: có NK-3, Nhập trong kỳ 68"),

    ("007", "Hàng không có biến động ở kho đã chọn", "P1",
     "Hàng H2 chưa từng nhập vào kho K1",
     "1. Chọn H2, Kho K1, bấm Lọc",
     "—",
     "- Khối tổng hợp hiện \"-\" ở Tồn đầu, Nhập, Xuất, Tồn cuối\n"
     "- Không có dòng chứng từ"),

    ("008", "Đổi hàng hóa rồi lọc lại", "P1",
     H1 + "\nHàng H2 có 2 chứng từ ở K1",
     "1. Lọc H1\n"
     "2. Chọn H2, bấm Lọc",
     "—",
     "- Bảng thay toàn bộ bằng dữ liệu H2, ĐVT về đơn vị nhỏ nhất của H2"),
]


SEC_III = [
    ("001", "Chọn kho hiện Nhà và Vị trí tự do", "P1",
     "Kho K1 có nhà N1 (dãy D1, khoang KH1 gồm vị trí P1) và vị trí tự do P2",
     "1. Chọn Kho K1\n"
     "2. Quan sát khung Nhà và khung Vị trí",
     "—",
     "- Khung Nhà có N1 dưới tiêu đề K1\n"
     "- Khung Vị trí có mục \"Vị trí tự do\" với P2"),

    ("002", "Chọn lần lượt Nhà, Dãy, Khoang", "P1",
     "Như III.001",
     "1. Tích N1\n"
     "2. Tích D1\n"
     "3. Tích KH1",
     "—",
     "- Bước 1: khung Dãy hiện D1\n"
     "- Bước 2: khung Khoang hiện KH1\n"
     "- Bước 3: khung Vị trí có thêm mục \"Vị trí thuộc khoang\" với P1"),

    ("003", "Chỉ chọn Vị trí P2", "P0",
     H1 + "\nP2 là vị trí tự do của K1",
     "1. Chọn H1, Kho K1, Từ ngày 01/01, Loại báo cáo \"Không nhặt điều chuyển\"\n"
     "2. Tích Vị trí P2, bấm Lọc",
     "Vị trí: P2",
     "- Chỉ có NK-1 với 1 dòng con P2 lô L02 = 12\n"
     "- Nhập trong kỳ 12, Xuất 0, Tồn cuối kỳ 12"),

    ("004", "Chọn Nhà mà không chọn Vị trí", "P1",
     H1 + "\nP1 thuộc nhà N1, P2 là vị trí tự do",
     "1. Chọn H1, Kho K1, tích Nhà N1, không tích vị trí nào\n"
     "2. Bấm Lọc",
     "Nhà: N1",
     "- Mong đợi: chỉ có biến động ở P1\n"
     "- Lưu ý: theo code hiện tại vẫn có dòng con P2, số liệu như không chọn nhà - ghi Failed"),

    ("005", "Lọc vị trí có điều chuyển vào, loại Tất cả", "P1",
     H1,
     "1. Chọn H1, Kho K1, Từ ngày 01/01, Loại báo cáo \"Tất cả\", tích P2, bấm Lọc",
     "Vị trí: P2",
     "- Dòng DCVT-1: dòng con P2 lô L02 SL 6, SL tồn 18\n"
     "- Mong đợi: số 6 nằm ở cột Nhập, Tồn cuối kỳ 18 bằng SL tồn dòng cuối\n"
     "- Lưu ý: theo code hiện tại cột Xuất hiện \"-6\", cột Nhập trống và Tồn cuối kỳ là 12 - ghi Failed"),

    ("006", "Bỏ tích kho thì khung vị trí trống", "P2",
     "Đã chọn K1 và tích vài vị trí",
     "1. Bỏ K1 khỏi ô Kho",
     "—",
     "- Khung Nhà, Vị trí không còn mục nào của K1"),
]


SEC_IV = [
    ("001", "Lọc theo khoảng ngày tính trọn hai đầu", "P0",
     H1,
     "1. Chọn H1, Kho K1, Từ ngày 10/03, Đến ngày 15/04, bấm Lọc",
     "Từ ngày: 10/03\n"
     "Đến ngày: 15/04",
     "- Có đúng NK-1 và XK-1\n"
     "- Tồn đầu kỳ 24, Nhập 36, Xuất 30, Tồn cuối kỳ 30"),

    ("002", "Tồn đầu kỳ gồm mọi biến động trước Từ ngày", "P0",
     H1,
     "1. Chọn H1, Kho K1, Từ ngày 01/04, Đến ngày hôm nay, bấm Lọc",
     "Từ ngày: 01/04",
     "- Tồn đầu kỳ 60, Nhập 0, Xuất 30, Tồn cuối kỳ 30\n"
     "- Dòng XK-1 có SL tồn 30"),

    ("003", "Để trống Từ ngày", "P1",
     H1 + "\nNăm trước H1 có nhập 10, xuất 10 ở K1",
     "1. Xóa trống Từ ngày, bấm Lọc",
     "Từ ngày: (trống)",
     "- Tồn đầu kỳ 0\n"
     "- Có cả các chứng từ của năm trước"),

    ("004", "Để trống Đến ngày", "P2",
     H1,
     "1. Xóa trống Đến ngày, bấm Lọc",
     "—",
     "- Lấy tới thời điểm hiện tại, số liệu như khi Đến ngày là hôm nay"),

    ("005", "Đến ngày trước Từ ngày", "P2",
     H1,
     "1. Chọn Từ ngày 01/06, Đến ngày 01/03, bấm Lọc",
     "—",
     "- Mong đợi: báo lỗi khoảng ngày\n"
     "- Lưu ý: theo code hiện tại không báo, bảng không có dòng chứng từ, Tồn đầu 30, Tồn cuối 30 - ghi "
     "Failed nếu nghiệp vụ yêu cầu chặn"),

    ("006", "Ngày chứng từ là ngày ghi nhận vào kho", "P1",
     "Phiếu xuất XK-5 của H1 lập ngày 28/02 nhưng thủ kho xuất thực tế ngày 02/03",
     "1. Lọc H1 từ 01/03 đến 31/03",
     "—",
     "- Có XK-5, cột Ngày chứng từ 02/03\n"
     "- Lọc 01/02 đến 28/02 thì không có XK-5"),

    ("007", "Loại báo cáo Tất cả có dòng điều chuyển", "P0",
     H1,
     "1. " + LOC,
     "—",
     "- Có dòng DCVT-1 với 2 dòng con: Xuất 6 lô L02 vị trí P1, Nhập 6 lô L02 vị trí P2\n"
     "- Nhập trong kỳ 60, Xuất trong kỳ 30 (không tính điều chuyển)"),

    ("008", "Loại báo cáo Không nhặt điều chuyển", "P0",
     H1,
     "1. Như IV.007 nhưng chọn Loại báo cáo \"Không nhặt điều chuyển\", bấm Lọc",
     "Loại báo cáo: Không nhặt điều chuyển",
     "- Không có dòng DCVT-1, còn 3 dòng\n"
     "- Tổng hợp không đổi: Tồn đầu 0, Nhập 60, Xuất 30, Tồn cuối 30"),
]
