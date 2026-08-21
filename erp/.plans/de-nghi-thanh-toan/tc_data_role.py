# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Phieu de nghi thanh toan'."""

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Quản lý Phiếu đề nghị thanh toán: chứng từ do bộ phận kinh doanh lập để đề nghị chi tiền, "
     "thuộc nhóm Công nợ - Thu - Chi.\n"
     "Phiếu đi qua DÂY CHUYỀN DUYỆT NHIỀU CẤP: người lập gửi duyệt → Trưởng phòng → Kế toán công nợ "
     "→ Kế toán trưởng → (tùy chọn) Ban giám đốc → Kế toán thanh toán lập Phiếu chi hoặc Phiếu ủy "
     "nhiệm chi.\n"
     "Ở mỗi cấp, người duyệt được SỬA LẠI SỐ TIỀN của từng dòng và ghi chú duyệt riêng của cấp mình; "
     "hoặc bấm Không duyệt kèm lý do.\n"
     "Người dùng làm được: xem danh sách, lọc, tạo phiếu (Lưu nháp hoặc Lưu và gửi duyệt), đính kèm "
     "tài liệu, sửa, xóa, xem chi tiết, in và xuất Excel."),

    ("2. Đối tượng được tính / hiển thị",
     "Phiếu hiển thị đủ 10 trạng thái: Đang tạo · Chờ TP duyệt · Chờ kế toán công nợ duyệt · Chờ kế "
     "toán trưởng duyệt · Chờ ban giám đốc duyệt · Chờ tạo phiếu chi · Chờ duyệt phiếu chi · Duyệt "
     "phiếu chi · Đã hủy · Không duyệt.\n"
     "Chỉ nhãn \"Duyệt phiếu chi\" tô XANH, chín nhãn còn lại tô ĐỎ.\n"
     "Phạm vi phiếu nhìn thấy phụ thuộc chế độ danh sách đang mở:\n"
     "- Chế độ \"Phiếu của tôi\" (đường dẫn không kèm tham số): chỉ phiếu do chính mình lập, gồm cả "
     "phiếu nháp của mình.\n"
     "- Chế độ \"Tất cả\" (mục menu Đề nghị thanh toán trỏ vào đây): lấy theo 4 quyền xem ở mục 7, và "
     "luôn ẩn phiếu nháp của người khác.\n"
     "- Chế độ \"Chờ duyệt\": phiếu thuộc CÔNG TY của người đăng nhập và đang ở đúng bước mà người đó "
     "có quyền xử lý (xem mục 7). Một người giữ nhiều quyền duyệt sẽ thấy gộp nhiều bước.\n"
     "- Chế độ \"Đã xử lý\": phiếu mà chính người đăng nhập đã duyệt ở bất kỳ cấp nào. Chế độ này "
     "KHÔNG có mục menu nào trỏ tới, chỉ vào được bằng đường dẫn trực tiếp.\n"
     "Loại chi hiển thị trong danh sách gồm cả những loại không lập mới được (xem mục 3)."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu nháp (Đang tạo) của NGƯỜI KHÁC bị ẩn ở chế độ \"Tất cả\".\n"
     "- Nút Sửa và Xóa chỉ hiện khi phiếu ở trạng thái Đang tạo hoặc Không duyệt VÀ người đăng nhập "
     "đúng là người lập phiếu.\n"
     "- Nút \"Tạo phiếu chi\" / \"Tạo phiếu ủy nhiệm chi\" chỉ hiện khi phiếu ở \"Chờ tạo phiếu chi\" "
     "và người đăng nhập có quyền \"Kế toán thanh toán\". Hình thức thanh toán TM ra nút Tạo phiếu "
     "chi, CK ra nút Tạo phiếu ủy nhiệm chi.\n"
     "- Nút duyệt của mỗi cấp chỉ hiện đúng cho người có quyền cấp đó VÀ khi phiếu đang đứng ở bước "
     "của cấp đó.\n"
     "- Nút In và Xuất Excel luôn hiện cho mọi dòng, mọi trạng thái.\n"
     "- Nút Tạo mới chỉ có ở chế độ \"Phiếu của tôi\" và \"Tất cả\".\n"
     "- ⚠️ Ô \"Loại chi\" LỆCH NHAU giữa 3 màn: màn nhập chỉ cho chọn 4 loại (Chi trả nhà cung cấp · "
     "Chi trả lại khách hàng · Chi thưởng thực hiện hợp đồng · Thanh toán chi phí vận chuyển NCC); ô "
     "lọc của màn danh sách có 6 loại (thêm Chi thưởng NVKD và Chi khác); ô lọc của màn Chờ duyệt có "
     "đủ 7 loại (thêm Chi thu nhập cho nhân viên).\n"
     "- Ô chọn \"Kiểu hợp đồng\" (Có hợp đồng / Không có hợp đồng) của loại Chi trả nhà cung cấp đã bị "
     "ẩn khỏi giao diện: mọi phiếu lập mới luôn là CÓ hợp đồng.\n"
     "- Ba ô lọc Công ty / Phòng ban / Bộ phận chỉ hiện ở chế độ \"Tất cả\" và chỉ với người có quyền "
     "xem theo cấp tương ứng. Riêng chế độ \"Chờ duyệt\" có ô lọc Phòng ban riêng, luôn hiện.\n"
     "- Màn hình KHÔNG có chức năng Nhập Excel."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Hai ô \"Từ ngày\" và \"Đến ngày\" lọc theo NGÀY LẬP PHIẾU.\n"
     "⚠️ Hai đầu mút KHÔNG được tính trọn ngày: hệ thống so với mốc 0 giờ của ngày nhập vào, nên phiếu "
     "lập trong chính ngày điền ở ô \"Đến ngày\" bị loại khỏi kết quả. Đây là bẫy đối chiếu số liệu, "
     "xem mục 9.\n"
     "Không có bộ lọc theo cột \"Ngày nhận\" (ngày trưởng phòng duyệt), dù cột này có trên lưới.\n"
     "Riêng loại chi \"Thanh toán chi phí vận chuyển NCC\" có thêm ô \"Đến ngày\" NẰM TRONG FORM (không "
     "phải bộ lọc): đó là mốc thời gian để hệ thống lấy các chuyến xe phát sinh tới ngày đó."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Hai cấp: Phiếu → Dòng chi tiết. Riêng loại Chi trả lại khách hàng và Chi thưởng NVKD có thêm cấp "
     "thứ ba: mỗi dòng chi tiết phân bổ tiếp theo phiếu yêu cầu xuất hàng.\n"
     "- Phiếu giữ: Mã phiếu, Loại chi, Hình thức thanh toán (TM / CK), Loại tiền, Tỷ giá, Lý do chi, "
     "thông tin đối tượng nhận tiền và tài khoản ngân hàng, tệp đính kèm, 4 ô ghi chú duyệt của 4 cấp "
     "và ô Ghi chú không duyệt.\n"
     "- Mỗi dòng chi tiết gắn một đối tượng (khách hàng / nhà cung cấp / nhân viên) và thường gắn một "
     "hợp đồng, kèm 5 cột tiền: Số tiền đề nghị chi · TP duyệt · KT công nợ duyệt · KT trưởng/BGĐ · Số "
     "tiền chi.\n"
     "- Mã phiếu sinh tự động: mã công ty + \".DNTT\" + tháng năm (4 số) + \".\" + 5 chữ số tăng dần.\n"
     "- ⚠️ Tiền tố mã TRÙNG với màn Phiếu đề nghị thu tiền nhưng đếm số riêng, nên hai màn có thể tồn "
     "tại hai phiếu khác nhau MANG CÙNG MỘT MÃ. Khi trao đổi phải nói rõ là phiếu thu hay phiếu chi.\n"
     "- Công ty / Phòng ban / Bộ phận của phiếu lấy từ hồ sơ nhân sự của người lập lúc tạo phiếu.\n"
     "- Mỗi lần lưu, toàn bộ dòng chi tiết cũ bị xóa và ghi lại từ đầu."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Cột \"Số tiền\" ngoài danh sách ĐỔI NGUỒN theo trạng thái phiếu:\n"
     "  · Đang tạo, Chờ TP duyệt, Đã hủy, Không duyệt → tổng cột \"Số tiền đề nghị chi\".\n"
     "  · Chờ kế toán công nợ duyệt → tổng cột \"TP duyệt\".\n"
     "  · Chờ kế toán trưởng duyệt, Chờ ban giám đốc duyệt → tổng cột \"KT công nợ duyệt\".\n"
     "  · Chờ tạo phiếu chi, Chờ duyệt phiếu chi, Duyệt phiếu chi → tổng cột \"KT trưởng/BGĐ\".\n"
     "  Số hiển thị có 2 chữ số thập phân và kèm TÊN LOẠI TIỀN của phiếu (ví dụ 15.000.000,00 VND).\n"
     "- ⚠️ Vì cột này đổi nguồn, cùng một phiếu sẽ hiện SỐ KHÁC NHAU trước và sau mỗi lần duyệt nếu "
     "người duyệt sửa số tiền. Không phải lỗi.\n"
     "- Hai ô lọc \"Số tiền đề nghị thanh toán từ - đến\" luôn so với tổng cột \"Số tiền đề nghị chi\" "
     "đã quy đổi VND, KHÔNG đổi theo trạng thái như cột hiển thị.\n"
     "- Trong form, dòng Tổng cộng cộng dồn từng cột tiền của mọi dòng chi tiết.\n"
     "- Không cho chọn TRÙNG một hợp đồng ở hai dòng trong cùng một phiếu; riêng loại Chi thưởng NVKD "
     "thì được trùng hợp đồng nếu khác Mã vụ việc.\n"
     "- Ô lọc Khách hàng và Nhà cung cấp quét CẢ đối tượng ghi ở đầu phiếu LẪN đối tượng ghi ở từng "
     "dòng chi tiết; một phiếu khớp cả hai vẫn chỉ hiện một dòng."),

    ("7. Phân quyền cấp",
     "Nhóm quyền XEM (4 quyền, chỉ ảnh hưởng chế độ \"Tất cả\", xét theo thứ tự trên xuống):\n"
     "1. \"Xem tất cả phiếu đề nghị thanh toán của tổng công ty\"\n"
     "2. \"Xem tất cả phiếu đề nghị thanh toán của công ty\"\n"
     "3. \"Xem tất cả phiếu đề nghị thanh toán của phòng ban\"\n"
     "4. \"Xem tất cả phiếu đề nghị thanh toán của bộ phận\"\n"
     "Ai không có quyền nào trong bốn quyền trên thì chỉ thấy phiếu do chính mình lập.\n"
     "Nhóm quyền DUYỆT (mỗi quyền mở đúng một bước):\n"
     "5. \"Trưởng phòng duyệt đề nghị thanh toán\" — xử lý phiếu ở bước Chờ TP duyệt, và CHỈ phiếu "
     "thuộc phòng ban mình được phân công quản lý.\n"
     "6. \"Kế toán công nợ duyệt đề nghị thanh toán\" — bước Chờ kế toán công nợ duyệt (toàn công ty).\n"
     "7. \"Kế toán trưởng duyệt đề nghi thanh toán\" — bước Chờ kế toán trưởng duyệt (toàn công ty).\n"
     "8. \"Ban giám đốc duyệt đề nghi thanh toán\" — bước Chờ ban giám đốc duyệt (toàn công ty).\n"
     "9. \"Kế toán thanh toán\" — bước Chờ tạo phiếu chi (toàn công ty).\n"
     "10. \"Kinh doanh đề nghị thanh toán\" — chỉ dùng để nhận thông báo khi phiếu bị từ chối.\n"
     "⚠️ QA LƯU Ý KHI GÁN QUYỀN: tên hai quyền số 7 và số 8 trong hệ thống viết là \"đề nghi thanh "
     "toán\" (thiếu dấu), không phải \"đề nghị thanh toán\". Phải chọn đúng tên đang có, gán nhầm sang "
     "tên đúng chính tả thì người dùng sẽ không duyệt được.\n"
     "Tài khoản có vai trò Super Admin luôn mở được chi tiết mọi phiếu.\n"
     "⚠️ Các chức năng tạo / sửa / xóa / in / xuất Excel / đổi trạng thái KHÔNG được hệ thống chặn "
     "bằng quyền, chỉ ẩn hiện nút trên giao diện. Nhóm test bỏ qua giao diện dựng riêng để đo rủi ro "
     "này (xem các ca TC-ROLE cuối và mục IX)."),

    ("8. Cách tính các ô thống kê",
     "- Ô \"Hiển thị a đến b trong tổng số N\" dưới bảng: a là dòng đầu trang đang xem, b là dòng cuối, "
     "N là tổng số phiếu khớp bộ lọc trong phạm vi chế độ đang mở.\n"
     "- Ô \"Số dòng mỗi trang\": mặc định 10; đổi số dòng thì bảng quay về trang 1.\n"
     "- Cột STT đánh liên tục theo trang: trang 2 với 10 dòng mỗi trang bắt đầu từ 11.\n"
     "- Cột \"Số tiền\": xem công thức đổi nguồn ở mục 6.\n"
     "- Cột \"Ngày lập\" và \"Ngày nhận\" hiển thị dạng ngày/tháng/năm, không có giờ. \"Ngày nhận\" là "
     "thời điểm Trưởng phòng bấm duyệt; phiếu chưa qua bước đó thì ô này để trống.\n"
     "- Cột \"Số tiền còn nợ\" trong form (tên đổi theo loại chi: Số tiền còn nợ / Công nợ còn lại / Số "
     "dư còn nợ / Số tiền còn lại) lấy từ sổ kế toán của hợp đồng, TÍNH LẠI mỗi lần mở phiếu và mỗi "
     "lần in, KHÔNG lưu trong phiếu.\n"
     "- Với loại Thanh toán chi phí vận chuyển NCC, cột \"Đã thanh toán\" là số đã chi cho phiếu hạch "
     "toán chuyến xe đó; \"Số tiền còn lại\" = Tổng cước − Đã thanh toán, và hệ thống chỉ lấy về những "
     "chuyến còn lại lớn hơn 0.\n"
     "- Cột quy đổi VND của mỗi dòng = Số tiền của cột đó × Tỷ giá; chỉ hiện khi loại tiền khác VND."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất của màn này — đọc trước khi chạy test:\n"
     "1. ⚠️ Cột \"Số tiền\" ngoài danh sách ĐỔI NGUỒN theo trạng thái (mục 6). Đối chiếu số liệu phải "
     "xem phiếu đang ở bước nào, đừng so thẳng với số người lập nhập ban đầu.\n"
     "2. ⚠️ Ô nhập \"Số tiền đề nghị chi\" bị TỰ ĐỘNG KÉO XUỐNG bằng số còn nợ nếu nhập vượt — nhưng "
     "chỉ với loại Chi trả lại khách hàng và Thanh toán chi phí vận chuyển NCC. Bốn loại còn lại nhập "
     "vượt bao nhiêu cũng được. Kiểm kỹ từng loại chi.\n"
     "3. ⚠️ Bấm \"Không duyệt\" đẩy phiếu sang trạng thái Không duyệt nhưng KHÔNG gửi thông báo cho "
     "ai, kể cả người lập. Người lập phải tự vào xem mới biết. Ghi nhận là hiện trạng.\n"
     "4. ⚠️ Cửa sổ chọn hợp đồng của loại Chi trả lại khách hàng và Chi thưởng NVKD CHỈ hiện hợp đồng "
     "do CHÍNH NGƯỜI ĐANG ĐĂNG NHẬP lập. Không thấy hợp đồng thường là vì hợp đồng của người khác.\n"
     "5. ⚠️ Nếu lưu phiếu mà hệ thống gặp lỗi, màn hình đổ ra một khối chữ kỹ thuật dài thay vì báo "
     "\"Cập nhật thất bại\". Gặp trường hợp này ghi nhận Failed và chụp lại toàn bộ màn hình.\n"
     "6. ⚠️ Xóa phiếu không kiểm tra quyền và không kiểm tra trạng thái ở phía hệ thống; ngoài ra xóa "
     "phiếu KHÔNG xóa theo các dòng chi tiết. Xem mục VI.\n"
     "7. ⚠️ Người lập phiếu mà đồng thời là trưởng phòng có thể bị CHẶN NGAY KHI BẤM LƯU nếu phòng "
     "mình quản lý còn nhân viên có hàng giữ / hàng mượn / hàng nhập thẳng quá hạn. Thông báo dạng "
     "\"Phòng ban bạn quản lý có nhân viên ... quá hạn. Không thể thực hiện thao tác này.\" Đây là ràng "
     "buộc CÓ CHỦ ĐÍCH, không phải lỗi; nhưng chỉ áp dụng khi công ty đã bật cấu hình chặn.\n"
     "8. ⚠️ Ô \"Đến ngày\" của bộ lọc làm rụng trọn ngày cuối (mục 4).\n"
     "9. ⚠️ Loại chi \"Chi trả nhà cung cấp\" BẮT BUỘC có tệp đính kèm khi tạo mới; các loại khác thì "
     "không. Tệp cho phép: pdf, png, jpg, jpeg, doc, docx, xls, xlsx, zip; tối đa khoảng 20 MB mỗi tệp.\n"
     "10. ⚠️ Ô \"Loại chi\" của màn nhập, màn danh sách và màn Chờ duyệt có số lựa chọn KHÁC NHAU "
     "(mục 3). Đừng kết luận thiếu lựa chọn khi chưa đối chiếu đúng màn.\n"
     "11. ⚠️ Tiền tố mã phiếu trùng với màn Phiếu đề nghị thu tiền (mục 5).\n"
     "12. Bộ lọc được ghi nhớ RIÊNG cho từng chế độ danh sách; test xong nhớ bấm nút làm mới bộ lọc "
     "trước khi sang ca test khác.\n"
     "13. Nhánh \"Chi trả nhà cung cấp KHÔNG có hợp đồng\" hiện không kích hoạt được vì ô chọn Kiểu "
     "hợp đồng đã bị ẩn khỏi giao diện — chỉ gặp ở phiếu cũ."),
]

# ============================================================ TC PHAN QUYEN
ROLE_TCS = [
    ("00", "Tài khoản không có quyền xem nào chỉ thấy phiếu do chính mình lập", "P0",
     "Tài khoản NV-A không được gán quyền nào trong 4 quyền xem theo cấp; NV-A đã lập 18 phiếu; công ty "
     "của NV-A có hơn 200 phiếu của nhiều người",
     "1. Đăng nhập bằng NV-A\n"
     "2. Mở menu Công nợ - Thu - Chi, bấm mục Đề nghị thanh toán\n"
     "3. Đọc số tổng dưới bảng\n"
     "4. Lật hết các trang, soát cột Người lập",
     "Tài khoản: NV-A (không quyền xem theo cấp)",
     "- Vào được màn hình, không bị chặn\n"
     "- Tổng hiện đúng 18\n"
     "- Mọi dòng đều có Người lập là NV-A\n"
     "- Nút Tạo mới VẪN hiển thị (hành vi lập phiếu không gắn quyền)"),

    ("01", "Quyền xem của tổng công ty thấy phiếu của mọi công ty", "P0",
     "Tài khoản B chỉ có quyền \"Xem tất cả phiếu đề nghị thanh toán của tổng công ty\"; hệ thống có "
     "phiếu của ít nhất 3 công ty",
     "1. Đăng nhập bằng B, mở mục Đề nghị thanh toán trên menu\n"
     "2. Bấm nút Bộ lọc\n"
     "3. Ghi lại các ô lọc theo đơn vị đang hiện\n"
     "4. Chọn lần lượt từng Công ty rồi bấm nút tìm kiếm",
     "Quyền: Xem tất cả phiếu đề nghị thanh toán của tổng công ty",
     "- Khối lọc hiện CẢ ô Công ty và ô Phòng ban\n"
     "- Chọn công ty nào ra phiếu của công ty đó\n"
     "- Bỏ chọn công ty thì thấy phiếu của cả 3 công ty"),

    ("02", "Quyền xem của công ty chỉ thấy phiếu công ty mình", "P0",
     "Tài khoản C chỉ có quyền \"Xem tất cả phiếu đề nghị thanh toán của công ty\", thuộc công ty 3; "
     "công ty 3 có 90 phiếu, công ty 1 có 600 phiếu",
     "1. Đăng nhập bằng C, mở mục Đề nghị thanh toán\n"
     "2. Bấm nút Bộ lọc, ghi lại các ô lọc theo đơn vị\n"
     "3. Đọc số tổng và soát cột Phòng ban",
     "Quyền: Xem tất cả phiếu đề nghị thanh toán của công ty",
     "- Khối lọc KHÔNG có ô Công ty, chỉ có ô Phòng ban\n"
     "- Tổng bằng 90 trừ đi số phiếu nháp của người khác trong công ty 3\n"
     "- Không có phiếu nào của công ty 1"),

    ("03", "Quyền xem của phòng ban chỉ thấy phiếu phòng ban mình quản lý", "P0",
     "Tài khoản D chỉ có quyền \"Xem tất cả phiếu đề nghị thanh toán của phòng ban\", được phân công "
     "quản lý đúng 2 phòng ban trong công ty mình; 2 phòng ban đó có 20 phiếu",
     "1. Đăng nhập bằng D, mở mục Đề nghị thanh toán\n"
     "2. Bấm nút Bộ lọc, ghi lại các ô lọc theo đơn vị\n"
     "3. Soát cột Phòng ban của mọi dòng qua tất cả các trang",
     "Quyền: Xem tất cả phiếu đề nghị thanh toán của phòng ban",
     "- Khối lọc hiện ô Phòng ban và ô Bộ phận\n"
     "- Ô Phòng ban CHỈ liệt kê 2 phòng ban D được phân công\n"
     "- Chỉ hiện phiếu thuộc 2 phòng ban đó, cộng phiếu nháp của chính D"),

    ("04", "Quyền xem của bộ phận chỉ thấy phiếu bộ phận mình quản lý", "P1",
     "Tài khoản E chỉ có quyền \"Xem tất cả phiếu đề nghị thanh toán của bộ phận\", quản lý 1 bộ phận "
     "trong công ty mình",
     "1. Đăng nhập bằng E, mở mục Đề nghị thanh toán\n"
     "2. Đọc số tổng và soát danh sách\n"
     "3. Bấm nút Bộ lọc, quan sát các ô lọc theo đơn vị",
     "Quyền: Xem tất cả phiếu đề nghị thanh toán của bộ phận",
     "- Chỉ hiện phiếu thuộc đúng bộ phận được phân công, cộng phiếu nháp của chính E\n"
     "- ⚠️ Khối lọc KHÔNG hiện ô Công ty / Phòng ban / Bộ phận cho mức quyền này — ghi nhận đúng hiện "
     "trạng"),

    ("05", "Có nhiều quyền xem cùng lúc thì lấy phạm vi rộng nhất", "P1",
     "Tài khoản F có ĐỒNG THỜI quyền xem của tổng công ty và quyền xem của bộ phận",
     "1. Đăng nhập bằng F, mở mục Đề nghị thanh toán\n"
     "2. Đọc số tổng, so với số của tài khoản B ở TC-ROLE-01",
     "Quyền: tổng công ty + bộ phận",
     "- Tổng bằng đúng số của tài khoản chỉ có quyền tổng công ty\n"
     "- Không bị thu hẹp về phạm vi bộ phận"),

    ("06", "Trưởng phòng chỉ thấy phiếu chờ mình duyệt của phòng mình quản lý", "P0",
     "Tài khoản TP-1 có quyền \"Trưởng phòng duyệt đề nghị thanh toán\", quản lý phòng P1; công ty có "
     "3 phiếu Chờ TP duyệt của phòng P1 và 5 phiếu Chờ TP duyệt của phòng P2",
     "1. Đăng nhập bằng TP-1\n"
     "2. Mở mục Phiếu đề nghị thanh toán chờ duyệt trên menu\n"
     "3. Đọc số tổng, cột Trạng thái và cột Phòng ban",
     "Quyền: Trưởng phòng duyệt đề nghị thanh toán",
     "- Mục menu HIỂN THỊ\n"
     "- Đúng 3 dòng, tất cả đều Chờ TP duyệt và thuộc phòng P1\n"
     "- KHÔNG thấy 5 phiếu của phòng P2\n"
     "- Phía trên bảng KHÔNG có nút Tạo mới"),

    ("07", "Kế toán công nợ thấy toàn bộ phiếu ở bước của mình trong công ty", "P0",
     "Tài khoản KTCN-1 chỉ có quyền \"Kế toán công nợ duyệt đề nghị thanh toán\"; công ty có 4 phiếu "
     "Chờ kế toán công nợ duyệt của 3 phòng ban khác nhau và 3 phiếu Chờ TP duyệt",
     "1. Đăng nhập bằng KTCN-1, mở màn chờ duyệt\n"
     "2. Đọc số tổng và cột Trạng thái",
     "—",
     "- Đúng 4 dòng, tất cả đều Chờ kế toán công nợ duyệt\n"
     "- Thấy đủ phiếu của cả 3 phòng ban, không bị giới hạn theo phòng\n"
     "- KHÔNG thấy 3 phiếu Chờ TP duyệt"),

    ("08", "Kế toán trưởng thấy đúng bước của mình", "P0",
     "Tài khoản KTT-1 chỉ có quyền \"Kế toán trưởng duyệt đề nghi thanh toán\" (chú ý tên quyền viết "
     "thiếu dấu); công ty có 2 phiếu Chờ kế toán trưởng duyệt",
     "1. Đăng nhập bằng KTT-1, mở màn chờ duyệt\n"
     "2. Đọc số tổng và cột Trạng thái",
     "Quyền: Kế toán trưởng duyệt đề nghi thanh toán",
     "- Đúng 2 dòng, đều ở Chờ kế toán trưởng duyệt\n"
     "- ⚠️ Nếu gán nhầm sang tên có dấu đầy đủ thì màn này rỗng — kiểm lại tên quyền trước khi báo lỗi"),

    ("09", "Ban giám đốc thấy đúng bước của mình", "P0",
     "Tài khoản BGD-1 chỉ có quyền \"Ban giám đốc duyệt đề nghi thanh toán\"; công ty có 1 phiếu Chờ "
     "ban giám đốc duyệt",
     "1. Đăng nhập bằng BGD-1, mở màn chờ duyệt\n"
     "2. Đọc số tổng và cột Trạng thái",
     "Quyền: Ban giám đốc duyệt đề nghi thanh toán",
     "- Đúng 1 dòng, ở Chờ ban giám đốc duyệt\n"
     "- Không thấy phiếu ở các bước khác"),

    ("10", "Kế toán thanh toán thấy phiếu chờ tạo phiếu chi", "P0",
     "Tài khoản KTTT-1 chỉ có quyền \"Kế toán thanh toán\"; công ty có 6 phiếu Chờ tạo phiếu chi",
     "1. Đăng nhập bằng KTTT-1, mở màn chờ duyệt\n"
     "2. Đọc số tổng và cột Trạng thái\n"
     "3. Mở menu hành động của một dòng hình thức thanh toán TM và một dòng CK",
     "—",
     "- Đúng 6 dòng, đều ở Chờ tạo phiếu chi\n"
     "- Dòng TM có mục \"Tạo phiếu chi\"; dòng CK có mục \"Tạo phiếu ủy nhiệm chi\"\n"
     "- Cả hai dòng đều có thêm mục \"Không duyệt\""),

    ("11", "Người giữ nhiều quyền duyệt thấy gộp nhiều bước", "P1",
     "Tài khoản KT-ALL có ĐỒNG THỜI quyền kế toán công nợ, kế toán trưởng và kế toán thanh toán; công "
     "ty có 4 phiếu ở bước công nợ, 2 phiếu ở bước kế toán trưởng, 6 phiếu ở bước chờ tạo phiếu chi",
     "1. Đăng nhập bằng KT-ALL, mở màn chờ duyệt\n"
     "2. Đọc số tổng\n"
     "3. Lọc lần lượt từng trạng thái để đếm",
     "—",
     "- Tổng hiện 12 dòng\n"
     "- Đủ cả 3 nhóm trạng thái, không thiếu nhóm nào\n"
     "- Không lẫn phiếu ở bước Chờ TP duyệt và Chờ ban giám đốc duyệt"),

    ("12", "Không có quyền duyệt nào vẫn mở được màn chờ duyệt", "P0",
     "Tài khoản NV-A không có bất kỳ quyền duyệt nào trong 5 quyền; công ty của NV-A có nhiều phiếu ở "
     "đủ các bước, gồm cả phiếu nháp của người khác",
     "1. Đăng nhập bằng NV-A\n"
     "2. Tìm mục Phiếu đề nghị thanh toán chờ duyệt trên menu\n"
     "3. Dán thẳng đường dẫn màn chờ duyệt vào thanh địa chỉ\n"
     "4. Đọc số tổng và cột Trạng thái",
     "Đường dẫn màn chờ duyệt",
     "- Mục menu KHÔNG hiển thị\n"
     "- ⚠️ Hiện trạng: dán thẳng đường dẫn thì màn MỞ ĐƯỢC và liệt kê TẤT CẢ phiếu của công ty, gồm cả "
     "phiếu nháp của người khác. LỖ HỔNG, ghi nhận Failed\n"
     "- Kỳ vọng đúng: chặn truy cập hoặc trả về bảng rỗng"),

    ("13", "Mở chi tiết phiếu ngoài phạm vi quyền bị chặn", "P0",
     "Tài khoản NV-A (không quyền xem theo cấp, không quyền duyệt); lấy đường dẫn chi tiết của 1 phiếu "
     "do người khác lập ở phòng ban khác, trạng thái Duyệt phiếu chi",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dán đường dẫn chi tiết phiếu đó vào thanh địa chỉ",
     "Phiếu người khác, trạng thái Duyệt phiếu chi",
     "- Hệ thống hiện trang báo không tìm thấy nội dung\n"
     "- Không hiển thị bất kỳ dữ liệu nào của phiếu"),

    ("14", "Người duyệt ở bước hiện tại mở được chi tiết dù không có quyền xem theo cấp", "P0",
     "Tài khoản KTCN-1 chỉ có quyền kế toán công nợ, không có quyền xem theo cấp nào; phiếu X đang ở "
     "Chờ kế toán công nợ duyệt, do người khác lập, cùng công ty",
     "1. Đăng nhập bằng KTCN-1\n"
     "2. Mở chi tiết phiếu X\n"
     "3. Sau khi phiếu chuyển sang bước sau, mở lại chi tiết phiếu X",
     "—",
     "- Lúc phiếu còn ở bước của mình: mở được chi tiết bình thường\n"
     "- Sau khi đã duyệt: vẫn mở được (người đã duyệt luôn xem lại được)\n"
     "- Nếu phiếu chuyển sang bước sau do người khác xử lý thì KTCN-1 không còn mở được"),

    ("15", "Người đã duyệt xem lại phiếu ở chế độ Đã xử lý", "P1",
     "Tài khoản TP-1 đã duyệt 5 phiếu ở bước trưởng phòng",
     "1. Đăng nhập bằng TP-1\n"
     "2. Mở chế độ Đã xử lý bằng đường dẫn trực tiếp\n"
     "3. Đọc số tổng và cột Trạng thái",
     "—",
     "- Liệt kê đúng 5 phiếu TP-1 đã duyệt, ở nhiều trạng thái khác nhau\n"
     "- Không có mục menu nào dẫn tới chế độ này"),

    ("16", "Bỏ qua giao diện gọi thẳng chức năng Xóa phiếu của người khác", "P0",
     "Tài khoản NV-A; đường dẫn xóa của 1 phiếu trạng thái Duyệt phiếu chi do người khác lập; đã sao "
     "lưu dữ liệu trước khi test",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dán thẳng đường dẫn xóa của phiếu đó\n"
     "3. Kiểm tra phiếu còn hay mất",
     "Phiếu Duyệt phiếu chi của người khác",
     "- ⚠️ Hiện trạng: phiếu BỊ XÓA, hệ thống báo xóa thành công. LỖ HỔNG, ghi nhận Failed\n"
     "- Kỳ vọng đúng: từ chối và giữ nguyên phiếu\n"
     "- Khôi phục dữ liệu ngay sau khi test"),

    ("17", "Bỏ qua giao diện gọi thẳng chức năng Sửa để tự duyệt phiếu", "P0",
     "Tài khoản NV-A không có quyền duyệt nào; phiếu Y đang ở Chờ TP duyệt",
     "1. Đăng nhập bằng NV-A, lấy phiên đăng nhập\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Cập nhật phiếu Y, gửi trạng thái là Chờ tạo "
     "phiếu chi\n"
     "3. Mở lại phiếu Y, đọc Trạng thái",
     "Trạng thái gửi lên: Chờ tạo phiếu chi",
     "- ⚠️ Hiện trạng: phiếu nhảy thẳng sang Chờ tạo phiếu chi, bỏ qua cả 3 cấp duyệt. LỖ HỔNG nghiêm "
     "trọng, ghi nhận Failed\n"
     "- Kỳ vọng đúng: từ chối vì người gọi không có quyền duyệt ở bước hiện tại"),

    ("18", "Bỏ qua giao diện gọi thẳng chức năng đổi trạng thái để từ chối phiếu", "P0",
     "Tài khoản NV-A không có quyền duyệt nào; phiếu Z đang ở Chờ kế toán trưởng duyệt",
     "1. Đăng nhập bằng NV-A, lấy phiên đăng nhập\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng đổi trạng thái phiếu Z sang Không duyệt kèm lý "
     "do bất kỳ\n"
     "3. Mở lại phiếu Z",
     "—",
     "- ⚠️ Hiện trạng: phiếu chuyển sang Không duyệt. LỖ HỔNG, ghi nhận Failed\n"
     "- Kỳ vọng đúng: chỉ người có quyền ở đúng bước mới từ chối được"),

    ("19", "In và Xuất Excel phiếu của người khác không bị chặn", "P1",
     "Tài khoản NV-A; đường dẫn in và đường dẫn xuất Excel của 1 phiếu ở công ty khác",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dán thẳng đường dẫn in của phiếu đó\n"
     "3. Dán thẳng đường dẫn xuất Excel",
     "Phiếu công ty khác",
     "- ⚠️ Hiện trạng: bản in hiện đầy đủ và tệp Excel tải về được. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: kiểm tra quyền xem trước khi cho in và xuất, như màn chi tiết"),

    ("20", "Trưởng phòng bị chặn thao tác khi phòng còn hàng quá hạn", "P1",
     "Tài khoản TP-2 quản lý phòng P3; công ty của TP-2 ĐÃ bật cấu hình chặn cho hành động \"Duyệt đề "
     "nghị thanh toán\"; phòng P3 đang có nhân viên còn hàng giữ quá hạn",
     "1. Đăng nhập bằng TP-2\n"
     "2. Tạo một phiếu đề nghị thanh toán hợp lệ, bấm Lưu\n"
     "3. Đọc thông báo\n"
     "4. Mở màn chờ duyệt, mở một phiếu ở bước Chờ TP duyệt, bấm TP Duyệt",
     "—",
     "- Cả 2 thao tác đều bị chặn\n"
     "- Thông báo dạng \"Phòng ban bạn quản lý có nhân viên hàng giữ quá hạn. Không thể thực hiện thao "
     "tác này.\"\n"
     "- ⚠️ Đây là ràng buộc CÓ CHỦ ĐÍCH, không ghi Failed. Nhưng lưu ý nó chặn cả việc TP tự lập phiếu "
     "của mình, không chỉ chặn duyệt\n"
     "- Tài khoản Super Admin không bị chặn"),
]
