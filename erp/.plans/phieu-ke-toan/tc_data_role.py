# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Phieu ke toan'."""

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Quản lý Phiếu kế toán: chứng từ do kế toán lập để ghi bút toán vào Sổ chi tiết các tài khoản. "
     "Màn nằm ở menu Kế toán, nhóm Sổ tổng hợp.\n"
     "Phiếu lập được theo 5 cách: lập tay hoàn toàn, hoặc lấy dữ liệu từ một trong bốn chứng từ nguồn "
     "— Phiếu yêu cầu điều chỉnh công nợ · Phiếu yêu cầu hạch toán bổ sung · Phiếu yêu cầu hạch toán "
     "hoa hồng tháng · bảng Chi phí vận chuyển nhanh.\n"
     "⚠️ KHÁC hẳn màn Đề nghị thanh toán: màn này KHÔNG có dây chuyền duyệt nhiều cấp. Chính người "
     "lập bấm \"Lưu và duyệt\" là phiếu được duyệt ngay và bút toán vào sổ ngay lúc đó. Không có "
     "bước gửi duyệt, không có người duyệt riêng, không có chức năng Không duyệt.\n"
     "Người dùng làm được: xem danh sách, lọc, tạo phiếu (Lưu nháp hoặc Lưu và duyệt), đính kèm tài "
     "liệu, sửa, xóa, xem chi tiết, in và xuất Excel."),

    ("2. Đối tượng được tính / hiển thị",
     "Phiếu chỉ có 3 trạng thái: Đang tạo · Đã duyệt · Hủy.\n"
     "Chỉ nhãn \"Đã duyệt\" tô XANH; \"Đang tạo\" và \"Hủy\" đều tô ĐỎ.\n"
     "Màn có 4 chế độ danh sách, cùng một đường dẫn, khác nhau ở phần tham số phía sau:\n"
     "- Chế độ \"Tất cả\": mục menu Phiếu kế toán trỏ thẳng vào đây. Phạm vi lấy theo 2 quyền xem ở "
     "mục 7, và LUÔN ẩn phiếu nháp của người khác.\n"
     "- Chế độ \"Phiếu của tôi\" (đường dẫn không kèm tham số): chỉ phiếu do chính mình lập, gồm cả "
     "phiếu nháp của mình. Không có mục menu nào trỏ tới.\n"
     "- Chế độ \"Cần duyệt\" (tiêu đề Danh sách phiếu kế toán cần duyệt): lọc cứng theo trạng thái Đã "
     "duyệt. Không có mục menu nào trỏ tới.\n"
     "- Chế độ \"Đã duyệt\" (tiêu đề Danh sách phiếu kế toán đã duyệt). Không có mục menu nào trỏ "
     "tới.\n"
     "⚠️ Hai chế độ \"Cần duyệt\" và \"Đã duyệt\" KHÔNG áp phạm vi quyền xem, xem cảnh báo ở mục 9."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu nháp (Đang tạo) của NGƯỜI KHÁC bị ẩn ở chế độ \"Tất cả\".\n"
     "- Nút Sửa và Xóa chỉ hiện khi phiếu ở trạng thái Đang tạo VÀ người đăng nhập đúng là người lập "
     "phiếu. Không có quyền nào mở thêm được hai nút này.\n"
     "- Nút In và Xuất Excel luôn hiện cho mọi dòng, mọi trạng thái.\n"
     "- Nút Tạo mới chỉ có ở chế độ \"Tất cả\" và \"Phiếu của tôi\"; mở được màn Tạo mới thì cần quyền "
     "\"Kế toán thanh toán\".\n"
     "- Nút \"Thêm chi tiết\" và biểu tượng thùng rác xóa dòng bị ẩn khi phiếu được lập từ chứng từ "
     "nguồn — người lập chỉ được sửa số liệu, không được đổi cấu trúc dòng.\n"
     "- Ô \"Loại tiền\" bị khóa khi phiếu lập từ Phiếu yêu cầu điều chỉnh công nợ.\n"
     "- Ô \"Tỷ giá\" bị khóa khi loại tiền là VNĐ.\n"
     "- Cột \"Số phiếu yc xuất hàng\" bị ẩn với phiếu lập từ Phiếu yêu cầu hạch toán bổ sung dạng thứ "
     "bảy; với dạng này ô Số tài khoản cũng bị khóa ở các dòng đã có sẵn tài khoản.\n"
     "- Ô chọn phiếu yêu cầu xuất hàng và ô đánh dấu số dư đầu kỳ CHỈ hiện khi hợp đồng đang chọn là "
     "hợp đồng nguyên tắc / phụ lục nguyên tắc.\n"
     "- ⚠️ Cột \"Mã khế ước\" có trên lưới chi tiết nhưng LUÔN TRỐNG, không có ô nhập.\n"
     "- ⚠️ Giao diện KHÔNG có nút Hủy phiếu, dù trạng thái Hủy vẫn tồn tại trong ô lọc.\n"
     "- Màn hình KHÔNG có chức năng nhập Excel."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Hai ô \"Từ ngày\" và \"Đến ngày\" lọc theo NGÀY LẬP PHIẾU.\n"
     "⚠️ Đầu mút bên phải KHÔNG được tính trọn ngày: hệ thống so với mốc 0 giờ của ngày nhập vào, nên "
     "phiếu lập trong chính ngày điền ở ô \"Đến ngày\" bị loại khỏi kết quả. Đây là bẫy đối chiếu số "
     "liệu, xem mục 9.\n"
     "Cột \"Ngày hạch toán\" có trên lưới nhưng KHÔNG có bộ lọc theo cột này, dù đây mới là ngày ghi "
     "sổ. Muốn soát theo kỳ kế toán phải mở từng phiếu.\n"
     "Ngày hạch toán trên form mặc định là ngày hiện tại và người lập sửa tay được, gồm cả sửa lùi về "
     "kỳ trước hoặc đẩy sang tương lai."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Hai cấp: Phiếu → Dòng chi tiết. Các dòng chi tiết được gom thành từng \"Nhóm định khoản\" do "
     "người lập tự đánh số ở cột cuối bảng; mọi ràng buộc cân đối nợ - có đều xét TRONG TỪNG NHÓM.\n"
     "- Phiếu giữ: Mã phiếu, chứng từ nguồn (nếu có), Ngày hạch toán, Loại tiền, Tỷ giá, Diễn giải, "
     "tệp đính kèm.\n"
     "- Mỗi dòng chi tiết giữ: Số tài khoản, Tên tài khoản (tự hiện), Mã khách - Tên khách, Phát sinh "
     "nợ, Phát sinh có, Diễn giải, Đơn hàng/Hợp đồng, Số phiếu yc xuất hàng, NVKD, Mã phí, Mã vụ "
     "việc, Mã khế ước, Ngân hàng, STK ngân hàng, Nhóm định khoản.\n"
     "- Khi loại tiền là ngoại tệ, hai cột Phát sinh nợ và Phát sinh có mỗi cột tách làm hai: cột "
     "nguyên tệ để nhập và cột VNĐ hệ thống tự quy đổi.\n"
     "- Mã phiếu sinh tự động: mã công ty + \".PKT\" + tháng năm (4 số) + \".\" + 5 chữ số tăng dần, "
     "ví dụ TP.PKT0925.00001. Bộ đếm chạy lại từ đầu mỗi tháng.\n"
     "- Công ty / Phòng ban / Bộ phận của phiếu lấy từ hồ sơ nhân sự của người lập lúc tạo phiếu.\n"
     "- Mỗi lần lưu, toàn bộ dòng chi tiết cũ bị xóa và ghi lại từ đầu."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Cột \"Tổng phát sinh\" ngoài danh sách = tổng cột Phát sinh nợ ĐÃ QUY ĐỔI VNĐ của mọi dòng "
     "chi tiết. ⚠️ Chỉ cộng bên NỢ; phiếu ngoại tệ vẫn hiện số VNĐ, không hiện nguyên tệ và không kèm "
     "tên loại tiền.\n"
     "- Hai ô lọc \"Số tiền từ - đến\" so với chính con số \"Tổng phát sinh\" nói trên.\n"
     "- Mỗi dòng chi tiết chỉ được có Phát sinh nợ HOẶC Phát sinh có: gõ vào ô này thì ô kia tự về 0.\n"
     "- Trong một nhóm định khoản, tổng phát sinh nợ phải BẰNG tổng phát sinh có (so sau khi làm tròn "
     "2 chữ số thập phân).\n"
     "- Trong một nhóm định khoản, KHÔNG được vừa có nhiều dòng nợ vừa có nhiều dòng có. Chỉ chấp "
     "nhận một nợ - nhiều có, hoặc nhiều nợ - một có.\n"
     "- Trong một nhóm định khoản, không cho hai dòng TRÙNG bộ Số tài khoản + đối tượng + hợp đồng. "
     "Ràng buộc này chỉ xét những dòng CÓ gắn hợp đồng; dòng không gắn hợp đồng thì bỏ qua.\n"
     "- Khi duyệt: mỗi dòng chi tiết thành một bút toán trong Sổ chi tiết các tài khoản. Trong mỗi "
     "nhóm, dòng có số tiền LỚN NHẤT là dòng gốc và được ghi đối ứng với tất cả tài khoản còn lại "
     "trong nhóm (mỗi tài khoản một lần, dù xuất hiện nhiều dòng); các dòng còn lại ghi đối ứng ngược "
     "lại với tài khoản của dòng gốc.\n"
     "- Dòng có cả nợ và có bằng 0 thì bị bỏ qua, không sinh bút toán."),

    ("7. Phân quyền cấp",
     "Nhóm quyền XEM (chỉ ảnh hưởng chế độ \"Tất cả\", xét theo thứ tự trên xuống):\n"
     "1. \"Xem tất cả phiếu kế toán của tổng công ty\"\n"
     "2. \"Xem tất cả phiếu kế toán của công ty\"\n"
     "Ai không có quyền nào trong hai quyền trên thì chỉ thấy phiếu do chính mình lập.\n"
     "⚠️ Màn này KHÔNG có quyền xem theo phòng ban và theo bộ phận (khác hẳn màn Đề nghị thanh toán "
     "và màn Yêu cầu điều chỉnh công nợ vốn có đủ 4 cấp).\n"
     "Quyền THAO TÁC:\n"
     "3. \"Kế toán thanh toán\" — bắt buộc để mở màn Tạo mới.\n"
     "4. \"Thủ quỹ duyệt phiếu thu\" — đang được dùng để gác chế độ \"Cần duyệt\" của màn Phiếu kế "
     "toán. ⚠️ Tên quyền không khớp nghiệp vụ phiếu kế toán, cần rà soát lại với nghiệp vụ.\n"
     "Sửa, Xóa và Duyệt KHÔNG gắn quyền riêng: chỉ chính người lập phiếu thao tác được, và chỉ khi "
     "phiếu còn ở trạng thái Đang tạo. Người giữ mọi quyền xem cũng không sửa được phiếu của người "
     "khác.\n"
     "Tài khoản Super Admin xem được mọi phiếu, kể cả phiếu nháp của người khác."),

    ("8. Cách tính các ô thống kê",
     "Màn danh sách KHÔNG có ô thống kê tổng hợp. Chỉ có dòng đếm bản ghi của lưới: \"Hiển thị a-b / "
     "N\" — a là dòng đầu trang, b là dòng cuối trang, N là tổng số phiếu khớp bộ lọc và khớp phạm vi "
     "quyền của chế độ đang mở.\n"
     "Trong form nhập, dòng \"Tổng\" ở cuối bảng chi tiết cộng dồn từng cột tiền của MỌI dòng chi "
     "tiết, không tách theo nhóm định khoản. Khi loại tiền là ngoại tệ, dòng Tổng có 4 ô: tổng nợ "
     "nguyên tệ, tổng nợ VNĐ, tổng có nguyên tệ, tổng có VNĐ.\n"
     "⚠️ Dòng Tổng cộng gộp mọi nhóm nên vẫn có thể cân bằng trong khi từng nhóm lệch. Không dùng "
     "dòng Tổng để kết luận phiếu hợp lệ."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất của màn, đọc trước khi test:\n"
     "1. ⚠️ Hai chế độ \"Cần duyệt\" và \"Đã duyệt\" KHÔNG áp phạm vi quyền xem — người không có quyền "
     "xem nào vẫn đọc được phiếu của mọi công ty qua hai chế độ này. Đây là lỗ hổng cần báo, không "
     "phải thiết kế.\n"
     "2. ⚠️ Quyền \"Kế toán thanh toán\" CHỈ gác cửa vào màn Tạo mới. Chức năng lưu phiếu, sửa, xóa, "
     "in và xuất Excel không kiểm quyền này. Tester kỹ thuật phải test riêng bằng cách gọi thẳng chức "
     "năng, bỏ qua giao diện (xem nhóm TC-ROLE).\n"
     "3. ⚠️ Khối lọc Công ty / Phòng ban hiện hay ẩn theo BỘ QUYỀN CHUNG của lưới (\"Xem tất cả "
     "phiếu\", \"Xem tất cả phiếu của công ty\", \"Xem tất cả phiếu của phòng ban\"), KHÁC bộ quyền "
     "lọc dữ liệu ở mục 7. Hậu quả: có người thấy ô lọc Công ty nhưng chọn công ty khác vẫn ra rỗng, "
     "và ô lọc Phòng ban thì hoàn toàn vô tác dụng vì dữ liệu không lọc theo phòng ban.\n"
     "4. ⚠️ Ô \"Đến ngày\" loại luôn phiếu lập trong chính ngày đó. Đối chiếu số liệu phải cộng thêm "
     "một ngày.\n"
     "5. ⚠️ Cột \"Tổng phát sinh\" chỉ cộng bên NỢ và luôn quy về VNĐ. Phiếu ngoại tệ nhìn trên danh "
     "sách sẽ khác số nguyên tệ trong phiếu.\n"
     "6. ⚠️ Ngày hạch toán bắt buộc trên nhãn (có dấu sao đỏ) nhưng hệ thống KHÔNG chặn khi để trống: "
     "để trống thì tự lấy ngày hiện tại. Ngược lại nếu gõ tay sai định dạng ngày/tháng/năm thì trang "
     "có thể lỗi trắng — cần thử.\n"
     "7. ⚠️ Ràng buộc \"số tiền không vượt quá số dư đầu kỳ của hợp đồng\" đã được viết trong hệ thống "
     "nhưng không thấy chạy lúc lưu. Test kỹ hai trường hợp ở nhóm Ràng buộc nhập liệu, nếu lưu được "
     "thì ghi Failed.\n"
     "8. ⚠️ Phiếu đã duyệt không có nút Sửa nhưng chức năng cập nhật không chặn phiếu đã duyệt. Nếu "
     "gọi thẳng chức năng cập nhật với phiếu đã duyệt thì có nguy cơ ghi TRÙNG bút toán vào sổ.\n"
     "9. Mọi số tiền nhập được có dấu phân cách nghìn và tối đa 2 chữ số thập phân; hệ thống tự làm "
     "tròn 2 số.\n"
     "10. Nhóm TC-ROLE có phần dành cho tester kỹ thuật: dùng công cụ kiểm thử để gọi thẳng chức năng, "
     "bỏ qua giao diện. Tester nghiệp vụ bỏ qua các dòng này."),
]

ROLE_TCS = [
    ("00", "Tài khoản không có quyền xem nào chỉ thấy phiếu do chính mình lập", "P0",
     "Tài khoản NV-A không được gán quyền xem nào của màn Phiếu kế toán; NV-A đã lập 7 phiếu; công ty "
     "của NV-A có hơn 60 phiếu của nhiều người",
     "1. Đăng nhập bằng NV-A\n"
     "2. Mở menu Kế toán, nhóm Sổ tổng hợp, bấm mục Phiếu kế toán\n"
     "3. Đọc dòng đếm bản ghi dưới bảng\n"
     "4. Lật hết các trang, soát cột Người lập",
     "Tài khoản: NV-A (không quyền xem)",
     "- Vào được màn hình, không bị chặn\n"
     "- Dòng đếm hiện đúng 7\n"
     "- Mọi dòng đều có Người lập là NV-A\n"
     "- ⚠️ Nút Tạo mới VẪN hiển thị dù NV-A chưa chắc bấm vào được, xem TC-ROLE-03"),

    ("01", "Quyền xem của tổng công ty thấy phiếu của mọi công ty", "P0",
     "Tài khoản B chỉ có quyền \"Xem tất cả phiếu kế toán của tổng công ty\"; hệ thống có phiếu đã "
     "duyệt của ít nhất 3 công ty",
     "1. Đăng nhập bằng B, mở mục Phiếu kế toán trên menu\n"
     "2. Đọc dòng đếm bản ghi\n"
     "3. Soát cột Phòng ban, đối chiếu với danh sách công ty",
     "Quyền: Xem tất cả phiếu kế toán của tổng công ty",
     "- Thấy phiếu của cả 3 công ty\n"
     "- Không có phiếu nháp nào của người khác lọt vào danh sách\n"
     "- Phiếu nháp của chính B vẫn hiện"),

    ("02", "Quyền xem của công ty chỉ thấy phiếu công ty mình", "P0",
     "Tài khoản C chỉ có quyền \"Xem tất cả phiếu kế toán của công ty\", thuộc công ty 3; công ty 3 có "
     "40 phiếu (trong đó 5 phiếu nháp của người khác), công ty 1 có hơn 200 phiếu",
     "1. Đăng nhập bằng C, mở mục Phiếu kế toán\n"
     "2. Đọc dòng đếm bản ghi\n"
     "3. Soát toàn bộ danh sách",
     "Quyền: Xem tất cả phiếu kế toán của công ty",
     "- Dòng đếm bằng 35 (40 trừ 5 phiếu nháp của người khác)\n"
     "- Không có phiếu nào của công ty 1\n"
     "- Phiếu nháp của chính C vẫn hiện thêm ngoài 35 phiếu trên"),

    ("03", "Không có quyền Kế toán thanh toán thì không mở được màn Tạo mới", "P0",
     "Tài khoản NV-A không có quyền \"Kế toán thanh toán\"",
     "1. Đăng nhập bằng NV-A, mở mục Phiếu kế toán\n"
     "2. Bấm nút Tạo mới\n"
     "3. Quan sát màn hình",
     "Tài khoản: NV-A (không có quyền Kế toán thanh toán)",
     "- Hệ thống từ chối, báo không có quyền, không mở được form nhập phiếu\n"
     "- ⚠️ Nút Tạo mới vẫn hiện trên danh sách dù bấm vào bị chặn — đây là điểm khó chịu về trải "
     "nghiệm, ghi nhận lại nhưng không ghi Failed"),

    ("04", "Có quyền Kế toán thanh toán thì mở được màn Tạo mới", "P0",
     "Tài khoản KT-1 có quyền \"Kế toán thanh toán\"",
     "1. Đăng nhập bằng KT-1, mở mục Phiếu kế toán\n"
     "2. Bấm nút Tạo mới",
     "Quyền: Kế toán thanh toán",
     "- Mở đúng màn Tạo phiếu kế toán\n"
     "- Có đủ 3 nút cuối trang: Lưu · Lưu và duyệt · Quay lại"),

    ("05", "Chế độ Cần duyệt bị chặn với tài khoản thiếu quyền", "P1",
     "Tài khoản NV-A không có quyền \"Thủ quỹ duyệt phiếu thu\"",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dán đường dẫn màn Danh sách phiếu kế toán cần duyệt vào thanh địa chỉ",
     "Tài khoản: NV-A",
     "- Hệ thống từ chối, báo không có quyền\n"
     "- ⚠️ Quyền đang gác chế độ này tên là \"Thủ quỹ duyệt phiếu thu\" — không liên quan nghiệp vụ "
     "phiếu kế toán. Ghi nhận để nghiệp vụ rà soát, không ghi Failed"),

    ("06", "Chế độ Cần duyệt và Đã duyệt để lộ phiếu ngoài phạm vi quyền", "P0",
     "Tài khoản C chỉ có quyền \"Xem tất cả phiếu kế toán của công ty\" (công ty 3) và có quyền \"Thủ "
     "quỹ duyệt phiếu thu\"; công ty 1 có nhiều phiếu đã duyệt",
     "1. Đăng nhập bằng C, mở mục Phiếu kế toán, ghi lại dòng đếm bản ghi\n"
     "2. Dán đường dẫn màn Danh sách phiếu kế toán cần duyệt, đọc dòng đếm\n"
     "3. Dán đường dẫn màn Danh sách phiếu kế toán đã duyệt, đọc dòng đếm\n"
     "4. Ở cả hai chế độ, soát cột Phòng ban tìm phiếu của công ty 1",
     "Tài khoản: C (chỉ quyền xem theo công ty)",
     "- ⚠️ LỖI CẦN BÁO: hai chế độ Cần duyệt và Đã duyệt hiện phiếu của MỌI công ty, gồm cả công ty 1 "
     "mà C không có quyền xem\n"
     "- Số bản ghi ở hai chế độ này lớn hơn hẳn số ở chế độ Tất cả\n"
     "- Kết quả mong đợi đúng: hai chế độ này phải bó theo cùng phạm vi quyền như chế độ Tất cả"),

    ("07", "Khối lọc theo đơn vị dùng bộ quyền khác bộ quyền lọc dữ liệu", "P1",
     "Tài khoản C chỉ có quyền \"Xem tất cả phiếu kế toán của công ty\" (công ty 3) và có thêm quyền "
     "chung \"Xem tất cả phiếu\" của lưới danh sách",
     "1. Đăng nhập bằng C, mở mục Phiếu kế toán\n"
     "2. Bấm nút Bộ lọc, quan sát các ô lọc theo đơn vị\n"
     "3. Chọn một công ty KHÁC công ty 3 rồi bấm nút tìm kiếm\n"
     "4. Chọn một Phòng ban bất kỳ rồi bấm nút tìm kiếm",
     "Chọn Công ty: công ty 1",
     "- Khối lọc CÓ hiện ô Công ty và ô Phòng ban\n"
     "- ⚠️ Chọn công ty 1 ra danh sách RỖNG dù ô lọc cho chọn — vì phạm vi dữ liệu vẫn bó ở công ty 3\n"
     "- ⚠️ Ô lọc Phòng ban không làm thay đổi kết quả (màn không lọc theo phòng ban)\n"
     "- Ghi nhận cả hai điểm để nghiệp vụ quyết định ẩn ô lọc hay mở quyền"),

    ("08", "Super Admin xem được mọi phiếu kể cả phiếu nháp của người khác", "P1",
     "Tài khoản quản trị cao nhất; NV-A có 2 phiếu nháp",
     "1. Đăng nhập bằng tài khoản quản trị\n"
     "2. Mở chi tiết một phiếu nháp của NV-A bằng đường dẫn trực tiếp",
     "—",
     "- Mở được màn chi tiết đầy đủ\n"
     "- ⚠️ Vẫn KHÔNG có nút Sửa và Xóa (hai nút này chỉ dành cho người lập)"),

    ("09", "Người có mọi quyền xem vẫn không sửa được phiếu của người khác", "P0",
     "Tài khoản B có quyền \"Xem tất cả phiếu kế toán của tổng công ty\"; NV-A có 1 phiếu ở trạng thái "
     "Đang tạo",
     "1. Đăng nhập bằng B\n"
     "2. Mở chế độ Tất cả, tìm phiếu nháp của NV-A\n"
     "3. Dán đường dẫn màn sửa của phiếu đó vào thanh địa chỉ",
     "—",
     "- Phiếu nháp của NV-A không xuất hiện trong danh sách của B\n"
     "- Mở đường dẫn màn sửa: hệ thống báo dữ liệu không tồn tại, không cho sửa"),

    ("10", "Tester kỹ thuật: gọi thẳng chức năng Lưu phiếu khi thiếu quyền Kế toán thanh toán", "P0",
     "Tài khoản NV-A KHÔNG có quyền \"Kế toán thanh toán\"; đã có sẵn một bộ dữ liệu phiếu hợp lệ",
     "1. Đăng nhập bằng NV-A trên trình duyệt\n"
     "2. Dùng công cụ kiểm thử gọi thẳng chức năng Lưu phiếu kế toán, bỏ qua giao diện\n"
     "3. Quay lại danh sách chế độ Phiếu của tôi, kiểm tra có phiếu mới không",
     "Bộ dữ liệu phiếu hợp lệ",
     "- Kết quả mong đợi: hệ thống từ chối, báo không có quyền\n"
     "- ⚠️ Hiện trạng dự kiến LỖI: phiếu vẫn được tạo, vì quyền chỉ gác cửa vào màn Tạo mới chứ không "
     "gác chức năng lưu. Nếu tạo được thì ghi Failed"),

    ("11", "Tester kỹ thuật: gọi thẳng chức năng Sửa phiếu của người khác", "P0",
     "Tài khoản NV-B; phiếu P ở trạng thái Đang tạo do NV-A lập",
     "1. Đăng nhập bằng NV-B\n"
     "2. Dùng công cụ kiểm thử gọi thẳng chức năng cập nhật phiếu P, bỏ qua giao diện\n"
     "3. Đăng nhập lại bằng NV-A, mở phiếu P",
     "Sửa Diễn giải phiếu P",
     "- Kết quả mong đợi: hệ thống từ chối, phiếu P giữ nguyên nội dung cũ\n"
     "- ⚠️ Hiện trạng dự kiến LỖI: chức năng cập nhật không kiểm người lập. Nếu nội dung phiếu P bị "
     "đổi thì ghi Failed"),

    ("12", "Tester kỹ thuật: gọi thẳng chức năng cập nhật với phiếu ĐÃ DUYỆT", "P0",
     "Phiếu Q đã duyệt, đã sinh bút toán trong Sổ chi tiết các tài khoản; ghi lại số dòng bút toán của "
     "phiếu Q trước khi test",
     "1. Đăng nhập bằng chính người lập phiếu Q\n"
     "2. Dùng công cụ kiểm thử gọi thẳng chức năng cập nhật phiếu Q với trạng thái Đã duyệt\n"
     "3. Mở Sổ chi tiết các tài khoản, đếm lại số dòng bút toán của phiếu Q",
     "Trạng thái gửi lên: Đã duyệt",
     "- Kết quả mong đợi: hệ thống từ chối vì phiếu đã duyệt\n"
     "- ⚠️ Hiện trạng dự kiến LỖI NẶNG: số dòng bút toán của phiếu Q TĂNG GẤP ĐÔI, sổ kế toán sai số "
     "liệu. Nếu tăng thì ghi Failed và báo ngay"),

    ("13", "Tester kỹ thuật: gọi thẳng chức năng In và Xuất Excel phiếu ngoài quyền xem", "P1",
     "Tài khoản C chỉ có quyền xem theo công ty 3; phiếu R thuộc công ty 1",
     "1. Đăng nhập bằng C\n"
     "2. Mở chi tiết phiếu R bằng đường dẫn trực tiếp, ghi nhận kết quả\n"
     "3. Mở chức năng In của phiếu R bằng đường dẫn trực tiếp\n"
     "4. Mở chức năng Xuất Excel của phiếu R bằng đường dẫn trực tiếp",
     "—",
     "- Bước 2: hệ thống báo dữ liệu không tồn tại (đúng)\n"
     "- ⚠️ Bước 3 và 4 dự kiến LỖI: vẫn in và tải được nội dung phiếu R, vì hai chức năng này không "
     "kiểm quyền xem. Nếu tải được thì ghi Failed"),
]
