# -*- coding: utf-8 -*-
"""Noi dung TC man ERP: Bao cao chi tiet cong no KH (saleReports.customerDebtDetails)."""
from common import COT_SO_LIEU, DU_LIEU_MAU, data_change_tcs

Q = "Xem báo cáo chi tiết công nợ khách hàng theo "

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Báo cáo công nợ phải thu của từng KHÁCH HÀNG, tách theo từng HỢP ĐỒNG / ĐƠN HÀNG trong một khoảng "
     "thời gian: đầu kỳ còn nợ bao nhiêu, trong kỳ phát sinh tăng / giảm bao nhiêu, cuối kỳ còn nợ bao "
     "nhiêu. Màn chỉ để xem.\n"
     "Đường vào: menu Kinh doanh > Báo cáo công nợ > 'Báo cáo chi tiết công nợ KH'. Tiêu đề trang: "
     "'Báo cáo chi tiết công nợ khách hàng'."),

    ("2. Đối tượng được tính / hiển thị",
     COT_SO_LIEU + "\n"
     "Các dòng hợp đồng chỉ lấy bút toán CÓ gắn khách hàng và số tiền lớn hơn 0."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Bút toán chưa gắn khách hàng: không có dòng hợp đồng nào, nhưng VẪN được tính vào 'Số dư đầu kỳ' "
     "của dòng Tổng cộng.\n"
     "- Bút toán gắn khách nhưng không gắn hợp đồng: hiện thành dòng có dấu '-' ở cột Đơn hàng/hợp đồng "
     "(rê chuột hiện 'Phiếu báo có hoặc kế toán chưa được ghi nhận').\n"
     "- Hợp đồng nằm ngoài phạm vi quyền xem (mục 7)."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Từ ngày và Đến ngày BẮT BUỘC, mặc định để trống. Lọc theo NGÀY HẠCH TOÁN của phiếu, lấy trọn ngày "
     "cuối.\n"
     "- Trước Từ ngày: cộng vào Số dư đầu kỳ.\n- Từ ngày đến Đến ngày: vào các cột phát sinh.\n"
     "- Sau Đến ngày: không tính.\n"
     "Đến ngày nhỏ hơn Từ ngày: báo 'Đến ngày phải lớn hơn hoặc bằng Từ ngày'.\n"
     "Màn không tự tải: phải bấm 'Lọc'."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Bảng 2 cấp, 15 cột: STT · Đơn hàng/hợp đồng · Phòng ban · Bộ phận · NVKD · Số dư đầu kỳ · "
     "[Phát sinh tăng: Hàng hóa/Dịch vụ · Điều chỉnh công nợ · Cộng] · [Phát sinh giảm: Nhập trả lại · Đã "
     "thanh toán · Điều chỉnh công nợ · Cộng] · Trả lại tiền thừa · Số dư cuối kì.\n"
     "- Dòng khách hàng (chữ đậm, STT 1, 2...): 'Mã KH - Tên KH', cộng các hợp đồng bên dưới.\n"
     "- Dòng hợp đồng (STT 1.1, 1.2...): link mở hợp đồng, Phòng ban / Bộ phận / NVKD của NGƯỜI LẬP hợp "
     "đồng theo hồ sơ HIỆN TẠI.\n"
     "- Dòng Tổng cộng nằm ngay dưới tiêu đề.\n"
     "Phân trang 15 dòng HỢP ĐỒNG mỗi trang, khách hàng xếp theo thứ tự tạo trong danh mục."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Một hợp đồng một dòng (gom theo khách hàng + hợp đồng).\n"
     "- Dòng khách hàng chỉ cộng các hợp đồng NẰM TRÊN TRANG ĐANG XEM: khách có hợp đồng vắt qua 2 trang "
     "thì mỗi trang hiện một tổng riêng - đây là cách ERP đang làm, không ghi Failed.\n"
     "- Dòng Tổng cộng tính trên TOÀN BỘ dữ liệu sau lọc (mọi trang), cộng thêm Số dư đầu kỳ chung.\n"
     "- Các ô số tiền (trừ 2 cột Cộng, Số dư đầu kỳ, Số dư cuối kì) bấm được, mở cửa sổ danh sách phiếu "
     "tạo ra con số đó."),

    ("7. Phân quyền cấp",
     "Mọi tài khoản đều mở được màn. Phạm vi theo quyền:\n"
     "- '" + Q + "tổng công ty': mọi công ty; có ô lọc Công ty, Phòng ban, Bộ phận, Nhân viên.\n"
     "- '" + Q + "công ty': công ty mình + hợp đồng mình lập; có ô Phòng ban, Bộ phận, Nhân viên.\n"
     "- '" + Q + "phòng ban': các phòng mình được phân quản lý + hợp đồng mình lập; chỉ có ô Bộ phận, "
     "Nhân viên.\n"
     "- '" + Q + "bộ phận': các bộ phận mình quản lý + hợp đồng mình lập; có ô Phòng ban, Bộ phận, Nhân viên.\n"
     "- Không quyền nào: chỉ hợp đồng mình lập; không có ô Công ty / Phòng ban / Bộ phận / Nhân viên."),

    ("8. Cách tính các ô thống kê",
     "- Cộng (tăng) = Hàng hóa/Dịch vụ + Điều chỉnh công nợ tăng.\n"
     "- Cộng (giảm) = Nhập trả lại + Đã thanh toán + Điều chỉnh công nợ giảm.\n"
     "- Số dư cuối kì = Số dư đầu kỳ + Cộng tăng - Cộng giảm + Trả lại tiền thừa.\n"
     "- Ô 'Số dư cuối kỳ' (bộ lọc): Tất cả / Dư nợ (cuối kỳ lớn hơn 0) / Dư có (nhỏ hơn 0); áp cho dòng "
     "hợp đồng, KHÔNG áp cho dòng Tổng cộng.\n"
     "- Số hiển thị có dấu phẩy phân cách hàng nghìn; ô bằng 0 hiện dấu '-'.\n"
     "- 'Xuất excel' KHÔNG tải file ngay: hệ thống gửi file qua email của người bấm."),

    ("9. Ghi chú đọc bảng",
     DU_LIEU_MAU + "\n"
     "Các lỗi ERP ĐÃ BIẾT (kết quả mong đợi viết theo cách ĐÚNG; thấy đúng hiện tượng lỗi thì ghi Failed, "
     "chép câu 'Lỗi ERP đã biết' vào cột Ghi chú):\n"
     "(1) Người có quyền theo bộ phận hoặc không có quyền nào: 'Số dư đầu kỳ' của dòng Tổng cộng là số dư "
     "của TOÀN HỆ THỐNG (hàng trăm tỷ), không phải của phạm vi mình được xem.\n"
     "(2) Khách hàng không còn trong danh mục: các hợp đồng của khách đó bị dồn nhầm vào khách hàng đứng "
     "kế tiếp.\n"
     "(3) Hợp đồng lập bên hệ thống HRM hiện dấu '-' thay vì mã hợp đồng.\n"
     "Các điểm GHI NHẬN (đúng hiện trạng, không ghi Failed): ô bằng 0 vẫn bấm được và có thể vẫn ra phiếu; "
     "cửa sổ chi tiết luôn có tiêu đề 'Chi tiết số tiền đã thanh toán' dù bấm ở cột nào; dòng Tổng cộng có "
     "thể khác tổng các dòng khách hàng vì có bút toán chưa gắn khách."),
]

ROLE_TCS = [
    ("00", "Không có quyền nào: chỉ thấy hợp đồng mình lập", "P0",
     "Tài khoản A (nhân viên kinh doanh) không có quyền nào trong 4 quyền xem. A lập 3 hợp đồng có phát "
     "sinh trong tháng",
     "1. Đăng nhập A, mở màn\n2. Quan sát bộ lọc\n3. Nhập kỳ tháng này, bấm 'Lọc'",
     "Tài khoản: A",
     "- Không có ô Công ty, Phòng ban, Bộ phận, Nhân viên\n"
     "- Bảng chỉ có hợp đồng do A lập\n"
     "- 'Số dư đầu kỳ' dòng Tổng cộng chỉ là của các hợp đồng của A\n"
     "- Lỗi ERP đã biết: 'Số dư đầu kỳ' dòng Tổng cộng là số của toàn hệ thống"),

    ("01", "Quyền theo bộ phận", "P0",
     "Tài khoản B có quyền '" + Q + "bộ phận', được phân quản lý bộ phận BP1",
     "1. Đăng nhập B, mở màn, quan sát bộ lọc\n2. Lọc tháng này",
     "Tài khoản: B",
     "- Có ô Phòng ban, Bộ phận, Nhân viên\n"
     "- Bảng có hợp đồng của BP1 và hợp đồng B lập, không có bộ phận khác\n"
     "- Lỗi ERP đã biết: 'Số dư đầu kỳ' dòng Tổng cộng là số của toàn hệ thống"),

    ("02", "Quyền theo phòng ban", "P0",
     "Tài khoản C có quyền '" + Q + "phòng ban', được phân quản lý phòng P1 (trong công ty mình)",
     "1. Đăng nhập C, mở màn, quan sát bộ lọc\n2. Lọc tháng này",
     "Tài khoản: C",
     "- Chỉ có ô Bộ phận, Nhân viên (không có ô Phòng ban)\n"
     "- Bảng có hợp đồng thuộc phòng P1 và hợp đồng C lập\n- Không có phòng khác"),

    ("03", "Quyền theo công ty", "P0",
     "Tài khoản D có quyền '" + Q + "công ty', thuộc công ty 1",
     "1. Đăng nhập D, mở màn\n2. Lọc tháng này",
     "Tài khoản: D",
     "- Có ô Phòng ban, Bộ phận, Nhân viên; không có ô Công ty\n"
     "- Bảng có mọi hợp đồng của công ty 1, không có công ty khác"),

    ("04", "Quyền theo tổng công ty", "P0",
     "Tài khoản E có quyền '" + Q + "tổng công ty'",
     "1. Đăng nhập E, mở màn\n2. Lọc tháng này",
     "Tài khoản: E",
     "- Có đủ 4 ô Công ty, Phòng ban, Bộ phận, Nhân viên\n- Bảng có hợp đồng của mọi công ty"),

    ("05", "Phạm vi quyền áp cho cửa sổ chi tiết phiếu", "P1",
     "Tài khoản A (không quyền)",
     "1. Lọc, bấm ô 'Đã thanh toán' của một hợp đồng của A",
     "Tài khoản: A",
     "- Cửa sổ chỉ liệt kê phiếu của hợp đồng đó"),
]

SECTIONS = [
    ("I", "Giao diện & mở màn", [
        ("001", "Bố cục màn hình", "P0", "Tài khoản quyền tổng công ty",
         "1. Menu Kinh doanh > Báo cáo công nợ > 'Báo cáo chi tiết công nợ KH'\n2. Quan sát",
         "",
         "- Tiêu đề 'Báo cáo chi tiết công nợ khách hàng'\n"
         "- Ô lọc: Từ ngày* · Đến ngày* · Khách hàng · Số hợp đồng · Số dư cuối kỳ · Công ty · Phòng ban · "
         "Bộ phận · Nhân viên\n"
         "- Nút 'Lọc', nút làm mới (mũi tên xoay vòng), nút 'Xuất excel'"),
        ("002", "Màn không tự tải khi mở", "P0", "Vừa mở màn",
         "1. Quan sát bảng", "",
         "- Bảng 'Chưa có dữ liệu', dòng Tổng cộng trống\n- Từ ngày, Đến ngày trống"),
        ("003", "Tiêu đề cột 2 tầng", "P0", "Đã mở màn",
         "1. Đọc tiêu đề bảng", "",
         "- Tầng 1: STT · Đơn hàng/hợp đồng · Phòng ban · Bộ phận · NVKD · Số dư đầu kỳ · Phát sinh tăng "
         "trong kì · Phát sinh giảm trong kì · Trả lại tiền thừa · Số dư cuối kì\n"
         "- Tầng 2 dưới Phát sinh tăng: Hàng hóa/Dịch vụ · Điều chỉnh công nợ · Cộng\n"
         "- Tầng 2 dưới Phát sinh giảm: Nhập trả lại · Đã thanh toán · Điều chỉnh công nợ · Cộng"),
        ("004", "Lựa chọn ô Số dư cuối kỳ", "P2", "Đã mở màn",
         "1. Mở ô 'Số dư cuối kỳ'", "",
         "- 3 lựa chọn: Tất cả · Dư nợ · Dư có; mặc định 'Tất cả'"),
        ("005", "Ô Khách hàng tìm theo tên / mã", "P1", "Đã mở màn",
         "1. Gõ vài ký tự tên hoặc mã khách vào ô Khách hàng", "",
         "- Danh sách gợi ý khách khớp, chọn được nhiều khách"),
    ]),

    ("II", "Bộ lọc", [
        ("001", "Bấm Lọc khi thiếu ngày", "P0", "Từ ngày trống",
         "1. Bấm 'Lọc'", "",
         "- Thông báo 'Chưa chọn đủ điều kiện bắt buộc'\n- Dưới ô Từ ngày hiện 'Bắt buộc chọn'"),
        ("002", "Đến ngày nhỏ hơn Từ ngày", "P0", "Đã mở màn",
         "1. Từ ngày 30/09/2026, Đến ngày 01/09/2026\n2. Bấm 'Lọc'", "",
         "- Thông báo và chữ đỏ dưới ô Đến ngày: 'Đến ngày phải lớn hơn hoặc bằng Từ ngày'\n- Không tải dữ liệu"),
        ("003", "Lọc theo khoảng ngày", "P0", "Có dữ liệu tháng 09/2026",
         "1. Từ ngày 01/09/2026, Đến ngày 30/09/2026, bấm 'Lọc'", "",
         "- Bảng có dữ liệu, dòng Tổng cộng có số\n- Phát sinh chỉ gồm phiếu hạch toán trong tháng 9"),
        ("004", "Lọc theo 1 khách hàng", "P0", "KH-TEST có 2 hợp đồng",
         "1. Chọn Khách hàng KH-TEST, lọc", "",
         "- Chỉ một dòng khách KH-TEST với 2 hợp đồng bên dưới\n- Tổng cộng chỉ tính của KH-TEST"),
        ("005", "Lọc nhiều khách hàng", "P1", "",
         "1. Chọn 2 khách hàng, lọc", "",
         "- Hiện đúng 2 khách hàng"),
        ("006", "Lọc Số hợp đồng phải gõ đủ mã", "P1", "Hợp đồng mã HD-TEST-01",
         "1. Ô Số hợp đồng nhập 'HD-TEST-01', lọc\n2. Nhập 'HD-TEST', lọc", "",
         "- Bước 1: chỉ hợp đồng HD-TEST-01\n"
         "- Bước 2: ghi nhận: 'Chưa có dữ liệu' vì ô này so khớp đủ mã, không tìm theo một phần"),
        ("007", "Lọc Dư nợ", "P0", "Có hợp đồng dư nợ và hợp đồng dư có",
         "1. 'Số dư cuối kỳ' chọn 'Dư nợ', lọc", "",
         "- Mọi dòng hợp đồng có 'Số dư cuối kì' lớn hơn 0\n"
         "- Ghi nhận: dòng Tổng cộng không đổi so với khi chọn 'Tất cả'"),
        ("008", "Lọc Dư có", "P0", "",
         "1. 'Số dư cuối kỳ' chọn 'Dư có', lọc", "",
         "- Mọi dòng hợp đồng có 'Số dư cuối kì' nhỏ hơn 0 (số âm)"),
        ("009", "Lọc Công ty", "P1", "Tài khoản quyền tổng công ty",
         "1. Chọn Công ty 1\n2. Mở ô Phòng ban, Nhân viên\n3. Lọc", "",
         "- Ô Phòng ban, Nhân viên chỉ còn của công ty 1\n- Bảng chỉ hợp đồng công ty 1"),
        ("010", "Lọc Phòng ban, Bộ phận", "P1", "Tài khoản quyền công ty",
         "1. Chọn phòng P1, mở ô Bộ phận\n2. Chọn BP1, lọc", "",
         "- Ô Bộ phận chỉ còn bộ phận của P1\n- Bảng chỉ hợp đồng thuộc BP1"),
        ("011", "Lọc Nhân viên", "P0", "Nhân viên A lập 3 hợp đồng",
         "1. Chọn Nhân viên A, lọc", "",
         "- Chỉ các hợp đồng do A lập, cột NVKD = A"),
        ("012", "Phòng ban hiển thị theo hồ sơ hiện tại người lập", "P2",
         "Nhân viên A lập hợp đồng khi ở P1, nay đã chuyển sang P2",
         "1. Lọc theo hợp đồng của A", "",
         "- Ghi nhận hiện tượng: cột Phòng ban hiện P2 (phòng hiện tại), không phải phòng lúc lập hợp đồng"),
        ("013", "Kết hợp nhiều bộ lọc", "P1", "",
         "1. Nhập kỳ, chọn Khách hàng, Nhân viên, Dư nợ, lọc", "",
         "- Chỉ dòng thỏa đồng thời mọi điều kiện"),
    ]),

    ("III", "Bảng số liệu & phân trang", [
        ("001", "Dòng khách hàng và dòng hợp đồng", "P0", "Lọc tháng có dữ liệu",
         "1. Quan sát bảng", "",
         "- Dòng khách chữ đậm, STT 1; cột Đơn hàng/hợp đồng hiện 'Mã KH - Tên KH'\n"
         "- Dòng hợp đồng STT 1.1, 1.2; mã hợp đồng là link\n"
         "- Dòng khách = cộng các dòng hợp đồng bên dưới (trên cùng trang)"),
        ("002", "Link hợp đồng mở tab mới", "P1", "",
         "1. Bấm mã hợp đồng", "",
         "- Mở chi tiết hợp đồng đúng loại (hợp đồng hãng, hợp đồng dịch vụ...) ở tab mới"),
        ("003", "Công thức Cộng và Số dư cuối kì", "P0", "Chọn một hợp đồng có đủ các cột",
         "1. Tự tính lại theo công thức mục 8", "",
         "- 2 cột Cộng và Số dư cuối kì đúng công thức trên cả dòng hợp đồng, dòng khách, dòng Tổng cộng"),
        ("004", "Định dạng số", "P1", "",
         "1. Đọc các ô số tiền", "",
         "- Có dấu phẩy phân cách hàng nghìn\n- Ô bằng 0 hiện '-'"),
        ("005", "Dòng không gắn hợp đồng", "P2", "Khách có phiếu báo có chưa gắn hợp đồng",
         "1. Lọc theo khách đó\n2. Rê chuột vào dấu '-' ở cột Đơn hàng/hợp đồng", "",
         "- Có dòng '-' với chú thích 'Phiếu báo có hoặc kế toán chưa được ghi nhận'"),
        ("006", "Phân trang 15 hợp đồng", "P0", "Kết quả trên 15 hợp đồng",
         "1. Đếm dòng hợp đồng trang 1\n2. Sang trang 2", "",
         "- Trang 1 có 15 dòng hợp đồng (không tính dòng khách)\n"
         "- Trang 2 STT khách nối tiếp trang 1\n- Dòng Tổng cộng không đổi khi chuyển trang"),
        ("007", "Khách vắt qua 2 trang", "P2", "Một khách có hợp đồng nằm ở cuối trang 1 và đầu trang 2",
         "1. Đọc dòng khách ở trang 1 và trang 2", "",
         "- Ghi nhận: mỗi trang hiện dòng khách với tổng chỉ của các hợp đồng trên trang đó"),
        ("008", "Dòng Tổng cộng tính mọi trang", "P0", "Có nhiều trang",
         "1. Cộng tay cột 'Đã thanh toán' các trang\n2. So với dòng Tổng cộng", "",
         "- Bằng nhau (chênh lệch, nếu có, chỉ do bút toán chưa gắn khách)"),
        ("009", "Hợp đồng lập bên HRM", "P2", "Có hợp đồng lập ở hệ thống HRM đã phát sinh công nợ",
         "1. Lọc theo khách của hợp đồng đó", "",
         "- Cột Đơn hàng/hợp đồng hiện mã hợp đồng\n- Lỗi ERP đã biết: hiện dấu '-'"),
        ("010", "Khách hàng không còn trong danh mục", "P2",
         "Có bút toán gắn khách hàng đã bị xóa khỏi danh mục (nhờ đội phát triển chỉ định dữ liệu)",
         "1. Lọc kỳ chứa bút toán đó", "",
         "- Hợp đồng hiện dưới một dòng khách riêng\n"
         "- Lỗi ERP đã biết: hợp đồng bị dồn vào dòng của khách hàng đứng kế tiếp"),
    ]),

    ("IV", "Cửa sổ chi tiết phiếu", [
        ("001", "Bấm ô Hàng hóa/Dịch vụ", "P0", "Hợp đồng có phiếu xuất trong kỳ",
         "1. Bấm số ở cột 'Hàng hóa/Dịch vụ'", "",
         "- Mở cửa sổ danh sách phiếu: STT · Mã phiếu · Phát sinh nợ · Phát sinh có · Ngày lập · Người lập\n"
         "- Tổng Phát sinh nợ trừ Phát sinh có bằng số vừa bấm"),
        ("002", "Bấm ô Đã thanh toán", "P0", "Hợp đồng có phiếu thu trong kỳ",
         "1. Bấm số ở cột 'Đã thanh toán'", "",
         "- Cột: STT · Mã phiếu · Số tiền · Ngày lập · Người lập\n- Tổng Số tiền bằng số vừa bấm"),
        ("003", "Bấm ô Nhập trả lại, Điều chỉnh công nợ, Trả lại tiền thừa", "P1", "",
         "1. Lần lượt bấm từng ô", "",
         "- Mỗi cửa sổ chỉ có đúng loại phiếu của cột đó, tổng bằng số đã bấm"),
        ("004", "Tiêu đề cửa sổ", "P2", "",
         "1. Bấm ô cột 'Hàng hóa/Dịch vụ'", "",
         "- Ghi nhận: tiêu đề luôn là 'Chi tiết số tiền đã thanh toán' với mọi cột"),
        ("005", "Bấm ô bằng 0", "P2", "Dòng có ô hiện '-'",
         "1. Bấm vào dấu '-'", "",
         "- Ghi nhận: vẫn mở cửa sổ; có thể vẫn hiện phiếu (vd phiếu thu đã tính ở cột khác)"),
        ("006", "Cửa sổ của dòng khách hàng", "P2", "",
         "1. Bấm ô 'Đã thanh toán' ở dòng khách (chữ đậm)", "",
         "- Liệt kê phiếu của mọi hợp đồng của khách"),
    ]),

    ("V", "Làm mới & Xuất excel", [
        ("001", "Nút làm mới", "P1", "Đã nhập đủ ô lọc và có dữ liệu",
         "1. Bấm làm mới", "",
         "- Mọi ô lọc về trống (kể cả Từ ngày, Đến ngày, Số dư cuối kỳ)\n- Bảng xóa các dòng\n"
         "- Ghi nhận: dòng Tổng cộng vẫn giữ số cũ cho tới lần Lọc sau"),
        ("002", "Xuất excel gửi qua email", "P0", "Đã nhập kỳ",
         "1. Bấm 'Xuất excel'\n2. Kiểm tra hộp thư", "",
         "- Mở tab mới, thông báo 'Báo cáo chi tiết công nợ khách hàng sẽ gửi về mail của bạn trong ít phút!'\n"
         "- Vài phút sau nhận email kèm file Excel"),
        ("003", "Nội dung file Excel", "P0", "Đã nhận file",
         "1. Mở file, so với màn hình cùng bộ lọc", "",
         "- Đủ mọi hợp đồng (mọi trang), cột như màn hình\n- Dòng Tổng cộng khớp màn hình"),
        ("004", "Xuất excel khi Đến ngày nhỏ hơn Từ ngày", "P2", "",
         "1. Nhập ngày sai thứ tự, bấm 'Xuất excel'", "",
         "- Không gửi email; báo lỗi 'Đến ngày phải lớn hơn hoặc bằng Từ ngày'"),
        ("005", "Excel theo phạm vi quyền", "P1", "Tài khoản A (không quyền)",
         "1. Lọc, Xuất excel", "",
         "- File chỉ có hợp đồng A lập"),
    ]),

    ("VI", "Tạo phiếu - số liệu thay đổi (luồng end-to-end)", data_change_tcs("detail") + [
        ("018", "Phiếu mới hiện trong cửa sổ chi tiết", "P1", "Đã tạo phiếu thu ở TC 004",
         "1. Bấm ô 'Đã thanh toán' của HD-TEST-01", "",
         "- Cửa sổ có mã phiếu thu vừa lập, số tiền 4,000,000, người lập đúng"),
    ]),
]
