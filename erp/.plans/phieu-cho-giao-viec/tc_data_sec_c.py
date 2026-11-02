# -*- coding: utf-8 -*-
"""Section IX - XII cho man Phieu cho giao viec."""
from tc_data_role import MENU, DATA, OPEN_TP1

DENY = "Bấm nút bánh răng dòng HD-01, chọn \"Từ chối tiếp nhận xử lý\""

SEC_IX = [
    ("001", "Hộp xác nhận từ chối tiếp nhận xử lý", "P0",
     DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. " + DENY,
     "—",
     "- Hộp \"Xác nhận!\" với câu \"Bạn chắc muốn từ chối tiếp nhận xử lý cho hợp đồng này\"\n"
     "- Ô \"Lý do từ chối\" có dấu (*)\n"
     "- Nút Xác nhận, Hủy"),

    ("002", "Bỏ trống lý do từ chối", "P0",
     DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. " + DENY + "\n"
     "3. Để trống Lý do từ chối, bấm Xác nhận",
     "Lý do từ chối: (trống)",
     "- Hiện \"Bạn phải nhập lý do từ chối tiếp nhận xử lý\"\n"
     "- Hộp vẫn mở, HD-01 không đổi"),

    ("003", "Từ chối thành công", "P0",
     DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. " + DENY + "\n"
     "3. Nhập lý do, bấm Xác nhận",
     "Lý do từ chối: Không đủ kỹ thuật viên",
     "- Thông báo \"Thao tác thành công!\", trang tự tải lại\n"
     "- Không còn HD-01 trong tab Hợp đồng\n"
     "- Chi tiết HD-01 không còn phòng tiếp nhận"),

    ("004", "Người lập hợp đồng nhận thông báo", "P0",
     "TP-1 vừa từ chối HD-01 (TC 003)\n" + DATA,
     "1. Đăng nhập KD-1, mở chuông thông báo\n"
     "2. Bấm thông báo mới",
     "—",
     "- Thông báo \"<tên TP-1> Yêu cầu cần xác nhận lại phòng tiếp nhận xử lý.\"\n"
     "- Bấm vào mở trang thay đổi phòng tiếp nhận xử lý của HD-01"),

    ("005", "Bấm Hủy ở hộp xác nhận", "P1",
     DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. " + DENY + "\n"
     "3. Nhập lý do rồi bấm Hủy",
     "—",
     "- Hộp đóng, HD-01 vẫn ở danh sách, KD-1 không nhận thông báo"),

    ("006", "Hợp đồng đã có phiếu giao việc thì không có Từ chối", "P0",
     "HD-01 đã có phiếu giao việc Chờ thực hiện 1 công, còn 1 công và dịch vụ\n" + DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm nút bánh răng dòng HD-01",
     "—",
     "- Có \"Tạo phiếu giao việc\"\n"
     "- Không có \"Từ chối tiếp nhận xử lý\""),

    ("007", "Phiếu giao việc đã Hủy vẫn chặn Từ chối", "P2",
     "HD-01 từng có 1 phiếu giao việc, phiếu đó đã bị xóa (Hủy)\n" + DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm nút bánh răng dòng HD-01",
     "—",
     "- Theo code hiện tại không có \"Từ chối tiếp nhận xử lý\"\n"
     "- Lưu ý: nếu nghiệp vụ muốn phiếu đã Hủy không tính thì ghi Failed"),

    ("008", "Gọi thẳng chức năng từ chối khi đã có phiếu giao việc", "P1",
     "HD-01 như TC 006\n" + DATA,
     "1. Đăng nhập TP-1\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng từ chối tiếp nhận xử lý cho HD-01 kèm lý do",
     "—",
     "- Mong đợi: bị chặn vì đã có phiếu giao việc\n"
     "- Lưu ý: theo code hiện tại thành công, HD-01 mất phòng tiếp nhận dù đang có phiếu giao việc - ghi "
     "Failed"),

    ("009", "Chọn lại phòng tiếp nhận sau khi bị từ chối", "P0",
     "TP-1 đã từ chối HD-01\n" + DATA,
     "1. KD-1 mở thông báo, chọn phòng tiếp nhận PKT2, lưu\n"
     "2. Đăng nhập TP-2, " + MENU,
     "—",
     "- TP-2 thấy HD-01 trong tab Hợp đồng, có \"Tạo phiếu giao việc\"\n"
     "- TP-1 không còn thấy HD-01"),
]


SEC_X = [
    ("001", "Giao một phần thì hợp đồng vẫn chờ giao", "P0",
     DATA,
     "1. TP-1 tạo phiếu giao việc từ HD-01, chỉ giao 1 công M1, không giao dịch vụ\n"
     "2. Mở lại Phiếu chờ giao việc, bấm \"Tạo phiếu giao việc\" ở HD-01",
     "—",
     "- HD-01 vẫn ở danh sách\n"
     "- Form mới chỉ còn 1 công M1 và dịch vụ \"Vệ sinh máy\" SL 1"),

    ("002", "Giao hết thì hợp đồng rời danh sách", "P0",
     DATA,
     "1. TP-1 tạo phiếu giao việc từ HD-01 giao 2 công M1 và dịch vụ\n"
     "2. Mở lại Phiếu chờ giao việc",
     "—",
     "- Không còn HD-01"),

    ("003", "Xóa phiếu giao việc thì hợp đồng quay lại", "P0",
     "HD-01 đã giao hết bằng phiếu GV-11 Chờ thực hiện\n" + DATA,
     "1. TP-1 mở danh sách Phiếu giao việc, xóa GV-11\n"
     "2. Mở lại Phiếu chờ giao việc",
     "—",
     "- GV-11 Trạng thái Hủy\n"
     "- HD-01 hiện lại, bấm Tạo phiếu giao việc thấy đủ 2 công và dịch vụ"),

    ("004", "Phiếu giao việc đã nhập kết quả vẫn giữ phần đã giao", "P1",
     "HD-01 giao hết bằng GV-12, GV-12 Đã nhập kết quả\n" + DATA,
     "1. " + OPEN_TP1,
     "—",
     "- Không có HD-01"),

    ("005", "Xóa phiếu giao việc của yêu cầu giao việc khác", "P0",
     "YC-01 đã giao bằng GV-13 Chờ thực hiện, YC-01 Đã giao việc\n" + DATA,
     "1. TP-1 xóa GV-13\n"
     "2. Mở tab Giao việc khác",
     "—",
     "- YC-01 hiện lại, Trạng thái \"Chờ giao việc\""),

    ("006", "Xóa phiếu giao việc của yêu cầu lắp đặt", "P0",
     "LD-01 đã giao đủ 3 máy bằng GV-14 Chờ thực hiện, LD-01 Đang giao việc\n" + DATA,
     "1. TP-1 xóa GV-14\n"
     "2. Mở tab Lắp đặt bàn giao",
     "—",
     "- LD-01 hiện lại, Trạng thái \"Chờ giao việc\", form giao còn đủ 3 máy"),

    ("007", "Xóa phiếu giao việc của phiếu bảo hành", "P1",
     "BH-01 đã giao hết bằng GV-15 Chờ thực hiện\n" + DATA,
     "1. TP-1 xóa GV-15\n"
     "2. Mở tab Phiếu bảo hành",
     "—",
     "- BH-01 hiện lại"),

    ("008", "PL giảm được duyệt làm giảm số còn giao", "P1",
     "HD-01 chưa giao việc; PL giảm PLG-01 giảm 2 công M1 và dịch vụ đã được duyệt\n" + DATA,
     "1. " + OPEN_TP1,
     "—",
     "- Không còn HD-01 (không còn việc để giao)"),
]


SEC_XI = [
    ("001", "Ô Phiếu chờ giao việc trên trang chủ", "P0",
     DATA,
     "1. Đăng nhập TP-1, xem trang chủ nhóm Bảo hành sửa chữa\n"
     "2. Bấm ô \"Phiếu chờ giao việc\"",
     "—",
     "- Có ô \"Phiếu chờ giao việc\"\n"
     "- Bấm mở màn Phiếu chờ giao việc"),

    ("002", "Người không có quyền Tạo phiếu giao việc không thấy ô", "P1",
     "NV-A không có quyền \"Tạo phiếu giao việc\"",
     "1. Đăng nhập NV-A, xem trang chủ",
     "—",
     "- Không có ô \"Phiếu chờ giao việc\""),

    ("003", "Số đếm bằng tổng 5 loại của phòng mình", "P0",
     DATA,
     "1. Đăng nhập TP-1, xem trang chủ",
     "—",
     "- Ô \"Phiếu chờ giao việc\" = 5 (HD-01, PL-01, BH-01, LD-01, YC-01)"),

    ("004", "Số đếm giảm khi giao hết một chứng từ", "P0",
     DATA,
     "1. TP-1 giao hết việc của HD-01\n"
     "2. Quay lại trang chủ",
     "—",
     "- Ô \"Phiếu chờ giao việc\" = 4"),

    ("005", "Ô đếm vẫn tính phiếu bảo hành đã giao hết", "P2",
     "BH-01 đã giao hết máy và dịch vụ, vẫn Đã duyệt\n" + DATA,
     "1. Đăng nhập TP-1, xem trang chủ và tab Phiếu bảo hành",
     "—",
     "- Tab Phiếu bảo hành không có BH-01\n"
     "- Mong đợi: ô đếm = 4\n"
     "- Lưu ý: theo code hiện tại ô đếm vẫn tính BH-01 nên ra 5 - ghi Failed"),

    ("006", "Ô đếm và danh sách lệch với người không phụ trách phòng", "P1",
     "KTV-1 thuộc PKT1, có quyền \"Tạo phiếu giao việc\", không phụ trách phòng nào\n" + DATA,
     "1. Đăng nhập KTV-1, xem trang chủ\n"
     "2. Bấm ô \"Phiếu chờ giao việc\"",
     "—",
     "- Ô đếm = 5\n"
     "- Tab Hợp đồng, PL bổ sung, Lắp đặt bàn giao trống\n"
     "- Mong đợi: ô đếm khớp với danh sách\n"
     "- Lưu ý: ô đếm xét phòng của chính mình, danh sách xét phòng được phân phụ trách - ghi Failed"),
]


SEC_XII = [
    ("001", "Hai tab cùng giao việc cho một hợp đồng", "P1",
     DATA,
     "1. TP-1 mở form tạo phiếu giao việc từ HD-01 ở tab A và tab B\n"
     "2. Tab A giao 2 công M1, Lưu\n"
     "3. Tab B giao 2 công M1, Lưu",
     "—",
     "- Mong đợi: tab B bị chặn vì HD-01 không còn công M1\n"
     "- Lưu ý: theo code hiện tại cả hai lưu được, M1 bị giao 4 công trên 2 - ghi Failed"),

    ("002", "Danh sách mở sẵn không tự cập nhật", "P2",
     DATA,
     "1. TP-1 mở Phiếu chờ giao việc ở tab A\n"
     "2. Ở tab B giao hết việc của HD-01\n"
     "3. Ở tab A (chưa tải lại) bấm \"Tạo phiếu giao việc\" dòng HD-01",
     "—",
     "- Tab A vẫn còn dòng HD-01 cho tới khi tải lại\n"
     "- Form mở ra báo \"Không có quyền!\", không có dữ liệu"),

    ("003", "Luồng hợp đồng: duyệt - chờ giao - giao - xóa - giao lại", "P0",
     "KD-1 lập hợp đồng HD-20 phòng tiếp nhận PKT1, còn 1 công sửa\n" + DATA,
     "1. Duyệt HD-20 sang Có hiệu lực\n"
     "2. TP-1 mở Phiếu chờ giao việc và trang chủ\n"
     "3. TP-1 tạo phiếu giao việc GV-20 giao 1 công\n"
     "4. TP-1 xóa GV-20\n"
     "5. TP-1 tạo lại phiếu giao việc cho HD-20",
     "—",
     "- Bước 2: có HD-20, ô đếm tăng 1\n"
     "- Bước 3: HD-20 rời danh sách, ô đếm giảm 1\n"
     "- Bước 4: HD-20 hiện lại\n"
     "- Bước 5: tạo được, HD-20 rời danh sách"),

    ("004", "Luồng từ chối và chuyển phòng tiếp nhận", "P0",
     DATA,
     "1. TP-1 từ chối tiếp nhận HD-01 kèm lý do\n"
     "2. KD-1 bấm thông báo, chọn phòng tiếp nhận PKT2\n"
     "3. TP-2 tạo phiếu giao việc cho HD-01",
     "—",
     "- Bước 1: HD-01 rời danh sách của TP-1\n"
     "- Bước 2: HD-01 hiện ở danh sách của TP-2\n"
     "- Bước 3: tạo thành công, HD-01 rời danh sách"),

    ("005", "Luồng yêu cầu lắp đặt bàn giao", "P1",
     "Yêu cầu lắp đặt LD-05 Chờ TP duyệt, phòng tiếp nhận PKT1, 2 máy cần lắp\n" + DATA,
     "1. Trưởng phòng duyệt LD-05\n"
     "2. TP-1 mở tab Lắp đặt bàn giao\n"
     "3. TP-1 giao 1 máy, rồi giao tiếp 1 máy",
     "—",
     "- Bước 2: có LD-05, Trạng thái \"Chờ giao việc\"\n"
     "- Sau lần giao thứ nhất: LD-05 vẫn hiện\n"
     "- Sau lần giao thứ hai: LD-05 rời danh sách, Trạng thái \"Đang giao việc\""),

    ("006", "Luồng yêu cầu giao việc khác", "P1",
     "Nhân viên lập YC-06, gửi sang Chờ giao việc, phòng tiếp nhận PKT1\n" + DATA,
     "1. TP-1 mở tab Giao việc khác\n"
     "2. Tạo phiếu giao việc cho YC-06\n"
     "3. Xóa phiếu giao việc vừa tạo",
     "—",
     "- Bước 1: có YC-06\n"
     "- Bước 2: YC-06 \"Đã giao việc\", rời danh sách\n"
     "- Bước 3: YC-06 về \"Chờ giao việc\", hiện lại"),
]
