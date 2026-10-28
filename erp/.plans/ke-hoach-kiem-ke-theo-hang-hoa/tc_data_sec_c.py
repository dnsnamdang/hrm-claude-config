# -*- coding: utf-8 -*-
"""Section VI - X - xoa, in & excel, rang buoc, co lap & dong thoi, luong dau - cuoi."""
from tc_data_role import P1

SEC_VI = [
    ("001", "Xóa kế hoạch nháp của mình", "P0",
     "KH-1 Đang tạo do NV-A lập",
     "1. Đăng nhập NV-A, bấm bánh răng > Xóa ở KH-1\n"
     "2. Bấm đồng ý ở hộp xác nhận\n"
     "3. Tìm lại KH-1",
     "—",
     "- Mong đợi: báo \"Xóa thành công!\", KH-1 biến mất khỏi danh sách\n"
     "- Lưu ý: theo code hiện tại hệ thống báo lỗi hệ thống, KH-1 VẪN CÒN - ghi Failed"),

    ("002", "Hủy ở hộp xác nhận xóa", "P1",
     "KH-1 Đang tạo do NV-A lập",
     "1. Bấm bánh răng > Xóa ở KH-1\n"
     "2. Bấm hủy ở hộp xác nhận",
     "—",
     "- KH-1 còn nguyên, danh sách không đổi"),

    ("003", "Kế hoạch đã gửi không có nút Xóa", "P0",
     "KH-2 Đang kiểm do chính NV-A lập",
     "1. Đăng nhập NV-A, bấm bánh răng của KH-2",
     "—",
     "- Không có Xóa, không có Sửa"),

    ("004", "Gọi thẳng chức năng Xóa kế hoạch đã gửi", "P1",
     "KH-2 Đang kiểm do chính NV-A lập",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa KH-2",
     "—",
     "- Báo \"Không thể xóa!\", KH-2 còn nguyên, vẫn Đang kiểm"),
]


SEC_VII = [
    ("001", "In một kế hoạch", "P0",
     "KH-2: kho K1, ghi chú \"Kiểm quý 4\", hàng H1 (KT1 = 6, KT2 = 4), H2 (KT1 = 3), 2 thành viên",
     "1. Bấm bánh răng > In ở KH-2\n"
     "2. Soát bản in ở thẻ mới",
     "—",
     "- Khổ ngang, tiêu đề \"Kế hoạch kiểm kê theo mặt hàng\"\n"
     "- Có Số phiếu, Ngày kiểm kê, Kho, Ghi chú, Hội đồng kiểm kê\n"
     "- Bảng: STT, Tên hàng, Mã hàng, ĐVT, Kho kế toán, SL tồn, Tổng SL\n"
     "- H1 chiếm 2 dòng (KT1 6, KT2 4), Tổng SL 10 gộp ô; H2 1 dòng, Tổng SL 3"),

    ("002", "Bản in ghi Hội đồng kiểm kê", "P2",
     "KH-2 có thành viên \"Nguyễn Văn An\" (Thủ kho) và \"Trần Thị Bình\" (Kế toán kho)",
     "1. In KH-2, đọc phần Hội đồng kiểm kê",
     "—",
     "- Mong đợi: hai tên tách biệt, kèm chức vụ\n"
     "- Lưu ý: theo code hiện tại hiện liền \"Nguyễn Văn AnTrần Thị Bình\", không có chức vụ - ghi Failed"),

    ("003", "Xuất excel một kế hoạch", "P0",
     "Kế hoạch KH-2 bất kỳ",
     "1. Bấm bánh răng > Xuất excel ở KH-2",
     "—",
     "- Mong đợi: tải về tệp Excel kế hoạch, nội dung như bản In\n"
     "- Lưu ý: theo code hiện tại hệ thống báo lỗi, không tải được tệp - ghi Failed"),

    ("004", "In danh sách theo bộ lọc", "P0",
     "Đang lọc Trạng thái Đang kiểm, có 3 kết quả",
     "1. Bấm nút In ở hàng nút trên bảng",
     "—",
     "- Mở bản in khổ ngang ở thẻ mới\n"
     "- Bảng: STT, Số phiếu, Ngày kiểm kê, Kho, Người lập, Trạng thái\n"
     "- Đúng 3 dòng như trên lưới"),

    ("005", "Xuất excel danh sách theo bộ lọc", "P0",
     "Đang lọc Người tạo NV-A, có 2 kết quả",
     "1. Bấm nút Xuất excel ở hàng nút trên bảng\n"
     "2. Mở tệp tải về",
     "—",
     "- Tải về tệp \"danh_sach_ke_hoach_kiem_ke_theo_hang_hoa\"\n"
     "- Tiêu đề \"Danh sách kế hoạch kiểm kê theo hàng hóa\"\n"
     "- Đúng 2 dòng như trên lưới"),

    ("006", "In / Xuất danh sách khi đang lọc Mã hàng hóa", "P2",
     "Đang nhập ô \"Nhập mã hàng hóa\"",
     "1. Bấm In, rồi bấm Xuất excel",
     "—",
     "- Mong đợi: bản In và tệp Excel chỉ gồm kế hoạch có mã hàng đã nhập\n"
     "- Lưu ý: theo code hiện tại cả hai báo lỗi (cùng nguyên nhân TC_02.007), ghi lại thực tế"),

    ("007", "In danh sách không gồm nháp của người khác", "P1",
     "Người xem quyền tổng công ty; người khác có 2 kế hoạch Đang tạo",
     "1. Không lọc gì, bấm In",
     "—",
     "- Số dòng bản in = số tổng trên lưới, không có 2 kế hoạch nháp của người khác"),

    ("008", "Bản in kế hoạch nhiều kho", "P2",
     "KH-5 chọn kho K1, K2",
     "1. In KH-5",
     "—",
     "- Dòng Kho hiện \"K1, K2\""),
]


SEC_VIII = [
    ("001", "Lưu khi chưa chọn kho", "P0",
     "—",
     "1. Tạo mới, không chọn kho, thêm 1 thành viên\n"
     "2. Bấm Lưu",
     "—",
     "- Báo \"Tạo thất bại!\"\n"
     "- Dưới ô Kho có lỗi (tiếng Anh) \"The warehouses field is required.\"\n"
     "- Không lưu kế hoạch"),

    ("002", "Lưu khi chưa có hàng hóa", "P0",
     "—",
     "1. Tạo mới, chọn Kho K1, thêm 1 thành viên, không thêm hàng\n"
     "2. Bấm Lưu",
     "—",
     "- Báo \"Tạo thất bại!\"\n"
     "- Tab Hàng hóa đổi màu đỏ có biểu tượng chấm than\n"
     "- Dưới bảng có lỗi \"The products field is required.\""),

    ("003", "Lưu khi chưa có thành viên", "P0",
     "—",
     "1. Tạo mới, chọn kho, thêm hàng, không thêm thành viên\n"
     "2. Bấm Lưu",
     "—",
     "- Báo \"Tạo thất bại!\"\n"
     "- Tab Hội đồng kiểm kê đổi màu đỏ\n"
     "- Có lỗi \"The members field is required.\""),

    ("004", "Lưu khi dòng thành viên chưa chọn người", "P0",
     "—",
     "1. Tạo mới, đủ kho và hàng\n"
     "2. Thêm 1 dòng thành viên nhưng để trống ô Thành viên\n"
     "3. Bấm Lưu",
     "—",
     "- Báo \"Tạo thất bại!\"\n"
     "- Dưới ô Thành viên dòng 1 có lỗi \"The members.0.employee_id field is required.\"\n"
     "- Tab Hội đồng kiểm kê đổi màu đỏ"),

    ("005", "Lưu khi thành viên không có vai trò nào", "P1",
     "Nhân viên NV-R chưa được gán vai trò nào",
     "1. Tạo mới, đủ kho và hàng\n"
     "2. Thêm thành viên NV-R (ô Chức vụ trống)\n"
     "3. Bấm Lưu",
     "—",
     "- Mong đợi: báo lỗi rõ ràng dưới ô Chức vụ\n"
     "- Lưu ý: theo code hiện tại báo chung \"Đã có lỗi xảy ra\", không lưu - ghi lại thực tế"),

    ("006", "Một thành viên được thêm hai lần", "P2",
     "—",
     "1. Tạo mới, đủ kho và hàng\n"
     "2. Thêm 2 dòng cùng chọn NV-K\n"
     "3. Bấm Lưu",
     "—",
     "- Theo code hiện tại: lưu được, Hội đồng có 2 dòng NV-K\n"
     "- Lưu ý: ghi Failed nếu nghiệp vụ yêu cầu chặn trùng"),

    ("007", "Ghi chú tối đa 255 ký tự", "P1",
     "—",
     "1. Tạo mới, đủ dữ liệu\n"
     "2. Nhập Ghi chú đúng 255 ký tự, Lưu\n"
     "3. Tạo kế hoạch khác, Ghi chú 256 ký tự, Lưu",
     "Ghi chú: 255 ký tự / 256 ký tự",
     "- 255 ký tự: lưu được, hiện đủ ở Chi tiết\n"
     "- 256 ký tự: mong đợi báo lỗi độ dài rõ ràng; theo code hiện tại có thể báo \"Đã có lỗi xảy ra\" "
     "- ghi lại thực tế"),

    ("008", "Ghi chú có ký tự đặc biệt và tiếng Việt", "P2",
     "—",
     "1. Tạo mới, Ghi chú \"Kiểm <b>gấp</b> & 'ngay'\", Lưu\n"
     "2. Mở Chi tiết và bản In",
     "Ghi chú: Kiểm <b>gấp</b> & 'ngay'",
     "- Chi tiết: Ghi chú hiện đúng nguyên văn\n"
     "- Bản In: mong đợi hiện nguyên văn; Lưu ý: theo code hiện tại chữ \"gấp\" có thể bị in đậm - ghi "
     "lại thực tế"),

    ("009", "Ghi chú để trống vẫn lưu được", "P2",
     "—",
     "1. Tạo mới, đủ dữ liệu, bỏ trống Ghi chú, Lưu",
     "—",
     "- Báo \"Tạo thành công\""),

    ("010", "Tổng SL có phần thập phân", "P2",
     "Hàng H5 đơn vị Kg, tồn kế toán KT1 = 2,756",
     "1. Tạo mới, thêm H5, Lưu\n"
     "2. Mở Chi tiết",
     "—",
     "- Tổng SL hiện làm tròn còn 2 chữ số thập phân (2,76)"),

    ("011", "Gọi thẳng chức năng Lưu với hàng trùng", "P1",
     "Tester kỹ thuật",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Lưu kế hoạch, gửi 2 dòng cùng hàng H1",
     "—",
     "- Báo \"Tạo thất bại!\", không lưu"),

    ("012", "Gọi thẳng chức năng Lưu với trạng thái không hợp lệ", "P1",
     "Tester kỹ thuật",
     "1. Gọi thẳng chức năng Lưu kế hoạch với trạng thái Hoàn thành",
     "Trạng thái: Hoàn thành",
     "- Báo \"Tạo thất bại!\", chỉ chấp nhận Đang tạo hoặc Đang kiểm"),

    ("013", "Gọi thẳng chức năng Lưu với kho của công ty khác", "P2",
     "NV-A thuộc công ty 1; kho K5 thuộc công ty 3",
     "1. Gọi thẳng chức năng Lưu kế hoạch với kho K5",
     "Kho: K5",
     "- Mong đợi: hệ thống từ chối\n"
     "- Lưu ý: theo code hiện tại lưu được - ghi Failed nếu nghiệp vụ yêu cầu chặn"),
]


SEC_IX = [
    ("001", "Kế hoạch mang công ty và phòng ban của người lập", "P1",
     "NV-A thuộc công ty 1, phòng Kho HN",
     "1. NV-A lập và Lưu & kiểm kế hoạch KH-8\n"
     "2. Tài khoản quyền \"Tổng kiểm kê kho theo hàng hóa\" công ty 1 và công ty 3 cùng tìm KH-8",
     "—",
     "- Người công ty 1 thấy KH-8\n"
     "- Người công ty 3 không thấy KH-8"),

    ("002", "Người lập chuyển công ty vẫn thấy kế hoạch cũ", "P2",
     "NV-A lập KH-9 khi ở công ty 1, sau đó chuyển sang công ty 3, có quyền \"Tổng kiểm kê kho theo "
     "hàng hóa\"",
     "1. Đăng nhập NV-A, mở màn từ menu, tìm KH-9",
     "—",
     "- Vẫn thấy KH-9 (kế hoạch do mình lập)"),

    ("003", "Hai người cùng lập phiếu kiểm kê từ một kế hoạch", "P0",
     "KH-2 Đang kiểm; TK1, TK2 đều có quyền Lập phiếu kiểm kê kho theo hàng hóa",
     "1. TK1 và TK2 cùng mở màn lập phiếu kiểm kê từ KH-2\n"
     "2. TK1 bấm Lưu trước, sau đó TK2 bấm Lưu",
     "—",
     "- Mong đợi: lần lưu của TK2 bị từ chối vì kế hoạch đã có phiếu kiểm kê\n"
     "- Lưu ý: theo code hiện tại TK2 vẫn lưu được, KH-2 có 2 phiếu kiểm kê - ghi Failed"),

    ("004", "Sửa kế hoạch ở hai thẻ cùng lúc", "P2",
     "KH-1 Đang tạo do NV-A lập",
     "1. NV-A mở Sửa KH-1 ở thẻ 1 và thẻ 2\n"
     "2. Thẻ 1 đổi Ghi chú \"A\", Lưu\n"
     "3. Thẻ 2 đổi Ghi chú \"B\", Lưu",
     "—",
     "- Cả hai lần báo \"Sửa thành công\"\n"
     "- Chi tiết KH-1 hiện Ghi chú \"B\" (lần lưu sau ghi đè)"),

    ("005", "Gửi kiểm ở thẻ cũ sau khi đã gửi ở thẻ khác", "P1",
     "KH-1 Đang tạo do NV-A lập, mở Sửa ở thẻ 1 và thẻ 2",
     "1. Thẻ 1 bấm Lưu & gửi\n"
     "2. Thẻ 2 bấm Lưu",
     "—",
     "- Thẻ 2 báo \"Bạn không có quyền sửa phiếu này\"\n"
     "- KH-1 vẫn Đang kiểm"),

    ("006", "Lập phiếu kiểm kê từ thẻ cũ sau khi kế hoạch đã có phiếu", "P1",
     "TK1 mở danh sách kế hoạch từ trước, KH-2 vẫn hiện nút Lập phiếu; trong lúc đó TK2 đã lập phiếu từ "
     "KH-2",
     "1. TK1 bấm \"Lập phiếu kiểm kê theo hàng hóa\" ở KH-2 trên thẻ cũ",
     "—",
     "- Màn " + P1 + " báo \"Không có quyền\", không điền sẵn dữ liệu kế hoạch"),
]


SEC_X = [
    ("001", "Luồng chuẩn: lập kế hoạch, gửi kiểm, lập phiếu kiểm kê", "P0",
     "NV-A (kế toán kho) không có quyền xem; TK1 có quyền \"Lập phiếu kiểm kê kho theo hàng hóa\" và "
     "\"Tổng kiểm kê kho theo hàng hóa\"; kho K1 không có phiếu kho chưa xong",
     "1. NV-A tạo kế hoạch kho K1, hàng H1, H2, Hội đồng 2 người, bấm Lưu\n"
     "2. NV-A mở Sửa, thêm H3, bấm Lưu & gửi\n"
     "3. TK1 bấm thông báo / mở danh sách, bấm \"Lập phiếu kiểm kê theo hàng hóa\"\n"
     "4. TK1 lưu phiếu kiểm kê\n"
     "5. NV-A xem lại kế hoạch",
     "—",
     "- Sau bước 1: Đang tạo\n"
     "- Sau bước 2: Đang kiểm, có H1, H2, H3, TK1 có thông báo\n"
     "- Sau bước 3: phiếu kiểm kê điền sẵn kho K1, H1, H2, H3, Hội đồng 2 người\n"
     "- Sau bước 5: kế hoạch \"Đã lập phiếu kiểm kê\", không còn nút Lập phiếu"),

    ("002", "Luồng bị chặn rồi gửi lại sau khi xử lý phiếu kho", "P0",
     "Kho K1 có phiếu nhập kho PNK-1 chưa xong chứa H1",
     "1. Tạo kế hoạch kho K1, hàng H1, bấm Lưu & kiểm\n"
     "2. Bấm Lưu (nháp)\n"
     "3. Hoàn tất PNK-1\n"
     "4. Mở Sửa kế hoạch, bấm Lưu & gửi",
     "—",
     "- Bước 1: cửa sổ cảnh báo có PNK-1, không lưu\n"
     "- Bước 2: lưu nháp được\n"
     "- Bước 4: kế hoạch chuyển Đang kiểm, SL tồn H1 đã tính cả phần PNK-1 nhập vào"),

    ("003", "Luồng đến khi phiếu kiểm kê hoàn thành", "P1",
     "KH-2 đã Đã lập phiếu kiểm kê với phiếu PKK-2",
     "1. Đưa PKK-2 qua các bước kiểm, duyệt đến Hoàn thành\n"
     "2. Xem lại KH-2 ở danh sách, ở Chi tiết và bản In",
     "—",
     "- PKK-2 Hoàn thành\n"
     "- KH-2 mong đợi Hoàn thành; theo code hiện tại vẫn \"Đã lập phiếu kiểm kê\" (xem TC_05.013)\n"
     "- Chi tiết và bản In của KH-2 vẫn giữ số tồn lúc lập kế hoạch"),

    ("004", "Lập lại kế hoạch mới cho cùng hàng sau khi kế hoạch cũ đã có phiếu", "P2",
     "KH-2 (kho K1, hàng H1) đã Đã lập phiếu kiểm kê",
     "1. Tạo kế hoạch mới kho K1, hàng H1, bấm Lưu & kiểm",
     "—",
     "- Lưu được, kế hoạch mới Đang kiểm (hệ thống không chặn trùng hàng giữa các kế hoạch)"),
]
