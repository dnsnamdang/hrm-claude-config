# -*- coding: utf-8 -*-
"""Section I - X cho man Bao cao ton kho chi tiet theo mat hang."""
from tc_data_role import MENU, H1, LOC

SEC_I = [
    ("001", "Bố cục mặc định của màn", "P0",
     "KT-1 có quyền xem báo cáo tồn kho theo công ty",
     "1. " + MENU + "\n"
     "2. Quan sát từ trên xuống",
     "—",
     "- Bộ lọc: Tính đến ngày, Tồn theo công ty, Kho (bắt buộc), Công ty thuê kho, Nhóm hàng hóa, Tính chất "
     "hàng hóa, Loại hàng hóa, Thương hiệu, Hãng sản xuất, Hàng hóa, Hợp đồng\n"
     "- Nút Xuất excel (mờ), Lọc (mờ khi chưa chọn kho), nút làm mới\n"
     "- Bảng có cột STT, Tên hàng hóa, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn, Công ty, Lô, Vị trí, SL, "
     "Cộng"),

    ("002", "Lọc lần đầu", "P0",
     H1,
     "1. " + LOC,
     "—",
     "- Có dòng H1, không có H2\n"
     "- Nút Xuất excel sáng lên"),

    ("003", "Không có nút In", "P2",
     "—",
     "1. Quan sát hàng nút",
     "—",
     "- Chỉ có Xuất excel, Lọc, làm mới; không có In"),

    ("004", "Biểu tượng đang tải", "P2",
     H1,
     "1. Bấm Lọc, quan sát ngay",
     "—",
     "- Nút Lọc, Xuất excel hiện vòng xoay và bị mờ; bảng hiện \"Đang tải dữ liệu\""),

    ("005", "Thu gọn khung Bộ lọc", "P2",
     "—",
     "1. Bấm mũi tên góc phải khung Bộ lọc 2 lần",
     "—",
     "- Khung thu gọn rồi mở lại, giá trị đã chọn còn nguyên"),
]


SEC_II = [
    ("001", "Nút Lọc mờ khi chưa chọn Kho", "P0",
     "—",
     "1. Mở màn, không chọn Kho",
     "—",
     "- Nút Lọc mờ, không bấm được"),

    ("002", "Đổi Tồn theo công ty xóa Kho đã chọn", "P0",
     "KT-2 có quyền tổng công ty; TPE có kho K1, TPC có kho K5",
     "1. Chọn TPE, Kho K1\n"
     "2. Đổi sang TPC, mở ô Kho",
     "—",
     "- Ô Kho và Công ty thuê kho bị xóa trống\n"
     "- Danh sách kho chỉ còn kho của TPC (K5)"),

    ("003", "Chọn Kho tự chọn hết Công ty thuê kho", "P0",
     H1,
     "1. Chọn Kho K1, mở ô Công ty thuê kho",
     "—",
     "- Có TPE, TPC, cả hai đều được chọn"),

    ("004", "Bỏ một Công ty thuê kho", "P0",
     H1,
     "1. Chọn Kho K1, bỏ TPC ở ô Công ty thuê kho, bấm Lọc",
     "—",
     "- H1: SL tồn 30, chỉ còn dòng công ty TPE"),

    ("005", "Chỉ hiện hàng của kho đã chọn", "P0",
     H1 + "\nKho K2 có hàng H3 tồn 5",
     "1. " + LOC,
     "—",
     "- Không có H3"),

    ("006", "Lọc theo Hàng hóa", "P0",
     H1 + "\nKho K1 còn tồn H4",
     "1. Bấm nút tìm ở ô Hàng hóa, chọn H1, bấm Lọc\n"
     "2. Bấm x ở ô Hàng hóa, bấm Lọc",
     "—",
     "- Bước 1: chỉ có H1\n"
     "- Bước 2: có cả H1 và H4"),

    ("007", "Lọc theo Nhóm, Tính chất, Loại hàng hóa", "P1",
     "H1 thuộc nhóm \"Máy in\", tính chất \"Hàng hóa\", loại \"Thiết bị\"; H4 thuộc nhóm \"Mực in\"",
     "1. Chọn Nhóm hàng hóa \"Máy in\", bấm Lọc\n"
     "2. Bỏ nhóm, chọn Loại hàng hóa \"Thiết bị\", bấm Lọc",
     "—",
     "- Cả 2 bước: chỉ có H1"),

    ("008", "Lọc theo Thương hiệu, Hãng sản xuất", "P1",
     "H1 thương hiệu Canon, hãng sản xuất Canon Inc; H4 thương hiệu HP",
     "1. Chọn Thương hiệu Canon, bấm Lọc\n"
     "2. Bỏ thương hiệu, chọn Hãng sản xuất \"Canon Inc\", bấm Lọc",
     "—",
     "- Cả 2 bước: chỉ có H1"),

    ("009", "Lọc theo Hợp đồng", "P1",
     H1,
     "1. Nhập Hợp đồng \"HD-01\", bấm Lọc",
     "Hợp đồng: HD-01",
     "- Chỉ có H1, chỉ có lô L01 kèm \"Hợp đồng: HD-01\"\n"
     "- Không có lô L02, L03"),

    ("010", "Kết hợp nhiều ô lọc không có kết quả", "P2",
     H1,
     "1. Chọn Hàng hóa H1, Thương hiệu HP, bấm Lọc",
     "—",
     "- Bảng ghi \"Chưa có dữ liệu\", nút Xuất excel mờ"),

    ("011", "Nút làm mới", "P1",
     "Đã chọn kho, nhóm hàng, hàng hóa và lọc",
     "1. Bấm nút làm mới\n"
     "2. Mở ô Kho",
     "—",
     "- Bước 1: các ô lọc về mặc định, Tính đến ngày về hôm nay\n"
     "- Mong đợi bước 2: có danh sách kho của công ty\n"
     "- Lưu ý: theo code hiện tại ô Kho trống, phải đổi công ty rồi đổi lại - ghi Failed"),
]


SEC_III = [
    ("001", "Tính đến hôm nay", "P0",
     H1,
     "1. " + LOC + ", đọc dòng H1",
     "—",
     "- SL tồn 42"),

    ("002", "Tính trọn ngày ở Tính đến ngày", "P1",
     H1 + "\nNgày 15/10 lúc 17:00 nhập thêm 3 Cái H1 lô L02 vị trí P1 cho TPE",
     "1. Chọn Tính đến ngày 15/10, bấm Lọc",
     "Tính đến ngày: 15/10",
     "- Đã tính phần nhập lúc 17:00 ngày 15/10"),

    ("003", "Tính đến ngày trong quá khứ: số tổng", "P0",
     H1 + "\nNgày 20/10 xuất 5 Cái lô L01 vị trí P1 của TPE (trước đó P1 lô L01 = 25)",
     "1. Chọn Tính đến ngày 15/10, bấm Lọc",
     "Tính đến ngày: 15/10",
     "- H1: SL tồn 47, Cộng TPE 35"),

    ("004", "Tính đến ngày trong quá khứ: số lô / vị trí", "P0",
     "Như III.003",
     "1. Chọn Tính đến ngày 15/10, bấm Lọc, đọc dòng lô L01 vị trí P1",
     "—",
     "- Mong đợi: 25\n"
     "- Lưu ý: theo code hiện tại hiện 20 (số hiện tại), tổng các vị trí không bằng Cộng 35 - ghi Failed"),

    ("005", "Lô đã hết hàng sau ngày lọc", "P1",
     H1 + "\nLô L04 của TPE ở P2 có 8 Cái tới 10/10, ngày 12/10 xuất hết",
     "1. Chọn Tính đến ngày 11/10, bấm Lọc",
     "—",
     "- Mong đợi: có dòng lô L04 vị trí P2 SL 8\n"
     "- Lưu ý: theo code hiện tại không có lô L04 dù Cộng TPE đã tính 8 - ghi Failed"),

    ("006", "Tính đến ngày trước khi có hàng", "P2",
     "H1 nhập vào K1 lần đầu ngày 01/03",
     "1. Chọn Tính đến ngày 28/02, bấm Lọc",
     "—",
     "- Không có dòng H1"),
]


SEC_IV = [
    ("001", "Chi tiết theo công ty, lô, vị trí", "P0",
     H1,
     "1. " + LOC + " (giữ cả TPE, TPC ở ô Công ty thuê kho)\n"
     "2. Đọc dòng H1",
     "—",
     "- Công ty TPE, Cộng 30: lô L01 có P1 20, P2 4; lô L02 có P1 6\n"
     "- Công ty TPC, Cộng 12: lô L03 có P3 12\n"
     "- SL tồn 42"),

    ("002", "SL tồn bằng tổng Cộng các công ty", "P0",
     H1,
     "1. Lọc như IV.001, cộng các ô Cộng",
     "—",
     "- 30 + 12 = 42 bằng SL tồn"),

    ("003", "Cộng của công ty bằng tổng SL các vị trí", "P0",
     H1,
     "1. Lọc như IV.001, cộng SL các dòng của TPE",
     "—",
     "- 20 + 4 + 6 = 30 bằng Cộng của TPE"),

    ("004", "Vị trí hết hàng không hiện", "P1",
     H1 + "\nLô L02 từng có ở vị trí P2 nhưng đã chuyển hết sang P1",
     "1. Lọc như IV.001",
     "—",
     "- Lô L02 chỉ có dòng P1, không có dòng P2 bằng 0"),

    ("005", "Hàng tồn 0 không hiện", "P0",
     H1,
     "1. " + LOC,
     "—",
     "- Không có dòng H2"),

    ("006", "Thông tin hợp đồng, khách hàng của lô", "P1",
     H1 + "\nHợp đồng HD-01 có khách hàng \"Nguyễn Văn A\" - 0901234567, ngày đặt 01/10, ngày trả 10/10",
     "1. Lọc như IV.001, đọc ô lô L01",
     "—",
     "- \"L01\", dòng \"Hợp đồng: HD-01\" bấm được để mở hợp đồng\n"
     "- \"Khách hàng: Nguyễn Văn A - 0901234567\", Ngày đặt hàng 01/10, Ngày trả hàng 10/10"),

    ("007", "Hợp đồng chưa có ngày trả hàng", "P2",
     "Lô L05 nhập từ hợp đồng HD-02, HD-02 có khách hàng nhưng để trống ngày trả hàng",
     "1. Lọc kho chứa L05, đọc ô lô L05",
     "—",
     "- Mong đợi: Ngày trả hàng để trống\n"
     "- Lưu ý: theo code hiện tại hiện ngày hôm nay - ghi Failed"),

    ("008", "Hợp đồng chưa có thông tin khách hàng", "P2",
     "Lô L06 nhập từ hợp đồng HD-03, HD-03 chưa khai báo khách hàng",
     "1. Lọc kho chứa L06, đọc ô lô L06",
     "—",
     "- Mong đợi: vẫn hiện \"Hợp đồng: HD-03\"\n"
     "- Lưu ý: theo code hiện tại không hiện số hợp đồng - ghi Failed"),

    ("009", "Công ty thuê kho tồn âm", "P2",
     "Hàng H5 ở K1: TPE tồn 10, TPC tồn -2 (xuất vượt)",
     "1. Lọc kho K1 (giữ TPE, TPC), đọc dòng H5",
     "—",
     "- Theo code hiện tại: chỉ có dòng TPE Cộng 10, SL tồn 10 (phần âm của TPC bị bỏ)\n"
     "- Lưu ý: ghi Failed nếu nghiệp vụ cần thấy tồn âm"),

    ("010", "Lô nhập không từ hợp đồng", "P2",
     H1,
     "1. Lọc như IV.001, đọc ô lô L02",
     "—",
     "- Chỉ có số lô, không có dòng Hợp đồng, Khách hàng"),
]


SEC_V = [
    ("001", "Ô ĐVT liệt kê các ĐVT của hàng", "P1",
     H1,
     "1. Lọc, mở ô ĐVT của H1",
     "—",
     "- Có \"Cái\" và \"Thùng (x12)\", mặc định Cái"),

    ("002", "Đổi ĐVT sang Thùng", "P0",
     H1,
     "1. Lọc như IV.001, chọn ĐVT Thùng ở H1",
     "ĐVT: Thùng",
     "- Mong đợi: SL tồn 3,5; Cộng TPE 2,5; Cộng TPC 1\n"
     "- Lưu ý: theo code hiện tại làm tròn thành 4, 3, 1 - ghi Failed nếu cần số lẻ"),

    ("003", "Đổi ĐVT chỉ ảnh hưởng hàng đó", "P1",
     H1 + "\nK1 còn tồn H4 có ĐVT Hộp",
     "1. Lọc, đổi ĐVT H1 sang Thùng",
     "—",
     "- Số của H4 giữ nguyên"),

    ("004", "Đổi lại ĐVT cơ bản", "P2",
     H1,
     "1. Đang ở Thùng, chọn lại Cái",
     "—",
     "- Mọi số của H1 trở về như ban đầu"),
]


SEC_VI = [
    ("001", "Phân trang 20 hàng", "P1",
     "Kho K1 có 45 mặt hàng còn tồn",
     "1. Lọc kho K1\n"
     "2. Chuyển sang trang 3",
     "—",
     "- Bước 1: 20 hàng, có 3 trang\n"
     "- Bước 2: 5 hàng, STT từ 41 đến 45"),

    ("002", "Sắp xếp theo tên hàng", "P1",
     "Kho K1 có hàng tên \"Bút\", \"Ấm\", \"Cân\"",
     "1. Lọc kho K1",
     "—",
     "- Thứ tự theo tên hàng tăng dần"),

    ("003", "Chuyển trang giữ bộ lọc", "P2",
     "Đã lọc Thương hiệu Canon, có hơn 20 hàng",
     "1. Chuyển sang trang 2",
     "—",
     "- Trang 2 vẫn chỉ có hàng Canon"),
]


SEC_VII = [
    ("001", "Mở cửa sổ Xuất Excel", "P1",
     H1,
     "1. Lọc, bấm Xuất excel\n"
     "2. Không chọn mẫu, bấm Xuất EXCEL",
     "—",
     "- Bước 1: cửa sổ \"Xuất Excel\" với mẫu: Xuất excel đầy đủ, Xuất excel ngắn gọn\n"
     "- Bước 2: báo \"Vui lòng chọn mẫu xuất excel.\""),

    ("002", "Xuất excel ngắn gọn", "P0",
     H1,
     "1. Lọc như IV.001, Xuất excel, chọn \"Xuất excel ngắn gọn\", bấm Xuất EXCEL",
     "Mẫu: ngắn gọn",
     "- Tải file \"bao_cao_ton_kho_chi_tiet_mat_hang.xlsx\"\n"
     "- Phần đầu có Kho \"K1 - <tên kho>\", ngày tính đến\n"
     "- Có dòng H1 với SL tồn 42"),

    ("003", "Xuất excel đầy đủ", "P0",
     H1,
     "1. Lọc như IV.001, Xuất excel, chọn \"Xuất excel đầy đủ\", bấm Xuất EXCEL",
     "Mẫu: đầy đủ",
     "- File có H1 kèm Công ty, Lô, Vị trí, SL, Cộng như trên màn\n"
     "- SL tồn 42; TPE Cộng 30; TPC Cộng 12"),

    ("004", "File theo ĐVT nhỏ nhất", "P2",
     H1,
     "1. Đổi ĐVT H1 sang Thùng, Xuất excel ngắn gọn",
     "—",
     "- Theo code hiện tại: file ghi ĐVT Cái, SL tồn 42\n"
     "- Lưu ý: ghi Failed nếu nghiệp vụ muốn file theo ĐVT đang chọn"),

    ("005", "Xuất khi có từ 150 hàng trở lên", "P1",
     "Kho K2 có 160 mặt hàng còn tồn; KT-1 có email",
     "1. Lọc kho K2, Xuất excel ngắn gọn",
     "—",
     "- Không tải file ngay, báo \"Báo cáo tồn kho chi tiết theo mặt hàng sẽ gửi về mail của bạn trong ít "
     "phút!\"\n"
     "- Vài phút sau email của KT-1 nhận được file"),

    ("006", "Xuất theo bộ lọc đang chọn", "P1",
     H1 + "\nK1 còn tồn H4",
     "1. Chọn Hàng hóa H1, bấm Lọc, Xuất excel ngắn gọn",
     "—",
     "- File chỉ có H1"),

    ("007", "Nút Xuất excel mờ khi chưa có kết quả", "P1",
     "—",
     "1. Mở màn, chưa bấm Lọc, bấm Xuất excel",
     "—",
     "- Nút mờ, không mở cửa sổ"),
]


SEC_VIII = [
    ("001", "Tính đến ngày để trống", "P1",
     "—",
     "1. Xóa trống Tính đến ngày, chọn Kho K1",
     "—",
     "- Nút Lọc mờ, không bấm được"),

    ("002", "Hợp đồng gõ một phần số", "P2",
     H1,
     "1. Nhập Hợp đồng \"HD-0\", bấm Lọc",
     "Hợp đồng: HD-0",
     "- Tìm gần đúng: có các lô thuộc HD-01, HD-02, HD-03"),

    ("003", "Hợp đồng không tồn tại", "P2",
     H1,
     "1. Nhập Hợp đồng \"KHONGTONTAI\", bấm Lọc",
     "—",
     "- Bảng ghi \"Chưa có dữ liệu\""),

    ("004", "Bấm Lọc liên tiếp với hai kho", "P2",
     "Kho K1, K2 đều có hàng",
     "1. Chọn K1, bấm Lọc; ngay lập tức đổi K2, bấm Lọc",
     "—",
     "- Bảng chỉ hiện kết quả K2"),
]


SEC_IX = [
    ("001", "Khớp với Thẻ kho", "P0",
     H1,
     "1. Lọc như IV.001, ghi SL tồn H1\n"
     "2. Mở Thẻ kho, chọn H1, Kho K1, Đến ngày hôm nay, bấm Lọc",
     "—",
     "- SL tồn ở báo cáo này (42) bằng Tồn cuối kỳ ở Thẻ kho"),

    ("002", "Khớp với Báo cáo tồn kho theo vị trí", "P1",
     H1,
     "1. So số từng vị trí P1, P2, P3 của H1 với Báo cáo tồn kho theo vị trí",
     "—",
     "- P1 = 26, P2 = 4, P3 = 12 ở cả hai báo cáo"),

    ("003", "Có biến động mới trong lúc đang xem", "P2",
     H1,
     "1. Lọc H1\n"
     "2. Người khác hoàn thành phiếu xuất 2 Cái H1 lô L02 ở P1 của TPE\n"
     "3. Bấm Lọc lại",
     "—",
     "- Bước 3: SL tồn 40, Cộng TPE 28, lô L02 P1 = 4"),
]


SEC_X = [
    ("001", "Luồng nhập, điều chuyển rồi xem báo cáo", "P0",
     "Hàng H6 mới, chưa có tồn ở K1",
     "1. Hoàn thành phiếu nhập kho 20 Cái H6 lô L10 vào P1 cho TPE\n"
     "2. Hoàn thành phiếu điều chuyển vị trí 5 Cái từ P1 sang P2\n"
     "3. " + MENU + ", lọc Kho K1",
     "—",
     "- H6: SL tồn 20, công ty TPE Cộng 20, lô L10 có P1 15, P2 5"),

    ("002", "Luồng kiểm kê có điều chỉnh rồi xem báo cáo", "P0",
     "Hàng H7 ở K1 tồn 10 Cái (TPE, lô L11, P1)",
     "1. Lập phiếu kiểm kê, Thực kiểm H7 = 7, duyệt, xử lý bằng phiếu xuất kho điều chỉnh và hoàn thành\n"
     "2. Lọc báo cáo kho K1",
     "—",
     "- H7: SL tồn 7, lô L11 P1 = 7"),

    ("003", "Luồng xuất hết hàng", "P1",
     "Hàng H8 ở K1 tồn 3 Cái",
     "1. Hoàn thành phiếu xuất kho 3 Cái H8\n"
     "2. Lọc báo cáo kho K1 tính đến hôm nay",
     "—",
     "- Không còn dòng H8"),
]
