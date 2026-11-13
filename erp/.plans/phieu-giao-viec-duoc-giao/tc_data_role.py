# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Phieu giao viec duoc giao'."""

MENU_DG = "Mở menu Bảo hành sửa chữa > mục \"Giao việc\" > bấm \"Phiếu giao việc được giao\""
MENU = "Mở menu Bảo hành sửa chữa > mục \"Giao việc\" > bấm \"Phiếu giao việc\""

# Du lieu mau dung chung
DATA = ("Công ty TPE có phòng kỹ thuật PKT1; công ty TPC có phòng PKT9.\n"
        "Tài khoản:\n"
        "- TP-1: trưởng PKT1, người lập các phiếu giao việc của PKT1\n"
        "- KTV-1 (trưởng nhóm), KTV-2 (thành viên): kỹ thuật viên PKT1, không có quyền xem phiếu giao việc, "
        "không có quyền \"Nhập kết quả thực hiện\"\n"
        "- KTV-3: kỹ thuật viên PKT1 không thuộc nhóm nào\n"
        "Phiếu giao việc:\n"
        "- PGV-01 (TPE, từ hợp đồng HD-01, khách KH-1, dự kiến 10/11 - 12/11/2026, Tổng công 2): phiếu công tác "
        "PCT-01 bên HRM gồm KTV-1 (trưởng nhóm), KTV-2, đã duyệt; trạng thái Chờ thực hiện\n"
        "- PGV-02 (TPE, từ yêu cầu lắp đặt LD-01 của hợp đồng hàng HDH-01): PCT-02 gồm KTV-2, đã duyệt; "
        "trạng thái Đã duyệt kết quả\n"
        "- PGV-03 (TPE): chưa có phiếu công tác\n"
        "- PGV-09 (TPC): PCT-09 gồm KTV-1, đã duyệt; trạng thái Chờ thực hiện")

OPEN_KTV1 = "Đăng nhập KTV-1, " + MENU_DG
OPEN_KTV2 = "Đăng nhập KTV-2, " + MENU_DG

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Phiếu giao việc được giao: danh sách phiếu giao việc mà người đăng nhập là NGƯỜI THỰC HIỆN (trưởng "
     "nhóm hoặc thành viên). Kỹ thuật viên dùng màn này để biết việc của mình và bấm \"Nhập kết quả\".\n"
     "Người dùng làm được: xem danh sách, lọc, mở chi tiết phiếu, mở phiếu nhập kết quả / phiếu duyệt kết "
     "quả, bấm \"Nhập kết quả\" khi đủ điều kiện, In, Xuất excel.\n"
     "Người thực hiện không chọn trên ERP: được ghi sang từ phiếu công tác (PCT) bên HRM khi PCT được duyệt."),

    ("2. Đối tượng được tính / hiển thị",
     "- Mọi phiếu giao việc (không gồm phiếu duyệt kết quả) mà người đăng nhập có tên trong danh sách người "
     "thực hiện, ở mọi trạng thái trừ Hủy, mọi công ty.\n"
     "- Không phụ thuộc quyền xem phiếu giao việc: có quyền xem theo công ty vẫn chỉ thấy phiếu của mình.\n"
     "- Mới nhất lên đầu, phân trang, STT liên tục."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu đã Xóa (Hủy).\n"
     "- Phiếu mình lập nhưng không thực hiện.\n"
     "- Phiếu có PCT chưa duyệt (người thực hiện chỉ được ghi sang khi PCT duyệt).\n"
     "- Phiếu mà PCT bị xóa, hoặc PCT sửa bỏ tên mình.\n"
     "- Màn không có nút Tạo mới, không có ô lọc Công ty / Phòng ban, người thực hiện không có nút Xóa."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "- \"Thời gian dự kiến từ ngày\": Ngày dự kiến bắt đầu của phiếu từ ngày này trở đi.\n"
     "- \"Thời gian dự kiến đến ngày\": Ngày dự kiến kết thúc của phiếu đến hết ngày này."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Bảng: STT, Số phiếu giao việc (bấm mở chi tiết), Số hợp đồng (bấm mở chứng từ gốc), Số phiếu yêu cầu, "
     "Khách hàng, Người yêu cầu, Người lập, Người thực hiện (trưởng nhóm kèm SĐT), Thời gian dự kiến, Tổng công "
     "định mức, Trạng thái, Hành động (Nhập kết quả, Xem phiếu nhập kết quả, Xem phiếu duyệt kết quả).\n"
     "Bộ lọc: Số phiếu giao việc, Số hợp đồng, Số phiếu yêu cầu, Khách hàng, Người yêu cầu, Trạng thái, Người "
     "lập, Người thực hiện, Thời gian dự kiến từ / đến ngày."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Một phiếu chỉ hiện 1 dòng dù nhóm có nhiều người.\n"
     "- Cột Người thực hiện hiện trưởng nhóm; nhóm không có trưởng nhóm thì hiện người đầu tiên.\n"
     "- Nút \"Nhập kết quả\" hiện khi: phiếu Chờ thực hiện, PCT đã duyệt, phiếu có người thực hiện, chưa có "
     "phiếu nhập kết quả, và người đăng nhập là người thực hiện (trưởng nhóm hay thành viên đều được) hoặc có "
     "quyền \"Nhập kết quả thực hiện\".\n"
     "- Mỗi phiếu giao việc chỉ có 1 phiếu nhập kết quả: một người trong nhóm nhập rồi thì người khác mất nút."),

    ("7. Phân quyền cấp",
     "- Mở menu: mọi tài khoản đăng nhập; chỉ thấy phiếu mình thực hiện.\n"
     "- Xem chi tiết: người thực hiện xem được phiếu của mình; người ngoài nhóm không có quyền xem thì ra trang "
     "không tìm thấy.\n"
     "- In / Xuất excel: lấy theo phạm vi của menu \"Phiếu giao việc\" (theo quyền xem), không theo menu này.\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- Cột Tổng công định mức hiện 2 số lẻ.\n"
     "- Không có ô đếm \"phiếu chờ nhập kết quả\" trên trang chủ cho người thực hiện.\n"
     "- In / Xuất excel: tiêu đề \"DANH SÁCH PHIẾU GIAO VIỆC\", file danh_sach_phieu_giao_viec.xlsx."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- Đường dẫn lấy dữ liệu phiếu giao việc dành cho ứng dụng HRM không cần đăng nhập: ai có số thứ tự phiếu "
     "cũng đọc được khách hàng, người liên hệ, nội dung việc.\n"
     "- In / Xuất excel ở menu này ra cả phiếu không giao cho mình và bỏ qua bộ lọc (đã ghi ở bộ Phiếu giao "
     "việc).\n"
     "- Nút Quay lại ở chi tiết đưa về danh sách \"Phiếu giao việc\", không về \"Phiếu giao việc được giao\".\n"
     "- Tiêu đề trang giống hệt menu \"Phiếu giao việc\" (\"Danh sách phiếu giao việc\").\n"
     "- Lọc Người yêu cầu không ra phiếu lắp đặt / giao việc khác (đã ghi ở bộ Phiếu giao việc).\n"
     "- Dán thẳng đường dẫn form nhập kết quả của phiếu không giao cho mình vẫn mở được form (đã ghi ở bộ Phiếu "
     "nhập kết quả)."),
]


ROLE_TCS = [
    ("00", "Tài khoản không thực hiện phiếu nào thấy danh sách trống", "P0",
     "KTV-3 như dữ liệu mẫu, không có quyền nào về phiếu giao việc\n" + DATA,
     "1. Đăng nhập KTV-3\n"
     "2. " + MENU_DG,
     "Tài khoản: KTV-3",
     "- Mở trang danh sách phiếu giao việc\n"
     "- Bảng không có dữ liệu"),

    ("01", "Người thực hiện không có quyền xem vẫn thấy phiếu của mình", "P0",
     DATA,
     "1. " + OPEN_KTV1,
     "Tài khoản: KTV-1",
     "- Có PGV-01 và PGV-09\n"
     "- Không có PGV-02, PGV-03"),

    ("02", "Quyền xem theo công ty không làm rộng danh sách được giao", "P0",
     "KTV-1 có thêm quyền \"Xem phiếu giao việc theo công ty\"\n" + DATA,
     "1. " + OPEN_KTV1,
     "—",
     "- Chỉ có PGV-01 và PGV-09\n"
     "- Không có PGV-02, PGV-03 dù cùng công ty TPE"),

    ("03", "Quyền theo tổng công ty cũng chỉ thấy phiếu mình thực hiện", "P1",
     "QL-T có quyền \"Xem phiếu giao việc theo tổng công ty\", không thực hiện phiếu nào\n" + DATA,
     "1. Đăng nhập QL-T, " + MENU_DG,
     "—",
     "- Bảng không có dữ liệu\n"
     "- Không có ô lọc Công ty, Phòng ban"),

    ("04", "Người lập không thực hiện thì không thấy phiếu mình lập", "P0",
     DATA,
     "1. Đăng nhập TP-1, " + MENU_DG,
     "—",
     "- Không có PGV-01, PGV-02, PGV-03\n"
     "- Ở menu \"Phiếu giao việc\" TP-1 vẫn thấy các phiếu này"),

    ("05", "Người ngoài nhóm mở chi tiết qua đường dẫn", "P0",
     "KTV-3 không có quyền xem; có đường dẫn chi tiết PGV-01\n" + DATA,
     "1. Đăng nhập KTV-3, dán đường dẫn chi tiết PGV-01",
     "—",
     "- Ra trang không tìm thấy"),

    ("06", "Người thực hiện không có quyền nhập kết quả vẫn có nút Nhập kết quả", "P0",
     DATA,
     "1. " + OPEN_KTV2 + "\n"
     "2. Bấm nút bánh răng ở PGV-01",
     "—",
     "- Có \"Nhập kết quả\""),

    ("07", "Người thực hiện không có nút Xóa", "P0",
     DATA,
     "1. " + OPEN_KTV1 + "\n"
     "2. Bấm nút bánh răng ở PGV-01",
     "—",
     "- Không có \"Xóa\""),

    ("08", "Người thực hiện dán đường dẫn Xóa phiếu", "P1",
     "PGV-03 do TP-1 lập, Chờ thực hiện, chưa có PCT; KTV-1 có đường dẫn Xóa của PGV-03\n" + DATA,
     "1. Đăng nhập KTV-1, dán đường dẫn Xóa của PGV-03",
     "—",
     "- Ra trang không tìm thấy\n"
     "- PGV-03 vẫn Chờ thực hiện"),
]
