# -*- coding: utf-8 -*-
"""Section V - VIII cho man Phieu giao viec."""
from tc_data_role import MENU, DATA, OPEN_TP1, FROM_HD01

FROM_BH01 = ("Đăng nhập TP-1, mở Phiếu chờ giao việc, tab Phiếu bảo hành, bấm nút bánh răng dòng BH-01, chọn "
             "\"Tạo phiếu giao việc\"")
FROM_LD01 = ("Đăng nhập TP-1, mở Phiếu chờ giao việc, tab Lắp đặt bàn giao, bấm nút bánh răng dòng LD-01, chọn "
             "\"Tạo phiếu giao việc\"")
FROM_YC01 = ("Đăng nhập TP-1, mở Phiếu chờ giao việc, tab Giao việc khác, bấm nút bánh răng dòng YC-01, chọn "
             "\"Tạo phiếu giao việc\"")

SEC_V = [
    ("001", "Mở form tạo phiếu từ phiếu bảo hành", "P0",
     DATA,
     "1. " + FROM_BH01,
     "—",
     "- Ô \"Số phiếu bảo hành\" BH-01 (bấm mở phiếu bảo hành)\n"
     "- Có mục \"A - BẢO HÀNH\": máy M2 lỗi E2, SL còn trên hợp đồng 1, SL giao lần này 1, Định mức công 1.5"),

    ("002", "Lưu phiếu bảo hành", "P0",
     DATA,
     "1. " + FROM_BH01 + "\n"
     "2. Chọn ngày dự kiến là hôm nay, bấm \"Lưu & duyệt\"",
     "—",
     "- Tạo phiếu thành công, Trạng thái \"Chờ thực hiện\", Tổng công định mức 1.50\n"
     "- BH-01 rời tab Phiếu bảo hành của Phiếu chờ giao việc"),

    ("003", "Phiếu bảo hành đã giao hết thì báo không có sản phẩm", "P0",
     "BH-01 đã có PGV-04 Chờ thực hiện giao máy M2\n" + DATA,
     "1. Đăng nhập TP-1, dán đường dẫn form tạo phiếu giao việc cho BH-01\n"
     "2. Chọn ngày dự kiến, bấm \"Lưu & duyệt\"",
     "—",
     "- Thông báo \"Không có sản phẩm bảo hành để giao\"\n"
     "- Không tạo phiếu"),

    ("004", "Dòng bảo hành để SL giao 0", "P1",
     DATA,
     "1. " + FROM_BH01 + "\n"
     "2. Ô SL giao lần này của M2 gõ 0\n"
     "3. Xem Tổng công định mức",
     "—",
     "- Mong đợi: Công chính 0.00 như dòng sửa chữa (IV.009)\n"
     "- Lưu ý: theo code hiện tại vẫn cộng 1.50 vào Công chính - ghi Failed"),

    ("005", "Xóa phiếu bảo hành trả lại phiếu chờ giao", "P0",
     "PGV-06 từ BH-01, Chờ thực hiện, chưa có phiếu công tác, do TP-1 lập",
     "1. " + OPEN_TP1 + "\n"
     "2. Xóa PGV-06 (xem mục IX)\n"
     "3. Mở Phiếu chờ giao việc, tab Phiếu bảo hành",
     "—",
     "- BH-01 quay lại danh sách, mở form thấy M2 SL còn 1"),
]

SEC_VI = [
    ("001", "Mở form tạo phiếu từ yêu cầu lắp đặt", "P0",
     DATA,
     "1. " + FROM_LD01,
     "—",
     "- Ô \"Phiếu yêu cầu lắp đặt, bàn giao\" LD-01, ô \"Hợp đồng\" HDH-01 (đều bấm mở)\n"
     "- Mục \"A - Lắp đặt bàn giao\": M3, SL bàn giao 3, SL tính công khoán 2, Định mức công 1, Tổng công định "
     "mức 2.00"),

    ("002", "SL tính công khoán làm tròn lên", "P0",
     DATA,
     "1. " + FROM_LD01 + "\n"
     "2. Ô SL bàn giao của M3 gõ 1",
     "—",
     "- SL tính công khoán 1, Tổng công định mức của dòng 1.00"),

    ("003", "Không nhập SL bàn giao quá số còn lại", "P0",
     DATA,
     "1. " + FROM_LD01 + "\n"
     "2. Ô SL bàn giao của M3 gõ 7",
     "—",
     "- Ô tự về 3"),

    ("004", "Giao một phần yêu cầu lắp đặt", "P0",
     DATA,
     "1. " + FROM_LD01 + "\n"
     "2. Ô SL bàn giao gõ 2, chọn ngày dự kiến, bấm \"Lưu & duyệt\"\n"
     "3. Mở lại Phiếu chờ giao việc, tab Lắp đặt bàn giao",
     "—",
     "- Tạo phiếu thành công\n"
     "- LD-01 vẫn còn; mở form giao tiếp thấy M3 còn 1"),

    ("005", "Giao hết yêu cầu lắp đặt", "P0",
     DATA,
     "1. " + FROM_LD01 + "\n"
     "2. Giữ SL bàn giao 3, chọn ngày dự kiến, bấm \"Lưu & duyệt\"",
     "—",
     "- Tạo phiếu thành công\n"
     "- LD-01 rời tab Lắp đặt bàn giao, mở LD-01 thấy trạng thái \"Đang giao việc\""),

    ("006", "Mở form tạo phiếu từ yêu cầu giao việc khác", "P0",
     DATA,
     "1. " + FROM_YC01,
     "—",
     "- Ô \"Phiếu YC giao việc khác\" YC-01 (bấm mở)\n"
     "- Mục \"A - Dịch vụ đính kèm\": \"Khảo sát mặt bằng\" Định mức công 0,5\n"
     "- Các mục sau đánh \"B - CÔNG VIỆC PHỤ\", \"C - TỔNG HỢP\""),

    ("007", "Lưu phiếu giao việc khác", "P0",
     DATA,
     "1. " + FROM_YC01 + "\n"
     "2. Chọn ngày dự kiến, bấm \"Lưu & duyệt\"",
     "—",
     "- Tạo phiếu thành công, Tổng công định mức 0.50\n"
     "- YC-01 chuyển Đã giao việc, rời tab Giao việc khác"),

    ("008", "Sửa định mức công dịch vụ đính kèm", "P1",
     DATA,
     "1. " + FROM_YC01 + "\n"
     "2. Ô Định mức công của \"Khảo sát mặt bằng\" gõ 1,25",
     "—",
     "- Tổng công định mức được giao 1.25"),

    ("009", "Mở form của yêu cầu phòng khác", "P1",
     "YC-05 Chờ giao việc, phòng tiếp nhận PKT2\n" + DATA,
     "1. Đăng nhập TP-1, dán đường dẫn form tạo phiếu giao việc cho YC-05",
     "—",
     "- Thông báo \"Không có quyền!\", form không có dữ liệu yêu cầu"),
]

SEC_VII = [
    ("001", "Thiếu Ngày dự kiến bắt đầu", "P0",
     DATA,
     "1. " + FROM_HD01 + "\n"
     "2. Xóa Ngày dự kiến bắt đầu, bấm \"Lưu & duyệt\"",
     "—",
     "- Báo lỗi dưới ô Ngày dự kiến bắt đầu, không tạo phiếu"),

    ("002", "Ngày dự kiến bắt đầu trước hôm nay", "P0",
     DATA,
     "1. " + FROM_HD01 + "\n"
     "2. Ngày dự kiến bắt đầu chọn hôm qua, bấm \"Lưu & duyệt\"",
     "—",
     "- Báo \"Ngày bắt đầu phải lớn hơn hoặc bằng ngày hiện tại\""),

    ("003", "Ngày kết thúc trước ngày bắt đầu", "P0",
     DATA,
     "1. " + FROM_HD01 + "\n"
     "2. Bắt đầu 10/11/2026, kết thúc 09/11/2026, bấm \"Lưu & duyệt\"",
     "—",
     "- Báo \"Ngày kết thúc phải lớn hơn hoặc bằng ngày hiện tại và ngày bắt đầu\""),

    ("004", "Ô ngày dự kiến ở hai chỗ luôn khớp nhau", "P2",
     DATA,
     "1. " + FROM_HD01 + "\n"
     "2. Chọn Ngày dự kiến bắt đầu ở phần Thông tin khách hàng là 10/11/2026\n"
     "3. Xem ô \"Từ ngày\" ở phần Thời gian dự kiến thực hiện",
     "—",
     "- Ô \"Từ ngày\" cũng là 10/11/2026"),

    ("005", "Thêm công phụ P3", "P0",
     DATA,
     "1. " + FROM_HD01 + "\n"
     "2. Ở \"I. Công phụ tính P3\" bấm +, gõ Tên \"Vận chuyển máy\", định mức 0,5",
     "—",
     "- Công phụ 0.50\n"
     "- Tổng công định mức được giao 2.50"),

    ("006", "Công phụ thiếu tên", "P1",
     DATA,
     "1. " + FROM_HD01 + "\n"
     "2. Thêm 1 dòng công phụ chỉ nhập định mức 0,5, bấm \"Lưu & duyệt\"",
     "—",
     "- Báo lỗi thiếu thông tin, không tạo phiếu"),

    ("007", "Xóa dòng công phụ", "P2",
     DATA,
     "1. Làm như TC 005\n"
     "2. Bấm x ở dòng \"Vận chuyển máy\"",
     "—",
     "- Dòng mất, Tổng công định mức về 2.00"),

    ("008", "Mở form tạo trống không có chứng từ gốc", "P1",
     "—",
     "1. Đăng nhập TP-1, dán đường dẫn form tạo phiếu giao việc không kèm chứng từ\n"
     "2. Bấm \"Lưu & duyệt\"",
     "—",
     "- Form không có chứng từ, không có hàng\n"
     "- Báo lỗi thiếu Khách hàng, Người liên hệ, không tạo phiếu"),

    ("009", "Bấm Lưu & duyệt nhiều lần liên tiếp", "P1",
     DATA,
     "1. " + FROM_HD01 + "\n"
     "2. Chọn ngày dự kiến, bấm nhanh \"Lưu & duyệt\" 2 lần",
     "—",
     "- Nút bị khóa sau lần bấm đầu\n"
     "- Chỉ tạo 1 phiếu"),

    ("010", "Trưởng phòng bị chặn vì phòng có nhân viên quá hạn", "P1",
     "Cấu hình chặn quá hạn bật cho hành động \"Tạo phiếu giao việc\"; PKT1 có nhân viên quá hạn\n" + DATA,
     "1. " + FROM_HD01 + "\n"
     "2. Chọn ngày dự kiến, bấm \"Lưu & duyệt\"",
     "—",
     "- Hiện thông báo chặn quá hạn kèm danh sách quá hạn\n"
     "- Không tạo phiếu"),

    ("011", "Gọi thẳng chức năng lưu với số lượng lớn hơn số còn", "P1",
     DATA,
     "1. Đăng nhập TP-1\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng lưu phiếu giao việc cho HD-01, \"Vệ sinh máy\" SL 5",
     "—",
     "- Mong đợi: bị chặn vì vượt số còn 1\n"
     "- Lưu ý: theo code hiện tại lưu thành công (đã ghi ở bộ Phiếu chờ giao việc) - ghi Failed"),

    ("012", "Gọi thẳng chức năng lưu với trạng thái khác Chờ thực hiện", "P1",
     DATA,
     "1. Đăng nhập TP-1\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng lưu phiếu giao việc cho HD-01, gửi kèm trạng thái "
     "\"Đã duyệt kết quả\"",
     "—",
     "- Mong đợi: phiếu mới luôn ở Chờ thực hiện\n"
     "- Lưu ý: theo code hiện tại phiếu được tạo thẳng ở trạng thái Đã duyệt kết quả - ghi Failed"),
]

SEC_VIII = [
    ("001", "Mở chi tiết phiếu giao việc", "P0",
     "PGV-01 từ HD-01, Chờ thực hiện, do TP-1 lập",
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm số phiếu PGV-01",
     "—",
     "- Tiêu đề \"Phiếu giao việc PGV-01\"\n"
     "- Góc trên hiện người lập và thời gian lập\n"
     "- Mọi ô đều khóa, không có nút \"Lưu & duyệt\", chỉ có \"Quay lại\""),

    ("002", "Chi tiết không hiện cột SL còn trên hợp đồng", "P1",
     "PGV-01 như TC 001",
     "1. Mở chi tiết PGV-01",
     "—",
     "- Bảng dịch vụ sửa chữa không có cột \"SL còn trên hợp đồng\"\n"
     "- SL giao lần này 1, Định mức công 2"),

    ("003", "Chi tiết phiếu lắp đặt", "P1",
     "PGV-02 từ LD-01 giao 3 máy M3",
     "1. Mở chi tiết PGV-02",
     "—",
     "- Ô Phiếu yêu cầu lắp đặt LD-01, Hợp đồng HDH-01, Người yêu cầu KD-1, Phòng yêu cầu PKD\n"
     "- Bảng lắp đặt có M3 SL bàn giao 3"),

    ("004", "Bấm số hợp đồng ở chi tiết mở chứng từ gốc", "P2",
     "PGV-01 như TC 001",
     "1. Mở chi tiết PGV-01, bấm HD-01",
     "—",
     "- Mở hợp đồng HD-01 ở tab mới"),

    ("005", "Bấm Quay lại ở chi tiết", "P2",
     "PGV-01 như TC 001",
     "1. Mở chi tiết PGV-01, bấm \"Quay lại\"",
     "—",
     "- Về danh sách Phiếu giao việc"),

    ("006", "Phiếu đã xóa vẫn mở được chi tiết qua đường dẫn", "P2",
     "PGV-04 đã Xóa, do TP-1 lập",
     "1. Đăng nhập TP-1, dán đường dẫn chi tiết PGV-04",
     "—",
     "- Mở được chi tiết, các ô khóa (không có chỗ nào hiện chữ Hủy)\n"
     "- Ghi nhận cho nghiệp vụ: nếu cần hiện rõ phiếu đã hủy thì ghi Failed"),
]
