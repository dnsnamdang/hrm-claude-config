# -*- coding: utf-8 -*-
"""Sinh file testcase Excel cho man DANH MUC "Ly do huy cuoc hop" (/assign/meeting_cancel_reason).

Chay:  python .plans/danh-muc-ly-do-huy-cuoc-hop/gen_testcase.py
"""
import os
import sys

try:  # console Windows mac dinh cp1252 -> print tieng Viet se no UnicodeEncodeError
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", ".claude", "skills",
                                "testcase-documenter", "assets"))

from tc_engine import build  # noqa: E402

FEATURE = "Danh mục Lý do hủy cuộc họp"
MODULE = "Giao việc - Danh mục"
OUTPUT = os.path.join(HERE, "testcase - Danh mục lý do hủy cuộc họp.xlsx")

# ---------------------------------------------------------------- bo du lieu mau dung xuyen suot
FIX = (
    "Danh mục thử nghiệm có 12 lý do (3 lý do hệ thống tạo sẵn + 9 lý do nhóm kiểm thử thêm):\n"
    "- Hủy do khách dời lịch — Hoạt động — 0 cuộc họp dùng\n"
    "- Hủy do khách không gặp — Hoạt động — 4 cuộc họp dùng\n"
    "- Hủy do mình bận đột xuất — Hoạt động — 0 cuộc họp dùng\n"
    "- Hủy do thời tiết xấu — Hoạt động — 0 cuộc họp dùng — người tạo Phan Văn Khôi\n"
    "- Hủy do phòng họp bị trùng — Khóa — 0 cuộc họp dùng\n"
    "- Hủy do khách hẹn lại tuần sau — Hoạt động — 3 cuộc họp dùng\n"
    "- Hủy do thiếu tài liệu chuẩn bị — Hoạt động — 0 cuộc họp dùng — người tạo Trần Thị Thu\n"
    "- 5 lý do còn lại: Hoạt động, 0 cuộc họp dùng, người tạo Đặng Văn Nam"
)

ACC = (
    "3 tài khoản kiểm thử:\n"
    "- Tài khoản A (Phan Văn Khôi): có quyền Quản lý danh mục lý do hủy cuộc họp\n"
    "- Tài khoản B (Trần Thị Thu): CHỈ có quyền Xem danh mục lý do hủy cuộc họp\n"
    "- Tài khoản C (Lê Văn Hùng): không có cả 2 quyền trên"
)

MENU = ("Đăng nhập → vào phân hệ Giao việc → mở nhóm \"Danh mục\" ở thanh menu bên trái → "
        "bấm mục \"Lý do hủy cuộc họp\"")

# ---------------------------------------------------------------- 1. KHOI MO TA (9 muc)
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Quản lý danh mục \"Lý do hủy cuộc họp\" của phân hệ Giao việc: thêm / sửa / xem / khóa - mở khóa / "
     "xóa, nhập danh sách từ Excel và xuất danh sách ra Excel.\n"
     "Danh mục này là NGUỒN DUY NHẤT cho ô chọn lý do ở cửa sổ \"Hủy cuộc họp\" — người dùng bắt buộc "
     "chọn một lý do trong danh mục khi hủy một cuộc họp, nên dữ liệu ở đây ảnh hưởng trực tiếp sang "
     "màn Cuộc họp và các báo cáo có cột Lý do hủy."),

    ("2. Đối tượng được tính / hiển thị",
     "Màn danh sách hiển thị TẤT CẢ lý do trong danh mục, không loại trừ bản ghi nào:\n"
     "- Lý do ở trạng thái Hoạt động (thẻ xanh, biểu tượng dấu tích)\n"
     "- Lý do ở trạng thái Khóa (thẻ xám, biểu tượng ổ khóa)\n"
     "- Lý do đang được cuộc họp sử dụng và lý do chưa được cuộc họp nào dùng\n"
     "- 3 lý do hệ thống tạo sẵn: Hủy do khách dời lịch · Hủy do khách không gặp · Hủy do mình bận đột xuất\n"
     "Danh mục dùng chung toàn hệ thống: KHÔNG chia theo công ty / phòng ban / bộ phận, mọi tài khoản có "
     "quyền đều nhìn thấy đúng một danh sách giống nhau.\n"
     "Riêng ô chọn lý do trong cửa sổ \"Hủy cuộc họp\" chỉ lấy lý do đang Hoạt động, xếp theo thứ tự tạo "
     "từ cũ đến mới."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Lý do đang Khóa: KHÔNG xuất hiện trong ô chọn lý do ở cửa sổ \"Hủy cuộc họp\" (không chọn mới "
     "được nữa), nhưng vẫn hiển thị đầy đủ ở màn danh mục và vẫn hiện đúng tên trên các cuộc họp đã hủy "
     "bằng lý do đó từ trước.\n"
     "- Không có bản ghi nào bị ẩn khỏi màn danh sách vì lý do phân quyền hay cấp tổ chức.\n"
     "- Cuộc họp bị hủy tự động bởi hệ thống (không do người dùng bấm hủy) không gắn lý do trong danh "
     "mục này, cột Lý do hủy của các cuộc họp đó giữ nguyên nội dung cũ."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Cặp ô lọc \"Cập nhật từ\" và \"Đến\" áp dụng cho cột Cập nhật (thời điểm chỉnh sửa gần nhất của "
     "lý do), so sánh theo NGÀY và bao gồm cả hai đầu mốc: chọn 01/09/2026 đến 10/09/2026 thì lý do cập "
     "nhật lúc 10/09/2026 23:30 vẫn được tính.\n"
     "Màn KHÔNG có bộ lọc theo Ngày tạo — muốn tìm theo người lập thì dùng ô lọc Người tạo."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Bảng phẳng một cấp, không có cha - con, không nhóm. Mỗi dòng là một lý do hủy gồm: STT · Lý do hủy "
     "cuộc họp · Mô tả · Người tạo · Ngày tạo · Cập nhật (ngày giờ kèm dòng \"bởi + tên người cập nhật\") "
     "· Trạng thái (kèm nút khóa / mở khóa) · Hành động (Xem · Sửa · Xóa).\n"
     "Mỗi lý do có thể được nhiều cuộc họp dùng; số cuộc họp đang dùng quyết định lý do đó còn xóa được "
     "hay không."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "Tên lý do là DUY NHẤT trên toàn hệ thống:\n"
     "- Thêm mới hoặc sửa mà trùng tên một lý do đã có (kể cả khác chữ hoa - chữ thường) đều bị chặn với "
     "thông báo \"Lý do hủy cuộc họp đã tồn tại trong hệ thống\".\n"
     "- Sửa mà giữ nguyên tên cũ của chính nó thì KHÔNG bị coi là trùng.\n"
     "- Khi nhập từ tệp Excel, hệ thống còn cắt bỏ khoảng trắng đầu - cuối và bỏ qua khác biệt chữ hoa - "
     "chữ thường, đồng thời chặn hai dòng trùng nhau trong cùng một tệp (báo rõ số dòng trùng)."),

    ("7. Phân quyền cấp",
     "Đúng 2 quyền, cấp trong phần Phân quyền của hệ thống, nhóm \"Danh mục\":\n"
     "- \"Quản lý danh mục lý do hủy cuộc họp\": xem danh sách, thêm, sửa, xóa, khóa / mở khóa, nhập từ "
     "Excel, xuất Excel.\n"
     "- \"Xem danh mục lý do hủy cuộc họp\": chỉ xem danh sách và xem chi tiết một lý do.\n"
     "Có một trong hai quyền là nhìn thấy mục menu \"Lý do hủy cuộc họp\". Không có quyền nào thì không "
     "thấy mục menu và không mở được màn.\n"
     "Danh mục KHÔNG phân quyền theo cấp tổ chức (công ty / phòng ban / bộ phận).\n"
     "Riêng ô chọn lý do trong cửa sổ \"Hủy cuộc họp\" không đòi hai quyền trên — người dùng hủy được "
     "cuộc họp mà không cần quyền quản trị danh mục (đúng thiết kế)."),

    ("8. Cách tính các ô thống kê",
     "- Dòng \"Hiển thị a–b / N lý do\" dưới bảng: a là số thứ tự dòng đầu tiên của trang đang xem, b là "
     "dòng cuối cùng của trang, N là tổng số lý do khớp bộ lọc hiện tại (không phải tổng toàn danh mục).\n"
     "- Cột STT đánh số liên tục theo toàn bộ kết quả lọc, không đánh lại từ 1 ở mỗi trang: trang 2 với "
     "10 dòng mỗi trang bắt đầu từ 11.\n"
     "- Ô chọn số dòng mỗi trang có 4 mức: 5 · 10 · 20 · 50, mặc định 10.\n"
     "- Cột Cập nhật hiển thị theo dạng ngày/tháng/năm giờ:phút, dòng dưới ghi \"bởi <tên người cập nhật "
     "gần nhất>\".\n"
     "- Tệp Excel xuất ra chứa TẤT CẢ dòng khớp bộ lọc (tối đa 10.000 dòng), không chỉ dòng của trang "
     "đang xem."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất của màn này — đọc trước khi chạy test:\n"
     "1) Đổi ô lọc nâng cao (Trạng thái, Người tạo, Người cập nhật, khoảng ngày) là danh sách TỰ tải lại "
     "ngay; riêng ô tìm nhanh phải bấm nút Tìm kiếm hoặc nhấn Enter mới áp dụng.\n"
     "2) Ô tìm nhanh tìm cả trong cột Mô tả, không chỉ tên lý do — kết quả có thể chứa dòng mà tên không "
     "khớp chữ đã gõ.\n"
     "3) Chỉ cột Cập nhật bấm sắp xếp được; các cột khác không có mũi tên sắp xếp.\n"
     "4) Lý do đang Khóa thì nút Sửa bị làm mờ — muốn sửa phải Mở khóa trước.\n"
     "5) Lý do đã được ít nhất một cuộc họp dùng thì nút Xóa bị mờ xám vĩnh viễn; cách duy nhất để ngừng "
     "dùng là Khóa nó lại.\n"
     "6) Khóa một lý do KHÔNG làm mất tên lý do trên các cuộc họp đã hủy trước đó.\n"
     "7) Nút Xuất Excel xuất theo bộ lọc đang áp dụng, KHÔNG phải toàn bộ danh mục.\n"
     "8) Nhập từ Excel: ô Trạng thái phải gõ đúng chính xác \"Hoạt động\" hoặc \"Khóa\" (đúng dấu, đúng "
     "chữ hoa - chữ thường); gõ \"hoạt động\" thường hay \"Hoat dong\" không dấu đều bị coi là sai.\n"
     "9) Cửa sổ Thêm có nút \"Lưu và tiếp tục\", cửa sổ Sửa thì không.\n"
     "10) Xóa dòng cuối cùng của một trang có thể làm trang đang xem trống — đây không phải lỗi, bấm về "
     "trang trước vẫn thấy đủ dữ liệu."),
]

# ---------------------------------------------------------------- 2. PHAN QUYEN
ROLE_TCS = [
    ("01", "Tài khoản có quyền quản lý danh mục nhìn thấy và dùng được đầy đủ chức năng", "P0",
     ACC + "\n" + FIX,
     "1. Đăng nhập bằng tài khoản A\n"
     "2. " + MENU + "\n"
     "3. Quan sát khu vực nút phía trên bảng và cột Hành động của từng dòng",
     "Tài khoản: A (quyền Quản lý danh mục lý do hủy cuộc họp)",
     "- Mục menu \"Lý do hủy cuộc họp\" hiện trong nhóm Danh mục của phân hệ Giao việc\n"
     "- Màn mở ra, bảng hiện đủ 12 lý do\n"
     "- Phía trên bảng có đủ 3 nút: Tạo mới (xanh dương) · Import Excel (cam) · Xuất Excel (xanh lá)\n"
     "- Mỗi dòng có nút Xem, nút Sửa, nút Xóa; cột Trạng thái có thêm nút khóa / mở khóa"),

    ("02", "Tài khoản chỉ có quyền xem danh mục chỉ được xem, không thao tác được", "P0",
     ACC + "\n" + FIX,
     "1. Đăng nhập bằng tài khoản B\n"
     "2. " + MENU + "\n"
     "3. Quan sát khu vực nút phía trên bảng, cột Trạng thái và cột Hành động\n"
     "4. Bấm nút Xem ở dòng bất kỳ",
     "Tài khoản: B (chỉ có quyền Xem danh mục lý do hủy cuộc họp)",
     "- Vẫn nhìn thấy mục menu và mở được màn, bảng hiện đủ 12 lý do\n"
     "- KHÔNG có nút Tạo mới, KHÔNG có nút Import Excel, KHÔNG có nút Xuất Excel\n"
     "- Cột Trạng thái chỉ hiện thẻ trạng thái, KHÔNG có nút khóa / mở khóa\n"
     "- Cột Hành động chỉ còn nút Xem; không có nút Sửa và nút Xóa\n"
     "- Bấm Xem mở được cửa sổ xem chi tiết, mọi ô ở chế độ chỉ đọc, chỉ có nút Đóng"),

    ("03", "Tài khoản không có quyền nào của danh mục không vào được màn", "P0",
     ACC,
     "1. Đăng nhập bằng tài khoản C\n"
     "2. Vào phân hệ Giao việc, mở nhóm \"Danh mục\", tìm mục \"Lý do hủy cuộc họp\"\n"
     "3. Gõ thẳng đường dẫn màn danh mục lý do hủy cuộc họp lên thanh địa chỉ và nhấn Enter",
     "Tài khoản: C (không có quyền nào của danh mục)",
     "- Nhóm Danh mục KHÔNG có mục \"Lý do hủy cuộc họp\"\n"
     "- Gõ thẳng đường dẫn thì hệ thống từ chối, đưa về trang báo không có quyền truy cập\n"
     "- ⚠️ Không được hiện bảng dữ liệu rỗng kèm nút Tạo mới; cũng không được để trang treo hoặc trắng"),

    ("04", "Chặn thêm mới khi gọi thẳng chức năng, bỏ qua giao diện", "P0",
     ACC + "\nDành cho tester kỹ thuật. Chuẩn bị công cụ kiểm thử gọi thẳng chức năng và mã đăng nhập "
     "của tài khoản B và tài khoản C.",
     "1. Đăng nhập lấy mã phiên của tài khoản B\n"
     "2. Dùng công cụ kiểm thử gọi thẳng chức năng Lưu lý do hủy cuộc họp với tên \"Lý do thử bỏ qua "
     "giao diện\"\n"
     "3. Lặp lại bước 2 với mã phiên của tài khoản C\n"
     "4. Đăng nhập lại bằng tài khoản A, mở màn danh mục và tìm tên vừa gửi",
     "Tên gửi lên: Lý do thử bỏ qua giao diện · Trạng thái: Hoạt động",
     "- Cả 2 lần gọi đều bị hệ thống từ chối với thông báo không có quyền\n"
     "- ⚠️ Danh mục KHÔNG phát sinh dòng \"Lý do thử bỏ qua giao diện\"; tổng số lý do vẫn là 12"),

    ("05", "Chặn sửa khi gọi thẳng chức năng, bỏ qua giao diện", "P0",
     ACC + "\nDành cho tester kỹ thuật. Lý do \"Hủy do thời tiết xấu\" đang Hoạt động.",
     "1. Đăng nhập lấy mã phiên của tài khoản B\n"
     "2. Dùng công cụ kiểm thử gọi thẳng chức năng Lưu, trỏ vào lý do \"Hủy do thời tiết xấu\", đổi tên "
     "thành \"Tên bị sửa trộm\"\n"
     "3. Đăng nhập lại bằng tài khoản A, mở màn danh mục, tìm lại lý do đó",
     "Tên mới gửi lên: Tên bị sửa trộm",
     "- Hệ thống từ chối, báo không có quyền\n"
     "- Lý do vẫn giữ nguyên tên \"Hủy do thời tiết xấu\", cột Cập nhật không đổi"),

    ("06", "Chặn xóa khi gọi thẳng chức năng, bỏ qua giao diện", "P0",
     ACC + "\nDành cho tester kỹ thuật. Lý do \"Hủy do thiếu tài liệu chuẩn bị\" chưa cuộc họp nào dùng.",
     "1. Đăng nhập lấy mã phiên của tài khoản B\n"
     "2. Dùng công cụ kiểm thử gọi thẳng chức năng Xóa, trỏ vào lý do \"Hủy do thiếu tài liệu chuẩn bị\"\n"
     "3. Lặp lại với mã phiên của tài khoản C\n"
     "4. Đăng nhập bằng tài khoản A, kiểm tra lại danh mục",
     "—",
     "- Cả 2 lần đều bị từ chối, báo không có quyền\n"
     "- ⚠️ Lý do \"Hủy do thiếu tài liệu chuẩn bị\" vẫn còn nguyên trong danh mục"),

    ("07", "Chặn khóa và mở khóa khi gọi thẳng chức năng, bỏ qua giao diện", "P1",
     ACC + "\nDành cho tester kỹ thuật. \"Hủy do khách dời lịch\" đang Hoạt động, \"Hủy do phòng họp bị "
     "trùng\" đang Khóa.",
     "1. Đăng nhập lấy mã phiên của tài khoản B\n"
     "2. Gọi thẳng chức năng Khóa, trỏ vào \"Hủy do khách dời lịch\"\n"
     "3. Gọi thẳng chức năng Mở khóa, trỏ vào \"Hủy do phòng họp bị trùng\"\n"
     "4. Đăng nhập bằng tài khoản A và kiểm tra lại 2 dòng trên",
     "—",
     "- Cả 2 lần gọi đều bị từ chối, báo không có quyền\n"
     "- Trạng thái 2 lý do giữ nguyên: một Hoạt động, một Khóa"),

    ("08", "Chặn xuất Excel khi gọi thẳng chức năng, bỏ qua giao diện", "P1",
     ACC + "\nDành cho tester kỹ thuật.",
     "1. Đăng nhập lấy mã phiên của tài khoản B\n"
     "2. Dùng công cụ kiểm thử gọi thẳng chức năng Xuất Excel của danh mục lý do hủy cuộc họp\n"
     "3. Lặp lại với mã phiên của tài khoản C",
     "—",
     "- Cả 2 lần đều bị từ chối, báo không có quyền\n"
     "- ⚠️ Không có tệp Excel nào được trả về (tài khoản chỉ có quyền xem cũng không được xuất dữ liệu ra)"),

    ("09", "Chặn nhập từ Excel khi gọi thẳng chức năng, bỏ qua giao diện", "P1",
     ACC + "\nDành cho tester kỹ thuật.",
     "1. Đăng nhập lấy mã phiên của tài khoản B\n"
     "2. Gọi thẳng chức năng Kiểm tra dữ liệu nhập với 1 dòng hợp lệ\n"
     "3. Gọi thẳng chức năng Nhập dữ liệu với đúng 1 dòng đó\n"
     "4. Đăng nhập bằng tài khoản A và kiểm tra danh mục",
     "1 dòng: Lý do hủy cuộc họp = Lý do nhập trộm · Trạng thái = Hoạt động",
     "- Cả 2 lần gọi đều bị từ chối, báo không có quyền\n"
     "- Danh mục không phát sinh dòng \"Lý do nhập trộm\""),

    ("10", "Người không có quyền danh mục vẫn hủy được cuộc họp và chọn được lý do", "P0",
     ACC + "\nTài khoản C là người tạo một cuộc họp chưa tới giờ bắt đầu.",
     "1. Đăng nhập bằng tài khoản C\n"
     "2. Mở cuộc họp do chính mình tạo, chưa tới giờ bắt đầu\n"
     "3. Bấm nút Hủy\n"
     "4. Mở ô chọn Lý do hủy trong cửa sổ hiện ra",
     "—",
     "- ⚠️ Đúng thiết kế: ô chọn lý do vẫn liệt kê đầy đủ các lý do đang Hoạt động dù tài khoản C không "
     "có quyền nào của danh mục\n"
     "- Chọn lý do và xác nhận thì cuộc họp hủy thành công\n"
     "- Tài khoản C vẫn không nhìn thấy mục menu danh mục, không sửa được danh mục"),

    ("11", "Gỡ quyền giữa chừng thì thao tác tiếp theo bị chặn", "P1",
     ACC + "\nTài khoản A đang mở sẵn màn danh mục.",
     "1. Tài khoản A mở màn danh mục, để nguyên trang\n"
     "2. Quản trị viên gỡ quyền Quản lý danh mục lý do hủy cuộc họp của tài khoản A\n"
     "3. Tài khoản A bấm Tạo mới, nhập tên mới rồi bấm Lưu (chưa tải lại trang)",
     "Tên: Lý do sau khi bị gỡ quyền",
     "- Hệ thống từ chối, báo không có quyền; cửa sổ không báo thêm mới thành công\n"
     "- Sau khi tải lại trang, mục menu và các nút thao tác biến mất\n"
     "- Danh mục không phát sinh dòng mới"),
]

# ---------------------------------------------------------------- 3. CAC SECTION NGHIEP VU
S1 = [
    (1, "Mở màn danh mục đúng đường menu", "P0", ACC + "\n" + FIX,
     "1. Đăng nhập bằng tài khoản A\n"
     "2. " + MENU + "\n"
     "3. Đối chiếu số dòng hiện ra với số lý do đang có",
     "—",
     "- Màn mở ra với tiêu đề bảng \"Danh sách lý do hủy cuộc họp\"\n"
     "- Bảng hiện đủ 12 lý do, dòng \"Hiển thị 1–10 / 12 lý do\" nằm dưới bảng\n"
     "- Không có thông báo lỗi nào trên màn"),

    (2, "Kiểm tra tiêu đề và phần đầu màn", "P2", FIX,
     "1. Mở màn danh mục\n2. Quan sát tiêu đề trình duyệt, khối bộ lọc và tiêu đề bảng",
     "—",
     "- Tiêu đề tab trình duyệt: Danh sách lý do hủy cuộc họp\n"
     "- Khối bộ lọc có tiêu đề \"Bộ lọc danh sách lý do hủy cuộc họp\" và dòng phụ \"Bạn có thể chọn tìm "
     "kiếm nâng cao để lọc nhiều thông tin hơn\"\n"
     "- Ô tìm nhanh có chữ gợi ý \"Tìm theo lý do hủy cuộc họp, mô tả\""),

    (3, "Kiểm tra đủ và đúng thứ tự các cột của bảng", "P0", FIX,
     "1. Mở màn danh mục\n2. Đọc lần lượt tiêu đề các cột từ trái sang phải",
     "—",
     "- Đúng 8 cột theo thứ tự: STT · Lý do hủy cuộc họp · Mô tả · Người tạo · Ngày tạo · Cập nhật · "
     "Trạng thái · Hành động\n"
     "- Chỉ cột Cập nhật có biểu tượng sắp xếp"),

    (4, "Bộ lọc nâng cao mặc định đang thu gọn", "P1", FIX,
     "1. Mở màn danh mục lần đầu trong phiên đăng nhập\n2. Quan sát khối bộ lọc",
     "—",
     "- Chỉ hiện ô tìm nhanh cùng 2 nút Tìm kiếm và Làm mới\n"
     "- Các ô Trạng thái, Người tạo, Người cập nhật gần nhất, Cập nhật từ, Đến đang bị ẩn"),

    (5, "Mở và đóng bộ lọc nâng cao", "P1", FIX,
     "1. Bấm \"Tìm kiếm nâng cao\"\n2. Quan sát các ô lọc hiện ra\n3. Bấm \"Ẩn tìm kiếm nâng cao\"",
     "—",
     "- Khi mở: hiện đủ 5 ô lọc — Trạng thái · Người tạo · Người cập nhật gần nhất · Cập nhật từ · Đến\n"
     "- Khi đóng: các ô thu lại, giá trị đã chọn trước đó KHÔNG bị xóa và danh sách không đổi"),

    (6, "Thứ tự mặc định của danh sách là mới thêm lên đầu", "P0",
     FIX + "\nVừa thêm lý do \"Hủy do khách đổi người dự\" cách đây 1 phút.",
     "1. Mở màn danh mục, không chọn bộ lọc nào\n2. Đọc dòng đầu tiên của bảng",
     "—",
     "- Dòng đầu tiên là \"Hủy do khách đổi người dự\" (lý do thêm gần đây nhất)\n"
     "- ⚠️ Mặc định KHÔNG sắp theo tên và cũng không sắp theo cột Cập nhật"),

    (7, "Mỗi trang mặc định 10 dòng", "P1", FIX,
     "1. Mở màn danh mục\n2. Đếm số dòng của trang 1 và đọc ô chọn số dòng mỗi trang",
     "—",
     "- Trang 1 có đúng 10 dòng\n- Ô chọn số dòng mỗi trang đang là 10\n- Thanh phân trang hiện 2 trang"),

    (8, "Gõ thẳng đường dẫn màn khi đã đăng nhập", "P1", ACC + "\n" + FIX,
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Gõ thẳng đường dẫn màn danh mục lý do hủy cuộc họp lên thanh địa chỉ, nhấn Enter",
     "—",
     "- Màn mở bình thường, danh sách giống hệt khi vào bằng menu\n- Không phải đăng nhập lại"),

    (9, "Thêm tham số lạ vào cuối đường dẫn", "P1", FIX,
     "1. Mở màn danh mục\n"
     "2. Sửa tay thanh địa chỉ, thêm một tham số lạ không có thật vào cuối đường dẫn rồi nhấn Enter\n"
     "3. Quan sát danh sách",
     "Tham số lạ: loai=khong-co-that",
     "- ⚠️ Hệ thống bỏ qua tham số lạ, màn vẫn mở đúng danh sách mặc định 12 lý do\n"
     "- Không báo lỗi, không hiện thêm hay bớt dữ liệu"),

    (10, "Nút Làm mới xóa hết điều kiện lọc", "P0",
     FIX + "\nĐang lọc Trạng thái = Khóa và gõ chữ \"phòng\" ở ô tìm nhanh, bảng còn 1 dòng.",
     "1. Bấm nút Làm mới\n2. Quan sát các ô lọc và bảng",
     "—",
     "- Ô tìm nhanh trống, ô Trạng thái trống, các ô lọc khác trống\n"
     "- Bảng trở lại đủ 12 lý do, quay về trang 1"),

    (11, "Tải lại trang sau khi lọc", "P2",
     FIX + "\nĐang lọc Trạng thái = Hoạt động.",
     "1. Nhấn F5 để tải lại trang\n2. Quan sát ô lọc Trạng thái và bảng",
     "—",
     "- ⚠️ Hệ thống KHÔNG ghi nhớ bộ lọc: ô Trạng thái trống trở lại và bảng hiện đủ 12 lý do"),

    (12, "Màn hiển thị khi không có dòng nào khớp bộ lọc", "P1",
     FIX,
     "1. Gõ vào ô tìm nhanh một chuỗi chắc chắn không có\n2. Bấm Tìm kiếm",
     "Từ khóa: zzzkhongtontai",
     "- Bảng không có dòng dữ liệu nào\n"
     "- Hiện đúng dòng chữ \"Không có dữ liệu phù hợp bộ lọc.\"\n"
     "- Không hiện thanh phân trang rác, không báo lỗi đỏ"),
]

S2 = [
    (1, "Tìm nhanh theo một phần tên lý do", "P0", FIX,
     "1. Gõ \"khách\" vào ô tìm nhanh\n2. Bấm nút Tìm kiếm\n3. Đếm và đọc tên các dòng trả về",
     "Từ khóa: khách",
     "- Chỉ còn các lý do có chữ \"khách\" trong tên: Hủy do khách dời lịch · Hủy do khách không gặp · "
     "Hủy do khách hẹn lại tuần sau\n"
     "- Dòng dưới bảng đổi thành \"Hiển thị 1–3 / 3 lý do\""),

    (2, "Tìm nhanh khớp cả nội dung cột Mô tả", "P0",
     FIX + "\nLý do \"Hủy do thời tiết xấu\" có mô tả \"Mưa bão, đường ngập, không di chuyển được\".",
     "1. Gõ \"đường ngập\" vào ô tìm nhanh\n2. Bấm Tìm kiếm",
     "Từ khóa: đường ngập",
     "- ⚠️ Vẫn ra dòng \"Hủy do thời tiết xấu\" dù tên lý do không chứa chữ đã gõ — ô tìm nhanh tìm cả "
     "trong cột Mô tả\n"
     "- Chỉ 1 dòng trong kết quả"),

    (3, "Tìm nhanh không phân biệt chữ hoa chữ thường", "P1", FIX,
     "1. Gõ \"KHÁCH\" (viết hoa) vào ô tìm nhanh\n2. Bấm Tìm kiếm",
     "Từ khóa: KHÁCH",
     "- Kết quả giống hệt khi gõ chữ thường: 3 lý do có chữ khách"),

    (4, "Tìm nhanh có khoảng trắng thừa hai đầu", "P2", FIX,
     "1. Gõ \"   khách   \" (có khoảng trắng trước và sau) vào ô tìm nhanh\n2. Bấm Tìm kiếm",
     "Từ khóa: (khoảng trắng)khách(khoảng trắng)",
     "- Vẫn ra đúng 3 lý do có chữ khách, khoảng trắng thừa không làm mất kết quả"),

    (5, "Tìm nhanh với ký tự phần trăm và gạch dưới", "P0",
     FIX + "\nDanh mục KHÔNG có lý do nào chứa ký tự phần trăm.",
     "1. Gõ ký tự phần trăm vào ô tìm nhanh\n2. Bấm Tìm kiếm\n3. Xóa đi, gõ ký tự gạch dưới rồi Tìm kiếm",
     "Từ khóa lần 1: % · Từ khóa lần 2: _",
     "- ⚠️ Cả hai lần đều cho kết quả trống, hệ thống hiểu đây là ký tự bình thường chứ không phải ký tự "
     "đại diện tìm mọi thứ\n"
     "- Không được trả về toàn bộ 12 dòng"),

    (6, "Gõ ô tìm nhanh nhưng chưa bấm Tìm kiếm", "P0", FIX,
     "1. Gõ \"khách\" vào ô tìm nhanh\n2. KHÔNG bấm gì thêm, chờ 5 giây\n3. Quan sát bảng",
     "Từ khóa: khách",
     "- ⚠️ Bảng vẫn giữ nguyên 12 dòng — ô tìm nhanh chỉ áp dụng khi bấm Tìm kiếm hoặc nhấn Enter"),

    (7, "Nhấn Enter trong ô tìm nhanh", "P1", FIX,
     "1. Gõ \"khách\" vào ô tìm nhanh\n2. Nhấn phím Enter",
     "Từ khóa: khách",
     "- Danh sách lọc ngay giống như bấm nút Tìm kiếm, còn 3 dòng\n- Trang không bị tải lại từ đầu"),

    (8, "Nút xóa nhanh trong ô tìm kiếm", "P2", FIX,
     "1. Gõ \"khách\" vào ô tìm nhanh và bấm Tìm kiếm\n2. Bấm dấu x nhỏ bên phải trong ô tìm nhanh",
     "Từ khóa: khách",
     "- Ô tìm nhanh trống lại\n- Danh sách trở về đủ 12 dòng"),

    (9, "Lọc theo trạng thái Hoạt động", "P0", FIX,
     "1. Mở Tìm kiếm nâng cao\n2. Chọn Trạng thái = Hoạt động\n3. Quan sát bảng ngay, không bấm gì thêm",
     "Trạng thái: Hoạt động",
     "- ⚠️ Danh sách TỰ lọc lại ngay khi chọn, không cần bấm Tìm kiếm\n"
     "- Còn 11 dòng, tất cả đều mang thẻ Hoạt động\n- Không còn dòng \"Hủy do phòng họp bị trùng\""),

    (10, "Lọc theo trạng thái Khóa", "P0", FIX,
     "1. Chọn Trạng thái = Khóa ở bộ lọc nâng cao",
     "Trạng thái: Khóa",
     "- Chỉ còn 1 dòng \"Hủy do phòng họp bị trùng\" với thẻ Khóa\n- Dòng dưới bảng: Hiển thị 1–1 / 1 lý do"),

    (11, "Bỏ chọn trạng thái", "P1", FIX + "\nĐang lọc Trạng thái = Khóa.",
     "1. Bấm dấu x trong ô Trạng thái để bỏ chọn",
     "—",
     "- Ô Trạng thái trống lại\n- Danh sách trở về đủ 12 dòng ngay lập tức"),

    (12, "Lọc theo người tạo", "P0",
     FIX + "\nTài khoản Phan Văn Khôi tạo 1 lý do; Trần Thị Thu tạo 1 lý do; Đặng Văn Nam tạo 10 lý do.",
     "1. Mở Tìm kiếm nâng cao\n2. Chọn Người tạo = Phan Văn Khôi",
     "Người tạo: Phan Văn Khôi",
     "- Chỉ còn 1 dòng \"Hủy do thời tiết xấu\", cột Người tạo ghi Phan Văn Khôi\n"
     "- Dòng dưới bảng: Hiển thị 1–1 / 1 lý do"),

    (13, "Lọc theo người cập nhật gần nhất", "P1",
     FIX + "\nTài khoản Trần Thị Thu vừa sửa mô tả của 2 lý do.",
     "1. Chọn Người cập nhật gần nhất = Trần Thị Thu",
     "Người cập nhật gần nhất: Trần Thị Thu",
     "- Chỉ còn 2 dòng, cột Cập nhật của cả hai đều ghi \"bởi Trần Thị Thu\"\n"
     "- ⚠️ Người tạo của 2 dòng đó có thể là người khác — đây là bộ lọc theo người sửa cuối cùng"),

    (14, "Lọc từ một mốc ngày cập nhật", "P1",
     FIX + "\n5 lý do có ngày cập nhật 12/09/2026, 7 lý do cập nhật 05/09/2026.",
     "1. Chọn Cập nhật từ = 10/09/2026\n2. Để trống ô Đến",
     "Cập nhật từ: 10/09/2026",
     "- Còn đúng 5 dòng, cột Cập nhật của tất cả đều từ 10/09/2026 trở về sau"),

    (15, "Lọc đến một mốc ngày cập nhật", "P1",
     FIX + "\n5 lý do có ngày cập nhật 12/09/2026, 7 lý do cập nhật 05/09/2026.",
     "1. Để trống ô Cập nhật từ\n2. Chọn Đến = 09/09/2026",
     "Đến: 09/09/2026",
     "- Còn đúng 7 dòng, tất cả có ngày cập nhật từ 09/09/2026 trở về trước"),

    (16, "Lọc khoảng ngày cập nhật lấy trọn cả hai đầu mốc", "P0",
     FIX + "\nCó 1 lý do cập nhật lúc 05/09/2026 08:05 và 1 lý do cập nhật lúc 12/09/2026 23:40.",
     "1. Chọn Cập nhật từ = 05/09/2026\n2. Chọn Đến = 12/09/2026\n3. Kiểm tra 2 dòng ở hai đầu mốc",
     "Cập nhật từ: 05/09/2026 · Đến: 12/09/2026",
     "- ⚠️ Cả dòng cập nhật lúc 05/09/2026 08:05 và dòng cập nhật lúc 12/09/2026 23:40 đều nằm trong kết "
     "quả (bao gồm trọn hai ngày đầu và cuối, không cắt theo giờ)"),

    (17, "Chọn khoảng ngày ngược (từ lớn hơn đến)", "P1", FIX,
     "1. Chọn Cập nhật từ = 20/09/2026\n2. Chọn Đến = 01/09/2026",
     "Cập nhật từ: 20/09/2026 · Đến: 01/09/2026",
     "- Bảng trống, hiện dòng \"Không có dữ liệu phù hợp bộ lọc.\"\n- Không báo lỗi đỏ, không treo trang"),

    (18, "Gõ tay ngày có số ngày lớn hơn 12", "P0", FIX,
     "1. Gõ tay vào ô Cập nhật từ giá trị 13/09/2026\n2. Gõ tay vào ô Đến giá trị 25/09/2026\n"
     "3. Quan sát kết quả lọc",
     "Cập nhật từ: 13/09/2026 · Đến: 25/09/2026",
     "- ⚠️ Hệ thống hiểu đúng là ngày 13 và ngày 25 tháng 9, lọc ra đúng các dòng trong khoảng đó\n"
     "- Không báo lỗi định dạng ngày, không trả về kết quả trống bất thường"),

    (19, "Kết hợp nhiều điều kiện lọc cùng lúc", "P0",
     FIX + "\nLý do \"Hủy do khách không gặp\" do Đặng Văn Nam tạo, đang Hoạt động.",
     "1. Gõ \"khách\" vào ô tìm nhanh và bấm Tìm kiếm\n2. Chọn Trạng thái = Hoạt động\n"
     "3. Chọn Người tạo = Đặng Văn Nam",
     "Từ khóa: khách · Trạng thái: Hoạt động · Người tạo: Đặng Văn Nam",
     "- Các điều kiện cộng dồn với nhau (thỏa TẤT CẢ mới hiện), không phải cộng gộp kết quả\n"
     "- Kết quả chỉ còn các lý do vừa chứa chữ khách, vừa Hoạt động, vừa do Đặng Văn Nam tạo"),

    (20, "Đổi bộ lọc khi đang đứng ở trang 2", "P1",
     FIX + "\nĐang ở trang 2 của danh sách 12 dòng.",
     "1. Bấm sang trang 2\n2. Chọn Trạng thái = Hoạt động\n3. Quan sát số trang đang đứng",
     "Trạng thái: Hoạt động",
     "- ⚠️ Danh sách nhảy về trang 1 của kết quả mới, không giữ trang 2 cũ\n"
     "- Không hiện bảng trống do đứng ở trang không còn tồn tại"),

    (21, "Làm mới sau khi dùng nhiều điều kiện lọc", "P1",
     FIX + "\nĐang lọc: từ khóa khách + Trạng thái Hoạt động + Người tạo Đặng Văn Nam + khoảng ngày.",
     "1. Bấm nút Làm mới\n2. Kiểm tra lần lượt từng ô lọc và bảng",
     "—",
     "- Tất cả 6 ô lọc trở về trống\n- Bảng đủ 12 dòng, về trang 1, số dòng mỗi trang giữ nguyên 10"),
]

S3 = [
    (1, "Số thứ tự chạy liên tục qua các trang", "P0",
     FIX + "\nDanh sách 12 lý do, 10 dòng mỗi trang.",
     "1. Xem cột STT ở trang 1\n2. Bấm sang trang 2 và xem cột STT",
     "—",
     "- Trang 1 đánh số 1 đến 10\n- ⚠️ Trang 2 bắt đầu từ 11, KHÔNG quay lại 1"),

    (2, "Sắp xếp cột Cập nhật tăng dần", "P0", FIX,
     "1. Bấm vào tiêu đề cột Cập nhật lần thứ nhất\n2. Đọc cột Cập nhật từ trên xuống",
     "—",
     "- Mũi tên sắp xếp đổi chiều\n- Dòng có ngày cập nhật cũ nhất lên đầu, mới nhất xuống cuối"),

    (3, "Sắp xếp cột Cập nhật giảm dần", "P0", FIX,
     "1. Bấm vào tiêu đề cột Cập nhật lần thứ hai",
     "—",
     "- Dòng có ngày cập nhật mới nhất lên đầu\n- Số dòng tổng không đổi (vẫn 12)"),

    (4, "Sắp xếp giữ nguyên điều kiện lọc đang có", "P1",
     FIX + "\nĐang lọc Trạng thái = Hoạt động, còn 11 dòng.",
     "1. Bấm sắp xếp cột Cập nhật\n2. Kiểm tra ô lọc Trạng thái và số dòng",
     "—",
     "- Ô Trạng thái vẫn là Hoạt động\n- Vẫn đúng 11 dòng, chỉ thay đổi thứ tự"),

    (5, "Sắp xếp xong quay về trang 1", "P1", FIX + "\nĐang đứng ở trang 2.",
     "1. Bấm sang trang 2\n2. Bấm sắp xếp cột Cập nhật",
     "—",
     "- Danh sách nhảy về trang 1 của kết quả vừa sắp xếp"),

    (6, "Các cột khác không sắp xếp được", "P1", FIX,
     "1. Lần lượt bấm vào tiêu đề các cột: Lý do hủy cuộc họp, Mô tả, Người tạo, Ngày tạo, Trạng thái",
     "—",
     "- ⚠️ Không cột nào trong số đó đổi thứ tự dữ liệu, không có mũi tên sắp xếp\n"
     "- Không báo lỗi khi bấm"),

    (7, "Đổi số dòng mỗi trang", "P0", FIX,
     "1. Chọn số dòng mỗi trang = 5\n2. Đếm số dòng và số trang\n3. Chọn tiếp 50",
     "Số dòng mỗi trang: 5 rồi 50",
     "- Với 5: trang 1 có 5 dòng, thanh phân trang hiện 3 trang, dòng dưới bảng \"Hiển thị 1–5 / 12 lý do\"\n"
     "- Với 50: cả 12 dòng hiện trên một trang, chỉ còn 1 trang\n- Ô chọn có đúng 4 mức: 5 · 10 · 20 · 50"),

    (8, "Đổi số dòng mỗi trang khi đang ở trang cuối", "P1", FIX + "\nĐang ở trang 2 với 10 dòng mỗi trang.",
     "1. Bấm sang trang 2\n2. Đổi số dòng mỗi trang thành 50",
     "Số dòng mỗi trang: 50",
     "- Quay về trang 1, hiện đủ 12 dòng, không hiện bảng trống"),

    (9, "Chuyển trang bằng nút số và nút mũi tên", "P1", FIX,
     "1. Bấm nút số 2\n2. Bấm mũi tên lùi về trang trước\n3. Bấm mũi tên tiến tới trang sau",
     "—",
     "- Mỗi lần bấm, bảng đổi đúng nhóm dòng của trang đó, số trang đang chọn được tô đậm\n"
     "- Ở trang 1 nút lùi bị mờ, ở trang cuối nút tiến bị mờ"),

    (10, "Dòng đếm số bản ghi dưới bảng", "P0", FIX,
     "1. Xem dòng đếm ở trang 1\n2. Bấm sang trang 2 và xem lại\n3. Lọc Trạng thái = Khóa và xem lại",
     "—",
     "- Trang 1: Hiển thị 1–10 / 12 lý do\n- Trang 2: Hiển thị 11–12 / 12 lý do\n"
     "- ⚠️ Khi lọc còn 1 dòng: Hiển thị 1–1 / 1 lý do — tổng đếm theo bộ lọc, không phải tổng danh mục"),

    (11, "Mô tả dài hiển thị xuống dòng, không tràn bảng", "P1",
     FIX + "\nMột lý do có mô tả dài khoảng 380 ký tự, gồm 3 đoạn xuống dòng.",
     "1. Tìm dòng có mô tả dài\n2. Quan sát ô Mô tả",
     "—",
     "- Nội dung tự xuống dòng trong ô, giữ đúng 3 đoạn như khi nhập\n"
     "- Không đè sang cột bên cạnh, không phải cuộn ngang mới đọc được"),

    (12, "Cột Cập nhật hiện đủ ngày giờ và người cập nhật", "P0",
     FIX + "\nLý do \"Hủy do thời tiết xấu\" vừa được Trần Thị Thu sửa lúc 12/09/2026 14:25.",
     "1. Xem ô Cập nhật của dòng đó",
     "—",
     "- Dòng trên hiện 12/09/2026 14:25 (có đủ giờ và phút, không chỉ ngày)\n"
     "- Dòng dưới hiện \"bởi Trần Thị Thu\""),

    (13, "Thẻ trạng thái đúng màu và đúng chữ", "P0", FIX,
     "1. Xem cột Trạng thái của một lý do Hoạt động và một lý do Khóa",
     "—",
     "- Lý do Hoạt động: thẻ xanh, biểu tượng dấu tích, chữ \"Hoạt động\"\n"
     "- Lý do Khóa: thẻ xám, biểu tượng ổ khóa, chữ \"Khóa\"\n"
     "- ⚠️ Không hiện số 1 hay số 2 thay cho chữ"),
]

S4 = [
    (1, "Mở cửa sổ Thêm mới", "P0", FIX,
     "1. Bấm nút Tạo mới\n2. Quan sát tiêu đề cửa sổ, các ô nhập và các nút ở chân cửa sổ",
     "—",
     "- Tiêu đề cửa sổ: Thêm lý do hủy cuộc họp\n"
     "- Ô \"Lý do hủy cuộc họp\" trống, có dấu sao đỏ bắt buộc, gợi ý \"VD: Hủy do khách dời lịch / Hủy "
     "do khách không gặp / ...\"\n"
     "- Ô Trạng thái điền sẵn \"Hoạt động\"\n- Ô Mô tả trống\n"
     "- Chân cửa sổ có 3 nút: Lưu · Lưu và tiếp tục · Đóng"),

    (2, "Thêm mới đầy đủ thông tin hợp lệ", "P0", FIX,
     "1. Bấm Tạo mới\n2. Nhập Lý do hủy cuộc họp\n3. Nhập Mô tả\n4. Để Trạng thái là Hoạt động\n"
     "5. Bấm Lưu\n6. Quan sát danh sách",
     "Lý do hủy cuộc họp: Hủy do khách đổi người dự\nMô tả: Khách báo đổi người tham dự, dời sang buổi khác",
     "- Hiện thông báo xanh \"Thêm mới thành công\", cửa sổ tự đóng\n"
     "- Dòng mới xuất hiện ở ĐẦU danh sách với thẻ Hoạt động\n"
     "- Cột Người tạo là người đang đăng nhập, Ngày tạo là hôm nay\n- Tổng số lý do tăng lên 13"),

    (3, "Thêm mới chỉ nhập tên, bỏ trống mô tả", "P1", FIX,
     "1. Bấm Tạo mới\n2. Chỉ nhập ô Lý do hủy cuộc họp\n3. Bấm Lưu",
     "Lý do hủy cuộc họp: Hủy do hệ thống bảo trì",
     "- Lưu thành công, không báo lỗi ở ô Mô tả\n- Dòng mới có ô Mô tả trống trong danh sách"),

    (4, "Thêm mới với trạng thái Khóa", "P0", FIX,
     "1. Bấm Tạo mới\n2. Nhập tên\n3. Đổi Trạng thái sang Khóa\n4. Bấm Lưu\n"
     "5. Tìm dòng vừa tạo trong danh sách",
     "Lý do hủy cuộc họp: Hủy do lịch trùng phòng họp lớn · Trạng thái: Khóa",
     "- Lưu thành công\n- ⚠️ Dòng mới mang thẻ Khóa ngay, nút Sửa của dòng đó bị mờ\n"
     "- ⚠️ Lý do này KHÔNG xuất hiện trong ô chọn lý do ở cửa sổ hủy cuộc họp"),

    (5, "Bỏ trống tên khi thêm mới", "P0", FIX,
     "1. Bấm Tạo mới\n2. Để trống ô Lý do hủy cuộc họp\n3. Bấm Lưu",
     "Lý do hủy cuộc họp: (để trống)",
     "- ⚠️ Cửa sổ KHÔNG đóng\n"
     "- Ô Lý do hủy cuộc họp viền đỏ, ngay dưới hiện chữ đỏ \"Vui lòng nhập lý do hủy cuộc họp\"\n"
     "- Có thông báo \"Bạn chưa nhập đầy đủ thông tin\"\n- Danh mục không phát sinh dòng mới"),

    (6, "Thêm mới trùng tên đã có", "P0", FIX,
     "1. Bấm Tạo mới\n2. Nhập đúng tên một lý do đã có\n3. Bấm Lưu",
     "Lý do hủy cuộc họp: Hủy do khách dời lịch",
     "- Cửa sổ không đóng, ô tên viền đỏ kèm chữ đỏ \"Lý do hủy cuộc họp đã tồn tại trong hệ thống\"\n"
     "- Tổng số lý do không đổi"),

    (7, "Thêm mới trùng tên nhưng khác chữ hoa chữ thường", "P1", FIX,
     "1. Bấm Tạo mới\n2. Nhập \"HỦY DO KHÁCH DỜI LỊCH\" (viết hoa toàn bộ)\n3. Bấm Lưu",
     "Lý do hủy cuộc họp: HỦY DO KHÁCH DỜI LỊCH",
     "- ⚠️ Vẫn bị chặn với thông báo \"Lý do hủy cuộc họp đã tồn tại trong hệ thống\" — tên là duy nhất "
     "không phân biệt chữ hoa chữ thường"),

    (8, "Tên dài đúng 255 ký tự và dài hơn 255 ký tự", "P0", FIX,
     "1. Bấm Tạo mới, dán chuỗi đúng 255 ký tự vào ô tên, bấm Lưu\n"
     "2. Bấm Tạo mới lần nữa, dán chuỗi 256 ký tự, bấm Lưu",
     "Lần 1: chuỗi 255 ký tự · Lần 2: chuỗi 256 ký tự",
     "- Lần 1 lưu thành công, danh sách hiện đủ nội dung dài, ô xuống dòng gọn\n"
     "- ⚠️ Lần 2 bị chặn: ô tên viền đỏ kèm chữ \"Lý do hủy cuộc họp tối đa 255 ký tự\", cửa sổ không đóng"),

    (9, "Ô Mô tả chặn nhập quá 1000 ký tự", "P1", FIX,
     "1. Bấm Tạo mới\n2. Dán một đoạn dài 2000 ký tự vào ô Mô tả\n3. Đếm số ký tự nhận được\n4. Bấm Lưu",
     "Mô tả: đoạn 2000 ký tự",
     "- ⚠️ Ô Mô tả chỉ nhận đúng 1000 ký tự đầu, phần còn lại không vào được\n"
     "- Bấm Lưu thành công, không báo lỗi độ dài"),

    (10, "Nút Lưu và tiếp tục", "P0", FIX,
     "1. Bấm Tạo mới\n2. Nhập tên và mô tả\n3. Bấm \"Lưu và tiếp tục\"\n4. Quan sát cửa sổ\n"
     "5. Nhập tiếp lý do thứ hai và bấm Lưu",
     "Lý do 1: Hủy do mất điện toàn tòa nhà\nLý do 2: Hủy do khách yêu cầu họp trực tuyến",
     "- Sau bước 3: hiện \"Thêm mới thành công\", ⚠️ cửa sổ VẪN MỞ, các ô trở về trống, Trạng thái quay "
     "lại Hoạt động\n"
     "- Sau bước 5: cửa sổ đóng, danh sách có đủ cả 2 lý do vừa thêm"),

    (11, "Cửa sổ Sửa không có nút Lưu và tiếp tục", "P1", FIX,
     "1. Bấm nút Sửa ở một dòng đang Hoạt động\n2. Quan sát chân cửa sổ",
     "—",
     "- ⚠️ Chỉ có 2 nút: Lưu và Đóng, không có \"Lưu và tiếp tục\""),

    (12, "Bấm Đóng khi đã nhập dở", "P1", FIX,
     "1. Bấm Tạo mới\n2. Nhập tên và mô tả nhưng chưa lưu\n3. Bấm nút Đóng\n4. Bấm Tạo mới lần nữa",
     "Lý do hủy cuộc họp: Nhập dở rồi bỏ",
     "- Cửa sổ đóng, danh sách không có dòng \"Nhập dở rồi bỏ\"\n"
     "- ⚠️ Mở lại Tạo mới thì các ô đều trống sạch, Trạng thái về Hoạt động — không còn dữ liệu nhập dở"),

    (13, "Đóng cửa sổ bằng dấu x ở góc trên", "P2", FIX,
     "1. Bấm Tạo mới\n2. Nhập tên\n3. Bấm dấu x ở góc trên bên phải cửa sổ",
     "—",
     "- Cửa sổ đóng, không lưu gì, danh sách giữ nguyên số dòng"),

    (14, "Bấm Lưu hai lần liên tiếp thật nhanh", "P0", FIX,
     "1. Bấm Tạo mới, nhập tên hợp lệ\n2. Bấm nút Lưu 2 lần liên tiếp thật nhanh\n"
     "3. Tìm tên vừa nhập trong danh sách",
     "Lý do hủy cuộc họp: Hủy do trùng lịch lãnh đạo",
     "- ⚠️ Chỉ tạo ra ĐÚNG 1 dòng, không tạo 2 dòng trùng tên\n"
     "- Nút Lưu bị khóa tạm trong lúc đang lưu, chỉ hiện 1 thông báo thành công"),

    (15, "Mở cửa sổ Sửa của một lý do đang Hoạt động", "P0",
     FIX + "\nLý do \"Hủy do thời tiết xấu\" có mô tả \"Mưa bão, đường ngập, không di chuyển được\".",
     "1. Bấm nút Sửa (biểu tượng bút chì) ở dòng \"Hủy do thời tiết xấu\"\n2. Quan sát nội dung cửa sổ",
     "—",
     "- Tiêu đề: Sửa lý do hủy cuộc họp\n"
     "- Ô tên điền sẵn \"Hủy do thời tiết xấu\", ô Mô tả điền sẵn đúng nội dung cũ, Trạng thái là Hoạt động\n"
     "- Các ô đều sửa được"),

    (16, "Sửa tên của một lý do", "P0", FIX,
     "1. Bấm Sửa ở dòng \"Hủy do thời tiết xấu\"\n2. Đổi tên\n3. Bấm Lưu\n"
     "4. Quan sát dòng đó trong danh sách",
     "Tên mới: Hủy do thời tiết xấu, mưa bão",
     "- Hiện \"Cập nhật thành công\", cửa sổ đóng\n- Dòng trong danh sách đổi sang tên mới\n"
     "- Cột Cập nhật đổi thành thời điểm hiện tại, dòng dưới ghi \"bởi + tên người đang đăng nhập\"\n"
     "- Ngày tạo và Người tạo KHÔNG đổi"),

    (17, "Sửa mà giữ nguyên tên cũ của chính nó", "P0", FIX,
     "1. Bấm Sửa ở dòng \"Hủy do khách dời lịch\"\n2. Không đụng ô tên, chỉ đổi Mô tả\n3. Bấm Lưu",
     "Mô tả mới: Khách chủ động đề nghị dời sang ngày khác",
     "- ⚠️ KHÔNG báo trùng tên — tên cũ của chính bản ghi đang sửa không bị coi là trùng\n"
     "- Cập nhật thành công, mô tả mới hiện trong danh sách"),

    (18, "Sửa thành tên của một lý do khác đã có", "P1", FIX,
     "1. Bấm Sửa ở dòng \"Hủy do thời tiết xấu\"\n2. Đổi tên thành \"Hủy do khách không gặp\"\n3. Bấm Lưu",
     "Tên mới: Hủy do khách không gặp",
     "- Bị chặn, ô tên viền đỏ kèm chữ \"Lý do hủy cuộc họp đã tồn tại trong hệ thống\"\n"
     "- Cửa sổ không đóng, danh sách không đổi"),

    (19, "Đổi trạng thái sang Khóa ngay trong cửa sổ Sửa", "P1", FIX,
     "1. Bấm Sửa ở dòng \"Hủy do mình bận đột xuất\"\n2. Đổi ô Trạng thái sang Khóa\n3. Bấm Lưu",
     "Trạng thái: Khóa",
     "- Cập nhật thành công, dòng chuyển sang thẻ Khóa\n"
     "- ⚠️ Sau khi lưu, nút Sửa của chính dòng đó bị mờ (muốn sửa tiếp phải Mở khóa)"),

    (20, "Nút Sửa bị mờ với lý do đang Khóa", "P0",
     FIX + "\nLý do \"Hủy do phòng họp bị trùng\" đang Khóa.",
     "1. Tìm dòng \"Hủy do phòng họp bị trùng\"\n2. Rê chuột vào nút Sửa và thử bấm",
     "—",
     "- ⚠️ Nút Sửa ở trạng thái mờ, bấm không mở được cửa sổ nào\n"
     "- Nút Xem vẫn bấm được bình thường"),

    (21, "Xem chi tiết một lý do", "P0", FIX,
     "1. Bấm nút Xem (biểu tượng con mắt) ở dòng bất kỳ\n2. Thử gõ vào ô tên và ô mô tả\n"
     "3. Quan sát chân cửa sổ",
     "—",
     "- Tiêu đề: Xem lý do hủy cuộc họp\n- Các ô hiện đúng dữ liệu của dòng đã chọn\n"
     "- ⚠️ Mọi ô đều ở chế độ chỉ đọc, không gõ được, ô Trạng thái không đổi được\n"
     "- Chân cửa sổ chỉ có nút Đóng, không có nút Lưu"),

    (22, "Xem chi tiết một lý do đang Khóa", "P1",
     FIX + "\nLý do \"Hủy do phòng họp bị trùng\" đang Khóa.",
     "1. Bấm nút Xem ở dòng đang Khóa",
     "—",
     "- ⚠️ Vẫn mở xem được bình thường (khóa chỉ chặn sửa, không chặn xem)\n"
     "- Ô Trạng thái hiện \"Khóa\""),

    (23, "Xem chi tiết bằng tài khoản chỉ có quyền xem", "P1", ACC + "\n" + FIX,
     "1. Đăng nhập bằng tài khoản B\n2. Mở màn danh mục\n3. Bấm nút Xem ở một dòng",
     "Tài khoản: B",
     "- Mở được cửa sổ xem, dữ liệu hiển thị đúng, chỉ có nút Đóng\n- Không có nút Lưu, không sửa được ô nào"),

    (24, "Lưu thất bại do mất kết nối", "P2", FIX,
     "1. Bấm Tạo mới, nhập tên hợp lệ\n2. Ngắt mạng của máy đang test\n3. Bấm Lưu",
     "Lý do hủy cuộc họp: Hủy do mất kết nối thử nghiệm",
     "- Hiện thông báo lỗi đỏ \"Thêm mới thất bại\"\n"
     "- ⚠️ Cửa sổ vẫn mở và GIỮ NGUYÊN nội dung đã nhập, không bắt gõ lại từ đầu\n"
     "- Nối mạng lại rồi bấm Lưu thì lưu được"),
]

S5 = [
    (1, "Nút khóa hiện đúng chỗ và đúng chú giải", "P0", FIX,
     "1. Mở màn danh mục bằng tài khoản có quyền quản lý\n"
     "2. Rê chuột vào nút bên cạnh thẻ trạng thái của một dòng Hoạt động\n"
     "3. Rê chuột vào nút tương ứng của dòng đang Khóa",
     "—",
     "- Dòng Hoạt động: nút biểu tượng ổ khóa đóng, chú giải \"Khóa lý do\"\n"
     "- Dòng đang Khóa: nút biểu tượng ổ khóa mở, chú giải \"Mở khóa lý do\""),

    (2, "Cửa sổ xác nhận khi bấm khóa", "P0", FIX,
     "1. Bấm nút khóa ở dòng \"Hủy do khách dời lịch\"\n2. Đọc nội dung cửa sổ xác nhận",
     "—",
     "- Tiêu đề: Xác nhận khóa\n"
     "- Nội dung: Bạn có chắc muốn khóa lý do hủy cuộc họp 'Hủy do khách dời lịch'?\n"
     "- Nút xác nhận ghi chữ \"Khóa\", màu đỏ, có biểu tượng ổ khóa; bên cạnh là nút Hủy"),

    (3, "Xác nhận khóa thành công", "P0", FIX,
     "1. Bấm nút khóa ở dòng \"Hủy do khách dời lịch\"\n2. Bấm nút Khóa trong cửa sổ xác nhận\n"
     "3. Quan sát dòng đó",
     "—",
     "- Hiện thông báo xanh \"Khóa thành công\"\n- Thẻ trạng thái đổi sang Khóa (xám, ổ khóa)\n"
     "- Nút Sửa của dòng đó chuyển sang mờ\n- Nút bên cạnh thẻ đổi thành biểu tượng mở khóa"),

    (4, "Bấm Hủy ở cửa sổ xác nhận khóa", "P1", FIX,
     "1. Bấm nút khóa ở một dòng Hoạt động\n2. Bấm nút Hủy trong cửa sổ xác nhận",
     "—",
     "- Cửa sổ đóng, không có thông báo nào\n- Dòng giữ nguyên trạng thái Hoạt động"),

    (5, "Cửa sổ xác nhận khi bấm mở khóa", "P1",
     FIX + "\nLý do \"Hủy do phòng họp bị trùng\" đang Khóa.",
     "1. Bấm nút mở khóa ở dòng đang Khóa\n2. Đọc nội dung và màu nút trong cửa sổ xác nhận",
     "—",
     "- Tiêu đề: Xác nhận mở khóa\n"
     "- Nội dung: Bạn có chắc muốn mở khóa lý do hủy cuộc họp 'Hủy do phòng họp bị trùng'?\n"
     "- ⚠️ Nút xác nhận ghi \"Mở khóa\" và KHÔNG tô đỏ (mở khóa là thao tác khôi phục, không phải phá hủy)"),

    (6, "Xác nhận mở khóa thành công", "P0",
     FIX + "\nLý do \"Hủy do phòng họp bị trùng\" đang Khóa.",
     "1. Bấm nút mở khóa ở dòng đó\n2. Bấm nút Mở khóa trong cửa sổ xác nhận",
     "—",
     "- Hiện thông báo \"Mở khóa thành công\"\n- Thẻ đổi sang Hoạt động (xanh, dấu tích)\n"
     "- Nút Sửa của dòng đó dùng lại được bình thường"),

    (7, "Khóa được cả lý do đang có cuộc họp dùng", "P0",
     FIX + "\nLý do \"Hủy do khách không gặp\" đang được 4 cuộc họp dùng, nút Xóa đang mờ.",
     "1. Bấm nút khóa ở dòng \"Hủy do khách không gặp\"\n2. Xác nhận khóa",
     "—",
     "- ⚠️ Khóa thành công dù lý do đang được 4 cuộc họp dùng — đây chính là cách thay thế cho việc xóa\n"
     "- Nút Xóa của dòng vẫn mờ như trước"),

    (8, "Lý do vừa khóa biến mất khỏi ô chọn khi hủy cuộc họp", "P0",
     FIX + "\nVừa khóa lý do \"Hủy do khách dời lịch\". Có 1 cuộc họp chưa tới giờ bắt đầu để thử hủy.",
     "1. Mở màn Cuộc họp, mở một cuộc họp chưa tới giờ bắt đầu\n2. Bấm nút Hủy\n"
     "3. Mở ô chọn Lý do hủy và đọc danh sách",
     "—",
     "- ⚠️ Không còn dòng \"Hủy do khách dời lịch\" trong ô chọn\n"
     "- Các lý do Hoạt động khác vẫn liệt kê đầy đủ"),

    (9, "Cuộc họp đã hủy trước đó vẫn hiện tên lý do vừa bị khóa", "P0",
     FIX + "\nCuộc họp \"Khảo sát nhà máy A\" đã hủy trước đó bằng lý do \"Hủy do khách dời lịch\"; lý do "
     "này vừa bị khóa.",
     "1. Mở màn Cuộc họp\n2. Mở cuộc họp \"Khảo sát nhà máy A\"\n3. Đọc ô Lý do hủy",
     "—",
     "- ⚠️ Vẫn hiện đúng \"Hủy do khách dời lịch\" kèm ghi chú kèm theo (nếu có)\n"
     "- Không hiện ô trống, không hiện dấu gạch ngang, không báo lỗi"),

    (10, "Hai người cùng khóa một dòng", "P1",
     FIX + "\nMở màn danh mục trên 2 trình duyệt bằng 2 tài khoản đều có quyền quản lý.",
     "1. Cả 2 cùng mở màn, cùng nhìn thấy dòng \"Hủy do mình bận đột xuất\" đang Hoạt động\n"
     "2. Người thứ nhất bấm khóa và xác nhận\n"
     "3. Người thứ hai (chưa tải lại trang) cũng bấm khóa và xác nhận",
     "—",
     "- Người thứ nhất: Khóa thành công\n"
     "- ⚠️ Người thứ hai nhận thông báo \"Dữ liệu đã thay đổi, vui lòng tải lại\", không ghi đè, không báo "
     "thành công nhầm"),

    (11, "Khóa xong vẫn giữ nguyên bộ lọc và trang đang xem", "P1",
     FIX + "\nĐang lọc Trạng thái = Hoạt động và đứng ở trang 2.",
     "1. Bấm khóa một dòng ở trang 2 và xác nhận\n2. Quan sát bộ lọc và số trang",
     "—",
     "- Sau khi khóa, ô lọc Trạng thái vẫn là Hoạt động, vẫn đứng ở trang 2\n"
     "- Dòng vừa khóa rời khỏi kết quả lọc vì không còn là Hoạt động"),
]

S6 = [
    (1, "Nút Xóa hiển thị đúng với lý do chưa được dùng", "P0",
     FIX + "\nLý do \"Hủy do thiếu tài liệu chuẩn bị\" chưa cuộc họp nào dùng.",
     "1. Tìm dòng đó\n2. Rê chuột vào nút Xóa",
     "—",
     "- Nút Xóa màu đỏ, bấm được, chú giải hiện chữ \"Xóa\""),

    (2, "Cửa sổ xác nhận xóa", "P0", FIX,
     "1. Bấm nút Xóa ở dòng \"Hủy do thiếu tài liệu chuẩn bị\"\n2. Đọc nội dung cửa sổ",
     "—",
     "- Tiêu đề: Xác nhận xóa\n"
     "- Nội dung: Bạn có chắc muốn xóa lý do hủy cuộc họp 'Hủy do thiếu tài liệu chuẩn bị'?\n"
     "- Nút xác nhận ghi \"Xóa\", màu đỏ, kèm biểu tượng thùng rác; bên cạnh là nút Hủy"),

    (3, "Xóa thành công một lý do chưa được dùng", "P0",
     FIX + "\nDanh mục đang có 12 lý do.",
     "1. Bấm Xóa ở dòng \"Hủy do thiếu tài liệu chuẩn bị\"\n2. Bấm nút Xóa trong cửa sổ xác nhận\n"
     "3. Đếm lại số dòng",
     "—",
     "- Hiện thông báo \"Xóa thành công\"\n- Dòng biến mất khỏi danh sách\n"
     "- Dòng đếm dưới bảng đổi thành tổng 11 lý do"),

    (4, "Bấm Hủy ở cửa sổ xác nhận xóa", "P1", FIX,
     "1. Bấm Xóa ở một dòng\n2. Bấm nút Hủy trong cửa sổ xác nhận",
     "—",
     "- Cửa sổ đóng, dòng vẫn còn nguyên, tổng số lý do không đổi"),

    (5, "Nút Xóa bị mờ với lý do đang được cuộc họp dùng", "P0",
     FIX + "\nLý do \"Hủy do khách hẹn lại tuần sau\" đang được 3 cuộc họp dùng.",
     "1. Tìm dòng đó\n2. Rê chuột vào nút Xóa và thử bấm",
     "—",
     "- ⚠️ Nút Xóa xám mờ, bấm không mở cửa sổ xác nhận\n"
     "- Chú giải hiện đúng câu: Lý do đang được dùng ở cuộc họp, không xóa được. Bạn có thể Khóa lý do này."),

    (6, "Ép xóa lý do đang được dùng bằng cách bỏ qua giao diện", "P0",
     FIX + "\nDành cho tester kỹ thuật. Lý do \"Hủy do khách hẹn lại tuần sau\" đang được 3 cuộc họp dùng.",
     "1. Đăng nhập bằng tài khoản có quyền quản lý\n"
     "2. Dùng công cụ kiểm thử gọi thẳng chức năng Xóa, trỏ vào lý do đó\n"
     "3. Quay lại màn danh mục kiểm tra",
     "—",
     "- ⚠️ Hệ thống từ chối kèm thông báo: Lý do hủy này đang được dùng ở 3 cuộc họp nên không xóa được. "
     "Bạn có thể Khóa lý do này.\n"
     "- Lý do vẫn còn trong danh mục, 3 cuộc họp kia vẫn hiện đúng tên lý do"),

    (7, "Xóa lý do đang Khóa nhưng chưa cuộc họp nào dùng", "P1",
     FIX + "\nLý do \"Hủy do phòng họp bị trùng\" đang Khóa, 0 cuộc họp dùng.",
     "1. Kiểm tra nút Xóa của dòng đó\n2. Bấm Xóa và xác nhận",
     "—",
     "- ⚠️ Xóa được bình thường: điều kiện xóa phụ thuộc \"đã có cuộc họp dùng hay chưa\", KHÔNG phụ "
     "thuộc trạng thái Khóa hay Hoạt động\n- Hiện \"Xóa thành công\", dòng biến mất"),

    (8, "Xóa bản ghi đã bị người khác xóa trước", "P1",
     FIX + "\nMở màn trên 2 trình duyệt bằng 2 tài khoản có quyền quản lý.",
     "1. Người thứ nhất xóa dòng \"Hủy do hệ thống bảo trì\"\n"
     "2. Người thứ hai (chưa tải lại trang) cũng bấm Xóa ở dòng đó và xác nhận",
     "—",
     "- Người thứ hai nhận thông báo \"Dữ liệu đã thay đổi, vui lòng tải lại\"\n"
     "- Không báo xóa thành công nhầm, trang không treo"),

    (9, "Xóa dòng cuối cùng của trang đang xem", "P1",
     FIX + "\nDanh sách 11 dòng, 10 dòng mỗi trang, trang 2 chỉ còn 1 dòng.",
     "1. Bấm sang trang 2\n2. Xóa dòng duy nhất ở trang 2",
     "—",
     "- Hiện \"Xóa thành công\"\n"
     "- ⚠️ Trang đang xem có thể hiện trống — không phải lỗi; bấm về trang 1 vẫn thấy đủ 10 dòng còn lại, "
     "không báo lỗi đỏ"),

    (10, "Dữ liệu sau khi xóa không còn trong tệp xuất Excel", "P2", FIX,
     "1. Xóa một lý do chưa được dùng\n2. Bấm Xuất Excel\n3. Mở tệp và tìm tên vừa xóa",
     "—",
     "- Tệp Excel không còn dòng vừa xóa, tổng số dòng giảm đúng 1"),
]

S7 = [
    (1, "Nút Xuất Excel hiển thị đúng", "P0", ACC + "\n" + FIX,
     "1. Đăng nhập bằng tài khoản A, mở màn danh mục\n2. Quan sát nút Xuất Excel\n"
     "3. Đăng nhập lại bằng tài khoản B và quan sát",
     "—",
     "- Tài khoản A: nút \"Xuất Excel\" màu xanh lá, biểu tượng tệp Excel, nằm bên phải nút Import Excel\n"
     "- Tài khoản B: không có nút này"),

    (2, "Xuất Excel toàn bộ danh mục", "P0", FIX,
     "1. Không chọn bộ lọc nào\n2. Bấm Xuất Excel\n3. Mở tệp vừa tải",
     "—",
     "- Trình duyệt tải về tệp tên danh_sach_ly_do_huy_cuoc_hop.xlsx\n"
     "- Hiện thông báo \"Xuất Excel thành công\"\n- Tệp mở được, có đúng 12 dòng dữ liệu"),

    (3, "Đầu tệp có logo và tiêu đề", "P0", FIX,
     "1. Mở tệp vừa tải\n2. Xem 2 dòng đầu tiên",
     "—",
     "- Dòng 1 là ảnh tiêu đề công ty, hiển thị đủ, không bị cắt và không đè lên tiêu đề\n"
     "- Dòng 2 là tiêu đề in đậm căn giữa: Danh sách lý do hủy cuộc họp"),

    (4, "Tệp Excel đủ và đúng thứ tự các cột", "P1", FIX,
     "1. Mở tệp vừa tải\n2. Đọc hàng tiêu đề của bảng",
     "—",
     "- Đúng 8 cột theo thứ tự: STT · Lý do hủy cuộc họp · Trạng thái · Mô tả · Người tạo · Người cập "
     "nhật · Ngày tạo · Ngày cập nhật\n"
     "- ⚠️ Thứ tự cột trong tệp KHÁC thứ tự trên màn hình (cột Trạng thái đứng trước Mô tả) — đúng thiết kế"),

    (5, "Cột Trạng thái trong tệp ghi bằng chữ", "P0", FIX,
     "1. Mở tệp vừa tải\n2. Đọc cột Trạng thái của dòng Hoạt động và dòng Khóa",
     "—",
     "- ⚠️ Ghi đúng chữ \"Hoạt động\" và \"Khóa\", không phải số 1 và số 2"),

    (6, "Xuất Excel theo bộ lọc đang áp dụng", "P0",
     FIX + "\nLọc Trạng thái = Khóa, bảng còn 1 dòng.",
     "1. Lọc Trạng thái = Khóa\n2. Bấm Xuất Excel\n3. Mở tệp và đếm số dòng",
     "Trạng thái: Khóa",
     "- ⚠️ Tệp chỉ có đúng 1 dòng khớp bộ lọc, KHÔNG xuất cả 12 lý do"),

    (7, "Xuất Excel khi kết quả nhiều hơn một trang", "P0",
     FIX + "\nDanh sách 12 dòng, đang xem trang 1 với 10 dòng mỗi trang.",
     "1. Đứng ở trang 1\n2. Bấm Xuất Excel\n3. Đếm số dòng trong tệp",
     "—",
     "- ⚠️ Tệp có đủ 12 dòng, không phải chỉ 10 dòng của trang đang xem"),

    (8, "Mô tả nhiều dòng giữ đúng ngắt dòng trong tệp", "P1",
     FIX + "\nMột lý do có mô tả gồm 3 đoạn xuống dòng.",
     "1. Bấm Xuất Excel\n2. Mở tệp và xem ô Mô tả của dòng đó",
     "—",
     "- ⚠️ Ô Mô tả giữ đúng 3 đoạn, không dính liền thành một dòng dài\n"
     "- Không hiện thẻ lạ kiểu dấu ngoặc nhọn hay ký hiệu xuống dòng dạng chữ"),

    (9, "Xuất Excel khi bộ lọc không ra kết quả", "P1", FIX,
     "1. Lọc ra kết quả trống (gõ chuỗi không tồn tại và bấm Tìm kiếm)\n2. Bấm Xuất Excel\n3. Mở tệp",
     "Từ khóa: zzzkhongtontai",
     "- Vẫn tải về được tệp, mở được, có logo và hàng tiêu đề nhưng không có dòng dữ liệu nào\n"
     "- Không báo lỗi đỏ"),

    (10, "Độ rộng cột trong tệp đủ đọc", "P2", FIX,
     "1. Mở tệp vừa tải\n2. Xem các cột Lý do hủy cuộc họp, Mô tả, Người tạo, Ngày cập nhật",
     "—",
     "- Không cột nào bị cắt chữ hay hiện dãy dấu thăng\n- Không phải kéo tay mới đọc được nội dung"),
]

S8 = [
    (1, "Nút Import Excel hiển thị đúng", "P0", ACC + "\n" + FIX,
     "1. Đăng nhập bằng tài khoản A, mở màn danh mục\n2. Quan sát nút Import Excel\n"
     "3. Đăng nhập lại bằng tài khoản B và quan sát",
     "—",
     "- Tài khoản A: nút \"Import Excel\" màu cam, đứng giữa nút Tạo mới và nút Xuất Excel\n"
     "- Tài khoản B: không có nút này"),

    (2, "Mở cửa sổ nhập từ Excel", "P1", FIX,
     "1. Bấm nút Import Excel\n2. Quan sát cửa sổ hiện ra",
     "—",
     "- Tiêu đề: Import Lý do hủy cuộc họp, dòng phụ \"Import từ Excel • Validate xong dòng hợp lệ sẽ bị "
     "khóa\"\n"
     "- Có nút tải tệp mẫu và vùng chọn tệp"),

    (3, "Tải tệp mẫu", "P1", FIX,
     "1. Bấm nút tải tệp mẫu trong cửa sổ nhập\n2. Mở tệp vừa tải",
     "—",
     "- Tệp tên Mau_import_LyDoHuyCuocHop.xlsx\n"
     "- Có 4 cột: STT · Lý do hủy cuộc họp (bắt buộc) · Trạng thái (bắt buộc) · Mô tả"),

    (4, "Chọn tệp đúng mẫu và xem trước dữ liệu", "P0",
     FIX + "\nChuẩn bị tệp 5 dòng hợp lệ, tên chưa tồn tại trong danh mục.",
     "1. Bấm Import Excel\n2. Chọn tệp 5 dòng\n3. Đếm số dòng trong bảng xem trước",
     "Tệp: 5 dòng, mỗi dòng có tên khác nhau, Trạng thái đều là Hoạt động",
     "- Bảng xem trước hiện đúng 5 dòng dữ liệu\n"
     "- ⚠️ Hàng tiêu đề của tệp không bị đếm thành một dòng dữ liệu"),

    (5, "Kiểm tra dữ liệu khi tất cả đều hợp lệ", "P0",
     FIX + "\nĐã chọn tệp 5 dòng hợp lệ.",
     "1. Bấm nút kiểm tra dữ liệu\n2. Quan sát bảng xem trước và thông báo",
     "—",
     "- Thông báo \"Validate thành công\" hoặc dòng chữ báo cả 5 dòng đã hợp lệ\n"
     "- ⚠️ Các dòng hợp lệ chuyển sang trạng thái bị khóa, không sửa tay được nữa\n"
     "- Nút nhập dữ liệu vào hệ thống bật lên"),

    (6, "Nhập dữ liệu hợp lệ vào hệ thống", "P0",
     FIX + "\nĐã kiểm tra xong 5 dòng hợp lệ.",
     "1. Bấm nút nhập dữ liệu\n2. Quan sát thông báo và danh sách",
     "—",
     "- Thông báo \"Import thành công 5 lý do hủy cuộc họp\"\n- Cửa sổ nhập tự đóng\n"
     "- Danh sách có thêm đủ 5 dòng mới, cột Người tạo là người đang đăng nhập"),

    (7, "Dòng thiếu tên lý do", "P0",
     FIX + "\nTệp 3 dòng, dòng thứ 2 để trống ô Lý do hủy cuộc họp.",
     "1. Chọn tệp\n2. Bấm kiểm tra dữ liệu\n3. Đọc lỗi ở dòng thứ 2",
     "Dòng 2: Lý do hủy cuộc họp = (trống) · Trạng thái = Hoạt động",
     "- Dòng 2 bị đánh dấu không hợp lệ, hiện lỗi \"Lý do hủy cuộc họp không được để trống\"\n"
     "- 2 dòng còn lại vẫn hợp lệ, thông báo ghi rõ 2 hợp lệ / 1 không hợp lệ"),

    (8, "Tên lý do dài quá 255 ký tự trong tệp", "P1",
     FIX + "\nTệp 2 dòng, dòng 1 có tên dài 300 ký tự.",
     "1. Chọn tệp\n2. Bấm kiểm tra dữ liệu",
     "Dòng 1: tên dài 300 ký tự",
     "- Dòng 1 báo lỗi \"Lý do hủy cuộc họp vượt quá độ dài cho phép (tối đa 255 ký tự)\"\n"
     "- Dòng 2 vẫn hợp lệ"),

    (9, "Mô tả dài quá 1000 ký tự trong tệp", "P2",
     FIX + "\nTệp 2 dòng, dòng 1 có mô tả dài 1500 ký tự.",
     "1. Chọn tệp\n2. Bấm kiểm tra dữ liệu",
     "Dòng 1: mô tả dài 1500 ký tự",
     "- Dòng 1 báo lỗi \"Mô tả vượt quá độ dài cho phép (tối đa 1000 ký tự)\""),

    (10, "Ô Trạng thái để trống trong tệp", "P0",
     FIX + "\nTệp 2 dòng, dòng 1 để trống ô Trạng thái.",
     "1. Chọn tệp\n2. Bấm kiểm tra dữ liệu",
     "Dòng 1: Trạng thái = (trống)",
     "- Dòng 1 báo lỗi \"Trạng thái không hợp lệ (chỉ nhận đúng: Hoạt động hoặc Khóa)\"\n"
     "- Dòng 1 không được nhập vào hệ thống"),

    (11, "Trạng thái viết sai chính tả hoặc sai dấu", "P0",
     FIX + "\nTệp 3 dòng: dòng 1 ghi \"hoạt động\" chữ thường, dòng 2 ghi \"Hoat dong\" không dấu, dòng 3 "
     "ghi \"Đang dùng\".",
     "1. Chọn tệp\n2. Bấm kiểm tra dữ liệu\n3. Đọc lỗi từng dòng",
     "Dòng 1: hoạt động · Dòng 2: Hoat dong · Dòng 3: Đang dùng",
     "- ⚠️ CẢ 3 dòng đều bị báo \"Trạng thái không hợp lệ (chỉ nhận đúng: Hoạt động hoặc Khóa)\" — ô này "
     "so khớp nguyên văn, phải đúng dấu và đúng chữ hoa chữ thường"),

    (12, "Nhập dòng có trạng thái Khóa", "P1",
     FIX + "\nTệp 1 dòng với Trạng thái ghi đúng \"Khóa\".",
     "1. Chọn tệp, kiểm tra dữ liệu và nhập vào hệ thống\n2. Tìm dòng vừa nhập trong danh sách",
     "Dòng 1: Lý do = Hủy do trùng lịch công tác · Trạng thái = Khóa",
     "- Nhập thành công\n"
     "- ⚠️ Dòng mới mang thẻ Khóa ngay, nút Sửa mờ, không xuất hiện trong ô chọn lý do khi hủy cuộc họp"),

    (13, "Tên trùng với lý do đã có trong hệ thống", "P0",
     FIX + "\nTệp 3 dòng, dòng 2 ghi đúng tên \"Hủy do khách dời lịch\" đã có sẵn.",
     "1. Chọn tệp\n2. Bấm kiểm tra dữ liệu",
     "Dòng 2: Hủy do khách dời lịch",
     "- Dòng 2 báo lỗi \"Lý do hủy cuộc họp đã tồn tại trong hệ thống\"\n"
     "- Nhập vào hệ thống thì chỉ 2 dòng còn lại được thêm, không ghi đè dòng cũ"),

    (14, "Hai dòng trùng nhau trong cùng một tệp", "P0",
     FIX + "\nTệp 4 dòng, dòng 2 và dòng 4 có tên giống hệt nhau và chưa có trong hệ thống.",
     "1. Chọn tệp\n2. Bấm kiểm tra dữ liệu\n3. Đọc lỗi của dòng sau",
     "Dòng 2 và dòng 4: Hủy do khách đi công tác",
     "- ⚠️ Dòng đứng sau báo lỗi trùng lặp trong tệp và ghi rõ SỐ DÒNG đã trùng với nó\n"
     "- Dòng đứng trước vẫn hợp lệ; nhập vào hệ thống chỉ tạo 1 bản ghi cho tên đó"),

    (15, "Trùng nhau chỉ khác chữ hoa chữ thường hoặc khoảng trắng thừa", "P1",
     FIX + "\nTệp 3 dòng: dòng 1 ghi \"Hủy do mưa lớn\", dòng 2 ghi \"HỦY DO MƯA LỚN\", dòng 3 ghi "
     "\"  Hủy do mưa lớn  \" (có khoảng trắng hai đầu).",
     "1. Chọn tệp\n2. Bấm kiểm tra dữ liệu",
     "3 dòng như mô tả ở tiền điều kiện",
     "- ⚠️ Dòng 2 và dòng 3 đều bị coi là trùng với dòng 1 — hệ thống cắt khoảng trắng hai đầu và bỏ qua "
     "khác biệt chữ hoa chữ thường khi so trùng\n"
     "- Chỉ dòng 1 hợp lệ"),

    (16, "Tệp vừa có dòng đúng vừa có dòng sai", "P0",
     FIX + "\nTệp 5 dòng: 3 dòng hợp lệ, 2 dòng sai (1 thiếu tên, 1 sai trạng thái).",
     "1. Chọn tệp\n2. Bấm kiểm tra dữ liệu\n3. Bấm nhập dữ liệu\n4. Kiểm tra danh sách",
     "Tệp 5 dòng như tiền điều kiện",
     "- Sau kiểm tra: thông báo ghi rõ 3 hợp lệ, 2 không hợp lệ; 3 dòng đúng bị khóa lại, 2 dòng sai vẫn "
     "sửa được\n"
     "- ⚠️ Sau khi nhập: thông báo cảnh báo \"Import thành công 3/5 lý do hủy cuộc họp. 2 lý do hủy cuộc "
     "họp thất bại.\"; danh mục chỉ tăng thêm đúng 3 dòng"),

    (17, "Sửa tay dòng lỗi rồi kiểm tra lại", "P1",
     FIX + "\nĐang ở bước xem trước, có 1 dòng lỗi thiếu tên.",
     "1. Gõ tên hợp lệ vào ô bị lỗi ngay trong bảng xem trước\n2. Bấm kiểm tra dữ liệu lần nữa",
     "Tên bổ sung: Hủy do khách bận đột xuất",
     "- Dòng vừa sửa chuyển sang hợp lệ, hết chữ lỗi đỏ\n- Số dòng hợp lệ tăng thêm 1"),

    (18, "Tệp không có dòng dữ liệu nào", "P1", FIX + "\nTệp chỉ có hàng tiêu đề.",
     "1. Chọn tệp\n2. Bấm kiểm tra dữ liệu",
     "Tệp: chỉ có hàng tiêu đề",
     "- Hệ thống báo phải có ít nhất 1 dòng dữ liệu, không cho sang bước nhập\n- Không báo lỗi khó hiểu"),

    (19, "Tệp vượt quá 1000 dòng", "P2", FIX + "\nTệp có 1200 dòng hợp lệ.",
     "1. Chọn tệp\n2. Bấm kiểm tra dữ liệu",
     "Tệp: 1200 dòng",
     "- Hệ thống báo mỗi lần nhập tối đa 1000 dòng\n- Không nhập bản ghi nào vào danh mục"),

    (20, "Tệp sai cấu trúc cột", "P1", FIX + "\nTệp có các tiêu đề cột hoàn toàn khác mẫu.",
     "1. Chọn tệp\n2. Quan sát bảng xem trước",
     "Tệp: tiêu đề cột là A, B, C, D",
     "- Hệ thống không nhận, báo tệp sai mẫu hoặc bảng xem trước không ghép được cột\n"
     "- ⚠️ Không được âm thầm nhập dữ liệu vào sai cột"),

    (21, "Đóng cửa sổ nhập giữa chừng rồi mở lại", "P2", FIX,
     "1. Bấm Import Excel, chọn tệp, kiểm tra dữ liệu\n2. Đóng cửa sổ khi chưa nhập\n"
     "3. Bấm Import Excel lần nữa",
     "—",
     "- Cửa sổ mở lại ở bước chọn tệp, không giữ dữ liệu của lần trước\n- Danh mục không phát sinh dòng nào"),

    (22, "Người tạo của dòng nhập từ Excel", "P1", FIX + "\nĐăng nhập bằng tài khoản A.",
     "1. Nhập 2 dòng hợp lệ từ tệp Excel\n2. Xem cột Người tạo của 2 dòng mới",
     "—",
     "- Cột Người tạo ghi tên tài khoản A (người thực hiện nhập), không để trống\n"
     "- Ngày tạo là ngày hôm nay"),
]

S9 = [
    (1, "Tên lý do chỉ gồm khoảng trắng", "P0", FIX,
     "1. Bấm Tạo mới\n2. Gõ 5 dấu cách vào ô Lý do hủy cuộc họp, không gõ chữ nào\n3. Bấm Lưu\n"
     "4. Kiểm tra danh sách",
     "Lý do hủy cuộc họp: (5 dấu cách)",
     "- ⚠️ Hệ thống phải báo lỗi bắt buộc tại ô Lý do hủy cuộc họp và KHÔNG tạo ra bản ghi nào\n"
     "- Nếu lưu được và danh sách xuất hiện một dòng có tên trống thì ghi nhận Failed"),

    (2, "Tên có ký tự đặc biệt của thẻ trình duyệt", "P1", FIX,
     "1. Bấm Tạo mới\n2. Nhập tên có chứa dấu ngoặc nhọn và dấu nháy\n3. Bấm Lưu\n"
     "4. Xem dòng đó trong danh sách và trong tệp Excel xuất ra",
     "Lý do hủy cuộc họp: Hủy do <khách> \"bận\" & đổi lịch",
     "- ⚠️ Danh sách hiển thị nguyên văn đúng chuỗi đã nhập, KHÔNG mất phần trong dấu ngoặc nhọn, không "
     "chạy thành thẻ, không hiện ký hiệu lạ kiểu và-a-m-p\n"
     "- Tệp Excel cũng hiện đúng nguyên văn"),

    (3, "Tên có tiếng Việt có dấu và ký tự biểu cảm", "P2", FIX,
     "1. Bấm Tạo mới\n2. Nhập tên có dấu tiếng Việt đầy đủ kèm 1 ký tự biểu cảm\n3. Bấm Lưu",
     "Lý do hủy cuộc họp: Hủy do khách ốm đột xuất 🤒",
     "- Lưu thành công, danh sách hiển thị đúng dấu tiếng Việt và ký tự biểu cảm, không thành dấu hỏi"),

    (4, "Mô tả nhiều đoạn xuống dòng", "P1", FIX,
     "1. Bấm Tạo mới\n2. Nhập mô tả gồm 3 đoạn, mỗi đoạn xuống dòng bằng phím Enter\n3. Bấm Lưu\n"
     "4. Xem ô Mô tả trong danh sách và mở lại bằng nút Xem",
     "Mô tả: 3 đoạn xuống dòng",
     "- Danh sách giữ đúng 3 đoạn\n- Mở lại bằng nút Xem cũng thấy đúng 3 đoạn, không dính liền một dòng"),

    (5, "Tên chỉ có 1 ký tự", "P2", FIX,
     "1. Bấm Tạo mới\n2. Nhập 1 chữ cái vào ô tên\n3. Bấm Lưu",
     "Lý do hủy cuộc họp: X",
     "- Lưu thành công, không có ràng buộc độ dài tối thiểu"),

    (6, "Khoảng trắng thừa hai đầu tên khi thêm tay", "P1", FIX,
     "1. Bấm Tạo mới\n2. Nhập \"  Hủy do khách hủy gấp  \" (có khoảng trắng hai đầu)\n3. Bấm Lưu\n"
     "4. Xem tên trong danh sách\n5. Thử thêm lại đúng tên đó nhưng không có khoảng trắng",
     "Lần 1: (khoảng trắng)Hủy do khách hủy gấp(khoảng trắng) · Lần 2: Hủy do khách hủy gấp",
     "- ⚠️ Tên hiển thị trong danh sách không được thừa khoảng trắng hai đầu\n"
     "- Lần 2 phải bị chặn với thông báo đã tồn tại (không được tạo ra 2 dòng nhìn giống hệt nhau)"),

    (7, "Ô Trạng thái không cho để trống", "P1", FIX,
     "1. Bấm Tạo mới\n2. Mở ô Trạng thái và tìm cách bỏ chọn giá trị đang có",
     "—",
     "- ⚠️ Ô Trạng thái không có nút xóa lựa chọn, luôn phải là Hoạt động hoặc Khóa\n"
     "- Danh sách chọn chỉ có đúng 2 giá trị này, không có ô tìm kiếm bên trong"),

    (8, "Nhập lý do rồi tìm lại bằng chính chuỗi đặc biệt vừa nhập", "P2",
     FIX + "\nĐã tạo lý do \"Hủy do <khách> \"bận\" & đổi lịch\".",
     "1. Gõ \"&\" vào ô tìm nhanh và bấm Tìm kiếm",
     "Từ khóa: &",
     "- Tìm ra đúng dòng vừa tạo, không báo lỗi, không trả về toàn bộ danh sách"),
]

S10 = [
    (1, "Ô chọn lý do khi hủy cuộc họp chỉ liệt kê lý do đang Hoạt động", "P0",
     FIX + "\nCó 1 cuộc họp chưa tới giờ bắt đầu để thử hủy.",
     "1. Mở màn Cuộc họp, mở một cuộc họp chưa tới giờ bắt đầu\n2. Bấm nút Hủy\n"
     "3. Mở ô chọn Lý do hủy, đếm và đối chiếu với danh mục",
     "—",
     "- Ô chọn liệt kê đúng 11 lý do đang Hoạt động\n"
     "- ⚠️ Không có lý do \"Hủy do phòng họp bị trùng\" (đang Khóa)\n"
     "- Thứ tự liệt kê là từ lý do tạo cũ nhất đến mới nhất"),

    (2, "Lý do mới thêm xuất hiện ngay trong ô chọn", "P0",
     FIX,
     "1. Thêm lý do mới ở màn danh mục\n2. Sang màn Cuộc họp, mở một cuộc họp chưa tới giờ bắt đầu\n"
     "3. Bấm Hủy và mở ô chọn Lý do hủy",
     "Lý do mới: Hủy do khách đổi địa điểm",
     "- Lý do vừa thêm có mặt trong danh sách chọn, nằm ở cuối danh sách\n- Chọn được và hủy được cuộc họp"),

    (3, "Lý do vừa khóa biến mất khỏi ô chọn", "P0", FIX,
     "1. Khóa lý do \"Hủy do mình bận đột xuất\" ở màn danh mục\n"
     "2. Sang màn Cuộc họp, bấm Hủy một cuộc họp chưa tới giờ bắt đầu\n3. Mở ô chọn Lý do hủy",
     "—",
     "- ⚠️ Lý do vừa khóa không còn trong ô chọn, số dòng trong ô chọn giảm đúng 1"),

    (4, "Đổi tên lý do thì cuộc họp đã hủy hiện tên mới", "P0",
     FIX + "\nCuộc họp \"Khảo sát nhà máy A\" đã hủy bằng lý do \"Hủy do khách không gặp\".",
     "1. Ở màn danh mục, sửa tên lý do đó thành \"Hủy do khách vắng mặt\"\n"
     "2. Mở lại cuộc họp \"Khảo sát nhà máy A\" và đọc ô Lý do hủy",
     "Tên mới: Hủy do khách vắng mặt",
     "- ⚠️ Cuộc họp hiện TÊN MỚI \"Hủy do khách vắng mặt\" — tên lý do đọc trực tiếp từ danh mục, không "
     "phải bản chép cố định lúc hủy\n- Phần ghi chú hủy kèm theo giữ nguyên"),

    (5, "Hủy cuộc họp bằng một lý do làm khóa nút Xóa của lý do đó", "P0",
     FIX + "\nLý do \"Hủy do thời tiết xấu\" chưa cuộc họp nào dùng, nút Xóa đang bấm được.",
     "1. Mở một cuộc họp chưa tới giờ bắt đầu, bấm Hủy, chọn lý do \"Hủy do thời tiết xấu\", xác nhận\n"
     "2. Quay lại màn danh mục, tải lại danh sách\n3. Rê chuột vào nút Xóa của lý do đó",
     "—",
     "- ⚠️ Nút Xóa của lý do đó chuyển sang mờ xám ngay, chú giải đổi thành câu lý do đang được dùng ở "
     "cuộc họp\n- Nút khóa và nút Sửa vẫn dùng được bình thường"),

    (6, "Không còn lý do Hoạt động nào trong danh mục", "P1",
     "Tất cả lý do trong danh mục đều đang ở trạng thái Khóa (khóa hết 12 dòng).",
     "1. Mở một cuộc họp chưa tới giờ bắt đầu\n2. Bấm Hủy\n3. Mở ô chọn Lý do hủy và thử xác nhận hủy",
     "—",
     "- ⚠️ Ô chọn trống, không có lựa chọn nào\n"
     "- Bấm xác nhận hủy thì hệ thống báo lỗi đỏ bắt buộc chọn lý do, cuộc họp KHÔNG bị hủy\n"
     "- Không để hủy được với lý do trống"),
]

S11 = [
    (1, "Hai người cùng thêm một tên giống nhau", "P0",
     FIX + "\nMở màn danh mục trên 2 trình duyệt bằng 2 tài khoản đều có quyền quản lý.",
     "1. Cả 2 cùng bấm Tạo mới và nhập cùng một tên chưa tồn tại\n2. Người thứ nhất bấm Lưu\n"
     "3. Người thứ hai bấm Lưu ngay sau đó",
     "Tên: Hủy do thay đổi kế hoạch chung",
     "- Người thứ nhất: Thêm mới thành công\n"
     "- ⚠️ Người thứ hai bị chặn với thông báo \"Lý do hủy cuộc họp đã tồn tại trong hệ thống\"; danh mục "
     "chỉ có 1 dòng với tên đó"),

    (2, "Sửa một lý do vừa bị người khác khóa", "P0",
     FIX + "\nMở màn trên 2 trình duyệt bằng 2 tài khoản có quyền quản lý.",
     "1. Người A bấm Sửa dòng \"Hủy do thời tiết xấu\", đổi tên nhưng CHƯA bấm Lưu\n"
     "2. Người B khóa chính dòng đó và xác nhận\n3. Người A bấm Lưu",
     "Tên mới của người A: Hủy do mưa bão kéo dài",
     "- ⚠️ Người A nhận thông báo \"Dữ liệu đã thay đổi, vui lòng tải lại\", nội dung không được ghi đè\n"
     "- Dòng vẫn ở trạng thái Khóa với tên cũ"),

    (3, "Sửa một lý do vừa bị người khác xóa", "P1",
     FIX + "\nMở màn trên 2 trình duyệt bằng 2 tài khoản có quyền quản lý.",
     "1. Người A bấm Sửa một dòng chưa được cuộc họp nào dùng, đổi mô tả, chưa bấm Lưu\n"
     "2. Người B xóa chính dòng đó\n3. Người A bấm Lưu",
     "—",
     "- Người A nhận thông báo \"Dữ liệu đã thay đổi, vui lòng tải lại\"\n"
     "- Không tạo lại bản ghi đã xóa, không treo trang"),

    (4, "Mở xem một dòng vừa bị người khác xóa", "P1",
     FIX + "\nMở màn trên 2 trình duyệt.",
     "1. Người B xóa một dòng\n2. Người A (chưa tải lại trang) bấm nút Xem ở chính dòng đó",
     "—",
     "- Hiện thông báo \"Dữ liệu đã thay đổi, vui lòng tải lại\"\n"
     "- ⚠️ Cửa sổ xem KHÔNG mở ra với dữ liệu trống, trang không treo"),

    (5, "Danh mục dùng chung cho mọi công ty và phòng ban", "P0",
     ACC + "\nTài khoản A thuộc Công ty 1, tài khoản D thuộc Công ty 4, cả hai đều có quyền quản lý danh mục.",
     "1. Tài khoản A thêm lý do mới\n2. Đăng nhập bằng tài khoản D ở trình duyệt khác, mở màn danh mục\n"
     "3. Tìm lý do vừa thêm",
     "Lý do mới: Hủy do lịch công ty thay đổi",
     "- ⚠️ Tài khoản D thấy đúng lý do do tài khoản A tạo và thấy tổng số dòng giống hệt tài khoản A — "
     "danh mục dùng chung toàn hệ thống, không chia theo công ty / phòng ban / bộ phận"),

    (6, "Nhập từ Excel trong lúc người khác thêm tay cùng tên", "P2",
     FIX + "\n2 tài khoản có quyền quản lý, tên \"Hủy do đối tác bận\" chưa có trong danh mục.",
     "1. Người A chuẩn bị tệp 1 dòng với tên đó và bấm kiểm tra dữ liệu (đang hợp lệ)\n"
     "2. Người B thêm tay đúng tên đó và lưu thành công\n3. Người A bấm nhập dữ liệu",
     "Tên: Hủy do đối tác bận",
     "- ⚠️ Người A nhận cảnh báo dòng đó đã tồn tại và không nhập được\n"
     "- Danh mục chỉ có 1 dòng mang tên đó"),

    (7, "Hai người cùng xóa một dòng", "P2",
     FIX + "\n2 tài khoản có quyền quản lý đang mở cùng màn.",
     "1. Người A xóa dòng \"Hủy do hệ thống bảo trì\" thành công\n"
     "2. Người B (chưa tải lại) cũng bấm Xóa dòng đó và xác nhận",
     "—",
     "- Người B nhận thông báo \"Dữ liệu đã thay đổi, vui lòng tải lại\"\n"
     "- Tổng số lý do chỉ giảm đúng 1"),
]

S12 = [
    (1, "Luồng quản trị danh mục từ đầu đến cuối", "P0", ACC + "\n" + FIX,
     "1. Đăng nhập bằng tài khoản A, " + MENU + "\n"
     "2. Bấm Tạo mới, thêm lý do \"Hủy do khách đi công tác nước ngoài\", bấm Lưu\n"
     "3. Gõ \"nước ngoài\" vào ô tìm nhanh, bấm Tìm kiếm\n"
     "4. Bấm Sửa, đổi Mô tả, bấm Lưu\n"
     "5. Bấm nút khóa ở dòng đó, xác nhận Khóa\n"
     "6. Bấm nút mở khóa, xác nhận Mở khóa\n"
     "7. Bấm Xóa, xác nhận Xóa\n8. Bấm Làm mới",
     "Lý do: Hủy do khách đi công tác nước ngoài",
     "- Bước 2: Thêm mới thành công, dòng lên đầu danh sách\n- Bước 3: còn đúng 1 dòng\n"
     "- Bước 4: Cập nhật thành công, cột Cập nhật đổi sang thời điểm hiện tại và tên người đang đăng nhập\n"
     "- Bước 5: Khóa thành công, thẻ Khóa, nút Sửa mờ\n- Bước 6: Mở khóa thành công, nút Sửa dùng lại được\n"
     "- Bước 7: Xóa thành công, dòng biến mất\n"
     "- Bước 8: bộ lọc sạch, danh sách trở về đúng số lý do ban đầu"),

    (2, "Luồng nhập từ Excel rồi lọc và xuất lại để đối chiếu", "P0", ACC + "\n" + FIX,
     "1. Đăng nhập bằng tài khoản A, mở màn danh mục\n"
     "2. Bấm Import Excel, chọn tệp 5 dòng hợp lệ, kiểm tra dữ liệu rồi nhập vào hệ thống\n"
     "3. Lọc Người tạo = tài khoản A\n4. Bấm Xuất Excel\n5. Mở tệp và đối chiếu",
     "Tệp: 5 dòng hợp lệ, trạng thái đều Hoạt động",
     "- Bước 2: Import thành công 5 lý do hủy cuộc họp, danh sách tăng thêm 5 dòng\n"
     "- Bước 3: bảng chỉ còn các lý do do tài khoản A tạo, trong đó có đủ 5 dòng vừa nhập\n"
     "- Bước 5: ⚠️ tệp Excel có đúng số dòng của kết quả lọc, tên và mô tả khớp từng dòng trên màn hình"),

    (3, "Luồng nghiệp vụ trọn vẹn: tạo lý do, hủy cuộc họp, ngừng dùng lý do", "P0",
     ACC + "\n" + FIX + "\nCó 1 cuộc họp \"Khảo sát nhà máy B\" chưa tới giờ bắt đầu.",
     "1. Ở màn danh mục, thêm lý do \"Hủy do khách yêu cầu dời sang quý sau\"\n"
     "2. Sang màn Cuộc họp, mở \"Khảo sát nhà máy B\", bấm Hủy, chọn lý do vừa tạo, nhập ghi chú và xác nhận\n"
     "3. Quay lại màn danh mục, tải lại danh sách, kiểm tra nút Xóa của lý do đó\n"
     "4. Bấm nút khóa ở lý do đó và xác nhận\n"
     "5. Mở một cuộc họp khác chưa tới giờ bắt đầu, bấm Hủy và mở ô chọn lý do\n"
     "6. Mở lại cuộc họp \"Khảo sát nhà máy B\" và đọc ô Lý do hủy",
     "Lý do: Hủy do khách yêu cầu dời sang quý sau\nGhi chú hủy: Khách đề nghị lùi sang tháng 1",
     "- Bước 1: thêm thành công\n- Bước 2: cuộc họp chuyển sang trạng thái đã hủy\n"
     "- Bước 3: ⚠️ nút Xóa của lý do đó đã chuyển sang mờ, chú giải báo đang được dùng ở cuộc họp\n"
     "- Bước 4: Khóa thành công\n- Bước 5: ⚠️ ô chọn không còn lý do vừa khóa\n"
     "- Bước 6: ⚠️ cuộc họp cũ VẪN hiện đúng tên lý do kèm ghi chú \"Khách đề nghị lùi sang tháng 1\""),

    (4, "Luồng của tài khoản chỉ có quyền xem", "P0", ACC + "\n" + FIX,
     "1. Đăng nhập bằng tài khoản B, " + MENU + "\n"
     "2. Gõ \"khách\" vào ô tìm nhanh và bấm Tìm kiếm\n"
     "3. Lọc Trạng thái = Hoạt động\n4. Bấm sắp xếp cột Cập nhật\n5. Bấm nút Xem ở một dòng\n"
     "6. Đóng cửa sổ và bấm Làm mới",
     "Tài khoản: B",
     "- Mọi thao tác xem, lọc, tìm, sắp xếp, phân trang đều hoạt động bình thường\n"
     "- ⚠️ Trong suốt luồng KHÔNG có nút Tạo mới, Import Excel, Xuất Excel, Sửa, Xóa, khóa / mở khóa\n"
     "- Không xuất hiện thông báo lỗi quyền nào (vì không có nút nào để bấm nhầm)"),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", S1),
    ("II", "BỘ LỌC & TÌM KIẾM", S2),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", S3),
    ("IV", "THÊM / SỬA / XEM LÝ DO HỦY", S4),
    ("V", "KHÓA / MỞ KHÓA", S5),
    ("VI", "XÓA", S6),
    ("VII", "XUẤT EXCEL", S7),
    ("VIII", "NHẬP DANH SÁCH TỪ EXCEL", S8),
    ("IX", "RÀNG BUỘC NHẬP LIỆU", S9),
    ("X", "ẢNH HƯỞNG SANG MÀN CUỘC HỌP", S10),
    ("XI", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", S11),
    ("XII", "LUỒNG TỔNG THỂ", S12),
]

if __name__ == "__main__":
    build(
        output_file=OUTPUT,
        sheet_name="Trang tính1",
        feature_name=FEATURE,
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )
