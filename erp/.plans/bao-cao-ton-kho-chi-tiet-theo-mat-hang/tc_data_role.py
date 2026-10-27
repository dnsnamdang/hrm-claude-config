# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Bao cao ton kho chi tiet theo mat hang'."""

MENU = "Mở menu Kho > mục \"Báo cáo kho\" > bấm \"Báo cáo tồn kho chi tiết theo mặt hàng\""

# Du lieu mau dung chung
H1 = ("Kho K1 có 2 công ty thuê kho TPE, TPC. Hàng H1 (ĐVT Cái, thêm ĐVT Thùng hệ số 12) đang tồn:\n"
      "- TPE: lô L01 (nhập từ phiếu NK-1 thuộc hợp đồng HD-01) vị trí P1 = 20, P2 = 4; lô L02 vị trí P1 = 6\n"
      "- TPC: lô L03 vị trí P3 = 12\n"
      "Hàng H2 ở K1 đã xuất hết (tồn 0)")

LOC = "Chọn Tồn theo công ty TPE, Kho K1, Tính đến ngày hôm nay, bấm Lọc"

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Báo cáo tồn kho chi tiết theo mặt hàng: cho biết tại MỘT kho, tính đến một ngày, mỗi mặt hàng còn "
     "tồn bao nhiêu, chia theo Công ty thuê kho > Lô > Vị trí; lô gắn hợp đồng thì kèm số hợp đồng và "
     "thông tin khách hàng.\n"
     "Người dùng làm được: lọc theo kho, công ty thuê kho, nhóm / tính chất / loại hàng, thương hiệu, hãng "
     "sản xuất, hàng hóa, hợp đồng; đổi đơn vị tính từng hàng; Xuất Excel đầy đủ hoặc ngắn gọn. Màn chỉ "
     "xem, không sửa dữ liệu."),

    ("2. Đối tượng được tính / hiển thị",
     "- Mặt hàng có tổng tồn (của các Công ty thuê kho đang chọn) khác 0 tại kho đã chọn, tính tới hết "
     "ngày ở ô \"Tính đến ngày\".\n"
     "- Trong mỗi hàng: từng Công ty thuê kho có tồn lớn hơn 0; trong công ty là từng lô; trong lô là từng "
     "vị trí còn số lượng lớn hơn 0.\n"
     "- Lô nhập từ phiếu nhập có hợp đồng: hiện \"Hợp đồng: <số>\" (bấm mở hợp đồng) và khách hàng, ngày "
     "đặt hàng, ngày trả hàng.\n"
     "- Sắp theo tên hàng A đến Z, 20 hàng mỗi trang."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Hàng có tổng tồn bằng 0 tại kho.\n"
     "- Công ty thuê kho có tồn bằng 0 hoặc âm (không hiện dòng công ty).\n"
     "- Vị trí / lô đã hết hàng.\n"
     "- Công ty thuê kho bị bỏ chọn ở bộ lọc.\n"
     "- Nút In đang bị ẩn, chỉ có Xuất excel."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Chỉ có 1 ô \"Tính đến ngày\" (bắt buộc, mặc định hôm nay): SL tồn và Cộng của từng công ty tính tới "
     "hết ngày này (tính trọn ngày).\n"
     "Lưu ý: theo code hiện tại số lượng từng Lô / Vị trí luôn là số HIỆN TẠI, không tính lùi theo ngày."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Bộ lọc: Tính đến ngày, Tồn theo công ty, Kho (chọn 1, bắt buộc), Công ty thuê kho (tự chọn hết theo "
     "kho), Nhóm hàng hóa, Tính chất hàng hóa, Loại hàng hóa, Thương hiệu, Hãng sản xuất, Hàng hóa (có nút x "
     "để bỏ), Hợp đồng; nút Xuất excel, Lọc, nút làm mới.\n"
     "Bảng: STT, Tên hàng hóa, Model, Mã hàng, Thương hiệu, ĐVT (chọn được), SL tồn, Chi tiết gồm Công "
     "ty > Lô (kèm hợp đồng, khách hàng) > Vị trí > SL, Cộng (tổng của công ty)."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- SL tồn của hàng = tổng Cộng của các công ty được hiện.\n"
     "- Cộng của công ty = tổng tồn của công ty đó tại kho tính đến ngày.\n"
     "- Đổi ĐVT: mọi số của hàng đó chia cho hệ số, làm tròn số nguyên khi hiển thị.\n"
     "Với dữ liệu mẫu H1, ĐVT Cái: SL tồn 42; TPE Cộng 30 (L01: P1 20, P2 4; L02: P1 6); TPC Cộng 12 "
     "(L03: P3 12)."),

    ("7. Phân quyền cấp",
     "- Mở màn và Xuất Excel cần một trong 3 quyền: \"Xem báo cáo tồn kho theo tổng công ty\", \"... theo "
     "công ty\", \"... theo kho\"; không có thì ra trang không tìm thấy.\n"
     "- Quyền theo tổng công ty: ô Tồn theo công ty có mọi công ty; quyền khác chỉ có công ty mình.\n"
     "- Quyền \"theo kho\" hiện cho xem mọi kho của công ty như quyền \"theo công ty\".\n"
     "- Chức năng lấy dữ liệu khi bấm Lọc KHÔNG kiểm tra quyền.\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- Phân trang 20 hàng mỗi trang, STT liên tục qua các trang.\n"
     "- Xuất Excel: dưới 150 hàng thì tải file ngay; từ 150 hàng trở lên thì hệ thống gửi file về email và "
     "báo \"Báo cáo tồn kho chi tiết theo mặt hàng sẽ gửi về mail của bạn trong ít phút!\"."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- Chọn Tính đến ngày trong quá khứ: SL tồn, Cộng đúng theo ngày nhưng số Lô / Vị trí là số hiện tại, "
     "lô đã hết hàng sau ngày đó bị mất.\n"
     "- Đổi ĐVT sang Thùng làm tròn số nguyên (42 Cái hiện 4 Thùng thay vì 3,5).\n"
     "- Bấm nút làm mới thì ô Kho trống danh sách, phải đổi công ty rồi đổi lại mới chọn được kho.\n"
     "- Lô có hợp đồng nhưng hợp đồng chưa có thông tin khách hàng thì không hiện số hợp đồng; ngày đặt / "
     "trả hàng để trống lại hiện ngày hôm nay.\n"
     "- File Excel luôn theo ĐVT nhỏ nhất, không theo ĐVT đang chọn trên màn."),
]


ROLE_TCS = [
    ("00", "Không có quyền xem báo cáo tồn kho thì không mở được màn", "P0",
     "NV-A không có quyền nào trong 3 quyền xem báo cáo tồn kho",
     "1. Đăng nhập NV-A\n"
     "2. " + MENU,
     "Tài khoản: NV-A",
     "- Ra trang không tìm thấy"),

    ("01", "Quyền theo công ty mở được màn", "P0",
     "KT-1 có quyền \"Xem báo cáo tồn kho theo công ty\", thuộc TPE",
     "1. Đăng nhập KT-1\n"
     "2. " + MENU,
     "—",
     "- Tiêu đề \"BÁO CÁO TỒN KHO CHI TIẾT THEO MẶT HÀNG\"\n"
     "- Tính đến ngày = hôm nay, Tồn theo công ty = TPE, ô Tồn theo công ty chỉ có TPE\n"
     "- Bảng ghi \"Chưa có dữ liệu\""),

    ("02", "Quyền theo tổng công ty thấy mọi công ty", "P0",
     "KT-2 có quyền \"Xem báo cáo tồn kho theo tổng công ty\"",
     "1. Đăng nhập KT-2, mở màn\n"
     "2. Mở ô Tồn theo công ty",
     "—",
     "- Liệt kê mọi công ty, mặc định chọn công ty của KT-2"),

    ("03", "Quyền theo kho chỉ nên thấy kho được phân", "P1",
     "TK-3 có quyền \"Xem báo cáo tồn kho theo kho\", thuộc TPE, chỉ được phân kho K1; TPE có K1, K2",
     "1. Đăng nhập TK-3, mở ô Kho",
     "—",
     "- Mong đợi: chỉ có K1\n"
     "- Lưu ý: nếu có cả K2 thì ghi Failed (quyền theo kho đang được đối xử như theo công ty)"),

    ("04", "Gọi thẳng chức năng lấy dữ liệu khi không có quyền", "P1",
     "NV-A không có quyền xem báo cáo tồn kho",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng lấy dữ liệu báo cáo với Kho K1",
     "—",
     "- Mong đợi: bị chặn\n"
     "- Lưu ý: theo code hiện tại trả về đủ số liệu tồn - ghi Failed"),

    ("05", "Xuất Excel qua đường dẫn khi không có quyền", "P1",
     "NV-A không có quyền xem báo cáo tồn kho; KT-1 đã copy đường dẫn Xuất Excel",
     "1. Đăng nhập NV-A, dán đường dẫn Xuất Excel",
     "—",
     "- Ra trang không tìm thấy, không tải được file"),

    ("06", "Không chọn được công ty khác khi chỉ có quyền theo công ty", "P0",
     "KT-1 chỉ có quyền theo công ty (TPE); kho K5 thuộc TPC",
     "1. Mở ô Tồn theo công ty và ô Kho",
     "—",
     "- Không có TPC, không có K5"),
]
