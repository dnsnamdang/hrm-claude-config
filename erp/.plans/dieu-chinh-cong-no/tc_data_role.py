# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen — man ERP 'Phieu yeu cau dieu chinh cong no'."""

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Quản lý Phiếu yêu cầu điều chỉnh công nợ: chứng từ do kinh doanh lập để đề nghị kế toán CHUYỂN "
     "một khoản công nợ từ hợp đồng / khách hàng này sang hợp đồng / khách hàng khác.\n"
     "Mỗi phiếu gồm nhiều dòng \"Điều chỉnh từ\"; mỗi dòng lại có nhiều dòng \"Điều chỉnh đến\" để "
     "tách khoản tiền đó ra nhiều đích.\n"
     "Có 2 loại phiếu: Điều chỉnh công nợ khách hàng và Điều chỉnh công nợ NCC — hai loại dùng hai "
     "bảng nhập khác nhau và hai quy tắc số tiền khác nhau (xem mục 6).\n"
     "Luồng: người lập Lưu nháp hoặc Lưu và gửi duyệt → Kế toán thanh toán mở màn chờ duyệt, chọn "
     "\"Tạo phiếu kế toán\" (đồng ý) hoặc \"Không duyệt\" (từ chối, bắt buộc nhập lý do).\n"
     "Phiếu còn được tạo tự động từ màn Phiếu báo có: hệ thống đẩy sẵn các dòng điều chỉnh từ sang "
     "màn tạo phiếu."),

    ("2. Đối tượng được tính / hiển thị",
     "Phiếu hiển thị đủ 6 trạng thái: Đang tạo · Chờ tạo phiếu kế toán · Đã tạo phiếu kế toán · Đã "
     "duyệt phiếu kế toán · Hủy · Từ chối.\n"
     "Hai nhãn \"Đã tạo phiếu kế toán\" và \"Đã duyệt phiếu kế toán\" tô XANH; bốn nhãn còn lại tô ĐỎ.\n"
     "Phạm vi phiếu nhìn thấy phụ thuộc chế độ danh sách đang mở:\n"
     "- Chế độ \"Phiếu của tôi\" (đường dẫn không kèm tham số): chỉ phiếu do chính mình lập, gồm cả "
     "phiếu nháp của mình.\n"
     "- Chế độ \"Tất cả\" (mục menu trỏ vào đây): lấy theo 4 quyền xem ở mục 7, và luôn ẩn phiếu nháp "
     "của người khác.\n"
     "- Chế độ \"Chờ duyệt\" (mục Phiếu yêu cầu điều chỉnh công nợ chờ duyệt): chỉ phiếu trạng thái "
     "Chờ tạo phiếu kế toán, do người thuộc CÔNG TY của người đăng nhập lập.\n"
     "- Chế độ \"Đã xử lý\": xem cảnh báo ở mục 9 — màn này đang lấy nhầm dữ liệu.\n"
     "Cột \"KH/NCC\" hiển thị khách hàng của dòng điều chỉnh ĐẾN đầu tiên (với phiếu khách hàng) hoặc "
     "nhà cung cấp của dòng điều chỉnh TỪ đầu tiên (với phiếu NCC)."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu nháp (Đang tạo) của NGƯỜI KHÁC bị ẩn ở chế độ \"Tất cả\".\n"
     "- Nút \"Tạo phiếu kế toán\" và \"Không duyệt\" chỉ hiện với người có quyền \"Kế toán thanh toán\" "
     "và chỉ trên phiếu đang ở trạng thái Chờ tạo phiếu kế toán.\n"
     "- ⚠️ Màn CHI TIẾT KHÔNG có nút Sửa, Xóa, In và Xuất Excel — bốn thao tác này chỉ có trong menu "
     "hành động của từng dòng ngoài danh sách.\n"
     "- Màn Chờ duyệt bỏ nút Tạo mới và bỏ nút Xuất Excel danh sách.\n"
     "- Ô \"Loại phiếu\" bị KHÓA khi mở màn Sửa: đã lưu rồi thì không đổi được loại phiếu.\n"
     "- Hai ô Loại tiền và Tỷ giá CHỈ hiện khi Loại phiếu là Điều chỉnh công nợ NCC; phiếu khách hàng "
     "không có hai ô này.\n"
     "- Với phiếu tạo từ Phiếu báo có: nút thêm dòng \"Điều chỉnh từ\" bị ẩn, người dùng chỉ được thêm "
     "dòng \"Điều chỉnh đến\".\n"
     "- Cửa sổ chọn hợp đồng ở cột \"Điều chỉnh từ\" CHỈ hiện hợp đồng do chính người đăng nhập lập, "
     "và loại bỏ hợp đồng còn ở trạng thái Đang tạo / Chờ duyệt / Từ chối / Hủy.\n"
     "- Màn hình KHÔNG có chức năng Nhập Excel."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Hai ô \"Từ ngày\" và \"Đến ngày\" lọc theo NGÀY LẬP PHIẾU.\n"
     "⚠️ Hai đầu mút KHÔNG được tính trọn ngày: hệ thống so với mốc 0 giờ của ngày nhập vào, nên phiếu "
     "lập trong chính ngày điền ở ô \"Đến ngày\" bị loại khỏi kết quả. Đây là bẫy đối chiếu số liệu.\n"
     "Không có bộ lọc theo cột \"Ngày nhận\" (ngày gửi duyệt), dù cột này có trên lưới."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "BA cấp: Phiếu → dòng \"Điều chỉnh từ\" → dòng \"Điều chỉnh đến\".\n"
     "- Phiếu giữ: Mã phiếu, Loại phiếu, Số phiếu báo có (nếu tạo từ báo có), Loại tiền và Tỷ giá (chỉ "
     "phiếu NCC), Diễn giải, Trạng thái, Người lập, Phòng ban, Ngày nhận, Người duyệt, Lý do không "
     "duyệt.\n"
     "- Mỗi dòng \"Điều chỉnh từ\" gắn một khách hàng (hoặc nhà cung cấp) và một hợp đồng, kèm Số dư và "
     "Số tiền điều chỉnh từ.\n"
     "- Mỗi dòng \"Điều chỉnh từ\" có ÍT NHẤT MỘT dòng \"Điều chỉnh đến\"; mỗi dòng đến cũng gắn một "
     "khách hàng (hoặc nhà cung cấp), một hợp đồng và một số tiền.\n"
     "- Mã phiếu sinh tự động: mã công ty + \".DNDCCN\" + tháng năm (4 số) + \".\" + 5 chữ số tăng dần, "
     "ví dụ TPE.DNDCCN0826.00012. Không sửa tay được.\n"
     "- Công ty / Phòng ban / Bộ phận của phiếu lấy từ hồ sơ nhân sự của người lập lúc tạo phiếu.\n"
     "- Mỗi lần lưu, toàn bộ dòng chi tiết cũ bị xóa và ghi lại từ đầu."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "QUY TẮC SỐ TIỀN — khác nhau theo loại phiếu, đây là phần dễ sai nhất của màn:\n"
     "- Phiếu ĐIỀU CHỈNH CÔNG NỢ KHÁCH HÀNG: tổng các dòng \"Điều chỉnh đến\" KHÔNG ĐƯỢC LỚN HƠN số "
     "tiền \"Điều chỉnh từ\". Được phép NHỎ HƠN. Áp dụng cả khi Lưu nháp lẫn khi Gửi duyệt.\n"
     "- Phiếu ĐIỀU CHỈNH CÔNG NỢ NCC (không tạo từ báo có): khi GỬI DUYỆT, tổng các dòng đến phải BẰNG "
     "CHÍNH XÁC số tiền điều chỉnh từ. Khi chỉ Lưu nháp thì KHÔNG kiểm ràng buộc này.\n"
     "- Phiếu ĐIỀU CHỈNH CÔNG NỢ NCC tạo từ Phiếu báo có: khi gửi duyệt chỉ cần KHÔNG LỚN HƠN, không "
     "bắt buộc bằng.\n"
     "- Mỗi ô \"Số tiền\" của dòng điều chỉnh đến phải LỚN HƠN 0. Số tiền điều chỉnh từ phải từ 0 trở lên.\n"
     "- KHÔNG cho hợp đồng \"Điều chỉnh đến\" trùng với hợp đồng \"Điều chỉnh từ\" trong cùng một dòng.\n"
     "- Cột \"Số tiền\" ngoài danh sách là tổng tiền của cả phiếu, hiển thị không có phần thập phân.\n"
     "- Hai ô lọc \"Số tiền từ - đến\" so với chính cột Số tiền này.\n"
     "- Số dư công nợ đọc từ sổ kế toán: phiếu khách hàng lấy tài khoản Phải thu khách hàng, phiếu NCC "
     "lấy tài khoản Phải trả nhà cung cấp."),

    ("7. Phân quyền cấp",
     "Năm quyền liên quan tới màn hình này:\n"
     "1. \"Xem tất cả phiếu yêu cầu điều chỉnh của tổng công ty\" — thấy phiếu của mọi công ty.\n"
     "2. \"Xem tất cả phiếu yêu cầu điều chỉnh của công ty\" — chỉ phiếu thuộc công ty mình.\n"
     "3. \"Xem tất cả phiếu yêu cầu điều chỉnh của phòng ban\" — phiếu thuộc các phòng ban mình được "
     "phân công quản lý, CỘNG THÊM phiếu do chính mình lập.\n"
     "4. \"Xem tất cả phiếu yêu cầu điều chỉnh của bộ phận\" — phiếu thuộc các bộ phận mình được phân "
     "công quản lý, CỘNG THÊM phiếu do chính mình lập.\n"
     "5. \"Kế toán thanh toán\" — vào được màn Phiếu yêu cầu điều chỉnh công nợ chờ duyệt, bấm được "
     "\"Tạo phiếu kế toán\" và \"Không duyệt\".\n"
     "Bốn quyền xem xét theo THỨ TỰ TRÊN XUỐNG; ai không có quyền nào trong bốn quyền trên thì chỉ thấy "
     "phiếu do chính mình lập.\n"
     "Tài khoản có vai trò Super Admin luôn mở được chi tiết mọi phiếu.\n"
     "⚠️ Chỉ đường dẫn màn Chờ duyệt được hệ thống chặn bằng quyền \"Kế toán thanh toán\". Các chức "
     "năng tạo / sửa / xóa / in / xuất Excel KHÔNG gắn quyền ở phía hệ thống, chỉ ẩn hiện nút trên "
     "giao diện. Riêng chức năng Không duyệt CÓ kiểm tra quyền và trạng thái ở phía hệ thống — điểm "
     "này chặt hơn hai màn Đề nghị thu tiền và Đề nghị thanh toán."),

    ("8. Cách tính các ô thống kê",
     "- Ô \"Hiển thị a đến b trong tổng số N\" dưới bảng: a là dòng đầu trang đang xem, b là dòng cuối, "
     "N là tổng số phiếu khớp bộ lọc trong phạm vi chế độ đang mở.\n"
     "- Ô \"Số dòng mỗi trang\": mặc định 10; đổi số dòng thì bảng quay về trang 1.\n"
     "- Cột STT đánh liên tục theo trang: trang 2 với 10 dòng mỗi trang bắt đầu từ 11.\n"
     "- Cột \"Số tiền\": tổng tiền của phiếu, có dấu chấm ngăn nghìn, KHÔNG có phần thập phân.\n"
     "- Cột \"Ngày lập\" và \"Ngày nhận\" hiển thị dạng ngày/tháng/năm, không có giờ. \"Ngày nhận\" là "
     "thời điểm người lập bấm Lưu và gửi duyệt; phiếu còn nháp thì ô này trống.\n"
     "- Cột \"Số dư\" trong form đọc từ sổ kế toán của chính hợp đồng đó, TÍNH LẠI mỗi lần mở phiếu, "
     "KHÔNG lưu trong phiếu.\n"
     "- Với phiếu NCC dùng ngoại tệ, cột Số dư và cột Số tiền tách làm hai: một cột nguyên tệ và một "
     "cột quy đổi VNĐ theo tỷ giá của phiếu.\n"
     "- Tệp Excel danh sách xuất ra 12 cột theo đúng bộ lọc đang áp dụng trên màn."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất của màn này — đọc trước khi chạy test:\n"
     "1. ⚠️ QUY TẮC SỐ TIỀN KHÁC NHAU GIỮA HAI LOẠI PHIẾU (mục 6): khách hàng cho phép tổng đến NHỎ "
     "HƠN từ; NCC bắt buộc BẰNG khi gửi duyệt. Đừng lấy kết quả của loại này suy ra loại kia.\n"
     "2. ⚠️ Phiếu NCC lưu NHÁP thì không kiểm ràng buộc bằng nhau, nhưng bấm Gửi duyệt mới báo lỗi. "
     "Phải test cả hai nút.\n"
     "3. ⚠️ Chế độ danh sách \"Đã xử lý\" đang lấy dữ liệu của màn Phiếu đề nghị thu tiền chứ không "
     "phải của màn này — mở ra sẽ thấy phiếu đề nghị thu tiền với các cột lệch nhau. Ghi nhận Failed. "
     "Chế độ này cũng không có mục menu nào trỏ tới.\n"
     "4. ⚠️ Ô lọc \"Hợp đồng\" ở màn Chờ duyệt không có tác dụng: gõ gì vào cũng ra nguyên kết quả cũ. "
     "Hai ô \"Hợp đồng điều chỉnh từ\" và \"Hợp đồng điều chỉnh đến\" ở màn danh sách thì chạy đúng.\n"
     "5. ⚠️ Nút Sửa / Xóa hiện với MỌI phiếu ở trạng thái Đang tạo, kể cả phiếu của người khác nếu "
     "nhìn thấy được; còn phiếu Từ chối thì chỉ người lập mới thấy nút. Hai trạng thái hành xử khác "
     "nhau — đây là lỗi, không phải thiết kế.\n"
     "6. ⚠️ Xóa phiếu không kiểm tra quyền và không kiểm tra trạng thái ở phía hệ thống; ngoài ra xóa "
     "phiếu KHÔNG xóa theo các dòng chi tiết.\n"
     "7. ⚠️ Bấm \"Không duyệt\" KHÔNG gửi thông báo cho người lập. Người lập phải tự vào xem mới biết.\n"
     "8. ⚠️ Tệp Excel của MỘT phiếu luôn mang cùng một tên (không kèm mã phiếu), tải nhiều phiếu liên "
     "tiếp sẽ ghi đè hoặc bị đánh số trùng trong thư mục tải về.\n"
     "9. ⚠️ Phần đầu trang của tệp Excel danh sách lấy theo công ty của NGƯỜI ĐANG ĐĂNG NHẬP, không "
     "phải công ty của các phiếu trong danh sách. Khi người xem tổng công ty xuất danh sách nhiều công "
     "ty thì đầu trang chỉ ghi một công ty.\n"
     "10. ⚠️ Cửa sổ chọn hợp đồng ở cột Điều chỉnh từ chỉ hiện hợp đồng do CHÍNH NGƯỜI ĐANG ĐĂNG NHẬP "
     "lập. Không thấy hợp đồng thường là vì hợp đồng của người khác.\n"
     "11. ⚠️ Ô \"Đến ngày\" của bộ lọc làm rụng trọn ngày cuối (mục 4).\n"
     "12. ⚠️ Cảnh báo \"Số tiền điều chỉnh vào hợp đồng không có nợ!\" chỉ là hỏi xác nhận, bấm Xác "
     "nhận vẫn đi tiếp được. Đừng nhầm với lỗi chặn.\n"
     "13. Bộ lọc được ghi nhớ RIÊNG cho từng chế độ danh sách; test xong nhớ bấm nút làm mới bộ lọc "
     "trước khi sang ca test khác."),
]

# ============================================================ TC PHAN QUYEN
ROLE_TCS = [
    ("00", "Tài khoản không có quyền xem nào chỉ thấy phiếu do chính mình lập", "P0",
     "Tài khoản NV-A không được gán quyền nào trong 4 quyền xem theo cấp; NV-A đã lập 12 phiếu; công ty "
     "của NV-A có hơn 80 phiếu của nhiều người",
     "1. Đăng nhập bằng NV-A\n"
     "2. Mở menu Công nợ - Thu - Chi, bấm mục Phiếu yêu cầu điều chỉnh công nợ\n"
     "3. Đọc số tổng dưới bảng\n"
     "4. Lật hết các trang, soát cột Người lập",
     "Tài khoản: NV-A (không quyền xem theo cấp)",
     "- Vào được màn hình, không bị chặn\n"
     "- Tổng hiện đúng 12\n"
     "- Mọi dòng đều có Người lập là NV-A\n"
     "- Nút Tạo mới VẪN hiển thị (hành vi lập phiếu không gắn quyền)"),

    ("01", "Quyền xem của tổng công ty thấy phiếu của mọi công ty", "P0",
     "Tài khoản B chỉ có quyền \"Xem tất cả phiếu yêu cầu điều chỉnh của tổng công ty\"; hệ thống có "
     "phiếu của ít nhất 3 công ty",
     "1. Đăng nhập bằng B, mở mục Phiếu yêu cầu điều chỉnh công nợ trên menu\n"
     "2. Bấm nút Bộ lọc, ghi lại các ô lọc theo đơn vị\n"
     "3. Chọn lần lượt từng Công ty rồi bấm nút tìm kiếm",
     "Quyền: Xem tất cả phiếu yêu cầu điều chỉnh của tổng công ty",
     "- Khối lọc hiện CẢ ô Công ty và ô Phòng ban\n"
     "- Chọn công ty nào ra phiếu của công ty đó\n"
     "- Bỏ chọn công ty thì thấy phiếu của cả 3 công ty"),

    ("02", "Quyền xem của công ty chỉ thấy phiếu công ty mình", "P0",
     "Tài khoản C chỉ có quyền \"Xem tất cả phiếu yêu cầu điều chỉnh của công ty\", thuộc công ty 3; "
     "công ty 3 có 40 phiếu, công ty 1 có 300 phiếu",
     "1. Đăng nhập bằng C, mở mục Phiếu yêu cầu điều chỉnh công nợ\n"
     "2. Bấm nút Bộ lọc, ghi lại các ô lọc theo đơn vị\n"
     "3. Đọc số tổng và soát cột Phòng ban",
     "Quyền: Xem tất cả phiếu yêu cầu điều chỉnh của công ty",
     "- Khối lọc KHÔNG có ô Công ty, chỉ có ô Phòng ban\n"
     "- Tổng bằng 40 trừ đi số phiếu nháp của người khác trong công ty 3\n"
     "- Không có phiếu nào của công ty 1"),

    ("03", "Quyền xem của phòng ban thấy thêm phiếu của chính mình", "P0",
     "Tài khoản D chỉ có quyền \"Xem tất cả phiếu yêu cầu điều chỉnh của phòng ban\", quản lý phòng P1; "
     "phòng P1 có 8 phiếu; D thuộc phòng P2 và tự lập 3 phiếu ở phòng P2",
     "1. Đăng nhập bằng D, mở mục Phiếu yêu cầu điều chỉnh công nợ\n"
     "2. Đọc số tổng\n"
     "3. Soát cột Phòng ban và cột Người lập của mọi dòng",
     "Quyền: Xem tất cả phiếu yêu cầu điều chỉnh của phòng ban",
     "- Hiện 8 phiếu của phòng P1 CỘNG THÊM 3 phiếu của chính D ở phòng P2\n"
     "- ⚠️ Điểm khác biệt của màn này: nhánh phòng ban và bộ phận LUÔN kèm thêm phiếu của chính mình, "
     "khác hai màn Đề nghị thu tiền và Đề nghị thanh toán"),

    ("04", "Quyền xem của bộ phận thấy thêm phiếu của chính mình", "P1",
     "Tài khoản E chỉ có quyền \"Xem tất cả phiếu yêu cầu điều chỉnh của bộ phận\", quản lý 1 bộ phận; "
     "E cũng tự lập vài phiếu ở bộ phận khác",
     "1. Đăng nhập bằng E, mở mục Phiếu yêu cầu điều chỉnh công nợ\n"
     "2. Đọc số tổng và soát danh sách",
     "Quyền: Xem tất cả phiếu yêu cầu điều chỉnh của bộ phận",
     "- Hiện phiếu của bộ phận được phân công CỘNG THÊM phiếu do chính E lập\n"
     "- ⚠️ Khối lọc KHÔNG hiện ô Công ty / Phòng ban / Bộ phận cho mức quyền này"),

    ("05", "Có nhiều quyền xem cùng lúc thì lấy phạm vi rộng nhất", "P1",
     "Tài khoản F có ĐỒNG THỜI quyền xem của tổng công ty và quyền xem của bộ phận",
     "1. Đăng nhập bằng F, mở mục Phiếu yêu cầu điều chỉnh công nợ\n"
     "2. Đọc số tổng, so với số của tài khoản B ở TC-ROLE-01",
     "—",
     "- Tổng bằng đúng số của tài khoản chỉ có quyền tổng công ty\n"
     "- Không bị thu hẹp về phạm vi bộ phận"),

    ("06", "Kế toán thanh toán vào được màn chờ duyệt", "P0",
     "Tài khoản KT-1 có quyền \"Kế toán thanh toán\", thuộc công ty 3; công ty 3 có 3 phiếu ở Chờ tạo "
     "phiếu kế toán, công ty 1 có 9 phiếu ở cùng trạng thái",
     "1. Đăng nhập bằng KT-1\n"
     "2. Mở nhóm menu phê duyệt, bấm mục Phiếu yêu cầu điều chỉnh công nợ chờ duyệt\n"
     "3. Đọc số tổng, cột Trạng thái và bộ nút phía trên bảng",
     "Quyền: Kế toán thanh toán",
     "- Mục menu HIỂN THỊ\n"
     "- Đúng 3 dòng, tất cả đều Chờ tạo phiếu kế toán, người lập thuộc công ty 3\n"
     "- KHÔNG thấy 9 phiếu của công ty 1\n"
     "- Phía trên bảng chỉ có nút Bộ lọc, KHÔNG có nút Tạo mới và KHÔNG có nút Xuất excel"),

    ("07", "Không có quyền Kế toán thanh toán thì bị chặn ở màn chờ duyệt", "P0",
     "Tài khoản NV-A, không có quyền \"Kế toán thanh toán\"",
     "1. Đăng nhập bằng NV-A\n"
     "2. Tìm mục Phiếu yêu cầu điều chỉnh công nợ chờ duyệt trên menu\n"
     "3. Dán thẳng đường dẫn màn chờ duyệt vào thanh địa chỉ",
     "—",
     "- Mục menu KHÔNG hiển thị\n"
     "- Dán thẳng đường dẫn: hệ thống từ chối, báo không có quyền, không hiện dữ liệu phiếu nào"),

    ("08", "Màn chờ duyệt lọc theo công ty của NGƯỜI LẬP", "P1",
     "KT-1 thuộc công ty 3; có phiếu do một nhân viên công ty 1 lập nhưng phiếu đó ghi nhận công ty 3 "
     "(dữ liệu cũ, nếu không dựng được thì ghi Không áp dụng)",
     "1. Mở màn chờ duyệt bằng KT-1\n"
     "2. Soát cột Người lập của mọi dòng, đối chiếu công ty của từng người",
     "—",
     "- Chỉ hiện phiếu mà NGƯỜI LẬP thuộc công ty 3\n"
     "- ⚠️ Màn này lọc theo công ty của người lập, không lọc theo cột công ty ghi trên phiếu — nếu hai "
     "thứ lệch nhau thì kết quả có thể khác kỳ vọng, ghi nhận lại"),

    ("09", "Phiếu nháp của người khác bị ẩn ở chế độ Tất cả", "P0",
     "Tài khoản B có quyền xem tổng công ty; NV-A vừa Lưu nháp 1 phiếu mã kết thúc .00021",
     "1. Đăng nhập bằng B, mở mục Phiếu yêu cầu điều chỉnh công nợ\n"
     "2. Bấm Bộ lọc, gõ .00021 vào ô Mã phiếu, tìm kiếm\n"
     "3. Xóa ô mã, chọn Trạng thái = Đang tạo, tìm lại",
     "—",
     "- Tìm theo mã: không ra dòng nào\n"
     "- Lọc Đang tạo: chỉ ra phiếu nháp của chính B\n"
     "- ⚠️ Quy tắc cố định, KHÔNG ghi Failed"),

    ("10", "Mở chi tiết phiếu ngoài phạm vi quyền bị chặn", "P0",
     "Tài khoản NV-A (không quyền xem theo cấp, không phải kế toán); lấy đường dẫn chi tiết của 1 phiếu "
     "do người khác lập, trạng thái Đã duyệt phiếu kế toán",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dán đường dẫn chi tiết phiếu đó vào thanh địa chỉ",
     "—",
     "- Hệ thống hiện trang báo không tìm thấy nội dung\n"
     "- Không hiển thị bất kỳ dữ liệu nào của phiếu"),

    ("11", "Người đã duyệt vẫn xem lại được phiếu", "P1",
     "KT-1 đã xử lý 1 phiếu của người khác; KT-1 không có quyền xem theo cấp nào",
     "1. Đăng nhập bằng KT-1\n"
     "2. Dán thẳng đường dẫn chi tiết phiếu đã từng xử lý",
     "—",
     "- Mở được chi tiết bình thường\n"
     "- Không có nút Tạo phiếu kế toán và Không duyệt (phiếu đã rời trạng thái chờ)"),

    ("12", "Kế toán thanh toán mở được phiếu chờ duyệt dù không có quyền xem theo cấp", "P0",
     "KT-2 chỉ có quyền \"Kế toán thanh toán\", không có quyền xem theo cấp; phiếu X đang ở Chờ tạo "
     "phiếu kế toán, do người khác lập cùng công ty",
     "1. Mở màn chờ duyệt bằng KT-2, bấm Mã phiếu X\n"
     "2. Quan sát hàng nút\n"
     "3. Mở màn danh sách chế độ Tất cả, đọc số tổng",
     "—",
     "- ⚠️ Điểm cần kiểm kỹ: mở chi tiết phiếu X có vào được hay hiện trang báo không tìm thấy. Nếu "
     "không vào được trong khi dòng vẫn hiện ở màn chờ duyệt thì ghi Failed kèm ảnh chụp\n"
     "- Màn danh sách chế độ Tất cả: KT-2 chỉ thấy phiếu do chính mình lập"),

    ("13", "Bỏ qua giao diện gọi thẳng chức năng Xóa phiếu của người khác", "P0",
     "Tài khoản NV-A; đường dẫn xóa của 1 phiếu trạng thái Đã duyệt phiếu kế toán do người khác lập; "
     "đã sao lưu dữ liệu trước khi test",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dán thẳng đường dẫn xóa của phiếu đó\n"
     "3. Kiểm tra phiếu còn hay mất",
     "—",
     "- ⚠️ Hiện trạng: phiếu BỊ XÓA, hệ thống báo xóa thành công. LỖ HỔNG, ghi nhận Failed\n"
     "- Kỳ vọng đúng: từ chối và giữ nguyên phiếu\n"
     "- Khôi phục dữ liệu ngay sau khi test"),

    ("14", "Bỏ qua giao diện gọi thẳng chức năng Sửa phiếu của người khác", "P0",
     "Tài khoản NV-A; 1 phiếu trạng thái Chờ tạo phiếu kế toán do người khác lập",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dán thẳng đường dẫn màn Sửa của phiếu đó\n"
     "3. Nếu mở được, sửa Diễn giải rồi bấm Lưu\n"
     "4. Kiểm tra lại nội dung phiếu",
     "—",
     "- ⚠️ Hiện trạng: màn Sửa MỞ ĐƯỢC và lưu được đè lên phiếu, đồng thời đẩy phiếu về trạng thái "
     "Đang tạo. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: từ chối ngay khi mở màn Sửa"),

    ("15", "Chức năng Không duyệt có kiểm tra quyền ở phía hệ thống", "P0",
     "Tài khoản NV-A không có quyền \"Kế toán thanh toán\"; 1 phiếu đang ở Chờ tạo phiếu kế toán",
     "1. Đăng nhập bằng NV-A, lấy phiên đăng nhập\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng đổi trạng thái phiếu sang Từ chối kèm lý do\n"
     "3. Mở lại phiếu, đọc Trạng thái",
     "—",
     "- Hệ thống TỪ CHỐI, trả về thông báo \"Không có quyền!\"\n"
     "- Trạng thái phiếu KHÔNG đổi\n"
     "- ⚠️ Đây là điểm màn này làm ĐÚNG, chặt hơn hai màn Đề nghị thu tiền và Đề nghị thanh toán"),

    ("16", "Không duyệt phiếu đã rời trạng thái chờ", "P1",
     "KT-1 có quyền kế toán thanh toán; 1 phiếu đã ở Đã tạo phiếu kế toán",
     "1. Mở chi tiết phiếu đó, quan sát hàng nút\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng đổi trạng thái sang Từ chối",
     "—",
     "- Giao diện KHÔNG có nút Tạo phiếu kế toán và Không duyệt\n"
     "- Gọi thẳng: hệ thống trả về \"Không có quyền!\", trạng thái phiếu không đổi"),

    ("17", "In và Xuất Excel phiếu của người khác không bị chặn", "P1",
     "Tài khoản NV-A; đường dẫn in và đường dẫn xuất Excel của 1 phiếu ở công ty khác",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dán thẳng đường dẫn in của phiếu đó\n"
     "3. Dán thẳng đường dẫn xuất Excel một phiếu",
     "—",
     "- ⚠️ Hiện trạng: bản in hiện đầy đủ và tệp Excel tải về được. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: kiểm tra quyền xem trước khi cho in và xuất"),

    ("18", "Xuất Excel danh sách bị giới hạn theo phạm vi quyền", "P0",
     "Tài khoản C chỉ có quyền xem theo công ty (công ty 3)",
     "1. Mở màn danh sách chế độ Tất cả, không đặt bộ lọc\n"
     "2. Bấm nút Xuất excel\n"
     "3. Mở tệp, đếm số dòng và soát cột Phòng ban",
     "—",
     "- Số dòng trong tệp bằng đúng số tổng trên màn\n"
     "- Không có phiếu của công ty khác lọt vào tệp\n"
     "- ⚠️ Nếu tệp chứa phiếu ngoài phạm vi quyền thì ghi Failed"),
]
