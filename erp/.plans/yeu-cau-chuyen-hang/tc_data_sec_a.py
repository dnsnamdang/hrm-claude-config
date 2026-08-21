# -*- coding: utf-8 -*-
"""Section I, II, III — hien thi trang, bo loc, danh sach."""

SEC_I = [
    ("001", "Vào màn từ mục menu", "P0",
     "Tài khoản bất kỳ đã đăng nhập",
     "1. Mở menu trên cùng, tìm mục Phiếu yêu cầu chuyển hàng\n"
     "2. Bấm vào\n"
     "3. Quan sát tiêu đề trang và bảng",
     "—",
     "- Mở đúng màn Quản lý yêu cầu chuyển hàng\n"
     "- Bảng nạp dữ liệu, không báo lỗi\n"
     "- Đây là chế độ \"Tất cả\": phạm vi phiếu theo quyền xem của người đăng nhập"),

    ("002", "Vào màn từ lối vào thứ hai trên menu", "P1",
     "Vẫn tài khoản ở TC_01.001",
     "1. Tìm mục Phiếu yêu cầu chuyển hàng ở nhóm menu còn lại\n"
     "2. Bấm vào, so với kết quả của TC_01.001",
     "—",
     "- Mở đúng cùng một màn, cùng chế độ, cùng số tổng\n"
     "- ⚠️ Hai mục menu viết hoa khác nhau (\"Phiếu Yêu cầu chuyển hàng\" và \"Phiếu yêu cầu chuyển "
     "hàng\") nhưng trỏ về cùng một màn — ghi nhận"),

    ("003", "Chế độ Phiếu của tôi khác chế độ Tất cả", "P0",
     "Tài khoản C có quyền xem theo công ty; công ty có 30 phiếu, C tự lập 5 phiếu",
     "1. Vào màn bằng mục menu (chế độ Tất cả), đọc số tổng\n"
     "2. Dán đường dẫn màn danh sách KHÔNG kèm tham số chế độ, đọc số tổng\n"
     "3. Soát cột Người tạo ở chế độ thứ hai",
     "—",
     "- Chế độ Tất cả: tổng theo phạm vi công ty\n"
     "- Chế độ không kèm tham số: chỉ 5 phiếu, mọi dòng đều do C lập\n"
     "- Chế độ này hiện CẢ phiếu nháp của C"),

    ("004", "Bố cục mặc định của màn danh sách", "P0",
     "Tài khoản có quyền xem tổng công ty",
     "1. Mở màn danh sách\n"
     "2. Quan sát từ trên xuống",
     "—",
     "- Phía trên bảng có nút \"Bộ lọc\", nút \"Tạo mới\" và nút \"Xuất excel\"\n"
     "- Khối tìm kiếm mặc định ĐANG THU GỌN\n"
     "- Bảng có 8 cột: STT, Mã yêu cầu, Người tạo, Ngày tạo, Người tiếp nhận, Ngày tiếp nhận, Trạng "
     "thái, Hành động\n"
     "- Mặc định 10 dòng mỗi trang, phiếu mới nhất lên đầu"),

    ("005", "Ô lọc Trạng thái có hai mục trùng tên", "P0",
     "Đang ở màn danh sách, dữ liệu có phiếu ở nhiều trạng thái",
     "1. Bấm Bộ lọc, mở ô Trạng thái\n"
     "2. Đếm số lựa chọn và ghi lại tên từng mục theo thứ tự\n"
     "3. Chọn mục \"Đang nhập kho\" THỨ NHẤT, tìm kiếm, ghi số kết quả\n"
     "4. Chọn mục \"Đang nhập kho\" THỨ HAI, tìm kiếm, ghi số kết quả",
     "—",
     "- Ô Trạng thái có 13 lựa chọn: Đã tiếp nhận, Chờ duyệt, Đang tạo, Đang đề nghị, Đang xuất kho, "
     "Đã xuất kho, Đang vận chuyển, Đang nhập kho, Đang nhập kho, Đã nhập kho, Đã nhập hàng, Đã phân "
     "bổ, Đã hủy\n"
     "- ⚠️ Hiện trạng: HAI mục cùng tên \"Đang nhập kho\", người dùng không phân biệt được. Hai lần lọc "
     "cho ra kết quả khác nhau. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: đặt tên phân biệt hoặc gộp lại thành một"),

    ("006", "Nhãn trạng thái hiển thị đúng màu", "P0",
     "Dữ liệu có phiếu ở nhiều trạng thái",
     "1. Lọc lần lượt Đang tạo, Chờ duyệt, Đã tiếp nhận, Đã hủy\n"
     "2. Quan sát nhãn ở cột Trạng thái",
     "4 trạng thái",
     "- Đang tạo, Chờ duyệt, Đã hủy: nhãn ĐỎ\n"
     "- Đã tiếp nhận và các trạng thái của dây chuyền kho phía sau: nhãn XANH"),

    ("007", "Cột Người tiếp nhận và Ngày tiếp nhận", "P1",
     "Có phiếu còn nháp, phiếu Chờ duyệt chưa xử lý, phiếu đã bị Không duyệt và phiếu Đã tiếp nhận",
     "1. Đọc cột Người tiếp nhận và Ngày tiếp nhận của 4 phiếu trên",
     "—",
     "- Phiếu nháp và phiếu Chờ duyệt chưa xử lý: cả 2 cột TRỐNG\n"
     "- Phiếu Đã tiếp nhận: hiện tên kế toán kho và ngày tiếp nhận\n"
     "- ⚠️ Phiếu đã bị Không duyệt ĐÃ QUAY VỀ trạng thái Đang tạo nhưng 2 cột này VẪN có dữ liệu — "
     "người lập nhìn thấy phiếu nháp lại có người tiếp nhận. Ghi nhận và báo lại nghiệp vụ"),

    ("008", "Bấm mã yêu cầu mở màn chi tiết", "P1",
     "Danh sách đang có phiếu do chính người đăng nhập lập",
     "1. Bấm vào Mã yêu cầu ở dòng của mình\n"
     "2. Quan sát trang mở ra",
     "—",
     "- Mở màn chi tiết đúng phiếu vừa bấm\n"
     "- Mã yêu cầu trên màn chi tiết khớp với dòng vừa bấm\n"
     "- ⚠️ Với phiếu của người khác thì xem TC-ROLE-06"),

    ("009", "Định dạng mã yêu cầu", "P1",
     "Vừa lập một phiếu mới",
     "1. Đọc Mã yêu cầu của phiếu vừa lập và vài phiếu cũ",
     "—",
     "- Mã có dạng PYCCH- kèm 5 chữ số, ví dụ PYCCH-00042\n"
     "- Mã tăng dần theo thứ tự lập phiếu\n"
     "- Không có phần mã công ty và tháng năm như các màn phiếu tài chính"),

    ("010", "Bảng rỗng khi bộ lọc không khớp phiếu nào", "P1",
     "Danh sách đang có dữ liệu",
     "1. Bấm Bộ lọc, gõ chuỗi chắc chắn không tồn tại vào ô Mã yêu cầu\n"
     "2. Bấm nút tìm kiếm",
     "Mã yêu cầu: ZZZZ-KHONG-TON-TAI",
     "- Bảng hiện dòng báo không có dữ liệu\n"
     "- Tổng hiện 0, không có lỗi đỏ\n"
     "- Nút Tạo mới và nút Xuất excel vẫn còn"),

    ("011", "Màn Chờ duyệt của kế toán kho", "P0",
     "Tài khoản KT-1, đang ở màn Phiếu yêu cầu chuyển hàng chờ duyệt",
     "1. Ghi lại tên các cột và bộ nút phía trên bảng\n"
     "2. Đọc cột Trạng thái của mọi dòng\n"
     "3. Mở menu hành động của một dòng",
     "—",
     "- Bảng có đúng 8 cột như màn danh sách\n"
     "- Có nút Bộ lọc, Tạo mới và Xuất excel\n"
     "- MỌI dòng đều ở trạng thái Chờ duyệt\n"
     "- Menu hành động có: Tổng hợp và In yêu cầu"),

    ("012", "Chế độ Kế toán kho theo dõi khác màn Chờ duyệt", "P1",
     "Tài khoản KT-1; công ty có phiếu ở nhiều trạng thái",
     "1. Mở màn Chờ duyệt, đọc số tổng\n"
     "2. Dán đường dẫn chế độ Kế toán kho theo dõi, đọc số tổng và cột Trạng thái",
     "—",
     "- Màn Chờ duyệt: chỉ phiếu Chờ duyệt\n"
     "- Chế độ Kế toán kho theo dõi: mọi phiếu của người cùng công ty TRỪ phiếu nháp — số tổng lớn hơn\n"
     "- Màn này KHÔNG có nút Xuất excel (chỉ có Bộ lọc và Tạo mới)\n"
     "- Không có mục menu nào trỏ tới"),

    ("013", "Hai đường dẫn cũ không có mục menu", "P2",
     "Tài khoản có quyền xem tổng công ty",
     "1. Rà toàn bộ menu, tìm mục dẫn tới chế độ Kế toán kho theo dõi và màn danh sách sao chép\n"
     "2. Mở từng đường dẫn trực tiếp",
     "—",
     "- Không có mục menu nào trỏ tới hai màn này\n"
     "- Mở bằng đường dẫn thì màn vẫn chạy, không báo lỗi\n"
     "- ⚠️ Ghi nhận là hiện trạng: chức năng có nhưng không có lối vào"),
]

SEC_II = [
    ("001", "Bung và thu gọn khối bộ lọc", "P1",
     "Vừa mở màn danh sách",
     "1. Quan sát khối tìm kiếm trước khi bấm gì\n"
     "2. Bấm nút Bộ lọc\n"
     "3. Bấm lại lần nữa",
     "—",
     "- Ban đầu khối tìm kiếm ẩn\n"
     "- Bấm lần 1 bung ra đủ các ô lọc, có nút kính lúp (tìm kiếm) và nút mũi tên tròn (làm mới)\n"
     "- Bấm lần 2 thu gọn lại"),

    ("002", "Danh sách các ô lọc", "P0",
     "Tài khoản có quyền xem tổng công ty",
     "1. Bấm Bộ lọc\n"
     "2. Ghi lại toàn bộ ô lọc",
     "—",
     "- Có các ô: Công ty, Phòng ban, Từ ngày, Đến ngày, Mã yêu cầu, Trạng thái, ô \"Nhập tên, mã hàng "
     "hóa\", Người tiếp nhận, Người tạo\n"
     "- Có 2 nút: tìm kiếm và làm mới"),

    ("003", "Ô lọc theo đơn vị hiện theo quyền", "P0",
     "Lần lượt dùng 4 tài khoản: quyền tổng công ty, quyền công ty, quyền phòng ban, không quyền nào",
     "1. Với mỗi tài khoản, bấm Bộ lọc\n"
     "2. Ghi lại xem có ô Công ty, ô Phòng ban, ô Bộ phận hay không",
     "4 mức quyền",
     "- Quyền tổng công ty: có ô Công ty và ô Phòng ban\n"
     "- Quyền công ty: chỉ có ô Phòng ban\n"
     "- Quyền phòng ban: có ô Phòng ban và ô Bộ phận\n"
     "- Không quyền nào: các ô này không hiện"),

    ("004", "Lọc theo Mã yêu cầu tìm được khớp một phần", "P0",
     "Có phiếu mã PYCCH-00042",
     "1. Gõ 00042 vào ô Mã yêu cầu, bấm tìm kiếm\n"
     "2. Gõ PYCCH, tìm lại",
     "—",
     "- Gõ 00042: chỉ còn phiếu có chuỗi đó trong mã\n"
     "- Gõ PYCCH: ra toàn bộ phiếu (mọi mã đều bắt đầu bằng chuỗi này)\n"
     "- Bảng về trang 1, tổng đổi theo"),

    ("005", "Bộ lọc chỉ chạy khi bấm nút tìm kiếm", "P0",
     "Khối lọc đang bung",
     "1. Gõ 00042 vào ô Mã yêu cầu, KHÔNG bấm gì thêm, chờ 5 giây\n"
     "2. Bấm nút tìm kiếm",
     "—",
     "- Trong lúc gõ, bảng KHÔNG đổi\n"
     "- Chỉ sau khi bấm nút tìm kiếm bảng mới lọc lại"),

    ("006", "Lọc theo Trạng thái", "P0",
     "Dữ liệu có phiếu ở nhiều trạng thái",
     "1. Chọn Trạng thái = Chờ duyệt, tìm kiếm, soát cột Trạng thái\n"
     "2. Lặp lại với Đã tiếp nhận và Đã hủy",
     "3 trạng thái",
     "- Mỗi lần lọc, mọi dòng đều đúng trạng thái đang chọn\n"
     "- Lọc Đang tạo chỉ ra phiếu nháp của chính người đăng nhập\n"
     "- ⚠️ Với mục \"Đang nhập kho\" xem riêng TC_01.005"),

    ("007", "Lọc theo tên hoặc mã hàng hóa", "P0",
     "Phiếu P có hàng hóa mã HH-001 tên \"Máy bơm ly tâm\"; phiếu Q không chứa hàng hóa đó",
     "1. Gõ HH-001 vào ô \"Nhập tên, mã hàng hóa\", tìm kiếm\n"
     "2. Xóa đi, gõ \"Máy bơm\", tìm lại\n"
     "3. Mở chi tiết một dòng kết quả để đối chiếu",
     "—",
     "- Gõ mã hàng: ra phiếu P, không ra phiếu Q\n"
     "- Gõ một phần TÊN hàng: cũng ra phiếu P (ô này quét cả mã lẫn tên)\n"
     "- Phiếu chứa nhiều hàng hóa khớp vẫn chỉ hiện MỘT dòng"),

    ("008", "Lọc theo Người tạo", "P1",
     "NV-B đã lập 4 phiếu trong phạm vi người đăng nhập nhìn thấy",
     "1. Bấm ô Người tạo, gõ tên NV-B, chọn từ gợi ý\n"
     "2. Bấm tìm kiếm, đọc cột Người tạo",
     "—",
     "- Mọi dòng đều có Người tạo là NV-B\n"
     "- Số dòng khớp số phiếu của NV-B trong phạm vi được xem (không tính phiếu nháp của NV-B)"),

    ("009", "Lọc theo Người tiếp nhận", "P1",
     "KT-1 đã tiếp nhận ít nhất 3 phiếu",
     "1. Bấm ô Người tiếp nhận, chọn KT-1, tìm kiếm\n"
     "2. Đọc cột Người tiếp nhận của kết quả",
     "—",
     "- Chỉ ra phiếu mà KT-1 là người tiếp nhận\n"
     "- ⚠️ Kết quả bao gồm CẢ phiếu KT-1 đã bấm Không duyệt (đã quay về Đang tạo) nếu người đăng nhập "
     "là người lập phiếu đó — ghi nhận"),

    ("010", "Lọc theo Từ ngày", "P0",
     "Có phiếu lập ngày 31/07/2026 và phiếu lập ngày 05/08/2026",
     "1. Nhập Từ ngày = 01/08/2026, tìm kiếm\n"
     "2. Đọc cột Ngày tạo của dòng cũ nhất trong kết quả",
     "Từ ngày: 01/08/2026",
     "- Phiếu 31/07/2026 bị loại\n"
     "- Phiếu 05/08/2026 còn trong kết quả\n"
     "- Phiếu lập đúng 0 giờ ngày 01/08/2026 (nếu có) VẪN được lấy"),

    ("011", "Ô Đến ngày tính trọn ngày cuối", "P0",
     "Có phiếu lập lúc 23:50 ngày 31/08/2026 và phiếu lập ngày 30/08/2026",
     "1. Nhập Đến ngày = 31/08/2026, tìm kiếm\n"
     "2. Tìm phiếu lập ngày 31/08/2026 trong kết quả",
     "Đến ngày: 31/08/2026",
     "- Phiếu lập lúc 23:50 ngày 31/08/2026 CÓ trong kết quả\n"
     "- ⚠️ Màn này tính TRỌN ngày cuối, KHÁC ba màn phiếu tài chính. Đây là hành vi ĐÚNG, không ghi "
     "Failed\n"
     "- Phiếu 30/08/2026 cũng có trong kết quả"),

    ("012", "Nhập Đến ngày nhỏ hơn Từ ngày", "P2",
     "Danh sách đang có dữ liệu",
     "1. Nhập Từ ngày = 31/08/2026, Đến ngày = 01/08/2026\n"
     "2. Bấm tìm kiếm",
     "—",
     "- Bảng trả về rỗng, hiện dòng báo không có dữ liệu\n"
     "- Không treo trang, không lỗi đỏ"),

    ("013", "Kết hợp nhiều điều kiện lọc cùng lúc", "P0",
     "Có ít nhất 2 phiếu trạng thái Chờ duyệt do NV-B lập, chứa hàng hóa mã HH-001",
     "1. Chọn Trạng thái = Chờ duyệt\n"
     "2. Chọn Người tạo = NV-B\n"
     "3. Gõ HH-001 vào ô tên, mã hàng hóa\n"
     "4. Bấm tìm kiếm, kiểm TỪNG dòng kết quả",
     "3 điều kiện cùng lúc",
     "- Mọi dòng thỏa ĐỒNG THỜI cả 3 điều kiện\n"
     "- ⚠️ Kiểm từng dòng, đừng chỉ nhìn số tổng"),

    ("014", "Nút làm mới xóa sạch điều kiện lọc", "P0",
     "Đang lọc bằng ít nhất 4 điều kiện",
     "1. Bấm nút làm mới\n"
     "2. Quan sát các ô lọc và bảng",
     "—",
     "- Mọi ô lọc về trống, kể cả ô chọn Người tạo và Người tiếp nhận\n"
     "- Bảng nạp lại đầy đủ từ trang 1"),

    ("015", "Đổi Công ty thì danh sách Phòng ban đổi theo", "P1",
     "Tài khoản có quyền xem tổng công ty",
     "1. Chọn Công ty A, mở ô Phòng ban, ghi lại danh sách\n"
     "2. Đổi Công ty sang B, mở lại ô Phòng ban",
     "—",
     "- Danh sách Phòng ban đổi theo công ty đang chọn\n"
     "- Không còn phòng ban của công ty A trong danh sách"),

    ("016", "Lọc theo Phòng ban", "P1",
     "Tài khoản có quyền xem tổng công ty; phòng P1 có 6 phiếu",
     "1. Chọn Phòng ban = P1, tìm kiếm\n"
     "2. Đọc số tổng và mở vài phiếu để đối chiếu người lập",
     "—",
     "- Ra đúng 6 phiếu, trừ phiếu nháp của người khác\n"
     "- Mọi người lập đều thuộc phòng P1"),

    ("017", "Bộ lọc được ghi nhớ khi rời màn rồi quay lại", "P1",
     "Đang lọc Trạng thái = Chờ duyệt ở chế độ Tất cả",
     "1. Sang màn khác\n"
     "2. Quay lại mục Phiếu yêu cầu chuyển hàng trên menu\n"
     "3. Bấm Bộ lọc, quan sát các ô",
     "—",
     "- Điều kiện Trạng thái = Chờ duyệt vẫn còn, bảng hiện đúng tập đã lọc\n"
     "- ⚠️ Test xong nhớ bấm nút làm mới trước khi sang ca test khác"),

    ("018", "Bộ lọc của các chế độ danh sách không dùng chung", "P1",
     "Tài khoản KT-1 mở được cả màn danh sách và màn Chờ duyệt",
     "1. Ở chế độ Tất cả, lọc Người tạo = NV-B\n"
     "2. Sang màn Chờ duyệt, bấm Bộ lọc, quan sát\n"
     "3. Quay lại chế độ Tất cả",
     "—",
     "- Màn Chờ duyệt mở ra với bộ lọc TRẮNG\n"
     "- Quay lại chế độ Tất cả vẫn còn điều kiện Người tạo = NV-B"),

    ("019", "Lọc trên màn Chờ duyệt không phá điều kiện trạng thái", "P0",
     "Tài khoản KT-1 ở màn Chờ duyệt, có 4 phiếu",
     "1. Chọn Trạng thái = Đã tiếp nhận, bấm tìm kiếm\n"
     "2. Quan sát kết quả",
     "—",
     "- Kết quả RỖNG: màn này đã cố định chỉ lấy phiếu Chờ duyệt, chọn trạng thái khác thì không còn "
     "dòng nào\n"
     "- ⚠️ Ghi nhận đúng hiện trạng; nếu ra phiếu Đã tiếp nhận thì đó là rò rỉ, ghi Failed"),

    ("020", "Lọc theo hàng hóa không tồn tại", "P2",
     "Danh sách đang có dữ liệu",
     "1. Gõ một mã hàng chắc chắn không có vào ô tên, mã hàng hóa\n"
     "2. Bấm tìm kiếm",
     "—",
     "- Bảng rỗng, tổng hiện 0\n"
     "- Không báo lỗi, không treo trang"),
]

SEC_III = [
    ("001", "Thứ tự mặc định là phiếu mới nhất lên đầu", "P0",
     "Danh sách chưa bấm sắp xếp cột nào",
     "1. Mở màn danh sách\n"
     "2. Đọc cột Ngày tạo của 10 dòng đầu",
     "—",
     "- Ngày tạo giảm dần từ trên xuống\n"
     "- Dòng đầu là phiếu lập gần đây nhất trong phạm vi đang xem"),

    ("002", "Cột nào cho phép sắp xếp ở màn danh sách", "P1",
     "Danh sách đang có dữ liệu",
     "1. Bấm lần lượt tiêu đề từng cột\n"
     "2. Ghi lại cột nào có mũi tên sắp xếp và cột nào không",
     "—",
     "- Chỉ cột Mã yêu cầu có mũi tên sắp xếp\n"
     "- Các cột Người tạo, Ngày tạo, Người tiếp nhận, Ngày tiếp nhận, Trạng thái, Hành động KHÔNG sắp "
     "xếp được\n"
     "- ⚠️ Ghi nhận: cột Ngày tạo là cột hay dùng để sắp xếp nhất nhưng lại không bật — báo lại nghiệp "
     "vụ"),

    ("003", "Sắp xếp theo cột Mã yêu cầu", "P0",
     "Danh sách có nhiều hơn 1 trang",
     "1. Bấm tiêu đề cột Mã yêu cầu\n"
     "2. Đọc thứ tự mã trên trang 1\n"
     "3. Bấm lần nữa để đổi chiều",
     "—",
     "- Lần 1: sắp xếp theo mã tăng dần, mũi tên đổi chiều\n"
     "- Lần 2: thứ tự đảo ngược\n"
     "- Bảng KHÔNG báo lỗi tải dữ liệu"),

    ("004", "Chuyển trang giữ nguyên bộ lọc", "P0",
     "Đang lọc Trạng thái = Chờ duyệt, kết quả nhiều hơn 3 trang",
     "1. Sang trang 2, soát cột Trạng thái\n"
     "2. Đọc ô hiển thị số dòng\n"
     "3. Sang trang 3 rồi quay về trang 1",
     "—",
     "- Mọi trang đều chỉ có phiếu Chờ duyệt\n"
     "- Tổng N giữ nguyên, khoảng a đến b đổi theo trang"),

    ("005", "Cột STT đánh số liên tục theo trang", "P0",
     "10 dòng mỗi trang, kết quả hơn 20 dòng",
     "1. Đọc STT dòng cuối trang 1\n"
     "2. Sang trang 2, đọc STT dòng đầu và dòng cuối",
     "—",
     "- Trang 1 kết thúc ở 10\n"
     "- Trang 2 chạy từ 11 tới 20"),

    ("006", "Đổi số dòng mỗi trang", "P0",
     "Kết quả hơn 100 dòng, đang ở trang 3",
     "1. Đổi số dòng mỗi trang sang 25\n"
     "2. Quan sát trang hiện tại và số dòng\n"
     "3. Đổi tiếp sang 100",
     "—",
     "- Mỗi lần đổi đều quay về trang 1\n"
     "- Số dòng trên màn đúng bằng số vừa chọn (trừ trang cuối)\n"
     "- Ô hiển thị số dòng cập nhật theo"),

    ("007", "Menu hành động theo trạng thái và theo người", "P0",
     "4 dòng: (a) Đang tạo của chính mình; (b) Chờ duyệt của chính mình; (c) Đã tiếp nhận của chính "
     "mình; (d) Chờ duyệt của người khác. Người đăng nhập KHÔNG có quyền Kế toán kho",
     "1. Mở menu bánh răng ở cột Hành động của từng dòng\n"
     "2. Ghi lại các mục trong menu",
     "4 trường hợp",
     "- (a) Sửa yêu cầu, Xóa yêu cầu, In yêu cầu\n"
     "- (b) chỉ In yêu cầu\n"
     "- (c) chỉ In yêu cầu\n"
     "- (d) chỉ In yêu cầu\n"
     "- Mọi dòng luôn có In yêu cầu"),

    ("008", "Kế toán kho có thêm mục Tổng hợp", "P0",
     "Tài khoản KT-1; 1 phiếu Chờ duyệt và 1 phiếu Đã tiếp nhận, đều của người cùng công ty",
     "1. Mở menu hành động của từng dòng",
     "—",
     "- Phiếu Chờ duyệt: có mục \"Tổng hợp\" và \"In yêu cầu\"\n"
     "- Phiếu Đã tiếp nhận: chỉ có \"In yêu cầu\"\n"
     "- Bấm Tổng hợp chuyển sang màn tạo Phiếu yêu cầu xuất hàng kèm sẵn phiếu này"),

    ("009", "Kế toán kho không thấy nút Sửa Xóa trên phiếu người khác", "P0",
     "Tài khoản KT-1; phiếu Chờ duyệt do NV-A lập",
     "1. Mở menu hành động của dòng đó\n"
     "2. Mở chi tiết phiếu, quan sát hàng nút",
     "—",
     "- Menu chỉ có Tổng hợp và In yêu cầu, KHÔNG có Sửa và Xóa\n"
     "- Màn chi tiết có nút Không duyệt, Tổng hợp, Quay lại — không có Sửa\n"
     "- ⚠️ Màn này xét đúng người lập ở cả 2 chỗ — điểm làm đúng"),

    ("010", "Định dạng ngày trên lưới", "P1",
     "Danh sách đang có dữ liệu",
     "1. Đọc cột Ngày tạo và Ngày tiếp nhận của vài dòng",
     "—",
     "- Cả hai cột hiện dạng ngày/tháng/năm, KHÔNG có giờ phút\n"
     "- Ô không có dữ liệu để trống, không hiện chữ lạ"),

    ("011", "Xuất Excel danh sách theo bộ lọc hiện tại", "P0",
     "Đang lọc Trạng thái = Chờ duyệt, kết quả 5 phiếu",
     "1. Bấm nút Xuất excel\n"
     "2. Chờ tệp tải về, mở tệp\n"
     "3. Đếm số dòng và đối chiếu nội dung",
     "—",
     "- Mở TAB MỚI để tải, tệp tên danh_sach_yeu_cau_chuyen_hang.xlsx\n"
     "- Tệp có đúng 5 dòng, đúng các phiếu đang hiện trên màn\n"
     "- 7 cột: STT, Mã yêu cầu, Người tạo, Ngày tạo, Người tiếp nhận, Ngày tiếp nhận, Trạng thái"),

    ("012", "Tệp Excel ghi lại khoảng thời gian đã lọc", "P1",
     "Đang lọc Từ ngày = 01/08/2026 và Đến ngày = 31/08/2026",
     "1. Bấm Xuất excel, mở tệp\n"
     "2. Tìm dòng ghi khoảng thời gian\n"
     "3. Xóa ô Đến ngày, xuất lại và đọc dòng đó",
     "—",
     "- Lần 1: tệp có dòng \"Từ ngày 01/08/2026 đến ngày 31/08/2026\"\n"
     "- Lần 2: dòng đổi thành \"Từ ngày 01/08/2026\"\n"
     "- Không lọc thời gian thì dòng này không hiện"),

    ("013", "Phần đầu trang của tệp Excel lấy theo người đăng nhập", "P1",
     "Tài khoản có quyền xem tổng công ty, danh sách đang chứa phiếu của nhiều công ty",
     "1. Bấm Xuất excel, mở tệp\n"
     "2. Đọc phần đầu trang, đối chiếu với các dòng bên dưới",
     "—",
     "- ⚠️ Hiện trạng: phần đầu trang chỉ ghi thông tin công ty của NGƯỜI ĐANG ĐĂNG NHẬP trong khi các "
     "dòng bên dưới thuộc nhiều công ty. Ghi nhận và báo lại nghiệp vụ\n"
     "- Người xem trong phạm vi một công ty thì không gặp vấn đề này"),
]
