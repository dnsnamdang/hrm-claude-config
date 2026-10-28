# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Ke hoach kiem ke theo hang hoa'."""

MENU = ("Mở menu Kế toán > nhóm \"Kiểm kê\" > cột \"Theo vị trí\" > bấm \"Kế hoạch kiểm kê theo hàng hóa\"")

P1 = "Phiếu kiểm kê theo hàng hóa"

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Quản lý Kế hoạch kiểm kê theo hàng hóa: chứng từ do người lập (thường là kế toán kho) tạo ra để "
     "chốt DANH SÁCH MẶT HÀNG cần kiểm kê trong một hoặc nhiều kho vật lý và HỘI ĐỒNG KIỂM KÊ.\n"
     "Khi thêm một hàng, hệ thống chụp lại tồn kho KẾ TOÁN hiện tại của hàng đó, chia theo từng kho kế "
     "toán. Số liệu này là căn cứ để thủ kho lập Phiếu kiểm kê theo hàng hóa.\n"
     "Người dùng làm được: xem danh sách, lọc, tạo kế hoạch (Lưu nháp hoặc Lưu & kiểm), sửa, xóa khi còn "
     "nháp, xem chi tiết, in và xuất Excel từng kế hoạch hoặc cả danh sách.\n"
     "Người có quyền Lập phiếu kiểm kê kho theo hàng hóa nhận thông báo và bấm \"Lập phiếu kiểm kê theo "
     "hàng hóa\" ngay trên kế hoạch."),

    ("2. Đối tượng được tính / hiển thị",
     "Kế hoạch có 4 trạng thái hiển thị:\n"
     "- Đang tạo (nhãn ĐỎ): vừa bấm Lưu, còn sửa / xóa được.\n"
     "- Đang kiểm (nhãn ĐỎ): đã bấm Lưu & kiểm, chờ lập phiếu kiểm kê.\n"
     "- Đã lập phiếu kiểm kê (nhãn XANH): đã có Phiếu kiểm kê theo hàng hóa được lưu từ kế hoạch này.\n"
     "- Hoàn thành (nhãn XANH): có trong ô lọc Trạng thái nhưng hiện KHÔNG có thao tác nào đưa kế hoạch "
     "tới trạng thái này (xem mục 9).\n"
     "Phạm vi kế hoạch nhìn thấy phụ thuộc lối vào:\n"
     "- Lối vào từ menu (Kế toán > Kiểm kê > Theo vị trí > Kế hoạch kiểm kê theo hàng hóa): theo quyền "
     "xem ở mục 7, luôn ẩn kế hoạch Đang tạo của người khác.\n"
     "- Lối vào \"Kế hoạch của tôi\" (không có mục menu; hệ thống tự đưa về đây sau khi bấm Xóa): chỉ kế "
     "hoạch do chính mình lập, gồm cả nháp.\n"
     "Bảng chi tiết của kế hoạch: mỗi hàng hóa kèm các kho kế toán đang có tồn kế toán lớn hơn 0."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Kế hoạch Đang tạo của NGƯỜI KHÁC bị ẩn ở lối vào menu, kể cả với quyền tổng công ty.\n"
     "- Nút Sửa và Xóa (trong menu bánh răng ở cột Hành động) chỉ hiện khi kế hoạch Đang tạo VÀ người "
     "đăng nhập là người lập.\n"
     "- Nút \"Lập phiếu kiểm kê theo hàng hóa\" chỉ hiện khi kế hoạch Đang kiểm VÀ người đăng nhập có "
     "quyền Lập phiếu kiểm kê kho theo hàng hóa. KHÔNG kiểm tra người đó có phải thủ kho của kho không.\n"
     "- Nút In và Xuất excel luôn hiện cho mọi dòng, mọi trạng thái.\n"
     "- Cửa sổ chọn hàng chỉ liệt kê hàng có tồn kế toán lớn hơn 0 trong các kho đã chọn.\n"
     "- Kho kế toán có tồn bằng 0 không hiện dưới hàng hóa.\n"
     "- Màn hình KHÔNG có chức năng Hủy kế hoạch, KHÔNG có đính kèm, KHÔNG có Nhập Excel, KHÔNG cho sửa "
     "Tổng SL bằng tay.\n"
     "- Ô lọc Công ty / Phòng ban chỉ hiện ở lối vào menu với người có quyền xem theo tổng công ty / "
     "theo công ty."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Hai ô \"Từ ngày\" và \"Đến ngày\" lọc theo NGÀY LẬP kế hoạch (chính là cột \"Ngày kiểm kê\" trên "
     "lưới).\n"
     "Hai đầu mút đều được tính TRỌN NGÀY: kế hoạch lập lúc 23:59 của ngày điền ở ô \"Đến ngày\" vẫn có "
     "trong kết quả.\n"
     "Ô \"Ngày kiểm kê\" trên màn nhập bị khóa: khi tạo là hôm nay; khi sửa hiện ngày cũ nhưng bấm Lưu "
     "thì hệ thống ghi lại thành ngày sửa. Cột \"Ngày kiểm kê\" trên lưới vẫn giữ ngày lập ban đầu."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Khung \"Thông tin chung\": Ngày kiểm kê (khóa), Kho (chọn nhiều kho vật lý của công ty mình), "
     "Ghi chú.\n"
     "Tab \"Hàng hóa\": Hàng hóa (Tên hàng, Model, Mã hàng, ĐVT cơ bản, Tổng SL) > Kho kế toán (mã - tên) "
     "> SL tồn kho kế toán.\n"
     "Tab \"Hội đồng kiểm kê\": danh sách Thành viên + Chức vụ (Chức vụ chọn trong các vai trò đã gán cho "
     "nhân viên đó; chọn thành viên thì Chức vụ tự lấy vai trò đầu tiên).\n"
     "Số phiếu sinh tự động: <mã công ty của người lập>.KHKKHH-<số thứ tự 5 chữ số>, ví dụ "
     "TPE.KHKKHH-00125 (ngăn cách bằng DẤU CHẤM, khác kế hoạch theo vị trí dùng gạch ngang)."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- \"SL tồn kho kế toán\" = tồn kế toán của hàng tại kho kế toán đó, lúc bấm chọn hàng.\n"
     "- \"Tổng SL\" của một hàng = tổng các dòng SL tồn kho kế toán bên dưới hàng đó.\n"
     "- Một hàng chỉ được chọn 1 lần (chọn lại báo \"Hàng hóa đã được chọn\").\n"
     "- Một nhân viên có thể bị thêm 2 lần vào Hội đồng kiểm kê, hệ thống không chặn.\n"
     "- Số liệu tồn được LƯU CỨNG lúc bấm Lưu; tồn thay đổi sau đó không làm đổi màn Chi tiết, bản In.\n"
     "- Riêng khi mở màn Sửa, hệ thống lấy lại TỒN HIỆN TẠI cho mọi hàng; lưu lại thì ghi đè số cũ.\n"
     "- Đổi ô Kho (thêm hay bớt kho) thì danh sách hàng bị XÓA SẠCH, không hỏi xác nhận."),

    ("7. Phân quyền cấp",
     "Ba quyền thuộc nhóm \"Kiểm kê kho\" (phân hệ Kho):\n"
     "- \"Tổng kiểm kê kho theo hàng hóa - tổng công ty\": ở lối vào menu xem kế hoạch của MỌI công ty; "
     "khối lọc có thêm ô Công ty và Phòng ban; ô lọc Kho liệt kê kho của mọi công ty.\n"
     "- \"Tổng kiểm kê kho theo hàng hóa\": ở lối vào menu xem kế hoạch của công ty mình và kế hoạch do "
     "mình lập; khối lọc có thêm ô Phòng ban.\n"
     "- \"Lập phiếu kiểm kê kho theo hàng hóa\": nhận thông báo khi kế hoạch được gửi kiểm và có nút "
     "\"Lập phiếu kiểm kê theo hàng hóa\" trên kế hoạch Đang kiểm.\n"
     "Không có quyền nào: vẫn vào được màn, vẫn Tạo mới được, chỉ thấy kế hoạch của mình.\n"
     "Xem chi tiết, In, Xuất excel KHÔNG kiểm tra quyền.\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API (bỏ qua giao diện) dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- Dòng thông tin dưới bảng: \"Hiển thị a đến b của N\" - a là dòng đầu trang, b là dòng cuối trang, "
     "N là tổng kế hoạch khớp bộ lọc trong phạm vi lối vào đang mở.\n"
     "- Màn này KHÔNG có ô đếm ở Trang chủ.\n"
     "- STT trên lưới đánh liên tục qua các trang.\n"
     "- \"Tổng SL\" làm tròn 2 chữ số thập phân khi lưu."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- Ô lọc Kho, ô lọc Công ty, ô lọc Phòng ban HIỆN RA nhưng KHÔNG có tác dụng lọc.\n"
     "- Ô lọc \"Nhập mã hàng hóa\" làm bảng báo lỗi, không tải được dữ liệu.\n"
     "- Bấm Xóa kế hoạch nháp thì hệ thống báo lỗi, kế hoạch KHÔNG bị xóa.\n"
     "- Bấm Xuất excel trên MỘT kế hoạch thì hệ thống báo lỗi, không tải được tệp (Xuất excel danh sách "
     "vẫn chạy).\n"
     "- Chọn từ 2 kho trở lên: hàng chỉ lấy tồn kế toán của MỘT kho vật lý, Tổng SL thiếu phần của kho "
     "còn lại.\n"
     "- Nút làm mới số liệu (biểu tượng mũi tên tròn) không có tác dụng.\n"
     "- Cảnh báo \"phiếu chưa xử lí xong\" khi Lưu & kiểm chỉ xét hàng CUỐI CÙNG trong danh sách.\n"
     "- Thông báo gửi kiểm mở ra Phiếu kiểm kê theo hàng hóa có cùng số thứ tự, KHÔNG mở kế hoạch.\n"
     "- Kế hoạch chuyển \"Đã lập phiếu kiểm kê\" ngay khi bấm Lưu phiếu kiểm kê (kể cả lưu nháp); xóa "
     "phiếu kiểm kê đó thì kế hoạch KHÔNG quay lại Đang kiểm.\n"
     "- Kế hoạch KHÔNG bao giờ lên \"Hoàn thành\", kể cả khi phiếu kiểm kê đã hoàn thành.\n"
     "- Thông báo lỗi kiểm tra dữ liệu dưới từng ô hiển thị bằng TIẾNG ANH (ví dụ \"The products field "
     "is required.\").\n"
     "- Bản In: tên các thành viên Hội đồng kiểm kê viết liền nhau, không có dấu ngăn cách, không có "
     "Chức vụ.\n"
     "- Nút trên màn Sửa ghi \"Lưu & gửi\", trên màn Tạo mới ghi \"Lưu & kiểm\" - cùng một chức năng.\n"
     "- Hệ thống ghi nhớ bộ lọc và trang đang xem theo từng lối vào, trên từng trình duyệt."),
]


ROLE_TCS = [
    ("00", "Tài khoản không có quyền nào chỉ thấy kế hoạch do mình lập", "P0",
     "Tài khoản NV-A không có quyền nào trong 3 quyền ở mục 7\n"
     "NV-A đã lập 3 kế hoạch (1 Đang tạo, 2 Đang kiểm)\n"
     "Công ty của NV-A có thêm 20 kế hoạch đã gửi của người khác",
     "1. Đăng nhập bằng NV-A\n"
     "2. " + MENU + "\n"
     "3. Đọc số tổng dưới bảng\n"
     "4. Bấm nút Bộ lọc, quan sát các ô lọc",
     "Tài khoản: NV-A",
     "- Vào được màn, không bị chặn\n"
     "- Tổng hiện đúng 3 (gồm cả kế hoạch nháp của NV-A), mọi dòng có Người lập là NV-A\n"
     "- Nút Tạo mới VẪN hiển thị\n"
     "- Khối lọc KHÔNG có ô Công ty, Phòng ban"),

    ("01", "Quyền tổng công ty thấy kế hoạch của mọi công ty", "P0",
     "Tài khoản B chỉ có quyền \"Tổng kiểm kê kho theo hàng hóa - tổng công ty\"\n"
     "Công ty 1 có 10 kế hoạch đã gửi, công ty 3 có 4 kế hoạch đã gửi\n"
     "Người khác có 2 kế hoạch Đang tạo; B chưa lập kế hoạch nào",
     "1. Đăng nhập bằng B\n"
     "2. " + MENU + "\n"
     "3. Đọc số tổng\n"
     "4. Bấm nút Bộ lọc, mở ô Kho",
     "Quyền: Tổng kiểm kê kho theo hàng hóa - tổng công ty",
     "- Tổng = 14 (kế hoạch của cả 2 công ty)\n"
     "- 2 kế hoạch Đang tạo của người khác KHÔNG hiện\n"
     "- Khối lọc hiện CẢ ô Công ty và ô Phòng ban\n"
     "- Ô Kho liệt kê kho của mọi công ty"),

    ("02", "Quyền theo công ty chỉ thấy kế hoạch công ty mình và kế hoạch mình lập", "P0",
     "Tài khoản C chỉ có quyền \"Tổng kiểm kê kho theo hàng hóa\", thuộc công ty 3\n"
     "Công ty 3 có 4 kế hoạch đã gửi, công ty 1 có 10 kế hoạch đã gửi\n"
     "C đã lập 1 kế hoạch khi còn thuộc công ty 1",
     "1. Đăng nhập bằng C\n"
     "2. " + MENU + "\n"
     "3. Đọc số tổng, soát cột Số phiếu (tiền tố mã công ty)\n"
     "4. Bấm Bộ lọc, mở ô Kho",
     "Quyền: Tổng kiểm kê kho theo hàng hóa",
     "- Tổng = 4 + 1 = 5\n"
     "- Không thấy kế hoạch nào khác của công ty 1\n"
     "- Khối lọc có ô Phòng ban, KHÔNG có ô Công ty\n"
     "- Ô Kho chỉ liệt kê kho của công ty 3"),

    ("03", "Có cả hai quyền xem thì áp quyền rộng hơn", "P1",
     "Tài khoản D có cả \"Tổng kiểm kê kho theo hàng hóa - tổng công ty\" và \"Tổng kiểm kê kho theo "
     "hàng hóa\"",
     "1. Đăng nhập bằng D, mở màn từ menu\n"
     "2. So số tổng với tài khoản B ở TC-ROLE-01",
     "—",
     "- Số tổng bằng số của B (phạm vi tổng công ty)\n"
     "- Khối lọc có ô Công ty"),

    ("04", "Có quyền Lập phiếu thì thấy nút Lập phiếu kiểm kê trên kế hoạch Đang kiểm", "P0",
     "Tài khoản TK1 có quyền \"Lập phiếu kiểm kê kho theo hàng hóa\" và \"Tổng kiểm kê kho theo hàng hóa\"\n"
     "Công ty có kế hoạch KH-2 Đang kiểm, KH-4 Đã lập phiếu kiểm kê",
     "1. Đăng nhập bằng TK1, mở màn từ menu\n"
     "2. Bấm biểu tượng bánh răng ở cột Hành động của KH-2\n"
     "3. Bấm bánh răng của KH-4",
     "—",
     "- KH-2: menu có \"Lập phiếu kiểm kê theo hàng hóa\", In, Xuất excel\n"
     "- KH-4: chỉ có In, Xuất excel"),

    ("05", "Không có quyền Lập phiếu thì không có nút và bị chặn khi mở thẳng", "P0",
     "Tài khoản NV-C chỉ có quyền \"Tổng kiểm kê kho theo hàng hóa\"\n"
     "Kế hoạch KH-2 Đang kiểm; NV-C nhận được đường dẫn màn lập phiếu kiểm kê gắn KH-2 từ đồng nghiệp",
     "1. Đăng nhập NV-C, mở màn từ menu, bấm bánh răng của KH-2\n"
     "2. Dán đường dẫn lập phiếu kiểm kê gắn KH-2 vào trình duyệt",
     "—",
     "- Bước 1: menu chỉ có In, Xuất excel\n"
     "- Bước 2: màn " + P1 + " mở ra nhưng báo \"Không có quyền\", KHÔNG điền sẵn dữ liệu kế hoạch"),

    ("06", "Có quyền Lập phiếu nhưng không phải thủ kho vẫn có nút", "P1",
     "Tài khoản TK2 có quyền \"Lập phiếu kiểm kê kho theo hàng hóa\" và \"Tổng kiểm kê kho theo hàng "
     "hóa\", KHÔNG được phân công thủ kho của kho K1\n"
     "Kế hoạch KH-2 Đang kiểm của kho K1",
     "1. Đăng nhập TK2, mở màn từ menu\n"
     "2. Bấm bánh răng của KH-2",
     "—",
     "- Theo code hiện tại: CÓ nút \"Lập phiếu kiểm kê theo hàng hóa\" (không kiểm tra thủ kho)\n"
     "- Lưu ý: khác màn kế hoạch theo vị trí (có kiểm tra thủ kho) - ghi Failed nếu nghiệp vụ yêu cầu "
     "chỉ thủ kho được lập"),

    ("07", "Chỉ người lập mới thấy Sửa / Xóa trên kế hoạch Đang tạo", "P0",
     "NV-A lập kế hoạch KH-1 ở trạng thái Đang tạo\n"
     "NV-B cùng công ty có quyền \"Tổng kiểm kê kho theo hàng hóa - tổng công ty\"",
     "1. Đăng nhập NV-A, bấm bánh răng của KH-1\n"
     "2. Đăng nhập NV-B, tìm KH-1 bằng ô Mã phiếu",
     "—",
     "- NV-A thấy: Sửa, Xóa, In, Xuất excel\n"
     "- NV-B KHÔNG tìm thấy KH-1 (nháp người khác bị ẩn)"),

    ("08", "Xem chi tiết, In không kiểm tra quyền và công ty", "P1",
     "NV-X thuộc công ty 3, không có quyền nào\n"
     "Kế hoạch KH-2 của công ty 1; NV-X nhận được đường dẫn màn Chi tiết KH-2 từ đồng nghiệp",
     "1. Đăng nhập NV-X\n"
     "2. Dán đường dẫn màn Chi tiết KH-2 vào trình duyệt\n"
     "3. Dán đường dẫn In của KH-2",
     "—",
     "- Theo code hiện tại: hệ thống MỞ ĐƯỢC chi tiết và bản In của KH-2\n"
     "- Bản In mang tiêu đề (logo) công ty của NV-X, không phải công ty 1\n"
     "- Lưu ý: điểm hở cô lập dữ liệu giữa các công ty - ghi Failed nếu nghiệp vụ yêu cầu chặn"),

    ("09", "Gọi thẳng chức năng Lưu sửa trên kế hoạch không phải của mình", "P0",
     "Kế hoạch KH-1 Đang tạo do NV-A lập\n"
     "Tester kỹ thuật đăng nhập bằng NV-B",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Lưu sửa của KH-1, bỏ qua giao diện, gửi ghi chú "
     "mới\n"
     "2. Đăng nhập NV-A mở lại KH-1",
     "—",
     "- Hệ thống báo \"Bạn không có quyền sửa phiếu này\"\n"
     "- KH-1 giữ nguyên"),

    ("10", "Gọi thẳng chức năng Lưu sửa trên kế hoạch đã gửi của chính mình", "P0",
     "Kế hoạch KH-2 Đang kiểm do chính NV-A lập",
     "1. Đăng nhập NV-A\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Lưu sửa của KH-2, gửi trạng thái Đang tạo\n"
     "3. Gọi thẳng chức năng mở màn Sửa của KH-2",
     "—",
     "- Bước 2: báo \"Bạn không có quyền sửa phiếu này\", KH-2 vẫn Đang kiểm\n"
     "- Bước 3: hiện trang không tìm thấy"),

    ("11", "Gọi thẳng chức năng Xóa kế hoạch của người khác", "P0",
     "Kế hoạch KH-1 Đang tạo do NV-A lập; tester đăng nhập NV-B",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa của KH-1, bỏ qua giao diện\n"
     "2. Đăng nhập NV-A kiểm tra KH-1",
     "—",
     "- Hệ thống báo \"Không thể xóa!\", đưa về danh sách \"Kế hoạch của tôi\"\n"
     "- KH-1 vẫn còn nguyên"),
]
