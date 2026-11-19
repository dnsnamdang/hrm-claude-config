# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Phieu cho giao viec'."""

MENU = "Mở menu Bảo hành sửa chữa > mục \"Giao việc\" > bấm \"Phiếu chờ giao việc\""

# Du lieu mau dung chung
DATA = ("Công ty TPE có phòng PKT1, PKT2 (kỹ thuật) và PKD (kinh doanh).\n"
        "- TP-1: thuộc PKT1, được phân phụ trách phòng PKT1, có quyền \"Tạo phiếu giao việc\"\n"
        "- TP-2: thuộc PKT2, phụ trách PKT2, có quyền \"Tạo phiếu giao việc\"\n"
        "- KD-1: nhân viên PKD, người lập hợp đồng\n"
        "Chứng từ:\n"
        "- HD-01: hợp đồng dịch vụ SC - BH Có hiệu lực, phòng tiếp nhận PKT1, máy M1 serial S1 sửa 2 công, "
        "dịch vụ \"Vệ sinh máy\" SL 1, chưa giao việc\n"
        "- HD-02: Có hiệu lực, phòng tiếp nhận PKT2, chưa giao việc\n"
        "- PL-01: PL bổ sung của HD-01, Có hiệu lực, phòng tiếp nhận PKT1, thêm 1 công sửa M1\n"
        "- BH-01: phiếu bảo hành Đã duyệt của TPE, phòng tiếp nhận PKT1, máy M2 chưa giao\n"
        "- LD-01: yêu cầu lắp đặt bàn giao Chờ giao việc, phòng tiếp nhận PKT1, 3 máy M3 cần lắp đặt\n"
        "- YC-01: yêu cầu giao việc khác Chờ giao việc, phòng tiếp nhận PKT1")

OPEN_TP1 = "Đăng nhập TP-1, " + MENU

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Phiếu chờ giao việc: nơi trưởng phòng kỹ thuật (phòng tiếp nhận xử lý) xem các chứng từ còn việc chưa "
     "giao cho kỹ thuật viên, rồi bấm \"Tạo phiếu giao việc\" hoặc \"Từ chối tiếp nhận xử lý\".\n"
     "Màn gồm 5 tab: Hợp đồng, PL bổ sung, Phiếu bảo hành, Lắp đặt bàn giao, Giao việc khác. Màn chỉ là danh "
     "sách, không có Tạo mới, In, Xuất Excel; việc giao làm ở form Phiếu giao việc."),

    ("2. Đối tượng được tính / hiển thị",
     "- Tab Hợp đồng / PL bổ sung: chứng từ Có hiệu lực, còn công sửa chữa hoặc dịch vụ chưa giao (đã trừ "
     "phần PL giảm và phần đang nằm trong phiếu giao việc chưa hủy).\n"
     "- Tab Phiếu bảo hành: phiếu Đã duyệt còn máy / dịch vụ chưa giao.\n"
     "- Tab Lắp đặt bàn giao: yêu cầu Chờ giao việc còn máy cần lắp đặt chưa giao.\n"
     "- Tab Giao việc khác: yêu cầu Chờ giao việc.\n"
     "- Mới nhất lên đầu, có phân trang."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Chứng từ Đang tạo, Chờ duyệt, Chờ TP duyệt, Không duyệt, Đóng.\n"
     "- Chứng từ đã giao hết việc (phiếu giao việc đã Hủy thì phần đó được trả lại).\n"
     "- Hợp đồng / PL / Lắp đặt của phòng tiếp nhận mà người xem không phụ trách (trừ quyền xem theo tổng "
     "công ty).\n"
     "- Hợp đồng đã bị Từ chối tiếp nhận xử lý (không còn phòng tiếp nhận)."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Mỗi tab có Từ ngày / Đến ngày:\n"
     "- Hợp đồng, PL bổ sung, Phiếu bảo hành: theo Ngày lập chứng từ (Đến ngày tính trọn ngày).\n"
     "- Lắp đặt bàn giao, Giao việc khác: theo code hiện tại lọc theo ngày dự kiến của yêu cầu, không theo "
     "Ngày lập đang hiện trên bảng."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "- Hợp đồng / PL bổ sung: STT, Mã phiếu (chữ thường, không bấm được), Tổng thanh toán, Khách hàng, Người "
     "liên hệ - SĐT, Người lập, Ngày lập, Người duyệt, Ngày duyệt, Trạng thái, Hành động. Lọc: Số hợp đồng, "
     "Người duyệt hợp đồng, Trạng thái, Người lập, Khách hàng.\n"
     "- Phiếu bảo hành: STT, Mã phiếu (bấm mở), Khách hàng, Người liên hệ - SĐT, Người lập, Ngày lập, Trạng "
     "thái, Hành động. Lọc: Số phiếu bảo hành, Trạng thái, Khách hàng, Hàng hóa.\n"
     "- Lắp đặt bàn giao / Giao việc khác: STT, Số phiếu, Số hợp đồng, Khách hàng, Người lập, Ngày lập, Trạng "
     "thái, Hành động. Lọc: Số phiếu yêu cầu, Khách hàng, Số hợp đồng, Người lập (Giao việc khác thêm Trạng "
     "thái).\n"
     "- Người phụ trách phòng có thêm ô Phòng ban, Bộ phận."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "Số còn giao của một dòng = số trên chứng từ - số đã giảm bởi PL giảm - số đã giao xong - số đang nằm "
     "trong phiếu giao việc Chờ thực hiện / Đang nhập kết quả / Đã nhập kết quả / Đang duyệt kết quả.\n"
     "Chứng từ còn ít nhất 1 dòng có số còn giao lớn hơn 0 thì hiện. Với dữ liệu mẫu: HD-01 còn 2 công M1 + "
     "1 Vệ sinh máy; giao 2 công thì vẫn hiện (còn dịch vụ); giao thêm dịch vụ thì rời danh sách."),

    ("7. Phân quyền cấp",
     "- Màn không đòi quyền riêng: ai đăng nhập cũng mở được.\n"
     "- Tab Hợp đồng, PL bổ sung, Lắp đặt bàn giao: thấy chứng từ có phòng tiếp nhận là phòng mình được phân "
     "phụ trách; quyền \"Xem danh sách phiếu chờ giao việc theo tổng công ty\" thấy mọi công ty.\n"
     "- Tab Phiếu bảo hành, Giao việc khác: theo code hiện tại không giới hạn, ai cũng thấy mọi phiếu.\n"
     "- Nút \"Tạo phiếu giao việc\" / \"Từ chối tiếp nhận xử lý\": cần quyền \"Tạo phiếu giao việc\" và phòng "
     "của chính người xem là phòng tiếp nhận (Lắp đặt / Giao việc khác không cần quyền này).\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- Tab không có số đếm.\n"
     "- Trang chủ, nhóm Bảo hành sửa chữa: ô \"Phiếu chờ giao việc\" (chỉ người có quyền \"Tạo phiếu giao "
     "việc\") = số Hợp đồng + PL bổ sung + Phiếu bảo hành + Lắp đặt + Giao việc khác có phòng tiếp nhận là "
     "phòng của người xem. Với dữ liệu mẫu TP-1 thấy 5."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- Tab Phiếu bảo hành và Giao việc khác hiện phiếu của mọi công ty, mọi phòng.\n"
     "- Danh sách xét \"phòng được phân phụ trách\", còn nút giao việc và ô đếm trang chủ xét \"phòng của "
     "chính mình\": hai cách có thể lệch nhau.\n"
     "- Kiểm tra \"đang có PL giảm chờ duyệt\" chỉ chạy khi bấm nút ở tab Hợp đồng.\n"
     "- Lưu phiếu giao việc không kiểm tra lại số còn giao của hợp đồng: hai người cùng giao có thể vượt số.\n"
     "- Tab Phiếu bảo hành luôn hiện nút Tạo phiếu giao việc, kể cả người không có quyền."),
]


ROLE_TCS = [
    ("00", "Người không có quyền gì vẫn mở được màn", "P0",
     "NV-A thuộc PKD, không có quyền giao việc, không phụ trách phòng nào\n" + DATA,
     "1. Đăng nhập NV-A\n"
     "2. " + MENU,
     "Tài khoản: NV-A",
     "- Mở được trang \"Danh sách phiếu chờ giao việc\" với 5 tab\n"
     "- Tab Hợp đồng ghi không có dữ liệu"),

    ("01", "Tab Phiếu bảo hành chỉ nên hiện phiếu của phòng / công ty mình", "P1",
     "NV-A như TC 00; thêm BH-02 Đã duyệt của công ty TPC, phòng tiếp nhận PKT9",
     "1. Đăng nhập NV-A, mở màn\n"
     "2. Bấm tab Phiếu bảo hành",
     "—",
     "- Mong đợi: không thấy BH-01, BH-02\n"
     "- Lưu ý: theo code hiện tại thấy cả BH-01 và BH-02 (mọi công ty) - ghi Failed"),

    ("02", "Tab Giao việc khác chỉ nên hiện yêu cầu của phòng / công ty mình", "P1",
     "NV-A như TC 00; thêm YC-02 Chờ giao việc của TPC, phòng tiếp nhận PKT9",
     "1. Đăng nhập NV-A, mở màn\n"
     "2. Bấm tab Giao việc khác",
     "—",
     "- Mong đợi: không thấy YC-01, YC-02\n"
     "- Lưu ý: theo code hiện tại thấy cả hai - ghi Failed"),

    ("03", "Trưởng phòng chỉ thấy hợp đồng của phòng mình phụ trách", "P0",
     DATA,
     "1. " + OPEN_TP1,
     "Tài khoản: TP-1",
     "- Tab Hợp đồng có HD-01\n"
     "- Không có HD-02 (phòng tiếp nhận PKT2)"),

    ("04", "Quyền xem theo tổng công ty thấy mọi hợp đồng chờ giao việc", "P0",
     "QL-TCT thuộc PKT2, có quyền \"Xem danh sách phiếu chờ giao việc theo tổng công ty\"; thêm HD-09 Có hiệu "
     "lực của công ty TPC\n" + DATA,
     "1. Đăng nhập QL-TCT, mở màn",
     "—",
     "- Tab Hợp đồng có HD-01, HD-02, HD-09\n"
     "- Tab Lắp đặt bàn giao có LD-01"),

    ("05", "Thấy theo tổng công ty nhưng không giao được việc phòng khác", "P0",
     "QL-TCT như TC 04, có thêm quyền \"Tạo phiếu giao việc\"",
     "1. Đăng nhập QL-TCT, mở màn\n"
     "2. Bấm nút bánh răng ở dòng HD-01",
     "—",
     "- Không có \"Tạo phiếu giao việc\", không có \"Từ chối tiếp nhận xử lý\"\n"
     "- Dòng HD-02 (phòng PKT2 của QL-TCT) có \"Tạo phiếu giao việc\""),

    ("06", "Không có quyền Tạo phiếu giao việc thì không có nút", "P0",
     "TP-1 bị bỏ quyền \"Tạo phiếu giao việc\"\n" + DATA,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm nút bánh răng ở dòng HD-01",
     "—",
     "- Vẫn thấy HD-01\n"
     "- Không có \"Tạo phiếu giao việc\", không có \"Từ chối tiếp nhận xử lý\""),

    ("07", "Kỹ thuật viên cùng phòng nhưng không phụ trách phòng", "P1",
     "KTV-1 thuộc PKT1, có quyền \"Tạo phiếu giao việc\", không được phân phụ trách phòng nào\n" + DATA,
     "1. Đăng nhập KTV-1, mở màn",
     "—",
     "- Tab Hợp đồng, PL bổ sung, Lắp đặt bàn giao không có dữ liệu\n"
     "- Lưu ý: ô đếm trang chủ của KTV-1 vẫn ra 5 (xem XI.006); nếu nghiệp vụ muốn KTV-1 giao được việc thì "
     "ghi Failed"),

    ("08", "Phụ trách phòng nhưng thuộc phòng khác", "P1",
     "TP-3 thuộc PKD, được phân phụ trách cả PKT1, có quyền \"Tạo phiếu giao việc\"\n" + DATA,
     "1. Đăng nhập TP-3, mở màn\n"
     "2. Bấm nút bánh răng ở dòng HD-01",
     "—",
     "- Thấy HD-01\n"
     "- Mong đợi: có \"Tạo phiếu giao việc\"\n"
     "- Lưu ý: theo code hiện tại không có nút vì phòng của TP-3 là PKD - ghi Failed nếu nghiệp vụ cho người "
     "phụ trách phòng giao việc"),

    ("09", "Gọi thẳng chức năng lưu phiếu giao việc cho hợp đồng phòng khác", "P1",
     DATA,
     "1. Đăng nhập TP-1\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng lưu phiếu giao việc cho HD-02 (phòng PKT2) với đủ "
     "thông tin bắt buộc",
     "—",
     "- Mong đợi: bị chặn, không tạo phiếu\n"
     "- Lưu ý: theo code hiện tại lưu thành công, HD-02 bị trừ số còn giao - ghi Failed"),

    ("10", "Super Admin ở tab Lắp đặt bàn giao", "P2",
     "SA có vai trò Super Admin và quyền \"Xem danh sách phiếu chờ giao việc theo tổng công ty\", thuộc phòng "
     "PKD\n" + DATA,
     "1. Đăng nhập SA, mở màn, bấm tab Lắp đặt bàn giao\n"
     "2. Bấm nút bánh răng ở dòng LD-01",
     "—",
     "- Mong đợi: có \"Tạo phiếu giao việc\" như ở tab Hợp đồng\n"
     "- Lưu ý: tab này kiểm tra tên vai trò viết khác (\"Super admin\"), nếu không có nút thì ghi Failed"),
]
