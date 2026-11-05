# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Phieu hach toan dich vu - HDBH'."""

MENU = ("Mở menu Kế toán > \"Hàng hoá - Dịch vụ - Vận chuyển\" > nhóm \"Bán Dịch vụ\" > bấm \"Phiếu hạch toán "
        "dịch vụ - HĐBH\"")
MENU_YC = ("Mở menu Kế toán > \"Hàng hoá - Dịch vụ - Vận chuyển\" > nhóm \"Bán Dịch vụ\" > bấm \"Yêu cầu hạch "
           "toán dịch vụ - HĐBH\"")

# Du lieu mau dung chung
HD = ("Hợp đồng bán hàng HD-01 (hợp đồng hãng, Có hiệu lực) của khách KH-1, người lập NV-1 thuộc TPE. "
      "Dịch vụ đi kèm \"Lắp đặt\": giá niêm yết 2.000.000, doanh số vượt trội 0, giảm giá 200.000, VAT 10%, "
      "hệ số giá vốn 60%. Phí vận chuyển 500.000, VAT vận chuyển 8%")
YC1 = ("Phiếu yêu cầu hạch toán dịch vụ YC-1 kiểu Dịch vụ của HD-01 do NV-1 lập, gồm dòng \"Lắp đặt\", "
       "trạng thái Chờ duyệt")
YC2 = ("Phiếu yêu cầu hạch toán dịch vụ YC-2 kiểu Vận chuyển của HD-01 do NV-1 lập, gồm dòng \"Chi phí vận "
       "chuyển\" 500.000, trạng thái Chờ duyệt")
KT1 = "KT-1 thuộc TPE có quyền \"Hạch toán yêu cầu làm dịch vụ\""
TAO = ("KT-1 " + MENU_YC + ", bấm mã YC-1, bấm \"Hạch toán dịch vụ\"")

# So lieu ky vong cho YC-1
TIEN_YC1 = "Tổng thanh toán 1.980.000 (giá trên hợp đồng 1.800.000 + VAT 180.000)"

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Phiếu hạch toán dịch vụ - HĐBH: kế toán lập từ một Phiếu yêu cầu hạch toán dịch vụ đang Chờ duyệt "
     "(của hợp đồng bán hàng) để ghi nhận doanh thu dịch vụ đi kèm, chi phí hoặc phí vận chuyển của hợp "
     "đồng vào sổ: sinh bút toán doanh thu, giảm trừ doanh thu, giá vốn và các khoản thưởng, thuế, quỹ rủi "
     "ro theo tỷ lệ; ghi công nợ phải thu khách hàng.\n"
     "Người dùng làm được: lập phiếu (Lưu hoặc Lưu & Duyệt), sửa / xóa phiếu Đang tạo của mình, xem chi "
     "tiết và tab Hạch toán, xuất Excel danh sách."),

    ("2. Đối tượng được tính / hiển thị",
     "- Dòng chi tiết lấy nguyên từ phiếu yêu cầu: tab \"Dịch vụ đi kèm\" (hoặc \"Chi phí\") gồm Giá niêm "
     "yết, Doanh số vượt trội, Giá bán, Giảm giá, Giá trên hợp đồng, Giá vốn; không sửa được.\n"
     "- Tổng thanh toán = Giá trên hợp đồng + VAT. VAT lấy theo hợp đồng: kiểu Dịch vụ theo VAT dịch vụ đi "
     "kèm, kiểu Chi phí theo VAT chi phí, kiểu Vận chuyển theo VAT vận chuyển.\n"
     "- Giá vốn = Giá niêm yết nhân hệ số giá vốn.\n"
     "- Thông tin khách hàng, Tài khoản nợ 1311, doanh thu 5113, giá vốn 632, chiết khấu 5211, thuế 33311.\n"
     "- Danh sách: phiếu theo quyền xem; phiếu Đang tạo chỉ người lập thấy."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu yêu cầu không ở trạng thái Chờ duyệt không lập được phiếu.\n"
     "- Phiếu Đang tạo của người khác.\n"
     "- Kiểu Vận chuyển không có bút toán giá vốn.\n"
     "- Bút toán có số tiền bằng 0 không được ghi.\n"
     "- Không có In; không có Hủy duyệt sau khi Đã duyệt."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Từ ngày / Đến ngày lọc theo Ngày lập phiếu (tính trọn ngày Đến ngày). Bút toán ghi theo thời điểm bấm "
     "Lưu & Duyệt."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Bộ lọc: Từ ngày, Đến ngày, Mã, Số hợp đồng, Trạng thái, Người duyệt, Khách hàng, Dịch vụ, Số tiền từ, "
     "Số tiền đến; Công ty / Phòng ban (khi có quyền xem rộng).\n"
     "Bảng: STT, Ngày lập, Mã, Số hợp đồng, Khách hàng, Tổng thanh toán, Người lập, Ngày duyệt, Trạng thái, "
     "Hành động (Sửa, Xóa).\n"
     "Form: Chọn phiếu yêu cầu hạch toán dịch vụ (bắt buộc), Ghi chú, thông tin khách, bảng chi tiết; nút "
     "Lưu, Lưu & Duyệt, Hủy.\n"
     "Chi tiết: tab Thông tin, tab Hạch toán (danh sách bút toán theo nhóm)."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "Với YC-1 (Lắp đặt 2.000.000, giảm 200.000, VAT 10%, hệ số giá vốn 60%):\n"
     "- Doanh thu: Nợ 1311 2.200.000 / Có 5113 2.000.000, Có 33311 200.000\n"
     "- Giảm trừ: Nợ 5213 200.000, Nợ 33311 20.000 / Có 1311 220.000\n"
     "- Giá vốn: Nợ 632 1.200.000 / Có 1541 1.200.000\n"
     "- Công nợ khách KH-1 tăng 1.980.000 (bằng Tổng thanh toán)\n"
     "Với YC-2 (vận chuyển 500.000, VAT 8%): Nợ 1311 540.000 / Có 5113 500.000, Có 33311 40.000; không có giá "
     "vốn.\n"
     "Phụ lục bổ sung: bút toán ghi về hợp đồng gốc."),

    ("7. Phân quyền cấp",
     "- Nút \"Hạch toán dịch vụ\" ở phiếu yêu cầu cần quyền \"Hạch toán yêu cầu làm dịch vụ\".\n"
     "- Xem danh sách: \"Xem hạch toán dịch vụ theo tổng công ty\" / \"... theo công ty\" / \"... theo phòng "
     "ban\"; không có thì chỉ thấy phiếu mình lập.\n"
     "- Sửa, Xóa: chỉ người lập, khi phiếu Đang tạo.\n"
     "- Chức năng lưu phiếu không kiểm tra quyền.\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- Danh sách phân trang, phiếu mới lập nhất lên đầu.\n"
     "- Khi Lưu & Duyệt: phiếu yêu cầu chuyển \"Đã hạch toán\", đề nghị xuất dịch vụ gốc (nếu có) chuyển Đã "
     "hạch toán, người lập phiếu yêu cầu nhận thông báo \"Phiếu yêu cầu hạch toán làm dịch vụ của bạn đã "
     "được duyệt\"; hợp đồng cập nhật ngày bàn giao và hạn thanh toán khi đã xuất và hạch toán đủ; dòng "
     "\"Chi phí vận chuyển\" đánh dấu hợp đồng đã hạch toán vận chuyển.\n"
     "- Xuất excel: file \"DANH SÁCH HẠCH TOÁN DỊCH VỤ\" theo bộ lọc."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- Một phiếu yêu cầu lập được nhiều phiếu hạch toán; duyệt cả hai thì bút toán ghi 2 lần.\n"
     "- Nút Duyệt / Không duyệt ở màn Chi tiết: Duyệt có thể lấy nhầm dòng chi phí của phiếu yêu cầu khác; "
     "Không duyệt luôn thất bại.\n"
     "- Lưu rồi vào Sửa bấm Lưu & Duyệt thì hợp đồng không cập nhật ngày bàn giao, hạn thanh toán.\n"
     "- Phiếu yêu cầu đã bị Không duyệt vẫn duyệt được phiếu hạch toán Đang tạo của nó.\n"
     "- Bộ lọc Người duyệt không có tác dụng; cột Ngày duyệt hiện dạng năm-tháng-ngày."),
]


ROLE_TCS = [
    ("00", "Không có quyền xem chỉ thấy phiếu mình lập", "P0",
     "NV-A không có quyền xem hạch toán dịch vụ, đã lập HT-1; KT-1 lập HT-2 (Đã duyệt)",
     "1. Đăng nhập NV-A\n"
     "2. " + MENU,
     "Tài khoản: NV-A",
     "- Chỉ có HT-1, không có HT-2"),

    ("01", "Quyền theo công ty thấy phiếu công ty mình", "P0",
     "KT-2 thuộc TPE có quyền \"Xem hạch toán dịch vụ theo công ty\"; HT-2 (Đã duyệt) do KT-1 (TPE) lập, "
     "HT-5 (Đã duyệt) do người TPC lập",
     "1. Đăng nhập KT-2, mở màn từ menu",
     "—",
     "- Có HT-2, không có HT-5"),

    ("02", "Quyền theo tổng công ty thấy mọi công ty", "P0",
     "KT-3 có quyền \"Xem hạch toán dịch vụ theo tổng công ty\"; HT-2 của TPE, HT-5 của TPC",
     "1. Đăng nhập KT-3, mở màn từ menu",
     "—",
     "- Có cả HT-2 và HT-5"),

    ("03", "Quyền theo phòng ban thấy phiếu người cùng phòng", "P1",
     "KT-4 phòng Kế toán có quyền \"Xem hạch toán dịch vụ theo phòng ban\"; HT-2 do KT-1 cùng phòng lập, HT-6 "
     "do người phòng khác lập",
     "1. Đăng nhập KT-4, mở màn từ menu",
     "—",
     "- Có HT-2, không có HT-6"),

    ("04", "Phiếu Đang tạo của người khác không hiện", "P0",
     "KT-1 lưu HT-3 (Đang tạo); KT-3 có quyền theo tổng công ty",
     "1. Đăng nhập KT-3, mở màn",
     "—",
     "- Không có HT-3"),

    ("05", "Mở Chi tiết phiếu Đang tạo của người khác qua đường dẫn", "P1",
     "HT-3 Đang tạo của KT-1; KT-3 có quyền theo tổng công ty, có đường dẫn Chi tiết HT-3",
     "1. Đăng nhập KT-3, dán đường dẫn",
     "—",
     "- Ra trang không tìm thấy"),

    ("06", "Không có quyền hạch toán thì không có nút ở phiếu yêu cầu", "P0",
     "NV-B xem được YC-1 (Chờ duyệt) nhưng không có quyền \"Hạch toán yêu cầu làm dịch vụ\"",
     "1. Đăng nhập NV-B, mở Chi tiết YC-1",
     "—",
     "- Không có nút \"Hạch toán dịch vụ\", không có \"Không duyệt\""),

    ("07", "Gọi thẳng chức năng lưu khi không có quyền hạch toán", "P1",
     "NV-B không có quyền \"Hạch toán yêu cầu làm dịch vụ\"; YC-1 Chờ duyệt",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng lưu phiếu hạch toán cho YC-1 với trạng thái Đã duyệt",
     "—",
     "- Mong đợi: bị chặn\n"
     "- Lưu ý: theo code hiện tại phiếu được tạo Đã duyệt, bút toán được ghi, YC-1 thành Đã hạch toán - ghi "
     "Failed"),

    ("08", "Người khác không sửa được phiếu Đang tạo", "P0",
     "HT-3 Đang tạo của KT-1; KT-5 có quyền hạch toán, có đường dẫn Sửa HT-3",
     "1. Đăng nhập KT-5, dán đường dẫn Sửa HT-3",
     "—",
     "- Ra trang không tìm thấy"),

    ("09", "Super Admin xem được mọi phiếu nhưng không sửa phiếu người khác", "P2",
     "SA là Super Admin; HT-3 Đang tạo của KT-1",
     "1. Đăng nhập SA, mở đường dẫn Chi tiết HT-3\n"
     "2. Mở đường dẫn Sửa HT-3",
     "—",
     "- Bước 1: mở được Chi tiết\n"
     "- Bước 2: ra trang không tìm thấy"),
]
