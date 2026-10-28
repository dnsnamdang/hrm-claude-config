# -*- coding: utf-8 -*-
"""Cac section nghiep vu cho man 'Tong hop phieu bao hang ve'."""

SEC_I = [
    ("001", "Mở màn từ menu", "P0",
     "Tài khoản B có quyền xem theo tổng công ty",
     "1. Rê chuột vào menu Kinh doanh > Thông báo\n"
     "2. Bấm \"Phiếu báo hàng về\"",
     "—",
     "- Tiêu đề trang \"Tổng hợp phiếu báo hàng về\"\n"
     "- Có 3 tab theo thứ tự: Nhập khẩu · Trong nước · Mua ngoài\n"
     "- Tab Nhập khẩu được chọn sẵn, bảng đã có dữ liệu"),

    ("002", "Cột của tab Nhập khẩu", "P0",
     "Mở màn",
     "1. Quan sát tiêu đề bảng tab Nhập khẩu",
     "—",
     "- Đúng 10 cột: STT · Mã · Ngày tạo · Kho · Nhà cung cấp · Invoice · Hợp đồng · Người lập · Trạng thái · "
     "Hành động"),

    ("003", "Cột của tab Trong nước", "P0",
     "Mở màn",
     "1. Bấm tab Trong nước, quan sát tiêu đề bảng",
     "—",
     "- Đúng 7 cột: STT · Mã · Ngày tạo · Hợp đồng · Nhà cung cấp · Kho · Trạng thái\n"
     "- Không có cột Hành động, không có cột Người lập"),

    ("004", "Cột của tab Mua ngoài", "P0",
     "Mở màn",
     "1. Bấm tab Mua ngoài, quan sát tiêu đề bảng",
     "—",
     "- Đúng 7 cột: STT · Mã · Ngày tạo · Kho · Hợp đồng · Nhà cung cấp · Trạng thái\n"
     "- Không có cột Hành động"),

    ("005", "Chuyển qua lại giữa các tab", "P1",
     "Đang ở tab Nhập khẩu trang 3",
     "1. Bấm tab Mua ngoài\n"
     "2. Bấm lại tab Nhập khẩu",
     "—",
     "- Mỗi tab giữ trang và bộ lọc riêng\n"
     "- Quay lại tab Nhập khẩu vẫn ở trang 3"),

    ("006", "Màn không có chức năng tạo phiếu", "P2",
     "Mở màn",
     "1. Quan sát vùng nút ở cả 3 tab",
     "—",
     "- Chỉ có nút Bộ lọc, không có Tạo mới, Xuất Excel danh sách, Import"),

    ("007", "Tab không có dữ liệu", "P2",
     "Không có phiếu trong nước nào trong hệ thống",
     "1. Bấm tab Trong nước",
     "—",
     "- Bảng hiện thông báo không có dữ liệu, tổng 0, không lỗi trang"),
]

SEC_II = [
    ("001", "Mở khối Bộ lọc ở từng tab", "P1",
     "Tài khoản không có quyền xem theo cấp",
     "1. Bấm Bộ lọc ở từng tab, ghi lại các ô lọc",
     "—",
     "- Nhập khẩu: Mã · Nhà cung cấp · Invoice · Hợp đồng · Tên, mã hàng · Kho · Model · ô gợi ý "
     "\"all_barcodes\" · Người Lập · Trạng thái · Từ ngày · Đến ngày\n"
     "- Trong nước: Mã · Hợp đồng · Tên hàng · Mã hàng · Nhà cung cấp · Kho · Trạng thái\n"
     "- Mua ngoài: Công ty · Phòng ban · Từ ngày · Đến ngày · Mã · Hợp đồng · Tên, mã hàng · Kho · NCC · "
     "Trạng thái"),

    ("002", "Nhập khẩu - lọc theo Mã", "P0",
     "Có phiếu PBHV-00012 và PBHV-00120",
     "1. Nhập \"00012\" vào ô Mã, bấm kính lúp",
     "Mã: 00012",
     "- Ra cả PBHV-00012 và PBHV-00120 (tìm gần đúng)"),

    ("003", "Nhập khẩu - ô Nhà cung cấp liệt kê sai danh mục", "P0",
     "Mở tab Nhập khẩu",
     "1. Bấm Bộ lọc, mở ô Nhà cung cấp\n"
     "2. Chọn giá trị đầu tiên, bấm kính lúp",
     "—",
     "- Kỳ vọng nghiệp vụ: ô liệt kê danh sách nhà cung cấp\n"
     "- Lưu ý: theo code hiện tại ô đang liệt kê danh sách KHO, kết quả lọc sai - ghi nhận lỗi nếu xảy ra"),

    ("004", "Nhập khẩu - lọc theo Invoice và Hợp đồng", "P0",
     "Phiếu PBHV-00015 thuộc Invoice INV-2026-08, hợp đồng mua HĐNK-031",
     "1. Nhập \"INV-2026-08\" vào ô Invoice, bấm kính lúp\n"
     "2. Xóa, nhập \"HĐNK-031\" vào ô Hợp đồng, bấm kính lúp",
     "Invoice: INV-2026-08\nHợp đồng: HĐNK-031",
     "- Cả 2 lần đều có PBHV-00015, cột Invoice / Hợp đồng khớp giá trị đã lọc"),

    ("005", "Nhập khẩu - lọc theo Tên, mã hàng / Model / mã vạch", "P1",
     "PBHV-00015 có hàng mã TPE-001, model XR-500, mã vạch 8935000123",
     "1. Lần lượt nhập TPE-001 vào ô Tên, mã hàng; XR-500 vào ô Model; 8935000123 vào ô \"all_barcodes\"; "
     "mỗi lần bấm kính lúp",
     "—",
     "- Cả 3 lần đều có PBHV-00015"),

    ("006", "Nhập khẩu - lọc theo Kho, Người Lập, Trạng thái", "P0",
     "Tài khoản có quyền xem theo tổng công ty",
     "1. Chọn Kho = Kho Hà Nội, bấm kính lúp\n"
     "2. Bỏ Kho, chọn Người Lập = NV-A, bấm kính lúp\n"
     "3. Bỏ Người Lập, chọn Trạng thái = Đã gửi, bấm kính lúp",
     "—",
     "- Mỗi lần chỉ còn phiếu đúng điều kiện\n"
     "- Ô Người Lập tìm được cả nhân viên đã nghỉ"),

    ("007", "Nhập khẩu - lọc theo khoảng ngày tạo", "P0",
     "Có phiếu tạo lúc 16 giờ ngày 20/09/2026",
     "1. Nhập Từ ngày 20/09/2026, Đến ngày 20/09/2026, bấm kính lúp",
     "Từ ngày: 20/09/2026\nĐến ngày: 20/09/2026",
     "- Phiếu tạo ngày 20/09/2026 có trong kết quả (Đến ngày tính trọn ngày)"),

    ("008", "Trong nước - lọc theo Hợp đồng, Tên hàng, Mã hàng", "P0",
     "Phiếu trong nước PBHV-00003 thuộc HĐ mua trong nước HĐTN-010, có hàng \"Máy chiếu X1\" mã MC-X1",
     "1. Lần lượt lọc Hợp đồng = HĐTN-010; Tên hàng = Máy chiếu; Mã hàng = MC-X1",
     "—",
     "- Cả 3 lần đều có PBHV-00003"),

    ("009", "Trong nước - lọc theo Nhà cung cấp, Kho, Trạng thái", "P1",
     "Có phiếu trong nước của nhiều NCC, nhiều kho",
     "1. Lần lượt lọc từng ô, bấm kính lúp",
     "—",
     "- Kết quả đúng giá trị đã chọn ở cột tương ứng"),

    ("010", "Trong nước - không có lọc theo ngày", "P2",
     "Mở tab Trong nước",
     "1. Bấm Bộ lọc, tìm ô Từ ngày / Đến ngày",
     "—",
     "- Không có ô ngày"),

    ("011", "Mua ngoài - lọc theo Công ty / Phòng ban", "P0",
     "Công ty 1 có 300 phiếu mua ngoài, trong đó phòng MH1 có 40",
     "1. Chọn Công ty = Công ty 1, bấm kính lúp\n"
     "2. Chọn thêm Phòng ban = MH1, bấm kính lúp",
     "—",
     "- Bước 1: tổng 300\n"
     "- Bước 2: tổng 40\n"
     "- Chọn Công ty thì ô Phòng ban chỉ còn phòng của công ty đó"),

    ("012", "Mua ngoài - ô Hợp đồng không tìm theo mã phụ lục", "P1",
     "PBHV-00200 lập từ phụ lục PL-HĐMN-05 của hợp đồng HĐMN-05",
     "1. Nhập \"PL-HĐMN-05\" vào ô Hợp đồng, bấm kính lúp\n"
     "2. Nhập \"HĐMN-05\", bấm kính lúp",
     "—",
     "- Lưu ý: lần 1 KHÔNG ra PBHV-00200 (ô chỉ tìm theo mã hợp đồng mua ngoài)\n"
     "- Ghi nhận nếu nghiệp vụ yêu cầu tìm được theo mã phụ lục"),

    ("013", "Mua ngoài - lọc theo Tên, mã hàng, Kho, NCC, Trạng thái, khoảng ngày", "P1",
     "Có phiếu mua ngoài đa dạng",
     "1. Lần lượt lọc từng ô, bấm kính lúp",
     "—",
     "- Kết quả đúng giá trị đã chọn\n"
     "- Đến ngày tính trọn ngày"),

    ("014", "Nút làm mới", "P0",
     "Tab Nhập khẩu đang lọc 3 điều kiện",
     "1. Bấm nút làm mới (mũi tên tròn, xanh lá)",
     "—",
     "- Mọi ô lọc của tab đó trở về trống, danh sách hiện lại theo phạm vi quyền\n"
     "- Bộ lọc của 2 tab còn lại không bị ảnh hưởng"),

    ("015", "Ghi nhớ bộ lọc", "P1",
     "Tab Mua ngoài đang lọc Trạng thái = Đã gửi",
     "1. Chuyển sang màn khác, mở lại màn từ menu\n"
     "2. Bấm tab Mua ngoài",
     "—",
     "- Bộ lọc Trạng thái = Đã gửi vẫn được giữ"),

    ("016", "Lọc không có kết quả", "P2",
     "—",
     "1. Nhập Mã = \"ZZZ999\", bấm kính lúp",
     "Mã: ZZZ999",
     "- Bảng hiện không có dữ liệu, tổng 0"),
]

SEC_III = [
    ("001", "Phân trang và số dòng mỗi trang", "P1",
     "Tab Mua ngoài có 747 phiếu",
     "1. Đọc trang 1\n"
     "2. Sang trang 2\n"
     "3. Đổi số dòng mỗi trang thành 50",
     "—",
     "- Trang 1: 10 dòng, STT 1-10; trang 2 STT 11-20\n"
     "- Chọn 50: trang 1 có 50 dòng"),

    ("002", "Thứ tự mặc định phiếu mới nhất lên đầu", "P1",
     "Mở từng tab",
     "1. Đọc cột Ngày tạo từ trên xuống",
     "—",
     "- Ngày tạo giảm dần ở cả 3 tab"),

    ("003", "Sắp xếp theo Mã / Ngày tạo / Trạng thái", "P2",
     "Mở tab Nhập khẩu",
     "1. Bấm tiêu đề cột Mã, rồi Ngày tạo, rồi Trạng thái",
     "—",
     "- Danh sách sắp xếp lại theo cột vừa bấm\n"
     "- Các cột còn lại không sắp xếp được"),

    ("004", "Nhãn trạng thái", "P0",
     "Có phiếu ở cả 2 trạng thái",
     "1. Quan sát cột Trạng thái",
     "—",
     "- \"Đã gửi\" nền đỏ\n"
     "- \"Đã yêu cầu nhập hàng\" nền xanh"),

    ("005", "Bấm Mã mở chi tiết phiếu đúng luồng", "P0",
     "Mỗi tab có ít nhất 1 phiếu",
     "1. Ở từng tab bấm vào Mã phiếu đầu tiên",
     "—",
     "- Nhập khẩu: mở chi tiết phiếu báo hàng về nhập khẩu\n"
     "- Trong nước: mở chi tiết phiếu báo hàng về trong nước\n"
     "- Mua ngoài: mở chi tiết phiếu báo hàng về mua ngoài\n"
     "- Mã trên trang chi tiết khớp mã đã bấm"),

    ("006", "Bấm Invoice / Hợp đồng mở chứng từ gốc", "P1",
     "Tab Nhập khẩu và Mua ngoài có dữ liệu",
     "1. Tab Nhập khẩu: bấm Invoice, quay lại, bấm Hợp đồng\n"
     "2. Tab Mua ngoài: bấm Hợp đồng ở 1 phiếu lập từ hợp đồng và 1 phiếu lập từ phụ lục",
     "—",
     "- Mở đúng Invoice / hợp đồng mua nhập khẩu\n"
     "- Tab Mua ngoài: mở hợp đồng mua ngoài hoặc trang phụ lục tương ứng"),

    ("007", "Cột Nhà cung cấp tab Mua ngoài", "P2",
     "PBHV-00200 lập từ hợp đồng HĐMN-05, NCC Công ty An Phát",
     "1. Đọc cột Nhà cung cấp của PBHV-00200",
     "—",
     "- Hiển thị mã hợp đồng ghép tên NCC\n"
     "- Giá trị: \"HĐMN-05 - Công ty An Phát\""),

    ("008", "Phiếu không gắn kho", "P2",
     "Phiếu mua ngoài không chọn kho",
     "1. Đọc cột Kho",
     "—",
     "- Ô Kho để trống, không lỗi"),

    ("009", "Trùng mã phiếu giữa các tab", "P2",
     "Tab Nhập khẩu và tab Mua ngoài cùng có PBHV-00010",
     "1. Bấm Mã PBHV-00010 ở từng tab",
     "—",
     "- Mở 2 phiếu khác nhau của 2 luồng mua"),
]

SEC_IV = [
    ("001", "Menu hành động tab Nhập khẩu - phiếu Đã gửi do mình lập", "P0",
     "NV-A lập PBHV-00010 trạng thái Đã gửi",
     "1. Đăng nhập NV-A, bấm biểu tượng bánh răng ở cột Hành động của PBHV-00010",
     "—",
     "- Có 3 mục: In · Xuất Excel · Xóa"),

    ("002", "Menu hành động - phiếu không đủ điều kiện xóa", "P0",
     "PBHV-00011 Đã gửi do NV-B lập; PBHV-00020 Đã yêu cầu nhập hàng do NV-A lập",
     "1. Đăng nhập NV-A (có quyền xem theo tổng công ty), mở menu hành động 2 phiếu",
     "—",
     "- Cả 2 phiếu chỉ có In và Xuất Excel, KHÔNG có Xóa"),

    ("003", "In phiếu báo hàng về nhập khẩu", "P0",
     "PBHV-00010 có 3 dòng hàng",
     "1. Bấm bánh răng > In",
     "—",
     "- Mở tab trình duyệt mới hiển thị mẫu in \"Phiếu báo hàng về\" khổ ngang\n"
     "- Đủ 3 dòng hàng, thông tin khớp phiếu"),

    ("004", "Xuất Excel phiếu báo hàng về nhập khẩu", "P0",
     "PBHV-00010 có 3 dòng hàng",
     "1. Bấm bánh răng > Xuất Excel\n"
     "2. Mở file tải về",
     "—",
     "- Tải file tên \"phieu_bao_hang_ve.xlsx\"\n"
     "- Nội dung khớp phiếu, đủ 3 dòng hàng"),

    ("005", "Tab Trong nước / Mua ngoài không có thao tác", "P1",
     "Có phiếu ở 2 tab",
     "1. Quan sát từng dòng",
     "—",
     "- Không có biểu tượng bánh răng / menu hành động\n"
     "- Muốn In / Xuất Excel / Tạo yêu cầu nhập hàng phải vào màn danh sách của luồng tương ứng"),
]

SEC_V = [
    ("001", "Trạng thái đổi khi lập yêu cầu nhập hàng", "P0",
     "PBHV-00010 tab Nhập khẩu trạng thái Đã gửi, do NV-A lập",
     "1. NV-A lập Yêu cầu nhập hàng từ phiếu PBHV-00010 ở màn của luồng nhập khẩu\n"
     "2. Mở lại màn Tổng hợp, tab Nhập khẩu",
     "—",
     "- PBHV-00010 chuyển nhãn xanh \"Đã yêu cầu nhập hàng\"\n"
     "- Mục Xóa không còn trong menu hành động"),

    ("002", "Phiếu vừa lập yêu cầu nhập hàng biến mất với người khác", "P0",
     "Như TC_05.001; tài khoản B có quyền xem theo tổng công ty, không lập phiếu",
     "1. B mở tab Nhập khẩu, tìm PBHV-00010",
     "Mã: PBHV-00010",
     "- PBHV-00010 KHÔNG còn hiện với B\n"
     "- Lưu ý: ghi nhận nếu nghiệp vụ muốn người có quyền vẫn thấy phiếu đã yêu cầu nhập hàng"),
]

SEC_VI = [
    ("001", "Xóa phiếu Đã gửi từ tab Nhập khẩu", "P0",
     "NV-A lập PBHV-00010 Đã gửi, từ Invoice INV-2026-08",
     "1. Bấm bánh răng > Xóa\n"
     "2. Đọc hộp thoại, bấm Xác nhận\n"
     "3. Quay lại màn Tổng hợp, tìm PBHV-00010",
     "—",
     "- Hộp thoại \"Xác nhận xóa!\" nội dung \"Bạn chắc chắn muốn xóa bản ghi này?\"\n"
     "- Sau Xác nhận: Lưu ý - trình duyệt chuyển sang trang trắng, không có thông báo, phải tự quay lại\n"
     "- PBHV-00010 không còn trong danh sách"),

    ("002", "Hủy xóa", "P0",
     "PBHV-00010 Đã gửi do mình lập",
     "1. Bấm Xóa\n"
     "2. Bấm Hủy",
     "—",
     "- Hộp thoại đóng, phiếu còn nguyên"),

    ("003", "Xóa phiếu mở lại Invoice cho báo hàng về", "P1",
     "Như TC_06.001",
     "1. Sau khi xóa, vào màn lập phiếu báo hàng về nhập khẩu\n"
     "2. Chọn Invoice INV-2026-08",
     "—",
     "- Invoice INV-2026-08 lại chọn được để lập phiếu báo hàng về mới"),
]

SEC_VII = [
    ("001", "In / Xuất Excel theo từng phiếu (đã test ở IV)", "P2",
     "—", "1. Xem TC_04.003 và TC_04.004", "—",
     "- Màn không có In / Xuất Excel theo danh sách; chỉ có theo từng phiếu ở tab Nhập khẩu"),
]

SEC_VIII = [
    ("001", "Nhập ký tự đặc biệt vào ô tìm", "P2",
     "Mở tab Nhập khẩu",
     "1. Nhập \"%\" vào ô Mã, bấm kính lúp\n"
     "2. Nhập \"'\" vào ô Hợp đồng, bấm kính lúp",
     "—",
     "- Không lỗi trang, không treo bảng"),

    ("002", "Từ ngày lớn hơn Đến ngày", "P2",
     "Tab Mua ngoài",
     "1. Nhập Từ ngày 30/09/2026, Đến ngày 01/09/2026, bấm kính lúp",
     "—",
     "- Không báo lỗi, bảng trống"),

    ("003", "Nhập ngày sai định dạng", "P2",
     "Tab Nhập khẩu",
     "1. Gõ tay \"2026-09-01\" vào ô Từ ngày, bấm kính lúp",
     "—",
     "- Trang không treo; ghi lại kết quả thực tế"),
]

SEC_IX = [
    ("001", "Phiếu có hàng của hãng mình phụ trách mua", "P0",
     "NV-A không có quyền xem; được phân công phụ trách hãng H1 tại Công ty 1\n"
     "PBHV-00030 (Đã gửi, do NV-B lập) có 1 dòng hàng khuyến mại thuộc hãng H1",
     "1. NV-A mở tab Nhập khẩu, tìm PBHV-00030",
     "—",
     "- PBHV-00030 hiện (tính cả hàng thường, hàng bảo hành, hàng khuyến mại)"),

    ("002", "Hết phân công phụ trách hãng thì không còn thấy", "P1",
     "Như TC_09.001, sau đó phân công của NV-A với hãng H1 được kết thúc",
     "1. NV-A mở lại tab Nhập khẩu, tìm PBHV-00030",
     "—",
     "- PBHV-00030 không còn hiện"),

    ("003", "Phân công ở công ty khác không được tính", "P1",
     "NV-A được phân công hãng H2 nhưng ở Công ty 3, hồ sơ NV-A thuộc Công ty 1",
     "1. NV-A mở tab Nhập khẩu, tìm phiếu có hàng hãng H2",
     "—",
     "- Phiếu đó không hiện (chỉ tính phân công trong công ty của mình)"),

    ("004", "Phiếu mới lập hiện ngay ở cả tab", "P1",
     "Màn đang mở ở tab Mua ngoài",
     "1. Người khác lập 1 phiếu báo hàng về mua ngoài mới\n"
     "2. Bấm kính lúp",
     "—",
     "- Phiếu mới hiện đầu danh sách, trạng thái Đã gửi"),

    ("005", "Hai người cùng xóa một phiếu", "P2",
     "NV-A mở màn ở 2 trình duyệt, PBHV-00010 Đã gửi",
     "1. Trình duyệt 1 xóa PBHV-00010\n"
     "2. Trình duyệt 2 (chưa tải lại) bấm Xóa PBHV-00010, Xác nhận",
     "—",
     "- Trình duyệt 2 báo lỗi không tìm thấy dữ liệu, không làm hỏng dữ liệu khác"),
]

SEC_X = [
    ("001", "Luồng nhập khẩu: lập phiếu, theo dõi, lập yêu cầu nhập hàng", "P0",
     "NV-A có quyền \"Lập phiếu báo hàng về mua hàng nhập khẩu\"; Invoice INV-2026-09 chưa báo hàng về",
     "1. NV-A lập phiếu báo hàng về từ Invoice INV-2026-09 ở màn của luồng nhập khẩu\n"
     "2. Mở Kinh doanh > Thông báo > Phiếu báo hàng về, tab Nhập khẩu\n"
     "3. Kiểm tra dòng phiếu mới\n"
     "4. Lập Yêu cầu nhập hàng từ phiếu\n"
     "5. Quay lại màn Tổng hợp",
     "—",
     "- Bước 3: phiếu mới ở đầu danh sách, Đã gửi (đỏ), Invoice INV-2026-09, có In / Xuất Excel / Xóa\n"
     "- Bước 5: phiếu chuyển Đã yêu cầu nhập hàng (xanh), không còn Xóa"),

    ("002", "Luồng trong nước: phiếu hiện ở tab Trong nước", "P0",
     "NV-C có quyền \"Lập phiếu báo hàng về mua hàng trong nước\"",
     "1. NV-C lập phiếu báo hàng về từ hợp đồng mua trong nước HĐTN-011\n"
     "2. Tài khoản bất kỳ mở màn Tổng hợp, bấm tab Trong nước",
     "—",
     "- Phiếu mới hiện, cột Hợp đồng HĐTN-011, trạng thái Đã gửi"),

    ("003", "Luồng mua ngoài: phiếu hiện ở tab Mua ngoài", "P0",
     "Hợp đồng mua ngoài HĐMN-06 đã đủ điều kiện báo hàng về",
     "1. Lập phiếu báo hàng về từ HĐMN-06\n"
     "2. Mở màn Tổng hợp, bấm tab Mua ngoài, lọc Hợp đồng = HĐMN-06",
     "—",
     "- Phiếu mới hiện, trạng thái Đã gửi\n"
     "- Nhà cung cấp dạng \"HĐMN-06 - <Tên NCC>\""),

    ("004", "Đối chiếu số lượng với màn danh sách của từng luồng", "P1",
     "Tài khoản B có quyền xem phiếu báo hàng về nhập khẩu theo tổng công ty",
     "1. Đếm tổng tab Nhập khẩu ở màn Tổng hợp\n"
     "2. Đếm tổng ở màn Nhập khẩu > Mua hàng nhập khẩu > Danh sách báo hàng về",
     "—",
     "- Màn Tổng hợp ít hơn đúng bằng số phiếu Đã yêu cầu nhập hàng của người khác\n"
     "- Chênh lệch ngoài con số này phải ghi nhận"),
]
