# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Ke hoach kiem ke theo vi tri'."""

MENU = ("Mở menu Kế toán > nhóm \"Kiểm kê\" > cột \"Theo vị trí\" > bấm \"Kế hoạch kiểm kê theo vị trí\"")

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Quản lý Kế hoạch kiểm kê theo vị trí: chứng từ do người lập (thường là kế toán kho) tạo ra để "
     "chốt PHẠM VI cần kiểm kê trong một kho vật lý (Nhà > Dãy > Khoang > Vị trí) và HỘI ĐỒNG KIỂM KÊ.\n"
     "Khi bấm \"Lấy vị trí\", hệ thống chụp lại tồn kho hiện tại của từng vị trí đã chọn, chi tiết tới "
     "hàng hóa, công ty sở hữu và lô nhập. Số liệu này là căn cứ để thủ kho lập Phiếu kiểm kê theo vị trí.\n"
     "Người dùng làm được: xem danh sách, lọc, tạo kế hoạch (Lưu nháp hoặc Lưu & Gửi), sửa, xóa khi còn "
     "nháp, xem chi tiết, in và xuất Excel từng kế hoạch hoặc cả danh sách.\n"
     "Thủ kho của kho được kiểm (có quyền Lập phiếu kiểm kê kho theo vị trí) nhận thông báo và bấm "
     "\"Lập phiếu kiểm kê theo vị trí\" ngay trên kế hoạch."),

    ("2. Đối tượng được tính / hiển thị",
     "Kế hoạch có 4 trạng thái hiển thị:\n"
     "- Đang tạo (nhãn ĐỎ): vừa bấm Lưu, còn sửa / xóa được.\n"
     "- Đang kiểm (nhãn VÀNG): đã bấm Lưu & Gửi, chờ thủ kho lập phiếu kiểm kê.\n"
     "- Đã lập kiểm kê (nhãn XANH): thủ kho đã lưu Phiếu kiểm kê theo vị trí từ kế hoạch này.\n"
     "- Hoàn thành (nhãn XANH): phiếu kiểm kê lập từ kế hoạch được Ban kiểm soát duyệt mà KHÔNG có "
     "dòng nào thiếu hàng, hoặc mọi dòng thiếu đã được điều chuyển vị trí đủ số.\n"
     "Phạm vi kế hoạch nhìn thấy phụ thuộc lối vào:\n"
     "- Lối vào từ menu (Kế toán > Kiểm kê > Theo vị trí > Kế hoạch kiểm kê theo vị trí): theo quyền xem "
     "ở mục 7, luôn ẩn kế hoạch Đang tạo của người khác.\n"
     "- Lối vào từ Trang chủ > tab \"Phê duyệt\" > thẻ \"Kiểm kê\" > ô \"Kế hoạch kiểm kê vị trí chờ "
     "duyệt\": chỉ kế hoạch Đang kiểm của các kho mà người đăng nhập được phân công làm thủ kho (cần "
     "quyền Lập phiếu kiểm kê kho theo vị trí).\n"
     "- Lối vào \"Kế hoạch của tôi\" (không có mục menu, chỉ có khi bỏ tham số trên thanh địa chỉ): chỉ "
     "kế hoạch do chính mình lập, gồm cả nháp.\n"
     "Bảng chi tiết của kế hoạch chỉ gồm các vị trí đã tích VÀ đang có tồn lớn hơn 0; trong mỗi vị trí "
     "chỉ gồm lô còn tồn lớn hơn 0."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Kế hoạch Đang tạo của NGƯỜI KHÁC bị ẩn ở lối vào menu, kể cả với quyền tổng công ty.\n"
     "- Nút Sửa và Xóa (trong menu bánh răng ở cột Hành động) chỉ hiện khi kế hoạch Đang tạo VÀ người "
     "đăng nhập là người lập.\n"
     "- Nút \"Lập phiếu kiểm kê theo vị trí\" chỉ hiện khi kế hoạch Đang kiểm VÀ người đăng nhập có quyền "
     "Lập phiếu kiểm kê kho theo vị trí VÀ là thủ kho của kho được kiểm (tài khoản Super Admin được coi "
     "là thủ kho mọi kho, nhưng vẫn phải có quyền).\n"
     "- Nút In và Xuất excel luôn hiện cho mọi dòng, mọi trạng thái.\n"
     "- Vị trí đã tích nhưng KHÔNG có tồn bị loại khỏi bảng chi tiết (nhưng vẫn được ghi nhận vào phạm vi "
     "của kế hoạch, xem bộ lọc Vị trí ở mục 9).\n"
     "- Màn hình KHÔNG có chức năng Hủy kế hoạch, KHÔNG có ô Ghi chú, KHÔNG có Nhập Excel.\n"
     "- Ô lọc Công ty / Phòng ban chỉ hiện ở lối vào menu với người có quyền xem theo tổng công ty / "
     "theo công ty."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Hai ô \"Từ ngày\" và \"Đến ngày\" lọc theo NGÀY LẬP kế hoạch (chính là cột \"Ngày kiểm kê\" trên "
     "lưới).\n"
     "Hai đầu mút đều được tính TRỌN NGÀY: kế hoạch lập lúc 23:59 của ngày điền ở ô \"Đến ngày\" vẫn có "
     "trong kết quả.\n"
     "Ô \"Ngày kiểm kê\" trên màn nhập luôn là ngày lập (hôm nay), bị khóa, không sửa được."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Phần phạm vi (khung trên): 1 Kho vật lý > Nhà > Dãy > Khoang > Vị trí. Vị trí KHÔNG thuộc khoang "
     "nào (vị trí tự do) hiện ngay dưới tên kho ở khung Vị trí.\n"
     "Phần Chi tiết, tab \"Vị trí\": Vị trí > Hàng hóa (Tên hàng, Model, Mã hàng, Thương hiệu, ĐVT, SL "
     "tồn) > Công ty sở hữu > Lô (SL) và cột \"Cộng\" của công ty.\n"
     "Phần Chi tiết, tab \"Hội đồng kiểm kê\": danh sách Thành viên + Chức vụ (Chức vụ chọn trong các vai "
     "trò đã gán cho nhân viên đó trên hệ thống).\n"
     "Số phiếu sinh tự động: <mã công ty của người lập>-KHKKVT-<số thứ tự 5 chữ số>, ví dụ "
     "TPE-KHKKVT-00125."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- \"SL tồn\" của một hàng = tồn của hàng đó tại vị trí lúc bấm Lấy vị trí.\n"
     "- \"Cộng\" của một công ty = tổng SL các lô của công ty đó tại vị trí đó.\n"
     "- Cùng một hàng có tồn của 2 công ty thì tách 2 nhóm công ty, mỗi nhóm có danh sách lô riêng.\n"
     "- Một vị trí chỉ xuất hiện 1 lần trong kế hoạch; một nhân viên chỉ được có 1 dòng trong Hội đồng "
     "kiểm kê (trùng thì không lưu được).\n"
     "- Số liệu tồn được LƯU CỨNG lúc bấm Lưu; tồn thay đổi sau đó không làm đổi màn Chi tiết, bản In "
     "hay Excel.\n"
     "- Riêng khi mở màn Sửa, hệ thống TỰ BẤM Lấy vị trí lại: số liệu trên màn Sửa là tồn HIỆN TẠI, lưu "
     "lại thì ghi đè số cũ."),

    ("7. Phân quyền cấp",
     "Ba quyền thuộc nhóm \"Kiểm kê kho\" (phân hệ Kho):\n"
     "- \"Tổng kiểm kê kho theo vị trí - tổng công ty\": ở lối vào menu xem kế hoạch của MỌI công ty; khối "
     "lọc có thêm ô Công ty và Phòng ban.\n"
     "- \"Tổng kiểm kê kho theo vị trí\": ở lối vào menu xem kế hoạch của công ty mình và kế hoạch do mình "
     "lập; khối lọc có thêm ô Phòng ban (chỉ phòng ban của công ty mình).\n"
     "- \"Lập phiếu kiểm kê kho theo vị trí\": cùng với việc được phân công làm thủ kho của kho, người dùng "
     "thấy ô chờ duyệt ở Trang chủ, nhận thông báo khi kế hoạch được gửi và có nút \"Lập phiếu kiểm kê "
     "theo vị trí\".\n"
     "Không có quyền nào: vẫn vào được màn, vẫn Tạo mới được, chỉ thấy kế hoạch của mình.\n"
     "Xem chi tiết, In, Xuất excel KHÔNG kiểm tra quyền.\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API (bỏ qua giao diện) dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- Dòng thông tin dưới bảng: \"Hiển thị a đến b của N\" — a là dòng đầu trang, b là dòng cuối trang, "
     "N là tổng kế hoạch khớp bộ lọc trong phạm vi lối vào đang mở.\n"
     "- Ô \"Kế hoạch kiểm kê vị trí chờ duyệt\" ở Trang chủ = số kế hoạch Đang kiểm của các kho mà người "
     "đăng nhập là thủ kho; số này phải BẰNG N khi bấm vào ô. Ô bị ẩn khi bằng 0.\n"
     "- Tiêu đề thẻ \"Kiểm kê (n)\" ở Trang chủ: n là số ô con đang có số lớn hơn 0, KHÔNG phải tổng phiếu.\n"
     "- STT trên lưới đánh liên tục qua các trang."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất:\n"
     "- Ô lọc Công ty và Phòng ban HIỆN RA nhưng KHÔNG có tác dụng lọc — đổi giá trị không làm đổi kết "
     "quả. Ghi Failed nếu nghiệp vụ yêu cầu lọc được.\n"
     "- Ô lọc Kho và ô Kho vật lý trên màn nhập liệt kê kho của MỌI công ty, gồm cả kho ngừng hoạt động.\n"
     "- Ô lọc Nhà kho / Dãy / Khoang / Vị trí lọc theo PHẠM VI ĐÃ TÍCH lúc lập, không phải theo vị trí có "
     "trong bảng chi tiết.\n"
     "- Thông báo lỗi kiểm tra dữ liệu dưới từng ô đang hiển thị bằng TIẾNG ANH (ví dụ \"The members field "
     "is required.\").\n"
     "- Sửa xong bấm Lưu, hệ thống vẫn báo \"Tạo thành công\".\n"
     "- Bản In và Excel: cột \"Nhà Kho\" in MÃ KHO (màn hình hiện mã NHÀ); không có cột Model, Thương hiệu.\n"
     "- Lô có SL lẻ nhỏ hơn 1 (ví dụ 0,5) làm kế hoạch KHÔNG lưu được.\n"
     "- Kế hoạch chuyển sang \"Đã lập kiểm kê\" ngay khi thủ kho bấm Lưu phiếu kiểm kê (kể cả lưu nháp).\n"
     "- Kế hoạch lên \"Hoàn thành\" khi phiếu kiểm kê được duyệt mà KHÔNG thiếu hàng, hoặc khi phiếu điều "
     "chuyển vị trí chuyển đủ mọi dòng thiếu. Dòng thiếu xử lý bằng Tổng kiểm kê rồi bấm Hoàn thành thì "
     "kế hoạch vẫn đứng ở \"Đã lập kiểm kê\".\n"
     "- Nút \"Quay lại\" trên màn Tạo mới / Sửa / Chi tiết luôn về danh sách lối vào menu, kể cả khi đi "
     "vào từ Trang chủ.\n"
     "- Hệ thống ghi nhớ bộ lọc và trang đang xem theo từng lối vào, trên từng trình duyệt."),
]


ROLE_TCS = [
    ("00", "Tài khoản không có quyền nào chỉ thấy kế hoạch do mình lập", "P0",
     "Tài khoản NV-A không có quyền nào trong 3 quyền ở mục 7\n"
     "NV-A đã lập 3 kế hoạch (1 Đang tạo, 2 Đang kiểm)\n"
     "Công ty của NV-A có thêm 20 kế hoạch của người khác",
     "1. Đăng nhập bằng NV-A\n"
     "2. " + MENU + "\n"
     "3. Đọc số tổng dưới bảng\n"
     "4. Bấm nút Bộ lọc, quan sát các ô lọc",
     "Tài khoản: NV-A",
     "- Vào được màn, không bị chặn\n"
     "- Tổng hiện đúng 3, mọi dòng có Người lập là NV-A\n"
     "- Nút Tạo mới VẪN hiển thị (lập kế hoạch không gắn quyền)\n"
     "- Khối lọc KHÔNG có ô Công ty, Phòng ban"),

    ("01", "Quyền tổng công ty thấy kế hoạch của mọi công ty", "P0",
     "Tài khoản B chỉ có quyền \"Tổng kiểm kê kho theo vị trí - tổng công ty\"\n"
     "Công ty 1 có 10 kế hoạch đã gửi, công ty 3 có 4 kế hoạch đã gửi\n"
     "Người khác có 2 kế hoạch Đang tạo",
     "1. Đăng nhập bằng B\n"
     "2. " + MENU + "\n"
     "3. Đọc số tổng\n"
     "4. Bấm nút Bộ lọc, quan sát các ô lọc",
     "Quyền: Tổng kiểm kê kho theo vị trí - tổng công ty",
     "- Tổng = 14 (kế hoạch của cả 2 công ty) cộng kế hoạch B tự lập\n"
     "- 2 kế hoạch Đang tạo của người khác KHÔNG hiện\n"
     "- Khối lọc hiện CẢ ô Công ty và ô Phòng ban"),

    ("02", "Quyền theo công ty chỉ thấy kế hoạch công ty mình và kế hoạch mình lập", "P0",
     "Tài khoản C chỉ có quyền \"Tổng kiểm kê kho theo vị trí\", thuộc công ty 3\n"
     "Công ty 3 có 4 kế hoạch đã gửi, công ty 1 có 10 kế hoạch đã gửi\n"
     "C đã lập 1 kế hoạch khi còn thuộc công ty 1",
     "1. Đăng nhập bằng C\n"
     "2. " + MENU + "\n"
     "3. Đọc số tổng, soát cột Số phiếu (tiền tố mã công ty)\n"
     "4. Bấm Bộ lọc, mở ô Phòng ban",
     "Quyền: Tổng kiểm kê kho theo vị trí",
     "- Tổng = 4 + 1 = 5\n"
     "- Không thấy kế hoạch nào khác của công ty 1\n"
     "- Khối lọc có ô Phòng ban, KHÔNG có ô Công ty\n"
     "- Ô Phòng ban chỉ liệt kê phòng ban của công ty 3"),

    ("03", "Có cả hai quyền xem thì áp quyền rộng hơn", "P1",
     "Tài khoản D có cả \"Tổng kiểm kê kho theo vị trí - tổng công ty\" và \"Tổng kiểm kê kho theo vị trí\"",
     "1. Đăng nhập bằng D, mở màn từ menu\n"
     "2. So số tổng với tài khoản B ở TC-ROLE-01",
     "—",
     "- Số tổng bằng số của B (phạm vi tổng công ty)\n"
     "- Khối lọc có ô Công ty"),

    ("04", "Thủ kho có quyền Lập phiếu thấy ô chờ duyệt và nút Lập phiếu kiểm kê", "P0",
     "Tài khoản TK1 có quyền \"Lập phiếu kiểm kê kho theo vị trí\", được phân công thủ kho của kho K1\n"
     "Có 2 kế hoạch Đang kiểm của kho K1 và 1 kế hoạch Đang kiểm của kho K2",
     "1. Đăng nhập bằng TK1, ở Trang chủ bấm tab \"Phê duyệt\"\n"
     "2. Tìm thẻ \"Kiểm kê\", đọc số ở ô \"Kế hoạch kiểm kê vị trí chờ duyệt\"\n"
     "3. Bấm vào ô đó\n"
     "4. Bấm biểu tượng bánh răng ở cột Hành động của từng dòng",
     "—",
     "- Ô hiện số 2\n"
     "- Danh sách mở ra có đúng 2 kế hoạch của kho K1\n"
     "- Menu bánh răng có dòng \"Lập phiếu kiểm kê theo vị trí\", In, Xuất excel\n"
     "- Kế hoạch của kho K2 KHÔNG xuất hiện"),

    ("05", "Có quyền Lập phiếu nhưng không phải thủ kho của kho thì không có nút", "P0",
     "Tài khoản TK2 có quyền \"Lập phiếu kiểm kê kho theo vị trí\", chỉ là thủ kho kho K2\n"
     "TK2 có thêm quyền \"Tổng kiểm kê kho theo vị trí\" để nhìn thấy kế hoạch của kho K1",
     "1. Đăng nhập bằng TK2, mở màn từ menu\n"
     "2. Tìm 1 kế hoạch Đang kiểm của kho K1, bấm bánh răng",
     "—",
     "- Menu bánh răng chỉ có In, Xuất excel\n"
     "- KHÔNG có \"Lập phiếu kiểm kê theo vị trí\""),

    ("06", "Là thủ kho nhưng thiếu quyền Lập phiếu thì không có nút và không có ô chờ duyệt", "P0",
     "Tài khoản TK3 là thủ kho kho K1 nhưng KHÔNG có quyền \"Lập phiếu kiểm kê kho theo vị trí\"\n"
     "Kho K1 có 2 kế hoạch Đang kiểm",
     "1. Đăng nhập bằng TK3, ở Trang chủ bấm tab \"Phê duyệt\"\n"
     "2. Tìm ô \"Kế hoạch kiểm kê vị trí chờ duyệt\"\n"
     "3. Mở màn từ menu, bấm bánh răng của kế hoạch kho K1 (nếu nhìn thấy)",
     "—",
     "- Không có ô \"Kế hoạch kiểm kê vị trí chờ duyệt\"\n"
     "- Không có nút \"Lập phiếu kiểm kê theo vị trí\""),

    ("07", "Super Admin có quyền Lập phiếu được lập phiếu kiểm kê cho mọi kho", "P2",
     "Tài khoản SA có vai trò Super Admin và quyền \"Lập phiếu kiểm kê kho theo vị trí\", KHÔNG là thủ kho "
     "kho nào",
     "1. Đăng nhập bằng SA, mở màn từ menu\n"
     "2. Bấm bánh răng của một kế hoạch Đang kiểm bất kỳ\n"
     "3. Ở Trang chủ đọc ô \"Kế hoạch kiểm kê vị trí chờ duyệt\"",
     "—",
     "- Có nút \"Lập phiếu kiểm kê theo vị trí\" trên mọi kế hoạch Đang kiểm\n"
     "- Lưu ý: ô chờ duyệt ở Trang chủ KHÔNG hiện (vì SA không là thủ kho kho nào) — đúng code hiện tại"),

    ("08", "Chỉ người lập mới thấy Sửa / Xóa trên kế hoạch Đang tạo", "P0",
     "NV-A lập kế hoạch KH-1 ở trạng thái Đang tạo\n"
     "NV-B cùng công ty có quyền \"Tổng kiểm kê kho theo vị trí - tổng công ty\"",
     "1. Đăng nhập NV-A, bấm bánh răng của KH-1\n"
     "2. Đăng nhập NV-B, tìm KH-1 bằng ô Mã phiếu",
     "—",
     "- NV-A thấy: Sửa, Xóa, In, Xuất excel\n"
     "- NV-B KHÔNG tìm thấy KH-1 (nháp người khác bị ẩn)"),

    ("09", "Xem chi tiết, In, Xuất excel không kiểm tra quyền", "P1",
     "NV-X thuộc công ty 3, không có quyền nào\n"
     "Kế hoạch KH-2 của công ty 1; NV-X nhận được đường dẫn màn Chi tiết KH-2 từ đồng nghiệp",
     "1. Đăng nhập NV-X\n"
     "2. Dán đường dẫn màn Chi tiết KH-2 vào trình duyệt\n"
     "3. Quan sát nội dung",
     "—",
     "- Theo code hiện tại: hệ thống MỞ ĐƯỢC chi tiết KH-2, In và Xuất excel cũng được\n"
     "- Lưu ý: đây là điểm hở cô lập dữ liệu giữa các công ty — ghi Failed nếu nghiệp vụ yêu cầu chặn"),

    ("10", "Gọi thẳng chức năng Lưu sửa trên kế hoạch không phải của mình", "P0",
     "Kế hoạch KH-3 do NV-A lập, đang Đang kiểm\n"
     "Tester kỹ thuật đăng nhập bằng NV-B",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Lưu sửa của KH-3, bỏ qua giao diện, gửi trạng thái "
     "Đang tạo và danh sách thành viên khác\n"
     "2. Mở lại KH-3 trên giao diện",
     "—",
     "- Mong đợi: hệ thống từ chối, báo không có quyền, KH-3 giữ nguyên\n"
     "- Lưu ý: bước lưu sửa hiện KHÔNG kiểm tra người lập và trạng thái — nếu KH-3 bị đổi thì ghi Failed"),

    ("11", "Gọi thẳng chức năng Xóa kế hoạch của người khác", "P0",
     "Kế hoạch KH-1 Đang tạo do NV-A lập; tester đăng nhập NV-B",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa của KH-1, bỏ qua giao diện\n"
     "2. Đăng nhập NV-A kiểm tra KH-1",
     "—",
     "- Hệ thống báo \"Không thể xóa!\"\n"
     "- KH-1 vẫn còn nguyên"),

    ("12", "Mở thẳng màn Sửa của kế hoạch đã gửi", "P1",
     "Kế hoạch KH-3 Đang kiểm do chính NV-A lập",
     "1. Đăng nhập NV-A\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng mở màn Sửa của KH-3",
     "—",
     "- Hệ thống báo \"Không có quyền\", không mở form sửa"),

    ("13", "Mở thẳng màn lập phiếu kiểm kê từ kế hoạch khi không phải thủ kho", "P1",
     "Kế hoạch KH-3 Đang kiểm của kho K1\n"
     "TK2 có quyền Lập phiếu kiểm kê kho theo vị trí nhưng chỉ là thủ kho K2",
     "1. Đăng nhập TK2\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng mở màn Lập phiếu kiểm kê theo vị trí gắn kế hoạch "
     "KH-3",
     "—",
     "- Hệ thống hiện trang không tìm thấy, không cho lập phiếu"),
]
