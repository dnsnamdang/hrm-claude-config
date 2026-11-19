# -*- coding: utf-8 -*-
"""Section VIII, IX, X, XI - in & Excel, rang buoc, co lap & dong thoi, luong dau - cuoi."""
from tc_data_role import MENU, MENU_PXK, PKK, GIA, KKT, KT1, TAO, LUU_DUYET

SEC_VIII = [
    ("001", "In từng phiếu", "P0",
     "PXH-2 Đã hạch toán từ PXK-1, PKK-1, kho K1, H1 KKT-A 3, H2 KKT-A 1",
     "1. Mở Hành động > In của PXH-2",
     "—",
     "- Mở bản in ngang: Số phiếu, Ngày lập, Phiếu xuất kho PXK-1, Phiếu kiểm kê PKK-1, Kho K1, Thủ kho "
     "TK-1, Ghi chú\n"
     "- Bảng: STT, Tên hàng, Model, Mã hàng, ĐVT, SL xuất, Đơn giá vốn, Thành tiền vốn, Kho kế toán, Số "
     "lượng\n"
     "- H1: 3, 100,000, 300,000, KKT-A 3"),

    ("002", "Bản in có tên Người lập", "P1",
     "PXH-2 do KT-1 lập",
     "1. In PXH-2, xem chỗ ký Người lập",
     "—",
     "- Mong đợi: có tên KT-1\n"
     "- Lưu ý: theo code hiện tại để trống - ghi Failed"),

    ("003", "In phiếu Đang tạo", "P2",
     "PXH-3 Đang tạo",
     "1. In PXH-3",
     "—",
     "- Mở được bản in; Đơn giá vốn, Thành tiền vốn bằng 0"),

    ("004", "In danh sách theo bộ lọc", "P0",
     "Danh sách có 3 phiếu Đã hạch toán và 1 phiếu Đang tạo của mình",
     "1. Lọc Trạng thái Đã hạch toán\n"
     "2. Bấm In",
     "—",
     "- Bản in có 3 phiếu với cột: STT, Số phiếu, Phiếu xuất kho, Phiếu kiểm kê, Người lập, Ngày lập, Trạng "
     "thái\n"
     "- Có ngày tháng năm hiện tại"),

    ("005", "Xuất Excel danh sách theo bộ lọc", "P0",
     "Danh sách có 3 phiếu Đã hạch toán",
     "1. Lọc Trạng thái Đã hạch toán\n"
     "2. Bấm Xuất excel",
     "—",
     "- Tải file danh_sach_phieu_xuat_hang_dieu_chinh_kiem_ke.xlsx\n"
     "- Có tiêu đề \"Danh sách phiếu xuất hàng điều chỉnh kiểm kê\" và 3 phiếu"),

    ("006", "In danh sách không có cột Kho", "P2",
     "Có phiếu kho K1 và K2",
     "1. Bấm In danh sách",
     "—",
     "- Mong đợi: có cột Kho như trên màn\n"
     "- Lưu ý: theo code hiện tại không có cột Kho - ghi Failed nếu nghiệp vụ yêu cầu"),

    ("007", "In danh sách tôn trọng quyền xem", "P1",
     "KT-2 có quyền theo công ty TPE; có PXH-2 (TPE), PXH-5 (TPC)",
     "1. KT-2 bấm In danh sách",
     "—",
     "- Chỉ có PXH-2"),

    ("008", "Bản in khi ĐVT khác ĐVT nhỏ nhất", "P2",
     "Phiếu H3 1 Thùng (hệ số 12) đã hạch toán, bình quân 10.000 / Cái",
     "1. In phiếu",
     "—",
     "- Mong đợi: Thành tiền vốn 120,000\n"
     "- Lưu ý: theo code hiện tại in 10,000 - ghi Failed"),
]


SEC_IX = [
    ("001", "Nhân viên bắt buộc", "P0",
     "Đang ở form lập từ PXK-1, đã chọn kho kế toán",
     "1. Bỏ trống Nhân viên, bấm Lưu",
     "—",
     "- Báo \"Tạo thất bại!\", lỗi dưới ô Nhân viên; không tạo phiếu"),

    ("002", "Đơn giá xuất bỏ trống được coi là 0", "P2",
     "Đang ở form lập từ PXK-1",
     "1. Xóa trắng Đơn giá xuất H1, bấm Lưu",
     "—",
     "- Lưu thành công, Đơn giá xuất H1 = 0, Thành tiền xuất 0"),

    ("003", "Đơn giá xuất gõ chữ", "P2",
     "Đang ở form lập từ PXK-1",
     "1. Gõ \"abc\" vào Đơn giá xuất H1",
     "Đơn giá: abc",
     "- Ô không nhận chữ hoặc về 0; không lỗi trang"),

    ("004", "File đính kèm sai định dạng", "P1",
     "Đang ở form lập từ PXK-1",
     "1. Thêm file bang-ke.xlsx, bấm Lưu",
     "File: bang-ke.xlsx",
     "- Báo \"Tạo thất bại!\", ô file bị đánh dấu lỗi"),

    ("005", "Sửa phiếu không còn file nào thì phải đính kèm", "P2",
     "PXH-7 Đang tạo lập từ phiếu xuất kho không có file, lúc lập không thêm file",
     "1. Mở Sửa PXH-7, bấm Lưu",
     "—",
     "- Báo \"Sửa thất bại!\", lỗi dưới File đính kèm"),

    ("006", "Đơn giá xuất âm khi Sửa", "P2",
     "PXH-3 Đang tạo",
     "1. Dùng công cụ kiểm thử API gọi chức năng sửa PXH-3 với Đơn giá xuất H1 = -50000",
     "—",
     "- Mong đợi: bị chặn như khi lập\n"
     "- Lưu ý: theo code hiện tại Sửa lưu được giá âm - ghi Failed"),

    ("007", "Gọi thẳng chức năng lưu với SL lớn hơn số thiếu", "P1",
     PKK + "; " + KKT + "; " + KT1,
     "1. KT-1 dùng công cụ kiểm thử API gọi chức năng lưu với PXK-1, H1 SL 8, KKT-A 8, Lưu và duyệt",
     "—",
     "- Mong đợi: bị chặn vì khác SL của PXK-1 (3)\n"
     "- Lưu ý: theo code hiện tại lưu được, tồn kế toán H1 KKT-A còn 2 - ghi Failed"),

    ("008", "Gọi thẳng chức năng lưu với kho kế toán của kho khác", "P1",
     PKK + "; KKT-C thuộc kho K2 có H1 = 20; " + KT1,
     "1. KT-1 dùng công cụ kiểm thử API gọi chức năng lưu với PXK-1, H1 chọn KKT-C",
     "—",
     "- Mong đợi: bị chặn\n"
     "- Lưu ý: theo code hiện tại lưu được, tồn kế toán KKT-C bị trừ - ghi Failed"),

    ("009", "Đường dẫn Xóa không xóa được phiếu", "P2",
     "PXH-3 Đang tạo do KT-1 lập",
     "1. KT-1 dán đường dẫn Xóa của PXH-3",
     "—",
     "- PXH-3 vẫn còn trên danh sách"),
]


SEC_X = [
    ("001", "Hai tab cùng lập từ một phiếu xuất kho", "P0",
     PKK + "; " + KKT + "; " + KT1,
     "1. KT-1 mở form lập từ PXK-1 ở tab A và tab B\n"
     "2. Tab A: " + LUU_DUYET + "\n"
     "3. Tab B: " + LUU_DUYET,
     "—",
     "- Mong đợi: tab B bị chặn, chỉ có 1 phiếu\n"
     "- Lưu ý: theo code hiện tại ra 2 phiếu Đã hạch toán, tồn kế toán KKT-A H1 còn 4, H2 còn 3 - ghi "
     "Failed"),

    ("002", "Hai phiếu cùng lúc tranh tồn kế toán cuối cùng", "P1",
     "Tồn kế toán H2 ở KKT-A còn 1; PXH-8 và PXH-9 Đang tạo (khác phiếu kiểm kê), mỗi phiếu H2 KKT-A 1",
     "1. Hai kế toán mở Sửa PXH-8 và PXH-9, bấm \"Lưu và duyệt\" cùng lúc",
     "—",
     "- Mong đợi: chỉ 1 phiếu thành công, phiếu kia báo vượt số lượng được xuất\n"
     "- Lưu ý: nếu cả hai thành công và tồn kế toán H2 KKT-A thành -1 thì ghi Failed"),

    ("003", "Bấm Lưu và duyệt 2 lần liên tiếp", "P1",
     "Đang ở form lập từ PXK-1, đã chọn đủ",
     "1. Bấm nhanh \"Lưu và duyệt\" 2 lần",
     "—",
     "- Nút bị khóa sau lần bấm đầu, chỉ tạo 1 phiếu"),

    ("004", "Người khác không thấy phiếu Đang tạo", "P0",
     "KT-1 vừa Lưu PXH-3 Đang tạo; KT-2 có quyền theo công ty",
     "1. KT-2 mở màn từ menu, lọc Trạng thái Đang tạo",
     "—",
     "- Không có PXH-3"),

    ("005", "Công ty của phiếu theo thủ kho lập phiếu xuất kho", "P0",
     "Thủ kho TK-5 thuộc TPC lập PXK-5 (kho K5); KT-1 thuộc TPE có quyền Kế toán kho",
     "1. KT-1 lập phiếu xuất hàng từ PXK-5, Lưu và duyệt\n"
     "2. KT-2 (theo công ty TPE) và KT-6 (theo công ty TPC) mở danh sách",
     "—",
     "- KT-6 thấy phiếu (công ty TPC)\n"
     "- KT-2 không thấy\n"
     "- KT-1 vẫn thấy vì là người lập"),

    ("006", "Phiếu xuất kho đã Đang hạch toán thì không lập thêm từ màn", "P0",
     "KT-1 đã Lưu PXH-3 từ PXK-1 (PXK-1 Đang hạch toán); KT-2 có quyền Kế toán kho",
     "1. KT-2 " + MENU_PXK + ", mở Hành động của PXK-1",
     "—",
     "- Không có \"Tạo phiếu xuất hàng\""),

    ("007", "Đường dẫn In, Chi tiết của phiếu đã bị người khác sửa", "P2",
     "KT-1 mở Chi tiết PXH-3 ở tab A; sau đó ở tab B Lưu và duyệt PXH-3",
     "1. Tải lại tab A",
     "—",
     "- PXH-3 hiện Đã hạch toán, có Đơn giá vốn"),
]


SEC_XI = [
    ("001", "Luồng đầy đủ: kiểm kê thiếu đến hạch toán", "P0",
     PKK + "; " + GIA + "; " + KKT + "; " + KT1,
     "1. KT-1 " + MENU_PXK + ", bấm \"Tạo phiếu xuất hàng\" của PXK-1\n"
     "2. Chọn Nhân viên NV-K, KKT-A cho cả 2 dòng, bấm Lưu\n"
     "3. Mở Sửa phiếu vừa lập, đổi H1 thành KKT-A 1, KKT-B 2, bấm \"Lưu và duyệt\"\n"
     "4. Xem trạng thái phiếu, PXK-1, PKK-1, tồn kế toán\n"
     "5. Mở Chi tiết, In phiếu",
     "—",
     "- Sau bước 2: phiếu Đang tạo, PXK-1 Đang hạch toán, tồn kế toán chưa đổi\n"
     "- Sau bước 3: phiếu Đã hạch toán, PXK-1 Đã hạch toán, PKK-1 Hoàn thành\n"
     "- Tồn kế toán: H1 KKT-A 9, KKT-B 0; H2 KKT-A 4\n"
     "- Giá vốn H1 300.000, H2 300.000; Chi tiết và bản in khớp số liệu"),

    ("002", "Luồng Lưu và duyệt ngay khi lập", "P0",
     PKK + "; " + GIA + "; " + KKT + "; " + KT1,
     "1. KT-1 lập phiếu từ PXK-1, chọn Nhân viên NV-K\n"
     "2. " + LUU_DUYET + "\n"
     "3. Mở danh sách, mở Chi tiết phiếu",
     "—",
     "- Phiếu Đã hạch toán, chỉ có In trong Hành động\n"
     "- Tồn kế toán KKT-A: H1 7, H2 4\n"
     "- PXK-1 Đã hạch toán, không còn nút Tạo phiếu xuất hàng"),

    ("003", "Phiếu kiểm kê vừa thừa vừa thiếu hoàn thành sau cả hai phiếu", "P0",
     "PKK-2 có H4 thừa 4 (đã có Phiếu nhập kho điều chỉnh kiểm kê Chờ duyệt) và H1 thiếu 3 (đã có PXK-4 "
     "Chờ duyệt)",
     "1. KT-1 lập phiếu xuất hàng từ PXK-4, Lưu và duyệt; xem PKK-2\n"
     "2. KT-1 lập Phiếu nhập hàng điều chỉnh kiểm kê cho hàng thừa, Lưu và duyệt; xem PKK-2",
     "—",
     "- Sau bước 1: PKK-2 Đang xử lý\n"
     "- Sau bước 2: PKK-2 Hoàn thành"),

    ("004", "Tồn kế toán không đủ thì phải xử lý trước khi hạch toán", "P1",
     PKK + "; tồn kế toán H2 ở KKT-A, KKT-B đều 0; " + KT1,
     "1. KT-1 lập phiếu từ PXK-1, chọn KKT-A, bấm \"Lưu và duyệt\"\n"
     "2. Bấm Lưu\n"
     "3. Sau khi có phiếu nhập hàng H2 vào KKT-A 2 cái, mở Sửa phiếu, bấm \"Lưu và duyệt\"",
     "—",
     "- Bước 1: báo vượt số lượng được xuất, không tạo phiếu\n"
     "- Bước 2: phiếu Đang tạo\n"
     "- Bước 3: phiếu Đã hạch toán, tồn kế toán H2 KKT-A còn 1"),

    ("005", "Người xem theo công ty thấy phiếu sau hạch toán", "P1",
     "KT-1 vừa Lưu và duyệt phiếu từ PXK-1 (TPE); KT-2 có quyền xem theo công ty TPE",
     "1. KT-2 mở màn từ menu, bấm Số phiếu",
     "—",
     "- KT-2 thấy phiếu, mở Chi tiết được, không có nút Sửa"),
]
