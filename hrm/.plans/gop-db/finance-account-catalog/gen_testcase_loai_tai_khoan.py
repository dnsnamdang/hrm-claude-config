# -*- coding: utf-8 -*-
"""Sinh testcase cho man Danh muc loai tai khoan (phan he Tai chinh).

Chay:  python gen_testcase_loai_tai_khoan.py
"""
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "..", ".claude", "skills", "testcase-documenter", "assets"))

from tc_engine import build  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(HERE, "testcase - Danh muc loai tai khoan.xlsx")
SHEET_NAME = "Trang tính1"
FEATURE_NAME = "Danh mục loại tài khoản - Cập nhật ngày 13/08/2026"
MODULE_NAME = "Danh mục loại tài khoản"

# ============================================================================
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Quản lý danh sách các loại tài khoản kế toán (tài khoản tài sản, tài khoản nguồn vốn, "
     "tài khoản doanh thu…). Mỗi tài khoản trong Danh mục tài khoản đều được gán về một loại "
     "lấy từ danh mục này.\n"
     "Màn hình nằm ở phân hệ Tài chính → nhóm menu Danh mục → Danh mục loại tài khoản.\n"
     "Đây là màn được chuyển từ hệ thống cũ sang, hai cổng dùng CHUNG một danh mục."),

    ("2. Đối tượng được tính / hiển thị",
     "- Toàn bộ loại tài khoản trong danh mục, KHÔNG phân theo công ty / phòng ban.\n"
     "- Hiển thị cả loại tài khoản Hoạt động và loại tài khoản đang Khóa.\n"
     "- Mỗi dòng gồm 7 cột: STT, Mã loại tài khoản, Tên loại tài khoản, Ghi chú, Cập nhật, "
     "Trạng thái, Hành động.\n"
     "- Cột Cập nhật hiện thời điểm sửa gần nhất kèm tên người cập nhật."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Không có loại tài khoản nào bị ẩn khỏi màn này.\n"
     "- Loại tài khoản đang Khóa VẪN hiện ở đây nhưng KHÔNG còn được chọn khi tạo tài khoản mới.\n"
     "- Khi lọc theo một điều kiện (trạng thái, người tạo, người cập nhật, khoảng ngày cập nhật) "
     "thì các dòng không thỏa bị loại khỏi kết quả."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Hai ô \"Cập nhật từ\" và \"Cập nhật đến\" lọc theo NGÀY CẬP NHẬT gần nhất của loại tài khoản "
     "(chính là giá trị hiển thị ở cột Cập nhật), KHÔNG phải ngày tạo.\n"
     "Khoảng lọc tính bao gồm cả ngày đầu và ngày cuối.\n"
     "Được phép chỉ nhập một trong hai ô."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Danh sách phẳng, không phân cấp cha - con.\n"
     "Quan hệ với màn khác: một loại tài khoản có thể được nhiều tài khoản sử dụng. "
     "Đây là căn cứ để hệ thống chặn xóa và chặn khóa."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "Không cộng dồn. Mỗi loại tài khoản là một dòng độc lập.\n"
     "Chống trùng: cả Mã loại tài khoản và Tên loại tài khoản đều phải là duy nhất trong danh mục. "
     "Trùng mã báo \"Mã loại tài khoản đã tồn tại\"; trùng tên báo \"Tên loại tài khoản đã tồn tại\"."),

    ("7. Phân quyền cấp",
     "Hai quyền dành riêng cho màn này:\n"
     "- \"Xem danh mục loại tài khoản\": vào màn hình, xem danh sách, mở xem chi tiết, xem lịch sử "
     "chỉnh sửa, xuất Excel.\n"
     "- \"Quản lý danh mục loại tài khoản\": thêm mới, sửa, khóa, mở khóa, xóa, nhập từ Excel. "
     "Người có quyền này cũng vào và xem được màn hình.\n"
     "Không có quyền nào trong hai quyền trên thì không vào được màn hình.\n"
     "Danh mục KHÔNG phân quyền theo công ty / phòng ban / bộ phận."),

    ("8. Cách tính các ô thống kê",
     "- Dòng \"Hiển thị a - b / N\" dưới bảng: a là dòng đầu của trang đang xem, b là dòng cuối, "
     "N là tổng số loại tài khoản khớp bộ lọc hiện tại.\n"
     "- Cột STT đánh theo trang: trang 2 với cỡ trang 10 thì bắt đầu từ 11.\n"
     "- Bảng nhập từ Excel: số dòng hợp lệ và số dòng lỗi được đếm riêng; chỉ dòng hợp lệ mới được ghi vào."),

    ("9. Ghi chú đọc bảng",
     "- Nút Khóa / Mở khóa nằm NGAY TRONG cột Trạng thái, không nằm ở cột Hành động.\n"
     "- Loại tài khoản đang được tài khoản nào đó sử dụng thì KHÔNG xóa được VÀ cũng KHÔNG khóa "
     "được — khác với Danh mục tiền tệ (ở đó khóa vẫn được). Rê chuột vào nút để đọc lý do.\n"
     "- Loại tài khoản đang ở trạng thái Khóa thì nút Sửa bị vô hiệu; muốn sửa phải Mở khóa trước.\n"
     "- Cột Ghi chú có thể rất dài, được xuống dòng trong ô, không cắt cụt.\n"
     "- Bộ lọc được hệ thống ghi nhớ trong 10 phút. Kiểm thử bộ lọc nên bấm Làm mới trước mỗi kịch bản.\n"
     "- Nút Import Excel chỉ hiện với người có quyền Quản lý; nút Xuất Excel hiện với mọi người vào "
     "được màn.\n"
     "- Mọi thay đổi đều được ghi lại và xem được qua nút Lịch sử chỉnh sửa trên từng dòng."),
]

# ============================================================================
PRE_PERM = ("Có sẵn 2 tài khoản: tài khoản A chỉ được cấp quyền \"Xem danh mục loại tài khoản\"; "
            "tài khoản B được cấp quyền \"Quản lý danh mục loại tài khoản\". "
            "Danh mục đang có 7 loại tài khoản, trong đó loại \"Tài khoản tài sản\" đang được "
            "nhiều tài khoản sử dụng, loại \"LTK thử\" mới tạo chưa có tài khoản nào dùng.")

ROLE_TCS = [
    ("01", "Vào màn hình khi chỉ có quyền Xem", "P0", PRE_PERM,
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Vào phân hệ Tài chính → Danh mục → Danh mục loại tài khoản",
     "Tài khoản A (chỉ có quyền Xem)",
     "- Vào được màn hình, bảng hiển thị đủ 7 loại tài khoản\n"
     "- KHÔNG có nút Tạo mới, KHÔNG có nút Import Excel\n"
     "- Trên mỗi dòng chỉ có nút Xem và nút Lịch sử chỉnh sửa; KHÔNG có nút Sửa, nút Xóa\n"
     "- Cột Trạng thái không có nút Khóa / Mở khóa\n"
     "- Vẫn có nút Xuất Excel"),

    ("02", "Vào màn hình khi có quyền Quản lý", "P0", PRE_PERM,
     "1. Đăng nhập bằng tài khoản B\n2. Vào Danh mục loại tài khoản", "Tài khoản B",
     "- Có đủ 3 nút dưới bảng: Tạo mới, Xuất Excel, Import Excel\n"
     "- Mỗi dòng có đủ 4 nút: Xem, Sửa, Lịch sử chỉnh sửa, Xóa\n"
     "- Cột Trạng thái có nút Khóa hoặc Mở khóa"),

    ("03", "Chặn vào màn hình khi không có quyền nào", "P0",
     "Tài khoản C không có cả hai quyền của màn này.",
     "1. Đăng nhập bằng tài khoản C\n2. Tìm mục Danh mục loại tài khoản trong phân hệ Tài chính\n"
     "3. Dán thẳng đường dẫn màn hình vào thanh địa chỉ", "Tài khoản C",
     "- Mục menu KHÔNG hiện\n"
     "- Dán thẳng đường dẫn thì hệ thống chuyển sang trang báo không tìm thấy, "
     "không lộ dữ liệu nào"),

    ("04", "Chặn Thêm mới khi bỏ qua giao diện", "P0", PRE_PERM,
     "1. Đăng nhập bằng tài khoản A, lấy mã đăng nhập\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Thêm loại tài khoản, bỏ qua giao diện\n"
     "3. Mở lại màn hình kiểm tra", "Mã: ZZZ; Tên: Loại thử",
     "- Hệ thống từ chối, báo không có quyền\n"
     "- Danh sách vẫn 7 dòng, không có ZZZ"),

    ("05", "Chặn Sửa khi bỏ qua giao diện", "P0", PRE_PERM,
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Sửa loại \"Tài khoản tài sản\"\n"
     "3. Mở lại màn hình", "Đổi tên thành \"Bị sửa trộm\"",
     "- Hệ thống từ chối, báo không có quyền\n- Tên cũ giữ nguyên"),

    ("06", "Chặn Xóa khi bỏ qua giao diện", "P0", PRE_PERM,
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa loại \"LTK thử\"\n"
     "3. Mở lại màn hình", "Loại LTK thử (về nghiệp vụ là xóa được)",
     "- Hệ thống từ chối, báo không có quyền\n- LTK thử vẫn còn trong danh sách"),

    ("07", "Chặn Khóa / Mở khóa khi bỏ qua giao diện", "P1", PRE_PERM,
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Khóa loại \"LTK thử\"\n"
     "3. Mở lại màn hình", "Loại LTK thử đang Hoạt động",
     "- Hệ thống từ chối, báo không có quyền\n- LTK thử vẫn Hoạt động"),

    ("08", "Chặn Import Excel khi bỏ qua giao diện", "P1", PRE_PERM,
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Nhập loại tài khoản từ Excel\n"
     "3. Mở lại màn hình", "File Excel 3 dòng hợp lệ",
     "- Hệ thống từ chối, báo không có quyền\n- Danh sách vẫn 7 dòng"),

    ("09", "Người có quyền Xem vẫn xem được lịch sử chỉnh sửa", "P1", PRE_PERM,
     "1. Đăng nhập bằng tài khoản A\n2. Bấm nút Lịch sử chỉnh sửa trên một dòng", "—",
     "- Cửa sổ \"Lịch sử chỉnh sửa loại tài khoản\" mở bình thường và hiện dữ liệu"),
]

# ============================================================================
PRE = ("Đăng nhập bằng tài khoản có quyền \"Quản lý danh mục loại tài khoản\". "
       "Danh mục có 7 loại tài khoản: 6 loại Hoạt động và 1 loại đang Khóa. "
       "Loại \"Tài khoản tài sản\" đang được nhiều tài khoản sử dụng; "
       "loại \"LTK thử\" chưa có tài khoản nào dùng; có ít nhất 1 loại đã nhập Ghi chú dài "
       "trên 100 ký tự.")

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", [
        ("001", "Mở màn hình lần đầu", "P0", PRE,
         "1. Vào phân hệ Tài chính → Danh mục → Danh mục loại tài khoản\n2. Quan sát toàn màn hình",
         "—",
         "- Tiêu đề trang và tiêu đề bảng đều là \"Danh mục loại tài khoản\"\n"
         "- Khối lọc có tiêu đề \"Bộ lọc danh mục loại tài khoản\", mặc định thu gọn\n"
         "- Bảng có đủ 7 cột đúng thứ tự: STT, Mã loại tài khoản, Tên loại tài khoản, Ghi chú, "
         "Cập nhật, Trạng thái, Hành động\n"
         "- Dưới bảng có 3 nút: Tạo mới, Xuất Excel, Import Excel"),

        ("002", "Hiển thị đủ số bản ghi khi chưa lọc", "P0", PRE,
         "1. Mở màn hình\n2. Đọc dòng Hiển thị dưới bảng", "—",
         "- Tổng là 7, gồm cả loại đang Khóa"),

        ("003", "Cột Ghi chú xuống dòng khi nội dung dài", "P1", PRE,
         "1. Mở màn hình\n2. Nhìn dòng có Ghi chú dài trên 100 ký tự", "—",
         "- Nội dung ghi chú được xuống dòng trong ô, hiện đầy đủ\n"
         "- Không bị cắt cụt bằng dấu ba chấm, không tràn ra ngoài bảng"),

        ("004", "Cột Cập nhật hiện thời điểm và người cập nhật", "P1", PRE,
         "1. Mở màn hình\n2. Nhìn cột Cập nhật", "—",
         "- Hiện ngày giờ cập nhật gần nhất kèm tên người cập nhật\n"
         "- Dòng chưa từng sửa vẫn hiện thông tin của lần tạo, không để trắng trơn"),

        ("005", "Cột Trạng thái hiển thị đúng nhãn", "P0", PRE,
         "1. Mở màn hình\n2. Đối chiếu cột Trạng thái", "—",
         "- Loại đang dùng hiện nhãn \"Hoạt động\"\n- Loại bị khóa hiện nhãn \"Khóa\""),

        ("006", "Vị trí nút Khóa / Mở khóa", "P1", PRE,
         "1. Mở màn hình\n2. Nhìn cột Trạng thái và cột Hành động", "—",
         "- Nút Khóa / Mở khóa nằm ngay cạnh nhãn trạng thái, TRONG cột Trạng thái\n"
         "- Cột Hành động có 4 nút: Xem, Sửa, Lịch sử chỉnh sửa, Xóa"),

        ("007", "Bảng trống khi bộ lọc không khớp gì", "P1", PRE,
         "1. Gõ \"khongtontai123\" vào ô tìm nhanh\n2. Bấm Tìm kiếm", "khongtontai123",
         "- Bảng hiện thông báo không có dữ liệu phù hợp\n- Tổng dưới bảng là 0"),
    ]),

    ("II", "BỘ LỌC & TÌM KIẾM", [
        ("001", "Tìm nhanh theo Mã loại tài khoản", "P0", PRE,
         "1. Gõ mã của một loại tài khoản vào ô tìm nhanh\n2. Bấm Tìm kiếm", "TKTS",
         "- Kết quả chỉ còn dòng có mã tương ứng"),

        ("002", "Tìm nhanh theo Tên loại tài khoản", "P0", PRE,
         "1. Gõ \"tài sản\" vào ô tìm nhanh\n2. Bấm Tìm kiếm", "tài sản",
         "- Kết quả gồm mọi loại có chuỗi \"tài sản\" trong tên\n"
         "⚠️ Gợi ý trong ô ghi rõ: \"Tìm theo mã hoặc tên loại tài khoản...\""),

        ("003", "Tìm nhanh khớp một phần chuỗi", "P1", PRE,
         "1. Gõ 2 ký tự đầu của một mã\n2. Bấm Tìm kiếm", "TK",
         "- Mọi mã bắt đầu bằng TK đều ra kết quả, không cần gõ đủ mã"),

        ("004", "Tìm nhanh không phân biệt hoa thường", "P1", PRE,
         "1. Gõ mã bằng chữ thường\n2. Bấm Tìm kiếm", "tkts",
         "- Kết quả giống hệt khi gõ chữ hoa"),

        ("005", "Gõ ô tìm nhanh mà chưa bấm Tìm kiếm", "P1", PRE,
         "1. Gõ từ khóa\n2. Chờ 5 giây, không bấm gì", "TKTS",
         "- Bảng vẫn giữ nguyên, chưa lọc"),

        ("006", "Lọc theo Trạng thái = Hoạt động", "P0", PRE,
         "1. Mở bộ lọc nâng cao\n2. Chọn Trạng thái = Hoạt động\n3. Bấm Tìm kiếm",
         "Trạng thái: Hoạt động",
         "- Kết quả 6 dòng, tất cả mang nhãn Hoạt động"),

        ("007", "Lọc theo Trạng thái = Khóa", "P0", PRE,
         "1. Chọn Trạng thái = Khóa\n2. Bấm Tìm kiếm", "Trạng thái: Khóa",
         "- Kết quả 1 dòng mang nhãn Khóa"),

        ("008", "Lọc theo Người tạo", "P0", PRE,
         "1. Mở bộ lọc nâng cao\n2. Chọn một người trong ô Người tạo\n3. Bấm Tìm kiếm",
         "Người tạo: một nhân viên có trong danh sách",
         "- Kết quả chỉ còn các loại tài khoản do người đó tạo\n"
         "- Danh sách chọn Người tạo chỉ liệt kê những người thực sự đã tạo bản ghi, "
         "không liệt kê toàn bộ nhân viên"),

        ("009", "Lọc theo Người cập nhật", "P0", PRE,
         "1. Chọn một người trong ô Người cập nhật\n2. Bấm Tìm kiếm",
         "Người cập nhật: một nhân viên có trong danh sách",
         "- Kết quả chỉ còn các loại tài khoản do người đó cập nhật gần nhất\n"
         "- Cột Cập nhật của mọi dòng đều hiện tên người vừa chọn"),

        ("010", "Lọc theo Cập nhật từ", "P0", PRE,
         "1. Nhập Cập nhật từ = ngày hôm nay\n2. Bấm Tìm kiếm", "Cập nhật từ: hôm nay",
         "- Chỉ còn các dòng có ngày cập nhật từ hôm nay trở đi\n"
         "- Dòng cập nhật đúng hôm nay VẪN nằm trong kết quả (tính cả ngày đầu)"),

        ("011", "Lọc theo Cập nhật đến", "P0", PRE,
         "1. Nhập Cập nhật đến = ngày hôm nay\n2. Bấm Tìm kiếm", "Cập nhật đến: hôm nay",
         "- Chỉ còn các dòng có ngày cập nhật đến hết hôm nay\n"
         "- Dòng cập nhật đúng hôm nay VẪN nằm trong kết quả (tính cả ngày cuối)\n"
         "⚠️ Bẫy hay gặp: dòng cập nhật lúc 15h hôm nay bị loại vì hệ thống cắt mốc từ 0h"),

        ("012", "Lọc khoảng ngày cập nhật đầy đủ", "P0", PRE,
         "1. Nhập Cập nhật từ = đầu tháng, Cập nhật đến = cuối tháng\n2. Bấm Tìm kiếm",
         "Cập nhật từ: 01 tháng này; đến: ngày cuối tháng này",
         "- Chỉ còn các dòng có ngày cập nhật nằm trong khoảng, tính cả 2 mốc"),

        ("013", "Nhập Cập nhật từ lớn hơn Cập nhật đến", "P1", PRE,
         "1. Nhập Cập nhật từ = hôm nay, Cập nhật đến = hôm qua\n2. Bấm Tìm kiếm",
         "Từ: hôm nay; Đến: hôm qua",
         "- Hệ thống hoặc báo khoảng ngày không hợp lệ, hoặc trả về kết quả rỗng\n"
         "- Không được lỗi trắng trang"),

        ("014", "Kết hợp nhiều điều kiện lọc", "P0", PRE,
         "1. Chọn Trạng thái = Hoạt động\n2. Chọn Người tạo\n3. Nhập khoảng ngày cập nhật\n"
         "4. Bấm Tìm kiếm", "Trạng thái + Người tạo + khoảng ngày",
         "- Kết quả phải thỏa ĐỒNG THỜI mọi điều kiện đã chọn"),

        ("015", "Nút Làm mới xóa hết điều kiện và nạp lại", "P0", PRE,
         "1. Đặt nhiều điều kiện lọc và bấm Tìm kiếm\n2. Bấm nút Làm mới", "—",
         "- Mọi ô lọc trở về trống\n"
         "- Danh sách tự nạp lại đủ 7 dòng NGAY, không cần bấm Tìm kiếm lần nữa\n"
         "⚠️ Bẫy hay gặp: xóa chữ trong ô nhưng bảng vẫn giữ kết quả lọc cũ"),

        ("016", "Bộ lọc được nhớ khi quay lại màn trong 10 phút", "P1", PRE,
         "1. Chọn Trạng thái = Khóa, bấm Tìm kiếm\n2. Sang màn khác\n3. Quay lại trong 10 phút",
         "Trạng thái: Khóa",
         "- Ô lọc và kết quả vẫn giữ nguyên, khối lọc nâng cao giữ nguyên trạng thái đóng/mở"),

        ("017", "Lọc xong tự về trang 1", "P1", PRE + " Đang đứng ở trang 2.",
         "1. Chuyển sang trang 2\n2. Đặt điều kiện lọc\n3. Bấm Tìm kiếm", "—",
         "- Kết quả hiển thị từ trang 1, không hiện bảng trống"),
    ]),

    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", [
        ("001", "Sắp xếp theo Mã loại tài khoản", "P0", PRE,
         "1. Bấm tiêu đề cột Mã loại tài khoản 1 lần rồi 2 lần", "—",
         "- Lần 1 xếp tăng dần A→Z, lần 2 xếp giảm dần Z→A\n"
         "- Mũi tên trên tiêu đề đổi chiều tương ứng"),

        ("002", "Sắp xếp theo Tên loại tài khoản", "P0", PRE,
         "1. Bấm tiêu đề cột Tên loại tài khoản", "—",
         "- Thứ tự các dòng thực sự thay đổi theo tên\n"
         "⚠️ Bẫy: mũi tên đổi chiều nhưng danh sách đứng yên — đó là lỗi"),

        ("003", "Cột STT và Hành động không sắp xếp được", "P2", PRE,
         "1. Bấm tiêu đề cột STT rồi cột Hành động", "—",
         "- Không có mũi tên sắp xếp, bấm vào không đổi thứ tự và không lỗi"),

        ("004", "Sắp xếp giữ nguyên khi chuyển trang", "P1", PRE + " Đặt cỡ trang 5 để có 2 trang.",
         "1. Sắp xếp theo Mã giảm dần\n2. Chuyển sang trang 2", "Cỡ trang: 5",
         "- Trang 2 tiếp nối đúng thứ tự đã sắp"),

        ("005", "Chuyển trang bằng nút số trang", "P0", PRE + " Đặt cỡ trang 5, có 2 trang.",
         "1. Bấm số trang 2", "Cỡ trang: 5",
         "- Bảng hiện các dòng còn lại\n- Cột STT bắt đầu từ 6\n"
         "- Dòng Hiển thị dưới bảng cập nhật đúng"),

        ("006", "Đổi cỡ trang", "P0", PRE,
         "1. Đổi cỡ trang từ 10 sang 50", "Cỡ trang: 50",
         "- Toàn bộ 7 dòng hiện trên 1 trang\n- Danh sách chỉ nạp lại đúng một lần"),

        ("007", "Đổi cỡ trang khi đang ở trang cuối", "P1",
         PRE + " Đang ở trang 2 với cỡ trang 5.",
         "1. Đổi cỡ trang sang 50", "Cỡ trang: 50",
         "- Bảng hiện dữ liệu từ trang 1, KHÔNG hiện bảng trống"),

        ("008", "Vào màn hình chỉ gọi dữ liệu một lần", "P1", PRE,
         "1. Mở màn hình từ menu\n2. Quan sát hiệu ứng tải của bảng", "—",
         "- Bảng chỉ tải một lượt, không chớp tải hai lần"),
    ]),

    ("IV", "THÊM / SỬA / XEM LOẠI TÀI KHOẢN", [
        ("001", "Mở cửa sổ Thêm loại tài khoản", "P0", PRE,
         "1. Bấm nút Tạo mới", "—",
         "- Mở cửa sổ tiêu đề \"Thêm loại tài khoản\"\n"
         "- Có 4 ô: Mã loại tài khoản (bắt buộc), Trạng thái, Tên loại tài khoản (bắt buộc), Ghi chú\n"
         "- Hai ô bắt buộc có dấu sao đỏ bên cạnh nhãn"),

        ("002", "Thêm mới đầy đủ thông tin", "P0", PRE,
         "1. Bấm Tạo mới\n2. Nhập đủ 4 ô\n3. Bấm Lưu",
         "Mã: LTK1; Tên: Loại kiểm thử; Ghi chú: Dùng để kiểm thử; Trạng thái: Hoạt động",
         "- Thông báo thêm mới thành công\n"
         "- Cửa sổ đóng, danh sách nạp lại và có dòng LTK1 với đủ thông tin vừa nhập"),

        ("003", "Thêm mới chỉ nhập các ô bắt buộc", "P0", PRE,
         "1. Bấm Tạo mới\n2. Chỉ nhập Mã và Tên\n3. Bấm Lưu", "Mã: LTK2; Tên: Loại kiểm thử 2",
         "- Lưu thành công\n- Cột Ghi chú của dòng mới để trống\n"
         "- Trạng thái mặc định là Hoạt động"),

        ("004", "Mở cửa sổ Sửa nạp đúng dữ liệu cũ", "P0", PRE,
         "1. Bấm nút Sửa trên một dòng đang Hoạt động", "—",
         "- Tiêu đề cửa sổ là \"Sửa loại tài khoản\"\n"
         "- Các ô điền sẵn đúng dữ liệu đang có\n"
         "- Cạnh tiêu đề hiện thông tin lần cập nhật gần nhất"),

        ("005", "Sửa Tên loại tài khoản", "P0", PRE,
         "1. Bấm Sửa dòng LTK1\n2. Đổi Tên\n3. Bấm Lưu", "Tên: Loại kiểm thử (đã sửa)",
         "- Thông báo cập nhật thành công\n"
         "- Danh sách hiện tên mới, cột Cập nhật đổi sang thời điểm và người vừa sửa"),

        ("006", "Sửa Ghi chú", "P1", PRE,
         "1. Bấm Sửa dòng LTK1\n2. Đổi Ghi chú\n3. Bấm Lưu", "Ghi chú: nội dung mới",
         "- Cập nhật thành công, cột Ghi chú hiện nội dung mới"),

        ("007", "Xóa trắng Ghi chú đang có", "P1", PRE,
         "1. Bấm Sửa dòng có Ghi chú\n2. Xóa trắng ô Ghi chú\n3. Bấm Lưu", "Ghi chú: (để trống)",
         "- Cập nhật thành công, cột Ghi chú thành trống"),

        ("008", "Nút Sửa bị vô hiệu với loại tài khoản đang Khóa", "P0",
         PRE + " Loại \"LTK khóa\" đang ở trạng thái Khóa.",
         "1. Rê chuột vào nút Sửa của dòng LTK khóa\n2. Thử bấm", "Loại LTK khóa",
         "- Nút Sửa bị mờ, không bấm được\n"
         "- Rê chuột hiện chú thích \"Loại tài khoản đã khóa → không cho sửa\"\n"
         "⚠️ Muốn sửa phải Mở khóa trước"),

        ("009", "Nút Xem mở ở chế độ chỉ đọc", "P0", PRE,
         "1. Bấm nút Xem trên một dòng bất kỳ", "—",
         "- Tiêu đề cửa sổ là \"Xem loại tài khoản\"\n"
         "- Mọi ô đều mờ, không gõ được\n- KHÔNG có nút Lưu, chỉ có nút Đóng"),

        ("010", "Xem được cả loại tài khoản đang Khóa", "P1", PRE,
         "1. Bấm nút Xem trên dòng đang Khóa", "Loại LTK khóa",
         "- Cửa sổ Xem mở bình thường và hiện đủ thông tin"),

        ("011", "Bấm Đóng khi chưa sửa gì", "P1", PRE,
         "1. Bấm Sửa một dòng\n2. Không đổi gì\n3. Bấm Đóng", "—",
         "- Cửa sổ đóng ngay, không hỏi lại"),

        ("012", "Cảnh báo khi đóng lúc đang sửa dở", "P0", PRE,
         "1. Bấm Sửa một dòng\n2. Đổi Tên nhưng chưa Lưu\n3. Bấm Đóng", "Tên: sửa dở dang",
         "- Hệ thống cảnh báo dữ liệu chưa lưu và hỏi xác nhận\n"
         "- Chọn ở lại thì cửa sổ vẫn mở và giữ nguyên nội dung đang gõ\n"
         "- Chọn thoát thì dữ liệu cũ không bị đổi"),

        ("013", "Chống bấm Lưu nhiều lần liên tiếp", "P1", PRE,
         "1. Bấm Tạo mới, nhập đủ\n2. Bấm Lưu liên tiếp 3 lần thật nhanh",
         "Mã: LTK9; Tên: Loại thử 9",
         "- Chỉ tạo ra ĐÚNG 1 bản ghi LTK9\n- Nút Lưu bị vô hiệu trong lúc xử lý"),

        ("014", "Loại tài khoản mới dùng được ngay ở màn Danh mục tài khoản", "P0", PRE,
         "1. Tạo mới loại LTK1 ở trạng thái Hoạt động\n"
         "2. Sang màn Danh mục tài khoản, bấm Tạo mới\n3. Mở danh sách chọn Loại tài khoản",
         "Loại: LTK1",
         "- LTK1 có trong danh sách chọn và chọn được"),
    ]),

    ("V", "KHÓA & MỞ KHÓA", [
        ("001", "Khóa một loại tài khoản chưa ai dùng", "P0", PRE,
         "1. Bấm nút Khóa ở cột Trạng thái dòng LTK thử\n2. Đọc hộp xác nhận\n3. Bấm Khóa",
         "Loại: LTK thử",
         "- Hộp xác nhận tiêu đề \"Xác nhận khóa\", câu hỏi nêu đúng tên loại tài khoản\n"
         "- Thông báo \"Khóa thành công\"\n"
         "- Dòng đổi nhãn sang Khóa, nút đổi thành hình ổ khóa mở, nút Sửa chuyển sang mờ"),

        ("002", "Mở khóa một loại tài khoản đang Khóa", "P0",
         PRE + " Loại LTK thử đang ở trạng thái Khóa.",
         "1. Bấm nút Mở khóa\n2. Bấm Mở khóa trong hộp xác nhận", "Loại: LTK thử",
         "- Hộp xác nhận tiêu đề \"Xác nhận mở khóa\"\n"
         "- Thông báo \"Mở khóa thành công\"\n"
         "- Dòng quay lại nhãn Hoạt động, nút Sửa sáng trở lại"),

        ("003", "Không khóa được loại tài khoản đang được sử dụng", "P0",
         PRE + " Loại \"Tài khoản tài sản\" đang được nhiều tài khoản dùng.",
         "1. Rê chuột vào nút Khóa của dòng Tài khoản tài sản\n2. Thử bấm",
         "Loại: Tài khoản tài sản",
         "- Nút Khóa bị mờ, không bấm được\n"
         "- Rê chuột hiện chú thích \"Đang được sử dụng, không thể khóa\"\n"
         "⚠️ Khác Danh mục tiền tệ: ở màn này đang dùng thì KHÔNG khóa được"),

        ("004", "Hủy hộp xác nhận khóa", "P1", PRE,
         "1. Bấm nút Khóa trên dòng LTK thử\n2. Bấm Hủy", "Loại: LTK thử",
         "- Hộp đóng, trạng thái không đổi, không có thông báo thành công"),

        ("005", "Loại tài khoản đã khóa không còn chọn được khi tạo tài khoản", "P0",
         PRE + " Loại LTK thử đang ở trạng thái Khóa.",
         "1. Sang màn Danh mục tài khoản, bấm Tạo mới\n2. Mở danh sách chọn Loại tài khoản",
         "Loại: LTK thử (đang Khóa)",
         "- LTK thử KHÔNG có trong danh sách chọn"),

        ("006", "Tài khoản cũ vẫn hiện đúng loại đã bị khóa", "P0",
         "Có sẵn 1 tài khoản đang gán loại \"Tài khoản tài sản\"; sau đó loại này bị chuyển sang Khóa.",
         "1. Khóa loại Tài khoản tài sản (sau khi đã gỡ hết ràng buộc nếu cần)\n"
         "2. Mở lại tài khoản cũ ở chế độ Sửa", "Loại: Tài khoản tài sản (đang Khóa)",
         "- Ô Loại tài khoản vẫn hiện đúng tên, không trống, không tự nhảy sang giá trị khác\n"
         "- Lưu lại tài khoản không làm mất giá trị loại\n"
         "⚠️ Quy tắc chung toàn hệ thống: danh mục bị khóa vẫn phải hiện ở bản ghi đang dùng nó"),

        ("007", "Người chỉ có quyền Xem không thấy nút Khóa", "P0",
         "Đăng nhập bằng tài khoản chỉ có quyền \"Xem danh mục loại tài khoản\".",
         "1. Mở màn hình\n2. Nhìn cột Trạng thái", "—",
         "- Cột Trạng thái chỉ có nhãn, không có nút Khóa / Mở khóa"),
    ]),

    ("VI", "XÓA", [
        ("001", "Xóa loại tài khoản chưa ai dùng", "P0", PRE,
         "1. Bấm nút Xóa trên dòng LTK thử\n2. Đọc hộp xác nhận\n3. Bấm Xóa", "Loại: LTK thử",
         "- Hộp xác nhận tiêu đề \"Xác nhận xóa\", câu hỏi nêu đúng tên loại tài khoản\n"
         "- Thông báo \"Xóa thành công\"\n- Dòng biến mất, tổng dưới bảng giảm 1"),

        ("002", "Hủy hộp xác nhận xóa", "P0", PRE,
         "1. Bấm nút Xóa trên dòng LTK thử\n2. Bấm Hủy", "Loại: LTK thử",
         "- Hộp đóng, dòng vẫn còn nguyên"),

        ("003", "Nút Xóa bị vô hiệu với loại đang được sử dụng", "P0",
         PRE + " Loại \"Tài khoản tài sản\" đang được nhiều tài khoản dùng.",
         "1. Rê chuột vào nút Xóa của dòng Tài khoản tài sản\n2. Thử bấm",
         "Loại: Tài khoản tài sản",
         "- Nút Xóa bị mờ, không bấm được\n"
         "- Rê chuột hiện chú thích \"Loại tài khoản đang được sử dụng, không thể xóa\""),

        ("004", "Chặn xóa khi bỏ qua giao diện", "P0",
         PRE + " Loại \"Tài khoản tài sản\" đang được sử dụng.",
         "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa loại Tài khoản tài sản\n"
         "2. Mở lại màn hình", "Loại: Tài khoản tài sản",
         "- Hệ thống chặn, báo loại tài khoản đang được sử dụng\n- Dòng vẫn còn\n"
         "⚠️ Không được dựa vào việc nút bị mờ ở giao diện để bảo vệ dữ liệu"),

        ("005", "Xóa loại tài khoản vừa bị người khác gán cho tài khoản", "P1",
         "Hai tài khoản cùng thao tác. Loại LTK thử ban đầu chưa ai dùng.",
         "1. Người 1 mở màn hình (nút Xóa của LTK thử đang sáng)\n"
         "2. Người 2 tạo một tài khoản gán loại LTK thử\n"
         "3. Người 1 bấm Xóa và xác nhận", "Loại: LTK thử",
         "- Hệ thống chặn lại, báo loại tài khoản đang được sử dụng\n- Dòng vẫn còn"),

        ("006", "Xóa dòng cuối cùng của trang", "P1",
         PRE + " Đang ở trang 2, trang 2 chỉ còn 1 dòng và dòng đó xóa được.",
         "1. Xóa dòng duy nhất của trang 2", "—",
         "- Xóa thành công\n- Màn tự lùi về trang 1, KHÔNG hiện bảng trống"),

        ("007", "Xóa loại tài khoản đang ở trạng thái Khóa", "P2",
         PRE + " Loại LTK thử đang Khóa và chưa ai dùng.",
         "1. Bấm Xóa và xác nhận", "Loại: LTK thử",
         "- Xóa được bình thường; trạng thái Khóa không cản việc xóa"),

        ("008", "Người chỉ có quyền Xem không thấy nút Xóa", "P0",
         "Đăng nhập bằng tài khoản chỉ có quyền \"Xem danh mục loại tài khoản\".",
         "1. Mở màn hình, nhìn cột Hành động", "—",
         "- Chỉ có nút Xem và nút Lịch sử chỉnh sửa, không có nút Xóa"),
    ]),

    ("VII", "LỊCH SỬ CHỈNH SỬA", [
        ("001", "Mở cửa sổ lịch sử chỉnh sửa", "P0", PRE,
         "1. Bấm nút Lịch sử chỉnh sửa trên một dòng đã từng bị sửa", "—",
         "- Mở cửa sổ tiêu đề \"Lịch sử chỉnh sửa loại tài khoản\"\n"
         "- Có danh sách các lần thay đổi kèm thời điểm và người thực hiện"),

        ("002", "Lịch sử ghi nhận lần sửa vừa thực hiện", "P0", PRE,
         "1. Sửa Tên của dòng LTK1 và Lưu\n2. Bấm nút Lịch sử chỉnh sửa của dòng đó",
         "Tên cũ: Loại kiểm thử → Tên mới: Loại kiểm thử A",
         "- Lịch sử có bản ghi mới nhất, nêu rõ trường Tên loại tài khoản đổi từ giá trị cũ "
         "sang giá trị mới\n- Ghi đúng người thực hiện và thời điểm"),

        ("003", "Lịch sử sắp xếp mới nhất lên đầu", "P0",
         PRE + " Dòng LTK1 đã bị sửa ít nhất 3 lần vào các thời điểm khác nhau.",
         "1. Mở cửa sổ lịch sử của LTK1\n2. Đọc thứ tự các dòng", "—",
         "- Lần sửa gần nhất nằm ở TRÊN CÙNG, các lần cũ xếp xuống dưới\n"
         "⚠️ Bẫy hay gặp: lịch sử xếp ngược, lần đầu tiên lại nằm trên cùng"),

        ("004", "Lịch sử ghi nhận thay đổi trạng thái", "P1", PRE,
         "1. Khóa dòng LTK1\n2. Mở cửa sổ lịch sử của dòng đó", "—",
         "- Có bản ghi cho biết Trạng thái đổi từ \"Hoạt động\" sang \"Khóa\"\n"
         "- Giá trị hiển thị bằng nhãn tiếng Việt, không phải con số"),

        ("005", "Lịch sử của bản ghi chưa từng bị sửa", "P2", PRE,
         "1. Tạo mới một loại tài khoản\n2. Bấm nút Lịch sử chỉnh sửa ngay", "Mã: LTK5",
         "- Cửa sổ mở bình thường\n"
         "- Chỉ có bản ghi của lần tạo, hoặc thông báo chưa có thay đổi nào; không lỗi"),

        ("006", "Đóng cửa sổ lịch sử", "P2", PRE,
         "1. Mở cửa sổ lịch sử\n2. Bấm Đóng", "—",
         "- Cửa sổ đóng, danh sách phía sau giữ nguyên bộ lọc và trang đang xem"),
    ]),

    ("VIII", "XUẤT EXCEL & NHẬP EXCEL", [
        ("001", "Xuất Excel toàn bộ danh mục", "P0", PRE,
         "1. Không lọc gì\n2. Bấm Xuất Excel\n3. Mở file tải về", "—",
         "- Thông báo \"Xuất Excel thành công\"\n- File mở được và có đủ 7 dòng"),

        ("002", "File Excel có đủ cột như trên màn hình", "P0", PRE,
         "1. Xuất Excel\n2. Đối chiếu tiêu đề cột với bảng trên màn hình", "—",
         "- File có các cột Mã loại tài khoản, Tên loại tài khoản, Ghi chú, Trạng thái\n"
         "- Tiêu đề cột bằng tiếng Việt giống trên màn hình"),

        ("003", "Xuất Excel theo đúng bộ lọc đang áp dụng", "P0", PRE,
         "1. Lọc Trạng thái = Khóa (còn 1 dòng)\n2. Xuất Excel\n3. Mở file", "Trạng thái: Khóa",
         "- File chỉ chứa đúng 1 dòng đang lọc\n"
         "⚠️ Bẫy hay gặp: file xuất toàn bộ danh mục, bỏ qua bộ lọc"),

        ("004", "Xuất Excel lấy đủ dữ liệu, không chỉ trang hiện tại", "P0",
         PRE + " Đặt cỡ trang 5 để có 2 trang.",
         "1. Đứng ở trang 1\n2. Xuất Excel\n3. Đếm số dòng trong file", "Cỡ trang: 5",
         "- File có đủ 7 dòng, không phải 5 dòng của trang đang xem"),

        ("005", "Tải file mẫu để nhập Excel", "P0", PRE,
         "1. Bấm nút Import Excel\n2. Bấm tải file mẫu\n3. Mở file mẫu", "—",
         "- Tải được file mẫu\n"
         "- File mẫu có đủ 4 cột: Mã loại tài khoản, Tên loại tài khoản, Ghi chú, Trạng thái\n"
         "- Hai cột bắt buộc được đánh dấu sao đỏ"),

        ("006", "Import Excel với dữ liệu hợp lệ", "P0", PRE,
         "1. Bấm Import Excel\n2. Chọn file có 3 dòng mã và tên đều mới\n3. Kiểm tra bảng xem trước\n"
         "4. Bấm xác nhận nhập", "3 dòng: IM1/IM2/IM3, tên và ghi chú đầy đủ",
         "- Bảng xem trước hiện đủ 3 dòng và đều được đánh là hợp lệ\n"
         "- Sau khi xác nhận: danh sách có thêm 3 loại tài khoản mới với đúng dữ liệu trong file"),

        ("007", "Import Excel thiếu cột bắt buộc", "P0", PRE,
         "1. Bấm Import Excel\n2. Chọn file có dòng bỏ trống cột Mã loại tài khoản\n"
         "3. Đọc bảng xem trước", "Dòng 2 bỏ trống Mã loại tài khoản",
         "- Dòng đó bị đánh dấu lỗi, nêu rõ thiếu Mã loại tài khoản\n"
         "- Chỉ các dòng hợp lệ được phép ghi vào"),

        ("008", "Import Excel có mã trùng dữ liệu đã có", "P0", PRE,
         "1. Chọn file có 1 dòng mang mã đã tồn tại trong danh mục\n2. Đọc bảng xem trước",
         "Dòng 1: mã TKTS (đã có)",
         "- Dòng đó bị đánh dấu lỗi trùng mã\n- Không tạo thêm bản ghi trùng mã"),

        ("009", "Import Excel có mã trùng nhau trong cùng file", "P1", PRE,
         "1. Chọn file có 2 dòng cùng mã IM9\n2. Đọc bảng xem trước", "Dòng 1 và dòng 3 cùng mã IM9",
         "- Hệ thống phát hiện trùng ngay trong file và chặn\n"
         "- Danh mục không xuất hiện 2 loại tài khoản cùng mã"),

        ("010", "Import Excel với file sai định dạng", "P1", PRE,
         "1. Bấm Import Excel\n2. Chọn một file không phải Excel", "File .txt",
         "- Hệ thống báo file không hợp lệ, không lỗi trắng trang"),

        ("011", "Import Excel với file rỗng", "P2", PRE,
         "1. Chọn file Excel chỉ có dòng tiêu đề", "File 0 dòng dữ liệu",
         "- Hệ thống báo không có dữ liệu để nhập, không tạo bản ghi nào"),

        ("012", "Dòng hợp lệ bị khóa sau khi kiểm tra", "P1", PRE,
         "1. Chọn file có cả dòng hợp lệ và dòng lỗi\n"
         "2. Quan sát bảng xem trước sau khi kiểm tra xong", "File 5 dòng: 3 hợp lệ, 2 lỗi",
         "- Dòng hợp lệ chuyển sang trạng thái khóa, không sửa được nữa\n"
         "- Dòng lỗi vẫn cho sửa tại chỗ để nhập lại\n"
         "- Phần mô tả dưới tiêu đề cửa sổ ghi rõ quy tắc này"),

        ("013", "Người chỉ có quyền Xem không thấy nút Import Excel", "P0",
         "Đăng nhập bằng tài khoản chỉ có quyền \"Xem danh mục loại tài khoản\".",
         "1. Mở màn hình, nhìn cụm nút dưới bảng", "—",
         "- Có nút Xuất Excel nhưng KHÔNG có nút Import Excel và không có nút Tạo mới"),
    ]),

    ("IX", "RÀNG BUỘC NHẬP LIỆU", [
        ("001", "Bỏ trống cả 2 ô bắt buộc", "P0", PRE,
         "1. Bấm Tạo mới\n2. Không nhập gì\n3. Bấm Lưu", "(để trống hết)",
         "- Ô Mã loại tài khoản và ô Tên loại tài khoản viền đỏ, hiện chữ đỏ "
         "\"Bắt buộc phải nhập\" ngay dưới ô\n- Cửa sổ không đóng, không tạo bản ghi"),

        ("002", "Bỏ trống riêng Mã loại tài khoản", "P0", PRE,
         "1. Bấm Tạo mới\n2. Chỉ nhập Tên\n3. Bấm Lưu", "Tên: Loại thử",
         "- Chỉ ô Mã loại tài khoản báo lỗi\n- Dữ liệu ở ô Tên vẫn còn nguyên"),

        ("003", "Nhập trùng Mã loại tài khoản", "P0", PRE,
         "1. Bấm Tạo mới\n2. Nhập Mã đã tồn tại\n3. Bấm Lưu", "Mã: TKTS; Tên: Trùng mã",
         "- Ô Mã báo \"Mã loại tài khoản đã tồn tại\", không lưu"),

        ("004", "Nhập trùng Tên loại tài khoản", "P0", PRE,
         "1. Bấm Tạo mới\n2. Nhập Tên đã tồn tại\n3. Bấm Lưu", "Mã: MOI1; Tên: Tài khoản tài sản",
         "- Ô Tên báo \"Tên loại tài khoản đã tồn tại\", không lưu\n"
         "⚠️ Khác Danh mục tiền tệ: ở màn này TÊN cũng phải là duy nhất"),

        ("005", "Sửa mà giữ nguyên Mã và Tên của chính nó", "P0", PRE,
         "1. Bấm Sửa một dòng\n2. Giữ nguyên Mã và Tên, chỉ đổi Ghi chú\n3. Bấm Lưu",
         "Ghi chú: nội dung mới",
         "- Lưu thành công\n"
         "⚠️ Bẫy hay gặp: hệ thống coi mã/tên của chính bản ghi đang sửa là trùng và chặn nhầm"),

        ("006", "Nhập Mã dài hơn 255 ký tự", "P2", PRE,
         "1. Bấm Tạo mới\n2. Dán chuỗi 300 ký tự vào ô Mã\n3. Bấm Lưu", "Mã: chuỗi 300 ký tự",
         "- Báo \"Tối đa 255 ký tự\", không lưu"),

        ("007", "Nhập Tên dài hơn 255 ký tự", "P2", PRE,
         "1. Bấm Tạo mới\n2. Dán chuỗi 300 ký tự vào ô Tên\n3. Bấm Lưu", "Tên: chuỗi 300 ký tự",
         "- Báo \"Tối đa 255 ký tự\", không lưu"),

        ("008", "Nhập Ghi chú dài hơn 255 ký tự", "P2", PRE,
         "1. Bấm Tạo mới\n2. Dán chuỗi 300 ký tự vào ô Ghi chú\n3. Bấm Lưu",
         "Ghi chú: chuỗi 300 ký tự",
         "- Báo \"Tối đa 255 ký tự\", không lưu"),

        ("009", "Nhập tên có dấu tiếng Việt", "P1", PRE,
         "1. Bấm Tạo mới\n2. Nhập Tên có dấu đầy đủ\n3. Bấm Lưu",
         "Mã: LTKV; Tên: Tài khoản phải thu khách hàng",
         "- Lưu thành công, danh sách hiện đúng dấu tiếng Việt"),

        ("010", "Lỗi biến mất sau khi nhập lại đúng", "P1", PRE,
         "1. Bấm Tạo mới, bấm Lưu ngay để 2 ô báo đỏ\n2. Nhập đủ 2 ô\n3. Bấm Lưu",
         "Mã: OK1; Tên: Hết lỗi",
         "- Viền đỏ và chữ đỏ biến mất khi nhập đủ\n- Lưu thành công"),

        ("011", "Khoảng trắng đầu cuối trong Mã", "P2", PRE,
         "1. Bấm Tạo mới\n2. Nhập Mã = \"  ABC  \"\n3. Bấm Lưu và xem danh sách", "Mã: \"  ABC  \"",
         "- Danh sách hiện mã ABC không có khoảng trắng thừa\n"
         "- Không tạo được 2 loại mà mắt thường nhìn thấy mã giống hệt nhau"),
    ]),

    ("X", "LUỒNG XUYÊN SUỐT", [
        ("001", "Vòng đời đầy đủ của một loại tài khoản", "P0", PRE,
         "1. Tạo mới loại LTK1\n2. Tìm lại bằng ô tìm nhanh\n3. Sửa Tên và Ghi chú\n"
         "4. Xem lịch sử chỉnh sửa\n5. Khóa rồi Mở khóa\n6. Xuất Excel kiểm tra có LTK1\n7. Xóa LTK1",
         "Mã: LTK1; Tên: Loại kiểm thử",
         "- Từng bước có thông báo thành công tương ứng\n"
         "- Bước 4 lịch sử ghi nhận đúng lần sửa ở bước 3\n"
         "- Sau bước 7, LTK1 không còn trong danh sách và không còn trong file Excel xuất lại"),

        ("002", "Khóa để ngừng dùng thay vì xóa", "P0",
         PRE + " Loại \"Tài khoản tài sản\" đang được nhiều tài khoản dùng.",
         "1. Thử xóa → nút Xóa mờ, không bấm được\n"
         "2. Thử khóa → nút Khóa cũng mờ, không bấm được\n"
         "3. Rê chuột đọc chú thích trên cả hai nút", "Loại: Tài khoản tài sản",
         "- Cả hai nút đều mờ với chú thích nêu rõ đang được sử dụng\n"
         "⚠️ Ở màn này, loại tài khoản đang dùng thì KHÔNG khóa và KHÔNG xóa được — "
         "muốn ngừng dùng phải chuyển hết tài khoản sang loại khác trước"),

        ("003", "Import Excel rồi kiểm tra lại toàn bộ", "P1", PRE,
         "1. Import Excel 3 dòng mới\n2. Lọc lại danh sách theo Người tạo là chính mình\n"
         "3. Mở lịch sử chỉnh sửa của 1 trong 3 dòng vừa nhập\n4. Xuất Excel", "File 3 dòng",
         "- 3 dòng mới đều có trong danh sách và trong file Excel xuất ra\n"
         "- Lịch sử ghi nhận lần tạo của các dòng đó\n"
         "- Bộ lọc Người tạo bắt đúng 3 dòng vừa nhập"),

        ("004", "Kiểm tra nhất quán giữa hai cổng", "P1", PRE,
         "1. Tạo mới loại LTK1 ở cổng mới\n2. Mở danh mục loại tài khoản ở cổng cũ, tìm LTK1\n"
         "3. Sửa Ghi chú của LTK1 ở cổng cũ\n4. Quay lại cổng mới, nạp lại danh sách",
         "Mã: LTK1",
         "- Bước 2: cổng cũ thấy LTK1\n- Bước 4: cổng mới hiện ghi chú vừa sửa\n"
         "⚠️ Hai cổng dùng chung một danh mục, mọi sai lệch đều là lỗi"),
    ]),
]

build(output_file=OUTPUT_FILE, sheet_name=SHEET_NAME, feature_name=FEATURE_NAME,
      module_name=MODULE_NAME, description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS, sections=SECTIONS)
