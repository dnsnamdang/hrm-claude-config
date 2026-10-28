# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Khai bao han muc cong no khach hang'."""

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Khai báo hạn mức công nợ cho từng khách hàng, RIÊNG THEO TỪNG CÔNG TY trong tập đoàn. Mỗi cặp "
     "Khách hàng - Công ty có 3 thông tin:\n"
     "- Cách tính lãi: \"Theo vượt hạn mức công nợ\" hoặc \"Theo thời gian thanh toán\".\n"
     "- Hạn mức công nợ tính lãi (VNĐ).\n"
     "- Hạn mức công nợ xuất hàng (VNĐ).\n"
     "Số liệu khai báo ở đây được dùng tiếp ở 3 nơi:\n"
     "- Phiếu yêu cầu xuất hàng: khi gửi duyệt, nếu công nợ của khách vượt Hạn mức công nợ xuất hàng "
     "của công ty người lập thì hệ thống hỏi xác nhận gửi duyệt vượt hạn mức.\n"
     "- Phiếu tính lãi: khi chọn khách hàng, hệ thống lấy Cách tính lãi và Hạn mức công nợ tính lãi "
     "của công ty người lập.\n"
     "- Báo cáo hạn mức công nợ khách hàng: hiển thị 2 cột Hạn mức tính lãi / Hạn mức được nợ.\n"
     "Người dùng làm được: xem danh sách khách hàng kèm hạn mức theo công ty, tìm theo khách hàng, "
     "sửa trực tiếp trên lưới và bấm nút Lưu (biểu tượng đĩa mềm) ở từng khách hàng."),

    ("2. Đối tượng được tính / hiển thị",
     "- Danh sách hiển thị TẤT CẢ khách hàng trong hệ thống: mọi trạng thái (đang hoạt động lẫn ngừng "
     "hoạt động), mọi công ty, kể cả khách chưa từng được khai báo hạn mức.\n"
     "- Mỗi khách hàng chiếm 1 khối dòng: dòng đầu là Mã khách / Tên khách / MST/CMND, các dòng dưới "
     "là từng công ty kèm 3 ô khai báo.\n"
     "- Khách CHƯA có khai báo nào: hiện đủ các công ty mà người đăng nhập được thấy (xem mục 7), ô Hạn "
     "mức hiện 0, ô Cách tính lãi chưa có giá trị thật.\n"
     "- Khách ĐÃ có khai báo ở ít nhất 1 công ty: CHỈ hiện các công ty đã được khai báo, các công ty "
     "chưa khai báo KHÔNG được bổ sung thêm dòng (xem mục 9).\n"
     "- Cột \"Cách tính lãi\" có 2 lựa chọn: Theo vượt hạn mức công nợ · Theo thời gian thanh toán."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Người chỉ có quyền \"Quản lý khai báo hạn mức công nợ khách hàng\" (KHÔNG có quyền \"Xem khai báo "
     "hạn mức công nợ khách hàng\"): chỉ thấy dòng của CÔNG TY MÌNH, các công ty khác bị ẩn.\n"
     "- Dòng công ty khác với công ty của người đăng nhập luôn bị KHÓA (ô xám, không sửa được), kể cả khi "
     "người đó có đủ 2 quyền.\n"
     "- Người không có quyền \"Quản lý khai báo hạn mức công nợ khách hàng\": mọi ô đều bị khóa.\n"
     "- Nút Lưu (biểu tượng đĩa mềm) KHÔNG bị ẩn với bất kỳ ai.\n"
     "- Màn hình KHÔNG có: nút Tạo mới, nút Xóa, In, Xuất Excel, Nhập Excel, sắp xếp theo cột, ô chọn số "
     "dòng mỗi trang, dòng tổng số bản ghi."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Không áp dụng: màn hình chỉ có 1 ô lọc \"Chọn khách hàng\", không có bộ lọc ngày. Hạn mức không có "
     "hiệu lực theo thời gian - giá trị đang lưu là giá trị dùng cho mọi chứng từ phát sinh sau đó."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Hai cấp: Khách hàng > Công ty.\n"
     "- Mỗi cặp Khách hàng - Công ty có tối đa 1 bộ khai báo (Cách tính lãi, Hạn mức tính lãi, Hạn mức "
     "xuất hàng).\n"
     "- Lưu ý quan trọng: mỗi lần bấm Lưu ở một khách hàng, hệ thống XÓA TOÀN BỘ khai báo cũ của khách "
     "đó (ở MỌI công ty) rồi ghi lại đúng những dòng đang hiện trên màn hình. Dòng nào không hiện trên "
     "màn của người bấm Lưu sẽ bị mất.\n"
     "- Người tạo / người cập nhật của khai báo được ghi nhận là người bấm Lưu gần nhất (không hiển thị "
     "trên màn)."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Không cộng dồn: mỗi lần Lưu là ghi đè toàn bộ, không giữ lịch sử thay đổi.\n"
     "- Khi Phiếu yêu cầu xuất hàng tra hạn mức: chỉ lấy khai báo của CÔNG TY NGƯỜI LẬP PHIẾU; khai báo "
     "của công ty khác không được dùng.\n"
     "- Công nợ đem so với hạn mức xuất hàng = (phát sinh Nợ - phát sinh Có tài khoản 131 của khách hàng, "
     "chỉ tính trên các hợp đồng do CHÍNH NGƯỜI LẬP PHIẾU tạo) + tổng tiền sau thuế của phiếu đang gửi.\n"
     "- Hạn mức xuất hàng bằng 0 hoặc để trống = KHÔNG giới hạn (không kiểm tra)."),

    ("7. Phân quyền cấp",
     "2 quyền thuộc nhóm \"Quản lý khai báo hạn mức công nợ khách hàng\" (danh mục Kế toán):\n"
     "- \"Quản lý khai báo hạn mức công nợ khách hàng\": được SỬA dòng của công ty mình.\n"
     "- \"Xem khai báo hạn mức công nợ khách hàng\": được XEM dòng của mọi công ty.\n"
     "Kết hợp:\n"
     "- Chỉ Quản lý: thấy và sửa dòng công ty mình; không thấy công ty khác.\n"
     "- Chỉ Xem: thấy mọi công ty, không sửa được ô nào.\n"
     "- Cả hai: thấy mọi công ty, sửa được dòng công ty mình.\n"
     "- Không có quyền nào: Lưu ý - VẪN thấy mục menu, VẪN mở được màn và thấy MỌI công ty (giống quyền "
     "Xem), mọi ô bị khóa.\n"
     "- Màn hình KHÔNG chặn quyền ở phía hệ thống khi Lưu: kiểm tra quyền chỉ nằm ở giao diện (khóa ô)."),

    ("8. Cách tính các ô thống kê",
     "Không có ô thống kê.\n"
     "- Cột STT = thứ tự dòng TRONG TRANG HIỆN TẠI (trang nào cũng bắt đầu lại từ 1).\n"
     "- Ô Hạn mức hiển thị dạng số nguyên có dấu phẩy ngăn cách hàng nghìn (vd 500,000,000); ô trống "
     "hiển thị 0."),

    ("9. Ghi chú đọc bảng",
     "- Phân trang 10 khách hàng/trang, thanh trang có nút « ‹ › » và tối đa 10 số trang.\n"
     "- Không có dòng \"tổng số bản ghi\"; để biết tổng phải lật tới trang cuối.\n"
     "- Bẫy 1 - MẤT DỮ LIỆU: người chỉ có quyền Quản lý (không có quyền Xem) bấm Lưu một khách hàng sẽ "
     "XÓA khai báo của các công ty khác của khách đó (vì các dòng đó không hiện trên màn của họ).\n"
     "- Bẫy 2 - KHÔNG THÊM ĐƯỢC CÔNG TY: khách đã có khai báo ở công ty 1 thì người công ty 3 (đủ 2 "
     "quyền) không thấy dòng công ty 3 để khai báo.\n"
     "- Bẫy 3 - GHI ĐÈ CHÉO: mỗi lần Lưu gửi lại cả dòng của công ty khác (đang khóa) theo số liệu lúc mở "
     "trang, nên có thể ghi đè số mới mà người công ty khác vừa lưu.\n"
     "- Bẫy 4 - Ô Cách tính lãi của khách mới: ô có thể hiển thị sẵn chữ \"Theo vượt hạn mức công nợ\" "
     "nhưng nếu không bấm chọn lại thì giá trị lưu xuống là TRỐNG; Phiếu tính lãi sẽ báo \"Khách hàng chưa "
     "cấu hình cách tính lãi!\".\n"
     "- Bẫy 5 - Giới hạn số: hạn mức lưu dạng số nguyên, tối đa 2,147,483,647. Nhập lớn hơn (vd 3 tỷ) "
     "hệ thống vẫn báo thành công nhưng lưu thành 2,147,483,647. Số lẻ thập phân bị làm tròn, số âm "
     "không bị chặn.\n"
     "- Bẫy 6 - Nút tìm kiếm: chỉ phản hồi khi bấm đúng vào biểu tượng kính lúp; chọn khách hàng xong "
     "không tự lọc.\n"
     "- Không có hỏi xác nhận trước khi Lưu, không cảnh báo khi chuyển trang mà chưa Lưu (số vừa nhập "
     "bị mất).\n"
     "- Nhóm TC dùng công cụ kiểm thử API (bỏ qua giao diện) dành cho tester kỹ thuật."),
]

ROLE_TCS = [
    ("00", "Tài khoản không có quyền nào vẫn mở được màn và xem mọi công ty", "P0",
     "Tài khoản NV-A không có quyền \"Quản lý khai báo hạn mức công nợ khách hàng\" lẫn \"Xem khai báo "
     "hạn mức công nợ khách hàng\"\n"
     "Hệ thống có 3 công ty: Công ty 1, Công ty 3, Công ty 4\n"
     "Khách KH-001 đã khai báo ở cả 3 công ty",
     "1. Đăng nhập bằng NV-A\n"
     "2. Mở menu Kế toán > Kế toán Công nợ > nhóm Khách hàng > bấm \"Khai báo hạn mức công nợ KH\"\n"
     "3. Tìm khách KH-001\n"
     "4. Thử bấm vào các ô của 3 dòng công ty",
     "Tài khoản: NV-A (không quyền)",
     "- Mục menu \"Khai báo hạn mức công nợ KH\" VẪN hiển thị\n"
     "- Màn mở bình thường, tiêu đề \"Khai báo hạn mức công nợ khách hàng\"\n"
     "- KH-001 hiện đủ 3 dòng công ty\n"
     "- Cả 3 dòng đều bị khóa (ô xám), không sửa được\n"
     "- Lưu ý: theo đúng logic hiện tại, tài khoản không quyền xem được như người có quyền Xem"),

    ("01", "Chỉ có quyền Xem: thấy mọi công ty, không sửa được", "P0",
     "Tài khoản B chỉ có quyền \"Xem khai báo hạn mức công nợ khách hàng\", thuộc Công ty 1\n"
     "KH-001 khai báo ở Công ty 1 (500,000,000) và Công ty 3 (300,000,000)",
     "1. Đăng nhập bằng B, mở màn Khai báo hạn mức công nợ KH\n"
     "2. Tìm KH-001\n"
     "3. Thử sửa ô Hạn mức công nợ xuất hàng ở dòng Công ty 1",
     "Quyền: Xem khai báo hạn mức công nợ khách hàng",
     "- KH-001 hiện 2 dòng: Công ty 1 và Công ty 3 với đúng số liệu\n"
     "- Cả 2 dòng khóa, kể cả dòng Công ty 1 (công ty của B)\n"
     "- Nút Lưu (đĩa mềm) vẫn hiển thị"),

    ("02", "Chỉ có quyền Quản lý: chỉ thấy và sửa được công ty mình", "P0",
     "Tài khoản C chỉ có quyền \"Quản lý khai báo hạn mức công nợ khách hàng\", thuộc Công ty 3\n"
     "KH-001 khai báo ở Công ty 1 (500,000,000) và Công ty 3 (300,000,000)",
     "1. Đăng nhập bằng C, mở màn\n"
     "2. Tìm KH-001\n"
     "3. Quan sát số dòng công ty và trạng thái các ô",
     "Quyền: Quản lý khai báo hạn mức công nợ khách hàng",
     "- KH-001 chỉ hiện 1 dòng Công ty 3, số 300,000,000\n"
     "- KHÔNG có dòng Công ty 1\n"
     "- 3 ô của dòng Công ty 3 sửa được"),

    ("03", "Có cả 2 quyền: thấy mọi công ty, chỉ sửa được công ty mình", "P0",
     "Tài khoản D có cả quyền Quản lý và quyền Xem, thuộc Công ty 1\n"
     "KH-001 khai báo ở Công ty 1, Công ty 3, Công ty 4",
     "1. Đăng nhập bằng D, mở màn\n"
     "2. Tìm KH-001\n"
     "3. Thử sửa từng dòng",
     "Quyền: Quản lý + Xem",
     "- Hiện đủ 3 dòng công ty\n"
     "- Chỉ dòng Công ty 1 sửa được\n"
     "- Dòng Công ty 3 và Công ty 4 bị khóa"),

    ("04", "Quản lý ở công ty này không sửa được khai báo của công ty khác dù thấy", "P1",
     "Tài khoản D có cả 2 quyền, thuộc Công ty 1; được chuyển sang Công ty 3 trong hồ sơ nhân sự",
     "1. Đăng nhập lại bằng D sau khi đổi công ty\n"
     "2. Mở màn, tìm KH-001",
     "Công ty của D: Công ty 3",
     "- Dòng Công ty 3 mở khóa\n"
     "- Dòng Công ty 1 chuyển sang khóa\n"
     "- Quyền sửa đi theo công ty hiện tại trong hồ sơ nhân sự"),

    ("05", "Người không có quyền bấm Lưu không làm thay đổi số liệu", "P1",
     "Tài khoản B chỉ có quyền Xem\n"
     "KH-001 khai báo Công ty 1: Hạn mức xuất hàng 500,000,000",
     "1. Đăng nhập bằng B, tìm KH-001\n"
     "2. Bấm nút Lưu (đĩa mềm)\n"
     "3. Tải lại trang, tìm lại KH-001",
     "—",
     "- Hiện thông báo xanh \"Cập nhật thành công!\"\n"
     "- Số liệu sau khi tải lại giữ nguyên 500,000,000\n"
     "- Lưu ý: hệ thống không chặn thao tác Lưu của người không có quyền, chỉ vì ô bị khóa nên số "
     "không đổi"),

    ("06", "Gọi thẳng chức năng Lưu bằng công cụ kiểm thử API khi không có quyền Quản lý", "P0",
     "Tài khoản B chỉ có quyền Xem, thuộc Công ty 1\n"
     "KH-001 khai báo Công ty 1: Hạn mức xuất hàng 500,000,000",
     "1. Đăng nhập bằng B\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Lưu khai báo của KH-001, bỏ qua giao diện, gửi "
     "Hạn mức xuất hàng Công ty 1 = 999,000,000\n"
     "3. Mở lại màn, tìm KH-001",
     "Hạn mức công nợ xuất hàng: 999,000,000",
     "- Kỳ vọng nghiệp vụ: hệ thống từ chối, báo không có quyền, số giữ 500,000,000\n"
     "- Lưu ý: theo code hiện tại hệ thống KHÔNG kiểm tra quyền khi Lưu nên sẽ lưu thành 999,000,000 - "
     "ghi nhận là lỗ hổng phân quyền nếu xảy ra"),

    ("07", "Gọi thẳng chức năng Lưu để sửa khai báo của công ty khác", "P0",
     "Tài khoản C chỉ có quyền Quản lý, thuộc Công ty 3\n"
     "KH-001 khai báo Công ty 1: 500,000,000; Công ty 3: 300,000,000",
     "1. Đăng nhập bằng C\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Lưu của KH-001, gửi kèm dòng Công ty 1 = "
     "1,000,000,000\n"
     "3. Đăng nhập tài khoản có quyền Xem, mở KH-001",
     "Công ty 1 - Hạn mức xuất hàng: 1,000,000,000",
     "- Kỳ vọng nghiệp vụ: hệ thống từ chối dòng của công ty khác\n"
     "- Lưu ý: theo code hiện tại dòng Công ty 1 bị đổi thành 1,000,000,000 - ghi nhận lỗ hổng nếu xảy ra"),
]
