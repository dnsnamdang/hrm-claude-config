# -*- coding: utf-8 -*-
"""Section VIII, IX, X — rang buoc nhap lieu, co lap du lieu, luong dau - cuoi."""

SEC_VIII = [
    ("001", "Bỏ trống Diễn giải của phiếu", "P0",
     "Màn Tạo phiếu, chi tiết đã nhập hợp lệ",
     "1. Xóa trắng ô Diễn giải\n"
     "2. Bấm Lưu",
     "Diễn giải: để trống",
     "- Hệ thống báo lỗi đỏ \"Bắt buộc nhập\" ngay dưới ô Diễn giải\n"
     "- Phiếu không được tạo, dữ liệu đã nhập vẫn còn trên form"),

    ("002", "Bỏ trống Loại tiền", "P0",
     "Màn Tạo phiếu, chi tiết đã nhập hợp lệ",
     "1. Chọn lại Loại tiền về dòng trống\n"
     "2. Bấm Lưu",
     "Loại tiền: để trống",
     "- Báo lỗi đỏ \"Bắt buộc nhập\" dưới ô Loại tiền\n"
     "- Phiếu không được tạo"),

    ("003", "Bỏ trống Tỷ giá khi chọn ngoại tệ", "P0",
     "Đã chọn Loại tiền USD",
     "1. Xóa trắng ô Tỷ giá\n"
     "2. Bấm Lưu",
     "Tỷ giá: để trống",
     "- Báo lỗi đỏ \"Bắt buộc nhập\" dưới ô Tỷ giá\n"
     "- Phiếu không được tạo"),

    ("004", "Nhập Tỷ giá bằng 0", "P0",
     "Đã chọn Loại tiền USD, đã nhập chi tiết 100 USD",
     "1. Nhập Tỷ giá là 0\n"
     "2. Đọc cột VNĐ của các dòng\n"
     "3. Bấm Lưu và duyệt",
     "Tỷ giá: 0",
     "- Cột VNĐ của mọi dòng về 0\n"
     "- Kết quả mong đợi: hệ thống chặn, báo tỷ giá phải lớn hơn 0\n"
     "- ⚠️ Nếu lưu được thì Sổ chi tiết các tài khoản ghi bút toán 0 đồng — ghi Failed và báo ngay"),

    ("005", "Lưu phiếu không có dòng chi tiết nào", "P0",
     "Màn Tạo phiếu, đã nhập đủ thông tin chung",
     "1. Không thêm dòng chi tiết nào\n"
     "2. Bấm Lưu",
     "—",
     "- Hệ thống báo bắt buộc nhập chi tiết\n"
     "- Phiếu không được tạo"),

    ("006", "Để trống Ngày hạch toán", "P1",
     "Màn Tạo phiếu, mọi thứ khác hợp lệ",
     "1. Xóa trắng ô Ngày hạch toán\n"
     "2. Bấm Lưu\n"
     "3. Mở lại phiếu vừa tạo",
     "Ngày hạch toán: để trống",
     "- ⚠️ Dù nhãn có dấu sao đỏ, hệ thống KHÔNG chặn: phiếu vẫn lưu được\n"
     "- Ngày hạch toán được điền tự động bằng ngày hiện tại\n"
     "- Ghi nhận để nghiệp vụ quyết định có chặn hay không"),

    ("007", "Gõ tay Ngày hạch toán sai định dạng", "P0",
     "Màn Tạo phiếu, mọi thứ khác hợp lệ",
     "1. Gõ tay vào ô Ngày hạch toán một chuỗi không phải ngày/tháng/năm\n"
     "2. Bấm Lưu",
     "Ngày hạch toán: 2025-13-45",
     "- Kết quả mong đợi: báo lỗi đỏ dưới ô Ngày hạch toán, cửa sổ không đóng, dữ liệu còn nguyên\n"
     "- ⚠️ Hiện trạng dự kiến LỖI: trang trắng hoặc báo lỗi hệ thống. Nếu vậy ghi Failed"),

    ("008", "Ngày hạch toán lùi về kỳ trước hoặc đẩy sang tương lai", "P1",
     "Kỳ kế toán tháng trước đã khóa sổ",
     "1. Chọn Ngày hạch toán là một ngày của tháng trước, bấm Lưu và duyệt\n"
     "2. Tạo phiếu khác, chọn Ngày hạch toán là ngày của năm sau, bấm Lưu và duyệt",
     "Tháng trước · Năm sau",
     "- Kiểm tra hệ thống có chặn ghi sổ vào kỳ đã khóa hay không\n"
     "- ⚠️ Nếu cả hai đều ghi sổ được thì đây là rủi ro nghiệp vụ, ghi nhận để kế toán trưởng quyết"),

    ("009", "Diễn giải phiếu nhập rất dài", "P2",
     "Màn Tạo phiếu",
     "1. Dán 1000 ký tự vào ô Diễn giải\n"
     "2. Bấm Lưu\n"
     "3. Mở lại phiếu và xem cột Diễn giải ngoài danh sách",
     "1000 ký tự",
     "- Lưu thành công hoặc báo lỗi rõ ràng về độ dài\n"
     "- Không xuất hiện lỗi hệ thống\n"
     "- Nội dung đọc lại không bị cắt cụt giữa chừng mà không báo gì"),

    ("010", "Không chọn Số tài khoản ở dòng chi tiết", "P0",
     "Có 3 dòng chi tiết, dòng thứ 2 chưa chọn tài khoản",
     "1. Bấm Lưu\n"
     "2. Quan sát vị trí báo lỗi",
     "—",
     "- Báo lỗi đỏ \"Bắt buộc nhập\" ngay dưới ô Số tài khoản của ĐÚNG dòng thứ 2\n"
     "- Hai dòng còn lại không bị đánh dấu lỗi"),

    ("011", "Bỏ trống Diễn giải của dòng chi tiết", "P0",
     "Có dòng chi tiết đã chọn tài khoản và số tiền, chưa nhập Diễn giải dòng",
     "1. Bấm Lưu",
     "—",
     "- Báo lỗi đỏ \"Bắt buộc nhập\" dưới ô Diễn giải của dòng đó\n"
     "- Phiếu không được tạo"),

    ("012", "Bỏ trống Nhóm định khoản", "P0",
     "Có dòng chi tiết đầy đủ nhưng ô Nhóm định khoản để trống",
     "1. Bấm Lưu",
     "—",
     "- Báo lỗi đỏ \"Bắt buộc nhập\" dưới ô Nhóm định khoản\n"
     "- Phiếu không được tạo"),

    ("013", "Nhập số tiền âm", "P0",
     "Có dòng chi tiết",
     "1. Nhập Phát sinh nợ là số âm\n"
     "2. Bấm Lưu",
     "Phát sinh nợ: -1.000.000",
     "- Hệ thống chặn, báo số tiền không được nhỏ hơn 0\n"
     "- Phiếu không được tạo"),

    ("014", "Nhập chữ vào ô số tiền", "P1",
     "Có dòng chi tiết",
     "1. Gõ chuỗi chữ vào ô Phát sinh nợ, bấm ra ngoài\n"
     "2. Bấm Lưu",
     "Phát sinh nợ: abc",
     "- Ô không nhận ký tự chữ, hoặc tự về 0\n"
     "- Không xuất hiện lỗi hệ thống"),

    ("015", "Dòng chi tiết không nhập cả nợ lẫn có", "P0",
     "Có 2 dòng cùng nhóm; dòng 2 để cả Phát sinh nợ và Phát sinh có bằng 0",
     "1. Bấm Lưu",
     "—",
     "- Hệ thống báo \"Bắt buộc nhập phát sinh nợ hoặc phát sinh có\"\n"
     "- Phiếu không được tạo"),

    ("016", "Tài khoản theo dõi công nợ bắt buộc chọn đối tượng", "P0",
     "Chọn một tài khoản được cấu hình theo dõi công nợ, để trống cột Mã khách",
     "1. Bấm Lưu",
     "—",
     "- Báo lỗi đỏ \"Bắt buộc nhập\" dưới ô chọn đối tượng ở cột Mã khách"),

    ("017", "Tài khoản tiền gửi ngân hàng bắt buộc chọn Ngân hàng", "P0",
     "Dòng chi tiết chọn tài khoản 1211, để trống ô Ngân hàng",
     "1. Bấm Lưu",
     "Số tài khoản: 1211",
     "- Báo lỗi đỏ \"Bắt buộc nhập\" dưới ô Ngân hàng\n"
     "- Áp dụng cho cả 1211, 1212 và 1213"),

    ("018", "Tài khoản tiền gửi ngân hàng bắt buộc chọn STK ngân hàng", "P0",
     "Dòng chi tiết chọn tài khoản 1211, đã chọn Ngân hàng, để trống STK ngân hàng",
     "1. Bấm Lưu",
     "Số tài khoản: 1211",
     "- Báo lỗi đỏ \"Bắt buộc nhập\" dưới ô STK ngân hàng"),

    ("019", "Tài khoản chi phí bắt buộc chọn Mã phí", "P0",
     "Dòng chi tiết chọn tài khoản 811, để trống ô Mã phí",
     "1. Bấm Lưu",
     "Số tài khoản: 811",
     "- Báo lỗi đỏ \"Bắt buộc nhập\" dưới ô Mã phí\n"
     "- Áp dụng cho mọi tài khoản thuộc nhóm chi phí"),

    ("020", "Tài khoản 3361 bắt buộc chọn đối tượng", "P1",
     "Dòng chi tiết chọn tài khoản 3361, để trống cột Mã khách",
     "1. Bấm Lưu",
     "Số tài khoản: 3361",
     "- Báo lỗi đỏ \"Bắt buộc nhập\" dưới ô chọn đối tượng"),

    ("021", "Tài khoản phải thu khách hàng bắt buộc chọn hợp đồng", "P0",
     "Dòng chi tiết chọn tài khoản 1311, chọn khách hàng thường KH-01, để trống Đơn hàng/Hợp đồng",
     "1. Bấm Lưu",
     "Số tài khoản: 1311 · Khách: KH-01",
     "- Báo lỗi đỏ \"Bắt buộc nhập\" dưới ô Đơn hàng/Hợp đồng\n"
     "- Áp dụng cho cả tài khoản 1312"),

    ("022", "Khách hàng KHÁCH KHÔNG RÕ không bắt buộc hợp đồng", "P0",
     "Danh mục có khách hàng tên KHÁCH KHÔNG RÕ; dòng chi tiết chọn tài khoản 1311 và khách hàng này, "
     "để trống Đơn hàng/Hợp đồng",
     "1. Bấm Lưu",
     "Số tài khoản: 1311 · Khách: KHÁCH KHÔNG RÕ",
     "- Lưu thành công, KHÔNG báo lỗi bắt buộc hợp đồng\n"
     "- Đây là ngoại lệ có chủ đích cho khoản thu chưa xác định được khách"),

    ("023", "Tài khoản chi phí chờ phân bổ bắt buộc hợp đồng và mã vụ việc", "P0",
     "Dòng chi tiết chọn tài khoản 35241, để trống cả Đơn hàng/Hợp đồng và Mã vụ việc",
     "1. Bấm Lưu",
     "Số tài khoản: 35241",
     "- Báo lỗi đỏ \"Bắt buộc nhập\" ở CẢ ô Đơn hàng/Hợp đồng và ô Mã vụ việc\n"
     "- Áp dụng tương tự cho tài khoản 3351"),

    ("024", "Nhóm tài khoản phải trả khác bắt buộc chọn Mã vụ việc", "P1",
     "Dòng chi tiết chọn tài khoản 33481, để trống Mã vụ việc",
     "1. Bấm Lưu",
     "Số tài khoản: 33481",
     "- Báo lỗi đỏ \"Bắt buộc nhập\" dưới ô Mã vụ việc"),

    ("025", "Tài khoản phải trả người bán bắt buộc chọn hợp đồng", "P0",
     "Dòng chi tiết chọn một tài khoản con của 331, để trống Đơn hàng/Hợp đồng",
     "1. Bấm Lưu",
     "Số tài khoản: 3311",
     "- Báo lỗi đỏ \"Bắt buộc nhập\" dưới ô Đơn hàng/Hợp đồng\n"
     "- Áp dụng cho mọi tài khoản con của 331"),

    ("026", "Hợp đồng nguyên tắc bắt buộc chọn phiếu yêu cầu xuất hàng", "P0",
     "Phiếu lập TAY (không từ chứng từ nguồn); dòng chi tiết gắn hợp đồng nguyên tắc HD-NT, KHÔNG tích "
     "số dư đầu kỳ, để trống ô Số phiếu yc xuất hàng",
     "1. Bấm Lưu",
     "Hợp đồng: HD-NT",
     "- Báo lỗi đỏ \"Bắt buộc nhập\" dưới ô Số phiếu yc xuất hàng\n"
     "- Ràng buộc này bảo đảm bút toán công nợ luôn gắn được về đúng lần xuất hàng"),

    ("027", "Hợp đồng nguyên tắc có tích số dư đầu kỳ thì không bắt buộc phiếu xuất hàng", "P0",
     "Như trường hợp trên nhưng ĐÃ tích ô Số dư nợ đầu kì",
     "1. Bấm Lưu",
     "Hợp đồng: HD-NT · tích số dư đầu kỳ",
     "- Lưu thành công, không báo lỗi bắt buộc phiếu xuất hàng"),

    ("028", "Phiếu lập từ Yêu cầu điều chỉnh công nợ không bắt buộc phiếu xuất hàng", "P1",
     "Phiếu lập từ YCDC-01, trong đó có dòng gắn hợp đồng nguyên tắc và không có phiếu xuất hàng",
     "1. Bấm Lưu",
     "—",
     "- Lưu thành công, không báo lỗi bắt buộc phiếu xuất hàng\n"
     "- Ràng buộc chỉ áp cho phiếu lập tay"),

    ("029", "Tổng phát sinh nợ khác tổng phát sinh có trong một nhóm", "P0",
     "Nhóm định khoản 1 có 2 dòng: Nợ 1.000.000 và Có 900.000",
     "1. Bấm Lưu",
     "—",
     "- Hệ thống báo \"Tổng số phát sinh nợ và phát sinh có trong một nhóm không bằng nhau\"\n"
     "- Phiếu không được tạo"),

    ("030", "Một nhóm lệch trong khi nhóm khác đã cân", "P0",
     "Nhóm 1 cân đủ 2.000.000 hai bên; nhóm 2 có Nợ 1.000.000 và Có 800.000",
     "1. Bấm Lưu",
     "—",
     "- Vẫn báo lỗi lệch nợ - có và không tạo phiếu\n"
     "- ⚠️ Dòng Tổng cuối bảng có thể vẫn trông cân vì gộp cả hai nhóm — không tin dòng Tổng"),

    ("031", "Nhiều dòng nợ và nhiều dòng có trong cùng một nhóm", "P0",
     "Nhóm 1 có 4 dòng: Nợ 1.000.000 · Nợ 2.000.000 · Có 1.500.000 · Có 1.500.000 (tổng hai bên bằng "
     "nhau)",
     "1. Bấm Lưu",
     "—",
     "- Hệ thống báo \"Có nhiều phát sinh có và phát sinh nợ trong một nhóm định khoản\"\n"
     "- Phiếu không được tạo dù tổng hai bên đã cân"),

    ("032", "Một nợ - nhiều có trong cùng nhóm là hợp lệ", "P0",
     "Nhóm 1 có 3 dòng: Nợ 3.000.000 · Có 1.000.000 · Có 2.000.000",
     "1. Bấm Lưu",
     "—",
     "- Lưu thành công"),

    ("033", "Nhiều nợ - một có trong cùng nhóm là hợp lệ", "P0",
     "Nhóm 1 có 3 dòng: Nợ 1.000.000 · Nợ 2.000.000 · Có 3.000.000",
     "1. Bấm Lưu",
     "—",
     "- Lưu thành công"),

    ("034", "Trùng tài khoản, đối tượng và hợp đồng trong cùng một nhóm", "P0",
     "Nhóm 1 có 2 dòng cùng tài khoản 1311, cùng khách hàng KH-01, cùng hợp đồng HD-01",
     "1. Bấm Lưu",
     "—",
     "- Hệ thống báo \"Nhóm định khoản 1 đang bị trùng số tài khoản, khách hàng và hợp đồng\"\n"
     "- Thông báo nêu đúng số hiệu nhóm bị trùng"),

    ("035", "Trùng tài khoản và đối tượng nhưng khác hợp đồng là hợp lệ", "P0",
     "Nhóm 1 có 2 dòng cùng tài khoản 1311, cùng khách hàng KH-01 nhưng hợp đồng HD-01 và HD-02",
     "1. Bấm Lưu",
     "—",
     "- Lưu thành công, không báo trùng"),

    ("036", "Trùng hoàn toàn nhưng không gắn hợp đồng", "P1",
     "Nhóm 1 có 2 dòng cùng tài khoản, cùng đối tượng, ĐỀU KHÔNG gắn hợp đồng, tổng nợ - có vẫn cân",
     "1. Bấm Lưu",
     "—",
     "- ⚠️ Lưu thành công: quy tắc chống trùng chỉ xét dòng CÓ gắn hợp đồng\n"
     "- Ghi nhận để nghiệp vụ xác nhận có muốn siết thêm không"),

    ("037", "Trùng bộ khóa nhưng khác nhóm định khoản là hợp lệ", "P1",
     "Hai dòng giống hệt nhau về tài khoản, đối tượng và hợp đồng nhưng đặt ở nhóm 1 và nhóm 2, mỗi "
     "nhóm đều cân nợ - có",
     "1. Bấm Lưu",
     "—",
     "- Lưu thành công, quy tắc chống trùng chỉ xét trong từng nhóm"),

    ("038", "Điều chỉnh vượt quá số tiền của Báo có", "P0",
     "Chi tiết Báo có BC-01 số tiền 10.000.000, đã điều chỉnh 8.000.000; dòng chi tiết gắn BC-01 nhập "
     "Phát sinh nợ 3.000.000",
     "1. Bấm Lưu",
     "Phát sinh nợ: 3.000.000",
     "- Hệ thống báo \"Tổng số tiền điều chỉnh vượt quá số tiền của báo có!\"\n"
     "- Phiếu không được tạo"),

    ("039", "Điều chỉnh đúng bằng phần còn lại của Báo có", "P0",
     "Như trên, phần còn lại là 2.000.000; dòng chi tiết nhập Phát sinh nợ đúng 2.000.000",
     "1. Bấm Lưu",
     "Phát sinh nợ: 2.000.000",
     "- Lưu thành công, không báo vượt"),

    ("040", "Phát sinh có vượt quá số dư nợ đầu kỳ của hợp đồng", "P0",
     "Dòng chi tiết gắn hợp đồng nguyên tắc HD-NT có số dư nợ đầu kỳ 1.000.000, đã tích ô Số dư nợ "
     "đầu kì; nhập Phát sinh có 2.000.000",
     "1. Bấm Lưu",
     "Phát sinh có: 2.000.000",
     "- Kết quả mong đợi: cảnh báo \"Số tiền phát sinh có vượt quá số dư nợ đầu kì của hợp đồng\", "
     "không lưu\n"
     "- ⚠️ Hiện trạng dự kiến LỖI: ràng buộc này có trong hệ thống nhưng không thấy chạy lúc lưu. Nếu "
     "lưu được thì ghi Failed"),

    ("041", "Phát sinh nợ vượt quá số dư có đầu kỳ của hợp đồng", "P0",
     "Dòng chi tiết gắn hợp đồng nguyên tắc có số dư CÓ đầu kỳ 1.000.000, đã tích ô số dư đầu kỳ; nhập "
     "Phát sinh nợ 2.000.000",
     "1. Bấm Lưu",
     "Phát sinh nợ: 2.000.000",
     "- Kết quả mong đợi: cảnh báo \"Số tiền phát sinh nợ vượt quá số dư có đầu kì của hợp đồng\"\n"
     "- ⚠️ Cùng nghi vấn như trường hợp trên, nếu lưu được thì ghi Failed"),

    ("042", "Số tiền lẻ thập phân vẫn cân được sau làm tròn", "P1",
     "Nhóm 1: Nợ 1.000,555 · Có 1.000,55 và Có 0,005",
     "1. Bấm Lưu",
     "—",
     "- Hệ thống so tổng nợ - có SAU khi làm tròn 2 chữ số thập phân\n"
     "- Không báo lệch sai, lưu thành công"),

    ("043", "Số tiền cực lớn", "P1",
     "Có dòng chi tiết",
     "1. Nhập Phát sinh nợ là 999.999.999.999.999, cân bên có tương ứng\n"
     "2. Bấm Lưu và duyệt\n"
     "3. Đọc lại số tiền trên danh sách, màn chi tiết và trong Sổ chi tiết các tài khoản",
     "999.999.999.999.999",
     "- Số tiền giữ nguyên ở cả 3 nơi, không bị làm tròn mất chữ số\n"
     "- Hoặc hệ thống chặn với thông báo rõ ràng về giới hạn số tiền"),

    ("044", "Đính kèm tệp dung lượng lớn và định dạng lạ", "P1",
     "Màn Tạo phiếu",
     "1. Chọn một tệp lớn hơn 20 MB, bấm Lưu\n"
     "2. Chọn một tệp chương trình chạy được, bấm Lưu",
     "Tệp 25 MB · tệp chương trình",
     "- Hệ thống báo lỗi rõ ràng về dung lượng hoặc định dạng không cho phép\n"
     "- Trang không treo, dữ liệu đã nhập vẫn còn"),

    ("045", "Nhập nội dung có chứa mã lệnh vào ô Diễn giải", "P0",
     "Màn Tạo phiếu",
     "1. Nhập một đoạn mã lệnh dạng thẻ vào ô Diễn giải\n"
     "2. Lưu phiếu\n"
     "3. Xem cột Diễn giải ngoài danh sách và trong màn chi tiết",
     "Đoạn mã lệnh dạng thẻ",
     "- Nội dung hiển thị nguyên văn dưới dạng chữ\n"
     "- Không có cửa sổ bật lên, không có hành vi lạ nào xảy ra"),
]

SEC_IX = [
    ("001", "Hai người cùng lập phiếu tại một thời điểm", "P0",
     "Hai tài khoản KT-1 và KT-2 cùng công ty, cùng có quyền Kế toán thanh toán",
     "1. Cả hai mở màn Tạo phiếu, nhập dữ liệu hợp lệ\n"
     "2. Đếm 3 giây rồi cùng bấm Lưu\n"
     "3. Đối chiếu mã 2 phiếu vừa tạo",
     "—",
     "- Hai phiếu có mã KHÁC nhau, số thứ tự liền nhau\n"
     "- Không phiếu nào bị lỗi hay bị ghi đè"),

    ("002", "Một người mở màn Sửa trong khi phiếu bị người khác xóa", "P1",
     "Phiếu P Đang tạo do KT-1 lập; KT-1 mở màn Sửa và để đó",
     "1. Người quản trị xóa phiếu P từ phiên khác\n"
     "2. KT-1 bấm Lưu trên màn Sửa đang mở",
     "—",
     "- Hệ thống báo dữ liệu đã thay đổi hoặc không tồn tại\n"
     "- Không tạo ra phiếu mới, không treo trang"),

    ("003", "Mở màn Sửa rồi phiếu bị duyệt ở phiên khác", "P0",
     "Phiếu P Đang tạo; KT-1 mở màn Sửa ở tab 1 và cũng mở màn Sửa ở tab 2",
     "1. Ở tab 2 bấm Lưu và duyệt\n"
     "2. Quay lại tab 1, sửa số tiền rồi bấm Lưu và duyệt",
     "—",
     "- Kết quả mong đợi: tab 1 báo phiếu đã được duyệt, từ chối thao tác\n"
     "- ⚠️ Hiện trạng dự kiến LỖI: phiếu bị duyệt hai lần và bút toán bị ghi trùng vào sổ. Kiểm tra "
     "số dòng bút toán, nếu tăng gấp đôi thì ghi Failed"),

    ("004", "Hai phiếu cùng lập từ một Yêu cầu điều chỉnh công nợ", "P0",
     "Phiếu yêu cầu điều chỉnh công nợ YCDC-01 đã duyệt, chưa có phiếu kế toán nào",
     "1. KT-1 mở màn Tạo phiếu và chọn YCDC-01\n"
     "2. KT-2 cũng mở màn Tạo phiếu và chọn YCDC-01\n"
     "3. KT-1 bấm Lưu, sau đó KT-2 bấm Lưu",
     "—",
     "- KT-1 lưu thành công\n"
     "- KT-2 bị chặn với thông báo phiếu yêu cầu đã được dùng lập phiếu kế toán\n"
     "- Chỉ tồn tại 1 phiếu kế toán gắn với YCDC-01"),

    ("005", "Hai phiếu cùng lập từ một Yêu cầu hạch toán bổ sung", "P0",
     "Phiếu yêu cầu hạch toán bổ sung HTBS-01 chưa có phiếu kế toán",
     "1. Lập và lưu phiếu kế toán thứ nhất từ HTBS-01\n"
     "2. Mở lại màn Tạo phiếu từ HTBS-01 lần nữa, nhập hợp lệ và bấm Lưu",
     "—",
     "- Lần thứ hai bị chặn với thông báo phiếu yêu cầu hạch toán bổ sung này đã có phiếu kế toán\n"
     "- Chỉ tồn tại 1 phiếu kế toán gắn với HTBS-01"),

    ("006", "Điều chỉnh Báo có từ hai phiếu cùng lúc", "P0",
     "Chi tiết Báo có BC-01 còn được điều chỉnh 2.000.000",
     "1. Lập phiếu A điều chỉnh 2.000.000 gắn BC-01, chưa lưu\n"
     "2. Lập phiếu B cũng điều chỉnh 2.000.000 gắn BC-01, bấm Lưu và duyệt\n"
     "3. Quay lại phiếu A, bấm Lưu và duyệt",
     "Mỗi phiếu 2.000.000",
     "- Phiếu B duyệt thành công\n"
     "- Phiếu A bị chặn với thông báo vượt quá số tiền của báo có\n"
     "- Tổng đã điều chỉnh của BC-01 không vượt 10.000.000"),

    ("007", "Đổi phòng ban của người lập sau khi đã tạo phiếu", "P2",
     "KT-1 thuộc phòng PB-1 và đã lập 3 phiếu; sau đó nhân sự chuyển KT-1 sang phòng PB-2",
     "1. Đăng nhập tài khoản có quyền xem tổng công ty\n"
     "2. Tìm lại 3 phiếu cũ, đọc thông tin đơn vị",
     "—",
     "- Ba phiếu cũ vẫn thuộc phòng PB-1 tại thời điểm lập, không bị đổi theo hồ sơ mới\n"
     "- Phiếu lập sau khi chuyển mới thuộc PB-2"),

    ("008", "Xóa danh mục đang được phiếu sử dụng", "P1",
     "Phiếu Q đã duyệt có dòng dùng Mã phí MP-1 và Mã vụ việc VV-1",
     "1. Vào danh mục, khóa hoặc xóa MP-1 và VV-1\n"
     "2. Mở lại màn chi tiết phiếu Q\n"
     "3. Mở lại màn Sửa của một phiếu nháp cũng dùng MP-1",
     "—",
     "- Màn chi tiết phiếu Q vẫn hiển thị đủ Mã phí và Mã vụ việc cũ\n"
     "- Màn Sửa không tự xóa mất giá trị cũ mà không báo gì\n"
     "- Không lỗi hệ thống"),
]

SEC_X = [
    ("001", "Luồng đầy đủ: lập tay, lưu nháp, sửa, duyệt, kiểm tra sổ", "P0",
     "Tài khoản KT-1 có quyền Kế toán thanh toán; khách hàng KH-01 có hợp đồng thường HD-01",
     "1. Tạo phiếu mới, nhập Diễn giải, để Loại tiền VNĐ\n"
     "2. Thêm 2 dòng: Nợ tài khoản 1311 gắn KH-01 và HD-01 số tiền 5.000.000; Có tài khoản 5111 số "
     "tiền 5.000.000; cùng Nhóm định khoản 1\n"
     "3. Bấm Lưu, kiểm tra phiếu ở trạng thái Đang tạo\n"
     "4. Mở Sửa, đổi số tiền cả hai dòng thành 6.000.000, bấm Lưu\n"
     "5. Mở Sửa lần nữa, bấm Lưu và duyệt\n"
     "6. Mở Sổ chi tiết các tài khoản, tra theo tài khoản 1311 và 5111\n"
     "7. In phiếu và Xuất Excel phiếu",
     "5.000.000 rồi 6.000.000",
     "- Bước 3: phiếu Đang tạo, chưa có bút toán nào\n"
     "- Bước 4: Tổng phát sinh ngoài danh sách đổi thành 6.000.000\n"
     "- Bước 5: phiếu Đã duyệt, báo duyệt thành công\n"
     "- Bước 6: đúng 2 bút toán số tiền 6.000.000, đối ứng lẫn nhau, ghi theo Ngày hạch toán\n"
     "- Bước 7: bản in và tệp Excel đều thể hiện 6.000.000\n"
     "- Sau khi duyệt: menu Hành động không còn Sửa và Xóa"),

    ("002", "Luồng từ Yêu cầu điều chỉnh công nợ tới ghi sổ", "P0",
     "Phiếu yêu cầu điều chỉnh công nợ YCDC-01 đã duyệt, 2 dòng chi tiết",
     "1. Mở màn Tạo phiếu kế toán, chọn YCDC-01\n"
     "2. Kiểm tra dữ liệu nạp sẵn và các ô bị khóa\n"
     "3. Bấm Lưu, mở màn YCDC-01 đọc trạng thái\n"
     "4. Mở Sửa phiếu kế toán, bấm Lưu và duyệt\n"
     "5. Mở lại màn YCDC-01 đọc trạng thái và người duyệt\n"
     "6. Mở Sổ chi tiết các tài khoản kiểm tra bút toán",
     "—",
     "- Bước 3: YCDC-01 chuyển sang đã tạo phiếu kế toán\n"
     "- Bước 5: YCDC-01 chuyển Đã duyệt, ghi đúng người duyệt\n"
     "- Bước 6: bút toán khớp từng dòng của phiếu yêu cầu\n"
     "- Cột Mã phiếu YCDC ngoài danh sách bấm được sang YCDC-01"),

    ("003", "Luồng từ Yêu cầu hạch toán bổ sung tới thông báo cho người đề nghị", "P0",
     "Phiếu yêu cầu hạch toán bổ sung HTBS-01 do NV-A lập, có 2 tệp đính kèm",
     "1. KT-1 lập phiếu kế toán từ HTBS-01\n"
     "2. Kiểm tra tệp đính kèm được kế thừa\n"
     "3. Bấm Lưu và duyệt\n"
     "4. Đăng nhập NV-A, mở khu vực thông báo và bấm vào thông báo mới\n"
     "5. Thử lập phiếu kế toán thứ hai từ HTBS-01",
     "—",
     "- Bước 2: 2 tệp của HTBS-01 hiện sẵn trên phiếu kế toán\n"
     "- Bước 3: HTBS-01 chuyển Đã duyệt\n"
     "- Bước 4: NV-A nhận thông báo, bấm vào mở đúng HTBS-01\n"
     "- Bước 5: bị chặn vì HTBS-01 đã có phiếu kế toán"),

    ("004", "Luồng phiếu ngoại tệ từ lập tới đối chiếu số liệu", "P0",
     "Khách hàng nước ngoài KH-USD; loại tiền USD tỷ giá mặc định 25.000",
     "1. Tạo phiếu, đổi Loại tiền sang USD\n"
     "2. Nhập Nợ 100 USD và Có 100 USD ở cùng nhóm, kiểm tra cột VNĐ\n"
     "3. Sửa Tỷ giá thành 26.000, kiểm tra lại cột VNĐ\n"
     "4. Bấm Lưu và duyệt\n"
     "5. Đọc cột Tổng phát sinh ngoài danh sách\n"
     "6. Mở Sổ chi tiết các tài khoản kiểm tra số nguyên tệ, số quy đổi và tỷ giá\n"
     "7. Xuất Excel phiếu",
     "100 USD · tỷ giá 25.000 rồi 26.000",
     "- Bước 2: cột VNĐ hiện 2.500.000\n"
     "- Bước 3: cột VNĐ đổi thành 2.600.000 ở cả hai dòng\n"
     "- Bước 5: Tổng phát sinh hiện 2.600.000, không kèm chữ USD\n"
     "- Bước 6: bút toán lưu cả nguyên tệ 100, quy đổi 2.600.000 và tỷ giá 26.000\n"
     "- Bước 7: tệp Excel có đủ cột nguyên tệ và quy đổi"),

    ("005", "Luồng điều chỉnh số dư lẻ đầu - cuối", "P0",
     "Công ty đặt mức số dư lẻ được điều chỉnh là 10.000; hợp đồng HD-01 của KH-01 sau bút toán sẽ còn "
     "dư nợ 6.000",
     "1. Tạo phiếu có dòng Có tài khoản 1311 gắn KH-01 và HD-01, cân nhóm đầy đủ\n"
     "2. Bấm Lưu và duyệt lần 1\n"
     "3. Tích ô điều chỉnh cho HD-01, kiểm tra 2 dòng mới sinh ra\n"
     "4. Bấm Lưu và duyệt lần 2\n"
     "5. Mở Sổ chi tiết các tài khoản, tra số dư còn lại của HD-01",
     "Số dư lẻ 6.000",
     "- Bước 2: hiện khối điều chỉnh số dư lẻ, phiếu chưa lưu\n"
     "- Bước 3: thêm nhóm định khoản mới với 2 dòng Nợ 811 và Có 1311 số tiền 6.000, diễn giải Điều "
     "chỉnh số dư lẻ\n"
     "- Bước 4: duyệt thành công, không hỏi lại\n"
     "- Bước 5: hợp đồng HD-01 về số dư 0"),

    ("006", "Luồng từ Chi phí vận chuyển nhanh tới ghi sổ", "P0",
     "Bảng Chi phí vận chuyển nhanh có 2 bản ghi chưa hạch toán thuộc 2 khách hàng, số tiền 1.000.000 "
     "và 2.000.000",
     "1. Tích chọn cả 2 bản ghi, lập phiếu kế toán\n"
     "2. Kiểm tra 4 dòng chi tiết và 2 nhóm định khoản\n"
     "3. Chọn hợp đồng cho từng dòng, kiểm tra danh sách hợp đồng được lọc\n"
     "4. Nhập Diễn giải và Mã phí còn thiếu, bấm Lưu và duyệt\n"
     "5. Mở lại bảng Chi phí vận chuyển nhanh\n"
     "6. Mở Sổ chi tiết các tài khoản kiểm tra bút toán",
     "1.000.000 và 2.000.000",
     "- Bước 2: 4 dòng, mỗi bản ghi 1 cặp Nợ 35241 và Có 811, nhóm 1 và nhóm 2\n"
     "- Bước 3: chỉ hiện hợp đồng bán của đúng khách hàng và đúng nhân viên kinh doanh\n"
     "- Bước 5: hai bản ghi chuyển sang đã hạch toán và mở được sang phiếu kế toán\n"
     "- Bước 6: đủ 4 bút toán, tổng phát sinh nợ 3.000.000"),
]
