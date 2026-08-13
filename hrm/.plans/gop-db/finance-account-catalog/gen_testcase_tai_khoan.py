# -*- coding: utf-8 -*-
"""Sinh testcase cho man Danh muc tai khoan (phan he Tai chinh).

Chay:  python gen_testcase_tai_khoan.py
"""
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "..", ".claude", "skills", "testcase-documenter", "assets"))

from tc_engine import build  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(HERE, "testcase - Danh muc tai khoan.xlsx")
SHEET_NAME = "Trang tính1"
FEATURE_NAME = "Danh mục tài khoản - Cập nhật ngày 13/08/2026"
MODULE_NAME = "Danh mục tài khoản"

# ============================================================================
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Quản lý hệ thống tài khoản kế toán 3 bậc dùng chung cho toàn hệ thống (hạch toán chứng từ, "
     "sổ sách, báo cáo tài chính, theo dõi công nợ).\n"
     "Màn hình nằm ở phân hệ Tài chính → nhóm menu Danh mục → Danh mục tài khoản.\n"
     "Đây là màn được chuyển từ hệ thống cũ sang, hai cổng dùng CHUNG một danh mục tài khoản."),

    ("2. Đối tượng được tính / hiển thị",
     "- Toàn bộ tài khoản trong danh mục, KHÔNG phân theo công ty / phòng ban — ai có quyền vào "
     "màn thì thấy đủ như nhau.\n"
     "- Hiển thị cả tài khoản Hoạt động và tài khoản đang Khóa.\n"
     "- Mỗi dòng gồm 11 cột: STT, Cấp 1, Cấp 2, Cấp 3, Tên tài khoản, Loại tài khoản, "
     "Theo dõi công nợ, Ngày tạo, Cập nhật, Trạng thái, Hành động.\n"
     "- Số tài khoản được đặt vào đúng cột Cấp 1 / Cấp 2 / Cấp 3 theo bậc của nó, ba cột còn lại "
     "để trống — nhờ vậy nhìn vào bảng là thấy ngay cây tài khoản thụt lề theo bậc.\n"
     "- Cột Theo dõi công nợ chỉ hiện dấu đánh dấu ở những tài khoản có bật, tài khoản không bật "
     "thì để trống."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Không có tài khoản nào bị ẩn khỏi màn này.\n"
     "- Tài khoản đang Khóa VẪN hiện ở đây nhưng KHÔNG còn được chọn khi hạch toán chứng từ mới.\n"
     "- Trong danh sách chọn Tài khoản mẹ ở màn thêm/sửa: chỉ hiện các tài khoản đúng bậc liền "
     "trên bậc đang chọn (bậc 2 chỉ chọn được mẹ bậc 1, bậc 3 chỉ chọn được mẹ bậc 2)."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Không áp dụng. Màn hình không có ô lọc theo khoảng thời gian.\n"
     "Hai cột Ngày tạo và Cập nhật chỉ để xem, không phải điều kiện lọc."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Cây 3 bậc, gắn kết theo SỐ tài khoản chứ không theo tên:\n"
     "- Bậc 1: số tài khoản 3 chữ số, KHÔNG có tài khoản mẹ. Ví dụ 131.\n"
     "- Bậc 2: có tài khoản mẹ là một tài khoản bậc 1. Ví dụ 1311 (mẹ là 131).\n"
     "- Bậc 3: có tài khoản mẹ là một tài khoản bậc 2. Ví dụ 13111 (mẹ là 1311).\n"
     "Ba quy tắc bắt buộc của cây:\n"
     "a) Tài khoản mẹ phải đúng bậc liền trên.\n"
     "b) Số tài khoản con phải BẮT ĐẦU BẰNG số tài khoản mẹ.\n"
     "c) Tài khoản đang có tài khoản con thì KHÔNG được đổi Bậc và KHÔNG được đổi Số tài khoản."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "Không cộng dồn. Mỗi tài khoản là một dòng độc lập.\n"
     "Chống trùng: Số tài khoản là duy nhất trong toàn danh mục; trùng sẽ báo "
     "\"Số tài khoản đã tồn tại\".\n"
     "Tên tài khoản KHÔNG bắt buộc duy nhất — được phép trùng."),

    ("7. Phân quyền cấp",
     "Hai quyền dành riêng cho màn này:\n"
     "- \"Xem danh mục tài khoản\": vào màn hình, xem danh sách, mở xem chi tiết, xem lịch sử "
     "chỉnh sửa, in danh sách, xuất Excel.\n"
     "- \"Quản lý danh mục tài khoản\": thêm mới, sửa, khóa, mở khóa, xóa, nhập từ Excel.\n"
     "Không có quyền nào trong hai quyền trên thì không vào được màn hình.\n"
     "Danh mục KHÔNG phân quyền theo công ty / phòng ban / bộ phận.\n"
     "⚠️ Ngoài quyền, còn một ràng buộc riêng: các thao tác Khóa, Mở khóa và Xóa chỉ dành cho "
     "CHÍNH NGƯỜI ĐÃ TẠO tài khoản đó. Người khác dù có quyền Quản lý cũng không thao tác được."),

    ("8. Cách tính các ô thống kê",
     "- Dòng \"Hiển thị a - b / N\" dưới bảng: a là dòng đầu của trang đang xem, b là dòng cuối, "
     "N là tổng số tài khoản khớp bộ lọc hiện tại.\n"
     "- Cột STT đánh theo trang: trang 2 với cỡ trang 10 thì bắt đầu từ 11.\n"
     "- Bản in danh sách lấy đúng tập dữ liệu đang lọc, không phải toàn bộ danh mục.\n"
     "- Bảng nhập từ Excel: số dòng hợp lệ và số dòng lỗi được đếm riêng."),

    ("9. Ghi chú đọc bảng",
     "- Số tài khoản chỉ được nhập CHỮ SỐ, từ 3 đến 15 chữ số. Chữ cái, dấu chấm, dấu gạch đều bị chặn.\n"
     "- Cột Cấp 1 / Cấp 2 / Cấp 3 KHÔNG phải ba số khác nhau — chỉ là một số tài khoản được đặt "
     "vào đúng cột theo bậc. Đọc nhầm thành ba giá trị là sai.\n"
     "- Nút Khóa / Mở khóa nằm NGAY TRONG cột Trạng thái, không nằm ở cột Hành động.\n"
     "- Tài khoản đang ở trạng thái Khóa thì nút Sửa bị vô hiệu; muốn sửa phải Mở khóa trước.\n"
     "- Người không phải người tạo sẽ thấy nút Khóa / Mở khóa / Xóa bị mờ, dù có quyền Quản lý. "
     "Đây là thiết kế, không phải lỗi.\n"
     "- Bộ lọc được hệ thống ghi nhớ trong 10 phút. Kiểm thử bộ lọc nên bấm Làm mới trước mỗi kịch bản.\n"
     "- Thêm mới và Sửa mở ra TRANG RIÊNG, không phải cửa sổ nhỏ như các danh mục khác.\n"
     "- Mọi thay đổi đều xem lại được qua nút Lịch sử chỉnh sửa trên từng dòng."),
]

# ============================================================================
PRE_PERM = ("Có sẵn 3 tài khoản đăng nhập: A chỉ có quyền \"Xem danh mục tài khoản\"; "
            "B có quyền \"Quản lý danh mục tài khoản\" VÀ là người đã tạo tài khoản 999 (bậc 1, "
            "chưa dùng ở chứng từ nào, chưa có tài khoản con); C có quyền Quản lý nhưng KHÔNG "
            "phải người tạo tài khoản 999. Danh mục đang có 308 tài khoản.")

ROLE_TCS = [
    ("01", "Vào màn hình khi chỉ có quyền Xem", "P0", PRE_PERM,
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Vào phân hệ Tài chính → Danh mục → Danh mục tài khoản", "Tài khoản A",
     "- Vào được màn hình, bảng hiển thị dữ liệu\n"
     "- KHÔNG có nút Tạo mới, KHÔNG có nút Import Excel\n"
     "- Trên mỗi dòng chỉ còn nút Lịch sử chỉnh sửa; KHÔNG có nút Sửa, nút Xóa\n"
     "- Cột Trạng thái không có nút Khóa / Mở khóa\n"
     "- Vẫn có nút In danh sách và nút Xuất Excel"),

    ("02", "Vào màn hình khi có quyền Quản lý", "P0", PRE_PERM,
     "1. Đăng nhập bằng tài khoản B\n2. Vào Danh mục tài khoản", "Tài khoản B",
     "- Có đủ 4 nút dưới bảng: Tạo mới, In danh sách, Xuất Excel, Import Excel\n"
     "- Mỗi dòng có đủ 3 nút: Sửa, Lịch sử chỉnh sửa, Xóa\n"
     "- Cột Trạng thái có nút Khóa hoặc Mở khóa"),

    ("03", "Chặn vào màn hình khi không có quyền nào", "P0",
     "Tài khoản D không có cả hai quyền của màn này.",
     "1. Đăng nhập bằng tài khoản D\n2. Tìm mục Danh mục tài khoản trong phân hệ Tài chính\n"
     "3. Dán thẳng đường dẫn màn hình vào thanh địa chỉ", "Tài khoản D",
     "- Mục menu KHÔNG hiện\n"
     "- Dán thẳng đường dẫn thì hệ thống chuyển sang trang báo không tìm thấy, không lộ dữ liệu"),

    ("04", "Chặn vào trang Thêm mới khi chỉ có quyền Xem", "P0", PRE_PERM,
     "1. Đăng nhập bằng tài khoản A\n2. Dán thẳng đường dẫn trang Thêm tài khoản vào thanh địa chỉ",
     "Tài khoản A",
     "- Hệ thống không cho vào trang thêm mới, chuyển sang trang báo không tìm thấy hoặc "
     "quay về danh sách kèm thông báo không có quyền"),

    ("05", "Chặn Thêm mới khi bỏ qua giao diện", "P0", PRE_PERM,
     "1. Đăng nhập bằng tài khoản A, lấy mã đăng nhập\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Thêm tài khoản, bỏ qua giao diện\n"
     "3. Mở lại màn hình kiểm tra", "Số tài khoản: 998; Tên: Tài khoản thử; Bậc 1",
     "- Hệ thống từ chối, báo không có quyền\n- Không xuất hiện tài khoản 998"),

    ("06", "Chặn Sửa khi bỏ qua giao diện", "P0", PRE_PERM,
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Sửa tài khoản 999\n"
     "3. Mở lại màn hình", "Đổi tên thành \"Bị sửa trộm\"",
     "- Hệ thống từ chối, báo không có quyền\n- Tên cũ giữ nguyên"),

    ("07", "Chặn Xóa khi bỏ qua giao diện", "P0", PRE_PERM,
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa tài khoản 999\n"
     "3. Mở lại màn hình", "Tài khoản 999 (về nghiệp vụ là xóa được)",
     "- Hệ thống từ chối, báo không có quyền\n- Tài khoản 999 vẫn còn"),

    ("08", "Chặn Xóa của người có quyền nhưng không phải người tạo", "P0", PRE_PERM,
     "1. Đăng nhập bằng tài khoản C (có quyền Quản lý, KHÔNG phải người tạo 999)\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa tài khoản 999\n"
     "3. Mở lại màn hình", "Tài khoản C xóa tài khoản 999 của người khác",
     "- Hệ thống từ chối\n- Tài khoản 999 vẫn còn\n"
     "⚠️ Đây là ràng buộc riêng của màn này: chỉ chính người tạo mới được xóa"),

    ("09", "Chặn Khóa của người có quyền nhưng không phải người tạo", "P0", PRE_PERM,
     "1. Đăng nhập bằng tài khoản C\n"
     "2. Mở màn hình, rê chuột vào nút Khóa của dòng 999\n"
     "3. Dùng công cụ kiểm thử API gọi thẳng chức năng Khóa tài khoản 999", "Tài khoản C",
     "- Trên giao diện nút Khóa bị mờ\n"
     "- Gọi thẳng cũng bị từ chối, trạng thái tài khoản 999 không đổi"),

    ("10", "Chặn Import Excel khi bỏ qua giao diện", "P1", PRE_PERM,
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Nhập tài khoản từ Excel\n"
     "3. Mở lại màn hình", "File Excel 3 dòng hợp lệ",
     "- Hệ thống từ chối, báo không có quyền\n- Danh sách không tăng thêm dòng nào"),

    ("11", "Người chỉ có quyền Xem vẫn in và xuất Excel được", "P1", PRE_PERM,
     "1. Đăng nhập bằng tài khoản A\n2. Bấm In danh sách\n3. Bấm Xuất Excel", "Tài khoản A",
     "- Cả hai chức năng đều dùng được bình thường"),
]

# ============================================================================
PRE = ("Đăng nhập bằng tài khoản có quyền \"Quản lý danh mục tài khoản\". "
       "Danh mục có 308 tài khoản đủ cả 3 bậc, ví dụ 131 (bậc 1) - 1311 (bậc 2) - 13111 (bậc 3). "
       "Người đăng nhập là người đã tạo tài khoản 999 (bậc 1, chưa có con, chưa dùng ở chứng từ). "
       "Có ít nhất 1 tài khoản đang ở trạng thái Khóa và 1 tài khoản có bật Theo dõi công nợ.")

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", [
        ("001", "Mở màn hình lần đầu", "P0", PRE,
         "1. Vào phân hệ Tài chính → Danh mục → Danh mục tài khoản\n2. Quan sát toàn màn hình", "—",
         "- Tiêu đề trang và tiêu đề bảng đều là \"Danh mục tài khoản\"\n"
         "- Khối lọc có tiêu đề \"Bộ lọc danh mục tài khoản\", mặc định thu gọn\n"
         "- Bảng có đủ 11 cột đúng thứ tự: STT, Cấp 1, Cấp 2, Cấp 3, Tên tài khoản, Loại tài khoản, "
         "Theo dõi công nợ, Ngày tạo, Cập nhật, Trạng thái, Hành động\n"
         "- Dưới bảng có 4 nút: Tạo mới, In danh sách, Xuất Excel, Import Excel"),

        ("002", "Số tài khoản nằm đúng cột theo bậc", "P0", PRE,
         "1. Mở màn hình\n2. Tìm ba dòng 131, 1311, 13111 và nhìn 3 cột Cấp", "—",
         "- Dòng 131 chỉ điền cột Cấp 1, hai cột Cấp 2 và Cấp 3 để trống\n"
         "- Dòng 1311 chỉ điền cột Cấp 2\n- Dòng 13111 chỉ điền cột Cấp 3\n"
         "⚠️ Nhìn ngang là thấy cây thụt lề theo bậc; số chỉ xuất hiện MỘT lần trên mỗi dòng"),

        ("003", "Cột Theo dõi công nợ", "P1", PRE,
         "1. Mở màn hình\n2. So sánh dòng có bật và dòng không bật theo dõi công nợ", "—",
         "- Dòng có bật hiện dấu đánh dấu, rê chuột hiện chú thích \"Có theo dõi công nợ\"\n"
         "- Dòng không bật để trống, không hiện dấu gạch hay chữ \"Không\""),

        ("004", "Cột Loại tài khoản hiện tên loại", "P0", PRE,
         "1. Mở màn hình\n2. Nhìn cột Loại tài khoản", "—",
         "- Hiện TÊN loại tài khoản bằng tiếng Việt (ví dụ \"Tài khoản tài sản\"), "
         "không hiện con số\n- Tài khoản chưa gán loại thì để trống, không lỗi"),

        ("005", "Cột Ngày tạo và Cập nhật", "P1", PRE,
         "1. Mở màn hình\n2. Nhìn hai cột Ngày tạo và Cập nhật", "—",
         "- Ngày tạo hiện thời điểm tạo kèm tên người tạo\n"
         "- Cập nhật hiện thời điểm sửa gần nhất kèm tên người cập nhật"),

        ("006", "Cột Trạng thái hiển thị đúng nhãn", "P0", PRE,
         "1. Mở màn hình\n2. Đối chiếu cột Trạng thái", "—",
         "- Tài khoản đang dùng hiện nhãn \"Hoạt động\"\n- Tài khoản bị khóa hiện nhãn \"Khóa\""),

        ("007", "Vị trí nút Khóa / Mở khóa", "P1", PRE,
         "1. Mở màn hình\n2. Nhìn cột Trạng thái và cột Hành động", "—",
         "- Nút Khóa / Mở khóa nằm cạnh nhãn trạng thái, TRONG cột Trạng thái\n"
         "- Cột Hành động có 3 nút: Sửa, Lịch sử chỉnh sửa, Xóa\n"
         "⚠️ Màn này KHÁC các danh mục khác: KHÔNG có nút Xem riêng, "
         "muốn xem chi tiết thì mở trang Sửa"),

        ("008", "Tên tài khoản dài được xuống dòng", "P2", PRE,
         "1. Tìm dòng có Tên tài khoản dài (ví dụ \"Phải thu của khách hàng ngắn hạn\")", "—",
         "- Tên được xuống dòng trong ô, hiện đầy đủ, không cắt cụt, không tràn bảng"),

        ("009", "Bảng trống khi bộ lọc không khớp gì", "P1", PRE,
         "1. Gõ \"khongtontai123\" vào ô tìm nhanh\n2. Bấm Tìm kiếm", "khongtontai123",
         "- Bảng hiện thông báo không có dữ liệu phù hợp, tổng dưới bảng là 0"),

        ("010", "Màn hình mở nhanh với 308 bản ghi", "P1", PRE,
         "1. Mở màn hình và bấm giờ đến khi bảng hiện xong", "—",
         "- Bảng hiện trong vòng vài giây, không treo trang\n"
         "- Danh sách chỉ tải MỘT lượt, không chớp tải hai lần"),
    ]),

    ("II", "BỘ LỌC & TÌM KIẾM", [
        ("001", "Tìm nhanh theo Số tài khoản", "P0", PRE,
         "1. Gõ \"1311\" vào ô tìm nhanh\n2. Bấm Tìm kiếm", "1311",
         "- Kết quả gồm các tài khoản có số chứa 1311\n"
         "⚠️ Gợi ý trong ô ghi rõ: \"Tìm theo số hoặc tên tài khoản...\""),

        ("002", "Tìm nhanh theo Tên tài khoản", "P0", PRE,
         "1. Gõ \"phải thu\" vào ô tìm nhanh\n2. Bấm Tìm kiếm", "phải thu",
         "- Kết quả gồm mọi tài khoản có chuỗi \"phải thu\" trong tên"),

        ("003", "Tìm nhanh khớp phần GIỮA của tên", "P0", PRE,
         "1. Gõ một cụm nằm ở GIỮA tên tài khoản (ví dụ \"khách hàng\")\n2. Bấm Tìm kiếm",
         "khách hàng",
         "- Tài khoản \"Phải thu của khách hàng ngắn hạn\" vẫn ra kết quả\n"
         "⚠️ Đây là lỗi cũ của hệ thống trước đây: chỉ tìm được khi gõ đúng phần ĐUÔI của tên. "
         "Bắt buộc phải kiểm trường hợp này"),

        ("004", "Tìm nhanh không phân biệt hoa thường", "P1", PRE,
         "1. Gõ \"PHẢI THU\" bằng chữ hoa\n2. Bấm Tìm kiếm", "PHẢI THU",
         "- Kết quả giống hệt khi gõ chữ thường"),

        ("005", "Gõ ô tìm nhanh mà chưa bấm Tìm kiếm", "P1", PRE,
         "1. Gõ từ khóa\n2. Chờ 5 giây, không bấm gì", "1311",
         "- Bảng vẫn giữ nguyên, chưa lọc"),

        ("006", "Lọc theo Bậc tài khoản", "P0", PRE,
         "1. Mở bộ lọc nâng cao\n2. Chọn Bậc tài khoản = 1\n3. Bấm Tìm kiếm", "Bậc: 1",
         "- Kết quả chỉ còn tài khoản bậc 1\n"
         "- Mọi dòng chỉ điền cột Cấp 1, hai cột Cấp 2 và Cấp 3 đều trống"),

        ("007", "Lọc theo Bậc tài khoản bậc 3", "P1", PRE,
         "1. Chọn Bậc tài khoản = 3\n2. Bấm Tìm kiếm", "Bậc: 3",
         "- Kết quả chỉ còn tài khoản bậc 3, mọi dòng chỉ điền cột Cấp 3"),

        ("008", "Lọc theo Loại tài khoản", "P0", PRE,
         "1. Chọn một giá trị trong ô Loại tài khoản\n2. Bấm Tìm kiếm", "Loại: Tài khoản tài sản",
         "- Kết quả chỉ còn tài khoản thuộc loại đã chọn\n"
         "- Cột Loại tài khoản của mọi dòng đều hiện đúng loại vừa chọn"),

        ("009", "Lọc theo Theo dõi công nợ", "P0", PRE,
         "1. Chọn Theo dõi công nợ = Có\n2. Bấm Tìm kiếm", "Theo dõi công nợ: Có",
         "- Kết quả chỉ còn các tài khoản có dấu đánh dấu ở cột Theo dõi công nợ"),

        ("010", "Lọc theo Theo dõi công nợ = Không", "P1", PRE,
         "1. Chọn Theo dõi công nợ = Không\n2. Bấm Tìm kiếm", "Theo dõi công nợ: Không",
         "- Kết quả chỉ còn các tài khoản để trống cột Theo dõi công nợ"),

        ("011", "Lọc theo Trạng thái", "P0", PRE,
         "1. Chọn Trạng thái = Khóa\n2. Bấm Tìm kiếm\n3. Chọn lại Trạng thái = Hoạt động",
         "Trạng thái: Khóa rồi Hoạt động",
         "- Mỗi lần lọc, mọi dòng đều mang đúng nhãn trạng thái đã chọn"),

        ("012", "Lọc theo Người tạo", "P0", PRE,
         "1. Chọn một người trong ô Người tạo\n2. Bấm Tìm kiếm", "Người tạo: một nhân viên",
         "- Kết quả chỉ còn tài khoản do người đó tạo\n"
         "- Danh sách chọn chỉ liệt kê người thực sự đã tạo bản ghi, không liệt kê toàn bộ nhân viên"),

        ("013", "Lọc theo Người cập nhật", "P0", PRE,
         "1. Chọn một người trong ô Người cập nhật\n2. Bấm Tìm kiếm", "Người cập nhật: một nhân viên",
         "- Kết quả chỉ còn tài khoản do người đó cập nhật gần nhất"),

        ("014", "Kết hợp nhiều điều kiện lọc", "P0", PRE,
         "1. Chọn Bậc = 2, Trạng thái = Hoạt động, Theo dõi công nợ = Có\n2. Bấm Tìm kiếm",
         "Bậc 2 + Hoạt động + Có theo dõi công nợ",
         "- Kết quả phải thỏa ĐỒNG THỜI cả ba điều kiện"),

        ("015", "Nút Làm mới xóa hết điều kiện và nạp lại", "P0", PRE,
         "1. Đặt nhiều điều kiện lọc và bấm Tìm kiếm\n2. Bấm nút Làm mới", "—",
         "- Mọi ô lọc trở về trống\n"
         "- Danh sách tự nạp lại đủ 308 dòng NGAY, không cần bấm Tìm kiếm lần nữa"),

        ("016", "Bộ lọc được nhớ khi quay lại màn trong 10 phút", "P1", PRE,
         "1. Chọn Bậc = 1, bấm Tìm kiếm\n2. Sang màn khác\n3. Quay lại trong 10 phút", "Bậc: 1",
         "- Ô lọc và kết quả vẫn giữ nguyên"),

        ("017", "Lọc xong tự về trang 1", "P1", PRE + " Đang đứng ở trang 5.",
         "1. Chuyển sang trang 5\n2. Đặt điều kiện lọc\n3. Bấm Tìm kiếm", "—",
         "- Kết quả hiển thị từ trang 1, không hiện bảng trống"),
    ]),

    ("III", "DANH SÁCH & PHÂN TRANG", [
        ("001", "Thứ tự mặc định theo cây tài khoản", "P0", PRE,
         "1. Mở màn hình khi chưa lọc, chưa sắp xếp\n2. Đọc thứ tự các dòng", "—",
         "- Tài khoản con nằm ngay dưới tài khoản mẹ của nó (131 rồi 1311 rồi 13111)\n"
         "⚠️ Không được xáo trộn khiến con nằm cách xa mẹ"),

        ("002", "Chuyển trang bằng nút số trang", "P0", PRE + " Cỡ trang 10 nên có nhiều trang.",
         "1. Bấm số trang 2", "—",
         "- Bảng hiện dữ liệu trang 2\n- Cột STT bắt đầu từ 11\n"
         "- Dòng Hiển thị dưới bảng cập nhật đúng"),

        ("003", "Chuyển tới trang cuối", "P1", PRE,
         "1. Bấm nút chuyển tới trang cuối", "—",
         "- Bảng hiện các dòng cuối cùng, không lỗi, không trống"),

        ("004", "Đổi cỡ trang", "P0", PRE,
         "1. Đổi cỡ trang từ 10 sang 100", "Cỡ trang: 100",
         "- Bảng hiện 100 dòng\n- Danh sách chỉ nạp lại đúng một lần"),

        ("005", "Đổi cỡ trang khi đang ở trang cuối", "P1", PRE + " Đang ở trang cuối.",
         "1. Đổi cỡ trang sang 100", "Cỡ trang: 100",
         "- Bảng hiện dữ liệu, KHÔNG hiện bảng trống\n"
         "⚠️ Bẫy phân trang: giữ nguyên số trang cũ sau khi tăng cỡ trang sẽ ra bảng rỗng"),

        ("006", "Giữ nguyên trang khi thao tác trên dòng", "P1", PRE,
         "1. Chuyển sang trang 3\n2. Bấm Xem một dòng rồi Đóng", "—",
         "- Vẫn đang ở trang 3, không bị nhảy về trang 1"),
    ]),

    ("IV", "THÊM / SỬA / XEM TÀI KHOẢN", [
        ("001", "Mở trang Thêm tài khoản", "P0", PRE,
         "1. Bấm nút Tạo mới", "—",
         "- Chuyển sang TRANG RIÊNG để thêm tài khoản, không phải cửa sổ nhỏ\n"
         "- Có các ô: Số tài khoản (bắt buộc), Bậc tài khoản (bắt buộc), Tài khoản mẹ, "
         "Tên tài khoản (bắt buộc), Loại tài khoản (bắt buộc), Trạng thái, và ô đánh dấu "
         "\"Tài khoản theo dõi công nợ\"\n"
         "- Các ô bắt buộc có dấu sao đỏ bên cạnh nhãn\n"
         "- Trang chia làm 2 khối: \"Vị trí trong hệ thống tài khoản\" (Số tài khoản, Bậc tài "
         "khoản, Tài khoản mẹ) và \"Thông tin tài khoản\" (Tên tài khoản, Loại tài khoản, "
         "Trạng thái, ô đánh dấu Tài khoản theo dõi công nợ)\n"
         "- Dưới ô Số tài khoản có dòng nhắc: chỉ nhập số, tối đa 15 chữ số; 3 chữ số là cấp 1, "
         "4 số cấp 2, từ 5 số cấp 3\n"
         "- Góc trên bên phải có 3 nút: Lưu, Lưu & Thêm tiếp, Quay lại"),

        ("002", "Thêm mới tài khoản bậc 1", "P0", PRE,
         "1. Bấm Tạo mới\n2. Nhập Số tài khoản 3 chữ số\n3. Chọn Bậc = 1\n"
         "4. Nhập Tên và chọn Loại tài khoản\n5. Bấm Lưu",
         "Số: 991; Bậc: 1; Tên: Tài khoản kiểm thử; Loại: Tài khoản tài sản",
         "- Ô Tài khoản mẹ KHÔNG bắt buộc (không có dấu sao) khi Bậc = 1\n"
         "- Lưu thành công, quay về danh sách và có dòng 991\n"
         "- Số 991 nằm ở cột Cấp 1"),

        ("003", "Thêm mới tài khoản bậc 2", "P0", PRE,
         "1. Bấm Tạo mới\n2. Chọn Bậc = 2\n3. Chọn Tài khoản mẹ = 991\n"
         "4. Nhập Số tài khoản = 9911\n5. Nhập Tên, chọn Loại\n6. Bấm Lưu",
         "Số: 9911; Bậc: 2; Mẹ: 991",
         "- Ô Tài khoản mẹ chuyển thành bắt buộc (có dấu sao) khi chọn Bậc 2\n"
         "- Lưu thành công, số 9911 nằm ở cột Cấp 2\n"
         "- Dòng 9911 nằm ngay dưới dòng 991 trong danh sách"),

        ("004", "Thêm mới tài khoản bậc 3", "P0", PRE,
         "1. Bấm Tạo mới\n2. Chọn Bậc = 3\n3. Chọn Tài khoản mẹ = 9911\n"
         "4. Nhập Số tài khoản = 99111\n5. Nhập Tên, chọn Loại\n6. Bấm Lưu",
         "Số: 99111; Bậc: 3; Mẹ: 9911",
         "- Lưu thành công, số 99111 nằm ở cột Cấp 3"),

        ("005", "Danh sách Tài khoản mẹ lọc theo bậc đang chọn", "P0", PRE,
         "1. Bấm Tạo mới\n2. Chọn Bậc = 2, mở danh sách Tài khoản mẹ và quan sát\n"
         "3. Đổi Bậc = 3, mở lại danh sách Tài khoản mẹ", "Bậc 2 rồi Bậc 3",
         "- Ở Bậc 2: danh sách chỉ liệt kê tài khoản BẬC 1\n"
         "- Ở Bậc 3: danh sách chỉ liệt kê tài khoản BẬC 2\n"
         "⚠️ Không được liệt kê lẫn lộn mọi bậc"),

        ("006", "Bật ô đánh dấu Tài khoản theo dõi công nợ", "P0", PRE,
         "1. Bấm Tạo mới, nhập đủ thông tin\n2. Bấm vào ô đánh dấu \"Tài khoản theo dõi công nợ\"\n"
         "3. Bấm Lưu", "Số: 992; bật theo dõi công nợ",
         "- Ô đánh dấu bấm được và đổi trạng thái ngay khi bấm\n"
         "- Bên dưới có dòng giải thích khi nào nên bật\n"
         "- Sau khi lưu, dòng 992 có dấu đánh dấu ở cột Theo dõi công nợ\n"
         "⚠️ Bẫy hay gặp: bấm vào ô đánh dấu không ăn, phải bấm đúng vào chữ mới được"),

        ("007", "Mở trang Sửa nạp đúng dữ liệu cũ", "P0", PRE,
         "1. Bấm nút Sửa trên dòng 991", "—",
         "- Chuyển sang trang sửa, mọi ô điền sẵn đúng dữ liệu đang có\n"
         "- Ô đánh dấu Theo dõi công nợ đúng trạng thái đang lưu"),

        ("008", "Sửa Tên tài khoản", "P0", PRE,
         "1. Bấm Sửa dòng 991\n2. Đổi Tên\n3. Bấm Lưu", "Tên: Tài khoản kiểm thử (đã sửa)",
         "- Lưu thành công, quay về danh sách hiện tên mới\n"
         "- Cột Cập nhật đổi sang thời điểm và người vừa sửa"),

        ("009", "Sửa Loại tài khoản", "P1", PRE,
         "1. Bấm Sửa dòng 991\n2. Đổi Loại tài khoản\n3. Bấm Lưu", "Loại: Tài khoản nguồn vốn",
         "- Lưu thành công, cột Loại tài khoản hiện giá trị mới"),

        ("010", "Bật / tắt Theo dõi công nợ khi sửa", "P1", PRE,
         "1. Bấm Sửa dòng đang bật Theo dõi công nợ\n2. Bỏ đánh dấu\n3. Bấm Lưu", "Bỏ đánh dấu",
         "- Lưu thành công, cột Theo dõi công nợ của dòng đó trở về trống"),

        ("011", "Nút Sửa bị vô hiệu với tài khoản đang Khóa", "P0",
         PRE + " Tài khoản 993 đang ở trạng thái Khóa.",
         "1. Rê chuột vào nút Sửa của dòng 993\n2. Thử bấm", "Tài khoản 993 đang Khóa",
         "- Nút Sửa bị mờ, không bấm được\n"
         "- Rê chuột hiện chú thích \"Tài khoản đã khóa → không cho sửa\""),

        ("012", "Xem chi tiết một tài khoản", "P0", PRE,
         "1. Bấm nút Sửa trên một dòng bất kỳ để xem chi tiết\n2. Bấm Quay lại", "—",
         "- Trang sửa hiện đầy đủ thông tin của tài khoản đó\n"
         "- Bấm Quay lại khi chưa đổi gì thì về danh sách ngay, không hỏi lại\n"
         "⚠️ Màn này KHÔNG có nút Xem riêng — xem chi tiết bằng cách mở trang Sửa"),

        ("013", "Cảnh báo khi rời trang lúc đang nhập dở", "P0", PRE,
         "1. Bấm Tạo mới\n2. Nhập vài ô\n3. Bấm quay lại danh sách", "Số: 995; Tên: nhập dở",
         "- Hệ thống cảnh báo dữ liệu chưa lưu và hỏi xác nhận\n"
         "- Chọn ở lại thì trang vẫn giữ nguyên nội dung đang nhập\n"
         "- Chọn thoát thì không tạo bản ghi nào"),

        ("014", "Rời trang khi chưa nhập gì", "P1", PRE,
         "1. Bấm Tạo mới\n2. Không nhập gì\n3. Bấm quay lại danh sách", "—",
         "- Quay về danh sách ngay, KHÔNG hỏi lại"),

        ("015", "Chống bấm Lưu nhiều lần liên tiếp", "P1", PRE,
         "1. Bấm Tạo mới, nhập đủ\n2. Bấm Lưu liên tiếp 3 lần thật nhanh",
         "Số: 996; Tên: Tài khoản thử 6",
         "- Chỉ tạo ra ĐÚNG 1 tài khoản 996\n- Nút Lưu bị vô hiệu trong lúc xử lý"),

        ("016", "Tài khoản mới dùng được ngay khi hạch toán", "P0", PRE,
         "1. Tạo mới tài khoản 991 ở trạng thái Hoạt động\n"
         "2. Mở một màn hạch toán chứng từ, mở danh sách chọn tài khoản", "Số: 991",
         "- Tài khoản 991 có trong danh sách chọn và chọn được"),
    ]),

    ("V", "RÀNG BUỘC CÂY TÀI KHOẢN", [
        ("001", "Bậc 2 bỏ trống Tài khoản mẹ", "P0", PRE,
         "1. Bấm Tạo mới\n2. Chọn Bậc = 2, để trống Tài khoản mẹ\n3. Nhập các ô còn lại\n"
         "4. Bấm Lưu", "Bậc: 2; Tài khoản mẹ: (để trống)",
         "- Ô Tài khoản mẹ báo \"Bắt buộc phải chọn tài khoản mẹ với bậc 2 và 3\", không lưu"),

        ("002", "Bậc 3 bỏ trống Tài khoản mẹ", "P0", PRE,
         "1. Bấm Tạo mới\n2. Chọn Bậc = 3, để trống Tài khoản mẹ\n3. Bấm Lưu",
         "Bậc: 3; Tài khoản mẹ: (để trống)",
         "- Báo lỗi bắt buộc chọn tài khoản mẹ, không lưu"),

        ("003", "Bậc 1 không cần Tài khoản mẹ", "P0", PRE,
         "1. Bấm Tạo mới\n2. Chọn Bậc = 1, để trống Tài khoản mẹ\n3. Nhập các ô còn lại\n"
         "4. Bấm Lưu", "Bậc: 1; Tài khoản mẹ: (để trống)",
         "- Lưu thành công, không báo lỗi ở ô Tài khoản mẹ"),

        ("004", "Chọn Tài khoản mẹ sai bậc", "P0", PRE,
         "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Thêm tài khoản bậc 3 nhưng đưa mẹ là "
         "một tài khoản BẬC 1\n2. Đọc thông báo trả về",
         "Số: 99911; Bậc: 3; Mẹ: 131 (bậc 1)",
         "- Hệ thống chặn, báo tài khoản mẹ phải là tài khoản bậc 2 và nêu rõ mẹ đang là bậc mấy\n"
         "- Không tạo bản ghi\n"
         "⚠️ Giao diện đã lọc sẵn danh sách mẹ, nhưng hệ thống vẫn phải chặn ở tầng dưới"),

        ("005", "Số tài khoản con không bắt đầu bằng số mẹ", "P0", PRE,
         "1. Bấm Tạo mới\n2. Chọn Bậc = 2, Tài khoản mẹ = 991\n"
         "3. Nhập Số tài khoản = 8888 (không bắt đầu bằng 991)\n4. Bấm Lưu",
         "Số: 8888; Mẹ: 991",
         "- Hệ thống chặn, thông báo nêu rõ số tài khoản con phải bắt đầu bằng số tài khoản mẹ "
         "và gợi ý dạng đúng (991 thì con phải là 9911, 9912…)\n"
         "- Không tạo bản ghi\n"
         "⚠️ Đây là quy tắc quan trọng nhất của cây: sai điều này thì dòng đó nằm sai chỗ vĩnh viễn"),

        ("006", "Số tài khoản con bắt đầu đúng bằng số mẹ", "P0", PRE,
         "1. Bấm Tạo mới\n2. Chọn Bậc = 2, Tài khoản mẹ = 991\n3. Nhập Số tài khoản = 9912\n"
         "4. Bấm Lưu", "Số: 9912; Mẹ: 991",
         "- Lưu thành công\n- Dòng 9912 nằm ngay dưới 991 trong danh sách"),

        ("007", "Không đổi được Bậc của tài khoản đang có con", "P0",
         PRE + " Tài khoản 991 (bậc 1) đang có 2 tài khoản con là 9911 và 9912.",
         "1. Bấm Sửa dòng 991\n2. Đổi Bậc từ 1 sang 2\n3. Bấm Lưu", "Bậc: 1 → 2",
         "- Hệ thống chặn, thông báo nêu rõ tài khoản đang có bao nhiêu tài khoản con nên "
         "không được đổi bậc, kèm gợi ý chuyển hoặc xóa các tài khoản con trước\n"
         "- Không lưu"),

        ("008", "Không đổi được Số tài khoản của tài khoản đang có con", "P0",
         PRE + " Tài khoản 991 đang có 2 tài khoản con.",
         "1. Bấm Sửa dòng 991\n2. Đổi Số tài khoản từ 991 sang 997\n3. Bấm Lưu", "Số: 991 → 997",
         "- Hệ thống chặn, thông báo nêu rõ tài khoản đang có tài khoản con nên không được đổi "
         "số tài khoản\n- Không lưu\n"
         "⚠️ Nếu đổi được thì các tài khoản con sẽ mất mẹ và nằm lạc khỏi cây"),

        ("009", "Đổi được Tên và Loại của tài khoản đang có con", "P0",
         PRE + " Tài khoản 991 đang có 2 tài khoản con.",
         "1. Bấm Sửa dòng 991\n2. Đổi Tên và Loại tài khoản, GIỮ NGUYÊN Số và Bậc\n3. Bấm Lưu",
         "Tên và Loại mới",
         "- Lưu thành công\n"
         "⚠️ Chỉ Bậc và Số tài khoản bị khóa, các trường khác vẫn sửa được bình thường"),

        ("010", "Đổi Bậc và Số của tài khoản chưa có con", "P1",
         PRE + " Tài khoản 9912 là bậc 2, chưa có tài khoản con nào.",
         "1. Bấm Sửa dòng 9912\n2. Đổi Số tài khoản thành 9913\n3. Bấm Lưu", "Số: 9912 → 9913",
         "- Lưu thành công vì tài khoản này chưa có con"),

        ("011", "Chọn Tài khoản mẹ không tồn tại", "P1", PRE,
         "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Thêm tài khoản bậc 2 với mẹ là "
         "một số tài khoản không có trong danh mục", "Mẹ: 123456789",
         "- Hệ thống chặn, báo \"Không tìm thấy tài khoản mẹ\", không tạo bản ghi"),
    ]),

    ("VI", "KHÓA & MỞ KHÓA", [
        ("001", "Khóa tài khoản do chính mình tạo", "P0", PRE,
         "1. Bấm nút Khóa ở cột Trạng thái dòng 999\n2. Đọc hộp xác nhận\n3. Bấm Khóa",
         "Tài khoản 999 (do chính người đang đăng nhập tạo)",
         "- Hộp xác nhận tiêu đề \"Xác nhận khóa\", câu hỏi nêu đúng tên tài khoản\n"
         "- Thông báo khóa thành công\n"
         "- Dòng đổi nhãn sang Khóa, nút Sửa của dòng đó chuyển sang mờ"),

        ("002", "Mở khóa tài khoản do chính mình tạo", "P0",
         PRE + " Tài khoản 999 đang ở trạng thái Khóa và do chính người đăng nhập tạo.",
         "1. Bấm nút Mở khóa\n2. Bấm Mở khóa trong hộp xác nhận", "Tài khoản 999",
         "- Hộp xác nhận tiêu đề \"Xác nhận mở khóa\"\n- Thông báo mở khóa thành công\n"
         "- Dòng quay lại nhãn Hoạt động, nút Sửa sáng trở lại"),

        ("003", "Không khóa được tài khoản do người khác tạo", "P0",
         PRE + " Tài khoản 131 do người khác tạo.",
         "1. Rê chuột vào nút Khóa của dòng 131\n2. Thử bấm", "Tài khoản 131 của người khác",
         "- Nút Khóa bị mờ, không bấm được\n- Rê chuột hiện chú thích nêu lý do\n"
         "⚠️ Ràng buộc riêng của màn này: chỉ chính người tạo mới khóa được"),

        ("004", "Hủy hộp xác nhận khóa", "P1", PRE,
         "1. Bấm nút Khóa trên dòng 999\n2. Bấm Hủy", "Tài khoản 999",
         "- Hộp đóng, trạng thái không đổi, không có thông báo thành công"),

        ("005", "Tài khoản đã khóa không còn chọn được khi hạch toán", "P0",
         PRE + " Tài khoản 999 đang ở trạng thái Khóa.",
         "1. Mở một màn hạch toán chứng từ\n2. Mở danh sách chọn tài khoản", "Tài khoản 999",
         "- Tài khoản 999 KHÔNG có trong danh sách chọn"),

        ("006", "Chứng từ cũ vẫn hiện đúng tài khoản đã bị khóa", "P0",
         "Có sẵn 1 chứng từ đã hạch toán vào tài khoản 1311; sau đó 1311 bị chuyển sang Khóa.",
         "1. Khóa tài khoản 1311\n2. Mở lại chứng từ cũ ở chế độ Sửa", "Tài khoản 1311 đang Khóa",
         "- Ô tài khoản của chứng từ vẫn hiện đúng 1311 kèm tên, không trống, "
         "không tự nhảy sang tài khoản khác\n"
         "- Lưu lại chứng từ không làm mất giá trị tài khoản\n"
         "⚠️ Quy tắc chung toàn hệ thống: danh mục bị khóa vẫn phải hiện ở bản ghi đang dùng nó"),

        ("007", "Khóa tài khoản mẹ không tự khóa tài khoản con", "P1",
         PRE + " Tài khoản 991 có 2 tài khoản con.",
         "1. Khóa tài khoản 991\n2. Kiểm tra trạng thái của 9911 và 9912", "Tài khoản 991",
         "- Chỉ 991 đổi sang Khóa\n- Hai tài khoản con vẫn ở trạng thái Hoạt động\n"
         "- Đây là hành vi hiện tại; nếu nghiệp vụ muốn khóa theo cây thì phải nêu thành yêu cầu riêng"),

        ("008", "Người chỉ có quyền Xem không thấy nút Khóa", "P0",
         "Đăng nhập bằng tài khoản chỉ có quyền \"Xem danh mục tài khoản\".",
         "1. Mở màn hình\n2. Nhìn cột Trạng thái", "—",
         "- Cột Trạng thái chỉ có nhãn, không có nút Khóa / Mở khóa"),
    ]),

    ("VII", "XÓA", [
        ("001", "Xóa tài khoản do chính mình tạo, chưa có con, chưa dùng", "P0", PRE,
         "1. Bấm nút Xóa trên dòng 999\n2. Đọc hộp xác nhận\n3. Bấm Xóa", "Tài khoản 999",
         "- Hộp xác nhận tiêu đề \"Xác nhận xóa\", câu hỏi nêu đúng tên tài khoản\n"
         "- Thông báo xóa thành công\n- Dòng biến mất, tổng dưới bảng giảm 1"),

        ("002", "Hủy hộp xác nhận xóa", "P0", PRE,
         "1. Bấm nút Xóa trên dòng 999\n2. Bấm Hủy", "Tài khoản 999",
         "- Hộp đóng, dòng vẫn còn nguyên"),

        ("003", "Không xóa được tài khoản do người khác tạo", "P0",
         PRE + " Tài khoản 131 do người khác tạo.",
         "1. Rê chuột vào nút Xóa của dòng 131\n2. Thử bấm", "Tài khoản 131 của người khác",
         "- Nút Xóa bị mờ, không bấm được, rê chuột hiện chú thích nêu lý do"),

        ("004", "Không xóa được tài khoản đang có tài khoản con", "P0",
         PRE + " Tài khoản 991 do chính mình tạo và đang có 2 tài khoản con.",
         "1. Rê chuột vào nút Xóa của dòng 991\n2. Thử bấm", "Tài khoản 991",
         "- Nút Xóa bị mờ, chú thích nêu rõ tài khoản đang có tài khoản con\n"
         "⚠️ Muốn xóa phải xóa hết tài khoản con trước"),

        ("005", "Không xóa được tài khoản đã dùng ở chứng từ", "P0",
         PRE + " Tài khoản 998 do chính mình tạo, chưa có con nhưng đã được hạch toán ở 1 chứng từ.",
         "1. Rê chuột vào nút Xóa của dòng 998\n2. Thử bấm", "Tài khoản 998",
         "- Nút Xóa bị mờ, chú thích nêu rõ tài khoản đang được sử dụng"),

        ("006", "Chặn xóa khi bỏ qua giao diện", "P0",
         PRE + " Tài khoản 991 đang có tài khoản con.",
         "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa tài khoản 991\n2. Mở lại màn hình",
         "Tài khoản 991",
         "- Hệ thống chặn, nêu lý do\n- Tài khoản 991 và các con vẫn còn nguyên\n"
         "⚠️ Không được dựa vào việc nút bị mờ ở giao diện để bảo vệ dữ liệu"),

        ("007", "Xóa tài khoản vừa bị người khác hạch toán", "P1",
         "Hai người cùng thao tác. Tài khoản 999 ban đầu chưa dùng ở đâu.",
         "1. Người 1 mở màn hình (nút Xóa của 999 đang sáng)\n"
         "2. Người 2 lập chứng từ hạch toán vào 999\n3. Người 1 bấm Xóa và xác nhận",
         "Tài khoản 999",
         "- Hệ thống chặn lại, báo tài khoản đang được sử dụng\n- Dòng vẫn còn"),

        ("008", "Xóa tài khoản con rồi xóa tài khoản mẹ", "P1",
         PRE + " Tài khoản 991 do chính mình tạo, có 2 con 9911 và 9912 cũng do chính mình tạo, "
         "cả 3 đều chưa dùng ở chứng từ nào.",
         "1. Xóa 9911\n2. Xóa 9912\n3. Rê chuột vào nút Xóa của 991\n4. Xóa 991", "—",
         "- Sau khi xóa hết con, nút Xóa của 991 chuyển từ mờ sang bấm được\n"
         "- Xóa 991 thành công"),

        ("009", "Xóa dòng cuối cùng của trang", "P1",
         PRE + " Đang ở trang cuối, trang đó chỉ còn 1 dòng và dòng đó xóa được.",
         "1. Xóa dòng duy nhất của trang cuối", "—",
         "- Xóa thành công\n- Màn tự lùi về trang trước và hiện dữ liệu, KHÔNG hiện bảng trống"),

        ("010", "Người chỉ có quyền Xem không thấy nút Xóa", "P0",
         "Đăng nhập bằng tài khoản chỉ có quyền \"Xem danh mục tài khoản\".",
         "1. Mở màn hình, nhìn cột Hành động", "—",
         "- Chỉ còn nút Lịch sử chỉnh sửa, không có nút Sửa và nút Xóa"),
    ]),

    ("VIII", "IN, XUẤT EXCEL & NHẬP EXCEL", [
        ("001", "In danh sách toàn bộ", "P0", PRE,
         "1. Không lọc gì\n2. Bấm nút In danh sách", "—",
         "- Mở bản in danh mục tài khoản\n"
         "- Bản in có tiêu đề, đủ các cột chính và đủ số dòng như trên màn hình"),

        ("002", "In danh sách theo bộ lọc đang áp dụng", "P0", PRE,
         "1. Lọc Bậc tài khoản = 1\n2. Bấm In danh sách", "Bậc: 1",
         "- Bản in chỉ chứa các tài khoản bậc 1 đang lọc\n"
         "⚠️ Bẫy hay gặp: bản in ra toàn bộ danh mục, bỏ qua bộ lọc"),

        ("003", "Bản in hiển thị đúng cấu trúc bậc", "P1", PRE,
         "1. Bấm In danh sách\n2. Đối chiếu các cột Cấp trên bản in", "—",
         "- Số tài khoản nằm đúng cột theo bậc, giống trên màn hình\n"
         "- Bản in đọc được, không vỡ khung, không mất chữ"),

        ("004", "Bản in không mất định dạng khi in ra giấy", "P1", PRE,
         "1. Bấm In danh sách\n2. Mở hộp thoại in của trình duyệt và xem trước", "—",
         "- Nội dung nằm gọn trong khổ giấy, không tràn lề, chữ không bị cắt\n"
         "⚠️ Bẫy hay gặp ở màn in: xem trên màn hình thì đẹp, in ra thì mất định dạng"),

        ("005", "Xuất Excel toàn bộ danh mục", "P0", PRE,
         "1. Không lọc gì\n2. Bấm Xuất Excel\n3. Mở file tải về", "—",
         "- Thông báo \"Xuất Excel thành công\"\n- File mở được và có đủ 308 dòng"),

        ("006", "File Excel có đủ cột như trên màn hình", "P0", PRE,
         "1. Xuất Excel\n2. Đối chiếu tiêu đề cột với bảng trên màn hình", "—",
         "- File có các cột Số tài khoản (hoặc 3 cột Cấp), Tên tài khoản, Loại tài khoản, "
         "Theo dõi công nợ, Trạng thái\n- Tiêu đề cột bằng tiếng Việt giống trên màn hình"),

        ("007", "Xuất Excel theo đúng bộ lọc đang áp dụng", "P0", PRE,
         "1. Lọc Bậc tài khoản = 3\n2. Xuất Excel\n3. Mở file", "Bậc: 3",
         "- File chỉ chứa các tài khoản bậc 3"),

        ("008", "Xuất Excel lấy đủ dữ liệu, không chỉ trang hiện tại", "P0", PRE,
         "1. Đứng ở trang 1 với cỡ trang 10\n2. Xuất Excel\n3. Đếm số dòng trong file", "—",
         "- File có đủ 308 dòng, không phải 10 dòng của trang đang xem"),

        ("009", "Tải file mẫu để nhập Excel", "P0", PRE,
         "1. Bấm nút Import Excel\n2. Bấm tải file mẫu\n3. Mở file mẫu", "—",
         "- Tải được file mẫu, có đủ các cột cần thiết\n"
         "- Cột bắt buộc được đánh dấu sao đỏ"),

        ("010", "Import Excel với dữ liệu hợp lệ", "P0", PRE,
         "1. Bấm Import Excel\n2. Chọn file 3 dòng có số tài khoản mới và đúng cây\n"
         "3. Kiểm tra bảng xem trước\n4. Bấm xác nhận nhập",
         "3 dòng: 981 (bậc 1), 9811 (bậc 2, mẹ 981), 98111 (bậc 3, mẹ 9811)",
         "- Bảng xem trước hiện đủ 3 dòng và đều hợp lệ\n"
         "- Sau khi xác nhận: 3 tài khoản mới nằm đúng cột Cấp tương ứng, con nằm dưới mẹ"),

        ("011", "Import Excel có dòng sai quy tắc cây", "P0", PRE,
         "1. Chọn file có 1 dòng bậc 2 nhưng số không bắt đầu bằng số mẹ\n2. Đọc bảng xem trước",
         "Dòng 2: số 8888, mẹ 981",
         "- Dòng đó bị đánh dấu lỗi, nêu rõ lý do\n- Chỉ dòng hợp lệ mới được ghi vào"),

        ("012", "Import Excel có số tài khoản trùng dữ liệu đã có", "P0", PRE,
         "1. Chọn file có 1 dòng mang số tài khoản đã tồn tại\n2. Đọc bảng xem trước",
         "Dòng 1: số 131 (đã có)",
         "- Dòng đó bị đánh dấu lỗi trùng số tài khoản\n- Không tạo bản ghi trùng"),

        ("013", "Import Excel với file sai định dạng", "P1", PRE,
         "1. Bấm Import Excel\n2. Chọn một file không phải Excel", "File .txt",
         "- Hệ thống báo file không hợp lệ, không lỗi trắng trang"),

        ("014", "Dòng hợp lệ bị khóa sau khi kiểm tra", "P1", PRE,
         "1. Chọn file có cả dòng hợp lệ và dòng lỗi\n2. Quan sát bảng xem trước sau khi kiểm tra",
         "File 5 dòng: 3 hợp lệ, 2 lỗi",
         "- Dòng hợp lệ chuyển sang trạng thái khóa, không sửa được nữa\n"
         "- Dòng lỗi vẫn cho sửa tại chỗ để nhập lại"),

        ("015", "Người chỉ có quyền Xem không thấy nút Import Excel", "P0",
         "Đăng nhập bằng tài khoản chỉ có quyền \"Xem danh mục tài khoản\".",
         "1. Mở màn hình, nhìn cụm nút dưới bảng", "—",
         "- Có nút In danh sách và Xuất Excel nhưng KHÔNG có Import Excel và Tạo mới"),
    ]),

    ("IX", "RÀNG BUỘC NHẬP LIỆU", [
        ("001", "Bỏ trống các ô bắt buộc", "P0", PRE,
         "1. Bấm Tạo mới\n2. Không nhập gì\n3. Bấm Lưu", "(để trống hết)",
         "- Ô Số tài khoản và Tên tài khoản báo \"Bắt buộc phải nhập\"\n"
         "- Ô Bậc tài khoản và Loại tài khoản báo \"Bắt buộc phải chọn\"\n"
         "- Không tạo bản ghi nào"),

        ("002", "Nhập Số tài khoản có chữ cái", "P0", PRE,
         "1. Bấm Tạo mới\n2. Nhập Số tài khoản = \"13A1\"\n3. Bấm Lưu", "Số: 13A1",
         "- Báo số tài khoản chỉ được nhập chữ số, từ 3 đến 15 chữ số\n- Không lưu"),

        ("003", "Nhập Số tài khoản có dấu chấm", "P0", PRE,
         "1. Bấm Tạo mới\n2. Nhập Số tài khoản = \"131.1\"\n3. Bấm Lưu", "Số: 131.1",
         "- Báo lỗi chỉ được nhập chữ số, không lưu"),

        ("004", "Nhập Số tài khoản chỉ 2 chữ số", "P0", PRE,
         "1. Bấm Tạo mới\n2. Nhập Số tài khoản = \"13\"\n3. Bấm Lưu", "Số: 13",
         "- Báo số tài khoản phải từ 3 đến 15 chữ số, không lưu"),

        ("005", "Nhập Số tài khoản đúng 3 chữ số", "P0", PRE,
         "1. Bấm Tạo mới\n2. Nhập Số tài khoản = \"981\", Bậc = 1, nhập Tên và Loại\n3. Bấm Lưu",
         "Số: 981",
         "- Lưu thành công (3 chữ số là độ dài tối thiểu hợp lệ)"),

        ("006", "Nhập Số tài khoản dài hơn 15 chữ số", "P0", PRE,
         "1. Bấm Tạo mới\n2. Nhập Số tài khoản gồm 20 chữ số\n3. Bấm Lưu", "Số: 20 chữ số",
         "- Báo số tài khoản chỉ được từ 3 đến 15 chữ số, không lưu\n"
         "⚠️ Bẫy nghiêm trọng: nếu lọt qua thì hệ thống lưu ra một con số KHÁC hẳn số đã nhập "
         "mà vẫn báo thành công. Bắt buộc phải kiểm và đối chiếu lại số trong danh sách"),

        ("007", "Nhập Số tài khoản đúng 15 chữ số", "P1", PRE,
         "1. Bấm Tạo mới\n2. Nhập Số tài khoản gồm đúng 15 chữ số\n3. Bấm Lưu",
         "Số: 999999999999999",
         "- Lưu thành công\n- Danh sách hiện ĐÚNG con số vừa nhập, không sai một chữ số nào"),

        ("008", "Nhập trùng Số tài khoản", "P0", PRE,
         "1. Bấm Tạo mới\n2. Nhập Số tài khoản đã tồn tại\n3. Bấm Lưu", "Số: 131",
         "- Báo \"Số tài khoản đã tồn tại\", không lưu"),

        ("009", "Sửa mà giữ nguyên Số tài khoản của chính nó", "P0", PRE,
         "1. Bấm Sửa một dòng chưa có con\n2. Giữ nguyên Số, chỉ đổi Tên\n3. Bấm Lưu",
         "Số không đổi; Tên mới",
         "- Lưu thành công\n"
         "⚠️ Bẫy hay gặp: hệ thống coi số của chính bản ghi đang sửa là trùng và chặn nhầm"),

        ("010", "Nhập Tên tài khoản dài hơn 255 ký tự", "P2", PRE,
         "1. Bấm Tạo mới\n2. Dán chuỗi 300 ký tự vào ô Tên tài khoản\n3. Bấm Lưu",
         "Tên: chuỗi 300 ký tự",
         "- Báo \"Tối đa 255 ký tự\", không lưu"),

        ("011", "Nhập tên có dấu tiếng Việt", "P1", PRE,
         "1. Bấm Tạo mới\n2. Nhập Tên có dấu đầy đủ\n3. Bấm Lưu",
         "Tên: Phải thu của khách hàng ngắn hạn",
         "- Lưu thành công, danh sách hiện đúng dấu tiếng Việt"),

        ("012", "Bậc tài khoản chỉ nhận 1, 2 hoặc 3", "P1", PRE,
         "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Thêm tài khoản với Bậc = 4", "Bậc: 4",
         "- Hệ thống chặn, báo bậc tài khoản chỉ nhận 1, 2 hoặc 3, không tạo bản ghi"),

        ("013", "Lỗi biến mất sau khi nhập lại đúng", "P1", PRE,
         "1. Bấm Tạo mới, bấm Lưu ngay để các ô báo đỏ\n2. Nhập đủ mọi ô bắt buộc\n3. Bấm Lưu",
         "Số: 982; Tên: Hết lỗi; Bậc 1; Loại: Tài khoản tài sản",
         "- Viền đỏ và chữ đỏ biến mất khi nhập đủ\n- Lưu thành công"),

        ("014", "Khoảng trắng đầu cuối trong Số tài khoản", "P2", PRE,
         "1. Bấm Tạo mới\n2. Nhập Số tài khoản = \"  983  \"\n3. Bấm Lưu và xem danh sách",
         "Số: \"  983  \"",
         "- Danh sách hiện số 983 không có khoảng trắng thừa\n"
         "- Không tạo được 2 tài khoản mà mắt thường nhìn thấy số giống hệt nhau"),
    ]),

    ("X", "LỊCH SỬ, ĐỒNG THỜI & LUỒNG XUYÊN SUỐT", [
        ("001", "Mở cửa sổ lịch sử chỉnh sửa", "P0", PRE,
         "1. Bấm nút Lịch sử chỉnh sửa trên một dòng đã từng bị sửa", "—",
         "- Mở cửa sổ tiêu đề \"Lịch sử chỉnh sửa tài khoản\"\n"
         "- Có danh sách các lần thay đổi kèm thời điểm và người thực hiện"),

        ("002", "Lịch sử ghi nhận lần sửa vừa thực hiện", "P0", PRE,
         "1. Sửa Tên của một tài khoản và Lưu\n2. Bấm nút Lịch sử chỉnh sửa của dòng đó",
         "Tên cũ → Tên mới",
         "- Lịch sử có bản ghi mới nhất, nêu rõ trường Tên tài khoản đổi từ giá trị cũ sang mới\n"
         "- Ghi đúng người thực hiện và thời điểm"),

        ("003", "Lịch sử sắp xếp mới nhất lên đầu", "P0",
         PRE + " Một tài khoản đã bị sửa ít nhất 3 lần.",
         "1. Mở cửa sổ lịch sử của tài khoản đó\n2. Đọc thứ tự các dòng", "—",
         "- Lần sửa gần nhất nằm ở TRÊN CÙNG\n"
         "⚠️ Bẫy hay gặp: lịch sử xếp ngược, lần đầu tiên lại nằm trên cùng"),

        ("004", "Lịch sử ghi nhận thay đổi trạng thái và loại tài khoản", "P1", PRE,
         "1. Khóa một tài khoản\n2. Mở khóa lại\n3. Đổi Loại tài khoản\n4. Mở cửa sổ lịch sử", "—",
         "- Có đủ 3 bản ghi thay đổi\n"
         "- Giá trị hiển thị bằng nhãn tiếng Việt (Hoạt động / Khóa, tên loại tài khoản), "
         "không phải con số"),

        ("005", "Hai người cùng sửa một tài khoản", "P1",
         "Hai tài khoản đều có quyền Quản lý, cùng mở trang Sửa của tài khoản 999.",
         "1. Người 1 đổi Tên và Lưu\n2. Người 2 (đang mở trang với dữ liệu cũ) đổi Loại và Lưu\n"
         "3. Nạp lại danh sách", "Người 1 đổi Tên; Người 2 đổi Loại",
         "- Cả hai đều lưu được\n"
         "- Kết quả cuối là bản của người lưu sau; hệ thống không lỗi, không nhân đôi bản ghi\n"
         "- Lịch sử ghi nhận cả hai lần sửa"),

        ("006", "Sửa một tài khoản vừa bị người khác xóa", "P1",
         "Hai người đều có quyền Quản lý và cùng là người tạo. Tài khoản 999 chưa dùng ở đâu.",
         "1. Người 1 mở trang Sửa của 999\n2. Người 2 xóa 999\n3. Người 1 bấm Lưu", "Tài khoản 999",
         "- Hệ thống báo dữ liệu đã thay đổi hoặc không còn tồn tại\n"
         "- Màn hình KHÔNG treo, không trắng trang"),

        ("007", "Hai người cùng tạo tài khoản cùng số", "P1",
         "Hai người đều có quyền Quản lý.",
         "1. Cả hai cùng mở trang Tạo mới và nhập Số tài khoản = 985\n"
         "2. Người 1 bấm Lưu\n3. Người 2 bấm Lưu", "Số: 985 (cả hai)",
         "- Người thứ nhất lưu thành công\n"
         "- Người thứ hai bị chặn với thông báo \"Số tài khoản đã tồn tại\"\n"
         "- Danh mục chỉ có ĐÚNG 1 tài khoản số 985"),

        ("008", "Danh mục dùng chung cho mọi công ty", "P1",
         "Hai người thuộc hai công ty khác nhau, đều có quyền Xem danh mục tài khoản.",
         "1. Cả hai cùng mở màn hình\n2. So sánh tổng số dòng và nội dung", "—",
         "- Hai người thấy DANH SÁCH GIỐNG HỆT NHAU\n"
         "⚠️ Danh mục này cố ý không phân theo công ty — thấy khác nhau mới là lỗi"),

        ("009", "Vòng đời đầy đủ của một nhánh tài khoản", "P0", PRE,
         "1. Tạo tài khoản 981 (bậc 1)\n2. Tạo tài khoản con 9811 (bậc 2, mẹ 981)\n"
         "3. Thử đổi số của 981 → bị chặn\n4. Sửa Tên của 981 → được\n"
         "5. Xem lịch sử chỉnh sửa của 981\n6. Xóa 9811\n7. Xóa 981",
         "Cây 981 → 9811",
         "- Bước 3 bị chặn đúng như mong đợi, nêu rõ lý do có tài khoản con\n"
         "- Bước 4 lưu thành công\n- Bước 5 lịch sử ghi nhận lần sửa ở bước 4\n"
         "- Sau bước 7, cả hai tài khoản đều không còn trong danh sách"),

        ("010", "Kiểm tra nhất quán giữa hai cổng", "P1", PRE,
         "1. Tạo tài khoản 981 ở cổng mới\n2. Mở danh mục tài khoản ở cổng cũ, tìm 981\n"
         "3. Sửa Tên của 981 ở cổng cũ\n4. Quay lại cổng mới, nạp lại danh sách", "Số: 981",
         "- Bước 2: cổng cũ thấy 981 với đúng bậc và loại\n"
         "- Bước 4: cổng mới hiện tên vừa sửa\n"
         "⚠️ Hai cổng dùng chung một danh mục, mọi sai lệch đều là lỗi"),
    ]),
]

build(output_file=OUTPUT_FILE, sheet_name=SHEET_NAME, feature_name=FEATURE_NAME,
      module_name=MODULE_NAME, description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS, sections=SECTIONS)
