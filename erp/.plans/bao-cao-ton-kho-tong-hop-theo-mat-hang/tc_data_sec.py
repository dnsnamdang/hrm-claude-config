# -*- coding: utf-8 -*-
"""Section I - IX cho man Bao cao ton kho tong hop theo mat hang."""
from tc_data_role import MENU, H1

SEC_I = [
    ("001", "Bố cục mặc định của màn", "P0",
     "KT-2 có quyền xem theo tổng công ty, thuộc TPE",
     "1. " + MENU + "\n"
     "2. Quan sát từ trên xuống",
     "—",
     "- Bộ lọc: Tính đến ngày (hôm nay), Nhóm, Tính chất, Loại hàng hóa, Thương hiệu, Hãng sản xuất, Hàng "
     "hóa, Hợp đồng, Tồn theo công ty (TPE), ô \"Xem toàn bộ kho\" đã tích, Kho (chọn sẵn mọi kho của TPE), "
     "Công ty thuê kho\n"
     "- Nút Xuất excel (mờ), Lọc, làm mới\n"
     "- Khu Chi tiết ghi \"Chưa có dữ liệu\""),

    ("002", "Lọc với mặc định", "P0",
     H1,
     "1. Mở màn, bấm Lọc ngay",
     "—",
     "- Có H1 SL tồn 50, không có H2\n"
     "- Bảng có cột STT, Tên hàng hóa, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn\n"
     "- Nút Xuất excel sáng lên"),

    ("003", "Không có nút In", "P2",
     "—",
     "1. Quan sát hàng nút",
     "—",
     "- Chỉ có Xuất excel, Lọc, làm mới"),

    ("004", "Biểu tượng đang tải", "P2",
     H1,
     "1. Bấm Lọc, quan sát ngay",
     "—",
     "- Nút hiện vòng xoay, khu Chi tiết hiện \"Đang tải dữ liệu\""),
]


SEC_II = [
    ("001", "Bỏ tích Xem toàn bộ kho", "P0",
     H1,
     "1. Bỏ tích \"Xem toàn bộ kho\"",
     "—",
     "- Ô Kho và Công ty thuê kho bị xóa trống\n"
     "- Nút Lọc mờ"),

    ("002", "Chọn một kho", "P0",
     H1,
     "1. Bỏ tích Xem toàn bộ kho, chọn Kho K1, bấm Lọc",
     "Kho: K1",
     "- Ô Công ty thuê kho tự có TPE, TPC đều được chọn\n"
     "- H1: SL tồn 42"),

    ("003", "Chọn nhiều kho cộng gộp", "P0",
     H1,
     "1. Chọn Kho K1 và K2, bấm Lọc",
     "Kho: K1, K2",
     "- H1: SL tồn 50"),

    ("004", "Bỏ một Công ty thuê kho", "P0",
     H1,
     "1. Chọn Kho K1, K2; bỏ TPC ở ô Công ty thuê kho, bấm Lọc",
     "—",
     "- H1: SL tồn 38\n"
     "- Với quyền tổng công ty: chỉ còn cột TPE"),

    ("005", "Tích lại Xem toàn bộ kho", "P1",
     "Đang chọn riêng K1",
     "1. Tích lại \"Xem toàn bộ kho\"",
     "—",
     "- Ô Kho chọn lại mọi kho của công ty"),

    ("006", "Đổi Tồn theo công ty", "P0",
     "KT-2 có quyền tổng công ty; TPC có kho K5",
     "1. Đổi Tồn theo công ty sang TPC",
     "—",
     "- Ô Xem toàn bộ kho tích lại, ô Kho chọn sẵn mọi kho của TPC (K5), không còn K1, K2"),

    ("007", "Lọc theo Hàng hóa", "P0",
     H1 + "\nCòn tồn H4",
     "1. Chọn Hàng hóa H1 qua nút tìm, bấm Lọc\n"
     "2. Bấm x ở ô Hàng hóa, bấm Lọc",
     "—",
     "- Bước 1: chỉ có H1\n"
     "- Bước 2: có H1 và H4"),

    ("008", "Lọc theo Nhóm, Tính chất, Loại hàng hóa", "P1",
     "H1 nhóm \"Máy in\", loại \"Thiết bị\"; H4 nhóm \"Mực in\"",
     "1. Chọn Nhóm \"Máy in\", bấm Lọc\n"
     "2. Bỏ nhóm, chọn Loại \"Thiết bị\", bấm Lọc",
     "—",
     "- Cả 2 bước: chỉ có H1"),

    ("009", "Lọc theo Thương hiệu, Hãng sản xuất", "P1",
     "H1 thương hiệu Canon; H4 thương hiệu HP",
     "1. Chọn Thương hiệu Canon, bấm Lọc",
     "—",
     "- Chỉ có H1"),

    ("010", "Lọc theo Hợp đồng", "P1",
     H1 + "\n10 Cái H1 ở K1 của TPE nhập từ phiếu nhập thuộc hợp đồng HD-01",
     "1. Nhập Hợp đồng \"HD-01\", bấm Lọc",
     "Hợp đồng: HD-01",
     "- Chỉ có H1, SL tồn là phần liên quan hợp đồng HD-01 (10 trừ phần đã xuất theo hợp đồng)"),

    ("011", "Không có kết quả", "P2",
     H1,
     "1. Chọn Hàng hóa H1, Thương hiệu HP, bấm Lọc",
     "—",
     "- Ghi \"Chưa có dữ liệu\", nút Xuất excel mờ"),

    ("012", "Nút làm mới", "P1",
     "Đang tích Xem toàn bộ kho, đã chọn nhóm hàng, hàng hóa",
     "1. Bấm nút làm mới",
     "—",
     "- Các ô lọc về trống, Tính đến ngày về hôm nay\n"
     "- Mong đợi: Xem toàn bộ kho vẫn tích, Kho chọn sẵn mọi kho\n"
     "- Lưu ý: theo code hiện tại ô Xem toàn bộ kho bị bỏ tích, ô Kho trống - ghi Failed"),
]


SEC_III = [
    ("001", "Tính đến hôm nay", "P0",
     H1,
     "1. Chọn K1, K2, bấm Lọc",
     "—",
     "- H1: SL tồn 50"),

    ("002", "Tính đến ngày trong quá khứ", "P0",
     H1 + "\nNgày 20/10 xuất 5 Cái H1 ở K1 của TPE",
     "1. Chọn Tính đến ngày 19/10, bấm Lọc",
     "Tính đến ngày: 19/10",
     "- H1: SL tồn 55, cột TPE 43"),

    ("003", "Tính trọn ngày", "P1",
     H1 + "\nNgày 15/10 lúc 17:00 nhập thêm 3 Cái H1 ở K2",
     "1. Chọn Tính đến ngày 15/10, bấm Lọc\n"
     "2. Chọn 14/10, bấm Lọc",
     "—",
     "- Bước 1 có tính 3 Cái nhập lúc 17:00; bước 2 không tính"),

    ("004", "Tính đến ngày trước khi có hàng", "P2",
     "H1 nhập lần đầu ngày 01/03",
     "1. Chọn Tính đến ngày 28/02, bấm Lọc",
     "—",
     "- Không có H1"),

    ("005", "Để trống Tính đến ngày", "P1",
     "—",
     "1. Xóa trống Tính đến ngày",
     "—",
     "- Nút Lọc mờ"),
]


SEC_IV = [
    ("001", "Cột Chi tiết theo Công ty thuê kho", "P0",
     "KT-2 có quyền tổng công ty\n" + H1,
     "1. Chọn K1, K2, bấm Lọc\n"
     "2. Rê chuột vào tiêu đề cột",
     "—",
     "- Có cột TPE, TPC; H1: TPE 38 (K1 30 + K2 8), TPC 12\n"
     "- Rê chuột hiện mã công ty"),

    ("002", "SL tồn bằng tổng các cột Chi tiết", "P0",
     "Như IV.001",
     "1. Cộng các cột Chi tiết của H1",
     "—",
     "- 38 + 12 = 50 bằng SL tồn"),

    ("003", "Công ty không có tồn hiện dấu gạch", "P1",
     "KT-2 có quyền tổng công ty; hàng H4 chỉ có tồn của TPE",
     "1. Lọc K1, K2, đọc dòng H4",
     "—",
     "- Cột TPC hiện \"-\""),

    ("004", "Công ty thuê kho tồn âm", "P2",
     "KT-2 có quyền tổng công ty; H5 ở K1: TPE 10, TPC -2",
     "1. Lọc K1, đọc dòng H5",
     "—",
     "- Cột TPE 10, TPC -2, SL tồn 8"),

    ("005", "Hàng tồn 0 không hiện", "P0",
     H1,
     "1. Lọc K1, K2",
     "—",
     "- Không có H2"),
]


SEC_V = [
    ("001", "Đổi ĐVT sang Thùng", "P0",
     "KT-2 có quyền tổng công ty\n" + H1,
     "1. Lọc K1, K2, chọn ĐVT Thùng ở H1",
     "ĐVT: Thùng",
     "- Cột TPE 3.17, TPC 1\n"
     "- Mong đợi: SL tồn 4,17\n"
     "- Lưu ý: theo code hiện tại SL tồn hiện 4 (làm tròn) - ghi Failed nếu cần số lẻ"),

    ("002", "ĐVT đã đổi được giữ khi lọc lại", "P1",
     H1,
     "1. Đổi ĐVT H1 sang Thùng\n"
     "2. Đổi Tính đến ngày, bấm Lọc lại",
     "—",
     "- H1 vẫn ở ĐVT Thùng"),

    ("003", "Đổi ĐVT chỉ ảnh hưởng hàng đó", "P2",
     H1 + "\nCòn tồn H4",
     "1. Đổi ĐVT H1 sang Thùng",
     "—",
     "- Số của H4 giữ nguyên"),
]


SEC_VI = [
    ("001", "Phân trang 20 hàng", "P1",
     "Các kho đã chọn có 45 mặt hàng còn tồn",
     "1. Lọc, chuyển sang trang 3",
     "—",
     "- Có 3 trang; trang 3 có 5 hàng, STT từ 41 đến 45"),

    ("002", "Sắp xếp theo tên hàng", "P2",
     "Có hàng tên \"Bút\", \"Ấm\", \"Cân\"",
     "1. Lọc",
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
     "- Bước 1: cửa sổ \"Xuất Excel\" có Xuất excel đầy đủ, Xuất excel ngắn gọn\n"
     "- Bước 2: báo \"Vui lòng chọn mẫu xuất excel.\""),

    ("002", "Xuất excel đầy đủ", "P0",
     "KT-2 có quyền tổng công ty\n" + H1,
     "1. Lọc K1, K2, Xuất excel đầy đủ",
     "Mẫu: đầy đủ",
     "- Tải file \"bao_cao_ton_kho_tong_hop_mat_hang.xlsx\"\n"
     "- Phần đầu ghi các kho \"K1 - <tên>,K2 - <tên>\", ngày tính đến\n"
     "- H1: SL tồn 50, cột TPE 38, TPC 12"),

    ("003", "Xuất excel ngắn gọn", "P0",
     H1,
     "1. Lọc K1, K2, Xuất excel ngắn gọn",
     "Mẫu: ngắn gọn",
     "- File có H1 SL tồn 50, không có cột theo công ty thuê kho"),

    ("004", "File theo ĐVT đã đổi", "P1",
     H1,
     "1. Đổi ĐVT H1 sang Thùng, Xuất excel đầy đủ",
     "—",
     "- H1: ĐVT \"Thùng (x12)\", SL tồn 4.17"),

    ("005", "Xuất từ 500 hàng trở lên", "P1",
     "Các kho đã chọn có 520 mặt hàng còn tồn; KT-2 có email",
     "1. Lọc, Xuất excel ngắn gọn",
     "—",
     "- Không tải ngay, báo \"Báo cáo tồn kho tổng hợp sẽ gửi về mail của bạn trong ít phút!\"\n"
     "- Vài phút sau email nhận được file"),

    ("006", "Xuất theo bộ lọc đang chọn", "P1",
     H1 + "\nCòn tồn H4",
     "1. Chọn Hàng hóa H1, Lọc, Xuất excel ngắn gọn",
     "—",
     "- File chỉ có H1"),
]


SEC_VIII = [
    ("001", "Khớp với Báo cáo tồn kho chi tiết theo mặt hàng", "P0",
     H1,
     "1. Lọc báo cáo này chỉ với K1, ghi SL tồn H1\n"
     "2. Mở Báo cáo tồn kho chi tiết theo mặt hàng, chọn K1, Lọc",
     "—",
     "- Cả hai cùng SL tồn H1 = 42"),

    ("002", "Khớp với Thẻ kho", "P1",
     H1,
     "1. Lọc báo cáo này với K1, K2\n"
     "2. Mở Thẻ kho, chọn H1, Kho K1 và K2, Lọc",
     "—",
     "- SL tồn 50 bằng Tồn cuối kỳ ở Thẻ kho"),

    ("003", "Bấm Lọc liên tiếp", "P2",
     H1,
     "1. Bấm Lọc với K1, ngay lập tức đổi sang K2 bấm Lọc",
     "—",
     "- Chỉ hiện kết quả của K2"),

    ("004", "Có biến động mới trong lúc đang xem", "P2",
     H1,
     "1. Lọc\n"
     "2. Người khác hoàn thành phiếu xuất 2 Cái H1 ở K2\n"
     "3. Bấm Lọc lại",
     "—",
     "- Bước 3: H1 SL tồn 48"),
]


SEC_IX = [
    ("001", "Luồng nhập, xuất rồi xem báo cáo", "P0",
     "Hàng H6 mới; công ty TPE có kho K1, K2",
     "1. Hoàn thành phiếu nhập 20 Cái H6 vào K1, 10 Cái vào K2\n"
     "2. Hoàn thành phiếu xuất 5 Cái H6 từ K1\n"
     "3. " + MENU + ", bấm Lọc",
     "—",
     "- H6: SL tồn 25"),

    ("002", "Luồng kiểm kê có điều chỉnh rồi xem báo cáo", "P0",
     "Hàng H7 ở K1 tồn 10 Cái",
     "1. Lập phiếu kiểm kê, Thực kiểm H7 = 12, duyệt, xử lý bằng phiếu nhập kho điều chỉnh và hoàn thành\n"
     "2. Lọc báo cáo",
     "—",
     "- H7: SL tồn 12"),

    ("003", "Luồng xuất hết hàng", "P1",
     "Hàng H8 tồn 3 Cái ở K1",
     "1. Hoàn thành phiếu xuất 3 Cái H8\n"
     "2. Lọc báo cáo",
     "—",
     "- Không còn H8"),
]
