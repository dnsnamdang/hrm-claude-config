# -*- coding: utf-8 -*-
"""Section V - XI: tong hop, chi tiet chung tu, don vi tinh, in / excel, rang buoc, co lap, luong."""
from tc_data_role import MENU, H1, LOC

SEC_V = [
    ("001", "Số liệu khối tổng hợp", "P0",
     H1,
     "1. " + LOC + "\n"
     "2. Đọc khối tổng hợp",
     "—",
     "- Tồn đầu kỳ \"-\" (bằng 0)\n"
     "- Nhập trong kỳ 60, Xuất trong kỳ 30, Tồn cuối kỳ 30"),

    ("002", "Tồn cuối kỳ khớp tồn thực tế", "P0",
     H1,
     "1. Lọc như V.001\n"
     "2. Mở Báo cáo tồn kho theo vị trí, xem tồn H1 ở K1",
     "—",
     "- Báo cáo theo vị trí: P1 = 12 (L01 = 4, L02 = 8), P2 = 18\n"
     "- Tồn cuối kỳ 30 bằng tổng P1 và P2"),

    ("003", "SL tồn lũy kế từng dòng", "P0",
     H1,
     "1. Lọc như V.001, đọc cột SL tồn từ trên xuống",
     "—",
     "- NHAP_TON_DAU: 24\n"
     "- NK-1: 60\n"
     "- XK-1: 30\n"
     "- DCVT-1: 30"),

    ("004", "SL tồn dòng cuối bằng Tồn cuối kỳ", "P0",
     H1,
     "1. Lọc như V.001, so SL tồn dòng cuối với Tồn cuối kỳ",
     "—",
     "- Cả hai cùng là 30"),

    ("005", "Phiếu nhập, xuất điều chỉnh kiểm kê được tính vào Nhập, Xuất", "P0",
     H1 + "\nNgày 01/06: phiếu nhập kho điều chỉnh kiểm kê NDC-1 nhập 3 Cái; ngày 02/06: phiếu xuất kho điều "
     "chỉnh kiểm kê XDC-1 xuất 2 Cái",
     "1. " + LOC,
     "—",
     "- Có dòng NDC-1 (Nhập 3) và XDC-1 (Xuất 2)\n"
     "- Nhập trong kỳ 63, Xuất trong kỳ 32, Tồn cuối kỳ 31"),

    ("006", "Phiếu nhập lại, xuất lại được tính", "P1",
     H1 + "\nNgày 05/06: phiếu nhập lại NL-1 nhập 4 Cái; ngày 06/06: phiếu xuất lại XL-1 xuất 1 Cái",
     "1. " + LOC,
     "—",
     "- Có dòng NL-1 (Nhập 4), XL-1 (Xuất 1)\n"
     "- Nhập trong kỳ 64, Xuất trong kỳ 31, Tồn cuối kỳ 33"),

    ("007", "Chứng từ chưa ghi nhận vào kho không hiện", "P0",
     H1 + "\nPhiếu nhập kho NK-9 của H1 còn nháp, chưa nhập kho",
     "1. " + LOC,
     "—",
     "- Không có dòng NK-9, Nhập trong kỳ vẫn 60"),
]


SEC_VI = [
    ("001", "Dòng nhập tồn đầu", "P0",
     H1,
     "1. " + LOC + "\n"
     "2. Đọc dòng đầu tiên",
     "—",
     "- Ngày chứng từ 05/01, Số chứng từ \"NHAP_TON_DAU_<số>\" không bấm được\n"
     "- Diễn giải \"Nhập tồn đầu\", Nhập 24, dòng con lô L01 vị trí P1 SL 24\n"
     "- NVKD trống"),

    ("002", "Một chứng từ nhiều lô / vị trí gom thành 1 dòng", "P0",
     H1,
     "1. " + LOC + "\n"
     "2. Đọc dòng XK-1",
     "—",
     "- XK-1 là 1 dòng, cột Xuất 30\n"
     "- 2 dòng con: lô L01 vị trí P1 SL 20; lô L02 vị trí P1 SL 10\n"
     "- Cột STT, Ngày, Số chứng từ, SL tồn gộp ô cho cả 2 dòng con"),

    ("003", "Dòng phiếu nhập kho", "P0",
     H1 + "\nNK-1 có ghi chú \"Nhập hàng tháng 3\", người yêu cầu NV-KD thuộc phòng KD1",
     "1. " + LOC + "\n"
     "2. Đọc dòng NK-1",
     "—",
     "- Ngày chứng từ 10/03, Diễn giải \"Nhập hàng tháng 3\", Nhập 36\n"
     "- 2 dòng con: L02 P1 = 24; L02 P2 = 12\n"
     "- NVKD \"<họ tên NV-KD> - KD1\""),

    ("004", "Bấm Số chứng từ mở chứng từ gốc", "P0",
     H1,
     "1. Lọc như VI.001\n"
     "2. Bấm lần lượt NK-1, XK-1, DCVT-1",
     "—",
     "- Mỗi lần mở tab mới đúng trang chi tiết phiếu nhập kho, phiếu xuất kho, phiếu điều chuyển vị trí"),

    ("005", "Bấm số phiếu nhập, xuất điều chỉnh kiểm kê", "P1",
     "Như V.005",
     "1. Bấm NDC-1, rồi XDC-1",
     "—",
     "- Mở đúng trang chi tiết phiếu nhập kho điều chỉnh và phiếu xuất kho điều chỉnh"),

    ("006", "Dòng điều chuyển vị trí", "P0",
     H1,
     "1. " + LOC + "\n"
     "2. Đọc dòng DCVT-1",
     "—",
     "- Cột Nhập, Xuất ở dòng chính trống\n"
     "- Dòng con 1: Xuất 6, lô L02, vị trí P1, SL theo vị trí 6\n"
     "- Dòng con 2: Nhập 6, lô L02, vị trí P2, SL theo vị trí 6"),

    ("007", "Sắp xếp theo thời gian ghi nhận", "P1",
     H1 + "\nNgày 15/04 có thêm phiếu xuất XK-2 ghi nhận sau XK-1 1 tiếng",
     "1. " + LOC,
     "—",
     "- Các dòng tăng dần theo thời gian, XK-1 đứng trước XK-2\n"
     "- STT đánh liên tục từ 1"),

    ("008", "Cột SL theo vị trí luôn là số dương", "P2",
     H1,
     "1. Lọc như VI.001, đọc dòng con của XK-1",
     "—",
     "- Hiện 20 và 10, không có dấu trừ"),

    ("009", "Dòng chứng từ không có người yêu cầu", "P2",
     "Phiếu điều chuyển vị trí DCVT-2 của H1 không có người yêu cầu",
     "1. Lọc H1, đọc cột NVKD của DCVT-2",
     "—",
     "- Mong đợi: NVKD trống\n"
     "- Lưu ý: nếu hiện \"null - null\" hoặc \"undefined - undefined\" thì ghi Failed"),

    ("010", "Chứng từ có ký tự đặc biệt trong diễn giải", "P2",
     "XK-1 có ghi chú \"Xuất cho A & B <gấp>\"",
     "1. Lọc H1, đọc Diễn giải XK-1",
     "—",
     "- Hiện đúng nguyên văn, không vỡ bảng"),
]


SEC_VII = [
    ("001", "Ô Đơn vị tính liệt kê các ĐVT của hàng", "P1",
     H1,
     "1. Lọc H1, mở ô Đơn vị tính",
     "—",
     "- Có \"Cái\" và \"Thùng (x12)\", mặc định Cái (đơn vị nhỏ nhất)"),

    ("002", "Đổi sang Thùng đổi số khối tổng hợp", "P0",
     H1,
     "1. Lọc H1 từ 01/04, chọn Đơn vị tính Thùng",
     "Đơn vị tính: Thùng",
     "- Tồn đầu kỳ 5, Xuất trong kỳ 2,5, Tồn cuối kỳ 2,5\n"
     "- Không cần bấm Lọc lại"),

    ("003", "Đổi sang Thùng đổi số từng dòng", "P0",
     H1,
     "1. Lọc H1 từ 01/04, chọn Đơn vị tính Thùng\n"
     "2. Đọc dòng XK-1",
     "—",
     "- Xuất 2,5; dòng con 1,67 và 0,83\n"
     "- Mong đợi: SL tồn 2,5\n"
     "- Lưu ý: theo code hiện tại SL tồn hiện 57,5 (lấy Tồn đầu 60 Cái cộng biến động tính theo Thùng) - ghi "
     "Failed"),

    ("004", "Đổi Thùng khi Tồn đầu kỳ bằng 0", "P1",
     H1,
     "1. " + LOC + "\n"
     "2. Chọn Thùng, đọc cột SL tồn",
     "—",
     "- 2; 5; 2,5; 2,5"),

    ("005", "Đổi lại Cái", "P2",
     H1,
     "1. Đang ở Thùng, chọn lại Cái",
     "—",
     "- Mọi số trở về như lúc chưa đổi"),
]


SEC_VIII = [
    ("001", "In khi chưa chọn hàng", "P0",
     "Chưa chọn hàng hóa",
     "1. Bấm In\n"
     "2. Bấm Xuất excel",
     "—",
     "- Cả 2 lần báo \"Chưa chọn đủ điều kiện bắt buộc\", không mở cửa sổ chọn kiểu"),

    ("002", "Cửa sổ chọn kiểu in", "P1",
     H1,
     "1. Chọn H1, bấm In\n"
     "2. Không chọn Kiểu in, bấm IN",
     "—",
     "- Bước 1: cửa sổ \"In báo cáo\" với Kiểu in: Đầy đủ, Rút gọn\n"
     "- Bước 2: không có gì xảy ra"),

    ("003", "In kiểu Đầy đủ", "P0",
     H1,
     "1. Lọc như VI.001, bấm In, chọn Đầy đủ, bấm IN",
     "Kiểu in: Đầy đủ",
     "- Mở tab mới khổ ngang, phần đầu có Từ ngày, Đến ngày, Kho \"K1 - <tên kho>\", Hàng hóa "
     "\"<mã>-<tên H1>\"\n"
     "- Khối tổng hợp và các dòng như trên màn, có cột NVKD\n"
     "- Cuối có ngày, tháng, năm hiện tại"),

    ("004", "In kiểu Rút gọn", "P1",
     H1,
     "1. Bấm In, chọn Rút gọn, bấm IN",
     "Kiểu in: Rút gọn",
     "- Giống bản Đầy đủ nhưng không có cột NVKD"),

    ("005", "Bản In theo ĐVT đang chọn", "P1",
     H1,
     "1. Lọc H1 từ 01/04, chọn Đơn vị tính Thùng\n"
     "2. In Đầy đủ",
     "—",
     "- Dòng Đơn vị tính ghi \"Thùng\", Tồn đầu kỳ 5, dòng XK-1 SL tồn 3 (đúng 2,5 làm tròn)\n"
     "- Mong đợi: Xuất trong kỳ và cột Xuất hiện 2,5\n"
     "- Lưu ý: theo code hiện tại làm tròn thành 3 - ghi Failed nếu cần số lẻ"),

    ("006", "Cột Xuất trên bản In", "P2",
     H1,
     "1. In Đầy đủ ở ĐVT Cái, đọc dòng XK-1",
     "—",
     "- Mong đợi: Xuất 30 như trên màn\n"
     "- Lưu ý: theo code hiện tại in \"-30\", dòng con \"-20\", \"-10\" - ghi Failed"),

    ("007", "In khi không chọn kho", "P2",
     H1,
     "1. Chọn H1, để trống Kho, In Đầy đủ",
     "—",
     "- Phần đầu bản In ô Kho để trống, số liệu là mọi kho của công ty"),

    ("008", "Xuất Excel", "P0",
     H1,
     "1. Lọc như VI.001, bấm Xuất excel, chọn Đầy đủ, bấm Xuất",
     "Kiểu xuất: Đầy đủ",
     "- Tải về file \"bao_cao_the_kho.xlsx\"\n"
     "- Số liệu khớp bản In Đầy đủ, phần đầu là thông tin công ty người xuất"),

    ("009", "In theo bộ lọc chưa bấm Lọc lại", "P2",
     H1,
     "1. Lọc H1 từ 01/01\n"
     "2. Đổi Từ ngày sang 01/04 nhưng không bấm Lọc, bấm In",
     "—",
     "- Bản In theo Từ ngày 01/04 (Tồn đầu kỳ 60), khác với bảng đang hiện trên màn"),
]


SEC_IX = [
    ("001", "Nút Lọc mờ khi chưa chọn hàng", "P0",
     "—",
     "1. Mở màn, chọn kho và ngày nhưng không chọn hàng",
     "—",
     "- Nút Lọc mờ, không bấm được"),

    ("002", "Gọi thẳng chức năng lấy dữ liệu không kèm hàng", "P2",
     "TK-1 có quyền Thủ kho",
     "1. Dùng công cụ kiểm thử API gọi chức năng lấy dữ liệu Thẻ kho không truyền hàng hóa",
     "—",
     "- Báo \"Chưa chọn hàng hóa\""),

    ("003", "Gõ ngày sai định dạng", "P2",
     H1,
     "1. Gõ tay \"31/02\" vào Từ ngày, bấm Lọc",
     "Từ ngày: 31/02",
     "- Ô không nhận ngày không tồn tại hoặc báo lỗi, không ra số liệu sai"),

    ("004", "Bấm Lọc liên tiếp với hai hàng khác nhau", "P2",
     H1 + "\nHàng H2 có lịch sử ở K1",
     "1. Chọn H1, bấm Lọc; ngay lập tức chọn H2, bấm Lọc",
     "—",
     "- Bảng chỉ hiện kết quả của lần bấm sau cùng (H2), không lẫn H1"),

    ("005", "Hàng có rất nhiều chứng từ", "P2",
     "Hàng H3 có hơn 2.000 lần nhập xuất trong năm ở K1",
     "1. Lọc H3 từ 01/01 đến hôm nay",
     "—",
     "- Bảng tải xong trong thời gian chấp nhận được, không treo trình duyệt\n"
     "- Bảng không phân trang, hiện đủ mọi dòng"),

    ("006", "Tồn âm hiển thị", "P1",
     "Hàng H4 ở K1 bị xuất vượt tồn, SL tồn sau phiếu XK-7 là -2",
     "1. Lọc H4, đọc SL tồn dòng XK-7 trên màn và trên bản In",
     "—",
     "- Màn hình: -2\n"
     "- Mong đợi bản In: -2\n"
     "- Lưu ý: theo code hiện tại bản In ghi 2 (mất dấu trừ) - ghi Failed"),
]


SEC_X = [
    ("001", "Tồn theo công ty chỉ tính phần của công ty", "P0",
     H1 + "\nKho K1 dùng chung; công ty TPC (công ty thuê kho) nhập H1 8 Cái ngày 03/03 (NK-3)",
     "1. Chọn Tồn theo công ty TPE, không chọn kho, lọc H1",
     "—",
     "- Không có NK-3, Nhập trong kỳ 60"),

    ("002", "Thủ kho không thấy kho không được phân", "P0",
     "TK-1 được phân K1; K3 cùng công ty có H1 nhập 7 Cái (NK-4)",
     "1. TK-1 mở ô Kho\n"
     "2. Lọc H1 không chọn kho",
     "—",
     "- Bước 1: không có K3\n"
     "- Mong đợi bước 2: không có NK-4\n"
     "- Lưu ý: nếu có NK-4 của K3 thì ghi Failed (khi không chọn kho hệ thống lấy mọi kho của công ty)"),

    ("003", "Có biến động mới trong lúc đang xem", "P2",
     H1,
     "1. Lọc H1\n"
     "2. Người khác hoàn thành phiếu xuất XK-8 xuất 2 Cái H1 ở K1\n"
     "3. Bấm Lọc lại",
     "—",
     "- Bước 1: Tồn cuối kỳ 30\n"
     "- Bước 3: có thêm dòng XK-8, Tồn cuối kỳ 28"),
]


SEC_XI = [
    ("001", "Luồng nhập, xuất, điều chuyển rồi xem Thẻ kho", "P0",
     "Hàng H5 mới, chưa có tồn ở K1",
     "1. Hoàn thành phiếu nhập kho 50 Cái H5 vào P1\n"
     "2. Hoàn thành phiếu xuất kho 20 Cái H5 từ P1\n"
     "3. Hoàn thành phiếu điều chuyển 10 Cái H5 từ P1 sang P2\n"
     "4. " + MENU + ", lọc H5 kho K1",
     "—",
     "- 3 dòng theo đúng thứ tự, SL tồn 50, 30, 30\n"
     "- Nhập 50, Xuất 20, Tồn cuối kỳ 30, khớp tồn ở báo cáo tồn kho theo vị trí"),

    ("002", "Luồng kiểm kê có chênh lệch rồi xem Thẻ kho", "P0",
     "Hàng H6 ở K1 tồn 10 Cái",
     "1. Lập phiếu kiểm kê theo hàng hóa, Thực kiểm H6 = 7, duyệt\n"
     "2. Xử lý bằng phiếu xuất kho điều chỉnh, hoàn thành phiếu xuất\n"
     "3. Lọc Thẻ kho H6",
     "—",
     "- Có dòng phiếu xuất kho điều chỉnh, Xuất 3\n"
     "- Tồn cuối kỳ 7"),

    ("003", "Luồng xem, đổi ĐVT, In Rút gọn", "P1",
     H1,
     "1. " + LOC + "\n"
     "2. Chọn Thùng\n"
     "3. In Rút gọn",
     "—",
     "- Màn và bản In cùng Tồn cuối kỳ 2,5 (bản In làm tròn 3), bản In không có cột NVKD"),
]
