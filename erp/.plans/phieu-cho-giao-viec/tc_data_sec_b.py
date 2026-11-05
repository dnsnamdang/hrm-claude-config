# -*- coding: utf-8 -*-
"""Section V - VIII cho man Phieu cho giao viec."""
from tc_data_role import MENU, DATA, OPEN_TP1

SEC_V = [
    ("001", "Yêu cầu lắp đặt Chờ giao việc thì hiện", "P0",
     DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm tab Lắp đặt bàn giao",
     "—",
     "- Có LD-01"),

    ("002", "Yêu cầu lắp đặt Chờ TP duyệt không hiện", "P0",
     "LD-02 Chờ TP duyệt, phòng tiếp nhận PKT1\n" + DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm tab Lắp đặt bàn giao",
     "—",
     "- Không có LD-02"),

    ("003", "Chỉ tính hàng được đánh dấu cần lắp đặt", "P1",
     "LD-03 Chờ giao việc, phòng PKT1: máy M3 SL 1 cần lắp đặt đã giao đủ; phụ kiện P1 SL 5 không đánh dấu "
     "cần lắp đặt\n" + DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm tab Lắp đặt bàn giao",
     "—",
     "- Không có LD-03"),

    ("004", "Giao một phần vẫn hiện, giao đủ thì rời danh sách", "P0",
     DATA,
     "1. TP-1 tạo phiếu giao việc cho LD-01 giao 2 máy M3\n"
     "2. Mở lại tab Lắp đặt bàn giao\n"
     "3. Tạo tiếp phiếu giao việc cho LD-01 giao 1 máy M3\n"
     "4. Mở lại tab Lắp đặt bàn giao",
     "—",
     "- Sau bước 2: LD-01 vẫn hiện, Trạng thái \"Chờ giao việc\"\n"
     "- Sau bước 4: không còn LD-01; mở chi tiết LD-01 thấy Trạng thái \"Đang giao việc\""),

    ("005", "Tạo phiếu giao việc từ yêu cầu lắp đặt mở tab mới", "P1",
     DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm tab Lắp đặt bàn giao, nút bánh răng dòng LD-01, chọn \"Tạo phiếu giao việc\"",
     "—",
     "- Mở tab trình duyệt mới, form điền sẵn 3 máy M3 cần lắp đặt"),

    ("006", "In và Xuất excel ở dòng yêu cầu lắp đặt", "P2",
     DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm tab Lắp đặt bàn giao, nút bánh răng dòng LD-01, lần lượt chọn \"In\", \"Xuất excel\"",
     "—",
     "- In: mở bản in LD-01 ở tab mới\n"
     "- Xuất excel: tải file của LD-01"),
]


SEC_VI = [
    ("001", "Yêu cầu giao việc khác Chờ giao việc thì hiện", "P0",
     DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm tab Giao việc khác",
     "—",
     "- Có YC-01, có nút \"Tạo phiếu giao việc\""),

    ("002", "Yêu cầu Đang tạo không hiện", "P1",
     "YC-03 Đang tạo, phòng tiếp nhận PKT1\n" + DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm tab Giao việc khác",
     "—",
     "- Không có YC-03"),

    ("003", "Tạo phiếu giao việc xong thì yêu cầu rời danh sách", "P0",
     DATA,
     "1. TP-1 bấm \"Tạo phiếu giao việc\" ở YC-01, nhập đủ thông tin, Lưu\n"
     "2. Mở lại tab Giao việc khác",
     "—",
     "- Không còn YC-01\n"
     "- Chi tiết YC-01 có Trạng thái \"Đã giao việc\""),

    ("004", "Người không cùng phòng tiếp nhận không có nút", "P0",
     DATA,
     "1. Đăng nhập TP-2, " + MENU + "\n"
     "2. Bấm tab Giao việc khác, nút bánh răng dòng YC-01",
     "—",
     "- Không có \"Tạo phiếu giao việc\""),

    ("005", "Yêu cầu phòng khác vẫn hiện với trưởng phòng", "P1",
     "YC-04 Chờ giao việc, phòng tiếp nhận PKT2\n" + DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm tab Giao việc khác",
     "—",
     "- Mong đợi: không có YC-04\n"
     "- Lưu ý: theo code hiện tại có YC-04 (không có nút giao) - ghi Failed"),
]


SEC_VII = [
    ("001", "Lọc Số hợp đồng ở tab Hợp đồng", "P0",
     "Thêm HD-11 Có hiệu lực, phòng PKT1, còn việc\n" + DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Mở khung tìm kiếm, gõ \"HD-01\" vào ô Số hợp đồng",
     "Số hợp đồng: HD-01",
     "- Chỉ còn HD-01"),

    ("002", "Lọc Khách hàng", "P1",
     "HD-01 của khách K1; HD-11 của khách K2\n" + DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Chọn Khách hàng K1",
     "Khách hàng: K1",
     "- Chỉ còn HD-01"),

    ("003", "Lọc Người lập", "P1",
     "HD-01 do KD-1 lập; HD-11 do KD-2 lập\n" + DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Chọn Người lập KD-1",
     "Người lập: KD-1",
     "- Chỉ còn HD-01"),

    ("004", "Lọc Người duyệt hợp đồng", "P2",
     "HD-01 do GĐ-1 duyệt; HD-11 do GĐ-2 duyệt\n" + DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Chọn Người duyệt hợp đồng GĐ-1",
     "—",
     "- Chỉ còn HD-01"),

    ("005", "Ô Trạng thái liệt kê trạng thái không dùng tới", "P2",
     DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Mở ô Trạng thái, chọn \"Chờ duyệt\"",
     "—",
     "- Bảng không có dữ liệu (tab chỉ có hợp đồng Có hiệu lực)\n"
     "- Lưu ý: ô Trạng thái nên chỉ có \"Có hiệu lực\"; ghi nhận để nghiệp vụ quyết"),

    ("006", "Từ ngày / Đến ngày ở tab Hợp đồng theo Ngày lập", "P1",
     "HD-01 lập 10/10/2026; HD-11 lập 20/10/2026\n" + DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Chọn Từ ngày 01/10/2026, Đến ngày 15/10/2026",
     "—",
     "- Chỉ còn HD-01\n"
     "- Đổi Đến ngày thành 20/10/2026: có cả HD-11 (tính trọn ngày)"),

    ("007", "Từ ngày / Đến ngày ở tab Lắp đặt bàn giao", "P2",
     "LD-01 lập 10/10/2026, ngày dự kiến 05/11/2026; LD-04 lập 20/10/2026, ngày dự kiến 25/10/2026\n" + DATA,
     "1. " + OPEN_TP1 + ", bấm tab Lắp đặt bàn giao\n"
     "2. Chọn Từ ngày 01/10/2026, Đến ngày 15/10/2026",
     "—",
     "- Mong đợi: lọc theo Ngày lập, chỉ còn LD-01\n"
     "- Lưu ý: theo code hiện tại lọc Từ ngày theo ngày dự kiến và Đến ngày không có tác dụng, ra cả LD-01 "
     "và LD-04 - ghi Failed"),

    ("008", "Từ ngày / Đến ngày ở tab Giao việc khác", "P1",
     "YC-01 lập 10/10/2026, dự kiến 01/11 - 03/11/2026\n" + DATA,
     "1. " + OPEN_TP1 + ", bấm tab Giao việc khác\n"
     "2. Chọn Từ ngày 01/10/2026, Đến ngày 15/10/2026",
     "—",
     "- Mong đợi: lọc theo Ngày lập, có YC-01\n"
     "- Lưu ý: theo code hiện tại bảng báo lỗi, không hiện dòng nào (lọc theo thông tin phiếu không có) - ghi Failed"),

    ("009", "Lọc Hàng hóa ở tab Phiếu bảo hành", "P1",
     "BH-01 có máy M2 mã MM2; BH-05 Đã duyệt, phòng PKT1, có máy M5\n" + DATA,
     "1. " + OPEN_TP1 + ", bấm tab Phiếu bảo hành\n"
     "2. Gõ \"MM2\" vào ô Hàng hóa",
     "—",
     "- Chỉ còn BH-01\n"
     "- Gõ tên \"M2\" cũng ra BH-01"),

    ("010", "Lọc Số hợp đồng ở tab Giao việc khác phải gõ đủ số", "P2",
     "YC-01 gắn hợp đồng HDB-123\n" + DATA,
     "1. " + OPEN_TP1 + ", bấm tab Giao việc khác\n"
     "2. Gõ \"HDB-12\" vào ô Số hợp đồng; sau đó gõ \"HDB-123\"",
     "—",
     "- \"HDB-12\": không có YC-01\n"
     "- \"HDB-123\": có YC-01\n"
     "- Lưu ý: các tab khác tìm được theo một phần số; ghi Failed nếu nghiệp vụ muốn giống nhau"),

    ("011", "Phân trang và STT", "P2",
     "PKT1 có 25 hợp đồng chờ giao việc\n" + DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Sang trang 2",
     "—",
     "- STT nối tiếp trang 1\n"
     "- Mới nhất ở đầu trang 1"),

    ("012", "Mỗi tab giữ bộ lọc riêng", "P2",
     DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Ở tab Hợp đồng lọc Số hợp đồng \"HD-01\"\n"
     "3. Bấm tab PL bổ sung",
     "—",
     "- Tab PL bổ sung không bị lọc theo \"HD-01\", vẫn có PL-01"),

    ("013", "Lọc Phòng ban của trưởng phòng", "P2",
     "TP-1 phụ trách PKT1; HD-01 do phòng PKD lập; HD-12 phòng tiếp nhận PKT1 do phòng PKT1 lập\n" + DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Chọn Phòng ban PKT1",
     "—",
     "- Ô Phòng ban lọc theo phòng lập hợp đồng: chỉ còn HD-12"),
]


SEC_VIII = [
    ("001", "Tạo phiếu giao việc từ hợp đồng", "P0",
     DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm nút bánh răng dòng HD-01, chọn \"Tạo phiếu giao việc\"",
     "—",
     "- Mở form tạo phiếu giao việc trên tab hiện tại\n"
     "- Điền sẵn hợp đồng HD-01, khách hàng, máy M1 serial S1 2 công, dịch vụ \"Vệ sinh máy\" SL 1"),

    ("002", "Hợp đồng đang có PL giảm chờ duyệt thì không cho tạo", "P0",
     "HD-05 Có hiệu lực, phòng PKT1, còn việc, có PL giảm PLG-05 Chờ duyệt\n" + DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm nút bánh răng dòng HD-05, chọn \"Tạo phiếu giao việc\"",
     "—",
     "- Thông báo \"Hợp đồng đang có PL giảm chờ duyệt!\"\n"
     "- Vẫn ở danh sách, không mở form"),

    ("003", "PL giảm đã duyệt thì tạo được", "P1",
     "PLG-05 của HD-05 đã được duyệt\n" + DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm \"Tạo phiếu giao việc\" ở HD-05",
     "—",
     "- Mở form tạo phiếu giao việc"),

    ("004", "Mở thẳng form khi đang có PL giảm chờ duyệt", "P1",
     "HD-05 như TC 002\n" + DATA,
     "1. Đăng nhập TP-1\n"
     "2. Dán đường dẫn form tạo phiếu giao việc cho HD-05, nhập đủ thông tin, Lưu",
     "—",
     "- Mong đợi: bị chặn với thông báo PL giảm chờ duyệt\n"
     "- Lưu ý: theo code hiện tại chỉ chặn khi bấm từ danh sách, form vẫn mở và lưu được - ghi Failed"),

    ("005", "Mở thẳng form cho hợp đồng phòng khác", "P0",
     DATA,
     "1. Đăng nhập TP-1\n"
     "2. Dán đường dẫn form tạo phiếu giao việc cho HD-02",
     "—",
     "- Thông báo \"Không có quyền!\", form không có dữ liệu hợp đồng"),

    ("006", "Lưu phiếu giao việc thành công", "P0",
     DATA,
     "1. TP-1 bấm \"Tạo phiếu giao việc\" ở HD-01\n"
     "2. Chọn ngày dự kiến bắt đầu và kết thúc từ hôm nay, giao 2 công M1 và dịch vụ, bấm \"Lưu & duyệt\"",
     "—",
     "- Thông báo \"Tạo phiếu giao việc thành công!\"\n"
     "- Chuyển sang danh sách Phiếu giao việc, phiếu mới Trạng thái \"Chờ thực hiện\"\n"
     "- Mở lại Phiếu chờ giao việc: không còn HD-01"),

    ("007", "Ngày bắt đầu dự kiến trước hôm nay", "P1",
     DATA,
     "1. TP-1 mở form tạo phiếu giao việc từ HD-01\n"
     "2. Chọn Ngày bắt đầu là hôm qua, bấm Lưu",
     "—",
     "- Báo \"Ngày bắt đầu phải lớn hơn hoặc bằng ngày hiện tại\", không tạo phiếu"),

    ("008", "Ngày kết thúc trước ngày bắt đầu", "P1",
     DATA,
     "1. TP-1 mở form tạo phiếu giao việc từ HD-01\n"
     "2. Chọn Ngày bắt đầu 05/11/2026, Ngày kết thúc 04/11/2026, bấm Lưu",
     "—",
     "- Báo \"Ngày kết thúc phải lớn hơn hoặc bằng ngày hiện tại và ngày bắt đầu\", không tạo phiếu"),

    ("009", "Trưởng phòng bị chặn vì phòng có nhân viên quá hạn", "P1",
     "Cấu hình chặn quá hạn bật cho hành động \"Tạo phiếu giao việc\"; phòng PKT1 có nhân viên quá hạn\n" + DATA,
     "1. TP-1 mở form tạo phiếu giao việc từ HD-01, nhập đủ, bấm Lưu",
     "—",
     "- Hiện thông báo chặn quá hạn kèm danh sách quá hạn\n"
     "- Không tạo phiếu, HD-01 vẫn ở danh sách chờ"),
]
