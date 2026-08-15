# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man Danh muc khach hang (/assign/customers).

Chay:  python .plans/gop-db/customer-docs/gen_testcase.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills",
                                "testcase-documenter", "assets"))
sys.path.insert(0, HERE)
from tc_engine import build  # noqa: E402
from tc_sections_a import SEC_I, SEC_II, SEC_III, SEC_IV  # noqa: E402
from tc_sections_b import SEC_V  # noqa: E402
from tc_sections_c import SEC_VI, SEC_VII, SEC_VIII, SEC_IX, SEC_X  # noqa: E402

MODULE = "Danh mục khách hàng"

# ----------------------------------------------------------------- 9 muc mo ta
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Quản lý tập trung toàn bộ khách hàng của hệ thống sau khi gộp dữ liệu hai phần mềm cũ. "
     "Màn hình cho phép tra cứu, lọc nhiều tiêu chí, thêm mới, sửa, xem chi tiết, khóa/mở khóa, "
     "xem lịch sử thay đổi, nhập hàng loạt từ file Excel và xuất danh sách ra CSV / Excel / PDF. "
     "Từ mỗi dòng còn mở được màn Quản lý khách hàng gồm 6 thẻ: Thông tin chung, Thông tin liên hệ, Báo giá, Hợp đồng, "
     "Danh sách trang thiết bị, Thông tin khác."),

    ("2. Đối tượng được tính / hiển thị",
     "- Tất cả khách hàng còn hiệu lực (trạng thái Hoạt động) và khách hàng đã Khóa — cột Trạng thái "
     "phân biệt hai nhóm này, mặc định KHÔNG lọc bỏ khách hàng đã Khóa.\n"
     "- 5 loại đối tượng: Cá nhân, Doanh nghiệp tư nhân, Doanh nghiệp nước ngoài, Tổ chức phi chính phủ, Cơ quan nhà nước "
     "(nhãn hiển thị ở cột Loại và ô lọc Loại hình tổ chức).\n"
     "- Khách hàng tổ chức: luôn hiện trong phạm vi quyền của người đăng nhập.\n"
     "- Khách hàng cá nhân: chỉ hiện khi thỏa ít nhất một điều kiện — do chính mình tạo; mình đang "
     "đăng ký còn hạn; đang có người khác đăng ký còn hạn; đã phát sinh báo giá / cuộc họp / dự án "
     "tiềm khách tiềm năng (của bất kỳ ai); hoặc người dùng gõ ĐÚNG TRỌN VẸN số điện thoại vào ô tìm kiếm.\n"
     "- Khách hàng vừa là nhà cung cấp (có tích 'Là nhà cung cấp') vẫn hiển thị bình thường ở màn này."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Khách hàng nằm ngoài phạm vi quyền xem của người đăng nhập (xem mục 7).\n"
     "- Khách hàng cá nhân 'tự do' — chưa ai đăng ký, chưa phát sinh báo giá / cuộc họp / dự án tiềm năng "
     "và không do mình tạo: KHÔNG hiện trong danh sách, chỉ hiện khi gõ đúng trọn vẹn số điện thoại.\n"
     "- Khách hàng đã bị xóa vĩnh viễn khỏi hệ thống (nếu có) không còn xuất hiện; lưu ý thao tác Khóa "
     "KHÔNG xóa dữ liệu, khách hàng đã Khóa vẫn nằm trong danh sách và vẫn xuất ra file.\n"
     "- Người liên hệ của khách hàng tổ chức không phải là một dòng riêng trong danh sách; chỉ xem được "
     "khi mở chi tiết khách hàng đó."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Màn hình KHÔNG có bộ lọc khoảng thời gian. Yếu tố thời gian chỉ xuất hiện ở:\n"
     "- Cột Ngày tạo (hiển thị, sắp xếp được) — dùng để đối chiếu thứ tự bản ghi.\n"
     "- Cột Người sửa (gần nhất) và Người tạo — dùng để truy nguồn.\n"
     "- Màn Lịch sử khách hàng: liệt kê các lần thay đổi theo thứ tự MỚI NHẤT ở trên cùng.\n"
     "Nếu cần lọc theo thời gian, QA ghi nhận là yêu cầu mở rộng, không báo lỗi."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "- Khách hàng tổ chức có thể trỏ tới một khách hàng khác làm Công ty mẹ (cột Công ty mẹ). "
     "Đây là quan hệ 1 cấp, dùng cho chi nhánh / đơn vị trực thuộc.\n"
     "- Khi đã chọn Công ty mẹ thì Mã số thuế trở thành KHÔNG bắt buộc (chi nhánh dùng chung mã số thuế "
     "của công ty mẹ). Không chọn Công ty mẹ thì Mã số thuế BẮT BUỘC.\n"
     "- Mỗi khách hàng tổ chức có nhiều Người đại diện và nhiều Người liên hệ; mỗi Người liên hệ lại có "
     "thể có nhiều số điện thoại và nhiều tài khoản ngân hàng.\n"
     "- Lĩnh vực kinh doanh khai theo CẶP: Loại hình hoạt động — Lĩnh vực kinh doanh. Lĩnh vực phải thuộc "
     "đúng loại hình đã chọn ở vế trái, chọn lệch cặp sẽ bị chặn.\n"
     "- Địa chỉ theo cây: Quốc gia → Tỉnh/Thành phố → Quận/Huyện → Phường/Xã → Thôn/Xóm. Đổi cấp trên thì "
     "cấp dưới bị xóa trắng và nạp lại."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Mỗi khách hàng chỉ hiện MỘT dòng dù có nhiều báo giá, nhiều người liên hệ, nhiều lĩnh vực kinh doanh.\n"
     "- Các cột dạng danh sách (Nhóm KH, Hãng xe) gộp nhiều giá trị vào một ô, ngăn nhau bằng dấu phẩy.\n"
     "- Cột SĐT có thể chứa nhiều số ngăn nhau bằng dấu phẩy; khi tìm theo số điện thoại, hệ thống so khớp "
     "trên từng số chứ không so trên cả chuỗi.\n"
     "- Ô 'Hiển thị a–b / N': a là số thứ tự dòng đầu trang hiện tại, b là dòng cuối trang, N là TỔNG số "
     "khách hàng khớp bộ lọc (không phải tổng toàn hệ thống).\n"
     "- Email, Mã số thuế và Số CMND/CCCD là duy nhất toàn hệ thống — trùng sẽ bị chặn khi lưu."),

    ("7. Phân quyền cấp",
     "Màn hình dùng bộ quyền khách hàng (không phải quyền riêng của phần mềm nhân sự). Các quyền liên quan:\n"
     "- Xem khách hàng — mở màn Quản lý khách hàng (thẻ Báo giá, Hợp đồng, Danh sách trang thiết bị).\n"
     "- Thêm khách hàng — nút Tạo mới và chức năng Import Excel.\n"
     "- Sửa khách hàng — nút Sửa, sửa trang thiết bị, tải ảnh/tài liệu ở thẻ Thông tin khác.\n"
     "- Xóa khách hàng — thao tác Khóa và Mở khóa khách hàng.\n"
     "- Xuất dữ liệu khách hàng — ba nút Xuất CSV, Xuất Excel, Xuất PDF.\n"
     "Bốn cấp quyết định PHẠM VI DỮ LIỆU nhìn thấy, xét theo thứ tự ưu tiên từ trên xuống:\n"
     "- Xem tất cả khách hàng → thấy toàn bộ.\n"
     "- Xem tất cả khách hàng của công ty → thấy khách hàng phát sinh báo giá thuộc công ty mình.\n"
     "- Xem tất cả khách hàng của phòng ban → giới hạn theo phòng ban mình.\n"
     "- Xem tất cả khách hàng của bộ phận → giới hạn theo bộ phận mình.\n"
     "Không có cấp nào ở trên: chỉ thấy khách hàng DO CHÍNH MÌNH TẠO, cộng thêm khách hàng mình đang đăng ký "
     "còn hạn hoặc đã từng tương tác. Lưu ý: bản thân việc MỞ màn danh sách không cần quyền — ai đăng nhập "
     "cũng vào được, chỉ khác nhau ở lượng dữ liệu nhìn thấy."),

    ("8. Cách tính các ô thống kê",
     "- Ô 'Hiển thị a–b / N' ở góc dưới lưới: N là tổng số khách hàng khớp bộ lọc đang áp dụng. Đổi bộ lọc "
     "thì N phải đổi theo; xóa hết bộ lọc thì N quay về tổng số khách hàng trong phạm vi quyền.\n"
     "- Số ghi trên nhãn của nút Bộ lọc nâng cao là SỐ TIÊU CHÍ ĐANG CÓ GIÁ TRỊ, không phải số bản ghi.\n"
     "- Màn Import Excel hiển thị 3 con số sau khi chạy: tổng số dòng đọc được, số dòng thêm thành công, "
     "số dòng lỗi. Ba con số này phải cộng khớp: thành công + lỗi = tổng dòng dữ liệu.\n"
     "- Ở thẻ Danh sách trang thiết bị, số lượng thiết bị là tổng cộng dồn theo từng mã thiết bị, không "
     "đếm theo số dòng chứng từ."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất của màn này, QA đọc trước khi test:\n"
     "- ⚠️ Khóa KHÔNG phải Xóa. Sau khi Khóa, khách hàng VẪN nằm trong danh sách với trạng thái Khóa, vẫn "
     "xuất ra file, chỉ không chọn được ở các màn nghiệp vụ khác.\n"
     "- ⚠️ Mã số thuế bắt buộc hay không PHỤ THUỘC ô Công ty mẹ. Test cả hai chiều.\n"
     "- ⚠️ Khối 'Địa chỉ giao hàng' CHỈ hiện ở màn Sửa, KHÔNG hiện khi Tạo mới — đây là thiết kế, không phải lỗi.\n"
     "- ⚠️ Đổi ô Loại hình tổ chức giữa Cá nhân và nhóm tổ chức sẽ đổi hẳn các khối nhập liệu bên dưới; dữ liệu đã "
     "gõ ở khối cũ không được mang sang khối mới.\n"
     "- ⚠️ Khách hàng cá nhân 'tự do' không hiện trong danh sách; muốn tìm phải gõ ĐÚNG TRỌN VẸN số điện "
     "thoại. Gõ thiếu một chữ số sẽ không ra kết quả — đây là quy tắc, không phải lỗi tìm kiếm.\n"
     "- ⚠️ Cột STT và Mã KH bị khóa luôn hiển thị, không bỏ tích được ở cửa sổ Tuỳ chỉnh cột.\n"
     "- ⚠️ Chức năng 'Cài đặt bộ lọc' chỉ đổi việc HIỆN/ẨN ô lọc trên giao diện, không đổi kết quả lọc. "
     "Ô lọc bị ẩn mà đang có giá trị thì giá trị đó vẫn áp dụng.\n"
     "- ⚠️ Số điện thoại phải bắt đầu bằng số 0 và dài từ 10 đến 12 chữ số; số cố định có mã vùng dạng cũ "
     "sẽ bị báo sai định dạng.\n"
     "- ⚠️ Bốn cột Công ty mẹ / Hãng xe / Người tạo / Người sửa mặc định ẩn vì làm lưới chậm hơn; bật lên "
     "rồi tải trang phải kiểm tra lại tốc độ.\n"
     "- ⚠️ File nhập liệu: dòng 1 là tiêu đề, DỮ LIỆU BẮT ĐẦU TỪ DÒNG 3. Dòng để trống ô Tên khách hàng "
     "được hiểu là thêm người liên hệ cho khách hàng ở dòng ngay trên."),
]

# ----------------------------------------------------------------- TC phan quyen
ROLE_TCS = [
    ("00", "Mở màn hình khi tài khoản không có quyền khách hàng nào", "P0",
     "Tài khoản T0 đăng nhập được, không được gán bất kỳ quyền khách hàng nào. Tài khoản này đã tự tạo 3 khách hàng.",
     "1. Đăng nhập bằng tài khoản T0\n2. Vào menu Giao việc → Danh mục khách hàng",
     "Tài khoản: T0",
     "- Màn hình VẪN mở được, không báo từ chối truy cập\n"
     "- Lưới chỉ hiện đúng 3 khách hàng do chính T0 tạo\n"
     "- Ô 'Hiển thị a–b / N' hiện N = 3\n"
     "- ⚠️ Không hiện các nút Tạo mới, Import Excel, Xuất CSV / Excel / PDF"),

    ("01", "Quyền Xem tất cả khách hàng — thấy toàn bộ dữ liệu", "P0",
     "Hệ thống có 3.451 khách hàng. Tài khoản T1 được gán quyền 'Xem tất cả khách hàng'.",
     "1. Đăng nhập bằng T1\n2. Mở Danh mục khách hàng\n3. Không áp dụng bộ lọc nào\n4. Đọc ô 'Hiển thị a–b / N'",
     "Tài khoản: T1",
     "- N = 3.451, đúng bằng tổng số khách hàng của hệ thống\n"
     "- Thấy được cả khách hàng do người khác tạo và khách hàng đã Khóa"),

    ("02", "Quyền Xem tất cả khách hàng của công ty", "P0",
     "Tài khoản T2 thuộc công ty A, chỉ có quyền 'Xem tất cả khách hàng của công ty'. "
     "Công ty A có 210 khách hàng phát sinh báo giá; công ty B có 180 khách hàng riêng biệt.",
     "1. Đăng nhập bằng T2\n2. Mở Danh mục khách hàng\n3. Đọc tổng số bản ghi\n"
     "4. Tìm tên một khách hàng chỉ thuộc công ty B",
     "Tài khoản: T2 (công ty A)",
     "- Thấy 210 khách hàng của công ty A cộng thêm khách hàng do chính T2 tạo\n"
     "- Khách hàng riêng của công ty B KHÔNG xuất hiện, kể cả khi tìm đúng tên\n"
     "- ⚠️ Không báo lỗi, chỉ đơn giản không có kết quả"),

    ("03", "Quyền Xem tất cả khách hàng của phòng ban", "P0",
     "Tài khoản T3 thuộc phòng ban P1 của công ty A, chỉ có quyền 'Xem tất cả khách hàng của phòng ban'. "
     "Phòng P1 có 64 khách hàng, phòng P2 cùng công ty có 90 khách hàng khác.",
     "1. Đăng nhập bằng T3\n2. Mở Danh mục khách hàng\n3. Đọc tổng số bản ghi",
     "Tài khoản: T3 (phòng P1)",
     "- Chỉ thấy 64 khách hàng của phòng P1 cộng khách hàng do chính T3 tạo\n"
     "- Khách hàng riêng của phòng P2 không xuất hiện"),

    ("04", "Quyền Xem tất cả khách hàng của bộ phận", "P0",
     "Tài khoản T4 thuộc bộ phận BP1, chỉ có quyền 'Xem tất cả khách hàng của bộ phận'. "
     "Bộ phận BP1 có 25 khách hàng.",
     "1. Đăng nhập bằng T4\n2. Mở Danh mục khách hàng\n3. Đọc tổng số bản ghi",
     "Tài khoản: T4 (bộ phận BP1)",
     "- Chỉ thấy 25 khách hàng của bộ phận BP1 cộng khách hàng do chính T4 tạo"),

    ("05", "Thứ tự ưu tiên khi có nhiều cấp quyền xem cùng lúc", "P1",
     "Tài khoản T5 được gán ĐỒNG THỜI 'Xem tất cả khách hàng của công ty' và "
     "'Xem tất cả khách hàng của bộ phận'. Công ty có 210 khách hàng, bộ phận có 25.",
     "1. Đăng nhập bằng T5\n2. Mở Danh mục khách hàng\n3. Đọc tổng số bản ghi",
     "Tài khoản: T5",
     "- Áp dụng cấp RỘNG hơn: thấy 210 khách hàng cấp công ty\n"
     "- ⚠️ Không được lấy giao của hai cấp (không ra 25)"),

    ("06", "Quyền Thêm khách hàng — hiện nút Tạo mới và Import Excel", "P0",
     "Tài khoản T6 có quyền 'Thêm khách hàng', không có quyền Sửa và Xóa khách hàng.",
     "1. Đăng nhập bằng T6\n2. Mở Danh mục khách hàng\n3. Quan sát thanh công cụ\n4. Bấm Tạo mới",
     "Tài khoản: T6",
     "- Nút Tạo mới và Import Excel HIỆN và bấm được\n"
     "- Vào được màn thêm mới, lưu thành công\n"
     "- Nút Sửa trên từng dòng bị mờ / không bấm được"),

    ("07", "Không có quyền Thêm khách hàng", "P0",
     "Tài khoản T7 chỉ có quyền 'Xem tất cả khách hàng'.",
     "1. Đăng nhập bằng T7\n2. Mở Danh mục khách hàng\n3. Quan sát thanh công cụ",
     "Tài khoản: T7",
     "- Không hiện nút Tạo mới và Import Excel\n"
     "- Vẫn xem được danh sách bình thường"),

    ("08", "Quyền Sửa khách hàng", "P0",
     "Tài khoản T8 có quyền 'Sửa khách hàng', không có 'Thêm khách hàng'. "
     "Khách hàng KH-A đang ở trạng thái Hoạt động.",
     "1. Đăng nhập bằng T8\n2. Mở Danh mục khách hàng\n3. Bấm biểu tượng bút chì ở dòng KH-A\n"
     "4. Sửa ô Tên viết tắt và bấm Lưu",
     "Tài khoản: T8 · Tên viết tắt mới: KHA-2026",
     "- Vào được màn sửa, lưu thành công, thông báo lưu thành công\n"
     "- Không hiện nút Tạo mới"),

    ("09", "Không có quyền Sửa khách hàng", "P0",
     "Tài khoản T9 chỉ có quyền 'Xem tất cả khách hàng'.",
     "1. Đăng nhập bằng T9\n2. Mở Danh mục khách hàng\n3. Quan sát cột Hành động",
     "Tài khoản: T9",
     "- Biểu tượng Sửa bị vô hiệu hóa (mờ), rê chuột vào hiện chú thích không có quyền\n"
     "- ⚠️ Nút bị vô hiệu hóa chứ KHÔNG bị ẩn đi"),

    ("10", "Quyền Xóa khách hàng — dùng cho Khóa và Mở khóa", "P0",
     "Tài khoản T10 có quyền 'Xóa khách hàng'. Khách hàng KH-B đang Hoạt động, KH-C đang Khóa.",
     "1. Đăng nhập bằng T10\n2. Mở Danh mục khách hàng\n"
     "3. Bấm biểu tượng ổ khóa ở dòng KH-B, xác nhận\n4. Bấm biểu tượng ổ khóa ở dòng KH-C, xác nhận",
     "Tài khoản: T10",
     "- Cả hai thao tác thành công, cột Trạng thái đổi tương ứng\n"
     "- ⚠️ Không có quyền riêng tên là 'Khóa khách hàng'; hai thao tác này dùng chung quyền Xóa khách hàng"),

    ("11", "Không có quyền Xóa khách hàng", "P0",
     "Tài khoản T11 có quyền Xem và Sửa khách hàng, KHÔNG có quyền Xóa khách hàng.",
     "1. Đăng nhập bằng T11\n2. Mở Danh mục khách hàng\n3. Mở menu ba chấm ở một dòng",
     "Tài khoản: T11",
     "- Thao tác Khóa / Mở khóa bị vô hiệu hóa\n"
     "- Thao tác Sửa vẫn dùng được bình thường"),

    ("12", "Quyền Xuất dữ liệu khách hàng", "P0",
     "Tài khoản T12 có quyền 'Xuất dữ liệu khách hàng'. Bộ lọc đang cho ra 120 khách hàng.",
     "1. Đăng nhập bằng T12\n2. Mở Danh mục khách hàng\n3. Bấm lần lượt Xuất CSV, Xuất Excel, Xuất PDF",
     "Tài khoản: T12",
     "- Cả ba nút bấm được và tải về file tương ứng\n"
     "- Nội dung file đúng 120 khách hàng đang lọc"),

    ("13", "Không có quyền Xuất dữ liệu khách hàng", "P0",
     "Tài khoản T13 có quyền 'Xem tất cả khách hàng', không có quyền xuất dữ liệu.",
     "1. Đăng nhập bằng T13\n2. Mở Danh mục khách hàng\n3. Quan sát nhóm nút xuất file",
     "Tài khoản: T13",
     "- Ba nút Xuất CSV / Xuất Excel / Xuất PDF bị vô hiệu hóa hoặc không hiện"),

    ("14", "Quyền Xem khách hàng — mở màn Quản lý khách hàng", "P0",
     "Tài khoản T14 có quyền 'Xem khách hàng'. Khách hàng KH-D có 2 báo giá và 1 hợp đồng.",
     "1. Đăng nhập bằng T14\n2. Mở Danh mục khách hàng\n"
     "3. Mở menu ba chấm ở dòng KH-D → chọn Quản lý\n4. Bấm lần lượt các thẻ Báo giá, Hợp đồng, Danh sách trang thiết bị",
     "Tài khoản: T14",
     "- Mở được màn Quản lý khách hàng\n"
     "- Thẻ Báo giá hiện 2 dòng, thẻ Hợp đồng hiện 1 dòng"),

    ("15", "Không có quyền Xem khách hàng — chặn các thẻ nghiệp vụ", "P1",
     "Tài khoản T15 không có quyền 'Xem khách hàng'.",
     "1. Đăng nhập bằng T15\n2. Mở màn Quản lý khách hàng của một khách hàng bất kỳ\n"
     "3. Bấm thẻ Báo giá",
     "Tài khoản: T15",
     "- Hệ thống từ chối, báo không có quyền, không hiện dữ liệu báo giá\n"
     "- Trang không bị treo hoặc trắng màn"),

    ("16", "Chặn thêm khách hàng khi bỏ qua giao diện", "P0",
     "Tài khoản T16 KHÔNG có quyền 'Thêm khách hàng'. Tester dùng công cụ kiểm thử để gọi thẳng chức năng.",
     "1. Đăng nhập bằng T16, lấy phiên đăng nhập\n"
     "2. Dùng công cụ kiểm thử gọi thẳng chức năng Thêm khách hàng, bỏ qua giao diện\n"
     "3. Kiểm tra lại danh sách khách hàng",
     "Tài khoản: T16 · Dữ liệu gửi: một khách hàng cá nhân hợp lệ",
     "- Hệ thống từ chối, báo không có quyền\n"
     "- ⚠️ Không có khách hàng mới nào được tạo ra\n"
     "- (Nhóm test này dành cho tester kỹ thuật, xem ghi chú mục 9)"),

    ("17", "Chặn sửa khách hàng khi bỏ qua giao diện", "P0",
     "Tài khoản T17 KHÔNG có quyền 'Sửa khách hàng'. Khách hàng KH-E có tên 'Công ty ABC'.",
     "1. Đăng nhập bằng T17\n2. Dùng công cụ kiểm thử gọi thẳng chức năng Sửa cho KH-E, đổi tên thành 'XYZ'\n"
     "3. Mở lại chi tiết KH-E",
     "Tài khoản: T17 · Tên mới: XYZ",
     "- Hệ thống từ chối, báo không có quyền\n"
     "- Tên khách hàng vẫn là 'Công ty ABC'"),

    ("18", "Chặn khóa/mở khóa khi bỏ qua giao diện", "P0",
     "Tài khoản T18 KHÔNG có quyền 'Xóa khách hàng'. Khách hàng KH-F đang Hoạt động.",
     "1. Đăng nhập bằng T18\n2. Dùng công cụ kiểm thử gọi thẳng thao tác Khóa cho KH-F\n"
     "3. Kiểm tra trạng thái KH-F",
     "Tài khoản: T18",
     "- Hệ thống từ chối, báo không có quyền\n"
     "- KH-F vẫn ở trạng thái Hoạt động"),

    ("19", "Chặn xuất dữ liệu khi bỏ qua giao diện", "P1",
     "Tài khoản T19 KHÔNG có quyền 'Xuất dữ liệu khách hàng'.",
     "1. Đăng nhập bằng T19\n2. Dùng công cụ kiểm thử gọi thẳng chức năng Xuất Excel danh sách khách hàng",
     "Tài khoản: T19",
     "- Hệ thống từ chối, báo không có quyền\n"
     "- Không có file nào được sinh ra"),

    ("20", "Chặn nhập dữ liệu từ Excel khi bỏ qua giao diện", "P1",
     "Tài khoản T20 KHÔNG có quyền 'Thêm khách hàng'.",
     "1. Đăng nhập bằng T20\n2. Dùng công cụ kiểm thử gọi thẳng chức năng Import khách hàng kèm một file hợp lệ 5 dòng\n"
     "3. Kiểm tra danh sách",
     "Tài khoản: T20 · File: 5 dòng khách hàng hợp lệ",
     "- Hệ thống từ chối, báo không có quyền\n"
     "- ⚠️ Không có dòng nào trong 5 dòng được thêm vào hệ thống"),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "TÌM KIẾM & BỘ LỌC NÂNG CAO", SEC_II),
    ("III", "CÀI ĐẶT BỘ LỌC & TUỲ CHỈNH CỘT", SEC_III),
    ("IV", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", SEC_IV),
    ("V", "TẠO MỚI / SỬA / XEM CHI TIẾT KHÁCH HÀNG", SEC_V),
    ("VI", "KHÓA / MỞ KHÓA KHÁCH HÀNG", SEC_VI),
    ("VII", "MÀN QUẢN LÝ KHÁCH HÀNG & LỊCH SỬ THAY ĐỔI", SEC_VII),
    ("VIII", "NHẬP DỮ LIỆU TỪ FILE EXCEL", SEC_VIII),
    ("IX", "XUẤT FILE CSV / EXCEL / PDF", SEC_IX),
    ("X", "CÔ LẬP DỮ LIỆU, THAO TÁC ĐỒNG THỜI & LUỒNG TỔNG HỢP", SEC_X),
]

build(
    output_file=os.path.join(HERE, "testcase.xlsx"),
    sheet_name="Trang tính1",
    feature_name="Danh mục khách hàng - Cập nhật ngày 15/08/2026",
    module_name=MODULE,
    description_block=DESCRIPTION_BLOCK,
    role_tcs=ROLE_TCS,
    sections=SECTIONS,
)
