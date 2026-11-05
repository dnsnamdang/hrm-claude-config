# -*- coding: utf-8 -*-
"""Section IX - XII cho man Phieu yeu cau giao viec khac."""
from tc_data_role import MENU, MENU_CHO, DATA, OPEN_KD1

Y01 = ("YC-01 do KD-1 lập: KH-01, HD-01, 3 dòng dịch vụ (Vệ sinh máy, Bảo trì định kỳ, Hướng dẫn sử dụng), "
       "phòng tiếp nhận PKT1, Chờ giao việc")
OPEN_Y01_TP1 = "Đăng nhập TP-1, bấm thông báo của YC-01 (hoặc dán đường dẫn chi tiết YC-01)"

SEC_IX = [
    ("001", "Người lập xem chi tiết", "P0",
     Y01,
     "1. " + OPEN_KD1 + "\n"
     "2. Bấm Số phiếu YC-01",
     "—",
     "- Tiêu đề \"Phiếu yêu cầu giao việc khác <số phiếu>\"\n"
     "- Đủ thông tin đã nhập, các ô không sửa được\n"
     "- Không có Lưu, Lưu và gửi duyệt, Thêm dịch vụ\n"
     "- Không có \"Tạo phiếu giao việc\", \"Không duyệt\"; có \"Quay lại\""),

    ("002", "Phòng tiếp nhận mở chi tiết phiếu Chờ giao việc", "P0",
     Y01 + "; TP-1 thuộc PKT1, không có quyền xem phiếu yêu cầu giao việc khác",
     "1. " + OPEN_Y01_TP1,
     "—",
     "- Mở được chi tiết YC-01\n"
     "- Có khung \"Ghi chú duyệt\" nhập được\n"
     "- Có nút \"Tạo phiếu giao việc\", \"Không duyệt\", \"Quay lại\""),

    ("003", "Người khác phòng tiếp nhận không mở được", "P0",
     Y01 + "; KT-9 thuộc phòng kỹ thuật khác, không có quyền xem",
     "1. Đăng nhập KT-9, dán đường dẫn chi tiết YC-01",
     "—",
     "- Ra trang không tìm thấy"),

    ("004", "Quyền theo công ty xem chi tiết phiếu công ty mình", "P1",
     Y01 + "; QL-C có quyền theo công ty, thuộc TPE",
     "1. Đăng nhập QL-C, " + MENU + ", bấm Số phiếu YC-01",
     "—",
     "- Mở được chi tiết, không có \"Tạo phiếu giao việc\", \"Không duyệt\""),

    ("005", "Quyền theo công ty không xem được phiếu công ty khác", "P1",
     "QL-C có quyền theo công ty, thuộc TPE; YC-09 của TPC",
     "1. Đăng nhập QL-C, dán đường dẫn chi tiết YC-09",
     "—",
     "- Ra trang không tìm thấy"),

    ("006", "Phiếu Đang tạo chỉ người lập xem được", "P0",
     "YC-04 do KD-1 lập, Đang tạo; QL-T có quyền tổng công ty",
     "1. Đăng nhập QL-T, dán đường dẫn chi tiết YC-04",
     "—",
     "- Ra trang không tìm thấy"),

    ("007", "Người lập xem lý do bị từ chối", "P0",
     "YC-05 do KD-1 lập, bị TP-1 Không duyệt với ghi chú \"Không thuộc phạm vi PKT1\"",
     "1. " + OPEN_KD1 + ", bấm Số phiếu YC-05",
     "—",
     "- Trạng thái Từ chối\n"
     "- Khung \"Ghi chú duyệt\" hiện \"Không thuộc phạm vi PKT1\", không sửa được"),

    ("008", "Phiếu chưa có ghi chú duyệt thì không hiện khung", "P2",
     Y01,
     "1. " + OPEN_KD1 + ", bấm Số phiếu YC-01",
     "—",
     "- Không có khung \"Ghi chú duyệt\""),

    ("009", "Màn chi tiết không đổi được dữ liệu", "P2",
     "YC-04 do KD-1 lập, không có hợp đồng, 1 dòng \"Kiểm tra định kỳ\"; YC-01 có HD-01",
     "1. KD-1 mở chi tiết YC-01, YC-04\n"
     "2. Thử bấm nút tìm Người liên hệ, ô tích, dấu x ở dòng dịch vụ",
     "—",
     "- Mong đợi: màn chi tiết chỉ xem, không có các nút này\n"
     "- Lưu ý: theo code hiện tại vẫn có nút tìm Người liên hệ, ô tích bấm được, YC-04 còn dấu x bỏ dòng (không "
     "lưu, tải lại trang thì về như cũ) - ghi Failed"),

    ("010", "Phòng QTC, Nhân viên QTC theo hợp đồng", "P2",
     Y01 + "; HD-01 có Phòng QTC PKD1, Nhân viên QTC KD-1",
     "1. KD-1 mở chi tiết YC-01",
     "—",
     "- Phòng QTC PKD1, Nhân viên QTC KD-1; phiếu không hợp đồng thì 2 ô trống"),
]

SEC_X = [
    ("001", "Không duyệt khi chưa nhập ghi chú", "P0",
     Y01,
     "1. " + OPEN_Y01_TP1 + "\n"
     "2. Để trống Ghi chú duyệt, bấm \"Không duyệt\"",
     "—",
     "- Thông báo \"Tạo thất bại!\", dưới khung Ghi chú duyệt có câu báo bắt buộc\n"
     "- YC-01 vẫn Chờ giao việc\n"
     "- Lưu ý: chữ \"Tạo thất bại!\" không hợp với thao tác Không duyệt; ghi Failed nếu nghiệp vụ cần câu đúng"),

    ("002", "Không duyệt có ghi chú", "P0",
     Y01,
     "1. " + OPEN_Y01_TP1 + "\n"
     "2. Nhập Ghi chú duyệt \"Không thuộc phạm vi PKT1\", bấm \"Không duyệt\"",
     "—",
     "- Thông báo \"Thao tác thành công!\", về Danh sách phiếu yêu cầu giao việc khác\n"
     "- YC-01 chuyển \"Từ chối\"\n"
     "- YC-01 không còn ở Phiếu chờ giao việc, tab Giao việc khác"),

    ("003", "Người lập nhận thông báo khi bị từ chối", "P1",
     "Làm như TC 002",
     "1. Đăng nhập KD-1, mở chuông thông báo",
     "—",
     "- Mong đợi: có thông báo YC-01 bị từ chối, bấm mở chi tiết\n"
     "- Lưu ý: theo code hiện tại không gửi thông báo nào - ghi Failed"),

    ("004", "Sau từ chối người lập chỉ còn Xóa", "P0",
     "Làm như TC 002",
     "1. " + OPEN_KD1 + ", bấm bánh răng ở YC-01",
     "—",
     "- Chỉ có \"Xóa\""),

    ("005", "Phòng tiếp nhận không mở lại được phiếu đã từ chối", "P1",
     "Làm như TC 002; TP-1 không có quyền xem",
     "1. Đăng nhập TP-1, dán đường dẫn chi tiết YC-01",
     "—",
     "- Ra trang không tìm thấy"),

    ("006", "Nhân viên phòng tiếp nhận không có quyền giao việc vẫn Không duyệt được", "P1",
     Y01 + "; KTV-1 thuộc PKT1, không có quyền \"Tạo phiếu giao việc\"",
     "1. Đăng nhập KTV-1, dán đường dẫn chi tiết YC-01",
     "—",
     "- Theo code hiện tại: thấy \"Tạo phiếu giao việc\", \"Không duyệt\" và Không duyệt được\n"
     "- Ghi Failed nếu nghiệp vụ chỉ cho người có quyền \"Tạo phiếu giao việc\" xử lý"),

    ("007", "Gọi thẳng Không duyệt phiếu Đã giao việc", "P1",
     "YC-06 Đã giao việc, đã có phiếu giao việc PGV-06",
     "1. Đăng nhập TP-1, dùng công cụ kiểm thử API gọi thẳng chức năng Không duyệt YC-06 với ghi chú \"test\"",
     "—",
     "- Mong đợi: bị chặn, YC-06 vẫn Đã giao việc\n"
     "- Lưu ý: theo code hiện tại YC-06 chuyển Từ chối dù đã có PGV-06, người lập còn xóa được YC-06 - ghi "
     "Failed"),

    ("008", "Gọi thẳng Không duyệt phiếu Đang tạo", "P2",
     "YC-04 do KD-1 lập, Đang tạo",
     "1. Đăng nhập TP-1, dùng công cụ kiểm thử API gọi thẳng chức năng Không duyệt YC-04",
     "—",
     "- Mong đợi: bị chặn\n"
     "- Lưu ý: theo code hiện tại YC-04 chuyển Từ chối, KD-1 không sửa tiếp được - ghi Failed"),
]

SEC_XI = [
    ("001", "Phiếu gửi duyệt hiện ở Phiếu chờ giao việc", "P0",
     Y01,
     "1. Đăng nhập TP-1, " + MENU_CHO + ", chọn tab Giao việc khác",
     "—",
     "- Có YC-01, nút bánh răng có \"Tạo phiếu giao việc\""),

    ("002", "Tạo phiếu giao việc từ màn chi tiết yêu cầu", "P0",
     Y01,
     "1. " + OPEN_Y01_TP1 + "\n"
     "2. Bấm \"Tạo phiếu giao việc\"",
     "—",
     "- Mở form phiếu giao việc, thông báo \"Lấy dữ liệu thành công\"\n"
     "- Khách hàng KH-01, hợp đồng HD-01, ô \"Phiếu YC giao việc khác\" là YC-01\n"
     "- Người yêu cầu KD-1 kèm số điện thoại của KD-1\n"
     "- Có 3 dòng dịch vụ của YC-01"),

    ("003", "Dòng bỏ tích cần giao không sang phiếu giao việc", "P1",
     "YC-02 Chờ giao việc, phòng tiếp nhận PKT1, 3 dòng, dòng \"Bảo trì định kỳ\" bỏ tích",
     "1. Đăng nhập TP-1, mở chi tiết YC-02, bấm \"Tạo phiếu giao việc\"",
     "—",
     "- Mong đợi: form chỉ có 2 dòng đã tích\n"
     "- Lưu ý: theo code hiện tại có đủ 3 dòng, kể cả \"Bảo trì định kỳ\" - ghi Failed"),

    ("004", "Lưu phiếu giao việc chuyển yêu cầu sang Đã giao việc", "P0",
     Y01,
     "1. Làm như TC 002, điền đủ, bấm \"Lưu & duyệt\"\n"
     "2. KD-1 mở danh sách Phiếu yêu cầu giao việc khác",
     "—",
     "- YC-01 Trạng thái \"Đã giao việc\"\n"
     "- YC-01 rời Phiếu chờ giao việc, tab Giao việc khác"),

    ("005", "Phiếu Đã giao việc không còn nút xử lý", "P0",
     "Làm như TC 004; TP-1 có quyền \"Xem phiếu yêu cầu giao việc khác theo công ty\"",
     "1. Đăng nhập TP-1, mở chi tiết YC-01",
     "—",
     "- Không có \"Tạo phiếu giao việc\", \"Không duyệt\", không có khung Ghi chú duyệt nhập được"),

    ("006", "Phòng tiếp nhận mở yêu cầu từ phiếu giao việc sau khi đã giao", "P1",
     "Làm như TC 004; TP-1 không có quyền xem phiếu yêu cầu giao việc khác",
     "1. Đăng nhập TP-1, mở phiếu giao việc vừa lập, bấm số YC-01 ở ô \"Phiếu YC giao việc khác\"",
     "—",
     "- Mong đợi: mở được chi tiết YC-01\n"
     "- Lưu ý: theo code hiện tại ra trang không tìm thấy (phòng tiếp nhận chỉ xem được khi phiếu còn Chờ giao "
     "việc) - ghi Failed"),

    ("007", "Xóa phiếu giao việc trả yêu cầu về Chờ giao việc", "P0",
     "Làm như TC 004; phiếu giao việc PGV-01 chưa có phiếu công tác",
     "1. Đăng nhập TP-1, xóa PGV-01\n"
     "2. KD-1 mở danh sách Phiếu yêu cầu giao việc khác",
     "—",
     "- YC-01 về \"Chờ giao việc\"\n"
     "- YC-01 có lại ở Phiếu chờ giao việc, tab Giao việc khác"),

    ("008", "Người lập không tạo được phiếu giao việc", "P1",
     Y01,
     "1. Đăng nhập KD-1, dán đường dẫn tạo phiếu giao việc từ YC-01",
     "—",
     "- Thông báo \"Không có quyền!\", form không có dữ liệu YC-01"),

    ("009", "Phiếu Đang tạo không sang Phiếu chờ giao việc", "P0",
     "YC-04 do KD-1 lập, Đang tạo, phòng tiếp nhận PKT1",
     "1. Đăng nhập TP-1, " + MENU_CHO + ", chọn tab Giao việc khác",
     "—",
     "- Không có YC-04"),
]

SEC_XII = [
    ("001", "Một người giao việc, người khác cùng lúc Không duyệt", "P1",
     Y01 + "; TP-1, TP-2 cùng thuộc PKT1, cùng mở chi tiết YC-01",
     "1. TP-1 bấm \"Tạo phiếu giao việc\", lưu thành công\n"
     "2. TP-2 (chưa tải lại trang) nhập ghi chú, bấm \"Không duyệt\"",
     "—",
     "- Mong đợi: TP-2 bị chặn vì YC-01 đã giao việc\n"
     "- Lưu ý: theo code hiện tại YC-01 chuyển Từ chối dù đã có phiếu giao việc - ghi Failed"),

    ("002", "Người lập xóa yêu cầu sau khi bị từ chối nhầm", "P1",
     "Làm như TC 001 (YC-01 Từ chối, đã có phiếu giao việc PGV-01)",
     "1. KD-1 xóa YC-01\n"
     "2. TP-1 mở PGV-01",
     "—",
     "- Mong đợi: không xóa được yêu cầu đã có phiếu giao việc\n"
     "- Lưu ý: theo code hiện tại xóa được, PGV-01 mất liên kết, ô \"Phiếu YC giao việc khác\" trống - ghi "
     "Failed"),

    ("003", "Hai người cùng tạo phiếu giao việc từ một yêu cầu", "P1",
     Y01 + "; TP-1, TP-2 cùng mở form tạo phiếu giao việc từ YC-01",
     "1. TP-1 lưu, rồi TP-2 lưu",
     "—",
     "- Mong đợi: TP-2 bị chặn\n"
     "- Lưu ý: theo code hiện tại lưu được 2 phiếu giao việc cho YC-01 (đã ghi ở bộ Phiếu chờ giao việc) - ghi "
     "Failed"),

    ("004", "Hai người cùng chọn một hợp đồng ở hai form", "P1",
     "KD-1 mở 2 tab tạo mới, cả 2 chọn KH-01 và HD-01 (lúc này HD-01 chưa có phiếu yêu cầu)",
     "1. Tab 1 bấm \"Lưu và gửi duyệt\"\n"
     "2. Tab 2 bấm \"Lưu và gửi duyệt\"",
     "—",
     "- Mong đợi: tab 2 bị chặn vì HD-01 đã có phiếu yêu cầu\n"
     "- Lưu ý: theo code hiện tại tạo được 2 phiếu cho HD-01 - ghi Failed"),

    ("005", "Hai người bấm Lưu đúng cùng lúc", "P2",
     "KD-1 và KD-2 đều đã điền xong form tạo mới",
     "1. Hai người bấm \"Lưu\" cùng một lúc",
     "—",
     "- Mong đợi: cả hai phiếu tạo thành công, số phiếu khác nhau\n"
     "- Lưu ý: có thể một người nhận thông báo lỗi kỹ thuật khó hiểu, phiếu không được tạo - ghi Failed nếu "
     "gặp"),

    ("006", "Luồng đầu - cuối: tạo, gửi, giao việc", "P0",
     DATA,
     "1. KD-1 tạo phiếu: KH-01, Anh Bình, Thời gian dự kiến 10/11/2026, Địa chỉ lắp đặt \"12 Lê Lợi\", Phòng "
     "tiếp nhận PKT1, HD-01, bấm \"Lưu\"\n"
     "2. KD-1 mở Sửa, bấm \"Lưu và gửi duyệt\"\n"
     "3. TP-1 bấm thông báo, bấm \"Tạo phiếu giao việc\", lưu phiếu giao việc\n"
     "4. KD-1 xem danh sách",
     "—",
     "- Bước 1: Đang tạo, TP-1 chưa có thông báo\n"
     "- Bước 2: Chờ giao việc, TP-1 có thông báo\n"
     "- Bước 3: phiếu giao việc có 3 dòng dịch vụ của HD-01\n"
     "- Bước 4: phiếu Đã giao việc, không còn Sửa, Xóa"),

    ("007", "Luồng đầu - cuối: từ chối, xóa, lập lại", "P0",
     DATA,
     "1. KD-1 tạo phiếu với HD-01, \"Lưu và gửi duyệt\"\n"
     "2. TP-1 Không duyệt với ghi chú \"Sai phòng, gửi PKT2\"\n"
     "3. KD-1 xem chi tiết, rồi xóa phiếu\n"
     "4. KD-1 tạo phiếu mới với HD-01, Phòng tiếp nhận PKT2, \"Lưu và gửi duyệt\"",
     "—",
     "- Bước 2: phiếu Từ chối\n"
     "- Bước 3: thấy ghi chú \"Sai phòng, gửi PKT2\"; xóa thành công\n"
     "- Bước 4: chọn lại được HD-01, phiếu mới Chờ giao việc, người PKT2 có quyền giao việc nhận thông báo"),

    ("008", "Luồng đầu - cuối: giao việc, xóa phiếu giao việc, giao lại", "P1",
     Y01,
     "1. TP-1 tạo phiếu giao việc PGV-01 từ YC-01\n"
     "2. TP-1 xóa PGV-01\n"
     "3. TP-1 tạo lại phiếu giao việc từ YC-01",
     "—",
     "- Bước 1: YC-01 Đã giao việc\n"
     "- Bước 2: YC-01 Chờ giao việc\n"
     "- Bước 3: tạo được, YC-01 Đã giao việc"),
]
