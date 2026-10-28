# -*- coding: utf-8 -*-
"""Section I, II, III - hien thi trang & loi vao, bo loc, danh sach."""
from tc_data_role import MENU

SEC_I = [
    ("001", "Vào màn từ menu Kế toán", "P0",
     "Tài khoản có quyền \"Tổng kiểm kê kho theo hàng hóa\"",
     "1. " + MENU + "\n"
     "2. Quan sát tiêu đề trang và bảng",
     "—",
     "- Mở màn tiêu đề \"Kế hoạch kiểm kê hàng hóa\"\n"
     "- Bảng tải dữ liệu, không báo lỗi\n"
     "- Phạm vi kế hoạch theo quyền xem của người đăng nhập"),

    ("002", "Bố cục mặc định của màn danh sách", "P0",
     "Tài khoản bất kỳ, có ít nhất 12 kế hoạch nhìn thấy được",
     "1. Mở màn từ menu\n"
     "2. Quan sát từ trên xuống",
     "—",
     "- Hàng nút: Bộ lọc, Tạo mới, In, Xuất excel\n"
     "- Khối tìm kiếm mặc định ĐANG THU GỌN\n"
     "- Bảng có các cột: STT, Số phiếu, Ngày kiểm kê, Kho, Trạng thái, Người lập, Hành động\n"
     "- Mặc định 10 dòng mỗi trang, kế hoạch mới lập nhất lên đầu"),

    ("003", "Nhãn trạng thái hiển thị đúng màu", "P1",
     "Có ít nhất 1 kế hoạch mỗi trạng thái Đang tạo (của mình), Đang kiểm, Đã lập phiếu kiểm kê",
     "1. Mở màn từ menu\n"
     "2. Quan sát cột Trạng thái",
     "—",
     "- Đang tạo: nhãn đỏ\n"
     "- Đang kiểm: nhãn đỏ\n"
     "- Đã lập phiếu kiểm kê: nhãn xanh"),

    ("004", "Lối vào Kế hoạch của tôi chỉ hiện kế hoạch mình lập", "P1",
     "NV-A có quyền \"Tổng kiểm kê kho theo hàng hóa\", đã lập 2 kế hoạch\n"
     "Công ty có thêm 5 kế hoạch đã gửi của người khác",
     "1. Đăng nhập NV-A, lập 1 kế hoạch Đang tạo rồi bấm Xóa (hệ thống đưa về lối vào Kế hoạch của tôi); "
     "hoặc bỏ tham số trên thanh địa chỉ của màn danh sách\n"
     "2. Đọc số tổng",
     "—",
     "- Chỉ hiện kế hoạch do NV-A lập, gồm cả nháp\n"
     "- Không hiện 5 kế hoạch của người khác"),

    ("005", "Bấm Số phiếu mở màn Chi tiết", "P0",
     "Có kế hoạch KH-2 Đang kiểm",
     "1. Mở màn từ menu\n"
     "2. Bấm vào Số phiếu của KH-2",
     "—",
     "- Mở màn Chi tiết của KH-2 trong cùng thẻ\n"
     "- Mọi ô bị khóa, không có nút thêm / bớt hàng và thành viên"),

    ("006", "Bấm Tạo mới mở màn lập kế hoạch", "P0",
     "Tài khoản bất kỳ",
     "1. Mở màn từ menu\n"
     "2. Bấm Tạo mới",
     "—",
     "- Mở màn tiêu đề \"Kế hoạch kiểm kê hàng hóa\"\n"
     "- Ô Ngày kiểm kê = hôm nay, bị khóa\n"
     "- Bảng hàng hóa hiện \"Chưa chọn hàng hóa\", tab Hội đồng kiểm kê hiện \"Chưa có thành viên\"\n"
     "- Nút cuối trang: Lưu, Lưu & kiểm, Hủy"),

    ("007", "Kế hoạch có nhiều kho hiển thị đủ tên kho", "P1",
     "Kế hoạch KH-5 chọn 2 kho K1, K2",
     "1. Mở màn từ menu, tìm KH-5\n"
     "2. Đọc cột Kho",
     "—",
     "- Cột Kho hiện \"K1, K2\" (ngăn cách dấu phẩy)"),

    ("008", "Kế hoạch đã gửi không có nút Sửa trên màn Chi tiết", "P1",
     "Kế hoạch KH-2 Đang kiểm do chính mình lập",
     "1. Mở màn Chi tiết KH-2\n"
     "2. Quan sát cuối trang",
     "—",
     "- Chỉ có nút Quay lại\n"
     "- Bấm Quay lại về danh sách lối vào menu"),
]


SEC_II = [
    ("001", "Mở khối tìm kiếm đủ các ô lọc", "P0",
     "Tài khoản có quyền \"Tổng kiểm kê kho theo hàng hóa\"",
     "1. Mở màn từ menu\n"
     "2. Bấm nút Bộ lọc",
     "—",
     "- Hiện các ô: Mã phiếu, Kho, Trạng thái, Người tạo, Nhập mã hàng hóa, Nhập tên hàng hóa, Từ ngày, "
     "Đến ngày, Phòng ban\n"
     "- Ô Trạng thái có 4 lựa chọn: Đang tạo, Đang kiểm, Đã lập phiếu kiểm kê, Hoàn thành"),

    ("002", "Lọc theo Mã phiếu tìm gần đúng", "P0",
     "Có kế hoạch TPE.KHKKHH-00125 và TPE.KHKKHH-00126",
     "1. Bấm Bộ lọc\n"
     "2. Nhập \"00125\" vào ô Mã phiếu",
     "Mã phiếu: 00125",
     "- Chỉ hiện TPE.KHKKHH-00125\n"
     "- Số tổng = 1"),

    ("003", "Lọc theo Trạng thái", "P0",
     "Có 3 kế hoạch Đang kiểm, 2 kế hoạch Đã lập phiếu kiểm kê",
     "1. Bấm Bộ lọc\n"
     "2. Chọn Trạng thái \"Đang kiểm\"",
     "Trạng thái: Đang kiểm",
     "- Hiện đúng 3 kế hoạch, cột Trạng thái đều là Đang kiểm"),

    ("004", "Lọc theo Trạng thái Hoàn thành luôn rỗng", "P2",
     "Đã có phiếu kiểm kê theo hàng hóa lập từ kế hoạch được Hoàn thành",
     "1. Bấm Bộ lọc\n"
     "2. Chọn Trạng thái \"Hoàn thành\"",
     "Trạng thái: Hoàn thành",
     "- Theo code hiện tại: bảng rỗng\n"
     "- Lưu ý: không có thao tác nào đưa kế hoạch lên Hoàn thành - ghi Failed nếu nghiệp vụ yêu cầu"),

    ("005", "Lọc theo Người tạo", "P1",
     "NV-A lập 2 kế hoạch đã gửi, NV-B lập 3 kế hoạch đã gửi; người xem có quyền tổng công ty",
     "1. Bấm Bộ lọc\n"
     "2. Gõ tên NV-A vào ô Người tạo, chọn NV-A",
     "Người tạo: NV-A",
     "- Hiện đúng 2 kế hoạch, cột Người lập đều là NV-A"),

    ("006", "Lọc theo Tên hàng hóa tìm gần đúng", "P0",
     "Kế hoạch KH-5 có hàng \"Máy in Canon LBP 2900\"; KH-6 không có hàng này",
     "1. Bấm Bộ lọc\n"
     "2. Nhập \"canon lbp\" vào ô Nhập tên hàng hóa",
     "Tên hàng: canon lbp",
     "- Hiện KH-5, không hiện KH-6\n"
     "- Tìm không phân biệt chữ hoa / thường"),

    ("007", "Lọc theo Mã hàng hóa", "P0",
     "Kế hoạch KH-5 có hàng mã \"CN-2900\"",
     "1. Bấm Bộ lọc\n"
     "2. Nhập \"CN-2900\" vào ô Nhập mã hàng hóa",
     "Mã hàng: CN-2900",
     "- Mong đợi: chỉ hiện các kế hoạch có hàng CN-2900\n"
     "- Lưu ý: theo code hiện tại bảng báo lỗi, không tải được dữ liệu - ghi Failed"),

    ("008", "Lọc theo Kho", "P0",
     "KH-5 kiểm kho K1, KH-6 kiểm kho K2",
     "1. Bấm Bộ lọc\n"
     "2. Chọn Kho \"K1\"",
     "Kho: K1",
     "- Mong đợi: chỉ hiện KH-5\n"
     "- Lưu ý: theo code hiện tại ô Kho KHÔNG có tác dụng, vẫn hiện cả KH-6 - ghi Failed"),

    ("009", "Lọc theo Công ty và Phòng ban", "P1",
     "Tài khoản quyền tổng công ty; công ty 1 có 10 kế hoạch, công ty 3 có 4 kế hoạch",
     "1. Bấm Bộ lọc\n"
     "2. Chọn Công ty \"công ty 3\"\n"
     "3. Chọn thêm 1 Phòng ban",
     "Công ty: công ty 3",
     "- Mong đợi: chỉ hiện kế hoạch của công ty 3 / phòng ban đã chọn\n"
     "- Lưu ý: theo code hiện tại số tổng KHÔNG đổi - ghi Failed"),

    ("010", "Lọc theo khoảng ngày tính trọn hai đầu", "P0",
     "Có kế hoạch lập 01/10 08:00, 05/10 23:59, 06/10 09:00",
     "1. Bấm Bộ lọc\n"
     "2. Chọn Từ ngày 01/10, Đến ngày 05/10",
     "Từ ngày: 01/10\n"
     "Đến ngày: 05/10",
     "- Hiện kế hoạch 01/10 và 05/10\n"
     "- Không hiện kế hoạch 06/10"),

    ("011", "Chỉ điền Từ ngày", "P2",
     "Có kế hoạch lập trước và sau 10/10",
     "1. Bấm Bộ lọc\n"
     "2. Chỉ chọn Từ ngày 10/10",
     "Từ ngày: 10/10",
     "- Chỉ hiện kế hoạch lập từ 10/10 trở về sau"),

    ("012", "Kết hợp nhiều ô lọc", "P1",
     "Có kế hoạch Đang kiểm chứa hàng Canon do NV-A lập, và kế hoạch Đang kiểm chứa hàng Canon do NV-B lập",
     "1. Bấm Bộ lọc\n"
     "2. Chọn Trạng thái Đang kiểm, Người tạo NV-A, nhập tên hàng \"canon\"",
     "—",
     "- Chỉ hiện kế hoạch thỏa CẢ 3 điều kiện (của NV-A)"),

    ("013", "Không có kết quả khớp", "P2",
     "—",
     "1. Bấm Bộ lọc\n"
     "2. Nhập Mã phiếu \"KHONGTONTAI\"",
     "Mã phiếu: KHONGTONTAI",
     "- Bảng hiện thông báo không có dữ liệu, số tổng = 0"),

    ("014", "Xóa bộ lọc trả về danh sách đầy đủ", "P1",
     "Đang lọc theo Trạng thái Đang kiểm",
     "1. Bấm nút xóa bộ lọc trong khối tìm kiếm",
     "—",
     "- Mọi ô lọc trở về trống\n"
     "- Số tổng trở về như lúc mới vào màn"),

    ("015", "Ô lọc không mở rộng phạm vi quyền", "P0",
     "NV-A không có quyền xem nào; NV-B (công ty khác) lập kế hoạch TPE.KHKKHH-00200",
     "1. Đăng nhập NV-A\n"
     "2. Bấm Bộ lọc, nhập Mã phiếu \"00200\"",
     "Mã phiếu: 00200",
     "- Không tìm thấy kế hoạch của NV-B"),

    ("016", "Hệ thống ghi nhớ bộ lọc khi quay lại màn", "P2",
     "—",
     "1. Lọc Trạng thái Đang kiểm, chuyển sang trang 2\n"
     "2. Mở màn Chi tiết một kế hoạch, bấm Quay lại",
     "—",
     "- Bộ lọc Đang kiểm và trang 2 vẫn được giữ"),
]


SEC_III = [
    ("001", "Phân trang và STT liên tục", "P1",
     "Có 25 kế hoạch nhìn thấy được",
     "1. Mở màn từ menu\n"
     "2. Chuyển sang trang 2, rồi trang 3",
     "—",
     "- Trang 2 STT từ 11 đến 20, trang 3 từ 21 đến 25\n"
     "- Dòng dưới bảng: \"Hiển thị 21 đến 25 của 25\""),

    ("002", "Đổi số dòng mỗi trang", "P2",
     "Có 25 kế hoạch",
     "1. Chọn 25 dòng mỗi trang",
     "—",
     "- Hiện đủ 25 dòng trên 1 trang"),

    ("003", "Sắp xếp theo Số phiếu", "P1",
     "Có ít nhất 5 kế hoạch",
     "1. Bấm tiêu đề cột Số phiếu 1 lần, rồi bấm lần 2",
     "—",
     "- Lần 1 sắp tăng dần, lần 2 giảm dần theo Số phiếu"),

    ("004", "Các cột khác không sắp xếp được", "P2",
     "—",
     "1. Bấm tiêu đề các cột Ngày kiểm kê, Kho, Trạng thái, Người lập",
     "—",
     "- Thứ tự dòng không đổi"),

    ("005", "Cột Ngày kiểm kê là ngày lập kế hoạch", "P1",
     "Kế hoạch KH-1 lập ngày 01/10, sửa và Lưu lại ngày 03/10",
     "1. Mở danh sách, đọc cột Ngày kiểm kê của KH-1\n"
     "2. Mở Chi tiết KH-1, đọc ô Ngày kiểm kê",
     "—",
     "- Danh sách: 01/10\n"
     "- Chi tiết: 03/10\n"
     "- Lưu ý: hai nơi hiện hai ngày khác nhau - ghi Failed nếu nghiệp vụ yêu cầu thống nhất"),

    ("006", "Menu bánh răng theo trạng thái và người xem", "P0",
     "Người xem là người lập, có quyền Lập phiếu kiểm kê kho theo hàng hóa\n"
     "Có KH-1 Đang tạo, KH-2 Đang kiểm, KH-4 Đã lập phiếu kiểm kê, cùng do người xem lập",
     "1. Bấm bánh răng lần lượt ở KH-1, KH-2, KH-4",
     "—",
     "- KH-1: Sửa, Xóa, In, Xuất excel\n"
     "- KH-2: Lập phiếu kiểm kê theo hàng hóa, In, Xuất excel\n"
     "- KH-4: In, Xuất excel"),

    ("007", "Danh sách cập nhật sau khi lưu", "P1",
     "—",
     "1. Tạo kế hoạch mới, bấm Lưu & kiểm\n"
     "2. Quan sát danh sách sau khi hệ thống chuyển về",
     "—",
     "- Kế hoạch mới nằm dòng đầu, trạng thái Đang kiểm, Người lập là mình"),
]
