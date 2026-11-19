# -*- coding: utf-8 -*-
"""Section V - VIII cho man Phieu nhap ket qua."""
from tc_data_role import MENU, MENU_PGV, MENU_DG, DATA, OPEN_KTV1, OPEN_QL1, FROM_PGV

SEC_V = [
    ("001", "Sửa chữa: hoàn thành máy M1", "P0",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-02") + "\n"
     "2. Tích Đã hoàn thành dòng M1",
     "—",
     "- Hoàn thành = 100%, ô bị khóa\n"
     "- SL bàn giao 1 (không sửa được), Serial điền sẵn S1\n"
     "- CK đề xuất duyệt 2; Công khoán chính và Tổng công định mức 2"),

    ("002", "Sửa chữa: hoàn thành một phần", "P0",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-02") + "\n"
     "2. Không tích, nhập Hoàn thành 50",
     "—",
     "- CK đề xuất duyệt 1\n"
     "- Tổng công định mức 1"),

    ("003", "Đã hoàn thành mà xóa trống serial", "P0",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-02") + "\n"
     "2. Tích Đã hoàn thành dòng M1, xóa trống ô Serial, bấm Lưu",
     "—",
     "- Báo lỗi bắt buộc nhập Serial, không tạo phiếu"),

    ("004", "Serial nhập là 0", "P2",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-02") + "\n"
     "2. Tích Đã hoàn thành, gõ Serial \"0\", bấm Lưu",
     "—",
     "- Báo lỗi Serial không hợp lệ, không tạo phiếu"),

    ("005", "Nhập serial mới khi thiết bị đã đủ serial đang dùng", "P0",
     DATA + "\nKhách hàng có 1 máy M1, serial S1 đang sử dụng",
     "1. " + FROM_PGV.format(pgv="PGV-02") + "\n"
     "2. Tích Đã hoàn thành, gõ Serial mới S1-NEW (không chọn từ danh sách), bấm Lưu",
     "—",
     "- Báo \"Thiết bị \"M1\": số serial đang sử dụng đã đủ theo số lượng thiết bị. Vui lòng vào Danh mục "
     "serial thiết bị để ngừng sử dụng bớt 1 serial cũ trước khi nhập serial mới.\"\n"
     "- Ô Serial vừa gõ bị xóa trống, không tạo phiếu"),

    ("006", "Nhập serial thêm vượt số chỗ còn trống", "P1",
     DATA + "\nKhách hàng có 3 máy M1 nhưng mới có 2 serial đang sử dụng; phiếu giao việc gồm 2 dòng M1",
     "1. Mở form nhập kết quả, tích Đã hoàn thành 2 dòng M1\n"
     "2. Gõ 2 serial mới khác nhau SN-A, SN-B, bấm Lưu",
     "—",
     "- Báo \"Thiết bị \"M1\": số serial nhập thêm (2) vượt quá số lượng thiết bị còn có thể gắn serial (1).\"\n"
     "- Không tạo phiếu"),

    ("007", "Dịch vụ và vật tư đi kèm máy sửa chữa", "P1",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-02") + "\n"
     "2. Dưới dòng M1, tích hoàn thành dịch vụ \"Vệ sinh máy\", sửa SL vật tư VT1 thành 2, bấm Lưu\n"
     "3. Mở lại phiếu vừa tạo",
     "—",
     "- Dịch vụ \"Vệ sinh máy\" ở trạng thái hoàn thành\n"
     "- Vật tư VT1 SL 2"),

    ("008", "Bảo hành: hoàn thành máy M2", "P0",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-03") + "\n"
     "2. Tích Đã hoàn thành dòng M2 (serial S2), bấm \"Lưu & Gửi duyệt\"",
     "—",
     "- Thông báo \"Tạo phiếu nhập kết quả thành công!\"\n"
     "- Phiếu mới Chờ duyệt kết quả; Tổng công định mức 1,5"),

    ("009", "Bảo hành: hoàn thành một phần", "P1",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-03") + "\n"
     "2. Không tích, nhập Hoàn thành 40",
     "—",
     "- CK đề xuất duyệt 0,6\n"
     "- Tổng công định mức 0,6"),

    ("010", "Đính kèm ảnh công trình đúng định dạng", "P2",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-02") + "\n"
     "2. Ảnh công trình chọn file anh1.jpg (2MB); Ảnh biên bản bàn giao chọn bienban.pdf\n"
     "3. Tích Đã hoàn thành, bấm Lưu, mở lại phiếu",
     "—",
     "- Phiếu lưu thành công, hiện đủ 2 file, bấm xem được"),
]

SEC_VI = [
    ("001", "Giao việc khác: công khoán đề xuất mặc định", "P0",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-04"),
     "—",
     "- Dòng \"Khảo sát mặt bằng\": ĐM công 0,5; Công khoán đề xuất duyệt điền sẵn 0,5 (sửa được)\n"
     "- Tổng công định mức 0,5"),

    ("002", "Giao việc khác: hạ công khoán đề xuất", "P1",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-04") + "\n"
     "2. Tích Đã hoàn thành, sửa Công khoán đề xuất duyệt 0,3, bấm Lưu",
     "—",
     "- Lưu thành công; Tổng công định mức 0,3"),

    ("003", "Công khoán đề xuất vượt định mức công", "P0",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-04") + "\n"
     "2. Sửa Công khoán đề xuất duyệt 0,8, bấm Lưu",
     "—",
     "- Báo \"Công khoán đề xuất duyệt không được lớn hơn định mức công\", không tạo phiếu"),

    ("004", "Thêm dòng công phụ P3", "P0",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-02") + "\n"
     "2. Tích Đã hoàn thành M1\n"
     "3. Ở \"B - Công phụ tính P3\" bấm dấu +, nhập \"Đi dây điện\", ĐM công 0,5, Công khoán đề xuất 0,5, tích "
     "Đã hoàn thành",
     "—",
     "- Công khoán chính 2, Công khoán phụ 0,5, Tổng công định mức 2,5"),

    ("005", "Công phụ chưa tích hoàn thành không tính", "P1",
     DATA,
     "1. Như TC 004 nhưng không tích Đã hoàn thành dòng \"Đi dây điện\"",
     "—",
     "- Công khoán phụ 0, Tổng công định mức 2"),

    ("006", "Công phụ đề xuất vượt ĐM công", "P1",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-02") + "\n"
     "2. Thêm công phụ \"Đi dây điện\" ĐM công 0,5, Công khoán đề xuất 1, bấm Lưu",
     "—",
     "- Báo \"Công khoán đề xuất duyệt không được lớn hơn định mức công\", không tạo phiếu"),

    ("007", "Công phụ để trống tên hoặc ĐM công", "P1",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-02") + "\n"
     "2. Bấm + thêm công phụ, để trống tên và ĐM công, bấm Lưu",
     "—",
     "- Báo lỗi bắt buộc nhập ở dòng công phụ, không tạo phiếu"),

    ("008", "Xóa dòng công phụ vừa thêm", "P2",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-02") + "\n"
     "2. Thêm công phụ rồi bấm dấu x đỏ cạnh tên",
     "—",
     "- Dòng bị xóa, Công khoán phụ về 0"),

    ("009", "Tiêu đề khối dịch vụ trả tiền", "P2",
     DATA + "\nPGV-02 có vật tư VT1 cho sửa chữa nhưng không có vật tư cho bảo hành",
     "1. " + FROM_PGV.format(pgv="PGV-02"),
     "—",
     "- Mong đợi: chỉ một tiêu đề khối dịch vụ trả tiền, ghi đúng chữ \"DANH SÁCH DỊCH VỤ TRẢ TIỀN\"\n"
     "- Lưu ý: theo code hiện tại hiện cả \"C - DANH SÁCH DỊCH VỤ TRẢ TIỀN\" và \"B - DANH SÁCH VỤ TRẢ TIỀN\" "
     "(thiếu chữ \"DỊCH\") - ghi Failed"),
]

SEC_VII = [
    ("001", "Lưu phiếu nháp", "P0",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-02") + "\n"
     "2. Tích Đã hoàn thành M1, bấm Lưu",
     "—",
     "- Thông báo \"Tạo phiếu nhập kết quả thành công!\", chuyển sang danh sách\n"
     "- Phiếu mới có số dạng <mã công ty>.PNKQ.<năm><số thứ tự>, trạng thái \"Đang tạo\"\n"
     "- PGV-02 chuyển \"Đang nhập kết quả\""),

    ("002", "Lưu & Gửi duyệt", "P0",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-02") + "\n"
     "2. Tích Đã hoàn thành M1, bấm \"Lưu & Gửi duyệt\"",
     "—",
     "- Phiếu mới \"Chờ duyệt kết quả\"\n"
     "- PGV-02 chuyển \"Đã nhập kết quả\"\n"
     "- QL-1 nhận thông báo \"Bạn có 1 phiếu kết quả giao việc cần duyệt\""),

    ("003", "Gửi duyệt khi không hoàn thành việc nào", "P0",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-02") + "\n"
     "2. Không tích Đã hoàn thành, nhập Hoàn thành 30, bấm \"Lưu & Gửi duyệt\"",
     "—",
     "- Hiện hộp \"Phiếu không hoàn thành công việc, bạn có đồng ý không?\"\n"
     "- Bấm Hủy: không tạo phiếu, ở lại form\n"
     "- Bấm Xác nhận: tạo phiếu Chờ duyệt kết quả"),

    ("004", "Lưu nháp không hỏi xác nhận dù chưa hoàn thành", "P2",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-02") + "\n"
     "2. Không tích, nhập Hoàn thành 30, bấm Lưu",
     "—",
     "- Không hiện hộp xác nhận, phiếu Đang tạo được tạo"),

    ("005", "Nút Lưu khóa khi đang gửi", "P2",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-02") + "\n"
     "2. Bấm \"Lưu & Gửi duyệt\" rồi bấm tiếp ngay",
     "—",
     "- Nút hiện biểu tượng chờ và bị khóa, chỉ 1 phiếu được tạo"),

    ("006", "Thông báo gửi duyệt chỉ tới người duyệt cùng công ty", "P1",
     DATA,
     "1. KTV-1 gửi duyệt phiếu nhập kết quả của PGV-02\n"
     "2. Đăng nhập QL-9 (TPC) xem chuông thông báo",
     "—",
     "- QL-9 không nhận thông báo"),

    ("007", "Ô trang chủ đếm phiếu chờ duyệt", "P0",
     DATA + "\nTPE đang có 2 phiếu Chờ duyệt kết quả; TPC có 1",
     "1. Đăng nhập QL-1, xem trang chủ\n"
     "2. Bấm ô \"Chờ duyệt phiếu nhập kết quả giao việc\"",
     "—",
     "- Ô hiện 2\n"
     "- Mở danh sách chỉ có 2 phiếu Chờ duyệt kết quả của TPE"),

    ("008", "Ô trang chủ không hiện với người không có quyền duyệt", "P2",
     DATA,
     "1. Đăng nhập KTV-1, xem trang chủ",
     "—",
     "- Không có ô \"Chờ duyệt phiếu nhập kết quả giao việc\""),

    ("009", "Nút Quay lại", "P2",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-02") + "\n"
     "2. Bấm Quay lại",
     "—",
     "- Về danh sách Phiếu nhập kết quả, không tạo phiếu"),
]

SEC_VIII = [
    ("001", "Xem chi tiết phiếu", "P0",
     DATA + "\nNKQ-01: KTV-1 lập cho PGV-01, 3 máy M3 Đã hoàn thành, Chờ duyệt kết quả",
     "1. " + OPEN_KTV1 + "\n"
     "2. Bấm số NKQ-01",
     "—",
     "- Mở tab mới, mọi ô bị khóa\n"
     "- Bảng lắp đặt đúng số đã nhập, Tổng công định mức 2\n"
     "- KTV-1 không có nút Sửa, Duyệt; chỉ có Quay lại"),

    ("002", "Chi tiết với người duyệt có nút duyệt", "P0",
     DATA + "\nNKQ-01 Chờ duyệt kết quả",
     "1. Đăng nhập QL-1, mở chi tiết NKQ-01",
     "—",
     "- Có khung \"Ghi chú duyệt\", nút \"Không duyệt\" và \"Duyệt kết quả\""),

    ("003", "Chi tiết phiếu bị Không duyệt hiện lý do", "P1",
     DATA + "\nNKQ-03 Không duyệt kết quả với lý do \"Thiếu ảnh biên bản\"",
     "1. " + OPEN_KTV1 + ", mở chi tiết NKQ-03",
     "—",
     "- Khung \"Ghi chú duyệt\" hiện \"Thiếu ảnh biên bản\", không sửa được"),

    ("004", "Mở phiếu nhập kết quả từ phiếu giao việc", "P1",
     DATA + "\nPGV-01 đã có NKQ-01",
     "1. Đăng nhập KTV-1, " + MENU_DG + "\n"
     "2. Bấm nút bánh răng dòng PGV-01, chọn \"Xem phiếu nhập kết quả\"",
     "—",
     "- Mở chi tiết NKQ-01"),

    ("005", "Bấm số phiếu giao việc trên danh sách", "P2",
     DATA + "\nNKQ-01 của PGV-01",
     "1. " + OPEN_KTV1 + "\n"
     "2. Bấm số PGV-01 ở dòng NKQ-01",
     "—",
     "- Mở chi tiết PGV-01 ở tab mới"),
]
