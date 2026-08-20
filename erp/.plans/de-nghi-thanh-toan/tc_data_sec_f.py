# -*- coding: utf-8 -*-
"""Section IX (co lap du lieu, thao tac dong thoi) va X (luong nghiep vu dau - cuoi)."""

SEC_IX = [
    ("001", "Hai người cùng lập phiếu tại một thời điểm", "P0",
     "2 tài khoản cùng công ty, cùng chuẩn bị sẵn form Tạo mới hợp lệ",
     "1. Cả 2 bấm Lưu gần như cùng lúc\n"
     "2. Đối chiếu mã của 2 phiếu vừa tạo\n"
     "3. Lặp lại 3 lần để tăng khả năng va chạm",
     "2 phiếu tạo đồng thời",
     "- Cả 2 phiếu đều lưu thành công\n"
     "- ⚠️ Mã phiếu sinh không có khóa chống va chạm: nếu 2 phiếu ra TRÙNG mã thì ghi Failed kèm ảnh "
     "chụp; nếu 2 mã liên tiếp thì đạt"),

    ("002", "Mã phiếu trùng tiền tố với màn Đề nghị thu tiền", "P1",
     "Cùng một công ty, cùng tháng; đã có phiếu đề nghị thu tiền mã kết thúc .00007",
     "1. Lập một phiếu đề nghị thanh toán mới\n"
     "2. So mã phiếu vừa tạo với mã phiếu đề nghị thu tiền\n"
     "3. Tìm mã đó trên cả hai màn",
     "—",
     "- Hai màn dùng CÙNG tiền tố mã công ty + DNTT + tháng năm nhưng đếm số riêng\n"
     "- Có thể tồn tại hai phiếu khác nhau MANG CÙNG MỘT MÃ ở hai màn\n"
     "- ⚠️ Ghi nhận đúng hiện trạng và nêu rủi ro nhầm lẫn khi trao đổi qua mã phiếu"),

    ("003", "Chống bấm Lưu nhiều lần liên tiếp", "P0",
     "Màn Tạo mới đã điền hợp lệ",
     "1. Bấm nút Lưu liên tục 3 lần thật nhanh\n"
     "2. Quan sát thông báo\n"
     "3. Mở danh sách, đếm số phiếu vừa tạo",
     "—",
     "- Nút chuyển sang trạng thái đang xử lý sau lần bấm đầu\n"
     "- Nếu bấm lại thì hiện cảnh báo \"Đang xử lý, vui lòng chờ...\"\n"
     "- CHỈ MỘT phiếu được tạo; nếu ra 2 hoặc 3 phiếu thì ghi Failed"),

    ("004", "Hai cấp cùng thao tác trên một phiếu", "P0",
     "Mở 2 tab cùng một phiếu ở Chờ kế toán công nợ duyệt: tab 1 dùng KTCN-1, tab 2 dùng KTCN-2 (cùng "
     "quyền kế toán công nợ)",
     "1. Tab 1 nhập số tiền và bấm KT công nợ duyệt\n"
     "2. Tab 2 (chưa tải lại) cũng nhập số khác và bấm KT công nợ duyệt\n"
     "3. Mở lại phiếu, đọc Trạng thái và cột KT công nợ duyệt",
     "—",
     "- ⚠️ Hiện trạng: tab 2 vẫn thực hiện được, ghi đè số tiền và đẩy phiếu tiếp một bước nữa. Ghi "
     "nhận Failed kèm số liệu cụ thể\n"
     "- Kỳ vọng đúng: tab 2 bị báo phiếu đã rời bước, không cho thao tác"),

    ("005", "Người lập sửa phiếu trong khi cấp trên đang duyệt", "P0",
     "Mở 2 tab: tab 1 là màn Sửa phiếu nháp của NV-A; tab 2 dùng chính NV-A gửi duyệt phiếu đó",
     "1. Tab 2 gửi duyệt phiếu\n"
     "2. Tab 1 sửa Lý do chi rồi bấm Lưu\n"
     "3. Mở lại phiếu, đọc Trạng thái và Lý do chi",
     "—",
     "- ⚠️ Hiện trạng: tab 1 lưu ĐÈ được, phiếu quay lại trạng thái Đang tạo và mất trạng thái Chờ TP "
     "duyệt. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: chặn lưu vì phiếu đã rời trạng thái cho phép sửa"),

    ("006", "Không duyệt phiếu đã rời bước", "P0",
     "Phiếu đang ở Chờ kế toán trưởng duyệt; KTCN-1 vẫn mở được chi tiết vì đã duyệt bước trước",
     "1. KTT-1 duyệt phiếu ở tab 1\n"
     "2. Ở tab 2 của KTCN-1 (chưa tải lại), thử tìm nút Không duyệt\n"
     "3. Nếu nút còn, bấm và xác nhận",
     "—",
     "- Nút Không duyệt lẽ ra đã không hiện với KTCN-1\n"
     "- Nếu bấm được và phiếu bị đẩy sang Không duyệt sau khi đã duyệt xong thì ghi Failed"),

    ("007", "Phạm vi dữ liệu không rò rỉ giữa các công ty", "P0",
     "Tài khoản chỉ có quyền xem theo công ty, thuộc công ty 3",
     "1. Lọc Lý do chi bằng một cụm từ chỉ có ở phiếu của công ty 1\n"
     "2. Lọc Khách hàng bằng một khách hàng chỉ có ở công ty 1\n"
     "3. Nhập khoảng tiền rất rộng từ 0 đến 999.999.999.999",
     "—",
     "- Cả 3 cách đều không làm lộ phiếu của công ty 1\n"
     "- Tổng luôn nằm trong phạm vi công ty 3"),

    ("008", "Màn Chờ duyệt không lộ phiếu ngoài công ty", "P0",
     "KTCN-1 thuộc công ty 3; công ty 1 cũng có phiếu ở bước Chờ kế toán công nợ duyệt",
     "1. Mở màn Chờ duyệt\n"
     "2. Dùng ô lọc Phòng ban chọn một phòng ban của CÔNG TY KHÁC (danh sách ô này liệt kê mọi phòng "
     "ban)\n"
     "3. Bấm tìm kiếm",
     "—",
     "- Kết quả rỗng, không lộ phiếu của công ty khác\n"
     "- ⚠️ Nếu ra phiếu của công ty khác thì ghi Failed"),

    ("009", "Đổi tỷ giá trong danh mục không làm đổi phiếu đã lưu", "P1",
     "Phiếu ngoại tệ đã lưu với tỷ giá 25.000; sau đó danh mục đổi tỷ giá loại tiền đó thành 26.000",
     "1. Mở màn chi tiết phiếu, đọc Tỷ giá và cột quy đổi\n"
     "2. Đọc cột Số tiền ngoài danh sách\n"
     "3. Mở bản in, đọc các số tiền",
     "—",
     "- Tỷ giá và số quy đổi trong phiếu GIỮ NGUYÊN theo lúc lập\n"
     "- Ghi nhận thực tế bản in có lấy đúng tỷ giá của phiếu hay không"),

    ("010", "Xóa phiếu xong danh sách nạp lại đúng số tổng", "P1",
     "Đang lọc Trạng thái = Đang tạo, có 5 phiếu",
     "1. Xóa 1 phiếu\n"
     "2. Đọc lại số tổng và các ô lọc",
     "—",
     "- Tổng còn 4\n"
     "- Ghi nhận thực tế bộ lọc Trạng thái có được giữ lại hay không"),

    ("011", "Mở màn Sửa phiếu của nhân sự không còn phòng ban", "P2",
     "Phiếu do một nhân viên đã bị gỡ khỏi phòng ban lập",
     "1. Mở màn Sửa hoặc màn Chi tiết phiếu đó",
     "—",
     "- Ghi nhận đúng hiện trạng: màn mở được với ô Phòng ban trống, hay hệ thống báo lỗi trang\n"
     "- Nếu báo lỗi trang thì ghi Failed"),
]

SEC_X = [
    ("001", "Vòng đời đầy đủ đi qua kế toán trưởng, không qua ban giám đốc", "P0",
     "NV-A thuộc phòng P1 công ty 3; TP-1 quản lý P1; KTCN-1, KTT-1, KTTT-1 cùng công ty; KH-001 có "
     "hợp đồng do NV-A lập",
     "1. NV-A tạo phiếu Chi trả lại khách hàng, hình thức TM, 2 dòng tổng 15.000.000, bấm Lưu\n"
     "2. NV-A mở lại phiếu, bấm Sửa, chỉnh số tiền dòng 1, bấm Lưu và gửi duyệt\n"
     "3. TP-1 mở phiếu ở màn Chờ duyệt, nhập cột TP duyệt và ghi chú, bấm TP Duyệt\n"
     "4. KTCN-1 mở phiếu, nhập cột KT công nợ duyệt, bấm KT công nợ duyệt\n"
     "5. KTT-1 mở phiếu, nhập cột KT trưởng/BGD, bấm KT Trưởng Duyệt\n"
     "6. KTTT-1 mở phiếu, bấm Tạo phiếu chi",
     "Vòng đời một phiếu, 5 bước",
     "- Bước 1: Đang tạo, chỉ NV-A nhìn thấy ở chế độ Tất cả, có nút Sửa và Xóa\n"
     "- Bước 2: Chờ TP duyệt, nút Sửa và Xóa biến mất, TP-1 nhận thông báo\n"
     "- Bước 3: Chờ kế toán công nợ duyệt, cột Ngày nhận có dữ liệu, cột Số tiền đổi sang số TP duyệt\n"
     "- Bước 4: Chờ kế toán trưởng duyệt, cột Số tiền đổi sang số KT công nợ duyệt\n"
     "- Bước 5: nhảy THẲNG sang Chờ tạo phiếu chi, bỏ qua bước ban giám đốc\n"
     "- Bước 6: chuyển sang màn tạo Phiếu chi với phiếu đã gắn sẵn\n"
     "- Ở mỗi bước, người lập và các cấp đã duyệt đều nhận được thông báo tương ứng"),

    ("002", "Vòng đời đi qua ban giám đốc", "P0",
     "Phiếu đang ở Chờ kế toán trưởng duyệt; BGD-1 có quyền ban giám đốc",
     "1. KTT-1 bấm Chuyển duyệt BGĐ\n"
     "2. BGD-1 mở phiếu ở màn Chờ duyệt, nhập ghi chú và số tiền, bấm BGD Duyệt\n"
     "3. KTTT-1 mở màn Chờ duyệt",
     "—",
     "- Sau bước 1: Chờ ban giám đốc duyệt, BGD-1 nhận thông báo\n"
     "- Sau bước 2: Chờ tạo phiếu chi\n"
     "- KTTT-1 thấy phiếu trong màn Chờ duyệt của mình\n"
     "- Màn chi tiết lưu đủ cả 4 ô ghi chú duyệt của 4 cấp"),

    ("003", "Vòng đời bị từ chối rồi lập lại", "P0",
     "NV-A và TP-1 như TC_10.001",
     "1. NV-A lập phiếu và gửi duyệt\n"
     "2. TP-1 nhập Ghi chú không duyệt \"Thiếu chứng từ\", bấm Không duyệt, xác nhận\n"
     "3. NV-A kiểm chuông thông báo\n"
     "4. NV-A mở chi tiết phiếu, đọc Ghi chú không duyệt, bấm Sửa, bổ sung rồi Lưu và gửi duyệt\n"
     "5. TP-1 duyệt lại",
     "—",
     "- Bước 2: phiếu chuyển sang Không duyệt, TP-1 được đưa về chế độ Đã xử lý\n"
     "- Bước 3: ⚠️ NV-A KHÔNG nhận được thông báo nào — ghi nhận Failed (mục 9 ghi chú 3)\n"
     "- Bước 4: phiếu quay lại Chờ TP duyệt, nút Sửa và Xóa lại biến mất\n"
     "- Bước 5: phiếu chạy tiếp bình thường, Ghi chú không duyệt cũ vẫn còn trên phiếu"),

    ("004", "Vòng đời phiếu Chi trả nhà cung cấp bằng chuyển khoản", "P0",
     "NV-A; nhà cung cấp NCC-01 trong nước có hợp đồng mua đã duyệt và có tài khoản ngân hàng trong "
     "hồ sơ",
     "1. Tạo phiếu Chi trả nhà cung cấp, hình thức CK\n"
     "2. Chọn NCC-01 ở đầu phiếu, kiểm các ô ngân hàng có tự điền không\n"
     "3. Thêm 2 dòng chi tiết, chọn 2 hợp đồng mua khác nhau, nhập số tiền\n"
     "4. Đính kèm 1 tệp pdf, bấm Lưu và gửi duyệt\n"
     "5. Chạy hết dây chuyền duyệt tới bước kế toán thanh toán\n"
     "6. Mở bản in và xuất Excel",
     "2 hợp đồng mua, 1 tệp đính kèm",
     "- Ô Nhà cung cấp nằm ở ĐẦU PHIẾU, bảng chi tiết không có cột Nhà cung cấp\n"
     "- Thông tin ngân hàng tự điền nếu hồ sơ có sẵn\n"
     "- Cột đối tượng ngoài danh sách hiện nhà cung cấp ghi ở đầu phiếu\n"
     "- Ở bước cuối, nút hiện là \"Tạo phiếu ủy nhiệm chi\"\n"
     "- Bản in dùng mẫu chi trả nhà cung cấp chuyển khoản, có khối thông tin ngân hàng"),

    ("005", "Vòng đời phiếu Thanh toán chi phí vận chuyển", "P0",
     "NV-A; nhà cung cấp vận chuyển NCC-V có chuyến xe phát sinh chưa thanh toán hết",
     "1. Tạo phiếu, chọn Loại chi = Thanh toán chi phí vận chuyển NCC, hình thức TM\n"
     "2. Điền Đến ngày, chọn NCC-V, bấm Lấy dữ liệu\n"
     "3. Bỏ tích một số dòng, nhập số tiền cho các dòng còn lại, bấm Lưu và gửi duyệt\n"
     "4. Chạy hết dây chuyền duyệt\n"
     "5. Mở lại chi tiết, đối chiếu số dòng và số tiền",
     "—",
     "- Bảng nạp đúng các chuyến còn phải trả lớn hơn 0\n"
     "- Phiếu chỉ lưu các dòng đã tích\n"
     "- Nhập vượt Số tiền còn lại thì ô tự kéo xuống bằng số còn lại\n"
     "- Bấm vào ô Hạch toán mở được cửa sổ Chi tiết chuyến xe ở cả màn nhập và màn xem"),

    ("006", "Vòng đời phiếu ngoại tệ qua các cấp duyệt", "P0",
     "NV-A; danh mục có USD tỷ giá 25.000",
     "1. Tạo phiếu Chi trả lại khách hàng, đổi Loại tiền sang USD\n"
     "2. Thêm 2 dòng, mỗi dòng 1.000 USD, bấm Lưu và gửi duyệt\n"
     "3. Ở mỗi cấp duyệt, nhập số của cấp mình và đọc cột quy đổi VND\n"
     "4. Đọc cột Số tiền ngoài danh sách sau mỗi bước\n"
     "5. Lọc khoảng tiền từ 40.000.000 đến 60.000.000",
     "USD, tỷ giá 25.000, 2 dòng x 1.000",
     "- Mỗi nhóm cột tiền tách 2 cột con: USD và VND\n"
     "- Cột Số tiền ngoài danh sách hiện số NGUYÊN TỆ kèm chữ USD\n"
     "- Cột quy đổi VND của mỗi dòng bằng số nguyên tệ nhân 25.000\n"
     "- Bộ lọc khoảng tiền TÌM RA phiếu này (so số quy đổi 50.000.000)"),

    ("007", "Đối chiếu số liệu tổng của màn với dữ liệu gốc", "P1",
     "Tài khoản có quyền xem tổng công ty; đã có bản trích dữ liệu gốc để đối chiếu",
     "1. Mở chế độ Tất cả, không đặt bộ lọc nào, ghi lại số tổng\n"
     "2. Đếm số phiếu nháp của người khác trong dữ liệu gốc\n"
     "3. Đối chiếu: tổng trên màn = tổng dữ liệu gốc trừ số phiếu nháp của người khác\n"
     "4. Lặp lại phép đối chiếu với bộ lọc theo khoảng ngày",
     "—",
     "- Bước 3 khớp chính xác\n"
     "- ⚠️ Bước 4 phải cộng bù phần bị ô \"Đến ngày\" làm rụng (mục 9 ghi chú 8), nếu không sẽ lệch\n"
     "- ⚠️ Nếu dữ liệu gốc còn dòng chi tiết mồ côi của phiếu đã xóa (TC_06.007) thì các phép cộng "
     "theo dòng chi tiết sẽ lệch — nêu rõ khi báo cáo"),
]
