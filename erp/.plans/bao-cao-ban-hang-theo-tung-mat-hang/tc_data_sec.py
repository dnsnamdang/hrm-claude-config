# -*- coding: utf-8 -*-
"""Section I - X cho man Bao cao ban hang theo tung mat hang."""
from tc_data_role import MENU, DATA, KT, LOC_T10, LOC_T11

KTD = KT + "\n" + DATA

SEC_I = [
    ("001", "Bố cục mặc định của màn", "P0",
     KT,
     "1. " + MENU + "\n"
     "2. Quan sát từ trên xuống",
     "—",
     "- Tiêu đề trang \"Báo cáo bán hàng theo mặt hàng\"\n"
     "- Bộ lọc: Phòng ban, Bộ phận, Nhân viên, Khách hàng, Hình thức bán, Thương hiệu, Hãng sản xuất, Nhóm "
     "hàng hóa, Tính chất hàng hóa, Loại hàng hóa, Mã sản phẩm, Tên sản phẩm, Mã hợp đồng, Từ ngày (bắt "
     "buộc), Đến ngày (bắt buộc), Kho\n"
     "- Nút Lọc (mờ), làm mới, In, Xuất excel\n"
     "- Bảng ghi \"Chưa có dữ liệu\", chưa tự lọc"),

    ("002", "Cột của bảng", "P0",
     KTD,
     "1. " + LOC_T10,
     "—",
     "- Cột: STT, Mã hàng, Tên hàng, Thương hiệu, Hãng SX, ĐVT, Tồn kho ngày đầu (01/10/2026), Tồn kho "
     "ngày đến (31/10/2026), SL bán, SL trả lại, SL bán thực tế, Đơn giá bán, Thành tiền bán, Đơn giá net, "
     "Thành tiền net, Chênh lệch, Thời gian bảo hành (tháng), ĐM đàm phán giá\n"
     "- Không có cột Đơn giá vốn, Thành tiền vốn, Lãi lỗ"),

    ("003", "Ngày đã chọn hiện dưới tên cột tồn kho", "P2",
     KT,
     "1. Chọn Từ ngày 01/10/2026, Đến ngày 31/10/2026 (chưa bấm Lọc)",
     "—",
     "- Dưới \"Tồn kho ngày đầu\" hiện (01/10/2026), dưới \"Tồn kho ngày đến\" hiện (31/10/2026)"),

    ("004", "Biểu tượng đang tải", "P2",
     KT,
     "1. " + LOC_T10 + ", quan sát ngay",
     "—",
     "- Bảng hiện \"Đang tải dữ liệu\"; nút Lọc, In, Xuất excel mờ đến khi xong"),

    ("005", "Khoảng ngày không có phát sinh", "P1",
     KT + "; không có phiếu bán nào năm 2020",
     "1. Chọn Từ ngày 01/01/2020, Đến ngày 31/12/2020, bấm Lọc",
     "—",
     "- Bảng ghi \"Chưa có dữ liệu\"; dòng Tổng cộng trống"),

    ("006", "Tên trang khác tên menu", "P2",
     KT,
     "1. " + MENU + ", xem tiêu đề tab trình duyệt",
     "—",
     "- Mong đợi: thống nhất với menu \"Báo cáo bán hàng theo từng mặt hàng\"\n"
     "- Lưu ý: theo code hiện tại ghi \"Báo cáo bán hàng theo mặt hàng\" - ghi Failed nếu cần thống nhất"),
]


SEC_II = [
    ("001", "Thiếu Từ ngày / Đến ngày", "P0",
     KT,
     "1. Chỉ chọn Từ ngày 01/10/2026, để trống Đến ngày",
     "—",
     "- Nút Lọc mờ, không bấm được"),

    ("002", "In / Xuất excel khi thiếu ngày", "P1",
     KT,
     "1. Để trống Từ ngày, Đến ngày, bấm In\n"
     "2. Bấm Xuất excel",
     "—",
     "- Cả 2 lần báo \"Vui lòng chọn đầy đủ \"Từ ngày\" và \"Đến ngày\".\", không mở bản in, không tải file"),

    ("003", "Lọc theo khoảng ngày", "P0",
     KTD,
     "1. " + LOC_T11,
     "—",
     "- Chỉ có H1: SL bán 4, SL trả lại \"-\", SL bán thực tế 4, Thành tiền bán 4.000.000 (PXH-03)\n"
     "- Không có H2"),

    ("004", "Ngày đầu và ngày cuối được tính trọn ngày", "P0",
     KTD,
     "1. Chọn Từ ngày 05/10/2026, Đến ngày 05/10/2026, bấm Lọc",
     "—",
     "- Có H1 SL bán 10 (PXH-01 tạo trong ngày 05/10/2026)"),

    ("005", "Từ ngày sau Đến ngày", "P2",
     KT,
     "1. Chọn Từ ngày 31/10/2026, Đến ngày 01/10/2026, bấm Lọc",
     "—",
     "- Mong đợi: báo lỗi khoảng ngày\n"
     "- Lưu ý: theo code hiện tại không chặn, bảng ra \"Chưa có dữ liệu\" - ghi Failed"),

    ("006", "Lọc Phòng ban", "P0",
     KTD,
     "1. Chọn Phòng ban PKD2\n"
     "2. " + LOC_T10,
     "—",
     "- Chỉ có H2 (SL bán 5)"),

    ("007", "Lọc Nhân viên - hàng bán xuất kho", "P0",
     KTD,
     "1. Chọn Nhân viên NV-C\n"
     "2. " + LOC_T10,
     "—",
     "- Chỉ có H2 SL bán 5"),

    ("008", "Lọc Nhân viên - hàng có trả lại", "P0",
     KTD,
     "1. Chọn Nhân viên NV-A\n"
     "2. " + LOC_T10 + ", xem dòng H1",
     "—",
     "- Mong đợi: SL bán 12, SL trả lại 2, SL bán thực tế 10, Thành tiền bán 10.000.000\n"
     "- Lưu ý: theo code hiện tại SL trả lại \"-\", SL bán thực tế 12, Thành tiền bán 12.000.000 (phiếu trả "
     "lại xét theo người lập phiếu nhập TK-1) - ghi Failed"),

    ("009", "Lọc Khách hàng", "P0",
     KTD,
     "1. Chọn Khách hàng KH-02\n"
     "2. " + LOC_T10,
     "—",
     "- H1 SL bán 2 (BM-01), H2 SL bán 5 (PXH-02)"),

    ("010", "Lọc Hình thức bán - Xuất bán hàng", "P0",
     KTD + "\n- 08/10/2026 PXH-KM xuất khuyến mại HD-01: H1 = 3",
     "1. Chọn Hình thức bán \"Xuất bán hàng\"\n"
     "2. " + LOC_T10,
     "—",
     "- H1 SL bán 12 (không gồm 3 cái khuyến mại), SL trả lại 2"),

    ("011", "Lọc Hình thức bán - Xuất khuyến mại", "P0",
     KTD + "\n- 08/10/2026 PXH-KM xuất khuyến mại HD-01: H1 = 3",
     "1. Chọn Hình thức bán \"Xuất khuyến mại\"\n"
     "2. " + LOC_T10,
     "—",
     "- H1 SL bán 3, SL trả lại \"-\" (khuyến mại không trừ trả lại)"),

    ("012", "Lọc Thương hiệu / Hãng sản xuất chọn nhiều", "P1",
     KTD + "; H1 thương hiệu TH-A, H2 thương hiệu TH-B",
     "1. Chọn Thương hiệu TH-A và TH-B\n"
     "2. " + LOC_T10 + "\n"
     "3. Bỏ TH-B, bấm Lọc",
     "—",
     "- Bước 2: có H1 và H2\n"
     "- Bước 3: chỉ có H1"),

    ("013", "Lọc Nhóm / Tính chất / Loại hàng hóa", "P1",
     KTD + "; H2 thuộc nhóm NH-2",
     "1. Chọn Nhóm hàng hóa NH-2\n"
     "2. " + LOC_T10,
     "—",
     "- Chỉ có H2"),

    ("014", "Lọc Mã / Tên sản phẩm theo một phần", "P1",
     KTD + "; mã H1 là JONN-AR020060",
     "1. Nhập Mã sản phẩm \"AR0200\"\n"
     "2. " + LOC_T10,
     "—",
     "- Có H1, không có H2"),

    ("015", "Lọc Mã hợp đồng theo một phần", "P0",
     KTD + "; số HD-02 là TPE.HD.2026-0222",
     "1. Nhập Mã hợp đồng \"2026-0222\"\n"
     "2. " + LOC_T10,
     "—",
     "- Chỉ có H1 SL bán 2 (BM-01 của HD-02)"),

    ("016", "Lọc Mã hợp đồng: trả lại theo hợp đồng của phiếu bán gốc", "P1",
     KTD,
     "1. Nhập Mã hợp đồng của HD-01\n"
     "2. " + LOC_T10,
     "—",
     "- H1: SL bán 10, SL trả lại 2, SL bán thực tế 8"),

    ("017", "Lọc Kho", "P0",
     KTD,
     "1. Chọn Kho K2\n"
     "2. " + LOC_T10,
     "—",
     "- Chỉ có H2 (PXH-02 tại K2)"),

    ("018", "Ô Kho đổi theo Công ty", "P1",
     "TGD có quyền phạm vi Tổng công ty; TPC có kho C1",
     "1. Mở ô Kho\n"
     "2. Chọn Công ty TPC, mở lại ô Kho",
     "—",
     "- Bước 1: kho của mọi công ty\n"
     "- Bước 2: chỉ kho của TPC (có C1)"),

    ("019", "Nút làm mới", "P1",
     KTD,
     "1. Chọn Khách hàng KH-02, Kho K1, " + LOC_T10 + "\n"
     "2. Bấm nút làm mới",
     "—",
     "- Mọi ô lọc về trống (kể cả Từ ngày, Đến ngày), nút Lọc mờ\n"
     "- Bảng vẫn giữ kết quả cũ cho tới lần Lọc sau"),
]


SEC_III = [
    ("001", "Số liệu hàng có xuất bán và bán khi mượn", "P0",
     KTD,
     "1. " + LOC_T10 + ", xem dòng H1",
     "—",
     "- SL bán 12 (PXH-01 10 + BM-01 2), SL trả lại 2, SL bán thực tế 10\n"
     "- Đơn giá bán 1.000.000, Thành tiền bán 10.000.000\n"
     "- Đơn giá net 900.000, Thành tiền net 9.000.000, Chênh lệch 1.000.000"),

    ("002", "Hàng không có giảm giá", "P0",
     KTD,
     "1. " + LOC_T10 + ", xem dòng H2",
     "—",
     "- SL bán 5, SL trả lại \"-\", SL bán thực tế 5\n"
     "- Đơn giá bán 2.000.000, Thành tiền bán 10.000.000, Đơn giá net 2.000.000, Thành tiền net 10.000.000, "
     "Chênh lệch 0"),

    ("003", "Phiếu xuất chưa hoàn thành không tính", "P0",
     KTD + "\n- 25/10/2026 PXH-04 xuất bán H2 = 7, phiếu đang tạo",
     "1. " + LOC_T10 + ", xem dòng H2",
     "—",
     "- H2 vẫn SL bán 5"),

    ("004", "Phiếu xuất loại khác không tính", "P0",
     KTD + "\n- 26/10/2026 phiếu xuất điều chuyển H2 = 4 đã hoàn thành",
     "1. " + LOC_T10,
     "—",
     "- H2 vẫn SL bán 5"),

    ("005", "Phiếu xuất bảo dưỡng - sửa chữa được tính", "P1",
     KTD + "\n- 22/10/2026 PXH-BD xuất bảo dưỡng - sửa chữa hợp đồng dịch vụ DV-01: H2 = 1, đơn giá 2.000.000",
     "1. " + LOC_T10,
     "—",
     "- H2 SL bán 6, Thành tiền bán 12.000.000"),

    ("006", "Xuất khuyến mại giá 0 kéo đơn giá xuống", "P1",
     KTD + "\n- 08/10/2026 PXH-KM xuất khuyến mại HD-01: H1 = 4, đơn giá 0",
     "1. Để Hình thức bán \"Tất cả\"\n"
     "2. " + LOC_T10 + ", xem dòng H1",
     "—",
     "- SL bán 16, SL trả lại 2, SL bán thực tế 14\n"
     "- Theo code hiện tại: Đơn giá bán 750.000 (12.000.000 chia 16), Thành tiền bán 10.500.000\n"
     "- Lưu ý: nếu nghiệp vụ yêu cầu Thành tiền bán 10.000.000 (khuyến mại không có tiền) thì ghi Failed"),

    ("007", "Phiếu bán khi mượn chỉ tính khi đã duyệt", "P0",
     KTD + "\n- 28/10/2026 BM-02 bán khi mượn H1 = 1, chưa duyệt",
     "1. " + LOC_T10,
     "—",
     "- H1 vẫn SL bán 12"),

    ("008", "Bán khi mượn bằng ĐVT lớn quy về ĐVT cơ bản", "P1",
     "H3 ĐVT cơ bản Cái, thêm ĐVT Thùng hệ số 12; 14/10/2026 BM-03 bán khi mượn H3 = 2 Thùng, đơn giá "
     "1.500.000 / Thùng",
     "1. " + LOC_T10 + ", xem dòng H3",
     "—",
     "- ĐVT Cái; SL bán 24; Thành tiền bán 3.000.000; Đơn giá bán 125.000"),

    ("009", "Xuất bán bằng ĐVT lớn quy về ĐVT cơ bản", "P1",
     "H3 như trên; 16/10/2026 PXH-05 xuất bán H3 = 1 Thùng, đơn giá 1.200.000 / Thùng",
     "1. " + LOC_T10 + ", xem dòng H3",
     "—",
     "- Phần của PXH-05: SL 12 Cái, thành tiền 1.200.000"),

    ("010", "Hàng chỉ có trả lại trong kỳ, không còn bán thực tế", "P1",
     "H4: 02/10/2026 PXH-06 bán 1 cái giá 500.000; 30/10/2026 trả lại 1 cái",
     "1. " + LOC_T10 + ", xem dòng H4",
     "—",
     "- SL bán 1, SL trả lại 1, SL bán thực tế \"-\"\n"
     "- Đơn giá bán 500.000, Thành tiền bán 0"),

    ("011", "Ô số bằng 0 hiển thị dấu gạch", "P2",
     KTD,
     "1. " + LOC_T10 + ", xem SL trả lại của H2",
     "—",
     "- Hiện \"-\""),
]


SEC_IV = [
    ("001", "Trả lại trong kỳ của phiếu bán trong kỳ được trừ", "P0",
     KTD,
     "1. " + LOC_T10 + ", xem dòng H1",
     "—",
     "- SL trả lại 2, SL bán thực tế 10"),

    ("002", "Phiếu bán kỳ trước, trả lại kỳ này", "P1",
     KTD + "\n- 10/11/2026 PNH-TL2 nhập trả lại 1 cái H1 của PXH-01 (bán 05/10/2026)",
     "1. " + LOC_T11 + ", xem dòng H1\n"
     "2. " + LOC_T10 + ", xem dòng H1",
     "—",
     "- Theo code hiện tại: bước 1 SL trả lại \"-\" (phiếu bán gốc ngoài kỳ); bước 2 SL trả lại 2 (phiếu "
     "trả ngoài kỳ)\n"
     "- Lưu ý: 1 cái trả lại không bị trừ ở kỳ nào - ghi Failed nếu nghiệp vụ yêu cầu trừ ở kỳ trả lại"),

    ("003", "Nhập trả lại chưa hoàn thành không trừ", "P0",
     KTD + "\n- 25/10/2026 PNH-TL3 trả lại H1 = 1, phiếu đang tạo",
     "1. " + LOC_T10,
     "—",
     "- H1 SL trả lại 2"),

    ("004", "Trả lại hàng bán khi mượn", "P0",
     KTD + "\n- 18/10/2026 PNH-TL4 nhập hàng bán (khi mượn) trả lại của BM-01: H1 = 1",
     "1. " + LOC_T10,
     "—",
     "- H1 SL trả lại 3, SL bán thực tế 9, Thành tiền bán 9.000.000"),

    ("005", "Lọc Kho áp cho phiếu trả lại theo kho nhập", "P1",
     KTD + "; PNH-TL1 nhập về K2; BM-01 lấy hàng ở K2",
     "1. Chọn Kho K1\n"
     "2. " + LOC_T10,
     "—",
     "- H1 SL bán 10 (PXH-01 tại K1), SL trả lại \"-\" (phiếu trả về K2)\n"
     "- Lưu ý: ghi để nghiệp vụ quyết lọc kho theo kho xuất hay kho nhập trả"),

    ("006", "Lọc Khách hàng áp cho phiếu trả lại", "P1",
     KTD,
     "1. Chọn Khách hàng KH-01\n"
     "2. " + LOC_T10,
     "—",
     "- H1: SL bán 10, SL trả lại 2, SL bán thực tế 8"),
]


SEC_V = [
    ("001", "Tồn kho ngày đầu và ngày đến", "P0",
     KTD + "; tồn kế toán H1 của TPE: 30/09/2026 còn 50; sau các phiếu tháng 10 còn 40",
     "1. " + LOC_T10 + ", xem dòng H1",
     "—",
     "- Tồn kho ngày đầu 50 (đến trước 01/10/2026)\n"
     "- Tồn kho ngày đến 40 (đến hết 31/10/2026)"),

    ("002", "Tồn kho không theo ô Kho đang lọc", "P1",
     KTD + "; tồn kế toán H1: K1 30, K2 20 vào 30/09/2026",
     "1. Chọn Kho K1\n"
     "2. " + LOC_T10 + ", xem Tồn kho ngày đầu của H1",
     "—",
     "- Mong đợi: 30 (tồn của K1)\n"
     "- Lưu ý: theo code hiện tại hiện 50 (tồn cả công ty) - ghi Failed nếu nghiệp vụ yêu cầu theo kho"),

    ("003", "Tồn kho theo công ty đang lọc", "P1",
     "TGD quyền Tổng công ty; tồn kế toán H1 30/09/2026: TPE 50, TPC 7",
     "1. " + LOC_T10 + "\n"
     "2. Chọn Công ty TPC, bấm Lọc",
     "—",
     "- Bước 1: Tồn kho ngày đầu 57\n"
     "- Bước 2: Tồn kho ngày đầu 7"),

    ("004", "Thời gian bảo hành quy ra tháng", "P1",
     KTD,
     "1. " + LOC_T10,
     "—",
     "- H1 (1 năm): 12\n"
     "- H2 (90 ngày): 3"),

    ("005", "Hàng chưa khai bảo hành", "P2",
     "H5 không có thời gian bảo hành, có bán trong tháng 10/2026",
     "1. " + LOC_T10 + ", xem dòng H5",
     "—",
     "- Thời gian bảo hành \"-\""),

    ("006", "ĐM đàm phán giá theo bảng giá công ty", "P1",
     KTD + "; bảng giá ĐVT Cái của H1: TPE giảm tối đa 10%, TPC 15%",
     "1. Đăng nhập KT-1, " + LOC_T10,
     "—",
     "- H1 ĐM đàm phán giá 10"),
]


SEC_VI = [
    ("001", "Mở cửa sổ chi tiết", "P0",
     KTD,
     "1. " + LOC_T10 + "\n"
     "2. Bấm Mã hàng của H1",
     "—",
     "- Cửa sổ \"Chi tiết phát sinh của <mã> - <tên H1>\"\n"
     "- 2 dòng: HD-01 (KH-01) SL bán 10; HD-02 (KH-02) SL bán 2\n"
     "- Cột Đơn vị là Cái; không có cột Đơn giá vốn, Thành tiền vốn, Lãi lỗ"),

    ("002", "Cửa sổ chi tiết không trừ hàng trả lại", "P0",
     KTD,
     "1. " + LOC_T10 + ", bấm Mã hàng của H1",
     "—",
     "- Mong đợi: dòng HD-01 SL trả lại 2, SL bán thực tế 8; tổng khớp dòng chính (thực tế 10)\n"
     "- Lưu ý: theo code hiện tại SL trả lại \"-\", HD-01 SL bán thực tế 10, cộng cửa sổ ra 12 - ghi Failed"),

    ("003", "Số tiền từng dòng của cửa sổ", "P0",
     KTD,
     "1. " + LOC_T10 + ", bấm Mã hàng của H1, xem dòng HD-01",
     "—",
     "- Đơn giá bán 1.000.000, Thành tiền bán 10.000.000\n"
     "- Đơn giá net 900.000, Thành tiền net 9.000.000, Chênh lệch 1.000.000"),

    ("004", "Cửa sổ giữ bộ lọc của màn chính", "P0",
     KTD,
     "1. Chọn Khách hàng KH-02, " + LOC_T10 + "\n"
     "2. Bấm Mã hàng của H1",
     "—",
     "- Chỉ có dòng HD-02 SL bán 2"),

    ("005", "Bấm số hợp đồng mở hợp đồng", "P1",
     KTD + "\n- 22/10/2026 PXH-BD xuất bảo dưỡng - sửa chữa DV-01: H2 = 1",
     "1. " + LOC_T10 + ", bấm Mã hàng H1, bấm HD-01\n"
     "2. Mở chi tiết H2, bấm DV-01",
     "—",
     "- Bước 1: mở tab mới chi tiết hợp đồng hãng HD-01\n"
     "- Bước 2: mở tab mới chi tiết hợp đồng dịch vụ DV-01"),

    ("006", "Phân trang cửa sổ chi tiết", "P2",
     "H1 có 25 phiếu xuất bán trong tháng 10/2026",
     "1. " + LOC_T10 + ", bấm Mã hàng H1\n"
     "2. Bấm trang 2 của cửa sổ",
     "—",
     "- Trang 1: 20 dòng, STT 1 đến 20\n"
     "- Trang 2: 5 dòng, STT 21 đến 25"),

    ("007", "Mở lại cửa sổ hàng khác về trang 1", "P2",
     "H1 có 25 dòng chi tiết; H2 có 3 dòng",
     "1. Mở chi tiết H1, sang trang 2, đóng cửa sổ\n"
     "2. Bấm Mã hàng H2",
     "—",
     "- Cửa sổ ở trang 1, có 3 dòng của H2"),
]


SEC_VII = [
    ("001", "Dòng Tổng cộng", "P0",
     KTD,
     "1. " + LOC_T10,
     "—",
     "- SL bán 17, SL trả lại 2, SL bán thực tế 15\n"
     "- Thành tiền bán 20.000.000, Thành tiền net 19.000.000, Chênh lệch 1.000.000"),

    ("002", "Tổng cộng tính mọi trang", "P0",
     "Tháng 10/2026 có 25 mặt hàng bán được",
     "1. " + LOC_T10 + "\n"
     "2. Ghi lại Tổng cộng, sang trang 2",
     "—",
     "- Trang 1: 20 hàng, trang 2: 5 hàng\n"
     "- Tổng cộng giống nhau ở 2 trang, bằng tổng 25 hàng"),

    ("003", "STT liên tục qua trang", "P1",
     "Tháng 10/2026 có 25 mặt hàng",
     "1. " + LOC_T10 + ", sang trang 2",
     "—",
     "- STT trang 2 từ 21 đến 25"),

    ("004", "Lọc lại quay về trang 1", "P2",
     "Tháng 10/2026 có 25 mặt hàng",
     "1. " + LOC_T10 + ", sang trang 2\n"
     "2. Bấm Lọc",
     "—",
     "- Bảng về trang 1"),
]


SEC_VIII = [
    ("001", "In theo bộ lọc", "P0",
     KTD,
     "1. Chọn Phòng ban PKD1, " + LOC_T10 + "\n"
     "2. Bấm In",
     "—",
     "- Mở tab bản in ngang, có đầu trang công ty\n"
     "- Bảng in đủ cột như màn (không có giá vốn, lãi lỗ); chỉ có H1, số liệu như trên màn\n"
     "- Tên cột tồn kho ghi (Ngày 01/10/2026), (Ngày 31/10/2026)"),

    ("002", "In lấy đủ mọi trang", "P0",
     "Tháng 10/2026 có 25 mặt hàng",
     "1. " + LOC_T10 + ", bấm In",
     "—",
     "- Bản in có đủ 25 hàng, dòng TỔNG CỘNG khớp màn"),

    ("003", "Xuất excel dưới 2000 hàng", "P0",
     KTD,
     "1. " + LOC_T10 + ", bấm Xuất excel",
     "—",
     "- Tải file \"bao_cao_ban_hang_theo_mat_hang.xlsx\"\n"
     "- Tiêu đề \"Báo cáo bán hàng theo mặt hàng\"; có H1, H2 và dòng TỔNG CỘNG như màn"),

    ("004", "Số trong file Excel làm tròn", "P2",
     KTD + "\n- 08/10/2026 PXH-KM xuất khuyến mại HD-01: H1 = 6, đơn giá 0",
     "1. Bấm Xuất excel tháng 10/2026, xem Đơn giá bán H1",
     "—",
     "- File ghi số nguyên (666667), trên màn 666.667"),

    ("005", "Tồn kho trống trong file Excel", "P2",
     "H6 chưa từng có tồn kế toán trước 01/10/2026, có bán trong tháng 10",
     "1. Xem Tồn kho ngày đầu của H6 trên màn và trong file Excel",
     "—",
     "- Mong đợi: màn và file thống nhất\n"
     "- Lưu ý: theo code hiện tại màn hiện \"-\", file ghi 0 - ghi Failed nếu cần thống nhất"),

    ("006", "Xuất excel từ 2000 hàng trở lên gửi email", "P1",
     "Năm 2025 có 2100 mặt hàng bán được; KT-1 có email kt1@tpe.vn",
     "1. Chọn Từ ngày 01/01/2025, Đến ngày 31/12/2025, bấm Xuất excel",
     "—",
     "- Báo \"Báo cáo bán hàng theo mặt hàng sẽ được gửi về mail sau ít phút!\"\n"
     "- Vài phút sau kt1@tpe.vn nhận email có file Excel đủ 2100 hàng"),

    ("007", "In / Excel theo phạm vi quyền", "P0",
     "TP-1 phạm vi Phòng ban PKD1\n" + DATA,
     "1. Đăng nhập TP-1, " + LOC_T10 + ", bấm In, bấm Xuất excel",
     "—",
     "- Bản in và file chỉ có H1, không có H2 của PKD2"),
]


SEC_IX = [
    ("001", "Đối chiếu với Báo cáo tổng hợp bán hàng", "P0",
     "KT-1 có thêm quyền \"Xem báo cáo tổng hợp bán hàng\" phạm vi Công ty\n" + DATA,
     "1. " + LOC_T10 + " ở màn này\n"
     "2. Mở \"Báo cáo tổng hợp bán hàng\", cùng khoảng ngày",
     "—",
     "- SL bán, SL trả lại, SL bán thực tế, Thành tiền bán, Thành tiền net, Chênh lệch từng hàng giống nhau\n"
     "- Màn tổng hợp có thêm Đơn giá vốn, Thành tiền vốn, Lãi lỗ"),

    ("002", "Đối chiếu với phiếu xuất hàng", "P0",
     KTD,
     "1. " + LOC_T10 + ", ghi SL bán của H2\n"
     "2. Mở PXH-02, xem SL xuất H2",
     "—",
     "- Cùng là 5"),

    ("003", "Màn chỉ xem, không đổi dữ liệu", "P1",
     KTD,
     "1. Lọc, mở chi tiết, In, Xuất excel nhiều lần\n"
     "2. Mở lại PXH-01, HD-01",
     "—",
     "- Phiếu và hợp đồng không thay đổi"),

    ("004", "Lọc Mã hợp đồng có ký tự đặc biệt", "P1",
     KT,
     "1. Nhập Mã hợp đồng \"' OR 1=1 --\"\n"
     "2. " + LOC_T10,
     "—",
     "- Bảng \"Chưa có dữ liệu\", không báo lỗi hệ thống"),

    ("005", "Nhân viên chuyển phòng", "P2",
     KTD + "; 01/11/2026 NV-A chuyển sang PKD2",
     "1. Chọn Phòng ban PKD1, " + LOC_T10,
     "—",
     "- Theo code hiện tại: H1 SL bán 10 (PXH-01 theo phòng trên phiếu yêu cầu); phần BM-01 chuyển theo "
     "phòng mới của NV-A nên không có\n"
     "- Lưu ý: ghi để nghiệp vụ quyết, nếu cần cùng một cách thì ghi Failed"),

    ("006", "Hai người lọc cùng lúc", "P2",
     KTD + "; TP-1 phạm vi Phòng ban PKD1",
     "1. KT-1 và TP-1 cùng bấm Lọc tháng 10/2026",
     "—",
     "- KT-1 thấy H1, H2; TP-1 chỉ thấy H1"),
]


SEC_X = [
    ("001", "Bán - trả lại - xem báo cáo", "P0",
     KT + "; NV-A có HD-01 bán H1 đơn giá 1.000.000, giảm giá tối đa 10%",
     "1. Hoàn thành phiếu xuất bán HD-01: H1 = 10, ngày 05/10/2026\n"
     "2. Mở báo cáo, " + LOC_T10 + "\n"
     "3. Hoàn thành phiếu nhập hàng bán trả lại 2 cái của phiếu trên, ngày 20/10/2026\n"
     "4. Bấm Lọc lại",
     "—",
     "- Bước 2: H1 SL bán 10, SL bán thực tế 10, Thành tiền bán 10.000.000\n"
     "- Bước 4: SL trả lại 2, SL bán thực tế 8, Thành tiền bán 8.000.000, Thành tiền net 7.200.000"),

    ("002", "Bán khi mượn vào báo cáo", "P0",
     KT + "; NV-A cho KH-02 mượn 2 cái H1",
     "1. Lập và duyệt phiếu bán khi mượn 2 cái H1 giá 1.000.000 ngày 12/10/2026\n"
     "2. Mở báo cáo, " + LOC_T10,
     "—",
     "- H1 có thêm SL bán 2, Thành tiền bán thêm 2.000.000\n"
     "- Cửa sổ chi tiết H1 có dòng HD-02"),

    ("003", "Phiếu xuất bị hủy rời báo cáo", "P1",
     KTD,
     "1. " + LOC_T10 + ", ghi SL bán H2 (5)\n"
     "2. Hủy / đưa PXH-02 về chưa hoàn thành\n"
     "3. Bấm Lọc lại",
     "—",
     "- Bước 3: không còn H2"),
]
