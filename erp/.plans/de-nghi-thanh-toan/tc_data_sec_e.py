# -*- coding: utf-8 -*-
"""Section VIII — rang buoc nhap lieu."""

SEC_VIII = [
    ("001", "Lưu khi để trống Lý do chi", "P0",
     "Màn Tạo mới, đã chọn Loại chi và Hình thức thanh toán, có 1 dòng chi tiết hợp lệ, để trống Lý do chi",
     "1. Bấm Lưu\n"
     "2. Quan sát",
     "Lý do chi: để trống",
     "- Không lưu\n"
     "- Lỗi đỏ \"Bắt buộc nhập\" ngay dưới ô Lý do chi\n"
     "- Ở lại form, dữ liệu đã nhập còn nguyên"),

    ("002", "Lưu khi để trống Loại chi hoặc Hình thức thanh toán", "P0",
     "Màn Tạo mới, đã điền Lý do chi",
     "1. Bỏ trống Loại chi, bấm Lưu, quan sát\n"
     "2. Chọn Loại chi, bỏ trống Hình thức thanh toán, bấm Lưu",
     "—",
     "- Cả 2 lần đều không lưu\n"
     "- Lỗi đỏ \"Bắt buộc nhập\" hiện đúng dưới ô đang thiếu\n"
     "- Kèm lỗi ở phần Chi tiết vì bảng chưa hiện nên chưa có dòng nào"),

    ("003", "Lưu khi để trống Loại tiền hoặc Tỷ giá", "P0",
     "Màn Tạo mới đã điền các ô khác hợp lệ",
     "1. Xóa lựa chọn ở ô Loại tiền, bấm Lưu\n"
     "2. Chọn lại Loại tiền là USD, xóa sạch ô Tỷ giá, bấm Lưu",
     "—",
     "- Cả 2 lần đều không lưu\n"
     "- Lỗi đỏ \"Bắt buộc nhập\" hiện đúng dưới ô đang thiếu"),

    ("004", "Lưu khi bảng chi tiết không có dòng nào", "P0",
     "Loại chi = Thanh toán chi phí vận chuyển NCC, chưa bấm Lấy dữ liệu nên bảng trống; đã điền các ô "
     "bắt buộc khác",
     "1. Bấm Lưu\n"
     "2. Quan sát dưới bảng chi tiết",
     "0 dòng chi tiết",
     "- Không lưu\n"
     "- Lỗi đỏ \"Bắt buộc nhập\" hiện ngay dưới bảng chi tiết"),

    ("005", "Lưu khi dòng chi tiết chưa chọn đối tượng ở hình thức TM", "P0",
     "Loại chi = Chi trả lại khách hàng, Hình thức TM, có 1 dòng trống hoàn toàn, Lý do chi đã điền",
     "1. Bấm Lưu\n"
     "2. Quan sát dòng chi tiết",
     "—",
     "- Không lưu\n"
     "- Ô Khách hàng của dòng 1 báo lỗi \"Bắt buộc nhập\"\n"
     "- Ô Số đơn hàng/Hợp đồng cũng báo lỗi \"Bắt buộc nhập\"\n"
     "- Ô Số tiền đề nghị chi báo lỗi \"Bắt buộc nhập\""),

    ("006", "Lưu khi hình thức CK mà chưa chọn đối tượng ở đầu phiếu", "P0",
     "Loại chi = Chi trả lại khách hàng, Hình thức CK, chưa chọn Khách hàng ở đầu phiếu",
     "1. Bấm Lưu\n"
     "2. Quan sát ô Khách hàng ở đầu phiếu",
     "—",
     "- Không lưu\n"
     "- Ô Khách hàng ở đầu phiếu báo lỗi \"Bắt buộc nhập\"\n"
     "- Lặp lại với Loại chi = Chi trả nhà cung cấp, Hình thức CK: ô Nhà cung cấp báo lỗi tương ứng"),

    ("007", "Lưu khi chuyển khoản trong nước mà thiếu thông tin ngân hàng", "P0",
     "Loại chi = Chi trả lại khách hàng, Hình thức CK, đã chọn khách hàng, xóa sạch 5 ô thông tin "
     "ngân hàng",
     "1. Bấm Lưu\n"
     "2. Quan sát khối thông tin ngân hàng",
     "—",
     "- Không lưu\n"
     "- Cả 5 ô đều báo lỗi \"Bắt buộc nhập\": Số tài khoản, Tên tài khoản, Ngân hàng, Chi nhánh, "
     "Tỉnh/Thành phố"),

    ("008", "Lưu khi chuyển khoản quốc tế mà thiếu mã định danh ngân hàng hoặc Phí", "P0",
     "Loại chi = Chi trả nhà cung cấp, Hình thức CK, nhà cung cấp NƯỚC NGOÀI",
     "1. Xóa ô mã định danh ngân hàng, bấm Lưu\n"
     "2. Điền lại, xóa lựa chọn ở ô Phí, bấm Lưu",
     "—",
     "- Cả 2 lần đều không lưu\n"
     "- Lỗi đỏ \"Bắt buộc nhập\" hiện đúng dưới ô đang thiếu\n"
     "- ⚠️ Chuyển khoản quốc tế KHÔNG bắt buộc Chi nhánh và Tỉnh/Thành phố như chuyển khoản trong nước"),

    ("009", "Loại Chi trả nhà cung cấp bắt buộc có tệp đính kèm khi tạo mới", "P0",
     "Màn Tạo mới, Loại chi = Chi trả nhà cung cấp, mọi ô khác đã điền hợp lệ, CHƯA chọn tệp nào",
     "1. Bấm Lưu\n"
     "2. Quan sát khối File đính kèm\n"
     "3. Chọn 1 tệp pdf rồi bấm Lưu lại",
     "—",
     "- Bước 1: không lưu, báo lỗi ở khối File đính kèm\n"
     "- Bước 3: lưu thành công\n"
     "- Nhãn khối có dấu bắt buộc màu đỏ khi Loại chi là Chi trả nhà cung cấp"),

    ("010", "Ba loại chi còn lại không bắt buộc tệp đính kèm", "P0",
     "Lần lượt tạo 3 phiếu loại Chi trả lại khách hàng, Chi thưởng thực hiện hợp đồng, Thanh toán chi "
     "phí vận chuyển NCC — không đính kèm tệp nào",
     "1. Với mỗi loại, điền đủ các ô bắt buộc rồi bấm Lưu",
     "3 loại chi",
     "- Cả 3 đều lưu thành công không cần tệp\n"
     "- Nhãn khối File đính kèm KHÔNG có dấu bắt buộc"),

    ("011", "Sửa phiếu Chi trả nhà cung cấp đã có tệp thì không bắt buộc thêm tệp", "P1",
     "Phiếu Chi trả nhà cung cấp đã lưu và đã có 1 tệp đính kèm",
     "1. Mở màn Sửa, không thêm tệp mới\n"
     "2. Đổi Lý do chi, bấm Lưu",
     "—",
     "- Lưu thành công, không đòi thêm tệp\n"
     "- Tệp cũ vẫn còn trên phiếu"),

    ("012", "Đính kèm tệp sai định dạng", "P0",
     "Màn Tạo mới, Loại chi = Chi trả nhà cung cấp",
     "1. Chọn một tệp có phần mở rộng không nằm trong danh sách cho phép (ví dụ tệp exe hoặc txt)\n"
     "2. Bấm Lưu",
     "Tệp .exe hoặc .txt",
     "- Không lưu\n"
     "- Hệ thống báo lỗi ở khối File đính kèm\n"
     "- Định dạng cho phép: pdf, png, jpg, jpeg, doc, docx, xls, xlsx, zip"),

    ("013", "Đính kèm tệp quá dung lượng", "P1",
     "Có sẵn 1 tệp pdf dung lượng trên 20 MB",
     "1. Chọn tệp đó ở khối File đính kèm\n"
     "2. Bấm Lưu",
     "Tệp pdf khoảng 25 MB",
     "- Không lưu, hệ thống báo lỗi dung lượng ở khối File đính kèm\n"
     "- Tệp dưới 20 MB thì lưu được"),

    ("014", "Loại vận chuyển bắt buộc có Đến ngày và Nhà cung cấp", "P0",
     "Loại chi = Thanh toán chi phí vận chuyển NCC, đã điền Lý do chi",
     "1. Bỏ trống ô Đến ngày, bấm Lưu\n"
     "2. Điền Đến ngày, bỏ trống Nhà cung cấp, bấm Lưu",
     "—",
     "- Cả 2 lần đều không lưu\n"
     "- Lỗi đỏ \"Bắt buộc nhập\" hiện đúng dưới ô đang thiếu"),

    ("015", "Số tiền đề nghị chi bằng 0 bị chặn", "P0",
     "Loại chi = Chi trả lại khách hàng, 1 dòng đủ khách hàng và hợp đồng, để Số tiền đề nghị chi = 0",
     "1. Bấm Lưu\n"
     "2. Quan sát dòng chi tiết",
     "Số tiền đề nghị chi: 0",
     "- Không lưu\n"
     "- Ô Số tiền đề nghị chi báo lỗi đỏ (hệ thống yêu cầu số tiền tối thiểu là 1)\n"
     "- ⚠️ Khác màn Đề nghị thu tiền: bên đó số 0 lưu được"),

    ("016", "Số tiền đề nghị chi âm bị chặn", "P0",
     "1 dòng đủ đối tượng và hợp đồng",
     "1. Thử gõ dấu trừ rồi số vào ô Số tiền đề nghị chi\n"
     "2. Bấm Lưu",
     "Số tiền: -1.000.000",
     "- Ô tiền không nhận dấu trừ, hoặc nếu nhận thì khi Lưu báo lỗi đỏ\n"
     "- Không tạo được phiếu có số tiền âm"),

    ("017", "Ô Số tiền chỉ nhận số và tự thêm dấu ngăn nghìn", "P1",
     "Đang ở dòng chi tiết",
     "1. Gõ chữ cái vào ô Số tiền đề nghị chi\n"
     "2. Gõ 12000000, rời ô\n"
     "3. Quan sát cột quy đổi và dòng Tổng cộng",
     "Nhập chữ, rồi 12000000",
     "- Chữ cái không được nhận\n"
     "- Số hiện thành 12.000.000\n"
     "- Cột quy đổi và dòng Tổng cộng cập nhật theo"),

    ("018", "Số tiền có phần thập phân trên phiếu ngoại tệ", "P2",
     "Phiếu loại tiền USD, tỷ giá 25.000, 1 dòng",
     "1. Nhập Số tiền đề nghị chi = 1.234,56\n"
     "2. Rời ô, đọc lại giá trị và cột quy đổi\n"
     "3. Lưu và mở lại phiếu",
     "1.234,56 USD",
     "- Giữ đúng 2 chữ số thập phân, không bị làm tròn về số nguyên\n"
     "- Cột quy đổi VND tính đúng theo tỷ giá\n"
     "- Mở lại vẫn đúng số vừa nhập"),

    ("019", "Loại vận chuyển không bắt buộc số tiền cho dòng bỏ tích", "P1",
     "Loại chi = Thanh toán chi phí vận chuyển NCC, bảng đã nạp 4 dòng, bỏ tích 2 dòng và để trống số "
     "tiền của 2 dòng đó",
     "1. Điền số tiền cho 2 dòng còn tích\n"
     "2. Bấm Lưu",
     "—",
     "- Lưu thành công, không đòi số tiền của 2 dòng bỏ tích\n"
     "- Phiếu lưu xong chỉ còn 2 dòng đã tích"),

    ("020", "Lý do chi và Ghi chú nhận chuỗi dài có dấu tiếng Việt", "P2",
     "Màn Tạo mới hợp lệ",
     "1. Nhập Lý do chi dài khoảng 200 ký tự có dấu\n"
     "2. Nhập Ghi chú dòng chi tiết khoảng 200 ký tự có dấu\n"
     "3. Lưu rồi mở lại chi tiết",
     "Chuỗi dài có dấu",
     "- Lưu được, không cắt chữ, không lỗi font\n"
     "- Cột Lý do chi ngoài danh sách hiển thị đầy đủ hoặc rút gọn nhưng không vỡ bố cục"),

    ("021", "Bỏ qua giao diện gửi lên loại chi không hợp lệ", "P1",
     "Tài khoản bất kỳ; dùng công cụ kiểm thử API",
     "1. Gọi thẳng chức năng Tạo phiếu, gửi Loại chi = 99\n"
     "2. Quan sát kết quả và danh sách phiếu",
     "Loại chi: 99",
     "- ⚠️ Hiện trạng: hệ thống chỉ kiểm tra Loại chi phải là số, nên phiếu Loại chi 99 TẠO ĐƯỢC và "
     "hiện trong danh sách với cột Loại chi để trống. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: chỉ nhận các loại chi có trong danh mục"),

    ("022", "Bỏ qua giao diện gửi lên trạng thái tùy ý khi tạo phiếu", "P0",
     "Tài khoản bất kỳ; dùng công cụ kiểm thử API",
     "1. Gọi thẳng chức năng Tạo phiếu với trạng thái là Chờ tạo phiếu chi\n"
     "2. Tìm phiếu vừa tạo trong danh sách, đọc Trạng thái",
     "Trạng thái gửi lên: Chờ tạo phiếu chi",
     "- ⚠️ Hiện trạng: phiếu được tạo NGAY ở trạng thái Chờ tạo phiếu chi, bỏ qua toàn bộ 3 cấp duyệt. "
     "LỖ HỔNG, ghi nhận Failed\n"
     "- Kỳ vọng đúng: khi tạo chỉ cho 2 trạng thái Đang tạo hoặc Chờ TP duyệt"),

    ("023", "Thông báo lỗi khi lưu gặp sự cố", "P1",
     "Dựng một trường hợp làm việc lưu thất bại (ví dụ nhờ đội kỹ thuật tạm ngắt dịch vụ lưu tệp đính "
     "kèm) trên môi trường test",
     "1. Bấm Lưu ở màn Sửa\n"
     "2. Quan sát màn hình",
     "—",
     "- ⚠️ Hiện trạng: màn hình đổ ra một khối chữ kỹ thuật dài thay vì câu \"Cập nhật phiếu đề nghị "
     "thanh toán thất bại!\". Ghi nhận Failed kèm ảnh chụp toàn màn hình\n"
     "- Kỳ vọng đúng: hiện thông báo lỗi ngắn gọn, giữ nguyên dữ liệu người dùng đang nhập"),
]
