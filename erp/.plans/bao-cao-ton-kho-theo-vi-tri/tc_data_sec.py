# -*- coding: utf-8 -*-
"""Section I - X cho man Bao cao ton kho theo vi tri."""
from tc_data_role import MENU, K1, LOC

SEC_I = [
    ("001", "Bố cục mặc định của màn", "P0",
     "TK-1 có quyền xem theo công ty",
     "1. " + MENU + "\n"
     "2. Quan sát từ trên xuống",
     "—",
     "- Bộ lọc: Tính đến ngày, Nhóm, Tính chất, Loại hàng hóa, Thương hiệu, Hãng sản xuất, Hàng hóa, Hợp "
     "đồng, Tồn theo công ty, Kho (bắt buộc), Công ty thuê kho, 4 khung Nhà, Dãy, Khoang, Vị trí\n"
     "- Nút Xuất excel (mờ), Lọc (mờ), làm mới; không có nút In"),

    ("002", "Lọc lần đầu", "P0",
     K1,
     "1. " + LOC,
     "—",
     "- Bảng có cột STT, Nhà Kho, Vị trí, Tên hàng hóa, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn, Công ty, "
     "Lô, SL, Cộng\n"
     "- 3 vị trí P1, P2, P3 theo thứ tự tên; dòng cuối \"Tổng cộng\" 47"),

    ("003", "Biểu tượng đang tải", "P2",
     K1,
     "1. Bấm Lọc, quan sát ngay",
     "—",
     "- Khu Chi tiết hiện \"Đang tải dữ liệu\""),
]


SEC_II = [
    ("001", "Đổi Tồn theo công ty xóa Kho đã chọn", "P0",
     "TK-2 có quyền tổng công ty; TPC có kho K5",
     "1. Chọn TPE, Kho K1\n"
     "2. Đổi sang TPC, mở ô Kho",
     "—",
     "- Kho, Công ty thuê kho bị xóa; danh sách kho chỉ còn K5"),

    ("002", "Chọn Kho tự chọn hết Công ty thuê kho", "P0",
     K1,
     "1. Chọn Kho K1",
     "—",
     "- Công ty thuê kho tự có TPE, TPC đều được chọn\n"
     "- Khung Nhà có N1; khung Vị trí có mục vị trí tự do P3"),

    ("003", "Bỏ một Công ty thuê kho", "P0",
     K1,
     "1. Chọn Kho K1, bỏ TPC, bấm Lọc",
     "—",
     "- Chỉ còn P1, P2; không có P3\n"
     "- Tổng cộng 35"),

    ("004", "Lọc theo Hàng hóa", "P0",
     K1,
     "1. Chọn Hàng hóa H4, bấm Lọc",
     "—",
     "- Chỉ có vị trí P1 với hàng H4 lô L07 = 5\n"
     "- SL tồn P1 là 5, Tổng cộng 5"),

    ("005", "Lọc theo Thương hiệu, Nhóm, Hãng sản xuất", "P1",
     K1 + "\nH1 thương hiệu Canon nhóm \"Máy in\"; H4 thương hiệu HP nhóm \"Mực in\"",
     "1. Chọn Thương hiệu Canon, bấm Lọc\n"
     "2. Bỏ thương hiệu, chọn Nhóm \"Mực in\", bấm Lọc",
     "—",
     "- Bước 1: P1 (chỉ H1, 26), P2, P3\n"
     "- Bước 2: chỉ P1 với H4"),

    ("006", "Lọc theo Loại hàng hóa", "P1",
     K1 + "\nH1 thuộc loại hàng \"Thiết bị\"",
     "1. Chọn Loại hàng hóa \"Thiết bị\", bấm Lọc",
     "—",
     "- Mong đợi: có các vị trí chứa H1\n"
     "- Lưu ý: nếu bảng ghi \"Chưa có dữ liệu\" thì ghi Failed"),

    ("007", "Lọc theo Hợp đồng", "P1",
     K1 + "\nLô L01 nhập từ phiếu nhập thuộc hợp đồng HD-01",
     "1. Nhập Hợp đồng \"HD-01\", bấm Lọc",
     "Hợp đồng: HD-01",
     "- Chỉ có P1, P2 với lô L01 (20 và 4)\n"
     "- Không có lô L02, L03, L07"),

    ("008", "Không có kết quả", "P2",
     K1,
     "1. Chọn Hàng hóa H1, Thương hiệu HP, bấm Lọc",
     "—",
     "- Ghi \"Chưa có dữ liệu\", nút Xuất excel mờ"),

    ("009", "Nút làm mới", "P1",
     "Đã chọn kho, nhà, hàng hóa và lọc",
     "1. Bấm nút làm mới\n"
     "2. Mở ô Kho",
     "—",
     "- Bước 1: các ô lọc về trống, Tính đến ngày về hôm nay\n"
     "- Mong đợi bước 2: có danh sách kho\n"
     "- Lưu ý: theo code hiện tại ô Kho trống, phải đổi công ty rồi đổi lại - ghi Failed"),
]


SEC_III = [
    ("001", "Lọc theo Nhà", "P0",
     K1,
     "1. Chọn Kho K1, tích Nhà N1, bấm Lọc",
     "Nhà: N1",
     "- Có P1, P2 (cột Nhà Kho là N1); không có P3"),

    ("002", "Lọc theo Dãy, Khoang", "P1",
     K1,
     "1. Tích N1, tích Dãy D1, tích Khoang KH1, bấm Lọc",
     "—",
     "- Có P1, P2; không có P3"),

    ("003", "Chọn từng Vị trí", "P0",
     K1,
     "1. Tích N1 > D1 > KH1, ở khung Vị trí chỉ tích P2, bấm Lọc",
     "Vị trí: P2",
     "- Chỉ có P2, Tổng cộng 4"),

    ("004", "Chọn vị trí tự do", "P0",
     K1,
     "1. Chọn Kho K1, ở khung Vị trí tích P3 (mục vị trí tự do), bấm Lọc",
     "Vị trí: P3",
     "- Chỉ có P3; cột Nhà Kho hiện \"-\"; Tổng cộng 12"),

    ("005", "Khung chọn hiện theo cấp", "P2",
     K1,
     "1. Chọn Kho K1, tích N1, rồi D1, rồi KH1",
     "—",
     "- Khung Dãy hiện D1 sau khi tích N1; khung Khoang hiện KH1 sau khi tích D1; khung Vị trí có thêm mục "
     "vị trí thuộc khoang P1, P2 sau khi tích KH1"),
]


SEC_IV = [
    ("001", "Chi tiết một vị trí nhiều hàng", "P0",
     K1,
     "1. " + LOC + ", đọc vị trí P1",
     "—",
     "- STT 1, Nhà Kho N1, Vị trí P1, SL tồn 31\n"
     "- H1: công ty TPE, lô L01 = 20, lô L02 = 6, Cộng 26\n"
     "- H4: công ty TPE, lô L07 = 5, Cộng 5"),

    ("002", "SL tồn vị trí bằng tổng các Cộng", "P0",
     K1,
     "1. Lọc như IV.001, cộng các ô Cộng của P1",
     "—",
     "- 26 + 5 = 31"),

    ("003", "Tổng cộng bằng tổng SL tồn các vị trí", "P0",
     K1,
     "1. Lọc như IV.001",
     "—",
     "- 31 + 4 + 12 = 47 ở dòng Tổng cộng"),

    ("004", "Vị trí chứa hàng của công ty thuê kho khác", "P1",
     K1,
     "1. Lọc như IV.001, đọc vị trí P3",
     "—",
     "- H1, công ty TPC, lô L03 = 12, Cộng 12"),

    ("005", "Lô hết hàng tại vị trí không hiện", "P1",
     K1 + "\nLô L02 từng có ở P2 nhưng đã chuyển hết sang P1",
     "1. Lọc như IV.001, đọc vị trí P2",
     "—",
     "- P2 chỉ có lô L01, không có dòng L02 bằng 0"),

    ("006", "Vị trí trống không hiện", "P1",
     K1 + "\nVị trí P4 của K1 đã hết hàng",
     "1. Lọc như IV.001",
     "—",
     "- Không có dòng P4"),

    ("007", "Thông tin hợp đồng của lô", "P1",
     K1 + "\nLô L01 thuộc hợp đồng HD-01, khách hàng \"Nguyễn Văn A\" - 0901234567, ngày đặt 01/10, ngày trả "
     "10/10",
     "1. Lọc như IV.001, đọc ô lô L01 ở P1",
     "—",
     "- \"Hợp đồng: HD-01\" bấm mở được hợp đồng\n"
     "- \"Khách hàng: Nguyễn Văn A - 0901234567\", Ngày đặt hàng 01/10, Ngày trả hàng 10/10"),

    ("008", "Hợp đồng chưa có ngày trả hàng", "P2",
     "Lô L05 thuộc hợp đồng HD-02, HD-02 để trống ngày trả hàng",
     "1. Lọc kho chứa L05, đọc ô lô L05",
     "—",
     "- Mong đợi: Ngày trả hàng để trống\n"
     "- Lưu ý: theo code hiện tại hiện ngày hôm nay - ghi Failed"),
]


SEC_V = [
    ("001", "Tính đến ngày trong quá khứ", "P0",
     K1 + "\nNgày 20/10 xuất 5 Cái H1 lô L01 tại P1 của TPE (trước đó L01 tại P1 = 25)",
     "1. Chọn Tính đến ngày 19/10, bấm Lọc, đọc P1",
     "Tính đến ngày: 19/10",
     "- P1: SL tồn 36; H1 lô L01 = 25, Cộng 31\n"
     "- Tổng cộng 52"),

    ("002", "Lô hết hàng sau ngày lọc vẫn hiện", "P1",
     K1 + "\nLô L04 của TPE ở P2 có 8 Cái tới 10/10, ngày 12/10 xuất hết",
     "1. Chọn Tính đến ngày 11/10, bấm Lọc, đọc P2",
     "—",
     "- P2 có lô L04 = 8"),

    ("003", "Điều chuyển vị trí sau ngày lọc", "P1",
     K1 + "\nNgày 21/10 điều chuyển 4 Cái H1 lô L01 từ P2 sang P1",
     "1. Chọn Tính đến ngày 20/10, bấm Lọc\n"
     "2. Chọn Tính đến ngày hôm nay, bấm Lọc",
     "—",
     "- Bước 1: P2 vẫn có L01 = 4\n"
     "- Bước 2: không còn P2, P1 lô L01 = 24"),

    ("004", "Tính trọn ngày", "P2",
     K1 + "\nNgày 15/10 lúc 17:00 nhập thêm 3 Cái H4 vào P1",
     "1. Chọn Tính đến ngày 15/10, bấm Lọc",
     "—",
     "- Đã tính 3 Cái nhập lúc 17:00"),

    ("005", "Để trống Tính đến ngày", "P1",
     "—",
     "1. Xóa trống Tính đến ngày, chọn Kho K1",
     "—",
     "- Nút Lọc mờ"),
]


SEC_VI = [
    ("001", "Đổi ĐVT của một hàng", "P0",
     K1 + "\nH1 có thêm ĐVT Thùng hệ số 12",
     "1. Lọc như IV.001, ở P1 chọn ĐVT Thùng cho H1",
     "ĐVT: Thùng",
     "- H1 tại P1: lô L01 1.67, lô L02 0.5, Cộng 2.17\n"
     "- SL tồn P1 vẫn 31, Tổng cộng vẫn 47; số của H4 không đổi"),

    ("002", "Lô có SL bằng 0 sau quy đổi", "P2",
     K1,
     "1. Lọc như IV.001, quan sát cột SL các lô",
     "—",
     "- Không có lô nào hiện \"0\"; nếu có thì hiện \"-\""),
]


SEC_VII = [
    ("001", "Phân trang 20 vị trí", "P1",
     "Kho K2 có 45 vị trí đang có hàng",
     "1. Lọc kho K2, chuyển sang trang 3",
     "—",
     "- Có 3 trang; trang 3 có 5 vị trí, STT từ 41 đến 45\n"
     "- Dòng Tổng cộng ở mọi trang đều là tổng của cả 45 vị trí"),

    ("002", "Sắp xếp theo tên vị trí", "P2",
     "Kho có vị trí tên \"B-01\", \"A-02\", \"A-01\"",
     "1. Lọc kho đó",
     "—",
     "- Thứ tự A-01, A-02, B-01"),
]


SEC_VIII = [
    ("001", "Mở cửa sổ Xuất Excel", "P1",
     K1,
     "1. Lọc, bấm Xuất excel\n"
     "2. Không chọn mẫu, bấm Xuất EXCEL",
     "—",
     "- Bước 1: cửa sổ \"Xuất Excel\" có mẫu đầy đủ và ngắn gọn\n"
     "- Bước 2: báo \"Vui lòng chọn mẫu xuất excel.\""),

    ("002", "Xuất excel đầy đủ khi dưới 5 vị trí", "P0",
     K1,
     "1. " + LOC + "\n"
     "2. Xuất excel, chọn mẫu đầy đủ, bấm Xuất EXCEL",
     "Mẫu: đầy đủ",
     "- Tải ngay file \"bao_cao_ton_kho_theo_vi_tri.xlsx\"\n"
     "- Phần đầu có Kho \"K1 - <tên kho>\", ngày tính đến\n"
     "- Số liệu P1, P2, P3 và Tổng cộng 47 khớp màn hình"),

    ("003", "Xuất excel ngắn gọn", "P1",
     K1,
     "1. Lọc như VIII.002, Xuất excel mẫu ngắn gọn",
     "Mẫu: ngắn gọn",
     "- Tải file, có đủ 3 vị trí và SL tồn, gọn hơn mẫu đầy đủ"),

    ("004", "Xuất khi từ 5 vị trí trở lên", "P0",
     "Kho K2 có 85 vị trí đang có hàng; TK-1 có quyền xem theo công ty",
     "1. Lọc kho K2, Xuất excel mẫu đầy đủ\n"
     "2. Chờ vài phút, mở menu tài khoản > \"Download File\"",
     "—",
     "- Bước 1: không tải ngay, báo \"Danh sách hàng sẽ được xuất file sau ít phút!.\"\n"
     "- Bước 2: có 3 file \"bao_cao_ton_kho_theo_vi_tri_1...\", \"_2...\", \"_3...\" (40, 40, 5 vị trí), tải "
     "được\n"
     "- Lưu ý: ghi Failed nếu nghiệp vụ cần báo khi xong hoặc 1 file duy nhất"),

    ("005", "Xuất theo bộ lọc vị trí", "P1",
     K1,
     "1. Tích P3, Lọc, Xuất excel mẫu đầy đủ",
     "—",
     "- File chỉ có P3"),
]


SEC_IX = [
    ("001", "Khớp với Báo cáo tồn kho chi tiết theo mặt hàng", "P0",
     K1,
     "1. Lọc báo cáo này với K1, ghi tổng của H1 ở các vị trí\n"
     "2. Mở Báo cáo tồn kho chi tiết theo mặt hàng, chọn K1, đọc H1",
     "—",
     "- Báo cáo này: H1 = 20 + 6 + 4 + 12 = 42\n"
     "- Báo cáo chi tiết: SL tồn H1 = 42, số từng lô / vị trí trùng nhau"),

    ("002", "Khớp với Thẻ kho khi lọc theo vị trí", "P1",
     K1,
     "1. Mở Thẻ kho, chọn H1, Kho K1, tích vị trí P3, loại báo cáo Không nhặt điều chuyển, bấm Lọc",
     "—",
     "- Tồn cuối kỳ 12 bằng số H1 tại P3 ở báo cáo này"),

    ("003", "Bấm Lọc liên tiếp với hai kho", "P2",
     "Kho K1, K2 đều có hàng",
     "1. Chọn K1 bấm Lọc, ngay lập tức đổi K2 bấm Lọc",
     "—",
     "- Chỉ hiện kết quả K2"),

    ("004", "Có biến động mới trong lúc đang xem", "P2",
     K1,
     "1. Lọc\n"
     "2. Người khác hoàn thành phiếu điều chuyển 6 Cái H1 lô L02 từ P1 sang P2\n"
     "3. Bấm Lọc lại",
     "—",
     "- Bước 3: P1 = 25, P2 = 10, Tổng cộng vẫn 47"),
]


SEC_X = [
    ("001", "Luồng nhập vào vị trí rồi xem báo cáo", "P0",
     "Vị trí P5 của K1 đang trống",
     "1. Hoàn thành phiếu nhập kho 15 Cái H6 lô L20 vào P5 cho TPE\n"
     "2. " + MENU + ", lọc Kho K1",
     "—",
     "- Có vị trí P5: H6, TPE, lô L20 = 15, Cộng 15, SL tồn 15"),

    ("002", "Luồng điều chuyển vị trí rồi xem báo cáo", "P0",
     K1,
     "1. Hoàn thành phiếu điều chuyển vị trí 12 Cái H1 lô L03 từ P3 sang P2\n"
     "2. Lọc Kho K1",
     "—",
     "- Không còn P3\n"
     "- P2: H1 có TPE lô L01 = 4 và TPC lô L03 = 12, SL tồn 16; Tổng cộng 47"),

    ("003", "Luồng kiểm kê theo vị trí có điều chỉnh", "P1",
     K1,
     "1. Lập phiếu kiểm kê, Thực kiểm H4 tại P1 = 3, duyệt, xử lý bằng phiếu xuất kho điều chỉnh và hoàn "
     "thành\n"
     "2. Lọc Kho K1",
     "—",
     "- P1: H4 lô L07 = 3, SL tồn 29; Tổng cộng 45"),
]
