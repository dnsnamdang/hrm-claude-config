# -*- coding: utf-8 -*-
"""Section VII - XI: duyet & but toan, in / excel, rang buoc, co lap & dong thoi, luong."""
from tc_data_role import KK, MENU

# Bien ban mau da gui duyet
BB2 = ("BB-2 Chờ duyệt của kho K1 (lấy từ KK-10, KK-11):\n"
       "- H1 thừa 3: Giá vốn, % nhân viên 40, NV chịu NV-C (Chi phí nhân viên 120.000, công ty 180.000)\n"
       "- H2 thiếu 2: Giá vốn, % nhân viên 100, NV chịu NV-D (500.000 / 0)\n"
       "- H3 thiếu 1: Giá vốn, % nhân viên 100, NV chịu NV-D (50.000 / 0)")

SEC_VII = [
    ("001", "Màn duyệt: các ô người duyệt sửa được", "P0",
     BB2 + "\nDUYET-1 có quyền duyệt",
     "1. DUYET-1 mở Chi tiết BB-2 từ thông báo\n"
     "2. Thử bấm vào từng ô",
     "—",
     "- Từ ngày, Đến ngày, Kho, Ghi chú, khung Phiếu kiểm kê bị khóa; không có nút Lấy dữ liệu\n"
     "- Giá xử lý, % Chi phí nhân viên, % Chi phí công ty, NV chịu sửa được ở cả 2 tab\n"
     "- Lý do: tab Hàng thừa sửa được, tab Hàng thiếu bị khóa"),

    ("002", "Duyệt không chỉnh sửa", "P0",
     BB2,
     "1. DUYET-1 bấm Duyệt",
     "—",
     "- Báo \"Thao tác thành công!\", về danh sách biên bản của DUYET-1\n"
     "- BB-2: Đã duyệt (nhãn xanh), Người duyệt DUYET-1, Ngày duyệt hôm nay\n"
     "- Menu bánh răng BB-2 chỉ còn In, Xuất Excel"),

    ("003", "Bút toán phần chi phí nhân viên của hàng thừa", "P0",
     BB2,
     "1. DUYET-1 Duyệt BB-2\n"
     "2. Mở sổ chi tiết tài khoản 3381, 3341, lọc theo chứng từ BB-2",
     "—",
     "- Có cặp Nợ 3381 / Có 3341 số tiền 120.000, đối tượng NV-C"),

    ("004", "Bút toán phần chi phí công ty của hàng thừa", "P0",
     BB2,
     "1. DUYET-1 Duyệt BB-2\n"
     "2. Mở sổ chi tiết tài khoản 3381, 711, lọc theo chứng từ BB-2",
     "—",
     "- Mong đợi: Nợ 3381 / Có 711 số tiền 180.000\n"
     "- Lưu ý: theo code hiện tại số tiền là 120.000 (bằng phần nhân viên) - ghi Failed"),

    ("005", "Bút toán hàng thiếu gộp theo NV chịu", "P0",
     BB2,
     "1. DUYET-1 Duyệt BB-2\n"
     "2. Mở sổ chi tiết tài khoản 3341, 1381, lọc theo chứng từ BB-2",
     "—",
     "- Có 1 cặp Nợ 3341 / Có 1381 số tiền 550.000 (500.000 + 50.000), đối tượng NV-D\n"
     "- Không tách thành 2 dòng riêng cho H2, H3"),

    ("006", "Bút toán phần chi phí công ty của hàng thiếu", "P0",
     BB2,
     "1. DUYET-1 Duyệt BB-2\n"
     "2. Mở sổ chi tiết tài khoản 811, 1381, lọc theo chứng từ BB-2",
     "—",
     "- Mong đợi: Nợ 811 / Có 1381 bằng 0 vì công ty không chịu phần nào\n"
     "- Lưu ý: theo code hiện tại ghi Nợ 811 / Có 1381 số tiền 550.000 - ghi Failed"),

    ("007", "Người duyệt sửa % trước khi duyệt", "P0",
     BB2,
     "1. DUYET-1 mở BB-2, đổi % Chi phí nhân viên của H2 thành 50\n"
     "2. Bấm Duyệt, mở lại Chi tiết BB-2 và sổ chi tiết tài khoản 3341",
     "% Chi phí nhân viên H2: 50",
     "- Chi tiết BB-2: H2 % nhân viên 50, Chi phí nhân viên 250.000, Chi phí công ty 250.000\n"
     "- Cặp Nợ 3341 / Có 1381 của NV-D là 300.000"),

    ("008", "Người duyệt đổi NV chịu", "P1",
     BB2,
     "1. DUYET-1 mở BB-2, đổi NV chịu H3 sang NV-E\n"
     "2. Bấm Duyệt, mở sổ chi tiết tài khoản 3341",
     "NV chịu H3: NV-E",
     "- NV-D: Nợ 3341 / Có 1381 số tiền 500.000\n"
     "- NV-E: Nợ 3341 / Có 1381 số tiền 50.000"),

    ("009", "Người duyệt đổi Giá xử lý sang Giá bán", "P1",
     BB2,
     "1. DUYET-1 mở BB-2, đổi Giá xử lý H2 sang Giá bán\n"
     "2. Bấm Duyệt",
     "Giá xử lý H2: Giá bán",
     "- Chi tiết BB-2: H2 Chi phí nhân viên 600.000\n"
     "- Cặp Nợ 3341 / Có 1381 của NV-D là 650.000"),

    ("010", "Duyệt khi người duyệt xóa NV chịu", "P1",
     BB2,
     "1. DUYET-1 xóa NV chịu của H2\n"
     "2. Bấm Duyệt",
     "—",
     "- Báo \"Tạo thất bại!\", có dòng báo lỗi dưới ô NV chịu H2\n"
     "- BB-2 vẫn Chờ duyệt, chưa có bút toán"),

    ("011", "Duyệt khi hệ thống thiếu tài khoản kế toán", "P1",
     BB2 + "\nTài khoản 3381 chưa được khai báo trong danh mục tài khoản",
     "1. DUYET-1 bấm Duyệt BB-2",
     "—",
     "- Báo \"Tài khoản 3381 không có trong hệ thống!\"\n"
     "- BB-2 vẫn Chờ duyệt, không có bút toán nào"),

    ("012", "Duyệt lần hai", "P0",
     "BB-2 vừa được DUYET-1 duyệt",
     "1. DUYET-1 mở lại Chi tiết BB-2\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Duyệt BB-2",
     "—",
     "- Bước 1: không còn nút Duyệt\n"
     "- Bước 2: báo \"Không có quyền\"\n"
     "- Bút toán của BB-2 không bị ghi thêm"),

    ("013", "Duyệt không làm thay đổi tồn kho", "P0",
     BB2 + "\nGhi lại tồn H1, H2, H3 ở kho K1 trước khi duyệt",
     "1. DUYET-1 Duyệt BB-2\n"
     "2. Tra cứu tồn kho H1, H2, H3 ở kho K1",
     "—",
     "- Tồn kho không đổi (số lượng đã được điều chỉnh từ các phiếu nhập / xuất điều chỉnh)"),

    ("014", "Biên bản chỉ có hàng thiếu", "P1",
     "BB-4 Chờ duyệt chỉ có H2 thiếu 2, 100% NV-D",
     "1. DUYET-1 Duyệt BB-4\n"
     "2. Mở sổ chi tiết tài khoản 3381, 711",
     "—",
     "- Duyệt thành công\n"
     "- Không có bút toán 3381, 711 nào có số tiền khác 0 cho BB-4"),

    ("015", "Không có chức năng Không duyệt", "P1",
     BB2 + "\nDUYET-1 thấy Lý do H2 sai",
     "1. DUYET-1 mở Chi tiết BB-2, tìm nút trả lại cho người lập",
     "—",
     "- Theo code hiện tại: chỉ có Duyệt và Quay lại, Lý do hàng thiếu bị khóa\n"
     "- Lưu ý: biên bản sai không trả lại được, người lập cũng không sửa được - ghi Failed nếu nghiệp vụ "
     "cần Không duyệt"),

    ("016", "Tài khoản đối ứng của phần chi phí công ty hàng thừa", "P2",
     "BB-2 đã duyệt",
     "1. Mở sổ chi tiết tài khoản 3381, xem tài khoản đối ứng của dòng Nợ phần chi phí công ty",
     "—",
     "- Mong đợi: đối ứng 711\n"
     "- Lưu ý: theo code hiện tại đối ứng ghi 771 - ghi Failed"),
]


SEC_VIII = [
    ("001", "In biên bản: phần thông tin chung", "P0",
     BB2 + "\nGhi chú \"Kiểm kê tháng 10\"",
     "1. Bấm bánh răng ở BB-2, chọn In",
     "—",
     "- Mở tab mới, khổ ngang, tiêu đề \"Biên bản xử lý hàng thừa thiếu\"\n"
     "- Có Số phiếu, Ngày lập, Từ ngày 01/10, Đến ngày 10/10, Kho K1, Ghi chú\n"
     "- Phiếu kiểm kê ghi \"KK-10; KK-11\""),

    ("002", "In biên bản: bảng hàng thừa, hàng thiếu", "P0",
     BB2,
     "1. In BB-2, đọc 2 bảng",
     "—",
     "- Bảng \"Tab1 - Hàng Thừa\" có H1; bảng \"Tab2 - Hàng Thiếu\" có H2, H3, STT mỗi bảng đánh lại từ 1\n"
     "- H1: Mã kho KT01, SL 3, Thành tiền vốn 300.000, Giá xử lý \"Giá vốn\", Chi phí nhân viên (%) \"40 %\", "
     "NV chịu dạng \"mã-họ tên\""),

    ("003", "In biên bản: cột Thành tiền bán", "P1",
     BB2,
     "1. In BB-2, đọc cột Thành tiền bán của H1",
     "—",
     "- Mong đợi: 450.000\n"
     "- Lưu ý: theo code hiện tại in 150.000 (đơn giá bán) - ghi Failed"),

    ("004", "In biên bản: ô trống khi bằng 0", "P2",
     BB2,
     "1. In BB-2, đọc dòng H2 (100% nhân viên)",
     "—",
     "- Chi phí công ty (%) để trống\n"
     "- Mong đợi: Chi phí công ty hiện \"-\"\n"
     "- Lưu ý: theo code hiện tại hiện 500.000 (xem V.012) - ghi Failed"),

    ("005", "Xuất Excel một biên bản", "P1",
     "BB-2 số BBXLKKHH-00007",
     "1. Bấm bánh răng ở BB-2, chọn Xuất Excel",
     "—",
     "- Tải về file \"bien_ban_xu_ly_hang_thua_thieuBBXLKKHH-00007.xlsx\"\n"
     "- Nội dung khớp bản In"),

    ("006", "In danh sách theo bộ lọc", "P1",
     "KT-1 có 3 biên bản Chờ duyệt, 2 Đã duyệt",
     "1. Lọc Trạng thái Chờ duyệt\n"
     "2. Bấm In ở hàng nút",
     "—",
     "- Mở tab mới khổ ngang, có đúng 3 dòng\n"
     "- Cột: STT, Số phiếu, Ngày lập, Kho vật lý, SL hàng thừa, SL hàng thiếu, Người lập, Người duyệt, "
     "Ngày duyệt, Trạng thái\n"
     "- Cuối có ngày, tháng, năm hiện tại"),

    ("007", "Xuất excel danh sách", "P1",
     "KT-1 có 5 biên bản",
     "1. Bấm Xuất excel ở hàng nút",
     "—",
     "- Tải file \"danh_sach_bien_ban_xu_ly_hang_thua_thieu_sau_kiem_ke.xlsx\"\n"
     "- Tiêu đề \"Danh sách biên bản xử lý hàng thừa thiếu sau kiểm kê\", 5 dòng, cột như bản In"),

    ("008", "Phần đầu bản In theo công ty người in", "P2",
     "BB-3 của công ty 1; NV-X công ty 3 mở được đường dẫn In",
     "1. NV-X mở đường dẫn In BB-3",
     "—",
     "- Phần đầu bản In là thông tin công ty 3 (công ty người in), không phải công ty 1\n"
     "- Lưu ý: ghi Failed nếu nghiệp vụ yêu cầu theo công ty của biên bản"),
]


SEC_IX = [
    ("001", "Lấy dữ liệu khi thiếu Từ ngày, Đến ngày, Kho", "P0",
     "Form Tạo mới trống",
     "1. Bấm Lấy dữ liệu ngay",
     "—",
     "- Báo \"Thiếu thông tin!\"\n"
     "- Dưới Từ ngày, Đến ngày, Kho vật lý có dòng báo bắt buộc bằng tiếng Anh\n"
     "- Bảng không đổi"),

    ("002", "Đến ngày trước Từ ngày", "P0",
     "—",
     "1. Chọn Từ ngày 10/10, Đến ngày 01/10, Kho K1\n"
     "2. Bấm Lấy dữ liệu",
     "Từ ngày: 10/10\n"
     "Đến ngày: 01/10",
     "- Báo \"Thiếu thông tin!\", dưới Đến ngày có dòng báo phải sau hoặc bằng Từ ngày (tiếng Anh)"),

    ("003", "Lý do bắt buộc ở từng dòng", "P0",
     KK,
     "1. Lấy dữ liệu, chọn NV chịu mọi dòng, để trống Lý do H1 và H3\n"
     "2. Bấm Lưu",
     "—",
     "- Báo \"Tạo thất bại!\"\n"
     "- Dưới ô Lý do H1 (tab Hàng thừa) và H3 (tab Hàng thiếu) có dòng báo bắt buộc\n"
     "- Chưa tạo biên bản"),

    ("004", "Lý do chỉ gồm khoảng trắng", "P2",
     KK,
     "1. Nhập Lý do H1 là 3 dấu cách, nhập đủ các ô khác\n"
     "2. Bấm Lưu",
     "Lý do: (3 dấu cách)",
     "- Báo lỗi bắt buộc như ô để trống"),

    ("005", "Ô % nhập chữ", "P1",
     KK,
     "1. Ở H2 nhập % Chi phí nhân viên \"abc\"\n"
     "2. Nhập đủ các ô khác, bấm Lưu",
     "% Chi phí nhân viên: abc",
     "- Mong đợi: báo \"Tạo thất bại!\", dưới ô % H2 có dòng báo phải là số\n"
     "- Lưu ý: theo code hiện tại lưu được, H2 có cả 2 ô % bằng 0 và chi phí bằng 0 - ghi Failed"),

    ("006", "Ô % nhập số thập phân", "P2",
     KK,
     "1. Ở H1 nhập % Chi phí nhân viên 33.5",
     "% Chi phí nhân viên: 33.5",
     "- % Chi phí công ty 66.5; Chi phí nhân viên 100.500, Chi phí công ty 199.500"),

    ("007", "File đính kèm không phải PDF", "P1",
     KK,
     "1. Bấm dấu + ở File đính kèm, ở hộp chọn file chuyển sang \"Tất cả file\", chọn \"bienban.docx\"\n"
     "2. Nhập đủ dữ liệu, bấm Lưu",
     "File: bienban.docx",
     "- Báo \"Tạo thất bại!\", ô file viền đỏ\n"
     "- Chưa tạo biên bản"),

    ("008", "File ảnh được chấp nhận", "P2",
     KK,
     "1. Đính kèm \"anh.jpg\" (chọn qua \"Tất cả file\"), nhập đủ dữ liệu, bấm Lưu",
     "File: anh.jpg",
     "- Theo code hiện tại: lưu thành công dù ô ghi \"(PDF)\"\n"
     "- Lưu ý: ghi Failed nếu nghiệp vụ chỉ nhận PDF"),

    ("009", "Ô file thêm nhưng chưa chọn file", "P2",
     KK,
     "1. Bấm dấu + ở File đính kèm nhưng không chọn file\n"
     "2. Nhập đủ dữ liệu, bấm Lưu",
     "—",
     "- Báo \"Tạo thất bại!\", ô file viền đỏ; bấm x bỏ ô trống thì lưu được"),

    ("010", "Bấm Lưu liên tiếp nhiều lần", "P1",
     KK,
     "1. Nhập đủ dữ liệu\n"
     "2. Bấm Lưu 3 lần thật nhanh",
     "—",
     "- Nút mờ ngay sau lần bấm đầu\n"
     "- Chỉ có 1 biên bản mới"),

    ("011", "Thông báo lỗi khi sửa và khi duyệt", "P2",
     "BB-1 Đang tạo; BB-2 Chờ duyệt",
     "1. Sửa BB-1, xóa Lý do H1, bấm Lưu\n"
     "2. Người duyệt xóa NV chịu H2 ở BB-2, bấm Duyệt",
     "—",
     "- Cả 2 bước đều báo \"Tạo thất bại!\" dù không phải thao tác tạo\n"
     "- Lưu ý: ghi Failed nếu nghiệp vụ yêu cầu câu thông báo đúng thao tác"),
]


SEC_X = [
    ("001", "Một phiếu kiểm kê đưa vào hai biên bản", "P0",
     KK + "\nBB-2 lấy từ KK-10, KK-11 đã Đã duyệt",
     "1. KT-1 Tạo mới, lấy dữ liệu 01/10 đến 10/10, kho K1\n"
     "2. Nhập đủ, bấm Lưu và gửi duyệt, người duyệt Duyệt\n"
     "3. Mở sổ chi tiết tài khoản 3341",
     "—",
     "- Mong đợi bước 1: KK-10, KK-11 không còn được lấy vì đã có trong BB-2\n"
     "- Lưu ý: theo code hiện tại lấy lại được, bút toán công nợ NV-C, NV-D bị ghi 2 lần - ghi Failed"),

    ("002", "Hai người duyệt bấm Duyệt cùng lúc", "P1",
     BB2 + "\nDUYET-1 và DUYET-2 cùng mở Chi tiết BB-2",
     "1. DUYET-1 và DUYET-2 cùng bấm Duyệt trong cùng một giây",
     "—",
     "- Chỉ 1 lần duyệt thành công, người còn lại báo \"Không có quyền\"\n"
     "- Bút toán chỉ có 1 bộ\n"
     "- Lưu ý: nếu cả hai cùng thành công và bút toán bị nhân đôi thì ghi Failed"),

    ("003", "Lấy được phiếu kiểm kê của công ty khác dùng chung kho", "P1",
     "Kho K1 dùng chung; KK-30 của công ty 3 Hoàn thành ngày 06/10; KT-1 thuộc công ty 1",
     "1. KT-1 lấy dữ liệu 01/10 đến 10/10, kho K1",
     "—",
     "- Theo code hiện tại: KK-30 hiện ở khung Phiếu kiểm kê và lập biên bản được\n"
     "- Lưu ý: ghi Failed nếu nghiệp vụ yêu cầu chỉ lấy phiếu công ty mình"),

    ("004", "Người lập sửa trong lúc người duyệt đang mở", "P2",
     "BB-1 Đang tạo do KT-1 lập",
     "1. KT-1 mở Sửa BB-1 ở tab 1, bấm Lưu và gửi duyệt ở tab 2\n"
     "2. Quay lại tab 1 bấm Lưu",
     "—",
     "- Bước 2: báo \"Bạn không có quyền sửa phiếu này\", BB-1 vẫn Chờ duyệt"),
]


SEC_XI = [
    ("001", "Luồng đầu - cuối: kiểm kê, điều chỉnh, biên bản, duyệt", "P0",
     "Hàng H1 ở kho K1 tồn 10, đơn giá vốn 100.000; KT-1 có quyền Kế toán kho; DUYET-1 có quyền duyệt",
     "1. Lập phiếu kiểm kê theo hàng hóa kho K1, Thực kiểm H1 = 7, duyệt, xử lý bằng phiếu xuất điều chỉnh "
     "và hoàn thành phiếu xuất cho tới khi phiếu kiểm kê Hoàn thành\n"
     "2. KT-1 " + MENU + ", Tạo mới, lấy dữ liệu theo ngày kiểm kê, kho K1\n"
     "3. H1: Lý do \"Mất hàng\", % nhân viên 100, NV chịu NV-D; bấm Lưu và gửi duyệt\n"
     "4. DUYET-1 mở từ thông báo, bấm Duyệt",
     "—",
     "- Bước 2: H1 ở tab Hàng thiếu, SL 3, Thành tiền vốn 300.000\n"
     "- Bước 4: biên bản Đã duyệt; Nợ 3341 / Có 1381 300.000 cho NV-D\n"
     "- Tồn H1 vẫn 7"),

    ("002", "Luồng lưu nháp, sửa, gửi duyệt", "P0",
     KK,
     "1. Lấy dữ liệu, nhập Lý do, NV chịu, bấm Lưu\n"
     "2. Mở Sửa, đổi % nhân viên H1 thành 40, bấm Lưu và gửi duyệt\n"
     "3. Người duyệt Duyệt",
     "—",
     "- Bước 1: Đang tạo; bước 2: Chờ duyệt; bước 3: Đã duyệt\n"
     "- Chi tiết sau duyệt giữ % nhân viên H1 là 40"),

    ("003", "Luồng hàng thừa công ty chịu toàn bộ", "P1",
     "KK-10 chỉ có H1 thừa 3 (Thành tiền vốn 300.000)",
     "1. Lập biên bản, H1: % Chi phí công ty 100, NV chịu NV-C, Lý do \"Nhầm nhập\"\n"
     "2. Gửi duyệt, người duyệt Duyệt, mở sổ chi tiết",
     "% Chi phí công ty: 100",
     "- Mong đợi: Nợ 3381 / Có 711 300.000; Nợ 3381 / Có 3341 bằng 0\n"
     "- Lưu ý: nếu Có 711 bằng 0 thì ghi Failed (xem V.012)"),

    ("004", "Tách phiếu kiểm kê ra hai biên bản", "P1",
     KK,
     "1. Biên bản A: lấy dữ liệu, bỏ chọn KK-11, Lưu và gửi duyệt\n"
     "2. Biên bản B: lấy dữ liệu, bỏ chọn KK-10, Lưu và gửi duyệt",
     "—",
     "- Biên bản A chỉ có H1, H2; biên bản B chỉ có H3\n"
     "- Cột Hàng thừa / Hàng thiếu: A là 3 / 2, B là 0 / 1"),
]
