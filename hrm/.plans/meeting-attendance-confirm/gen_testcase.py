# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho Redmine #11369 - Xac nhan tham du truoc cuoc hop."""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", ".claude", "skills",
                                "testcase-documenter", "assets"))
from tc_engine import build  # noqa: E402

MODULE = "Cuộc họp - Xác nhận tham dự"

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Cho phép khách mời NỘI BỘ của một cuộc họp tự phản hồi trước giờ họp là \"Có mặt\" hay "
     "\"Vắng có lý do\", thay vì chờ người chủ trì điểm danh. Phản hồi được ghi thẳng vào bảng "
     "Điểm danh của cuộc họp nên người chủ trì mở biên bản là thấy sẵn và vẫn sửa đè được. "
     "Người dùng phản hồi được ở HAI nơi: thanh \"Xác nhận tham dự\" trên màn Chi tiết cuộc họp, "
     "và ngay trên dòng thông báo trong bảng thông báo (biểu tượng quả chuông)."),

    ("2. Đối tượng được tính / hiển thị",
     "Thanh \"Xác nhận tham dự\" chỉ hiện khi ĐỒNG THỜI:\n"
     "- Người đang đăng nhập có tên trong \"Thành phần tham gia - Phía Công ty\" (khách mời nội bộ) "
     "của cuộc họp đó;\n"
     "- Cuộc họp đang ở trạng thái \"Lên lịch\" hoặc \"Chốt lịch\";\n"
     "- Thời điểm hiện tại còn TRƯỚC giờ bắt đầu cuộc họp;\n"
     "- Đang ở màn Chi tiết cuộc họp (không phải màn Tạo mới / Sửa).\n"
     "Trên bảng thông báo: cụm nút chỉ hiện ở dòng thông báo cuộc họp sinh ra từ hai sự kiện "
     "\"Lên lịch\" và \"Chốt lịch\"."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Người KHÔNG có tên trong Thành phần tham gia phía Công ty: không thấy thanh xác nhận.\n"
     "- Khách mời bên ngoài / khách hàng: không nằm trong luồng này vì không có tài khoản đăng nhập.\n"
     "- Cuộc họp ở trạng thái \"Đang tạo\", \"Hoàn thành\" hoặc \"Hủy\": cụm nút ẩn, chỉ còn dòng lý do "
     "vì sao không xác nhận được.\n"
     "- Cuộc họp đã tới hoặc qua giờ bắt đầu: cụm nút ẩn, việc chốt điểm danh thuộc về người chủ trì.\n"
     "- Người dùng KHÔNG được tự chọn \"Vắng không lý do\" - chỉ người chủ trì đánh được trạng thái này "
     "ở bảng Điểm danh.\n"
     "- Thông báo \"Thay đổi lịch\" hiện KHÔNG kèm cụm nút xác nhận (chỉ Lên lịch và Chốt lịch có)."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Không có bộ lọc thời gian trên giao diện. Nhưng thời gian là điều kiện chặn quan trọng nhất: mốc "
     "so sánh là \"Thời gian bắt đầu\" của cuộc họp - còn trước mốc này thì xác nhận được, từ đúng mốc "
     "trở đi thì không."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Phản hồi trước họp và điểm danh thật của người chủ trì dùng CHUNG một ô dữ liệu trên dòng của "
     "người đó trong tab \"Điểm danh\". Bốn trạng thái của ô này: \"Chưa điểm danh\", \"Có mặt\", "
     "\"Vắng có lý do\", \"Vắng không lý do\". Người dùng tự phản hồi chỉ đặt được 2 trạng thái giữa; "
     "người chủ trì đặt được cả 4 và ghi đè lên phản hồi của người dùng.\n"
     "Hệ quả đã được chấp nhận: sau cuộc họp KHÔNG phân biệt được ai tự báo, ai bị chủ trì sửa."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "Hệ thống chỉ giữ LỰA CHỌN CUỐI CÙNG, không lưu lịch sử đổi ý. Đổi từ \"Vắng có lý do\" sang "
     "\"Có mặt\" thì lý do vắng cũ bị xóa sạch, không để lại ghi chú lạc. "
     "Cùng một cuộc họp có thể xuất hiện đồng thời ở màn Chi tiết và ở nhiều dòng thông báo trên chuông; "
     "phản hồi ở một nơi phải làm mọi nơi còn lại đổi theo ngay, không được để hai trạng thái mâu thuẫn "
     "trên cùng một màn hình."),

    ("7. Phân quyền cấp",
     "Tính năng KHÔNG thêm quyền mới - đây là thao tác tự phục vụ của chính người trong cuộc họp, "
     "tư cách được xét theo danh sách Thành phần tham gia chứ không theo quyền.\n"
     "Các quyền liên quan đang có sẵn, dùng để dựng dữ liệu test:\n"
     "- \"Xem danh sách meeting theo tổng công ty\"\n"
     "- \"Xem danh sách meeting theo công ty\"\n"
     "- \"Xem danh sách meeting theo phòng ban\"\n"
     "- \"Xem danh sách meeting theo bộ phận\"\n"
     "Lưu ý: người tạo cuộc họp và người chủ trì vẫn dùng luồng Điểm danh sẵn có, không đi qua thanh "
     "xác nhận này (trừ khi chính họ cũng nằm trong Thành phần tham gia phía Công ty)."),

    ("8. Cách tính các ô thống kê",
     "- Nhãn trạng thái trên thanh xác nhận: chưa phản hồi hiện \"Chưa phản hồi\" (nền xám); đã chọn "
     "Có mặt hiện \"Đã xác nhận: Có mặt\" (nền xanh lá); đã báo vắng hiện \"Đã báo: Vắng có lý do - "
     "<lý do>\" (nền cam); bị chủ trì đánh vắng không lý do hiện \"Vắng không lý do\" (nền đỏ).\n"
     "- Lý do vắng quá dài thì nhãn cắt bớt bằng dấu ba chấm; rê chuột vào nhãn xem được đủ chữ.\n"
     "- Cột Trạng thái ở tab Điểm danh hiện đúng nhãn tương ứng; chưa ai phản hồi thì hiện "
     "\"Chưa điểm danh\"."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất:\n"
     "1) Nút của lựa chọn ĐANG áp dụng bị ẩn đi, chỉ còn nút của lựa chọn kia. Đang \"Có mặt\" thì chỉ "
     "thấy nút [Vắng có lý do] - đây là ĐÚNG thiết kế, không phải mất nút.\n"
     "2) Đang ở trạng thái Vắng, muốn sửa RIÊNG lý do thì bấm biểu tượng cây bút vuông cạnh nhãn trạng "
     "thái, không phải bấm lại nút.\n"
     "3) Bấm nút trên dòng thông báo ở chuông thì bảng thông báo PHẢI ở nguyên đó, không được đóng lại "
     "và không được nhảy sang màn chi tiết. Cả hai nút phải hành xử giống nhau.\n"
     "4) Mốc chặn là giờ BẮT ĐẦU cuộc họp, không phải giờ kết thúc.\n"
     "5) Phản hồi ghi ngay khi bấm, không cần bấm Lưu ở màn cuộc họp.\n"
     "6) Thanh xác nhận phải thấp hơn hẳn thanh trạng thái phía trên; nhãn, biểu tượng và các nút nằm "
     "trên cùng một đường ngang, cùng cỡ chữ."),
]

ROLE_TCS = [
    ("00", "Khách mời nội bộ thấy thanh xác nhận tham dự", "P0",
     "Cuộc họp MET-TEST-01 trạng thái \"Chốt lịch\", giờ bắt đầu là ngày mai. Thành phần tham gia phía "
     "Công ty gồm 5 người, trong đó có tài khoản A.",
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Vào phân hệ Giao việc → nhóm Cuộc họp → bấm \"Cuộc họp\"\n"
     "3. Mở cuộc họp MET-TEST-01 ở màn Chi tiết\n"
     "4. Quan sát khu vực ngay dưới thanh trạng thái",
     "Tài khoản: A (khách mời nội bộ)",
     "- Thanh \"Xác nhận tham dự\" hiện với nhãn \"Chưa phản hồi\"\n"
     "- Có đủ 2 nút [Có mặt] và [Vắng có lý do]"),

    ("01", "Người ngoài Thành phần tham gia không thấy thanh xác nhận", "P0",
     "Cùng cuộc họp MET-TEST-01. Tài khoản C KHÔNG nằm trong Thành phần tham gia phía Công ty nhưng có "
     "quyền xem danh sách cuộc họp theo công ty.",
     "1. Đăng nhập bằng tài khoản C\n"
     "2. Vào phân hệ Giao việc → nhóm Cuộc họp → bấm \"Cuộc họp\"\n"
     "3. Mở cuộc họp MET-TEST-01 ở màn Chi tiết",
     "Tài khoản: C (ngoài danh sách tham gia)",
     "- ⚠️ Thanh \"Xác nhận tham dự\" KHÔNG xuất hiện\n"
     "- Các phần còn lại của màn chi tiết vẫn xem được bình thường"),

    ("02", "Người chủ trì đồng thời là khách mời nội bộ", "P1",
     "Cuộc họp MET-TEST-02, tài khoản D là người chủ trì VÀ có tên trong Thành phần tham gia phía "
     "Công ty. Trạng thái \"Chốt lịch\", chưa tới giờ.",
     "1. Đăng nhập bằng tài khoản D\n"
     "2. Mở MET-TEST-02 ở màn Chi tiết\n"
     "3. Quan sát thanh xác nhận và tab Điểm danh",
     "Tài khoản: D (chủ trì + khách mời)",
     "- Thanh xác nhận vẫn hiện, dùng được bình thường\n"
     "- Người chủ trì vẫn dùng được luồng Điểm danh sẵn có ở tab Điểm danh"),

    ("03", "Gọi thẳng chức năng xác nhận, bỏ qua giao diện - người ngoài danh sách", "P0",
     "Cuộc họp MET-TEST-01. Tài khoản C không nằm trong Thành phần tham gia phía Công ty. "
     "Dành cho tester kỹ thuật.",
     "1. Đăng nhập bằng tài khoản C\n"
     "2. Dùng công cụ kiểm thử gọi thẳng chức năng Xác nhận tham dự cho cuộc họp MET-TEST-01, "
     "bỏ qua giao diện\n"
     "3. Đọc thông báo trả về\n"
     "4. Kiểm lại tab Điểm danh của MET-TEST-01",
     "Lựa chọn gửi lên: Có mặt",
     "- ⚠️ Hệ thống từ chối kèm nội dung \"Bạn không nằm trong Thành phần tham gia nội bộ của cuộc họp "
     "này.\"\n"
     "- Không dòng điểm danh nào bị tạo thêm hay bị sửa"),

    ("04", "Gọi thẳng chức năng xác nhận cho người khác", "P0",
     "Cuộc họp MET-TEST-01 có cả tài khoản A và tài khoản E trong Thành phần tham gia. "
     "Dành cho tester kỹ thuật.",
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Dùng công cụ kiểm thử gọi thẳng chức năng Xác nhận tham dự, cố tình chỉ định người được xác "
     "nhận là tài khoản E\n"
     "3. Kiểm dòng của A và dòng của E ở tab Điểm danh",
     "Lựa chọn gửi lên: Có mặt",
     "- ⚠️ Chỉ dòng của chính tài khoản A bị đổi; dòng của E giữ nguyên\n"
     "- Không có cách nào đặt trạng thái điểm danh cho người khác qua chức năng này"),

    ("05", "Gọi thẳng chức năng xác nhận với lựa chọn Vắng không lý do", "P0",
     "Cuộc họp MET-TEST-01, tài khoản A là khách mời nội bộ. Dành cho tester kỹ thuật.",
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Dùng công cụ kiểm thử gọi thẳng chức năng Xác nhận tham dự với lựa chọn \"Vắng không lý do\"\n"
     "3. Đọc thông báo trả về và kiểm tab Điểm danh",
     "Lựa chọn gửi lên: Vắng không lý do",
     "- ⚠️ Hệ thống từ chối với nội dung \"Lựa chọn tham dự không hợp lệ.\"\n"
     "- Dòng điểm danh của A không đổi"),
]

SEC_I = [
    ("001", "Mở màn Chi tiết cuộc họp từ danh sách", "P0",
     "Cuộc họp MET-TEST-01 trạng thái \"Chốt lịch\", giờ bắt đầu ngày mai, tài khoản A là khách mời "
     "nội bộ, chưa phản hồi.",
     "1. Vào phân hệ Giao việc → nhóm Cuộc họp → bấm \"Cuộc họp\"\n"
     "2. Bấm vào tên cuộc họp MET-TEST-01\n"
     "3. Quan sát khu vực dưới thanh trạng thái",
     "—",
     "- Thanh xác nhận nằm ngay dưới thanh trạng thái, trong khối Thông tin chung\n"
     "- Có biểu tượng người kèm chữ \"Xác nhận tham dự\", nhãn \"Chưa phản hồi\" và 2 nút"),

    ("002", "Mở màn Chi tiết bằng đường dẫn trên dòng thông báo", "P0",
     "Tài khoản A vừa nhận thông báo cuộc họp MET-TEST-01 trên chuông.",
     "1. Bấm biểu tượng quả chuông\n"
     "2. Bấm vào phần nội dung của dòng thông báo cuộc họp (không bấm vào nút)\n"
     "3. Quan sát màn hình mở ra",
     "—",
     "- Chuyển sang màn Chi tiết đúng cuộc họp MET-TEST-01\n"
     "- Thanh xác nhận hiện đúng trạng thái phản hồi hiện tại"),

    ("003", "Màn Tạo mới cuộc họp không có thanh xác nhận", "P0",
     "Tài khoản A có quyền tạo cuộc họp.",
     "1. Vào phân hệ Giao việc → nhóm Cuộc họp → bấm \"Cuộc họp\" → \"Thêm mới\"\n"
     "2. Quan sát khu vực Thông tin chung",
     "—",
     "- ⚠️ Không có thanh xác nhận tham dự (cuộc họp chưa tồn tại, chưa có ai là khách mời)"),

    ("004", "Màn Sửa cuộc họp không có thanh xác nhận", "P1",
     "Cuộc họp MET-TEST-02, tài khoản D là người tạo nên sửa được.",
     "1. Mở MET-TEST-02 → bấm nút Sửa\n"
     "2. Quan sát khu vực Thông tin chung",
     "—",
     "- Không có thanh xác nhận tham dự ở chế độ Sửa\n"
     "- Quay về màn Chi tiết thì thanh hiện lại"),

    ("005", "Giao diện thanh xác nhận gọn và thẳng hàng", "P1",
     "Cuộc họp MET-TEST-01, tài khoản A đang thấy thanh xác nhận.",
     "1. Mở màn Chi tiết MET-TEST-01\n"
     "2. So chiều cao thanh xác nhận với thanh trạng thái phía trên\n"
     "3. Nhìn đường ngang của nhãn, biểu tượng và 2 nút",
     "—",
     "- ⚠️ Thanh xác nhận thấp hơn hẳn thanh trạng thái\n"
     "- Nhãn trạng thái, chữ \"Xác nhận tham dự\" và 2 nút cùng cỡ chữ, cùng chiều cao, tâm nằm trên "
     "một đường ngang\n"
     "- Không có thành phần nào bị đẩy xuống dòng dưới"),

    ("006", "Cuộc họp có nhiều khách mời nội bộ - mỗi người thấy trạng thái của chính mình", "P0",
     "Cuộc họp MET-TEST-01 có 5 khách mời nội bộ. Tài khoản A đã chọn \"Có mặt\", tài khoản E đã báo "
     "\"Vắng có lý do - Đi công tác\", 3 người còn lại chưa phản hồi.",
     "1. Đăng nhập tài khoản A, mở màn Chi tiết, đọc nhãn trạng thái\n"
     "2. Đăng xuất, đăng nhập tài khoản E, mở cùng cuộc họp, đọc nhãn trạng thái",
     "—",
     "- Tài khoản A thấy \"Đã xác nhận: Có mặt\"\n"
     "- Tài khoản E thấy \"Đã báo: Vắng có lý do - Đi công tác\"\n"
     "- ⚠️ Mỗi người chỉ thấy phản hồi của chính mình trên thanh này, phản hồi của người khác xem ở "
     "tab Điểm danh"),
]

SEC_II = [
    ("001", "Xác nhận Có mặt lần đầu", "P0",
     "Cuộc họp MET-TEST-01 trạng thái \"Chốt lịch\", giờ bắt đầu ngày mai. Tài khoản A chưa phản hồi.",
     "1. Mở màn Chi tiết MET-TEST-01\n"
     "2. Bấm nút [Có mặt]\n"
     "3. Quan sát thông báo, nhãn trạng thái và các nút còn lại",
     "Lựa chọn: Có mặt",
     "- Thông báo xanh \"Xác nhận tham dự thành công\"\n"
     "- Nhãn đổi ngay thành \"Đã xác nhận: Có mặt\" (nền xanh lá)\n"
     "- ⚠️ Nút [Có mặt] biến mất, chỉ còn nút [Vắng có lý do]\n"
     "- Không phải bấm Lưu, không phải tải lại trang"),

    ("002", "Xác nhận Có mặt ở cuộc họp trạng thái Lên lịch", "P0",
     "Cuộc họp MET-TEST-03 ở trạng thái \"Lên lịch\", giờ bắt đầu còn 3 ngày nữa, tài khoản A là "
     "khách mời nội bộ.",
     "1. Mở màn Chi tiết MET-TEST-03\n"
     "2. Bấm nút [Có mặt]",
     "Lựa chọn: Có mặt",
     "- Xác nhận thành công, nhãn đổi thành \"Đã xác nhận: Có mặt\"\n"
     "- ⚠️ Cả 2 trạng thái Lên lịch và Chốt lịch đều cho xác nhận"),

    ("003", "Phản hồi được ghi lại sau khi tải lại trang", "P0",
     "Tài khoản A vừa bấm [Có mặt] cho cuộc họp MET-TEST-01.",
     "1. Nhấn phím F5 để tải lại trang\n"
     "2. Đọc nhãn trạng thái trên thanh xác nhận",
     "—",
     "- Nhãn vẫn là \"Đã xác nhận: Có mặt\"\n"
     "- Nút [Có mặt] vẫn ẩn, chỉ còn nút [Vắng có lý do]"),

    ("004", "Bấm Có mặt khi mạng lỗi", "P1",
     "Tài khoản A đang mở màn Chi tiết MET-TEST-01, ngắt kết nối mạng trước khi bấm.",
     "1. Ngắt mạng\n"
     "2. Bấm nút [Có mặt]\n"
     "3. Đọc thông báo",
     "—",
     "- Hiện thông báo đỏ báo không xác nhận được, gợi ý tải lại trang và thử lại\n"
     "- Nhãn trạng thái KHÔNG đổi sang Có mặt (không báo thành công giả)"),
]

SEC_III = [
    ("001", "Mở cửa sổ báo vắng mặt", "P0",
     "Cuộc họp MET-TEST-01, tài khoản A chưa phản hồi.",
     "1. Mở màn Chi tiết MET-TEST-01\n"
     "2. Bấm nút [Vắng có lý do]\n"
     "3. Đọc kỹ tiêu đề, nội dung, nhãn ô nhập và 2 nút",
     "—",
     "- Tiêu đề: \"Báo vắng mặt cuộc họp\"\n"
     "- Nội dung: \"Bạn báo vắng mặt cuộc họp này. Vui lòng nhập lý do để người chủ trì nắm được.\"\n"
     "- Có ô nhập nhãn \"Ghi chú / Lý do\", gợi ý trong ô \"Nhập lý do vắng mặt\"\n"
     "- Hai nút \"Hủy\" và \"Xác nhận\""),

    ("002", "Báo vắng với lý do hợp lệ", "P0",
     "Cửa sổ \"Báo vắng mặt cuộc họp\" đang mở, tài khoản A chưa phản hồi.",
     "1. Nhập lý do \"Đi công tác tại Đà Nẵng\"\n"
     "2. Bấm \"Xác nhận\"\n"
     "3. Quan sát thông báo, nhãn trạng thái và các nút",
     "Lý do: Đi công tác tại Đà Nẵng",
     "- Cửa sổ đóng, hiện thông báo xanh \"Xác nhận tham dự thành công\"\n"
     "- Nhãn đổi thành \"Đã báo: Vắng có lý do - Đi công tác tại Đà Nẵng\" (nền cam)\n"
     "- ⚠️ Nút [Vắng có lý do] biến mất, chỉ còn nút [Có mặt] và biểu tượng cây bút cạnh nhãn"),

    ("003", "Để trống lý do vắng mặt", "P0",
     "Cửa sổ \"Báo vắng mặt cuộc họp\" đang mở, ô lý do để trống.",
     "1. Không nhập gì vào ô lý do\n"
     "2. Bấm \"Xác nhận\"",
     "Lý do: (để trống)",
     "- ⚠️ Ô lý do viền đỏ kèm dòng chữ đỏ \"Vui lòng nhập lý do vắng mặt\"\n"
     "- ⚠️ Cửa sổ KHÔNG đóng\n"
     "- Nhãn trạng thái trên thanh xác nhận không đổi"),

    ("004", "Nhập lý do toàn dấu cách", "P0",
     "Cửa sổ \"Báo vắng mặt cuộc họp\" đang mở.",
     "1. Gõ 5 dấu cách vào ô lý do\n"
     "2. Bấm \"Xác nhận\"",
     "Lý do: \"     \" (toàn dấu cách)",
     "- ⚠️ Bị chặn y như để trống: báo \"Vui lòng nhập lý do vắng mặt\", cửa sổ không đóng\n"
     "- Không có dòng điểm danh nào bị ghi với lý do rỗng"),

    ("005", "Nhập lý do rồi bấm Hủy", "P0",
     "Cửa sổ \"Báo vắng mặt cuộc họp\" đang mở, tài khoản A đang ở trạng thái \"Chưa phản hồi\".",
     "1. Nhập lý do \"Bận việc gia đình\"\n"
     "2. Bấm \"Hủy\"\n"
     "3. Quan sát thanh xác nhận",
     "Lý do: Bận việc gia đình",
     "- Cửa sổ đóng, không có thông báo nào\n"
     "- Nhãn vẫn là \"Chưa phản hồi\", vẫn đủ 2 nút"),

    ("006", "Lý do vắng mặt rất dài", "P1",
     "Cửa sổ \"Báo vắng mặt cuộc họp\" đang mở.",
     "1. Nhập lý do dài khoảng 200 ký tự\n"
     "2. Bấm \"Xác nhận\"\n"
     "3. Quan sát nhãn trạng thái trên thanh và trên dòng thông báo ở chuông\n"
     "4. Rê chuột vào nhãn",
     "Lý do: chuỗi 200 ký tự",
     "- ⚠️ Nhãn cắt bớt bằng dấu ba chấm, KHÔNG kéo dài đẩy nút xuống dòng dưới\n"
     "- Rê chuột vào nhãn xem được đủ nội dung lý do\n"
     "- Tab Điểm danh hiển thị đủ lý do"),

    ("007", "Lý do chứa ký tự đặc biệt và dấu tiếng Việt", "P2",
     "Cửa sổ \"Báo vắng mặt cuộc họp\" đang mở.",
     "1. Nhập lý do: Nghỉ ốm (có giấy) & đang điều trị <tại nhà>\n"
     "2. Bấm \"Xác nhận\"\n"
     "3. Kiểm nhãn trạng thái và tab Điểm danh",
     "Lý do: Nghỉ ốm (có giấy) & đang điều trị <tại nhà>",
     "- Lý do hiển thị nguyên văn ở cả 2 nơi, không bị mất ký tự, không hiện mã lạ"),

    ("008", "Đóng cửa sổ bằng phím Esc", "P2",
     "Cửa sổ \"Báo vắng mặt cuộc họp\" đang mở, đã nhập dở lý do.",
     "1. Nhấn phím Esc",
     "—",
     "- Cửa sổ đóng, không ghi nhận phản hồi nào\n"
     "- Mở lại cửa sổ thì ô lý do trống (chưa từng báo vắng)"),
]

SEC_IV = [
    ("001", "Đổi từ Có mặt sang Vắng có lý do", "P0",
     "Tài khoản A đang ở trạng thái \"Đã xác nhận: Có mặt\" cho cuộc họp MET-TEST-01, chưa tới giờ họp.",
     "1. Bấm nút [Vắng có lý do]\n"
     "2. Nhập lý do \"Trùng lịch khách hàng\"\n"
     "3. Bấm \"Xác nhận\"",
     "Lý do: Trùng lịch khách hàng",
     "- Nhãn đổi thành \"Đã báo: Vắng có lý do - Trùng lịch khách hàng\"\n"
     "- Nút [Vắng có lý do] ẩn, nút [Có mặt] hiện trở lại\n"
     "- Tab Điểm danh đổi theo"),

    ("002", "Đổi từ Vắng có lý do sang Có mặt thì lý do cũ bị xóa", "P0",
     "Tài khoản A đang ở \"Đã báo: Vắng có lý do - Trùng lịch khách hàng\".",
     "1. Bấm nút [Có mặt]\n"
     "2. Đọc nhãn trạng thái\n"
     "3. Mở tab Điểm danh, xem dòng của tài khoản A\n"
     "4. Bấm lại [Vắng có lý do] để mở cửa sổ",
     "—",
     "- Nhãn đổi thành \"Đã xác nhận: Có mặt\"\n"
     "- ⚠️ Cột lý do / ghi chú ở tab Điểm danh trống hẳn, không còn \"Trùng lịch khách hàng\"\n"
     "- Cửa sổ báo vắng mở ra với ô lý do TRỐNG"),

    ("003", "Sửa riêng lý do vắng bằng biểu tượng cây bút", "P0",
     "Tài khoản A đang ở \"Đã báo: Vắng có lý do - Đi công tác tại Đà Nẵng\".",
     "1. Bấm biểu tượng cây bút vuông cạnh nhãn trạng thái\n"
     "2. Quan sát ô lý do trong cửa sổ vừa mở\n"
     "3. Sửa thành \"Đi công tác tại Hải Phòng\"\n"
     "4. Bấm \"Xác nhận\"",
     "Lý do mới: Đi công tác tại Hải Phòng",
     "- ⚠️ Cửa sổ mở ra đã ĐIỀN SẴN lý do cũ, không bắt gõ lại từ đầu\n"
     "- Sau khi xác nhận, nhãn thành \"Đã báo: Vắng có lý do - Đi công tác tại Hải Phòng\"\n"
     "- Trạng thái vẫn là Vắng có lý do, không bị nhảy về Có mặt"),

    ("004", "Biểu tượng cây bút chỉ hiện ở trạng thái Vắng", "P0",
     "Cuộc họp MET-TEST-01, tài khoản A lần lượt ở 3 trạng thái.",
     "1. Ở trạng thái \"Chưa phản hồi\" - tìm biểu tượng cây bút\n"
     "2. Bấm [Có mặt], tìm lại biểu tượng cây bút\n"
     "3. Bấm [Vắng có lý do], nhập lý do, xác nhận, tìm lại biểu tượng",
     "—",
     "- Bước 1 và 2: KHÔNG có biểu tượng cây bút\n"
     "- Bước 3: biểu tượng cây bút hiện cạnh nhãn, cùng chiều cao với nút bên cạnh\n"
     "- Rê chuột vào biểu tượng hiện gợi ý \"Sửa lý do vắng mặt\""),

    ("005", "Sửa lý do rồi bấm Hủy thì giữ lý do cũ", "P1",
     "Tài khoản A đang ở \"Đã báo: Vắng có lý do - Đi công tác tại Hải Phòng\".",
     "1. Bấm biểu tượng cây bút\n"
     "2. Xóa hết và gõ lý do khác\n"
     "3. Bấm \"Hủy\"\n"
     "4. Đọc nhãn trạng thái",
     "—",
     "- Nhãn vẫn là \"Đã báo: Vắng có lý do - Đi công tác tại Hải Phòng\"\n"
     "- Mở lại cửa sổ thì ô lý do lại là lý do cũ, không phải nội dung vừa gõ dở"),

    ("006", "Đổi lựa chọn nhiều lần liên tiếp", "P1",
     "Cuộc họp MET-TEST-01, tài khoản A chưa phản hồi, chưa tới giờ họp.",
     "1. Bấm [Có mặt]\n"
     "2. Bấm [Vắng có lý do], nhập \"Lý do 1\", xác nhận\n"
     "3. Bấm [Có mặt]\n"
     "4. Bấm [Vắng có lý do], nhập \"Lý do 2\", xác nhận\n"
     "5. Tải lại trang",
     "Lý do 1 → Lý do 2",
     "- Mỗi lần đổi đều báo thành công và nhãn đổi ngay\n"
     "- Sau khi tải lại: chỉ giữ lựa chọn CUỐI CÙNG \"Đã báo: Vắng có lý do - Lý do 2\"\n"
     "- Tab Điểm danh chỉ có 1 dòng của A với lý do mới nhất"),

    ("007", "Không tự chọn được Vắng không lý do", "P0",
     "Cuộc họp MET-TEST-01, tài khoản A là khách mời nội bộ.",
     "1. Quan sát toàn bộ các nút trên thanh xác nhận",
     "—",
     "- ⚠️ Chỉ có 2 lựa chọn [Có mặt] và [Vắng có lý do]\n"
     "- Không có nút hay lựa chọn nào cho \"Vắng không lý do\""),

    ("008", "Người chủ trì đánh Vắng không lý do rồi người dùng mở lại màn", "P1",
     "Cuộc họp MET-TEST-01 chưa tới giờ. Người chủ trì vào tab Điểm danh đánh tài khoản A là "
     "\"Vắng không lý do\".",
     "1. Đăng nhập tài khoản A\n"
     "2. Mở màn Chi tiết MET-TEST-01\n"
     "3. Đọc nhãn trạng thái và đếm số nút",
     "—",
     "- Nhãn hiện \"Vắng không lý do\" (nền đỏ)\n"
     "- ⚠️ Hiện ĐỦ CẢ 2 nút [Có mặt] và [Vắng có lý do] để người dùng phản hồi lại\n"
     "- Không có biểu tượng cây bút"),
]

SEC_V = [
    ("001", "Đã qua giờ bắt đầu thì không còn nút", "P0",
     "Cuộc họp MET-TEST-04 trạng thái \"Chốt lịch\", giờ bắt đầu là 1 tiếng trước. Tài khoản A là "
     "khách mời nội bộ, chưa phản hồi.",
     "1. Mở màn Chi tiết MET-TEST-04\n"
     "2. Quan sát thanh xác nhận",
     "—",
     "- ⚠️ Không còn nút [Có mặt] / [Vắng có lý do]\n"
     "- Hiện dòng giải thích kèm biểu tượng ổ khóa: \"Cuộc họp đã đến giờ bắt đầu, việc chốt điểm danh "
     "thuộc về người chủ trì.\"\n"
     "- Nhãn trạng thái vẫn hiện để người dùng biết mình đang ở trạng thái nào"),

    ("002", "Đúng thời điểm bắt đầu là đã bị chặn", "P0",
     "Cuộc họp MET-TEST-05 có giờ bắt đầu đúng bằng thời điểm hiện tại.",
     "1. Mở màn Chi tiết MET-TEST-05\n"
     "2. Quan sát thanh xác nhận",
     "—",
     "- ⚠️ Đã bị chặn ngay tại mốc bắt đầu, không phải chờ qua giờ mới chặn"),

    ("003", "Cuộc họp trạng thái Hoàn thành", "P0",
     "Cuộc họp MET-TEST-06 đã ở trạng thái \"Hoàn thành\". Tài khoản A là khách mời nội bộ.",
     "1. Mở màn Chi tiết MET-TEST-06\n"
     "2. Quan sát thanh xác nhận",
     "—",
     "- Không còn nút nào\n"
     "- Hiện dòng giải thích \"Cuộc họp không ở trạng thái Lên lịch / Chốt lịch nên không xác nhận "
     "tham dự được.\""),

    ("004", "Cuộc họp trạng thái Hủy", "P1",
     "Cuộc họp MET-TEST-07 ở trạng thái \"Hủy\", giờ bắt đầu vẫn còn ở tương lai.",
     "1. Mở màn Chi tiết MET-TEST-07\n"
     "2. Quan sát thanh xác nhận và khối lý do hủy",
     "—",
     "- Không còn nút xác nhận, hiện dòng giải thích về trạng thái\n"
     "- Khối lý do hủy của cuộc họp vẫn hiển thị bình thường"),

    ("005", "Cuộc họp trạng thái Đang tạo", "P1",
     "Cuộc họp MET-TEST-08 còn ở trạng thái \"Đang tạo\", đã có Thành phần tham gia gồm tài khoản A.",
     "1. Đăng nhập tài khoản A, mở màn Chi tiết MET-TEST-08",
     "—",
     "- Không có nút xác nhận, hiện dòng giải thích về trạng thái"),

    ("006", "Cuộc họp không có giờ bắt đầu", "P2",
     "Cuộc họp MET-TEST-09 trạng thái \"Lên lịch\" nhưng chưa nhập Thời gian bắt đầu.",
     "1. Mở màn Chi tiết MET-TEST-09\n"
     "2. Quan sát thanh xác nhận",
     "—",
     "- ⚠️ Không cho xác nhận (không xác định được mốc chặn), hiện dòng giải thích\n"
     "- Màn hình không lỗi trắng trang"),

    ("007", "Giờ họp bị dời sang tương lai thì xác nhận lại được", "P1",
     "Cuộc họp MET-TEST-04 đã qua giờ bắt đầu nên đang bị khóa. Người chủ trì sửa Thời gian bắt đầu "
     "sang ngày mai và lưu.",
     "1. Người chủ trì dời giờ họp sang ngày mai\n"
     "2. Tài khoản A tải lại màn Chi tiết MET-TEST-04",
     "Thời gian bắt đầu mới: ngày mai",
     "- Cụm 2 nút hiện trở lại, dòng giải thích khóa biến mất"),

    ("008", "Gọi thẳng chức năng xác nhận sau khi đã qua giờ họp", "P0",
     "Cuộc họp MET-TEST-04 đã qua giờ bắt đầu. Tài khoản A là khách mời nội bộ. Dành cho tester "
     "kỹ thuật.",
     "1. Dùng công cụ kiểm thử gọi thẳng chức năng Xác nhận tham dự, bỏ qua giao diện\n"
     "2. Đọc thông báo trả về\n"
     "3. Kiểm tab Điểm danh",
     "Lựa chọn gửi lên: Có mặt",
     "- ⚠️ Bị chặn kèm đúng nội dung \"Cuộc họp đã đến giờ bắt đầu, việc chốt điểm danh thuộc về người "
     "chủ trì.\" - không dựa vào việc giao diện đã ẩn nút\n"
     "- Dòng điểm danh của A không đổi"),
]

SEC_VI = [
    ("001", "Cụm nút hiện trên dòng thông báo Lên lịch", "P0",
     "Người chủ trì vừa chuyển cuộc họp MET-TEST-10 sang trạng thái \"Lên lịch\", tài khoản A là "
     "khách mời nội bộ và vừa nhận thông báo.",
     "1. Đăng nhập tài khoản A\n"
     "2. Bấm biểu tượng quả chuông\n"
     "3. Tìm dòng thông báo về cuộc họp MET-TEST-10",
     "—",
     "- Dòng thông báo có kèm 2 nút [Có mặt] và [Vắng có lý do]\n"
     "- Nội dung thông báo hiện đủ tên cuộc họp, thời gian, địa điểm, hình thức"),

    ("002", "Cụm nút hiện trên dòng thông báo Chốt lịch", "P0",
     "Người chủ trì chuyển cuộc họp MET-TEST-10 sang \"Chốt lịch\".",
     "1. Tài khoản A bấm biểu tượng quả chuông\n"
     "2. Tìm dòng thông báo Chốt lịch của MET-TEST-10",
     "—",
     "- Dòng thông báo có kèm cụm nút xác nhận"),

    ("003", "Thông báo Thay đổi lịch không có cụm nút", "P1",
     "Người chủ trì sửa thời gian cuộc họp MET-TEST-10 (không đổi trạng thái) nên tài khoản A nhận "
     "thông báo thay đổi lịch.",
     "1. Tài khoản A bấm biểu tượng quả chuông\n"
     "2. Tìm dòng thông báo thay đổi lịch",
     "—",
     "- ⚠️ Dòng này KHÔNG có cụm nút xác nhận - đây là hành vi hiện tại đã thống nhất, không phải lỗi"),

    ("004", "Bảng thông báo không đóng khi bấm nút Có mặt", "P0",
     "Tài khoản A đang mở bảng thông báo, thấy dòng thông báo MET-TEST-10 kèm cụm nút.",
     "1. Bấm nút [Có mặt] ngay trên dòng thông báo\n"
     "2. Quan sát bảng thông báo và địa chỉ trang",
     "—",
     "- ⚠️ Bảng thông báo VẪN MỞ, không bị đóng\n"
     "- ⚠️ KHÔNG chuyển sang màn Chi tiết cuộc họp\n"
     "- Hiện thông báo xanh \"Xác nhận tham dự thành công\", nhãn trên dòng đổi thành \"Đã xác nhận: "
     "Có mặt\""),

    ("005", "Bảng thông báo không đóng khi bấm nút Vắng có lý do", "P0",
     "Tài khoản A đang mở bảng thông báo, thấy dòng thông báo MET-TEST-10 kèm cụm nút.",
     "1. Bấm nút [Vắng có lý do]\n"
     "2. Quan sát bảng thông báo lúc cửa sổ nhập lý do đang mở\n"
     "3. Nhập lý do rồi bấm \"Xác nhận\"\n"
     "4. Quan sát lại bảng thông báo",
     "Lý do: Trùng lịch công tác",
     "- ⚠️ Bảng thông báo vẫn mở suốt lúc cửa sổ nhập lý do hiện\n"
     "- Sau khi xác nhận, bảng thông báo vẫn mở, nhãn trên dòng đổi thành \"Đã báo: Vắng có lý do - "
     "Trùng lịch công tác\"\n"
     "- ⚠️ Hai nút hành xử GIỐNG NHAU, không nút nào làm đóng bảng"),

    ("006", "Bấm Hủy ở cửa sổ nhập lý do mở từ chuông", "P0",
     "Cửa sổ nhập lý do được mở từ dòng thông báo trên chuông.",
     "1. Bấm \"Hủy\"\n"
     "2. Quan sát bảng thông báo",
     "—",
     "- Cửa sổ đóng, bảng thông báo VẪN MỞ\n"
     "- Không ghi nhận phản hồi nào"),

    ("007", "Mở chuông là thấy ngay trạng thái đã phản hồi", "P0",
     "Tài khoản A đã xác nhận \"Có mặt\" cho MET-TEST-10 ở màn Chi tiết từ hôm trước. Bảng thông báo "
     "đang đóng.",
     "1. Bấm biểu tượng quả chuông để mở bảng thông báo\n"
     "2. Nhìn dòng thông báo của MET-TEST-10 ngay khi bảng vừa mở",
     "—",
     "- ⚠️ Hiện sẵn nhãn \"Đã xác nhận: Có mặt\" và ẩn sẵn nút [Có mặt], không phải bấm gì trước\n"
     "- Dòng của cuộc họp chưa phản hồi thì hiện đủ 2 nút"),

    ("008", "Nhiều dòng thông báo cùng lúc chỉ tra trạng thái một lần", "P1",
     "Bảng thông báo của tài khoản A đang có 10 dòng thông báo cuộc họp khác nhau.",
     "1. Mở bảng thông báo\n"
     "2. Quan sát thời gian hiển thị và trạng thái từng dòng",
     "10 dòng thông báo cuộc họp",
     "- Bảng hiện ra không bị chậm hay giật\n"
     "- Mọi dòng đều hiện đúng trạng thái phản hồi của chính tài khoản A\n"
     "- ⚠️ Hệ thống chỉ tra trạng thái MỘT lần cho cả bảng, không tra theo từng dòng"),

    ("009", "Giao diện cụm nút trong bảng thông báo thẳng hàng", "P1",
     "Bảng thông báo đang hiện dòng thông báo có nhãn trạng thái và cụm nút.",
     "1. Nhìn nhãn trạng thái và 2 nút trên dòng thông báo",
     "—",
     "- ⚠️ Nhãn và các nút cùng cỡ chữ, cùng chiều cao, tâm trên một đường ngang - chữ trong nhãn "
     "không bị dính mép trên\n"
     "- Lý do dài bị cắt bằng dấu ba chấm, không đẩy nút xuống dòng"),

    ("010", "Tra trạng thái thất bại thì quay về hành vi cũ", "P2",
     "Ngắt mạng ngay trước khi mở bảng thông báo.",
     "1. Ngắt mạng\n"
     "2. Mở bảng thông báo\n"
     "3. Quan sát dòng thông báo cuộc họp",
     "—",
     "- Không hiện lỗi đỏ làm hỏng bảng thông báo\n"
     "- Dòng cuộc họp hiện đủ 2 nút như khi chưa biết trạng thái (không hiện nhãn sai)"),

    ("011", "Bấm vào phần nội dung thông báo vẫn điều hướng bình thường", "P0",
     "Bảng thông báo đang hiện dòng thông báo cuộc họp MET-TEST-10 kèm cụm nút.",
     "1. Bấm vào phần chữ của dòng thông báo (tránh vùng nút)\n"
     "2. Quan sát",
     "—",
     "- Chuyển sang màn Chi tiết đúng cuộc họp\n"
     "- Dòng thông báo được đánh dấu đã đọc như cũ"),
]

SEC_VII = [
    ("001", "Tab Điểm danh cập nhật ngay sau khi xác nhận", "P0",
     "Tài khoản A đang mở màn Chi tiết MET-TEST-01, dòng của A ở tab Điểm danh đang là "
     "\"Chưa điểm danh\".",
     "1. Bấm nút [Có mặt] trên thanh xác nhận\n"
     "2. Chuyển sang tab \"Điểm danh\"\n"
     "3. Tìm dòng của chính tài khoản A",
     "—",
     "- ⚠️ Dòng của A hiện \"Có mặt\" ngay, KHÔNG phải tải lại trang\n"
     "- Dòng của những người khác không đổi"),

    ("002", "Lý do vắng hiện ở tab Điểm danh", "P0",
     "Tài khoản A vừa báo vắng với lý do \"Đi công tác tại Đà Nẵng\".",
     "1. Chuyển sang tab \"Điểm danh\"\n"
     "2. Xem dòng của tài khoản A",
     "Lý do: Đi công tác tại Đà Nẵng",
     "- Cột trạng thái hiện \"Vắng có lý do\"\n"
     "- Cột ghi chú / lý do hiện đúng \"Đi công tác tại Đà Nẵng\""),

    ("003", "Nhãn Chưa điểm danh cho người chưa phản hồi", "P1",
     "Cuộc họp MET-TEST-01 có 5 khách mời nội bộ, 3 người chưa ai phản hồi.",
     "1. Mở tab \"Điểm danh\"\n"
     "2. Đọc cột trạng thái của 3 người chưa phản hồi",
     "—",
     "- ⚠️ Hiện \"Chưa điểm danh\", không hiện \"Dự kiến tham gia\""),

    ("004", "Người chủ trì ghi đè phản hồi của khách mời", "P0",
     "Tài khoản A đã tự báo \"Vắng có lý do - Đi công tác\". Cuộc họp đã tới giờ và đang diễn ra.",
     "1. Người chủ trì mở tab Điểm danh\n"
     "2. Sửa dòng của tài khoản A thành \"Có mặt\"\n"
     "3. Lưu\n"
     "4. Tài khoản A tải lại màn Chi tiết",
     "—",
     "- Dòng của A ở tab Điểm danh là \"Có mặt\"\n"
     "- Tài khoản A thấy nhãn \"Đã xác nhận: Có mặt\" nhưng không còn nút để đổi (đã qua giờ)\n"
     "- ⚠️ Hệ thống không phân biệt phản hồi tự báo và điểm danh do chủ trì sửa - đây là thiết kế đã "
     "thống nhất"),

    ("005", "Phản hồi từ chuông đồng bộ sang màn Chi tiết đang mở", "P0",
     "Tài khoản A đang mở màn Chi tiết MET-TEST-10 ở trạng thái \"Chưa phản hồi\", đồng thời mở bảng "
     "thông báo có dòng của chính cuộc họp đó.",
     "1. Bấm nút [Có mặt] trên dòng thông báo ở chuông\n"
     "2. Đóng bảng thông báo\n"
     "3. Nhìn thanh xác nhận ở màn Chi tiết phía sau\n"
     "4. Mở tab Điểm danh",
     "—",
     "- ⚠️ Thanh xác nhận ở màn Chi tiết đổi theo ngay, không phải tải lại trang\n"
     "- Tab Điểm danh cũng đã cập nhật dòng của A\n"
     "- Không có hai trạng thái mâu thuẫn trên cùng màn hình"),

    ("006", "Phản hồi ở màn Chi tiết đồng bộ sang dòng thông báo", "P1",
     "Tài khoản A mở màn Chi tiết MET-TEST-10 và mở sẵn bảng thông báo có dòng của cuộc họp đó.",
     "1. Bấm [Vắng có lý do] trên thanh xác nhận, nhập lý do, xác nhận\n"
     "2. Nhìn dòng thông báo tương ứng trên bảng thông báo",
     "Lý do: Bận lịch khác",
     "- Nhãn trên dòng thông báo đổi thành \"Đã báo: Vắng có lý do - Bận lịch khác\""),

    ("007", "Cùng một cuộc họp có nhiều dòng thông báo", "P2",
     "Cuộc họp MET-TEST-10 sinh ra 2 dòng thông báo (Lên lịch và Chốt lịch) đều nằm trên bảng "
     "thông báo của tài khoản A.",
     "1. Mở bảng thông báo\n"
     "2. Bấm [Có mặt] ở dòng thông báo thứ nhất\n"
     "3. Nhìn dòng thông báo thứ hai",
     "—",
     "- ⚠️ Cả 2 dòng cùng đổi sang \"Đã xác nhận: Có mặt\", không để một dòng còn 2 nút\n"
     "- Cửa sổ nhập lý do mở từ dòng nào chỉ ảnh hưởng dòng đó (không mở nhầm nhiều cửa sổ)"),
]

SEC_VIII = [
    ("001", "Hai người cùng phản hồi một lúc", "P1",
     "Cuộc họp MET-TEST-01, tài khoản A và tài khoản E đều là khách mời nội bộ, mở màn Chi tiết trên "
     "2 trình duyệt khác nhau.",
     "1. Cùng lúc: A bấm [Có mặt], E báo vắng với lý do \"Bận\"\n"
     "2. Cả hai tải lại trang\n"
     "3. Mở tab Điểm danh",
     "—",
     "- Dòng của A là \"Có mặt\", dòng của E là \"Vắng có lý do - Bận\"\n"
     "- Không ai ghi đè lên ai"),

    ("002", "Cuộc họp bị hủy trong lúc người dùng đang mở màn", "P1",
     "Tài khoản A đang mở màn Chi tiết MET-TEST-01 với cụm nút hiện. Người chủ trì hủy cuộc họp ở "
     "phiên khác.",
     "1. Tài khoản A bấm [Có mặt] mà không tải lại trang\n"
     "2. Đọc thông báo",
     "—",
     "- ⚠️ Hệ thống từ chối kèm nội dung \"Cuộc họp không ở trạng thái Lên lịch / Chốt lịch nên không "
     "xác nhận tham dự được.\"\n"
     "- Không treo trang, nhãn trạng thái không đổi"),

    ("003", "Người dùng bị đưa ra khỏi Thành phần tham gia", "P1",
     "Tài khoản A đang mở màn Chi tiết MET-TEST-01. Người chủ trì xóa A khỏi Thành phần tham gia phía "
     "Công ty và lưu.",
     "1. Tài khoản A bấm [Có mặt] mà không tải lại trang\n"
     "2. Đọc thông báo\n"
     "3. Tải lại trang",
     "—",
     "- Hệ thống từ chối kèm nội dung \"Bạn không nằm trong Thành phần tham gia nội bộ của cuộc họp "
     "này.\"\n"
     "- Sau khi tải lại, thanh xác nhận biến mất"),

    ("004", "Cuộc họp bị xóa trong lúc người dùng đang mở màn", "P2",
     "Tài khoản A đang mở màn Chi tiết một cuộc họp vừa bị người có quyền xóa.",
     "1. Bấm [Có mặt]\n"
     "2. Đọc thông báo",
     "—",
     "- Hệ thống báo không tìm thấy cuộc họp, không treo trang"),

    ("005", "Bấm liên tiếp nhiều lần vào nút Có mặt", "P2",
     "Tài khoản A đang ở \"Chưa phản hồi\" cho MET-TEST-01.",
     "1. Bấm nhanh 3 lần liên tiếp vào nút [Có mặt]\n"
     "2. Đếm số thông báo hiện ra\n"
     "3. Mở tab Điểm danh",
     "—",
     "- Chỉ ghi nhận 1 lần, không sinh nhiều dòng điểm danh trùng\n"
     "- Nút tạm khóa trong lúc đang gửi, không cho bấm chồng"),

    ("006", "Cuộc họp có rất nhiều khách mời nội bộ", "P2",
     "Cuộc họp MET-TEST-11 có 80 người trong Thành phần tham gia phía Công ty, tài khoản A là một "
     "trong số đó.",
     "1. Mở màn Chi tiết MET-TEST-11\n"
     "2. Bấm [Có mặt]\n"
     "3. Mở tab Điểm danh, tìm dòng của A",
     "—",
     "- Thanh xác nhận hiện bình thường, phản hồi ghi trong vòng 2 giây\n"
     "- Chỉ dòng của A đổi, 79 dòng còn lại giữ nguyên"),
]

SEC_IX = [
    ("001", "Luồng đầy đủ: nhận thông báo, báo vắng, đổi ý, chủ trì chốt", "P0",
     "Tài khoản D là người chủ trì, tài khoản A là khách mời nội bộ. Cuộc họp MET-TEST-12 mới lập, "
     "giờ bắt đầu là ngày mai.",
     "1. Tài khoản D chuyển cuộc họp sang \"Chốt lịch\"\n"
     "2. Tài khoản A mở bảng thông báo, bấm [Vắng có lý do], nhập \"Đi công tác\", xác nhận\n"
     "3. Tài khoản A mở màn Chi tiết, kiểm nhãn trạng thái và tab Điểm danh\n"
     "4. Tài khoản A bấm biểu tượng cây bút, sửa lý do thành \"Đi công tác Hà Nội\", xác nhận\n"
     "5. Tài khoản A bấm [Có mặt]\n"
     "6. Tài khoản D mở tab Điểm danh của cuộc họp",
     "Lý do: Đi công tác → Đi công tác Hà Nội",
     "- Bước 2: bảng thông báo vẫn mở, nhãn đổi ngay\n"
     "- Bước 3: nhãn \"Đã báo: Vắng có lý do - Đi công tác\", tab Điểm danh đúng trạng thái và lý do\n"
     "- Bước 4: cửa sổ điền sẵn lý do cũ, sửa xong nhãn đổi theo, trạng thái vẫn là Vắng\n"
     "- Bước 5: nhãn thành \"Đã xác nhận: Có mặt\", lý do cũ bị xóa sạch\n"
     "- Bước 6: người chủ trì thấy dòng của A là \"Có mặt\", cột lý do trống"),

    ("002", "Luồng đầy đủ: xác nhận trước, hết hạn, chủ trì chốt điểm danh", "P0",
     "Cuộc họp MET-TEST-13 trạng thái \"Chốt lịch\", giờ bắt đầu sau 10 phút nữa. Tài khoản A là "
     "khách mời nội bộ.",
     "1. Tài khoản A bấm [Có mặt] trước giờ họp\n"
     "2. Chờ qua giờ bắt đầu, tài khoản A tải lại màn Chi tiết\n"
     "3. Tài khoản D (chủ trì) mở tab Điểm danh, đổi dòng của A thành \"Vắng không lý do\", lưu\n"
     "4. Tài khoản A tải lại màn Chi tiết",
     "—",
     "- Bước 1: xác nhận thành công\n"
     "- Bước 2: nhãn vẫn là \"Đã xác nhận: Có mặt\" nhưng không còn nút, hiện dòng giải thích đã tới "
     "giờ họp\n"
     "- Bước 4: nhãn đổi thành \"Vắng không lý do\", vẫn không có nút nào để đổi lại"),

    ("003", "Luồng nhiều khách mời phản hồi khác nhau", "P1",
     "Cuộc họp MET-TEST-14 trạng thái \"Chốt lịch\", giờ bắt đầu ngày mai, 4 khách mời nội bộ A, E, "
     "F, G.",
     "1. A bấm [Có mặt]\n"
     "2. E báo vắng lý do \"Nghỉ phép\"\n"
     "3. F không phản hồi\n"
     "4. G bấm [Có mặt] rồi đổi sang báo vắng lý do \"Trùng lịch\"\n"
     "5. Người chủ trì mở tab Điểm danh",
     "—",
     "- Tab Điểm danh: A \"Có mặt\"; E \"Vắng có lý do - Nghỉ phép\"; F \"Chưa điểm danh\"; "
     "G \"Vắng có lý do - Trùng lịch\"\n"
     "- Không dòng nào bị lẫn lý do của người khác"),
]

SECTIONS = [
    ("I", "HIỂN THỊ THANH XÁC NHẬN & TRUY CẬP", SEC_I),
    ("II", "XÁC NHẬN CÓ MẶT", SEC_II),
    ("III", "BÁO VẮNG CÓ LÝ DO", SEC_III),
    ("IV", "ĐỔI LẠI LỰA CHỌN & SỬA LÝ DO", SEC_IV),
    ("V", "ĐIỀU KIỆN KHÓA (TRẠNG THÁI & THỜI GIAN)", SEC_V),
    ("VI", "XÁC NHẬN NGAY TRÊN THÔNG BÁO (CHUÔNG)", SEC_VI),
    ("VII", "ĐỒNG BỘ VỚI TAB ĐIỂM DANH", SEC_VII),
    ("VIII", "THAO TÁC ĐỒNG THỜI & TRƯỜNG HỢP BIÊN", SEC_VIII),
    ("IX", "LUỒNG ĐẦU CUỐI", SEC_IX),
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testcase.xlsx")
    build(
        output_file=out,
        sheet_name="Trang tính1",
        feature_name="Xác nhận tham dự trước cuộc họp",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )
