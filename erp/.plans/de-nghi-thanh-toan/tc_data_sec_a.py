# -*- coding: utf-8 -*-
"""Section I, II, III — hien thi trang, bo loc, danh sach."""

SEC_I = [
    ("001", "Vào màn từ mục menu Công nợ - Thu - Chi", "P0",
     "Tài khoản bất kỳ đã đăng nhập",
     "1. Mở menu trên cùng, vào nhóm Công nợ - Thu - Chi\n"
     "2. Bấm mục Đề nghị thanh toán\n"
     "3. Quan sát tiêu đề trang và bảng",
     "—",
     "- Mở đúng màn Danh sách phiếu đề nghị thanh toán\n"
     "- Bảng nạp dữ liệu, không báo lỗi\n"
     "- Đây là chế độ \"Tất cả\": phạm vi phiếu theo quyền xem của người đăng nhập"),

    ("002", "Vào màn từ lối vào thứ hai trong nhóm Đề nghị", "P1",
     "Vẫn tài khoản ở TC_01.001",
     "1. Mở menu, vào nhóm chứa mục \"Đề nghị\"\n"
     "2. Bấm mục Đề nghị thanh toán\n"
     "3. So với kết quả của TC_01.001",
     "—",
     "- Mở đúng cùng một màn, cùng chế độ, cùng số tổng\n"
     "- Không mở nhầm sang màn Đề nghị thu tiền"),

    ("003", "Chế độ Phiếu của tôi khác chế độ Tất cả", "P0",
     "Tài khoản C có quyền xem theo công ty; công ty có 90 phiếu, C tự lập 9 phiếu",
     "1. Vào màn bằng mục menu (chế độ Tất cả), đọc số tổng\n"
     "2. Dán đường dẫn màn danh sách KHÔNG kèm tham số chế độ, đọc số tổng\n"
     "3. Soát cột Người lập ở chế độ thứ hai",
     "—",
     "- Chế độ Tất cả: tổng theo phạm vi công ty\n"
     "- Chế độ không kèm tham số: chỉ 9 phiếu, mọi dòng đều do C lập\n"
     "- Chế độ này hiện CẢ phiếu nháp của C"),

    ("004", "Bố cục mặc định của màn danh sách", "P0",
     "Tài khoản có quyền xem tổng công ty",
     "1. Mở màn Đề nghị thanh toán\n"
     "2. Quan sát từ trên xuống",
     "—",
     "- Phía trên bảng có nút \"Bộ lọc\" và nút \"Tạo mới\"\n"
     "- Khối tìm kiếm mặc định ĐANG THU GỌN\n"
     "- Bảng có các cột: STT, Mã phiếu, Loại chi, Hình thức thanh toán, Khách hàng, Số tiền, Ngày lập, "
     "Ngày nhận, Người lập, Phòng ban, Trạng thái, Hành động\n"
     "- Mặc định 10 dòng mỗi trang, phiếu mới nhất lên đầu"),

    ("005", "Cột Ngày nhận chỉ có dữ liệu sau khi trưởng phòng duyệt", "P1",
     "Có phiếu đang ở Chờ TP duyệt và phiếu đã qua bước trưởng phòng",
     "1. Tìm 1 phiếu ở Chờ TP duyệt, đọc cột Ngày nhận\n"
     "2. Tìm 1 phiếu ở Chờ kế toán công nợ duyệt trở đi, đọc cột Ngày nhận",
     "—",
     "- Phiếu chưa qua bước trưởng phòng: cột Ngày nhận TRỐNG\n"
     "- Phiếu đã qua: hiện ngày trưởng phòng bấm duyệt, dạng ngày/tháng/năm"),

    ("006", "Nhãn trạng thái hiển thị đúng cho cả 10 trạng thái", "P0",
     "Dữ liệu có phiếu ở nhiều trạng thái khác nhau",
     "1. Bấm Bộ lọc, mở ô Trạng thái, đếm số lựa chọn\n"
     "2. Chọn lần lượt từng trạng thái rồi tìm kiếm\n"
     "3. Quan sát nhãn ở cột Trạng thái",
     "10 trạng thái",
     "- Ô Trạng thái có đúng 10 lựa chọn: Đang tạo, Chờ TP duyệt, Chờ kế toán công nợ duyệt, Chờ kế "
     "toán trưởng duyệt, Chờ ban giám đốc duyệt, Chờ tạo phiếu chi, Chờ duyệt phiếu chi, Duyệt phiếu "
     "chi, Đã hủy, Không duyệt\n"
     "- CHỈ nhãn \"Duyệt phiếu chi\" tô XANH, chín nhãn còn lại tô ĐỎ\n"
     "- ⚠️ Trạng thái \"Đã hủy\" thường không có dữ liệu vì màn này không tạo ra nó — ghi Không áp dụng "
     "nếu môi trường test không có"),

    ("007", "Cột Số tiền đổi nguồn theo trạng thái phiếu", "P0",
     "Phiếu X: người lập đề nghị 20.000.000; trưởng phòng duyệt hạ xuống 15.000.000; kế toán công nợ "
     "duyệt hạ xuống 12.000.000; kế toán trưởng duyệt hạ xuống 10.000.000",
     "1. Ghi lại cột Số tiền của phiếu X ngay sau khi gửi duyệt\n"
     "2. Sau mỗi lần duyệt của từng cấp, quay lại danh sách và đọc lại cột Số tiền\n"
     "3. Ghi thành bảng 4 mốc",
     "20.000.000 → 15.000.000 → 12.000.000 → 10.000.000",
     "- Ở Chờ TP duyệt: hiện 20.000.000,00\n"
     "- Ở Chờ kế toán công nợ duyệt: hiện 15.000.000,00 (số trưởng phòng duyệt)\n"
     "- Ở Chờ kế toán trưởng duyệt: hiện 12.000.000,00 (số kế toán công nợ duyệt)\n"
     "- Ở Chờ tạo phiếu chi: hiện 10.000.000,00 (số kế toán trưởng duyệt)\n"
     "- ⚠️ Đúng thiết kế, KHÔNG ghi Failed"),

    ("008", "Cột Số tiền hiển thị kèm tên loại tiền", "P1",
     "Có phiếu loại tiền VND và phiếu loại tiền USD",
     "1. Tìm 2 phiếu trên trong danh sách\n"
     "2. Đọc cột Số tiền",
     "—",
     "- Số tiền có 2 chữ số thập phân và có tên loại tiền phía sau, ví dụ 15.000.000,00 VND và "
     "1.000,00 USD\n"
     "- Số của phiếu ngoại tệ là số NGUYÊN TỆ, không phải số quy đổi"),

    ("009", "Cột Khách hàng đổi nguồn theo loại chi và hình thức thanh toán", "P0",
     "4 phiếu: (a) Chi trả nhà cung cấp - TM; (b) Chi trả nhà cung cấp - CK; (c) Chi trả lại khách "
     "hàng - TM; (d) Thanh toán chi phí vận chuyển NCC",
     "1. Tìm 4 phiếu trên trong danh sách\n"
     "2. Đọc cột Khách hàng của từng dòng\n"
     "3. Mở chi tiết từng phiếu để đối chiếu",
     "4 tổ hợp",
     "- (a) hiện nhà cung cấp của DÒNG CHI TIẾT ĐẦU TIÊN\n"
     "- (b) hiện nhà cung cấp ghi ở ĐẦU PHIẾU\n"
     "- (c) hiện khách hàng của dòng chi tiết đầu tiên\n"
     "- (d) hiện nhà cung cấp ghi ở đầu phiếu\n"
     "- ⚠️ Cột tên là \"Khách hàng\" nhưng nội dung có thể là nhà cung cấp — không phải lỗi"),

    ("010", "Phiếu loại Chi khác và Chi thu nhập cho nhân viên vẫn hiển thị", "P2",
     "Kho dữ liệu có phiếu cũ loại Chi khác hoặc Chi thu nhập cho nhân viên (nếu không có thì ghi "
     "Không áp dụng)",
     "1. Lọc Loại chi = Chi khác ở màn danh sách\n"
     "2. Đọc cột Loại chi và cột Khách hàng\n"
     "3. Mở màn Chờ duyệt, mở ô Loại chi, tìm mục Chi thu nhập cho nhân viên",
     "—",
     "- Phiếu cũ hiện đúng nhãn loại chi\n"
     "- Cột Khách hàng của loại Chi khác để TRỐNG\n"
     "- Ô Loại chi ở màn Chờ duyệt CÓ mục Chi thu nhập cho nhân viên, ô lọc ở màn danh sách thì KHÔNG"),

    ("011", "Bấm mã phiếu mở màn chi tiết", "P1",
     "Danh sách đang có phiếu",
     "1. Bấm vào Mã phiếu ở dòng đầu\n"
     "2. Quan sát trang mở ra",
     "—",
     "- Mở màn Chi tiết phiếu đề nghị thanh toán đúng phiếu vừa bấm\n"
     "- Mã phiếu trên màn chi tiết khớp với dòng vừa bấm"),

    ("012", "Bảng rỗng khi bộ lọc không khớp phiếu nào", "P1",
     "Danh sách đang có dữ liệu",
     "1. Bấm Bộ lọc, gõ chuỗi chắc chắn không tồn tại vào ô Mã phiếu\n"
     "2. Bấm nút tìm kiếm",
     "Mã phiếu: ZZZZ-KHONG-TON-TAI",
     "- Bảng hiện dòng báo không có dữ liệu\n"
     "- Tổng hiện 0, không có lỗi đỏ\n"
     "- Nút Tạo mới vẫn còn"),

    ("013", "Danh sách vẫn tải được khi phiếu thiếu loại tiền", "P2",
     "Phiếu cũ có ô Loại tiền để trống hoặc trỏ tới loại tiền đã bị xóa khỏi danh mục (nếu không dựng "
     "được thì ghi Không áp dụng)",
     "1. Mở màn danh sách ở phạm vi có chứa phiếu đó\n"
     "2. Quan sát bảng",
     "—",
     "- ⚠️ Điểm rủi ro: nếu bảng KHÔNG tải được và báo lỗi toàn màn thì ghi Failed kèm ảnh chụp\n"
     "- Kỳ vọng đúng: chỉ dòng đó hiển thị thiếu tên loại tiền, các dòng khác vẫn bình thường"),
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
     "- Có các ô: Công ty, Phòng ban, Từ ngày, Đến ngày, Mã phiếu, Lý do chi, Số tiền đề nghị thanh "
     "toán từ, Số tiền đề nghị thanh toán đến, Loại chi, Hình thức thanh toán, Người lập, Trạng thái, "
     "Khách hàng, Nhà cung cấp\n"
     "- Có 2 nút: tìm kiếm và làm mới"),

    ("003", "Màn Chờ duyệt có ô lọc Phòng ban riêng", "P1",
     "Tài khoản KTCN-1, đang ở màn Chờ duyệt",
     "1. Bấm Bộ lọc\n"
     "2. Ghi lại các ô lọc, so với màn danh sách",
     "—",
     "- Có ô Phòng ban (danh sách đầy đủ mọi phòng ban), dù người dùng không có quyền xem theo cấp\n"
     "- KHÔNG có ô Công ty và ô Bộ phận\n"
     "- Vẫn có ô Trạng thái"),

    ("004", "Ô Loại chi của 3 màn có số lựa chọn khác nhau", "P0",
     "Tài khoản có đủ quyền để mở cả 3 màn",
     "1. Ở màn nhập (Tạo mới), mở ô Loại chi, ghi lại danh sách\n"
     "2. Ở màn danh sách, bấm Bộ lọc, mở ô Loại chi, ghi lại\n"
     "3. Ở màn Chờ duyệt, bấm Bộ lọc, mở ô Loại chi, ghi lại",
     "3 màn",
     "- Màn nhập: 4 lựa chọn — Chi trả nhà cung cấp, Chi trả lại khách hàng, Chi thưởng thực hiện hợp "
     "đồng, Thanh toán chi phí vận chuyển NCC\n"
     "- Ô lọc màn danh sách: 6 lựa chọn — thêm Chi thưởng NVKD và Chi khác\n"
     "- Ô lọc màn Chờ duyệt: 7 lựa chọn — thêm Chi thu nhập cho nhân viên\n"
     "- ⚠️ Đây là hiện trạng, ghi nhận đúng số lượng từng màn"),

    ("005", "Lọc theo Mã phiếu tìm được khớp một phần", "P0",
     "Có phiếu mã kết thúc bằng .00023",
     "1. Gõ 00023 vào ô Mã phiếu\n"
     "2. Bấm nút tìm kiếm",
     "Mã phiếu: 00023",
     "- Chỉ còn phiếu có chuỗi 00023 nằm trong mã\n"
     "- Bảng về trang 1, tổng đổi theo"),

    ("006", "Bộ lọc chỉ chạy khi bấm nút tìm kiếm", "P0",
     "Khối lọc đang bung",
     "1. Gõ 00023 vào ô Mã phiếu, KHÔNG bấm gì thêm, chờ 5 giây\n"
     "2. Bấm nút tìm kiếm",
     "—",
     "- Trong lúc gõ, bảng KHÔNG đổi\n"
     "- Chỉ sau khi bấm nút tìm kiếm bảng mới lọc lại"),

    ("007", "Lọc theo Lý do chi", "P1",
     "Có phiếu Lý do chi chứa cụm \"cước vận chuyển\"",
     "1. Gõ \"cước vận chuyển\" vào ô Lý do chi, tìm kiếm\n"
     "2. Mở chi tiết vài dòng kết quả để đối chiếu\n"
     "3. Gõ một phần cụm từ (ví dụ \"vận chuyển\"), tìm lại",
     "Lý do chi: cước vận chuyển",
     "- Chỉ ra phiếu có Lý do chi chứa chuỗi vừa gõ\n"
     "- Gõ một phần vẫn ra kết quả\n"
     "- Không phân biệt vị trí chuỗi nằm ở đầu hay giữa"),

    ("008", "Lọc theo Loại chi", "P0",
     "Dữ liệu có phiếu ở nhiều loại chi",
     "1. Chọn Loại chi = Chi trả nhà cung cấp, tìm kiếm, soát cột Loại chi\n"
     "2. Đổi sang Thanh toán chi phí vận chuyển NCC, tìm kiếm, soát lại",
     "2 loại chi",
     "- Mỗi lần lọc, mọi dòng đều đúng loại chi vừa chọn\n"
     "- Không lẫn loại chi khác"),

    ("009", "Lọc theo Hình thức thanh toán", "P0",
     "Dữ liệu có cả phiếu TM và CK",
     "1. Chọn Hình thức thanh toán = TM, tìm kiếm\n"
     "2. Đổi sang CK, tìm kiếm",
     "TM → CK",
     "- Ô lọc có đúng 2 lựa chọn: TM và CK\n"
     "- Mọi dòng kết quả đều đúng hình thức đang chọn"),

    ("010", "Lọc theo Trạng thái", "P0",
     "Dữ liệu có phiếu ở nhiều trạng thái",
     "1. Chọn Trạng thái = Chờ TP duyệt, tìm kiếm\n"
     "2. Lặp lại với Chờ tạo phiếu chi và Không duyệt",
     "3 trạng thái",
     "- Mỗi lần lọc, mọi dòng đều đúng trạng thái đang chọn\n"
     "- Lọc Đang tạo ở chế độ Tất cả chỉ ra phiếu nháp của chính người đăng nhập"),

    ("011", "Lọc theo Người lập", "P1",
     "NV-B đã lập 7 phiếu trong phạm vi người đăng nhập nhìn thấy",
     "1. Bấm ô Người lập, gõ tên NV-B, chọn từ gợi ý\n"
     "2. Bấm tìm kiếm, đọc cột Người lập",
     "Người lập: NV-B",
     "- Mọi dòng đều có Người lập là NV-B\n"
     "- Số dòng khớp số phiếu của NV-B trong phạm vi được xem"),

    ("012", "Lọc theo Khách hàng quét cả đầu phiếu lẫn dòng chi tiết", "P0",
     "Khách hàng KH-001: xuất hiện ở ĐẦU PHIẾU của phiếu M (Chi trả lại khách hàng - CK) và xuất hiện "
     "ở DÒNG CHI TIẾT của phiếu N (Chi trả lại khách hàng - TM)",
     "1. Bấm ô Khách hàng, gõ từ khóa, chọn KH-001\n"
     "2. Bấm tìm kiếm\n"
     "3. Tìm phiếu M và phiếu N trong kết quả",
     "Khách hàng: KH-001",
     "- Cả phiếu M và phiếu N đều CÓ trong kết quả\n"
     "- Mỗi phiếu chỉ hiện một dòng, không nhân đôi"),

    ("013", "Lọc theo Nhà cung cấp quét cả đầu phiếu lẫn dòng chi tiết", "P0",
     "Nhà cung cấp NCC-01: ở đầu phiếu của một phiếu Chi trả nhà cung cấp - CK, và ở dòng chi tiết của "
     "một phiếu Chi trả nhà cung cấp - TM",
     "1. Mở ô Nhà cung cấp, chọn NCC-01, tìm kiếm\n"
     "2. Soát kết quả và mở chi tiết để đối chiếu",
     "Nhà cung cấp: NCC-01",
     "- Ô Nhà cung cấp là danh sách chọn sẵn (không phải gõ tìm)\n"
     "- Cả 2 phiếu đều có trong kết quả"),

    ("014", "Lọc theo khoảng Số tiền đề nghị thanh toán", "P0",
     "Có phiếu tổng đề nghị 5.000.000; có phiếu 20.000.000; có phiếu 90.000.000",
     "1. Nhập Số tiền đề nghị thanh toán từ = 10.000.000, để trống ô đến, tìm kiếm\n"
     "2. Nhập thêm ô đến = 50.000.000, tìm kiếm",
     "Từ 10.000.000 · Đến 50.000.000",
     "- Bước 1: mất phiếu 5.000.000; còn phiếu 20.000.000 và 90.000.000\n"
     "- Bước 2: chỉ còn phiếu trong đoạn 10.000.000 đến 50.000.000, tính cả 2 đầu mút"),

    ("015", "Khoảng tiền luôn so với số đề nghị ban đầu, không đổi theo trạng thái", "P0",
     "Phiếu X: người lập đề nghị 20.000.000, đã qua các cấp duyệt và hiện còn 10.000.000; phiếu đang ở "
     "Chờ tạo phiếu chi",
     "1. Đọc cột Số tiền của phiếu X ngoài danh sách\n"
     "2. Lọc khoảng tiền từ 18.000.000 đến 22.000.000, tìm kiếm\n"
     "3. Lọc khoảng tiền từ 9.000.000 đến 11.000.000, tìm kiếm",
     "Hai khoảng lọc",
     "- Cột Số tiền hiện 10.000.000,00 (số kế toán trưởng duyệt)\n"
     "- Bước 2: phiếu X CÓ trong kết quả (khớp số đề nghị ban đầu 20.000.000)\n"
     "- Bước 3: phiếu X KHÔNG có trong kết quả\n"
     "- ⚠️ Bộ lọc và cột hiển thị dùng hai nguồn số khác nhau — bẫy dễ báo lỗi oan"),

    ("016", "Khoảng tiền trên phiếu ngoại tệ so số quy đổi", "P0",
     "Phiếu Z loại tiền USD, 1 dòng đề nghị 1.000 USD, tỷ giá 25.000 nên quy đổi 25.000.000",
     "1. Lọc khoảng tiền từ 20.000.000 đến 30.000.000, tìm phiếu Z\n"
     "2. Lọc khoảng tiền từ 500 đến 2.000, tìm lại",
     "Hai khoảng lọc",
     "- Bước 1: phiếu Z CÓ trong kết quả\n"
     "- Bước 2: phiếu Z KHÔNG có trong kết quả\n"
     "- ⚠️ Bộ lọc so số đã quy đổi VND, trong khi cột Số tiền hiển thị số nguyên tệ"),

    ("017", "Lọc theo Từ ngày", "P0",
     "Có phiếu lập ngày 31/07/2026 và phiếu lập ngày 05/08/2026",
     "1. Nhập Từ ngày = 01/08/2026, tìm kiếm\n"
     "2. Đọc cột Ngày lập của dòng cũ nhất trong kết quả",
     "Từ ngày: 01/08/2026",
     "- Phiếu 31/07/2026 bị loại\n"
     "- Phiếu 05/08/2026 còn trong kết quả"),

    ("018", "Ô Đến ngày làm rụng trọn ngày cuối", "P0",
     "Có phiếu lập lúc 09:15 ngày 31/08/2026 và phiếu lập ngày 30/08/2026",
     "1. Nhập Đến ngày = 31/08/2026, tìm kiếm\n"
     "2. Tìm phiếu lập ngày 31/08/2026 trong kết quả\n"
     "3. Đổi Đến ngày = 01/09/2026, tìm lại",
     "Đến ngày: 31/08/2026, rồi 01/09/2026",
     "- ⚠️ Hiện trạng: đặt Đến ngày 31/08/2026 thì phiếu lập trong chính ngày 31/08 BỊ MẤT; phải đặt "
     "01/09/2026 mới thấy. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: Đến ngày phải tính trọn ngày đó\n"
     "- Phiếu 30/08/2026 có mặt ở cả 2 lần"),

    ("019", "Kết hợp nhiều điều kiện lọc cùng lúc", "P0",
     "Có ít nhất 2 phiếu Chi trả nhà cung cấp, hình thức CK, trạng thái Chờ tạo phiếu chi",
     "1. Chọn Loại chi = Chi trả nhà cung cấp\n"
     "2. Chọn Hình thức thanh toán = CK\n"
     "3. Chọn Trạng thái = Chờ tạo phiếu chi\n"
     "4. Bấm tìm kiếm, kiểm TỪNG dòng kết quả",
     "3 điều kiện cùng lúc",
     "- Mọi dòng thỏa ĐỒNG THỜI cả 3 điều kiện\n"
     "- ⚠️ Kiểm từng dòng, đừng chỉ nhìn số tổng"),

    ("020", "Nút làm mới xóa sạch điều kiện lọc", "P0",
     "Đang lọc bằng ít nhất 4 điều kiện",
     "1. Bấm nút làm mới (biểu tượng mũi tên tròn)\n"
     "2. Quan sát các ô lọc và bảng",
     "—",
     "- Mọi ô lọc về trống, kể cả ô chọn Khách hàng và Nhà cung cấp\n"
     "- Bảng nạp lại đầy đủ từ trang 1"),

    ("021", "Đổi Công ty thì danh sách Phòng ban đổi theo", "P1",
     "Tài khoản có quyền xem tổng công ty",
     "1. Chọn Công ty A, mở ô Phòng ban, ghi lại danh sách\n"
     "2. Đổi Công ty sang B, mở lại ô Phòng ban",
     "Công ty A → B",
     "- Danh sách Phòng ban đổi theo công ty đang chọn\n"
     "- Không còn phòng ban của công ty A trong danh sách"),

    ("022", "Bộ lọc được ghi nhớ và ghi nhớ riêng cho từng chế độ", "P1",
     "Tài khoản KT-ALL mở được cả màn danh sách và màn Chờ duyệt",
     "1. Ở chế độ Tất cả, lọc Loại chi = Chi trả nhà cung cấp\n"
     "2. Sang màn Chờ duyệt, bấm Bộ lọc, quan sát\n"
     "3. Quay lại chế độ Tất cả",
     "—",
     "- Màn Chờ duyệt mở ra với bộ lọc TRẮNG\n"
     "- Quay lại chế độ Tất cả vẫn còn điều kiện Loại chi = Chi trả nhà cung cấp\n"
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
     "1. Bấm lần lượt tiêu đề các cột: Mã phiếu, Loại chi, Hình thức thanh toán, Khách hàng, Ngày lập, "
     "Ngày nhận, Người lập, Phòng ban, Trạng thái\n"
     "2. Quan sát thứ tự dòng sau mỗi lần bấm\n"
     "3. Bấm tiêu đề cột Số tiền",
     "—",
     "- Chín cột ở bước 1 KHÔNG có mũi tên sắp xếp, bấm không đổi thứ tự\n"
     "- Chỉ cột Số tiền có mũi tên sắp xếp"),

    ("003", "Sắp xếp theo cột Số tiền", "P0",
     "Danh sách có nhiều hơn 1 trang, số tiền các phiếu khác nhau rõ rệt",
     "1. Bấm tiêu đề cột Số tiền\n"
     "2. Đọc cột Số tiền từ trên xuống\n"
     "3. Bấm lần nữa để đổi chiều",
     "—",
     "- Bảng sắp xếp đúng theo giá trị số tiền, tăng rồi giảm\n"
     "- Bảng KHÔNG báo lỗi tải dữ liệu\n"
     "- ⚠️ Điểm rủi ro: cột Số tiền là số cộng dồn, không phải dữ liệu gốc. Nếu bảng báo lỗi hoặc thứ "
     "tự không đổi thì ghi Failed kèm ảnh chụp"),

    ("004", "Chuyển trang giữ nguyên bộ lọc", "P0",
     "Đang lọc Loại chi = Chi trả nhà cung cấp, kết quả nhiều hơn 3 trang",
     "1. Sang trang 2, soát cột Loại chi\n"
     "2. Đọc ô hiển thị số dòng\n"
     "3. Sang trang 3 rồi quay về trang 1",
     "—",
     "- Mọi trang đều chỉ có Chi trả nhà cung cấp\n"
     "- Tổng N giữ nguyên, khoảng a đến b đổi theo trang\n"
     "- Chuyển trang không làm mất điều kiện lọc"),

    ("005", "Cột STT đánh số liên tục theo trang", "P0",
     "10 dòng mỗi trang, kết quả hơn 20 dòng",
     "1. Đọc STT dòng cuối trang 1\n"
     "2. Sang trang 2, đọc STT dòng đầu và dòng cuối",
     "10 dòng mỗi trang",
     "- Trang 1 kết thúc ở 10\n"
     "- Trang 2 chạy từ 11 tới 20"),

    ("006", "Đổi số dòng mỗi trang", "P0",
     "Kết quả hơn 100 dòng, đang ở trang 3",
     "1. Đổi số dòng mỗi trang sang 25\n"
     "2. Quan sát trang hiện tại và số dòng\n"
     "3. Đổi tiếp sang 100",
     "25 rồi 100 dòng mỗi trang",
     "- Mỗi lần đổi đều quay về trang 1\n"
     "- Số dòng trên màn đúng bằng số vừa chọn (trừ trang cuối)\n"
     "- Ô hiển thị số dòng cập nhật theo"),

    ("007", "Menu hành động của từng dòng theo trạng thái", "P0",
     "4 dòng: (a) Đang tạo của chính mình; (b) Chờ TP duyệt; (c) Không duyệt của chính mình; (d) Duyệt "
     "phiếu chi. Người đăng nhập KHÔNG có quyền Kế toán thanh toán",
     "1. Mở menu bánh răng ở cột Hành động của từng dòng\n"
     "2. Ghi lại các mục trong menu",
     "4 trạng thái",
     "- (a) In, Xuất Excel, Sửa, Xóa\n"
     "- (b) In, Xuất Excel\n"
     "- (c) In, Xuất Excel, Sửa, Xóa\n"
     "- (d) In, Xuất Excel\n"
     "- Mọi dòng luôn có In và Xuất Excel"),

    ("008", "Menu hành động của kế toán thanh toán trên phiếu chờ tạo phiếu chi", "P0",
     "Tài khoản KTTT-1 có quyền Kế toán thanh toán; 2 phiếu ở Chờ tạo phiếu chi, một phiếu TM và một "
     "phiếu CK",
     "1. Mở menu hành động của từng dòng",
     "TM và CK",
     "- Dòng TM: In, Xuất Excel, Tạo phiếu chi, Không duyệt\n"
     "- Dòng CK: In, Xuất Excel, Tạo phiếu ủy nhiệm chi, Không duyệt\n"
     "- Mục \"Không duyệt\" chỉ dẫn sang màn chi tiết, không tự thực hiện ngay"),

    ("009", "Nút Sửa và Xóa không hiện trên phiếu của người khác", "P0",
     "Tài khoản C có quyền xem theo công ty; phiếu W trạng thái Không duyệt do NV-B lập, cùng công ty",
     "1. Đăng nhập bằng C, tìm phiếu W\n"
     "2. Mở menu hành động của dòng phiếu W\n"
     "3. Mở màn chi tiết phiếu W, quan sát hàng nút",
     "Phiếu W của NV-B, trạng thái Không duyệt",
     "- Menu chỉ có In và Xuất Excel, KHÔNG có Sửa và Xóa\n"
     "- Màn chi tiết cũng không có nút Sửa và Xóa\n"
     "- ⚠️ Khác với màn Đề nghị thu tiền: màn này CÓ xét người lập"),

    ("010", "Định dạng số tiền và ngày trên lưới", "P1",
     "Có phiếu tổng tiền tròn và phiếu có phần lẻ",
     "1. Đọc cột Số tiền, Ngày lập, Ngày nhận của vài dòng",
     "—",
     "- Số tiền có dấu chấm ngăn nghìn, LUÔN 2 chữ số thập phân, kèm tên loại tiền\n"
     "- Ngày lập và Ngày nhận dạng ngày/tháng/năm, KHÔNG có giờ phút"),

    ("011", "Ô tìm kiếm nhanh sẵn có của bảng", "P2",
     "Danh sách đang có dữ liệu",
     "1. Tìm ô tìm kiếm nhanh ở góc bảng (nếu có)\n"
     "2. Gõ một mã phiếu vào đó",
     "—",
     "- Ghi nhận hành vi thực tế: có lọc được hay không\n"
     "- Không được làm bảng báo lỗi"),

    ("012", "Danh sách nạp lại sau khi phiếu đổi trạng thái", "P1",
     "Đang mở màn danh sách; ở tab khác, một cấp vừa duyệt một phiếu đang hiện trên màn",
     "1. Bấm nút tìm kiếm để nạp lại\n"
     "2. Đọc cột Trạng thái và cột Số tiền của phiếu đó",
     "—",
     "- Trạng thái cập nhật sang bước mới\n"
     "- Cột Số tiền đổi sang nguồn tương ứng bước mới (mục 6)"),
]
