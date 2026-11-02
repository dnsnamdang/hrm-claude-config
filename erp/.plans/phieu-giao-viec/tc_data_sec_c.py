# -*- coding: utf-8 -*-
"""Section IX - XII cho man Phieu giao viec."""
from tc_data_role import MENU, MENU_DG, DATA, OPEN_TP1, FROM_HD01

P01 = "PGV-01 từ HD-01, Chờ thực hiện, chưa có phiếu công tác, do TP-1 lập"

SEC_IX = [
    ("001", "Người lập thấy nút Xóa ở phiếu Chờ thực hiện chưa có phiếu công tác", "P0",
     P01,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm nút bánh răng ở PGV-01",
     "—",
     "- Có \"Xóa\"\n"
     "- Không có \"Nhập kết quả\", \"Xem phiếu nhập kết quả\""),

    ("002", "Xác nhận trước khi xóa", "P0",
     P01,
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm \"Xóa\" ở PGV-01",
     "—",
     "- Hộp \"Xác nhận xóa!\" với câu \"Bạn chắc chắn muốn xóa bản ghi này?\""),

    ("003", "Hủy hộp xác nhận thì không xóa", "P1",
     P01,
     "1. Làm như TC 002, bấm Hủy",
     "—",
     "- PGV-01 vẫn ở danh sách, Chờ thực hiện"),

    ("004", "Xóa phiếu từ hợp đồng", "P0",
     P01,
     "1. Làm như TC 002, bấm đồng ý\n"
     "2. Mở Phiếu chờ giao việc, tab Hợp đồng",
     "—",
     "- PGV-01 biến mất khỏi danh sách Phiếu giao việc\n"
     "- HD-01 quay lại danh sách chờ, mở form thấy M1 SL còn 1, \"Vệ sinh máy\" SL còn 1"),

    ("005", "Xóa phiếu lắp đặt trả số và trạng thái cho yêu cầu", "P0",
     "PGV-02 từ LD-01 giao đủ 3 máy, Chờ thực hiện, chưa có phiếu công tác, do TP-1 lập; LD-01 đang \"Đang "
     "giao việc\"",
     "1. " + OPEN_TP1 + "\n"
     "2. Xóa PGV-02\n"
     "3. Mở LD-01 và Phiếu chờ giao việc, tab Lắp đặt bàn giao",
     "—",
     "- LD-01 về \"Chờ giao việc\", có lại trong tab Lắp đặt bàn giao, còn 3 máy"),

    ("006", "Xóa phiếu giao việc khác trả yêu cầu về chờ giao", "P0",
     "PGV-03 từ YC-01, Chờ thực hiện, chưa có phiếu công tác, do TP-1 lập; YC-01 đang Đã giao việc",
     "1. " + OPEN_TP1 + "\n"
     "2. Xóa PGV-03",
     "—",
     "- YC-01 về \"Chờ giao việc\", có lại trong tab Giao việc khác"),

    ("007", "Phiếu đã có phiếu công tác thì không xóa được", "P0",
     "PGV-01 đã được lập phiếu công tác bên HRM (chưa duyệt)",
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm nút bánh răng ở PGV-01",
     "—",
     "- Không có \"Xóa\""),

    ("008", "Phiếu đã nhập kết quả thì không xóa được", "P0",
     "PGV-01 Đang nhập kết quả",
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm nút bánh răng ở PGV-01",
     "—",
     "- Không có \"Xóa\", có \"Xem phiếu nhập kết quả\""),

    ("009", "Super Admin xóa phiếu người khác", "P1",
     P01 + "; SA có vai trò Super Admin",
     "1. Đăng nhập SA, " + MENU + "\n"
     "2. Bấm \"Xóa\" ở PGV-01, đồng ý",
     "—",
     "- PGV-01 bị xóa, HD-01 quay lại chờ giao việc"),

    ("010", "Dán đường dẫn Xóa của phiếu đã có phiếu công tác", "P1",
     "PGV-01 như TC 007; TP-1 có đường dẫn Xóa của PGV-01",
     "1. Đăng nhập TP-1, dán đường dẫn Xóa",
     "—",
     "- Ra trang không tìm thấy, PGV-01 không đổi"),
]

SEC_X = [
    ("001", "Phiếu công tác chưa duyệt thì chưa nhập kết quả", "P0",
     "PGV-01 có phiếu công tác bên HRM gắn KTV-1, phiếu công tác chưa duyệt",
     "1. Đăng nhập KTV-1\n"
     "2. " + MENU_DG + "\n"
     "3. Bấm nút bánh răng ở PGV-01",
     "—",
     "- Có PGV-01, Người thực hiện KTV-1\n"
     "- Không có \"Nhập kết quả\""),

    ("002", "Phiếu công tác đã duyệt thì người thực hiện nhập kết quả", "P0",
     "Phiếu công tác của PGV-01 đã duyệt",
     "1. Đăng nhập KTV-1, " + MENU_DG + "\n"
     "2. Bấm nút bánh răng ở PGV-01, chọn \"Nhập kết quả\"",
     "—",
     "- Mở form nhập kết quả của PGV-01"),

    ("003", "Người không thực hiện và không có quyền thì không có Nhập kết quả", "P1",
     "Như TC 002; QL-C có quyền xem theo công ty, không có quyền \"Nhập kết quả thực hiện\"",
     "1. Đăng nhập QL-C, " + MENU + "\n"
     "2. Bấm nút bánh răng ở PGV-01",
     "—",
     "- Không có \"Nhập kết quả\""),

    ("004", "Lưu nháp kết quả chuyển Đang nhập kết quả", "P0",
     "Như TC 002",
     "1. KTV-1 nhập kết quả PGV-01, bấm lưu nháp\n"
     "2. Mở danh sách Phiếu giao việc",
     "—",
     "- PGV-01 \"Đang nhập kết quả\"\n"
     "- Có \"Xem phiếu nhập kết quả\", không còn \"Nhập kết quả\""),

    ("005", "Gửi kết quả chuyển Đã nhập kết quả", "P0",
     "Như TC 004",
     "1. KTV-1 mở phiếu nhập kết quả, gửi duyệt\n"
     "2. Mở danh sách Phiếu giao việc",
     "—",
     "- PGV-01 \"Đã nhập kết quả\"\n"
     "- Người có quyền \"Duyệt phiếu nhập kết quả\" nhận thông báo \"Bạn có 1 phiếu kết quả giao việc cần "
     "duyệt\""),

    ("006", "Duyệt kết quả chuyển Đã duyệt kết quả", "P0",
     "Như TC 005",
     "1. Người duyệt lập phiếu duyệt kết quả và duyệt\n"
     "2. Mở danh sách Phiếu giao việc",
     "—",
     "- PGV-01 \"Đã duyệt kết quả\"\n"
     "- Có \"Xem phiếu duyệt kết quả\""),

    ("007", "Phiếu duyệt kết quả đang tạo thì chưa có nút xem", "P1",
     "Như TC 005; người duyệt mới lưu nháp phiếu duyệt kết quả",
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm nút bánh răng ở PGV-01",
     "—",
     "- PGV-01 \"Đang duyệt kết quả\"\n"
     "- Chưa có \"Xem phiếu duyệt kết quả\""),

    ("008", "Xóa phiếu nhập kết quả trả phiếu giao việc về Chờ thực hiện", "P1",
     "PGV-01 Đang nhập kết quả",
     "1. KTV-1 xóa phiếu nhập kết quả của PGV-01\n"
     "2. Mở danh sách Phiếu giao việc",
     "—",
     "- PGV-01 \"Chờ thực hiện\", có lại \"Nhập kết quả\""),

    ("009", "Phiếu duyệt kết quả không nằm trong danh sách Phiếu giao việc", "P1",
     "Như TC 006",
     "1. " + OPEN_TP1,
     "—",
     "- Chỉ có 1 dòng PGV-01, không có dòng phiếu duyệt kết quả"),

    ("010", "Lọc trạng thái Đã duyệt kết quả", "P2",
     "Như TC 006",
     "1. " + OPEN_TP1 + "\n"
     "2. Ô Trạng thái chọn \"Đã duyệt kết quả\"",
     "—",
     "- Có PGV-01"),
]

SEC_XI = [
    ("001", "In danh sách", "P0",
     "TP-1 thấy PGV-01, PGV-02, PGV-03",
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm \"In\"",
     "—",
     "- Mở tab mới bản in ngang \"DANH SÁCH PHIẾU GIAO VIỆC\" có tiêu đề công ty\n"
     "- Đủ 3 phiếu, mới nhất lên đầu, có số hợp đồng, số yêu cầu, khách hàng, người yêu cầu, người lập"),

    ("002", "Xuất excel danh sách", "P0",
     "Như TC 001",
     "1. " + OPEN_TP1 + "\n"
     "2. Bấm \"Xuất excel\"",
     "—",
     "- Tải file danh_sach_phieu_giao_viec.xlsx, tiêu đề \"DANH SÁCH PHIẾU GIAO VIỆC\", đủ 3 phiếu"),

    ("003", "In theo bộ lọc đang chọn", "P1",
     "Như TC 001",
     "1. " + OPEN_TP1 + "\n"
     "2. Ô Trạng thái chọn \"Chờ thực hiện\" (bảng còn PGV-01), bấm \"In\"",
     "—",
     "- Mong đợi: bản in chỉ có PGV-01\n"
     "- Lưu ý: theo code hiện tại bản in có cả 3 phiếu (bỏ qua bộ lọc) - ghi Failed"),

    ("004", "Xuất excel theo bộ lọc đang chọn", "P1",
     "Như TC 001",
     "1. " + OPEN_TP1 + "\n"
     "2. Ô Số phiếu giao việc gõ \"02\", bấm \"Xuất excel\"",
     "—",
     "- Mong đợi: file chỉ có PGV-02\n"
     "- Lưu ý: theo code hiện tại file có cả 3 phiếu - ghi Failed"),

    ("005", "In ở menu Phiếu giao việc được giao", "P1",
     "KTV-1 có quyền \"Xem phiếu giao việc theo công ty\"; chỉ PGV-01 giao cho KTV-1, công ty có 3 phiếu",
     "1. Đăng nhập KTV-1, " + MENU_DG + " (bảng có PGV-01)\n"
     "2. Bấm \"In\"",
     "—",
     "- Mong đợi: bản in chỉ có PGV-01\n"
     "- Lưu ý: theo code hiện tại in cả 3 phiếu của công ty - ghi Failed"),

    ("006", "Không có quyền xem thì bản in chỉ có phiếu của mình", "P1",
     "NV-A không có quyền xem, đã lập PGV-07",
     "1. Đăng nhập NV-A, dán đường dẫn In danh sách",
     "—",
     "- Bản in chỉ có PGV-07"),
]

SEC_XII = [
    ("001", "Đường dẫn Sửa không mở được với phiếu Chờ thực hiện", "P1",
     P01 + "; TP-1 có đường dẫn sửa PGV-01",
     "1. Đăng nhập TP-1, dán đường dẫn sửa PGV-01",
     "—",
     "- Ra trang không tìm thấy (màn không có chức năng Sửa)"),

    ("002", "Đường dẫn Sửa với phiếu Đã duyệt kết quả", "P1",
     "PGV-03 Đã duyệt kết quả, do TP-1 lập",
     "1. Đăng nhập TP-1, dán đường dẫn sửa PGV-03",
     "—",
     "- Mong đợi: ra trang không tìm thấy\n"
     "- Lưu ý: theo code hiện tại mở được form \"Chỉnh sửa phiếu giao việc\" và lưu được, làm đổi dữ liệu "
     "phiếu đã duyệt kết quả - ghi Failed"),

    ("003", "Hai người cùng tạo phiếu giao việc cho một hợp đồng", "P1",
     "TP-1 và TP-1B (cùng PKT1, cùng quyền) cùng mở form tạo phiếu giao việc từ HD-01 trên hai máy\n" + DATA,
     "1. TP-1 bấm \"Lưu & duyệt\"\n"
     "2. TP-1B bấm \"Lưu & duyệt\"",
     "—",
     "- Mong đợi: phiếu thứ hai bị chặn vì HD-01 đã giao hết\n"
     "- Lưu ý: theo code hiện tại tạo được 2 phiếu, M1 bị giao 2 lần (đã ghi ở bộ Phiếu chờ giao việc) - ghi "
     "Failed"),

    ("004", "Xóa phiếu trong lúc HRM đang lập phiếu công tác", "P2",
     P01 + "; TP-1 đang mở danh sách",
     "1. Bên HRM lập phiếu công tác cho PGV-01\n"
     "2. TP-1 (chưa tải lại trang) bấm \"Xóa\" ở PGV-01, đồng ý",
     "—",
     "- Ra trang không tìm thấy, PGV-01 không bị xóa"),

    ("005", "Luồng đầu - cuối hợp đồng sửa chữa", "P0",
     DATA,
     "1. TP-1 tạo phiếu giao việc từ HD-01, giao đủ\n"
     "2. HRM lập và duyệt phiếu công tác gắn KTV-1\n"
     "3. KTV-1 nhập kết quả, gửi\n"
     "4. Người duyệt duyệt kết quả",
     "—",
     "- Sau 1: phiếu Chờ thực hiện, HD-01 rời danh sách chờ\n"
     "- Sau 2: Người thực hiện KTV-1, không còn nút Xóa\n"
     "- Sau 3: Đã nhập kết quả\n"
     "- Sau 4: Đã duyệt kết quả, có \"Xem phiếu duyệt kết quả\""),

    ("006", "Luồng đầu - cuối lắp đặt giao làm hai lần", "P0",
     DATA,
     "1. TP-1 tạo PGV-A từ LD-01 giao 2 máy\n"
     "2. TP-1 tạo PGV-B từ LD-01 giao 1 máy\n"
     "3. TP-1 xóa PGV-B",
     "—",
     "- Sau 1: LD-01 Chờ giao việc, còn 1 máy\n"
     "- Sau 2: LD-01 Đang giao việc, rời danh sách chờ\n"
     "- Sau 3: LD-01 về Chờ giao việc, còn 1 máy; PGV-A không đổi"),

    ("007", "Luồng đầu - cuối giao việc khác: tạo, xóa, tạo lại", "P1",
     DATA,
     "1. TP-1 tạo phiếu từ YC-01\n"
     "2. Xóa phiếu đó\n"
     "3. Tạo lại phiếu từ YC-01",
     "—",
     "- Sau 1: YC-01 Đã giao việc\n"
     "- Sau 2: YC-01 Chờ giao việc\n"
     "- Sau 3: tạo thành công, YC-01 Đã giao việc, danh sách chỉ có phiếu mới (phiếu đã xóa không hiện)"),
]
