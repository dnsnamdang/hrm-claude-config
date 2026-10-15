# -*- coding: utf-8 -*-
"""Phan dung chung cho 3 bo testcase ERP bao cao cong no khach hang.

- COT_SO_LIEU: giai thich 8 cot so lay tu phieu nao (doc tu AccountDetail::getReportData,
  CustomerDebtDetailByEmployeeService, SaleReportService::getDebtReconciliationReport).
- data_change_tcs(screen): bo TC "tao phieu goc -> bao cao tang/giam dung", dung cho ca 3 man,
  khac nhau o cho quan sat va 2 diem ky quac cua man Doi chieu.
"""

MENU_YCXH = "menu Khởi tạo > Hàng hóa > Nhập - xuất hàng > 'Phiếu Yêu cầu xuất hàng'"
MENU_YCNH = "menu Khởi tạo > Hàng hóa > Nhập - xuất hàng > 'Phiếu Yêu cầu nhập hàng'"
MENU_PT = "menu Kế toán > Quản lý tiền > 'Phiếu thu'"
MENU_BC = "menu Kế toán > Quản lý tiền > 'Phiếu báo có'"
MENU_PC = "menu Kế toán > Quản lý tiền > 'Phiếu chi'"
MENU_UNC = "menu Kế toán > Quản lý tiền > 'Phiếu ủy nhiệm chi'"
MENU_DCCN = "menu Kế toán > nhóm Điều chỉnh công nợ > 'Yêu cầu điều chỉnh công nợ'"
MENU_HTDV = "menu Kế toán > 'Yêu cầu hạch toán dịch vụ - HĐBH' / 'Phiếu hạch toán dịch vụ - HĐBH'"
SO_CHI_TIET = "'Sổ chi tiết công nợ phải thu khách hàng' (menu Kế toán, nhóm Khách hàng)"

COT_SO_LIEU = (
    "Cả 3 báo cáo đọc cùng một nguồn: các bút toán ghi vào tài khoản phải thu khách hàng 131 (kể cả "
    "tài khoản con) khi một phiếu được HẠCH TOÁN. Ngày dùng để lọc là NGÀY HẠCH TOÁN của phiếu. Phiếu "
    "mới lập / chờ duyệt / chưa hạch toán thì chưa có bút toán nên chưa làm báo cáo thay đổi.\n"
    "Cột số liệu và loại phiếu làm nó thay đổi:\n"
    "- Số dư đầu kỳ: mọi phát sinh có ngày hạch toán TRƯỚC Từ ngày (nợ trừ có).\n"
    "- Phát sinh tăng / Hàng hóa-Dịch vụ: phiếu xuất kho bán hàng, phiếu xuất bán hàng mượn, phiếu hạch "
    "toán dịch vụ, phiếu hạch toán dịch vụ BH-SC, biên bản thanh lý, khai báo đầu kỳ công nợ (phần ghi "
    "tăng); trừ đi phần ghi giảm của chính các phiếu đó.\n"
    "- Phát sinh tăng / Điều chỉnh công nợ: phiếu điều chỉnh công nợ ghi TĂNG nợ khách.\n"
    "- Phát sinh giảm / Nhập trả lại: phiếu nhập hàng khách trả lại.\n"
    "- Phát sinh giảm / Đã thanh toán: phiếu thu, phiếu báo có, khai báo đầu kỳ công nợ (phần đã thu).\n"
    "- Phát sinh giảm / Điều chỉnh công nợ: phiếu điều chỉnh công nợ ghi GIẢM nợ khách.\n"
    "- Trả lại tiền thừa: phiếu chi, phiếu ủy nhiệm chi trả tiền lại cho khách.\n"
    "- Số dư cuối kỳ = Đầu kỳ + Cộng tăng - Cộng giảm + Trả lại tiền thừa. Số dương là khách còn nợ "
    "(Dư nợ), số âm là khách trả thừa (Dư có)."
)

DU_LIEU_MAU = (
    "Dữ liệu mẫu dùng xuyên suốt nhóm test 'Tạo phiếu - số liệu thay đổi': khách hàng KH-TEST, hợp đồng "
    "bán hàng HD-TEST-01 do nhân viên A (phòng P1, bộ phận BP1) lập, đã ký. Kỳ lọc: Từ ngày = ngày 1 "
    "tháng hiện tại, Đến ngày = hôm nay. Trước mỗi bước CHỤP LẠI số liệu để so (gọi là 'số nền'). Nếu "
    "tài khoản tester không lập / duyệt được phiếu nào thì nhờ kế toán lập giúp, chỉ cần đúng khách "
    "hàng, hợp đồng, số tiền và ngày hạch toán."
)


def _where(screen):
    if screen == "detail":
        return ("dòng hợp đồng HD-TEST-01, dòng khách hàng KH-TEST (dòng đậm phía trên) và dòng "
                "Tổng cộng")
    if screen == "employee":
        return ("dòng hợp đồng HD-TEST-01, dòng nhân viên A (dòng đậm phía trên) và dòng Tổng cộng")
    return "dòng hợp đồng HD-TEST-01 (dòng đậm), dòng chứng từ mới bên dưới và dòng Tổng cộng"


def _filter(screen):
    if screen == "compare":
        return "Từ ngày = ngày 1 tháng này, Đến ngày = hôm nay, Khách hàng = KH-TEST, bấm 'Lọc'"
    return ("Từ ngày = ngày 1 tháng này, Đến ngày = hôm nay, Khách hàng = KH-TEST, bấm 'Lọc'")


def data_change_tcs(screen):
    """screen: 'detail' | 'employee' | 'compare'."""
    w = _where(screen)
    f = _filter(screen)
    cmp_ = screen == "compare"
    tcs = []

    tcs.append(("001", "Ghi lại số nền trước khi tạo phiếu", "P0",
                "Đã có KH-TEST và HD-TEST-01 như mô tả mục 9",
                "1. Mở báo cáo, nhập: " + f + "\n"
                "2. Chụp màn hình " + w + "\n"
                "3. Mở thêm " + SO_CHI_TIET + " cùng khách hàng, cùng kỳ, chụp lại số dư cuối kỳ",
                "KH-TEST, HD-TEST-01",
                "- Có đủ số liệu 8 cột để làm số nền cho các TC sau\n"
                "- Số dư cuối kỳ của khách trên báo cáo khớp với sổ chi tiết công nợ phải thu"))

    tcs.append(("002", "Phiếu xuất kho bán hàng làm tăng cột Hàng hóa/Dịch vụ", "P0",
                "Đã có số nền (TC trước)",
                "1. Vào " + MENU_YCXH + ", lập yêu cầu xuất hàng cho HD-TEST-01, giá trị 10,000,000, duyệt\n"
                "2. Kho lập và duyệt phiếu xuất kho cho yêu cầu đó (ngày hạch toán hôm nay)\n"
                "3. Quay lại báo cáo, lọc lại như số nền",
                "Giá trị xuất: 10,000,000",
                "- Cột 'Hàng hóa/Dịch vụ' tăng đúng 10,000,000 ở " + w + "\n"
                "- Cột 'Cộng' phát sinh tăng và 'Số dư cuối kì' tăng 10,000,000"
                + ("" if cmp_ else "") +
                ("\n- Có thêm dòng chứng từ: Ngày chứng từ hôm nay, Số chứng từ = mã phiếu xuất (kèm mã "
                 "yêu cầu xuất hàng trong ngoặc)" if cmp_ else "")))

    tcs.append(("003", "Phiếu chưa hạch toán không làm đổi báo cáo", "P0",
                "Số nền đã cập nhật sau TC trước",
                "1. Lập thêm một yêu cầu xuất hàng 5,000,000 cho HD-TEST-01, CHƯA xuất kho\n"
                "2. Lập một phiếu thu 1,000,000 cho HD-TEST-01, để ở trạng thái chưa duyệt / chưa hạch toán\n"
                "3. Lọc lại báo cáo",
                "",
                "- Không cột nào thay đổi so với số nền\n"
                "- Sau khi hoàn tất xuất kho / hạch toán thì báo cáo mới tăng (kiểm ở các TC sau)"))

    tcs.append(("004", "Phiếu thu làm tăng cột Đã thanh toán", "P0",
                "Đã có số nền mới",
                "1. Vào " + MENU_PT + ", lập phiếu thu của KH-TEST, chọn hợp đồng HD-TEST-01, số tiền "
                "4,000,000, duyệt và hạch toán hôm nay\n2. Lọc lại báo cáo",
                "Số tiền thu: 4,000,000",
                "- Cột 'Đã thanh toán' tăng 4,000,000 ở " + w + "\n"
                "- Cột 'Cộng' phát sinh giảm tăng 4,000,000; 'Số dư cuối kì' giảm 4,000,000"
                + ("\n- Dòng chứng từ mới có Số chứng từ = mã phiếu thu, bấm vào mở đúng phiếu thu" if cmp_ else "")))

    tcs.append(("005", "Phiếu báo có làm tăng cột Đã thanh toán", "P1",
                "Đã có số nền mới",
                "1. Vào " + MENU_BC + ", lập phiếu báo có của KH-TEST cho HD-TEST-01, 1,000,000, hạch toán "
                "hôm nay\n2. Lọc lại báo cáo",
                "1,000,000",
                "- Cột 'Đã thanh toán' tăng 1,000,000; 'Số dư cuối kì' giảm 1,000,000 ở " + w))

    dccn_tang_cmp = ("\n- Ghi nhận (giữ nguyên như hiện tại, không ghi Failed): ở dòng hợp đồng, 'Số dư cuối "
                     "kì' KHÔNG đổi vì màn này không tính 2 cột Điều chỉnh công nợ vào số dư của từng hợp "
                     "đồng; chỉ dòng Tổng cộng tăng 2,000,000" if cmp_ else
                     "\n- 'Số dư cuối kì' tăng 2,000,000")
    tcs.append(("006", "Điều chỉnh công nợ TĂNG", "P0",
                "Đã có số nền mới",
                "1. Vào " + MENU_DCCN + ", lập yêu cầu điều chỉnh TĂNG công nợ KH-TEST, hợp đồng HD-TEST-01, "
                "2,000,000; duyệt đủ các cấp để kế toán lập phiếu điều chỉnh, ngày hạch toán hôm nay\n"
                "2. Lọc lại báo cáo",
                "Tăng 2,000,000",
                "- Cột 'Điều chỉnh công nợ' thuộc nhóm Phát sinh TĂNG tăng 2,000,000 ở " + w
                + dccn_tang_cmp))

    dccn_giam_cmp = ("\n- Ghi nhận (giữ nguyên): dòng hợp đồng 'Số dư cuối kì' KHÔNG giảm; chỉ dòng Tổng "
                     "cộng giảm 500,000" if cmp_ else "\n- 'Số dư cuối kì' giảm 500,000")
    tcs.append(("007", "Điều chỉnh công nợ GIẢM", "P0",
                "Đã có số nền mới",
                "1. Lập yêu cầu điều chỉnh GIẢM công nợ KH-TEST, HD-TEST-01, 500,000, duyệt và hạch toán "
                "hôm nay\n2. Lọc lại báo cáo",
                "Giảm 500,000",
                "- Cột 'Điều chỉnh công nợ' thuộc nhóm Phát sinh GIẢM tăng 500,000 ở " + w + dccn_giam_cmp))

    tcs.append(("008", "Khách trả lại hàng làm tăng cột Nhập trả lại", "P0",
                "Hợp đồng HD-TEST-01 đã xuất hàng ở TC 002",
                "1. Vào " + MENU_YCNH + ", lập yêu cầu nhập hàng khách trả lại theo HD-TEST-01, giá trị "
                "3,000,000, duyệt\n2. Kho nhập kho, phiếu nhập được hạch toán hôm nay\n3. Lọc lại báo cáo",
                "Trả lại 3,000,000",
                "- Cột 'Nhập trả lại' tăng 3,000,000; 'Số dư cuối kì' giảm 3,000,000 ở " + w
                + ("\n- Dòng chứng từ mới: mã phiếu nhập kèm mã yêu cầu nhập hàng trong ngoặc" if cmp_ else "")))

    tcs.append(("009", "Phiếu chi trả lại tiền thừa", "P1",
                "Đã có số nền mới",
                "1. Vào " + MENU_PC + ", lập phiếu chi trả tiền cho KH-TEST, hợp đồng HD-TEST-01, 200,000, "
                "hạch toán hôm nay\n2. Lọc lại báo cáo",
                "200,000",
                "- Cột 'Trả lại tiền thừa' tăng 200,000; 'Số dư cuối kì' TĂNG 200,000 ở " + w))

    tcs.append(("010", "Phiếu ủy nhiệm chi trả lại tiền thừa", "P2",
                "Đã có số nền mới",
                "1. Vào " + MENU_UNC + ", lập ủy nhiệm chi trả KH-TEST cho HD-TEST-01, 300,000, hạch toán "
                "hôm nay\n2. Lọc lại báo cáo",
                "300,000",
                "- Cột 'Trả lại tiền thừa' tăng 300,000; 'Số dư cuối kì' tăng 300,000"))

    tcs.append(("011", "Phiếu hạch toán dịch vụ làm tăng Hàng hóa/Dịch vụ", "P2",
                "KH-TEST có một hợp đồng dịch vụ bảo hành - sửa chữa HD-TEST-DV",
                "1. Vào " + MENU_HTDV + ", lập và duyệt hạch toán dịch vụ 1,500,000 cho HD-TEST-DV, ngày "
                "hôm nay\n2. Lọc lại báo cáo",
                "1,500,000",
                "- Xuất hiện / tăng dòng hợp đồng HD-TEST-DV, cột 'Hàng hóa/Dịch vụ' tăng 1,500,000\n"
                "- Dòng Tổng cộng tăng tương ứng"))

    tcs.append(("012", "Kiểm tổng sau chuỗi phiếu", "P0",
                "Đã chạy xong TC 002 và 004 đến 010 trên HD-TEST-01",
                "1. Lọc lại báo cáo\n2. So 'Số dư cuối kì' của HD-TEST-01 với số nền ban đầu (TC 001)",
                "",
                "- Chênh lệch = +10,000,000 - 4,000,000 - 1,000,000 + 2,000,000 - 500,000 - 3,000,000 "
                "+ 200,000 + 300,000 = +4,000,000"
                + ("\n- Ghi nhận màn này: dòng hợp đồng chỉ chênh +2,500,000 vì bỏ qua 2 cột Điều chỉnh "
                   "công nợ; dòng Tổng cộng chênh đủ +4,000,000" if cmp_ else
                   "\n- Dòng khách hàng / nhân viên và dòng Tổng cộng chênh đúng +4,000,000")))

    tcs.append(("013", "Phiếu hạch toán TRƯỚC Từ ngày rơi vào Số dư đầu kỳ", "P0",
                "Một phiếu thu 700,000 của KH-TEST cho HD-TEST-01 có ngày hạch toán là ngày cuối tháng trước",
                "1. Lọc kỳ tháng này\n2. Đổi Từ ngày về ngày 1 tháng trước, lọc lại",
                "700,000",
                ("- Bước 1: phiếu này KHÔNG nằm ở cột 'Đã thanh toán'; nằm trong 'Số dư đầu kỳ' của dòng "
                 "Tổng cộng\n- Ghi nhận màn này: 'Số dư đầu kỳ' của dòng hợp đồng luôn trống / bằng 0\n"
                 "- Bước 2: phiếu chuyển sang cột 'Đã thanh toán' và có dòng chứng từ riêng" if cmp_ else
                 "- Bước 1: phiếu này KHÔNG nằm ở cột 'Đã thanh toán' mà làm 'Số dư đầu kỳ' giảm 700,000\n"
                 "- Bước 2: phiếu chuyển sang cột 'Đã thanh toán'; 'Số dư cuối kì' không đổi giữa 2 lần lọc")))

    tcs.append(("014", "Phiếu hạch toán SAU Đến ngày không tính", "P1",
                "Một phiếu thu cho HD-TEST-01 hạch toán hôm nay",
                "1. Lọc Đến ngày = hôm qua\n2. Lọc Đến ngày = hôm nay",
                "",
                "- Bước 1: phiếu không được tính ở cột nào\n- Bước 2: phiếu được tính vào 'Đã thanh toán'"))

    tcs.append(("015", "Hủy / xóa phiếu thì báo cáo trả về như cũ", "P1",
                "Phiếu thu 4,000,000 ở TC 004",
                "1. Kế toán hủy hạch toán (hoặc xóa) phiếu thu đó\n2. Lọc lại báo cáo",
                "",
                "- Cột 'Đã thanh toán' giảm lại 4,000,000; 'Số dư cuối kì' tăng lại 4,000,000"))

    if screen != "compare":
        tcs.append(("016", "Thu vượt làm hợp đồng chuyển sang Dư có", "P1",
                    "HD-TEST-01 đang dư nợ 4,000,000 (sau TC 012)",
                    "1. Lập phiếu thu 5,000,000 cho HD-TEST-01, hạch toán hôm nay\n"
                    "2. Lọc với 'Số dư cuối kỳ' = Dư nợ\n3. Lọc với 'Số dư cuối kỳ' = Dư có",
                    "",
                    "- 'Số dư cuối kì' của HD-TEST-01 = -1,000,000\n"
                    "- Bước 2: HD-TEST-01 không còn trong danh sách\n- Bước 3: HD-TEST-01 có trong danh sách"))

    tcs.append(("017", "Khớp chéo với các báo cáo công nợ khác", "P1",
                "Sau chuỗi phiếu ở trên",
                "1. Lọc cùng kỳ, cùng KH-TEST ở 3 màn: Báo cáo chi tiết công nợ KH, Báo cáo tổng hợp công nợ "
                "khách hàng theo nhân viên, Bảng đối chiếu công nợ 1 khách hàng\n"
                "2. Mở " + SO_CHI_TIET + " cùng kỳ",
                "",
                "- 8 cột của HD-TEST-01 bằng nhau ở màn Chi tiết và màn Theo nhân viên\n"
                "- Dòng Tổng cộng 'Số dư cuối kì' của khách bằng nhau ở cả 3 màn và bằng số dư trên sổ chi "
                "tiết công nợ phải thu\n"
                "- Riêng màn Đối chiếu, dòng hợp đồng khác nhau ở Số dư đầu kỳ / cuối kì như đã ghi nhận\n"
                "- Nếu dòng Tổng cộng lệch giữa các màn: ghi số của từng màn vào cột Ghi chú để đối chiếu"))
    return tcs
