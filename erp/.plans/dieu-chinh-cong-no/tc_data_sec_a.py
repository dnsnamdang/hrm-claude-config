# -*- coding: utf-8 -*-
"""Section I, II, III — hien thi trang, bo loc, danh sach."""

SEC_I = [
    ("001", "Vào màn từ mục menu Công nợ - Thu - Chi", "P0",
     "Tài khoản bất kỳ đã đăng nhập",
     "1. Mở menu trên cùng, vào nhóm Công nợ - Thu - Chi\n"
     "2. Bấm mục Phiếu yêu cầu điều chỉnh công nợ\n"
     "3. Quan sát tiêu đề trang và bảng",
     "—",
     "- Mở đúng màn danh sách Phiếu yêu cầu điều chỉnh công nợ\n"
     "- Bảng nạp dữ liệu, không báo lỗi\n"
     "- Đây là chế độ \"Tất cả\": phạm vi phiếu theo quyền xem của người đăng nhập"),

    ("002", "Vào màn từ lối vào thứ hai trên menu", "P1",
     "Vẫn tài khoản ở TC_01.001",
     "1. Mở menu, tìm mục \"Yêu cầu điều chỉnh công nợ\" ở nhóm còn lại\n"
     "2. Bấm vào, so với kết quả của TC_01.001",
     "—",
     "- Mở đúng cùng một màn, cùng chế độ, cùng số tổng\n"
     "- ⚠️ Hai mục menu đặt tên khác nhau (\"Phiếu yêu cầu điều chỉnh công nợ\" và \"Yêu cầu điều chỉnh "
     "công nợ\") nhưng trỏ về cùng một màn — ghi nhận"),

    ("003", "Chế độ Phiếu của tôi khác chế độ Tất cả", "P0",
     "Tài khoản C có quyền xem theo công ty; công ty có 40 phiếu, C tự lập 6 phiếu",
     "1. Vào màn bằng mục menu (chế độ Tất cả), đọc số tổng\n"
     "2. Dán đường dẫn màn danh sách KHÔNG kèm tham số chế độ, đọc số tổng\n"
     "3. Soát cột Người lập ở chế độ thứ hai",
     "—",
     "- Chế độ Tất cả: tổng theo phạm vi công ty\n"
     "- Chế độ không kèm tham số: chỉ 6 phiếu, mọi dòng đều do C lập\n"
     "- Chế độ này hiện CẢ phiếu nháp của C"),

    ("004", "Bố cục mặc định của màn danh sách", "P0",
     "Tài khoản có quyền xem tổng công ty",
     "1. Mở màn danh sách\n"
     "2. Quan sát từ trên xuống",
     "—",
     "- Phía trên bảng có nút \"Bộ lọc\", nút \"Tạo mới\" và nút \"Xuất excel\"\n"
     "- Khối tìm kiếm mặc định ĐANG THU GỌN\n"
     "- Bảng có các cột: STT, Mã phiếu, Loại phiếu, Số phiếu báo có, KH/NCC, Số tiền, Ngày lập, Người "
     "lập, Phòng ban, Ngày nhận, Người duyệt, Trạng thái, Hành động\n"
     "- Mặc định 10 dòng mỗi trang, phiếu mới nhất lên đầu"),

    ("005", "Cột Loại phiếu hiển thị đúng hai loại", "P0",
     "Dữ liệu có cả phiếu điều chỉnh công nợ khách hàng và phiếu điều chỉnh công nợ NCC",
     "1. Bấm Bộ lọc, chọn Loại phiếu = Điều chỉnh công nợ khách hàng, tìm kiếm\n"
     "2. Đọc cột Loại phiếu\n"
     "3. Đổi sang Điều chỉnh công nợ NCC, tìm lại",
     "2 loại phiếu",
     "- Ô lọc Loại phiếu có đúng 2 lựa chọn\n"
     "- Cột Loại phiếu hiện đúng nhãn \"Điều chỉnh công nợ khách hàng\" hoặc \"Điều chỉnh công nợ NCC\"\n"
     "- Phiếu cũ chưa có loại phiếu vẫn hiện nhãn khách hàng (giá trị mặc định)"),

    ("006", "Cột KH/NCC lấy nguồn khác nhau theo loại phiếu", "P0",
     "Phiếu M loại khách hàng có 2 dòng điều chỉnh đến của 2 khách hàng, dòng đến đầu tiên là KH-001; "
     "phiếu N loại NCC có dòng điều chỉnh từ của NCC-01",
     "1. Tìm phiếu M và phiếu N trong danh sách\n"
     "2. Đọc cột KH/NCC của từng dòng\n"
     "3. Mở chi tiết từng phiếu để đối chiếu",
     "—",
     "- Phiếu M hiện \"KH-001 - <tên khách hàng>\" — lấy từ dòng điều chỉnh ĐẾN đầu tiên\n"
     "- Phiếu N hiện \"NCC-01 - <tên nhà cung cấp>\" — lấy từ dòng điều chỉnh TỪ đầu tiên\n"
     "- ⚠️ Hai loại phiếu lấy hai nguồn khác nhau, không phải lỗi"),

    ("007", "Nhãn trạng thái hiển thị đúng cho cả 6 trạng thái", "P0",
     "Dữ liệu có phiếu ở nhiều trạng thái",
     "1. Bấm Bộ lọc, mở ô Trạng thái, đếm số lựa chọn\n"
     "2. Chọn lần lượt từng trạng thái rồi tìm kiếm\n"
     "3. Quan sát nhãn ở cột Trạng thái",
     "6 trạng thái",
     "- Ô Trạng thái có đúng 6 lựa chọn: Đang tạo, Chờ tạo phiếu kế toán, Đã tạo phiếu kế toán, Đã "
     "duyệt phiếu kế toán, Hủy, Từ chối\n"
     "- Đã tạo phiếu kế toán và Đã duyệt phiếu kế toán: nhãn XANH\n"
     "- Bốn nhãn còn lại: nhãn ĐỎ"),

    ("008", "Cột Số phiếu báo có là liên kết mở tab mới", "P1",
     "Có ít nhất 1 phiếu được tạo từ Phiếu báo có và 1 phiếu lập tay",
     "1. Tìm 2 phiếu trên\n"
     "2. Đọc cột Số phiếu báo có\n"
     "3. Bấm vào mã phiếu báo có",
     "—",
     "- Phiếu tạo từ báo có: cột hiện mã phiếu báo có dạng liên kết\n"
     "- Bấm vào mở TAB MỚI sang màn chi tiết phiếu báo có\n"
     "- Phiếu lập tay: cột để trống"),

    ("009", "Cột Ngày nhận và Người duyệt", "P1",
     "Có phiếu còn nháp, phiếu đã gửi duyệt và phiếu đã bị Từ chối",
     "1. Đọc cột Ngày nhận và cột Người duyệt của 3 phiếu trên",
     "—",
     "- Phiếu còn nháp: cả 2 cột TRỐNG\n"
     "- Phiếu đã gửi duyệt: cột Ngày nhận hiện ngày bấm Lưu và gửi duyệt\n"
     "- ⚠️ Kiểm kỹ cột Người duyệt có được điền sau khi kế toán xử lý hay không; nếu vẫn trống thì ghi "
     "nhận lại số liệu cụ thể"),

    ("010", "Bấm mã phiếu mở màn chi tiết", "P1",
     "Danh sách đang có phiếu",
     "1. Bấm vào Mã phiếu ở dòng đầu\n"
     "2. Quan sát trang mở ra",
     "—",
     "- Mở màn Chi tiết phiếu yêu cầu điều chỉnh công nợ đúng phiếu vừa bấm\n"
     "- Mã phiếu trên màn chi tiết khớp với dòng vừa bấm"),

    ("011", "Bảng rỗng khi bộ lọc không khớp phiếu nào", "P1",
     "Danh sách đang có dữ liệu",
     "1. Bấm Bộ lọc, gõ chuỗi chắc chắn không tồn tại vào ô Mã phiếu\n"
     "2. Bấm nút tìm kiếm",
     "Mã phiếu: ZZZZ-KHONG-TON-TAI",
     "- Bảng hiện dòng báo không có dữ liệu\n"
     "- Tổng hiện 0, không có lỗi đỏ\n"
     "- Nút Tạo mới và nút Xuất excel vẫn còn"),

    ("012", "Chế độ Đã xử lý lấy nhầm dữ liệu của màn khác", "P0",
     "Tài khoản KT-1 đã xử lý vài phiếu điều chỉnh công nợ",
     "1. Rà toàn bộ menu, tìm mục dẫn tới danh sách phiếu mình đã xử lý\n"
     "2. Mở chế độ Đã xử lý bằng đường dẫn trực tiếp\n"
     "3. Đọc tên các cột và nội dung vài dòng, đối chiếu với danh sách phiếu điều chỉnh công nợ",
     "—",
     "- Không có mục menu nào trỏ tới chế độ này\n"
     "- ⚠️ Hiện trạng: màn mở ra nhưng hiển thị dữ liệu của màn PHIẾU ĐỀ NGHỊ THU TIỀN, không phải "
     "phiếu điều chỉnh công nợ; các cột lệch nhau, ô lọc \"Loại thu\" cũng là của màn kia. Ghi nhận "
     "Failed kèm ảnh chụp\n"
     "- Kỳ vọng đúng: liệt kê phiếu điều chỉnh công nợ mà người đăng nhập đã xử lý"),

    ("013", "Màn Chờ duyệt đổi tên cột và bớt nút", "P1",
     "Tài khoản KT-1, đang ở màn Chờ duyệt",
     "1. Ghi lại tên các cột của bảng\n"
     "2. Quan sát bộ nút phía trên bảng\n"
     "3. So với màn danh sách chế độ Tất cả",
     "—",
     "- Cột thứ 5 tên là \"Khách hàng\" thay vì \"KH/NCC\", tuy nội dung vẫn có thể là nhà cung cấp\n"
     "- Không có nút Tạo mới và không có nút Xuất excel\n"
     "- Các cột còn lại giống màn danh sách"),
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

    ("002", "Danh sách các ô lọc ở chế độ Tất cả", "P0",
     "Tài khoản có quyền xem tổng công ty",
     "1. Bấm Bộ lọc\n"
     "2. Ghi lại toàn bộ ô lọc",
     "—",
     "- Có các ô: Công ty, Phòng ban, Từ ngày, Đến ngày, Mã phiếu, Loại phiếu, Số phiếu báo có, KH/NCC, "
     "Hợp đồng điều chỉnh từ, Hợp đồng điều chỉnh đến, Số tiền từ, Số tiền đến, Người lập, Người duyệt, "
     "Trạng thái\n"
     "- Có 2 nút: tìm kiếm và làm mới"),

    ("003", "Bộ lọc màn Chờ duyệt khác màn danh sách", "P1",
     "Tài khoản KT-1, đang ở màn Chờ duyệt",
     "1. Bấm Bộ lọc\n"
     "2. Ghi lại các ô lọc, so với màn danh sách",
     "—",
     "- Có các ô: Công ty, Phòng ban, Từ ngày, Đến ngày, Mã phiếu, Số phiếu báo có, Khách hàng, Hợp "
     "đồng, Số tiền từ, Số tiền đến, Người lập\n"
     "- KHÔNG có ô Loại phiếu, Trạng thái, Người duyệt\n"
     "- ⚠️ Ô Công ty và Phòng ban LUÔN hiện ở màn này dù người dùng không có quyền xem theo cấp"),

    ("004", "Lọc theo Mã phiếu tìm được khớp một phần", "P0",
     "Có phiếu mã kết thúc bằng .00012",
     "1. Gõ 00012 vào ô Mã phiếu\n"
     "2. Bấm nút tìm kiếm",
     "Mã phiếu: 00012",
     "- Chỉ còn phiếu có chuỗi 00012 nằm trong mã\n"
     "- Bảng về trang 1, tổng đổi theo"),

    ("005", "Bộ lọc chỉ chạy khi bấm nút tìm kiếm", "P0",
     "Khối lọc đang bung",
     "1. Gõ 00012 vào ô Mã phiếu, KHÔNG bấm gì thêm, chờ 5 giây\n"
     "2. Bấm nút tìm kiếm",
     "—",
     "- Trong lúc gõ, bảng KHÔNG đổi\n"
     "- Chỉ sau khi bấm nút tìm kiếm bảng mới lọc lại"),

    ("006", "Lọc theo Loại phiếu", "P0",
     "Dữ liệu có cả 2 loại phiếu",
     "1. Chọn Loại phiếu = Điều chỉnh công nợ khách hàng, tìm kiếm, soát cột Loại phiếu\n"
     "2. Đổi sang Điều chỉnh công nợ NCC, tìm lại",
     "2 loại phiếu",
     "- Mỗi lần lọc, mọi dòng đều đúng loại phiếu vừa chọn\n"
     "- Tổng 2 lần lọc cộng lại bằng tổng khi không lọc (nếu mọi phiếu đều đã có loại phiếu)"),

    ("007", "Lọc theo Số phiếu báo có", "P1",
     "Có ít nhất 2 phiếu tạo từ cùng một phiếu báo có mã BC-2026-001",
     "1. Gõ BC-2026-001 vào ô Số phiếu báo có, tìm kiếm\n"
     "2. Đọc cột Số phiếu báo có của kết quả\n"
     "3. Gõ một phần mã, tìm lại",
     "Số phiếu báo có: BC-2026-001",
     "- Chỉ ra phiếu gắn đúng phiếu báo có đó\n"
     "- Gõ một phần mã vẫn ra kết quả\n"
     "- Phiếu lập tay (không có phiếu báo có) không lọt vào kết quả"),

    ("008", "Lọc theo KH/NCC quét cả bốn vị trí", "P0",
     "Khách hàng KH-001 xuất hiện ở dòng điều chỉnh TỪ của phiếu M và ở dòng điều chỉnh ĐẾN của phiếu "
     "N; nhà cung cấp NCC-01 xuất hiện ở phiếu loại NCC",
     "1. Bấm ô KH/NCC, gõ từ khóa, chọn KH-001, tìm kiếm\n"
     "2. Tìm phiếu M và phiếu N trong kết quả\n"
     "3. Làm lại với NCC-01",
     "—",
     "- Ô KH/NCC là ô chọn tìm từ xa, gợi ý gồm CẢ khách hàng lẫn nhà cung cấp\n"
     "- Cả phiếu M và phiếu N đều có trong kết quả (quét cả điều chỉnh từ lẫn điều chỉnh đến)\n"
     "- Chọn NCC-01 ra đúng phiếu loại NCC\n"
     "- Mỗi phiếu chỉ hiện một dòng, không nhân đôi"),

    ("009", "Lọc theo Hợp đồng điều chỉnh từ", "P0",
     "Phiếu P có dòng điều chỉnh TỪ gắn hợp đồng HD-2026-001; phiếu Q có dòng điều chỉnh ĐẾN gắn chính "
     "hợp đồng đó",
     "1. Gõ HD-2026-001 vào ô Hợp đồng điều chỉnh từ, tìm kiếm\n"
     "2. Kiểm phiếu P và phiếu Q có trong kết quả không\n"
     "3. Gõ một phần mã, tìm lại",
     "Hợp đồng: HD-2026-001",
     "- Phiếu P CÓ trong kết quả\n"
     "- Phiếu Q KHÔNG có (hợp đồng đó nằm ở cột điều chỉnh đến)\n"
     "- Gõ một phần mã vẫn ra kết quả"),

    ("010", "Lọc theo Hợp đồng điều chỉnh đến", "P0",
     "Vẫn dữ liệu ở TC_02.009",
     "1. Gõ HD-2026-001 vào ô Hợp đồng điều chỉnh đến, tìm kiếm\n"
     "2. Kiểm phiếu P và phiếu Q",
     "—",
     "- Phiếu Q CÓ trong kết quả\n"
     "- Phiếu P KHÔNG có\n"
     "- Điền cả hai ô cùng lúc thì chỉ ra phiếu thỏa ĐỒNG THỜI hai điều kiện"),

    ("011", "Ô lọc Hợp đồng ở màn Chờ duyệt không có tác dụng", "P0",
     "Màn Chờ duyệt đang có ít nhất 5 phiếu",
     "1. Ghi lại số tổng hiện tại\n"
     "2. Gõ một mã hợp đồng có thật vào ô Hợp đồng, tìm kiếm\n"
     "3. Gõ chuỗi chắc chắn vô nghĩa, tìm lại",
     "Hợp đồng: mã có thật, rồi \"ZZZZZZ\"",
     "- ⚠️ Hiện trạng: cả 2 lần tổng số phiếu KHÔNG đổi, hệ thống bỏ qua ô này. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: lọc theo hợp đồng như ở màn danh sách, hoặc bỏ hẳn ô lọc này"),

    ("012", "Lọc theo khoảng Số tiền", "P0",
     "Có phiếu tổng tiền 3.000.000; có phiếu 20.000.000; có phiếu 90.000.000",
     "1. Nhập Số tiền từ = 10.000.000, để trống ô đến, tìm kiếm\n"
     "2. Nhập thêm Số tiền đến = 50.000.000, tìm kiếm\n"
     "3. Đối chiếu cột Số tiền của kết quả",
     "Từ 10.000.000 · Đến 50.000.000",
     "- Bước 1: mất phiếu 3.000.000; còn phiếu 20.000.000 và 90.000.000\n"
     "- Bước 2: chỉ còn phiếu trong đoạn 10.000.000 đến 50.000.000, tính cả 2 đầu mút"),

    ("013", "Lọc theo Người lập", "P1",
     "NV-B đã lập 5 phiếu trong phạm vi người đăng nhập nhìn thấy",
     "1. Bấm ô Người lập, gõ tên NV-B, chọn từ gợi ý\n"
     "2. Bấm tìm kiếm, đọc cột Người lập",
     "—",
     "- Mọi dòng đều có Người lập là NV-B\n"
     "- Số dòng khớp số phiếu của NV-B trong phạm vi được xem"),

    ("014", "Lọc theo Người duyệt", "P1",
     "KT-1 đã xử lý ít nhất 3 phiếu",
     "1. Bấm ô Người duyệt, chọn KT-1, tìm kiếm\n"
     "2. Đọc cột Người duyệt của kết quả",
     "—",
     "- Chỉ ra phiếu mà KT-1 là người xử lý\n"
     "- ⚠️ Nếu cột Người duyệt của kết quả để trống thì đối chiếu lại với TC_01.009 và ghi nhận"),

    ("015", "Lọc theo Trạng thái", "P0",
     "Dữ liệu có phiếu ở nhiều trạng thái",
     "1. Chọn Trạng thái = Chờ tạo phiếu kế toán, tìm kiếm\n"
     "2. Lặp lại với Từ chối và Đã duyệt phiếu kế toán",
     "3 trạng thái",
     "- Mỗi lần lọc, mọi dòng đều đúng trạng thái đang chọn\n"
     "- Lọc Đang tạo ở chế độ Tất cả chỉ ra phiếu nháp của chính người đăng nhập"),

    ("016", "Lọc theo Từ ngày", "P0",
     "Có phiếu lập ngày 31/07/2026 và phiếu lập ngày 05/08/2026",
     "1. Nhập Từ ngày = 01/08/2026, tìm kiếm\n"
     "2. Đọc cột Ngày lập của dòng cũ nhất trong kết quả",
     "Từ ngày: 01/08/2026",
     "- Phiếu 31/07/2026 bị loại\n"
     "- Phiếu 05/08/2026 còn trong kết quả"),

    ("017", "Ô Đến ngày làm rụng trọn ngày cuối", "P0",
     "Có phiếu lập lúc 09:15 ngày 31/08/2026 và phiếu lập ngày 30/08/2026",
     "1. Nhập Đến ngày = 31/08/2026, tìm kiếm\n"
     "2. Tìm phiếu lập ngày 31/08/2026 trong kết quả\n"
     "3. Đổi Đến ngày = 01/09/2026, tìm lại",
     "—",
     "- ⚠️ Hiện trạng: đặt Đến ngày 31/08/2026 thì phiếu lập trong chính ngày 31/08 BỊ MẤT; phải đặt "
     "01/09/2026 mới thấy. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: Đến ngày phải tính trọn ngày đó\n"
     "- Phiếu 30/08/2026 có mặt ở cả 2 lần"),

    ("018", "Kết hợp nhiều điều kiện lọc cùng lúc", "P0",
     "Có ít nhất 2 phiếu loại NCC, trạng thái Chờ tạo phiếu kế toán, tổng tiền trên 10.000.000",
     "1. Chọn Loại phiếu = Điều chỉnh công nợ NCC\n"
     "2. Chọn Trạng thái = Chờ tạo phiếu kế toán\n"
     "3. Nhập Số tiền từ = 10.000.000\n"
     "4. Bấm tìm kiếm, kiểm TỪNG dòng kết quả",
     "3 điều kiện cùng lúc",
     "- Mọi dòng thỏa ĐỒNG THỜI cả 3 điều kiện\n"
     "- ⚠️ Kiểm từng dòng, đừng chỉ nhìn số tổng"),

    ("019", "Nút làm mới xóa sạch điều kiện lọc", "P0",
     "Đang lọc bằng ít nhất 4 điều kiện",
     "1. Bấm nút làm mới\n"
     "2. Quan sát các ô lọc và bảng",
     "—",
     "- Mọi ô lọc về trống, kể cả ô chọn KH/NCC và Người duyệt\n"
     "- Bảng nạp lại đầy đủ từ trang 1"),

    ("020", "Đổi Công ty thì danh sách Phòng ban đổi theo", "P1",
     "Tài khoản có quyền xem tổng công ty",
     "1. Chọn Công ty A, mở ô Phòng ban, ghi lại danh sách\n"
     "2. Đổi Công ty sang B, mở lại ô Phòng ban",
     "—",
     "- Danh sách Phòng ban đổi theo công ty đang chọn\n"
     "- Không còn phòng ban của công ty A trong danh sách"),

    ("021", "Bộ lọc được ghi nhớ và ghi nhớ riêng cho từng chế độ", "P1",
     "Tài khoản KT-1 mở được cả màn danh sách và màn Chờ duyệt",
     "1. Ở chế độ Tất cả, lọc Loại phiếu = Điều chỉnh công nợ NCC\n"
     "2. Sang màn Chờ duyệt, bấm Bộ lọc, quan sát\n"
     "3. Quay lại chế độ Tất cả",
     "—",
     "- Màn Chờ duyệt mở ra với bộ lọc TRẮNG\n"
     "- Quay lại chế độ Tất cả vẫn còn điều kiện Loại phiếu = Điều chỉnh công nợ NCC\n"
     "- ⚠️ Test xong nhớ bấm nút làm mới trước khi sang ca test khác"),
]

SEC_III = [
    ("001", "Thứ tự mặc định là phiếu mới nhất lên đầu", "P0",
     "Danh sách chưa bấm sắp xếp cột nào",
     "1. Mở màn danh sách\n"
     "2. Đọc cột Ngày lập của 10 dòng đầu",
     "—",
     "- Ngày lập giảm dần từ trên xuống\n"
     "- Dòng đầu là phiếu lập gần đây nhất trong phạm vi đang xem"),

    ("002", "Chỉ cột Số tiền cho phép sắp xếp", "P1",
     "Danh sách đang có dữ liệu",
     "1. Bấm lần lượt tiêu đề các cột: Mã phiếu, Loại phiếu, Số phiếu báo có, KH/NCC, Ngày lập, Người "
     "lập, Phòng ban, Ngày nhận, Người duyệt, Trạng thái\n"
     "2. Quan sát thứ tự dòng sau mỗi lần bấm\n"
     "3. Bấm tiêu đề cột Số tiền",
     "—",
     "- Mười cột ở bước 1 KHÔNG có mũi tên sắp xếp, bấm không đổi thứ tự\n"
     "- Chỉ cột Số tiền có mũi tên sắp xếp"),

    ("003", "Sắp xếp theo cột Số tiền", "P0",
     "Danh sách có nhiều hơn 1 trang, số tiền các phiếu khác nhau rõ rệt",
     "1. Bấm tiêu đề cột Số tiền\n"
     "2. Đọc cột Số tiền từ trên xuống\n"
     "3. Bấm lần nữa để đổi chiều",
     "—",
     "- Bảng sắp xếp đúng theo giá trị số tiền, tăng rồi giảm\n"
     "- Bảng KHÔNG báo lỗi tải dữ liệu\n"
     "- Mỗi lần bấm đều về trang 1"),

    ("004", "Chuyển trang giữ nguyên bộ lọc", "P0",
     "Đang lọc Loại phiếu = Điều chỉnh công nợ khách hàng, kết quả nhiều hơn 3 trang",
     "1. Sang trang 2, soát cột Loại phiếu\n"
     "2. Đọc ô hiển thị số dòng\n"
     "3. Sang trang 3 rồi quay về trang 1",
     "—",
     "- Mọi trang đều chỉ có phiếu khách hàng\n"
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

    ("007", "Menu hành động của từng dòng theo trạng thái", "P0",
     "4 dòng: (a) Đang tạo của chính mình; (b) Chờ tạo phiếu kế toán; (c) Từ chối của chính mình; "
     "(d) Đã duyệt phiếu kế toán. Người đăng nhập KHÔNG có quyền Kế toán thanh toán",
     "1. Mở menu bánh răng ở cột Hành động của từng dòng\n"
     "2. Ghi lại các mục trong menu",
     "4 trạng thái",
     "- (a) In, Xuất Excel, Sửa, Xóa\n"
     "- (b) In, Xuất Excel\n"
     "- (c) In, Xuất Excel, Sửa, Xóa\n"
     "- (d) In, Xuất Excel\n"
     "- Mọi dòng luôn có In và Xuất Excel"),

    ("008", "Kế toán thanh toán có thêm mục Tạo phiếu kế toán", "P0",
     "Tài khoản KT-1; 1 phiếu ở Chờ tạo phiếu kế toán và 1 phiếu ở Đã tạo phiếu kế toán",
     "1. Mở menu hành động của từng dòng",
     "—",
     "- Phiếu Chờ tạo phiếu kế toán: có thêm mục \"Tạo phiếu kế toán\"\n"
     "- Phiếu Đã tạo phiếu kế toán: KHÔNG có mục này\n"
     "- Bấm \"Tạo phiếu kế toán\" chuyển sang màn tạo Phiếu kế toán kèm sẵn phiếu yêu cầu"),

    ("009", "Nút Sửa và Xóa hiện sai với phiếu Đang tạo của người khác", "P0",
     "Tài khoản C nhìn thấy được một phiếu trạng thái Đang tạo do NV-B lập (dựng bằng cách mở màn Chờ "
     "duyệt rồi bỏ điều kiện trạng thái, hoặc nhờ đội kỹ thuật dựng dữ liệu)",
     "1. Tìm dòng phiếu nháp của NV-B\n"
     "2. Mở menu hành động\n"
     "3. So với một phiếu trạng thái Từ chối của NV-B",
     "—",
     "- ⚠️ Hiện trạng: phiếu Đang tạo của NGƯỜI KHÁC vẫn hiện đủ Sửa và Xóa\n"
     "- Phiếu Từ chối của người khác thì KHÔNG hiện 2 nút này\n"
     "- Hai trạng thái hành xử khác nhau — ghi nhận Failed, kỳ vọng đúng là cả hai đều phải xét người lập"),

    ("010", "Định dạng số tiền và ngày trên lưới", "P1",
     "Có phiếu tổng tiền lớn và phiếu tổng tiền 0",
     "1. Đọc cột Số tiền, Ngày lập, Ngày nhận của vài dòng",
     "—",
     "- Số tiền có dấu chấm ngăn nghìn, KHÔNG có phần thập phân\n"
     "- Phiếu tổng tiền 0 hiện 0, không để trống\n"
     "- Ngày lập và Ngày nhận dạng ngày/tháng/năm, KHÔNG có giờ phút"),

    ("011", "Xuất Excel danh sách theo bộ lọc hiện tại", "P0",
     "Đang lọc Loại phiếu = Điều chỉnh công nợ NCC, kết quả 7 phiếu",
     "1. Bấm nút Xuất excel\n"
     "2. Chờ tệp tải về, mở tệp\n"
     "3. Đếm số dòng và đối chiếu nội dung",
     "—",
     "- Mở TAB MỚI để tải, tệp tên danh_sach_yeu_cau_dieu_chinh_cong_no.xlsx\n"
     "- Tệp có đúng 7 dòng, đúng các phiếu đang hiện trên màn\n"
     "- 12 cột: STT, Mã phiếu, Số phiếu báo có, Loại phiếu, KH/NCC, Số tiền, Ngày lập, Người lập, "
     "Phòng ban, Ngày nhận, Người duyệt, Trạng thái"),

    ("012", "Phần đầu trang của tệp Excel danh sách lấy theo người đăng nhập", "P1",
     "Tài khoản có quyền xem tổng công ty, danh sách đang chứa phiếu của 3 công ty khác nhau",
     "1. Bấm Xuất excel, mở tệp\n"
     "2. Đọc phần đầu trang của tệp\n"
     "3. Đối chiếu với cột Phòng ban của các dòng bên dưới",
     "—",
     "- ⚠️ Hiện trạng: phần đầu trang chỉ ghi thông tin công ty của NGƯỜI ĐANG ĐĂNG NHẬP, trong khi các "
     "dòng bên dưới thuộc nhiều công ty. Ghi nhận và báo lại nghiệp vụ\n"
     "- Người xem trong phạm vi một công ty thì không gặp vấn đề này"),

    ("013", "Xuất Excel danh sách khi bảng rỗng", "P2",
     "Đang lọc bằng điều kiện không khớp phiếu nào",
     "1. Bấm nút Xuất excel\n"
     "2. Mở tệp",
     "—",
     "- Tệp vẫn tải về được, không báo lỗi\n"
     "- Bảng trong tệp chỉ có dòng tiêu đề, không có dòng dữ liệu"),
]
