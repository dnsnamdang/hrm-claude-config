# -*- coding: utf-8 -*-
"""Section I, II, III — hien thi trang & loi vao, bo loc, danh sach."""
from tc_data_role import MENU

SEC_I = [
    ("001", "Vào màn từ menu Kho", "P0",
     "Tài khoản có quyền \"Xem điều chuyển vị trí theo công ty\"",
     "1. " + MENU,
     "—",
     "- Mở màn danh sách phiếu điều chuyển vị trí, bảng tải dữ liệu không lỗi"),

    ("002", "Bố cục màn danh sách", "P0",
     "Phạm vi có ít nhất 12 phiếu",
     "1. Quan sát từ trên xuống",
     "—",
     "- Hàng lọc: ô \"Chọn khoảng thời gian\", ô \"Tên, mã hàng hóa\", ô \"Chọn kho\"; nút Tìm kiếm, Tạo mới, Xuất excel\n"
     "- Cột: STT, Mã phiếu, Ngày lập, Kho, Phiếu kiểm kê, Trạng thái, Người lập, Hành động\n"
     "- Dưới tiêu đề cột Mã phiếu có ô tìm, dưới cột Trạng thái có ô chọn\n"
     "- 10 dòng mỗi trang, phiếu mới nhất lên đầu"),

    ("003", "Sửa tham số trên thanh địa chỉ không đổi phạm vi", "P1",
     "C có quyền xem theo công ty",
     "1. Mở màn từ menu, ghi tổng\n"
     "2. Xóa phần tham số sau dấu hỏi trên thanh địa chỉ, nhấn Enter\n"
     "3. Đổi thành giá trị lạ abc",
     "—",
     "- Cả 3 lần tổng như nhau, không lỗi"),

    ("004", "Nhãn trạng thái", "P0",
     "Có phiếu Đang tạo và Đã chuyển",
     "1. Mở ô chọn dưới cột Trạng thái\n"
     "2. Quan sát nhãn",
     "—",
     "- Ô có 2 lựa chọn: Đã chuyển, Đang tạo\n"
     "- Đã chuyển nền XANH, Đang tạo nền ĐỎ"),

    ("005", "Mã phiếu chỉ bấm được khi Đã chuyển", "P1",
     "PĐ-1 Đang tạo, PĐ-3 Đã chuyển",
     "1. Bấm vào Mã phiếu của PĐ-1\n"
     "2. Bấm vào Mã phiếu của PĐ-3",
     "—",
     "- PĐ-1: chữ thường, không bấm được\n"
     "- PĐ-3: mở màn Chi tiết"),

    ("006", "Menu bánh răng theo trạng thái", "P0",
     "PĐ-1 Đang tạo, PĐ-3 Đã chuyển",
     "1. Bấm bánh răng từng phiếu",
     "—",
     "- PĐ-1: Sửa, Xóa\n"
     "- PĐ-3: In phiếu"),

    ("007", "Bố cục màn Chi tiết", "P0",
     "PĐ-3 Đã chuyển kho K1, ghi chú \"Dồn hàng\", 2 dòng, 1 file PDF",
     "1. Bấm Mã phiếu PĐ-3",
     "—",
     "- Tiêu đề \"Phiếu điều chuyển vị trí: <Mã phiếu>\"\n"
     "- Kho, Ghi chú hiện đúng, bị khóa; File đính kèm mở được\n"
     "- Bảng: STT, Tên hàng hóa, Model, Mã hàng hóa, Đơn vị tính, Vị trí xuất, Lô xuất, Vị trí nhập, SL\n"
     "- Chỉ có nút Quay lại, KHÔNG có nút In"),

    ("008", "Cột Phiếu kiểm kê", "P1",
     "PĐ-4 lập từ phiếu kiểm kê theo vị trí KK-2; PĐ-5 lập từ phiếu kiểm kê theo hàng hóa KKHH-1",
     "1. Đọc cột Phiếu kiểm kê của PĐ-4, PĐ-5",
     "—",
     "- PĐ-5 hiện mã KKHH-1\n"
     "- Mong đợi PĐ-4 hiện mã KK-2; Lưu ý: code hiện tại để trống — nếu vậy ghi Failed"),

    ("009", "Mở Tạo mới từ phiếu kiểm kê theo vị trí", "P0",
     "KK-2 Chờ xử lý có dòng thiếu 2 cái HH-0091 ở P1 lô L02; XL có quyền Xử lý phiếu kiểm kê vị trí và Điều "
     "chuyển vị trí",
     "1. XL mở Chi tiết KK-2, bấm \"Tạo phiếu điều chuyển vị trí\"",
     "—",
     "- Mở tab mới \"Tạo phiếu điều chuyển vị trí\"\n"
     "- Kho = kho của KK-2, bị khóa\n"
     "- Có sẵn dòng HH-0091, Vị trí xuất P1, Lô xuất L02, SL 2; các ô này bị khóa\n"
     "- Ô Vị trí nhập trống, chọn được"),

    ("010", "Người xử lý thiếu quyền Điều chuyển vị trí", "P1",
     "XL2 có quyền Xử lý phiếu kiểm kê vị trí nhưng KHÔNG có quyền Điều chuyển vị trí",
     "1. XL2 mở KK-2, bấm \"Tạo phiếu điều chuyển vị trí\"",
     "—",
     "- Tab mới hiện trang không tìm thấy"),

    ("011", "Mở Tạo mới từ phiếu kiểm kê theo hàng hóa", "P1",
     "Phiếu kiểm kê theo hàng hóa KKHH-1 đang xử lý, có dòng cần điều chuyển",
     "1. Mở Chi tiết KKHH-1, bấm \"Tạo phiếu điều chuyển vị trí\"",
     "—",
     "- Màn Tạo mới có sẵn kho và các dòng của KKHH-1; Kho, ĐVT, Vị trí xuất, Lô, SL bị khóa"),

    ("012", "Bộ lọc được ghi nhớ khi quay lại", "P2",
     "—",
     "1. Gõ Mã phiếu, sang trang 2\n"
     "2. Rời màn rồi mở lại từ menu",
     "—",
     "- Ô Mã phiếu và trang 2 được giữ"),
]


SEC_II = [
    ("001", "Lọc Mã phiếu khớp một phần", "P0",
     "Có PĐCVT-00318 và PĐCVT-00319",
     "1. Gõ 0031 vào ô dưới cột Mã phiếu",
     "Mã phiếu: 0031",
     "- Hiện cả 2 phiếu"),

    ("002", "Lọc Trạng thái", "P0",
     "Có 3 phiếu Đang tạo, 9 phiếu Đã chuyển",
     "1. Chọn Trạng thái = Đang tạo, rồi Đã chuyển",
     "—",
     "- Lần lượt 3 và 9 dòng"),

    ("003", "Lọc theo tên hoặc mã hàng hóa", "P0",
     "PĐ-3 có hàng HH-0091 \"Máy bơm ly tâm 2HP\"; PĐ-6 không có",
     "1. Gõ HH-0091 vào ô \"Tên, mã hàng hóa\", nhấn Enter\n"
     "2. Đổi thành \"ly tâm\", bấm Tìm kiếm",
     "Hàng hóa: HH-0091 / ly tâm",
     "- Cả hai lần có PĐ-3, không có PĐ-6"),

    ("004", "Lọc hàng hóa với phiếu nháp", "P2",
     "PĐ-1 Đang tạo có hàng HH-0091",
     "1. Gõ HH-0091, bấm Tìm kiếm",
     "—",
     "- Mong đợi: có PĐ-1\n"
     "- Lưu ý: ô này chỉ tìm trong dòng của phiếu ĐÃ CHUYỂN, phiếu nháp có thể không hiện — ghi nhận"),

    ("005", "Lọc theo kho", "P0",
     "K1 có 5 phiếu, K2 có 4 phiếu",
     "1. Chọn ô \"Chọn kho\" = K1, bấm Tìm kiếm",
     "Kho: K1",
     "- 5 dòng, cột Kho đều là K1\n"
     "- Ô Chọn kho liệt kê kho của mọi công ty dạng \"mã - tên\""),

    ("006", "Lọc khoảng thời gian, ngày kết thúc", "P0",
     "PĐ-7 lập 09:00 ngày 05/10/2026; PĐ-8 lập 08:00 ngày 01/10/2026",
     "1. Chọn khoảng 01/10/2026 đến 05/10/2026, bấm Apply, bấm Tìm kiếm",
     "Khoảng: 01/10/2026 - 05/10/2026",
     "- Ô hiện \"01/10/2026 đến 05/10/2026\"\n"
     "- Có PĐ-8\n"
     "- Mong đợi có PĐ-7; Lưu ý: code hiện tại loại phiếu trong ngày kết thúc — nếu không có PĐ-7 thì ghi Failed"),

    ("007", "Xóa khoảng thời gian", "P2",
     "Đang lọc khoảng thời gian",
     "1. Mở ô thời gian, bấm Clear, bấm Tìm kiếm",
     "—",
     "- Ô trống, danh sách về đủ phạm vi"),

    ("008", "Kết hợp nhiều điều kiện", "P1",
     "K1 có 5 phiếu, 2 Đang tạo",
     "1. Chọn kho K1, Trạng thái = Đang tạo, bấm Tìm kiếm",
     "—",
     "- 2 dòng"),

    ("009", "Ký tự đặc biệt", "P2",
     "—",
     "1. Gõ %, _ , ' vào ô Mã phiếu và ô hàng hóa",
     "—",
     "- Không lỗi, không treo trang"),
]


SEC_III = [
    ("001", "Mặc định mới nhất lên đầu", "P0",
     "Phiếu lập 01/10, 05/10, 10/10/2026",
     "1. Mở màn từ menu",
     "—",
     "- Thứ tự 10/10, 05/10, 01/10"),

    ("002", "Sắp xếp theo Mã phiếu, Ngày lập, Trạng thái", "P1",
     "Có ít nhất 5 phiếu",
     "1. Bấm tiêu đề Mã phiếu, Ngày lập, Trạng thái, mỗi cột 2 lần\n"
     "2. Thử bấm Kho, Phiếu kiểm kê, Người lập",
     "—",
     "- 3 cột đầu sắp xếp tăng / giảm được\n"
     "- Kho, Phiếu kiểm kê, Người lập không sắp xếp được"),

    ("003", "Phân trang", "P0",
     "Phạm vi có 23 phiếu",
     "1. Sang trang 3\n"
     "2. Đổi 25 dòng mỗi trang",
     "—",
     "- Trang 3: \"Hiển thị 21 đến 23 của 23\"\n"
     "- 25 dòng: 1 trang đủ 23"),

    ("004", "Phiếu nháp của người khác vẫn hiện", "P1",
     "B quyền tổng công ty; TK1 có 2 phiếu Đang tạo",
     "1. B lọc Trạng thái = Đang tạo",
     "—",
     "- Thấy 2 phiếu của TK1 (khác các màn kiểm kê vốn ẩn nháp người khác) — ghi nhận"),

    ("005", "Bảng trống", "P2",
     "Tài khoản chưa có phiếu, không có quyền xem",
     "1. Mở màn từ menu",
     "—",
     "- Bảng báo không có dữ liệu, không lỗi"),
]
