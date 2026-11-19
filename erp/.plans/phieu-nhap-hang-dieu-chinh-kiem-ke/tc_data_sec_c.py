# -*- coding: utf-8 -*-
"""Section VIII, IX, X, XI - in & excel, rang buoc, co lap & dong thoi, luong dau - cuoi."""
from tc_data_role import MENU, MENU_PNK, PKK, GIA, KKT, KT1, TAO, LUU_DUYET

SEC_VIII = [
    ("001", "In từng phiếu", "P0",
     "PNH-2 Đã hạch toán từ PNK-1 (PKK-1), kho K1, Ghi chú \"Nhập thừa sau kiểm kê\"; H4 KKT-A 3, KKT-B 1",
     "1. Mở Hành động > In của PNH-2",
     "—",
     "- Mở bản in khổ ngang: Số phiếu, Ngày lập, Kho K1, Phiếu nhập kho PNK-1, Phiếu kiểm kê PKK-1, Ghi chú\n"
     "- Bảng: Tên hàng, Model, Mã hàng, ĐVT, SL nhập, Đơn giá nhập, Thành tiền nhập, Kho kế toán, Số lượng\n"
     "- H4 chiếm 2 dòng kho kế toán KKT-A 3, KKT-B 1"),

    ("002", "Bản in ghi tên thủ kho", "P1",
     "PNH-2 lập từ PNK-1 do TK-1 lập",
     "1. In PNH-2, xem phần ký",
     "—",
     "- Thủ kho: TK-1\n"
     "- Ngày tháng năm là ngày in"),

    ("003", "In danh sách theo bộ lọc", "P0",
     "KT-1 có 3 phiếu Đã hạch toán, 2 phiếu Đang tạo",
     "1. Lọc Trạng thái Đã hạch toán\n"
     "2. Bấm In",
     "—",
     "- Mở tab bản in danh sách đúng 3 phiếu\n"
     "- Cột: STT, Số phiếu, Phiếu nhập kho, Phiếu kiểm kê, Người lập, Ngày lập, Trạng thái"),

    ("004", "Xuất Excel danh sách", "P0",
     "KT-1 có 5 phiếu",
     "1. Bấm Xuất excel",
     "—",
     "- Tải file danh_sach_phieu_nhap_hang_dieu_chinh_kiem_ke.xlsx\n"
     "- Tiêu đề \"Danh sách phiếu nhập hàng điều chỉnh kiểm kê\", đủ 5 phiếu, cùng cột như bản in danh sách"),

    ("005", "Xuất Excel theo bộ lọc Mã phiếu", "P1",
     "Có PNHĐCKK-00007 và PNHĐCKK-00008",
     "1. Lọc Mã phiếu 00007, bấm Xuất excel",
     "—",
     "- File chỉ có PNHĐCKK-00007"),

    ("006", "In phiếu Đang tạo", "P2",
     "PNH-3 Đang tạo do KT-1 lập",
     "1. KT-1 mở Hành động > In của PNH-3",
     "—",
     "- In được, số liệu theo lần Lưu gần nhất"),
]


SEC_IX = [
    ("001", "Đơn giá âm", "P1",
     "Đang ở form lập từ PNK-1",
     "1. Nhập Đơn giá H4 = -120000\n"
     "2. Chọn kho kế toán, Nhân viên, bấm Lưu và duyệt",
     "Đơn giá H4: -120000",
     "- Mong đợi: báo lỗi đơn giá, không lưu\n"
     "- Lưu ý: theo code hiện tại lưu được, bút toán H4 âm 480.000 - ghi Failed"),

    ("002", "Đơn giá bằng 0", "P2",
     "Đang ở form lập từ PNK-1",
     "1. Xóa trắng Đơn giá H4, bấm Lưu và duyệt",
     "—",
     "- Theo code hiện tại lưu được với đơn giá 0, Nợ 1561 H4 = 0\n"
     "- Nghiệp vụ xác nhận có cho phép không"),

    ("003", "Đơn giá có dấu phân cách", "P1",
     "Đang ở form lập từ PNK-1",
     "1. Nhập Đơn giá H4 \"135,500\"",
     "Đơn giá: 135,500",
     "- Thành tiền H4 = 542,000; sau khi lưu đơn giá là 135.500"),

    ("004", "File đính kèm sai định dạng", "P1",
     "Đang ở form lập từ PNK-1",
     "1. Thêm file bien-ban.docx (đổi bộ lọc chọn file sang mọi loại)\n"
     "2. Bấm Lưu",
     "File: bien-ban.docx",
     "- Báo \"Tạo thất bại!\", ô file báo lỗi; không tạo phiếu"),

    ("005", "Gọi thẳng chức năng lưu với SL nhập khác phiếu nhập kho", "P1",
     PKK + "; " + KT1,
     "1. KT-1 dùng công cụ kiểm thử API gọi thẳng chức năng lưu phiếu từ PNK-1, gửi H4 SL 10 (KKT-A 10), "
     "Lưu và duyệt",
     "—",
     "- Mong đợi: bị chặn vì SL khác phiếu nhập kho (4)\n"
     "- Lưu ý: theo code hiện tại lưu được, tồn kế toán H4 tăng 10 trong khi tồn vật lý chỉ tăng 4 - ghi "
     "Failed"),

    ("006", "Gọi thẳng chức năng lưu với kho kế toán không thuộc kho K1", "P1",
     PKK + "; KKT-C gắn kho K2",
     "1. KT-1 dùng công cụ kiểm thử API gọi thẳng chức năng lưu phiếu từ PNK-1, H4 chọn KKT-C",
     "—",
     "- Mong đợi: bị chặn\n"
     "- Lưu ý: theo code hiện tại lưu được, tồn kế toán H4 tăng ở KKT-C - ghi Failed"),

    ("007", "Gọi thẳng chức năng lưu không có dòng hàng", "P2",
     KT1,
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng lưu phiếu từ PNK-1 nhưng không gửi dòng hàng",
     "—",
     "- Báo \"Tạo thất bại!\", không tạo phiếu"),
]


SEC_X = [
    ("001", "Hai tab cùng lập từ một phiếu nhập kho", "P0",
     PKK + "; " + KT1,
     "1. KT-1 mở form \"Tạo phiếu nhập hàng\" của PNK-1 ở tab A và tab B\n"
     "2. Tab A: " + LUU_DUYET + "\n"
     "3. Tab B: " + LUU_DUYET,
     "—",
     "- Mong đợi: tab B báo phiếu nhập kho đã được hạch toán, không tạo phiếu\n"
     "- Lưu ý: theo code hiện tại tạo 2 phiếu, tồn kế toán H4 tăng 8, H5 tăng 4 - ghi Failed"),

    ("002", "Gọi thẳng chức năng lưu từ phiếu nhập kho đã Đã hạch toán", "P1",
     "PNK-1 Đã hạch toán (đã có PNH-2)",
     "1. KT-1 dùng công cụ kiểm thử API gọi thẳng chức năng lưu phiếu mới từ PNK-1, Lưu và duyệt",
     "—",
     "- Mong đợi: bị chặn\n"
     "- Lưu ý: theo code hiện tại tạo thêm phiếu, tồn kế toán cộng lần 2 - ghi Failed"),

    ("003", "Gọi thẳng chức năng lưu từ phiếu nhập kho Đang tạo", "P1",
     "PNK-4 Đang tạo (thủ kho chưa gửi duyệt, tồn vật lý chưa cộng)",
     "1. KT-1 dùng công cụ kiểm thử API gọi thẳng chức năng lưu phiếu từ PNK-4, Lưu và duyệt",
     "—",
     "- Mong đợi: bị chặn\n"
     "- Lưu ý: theo code hiện tại tạo được, tồn kế toán tăng dù tồn vật lý chưa tăng - ghi Failed"),

    ("004", "Xóa phiếu qua đường dẫn", "P1",
     "PNH-3 Đang tạo do KT-1 lập từ PNK-1 (PNK-1 Đang hạch toán)",
     "1. KT-1 dán đường dẫn Xóa của PNH-3\n"
     "2. " + MENU_PNK + ", xem PNK-1",
     "—",
     "- Mong đợi: không xóa được (màn không có chức năng Xóa) hoặc xóa xong PNK-1 trở về Chờ duyệt\n"
     "- Lưu ý: theo code hiện tại PNH-3 bị xóa, PNK-1 kẹt ở Đang hạch toán, không lập lại được phiếu nhập "
     "hàng - ghi Failed"),

    ("005", "Bấm Lưu và duyệt liên tiếp", "P1",
     "Đang ở form lập từ PNK-1, đã điền đủ",
     "1. Bấm \"Lưu và duyệt\" 2 lần thật nhanh",
     "—",
     "- Nút bị khóa trong lúc xử lý, chỉ tạo 1 phiếu"),

    ("006", "Công ty của phiếu theo thủ kho lập phiếu nhập kho", "P1",
     "KT-4 thuộc TPC có quyền Kế toán kho; PNK-1 do TK-1 (TPE) lập; KT-2 có quyền xem theo công ty TPE",
     "1. KT-4 lập phiếu từ PNK-1, Lưu và duyệt\n"
     "2. KT-2 mở màn từ menu",
     "—",
     "- KT-2 thấy phiếu KT-4 vừa lập (phiếu thuộc TPE)"),

    ("007", "Phiếu Đang tạo của người khác không mở Chi tiết được", "P1",
     "PNH-3 Đang tạo do KT-1 lập; NV-A không có quyền xem",
     "1. NV-A dán đường dẫn Chi tiết PNH-3",
     "—",
     "- Ra trang không tìm thấy"),
]


SEC_XI = [
    ("001", "Luồng đầy đủ: kiểm kê thừa đến hạch toán", "P0",
     PKK + "; " + GIA + "; " + KKT + "; " + KT1,
     "1. KT-1 " + MENU_PNK + ", bấm \"Tạo phiếu nhập hàng\" của PNK-1\n"
     "2. Chọn Nhân viên NV-K, KKT-A cho cả 2 dòng, bấm Lưu\n"
     "3. Mở Sửa phiếu vừa lập, đổi H4 thành KKT-A 3, KKT-B 1, bấm \"Lưu và duyệt\"\n"
     "4. Xem trạng thái phiếu, PNK-1, tồn kế toán, bút toán\n"
     "5. In phiếu",
     "—",
     "- Sau bước 2: phiếu Đang tạo, PNK-1 Đang hạch toán, tồn kế toán chưa đổi\n"
     "- Sau bước 3: phiếu Đã hạch toán, PNK-1 Đã hạch toán\n"
     "- Tồn kế toán: H4 KKT-A 3, KKT-B 1; H5 KKT-A 2\n"
     "- Bút toán Nợ 1561 H4 480.000, H5 600.000; Có 3381 1.080.000\n"
     "- Bản in khớp số liệu"),

    ("002", "Luồng Lưu và duyệt ngay khi lập", "P0",
     PKK + "; " + GIA + "; " + KKT + "; " + KT1,
     "1. KT-1 lập phiếu từ PNK-1, chọn Nhân viên NV-K\n"
     "2. " + LUU_DUYET + "\n"
     "3. Mở danh sách, mở Chi tiết phiếu",
     "—",
     "- Phiếu Đã hạch toán, chỉ có In trong Hành động\n"
     "- Tồn kế toán KKT-A: H4 4, H5 2\n"
     "- PNK-1 Đã hạch toán, không còn nút Tạo phiếu nhập hàng"),

    ("003", "Phiếu kiểm kê vừa thừa vừa thiếu hoàn thành sau cả hai phiếu", "P0",
     "PKK-2 có H4 thừa 4 (đã có PNK-1 Chờ duyệt) và H1 thiếu 5 (đã có Phiếu xuất kho điều chỉnh kiểm kê "
     "Chờ duyệt)",
     "1. KT-1 lập phiếu nhập hàng từ PNK-1, Lưu và duyệt; xem PKK-2\n"
     "2. KT-1 lập Phiếu xuất hàng điều chỉnh kiểm kê cho hàng thiếu, hoàn thành; xem PKK-2",
     "—",
     "- Sau bước 1: PKK-2 Đang xử lý\n"
     "- Sau bước 2: PKK-2 Hoàn thành"),

    ("004", "Người xem theo công ty thấy phiếu sau hạch toán", "P1",
     "KT-1 vừa Lưu và duyệt phiếu từ PNK-1 (TPE); KT-2 có quyền xem theo công ty TPE",
     "1. KT-2 mở màn từ menu, bấm Số phiếu",
     "—",
     "- KT-2 thấy phiếu, mở Chi tiết được, không có nút Sửa"),
]
