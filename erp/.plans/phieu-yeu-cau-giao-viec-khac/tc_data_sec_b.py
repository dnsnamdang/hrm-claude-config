# -*- coding: utf-8 -*-
"""Section V - VIII cho man Phieu yeu cau giao viec khac."""
from tc_data_role import MENU, DATA, OPEN_KD1, OPEN_CREATE

FILLED = ("Form tạo mới của KD-1 đã chọn KH-01, người liên hệ Anh Bình, Thời gian dự kiến 10/11/2026, Địa chỉ "
          "lắp đặt \"12 Lê Lợi\", Phòng tiếp nhận PKT1")

SEC_V = [
    ("001", "Chọn hợp đồng khi chưa chọn khách", "P1",
     DATA,
     "1. " + OPEN_CREATE + "\n"
     "2. Bấm nút tìm ở ô Hợp đồng",
     "—",
     "- Thông báo \"Chưa chọn khách hàng!\", không mở danh sách"),

    ("002", "Danh sách hợp đồng để chọn", "P0",
     DATA + "\nKH-01 còn có HD-03 do KD-2 lập và HD-04 Đã thanh lý do KD-1 lập",
     "1. " + OPEN_CREATE + ", chọn KH-01\n"
     "2. Bấm nút tìm ở ô Hợp đồng",
     "—",
     "- Có HD-01\n"
     "- Không có HD-03 (người khác lập), không có HD-04 (không còn hiệu lực)"),

    ("003", "Chọn hợp đồng lấy sẵn dịch vụ của hợp đồng và phụ lục bổ sung", "P0",
     DATA,
     "1. " + OPEN_CREATE + ", chọn KH-01\n"
     "2. Chọn hợp đồng HD-01",
     "—",
     "- Thông báo \"Thêm thành công\"\n"
     "- Ô Hợp đồng \"HD-01\"\n"
     "- Bảng có 3 dòng: Vệ sinh máy, Bảo trì định kỳ, Hướng dẫn sử dụng, đều đã tích\n"
     "- Phòng QTC, Nhân viên QTC hiện theo HD-01"),

    ("004", "Có hợp đồng thì không thêm, không bỏ được dòng", "P0",
     "Đã chọn HD-01 như TC 003",
     "1. Xem bảng Danh sách cần giao việc",
     "—",
     "- Không có nút \"Thêm dịch vụ\"\n"
     "- Không có dấu x để bỏ dòng"),

    ("005", "Chọn hợp đồng thay các dòng đã tự thêm", "P1",
     "Form đã chọn KH-01, tự thêm dịch vụ \"Kiểm tra định kỳ\"",
     "1. Chọn hợp đồng HD-01",
     "—",
     "- Bảng chỉ còn 3 dòng của HD-01, mất dòng \"Kiểm tra định kỳ\""),

    ("006", "Chọn hợp đồng đã có phiếu yêu cầu", "P0",
     "HD-02 của KH-01 đã có phiếu yêu cầu YC-07 (Chờ giao việc)",
     "1. " + OPEN_CREATE + ", chọn KH-01\n"
     "2. Chọn hợp đồng HD-02",
     "—",
     "- Mong đợi: thông báo \"Phiếu đã được lập yêu cầu.Vui lòng kiểm tra lại!\", ô Hợp đồng vẫn trống\n"
     "- Lưu ý: theo code hiện tại không có thông báo nào, ô Hợp đồng nhận HD-02, bảng không có dòng - ghi "
     "Failed"),

    ("007", "Lưu được phiếu thứ hai cho cùng hợp đồng", "P0",
     "HD-02 đã có YC-07. Form tạo mới đã chọn KH-01, tự thêm \"Kiểm tra định kỳ\", rồi chọn hợp đồng HD-02",
     "1. Điền đủ ô bắt buộc, bấm \"Lưu và gửi duyệt\"",
     "—",
     "- Trước khi lưu: bảng vẫn giữ dòng \"Kiểm tra định kỳ\", không còn nút \"Thêm dịch vụ\"\n"
     "- Mong đợi: bị chặn vì HD-02 đã có phiếu yêu cầu\n"
     "- Lưu ý: theo code hiện tại lưu thành công, HD-02 có 2 phiếu yêu cầu - ghi Failed"),

    ("008", "Phụ lục bổ sung chưa duyệt cũng được lấy dịch vụ", "P1",
     "HD-01 có thêm PL-02 Đang tạo, có dịch vụ \"Đào tạo vận hành\"",
     "1. " + OPEN_CREATE + ", chọn KH-01, chọn HD-01",
     "—",
     "- Mong đợi: chỉ lấy dịch vụ của phụ lục đã có hiệu lực\n"
     "- Lưu ý: theo code hiện tại có cả \"Đào tạo vận hành\" của PL-02 - ghi Failed nếu nghiệp vụ chỉ lấy phụ lục "
     "có hiệu lực"),

    ("009", "Tự thêm dịch vụ khi không có hợp đồng", "P0",
     FILLED,
     "1. Bấm \"Thêm dịch vụ\"\n"
     "2. Chọn \"Kiểm tra định kỳ\"",
     "—",
     "- Bảng có dòng \"Kiểm tra định kỳ\", đã tích, có dấu x để bỏ"),

    ("010", "Danh sách dịch vụ để tự thêm", "P1",
     FILLED + "\n\"Phí vận chuyển\" là dịch vụ không tính doanh thu",
     "1. Bấm \"Thêm dịch vụ\", tìm \"Phí vận chuyển\"",
     "—",
     "- Không có \"Phí vận chuyển\""),

    ("011", "Bỏ một dòng tự thêm", "P1",
     FILLED + "; đã thêm \"Kiểm tra định kỳ\", \"Vệ sinh máy\"",
     "1. Bấm dấu x ở dòng \"Vệ sinh máy\"",
     "—",
     "- Bảng còn 1 dòng \"Kiểm tra định kỳ\""),

    ("012", "Thêm trùng một dịch vụ", "P2",
     FILLED + "; đã thêm \"Kiểm tra định kỳ\"",
     "1. Bấm \"Thêm dịch vụ\", chọn lại \"Kiểm tra định kỳ\"",
     "—",
     "- Bảng có 2 dòng \"Kiểm tra định kỳ\"\n"
     "- Lưu ý: không chặn trùng; nghiệp vụ xác nhận có cần chặn không"),

    ("013", "Ô tích tất cả", "P1",
     "Đã chọn HD-01, 3 dòng đều tích",
     "1. Bỏ tích ô ở tiêu đề cột\n"
     "2. Tích lại ô ở tiêu đề cột",
     "—",
     "- Bước 1: cả 3 dòng bỏ tích\n"
     "- Bước 2: cả 3 dòng tích lại"),

    ("014", "Bỏ tích một dòng thì ô tiêu đề bỏ tích", "P2",
     "Đã chọn HD-01, 3 dòng đều tích",
     "1. Bỏ tích dòng \"Bảo trì định kỳ\"",
     "—",
     "- Ô tích ở tiêu đề tự bỏ tích"),

    ("015", "Đổi khách hàng sau khi đã chọn hợp đồng", "P1",
     "Đã chọn KH-01 và HD-01; KH-03 là khách khác",
     "1. Chọn lại khách hàng KH-03",
     "—",
     "- Mong đợi: ô Hợp đồng và bảng dịch vụ được xóa\n"
     "- Lưu ý: theo code hiện tại vẫn giữ HD-01 và 3 dòng của HD-01, lưu được phiếu KH-03 gắn hợp đồng KH-01 - "
     "ghi Failed"),

    ("016", "Không bỏ được hợp đồng đã chọn", "P2",
     "Đã chọn KH-01 và HD-01",
     "1. Tìm cách xóa ô Hợp đồng",
     "—",
     "- Không có nút xóa hợp đồng; chỉ chọn được hợp đồng khác hoặc mở lại form\n"
     "- Lưu ý: nghiệp vụ xác nhận có cần cho bỏ hợp đồng không"),
]

SEC_VI = [
    ("001", "Bấm Lưu tạo phiếu Đang tạo", "P0",
     FILLED + "; đã thêm \"Kiểm tra định kỳ\"",
     "1. Bấm \"Lưu\"",
     "—",
     "- Thông báo \"Thao tác thành công!\"\n"
     "- Về danh sách, phiếu mới ở dòng 1, Trạng thái \"Đang tạo\", Người lập KD-1\n"
     "- PKT1 không nhận thông báo"),

    ("002", "Số phiếu theo mã công ty và năm", "P0",
     "Làm như TC 001",
     "1. Xem Số phiếu của phiếu mới",
     "—",
     "- Dạng \"TPE.YCGVK.2026\" + 6 chữ số"),

    ("003", "Bấm Lưu và gửi duyệt", "P0",
     FILLED + "; đã chọn HD-01",
     "1. Bấm \"Lưu và gửi duyệt\"",
     "—",
     "- Thông báo \"Thao tác thành công!\"\n"
     "- Phiếu mới Trạng thái \"Chờ giao việc\"\n"
     "- Phiếu có trong Phiếu chờ giao việc, tab Giao việc khác"),

    ("004", "Phòng tiếp nhận nhận thông báo khi gửi duyệt", "P0",
     "Làm như TC 003; TP-1 thuộc PKT1 có quyền \"Tạo phiếu giao việc\"; KTV-1 thuộc PKT1 không có quyền này",
     "1. Đăng nhập TP-1, mở chuông thông báo\n"
     "2. Bấm thông báo\n"
     "3. Đăng nhập KTV-1, mở chuông thông báo",
     "—",
     "- TP-1 có thông báo mới, bấm vào mở chi tiết phiếu\n"
     "- KTV-1 không có thông báo"),

    ("005", "Nội dung thông báo cho phòng tiếp nhận", "P2",
     "Làm như TC 004",
     "1. Đọc nội dung thông báo của TP-1",
     "—",
     "- Mong đợi: câu rõ ràng có tên người gửi, ví dụ \"Bạn có một yêu cầu giao việc khác cần xử lý - <tên "
     "KD-1>\"\n"
     "- Lưu ý: theo code hiện tại là \"Bạn có một yêu giao việc khác cần xử lý<tên KD-1>\" (thiếu chữ \"cầu\", tên "
     "dính liền) - ghi Failed"),

    ("006", "Phiếu lưu đúng dữ liệu đã nhập", "P0",
     "Làm như TC 003",
     "1. Bấm Số phiếu mở chi tiết",
     "—",
     "- KH-01, Anh Bình, Thời gian dự kiến 10/11/2026, Địa chỉ lắp đặt \"12 Lê Lợi\", Phòng tiếp nhận PKT1, Hợp "
     "đồng HD-01\n"
     "- 3 dòng dịch vụ của HD-01, đều tích"),

    ("007", "Dòng bỏ tích vẫn lưu, giữ trạng thái bỏ tích", "P1",
     FILLED + "; đã chọn HD-01, bỏ tích \"Bảo trì định kỳ\"",
     "1. Bấm \"Lưu\"\n"
     "2. Mở Sửa phiếu",
     "—",
     "- \"Bảo trì định kỳ\" vẫn có trong bảng, không tích"),

    ("008", "Nút bị khóa khi đang lưu", "P2",
     FILLED + "; đã thêm 1 dịch vụ",
     "1. Bấm \"Lưu\", trong lúc chờ bấm tiếp \"Lưu\"",
     "—",
     "- Hai nút mờ, có biểu tượng chờ; chỉ tạo 1 phiếu"),
]

SEC_VII = [
    ("001", "Bỏ trống Khách hàng", "P0",
     DATA,
     "1. " + OPEN_CREATE + "\n"
     "2. Chỉ chọn Thời gian dự kiến, Phòng tiếp nhận, bấm \"Lưu\"",
     "—",
     "- Thông báo \"Thao tác thất bại\"\n"
     "- Dưới ô Khách hàng có câu báo bắt buộc; không tạo phiếu"),

    ("002", "Bỏ trống Người liên hệ của khách doanh nghiệp", "P0",
     FILLED.replace(", người liên hệ Anh Bình", "") + "; đã thêm 1 dịch vụ",
     "1. Bấm \"Lưu\"",
     "—",
     "- Thông báo \"Thao tác thất bại\", dưới ô Người liên hệ có câu báo bắt buộc"),

    ("003", "Bỏ trống Thời gian dự kiến", "P0",
     FILLED.replace(", Thời gian dự kiến 10/11/2026", "") + "; đã thêm 1 dịch vụ",
     "1. Bấm \"Lưu\"",
     "—",
     "- Thông báo \"Thao tác thất bại\", dưới ô Thời gian dự kiến có câu báo bắt buộc"),

    ("004", "Bỏ trống Địa chỉ lắp đặt", "P0",
     "Form đã chọn KH-04 (doanh nghiệp không có địa chỉ giao hàng), người liên hệ, thời gian, phòng tiếp nhận, "
     "1 dịch vụ; Địa chỉ lắp đặt trống",
     "1. Bấm \"Lưu\"",
     "—",
     "- Thông báo \"Thao tác thất bại\", dưới ô Địa chỉ lắp đặt có câu báo bắt buộc"),

    ("005", "Bỏ trống Phòng tiếp nhận xử lý", "P0",
     FILLED.replace(", Phòng tiếp nhận PKT1", "") + "; đã thêm 1 dịch vụ",
     "1. Bấm \"Lưu và gửi duyệt\"",
     "—",
     "- Thông báo \"Thao tác thất bại\", dưới ô Phòng tiếp nhận xử lý có câu báo bắt buộc"),

    ("006", "Bảng dịch vụ không có dòng nào", "P0",
     FILLED,
     "1. Không thêm dịch vụ, bấm \"Lưu\"",
     "—",
     "- Không tạo phiếu, thông báo \"Thao tác thất bại\"\n"
     "- Lưu ý: không có câu nào nói thiếu dịch vụ; ghi Failed nếu nghiệp vụ cần câu báo rõ"),

    ("007", "Khách hàng chưa có địa chỉ", "P1",
     "KH-05 doanh nghiệp không có địa chỉ, có địa chỉ giao hàng \"Xưởng A\"",
     "1. " + OPEN_CREATE + "\n"
     "2. Chọn KH-05, người liên hệ, Địa chỉ lắp đặt \"Xưởng A\", thời gian, phòng tiếp nhận, 1 dịch vụ, bấm "
     "\"Lưu\"",
     "—",
     "- Mong đợi: lưu được, hoặc có câu báo rõ \"thiếu địa chỉ khách hàng\"\n"
     "- Lưu ý: theo code hiện tại chỉ báo \"Thao tác thất bại\", không có câu nào trên form nói lý do - ghi Failed"),

    ("008", "Thời gian dự kiến trước hôm nay", "P2",
     FILLED.replace("10/11/2026", "01/11/2026") + "; đã thêm 1 dịch vụ",
     "1. Bấm \"Lưu\"",
     "—",
     "- Lưu thành công (không chặn ngày quá khứ)\n"
     "- Lưu ý: nghiệp vụ xác nhận có cần chặn không"),

    ("009", "Ghi chú dài", "P2",
     FILLED + "; đã thêm 1 dịch vụ",
     "1. Gõ Ghi chú 300 ký tự, bấm \"Lưu\"",
     "—",
     "- Mong đợi: lưu đủ nội dung, hoặc báo giới hạn độ dài trước khi lưu\n"
     "- Lưu ý: theo code hiện tại lưu thành công nhưng ghi chú bị cắt còn 255 ký tự, không báo - ghi Failed nếu "
     "nghiệp vụ cần giữ đủ"),
]

SEC_VIII = [
    ("001", "Mở Sửa phiếu Đang tạo", "P0",
     "YC-04 do KD-1 lập, Đang tạo, KH-02, dịch vụ \"Kiểm tra định kỳ\"",
     "1. " + OPEN_KD1 + "\n"
     "2. Bấm bánh răng ở YC-04, chọn \"Sửa\"",
     "—",
     "- Form hiện đúng dữ liệu YC-04, sửa được các ô\n"
     "- Có nút Lưu, Lưu và gửi duyệt, Quay lại"),

    ("002", "Sửa rồi Lưu giữ Đang tạo", "P0",
     "Làm như TC 001",
     "1. Đổi Thời gian dự kiến sang 15/11/2026, thêm dịch vụ \"Vệ sinh máy\"\n"
     "2. Bấm \"Lưu\"",
     "—",
     "- Thông báo \"Thao tác thành công!\"\n"
     "- YC-04 vẫn Đang tạo, giữ nguyên Số phiếu\n"
     "- Mở lại: thời gian 15/11/2026, 2 dòng dịch vụ"),

    ("003", "Sửa rồi Lưu và gửi duyệt", "P0",
     "Làm như TC 001; phòng tiếp nhận của YC-04 là PKT1",
     "1. Bấm \"Lưu và gửi duyệt\"",
     "—",
     "- YC-04 chuyển \"Chờ giao việc\"\n"
     "- TP-1 nhận thông báo\n"
     "- Bánh răng ở YC-04 không còn Sửa, Xóa"),

    ("004", "Không mở được Sửa phiếu Chờ giao việc", "P0",
     "YC-01 do KD-1 lập, Chờ giao việc",
     "1. Đăng nhập KD-1, dán đường dẫn sửa YC-01",
     "—",
     "- Ra trang không tìm thấy"),

    ("005", "Người khác không mở được Sửa", "P0",
     "YC-04 do KD-1 lập, Đang tạo",
     "1. Đăng nhập KD-2, dán đường dẫn sửa YC-04",
     "—",
     "- Ra trang không tìm thấy"),

    ("006", "Phiếu Từ chối không sửa được", "P1",
     "YC-05 do KD-1 lập, Từ chối",
     "1. " + OPEN_KD1 + "\n"
     "2. Bấm bánh răng ở YC-05",
     "—",
     "- Chỉ có \"Xóa\", không có \"Sửa\"\n"
     "- Lưu ý: người lập không gửi lại được phiếu bị từ chối, phải lập phiếu mới; nghiệp vụ xác nhận"),

    ("007", "Xác nhận trước khi xóa", "P1",
     "YC-04 do KD-1 lập, Đang tạo",
     "1. " + OPEN_KD1 + "\n"
     "2. Bấm bánh răng ở YC-04, chọn \"Xóa\"",
     "—",
     "- Hiện hộp xác nhận xóa; bấm Hủy thì YC-04 vẫn còn"),

    ("008", "Xóa phiếu Đang tạo", "P0",
     "Làm như TC 007",
     "1. Bấm đồng ý xóa",
     "—",
     "- Thông báo \"Xóa thành công\"\n"
     "- YC-04 biến mất khỏi danh sách; dán lại đường dẫn chi tiết ra trang không tìm thấy"),

    ("009", "Xóa phiếu Từ chối", "P0",
     "YC-05 do KD-1 lập, Từ chối, gắn HD-05",
     "1. " + OPEN_KD1 + ", xóa YC-05\n"
     "2. Tạo mới, chọn khách của HD-05, chọn HD-05",
     "—",
     "- YC-05 biến mất\n"
     "- Chọn lại được HD-05, lấy được dịch vụ"),

    ("010", "Không xóa được phiếu Chờ giao việc / Đã giao việc", "P0",
     "YC-01 Chờ giao việc, YC-06 Đã giao việc, đều do KD-1 lập",
     "1. Đăng nhập KD-1, dán đường dẫn xóa YC-01, rồi YC-06",
     "—",
     "- Cả hai lần báo \"Không có quyền\", YC-01 và YC-06 vẫn còn"),

    ("011", "Hợp đồng của phiếu bị từ chối chưa xóa thì chưa lập lại được", "P2",
     "YC-05 Từ chối, gắn HD-05, chưa xóa",
     "1. Đăng nhập KD-1, tạo mới, chọn khách của HD-05, chọn HD-05",
     "—",
     "- Không lấy được dịch vụ (HD-05 vẫn tính là đã có phiếu yêu cầu)\n"
     "- Lưu ý: nghiệp vụ xác nhận phiếu Từ chối có nên giữ hợp đồng không"),
]
