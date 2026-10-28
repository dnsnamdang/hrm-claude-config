# -*- coding: utf-8 -*-
"""Section V - X — trang thai, xoa, in/xuat, rang buoc, co lap & dong thoi, luong dau-cuoi."""

SEC_V = [
    ("001", "Thủ kho bấm Lập phiếu kiểm kê theo vị trí từ kế hoạch", "P0",
     "Kế hoạch KH-3 Đang kiểm của kho K1; TK1 có quyền Lập phiếu, là thủ kho K1",
     "1. TK1 mở danh sách chờ duyệt từ Trang chủ\n"
     "2. Bấm bánh răng của KH-3 > \"Lập phiếu kiểm kê theo vị trí\"",
     "—",
     "- Mở màn tạo Phiếu kiểm kê theo vị trí\n"
     "- Phiếu đã gắn sẵn kế hoạch KH-3, phạm vi và danh sách hàng lấy từ KH-3"),

    ("002", "Lưu phiếu kiểm kê thì kế hoạch chuyển Đã lập kiểm kê", "P0",
     "Như TC_05.001; ô chờ duyệt của TK1 đang là 2",
     "1. Trên màn phiếu kiểm kê, bấm Lưu (lưu nháp)\n"
     "2. Quay lại danh sách kế hoạch, tìm KH-3\n"
     "3. Về Trang chủ đọc ô chờ duyệt",
     "—",
     "- KH-3 chuyển \"Đã lập kiểm kê\" (xanh) NGAY cả khi phiếu kiểm kê mới lưu nháp\n"
     "- Menu bánh răng của KH-3 không còn \"Lập phiếu kiểm kê theo vị trí\"\n"
     "- KH-3 rời khỏi danh sách chờ duyệt, ô ở Trang chủ còn 1"),

    ("003", "Phiếu kiểm kê duyệt không thiếu hàng thì kế hoạch Hoàn thành", "P0",
     "Phiếu kiểm kê KK-1 lập từ KH-3, mọi dòng khớp hoặc thừa, đang chờ Ban kiểm soát duyệt",
     "1. Tài khoản có quyền \"Ban kiểm soát duyệt kết quả kiểm kê\" duyệt KK-1\n"
     "2. Mở danh sách kế hoạch, tìm KH-3",
     "—",
     "- KH-3 chuyển \"Hoàn thành\" (xanh)"),

    ("004", "Hàng thiếu xử lý bằng Tổng kiểm kê thì kế hoạch dừng ở Đã lập kiểm kê", "P1",
     "Phiếu kiểm kê KK-2 lập từ KH-11, có 1 dòng thiếu 2 cái",
     "1. Ban kiểm soát duyệt KK-2 (chuyển sang chờ xử lý)\n"
     "2. Người có quyền \"Xử lý phiếu kiểm kê vị trí\" tích Tổng kiểm kê dòng thiếu, bấm Hoàn thành KK-2\n"
     "3. Tìm KH-11 trên danh sách kế hoạch",
     "—",
     "- Mong đợi: KH-11 chuyển \"Hoàn thành\" khi KK-2 hoàn thành\n"
     "- Lưu ý: code hiện tại KHÔNG cập nhật, KH-11 vẫn \"Đã lập kiểm kê\" — nếu vậy ghi Failed"),

    ("005", "Xóa phiếu kiểm kê nháp không trả kế hoạch về Đang kiểm", "P1",
     "KH-12 đã sang Đã lập kiểm kê do TK1 lưu nháp phiếu kiểm kê KK-3",
     "1. TK1 xóa KK-3\n"
     "2. Tìm KH-12, bấm bánh răng",
     "—",
     "- Mong đợi: KH-12 về Đang kiểm để lập lại phiếu\n"
     "- Lưu ý: code hiện tại KH-12 vẫn \"Đã lập kiểm kê\" và không còn nút lập phiếu — nếu vậy ghi Failed"),

    ("006", "Không có chức năng Hủy kế hoạch trên giao diện", "P2",
     "Có kế hoạch ở cả 4 trạng thái do chính mình lập",
     "1. Bấm bánh răng ở từng kế hoạch\n"
     "2. Mở Chi tiết từng kế hoạch",
     "—",
     "- Không có nút \"Hủy\" ở đâu cả\n"
     "- Kế hoạch đã gửi nhầm chỉ xử lý được qua hỗ trợ kỹ thuật (ghi nhận cho nghiệp vụ)"),

    ("007", "Kế hoạch Đang kiểm khóa sửa và xóa với người lập", "P0",
     "KH-3 Đang kiểm do NV-A lập",
     "1. NV-A bấm bánh răng của KH-3\n"
     "2. Mở Chi tiết KH-3",
     "—",
     "- Không có Sửa, Xóa\n"
     "- Màn Chi tiết chỉ xem"),
]


SEC_VI = [
    ("001", "Xóa kế hoạch nháp", "P0",
     "KH-10 Đang tạo do NV-A lập; danh sách đang ở trang 2",
     "1. Bấm bánh răng của KH-10 > Xóa\n"
     "2. Quan sát hộp xác nhận\n"
     "3. Bấm \"Xác nhận\"",
     "—",
     "- Hộp tiêu đề \"Xác nhận xóa!\", nội dung \"Bạn chắc chắn muốn xóa bản ghi này?\", 2 nút Xác nhận và "
     "Hủy\n"
     "- Sau Xác nhận: thông báo \"Xóa thành công!\", KH-10 biến mất\n"
     "- Vẫn ở đúng lối vào đang xem"),

    ("002", "Bấm Hủy ở hộp xác nhận", "P1",
     "KH-10 Đang tạo",
     "1. Bấm Xóa, rồi bấm \"Hủy\"",
     "—",
     "- Hộp đóng, KH-10 vẫn còn, trạng thái không đổi"),

    ("003", "Kế hoạch đã gửi không có nút Xóa", "P0",
     "NV-A có kế hoạch Đang kiểm, Đã lập kiểm kê, Hoàn thành",
     "1. Bấm bánh răng từng kế hoạch",
     "—",
     "- Không có Xóa ở cả 3 kế hoạch"),

    ("004", "Xóa xong số phiếu không bị dùng lại", "P2",
     "Kế hoạch mới nhất là TPE-KHKKVT-00130 (Đang tạo)",
     "1. Xóa 00130\n"
     "2. Tạo kế hoạch mới",
     "—",
     "- Kế hoạch mới có số lớn hơn 00130, không lấy lại 00130"),
]


SEC_VII = [
    ("001", "In 1 kế hoạch", "P0",
     "KH-9 kho \"K1 - Kho Hà Nội\", 2 vị trí, hội đồng gồm Nguyễn Văn K và Trần Thị L",
     "1. Bấm bánh răng của KH-9 > In",
     "—",
     "- Mở tab mới, trang khổ ngang\n"
     "- Có đầu trang công ty, tiêu đề \"KẾ HOẠCH KIỂM KÊ THEO VỊ TRÍ\"\n"
     "- Số phiếu, Ngày kiểm kê đúng KH-9, Kho vật lý = Kho Hà Nội\n"
     "- Hội đồng kiểm kê: \"Nguyễn Văn K; Trần Thị L\"\n"
     "- Bảng: STT, Nhà Kho, Vị trí, Tên hàng, Mã hàng, ĐVT, SL tồn, Công ty, Lô, SL, Cộng — số liệu "
     "khớp màn Chi tiết"),

    ("002", "Cột Nhà Kho trên bản In và Excel", "P1",
     "KH-9 có vị trí P1 thuộc nhà N1 của kho K1",
     "1. Mở Chi tiết KH-9, đọc cột Nhà Kho của P1\n"
     "2. In KH-9, đọc cột Nhà Kho của P1",
     "—",
     "- Màn Chi tiết: mã nhà N1\n"
     "- Bản In: mã KHO K1\n"
     "- Bản In không có cột Model, Thương hiệu\n"
     "- Lưu ý: lệch giữa màn hình và bản In, ghi nhận để nghiệp vụ quyết định"),

    ("003", "Xuất excel 1 kế hoạch", "P0",
     "KH-9 như TC_07.001",
     "1. Bấm bánh răng của KH-9 > Xuất excel\n"
     "2. Mở file tải về",
     "—",
     "- Tải về file tên ke_hoach_kiem_ke_theo_vi_tri_<Số phiếu>.xlsx\n"
     "- Nội dung giống bản In: tiêu đề, Số phiếu, Ngày kiểm kê, Kho vật lý, Hội đồng kiểm kê, bảng chi tiết\n"
     "- Cuối file có dòng \"Nhận xét, đánh giá:\" và \"Ngày...Tháng...Năm...\""),

    ("004", "In và Xuất excel kế hoạch nháp", "P2",
     "KH-10 Đang tạo",
     "1. Bấm In, rồi Xuất excel trên KH-10",
     "—",
     "- Cả 2 đều chạy, không bị chặn theo trạng thái"),

    ("005", "In danh sách theo bộ lọc", "P0",
     "Lối vào menu, lọc Kho = K1 ra 4 kế hoạch",
     "1. Bấm nút \"In\" ở hàng nút trên bảng",
     "Kho: K1",
     "- Mở tab mới, bảng có STT, Số phiếu, Ngày kiểm kê, Kho, Người lập, Trạng thái\n"
     "- Đúng 4 dòng, khớp danh sách đang lọc\n"
     "- Ngày tháng năm ở cuối là ngày in"),

    ("006", "Xuất excel danh sách lấy hết, không theo phân trang", "P0",
     "Phạm vi đang xem có 23 kế hoạch, bảng hiện 10 dòng/trang",
     "1. Bấm nút \"Xuất excel\" ở hàng nút trên bảng\n"
     "2. Mở file",
     "—",
     "- File tên danh_sach_ke_hoach_kiem_ke_theo_vi_tri.xlsx\n"
     "- Tiêu đề \"Danh sách kế hoạch kiểm kê theo vị trí\"\n"
     "- Đủ 23 dòng, không chỉ 10 dòng của trang hiện tại"),

    ("007", "In và Xuất excel danh sách từ lối vào chờ duyệt", "P1",
     "TK1 có 2 kế hoạch chờ; TK1 có quyền \"Tổng kiểm kê kho theo vị trí\"",
     "1. Mở lối vào chờ duyệt, bấm In\n"
     "2. Bấm Xuất excel",
     "—",
     "- Cả bản In và Excel chỉ có 2 kế hoạch chờ duyệt, KHÔNG lấy theo phạm vi công ty"),

    ("008", "Tên hàng có ký tự & hiển thị đúng khi In", "P2",
     "KH-13 có hàng tên \"Van bi & khớp nối\"",
     "1. In KH-13\n"
     "2. Xuất excel KH-13",
     "—",
     "- Cả 2 hiện đúng chữ \"Van bi & khớp nối\", file Excel mở được không báo lỗi"),
]


SEC_VIII = [
    ("001", "Lưu khi chưa chọn kho", "P0",
     "Màn Tạo mới, chưa chọn gì",
     "1. Bấm \"Lưu\"",
     "—",
     "- Thông báo vàng \"Tạo thất bại!\"\n"
     "- Chữ đỏ dưới ô Kho vật lý, dưới bảng chi tiết, dưới bảng hội đồng (nội dung tiếng Anh, ví dụ \"The "
     "warehouses field is required.\")\n"
     "- Tab \"Hội đồng kiểm kê\" chuyển đỏ, có dấu chấm than\n"
     "- Vẫn ở màn Tạo mới, không tạo kế hoạch"),

    ("002", "Lưu khi chưa bấm Lấy vị trí", "P0",
     "Đã chọn kho, tích vị trí, có thành viên, CHƯA bấm Lấy vị trí",
     "1. Bấm \"Lưu\"",
     "—",
     "- \"Tạo thất bại!\", chữ đỏ dưới bảng chi tiết (\"The items field is required.\")\n"
     "- Lưu ý: tab \"Vị trí\" KHÔNG chuyển đỏ dù có lỗi — ghi nhận"),

    ("003", "Lưu khi các vị trí đã tích đều không có tồn", "P1",
     "Chỉ tích P3 (tồn 0), bấm Lấy vị trí ra \"Chưa có dữ liệu\"",
     "1. Thêm thành viên, bấm \"Lưu\"",
     "—",
     "- \"Tạo thất bại!\", lỗi dưới bảng chi tiết\n"
     "- Không tạo được kế hoạch rỗng"),

    ("004", "Lưu khi chưa có thành viên", "P0",
     "Đủ kho, vị trí, đã Lấy vị trí; tab Hội đồng trống",
     "1. Bấm \"Lưu & Gửi\"",
     "—",
     "- \"Tạo thất bại!\"\n"
     "- Chữ đỏ dưới bảng hội đồng, tab \"Hội đồng kiểm kê\" chuyển đỏ"),

    ("005", "Dòng thành viên để trống", "P1",
     "Tab Hội đồng có 1 dòng chưa chọn thành viên",
     "1. Bấm \"Lưu\"",
     "—",
     "- Chữ đỏ dưới ô Thành viên và ô Chức vụ của dòng đó"),

    ("006", "Một nhân viên được thêm 2 lần", "P0",
     "Tab Hội đồng: dòng 1 và dòng 2 đều chọn NV-K",
     "1. Bấm \"Lưu\"",
     "Thành viên dòng 1, 2: NV-K",
     "- \"Tạo thất bại!\"\n"
     "- Chữ đỏ báo trùng giá trị dưới ô Thành viên của cả 2 dòng"),

    ("007", "Thành viên chưa được gán vai trò nào", "P1",
     "Nhân viên NV-M đang làm việc nhưng chưa được gán vai trò nào trên hệ thống",
     "1. Thêm dòng, chọn NV-M\n"
     "2. Mở ô Chức vụ, bấm \"Lưu\"",
     "Thành viên: NV-M",
     "- Ô Chức vụ không có lựa chọn nào\n"
     "- Lưu: báo lỗi dưới ô Chức vụ, không lưu được\n"
     "- Lưu ý: phải gán vai trò cho NV-M trước khi đưa vào hội đồng"),

    ("008", "Lô có SL lẻ nhỏ hơn 1", "P1",
     "Vị trí P6 có hàng tính theo mét, lô L09 tồn 0,5",
     "1. Tích P6, Lấy vị trí, thêm thành viên\n"
     "2. Bấm \"Lưu\"",
     "SL lô: 0,5",
     "- \"Tạo thất bại!\", không lưu được\n"
     "- Lưu ý: không có dòng lỗi chỉ rõ lô nào — tester ghi nhận, nghiệp vụ quyết định có cho SL lẻ hay không"),

    ("009", "Đổi kho sau khi đã Lấy vị trí mà không lấy lại", "P0",
     "Đã chọn K1, tích P1, Lấy vị trí, thêm thành viên",
     "1. Đổi Kho vật lý sang K2 (không bấm Lấy vị trí lại)\n"
     "2. Bấm \"Lưu\"",
     "Kho vật lý: K2",
     "- Bảng chi tiết vẫn còn P1 của K1\n"
     "- Bấm Lưu: thông báo đỏ \"Đã có lỗi xảy ra\", KHÔNG tạo kế hoạch nào\n"
     "- Mong đợi tốt hơn: hệ thống báo rõ phải lấy lại vị trí"),

    ("010", "Bỏ tích vị trí sau khi đã Lấy vị trí mà không lấy lại", "P1",
     "Đã tích P1, P2, Lấy vị trí ra 2 vị trí",
     "1. Bỏ tích P2 (không bấm Lấy vị trí)\n"
     "2. Thêm thành viên, bấm \"Lưu\", mở Chi tiết",
     "—",
     "- Kế hoạch vẫn lưu cả P1 và P2 theo bảng chi tiết\n"
     "- Khung Vị trí ở Chi tiết chỉ tích P1\n"
     "- Lưu ý: bảng chi tiết và phạm vi tích bị lệch — người dùng phải bấm Lấy vị trí lại sau mỗi lần đổi"),

    ("011", "Chọn lại Chọn kho kiểm sau khi đã chọn kho", "P2",
     "Đã chọn K1",
     "1. Mở ô Kho vật lý, chọn dòng \"Chọn kho kiểm\"\n"
     "2. Bấm \"Lưu\"",
     "—",
     "- \"Tạo thất bại!\"\n"
     "- Lưu ý: dưới ô Kho vật lý có thể KHÔNG hiện chữ đỏ — ghi nhận"),

    ("012", "Sửa lỗi xong lưu lại được, dữ liệu đã nhập còn nguyên", "P1",
     "Đang ở trạng thái lỗi của TC_08.004",
     "1. Thêm 1 thành viên\n"
     "2. Bấm \"Lưu\"",
     "—",
     "- Kho, vị trí, bảng chi tiết đã nhập trước vẫn còn\n"
     "- Lưu thành công, chữ đỏ biến mất"),

    ("013", "Lỗi kiểm tra trên màn Sửa", "P1",
     "KH-10 Đang tạo",
     "1. Mở Sửa, bớt hết thành viên\n"
     "2. Bấm \"Lưu\"",
     "—",
     "- Thông báo vàng \"Thao tác thất bại!\"\n"
     "- Chữ đỏ dưới bảng hội đồng; KH-10 không bị đổi"),
]


SEC_IX = [
    ("001", "Kế hoạch ghi nhận công ty của người lập", "P0",
     "NV-A thuộc công ty 1 lập và gửi KH-14\n"
     "C có quyền \"Tổng kiểm kê kho theo vị trí\", thuộc công ty 3",
     "1. C mở màn từ menu, tìm KH-14 bằng Mã phiếu",
     "—",
     "- C KHÔNG tìm thấy KH-14"),

    ("002", "Người lập chuyển công ty vẫn thấy kế hoạch cũ", "P2",
     "NV-A lập KH-15 khi ở công ty 1, sau đó chuyển sang công ty 3",
     "1. NV-A mở màn từ menu, tìm KH-15",
     "—",
     "- NV-A vẫn thấy KH-15, Số phiếu vẫn mang tiền tố công ty 1"),

    ("003", "Danh sách chờ duyệt của thủ kho không lọc theo công ty", "P1",
     "TK4 thuộc công ty 3, là thủ kho K1 (kho của công ty 1), có quyền Lập phiếu\n"
     "NV-A công ty 1 gửi KH-16 cho kho K1",
     "1. TK4 xem ô chờ duyệt ở Trang chủ\n"
     "2. Bấm vào ô",
     "—",
     "- KH-16 CÓ trong danh sách chờ của TK4 và có nút Lập phiếu kiểm kê\n"
     "- Nhưng TK4 KHÔNG nhận thông báo (thông báo chỉ gửi người cùng công ty — xem TC_04.021)\n"
     "- Lưu ý: ghi nhận lệch giữa thông báo và danh sách chờ"),

    ("004", "Hai cửa sổ: một bên gửi, một bên vẫn đang sửa", "P0",
     "KH-10 Đang tạo do NV-A lập; NV-A mở màn Sửa KH-10 ở 2 tab",
     "1. Tab 1: bấm \"Lưu & Gửi\"\n"
     "2. Tab 2 (chưa tải lại): bấm \"Lưu\"\n"
     "3. Tải lại danh sách, xem trạng thái KH-10",
     "—",
     "- Mong đợi: tab 2 bị từ chối, KH-10 giữ Đang kiểm\n"
     "- Lưu ý: bước lưu sửa không kiểm tra trạng thái, KH-10 có thể bị kéo về Đang tạo — nếu vậy ghi Failed"),

    ("005", "Hai cửa sổ cùng xóa một kế hoạch", "P2",
     "KH-10 Đang tạo; NV-A mở danh sách ở 2 tab",
     "1. Tab 1 xóa KH-10\n"
     "2. Tab 2 (chưa tải lại) bấm Xóa KH-10, Xác nhận",
     "—",
     "- Mong đợi: báo kế hoạch không còn, không treo trang\n"
     "- Lưu ý: nếu hiện trang lỗi hệ thống thì ghi Failed"),

    ("006", "Hai thủ kho cùng lập phiếu kiểm kê cho một kế hoạch", "P1",
     "KH-3 Đang kiểm kho K1; TK1 và TK5 đều là thủ kho K1, có quyền Lập phiếu",
     "1. TK1 và TK5 cùng mở màn Lập phiếu kiểm kê từ KH-3\n"
     "2. TK1 bấm Lưu, sau đó TK5 bấm Lưu",
     "—",
     "- Mong đợi: chỉ 1 phiếu kiểm kê được tạo cho KH-3, người lưu sau được báo kế hoạch đã có phiếu\n"
     "- Nếu cả 2 phiếu cùng được tạo thì ghi Failed"),

    ("007", "Tồn kho đổi giữa lúc Lấy vị trí và lúc Lưu", "P1",
     "P1 có HH-0091 tồn 30",
     "1. Màn Tạo mới: tích P1, bấm Lấy vị trí (hiện 30)\n"
     "2. Ở cửa sổ khác, xuất kho 5 cái HH-0091 khỏi P1\n"
     "3. Quay lại bấm \"Lưu\" (không lấy lại), mở Chi tiết",
     "—",
     "- Kế hoạch lưu SL tồn = 30 (số lúc bấm Lấy vị trí)\n"
     "- Lưu ý: muốn số mới nhất phải bấm Lấy vị trí lại trước khi lưu"),
]


SEC_X = [
    ("001", "Luồng chuẩn: nháp, gửi, lập phiếu kiểm kê, hoàn thành", "P0",
     "NV-A (công ty 1); TK1 (công ty 1, quyền Lập phiếu, thủ kho K1); BKS có quyền \"Ban kiểm soát duyệt "
     "kết quả kiểm kê\"\n"
     "P1 có HH-0091 tồn 30",
     "1. NV-A tạo kế hoạch kho K1, tích P1, Lấy vị trí, thêm 2 thành viên, bấm Lưu\n"
     "2. NV-A mở Sửa, bấm Lưu & Gửi\n"
     "3. TK1 bấm thông báo, mở kế hoạch; vào danh sách chờ duyệt, bấm Lập phiếu kiểm kê theo vị trí, "
     "nhập kết quả khớp 30, lưu và gửi duyệt\n"
     "4. BKS duyệt phiếu kiểm kê\n"
     "5. NV-A xem lại kế hoạch, In và Xuất excel",
     "—",
     "- Trạng thái kế hoạch lần lượt: Đang tạo, Đang kiểm, Đã lập kiểm kê, Hoàn thành\n"
     "- TK1 nhận đúng 1 thông báo ở bước 2\n"
     "- Ô chờ duyệt Trang chủ của TK1 tăng 1 ở bước 2, giảm 1 ở bước 3\n"
     "- Bản In và Excel ở bước 5 khớp màn Chi tiết"),

    ("002", "Luồng có hàng thiếu", "P0",
     "Như TC_10.001 nhưng khi kiểm thực tế P1 chỉ còn 28",
     "1. Thực hiện bước 1 đến 3 như TC_10.001, nhập kết quả 28\n"
     "2. BKS duyệt phiếu kiểm kê\n"
     "3. Người có quyền \"Xử lý phiếu kiểm kê vị trí\" xử lý xong và hoàn thành phiếu kiểm kê\n"
     "4. Xem trạng thái kế hoạch",
     "SL thực tế: 28",
     "- Sau bước 2: phiếu kiểm kê sang chờ xử lý, kế hoạch vẫn Đã lập kiểm kê\n"
     "- Sau bước 3: mong đợi kế hoạch Hoàn thành (Lưu ý: xem TC_05.004 — code hiện tại vẫn Đã lập kiểm kê)\n"
     "- Nếu bước 3 xử lý bằng phiếu điều chuyển vị trí chuyển đủ số thiếu thì kế hoạch TỰ Hoàn thành"),

    ("003", "Kế hoạch nhiều nhà, nhiều công ty sở hữu", "P1",
     "Kho K1: P1 (nhà N1) có hàng của TPE và ENE; P4 (nhà N2) có hàng của TPE; PT1 tự do có hàng ENE",
     "1. Tạo kế hoạch tích P1, P4, PT1, Lấy vị trí, Lưu & Gửi\n"
     "2. Mở Chi tiết, In, Xuất excel",
     "—",
     "- 3 vị trí, P1 tách 2 nhóm công ty TPE và ENE với Cộng đúng tổng lô\n"
     "- Số liệu giống nhau trên màn Chi tiết, bản In, Excel (trừ cột Nhà Kho, xem TC_07.002)"),

    ("004", "Kế hoạch nháp bị bỏ rồi xóa", "P2",
     "NV-A có KH-17 Đang tạo",
     "1. NV-A mở Sửa KH-17, thay đổi thành viên, bấm Lưu\n"
     "2. Quyết định không kiểm nữa, xóa KH-17\n"
     "3. Đăng nhập TK1 xem thông báo và ô chờ duyệt",
     "—",
     "- KH-17 biến mất khỏi mọi lối vào\n"
     "- TK1 không nhận thông báo nào về KH-17, ô chờ duyệt không đổi"),
]
