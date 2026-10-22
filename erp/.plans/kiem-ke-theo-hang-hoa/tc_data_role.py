# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Kiem ke theo hang hoa' (phieu kiem ke)."""

MENU = "Mở menu Kho > nhóm \"Kiểm kho\" > cột \"Theo vị trí\" > bấm \"Kiểm kê theo hàng hóa\""
HOME = ("Ở Trang chủ bấm tab \"Phê duyệt\" > thẻ \"Kiểm kê\" > bấm ô \"Kiểm kê hàng hóa chờ duyệt\"")

# Du lieu mau dung chung
H1 = ("Hàng H1 (ĐVT cơ bản Cái, có thêm ĐVT Thùng hệ số 12) ở kho K1:\n"
      "vị trí P1: công ty TPE lô L01 = 30; vị trí P2: công ty TPE lô L02 = 10")

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Quản lý Phiếu kiểm kê theo hàng hóa: chứng từ thủ kho lập để đếm thực tế từng MẶT HÀNG trong một "
     "hoặc nhiều kho vật lý, chi tiết tới Vị trí > Công ty > Lô, so với tồn trên hệ thống.\n"
     "Phiếu đi qua các bước: lập phiếu (tự do, hoặc lấy từ Kế hoạch kiểm kê theo hàng hóa / Kế hoạch "
     "tổng kiểm kê hàng hóa) > người lập cập nhật kết quả Thực kiểm kèm file kết quả > Ban kiểm soát "
     "Duyệt hoặc Không duyệt > nếu có chênh lệch thì người xử lý tạo phiếu điều chuyển vị trí, phiếu "
     "nhập kho / xuất kho điều chỉnh kiểm kê > phiếu Hoàn thành.\n"
     "Người dùng làm được: xem danh sách, lọc, tạo (Lưu nháp / Lưu & gửi), sửa, xóa khi còn nháp, cập "
     "nhật kết quả, duyệt, xử lý, in và xuất Excel từng phiếu hoặc cả danh sách."),

    ("2. Đối tượng được tính / hiển thị",
     "Phiếu có 7 trạng thái (chỉ Hoàn thành nhãn XANH, còn lại nhãn ĐỎ):\n"
     "- Đang tạo: vừa bấm Lưu, còn sửa / xóa được.\n"
     "- Đang kiểm: đã bấm Lưu & gửi, chờ người lập nhập Thực kiểm.\n"
     "- Chờ KT duyệt: người lập đã bấm Gửi duyệt.\n"
     "- Không duyệt: Ban kiểm soát từ chối, người lập nhập lại kết quả.\n"
     "- Chờ xử lý: được duyệt và có ít nhất 1 dòng chênh lệch.\n"
     "- Đang xử lý: đã có chứng từ xử lý nhưng chưa xử lý đủ mọi dòng chênh lệch.\n"
     "- Hoàn thành: duyệt mà không chênh lệch, hoặc mọi dòng chênh lệch đã được xử lý đủ số.\n"
     "Phạm vi phiếu nhìn thấy phụ thuộc lối vào:\n"
     "- Lối vào từ menu (Kho > Kiểm kho > Theo vị trí > Kiểm kê theo hàng hóa): theo quyền xem ở mục 7, "
     "luôn ẩn phiếu Đang tạo của người khác.\n"
     "- Lối vào Trang chủ > tab \"Phê duyệt\" > thẻ \"Kiểm kê\" > ô \"Kiểm kê hàng hóa chờ duyệt\": phiếu "
     "Chờ KT duyệt (cần quyền Ban kiểm soát duyệt kết quả kiểm kê).\n"
     "- Lối vào \"Phiếu của tôi\" (không có mục menu; hệ thống tự đưa về đây sau khi Gửi duyệt, Duyệt, "
     "Không duyệt): chỉ phiếu do chính mình lập."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu Đang tạo của NGƯỜI KHÁC bị ẩn ở lối vào menu, kể cả với quyền tổng công ty.\n"
     "- Sửa / Xóa: chỉ khi phiếu Đang tạo VÀ người xem là người lập.\n"
     "- Cập nhật kết quả: chỉ khi phiếu Đang kiểm hoặc Không duyệt VÀ người xem là người lập.\n"
     "- Duyệt: chỉ khi phiếu Chờ KT duyệt VÀ có quyền Ban kiểm soát duyệt kết quả kiểm kê.\n"
     "- Xử lý: chỉ khi phiếu Chờ xử lý / Đang xử lý VÀ có quyền Xử lý phiếu kiểm kê hàng hóa.\n"
     "- In, Xuất excel luôn hiện.\n"
     "- Lô có tồn bằng 0 không hiện trong bảng hàng hóa.\n"
     "- Phiếu lập từ Kế hoạch kiểm kê theo hàng hóa KHÔNG cho thêm / bớt hàng, KHÔNG cho đổi kho.\n"
     "- Cột Thực kiểm, Chênh lệch, Ghi chú dòng, tab \"Hàng thừa khác\" và ô File kết quả chỉ hiện từ "
     "bước Cập nhật kết quả trở đi.\n"
     "- Hàng thừa khác KHÔNG có trên bản In và KHÔNG được tính vào bước Xử lý."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Hai ô \"Từ ngày\" và \"Đến ngày\" lọc theo NGÀY LẬP phiếu (cột \"Ngày kiểm kê\" trên lưới), tính "
     "trọn hai đầu.\n"
     "Ô \"Ngày kiểm kê\" trên màn nhập bị khóa: là ngày lập; sửa và Lưu lại thì ghi thành ngày sửa. Bản In "
     "danh sách in Ngày kiểm kê theo ngày sửa này, lưới vẫn hiện ngày lập ban đầu."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Khung \"Thông tin chung\": Kế hoạch kiểm kê (chọn qua cửa sổ, có nút xóa), Ngày kiểm kê (khóa), "
     "Kho (nhiều kho vật lý của công ty mình), Công ty thuê kho (tự chọn hết theo kho), Ghi chú; từ bước "
     "cập nhật kết quả có thêm File kết quả.\n"
     "Tab \"Hàng hóa\": Hàng (Tên, Model, Mã, ĐVT, SL tồn kho) > Vị trí (kèm SL tồn của vị trí) > Công "
     "ty > Lô (Tồn theo lô) > ĐVT kiểm kê > Thực kiểm > Chênh lệch > Ghi chú.\n"
     "Tab \"Hàng thừa khác\": hàng có ngoài danh sách (chọn hàng có sẵn hoặc gõ tên mới + ĐVT) > Vị trí > "
     "Thực kiểm.\n"
     "Tab \"Hội đồng kiểm kê\": Thành viên + Chức vụ.\n"
     "Khung \"Ghi chú duyệt\" ở màn Chi tiết: chỉ người duyệt nhập được.\n"
     "Số phiếu: <mã công ty người lập>.KKK-<5 chữ số>, ví dụ TPE.KKK-00042."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Chọn ĐVT kiểm kê lớn hơn (ví dụ Thùng hệ số 12) cho lô tồn 30 Cái: dòng tách thành 2 Thùng và tự "
     "thêm dòng 6 Cái cho phần lẻ.\n"
     "- Chênh lệch của dòng = Thực kiểm - SL của dòng (theo ĐVT kiểm kê của dòng đó).\n"
     "- Ở bước Đang kiểm, Thực kiểm mặc định bằng SL tồn (chênh lệch 0); để trống ô Thực kiểm được hiểu "
     "là 0.\n"
     "- Một hàng chỉ được chọn 1 lần (báo \"Hàng hóa đã được chọn\").\n"
     "- Bước Xử lý xét TỔNG chênh lệch của từng hàng:\n"
     "  + Tổng bằng 0 nhưng có dòng thiếu (lệch vị trí): cần Phiếu điều chuyển vị trí.\n"
     "  + Tổng khác 0 và có dòng thừa: cần phiếu nhập kho điều chỉnh kiểm kê.\n"
     "  + Tổng khác 0 và có dòng thiếu: cần phiếu xuất kho điều chỉnh kiểm kê.\n"
     "- Mỗi loại chứng từ xử lý chỉ tạo được 1 lần cho 1 phiếu kiểm kê."),

    ("7. Phân quyền cấp",
     "Các quyền thuộc nhóm \"Kiểm kê kho\" (phân hệ Kho):\n"
     "- \"Xem phiếu kiểm kê hàng hóa - theo tổng công ty\": lối vào menu xem phiếu MỌI công ty, khối lọc có "
     "ô Công ty, Phòng ban; ô lọc Kho liệt kê kho mọi công ty.\n"
     "- \"Xem phiếu kiểm kê hàng hóa - theo công ty\": xem phiếu công ty mình và phiếu mình lập.\n"
     "- \"Lập phiếu kiểm kê kho theo hàng hóa\": được lấy dữ liệu từ Kế hoạch kiểm kê theo hàng hóa.\n"
     "- \"Ban kiểm soát duyệt kết quả kiểm kê\": ô chờ duyệt ở Trang chủ, nút Duyệt / Không duyệt.\n"
     "- \"Xử lý phiếu kiểm kê hàng hóa\": nút Xử lý, nhận thông báo khi phiếu được duyệt có chênh lệch.\n"
     "Không có quyền nào: vẫn Tạo mới được (phiếu tự do), chỉ thấy phiếu của mình.\n"
     "Xem chi tiết, In, Xuất excel KHÔNG kiểm tra quyền.\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- Dòng dưới bảng \"Hiển thị a đến b của N\": N là tổng phiếu khớp bộ lọc trong phạm vi lối vào.\n"
     "- Ô \"Kiểm kê hàng hóa chờ duyệt\" ở Trang chủ = số phiếu Chờ KT duyệt của CÔNG TY người đăng nhập; "
     "ô ẩn khi bằng 0.\n"
     "- \"SL tồn kho\" của hàng = tổng SL tồn của các vị trí; số đỏ cạnh mã vị trí là tồn của vị trí đó.\n"
     "- STT đánh liên tục qua các trang."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- Cảnh báo \"còn phiếu nhập / xuất kho chưa xong\" KHÔNG bao giờ chặn Lưu & gửi.\n"
     "- Cột \"Ngày duyệt\" luôn trống dù phiếu đã được duyệt.\n"
     "- Ô chờ duyệt ở Trang chủ chỉ đếm công ty mình nhưng danh sách mở ra gồm phiếu chờ duyệt của MỌI "
     "công ty; người duyệt duyệt được phiếu công ty khác.\n"
     "- Gửi duyệt xong, thông báo gửi cho nhóm \"Kế toán kho\", không gửi theo quyền Ban kiểm soát.\n"
     "- Nút xử lý ghi \"Tạo phiếu nhập kho điều chuyển\" / \"Tạo phiếu xuất kho điều chuyển\" nhưng thực "
     "chất mở phiếu nhập / xuất kho ĐIỀU CHỈNH KIỂM KÊ.\n"
     "- Cửa sổ chọn Kế hoạch kiểm kê gần như không bao giờ hiện Kế hoạch tổng kiểm kê (chỉ hiện kế hoạch "
     "có từ ngày và đến ngày cùng là hôm nay).\n"
     "- Sửa phiếu lập từ Kế hoạch tổng kiểm kê luôn báo \"Hàng hóa đã lập phiếu kiểm kê\".\n"
     "- Bản In / Excel danh sách: phiếu không gắn kế hoạch có thể hiện mã kế hoạch của dòng phía trên.\n"
     "- Ô Thực kiểm dùng dấu phẩy làm dấu phân cách hàng nghìn: gõ \"2,5\" được hiểu là 25.\n"
     "- Thông báo lỗi kiểm tra dữ liệu hiển thị bằng TIẾNG ANH.\n"
     "- Xóa phiếu lập từ kế hoạch không trả kế hoạch về Đang kiểm."),
]


ROLE_TCS = [
    ("00", "Tài khoản không có quyền nào chỉ thấy phiếu do mình lập", "P0",
     "NV-A không có quyền xem nào; NV-A lập 3 phiếu (1 Đang tạo, 2 Đang kiểm)\n"
     "Công ty có thêm 15 phiếu đã gửi của người khác",
     "1. Đăng nhập NV-A\n"
     "2. " + MENU + "\n"
     "3. Đọc số tổng, bấm Bộ lọc",
     "Tài khoản: NV-A",
     "- Tổng = 3, mọi dòng Người lập là NV-A\n"
     "- Nút Tạo mới vẫn hiện\n"
     "- Khối lọc không có ô Công ty, Phòng ban"),

    ("01", "Quyền xem theo tổng công ty thấy phiếu mọi công ty", "P0",
     "Tài khoản B có quyền \"Xem phiếu kiểm kê hàng hóa - theo tổng công ty\"\n"
     "Công ty 1 có 8 phiếu đã gửi, công ty 3 có 5 phiếu đã gửi; người khác có 2 phiếu Đang tạo",
     "1. Đăng nhập B, mở màn từ menu\n"
     "2. Đọc số tổng, bấm Bộ lọc",
     "Quyền: Xem phiếu kiểm kê hàng hóa - theo tổng công ty",
     "- Tổng = 13\n"
     "- 2 phiếu Đang tạo của người khác không hiện\n"
     "- Khối lọc có ô Công ty và Phòng ban"),

    ("02", "Quyền xem theo công ty thấy phiếu công ty mình và phiếu mình lập", "P0",
     "Tài khoản C có quyền \"Xem phiếu kiểm kê hàng hóa - theo công ty\", thuộc công ty 3\n"
     "Công ty 3 có 5 phiếu đã gửi; C từng lập 1 phiếu khi ở công ty 1",
     "1. Đăng nhập C, mở màn từ menu\n"
     "2. Đọc số tổng",
     "Quyền: Xem phiếu kiểm kê hàng hóa - theo công ty",
     "- Tổng = 6 (5 + 1)\n"
     "- Khối lọc có ô Phòng ban, không có ô Công ty"),

    ("03", "Người lập thấy Sửa, Xóa trên phiếu nháp; người khác không thấy phiếu", "P0",
     "NV-A lập phiếu KK-1 Đang tạo; NV-B có quyền xem theo tổng công ty",
     "1. NV-A bấm bánh răng ở KK-1\n"
     "2. NV-B tìm KK-1 bằng ô Mã phiếu",
     "—",
     "- NV-A thấy: Sửa, Xóa, In, Xuất excel\n"
     "- NV-B không tìm thấy KK-1"),

    ("04", "Chỉ người lập mới có Cập nhật kết quả", "P0",
     "KK-2 Đang kiểm do NV-A lập; NV-B có quyền xem theo tổng công ty và quyền Ban kiểm soát",
     "1. NV-A bấm bánh răng ở KK-2\n"
     "2. NV-B bấm bánh răng ở KK-2, mở Chi tiết KK-2",
     "—",
     "- NV-A thấy \"Cập nhật kết quả\"\n"
     "- NV-B chỉ thấy In, Xuất excel; màn Chi tiết không có nút Gửi duyệt, không có ô Thực kiểm nhập được"),

    ("05", "Quyền Ban kiểm soát thấy ô chờ duyệt và nút Duyệt", "P0",
     "BKS có quyền \"Ban kiểm soát duyệt kết quả kiểm kê\", thuộc công ty 1\n"
     "Công ty 1 có 2 phiếu Chờ KT duyệt",
     "1. Đăng nhập BKS\n"
     "2. " + HOME + "\n"
     "3. Bấm bánh răng ở một phiếu, chọn Duyệt",
     "—",
     "- Ô hiện số 2\n"
     "- Menu bánh răng có \"Duyệt\"\n"
     "- Màn Chi tiết có nút Duyệt, Không duyệt; ô Ghi chú duyệt nhập được"),

    ("06", "Không có quyền Ban kiểm soát thì không duyệt được", "P0",
     "NV-B có quyền xem theo tổng công ty, không có quyền Ban kiểm soát; KK-3 Chờ KT duyệt",
     "1. Đăng nhập NV-B, mở Chi tiết KK-3\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Duyệt KK-3",
     "—",
     "- Bước 1: không có nút Duyệt / Không duyệt, ô Ghi chú duyệt bị khóa\n"
     "- Bước 2: báo \"Bạn không có quyền duyệt phiếu này\", KK-3 vẫn Chờ KT duyệt"),

    ("07", "Quyền Xử lý thấy nút Xử lý trên phiếu Chờ xử lý", "P0",
     "XL có quyền \"Xử lý phiếu kiểm kê hàng hóa\" và quyền xem theo công ty; KK-4 Chờ xử lý",
     "1. Đăng nhập XL, bấm bánh răng ở KK-4\n"
     "2. Bấm Xử lý",
     "—",
     "- Menu có \"Xử lý\"\n"
     "- Màn Chi tiết hiện nút tạo chứng từ xử lý phù hợp (xem nhóm VII)"),

    ("08", "Không có quyền Xử lý thì không thấy nút xử lý", "P1",
     "NV-B không có quyền Xử lý; KK-4 Chờ xử lý",
     "1. Đăng nhập NV-B, mở Chi tiết KK-4",
     "—",
     "- Không có nút \"Tạo phiếu điều chuyển vị trí\", \"Tạo phiếu nhập kho điều chuyển\", \"Tạo phiếu "
     "xuất kho điều chuyển\""),

    ("09", "Lấy dữ liệu từ Kế hoạch cần quyền Lập phiếu", "P0",
     "NV-A không có quyền \"Lập phiếu kiểm kê kho theo hàng hóa\"; kế hoạch KH-2 Đang kiểm",
     "1. Đăng nhập NV-A, Tạo mới phiếu kiểm kê\n"
     "2. Bấm nút tìm ở ô Kế hoạch kiểm kê, chọn KH-2",
     "—",
     "- Báo \"Không có quyền\"\n"
     "- Form không được điền dữ liệu kế hoạch"),

    ("10", "Xem chi tiết, In phiếu công ty khác qua đường dẫn", "P1",
     "NV-X công ty 3 không có quyền nào; phiếu KK-5 của công ty 1",
     "1. Đăng nhập NV-X, dán đường dẫn Chi tiết KK-5\n"
     "2. Dán đường dẫn In KK-5",
     "—",
     "- Theo code hiện tại: mở được cả hai\n"
     "- Lưu ý: điểm hở cô lập dữ liệu - ghi Failed nếu nghiệp vụ yêu cầu chặn"),

    ("11", "Gọi thẳng chức năng Gửi kết quả trên phiếu người khác", "P0",
     "KK-2 Đang kiểm do NV-A lập; tester đăng nhập NV-B",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Gửi duyệt kết quả của KK-2",
     "—",
     "- Báo \"Bạn không có quyền cập nhật phiếu này\", KK-2 giữ nguyên"),

    ("12", "Gọi thẳng chức năng Lưu sửa / Xóa phiếu người khác", "P0",
     "KK-1 Đang tạo do NV-A lập; tester đăng nhập NV-B",
     "1. Gọi thẳng chức năng Lưu sửa KK-1\n"
     "2. Gọi thẳng chức năng Xóa KK-1",
     "—",
     "- Bước 1: báo \"Bạn không có quyền sửa phiếu này\"\n"
     "- Bước 2: báo \"Không thể xóa!\"\n"
     "- KK-1 còn nguyên"),
]
