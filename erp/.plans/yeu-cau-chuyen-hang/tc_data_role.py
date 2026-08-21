# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen — man ERP 'Phieu yeu cau chuyen hang'."""

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Quản lý Phiếu yêu cầu chuyển hàng: chứng từ do người kinh doanh lập để đề nghị kho chuyển hàng "
     "hóa về phục vụ khách hàng của mình.\n"
     "Mỗi phiếu gồm nhiều dòng hàng hóa; mỗi hàng hóa lại chia cho nhiều khách hàng, mỗi khách hàng có "
     "số lượng, ngày cần và ghi chú riêng.\n"
     "Luồng: người lập Lưu nháp hoặc Lưu và Gửi → Kế toán kho mở màn chờ duyệt, chọn \"Tổng hợp\" (gom "
     "yêu cầu vào Phiếu yêu cầu xuất hàng loại Xuất điều chuyển kho chi nhánh) hoặc \"Không duyệt\" "
     "(trả lại, bắt buộc nhập ghi chú).\n"
     "Sau khi được tổng hợp, phiếu đi tiếp theo dây chuyền kho: xuất kho → vận chuyển → nhập kho → "
     "phân bổ. Các bước đó do MÀN KHÁC điều khiển, màn này chỉ hiển thị trạng thái."),

    ("2. Đối tượng được tính / hiển thị",
     "Phiếu có tới 13 trạng thái, nhưng bản thân màn này chỉ tạo ra 2 trạng thái đầu:\n"
     "- Đang tạo (đỏ) — bản nháp, do người lập bấm Lưu.\n"
     "- Chờ duyệt (đỏ) — đã bấm Lưu và Gửi, đang đợi kế toán kho.\n"
     "Các trạng thái còn lại do dây chuyền kho phía sau đặt: Đã tiếp nhận · Đang đề nghị · Đang xuất "
     "kho · Đã xuất kho · Đang vận chuyển · Đang nhập kho · Đang nhập kho · Đã nhập kho · Đã nhập hàng "
     "· Đã phân bổ (tất cả tô XANH) và Đã hủy (đỏ).\n"
     "⚠️ Danh sách trạng thái có HAI mục cùng tên \"Đang nhập kho\" — xem mục 9.\n"
     "Phạm vi phiếu nhìn thấy phụ thuộc chế độ danh sách đang mở:\n"
     "- Chế độ \"Phiếu của tôi\" (đường dẫn không kèm tham số): chỉ phiếu do chính mình lập.\n"
     "- Chế độ \"Tất cả\" (mục menu Phiếu yêu cầu chuyển hàng): lấy theo 4 quyền xem ở mục 7.\n"
     "- Chế độ \"Chờ duyệt\" (mục Phiếu yêu cầu chuyển hàng chờ duyệt): chỉ phiếu trạng thái Chờ duyệt, "
     "do người CÙNG CÔNG TY với người đăng nhập lập; chỉ mở được khi có quyền \"Kế toán kho\".\n"
     "- Chế độ \"Kế toán kho theo dõi\": mọi phiếu của người cùng công ty trừ phiếu nháp. Chế độ này "
     "không có mục menu, chỉ vào bằng đường dẫn.\n"
     "Ở MỌI chế độ, phiếu nháp của NGƯỜI KHÁC luôn bị ẩn."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu nháp (Đang tạo) của NGƯỜI KHÁC bị ẩn ở mọi chế độ, kể cả với người xem toàn tổng công ty.\n"
     "- Hai mục \"Sửa yêu cầu\" và \"Xóa yêu cầu\" chỉ hiện khi phiếu ở trạng thái Đang tạo VÀ người "
     "đăng nhập đúng là người lập.\n"
     "- Mục \"Tổng hợp\" chỉ hiện khi phiếu ở trạng thái Chờ duyệt, người đăng nhập có quyền \"Kế toán "
     "kho\" VÀ cùng công ty với phiếu.\n"
     "- Nút \"Không duyệt\" và khối \"Ghi chú duyệt\" ở màn chi tiết cũng theo đúng điều kiện trên.\n"
     "- Mục \"In yêu cầu\" luôn hiện trong menu hành động của mọi dòng, nhưng bấm vào có mở được hay "
     "không thì tùy quyền xem chi tiết — xem mục 9.\n"
     "- Ô \"Xem tồn\" và cột \"SL tồn\" chỉ có số khi người dùng đã chọn kho ở ô Xem tồn; chưa chọn thì "
     "cột hiện dấu gạch ngang.\n"
     "- Màn hình KHÔNG có chức năng Nhập Excel."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Hai ô \"Từ ngày\" và \"Đến ngày\" lọc theo NGÀY TẠO PHIẾU và tính TRỌN NGÀY ở cả hai đầu: nhập "
     "Đến ngày là 31/08/2026 thì phiếu tạo lúc 23:50 ngày 31/08/2026 VẪN được lấy.\n"
     "⚠️ Đây là điểm màn này làm ĐÚNG, khác ba màn Đề nghị thu tiền, Đề nghị thanh toán và Yêu cầu "
     "điều chỉnh công nợ (ba màn kia làm rụng trọn ngày cuối). Đừng đem kết quả của màn kia suy sang.\n"
     "Không có bộ lọc theo Ngày tiếp nhận, dù cột này có trên lưới.\n"
     "Khoảng thời gian đang lọc được ghi vào tệp Excel danh sách dưới dạng dòng \"Từ ngày ... đến ngày "
     "...\"."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "BA cấp: Phiếu → dòng Hàng hóa → dòng Khách hàng.\n"
     "- Phiếu giữ: Mã yêu cầu, Ngày lập, Người lập, Ghi chú, tệp đính kèm, Trạng thái, Người tiếp nhận, "
     "Ngày tiếp nhận, Ghi chú duyệt.\n"
     "- Mỗi dòng Hàng hóa gắn một hàng hóa và một đơn vị tính, kèm Giá niêm yết và SL tồn (chỉ để tham "
     "khảo, không lưu vào phiếu).\n"
     "- Mỗi dòng Hàng hóa có ÍT NHẤT MỘT dòng Khách hàng: Khách hàng · Số lượng · Ngày cần · Ghi chú.\n"
     "- Số lượng của dòng Hàng hóa = TỔNG số lượng các dòng Khách hàng bên dưới, hệ thống tự cộng.\n"
     "- Mã yêu cầu sinh tự động sau khi lưu, dạng PYCCH- kèm 5 chữ số theo số thứ tự bản ghi, ví dụ "
     "PYCCH-00042. Không sửa tay được.\n"
     "- Công ty / Phòng ban / Bộ phận của phiếu lấy từ hồ sơ nhân sự của người lập lúc tạo phiếu.\n"
     "- Mỗi lần lưu, toàn bộ dòng hàng hóa và dòng khách hàng cũ bị xóa và ghi lại từ đầu."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Dòng \"Tổng cộng\" trong ô Khách hàng của mỗi hàng hóa = tổng Số lượng của các dòng khách hàng "
     "thuộc hàng hóa đó. Số này cập nhật ngay khi gõ.\n"
     "- KHÔNG cho chọn TRÙNG một hàng hóa ở hai dòng trong cùng một phiếu. Giao diện chặn ngay khi "
     "chọn với cảnh báo \"Hàng hóa đã được chọn!\"; nếu lọt qua thì khi lưu hệ thống báo \"Thông tin "
     "không hợp lệ!\".\n"
     "- CÙNG MỘT khách hàng ĐƯỢC phép xuất hiện nhiều lần trong cùng một hàng hóa (ví dụ hai ngày cần "
     "khác nhau) — hệ thống không chặn, không gộp.\n"
     "- Cột \"SL tồn\" là số tồn của kho đang chọn ở ô Xem tồn, KHÔNG cộng dồn nhiều kho và KHÔNG bị "
     "trừ đi số lượng đang yêu cầu.\n"
     "- Ô lọc \"Nhập tên, mã hàng hóa\" quét ĐỒNG THỜI mã hàng và tên hàng của các dòng hàng hóa; một "
     "phiếu khớp nhiều hàng hóa vẫn chỉ hiện một dòng."),

    ("7. Phân quyền cấp",
     "Năm quyền liên quan tới màn hình này:\n"
     "1. \"Xem yêu cầu chuyển hàng theo tổng công ty\" — thấy phiếu của mọi công ty.\n"
     "2. \"Xem yêu cầu chuyển hàng theo công ty\" — chỉ phiếu thuộc công ty mình.\n"
     "3. \"Xem yêu cầu chuyển hàng theo phòng ban\" — phiếu thuộc các phòng ban mình được phân công "
     "quản lý, CỘNG phòng ban của chính mình, CỘNG phiếu do chính mình lập.\n"
     "4. \"Xem yêu cầu chuyển hàng theo bộ phận\" — phiếu thuộc các bộ phận mình được phân công quản "
     "lý, CỘNG bộ phận của chính mình, CỘNG phiếu do chính mình lập.\n"
     "5. \"Kế toán kho\" — vào được màn chờ duyệt, bấm được Tổng hợp và Không duyệt, và xem được chi "
     "tiết mọi phiếu trong công ty mình.\n"
     "Bốn quyền xem xét theo THỨ TỰ TRÊN XUỐNG; ai không có quyền nào trong bốn quyền trên thì chỉ thấy "
     "phiếu do chính mình lập.\n"
     "⚠️ CẢNH BÁO QUAN TRỌNG: quyền MỞ CHI TIẾT hẹp hơn hẳn quyền XEM DANH SÁCH. Chỉ Super admin, "
     "người lập phiếu, và người có quyền \"Kế toán kho\" cùng công ty mới mở được màn chi tiết và bản "
     "in. Người chỉ có 4 quyền xem theo cấp sẽ THẤY dòng trên danh sách nhưng KHÔNG mở được chi tiết — "
     "xem mục 9."),

    ("8. Cách tính các ô thống kê",
     "- Ô \"Hiển thị a đến b trong tổng số N\" dưới bảng: a là dòng đầu trang đang xem, b là dòng cuối, "
     "N là tổng số phiếu khớp bộ lọc trong phạm vi chế độ đang mở.\n"
     "- Ô \"Số dòng mỗi trang\": mặc định 10; đổi số dòng thì bảng quay về trang 1.\n"
     "- Cột STT đánh liên tục theo trang: trang 2 với 10 dòng mỗi trang bắt đầu từ 11.\n"
     "- Cột \"Ngày tạo\" và \"Ngày tiếp nhận\" hiển thị dạng ngày/tháng/năm, không có giờ. \"Ngày tiếp "
     "nhận\" là thời điểm kế toán kho bấm Tổng hợp hoặc bấm Không duyệt.\n"
     "- Trong form, ô \"Giá niêm yết\" lấy theo bảng giá của hàng hóa ứng với đơn vị tính đang chọn; "
     "đổi đơn vị tính thì giá đổi theo.\n"
     "- Ô \"SL tồn\" lấy tồn kho thực tế của kho đang chọn ở ô Xem tồn, tính tại thời điểm chọn.\n"
     "- Tệp Excel danh sách xuất ra 7 cột theo đúng bộ lọc đang áp dụng, kèm dòng ghi khoảng thời gian "
     "đã lọc."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất của màn này — đọc trước khi chạy test:\n"
     "1. ⚠️ LỖI NẶNG NHẤT: người có quyền \"Xem yêu cầu chuyển hàng theo công ty\" (hoặc theo tổng công "
     "ty / phòng ban / bộ phận) NHÌN THẤY dòng trên danh sách nhưng bấm vào Mã yêu cầu thì ra trang báo "
     "không tìm thấy nội dung; bấm In cũng vậy. Chỉ người lập phiếu và người có quyền \"Kế toán kho\" "
     "cùng công ty mới mở được. Ghi nhận Failed.\n"
     "2. ⚠️ Ô lọc Trạng thái có HAI mục cùng tên \"Đang nhập kho\" (hai giá trị khác nhau). Chọn mục "
     "thứ nhất và mục thứ hai cho ra hai tập kết quả KHÁC nhau. Ghi nhận Failed, và khi test lọc trạng "
     "thái phải nói rõ chọn mục thứ mấy.\n"
     "3. ⚠️ \"Không duyệt\" KHÔNG đưa phiếu sang một trạng thái từ chối riêng mà đẩy phiếu VỀ LẠI \"Đang "
     "tạo\". Hệ quả: phiếu biến mất khỏi mọi màn của kế toán kho, chỉ người lập còn thấy; nhưng cột "
     "Người tiếp nhận và Ngày tiếp nhận vẫn đã được điền.\n"
     "4. ⚠️ Sau khi bấm Không duyệt, hệ thống chuyển sang màn \"Kế toán kho theo dõi\" chứ không quay "
     "về màn Chờ duyệt mà người dùng vừa đi ra. Nút Quay lại của màn chi tiết cũng dẫn về màn đó.\n"
     "5. ⚠️ Ngày cần phải LỚN HƠN ngày hôm nay. Chọn đúng ngày hôm nay cũng bị báo không hợp lệ.\n"
     "6. ⚠️ Tệp đính kèm BẮT BUỘC khi tạo mới và chỉ nhận định dạng PDF. Khi SỬA thì không bắt buộc "
     "thêm tệp mới.\n"
     "7. ⚠️ Trạng thái phiếu chỉ đổi sang \"Đã tiếp nhận\" khi kế toán kho LƯU XONG Phiếu yêu cầu xuất "
     "hàng, chứ không phải lúc bấm nút Tổng hợp. Bấm Tổng hợp rồi thoát giữa chừng thì phiếu vẫn ở Chờ "
     "duyệt.\n"
     "8. ⚠️ Không gộp được nhiều yêu cầu chuyển hàng của NHIỀU NGƯỜI KHÁC NHAU vào cùng một Phiếu yêu "
     "cầu xuất hàng: hệ thống báo \"Phiếu yêu cầu chuyển hàng không cùng 1 người yêu cầu. Vui lòng "
     "kiểm tra lại!\".\n"
     "9. ⚠️ Khi hệ thống chặn thao tác Sửa, câu thông báo có thể KHÔNG hiện ra do lỗi đặt tên khóa "
     "thông báo — màn hình im lặng, không lưu và cũng không báo gì. Ghi nhận Failed nếu gặp.\n"
     "10. ⚠️ Cùng một khách hàng được phép lặp lại nhiều lần trong cùng một hàng hóa. Đừng báo lỗi "
     "trùng ở đây; chỉ HÀNG HÓA mới bị cấm trùng.\n"
     "11. Hai đường dẫn cũ \"Kế toán kho theo dõi\" và một màn danh sách sao chép khác vẫn chạy được "
     "nhưng KHÔNG có mục menu nào trỏ tới.\n"
     "12. Bộ lọc được ghi nhớ RIÊNG cho từng chế độ danh sách; test xong nhớ bấm nút làm mới bộ lọc "
     "trước khi sang ca test khác."),
]

# ============================================================ TC PHAN QUYEN
ROLE_TCS = [
    ("00", "Tài khoản không có quyền xem nào chỉ thấy phiếu do chính mình lập", "P0",
     "Tài khoản NV-A không được gán quyền nào trong 4 quyền xem theo cấp và không có quyền Kế toán kho; "
     "NV-A đã lập 9 phiếu; công ty của NV-A có hơn 60 phiếu của nhiều người",
     "1. Đăng nhập bằng NV-A\n"
     "2. Mở menu, bấm mục Phiếu yêu cầu chuyển hàng\n"
     "3. Đọc số tổng dưới bảng\n"
     "4. Lật hết các trang, soát cột Người tạo",
     "Tài khoản: NV-A (không quyền xem theo cấp)",
     "- Vào được màn hình, không bị chặn\n"
     "- Tổng hiện đúng 9\n"
     "- Mọi dòng đều có Người tạo là NV-A\n"
     "- Nút Tạo mới VẪN hiển thị (hành vi lập phiếu không gắn quyền)"),

    ("01", "Quyền xem của tổng công ty thấy phiếu của mọi công ty", "P0",
     "Tài khoản B chỉ có quyền \"Xem yêu cầu chuyển hàng theo tổng công ty\"; hệ thống có phiếu của ít "
     "nhất 3 công ty",
     "1. Đăng nhập bằng B, mở mục Phiếu yêu cầu chuyển hàng\n"
     "2. Bấm nút Bộ lọc, ghi lại các ô lọc theo đơn vị\n"
     "3. Chọn lần lượt từng Công ty rồi bấm nút tìm kiếm",
     "Quyền: Xem yêu cầu chuyển hàng theo tổng công ty",
     "- Khối lọc hiện CẢ ô Công ty và ô Phòng ban\n"
     "- Chọn công ty nào ra phiếu của công ty đó\n"
     "- Bỏ chọn công ty thì thấy phiếu của cả 3 công ty (trừ phiếu nháp của người khác)"),

    ("02", "Quyền xem của công ty chỉ thấy phiếu công ty mình", "P0",
     "Tài khoản C chỉ có quyền \"Xem yêu cầu chuyển hàng theo công ty\", thuộc công ty 3; công ty 3 có "
     "30 phiếu, công ty 1 có 200 phiếu",
     "1. Đăng nhập bằng C, mở mục Phiếu yêu cầu chuyển hàng\n"
     "2. Đọc số tổng\n"
     "3. Soát cột Người tạo của mọi dòng",
     "Quyền: Xem yêu cầu chuyển hàng theo công ty",
     "- Tổng bằng 30 trừ đi số phiếu nháp của người khác trong công ty 3\n"
     "- Không có phiếu nào của công ty 1"),

    ("03", "Quyền xem của phòng ban thấy thêm phòng ban của mình và phiếu của mình", "P0",
     "Tài khoản D chỉ có quyền \"Xem yêu cầu chuyển hàng theo phòng ban\", quản lý phòng P1; D thuộc "
     "phòng P2; phòng P1 có 6 phiếu, phòng P2 có 4 phiếu của người khác, D tự lập 2 phiếu",
     "1. Đăng nhập bằng D, mở mục Phiếu yêu cầu chuyển hàng\n"
     "2. Đọc số tổng\n"
     "3. Soát cột Người tạo và đối chiếu phòng ban của từng người",
     "Quyền: Xem yêu cầu chuyển hàng theo phòng ban",
     "- Thấy phiếu của phòng P1 (được phân công quản lý) CỘNG phiếu của phòng P2 (phòng của chính D) "
     "CỘNG phiếu do chính D lập\n"
     "- ⚠️ Điểm riêng của màn này: phòng ban CỦA CHÍNH MÌNH cũng được tính vào phạm vi, dù không được "
     "phân công quản lý"),

    ("04", "Quyền xem của bộ phận thấy thêm bộ phận của mình và phiếu của mình", "P1",
     "Tài khoản E chỉ có quyền \"Xem yêu cầu chuyển hàng theo bộ phận\", quản lý 1 bộ phận; E thuộc bộ "
     "phận khác",
     "1. Đăng nhập bằng E, mở mục Phiếu yêu cầu chuyển hàng\n"
     "2. Đọc số tổng và soát danh sách",
     "Quyền: Xem yêu cầu chuyển hàng theo bộ phận",
     "- Thấy phiếu của bộ phận được phân công CỘNG bộ phận của chính E CỘNG phiếu do E lập"),

    ("05", "Có nhiều quyền xem cùng lúc thì lấy phạm vi rộng nhất", "P1",
     "Tài khoản F có ĐỒNG THỜI quyền xem theo tổng công ty và quyền xem theo bộ phận",
     "1. Đăng nhập bằng F, mở mục Phiếu yêu cầu chuyển hàng\n"
     "2. Đọc số tổng, so với số của tài khoản B ở TC-ROLE-01",
     "—",
     "- Tổng bằng đúng số của tài khoản chỉ có quyền tổng công ty\n"
     "- Không bị thu hẹp về phạm vi bộ phận"),

    ("06", "Người có quyền xem theo cấp không mở được chi tiết", "P0",
     "Tài khoản C chỉ có quyền \"Xem yêu cầu chuyển hàng theo công ty\", KHÔNG có quyền Kế toán kho; "
     "phiếu X do NV-A cùng công ty lập, trạng thái Chờ duyệt",
     "1. Đăng nhập bằng C, tìm phiếu X trong danh sách\n"
     "2. Bấm vào Mã yêu cầu của phiếu X\n"
     "3. Quay lại, mở menu hành động và bấm In yêu cầu",
     "Phiếu X của NV-A, cùng công ty",
     "- ⚠️ Hiện trạng: dòng phiếu X HIỆN trong danh sách nhưng bấm vào Mã yêu cầu ra trang báo không "
     "tìm thấy nội dung; bấm In cũng ra trang đó. LỖI NẶNG, ghi nhận Failed\n"
     "- Kỳ vọng đúng: đã cho thấy trên danh sách thì phải mở được chi tiết và in được\n"
     "- Lặp lại với tài khoản có quyền tổng công ty, phòng ban, bộ phận — kết quả giống nhau"),

    ("07", "Kế toán kho mở được chi tiết mọi phiếu trong công ty", "P0",
     "Tài khoản KT-1 có quyền \"Kế toán kho\", thuộc công ty 3; phiếu X do NV-A cùng công ty lập, "
     "trạng thái Chờ duyệt; phiếu Y do người công ty 1 lập",
     "1. Đăng nhập bằng KT-1\n"
     "2. Mở chi tiết phiếu X\n"
     "3. Dán thẳng đường dẫn chi tiết phiếu Y",
     "—",
     "- Phiếu X: mở được chi tiết đầy đủ\n"
     "- Phiếu Y (công ty khác): ra trang báo không tìm thấy nội dung"),

    ("08", "Kế toán kho vào được màn chờ duyệt", "P0",
     "Tài khoản KT-1 có quyền Kế toán kho, thuộc công ty 3; công ty 3 có 4 phiếu Chờ duyệt, công ty 1 "
     "có 11 phiếu Chờ duyệt",
     "1. Đăng nhập bằng KT-1\n"
     "2. Mở nhóm menu phê duyệt, bấm mục Phiếu yêu cầu chuyển hàng chờ duyệt\n"
     "3. Đọc số tổng và cột Trạng thái",
     "Quyền: Kế toán kho",
     "- Mục menu HIỂN THỊ\n"
     "- Đúng 4 dòng, tất cả đều ở Chờ duyệt, người tạo thuộc công ty 3\n"
     "- KHÔNG thấy 11 phiếu của công ty 1\n"
     "- Mỗi dòng có thêm mục \"Tổng hợp\" trong menu hành động"),

    ("09", "Không có quyền Kế toán kho thì màn chờ duyệt rơi về phiếu của mình", "P0",
     "Tài khoản NV-A không có quyền Kế toán kho; NV-A đã lập 9 phiếu, trong đó 2 phiếu ở Chờ duyệt; "
     "công ty có nhiều phiếu Chờ duyệt của người khác",
     "1. Đăng nhập bằng NV-A\n"
     "2. Tìm mục Phiếu yêu cầu chuyển hàng chờ duyệt trên menu\n"
     "3. Dán thẳng đường dẫn màn chờ duyệt vào thanh địa chỉ\n"
     "4. Đọc số tổng và cột Người tạo",
     "—",
     "- Mục menu KHÔNG hiển thị\n"
     "- Dán thẳng đường dẫn: màn mở ra nhưng CHỈ hiện phiếu do chính NV-A lập, không lộ phiếu người "
     "khác\n"
     "- ⚠️ Đây là điểm màn này làm ĐÚNG — không rò rỉ dữ liệu như một số màn khác\n"
     "- Menu hành động không có mục Tổng hợp"),

    ("10", "Chế độ Kế toán kho theo dõi chỉ dành cho kế toán kho", "P1",
     "KT-1 có quyền Kế toán kho; NV-A không có",
     "1. KT-1 dán đường dẫn màn Kế toán kho theo dõi, đọc số tổng và cột Trạng thái\n"
     "2. NV-A dán cùng đường dẫn, đọc số tổng và cột Người tạo",
     "—",
     "- KT-1: thấy mọi phiếu của người cùng công ty, TRỪ phiếu nháp; gồm cả phiếu đã tiếp nhận và các "
     "trạng thái sau đó\n"
     "- NV-A: chỉ thấy phiếu do chính mình lập\n"
     "- Không có mục menu nào trỏ tới chế độ này"),

    ("11", "Phiếu nháp của người khác bị ẩn ở mọi chế độ", "P0",
     "Tài khoản B có quyền xem tổng công ty và cả quyền Kế toán kho; NV-A vừa bấm Lưu (nháp) một phiếu",
     "1. Đăng nhập bằng B\n"
     "2. Ở chế độ Tất cả, lọc Trạng thái = Đang tạo, đọc kết quả\n"
     "3. Mở chế độ Kế toán kho theo dõi, lọc lại Trạng thái = Đang tạo\n"
     "4. Mở chế độ Chờ duyệt",
     "—",
     "- Cả 3 chế độ đều KHÔNG hiện phiếu nháp của NV-A\n"
     "- Chỉ hiện phiếu nháp của chính B\n"
     "- ⚠️ Quy tắc cố định, KHÔNG ghi Failed"),

    ("12", "Người lập luôn xem được phiếu của mình dù không có quyền nào", "P0",
     "Tài khoản NV-A không có quyền xem theo cấp và không có quyền Kế toán kho; NV-A đã lập phiếu ở "
     "nhiều trạng thái khác nhau",
     "1. Đăng nhập bằng NV-A, mở màn danh sách\n"
     "2. Mở chi tiết lần lượt vài phiếu ở các trạng thái khác nhau\n"
     "3. Bấm In yêu cầu",
     "—",
     "- Mở được chi tiết mọi phiếu do chính mình lập, ở mọi trạng thái\n"
     "- In được bình thường"),

    ("13", "Bỏ qua giao diện gọi thẳng chức năng Xóa phiếu của người khác", "P0",
     "Tài khoản NV-A; 1 phiếu nháp do NV-B lập (lấy số phiếu từ tài khoản quản trị)",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dán thẳng đường dẫn xóa của phiếu đó\n"
     "3. Kiểm tra phiếu còn hay mất",
     "Phiếu nháp của NV-B",
     "- Hệ thống TỪ CHỐI, hiện thông báo màu vàng \"Không thể xóa!\"\n"
     "- Phiếu VẪN còn nguyên\n"
     "- ⚠️ Đây là điểm màn này làm ĐÚNG, chặt hơn ba màn Đề nghị thu tiền, Đề nghị thanh toán và Yêu "
     "cầu điều chỉnh công nợ"),

    ("14", "Bỏ qua giao diện mở màn Sửa phiếu của người khác", "P0",
     "Tài khoản NV-A; 1 phiếu nháp do NV-B lập và 1 phiếu Chờ duyệt do chính NV-A lập",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dán thẳng đường dẫn màn Sửa của phiếu nháp NV-B\n"
     "3. Dán thẳng đường dẫn màn Sửa của phiếu Chờ duyệt của chính mình",
     "—",
     "- Cả 2 lần đều ra trang báo không tìm thấy nội dung\n"
     "- Không mở được form, không sửa được"),

    ("15", "Bỏ qua giao diện gọi thẳng chức năng lưu phiếu của người khác", "P0",
     "Tài khoản NV-A; 1 phiếu nháp do NV-B lập",
     "1. Đăng nhập bằng NV-A, lấy phiên đăng nhập\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Sửa phiếu đó với nội dung hợp lệ\n"
     "3. Quan sát phản hồi\n"
     "4. Đăng nhập NV-B, mở lại phiếu",
     "—",
     "- Hệ thống KHÔNG lưu, phiếu của NV-B giữ nguyên nội dung\n"
     "- ⚠️ Kiểm kỹ phản hồi: nếu hệ thống trả về mà KHÔNG kèm câu \"Bạn không có quyền sửa yêu cầu "
     "này\" thì ghi nhận Failed — có lỗi đặt tên khóa thông báo, người dùng sẽ không biết vì sao thất "
     "bại (mục 9 ghi chú 9)"),

    ("16", "Bỏ qua giao diện gọi thẳng chức năng Không duyệt", "P0",
     "Tài khoản NV-A không có quyền Kế toán kho; 1 phiếu đang ở Chờ duyệt",
     "1. Đăng nhập bằng NV-A, lấy phiên đăng nhập\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Không duyệt cho phiếu đó kèm ghi chú\n"
     "3. Mở lại phiếu, đọc Trạng thái",
     "—",
     "- Hệ thống TỪ CHỐI với thông báo \"Không có quyền\"\n"
     "- Trạng thái phiếu KHÔNG đổi\n"
     "- ⚠️ Điểm làm đúng của màn này"),

    ("17", "Bỏ qua giao diện lấy dữ liệu phiếu để tổng hợp", "P1",
     "Tài khoản NV-A không có quyền Kế toán kho; 1 phiếu ở Chờ duyệt của người khác",
     "1. Đăng nhập bằng NV-A, lấy phiên đăng nhập\n"
     "2. Gọi thẳng chức năng lấy dữ liệu phiếu để tổng hợp",
     "—",
     "- Hệ thống từ chối với thông báo \"Không thể chọn phiếu này\"\n"
     "- Không trả về dữ liệu hàng hóa và khách hàng của phiếu"),

    ("18", "Xuất Excel danh sách bị giới hạn theo phạm vi quyền", "P0",
     "Tài khoản C chỉ có quyền xem theo công ty (công ty 3)",
     "1. Mở màn danh sách chế độ Tất cả, không đặt bộ lọc\n"
     "2. Bấm nút Xuất excel\n"
     "3. Mở tệp, đếm số dòng và soát cột Người tạo",
     "—",
     "- Số dòng trong tệp bằng đúng số tổng trên màn\n"
     "- Không có phiếu của công ty khác lọt vào tệp\n"
     "- ⚠️ Nếu tệp chứa phiếu ngoài phạm vi quyền thì ghi Failed"),
]
