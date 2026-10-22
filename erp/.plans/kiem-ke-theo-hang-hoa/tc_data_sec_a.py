# -*- coding: utf-8 -*-
"""Section I, II, III - hien thi & loi vao, bo loc, danh sach."""
from tc_data_role import MENU, HOME

SEC_I = [
    ("001", "Vào màn từ menu Kho", "P0",
     "Tài khoản có quyền \"Xem phiếu kiểm kê hàng hóa - theo công ty\"",
     "1. " + MENU + "\n"
     "2. Quan sát tiêu đề và bảng",
     "—",
     "- Tiêu đề trang \"Kiểm kê hàng hóa\"\n"
     "- Bảng tải dữ liệu, không báo lỗi"),

    ("002", "Bố cục mặc định của màn danh sách", "P0",
     "Có ít nhất 12 phiếu nhìn thấy được",
     "1. Mở màn từ menu\n"
     "2. Quan sát từ trên xuống",
     "—",
     "- Hàng nút: Bộ lọc, Tạo mới, In, Xuất excel\n"
     "- Bảng có cột: STT, Số phiếu, Ngày kiểm kê, Kho, Trạng thái, Người lập, Người duyệt, Ngày duyệt, "
     "Hành động\n"
     "- 10 dòng mỗi trang, phiếu mới lập nhất lên đầu"),

    ("003", "Vào màn từ ô chờ duyệt ở Trang chủ", "P0",
     "BKS có quyền Ban kiểm soát, thuộc công ty 1; công ty 1 có 2 phiếu Chờ KT duyệt, 1 phiếu Chờ xử lý",
     "1. Đăng nhập BKS\n"
     "2. " + HOME + "\n"
     "3. So số trên ô với số tổng dưới bảng",
     "—",
     "- Ô hiện 2, danh sách có 2 phiếu, đều Chờ KT duyệt\n"
     "- Phiếu Chờ xử lý không hiện"),

    ("004", "Ô chờ duyệt đếm công ty mình nhưng danh sách gồm mọi công ty", "P1",
     "BKS thuộc công ty 1; công ty 1 có 2 phiếu Chờ KT duyệt, công ty 3 có 3 phiếu Chờ KT duyệt",
     "1. Đăng nhập BKS, đọc số ở ô \"Kiểm kê hàng hóa chờ duyệt\"\n"
     "2. Bấm vào ô, đọc số tổng",
     "—",
     "- Ô hiện 2\n"
     "- Mong đợi: danh sách có 2 phiếu\n"
     "- Lưu ý: theo code hiện tại danh sách có 5 phiếu (gồm công ty 3) - ghi Failed"),

    ("005", "Ô chờ duyệt ẩn khi không còn phiếu chờ", "P2",
     "Công ty của BKS không còn phiếu Chờ KT duyệt",
     "1. Đăng nhập BKS, mở tab Phê duyệt ở Trang chủ",
     "—",
     "- Không có ô \"Kiểm kê hàng hóa chờ duyệt\""),

    ("006", "Nhãn trạng thái hiển thị đúng màu", "P1",
     "Có phiếu ở các trạng thái Đang kiểm, Chờ KT duyệt, Chờ xử lý, Hoàn thành",
     "1. Mở màn từ menu, quan sát cột Trạng thái",
     "—",
     "- Hoàn thành: nhãn xanh\n"
     "- Các trạng thái còn lại: nhãn đỏ"),

    ("007", "Bấm Số phiếu mở màn Chi tiết", "P0",
     "Có phiếu KK-2 Đang kiểm do người khác lập",
     "1. Bấm Số phiếu KK-2",
     "—",
     "- Mở màn Chi tiết, mọi ô bị khóa\n"
     "- Cuối trang chỉ có nút Quay lại"),

    ("008", "Bấm Tạo mới mở form phiếu kiểm kê", "P0",
     "—",
     "1. Bấm Tạo mới",
     "—",
     "- Ô Kế hoạch kiểm kê hiện \"-\", Ngày kiểm kê = hôm nay (khóa)\n"
     "- Bảng hàng hóa trống; KHÔNG có cột Thực kiểm, Chênh lệch, Ghi chú dòng; KHÔNG có tab Hàng thừa khác\n"
     "- Nút cuối trang: Lưu, Lưu & gửi, Hủy"),
]


SEC_II = [
    ("001", "Khối tìm kiếm đủ các ô lọc", "P0",
     "Tài khoản có quyền xem theo công ty",
     "1. Bấm Bộ lọc",
     "—",
     "- Có ô: Mã phiếu, Kho, Trạng thái (7 lựa chọn), Người tạo, Người duyệt, Nhập mã hàng hóa, Nhập tên "
     "hàng hóa, Từ ngày, Đến ngày, Phòng ban"),

    ("002", "Lọc theo Mã phiếu tìm gần đúng", "P0",
     "Có phiếu TPE.KKK-00042 và TPE.KKK-00043",
     "1. Nhập \"00042\" vào ô Mã phiếu",
     "Mã phiếu: 00042",
     "- Chỉ hiện TPE.KKK-00042"),

    ("003", "Lọc theo Kho", "P0",
     "KK-5 kiểm kho K1, KK-6 kiểm kho K2",
     "1. Chọn Kho \"K1\"",
     "Kho: K1",
     "- Hiện KK-5, không hiện KK-6"),

    ("004", "Lọc theo Trạng thái", "P0",
     "Có 3 phiếu Chờ xử lý, 2 phiếu Hoàn thành",
     "1. Chọn Trạng thái \"Chờ xử lý\"",
     "Trạng thái: Chờ xử lý",
     "- Hiện đúng 3 phiếu Chờ xử lý"),

    ("005", "Lọc theo Người tạo và Người duyệt", "P1",
     "NV-A lập 2 phiếu, trong đó 1 phiếu do BKS duyệt",
     "1. Chọn Người tạo NV-A\n"
     "2. Chọn thêm Người duyệt BKS",
     "—",
     "- Bước 1: 2 phiếu\n"
     "- Bước 2: 1 phiếu, cột Người duyệt là BKS"),

    ("006", "Lọc theo Mã hàng và Tên hàng", "P0",
     "KK-5 có hàng mã \"CN-2900\" tên \"Máy in Canon LBP 2900\"; KK-6 không có",
     "1. Nhập \"CN-2900\" vào ô Nhập mã hàng hóa\n"
     "2. Xóa ô mã, nhập \"canon lbp\" vào ô Nhập tên hàng hóa",
     "—",
     "- Cả hai lần chỉ hiện KK-5"),

    ("007", "Lọc theo khoảng ngày tính trọn hai đầu", "P0",
     "Có phiếu lập 01/10 08:00, 05/10 23:59, 06/10 09:00",
     "1. Chọn Từ ngày 01/10, Đến ngày 05/10",
     "Từ ngày: 01/10\n"
     "Đến ngày: 05/10",
     "- Hiện phiếu 01/10 và 05/10, không hiện 06/10"),

    ("008", "Lọc theo Công ty / Phòng ban", "P1",
     "Tài khoản quyền xem theo tổng công ty",
     "1. Chọn Công ty \"công ty 3\", rồi chọn 1 Phòng ban",
     "—",
     "- Mong đợi: chỉ hiện phiếu của công ty / phòng ban đã chọn\n"
     "- Lưu ý: theo code hiện tại số tổng không đổi - ghi Failed nếu nghiệp vụ yêu cầu lọc được"),

    ("009", "Kết hợp nhiều ô lọc", "P1",
     "—",
     "1. Chọn Trạng thái Chờ KT duyệt, Kho K1, nhập tên hàng \"canon\"",
     "—",
     "- Chỉ hiện phiếu thỏa cả 3 điều kiện"),

    ("010", "Ô lọc không mở rộng phạm vi quyền", "P0",
     "NV-A không có quyền xem; NV-B công ty khác lập TPE.KKK-00099",
     "1. Đăng nhập NV-A, nhập Mã phiếu \"00099\"",
     "—",
     "- Không tìm thấy"),

    ("011", "Xóa bộ lọc", "P2",
     "Đang lọc Trạng thái Chờ xử lý",
     "1. Bấm nút xóa bộ lọc",
     "—",
     "- Các ô trở về trống, số tổng như lúc mới vào"),

    ("012", "Không có kết quả", "P2",
     "—",
     "1. Nhập Mã phiếu \"KHONGTONTAI\"",
     "—",
     "- Bảng báo không có dữ liệu, tổng = 0"),
]


SEC_III = [
    ("001", "Phân trang và STT liên tục", "P1",
     "Có 25 phiếu",
     "1. Chuyển sang trang 3",
     "—",
     "- STT từ 21 đến 25, dòng dưới bảng \"Hiển thị 21 đến 25 của 25\""),

    ("002", "Sắp xếp theo Số phiếu", "P2",
     "Có ít nhất 5 phiếu",
     "1. Bấm tiêu đề cột Số phiếu 2 lần",
     "—",
     "- Lần 1 tăng dần, lần 2 giảm dần\n"
     "- Các cột khác không sắp xếp được"),

    ("003", "Menu bánh răng theo trạng thái", "P0",
     "Người xem là người lập, có đủ quyền Ban kiểm soát và Xử lý\n"
     "Có KK-1 Đang tạo, KK-2 Đang kiểm, KK-3 Chờ KT duyệt, KK-4 Chờ xử lý, KK-7 Không duyệt, KK-8 Hoàn "
     "thành, cùng do người xem lập",
     "1. Bấm bánh răng ở từng phiếu",
     "—",
     "- KK-1: Sửa, Xóa, In, Xuất excel\n"
     "- KK-2, KK-7: Cập nhật kết quả, In, Xuất excel\n"
     "- KK-3: Duyệt, In, Xuất excel\n"
     "- KK-4: Xử lý, In, Xuất excel\n"
     "- KK-8: In, Xuất excel"),

    ("004", "Cột Người duyệt và Ngày duyệt", "P1",
     "KK-4 đã được BKS duyệt hôm nay",
     "1. Tìm KK-4, đọc cột Người duyệt, Ngày duyệt",
     "—",
     "- Người duyệt: BKS\n"
     "- Mong đợi: Ngày duyệt là hôm nay\n"
     "- Lưu ý: theo code hiện tại Ngày duyệt luôn trống - ghi Failed"),

    ("005", "Kế hoạch nhiều kho hiển thị đủ tên kho", "P2",
     "KK-5 kiểm 2 kho K1, K2",
     "1. Đọc cột Kho của KK-5",
     "—",
     "- Hiện \"K1, K2\""),

    ("006", "Lối vào Phiếu của tôi sau khi duyệt", "P2",
     "BKS vừa Duyệt phiếu KK-3 do NV-A lập",
     "1. Quan sát danh sách hệ thống đưa về sau khi Duyệt",
     "—",
     "- Theo code hiện tại: về danh sách \"Phiếu của tôi\" của BKS, KHÔNG thấy KK-3\n"
     "- Lưu ý: ghi Failed nếu nghiệp vụ muốn quay về danh sách chờ duyệt"),
]
