# -*- coding: utf-8 -*-
"""Noi dung TC man ERP: Bao cao tong hop cong no khach hang theo nhan vien
(saleReports.customerDebtDetailByEmployee)."""
from common import COT_SO_LIEU, DU_LIEU_MAU, data_change_tcs, MENU_YCXH

Q = "Xem báo cáo tổng hợp công nợ khách hàng theo nhân viên - "

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Báo cáo công nợ phải thu gom theo NHÂN VIÊN LẬP HỢP ĐỒNG: mỗi nhân viên đang có những hợp đồng nào "
     "còn nợ, nợ bao nhiêu, nghiệm thu ngày nào, đã nợ bao nhiêu ngày. Dùng để giao nhân viên đi đòi nợ. "
     "Màn chỉ để xem.\n"
     "Đường vào: menu Kinh doanh > Báo cáo công nợ > 'Báo cáo tổng hợp công nợ khách hàng theo nhân "
     "viên'."),

    ("2. Đối tượng được tính / hiển thị",
     COT_SO_LIEU + "\n"
     "Số liệu 8 cột của một hợp đồng phải BẰNG số của cùng hợp đồng đó trên màn 'Báo cáo chi tiết công nợ KH'."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Bút toán chưa gắn khách hàng hoặc số tiền bằng 0.\n"
     "- Hợp đồng ngoài phạm vi quyền xem (mục 7).\n"
     "- Cột 'Số ngày nợ' để trống khi hợp đồng không còn dư nợ (Số dư cuối kì nhỏ hơn hoặc bằng 0) hoặc "
     "không xác định được ngày nghiệm thu."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Từ ngày và Đến ngày BẮT BUỘC, lọc theo NGÀY HẠCH TOÁN (trước Từ ngày vào Số dư đầu kỳ).\n"
     "Ô 'Ngày nghiệm thu' (không bắt buộc) lọc các hợp đồng có ngày nghiệm thu ĐÚNG BẰNG ngày chọn.\n"
     "Màn không tự tải: phải bấm 'Lọc'."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Bảng 2 cấp, 16 cột: STT · Đơn hàng/hợp đồng · Khách hàng · Số dư đầu kỳ · [Phát sinh tăng: Hàng "
     "hóa/Dịch vụ · Điều chỉnh công nợ · Cộng] · [Phát sinh giảm: Nhập trả lại · Đã thanh toán · Điều "
     "chỉnh công nợ · Cộng] · Trả lại tiền thừa · Số dư cuối kì · Ngày nghiệm thu · Số ngày nợ (Ngày).\n"
     "- Dòng nhân viên (chữ đậm): 'Mã - Họ tên' người lập hợp đồng, cộng các hợp đồng bên dưới.\n"
     "- Dòng hợp đồng: link hợp đồng, cột Khách hàng 'Mã - Tên'.\n"
     "- 3 cột đầu dính bên trái khi cuộn ngang. Dòng Tổng cộng nằm dưới tiêu đề.\n"
     "Phân trang 15 dòng HỢP ĐỒNG mỗi trang; nhân viên xếp theo thứ tự tạo tài khoản, không theo tên."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Gom theo (nhân viên lập, hợp đồng): một hợp đồng một dòng.\n"
     "- Hợp đồng có bút toán của nhiều khách: cột Khách hàng chỉ hiện MỘT khách bất kỳ (ghi nhận).\n"
     "- Dòng nhân viên chỉ cộng các hợp đồng trên TRANG ĐANG XEM (ghi nhận, giống màn Chi tiết).\n"
     "- Dòng Tổng cộng tính mọi trang + Số dư đầu kỳ chung."),

    ("7. Phân quyền cấp",
     "Mọi tài khoản mở được màn. Phạm vi:\n"
     "- '" + Q + "tổng công ty': mọi công ty; có ô Công ty, Phòng ban, Bộ phận, Nhân viên.\n"
     "- '" + Q + "công ty': công ty mình + hợp đồng mình lập.\n"
     "- '" + Q + "phòng ban': phòng mình đang ngồi + phòng được phân quản lý + hợp đồng mình lập; chỉ có ô "
     "Bộ phận, Nhân viên.\n"
     "- '" + Q + "bộ phận': bộ phận mình đang ngồi + bộ phận quản lý + hợp đồng mình lập.\n"
     "- Không quyền: chỉ hợp đồng mình lập; không có ô Công ty / Phòng ban / Bộ phận / Nhân viên."),

    ("8. Cách tính các ô thống kê",
     "- Cộng, Số dư cuối kì: như màn Chi tiết (Cuối kỳ = Đầu kỳ + Cộng tăng - Cộng giảm + Trả lại tiền thừa).\n"
     "- Ngày nghiệm thu của hợp đồng hãng CẦN LẮP ĐẶT: ngày của biên bản nghiệm thu bàn giao gần nhất.\n"
     "- Hợp đồng hãng không cần lắp đặt: ngày muộn nhất trong các phiếu xuất kho bán theo hợp đồng hãng "
     "(ngày duyệt), phiếu xuất bán hàng mượn, phiếu hạch toán dịch vụ.\n"
     "- Hợp đồng dịch vụ BH-SC: ngày muộn nhất trong hạch toán dịch vụ BH-SC, xuất bán hàng mượn, phiếu "
     "xuất kho.\n"
     "- Không có các phiếu trên: lấy ngày nghiệm thu bàn giao khai trong công nợ đầu kỳ quá hạn.\n"
     "- Số ngày nợ = Hôm nay - (Ngày nghiệm thu + 6 ngày); nhỏ hơn 0 thì hiện 0; chỉ hiện khi còn dư nợ.\n"
     "- 2 nút xuất ('Xuất excel', 'Xuất excel mẫu in') đều GỬI FILE QUA EMAIL, không tải ngay."),

    ("9. Ghi chú đọc bảng",
     DU_LIEU_MAU + "\n"
     "Các lỗi ERP ĐÃ BIẾT (thấy đúng hiện tượng thì ghi Failed, chép câu 'Lỗi ERP đã biết' vào Ghi chú):\n"
     "(1) 'Số dư đầu kỳ' của dòng Tổng cộng luôn là số của TOÀN HỆ THỐNG với mọi người xem, không theo phạm "
     "vi quyền.\n"
     "(2) Người không có quyền xem vẫn xem được hợp đồng của nhân viên khác nếu tự sửa đường dẫn xuất excel "
     "thêm nhân viên khác (dành cho tester kỹ thuật).\n"
     "(3) Không lọc gì với kỳ dài: tải rất chậm (có thể 20 giây trở lên).\n"
     "Ghi nhận: Số ngày nợ có thể lệch 1 ngày giữa 2 lần xem nếu xem quanh mốc giờ nghiệm thu."),
]

ROLE_TCS = [
    ("00", "Không có quyền nào: chỉ thấy hợp đồng mình lập", "P0",
     "Tài khoản A không có 4 quyền xem, lập 3 hợp đồng còn nợ",
     "1. Đăng nhập A, mở màn, quan sát bộ lọc\n2. Lọc tháng này", "Tài khoản: A",
     "- Không có ô Công ty, Phòng ban, Bộ phận, Nhân viên\n- Chỉ có dòng nhân viên A với hợp đồng của A\n"
     "- Lỗi ERP đã biết: 'Số dư đầu kỳ' dòng Tổng cộng là số của toàn hệ thống"),
    ("01", "Quyền theo bộ phận gồm cả bộ phận mình đang ngồi", "P0",
     "Tài khoản B có quyền '" + Q + "bộ phận', ngồi ở BP1, được phân quản lý BP2",
     "1. Đăng nhập B, lọc tháng này", "Tài khoản: B",
     "- Có nhân viên của cả BP1 và BP2\n- Không có bộ phận khác"),
    ("02", "Quyền theo phòng ban gồm cả phòng mình đang ngồi", "P0",
     "Tài khoản C có quyền '" + Q + "phòng ban', ngồi ở P1, được phân quản lý P2",
     "1. Đăng nhập C, quan sát bộ lọc\n2. Lọc tháng này", "Tài khoản: C",
     "- Chỉ có ô Bộ phận, Nhân viên\n- Có nhân viên của P1 và P2"),
    ("03", "Quyền theo công ty", "P0", "Tài khoản D có quyền '" + Q + "công ty' (công ty 1)",
     "1. Đăng nhập D, lọc tháng này", "Tài khoản: D",
     "- Mọi nhân viên công ty 1, không có công ty khác\n- Có ô Phòng ban, Bộ phận, Nhân viên"),
    ("04", "Quyền theo tổng công ty", "P0", "Tài khoản E có quyền '" + Q + "tổng công ty'",
     "1. Đăng nhập E, lọc tháng này", "Tài khoản: E",
     "- Có đủ 4 ô lọc tổ chức\n- Nhân viên của mọi công ty"),
    ("05", "Không quyền nhưng sửa đường dẫn để xem nhân viên khác", "P1",
     "Tài khoản A (không quyền). Dành cho tester kỹ thuật. Biết mã tài khoản của nhân viên B",
     "1. Bấm 'Xuất excel', sao chép đường dẫn\n2. Thêm tham số nhân viên = mã của B, mở đường dẫn\n"
     "3. Kiểm tra email nhận được", "Tài khoản: A",
     "- File chỉ có hợp đồng của A (hoặc trống)\n"
     "- Lỗi ERP đã biết: file có hợp đồng của B"),
]

SECTIONS = [
    ("I", "Giao diện & mở màn", [
        ("001", "Bố cục màn hình", "P0", "Tài khoản quyền tổng công ty",
         "1. Menu Kinh doanh > Báo cáo công nợ > 'Báo cáo tổng hợp công nợ khách hàng theo nhân viên'", "",
         "- Tiêu đề 'Báo cáo tổng hợp công nợ khách hàng theo nhân viên'\n"
         "- Ô lọc: Từ ngày* · Đến ngày* · Khách hàng · Số hợp đồng · Số dư cuối kỳ · Ngày nghiệm thu · "
         "Công ty · Phòng ban · Bộ phận · Nhân viên\n"
         "- Nút: 'Lọc' · làm mới · 'Xuất excel' · 'Xuất excel mẫu in'"),
        ("002", "Không tự tải khi mở", "P0", "Vừa mở màn", "1. Quan sát bảng", "",
         "- 'Chưa có dữ liệu'"),
        ("003", "Tiêu đề cột", "P0", "", "1. Đọc tiêu đề", "",
         "- Đủ 16 cột theo thứ tự ở mục 5, có 2 cột cuối 'Ngày nghiệm thu', 'Số ngày nợ (Ngày)'"),
        ("004", "3 cột đầu dính khi cuộn ngang", "P2", "Có dữ liệu",
         "1. Cuộn ngang bảng sang phải", "",
         "- STT, Đơn hàng/hợp đồng, Khách hàng vẫn đứng yên bên trái"),
    ]),

    ("II", "Bộ lọc", [
        ("001", "Thiếu ngày bắt buộc", "P0", "", "1. Để trống Từ ngày, bấm 'Lọc'", "",
         "- Thông báo 'Chưa chọn đủ điều kiện bắt buộc', ô trống hiện 'Bắt buộc chọn'"),
        ("002", "Lọc theo kỳ", "P0", "", "1. Nhập kỳ tháng 09/2026, lọc", "",
         "- Có dòng nhân viên, hợp đồng; dòng Tổng cộng có số"),
        ("003", "Lọc Khách hàng", "P1", "KH-TEST có hợp đồng của 2 nhân viên",
         "1. Chọn KH-TEST, lọc", "", "- Hiện 2 nhân viên, mỗi người các hợp đồng của KH-TEST"),
        ("004", "Lọc Số hợp đồng", "P1", "", "1. Nhập đủ mã HD-TEST-01, lọc", "",
         "- Chỉ một dòng hợp đồng HD-TEST-01 dưới nhân viên A"),
        ("005", "Lọc Dư nợ / Dư có", "P0", "", "1. Chọn 'Dư nợ', lọc\n2. Chọn 'Dư có', lọc", "",
         "- Bước 1: mọi hợp đồng có Số dư cuối kì lớn hơn 0\n- Bước 2: mọi hợp đồng có số âm"),
        ("006", "Lọc Ngày nghiệm thu", "P1", "HD-TEST-01 có ngày nghiệm thu 15/09/2026",
         "1. Ô 'Ngày nghiệm thu' chọn 15/09/2026, lọc\n2. Chọn 16/09/2026, lọc", "",
         "- Bước 1: có HD-TEST-01, mọi dòng có Ngày nghiệm thu 15/09/2026\n"
         "- Bước 2: không có HD-TEST-01 (lọc đúng bằng ngày)"),
        ("007", "Lọc Nhân viên", "P0", "", "1. Chọn nhân viên A, lọc", "",
         "- Chỉ dòng nhân viên A"),
        ("008", "Lọc Công ty / Phòng ban / Bộ phận", "P1", "Tài khoản quyền tổng công ty",
         "1. Chọn Công ty 1, Phòng P1, Bộ phận BP1, lọc", "",
         "- Ô dưới thu hẹp theo ô trên\n- Chỉ nhân viên thuộc BP1"),
        ("009", "Kết hợp bộ lọc", "P1", "", "1. Kỳ + Nhân viên A + Dư nợ, lọc", "",
         "- Chỉ hợp đồng còn nợ của A"),
    ]),

    ("III", "Bảng số liệu & phân trang", [
        ("001", "Dòng nhân viên và hợp đồng", "P0", "Lọc có dữ liệu", "1. Quan sát", "",
         "- Dòng nhân viên chữ đậm 'Mã - Họ tên'\n- Dòng hợp đồng: link hợp đồng, Khách hàng 'Mã - Tên'\n"
         "- Dòng nhân viên = cộng các hợp đồng bên dưới trên cùng trang"),
        ("002", "Số liệu khớp màn Chi tiết", "P0", "Chọn HD-TEST-01",
         "1. Lọc cùng kỳ ở màn này và màn 'Báo cáo chi tiết công nợ KH'\n2. So 8 cột", "",
         "- 8 cột số và Số dư cuối kì của HD-TEST-01 bằng nhau ở 2 màn"),
        ("003", "Phân trang 15 hợp đồng", "P0", "Trên 15 hợp đồng", "1. Đếm, chuyển trang", "",
         "- 15 dòng hợp đồng / trang\n- Tổng cộng không đổi khi chuyển trang"),
        ("004", "Thứ tự nhân viên", "P2", "", "1. Quan sát thứ tự các dòng nhân viên", "",
         "- Ghi nhận: xếp theo thứ tự tạo tài khoản, không theo bảng chữ cái"),
        ("005", "Hợp đồng nhiều khách hàng", "P2", "Một hợp đồng có bút toán của 2 khách",
         "1. Lọc theo hợp đồng đó", "",
         "- Ghi nhận: một dòng duy nhất, cột Khách hàng hiện 1 trong 2 khách"),
        ("006", "Tốc độ tải", "P2", "Tài khoản quyền tổng công ty, kỳ 6 tháng, không lọc khác",
         "1. Bấm 'Lọc', bấm giờ", "",
         "- Hiện xong trong khoảng 10 giây\n- Lỗi ERP đã biết: có thể mất 20 giây trở lên"),
    ]),

    ("IV", "Ngày nghiệm thu & Số ngày nợ", [
        ("001", "Hợp đồng hãng cần lắp đặt lấy ngày biên bản nghiệm thu", "P0",
         "Hợp đồng hãng HD-LD (cần lắp đặt) đã xuất hàng; lập biên bản nghiệm thu bàn giao ngày 10/09/2026",
         "1. Lọc theo HD-LD", "",
         "- Ngày nghiệm thu = 10/09/2026 (theo biên bản, không theo ngày xuất kho)"),
        ("002", "Hợp đồng hãng không lắp đặt lấy ngày xuất kho muộn nhất", "P0",
         "Hợp đồng hãng HD-KLD (không lắp đặt) có 2 phiếu xuất kho bán theo hợp đồng duyệt ngày 05/09 và "
         "20/09/2026",
         "1. Lọc theo HD-KLD", "",
         "- Ngày nghiệm thu = 20/09/2026"),
        ("003", "Xuất kho thêm làm đổi Ngày nghiệm thu", "P1", "Tiếp TC trước",
         "1. Vào " + MENU_YCXH + ", xuất thêm hàng cho HD-KLD, phiếu xuất duyệt hôm nay\n2. Lọc lại", "",
         "- Ngày nghiệm thu đổi thành hôm nay\n- Số ngày nợ về 0"),
        ("004", "Công thức Số ngày nợ", "P0",
         "Hợp đồng còn dư nợ, Ngày nghiệm thu cách hôm nay 30 ngày",
         "1. Đọc cột 'Số ngày nợ (Ngày)'", "",
         "- Số ngày nợ bằng 24 (30 ngày trừ 6 ngày)"),
        ("005", "Nghiệm thu chưa quá 6 ngày", "P1", "Ngày nghiệm thu là 3 ngày trước, còn dư nợ",
         "1. Đọc Số ngày nợ", "", "- Hiện 0 (không hiện số âm)"),
        ("006", "Hết nợ thì không hiện Số ngày nợ", "P0",
         "HD-KLD còn dư nợ 5,000,000, Số ngày nợ đang có số",
         "1. Lập phiếu thu 5,000,000 cho HD-KLD, hạch toán hôm nay\n2. Lọc lại", "",
         "- Số dư cuối kì = 0, cột Số ngày nợ trống\n- Ngày nghiệm thu vẫn hiện"),
        ("007", "Hợp đồng chưa có phiếu nào để xác định ngày", "P2",
         "Hợp đồng có công nợ nhưng chưa xuất kho, chưa nghiệm thu, không có khai báo đầu kỳ quá hạn",
         "1. Lọc theo hợp đồng đó", "", "- Ngày nghiệm thu và Số ngày nợ để trống"),
        ("008", "Lấy ngày khai trong công nợ đầu kỳ quá hạn", "P2",
         "Hợp đồng cũ chỉ có khai báo đầu kỳ công nợ, đánh dấu quá hạn, ngày nghiệm thu bàn giao 01/03/2026",
         "1. Lọc theo hợp đồng đó", "", "- Ngày nghiệm thu = 01/03/2026"),
    ]),

    ("V", "Làm mới & Xuất excel", [
        ("001", "Nút làm mới", "P1", "Đã lọc", "1. Bấm làm mới", "",
         "- Mọi ô lọc về trống, bảng xóa các dòng"),
        ("002", "Xuất excel gửi email", "P0", "Đã nhập kỳ",
         "1. Bấm 'Xuất excel'\n2. Kiểm tra email", "",
         "- Thông báo 'Báo cáo tổng hợp công nợ khách hàng theo nhân viên sẽ gửi về mail của bạn trong ít "
         "phút!'\n- Nhận email kèm file, số liệu khớp màn hình, đủ mọi trang"),
        ("003", "Xuất excel mẫu in", "P0", "Đã nhập kỳ",
         "1. Bấm 'Xuất excel mẫu in'\n2. Mở file nhận qua email", "",
         "- File theo mẫu in: Giá trị hợp đồng thực tế, Giá trị đã thanh toán, Còn nợ cuối kỳ, Ngày nghiệm "
         "thu, Số ngày nợ và các cột trống để nhân viên ghi giải trình / kế hoạch thu / xác nhận công nợ"),
        ("004", "Excel theo phạm vi quyền", "P1", "Tài khoản B (quyền bộ phận)",
         "1. Xuất excel", "", "- File chỉ có nhân viên của BP1, BP2"),
    ]),

    ("VI", "Tạo phiếu - số liệu thay đổi (luồng end-to-end)", data_change_tcs("employee") + [
        ("018", "Hợp đồng mới của nhân viên xuất hiện dưới đúng nhân viên", "P1",
         "Nhân viên A chưa có hợp đồng HD-TEST-02",
         "1. A lập hợp đồng HD-TEST-02 cho KH-TEST, xuất kho 6,000,000, hạch toán hôm nay\n2. Lọc lại", "",
         "- HD-TEST-02 hiện dưới dòng nhân viên A, Hàng hóa/Dịch vụ 6,000,000\n"
         "- Dòng nhân viên A tăng 6,000,000 ở Số dư cuối kì"),
    ]),
]
