# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man Danh muc tien te (phan he Tai chinh).

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
FEATURE_NAME = "Danh mục tiền tệ - Cập nhật ngày 13/08/2026"
MODULE_NAME = "Danh mục tiền tệ"

# ============================================================================
# 9 MUC MO TA TINH NANG
# ============================================================================
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Quản lý tập trung danh sách các loại tiền tệ và tỷ giá quy đổi ra Đồng Việt Nam, dùng chung cho "
     "toàn hệ thống (báo giá, hợp đồng, đề nghị thu tiền, đề nghị chi tiền, công nợ, phiếu kế toán…).\n"
     "Màn hình nằm ở phân hệ Tài chính → nhóm menu Danh mục → Danh mục tiền tệ.\n"
     "Đây là màn được chuyển từ hệ thống cũ sang. Hai cổng dùng CHUNG một danh sách tiền tệ, nên sửa ở "
     "cổng mới thì cổng cũ cũng thấy ngay và ngược lại."),

    ("2. Đối tượng được tính / hiển thị",
     "- Toàn bộ tiền tệ trong danh mục, KHÔNG phân theo công ty / phòng ban — ai có quyền vào màn thì "
     "thấy đủ như nhau.\n"
     "- Hiển thị cả tiền tệ ở trạng thái Hoạt động và trạng thái Khóa (mặc định không lọc trạng thái).\n"
     "- Mỗi dòng gồm 7 cột: STT, Mã tiền tệ, Tên tiền tệ (kèm dòng phụ \"Tên gọi khác\" nếu có), "
     "Tỷ giá (VNĐ), Cập nhật, Trạng thái, Hành động.\n"
     "- Cột Tên tiền tệ chỉ hiện dòng phụ \"Tên gọi khác\" khi tiền tệ đó có nhập tên gọi khác; "
     "không nhập thì không hiện dòng phụ (không hiện dòng trống)."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Không có tiền tệ nào bị ẩn khỏi danh sách: màn này không có khái niệm xóa mềm / lưu trữ.\n"
     "- Tiền tệ ở trạng thái Khóa VẪN hiện trong danh sách của màn này, chỉ bị chặn không cho chọn mới "
     "ở các màn nghiệp vụ khác.\n"
     "- Khi lọc theo Trạng thái = Hoạt động thì các tiền tệ đang Khóa bị loại khỏi kết quả và ngược lại."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Không áp dụng. Màn hình không có bộ lọc theo khoảng thời gian.\n"
     "Cột Cập nhật chỉ để xem và để sắp xếp, không phải điều kiện lọc."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Danh sách phẳng, không phân cấp cha - con.\n"
     "Mã tiền tệ là giá trị không được trùng trong toàn danh mục.\n"
     "Tỷ giá luôn được hiểu là: 1 đơn vị tiền tệ đó bằng bao nhiêu Đồng Việt Nam."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "Không cộng dồn. Mỗi tiền tệ là một dòng độc lập.\n"
     "Quy tắc chống trùng: Mã tiền tệ là duy nhất. Thêm mới hoặc sửa sang một mã đã có sẽ bị chặn với "
     "thông báo \"Mã tiền tệ đã tồn tại\" ngay dưới ô Mã tiền tệ.\n"
     "Tên tiền tệ và Tên gọi khác KHÔNG bắt buộc duy nhất — được phép trùng."),

    ("7. Phân quyền cấp",
     "Hai quyền dành riêng cho màn này:\n"
     "- \"Xem danh mục tiền tệ\": vào được màn hình, xem danh sách, mở xem chi tiết, xuất Excel.\n"
     "- \"Quản lý danh mục tiền tệ\": thêm mới, sửa, khóa, mở khóa, xóa. Người có quyền này cũng "
     "vào và xem được màn hình.\n"
     "Không có quyền nào trong hai quyền trên thì không vào được màn hình.\n"
     "Danh mục KHÔNG phân quyền theo công ty / phòng ban / bộ phận."),

    ("8. Cách tính các ô thống kê",
     "- Dòng \"Hiển thị a - b / N\" dưới bảng: a là số thứ tự dòng đầu của trang đang xem, b là dòng "
     "cuối, N là tổng số tiền tệ khớp bộ lọc hiện tại (không phải tổng toàn danh mục).\n"
     "- Cột STT được đánh theo trang: trang 2 với cỡ trang 10 thì bắt đầu từ 11.\n"
     "- Cột Tỷ giá (VNĐ) hiển thị theo định dạng Việt Nam: dấu chấm ngăn cách hàng nghìn, dấu phẩy "
     "ngăn phần thập phân, luôn 2 chữ số thập phân. Ví dụ 26.520,00."),

    ("9. Ghi chú đọc bảng",
     "- Ô nhập Tỷ giá dùng dấu phẩy làm dấu thập phân theo chuẩn Việt Nam; tối đa 999.999,99. "
     "Nhập vượt trần sẽ bị chặn kèm thông báo.\n"
     "- Tỷ giá được hệ thống TỰ ĐỘNG cập nhật lại hằng ngày lúc 03:00 sáng theo tỷ giá bán của "
     "Vietcombank, khớp theo Mã tiền tệ (riêng VNĐ được bỏ qua). Vì vậy tỷ giá sửa tay hôm nay có thể "
     "khác vào sáng hôm sau — đây là hành vi đúng, không phải lỗi. Khi kiểm thử tỷ giá, hãy đối chiếu "
     "trong cùng một ngày.\n"
     "- Nút Xóa bị mờ (không bấm được) với tiền tệ đang được dùng ở chứng từ khác. Trạng thái mờ này "
     "xuất hiện chậm hơn bảng khoảng vài trăm mili giây — vừa mở màn mà nút còn sáng là bình thường, "
     "bấm vào vẫn bị hệ thống chặn lại.\n"
     "- Nút Khóa / Mở khóa nằm NGAY TRONG cột Trạng thái, không nằm ở cột Hành động.\n"
     "- Bộ lọc được hệ thống ghi nhớ trong 10 phút: rời màn rồi quay lại trong 10 phút thì bộ lọc cũ "
     "vẫn còn. Khi kiểm thử bộ lọc, nhớ bấm Làm mới trước mỗi kịch bản.\n"
     "- Nút Xuất Excel luôn hiện với mọi người vào được màn."),
]

# ============================================================================
# TC PHAN QUYEN
# ============================================================================
PRE_2_PERM = ("Có sẵn 2 tài khoản: tài khoản A chỉ được cấp quyền \"Xem danh mục tiền tệ\"; "
              "tài khoản B được cấp quyền \"Quản lý danh mục tiền tệ\". "
              "Danh mục đang có 11 tiền tệ, trong đó VNĐ và USD đang được dùng ở chứng từ khác, "
              "tiền tệ \"TST\" mới tạo chưa dùng ở đâu.")

ROLE_TCS = [
    ("01", "Vào màn hình khi chỉ có quyền Xem", "P0",
     PRE_2_PERM,
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Vào phân hệ Tài chính → Danh mục → Danh mục tiền tệ",
     "Tài khoản A (chỉ có quyền Xem danh mục tiền tệ)",
     "- Vào được màn hình, bảng hiển thị đủ 11 tiền tệ\n"
     "- KHÔNG có nút Tạo mới\n"
     "- Trên mỗi dòng chỉ có nút Xem (hình con mắt); KHÔNG có nút Sửa, nút Xóa\n"
     "- Trong cột Trạng thái KHÔNG có nút Khóa / Mở khóa\n"
     "- Vẫn có nút Xuất Excel"),

    ("02", "Vào màn hình khi có quyền Quản lý", "P0",
     PRE_2_PERM,
     "1. Đăng nhập bằng tài khoản B\n"
     "2. Vào Danh mục tiền tệ",
     "Tài khoản B (có quyền Quản lý danh mục tiền tệ)",
     "- Vào được màn hình\n"
     "- Có nút Tạo mới và nút Xuất Excel\n"
     "- Mỗi dòng có đủ 3 nút: Xem, Sửa, Xóa\n"
     "- Cột Trạng thái có nút Khóa (với dòng đang Hoạt động) hoặc Mở khóa (với dòng đang Khóa)"),

    ("03", "Chặn vào màn hình khi không có quyền nào", "P0",
     "Tài khoản C không được cấp cả hai quyền \"Xem danh mục tiền tệ\" và \"Quản lý danh mục tiền tệ\".",
     "1. Đăng nhập bằng tài khoản C\n"
     "2. Mở phân hệ Tài chính, tìm mục Danh mục tiền tệ\n"
     "3. Dán thẳng đường dẫn của màn Danh mục tiền tệ vào thanh địa chỉ",
     "Tài khoản C (không có quyền nào của màn này)",
     "- Mục menu Danh mục tiền tệ KHÔNG hiện trong phân hệ Tài chính\n"
     "- Dán thẳng đường dẫn thì hệ thống chuyển sang trang báo không tìm thấy, "
     "KHÔNG hiện dữ liệu tiền tệ nào\n"
     "⚠️ Không được để lộ dù chỉ một phần bảng dữ liệu rồi mới chuyển trang"),

    ("04", "Chặn Thêm mới khi bỏ qua giao diện", "P0",
     PRE_2_PERM + " Chuẩn bị công cụ kiểm thử API và mã đăng nhập của tài khoản A.",
     "1. Đăng nhập bằng tài khoản A, lấy mã đăng nhập\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Thêm tiền tệ, bỏ qua giao diện\n"
     "3. Mở lại màn Danh mục tiền tệ kiểm tra",
     "Mã tiền tệ: ZZZ; Tên tiền tệ: Tiền thử; Tỷ giá: 1,00",
     "- Hệ thống từ chối, báo không có quyền\n"
     "- Danh sách vẫn 11 tiền tệ, không xuất hiện ZZZ\n"
     "⚠️ Đây là nhóm dành cho tester kỹ thuật; nếu bản ghi được tạo là lỗ hổng phân quyền nghiêm trọng"),

    ("05", "Chặn Sửa khi bỏ qua giao diện", "P0",
     PRE_2_PERM,
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Sửa tiền tệ USD, bỏ qua giao diện\n"
     "3. Mở lại màn Danh mục tiền tệ, xem dòng USD",
     "Sửa Tên tiền tệ USD thành \"Bị sửa trộm\"",
     "- Hệ thống từ chối, báo không có quyền\n"
     "- Dòng USD giữ nguyên tên cũ và tỷ giá cũ"),

    ("06", "Chặn Xóa khi bỏ qua giao diện", "P0",
     PRE_2_PERM,
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa tiền tệ \"TST\", bỏ qua giao diện\n"
     "3. Mở lại màn Danh mục tiền tệ",
     "Tiền tệ TST (chưa dùng ở đâu nên về nghiệp vụ là xóa được)",
     "- Hệ thống từ chối, báo không có quyền\n"
     "- Tiền tệ TST vẫn còn trong danh sách\n"
     "⚠️ Bản ghi \"xóa được\" là phép thử nặng nhất: nếu quyền hở thì dữ liệu mất thật"),

    ("07", "Chặn Khóa / Mở khóa khi bỏ qua giao diện", "P1",
     PRE_2_PERM,
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Khóa tiền tệ USD, bỏ qua giao diện\n"
     "3. Mở lại màn Danh mục tiền tệ",
     "Tiền tệ USD đang ở trạng thái Hoạt động",
     "- Hệ thống từ chối, báo không có quyền\n"
     "- USD vẫn ở trạng thái Hoạt động"),

    ("08", "Người có quyền Quản lý làm được trọn vòng đời", "P1",
     PRE_2_PERM,
     "1. Đăng nhập bằng tài khoản B\n"
     "2. Tạo mới 1 tiền tệ\n"
     "3. Sửa tiền tệ vừa tạo\n"
     "4. Khóa rồi Mở khóa tiền tệ đó\n"
     "5. Xóa tiền tệ đó",
     "Mã: TC1; Tên: Tiền kiểm thử; Tỷ giá: 1.000,00",
     "- Cả 5 thao tác đều thực hiện được, mỗi thao tác có thông báo thành công tương ứng\n"
     "- Sau bước 5, tiền tệ TC1 không còn trong danh sách"),
]

# ============================================================================
# SECTION NGHIEP VU
# ============================================================================
PRE_LIST = ("Đăng nhập bằng tài khoản có quyền \"Quản lý danh mục tiền tệ\". "
            "Danh mục có 11 tiền tệ, trong đó 9 tiền tệ Hoạt động và 2 tiền tệ đang Khóa; "
            "có ít nhất 1 tiền tệ đã nhập Tên gọi khác (USD - Đô la Mỹ) và 1 tiền tệ bỏ trống "
            "Tên gọi khác.")

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", [
        ("001", "Mở màn hình lần đầu", "P0", PRE_LIST,
         "1. Vào phân hệ Tài chính → Danh mục → Danh mục tiền tệ\n"
         "2. Quan sát toàn màn hình", "—",
         "- Tiêu đề trang và tiêu đề bảng đều là \"Danh mục tiền tệ\"\n"
         "- Khối lọc phía trên có tiêu đề \"Bộ lọc danh mục tiền tệ\", mặc định ở dạng thu gọn "
         "(chỉ hiện ô tìm nhanh)\n"
         "- Bảng hiển thị đủ 7 cột theo đúng thứ tự: STT, Mã tiền tệ, Tên tiền tệ, Tỷ giá (VNĐ), "
         "Cập nhật, Trạng thái, Hành động\n"
         "- Dưới bảng có nút Tạo mới và nút Xuất Excel"),

        ("002", "Hiển thị đúng 11 bản ghi khi chưa lọc", "P0", PRE_LIST,
         "1. Mở màn hình\n2. Đọc dòng \"Hiển thị … / …\" dưới bảng", "—",
         "- Tổng hiển thị là 11\n"
         "- Cả tiền tệ Hoạt động và tiền tệ Khóa đều có mặt"),

        ("003", "Cột Tên tiền tệ hiện dòng phụ Tên gọi khác", "P1", PRE_LIST,
         "1. Mở màn hình\n2. Nhìn dòng USD và dòng tiền tệ không có tên gọi khác", "—",
         "- Dòng USD hiện tên tiền tệ ở dòng trên, dòng dưới hiện \"Tên gọi khác: Đô la Mỹ\"\n"
         "- Dòng không có tên gọi khác chỉ hiện 1 dòng tên, KHÔNG có dòng phụ trống"),

        ("004", "Định dạng số của cột Tỷ giá (VNĐ)", "P0", PRE_LIST,
         "1. Mở màn hình\n2. Đối chiếu cột Tỷ giá của các dòng", "—",
         "- Tỷ giá hiển thị dạng 26.520,00 — dấu chấm ngăn hàng nghìn, dấu phẩy ngăn phần thập phân, "
         "luôn có đúng 2 chữ số thập phân\n"
         "⚠️ Không được hiện dạng 26520 hay 26,520.00"),

        ("005", "Cột Trạng thái hiển thị đúng nhãn", "P0", PRE_LIST,
         "1. Mở màn hình\n2. Đối chiếu cột Trạng thái", "—",
         "- Tiền tệ đang dùng hiển thị nhãn \"Hoạt động\"\n"
         "- Tiền tệ bị khóa hiển thị nhãn \"Khóa\"\n"
         "- Không dòng nào để trống ô Trạng thái"),

        ("006", "Vị trí nút Khóa / Mở khóa", "P1", PRE_LIST,
         "1. Mở màn hình\n2. Nhìn cột Trạng thái và cột Hành động", "—",
         "- Nút Khóa (hình ổ khóa đóng) hoặc Mở khóa (hình ổ khóa mở) nằm ngay bên phải nhãn trạng "
         "thái, TRONG cột Trạng thái\n"
         "- Cột Hành động chỉ có 3 nút: Xem, Sửa, Xóa"),

        ("007", "Cột Cập nhật khi chưa có ngày cập nhật", "P2", PRE_LIST,
         "1. Mở màn hình\n2. Nhìn cột Cập nhật của mọi dòng", "—",
         "- Dòng có ngày cập nhật hiện đúng ngày giờ\n"
         "- Dòng chưa có ngày cập nhật hiện dấu gạch ngang, không để ô trắng trơn"),

        ("008", "Bảng trống khi bộ lọc không khớp gì", "P1", PRE_LIST,
         "1. Gõ vào ô tìm nhanh chuỗi \"khongtontai123\"\n2. Bấm Tìm kiếm", "khongtontai123",
         "- Bảng hiện dòng chữ \"Không có dữ liệu phù hợp bộ lọc.\"\n"
         "- Dòng Hiển thị dưới bảng cho tổng là 0\n"
         "- Nút Tạo mới và Xuất Excel vẫn còn"),

        ("009", "Vào màn hình khi danh mục rỗng", "P2",
         "Môi trường kiểm thử riêng, danh mục tiền tệ không có bản ghi nào.",
         "1. Mở màn Danh mục tiền tệ", "—",
         "- Màn hình mở bình thường, không báo lỗi\n"
         "- Bảng hiện thông báo không có dữ liệu, tổng là 0"),
    ]),

    ("II", "BỘ LỌC & TÌM KIẾM", [
        ("001", "Tìm nhanh theo Mã tiền tệ", "P0", PRE_LIST,
         "1. Gõ \"USD\" vào ô tìm nhanh\n2. Bấm Tìm kiếm", "USD",
         "- Kết quả chỉ còn dòng có mã USD\n"
         "- Tổng dưới bảng đổi theo số dòng khớp"),

        ("002", "Tìm nhanh theo Tên tiền tệ", "P0", PRE_LIST,
         "1. Gõ \"Đô la\" vào ô tìm nhanh\n2. Bấm Tìm kiếm", "Đô la",
         "- Kết quả gồm mọi tiền tệ có chuỗi \"Đô la\" trong Tên tiền tệ hoặc Tên gọi khác"),

        ("003", "Tìm nhanh theo Tên gọi khác", "P0", PRE_LIST,
         "1. Gõ đúng phần Tên gọi khác của một tiền tệ (ví dụ \"Đô la Mỹ\")\n2. Bấm Tìm kiếm",
         "Đô la Mỹ",
         "- Tiền tệ tương ứng vẫn ra kết quả dù chuỗi tìm chỉ nằm ở Tên gọi khác\n"
         "⚠️ Ô tìm nhanh phải quét cả 3 trường: Mã, Tên, Tên gọi khác (gợi ý ngay trong ô: "
         "\"Tìm theo mã, tên hoặc tên gọi khác...\")"),

        ("004", "Tìm nhanh khớp một phần chuỗi", "P1", PRE_LIST,
         "1. Gõ \"US\" (chỉ 2 ký tự đầu của USD)\n2. Bấm Tìm kiếm", "US",
         "- USD vẫn nằm trong kết quả\n"
         "⚠️ Không được yêu cầu gõ đúng nguyên mã mới ra kết quả"),

        ("005", "Tìm nhanh không phân biệt hoa thường", "P1", PRE_LIST,
         "1. Gõ \"usd\" bằng chữ thường\n2. Bấm Tìm kiếm", "usd",
         "- Kết quả giống hệt khi gõ \"USD\""),

        ("006", "Gõ ô tìm nhanh mà chưa bấm Tìm kiếm", "P1", PRE_LIST,
         "1. Gõ \"USD\" vào ô tìm nhanh\n2. KHÔNG bấm gì, chờ 5 giây\n3. Quan sát bảng", "USD",
         "- Bảng vẫn giữ nguyên 11 dòng, chưa lọc\n"
         "⚠️ Ô tìm nhanh chỉ có tác dụng sau khi bấm nút Tìm kiếm hoặc nhấn Enter"),

        ("007", "Lọc theo Trạng thái = Hoạt động", "P0", PRE_LIST,
         "1. Bấm mở bộ lọc nâng cao\n2. Chọn Trạng thái = Hoạt động\n3. Bấm Tìm kiếm",
         "Trạng thái: Hoạt động",
         "- Kết quả chỉ còn 9 dòng, tất cả đều mang nhãn Hoạt động\n"
         "- Không dòng nào mang nhãn Khóa"),

        ("008", "Lọc theo Trạng thái = Khóa", "P0", PRE_LIST,
         "1. Mở bộ lọc nâng cao\n2. Chọn Trạng thái = Khóa\n3. Bấm Tìm kiếm",
         "Trạng thái: Khóa",
         "- Kết quả chỉ còn 2 dòng, đều mang nhãn Khóa"),

        ("009", "Bỏ chọn Trạng thái bằng dấu x", "P1", PRE_LIST,
         "1. Chọn Trạng thái = Khóa, bấm Tìm kiếm\n2. Bấm dấu x trên ô Trạng thái để bỏ chọn\n"
         "3. Bấm Tìm kiếm", "Trạng thái: (bỏ trống)",
         "- Danh sách quay lại đủ 11 dòng\n"
         "⚠️ Ô Trạng thái không có lựa chọn \"Tất cả\"; bỏ lọc bằng cách bấm dấu x"),

        ("010", "Kết hợp tìm nhanh và lọc Trạng thái", "P0", PRE_LIST,
         "1. Gõ \"D\" vào ô tìm nhanh\n2. Chọn Trạng thái = Hoạt động\n3. Bấm Tìm kiếm",
         "Từ khóa: D; Trạng thái: Hoạt động",
         "- Kết quả phải thỏa ĐỒNG THỜI cả hai điều kiện\n"
         "- Không có dòng nào mang nhãn Khóa trong kết quả"),

        ("011", "Nút Làm mới xóa hết điều kiện và nạp lại", "P0", PRE_LIST,
         "1. Gõ từ khóa và chọn Trạng thái = Khóa, bấm Tìm kiếm\n2. Bấm nút Làm mới", "—",
         "- Ô tìm nhanh trống, ô Trạng thái trống\n"
         "- Danh sách tự nạp lại đủ 11 dòng NGAY, không cần bấm Tìm kiếm thêm lần nữa\n"
         "⚠️ Bẫy hay gặp: bấm Làm mới chỉ xóa chữ trong ô mà bảng vẫn giữ kết quả lọc cũ"),

        ("012", "Bộ lọc được nhớ khi quay lại màn trong 10 phút", "P1", PRE_LIST,
         "1. Chọn Trạng thái = Khóa, bấm Tìm kiếm\n2. Sang màn khác\n"
         "3. Trong vòng 10 phút quay lại Danh mục tiền tệ", "Trạng thái: Khóa",
         "- Ô Trạng thái vẫn đang là Khóa và danh sách vẫn đang lọc theo Khóa\n"
         "- Trạng thái đóng/mở của khối lọc nâng cao cũng được giữ nguyên"),

        ("013", "Bộ lọc hết hạn nhớ sau 10 phút", "P2", PRE_LIST,
         "1. Chọn Trạng thái = Khóa, bấm Tìm kiếm\n2. Sang màn khác và chờ quá 10 phút\n"
         "3. Quay lại Danh mục tiền tệ", "Trạng thái: Khóa",
         "- Bộ lọc trở về trống, danh sách hiện đủ 11 dòng"),

        ("014", "Lọc xong tự về trang 1", "P1",
         PRE_LIST + " Đang đứng ở trang 2 của danh sách.",
         "1. Chuyển sang trang 2\n2. Chọn Trạng thái = Hoạt động\n3. Bấm Tìm kiếm", "—",
         "- Kết quả hiển thị từ trang 1\n"
         "⚠️ Không được giữ nguyên trang 2 rồi báo bảng trống"),

        ("015", "Tìm nhanh với chuỗi có khoảng trắng thừa", "P2", PRE_LIST,
         "1. Gõ \"  USD  \" (có khoảng trắng đầu và cuối)\n2. Bấm Tìm kiếm", "  USD  ",
         "- Vẫn tìm ra USD, không báo không có dữ liệu"),

        ("016", "Tìm nhanh với ký tự đặc biệt", "P2", PRE_LIST,
         "1. Gõ chuỗi \"%'\" vào ô tìm nhanh\n2. Bấm Tìm kiếm", "%'",
         "- Màn hình không lỗi, không trắng trang\n"
         "- Hiện kết quả rỗng hoặc kết quả khớp đúng nghĩa đen của chuỗi đó"),
    ]),

    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", [
        ("001", "Sắp xếp theo Mã tiền tệ tăng dần", "P0", PRE_LIST,
         "1. Bấm tiêu đề cột Mã tiền tệ 1 lần\n2. Quan sát thứ tự các dòng", "—",
         "- Danh sách xếp theo mã từ A đến Z\n"
         "- Mũi tên trên tiêu đề cột chỉ chiều tăng dần"),

        ("002", "Sắp xếp theo Mã tiền tệ giảm dần", "P0", PRE_LIST,
         "1. Bấm tiêu đề cột Mã tiền tệ 2 lần\n2. Quan sát", "—",
         "- Danh sách xếp ngược từ Z về A, mũi tên đổi chiều"),

        ("003", "Sắp xếp theo Tên tiền tệ", "P1", PRE_LIST,
         "1. Bấm tiêu đề cột Tên tiền tệ\n2. Quan sát", "—",
         "- Danh sách xếp theo Tên tiền tệ, thứ tự thật sự thay đổi"),

        ("004", "Sắp xếp theo Tỷ giá", "P0", PRE_LIST,
         "1. Bấm tiêu đề cột Tỷ giá (VNĐ)\n2. Quan sát", "—",
         "- Danh sách xếp theo giá trị SỐ của tỷ giá, không phải theo chuỗi\n"
         "⚠️ Bẫy: nếu xếp theo chuỗi thì 9.000,00 sẽ đứng sau 26.520,00 — đó là lỗi"),

        ("005", "Sắp xếp theo Cập nhật", "P1", PRE_LIST,
         "1. Bấm tiêu đề cột Cập nhật\n2. Quan sát", "—",
         "- Danh sách xếp theo ngày giờ cập nhật, thứ tự thật sự thay đổi"),

        ("006", "Sắp xếp theo Trạng thái", "P2", PRE_LIST,
         "1. Bấm tiêu đề cột Trạng thái\n2. Quan sát", "—",
         "- Các dòng cùng trạng thái được gom lại liền nhau"),

        ("007", "Cột STT và cột Hành động không sắp xếp được", "P2", PRE_LIST,
         "1. Bấm tiêu đề cột STT\n2. Bấm tiêu đề cột Hành động", "—",
         "- Hai cột này không có mũi tên sắp xếp, bấm vào không đổi thứ tự và không lỗi"),

        ("008", "Sắp xếp giữ nguyên khi chuyển trang", "P1",
         PRE_LIST + " Đặt cỡ trang 10 để có 2 trang.",
         "1. Sắp xếp theo Tỷ giá giảm dần\n2. Chuyển sang trang 2", "—",
         "- Trang 2 tiếp nối đúng thứ tự đã sắp, không quay về thứ tự mặc định"),

        ("009", "Chuyển trang bằng nút số trang", "P0",
         PRE_LIST + " Cỡ trang đang là 10, danh mục có 11 dòng nên có 2 trang.",
         "1. Bấm số trang 2", "—",
         "- Bảng hiện dòng thứ 11\n"
         "- Cột STT bắt đầu từ 11\n"
         "- Dòng Hiển thị dưới bảng cập nhật đúng khoảng đang xem"),

        ("010", "Đổi cỡ trang", "P0", PRE_LIST,
         "1. Đổi cỡ trang từ 10 sang 50\n2. Quan sát", "Cỡ trang: 50",
         "- Toàn bộ 11 dòng hiện trên 1 trang\n"
         "- Danh sách chỉ nạp lại đúng MỘT lần, không nhấp nháy tải hai lượt"),

        ("011", "Đổi cỡ trang khi đang ở trang cuối", "P1",
         PRE_LIST + " Đang đứng ở trang 2 với cỡ trang 10.",
         "1. Đổi cỡ trang sang 50", "Cỡ trang: 50",
         "- Bảng hiện đủ dữ liệu từ trang 1, không hiện bảng trống\n"
         "⚠️ Bẫy phân trang: giữ nguyên số trang 2 sau khi tăng cỡ trang sẽ ra bảng rỗng"),

        ("012", "Vào màn hình chỉ gọi dữ liệu một lần", "P1", PRE_LIST,
         "1. Mở màn Danh mục tiền tệ từ menu\n2. Quan sát hiệu ứng tải của bảng", "—",
         "- Bảng chỉ tải MỘT lượt rồi đứng yên\n"
         "⚠️ Bẫy: bảng chớp tải hai lần liên tiếp khi vừa vào màn"),
    ]),

    ("IV", "THÊM / SỬA / XEM TIỀN TỆ", [
        ("001", "Mở cửa sổ Thêm tiền tệ", "P0", PRE_LIST,
         "1. Bấm nút Tạo mới", "—",
         "- Mở cửa sổ tiêu đề \"Thêm tiền tệ\"\n"
         "- Có 5 ô: Mã tiền tệ (bắt buộc), Trạng thái, Tên tiền tệ (bắt buộc), Tên gọi khác, "
         "Tỷ giá (VNĐ) (bắt buộc)\n"
         "- Ba ô bắt buộc có dấu sao đỏ bên cạnh nhãn\n"
         "- Cuối cửa sổ có 3 nút: Lưu, Lưu & Tiếp tục, Đóng"),

        ("002", "Thêm mới đầy đủ thông tin", "P0", PRE_LIST,
         "1. Bấm Tạo mới\n2. Nhập Mã tiền tệ, Tên tiền tệ, Tên gọi khác, Tỷ giá\n"
         "3. Chọn Trạng thái = Hoạt động\n4. Bấm Lưu",
         "Mã: TST; Tên: Tiền kiểm thử; Tên gọi khác: Đồng thử; Tỷ giá: 1.234,56; "
         "Trạng thái: Hoạt động",
         "- Hiện thông báo \"Thêm mới thành công\"\n"
         "- Cửa sổ đóng lại, danh sách nạp lại và có dòng TST\n"
         "- Cột Tỷ giá của dòng mới hiện 1.234,56\n"
         "- Cột Tên tiền tệ hiện \"Tiền kiểm thử\" và dòng phụ \"Tên gọi khác: Đồng thử\""),

        ("003", "Thêm mới chỉ nhập các ô bắt buộc", "P0", PRE_LIST,
         "1. Bấm Tạo mới\n2. Chỉ nhập Mã tiền tệ, Tên tiền tệ, Tỷ giá\n3. Bấm Lưu",
         "Mã: TS2; Tên: Tiền thử 2; Tỷ giá: 100,00",
         "- Lưu thành công\n"
         "- Dòng mới không có dòng phụ Tên gọi khác\n"
         "- Trạng thái mặc định là Hoạt động"),

        ("004", "Nút Lưu & Tiếp tục giữ cửa sổ để nhập tiếp", "P1", PRE_LIST,
         "1. Bấm Tạo mới\n2. Nhập đủ thông tin\n3. Bấm Lưu & Tiếp tục",
         "Mã: TS3; Tên: Tiền thử 3; Tỷ giá: 50,00",
         "- Hiện thông báo thêm mới thành công\n"
         "- Cửa sổ VẪN mở và các ô đã được xóa trắng để nhập bản ghi tiếp theo\n"
         "- Tiêu đề vẫn là \"Thêm tiền tệ\""),

        ("005", "Cửa sổ Sửa không có nút Lưu & Tiếp tục", "P1", PRE_LIST,
         "1. Bấm nút Sửa trên dòng USD\n2. Nhìn cụm nút cuối cửa sổ", "—",
         "- Chỉ có 2 nút: Lưu và Đóng\n"
         "⚠️ Nút Lưu & Tiếp tục chỉ dành cho thêm mới"),

        ("006", "Mở cửa sổ Sửa nạp đúng dữ liệu cũ", "P0", PRE_LIST,
         "1. Bấm nút Sửa trên dòng USD", "—",
         "- Tiêu đề cửa sổ là \"Sửa tiền tệ\"\n"
         "- Các ô điền sẵn đúng dữ liệu đang có của USD: mã, tên, tên gọi khác, tỷ giá, trạng thái\n"
         "- Cạnh tiêu đề có hiện thông tin lần cập nhật gần nhất"),

        ("007", "Sửa Tên tiền tệ", "P0", PRE_LIST,
         "1. Bấm Sửa dòng TST\n2. Đổi Tên tiền tệ\n3. Bấm Lưu",
         "Tên tiền tệ: Tiền kiểm thử (đã sửa)",
         "- Hiện thông báo \"Cập nhật thành công\"\n"
         "- Danh sách hiện tên mới, cột Cập nhật đổi sang thời điểm vừa sửa"),

        ("008", "Sửa Tỷ giá", "P0", PRE_LIST,
         "1. Bấm Sửa dòng TST\n2. Đổi Tỷ giá\n3. Bấm Lưu", "Tỷ giá: 9.876,54",
         "- Cập nhật thành công\n"
         "- Cột Tỷ giá hiện 9.876,54"),

        ("009", "Sửa Mã tiền tệ sang mã chưa tồn tại", "P1", PRE_LIST,
         "1. Bấm Sửa dòng TST\n2. Đổi Mã tiền tệ thành TSX\n3. Bấm Lưu", "Mã tiền tệ: TSX",
         "- Cập nhật thành công, danh sách hiện mã TSX"),

        ("010", "Xóa trắng Tên gọi khác đang có", "P1", PRE_LIST,
         "1. Bấm Sửa dòng có Tên gọi khác\n2. Xóa trắng ô Tên gọi khác\n3. Bấm Lưu",
         "Tên gọi khác: (để trống)",
         "- Cập nhật thành công\n"
         "- Dòng đó không còn dòng phụ Tên gọi khác trong danh sách"),

        ("011", "Nút Xem mở ở chế độ chỉ đọc", "P0", PRE_LIST,
         "1. Bấm nút Xem (hình con mắt) trên dòng USD", "—",
         "- Tiêu đề cửa sổ là \"Xem tiền tệ\"\n"
         "- Mọi ô đều mờ, không gõ được, không chọn được\n"
         "- KHÔNG có nút Lưu; chỉ có nút Đóng"),

        ("012", "Người chỉ có quyền Xem vẫn mở được cửa sổ Xem", "P1",
         "Đăng nhập bằng tài khoản chỉ có quyền \"Xem danh mục tiền tệ\".",
         "1. Bấm nút Xem trên một dòng bất kỳ", "—",
         "- Cửa sổ Xem tiền tệ mở bình thường, hiện đủ thông tin, không có nút Lưu"),

        ("013", "Bấm Đóng khi chưa sửa gì", "P1", PRE_LIST,
         "1. Bấm Sửa một dòng\n2. Không thay đổi gì\n3. Bấm Đóng", "—",
         "- Cửa sổ đóng ngay, KHÔNG hỏi lại\n"
         "- Danh sách giữ nguyên"),

        ("014", "Cảnh báo khi đóng lúc đang sửa dở", "P0", PRE_LIST,
         "1. Bấm Sửa một dòng\n2. Sửa Tên tiền tệ nhưng chưa bấm Lưu\n3. Bấm Đóng",
         "Tên tiền tệ: sửa dở dang",
         "- Hệ thống cảnh báo dữ liệu chưa được lưu và hỏi xác nhận trước khi đóng\n"
         "- Chọn ở lại thì cửa sổ vẫn mở và giữ nguyên nội dung đang gõ\n"
         "- Chọn thoát thì cửa sổ đóng và dữ liệu cũ không bị đổi"),

        ("015", "Đóng cửa sổ bằng dấu X góc phải", "P1", PRE_LIST,
         "1. Bấm Tạo mới\n2. Nhập vài ô\n3. Bấm dấu X ở góc trên bên phải cửa sổ", "Mã: ABC",
         "- Hành xử giống nút Đóng: có cảnh báo chưa lưu"),

        ("016", "Chống bấm Lưu nhiều lần liên tiếp", "P1", PRE_LIST,
         "1. Bấm Tạo mới, nhập đủ thông tin\n2. Bấm Lưu liên tiếp 3 lần thật nhanh",
         "Mã: TS9; Tên: Tiền thử 9; Tỷ giá: 10,00",
         "- Chỉ tạo ra ĐÚNG 1 bản ghi TS9\n"
         "- Nút Lưu bị vô hiệu trong lúc đang xử lý"),

        ("017", "Thêm mới rồi kiểm tra ở cổng cũ", "P2", PRE_LIST,
         "1. Thêm mới tiền tệ TST ở màn này\n2. Mở màn Danh mục tiền tệ ở cổng cũ", "Mã: TST",
         "- Tiền tệ TST cũng hiện ở cổng cũ với đúng mã, tên, tỷ giá\n"
         "⚠️ Hai cổng dùng chung một danh mục — sai lệch giữa hai bên là lỗi"),
    ]),

    ("V", "KHÓA & MỞ KHÓA", [
        ("001", "Khóa một tiền tệ đang Hoạt động", "P0", PRE_LIST,
         "1. Bấm nút Khóa (hình ổ khóa) ở cột Trạng thái của dòng TST\n"
         "2. Đọc nội dung hộp xác nhận\n3. Bấm Khóa", "Tiền tệ: TST",
         "- Hộp xác nhận có tiêu đề \"Xác nhận khóa\" và câu hỏi nêu đúng tên tiền tệ\n"
         "- Sau khi xác nhận: thông báo \"Khóa thành công\"\n"
         "- Dòng TST đổi nhãn sang Khóa, nút trong cột Trạng thái đổi thành hình ổ khóa mở"),

        ("002", "Mở khóa một tiền tệ đang Khóa", "P0",
         PRE_LIST + " Tiền tệ TST hiện đang ở trạng thái Khóa.",
         "1. Bấm nút Mở khóa ở cột Trạng thái dòng TST\n2. Bấm Mở khóa trong hộp xác nhận",
         "Tiền tệ: TST",
         "- Hộp xác nhận có tiêu đề \"Xác nhận mở khóa\"\n"
         "- Thông báo \"Mở khóa thành công\"\n"
         "- Dòng TST quay lại nhãn Hoạt động"),

        ("003", "Hủy hộp xác nhận khóa", "P1", PRE_LIST,
         "1. Bấm nút Khóa trên dòng TST\n2. Bấm Hủy", "Tiền tệ: TST",
         "- Hộp đóng lại, trạng thái TST KHÔNG đổi\n"
         "- Không có thông báo thành công nào"),

        ("004", "Khóa tiền tệ đang được dùng ở chứng từ khác", "P1",
         PRE_LIST + " Tiền tệ USD đang được dùng ở nhiều chứng từ.",
         "1. Bấm nút Khóa trên dòng USD\n2. Xác nhận", "Tiền tệ: USD",
         "- Khóa được bình thường (khóa chỉ ngăn dùng MỚI, không ảnh hưởng chứng từ đã lập)\n"
         "⚠️ Khác với Xóa — Xóa mới bị chặn khi đang được dùng"),

        ("005", "Tiền tệ đã khóa không còn được chọn ở màn nghiệp vụ", "P0",
         PRE_LIST + " Tiền tệ TST đang ở trạng thái Khóa và chưa được dùng ở chứng từ nào.",
         "1. Mở một màn có chọn tiền tệ (ví dụ lập báo giá)\n2. Mở danh sách chọn tiền tệ",
         "Tiền tệ: TST",
         "- TST KHÔNG có trong danh sách chọn"),

        ("006", "Chứng từ cũ vẫn hiện đúng tiền tệ đã bị khóa", "P0",
         "Có sẵn 1 báo giá đã lập với tiền tệ USD; sau đó USD bị chuyển sang trạng thái Khóa.",
         "1. Khóa tiền tệ USD\n2. Mở lại báo giá cũ ở chế độ Sửa", "Tiền tệ: USD (đang Khóa)",
         "- Ô tiền tệ của báo giá vẫn hiện đúng \"USD\", không bị trống, không tự nhảy sang tiền tệ khác\n"
         "- Lưu lại báo giá không làm mất giá trị tiền tệ\n"
         "⚠️ Đây là quy tắc chung toàn hệ thống: danh mục bị khóa vẫn phải hiện ở bản ghi đang dùng nó"),

        ("007", "Người chỉ có quyền Xem không thấy nút Khóa", "P0",
         "Đăng nhập bằng tài khoản chỉ có quyền \"Xem danh mục tiền tệ\".",
         "1. Mở màn hình\n2. Nhìn cột Trạng thái", "—",
         "- Cột Trạng thái chỉ có nhãn trạng thái, không có nút Khóa / Mở khóa"),

        ("008", "Khóa rồi lọc lại theo trạng thái", "P1", PRE_LIST,
         "1. Khóa tiền tệ TST\n2. Lọc Trạng thái = Hoạt động\n3. Lọc lại Trạng thái = Khóa",
         "Tiền tệ: TST",
         "- Ở bước 2 không có TST trong kết quả\n- Ở bước 3 có TST trong kết quả"),
    ]),

    ("VI", "XÓA", [
        ("001", "Xóa tiền tệ chưa dùng ở đâu", "P0",
         PRE_LIST + " Tiền tệ TST chưa được dùng ở bất kỳ chứng từ nào.",
         "1. Bấm nút Xóa trên dòng TST\n2. Đọc hộp xác nhận\n3. Bấm Xóa", "Tiền tệ: TST",
         "- Hộp xác nhận tiêu đề \"Xác nhận xóa\", câu hỏi nêu đúng tên tiền tệ\n"
         "- Thông báo \"Xóa thành công\"\n"
         "- Dòng TST biến mất, tổng dưới bảng giảm 1"),

        ("002", "Hủy hộp xác nhận xóa", "P0", PRE_LIST,
         "1. Bấm nút Xóa trên dòng TST\n2. Bấm Hủy", "Tiền tệ: TST",
         "- Hộp đóng, dòng TST vẫn còn nguyên"),

        ("003", "Nút Xóa bị vô hiệu với tiền tệ đang được dùng", "P0",
         PRE_LIST + " Tiền tệ USD đang được dùng ở đề nghị thu tiền và công nợ khách hàng.",
         "1. Mở màn hình, chờ bảng hiện xong khoảng 2 giây\n2. Rê chuột vào nút Xóa của dòng USD",
         "Tiền tệ: USD",
         "- Nút Xóa bị mờ, không bấm được\n"
         "- Rê chuột hiện chú thích cho biết tiền tệ đang được sử dụng\n"
         "⚠️ Trạng thái mờ xuất hiện chậm hơn bảng vài trăm mili giây — đó là thiết kế, không phải lỗi"),

        ("004", "Chặn xóa khi bấm ngay lúc nút chưa kịp mờ", "P0",
         PRE_LIST + " Tiền tệ USD đang được dùng ở chứng từ khác.",
         "1. Mở màn hình và bấm NGAY nút Xóa của dòng USD trong 1 giây đầu", "Tiền tệ: USD",
         "- Hệ thống KHÔNG mở hộp xác nhận\n"
         "- Hiện thông báo đỏ nêu tiền tệ đang được dùng ở đâu (tối đa 3 nơi) kèm gợi ý "
         "\"Hãy chuyển sang trạng thái Khóa.\"\n"
         "- Tiền tệ USD vẫn còn nguyên"),

        ("005", "Thông báo chặn xóa nêu tên nơi đang dùng", "P1",
         PRE_LIST + " Tiền tệ USD đang được dùng ở ít nhất 4 loại chứng từ khác nhau.",
         "1. Bấm nút Xóa dòng USD ngay khi bảng vừa hiện\n2. Đọc kỹ nội dung thông báo",
         "Tiền tệ: USD",
         "- Thông báo nêu tên nghiệp vụ đang dùng bằng tiếng Việt dễ hiểu, không quá 3 nơi\n"
         "- Không hiện tên kỹ thuật khó hiểu với người dùng"),

        ("006", "Xóa tiền tệ vừa mới bị người khác dùng", "P1",
         "Hai tài khoản cùng thao tác. Tiền tệ TST ban đầu chưa dùng ở đâu.",
         "1. Tài khoản 1 mở màn Danh mục tiền tệ (nút Xóa của TST đang sáng)\n"
         "2. Tài khoản 2 lập một báo giá dùng tiền tệ TST\n"
         "3. Tài khoản 1 bấm Xóa dòng TST và xác nhận", "Tiền tệ: TST",
         "- Hệ thống chặn lại, báo tiền tệ đang được dùng\n"
         "- TST vẫn còn trong danh sách\n"
         "⚠️ Kiểm tra phải được thực hiện lại tại thời điểm xóa, không tin vào trạng thái nút lúc mở màn"),

        ("007", "Xóa dòng cuối cùng của trang", "P1",
         PRE_LIST + " Đang ở trang 2, trang 2 chỉ còn đúng 1 dòng và dòng đó xóa được.",
         "1. Xóa dòng duy nhất của trang 2", "—",
         "- Xóa thành công\n"
         "- Màn tự lùi về trang 1 và hiện dữ liệu, KHÔNG hiện bảng trống"),

        ("008", "Xóa tiền tệ đang ở trạng thái Khóa", "P2",
         PRE_LIST + " Tiền tệ TST đang ở trạng thái Khóa và chưa dùng ở đâu.",
         "1. Bấm Xóa dòng TST và xác nhận", "Tiền tệ: TST",
         "- Xóa được bình thường; trạng thái Khóa không cản việc xóa"),

        ("009", "Người chỉ có quyền Xem không thấy nút Xóa", "P0",
         "Đăng nhập bằng tài khoản chỉ có quyền \"Xem danh mục tiền tệ\".",
         "1. Mở màn hình, nhìn cột Hành động", "—",
         "- Chỉ có nút Xem, không có nút Xóa"),
    ]),

    ("VII", "XUẤT EXCEL", [
        ("001", "Xuất Excel toàn bộ danh mục", "P0", PRE_LIST,
         "1. Không lọc gì\n2. Bấm nút Xuất Excel\n3. Mở file tải về", "—",
         "- Hiện thông báo \"Xuất Excel thành công\"\n"
         "- File tải về mở được bằng Excel\n"
         "- Nội dung có đủ 11 tiền tệ"),

        ("002", "File Excel có đủ cột như trên màn hình", "P0", PRE_LIST,
         "1. Bấm Xuất Excel\n2. Đối chiếu tiêu đề cột trong file với bảng trên màn hình", "—",
         "- File có các cột Mã tiền tệ, Tên tiền tệ, Tên gọi khác, Tỷ giá, Trạng thái\n"
         "- Tiêu đề cột viết bằng tiếng Việt giống trên màn hình"),

        ("003", "Xuất Excel theo đúng bộ lọc đang áp dụng", "P0", PRE_LIST,
         "1. Lọc Trạng thái = Khóa (còn 2 dòng)\n2. Bấm Xuất Excel\n3. Mở file",
         "Trạng thái: Khóa",
         "- File chỉ chứa đúng 2 dòng đang lọc\n"
         "⚠️ Bẫy hay gặp: file xuất ra toàn bộ danh mục, bỏ qua bộ lọc"),

        ("004", "Xuất Excel theo từ khóa tìm nhanh", "P1", PRE_LIST,
         "1. Gõ \"USD\" và bấm Tìm kiếm\n2. Bấm Xuất Excel\n3. Mở file", "USD",
         "- File chỉ chứa các dòng khớp từ khóa"),

        ("005", "Xuất Excel lấy đủ dữ liệu, không chỉ trang hiện tại", "P0",
         PRE_LIST + " Cỡ trang đang là 10, danh mục có 11 dòng.",
         "1. Đứng ở trang 1\n2. Bấm Xuất Excel\n3. Đếm số dòng trong file", "—",
         "- File có đủ 11 dòng\n"
         "⚠️ Bẫy: file chỉ có 10 dòng của trang đang xem"),

        ("006", "Định dạng tỷ giá trong file Excel", "P1", PRE_LIST,
         "1. Xuất Excel\n2. Nhìn cột Tỷ giá trong file", "—",
         "- Tỷ giá hiển thị đúng giá trị, đọc được, không mất phần thập phân"),

        ("007", "Xuất Excel khi kết quả lọc rỗng", "P2", PRE_LIST,
         "1. Lọc ra kết quả rỗng\n2. Bấm Xuất Excel", "Từ khóa: khongtontai123",
         "- Hệ thống không lỗi\n"
         "- Tải về file chỉ có dòng tiêu đề, hoặc báo không có dữ liệu để xuất"),

        ("008", "Người chỉ có quyền Xem vẫn xuất được Excel", "P1",
         "Đăng nhập bằng tài khoản chỉ có quyền \"Xem danh mục tiền tệ\".",
         "1. Bấm Xuất Excel", "—",
         "- Xuất được bình thường, có thông báo thành công"),
    ]),

    ("VIII", "RÀNG BUỘC NHẬP LIỆU", [
        ("001", "Bỏ trống cả 3 ô bắt buộc", "P0", PRE_LIST,
         "1. Bấm Tạo mới\n2. Không nhập gì\n3. Bấm Lưu", "(để trống hết)",
         "- Cả 3 ô Mã tiền tệ, Tên tiền tệ, Tỷ giá (VNĐ) viền đỏ và hiện chữ đỏ "
         "\"Bắt buộc phải nhập\" ngay dưới ô\n"
         "- Cửa sổ KHÔNG đóng, không tạo bản ghi nào"),

        ("002", "Bỏ trống riêng Mã tiền tệ", "P0", PRE_LIST,
         "1. Bấm Tạo mới\n2. Nhập Tên tiền tệ và Tỷ giá, để trống Mã\n3. Bấm Lưu",
         "Tên: Tiền thử; Tỷ giá: 100,00",
         "- Chỉ ô Mã tiền tệ báo \"Bắt buộc phải nhập\"\n"
         "- Dữ liệu đã nhập ở các ô khác vẫn còn nguyên"),

        ("003", "Nhập trùng Mã tiền tệ đã có", "P0", PRE_LIST,
         "1. Bấm Tạo mới\n2. Nhập Mã = USD (đã tồn tại)\n3. Nhập tên và tỷ giá\n4. Bấm Lưu",
         "Mã: USD; Tên: Trùng mã; Tỷ giá: 1,00",
         "- Ô Mã tiền tệ báo \"Mã tiền tệ đã tồn tại\"\n"
         "- Không tạo thêm bản ghi, danh sách vẫn 11 dòng"),

        ("004", "Sửa Mã tiền tệ sang mã của tiền tệ khác", "P0", PRE_LIST,
         "1. Bấm Sửa dòng TST\n2. Đổi Mã thành USD\n3. Bấm Lưu", "Mã: USD",
         "- Báo \"Mã tiền tệ đã tồn tại\", không lưu"),

        ("005", "Sửa mà giữ nguyên Mã của chính nó", "P0", PRE_LIST,
         "1. Bấm Sửa dòng USD\n2. Giữ nguyên Mã, chỉ đổi Tên\n3. Bấm Lưu",
         "Mã: USD (không đổi); Tên: Đô la Mỹ mới",
         "- Lưu thành công\n"
         "⚠️ Bẫy hay gặp: hệ thống coi mã của chính bản ghi đang sửa là trùng và chặn nhầm"),

        ("006", "Nhập Tỷ giá bằng 0", "P0", PRE_LIST,
         "1. Bấm Tạo mới\n2. Nhập Tỷ giá = 0\n3. Bấm Lưu", "Tỷ giá: 0",
         "- Ô Tỷ giá báo \"Tỷ giá phải lớn hơn 0\", không lưu"),

        ("007", "Nhập Tỷ giá âm", "P0", PRE_LIST,
         "1. Bấm Tạo mới\n2. Nhập Tỷ giá = -100\n3. Bấm Lưu", "Tỷ giá: -100",
         "- Ô Tỷ giá báo lỗi phải lớn hơn 0, không lưu"),

        ("008", "Nhập Tỷ giá bằng chữ", "P0", PRE_LIST,
         "1. Bấm Tạo mới\n2. Nhập Tỷ giá = \"abc\"\n3. Bấm Lưu", "Tỷ giá: abc",
         "- Ô Tỷ giá báo \"Tỷ giá phải là số\", không lưu"),

        ("009", "Nhập Tỷ giá vượt trần cho phép", "P0", PRE_LIST,
         "1. Bấm Tạo mới\n2. Nhập Tỷ giá = 1.000.000,00\n3. Bấm Lưu", "Tỷ giá: 1.000.000,00",
         "- Ô Tỷ giá báo \"Tỷ giá tối đa 999.999,99\", không lưu\n"
         "⚠️ Đây là trần cứng của hệ thống, không được lưu vượt rồi hiện sai số"),

        ("010", "Nhập Tỷ giá đúng sát trần", "P1", PRE_LIST,
         "1. Bấm Tạo mới\n2. Nhập Tỷ giá = 999.999,99\n3. Bấm Lưu",
         "Mã: MAX; Tên: Sát trần; Tỷ giá: 999.999,99",
         "- Lưu thành công\n- Danh sách hiện đúng 999.999,99, không làm tròn sai"),

        ("011", "Nhập Tỷ giá dùng dấu phẩy thập phân", "P0", PRE_LIST,
         "1. Bấm Tạo mới\n2. Nhập Tỷ giá = 26.520,75\n3. Bấm Lưu",
         "Tỷ giá: 26.520,75",
         "- Lưu thành công và danh sách hiện đúng 26.520,75\n"
         "⚠️ Bẫy hay gặp nhất của màn này: hệ thống hiểu nhầm dấu phẩy thành dấu ngăn hàng nghìn "
         "và lưu ra con số sai hẳn"),

        ("012", "Nhập Tỷ giá có nhiều hơn 2 chữ số thập phân", "P1", PRE_LIST,
         "1. Bấm Tạo mới\n2. Nhập Tỷ giá = 1,239\n3. Bấm Lưu", "Tỷ giá: 1,239",
         "- Hệ thống hoặc chặn với thông báo rõ ràng, hoặc làm tròn về 2 chữ số thập phân\n"
         "- Không được lưu ra giá trị khác hẳn giá trị đã nhập"),

        ("013", "Nhập Mã tiền tệ dài hơn 255 ký tự", "P2", PRE_LIST,
         "1. Bấm Tạo mới\n2. Dán chuỗi 300 ký tự vào ô Mã tiền tệ\n3. Bấm Lưu",
         "Mã: chuỗi 300 ký tự",
         "- Báo \"Tối đa 255 ký tự\" ngay dưới ô Mã tiền tệ, không lưu"),

        ("014", "Nhập Tên tiền tệ dài hơn 255 ký tự", "P2", PRE_LIST,
         "1. Bấm Tạo mới\n2. Dán chuỗi 300 ký tự vào ô Tên tiền tệ\n3. Bấm Lưu",
         "Tên: chuỗi 300 ký tự",
         "- Báo \"Tối đa 255 ký tự\", không lưu"),

        ("015", "Nhập Tên gọi khác dài hơn 255 ký tự", "P2", PRE_LIST,
         "1. Bấm Tạo mới\n2. Dán chuỗi 300 ký tự vào ô Tên gọi khác\n3. Bấm Lưu",
         "Tên gọi khác: chuỗi 300 ký tự",
         "- Báo \"Tối đa 255 ký tự\", không lưu"),

        ("016", "Nhập tên có dấu tiếng Việt", "P1", PRE_LIST,
         "1. Bấm Tạo mới\n2. Nhập Tên tiền tệ có dấu đầy đủ\n3. Bấm Lưu",
         "Mã: VND2; Tên: Đồng Việt Nam kiểm thử; Tỷ giá: 1,00",
         "- Lưu thành công\n- Danh sách hiện đúng dấu tiếng Việt, không bị lỗi phông"),

        ("017", "Lỗi biến mất sau khi sửa lại đúng", "P1", PRE_LIST,
         "1. Bấm Tạo mới, bấm Lưu ngay để 3 ô bắt buộc báo đỏ\n"
         "2. Nhập đủ 3 ô bắt buộc\n3. Bấm Lưu", "Mã: OK1; Tên: Hết lỗi; Tỷ giá: 5,00",
         "- Viền đỏ và chữ đỏ biến mất khi nhập đủ\n- Lưu thành công"),

        ("018", "Khoảng trắng đầu cuối trong Mã tiền tệ", "P2", PRE_LIST,
         "1. Bấm Tạo mới\n2. Nhập Mã = \"  ABC  \"\n3. Bấm Lưu và xem danh sách",
         "Mã: \"  ABC  \"",
         "- Danh sách hiện mã ABC không có khoảng trắng thừa hai đầu\n"
         "- Không tạo được 2 tiền tệ mà mắt thường nhìn thấy mã giống hệt nhau"),
    ]),

    ("IX", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", [
        ("001", "Hai người cùng sửa một tiền tệ", "P1",
         "Hai tài khoản đều có quyền Quản lý danh mục tiền tệ, cùng mở cửa sổ Sửa của tiền tệ TST.",
         "1. Tài khoản 1 đổi Tên và bấm Lưu\n"
         "2. Tài khoản 2 (vẫn đang mở cửa sổ với dữ liệu cũ) đổi Tỷ giá và bấm Lưu\n"
         "3. Nạp lại danh sách", "TK1 đổi Tên; TK2 đổi Tỷ giá",
         "- Cả hai thao tác đều lưu được\n"
         "- Kết quả cuối là bản của người lưu sau; hệ thống không lỗi, không nhân đôi bản ghi"),

        ("002", "Sửa một tiền tệ vừa bị người khác xóa", "P1",
         "Hai tài khoản đều có quyền Quản lý. Tiền tệ TST chưa dùng ở đâu.",
         "1. Tài khoản 1 mở cửa sổ Sửa của TST\n2. Tài khoản 2 xóa TST\n"
         "3. Tài khoản 1 bấm Lưu", "Tiền tệ: TST",
         "- Hệ thống báo dữ liệu đã thay đổi hoặc không còn tồn tại\n"
         "- Màn hình KHÔNG treo, không trắng trang; nạp lại danh sách thì TST đã mất"),

        ("003", "Khóa một tiền tệ vừa bị người khác xóa", "P2",
         "Tương tự trên nhưng thao tác là Khóa.",
         "1. Tài khoản 1 mở danh sách\n2. Tài khoản 2 xóa TST\n"
         "3. Tài khoản 1 bấm nút Khóa dòng TST", "Tiền tệ: TST",
         "- Hệ thống báo dữ liệu đã thay đổi, không treo trang"),

        ("004", "Cả hai cùng tạo tiền tệ cùng mã", "P1",
         "Hai tài khoản đều có quyền Quản lý.",
         "1. Cả hai cùng mở cửa sổ Tạo mới và nhập Mã = TSX\n"
         "2. Tài khoản 1 bấm Lưu\n3. Tài khoản 2 bấm Lưu", "Mã: TSX (cả hai)",
         "- Người thứ nhất lưu thành công\n"
         "- Người thứ hai bị chặn với thông báo \"Mã tiền tệ đã tồn tại\"\n"
         "- Danh mục chỉ có ĐÚNG 1 tiền tệ mã TSX"),

        ("005", "Ảnh hưởng của việc cập nhật tỷ giá tự động hằng ngày", "P1",
         "Tiền tệ USD có tỷ giá đang được sửa tay thành 1.000,00 vào hôm trước.",
         "1. Sửa tỷ giá USD thành 1.000,00 và lưu\n"
         "2. Sang ngày hôm sau (sau 03:00) mở lại màn hình", "Tỷ giá: 1.000,00",
         "- Tỷ giá USD đã được hệ thống tự cập nhật lại theo tỷ giá bán của Vietcombank\n"
         "- Cột Cập nhật đổi sang thời điểm cập nhật tự động\n"
         "⚠️ Đây là hành vi ĐÚNG theo thiết kế, không phải lỗi mất dữ liệu"),

        ("006", "VNĐ không bị cập nhật tự động", "P1",
         "Danh mục có tiền tệ mã VNĐ.",
         "1. Ghi lại tỷ giá của VNĐ\n2. Sang ngày hôm sau (sau 03:00) kiểm tra lại", "Tiền tệ: VNĐ",
         "- Tỷ giá VNĐ giữ nguyên, không bị cập nhật tự động"),

        ("007", "Tiền tệ đứng đầu danh sách nguồn cũng được cập nhật", "P1",
         "Tiền tệ AUD là dòng đầu tiên trong bảng tỷ giá nguồn của Vietcombank.",
         "1. Ghi lại tỷ giá và ngày cập nhật của AUD\n"
         "2. Sang ngày hôm sau (sau 03:00) kiểm tra lại", "Tiền tệ: AUD",
         "- Tỷ giá AUD được cập nhật, cột Cập nhật đổi sang ngày mới\n"
         "⚠️ Lỗi cũ của hệ thống trước đây: đồng tiền đứng ĐẦU danh sách nguồn không bao giờ được "
         "cập nhật, đứng yên nhiều tháng. Đây là trường hợp bắt buộc phải kiểm"),

        ("008", "Danh mục dùng chung cho mọi công ty", "P1",
         "Hai tài khoản thuộc hai công ty khác nhau, đều có quyền Xem danh mục tiền tệ.",
         "1. Cả hai cùng mở màn Danh mục tiền tệ\n2. So sánh số dòng và nội dung", "—",
         "- Hai người thấy DANH SÁCH GIỐNG HỆT NHAU\n"
         "⚠️ Danh mục này cố ý không phân theo công ty — thấy khác nhau mới là lỗi"),
    ]),

    ("X", "LUỒNG XUYÊN SUỐT", [
        ("001", "Vòng đời đầy đủ của một tiền tệ", "P0", PRE_LIST,
         "1. Tạo mới tiền tệ TST\n2. Tìm lại TST bằng ô tìm nhanh\n3. Sửa tỷ giá của TST\n"
         "4. Khóa TST\n5. Mở khóa TST\n6. Xuất Excel và kiểm tra có TST\n7. Xóa TST",
         "Mã: TST; Tên: Tiền kiểm thử; Tỷ giá ban đầu 100,00 → sửa thành 200,00",
         "- Từng bước đều có thông báo thành công tương ứng\n"
         "- Sau bước 7, TST không còn trong danh sách và không còn trong file Excel xuất lại"),

        ("002", "Tiền tệ mới dùng được ngay ở màn nghiệp vụ", "P0", PRE_LIST,
         "1. Tạo mới tiền tệ TST ở trạng thái Hoạt động\n"
         "2. Mở màn lập báo giá\n3. Mở danh sách chọn tiền tệ",
         "Mã: TST; Trạng thái: Hoạt động",
         "- TST có trong danh sách chọn và chọn được\n"
         "- Tỷ giá áp dụng đúng bằng tỷ giá vừa khai trong danh mục"),

        ("003", "Khóa để ngừng dùng thay vì xóa", "P0",
         PRE_LIST + " Tiền tệ USD đang được dùng ở nhiều chứng từ.",
         "1. Thử xóa USD → bị chặn kèm gợi ý chuyển sang trạng thái Khóa\n"
         "2. Bấm nút Khóa dòng USD và xác nhận\n"
         "3. Mở màn lập báo giá và tìm USD trong danh sách chọn\n"
         "4. Mở lại một chứng từ cũ đã dùng USD", "Tiền tệ: USD",
         "- Bước 1 bị chặn đúng như mong đợi\n"
         "- Bước 2 khóa thành công\n"
         "- Bước 3 USD không còn chọn được cho chứng từ mới\n"
         "- Bước 4 chứng từ cũ vẫn hiện đúng USD"),

        ("004", "Kiểm tra nhất quán giữa hai cổng", "P1", PRE_LIST,
         "1. Tạo mới tiền tệ TST ở cổng mới\n2. Mở danh mục tiền tệ ở cổng cũ, tìm TST\n"
         "3. Sửa tỷ giá của TST ở cổng cũ\n4. Quay lại cổng mới, nạp lại danh sách",
         "Mã: TST; Tỷ giá sửa ở cổng cũ: 555,55",
         "- Bước 2: cổng cũ thấy TST\n"
         "- Bước 4: cổng mới hiện tỷ giá 555,55\n"
         "⚠️ Hai cổng dùng chung một danh mục, mọi sai lệch đều là lỗi"),
    ]),
]

build(output_file=OUTPUT_FILE, sheet_name=SHEET_NAME, feature_name=FEATURE_NAME,
      module_name=MODULE_NAME, description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS, sections=SECTIONS)
