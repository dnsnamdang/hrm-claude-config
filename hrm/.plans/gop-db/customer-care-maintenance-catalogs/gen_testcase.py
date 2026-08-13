# -*- coding: utf-8 -*-
"""Sinh 2 file testcase cho 2 danh muc bao duong (phan he CSKH):
  - Cap dich vu bao duong
  - Danh muc ghi chu kiem tra bao duong

Chay:  python gen_testcase.py
"""
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "..", ".claude", "skills", "testcase-documenter", "assets"))

from tc_engine import build  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SHEET_NAME = "Trang tính1"

# ############################################################################
# MAN 1 — CAP DICH VU BAO DUONG
# ############################################################################
LV_DESC = [
    ("1. Mục đích tính năng",
     "Quản lý danh sách các cấp dịch vụ bảo dưỡng (Cấp 1, Cấp 2, Cấp 1 (6T)…). Cấp dịch vụ được "
     "dùng để phân mức bảo dưỡng trong gói bảo dưỡng, báo giá dịch vụ, hợp đồng dịch vụ, "
     "phiếu phân công công việc và phiếu nhập kết quả.\n"
     "Màn hình nằm ở phân hệ Chăm sóc khách hàng → nhóm menu Danh mục - Dịch vụ → "
     "Cấp dịch vụ bảo dưỡng.\n"
     "Đây là màn được chuyển từ hệ thống cũ sang, hai cổng dùng CHUNG một danh mục."),

    ("2. Đối tượng được tính / hiển thị",
     "- Toàn bộ cấp dịch vụ trong danh mục, KHÔNG phân theo công ty / phòng ban.\n"
     "- Mỗi dòng gồm 4 cột: STT, Tên cấp, Cập nhật, Hành động.\n"
     "- Danh mục hiện có khoảng 29 cấp dịch vụ."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Không có cấp dịch vụ nào bị ẩn. Màn này KHÔNG có trạng thái Hoạt động / Khóa — "
     "chỉ có thêm, sửa, xóa.\n"
     "- Khi tìm kiếm theo tên, các cấp không khớp bị loại khỏi kết quả."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Không áp dụng. Màn hình không có bộ lọc theo khoảng thời gian.\n"
     "Cột Cập nhật chỉ để xem và để sắp xếp."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Danh sách phẳng, không phân cấp cha - con.\n"
     "Tên cấp là giá trị duy nhất trong toàn danh mục.\n"
     "Quan hệ với màn khác: một cấp dịch vụ có thể được dùng ở 5 loại chứng từ khác nhau — "
     "gói bảo dưỡng, báo giá dịch vụ, hợp đồng dịch vụ, phiếu phân công công việc, "
     "phiếu nhập kết quả. Đây là căn cứ chặn xóa."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "Không cộng dồn. Mỗi cấp dịch vụ là một dòng độc lập.\n"
     "Chống trùng: Tên cấp phải duy nhất, trùng sẽ báo \"Tên cấp đã tồn tại\".\n"
     "Khoảng trắng thừa ở đầu và cuối tên được hệ thống cắt bỏ trước khi kiểm tra trùng."),

    ("7. Phân quyền cấp",
     "Hai quyền dành riêng cho màn này:\n"
     "- \"Xem cấp dịch vụ bảo dưỡng\": vào màn hình, xem danh sách, mở xem chi tiết, xuất Excel.\n"
     "- \"Quản lý cấp dịch vụ bảo dưỡng\": thêm mới, sửa, xóa.\n"
     "Không có quyền nào trong hai quyền trên thì không vào được màn hình.\n"
     "Danh mục KHÔNG phân quyền theo công ty / phòng ban / bộ phận."),

    ("8. Cách tính các ô thống kê",
     "- Dòng \"Hiển thị a - b / N\" dưới bảng: a là dòng đầu của trang đang xem, b là dòng cuối, "
     "N là tổng số cấp dịch vụ khớp bộ lọc hiện tại.\n"
     "- Cột STT đánh theo trang: trang 2 với cỡ trang 10 thì bắt đầu từ 11."),

    ("9. Ghi chú đọc bảng",
     "- Màn này KHÔNG có trạng thái Khóa / Mở khóa như các danh mục khác — chỉ Thêm, Sửa, Xóa.\n"
     "- Cấp dịch vụ đang được dùng ở bất kỳ chứng từ nào trong 5 loại nêu ở mục 5 thì KHÔNG xóa "
     "được. Rê chuột vào nút Xóa để đọc lý do.\n"
     "- Thông báo chặn xóa nêu tối đa 3 nơi đang dùng, dù thực tế có thể nhiều hơn.\n"
     "⚠️ Ở hệ thống cũ, cấp dịch vụ chỉ bị chặn xóa khi được dùng ở gói bảo dưỡng — 5 loại chứng "
     "từ còn lại KHÔNG được kiểm, nên xóa được cấp đang dùng trong hợp đồng và báo giá. "
     "Bản mới đã sửa. Đây là nhóm bắt buộc phải kiểm kỹ.\n"
     "- Bộ lọc được ghi nhớ trong 10 phút; kiểm thử tìm kiếm nên bấm Làm mới trước mỗi kịch bản."),
]

LV_PRE_PERM = ("Có sẵn 2 tài khoản: A chỉ có quyền \"Xem cấp dịch vụ bảo dưỡng\"; "
               "B có quyền \"Quản lý cấp dịch vụ bảo dưỡng\". Danh mục có 29 cấp dịch vụ, "
               "trong đó \"Cấp 1\" đang được dùng ở gói bảo dưỡng và hợp đồng dịch vụ, "
               "\"Cấp thử\" mới tạo chưa dùng ở đâu.")

LV_ROLE = [
    ("01", "Vào màn hình khi chỉ có quyền Xem", "P0", LV_PRE_PERM,
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Vào phân hệ Chăm sóc khách hàng → Danh mục - Dịch vụ → Cấp dịch vụ bảo dưỡng",
     "Tài khoản A",
     "- Vào được màn hình, bảng hiển thị đủ 29 cấp dịch vụ\n"
     "- KHÔNG có nút Tạo mới\n"
     "- Mỗi dòng chỉ có nút Xem; KHÔNG có nút Sửa, nút Xóa\n"
     "- Vẫn có nút Xuất Excel"),

    ("02", "Vào màn hình khi có quyền Quản lý", "P0", LV_PRE_PERM,
     "1. Đăng nhập bằng tài khoản B\n2. Vào Cấp dịch vụ bảo dưỡng", "Tài khoản B",
     "- Có nút Tạo mới và nút Xuất Excel\n- Mỗi dòng có đủ 3 nút: Xem, Sửa, Xóa"),

    ("03", "Chặn vào màn hình khi không có quyền nào", "P0",
     "Tài khoản C không có cả hai quyền của màn này.",
     "1. Đăng nhập bằng tài khoản C\n2. Tìm mục Cấp dịch vụ bảo dưỡng trong phân hệ Chăm sóc "
     "khách hàng\n3. Dán thẳng đường dẫn màn hình vào thanh địa chỉ", "Tài khoản C",
     "- Mục menu KHÔNG hiện\n"
     "- Dán thẳng đường dẫn thì chuyển sang trang báo không tìm thấy, không lộ dữ liệu"),

    ("04", "Chặn Thêm mới khi bỏ qua giao diện", "P0", LV_PRE_PERM,
     "1. Đăng nhập bằng tài khoản A, lấy mã đăng nhập\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Thêm cấp dịch vụ\n3. Mở lại màn hình",
     "Tên cấp: Cấp trộm",
     "- Hệ thống từ chối, báo không có quyền\n- Danh sách vẫn 29 dòng"),

    ("05", "Chặn Sửa khi bỏ qua giao diện", "P0", LV_PRE_PERM,
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Sửa cấp \"Cấp 1\"\n3. Mở lại màn hình",
     "Đổi tên thành \"Bị sửa trộm\"",
     "- Hệ thống từ chối, báo không có quyền\n- Tên cũ giữ nguyên"),

    ("06", "Chặn Xóa khi bỏ qua giao diện", "P0", LV_PRE_PERM,
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa cấp \"Cấp thử\"\n3. Mở lại màn hình",
     "Cấp thử (về nghiệp vụ là xóa được)",
     "- Hệ thống từ chối, báo không có quyền\n- Cấp thử vẫn còn trong danh sách"),

    ("07", "Người có quyền Quản lý làm được trọn vòng đời", "P1", LV_PRE_PERM,
     "1. Đăng nhập bằng tài khoản B\n2. Tạo mới 1 cấp dịch vụ\n3. Sửa cấp vừa tạo\n4. Xóa cấp đó",
     "Tên cấp: Cấp kiểm thử",
     "- Cả 3 thao tác đều thực hiện được kèm thông báo thành công\n"
     "- Sau bước 4, cấp đó không còn trong danh sách"),
]

LV_PRE = ("Đăng nhập bằng tài khoản có quyền \"Quản lý cấp dịch vụ bảo dưỡng\". "
          "Danh mục có 29 cấp dịch vụ; \"Cấp 1\" đang được dùng ở gói bảo dưỡng, hợp đồng dịch vụ "
          "và báo giá dịch vụ; \"Cấp thử\" chưa dùng ở đâu.")

LV_SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", [
        ("001", "Mở màn hình lần đầu", "P0", LV_PRE,
         "1. Vào phân hệ Chăm sóc khách hàng → Danh mục - Dịch vụ → Cấp dịch vụ bảo dưỡng\n"
         "2. Quan sát toàn màn hình", "—",
         "- Tiêu đề trang và tiêu đề bảng đều là \"Cấp dịch vụ bảo dưỡng\"\n"
         "- Khối lọc có tiêu đề \"Bộ lọc cấp dịch vụ bảo dưỡng\" và dòng phụ "
         "\"Tìm kiếm theo tên cấp dịch vụ bảo dưỡng\"\n"
         "- Bảng có đủ 4 cột: STT, Tên cấp, Cập nhật, Hành động\n"
         "- Dưới bảng có nút Tạo mới và nút Xuất Excel"),

        ("002", "Hiển thị đủ 29 bản ghi khi chưa lọc", "P0", LV_PRE,
         "1. Mở màn hình\n2. Đọc dòng Hiển thị dưới bảng", "—",
         "- Tổng hiển thị là 29"),

        ("003", "Màn hình không có cột Trạng thái", "P1", LV_PRE,
         "1. Mở màn hình\n2. Đối chiếu các cột của bảng", "—",
         "- KHÔNG có cột Trạng thái, KHÔNG có nút Khóa / Mở khóa\n"
         "⚠️ Đây là điểm khác so với các danh mục khác — cố ý bám theo hệ thống cũ"),

        ("004", "Cột Cập nhật hiện thời điểm sửa gần nhất", "P1", LV_PRE,
         "1. Mở màn hình\n2. Nhìn cột Cập nhật", "—",
         "- Hiện ngày giờ cập nhật gần nhất; dòng chưa từng sửa vẫn hiện thông tin lần tạo, "
         "không để trắng trơn"),

        ("005", "Bảng trống khi tìm không khớp gì", "P1", LV_PRE,
         "1. Gõ \"khongtontai123\" vào ô tìm nhanh\n2. Bấm Tìm kiếm", "khongtontai123",
         "- Bảng hiện thông báo không có dữ liệu phù hợp, tổng dưới bảng là 0\n"
         "- Nút Tạo mới và Xuất Excel vẫn còn"),

        ("006", "Vào màn hình khi danh mục rỗng", "P2",
         "Môi trường kiểm thử riêng, danh mục cấp dịch vụ không có bản ghi nào.",
         "1. Mở màn hình", "—",
         "- Màn hình mở bình thường, không lỗi; bảng hiện thông báo không có dữ liệu"),
    ]),

    ("II", "BỘ LỌC & TÌM KIẾM", [
        ("001", "Tìm nhanh theo Tên cấp", "P0", LV_PRE,
         "1. Gõ \"Cấp 1\" vào ô tìm nhanh\n2. Bấm Tìm kiếm", "Cấp 1",
         "- Kết quả gồm mọi cấp có chuỗi \"Cấp 1\" trong tên\n"
         "⚠️ Gợi ý trong ô ghi rõ: \"Tìm theo tên cấp...\""),

        ("002", "Tìm nhanh khớp một phần chuỗi", "P0", LV_PRE,
         "1. Gõ \"6T\" (chỉ một phần của \"Cấp 1 (6T)\")\n2. Bấm Tìm kiếm", "6T",
         "- Cấp \"Cấp 1 (6T)\" vẫn ra kết quả\n"
         "⚠️ Không được yêu cầu gõ đúng nguyên tên mới ra kết quả"),

        ("003", "Tìm nhanh không phân biệt hoa thường", "P1", LV_PRE,
         "1. Gõ \"cấp\" bằng chữ thường\n2. Bấm Tìm kiếm", "cấp",
         "- Kết quả giống hệt khi gõ \"Cấp\""),

        ("004", "Gõ ô tìm nhanh mà chưa bấm Tìm kiếm", "P1", LV_PRE,
         "1. Gõ từ khóa\n2. Chờ 5 giây, không bấm gì", "Cấp 1",
         "- Bảng vẫn giữ nguyên 29 dòng, chưa lọc"),

        ("005", "Nút Làm mới xóa điều kiện và nạp lại", "P0", LV_PRE,
         "1. Gõ từ khóa và bấm Tìm kiếm\n2. Bấm nút Làm mới", "—",
         "- Ô tìm nhanh trống\n"
         "- Danh sách tự nạp lại đủ 29 dòng NGAY, không cần bấm Tìm kiếm lần nữa\n"
         "⚠️ Bẫy hay gặp: xóa chữ trong ô nhưng bảng vẫn giữ kết quả lọc cũ"),

        ("006", "Bộ lọc được nhớ khi quay lại màn trong 10 phút", "P1", LV_PRE,
         "1. Tìm theo từ khóa, bấm Tìm kiếm\n2. Sang màn khác\n3. Quay lại trong 10 phút",
         "Cấp 1",
         "- Ô tìm nhanh và kết quả vẫn giữ nguyên"),

        ("007", "Tìm kiếm xong tự về trang 1", "P1", LV_PRE + " Đang đứng ở trang 2.",
         "1. Chuyển sang trang 2\n2. Gõ từ khóa và bấm Tìm kiếm", "Cấp",
         "- Kết quả hiển thị từ trang 1, không hiện bảng trống"),

        ("008", "Tìm nhanh với chuỗi có khoảng trắng thừa", "P2", LV_PRE,
         "1. Gõ \"  Cấp 1  \"\n2. Bấm Tìm kiếm", "  Cấp 1  ",
         "- Vẫn tìm ra kết quả, không báo không có dữ liệu"),

        ("009", "Tìm nhanh với ký tự đặc biệt", "P2", LV_PRE,
         "1. Gõ chuỗi \"%'\" vào ô tìm nhanh\n2. Bấm Tìm kiếm", "%'",
         "- Màn hình không lỗi, không trắng trang; kết quả rỗng hoặc khớp đúng nghĩa đen"),
    ]),

    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", [
        ("001", "Sắp xếp theo Tên cấp", "P0", LV_PRE,
         "1. Bấm tiêu đề cột Tên cấp 1 lần rồi 2 lần", "—",
         "- Lần 1 xếp tăng dần, lần 2 xếp giảm dần; mũi tên đổi chiều\n"
         "- Thứ tự các dòng thực sự thay đổi"),

        ("002", "Sắp xếp theo Cập nhật", "P1", LV_PRE,
         "1. Bấm tiêu đề cột Cập nhật", "—",
         "- Danh sách xếp theo ngày giờ cập nhật, thứ tự thực sự thay đổi"),

        ("003", "Cột STT và Hành động không sắp xếp được", "P2", LV_PRE,
         "1. Bấm tiêu đề cột STT rồi cột Hành động", "—",
         "- Không có mũi tên sắp xếp, bấm vào không đổi thứ tự và không lỗi"),

        ("004", "Sắp xếp giữ nguyên khi chuyển trang", "P1", LV_PRE + " Cỡ trang 10 nên có 3 trang.",
         "1. Sắp xếp theo Tên cấp giảm dần\n2. Chuyển sang trang 2", "—",
         "- Trang 2 tiếp nối đúng thứ tự đã sắp"),

        ("005", "Chuyển trang bằng nút số trang", "P0", LV_PRE + " Cỡ trang 10, có 3 trang.",
         "1. Bấm số trang 2", "—",
         "- Bảng hiện dữ liệu trang 2, cột STT bắt đầu từ 11\n"
         "- Dòng Hiển thị dưới bảng cập nhật đúng"),

        ("006", "Đổi cỡ trang", "P0", LV_PRE,
         "1. Đổi cỡ trang từ 10 sang 50", "Cỡ trang: 50",
         "- Toàn bộ 29 dòng hiện trên 1 trang\n- Danh sách chỉ nạp lại đúng một lần"),

        ("007", "Đổi cỡ trang khi đang ở trang cuối", "P1", LV_PRE + " Đang ở trang 3.",
         "1. Đổi cỡ trang sang 50", "Cỡ trang: 50",
         "- Bảng hiện dữ liệu từ trang 1, KHÔNG hiện bảng trống"),

        ("008", "Vào màn hình chỉ gọi dữ liệu một lần", "P1", LV_PRE,
         "1. Mở màn hình từ menu\n2. Quan sát hiệu ứng tải của bảng", "—",
         "- Bảng chỉ tải một lượt, không chớp tải hai lần"),
    ]),

    ("IV", "THÊM / SỬA / XEM CẤP DỊCH VỤ", [
        ("001", "Mở cửa sổ Thêm cấp dịch vụ", "P0", LV_PRE,
         "1. Bấm nút Tạo mới", "—",
         "- Mở cửa sổ tiêu đề \"Thêm cấp dịch vụ\"\n"
         "- Chỉ có 1 ô nhập: Tên cấp (bắt buộc, có dấu sao đỏ)\n"
         "- Cuối cửa sổ có 3 nút: Lưu, Lưu & Tiếp tục, Đóng"),

        ("002", "Thêm mới cấp dịch vụ", "P0", LV_PRE,
         "1. Bấm Tạo mới\n2. Nhập Tên cấp\n3. Bấm Lưu", "Tên cấp: Cấp kiểm thử",
         "- Thông báo thêm mới thành công\n"
         "- Cửa sổ đóng, danh sách nạp lại và có dòng \"Cấp kiểm thử\""),

        ("003", "Mở cửa sổ Sửa nạp đúng dữ liệu cũ", "P0", LV_PRE,
         "1. Bấm nút Sửa trên dòng \"Cấp kiểm thử\"", "—",
         "- Tiêu đề cửa sổ là \"Sửa cấp dịch vụ\"\n- Ô Tên cấp điền sẵn đúng tên đang có"),

        ("004", "Sửa Tên cấp", "P0", LV_PRE,
         "1. Bấm Sửa dòng \"Cấp kiểm thử\"\n2. Đổi Tên cấp\n3. Bấm Lưu",
         "Tên cấp: Cấp kiểm thử (đã sửa)",
         "- Thông báo cập nhật thành công\n"
         "- Danh sách hiện tên mới, cột Cập nhật đổi sang thời điểm vừa sửa"),

        ("005", "Sửa được cấp đang được sử dụng", "P1", LV_PRE,
         "1. Bấm Sửa dòng \"Cấp 1\" (đang được dùng ở nhiều chứng từ)\n2. Đổi tên\n3. Bấm Lưu",
         "Tên cấp: Cấp 1 - đổi tên",
         "- Lưu thành công\n"
         "- Các chứng từ đang dùng cấp này hiện tên MỚI\n"
         "⚠️ Đang được dùng chỉ chặn XÓA, không chặn SỬA"),

        ("006", "Nút Xem mở ở chế độ chỉ đọc", "P0", LV_PRE,
         "1. Bấm nút Xem trên một dòng bất kỳ", "—",
         "- Tiêu đề cửa sổ là \"Xem cấp dịch vụ\"\n"
         "- Ô Tên cấp mờ, không gõ được\n- KHÔNG có nút Lưu, chỉ có nút Đóng"),

        ("007", "Bấm Đóng khi chưa sửa gì", "P1", LV_PRE,
         "1. Bấm Sửa một dòng\n2. Không đổi gì\n3. Bấm Đóng", "—",
         "- Cửa sổ đóng ngay, không hỏi lại; danh sách giữ nguyên"),

        ("008", "Cảnh báo khi đóng lúc đang sửa dở", "P0", LV_PRE,
         "1. Bấm Sửa một dòng\n2. Đổi Tên cấp nhưng chưa Lưu\n3. Bấm Đóng", "Tên: sửa dở dang",
         "- Hệ thống cảnh báo dữ liệu chưa lưu và hỏi xác nhận\n"
         "- Chọn ở lại thì cửa sổ vẫn mở và giữ nguyên nội dung đang gõ\n"
         "- Chọn thoát thì dữ liệu cũ không bị đổi"),

        ("009", "Đóng cửa sổ bằng dấu X góc phải", "P1", LV_PRE,
         "1. Bấm Tạo mới\n2. Nhập tên\n3. Bấm dấu X ở góc trên bên phải", "Tên: ABC",
         "- Hành xử giống nút Đóng: có cảnh báo chưa lưu"),

        ("010", "Chống bấm Lưu nhiều lần liên tiếp", "P1", LV_PRE,
         "1. Bấm Tạo mới, nhập tên\n2. Bấm Lưu liên tiếp 3 lần thật nhanh", "Tên: Cấp thử 9",
         "- Chỉ tạo ra ĐÚNG 1 bản ghi\n- Nút Lưu bị vô hiệu trong lúc xử lý"),

        ("011", "Cấp mới dùng được ngay ở gói bảo dưỡng", "P0", LV_PRE,
         "1. Tạo mới cấp \"Cấp kiểm thử\"\n2. Mở màn Danh mục gói bảo dưỡng, tạo mới một gói\n"
         "3. Mở danh sách chọn cấp dịch vụ", "Tên cấp: Cấp kiểm thử",
         "- \"Cấp kiểm thử\" có trong danh sách chọn và chọn được"),
    ]),

    ("V", "XÓA", [
        ("001", "Xóa cấp dịch vụ chưa dùng ở đâu", "P0", LV_PRE,
         "1. Bấm nút Xóa trên dòng \"Cấp thử\"\n2. Đọc hộp xác nhận\n3. Bấm Xóa", "Cấp thử",
         "- Hộp xác nhận tiêu đề \"Xác nhận xóa\", câu hỏi nêu đúng tên cấp\n"
         "- Thông báo \"Xóa thành công\"\n- Dòng biến mất, tổng dưới bảng giảm 1"),

        ("002", "Hủy hộp xác nhận xóa", "P0", LV_PRE,
         "1. Bấm nút Xóa trên dòng \"Cấp thử\"\n2. Bấm Hủy", "Cấp thử",
         "- Hộp đóng, dòng vẫn còn nguyên"),

        ("003", "Không xóa được cấp đang dùng ở gói bảo dưỡng", "P0",
         LV_PRE + " Cấp \"Cấp 1\" đang được dùng ở gói bảo dưỡng.",
         "1. Bấm nút Xóa trên dòng \"Cấp 1\"", "Cấp 1",
         "- Hệ thống chặn, hiện thông báo nêu tên nơi đang dùng, trong đó có \"Gói bảo dưỡng\"\n"
         "- Không mở hộp xác nhận, dòng vẫn còn"),

        ("004", "Không xóa được cấp đang dùng ở hợp đồng dịch vụ", "P0",
         "Cấp \"Cấp HĐ\" KHÔNG nằm trong gói bảo dưỡng nào nhưng đang được dùng ở 1 hợp đồng dịch vụ.",
         "1. Bấm nút Xóa trên dòng \"Cấp HĐ\"", "Cấp HĐ",
         "- Hệ thống chặn, thông báo nêu \"Hợp đồng dịch vụ\"\n"
         "⚠️ Đây là trường hợp hệ thống cũ KHÔNG chặn — xóa được và làm hỏng hợp đồng. "
         "Bắt buộc phải kiểm"),

        ("005", "Không xóa được cấp đang dùng ở báo giá dịch vụ", "P0",
         "Cấp \"Cấp BG\" chỉ được dùng ở 1 báo giá dịch vụ, không nằm ở gói bảo dưỡng nào.",
         "1. Bấm nút Xóa trên dòng \"Cấp BG\"", "Cấp BG",
         "- Hệ thống chặn, thông báo nêu \"Báo giá dịch vụ\"\n"
         "⚠️ Trường hợp hệ thống cũ không chặn"),

        ("006", "Không xóa được cấp đang dùng ở phiếu phân công công việc", "P0",
         "Cấp \"Cấp PC\" chỉ được dùng ở 1 phiếu phân công công việc.",
         "1. Bấm nút Xóa trên dòng \"Cấp PC\"", "Cấp PC",
         "- Hệ thống chặn, thông báo nêu \"Phiếu phân công công việc\"\n"
         "⚠️ Trường hợp hệ thống cũ không chặn"),

        ("007", "Không xóa được cấp đang dùng ở phiếu nhập kết quả", "P0",
         "Cấp \"Cấp NKQ\" chỉ được dùng ở 1 phiếu nhập kết quả.",
         "1. Bấm nút Xóa trên dòng \"Cấp NKQ\"", "Cấp NKQ",
         "- Hệ thống chặn, thông báo nêu \"Phiếu nhập kết quả\"\n"
         "⚠️ Trường hợp hệ thống cũ không chặn"),

        ("008", "Thông báo chặn xóa nêu tối đa 3 nơi", "P1",
         "Cấp \"Cấp 1\" đang được dùng ở cả 5 loại chứng từ.",
         "1. Bấm nút Xóa trên dòng \"Cấp 1\"\n2. Đọc kỹ nội dung thông báo", "Cấp 1",
         "- Thông báo nêu tối đa 3 nơi bằng tên nghiệp vụ tiếng Việt dễ hiểu\n"
         "- Không liệt kê dài dòng, không hiện tên kỹ thuật khó hiểu"),

        ("009", "Chặn xóa khi bỏ qua giao diện", "P0", LV_PRE,
         "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa cấp \"Cấp 1\"\n2. Mở lại màn hình",
         "Cấp 1 (đang được dùng)",
         "- Hệ thống chặn, nêu lý do đang được sử dụng\n- Dòng vẫn còn\n"
         "⚠️ Không được dựa vào giao diện để bảo vệ dữ liệu"),

        ("010", "Xóa cấp vừa bị người khác đưa vào chứng từ", "P1",
         "Hai người cùng thao tác. Cấp \"Cấp thử\" ban đầu chưa dùng ở đâu.",
         "1. Người 1 mở màn hình\n2. Người 2 lập báo giá dịch vụ dùng \"Cấp thử\"\n"
         "3. Người 1 bấm Xóa dòng \"Cấp thử\" và xác nhận", "Cấp thử",
         "- Hệ thống chặn lại, báo cấp đang được sử dụng\n- Dòng vẫn còn\n"
         "⚠️ Kiểm tra phải được thực hiện lại tại thời điểm xóa"),

        ("011", "Xóa dòng cuối cùng của trang", "P1",
         LV_PRE + " Đang ở trang cuối, trang đó chỉ còn 1 dòng và dòng đó xóa được.",
         "1. Xóa dòng duy nhất của trang cuối", "—",
         "- Xóa thành công\n- Màn tự lùi về trang trước, KHÔNG hiện bảng trống"),

        ("012", "Người chỉ có quyền Xem không thấy nút Xóa", "P0",
         "Đăng nhập bằng tài khoản chỉ có quyền \"Xem cấp dịch vụ bảo dưỡng\".",
         "1. Mở màn hình, nhìn cột Hành động", "—",
         "- Chỉ có nút Xem, không có nút Sửa và nút Xóa"),
    ]),

    ("VI", "XUẤT EXCEL", [
        ("001", "Xuất Excel toàn bộ danh mục", "P0", LV_PRE,
         "1. Không lọc gì\n2. Bấm Xuất Excel\n3. Mở file tải về", "—",
         "- Thông báo \"Xuất Excel thành công\"\n- File mở được và có đủ 29 dòng"),

        ("002", "File Excel có đủ cột như trên màn hình", "P0", LV_PRE,
         "1. Xuất Excel\n2. Đối chiếu tiêu đề cột với bảng", "—",
         "- File có cột Tên cấp; tiêu đề cột bằng tiếng Việt giống trên màn hình"),

        ("003", "Xuất Excel theo đúng từ khóa đang tìm", "P0", LV_PRE,
         "1. Gõ \"Cấp 1\" và bấm Tìm kiếm\n2. Bấm Xuất Excel\n3. Mở file", "Cấp 1",
         "- File chỉ chứa các dòng khớp từ khóa\n"
         "⚠️ Bẫy hay gặp: file xuất toàn bộ danh mục, bỏ qua điều kiện tìm kiếm"),

        ("004", "Xuất Excel lấy đủ dữ liệu, không chỉ trang hiện tại", "P0",
         LV_PRE + " Cỡ trang 10 nên có 3 trang.",
         "1. Đứng ở trang 1\n2. Xuất Excel\n3. Đếm số dòng trong file", "—",
         "- File có đủ 29 dòng, không phải 10 dòng của trang đang xem"),

        ("005", "Xuất Excel khi kết quả rỗng", "P2", LV_PRE,
         "1. Tìm ra kết quả rỗng\n2. Bấm Xuất Excel", "khongtontai123",
         "- Không lỗi; tải về file chỉ có dòng tiêu đề hoặc báo không có dữ liệu để xuất"),

        ("006", "Người chỉ có quyền Xem vẫn xuất được Excel", "P1",
         "Đăng nhập bằng tài khoản chỉ có quyền \"Xem cấp dịch vụ bảo dưỡng\".",
         "1. Bấm Xuất Excel", "—",
         "- Xuất được bình thường, có thông báo thành công"),
    ]),

    ("VII", "RÀNG BUỘC NHẬP LIỆU", [
        ("001", "Bỏ trống Tên cấp", "P0", LV_PRE,
         "1. Bấm Tạo mới\n2. Không nhập gì\n3. Bấm Lưu", "(để trống)",
         "- Ô Tên cấp viền đỏ, hiện chữ đỏ \"Bắt buộc phải nhập\" ngay dưới ô\n"
         "- Cửa sổ không đóng, không tạo bản ghi"),

        ("002", "Nhập Tên cấp chỉ gồm khoảng trắng", "P0", LV_PRE,
         "1. Bấm Tạo mới\n2. Nhập 5 dấu cách\n3. Bấm Lưu", "\"     \"",
         "- Báo \"Bắt buộc phải nhập\", không tạo bản ghi\n"
         "⚠️ Hệ thống cắt khoảng trắng đầu cuối trước khi kiểm tra"),

        ("003", "Nhập trùng Tên cấp đã có", "P0", LV_PRE,
         "1. Bấm Tạo mới\n2. Nhập tên đã tồn tại\n3. Bấm Lưu", "Tên cấp: Cấp 1",
         "- Ô Tên cấp báo \"Tên cấp đã tồn tại\", không lưu"),

        ("004", "Nhập trùng tên nhưng khác khoảng trắng đầu cuối", "P0", LV_PRE,
         "1. Bấm Tạo mới\n2. Nhập \"  Cấp 1  \" (tên đã tồn tại kèm khoảng trắng)\n3. Bấm Lưu",
         "\"  Cấp 1  \"",
         "- Vẫn báo \"Tên cấp đã tồn tại\", không lưu\n"
         "⚠️ Không được tạo được 2 cấp mà mắt thường nhìn thấy tên giống hệt nhau"),

        ("005", "Sửa Tên cấp sang tên của cấp khác", "P0", LV_PRE,
         "1. Bấm Sửa dòng \"Cấp thử\"\n2. Đổi tên thành \"Cấp 1\"\n3. Bấm Lưu", "Tên cấp: Cấp 1",
         "- Báo \"Tên cấp đã tồn tại\", không lưu"),

        ("006", "Sửa mà giữ nguyên tên của chính nó", "P0", LV_PRE,
         "1. Bấm Sửa một dòng\n2. Giữ nguyên tên, bấm Lưu\n3. Kiểm tra danh sách", "Tên không đổi",
         "- Lưu thành công\n"
         "⚠️ Bẫy hay gặp: hệ thống coi tên của chính bản ghi đang sửa là trùng và chặn nhầm"),

        ("007", "Nhập Tên cấp dài hơn 255 ký tự", "P2", LV_PRE,
         "1. Bấm Tạo mới\n2. Dán chuỗi 300 ký tự\n3. Bấm Lưu", "Chuỗi 300 ký tự",
         "- Báo \"Tối đa 255 ký tự\", không lưu"),

        ("008", "Nhập tên có dấu tiếng Việt", "P1", LV_PRE,
         "1. Bấm Tạo mới\n2. Nhập tên có dấu đầy đủ\n3. Bấm Lưu",
         "Tên cấp: Cấp bảo dưỡng định kỳ 6 tháng",
         "- Lưu thành công, danh sách hiện đúng dấu tiếng Việt"),

        ("009", "Lỗi biến mất sau khi nhập lại đúng", "P1", LV_PRE,
         "1. Bấm Tạo mới, bấm Lưu ngay để ô báo đỏ\n2. Nhập tên hợp lệ\n3. Bấm Lưu",
         "Tên cấp: Hết lỗi",
         "- Viền đỏ và chữ đỏ biến mất khi nhập\n- Lưu thành công"),
    ]),

    ("VIII", "CÔ LẬP DỮ LIỆU & LUỒNG XUYÊN SUỐT", [
        ("001", "Hai người cùng sửa một cấp dịch vụ", "P1",
         "Hai tài khoản đều có quyền Quản lý, cùng mở cửa sổ Sửa của \"Cấp thử\".",
         "1. Người 1 đổi tên và Lưu\n2. Người 2 (đang mở với dữ liệu cũ) đổi tên khác và Lưu\n"
         "3. Nạp lại danh sách", "Hai tên khác nhau",
         "- Cả hai lưu được (hoặc người sau bị chặn nếu trùng tên)\n"
         "- Hệ thống không lỗi, không nhân đôi bản ghi"),

        ("002", "Sửa một cấp vừa bị người khác xóa", "P1",
         "Hai tài khoản đều có quyền Quản lý. Cấp \"Cấp thử\" chưa dùng ở đâu.",
         "1. Người 1 mở cửa sổ Sửa\n2. Người 2 xóa \"Cấp thử\"\n3. Người 1 bấm Lưu", "Cấp thử",
         "- Hệ thống báo dữ liệu đã thay đổi hoặc không còn tồn tại\n"
         "- Màn hình KHÔNG treo, không trắng trang"),

        ("003", "Hai người cùng tạo cấp cùng tên", "P1",
         "Hai tài khoản đều có quyền Quản lý.",
         "1. Cả hai cùng mở cửa sổ Tạo mới, nhập tên \"Cấp trùng\"\n"
         "2. Người 1 bấm Lưu\n3. Người 2 bấm Lưu", "Tên cấp: Cấp trùng",
         "- Người thứ nhất lưu thành công\n"
         "- Người thứ hai bị chặn với thông báo \"Tên cấp đã tồn tại\"\n"
         "- Danh mục chỉ có ĐÚNG 1 cấp tên \"Cấp trùng\""),

        ("004", "Danh mục dùng chung cho mọi công ty", "P1",
         "Hai người thuộc hai công ty khác nhau, đều có quyền Xem cấp dịch vụ bảo dưỡng.",
         "1. Cả hai cùng mở màn hình\n2. So sánh số dòng và nội dung", "—",
         "- Hai người thấy DANH SÁCH GIỐNG HỆT NHAU"),

        ("005", "Vòng đời đầy đủ của một cấp dịch vụ", "P0", LV_PRE,
         "1. Tạo mới cấp \"Cấp kiểm thử\"\n2. Tìm lại bằng ô tìm nhanh\n3. Sửa tên\n"
         "4. Xuất Excel kiểm tra có cấp đó\n5. Xóa cấp đó",
         "Tên cấp: Cấp kiểm thử → Cấp kiểm thử A",
         "- Từng bước có thông báo thành công tương ứng\n"
         "- Sau bước 5, cấp đó không còn trong danh sách và không còn trong file Excel xuất lại"),

        ("006", "Không xóa được sau khi đưa vào sử dụng", "P0", LV_PRE,
         "1. Tạo mới cấp \"Cấp kiểm thử\"\n2. Lập một báo giá dịch vụ dùng cấp đó\n"
         "3. Quay lại màn hình và bấm Xóa cấp đó", "Cấp kiểm thử",
         "- Bước 3 bị chặn với thông báo nêu \"Báo giá dịch vụ\"\n- Cấp vẫn còn trong danh mục"),

        ("007", "Kiểm tra nhất quán giữa hai cổng", "P1", LV_PRE,
         "1. Tạo mới cấp \"Cấp kiểm thử\" ở cổng mới\n2. Mở màn tương ứng ở cổng cũ, tìm cấp đó\n"
         "3. Sửa tên ở cổng cũ\n4. Quay lại cổng mới, nạp lại danh sách", "Cấp kiểm thử",
         "- Bước 2: cổng cũ thấy cấp vừa tạo\n- Bước 4: cổng mới hiện tên vừa sửa\n"
         "⚠️ Hai cổng dùng chung một danh mục, mọi sai lệch đều là lỗi"),
    ]),
]

build(output_file=os.path.join(HERE, "testcase - Cap dich vu bao duong.xlsx"),
      sheet_name=SHEET_NAME,
      feature_name="Cấp dịch vụ bảo dưỡng - Cập nhật ngày 13/08/2026",
      module_name="Cấp dịch vụ bảo dưỡng",
      description_block=LV_DESC, role_tcs=LV_ROLE, sections=LV_SECTIONS)

print("-" * 70)

# ############################################################################
# MAN 2 — DANH MUC GHI CHU KIEM TRA BAO DUONG
# ############################################################################
NM_DESC = [
    ("1. Mục đích tính năng",
     "Quản lý danh sách các hạng mục ghi chú khi kiểm tra bảo dưỡng (ví dụ "
     "\"Kiểm tra ngoại quan không tháo lắp\"). Mỗi hạng mục có một ký hiệu viết tắt để nhân viên "
     "kỹ thuật ghi nhanh trên phiếu.\n"
     "Màn hình nằm ở phân hệ Chăm sóc khách hàng → nhóm menu Danh mục - Dịch vụ → "
     "Danh mục ghi chú kiểm tra bảo dưỡng.\n"
     "Đây là màn được chuyển từ hệ thống cũ sang, hai cổng dùng CHUNG một danh mục."),

    ("2. Đối tượng được tính / hiển thị",
     "- Toàn bộ ghi chú kiểm tra trong danh mục, KHÔNG phân theo công ty / phòng ban.\n"
     "- Mỗi dòng gồm 6 cột: STT, Hạng mục, Ký hiệu, Mô tả, Cập nhật, Hành động.\n"
     "- Danh mục hiện có khoảng 11 ghi chú."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Không có ghi chú nào bị ẩn. Màn này KHÔNG có trạng thái Hoạt động / Khóa — "
     "chỉ có thêm, sửa, xóa.\n"
     "- Khi tìm kiếm, các ghi chú không khớp bị loại khỏi kết quả."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Không áp dụng. Màn hình không có bộ lọc theo khoảng thời gian.\n"
     "Cột Cập nhật chỉ để xem và để sắp xếp."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Danh sách phẳng, không phân cấp cha - con.\n"
     "Cả Hạng mục và Ký hiệu đều là giá trị duy nhất trong danh mục.\n"
     "Quan hệ với màn khác: ghi chú được gắn vào cấp bảo dưỡng của gói dịch vụ — "
     "đây là căn cứ chặn xóa."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "Không cộng dồn. Mỗi ghi chú là một dòng độc lập.\n"
     "Chống trùng: trùng Hạng mục báo \"Hạng mục đã tồn tại\"; trùng Ký hiệu báo "
     "\"Ký hiệu đã tồn tại\". Mô tả KHÔNG bắt buộc duy nhất."),

    ("7. Phân quyền cấp",
     "Hai quyền dành riêng cho màn này:\n"
     "- \"Xem ghi chú kiểm tra bảo dưỡng\": vào màn hình, xem danh sách, mở xem chi tiết, "
     "xuất Excel.\n"
     "- \"Quản lý ghi chú kiểm tra bảo dưỡng\": thêm mới, sửa, xóa.\n"
     "Không có quyền nào trong hai quyền trên thì không vào được màn hình.\n"
     "Danh mục KHÔNG phân quyền theo công ty / phòng ban / bộ phận."),

    ("8. Cách tính các ô thống kê",
     "- Dòng \"Hiển thị a - b / N\" dưới bảng: a là dòng đầu của trang đang xem, b là dòng cuối, "
     "N là tổng số ghi chú khớp bộ lọc hiện tại.\n"
     "- Cột STT đánh theo trang: trang 2 với cỡ trang 10 thì bắt đầu từ 11."),

    ("9. Ghi chú đọc bảng",
     "- Màn này KHÔNG có trạng thái Khóa / Mở khóa — chỉ Thêm, Sửa, Xóa.\n"
     "- Ghi chú đang được gắn vào cấp bảo dưỡng của gói dịch vụ thì KHÔNG xóa được. "
     "Rê chuột vào nút Xóa để đọc lý do.\n"
     "⚠️ Ở hệ thống cũ, màn này KHÔNG chặn xóa gì cả, dù phần lớn ghi chú đang được sử dụng — "
     "xóa xong là các gói dịch vụ mất ghi chú. Bản mới đã chặn. Đây là nhóm bắt buộc kiểm kỹ.\n"
     "- Ở hệ thống cũ, thêm và sửa mở ra TRANG RIÊNG; bản mới đưa về cửa sổ nhỏ cho đồng bộ với "
     "các danh mục khác. Đây là thay đổi có chủ ý, không phải lỗi.\n"
     "- Cột Mô tả có thể dài, được xuống dòng trong ô, không cắt cụt.\n"
     "- Bộ lọc được ghi nhớ trong 10 phút; kiểm thử tìm kiếm nên bấm Làm mới trước mỗi kịch bản."),
]

NM_PRE_PERM = ("Có sẵn 2 tài khoản: A chỉ có quyền \"Xem ghi chú kiểm tra bảo dưỡng\"; "
               "B có quyền \"Quản lý ghi chú kiểm tra bảo dưỡng\". Danh mục có 11 ghi chú, "
               "trong đó 9 ghi chú đang được gắn vào cấp bảo dưỡng của gói dịch vụ, "
               "ghi chú \"Ghi chú thử\" chưa dùng ở đâu.")

NM_ROLE = [
    ("01", "Vào màn hình khi chỉ có quyền Xem", "P0", NM_PRE_PERM,
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Vào phân hệ Chăm sóc khách hàng → Danh mục - Dịch vụ → "
     "Danh mục ghi chú kiểm tra bảo dưỡng", "Tài khoản A",
     "- Vào được màn hình, bảng hiển thị đủ 11 ghi chú\n"
     "- KHÔNG có nút Tạo mới\n"
     "- Mỗi dòng chỉ có nút Xem; KHÔNG có nút Sửa, nút Xóa\n- Vẫn có nút Xuất Excel"),

    ("02", "Vào màn hình khi có quyền Quản lý", "P0", NM_PRE_PERM,
     "1. Đăng nhập bằng tài khoản B\n2. Vào Danh mục ghi chú kiểm tra bảo dưỡng", "Tài khoản B",
     "- Có nút Tạo mới và nút Xuất Excel\n- Mỗi dòng có đủ 3 nút: Xem, Sửa, Xóa"),

    ("03", "Chặn vào màn hình khi không có quyền nào", "P0",
     "Tài khoản C không có cả hai quyền của màn này.",
     "1. Đăng nhập bằng tài khoản C\n2. Tìm mục này trong phân hệ Chăm sóc khách hàng\n"
     "3. Dán thẳng đường dẫn màn hình vào thanh địa chỉ", "Tài khoản C",
     "- Mục menu KHÔNG hiện\n"
     "- Dán thẳng đường dẫn thì chuyển sang trang báo không tìm thấy, không lộ dữ liệu"),

    ("04", "Chặn Thêm mới khi bỏ qua giao diện", "P0", NM_PRE_PERM,
     "1. Đăng nhập bằng tài khoản A, lấy mã đăng nhập\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Thêm ghi chú kiểm tra\n3. Mở lại màn hình",
     "Hạng mục: Ghi chú trộm; Ký hiệu: GCT",
     "- Hệ thống từ chối, báo không có quyền\n- Danh sách vẫn 11 dòng"),

    ("05", "Chặn Sửa khi bỏ qua giao diện", "P0", NM_PRE_PERM,
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Sửa một ghi chú\n3. Mở lại màn hình",
     "Đổi hạng mục thành \"Bị sửa trộm\"",
     "- Hệ thống từ chối, báo không có quyền\n- Nội dung cũ giữ nguyên"),

    ("06", "Chặn Xóa khi bỏ qua giao diện", "P0", NM_PRE_PERM,
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa \"Ghi chú thử\"\n3. Mở lại màn hình",
     "Ghi chú thử (về nghiệp vụ là xóa được)",
     "- Hệ thống từ chối, báo không có quyền\n- Ghi chú thử vẫn còn"),

    ("07", "Người có quyền Quản lý làm được trọn vòng đời", "P1", NM_PRE_PERM,
     "1. Đăng nhập bằng tài khoản B\n2. Tạo mới 1 ghi chú\n3. Sửa ghi chú vừa tạo\n4. Xóa ghi chú đó",
     "Hạng mục: Ghi chú kiểm thử; Ký hiệu: GCKT",
     "- Cả 3 thao tác đều thực hiện được kèm thông báo thành công\n"
     "- Sau bước 4, ghi chú đó không còn trong danh sách"),
]

NM_PRE = ("Đăng nhập bằng tài khoản có quyền \"Quản lý ghi chú kiểm tra bảo dưỡng\". "
          "Danh mục có 11 ghi chú, 9 trong số đó đang được gắn vào cấp bảo dưỡng của gói dịch vụ; "
          "\"Ghi chú thử\" chưa dùng ở đâu; có ít nhất 1 ghi chú có Mô tả dài trên 100 ký tự và "
          "1 ghi chú bỏ trống Mô tả.")

NM_SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", [
        ("001", "Mở màn hình lần đầu", "P0", NM_PRE,
         "1. Vào phân hệ Chăm sóc khách hàng → Danh mục - Dịch vụ → "
         "Danh mục ghi chú kiểm tra bảo dưỡng\n2. Quan sát toàn màn hình", "—",
         "- Tiêu đề trang và tiêu đề bảng đều là \"Danh mục ghi chú kiểm tra bảo dưỡng\"\n"
         "- Khối lọc có tiêu đề \"Bộ lọc ghi chú kiểm tra bảo dưỡng\" và dòng phụ "
         "\"Tìm kiếm theo hạng mục hoặc ký hiệu\"\n"
         "- Bảng có đủ 6 cột: STT, Hạng mục, Ký hiệu, Mô tả, Cập nhật, Hành động\n"
         "- Dưới bảng có nút Tạo mới và nút Xuất Excel"),

        ("002", "Hiển thị đủ 11 bản ghi khi chưa lọc", "P0", NM_PRE,
         "1. Mở màn hình\n2. Đọc dòng Hiển thị dưới bảng", "—",
         "- Tổng hiển thị là 11"),

        ("003", "Cột Mô tả xuống dòng khi nội dung dài", "P1", NM_PRE,
         "1. Mở màn hình\n2. Nhìn dòng có Mô tả dài trên 100 ký tự", "—",
         "- Nội dung được xuống dòng trong ô, hiện đầy đủ\n"
         "- Không cắt cụt bằng dấu ba chấm, không tràn ra ngoài bảng"),

        ("004", "Ghi chú không có Mô tả", "P2", NM_PRE,
         "1. Mở màn hình\n2. Nhìn dòng bỏ trống Mô tả", "—",
         "- Ô Mô tả để trống hoặc hiện dấu gạch ngang, không lỗi"),

        ("005", "Màn hình không có cột Trạng thái", "P1", NM_PRE,
         "1. Mở màn hình\n2. Đối chiếu các cột của bảng", "—",
         "- KHÔNG có cột Trạng thái, KHÔNG có nút Khóa / Mở khóa"),

        ("006", "Bảng trống khi tìm không khớp gì", "P1", NM_PRE,
         "1. Gõ \"khongtontai123\" vào ô tìm nhanh\n2. Bấm Tìm kiếm", "khongtontai123",
         "- Bảng hiện thông báo không có dữ liệu phù hợp, tổng dưới bảng là 0"),
    ]),

    ("II", "BỘ LỌC & TÌM KIẾM", [
        ("001", "Tìm nhanh theo Hạng mục", "P0", NM_PRE,
         "1. Gõ \"ngoại quan\" vào ô tìm nhanh\n2. Bấm Tìm kiếm", "ngoại quan",
         "- Kết quả gồm mọi ghi chú có chuỗi đó trong Hạng mục\n"
         "⚠️ Gợi ý trong ô ghi rõ: \"Tìm theo hạng mục hoặc ký hiệu...\""),

        ("002", "Tìm nhanh theo Ký hiệu", "P0", NM_PRE,
         "1. Gõ ký hiệu của một ghi chú (ví dụ \"KTBM\")\n2. Bấm Tìm kiếm", "KTBM",
         "- Ghi chú tương ứng ra kết quả dù chuỗi tìm chỉ nằm ở Ký hiệu"),

        ("003", "Tìm nhanh khớp một phần chuỗi", "P0", NM_PRE,
         "1. Gõ 2 ký tự đầu của một ký hiệu\n2. Bấm Tìm kiếm", "KT",
         "- Mọi ký hiệu bắt đầu bằng KT đều ra kết quả"),

        ("004", "Tìm nhanh không phân biệt hoa thường", "P1", NM_PRE,
         "1. Gõ ký hiệu bằng chữ thường\n2. Bấm Tìm kiếm", "ktbm",
         "- Kết quả giống hệt khi gõ chữ hoa"),

        ("005", "Tìm nhanh KHÔNG quét cột Mô tả", "P1", NM_PRE,
         "1. Gõ một chuỗi CHỈ xuất hiện trong cột Mô tả, không có trong Hạng mục và Ký hiệu\n"
         "2. Bấm Tìm kiếm", "chuỗi chỉ có trong Mô tả",
         "- Kết quả rỗng\n"
         "⚠️ Đây là hành vi đúng theo thiết kế: ô tìm nhanh chỉ quét Hạng mục và Ký hiệu"),

        ("006", "Gõ ô tìm nhanh mà chưa bấm Tìm kiếm", "P1", NM_PRE,
         "1. Gõ từ khóa\n2. Chờ 5 giây, không bấm gì", "KTBM",
         "- Bảng vẫn giữ nguyên 11 dòng, chưa lọc"),

        ("007", "Nút Làm mới xóa điều kiện và nạp lại", "P0", NM_PRE,
         "1. Gõ từ khóa và bấm Tìm kiếm\n2. Bấm nút Làm mới", "—",
         "- Ô tìm nhanh trống\n"
         "- Danh sách tự nạp lại đủ 11 dòng NGAY, không cần bấm Tìm kiếm lần nữa"),

        ("008", "Bộ lọc được nhớ khi quay lại màn trong 10 phút", "P1", NM_PRE,
         "1. Tìm theo từ khóa, bấm Tìm kiếm\n2. Sang màn khác\n3. Quay lại trong 10 phút", "KTBM",
         "- Ô tìm nhanh và kết quả vẫn giữ nguyên"),

        ("009", "Tìm kiếm xong tự về trang 1", "P1", NM_PRE + " Đang đứng ở trang 2.",
         "1. Chuyển sang trang 2\n2. Gõ từ khóa và bấm Tìm kiếm", "KT",
         "- Kết quả hiển thị từ trang 1, không hiện bảng trống"),

        ("010", "Tìm nhanh với ký tự đặc biệt", "P2", NM_PRE,
         "1. Gõ chuỗi \"%'\" vào ô tìm nhanh\n2. Bấm Tìm kiếm", "%'",
         "- Màn hình không lỗi, không trắng trang"),
    ]),

    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", [
        ("001", "Sắp xếp theo Hạng mục", "P0", NM_PRE,
         "1. Bấm tiêu đề cột Hạng mục 1 lần rồi 2 lần", "—",
         "- Lần 1 xếp tăng dần, lần 2 xếp giảm dần; thứ tự thực sự thay đổi"),

        ("002", "Sắp xếp theo Ký hiệu", "P0", NM_PRE,
         "1. Bấm tiêu đề cột Ký hiệu", "—",
         "- Danh sách xếp theo ký hiệu, thứ tự thực sự thay đổi"),

        ("003", "Sắp xếp theo Cập nhật", "P1", NM_PRE,
         "1. Bấm tiêu đề cột Cập nhật", "—",
         "- Danh sách xếp theo ngày giờ cập nhật"),

        ("004", "Cột Mô tả, STT và Hành động không sắp xếp được", "P2", NM_PRE,
         "1. Bấm tiêu đề các cột này", "—",
         "- Không có mũi tên sắp xếp, bấm vào không đổi thứ tự và không lỗi"),

        ("005", "Chuyển trang bằng nút số trang", "P0", NM_PRE + " Cỡ trang 10 nên có 2 trang.",
         "1. Bấm số trang 2", "—",
         "- Bảng hiện dòng thứ 11, cột STT bắt đầu từ 11\n"
         "- Dòng Hiển thị dưới bảng cập nhật đúng"),

        ("006", "Đổi cỡ trang", "P0", NM_PRE,
         "1. Đổi cỡ trang từ 10 sang 50", "Cỡ trang: 50",
         "- Toàn bộ 11 dòng hiện trên 1 trang\n- Danh sách chỉ nạp lại đúng một lần"),

        ("007", "Đổi cỡ trang khi đang ở trang cuối", "P1", NM_PRE + " Đang ở trang 2.",
         "1. Đổi cỡ trang sang 50", "Cỡ trang: 50",
         "- Bảng hiện dữ liệu từ trang 1, KHÔNG hiện bảng trống"),

        ("008", "Vào màn hình chỉ gọi dữ liệu một lần", "P1", NM_PRE,
         "1. Mở màn hình từ menu\n2. Quan sát hiệu ứng tải của bảng", "—",
         "- Bảng chỉ tải một lượt, không chớp tải hai lần"),
    ]),

    ("IV", "THÊM / SỬA / XEM GHI CHÚ", [
        ("001", "Mở cửa sổ Thêm ghi chú kiểm tra", "P0", NM_PRE,
         "1. Bấm nút Tạo mới", "—",
         "- Mở CỬA SỔ NHỎ tiêu đề \"Thêm ghi chú kiểm tra\", không phải trang riêng\n"
         "- Có 3 ô: Hạng mục (bắt buộc), Ký hiệu (bắt buộc), Mô tả\n"
         "- Hai ô bắt buộc có dấu sao đỏ bên cạnh nhãn\n"
         "- Cuối cửa sổ có 3 nút: Lưu, Lưu & Tiếp tục, Đóng"),

        ("002", "Thêm mới đầy đủ thông tin", "P0", NM_PRE,
         "1. Bấm Tạo mới\n2. Nhập đủ 3 ô\n3. Bấm Lưu",
         "Hạng mục: Kiểm tra kiểm thử; Ký hiệu: KTKT; Mô tả: Mô tả kiểm thử",
         "- Thông báo thêm mới thành công\n"
         "- Cửa sổ đóng, danh sách nạp lại và có dòng mới với đủ 3 giá trị vừa nhập"),

        ("003", "Thêm mới chỉ nhập các ô bắt buộc", "P0", NM_PRE,
         "1. Bấm Tạo mới\n2. Chỉ nhập Hạng mục và Ký hiệu\n3. Bấm Lưu",
         "Hạng mục: Kiểm thử 2; Ký hiệu: KT2",
         "- Lưu thành công\n- Cột Mô tả của dòng mới để trống"),

        ("004", "Mở cửa sổ Sửa nạp đúng dữ liệu cũ", "P0", NM_PRE,
         "1. Bấm nút Sửa trên một dòng", "—",
         "- Tiêu đề cửa sổ là \"Sửa ghi chú kiểm tra\"\n"
         "- Cả 3 ô điền sẵn đúng dữ liệu đang có"),

        ("005", "Sửa Hạng mục", "P0", NM_PRE,
         "1. Bấm Sửa dòng \"Kiểm tra kiểm thử\"\n2. Đổi Hạng mục\n3. Bấm Lưu",
         "Hạng mục: Kiểm tra kiểm thử (đã sửa)",
         "- Thông báo cập nhật thành công\n"
         "- Danh sách hiện nội dung mới, cột Cập nhật đổi sang thời điểm vừa sửa"),

        ("006", "Sửa Ký hiệu", "P0", NM_PRE,
         "1. Bấm Sửa một dòng\n2. Đổi Ký hiệu\n3. Bấm Lưu", "Ký hiệu: KTX",
         "- Cập nhật thành công, cột Ký hiệu hiện giá trị mới"),

        ("007", "Xóa trắng Mô tả đang có", "P1", NM_PRE,
         "1. Bấm Sửa dòng có Mô tả\n2. Xóa trắng ô Mô tả\n3. Bấm Lưu", "Mô tả: (để trống)",
         "- Cập nhật thành công, cột Mô tả thành trống"),

        ("008", "Sửa được ghi chú đang được sử dụng", "P1", NM_PRE,
         "1. Bấm Sửa một dòng đang được gắn vào cấp bảo dưỡng của gói dịch vụ\n"
         "2. Đổi Hạng mục\n3. Bấm Lưu", "Hạng mục mới",
         "- Lưu thành công\n"
         "- Các gói dịch vụ đang dùng ghi chú này hiện nội dung MỚI\n"
         "⚠️ Đang được dùng chỉ chặn XÓA, không chặn SỬA"),

        ("009", "Nút Xem mở ở chế độ chỉ đọc", "P0", NM_PRE,
         "1. Bấm nút Xem trên một dòng bất kỳ", "—",
         "- Tiêu đề cửa sổ là \"Xem ghi chú kiểm tra\"\n"
         "- Cả 3 ô đều mờ, không gõ được\n- KHÔNG có nút Lưu, chỉ có nút Đóng"),

        ("010", "Bấm Đóng khi chưa sửa gì", "P1", NM_PRE,
         "1. Bấm Sửa một dòng\n2. Không đổi gì\n3. Bấm Đóng", "—",
         "- Cửa sổ đóng ngay, không hỏi lại"),

        ("011", "Cảnh báo khi đóng lúc đang sửa dở", "P0", NM_PRE,
         "1. Bấm Sửa một dòng\n2. Đổi Hạng mục nhưng chưa Lưu\n3. Bấm Đóng",
         "Hạng mục: sửa dở dang",
         "- Hệ thống cảnh báo dữ liệu chưa lưu và hỏi xác nhận\n"
         "- Chọn ở lại thì cửa sổ vẫn mở và giữ nguyên nội dung đang gõ"),

        ("012", "Chống bấm Lưu nhiều lần liên tiếp", "P1", NM_PRE,
         "1. Bấm Tạo mới, nhập đủ\n2. Bấm Lưu liên tiếp 3 lần thật nhanh",
         "Hạng mục: Kiểm thử 9; Ký hiệu: KT9",
         "- Chỉ tạo ra ĐÚNG 1 bản ghi\n- Nút Lưu bị vô hiệu trong lúc xử lý"),

        ("013", "Ghi chú mới dùng được ngay ở gói bảo dưỡng", "P0", NM_PRE,
         "1. Tạo mới ghi chú \"Kiểm tra kiểm thử\"\n"
         "2. Mở màn Danh mục gói bảo dưỡng, vào phần cấp bảo dưỡng\n"
         "3. Mở danh sách chọn ghi chú kiểm tra", "Hạng mục: Kiểm tra kiểm thử",
         "- Ghi chú vừa tạo có trong danh sách chọn và chọn được"),
    ]),

    ("V", "XÓA", [
        ("001", "Xóa ghi chú chưa dùng ở đâu", "P0", NM_PRE,
         "1. Bấm nút Xóa trên dòng \"Ghi chú thử\"\n2. Đọc hộp xác nhận\n3. Bấm Xóa", "Ghi chú thử",
         "- Hộp xác nhận tiêu đề \"Xác nhận xóa\", câu hỏi nêu đúng tên hạng mục\n"
         "- Thông báo \"Xóa thành công\"\n- Dòng biến mất, tổng dưới bảng giảm 1"),

        ("002", "Hủy hộp xác nhận xóa", "P0", NM_PRE,
         "1. Bấm nút Xóa trên dòng \"Ghi chú thử\"\n2. Bấm Hủy", "Ghi chú thử",
         "- Hộp đóng, dòng vẫn còn nguyên"),

        ("003", "Nút Xóa bị vô hiệu với ghi chú đang được sử dụng", "P0",
         NM_PRE + " Ghi chú \"Kiểm tra ngoại quan không tháo lắp\" đang được gắn vào cấp bảo dưỡng "
         "của gói dịch vụ.",
         "1. Rê chuột vào nút Xóa của dòng đó\n2. Thử bấm", "Ghi chú đang được sử dụng",
         "- Nút Xóa bị mờ, không bấm được\n"
         "- Rê chuột hiện chú thích \"Ghi chú đang được sử dụng ở nghiệp vụ khác, không thể xóa\"\n"
         "⚠️ Hệ thống cũ KHÔNG chặn trường hợp này — xóa xong là gói dịch vụ mất ghi chú. "
         "Bắt buộc phải kiểm"),

        ("004", "Chặn xóa khi bỏ qua giao diện", "P0",
         NM_PRE + " Ghi chú đang được sử dụng ở gói dịch vụ.",
         "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa ghi chú đó\n2. Mở lại màn hình",
         "Ghi chú đang được sử dụng",
         "- Hệ thống chặn, nêu lý do đang được sử dụng\n- Dòng vẫn còn\n"
         "⚠️ Không được dựa vào việc nút bị mờ ở giao diện để bảo vệ dữ liệu"),

        ("005", "Xóa ghi chú vừa bị người khác đưa vào gói dịch vụ", "P1",
         "Hai người cùng thao tác. Ghi chú \"Ghi chú thử\" ban đầu chưa dùng ở đâu.",
         "1. Người 1 mở màn hình (nút Xóa đang sáng)\n"
         "2. Người 2 gắn ghi chú đó vào cấp bảo dưỡng của một gói dịch vụ\n"
         "3. Người 1 bấm Xóa và xác nhận", "Ghi chú thử",
         "- Hệ thống chặn lại, báo ghi chú đang được sử dụng\n- Dòng vẫn còn"),

        ("006", "Xóa dòng cuối cùng của trang", "P1",
         NM_PRE + " Đang ở trang 2, trang 2 chỉ còn 1 dòng và dòng đó xóa được.",
         "1. Xóa dòng duy nhất của trang 2", "—",
         "- Xóa thành công\n- Màn tự lùi về trang 1, KHÔNG hiện bảng trống"),

        ("007", "Người chỉ có quyền Xem không thấy nút Xóa", "P0",
         "Đăng nhập bằng tài khoản chỉ có quyền \"Xem ghi chú kiểm tra bảo dưỡng\".",
         "1. Mở màn hình, nhìn cột Hành động", "—",
         "- Chỉ có nút Xem, không có nút Sửa và nút Xóa"),
    ]),

    ("VI", "XUẤT EXCEL", [
        ("001", "Xuất Excel toàn bộ danh mục", "P0", NM_PRE,
         "1. Không lọc gì\n2. Bấm Xuất Excel\n3. Mở file tải về", "—",
         "- Thông báo \"Xuất Excel thành công\"\n- File mở được và có đủ 11 dòng"),

        ("002", "File Excel có đủ cột như trên màn hình", "P0", NM_PRE,
         "1. Xuất Excel\n2. Đối chiếu tiêu đề cột với bảng", "—",
         "- File có các cột Hạng mục, Ký hiệu, Mô tả\n"
         "- Tiêu đề cột bằng tiếng Việt giống trên màn hình"),

        ("003", "Xuất Excel theo đúng từ khóa đang tìm", "P0", NM_PRE,
         "1. Gõ \"KT\" và bấm Tìm kiếm\n2. Bấm Xuất Excel\n3. Mở file", "KT",
         "- File chỉ chứa các dòng khớp từ khóa"),

        ("004", "Xuất Excel lấy đủ dữ liệu, không chỉ trang hiện tại", "P0",
         NM_PRE + " Cỡ trang 10, có 2 trang.",
         "1. Đứng ở trang 1\n2. Xuất Excel\n3. Đếm số dòng trong file", "—",
         "- File có đủ 11 dòng, không phải 10 dòng của trang đang xem"),

        ("005", "Mô tả dài giữ nguyên trong file Excel", "P1", NM_PRE,
         "1. Xuất Excel\n2. Đối chiếu ô Mô tả của dòng có mô tả dài", "—",
         "- Nội dung mô tả đầy đủ, không bị cắt cụt"),

        ("006", "Người chỉ có quyền Xem vẫn xuất được Excel", "P1",
         "Đăng nhập bằng tài khoản chỉ có quyền \"Xem ghi chú kiểm tra bảo dưỡng\".",
         "1. Bấm Xuất Excel", "—",
         "- Xuất được bình thường, có thông báo thành công"),
    ]),

    ("VII", "RÀNG BUỘC NHẬP LIỆU", [
        ("001", "Bỏ trống cả 2 ô bắt buộc", "P0", NM_PRE,
         "1. Bấm Tạo mới\n2. Không nhập gì\n3. Bấm Lưu", "(để trống hết)",
         "- Ô Hạng mục và ô Ký hiệu viền đỏ, hiện chữ đỏ \"Bắt buộc phải nhập\" ngay dưới ô\n"
         "- Cửa sổ không đóng, không tạo bản ghi"),

        ("002", "Bỏ trống riêng Ký hiệu", "P0", NM_PRE,
         "1. Bấm Tạo mới\n2. Chỉ nhập Hạng mục\n3. Bấm Lưu", "Hạng mục: Kiểm thử",
         "- Chỉ ô Ký hiệu báo lỗi\n- Dữ liệu ở ô Hạng mục vẫn còn nguyên"),

        ("003", "Nhập trùng Hạng mục", "P0", NM_PRE,
         "1. Bấm Tạo mới\n2. Nhập Hạng mục đã tồn tại, Ký hiệu mới\n3. Bấm Lưu",
         "Hạng mục: Kiểm tra ngoại quan không tháo lắp; Ký hiệu: MOI1",
         "- Ô Hạng mục báo \"Hạng mục đã tồn tại\", không lưu"),

        ("004", "Nhập trùng Ký hiệu", "P0", NM_PRE,
         "1. Bấm Tạo mới\n2. Nhập Hạng mục mới, Ký hiệu đã tồn tại\n3. Bấm Lưu",
         "Hạng mục: Hạng mục mới; Ký hiệu: KTBM",
         "- Ô Ký hiệu báo \"Ký hiệu đã tồn tại\", không lưu"),

        ("005", "Sửa mà giữ nguyên Hạng mục và Ký hiệu của chính nó", "P0", NM_PRE,
         "1. Bấm Sửa một dòng\n2. Giữ nguyên Hạng mục và Ký hiệu, chỉ đổi Mô tả\n3. Bấm Lưu",
         "Mô tả: nội dung mới",
         "- Lưu thành công\n"
         "⚠️ Bẫy hay gặp: hệ thống coi giá trị của chính bản ghi đang sửa là trùng và chặn nhầm"),

        ("006", "Nhập Hạng mục dài hơn 255 ký tự", "P2", NM_PRE,
         "1. Bấm Tạo mới\n2. Dán chuỗi 300 ký tự vào ô Hạng mục\n3. Bấm Lưu",
         "Hạng mục: chuỗi 300 ký tự",
         "- Báo \"Tối đa 255 ký tự\", không lưu"),

        ("007", "Nhập Ký hiệu dài hơn 255 ký tự", "P2", NM_PRE,
         "1. Bấm Tạo mới\n2. Dán chuỗi 300 ký tự vào ô Ký hiệu\n3. Bấm Lưu",
         "Ký hiệu: chuỗi 300 ký tự",
         "- Báo \"Tối đa 255 ký tự\", không lưu"),

        ("008", "Nhập Mô tả dài hơn 255 ký tự", "P2", NM_PRE,
         "1. Bấm Tạo mới\n2. Dán chuỗi 300 ký tự vào ô Mô tả\n3. Bấm Lưu",
         "Mô tả: chuỗi 300 ký tự",
         "- Báo \"Tối đa 255 ký tự\", không lưu"),

        ("009", "Nhập nội dung có dấu tiếng Việt", "P1", NM_PRE,
         "1. Bấm Tạo mới\n2. Nhập Hạng mục có dấu đầy đủ\n3. Bấm Lưu",
         "Hạng mục: Kiểm tra siết lực bu lông đế máy",
         "- Lưu thành công, danh sách hiện đúng dấu tiếng Việt"),

        ("010", "Lỗi biến mất sau khi nhập lại đúng", "P1", NM_PRE,
         "1. Bấm Tạo mới, bấm Lưu ngay để 2 ô báo đỏ\n2. Nhập đủ 2 ô bắt buộc\n3. Bấm Lưu",
         "Hạng mục: Hết lỗi; Ký hiệu: HL",
         "- Viền đỏ và chữ đỏ biến mất khi nhập đủ\n- Lưu thành công"),

        ("011", "Khoảng trắng đầu cuối trong Ký hiệu", "P2", NM_PRE,
         "1. Bấm Tạo mới\n2. Nhập Ký hiệu = \"  ABC  \"\n3. Bấm Lưu và xem danh sách",
         "Ký hiệu: \"  ABC  \"",
         "- Danh sách hiện ký hiệu ABC không có khoảng trắng thừa\n"
         "- Không tạo được 2 ghi chú mà mắt thường nhìn thấy ký hiệu giống hệt nhau"),
    ]),

    ("VIII", "CÔ LẬP DỮ LIỆU & LUỒNG XUYÊN SUỐT", [
        ("001", "Hai người cùng sửa một ghi chú", "P1",
         "Hai tài khoản đều có quyền Quản lý, cùng mở cửa sổ Sửa của một ghi chú.",
         "1. Người 1 đổi Hạng mục và Lưu\n2. Người 2 (đang mở với dữ liệu cũ) đổi Mô tả và Lưu\n"
         "3. Nạp lại danh sách", "Người 1 đổi Hạng mục; Người 2 đổi Mô tả",
         "- Cả hai lưu được\n- Kết quả cuối là bản của người lưu sau; không lỗi, không nhân đôi"),

        ("002", "Sửa một ghi chú vừa bị người khác xóa", "P1",
         "Hai tài khoản đều có quyền Quản lý. Ghi chú \"Ghi chú thử\" chưa dùng ở đâu.",
         "1. Người 1 mở cửa sổ Sửa\n2. Người 2 xóa ghi chú đó\n3. Người 1 bấm Lưu", "Ghi chú thử",
         "- Hệ thống báo dữ liệu đã thay đổi hoặc không còn tồn tại\n"
         "- Màn hình KHÔNG treo, không trắng trang"),

        ("003", "Hai người cùng tạo ghi chú cùng ký hiệu", "P1",
         "Hai tài khoản đều có quyền Quản lý.",
         "1. Cả hai cùng mở cửa sổ Tạo mới, nhập Ký hiệu = \"TRUNG\"\n"
         "2. Người 1 bấm Lưu\n3. Người 2 bấm Lưu", "Ký hiệu: TRUNG (cả hai)",
         "- Người thứ nhất lưu thành công\n"
         "- Người thứ hai bị chặn với thông báo \"Ký hiệu đã tồn tại\"\n"
         "- Danh mục chỉ có ĐÚNG 1 ghi chú ký hiệu TRUNG"),

        ("004", "Danh mục dùng chung cho mọi công ty", "P1",
         "Hai người thuộc hai công ty khác nhau, đều có quyền Xem ghi chú kiểm tra bảo dưỡng.",
         "1. Cả hai cùng mở màn hình\n2. So sánh số dòng và nội dung", "—",
         "- Hai người thấy DANH SÁCH GIỐNG HỆT NHAU"),

        ("005", "Vòng đời đầy đủ của một ghi chú", "P0", NM_PRE,
         "1. Tạo mới ghi chú \"Kiểm tra kiểm thử\" (ký hiệu KTKT)\n2. Tìm lại bằng ô tìm nhanh\n"
         "3. Sửa Mô tả\n4. Xuất Excel kiểm tra có ghi chú đó\n5. Xóa ghi chú đó",
         "Hạng mục: Kiểm tra kiểm thử; Ký hiệu: KTKT",
         "- Từng bước có thông báo thành công tương ứng\n"
         "- Sau bước 5, ghi chú đó không còn trong danh sách và không còn trong file Excel xuất lại"),

        ("006", "Không xóa được sau khi đưa vào sử dụng", "P0", NM_PRE,
         "1. Tạo mới ghi chú \"Kiểm tra kiểm thử\"\n"
         "2. Gắn ghi chú đó vào cấp bảo dưỡng của một gói dịch vụ\n"
         "3. Quay lại màn hình và thử xóa ghi chú đó", "Kiểm tra kiểm thử",
         "- Nút Xóa chuyển sang mờ và không bấm được\n- Ghi chú vẫn còn trong danh mục"),

        ("007", "Kiểm tra nhất quán giữa hai cổng", "P1", NM_PRE,
         "1. Tạo mới ghi chú ở cổng mới\n2. Mở màn tương ứng ở cổng cũ, tìm ghi chú đó\n"
         "3. Sửa Mô tả ở cổng cũ\n4. Quay lại cổng mới, nạp lại danh sách", "Ký hiệu: KTKT",
         "- Bước 2: cổng cũ thấy ghi chú vừa tạo\n- Bước 4: cổng mới hiện mô tả vừa sửa\n"
         "⚠️ Hai cổng dùng chung một danh mục, mọi sai lệch đều là lỗi"),
    ]),
]

build(output_file=os.path.join(HERE, "testcase - Danh muc ghi chu kiem tra bao duong.xlsx"),
      sheet_name=SHEET_NAME,
      feature_name="Danh mục ghi chú kiểm tra bảo dưỡng - Cập nhật ngày 13/08/2026",
      module_name="DM ghi chú kiểm tra BD",
      description_block=NM_DESC, role_tcs=NM_ROLE, sections=NM_SECTIONS)
