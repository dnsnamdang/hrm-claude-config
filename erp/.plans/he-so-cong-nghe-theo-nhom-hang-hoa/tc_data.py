# -*- coding: utf-8 -*-
"""Khoi mo ta + toan bo TC cho man ERP 'He so cong nghe theo nhom hang hoa'."""

MENU = ("Mở menu trên cùng, rê chuột vào QTTT > nhóm \"Cấu hình ERP\" > bấm "
        "\"Hệ số công nghệ theo nhóm hàng hóa\"")

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Khai báo HỆ SỐ CÔNG NGHỆ (còn gọi là tỷ lệ hưởng công khoán) cho từng NHÓM HÀNG HÓA.\n"
     "Mỗi bản ghi gồm: Loại hệ số (tên gọi), Hệ số (số, tối đa 2 chữ số thập phân) và danh sách các "
     "nhóm hàng hóa được áp dụng hệ số đó.\n"
     "Hệ số được dùng làm hệ số hưởng MẶC ĐỊNH cho hàng hóa ở phần Lắp đặt bàn giao của phiếu phân "
     "công bảo hành - sửa chữa: hàng thuộc nhóm đã gán thì lấy hệ số của nhóm, hàng thuộc nhóm chưa "
     "gán thì lấy hệ số 1.\n"
     "Người dùng làm được: xem danh sách, lọc, thêm mới, sửa, xóa. Màn KHÔNG có in, xuất Excel, "
     "khóa/mở khóa."),

    ("2. Đối tượng được tính / hiển thị",
     "- Chỉ hiển thị các bản ghi thuộc CÔNG TY của người đang đăng nhập (công ty ghi nhận theo người "
     "tạo tại thời điểm tạo).\n"
     "- Không có trạng thái: mọi bản ghi của công ty đều hiển thị.\n"
     "- Cột Nhóm hàng hóa liệt kê mọi nhóm đã gán, mỗi nhóm một dòng, kể cả nhóm hàng đã ngừng "
     "hoạt động.\n"
     "- Ô chọn Nhóm hàng hóa áp dụng trong cửa sổ Thêm mới/Sửa chỉ liệt kê các nhóm hàng ĐANG HOẠT "
     "ĐỘNG, sắp xếp A-Z theo tên."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Bản ghi của công ty khác: không hiển thị, kể cả khi chọn công ty đó ở bộ lọc Công ty.\n"
     "- Nhóm hàng đã ngừng hoạt động: không có trong ô chọn Nhóm hàng hóa áp dụng.\n"
     "- Bản ghi đã xóa: biến mất hẳn, các nhóm hàng của nó được giải phóng để gán cho bản ghi khác."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Không áp dụng — màn không có bộ lọc theo ngày. Cột Ngày tạo / Ngày sửa chỉ để hiển thị."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Quan hệ 1 - nhiều: một bản ghi Loại hệ số gán được NHIỀU nhóm hàng; một nhóm hàng chỉ được "
     "thuộc TỐI ĐA MỘT bản ghi.\n"
     "Không có cây phân cấp. Không có bảng con hiển thị riêng."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Tên Loại tỷ lệ hưởng không được trùng trong cùng một công ty (công ty khác được trùng tên).\n"
     "- Một nhóm hàng không được nằm trong 2 bản ghi. Lưu ý: kiểm tra trùng nhóm áp dụng trên TOÀN "
     "HỆ THỐNG, không phân biệt công ty — nhóm đã gán ở công ty A thì công ty B không gán được.\n"
     "- Khi Sửa, danh sách nhóm hàng được THAY THẾ TOÀN BỘ bằng danh sách mới chọn (không cộng dồn)."),

    ("7. Phân quyền cấp",
     "Màn KHÔNG gắn quyền riêng nào: mọi tài khoản đã đăng nhập ERP đều thấy mục menu, xem, thêm "
     "mới, sửa, xóa được bản ghi của công ty mình.\n"
     "Nút Sửa và Xóa hiện trên MỌI dòng, không phụ thuộc người tạo.\n"
     "Chưa đăng nhập thì bị đưa về trang đăng nhập."),

    ("8. Cách tính các ô thống kê",
     "- Cột STT: đánh số liên tục theo trang, trang 2 với 10 dòng/trang bắt đầu từ 11.\n"
     "- Dòng dưới bảng \"Đang xem a đến b trong tổng số N mục\": a là dòng đầu trang, b là dòng cuối "
     "trang, N là tổng bản ghi của công ty khớp bộ lọc.\n"
     "- Màn không có ô tổng tiền / tổng số lượng."),

    ("9. Ghi chú đọc bảng",
     "- Cột Hệ số hiển thị dấu CHẤM thập phân và luôn 2 chữ số sau dấu, ví dụ nhập 3,2 thì hiện 3.20; "
     "ô nhập Hệ số cũng dùng dấu chấm (gõ 1.5, không gõ 1,5).\n"
     "- Ô Hệ số tự cắt phần thập phân về 2 chữ số khi đang gõ; KHÔNG chặn số âm và số 0.\n"
     "- Ngày tạo / Ngày sửa dạng ngày/tháng/năm - giờ:phút.\n"
     "- Nhãn không thống nhất: cột ghi \"Loại hệ số\", ô lọc ghi \"Loại tỷ lệ hưởng\", tiêu đề cửa sổ "
     "ghi \"tỷ lệ hưởng công khoán\" — cùng một thông tin.\n"
     "- Bộ lọc tự chạy sau khoảng nửa giây ngừng gõ, không cần bấm nút tìm; điều kiện lọc được trình "
     "duyệt ghi nhớ cho lần mở sau.\n"
     "- Bẫy dễ sai: bấm sắp xếp ở các cột Hệ số / Ngày tạo / Ngày sửa có thể KHÔNG đổi thứ tự (bản ghi "
     "mới tạo luôn được ưu tiên đứng đầu); bấm sắp xếp ở cột Nhóm hàng hóa có thể báo lỗi tải dữ liệu "
     "— xem nhóm III."),
]

ROLE_TCS = [
    ("00", "Tài khoản bất kỳ đã đăng nhập đều vào được màn và thao tác đủ", "P0",
     "Tài khoản NV-A là nhân viên thường, không được gán quyền cấu hình nào\n"
     "Công ty của NV-A có 3 bản ghi hệ số do người khác tạo",
     "1. Đăng nhập bằng NV-A\n"
     "2. " + MENU + "\n"
     "3. Quan sát nút Thêm mới và cột Hành động",
     "Tài khoản: NV-A",
     "- Mục menu hiển thị và mở được màn\n"
     "- Bảng hiện đủ 3 bản ghi của công ty\n"
     "- Có nút Thêm mới\n"
     "- Mọi dòng đều có nút Sửa (bút chì) và Xóa (dấu X đỏ), kể cả bản ghi do người khác tạo"),

    ("01", "Chưa đăng nhập không vào được màn", "P0",
     "Trình duyệt đã đăng xuất khỏi ERP",
     "1. Mở trang chủ ERP khi chưa đăng nhập\n"
     "2. Thử mở lại màn Hệ số công nghệ từ lịch sử trình duyệt",
     "—",
     "- Hệ thống đưa về trang đăng nhập\n"
     "- Không hiển thị bất kỳ dữ liệu hệ số nào"),

    ("02", "Nhân viên thường sửa được bản ghi do người khác tạo", "P1",
     "Bản ghi \"Hệ số lắp đặt\" do quản lý QL-B tạo, Hệ số 1.20\n"
     "Tài khoản NV-A cùng công ty, không có quyền đặc biệt",
     "1. Đăng nhập NV-A, mở màn\n"
     "2. Bấm Sửa ở dòng \"Hệ số lắp đặt\"\n"
     "3. Đổi Hệ số thành 1.50, bấm Lưu",
     "Hệ số: 1.50",
     "- Lưu thành công, thông báo \"Thao tác thành công\"\n"
     "- Cột Người sửa đổi thành NV-A, Người tạo vẫn là QL-B\n"
     "- Lưu ý: hành vi này đúng theo code hiện tại (màn không phân quyền); nếu nghiệp vụ yêu cầu "
     "giới hạn người sửa thì ghi nhận lại cho đội phát triển"),
]

SEC_I = [
    ("001", "Mở màn từ menu QTTT", "P0",
     "Tài khoản bất kỳ đã đăng nhập",
     "1. " + MENU + "\n"
     "2. Quan sát tiêu đề trang và bảng",
     "—",
     "- Mở đúng màn, tiêu đề trang \"Hệ số công nghệ theo nhóm hàng hóa\"\n"
     "- Bảng tải dữ liệu, không báo lỗi"),

    ("002", "Bố cục mặc định của màn", "P0",
     "Công ty có ít nhất 1 bản ghi",
     "1. Mở màn\n"
     "2. Quan sát từ trên xuống",
     "—",
     "- Góc phải phía trên có nút \"Thêm mới\" (biểu tượng dấu cộng)\n"
     "- Phía trên bảng có nút \"Bộ lọc\"; khối lọc mặc định ĐANG THU GỌN\n"
     "- Bảng có đủ 9 cột theo thứ tự: STT, Loại hệ số, Hệ số, Nhóm hàng hóa, Người tạo, Người sửa, "
     "Ngày tạo, Ngày sửa, Hành động\n"
     "- Dưới bảng có dòng \"Đang xem … trong tổng số … mục\", ô chọn số dòng \"Xem … mục\" và nút "
     "phân trang"),

    ("003", "Màn chỉ có một lối vào", "P2",
     "—",
     "1. Rà các phân hệ trên menu trên cùng\n"
     "2. Tìm mục \"Hệ số công nghệ theo nhóm hàng hóa\"",
     "—",
     "- Chỉ có 1 mục menu, nằm ở QTTT > Cấu hình ERP\n"
     "- Không có chế độ xem \"của tôi\" / \"tất cả\": luôn hiện toàn bộ bản ghi của công ty"),

    ("004", "Công ty chưa có bản ghi nào", "P1",
     "Đăng nhập tài khoản thuộc công ty chưa khai báo hệ số nào",
     "1. Mở màn",
     "—",
     "- Bảng hiện \"Không có dữ liệu\"\n"
     "- Dòng dưới bảng ghi \"Đang xem 0 đến 0 trong tổng số 0 mục\"\n"
     "- Nút Thêm mới vẫn dùng được"),

    ("005", "Tải lại trang giữ nguyên bộ lọc đã nhập", "P2",
     "Công ty có 5 bản ghi, trong đó 2 bản ghi tên chứa \"lắp\"",
     "1. Bấm Bộ lọc, gõ \"lắp\" vào ô Loại tỷ lệ hưởng, chờ bảng lọc xong\n"
     "2. Bấm F5 tải lại trang\n"
     "3. Mở lại khối Bộ lọc",
     "Loại tỷ lệ hưởng: lắp",
     "- Sau khi tải lại, ô Loại tỷ lệ hưởng vẫn còn chữ \"lắp\"\n"
     "- Bảng vẫn chỉ hiện 2 bản ghi"),
]

SEC_II = [
    ("001", "Mở / thu gọn khối Bộ lọc", "P1",
     "—",
     "1. Bấm nút Bộ lọc\n"
     "2. Bấm Bộ lọc lần nữa",
     "—",
     "- Lần 1: khối lọc mở ra gồm 4 ô: Công ty, Loại tỷ lệ hưởng, Người tạo, Người sửa và 2 nút "
     "tìm kiếm (kính lúp), làm mới (mũi tên tròn)\n"
     "- Lần 2: khối lọc thu gọn lại"),

    ("002", "Lọc theo Loại tỷ lệ hưởng — tìm gần đúng", "P0",
     "Công ty có 4 bản ghi: \"Hệ số lắp đặt\", \"Hệ số lắp ráp\", \"Hệ số bảo trì\", \"Thiết bị lớn\"",
     "1. Mở Bộ lọc\n"
     "2. Gõ \"lắp\" vào ô Loại tỷ lệ hưởng, ngừng gõ và chờ khoảng 1 giây",
     "Loại tỷ lệ hưởng: lắp",
     "- Bảng tự lọc, không cần bấm nút tìm\n"
     "- Còn đúng 2 dòng: \"Hệ số lắp đặt\", \"Hệ số lắp ráp\"\n"
     "- Tổng ghi \"trong tổng số 2 mục\""),

    ("003", "Lọc Loại tỷ lệ hưởng không phân biệt hoa thường", "P2",
     "Như TC_02.002",
     "1. Gõ \"HỆ SỐ\" vào ô Loại tỷ lệ hưởng",
     "Loại tỷ lệ hưởng: HỆ SỐ",
     "- Hiện 3 dòng có chữ \"Hệ số\" ở đầu tên\n"
     "- \"Thiết bị lớn\" không hiện"),

    ("004", "Lọc theo Người tạo", "P0",
     "Công ty có 5 bản ghi: NV-A tạo 2, QL-B tạo 3",
     "1. Mở Bộ lọc\n"
     "2. Ở ô Người tạo gõ vài ký tự tên NV-A, chọn NV-A trong danh sách gợi ý",
     "Người tạo: NV-A",
     "- Bảng còn đúng 2 dòng, cột Người tạo đều là NV-A\n"
     "- Danh sách gợi ý có cả nhân viên đã nghỉ việc"),

    ("005", "Lọc theo Người sửa", "P1",
     "Bản ghi X do NV-A tạo, QL-B sửa lần cuối; bản ghi Y do NV-A tạo và chưa ai sửa",
     "1. Mở Bộ lọc\n"
     "2. Chọn Người sửa: QL-B",
     "Người sửa: QL-B",
     "- Chỉ hiện bản ghi X\n"
     "- Bản ghi Y không hiện (Người sửa của Y chính là NV-A — người tạo)"),

    ("006", "Lọc theo Công ty của chính mình", "P1",
     "Tài khoản thuộc công ty C1, C1 có 5 bản ghi",
     "1. Mở Bộ lọc\n"
     "2. Ở ô Công ty chọn C1",
     "Công ty: C1",
     "- Bảng vẫn hiện đủ 5 bản ghi"),

    ("007", "Chọn công ty KHÁC ở ô Công ty không xem được dữ liệu công ty đó", "P0",
     "Tài khoản thuộc C1; công ty C2 có 4 bản ghi hệ số",
     "1. Mở Bộ lọc\n"
     "2. Ở ô Công ty chọn C2",
     "Công ty: C2",
     "- Bảng hiện \"Không có dữ liệu\"\n"
     "- KHÔNG lộ bản ghi nào của C2\n"
     "- Lưu ý: ô Công ty liệt kê mọi công ty đang hoạt động nhưng chỉ có tác dụng với công ty của "
     "chính mình"),

    ("008", "Kết hợp nhiều điều kiện lọc", "P1",
     "Công ty có \"Hệ số lắp đặt\" (NV-A tạo), \"Hệ số lắp ráp\" (QL-B tạo)",
     "1. Gõ \"lắp\" ở ô Loại tỷ lệ hưởng\n"
     "2. Chọn Người tạo: QL-B",
     "Loại tỷ lệ hưởng: lắp\nNgười tạo: QL-B",
     "- Chỉ còn \"Hệ số lắp ráp\""),

    ("009", "Nút làm mới xóa sạch điều kiện lọc", "P1",
     "Đang lọc như TC_02.008",
     "1. Bấm nút làm mới (mũi tên tròn) trong khối Bộ lọc",
     "—",
     "- Các ô lọc trở về trống\n"
     "- Bảng hiện lại toàn bộ bản ghi của công ty"),

    ("010", "Lọc không có kết quả", "P2",
     "—",
     "1. Gõ \"zzzz\" vào ô Loại tỷ lệ hưởng",
     "Loại tỷ lệ hưởng: zzzz",
     "- Bảng hiện \"Không có dữ liệu\", không báo lỗi"),

    ("011", "Ký tự đặc biệt trong ô lọc không làm lỗi trang", "P2",
     "—",
     "1. Gõ lần lượt: % , _ , ' , \" vào ô Loại tỷ lệ hưởng",
     "Loại tỷ lệ hưởng: %\n_\n'\n\"",
     "- Bảng tải bình thường, không báo lỗi\n"
     "- Lưu ý: gõ % hoặc _ có thể hiện TẤT CẢ bản ghi (ký tự này đóng vai trò đại diện khi tìm)"),
]

SEC_III = [
    ("001", "Thứ tự mặc định: bản ghi tạo sau đứng trước", "P0",
     "Tạo lần lượt 3 bản ghi \"HS-1\", \"HS-2\", \"HS-3\"",
     "1. Mở màn\n"
     "2. Đọc 3 dòng đầu",
     "—",
     "- Thứ tự từ trên xuống: HS-3, HS-2, HS-1\n"
     "- Sửa HS-1 xong KHÔNG làm HS-1 nhảy lên đầu"),

    ("002", "Cột Nhóm hàng hóa hiện mỗi nhóm một dòng", "P0",
     "Bản ghi \"Hệ số lắp đặt\" gán 3 nhóm: Máy lọc nước, Điều hòa, Bình nóng lạnh",
     "1. Tìm dòng \"Hệ số lắp đặt\"\n"
     "2. Đọc cột Nhóm hàng hóa",
     "—",
     "- Ô hiện đủ 3 tên nhóm, mỗi tên một dòng"),

    ("003", "Định dạng các cột số và ngày", "P1",
     "Bản ghi tạo lúc 09:05 ngày 14/10/2026 với Hệ số 3.2",
     "1. Tìm bản ghi\n"
     "2. Đọc cột Hệ số, Ngày tạo, Ngày sửa",
     "Hệ số: 3.2",
     "- Cột Hệ số hiện 3.20\n"
     "- Ngày tạo hiện 14/10/2026 - 09:05\n"
     "- Ngày sửa bằng Ngày tạo khi chưa sửa lần nào\n"
     "- Người sửa bằng Người tạo khi chưa sửa lần nào"),

    ("004", "Bấm sắp xếp cột Hệ số", "P1",
     "Có 3 bản ghi tạo theo thứ tự: A hệ số 2.00, B hệ số 0.50, C hệ số 1.00",
     "1. Bấm tiêu đề cột Hệ số (tăng dần)\n"
     "2. Bấm lần nữa (giảm dần)",
     "—",
     "- Tăng dần: B, C, A; giảm dần: A, C, B\n"
     "- Lưu ý: theo đọc code, thứ tự có thể KHÔNG đổi (giữ C, B, A theo ngày tạo) — nếu vậy ghi "
     "Failed"),

    ("005", "Bấm sắp xếp cột Ngày tạo / Ngày sửa", "P2",
     "Như TC_03.004; sửa bản ghi A sau cùng",
     "1. Bấm tiêu đề cột Ngày sửa (giảm dần)\n"
     "2. Bấm tiêu đề cột Ngày tạo (tăng dần)",
     "—",
     "- Ngày sửa giảm dần: A lên đầu\n"
     "- Ngày tạo tăng dần: A, B, C\n"
     "- Lưu ý: cùng nguy cơ như TC_03.004 — thứ tự không đổi thì ghi Failed"),

    ("006", "Bấm sắp xếp cột Nhóm hàng hóa", "P1",
     "Công ty có ít nhất 2 bản ghi",
     "1. Bấm tiêu đề cột Nhóm hàng hóa",
     "—",
     "- Bảng sắp lại hoặc giữ nguyên, KHÔNG báo lỗi\n"
     "- Lưu ý: theo đọc code, thao tác này có nguy cơ hiện hộp lỗi tải dữ liệu và bảng trống — "
     "nếu xảy ra ghi Failed"),

    ("007", "Các cột không cho sắp xếp", "P2",
     "—",
     "1. Bấm tiêu đề các cột STT, Loại hệ số, Người tạo, Người sửa, Hành động",
     "—",
     "- Không có mũi tên sắp xếp, bấm không đổi thứ tự"),

    ("008", "Phân trang mặc định 10 dòng", "P0",
     "Công ty có 23 bản ghi",
     "1. Mở màn, đọc dòng dưới bảng\n"
     "2. Bấm sang trang 3",
     "—",
     "- Trang 1: \"Đang xem 1 đến 10 trong tổng số 23 mục\"\n"
     "- Trang 3: 3 dòng, STT 21–23, \"Đang xem 21 đến 23 trong tổng số 23 mục\""),

    ("009", "Đổi số dòng mỗi trang", "P1",
     "Như TC_03.008",
     "1. Ở ô \"Xem … mục\" chọn 25",
     "Số dòng: 25",
     "- Cả 23 bản ghi nằm trên 1 trang, STT 1–23\n"
     "- Nút phân trang chỉ còn trang 1"),
]

SEC_IV = [
    ("001", "Mở cửa sổ Thêm mới", "P0",
     "—",
     "1. Bấm nút Thêm mới",
     "—",
     "- Mở cửa sổ tiêu đề \"Thêm mới tỷ lệ hưởng công khoán\"\n"
     "- Có 3 ô, đều có dấu (*): Loại tỷ lệ hưởng, Hệ số, Nhóm hàng hóa áp dụng\n"
     "- Các ô đều trống; ô Hệ số canh phải\n"
     "- Chân cửa sổ có nút Lưu (xanh lá) và Hủy (đỏ)"),

    ("002", "Thêm mới thành công với 1 nhóm hàng", "P0",
     "Nhóm \"Máy lọc nước\" đang hoạt động và chưa thuộc bản ghi nào",
     "1. Bấm Thêm mới\n"
     "2. Nhập Loại tỷ lệ hưởng, Hệ số\n"
     "3. Chọn 1 nhóm hàng\n"
     "4. Bấm Lưu",
     "Loại tỷ lệ hưởng: Hệ số lọc nước\nHệ số: 1.5\nNhóm hàng hóa áp dụng: Máy lọc nước",
     "- Thông báo \"Thao tác thành công\", cửa sổ tự đóng\n"
     "- Bảng tải lại, bản ghi mới nằm dòng đầu\n"
     "- Hệ số hiện 1.50; Nhóm hàng hóa hiện \"Máy lọc nước\"\n"
     "- Người tạo, Người sửa là tài khoản đang đăng nhập; Ngày tạo là thời điểm vừa lưu"),

    ("003", "Thêm mới với nhiều nhóm hàng", "P0",
     "3 nhóm Điều hòa, Bình nóng lạnh, Quạt điện đều chưa thuộc bản ghi nào",
     "1. Bấm Thêm mới, nhập tên và hệ số\n"
     "2. Ở ô Nhóm hàng hóa áp dụng chọn lần lượt 3 nhóm\n"
     "3. Bấm Lưu",
     "Loại tỷ lệ hưởng: Hệ số điện lạnh\nHệ số: 2\nNhóm: Điều hòa; Bình nóng lạnh; Quạt điện",
     "- Lưu thành công\n"
     "- Cột Nhóm hàng hóa hiện đủ 3 nhóm, mỗi nhóm một dòng"),

    ("004", "Ô chọn nhóm hàng chỉ có nhóm đang hoạt động, xếp A-Z", "P1",
     "Nhóm \"Máy cũ\" đã ngừng hoạt động; các nhóm khác đang hoạt động",
     "1. Bấm Thêm mới\n"
     "2. Mở ô Nhóm hàng hóa áp dụng, cuộn hết danh sách\n"
     "3. Gõ \"Máy cũ\" vào ô tìm của danh sách",
     "—",
     "- Danh sách xếp theo tên A-Z\n"
     "- Không tìm thấy \"Máy cũ\"\n"
     "- Lưu ý: nhóm đã thuộc bản ghi khác VẪN có trong danh sách — chỉ bị chặn khi bấm Lưu"),

    ("005", "Bỏ chọn một nhóm trong ô nhiều lựa chọn", "P2",
     "Đã chọn 2 nhóm trong cửa sổ Thêm mới",
     "1. Bấm dấu x trên thẻ của 1 nhóm\n"
     "2. Bấm Lưu",
     "—",
     "- Thẻ nhóm bị bỏ biến mất\n"
     "- Bản ghi lưu ra chỉ có 1 nhóm còn lại"),

    ("006", "Hủy cửa sổ Thêm mới không lưu gì", "P1",
     "—",
     "1. Bấm Thêm mới, nhập đủ 3 ô\n"
     "2. Bấm Hủy\n"
     "3. Bấm Thêm mới lần nữa",
     "Loại tỷ lệ hưởng: Thử hủy",
     "- Cửa sổ đóng, bảng không có bản ghi \"Thử hủy\"\n"
     "- Lần mở lại: cả 3 ô đều trống"),

    ("007", "Mở cửa sổ Sửa hiện đúng dữ liệu cũ", "P0",
     "Bản ghi \"Hệ số điện lạnh\", Hệ số 2.00, 3 nhóm như TC_04.003",
     "1. Bấm nút Sửa (bút chì) ở dòng \"Hệ số điện lạnh\"",
     "—",
     "- Cửa sổ tiêu đề \"Chỉnh sửa tỷ lệ hưởng công khoán\"\n"
     "- Loại tỷ lệ hưởng: Hệ số điện lạnh\n"
     "- Hệ số hiện 2 (bỏ phần .00 thừa)\n"
     "- Ô nhóm hàng đã chọn sẵn đúng 3 nhóm"),

    ("008", "Sửa tên và hệ số", "P0",
     "Như TC_04.007; tài khoản QL-B (khác người tạo) đang đăng nhập",
     "1. Bấm Sửa ở dòng \"Hệ số điện lạnh\"\n"
     "2. Đổi tên và hệ số\n"
     "3. Bấm Lưu",
     "Loại tỷ lệ hưởng: Hệ số điện lạnh 2026\nHệ số: 2.25",
     "- Thông báo \"Thao tác thành công\", cửa sổ đóng\n"
     "- Dòng hiện tên mới, Hệ số 2.25\n"
     "- Người sửa = QL-B, Ngày sửa = thời điểm vừa lưu\n"
     "- Người tạo và Ngày tạo KHÔNG đổi\n"
     "- Không phát sinh bản ghi mới (tổng số mục không đổi)"),

    ("009", "Sửa danh sách nhóm — thay thế toàn bộ", "P0",
     "Bản ghi đang có 3 nhóm: Điều hòa, Bình nóng lạnh, Quạt điện; nhóm \"Máy sấy\" chưa thuộc "
     "bản ghi nào",
     "1. Bấm Sửa\n"
     "2. Bỏ Quạt điện, thêm Máy sấy\n"
     "3. Bấm Lưu\n"
     "4. Mở Thêm mới bản ghi khác, chọn Quạt điện, Lưu",
     "Nhóm sau sửa: Điều hòa; Bình nóng lạnh; Máy sấy",
     "- Cột Nhóm hàng hóa hiện đúng 3 nhóm mới, không còn Quạt điện\n"
     "- Bước 4: Quạt điện gán được cho bản ghi khác (đã được giải phóng)"),

    ("010", "Lưu lại bản ghi mà không đổi gì", "P2",
     "Bản ghi bất kỳ",
     "1. Bấm Sửa\n"
     "2. Không đổi gì, bấm Lưu",
     "—",
     "- Lưu thành công, KHÔNG báo trùng tên với chính nó, KHÔNG báo trùng nhóm với chính nó"),

    ("011", "Hủy cửa sổ Sửa giữ nguyên dữ liệu", "P1",
     "Bản ghi Hệ số 2.25",
     "1. Bấm Sửa, đổi Hệ số thành 9\n"
     "2. Bấm Hủy\n"
     "3. Bấm Sửa lại dòng đó",
     "Hệ số: 9",
     "- Bảng vẫn hiện 2.25\n"
     "- Mở lại thấy Hệ số 2.25, không phải 9"),

    ("012", "Nhóm hàng đã ngừng hoạt động bị rơi mất khi sửa", "P1",
     "Bản ghi X gán 2 nhóm: Điều hòa và \"Máy cũ\"; sau đó nhóm \"Máy cũ\" bị chuyển sang ngừng "
     "hoạt động",
     "1. Đọc cột Nhóm hàng hóa của X\n"
     "2. Bấm Sửa X, quan sát ô nhóm hàng\n"
     "3. Đổi Hệ số, bấm Lưu\n"
     "4. Đọc lại cột Nhóm hàng hóa",
     "—",
     "- Bước 1: cột vẫn hiện cả \"Máy cũ\"\n"
     "- Bước 2: ô nhóm chỉ còn Điều hòa (Máy cũ không có trong danh sách chọn)\n"
     "- Bước 4: Máy cũ bị gỡ khỏi bản ghi\n"
     "- Lưu ý: đây là hệ quả của việc chỉ liệt kê nhóm đang hoạt động; QA xác nhận với nghiệp vụ "
     "có chấp nhận không"),

    ("013", "Bấm Lưu liên tục không tạo trùng bản ghi", "P1",
     "—",
     "1. Bấm Thêm mới, nhập đủ dữ liệu hợp lệ\n"
     "2. Bấm Lưu 3 lần thật nhanh",
     "Loại tỷ lệ hưởng: Bấm nhanh",
     "- Nút Lưu chuyển sang biểu tượng xoay và bị mờ trong lúc lưu\n"
     "- Bảng chỉ có 1 bản ghi \"Bấm nhanh\""),
]

SEC_V = [
    ("001", "Màn không có thao tác trạng thái", "P2",
     "—",
     "1. Quan sát cột Hành động và thanh nút",
     "—",
     "- Không áp dụng cho feature này: không có Khóa/Mở khóa, Duyệt/Từ chối\n"
     "- Cột Hành động chỉ có Sửa và Xóa"),
]

SEC_VI = [
    ("001", "Hộp xác nhận xóa", "P0",
     "Bản ghi \"Hệ số bảo trì\"",
     "1. Bấm nút Xóa (dấu X đỏ) ở dòng \"Hệ số bảo trì\"",
     "—",
     "- Hiện hộp xác nhận tiêu đề \"Xác nhận xóa!\", nội dung \"Bạn chắc chắn muốn xóa bản ghi "
     "này?\"\n"
     "- Có 2 nút: Xác nhận (đỏ) và Hủy"),

    ("002", "Hủy xóa", "P1",
     "Như TC_06.001",
     "1. Bấm Xóa\n"
     "2. Bấm Hủy trên hộp xác nhận",
     "—",
     "- Hộp đóng, bản ghi vẫn còn, tổng số mục không đổi"),

    ("003", "Xóa thành công", "P0",
     "Bản ghi \"Hệ số bảo trì\" gán nhóm Máy bơm; công ty có 6 bản ghi",
     "1. Bấm Xóa\n"
     "2. Bấm Xác nhận",
     "—",
     "- Trang tải lại, góc màn hình báo \"Xóa tỷ lệ hưởng công khoán thành công!\"\n"
     "- Bản ghi biến mất, tổng còn 5 mục"),

    ("004", "Xóa giải phóng nhóm hàng", "P0",
     "Đã xóa bản ghi ở TC_06.003",
     "1. Bấm Thêm mới\n"
     "2. Chọn nhóm Máy bơm, nhập tên, hệ số\n"
     "3. Bấm Lưu",
     "Loại tỷ lệ hưởng: Hệ số bơm mới\nHệ số: 1.1\nNhóm: Máy bơm",
     "- Lưu thành công, KHÔNG báo \"Máy bơm đã thuộc vào 1 loại tỷ lệ hưởng\""),

    ("005", "Xóa giải phóng tên Loại tỷ lệ hưởng", "P2",
     "Đã xóa \"Hệ số bảo trì\"",
     "1. Thêm mới bản ghi tên \"Hệ số bảo trì\"",
     "Loại tỷ lệ hưởng: Hệ số bảo trì",
     "- Lưu thành công, không báo \"Đã tồn tại\""),
]

SEC_VII = [
    ("001", "Màn không có In / Xuất Excel", "P2",
     "—",
     "1. Quan sát thanh nút phía trên bảng",
     "—",
     "- Không áp dụng cho feature này: không có nút In, Xuất excel, Xuất PDF, Import excel"),
]

SEC_VIII = [
    ("001", "Bỏ trống cả 3 ô", "P0",
     "—",
     "1. Bấm Thêm mới\n"
     "2. Không nhập gì, bấm Lưu",
     "—",
     "- Thông báo vàng \"Thao tác thất bại!\"\n"
     "- Dưới cả 3 ô hiện chữ đỏ \"Bắt buộc phải nhập\"\n"
     "- Cửa sổ KHÔNG đóng, không tạo bản ghi"),

    ("002", "Loại tỷ lệ hưởng chỉ gồm khoảng trắng", "P1",
     "—",
     "1. Bấm Thêm mới, gõ 3 dấu cách vào ô Loại tỷ lệ hưởng, nhập đủ 2 ô còn lại\n"
     "2. Bấm Lưu",
     "Loại tỷ lệ hưởng: (3 dấu cách)",
     "- Báo \"Bắt buộc phải nhập\" dưới ô Loại tỷ lệ hưởng"),

    ("003", "Trùng tên trong cùng công ty", "P0",
     "Công ty đã có bản ghi \"Hệ số lắp đặt\"",
     "1. Thêm mới bản ghi cùng tên \"Hệ số lắp đặt\", nhóm hàng chưa dùng\n"
     "2. Bấm Lưu",
     "Loại tỷ lệ hưởng: Hệ số lắp đặt",
     "- Báo đỏ \"Đã tồn tại\" dưới ô Loại tỷ lệ hưởng\n"
     "- Thông báo \"Thao tác thất bại!\", cửa sổ không đóng"),

    ("004", "Trùng tên khác hoa thường / thừa dấu cách hai đầu", "P1",
     "Như TC_08.003",
     "1. Thêm mới tên \"HỆ SỐ LẮP ĐẶT\" > Lưu\n"
     "2. Sửa thành \"  Hệ số lắp đặt  \" (dấu cách hai đầu) > Lưu",
     "Loại tỷ lệ hưởng: HỆ SỐ LẮP ĐẶT\n  Hệ số lắp đặt  ",
     "- Cả 2 lần đều báo \"Đã tồn tại\""),

    ("005", "Sửa bản ghi sang tên đã có của bản ghi khác", "P0",
     "Công ty có \"HS-A\" và \"HS-B\"",
     "1. Bấm Sửa \"HS-B\"\n"
     "2. Đổi tên thành \"HS-A\", bấm Lưu",
     "Loại tỷ lệ hưởng: HS-A",
     "- Báo \"Đã tồn tại\", HS-B giữ nguyên tên cũ"),

    ("006", "Ô Hệ số không nhận chữ", "P0",
     "—",
     "1. Bấm Thêm mới\n"
     "2. Gõ \"abc\" rồi gõ \"1a2\" vào ô Hệ số",
     "Hệ số: abc\n1a2",
     "- Ô không nhận chữ cái: \"abc\" không hiện ra, \"1a2\" chỉ còn phần số hợp lệ trước đó"),

    ("007", "Hệ số tự cắt về 2 chữ số thập phân", "P0",
     "—",
     "1. Gõ \"1.256\" vào ô Hệ số\n"
     "2. Nhập đủ ô khác, Lưu",
     "Hệ số: 1.256",
     "- Khi gõ, ô chỉ giữ \"1.25\"\n"
     "- Bảng hiện 1.25"),

    ("008", "Hệ số dùng dấu phẩy", "P1",
     "—",
     "1. Gõ \"1,5\" vào ô Hệ số",
     "Hệ số: 1,5",
     "- Ô không chấp nhận dấu phẩy (giữ \"1\")\n"
     "- Lưu ý: phải dùng dấu chấm cho phần thập phân"),

    ("009", "Hệ số bằng 0 và số âm", "P1",
     "—",
     "1. Thêm mới với Hệ số 0, Lưu\n"
     "2. Thêm mới bản ghi khác với Hệ số -1.5, Lưu",
     "Hệ số: 0\n-1.5",
     "- Code hiện tại CHO LƯU cả 0 và -1.50 (không có giới hạn dưới)\n"
     "- Lưu ý: hệ số 0 hoặc âm sẽ làm hệ số hưởng của hàng thuộc nhóm đó bằng 0/âm — QA xác nhận "
     "với nghiệp vụ, nếu không chấp nhận thì ghi Failed"),

    ("010", "Hệ số vượt giới hạn lưu trữ", "P2",
     "—",
     "1. Thêm mới với Hệ số 1000000, Lưu",
     "Hệ số: 1000000",
     "- Hệ thống từ chối, báo lỗi (thông báo đỏ \"Đã có lỗi xảy ra\")\n"
     "- Không tạo bản ghi; giá trị lớn nhất lưu được là 999999.99"),

    ("011", "Bỏ trống Nhóm hàng hóa áp dụng", "P0",
     "—",
     "1. Thêm mới, nhập tên và hệ số, không chọn nhóm\n"
     "2. Bấm Lưu",
     "—",
     "- Báo \"Bắt buộc phải nhập\" dưới ô Nhóm hàng hóa áp dụng"),

    ("012", "Chọn nhóm đã thuộc bản ghi khác", "P0",
     "Nhóm \"Điều hòa\" đã thuộc bản ghi \"Hệ số điện lạnh\"",
     "1. Thêm mới bản ghi \"HS mới\", chọn nhóm Điều hòa\n"
     "2. Bấm Lưu",
     "Nhóm: Điều hòa",
     "- Báo đỏ \"Điều hòa đã thuộc vào 1 loại tỷ lệ hưởng\" dưới ô nhóm\n"
     "- Không tạo bản ghi"),

    ("013", "Chọn nhiều nhóm, trong đó vài nhóm đã bị dùng", "P1",
     "Điều hòa và Quạt điện đã thuộc bản ghi khác; Máy sấy chưa thuộc bản ghi nào",
     "1. Thêm mới, chọn lần lượt Máy sấy, Điều hòa, Quạt điện\n"
     "2. Bấm Lưu",
     "—",
     "- Báo lỗi chỉ nêu tên MỘT nhóm vi phạm đầu tiên (Điều hòa)\n"
     "- Toàn bộ bản ghi không được lưu, kể cả Máy sấy"),

    ("014", "Sửa bản ghi, thêm nhóm đang thuộc bản ghi khác", "P0",
     "Bản ghi A có nhóm Máy sấy; bản ghi B có nhóm Điều hòa",
     "1. Bấm Sửa A, thêm nhóm Điều hòa\n"
     "2. Bấm Lưu",
     "—",
     "- Báo \"Điều hòa đã thuộc vào 1 loại tỷ lệ hưởng\"\n"
     "- A và B giữ nguyên nhóm cũ"),

    ("015", "Lỗi cũ còn sót khi mở cửa sổ Sửa", "P2",
     "—",
     "1. Bấm Thêm mới, bấm Lưu khi để trống để hiện lỗi đỏ\n"
     "2. Bấm Hủy\n"
     "3. Bấm Sửa một bản ghi bất kỳ",
     "—",
     "- Cửa sổ Sửa KHÔNG còn chữ đỏ \"Bắt buộc phải nhập\" của lần trước\n"
     "- Lưu ý: theo đọc code, lỗi cũ có thể vẫn hiện cho đến khi bấm Lưu — nếu vậy ghi Failed"),

    ("016", "Tên rất dài", "P2",
     "—",
     "1. Thêm mới với tên 255 ký tự > Lưu\n"
     "2. Thêm mới với tên 256 ký tự > Lưu",
     "Loại tỷ lệ hưởng: chuỗi 255 ký tự\nchuỗi 256 ký tự",
     "- 255 ký tự: lưu thành công, bảng hiển thị không vỡ khung\n"
     "- 256 ký tự: hệ thống từ chối, không tạo bản ghi"),
]

SEC_IX = [
    ("001", "Không thấy dữ liệu công ty khác", "P0",
     "Công ty C1 có 5 bản ghi, C2 có 4 bản ghi\n"
     "Tài khoản U1 thuộc C1, U2 thuộc C2",
     "1. Đăng nhập U1, mở màn, đọc tổng\n"
     "2. Đăng nhập U2, mở màn, đọc tổng",
     "—",
     "- U1 thấy đúng 5, U2 thấy đúng 4\n"
     "- Không dòng nào lẫn sang công ty kia"),

    ("002", "Hai công ty được đặt cùng tên", "P1",
     "C1 đã có \"Hệ số lắp đặt\"",
     "1. Đăng nhập U2 (C2)\n"
     "2. Thêm mới \"Hệ số lắp đặt\" với nhóm chưa dùng ở đâu",
     "Loại tỷ lệ hưởng: Hệ số lắp đặt",
     "- Lưu thành công, không báo \"Đã tồn tại\""),

    ("003", "Nhóm hàng đã gán ở công ty khác chặn công ty mình", "P0",
     "C1 đã gán nhóm \"Điều hòa\" vào bản ghi của C1",
     "1. Đăng nhập U2 (C2)\n"
     "2. Thêm mới bản ghi, chọn nhóm Điều hòa, Lưu",
     "Nhóm: Điều hòa",
     "- Code hiện tại báo \"Điều hòa đã thuộc vào 1 loại tỷ lệ hưởng\" dù U2 KHÔNG nhìn thấy bản "
     "ghi nào chứa Điều hòa\n"
     "- Lưu ý: nếu nghiệp vụ muốn mỗi công ty khai báo riêng thì đây là lỗi, ghi Failed và báo đội "
     "phát triển"),

    ("004", "Bản ghi ghi nhận công ty của người tạo", "P0",
     "U1 thuộc C1",
     "1. U1 thêm mới bản ghi \"HS-C1\"\n"
     "2. Đăng nhập tài khoản khác thuộc C1, mở màn\n"
     "3. Đăng nhập tài khoản thuộc C2, mở màn",
     "Loại tỷ lệ hưởng: HS-C1",
     "- Bước 2: thấy HS-C1\n"
     "- Bước 3: không thấy HS-C1"),

    ("005", "Hai người cùng sửa một bản ghi", "P1",
     "Bản ghi X Hệ số 1.00; U1 và U3 cùng công ty",
     "1. U1 bấm Sửa X, chưa Lưu\n"
     "2. U3 bấm Sửa X, đổi Hệ số 2, Lưu\n"
     "3. U1 đổi Hệ số 3, Lưu\n"
     "4. Tải lại trang",
     "—",
     "- Cả 2 lần lưu đều báo thành công\n"
     "- Kết quả cuối: Hệ số 3.00, Người sửa là U1 (người lưu sau ghi đè)"),

    ("006", "Hai người cùng gán một nhóm cho 2 bản ghi khác nhau", "P2",
     "Nhóm \"Máy sấy\" chưa thuộc bản ghi nào; U1 và U3 cùng công ty",
     "1. U1 mở Thêm mới, chọn Máy sấy, chưa Lưu\n"
     "2. U3 mở Thêm mới, chọn Máy sấy, Lưu\n"
     "3. U1 bấm Lưu",
     "—",
     "- Bước 3 báo \"Máy sấy đã thuộc vào 1 loại tỷ lệ hưởng\"\n"
     "- Máy sấy chỉ thuộc bản ghi của U3"),

    ("007", "Xóa bản ghi người khác vừa xóa", "P2",
     "Bản ghi X đang hiển thị trên 2 tab của U1 và U3",
     "1. U3 xóa X thành công\n"
     "2. U1 (chưa tải lại trang) bấm Xóa X, Xác nhận",
     "—",
     "- Hệ thống báo dữ liệu không còn tồn tại, không treo trang\n"
     "- Lưu ý: theo đọc code, bước 2 có nguy cơ hiện trang lỗi — nếu vậy ghi Failed"),

    ("008", "Sửa bản ghi người khác vừa xóa", "P2",
     "Như TC_09.007",
     "1. U3 xóa X\n"
     "2. U1 (chưa tải lại) bấm Sửa X",
     "—",
     "- Hệ thống báo dữ liệu đã thay đổi; không mở cửa sổ với dữ liệu trống rồi lưu thành bản ghi mới\n"
     "- Lưu ý: theo đọc code, cửa sổ Sửa có thể mở ra TRỐNG, nhập rồi Lưu sẽ tạo bản ghi MỚI — nếu "
     "vậy ghi Failed"),
]

SEC_X = [
    ("001", "Khai báo hệ số rồi dùng ở phiếu phân công lắp đặt", "P0",
     "Nhóm \"Máy lọc nước\" chưa gán hệ số\n"
     "Có sản phẩm SP-1 thuộc nhóm Máy lọc nước, chưa khai báo hệ số riêng",
     "1. Thêm mới \"Hệ số lọc nước\", Hệ số 1.5, nhóm Máy lọc nước\n"
     "2. Lập phiếu phân công bảo hành - sửa chữa có phần Lắp đặt bàn giao chứa SP-1\n"
     "3. Đọc hệ số hưởng của SP-1 ở phần Lắp đặt bàn giao",
     "Hệ số: 1.5",
     "- Hệ số hưởng của SP-1 mặc định là 1.5"),

    ("002", "Hàng thuộc nhóm chưa gán lấy hệ số 1", "P1",
     "SP-2 thuộc nhóm \"Phụ kiện\" chưa gán vào bản ghi nào",
     "1. Lập phiếu phân công có phần Lắp đặt bàn giao chứa SP-2\n"
     "2. Đọc hệ số hưởng của SP-2",
     "—",
     "- Hệ số hưởng của SP-2 mặc định là 1"),

    ("003", "Đổi hệ số nhóm không làm đổi phiếu đã lưu hệ số", "P1",
     "Phiếu phân công ở TC_10.001 đã được lưu với hệ số 1.5 cho SP-1",
     "1. Sửa \"Hệ số lọc nước\" thành 2\n"
     "2. Mở lại phiếu phân công ở TC_10.001\n"
     "3. Lập phiếu phân công mới có SP-1",
     "Hệ số: 2",
     "- Phiếu cũ vẫn giữ 1.5\n"
     "- Phiếu mới lấy 2"),

    ("004", "Xóa hệ số nhóm, phiếu mới quay về hệ số 1", "P1",
     "Như TC_10.003",
     "1. Xóa bản ghi \"Hệ số lọc nước\"\n"
     "2. Lập phiếu phân công mới có SP-1",
     "—",
     "- Hệ số hưởng của SP-1 mặc định là 1"),

    ("005", "Vòng đời đầy đủ một bản ghi", "P0",
     "Nhóm Máy sấy, Quạt điện chưa thuộc bản ghi nào",
     "1. Thêm mới \"HS-E2E\", Hệ số 1.2, nhóm Máy sấy\n"
     "2. Lọc theo tên \"E2E\" thấy đúng 1 dòng\n"
     "3. Sửa: Hệ số 1.35, đổi nhóm thành Quạt điện\n"
     "4. Thêm mới \"HS-E2E-2\" với nhóm Máy sấy\n"
     "5. Xóa \"HS-E2E\"\n"
     "6. Thêm mới \"HS-E2E-3\" với nhóm Quạt điện",
     "—",
     "- Bước 1, 3, 4, 6 đều \"Thao tác thành công\"\n"
     "- Sau bước 3: Hệ số 1.35, Nhóm hàng hóa chỉ còn Quạt điện\n"
     "- Bước 4 lưu được vì Máy sấy đã được giải phóng ở bước 3\n"
     "- Bước 5 báo \"Xóa tỷ lệ hưởng công khoán thành công!\"\n"
     "- Bước 6 lưu được vì Quạt điện đã được giải phóng ở bước 5"),
]
