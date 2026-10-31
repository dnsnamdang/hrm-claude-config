# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Phieu nhap hang dieu chinh kiem ke'."""

MENU = ("Mở menu Kế toán > \"Hàng hoá - Dịch vụ - Vận chuyển\" > nhóm \"Nhập hàng\" > bấm \"Phiếu nhập hàng "
        "điều chỉnh kiểm kê\"")
MENU_PNK = "Mở menu Kho > bấm \"Phiếu nhập kho điều chỉnh kiểm kê\""

# Du lieu mau dung chung
PKK = ("Phiếu kiểm kê PKK-1 của TPE tại kho K1. Kết quả kiểm kê có hàng THỪA:\n"
       "- H4 (ĐVT Cái): vị trí P2 thừa 4\n"
       "- H5 (ĐVT Cái): vị trí P3 thừa 2\n"
       "Thủ kho TK-1 (TPE) đã lập Phiếu nhập kho điều chỉnh kiểm kê PNK-1 từ PKK-1, gửi duyệt (Chờ duyệt), "
       "đính kèm file bb-thua.pdf; tồn kho vật lý đã cộng H4 = 4, H5 = 2")
GIA = "Giá nhập gần nhất trên Phiếu nhập hàng: H4 = 120.000, H5 = 300.000"
KKT = "Kho K1 gắn 2 kho kế toán của TPE: KKT-A, KKT-B; tồn kế toán H4, H5 tại KKT-A, KKT-B đều bằng 0"
KT1 = "KT-1 thuộc TPE có quyền \"Kế toán kho\""
TAO = ("KT-1 " + MENU_PNK + ", mở nút Hành động của PNK-1, bấm \"Tạo phiếu nhập hàng\"")
LUU_DUYET = "Chọn kho kế toán KKT-A cho dòng H4 và H5, bấm \"Lưu và duyệt\""

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Phiếu nhập hàng điều chỉnh kiểm kê: sau khi kiểm kê phát hiện hàng THỪA, thủ kho lập Phiếu nhập kho "
     "điều chỉnh kiểm kê (đã cộng tồn kho vật lý). Kế toán kho lập phiếu này từ phiếu nhập kho đó để nhập "
     "hàng vào TỒN KẾ TOÁN theo từng kho kế toán, ghi đơn giá nhập và sinh bút toán.\n"
     "Người dùng làm được: lập phiếu (Lưu hoặc Lưu và duyệt), sửa phiếu Đang tạo của mình, xem, in từng "
     "phiếu, in / xuất Excel danh sách."),

    ("2. Đối tượng được tính / hiển thị",
     "- Dòng chi tiết lấy nguyên từ Phiếu nhập kho điều chỉnh kiểm kê: Tên hàng, Model, Mã hàng, ĐVT, SL "
     "nhập (không sửa được).\n"
     "- Đơn giá nhập điền sẵn = đơn giá khác 0 của lần nhập hàng gần nhất của mặt hàng (không có thì 0), "
     "sửa được; Thành tiền nhập = SL nhập nhân Đơn giá nhập.\n"
     "- Mỗi dòng chia SL vào một hoặc nhiều kho kế toán gắn với kho của phiếu, cùng công ty.\n"
     "- Danh sách (menu Kế toán) hiện theo quyền xem; phiếu Đang tạo chỉ người lập thấy."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Hàng THIẾU sau kiểm kê (thuộc Phiếu xuất hàng điều chỉnh kiểm kê).\n"
     "- Phiếu Đang tạo của người khác.\n"
     "- Không có nút Xóa, không có Duyệt / Không duyệt riêng: \"Lưu và duyệt\" là hạch toán luôn.\n"
     "- Danh sách không có cột Người duyệt, Ngày duyệt."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Khối tìm kiếm có ô Từ ngày / Đến ngày nhưng theo code hiện tại không áp dụng vào kết quả. Cột Ngày "
     "lập là ngày lập phiếu nhập hàng. Danh sách sắp phiếu mới lập lên đầu."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Phiếu: Số phiếu (PNHĐCKK-00001 tăng dần), Phiếu nhập kho (liên kết), Phiếu kiểm kê (liên kết), Kho, "
     "Thủ kho, Nhân viên (bắt buộc), Ghi chú, File đính kèm (gồm file của phiếu nhập kho và file thêm).\n"
     "Chi tiết: STT, Tên hàng, Model, Mã hàng, ĐVT, SL nhập, Đơn giá nhập, Thành tiền nhập, Kho kế toán, Số "
     "lượng.\n"
     "Trạng thái: Đang tạo (đỏ), Đã hạch toán (xanh).\n"
     "Danh sách: STT, Số phiếu, Phiếu nhập kho, Phiếu kiểm kê, Kho, Người lập, Ngày lập, Trạng thái, Hành "
     "động (Sửa, In)."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Tổng Số lượng các kho kế toán của một dòng phải bằng SL nhập của dòng.\n"
     "- Một kho kế toán chỉ chọn 1 lần trong một dòng.\n"
     "- Lưu và duyệt: tồn kế toán của từng kho kế toán cộng thêm Số lượng nhân hệ số ĐVT; tồn kho vật lý "
     "KHÔNG đổi (đã cộng ở phiếu nhập kho).\n"
     "- Bút toán: Nợ 1561 từng mặt hàng = Đơn giá nhân SL; Có 3381 tổng tiền, đối tượng là Nhân viên.\n"
     "Với dữ liệu mẫu: H4 4 x 120.000 = 480.000; H5 2 x 300.000 = 600.000; tổng 1.080.000."),

    ("7. Phân quyền cấp",
     "- Lập phiếu: nút \"Tạo phiếu nhập hàng\" trên danh sách Phiếu nhập kho điều chỉnh kiểm kê, cần quyền "
     "\"Kế toán kho\" và phiếu nhập kho Chờ duyệt.\n"
     "- Danh sách: \"Xem phiếu nhập hàng điều chỉnh kiểm kê - theo tổng công ty\" thấy mọi công ty; \"... - "
     "theo công ty\" thấy công ty mình và phiếu mình lập; không có quyền nào thì chỉ thấy phiếu mình lập.\n"
     "- Công ty của phiếu = công ty của thủ kho lập phiếu nhập kho.\n"
     "- Sửa: chỉ người lập, phiếu Đang tạo.\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- Lưu: phiếu Đang tạo, phiếu nhập kho chuyển Đang hạch toán, chưa cộng tồn kế toán, chưa có bút toán.\n"
     "- Lưu và duyệt: phiếu Đã hạch toán, phiếu nhập kho chuyển Đã hạch toán, cộng tồn kế toán, sinh bút "
     "toán.\n"
     "- Cả hai trường hợp: phiếu kiểm kê chuyển Hoàn thành nếu không còn việc xử lý, ngược lại Đang xử lý."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- Lọc Kho, mã / tên hàng hóa, Từ ngày / Đến ngày, Công ty, Phòng ban không có tác dụng.\n"
     "- Người có quyền xem theo tổng công ty thấy phiếu công ty khác ở danh sách nhưng bấm vào ra trang "
     "không tìm thấy.\n"
     "- Mở 2 tab cùng lập từ 1 phiếu nhập kho ra 2 phiếu, tồn kế toán cộng 2 lần.\n"
     "- ĐVT khác ĐVT nhỏ nhất: Thành tiền trên màn khác số tiền bút toán.\n"
     "- Mỗi lần Lưu ở màn Sửa, số đã xử lý của kết quả kiểm kê bị cộng thêm lần nữa.\n"
     "- Thông báo khi lệch số kho kế toán ghi \"xuất kho\" thay vì nhập kho."),
]


ROLE_TCS = [
    ("00", "Không có quyền xem chỉ thấy phiếu mình lập", "P0",
     "NV-A không có 2 quyền xem phiếu nhập hàng điều chỉnh kiểm kê, đã lập PNH-1; KT-1 lập PNH-2 (Đã hạch "
     "toán)",
     "1. Đăng nhập NV-A\n"
     "2. " + MENU,
     "Tài khoản: NV-A",
     "- Chỉ có PNH-1, không có PNH-2"),

    ("01", "Quyền theo công ty thấy phiếu công ty mình", "P0",
     "KT-2 thuộc TPE có quyền \"Xem phiếu nhập hàng điều chỉnh kiểm kê - theo công ty\"; PNH-2 (Đã hạch "
     "toán) của TPE, PNH-5 (Đã hạch toán) của TPC",
     "1. Đăng nhập KT-2, mở màn từ menu",
     "—",
     "- Có PNH-2, không có PNH-5"),

    ("02", "Quyền theo tổng công ty thấy mọi công ty", "P0",
     "KT-3 thuộc TPE có quyền \"Xem phiếu nhập hàng điều chỉnh kiểm kê - theo tổng công ty\"; PNH-2 của TPE, "
     "PNH-5 của TPC",
     "1. Đăng nhập KT-3, mở màn từ menu",
     "—",
     "- Có cả PNH-2 và PNH-5"),

    ("03", "Phiếu Đang tạo của người khác không hiện", "P0",
     "KT-3 có quyền theo tổng công ty; KT-1 có PNH-3 Đang tạo",
     "1. Đăng nhập KT-3, mở màn từ menu",
     "—",
     "- Không có PNH-3"),

    ("04", "Chỉ người lập thấy nút Sửa", "P0",
     "PNH-3 Đang tạo do KT-1 lập; KT-2 có quyền Kế toán kho",
     "1. KT-1 mở nút Hành động của PNH-3\n"
     "2. KT-2 dán đường dẫn Sửa của PNH-3",
     "—",
     "- Bước 1: có Sửa, In\n"
     "- Bước 2: ra trang không tìm thấy"),

    ("05", "Chỉ Kế toán kho thấy nút Tạo phiếu nhập hàng", "P0",
     PKK + "; TK-1 không có quyền Kế toán kho; " + KT1,
     "1. TK-1 " + MENU_PNK + ", mở nút Hành động của PNK-1\n"
     "2. KT-1 làm tương tự",
     "—",
     "- TK-1: không có \"Tạo phiếu nhập hàng\"\n"
     "- KT-1: có \"Tạo phiếu nhập hàng\""),

    ("06", "Quyền theo tổng công ty mở Chi tiết phiếu công ty khác", "P0",
     "KT-3 thuộc TPE chỉ có quyền \"Xem phiếu nhập hàng điều chỉnh kiểm kê - theo tổng công ty\"; PNH-5 của "
     "TPC hiện trên danh sách của KT-3",
     "1. KT-3 bấm Số phiếu PNH-5\n"
     "2. Mở Hành động > In của PNH-5",
     "—",
     "- Mong đợi: mở được Chi tiết và bản in\n"
     "- Lưu ý: theo code hiện tại cả hai ra trang không tìm thấy - ghi Failed"),

    ("07", "Không có quyền xem mở Chi tiết phiếu người khác", "P1",
     "NV-B thuộc TPC không có quyền xem; PNH-2 của TPE",
     "1. Đăng nhập NV-B, dán đường dẫn Chi tiết PNH-2\n"
     "2. Dán đường dẫn In PNH-2",
     "—",
     "- Cả hai ra trang không tìm thấy"),

    ("08", "Gọi thẳng chức năng lưu phiếu khi không có quyền Kế toán kho", "P1",
     PKK + "; NV-A không có quyền Kế toán kho",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng lưu phiếu nhập hàng với PNK-1, đủ chi tiết, chọn "
     "Lưu và duyệt",
     "—",
     "- Mong đợi: bị chặn\n"
     "- Lưu ý: theo code hiện tại tạo được phiếu Đã hạch toán, tồn kế toán tăng - ghi Failed"),

    ("09", "Sửa phiếu người khác qua công cụ kiểm thử", "P1",
     "PNH-3 Đang tạo do KT-1 lập",
     "1. KT-2 dùng công cụ kiểm thử API gọi thẳng chức năng sửa PNH-3",
     "—",
     "- Báo \"Bạn không có quyền sửa phiếu này\", PNH-3 không đổi"),

    ("10", "Xuất Excel danh sách bỏ điều kiện loại danh sách", "P1",
     "NV-A không có quyền xem; có PNH-2 của TPE, PNH-5 của TPC, PNH-3 Đang tạo của KT-1",
     "1. NV-A dán đường dẫn Xuất Excel danh sách nhưng bỏ phần chọn loại danh sách",
     "—",
     "- Mong đợi: file chỉ có phiếu NV-A lập\n"
     "- Lưu ý: theo code hiện tại file có mọi phiếu của mọi công ty, kể cả PNH-3 Đang tạo - ghi Failed"),
]
