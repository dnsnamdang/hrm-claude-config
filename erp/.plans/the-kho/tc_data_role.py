# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'The kho'."""

MENU = "Mở menu Kho > mục \"Báo cáo kho\" > bấm \"Thẻ kho\""

# Du lieu mau dung chung
H1 = ("Hàng H1 (ĐVT cơ bản Cái, có thêm ĐVT Thùng hệ số 12) ở kho K1 của công ty TPE, năm nay:\n"
      "- 05/01: Nhập tồn đầu 24 Cái, vị trí P1 lô L01\n"
      "- 10/03: Phiếu nhập kho NK-1 nhập 36 Cái lô L02 (P1 = 24, P2 = 12)\n"
      "- 15/04: Phiếu xuất kho XK-1 xuất 30 Cái (P1 lô L01 = 20, P1 lô L02 = 10)\n"
      "- 20/05: Phiếu điều chuyển vị trí DCVT-1 chuyển 6 Cái lô L02 từ P1 sang P2")

LOC = ("Chọn hàng H1 qua nút tìm ở ô Hàng hóa, Kho K1, Từ ngày 01/01, Đến ngày hôm nay, Loại báo cáo "
       "\"Tất cả\", bấm Lọc")

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Thẻ kho: báo cáo theo dõi biến động số lượng của MỘT mặt hàng trong một khoảng thời gian, theo kho, "
     "công ty thuê kho và vị trí.\n"
     "Báo cáo gồm khối tổng hợp (Tồn đầu kỳ, Nhập trong kỳ, Xuất trong kỳ, Tồn cuối kỳ) và bảng chi tiết "
     "từng chứng từ làm thay đổi tồn: nhập tồn đầu, phiếu nhập kho, xuất kho, nhập / xuất điều chỉnh kiểm "
     "kê, nhập lại, xuất lại, điều chuyển vị trí; mỗi chứng từ tách theo Lô và Vị trí, kèm SL tồn lũy kế.\n"
     "Người dùng làm được: lọc, đổi đơn vị tính hiển thị, In và Xuất Excel theo kiểu Đầy đủ hoặc Rút gọn. "
     "Màn chỉ xem, không sửa dữ liệu."),

    ("2. Đối tượng được tính / hiển thị",
     "- Mọi lần ghi nhận tăng / giảm tồn của hàng đã chọn tại các vị trí thuộc kho đã chọn (không chọn kho "
     "thì lấy mọi kho của công ty ở ô \"Tồn theo công ty\").\n"
     "- Chỉ tính phần tồn của các Công ty thuê kho đang chọn.\n"
     "- Loại báo cáo \"Tất cả\": có cả dòng điều chuyển vị trí; \"Không nhặt điều chuyển\": bỏ hẳn điều "
     "chuyển vị trí.\n"
     "- Hàng đã ngừng sử dụng (đã xóa) vẫn chọn được ở cửa sổ tìm hàng."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Lần ghi nhận có số lượng thay đổi bằng 0.\n"
     "- Điều chuyển vị trí KHÔNG được cộng vào Nhập trong kỳ / Xuất trong kỳ ở cả 2 loại báo cáo.\n"
     "- Chứng từ chưa ghi nhận vào kho (nháp, chờ duyệt) không hiện.\n"
     "- Kho không được phân cho người dùng không có trong ô Kho."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Từ ngày / Đến ngày lọc theo NGÀY GHI NHẬN vào kho của từng lần nhập / xuất (cột \"Ngày chứng từ\"), "
     "tính trọn hai đầu. Mặc định từ 01/01 năm nay đến hôm nay.\n"
     "Tồn đầu kỳ = tổng mọi biến động trước Từ ngày; để trống Từ ngày thì Tồn đầu kỳ = 0 và lấy toàn bộ "
     "lịch sử."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Bộ lọc: Hàng hóa (bắt buộc, chọn qua cửa sổ), Tồn theo công ty, Kho (chọn nhiều), Công ty thuê kho "
     "(tự chọn hết theo kho), Từ ngày, Đến ngày, Loại báo cáo; 4 khung chọn Nhà > Dãy > Khoang > Vị trí "
     "(gồm Vị trí tự do của kho và Vị trí thuộc khoang).\n"
     "Bảng: STT, Ngày chứng từ, Số chứng từ (bấm mở chứng từ), Diễn giải, Số lượng Nhập / Xuất, Chi tiết "
     "(Lô, Vị trí, SL theo vị trí), SL tồn, NVKD (người yêu cầu - mã phòng ban).\n"
     "Nhập tồn đầu hiện số chứng từ \"NHAP_TON_DAU_<số>\", diễn giải \"Nhập tồn đầu\", không có đường dẫn."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Một chứng từ là 1 dòng, các lô / vị trí của chứng từ là các dòng con; Nhập hoặc Xuất của dòng = tổng "
     "các dòng con.\n"
     "- SL tồn của dòng = Tồn đầu kỳ + mọi biến động từ dòng đầu tới hết dòng đó (kể cả điều chuyển).\n"
     "- Tồn cuối kỳ = Tồn đầu kỳ + Nhập trong kỳ - Xuất trong kỳ.\n"
     "- Đổi Đơn vị tính thì mọi số chia cho hệ số của đơn vị đó, làm tròn 2 chữ số."),

    ("7. Phân quyền cấp",
     "- \"Thủ kho\": bắt buộc để mở màn và bấm Lọc; không có quyền thì ra trang không tìm thấy.\n"
     "- \"Xem báo cáo tồn kho theo tổng công ty\": ô Tồn theo công ty liệt kê mọi công ty; không có thì "
     "chỉ có công ty mình.\n"
     "- Ô Kho chỉ liệt kê kho được phân cho người dùng, thuộc công ty đang chọn.\n"
     "- In, Xuất Excel KHÔNG kiểm tra quyền Thủ kho.\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "Với dữ liệu mẫu H1, lọc 01/01 đến hôm nay, Tất cả, kho K1, ĐVT Cái:\n"
     "- Tồn đầu kỳ 0; Nhập trong kỳ 60 (24 + 36); Xuất trong kỳ 30; Tồn cuối kỳ 30.\n"
     "- SL tồn theo dòng: 24, 60, 30, 30.\n"
     "Lọc từ 01/04: Tồn đầu kỳ 60, Nhập 0, Xuất 30, Tồn cuối 30."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- Đổi Đơn vị tính sang Thùng: cột SL tồn từng dòng trên màn bị sai (cộng Tồn đầu kỳ tính theo Cái với "
     "biến động tính theo Thùng); bản In vẫn đúng.\n"
     "- Chọn Nhà / Dãy / Khoang không thu hẹp dữ liệu, chỉ chọn Vị trí mới có tác dụng.\n"
     "- Lọc theo vị trí có điều chuyển ra / vào: Tồn cuối kỳ khác SL tồn dòng cuối vì Tồn cuối không tính "
     "điều chuyển.\n"
     "- Bản In / Excel làm tròn số nguyên (2,5 Thùng in thành 3), cột Xuất in số âm, SL tồn âm in thành số "
     "dương.\n"
     "- Dòng chứng từ không có người yêu cầu có thể hiện NVKD \"null - null\".\n"
     "- Đến ngày trước Từ ngày không bị chặn, bảng trống."),
]


ROLE_TCS = [
    ("00", "Không có quyền Thủ kho thì không mở được màn", "P0",
     "NV-A không có quyền \"Thủ kho\"",
     "1. Đăng nhập NV-A\n"
     "2. " + MENU,
     "Tài khoản: NV-A",
     "- Ra trang không tìm thấy, không có bộ lọc Thẻ kho"),

    ("01", "Có quyền Thủ kho mở được màn", "P0",
     "TK-1 có quyền \"Thủ kho\", thuộc công ty TPE",
     "1. Đăng nhập TK-1\n"
     "2. " + MENU,
     "Tài khoản: TK-1",
     "- Tiêu đề \"Thẻ kho\"\n"
     "- Ô Tồn theo công ty chọn sẵn TPE, Từ ngày 01/01 năm nay, Đến ngày hôm nay\n"
     "- Bảng Chi tiết ghi \"Chưa có dữ liệu\""),

    ("02", "Quyền xem tồn kho theo tổng công ty thấy mọi công ty", "P0",
     "TK-2 có quyền Thủ kho và \"Xem báo cáo tồn kho theo tổng công ty\"",
     "1. Đăng nhập TK-2, mở màn từ menu\n"
     "2. Mở ô Tồn theo công ty",
     "—",
     "- Liệt kê mọi công ty, mặc định chọn công ty của TK-2"),

    ("03", "Không có quyền tổng công ty chỉ thấy công ty mình", "P0",
     "TK-1 chỉ có quyền Thủ kho, thuộc công ty TPE",
     "1. Mở ô Tồn theo công ty",
     "—",
     "- Chỉ có TPE"),

    ("04", "Ô Kho chỉ có kho được phân cho người dùng", "P0",
     "Công ty TPE có kho K1, K2, K3; TK-1 chỉ được phân K1, K2",
     "1. Mở ô Kho",
     "—",
     "- Chỉ có K1, K2"),

    ("05", "Không có quyền Thủ kho gọi thẳng chức năng Lọc", "P1",
     "NV-A không có quyền Thủ kho",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng lấy dữ liệu Thẻ kho của H1",
     "—",
     "- Trả về trang không tìm thấy, không có số liệu"),

    ("06", "Không có quyền Thủ kho vẫn In, Xuất Excel được qua đường dẫn", "P1",
     "NV-A không có quyền Thủ kho; TK-1 đã copy đường dẫn In Thẻ kho của H1",
     "1. Đăng nhập NV-A, dán đường dẫn In\n"
     "2. Dán đường dẫn Xuất Excel",
     "—",
     "- Theo code hiện tại: mở được bản In và tải được file, thấy đủ số liệu\n"
     "- Lưu ý: điểm hở phân quyền - ghi Failed nếu nghiệp vụ yêu cầu chặn"),
]
