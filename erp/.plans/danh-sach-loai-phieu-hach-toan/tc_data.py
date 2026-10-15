# -*- coding: utf-8 -*-
"""Khoi mo ta + toan bo TC cho man ERP 'Danh sach loai phieu hach toan'."""

MENU = ("Mở menu trên cùng, rê chuột vào QTTT > nhóm \"Cấu hình ERP\" > bấm "
        "\"Danh sách loại phiếu hạch toán\"")

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Màn TRA CỨU danh mục các loại phiếu mà hệ thống hạch toán: mỗi dòng là một loại phiếu (vd "
     "\"PXH - Xuất bán hàng\"), thuộc một Phân loại (Đề nghị xuất, Phiếu thu…) và có đánh dấu loại "
     "đó có Hạch toán riêng hay không.\n"
     "Danh mục do hệ thống khai báo sẵn, người dùng CHỈ XEM và LỌC được; màn không có Thêm mới, Sửa, "
     "Xóa, In, Xuất Excel."),

    ("2. Đối tượng được tính / hiển thị",
     "Hiển thị toàn bộ 105 loại phiếu, chia theo 9 Phân loại:\n"
     "- Đề nghị xuất: 20 loại\n"
     "- Đề nghị nhập: 23 loại\n"
     "- Xuất hàng: 21 loại\n"
     "- Nhập hàng: 24 loại\n"
     "- Thu: 5 loại (gồm Phiếu thu, 3 loại PT - …, Phiếu báo có)\n"
     "- Chi: 8 loại (gồm Phiếu chi, 6 loại PC - …, Phiếu báo nợ)\n"
     "- Phiếu kế toán: 1 loại\n"
     "- Dịch vụ: 2 loại (Bán dịch vụ, Mua dịch vụ)\n"
     "- Khác: 1 loại (Khác thu, chi, nhập, xuất)\n"
     "Cột Hạch toán riêng: có dấu tích xanh với 94 loại, để trống với 11 loại."),

    ("3. Đối tượng bị ẩn / không tính",
     "Không có bản ghi nào bị ẩn: danh mục dùng chung, không lọc theo công ty, phòng ban hay người "
     "đăng nhập. Không có trạng thái khóa/ngừng sử dụng."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Không áp dụng — màn không có bộ lọc theo ngày và không hiển thị cột ngày."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Danh mục 1 cấp, mỗi loại phiếu thuộc đúng 1 Phân loại.\n"
     "Tên loại phiếu thể hiện quan hệ cha con bằng chữ: dòng tổng (vd \"Phiếu xuất hàng\", \"Đề nghị xuất kho\") đứng trước các dòng chi "
     "tiết có tiền tố (\"PXH - …\", \"Đề nghị - …\"). Dòng tổng thường KHÔNG có dấu Hạch toán riêng."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "Không áp dụng — màn không cộng dồn số liệu; mỗi loại phiếu hiển thị đúng một dòng."),

    ("7. Phân quyền cấp",
     "Màn KHÔNG gắn quyền riêng: mọi tài khoản đã đăng nhập ERP đều thấy mục menu và xem được toàn "
     "bộ danh mục. Chưa đăng nhập thì bị đưa về trang đăng nhập."),

    ("8. Cách tính các ô thống kê",
     "- Cột STT: đánh số liên tục theo trang, trang 2 với 10 dòng/trang bắt đầu từ 11.\n"
     "- Dòng dưới bảng \"Đang xem a đến b trong tổng số N mục\": a là dòng đầu trang, b là dòng cuối "
     "trang, N là tổng loại phiếu khớp bộ lọc (không lọc là 105)."),

    ("9. Ghi chú đọc bảng",
     "- Thứ tự dòng là thứ tự khai báo sẵn (Đề nghị xuất trước, rồi Đề nghị nhập, Xuất hàng, Nhập "
     "hàng…); riêng Phiếu báo có / Phiếu báo nợ nằm ở cuối dù thuộc Thu / Chi.\n"
     "- Không cột nào bấm sắp xếp được.\n"
     "- Ô Loại phiếu tìm gần đúng, KHÔNG phân biệt hoa thường và KHÔNG phân biệt dấu (gõ \"kiem ke\" "
     "vẫn ra \"kiểm kê\").\n"
     "- Bộ lọc tự chạy sau khoảng nửa giây ngừng gõ; điều kiện lọc được trình duyệt ghi nhớ cho lần "
     "mở sau.\n"
     "- Tên loại phiếu có vài chỗ dư dấu cách hoặc gõ sai (vd \"PXH -  Xuất bán hàng\" có 2 dấu "
     "cách, \"Đề nghị - Xuất khác - Xuât thẳng\" thiếu dấu mũ) — dư dấu cách làm lọc theo tên "
     "đầy đủ bị trượt, xem nhóm VIII."),
]

ROLE_TCS = [
    ("00", "Tài khoản bất kỳ đã đăng nhập đều xem được danh mục", "P0",
     "Tài khoản NV-A là nhân viên thường, không có quyền kế toán hay cấu hình nào",
     "1. Đăng nhập bằng NV-A\n"
     "2. " + MENU + "\n"
     "3. Đọc tổng số dưới bảng",
     "Tài khoản: NV-A",
     "- Mục menu hiển thị và mở được màn\n"
     "- Tổng ghi \"trong tổng số 105 mục\""),

    ("01", "Chưa đăng nhập không vào được màn", "P0",
     "Trình duyệt đã đăng xuất khỏi ERP",
     "1. Thử mở lại màn Danh sách loại phiếu hạch toán từ lịch sử trình duyệt",
     "—",
     "- Hệ thống đưa về trang đăng nhập\n"
     "- Không hiển thị dòng dữ liệu nào"),

    ("02", "Không tài khoản nào có nút ghi dữ liệu", "P1",
     "Tài khoản quản trị cao nhất (Ban giám đốc / quản trị hệ thống)",
     "1. Đăng nhập tài khoản quản trị, mở màn\n"
     "2. Quan sát phía trên bảng và từng dòng",
     "—",
     "- Không có nút Thêm mới, Xuất excel\n"
     "- Bảng không có cột Hành động, không có nút Sửa / Xóa"),
]

SEC_I = [
    ("001", "Mở màn từ menu QTTT", "P0",
     "Tài khoản bất kỳ đã đăng nhập",
     "1. " + MENU + "\n"
     "2. Quan sát tiêu đề trang và bảng",
     "—",
     "- Mở đúng màn, tiêu đề trang \"Danh sách loại phiếu hạch toán\"\n"
     "- Bảng tải dữ liệu, không báo lỗi"),

    ("002", "Bố cục mặc định của màn", "P0",
     "—",
     "1. Mở màn\n"
     "2. Quan sát từ trên xuống",
     "—",
     "- Phía trên bảng chỉ có nút \"Bộ lọc\"; khối lọc mặc định ĐANG THU GỌN\n"
     "- Bảng có đúng 4 cột: STT, Loại phiếu, Phân loại, Hạch toán riêng\n"
     "- Dưới bảng có dòng \"Đang xem 1 đến 10 trong tổng số 105 mục\", ô \"Xem … mục\" và nút "
     "phân trang"),

    ("003", "Màn chỉ có một lối vào", "P2",
     "—",
     "1. Rà các phân hệ trên menu trên cùng, tìm mục \"Danh sách loại phiếu hạch toán\"",
     "—",
     "- Chỉ có 1 mục menu, nằm ở QTTT > Cấu hình ERP\n"
     "- Không có chế độ xem khác: luôn hiện toàn bộ danh mục"),

    ("004", "Tải lại trang giữ nguyên bộ lọc", "P2",
     "—",
     "1. Bấm Bộ lọc, chọn Phân loại: Thu, chờ bảng lọc xong\n"
     "2. Bấm F5 tải lại trang\n"
     "3. Mở lại khối Bộ lọc",
     "Phân loại: Thu",
     "- Ô Phân loại vẫn là Thu\n"
     "- Bảng vẫn chỉ có 5 dòng"),
]

SEC_II = [
    ("001", "Mở / thu gọn khối Bộ lọc", "P1",
     "—",
     "1. Bấm nút Bộ lọc\n"
     "2. Bấm Bộ lọc lần nữa",
     "—",
     "- Lần 1: khối lọc mở ra gồm ô chọn Phân loại, ô nhập Loại phiếu và 2 nút tìm kiếm (kính lúp), "
     "làm mới (mũi tên tròn)\n"
     "- Lần 2: khối lọc thu gọn lại"),

    ("002", "Ô Phân loại có đủ 9 lựa chọn", "P0",
     "—",
     "1. Mở Bộ lọc\n"
     "2. Bấm ô Phân loại, đọc danh sách",
     "—",
     "- Đúng 9 lựa chọn theo thứ tự: Đề nghị xuất, Đề nghị nhập, Xuất hàng, Nhập hàng, Thu, Chi, "
     "Phiếu kế toán, Dịch vụ, Khác"),

    ("003", "Lọc từng Phân loại ra đúng số dòng", "P0",
     "—",
     "1. Chọn lần lượt từng Phân loại\n"
     "2. Mỗi lần đọc tổng số dưới bảng và soát cột Phân loại",
     "9 Phân loại",
     "- Đề nghị xuất: 20 · Đề nghị nhập: 23 · Xuất hàng: 21 · Nhập hàng: 24\n"
     "- Thu: 5 · Chi: 8 · Phiếu kế toán: 1 · Dịch vụ: 2 · Khác: 1\n"
     "- Mọi dòng có cột Phân loại đúng giá trị đang lọc\n"
     "- Tổng 9 lần lọc cộng lại = 105"),

    ("004", "Phân loại Thu / Chi gồm cả phiếu báo có / báo nợ", "P1",
     "—",
     "1. Lọc Phân loại: Thu, đọc danh sách\n"
     "2. Lọc Phân loại: Chi, đọc danh sách",
     "Phân loại: Thu\nChi",
     "- Thu gồm: Phiếu thu, PT - Thu bán hàng, PT - Thu nhà cung cấp, PT - Thu khác, Phiếu báo có\n"
     "- Chi gồm: Phiếu chi, PC - Chi trả lại khách hàng, PC - Chi trả nhà cung cấp, PC - Chi thưởng "
     "NVKD, PC - Chi thu nhập nhân viên, PC - Chi thưởng thực hiện hợp đồng, PC - Chi khác, Phiếu "
     "báo nợ"),

    ("005", "Lọc theo Loại phiếu — tìm gần đúng", "P0",
     "—",
     "1. Mở Bộ lọc\n"
     "2. Gõ \"kiểm kê\" vào ô Loại phiếu, ngừng gõ chờ khoảng 1 giây",
     "Loại phiếu: kiểm kê",
     "- Bảng tự lọc, không cần bấm nút tìm\n"
     "- Còn đúng 2 dòng: \"PXH - Xuất điều chỉnh kiểm kê\", \"PNH - Nhập điều chỉnh kiểm kê\""),

    ("006", "Lọc Loại phiếu theo tiền tố", "P1",
     "—",
     "1. Gõ \"PT -\" vào ô Loại phiếu\n"
     "2. Xóa, gõ \"PC -\"",
     "Loại phiếu: PT -\nPC -",
     "- \"PT -\": 3 dòng PT - Thu bán hàng / Thu nhà cung cấp / Thu khác\n"
     "- \"PC -\": 6 dòng PC - …"),

    ("007", "Lọc không phân biệt hoa thường", "P2",
     "—",
     "1. Gõ \"PHIẾU KẾ TOÁN\" vào ô Loại phiếu",
     "Loại phiếu: PHIẾU KẾ TOÁN",
     "- Hiện dòng \"Phiếu kế toán\""),

    ("008", "Kết hợp Phân loại và Loại phiếu", "P0",
     "—",
     "1. Chọn Phân loại: Xuất hàng\n"
     "2. Gõ \"Xuất thẳng\" vào ô Loại phiếu",
     "Phân loại: Xuất hàng\nLoại phiếu: Xuất thẳng",
     "- Chỉ còn các dòng PXH có đuôi \"- Xuất thẳng\" (8 dòng)\n"
     "- Không lẫn dòng \"Đề nghị - … - Xuất thẳng\" của Phân loại Đề nghị xuất"),

    ("009", "Kết hợp lọc không có kết quả", "P1",
     "—",
     "1. Chọn Phân loại: Thu\n"
     "2. Gõ \"Nhập\" vào ô Loại phiếu",
     "Phân loại: Thu\nLoại phiếu: Nhập",
     "- Bảng hiện \"Không có dữ liệu\", tổng 0 mục, không báo lỗi"),

    ("010", "Bỏ chọn Phân loại quay về toàn bộ", "P0",
     "Đang lọc Phân loại: Chi",
     "1. Ở ô Phân loại chọn lại dòng trống \"Phân loại\"",
     "—",
     "- Bảng hiện lại 105 mục"),

    ("011", "Nút làm mới xóa sạch điều kiện lọc", "P1",
     "Đang lọc như TC_02.008",
     "1. Bấm nút làm mới (mũi tên tròn)",
     "—",
     "- Ô Phân loại và Loại phiếu trở về trống\n"
     "- Bảng hiện lại 105 mục, về trang 1"),
]

SEC_III = [
    ("001", "Thứ tự mặc định theo thứ tự khai báo", "P0",
     "—",
     "1. Mở màn, đọc 3 dòng đầu trang 1\n"
     "2. Sang trang cuối, đọc các dòng cuối",
     "—",
     "- 3 dòng đầu: Đề nghị xuất kho, Đề nghị - Xuất bán hàng, Đề nghị - Xuất bán hàng - Xuất thẳng\n"
     "- Các dòng cuối theo thứ tự: Phiếu báo có, Phiếu báo nợ, Phiếu kế toán, Bán dịch vụ, Mua dịch "
     "vụ, Khác thu, chi, nhập, xuất"),

    ("002", "Cột Phân loại hiển thị bằng chữ", "P0",
     "—",
     "1. Rà cột Phân loại trên vài trang",
     "—",
     "- Luôn hiện tên phân loại (vd \"Đề nghị xuất\", \"Nhập hàng\"), không hiện số\n"
     "- Không có ô Phân loại nào trống"),

    ("003", "Cột Hạch toán riêng", "P0",
     "—",
     "1. Lọc Phân loại: Nhập hàng, đọc cột Hạch toán riêng\n"
     "2. Lọc Phân loại: Dịch vụ, đọc cột Hạch toán riêng",
     "—",
     "- Nhập hàng: dòng \"Phiếu nhập hàng\" để trống, 23 dòng \"PNH - …\" có dấu tích xanh\n"
     "- Dịch vụ: cả 2 dòng để trống"),

    ("004", "Đếm số loại có Hạch toán riêng", "P1",
     "—",
     "1. Chọn hiển thị 100 mục/trang\n"
     "2. Đếm số dòng có dấu tích ở trang 1 và trang 2",
     "Số dòng: 100",
     "- Tổng 94 dòng có dấu tích, 11 dòng để trống\n"
     "- 11 dòng trống: Đề nghị nhập kho, Phiếu xuất hàng, Phiếu nhập hàng, Phiếu thu, Phiếu chi, "
     "Phiếu báo có, Phiếu báo nợ, Phiếu kế toán, Bán dịch vụ, Mua dịch vụ, Khác thu, chi, nhập, xuất\n"
     "- Lưu ý: \"Đề nghị xuất kho\" (dòng tổng của Đề nghị xuất) LẠI có dấu tích, khác với các dòng "
     "tổng còn lại — QA xác nhận với kế toán"),

    ("005", "Không cột nào sắp xếp được", "P2",
     "—",
     "1. Bấm tiêu đề lần lượt 4 cột",
     "—",
     "- Không có mũi tên sắp xếp, thứ tự dòng không đổi"),

    ("006", "Phân trang mặc định 10 dòng", "P0",
     "—",
     "1. Mở màn, đọc dòng dưới bảng\n"
     "2. Bấm sang trang cuối (trang 11)",
     "—",
     "- Trang 1: \"Đang xem 1 đến 10 trong tổng số 105 mục\"\n"
     "- Có 11 trang; trang 11 có 5 dòng, STT 101–105"),

    ("007", "Đổi số dòng mỗi trang", "P1",
     "—",
     "1. Ở ô \"Xem … mục\" lần lượt chọn 25, 50, 100",
     "Số dòng: 25\n50\n100",
     "- 25: 5 trang · 50: 3 trang · 100: 2 trang (trang 2 có 5 dòng)\n"
     "- STT nối tiếp đúng giữa các trang"),

    ("008", "Phân trang khi đang lọc", "P0",
     "Đang ở trang 3 khi chưa lọc",
     "1. Chọn Phân loại: Thu",
     "—",
     "- Bảng quay về trang 1, chỉ còn 1 trang với 5 dòng, STT 1–5"),
]

SEC_IV = [
    ("001", "Màn không có Thêm mới / Sửa / Xem chi tiết", "P1",
     "—",
     "1. Quan sát thanh nút và các dòng\n"
     "2. Bấm vào tên một loại phiếu",
     "—",
     "- Không áp dụng cho feature này: không có nút Thêm mới, không có nút Sửa\n"
     "- Bấm vào tên loại phiếu không mở trang nào"),
]

SEC_V = [
    ("001", "Màn không có thao tác trạng thái", "P2",
     "—",
     "1. Quan sát bảng",
     "—",
     "- Không áp dụng cho feature này: không có Khóa/Mở khóa, Duyệt/Từ chối"),
]

SEC_VI = [
    ("001", "Màn không có Xóa", "P2",
     "—",
     "1. Quan sát bảng",
     "—",
     "- Không áp dụng cho feature này: không có nút Xóa"),
]

SEC_VII = [
    ("001", "Màn không có In / Xuất Excel", "P2",
     "—",
     "1. Quan sát thanh nút phía trên bảng",
     "—",
     "- Không áp dụng cho feature này: không có nút In, Xuất excel, Xuất PDF"),
]

SEC_VIII = [
    ("001", "Ô Loại phiếu chỉ gồm khoảng trắng", "P2",
     "—",
     "1. Gõ 3 dấu cách vào ô Loại phiếu",
     "Loại phiếu: (3 dấu cách)",
     "- Bảng vẫn hiện 105 mục (coi như không lọc), không báo lỗi"),

    ("002", "Ký tự đặc biệt trong ô Loại phiếu", "P2",
     "—",
     "1. Gõ lần lượt: % , _ , ' , \" vào ô Loại phiếu",
     "Loại phiếu: %\n_\n'\n\"",
     "- Bảng tải bình thường, không báo lỗi\n"
     "- Lưu ý: gõ % hoặc _ có thể hiện TẤT CẢ 105 mục (ký tự đóng vai trò đại diện khi tìm)"),

    ("003", "Lọc theo tên có dư dấu cách", "P1",
     "—",
     "1. Gõ \"PXH - Xuất bán hàng\" (1 dấu cách sau gạch) vào ô Loại phiếu\n"
     "2. Gõ \"Xuất bán hàng\"",
     "Loại phiếu: PXH - Xuất bán hàng\nXuất bán hàng",
     "- Bước 1: KHÔNG ra 2 dòng PXH bán hàng vì tên lưu có 2 dấu cách sau gạch (\"PXH -  Xuất bán "
     "hàng\")\n"
     "- Bước 2: ra đủ các dòng Đề nghị và PXH có chữ \"Xuất bán hàng\"\n"
     "- Lưu ý: lỗi dữ liệu tên, báo đội phát triển chuẩn hóa nếu cần"),

    ("004", "Lọc theo tên có lỗi gõ", "P2",
     "—",
     "1. Chọn Phân loại: Đề nghị xuất\n"
     "2. Gõ \"Xuất thẳng\" vào ô Loại phiếu, đếm số dòng",
     "Loại phiếu: Xuất thẳng",
     "- Ra 8 dòng, CÓ CẢ dòng \"Đề nghị - Xuất khác - Xuât thẳng\" dù tên gõ thiếu dấu mũ\n"
     "- Lý do: ô Loại phiếu tìm KHÔNG phân biệt dấu"),

    ("005", "Lọc không phân biệt dấu", "P0",
     "—",
     "1. Gõ \"kiem ke\" (không dấu) vào ô Loại phiếu",
     "Loại phiếu: kiem ke",
     "- Vẫn ra 2 dòng điều chỉnh kiểm kê như TC_02.005"),

    ("006", "Dán chuỗi rất dài", "P2",
     "—",
     "1. Dán chuỗi 300 ký tự vào ô Loại phiếu",
     "Loại phiếu: chuỗi 300 ký tự",
     "- Bảng hiện \"Không có dữ liệu\", không treo, không báo lỗi"),
]

SEC_IX = [
    ("001", "Danh mục giống nhau ở mọi công ty", "P0",
     "Tài khoản U1 thuộc công ty C1, U2 thuộc công ty C2",
     "1. Đăng nhập U1, mở màn, đọc tổng và 10 dòng đầu\n"
     "2. Đăng nhập U2, làm tương tự",
     "—",
     "- Cả 2 đều thấy 105 mục, cùng thứ tự, cùng dấu Hạch toán riêng"),

    ("002", "Bộ lọc ghi nhớ riêng theo trình duyệt", "P2",
     "U1 đã lọc Phân loại: Thu trên máy 1",
     "1. U1 đăng nhập trên máy 2 (hoặc trình duyệt khác), mở màn",
     "—",
     "- Máy 2 không mang bộ lọc của máy 1: hiện đủ 105 mục"),

    ("003", "Hai người cùng xem không ảnh hưởng nhau", "P2",
     "U1 và U2 cùng mở màn",
     "1. U1 lọc Phân loại: Chi\n"
     "2. U2 tải lại trang",
     "—",
     "- U2 vẫn thấy 105 mục, không bị ảnh hưởng bộ lọc của U1"),
]

SEC_X = [
    ("001", "Tra cứu loại phiếu trước khi đối chiếu hạch toán", "P0",
     "Kế toán cần biết \"PNH - Nhập điều chỉnh kiểm kê\" có hạch toán riêng không",
     "1. " + MENU + "\n"
     "2. Bấm Bộ lọc, chọn Phân loại: Nhập hàng\n"
     "3. Gõ \"kiểm kê\" vào ô Loại phiếu\n"
     "4. Đọc cột Hạch toán riêng",
     "Phân loại: Nhập hàng\nLoại phiếu: kiểm kê",
     "- Còn đúng 1 dòng \"PNH - Nhập điều chỉnh kiểm kê\"\n"
     "- Cột Hạch toán riêng có dấu tích xanh"),

    ("002", "Lọc, làm mới rồi lọc lại liên tục", "P1",
     "—",
     "1. Lọc Phân loại: Dịch vụ (2 mục)\n"
     "2. Bấm làm mới (105 mục)\n"
     "3. Gõ \"Phiếu\" vào ô Loại phiếu\n"
     "4. Chọn thêm Phân loại: Chi",
     "—",
     "- Bước 1: 2 mục · Bước 2: 105 mục\n"
     "- Bước 4: chỉ còn Phiếu chi và Phiếu báo nợ\n"
     "- Không lần nào báo lỗi hay giữ dữ liệu của lần lọc trước"),
]
