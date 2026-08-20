# -*- coding: utf-8 -*-
"""Section VIII (rang buoc nhap lieu), IX (co lap du lieu), X (luong dau - cuoi)."""

SEC_VIII = [
    ("001", "Lưu khi để trống Diễn giải", "P0",
     "Màn Tạo mới, đã chọn Loại phiếu, có 1 dòng chi tiết hợp lệ, để trống Diễn giải",
     "1. Bấm Lưu\n"
     "2. Quan sát",
     "Diễn giải: để trống",
     "- Không lưu\n"
     "- Lỗi đỏ \"Bắt buộc nhập\" ngay dưới ô Diễn giải\n"
     "- Ở lại form, dữ liệu đã nhập còn nguyên"),

    ("002", "Lưu khi bảng chi tiết không có dòng nào", "P0",
     "Màn Tạo mới, đã chọn Loại phiếu và điền Diễn giải, xóa hết dòng Điều chỉnh từ",
     "1. Bấm Lưu\n"
     "2. Quan sát",
     "0 dòng chi tiết",
     "- Không lưu\n"
     "- Hệ thống báo lỗi phần chi tiết, yêu cầu phải có ít nhất một dòng"),

    ("003", "Lưu khi dòng Điều chỉnh từ không có dòng Điều chỉnh đến", "P0",
     "Phiếu khách hàng, dòng Điều chỉnh từ đã chọn khách hàng, hợp đồng và số tiền; xóa hết dòng đến",
     "1. Bấm Lưu\n"
     "2. Quan sát",
     "—",
     "- Không lưu\n"
     "- Hệ thống báo lỗi yêu cầu phải có ít nhất một dòng Điều chỉnh đến"),

    ("004", "Lưu khi chưa chọn khách hàng ở dòng Điều chỉnh từ", "P0",
     "Phiếu khách hàng, dòng Điều chỉnh từ còn trống hoàn toàn, Diễn giải đã điền",
     "1. Bấm Lưu\n"
     "2. Quan sát dòng chi tiết",
     "—",
     "- Không lưu\n"
     "- Ô Khách hàng ở nửa Điều chỉnh từ báo lỗi bắt buộc\n"
     "- Ô Khách hàng và Hợp đồng ở nửa Điều chỉnh đến cũng báo lỗi bắt buộc"),

    ("005", "Lưu khi chưa chọn hợp đồng ở dòng Điều chỉnh đến", "P0",
     "Phiếu khách hàng, dòng đến đã chọn khách hàng nhưng chưa chọn hợp đồng, đã nhập số tiền",
     "1. Bấm Lưu\n"
     "2. Quan sát",
     "—",
     "- Không lưu\n"
     "- Chỉ ô Hợp đồng của dòng đến báo lỗi, ô Khách hàng không báo lỗi"),

    ("006", "Lưu phiếu NCC khi chưa chọn nhà cung cấp", "P0",
     "Phiếu NCC, dòng Điều chỉnh từ chưa chọn nhà cung cấp, Diễn giải và Loại tiền đã điền",
     "1. Bấm Lưu\n"
     "2. Quan sát",
     "—",
     "- Không lưu\n"
     "- Ô Nhà cung cấp báo lỗi \"Bắt buộc chọn nhà cung cấp\""),

    ("007", "Lưu phiếu NCC khi chưa chọn hợp đồng mua", "P0",
     "Phiếu NCC, dòng Điều chỉnh từ đã chọn nhà cung cấp (không phải nhà cung cấp không rõ) nhưng chưa "
     "chọn hợp đồng mua",
     "1. Bấm Lưu\n"
     "2. Quan sát\n"
     "3. Làm tương tự với dòng Điều chỉnh đến",
     "—",
     "- Không lưu\n"
     "- Ô Hợp đồng mua báo lỗi \"Bắt buộc chọn hợp đồng mua\" ở cả hai nửa"),

    ("008", "Lưu phiếu NCC khi để trống Loại tiền", "P0",
     "Phiếu NCC, đã điền các ô khác hợp lệ, xóa lựa chọn ở ô Loại tiền",
     "1. Bấm Lưu\n"
     "2. Quan sát",
     "—",
     "- Không lưu\n"
     "- Ô Loại tiền báo lỗi \"Bắt buộc chọn loại tiền\"\n"
     "- Phiếu khách hàng không bị đòi ô này vì không hiện ô Loại tiền"),

    ("009", "Lưu phiếu NCC khi để trống Tỷ giá", "P1",
     "Phiếu NCC, đã chọn Loại tiền, xóa sạch ô Tỷ giá",
     "1. Bấm Lưu\n"
     "2. Quan sát",
     "—",
     "- Không lưu\n"
     "- Ô Tỷ giá báo lỗi \"Bắt buộc nhập tỷ giá\""),

    ("010", "Số tiền điều chỉnh đến bằng 0 bị chặn", "P0",
     "Dòng Điều chỉnh đến đã chọn đủ khách hàng và hợp đồng, để Số tiền = 0",
     "1. Bấm Lưu\n"
     "2. Quan sát",
     "Số tiền đến: 0",
     "- Không lưu\n"
     "- Hiện cảnh báo \"Số tiền phải > 0\"\n"
     "- Sửa thành số dương thì lưu được"),

    ("011", "Số tiền điều chỉnh đến âm bị chặn", "P0",
     "Dòng Điều chỉnh đến đã chọn đủ thông tin",
     "1. Thử gõ dấu trừ rồi số vào ô Số tiền\n"
     "2. Bấm Lưu",
     "Số tiền: -1.000.000",
     "- Ô tiền không nhận dấu trừ, hoặc nếu nhận thì khi Lưu bị chặn với cảnh báo số tiền phải lớn hơn 0\n"
     "- Không tạo được phiếu có số tiền âm"),

    ("012", "Số tiền điều chỉnh từ bằng 0", "P1",
     "Dòng Điều chỉnh từ đã chọn đủ khách hàng và hợp đồng, để Số tiền = 0; dòng đến có số tiền 0",
     "1. Bấm Lưu\n"
     "2. Quan sát",
     "—",
     "- Số tiền điều chỉnh từ được phép bằng 0 (hệ thống chỉ yêu cầu từ 0 trở lên)\n"
     "- Nhưng dòng đến bằng 0 vẫn bị chặn theo TC_08.010, nên phiếu không lưu được\n"
     "- ⚠️ Ghi nhận: thực tế không lập được phiếu có số tiền điều chỉnh từ bằng 0 vì dòng đến phải lớn "
     "hơn 0 mà tổng đến không được vượt điều chỉnh từ"),

    ("013", "Ô Số tiền chỉ nhận số và tự thêm dấu ngăn nghìn", "P1",
     "Đang ở dòng chi tiết",
     "1. Gõ chữ cái vào ô Số tiền\n"
     "2. Gõ 12000000, rời ô\n"
     "3. Quan sát cột quy đổi (nếu là phiếu NCC ngoại tệ)",
     "Nhập chữ, rồi 12000000",
     "- Chữ cái không được nhận\n"
     "- Số hiện thành 12.000.000\n"
     "- Cột quy đổi VNĐ (nếu có) cập nhật theo tỷ giá"),

    ("014", "Số tiền có phần thập phân ở phiếu NCC ngoại tệ", "P2",
     "Phiếu NCC loại tiền USD, tỷ giá 25.000",
     "1. Nhập số tiền dòng đến = 1.234,56\n"
     "2. Rời ô, đọc lại giá trị và cột quy đổi\n"
     "3. Lưu và mở lại phiếu",
     "1.234,56 USD",
     "- Giữ đúng phần thập phân, không bị làm tròn về số nguyên\n"
     "- Cột quy đổi VNĐ tính đúng theo tỷ giá\n"
     "- Mở lại vẫn đúng số vừa nhập"),

    ("015", "Diễn giải nhận chuỗi dài có dấu tiếng Việt", "P2",
     "Màn Tạo mới hợp lệ",
     "1. Nhập Diễn giải dài khoảng 300 ký tự có dấu, có xuống dòng\n"
     "2. Lưu rồi mở lại chi tiết\n"
     "3. Mở bản in",
     "Chuỗi dài có dấu",
     "- Lưu được, không cắt chữ, không lỗi font\n"
     "- Mở lại giữ đúng các dấu xuống dòng\n"
     "- Bản in hiện đủ nội dung Diễn giải"),

    ("016", "Bỏ qua giao diện gửi lên loại phiếu không hợp lệ", "P1",
     "Tài khoản bất kỳ; dùng công cụ kiểm thử API",
     "1. Gọi thẳng chức năng Tạo phiếu, gửi Loại phiếu = 9\n"
     "2. Quan sát kết quả",
     "Loại phiếu: 9",
     "- Hệ thống CHẶN, báo \"Loại phiếu không hợp lệ\"\n"
     "- Không tạo được phiếu\n"
     "- ⚠️ Đây là điểm màn này làm ĐÚNG, chặt hơn hai màn Đề nghị thu tiền và Đề nghị thanh toán"),

    ("017", "Bỏ qua giao diện gửi lên trạng thái tùy ý khi tạo phiếu", "P0",
     "Tài khoản bất kỳ; dùng công cụ kiểm thử API",
     "1. Gọi thẳng chức năng Tạo phiếu với trạng thái là Đã duyệt phiếu kế toán\n"
     "2. Tìm phiếu vừa tạo trong danh sách, đọc Trạng thái",
     "—",
     "- ⚠️ Hiện trạng: hệ thống không giới hạn trạng thái khi tạo, phiếu được tạo ngay ở trạng thái gửi "
     "lên. LỖ HỔNG, ghi nhận Failed\n"
     "- Kỳ vọng đúng: khi tạo chỉ cho 2 trạng thái Đang tạo hoặc Chờ tạo phiếu kế toán"),

    ("018", "Bỏ qua giao diện gửi lên khách hàng không tồn tại", "P1",
     "Tài khoản bất kỳ; dùng công cụ kiểm thử API",
     "1. Gọi thẳng chức năng Tạo phiếu khách hàng, gửi dòng chi tiết với khách hàng là một số không có "
     "thật\n"
     "2. Quan sát kết quả",
     "Khách hàng: 99999999",
     "- Hệ thống chặn, báo khách hàng không tồn tại\n"
     "- Không tạo được phiếu"),

    ("019", "Bỏ qua giao diện gửi lên phiếu báo có không tồn tại", "P2",
     "Tài khoản bất kỳ; dùng công cụ kiểm thử API",
     "1. Gọi thẳng chức năng Tạo phiếu, gửi số phiếu báo có không có thật\n"
     "2. Quan sát kết quả",
     "—",
     "- Hệ thống chặn, báo không tồn tại\n"
     "- Không tạo được phiếu"),

    ("020", "Bỏ qua giao diện gửi tổng điều chỉnh đến vượt điều chỉnh từ", "P0",
     "Tài khoản bất kỳ; dùng công cụ kiểm thử API",
     "1. Gọi thẳng chức năng Tạo phiếu khách hàng, gửi điều chỉnh từ 10.000.000 và tổng điều chỉnh đến "
     "15.000.000\n"
     "2. Quan sát kết quả",
     "—",
     "- Hệ thống CHẶN, báo tổng số tiền điều chỉnh đến không được lớn hơn số tiền điều chỉnh từ, kèm "
     "hai con số cụ thể\n"
     "- Không tạo được phiếu\n"
     "- ⚠️ Ràng buộc này được kiểm cả ở giao diện lẫn ở phía hệ thống — điểm làm đúng của màn"),

    ("021", "Bỏ qua giao diện gửi phiếu NCC lệch tổng khi gửi duyệt", "P0",
     "Tài khoản bất kỳ; dùng công cụ kiểm thử API",
     "1. Gọi thẳng chức năng Tạo phiếu NCC với trạng thái Chờ tạo phiếu kế toán, điều chỉnh từ "
     "10.000.000 và tổng đến 6.000.000\n"
     "2. Gọi lại với trạng thái Đang tạo, cùng số liệu",
     "—",
     "- Lần 1: bị chặn, báo tổng số tiền điều chỉnh đến phải bằng số tiền điều chỉnh từ\n"
     "- Lần 2: tạo được (lưu nháp không kiểm ràng buộc này)\n"
     "- Khớp đúng với hành vi trên giao diện ở TC_04.023 và TC_04.024"),
]

SEC_IX = [
    ("001", "Hai người cùng lập phiếu tại một thời điểm", "P0",
     "2 tài khoản cùng công ty, cùng chuẩn bị sẵn form Tạo mới hợp lệ",
     "1. Cả 2 bấm Lưu gần như cùng lúc\n"
     "2. Đối chiếu mã của 2 phiếu vừa tạo\n"
     "3. Lặp lại 3 lần để tăng khả năng va chạm",
     "—",
     "- Cả 2 phiếu đều lưu thành công\n"
     "- ⚠️ Mã phiếu sinh không có khóa chống va chạm: nếu 2 phiếu ra TRÙNG mã thì ghi Failed kèm ảnh "
     "chụp; nếu 2 mã liên tiếp thì đạt"),

    ("002", "Hai người ở hai công ty lập phiếu có tiền tố mã khác nhau", "P1",
     "Tài khoản công ty A và tài khoản công ty B",
     "1. Mỗi người lập 1 phiếu nháp\n"
     "2. Đọc mã 2 phiếu",
     "—",
     "- Tiền tố mã công ty khác nhau, phần giữa đều là DNDCCN kèm tháng năm\n"
     "- Phần 5 số đếm riêng theo từng tiền tố"),

    ("003", "Bấm Lưu nhiều lần liên tiếp", "P0",
     "Màn Tạo mới đã điền hợp lệ",
     "1. Bấm nút Lưu liên tục 3 lần thật nhanh\n"
     "2. Quan sát nút và thông báo\n"
     "3. Mở danh sách, đếm số phiếu vừa tạo",
     "—",
     "- Nút chuyển sang trạng thái đang xử lý sau lần bấm đầu và bị vô hiệu\n"
     "- CHỈ MỘT phiếu được tạo; nếu ra 2 hoặc 3 phiếu thì ghi Failed"),

    ("004", "Hai kế toán cùng xử lý một phiếu", "P0",
     "2 tài khoản kế toán thanh toán cùng công ty, cùng mở chi tiết một phiếu ở Chờ tạo phiếu kế toán",
     "1. Kế toán 1 nhập lý do và bấm Không duyệt, xác nhận\n"
     "2. Kế toán 2 (chưa tải lại) cũng nhập lý do khác và bấm Không duyệt, xác nhận\n"
     "3. Mở lại phiếu, đọc Trạng thái và lý do",
     "—",
     "- Kế toán 2 bị hệ thống từ chối với thông báo \"Không có quyền!\" vì phiếu đã rời trạng thái chờ\n"
     "- Lý do của kế toán 1 giữ nguyên, không bị ghi đè\n"
     "- ⚠️ Đây là điểm màn này làm ĐÚNG — đối chiếu với màn Đề nghị thanh toán nơi bị ghi đè"),

    ("005", "Người lập sửa phiếu trong khi kế toán đang xử lý", "P0",
     "Mở 2 tab: tab 1 là màn Sửa phiếu nháp của NV-A; tab 2 dùng chính NV-A gửi duyệt phiếu đó",
     "1. Tab 2 gửi duyệt phiếu\n"
     "2. Tab 1 sửa Diễn giải rồi bấm Lưu\n"
     "3. Mở lại phiếu, đọc Trạng thái và Diễn giải",
     "—",
     "- ⚠️ Hiện trạng: tab 1 lưu ĐÈ được, phiếu quay lại trạng thái Đang tạo và mất trạng thái Chờ tạo "
     "phiếu kế toán. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: chặn lưu vì phiếu đã rời trạng thái cho phép sửa"),

    ("006", "Sửa phiếu đã được kế toán lập phiếu kế toán", "P0",
     "Phiếu đã ở trạng thái Đã tạo phiếu kế toán; NV-A là người lập",
     "1. Đăng nhập NV-A, dán thẳng đường dẫn màn Sửa của phiếu đó\n"
     "2. Nếu mở được, sửa số tiền rồi bấm Lưu\n"
     "3. Mở lại phiếu kế toán đã lập, đối chiếu số liệu",
     "—",
     "- ⚠️ Hiện trạng: sửa được và phiếu bị đẩy về trạng thái Đang tạo, trong khi phiếu kế toán đã lập "
     "vẫn giữ số cũ — hai bên lệch nhau. Ghi nhận Failed kèm số liệu cụ thể\n"
     "- Kỳ vọng đúng: chặn sửa khi đã có phiếu kế toán"),

    ("007", "Phạm vi dữ liệu không rò rỉ giữa các công ty", "P0",
     "Tài khoản chỉ có quyền xem theo công ty, thuộc công ty 3",
     "1. Lọc theo Số phiếu báo có bằng mã chỉ có ở công ty 1\n"
     "2. Lọc KH/NCC bằng một khách hàng chỉ có ở công ty 1\n"
     "3. Nhập khoảng tiền rất rộng từ 0 đến 999.999.999.999\n"
     "4. Bấm Xuất excel và mở tệp",
     "—",
     "- Cả 4 cách đều không làm lộ phiếu của công ty 1\n"
     "- Tổng luôn nằm trong phạm vi công ty 3"),

    ("008", "Màn Chờ duyệt không lộ phiếu ngoài công ty", "P0",
     "KT-1 thuộc công ty 3; công ty 1 cũng có phiếu ở Chờ tạo phiếu kế toán",
     "1. Mở màn Chờ duyệt\n"
     "2. Dùng ô lọc Công ty chọn công ty 1, bấm tìm kiếm",
     "—",
     "- Kết quả rỗng, không lộ phiếu của công ty khác\n"
     "- ⚠️ Nếu ra phiếu của công ty 1 thì ghi Failed"),

    ("009", "Số dư hợp đồng được tính lại mỗi lần mở phiếu", "P1",
     "Phiếu lập từ tháng trước, cột Số dư lúc lập là 25.000.000; sau đó hợp đồng đã phát sinh thêm giao "
     "dịch",
     "1. Mở màn chi tiết phiếu đó\n"
     "2. Đọc cột Số dư và so với con số ghi nhận lúc lập phiếu\n"
     "3. Đọc cột Số tiền ngoài danh sách",
     "—",
     "- Cột Số dư hiện số MỚI theo sổ kế toán hiện tại, khác 25.000.000\n"
     "- Cột Số tiền của phiếu KHÔNG đổi (số tiền điều chỉnh đã lưu trong phiếu)\n"
     "- ⚠️ Đúng thiết kế, không ghi Failed"),

    ("010", "Xóa phiếu xong danh sách nạp lại đúng số tổng", "P1",
     "Đang lọc Trạng thái = Đang tạo, có 5 phiếu",
     "1. Xóa 1 phiếu\n"
     "2. Đọc lại số tổng và các ô lọc",
     "—",
     "- Tổng còn 4\n"
     "- Ghi nhận thực tế bộ lọc Trạng thái có được giữ lại hay không"),

    ("011", "Mở phiếu của nhân sự không còn phòng ban", "P2",
     "Phiếu do một nhân viên đã bị gỡ khỏi phòng ban lập",
     "1. Mở màn danh sách chứa phiếu đó\n"
     "2. Mở màn chi tiết và màn Sửa",
     "—",
     "- Ghi nhận đúng hiện trạng: cột Phòng ban để trống hay hệ thống báo lỗi trang\n"
     "- ⚠️ Nếu cả dòng hoặc cả bảng không tải được thì ghi Failed"),
]

SEC_X = [
    ("001", "Vòng đời đầy đủ phiếu điều chỉnh công nợ khách hàng", "P0",
     "NV-A thuộc công ty 3, là người lập của hợp đồng HD-A (khách hàng KH-001) và hợp đồng HD-B (khách "
     "hàng KH-002); KT-1 là kế toán thanh toán công ty 3",
     "1. NV-A tạo phiếu, Loại phiếu = Điều chỉnh công nợ khách hàng, Diễn giải \"Chuyển công nợ tháng "
     "8\"\n"
     "2. Dòng Điều chỉnh từ: KH-001 + HD-A, số tiền 10.000.000\n"
     "3. Thêm 2 dòng Điều chỉnh đến: KH-002 + HD-B số tiền 6.000.000, và KH-002 + HD-C số tiền "
     "4.000.000\n"
     "4. Bấm Lưu, kiểm phiếu trong danh sách\n"
     "5. Mở lại, bấm Sửa rồi Lưu và gửi duyệt\n"
     "6. KT-1 mở màn Chờ duyệt, mở phiếu, bấm Tạo phiếu kế toán",
     "Từ 10.000.000 → đến 6.000.000 + 4.000.000",
     "- Bước 4: trạng thái Đang tạo, cột Ngày nhận trống, chỉ NV-A thấy ở chế độ Tất cả\n"
     "- Bước 5: trạng thái Chờ tạo phiếu kế toán, cột Ngày nhận hiện ngày hôm nay, nút Sửa và Xóa biến "
     "mất, KT-1 nhận thông báo\n"
     "- Bước 6: chuyển sang màn tạo Phiếu kế toán với dữ liệu nạp sẵn đúng 1 dòng từ và 2 dòng đến\n"
     "- Cột Số tiền ngoài danh sách hiện 10.000.000 ở mọi bước"),

    ("002", "Vòng đời đầy đủ phiếu điều chỉnh công nợ NCC", "P0",
     "NV-A; nhà cung cấp NCC-01 và NCC-02 đều có hợp đồng mua",
     "1. Tạo phiếu, Loại phiếu = Điều chỉnh công nợ NCC, Loại tiền = VND\n"
     "2. Dòng Điều chỉnh từ: NCC-01 + hợp đồng mua HDM-A, số tiền 10.000.000\n"
     "3. Dòng Điều chỉnh đến: NCC-02 + hợp đồng mua HDM-B, số tiền 6.000.000\n"
     "4. Bấm Lưu (thành công), rồi bấm Lưu và gửi duyệt (bị chặn)\n"
     "5. Sửa số tiền dòng đến thành 10.000.000, bấm Lưu và gửi duyệt\n"
     "6. KT-1 mở phiếu, nhập lý do và bấm Không duyệt\n"
     "7. NV-A sửa lại và gửi duyệt lần nữa",
     "—",
     "- Bước 4: lưu nháp được với số lệch; gửi duyệt bị chặn với cảnh báo tổng đến phải bằng tổng từ\n"
     "- Bước 5: gửi duyệt thành công\n"
     "- Bước 6: trạng thái Từ chối, lý do lưu lại; NV-A KHÔNG nhận thông báo\n"
     "- Bước 7: phiếu quay lại Chờ tạo phiếu kế toán và xuất hiện lại ở màn Chờ duyệt"),

    ("003", "Vòng đời phiếu NCC dùng ngoại tệ", "P0",
     "NV-A; danh mục có USD tỷ giá 25.000",
     "1. Tạo phiếu NCC, chọn Loại tiền = USD, kiểm ô Tỷ giá tự điền\n"
     "2. Nhập dòng Điều chỉnh từ 1.000 USD và dòng đến 1.000 USD\n"
     "3. Đọc cột quy đổi VNĐ của cả hai nửa\n"
     "4. Bấm Lưu và gửi duyệt\n"
     "5. Xem danh sách, xem chi tiết, mở bản in và xuất Excel",
     "USD, tỷ giá 25.000",
     "- Ô Tỷ giá tự điền 25.000 khi chọn USD\n"
     "- Cột Số dư và cột Số tiền của cả hai nửa đều tách đôi ngoại tệ / VNĐ\n"
     "- Cột quy đổi hiện 25.000.000\n"
     "- Gửi duyệt thành công vì tổng đến bằng tổng từ"),

    ("004", "Vòng đời phiếu tạo từ Phiếu báo có", "P0",
     "Màn Phiếu báo có có dòng chưa xử lý; KT-1 là kế toán thanh toán",
     "1. Từ màn Phiếu báo có, chọn dòng rồi đẩy sang tạo phiếu điều chỉnh công nợ\n"
     "2. Kiểm Loại phiếu và ô Phiếu báo có, kiểm nút thêm dòng Điều chỉnh từ\n"
     "3. Thêm dòng Điều chỉnh đến với số tiền NHỎ HƠN số điều chỉnh từ\n"
     "4. Bấm Lưu và gửi duyệt\n"
     "5. Xem danh sách, bấm vào cột Số phiếu báo có\n"
     "6. KT-1 xử lý phiếu",
     "—",
     "- Loại phiếu tự đặt là Điều chỉnh công nợ khách hàng, ô Phiếu báo có chỉ đọc\n"
     "- Nút thêm dòng Điều chỉnh từ bị ẩn\n"
     "- Gửi duyệt thành công (phiếu khách hàng cho phép nhỏ hơn)\n"
     "- Cột Số phiếu báo có là liên kết, bấm vào mở tab mới sang màn Phiếu báo có"),

    ("005", "Phiếu gom nhiều dòng Điều chỉnh từ trong cùng một phiếu", "P0",
     "NV-A là người lập của ít nhất 3 hợp đồng thuộc 2 khách hàng khác nhau",
     "1. Tạo phiếu khách hàng, thêm 2 dòng Điều chỉnh từ với 2 khách hàng khác nhau\n"
     "2. Mỗi dòng thêm 2 dòng Điều chỉnh đến, số tiền hợp lệ theo từng dòng\n"
     "3. Bấm Lưu\n"
     "4. Xem danh sách, xem chi tiết, mở bản in\n"
     "5. Lọc theo Hợp đồng điều chỉnh đến bằng hợp đồng của dòng đến cuối cùng",
     "2 dòng từ, 4 dòng đến",
     "- Lưu được; mỗi dòng Điều chỉnh từ kiểm tổng riêng của mình, không cộng chung cả phiếu\n"
     "- Cột KH/NCC ngoài danh sách chỉ hiện khách hàng của dòng ĐẾN đầu tiên\n"
     "- Chi tiết và bản in hiện đủ cấu trúc 2 dòng từ và 4 dòng đến\n"
     "- Lọc theo hợp đồng điều chỉnh đến VẪN tìm ra phiếu này"),

    ("006", "Đối chiếu số liệu tổng của màn với dữ liệu gốc", "P1",
     "Tài khoản có quyền xem tổng công ty; đã có bản trích dữ liệu gốc để đối chiếu",
     "1. Mở chế độ Tất cả, không đặt bộ lọc nào, ghi lại số tổng\n"
     "2. Đếm số phiếu nháp của người khác trong dữ liệu gốc\n"
     "3. Đối chiếu: tổng trên màn = tổng dữ liệu gốc trừ số phiếu nháp của người khác\n"
     "4. Bấm Xuất excel, đếm số dòng trong tệp\n"
     "5. Lặp lại phép đối chiếu với bộ lọc theo khoảng ngày",
     "—",
     "- Bước 3 khớp chính xác\n"
     "- Bước 4: số dòng trong tệp bằng số tổng trên màn\n"
     "- ⚠️ Bước 5 phải cộng bù phần bị ô \"Đến ngày\" làm rụng (mục 9 ghi chú 11)\n"
     "- ⚠️ Nếu dữ liệu gốc còn dòng chi tiết mồ côi của phiếu đã xóa (TC_06.007) thì bộ lọc theo hợp "
     "đồng sẽ ra kết quả lệch — nêu rõ khi báo cáo"),
]
