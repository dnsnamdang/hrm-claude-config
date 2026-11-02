# -*- coding: utf-8 -*-
"""Section I - IV cho man Phieu cho giao viec."""
from tc_data_role import MENU, DATA, OPEN_TP1

SEC_I = [
    ("001", "Bố cục màn Phiếu chờ giao việc", "P0",
     DATA,
     "1. " + OPEN_TP1,
     "Tài khoản: TP-1",
     "- Tiêu đề trang \"Danh sách phiếu chờ giao việc\"\n"
     "- 5 tab theo thứ tự: Hợp đồng, PL bổ sung, Phiếu bảo hành, Lắp đặt bàn giao, Giao việc khác; tab Hợp "
     "đồng mở sẵn\n"
     "- Tab không có số đếm\n"
     "- Không có nút Tạo mới, In, Xuất Excel"),

    ("002", "Cột tab Hợp đồng", "P0",
     DATA,
     "1. " + OPEN_TP1,
     "—",
     "- Cột: STT, Mã phiếu, Tổng thanh toán, Khách hàng, Người liên hệ - SĐT, Người lập, Ngày lập, Người "
     "duyệt, Ngày duyệt, Trạng thái, Hành động\n"
     "- Dòng HD-01: Khách hàng dạng \"<mã KH> - <tên KH>\", Ngày lập dạng ngày/tháng/năm - giờ:phút, Trạng "
     "thái \"Có hiệu lực\""),

    ("003", "Cột tab PL bổ sung", "P1",
     DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm tab PL bổ sung",
     "—",
     "- Cùng các cột như tab Hợp đồng\n"
     "- Có dòng PL-01, Trạng thái \"Có hiệu lực\""),

    ("004", "Cột tab Phiếu bảo hành", "P1",
     DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm tab Phiếu bảo hành",
     "—",
     "- Cột: STT, Mã phiếu, Khách hàng, Người liên hệ - SĐT, Người lập, Ngày lập, Trạng thái, Hành động\n"
     "- Dòng BH-01 Trạng thái \"Đã duyệt\""),

    ("005", "Cột tab Lắp đặt bàn giao", "P1",
     DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm tab Lắp đặt bàn giao",
     "—",
     "- Cột: STT, Số phiếu, Số hợp đồng, Khách hàng, Người lập, Ngày lập, Trạng thái, Hành động\n"
     "- Người lập kèm số điện thoại; Trạng thái LD-01 \"Chờ giao việc\""),

    ("006", "Cột tab Giao việc khác", "P1",
     DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm tab Giao việc khác",
     "—",
     "- Cột: STT, Số phiếu, Số hợp đồng, Khách hàng, Người lập, Ngày lập, Trạng thái, Hành động\n"
     "- Dòng YC-01 Trạng thái \"Chờ giao việc\""),

    ("007", "Mã phiếu nào bấm mở được", "P1",
     DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Lần lượt bấm vào mã phiếu ở từng tab",
     "—",
     "- Tab Hợp đồng, PL bổ sung: Mã phiếu là chữ thường, bấm không mở gì\n"
     "- Tab Phiếu bảo hành: mở chi tiết BH-01\n"
     "- Tab Lắp đặt bàn giao: Số phiếu mở chi tiết LD-01, Số hợp đồng mở hợp đồng bán hàng"),

    ("008", "Tab chỉ tải khi bấm lần đầu", "P2",
     DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm tab Phiếu bảo hành, rồi quay lại tab Hợp đồng, rồi bấm lại tab Phiếu bảo hành",
     "—",
     "- Lần đầu bấm tab mới tải bảng\n"
     "- Quay lại tab đã mở thì bảng giữ nguyên, không tải lại từ đầu"),
]


SEC_II = [
    ("001", "Hợp đồng Có hiệu lực còn việc chưa giao thì hiện", "P0",
     DATA,
     "1. " + OPEN_TP1,
     "—",
     "- Tab Hợp đồng có HD-01"),

    ("002", "Hợp đồng Chờ duyệt không hiện", "P0",
     "HD-04 Chờ duyệt, phòng tiếp nhận PKT1\n" + DATA,
     "1. " + OPEN_TP1,
     "—",
     "- Không có HD-04"),

    ("003", "Hợp đồng đã giao hết việc không hiện", "P0",
     "HD-03 Có hiệu lực, phòng tiếp nhận PKT1, 1 công sửa, đã có phiếu giao việc GV-03 Chờ thực hiện 1 công\n" + DATA,
     "1. " + OPEN_TP1,
     "—",
     "- Không có HD-03"),

    ("004", "Hợp đồng phòng tiếp nhận khác không hiện", "P0",
     DATA,
     "1. " + OPEN_TP1,
     "—",
     "- Không có HD-02"),

    ("005", "Hợp đồng chỉ còn dịch vụ chưa giao vẫn hiện", "P0",
     "HD-01 đã có phiếu giao việc giao đủ 2 công M1, chưa giao \"Vệ sinh máy\"\n" + DATA,
     "1. " + OPEN_TP1,
     "—",
     "- HD-01 vẫn hiện"),

    ("006", "Hợp đồng chỉ còn vật tư chưa giao", "P2",
     "HD-06 Có hiệu lực, phòng tiếp nhận PKT1: công và dịch vụ đã giao hết, còn vật tư V1 SL 2 chưa giao\n"
     + DATA,
     "1. " + OPEN_TP1,
     "—",
     "- Mong đợi: theo nghiệp vụ, nếu vật tư cần giao thì HD-06 hiện\n"
     "- Lưu ý: danh sách không xét vật tư nên HD-06 không hiện, trong khi mở form theo đường dẫn vẫn giao "
     "được - ghi Failed nếu vật tư cần giao"),

    ("007", "Hợp đồng Đóng / Đã hoàn thành không hiện", "P1",
     "HD-07 Đóng, HD-08 Đã hoàn thành, đều phòng tiếp nhận PKT1, còn công chưa giao\n" + DATA,
     "1. " + OPEN_TP1,
     "—",
     "- Không có HD-07, HD-08"),

    ("008", "PL bổ sung không lẫn vào tab Hợp đồng", "P1",
     DATA,
     "1. " + OPEN_TP1,
     "—",
     "- Tab Hợp đồng không có PL-01"),

    ("009", "Tab chờ giao việc chỉ nên có thao tác giao việc", "P2",
     "SA có vai trò Super Admin và quyền \"Xem danh sách phiếu chờ giao việc theo tổng công ty\"; HD-01 chưa "
     "có phiếu giao việc\n" + DATA,
     "1. Đăng nhập SA, mở màn\n"
     "2. Bấm nút bánh răng ở dòng HD-01",
     "—",
     "- Mong đợi: chỉ có \"Tạo phiếu giao việc\", \"Từ chối tiếp nhận xử lý\"\n"
     "- Lưu ý: theo code hiện tại còn có \"Đóng hợp đồng\", \"Hủy duyệt hợp đồng\", \"Quản lý vận chuyển\" "
     "(và \"Quyết toán hợp đồng\" khi đủ điều kiện) - ghi Failed nếu nghiệp vụ không muốn"),
]


SEC_III = [
    ("001", "PL bổ sung Có hiệu lực còn việc thì hiện", "P0",
     DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm tab PL bổ sung",
     "—",
     "- Có PL-01"),

    ("002", "PL bổ sung Chờ duyệt không hiện", "P0",
     "PL-02 PL bổ sung Chờ duyệt, phòng tiếp nhận PKT1\n" + DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm tab PL bổ sung",
     "—",
     "- Không có PL-02"),

    ("003", "PL bổ sung phòng khác không hiện", "P1",
     "PL-03 Có hiệu lực, phòng tiếp nhận PKT2\n" + DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm tab PL bổ sung",
     "—",
     "- Không có PL-03"),

    ("004", "Tạo phiếu giao việc từ PL bổ sung", "P0",
     DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm tab PL bổ sung, nút bánh răng dòng PL-01, chọn \"Tạo phiếu giao việc\"",
     "—",
     "- Mở form tạo phiếu giao việc ngay trên tab hiện tại\n"
     "- Form điền sẵn theo PL-01: 1 công sửa M1"),

    ("005", "PL bổ sung đã có phiếu giao việc vẫn hiện Từ chối", "P2",
     "PL-01 có 2 công, đã có phiếu giao việc Chờ thực hiện 1 công\n" + DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm tab PL bổ sung, nút bánh răng dòng PL-01",
     "—",
     "- Mong đợi: giống tab Hợp đồng, không có \"Từ chối tiếp nhận xử lý\" khi đã có phiếu giao việc\n"
     "- Lưu ý: theo code hiện tại vẫn có nút - ghi Failed"),
]


SEC_IV = [
    ("001", "Phiếu bảo hành Đã duyệt còn máy chưa giao thì hiện", "P0",
     DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm tab Phiếu bảo hành",
     "—",
     "- Có BH-01"),

    ("002", "Phiếu bảo hành Đang tạo không hiện", "P0",
     "BH-03 Đang tạo\n" + DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm tab Phiếu bảo hành",
     "—",
     "- Không có BH-03"),

    ("003", "Phiếu bảo hành đã giao hết không hiện", "P0",
     "BH-01 đã có phiếu giao việc giao đủ máy M2 và dịch vụ\n" + DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm tab Phiếu bảo hành",
     "—",
     "- Không có BH-01"),

    ("004", "Phiếu bảo hành phòng khác vẫn hiện với trưởng phòng", "P1",
     "BH-04 Đã duyệt, phòng tiếp nhận PKT2\n" + DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm tab Phiếu bảo hành",
     "—",
     "- Mong đợi: không có BH-04\n"
     "- Lưu ý: theo code hiện tại có BH-04 - ghi Failed"),

    ("005", "Nút Tạo phiếu giao việc luôn hiện ở tab Phiếu bảo hành", "P1",
     "NV-A không có quyền \"Tạo phiếu giao việc\"\n" + DATA,
     "1. Đăng nhập NV-A, " + MENU + "\n"
     "2. Bấm tab Phiếu bảo hành, nút bánh răng dòng BH-01, chọn \"Tạo phiếu giao việc\"",
     "—",
     "- Mong đợi: NV-A không có nút\n"
     "- Lưu ý: theo code hiện tại nút luôn hiện; bấm vào form báo \"Không có quyền!\" và không có dữ liệu - "
     "ghi Failed"),

    ("006", "Tạo phiếu giao việc từ phiếu bảo hành", "P0",
     DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm tab Phiếu bảo hành, nút bánh răng dòng BH-01, chọn \"Tạo phiếu giao việc\"",
     "—",
     "- Mở form tạo phiếu giao việc điền sẵn theo BH-01, có máy M2"),

    ("007", "Tab Phiếu bảo hành không có Từ chối tiếp nhận xử lý", "P2",
     DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm tab Phiếu bảo hành, nút bánh răng dòng BH-01",
     "—",
     "- Chỉ có \"Tạo phiếu giao việc\""),
]
