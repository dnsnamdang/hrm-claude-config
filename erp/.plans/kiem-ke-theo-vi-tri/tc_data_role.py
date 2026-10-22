# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Kiem ke theo vi tri' (phieu kiem ke)."""

MENU = "Mở menu Kho > nhóm \"Kiểm kho\" > cột \"Theo vị trí\" > bấm \"Kiểm kê theo vị trí\""
HOME = ("Ở Trang chủ bấm tab \"Phê duyệt\" > thẻ \"Kiểm kê\" > bấm ô \"Kiểm kê vị trí chờ duyệt\"")

# Du lieu mau dung chung
P1 = ("Vị trí P1 (nhà N1, kho K1) có hàng HH-0091, ĐVT cơ bản Cái, có thêm ĐVT Thùng hệ số 12\n"
      "Tồn: công ty TPE lô L01 = 10, lô L02 = 15; công ty ENE lô L07 = 5")

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Quản lý Phiếu kiểm kê theo vị trí: chứng từ thủ kho lập để ghi nhận SỐ THỰC KIỂM của từng lô hàng "
     "tại từng vị trí, so với số tồn trên hệ thống.\n"
     "Phiếu thường được lập từ một Kế hoạch kiểm kê theo vị trí đang ở trạng thái Đang kiểm (lấy sẵn phạm vi, "
     "danh sách hàng và hội đồng kiểm kê), nhưng cũng có thể lập độc lập.\n"
     "Luồng: thủ kho lập phiếu, gửi, nhập kết quả kèm file biên bản, Ban kiểm soát duyệt hoặc không duyệt. "
     "Nếu có hàng THIẾU, người xử lý đánh dấu Tổng kiểm kê hoặc tạo phiếu điều chuyển vị trí rồi bấm Hoàn "
     "thành.\n"
     "Người dùng làm được: xem danh sách, lọc, tạo (Lưu / Lưu & Gửi), sửa, xóa khi còn nháp, nhập kết quả, "
     "duyệt, không duyệt, xử lý, in và xuất Excel từng phiếu hoặc cả danh sách."),

    ("2. Đối tượng được tính / hiển thị",
     "Phiếu có 5 trạng thái hiển thị:\n"
     "- Đang tạo (nhãn ĐỎ): vừa bấm Lưu, còn sửa / xóa được.\n"
     "- Đang kiểm (nhãn VÀNG): đã bấm Lưu & Gửi, hoặc bị Không duyệt trả về; người lập nhập kết quả.\n"
     "- Chờ duyệt kết quả (nhãn VÀNG): người lập đã bấm Lưu kết quả.\n"
     "- Chờ xử lý (nhãn VÀNG): Ban kiểm soát đã duyệt và có ít nhất 1 dòng THIẾU.\n"
     "- Hoàn thành (nhãn XANH): duyệt mà không có dòng thiếu; hoặc phiếu điều chuyển vị trí đã chuyển đủ mọi dòng thiếu (tự chuyển); hoặc người xử lý bấm Hoàn thành.\n"
     "Phạm vi phiếu nhìn thấy phụ thuộc lối vào:\n"
     "- Lối vào từ menu (Kho > Kiểm kho > Theo vị trí > Kiểm kê theo vị trí): theo quyền xem ở mục 7, luôn "
     "ẩn phiếu Đang tạo của người khác.\n"
     "- Lối vào từ Trang chủ > tab \"Phê duyệt\" > thẻ \"Kiểm kê\" > ô \"Kiểm kê vị trí chờ duyệt\": mọi phiếu "
     "Chờ duyệt kết quả (cần quyền Ban kiểm soát duyệt kết quả kiểm kê).\n"
     "- Lối vào \"Phiếu của tôi\": chỉ phiếu mình lập, gồm cả nháp. Không có mục menu, nhưng hệ thống TỰ CHUYỂN "
     "về đây sau khi bấm Lưu kết quả hoặc Hoàn thành."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu Đang tạo của NGƯỜI KHÁC bị ẩn ở lối vào menu.\n"
     "- Menu bánh răng: Sửa, Xóa chỉ khi Đang tạo và là người lập; \"Nhập kết quả\" chỉ khi Đang kiểm và là "
     "người lập; \"Duyệt kết quả\" chỉ khi Chờ duyệt kết quả và có quyền Ban kiểm soát; \"Xử lý\" chỉ khi Chờ "
     "xử lý và có quyền Xử lý phiếu kiểm kê vị trí. In, Xuất excel luôn có.\n"
     "- Nút Tạo mới hiện với mọi người, nhưng người không có quyền Lập phiếu kiểm kê kho theo vị trí bấm vào "
     "sẽ gặp trang không tìm thấy.\n"
     "- Ô Kho vật lý trên màn nhập chỉ liệt kê các kho mà người đăng nhập được phân công làm thủ kho.\n"
     "- Bốn cột Thực kiểm, Chênh lệch, Ghi chú, Tổng kiểm kê chỉ hiện khi phiếu đang được nhập kết quả hoặc đã "
     "nhập kết quả. Khối File đính kèm và Ghi chú duyệt chỉ có ở màn Chi tiết.\n"
     "- Màn hình KHÔNG có chức năng Hủy phiếu, KHÔNG có Nhập Excel kết quả."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Hai ô \"Từ ngày\" và \"Đến ngày\" lọc theo cột \"Ngày kiểm kê\", cả hai đầu mút tính TRỌN NGÀY.\n"
     "Ngày kiểm kê của phiếu lập TỪ KẾ HOẠCH lấy bằng NGÀY LẬP KẾ HOẠCH, không phải ngày lập phiếu. Phiếu lập "
     "độc lập thì lấy ngày lập phiếu. Ô này bị khóa, không sửa được.\n"
     "Không lọc được theo cột Ngày duyệt."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Phần phạm vi giống kế hoạch: 1 Kho vật lý > Nhà > Dãy > Khoang > Vị trí (vị trí tự do hiện ngay dưới "
     "tên kho).\n"
     "Tab \"Vị trí\": Vị trí > Hàng hóa (Tên hàng, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn) > Công ty (kèm "
     "tổng trong ngoặc đỏ) > Lô (kèm SL lô trong ngoặc đỏ) > một hoặc nhiều DÒNG KẾT QUẢ: SL, ĐVT kiểm kê, "
     "Thực kiểm, Chênh lệch, Ghi chú, Tổng kiểm kê.\n"
     "Tab \"Hội đồng kiểm kê\": Thành viên + Chức vụ.\n"
     "Khối \"File đính kèm\" (biên bản kiểm kê) và khối \"Ghi chú duyệt\".\n"
     "Số phiếu: <mã công ty người lập>-KKVT-<số thứ tự 5 chữ số>, ví dụ TPE-KKVT-00042."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Mỗi lô mặc định 1 dòng kết quả theo ĐVT cơ bản, SL = SL lô.\n"
     "- Đổi ĐVT kiểm kê sang đơn vị lớn: SL dòng = phần nguyên của (SL còn lại / hệ số); phần lẻ còn lại tự "
     "tách thành dòng mới theo ĐVT cơ bản. Không đủ 1 đơn vị lớn thì báo \"Số lượng không đủ để quy đổi!\".\n"
     "- Thực kiểm mặc định = SL; Chênh lệch = Thực kiểm - SL (cùng ĐVT của dòng).\n"
     "- Chênh lệch khác 0 thì BẮT BUỘC có Ghi chú. Ô Tổng kiểm kê chỉ được ghi nhận khi Chênh lệch khác 0.\n"
     "- Khi Duyệt: chỉ cần 1 dòng Chênh lệch ÂM là phiếu sang Chờ xử lý; không có dòng âm (khớp hoặc thừa) "
     "thì Hoàn thành ngay và kế hoạch gốc cũng Hoàn thành. Hàng THỪA không phát sinh bước xử lý.\n"
     "- Khi Xử lý: còn dòng thiếu chưa tích Tổng kiểm kê và chưa điều chuyển đủ số thiếu thì chỉ có nút \"Tạo "
     "phiếu điều chuyển vị trí\"; hết dòng như vậy thì có nút \"Hoàn thành\".\n"
     "- Điều chuyển đủ số thiếu của MỌI dòng thì phiếu và kế hoạch gốc TỰ chuyển Hoàn thành, không cần bấm nút.\n"
     "- Một vị trí chỉ 1 lần; một nhân viên chỉ 1 dòng trong hội đồng."),

    ("7. Phân quyền cấp",
     "Các quyền thuộc nhóm \"Kiểm kê kho\" (phân hệ Kho):\n"
     "- \"Xem phiếu kiểm kê vị trí - theo tổng công ty\": lối vào menu xem phiếu mọi công ty; khối lọc có ô "
     "Công ty, Phòng ban.\n"
     "- \"Xem phiếu kiểm kê vị trí - theo công ty\": xem phiếu công ty mình và phiếu mình lập; có ô Phòng ban.\n"
     "- \"Lập phiếu kiểm kê kho theo vị trí\": mở được màn Tạo mới; lập phiếu từ kế hoạch khi là thủ kho kho đó.\n"
     "- \"Ban kiểm soát duyệt kết quả kiểm kê\": thấy ô chờ duyệt ở Trang chủ, nhận thông báo, Duyệt kết quả / "
     "Không duyệt.\n"
     "- \"Xử lý phiếu kiểm kê vị trí\": nhận thông báo, tích Tổng kiểm kê, tạo phiếu điều chuyển vị trí, Hoàn "
     "thành.\n"
     "Không có quyền xem: chỉ thấy phiếu của mình. Nhập kết quả chỉ NGƯỜI LẬP làm được.\n"
     "Xem chi tiết, In, Xuất excel KHÔNG kiểm tra quyền.\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API (bỏ qua giao diện) dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- Dòng dưới bảng: \"Hiển thị a đến b của N\", N là tổng phiếu khớp bộ lọc trong phạm vi lối vào.\n"
     "- Ô \"Kiểm kê vị trí chờ duyệt\" ở Trang chủ = số phiếu Chờ duyệt kết quả của CÔNG TY người đăng nhập. "
     "Lưu ý: danh sách mở ra khi bấm ô lại lấy phiếu của MỌI công ty, nên N có thể lớn hơn số trên ô.\n"
     "- Cột Chênh lệch tính tự động theo công thức ở mục 6, không nhập tay.\n"
     "- STT đánh liên tục qua các trang."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất:\n"
     "- Ô Thực kiểm hiển thị số kiểu Anh: dấu PHẨY ngăn cách hàng nghìn (1,250). Gõ \"2,5\" sẽ được hiểu là 25.\n"
     "- Thiếu Ghi chú ở dòng có chênh lệch chỉ báo \"Thao tác thất bại!\", KHÔNG chỉ ra dòng nào.\n"
     "- Ngày kiểm kê của phiếu lập từ kế hoạch = ngày lập kế hoạch.\n"
     "- Ô lọc Công ty, Phòng ban HIỆN nhưng KHÔNG có tác dụng lọc.\n"
     "- In / Xuất excel DANH SÁCH có thể lỗi khi trong kết quả có phiếu lập độc lập (không gắn kế hoạch).\n"
     "- Nút X trên file đã đính kèm ở màn Chi tiết không xóa được file.\n"
     "- Màn Chi tiết vẫn hiện nút thêm / bớt thành viên nhưng thay đổi KHÔNG được lưu.\n"
     "- Sửa xong vẫn báo \"Tạo thành công\"; thông báo lỗi dưới ô bằng TIẾNG ANH.\n"
     "- Kế hoạch gốc chuyển \"Đã lập kiểm kê\" ngay khi phiếu được Lưu nháp; xóa phiếu không trả kế hoạch về; "
     "phiếu Chờ xử lý hoàn tất bằng nút Hoàn thành (sau khi tích Tổng kiểm kê) thì kế hoạch KHÔNG lên Hoàn thành (đi đường điều chuyển đủ thì có).\n"
     "- Bản In: không có cột Chênh lệch, Tổng kiểm kê; Thực kiểm tô ĐỎ khi lệch; ngày ký cuối trang = Ngày kiểm "
     "kê, không phải ngày in.\n"
     "- Hệ thống ghi nhớ bộ lọc và trang đang xem theo từng lối vào, trên từng trình duyệt."),
]


ROLE_TCS = [
    ("00", "Không có quyền nào: chỉ thấy phiếu mình lập, không mở được Tạo mới", "P0",
     "NV-A không có quyền nào ở mục 7; NV-A từng lập 2 phiếu (trước khi bị thu quyền)\n"
     "Công ty có thêm 15 phiếu của người khác",
     "1. Đăng nhập NV-A\n"
     "2. " + MENU + "\n"
     "3. Đọc số tổng\n"
     "4. Bấm Tạo mới",
     "Tài khoản: NV-A",
     "- Vào được danh sách, tổng = 2, đều do NV-A lập\n"
     "- Nút Tạo mới VẪN hiện, nhưng bấm vào thì hiện trang không tìm thấy"),

    ("01", "Xem theo tổng công ty thấy phiếu mọi công ty", "P0",
     "Tài khoản B chỉ có quyền \"Xem phiếu kiểm kê vị trí - theo tổng công ty\"\n"
     "Công ty 1 có 8 phiếu đã gửi, công ty 3 có 3 phiếu đã gửi; người khác có 2 phiếu Đang tạo",
     "1. Đăng nhập B, mở màn từ menu\n"
     "2. Đọc tổng, bấm Bộ lọc",
     "Quyền: Xem phiếu kiểm kê vị trí - theo tổng công ty",
     "- Tổng = 11 (cộng phiếu B tự lập nếu có)\n"
     "- 2 phiếu Đang tạo của người khác KHÔNG hiện\n"
     "- Khối lọc có ô Công ty và Phòng ban"),

    ("02", "Xem theo công ty chỉ thấy công ty mình và phiếu mình lập", "P0",
     "Tài khoản C chỉ có quyền \"Xem phiếu kiểm kê vị trí - theo công ty\", thuộc công ty 3\n"
     "Công ty 3 có 3 phiếu đã gửi, công ty 1 có 8",
     "1. Đăng nhập C, mở màn từ menu\n"
     "2. Đọc tổng, bấm Bộ lọc",
     "Quyền: Xem phiếu kiểm kê vị trí - theo công ty",
     "- Tổng = 3 (cộng phiếu C tự lập)\n"
     "- Khối lọc có ô Phòng ban, KHÔNG có ô Công ty"),

    ("03", "Quyền Lập phiếu mở được Tạo mới, Kho vật lý chỉ có kho mình làm thủ kho", "P0",
     "TK1 có quyền \"Lập phiếu kiểm kê kho theo vị trí\", là thủ kho K1 và K2; hệ thống có 6 kho",
     "1. Đăng nhập TK1, mở màn từ menu, bấm Tạo mới\n"
     "2. Mở ô Kho vật lý",
     "—",
     "- Mở được màn tạo, tiêu đề \"Kiểm kê theo vị trí\"\n"
     "- Ô Kho vật lý chỉ có K1, K2"),

    ("04", "Ban kiểm soát thấy ô chờ duyệt và nút Duyệt / Không duyệt", "P0",
     "BKS có quyền \"Ban kiểm soát duyệt kết quả kiểm kê\", thuộc công ty 1\n"
     "Công ty 1 có 2 phiếu Chờ duyệt kết quả",
     "1. Đăng nhập BKS, ở Trang chủ bấm tab \"Phê duyệt\", đọc ô \"Kiểm kê vị trí chờ duyệt\"\n"
     "2. Bấm vào ô, bấm bánh răng 1 phiếu > \"Duyệt kết quả\"",
     "—",
     "- Ô hiện số 2\n"
     "- Màn Chi tiết có nút \"Duyệt kết quả\", \"Không duyệt\"\n"
     "- Ô \"Ghi chú duyệt\" nhập được"),

    ("05", "Không có quyền Ban kiểm soát thì không duyệt được", "P0",
     "C có quyền xem theo công ty, KHÔNG có quyền Ban kiểm soát; phiếu KK-1 đang Chờ duyệt kết quả",
     "1. C mở màn từ menu, bấm bánh răng KK-1\n"
     "2. Bấm Số phiếu KK-1",
     "—",
     "- Bánh răng không có \"Duyệt kết quả\"\n"
     "- Màn Chi tiết không có nút Duyệt kết quả / Không duyệt; ô Ghi chú duyệt bị khóa\n"
     "- Không có ô chờ duyệt ở Trang chủ"),

    ("06", "Quyền Xử lý thấy nút Xử lý và thao tác được ở phiếu Chờ xử lý", "P0",
     "XL có quyền \"Xử lý phiếu kiểm kê vị trí\" và quyền xem theo công ty; KK-2 Chờ xử lý có 1 dòng thiếu 2 cái",
     "1. XL mở màn từ menu, bấm bánh răng KK-2 > \"Xử lý\"",
     "—",
     "- Ô Tổng kiểm kê ở các dòng tích được\n"
     "- Có nút \"Tạo phiếu điều chuyển vị trí\""),

    ("07", "Không có quyền Xử lý thì phiếu Chờ xử lý chỉ xem", "P1",
     "C có quyền xem theo công ty, KHÔNG có quyền Xử lý; KK-2 Chờ xử lý",
     "1. C mở Chi tiết KK-2",
     "—",
     "- Ô Tổng kiểm kê bị khóa\n"
     "- Không có nút Tạo phiếu điều chuyển vị trí, Hoàn thành"),

    ("08", "Chỉ người lập mới nhập được kết quả", "P0",
     "KK-3 Đang kiểm do TK1 lập; TK5 cũng là thủ kho K1, có quyền Lập phiếu và quyền xem theo công ty",
     "1. TK1 bấm bánh răng KK-3\n"
     "2. TK5 bấm bánh răng KK-3, rồi mở Chi tiết",
     "—",
     "- TK1 thấy \"Nhập kết quả\"\n"
     "- TK5 không thấy \"Nhập kết quả\"; màn Chi tiết của TK5 không có cột Thực kiểm, không có nút Lưu kết quả"),

    ("09", "Chỉ người lập mới thấy Sửa / Xóa phiếu nháp", "P1",
     "KK-4 Đang tạo do TK1 lập",
     "1. TK1 bấm bánh răng KK-4\n"
     "2. B (quyền tổng công ty) tìm KK-4",
     "—",
     "- TK1 thấy Sửa, Xóa, In, Xuất excel\n"
     "- B không tìm thấy KK-4"),

    ("10", "Xem chi tiết, In, Xuất excel không kiểm tra quyền", "P1",
     "NV-X công ty 3 không có quyền nào; nhận được đường dẫn Chi tiết phiếu KK-1 của công ty 1",
     "1. NV-X dán đường dẫn vào trình duyệt\n"
     "2. Thử In, Xuất excel",
     "—",
     "- Theo code hiện tại: mở được, In và Xuất excel được\n"
     "- Lưu ý: điểm hở cô lập dữ liệu — ghi Failed nếu nghiệp vụ yêu cầu chặn"),

    ("11", "Gọi thẳng chức năng Lưu phiếu mới khi không có quyền Lập phiếu", "P0",
     "NV-A không có quyền Lập phiếu kiểm kê kho theo vị trí",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Lưu phiếu kiểm kê mới, bỏ qua giao diện, với dữ liệu hợp lệ",
     "—",
     "- Mong đợi: hệ thống từ chối, báo không có quyền\n"
     "- Lưu ý: bước lưu hiện chỉ chặn ở màn Tạo mới, không chặn khi gọi thẳng — nếu tạo được phiếu thì ghi Failed"),

    ("12", "Gọi thẳng chức năng Lưu kết quả trên phiếu của người khác", "P0",
     "KK-3 Đang kiểm do TK1 lập; tester đăng nhập TK5",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Lưu kết quả của KK-3\n"
     "2. TK1 mở lại KK-3",
     "—",
     "- Hệ thống từ chối (Lưu ý: nội dung thông báo có thể trống)\n"
     "- KK-3 giữ nguyên Đang kiểm, không có kết quả mới"),

    ("13", "Gọi thẳng chức năng Duyệt khi không có quyền Ban kiểm soát", "P0",
     "KK-1 Chờ duyệt kết quả; tester đăng nhập C",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Duyệt, rồi Không duyệt của KK-1",
     "—",
     "- Cả hai đều báo \"Không có quyền\"\n"
     "- KK-1 giữ nguyên trạng thái"),

    ("14", "Gọi thẳng chức năng Lưu sửa trên phiếu đã gửi hoặc của người khác", "P1",
     "KK-1 Chờ duyệt kết quả do TK1 lập; tester đăng nhập TK5",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Lưu sửa của KK-1, gửi trạng thái Đang tạo",
     "—",
     "- Mong đợi: hệ thống từ chối, KK-1 giữ nguyên\n"
     "- Lưu ý: bước lưu sửa hiện KHÔNG kiểm tra người lập / trạng thái, còn xóa sạch kết quả đã nhập — nếu bị "
     "đổi thì ghi Failed"),

    ("15", "Gọi thẳng chức năng Hoàn thành khi còn dòng thiếu chưa xử lý", "P1",
     "KK-2 Chờ xử lý, 1 dòng thiếu 2 cái chưa tích Tổng kiểm kê, chưa điều chuyển; tester là XL",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Hoàn thành của KK-2",
     "—",
     "- Mong đợi: hệ thống chặn vì còn dòng thiếu chưa xử lý\n"
     "- Lưu ý: code hiện tại không kiểm tra, KK-2 có thể sang Hoàn thành — nếu vậy ghi Failed"),
]
