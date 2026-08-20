# -*- coding: utf-8 -*-
"""Section IV — tao moi / sua / xem chi tiet."""

SEC_IV = [
    ("001", "Bố cục màn Tạo mới", "P0",
     "Tài khoản bất kỳ, đang ở màn danh sách",
     "1. Bấm nút Tạo mới\n"
     "2. Quan sát khối Thông tin chung khi chưa chọn gì",
     "—",
     "- Tiêu đề trang \"Tạo phiếu đề nghị thanh toán\"\n"
     "- Khối Thông tin chung có: Loại chi, Hình thức thanh toán, Loại tiền, Tỷ giá, Người tạo, Phòng "
     "ban, Lý do chi — trong đó Loại chi, Hình thức thanh toán, Loại tiền, Tỷ giá, Lý do chi gắn dấu "
     "bắt buộc\n"
     "- Người tạo và Phòng ban điền sẵn theo người đang đăng nhập và bị khóa\n"
     "- Có khối File đính kèm và khối Chi tiết\n"
     "- Dưới cùng có 3 nút: Lưu, Lưu và gửi duyệt, Quay lại"),

    ("002", "Chưa chọn đủ Loại chi và Hình thức thanh toán thì chưa hiện bảng chi tiết", "P0",
     "Vừa mở màn Tạo mới",
     "1. Quan sát khối Chi tiết khi cả 2 ô còn trống\n"
     "2. Chỉ chọn Loại chi, quan sát\n"
     "3. Chọn thêm Hình thức thanh toán",
     "—",
     "- Chỉ khi CẢ HAI ô đã chọn thì bảng chi tiết mới hiện ra\n"
     "- Chọn thiếu một trong hai thì khối Chi tiết vẫn trống"),

    ("003", "Ô Loại chi chỉ có 4 lựa chọn khi lập mới", "P0",
     "Đang ở màn Tạo mới",
     "1. Mở ô Loại chi, đếm và ghi lại các lựa chọn",
     "—",
     "- Đúng 4 lựa chọn: Chi trả nhà cung cấp · Chi trả lại khách hàng · Chi thưởng thực hiện hợp đồng "
     "· Thanh toán chi phí vận chuyển NCC\n"
     "- KHÔNG có Chi thưởng NVKD, Chi thu nhập cho nhân viên, Chi khác\n"
     "- ⚠️ Đúng hiện trạng, đối chiếu mục 3 trước khi báo thiếu"),

    ("004", "Giá trị mặc định của Loại tiền và Tỷ giá", "P0",
     "Vừa mở màn Tạo mới",
     "1. Đọc ô Loại tiền và ô Tỷ giá\n"
     "2. Thử gõ vào ô Tỷ giá",
     "—",
     "- Loại tiền mặc định VND\n"
     "- Ô Tỷ giá bị KHÓA, bên phải có nhãn VND\n"
     "- Giá trị lấy theo tỷ giá của VND trong danh mục tiền tệ"),

    ("005", "Đổi Loại chi xóa sạch dòng chi tiết và thông tin ngân hàng", "P0",
     "Đang ở màn Tạo mới, Loại chi = Chi trả nhà cung cấp, Hình thức CK, đã chọn nhà cung cấp, đã điền "
     "số tài khoản và tên ngân hàng, đã có 2 dòng chi tiết",
     "1. Đổi Loại chi sang Chi trả lại khách hàng\n"
     "2. Quan sát ngay lập tức",
     "—",
     "- ⚠️ KHÔNG có hộp thoại xác nhận\n"
     "- Bảng chi tiết bị xóa sạch, còn lại 1 dòng trống\n"
     "- Mọi ô thông tin đối tượng và thông tin ngân hàng bị xóa trắng\n"
     "- Ghi nhận đúng hiện trạng"),

    ("006", "Đổi Hình thức thanh toán đổi bố cục form", "P0",
     "Loại chi = Chi trả nhà cung cấp, đang ở Hình thức TM, đã có 1 dòng chi tiết chọn nhà cung cấp",
     "1. Quan sát vị trí ô chọn Nhà cung cấp\n"
     "2. Đổi Hình thức thanh toán sang CK\n"
     "3. Quan sát lại",
     "TM → CK",
     "- TM: ô chọn Nhà cung cấp nằm TRONG BẢNG chi tiết, chọn theo từng dòng\n"
     "- CK: ô chọn Nhà cung cấp chuyển lên ĐẦU PHIẾU, chọn một lần cho cả phiếu; bảng chi tiết không "
     "còn cột Nhà cung cấp\n"
     "- Đổi hình thức cũng xóa sạch dòng chi tiết đã nhập"),

    ("007", "Bố cục bảng chi tiết theo từng Loại chi", "P0",
     "Lần lượt dựng 4 phiếu mới, mỗi phiếu một loại chi, hình thức TM",
     "1. Với mỗi loại chi, ghi lại tiêu đề các cột của bảng chi tiết",
     "4 loại chi",
     "- Chi trả nhà cung cấp: STT, Nhà cung cấp, Số hợp đồng nhập mua, Số tiền còn nợ, Số tiền đề nghị "
     "chi, Ghi chú, nút thao tác\n"
     "- Chi trả lại khách hàng: STT, Khách hàng, Số đơn hàng/Hợp đồng, Công nợ còn lại, Số tiền đề nghị "
     "chi, Ghi chú, nút thao tác\n"
     "- Chi thưởng thực hiện hợp đồng: STT, Số đơn hàng/Hợp đồng, Số tiền còn lại, Số tiền đề nghị chi, "
     "Ghi chú, nút thao tác\n"
     "- Thanh toán chi phí vận chuyển NCC: STT, ô tích chọn, Số chuyến xe, Hạch toán, Tổng cước, Đã "
     "thanh toán, Số tiền còn lại, Số tiền đề nghị chi (không có cột Ghi chú)"),

    ("008", "Thêm và xóa dòng chi tiết", "P0",
     "Loại chi = Chi trả lại khách hàng, Hình thức TM, đang có 1 dòng trống",
     "1. Bấm dấu cộng ở góc phải tiêu đề bảng 2 lần\n"
     "2. Đếm số dòng\n"
     "3. Bấm biểu tượng thùng rác ở dòng 2",
     "—",
     "- Sau bước 1 có 3 dòng, STT đánh 1, 2, 3\n"
     "- Xóa dòng 2 thì còn 2 dòng, STT đánh lại, dữ liệu 2 dòng còn lại không xáo trộn\n"
     "- Xóa dòng KHÔNG hỏi xác nhận"),

    ("009", "Chọn khách hàng cho từng dòng ở hình thức TM", "P0",
     "Loại chi = Chi trả lại khách hàng, Hình thức TM, có 2 dòng trống",
     "1. Bấm kính lúp ở ô Khách hàng dòng 1\n"
     "2. Quan sát cửa sổ: tiêu đề, các cột, các ô tìm\n"
     "3. Chọn KH-001; làm tương tự dòng 2 với KH-002",
     "Dòng 1: KH-001 · Dòng 2: KH-002",
     "- Cửa sổ tên \"Khách hàng\", 4 cột: STT, Mã khách hàng, Tên khách hàng, Loại khách hàng\n"
     "- Có 2 ô tìm: Mã khách hàng và Tên khách hàng\n"
     "- Chọn xong hiện thông báo xanh \"Thêm khách hàng thành công!\"\n"
     "- 2 dòng giữ 2 khách hàng KHÁC NHAU"),

    ("010", "Chọn khách hàng một lần cho cả phiếu ở hình thức CK", "P0",
     "Loại chi = Chi trả lại khách hàng, Hình thức CK",
     "1. Bấm kính lúp ở ô Khách hàng trên đầu phiếu\n"
     "2. Chọn KH-001\n"
     "3. Quan sát khối thông tin tài khoản ngân hàng bên dưới",
     "Khách hàng: KH-001",
     "- Ô Khách hàng ở đầu phiếu hiện mã và tên\n"
     "- Khối thông tin ngân hàng hiện ra với các ô: Số tài khoản, Tên tài khoản, Ngân hàng, Chi nhánh, "
     "Tỉnh/Thành phố — đều gắn dấu bắt buộc\n"
     "- Nếu khách hàng có sẵn tài khoản trong hồ sơ thì các ô được điền sẵn"),

    ("011", "Chọn nhà cung cấp và bố cục ngân hàng theo loại nhà cung cấp", "P0",
     "Loại chi = Chi trả nhà cung cấp, Hình thức CK; có 1 nhà cung cấp trong nước và 1 nhà cung cấp "
     "nước ngoài",
     "1. Chọn nhà cung cấp TRONG NƯỚC, quan sát khối ngân hàng\n"
     "2. Đổi sang nhà cung cấp NƯỚC NGOÀI, quan sát lại",
     "2 nhà cung cấp",
     "- Trong nước: khối ngân hàng có Số tài khoản, Tên tài khoản, Ngân hàng, Chi nhánh, Tỉnh/Thành phố\n"
     "- Nước ngoài: khối ngân hàng đổi sang dạng chuyển tiền quốc tế, có thêm ô Ngân hàng, Mã định "
     "danh ngân hàng, Ngân hàng trung gian và ô Phí\n"
     "- Ô Phí có 3 lựa chọn: Phí do người chuyển tiền chịu · Phí do người hưởng chịu · Phí chia sẻ cho "
     "2 bên"),

    ("012", "Chưa chọn đối tượng mà bấm chọn hợp đồng", "P0",
     "Loại chi = Chi trả lại khách hàng, có 1 dòng trống chưa chọn khách hàng",
     "1. Bấm kính lúp ở ô Số đơn hàng/Hợp đồng của dòng đó\n"
     "2. Quan sát\n"
     "3. Đổi Loại chi sang Chi trả nhà cung cấp và lặp lại",
     "—",
     "- Chi trả lại khách hàng: hiện cảnh báo vàng \"Chưa chọn khách hàng\", cửa sổ KHÔNG mở\n"
     "- Chi trả nhà cung cấp: hiện cảnh báo \"Chưa chọn nhà cung cấp\", cửa sổ KHÔNG mở"),

    ("013", "Cửa sổ chọn hợp đồng chỉ hiện hợp đồng do chính mình lập", "P0",
     "Khách hàng KH-001 có 3 hợp đồng do NV-A lập và 4 hợp đồng do NV-B lập, tất cả đều khác trạng thái "
     "Đang tạo",
     "1. Đăng nhập NV-A, tạo phiếu Chi trả lại khách hàng, chọn KH-001\n"
     "2. Mở cửa sổ chọn hợp đồng, ghi lại các mã\n"
     "3. Đăng nhập NV-B, làm lại từ bước 1",
     "KH-001: 3 hợp đồng của NV-A + 4 của NV-B",
     "- NV-A chỉ thấy đúng 3 hợp đồng của mình\n"
     "- NV-B chỉ thấy đúng 4 hợp đồng của mình\n"
     "- ⚠️ Quy tắc CÓ CHỦ ĐÍCH (mục 9 ghi chú 4), không phải mất dữ liệu"),

    ("014", "Cửa sổ chọn hợp đồng loại bỏ hợp đồng đang tạo", "P0",
     "Người đăng nhập là người lập của: 2 hợp đồng KH-002 đã qua bước tạo, 1 hợp đồng KH-002 còn ở "
     "trạng thái Đang tạo",
     "1. Chọn KH-002 cho dòng 1\n"
     "2. Mở cửa sổ chọn hợp đồng, đối chiếu với 3 hợp đồng đã biết",
     "—",
     "- Chỉ hiện 2 hợp đồng đã qua bước tạo\n"
     "- Hợp đồng Đang tạo KHÔNG hiện"),

    ("015", "Cửa sổ chọn hợp đồng nhập mua của loại Chi trả nhà cung cấp", "P0",
     "Loại chi = Chi trả nhà cung cấp; nhà cung cấp NCC-01 có hợp đồng mua đã duyệt do NGƯỜI KHÁC lập",
     "1. Chọn NCC-01, bấm kính lúp ở ô Số hợp đồng nhập mua\n"
     "2. Quan sát tiêu đề, cột và số dòng",
     "Nhà cung cấp: NCC-01",
     "- Cửa sổ tên \"Đơn hàng/Hợp đồng\", 3 cột: STT, Số đơn hàng/Hợp đồng, Ngày lập\n"
     "- ⚠️ Hợp đồng mua do NGƯỜI KHÁC lập VẪN hiện — khác cửa sổ hợp đồng bán ở TC_04.013\n"
     "- Chỉ hợp đồng mua đã duyệt mới hiện"),

    ("016", "Chọn hợp đồng tự điền mã và số tiền còn nợ", "P0",
     "Cửa sổ chọn hợp đồng đang mở; hợp đồng HD-2026-001 còn nợ 25.000.000",
     "1. Bấm chọn dòng HD-2026-001\n"
     "2. Quan sát dòng chi tiết trên form",
     "—",
     "- Hiện thông báo xanh \"Thêm thành công\", cửa sổ đóng lại\n"
     "- Ô hợp đồng hiện HD-2026-001\n"
     "- Cột Số tiền còn nợ hiện 25.000.000"),

    ("017", "Không chọn trùng một hợp đồng ở hai dòng", "P0",
     "Dòng 1 đã chọn HD-2026-001; dòng 2 đã chọn cùng khách hàng",
     "1. Mở cửa sổ chọn hợp đồng ở dòng 2\n"
     "2. Bấm chọn lại HD-2026-001",
     "—",
     "- Hiện cảnh báo vàng \"Hợp đồng đã tồn tại!\"\n"
     "- Dòng 2 không được gán hợp đồng"),

    ("018", "Loại Chi thưởng thực hiện hợp đồng lấy hợp đồng theo hạch toán của người lập", "P1",
     "Người đăng nhập có phát sinh hạch toán công việc thưởng thực hiện hợp đồng trên ít nhất 1 hợp "
     "đồng, hoặc là trưởng phòng của phòng hỗ trợ hạch toán",
     "1. Tạo phiếu Chi thưởng thực hiện hợp đồng\n"
     "2. Bấm kính lúp ở ô Số đơn hàng/Hợp đồng của dòng 1 (không cần chọn khách hàng trước)\n"
     "3. Quan sát cửa sổ",
     "—",
     "- Cửa sổ mở được NGAY dù chưa chọn khách hàng ở đầu phiếu\n"
     "- Cửa sổ có 4 cột: STT, Số đơn hàng/Hợp đồng, Khách hàng, Ngày lập; có thêm ô tìm theo Khách hàng\n"
     "- Chỉ hiện hợp đồng người đăng nhập có liên quan theo hạch toán"),

    ("019", "Loại Thanh toán chi phí vận chuyển lấy dữ liệu bằng nút riêng", "P0",
     "Loại chi = Thanh toán chi phí vận chuyển NCC, Hình thức TM; nhà cung cấp vận chuyển NCC-V có "
     "chuyến xe phát sinh chưa thanh toán hết trước ngày 31/08/2026",
     "1. Bấm nút \"Lấy dữ liệu\" khi CHƯA điền Đến ngày\n"
     "2. Điền Đến ngày = 31/08/2026, bấm lại khi CHƯA chọn nhà cung cấp\n"
     "3. Chọn nhà cung cấp NCC-V, bấm \"Lấy dữ liệu\"\n"
     "4. Quan sát bảng chi tiết",
     "Đến ngày 31/08/2026 · NCC-V",
     "- Bước 1: cảnh báo \"Chưa chọn đến ngày!\"\n"
     "- Bước 2: cảnh báo \"Chưa chọn nhà cung cấp!\"\n"
     "- Bước 3: bảng nạp các dòng chuyến xe, mỗi dòng có Số chuyến xe, Hạch toán, Tổng cước, Đã thanh "
     "toán, Số tiền còn lại\n"
     "- Chỉ nạp chuyến còn phải trả lớn hơn 0; nếu không có thì cảnh báo \"Không có dữ liệu!\""),

    ("020", "Chọn dòng cần thanh toán ở loại vận chuyển", "P0",
     "Bảng chi tiết đã nạp 5 dòng chuyến xe",
     "1. Quan sát ô tích ở đầu mỗi dòng và ô tích chọn tất cả ở tiêu đề\n"
     "2. Bỏ tích 2 dòng\n"
     "3. Bấm Lưu, mở lại phiếu vừa lưu",
     "5 dòng, bỏ tích 2",
     "- Ô tích chọn tất cả bật tắt được toàn bộ dòng\n"
     "- Sau khi lưu, phiếu chỉ còn 3 dòng đã tích\n"
     "- 2 dòng bỏ tích KHÔNG được lưu vào phiếu"),

    ("021", "Bấm vào ô Hạch toán mở cửa sổ chi tiết chuyến xe", "P1",
     "Bảng chi tiết loại vận chuyển đã có dòng",
     "1. Bấm vào ô Hạch toán của một dòng\n"
     "2. Quan sát cửa sổ mở ra",
     "—",
     "- Cửa sổ \"Chi tiết chuyến xe\" hiện các cột: Số chuyến xe, Phiếu hạch toán, Xe tính cước, Số km, "
     "Km phụ trội, Cước tính toán (Chính / Phụ trội), Cước thực tế, Thuế, Cước sau thuế, Tuyến đường, "
     "Xe, Nhân viên kinh doanh\n"
     "- Bấm Đóng thì về lại form, dữ liệu không đổi"),

    ("022", "Đính kèm tệp", "P0",
     "Đang ở màn Tạo mới, Loại chi = Chi trả nhà cung cấp",
     "1. Bấm biểu tượng dấu cộng ở khối File đính kèm\n"
     "2. Chọn 1 tệp pdf hợp lệ\n"
     "3. Thêm 1 ô nữa và chọn 1 tệp ảnh\n"
     "4. Quan sát tên tệp hiển thị",
     "1 tệp pdf + 1 tệp ảnh",
     "- Mỗi lần bấm dấu cộng thêm một ô chọn tệp\n"
     "- Sau khi chọn, ô hiện đúng tên tệp và biểu tượng đổi màu\n"
     "- Nhãn khối ghi rõ dấu bắt buộc khi Loại chi là Chi trả nhà cung cấp"),

    ("023", "Cột quy đổi VND chỉ hiện với loại tiền khác VND", "P0",
     "Loại chi bất kỳ, đã có 1 dòng chi tiết",
     "1. Để Loại tiền = VND, đếm số cột con của nhóm Số tiền đề nghị chi\n"
     "2. Đổi Loại tiền sang USD, đếm lại",
     "VND → USD",
     "- VND: nhóm chỉ có 1 cột\n"
     "- USD: tách 2 cột con, cột trái mang tên loại tiền, cột phải là VND\n"
     "- Cột VND chỉ hiển thị, không gõ được"),

    ("024", "Đổi Loại tiền tự lấy tỷ giá của loại tiền đó", "P0",
     "Danh mục tiền tệ: USD tỷ giá 25.000",
     "1. Đổi Loại tiền từ VND sang USD\n"
     "2. Đọc ô Tỷ giá\n"
     "3. Sửa tay tỷ giá thành 26.000\n"
     "4. Đổi về VND rồi lại sang USD",
     "—",
     "- Đổi sang USD: ô Tỷ giá MỞ KHÓA và tự điền 25.000\n"
     "- Sửa tay được, hệ thống không chặn\n"
     "- Đổi qua lại thì tỷ giá tự nạp lại theo danh mục, số sửa tay bị mất"),

    ("025", "Số tiền đề nghị chi bị kéo xuống bằng số còn nợ ở loại Chi trả lại khách hàng", "P0",
     "Loại chi = Chi trả lại khách hàng; dòng 1 gắn hợp đồng có Công nợ còn lại 10.000.000",
     "1. Nhập Số tiền đề nghị chi = 15.000.000\n"
     "2. Rời khỏi ô, đọc lại giá trị\n"
     "3. Nhập 8.000.000, đọc lại",
     "15.000.000 rồi 8.000.000",
     "- ⚠️ Nhập 15.000.000 thì ô tự đổi về 10.000.000 (bằng công nợ còn lại), KHÔNG có thông báo nào\n"
     "- Nhập 8.000.000 thì giữ nguyên 8.000.000\n"
     "- Đây là hành vi CÓ CHỦ ĐÍCH, ghi nhận đúng"),

    ("026", "Số tiền đề nghị chi KHÔNG bị kéo xuống ở loại Chi trả nhà cung cấp", "P0",
     "Loại chi = Chi trả nhà cung cấp; dòng 1 gắn hợp đồng có Số tiền còn nợ 10.000.000",
     "1. Nhập Số tiền đề nghị chi = 15.000.000\n"
     "2. Rời khỏi ô, đọc lại giá trị\n"
     "3. Lặp lại với loại Chi thưởng thực hiện hợp đồng",
     "15.000.000 trên nền còn nợ 10.000.000",
     "- Giữ nguyên 15.000.000, hệ thống KHÔNG kéo xuống và KHÔNG cảnh báo\n"
     "- Loại Chi thưởng thực hiện hợp đồng cũng vậy\n"
     "- ⚠️ Bốn loại chi hành xử khác nhau ở điểm này — đối chiếu mục 9 ghi chú 2"),

    ("027", "Dòng Tổng cộng cộng đúng các cột tiền", "P0",
     "Loại chi = Chi trả nhà cung cấp, VND, 3 dòng: còn nợ 25.000.000 / 10.000.000 / 5.000.000; đề "
     "nghị chi 10.000.000 / 5.000.000 / 2.000.000",
     "1. Nhập đủ 3 dòng\n"
     "2. Đọc dòng Tổng cộng cuối bảng",
     "3 dòng",
     "- Tổng cột còn nợ = 40.000.000\n"
     "- Tổng cột Số tiền đề nghị chi = 17.000.000\n"
     "- Số cập nhật ngay khi gõ, không phải bấm nút nào"),

    ("028", "Lưu nháp phiếu hợp lệ", "P0",
     "Màn Tạo mới, Loại chi = Chi trả lại khách hàng, Hình thức TM, VND, Lý do chi \"Hoàn tiền hợp "
     "đồng tháng 8\", 2 dòng đủ khách hàng, hợp đồng và số tiền 10.000.000 + 5.000.000",
     "1. Bấm nút Lưu\n"
     "2. Đọc thông báo\n"
     "3. Quan sát trang sau khi lưu, tìm phiếu vừa tạo",
     "Tổng 15.000.000",
     "- Thông báo xanh \"Thêm phiếu đề nghị thanh toán tiền thành công!\"\n"
     "- Chuyển về màn danh sách chế độ Tất cả\n"
     "- Phiếu mới ở đầu danh sách, trạng thái Đang tạo, cột Số tiền hiện 15.000.000,00 VND\n"
     "- Mã phiếu sinh tự động dạng mã công ty + DNTT + tháng năm + 5 số"),

    ("029", "Lưu và gửi duyệt gửi phiếu tới trưởng phòng", "P0",
     "Màn Tạo mới đã điền hợp lệ như TC_04.028; NV-A thuộc phòng P1; TP-1 quản lý phòng P1 và có quyền "
     "Trưởng phòng duyệt đề nghị thanh toán",
     "1. Bấm nút Lưu và gửi duyệt\n"
     "2. Đọc thông báo\n"
     "3. Tìm phiếu vừa tạo, đọc Trạng thái\n"
     "4. Đăng nhập TP-1, mở chuông thông báo và màn Chờ duyệt",
     "—",
     "- ⚠️ KHÔNG có hộp thoại xác nhận trước khi lưu\n"
     "- Thông báo \"Phiếu đề nghị thanh toán đã được gửi đến trưởng phòng!\"\n"
     "- Phiếu ở trạng thái Chờ TP duyệt, không còn nút Sửa và Xóa\n"
     "- TP-1 nhận thông báo \"Bạn có một phiếu đề nghị thanh toán cần duyệt từ <tên NV-A>\" và thấy "
     "phiếu trong màn Chờ duyệt"),

    ("030", "Thông báo chỉ gửi cho trưởng phòng đúng phòng và đúng công ty", "P1",
     "TP-1 quản lý phòng P1 cùng công ty với NV-A; TP-2 quản lý phòng P2 cùng công ty; TP-9 quản lý "
     "phòng cùng tên ở công ty khác",
     "1. NV-A (phòng P1) gửi duyệt 1 phiếu\n"
     "2. Kiểm chuông thông báo của TP-1, TP-2 và TP-9",
     "—",
     "- TP-1 nhận được thông báo\n"
     "- TP-2 KHÔNG nhận (khác phòng)\n"
     "- TP-9 KHÔNG nhận (khác công ty)"),

    ("031", "Bố cục màn Sửa", "P0",
     "Phiếu P trạng thái Đang tạo do chính người đăng nhập lập, 2 dòng chi tiết, có 1 tệp đính kèm",
     "1. Mở menu hành động dòng phiếu P, bấm Sửa\n"
     "2. Quan sát khối Thông tin chung và khối File đính kèm",
     "—",
     "- Tiêu đề trang \"Sửa đề nghị phiếu thanh toán - <mã phiếu>\"\n"
     "- Có thêm ô Mã phiếu chỉ đọc\n"
     "- Dữ liệu cũ nạp đủ, bảng chi tiết hiện đúng số dòng và số tiền đã lưu\n"
     "- Khối File đính kèm liệt kê tệp đã lưu, mỗi tệp có nút xóa riêng"),

    ("032", "Xóa tệp đính kèm ở màn Sửa", "P1",
     "Phiếu P đang mở màn Sửa, có 2 tệp đính kèm",
     "1. Bấm nút xóa ở tệp thứ nhất\n"
     "2. Đọc hộp thoại, bấm Hủy\n"
     "3. Bấm lại và Xác nhận\n"
     "4. Tải lại màn Sửa",
     "—",
     "- Hộp thoại hỏi \"Bạn chắc chắn muốn xóa file này?\"\n"
     "- Bấm Hủy: tệp còn nguyên\n"
     "- Bấm Xác nhận: hiện thông báo xóa thành công, danh sách còn 1 tệp\n"
     "- Tải lại vẫn còn 1 tệp"),

    ("033", "Sửa phiếu và lưu lại", "P0",
     "Phiếu P trạng thái Đang tạo, 2 dòng, tổng 15.000.000",
     "1. Đổi Lý do chi\n"
     "2. Sửa số tiền dòng 1 từ 10.000.000 thành 12.000.000\n"
     "3. Xóa dòng 2, thêm dòng mới với hợp đồng khác, số tiền 3.000.000\n"
     "4. Bấm Lưu, mở lại chi tiết phiếu P",
     "Tổng mới 15.000.000",
     "- Thông báo \"Cập nhật phiếu đề nghị thanh toán thành công!\"\n"
     "- Chuyển về màn danh sách chế độ Tất cả\n"
     "- Mở lại thấy Lý do chi mới và 2 dòng đúng như vừa sửa\n"
     "- Mã phiếu và Người tạo KHÔNG đổi"),

    ("034", "Sửa phiếu ở trạng thái Không duyệt rồi gửi duyệt lại", "P0",
     "Phiếu Q do chính người đăng nhập lập, trạng thái Không duyệt, có Ghi chú không duyệt",
     "1. Mở chi tiết phiếu Q, đọc khối Ghi chú không duyệt\n"
     "2. Bấm Sửa, chỉnh số tiền\n"
     "3. Bấm Lưu và gửi duyệt\n"
     "4. Kiểm trạng thái phiếu",
     "—",
     "- Khối Ghi chú không duyệt hiển thị đúng lý do bị từ chối, ở dạng chỉ đọc\n"
     "- Nút Sửa CÓ hiện với phiếu Không duyệt\n"
     "- ⚠️ Màn Sửa KHÔNG hiện Ghi chú không duyệt — người lập phải mở màn chi tiết mới đọc được\n"
     "- Sau khi lưu, phiếu quay lại Chờ TP duyệt"),

    ("035", "Không sửa được phiếu đang trong dây chuyền duyệt", "P0",
     "Phiếu R do chính người đăng nhập lập, đang ở Chờ kế toán công nợ duyệt",
     "1. Tìm phiếu R, mở menu hành động\n"
     "2. Mở màn chi tiết phiếu R, quan sát hàng nút",
     "—",
     "- Menu chỉ có In và Xuất Excel\n"
     "- Màn chi tiết không có nút Sửa và Xóa"),

    ("036", "Bố cục màn Chi tiết", "P0",
     "Phiếu S trạng thái Duyệt phiếu chi, 3 dòng chi tiết, loại tiền USD; người đăng nhập không có "
     "quyền duyệt nào",
     "1. Bấm Mã phiếu để mở chi tiết\n"
     "2. Quan sát toàn màn",
     "—",
     "- Tiêu đề trang \"Chi tiết phiếu đề nghị thanh toán\"\n"
     "- Mọi ô đều khóa, gồm cả 4 ô Ghi chú duyệt TP / KT công nợ / KT trưởng / BGĐ\n"
     "- Bảng chi tiết có đủ 5 nhóm cột tiền: Số tiền đề nghị chi, TP duyệt, KT công nợ duyệt, "
     "KT trưởng/BGD, Số tiền chi — mỗi nhóm tách 2 cột vì phiếu ngoại tệ\n"
     "- Hàng nút chỉ có In, Xuất Excel, Quay lại"),

    ("037", "Bốn ô Ghi chú duyệt chỉ mở cho đúng cấp và đúng bước", "P0",
     "Phiếu đang ở Chờ kế toán công nợ duyệt; lần lượt mở bằng KTCN-1, TP-1, KTT-1",
     "1. Với mỗi tài khoản, mở chi tiết phiếu\n"
     "2. Thử gõ vào từng ô trong 4 ô Ghi chú duyệt",
     "3 tài khoản",
     "- KTCN-1: chỉ ô \"Ghi chú duyệt KT công nợ\" gõ được, 3 ô còn lại khóa\n"
     "- TP-1: cả 4 ô đều khóa (phiếu đã qua bước của TP)\n"
     "- KTT-1: cả 4 ô đều khóa (chưa tới bước của KT trưởng)"),

    ("038", "Cột Số tiền chi lấy từ phiếu chi đã lập", "P1",
     "Phiếu đã có Phiếu chi hoặc Phiếu ủy nhiệm chi lập từ nó, số duyệt chi của từng dòng khác số đề "
     "nghị",
     "1. Mở chi tiết phiếu\n"
     "2. Đọc nhóm cột \"Số tiền chi\" của từng dòng",
     "—",
     "- Cột Số tiền chi hiện đúng số đã duyệt trên phiếu chi tương ứng\n"
     "- Phiếu chưa lập phiếu chi thì cột này trống hoặc bằng 0"),

    ("039", "Nút Quay lại trở về danh sách", "P2",
     "Đang mở màn chi tiết",
     "1. Bấm nút Quay lại",
     "—",
     "- Về màn danh sách chế độ Tất cả\n"
     "- Bộ lọc đang dùng trước đó vẫn còn"),

    ("040", "Rời màn nhập dở không có cảnh báo", "P2",
     "Màn Tạo mới, đã nhập Lý do chi và 1 dòng chi tiết, chưa lưu",
     "1. Bấm nút Quay lại",
     "—",
     "- Về thẳng màn danh sách\n"
     "- ⚠️ KHÔNG có cảnh báo \"thông tin chưa lưu\", dữ liệu mất hẳn. Ghi nhận đúng hiện trạng"),
]
