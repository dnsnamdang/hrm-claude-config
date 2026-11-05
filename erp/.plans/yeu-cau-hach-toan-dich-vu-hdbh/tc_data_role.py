# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Yeu cau hach toan dich vu - HDBH'."""

MENU = "Mở menu Kế toán > Bán Dịch vụ > bấm \"Yêu cầu hạch toán dịch vụ - HĐBH\""
MENU_HD = "Mở Kinh doanh > Đơn hàng - hợp đồng > \"Danh sách HĐ\""

# Du lieu mau dung chung
HD = ("HD-01: hợp đồng do KD-1 (TPE, phòng PKD1) lập, trạng thái Có hiệu lực, đã có phiếu Hỗ trợ hạch toán.\n"
      "- Dịch vụ đi kèm: DV1 \"Lắp đặt\" 2.000.000, DV2 \"Cấu hình\" 1.000.000 (VAT 10%)\n"
      "- Chi phí khác: CP1 \"Chi phí lắp dựng\" 500.000 (VAT 10%)\n"
      "- Chi phí vận chuyển 300.000 (VAT 8%), chưa hạch toán")

KD1 = "Đăng nhập KD-1 (người lập HD-01)"
KT1 = "KT-1 thuộc TPE, có quyền \"Hạch toán yêu cầu làm dịch vụ\""

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Yêu cầu hạch toán dịch vụ - HĐBH: nhân viên kinh doanh lập phiếu đề nghị kế toán hạch toán doanh thu "
     "dịch vụ đi kèm, chi phí khác hoặc chi phí vận chuyển của một hợp đồng bán hàng / đơn hàng.\n"
     "Người dùng làm được: lập phiếu từ hợp đồng (3 kiểu: Dịch vụ, Chi phí khác, Chi phí vận chuyển), chọn "
     "dòng cần hạch toán, đính kèm file, Lưu hoặc Lưu & Gửi duyệt, Sửa / Xóa phiếu của mình khi Đang tạo "
     "hoặc Không duyệt. Kế toán: Không duyệt (bắt buộc ghi chú) hoặc bấm \"Hạch toán dịch vụ\" để lập Phiếu "
     "hạch toán dịch vụ - HĐBH. Có Xuất excel danh sách."),

    ("2. Đối tượng được tính / hiển thị",
     "- Danh sách (menu, loại \"Tất cả\"): phiếu của người dùng và phiếu trong phạm vi quyền xem (tổng công "
     "ty / công ty / phòng ban / bộ phận, xét theo người lập); phiếu Đang tạo chỉ người lập thấy.\n"
     "- Danh sách chờ duyệt (từ ô trang chủ \"Yêu cầu hạch toán dịch vụ cần phê duyệt\"): phiếu Chờ duyệt "
     "của công ty mình.\n"
     "- Mỗi phiếu gắn đúng 1 hợp đồng / đơn hàng; mỗi dòng dịch vụ / chi phí của hợp đồng chỉ được gửi duyệt "
     "1 lần.\n"
     "- Sắp xếp: phiếu mới lập nhất lên đầu."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu Đang tạo của người khác.\n"
     "- Dòng giảm (từ phụ lục giảm) của hợp đồng không hiện khi lập phiếu.\n"
     "- Dòng đã nằm trong phiếu khác đang Chờ duyệt / Đã hạch toán: vẫn hiện nhưng tô đỏ, chọn sẽ bị chặn khi "
     "gửi.\n"
     "- Không có nút In."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Ô Từ ngày / Đến ngày lọc theo Ngày lập phiếu (đến hết ngày ở ô Đến ngày).\n"
     "Lưu ý: theo code hiện tại chỉ áp dụng Đến ngày, ô Từ ngày không có tác dụng (xem mục 9)."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Bộ lọc: Mã, Số hợp đồng, Trạng thái, Người duyệt, Khách hàng, Người lập, Người yêu cầu, Từ ngày / Đến "
     "ngày, Công ty / Phòng ban (người có quyền xem rộng).\n"
     "Bảng: STT, Ngày lập, Mã phiếu (mã dạng <mã công ty>.YCHTDV.xxxxx), Số đơn hàng/hợp đồng, Kinh doanh "
     "(người lập hợp đồng), Khách hàng, Tổng thanh toán, Người lập, Người duyệt, Ngày duyệt, Trạng thái, "
     "Hành động (Sửa, Xóa, Hạch toán dịch vụ).\n"
     "Form: Kiểu hạch toán, Chọn đơn hàng/hợp đồng, Ghi chú, thông tin khách hàng, File đính kèm; tab Dịch vụ "
     "đi kèm (kiểu Dịch vụ) hoặc Chi phí (kiểu Chi phí khác / Chi phí vận chuyển) có ô chọn từng dòng.\n"
     "Trạng thái: Đang tạo > Chờ duyệt > Đã hạch toán; hoặc Chờ duyệt > Không duyệt."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Tổng trước thuế = tổng \"Giá trị sau giảm giá\" của các dòng được chọn.\n"
     "- VAT = Tổng trước thuế x % VAT (làm tròn số nguyên); % VAT lấy theo dòng đầu tiên của nhóm (dịch vụ "
     "đi kèm hoặc chi phí) trên hợp đồng; vận chuyển lấy % VAT vận chuyển.\n"
     "- Tổng thanh toán = Tổng sau thuế.\n"
     "Với HD-01: chọn DV1 + DV2 = 3.000.000, VAT 300.000, Tổng thanh toán 3.300.000; CP1 = 550.000; vận "
     "chuyển = 324.000.\n"
     "- Khi Gửi duyệt, các dòng được chọn bị đánh dấu đã yêu cầu; Không duyệt thì trả lại."),

    ("7. Phân quyền cấp",
     "- Lập phiếu: chỉ người lập hợp đồng, hợp đồng phải Có hiệu lực và có phiếu Hỗ trợ hạch toán.\n"
     "- Sửa / Xóa: người lập phiếu, khi Đang tạo hoặc Không duyệt.\n"
     "- Không duyệt / Hạch toán dịch vụ: quyền \"Hạch toán yêu cầu làm dịch vụ\", phiếu Chờ duyệt.\n"
     "- Xem danh sách: 4 quyền \"Xem yêu cầu hạch toán làm dịch vụ của tổng công ty / công ty / phòng ban / bộ "
     "phận\"; không có quyền nào thì chỉ thấy phiếu mình lập.\n"
     "- Xem chi tiết: Super Admin, người lập, người duyệt, hoặc có quyền xem tương ứng.\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- Ô trang chủ \"Yêu cầu hạch toán dịch vụ cần phê duyệt\" (người có quyền Hạch toán yêu cầu làm dịch "
     "vụ) = số phiếu Chờ duyệt của công ty mình.\n"
     "- Phân trang 10 dòng, STT liên tục.\n"
     "- Xuất excel: file danh_sach_yeu_cau_hach_toan_lam_dich_vu.xlsx theo bộ lọc đang chọn, dòng tiêu đề "
     "ghi khoảng ngày lọc."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- Kế toán không có quyền xem của tổng công ty bấm Mã phiếu ở danh sách chờ duyệt thì ra trang không tìm "
     "thấy, nên không bấm được Không duyệt.\n"
     "- Chức năng Không duyệt không kiểm tra quyền và trạng thái: gọi thẳng thì đưa được phiếu Đã hạch toán "
     "về Không duyệt, các dòng được mở lại để yêu cầu lần nữa.\n"
     "- Phiếu kiểu Chi phí vận chuyển mở Sửa không có dòng nào, không lưu lại được.\n"
     "- Sửa phiếu của hợp đồng: tab Chi phí hiện thêm dòng giảm và dòng Chi phí vận chuyển; dòng VAT biến mất.\n"
     "- Gửi duyệt từ màn Sửa: thông báo gửi tới người có quyền \"Duyệt yêu cầu làm dịch vụ\", không phải kế "
     "toán.\n"
     "- Lọc Từ ngày và lọc Người duyệt không có tác dụng.\n"
     "- Cột Kinh doanh trong file Excel là người lập phiếu, không phải người lập hợp đồng."),
]


ROLE_TCS = [
    ("00", "Không có quyền xem chỉ thấy phiếu mình lập", "P0",
     "NV-A không có quyền nào trong 4 quyền xem yêu cầu hạch toán làm dịch vụ; NV-A lập 1 phiếu, KD-1 lập "
     "3 phiếu Chờ duyệt",
     "1. Đăng nhập NV-A\n"
     "2. " + MENU,
     "Tài khoản: NV-A",
     "- Danh sách chỉ có 1 phiếu của NV-A"),

    ("01", "Quyền xem của công ty thấy phiếu cả công ty", "P0",
     "QL-1 thuộc TPE có quyền \"Xem yêu cầu hạch toán làm dịch vụ của công ty\"; TPE có 5 phiếu Chờ duyệt, "
     "TPC có 2 phiếu",
     "1. Đăng nhập QL-1, mở màn từ menu",
     "—",
     "- Thấy 5 phiếu của TPE, không thấy phiếu TPC\n"
     "- Không thấy phiếu Đang tạo của người khác"),

    ("02", "Quyền xem của tổng công ty thấy mọi công ty", "P0",
     "TGD có quyền \"Xem yêu cầu hạch toán làm dịch vụ của tổng công ty\"",
     "1. Đăng nhập TGD, mở màn",
     "—",
     "- Thấy phiếu của TPE và TPC (trừ phiếu Đang tạo của người khác)"),

    ("03", "Quyền xem của công ty mở được chi tiết phiếu", "P0",
     "QL-1 có quyền xem của công ty (TPE); YC-1 Chờ duyệt do KD-1 (TPE) lập",
     "1. QL-1 bấm Mã phiếu YC-1 ở danh sách",
     "—",
     "- Mong đợi: mở màn chi tiết YC-1\n"
     "- Lưu ý: theo code hiện tại ra trang không tìm thấy (quyền xem của công ty / phòng ban / bộ phận không "
     "được xét ở màn chi tiết) - ghi Failed"),

    ("04", "Kế toán mở phiếu chờ duyệt để Không duyệt", "P0",
     KT1 + ", không có quyền xem nào; YC-1 Chờ duyệt của TPE",
     "1. KT-1 bấm ô trang chủ \"Yêu cầu hạch toán dịch vụ cần phê duyệt\"\n"
     "2. Bấm Mã phiếu YC-1",
     "—",
     "- Mong đợi: mở chi tiết, có nút Không duyệt và Hạch toán dịch vụ\n"
     "- Lưu ý: theo code hiện tại ra trang không tìm thấy - ghi Failed"),

    ("05", "Không có quyền Hạch toán thì không có nút xử lý", "P0",
     "QL-1 có quyền xem của tổng công ty nhưng không có quyền \"Hạch toán yêu cầu làm dịch vụ\"; YC-1 Chờ "
     "duyệt",
     "1. QL-1 mở chi tiết YC-1\n"
     "2. Mở menu Hành động của YC-1 ở danh sách",
     "—",
     "- Chi tiết chỉ có nút Quay lại\n"
     "- Menu Hành động không có \"Hạch toán dịch vụ\""),

    ("06", "Gọi thẳng chức năng Không duyệt khi không có quyền", "P0",
     "NV-A không có quyền \"Hạch toán yêu cầu làm dịch vụ\"; YC-1 Chờ duyệt",
     "1. Dùng công cụ kiểm thử API gọi chức năng Không duyệt YC-1 với ghi chú \"test\"",
     "—",
     "- Mong đợi: bị chặn, YC-1 vẫn Chờ duyệt\n"
     "- Lưu ý: theo code hiện tại YC-1 chuyển Không duyệt, Người duyệt là NV-A - ghi Failed"),

    ("07", "Người khác không sửa / xóa được phiếu", "P1",
     "YC-2 Đang tạo do KD-1 lập; KD-2 cùng phòng có đường dẫn Sửa và Xóa",
     "1. Đăng nhập KD-2, dán đường dẫn Sửa YC-2\n"
     "2. Dán đường dẫn Xóa YC-2",
     "—",
     "- Bước 1: trang không tìm thấy\n"
     "- Bước 2: thông báo \"Không thể xóa!\", YC-2 còn nguyên"),
]
