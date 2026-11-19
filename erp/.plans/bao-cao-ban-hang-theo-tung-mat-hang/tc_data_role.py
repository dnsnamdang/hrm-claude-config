# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Bao cao ban hang theo tung mat hang'."""

MENU = ("Mở menu Báo cáo > \"Báo cáo bán hàng\" > mục \"Báo cáo tổng hợp và so sánh số liệu bán hàng\" > "
        "bấm \"Báo cáo bán hàng theo từng mặt hàng\"")

# Du lieu mau dung chung (hom nay 16/11/2026)
DATA = ("Công ty TPE: phòng PKD1 (bộ phận BP1) có NV-A, NV-B; phòng PKD2 có NV-C; thủ kho TK-1. Kho K1, K2 "
        "của TPE. Hàng H1 (ĐVT Cái, bảo hành 1 năm, ĐM giảm giá tối đa 10%), H2 (ĐVT Cái, bảo hành 90 "
        "ngày).\n"
        "Phát sinh:\n"
        "- 05/10/2026 PXH-01 xuất bán HD-01 (yêu cầu xuất của NV-A, KH-01) tại K1: H1 = 10, đơn giá bán "
        "1.000.000, giảm giá tối đa 10%\n"
        "- 12/10/2026 BM-01 bán khi mượn HD-02 (NV-A, KH-02): H1 = 2, đơn giá bán 1.000.000, giảm giá tối đa "
        "10%\n"
        "- 15/10/2026 PXH-02 xuất bán HD-03 (NV-C, KH-02) tại K2: H2 = 5, đơn giá bán 2.000.000, không giảm "
        "giá\n"
        "- 20/10/2026 PNH-TL1 nhập hàng bán trả lại của PXH-01 (TK-1 lập phiếu nhập): H1 = 2\n"
        "- 03/11/2026 PXH-03 xuất bán HD-01 (NV-A) tại K1: H1 = 4, đơn giá bán 1.000.000, giảm giá tối đa 10%")

KT = "KT-1 có quyền \"Xem báo cáo bán hàng theo mặt hàng\" phạm vi Công ty, thuộc TPE"

LOC_T10 = "Chọn Từ ngày 01/10/2026, Đến ngày 31/10/2026, bấm Lọc"
LOC_T11 = "Chọn Từ ngày 01/11/2026, Đến ngày 30/11/2026, bấm Lọc"

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Báo cáo bán hàng theo từng mặt hàng: cho biết trong một khoảng ngày mỗi mặt hàng bán được bao nhiêu, "
     "trả lại bao nhiêu, bán thực tế bao nhiêu, thành tiền bán, thành tiền net (sau giảm giá tối đa) và "
     "chênh lệch; kèm tồn kho kế toán ngày đầu, ngày đến, thời gian bảo hành và ĐM đàm phán giá.\n"
     "Người dùng làm được: lọc theo công ty, phòng ban, bộ phận, nhân viên, khách hàng, hình thức bán, "
     "thương hiệu, hãng sản xuất, nhóm / tính chất / loại hàng, mã / tên sản phẩm, mã hợp đồng, kho, "
     "khoảng ngày; bấm Mã hàng mở cửa sổ chi tiết phát sinh theo từng hợp đồng; In, Xuất excel. Màn chỉ "
     "xem, không sửa dữ liệu. Khác màn \"Báo cáo tổng hợp bán hàng\": màn này không có các cột giá vốn và "
     "lãi lỗ."),

    ("2. Đối tượng được tính / hiển thị",
     "- Phiếu xuất hàng đã hoàn thành loại Xuất bán (HĐ hãng), Xuất khuyến mại (HĐ hãng), Xuất bảo dưỡng - "
     "sửa chữa; dòng có SL xuất lớn hơn 0.\n"
     "- Phiếu bán khi mượn (bán hàng đang cho mượn) ở trạng thái đã duyệt / hoàn thành.\n"
     "- Phiếu nhập hàng bán trả lại và nhập hàng bán (khi mượn) trả lại đã hoàn thành: trừ vào SL bán thực "
     "tế, chỉ khi phiếu bán gốc cũng nằm trong khoảng ngày.\n"
     "- Mỗi dòng là 1 mặt hàng, cộng gộp mọi hợp đồng, khách hàng, kho; 20 hàng mỗi trang."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu xuất chưa hoàn thành, phiếu xuất loại khác (điều chuyển, mượn, bảo hành...).\n"
     "- Phiếu trả lại của phiếu bán ngoài khoảng ngày.\n"
     "- Phạm vi quyền: không có quyền thì chỉ tính phiếu do chính mình lập yêu cầu.\n"
     "- Không có các cột Đơn giá vốn, Thành tiền vốn, Lãi lỗ."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Từ ngày, Đến ngày bắt buộc (nút Lọc mờ khi thiếu):\n"
     "- Xuất bán: theo ngày tạo phiếu xuất hàng; bán khi mượn: ngày tạo phiếu bán; trả lại: ngày tạo phiếu "
     "nhập trả lại và ngày phiếu bán gốc.\n"
     "- Tồn kho ngày đầu: tồn kế toán đến trước Từ ngày; Tồn kho ngày đến: đến hết Đến ngày."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Bảng: STT, Mã hàng (bấm mở chi tiết), Tên hàng, Thương hiệu, Hãng SX, ĐVT (ĐVT cơ bản), Tồn kho ngày "
     "đầu, Tồn kho ngày đến, SL bán, SL trả lại, SL bán thực tế, Đơn giá bán, Thành tiền bán, Đơn giá net, "
     "Thành tiền net, Chênh lệch, Thời gian bảo hành (tháng), ĐM đàm phán giá; dòng Tổng cộng ngay dưới "
     "tiêu đề.\n"
     "Cửa sổ chi tiết: STT, Số đơn hàng/HD (bấm mở hợp đồng), Khách hàng, Đơn vị, SL bán, SL trả lại, SL bán "
     "thực tế, Đơn giá bán, Thành tiền bán, Đơn giá net, Thành tiền net, Chênh lệch."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- SL bán = tổng SL xuất bán + bán khi mượn (quy về ĐVT cơ bản); SL trả lại = tổng SL nhập trả lại; "
     "SL bán thực tế = SL bán - SL trả lại.\n"
     "- Đơn giá bán = tổng thành tiền bán gốc chia SL bán; Thành tiền bán = Đơn giá bán x SL bán thực tế.\n"
     "- Đơn giá net = giá bán trừ % giảm giá tối đa của dòng hợp đồng; Thành tiền net = Đơn giá net x SL "
     "bán thực tế; Chênh lệch = Thành tiền bán - Thành tiền net.\n"
     "Với dữ liệu mẫu tháng 10/2026: H1 bán 12, trả lại 2, thực tế 10, Thành tiền bán 10.000.000, net "
     "9.000.000, chênh lệch 1.000.000; H2 bán 5, thực tế 5, Thành tiền 10.000.000."),

    ("7. Phân quyền cấp",
     "- Quyền \"Xem báo cáo bán hàng theo mặt hàng\" có 4 phạm vi: Tổng công ty (mọi công ty, có ô Công "
     "ty), Công ty, Phòng ban (các phòng mình quản lý), Bộ phận.\n"
     "- Không có quyền vẫn mở được màn, chỉ thấy số liệu của phiếu do mình lập yêu cầu.\n"
     "- Chức năng lấy dữ liệu, In, Xuất excel dùng cùng phạm vi.\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- Dòng Tổng cộng = tổng của mọi hàng khớp bộ lọc (kể cả các trang khác).\n"
     "- Thời gian bảo hành: năm x 12, tháng giữ nguyên, ngày chia 30.\n"
     "- ĐM đàm phán giá: % giảm giá tối đa của ĐVT cơ bản trong bảng giá của công ty đang lọc (không lọc "
     "thì công ty của người xem).\n"
     "- Xuất excel: dưới 2000 hàng tải ngay; từ 2000 hàng trở lên gửi về email và báo \"Báo cáo bán hàng "
     "theo mặt hàng sẽ được gửi về mail sau ít phút!\"."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- Lọc Nhân viên (hoặc người không có quyền xem báo cáo): hàng trả lại không được trừ, vì phiếu trả "
     "lại xét theo người lập phiếu nhập (thủ kho), không theo nhân viên bán.\n"
     "- Cửa sổ chi tiết không trừ hàng trả lại: SL trả lại luôn \"-\", tổng cửa sổ lệch dòng chính.\n"
     "- Hàng bán kỳ trước, trả lại kỳ này: không trừ ở kỳ nào.\n"
     "- Có xuất khuyến mại giá 0: Đơn giá bán bị kéo xuống vì chia cả SL khuyến mại.\n"
     "- Tồn kho ngày đầu / ngày đến không theo ô Kho đang lọc."),
]


ROLE_TCS = [
    ("00", "Không có quyền vẫn mở được màn, chỉ thấy phiếu của mình", "P0",
     "NV-A không có quyền \"Xem báo cáo bán hàng theo mặt hàng\"\n" + DATA,
     "1. Đăng nhập NV-A\n"
     "2. " + MENU + "\n"
     "3. " + LOC_T10,
     "Tài khoản: NV-A",
     "- Mở được màn, không có ô Công ty, Phòng ban, Bộ phận, Nhân viên\n"
     "- Chỉ có H1 (từ PXH-01, BM-01), không có H2 của NV-C\n"
     "- Lưu ý: nếu nghiệp vụ yêu cầu chặn người không có quyền thì ghi Failed"),

    ("01", "Không có quyền: hàng trả lại của mình nên được trừ", "P0",
     "NV-A không có quyền xem báo cáo\n" + DATA,
     "1. Đăng nhập NV-A, mở màn\n"
     "2. " + LOC_T10 + ", xem dòng H1",
     "—",
     "- Mong đợi: SL bán 12, SL trả lại 2, SL bán thực tế 10, Thành tiền bán 10.000.000\n"
     "- Lưu ý: theo code hiện tại SL trả lại \"-\", SL bán thực tế 12, Thành tiền bán 12.000.000 (phiếu trả "
     "lại do TK-1 lập nên không thuộc NV-A) - ghi Failed"),

    ("02", "Quyền phạm vi Bộ phận", "P1",
     "TB-1 trưởng bộ phận BP1, quyền phạm vi Bộ phận\n" + DATA,
     "1. Đăng nhập TB-1, mở màn\n"
     "2. " + LOC_T10,
     "—",
     "- Có ô Nhân viên, không có ô Công ty, Phòng ban, Bộ phận\n"
     "- Có H1 của NV-A (thuộc BP1), không có H2 của NV-C"),

    ("03", "Quyền phạm vi Phòng ban", "P0",
     "TP-1 trưởng PKD1, chỉ quản lý PKD1, quyền phạm vi Phòng ban\n" + DATA,
     "1. Đăng nhập TP-1, mở màn\n"
     "2. " + LOC_T10,
     "—",
     "- Có ô Bộ phận, Nhân viên; không có ô Công ty; không có ô Phòng ban (chỉ quản lý 1 phòng)\n"
     "- Có H1 (SL bán thực tế 10), không có H2"),

    ("04", "Phạm vi Phòng ban quản lý nhiều phòng", "P1",
     "TP-2 quản lý cả PKD1, PKD2, quyền phạm vi Phòng ban\n" + DATA,
     "1. Đăng nhập TP-2, mở màn\n"
     "2. " + LOC_T10 + "\n"
     "3. Chọn Phòng ban PKD2, bấm Lọc",
     "—",
     "- Bước 2: có H1 và H2; có ô Phòng ban\n"
     "- Bước 3: chỉ còn H2"),

    ("05", "Quyền phạm vi Công ty", "P0",
     KT + "\n" + DATA,
     "1. Đăng nhập KT-1, mở màn\n"
     "2. " + LOC_T10,
     "—",
     "- Có ô Phòng ban, Bộ phận, Nhân viên; không có ô Công ty\n"
     "- Có H1 và H2 của TPE; không có hàng bán của công ty TPC"),

    ("06", "Quyền phạm vi Tổng công ty", "P0",
     "TGD có quyền phạm vi Tổng công ty; TPC có phiếu xuất bán H1 = 3 ngày 10/10/2026\n" + DATA,
     "1. Đăng nhập TGD, mở màn\n"
     "2. " + LOC_T10 + "\n"
     "3. Chọn Công ty TPE, bấm Lọc",
     "—",
     "- Có ô Công ty\n"
     "- Bước 2: H1 SL bán 15 (TPE 12 + TPC 3)\n"
     "- Bước 3: H1 SL bán 12"),

    ("07", "Gọi thẳng chức năng lấy dữ liệu lấy được giá vốn", "P1",
     KT + "\n" + DATA,
     "1. Dùng công cụ kiểm thử API gọi chức năng lấy dữ liệu báo cáo tháng 10/2026 như KT-1",
     "—",
     "- Mong đợi: dữ liệu trả về không có Đơn giá vốn, Thành tiền vốn, Lãi lỗ (màn này ẩn các cột đó)\n"
     "- Lưu ý: theo code hiện tại dữ liệu trả về có đủ giá vốn và lãi lỗ từng hàng - ghi Failed nếu giá "
     "vốn cần giữ kín"),
]
