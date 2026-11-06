# -*- coding: utf-8 -*-
"""Section IX - XII cho man Phieu nhap ket qua."""
from tc_data_role import MENU, MENU_PGV, MENU_DG, DATA, OPEN_KTV1, OPEN_QL1, FROM_PGV

SEC_IX = [
    ("001", "Sửa phiếu Đang tạo và lưu", "P0",
     DATA + "\nNKQ-02: KTV-1 lập cho PGV-02, Đang tạo, M1 hoàn thành 50%",
     "1. " + OPEN_KTV1 + "\n"
     "2. Bánh răng dòng NKQ-02 chọn Sửa\n"
     "3. Đổi Hoàn thành M1 thành 80, bấm Lưu",
     "—",
     "- Form mở với số đã nhập (50%)\n"
     "- Thông báo \"Chỉnh sửa phiếu nhập kết quả thành công!\"\n"
     "- NKQ-02 vẫn Đang tạo, CK đề xuất duyệt 1,6"),

    ("002", "Sửa rồi Lưu & Gửi duyệt", "P0",
     DATA + "\nNKQ-02 Đang tạo",
     "1. KTV-1 mở Sửa NKQ-02\n"
     "2. Tích Đã hoàn thành M1, bấm \"Lưu & Gửi duyệt\"",
     "—",
     "- NKQ-02 chuyển \"Chờ duyệt kết quả\"\n"
     "- PGV-02 chuyển \"Đã nhập kết quả\"\n"
     "- QL-1 nhận thông báo cần duyệt"),

    ("003", "Sửa phiếu bị Không duyệt và gửi lại", "P0",
     DATA + "\nNKQ-03: KTV-1 lập, Không duyệt kết quả, lý do \"Thiếu ảnh biên bản\"",
     "1. KTV-1 mở Sửa NKQ-03\n"
     "2. Thêm ảnh biên bản bàn giao, bấm \"Lưu & Gửi duyệt\"",
     "—",
     "- NKQ-03 chuyển \"Chờ duyệt kết quả\"\n"
     "- Bánh răng không còn Sửa, Xóa"),

    ("004", "Xóa file đính kèm ở màn Sửa", "P2",
     DATA + "\nNKQ-02 Đang tạo có file dinhkem.pdf",
     "1. KTV-1 mở Sửa NKQ-02\n"
     "2. Bấm xóa file dinhkem.pdf, xác nhận",
     "—",
     "- Thông báo \"Xóa thành công\", file biến mất khỏi danh sách"),

    ("005", "Sửa qua đường dẫn phiếu Đã duyệt kết quả", "P0",
     DATA + "\nNKQ-04: KTV-1 lập, Đã duyệt kết quả; KTV-1 có đường dẫn Sửa NKQ-04",
     "1. Đăng nhập KTV-1, dán đường dẫn Sửa NKQ-04\n"
     "2. Đổi Ghi chú, bấm Lưu",
     "—",
     "- Mong đợi: không mở được form hoặc báo không được sửa\n"
     "- Lưu ý: theo code hiện tại Lưu thành công, NKQ-04 về \"Đang tạo\" và phiếu giao việc về \"Đang nhập kết "
     "quả\" dù đã duyệt - ghi Failed"),

    ("006", "Xóa phiếu Đang tạo", "P0",
     DATA + "\nNKQ-02 của PGV-02, Đang tạo",
     "1. " + OPEN_KTV1 + "\n"
     "2. Bánh răng dòng NKQ-02 chọn Xóa, xác nhận\n"
     "3. Mở " + "Phiếu giao việc được giao, bánh răng dòng PGV-02",
     "—",
     "- NKQ-02 biến mất khỏi danh sách\n"
     "- PGV-02 về \"Chờ thực hiện\", có lại nút \"Nhập kết quả\""),

    ("007", "Xóa phiếu Không duyệt kết quả", "P1",
     DATA + "\nNKQ-03 Không duyệt kết quả",
     "1. KTV-1 bánh răng dòng NKQ-03 chọn Xóa, xác nhận",
     "—",
     "- NKQ-03 bị xóa, phiếu giao việc về \"Chờ thực hiện\""),

    ("008", "Hủy hộp xác nhận xóa", "P2",
     DATA + "\nNKQ-02 Đang tạo",
     "1. KTV-1 bánh răng NKQ-02 chọn Xóa, bấm Hủy",
     "—",
     "- NKQ-02 vẫn còn"),

    ("009", "Xóa qua đường dẫn phiếu Chờ duyệt", "P1",
     DATA + "\nNKQ-01 Chờ duyệt kết quả; KTV-1 có đường dẫn Xóa NKQ-01",
     "1. Đăng nhập KTV-1, dán đường dẫn Xóa NKQ-01",
     "—",
     "- NKQ-01 không bị xóa\n"
     "- Mong đợi: có câu báo không được xóa\n"
     "- Lưu ý: theo code hiện tại chỉ chuyển về danh sách, không báo gì - ghi Failed"),

    ("010", "Người khác xóa qua đường dẫn", "P0",
     DATA + "\nNKQ-02 của KTV-1, Đang tạo",
     "1. Đăng nhập KTV-2, dán đường dẫn Xóa NKQ-02",
     "—",
     "- NKQ-02 không bị xóa"),
]

SEC_X = [
    ("001", "Không duyệt từ danh sách", "P0",
     DATA + "\nNKQ-01: KTV-1 lập cho PGV-01, Chờ duyệt kết quả",
     "1. " + OPEN_QL1 + "\n"
     "2. Bánh răng dòng NKQ-01 chọn \"Không duyệt kết quả\"\n"
     "3. Nhập lý do \"Thiếu ảnh biên bản\", bấm Xác nhận",
     "Tài khoản: QL-1",
     "- Thông báo \"Thao tác thành công!\"\n"
     "- NKQ-01 chuyển \"Không duyệt kết quả\"\n"
     "- KTV-1 nhận thông báo \"QL-1 vừa không duyệt phiếu nhập kết quả của bạn!\""),

    ("002", "Không duyệt khi bỏ trống lý do", "P0",
     DATA + "\nNKQ-01 Chờ duyệt kết quả",
     "1. QL-1 chọn \"Không duyệt kết quả\" ở NKQ-01\n"
     "2. Để trống lý do, bấm Xác nhận",
     "—",
     "- Báo \"Bạn phải nhập lý do không duyệt\", hộp vẫn mở\n"
     "- NKQ-01 vẫn Chờ duyệt kết quả"),

    ("003", "Lý do chỉ có khoảng trắng", "P2",
     DATA + "\nNKQ-01 Chờ duyệt kết quả",
     "1. QL-1 chọn \"Không duyệt kết quả\" ở danh sách, gõ 3 dấu cách, bấm Xác nhận\n"
     "2. Làm lại ở màn chi tiết",
     "—",
     "- Bước 2: báo \"Bạn phải nhập lý do không duyệt\"\n"
     "- Mong đợi bước 1 giống bước 2\n"
     "- Lưu ý: theo code hiện tại bước 1 báo \"Thao tác thất bại!\" - ghi Failed"),

    ("004", "Không duyệt từ màn chi tiết", "P1",
     DATA + "\nNKQ-01 Chờ duyệt kết quả",
     "1. QL-1 mở chi tiết NKQ-01, bấm \"Không duyệt\"\n"
     "2. Nhập lý do, Xác nhận",
     "—",
     "- NKQ-01 \"Không duyệt kết quả\", chuyển về danh sách"),

    ("005", "Sau khi Không duyệt, người lập sửa được", "P0",
     DATA + "\nNKQ-01 vừa bị Không duyệt",
     "1. " + OPEN_KTV1 + "\n"
     "2. Bánh răng dòng NKQ-01",
     "—",
     "- Có Sửa, Xóa\n"
     "- Chi tiết NKQ-01 hiện lý do ở khung \"Ghi chú duyệt\"\n"
     "- PGV-01 vẫn \"Đã nhập kết quả\" (ghi nhận, để nghiệp vụ xác nhận)"),

    ("006", "Bấm Duyệt kết quả mở phiếu duyệt kết quả", "P0",
     DATA + "\nNKQ-01 Chờ duyệt kết quả",
     "1. QL-1 bánh răng dòng NKQ-01 chọn \"Duyệt kết quả\"",
     "—",
     "- Mở form tạo phiếu duyệt kết quả, lấy sẵn kết quả của NKQ-01"),

    ("007", "Lưu nháp phiếu duyệt kết quả", "P0",
     DATA + "\nNKQ-01 Chờ duyệt kết quả",
     "1. QL-1 mở \"Duyệt kết quả\" của NKQ-01, bấm lưu nháp\n"
     "2. Mở lại danh sách Phiếu nhập kết quả",
     "—",
     "- NKQ-01 chuyển \"Đang duyệt kết quả\", không còn nút Duyệt / Không duyệt kết quả\n"
     "- PGV-01 chuyển \"Đang duyệt kết quả\""),

    ("008", "Duyệt xong phiếu duyệt kết quả", "P0",
     DATA + "\nNKQ-01 Chờ duyệt kết quả",
     "1. QL-1 mở \"Duyệt kết quả\" của NKQ-01, bấm lưu và duyệt\n"
     "2. Mở danh sách Phiếu nhập kết quả",
     "—",
     "- NKQ-01 \"Đã duyệt kết quả\", Người duyệt QL-1, Ngày duyệt là lúc duyệt\n"
     "- PGV-01 \"Đã duyệt kết quả\"\n"
     "- KTV-1 không còn Sửa, Xóa"),

    ("009", "Không duyệt từ phiếu duyệt kết quả đang lưu nháp", "P1",
     DATA + "\nNKQ-05 Đang duyệt kết quả, đã có phiếu duyệt kết quả lưu nháp",
     "1. QL-1 mở phiếu duyệt kết quả nháp của NKQ-05, bấm Không duyệt, nhập lý do",
     "—",
     "- NKQ-05 chuyển \"Không duyệt kết quả\", phiếu duyệt kết quả nháp bị xóa\n"
     "- Người lập NKQ-05 nhận thông báo không duyệt"),

    ("010", "Không duyệt qua đường dẫn phiếu đã duyệt", "P1",
     DATA + "\nNKQ-04 Đã duyệt kết quả",
     "1. QL-1 dùng công cụ kiểm thử API gọi thẳng chức năng Không duyệt NKQ-04 kèm lý do",
     "—",
     "- Báo \"Không có quyền!\", NKQ-04 vẫn Đã duyệt kết quả"),

    ("011", "Mở Duyệt kết quả qua đường dẫn khi khác công ty", "P1",
     DATA + "\nNKQ-01 (TPE) Chờ duyệt kết quả",
     "1. Đăng nhập QL-9 (TPC), dán đường dẫn \"Duyệt kết quả\" của NKQ-01",
     "—",
     "- Ra trang không tìm thấy, không mở được form duyệt"),
]

SEC_XI = [
    ("001", "Nhập kết quả lần hai cho cùng phiếu giao việc", "P0",
     DATA,
     "1. KTV-1 mở form nhập kết quả PGV-02 ở 2 tab\n"
     "2. Tab 1 bấm Lưu (thành công)\n"
     "3. Sau đó tab 2 bấm Lưu",
     "—",
     "- Tab 2 báo \"Phiếu giao việc này đã có phiếu nhập kết quả, không thể tạo thêm. Vui lòng mở phiếu kết "
     "quả đã có để chỉnh sửa.\"\n"
     "- Chỉ có 1 phiếu nhập kết quả cho PGV-02"),

    ("002", "Hai tab bấm Lưu đúng cùng lúc", "P2",
     DATA,
     "1. KTV-1 mở form nhập kết quả PGV-02 ở 2 tab\n"
     "2. Bấm Lưu ở 2 tab gần như cùng lúc",
     "—",
     "- Chỉ 1 phiếu được tạo\n"
     "- Mong đợi tab sau thấy câu báo như TC 001\n"
     "- Lưu ý: theo code hiện tại tab sau có thể thấy đoạn lỗi kỹ thuật của cơ sở dữ liệu - ghi Failed nếu gặp"),

    ("003", "Người không thực hiện lưu kết quả bằng cách gọi thẳng", "P0",
     DATA,
     "1. Đăng nhập KTV-2 (không thực hiện PGV-03, không có quyền \"Nhập kết quả thực hiện\")\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng lưu phiếu nhập kết quả cho PGV-03",
     "—",
     "- Mong đợi: báo không có quyền\n"
     "- Lưu ý: theo code hiện tại tạo được phiếu, KTV-2 là người tạo, PGV-03 chuyển \"Đang nhập kết quả\" - "
     "ghi Failed"),

    ("004", "Gọi thẳng chức năng lưu với trạng thái Đã duyệt kết quả", "P1",
     DATA,
     "1. Đăng nhập KTV-1\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng lưu cho PGV-03, gửi trạng thái \"Đã duyệt kết quả\"",
     "—",
     "- Mong đợi: chỉ nhận Đang tạo hoặc Chờ duyệt kết quả\n"
     "- Lưu ý: theo code hiện tại phiếu được tạo ở trạng thái \"Đã duyệt kết quả\" mà không qua duyệt - ghi "
     "Failed"),

    ("005", "Gọi thẳng chức năng sửa đổi sang phiếu giao việc khác", "P2",
     DATA + "\nNKQ-02 của PGV-02 Đang tạo; PGV-03 chưa có phiếu nhập kết quả",
     "1. KTV-1 dùng công cụ kiểm thử API gọi chức năng sửa NKQ-02, đổi phiếu giao việc thành PGV-03",
     "—",
     "- Mong đợi: không cho đổi phiếu giao việc\n"
     "- Lưu ý: theo code hiện tại NKQ-02 chuyển sang PGV-03, PGV-02 không còn phiếu nhập kết quả - ghi Failed"),

    ("006", "Người lập sửa trong lúc người duyệt đang xem", "P1",
     DATA + "\nNKQ-01 Chờ duyệt kết quả; QL-1 đang mở chi tiết NKQ-01",
     "1. KTV-1 dán đường dẫn Sửa NKQ-01, đổi % rồi bấm Lưu\n"
     "2. QL-1 bấm \"Không duyệt\"",
     "—",
     "- Mong đợi: bước 1 bị chặn vì phiếu đang Chờ duyệt\n"
     "- Lưu ý: theo code hiện tại bước 1 lưu được và NKQ-01 về Đang tạo; bước 2 báo \"Không có quyền!\" - ghi "
     "Failed"),

    ("007", "Hai người duyệt cùng Không duyệt", "P2",
     DATA + "\nQL-2 cũng có quyền duyệt ở TPE; NKQ-01 Chờ duyệt kết quả",
     "1. QL-1 và QL-2 cùng mở chi tiết NKQ-01\n"
     "2. QL-1 bấm Không duyệt (thành công), sau đó QL-2 bấm Không duyệt",
     "—",
     "- QL-2 báo \"Không có quyền!\"\n"
     "- KTV-1 chỉ nhận 1 thông báo"),
]

SEC_XII = [
    ("001", "Luồng lắp đặt: nhập, bị Không duyệt, gửi lại, duyệt", "P0",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-01") + ", tích Đã hoàn thành M3, nhập serial S3-5, bấm \"Lưu & Gửi duyệt\"\n"
     "2. QL-1 Không duyệt, lý do \"Thiếu ảnh\"\n"
     "3. KTV-1 Sửa, thêm ảnh công trình, \"Lưu & Gửi duyệt\"\n"
     "4. QL-1 bấm Duyệt kết quả, lưu và duyệt phiếu duyệt kết quả",
     "—",
     "- Sau bước 1: phiếu Chờ duyệt kết quả, PGV-01 Đã nhập kết quả\n"
     "- Sau bước 2: Không duyệt kết quả\n"
     "- Sau bước 3: Chờ duyệt kết quả\n"
     "- Sau bước 4: phiếu và PGV-01 \"Đã duyệt kết quả\", Tổng công định mức 2"),

    ("002", "Luồng sửa chữa: lưu nháp, xóa, nhập lại", "P0",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-02") + ", hoàn thành 50%, bấm Lưu\n"
     "2. Xóa phiếu vừa tạo\n"
     "3. Bấm lại \"Nhập kết quả\" ở PGV-02, tích Đã hoàn thành, \"Lưu & Gửi duyệt\"",
     "—",
     "- Sau bước 1: PGV-02 Đang nhập kết quả\n"
     "- Sau bước 2: PGV-02 Chờ thực hiện, có lại nút Nhập kết quả\n"
     "- Sau bước 3: phiếu mới Chờ duyệt kết quả, CK đề xuất 2"),

    ("003", "Luồng giao việc khác có công phụ", "P1",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-04") + ", tích Đã hoàn thành, thêm công phụ \"Đo đạc\" ĐM 0,2 đề xuất 0,2 "
     "đã hoàn thành\n"
     "2. Bấm \"Lưu & Gửi duyệt\"\n"
     "3. QL-1 mở chi tiết",
     "—",
     "- Tổng công định mức 0,7 (0,5 + 0,2)\n"
     "- QL-1 thấy đúng 2 dòng và có nút duyệt"),

    ("004", "Luồng bảo hành đến khi duyệt", "P1",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-03") + ", tích Đã hoàn thành M2, \"Lưu & Gửi duyệt\"\n"
     "2. QL-1 Duyệt kết quả",
     "—",
     "- Phiếu nhập kết quả và PGV-03 \"Đã duyệt kết quả\"\n"
     "- Danh sách hiện Người duyệt QL-1"),
]
