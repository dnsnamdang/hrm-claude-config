# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Phieu xuat kho dieu chinh kiem ke'."""

MENU = "Mở menu Kho > cột \"Xuất kho\" > bấm \"Phiếu xuất kho điều chỉnh kiểm kê\""
MENU_CHO_DUYET = ("Mở menu Chờ duyệt > \"Hàng hóa – dịch vụ – vận chuyển\" > nhóm \"Xuất hàng\" > bấm "
                  "\"Phiếu xuất kho điều chỉnh kiểm kê chờ duyệt\"")

# Du lieu mau dung chung
PKK = ("Phiếu kiểm kê PKK-1 của TPE tại kho K1, trạng thái Chờ xử lý, do TK-1 lập. Kết quả kiểm kê:\n"
       "- H1 (ĐVT Cái, giá cơ sở 150.000): vị trí P1 lô L01 hệ thống 20, thực tế 15 (thiếu 5)\n"
       "- H2 (ĐVT Cái, giá cơ sở 250.000): vị trí P2 lô L02 hệ thống 8, thực tế 6 (thiếu 2)\n"
       "- H3: vị trí P1 thiếu 3, vị trí P3 thừa 3 (tổng lệch bằng 0)\n"
       "- H4: vị trí P2 thừa 4")
TON_KT = "Tồn kế toán TPE tại kho kế toán gắn kho K1: H1 = 20, H2 = 8, không có hàng đang giữ chỗ / giữ hàng"
TK1 = "TK-1 thuộc TPE có quyền \"Xử lý phiếu kiểm kê hàng hóa\""
KT1 = "KT-1 thuộc TPE có quyền \"Kế toán kho\""
TAO = ("TK-1 mở Chi tiết PKK-1, bấm \"Tạo phiếu xuất kho điều chuyển\", thêm 1 file PDF, nhập Ghi chú "
       "\"Xuất thiếu sau kiểm kê\"")

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Phiếu xuất kho điều chỉnh kiểm kê: sau khi kiểm kê hàng hóa phát hiện hàng THIẾU so với hệ thống, "
     "thủ kho lập phiếu này để trừ tồn kho vật lý đúng vị trí, đúng lô. Phiếu sinh ra từ phiếu kiểm kê, "
     "mỗi phiếu kiểm kê chỉ có 1 phiếu xuất kho điều chỉnh.\n"
     "Người dùng làm được: lập phiếu từ phiếu kiểm kê (Lưu hoặc Gửi duyệt), sửa phiếu Đang tạo của mình, "
     "xem, in từng phiếu, in / xuất Excel danh sách. Kế toán kho \"duyệt\" bằng cách tạo Phiếu xuất hàng "
     "điều chỉnh kiểm kê từ phiếu Chờ duyệt."),

    ("2. Đối tượng được tính / hiển thị",
     "- Dòng chi tiết lấy từ kết quả kiểm kê của phiếu kiểm kê tại kho đã chọn: chỉ vị trí bị THIẾU, chưa "
     "xử lý xong, và mặt hàng có tổng lệch của mọi vị trí khác 0.\n"
     "- SL xuất = số thiếu trừ số đã xử lý; không sửa được trên phiếu.\n"
     "- Đơn giá bán = giá cơ sở của hàng theo công ty của phiếu kiểm kê; Thành tiền bán = SL xuất nhân "
     "Đơn giá bán.\n"
     "- Màn \"Tất cả\" (menu Kho): theo quyền xem; màn \"Chờ duyệt\": phiếu Chờ duyệt cho người có quyền "
     "Kế toán kho."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Vị trí thừa hàng (thuộc Phiếu nhập kho điều chỉnh kiểm kê).\n"
     "- Mặt hàng thiếu chỗ này thừa chỗ kia với tổng lệch bằng 0 (thuộc Phiếu điều chuyển vị trí).\n"
     "- Kết quả kiểm kê đã xử lý xong.\n"
     "- Phiếu Đang tạo của người khác (không hiện ở màn Tất cả).\n"
     "- Không có chức năng Xóa phiếu, không có nút Không duyệt."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Khối tìm kiếm có ô Từ ngày / Đến ngày nhưng theo code hiện tại không áp dụng vào kết quả. Cột \"Ngày "
     "kiểm kê\" trên danh sách thực chất là ngày lập phiếu xuất. Danh sách sắp phiếu mới lập lên đầu."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Phiếu: Số phiếu (PXKĐCKK-00001 tăng dần), Phiếu kiểm kho (liên kết), Kho, Ghi chú (bắt buộc), File "
     "đính kèm (bắt buộc ít nhất 1), Trạng thái.\n"
     "Chi tiết: STT, Tên hàng hóa, Model, Mã hàng hóa, ĐVT, Vị trí, Lô, SL xuất, Đơn giá bán, Thành tiền bán.\n"
     "Trạng thái: Đang tạo, Chờ duyệt, Đang hạch toán, Đã hạch toán.\n"
     "Danh sách: STT, Số phiếu, Ngày kiểm kê, Kho, Trạng thái, Người lập, Hành động (Sửa, Tạo phiếu xuất "
     "hàng, In)."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Kiểm tra tồn kế toán gom TỔNG SL các dòng cùng hàng, cùng công ty của lô, cùng ĐVT rồi so 1 lần với "
     "SL được xuất (đã trừ hàng giữ chỗ / giữ hàng).\n"
     "- Trừ tồn vật lý theo từng dòng: tồn kho, tồn của công ty, tồn vị trí và tồn lô tại vị trí; số trừ = "
     "SL xuất nhân hệ số ĐVT.\n"
     "Với dữ liệu mẫu PKK-1: phiếu có 2 dòng H1 P1 L01 = 5 (750.000), H2 P2 L02 = 2 (500.000); không có H3, H4."),

    ("7. Phân quyền cấp",
     "- Lập phiếu: nút trên Chi tiết phiếu kiểm kê cần quyền \"Xử lý phiếu kiểm kê hàng hóa\" và phiếu kiểm "
     "kê Chờ xử lý / Đang xử lý.\n"
     "- Màn Tất cả: \"Xem phiếu xuất kho điều chỉnh kiểm kê - theo tổng công ty\" thấy mọi công ty; \"... - "
     "theo công ty\" thấy công ty mình; không có quyền nào thì chỉ thấy phiếu mình lập.\n"
     "- Sửa: chỉ người lập, phiếu Đang tạo.\n"
     "- Tạo phiếu xuất hàng: quyền \"Kế toán kho\", phiếu Chờ duyệt.\n"
     "- Xem Chi tiết / In từng phiếu: hiện không kiểm tra quyền.\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- Gửi duyệt ngay khi tạo: trừ tồn kho vật lý luôn, gửi thông báo \"Bạn có 1 phiếu xuất kho điều chỉnh "
     "cần duyệt\" tới người có quyền Kế toán kho; phiếu kiểm kê chuyển Đang xử lý.\n"
     "- Tồn kế toán chỉ bị trừ khi Phiếu xuất hàng điều chỉnh kiểm kê hoàn thành; khi đó phiếu này chuyển "
     "Đã hạch toán (Phiếu xuất hàng còn Đang tạo thì phiếu này là Đang hạch toán).\n"
     "- Ô đếm trên trang chủ: số phiếu Chờ duyệt của công ty người xem."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- Lưu (Đang tạo) rồi vào Sửa bấm Gửi duyệt thì KHÔNG trừ tồn kho vật lý.\n"
     "- Lọc theo Kho, Từ ngày / Đến ngày, Công ty, Phòng ban không có tác dụng.\n"
     "- In / Xuất Excel danh sách bị lỗi khi danh sách có phiếu chưa có người duyệt.\n"
     "- Màn Chờ duyệt hiện phiếu của mọi công ty, trong khi ô đếm trang chủ chỉ đếm công ty mình.\n"
     "- Ở màn Sửa đổi Kho thì không tải lại được hàng, phiếu lưu kho mới với hàng của kho cũ.\n"
     "- Bản in phiếu ghi cột \"SL nhập\" thay vì SL xuất."),
]


ROLE_TCS = [
    ("00", "Không có quyền xem chỉ thấy phiếu mình lập", "P0",
     "NV-A không có 2 quyền xem phiếu xuất kho điều chỉnh kiểm kê; NV-A lập PX-1, TK-1 lập PX-2 (Chờ duyệt)",
     "1. Đăng nhập NV-A\n"
     "2. " + MENU,
     "Tài khoản: NV-A",
     "- Chỉ có PX-1, không có PX-2"),

    ("01", "Quyền theo công ty thấy phiếu của công ty mình", "P0",
     "KT-2 thuộc TPE có quyền \"Xem phiếu xuất kho điều chỉnh kiểm kê - theo công ty\"; PX-2 (Chờ duyệt) của "
     "TPE, PX-5 (Chờ duyệt) của TPC",
     "1. Đăng nhập KT-2, mở màn từ menu",
     "—",
     "- Có PX-2, không có PX-5"),

    ("02", "Quyền theo tổng công ty thấy mọi công ty", "P0",
     "KT-3 có quyền \"Xem phiếu xuất kho điều chỉnh kiểm kê - theo tổng công ty\"; PX-2 của TPE, PX-5 của TPC",
     "1. Đăng nhập KT-3, mở màn từ menu",
     "—",
     "- Có cả PX-2 và PX-5"),

    ("03", "Phiếu Đang tạo của người khác không hiện", "P0",
     "KT-3 có quyền theo tổng công ty; TK-1 có PX-3 trạng thái Đang tạo",
     "1. Đăng nhập KT-3, mở màn từ menu",
     "—",
     "- Không có PX-3"),

    ("04", "Chỉ người lập thấy nút Sửa", "P0",
     "PX-3 Đang tạo do TK-1 lập; KT-3 có quyền theo tổng công ty",
     "1. Đăng nhập TK-1, mở nút Hành động của PX-3\n"
     "2. Đăng nhập KT-3, dán đường dẫn Sửa của PX-3",
     "—",
     "- Bước 1: có Sửa, In\n"
     "- Bước 2: ra trang không tìm thấy"),

    ("05", "Chỉ Kế toán kho thấy Tạo phiếu xuất hàng", "P0",
     "PX-2 Chờ duyệt; " + KT1 + "; TK-1 không có quyền Kế toán kho",
     "1. TK-1 mở nút Hành động của PX-2\n"
     "2. KT-1 mở nút Hành động của PX-2",
     "—",
     "- TK-1: chỉ có In\n"
     "- KT-1: có \"Tạo phiếu xuất hàng\" và In"),

    ("06", "Không có quyền xử lý kiểm kê thì không thấy nút lập phiếu", "P0",
     "NV-A không có quyền \"Xử lý phiếu kiểm kê hàng hóa\"; PKK-1 Chờ xử lý có hàng thiếu",
     "1. NV-A mở Chi tiết PKK-1",
     "—",
     "- Không có nút \"Tạo phiếu xuất kho điều chuyển\""),

    ("07", "Màn Chờ duyệt của người không có quyền Kế toán kho", "P1",
     "NV-A không có quyền Kế toán kho, đã lập PX-1 Chờ duyệt; PX-2 Chờ duyệt do TK-1 lập",
     "1. NV-A dán đường dẫn màn Chờ duyệt",
     "—",
     "- Chỉ thấy phiếu NV-A lập (PX-1), không có PX-2"),

    ("08", "Xem Chi tiết phiếu công ty khác qua đường dẫn", "P1",
     "NV-B thuộc TPC không có quyền xem; PX-2 của TPE",
     "1. Đăng nhập NV-B, dán đường dẫn Chi tiết PX-2\n"
     "2. Dán đường dẫn In PX-2",
     "—",
     "- Mong đợi: ra trang không tìm thấy\n"
     "- Lưu ý: theo code hiện tại mở được đầy đủ phiếu và bản in - ghi Failed"),

    ("09", "Gọi thẳng chức năng lưu phiếu khi không có quyền xử lý kiểm kê", "P1",
     "NV-A không có quyền \"Xử lý phiếu kiểm kê hàng hóa\"; PKK-2 có hàng thiếu, chưa có phiếu xuất",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng lưu phiếu xuất kho điều chỉnh với PKK-2, đủ chi "
     "tiết, file, ghi chú",
     "—",
     "- Mong đợi: bị chặn\n"
     "- Lưu ý: theo code hiện tại tạo được phiếu - ghi Failed"),

    ("10", "Sửa phiếu người khác qua công cụ kiểm thử", "P1",
     "PX-3 Đang tạo do TK-1 lập; TK-2 cũng có quyền xử lý kiểm kê",
     "1. TK-2 dùng công cụ kiểm thử API gọi thẳng chức năng sửa PX-3",
     "—",
     "- Báo \"Bạn không có quyền sửa phiếu này\", PX-3 không đổi"),
]
