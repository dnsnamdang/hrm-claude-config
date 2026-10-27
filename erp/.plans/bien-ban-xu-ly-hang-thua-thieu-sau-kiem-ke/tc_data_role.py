# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Bien ban xu ly hang thua, thieu sau kiem ke'."""

MENU = ("Mở menu Kế toán > mục \"Kiểm kê\" > cột \"Theo vị trí\" > bấm \"Biên bản xử lý hàng thừa, "
        "thiếu sau kiểm kê\"")

# Du lieu mau dung chung
KK = ("Kho K1 có 2 phiếu kiểm kê theo hàng hóa đã Hoàn thành:\n"
      "- KK-10 ngày kiểm 05/10: hàng H1 thừa 3 (đã nhập điều chỉnh bằng phiếu NDC-1, đơn giá nhập 100.000, "
      "giá bán 150.000, kho kế toán KT01); hàng H2 thiếu 2 (đã xuất điều chỉnh bằng phiếu XDC-1, đơn giá "
      "xuất 250.000, giá bán 300.000, kho kế toán KT01)\n"
      "- KK-11 ngày kiểm 07/10: hàng H3 thiếu 1 (phiếu XDC-2, đơn giá xuất 50.000, giá bán 80.000)")

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Quản lý Biên bản xử lý hàng thừa, thiếu sau kiểm kê: chứng từ kế toán kho lập để quy trách nhiệm "
     "và hạch toán phần hàng thừa / thiếu đã được điều chỉnh kho sau các phiếu Kiểm kê theo hàng hóa.\n"
     "Người lập chọn khoảng ngày kiểm kê và kho vật lý, bấm \"Lấy dữ liệu\" để hệ thống gom mọi dòng "
     "chênh lệch của các phiếu kiểm kê đã Hoàn thành; với từng dòng nhập Lý do, chọn Giá xử lý (giá vốn "
     "/ giá bán), tỷ lệ chi phí nhân viên / công ty và nhân viên chịu.\n"
     "Người có quyền duyệt bấm Duyệt: hệ thống ghi bút toán công nợ nhân viên và thu nhập / chi phí khác.\n"
     "Người dùng làm được: xem danh sách, lọc, tạo (Lưu nháp / Lưu và gửi duyệt), sửa khi còn nháp, "
     "duyệt, in và xuất Excel từng biên bản hoặc cả danh sách."),

    ("2. Đối tượng được tính / hiển thị",
     "Biên bản có 3 trạng thái:\n"
     "- Đang tạo (nhãn đỏ): vừa bấm Lưu, người lập còn sửa được.\n"
     "- Chờ duyệt (nhãn đỏ): đã bấm Lưu và gửi duyệt.\n"
     "- Đã duyệt (nhãn xanh): đã ghi bút toán.\n"
     "Dòng được đưa vào biên bản khi bấm \"Lấy dữ liệu\":\n"
     "- Thuộc phiếu Kiểm kê theo hàng hóa trạng thái Hoàn thành, có kiểm kho vật lý đã chọn.\n"
     "- Ngày kiểm kê của phiếu nằm trong Từ ngày đến Đến ngày (tính trọn hai đầu).\n"
     "- Tổng chênh lệch của hàng trong phiếu khác 0: lớn hơn 0 vào tab Hàng thừa, nhỏ hơn 0 vào tab "
     "Hàng thiếu; SL là trị tuyệt đối.\n"
     "- Đơn giá vốn lấy từ phiếu nhập / xuất kho điều chỉnh kiểm kê đã hoàn thành của hàng đó; Đơn giá "
     "bán lấy từ phiếu kiểm kê."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Hàng chỉ lệch vị trí (tổng chênh lệch bằng 0) không vào biên bản.\n"
     "- Phiếu kiểm kê chưa Hoàn thành (Chờ xử lý, Đang xử lý...) không được lấy.\n"
     "- Bỏ chọn một phiếu ở khung \"Phiếu kiểm kê\" thì các dòng của phiếu đó ẩn khỏi 2 tab và không "
     "được lưu.\n"
     "- Sửa: chỉ khi biên bản Đang tạo VÀ người xem là người lập.\n"
     "- Duyệt: chỉ khi Chờ duyệt VÀ có quyền duyệt biên bản.\n"
     "- Không có nút Xóa, không có Không duyệt.\n"
     "- In, Xuất Excel luôn hiện."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "- Màn danh sách KHÔNG có ô lọc thời gian.\n"
     "- Ô Từ ngày / Đến ngày trên form biên bản lọc theo NGÀY KIỂM KÊ của phiếu kiểm kê, không theo ngày "
     "lập hay ngày hoàn thành phiếu."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Khung \"Thông tin chung\": Từ ngày, Đến ngày, Kho vật lý (bắt buộc), Ghi chú, File đính kèm.\n"
     "Khung \"Phiếu kiểm kê\": danh sách ô chọn theo mã phiếu kiểm kê, mặc định chọn hết.\n"
     "Khung \"Chi tiết\": nút Lấy dữ liệu, 2 tab Hàng thừa / Hàng thiếu, mỗi dòng gồm: Tên hàng, Model, "
     "Mã hàng, Mã kho (kho kế toán), SL, Đơn giá bán, Thành tiền bán, Đơn giá vốn, Thành tiền vốn, Phiếu "
     "xử lý (mã phiếu nhập / xuất điều chỉnh), Lý do, Giá xử lý, % Chi phí nhân viên, % Chi phí công ty, "
     "NV chịu, Chi phí nhân viên, Chi phí công ty.\n"
     "Số biên bản: BBXLKKHH-<5 chữ số>, ví dụ BBXLKKHH-00007 (không có mã công ty)."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Thành tiền bán = Đơn giá bán x SL; Thành tiền vốn = Đơn giá vốn x SL.\n"
     "- Giá xử lý mặc định Giá vốn; % Chi phí nhân viên mặc định 100, % Chi phí công ty = 100 - % nhân viên "
     "(sửa một ô thì ô kia tự đổi); nhập trên 100 tự về 100.\n"
     "- Chi phí nhân viên = Thành tiền (theo Giá xử lý) x % nhân viên; Chi phí công ty = Thành tiền x % công "
     "ty.\n"
     "- Cột Hàng thừa / Hàng thiếu trên lưới = tổng SL các dòng của tab tương ứng.\n"
     "- Bút toán khi duyệt, gộp theo NV chịu:\n"
     "  + Hàng thừa: Nợ 3381 / Có 3341 phần chi phí nhân viên; Nợ 3381 / Có 711 tổng phần chi phí công ty.\n"
     "  + Hàng thiếu: Nợ 3341 / Có 1381 phần chi phí nhân viên; Nợ 811 / Có 1381 phần chi phí công ty.\n"
     "- Hệ thống KHÔNG chặn việc đưa cùng một phiếu kiểm kê vào nhiều biên bản."),

    ("7. Phân quyền cấp",
     "- \"Kế toán kho\" (nhóm Kế toán): mở được màn Tạo mới; không có quyền này bấm Tạo mới ra trang "
     "không tìm thấy.\n"
     "- \"Duyệt biên bản xử lý hàng thừa, thiếu sau kiểm kê\" (nhóm Kiểm kê kho): nhận thông báo khi có "
     "biên bản gửi duyệt, thấy nút Duyệt và sửa được Giá xử lý, %, NV chịu khi duyệt.\n"
     "- \"Xem biên bản xử lý hàng thừa, thiếu sau kiểm kê - theo tổng công ty\" / \"- theo công ty\": có "
     "khai báo nhưng lối vào menu hiện tại KHÔNG dùng tới (luôn chỉ hiện biên bản của chính mình).\n"
     "Xem chi tiết, In, Xuất Excel KHÔNG kiểm tra quyền.\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- Dòng dưới bảng \"Hiển thị a đến b của N\": N là tổng biên bản khớp bộ lọc trong phạm vi lối vào.\n"
     "- Cột Hàng thừa / Hàng thiếu: tổng SL (không phải tiền).\n"
     "- STT đánh liên tục qua các trang."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- Lưu xong, Chi phí công ty được ghi BẰNG Chi phí nhân viên: màn hình vẫn hiện đúng nhưng bản In và "
     "bút toán Nợ 3381 / Có 711, Nợ 811 / Có 1381 sai số.\n"
     "- Lối vào menu chỉ hiện biên bản do mình lập, kể cả với quyền xem tổng công ty; người duyệt chỉ tìm "
     "được biên bản chờ duyệt qua thông báo.\n"
     "- Ô lọc Kho và Người duyệt không có tác dụng.\n"
     "- Một phiếu kiểm kê đưa được vào nhiều biên bản, mỗi biên bản duyệt đều ghi bút toán.\n"
     "- Hàng nhập / xuất điều chỉnh vào từ 2 kho kế toán trở lên làm nút Lấy dữ liệu lỗi.\n"
     "- Tab Hàng thừa không hiện lỗi thiếu NV chịu / % chi phí dưới dòng (chỉ báo \"Tạo thất bại!\").\n"
     "- Bấm mã phiếu xuất điều chỉnh ở cột Phiếu xử lý mở nhầm sang trang phiếu nhập.\n"
     "- Bản In: cột Thành tiền bán in ĐƠN GIÁ bán.\n"
     "- Không có Không duyệt: biên bản Chờ duyệt bị sai không trả lại được.\n"
     "- Người duyệt công ty nào cũng duyệt được; xem / In biên bản công ty khác qua đường dẫn.\n"
     "- Thông báo lỗi kiểm tra dữ liệu hiển thị bằng TIẾNG ANH; sửa hay duyệt lỗi đều báo \"Tạo thất "
     "bại!\"."),
]


ROLE_TCS = [
    ("00", "Không có quyền Kế toán kho thì không mở được màn Tạo mới", "P0",
     "NV-A không có quyền \"Kế toán kho\"",
     "1. Đăng nhập NV-A\n"
     "2. " + MENU + "\n"
     "3. Bấm Tạo mới",
     "Tài khoản: NV-A",
     "- Nút Tạo mới vẫn hiện trên danh sách\n"
     "- Bấm vào ra trang không tìm thấy, không có form biên bản"),

    ("01", "Không có quyền Kế toán kho gọi thẳng chức năng Lưu", "P1",
     "NV-A không có quyền \"Kế toán kho\"; kho K1 có phiếu KK-10 Hoàn thành",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Lưu biên bản với dữ liệu hợp lệ của KK-10",
     "—",
     "- Mong đợi: bị chặn vì không có quyền\n"
     "- Lưu ý: theo code hiện tại biên bản vẫn được tạo - ghi Failed"),

    ("02", "Có quyền Kế toán kho thì lập được biên bản", "P0",
     "KT-1 có quyền \"Kế toán kho\"\n" + KK,
     "1. Đăng nhập KT-1, mở màn từ menu, bấm Tạo mới\n"
     "2. Chọn Từ ngày 01/10, Đến ngày 10/10, Kho vật lý K1, bấm Lấy dữ liệu",
     "Kho vật lý: K1",
     "- Mở form \"Biên bản xử lý hàng sau kiểm kê hàng hóa\"\n"
     "- Khung Phiếu kiểm kê có KK-10, KK-11 đều được chọn\n"
     "- Tab Hàng thừa có H1, tab Hàng thiếu có H2, H3"),

    ("03", "Quyền xem theo tổng công ty vẫn chỉ thấy biên bản của mình", "P1",
     "XEM-1 có quyền \"Xem biên bản xử lý hàng thừa, thiếu sau kiểm kê - theo tổng công ty\"\n"
     "Công ty 1 có 6 biên bản Chờ duyệt / Đã duyệt của người khác; XEM-1 lập 1 biên bản",
     "1. Đăng nhập XEM-1, mở màn từ menu\n"
     "2. Đọc số tổng",
     "—",
     "- Mong đợi: thấy 7 biên bản\n"
     "- Lưu ý: theo code hiện tại chỉ thấy 1 biên bản của mình - ghi Failed"),

    ("04", "Quyền xem theo công ty vẫn chỉ thấy biên bản của mình", "P1",
     "XEM-2 có quyền \"Xem biên bản xử lý hàng thừa, thiếu sau kiểm kê - theo công ty\", thuộc công ty 1\n"
     "Công ty 1 có 6 biên bản đã gửi của người khác; XEM-2 chưa lập biên bản nào",
     "1. Đăng nhập XEM-2, mở màn từ menu",
     "—",
     "- Mong đợi: thấy 6 biên bản công ty 1\n"
     "- Lưu ý: theo code hiện tại bảng trống - ghi Failed"),

    ("05", "Người có quyền duyệt nhận thông báo khi có biên bản gửi duyệt", "P0",
     "KT-1 lập biên bản BB-2; DUYET-1 có quyền \"Duyệt biên bản xử lý hàng thừa, thiếu sau kiểm kê\"",
     "1. KT-1 bấm Lưu và gửi duyệt ở BB-2\n"
     "2. Đăng nhập DUYET-1, mở chuông thông báo, bấm thông báo mới",
     "—",
     "- Có thông báo \"Bạn có 1 biên bản xử lý hàng thừa thiếu, sau kiểm kê cần duyệt\"\n"
     "- Bấm vào mở màn Chi tiết BB-2, cuối trang có nút Duyệt và Quay lại"),

    ("06", "Người duyệt không tìm được biên bản chờ duyệt ở danh sách", "P1",
     "BB-2 Chờ duyệt do KT-1 lập; DUYET-1 có quyền duyệt, chưa lập biên bản nào",
     "1. Đăng nhập DUYET-1, mở màn từ menu\n"
     "2. Lọc Trạng thái \"Chờ duyệt\"",
     "—",
     "- Mong đợi: thấy BB-2 để duyệt\n"
     "- Lưu ý: theo code hiện tại bảng trống, chỉ mở được BB-2 qua thông báo - ghi Failed"),

    ("07", "Không có quyền duyệt thì không duyệt được", "P0",
     "NV-B không có quyền duyệt; BB-2 Chờ duyệt",
     "1. Đăng nhập NV-B, dán đường dẫn Chi tiết BB-2\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Duyệt BB-2",
     "—",
     "- Bước 1: không có nút Duyệt, mọi ô bị khóa\n"
     "- Bước 2: báo \"Không có quyền\", BB-2 vẫn Chờ duyệt, không có bút toán"),

    ("08", "Chỉ người lập sửa được biên bản Đang tạo", "P0",
     "BB-1 Đang tạo do KT-1 lập; KT-2 cũng có quyền Kế toán kho",
     "1. KT-1 bấm bánh răng ở BB-1\n"
     "2. KT-2 dán đường dẫn Sửa BB-1\n"
     "3. KT-2 dùng công cụ kiểm thử API gọi thẳng chức năng Lưu sửa BB-1",
     "—",
     "- Bước 1: menu có Sửa, In, Xuất Excel\n"
     "- Bước 2: trang không tìm thấy\n"
     "- Bước 3: báo \"Bạn không có quyền sửa phiếu này\", BB-1 giữ nguyên"),

    ("09", "Biên bản Chờ duyệt không sửa được kể cả người lập", "P0",
     "BB-2 Chờ duyệt do KT-1 lập",
     "1. KT-1 bấm bánh răng ở BB-2\n"
     "2. KT-1 dán đường dẫn Sửa BB-2",
     "—",
     "- Bước 1: menu chỉ có In, Xuất Excel\n"
     "- Bước 2: trang không tìm thấy"),

    ("10", "Gọi thẳng chức năng Xóa biên bản", "P1",
     "BB-1 Đang tạo và BB-2 Chờ duyệt cùng do KT-1 lập; KT-2 là người khác",
     "1. KT-2 gọi thẳng chức năng Xóa BB-1\n"
     "2. KT-1 gọi thẳng chức năng Xóa BB-2\n"
     "3. KT-1 gọi thẳng chức năng Xóa BB-1",
     "—",
     "- Bước 1, 2: báo \"Không có quyền\", biên bản còn nguyên\n"
     "- Bước 3: báo \"Thao tác thành công\", BB-1 biến mất khỏi danh sách\n"
     "- Giao diện không có nút Xóa"),

    ("11", "Xem chi tiết, In biên bản công ty khác qua đường dẫn", "P1",
     "NV-X công ty 3 không có quyền nào; BB-3 Đã duyệt của công ty 1",
     "1. Đăng nhập NV-X, dán đường dẫn Chi tiết BB-3\n"
     "2. Dán đường dẫn In và Xuất Excel BB-3",
     "—",
     "- Theo code hiện tại: mở được cả ba, thấy đủ NV chịu và số tiền\n"
     "- Lưu ý: điểm hở cô lập dữ liệu - ghi Failed nếu nghiệp vụ yêu cầu chặn"),

    ("12", "Người duyệt công ty khác duyệt được biên bản", "P1",
     "DUYET-3 có quyền duyệt, thuộc công ty 3; BB-2 Chờ duyệt của công ty 1",
     "1. Đăng nhập DUYET-3, dán đường dẫn Chi tiết BB-2",
     "—",
     "- Theo code hiện tại: có nút Duyệt, duyệt thành công\n"
     "- Lưu ý: ghi Failed nếu nghiệp vụ yêu cầu chỉ duyệt biên bản công ty mình"),
]
