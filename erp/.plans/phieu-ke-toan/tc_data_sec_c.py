# -*- coding: utf-8 -*-
"""Section V, VI, VII — luu & duyet ghi so, xoa, in & xuat Excel."""

SEC_V = [
    ("001", "Lưu nháp phiếu hợp lệ", "P0",
     "Màn Tạo phiếu đã nhập: Diễn giải, Loại tiền VNĐ, 2 dòng chi tiết cùng Nhóm định khoản 1, nợ "
     "1.000.000 và có 1.000.000",
     "1. Bấm nút Lưu\n"
     "2. Quan sát thông báo và màn hình\n"
     "3. Tìm phiếu vừa tạo trong danh sách",
     "—",
     "- Hệ thống báo tạo phiếu kế toán thành công\n"
     "- Tự chuyển về danh sách chế độ Tất cả\n"
     "- Phiếu mới ở trạng thái Đang tạo\n"
     "- ⚠️ Chưa có bút toán nào trong Sổ chi tiết các tài khoản"),

    ("002", "Mã phiếu sinh đúng quy tắc", "P0",
     "Người lập thuộc công ty mã TP; đang là tháng 09 năm 2026; công ty chưa có phiếu kế toán nào "
     "trong tháng",
     "1. Lưu một phiếu mới\n"
     "2. Đọc mã phiếu trên danh sách",
     "—",
     "- Mã có dạng TP.PKT0925.00001\n"
     "- Đúng thứ tự: mã công ty, dấu chấm, chữ PKT, tháng và năm 4 số, dấu chấm, 5 chữ số"),

    ("003", "Mã phiếu tăng dần và đếm lại theo tháng", "P1",
     "Công ty đã có phiếu TP.PKT0925.00001",
     "1. Lưu thêm 2 phiếu trong tháng 09\n"
     "2. Đổi ngày hệ thống sang tháng 10, lưu 1 phiếu nữa\n"
     "3. Đọc 3 mã phiếu vừa tạo",
     "—",
     "- Hai phiếu tháng 09 mang mã 00002 và 00003\n"
     "- Phiếu tháng 10 quay lại 00001 với phần tháng năm là 1025"),

    ("004", "Công ty, phòng ban, bộ phận lấy theo hồ sơ người lập", "P1",
     "Người lập KT-1 thuộc công ty 3, phòng ban PB-2, bộ phận BP-5",
     "1. Lưu một phiếu mới\n"
     "2. Đăng nhập tài khoản có quyền xem tổng công ty, lọc theo công ty 3\n"
     "3. Tìm phiếu vừa tạo",
     "—",
     "- Phiếu xuất hiện khi lọc theo công ty 3\n"
     "- Không xuất hiện khi lọc theo công ty khác"),

    ("005", "Lưu và duyệt phiếu hợp lệ", "P0",
     "Màn Tạo phiếu đã nhập hợp lệ: Nợ tài khoản 1311 số tiền 1.000.000, Có tài khoản 5111 số tiền "
     "1.000.000, cùng Nhóm định khoản 1",
     "1. Bấm nút Lưu và duyệt\n"
     "2. Quan sát thông báo\n"
     "3. Tìm phiếu trong danh sách",
     "—",
     "- Hệ thống báo duyệt phiếu kế toán thành công\n"
     "- Phiếu ở trạng thái Đã duyệt, nhãn tô xanh\n"
     "- Cột Tổng phát sinh hiện 1.000.000"),

    ("006", "Duyệt phiếu sinh bút toán vào Sổ chi tiết các tài khoản", "P0",
     "Phiếu vừa duyệt ở trường hợp trên",
     "1. Mở màn Sổ chi tiết các tài khoản\n"
     "2. Lọc theo tài khoản 1311 và theo tài khoản 5111\n"
     "3. Tìm bút toán của phiếu vừa duyệt",
     "—",
     "- Sinh đúng 2 bút toán: một bên NỢ tài khoản 1311, một bên CÓ tài khoản 5111\n"
     "- Số tiền, loại tiền, tỷ giá, mã phí, mã vụ việc, nhóm định khoản khớp với dòng chi tiết\n"
     "- Ngày ghi sổ là Ngày hạch toán trên phiếu, không phải ngày lập phiếu"),

    ("007", "Bút toán đối ứng khi một nợ nhiều có", "P0",
     "Phiếu nhóm 1 có 3 dòng: Nợ tài khoản A 3.000.000 · Có tài khoản B 1.000.000 · Có tài khoản C "
     "2.000.000",
     "1. Lưu và duyệt phiếu\n"
     "2. Mở Sổ chi tiết các tài khoản, xem tài khoản đối ứng của từng bút toán",
     "—",
     "- Dòng tài khoản A (số tiền lớn nhất) là dòng gốc, đối ứng với CẢ tài khoản B và tài khoản C\n"
     "- Dòng tài khoản B đối ứng với tài khoản A\n"
     "- Dòng tài khoản C đối ứng với tài khoản A"),

    ("008", "Bút toán đối ứng không lặp khi trùng tài khoản trong nhóm", "P1",
     "Phiếu nhóm 1 có 3 dòng: Nợ tài khoản A 3.000.000 · Có tài khoản B 1.000.000 (khách KH-01) · Có "
     "tài khoản B 2.000.000 (khách KH-02)",
     "1. Lưu và duyệt phiếu\n"
     "2. Xem tài khoản đối ứng của dòng tài khoản A",
     "—",
     "- Dòng tài khoản A chỉ ghi đối ứng với tài khoản B MỘT lần, không ghi hai lần"),

    ("009", "Duyệt phiếu gắn phiếu yêu cầu xuất hàng ghi nhận chứng từ gốc", "P0",
     "Phiếu có dòng gắn hợp đồng nguyên tắc và phiếu yêu cầu xuất hàng đã có phiếu xuất hàng tương ứng",
     "1. Lưu và duyệt phiếu\n"
     "2. Mở Sổ chi tiết các tài khoản, xem cột chứng từ gốc của bút toán đó",
     "—",
     "- Bút toán trỏ đúng tới Phiếu xuất hàng tương ứng\n"
     "- Với dòng gắn phiếu yêu cầu xuất bán hàng mượn thì trỏ tới phiếu Bán hàng mượn"),

    ("010", "Duyệt phiếu có đánh dấu số dư đầu kỳ", "P0",
     "Phiếu có dòng gắn hợp đồng nguyên tắc và ĐÃ tích ô Số dư nợ đầu kì",
     "1. Lưu và duyệt phiếu\n"
     "2. Mở Sổ chi tiết các tài khoản, xem chứng từ gốc của bút toán đó",
     "—",
     "- Bút toán trỏ tới bản khai báo công nợ đầu kỳ của hợp đồng, không trỏ tới phiếu xuất hàng"),

    ("011", "Dòng không có số tiền không sinh bút toán", "P1",
     "Phiếu có 3 dòng, trong đó 1 dòng cả nợ và có đều bằng 0 (nếu hệ thống cho lưu)",
     "1. Lưu và duyệt phiếu\n"
     "2. Đếm số bút toán sinh ra",
     "—",
     "- Chỉ sinh 2 bút toán cho 2 dòng có số tiền\n"
     "- Dòng 0 đồng bị bỏ qua"),

    ("012", "Duyệt phiếu điều chỉnh từ Báo có cập nhật số đã điều chỉnh", "P0",
     "Chi tiết Báo có BC-01 có số tiền 10.000.000, đã điều chỉnh 8.000.000; phiếu kế toán đang lập "
     "điều chỉnh thêm 2.000.000 bên nợ trên chính dòng gắn BC-01",
     "1. Lưu và duyệt phiếu\n"
     "2. Mở màn Báo có, xem chi tiết BC-01",
     "Phát sinh nợ: 2.000.000",
     "- Số tiền đã điều chỉnh của BC-01 tăng lên đúng 10.000.000\n"
     "- Phần còn lại được điều chỉnh của BC-01 về 0"),

    ("013", "Cảnh báo hợp đồng còn số dư lẻ khi Lưu và duyệt", "P0",
     "Công ty đặt mức số dư lẻ được điều chỉnh là 10.000; hợp đồng HD-01 sau bút toán này còn dư nợ "
     "6.000; phiếu có dòng Có tài khoản 1311 gắn HD-01",
     "1. Bấm nút Lưu và duyệt\n"
     "2. Quan sát màn hình và danh sách phiếu",
     "—",
     "- Hệ thống cảnh báo \"Hợp đồng có số dư lẻ\"\n"
     "- Hiện khối \"Bạn có muốn điều chỉnh số dư lẻ không?\" với dòng ghi rõ hợp đồng HD-01 còn số dư "
     "nợ 6.000\n"
     "- ⚠️ Phiếu CHƯA được lưu và CHƯA được duyệt ở bước này"),

    ("014", "Số dư lẻ vượt mức cấu hình thì không cảnh báo", "P0",
     "Công ty đặt mức số dư lẻ được điều chỉnh là 10.000; hợp đồng HD-02 sau bút toán còn dư nợ 50.000",
     "1. Bấm nút Lưu và duyệt",
     "—",
     "- Không hiện khối điều chỉnh số dư lẻ\n"
     "- Phiếu được duyệt ngay và sinh bút toán"),

    ("015", "Tích điều chỉnh số dư lẻ khi hợp đồng còn dư NỢ", "P0",
     "Đang hiện khối cảnh báo, hợp đồng HD-01 còn dư nợ 6.000; phiếu đang có 2 dòng ở Nhóm định khoản 1",
     "1. Tích ô \"Hợp đồng HD-01 còn số dư nợ 6.000\"\n"
     "2. Quan sát bảng chi tiết",
     "—",
     "- Bảng thêm 2 dòng ở NHÓM ĐỊNH KHOẢN MỚI (nhóm 2)\n"
     "- Một dòng Nợ tài khoản 811 số tiền 6.000, có Mã phí là mã điều chỉnh số dư công nợ khách hàng\n"
     "- Một dòng Có tài khoản 1311 số tiền 6.000, cùng khách hàng và hợp đồng HD-01\n"
     "- Cả 2 dòng có Diễn giải \"Điều chỉnh số dư lẻ\""),

    ("016", "Tích điều chỉnh số dư lẻ khi hợp đồng còn dư CÓ", "P0",
     "Đang hiện khối cảnh báo với hợp đồng HD-03 còn số dư CÓ 4.000",
     "1. Tích ô tương ứng\n"
     "2. Quan sát bảng chi tiết",
     "—",
     "- Thêm 2 dòng ở nhóm định khoản mới\n"
     "- Một dòng Nợ tài khoản 1311 số tiền 4.000\n"
     "- Một dòng Có tài khoản 711 số tiền 4.000, có Mã phí là mã điều chỉnh số dư công nợ khách hàng\n"
     "- Diễn giải \"Điều chỉnh số dư lẻ\""),

    ("017", "Bỏ tích điều chỉnh số dư lẻ", "P1",
     "Đã tích và bảng đã sinh 2 dòng điều chỉnh",
     "1. Bỏ tích ô đó\n"
     "2. Quan sát bảng chi tiết",
     "—",
     "- Hai dòng điều chỉnh biến mất\n"
     "- Các dòng ban đầu giữ nguyên, không bị mất hay nhân đôi"),

    ("018", "Bấm Lưu và duyệt lần thứ hai sau khi xử lý số dư lẻ", "P0",
     "Đang hiện khối cảnh báo, đã tích hoặc không tích",
     "1. Bấm nút Lưu và duyệt lần thứ hai\n"
     "2. Quan sát thông báo và danh sách",
     "—",
     "- Không hiện lại khối cảnh báo\n"
     "- Phiếu được duyệt, báo duyệt phiếu kế toán thành công\n"
     "- Nếu đã tích thì phiếu có thêm nhóm định khoản điều chỉnh số dư lẻ"),

    ("019", "Lưu nháp không kiểm tra số dư lẻ", "P1",
     "Phiếu có hợp đồng còn số dư lẻ trong mức cấu hình",
     "1. Bấm nút Lưu (không phải Lưu và duyệt)",
     "—",
     "- Lưu nháp thành công ngay\n"
     "- Không hiện khối điều chỉnh số dư lẻ"),

    ("020", "Lưu nháp từ chứng từ nguồn cập nhật trạng thái chứng từ nguồn", "P0",
     "Phiếu yêu cầu điều chỉnh công nợ YCDC-01 đang ở trạng thái đã duyệt; Phiếu yêu cầu hạch toán bổ "
     "sung HTBS-01 đang chờ hạch toán",
     "1. Lập phiếu kế toán từ YCDC-01, bấm Lưu, mở lại màn YCDC-01\n"
     "2. Lập phiếu kế toán từ HTBS-01, bấm Lưu, mở lại màn HTBS-01",
     "—",
     "- YCDC-01 chuyển sang trạng thái đã tạo phiếu kế toán, không cho chọn lại để lập phiếu khác\n"
     "- HTBS-01 chuyển sang trạng thái Đang duyệt"),

    ("021", "Duyệt phiếu cập nhật trạng thái chứng từ nguồn và gửi thông báo", "P0",
     "Đang lập phiếu kế toán từ Phiếu yêu cầu hạch toán bổ sung HTBS-01 do NV-A lập",
     "1. Bấm Lưu và duyệt\n"
     "2. Mở màn HTBS-01, đọc trạng thái và người duyệt\n"
     "3. Đăng nhập bằng NV-A, mở khu vực thông báo",
     "—",
     "- HTBS-01 chuyển Đã duyệt, ghi đúng người duyệt và thời điểm duyệt\n"
     "- NV-A nhận được thông báo nội dung nêu tên người duyệt và mã HTBS-01, bấm vào mở đúng phiếu"),

    ("022", "Duyệt phiếu lập từ Chi phí vận chuyển nhanh", "P0",
     "Đang lập phiếu từ 2 bản ghi Chi phí vận chuyển nhanh",
     "1. Bấm Lưu và duyệt\n"
     "2. Mở lại bảng Chi phí vận chuyển nhanh, tìm 2 bản ghi đó",
     "—",
     "- Hai bản ghi chuyển sang trạng thái đã hạch toán\n"
     "- Hai bản ghi không còn hiện trong danh sách chờ lập phiếu\n"
     "- Từ bản ghi mở được sang phiếu kế toán vừa tạo"),

    ("023", "Không bấm được nút Lưu nhiều lần liên tiếp", "P0",
     "Màn Tạo phiếu đã nhập hợp lệ",
     "1. Bấm nút Lưu liên tục 5 lần thật nhanh\n"
     "2. Về danh sách đếm số phiếu mới",
     "—",
     "- Ngay sau lần bấm đầu, cả hai nút Lưu và Lưu và duyệt chuyển sang trạng thái chờ, hiện biểu "
     "tượng xoay và không bấm được nữa\n"
     "- Chỉ tạo ra đúng 1 phiếu"),

    ("024", "Lỗi giữa chừng thì không tạo phiếu nửa vời", "P1",
     "Chuẩn bị dữ liệu gây lỗi ở bước ghi chi tiết (ví dụ hợp đồng bị xóa ngay trước khi bấm Lưu)",
     "1. Bấm Lưu\n"
     "2. Về danh sách kiểm tra\n"
     "3. Mở Sổ chi tiết các tài khoản kiểm tra",
     "—",
     "- Hệ thống báo thêm phiếu kế toán thất bại\n"
     "- KHÔNG có phiếu nào được tạo, kể cả phiếu rỗng\n"
     "- KHÔNG có bút toán nào lọt vào sổ"),

    ("025", "Giao diện không có nút Hủy phiếu", "P1",
     "Có phiếu ở cả trạng thái Đang tạo và Đã duyệt",
     "1. Mở menu Hành động của từng phiếu\n"
     "2. Mở màn Sửa và màn chi tiết, soát toàn bộ nút",
     "—",
     "- Không có nút Hủy ở bất kỳ đâu\n"
     "- ⚠️ Trạng thái Hủy vẫn nằm trong ô lọc nhưng không có đường nào tạo ra nó từ giao diện. Ghi "
     "nhận để nghiệp vụ quyết định bổ sung nút hay bỏ trạng thái"),

    ("026", "Duyệt phiếu lập từ Yêu cầu hạch toán hoa hồng tháng", "P1",
     "Đang lập phiếu kế toán từ Phiếu yêu cầu hạch toán hoa hồng tháng HH-01",
     "1. Bấm Lưu và duyệt\n"
     "2. Mở màn HH-01 đọc trạng thái\n"
     "3. Mở Sổ chi tiết các tài khoản kiểm tra bút toán hoa hồng",
     "—",
     "- HH-01 chuyển sang trạng thái đã hạch toán\n"
     "- Bút toán hoa hồng được ghi đủ theo từng dòng chi tiết"),
]

SEC_VI = [
    ("001", "Xóa phiếu nháp của mình", "P0",
     "Phiếu P ở trạng thái Đang tạo do chính mình lập",
     "1. Bấm Hành động rồi bấm Xóa\n"
     "2. Đọc nội dung cửa sổ xác nhận\n"
     "3. Bấm đồng ý",
     "—",
     "- Có cửa sổ xác nhận trước khi xóa\n"
     "- Sau khi đồng ý: hệ thống báo xóa phiếu kế toán thành công\n"
     "- Phiếu P biến mất khỏi danh sách"),

    ("002", "Hủy bỏ ở cửa sổ xác nhận xóa", "P1",
     "Phiếu P ở trạng thái Đang tạo do chính mình lập",
     "1. Bấm Hành động rồi bấm Xóa\n"
     "2. Bấm nút hủy bỏ trên cửa sổ xác nhận\n"
     "3. Kiểm tra danh sách",
     "—",
     "- Phiếu P vẫn còn nguyên trong danh sách"),

    ("003", "Không xóa được phiếu đã duyệt", "P0",
     "Phiếu Q đã duyệt do chính mình lập",
     "1. Mở menu Hành động của phiếu Q\n"
     "2. Dán đường dẫn chức năng xóa phiếu Q vào thanh địa chỉ",
     "—",
     "- Menu Hành động không có mục Xóa\n"
     "- Gọi trực tiếp: hệ thống báo không có quyền thực hiện thao tác này, phiếu Q còn nguyên"),

    ("004", "Không xóa được phiếu nháp của người khác", "P0",
     "Phiếu P ở trạng thái Đang tạo do NV-A lập; đăng nhập bằng NV-B",
     "1. Dán đường dẫn chức năng xóa phiếu P vào thanh địa chỉ",
     "—",
     "- Hệ thống báo không có quyền thực hiện thao tác này\n"
     "- Phiếu P còn nguyên khi NV-A đăng nhập lại"),

    ("005", "Xóa phiếu lập từ Yêu cầu điều chỉnh công nợ trả lại trạng thái chứng từ nguồn", "P0",
     "Phiếu P nháp được lập từ YCDC-01; YCDC-01 đang ở trạng thái đã tạo phiếu kế toán",
     "1. Xóa phiếu P\n"
     "2. Mở màn YCDC-01 đọc trạng thái\n"
     "3. Mở màn Tạo phiếu kế toán, bấm kính lúp chọn phiếu yêu cầu",
     "—",
     "- YCDC-01 quay về trạng thái chờ duyệt\n"
     "- YCDC-01 xuất hiện lại trong cửa sổ chọn phiếu yêu cầu, lập phiếu mới được"),

    ("006", "Xóa phiếu lập từ Yêu cầu hạch toán hoa hồng tháng", "P1",
     "Phiếu P nháp lập từ HH-01; HH-01 đang ở trạng thái Đang duyệt",
     "1. Xóa phiếu P\n"
     "2. Mở màn HH-01 đọc trạng thái",
     "—",
     "- HH-01 quay lại trạng thái chờ hạch toán, lập được phiếu kế toán mới"),

    ("007", "Xóa phiếu lập từ Yêu cầu hạch toán bổ sung", "P0",
     "Phiếu P nháp lập từ HTBS-01; HTBS-01 đang ở trạng thái Đang duyệt",
     "1. Xóa phiếu P\n"
     "2. Mở màn HTBS-01 đọc trạng thái\n"
     "3. Thử lập phiếu kế toán mới từ HTBS-01",
     "—",
     "- Kết quả mong đợi: HTBS-01 quay lại trạng thái chờ hạch toán và lập được phiếu mới\n"
     "- ⚠️ Hiện trạng dự kiến LỖI: HTBS-01 kẹt ở Đang duyệt. Nếu kẹt thì ghi Failed"),

    ("008", "Xóa phiếu không tồn tại", "P2",
     "—",
     "1. Dán đường dẫn chức năng xóa với một mã phiếu không có thật",
     "Mã phiếu: 999999999",
     "- Hệ thống báo dữ liệu không tồn tại\n"
     "- Không trắng trang, không lỗi hệ thống"),
]

SEC_VII = [
    ("001", "In phiếu kế toán", "P0",
     "Phiếu Q đã duyệt, có 4 dòng chi tiết; hệ thống đã cấu hình mẫu in Phiếu điều chỉnh công nợ",
     "1. Bấm Hành động rồi bấm In\n"
     "2. Đối chiếu nội dung bản in với màn chi tiết",
     "—",
     "- Mở bản in khổ NGANG\n"
     "- Có tiêu đề công ty, mã phiếu, mã chứng từ nguồn, người lập, ngày hạch toán\n"
     "- Bảng chi tiết in đủ số dòng và có dòng tổng cộng\n"
     "- Không còn ô nào để trống dạng ký hiệu thay thế"),

    ("002", "In phiếu ngoại tệ", "P1",
     "Phiếu USD, tỷ giá 25.000, phát sinh nợ 100 USD",
     "1. Bấm Hành động rồi bấm In\n"
     "2. Đọc bảng chi tiết trên bản in",
     "—",
     "- Bản in có thêm cột nguyên tệ và thể hiện tỷ giá\n"
     "- Số tiền nguyên tệ và số quy đổi khớp với màn chi tiết"),

    ("003", "In phiếu lập tay không có chứng từ nguồn", "P2",
     "Phiếu lập tay hoàn toàn",
     "1. Bấm In\n"
     "2. Xem dòng mã chứng từ nguồn trên bản in",
     "—",
     "- Ô mã chứng từ nguồn để TRỐNG, không in ra chữ rỗng hay ký hiệu lạ"),

    ("004", "In khi hệ thống chưa cấu hình mẫu in", "P2",
     "Tạm gỡ mẫu in Phiếu điều chỉnh công nợ khỏi danh mục mẫu báo cáo",
     "1. Bấm Hành động rồi bấm In",
     "—",
     "- Hệ thống báo không tìm thấy mẫu, không trắng trang\n"
     "- Sau khi khôi phục mẫu thì in lại bình thường"),

    ("005", "Xuất Excel chi tiết phiếu", "P0",
     "Phiếu Q đã duyệt, 4 dòng chi tiết",
     "1. Bấm Hành động rồi bấm Xuất Excel\n"
     "2. Mở tệp tải về, đối chiếu với màn chi tiết",
     "—",
     "- Tệp tải về tên là chi tiết phiếu kế toán\n"
     "- Nội dung khớp: thông tin chung, đủ 4 dòng chi tiết, dòng tổng cộng\n"
     "- Số tiền trong tệp ở dạng SỐ, cộng được bằng công thức"),

    ("006", "Xuất Excel phiếu ngoại tệ", "P1",
     "Phiếu USD, tỷ giá 25.000",
     "1. Bấm Xuất Excel\n"
     "2. Mở tệp, soát cột tiền",
     "—",
     "- Tệp có cả cột nguyên tệ và cột quy đổi VNĐ\n"
     "- Thể hiện rõ tỷ giá của phiếu"),

    ("007", "In và Xuất Excel với phiếu ở mọi trạng thái", "P1",
     "Có phiếu Đang tạo và phiếu Đã duyệt",
     "1. Thử In và Xuất Excel với cả hai phiếu",
     "—",
     "- Cả hai chức năng chạy được với mọi trạng thái\n"
     "- Phiếu nháp in ra vẫn đủ nội dung, có thể ghi rõ là bản nháp"),

    ("008", "Màn hình không có chức năng nhập Excel", "P2",
     "Đang ở màn danh sách và màn Tạo phiếu",
     "1. Soát toàn bộ nút trên hai màn",
     "—",
     "- Không có nút nhập dữ liệu từ Excel ở bất kỳ đâu\n"
     "- Ghi Không áp dụng cho nhóm kiểm thử nhập tệp"),
]
