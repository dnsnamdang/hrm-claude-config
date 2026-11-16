# -*- coding: utf-8 -*-
"""Muc VII - X: xem chi tiet, In / Excel, bao mat va dong thoi, luong dau - cuoi."""

from tc_data_role import MENU, MENU_DG, DATA, OPEN_KTV1, OPEN_KTV2

SEC_VII = [
    ("001", "Người thực hiện mở chi tiết phiếu", "P0",
     DATA,
     "1. " + OPEN_KTV1 + "\n"
     "2. Bấm số PGV-01",
     "—",
     "- Tiêu đề \"Phiếu giao việc PGV-01\"\n"
     "- Thông tin khách hàng, hợp đồng HD-01, người yêu cầu, các dòng việc và Tổng công định mức 2.00 khớp "
     "danh sách\n"
     "- Không sửa được ô nào, không có nút \"Lưu & duyệt\""),

    ("002", "Thành viên nhóm mở chi tiết", "P0",
     DATA,
     "1. " + OPEN_KTV2 + "\n"
     "2. Bấm số PGV-01",
     "—",
     "- Mở được chi tiết PGV-01"),

    ("003", "Chi tiết phiếu công ty khác mình thực hiện", "P1",
     DATA,
     "1. " + OPEN_KTV1 + "\n"
     "2. Bấm số PGV-09",
     "—",
     "- Mở được chi tiết PGV-09 (công ty TPC)"),

    ("004", "Bị bỏ khỏi PCT thì mất quyền xem chi tiết", "P1",
     "KTV-2 bị bỏ khỏi PCT-01 như TC II.008; KTV-2 còn giữ đường dẫn chi tiết PGV-01, không có quyền xem",
     "1. Đăng nhập KTV-2, dán đường dẫn chi tiết PGV-01",
     "—",
     "- Ra trang không tìm thấy"),

    ("005", "Chi tiết không có nút Nhập kết quả", "P2",
     DATA,
     "1. " + OPEN_KTV1 + "\n"
     "2. Bấm số PGV-01",
     "—",
     "- Trang chi tiết không có nút \"Nhập kết quả\"; muốn nhập phải quay lại danh sách"),

    ("006", "Nút Quay lại ở chi tiết", "P1",
     DATA,
     "1. " + OPEN_KTV1 + "\n"
     "2. Bấm số PGV-01, bấm \"Quay lại\"",
     "—",
     "- Mong đợi: quay về danh sách \"Phiếu giao việc được giao\"\n"
     "- Lưu ý: theo code hiện tại chuyển sang danh sách \"Phiếu giao việc\" - ghi Failed"),

    ("007", "Chi tiết không liệt kê thành viên nhóm", "P2",
     DATA,
     "1. " + OPEN_KTV2 + "\n"
     "2. Bấm số PGV-01",
     "—",
     "- Không có khối danh sách người thực hiện (khối này đang tắt)\n"
     "- Ghi nhận: người trong nhóm chỉ biết trưởng nhóm qua cột Người thực hiện ở danh sách, nghiệp vụ quyết, "
     "không ghi Failed"),

    ("008", "Bấm số hợp đồng khi không có quyền xem hợp đồng", "P2",
     "KTV-1 không có quyền xem hợp đồng SC - BH\n" + DATA,
     "1. " + OPEN_KTV1 + "\n"
     "2. Bấm HD-01 ở cột Số hợp đồng",
     "—",
     "- Ra trang không tìm thấy\n"
     "- Ghi nhận: nghiệp vụ quyết người thực hiện có cần xem hợp đồng gốc không, không ghi Failed"),
]

SEC_VIII = [
    ("001", "In danh sách khi chỉ là người thực hiện", "P0",
     "KTV-1 không có quyền xem phiếu giao việc\n" + DATA,
     "1. " + OPEN_KTV1 + "\n"
     "2. Bấm \"In\"",
     "—",
     "- Mở tab in \"DANH SÁCH PHIẾU GIAO VIỆC\"\n"
     "- Có PGV-01, PGV-09; không có PGV-02, PGV-03"),

    ("002", "In khi có quyền xem theo công ty", "P1",
     "KTV-1 có thêm quyền \"Xem phiếu giao việc theo công ty\"\n" + DATA,
     "1. " + OPEN_KTV1 + " (bảng có PGV-01, PGV-09)\n"
     "2. Bấm \"In\"",
     "—",
     "- Mong đợi: bản in chỉ có PGV-01, PGV-09\n"
     "- Lưu ý: theo code hiện tại bản in có mọi phiếu của TPE (PGV-01, PGV-02, PGV-03) và không có PGV-09 (đã "
     "ghi ở bộ Phiếu giao việc) - ghi Failed"),

    ("003", "In theo bộ lọc đang chọn", "P1",
     DATA,
     "1. " + OPEN_KTV1 + "\n"
     "2. Lọc Số phiếu giao việc \"01\", bấm Tìm kiếm (bảng chỉ còn PGV-01)\n"
     "3. Bấm \"In\"",
     "—",
     "- Mong đợi: bản in chỉ có PGV-01\n"
     "- Lưu ý: theo code hiện tại bản in có cả PGV-09 vì In bỏ qua bộ lọc (đã ghi ở bộ Phiếu giao việc) - ghi "
     "Failed"),

    ("004", "Xuất excel khi chỉ là người thực hiện", "P0",
     "KTV-1 không có quyền xem phiếu giao việc\n" + DATA,
     "1. " + OPEN_KTV1 + "\n"
     "2. Bấm \"Xuất excel\"",
     "—",
     "- Tải file danh_sach_phieu_giao_viec.xlsx, tiêu đề \"DANH SÁCH PHIẾU GIAO VIỆC\"\n"
     "- Có PGV-01, PGV-09; không có PGV-02, PGV-03"),

    ("005", "Xuất excel khi có quyền xem theo công ty", "P1",
     "Như TC 002",
     "1. " + OPEN_KTV1 + "\n"
     "2. Bấm \"Xuất excel\"",
     "—",
     "- Mong đợi: file chỉ có PGV-01, PGV-09\n"
     "- Lưu ý: theo code hiện tại file có mọi phiếu của TPE (đã ghi ở bộ Phiếu giao việc) - ghi Failed"),

    ("006", "Bản in và file không có phiếu đã Hủy", "P2",
     "PGV-06 có người thực hiện KTV-1, đã Hủy",
     "1. " + OPEN_KTV1 + "\n"
     "2. Bấm \"In\", rồi bấm \"Xuất excel\"",
     "—",
     "- Không có PGV-06 ở cả hai"),
]

SEC_IX = [
    ("001", "Đọc dữ liệu phiếu giao việc mà không đăng nhập", "P0",
     "Trình duyệt chưa đăng nhập ERP; biết số thứ tự nội bộ của PGV-01",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng lấy dữ liệu phiếu giao việc dành cho ứng dụng HRM, "
     "truyền số thứ tự của PGV-01, không kèm đăng nhập",
     "—",
     "- Mong đợi: bị chặn, yêu cầu đăng nhập\n"
     "- Lưu ý: theo code hiện tại trả về đủ dữ liệu PGV-01 (khách hàng, người liên hệ, thời gian, dòng việc, "
     "công định mức) - ghi Failed"),

    ("002", "Đổi số thứ tự để đọc phiếu của người khác", "P0",
     "Như TC 001",
     "1. Lặp lại TC 001 với số thứ tự của PGV-03 (không giao cho ai) và PGV-09 (công ty TPC)",
     "—",
     "- Mong đợi: bị chặn\n"
     "- Lưu ý: theo code hiện tại đọc được cả hai phiếu - ghi Failed"),

    ("003", "Danh sách cập nhật sau khi PCT được duyệt", "P1",
     "KTV-1 đang mở danh sách; PGV-04 có PCT-04 Chờ duyệt",
     "1. Trưởng phòng duyệt PCT-04 bên HRM\n"
     "2. KTV-1 không tải lại trang, bấm Tìm kiếm",
     "—",
     "- PGV-04 xuất hiện sau khi bấm Tìm kiếm (bảng lấy lại dữ liệu)"),

    ("004", "Nút Nhập kết quả cũ trên trang chưa tải lại", "P1",
     "KTV-1 và KTV-2 cùng đang mở danh sách, đều thấy \"Nhập kết quả\" ở PGV-01",
     "1. KTV-1 nhập và Lưu kết quả PGV-01\n"
     "2. KTV-2 (chưa tải lại) bấm \"Nhập kết quả\" ở PGV-01, nhập, bấm \"Lưu\"",
     "—",
     "- KTV-2 không lưu được, thông báo phiếu giao việc đã có phiếu nhập kết quả\n"
     "- Tải lại danh sách: PGV-01 \"Đang nhập kết quả\""),

    ("005", "PCT bị xóa khi người thực hiện đang mở form", "P1",
     "KTV-1 đang mở form nhập kết quả PGV-01",
     "1. Bên HRM xóa PCT-01\n"
     "2. KTV-1 bấm \"Lưu\"",
     "—",
     "- Không lưu được, thông báo \"Chỉ được nhập kết quả khi phiếu công tác (PCT) đã được duyệt\"\n"
     "- PGV-01 không còn trong danh sách của KTV-1"),
]

SEC_X = [
    ("001", "Từ PCT duyệt tới kết quả được duyệt", "P0",
     "TP-1 vừa lập PGV-11 (Chờ thực hiện) từ HD-01; PCT-11 gồm KTV-1 (trưởng nhóm), KTV-2 đang Chờ duyệt",
     "1. " + OPEN_KTV1 + ": không có PGV-11\n"
     "2. Trưởng phòng duyệt PCT-11 bên HRM\n"
     "3. KTV-1 tải lại: có PGV-11, bấm \"Nhập kết quả\", nhập đủ, bấm \"Lưu & Gửi duyệt\"\n"
     "4. Người duyệt duyệt kết quả\n"
     "5. KTV-1 và KTV-2 mở menu",
     "—",
     "- Sau bước 3: PGV-11 \"Đã nhập kết quả\", có \"Xem phiếu nhập kết quả\"\n"
     "- Sau bước 5: cả KTV-1 và KTV-2 thấy PGV-11 \"Đã duyệt kết quả\", có \"Xem phiếu duyệt kết quả\""),

    ("002", "Đối chiếu với menu Phiếu giao việc", "P0",
     "Như TC 001 sau bước 5; TP-1 là người lập",
     "1. Đăng nhập TP-1, " + MENU + ", tìm PGV-11\n"
     "2. So với dòng PGV-11 ở menu được giao của KTV-1",
     "—",
     "- Cùng Số phiếu, Khách hàng, Người thực hiện, Thời gian dự kiến, Tổng công định mức, Trạng thái"),

    ("003", "Nhập kết quả, xóa, nhập lại", "P1",
     "PGV-01 Chờ thực hiện, PCT-01 đã duyệt",
     "1. KTV-2 bấm \"Nhập kết quả\" ở PGV-01, bấm \"Lưu\"\n"
     "2. KTV-2 xóa phiếu nhập kết quả vừa lưu\n"
     "3. KTV-1 mở menu, bấm \"Nhập kết quả\" ở PGV-01, bấm \"Lưu\"",
     "—",
     "- Sau bước 2: PGV-01 về \"Chờ thực hiện\", có lại \"Nhập kết quả\"\n"
     "- Sau bước 3: PGV-01 \"Đang nhập kết quả\", phiếu nhập kết quả do KTV-1 lập"),

    ("004", "Đổi người trong nhóm giữa chừng", "P1",
     "PGV-01 Chờ thực hiện, PCT-01 đã duyệt gồm KTV-1, KTV-2",
     "1. Bên HRM sửa PCT-01: bỏ KTV-2, thêm KTV-3\n"
     "2. Lần lượt đăng nhập KTV-2, KTV-3, " + MENU_DG,
     "—",
     "- KTV-2 không còn PGV-01\n"
     "- KTV-3 có PGV-01 và có \"Nhập kết quả\""),
]
