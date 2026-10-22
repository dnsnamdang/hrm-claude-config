# -*- coding: utf-8 -*-
"""Section I, II, III — hien thi trang & loi vao, bo loc, danh sach."""
from tc_data_role import MENU, HOME

SEC_I = [
    ("001", "Vào màn từ menu Kho", "P0",
     "Tài khoản có quyền \"Xem phiếu kiểm kê vị trí - theo công ty\"",
     "1. " + MENU + "\n"
     "2. Quan sát tiêu đề và bảng",
     "—",
     "- Mở màn danh sách phiếu kiểm kê theo vị trí, bảng tải dữ liệu không lỗi\n"
     "- Phạm vi phiếu theo quyền xem"),

    ("002", "Bố cục mặc định của danh sách", "P0",
     "Phạm vi có ít nhất 12 phiếu",
     "1. Mở màn từ menu, quan sát từ trên xuống",
     "—",
     "- Hàng nút: Bộ lọc, Tạo mới, In, Xuất excel; khối tìm kiếm mặc định THU GỌN\n"
     "- Cột: STT, Số phiếu, Ngày kiểm kê, Kho, Trạng thái, Người lập, Người duyệt, Ngày duyệt, Hành động\n"
     "- 10 dòng mỗi trang, Ngày kiểm kê mới nhất lên đầu"),

    ("003", "Vào màn từ ô chờ duyệt ở Trang chủ", "P0",
     "BKS (quyền Ban kiểm soát, công ty 1); công ty 1 có 2 phiếu Chờ duyệt kết quả, 3 phiếu Hoàn thành",
     "1. Đăng nhập BKS\n"
     "2. " + HOME + "\n"
     "3. So số trên ô với tổng dưới bảng",
     "—",
     "- Ô hiện 2, danh sách có 2 phiếu, đều Chờ duyệt kết quả\n"
     "- Phiếu Hoàn thành không hiện"),

    ("004", "Số trên ô Trang chủ và danh sách khi có phiếu chờ của công ty khác", "P1",
     "BKS thuộc công ty 1; công ty 1 có 2, công ty 3 có 1 phiếu Chờ duyệt kết quả",
     "1. Đọc số trên ô \"Kiểm kê vị trí chờ duyệt\"\n"
     "2. Bấm vào ô, đọc tổng",
     "—",
     "- Ô hiện 2 (chỉ công ty 1)\n"
     "- Danh sách hiện 3 (cả công ty 3) và BKS duyệt được cả phiếu công ty 3\n"
     "- Lưu ý: hai con số lệch nhau — ghi Failed nếu nghiệp vụ yêu cầu Ban kiểm soát chỉ duyệt công ty mình"),

    ("005", "Lối vào Phiếu của tôi", "P1",
     "TK1 có quyền xem theo công ty; công ty có 12 phiếu, TK1 lập 4 (1 Đang tạo)",
     "1. Mở màn từ menu, ghi tổng\n"
     "2. Trên thanh địa chỉ xóa phần tham số sau dấu hỏi, nhấn Enter",
     "—",
     "- Bước 2: tổng = 4, đều do TK1 lập, có cả phiếu Đang tạo\n"
     "- Không có ô lọc Phòng ban"),

    ("006", "Sau Lưu kết quả và Hoàn thành hệ thống tự về Phiếu của tôi", "P1",
     "TK1 đang ở màn Chi tiết phiếu Đang kiểm của mình, đã nhập đủ kết quả",
     "1. Bấm \"Lưu kết quả\"\n"
     "2. So danh sách đang hiện với lối vào menu",
     "—",
     "- Về danh sách chỉ có phiếu TK1 lập (khác lối vào menu)\n"
     "- Lưu ý: đúng code hiện tại, ghi nhận để nghiệp vụ quyết định"),

    ("007", "Sửa tay tham số trên thanh địa chỉ thành giá trị lạ", "P1",
     "Tài khoản C có quyền xem theo công ty",
     "1. Mở màn từ menu\n"
     "2. Đổi giá trị sau dấu bằng trên thanh địa chỉ thành abc, nhấn Enter",
     "Tham số: abc",
     "- Không lỗi; chỉ hiện phiếu C tự lập, không lộ thêm dữ liệu"),

    ("008", "Mở lối vào chờ duyệt bằng tài khoản không có quyền Ban kiểm soát", "P1",
     "NV-A không có quyền Ban kiểm soát, lập 2 phiếu; nhận đường dẫn danh sách chờ duyệt",
     "1. NV-A dán đường dẫn vào trình duyệt",
     "—",
     "- Không lỗi, chỉ hiện 2 phiếu của NV-A"),

    ("009", "Bộ lọc ghi nhớ riêng theo lối vào", "P2",
     "BKS mở được cả 2 lối vào",
     "1. Lối vào menu: lọc Trạng thái = Hoàn thành, sang trang 2\n"
     "2. Rời màn, mở lại lối vào menu\n"
     "3. Mở lối vào chờ duyệt",
     "Trạng thái: Hoàn thành",
     "- Bước 2: còn bộ lọc và trang 2\n"
     "- Bước 3: bộ lọc trống"),

    ("010", "Nút làm mới xóa điều kiện nhưng giữ phạm vi", "P2",
     "BKS ở lối vào chờ duyệt, đang lọc Mã phiếu",
     "1. Bấm nút xanh lá có biểu tượng mũi tên vòng",
     "—",
     "- Ô Mã phiếu trống, danh sách vẫn là phiếu chờ duyệt"),

    ("011", "Nhãn 5 trạng thái", "P0",
     "Có phiếu ở đủ 5 trạng thái",
     "1. Mở ô Trạng thái trong Bộ lọc, đếm lựa chọn\n"
     "2. Lọc lần lượt, quan sát nhãn",
     "—",
     "- Đúng 5 lựa chọn: Đang tạo, Đang kiểm, Chờ duyệt kết quả, Chờ xử lý, Hoàn thành\n"
     "- Đang tạo ĐỎ; Đang kiểm, Chờ duyệt kết quả, Chờ xử lý VÀNG; Hoàn thành XANH"),

    ("012", "Menu bánh răng theo trạng thái và vai trò", "P0",
     "TK1 (người lập, quyền Lập phiếu, có cả quyền Ban kiểm soát và Xử lý) có 5 phiếu ở 5 trạng thái",
     "1. Bấm bánh răng từng phiếu",
     "—",
     "- Đang tạo: Sửa, Xóa, In, Xuất excel\n"
     "- Đang kiểm: Nhập kết quả, In, Xuất excel\n"
     "- Chờ duyệt kết quả: Duyệt kết quả, In, Xuất excel\n"
     "- Chờ xử lý: Xử lý, In, Xuất excel\n"
     "- Hoàn thành: In, Xuất excel"),

    ("013", "Bố cục màn Chi tiết", "P0",
     "KK-5 Hoàn thành, lập từ kế hoạch KH-3, có 2 file đính kèm, ghi chú duyệt \"Đã đối chiếu\"",
     "1. Bấm Số phiếu KK-5\n"
     "2. Bấm vào mã kế hoạch ở ô \"Kế hoạch kiểm kê\"",
     "—",
     "- Tiêu đề trang: \"Kiểm kê kho theo vị trí: <Số phiếu>\"\n"
     "- Ô Kế hoạch kiểm kê hiện mã KH-3, 2 nút X và kính lúp bị khóa; bấm mã mở Chi tiết KH-3 ở tab mới\n"
     "- Khối File đính kèm hiện 2 file, bấm vào mở được file\n"
     "- Bảng có thêm 4 cột Thực kiểm, Chênh lệch, Ghi chú, Tổng kiểm kê ở dạng chỉ xem\n"
     "- Khối \"Ghi chú duyệt\" hiện \"Đã đối chiếu\", bị khóa; cuối trang chỉ có Quay lại"),

    ("014", "Màn Chi tiết vẫn hiện nút thêm / bớt thành viên", "P2",
     "KK-5 Hoàn thành có 2 thành viên",
     "1. Mở Chi tiết KK-5, tab Hội đồng kiểm kê\n"
     "2. Bấm dấu +, chọn 1 người; tải lại trang",
     "—",
     "- Mong đợi: màn Chi tiết không có nút thêm / bớt thành viên\n"
     "- Lưu ý: hiện nút vẫn có, thao tác được nhưng tải lại thì mất — ghi nhận"),

    ("015", "Cột Người duyệt và Ngày duyệt", "P1",
     "KK-1 Chờ duyệt kết quả; BKS duyệt KK-1 ngày 15/10/2026; KK-6 bị Không duyệt",
     "1. Trước khi duyệt đọc 2 cột của KK-1\n"
     "2. Sau khi duyệt đọc lại\n"
     "3. Đọc 2 cột của KK-6",
     "—",
     "- Trước duyệt: trống\n"
     "- Sau duyệt: Người duyệt = họ tên BKS, Ngày duyệt = 15/10/2026\n"
     "- KK-6 (Không duyệt): 2 cột trống"),
]


SEC_II = [
    ("001", "Lọc Mã phiếu khớp một phần", "P0",
     "Có TPE-KKVT-00041 và TPE-KKVT-00042",
     "1. Bấm Bộ lọc, gõ 0004 vào ô Mã phiếu",
     "Mã phiếu: 0004",
     "- Bảng tự tải lại sau khoảng nửa giây, hiện cả 2 phiếu"),

    ("002", "Lọc Trạng thái", "P0",
     "Có 2 phiếu Chờ xử lý, 4 phiếu Hoàn thành",
     "1. Chọn Trạng thái = Chờ xử lý, rồi Hoàn thành",
     "Trạng thái: Chờ xử lý / Hoàn thành",
     "- Lần lượt 2 và 4 dòng"),

    ("003", "Lọc Người tạo", "P1",
     "TK1 lập 4 phiếu đã gửi",
     "1. Bấm ô Người tạo, gõ tìm TK1, chọn",
     "Người tạo: TK1",
     "- 4 dòng, Người lập đều là TK1"),

    ("004", "Lọc Người duyệt", "P1",
     "BKS đã duyệt 3 phiếu",
     "1. Bấm ô Người duyệt, gõ tìm BKS, chọn",
     "Người duyệt: BKS",
     "- 3 dòng, cột Người duyệt đều là BKS"),

    ("005", "Lọc theo mã hoặc tên hàng hóa", "P0",
     "KK-5 có hàng HH-0091 \"Máy bơm ly tâm 2HP\"; KK-6 không có",
     "1. Gõ HH-0091 vào ô \"Nhập tên hoặc mã hàng hóa\"\n"
     "2. Đổi thành \"ly tâm\"",
     "Hàng hóa: HH-0091 / ly tâm",
     "- Cả hai lần đều có KK-5, không có KK-6"),

    ("006", "Lọc ngày theo Ngày kiểm kê của kế hoạch gốc", "P0",
     "Kế hoạch KH-3 lập 01/10/2026; phiếu KK-7 lập từ KH-3 vào ngày 05/10/2026",
     "1. Chọn Từ ngày = Đến ngày = 05/10/2026\n"
     "2. Đổi thành 01/10/2026",
     "Từ ngày, Đến ngày: 05/10/2026 rồi 01/10/2026",
     "- Bước 1: KHÔNG có KK-7\n"
     "- Bước 2: CÓ KK-7, cột Ngày kiểm kê = 01/10/2026\n"
     "- Lưu ý: đúng code hiện tại (Ngày kiểm kê lấy theo kế hoạch)"),

    ("007", "Đến ngày tính trọn ngày", "P1",
     "Phiếu lập độc lập KK-8 lúc 23:50 ngày 10/10/2026",
     "1. Chọn Từ ngày = Đến ngày = 10/10/2026",
     "—",
     "- Có KK-8"),

    ("008", "Lọc Kho và lọc dây chuyền Nhà / Dãy / Khoang / Vị trí", "P1",
     "Kho K1 có nhà N1, N2; K1 có 3 phiếu, K2 có 2 phiếu",
     "1. Chọn Kho = K1\n"
     "2. Mở ô Nhà",
     "Kho: K1",
     "- 3 dòng, cột Kho đều là K1\n"
     "- Ô Nhà chỉ còn N1, N2"),

    ("009", "Ô lọc Công ty và Phòng ban", "P0",
     "B có quyền tổng công ty; công ty 1 có 8, công ty 3 có 3 phiếu",
     "1. Bấm Bộ lọc, chọn Công ty = công ty 3",
     "Công ty: công ty 3",
     "- Mong đợi: còn 3 phiếu\n"
     "- Lưu ý: code hiện tại không áp ô này, tổng vẫn 11 — nếu vậy ghi Failed"),

    ("010", "Kết hợp nhiều điều kiện", "P1",
     "Kho K1 có 3 phiếu, 1 trong đó Chờ xử lý",
     "1. Chọn Kho = K1, Trạng thái = Chờ xử lý",
     "—",
     "- 1 dòng"),

    ("011", "Lọc trong lối vào chờ duyệt không vượt phạm vi", "P1",
     "BKS ở lối vào chờ duyệt",
     "1. Lọc Trạng thái = Hoàn thành",
     "—",
     "- Bảng trống"),

    ("012", "Ký tự đặc biệt trong ô tìm", "P2",
     "—",
     "1. Gõ %, _ , ' vào ô Mã phiếu và ô hàng hóa",
     "—",
     "- Không lỗi, không treo trang"),
]


SEC_III = [
    ("001", "Mặc định Ngày kiểm kê mới nhất lên đầu", "P0",
     "Phiếu có Ngày kiểm kê 01/10, 05/10, 10/10/2026",
     "1. Mở màn từ menu",
     "—",
     "- Thứ tự 10/10, 05/10, 01/10"),

    ("002", "Sắp xếp theo Số phiếu", "P1",
     "Có ít nhất 3 phiếu",
     "1. Bấm tiêu đề cột Số phiếu 2 lần\n"
     "2. Thử bấm các cột khác",
     "—",
     "- Tăng dần rồi giảm dần\n"
     "- Các cột khác không sắp xếp được"),

    ("003", "Phân trang và đổi số dòng", "P0",
     "Phạm vi có 23 phiếu",
     "1. Sang trang 3\n"
     "2. Đổi 25 dòng mỗi trang",
     "—",
     "- Trang 3: \"Hiển thị 21 đến 23 của 23\"\n"
     "- 25 dòng: 1 trang đủ 23 dòng"),

    ("004", "Ẩn phiếu nháp người khác", "P0",
     "B (quyền tổng công ty) có 1 phiếu Đang tạo; TK1 có 2 phiếu Đang tạo",
     "1. B lọc Trạng thái = Đang tạo",
     "—",
     "- Chỉ 1 dòng của B"),

    ("005", "Bảng trống", "P2",
     "Tài khoản chưa có phiếu nào, không có quyền xem",
     "1. Mở màn từ menu",
     "—",
     "- Bảng báo không có dữ liệu, tổng = 0, không lỗi"),
]
