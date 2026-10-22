# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Phieu dieu chuyen vi tri'."""

MENU = "Mở menu Kho > nhóm \"Điều chuyển\" > bấm \"Phiếu điều chuyển vị trí\""

# Du lieu mau dung chung
DATA = ("Kho K1 (TK1 là thủ kho): hàng HH-0091 ĐVT cơ bản Cái, có ĐVT Thùng hệ số 12\n"
        "Vị trí P1 có lô L02 = 15 cái (công ty TPE); vị trí P4 đang trống")

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Quản lý Phiếu điều chuyển vị trí: chứng từ chuyển hàng từ vị trí này sang vị trí khác TRONG CÙNG MỘT "
     "KHO, theo từng lô. Tồn của kho không đổi, chỉ đổi tồn theo vị trí.\n"
     "Phiếu được lập tay, hoặc lập từ nút \"Tạo phiếu điều chuyển vị trí\" trên Phiếu kiểm kê theo vị trí "
     "(xử lý hàng thiếu) và trên Phiếu kiểm kê theo hàng hóa.\n"
     "Bấm \"Lưu\" thì giữ nháp, chưa đổi tồn. Bấm \"Điều chuyển\" thì hệ thống trừ tồn ở vị trí xuất và cộng "
     "tồn ở vị trí nhập NGAY, không qua bước duyệt.\n"
     "Người dùng làm được: xem danh sách, lọc, tạo, sửa và xóa nháp, đính kèm file PDF, In dự kiến, In phiếu, "
     "xem chi tiết, xuất Excel danh sách."),

    ("2. Đối tượng được tính / hiển thị",
     "Phiếu có 2 trạng thái:\n"
     "- Đang tạo (nhãn ĐỎ): đã bấm Lưu, chưa đổi tồn.\n"
     "- Đã chuyển (nhãn XANH): đã bấm Điều chuyển, tồn đã đổi.\n"
     "Lối vào: menu Kho > Điều chuyển > Phiếu điều chuyển vị trí. Danh sách LUÔN lấy theo quyền xem ở mục 7, "
     "sửa tham số trên thanh địa chỉ không đổi phạm vi.\n"
     "Lối vào màn Tạo mới có 3 cách: nút Tạo mới trên danh sách; nút \"Tạo phiếu điều chuyển vị trí\" trên "
     "Phiếu kiểm kê theo vị trí đang Chờ xử lý; nút cùng tên trên Phiếu kiểm kê theo hàng hóa.\n"
     "Phiếu Đang tạo của NGƯỜI KHÁC VẪN hiện trong danh sách (khác các màn kiểm kê)."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Số phiếu chỉ là liên kết mở Chi tiết khi phiếu Đã chuyển; phiếu Đang tạo không bấm được.\n"
     "- Menu bánh răng: Sửa, Xóa chỉ khi Đang tạo; \"In phiếu\" chỉ khi Đã chuyển.\n"
     "- Màn Chi tiết không có nút In, chỉ có Quay lại.\n"
     "- Ô Kho chỉ liệt kê kho mà người đăng nhập được phân công làm thủ kho.\n"
     "- Hộp chọn Vị trí xuất chỉ hiện vị trí đang có tồn của hàng đó; hộp chọn Vị trí nhập hiện mọi vị trí của kho.\n"
     "- Khi lập từ phiếu kiểm kê: ô Kho, ĐVT, Vị trí xuất, Lô xuất, SL bị KHÓA, chỉ chọn Vị trí nhập.\n"
     "- Cột \"Phiếu kiểm kê\" trên lưới KHÔNG hiện mã Phiếu kiểm kê theo vị trí (chỉ hiện mã phiếu kiểm kê "
     "theo hàng hóa hoặc phiếu kiểm kho cũ).\n"
     "- Không có bước duyệt, không có Hủy phiếu đã chuyển, không có In danh sách."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Ô \"Chọn khoảng thời gian\" lọc theo NGÀY LẬP phiếu.\n"
     "Ngày bắt đầu tính trọn ngày. Ngày kết thúc chỉ tính tới 0 giờ, nên phiếu lập TRONG CHÍNH NGÀY KẾT THÚC "
     "bị loại khỏi kết quả.\n"
     "Nút Xuất excel KHÔNG áp ô thời gian, ô hàng hóa và ô kho (xem mục 9)."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Phiếu: Kho, Ghi chú, File đính kèm (PDF).\n"
     "Mỗi dòng chi tiết: Tên hàng hóa, Model, Mã hàng hóa, Đơn vị tính, Vị trí xuất, Lô xuất, SL tồn, Vị trí "
     "nhập, SL. Một hàng có thể nằm nhiều dòng (khác vị trí, khác lô, hoặc cùng lô chia sang nhiều vị trí nhập).\n"
     "Số phiếu: PĐCVT-<số thứ tự 5 chữ số>, ví dụ PĐCVT-00318 (KHÔNG có mã công ty)."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- SL tồn của dòng = tồn của lô tại vị trí xuất chia cho hệ số ĐVT đang chọn, làm tròn 2 số lẻ.\n"
     "- SL lớn hơn SL tồn thì dòng tô nền ĐỎ NHẠT và nút \"Điều chuyển\" bị khóa.\n"
     "- Khi Điều chuyển, các dòng cùng hàng + vị trí xuất + lô được CỘNG DỒN (quy về ĐVT cơ bản) rồi so với "
     "tồn; đồng thời trừ đi phần hàng của phiếu nhập kho chưa hoàn tất tại vị trí đó.\n"
     "- Vị trí xuất và vị trí nhập của một dòng không được trùng nhau.\n"
     "- Bị chặn khi vị trí xuất / nhập đang được kiểm kê (kế hoạch kiểm kê Đang kiểm, phiếu kiểm kê theo vị trí "
     "Đang kiểm hoặc Chờ duyệt kết quả), hoặc hàng đang kiểm kê theo hàng hóa tại kho đó.\n"
     "- Phiếu lập từ phiếu kiểm kê theo vị trí: số đã chuyển được cộng vào dòng thiếu; chuyển đủ thì dòng đó "
     "coi như đã xử lý; hết dòng cần xử lý thì phiếu kiểm kê và kế hoạch gốc TỰ chuyển Hoàn thành."),

    ("7. Phân quyền cấp",
     "Các quyền thuộc nhóm \"Điều chuyển vị trí\" (phân hệ Kho):\n"
     "- \"Điều chuyển vị trí\": mở được màn Tạo mới (thiếu quyền thì trang không tìm thấy).\n"
     "- \"Xem điều chuyển vị trí theo tổng công ty\": thấy phiếu mọi công ty.\n"
     "- \"Xem điều chuyển vị trí theo công ty\": thấy phiếu của công ty mình (công ty người lập).\n"
     "- \"Xem điều chuyển vị trí theo kho\": thấy phiếu của các kho mình làm thủ kho.\n"
     "Không có quyền xem nào: chỉ thấy phiếu mình lập. Có nhiều quyền thì áp quyền rộng nhất.\n"
     "Sửa, Xóa, Xem chi tiết, In: code hiện tại KHÔNG kiểm tra người lập (xem mục 9).\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API (bỏ qua giao diện) dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- Dòng dưới bảng: \"Hiển thị a đến b của N\", N là tổng phiếu khớp bộ lọc trong phạm vi quyền.\n"
     "- Cột SL tồn: theo công thức ở mục 6, hiện \"-\" khi chưa chọn lô.\n"
     "- Hộp Chọn vị trí: cột Tồn = tồn của hàng tại vị trí, quy theo ĐVT đang chọn (lấy phần nguyên).\n"
     "- STT đánh liên tục qua các trang."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất:\n"
     "- Nút Sửa, Xóa hiện trên MỌI phiếu Đang tạo, kể cả của người khác, và người khác sửa / xóa được.\n"
     "- Ô thời gian: phiếu lập trong ngày kết thúc bị loại.\n"
     "- Xuất excel chỉ áp Mã phiếu và Trạng thái; bỏ qua thời gian, hàng hóa, kho.\n"
     "- SL = 0 vẫn Điều chuyển được (thông báo \"Bắt buộc phải nhập\" chỉ bắt ô trống).\n"
     "- Phiếu kiểm kê theo vị trí kiểm theo ĐVT lớn (ví dụ Thùng): dòng thiếu có thể không bao giờ được coi là "
     "đã xử lý dù đã chuyển đủ.\n"
     "- Phiếu nháp lập từ phiếu kiểm kê, sau đó Sửa rồi Điều chuyển: phiếu kiểm kê bị đặt Hoàn thành NGAY dù "
     "chưa chuyển đủ.\n"
     "- Lưu nháp KHÔNG giữ hàng: tới lúc Điều chuyển có thể báo vượt tồn.\n"
     "- Nút \"Hủy\" ở màn Tạo mới / Sửa chỉ là quay về danh sách, không hủy phiếu.\n"
     "- Thông báo lỗi dưới ô bằng tiếng Việt: \"Bắt buộc phải chọn\", \"Bắt buộc phải nhập\", \"Không hợp lệ\"."),
]


ROLE_TCS = [
    ("00", "Không có quyền nào: chỉ thấy phiếu mình lập, không mở được Tạo mới", "P0",
     "NV-A không có quyền nào ở mục 7, từng lập 2 phiếu; công ty có thêm 20 phiếu",
     "1. Đăng nhập NV-A\n"
     "2. " + MENU + "\n"
     "3. Đọc tổng, bấm Tạo mới",
     "Tài khoản: NV-A",
     "- Tổng = 2, đều do NV-A lập\n"
     "- Nút Tạo mới vẫn hiện, bấm vào thì trang không tìm thấy"),

    ("01", "Quyền Điều chuyển vị trí mở được Tạo mới", "P0",
     "TK1 có quyền \"Điều chuyển vị trí\", là thủ kho K1, K2; hệ thống có 6 kho",
     "1. TK1 bấm Tạo mới\n"
     "2. Mở ô Chọn kho",
     "—",
     "- Mở màn \"Tạo phiếu điều chuyển vị trí\"\n"
     "- Ô Chọn kho chỉ có K1, K2"),

    ("02", "Xem theo tổng công ty", "P0",
     "B chỉ có quyền \"Xem điều chuyển vị trí theo tổng công ty\"; công ty 1 có 12, công ty 3 có 5 phiếu",
     "1. B mở màn từ menu, đọc tổng",
     "—",
     "- Tổng = 17, gồm cả phiếu Đang tạo của người khác"),

    ("03", "Xem theo công ty", "P0",
     "C chỉ có quyền \"Xem điều chuyển vị trí theo công ty\", thuộc công ty 3; công ty 3 có 5 phiếu, C lập 1 "
     "phiếu khi còn ở công ty 1",
     "1. C mở màn từ menu, đọc tổng",
     "—",
     "- Tổng = 5\n"
     "- Lưu ý: phiếu C lập khi ở công ty 1 KHÔNG hiện (quyền này không cộng phiếu mình lập)"),

    ("04", "Xem theo kho", "P0",
     "TK2 chỉ có quyền \"Xem điều chuyển vị trí theo kho\", là thủ kho K2; K2 có 4 phiếu (của nhiều người), "
     "TK2 tự lập 1 phiếu ở K1",
     "1. TK2 mở màn từ menu, đọc tổng, soát cột Kho",
     "—",
     "- Tổng = 4, cột Kho đều là K2\n"
     "- Phiếu TK2 tự lập ở K1 KHÔNG hiện"),

    ("05", "Có nhiều quyền xem thì áp quyền rộng nhất", "P1",
     "D có cả quyền theo công ty và theo kho",
     "1. D mở màn từ menu, so tổng với C ở TC-ROLE-03 (cùng công ty)",
     "—",
     "- Tổng bằng phạm vi công ty"),

    ("06", "Người khác sửa được phiếu nháp không phải của mình", "P0",
     "PĐ-1 Đang tạo do TK1 lập; B (quyền tổng công ty, có quyền Điều chuyển vị trí) nhìn thấy PĐ-1",
     "1. B bấm bánh răng PĐ-1\n"
     "2. Bấm Sửa, đổi Ghi chú, bấm Lưu",
     "Ghi chú: B sửa",
     "- Mong đợi: B không thấy Sửa / Xóa trên phiếu của TK1\n"
     "- Lưu ý: code hiện tại hiện Sửa, Xóa và cho lưu — nếu vậy ghi Failed"),

    ("07", "Người khác xóa được phiếu nháp không phải của mình", "P0",
     "PĐ-2 Đang tạo do TK1 lập; B nhìn thấy PĐ-2",
     "1. B bấm bánh răng PĐ-2 > Xóa > Xác nhận",
     "—",
     "- Mong đợi: hệ thống từ chối\n"
     "- Lưu ý: code hiện tại báo \"Xóa thành công!\" — nếu vậy ghi Failed"),

    ("08", "Xem chi tiết và In phiếu không kiểm tra quyền", "P1",
     "NV-X công ty 3 không có quyền nào; nhận đường dẫn Chi tiết phiếu PĐ-3 (Đã chuyển) của công ty 1",
     "1. NV-X dán đường dẫn vào trình duyệt",
     "—",
     "- Theo code hiện tại: mở được\n"
     "- Lưu ý: ghi Failed nếu nghiệp vụ yêu cầu chặn"),

    ("09", "Gọi thẳng chức năng Lưu phiếu mới khi không có quyền Điều chuyển vị trí", "P0",
     "NV-A không có quyền Điều chuyển vị trí; tồn hợp lệ như dữ liệu mẫu",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Lưu phiếu với trạng thái Điều chuyển, bỏ qua giao diện",
     "—",
     "- Mong đợi: hệ thống từ chối, tồn không đổi\n"
     "- Lưu ý: quyền chỉ chặn ở màn Tạo mới — nếu điều chuyển được thì ghi Failed"),

    ("10", "Gọi thẳng chức năng điều chuyển cho kho mình không phải thủ kho", "P1",
     "TK1 có quyền Điều chuyển vị trí, chỉ là thủ kho K1",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Lưu phiếu, chọn kho K2",
     "—",
     "- Mong đợi: hệ thống từ chối\n"
     "- Nếu điều chuyển được trong kho K2 thì ghi Failed"),

    ("11", "Gọi thẳng chức năng Sửa phiếu đã chuyển", "P0",
     "PĐ-3 Đã chuyển",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Lưu sửa của PĐ-3",
     "—",
     "- Hệ thống từ chối (Lưu ý: nội dung thông báo có thể trống); PĐ-3 và tồn không đổi"),
]
