# -*- coding: utf-8 -*-
"""Noi dung TC man ERP: Bang doi chieu cong no 1 khach hang (saleReports.compareCustomerDebts)."""
from common import COT_SO_LIEU, DU_LIEU_MAU, data_change_tcs

Q = "Xem báo cáo đối soát công nợ khách hàng theo "

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Bảng đối chiếu công nợ của MỘT khách hàng trong một kỳ, liệt kê TỪNG CHỨNG TỪ phát sinh theo từng "
     "hợp đồng (phiếu xuất, phiếu thu, phiếu nhập trả...), dùng để gửi khách xác nhận công nợ. Có In và "
     "Xuất excel.\n"
     "Đường vào: menu Kinh doanh > Báo cáo công nợ > 'Bảng đối chiếu công nợ 1 khách hàng'."),

    ("2. Đối tượng được tính / hiển thị",
     COT_SO_LIEU + "\n"
     "Dòng chứng từ: mỗi phiếu hạch toán trong kỳ của hợp đồng là một dòng, theo thứ tự ngày."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu chưa hạch toán.\n- Phiếu ngoài kỳ (trước Từ ngày chỉ góp vào Số dư đầu kỳ của dòng Tổng cộng).\n"
     "- Bút toán của khách không gắn hợp đồng: không có dòng riêng nhưng VẪN tính vào dòng Tổng cộng."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "BẮT BUỘC đủ 3 ô: Từ ngày, Đến ngày, Khách hàng. Lọc theo NGÀY HẠCH TOÁN.\n"
     "Cột Ngày chứng từ hiển thị ngày hạch toán của từng phiếu."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Bảng 13 cột: STT · Ngày chứng từ · Số chứng từ · Diễn giải · Số dư đầu kỳ · [Phát sinh tăng: Hàng "
     "hóa/Dịch vụ · Điều chỉnh công nợ] · [Phát sinh giảm: Nhập trả lại · Đã thanh toán · Điều chỉnh công "
     "nợ] · Trả lại tiền thừa · Số dư cuối kì.\n"
     "- Dòng hợp đồng (chữ đậm, STT 1, 2...): link hợp đồng, tổng của hợp đồng.\n"
     "- Dòng chứng từ (STT 1.1, 1.2...): Số chứng từ là mã phiếu; phiếu xuất kho / xuất bán hàng mượn / "
     "phiếu nhập kèm mã phiếu yêu cầu trong ngoặc; cột Số dư cuối kì là số dư CHẠY sau từng chứng từ.\n"
     "- Dòng Tổng cộng dưới tiêu đề.\n"
     "Phân trang 15 HỢP ĐỒNG mỗi trang."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "Các điểm GHI NHẬN của màn này (khác 2 màn kia, hiện trạng ERP, KHÔNG ghi Failed):\n"
     "- 'Số dư đầu kỳ' của từng dòng hợp đồng luôn trống / bằng 0; số dư đầu kỳ chỉ có ở dòng Tổng cộng.\n"
     "- 'Số dư cuối kì' của dòng hợp đồng và số dư chạy của dòng chứng từ KHÔNG tính 2 cột Điều chỉnh công "
     "nợ.\n"
     "- Dòng Tổng cộng tính đủ mọi cột, mọi bút toán của khách (kể cả không gắn hợp đồng), cộng Số dư đầu "
     "kỳ. Vì vậy Tổng cộng có thể khác tổng các dòng hợp đồng."),

    ("7. Phân quyền cấp",
     "4 quyền '" + Q + "tổng công ty / công ty / phòng ban / bộ phận' CHỈ quyết định hiện các ô lọc Công ty, "
     "Phòng ban, Bộ phận, Nhân viên (như màn Chi tiết). Màn KHÔNG giới hạn dữ liệu theo quyền: ai cũng tra "
     "được mọi khách hàng (lỗi bảo mật, xem mục 9)."),

    ("8. Cách tính các ô thống kê",
     "- Số hiển thị có dấu phẩy, ô bằng 0 hiện '-'.\n"
     "- Bấm Số chứng từ của phiếu xuất kho / phiếu xuất bán hàng mượn: mở cửa sổ 'Danh sách hàng hóa: ...' "
     "(nút 'Chi tiết' mở phiếu, nút 'Hủy' đóng). Các chứng từ khác mở phiếu ở tab mới.\n"
     "- In: bản in khổ ngang theo mẫu đối soát công nợ. Xuất excel: tải ngay file "
     "'bang_doi_chieu_cong_no_1_khach_hang.xlsx'."),

    ("9. Ghi chú đọc bảng",
     DU_LIEU_MAU + "\n"
     "Các lỗi ERP ĐÃ BIẾT (thấy đúng hiện tượng thì ghi Failed, chép câu 'Lỗi ERP đã biết' vào Ghi chú):\n"
     "(1) Không giới hạn theo quyền: nhân viên không có quyền nào vẫn tra được công nợ của mọi khách hàng.\n"
     "(2) Hệ thống chia trang TRƯỚC rồi mới bỏ các hợp đồng toàn số 0, nên nhiều trang đầu có thể trống và "
     "STT nhảy cóc.\n"
     "(3) Cột Diễn giải của phiếu thu / phiếu chi / ủy nhiệm chi luôn trống.\n"
     "(4) Bản in: dòng Từ ngày / Đến ngày / Số hợp đồng trống; dòng Tổng cộng đảo chỗ 2 cột Điều chỉnh công nợ.\n"
     "(5) Khách có hợp đồng lập bên hệ thống HRM: bấm Lọc báo lỗi, không hiện bảng.\n"
     "Ghi nhận: ô Khách hàng cho chọn nhiều khách dù tên màn là '1 khách hàng'."),
]

ROLE_TCS = [
    ("00", "Không quyền vẫn tra được khách của người khác", "P0",
     "Tài khoản A không có 4 quyền xem. KH-KHAC là khách chỉ có hợp đồng do nhân viên phòng khác lập",
     "1. Đăng nhập A, mở màn, quan sát bộ lọc\n2. Chọn KH-KHAC, nhập kỳ, bấm 'Lọc'", "Tài khoản: A",
     "- Không có ô Công ty, Phòng ban, Bộ phận, Nhân viên\n"
     "- Không xem được hợp đồng của người khác (bảng trống)\n"
     "- Lỗi ERP đã biết: hiện đủ hợp đồng và chứng từ của KH-KHAC"),
    ("01", "Quyền theo tổng công ty hiện đủ ô lọc", "P1",
     "Tài khoản E có quyền '" + Q + "tổng công ty'",
     "1. Đăng nhập E, mở màn", "Tài khoản: E", "- Có ô Công ty, Phòng ban, Bộ phận, Nhân viên"),
    ("02", "Quyền theo công ty", "P1", "Tài khoản D có quyền '" + Q + "công ty'",
     "1. Đăng nhập D, mở màn", "Tài khoản: D", "- Có ô Phòng ban, Bộ phận, Nhân viên; không có ô Công ty"),
    ("03", "Quyền theo phòng ban", "P2", "Tài khoản C có quyền '" + Q + "phòng ban'",
     "1. Đăng nhập C, mở màn", "Tài khoản: C", "- Chỉ có ô Bộ phận, Nhân viên"),
    ("04", "Quyền theo bộ phận", "P2", "Tài khoản B có quyền '" + Q + "bộ phận'",
     "1. Đăng nhập B, mở màn", "Tài khoản: B", "- Có ô Phòng ban, Bộ phận, Nhân viên"),
]

SECTIONS = [
    ("I", "Giao diện & mở màn", [
        ("001", "Bố cục màn hình", "P0", "Tài khoản quyền tổng công ty",
         "1. Menu Kinh doanh > Báo cáo công nợ > 'Bảng đối chiếu công nợ 1 khách hàng'", "",
         "- Tiêu đề 'Bảng đối chiếu công nợ 1 khách hàng'\n"
         "- Ô lọc: Từ ngày* · Đến ngày* · Khách hàng* · Số hợp đồng · Công ty · Phòng ban · Bộ phận · Nhân viên\n"
         "- Nút: 'Lọc' · làm mới · 'Xuất excel' · 'In'"),
        ("002", "Không tự tải khi mở", "P0", "", "1. Quan sát bảng", "", "- 'Chưa có dữ liệu'"),
        ("003", "Tiêu đề cột", "P0", "", "1. Đọc tiêu đề", "",
         "- STT · Ngày chứng từ · Số chứng từ · Diễn giải · Số dư đầu kỳ · Phát sinh tăng (Hàng hóa/Dịch vụ, "
         "Điều chỉnh công nợ) · Phát sinh giảm (Nhập trả lại, Đã thanh toán, Điều chỉnh công nợ) · Trả lại "
         "tiền thừa · Số dư cuối kì"),
    ]),

    ("II", "Bộ lọc bắt buộc & lọc", [
        ("001", "Thiếu Khách hàng", "P0", "Đã nhập 2 ô ngày",
         "1. Để trống Khách hàng, bấm 'Lọc'", "",
         "- Thông báo 'Chưa chọn đủ điều kiện bắt buộc', dưới ô Khách hàng hiện 'Bắt buộc chọn'"),
        ("002", "Thiếu ngày", "P0", "Đã chọn khách", "1. Xóa Từ ngày, bấm 'Lọc'", "",
         "- Thông báo 'Chưa chọn đủ điều kiện bắt buộc'"),
        ("003", "Lọc 1 khách hàng", "P0", "KH-TEST có 2 hợp đồng phát sinh trong kỳ",
         "1. Nhập kỳ, chọn KH-TEST, bấm 'Lọc'", "",
         "- 2 dòng hợp đồng chữ đậm, mỗi dòng có các dòng chứng từ bên dưới theo thứ tự ngày"),
        ("004", "Ô Khách hàng chọn được nhiều", "P2", "", "1. Chọn 2 khách, lọc", "",
         "- Ghi nhận: chọn được 2 khách, bảng gộp hợp đồng của cả 2"),
        ("005", "Lọc Số hợp đồng", "P1", "", "1. Thêm Số hợp đồng = HD-TEST-01, lọc", "",
         "- Chỉ hợp đồng HD-TEST-01"),
        ("006", "Lọc Nhân viên / Phòng ban", "P2", "Tài khoản quyền tổng công ty",
         "1. Chọn Nhân viên A (người lập HD-TEST-01), lọc", "",
         "- Chỉ hợp đồng do A lập của khách đã chọn"),
    ]),

    ("III", "Bảng chứng từ", [
        ("001", "Dòng chứng từ phiếu xuất kho", "P0", "HD-TEST-01 có phiếu xuất trong kỳ",
         "1. Đọc dòng chứng từ phiếu xuất", "",
         "- Ngày chứng từ, Số chứng từ dạng 'Mã phiếu xuất (Mã yêu cầu xuất hàng)'\n"
         "- Số tiền ở cột Hàng hóa/Dịch vụ"),
        ("002", "Cửa sổ danh sách hàng của phiếu xuất", "P0", "",
         "1. Bấm Số chứng từ phiếu xuất", "",
         "- Cửa sổ 'Danh sách hàng hóa: Phiếu xuất hàng - <mã>' liệt kê hàng, số lượng, đơn giá, thành tiền\n"
         "- Nút 'Chi tiết' mở phiếu xuất ở tab mới, nút 'Hủy' đóng cửa sổ"),
        ("003", "Phiếu xuất bán hàng mượn", "P1", "Có phiếu xuất bán hàng mượn trong kỳ",
         "1. Bấm Số chứng từ", "",
         "- Cửa sổ có tiêu đề 'Danh sách hàng hóa: Phiếu xuất bán hàng mượn' kèm mã phiếu"),
        ("004", "Phiếu nhập trả lại", "P1", "Có phiếu nhập trả lại",
         "1. Đọc và bấm Số chứng từ", "",
         "- Dạng 'Mã phiếu nhập (Mã yêu cầu nhập hàng)'; bấm mở phiếu nhập ở tab mới"),
        ("005", "Phiếu thu và cột Diễn giải", "P1", "Có phiếu thu trong kỳ, phiếu có nội dung diễn giải",
         "1. Đọc dòng phiếu thu", "",
         "- Diễn giải hiện nội dung của phiếu thu\n- Lỗi ERP đã biết: Diễn giải trống"),
        ("006", "Số dư chạy", "P0", "Hợp đồng có 3 chứng từ: xuất 10,000,000; thu 4,000,000; nhập trả 3,000,000",
         "1. Đọc cột Số dư cuối kì của 3 dòng chứng từ", "",
         "- Lần lượt 10,000,000 · 6,000,000 · 3,000,000"),
        ("007", "Số dư đầu kỳ của dòng hợp đồng", "P2", "Hợp đồng còn nợ từ trước kỳ",
         "1. Đọc cột Số dư đầu kỳ của dòng hợp đồng", "",
         "- Ghi nhận: trống / '-'; số dư cũ chỉ nằm ở dòng Tổng cộng"),
        ("008", "Phân trang và trang trống", "P1",
         "Khách có rất nhiều hợp đồng, nhiều hợp đồng không có phát sinh trong kỳ",
         "1. Lọc khách đó\n2. Xem trang 1, 2, 3 và cột STT", "",
         "- Trang nào cũng có dữ liệu, STT liên tục\n"
         "- Lỗi ERP đã biết: một số trang đầu trống, STT nhảy cóc"),
        ("009", "Khách có hợp đồng lập bên HRM", "P2", "Khách có hợp đồng lập ở HRM đã phát sinh công nợ",
         "1. Lọc khách đó", "",
         "- Bảng hiện bình thường\n- Lỗi ERP đã biết: báo lỗi hệ thống, không hiện bảng"),
    ]),

    ("IV", "In & Xuất excel", [
        ("001", "In thiếu điều kiện", "P1", "Chưa chọn khách", "1. Bấm 'In'", "",
         "- Thông báo 'Chưa chọn đủ điều kiện bắt buộc'"),
        ("002", "Bản in", "P0", "Đã lọc KH-TEST", "1. Bấm 'In'", "",
         "- Mở tab mới bản in khổ ngang, đủ hợp đồng và chứng từ như màn hình (mọi trang)\n"
         "- Dòng Từ ngày / Đến ngày / Số hợp đồng ghi đúng kỳ đang lọc\n"
         "- Lỗi ERP đã biết: 3 thông tin này trống"),
        ("003", "Dòng Tổng cộng trên bản in", "P1", "", "1. So dòng Tổng cộng bản in với màn hình", "",
         "- Từng cột khớp màn hình\n- Lỗi ERP đã biết: 2 cột Điều chỉnh công nợ bị đảo chỗ"),
        ("004", "Xuất excel", "P0", "Đã lọc KH-TEST", "1. Bấm 'Xuất excel'", "",
         "- Tải ngay file 'bang_doi_chieu_cong_no_1_khach_hang.xlsx'\n"
         "- Có ảnh đầu trang công ty, khoảng ngày, bảng như màn hình, đủ mọi trang"),
        ("005", "Xuất excel thiếu điều kiện", "P2", "Chưa chọn khách", "1. Bấm 'Xuất excel'", "",
         "- Thông báo 'Chưa chọn đủ điều kiện bắt buộc', không tải file"),
    ]),

    ("V", "Tạo phiếu - số liệu thay đổi (luồng end-to-end)", data_change_tcs("compare") + [
        ("018", "Đối chiếu bản in với khách sau khi phát sinh phiếu", "P1",
         "Đã chạy chuỗi phiếu TC 002 đến 010",
         "1. In bảng đối chiếu KH-TEST kỳ tháng này\n2. So với danh sách phiếu đã lập", "",
         "- Bản in có đủ từng phiếu đã lập, đúng ngày, đúng số tiền, đúng cột"),
    ]),
]
