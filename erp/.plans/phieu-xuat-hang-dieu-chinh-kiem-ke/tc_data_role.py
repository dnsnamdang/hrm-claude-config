# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Phieu xuat hang dieu chinh kiem ke'."""

MENU = ("Mở menu Kế toán > \"Hàng hoá - Dịch vụ - Vận chuyển\" > nhóm \"Xuất hàng\" > bấm \"Phiếu xuất hàng "
        "điều chỉnh kiểm kê\"")
MENU_PXK = "Mở menu Kho > bấm \"Phiếu xuất kho điều chỉnh kiểm kê\""

# Du lieu mau dung chung
PKK = ("Phiếu kiểm kê PKK-1 của TPE tại kho K1. Kết quả kiểm kê có hàng THIẾU:\n"
       "- H1 (ĐVT Cái): vị trí P1 thiếu 3\n"
       "- H2 (ĐVT Cái): vị trí P2 thiếu 1\n"
       "Thủ kho TK-1 (TPE) đã lập Phiếu xuất kho điều chỉnh kiểm kê PXK-1 từ PKK-1, gửi duyệt (Chờ duyệt), "
       "đính kèm file bb-thieu.pdf; tồn kho vật lý đã trừ H1 = 3, H2 = 1")
GIA = "Đơn giá bán trên PXK-1: H1 = 150.000, H2 = 500.000"
KKT = ("Kho K1 gắn 2 kho kế toán của TPE: KKT-A, KKT-B. Tồn kế toán (không có hàng giữ, hàng chờ lấy):\n"
       "- H1: KKT-A 10 (giá trị 1.000.000, bình quân 100.000), KKT-B 2 (bình quân 100.000)\n"
       "- H2: KKT-A 5 (giá trị 1.500.000, bình quân 300.000), KKT-B 0")
KT1 = "KT-1 thuộc TPE có quyền \"Kế toán kho\""
TAO = ("KT-1 " + MENU_PXK + ", mở nút Hành động của PXK-1, bấm \"Tạo phiếu xuất hàng\"")
LUU_DUYET = "Chọn kho kế toán KKT-A cho dòng H1 và H2, bấm \"Lưu và duyệt\""

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Phiếu xuất hàng điều chỉnh kiểm kê: sau khi kiểm kê phát hiện hàng THIẾU, thủ kho lập Phiếu xuất kho "
     "điều chỉnh kiểm kê (đã trừ tồn kho vật lý). Kế toán kho lập phiếu này từ phiếu xuất kho đó để trừ "
     "hàng khỏi TỒN KẾ TOÁN theo từng kho kế toán, tính giá vốn và ghi nhận hạch toán.\n"
     "Người dùng làm được: lập phiếu (Lưu hoặc Lưu và duyệt), sửa phiếu Đang tạo của mình, xem, in từng "
     "phiếu, in / xuất Excel danh sách."),

    ("2. Đối tượng được tính / hiển thị",
     "- Dòng chi tiết lấy nguyên từ Phiếu xuất kho điều chỉnh kiểm kê: Tên hàng, Model, Mã hàng, ĐVT, SL "
     "xuất (không sửa được).\n"
     "- Đơn giá xuất điền sẵn = đơn giá bán trên phiếu xuất kho, sửa được; Thành tiền xuất = SL xuất nhân "
     "Đơn giá xuất.\n"
     "- Mỗi dòng chia SL vào một hoặc nhiều kho kế toán gắn với kho của phiếu, cùng công ty; cột \"SL được "
     "xuất\" cho biết tồn kế toán còn xuất được của kho kế toán đã chọn.\n"
     "- Sau khi hạch toán, màn Chi tiết hiện thêm Đơn giá vốn và Thành tiền vốn.\n"
     "- Danh sách (menu Kế toán) hiện theo quyền xem; phiếu Đang tạo chỉ người lập thấy."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Hàng THỪA sau kiểm kê (thuộc Phiếu nhập hàng điều chỉnh kiểm kê).\n"
     "- Phiếu Đang tạo của người khác.\n"
     "- Không có nút Xóa, không có Duyệt / Không duyệt riêng: \"Lưu và duyệt\" là hạch toán luôn.\n"
     "- Tồn kho vật lý KHÔNG đổi ở bước này (đã trừ ở phiếu xuất kho)."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Khối tìm kiếm có ô Từ ngày / Đến ngày nhưng theo code hiện tại không áp dụng vào kết quả. Cột Ngày "
     "lập là ngày lập phiếu xuất hàng. Danh sách sắp phiếu mới lập lên đầu."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Phiếu: Số phiếu (PXHĐCKK-00001 tăng dần), Phiếu xuất kho (liên kết), Phiếu kiểm kê (liên kết), Kho, "
     "Thủ kho, Nhân viên (bắt buộc), Ghi chú, File đính kèm (gồm file của phiếu xuất kho và file thêm).\n"
     "Chi tiết: STT, Tên hàng, Model, Mã hàng, ĐVT, SL xuất, Đơn giá xuất, Thành tiền xuất, (Đơn giá vốn, "
     "Thành tiền vốn ở màn Chi tiết), Kho kế toán, SL được xuất (khi lập / sửa), Số lượng.\n"
     "Trạng thái: Đang tạo (đỏ), Đã hạch toán (xanh).\n"
     "Danh sách: STT, Số phiếu, Phiếu xuất kho, Phiếu kiểm kê, Kho, Người lập, Ngày lập, Trạng thái, Hành "
     "động (Sửa, In)."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Tổng Số lượng các kho kế toán của một dòng phải bằng SL xuất của dòng.\n"
     "- Một kho kế toán chỉ chọn 1 lần trong một dòng.\n"
     "- Tổng số xuất của cùng một mặt hàng, cùng kho kế toán (cộng mọi dòng) không được vượt SL được xuất.\n"
     "- Lưu và duyệt: tồn kế toán từng kho kế toán trừ Số lượng nhân hệ số ĐVT; Đơn giá vốn = giá trị tồn "
     "kế toán giảm đi chia số lượng xuất.\n"
     "Với dữ liệu mẫu, xuất cả từ KKT-A: H1 3 x 100.000 = 300.000; H2 1 x 300.000 = 300.000; tổng giá vốn "
     "600.000. Thành tiền xuất: H1 450.000, H2 500.000."),

    ("7. Phân quyền cấp",
     "- Lập phiếu: nút \"Tạo phiếu xuất hàng\" trên danh sách Phiếu xuất kho điều chỉnh kiểm kê, cần quyền "
     "\"Kế toán kho\" và phiếu xuất kho Chờ duyệt.\n"
     "- Danh sách, Chi tiết, In: \"Xem phiếu xuất hàng điều chỉnh kiểm kê - theo tổng công ty\" thấy mọi "
     "công ty; \"... - theo công ty\" thấy công ty mình và phiếu mình lập; không có quyền nào thì chỉ thấy "
     "phiếu mình lập.\n"
     "- Công ty của phiếu = công ty của thủ kho lập phiếu xuất kho.\n"
     "- Sửa: chỉ người lập, phiếu Đang tạo.\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- Lưu: phiếu Đang tạo, phiếu xuất kho chuyển Đang hạch toán, chưa trừ tồn kế toán.\n"
     "- Lưu và duyệt: phiếu Đã hạch toán, phiếu xuất kho chuyển Đã hạch toán, trừ tồn kế toán, tính giá "
     "vốn, ghi bút toán.\n"
     "- Cả hai trường hợp: phiếu kiểm kê chuyển Hoàn thành nếu không còn việc xử lý, ngược lại Đang xử lý.\n"
     "- Giá vốn của phiếu Đã hạch toán được Biên bản xử lý hàng thừa, thiếu sau kiểm kê lấy làm giá vốn."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- Lưu và duyệt KHÔNG sinh bút toán nào (số tiền bút toán luôn bằng 0).\n"
     "- ĐVT khác ĐVT nhỏ nhất: Thành tiền vốn trên màn Chi tiết và bản in bị chia nhỏ theo hệ số.\n"
     "- Lọc Kho, Từ ngày / Đến ngày không có tác dụng.\n"
     "- Mở 2 tab cùng lập từ 1 phiếu xuất kho ra 2 phiếu, tồn kế toán trừ 2 lần.\n"
     "- Mỗi lần Lưu ở màn Sửa, số đã xử lý của kết quả kiểm kê bị cộng thêm lần nữa.\n"
     "- Bản in không có tên Người lập.\n"
     "- Đơn giá xuất chỉ để hiển thị, không ảnh hưởng giá vốn hay hạch toán."),
]


ROLE_TCS = [
    ("00", "Không có quyền xem chỉ thấy phiếu mình lập", "P0",
     "NV-A không có 2 quyền xem phiếu xuất hàng điều chỉnh kiểm kê, đã lập PXH-1; KT-1 lập PXH-2 (Đã hạch "
     "toán)",
     "1. Đăng nhập NV-A\n"
     "2. " + MENU,
     "Tài khoản: NV-A",
     "- Chỉ có PXH-1, không có PXH-2"),

    ("01", "Quyền theo công ty thấy phiếu công ty mình", "P0",
     "KT-2 thuộc TPE có quyền \"Xem phiếu xuất hàng điều chỉnh kiểm kê - theo công ty\"; PXH-2 (Đã hạch "
     "toán) của TPE, PXH-5 (Đã hạch toán) của TPC",
     "1. Đăng nhập KT-2, mở màn từ menu",
     "—",
     "- Có PXH-2, không có PXH-5"),

    ("02", "Quyền theo tổng công ty thấy mọi công ty", "P0",
     "KT-3 thuộc TPE có quyền \"Xem phiếu xuất hàng điều chỉnh kiểm kê - theo tổng công ty\"; PXH-2 của TPE, "
     "PXH-5 của TPC",
     "1. Đăng nhập KT-3, mở màn từ menu",
     "—",
     "- Có cả PXH-2 và PXH-5"),

    ("03", "Quyền theo tổng công ty mở được Chi tiết và In phiếu công ty khác", "P0",
     "KT-3 thuộc TPE chỉ có quyền theo tổng công ty; PXH-5 của TPC",
     "1. KT-3 bấm Số phiếu PXH-5\n"
     "2. Mở Hành động > In của PXH-5",
     "—",
     "- Mở được Chi tiết và bản in PXH-5"),

    ("04", "Phiếu Đang tạo của người khác không hiện", "P0",
     "KT-3 có quyền theo tổng công ty; KT-1 có PXH-3 Đang tạo",
     "1. Đăng nhập KT-3, mở màn từ menu",
     "—",
     "- Không có PXH-3"),

    ("05", "Chỉ người lập thấy nút Sửa", "P0",
     "PXH-3 Đang tạo do KT-1 lập; KT-2 có quyền Kế toán kho",
     "1. KT-1 mở nút Hành động của PXH-3\n"
     "2. KT-2 dán đường dẫn Sửa của PXH-3",
     "—",
     "- Bước 1: có Sửa, In\n"
     "- Bước 2: ra trang không tìm thấy"),

    ("06", "Chỉ Kế toán kho thấy nút Tạo phiếu xuất hàng", "P0",
     PKK + "; TK-1 không có quyền Kế toán kho; " + KT1,
     "1. TK-1 " + MENU_PXK + ", mở nút Hành động của PXK-1\n"
     "2. KT-1 làm tương tự",
     "—",
     "- TK-1: không có \"Tạo phiếu xuất hàng\"\n"
     "- KT-1: có \"Tạo phiếu xuất hàng\""),

    ("07", "Không có quyền xem mở Chi tiết phiếu người khác", "P1",
     "NV-B thuộc TPC không có quyền xem; PXH-2 của TPE",
     "1. Đăng nhập NV-B, dán đường dẫn Chi tiết PXH-2\n"
     "2. Dán đường dẫn In PXH-2",
     "—",
     "- Cả hai ra trang không tìm thấy"),

    ("08", "Quyền theo công ty không mở được phiếu công ty khác", "P1",
     "KT-2 thuộc TPE có quyền xem theo công ty; PXH-5 của TPC",
     "1. KT-2 dán đường dẫn Chi tiết PXH-5",
     "—",
     "- Ra trang không tìm thấy"),

    ("09", "Gọi thẳng chức năng lưu phiếu khi không có quyền Kế toán kho", "P1",
     PKK + "; " + KKT + "; NV-A không có quyền Kế toán kho",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng lưu phiếu xuất hàng với PXK-1, đủ chi tiết, chọn "
     "Lưu và duyệt",
     "—",
     "- Mong đợi: bị chặn\n"
     "- Lưu ý: theo code hiện tại tạo được phiếu Đã hạch toán, tồn kế toán bị trừ - ghi Failed"),

    ("10", "Sửa phiếu người khác qua công cụ kiểm thử", "P1",
     "PXH-3 Đang tạo do KT-1 lập",
     "1. KT-2 dùng công cụ kiểm thử API gọi thẳng chức năng sửa PXH-3",
     "—",
     "- Báo \"Bạn không có quyền sửa phiếu này\", PXH-3 không đổi"),

    ("11", "Xuất Excel danh sách bỏ điều kiện loại danh sách", "P1",
     "NV-A không có quyền xem; có PXH-2 của TPE, PXH-5 của TPC, PXH-3 Đang tạo của KT-1",
     "1. NV-A dán đường dẫn Xuất Excel danh sách nhưng bỏ phần chọn loại danh sách",
     "—",
     "- Mong đợi: file chỉ có phiếu NV-A lập\n"
     "- Lưu ý: theo code hiện tại file có mọi phiếu của mọi công ty, kể cả PXH-3 Đang tạo - ghi Failed"),
]
