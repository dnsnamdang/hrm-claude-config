# -*- coding: utf-8 -*-
"""Section IV — tao moi / sua / xem chi tiet."""

SEC_IV = [
    ("001", "Bố cục màn Tạo mới", "P0",
     "Tài khoản bất kỳ, đang ở màn danh sách",
     "1. Bấm nút Tạo mới\n"
     "2. Quan sát toàn màn",
     "—",
     "- Khối \"Thông tin chung\": Ngày lập (khóa, điền sẵn hôm nay), Người lập (khóa, điền sẵn tên "
     "người đăng nhập), Ghi chú, khối File đính kèm (PDF) có dấu bắt buộc\n"
     "- Khối \"Chi tiết\": góc phải có ô chọn \"Xem tồn\", bảng hàng hóa có 7 cột: STT, Hàng hóa, ĐVT, "
     "Giá niêm yết, SL tồn, Khách hàng, cột nút\n"
     "- Bảng chưa có dòng nào, hiện dòng chữ \"Chưa có hàng hóa\"\n"
     "- Dưới cùng có 3 nút: Lưu, Lưu & Gửi, Hủy"),

    ("002", "Thêm hàng hóa bằng cửa sổ tìm hàng", "P0",
     "Đang ở màn Tạo mới, bảng chi tiết còn trống",
     "1. Bấm nút dấu cộng ở tiêu đề cột cuối bảng\n"
     "2. Quan sát cửa sổ tìm hàng hóa\n"
     "3. Tìm và chọn hàng hóa HH-001\n"
     "4. Quan sát dòng vừa thêm",
     "Hàng hóa: HH-001",
     "- Cửa sổ tìm hàng hóa mở ra, tìm được theo mã và tên\n"
     "- Chọn xong hiện thông báo xanh \"Thêm thành công\"\n"
     "- Dòng mới hiện: tên hàng hóa, dòng Model, dòng Mã hàng, ô chọn ĐVT, Giá niêm yết, SL tồn"),

    ("003", "Không cho chọn trùng hàng hóa", "P0",
     "Bảng chi tiết đã có hàng hóa HH-001",
     "1. Bấm dấu cộng, chọn lại chính HH-001\n"
     "2. Quan sát",
     "—",
     "- Hiện cảnh báo vàng \"Hàng hóa đã được chọn!\"\n"
     "- Bảng KHÔNG thêm dòng thứ hai cho HH-001"),

    ("004", "Xóa dòng hàng hóa", "P0",
     "Bảng chi tiết có 3 hàng hóa, hàng hóa thứ 2 đã nhập 2 dòng khách hàng",
     "1. Bấm nút dấu trừ ở cột cuối của dòng hàng hóa thứ 2\n"
     "2. Đếm số dòng và soát dữ liệu 2 dòng còn lại",
     "—",
     "- Dòng hàng hóa thứ 2 biến mất cùng toàn bộ dòng khách hàng của nó\n"
     "- Còn 2 dòng, STT đánh lại 1 và 2, dữ liệu không xáo trộn\n"
     "- Xóa KHÔNG hỏi xác nhận"),

    ("005", "Chọn đơn vị tính và giá niêm yết đổi theo", "P0",
     "Hàng hóa HH-001 có 2 đơn vị tính: Cái (hệ số 1) và Thùng (hệ số 10), giá khác nhau",
     "1. Mở ô ĐVT của dòng hàng hóa, ghi lại các lựa chọn\n"
     "2. Chọn Cái, đọc Giá niêm yết\n"
     "3. Đổi sang Thùng, đọc lại Giá niêm yết",
     "Cái → Thùng",
     "- Ô ĐVT liệt kê các đơn vị của hàng hóa, đơn vị có hệ số khác 1 hiện kèm hệ số trong ngoặc "
     "(ví dụ \"Thùng (x10)\")\n"
     "- Giá niêm yết đổi theo đơn vị đang chọn"),

    ("006", "Ô Xem tồn và cột SL tồn", "P0",
     "Bảng chi tiết đã có 2 hàng hóa; hệ thống có nhiều kho",
     "1. Quan sát cột SL tồn khi CHƯA chọn kho ở ô Xem tồn\n"
     "2. Chọn một kho ở ô Xem tồn\n"
     "3. Đổi sang kho khác\n"
     "4. Bỏ chọn kho",
     "—",
     "- Chưa chọn kho: cột SL tồn hiện dấu gạch ngang\n"
     "- Chọn kho: cột SL tồn hiện số tồn của kho đó cho từng hàng hóa\n"
     "- Đổi kho: số cập nhật lại theo kho mới\n"
     "- Bỏ chọn: số về 0 hoặc dấu gạch ngang"),

    ("007", "Thêm hàng hóa sau khi đã chọn kho xem tồn", "P1",
     "Đã chọn kho ở ô Xem tồn, bảng có 1 hàng hóa",
     "1. Bấm dấu cộng, thêm hàng hóa mới\n"
     "2. Đọc cột SL tồn của dòng vừa thêm",
     "—",
     "- Dòng mới cũng có SL tồn theo kho đang chọn, không phải bấm lại ô Xem tồn"),

    ("008", "Thêm và xóa dòng khách hàng trong một hàng hóa", "P0",
     "Bảng có 1 hàng hóa, chưa có dòng khách hàng nào",
     "1. Bấm nút \"Thêm khách hàng\" 3 lần\n"
     "2. Đếm số dòng khách hàng\n"
     "3. Bấm nút dấu nhân ở dòng khách hàng thứ 2\n"
     "4. Thêm hàng hóa thứ hai và kiểm dòng khách hàng của nó",
     "—",
     "- Mỗi lần bấm thêm 1 dòng khách hàng gồm: ô Khách hàng, ô SL, ô Ngày cần, ô Ghi chú\n"
     "- Xóa dòng 2 thì còn 2 dòng, dữ liệu không xáo trộn\n"
     "- Hàng hóa thứ hai có danh sách dòng khách hàng RIÊNG, không ảnh hưởng lẫn nhau"),

    ("009", "Chọn khách hàng cho dòng chi tiết", "P0",
     "Đã có 1 dòng khách hàng trống",
     "1. Bấm kính lúp ở ô Khách hàng\n"
     "2. Quan sát cửa sổ tìm khách hàng\n"
     "3. Tìm và chọn KH-001\n"
     "4. Bấm kính lúp ở dòng khách hàng thứ hai và chọn KH-002",
     "—",
     "- Cửa sổ tìm khách hàng mở ra, tìm được theo mã và tên\n"
     "- Chọn xong ô hiện tên khách hàng, ô này chỉ đọc (chỉ chọn qua cửa sổ)\n"
     "- Hai dòng giữ hai khách hàng khác nhau, chọn dòng sau không ghi đè dòng trước"),

    ("010", "Cho phép cùng một khách hàng ở nhiều dòng", "P1",
     "Hàng hóa HH-001 đã có 1 dòng khách hàng KH-001, ngày cần 20/09/2026",
     "1. Thêm dòng khách hàng thứ hai, cũng chọn KH-001, ngày cần 25/09/2026\n"
     "2. Nhập số lượng cho cả hai dòng\n"
     "3. Bấm Lưu, mở lại phiếu",
     "KH-001 hai lần, hai ngày cần khác nhau",
     "- Hệ thống KHÔNG chặn, KHÔNG cảnh báo trùng\n"
     "- Lưu được, mở lại thấy đủ 2 dòng của cùng khách hàng\n"
     "- ⚠️ Chỉ HÀNG HÓA mới bị cấm trùng, khách hàng thì không — đừng báo lỗi ở đây"),

    ("011", "Dòng Tổng cộng cộng đúng số lượng", "P0",
     "Hàng hóa HH-001 có 3 dòng khách hàng",
     "1. Nhập số lượng lần lượt 5, 10, 20\n"
     "2. Đọc dòng Tổng cộng ngay dưới danh sách khách hàng\n"
     "3. Sửa dòng 2 thành 15, đọc lại",
     "5 + 10 + 20",
     "- Tổng cộng hiện 35\n"
     "- Sau khi sửa: hiện 40\n"
     "- Số cập nhật ngay khi gõ, không phải bấm nút nào\n"
     "- Mỗi hàng hóa có dòng Tổng cộng RIÊNG"),

    ("012", "Đính kèm tệp PDF", "P0",
     "Đang ở màn Tạo mới",
     "1. Bấm biểu tượng dấu cộng ở khối File đính kèm\n"
     "2. Chọn 1 tệp PDF hợp lệ\n"
     "3. Thêm ô nữa và chọn tệp PDF thứ hai\n"
     "4. Bấm nút dấu nhân trên một ô để bỏ tệp",
     "2 tệp PDF",
     "- Mỗi lần bấm dấu cộng thêm một ô chọn tệp\n"
     "- Sau khi chọn, ô hiện đúng tên tệp và biểu tượng đổi thành biểu tượng PDF\n"
     "- Bấm dấu nhân thì ô đó biến mất, tệp không được tải lên\n"
     "- Nhãn khối ghi rõ \"File đính kèm (PDF)\" kèm dấu bắt buộc"),

    ("013", "Lưu nháp phiếu hợp lệ", "P0",
     "Màn Tạo mới đã điền: Ghi chú \"Chuyển hàng cho khách miền Bắc\", 1 tệp PDF, 1 hàng hóa với 2 dòng "
     "khách hàng đầy đủ (SL, ngày cần sau hôm nay, ghi chú)",
     "1. Bấm nút Lưu\n"
     "2. Đọc thông báo\n"
     "3. Quan sát trang sau khi lưu, tìm phiếu vừa tạo",
     "—",
     "- Thông báo \"Yêu cầu của bạn đã được lưu. Bạn cần gửi để yêu cầu được xử lý\"\n"
     "- Phiếu mới ở đầu danh sách, trạng thái Đang tạo\n"
     "- Cột Người tiếp nhận và Ngày tiếp nhận TRỐNG\n"
     "- Mã yêu cầu sinh tự động dạng PYCCH- kèm 5 chữ số"),

    ("014", "Lưu và Gửi", "P0",
     "Màn Tạo mới đã điền hợp lệ như TC_04.013; KT-1 có quyền Kế toán kho cùng công ty",
     "1. Bấm nút Lưu & Gửi\n"
     "2. Đọc thông báo\n"
     "3. Tìm phiếu vừa tạo, đọc Trạng thái\n"
     "4. Đăng nhập KT-1, mở chuông thông báo và màn Chờ duyệt",
     "—",
     "- ⚠️ KHÔNG có hộp thoại xác nhận trước khi lưu\n"
     "- Thông báo \"Yêu cầu của bạn đã được gửi\"\n"
     "- Phiếu ở trạng thái Chờ duyệt, không còn mục Sửa và Xóa trong menu hành động\n"
     "- KT-1 nhận thông báo \"<tên người lập> vừa tạo yêu cầu chuyển hàng: <mã>\" và thấy phiếu trong "
     "màn Chờ duyệt"),

    ("015", "Thông báo chỉ gửi cho kế toán kho cùng công ty", "P1",
     "NV-A thuộc công ty 3; KT-1 là kế toán kho công ty 3; KT-9 là kế toán kho công ty 1",
     "1. NV-A bấm Lưu & Gửi một phiếu\n"
     "2. Kiểm chuông thông báo của KT-1 và KT-9\n"
     "3. Bấm vào thông báo của KT-1",
     "—",
     "- KT-1 nhận được thông báo\n"
     "- KT-9 KHÔNG nhận được\n"
     "- Bấm vào thông báo mở đúng màn chi tiết phiếu"),

    ("016", "Nút Hủy rời màn không có cảnh báo", "P2",
     "Màn Tạo mới, đã nhập Ghi chú và 1 hàng hóa, chưa lưu",
     "1. Bấm nút Hủy",
     "—",
     "- Về màn danh sách chế độ Tất cả\n"
     "- ⚠️ KHÔNG có cảnh báo \"thông tin chưa lưu\", dữ liệu mất hẳn. Ghi nhận đúng hiện trạng"),

    ("017", "Bố cục màn Sửa", "P0",
     "Phiếu P trạng thái Đang tạo do chính người đăng nhập lập, có 2 hàng hóa và 1 tệp đính kèm",
     "1. Mở menu hành động dòng phiếu P, bấm Sửa yêu cầu\n"
     "2. Quan sát khối Thông tin chung và khối File đính kèm",
     "—",
     "- Ngày lập hiện ngày lập gốc của phiếu, Người lập hiện tên người lập gốc\n"
     "- Dữ liệu cũ nạp đủ: Ghi chú, 2 hàng hóa cùng các dòng khách hàng\n"
     "- Khối File đính kèm liệt kê tệp đã lưu, mỗi tệp có nút xóa riêng và mở xem được\n"
     "- Vẫn có 3 nút Lưu, Lưu & Gửi, Hủy"),

    ("018", "Xóa tệp đính kèm ở màn Sửa", "P1",
     "Phiếu P đang mở màn Sửa, có 2 tệp đính kèm",
     "1. Bấm nút xóa ở tệp thứ nhất\n"
     "2. Quan sát danh sách tệp\n"
     "3. Tải lại màn Sửa",
     "—",
     "- Tệp bị gỡ khỏi danh sách, hiện thông báo xóa thành công\n"
     "- Tải lại vẫn còn 1 tệp\n"
     "- Phiếu vẫn lưu được dù đã xóa hết tệp (khi sửa không bắt buộc tệp)"),

    ("019", "Sửa phiếu và lưu lại", "P0",
     "Phiếu P trạng thái Đang tạo, 2 hàng hóa",
     "1. Đổi Ghi chú\n"
     "2. Xóa hàng hóa thứ 2, thêm hàng hóa khác với 1 dòng khách hàng\n"
     "3. Sửa số lượng một dòng khách hàng của hàng hóa thứ 1\n"
     "4. Bấm Lưu, mở lại phiếu P",
     "—",
     "- Thông báo \"Yêu cầu của bạn đã được lưu. Bạn cần gửi để yêu cầu được xử lý\"\n"
     "- Mở lại thấy Ghi chú mới và đúng 2 hàng hóa như vừa sửa\n"
     "- Mã yêu cầu và Người lập KHÔNG đổi\n"
     "- Trạng thái vẫn là Đang tạo"),

    ("020", "Sửa rồi gửi duyệt", "P0",
     "Phiếu P trạng thái Đang tạo do chính người đăng nhập lập",
     "1. Mở màn Sửa, chỉnh nội dung\n"
     "2. Bấm Lưu & Gửi\n"
     "3. Kiểm trạng thái phiếu và chuông thông báo của kế toán kho",
     "—",
     "- Thông báo \"Yêu cầu của bạn đã được gửi\"\n"
     "- Phiếu chuyển sang Chờ duyệt\n"
     "- Kế toán kho nhận thông báo mới"),

    ("021", "Không sửa được phiếu đã gửi", "P0",
     "Phiếu R do chính người đăng nhập lập, đang ở Chờ duyệt",
     "1. Tìm phiếu R, mở menu hành động\n"
     "2. Mở màn chi tiết phiếu R, quan sát hàng nút\n"
     "3. Dán thẳng đường dẫn màn Sửa của phiếu R",
     "—",
     "- Menu chỉ có In yêu cầu\n"
     "- Màn chi tiết chỉ có nút Quay lại\n"
     "- Dán thẳng đường dẫn Sửa: ra trang báo không tìm thấy nội dung"),

    ("022", "Sửa lại phiếu sau khi bị Không duyệt", "P0",
     "Phiếu Q do chính người đăng nhập lập, vừa bị kế toán kho bấm Không duyệt nên đã quay về Đang tạo",
     "1. Mở màn danh sách, tìm phiếu Q, đọc cột Trạng thái, Người tiếp nhận, Ngày tiếp nhận\n"
     "2. Mở chi tiết, đọc khối Ghi chú duyệt\n"
     "3. Mở menu hành động, bấm Sửa yêu cầu\n"
     "4. Chỉnh nội dung, bấm Lưu & Gửi",
     "—",
     "- Trạng thái là Đang tạo; cột Người tiếp nhận và Ngày tiếp nhận VẪN có dữ liệu của lần bị từ chối\n"
     "- Khối Ghi chú duyệt hiện lý do từ chối ở dạng chỉ đọc\n"
     "- Mục Sửa yêu cầu và Xóa yêu cầu hiện lại\n"
     "- Sau khi Lưu & Gửi, phiếu quay lại Chờ duyệt và xuất hiện lại ở màn Chờ duyệt của kế toán kho"),

    ("023", "Bố cục màn Chi tiết", "P0",
     "Phiếu S trạng thái Đã tiếp nhận do chính người đăng nhập lập, có 2 hàng hóa",
     "1. Bấm Mã yêu cầu để mở chi tiết\n"
     "2. Quan sát toàn màn",
     "—",
     "- Thông tin chung và bảng chi tiết chỉ hiển thị, mọi ô khóa\n"
     "- Bảng gộp dòng: mỗi hàng hóa chiếm một khối, bên dưới liệt kê từng dòng khách hàng với Khách "
     "hàng, SL, Ngày cần, Ghi chú\n"
     "- Có ô Xem tồn để tra tồn kho tại thời điểm xem\n"
     "- Hàng nút chỉ có Quay lại"),

    ("024", "Màn Chi tiết hiện thêm cột SL đã phân bổ", "P1",
     "Phiếu đã ở trạng thái Đã phân bổ",
     "1. Mở chi tiết phiếu đó\n"
     "2. Đếm số cột của bảng khách hàng, so với phiếu ở trạng thái khác",
     "—",
     "- Phiếu Đã phân bổ có THÊM một cột số lượng đã phân bổ\n"
     "- Phiếu ở trạng thái khác không có cột này"),

    ("025", "Màn Chi tiết của kế toán kho trên phiếu chờ duyệt", "P0",
     "Tài khoản KT-1; phiếu đang ở Chờ duyệt của người cùng công ty",
     "1. Mở chi tiết phiếu đó bằng KT-1\n"
     "2. Quan sát khối Ghi chú duyệt và hàng nút",
     "—",
     "- Khối \"Ghi chú duyệt\" hiện ra và GÕ ĐƯỢC\n"
     "- Hàng nút có: Không duyệt, Tổng hợp, Quay lại\n"
     "- Không có nút Sửa và Xóa"),

    ("026", "Khối Ghi chú duyệt bị khóa với người không đủ điều kiện", "P0",
     "Phiếu đã ở trạng thái Đã tiếp nhận và có ghi chú duyệt từ lần xử lý trước",
     "1. Mở chi tiết bằng tài khoản KT-1\n"
     "2. Thử gõ vào khối Ghi chú duyệt\n"
     "3. Mở bằng tài khoản người lập phiếu",
     "—",
     "- KT-1: khối Ghi chú duyệt hiện nhưng bị KHÓA (phiếu không còn ở Chờ duyệt)\n"
     "- Người lập: khối cũng hiện ở dạng chỉ đọc\n"
     "- Phiếu chưa từng có ghi chú duyệt thì khối này KHÔNG hiện"),

    ("027", "Ô Xem tồn hoạt động ở màn Chi tiết", "P1",
     "Đang mở màn chi tiết một phiếu có 2 hàng hóa",
     "1. Chọn một kho ở ô Xem tồn\n"
     "2. Đọc cột SL tồn\n"
     "3. Đổi sang kho khác",
     "—",
     "- Cột SL tồn hiện số tồn hiện tại của kho đang chọn\n"
     "- ⚠️ Đây là tồn tại THỜI ĐIỂM XEM, không phải tồn lúc lập phiếu — không phải lỗi"),

    ("028", "Nút Quay lại dẫn về đâu tùy vai trò", "P1",
     "Phiếu Chờ duyệt; mở lần lượt bằng KT-1 (kế toán kho) và bằng người lập",
     "1. Với mỗi tài khoản, mở chi tiết rồi bấm Quay lại\n"
     "2. Ghi lại màn hình hiện ra",
     "—",
     "- KT-1: về màn \"Kế toán kho theo dõi\" — KHÔNG phải màn Chờ duyệt vừa đi ra\n"
     "- Người lập: về màn danh sách chế độ Tất cả\n"
     "- ⚠️ Ghi nhận: kế toán kho bị đưa sang một màn khác với màn vừa rời, dễ tưởng mất phiếu"),

    ("029", "Mở chi tiết phiếu không tồn tại", "P2",
     "Người đăng nhập bất kỳ",
     "1. Gõ đường dẫn chi tiết với một số phiếu chắc chắn không tồn tại",
     "Số phiếu: 99999999",
     "- Hệ thống hiện trang báo không tìm thấy\n"
     "- Không treo trang trắng"),

    ("030", "Hai hàng hóa cùng khách hàng trong một phiếu", "P1",
     "Đang ở màn Tạo mới",
     "1. Thêm hàng hóa HH-001 và HH-002\n"
     "2. Cả hai hàng hóa đều thêm dòng khách hàng KH-001 với SL và ngày cần khác nhau\n"
     "3. Bấm Lưu, mở lại phiếu",
     "—",
     "- Lưu được, không bị chặn\n"
     "- Mở lại thấy đủ 2 hàng hóa, mỗi hàng hóa có dòng khách hàng KH-001 riêng\n"
     "- Dòng Tổng cộng của mỗi hàng hóa tính riêng, không cộng chung"),

    ("031", "Phiếu nhiều hàng hóa nhiều khách hàng", "P0",
     "Đang ở màn Tạo mới; có sẵn 3 hàng hóa và 4 khách hàng để chọn",
     "1. Thêm 3 hàng hóa\n"
     "2. Hàng hóa 1: 3 dòng khách hàng; hàng hóa 2: 1 dòng; hàng hóa 3: 2 dòng\n"
     "3. Điền đủ SL, ngày cần, ghi chú cho cả 6 dòng\n"
     "4. Bấm Lưu, mở lại chi tiết",
     "3 hàng hóa, 6 dòng khách hàng",
     "- Lưu được\n"
     "- Chi tiết hiện đủ 3 khối hàng hóa với đúng 3, 1, 2 dòng khách hàng\n"
     "- Dòng Tổng cộng của từng hàng hóa đúng bằng tổng SL các dòng của nó"),

    ("032", "Giá niêm yết được lưu theo đơn vị đã chọn", "P1",
     "Hàng hóa HH-001 có 2 đơn vị tính với giá khác nhau",
     "1. Chọn đơn vị Thùng, ghi lại Giá niêm yết\n"
     "2. Lưu phiếu\n"
     "3. Mở lại chi tiết, đọc ĐVT và Giá niêm yết",
     "—",
     "- Mở lại vẫn đúng đơn vị Thùng và đúng giá của đơn vị đó\n"
     "- ⚠️ Nếu giá hiển thị khác lúc lập thì kiểm xem bảng giá có đổi trong thời gian đó không trước "
     "khi báo lỗi"),

    ("033", "Thứ tự hàng hóa và dòng khách hàng giữ nguyên sau khi lưu", "P1",
     "Đang ở màn Tạo mới với 3 hàng hóa xếp theo thứ tự A, B, C",
     "1. Ghi lại thứ tự hàng hóa và thứ tự dòng khách hàng của từng hàng hóa\n"
     "2. Bấm Lưu\n"
     "3. Mở lại màn Sửa và màn Chi tiết, đối chiếu thứ tự",
     "—",
     "- Thứ tự hàng hóa giữ nguyên A, B, C ở cả 2 màn\n"
     "- Thứ tự dòng khách hàng trong từng hàng hóa cũng giữ nguyên"),

    ("034", "Lưu lại phiếu làm ghi lại toàn bộ chi tiết", "P1",
     "Phiếu P đang mở màn Sửa, có 2 hàng hóa",
     "1. Không đổi gì, bấm Lưu\n"
     "2. Mở lại phiếu, đếm hàng hóa và dòng khách hàng\n"
     "3. Nhờ đội kỹ thuật kiểm xem có phát sinh dòng thừa hay dòng mồ côi không",
     "—",
     "- Số hàng hóa và số dòng khách hàng KHÔNG đổi\n"
     "- Không phát sinh dòng thừa; hệ thống xóa hết dòng cũ rồi ghi lại từ đầu"),

    ("035", "Ghi chú phiếu để trống vẫn lưu được", "P1",
     "Màn Tạo mới đã điền đủ hàng hóa, khách hàng và tệp đính kèm, để trống Ghi chú",
     "1. Bấm Lưu",
     "—",
     "- Lưu thành công (Ghi chú của phiếu KHÔNG bắt buộc)\n"
     "- ⚠️ Khác với Ghi chú của TỪNG DÒNG KHÁCH HÀNG — ô đó bắt buộc, xem mục VIII"),
]
