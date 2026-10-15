# -*- coding: utf-8 -*-
"""Khoi mo ta + toan bo TC cho man ERP 'Cau hinh chan luong hang qua han'."""

MENU = ("Mở menu trên cùng, rê chuột vào QTTT > nhóm \"Cấu hình ERP\" > bấm "
        "\"Cấu hình chặn luồng hàng quá hạn\"")

TP = "CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT"
HP = "CN HẢI PHÒNG - CÔNG TY CP CÔNG NGHỆ THIẾT BỊ TÂN PHÁT"

QH_GIU = ("nhân viên còn hàng giữ (số lượng giữ lớn hơn 0) có ngày hết hạn giữ TRƯỚC hôm nay")
QH_MUON = ("nhân viên có phiếu yêu cầu xuất mượn do chính mình lập, đã mượn, ngày hẹn trả TRƯỚC hôm "
           "nay và chưa trả hết")
QH_NXT = ("nhân viên còn hàng nhập thẳng chưa xuất hết, đã quá số ngày ở ô \"Hạn xuất hàng nhập thẳng "
          "(Số ngày)\" trong quy chế công ty")

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Cấu hình, RIÊNG CHO TỪNG CÔNG TY, những thao tác nào bị CHẶN khi có hàng quá hạn.\n"
     "Màn có 2 tab:\n"
     "- \"1. Chặn nhân viên\": chặn chính người đang thao tác nếu BẢN THÂN họ có hàng mượn / hàng "
     "giữ / hàng nhập thẳng quá hạn. 21 ô tích chia 3 nhóm.\n"
     "- \"2. Chặn trưởng phòng duyệt\": chặn trưởng phòng duyệt/tạo phiếu nếu PHÒNG BAN họ quản lý "
     "có nhân viên quá hạn bất kỳ loại nào. 31 ô tích, gồm cả thao tác bên ERP và bên HRM.\n"
     "Mỗi lần Lưu có thay đổi sẽ ghi một dòng vào bảng Lịch sử chỉnh sửa ở cuối trang."),

    ("2. Đối tượng được tính / hiển thị",
     "Mỗi tab có một thanh tab con cho từng công ty đang hoạt động (5 công ty), xếp A-Z theo tên; "
     "công ty đầu tiên mở sẵn.\n"
     "Tab 1 — 3 nhóm, mỗi nhóm là một loại quá hạn:\n"
     "- Hàng mượn quá hạn (6 ô): Lập báo giá, Lập hợp đồng, Lập yêu cầu xuất hàng, Lập yêu cầu nhập "
     "hàng, Cập nhật hàng hóa, Duyệt hàng tạm.\n"
     "- Hàng giữ quá hạn (6 ô): giống nhóm trên.\n"
     "- Hàng nhập thẳng quá hạn (9 ô): 6 ô như trên + Lập yêu cầu xuất giữ, Gia hạn hàng giữ, Điều "
     "chuyển hàng giữ.\n"
     "Tab 2 — 31 ô, có dòng chú thích nghiêng phía trên và 2 liên kết \"Tích tất cả | Bỏ tích tất "
     "cả\".\n"
     "Định nghĩa quá hạn:\n"
     "- Hàng giữ quá hạn: " + QH_GIU + ".\n"
     "- Hàng mượn quá hạn: " + QH_MUON + ".\n"
     "- Hàng nhập thẳng quá hạn: " + QH_NXT + "."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Công ty ngừng hoạt động: không có tab con.\n"
     "- Tài khoản Super Admin KHÔNG BAO GIỜ bị chặn, dù cấu hình thế nào.\n"
     "- Hàng giữ / hàng mượn đã trả hết, hoặc còn trong hạn: không tính.\n"
     "- Tab 1, Lập yêu cầu xuất hàng: KHÔNG chặn nếu phiếu tích \"Xuất thẳng\", hoặc nếu mọi hàng "
     "trong phiếu đều là hàng giữ quá hạn của chính người lập (để giải phóng hàng giữ).\n"
     "- Tab 1, nhóm Hàng mượn, Lập yêu cầu nhập hàng: KHÔNG chặn phiếu loại \"Mượn trả lại\" (để "
     "trả hàng mượn).\n"
     "- Bảng lịch sử chỉ hiện 50 lần sửa gần nhất."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Không có bộ lọc. Mốc thời gian dùng khi xét quá hạn là NGÀY HÔM NAY:\n"
     "- Hàng giữ: so ngày hết hạn giữ.\n"
     "- Hàng mượn: so ngày hẹn trả.\n"
     "- Hàng nhập thẳng: ngày nhập + số ngày \"Hạn xuất hàng nhập thẳng\" của công ty."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Tab chính (Chặn nhân viên / Chặn trưởng phòng duyệt) > tab con công ty > (tab 1) nhóm loại "
     "quá hạn > ô tích thao tác.\n"
     "Tên nhóm ở tab 1 chuyển XANH và hiện số ô đang tích của nhóm khi có ít nhất 1 ô được tích.\n"
     "Trưởng phòng = người được gán quản lý phòng ban trong công ty của mình; phòng ban được xét "
     "gồm TẤT CẢ nhân viên thuộc các phòng đó, KỂ CẢ chính trưởng phòng."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Tick của công ty nào chỉ áp cho nhân viên/trưởng phòng THUỘC công ty đó (theo hồ sơ nhân "
     "viên, không theo công ty của phiếu).\n"
     "- Tab 1: khi người dùng dính nhiều loại quá hạn, hệ thống xét lần lượt Hàng giữ > Hàng mượn > "
     "Hàng nhập thẳng và chỉ báo MỘT thông báo của loại đầu tiên bị chặn.\n"
     "- Tab 2: không phân biệt nhóm; chỉ cần phòng có nhân viên quá hạn BẤT KỲ loại nào là chặn.\n"
     "- Một lần Lưu sinh MỘT dòng lịch sử, gộp mọi thay đổi của mọi công ty, mỗi thay đổi một dòng; "
     "Lưu mà không đổi gì thì không sinh dòng."),

    ("7. Phân quyền cấp",
     "Vào màn và Lưu cần quyền \"Cấu hình hệ thống\". Tài khoản Super Admin luôn vào được.\n"
     "Lưu ý: tại thời điểm viết tài liệu, môi trường gộp dữ liệu KHÔNG có quyền nào tên \"Cấu hình "
     "hệ thống\" cho ERP, nên trên thực tế chỉ Super Admin vào được; mục menu vẫn hiện với mọi người "
     "nhưng bấm vào ra trang \"Không có quyền truy cập\".\n"
     "Có một quyền khác tên \"Cấu hình chặn luồng hàng quá hạn\" nhưng màn ERP KHÔNG dùng quyền này."),

    ("8. Cách tính các ô thống kê",
     "- Số trong vòng tròn xám cạnh tên nhóm (tab 1) = số ô đang tích trong nhóm của công ty đang "
     "xem; tích/bỏ tích là số đổi ngay, chưa cần Lưu.\n"
     "- Cột STT bảng lịch sử: 1 là lần sửa mới nhất."),

    ("9. Ghi chú đọc bảng",
     "- Thông báo khi bị chặn ở tab 1: \"Có hàng giữ quá hạn!\" / \"Có hàng mượn quá hạn!\" / "
     "\"Có hàng nhập thẳng quá hạn!\" (thông báo vàng góc màn hình).\n"
     "- Khi bị chặn ở tab 2: KHÔNG hiện chữ thông báo, mà mở cửa sổ \"Phòng ban bạn quản lý có NV "
     "hàng quá hạn như sau:\" liệt kê nhân viên quá hạn.\n"
     "- Nếu công ty để trống / 0 ở ô \"Hạn xuất hàng nhập thẳng (Số ngày)\": tab 1 coi MỌI hàng nhập "
     "thẳng còn tồn là quá hạn; tab 2 lại bỏ qua loại này — hai tab xét khác nhau.\n"
     "- Không phải ô nào ở tab 2 cũng có hiệu lực: xem nhóm V để biết thao tác nào được chặn ở ERP, "
     "ở HRM, và những ô hiện CHƯA chặn ở đâu cả.\n"
     "- Nút Hủy KHÔNG hoàn tác ô đã tích mà đưa về trang chủ (thay đổi chưa Lưu bị bỏ)."),
]

ROLE_TCS = [
    ("00", "Tài khoản Super Admin vào được và Lưu được", "P0",
     "Tài khoản SA có vai trò Super Admin",
     "1. Đăng nhập SA\n"
     "2. " + MENU + "\n"
     "3. Tích 1 ô bất kỳ, bấm Lưu",
     "Tài khoản: SA",
     "- Mở được màn, tiêu đề \"Cấu hình chặn luồng hàng quá hạn\"\n"
     "- Lưu báo \"Thao tác thành công!\""),

    ("01", "Tài khoản có quyền Cấu hình hệ thống vào được", "P0",
     "Tài khoản KT-A (không phải Super Admin) thuộc chức vụ được cấp quyền \"Cấu hình hệ thống\" "
     "trong công ty của KT-A",
     "1. Đăng nhập KT-A, mở màn theo menu\n"
     "2. Tích 1 ô, bấm Lưu",
     "Tài khoản: KT-A",
     "- Mở được màn và Lưu thành công\n"
     "- Lưu ý: nếu hệ thống không có quyền tên \"Cấu hình hệ thống\" để cấp thì ghi Không thực hiện "
     "được và báo đội phát triển (xem mục 7)"),

    ("02", "Tài khoản không có quyền thấy menu nhưng bị chặn khi vào", "P0",
     "Tài khoản NV-B là nhân viên thường, không có quyền \"Cấu hình hệ thống\"",
     "1. Đăng nhập NV-B\n"
     "2. " + MENU,
     "Tài khoản: NV-B",
     "- Mục menu VẪN hiển thị\n"
     "- Bấm vào ra trang \"Không có quyền truy cập\" với dòng \"Bạn không có quyền truy cập vào chức "
     "năng này !\"\n"
     "- Không thấy bất kỳ ô tích nào"),

    ("03", "Quyền Cấu hình chặn luồng hàng quá hạn không mở được màn ERP", "P1",
     "Tài khoản NV-C chỉ được cấp quyền \"Cấu hình chặn luồng hàng quá hạn\"",
     "1. Đăng nhập NV-C vào ERP\n"
     "2. " + MENU,
     "Tài khoản: NV-C",
     "- Ra trang \"Không có quyền truy cập\"\n"
     "- Lưu ý: quyền này dành cho màn tương ứng bên HRM; QA xác nhận với nghiệp vụ có cần mở cho "
     "màn ERP không"),

    ("04", "Mất quyền giữa chừng không Lưu được", "P1",
     "KT-A đang mở màn; quản trị gỡ quyền \"Cấu hình hệ thống\" của KT-A",
     "1. KT-A (chưa tải lại trang) tích 1 ô, bấm Lưu",
     "—",
     "- Hệ thống từ chối, thông báo đỏ \"Đã có lỗi xảy ra\"\n"
     "- Không sinh dòng lịch sử, cấu hình không đổi"),

    ("05", "Super Admin không bao giờ bị chặn", "P0",
     "Tài khoản SA có hàng giữ quá hạn; công ty của SA tích \"Hàng giữ quá hạn - Lập báo giá\"; SA "
     "quản lý phòng có nhân viên quá hạn, tab 2 tích \"Duyệt hợp đồng bán\"",
     "1. SA lập báo giá, Lưu\n"
     "2. SA duyệt một hợp đồng bán chờ trưởng phòng duyệt",
     "—",
     "- Cả hai thao tác thành công, không có thông báo hay cửa sổ chặn"),
]

SEC_I = [
    ("001", "Mở màn từ menu QTTT", "P0",
     "Tài khoản Super Admin",
     "1. " + MENU,
     "—",
     "- Tiêu đề trang \"Cấu hình chặn luồng hàng quá hạn\"\n"
     "- Khung trên tiêu đề \"Chi tiết chặn (*)\", góc phải có nút \"Ẩn tất cả\"\n"
     "- Có 2 tab \"1. Chặn nhân viên\" (đang chọn) và \"2. Chặn trưởng phòng duyệt\"\n"
     "- Chân khung có nút Lưu (xanh lá) và Hủy (đỏ)\n"
     "- Bên dưới có khung \"Lịch sử chỉnh sửa\""),

    ("002", "Tab con công ty", "P0",
     "Hệ thống có 5 công ty đang hoạt động",
     "1. Mở màn, đọc thanh tab con ở tab 1\n"
     "2. Chuyển sang tab 2, đọc thanh tab con",
     "—",
     "- Cả 2 tab đều có 5 tab con, xếp A-Z: " + HP + " đứng đầu và đang mở sẵn\n"
     "- Không có tab cho công ty đã ngừng hoạt động"),

    ("003", "Bố cục tab 1 với 3 nhóm", "P0",
     "—",
     "1. Ở tab 1, mở tab con " + TP + "\n"
     "2. Đọc tên nhóm và các ô tích",
     "—",
     "- 3 nhóm: Hàng mượn quá hạn (6 ô), Hàng giữ quá hạn (6 ô), Hàng nhập thẳng quá hạn (9 ô)\n"
     "- Nhóm Hàng nhập thẳng có thêm 3 ô: Lập yêu cầu xuất giữ, Gia hạn hàng giữ, Điều chuyển hàng "
     "giữ\n"
     "- Màn hình rộng: 3 nhóm xếp 3 cột; thu nhỏ cửa sổ: 2 cột rồi 1 cột"),

    ("004", "Bố cục tab 2", "P0",
     "—",
     "1. Bấm tab \"2. Chặn trưởng phòng duyệt\"\n"
     "2. Đọc toàn bộ nội dung",
     "—",
     "- Dòng nghiêng: \"Chặn trưởng phòng duyệt các phiếu dưới đây nếu phòng ban do user quản lý có "
     "nhân viên quá hạn hàng mượn / hàng giữ / hàng NXT\"\n"
     "- Có liên kết \"Tích tất cả | Bỏ tích tất cả\"\n"
     "- 31 ô xếp 2 cột, từ \"Duyệt yêu cầu xuất giữ\" đến \"Duyệt kết quả công tác trên HRM\""),

    ("005", "Ô tích hiện đúng cấu hình đã lưu", "P0",
     "Cấu hình đang lưu của " + TP + ": tab 1 tích 16 ô (Hàng mượn đủ 6; Hàng giữ: Lập yêu cầu xuất "
     "hàng, Lập yêu cầu nhập hàng, Cập nhật hàng hóa, Duyệt hàng tạm; Hàng nhập thẳng: Lập yêu cầu "
     "xuất hàng, Lập yêu cầu nhập hàng, Lập yêu cầu xuất giữ, Điều chuyển hàng giữ, Cập nhật hàng "
     "hóa, Duyệt hàng tạm); tab 2 không tích ô nào",
     "1. Mở tab con " + TP + " ở tab 1, đọc ô tích và số cạnh tên nhóm\n"
     "2. Mở tab con này ở tab 2",
     "—",
     "- Số cạnh nhóm: Hàng mượn 6, Hàng giữ 4, Hàng nhập thẳng 6; cả 3 tên nhóm màu xanh\n"
     "- Ô tích khớp đúng danh sách ở tiền điều kiện\n"
     "- Tab 2: không ô nào được tích\n"
     "- Lưu ý: số liệu lấy theo dữ liệu môi trường thử ngày 14/10/2026, đối chiếu lại nếu dữ liệu đã "
     "đổi"),

    ("006", "Nhóm không có ô nào tích", "P2",
     "Công ty X không tích ô nào trong nhóm Hàng giữ quá hạn",
     "1. Mở tab con công ty X ở tab 1",
     "—",
     "- Tên nhóm Hàng giữ quá hạn màu đen, KHÔNG có số bên cạnh"),
]

SEC_II = [
    ("001", "Chuyển giữa 2 tab chính giữ nguyên ô đã tích chưa Lưu", "P1",
     "—",
     "1. Ở tab 1, tích thêm 1 ô\n"
     "2. Chuyển sang tab 2 rồi quay lại tab 1",
     "—",
     "- Ô vừa tích vẫn còn tích\n"
     "- Chưa sinh dòng lịch sử"),

    ("002", "Chuyển tab con công ty", "P1",
     "—",
     "1. Ở tab 1, tích 1 ô ở công ty A\n"
     "2. Mở tab con công ty B, rồi quay lại A",
     "—",
     "- Ô tích của B hiện theo cấu hình riêng của B, không bị ảnh hưởng\n"
     "- Quay lại A vẫn thấy ô vừa tích"),

    ("003", "Nút Ẩn tất cả / Hiện tất cả", "P1",
     "Đang ở tab 1, các nhóm đang mở",
     "1. Bấm \"Ẩn tất cả\"\n"
     "2. Bấm nút lần nữa",
     "—",
     "- Lần 1: mọi nhóm thu gọn chỉ còn tên nhóm, chữ trên nút đổi thành \"Hiện tất cả\"\n"
     "- Lần 2: mọi nhóm mở lại, nút về \"Ẩn tất cả\""),

    ("004", "Thu gọn một nhóm riêng lẻ", "P2",
     "—",
     "1. Bấm vào tên nhóm Hàng giữ quá hạn\n"
     "2. Bấm lần nữa",
     "—",
     "- Lần 1: chỉ nhóm này thu gọn, mũi tên bên phải đổi hướng\n"
     "- Lần 2: mở lại"),

    ("005", "Bấm vào chữ của ô tích", "P2",
     "—",
     "1. Bấm vào chữ \"Lập báo giá\" (không bấm vào ô vuông) trong nhóm Hàng mượn",
     "—",
     "- Ô tương ứng đổi trạng thái tích\n"
     "- Không làm đổi ô \"Lập báo giá\" của nhóm khác hay công ty khác"),
]

SEC_III = [
    ("001", "Bảng lịch sử khi chưa có thay đổi nào", "P2",
     "Môi trường chưa từng Lưu thay đổi cấu hình",
     "1. Mở màn, cuộn xuống khung Lịch sử chỉnh sửa",
     "—",
     "- Bảng có 4 cột: STT, Thời gian, Nội dung chỉnh sửa, Người cập nhật\n"
     "- Một dòng \"Chưa có lịch sử\""),

    ("002", "Lưu tích một ô sinh dòng lịch sử", "P0",
     "Ô \"Hàng giữ quá hạn - Lập báo giá\" của " + TP + " đang bỏ tích; người lưu là KT-A thuộc phòng "
     "mã KT",
     "1. Tích ô đó, bấm Lưu\n"
     "2. Sau khi trang tự tải lại, đọc dòng đầu bảng lịch sử",
     "—",
     "- STT 1, Thời gian = lúc lưu dạng ngày/tháng/năm giờ:phút\n"
     "- Nội dung: \"[" + TP + "] Tích: Hàng giữ quá hạn - Lập báo giá\"\n"
     "- Người cập nhật: \"KT - <họ tên KT-A>\""),

    ("003", "Bỏ tích ghi chữ Bỏ tích", "P0",
     "Như TC_03.002 sau khi đã lưu",
     "1. Bỏ tích ô đó, bấm Lưu",
     "—",
     "- Dòng mới nhất: \"[" + TP + "] Bỏ tích: Hàng giữ quá hạn - Lập báo giá\"\n"
     "- Dòng \"Tích\" của lần trước vẫn còn ở vị trí STT 2"),

    ("004", "Nhiều thay đổi nhiều công ty trong một lần Lưu", "P0",
     "—",
     "1. Tab 1, công ty A: tích \"Hàng mượn quá hạn - Lập hợp đồng\"\n"
     "2. Tab 2, công ty B: tích \"Duyệt hợp đồng bán\"\n"
     "3. Bấm Lưu",
     "—",
     "- Chỉ sinh MỘT dòng lịch sử\n"
     "- Ô nội dung có 2 dòng: \"[A] Tích: Hàng mượn quá hạn - Lập hợp đồng\" và \"[B] Tích: Chặn "
     "trưởng phòng duyệt - Duyệt hợp đồng bán\""),

    ("005", "Lưu không đổi gì không sinh lịch sử", "P1",
     "—",
     "1. Mở màn, không tích gì, bấm Lưu\n"
     "2. Tích 1 ô rồi bỏ tích lại chính ô đó, bấm Lưu",
     "—",
     "- Cả 2 lần đều báo \"Thao tác thành công!\"\n"
     "- Bảng lịch sử KHÔNG có dòng mới"),

    ("006", "Chỉ hiện 50 lần sửa gần nhất", "P2",
     "Đã có 52 lần Lưu có thay đổi",
     "1. Đếm số dòng bảng lịch sử",
     "—",
     "- Đúng 50 dòng, dòng đầu là lần sửa mới nhất\n"
     "- 2 lần sửa cũ nhất không hiện; không có phân trang"),

    ("007", "Tích tất cả ở tab 2 ghi đủ từng ô", "P1",
     "Công ty A ở tab 2 đang tích 2 ô",
     "1. Bấm \"Tích tất cả\" ở công ty A, Lưu",
     "—",
     "- Dòng lịch sử mới có 29 dòng \"[A] Tích: Chặn trưởng phòng duyệt - …\"\n"
     "- 2 ô đã tích từ trước KHÔNG được ghi lại"),
]

SEC_IV = [
    ("001", "Tích và Lưu thành công", "P0",
     "—",
     "1. Ở tab 1 công ty A, tích \"Hàng nhập thẳng quá hạn - Gia hạn hàng giữ\"\n"
     "2. Bấm Lưu",
     "—",
     "- Nút Lưu hiện biểu tượng xoay và bị mờ trong lúc lưu\n"
     "- Thông báo xanh \"Thao tác thành công!\"\n"
     "- Khoảng 1 giây sau trang tự tải lại; ô vẫn tích, số cạnh nhóm tăng 1"),

    ("002", "Bỏ tích và Lưu", "P0",
     "Ô ở TC_04.001 đang tích",
     "1. Bỏ tích, Lưu",
     "—",
     "- Thành công; sau khi tải lại ô không còn tích"),

    ("003", "Tích tất cả ở tab 2", "P0",
     "—",
     "1. Tab 2, công ty A, bấm \"Tích tất cả\"\n"
     "2. Bấm Lưu",
     "—",
     "- Bước 1: cả 31 ô của công ty A được tích; ô của công ty khác không đổi\n"
     "- Sau Lưu và tải lại: 31 ô vẫn tích"),

    ("004", "Bỏ tích tất cả ở tab 2", "P0",
     "Như TC_04.003",
     "1. Bấm \"Bỏ tích tất cả\", Lưu",
     "—",
     "- Cả 31 ô bỏ tích; sau tải lại vẫn trống\n"
     "- Ô ở tab 1 của công ty A KHÔNG bị ảnh hưởng"),

    ("005", "Cấu hình độc lập giữa các công ty", "P0",
     "Ô \"Hàng giữ quá hạn - Lập hợp đồng\" của A và B đều đang bỏ tích",
     "1. Chỉ tích ô này ở công ty A, Lưu\n"
     "2. Mở tab con B",
     "—",
     "- A: ô tích; B: ô vẫn trống"),

    ("006", "Cấu hình độc lập giữa các nhóm", "P1",
     "—",
     "1. Tích \"Lập báo giá\" ở nhóm Hàng mượn quá hạn (công ty A), Lưu\n"
     "2. Đọc ô \"Lập báo giá\" ở nhóm Hàng giữ và Hàng nhập thẳng",
     "—",
     "- Chỉ ô ở nhóm Hàng mượn được tích, 2 nhóm kia giữ nguyên"),

    ("007", "Hủy bỏ thay đổi chưa Lưu", "P1",
     "—",
     "1. Tích 3 ô bất kỳ\n"
     "2. Bấm Hủy\n"
     "3. Mở lại màn theo menu",
     "—",
     "- Bước 2 đưa về trang chủ, không hỏi xác nhận\n"
     "- Bước 3: 3 ô vẫn ở trạng thái cũ, không sinh lịch sử"),

    ("008", "Tải lại trang trước khi Lưu", "P2",
     "—",
     "1. Tích 1 ô, bấm F5",
     "—",
     "- Ô trở lại trạng thái đã lưu trước đó"),

    ("009", "Lưu khi mất kết nối", "P2",
     "—",
     "1. Tích 1 ô, ngắt mạng, bấm Lưu\n"
     "2. Bật mạng, tải lại trang",
     "—",
     "- Thông báo đỏ \"Đã có lỗi xảy ra\", nút Lưu dùng lại được\n"
     "- Sau tải lại: cấu hình không đổi"),
]

SEC_V = [
    # ---- Tab 1: chặn nhân viên ----
    ("001", "Nhân viên KHÔNG quá hạn không bị chặn", "P0",
     "Công ty A tích đủ 21 ô tab 1; nhân viên NV-1 thuộc A không có hàng giữ, hàng mượn, hàng nhập "
     "thẳng quá hạn",
     "1. NV-1 lập báo giá, Lưu\n"
     "2. NV-1 lập yêu cầu xuất hàng, Lưu",
     "—",
     "- Cả 2 lưu thành công, không có thông báo chặn"),

    ("002", "Hàng giữ quá hạn chặn Lập báo giá", "P0",
     "A tích \"Hàng giữ quá hạn - Lập báo giá\"; NV-1 (thuộc A) có 1 hàng giữ, số lượng 2, hết hạn "
     "giữ hôm qua",
     "1. NV-1 vào màn Báo giá, bấm Tạo mới\n"
     "2. (Nếu vào được) nhập đủ dữ liệu, bấm Lưu",
     "—",
     "- Hệ thống chặn, thông báo vàng \"Có hàng giữ quá hạn!\"\n"
     "- Bấm Tạo mới bị đưa về trang trước, hoặc bấm Lưu không tạo được báo giá\n"
     "- Áp dụng cả cho báo giá dịch vụ bảo hành - sửa chữa"),

    ("003", "Hàng giữ hết hạn HÔM NAY chưa tính quá hạn", "P1",
     "Như TC_05.002 nhưng ngày hết hạn giữ là hôm nay",
     "1. NV-1 lập báo giá, Lưu",
     "—",
     "- Lưu thành công (chỉ quá hạn khi ngày hết hạn TRƯỚC hôm nay)"),

    ("004", "Bỏ tích là hết chặn", "P0",
     "Như TC_05.002",
     "1. Quản trị bỏ tích \"Hàng giữ quá hạn - Lập báo giá\" của A, Lưu\n"
     "2. NV-1 lập báo giá, Lưu",
     "—",
     "- Lưu thành công, không chặn"),

    ("005", "Hàng mượn quá hạn chặn Lập hợp đồng", "P0",
     "A tích \"Hàng mượn quá hạn - Lập hợp đồng\"; NV-2 lập phiếu yêu cầu xuất mượn, đã mượn 3 cái, "
     "trả 1, ngày hẹn trả cách đây 5 ngày",
     "1. NV-2 lập hợp đồng bán, Lưu\n"
     "2. NV-2 lập hợp đồng dịch vụ bảo hành - sửa chữa, Lưu",
     "—",
     "- Cả 2 bị chặn, thông báo \"Có hàng mượn quá hạn!\""),

    ("006", "Hàng mượn đã trả hết không chặn", "P1",
     "Như TC_05.005 nhưng NV-2 đã trả đủ 3 cái",
     "1. NV-2 lập hợp đồng bán, Lưu",
     "—",
     "- Lưu thành công"),

    ("007", "Hàng nhập thẳng quá hạn theo số ngày của công ty", "P0",
     "A có \"Hạn xuất hàng nhập thẳng (Số ngày)\" = 10; A tích \"Hàng nhập thẳng quá hạn - Lập yêu "
     "cầu nhập hàng\"\n"
     "NV-3 có hàng nhập thẳng còn 4 cái, nhập cách đây 11 ngày",
     "1. NV-3 vào Yêu cầu nhập hàng, bấm Tạo mới\n"
     "2. Đổi ngày nhập của hàng (dữ liệu khác) thành cách đây 9 ngày, thử lại",
     "—",
     "- Bước 1: chặn, \"Có hàng nhập thẳng quá hạn!\"\n"
     "- Bước 2: không chặn"),

    ("008", "Công ty để trống số ngày hạn xuất nhập thẳng", "P1",
     "Công ty A để trống / 0 ô \"Hạn xuất hàng nhập thẳng (Số ngày)\"; NV-3 có hàng nhập thẳng còn "
     "tồn, mới nhập hôm nay; A tích \"Hàng nhập thẳng quá hạn - Lập báo giá\"",
     "1. NV-3 lập báo giá, Lưu",
     "—",
     "- Hệ thống chặn \"Có hàng nhập thẳng quá hạn!\" dù hàng mới nhập\n"
     "- Lưu ý: hành vi theo code hiện tại; QA xác nhận với nghiệp vụ, nếu không chấp nhận ghi "
     "Failed"),

    ("009", "Lập yêu cầu xuất hàng: phiếu Xuất thẳng được đi qua", "P0",
     "A tích \"Hàng giữ quá hạn - Lập yêu cầu xuất hàng\"\n"
     "A tích \"Hàng nhập thẳng quá hạn - Lập yêu cầu xuất hàng\"\n"
     "NV-1 có hàng giữ quá hạn",
     "1. NV-1 lập yêu cầu xuất hàng thường, Lưu\n"
     "2. NV-1 lập yêu cầu xuất hàng có tích \"Xuất thẳng\", Lưu",
     "—",
     "- Bước 1: chặn \"Có hàng giữ quá hạn!\"\n"
     "- Bước 2: lưu thành công"),

    ("010", "Lập yêu cầu xuất hàng để giải phóng chính hàng giữ quá hạn", "P0",
     "Như TC_05.009; hàng giữ quá hạn của NV-1 là Máy lọc nước LN-01",
     "1. NV-1 lập yêu cầu xuất hàng chỉ gồm LN-01, Lưu\n"
     "2. NV-1 lập phiếu gồm LN-01 và một hàng khác, Lưu",
     "—",
     "- Bước 1: lưu thành công (được xuất hàng đang giữ quá hạn)\n"
     "- Bước 2: chặn \"Có hàng giữ quá hạn!\""),

    ("011", "Lập yêu cầu nhập hàng loại Mượn trả lại không bị chặn bởi hàng mượn", "P0",
     "A tích \"Hàng mượn quá hạn - Lập yêu cầu nhập hàng\"; NV-2 có hàng mượn quá hạn",
     "1. NV-2 lập yêu cầu nhập hàng loại khác, Lưu\n"
     "2. NV-2 lập yêu cầu nhập hàng loại \"Mượn trả lại\", Lưu",
     "—",
     "- Bước 1: chặn \"Có hàng mượn quá hạn!\"\n"
     "- Bước 2: lưu thành công (để trả hàng mượn)"),

    ("012", "Cập nhật hàng hóa bị chặn", "P1",
     "A tích \"Hàng giữ quá hạn - Cập nhật hàng hóa\"; NV-1 có hàng giữ quá hạn và có quyền sửa hàng "
     "hóa",
     "1. NV-1 thử tạo mới, sửa, sao chép, xóa một hàng hóa",
     "—",
     "- Mọi thao tác bị chặn \"Có hàng giữ quá hạn!\"\n"
     "- Lưu ý: nếu ERP đã ẩn chức năng ghi hàng hóa (chuyển sang HRM) thì ghi Không áp dụng"),

    ("013", "Duyệt hàng tạm bị chặn", "P1",
     "A tích \"Hàng mượn quá hạn - Duyệt hàng tạm\"; NV-2 có quyền duyệt hàng tạm và có hàng mượn "
     "quá hạn",
     "1. NV-2 mở một hàng tạm, bấm Sửa / Duyệt / Từ chối",
     "—",
     "- Cả 3 thao tác bị chặn \"Có hàng mượn quá hạn!\""),

    ("014", "Ba ô riêng của nhóm Hàng nhập thẳng", "P0",
     "A tích \"Hàng nhập thẳng quá hạn\" - Lập yêu cầu xuất giữ, Gia hạn hàng giữ, Điều chuyển hàng "
     "giữ; NV-3 có hàng nhập thẳng quá hạn",
     "1. NV-3 lập yêu cầu xuất giữ\n"
     "2. NV-3 lập yêu cầu gia hạn hàng giữ\n"
     "3. NV-3 lập phiếu điều chuyển hàng giữ",
     "—",
     "- Cả 3 bị chặn \"Có hàng nhập thẳng quá hạn!\"\n"
     "- Nhân viên chỉ có hàng giữ / hàng mượn quá hạn (không có nhập thẳng) thì KHÔNG bị chặn 3 "
     "thao tác này"),

    ("015", "Dính nhiều loại quá hạn chỉ báo một thông báo", "P1",
     "A tích ô Lập báo giá ở cả 3 nhóm; NV-4 vừa có hàng giữ vừa có hàng mượn quá hạn",
     "1. NV-4 lập báo giá, Lưu",
     "—",
     "- Chỉ một thông báo \"Có hàng giữ quá hạn!\" (hàng giữ được xét trước)"),

    ("016", "Chặn theo công ty của nhân viên, không theo công ty phiếu", "P1",
     "Công ty A tích \"Hàng giữ quá hạn - Lập báo giá\", công ty B không tích; NV-1 thuộc A, có hàng "
     "giữ quá hạn",
     "1. NV-1 lập báo giá",
     "—",
     "- Bị chặn theo cấu hình của A\n"
     "- Nhân viên thuộc B có hàng giữ quá hạn KHÔNG bị chặn"),

    ("017", "Chỉ xét hàng của chính người thao tác", "P0",
     "A tích \"Hàng giữ quá hạn - Lập báo giá\"; NV-5 không có hàng quá hạn, cùng phòng với NV-1 có "
     "hàng giữ quá hạn",
     "1. NV-5 lập báo giá, Lưu",
     "—",
     "- Lưu thành công — tab 1 không xét đồng nghiệp"),

    # ---- Tab 2: chặn trưởng phòng ----
    ("018", "Trưởng phòng bị chặn duyệt hợp đồng bán", "P0",
     "A tích ở tab 2 \"Duyệt hợp đồng bán\"; TP-1 quản lý phòng KD1 (công ty A); NV-1 thuộc KD1 có "
     "hàng giữ quá hạn; có hợp đồng bán chờ TP-1 duyệt",
     "1. TP-1 mở hợp đồng, bấm Duyệt",
     "—",
     "- Không duyệt được\n"
     "- Mở cửa sổ \"Phòng ban bạn quản lý có NV hàng quá hạn như sau:\" có dòng NV-1, Loại quá hạn "
     "\"Hàng giữ\"\n"
     "- Không có thông báo chữ dạng thông báo vàng"),

    ("019", "Phòng hết nhân viên quá hạn thì duyệt được", "P0",
     "Như TC_05.018; NV-1 xuất hết hàng giữ quá hạn",
     "1. TP-1 bấm Duyệt lại",
     "—",
     "- Duyệt thành công"),

    ("020", "Tab 2 không phân biệt loại quá hạn", "P1",
     "Như TC_05.018 nhưng NV-1 chỉ có hàng mượn quá hạn; tab 1 không tích gì",
     "1. TP-1 duyệt hợp đồng bán",
     "—",
     "- Vẫn bị chặn; cửa sổ ghi Loại quá hạn \"Hàng mượn\""),

    ("021", "Trưởng phòng tự có hàng quá hạn cũng bị chặn", "P1",
     "TP-1 thuộc chính phòng KD1 do mình quản lý, có hàng giữ quá hạn; nhân viên khác không quá hạn",
     "1. TP-1 duyệt hợp đồng bán",
     "—",
     "- Bị chặn; cửa sổ liệt kê chính TP-1"),

    ("022", "Nhân viên đã nghỉ việc còn hàng quá hạn", "P2",
     "NV-6 đã nghỉ việc nhưng hồ sơ vẫn thuộc phòng KD1 và còn hàng mượn quá hạn",
     "1. TP-1 duyệt hợp đồng bán",
     "—",
     "- Theo code hiện tại TP-1 BỊ CHẶN và cửa sổ liệt kê NV-6\n"
     "- Lưu ý: QA xác nhận với nghiệp vụ có nên tính nhân viên đã nghỉ"),

    ("023", "Ô chưa tích ở tab 2 không chặn", "P0",
     "Như TC_05.018 nhưng ô \"Duyệt hợp đồng bán\" của A bỏ tích",
     "1. TP-1 duyệt hợp đồng bán",
     "—",
     "- Duyệt thành công"),

    ("024", "Người không quản lý phòng nào không bị tab 2 chặn", "P1",
     "Tài khoản KT-B có quyền duyệt hợp đồng nhưng không được gán quản lý phòng ban nào",
     "1. KT-B duyệt hợp đồng bán",
     "—",
     "- Duyệt thành công"),

    ("025", "Các thao tác ERP được chặn ở tab 2 — kho & hàng giữ", "P0",
     "A tích 6 ô: Duyệt yêu cầu xuất giữ, Duyệt gia hạn hàng giữ, Duyệt điều chuyển hàng giữ, Duyệt "
     "gia hạn hàng mượn, Duyệt yêu cầu xuất hàng, Duyệt yêu cầu xuất bán hàng mượn; phòng TP-1 có "
     "nhân viên quá hạn",
     "1. Với mỗi ô, TP-1 duyệt một phiếu tương ứng trên ERP",
     "6 loại phiếu",
     "- Cả 6 bị chặn và mở cửa sổ nhân viên quá hạn\n"
     "- Duyệt yêu cầu xuất hàng: chặn cả nút chuyển Ban giám đốc duyệt"),

    ("026", "Các thao tác ERP được chặn ở tab 2 — nhập hàng, hợp đồng, đặt hàng", "P0",
     "A tích: Duyệt yêu cầu nhập hàng, Duyệt hợp đồng mua, Duyệt yêu cầu đặt hàng, Duyệt quyết toán "
     "hợp đồng; phòng TP-1 có nhân viên quá hạn",
     "1. TP-1 duyệt yêu cầu nhập hàng (bước trưởng phòng / ban kiểm soát)\n"
     "2. TP-1 duyệt hợp đồng mua (trong nước, nước ngoài, nguyên tắc, mua dịch vụ)\n"
     "3. TP-1 duyệt yêu cầu đặt hàng\n"
     "4. TP-1 duyệt quyết toán hợp đồng",
     "—",
     "- Tất cả bị chặn, mở cửa sổ nhân viên quá hạn\n"
     "- Duyệt hợp đồng bán cũng chặn cả phụ lục và hợp đồng nguyên tắc"),

    ("027", "Các thao tác ERP được chặn ở tab 2 — dịch vụ & vận chuyển", "P1",
     "A tích: Duyệt yêu cầu lắp đặt bàn giao, Duyệt giá vận chuyển quốc tế, Duyệt yêu cầu mua dịch "
     "vụ, Duyệt kết quả công việc",
     "1. TP-1 lần lượt duyệt yêu cầu lắp đặt bàn giao, giá vận chuyển quốc tế, yêu cầu mua dịch vụ\n"
     "2. TP-1 lưu kết quả công việc ở màn duyệt kết quả bảo hành - sửa chữa",
     "—",
     "- Cả 4 bị chặn, mở cửa sổ nhân viên quá hạn"),

    ("028", "Ô Duyệt đề nghị thanh toán chặn ở bước LẬP phiếu", "P1",
     "A tích \"Duyệt đề nghị thanh toán\"; phòng TP-1 có nhân viên quá hạn",
     "1. TP-1 lập mới phiếu đề nghị thanh toán, Lưu\n"
     "2. TP-1 duyệt một phiếu đề nghị thanh toán chờ trưởng phòng duyệt",
     "—",
     "- Theo code hiện tại: bước 1 BỊ CHẶN, bước 2 KHÔNG bị chặn\n"
     "- Lưu ý: ngược với tên ô (\"Duyệt\"); ghi Failed nếu nghiệp vụ muốn chặn bước duyệt"),

    ("029", "Ô Tạo phiếu giao việc (phân hệ chấm công) phía ERP", "P2",
     "A tích \"Tạo phiếu giao việc (phân hệ chấm công)\"; phòng TP-1 có nhân viên quá hạn",
     "1. TP-1 lập phiếu phân công bảo hành - sửa chữa trên ERP, Lưu",
     "—",
     "- Theo code hiện tại KHÔNG bị chặn ở ERP (tên thao tác không khớp ô cấu hình)\n"
     "- Lưu ý: nếu nghiệp vụ muốn chặn ở ERP thì ghi Failed"),

    ("030", "Các ô tab 2 được chặn bên HRM — chấm công", "P0",
     "A tích: Tạo phiếu giao việc (CC), Tạo phiếu đi công tác (CC), Duyệt đơn xin nghỉ, Duyệt đề nghị "
     "tra soát công, Duyệt đăng ký làm thêm, Duyệt đơn đi muộn về sớm, Duyệt phiếu yêu cầu làm thêm, "
     "Duyệt phiếu giao việc (CC), Duyệt phiếu đi công tác (CC); phòng TP-1 có nhân viên quá hạn",
     "1. TP-1 đăng nhập HRM, lần lượt thực hiện 9 thao tác tương ứng ở phân hệ Chấm công",
     "9 thao tác",
     "- Cả 9 bị chặn: HRM mở cửa sổ \"Phòng ban bạn quản lý có NV hàng quá hạn như sau:\"\n"
     "- Không có chữ thông báo riêng"),

    ("031", "Các ô tab 2 được chặn bên HRM — giao việc & thanh toán", "P0",
     "A tích: Tạo phiếu công tác (GV), Chặn gia hạn và kết thúc phiếu công tác (GV), Duyệt đề nghị "
     "thanh toán HRM, Duyệt hồ sơ thanh toán, Duyệt quyết toán công theo HĐ, Duyệt kết quả công tác "
     "trên HRM",
     "1. TP-1 thực hiện từng thao tác tương ứng trên HRM",
     "6 thao tác",
     "- Cả 6 bị chặn, mở cửa sổ nhân viên quá hạn\n"
     "- Chặn gia hạn và kết thúc: kiểm tra ở màn duyệt yêu cầu gia hạn/kết thúc sớm; các nút kết "
     "thúc/gia hạn trực tiếp trên phiếu công tác chấm công có thể KHÔNG bị chặn — ghi nhận thực tế"),

    ("032", "HRM: các ô trùng tên thao tác ERP", "P1",
     "A tích: Duyệt yêu cầu xuất giữ, Duyệt gia hạn hàng mượn, Duyệt yêu cầu mua dịch vụ, và Duyệt "
     "gia hạn hàng giữ, Duyệt điều chuyển hàng giữ, Duyệt quyết toán hợp đồng",
     "1. TP-1 thực hiện các thao tác duyệt tương ứng trên các màn HRM (phân hệ Tài chính / Kho)",
     "—",
     "- Duyệt yêu cầu xuất giữ, gia hạn hàng mượn, yêu cầu mua dịch vụ: BỊ CHẶN trên HRM\n"
     "- Lưu ý: gia hạn hàng giữ, điều chuyển hàng giữ, quyết toán hợp đồng và các thao tác duyệt "
     "nhập/xuất/hợp đồng trên HRM hiện CHƯA chặn — ghi nhận thực tế, báo đội phát triển nếu nghiệp "
     "vụ cần"),

    ("033", "HRM không kết nối được ERP thì không chặn", "P2",
     "Ở HRM, phân hệ đang bật dùng ERP; máy chủ ERP tạm dừng",
     "1. TP-1 (phòng có nhân viên quá hạn, ô đã tích) duyệt đơn xin nghỉ trên HRM",
     "—",
     "- Theo code hiện tại thao tác ĐƯỢC THỰC HIỆN (không chặn khi không hỏi được ERP)\n"
     "- Lưu ý: ghi nhận để nghiệp vụ biết rủi ro"),
]

SEC_VI = [
    ("001", "Màn không có Xóa", "P2",
     "—",
     "1. Quan sát màn",
     "—",
     "- Không áp dụng cho feature này: muốn bỏ chặn thì bỏ tích rồi Lưu; không xóa được dòng lịch "
     "sử"),
]

SEC_VII = [
    ("001", "Cửa sổ nhân viên quá hạn trên ERP", "P0",
     "Như TC_05.018; phòng KD1 có NV-1 (hàng giữ), NV-2 (hàng mượn và hàng nhập thẳng)",
     "1. TP-1 bấm Duyệt hợp đồng bán bị chặn\n"
     "2. Đọc cửa sổ hiện ra",
     "—",
     "- Tiêu đề \"Phòng ban bạn quản lý có NV hàng quá hạn như sau:\"\n"
     "- Bảng 3 cột STT, Nhân viên, Loại quá hạn; trong lúc tải hiện \"Đang tải...\"\n"
     "- NV-1: mã - tên, \"Hàng giữ\"; NV-2: \"Hàng mượn, Hàng NXT\"\n"
     "- Có nút \"Xuất Excel\""),

    ("002", "Cửa sổ liệt kê mọi loại quá hạn bất kể ô đang tích", "P2",
     "Tab 1 của A không tích nhóm nào; phòng KD1 có NV-2 hàng nhập thẳng quá hạn",
     "1. Làm TP-1 bị chặn ở một thao tác tab 2",
     "—",
     "- Cửa sổ vẫn liệt kê NV-2 với \"Hàng NXT\""),

    ("003", "Xuất Excel danh sách nhân viên quá hạn", "P1",
     "Như TC_07.001",
     "1. Bấm \"Xuất Excel\" trong cửa sổ\n"
     "2. Mở file tải về",
     "—",
     "- Tải về file \"danh_sach_nhan_vien_qua_han.xlsx\"\n"
     "- File có đúng các nhân viên và loại quá hạn như trên cửa sổ"),

    ("004", "Cửa sổ trên HRM", "P1",
     "TP-1 bị chặn ở một thao tác trên HRM (TC_05.030)",
     "1. Đọc cửa sổ hiện ra, bấm Xuất Excel",
     "—",
     "- Cùng tiêu đề và cùng danh sách như cửa sổ trên ERP\n"
     "- Xuất Excel tải được file"),

    ("005", "Màn cấu hình không có In / Xuất Excel", "P2",
     "—",
     "1. Quan sát màn cấu hình",
     "—",
     "- Màn cấu hình không có nút In hay Xuất Excel"),
]

SEC_VIII = [
    ("001", "Màn không có ô nhập liệu tự do", "P2",
     "—",
     "1. Quan sát màn",
     "—",
     "- Chỉ có ô tích; không có ô chữ / ô số nên không có thông báo lỗi nhập liệu\n"
     "- Được phép bỏ tích toàn bộ rồi Lưu (không bắt buộc tích tối thiểu)"),

    ("002", "Bỏ tích toàn bộ một công ty", "P1",
     "Công ty A đang tích nhiều ô ở cả 2 tab",
     "1. Bỏ tích hết tab 1 (từng ô) và bấm \"Bỏ tích tất cả\" ở tab 2 của A\n"
     "2. Lưu\n"
     "3. Nhân viên có hàng quá hạn thuộc A lập báo giá",
     "—",
     "- Lưu thành công\n"
     "- Bước 3 không bị chặn"),

    ("003", "Bấm Lưu nhiều lần liên tiếp", "P2",
     "—",
     "1. Tích 1 ô, bấm Lưu 3 lần thật nhanh",
     "—",
     "- Nút Lưu bị mờ sau lần bấm đầu\n"
     "- Chỉ một dòng lịch sử cho thay đổi này"),
]

SEC_IX = [
    ("001", "Hai quản trị cùng sửa cấu hình", "P1",
     "SA-1 và SA-2 cùng mở màn; ô X và Y của công ty A đều đang bỏ tích",
     "1. SA-1 tích X, Lưu\n"
     "2. SA-2 (chưa tải lại trang) tích Y, Lưu\n"
     "3. Tải lại trang",
     "—",
     "- Kết quả: CHỈ Y được tích, X bị SA-2 ghi đè thành bỏ tích (người lưu sau thắng cho cả công "
     "ty)\n"
     "- Lịch sử có dòng của SA-1 \"Tích: X\" và dòng của SA-2 gồm \"Tích: Y\" và \"Bỏ tích: X\"\n"
     "- Lưu ý: ghi nhận để quản trị biết, nên tải lại trang trước khi sửa"),

    ("002", "Thay đổi cấu hình có hiệu lực ngay", "P0",
     "NV-1 (công ty A) có hàng giữ quá hạn và đang mở sẵn form báo giá",
     "1. Quản trị tích \"Hàng giữ quá hạn - Lập báo giá\" cho A, Lưu\n"
     "2. NV-1 bấm Lưu báo giá đang mở",
     "—",
     "- NV-1 bị chặn ngay, không cần đăng nhập lại"),

    ("003", "Trưởng phòng quản lý phòng ở công ty khác", "P2",
     "TP-2 thuộc công ty A, được gán quản lý phòng KD9 của công ty B; KD9 có nhân viên quá hạn; A "
     "tích \"Duyệt hợp đồng bán\"",
     "1. TP-2 duyệt hợp đồng bán",
     "—",
     "- Không bị chặn: chỉ xét phòng do TP-2 quản lý TRONG công ty của TP-2"),
]

SEC_X = [
    ("001", "Vòng đời chặn nhân viên", "P0",
     "Công ty A chưa tích ô nào ở tab 1; NV-1 thuộc A",
     "1. Quản trị tích \"Hàng mượn quá hạn - Lập yêu cầu xuất hàng\" cho A, Lưu, kiểm lịch sử\n"
     "2. NV-1 mượn hàng, để quá ngày hẹn trả\n"
     "3. NV-1 lập yêu cầu xuất hàng thường, Lưu\n"
     "4. NV-1 lập yêu cầu nhập hàng loại Mượn trả lại, trả đủ hàng\n"
     "5. NV-1 lập lại yêu cầu xuất hàng, Lưu",
     "—",
     "- Bước 1: lịch sử có \"[A] Tích: Hàng mượn quá hạn - Lập yêu cầu xuất hàng\"\n"
     "- Bước 3: chặn \"Có hàng mượn quá hạn!\"\n"
     "- Bước 4: không bị chặn\n"
     "- Bước 5: lưu thành công"),

    ("002", "Vòng đời chặn trưởng phòng", "P0",
     "Phòng KD1 (công ty A) do TP-1 quản lý; NV-2 thuộc KD1",
     "1. Quản trị tích ở tab 2 \"Duyệt yêu cầu xuất hàng\" cho A, Lưu\n"
     "2. NV-2 có hàng giữ quá hạn; NV-2 lập yêu cầu xuất hàng (giải phóng đúng hàng đó)\n"
     "3. TP-1 duyệt phiếu của NV-2\n"
     "4. TP-1 bấm Xuất Excel trong cửa sổ, nhắc NV-2 xử lý\n"
     "5. NV-2 xuất hết hàng giữ quá hạn qua kênh khác; TP-1 duyệt lại",
     "—",
     "- Bước 3: không duyệt được, cửa sổ liệt kê NV-2 \"Hàng giữ\"\n"
     "- Bước 4: tải được file danh sách\n"
     "- Bước 5: duyệt thành công\n"
     "- Lưu ý: TP-1 bị chặn duyệt cả phiếu giúp giải phóng hàng — đúng theo code hiện tại"),

    ("003", "Một cấu hình áp cho cả ERP và HRM", "P1",
     "A tích ở tab 2 \"Duyệt đơn xin nghỉ\" và \"Duyệt hợp đồng bán\"; phòng TP-1 có nhân viên quá "
     "hạn",
     "1. TP-1 duyệt hợp đồng bán trên ERP\n"
     "2. TP-1 duyệt đơn xin nghỉ trên HRM\n"
     "3. Quản trị bỏ tích cả 2 ô trên màn ERP, Lưu; TP-1 thử lại 2 thao tác",
     "—",
     "- Bước 1, 2: đều bị chặn và hiện cửa sổ nhân viên quá hạn\n"
     "- Bước 3: cả 2 thao tác thành công"),
]
