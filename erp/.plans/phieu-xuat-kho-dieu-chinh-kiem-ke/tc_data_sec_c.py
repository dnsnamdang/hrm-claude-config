# -*- coding: utf-8 -*-
"""Section IX, X, XI - rang buoc nhap lieu, co lap & dong thoi, luong dau - cuoi."""
from tc_data_role import MENU, MENU_CHO_DUYET, PKK, TON_KT, TK1, KT1

SEC_IX = [
    ("001", "Bỏ trống Ghi chú", "P0",
     "Đang ở form tạo từ PKK-1, đã thêm 1 file PDF",
     "1. Để trống Ghi chú, bấm Gửi duyệt",
     "—",
     "- Báo \"Tạo thất bại!\", dưới ô Ghi chú có thông báo bắt buộc nhập\n"
     "- Không tạo phiếu"),

    ("002", "Không đính kèm file khi tạo", "P0",
     "Đang ở form tạo từ PKK-1, đã nhập Ghi chú",
     "1. Không thêm file, bấm Lưu",
     "—",
     "- Báo \"Tạo thất bại!\", dưới khu File đính kèm có thông báo bắt buộc\n"
     "- Không tạo phiếu"),

    ("003", "Thêm ô file nhưng không chọn file", "P1",
     "Đang ở form tạo, đã nhập Ghi chú, đã chọn 1 file PDF",
     "1. Bấm dấu cộng thêm ô file thứ 2, không chọn file\n"
     "2. Bấm Lưu",
     "—",
     "- Báo \"Tạo thất bại!\", ô file thứ 2 viền đỏ\n"
     "- Xóa ô thứ 2 bằng dấu x rồi Lưu thì thành công"),

    ("004", "File không đúng định dạng", "P1",
     "Đang ở form tạo, đã nhập Ghi chú",
     "1. Thêm file \"bien_ban.docx\" (chọn Tất cả tệp ở hộp chọn file)\n"
     "2. Bấm Lưu",
     "File: bien_ban.docx",
     "- Báo \"Tạo thất bại!\", ô file viền đỏ, không tạo phiếu"),

    ("005", "Hộp chọn file chỉ gợi ý PDF", "P2",
     "Đang ở form tạo",
     "1. Bấm dấu cộng, bấm vào ô file",
     "—",
     "- Hộp chọn file chỉ lọc sẵn file PDF\n"
     "- Nhãn khu ghi \"File đính kèm (PDF)\""),

    ("006", "File ảnh JPG", "P2",
     "Đang ở form tạo, đã nhập Ghi chú",
     "1. Chọn Tất cả tệp, thêm file \"anh_ke.jpg\", bấm Lưu",
     "File: anh_ke.jpg",
     "- Lưu thành công (hệ thống nhận PDF, PNG, JPG, JPEG)"),

    ("007", "Không có dòng hàng", "P0",
     "PKK-4 kiểm kê K1, K2; K2 không thiếu hàng",
     "1. Mở form từ PKK-4, chọn Kho K2, thêm file, nhập Ghi chú\n"
     "2. Bấm Gửi duyệt",
     "—",
     "- Báo \"Tạo thất bại!\", dưới bảng Chi tiết có thông báo bắt buộc\n"
     "- Không tạo phiếu"),

    ("008", "Không sửa được SL xuất và Đơn giá", "P0",
     "Đang ở form tạo từ PKK-1",
     "1. Bấm vào ô SL xuất và Đơn giá bán của H1",
     "—",
     "- SL xuất chỉ hiển thị, không có ô nhập\n"
     "- Đơn giá bán bị khóa"),

    ("009", "Gọi thẳng chức năng lưu với SL xuất bằng 0", "P1",
     "PKK-1 chưa có phiếu xuất",
     "1. Dùng công cụ kiểm thử API gọi chức năng lưu với H1 SL xuất 0",
     "—",
     "- Báo \"Tạo thất bại!\", không tạo phiếu"),

    ("010", "Gọi thẳng chức năng lưu với SL xuất lớn hơn số thiếu", "P2",
     "PKK-1: H1 thiếu 5; tồn kế toán H1 = 20",
     "1. Dùng công cụ kiểm thử API gọi chức năng lưu với H1 SL xuất 12",
     "—",
     "- Mong đợi: bị chặn vì vượt số thiếu của kiểm kê\n"
     "- Lưu ý: theo code hiện tại tạo được phiếu xuất 12 - ghi Failed"),
]


SEC_X = [
    ("001", "Hai tab cùng lập phiếu từ một phiếu kiểm kê", "P1",
     PKK + "\n" + TON_KT,
     "1. TK-1 mở 2 tab, cả 2 bấm \"Tạo phiếu xuất kho điều chuyển\" từ PKK-1\n"
     "2. Tab 1 Gửi duyệt, sau đó tab 2 Gửi duyệt",
     "—",
     "- Mong đợi: tab 2 bị chặn vì PKK-1 đã có phiếu xuất\n"
     "- Lưu ý: theo code hiện tại tạo được 2 phiếu, tồn H1 tại P1 bị trừ 2 lần (còn 10) - ghi Failed"),

    ("002", "Thủ kho công ty khác lập phiếu", "P1",
     "TK-5 thuộc TPC có quyền xử lý kiểm kê; PKK-1 do TK-1 (TPE) lập",
     "1. TK-5 lập phiếu xuất từ PKK-1, Gửi duyệt\n"
     "2. KT-2 (quyền xem theo công ty, thuộc TPE) mở màn Tất cả",
     "—",
     "- KT-2 thấy phiếu (phiếu thuộc công ty của người lập phiếu kiểm kê là TPE)"),

    ("003", "Kế toán kho công ty khác tạo phiếu xuất hàng", "P1",
     "KT-6 thuộc TPC có quyền Kế toán kho; PX-2 của TPE Chờ duyệt",
     "1. KT-6 mở màn Chờ duyệt",
     "—",
     "- Mong đợi: không có PX-2\n"
     "- Lưu ý: theo code hiện tại có PX-2 kèm nút \"Tạo phiếu xuất hàng\" - ghi Failed"),

    ("004", "Phiếu xuất hàng tạo trùng từ một phiếu", "P2",
     KT1 + "; PX-2 đã Đang hạch toán",
     "1. KT-1 dán lại đường dẫn \"Tạo phiếu xuất hàng\" của PX-2",
     "—",
     "- Không lấy được dữ liệu PX-2 (báo không có quyền)"),

    ("005", "Tồn vị trí đã bị xuất trước khi gửi duyệt", "P1",
     "PX-3 Đang tạo có H1 P1 L01 = 5; sau đó một phiếu xuất kho khác đã xuất hết H1 tại P1 lô L01",
     "1. TK-1 mở Sửa PX-3 hoặc tạo lại phiếu tương tự, bấm Gửi duyệt",
     "—",
     "- Mong đợi: báo tồn vị trí không đủ\n"
     "- Lưu ý: ghi Failed nếu gửi được và tồn vị trí âm"),

    ("006", "Thông báo cần duyệt mở đúng phiếu", "P1",
     KT1 + "; TK-1 vừa Gửi duyệt PX-2",
     "1. KT-1 bấm thông báo \"Bạn có 1 phiếu xuất kho điều chỉnh cần duyệt\"",
     "—",
     "- Mở Chi tiết PX-2"),
]


SEC_XI = [
    ("001", "Luồng chuẩn: kiểm kê thiếu đến hạch toán xong", "P0",
     TK1 + "; " + KT1 + "\n" + PKK + "\n" + TON_KT,
     "1. TK-1 mở Chi tiết PKK-1, bấm \"Tạo phiếu xuất kho điều chuyển\", thêm file, nhập Ghi chú, bấm Gửi duyệt\n"
     "2. KT-1 mở " + "màn Chờ duyệt, bấm \"Tạo phiếu xuất hàng\" của phiếu vừa tạo, chọn kho kế toán, hoàn thành\n"
     "3. Xem phiếu xuất kho, tồn vị trí, tồn kế toán và PKK-1",
     "—",
     "- Phiếu xuất kho Đã hạch toán\n"
     "- Tồn vị trí: H1 P1 L01 còn 15, H2 P2 L02 còn 6\n"
     "- Tồn kế toán TPE: H1 còn 15, H2 còn 6\n"
     "- Nếu PKK-1 đã xử lý xong cả nhập, điều chuyển: PKK-1 Hoàn thành; nếu chưa: Đang xử lý"),

    ("002", "Luồng Lưu nháp rồi gửi duyệt sau", "P0",
     TK1 + "\n" + PKK + "\n" + TON_KT,
     "1. TK-1 lập phiếu từ PKK-1, bấm Lưu\n"
     "2. Mở Sửa, đổi Ghi chú, bấm Gửi duyệt\n"
     "3. Kế toán kho tạo phiếu xuất hàng và hoàn thành",
     "—",
     "- Phiếu qua Đang tạo, Chờ duyệt, Đã hạch toán\n"
     "- Mong đợi: tồn vị trí H1 P1 L01 còn 15\n"
     "- Lưu ý: theo code hiện tại tồn vị trí vẫn 20 vì bước 2 không trừ - ghi Failed"),

    ("003", "Luồng bị chặn do tồn kế toán rồi xử lý giữ hàng", "P1",
     PKK + "\nTồn kế toán TPE H1 = 5, trong đó 2 cái đang giữ hàng",
     "1. TK-1 lập phiếu từ PKK-1, bấm Gửi duyệt\n"
     "2. Bỏ giữ hàng 2 cái H1, quay lại form bấm Gửi duyệt lần nữa",
     "—",
     "- Bước 1: báo tồn kế toán không đủ (SL được xuất: 3, SL xuất: 5)\n"
     "- Bước 2: tạo phiếu thành công, Chờ duyệt"),

    ("004", "Phiếu kiểm kê có cả thừa, thiếu, lệch vị trí", "P1",
     PKK,
     "1. Lập phiếu xuất kho từ PKK-1, Gửi duyệt\n"
     "2. Mở lại Chi tiết PKK-1",
     "—",
     "- Phiếu xuất chỉ có H1, H2\n"
     "- PKK-1 không còn nút lập phiếu xuất; vẫn còn nút lập phiếu điều chuyển vị trí (H3) và phiếu nhập kho "
     "điều chuyển (H4)"),

    ("005", "Đối chiếu Thẻ kho sau khi gửi duyệt", "P1",
     "Vừa Gửi duyệt phiếu có H1 = 5 tại K1",
     "1. Mở Thẻ kho, chọn kho K1, hàng H1, hôm nay",
     "—",
     "- Có dòng xuất 5 gắn số phiếu xuất kho điều chỉnh kiểm kê, tồn cuối giảm 5"),
]
