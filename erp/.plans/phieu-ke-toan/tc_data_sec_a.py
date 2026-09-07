# -*- coding: utf-8 -*-
"""Section I, II, III — hien thi trang, bo loc, danh sach."""

SEC_I = [
    ("001", "Vào màn từ mục menu Sổ tổng hợp", "P0",
     "Tài khoản bất kỳ đã đăng nhập",
     "1. Mở menu trên cùng, vào nhóm Kế toán\n"
     "2. Vào mục Sổ tổng hợp\n"
     "3. Bấm mục Phiếu kế toán\n"
     "4. Quan sát tiêu đề trang và bảng",
     "—",
     "- Mở đúng màn Danh sách phiếu kế toán\n"
     "- Bảng nạp dữ liệu, không báo lỗi\n"
     "- Đây là chế độ \"Tất cả\": phạm vi phiếu theo quyền xem của người đăng nhập\n"
     "- ⚠️ Đây là mục menu DUY NHẤT trỏ vào màn này; ba chế độ còn lại chỉ vào được bằng đường dẫn"),

    ("002", "Bố cục mặc định của màn danh sách", "P0",
     "Tài khoản có quyền xem tất cả phiếu kế toán của tổng công ty",
     "1. Mở màn Phiếu kế toán\n"
     "2. Quan sát từ trên xuống\n"
     "3. Bấm nút Bộ lọc để mở khối tìm kiếm",
     "—",
     "- Phía trên bảng có nút \"Bộ lọc\" và nút \"Tạo mới\"\n"
     "- Khối tìm kiếm mặc định ĐANG THU GỌN\n"
     "- Bảng có đúng các cột: STT, Mã phiếu, Mã phiếu YCDC, Tổng phát sinh, Diễn giải, Ngày hạch "
     "toán, Ngày lập, Người lập, Phòng ban, Trạng thái, Hành động\n"
     "- Phiếu mới nhất lên đầu"),

    ("003", "Chế độ Phiếu của tôi khác chế độ Tất cả", "P0",
     "Tài khoản C có quyền xem theo công ty; công ty có 35 phiếu đã duyệt, C tự lập 7 phiếu trong đó "
     "có 2 phiếu nháp",
     "1. Vào màn bằng mục menu (chế độ Tất cả), đọc dòng đếm bản ghi\n"
     "2. Dán đường dẫn màn danh sách KHÔNG kèm tham số chế độ, đọc dòng đếm\n"
     "3. Soát cột Người lập ở chế độ thứ hai",
     "—",
     "- Chế độ Tất cả: đếm theo phạm vi công ty, có cả phiếu người khác\n"
     "- Chế độ không kèm tham số: đúng 7 phiếu, mọi dòng đều do C lập\n"
     "- Chế độ này hiện CẢ 2 phiếu nháp của C"),

    ("004", "Chế độ Cần duyệt lọc cứng theo trạng thái Đã duyệt", "P0",
     "Tài khoản có quyền \"Thủ quỹ duyệt phiếu thu\"; dữ liệu có phiếu ở cả 3 trạng thái",
     "1. Dán đường dẫn màn Danh sách phiếu kế toán cần duyệt\n"
     "2. Quan sát tiêu đề trang và các cột\n"
     "3. Soát cột Trạng thái của mọi dòng",
     "—",
     "- Tiêu đề trang: Danh sách phiếu kế toán cần duyệt\n"
     "- Bảng chỉ có 8 cột: STT, Mã phiếu, Mã phiếu YCDC, Ngày lập, Người lập, Phòng ban, Trạng thái, "
     "Hành động\n"
     "- ⚠️ Mọi dòng đều là Đã duyệt — tên màn là \"cần duyệt\" nhưng nội dung là phiếu ĐÃ duyệt. Ghi "
     "nhận để nghiệp vụ quyết định đổi tên hay đổi điều kiện lọc\n"
     "- Không có nút Tạo mới trên màn này"),

    ("005", "Chế độ Đã duyệt", "P1",
     "Dữ liệu có phiếu ở cả 3 trạng thái",
     "1. Dán đường dẫn màn Danh sách phiếu kế toán đã duyệt\n"
     "2. Quan sát tiêu đề trang, các cột và các ô lọc",
     "—",
     "- Tiêu đề trang: Danh sách phiếu kế toán đã duyệt\n"
     "- Bảng có 8 cột giống chế độ Cần duyệt\n"
     "- Khối lọc chỉ có 3 ô: Mã phiếu, Mã phiếu YCDC, Người lập\n"
     "- ⚠️ Danh sách hiện phiếu ở MỌI trạng thái chứ không riêng Đã duyệt — ghi nhận"),

    ("006", "Đổi bộ lọc rồi mở chế độ khác", "P0",
     "Tài khoản C có quyền xem theo công ty",
     "1. Mở chế độ Tất cả, lọc Trạng thái là Đang tạo, ghi lại dòng đếm\n"
     "2. Dán đường dẫn chế độ Phiếu của tôi\n"
     "3. Đọc dòng đếm và các ô lọc",
     "Trạng thái: Đang tạo",
     "- Chế độ mới THẮNG bộ lọc cũ về mặt phạm vi phiếu\n"
     "- Không còn thấy phiếu ngoài phạm vi Phiếu của tôi"),

    ("007", "Bấm nút làm mới xóa điều kiện lọc nhưng giữ phạm vi", "P0",
     "Đang ở chế độ Phiếu của tôi, đã lọc Mã phiếu và Trạng thái",
     "1. Bấm nút làm mới (biểu tượng hai mũi tên xoay) cạnh nút tìm kiếm\n"
     "2. Quan sát các ô lọc và danh sách",
     "—",
     "- Mọi ô lọc trở về trống\n"
     "- Danh sách vẫn CHỈ là phiếu của chính mình, không mở rộng ra phiếu người khác"),

    ("008", "Sửa tay tham số chế độ thành giá trị lạ", "P0",
     "Tài khoản C có quyền xem theo công ty, tự lập 7 phiếu",
     "1. Mở màn danh sách\n"
     "2. Sửa tay phần tham số chế độ trên thanh địa chỉ thành một chuỗi vô nghĩa\n"
     "3. Bấm Enter, đọc dòng đếm bản ghi",
     "Tham số chế độ: xyz123",
     "- Hệ thống không lỗi, không trắng trang\n"
     "- ⚠️ Kết quả trả về là danh sách KHÔNG bó phạm vi — cần kiểm chứng có lộ phiếu ngoài quyền xem "
     "không. Nếu thấy phiếu công ty khác thì ghi Failed"),

    ("009", "Tài khoản không có quyền xem mở chế độ Tất cả", "P0",
     "Tài khoản NV-A không có quyền xem nào, tự lập 7 phiếu",
     "1. Đăng nhập bằng NV-A, mở mục Phiếu kế toán trên menu\n"
     "2. Đọc dòng đếm và soát cột Người lập",
     "—",
     "- Chỉ thấy đúng 7 phiếu do NV-A lập\n"
     "- Đường dẫn là cách xem, không phải cách cấp quyền"),

    ("010", "Nhãn trạng thái hiển thị đúng cho cả 3 trạng thái", "P0",
     "Dữ liệu có phiếu Đang tạo và phiếu Đã duyệt",
     "1. Bấm Bộ lọc, mở ô Trạng thái, đếm số lựa chọn\n"
     "2. Chọn lần lượt từng trạng thái rồi tìm kiếm\n"
     "3. Quan sát nhãn ở cột Trạng thái",
     "3 trạng thái",
     "- Ô Trạng thái có đúng 3 lựa chọn: Đang tạo · Đã duyệt · Hủy\n"
     "- CHỈ nhãn \"Đã duyệt\" tô XANH, hai nhãn còn lại tô ĐỎ\n"
     "- ⚠️ Trạng thái \"Hủy\" thường không có dữ liệu vì giao diện không có nút Hủy — ghi Không áp "
     "dụng nếu môi trường test không có"),

    ("011", "Cột Ngày hạch toán và Ngày lập cùng dạng ngày tháng năm", "P1",
     "Có phiếu lập ngày hôm nay nhưng ngày hạch toán để lùi về tháng trước",
     "1. Mở danh sách, tìm phiếu đó\n"
     "2. Đọc cột Ngày hạch toán và cột Ngày lập",
     "Ngày hạch toán: 31/08/2026 · Ngày lập: hôm nay",
     "- Cả hai cột hiện dạng ngày/tháng/năm\n"
     "- Hai cột hiện hai giá trị KHÁC nhau đúng như dữ liệu nhập\n"
     "- ⚠️ Không có bộ lọc theo Ngày hạch toán, chỉ lọc được theo Ngày lập"),

    ("012", "Cột Tổng phát sinh hiển thị có dấu phân cách nghìn", "P1",
     "Phiếu có tổng phát sinh nợ 1.234.567",
     "1. Mở danh sách, tìm phiếu đó\n"
     "2. Đọc cột Tổng phát sinh",
     "1.234.567",
     "- Hiện đúng 1.234.567 với dấu phân cách nghìn\n"
     "- ⚠️ Không kèm tên loại tiền và không có phần thập phân, khác cột Số tiền của màn Đề nghị thanh "
     "toán"),

    ("013", "Bấm mã phiếu mở màn chi tiết", "P0",
     "Có phiếu mà người đăng nhập được xem",
     "1. Bấm vào mã phiếu ở cột Mã phiếu",
     "—",
     "- Mở màn Chi tiết phiếu kế toán kèm mã phiếu trên tiêu đề\n"
     "- Mở ngay trên tab hiện tại"),

    ("014", "Bấm mã chứng từ nguồn mở Phiếu yêu cầu điều chỉnh công nợ", "P1",
     "Có phiếu được lập từ Phiếu yêu cầu điều chỉnh công nợ",
     "1. Bấm mã ở cột Mã phiếu YCDC của dòng đó",
     "—",
     "- Mở TAB MỚI tới màn chi tiết Phiếu yêu cầu điều chỉnh công nợ đúng mã đó"),

    ("015", "Bấm mã chứng từ nguồn mở Phiếu yêu cầu hạch toán bổ sung", "P1",
     "Có phiếu được lập từ Phiếu yêu cầu hạch toán bổ sung",
     "1. Bấm mã ở cột Mã phiếu YCDC của dòng đó",
     "—",
     "- Cột Mã phiếu YCDC hiện mã của Phiếu yêu cầu hạch toán bổ sung\n"
     "- Mở TAB MỚI tới đúng màn chi tiết Phiếu yêu cầu hạch toán bổ sung\n"
     "- ⚠️ Cột vẫn mang tiêu đề \"Mã phiếu YCDC\" dù nội dung là chứng từ khác — dễ gây hiểu nhầm, "
     "ghi nhận"),

    ("016", "Chứng từ nguồn là Yêu cầu hạch toán hoa hồng tháng", "P2",
     "Có phiếu lập từ Phiếu yêu cầu hạch toán hoa hồng tháng",
     "1. Đọc cột Mã phiếu YCDC của dòng đó\n"
     "2. Thử bấm vào mã",
     "—",
     "- Hiện mã phiếu hoa hồng tháng dạng CHỮ THƯỜNG, không phải liên kết\n"
     "- Bấm vào không mở được gì"),

    ("017", "Phiếu lập tay không có chứng từ nguồn", "P1",
     "Có phiếu lập tay hoàn toàn (không chọn chứng từ nguồn nào)",
     "1. Đọc cột Mã phiếu YCDC và cột Phòng ban của dòng đó",
     "—",
     "- Cột Mã phiếu YCDC để TRỐNG\n"
     "- ⚠️ Cột Phòng ban cũng TRỐNG dù người lập có phòng ban — vì cột này chỉ lấy từ chứng từ nguồn. "
     "Ghi nhận, đây là điểm dễ bị hiểu là mất dữ liệu"),

    ("018", "Menu Hành động thay đổi theo trạng thái và người lập", "P0",
     "Có 3 phiếu: P1 Đang tạo do mình lập, P2 Đã duyệt do mình lập, P3 Đang tạo do người khác lập",
     "1. Bấm biểu tượng bánh răng ở cột Hành động của từng phiếu\n"
     "2. Ghi lại các mục hiện ra",
     "—",
     "- P1: có đủ In · Xuất Excel · Sửa · Xóa\n"
     "- P2: chỉ có In · Xuất Excel\n"
     "- P3: không nhìn thấy trong danh sách chế độ Tất cả\n"
     "- Nút In và Xuất Excel luôn có với mọi trạng thái"),

    ("019", "Hệ thống ghi nhớ điều kiện lọc khi quay lại màn", "P2",
     "Đang ở chế độ Tất cả",
     "1. Nhập điều kiện lọc Mã phiếu và bấm tìm kiếm\n"
     "2. Bấm vào một mã phiếu để mở chi tiết\n"
     "3. Bấm Quay lại",
     "Mã phiếu: PKT09",
     "- Quay về danh sách với điều kiện lọc và trang đang xem được giữ nguyên\n"
     "- Không phải nhập lại điều kiện từ đầu"),
]

SEC_II = [
    ("001", "Lọc theo Mã phiếu, khớp tương đối", "P0",
     "Có phiếu mã TP.PKT0925.00001 và phiếu mã TP.PKT0825.00007",
     "1. Bấm nút Bộ lọc\n"
     "2. Nhập một phần mã vào ô Mã phiếu\n"
     "3. Bấm nút tìm kiếm",
     "Mã phiếu: PKT0925",
     "- Chỉ hiện phiếu có mã CHỨA chuỗi vừa nhập\n"
     "- Phiếu tháng 8 không lọt vào kết quả"),

    ("002", "Lọc theo Mã phiếu YCDC khớp cả hai loại chứng từ nguồn", "P0",
     "Có phiếu lập từ Phiếu yêu cầu điều chỉnh công nợ mã YCDC-01 và phiếu lập từ Phiếu yêu cầu hạch "
     "toán bổ sung mã HTBS-01",
     "1. Nhập YCDC-01 vào ô Mã phiếu YCDC, tìm kiếm, ghi kết quả\n"
     "2. Xóa đi, nhập HTBS-01, tìm kiếm, ghi kết quả",
     "YCDC-01 · HTBS-01",
     "- Cả hai lần tìm đều ra đúng phiếu tương ứng\n"
     "- Ô lọc này quét CẢ Phiếu yêu cầu điều chỉnh công nợ LẪN Phiếu yêu cầu hạch toán bổ sung"),

    ("003", "Lọc theo Mã phiếu YCDC với chứng từ nguồn là hoa hồng tháng", "P1",
     "Có phiếu lập từ Phiếu yêu cầu hạch toán hoa hồng tháng mã HH-01, mã này đang hiện trên lưới",
     "1. Nhập HH-01 vào ô Mã phiếu YCDC\n"
     "2. Bấm tìm kiếm",
     "HH-01",
     "- ⚠️ Dự kiến KHÔNG tìm ra phiếu nào, dù mã HH-01 đang hiển thị trên cột Mã phiếu YCDC. Ô lọc "
     "không quét loại chứng từ nguồn này\n"
     "- Ghi nhận là lỗi lọc thiếu nguồn"),

    ("004", "Lọc theo Người lập", "P0",
     "Công ty có phiếu của ít nhất 3 người lập khác nhau",
     "1. Chọn một nhân viên ở ô Người lập\n"
     "2. Bấm tìm kiếm\n"
     "3. Soát cột Người lập",
     "Người lập: NV-A",
     "- Chỉ hiện phiếu do NV-A lập\n"
     "- Ô chọn tìm được nhân viên cả khi nhân viên đã nghỉ việc"),

    ("005", "Lọc theo Trạng thái Đang tạo", "P0",
     "Người đăng nhập có 2 phiếu nháp; công ty có nhiều phiếu đã duyệt",
     "1. Chọn Trạng thái là Đang tạo\n"
     "2. Bấm tìm kiếm",
     "Trạng thái: Đang tạo",
     "- Chỉ hiện 2 phiếu nháp của chính mình\n"
     "- Không lộ phiếu nháp của người khác"),

    ("006", "Lọc theo Trạng thái Đã duyệt", "P0",
     "Công ty có phiếu ở cả 2 trạng thái",
     "1. Chọn Trạng thái là Đã duyệt\n"
     "2. Bấm tìm kiếm",
     "Trạng thái: Đã duyệt",
     "- Mọi dòng đều mang nhãn Đã duyệt tô xanh"),

    ("007", "Lọc theo Trạng thái Hủy", "P2",
     "Môi trường test chưa có phiếu nào ở trạng thái Hủy",
     "1. Chọn Trạng thái là Hủy\n"
     "2. Bấm tìm kiếm",
     "Trạng thái: Hủy",
     "- Danh sách rỗng, không báo lỗi\n"
     "- ⚠️ Giao diện không có nút Hủy nên trạng thái này gần như không phát sinh — ghi Không áp dụng "
     "nếu không tạo được dữ liệu"),

    ("008", "Lọc theo số hiệu tài khoản trong chi tiết", "P0",
     "Phiếu X có dòng chi tiết dùng tài khoản 1311; phiếu Y chỉ dùng 5111 và 3331",
     "1. Nhập 1311 vào ô Tên hoặc số tài khoản\n"
     "2. Bấm tìm kiếm",
     "1311",
     "- Hiện phiếu X, không hiện phiếu Y\n"
     "- Tìm khớp tương đối nên các tài khoản con bắt đầu bằng 1311 cũng ra"),

    ("009", "Lọc theo tên tài khoản trong chi tiết", "P1",
     "Phiếu X có dòng dùng tài khoản tên \"Phải thu khách hàng\"",
     "1. Nhập Phải thu vào ô Tên hoặc số tài khoản\n"
     "2. Bấm tìm kiếm",
     "Phải thu",
     "- Hiện phiếu X\n"
     "- Ô lọc chấp nhận cả số hiệu lẫn tên tài khoản"),

    ("010", "Lọc theo Mã đơn hàng/hợp đồng", "P0",
     "Phiếu X có dòng chi tiết gắn hợp đồng HD-2026-08",
     "1. Nhập HD-2026 vào ô Mã đơn hàng/hợp đồng\n"
     "2. Bấm tìm kiếm",
     "HD-2026",
     "- Hiện phiếu X\n"
     "- Tìm khớp tương đối trên mã hợp đồng ghi ở dòng chi tiết"),

    ("011", "Lọc theo Khách hàng", "P0",
     "Phiếu X có dòng chi tiết gắn khách hàng KH-01; phiếu Y gắn nhà cung cấp",
     "1. Chọn KH-01 ở ô Khách hàng\n"
     "2. Bấm tìm kiếm",
     "Khách hàng: KH-01",
     "- Hiện phiếu X\n"
     "- ⚠️ Ô này chỉ quét đối tượng là KHÁCH HÀNG; phiếu gắn nhà cung cấp hoặc nhân viên không tìm "
     "được bằng ô này"),

    ("012", "Lọc theo Số tiền từ", "P0",
     "Phiếu A tổng phát sinh 1.000.000; phiếu B tổng phát sinh 5.000.000",
     "1. Nhập 2.000.000 vào ô Số tiền từ\n"
     "2. Bấm tìm kiếm",
     "Số tiền từ: 2.000.000",
     "- Chỉ hiện phiếu B\n"
     "- Ô nhận số có dấu phân cách nghìn"),

    ("013", "Lọc theo Số tiền đến, kiểm tra đầu mút", "P0",
     "Phiếu A tổng phát sinh đúng 1.000.000; phiếu B 5.000.000",
     "1. Nhập 1.000.000 vào ô Số tiền đến\n"
     "2. Bấm tìm kiếm",
     "Số tiền đến: 1.000.000",
     "- Phiếu A CÓ trong kết quả (đầu mút được tính)\n"
     "- Phiếu B không có"),

    ("014", "Nhập Số tiền từ lớn hơn Số tiền đến", "P2",
     "Có dữ liệu phiếu ở nhiều mức tiền",
     "1. Nhập Số tiền từ 5.000.000 và Số tiền đến 1.000.000\n"
     "2. Bấm tìm kiếm",
     "Từ 5.000.000 · Đến 1.000.000",
     "- Danh sách rỗng\n"
     "- Không báo lỗi hệ thống, không trắng trang"),

    ("015", "Lọc theo Ngân hàng", "P1",
     "Phiếu X có dòng chi tiết chọn ngân hàng Vietcombank",
     "1. Nhập Vietcom vào ô Ngân hàng\n"
     "2. Bấm tìm kiếm",
     "Vietcom",
     "- Hiện phiếu X\n"
     "- Tìm khớp tương đối trên TÊN ngân hàng"),

    ("016", "Lọc theo STK ngân hàng", "P1",
     "Phiếu X có dòng chi tiết chọn số tài khoản ngân hàng 0011001234567",
     "1. Nhập 001100 vào ô STK ngân hàng\n"
     "2. Bấm tìm kiếm",
     "001100",
     "- Hiện phiếu X\n"
     "- Tìm khớp tương đối trên số tài khoản ngân hàng ghi ở dòng chi tiết"),

    ("017", "Lọc theo NVKD", "P1",
     "Phiếu X có dòng chi tiết gắn hợp đồng do NVKD-1 lập; phiếu Y gắn hợp đồng do NVKD-2 lập",
     "1. Chọn NVKD-1 ở ô NVKD\n"
     "2. Bấm tìm kiếm",
     "NVKD: NVKD-1",
     "- Hiện phiếu X, không hiện phiếu Y\n"
     "- Ô này lọc theo người lập HỢP ĐỒNG gắn ở dòng chi tiết, không phải người lập phiếu kế toán"),

    ("018", "Lọc Từ ngày tính trọn ngày", "P0",
     "Phiếu Z được lập lúc 09 giờ ngày 10/09/2026",
     "1. Nhập Từ ngày là 10/09/2026, để trống Đến ngày\n"
     "2. Bấm tìm kiếm",
     "Từ ngày: 10/09/2026",
     "- Phiếu Z CÓ trong kết quả"),

    ("019", "Lọc Đến ngày làm mất phiếu lập trong chính ngày đó", "P0",
     "Phiếu Z được lập lúc 09 giờ ngày 10/09/2026",
     "1. Nhập Đến ngày là 10/09/2026, để trống Từ ngày, tìm kiếm, ghi kết quả\n"
     "2. Sửa Đến ngày thành 11/09/2026, tìm kiếm lại",
     "Đến ngày: 10/09/2026 rồi 11/09/2026",
     "- ⚠️ Bước 1: phiếu Z KHÔNG có trong kết quả dù lập đúng ngày đó\n"
     "- Bước 2: phiếu Z xuất hiện\n"
     "- Đây là bẫy đối chiếu số liệu: muốn lấy trọn ngày phải điền thêm 1 ngày"),

    ("020", "Ô lọc theo đơn vị chỉ có ở chế độ Tất cả", "P1",
     "Tài khoản B có quyền xem tất cả phiếu (bộ quyền chung của lưới)",
     "1. Mở chế độ Tất cả, bấm Bộ lọc, ghi lại các ô lọc theo đơn vị\n"
     "2. Mở chế độ Phiếu của tôi, bấm Bộ lọc, ghi lại\n"
     "3. Mở chế độ Cần duyệt, bấm Bộ lọc, ghi lại",
     "—",
     "- Chế độ Tất cả: có ô Công ty và ô Phòng ban\n"
     "- Chế độ Phiếu của tôi: KHÔNG có ô nào theo đơn vị\n"
     "- Chế độ Cần duyệt: chỉ có 3 ô Mã phiếu, Mã phiếu YCDC, Người lập"),

    ("021", "Kết hợp nhiều điều kiện lọc cùng lúc", "P0",
     "Công ty có phiếu đa dạng về trạng thái, người lập và số tiền",
     "1. Nhập đồng thời: Mã phiếu PKT09, Trạng thái Đã duyệt, Người lập NV-A, Số tiền từ 1.000.000\n"
     "2. Bấm tìm kiếm\n"
     "3. Soát từng dòng kết quả",
     "PKT09 · Đã duyệt · NV-A · từ 1.000.000",
     "- Mọi dòng thỏa mãn ĐỒNG THỜI cả 4 điều kiện\n"
     "- Không có dòng nào chỉ thỏa một phần"),

    ("022", "Tìm kiếm không có kết quả", "P1",
     "Đang ở chế độ Tất cả",
     "1. Nhập một mã phiếu chắc chắn không tồn tại\n"
     "2. Bấm tìm kiếm",
     "Mã phiếu: ZZZZZZ",
     "- Bảng hiện thông báo không có dữ liệu\n"
     "- Không báo lỗi, không trắng trang"),

    ("023", "Nút làm mới xóa hết điều kiện lọc", "P1",
     "Đang có 4 điều kiện lọc và đang ở trang 3",
     "1. Bấm nút làm mới cạnh nút tìm kiếm\n"
     "2. Quan sát các ô lọc và danh sách",
     "—",
     "- Mọi ô lọc trở về trống, kể cả ô chọn nhiều cấp\n"
     "- Danh sách trở về đầy đủ theo phạm vi của chế độ đang mở"),
]

SEC_III = [
    ("001", "Sắp xếp mặc định phiếu mới nhất lên đầu", "P0",
     "Có ít nhất 5 phiếu lập ở các thời điểm khác nhau trong 3 ngày gần đây",
     "1. Mở màn danh sách, không bấm sắp xếp\n"
     "2. Đọc cột Ngày lập từ trên xuống",
     "—",
     "- Phiếu lập gần đây nhất nằm dòng đầu\n"
     "- Ngày lập giảm dần dọc danh sách"),

    ("002", "Sắp xếp theo Mã phiếu hai chiều", "P1",
     "Có ít nhất 5 phiếu mã khác nhau",
     "1. Bấm tiêu đề cột Mã phiếu lần 1, đọc thứ tự\n"
     "2. Bấm lần 2, đọc thứ tự",
     "—",
     "- Lần 1 sắp tăng dần theo mã, lần 2 giảm dần\n"
     "- Biểu tượng mũi tên trên tiêu đề cột đổi chiều tương ứng"),

    ("003", "Sắp xếp theo Tổng phát sinh đúng giá trị số", "P0",
     "Có 3 phiếu tổng phát sinh 900.000 · 1.000.000 · 12.000.000",
     "1. Bấm tiêu đề cột Tổng phát sinh để sắp tăng dần\n"
     "2. Đọc thứ tự 3 phiếu",
     "—",
     "- Thứ tự đúng là 900.000 → 1.000.000 → 12.000.000\n"
     "- ⚠️ Nếu ra thứ tự 1.000.000 → 12.000.000 → 900.000 nghĩa là đang sắp theo chuỗi ký tự, ghi "
     "Failed"),

    ("004", "Các cột còn lại không sắp xếp được", "P2",
     "Có dữ liệu trên lưới",
     "1. Lần lượt bấm tiêu đề các cột Mã phiếu YCDC, Diễn giải, Ngày hạch toán, Ngày lập, Người lập, "
     "Phòng ban, Trạng thái\n"
     "2. Quan sát thứ tự danh sách",
     "—",
     "- Không cột nào trong nhóm trên đổi được thứ tự\n"
     "- Không có biểu tượng sắp xếp trên các tiêu đề đó\n"
     "- ⚠️ Không sắp xếp được theo Ngày hạch toán dù đây là ngày ghi sổ — ghi nhận cho nghiệp vụ"),

    ("005", "Đổi số dòng hiển thị mỗi trang", "P1",
     "Có hơn 50 phiếu trong phạm vi xem",
     "1. Đổi ô chọn số dòng mỗi trang sang mức lớn hơn\n"
     "2. Đếm số dòng thực tế trên trang",
     "—",
     "- Số dòng trên trang đúng bằng mức vừa chọn\n"
     "- Dòng đếm bản ghi cập nhật lại khoảng hiển thị"),

    ("006", "Chuyển trang giữ nguyên điều kiện lọc", "P0",
     "Đang lọc Trạng thái Đã duyệt, kết quả có hơn 2 trang",
     "1. Ghi lại dòng đếm bản ghi ở trang 1\n"
     "2. Chuyển sang trang 2\n"
     "3. Soát cột Trạng thái ở trang 2",
     "Trạng thái: Đã duyệt",
     "- Dòng đếm bản ghi giữ nguyên tổng số\n"
     "- Mọi dòng ở trang 2 vẫn là Đã duyệt, không bị mở lại toàn bộ dữ liệu"),

    ("007", "Sắp xếp rồi chuyển trang", "P1",
     "Kết quả có hơn 2 trang",
     "1. Sắp xếp theo Tổng phát sinh giảm dần\n"
     "2. Chuyển sang trang 2\n"
     "3. So giá trị dòng đầu trang 2 với dòng cuối trang 1",
     "—",
     "- Thứ tự vẫn liên tục giữa hai trang\n"
     "- Dòng đầu trang 2 nhỏ hơn hoặc bằng dòng cuối trang 1"),

    ("008", "Dòng đếm bản ghi khớp số phiếu thực tế", "P0",
     "Người đăng nhập có phạm vi xem đúng 35 phiếu",
     "1. Mở danh sách, đọc dòng đếm bản ghi\n"
     "2. Đặt số dòng mỗi trang lớn hơn 35, đếm tay số dòng trên lưới",
     "—",
     "- Dòng đếm ghi tổng 35\n"
     "- Đếm tay ra đúng 35 dòng"),

    ("009", "Cột Diễn giải với nội dung dài", "P2",
     "Có phiếu Diễn giải dài hơn 200 ký tự",
     "1. Mở danh sách, quan sát cột Diễn giải của phiếu đó",
     "Diễn giải 250 ký tự",
     "- Nội dung không phá vỡ bố cục bảng\n"
     "- Đọc được đầy đủ hoặc có cách xem hết (xuống dòng hoặc mở chi tiết)"),

    ("010", "Cột Phòng ban trống với phiếu không lập từ Yêu cầu điều chỉnh công nợ", "P1",
     "Có 3 phiếu: P1 lập tay, P2 lập từ Phiếu yêu cầu điều chỉnh công nợ, P3 lập từ Phiếu yêu cầu hạch "
     "toán bổ sung. Cả 3 người lập đều có phòng ban trong hồ sơ nhân sự",
     "1. Mở danh sách\n"
     "2. Đọc cột Phòng ban của cả 3 dòng",
     "—",
     "- P2 có tên phòng ban\n"
     "- ⚠️ P1 và P3 để TRỐNG dù người lập có phòng ban — cột này chỉ lấy phòng ban của Phiếu yêu cầu "
     "điều chỉnh công nợ. Ghi nhận là lỗi hiển thị thiếu"),

    ("011", "Tổng phát sinh của phiếu ngoại tệ hiện theo VNĐ", "P0",
     "Phiếu USD: phát sinh nợ 100 USD, tỷ giá 25.000",
     "1. Mở danh sách, tìm phiếu đó\n"
     "2. Đọc cột Tổng phát sinh",
     "100 USD × 25.000",
     "- Hiện 2.500.000\n"
     "- ⚠️ Không hiện số nguyên tệ và không kèm chữ USD — người đọc dễ nhầm là phiếu tiền Việt. Đây "
     "là thiết kế hiện tại, ghi nhận không ghi Failed"),

    ("012", "Danh sách rỗng khi tài khoản chưa lập phiếu nào", "P2",
     "Tài khoản mới, chưa lập phiếu nào, không có quyền xem nào",
     "1. Đăng nhập, mở mục Phiếu kế toán",
     "—",
     "- Bảng hiện thông báo không có dữ liệu\n"
     "- Nút Tạo mới và nút Bộ lọc vẫn hiển thị bình thường"),
]
