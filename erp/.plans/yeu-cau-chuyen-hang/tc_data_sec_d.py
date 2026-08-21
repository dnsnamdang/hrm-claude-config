# -*- coding: utf-8 -*-
"""Section VIII (rang buoc nhap lieu), IX (co lap du lieu), X (luong dau - cuoi)."""

SEC_VIII = [
    ("001", "Lưu khi chưa chọn hàng hóa nào", "P0",
     "Màn Tạo mới, đã đính kèm 1 tệp PDF, bảng chi tiết còn trống",
     "1. Bấm Lưu\n"
     "2. Quan sát",
     "0 hàng hóa",
     "- Không lưu, thông báo \"Tạo yêu cầu thất bại!\"\n"
     "- Lỗi đỏ \"Bắt buộc phải nhập\" hiện ngay dưới bảng chi tiết\n"
     "- Ở lại form, dữ liệu đã nhập còn nguyên"),

    ("002", "Lưu khi hàng hóa chưa có dòng khách hàng nào", "P0",
     "Đã thêm 1 hàng hóa và chọn ĐVT, nhưng chưa bấm Thêm khách hàng",
     "1. Bấm Lưu\n"
     "2. Quan sát dòng hàng hóa",
     "—",
     "- Không lưu\n"
     "- Lỗi đỏ \"Bắt buộc phải nhập\" hiện trong ô Khách hàng của hàng hóa đó"),

    ("003", "Lưu khi chưa chọn đơn vị tính", "P0",
     "Đã thêm 1 hàng hóa, xóa lựa chọn ở ô ĐVT, dòng khách hàng đã điền đủ",
     "1. Bấm Lưu\n"
     "2. Quan sát",
     "—",
     "- Không lưu\n"
     "- Lỗi đỏ \"Bắt buộc phải nhập\" ngay dưới ô ĐVT"),

    ("004", "Lưu khi dòng khách hàng chưa chọn khách hàng", "P0",
     "Đã thêm 1 hàng hóa và 1 dòng khách hàng trống hoàn toàn",
     "1. Bấm Lưu\n"
     "2. Quan sát dòng khách hàng",
     "—",
     "- Không lưu\n"
     "- Cả 4 ô đều báo lỗi: Khách hàng, SL, Ngày cần, Ghi chú — đều \"Bắt buộc phải nhập\""),

    ("005", "Lưu khi để trống Số lượng", "P0",
     "Dòng khách hàng đã chọn khách hàng, ngày cần và ghi chú; để trống SL",
     "1. Bấm Lưu\n"
     "2. Quan sát",
     "SL: để trống",
     "- Không lưu\n"
     "- Chỉ ô SL báo lỗi \"Bắt buộc phải nhập\", 3 ô còn lại sạch"),

    ("006", "Số lượng bằng 0 bị chặn", "P0",
     "Dòng khách hàng đã điền đủ, nhập SL = 0",
     "1. Bấm Lưu\n"
     "2. Quan sát",
     "SL: 0",
     "- Không lưu\n"
     "- Ô SL báo lỗi \"Không hợp lệ\" (số lượng tối thiểu là 1)\n"
     "- Sửa thành 1 thì lưu được"),

    ("007", "Số lượng âm bị chặn", "P0",
     "Dòng khách hàng đã điền đủ",
     "1. Thử gõ -5 vào ô SL\n"
     "2. Bấm Lưu",
     "SL: -5",
     "- Ô SL không nhận số âm, hoặc nếu nhận thì khi Lưu báo \"Không hợp lệ\"\n"
     "- Không tạo được phiếu có số lượng âm"),

    ("008", "Số lượng vượt giới hạn bị chặn", "P1",
     "Dòng khách hàng đã điền đủ",
     "1. Nhập SL = 1000000000 (một tỷ)\n"
     "2. Bấm Lưu\n"
     "3. Sửa thành 999999999, bấm Lưu lại",
     "—",
     "- Lần 1: không lưu, ô SL báo \"Không hợp lệ\"\n"
     "- Lần 2: lưu được (đây là giới hạn trên)"),

    ("009", "Số lượng là số lẻ", "P2",
     "Dòng khách hàng đã điền đủ",
     "1. Nhập SL = 2,5\n"
     "2. Bấm Lưu\n"
     "3. Mở lại phiếu, đọc lại SL và dòng Tổng cộng",
     "SL: 2,5",
     "- Ghi nhận thực tế: ô SL có nhận số lẻ hay tự làm tròn\n"
     "- Nếu lưu được thì dòng Tổng cộng phải cộng đúng phần lẻ\n"
     "- ⚠️ Ô SL khai bước nhảy là 1, nên nhiều trình duyệt sẽ chặn số lẻ ngay trên giao diện"),

    ("010", "Ngày cần bằng hôm nay bị chặn", "P0",
     "Dòng khách hàng đã điền đủ các ô khác",
     "1. Chọn Ngày cần là NGÀY HÔM NAY\n"
     "2. Bấm Lưu\n"
     "3. Đổi sang ngày mai, bấm Lưu lại",
     "Hôm nay, rồi ngày mai",
     "- Lần 1: KHÔNG lưu, ô Ngày cần báo \"Không hợp lệ\"\n"
     "- Lần 2: lưu được\n"
     "- ⚠️ Ngày cần phải LỚN HƠN hôm nay, chọn đúng hôm nay là không hợp lệ — bẫy dễ hiểu nhầm"),

    ("011", "Ngày cần trong quá khứ bị chặn", "P0",
     "Dòng khách hàng đã điền đủ các ô khác",
     "1. Chọn Ngày cần là ngày hôm qua\n"
     "2. Bấm Lưu",
     "—",
     "- Không lưu, ô Ngày cần báo \"Không hợp lệ\""),

    ("012", "Ngày cần để trống bị chặn", "P0",
     "Dòng khách hàng đã điền khách hàng, SL, ghi chú; để trống Ngày cần",
     "1. Bấm Lưu",
     "—",
     "- Không lưu\n"
     "- Chỉ ô Ngày cần báo lỗi \"Bắt buộc phải nhập\""),

    ("013", "Ghi chú của dòng khách hàng bắt buộc", "P0",
     "Dòng khách hàng đã điền khách hàng, SL, ngày cần; để trống Ghi chú",
     "1. Bấm Lưu\n"
     "2. Quan sát",
     "Ghi chú dòng: để trống",
     "- Không lưu\n"
     "- Ô Ghi chú của dòng báo lỗi \"Bắt buộc phải nhập\"\n"
     "- ⚠️ Khác với Ghi chú của PHIẾU — ô đó không bắt buộc (xem TC_04.035)"),

    ("014", "Ghi chú của dòng vượt 255 ký tự", "P1",
     "Dòng khách hàng đã điền đủ",
     "1. Nhập Ghi chú dòng dài khoảng 300 ký tự\n"
     "2. Bấm Lưu\n"
     "3. Rút xuống khoảng 250 ký tự, bấm Lưu lại",
     "—",
     "- Lần 1: không lưu, ô Ghi chú báo lỗi vượt độ dài\n"
     "- Lần 2: lưu được, mở lại giữ nguyên nội dung"),

    ("015", "Ghi chú của phiếu vượt 255 ký tự", "P1",
     "Màn Tạo mới đã điền đủ hàng hóa và khách hàng",
     "1. Nhập Ghi chú của phiếu dài khoảng 300 ký tự\n"
     "2. Bấm Lưu",
     "—",
     "- Không lưu\n"
     "- Lỗi \"Không được nhập quá 255 ký tự\" ngay dưới ô Ghi chú"),

    ("016", "Chuỗi tiếng Việt có dấu trong ghi chú", "P2",
     "Màn Tạo mới hợp lệ",
     "1. Nhập Ghi chú phiếu và Ghi chú dòng bằng tiếng Việt có dấu, khoảng 200 ký tự\n"
     "2. Lưu, mở lại chi tiết và mở bản in",
     "—",
     "- Lưu được, không cắt chữ, không lỗi font ở cả màn chi tiết lẫn bản in"),

    ("017", "Tạo mới bắt buộc có tệp đính kèm", "P0",
     "Màn Tạo mới đã điền đủ hàng hóa và khách hàng, CHƯA chọn tệp nào",
     "1. Bấm Lưu\n"
     "2. Quan sát khối File đính kèm\n"
     "3. Chọn 1 tệp PDF rồi bấm Lưu lại",
     "—",
     "- Lần 1: không lưu, lỗi \"Bắt buộc phải chọn\" ở khối File đính kèm\n"
     "- Lần 2: lưu thành công\n"
     "- Nhãn khối có dấu bắt buộc màu đỏ"),

    ("018", "Chỉ nhận tệp định dạng PDF", "P0",
     "Màn Tạo mới, đã điền đủ hàng hóa và khách hàng",
     "1. Chọn một tệp ảnh hoặc tệp Word ở khối File đính kèm\n"
     "2. Bấm Lưu\n"
     "3. Đổi sang tệp PDF, bấm Lưu lại",
     "Tệp .jpg hoặc .docx, rồi .pdf",
     "- Lần 1: không lưu, hệ thống báo \"Không hợp lệ\" ở khối File đính kèm\n"
     "- Lần 2: lưu thành công\n"
     "- ⚠️ Màn này CHỈ nhận PDF, khác màn Đề nghị thanh toán (màn kia nhận nhiều định dạng)"),

    ("019", "Sửa phiếu không bắt buộc thêm tệp mới", "P0",
     "Phiếu P trạng thái Đang tạo, đã có 1 tệp đính kèm",
     "1. Mở màn Sửa, không thêm tệp mới\n"
     "2. Đổi Ghi chú, bấm Lưu\n"
     "3. Xóa hết tệp đính kèm rồi bấm Lưu lần nữa",
     "—",
     "- Bước 2: lưu thành công, không đòi thêm tệp\n"
     "- Bước 3: ghi nhận thực tế — hệ thống có cho lưu phiếu không còn tệp nào hay không; nếu cho thì "
     "báo lại nghiệp vụ vì tạo mới lại bắt buộc"),

    ("020", "Chặn trùng hàng hóa ở phía hệ thống", "P0",
     "Tài khoản bất kỳ; dùng công cụ kiểm thử API",
     "1. Gọi thẳng chức năng Tạo phiếu, gửi 2 dòng hàng hóa CÙNG một mã hàng\n"
     "2. Quan sát phản hồi và danh sách phiếu",
     "2 dòng cùng hàng hóa",
     "- Hệ thống CHẶN, trả về thông báo \"Thông tin không hợp lệ!\"\n"
     "- Không tạo được phiếu\n"
     "- ⚠️ Ràng buộc này được kiểm ở CẢ giao diện lẫn phía hệ thống — điểm làm đúng"),

    ("021", "Chặn trạng thái không hợp lệ khi lưu", "P0",
     "Tài khoản bất kỳ; dùng công cụ kiểm thử API",
     "1. Gọi thẳng chức năng Tạo phiếu với trạng thái là \"Đã tiếp nhận\"\n"
     "2. Gọi lại với trạng thái \"Đã phân bổ\"\n"
     "3. Quan sát phản hồi và danh sách phiếu",
     "—",
     "- Cả 2 lần đều bị CHẶN, báo trạng thái không hợp lệ\n"
     "- Chỉ nhận 2 trạng thái Đang tạo và Chờ duyệt khi lưu\n"
     "- ⚠️ Điểm làm đúng, khác ba màn phiếu tài chính (những màn đó tạo được phiếu ở trạng thái bất kỳ)"),

    ("022", "Chặn hàng hóa và khách hàng không tồn tại", "P1",
     "Tài khoản bất kỳ; dùng công cụ kiểm thử API",
     "1. Gọi thẳng chức năng Tạo phiếu, gửi mã hàng hóa không có thật\n"
     "2. Gọi lại với khách hàng không có thật\n"
     "3. Gọi lại với đơn vị tính không có thật",
     "—",
     "- Cả 3 lần đều bị chặn, hệ thống báo không tồn tại\n"
     "- Không tạo được phiếu"),

    ("023", "Chặn ngày cần trong quá khứ ở phía hệ thống", "P1",
     "Tài khoản bất kỳ; dùng công cụ kiểm thử API",
     "1. Gọi thẳng chức năng Tạo phiếu, gửi Ngày cần là ngày hôm qua\n"
     "2. Gọi lại với Ngày cần là hôm nay",
     "—",
     "- Cả 2 lần đều bị chặn, báo \"Không hợp lệ\"\n"
     "- Ràng buộc giống hệt trên giao diện"),
]

SEC_IX = [
    ("001", "Hai người cùng lập phiếu tại một thời điểm", "P0",
     "2 tài khoản cùng công ty, cùng chuẩn bị sẵn form Tạo mới hợp lệ",
     "1. Cả 2 bấm Lưu gần như cùng lúc\n"
     "2. Đối chiếu Mã yêu cầu của 2 phiếu vừa tạo\n"
     "3. Lặp lại 3 lần",
     "—",
     "- Cả 2 phiếu đều lưu thành công\n"
     "- 2 mã KHÁC nhau (mã sinh theo số thứ tự bản ghi nên không đụng nhau)\n"
     "- Nếu ra trùng mã thì ghi Failed kèm ảnh chụp"),

    ("002", "Bấm Lưu nhiều lần liên tiếp", "P0",
     "Màn Tạo mới đã điền hợp lệ",
     "1. Bấm nút Lưu liên tục 3 lần thật nhanh\n"
     "2. Quan sát nút\n"
     "3. Mở danh sách, đếm số phiếu vừa tạo",
     "—",
     "- Nút chuyển sang trạng thái đang xử lý và bị vô hiệu sau lần bấm đầu\n"
     "- CHỈ MỘT phiếu được tạo; nếu ra 2 hoặc 3 phiếu thì ghi Failed"),

    ("003", "Hai kế toán kho cùng xử lý một phiếu", "P0",
     "2 tài khoản kế toán kho cùng công ty, cùng mở chi tiết một phiếu ở Chờ duyệt",
     "1. Kế toán 1 nhập ghi chú và bấm Không duyệt\n"
     "2. Kế toán 2 (chưa tải lại) cũng nhập ghi chú khác và bấm Không duyệt\n"
     "3. Mở lại phiếu, đọc Trạng thái, Ghi chú duyệt và Người tiếp nhận",
     "—",
     "- Kế toán 2 bị hệ thống từ chối với thông báo \"Không có quyền\" (phiếu đã rời trạng thái Chờ "
     "duyệt)\n"
     "- Ghi chú duyệt và Người tiếp nhận giữ nguyên của kế toán 1\n"
     "- ⚠️ Điểm làm đúng của màn này"),

    ("004", "Một kế toán Không duyệt trong khi người kia đang Tổng hợp", "P0",
     "2 tab: tab 1 là KT-1 đang ở màn tạo Phiếu yêu cầu xuất hàng từ phiếu X; tab 2 là KT-2 mở chi tiết "
     "phiếu X",
     "1. Tab 2: KT-2 nhập ghi chú và bấm Không duyệt (thành công, phiếu X về Đang tạo)\n"
     "2. Tab 1: KT-1 điền xong và bấm Lưu phiếu yêu cầu xuất hàng\n"
     "3. Mở lại phiếu X, đọc Trạng thái",
     "—",
     "- ⚠️ Điểm rủi ro: ghi nhận thực tế phiếu X kết thúc ở trạng thái nào. Nếu phiếu X bị đẩy sang "
     "\"Đã tiếp nhận\" dù vừa bị từ chối thì ghi Failed kèm ảnh chụp cả 2 tab\n"
     "- Kỳ vọng đúng: bước 2 bị chặn vì phiếu đã rời trạng thái Chờ duyệt"),

    ("005", "Người lập sửa phiếu trong khi kế toán đang xử lý", "P0",
     "2 tab: tab 1 là NV-A đang mở màn Sửa phiếu nháp; tab 2 dùng chính NV-A bấm Lưu & Gửi phiếu đó",
     "1. Tab 2 gửi phiếu\n"
     "2. Tab 1 sửa Ghi chú rồi bấm Lưu\n"
     "3. Mở lại phiếu, đọc Trạng thái và Ghi chú",
     "—",
     "- Tab 1 bị hệ thống từ chối vì phiếu đã rời trạng thái Đang tạo\n"
     "- Phiếu giữ nguyên trạng thái Chờ duyệt, không bị đẩy về Đang tạo\n"
     "- ⚠️ Kiểm kỹ có câu thông báo hiện ra không; nếu màn hình im lặng không báo gì thì ghi Failed "
     "(mục 9 ghi chú 9)"),

    ("006", "Phạm vi dữ liệu không rò rỉ giữa các công ty", "P0",
     "Tài khoản chỉ có quyền xem theo công ty, thuộc công ty 3",
     "1. Lọc theo tên, mã hàng hóa bằng mã hàng chỉ dùng ở công ty 1\n"
     "2. Lọc Người tạo bằng một nhân viên công ty 1\n"
     "3. Nhập khoảng ngày rất rộng\n"
     "4. Bấm Xuất excel và mở tệp",
     "—",
     "- Cả 4 cách đều không làm lộ phiếu của công ty 1\n"
     "- Tổng luôn nằm trong phạm vi công ty 3"),

    ("007", "Màn Chờ duyệt không lộ phiếu ngoài công ty", "P0",
     "KT-1 thuộc công ty 3; công ty 1 cũng có phiếu ở Chờ duyệt",
     "1. Mở màn Chờ duyệt\n"
     "2. Dùng ô lọc Công ty chọn công ty 1, bấm tìm kiếm\n"
     "3. Dùng ô lọc Người tạo chọn một nhân viên công ty 1",
     "—",
     "- Cả 2 cách đều cho kết quả rỗng\n"
     "- ⚠️ Nếu ra phiếu của công ty 1 thì ghi Failed"),

    ("008", "Số tồn kho thay đổi không ảnh hưởng phiếu đã lưu", "P1",
     "Phiếu lập tuần trước, lúc lập SL tồn của hàng hóa là 100; nay tồn đã đổi",
     "1. Mở chi tiết phiếu, chọn kho ở ô Xem tồn\n"
     "2. Đọc cột SL tồn\n"
     "3. Đọc cột số lượng của các dòng khách hàng",
     "—",
     "- Cột SL tồn hiện số tồn HIỆN TẠI, khác 100\n"
     "- Số lượng yêu cầu của từng dòng KHÔNG đổi\n"
     "- ⚠️ Đúng thiết kế: SL tồn chỉ để tham khảo, không lưu vào phiếu"),

    ("009", "Giá niêm yết đổi trong danh mục không đổi phiếu đã lưu", "P1",
     "Phiếu đã lưu với giá niêm yết 1.500.000; sau đó bảng giá đổi",
     "1. Mở chi tiết phiếu, đọc Giá niêm yết\n"
     "2. So với giá mới trong danh mục hàng hóa",
     "—",
     "- Ghi nhận thực tế: phiếu hiện giá đã lưu hay giá mới\n"
     "- ⚠️ Nếu hiện giá mới thì báo lại nghiệp vụ, vì phiếu cũ sẽ không còn khớp bản in đã ký"),

    ("010", "Xóa phiếu xong danh sách nạp lại đúng số tổng", "P1",
     "Đang lọc Trạng thái = Đang tạo, có 5 phiếu",
     "1. Xóa 1 phiếu\n"
     "2. Đọc lại số tổng và các ô lọc",
     "—",
     "- Tổng còn 4\n"
     "- Ghi nhận thực tế bộ lọc có được giữ lại hay không"),

    ("011", "Mở phiếu của nhân sự không còn phòng ban", "P2",
     "Phiếu do một nhân viên đã bị gỡ khỏi phòng ban lập",
     "1. Mở màn danh sách chứa phiếu đó\n"
     "2. Mở chi tiết và bản in",
     "—",
     "- Ghi nhận đúng hiện trạng: dòng vẫn hiện hay cả bảng báo lỗi\n"
     "- ⚠️ Nếu bảng hoặc bản in không tải được thì ghi Failed"),
]

SEC_X = [
    ("001", "Vòng đời đầy đủ: lập nháp - sửa - gửi - tiếp nhận", "P0",
     "NV-A thuộc công ty 3; KT-1 là kế toán kho công ty 3; có sẵn hàng hóa HH-001, HH-002 và khách hàng "
     "KH-001, KH-002",
     "1. NV-A tạo phiếu, đính kèm 1 tệp PDF, thêm HH-001 với 2 dòng khách hàng, bấm Lưu\n"
     "2. NV-A mở lại phiếu bằng Sửa yêu cầu, thêm HH-002 với 1 dòng khách hàng, bấm Lưu\n"
     "3. NV-A mở lại lần nữa, bấm Lưu & Gửi\n"
     "4. KT-1 mở màn Chờ duyệt, mở phiếu, bấm Tổng hợp\n"
     "5. KT-1 điền và lưu Phiếu yêu cầu xuất hàng\n"
     "6. NV-A mở chuông thông báo và xem lại phiếu",
     "Vòng đời một phiếu",
     "- Bước 1: trạng thái Đang tạo, chỉ NV-A thấy; có mục Sửa và Xóa\n"
     "- Bước 2: sửa được, phiếu vẫn Đang tạo\n"
     "- Bước 3: trạng thái Chờ duyệt, mất mục Sửa và Xóa, KT-1 nhận thông báo\n"
     "- Bước 4: chuyển sang màn Phiếu yêu cầu xuất hàng; phiếu VẪN ở Chờ duyệt\n"
     "- Bước 5: phiếu chuyển sang Đã tiếp nhận, cột Người tiếp nhận và Ngày tiếp nhận được điền\n"
     "- Bước 6: NV-A nhận thông báo đã tiếp nhận; phiếu chỉ còn mục In yêu cầu"),

    ("002", "Vòng đời bị Không duyệt rồi gửi lại", "P0",
     "NV-A và KT-1 như TC_10.001",
     "1. NV-A lập phiếu và bấm Lưu & Gửi\n"
     "2. KT-1 mở phiếu, nhập Ghi chú duyệt \"Sai số lượng\", bấm Không duyệt\n"
     "3. KT-1 mở lại màn Chờ duyệt và màn Kế toán kho theo dõi, tìm phiếu\n"
     "4. NV-A mở chuông thông báo, mở phiếu, đọc Ghi chú duyệt\n"
     "5. NV-A bấm Sửa yêu cầu, chỉnh số lượng, bấm Lưu & Gửi\n"
     "6. KT-1 mở lại màn Chờ duyệt",
     "—",
     "- Bước 2: phiếu về trạng thái Đang tạo; KT-1 được chuyển sang màn Kế toán kho theo dõi\n"
     "- Bước 3: phiếu KHÔNG còn ở cả hai màn của KT-1\n"
     "- Bước 4: NV-A nhận thông báo từ chối; đọc được lý do; cột Người tiếp nhận và Ngày tiếp nhận đã "
     "có dữ liệu dù phiếu đang là nháp\n"
     "- Bước 5: sửa và gửi lại được\n"
     "- Bước 6: phiếu xuất hiện trở lại ở màn Chờ duyệt"),

    ("003", "Vòng đời phiếu bị hủy phiếu xuất hàng", "P0",
     "Phiếu đã ở trạng thái Đã tiếp nhận, gắn với một Phiếu yêu cầu xuất hàng",
     "1. Ghi lại Trạng thái, Người tiếp nhận, Ngày tiếp nhận của phiếu\n"
     "2. Xóa hẳn Phiếu yêu cầu xuất hàng ở màn của nó\n"
     "3. Quay lại đọc 3 thông tin trên\n"
     "4. KT-1 mở màn Chờ duyệt\n"
     "5. KT-1 Tổng hợp lại phiếu đó",
     "—",
     "- Sau bước 2: phiếu quay về Chờ duyệt, Người tiếp nhận và Ngày tiếp nhận bị xóa trắng\n"
     "- Phiếu xuất hiện lại ở màn Chờ duyệt\n"
     "- Tổng hợp lại được bình thường, chạy tiếp vòng đời"),

    ("004", "Phiếu nhiều hàng hóa nhiều khách hàng đi hết vòng", "P0",
     "NV-A; có sẵn 3 hàng hóa và 4 khách hàng",
     "1. Tạo phiếu với 3 hàng hóa, tổng 6 dòng khách hàng, ngày cần khác nhau\n"
     "2. Đính kèm 2 tệp PDF, bấm Lưu & Gửi\n"
     "3. Xem danh sách, mở chi tiết, mở bản in, xuất Excel danh sách\n"
     "4. KT-1 Tổng hợp, kiểm dữ liệu nạp sang màn Phiếu yêu cầu xuất hàng",
     "3 hàng hóa, 6 dòng khách hàng",
     "- Lưu và gửi thành công\n"
     "- Chi tiết và bản in hiện đủ 3 khối hàng hóa và 6 dòng khách hàng\n"
     "- Dòng Tổng cộng của từng hàng hóa đúng bằng tổng SL các dòng của nó\n"
     "- Màn Phiếu yêu cầu xuất hàng nạp đủ 3 hàng hóa và 6 dòng khách hàng"),

    ("005", "Gộp hai phiếu của cùng một người vào một phiếu xuất hàng", "P0",
     "NV-A có 2 phiếu đang ở Chờ duyệt; KT-1 là kế toán kho",
     "1. KT-1 bấm Tổng hợp từ phiếu thứ nhất\n"
     "2. Ở màn Phiếu yêu cầu xuất hàng, thêm tiếp phiếu thứ hai\n"
     "3. Bấm Lưu\n"
     "4. Quay lại kiểm trạng thái cả 2 phiếu",
     "2 phiếu cùng một người lập",
     "- Gộp được, không bị chặn\n"
     "- CẢ HAI phiếu chuyển sang Đã tiếp nhận\n"
     "- NV-A nhận 2 thông báo tiếp nhận\n"
     "- ⚠️ Thử gộp thêm phiếu của người khác thì bị chặn — xem TC_05.005"),

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
     "- Bước 5 khớp luôn, KHÔNG phải cộng bù ngày cuối (màn này tính trọn ngày — mục 4)"),
]
