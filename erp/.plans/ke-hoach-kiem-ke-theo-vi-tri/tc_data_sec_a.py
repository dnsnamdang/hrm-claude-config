# -*- coding: utf-8 -*-
"""Section I, II, III — hien thi trang & loi vao, bo loc, danh sach."""
from tc_data_role import MENU

HOME = ("Ở Trang chủ bấm tab \"Phê duyệt\" > thẻ \"Kiểm kê\" > bấm ô \"Kế hoạch kiểm kê vị trí chờ duyệt\"")

SEC_I = [
    ("001", "Vào màn từ menu Kế toán", "P0",
     "Tài khoản có quyền \"Tổng kiểm kê kho theo vị trí\"",
     "1. " + MENU + "\n"
     "2. Quan sát tiêu đề trang và bảng",
     "—",
     "- Mở màn tiêu đề \"Kế hoạch kiểm kê theo vị trí\"\n"
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

    ("003", "Vào màn từ ô chờ duyệt ở Trang chủ", "P0",
     "Tài khoản TK1 có quyền Lập phiếu kiểm kê kho theo vị trí, là thủ kho K1\n"
     "Kho K1 có 2 kế hoạch Đang kiểm, 1 Đã lập kiểm kê, 1 Hoàn thành",
     "1. Đăng nhập TK1\n"
     "2. " + HOME + "\n"
     "3. So số trên ô với số tổng dưới bảng",
     "—",
     "- Ô hiện số 2, danh sách mở ra có tổng 2\n"
     "- Cả 2 dòng đều Đang kiểm, Kho là K1\n"
     "- Kế hoạch Đã lập kiểm kê / Hoàn thành KHÔNG hiện"),

    ("004", "Ô chờ duyệt ở Trang chủ ẩn khi không còn kế hoạch chờ", "P1",
     "TK1 là thủ kho K1; kho K1 không còn kế hoạch Đang kiểm nào",
     "1. Đăng nhập TK1, mở tab \"Phê duyệt\" ở Trang chủ\n"
     "2. Tìm ô \"Kế hoạch kiểm kê vị trí chờ duyệt\"",
     "—",
     "- Ô KHÔNG hiển thị\n"
     "- Số trong ngoặc ở tiêu đề thẻ \"Kiểm kê\" không đếm ô này"),

    ("005", "Lối vào Kế hoạch của tôi chỉ hiện kế hoạch mình lập", "P1",
     "Tài khoản C có quyền \"Tổng kiểm kê kho theo vị trí\"; công ty có 15 kế hoạch, C lập 4 (1 Đang tạo)",
     "1. Mở màn từ menu, ghi số tổng\n"
     "2. Trên thanh địa chỉ xóa phần tham số phía sau dấu hỏi, nhấn Enter\n"
     "3. Đọc số tổng, soát cột Người lập",
     "—",
     "- Bước 1: tổng theo phạm vi công ty\n"
     "- Bước 3: tổng = 4, mọi dòng Người lập là C, gồm cả kế hoạch Đang tạo\n"
     "- Khối lọc KHÔNG có ô Phòng ban"),

    ("006", "Sửa tay tham số trên thanh địa chỉ thành giá trị lạ", "P1",
     "Tài khoản C như TC_01.005",
     "1. Mở màn từ menu\n"
     "2. Trên thanh địa chỉ đổi giá trị sau dấu bằng thành chữ bất kỳ, ví dụ abc, nhấn Enter",
     "Tham số: abc",
     "- Trang mở bình thường, không báo lỗi\n"
     "- Chỉ hiện kế hoạch C tự lập (như lối vào Kế hoạch của tôi)\n"
     "- KHÔNG lộ thêm kế hoạch của người khác"),

    ("007", "Tài khoản thiếu quyền Lập phiếu mở lối vào chờ duyệt", "P1",
     "NV-A không có quyền Lập phiếu kiểm kê kho theo vị trí, đã lập 3 kế hoạch\n"
     "NV-A nhận được đường dẫn danh sách chờ duyệt từ thủ kho",
     "1. Đăng nhập NV-A\n"
     "2. Dán đường dẫn danh sách chờ duyệt vào trình duyệt",
     "—",
     "- Không báo lỗi\n"
     "- Chỉ hiện 3 kế hoạch do NV-A lập, KHÔNG hiện kế hoạch chờ của thủ kho"),

    ("008", "Nút Quay lại luôn về danh sách lối vào menu", "P2",
     "TK1 đang mở danh sách từ ô chờ duyệt ở Trang chủ",
     "1. Bấm Số phiếu của 1 kế hoạch để mở Chi tiết\n"
     "2. Bấm nút Quay lại",
     "—",
     "- Về danh sách theo lối vào menu (phạm vi theo quyền xem), KHÔNG về danh sách chờ duyệt\n"
     "- Lưu ý: đúng code hiện tại, ghi nhận để nghiệp vụ quyết định"),

    ("009", "Hệ thống ghi nhớ bộ lọc riêng cho từng lối vào", "P1",
     "TK1 có thể mở cả 2 lối vào menu và chờ duyệt",
     "1. Mở lối vào menu, lọc Trạng thái = Hoàn thành, sang trang 2\n"
     "2. Rời sang màn khác rồi mở lại lối vào menu\n"
     "3. Mở lối vào chờ duyệt từ Trang chủ",
     "Trạng thái: Hoàn thành",
     "- Bước 2: vẫn giữ Trạng thái = Hoàn thành và đang ở trang 2\n"
     "- Bước 3: bộ lọc trống, KHÔNG mang theo điều kiện của lối vào menu"),

    ("010", "Nút làm mới xóa điều kiện nhưng giữ phạm vi", "P1",
     "TK1 mở lối vào chờ duyệt, đang lọc Mã phiếu = 0012",
     "1. Bấm Bộ lọc\n"
     "2. Bấm nút màu xanh lá có biểu tượng mũi tên vòng (làm mới)",
     "Mã phiếu: 0012",
     "- Ô Mã phiếu trống\n"
     "- Danh sách vẫn là các kế hoạch chờ duyệt của TK1, không nhảy sang phạm vi khác"),

    ("011", "Nhãn trạng thái hiển thị đúng màu", "P0",
     "Có kế hoạch ở đủ 4 trạng thái",
     "1. Bấm Bộ lọc, mở ô Trạng thái, đếm lựa chọn\n"
     "2. Lọc lần lượt từng trạng thái, quan sát nhãn",
     "4 trạng thái",
     "- Ô Trạng thái có đúng 4 lựa chọn theo thứ tự: Đang kiểm, Đang tạo, Đã lập kiểm kê, Hoàn thành\n"
     "- Đang tạo: nhãn ĐỎ; Đang kiểm: nhãn VÀNG\n"
     "- Đã lập kiểm kê và Hoàn thành: nhãn XANH"),

    ("012", "Định dạng các cột trên lưới", "P1",
     "Kế hoạch KH-5 lập ngày 05/10/2026 cho kho \"Kho Hà Nội\" do NV-A lập",
     "1. Tìm KH-5\n"
     "2. Đọc từng cột\n"
     "3. Bấm vào Số phiếu",
     "—",
     "- Số phiếu dạng <mã công ty>-KHKKVT-<5 chữ số>, là liên kết\n"
     "- Ngày kiểm kê: 05/10/2026\n"
     "- Kho: Kho Hà Nội (tên kho)\n"
     "- Người lập: họ tên NV-A\n"
     "- Bấm Số phiếu mở màn Chi tiết của KH-5"),

    ("013", "Menu bánh răng thay đổi theo trạng thái", "P0",
     "NV-A là người lập, có quyền Lập phiếu và là thủ kho K1\n"
     "NV-A có 4 kế hoạch kho K1 ở 4 trạng thái",
     "1. Bấm bánh răng ở từng kế hoạch\n"
     "2. Ghi lại các mục",
     "—",
     "- Đang tạo: Sửa, Xóa, In, Xuất excel\n"
     "- Đang kiểm: Lập phiếu kiểm kê theo vị trí, In, Xuất excel\n"
     "- Đã lập kiểm kê, Hoàn thành: chỉ In, Xuất excel"),

    ("014", "Màn Chi tiết chỉ xem, không sửa được", "P0",
     "Kế hoạch KH-3 Đang kiểm có 3 vị trí, 2 thành viên",
     "1. Bấm Số phiếu KH-3\n"
     "2. Thử bấm vào các ô, ô tích\n"
     "3. Mở tab \"Hội đồng kiểm kê\"",
     "—",
     "- Tiêu đề trang: \"Kế hoạch kiểm kê theo vị trí: <Số phiếu>\"\n"
     "- Ô Kho vật lý và mọi ô tích bị khóa; không có ô tìm kiếm, không có \"Chọn hết\" ở đầu khung\n"
     "- Không có nút \"Lấy vị trí\", không có nút thêm / bớt thành viên\n"
     "- Chỉ có nút Quay lại\n"
     "- Tab Vị trí hiện đúng 3 vị trí, tab Hội đồng kiểm kê hiện 2 thành viên"),
]


SEC_II = [
    ("001", "Lọc theo Mã phiếu khớp một phần", "P0",
     "Có kế hoạch TPE-KHKKVT-00125 và TPE-KHKKVT-00126",
     "1. Bấm Bộ lọc\n"
     "2. Gõ 0012 vào ô \"Mã phiếu\"\n"
     "3. Chờ bảng tự tải lại",
     "Mã phiếu: 0012",
     "- Bảng tự tải lại sau khoảng nửa giây, không cần bấm nút tìm\n"
     "- Hiện cả 00125 và 00126"),

    ("002", "Lọc theo Trạng thái", "P0",
     "Có 3 kế hoạch Đang kiểm, 2 Hoàn thành trong phạm vi",
     "1. Bấm Bộ lọc, chọn Trạng thái = Đang kiểm\n"
     "2. Đổi sang Hoàn thành",
     "Trạng thái: Đang kiểm / Hoàn thành",
     "- Đang kiểm: đúng 3 dòng\n"
     "- Hoàn thành: đúng 2 dòng"),

    ("003", "Lọc theo Người tạo, tìm được cả nhân viên đã nghỉ", "P1",
     "NV-Q đã nghỉ việc, trước đó lập 2 kế hoạch đã gửi",
     "1. Bấm Bộ lọc, bấm ô \"Người tạo\"\n"
     "2. Gõ tên NV-Q, chọn kết quả",
     "Người tạo: NV-Q",
     "- Ô gợi ý tìm thấy NV-Q dù đã nghỉ\n"
     "- Bảng hiện đúng 2 kế hoạch của NV-Q"),

    ("004", "Lọc theo mã hàng hóa", "P0",
     "KH-5 có hàng mã HH-0091 ở 1 vị trí; KH-6 không có hàng này",
     "1. Bấm Bộ lọc, gõ HH-0091 vào ô \"Nhập tên hoặc mã hàng hóa\"",
     "Hàng hóa: HH-0091",
     "- Hiện KH-5, không hiện KH-6"),

    ("005", "Lọc theo một phần tên hàng hóa", "P1",
     "KH-5 có hàng \"Máy bơm ly tâm 2HP\"",
     "1. Gõ \"ly tâm\" vào ô \"Nhập tên hoặc mã hàng hóa\"",
     "Hàng hóa: ly tâm",
     "- Hiện KH-5 và mọi kế hoạch có hàng chứa cụm \"ly tâm\" trong tên"),

    ("006", "Lọc Từ ngày", "P1",
     "Kế hoạch lập các ngày 01/10, 05/10, 10/10/2026",
     "1. Bấm Bộ lọc, chọn Từ ngày = 05/10/2026",
     "Từ ngày: 05/10/2026",
     "- Hiện kế hoạch ngày 05/10 và 10/10, không hiện ngày 01/10"),

    ("007", "Đến ngày được tính trọn ngày", "P0",
     "Kế hoạch KH-7 lập lúc 23:50 ngày 05/10/2026",
     "1. Chọn Từ ngày = 05/10/2026, Đến ngày = 05/10/2026",
     "Từ ngày: 05/10/2026\n"
     "Đến ngày: 05/10/2026",
     "- KH-7 CÓ trong kết quả\n"
     "- Không có kế hoạch ngày 04/10 hay 06/10"),

    ("008", "Từ ngày lớn hơn Đến ngày", "P2",
     "—",
     "1. Chọn Từ ngày = 10/10/2026, Đến ngày = 01/10/2026",
     "Từ ngày: 10/10/2026\n"
     "Đến ngày: 01/10/2026",
     "- Bảng trống, không báo lỗi, không treo trang"),

    ("009", "Lọc theo Kho", "P0",
     "Có 4 kế hoạch kho K1, 3 kế hoạch kho K2",
     "1. Bấm Bộ lọc, chọn ô \"Kho\" = K1",
     "Kho: K1",
     "- Hiện đúng 4 dòng, cột Kho đều là K1"),

    ("010", "Ô lọc Nhà kho / Dãy / Khoang / Vị trí lọc dây chuyền theo cấp trên", "P1",
     "Kho K1 có nhà N1, N2; nhà N1 có dãy D1, D2",
     "1. Chọn Kho = K1, mở ô Nhà\n"
     "2. Chọn Nhà = N1, mở ô Dãy\n"
     "3. Bỏ chọn Kho",
     "Kho: K1\n"
     "Nhà: N1",
     "- Bước 1: ô Nhà chỉ còn N1, N2\n"
     "- Bước 2: ô Dãy chỉ còn D1, D2\n"
     "- Bước 3: ô Nhà trở về rỗng, không còn lựa chọn"),

    ("011", "Lọc Vị trí theo phạm vi đã tích, kể cả vị trí không có tồn", "P1",
     "Kế hoạch KH-8 đã tích vị trí P5 lúc lập; P5 không có tồn nên không có trong bảng chi tiết",
     "1. Chọn Kho, Nhà, Dãy, Khoang chứa P5, rồi chọn Vị trí = P5\n"
     "2. Mở chi tiết KH-8",
     "Vị trí: P5",
     "- KH-8 CÓ trong kết quả lọc\n"
     "- Tab Vị trí của KH-8 không có P5\n"
     "- Lưu ý: lọc theo phạm vi tích lúc lập, không phải theo bảng chi tiết"),

    ("012", "Ô lọc Kho liệt kê kho của mọi công ty", "P2",
     "Tài khoản thuộc công ty 3; hệ thống có kho của công ty 1 và công ty 3, có 1 kho ngừng hoạt động",
     "1. Bấm Bộ lọc, mở ô Kho",
     "—",
     "- Danh sách gồm kho của cả 2 công ty và kho ngừng hoạt động\n"
     "- Lưu ý: ghi nhận để nghiệp vụ quyết định có cần giới hạn"),

    ("013", "Ô lọc Công ty và Phòng ban", "P0",
     "Tài khoản B có quyền tổng công ty; công ty 1 có 10 kế hoạch, công ty 3 có 4 kế hoạch",
     "1. Mở màn từ menu, bấm Bộ lọc\n"
     "2. Chọn Công ty = công ty 3\n"
     "3. Chọn thêm một Phòng ban của công ty 3",
     "Công ty: công ty 3",
     "- Mong đợi: chỉ còn 4 kế hoạch của công ty 3, rồi thu hẹp theo phòng ban\n"
     "- Lưu ý: code hiện tại KHÔNG áp hai ô này vào kết quả, tổng vẫn là 14 — nếu vậy ghi Failed"),

    ("014", "Kết hợp nhiều điều kiện lọc", "P1",
     "Kho K1 có 4 kế hoạch, trong đó 2 Đang kiểm, 1 trong số đó có hàng HH-0091",
     "1. Chọn Kho = K1, Trạng thái = Đang kiểm\n"
     "2. Gõ HH-0091 vào ô hàng hóa",
     "Kho: K1\n"
     "Trạng thái: Đang kiểm\n"
     "Hàng hóa: HH-0091",
     "- Bước 1: 2 dòng\n"
     "- Bước 2: 1 dòng — các điều kiện cùng lúc thỏa"),

    ("015", "Bộ lọc trong lối vào chờ duyệt vẫn giữ phạm vi chờ duyệt", "P1",
     "TK1 có 2 kế hoạch chờ ở kho K1",
     "1. Mở lối vào chờ duyệt từ Trang chủ\n"
     "2. Lọc Trạng thái = Hoàn thành",
     "Trạng thái: Hoàn thành",
     "- Bảng trống (lối vào chờ duyệt chỉ có Đang kiểm)\n"
     "- Không lộ kế hoạch Hoàn thành ngoài phạm vi"),

    ("016", "Nhập ký tự đặc biệt vào ô tìm", "P2",
     "—",
     "1. Gõ lần lượt %, _ và ' vào ô Mã phiếu\n"
     "2. Gõ \"<b>\" vào ô hàng hóa",
     "Mã phiếu: %, _, '\n"
     "Hàng hóa: <b>",
     "- Không báo lỗi, không treo trang\n"
     "- Kết quả hợp lý (trống hoặc khớp đúng ký tự)"),
]


SEC_III = [
    ("001", "Sắp xếp mặc định mới nhất lên đầu", "P0",
     "Có kế hoạch lập 01/10, 05/10, 10/10/2026",
     "1. Mở màn từ menu, không lọc gì",
     "—",
     "- Thứ tự: 10/10, 05/10, 01/10"),

    ("002", "Sắp xếp theo cột Số phiếu", "P1",
     "Có ít nhất 3 kế hoạch",
     "1. Bấm tiêu đề cột Số phiếu\n"
     "2. Bấm lần nữa\n"
     "3. Thử bấm tiêu đề các cột khác",
     "—",
     "- Lần 1 tăng dần, lần 2 giảm dần theo Số phiếu\n"
     "- Các cột STT, Ngày kiểm kê, Kho, Trạng thái, Người lập, Hành động KHÔNG sắp xếp được"),

    ("003", "Phân trang và đổi số dòng mỗi trang", "P0",
     "Phạm vi có 23 kế hoạch",
     "1. Đọc thông tin dưới bảng\n"
     "2. Sang trang 3\n"
     "3. Đổi số dòng mỗi trang sang 25",
     "—",
     "- Trang 1: \"Hiển thị 1 đến 10 của 23\"\n"
     "- Trang 3: 3 dòng, \"Hiển thị 21 đến 23 của 23\"\n"
     "- 25 dòng: 1 trang, đủ 23 dòng"),

    ("004", "STT đánh liên tục qua các trang", "P2",
     "Phạm vi có 23 kế hoạch",
     "1. Sang trang 2, đọc cột STT",
     "—",
     "- STT chạy từ 11 đến 20"),

    ("005", "Ẩn kế hoạch nháp của người khác", "P0",
     "NV-B (quyền tổng công ty) có 1 kế hoạch Đang tạo của mình; NV-A có 2 kế hoạch Đang tạo",
     "1. NV-B mở màn từ menu, lọc Trạng thái = Đang tạo",
     "Trạng thái: Đang tạo",
     "- Chỉ 1 dòng của NV-B\n"
     "- 2 kế hoạch nháp của NV-A không hiện"),

    ("006", "Bảng trống khi không có dữ liệu", "P2",
     "Tài khoản mới chưa lập kế hoạch nào, không có quyền xem",
     "1. Mở màn từ menu",
     "—",
     "- Bảng báo không có dữ liệu, thông tin dưới bảng tổng = 0, không lỗi"),

    ("007", "Tổng trên lưới khớp số trên ô Trang chủ", "P1",
     "TK1 là thủ kho K1 và K2; K1 có 2, K2 có 1 kế hoạch Đang kiểm",
     "1. Đọc số ở ô \"Kế hoạch kiểm kê vị trí chờ duyệt\"\n"
     "2. Bấm vào ô, đọc tổng dưới bảng",
     "—",
     "- Cả hai đều là 3"),
]
