# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Ket chuyen chi phi phai tra'."""

MENU = "Mở menu Kế toán > mục \"Kết chuyển cuối kỳ\" > bấm \"Kết chuyển chi phí phải trả\""

# Du lieu mau dung chung
DATA = ("Công ty TPE có phòng kinh doanh PKD1, PKD2; công ty TPHP có phòng PKD9. Năm làm việc 2026, hôm nay "
        "06/11/2026.\n"
        "Tài khoản:\n"
        "- KT-1: kế toán TPE, có quyền \"Tạo kết chuyển chi phí phải trả\" và \"Xem kết chuyển chi phí phải "
        "trả theo công ty\"\n"
        "- KT-2: kế toán tổng công ty, có quyền \"Xem kết chuyển chi phí phải trả theo tổng công ty\" (không "
        "có quyền Tạo)\n"
        "- KT-3: kế toán TPE, chỉ có quyền \"Tạo kết chuyển chi phí phải trả\"\n"
        "- NV-A: nhân viên, không có quyền nào của màn này\n"
        "Số dư TK 3351 (chi phí phải trả) của PKD1, hợp đồng có xuất hóa đơn, ghi nhận trong năm 2026:\n"
        "- Vụ việc TTHHD (Thưởng thực hiện hợp đồng): HĐ-01 của NV-K1 dư Có 10.000.000 (ngày 15/09/2026); "
        "HĐ-02 của NV-K1 dư Có 5.000.000 (ngày 20/10/2026); HĐ-03 của NV-K2 dư Có 3.000.000 (ngày 25/10/2026)\n"
        "- Vụ việc TVC (Tiền vận chuyển): HĐ-01 của NV-K1 dư Nợ 500.000 (ngày 10/10/2026)\n"
        "- Vụ việc TNSQ (Thưởng năng suất quý): không có số dư\n"
        "Không được tính vào PKD1 / 31/10/2026:\n"
        "- HĐ-01 TTHHD 2.000.000 ngày 03/11/2026 (sau ngày tính)\n"
        "- HĐ-05 TTHHD 7.000.000 ngày 20/12/2025 (năm khác)\n"
        "- HĐ-06 (không xuất hóa đơn) TTHHD 1.000.000 ngày 01/10/2026\n"
        "- HĐ-07 của NV-K3 thuộc PKD2, TTHHD 9.000.000 ngày 01/10/2026")

OPEN_KT1 = "Đăng nhập KT-1, " + MENU
NEW_KT1 = OPEN_KT1 + ", bấm \"Thêm mới\""
HEAD = "Chọn Năm 2026, Tính đến ngày 31/10/2026, Phòng ban PKD1"

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Kết chuyển chi phí phải trả: cuối kỳ, kế toán chuyển số dư TK 3351 (chi phí phải trả ngắn hạn) đã "
     "ghi nhận cho nhân viên kinh doanh theo từng hợp đồng sang TK 33481 (phải trả người lao động khác), "
     "theo từng phòng ban và từng vụ việc (thưởng thực hiện hợp đồng, thưởng năng suất, tiền vận chuyển...).\n"
     "Người dùng làm được:\n"
     "- Xem danh sách phiếu kết chuyển, lọc theo số phiếu, người lập, phòng ban, ngày tạo.\n"
     "- Thêm mới: chọn Năm, Tính đến ngày, Phòng ban, thêm các dòng vụ việc (số tiền tự tính), bấm \"Lưu "
     "và duyệt\": phiếu được lưu và sinh bút toán ngay.\n"
     "- Xem chi tiết phiếu.\n"
     "Màn không có Sửa, Xóa, In, Xuất excel; không có bước duyệt riêng."),

    ("2. Đối tượng được tính / hiển thị",
     "Số tiền của một dòng vụ việc = tổng (Có trừ Nợ) TK 3351 của các bút toán thỏa đủ:\n"
     "- đúng vụ việc đã chọn, có nhân viên và có hợp đồng (hợp đồng hàng hoặc hợp đồng sửa chữa - bảo "
     "hành);\n"
     "- phòng ban của nhân viên trên bút toán là phòng ban đã chọn;\n"
     "- ngày hạch toán thuộc Năm đã chọn và không sau Tính đến ngày;\n"
     "- hợp đồng có xuất hóa đơn.\n"
     "Bút toán của các phiếu kết chuyển trước cũng được tính, nên phần đã kết chuyển tự trừ đi.\n"
     "Danh sách: STT, Số phiếu, Đến ngày, Ngày hạch toán, Phòng ban, Số tiền kết chuyển, Người tạo, Ngày "
     "tạo; mới nhất lên đầu."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Bút toán ngày sau Tính đến ngày, hoặc thuộc năm khác Năm đã chọn.\n"
     "- Bút toán của nhân viên thuộc phòng khác; bút toán không gắn nhân viên hoặc không gắn hợp đồng.\n"
     "- Hợp đồng không xuất hóa đơn (ô \"Xuất hóa đơn\" đang ẩn, phiếu luôn lưu là Có).\n"
     "- Danh sách: người không có quyền xem chỉ thấy phiếu mình tạo; quyền theo công ty thấy phiếu của các "
     "phòng đang hoạt động thuộc công ty mình.\n"
     "- Nút \"Thêm mới\" chỉ hiện với quyền \"Tạo kết chuyển chi phí phải trả\"."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "- Form: Năm (từ năm trước đến 10 năm sau) và Tính đến ngày (không được là ngày tương lai, phải thuộc "
     "Năm đã chọn). Ngày hạch toán tự lấy bằng Tính đến ngày, không sửa được.\n"
     "- Danh sách: Từ ngày / Đến ngày lọc theo Ngày tạo phiếu."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Thông tin chung: Số phiếu (tự sinh dạng <mã công ty người lập>.KCCPPT<năm>.<5 số>, ví dụ "
     "TPE.KCCPPT2026.00056), Năm, Tính đến ngày, Ngày hạch toán, Phòng ban, Ghi chú.\n"
     "Chi tiết: STT, Mã vụ việc (bắt buộc, không trùng), Tài khoản nợ 3351, Tài khoản có 33481, Số tiền. "
     "Nút + thêm dòng; dòng thứ 2 trở đi có nút xóa.\n"
     "Đổi Năm / Tính đến ngày / Phòng ban thì xóa hết các dòng chi tiết."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Số tiền kết chuyển của phiếu = tổng Số tiền các dòng.\n"
     "- Bút toán mỗi vụ việc: với từng cặp hợp đồng + nhân viên, số dư dương ghi Nợ 3351 (kèm hợp đồng, "
     "nhân viên); số dư âm ghi Có 3351. Phía 33481 gộp theo nhân viên + vụ việc, ghi ngược chiều.\n"
     "- Ngày hạch toán bút toán = Tính đến ngày; dòng làm tròn bằng 0 bị bỏ.\n"
     "Với dữ liệu mẫu (PKD1, 31/10/2026): TTHHD 18.000.000, TVC âm 500.000, tổng phiếu 17.500.000.\n"
     "Bút toán: Nợ 3351 10.000.000 (HĐ-01, NV-K1), 5.000.000 (HĐ-02, NV-K1), 3.000.000 (HĐ-03, NV-K2); "
     "Có 33481 15.000.000 (NV-K1), 3.000.000 (NV-K2); TVC: Có 3351 500.000 (HĐ-01) / Nợ 33481 500.000 "
     "(NV-K1)."),

    ("7. Phân quyền cấp",
     "- \"Tạo kết chuyển chi phí phải trả\": thấy nút Thêm mới, mở được form tạo.\n"
     "- \"Xem ... theo tổng công ty\": thấy mọi phiếu, mở mọi chi tiết.\n"
     "- \"Xem ... theo công ty\": thấy phiếu của phòng thuộc công ty mình; ô Phòng ban ở form chỉ có phòng "
     "công ty mình.\n"
     "- Không quyền xem: chỉ thấy phiếu mình tạo.\n"
     "- Lưu ý theo code hiện tại: chức năng lưu và chức năng tính số tiền không kiểm tra quyền.\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- Số tiền từng dòng tính ngay khi chọn vụ việc, thông báo \"Thêm thành công\".\n"
     "- Bút toán được hệ thống ghi chạy nền ngay sau khi lưu (thường vài giây); số tiền bút toán tính lại "
     "tại thời điểm ghi.\n"
     "- Danh sách hiện Số tiền kết chuyển có dấu phân cách, ngày dạng dd/mm/yyyy."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- Không chặn kết chuyển trùng phòng / kỳ / vụ việc, và Số tiền trên phiếu lấy theo số trình duyệt "
     "gửi lên: lưu lại từ một form mở từ trước thì phiếu ghi đủ số tiền nhưng không có bút toán nào "
     "(dữ liệu thật: TPE.KCCPPT2025.00010 trùng TPE.KCCPPT2025.00008, 492.706.613).\n"
     "- Không Sửa, không Xóa được phiếu đã lưu (đường dẫn sửa / xóa không có chức năng).\n"
     "- Lọc Số tiền từ / đến và Vụ việc không có tác dụng; lọc Đến ngày không gồm ngày cuối.\n"
     "- Người chỉ có quyền Tạo thấy phòng ban của mọi công ty ở form.\n"
     "- Màn chi tiết cho gõ Ghi chú nhưng không có nút lưu."),
]


ROLE_TCS = [
    ("00", "Không có quyền nào vẫn mở được danh sách nhưng chỉ thấy phiếu của mình", "P0",
     "NV-A không có quyền nào; trong hệ thống đã có phiếu do KT-1 tạo",
     "1. Đăng nhập NV-A\n"
     "2. " + MENU,
     "Tài khoản: NV-A",
     "- Màn danh sách mở được, không có nút \"Thêm mới\"\n"
     "- Bảng trống (NV-A chưa tạo phiếu nào), không thấy phiếu của KT-1"),

    ("01", "Quyền Tạo thấy nút Thêm mới và mở được form", "P0",
     DATA,
     "1. " + OPEN_KT1 + "\n"
     "2. Bấm \"Thêm mới\"",
     "—",
     "- Có nút \"Thêm mới\"\n"
     "- Mở form \"Tạo kết chuyển chi phí phải trả\", Năm mặc định 2026"),

    ("02", "Không có quyền Tạo mở thẳng đường dẫn tạo mới", "P0",
     DATA,
     "1. Đăng nhập KT-2\n"
     "2. Dán đường dẫn form tạo kết chuyển chi phí phải trả",
     "—",
     "- Ra trang không tìm thấy"),

    ("03", "Quyền xem theo công ty chỉ thấy phiếu công ty mình", "P0",
     DATA + "\nĐã có KC-01 (PKD1, TPE) và KC-09 (PKD9, TPHP)",
     "1. " + OPEN_KT1,
     "—",
     "- Có KC-01, không có KC-09"),

    ("04", "Quyền xem theo tổng công ty thấy mọi phiếu", "P0",
     DATA + "\nĐã có KC-01 (PKD1, TPE) và KC-09 (PKD9, TPHP)",
     "1. Đăng nhập KT-2, " + MENU,
     "—",
     "- Có cả KC-01 và KC-09"),

    ("05", "Mở chi tiết phiếu công ty khác qua đường dẫn", "P0",
     DATA + "\nKC-09 thuộc PKD9 (TPHP), do người TPHP tạo",
     "1. Đăng nhập KT-1\n"
     "2. Dán đường dẫn chi tiết KC-09",
     "—",
     "- Ra trang không tìm thấy"),

    ("06", "Người tạo luôn mở được chi tiết phiếu của mình", "P1",
     "KT-3 chỉ có quyền Tạo, đã tạo KC-03",
     "1. Đăng nhập KT-3, " + MENU + "\n"
     "2. Bấm số phiếu KC-03",
     "—",
     "- Danh sách có KC-03\n"
     "- Mở được màn chi tiết KC-03"),

    ("07", "Gọi thẳng chức năng lưu khi không có quyền Tạo", "P0",
     DATA,
     "1. Đăng nhập NV-A\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng lưu kết chuyển với PKD1, 31/10/2026, vụ việc TTHHD",
     "—",
     "- Mong đợi: bị chặn, không tạo phiếu, không sinh bút toán\n"
     "- Lưu ý: theo code hiện tại tạo được phiếu và sinh bút toán - ghi Failed"),

    ("08", "Gọi thẳng chức năng tính số tiền khi không có quyền", "P1",
     DATA,
     "1. Đăng nhập NV-A\n"
     "2. Dùng công cụ kiểm thử API gọi chức năng tính số tiền với PKD9, vụ việc TTHHD, năm 2026",
     "—",
     "- Mong đợi: bị chặn\n"
     "- Lưu ý: theo code hiện tại trả về số dư chi phí phải trả của PKD9 - ghi Failed"),

    ("09", "Người chỉ có quyền Tạo thấy phòng ban công ty khác", "P1",
     DATA,
     "1. Đăng nhập KT-3, " + MENU + ", bấm \"Thêm mới\"\n"
     "2. Mở ô Phòng ban",
     "—",
     "- Mong đợi: chỉ có phòng của TPE\n"
     "- Lưu ý: theo code hiện tại có cả PKD9 của TPHP - ghi Failed"),
]
