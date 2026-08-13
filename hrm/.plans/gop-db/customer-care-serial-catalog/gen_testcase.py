# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man Danh muc serial thiet bi lam dich vu (CSKH).

Chay:  python gen_testcase.py
"""
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "..", ".claude", "skills", "testcase-documenter", "assets"))

from tc_engine import build  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(HERE, "testcase.xlsx")
SHEET_NAME = "Trang tính1"
FEATURE_NAME = "Danh mục serial thiết bị làm dịch vụ - Cập nhật ngày 13/08/2026"
MODULE_NAME = "DM serial thiết bị DV"

# ============================================================================
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Tra cứu toàn bộ serial thiết bị đang được làm dịch vụ, kèm tên hàng và khách hàng đang sở "
     "hữu thiết bị đó. Dùng để tìm nhanh một serial khi tiếp nhận yêu cầu bảo hành, bảo dưỡng, "
     "sửa chữa.\n"
     "Màn hình nằm ở phân hệ Chăm sóc khách hàng → nhóm menu Danh mục - Dịch vụ → "
     "Danh mục serial thiết bị làm dịch vụ.\n"
     "⚠️ Đây là màn CHỈ ĐỌC: chỉ xem, lọc và xuất Excel. Mọi thao tác thêm / sửa / xóa serial nằm "
     "ở màn Quản lý khách hàng → tab Trang thiết bị, KHÔNG làm ở đây."),

    ("2. Đối tượng được tính / hiển thị",
     "- Toàn bộ serial thiết bị trong hệ thống, KHÔNG phân theo công ty / phòng ban.\n"
     "- Hiển thị cả serial Đang sử dụng và serial Ngưng sử dụng.\n"
     "- Mỗi dòng gồm 8 cột: STT, Serial thiết bị làm dịch vụ, Tên hàng, Khách hàng, Trạng thái, "
     "Người tạo, Người cập nhật, Ngày cập nhật.\n"
     "- KHÔNG có cột Hành động vì màn chỉ đọc.\n"
     "- Dữ liệu rất lớn: khoảng 21.600 dòng."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Không có serial nào bị ẩn khỏi danh sách khi chưa lọc.\n"
     "- Khi lọc theo Trạng thái = Ngưng sử dụng, hệ thống chỉ lấy các serial được đánh dấu ngưng "
     "theo đúng quy ước; một số ít serial cũ mang giá trị trạng thái lạ (không phải Đang sử dụng "
     "cũng không phải Ngưng sử dụng đúng quy ước) sẽ KHÔNG lọt vào kết quả dù trên bảng chúng "
     "vẫn hiện nhãn Ngưng sử dụng.\n"
     "⚠️ Đây là hành vi giữ nguyên từ hệ thống cũ, đang chờ nghiệp vụ chốt lại. Nếu QA thấy tổng "
     "của hai lần lọc (Đang sử dụng + Ngưng sử dụng) nhỏ hơn tổng khi không lọc thì đó chính là "
     "nhóm dòng này, không phải lỗi phát sinh mới."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Không áp dụng. Màn hình không có ô lọc theo khoảng thời gian.\n"
     "Cột Ngày cập nhật chỉ để xem và để sắp xếp."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Danh sách phẳng, không phân cấp cha - con.\n"
     "Mỗi serial gắn với một mặt hàng (Tên hàng) và một khách hàng (Khách hàng đang sở hữu "
     "thiết bị).\n"
     "Danh sách chọn Người tạo và Người cập nhật được lấy từ chính những người đã từng tạo / sửa "
     "serial, không phải toàn bộ danh sách nhân viên."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "Không cộng dồn, không gộp dòng. Mỗi serial là một dòng độc lập.\n"
     "Màn này không tạo dữ liệu nên không có quy tắc chống trùng riêng; việc chống trùng serial "
     "thuộc màn Quản lý khách hàng → tab Trang thiết bị."),

    ("7. Phân quyền cấp",
     "Chỉ MỘT quyền duy nhất cho màn này: \"Xem danh mục serial thiết bị làm dịch vụ\".\n"
     "Có quyền thì vào được màn hình, xem, lọc và xuất Excel. Không có quyền thì không vào được.\n"
     "Không có quyền quản lý riêng vì màn chỉ đọc.\n"
     "Danh mục KHÔNG phân quyền theo công ty / phòng ban / bộ phận."),

    ("8. Cách tính các ô thống kê",
     "- Dòng \"Hiển thị a - b / N\" dưới bảng: a là dòng đầu của trang đang xem, b là dòng cuối, "
     "N là tổng số serial khớp bộ lọc hiện tại (không phải tổng toàn bộ 21.600 dòng).\n"
     "- Cột STT đánh theo trang: trang 2 với cỡ trang 10 thì bắt đầu từ 11.\n"
     "- Thông báo sau khi xuất Excel nêu rõ SỐ DÒNG đã xuất — dùng con số này để đối chiếu với "
     "tổng dưới bảng."),

    ("9. Ghi chú đọc bảng",
     "- Màn CHỈ ĐỌC: không có nút Tạo mới, không có nút Sửa, không có nút Xóa, không có cột "
     "Hành động. Thấy bất kỳ nút ghi dữ liệu nào là sai.\n"
     "- Xuất Excel với hơn 21.000 dòng mất khoảng 10-15 giây và tải dữ liệu theo nhiều lượt. "
     "Trong lúc đó KHÔNG được rời màn hoặc bấm lại nút — hãy chờ đến khi có thông báo kết quả.\n"
     "- Trạng thái chỉ có hai giá trị hiển thị: Đang sử dụng và Ngưng sử dụng.\n"
     "- Một số serial cũ không có tên người cập nhật; ô đó để trống là bình thường, không phải lỗi.\n"
     "- Bộ lọc được hệ thống ghi nhớ trong 10 phút. Kiểm thử bộ lọc nên bấm Làm mới trước mỗi "
     "kịch bản.\n"
     "- Với dữ liệu lớn như vậy, hãy kiểm cả tốc độ: mở màn, chuyển trang và đổi cỡ trang đều "
     "phải xong trong vài giây."),
]

# ============================================================================
PRE_PERM = ("Có sẵn 2 tài khoản: A được cấp quyền \"Xem danh mục serial thiết bị làm dịch vụ\"; "
            "B KHÔNG được cấp quyền này. Danh mục có khoảng 21.600 serial.")

ROLE_TCS = [
    ("01", "Vào màn hình khi có quyền Xem", "P0", PRE_PERM,
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Vào phân hệ Chăm sóc khách hàng → Danh mục - Dịch vụ → "
     "Danh mục serial thiết bị làm dịch vụ", "Tài khoản A",
     "- Vào được màn hình, bảng hiển thị dữ liệu\n"
     "- Có nút Xuất Excel\n"
     "- KHÔNG có nút Tạo mới, không có cột Hành động"),

    ("02", "Chặn vào màn hình khi không có quyền", "P0", PRE_PERM,
     "1. Đăng nhập bằng tài khoản B\n"
     "2. Tìm mục Danh mục serial thiết bị làm dịch vụ trong phân hệ Chăm sóc khách hàng\n"
     "3. Dán thẳng đường dẫn màn hình vào thanh địa chỉ", "Tài khoản B",
     "- Mục menu KHÔNG hiện\n"
     "- Dán thẳng đường dẫn thì chuyển sang trang báo không tìm thấy, "
     "KHÔNG hiện dữ liệu serial nào\n"
     "⚠️ Không được để lộ dù chỉ một phần bảng rồi mới chuyển trang"),

    ("03", "Chặn lấy dữ liệu khi bỏ qua giao diện", "P0", PRE_PERM,
     "1. Đăng nhập bằng tài khoản B, lấy mã đăng nhập\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng lấy danh sách serial, bỏ qua giao diện",
     "Tài khoản B (không có quyền)",
     "- Hệ thống từ chối, báo không có quyền\n"
     "- Không trả về bất kỳ dòng dữ liệu nào\n"
     "⚠️ Dữ liệu này gắn với khách hàng nên rò rỉ là vấn đề nghiêm trọng"),

    ("04", "Không có chức năng ghi dữ liệu nào", "P0", PRE_PERM,
     "1. Đăng nhập bằng tài khoản A\n2. Rà toàn bộ màn hình: cụm nút dưới bảng, từng dòng, "
     "đầu trang", "Tài khoản A",
     "- Không tìm thấy nút Tạo mới, Sửa, Xóa, Nhập Excel hay bất kỳ nút ghi dữ liệu nào\n"
     "- Không bấm đúp vào dòng nào mở ra được cửa sổ sửa"),

    ("05", "Người có quyền xem thấy đủ dữ liệu của mọi công ty", "P1",
     "Hai tài khoản thuộc hai công ty khác nhau, đều có quyền Xem danh mục serial thiết bị "
     "làm dịch vụ.",
     "1. Cả hai cùng mở màn hình\n2. So sánh tổng dưới bảng", "—",
     "- Hai người thấy CÙNG một tổng số serial\n"
     "⚠️ Danh mục này cố ý không phân theo công ty"),
]

# ============================================================================
PRE = ("Đăng nhập bằng tài khoản có quyền \"Xem danh mục serial thiết bị làm dịch vụ\". "
       "Danh mục có khoảng 21.600 serial, gồm cả Đang sử dụng và Ngưng sử dụng; "
       "có ít nhất 1 serial thuộc khách hàng \"Công ty ABC\" và 1 serial không có tên "
       "người cập nhật.")

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", [
        ("001", "Mở màn hình lần đầu", "P0", PRE,
         "1. Vào phân hệ Chăm sóc khách hàng → Danh mục - Dịch vụ → "
         "Danh mục serial thiết bị làm dịch vụ\n2. Quan sát toàn màn hình", "—",
         "- Tiêu đề trang và tiêu đề bảng đều là \"Danh mục serial thiết bị làm dịch vụ\"\n"
         "- Khối lọc có tiêu đề \"Bộ lọc serial thiết bị làm dịch vụ\", mặc định thu gọn\n"
         "- Bảng có đủ 8 cột đúng thứ tự: STT, Serial thiết bị làm dịch vụ, Tên hàng, Khách hàng, "
         "Trạng thái, Người tạo, Người cập nhật, Ngày cập nhật\n"
         "- Dưới bảng chỉ có nút Xuất Excel"),

        ("002", "Không có cột Hành động", "P0", PRE,
         "1. Mở màn hình\n2. Kéo bảng sang phải hết cỡ", "—",
         "- Cột cuối cùng là Ngày cập nhật, KHÔNG có cột Hành động\n"
         "⚠️ Màn chỉ đọc: xuất hiện cột Hành động là sai thiết kế"),

        ("003", "Thời gian mở màn với hơn 21.000 dòng", "P0", PRE,
         "1. Mở màn hình và bấm giờ đến khi bảng hiện xong", "—",
         "- Bảng hiện trong vòng vài giây, không treo trang, không trắng màn hình\n"
         "- Chỉ tải dữ liệu MỘT lượt, không chớp tải hai lần"),

        ("004", "Cột Tên hàng và Khách hàng xuống dòng khi dài", "P1", PRE,
         "1. Mở màn hình\n2. Tìm dòng có tên hàng dài và tên khách hàng dài", "—",
         "- Nội dung được xuống dòng trong ô, hiện đầy đủ\n"
         "- Không cắt cụt, không tràn ra ngoài bảng"),

        ("005", "Cột Trạng thái hiển thị đúng nhãn", "P0", PRE,
         "1. Mở màn hình\n2. Đối chiếu cột Trạng thái", "—",
         "- Chỉ hiện hai nhãn: \"Đang sử dụng\" và \"Ngưng sử dụng\"\n"
         "- Không dòng nào hiện con số hay để trống"),

        ("006", "Serial không có người cập nhật", "P0", PRE,
         "1. Tìm dòng serial cũ chưa từng được sửa\n2. Nhìn cột Người cập nhật", "—",
         "- Ô để trống hoặc hiện dấu gạch ngang\n"
         "- Màn hình KHÔNG lỗi, dòng vẫn hiện đủ các cột còn lại\n"
         "⚠️ Đây là điểm hệ thống cũ hay lỗi khi thiếu thông tin người cập nhật"),

        ("007", "Bảng trống khi bộ lọc không khớp gì", "P1", PRE,
         "1. Gõ \"khongtontai123\" vào ô tìm nhanh\n2. Bấm Tìm kiếm", "khongtontai123",
         "- Bảng hiện thông báo không có dữ liệu phù hợp, tổng dưới bảng là 0\n"
         "- Nút Xuất Excel vẫn còn"),

        ("008", "Tổng dưới bảng đúng với dữ liệu thực", "P0", PRE,
         "1. Mở màn hình khi chưa lọc\n2. Đọc dòng Hiển thị dưới bảng", "—",
         "- Tổng khớp với số serial thực tế đang có (khoảng 21.600)\n"
         "- Không hiện tổng bằng số dòng của trang đang xem"),
    ]),

    ("II", "BỘ LỌC & TÌM KIẾM", [
        ("001", "Tìm nhanh theo Serial", "P0", PRE,
         "1. Gõ một số serial có thật vào ô tìm nhanh\n2. Bấm Tìm kiếm", "Một serial có thật",
         "- Kết quả gồm dòng có serial đó\n"
         "⚠️ Gợi ý trong ô ghi rõ: \"Tìm theo serial, tên hàng hoặc khách hàng...\""),

        ("002", "Tìm nhanh theo Tên hàng", "P0", PRE,
         "1. Gõ một phần tên hàng\n2. Bấm Tìm kiếm", "Một phần tên hàng",
         "- Kết quả gồm mọi serial của mặt hàng khớp chuỗi tìm"),

        ("003", "Tìm nhanh theo Khách hàng", "P0", PRE,
         "1. Gõ \"ABC\" (một phần tên khách hàng)\n2. Bấm Tìm kiếm", "ABC",
         "- Kết quả gồm mọi serial thuộc khách hàng khớp chuỗi tìm"),

        ("004", "Tìm nhanh khớp một phần chuỗi", "P0", PRE,
         "1. Gõ 4 ký tự giữa của một số serial\n2. Bấm Tìm kiếm", "4 ký tự giữa serial",
         "- Serial tương ứng vẫn ra kết quả\n"
         "⚠️ Không được yêu cầu gõ đúng nguyên serial mới ra kết quả"),

        ("005", "Tìm nhanh không phân biệt hoa thường", "P1", PRE,
         "1. Gõ tên hàng bằng chữ thường\n2. Bấm Tìm kiếm", "chữ thường",
         "- Kết quả giống hệt khi gõ chữ hoa"),

        ("006", "Gõ ô tìm nhanh mà chưa bấm Tìm kiếm", "P1", PRE,
         "1. Gõ từ khóa\n2. Chờ 5 giây, không bấm gì", "ABC",
         "- Bảng vẫn giữ nguyên, chưa lọc"),

        ("007", "Lọc theo Khách hàng", "P0", PRE,
         "1. Mở bộ lọc nâng cao\n2. Chọn một khách hàng trong ô Khách hàng\n3. Bấm Tìm kiếm",
         "Khách hàng: Công ty ABC",
         "- Kết quả chỉ còn serial của khách hàng đã chọn\n"
         "- Cột Khách hàng của mọi dòng đều là tên vừa chọn"),

        ("008", "Lọc theo Trạng thái = Đang sử dụng", "P0", PRE,
         "1. Chọn Trạng thái = Đang sử dụng\n2. Bấm Tìm kiếm\n3. Ghi lại tổng dưới bảng",
         "Trạng thái: Đang sử dụng",
         "- Kết quả chỉ còn các dòng mang nhãn Đang sử dụng"),

        ("009", "Lọc theo Trạng thái = Ngưng sử dụng", "P0", PRE,
         "1. Chọn Trạng thái = Ngưng sử dụng\n2. Bấm Tìm kiếm\n3. Ghi lại tổng dưới bảng",
         "Trạng thái: Ngưng sử dụng",
         "- Kết quả chỉ còn các dòng mang nhãn Ngưng sử dụng"),

        ("010", "Đối chiếu tổng của hai lần lọc trạng thái", "P0", PRE,
         "1. Ghi lại tổng khi KHÔNG lọc\n2. Ghi lại tổng khi lọc Đang sử dụng\n"
         "3. Ghi lại tổng khi lọc Ngưng sử dụng\n4. Cộng hai tổng ở bước 2 và 3 rồi so với bước 1",
         "—",
         "- Tổng cộng của hai lần lọc NHỎ HƠN tổng khi không lọc khoảng hơn chục dòng\n"
         "⚠️ Chênh lệch này là do một nhóm serial cũ mang giá trị trạng thái lạ, được giữ nguyên "
         "từ hệ thống cũ và đang chờ nghiệp vụ chốt. Ghi lại con số chênh lệch để báo cáo, "
         "KHÔNG ghi là lỗi mới phát sinh"),

        ("011", "Lọc theo Người tạo", "P0", PRE,
         "1. Chọn một người trong ô Người tạo\n2. Bấm Tìm kiếm", "Người tạo: một nhân viên",
         "- Kết quả chỉ còn serial do người đó tạo\n"
         "- Cột Người tạo của mọi dòng đều là tên vừa chọn"),

        ("012", "Danh sách chọn Người tạo chỉ liệt kê người đã tạo dữ liệu", "P1", PRE,
         "1. Mở danh sách chọn ở ô Người tạo\n2. Đếm số lượng và đối chiếu", "—",
         "- Danh sách ngắn, chỉ gồm những người thực sự đã tạo serial\n"
         "- KHÔNG liệt kê toàn bộ nhân viên công ty\n"
         "⚠️ Chọn một người bất kỳ trong danh sách này thì phải ra kết quả, "
         "không được ra bảng trống"),

        ("013", "Lọc theo Người cập nhật", "P0", PRE,
         "1. Chọn một người trong ô Người cập nhật\n2. Bấm Tìm kiếm",
         "Người cập nhật: một nhân viên",
         "- Kết quả chỉ còn serial do người đó cập nhật gần nhất"),

        ("014", "Kết hợp nhiều điều kiện lọc", "P0", PRE,
         "1. Chọn Khách hàng, Trạng thái = Đang sử dụng và Người tạo\n2. Bấm Tìm kiếm",
         "Khách hàng + Trạng thái + Người tạo",
         "- Kết quả phải thỏa ĐỒNG THỜI mọi điều kiện đã chọn"),

        ("015", "Kết hợp tìm nhanh và lọc nâng cao", "P0", PRE,
         "1. Gõ một phần tên hàng vào ô tìm nhanh\n2. Chọn Trạng thái = Đang sử dụng\n"
         "3. Bấm Tìm kiếm", "Từ khóa + Trạng thái",
         "- Kết quả phải thỏa cả hai điều kiện"),

        ("016", "Nút Làm mới xóa hết điều kiện và nạp lại", "P0", PRE,
         "1. Đặt nhiều điều kiện lọc và bấm Tìm kiếm\n2. Bấm nút Làm mới", "—",
         "- Mọi ô lọc trở về trống\n"
         "- Danh sách tự nạp lại toàn bộ NGAY, không cần bấm Tìm kiếm lần nữa\n"
         "⚠️ Bẫy hay gặp: xóa chữ trong ô nhưng bảng vẫn giữ kết quả lọc cũ"),

        ("017", "Bộ lọc được nhớ khi quay lại màn trong 10 phút", "P1", PRE,
         "1. Chọn Trạng thái = Ngưng sử dụng, bấm Tìm kiếm\n2. Sang màn khác\n"
         "3. Quay lại trong 10 phút", "Trạng thái: Ngưng sử dụng",
         "- Ô lọc và kết quả vẫn giữ nguyên, khối lọc nâng cao giữ nguyên trạng thái đóng/mở"),

        ("018", "Lọc xong tự về trang 1", "P1", PRE + " Đang đứng ở trang 50.",
         "1. Chuyển sang trang 50\n2. Đặt điều kiện lọc\n3. Bấm Tìm kiếm", "—",
         "- Kết quả hiển thị từ trang 1, không hiện bảng trống"),

        ("019", "Tốc độ lọc trên dữ liệu lớn", "P1", PRE,
         "1. Chọn Trạng thái = Đang sử dụng và bấm Tìm kiếm, bấm giờ", "—",
         "- Kết quả hiện trong vòng vài giây, không treo trang"),

        ("020", "Tìm nhanh với ký tự đặc biệt", "P2", PRE,
         "1. Gõ chuỗi \"%'\" vào ô tìm nhanh\n2. Bấm Tìm kiếm", "%'",
         "- Màn hình không lỗi, không trắng trang"),
    ]),

    ("III", "SẮP XẾP & PHÂN TRANG", [
        ("001", "Sắp xếp theo Serial", "P0", PRE,
         "1. Bấm tiêu đề cột Serial thiết bị làm dịch vụ 1 lần rồi 2 lần", "—",
         "- Lần 1 xếp tăng dần, lần 2 xếp giảm dần; mũi tên đổi chiều\n"
         "- Thứ tự các dòng THỰC SỰ thay đổi\n"
         "⚠️ Bẫy hay gặp: mũi tên đổi chiều nhưng danh sách đứng yên"),

        ("002", "Sắp xếp theo Tên hàng", "P0", PRE,
         "1. Bấm tiêu đề cột Tên hàng", "—",
         "- Danh sách xếp theo tên hàng, thứ tự thực sự thay đổi"),

        ("003", "Sắp xếp theo Khách hàng", "P0", PRE,
         "1. Bấm tiêu đề cột Khách hàng", "—",
         "- Danh sách xếp theo tên khách hàng, các dòng cùng khách hàng nằm liền nhau"),

        ("004", "Sắp xếp theo Trạng thái", "P1", PRE,
         "1. Bấm tiêu đề cột Trạng thái", "—",
         "- Các dòng cùng trạng thái được gom lại liền nhau"),

        ("005", "Sắp xếp theo Người tạo", "P1", PRE,
         "1. Bấm tiêu đề cột Người tạo", "—",
         "- Danh sách xếp theo tên người tạo, thứ tự thực sự thay đổi"),

        ("006", "Sắp xếp theo Người cập nhật", "P1", PRE,
         "1. Bấm tiêu đề cột Người cập nhật", "—",
         "- Danh sách xếp theo tên người cập nhật\n"
         "- Các dòng để trống người cập nhật được gom về một đầu, không gây lỗi"),

        ("007", "Sắp xếp theo Ngày cập nhật", "P0", PRE,
         "1. Bấm tiêu đề cột Ngày cập nhật 2 lần để xếp giảm dần", "—",
         "- Dòng cập nhật gần nhất nằm trên cùng\n"
         "- Xếp theo giá trị NGÀY, không phải theo chuỗi ký tự"),

        ("008", "Cột STT không sắp xếp được", "P2", PRE,
         "1. Bấm tiêu đề cột STT", "—",
         "- Không có mũi tên sắp xếp, bấm vào không đổi thứ tự và không lỗi"),

        ("009", "Sắp xếp giữ nguyên khi chuyển trang", "P1", PRE,
         "1. Sắp xếp theo Serial giảm dần\n2. Chuyển sang trang 2", "—",
         "- Trang 2 tiếp nối đúng thứ tự đã sắp, không quay về thứ tự mặc định"),

        ("010", "Sắp xếp giữ nguyên khi đang lọc", "P1", PRE,
         "1. Lọc theo một khách hàng\n2. Sắp xếp theo Ngày cập nhật", "—",
         "- Kết quả vẫn chỉ gồm khách hàng đã lọc, chỉ thay đổi thứ tự"),

        ("011", "Chuyển trang bằng nút số trang", "P0", PRE,
         "1. Bấm số trang 2", "—",
         "- Bảng hiện dữ liệu trang 2, cột STT bắt đầu từ 11\n"
         "- Dòng Hiển thị dưới bảng cập nhật đúng khoảng đang xem"),

        ("012", "Chuyển tới trang cuối của hơn 2.000 trang", "P0", PRE,
         "1. Bấm nút chuyển tới trang cuối\n2. Bấm giờ", "Cỡ trang: 10",
         "- Trang cuối hiện dữ liệu trong vài giây, không lỗi, không trống\n"
         "- Cột STT của trang cuối là các số lớn nhất, khớp với tổng dưới bảng"),

        ("013", "Đổi cỡ trang", "P0", PRE,
         "1. Đổi cỡ trang từ 10 sang 100", "Cỡ trang: 100",
         "- Bảng hiện 100 dòng\n- Danh sách chỉ nạp lại đúng MỘT lần, không chớp tải hai lượt"),

        ("014", "Đổi cỡ trang khi đang ở trang cuối", "P1", PRE + " Đang ở trang cuối.",
         "1. Đổi cỡ trang sang 100", "Cỡ trang: 100",
         "- Bảng hiện dữ liệu, KHÔNG hiện bảng trống\n"
         "⚠️ Bẫy phân trang: giữ nguyên số trang cũ sau khi tăng cỡ trang sẽ ra bảng rỗng"),

        ("015", "Phân trang sau khi lọc còn ít kết quả", "P1", PRE,
         "1. Lọc ra kết quả chỉ còn 3 dòng\n2. Quan sát phần phân trang", "—",
         "- Chỉ còn 1 trang, dòng Hiển thị ghi đúng 1 - 3 / 3"),
    ]),

    ("IV", "XUẤT EXCEL", [
        ("001", "Xuất Excel toàn bộ danh mục", "P0", PRE,
         "1. Không lọc gì\n2. Bấm nút Xuất Excel\n3. Chờ đến khi có thông báo\n4. Mở file tải về",
         "—",
         "- Trong lúc xử lý có dấu hiệu đang chạy, nút không bấm lại được\n"
         "- Kết thúc hiện thông báo xuất Excel thành công kèm SỐ DÒNG đã xuất\n"
         "- Số dòng trong thông báo khớp với tổng dưới bảng\n"
         "- File mở được bằng Excel"),

        ("002", "Thời gian xuất Excel với hơn 21.000 dòng", "P0", PRE,
         "1. Bấm Xuất Excel và bấm giờ", "—",
         "- Hoàn tất trong khoảng 10-20 giây\n"
         "- Màn hình KHÔNG treo, không trắng trang, không báo hết thời gian chờ\n"
         "⚠️ Đây là điểm rủi ro nhất của màn: dữ liệu lớn nên phải kiểm trên môi trường "
         "giống thật, không chỉ trên máy cá nhân"),

        ("003", "File Excel có đủ cột như trên màn hình", "P0", PRE,
         "1. Xuất Excel\n2. Đối chiếu tiêu đề cột với bảng trên màn hình", "—",
         "- File có các cột Serial, Tên hàng, Khách hàng, Trạng thái, Người tạo, Người cập nhật, "
         "Ngày cập nhật\n- Tiêu đề cột bằng tiếng Việt giống trên màn hình"),

        ("004", "Xuất Excel theo đúng bộ lọc đang áp dụng", "P0", PRE,
         "1. Lọc theo một khách hàng (còn khoảng 50 dòng)\n2. Bấm Xuất Excel\n3. Mở file và đếm",
         "Khách hàng: Công ty ABC",
         "- File chỉ chứa đúng số dòng đang lọc\n"
         "- Cột Khách hàng của mọi dòng đều là khách hàng đã lọc\n"
         "⚠️ Bẫy hay gặp: file xuất toàn bộ hơn 21.000 dòng, bỏ qua bộ lọc"),

        ("005", "Xuất Excel theo từ khóa tìm nhanh", "P0", PRE,
         "1. Gõ từ khóa và bấm Tìm kiếm\n2. Bấm Xuất Excel\n3. Mở file", "Một phần tên hàng",
         "- File chỉ chứa các dòng khớp từ khóa"),

        ("006", "Xuất Excel lấy đủ dữ liệu, không chỉ trang hiện tại", "P0", PRE,
         "1. Đứng ở trang 1 với cỡ trang 10\n2. Bấm Xuất Excel\n3. Đếm số dòng trong file", "—",
         "- File có đủ toàn bộ số dòng khớp bộ lọc, không phải 10 dòng của trang đang xem"),

        ("007", "Xuất Excel giữ đúng thứ tự đang sắp xếp", "P1", PRE,
         "1. Sắp xếp theo Ngày cập nhật giảm dần\n2. Bấm Xuất Excel\n3. Mở file", "—",
         "- Thứ tự dòng trong file khớp thứ tự đang hiển thị trên màn hình"),

        ("008", "Xuất Excel khi kết quả lọc rỗng", "P0", PRE,
         "1. Lọc ra kết quả rỗng\n2. Bấm Xuất Excel", "khongtontai123",
         "- Hệ thống hiện thông báo \"Không có dữ liệu để xuất\"\n"
         "- KHÔNG tải về file rỗng, không lỗi trắng trang"),

        ("009", "Serial thiếu người cập nhật trong file Excel", "P1", PRE,
         "1. Lọc ra dòng không có người cập nhật\n2. Xuất Excel và mở file", "—",
         "- Ô Người cập nhật của dòng đó để trống\n"
         "- File vẫn xuất bình thường, không đứt giữa chừng"),

        ("010", "Không rời màn trong lúc đang xuất", "P1", PRE,
         "1. Bấm Xuất Excel\n2. Ngay lập tức chuyển sang màn khác\n3. Quay lại", "—",
         "- Hệ thống không lỗi, không treo\n"
         "⚠️ Việc xuất có thể bị hủy giữa chừng — đây là hạn chế đã biết, hãy chờ xong "
         "rồi mới rời màn"),

        ("011", "Bấm Xuất Excel nhiều lần liên tiếp", "P1", PRE,
         "1. Bấm Xuất Excel liên tiếp 3 lần thật nhanh", "—",
         "- Chỉ chạy MỘT lượt xuất, nút bị vô hiệu trong lúc đang xử lý\n"
         "- Không tải về 3 file trùng nhau"),

        ("012", "Nội dung file khớp với dữ liệu trên màn hình", "P0", PRE,
         "1. Lọc còn khoảng 10 dòng\n2. Chụp lại nội dung bảng\n3. Xuất Excel và đối chiếu từng ô",
         "—",
         "- Mọi giá trị serial, tên hàng, khách hàng, trạng thái, người tạo, người cập nhật, "
         "ngày cập nhật đều khớp\n- Không lệch dòng, không lệch cột"),
    ]),

    ("V", "ĐỐI CHIẾU DỮ LIỆU & LUỒNG XUYÊN SUỐT", [
        ("001", "Serial mới tạo ở màn khác hiện ngay tại đây", "P0",
         PRE + " Có quyền vào màn Quản lý khách hàng.",
         "1. Vào Quản lý khách hàng → tab Trang thiết bị của khách hàng ABC\n"
         "2. Thêm một serial mới\n3. Quay lại Danh mục serial và tìm serial đó",
         "Serial: TEST-0001",
         "- Serial mới có mặt trong danh mục với đúng tên hàng, đúng khách hàng ABC\n"
         "- Cột Người tạo là người vừa thao tác"),

        ("002", "Sửa serial ở màn khác phản ánh ngay tại đây", "P0",
         PRE + " Serial TEST-0001 vừa được tạo.",
         "1. Vào Quản lý khách hàng → tab Trang thiết bị, sửa serial TEST-0001\n"
         "2. Quay lại Danh mục serial và tìm serial đó", "Đổi tên hàng của TEST-0001",
         "- Danh mục hiện tên hàng MỚI\n"
         "- Cột Người cập nhật và Ngày cập nhật đổi theo lần sửa vừa rồi"),

        ("003", "Chuyển serial sang Ngưng sử dụng", "P0", PRE,
         "1. Ở màn Quản lý khách hàng, chuyển serial TEST-0001 sang Ngưng sử dụng\n"
         "2. Quay lại Danh mục serial, lọc Trạng thái = Ngưng sử dụng và tìm serial đó",
         "Serial: TEST-0001",
         "- Serial hiện nhãn Ngưng sử dụng và nằm trong kết quả lọc\n"
         "- Lọc Trạng thái = Đang sử dụng thì serial này KHÔNG còn trong kết quả"),

        ("004", "Xóa serial ở màn khác thì mất khỏi danh mục", "P1", PRE,
         "1. Ở màn Quản lý khách hàng, xóa serial TEST-0001\n"
         "2. Quay lại Danh mục serial và tìm serial đó", "Serial: TEST-0001",
         "- Không tìm thấy serial đó nữa, tổng dưới bảng giảm 1"),

        ("005", "Luồng tra cứu đầy đủ", "P0", PRE,
         "1. Vào màn hình\n2. Gõ một số serial vào ô tìm nhanh và Tìm kiếm\n"
         "3. Đọc tên hàng và khách hàng của dòng kết quả\n"
         "4. Lọc thêm theo khách hàng đó để xem toàn bộ thiết bị của họ\n5. Xuất Excel danh sách đó",
         "Một serial có thật",
         "- Bước 2 ra đúng 1 dòng\n"
         "- Bước 4 ra toàn bộ serial của khách hàng đó\n"
         "- Bước 5 xuất ra file khớp đúng số dòng ở bước 4"),

        ("006", "Kiểm tra nhất quán giữa hai cổng", "P1", PRE,
         "1. Mở màn tương ứng ở cổng cũ, ghi lại tổng số serial\n"
         "2. Mở màn này ở cổng mới, so tổng số serial\n"
         "3. Chọn ngẫu nhiên 5 serial và đối chiếu tên hàng, khách hàng, trạng thái", "—",
         "- Tổng hai bên bằng nhau\n"
         "- 5 serial đối chiếu đều khớp mọi thông tin\n"
         "⚠️ Hai cổng đọc chung một nguồn dữ liệu, mọi sai lệch đều là lỗi"),

        ("007", "Màn mới hiện thêm 3 cột so với cổng cũ", "P1", PRE,
         "1. Mở màn tương ứng ở cổng cũ và đếm số cột\n2. Mở màn này và đếm số cột", "—",
         "- Màn mới có thêm các cột Người tạo, Người cập nhật, Ngày cập nhật so với cổng cũ\n"
         "⚠️ Đây là bổ sung có chủ ý, không phải sai lệch"),
    ]),
]

build(output_file=OUTPUT_FILE, sheet_name=SHEET_NAME, feature_name=FEATURE_NAME,
      module_name=MODULE_NAME, description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS, sections=SECTIONS)
