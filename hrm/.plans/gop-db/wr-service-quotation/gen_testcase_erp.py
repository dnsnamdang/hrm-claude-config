# -*- coding: utf-8 -*-
"""Sinh file testcase cho man ERP: Phieu cung cap thong tin lam bao gia."""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", ".claude", "skills",
                                "testcase-documenter", "assets"))
from tc_engine import build  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Phiếu cung cấp thông tin làm báo giá là chứng từ thứ 3 của luồng dịch vụ sửa chữa - bảo hành: "
     "Yêu cầu kiểm tra sửa chữa - bảo hành → Phiếu xử lý yêu cầu → Phiếu cung cấp thông tin làm báo giá "
     "→ Báo giá dịch vụ.\n"
     "Người của bộ phận kỹ thuật căn cứ Phiếu xử lý yêu cầu để liệt kê: thiết bị được bảo hành, "
     "dịch vụ kiểm tra - sửa chữa, thiết bị cần bảo dưỡng, vật tư đi kèm và các khoản chi phí liên quan; "
     "sau đó gửi sang cho người đã lập Phiếu yêu cầu để họ làm Báo giá dịch vụ gửi khách hàng.\n"
     "Màn hình gồm: danh sách phiếu, lập phiếu (từ Phiếu xử lý yêu cầu), sửa, xem chi tiết, xóa, "
     "Không duyệt (từ chối tiếp nhận), In phiếu, In danh sách và Xuất Excel danh sách."),

    ("2. Đối tượng được tính / hiển thị",
     "Màn hình có 2 lối vào từ menu, dùng chung một danh sách nhưng lọc khác nhau:\n"
     "• Menu CSKH → Kiểm tra bảo hành sửa chữa → Phiếu cung cấp thông tin làm báo giá: danh sách ĐẦY ĐỦ. "
     "Hiển thị phiếu theo phạm vi quyền xem (tổng công ty / công ty / phòng ban), cộng thêm mọi phiếu do "
     "chính người đang đăng nhập lập.\n"
     "• Menu Bán hàng → Báo giá dịch vụ sửa chữa - bảo dưỡng - bảo trì → Phiếu cung cấp thông tin làm báo giá: "
     "danh sách CHỜ LÀM BÁO GIÁ. Chỉ hiện phiếu thỏa ĐỒNG THỜI 3 điều kiện: trạng thái Chờ làm báo giá; "
     "thuộc Phiếu yêu cầu do chính người đang đăng nhập lập; phiếu có ít nhất một dòng dịch vụ sửa chữa "
     "hoặc một thiết bị cần bảo dưỡng.\n"
     "Các trạng thái phiếu có thể gặp: Đang tạo, Chờ làm báo giá, Chờ xử lý, Đang báo giá, Báo giá đã duyệt, "
     "Đã lập hợp đồng, Đã hoàn thành, Kết thúc, Không duyệt.\n"
     "Cột Trạng thái bảo hành chỉ có giá trị khi phiếu có thiết bị được bảo hành: Chờ tạo phiếu bảo hành / "
     "Đã tạo phiếu bảo hành."),

    ("3. Đối tượng bị ẩn / không tính",
     "• Phiếu ở trạng thái Đang tạo (nháp) của NGƯỜI KHÁC không hiện ở danh sách đầy đủ, dù người xem có "
     "quyền xem theo tổng công ty. Phiếu nháp chỉ người lập ra nó nhìn thấy.\n"
     "• Danh sách Chờ làm báo giá loại bỏ: phiếu khác trạng thái Chờ làm báo giá; phiếu của Phiếu yêu cầu do "
     "người khác lập; phiếu chỉ có bảo hành mà không có dòng sửa chữa và không có thiết bị bảo dưỡng.\n"
     "• Người không có bất kỳ quyền xem nào vẫn vào được màn danh sách nhưng chỉ thấy phiếu do chính mình lập.\n"
     "• Màn hình này không có nút Tạo mới. Phiếu chỉ sinh ra từ Phiếu xử lý yêu cầu đang ở trạng thái "
     "Chờ cung cấp thông tin, do người có quyền Tạo phiếu cung cấp thông tin thực hiện."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Ô chọn khoảng thời gian lọc theo NGÀY LẬP PHIẾU (cột Ngày lập phiếu trên lưới), không phải ngày nhận "
     "yêu cầu và không phải ngày gửi đi.\n"
     "Từ ngày lấy trọn ngày được chọn; Đến ngày lấy hết ngày được chọn (bao gồm cả phiếu lập lúc cuối ngày). "
     "Để trống một trong hai đầu thì chỉ chặn ở đầu còn lại."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Form phiếu gồm các khối theo đúng thứ tự:\n"
     "• Thông tin khách hàng — lấy từ Phiếu xử lý yêu cầu, chỉ ô Ghi chú cho nhập.\n"
     "• A - BẢO HÀNH THIẾT BỊ — các thiết bị được xử lý theo diện bảo hành.\n"
     "• B - DỊCH VỤ KIỂM TRA, SỬA CHỮA, BẢO DƯỠNG, gồm: I - Dịch vụ kiểm tra, sửa chữa (dòng thiết bị từ "
     "Phiếu xử lý) và II - Danh mục thiết bị cần bảo dưỡng (người lập tự thêm từ danh mục thiết bị của khách).\n"
     "• C - CHI PHÍ KHÁC, gồm: I. Các khoản chi phí liên quan và II. Chi phí vận chuyển thiết bị, vật tư.\n"
     "• D - TỔNG HỢP BÁO GIÁ, gồm: I. Bảo hành, II. Sửa chữa - Bảo dưỡng, III. Tổng hợp báo giá.\n"
     "• Điều khoản báo giá và Ghi chú duyệt.\n"
     "Mỗi dòng thiết bị ở khối A và B-I có 3 cấp con: dòng Công (công kiểm tra sửa chữa), Danh sách dịch vụ "
     "và Danh sách vật tư. Mỗi thiết bị ở khối B-II có các gói dịch vụ bảo dưỡng, mỗi gói lại có danh sách vật tư."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "• Ô Loại công việc của mỗi thiết bị chỉ có 2 giá trị: Sửa chữa và Bảo hành. Đổi giá trị này sẽ CHUYỂN "
     "NGUYÊN dòng thiết bị (kèm dịch vụ và vật tư của nó) giữa khối A và khối B-I, không nhân đôi dòng.\n"
     "• Chuyển một thiết bị từ Sửa chữa sang Bảo hành: hệ thống tự đặt Chi phí được bảo hành của dòng công, "
     "của từng dịch vụ và từng vật tư bằng đúng Thành tiền của chúng (khách không phải trả).\n"
     "• Chuyển ngược từ Bảo hành sang Sửa chữa: hệ thống đặt lại toàn bộ cột Cho bảo hành và Miễn phí ở khối "
     "C - Chi phí khác về 0.\n"
     "• Khối B-II: mỗi thiết bị chỉ được thêm tối đa bằng số lượng khách đang có; thêm quá thì bị chặn. "
     "Hai dòng cùng thiết bị mà trùng serial thì không lưu được.\n"
     "• Nút Thêm mới ở khối B-II lấy thiết bị từ danh mục thiết bị của chính khách hàng trên phiếu, "
     "không phải toàn bộ danh mục hàng hóa."),

    ("7. Phân quyền cấp",
     "Các quyền liên quan tới màn hình này:\n"
     "• Tạo phiếu cung cấp thông tin — được lập phiếu từ Phiếu xử lý yêu cầu; cũng là điều kiện để thấy thao "
     "tác Tạo phiếu cung cấp thông tin trên màn Phiếu xử lý yêu cầu.\n"
     "• Xem phiếu cung cấp thông tin theo tổng công ty — xem mọi phiếu của toàn hệ thống.\n"
     "• Xem phiếu cung cấp thông tin theo công ty — xem phiếu của công ty mình, cộng phiếu do mình lập.\n"
     "• Xem phiếu cung cấp thông tin theo phòng ban — xem phiếu của các phòng ban mình quản lý, cộng phiếu do "
     "mình lập.\n"
     "Ngoài quyền, còn 2 ràng buộc theo vai trò trên chính chứng từ: chỉ NGƯỜI LẬP PHIẾU mới được Sửa và Xóa "
     "(và chỉ khi phiếu đang ở Đang tạo hoặc Không duyệt); chỉ NGƯỜI LẬP PHIẾU YÊU CẦU mới được Tạo báo giá "
     "dịch vụ và Không duyệt."),

    ("8. Cách tính các ô thống kê",
     "Trên từng dòng chi tiết:\n"
     "• Thành tiền = Số lượng × Đơn giá bán.\n"
     "• Ở khối A: Khách hàng phải trả = Thành tiền − Chi phí được bảo hành (không cho âm; nhập số âm bị đưa về 0).\n"
     "• Ở khối B: Thành tiền sau chiết khấu = Thành tiền − Chiết khấu.\n"
     "Khối C - Chi phí khác: Khách hàng phải trả = Giá trị − (Cho bảo hành + Miễn phí). Cột Chi phí cho SC - BD "
     "là phần chi phí phân bổ cho nhánh sửa chữa - bảo dưỡng. Ba cột Cho bảo hành / Miễn phí / Trả phí chỉ hiện "
     "khi phiếu có ít nhất một thiết bị ở khối A.\n"
     "Khối D - I. Bảo hành: dòng 1 Tổng chi phí bảo hành = 1.1 Công kiểm tra sửa chữa + 1.2 Chi phí dịch vụ + "
     "1.3 Chi phí vật tư; cộng thêm dòng 2 Các khoản chi phí liên quan và dòng 3 Chi phí vận chuyển.\n"
     "Khối D - III. Tổng hợp báo giá: dòng Tổng cộng của mỗi cột = dòng Bảo hành + dòng Sửa chữa bảo dưỡng, "
     "tính riêng cho từng cột Thành tiền, Giảm giá, Phải thanh toán."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất của màn hình này:\n"
     "• Toàn bộ số tiền được tính ngay trên trình duyệt khi gõ. Sửa một ô Số lượng hay Đơn giá bán phải thấy "
     "khối D đổi theo NGAY, không cần bấm Lưu. Nếu phải tải lại trang mới đúng số thì đó là lỗi.\n"
     "• Cột Giá vốn chỉ có ở màn Lập phiếu và Sửa phiếu, KHÔNG có ở màn Xem chi tiết — số cột của cùng một "
     "bảng ở 2 màn lệch nhau 1 là đúng thiết kế.\n"
     "• Thiết bị mang NHIỀU lỗi: khi lập phiếu, hệ thống tách thành nhiều dòng theo từng lỗi, nhưng các dòng "
     "tách ra bị mất phần Danh sách dịch vụ. Ngoài ra phiếu có thiết bị nhiều hơn một lỗi sẽ KHÔNG hiện thao "
     "tác Tạo báo giá dịch vụ. Đây là điểm phải soi kỹ khi test.\n"
     "• Ô Ghi chú duyệt và nút Không duyệt chỉ hiện với đúng người đã lập Phiếu yêu cầu, và chỉ khi phiếu đủ "
     "điều kiện làm báo giá. Người khác mở cùng phiếu sẽ không thấy — không phải lỗi hiển thị.\n"
     "• Nút Lưu lưu phiếu ở trạng thái Đang tạo (còn sửa được); nút Lưu & Gửi duyệt đẩy phiếu sang Chờ làm "
     "báo giá và KHÔNG sửa lại được nữa. Cả hai nút đều bắt buộc nhập đủ trường, không có chế độ lưu nháp dễ dãi.\n"
     "• Số tiền hiển thị có dấu phân cách hàng nghìn, khi gõ vào ô nhập vẫn gõ số trơn."),
]

ROLE_TCS = [
    ("00",
     "Người có quyền Tạo phiếu cung cấp thông tin lập được phiếu",
     "P0",
     "Tài khoản A có quyền Tạo phiếu cung cấp thông tin. Có Phiếu xử lý yêu cầu số PXL-001 ở trạng thái "
     "Chờ cung cấp thông tin.",
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Vào menu CSKH → Kiểm tra bảo hành sửa chữa → Phiếu xử lý yêu cầu\n"
     "3. Mở menu bánh răng ở dòng PXL-001\n"
     "4. Bấm Tạo phiếu cung cấp thông tin",
     "—",
     "- Menu dòng PXL-001 có mục Tạo phiếu cung cấp thông tin\n"
     "- Bấm vào mở màn Tạo phiếu cung cấp thông tin làm báo giá\n"
     "- Khối Thông tin khách hàng đã điền sẵn Số phiếu xử lý, Người yêu cầu, Phòng yêu cầu, Ngày nhận phiếu "
     "xử lý, Khách hàng, Người liên hệ, Số điện thoại liên hệ, Địa chỉ sửa chữa"),

    ("01",
     "Người KHÔNG có quyền Tạo phiếu cung cấp thông tin không lập được",
     "P0",
     "Tài khoản B không có quyền Tạo phiếu cung cấp thông tin. Phiếu xử lý PXL-002 ở trạng thái "
     "Chờ cung cấp thông tin.",
     "1. Đăng nhập bằng tài khoản B\n"
     "2. Mở danh sách Phiếu xử lý yêu cầu\n"
     "3. Mở menu bánh răng ở dòng PXL-002\n"
     "4. Mở tiếp màn Xem chi tiết PXL-002 và soi dãy nút cuối trang",
     "—",
     "- Menu dòng PXL-002 KHÔNG có mục Tạo phiếu cung cấp thông tin\n"
     "- Màn chi tiết PXL-002 cũng không có nút Tạo phiếu cung cấp thông tin\n"
     "- ⚠️ Nút phải ẩn hẳn, không được hiện dạng chữ xám bấm không ăn"),

    ("02",
     "Chặn lập phiếu khi gọi thẳng chức năng, bỏ qua giao diện",
     "P0",
     "Tài khoản B không có quyền Tạo phiếu cung cấp thông tin. Biết số hiệu Phiếu xử lý PXL-002.",
     "1. Đăng nhập bằng tài khoản B\n"
     "2. Dùng công cụ kiểm thử để gọi thẳng chức năng Lưu phiếu cung cấp thông tin cho PXL-002, "
     "bỏ qua giao diện\n"
     "3. Mở lại danh sách phiếu cung cấp thông tin",
     "—",
     "- Hệ thống từ chối, trả về thông báo không có quyền\n"
     "- Không có phiếu mới nào được tạo\n"
     "- Trạng thái PXL-002 giữ nguyên Chờ cung cấp thông tin"),

    ("03",
     "Quyền Xem phiếu cung cấp thông tin theo tổng công ty",
     "P0",
     "Tài khoản C chỉ có quyền Xem phiếu cung cấp thông tin theo tổng công ty. Trong hệ thống có phiếu của "
     "3 công ty khác nhau, trong đó công ty 1 có 4 phiếu đã gửi và 1 phiếu Đang tạo của người khác.",
     "1. Đăng nhập bằng tài khoản C\n"
     "2. Vào menu CSKH → Phiếu cung cấp thông tin làm báo giá\n"
     "3. Đếm số dòng và đối chiếu cột Trạng thái",
     "—",
     "- Thấy phiếu của cả 3 công ty\n"
     "- ⚠️ KHÔNG thấy phiếu Đang tạo của người khác, dù có quyền cao nhất"),

    ("04",
     "Quyền Xem phiếu cung cấp thông tin theo công ty",
     "P0",
     "Tài khoản D chỉ có quyền Xem phiếu cung cấp thông tin theo công ty, thuộc công ty 1. Công ty 1 có 4 phiếu "
     "đã gửi; công ty 2 có 3 phiếu; bản thân D có 1 phiếu Đang tạo.",
     "1. Đăng nhập bằng tài khoản D\n"
     "2. Vào menu CSKH → Phiếu cung cấp thông tin làm báo giá\n"
     "3. Đối chiếu danh sách với dữ liệu chuẩn bị",
     "—",
     "- Thấy đúng 4 phiếu của công ty 1 và 1 phiếu Đang tạo do chính D lập, tổng 5 dòng\n"
     "- Không thấy phiếu nào của công ty 2"),

    ("05",
     "Quyền Xem phiếu cung cấp thông tin theo phòng ban",
     "P1",
     "Tài khoản E chỉ có quyền Xem phiếu cung cấp thông tin theo phòng ban và đang quản lý phòng Kỹ thuật 1. "
     "Phòng Kỹ thuật 1 có 3 phiếu; phòng Kỹ thuật 2 có 2 phiếu; E tự lập 1 phiếu Đang tạo.",
     "1. Đăng nhập bằng tài khoản E\n"
     "2. Vào menu CSKH → Phiếu cung cấp thông tin làm báo giá",
     "—",
     "- Thấy 3 phiếu của phòng Kỹ thuật 1 và 1 phiếu do chính E lập, tổng 4 dòng\n"
     "- Không thấy phiếu của phòng Kỹ thuật 2"),

    ("06",
     "Không có quyền xem nào thì chỉ thấy phiếu của mình",
     "P0",
     "Tài khoản F không có bất kỳ quyền Xem phiếu cung cấp thông tin nào, đã tự lập 2 phiếu.",
     "1. Đăng nhập bằng tài khoản F\n"
     "2. Vào menu CSKH → Phiếu cung cấp thông tin làm báo giá",
     "—",
     "- Danh sách chỉ có đúng 2 phiếu do F lập\n"
     "- Không có dòng nào của người khác"),

    ("07",
     "Mở trực tiếp phiếu ngoài phạm vi quyền",
     "P0",
     "Tài khoản D chỉ có quyền xem theo công ty, thuộc công ty 1. Phiếu PCCTT-900 thuộc công ty 2, "
     "trạng thái Chờ làm báo giá.",
     "1. Đăng nhập bằng tài khoản D\n"
     "2. Mở thẳng đường dẫn xem chi tiết của PCCTT-900",
     "—",
     "- Hệ thống hiện trang báo không tìm thấy dữ liệu\n"
     "- Không hiển thị bất kỳ nội dung nào của phiếu"),

    ("08",
     "Mở trực tiếp phiếu Đang tạo của người khác",
     "P0",
     "Phiếu PCCTT-901 do tài khoản A lập, đang ở trạng thái Đang tạo. Tài khoản C có quyền xem theo tổng công ty.",
     "1. Đăng nhập bằng tài khoản C\n"
     "2. Mở thẳng đường dẫn xem chi tiết của PCCTT-901",
     "—",
     "- Hệ thống hiện trang báo không tìm thấy dữ liệu\n"
     "- ⚠️ Quyền xem theo tổng công ty KHÔNG mở được phiếu nháp của người khác"),
]

SEC_I = [
    ("001", "Vào màn hình từ menu CSKH", "P0",
     "Tài khoản C có quyền xem theo tổng công ty.",
     "1. Đăng nhập\n2. Vào menu CSKH → Kiểm tra bảo hành sửa chữa\n"
     "3. Bấm Phiếu cung cấp thông tin làm báo giá",
     "—",
     "- Mở màn danh sách, tiêu đề trang là Danh sách phiếu cung cấp thông tin\n"
     "- Lưới hiển thị dữ liệu, không có dòng báo lỗi"),

    ("002", "Vào màn hình từ menu Bán hàng", "P0",
     "Tài khoản A đã lập 2 Phiếu yêu cầu, trong đó 1 phiếu đã có Phiếu cung cấp thông tin ở trạng thái "
     "Chờ làm báo giá và có dòng dịch vụ sửa chữa.",
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Vào menu Bán hàng → Báo giá dịch vụ sửa chữa - bảo dưỡng - bảo trì\n"
     "3. Bấm Phiếu cung cấp thông tin làm báo giá",
     "—",
     "- Tiêu đề trang là Danh sách phiếu cung cấp thông tin làm báo giá\n"
     "- Chỉ hiện đúng 1 phiếu Chờ làm báo giá nói trên"),

    ("003", "Đủ 11 cột trên lưới danh sách", "P0",
     "Danh sách có ít nhất 1 phiếu.",
     "1. Mở danh sách đầy đủ từ menu CSKH\n2. Đọc hàng tiêu đề của lưới từ trái sang phải",
     "—",
     "- Các cột lần lượt: STT, Số phiếu cung cấp thông tin, Số phiếu xử lí, Khách hàng, Người yêu cầu, "
     "Ngày nhận yêu cầu, Người lập phiếu, Ngày lập phiếu, Trạng thái, Trạng thái bảo hành, Hành động"),

    ("004", "Nội dung cột Khách hàng và Người yêu cầu", "P1",
     "Phiếu PCCTT-100 của khách hàng mã KH-0007 tên CÔNG TY TNHH ABC; Phiếu yêu cầu gốc do Nguyễn Văn A, "
     "số điện thoại 0900000001 lập.",
     "1. Mở danh sách đầy đủ\n2. Tìm dòng PCCTT-100\n3. Đọc cột Khách hàng và cột Người yêu cầu",
     "—",
     "- Cột Khách hàng hiện KH-0007 - CÔNG TY TNHH ABC\n"
     "- Cột Người yêu cầu hiện Nguyễn Văn A - 0900000001"),

    ("005", "Cột Số phiếu và Số phiếu xử lí là liên kết mở được", "P1",
     "Phiếu PCCTT-100 gắn với Phiếu xử lý PXL-055.",
     "1. Mở danh sách đầy đủ\n2. Bấm vào số phiếu ở cột Số phiếu cung cấp thông tin\n"
     "3. Quay lại danh sách, bấm vào số phiếu ở cột Số phiếu xử lí",
     "—",
     "- Bấm cột đầu mở màn xem chi tiết đúng phiếu PCCTT-100\n"
     "- Bấm cột thứ hai mở màn xem chi tiết Phiếu xử lý PXL-055"),

    ("006", "Cột Trạng thái bảo hành để trống khi phiếu không có bảo hành", "P1",
     "Phiếu PCCTT-101 chỉ có dịch vụ sửa chữa, không có thiết bị nào ở khối A - Bảo hành thiết bị.",
     "1. Mở danh sách đầy đủ\n2. Tìm dòng PCCTT-101\n3. Đọc cột Trạng thái bảo hành",
     "—",
     "- Ô Trạng thái bảo hành để trống, không hiện nhãn màu nào"),

    ("007", "Menu hành động của phiếu Đang tạo do chính mình lập", "P0",
     "Tài khoản A đang có phiếu PCCTT-102 ở trạng thái Đang tạo.",
     "1. Đăng nhập bằng tài khoản A\n2. Mở danh sách đầy đủ\n3. Bấm biểu tượng bánh răng ở dòng PCCTT-102",
     "—",
     "- Menu có: Sửa, Xóa, In\n"
     "- Không có Tạo báo giá dịch vụ, không có Từ chối tiếp nhận"),

    ("008", "Menu hành động của phiếu Chờ làm báo giá, người xem là người lập Phiếu yêu cầu", "P0",
     "Phiếu PCCTT-103 ở trạng thái Chờ làm báo giá, có 1 dòng dịch vụ sửa chữa, mỗi thiết bị chỉ 1 lỗi. "
     "Phiếu yêu cầu gốc do tài khoản A lập.",
     "1. Đăng nhập bằng tài khoản A\n2. Mở danh sách Chờ làm báo giá từ menu Bán hàng\n"
     "3. Bấm bánh răng ở dòng PCCTT-103",
     "—",
     "- Menu có: Tạo báo giá dịch vụ, Từ chối tiếp nhận, In\n"
     "- Không có Sửa và Xóa vì A không phải người lập phiếu này"),
]

SEC_II = [
    ("001", "Lọc theo Mã phiếu cung cấp thông tin", "P0",
     "Danh sách có các phiếu PCCTT-100, PCCTT-101, PCCTT-200.",
     "1. Mở danh sách đầy đủ\n2. Gõ 10 vào ô Mã phiếu cung cấp thông tin\n3. Chờ lưới tải lại",
     "Mã phiếu cung cấp thông tin: 10",
     "- Lưới còn PCCTT-100 và PCCTT-101\n- Không còn PCCTT-200\n"
     "- Ô lọc tìm theo một đoạn bất kỳ của mã, không cần gõ đủ"),

    ("002", "Lọc theo Mã phiếu xử lí", "P0",
     "PCCTT-100 gắn PXL-055; PCCTT-101 gắn PXL-056.",
     "1. Mở danh sách đầy đủ\n2. Gõ 055 vào ô Mã phiếu xử lí",
     "Mã phiếu xử lí: 055",
     "- Lưới chỉ còn dòng PCCTT-100"),

    ("003", "Lọc theo Khách hàng", "P0",
     "Có 2 phiếu của khách KH-0007 và 3 phiếu của khách KH-0008.",
     "1. Mở danh sách đầy đủ\n2. Bấm ô Khách hàng\n3. Gõ 0007 rồi chọn khách trong danh sách gợi ý",
     "Khách hàng: KH-0007",
     "- Ô lọc gợi ý danh sách khách hàng khi gõ\n- Lưới còn đúng 2 phiếu của KH-0007"),

    ("004", "Lọc theo Trạng thái", "P0",
     "Danh sách có phiếu ở các trạng thái Chờ làm báo giá, Đang báo giá và Không duyệt.",
     "1. Mở danh sách đầy đủ\n2. Chọn Chờ làm báo giá ở ô Trạng thái",
     "Trạng thái: Chờ làm báo giá",
     "- Chỉ còn các dòng có cột Trạng thái là Chờ làm báo giá\n"
     "- Ô Trạng thái liệt kê đủ 9 lựa chọn: Đang tạo, Chờ làm báo giá, Chờ xử lý, Đang báo giá, "
     "Báo giá đã duyệt, Đã lập hợp đồng, Đã hoàn thành, Kết thúc, Không duyệt"),

    ("005", "Lọc theo Người yêu cầu", "P1",
     "Nguyễn Văn A lập 3 Phiếu yêu cầu đã có phiếu cung cấp thông tin; Trần Thị B lập 2.",
     "1. Mở danh sách đầy đủ\n2. Bấm ô Người yêu cầu, gõ tên và chọn Nguyễn Văn A",
     "Người yêu cầu: Nguyễn Văn A",
     "- Lưới còn 3 dòng, cột Người yêu cầu đều là Nguyễn Văn A"),

    ("006", "Lọc theo Người lập", "P1",
     "Tài khoản A lập 4 phiếu, tài khoản D lập 2 phiếu.",
     "1. Mở danh sách đầy đủ\n2. Bấm ô Người lập, chọn tài khoản D",
     "Người lập: tài khoản D",
     "- Lưới còn 2 dòng, cột Người lập phiếu đều là tài khoản D"),

    ("007", "Lọc theo khoảng thời gian lập phiếu", "P0",
     "Có phiếu lập ngày 01/08/2026, 15/08/2026 và 25/08/2026.",
     "1. Mở danh sách đầy đủ\n2. Chọn khoảng thời gian từ 10/08/2026 đến 20/08/2026",
     "Từ ngày: 10/08/2026 · Đến ngày: 20/08/2026",
     "- Chỉ còn phiếu lập ngày 15/08/2026\n"
     "- Cột Ngày lập phiếu của mọi dòng nằm trong khoảng đã chọn"),

    ("008", "Đến ngày lấy trọn cả ngày cuối", "P0",
     "Có phiếu lập lúc 23:30 ngày 20/08/2026.",
     "1. Mở danh sách đầy đủ\n2. Chọn khoảng thời gian từ 20/08/2026 đến 20/08/2026",
     "Từ ngày: 20/08/2026 · Đến ngày: 20/08/2026",
     "- ⚠️ Phiếu lập lúc 23:30 vẫn phải xuất hiện, không bị cắt mất"),

    ("009", "Lọc theo Công ty ở danh sách đầy đủ", "P1",
     "Tài khoản C có quyền xem theo tổng công ty; hệ thống có phiếu của công ty 1 và công ty 2.",
     "1. Đăng nhập tài khoản C\n2. Mở danh sách đầy đủ\n3. Chọn công ty 1 ở ô lọc công ty",
     "Công ty: công ty 1",
     "- Ô lọc theo công ty chỉ hiện với người có quyền xem theo tổng công ty\n"
     "- Lưới chỉ còn phiếu của công ty 1"),

    ("010", "Lọc theo Phòng ban là phòng của người yêu cầu", "P1",
     "PCCTT-100 có Phiếu yêu cầu do người thuộc phòng Kinh doanh 1 lập; PCCTT-101 do người phòng Kinh doanh 2 lập.",
     "1. Mở danh sách đầy đủ\n2. Chọn phòng Kinh doanh 1 ở ô lọc phòng ban",
     "Phòng ban: Kinh doanh 1",
     "- Lưới còn PCCTT-100\n"
     "- ⚠️ Ô này lọc theo phòng của NGƯỜI YÊU CẦU, không phải phòng của người lập phiếu"),

    ("011", "Kết hợp nhiều ô lọc", "P0",
     "Khách KH-0007 có 3 phiếu, trong đó 1 phiếu Chờ làm báo giá lập ngày 15/08/2026.",
     "1. Mở danh sách đầy đủ\n2. Chọn Khách hàng KH-0007\n3. Chọn Trạng thái Chờ làm báo giá\n"
     "4. Chọn khoảng thời gian 01/08/2026 đến 31/08/2026",
     "Khách hàng: KH-0007 · Trạng thái: Chờ làm báo giá · Từ 01/08/2026 đến 31/08/2026",
     "- Các điều kiện áp dụng đồng thời\n- Còn đúng 1 dòng thỏa cả 3 điều kiện"),

    ("012", "Xóa điều kiện lọc trả về danh sách đầy đủ", "P1",
     "Đang lọc theo Trạng thái Chờ làm báo giá, lưới còn 2 dòng; tổng danh sách có 12 dòng.",
     "1. Xóa giá trị ở ô Trạng thái\n2. Chờ lưới tải lại",
     "—",
     "- Lưới quay về 12 dòng\n- Số Hiển thị ở chân lưới cập nhật đúng tổng"),

    ("013", "Lọc không ra kết quả", "P1",
     "Không có phiếu nào của khách KH-9999.",
     "1. Mở danh sách đầy đủ\n2. Gõ mã phiếu không tồn tại KHONGCO vào ô Mã phiếu cung cấp thông tin",
     "Mã phiếu cung cấp thông tin: KHONGCO",
     "- Lưới hiện dòng thông báo không có dữ liệu\n- Không hiện lỗi, không treo trang"),

    ("014", "Bộ lọc không phá phạm vi quyền", "P0",
     "Tài khoản D chỉ xem theo công ty 1. Công ty 2 có phiếu PCCTT-900.",
     "1. Đăng nhập tài khoản D\n2. Mở danh sách đầy đủ\n3. Gõ 900 vào ô Mã phiếu cung cấp thông tin",
     "Mã phiếu cung cấp thông tin: 900",
     "- Lưới không có dữ liệu\n"
     "- ⚠️ Bộ lọc không được dùng để nhìn thấy phiếu ngoài phạm vi quyền"),
]

SEC_III = [
    ("001", "Sắp xếp mặc định mới nhất lên đầu", "P0",
     "Có phiếu lập ngày 25/08/2026, 15/08/2026 và 01/08/2026.",
     "1. Mở danh sách đầy đủ\n2. Đọc cột Ngày lập phiếu từ trên xuống",
     "—",
     "- Dòng đầu là phiếu lập 25/08/2026, rồi 15/08/2026, rồi 01/08/2026"),

    ("002", "Sắp xếp theo cột Số phiếu", "P1",
     "Danh sách có ít nhất 5 phiếu.",
     "1. Mở danh sách đầy đủ\n2. Bấm tiêu đề cột Số phiếu cung cấp thông tin\n3. Bấm lần thứ hai",
     "—",
     "- Lần 1 sắp tăng dần theo mã phiếu\n- Lần 2 đảo thành giảm dần"),

    ("003", "Các cột không cho sắp xếp", "P2",
     "Danh sách có dữ liệu.",
     "1. Bấm lần lượt tiêu đề các cột Số phiếu xử lí, Khách hàng, Người yêu cầu, Ngày nhận yêu cầu, Hành động",
     "—",
     "- Các cột này không đổi thứ tự và không hiện mũi tên sắp xếp"),

    ("004", "Phân trang", "P0",
     "Danh sách có 27 phiếu, mỗi trang 10 dòng.",
     "1. Mở danh sách đầy đủ\n2. Đọc dòng thông tin hiển thị ở chân lưới\n3. Bấm sang trang 2, rồi trang 3",
     "—",
     "- Trang 1 có 10 dòng, trang 3 có 7 dòng\n- Dòng thông tin ở chân lưới cập nhật đúng theo trang"),

    ("005", "Đổi số dòng mỗi trang", "P1",
     "Danh sách có 27 phiếu.",
     "1. Đổi số dòng mỗi trang sang 25\n2. Đọc lại lưới",
     "Số dòng mỗi trang: 25",
     "- Trang 1 có 25 dòng, còn 2 trang\n- Cột STT đánh số liên tục từ 1"),

    ("006", "Giữ điều kiện lọc khi sang trang", "P1",
     "Đang lọc Trạng thái Chờ làm báo giá, kết quả có 15 dòng chia 2 trang.",
     "1. Bấm sang trang 2",
     "—",
     "- Trang 2 vẫn chỉ có phiếu Chờ làm báo giá\n- Ô lọc vẫn giữ giá trị đã chọn"),
]

SEC_IV = [
    ("001", "Dữ liệu điền sẵn khi lập phiếu", "P0",
     "Phiếu xử lý PXL-055 ở trạng thái Chờ cung cấp thông tin, của khách KH-0007 - CÔNG TY TNHH ABC, "
     "người liên hệ Trần Văn C số 0900000009, địa chỉ sửa chữa Số 1 Nguyễn Trãi, Hà Nội.",
     "1. Từ menu bánh răng của PXL-055 bấm Tạo phiếu cung cấp thông tin\n"
     "2. Đọc toàn bộ khối Thông tin khách hàng",
     "—",
     "- Số phiếu xử lý hiện PXL-055 dạng liên kết mở được sang phiếu xử lý\n"
     "- Người yêu cầu, Phòng yêu cầu, Ngày nhận phiếu xử lý điền sẵn\n"
     "- Khách hàng hiện KH-0007 - CÔNG TY TNHH ABC; Người liên hệ Trần Văn C; Số điện thoại liên hệ 0900000009; "
     "Địa chỉ sửa chữa Số 1 Nguyễn Trãi, Hà Nội\n"
     "- Tất cả các ô trên đều khóa, chỉ ô Ghi chú cho nhập"),

    ("002", "Dòng thiết bị chuyển sang từ Phiếu xử lý", "P0",
     "PXL-055 có 2 thiết bị được đánh dấu cần sửa chữa, mỗi thiết bị 1 lỗi.",
     "1. Mở màn Tạo phiếu cung cấp thông tin từ PXL-055\n"
     "2. Xem khối B - I - Dịch vụ kiểm tra, sửa chữa",
     "—",
     "- Có đúng 2 dòng thiết bị\n"
     "- Mỗi dòng hiện Tên thiết bị - Model - Mã hàng hóa, dòng Thiết bị, dòng Lỗi thiết bị, Serial và "
     "Số BBBGNT hoặc BBXNCV\n"
     "- Khối A - Bảo hành thiết bị đang trống"),

    ("003", "Ba dòng con của mỗi thiết bị", "P0",
     "Đang mở màn Tạo phiếu, khối B-I có thiết bị thứ nhất.",
     "1. Xem các dòng con đánh số 1.1, 1.2, 1.3 của thiết bị thứ nhất",
     "—",
     "- Dòng 1.1 là Công, có ô Số lượng, Giá vốn, Đơn giá bán, Thành tiền, Chiết khấu, "
     "Thành tiền sau chiết khấu, Ghi chú\n"
     "- Dòng 1.2 là Danh sách dịch vụ, có dấu cộng để thêm dịch vụ\n"
     "- Dòng 1.3 là danh sách vật tư, có dấu cộng để thêm vật tư"),

    ("004", "Cột Giá vốn hiện ở màn lập phiếu", "P0",
     "Đang mở màn Tạo phiếu.",
     "1. Đọc hàng tiêu đề bảng khối B-I",
     "—",
     "- Có cột Giá vốn nằm giữa cột Số lượng và cột Đơn giá bán"),

    ("005", "Thêm dịch vụ cho thiết bị", "P0",
     "Danh mục dịch vụ có dịch vụ Vệ sinh máy đang hoạt động, thuộc loại dịch vụ và có tính doanh thu.",
     "1. Bấm dấu cộng ở dòng Danh sách dịch vụ của thiết bị thứ nhất\n"
     "2. Trong cửa sổ Dịch vụ sửa chữa, gõ Vệ sinh vào ô Tên dịch vụ\n"
     "3. Bấm vào dòng Vệ sinh máy",
     "Tên dịch vụ: Vệ sinh",
     "- Cửa sổ Dịch vụ sửa chữa có các cột STT, Tên dịch vụ, % Định mức giảm giá\n"
     "- Sau khi chọn, dịch vụ được thêm thành một dòng con của thiết bị\n"
     "- Dòng mới có sẵn Đơn giá bán lấy từ danh mục dịch vụ"),

    ("006", "Xóa một dịch vụ đã thêm", "P1",
     "Thiết bị thứ nhất đang có 2 dịch vụ.",
     "1. Bấm dấu nhân màu đỏ ở cuối dòng dịch vụ thứ hai",
     "—",
     "- Dòng dịch vụ thứ hai biến mất ngay\n- Các số tiền ở khối D giảm tương ứng"),

    ("007", "Thêm vật tư cho thiết bị", "P0",
     "Có hàng hóa mã HH-001 tên Lọc gió, đơn vị Cái, đơn giá bán 150000.",
     "1. Bấm dấu cộng ở dòng danh sách vật tư của thiết bị thứ nhất\n"
     "2. Gõ HH-001 trong cửa sổ tìm hàng hóa\n3. Bấm chọn hàng hóa",
     "Hàng hóa: HH-001 - Lọc gió",
     "- Hệ thống báo Thêm thành công\n"
     "- Dòng vật tư mới có Tên vật tư Lọc gió, ĐVT Cái, Đơn giá bán 150,000, Số lượng mặc định 1"),

    ("008", "Tính Thành tiền của dòng vật tư", "P0",
     "Dòng vật tư Lọc gió đơn giá bán 150000.",
     "1. Nhập Số lượng 3 cho dòng vật tư Lọc gió\n2. Đọc cột Thành tiền của dòng đó",
     "Số lượng: 3 · Đơn giá bán: 150,000",
     "- Thành tiền hiện 450,000 ngay khi rời khỏi ô nhập, không cần tải lại trang"),

    ("009", "Tính Thành tiền sau chiết khấu", "P0",
     "Dòng vật tư Lọc gió có Thành tiền 450,000.",
     "1. Nhập Chiết khấu 100000 cho dòng vật tư đó\n2. Đọc cột Thành tiền sau chiết khấu",
     "Chiết khấu: 100,000",
     "- Thành tiền sau chiết khấu hiện 350,000"),

    ("010", "Chuyển thiết bị từ Sửa chữa sang Bảo hành", "P0",
     "Thiết bị thứ nhất đang ở khối B-I, có Thành tiền công 500,000, 1 dịch vụ 200,000 và 1 vật tư 450,000.",
     "1. Ở ô Loại công việc của thiết bị thứ nhất, chọn Bảo hành\n"
     "2. Xem khối A và khối B-I",
     "Loại công việc: Bảo hành",
     "- Nguyên dòng thiết bị kèm dịch vụ và vật tư chuyển sang khối A - Bảo hành thiết bị\n"
     "- Thiết bị biến mất khỏi khối B-I\n"
     "- Cột Chi phí được bảo hành của dòng công, dòng dịch vụ và dòng vật tư tự đặt bằng đúng Thành tiền, "
     "cột Khách hàng phải trả về 0"),

    ("011", "Chuyển thiết bị từ Bảo hành sang Sửa chữa", "P0",
     "Thiết bị đang ở khối A. Khối C đang có dòng chi phí với Cho bảo hành 100,000 và Miễn phí 50,000.",
     "1. Ở ô Loại công việc của thiết bị trong khối A, chọn Sửa chữa\n2. Xem khối B-I và khối C",
     "Loại công việc: Sửa chữa",
     "- Thiết bị chuyển về khối B-I\n"
     "- ⚠️ Toàn bộ cột Cho bảo hành và Miễn phí ở khối C bị đặt lại về 0"),

    ("012", "Cột riêng của khối A", "P1",
     "Có ít nhất 1 thiết bị ở khối A.",
     "1. Đọc hàng tiêu đề bảng khối A",
     "—",
     "- Khối A có cột Chi phí được bảo hành và Khách hàng phải trả, không có cột Chiết khấu\n"
     "- Khối B-I có cột Chiết khấu và Thành tiền sau chiết khấu, không có 2 cột kia"),

    ("013", "Khách hàng phải trả ở khối A", "P0",
     "Dòng công của thiết bị ở khối A có Thành tiền 500,000.",
     "1. Nhập Chi phí được bảo hành 300000 cho dòng công\n2. Đọc cột Khách hàng phải trả",
     "Chi phí được bảo hành: 300,000",
     "- Khách hàng phải trả hiện 200,000"),

    ("014", "Chi phí được bảo hành không nhận số âm", "P1",
     "Dòng công ở khối A có Thành tiền 500,000.",
     "1. Nhập -100000 vào ô Chi phí được bảo hành\n2. Rời khỏi ô",
     "Chi phí được bảo hành: -100,000",
     "- Ô tự đưa về 0\n- Khách hàng phải trả giữ nguyên 500,000"),

    ("015", "Thêm thiết bị cần bảo dưỡng", "P0",
     "Khách KH-0007 đang có thiết bị Máy nén khí X số lượng 2 trong danh mục thiết bị của khách.",
     "1. Bấm Thêm mới ở khối B - II - Danh mục thiết bị cần bảo dưỡng\n"
     "2. Trong cửa sổ, bấm vào tên thiết bị Máy nén khí X",
     "Thiết bị: Máy nén khí X",
     "- Cửa sổ có các cột STT, Tên thiết bị, Mã hàng hóa, Model, Thương hiệu, Nhà cung cấp, Số lượng, Serial, "
     "Loại trang thiết bị\n"
     "- Hệ thống báo Thêm thiết bị thành công và thêm 1 dòng vào khối B-II"),

    ("016", "Chặn thêm thiết bị quá số lượng khách đang có", "P0",
     "Khách KH-0007 có thiết bị Máy nén khí X số lượng 2; khối B-II đã có 2 dòng của thiết bị này.",
     "1. Bấm Thêm mới\n2. Bấm lại vào tên thiết bị Máy nén khí X lần thứ ba",
     "Thiết bị: Máy nén khí X (lần thứ 3)",
     "- Hệ thống báo Thiết bị đã chọn quá số lượng\n- Không thêm dòng thứ ba"),

    ("017", "Chọn gói dịch vụ bảo dưỡng cho thiết bị", "P0",
     "Thiết bị Máy nén khí X đã được thêm vào khối B-II và có gói dịch vụ bảo dưỡng cấu hình sẵn.",
     "1. Xem các dòng con của thiết bị vừa thêm\n2. Nhập Số lượng 1 cho một gói dịch vụ",
     "Số lượng: 1",
     "- Dòng gói dịch vụ hiện Tên dịch vụ kèm cấp độ trong ngoặc, ĐVT là Gói\n"
     "- Thành tiền của gói bằng Số lượng nhân Đơn giá bán"),

    ("018", "Thêm vật tư cho gói dịch vụ bảo dưỡng", "P1",
     "Khối B-II có 1 gói dịch vụ bảo dưỡng.",
     "1. Bấm Thêm vật tư ngay dưới tên gói dịch vụ\n2. Chọn một hàng hóa trong cửa sổ tìm kiếm",
     "—",
     "- Vật tư được thêm thành dòng con của gói dịch vụ, không phải dòng con của thiết bị"),

    ("019", "Nhập serial tạm và Chọn serial", "P1",
     "Thiết bị Máy nén khí X ở khối B-II có 1 serial đã lưu trong hệ thống nhưng số lượng khai là 2.",
     "1. Bấm Nhập serial tạm ở dòng thiết bị\n2. Gõ SN-TAM-01\n3. Bấm Chọn serial để quay lại chế độ chọn",
     "Serial: SN-TAM-01",
     "- Bấm Nhập serial tạm đổi ô chọn thành ô gõ tay và xóa serial đang chọn\n"
     "- Bấm Chọn serial đổi lại thành ô chọn và xóa nội dung vừa gõ"),

    ("020", "Xóa một thiết bị ở khối B-II", "P1",
     "Khối B-II đang có 2 thiết bị.",
     "1. Bấm dấu nhân đỏ ở dòng thiết bị thứ hai",
     "—",
     "- Thiết bị thứ hai cùng toàn bộ gói dịch vụ và vật tư của nó biến mất\n"
     "- Số tiền ở khối D giảm tương ứng"),

    ("021", "Nhập chi phí ở khối C và kiểm tra Khách hàng phải trả", "P0",
     "Phiếu có ít nhất 1 thiết bị ở khối A nên khối C hiện đủ 3 cột chi phí bảo hành. Dòng chi phí đầu tiên "
     "của mục I. Các khoản chi phí liên quan.",
     "1. Nhập Giá trị 1000000\n2. Nhập Cho bảo hành 300000\n3. Nhập Miễn phí 200000\n"
     "4. Đọc cột Khách hàng phải trả",
     "Giá trị: 1,000,000 · Cho bảo hành: 300,000 · Miễn phí: 200,000",
     "- Khách hàng phải trả hiện 500,000"),

    ("022", "Ẩn 3 cột chi phí bảo hành khi phiếu không có thiết bị bảo hành", "P1",
     "Phiếu chưa có thiết bị nào ở khối A.",
     "1. Đọc hàng tiêu đề bảng của mục I. Các khoản chi phí liên quan và mục II. Chi phí vận chuyển thiết bị, vật tư",
     "—",
     "- Không có nhóm cột Chi phí cho bảo hành với 3 cột con Cho bảo hành, Miễn phí, Trả phí\n"
     "- Vẫn còn các cột Giá trị, Chi phí cho SC - BD, Khách hàng phải trả, Ghi chú"),

    ("023", "Khối D cộng đúng tổng", "P0",
     "Khối D - I. Bảo hành đang có: Công kiểm tra sửa chữa 500,000; Chi phí dịch vụ 200,000; Chi phí vật tư 300,000.",
     "1. Đọc dòng 1 Tổng chi phí bảo hành ở cột Thành tiền",
     "—",
     "- Dòng 1 hiện 1,000,000, đúng bằng tổng 3 dòng 1.1, 1.2, 1.3"),

    ("024", "Dòng Tổng cộng của mục III. Tổng hợp báo giá", "P0",
     "Mục III đang có dòng Bảo hành phải thanh toán 700,000 và dòng Sửa chữa bảo dưỡng phải thanh toán 2,300,000.",
     "1. Đọc dòng Tổng cộng ở cột Phải thanh toán",
     "—",
     "- Dòng Tổng cộng hiện 3,000,000\n"
     "- Hai cột Thành tiền và Giảm giá cũng cộng theo cùng cách"),

    ("025", "Chọn mẫu Điều khoản báo giá", "P0",
     "Danh mục điều khoản báo giá có ít nhất 2 mẫu.",
     "1. Ở khối Điều khoản báo giá, mở ô chọn mẫu\n2. Chọn mẫu thứ hai",
     "Mẫu điều khoản: mẫu thứ hai",
     "- Nội dung trong ô soạn thảo bên dưới đổi thành nội dung của mẫu thứ hai\n"
     "- Khi mới mở màn lập phiếu, mẫu đầu tiên đã được chọn sẵn và nội dung đã đổ sẵn"),

    ("026", "Lưu phiếu ở trạng thái Đang tạo", "P0",
     "Đã nhập đủ thông tin cho phiếu lập từ PXL-055.",
     "1. Bấm nút Lưu\n2. Chờ chuyển trang\n3. Mở lại danh sách đầy đủ và tìm phiếu vừa lập",
     "—",
     "- Hệ thống báo tạo mới thành công và quay về danh sách\n"
     "- Phiếu mới có mã dạng mã công ty chấm PCCTT chấm năm chấm số thứ tự\n"
     "- Cột Trạng thái là Đang tạo"),

    ("027", "Lưu nháp đổi trạng thái 2 chứng từ phía trước", "P0",
     "Vừa Lưu phiếu cung cấp thông tin lập từ PXL-055 của Phiếu yêu cầu YC-030.",
     "1. Mở danh sách Phiếu xử lý yêu cầu, tìm PXL-055\n"
     "2. Mở danh sách Phiếu yêu cầu, tìm YC-030",
     "—",
     "- PXL-055 chuyển sang trạng thái đang cung cấp thông tin\n"
     "- YC-030 cũng chuyển sang trạng thái đang cung cấp thông tin"),

    ("028", "Hủy bỏ khi đang lập phiếu", "P1",
     "Đang mở màn lập phiếu và đã nhập một vài ô.",
     "1. Bấm nút Hủy ở cuối trang",
     "—",
     "- Quay về danh sách đầy đủ\n- Không tạo phiếu nào\n- Trạng thái PXL-055 giữ nguyên Chờ cung cấp thông tin"),

    ("029", "Thiết bị mang nhiều lỗi bị tách dòng", "P0",
     "PXL-060 có 1 thiết bị mang 2 lỗi, mỗi lỗi đều có dịch vụ đi kèm trong danh mục lỗi thiết bị.",
     "1. Lập phiếu cung cấp thông tin từ PXL-060\n"
     "2. Đếm số dòng thiết bị ở khối B-I\n3. Mở dòng Danh sách dịch vụ của từng dòng tách ra",
     "—",
     "- Thiết bị được tách thành 2 dòng, mỗi dòng một lỗi\n"
     "- ⚠️ Các dòng tách ra hiện đang KHÔNG có dịch vụ nào, phải ghi nhận lại vì đúng nghiệp vụ thì mỗi dòng "
     "phải giữ dịch vụ của lỗi tương ứng"),
]

SEC_V = [
    ("001", "Mở màn Sửa từ danh sách", "P0",
     "Phiếu PCCTT-102 ở trạng thái Đang tạo, do tài khoản A lập.",
     "1. Đăng nhập bằng tài khoản A\n2. Mở danh sách đầy đủ\n3. Bấm bánh răng ở dòng PCCTT-102, chọn Sửa",
     "—",
     "- Mở màn sửa với đầy đủ dữ liệu đã lưu: thiết bị, dịch vụ, vật tư, chi phí, điều khoản báo giá\n"
     "- Có nút Lưu, Lưu & Gửi duyệt, Hủy"),

    ("002", "Sửa được phiếu ở trạng thái Không duyệt", "P0",
     "Phiếu PCCTT-104 ở trạng thái Không duyệt, do tài khoản A lập.",
     "1. Đăng nhập bằng tài khoản A\n2. Mở menu bánh răng ở dòng PCCTT-104",
     "—",
     "- Menu vẫn có Sửa và Xóa\n- Mở màn sửa được bình thường"),

    ("003", "Không sửa được phiếu đã gửi", "P0",
     "Phiếu PCCTT-103 ở trạng thái Chờ làm báo giá, do tài khoản A lập.",
     "1. Đăng nhập bằng tài khoản A\n2. Mở menu bánh răng ở dòng PCCTT-103",
     "—",
     "- Menu KHÔNG có Sửa và Xóa\n- Chỉ còn In và các thao tác dành cho người lập Phiếu yêu cầu"),

    ("004", "Người khác không sửa được phiếu của mình", "P0",
     "Phiếu PCCTT-102 ở trạng thái Đang tạo do tài khoản A lập. Tài khoản C có quyền xem theo tổng công ty.",
     "1. Đăng nhập bằng tài khoản C\n2. Mở thẳng đường dẫn sửa phiếu PCCTT-102",
     "—",
     "- Không sửa được: hệ thống không cho lưu thay đổi\n"
     "- ⚠️ Chỉ đúng người lập phiếu mới được sửa, quyền xem cao không thay thế được"),

    ("005", "Sửa số liệu và lưu lại", "P0",
     "Phiếu PCCTT-102 Đang tạo, có dòng vật tư Lọc gió số lượng 3.",
     "1. Mở màn sửa\n2. Đổi Số lượng dòng Lọc gió thành 5\n3. Bấm Lưu\n4. Mở lại màn sửa phiếu đó",
     "Số lượng: 5",
     "- Số lượng lưu đúng 5\n- Thành tiền và khối D cập nhật theo giá trị mới"),

    ("006", "Xóa dòng đã lưu rồi lưu lại", "P1",
     "Phiếu PCCTT-102 đang có 2 thiết bị ở khối B-II.",
     "1. Mở màn sửa\n2. Xóa thiết bị thứ hai ở khối B-II\n3. Bấm Lưu\n4. Mở lại phiếu",
     "—",
     "- Phiếu chỉ còn 1 thiết bị ở khối B-II\n- Các gói dịch vụ và vật tư của thiết bị đã xóa cũng mất theo"),

    ("007", "Sửa rồi Lưu & Gửi duyệt", "P0",
     "Phiếu PCCTT-104 ở trạng thái Không duyệt, đã bổ sung đủ thông tin theo góp ý.",
     "1. Mở màn sửa\n2. Bấm Lưu & Gửi duyệt\n3. Mở lại danh sách",
     "—",
     "- Phiếu chuyển sang trạng thái Chờ làm báo giá\n- Không còn thao tác Sửa và Xóa"),

    ("008", "Ô Ghi chú duyệt hiện lại nội dung không duyệt lần trước", "P1",
     "Phiếu PCCTT-104 bị Không duyệt với ghi chú Thiếu chi phí vận chuyển.",
     "1. Mở màn xem chi tiết PCCTT-104 bằng tài khoản đã lập phiếu\n2. Cuộn xuống khối Ghi chú duyệt",
     "—",
     "- Khối Ghi chú duyệt hiện nội dung Thiếu chi phí vận chuyển ở dạng chỉ đọc"),
]

SEC_VI = [
    ("001", "Lưu & Gửi duyệt chuyển trạng thái phiếu", "P0",
     "Phiếu lập từ PXL-055 đã nhập đủ, đang ở màn lập phiếu.",
     "1. Bấm nút Lưu & Gửi duyệt\n2. Mở danh sách đầy đủ và tìm phiếu vừa gửi",
     "—",
     "- Phiếu có trạng thái Chờ làm báo giá\n- Không còn thao tác Sửa và Xóa với người lập"),

    ("002", "Gửi đi đóng dấu người và ngày xử lý lên Phiếu xử lý", "P0",
     "Vừa Lưu & Gửi duyệt phiếu lập từ PXL-055.",
     "1. Mở màn xem chi tiết PXL-055",
     "—",
     "- PXL-055 chuyển sang trạng thái đã cung cấp thông tin\n"
     "- Ghi nhận người xử lý là người vừa gửi phiếu và thời điểm xử lý là lúc gửi"),

    ("003", "Gửi đi cập nhật Phiếu yêu cầu gốc", "P0",
     "Phiếu xử lý PXL-055 thuộc Phiếu yêu cầu YC-030.",
     "1. Sau khi gửi phiếu, mở danh sách Phiếu yêu cầu và tìm YC-030",
     "—",
     "- YC-030 chuyển sang trạng thái đã có phiếu cung cấp thông tin làm báo giá"),

    ("004", "Thông báo gửi tới người lập Phiếu yêu cầu", "P0",
     "YC-030 do tài khoản A lập. Phiếu cung cấp thông tin có 1 dòng dịch vụ sửa chữa. "
     "Người gửi phiếu là tài khoản G tên Lê Văn G.",
     "1. Tài khoản G bấm Lưu & Gửi duyệt\n2. Đăng nhập bằng tài khoản A\n3. Mở chuông thông báo",
     "—",
     "- Tài khoản A nhận được thông báo có nội dung nói rằng có phiếu cung cấp thông tin cần làm báo giá "
     "từ Lê Văn G\n"
     "- Bấm vào thông báo mở đúng danh sách Chờ làm báo giá"),

    ("005", "Không bắn thông báo khi phiếu chỉ có bảo hành", "P1",
     "Phiếu chỉ có thiết bị ở khối A, khối B-I và B-II đều trống.",
     "1. Bấm Lưu & Gửi duyệt\n2. Đăng nhập bằng tài khoản đã lập Phiếu yêu cầu\n3. Mở chuông thông báo",
     "—",
     "- ⚠️ Không có thông báo mới nào về phiếu này\n- Phiếu vẫn chuyển đúng sang Chờ làm báo giá"),

    ("006", "Gửi phiếu có bảo hành sinh trạng thái bảo hành", "P0",
     "Phiếu có 2 thiết bị ở khối A - Bảo hành thiết bị.",
     "1. Bấm Lưu & Gửi duyệt\n2. Mở danh sách đầy đủ và đọc cột Trạng thái bảo hành của phiếu vừa gửi",
     "—",
     "- Cột Trạng thái bảo hành hiện Đã tạo phiếu bảo hành"),

    ("007", "Thao tác Từ chối tiếp nhận chỉ hiện với người lập Phiếu yêu cầu", "P0",
     "Phiếu PCCTT-103 Chờ làm báo giá, có dòng sửa chữa, mỗi thiết bị 1 lỗi. Phiếu yêu cầu do tài khoản A lập. "
     "Tài khoản G là người lập phiếu cung cấp thông tin.",
     "1. Đăng nhập bằng tài khoản G, mở màn xem chi tiết PCCTT-103\n"
     "2. Đăng nhập bằng tài khoản A, mở lại đúng phiếu đó",
     "—",
     "- Tài khoản G không thấy khối Ghi chú duyệt và không thấy nút Không duyệt\n"
     "- Tài khoản A thấy cả khối Ghi chú duyệt và nút Không duyệt"),

    ("008", "Bắt buộc nhập Ghi chú duyệt khi Không duyệt", "P0",
     "Tài khoản A đang mở màn xem chi tiết PCCTT-103.",
     "1. Để trống ô Ghi chú duyệt\n2. Bấm nút Không duyệt",
     "Ghi chú duyệt: để trống",
     "- Hệ thống báo thao tác thất bại và hiện lỗi đỏ ngay dưới ô Ghi chú duyệt\n"
     "- Trạng thái phiếu giữ nguyên Chờ làm báo giá"),

    ("009", "Không duyệt thành công", "P0",
     "Tài khoản A đang mở PCCTT-103, người lập phiếu là tài khoản G.",
     "1. Nhập Ghi chú duyệt: Thiếu chi phí vận chuyển\n2. Bấm Không duyệt",
     "Ghi chú duyệt: Thiếu chi phí vận chuyển",
     "- Hệ thống báo thao tác thành công và chuyển về danh sách Chờ làm báo giá\n"
     "- Phiếu chuyển sang trạng thái Không duyệt\n"
     "- Phiếu không còn nằm trong danh sách Chờ làm báo giá"),

    ("010", "Không duyệt trả trạng thái 2 chứng từ phía trước", "P0",
     "Vừa Không duyệt phiếu PCCTT-103 thuộc PXL-055 và YC-030.",
     "1. Mở PXL-055\n2. Mở YC-030",
     "—",
     "- Cả hai quay về trạng thái đang cung cấp thông tin, để người lập phiếu sửa lại và gửi lại"),

    ("011", "Không duyệt gửi thông báo cho người lập phiếu", "P0",
     "Tài khoản A vừa Không duyệt phiếu do tài khoản G lập. Tên tài khoản A là Nguyễn Văn A.",
     "1. Đăng nhập bằng tài khoản G\n2. Mở chuông thông báo\n3. Bấm vào thông báo mới nhất",
     "—",
     "- Có thông báo nói Nguyễn Văn A không tiếp nhận phiếu cung cấp thông tin\n"
     "- Bấm vào mở thẳng màn sửa phiếu vì tài khoản G còn quyền sửa"),

    ("012", "Thao tác Tạo báo giá dịch vụ", "P0",
     "PCCTT-103 Chờ làm báo giá, có dòng sửa chữa, mỗi thiết bị đúng 1 lỗi, Phiếu yêu cầu do tài khoản A lập.",
     "1. Đăng nhập bằng tài khoản A\n2. Mở danh sách Chờ làm báo giá\n"
     "3. Bấm bánh răng ở dòng PCCTT-103, chọn Tạo báo giá dịch vụ",
     "—",
     "- Mở màn lập Báo giá dịch vụ với dữ liệu lấy sẵn từ phiếu cung cấp thông tin"),

    ("013", "Ẩn Tạo báo giá dịch vụ khi thiết bị có nhiều hơn một lỗi", "P0",
     "PCCTT-105 Chờ làm báo giá, có 1 thiết bị mang 2 lỗi. Phiếu yêu cầu do tài khoản A lập.",
     "1. Đăng nhập bằng tài khoản A\n2. Mở danh sách và bấm bánh răng ở dòng PCCTT-105",
     "—",
     "- ⚠️ Menu KHÔNG có Tạo báo giá dịch vụ và không có Từ chối tiếp nhận\n"
     "- Đây là điểm dễ bị hiểu nhầm thành lỗi mất nút, cần ghi nhận rõ khi test"),

    ("014", "Ẩn Tạo báo giá dịch vụ khi phiếu chỉ có bảo hành", "P1",
     "PCCTT-106 Chờ làm báo giá, chỉ có thiết bị ở khối A, không có dòng sửa chữa, không có thiết bị bảo dưỡng, "
     "các khoản chi phí cho sửa chữa - bảo dưỡng đều bằng 0.",
     "1. Đăng nhập bằng tài khoản đã lập Phiếu yêu cầu\n2. Bấm bánh răng ở dòng PCCTT-106",
     "—",
     "- Menu không có Tạo báo giá dịch vụ và Từ chối tiếp nhận, chỉ còn In"),
]

SEC_VII = [
    ("001", "Xóa phiếu ở trạng thái Đang tạo", "P0",
     "Phiếu PCCTT-102 Đang tạo do tài khoản A lập.",
     "1. Đăng nhập bằng tài khoản A\n2. Bấm bánh răng ở dòng PCCTT-102, chọn Xóa\n3. Xác nhận",
     "—",
     "- Hệ thống hỏi xác nhận trước khi xóa\n- Sau khi xác nhận, phiếu biến mất khỏi danh sách"),

    ("002", "Hủy hộp thoại xác nhận xóa", "P1",
     "Phiếu PCCTT-102 Đang tạo.",
     "1. Chọn Xóa\n2. Bấm nút đóng hoặc hủy trên hộp thoại xác nhận",
     "—",
     "- Không xóa gì\n- Phiếu vẫn còn nguyên trong danh sách"),

    ("003", "Xóa phiếu trả trạng thái 2 chứng từ phía trước", "P0",
     "Phiếu PCCTT-102 thuộc PXL-055 và YC-030; PXL-055 đang ở trạng thái đang cung cấp thông tin.",
     "1. Xóa PCCTT-102\n2. Mở PXL-055\n3. Mở YC-030",
     "—",
     "- PXL-055 quay về trạng thái Chờ cung cấp thông tin, có thể lập phiếu mới\n"
     "- YC-030 quay về trạng thái đã xử lý"),

    ("004", "Xóa phiếu xóa sạch dòng chi tiết", "P0",
     "Phiếu PCCTT-102 có 2 thiết bị sửa chữa, 3 dịch vụ, 4 vật tư, 1 thiết bị bảo dưỡng và 5 dòng chi phí.",
     "1. Xóa PCCTT-102\n2. Lập lại phiếu mới từ PXL-055\n3. Xem các khối A, B, C",
     "—",
     "- Phiếu mới bắt đầu sạch, không sót dòng nào của phiếu cũ"),

    ("005", "Xóa được phiếu ở trạng thái Không duyệt", "P1",
     "Phiếu PCCTT-104 ở trạng thái Không duyệt do tài khoản A lập.",
     "1. Đăng nhập bằng tài khoản A\n2. Bấm bánh răng ở dòng PCCTT-104, chọn Xóa, xác nhận",
     "—",
     "- Xóa thành công\n- Hai chứng từ phía trước quay về trạng thái tương ứng"),

    ("006", "Không xóa được phiếu đã gửi", "P0",
     "Phiếu PCCTT-103 ở trạng thái Chờ làm báo giá.",
     "1. Đăng nhập bằng tài khoản đã lập PCCTT-103\n2. Mở menu bánh răng\n"
     "3. Dùng công cụ kiểm thử gọi thẳng chức năng Xóa cho phiếu này, bỏ qua giao diện",
     "—",
     "- Menu không có mục Xóa\n"
     "- Gọi thẳng chức năng Xóa cũng không xóa được: phiếu vẫn còn và giữ nguyên trạng thái"),
]

SEC_VIII = [
    ("001", "In một phiếu", "P0",
     "Phiếu PCCTT-103 có đủ dữ liệu ở các khối A, B, C, D.",
     "1. Bấm bánh răng ở dòng PCCTT-103, chọn In\n2. Xem bản in mở ra",
     "—",
     "- Mở bản in Phiếu cung cấp thông tin làm báo giá dịch vụ theo khổ dọc\n"
     "- Bản in có thông tin khách hàng, các dòng thiết bị, dịch vụ, vật tư, chi phí và phần tổng hợp"),

    ("002", "Thao tác In luôn hiện với mọi trạng thái", "P1",
     "Có phiếu ở các trạng thái Đang tạo, Chờ làm báo giá và Không duyệt.",
     "1. Lần lượt mở menu bánh răng của từng phiếu",
     "—",
     "- Mục In có ở cả 3 dòng, không phụ thuộc trạng thái"),

    ("003", "In danh sách theo điều kiện đang lọc", "P0",
     "Đang lọc Trạng thái Chờ làm báo giá và khoảng thời gian 01/08/2026 đến 31/08/2026, kết quả 6 dòng.",
     "1. Bấm nút In danh sách trên thanh công cụ của lưới\n2. Xem bản in mở ra",
     "—",
     "- Bản in danh sách theo khổ ngang\n"
     "- Bản in có đúng 6 dòng đang hiển thị theo bộ lọc, không phải toàn bộ danh sách\n"
     "- Dòng thời gian trên bản in ghi 01/08/2026 - 31/08/2026"),

    ("004", "In danh sách khi không lọc thời gian", "P2",
     "Không chọn khoảng thời gian nào.",
     "1. Bấm In danh sách",
     "—",
     "- Bản in vẫn mở được\n- Dòng thời gian để trống hoặc chỉ có dấu gạch nối, không hiện chữ lạ"),

    ("005", "Xuất Excel danh sách", "P0",
     "Đang lọc Khách hàng KH-0007, kết quả 3 dòng.",
     "1. Bấm nút Xuất Excel trên thanh công cụ của lưới\n2. Mở tệp tải về",
     "—",
     "- Tệp tải về có tên danh sách cung cấp thông tin làm báo giá\n"
     "- Nội dung có đúng 3 dòng đang lọc"),

    ("006", "Số tiền trên tệp Excel dùng được để tính", "P1",
     "Tệp Excel vừa xuất có cột số tiền.",
     "1. Mở tệp Excel\n2. Bôi đen một cột số tiền và xem tổng ở thanh trạng thái",
     "—",
     "- ⚠️ Ô số tiền không có dấu tam giác xanh cảnh báo đang lưu dạng chữ\n"
     "- Bôi đen cột ra được tổng, không ra 0"),

    ("007", "In phiếu ngoài phạm vi quyền", "P0",
     "Tài khoản D chỉ xem theo công ty 1. Phiếu PCCTT-900 thuộc công ty 2.",
     "1. Đăng nhập bằng tài khoản D\n2. Mở thẳng đường dẫn in của PCCTT-900",
     "—",
     "- Không in ra được nội dung phiếu\n- Hệ thống báo không tìm thấy dữ liệu"),

    ("008", "Bản in phiếu có bảo hành", "P1",
     "Phiếu có cả thiết bị bảo hành và dịch vụ sửa chữa.",
     "1. In phiếu\n2. Đối chiếu phần tổng hợp trên bản in với khối D trên màn hình",
     "—",
     "- Các con số Bảo hành, Sửa chữa bảo dưỡng và Tổng cộng trên bản in khớp đúng khối D - III. Tổng hợp báo giá"),
]

SEC_IX = [
    ("001", "Bắt buộc chọn mẫu điều khoản báo giá", "P0",
     "Đang ở màn lập phiếu, đã xóa trắng nội dung ô soạn thảo Điều khoản báo giá.",
     "1. Xóa hết nội dung trong ô soạn thảo\n2. Bấm Lưu",
     "Điều khoản báo giá: để trống",
     "- Hệ thống không lưu\n- Hiện lỗi đỏ ngay dưới ô soạn thảo Điều khoản báo giá\n"
     "- Các dữ liệu đã nhập ở khối khác vẫn còn nguyên trên màn hình"),

    ("002", "Bắt buộc có Người liên hệ", "P0",
     "Phiếu xử lý gốc không có người liên hệ.",
     "1. Mở màn lập phiếu\n2. Bấm Lưu",
     "Người liên hệ: để trống",
     "- Hệ thống không lưu và hiện lỗi đỏ dưới ô Người liên hệ"),

    ("003", "Bắt buộc có Địa chỉ sửa chữa", "P0",
     "Phiếu xử lý gốc không có địa chỉ sửa chữa.",
     "1. Mở màn lập phiếu\n2. Bấm Lưu",
     "Địa chỉ sửa chữa: để trống",
     "- Hệ thống không lưu và báo lỗi ở ô địa chỉ"),

    ("004", "Số lượng của dòng công không được để trống", "P0",
     "Khối B-I có 1 thiết bị.",
     "1. Xóa trắng ô Số lượng của dòng 1.1 Công\n2. Bấm Lưu",
     "Số lượng dòng Công: để trống",
     "- Hệ thống không lưu\n- Hiện lỗi đỏ ngay dưới ô Số lượng của dòng công đó"),

    ("005", "Số lượng vật tư không được để trống", "P0",
     "Thiết bị thứ nhất có 1 dòng vật tư.",
     "1. Xóa trắng ô Số lượng của dòng vật tư\n2. Bấm Lưu",
     "Số lượng vật tư: để trống",
     "- Hệ thống không lưu và báo lỗi đúng dòng vật tư đó"),

    ("006", "Giá trị chi phí không được để trống", "P0",
     "Khối C có 5 dòng chi phí mặc định.",
     "1. Xóa trắng ô Giá trị của dòng chi phí đầu tiên\n2. Bấm Lưu",
     "Giá trị: để trống",
     "- Hệ thống không lưu và báo lỗi đỏ ở ô Giá trị của dòng đó"),

    ("007", "Chặn trùng serial ở khối thiết bị cần bảo dưỡng", "P0",
     "Khối B-II có 2 dòng cùng thiết bị Máy nén khí X.",
     "1. Chọn cùng một serial SN-001 cho cả 2 dòng\n2. Bấm Lưu",
     "Serial dòng 1: SN-001 · Serial dòng 2: SN-001",
     "- Hệ thống không lưu\n- Hiện lỗi Bị trùng serial thiết bị ngay dưới ô serial"),

    ("008", "Serial khác nhau thì lưu được", "P1",
     "Khối B-II có 2 dòng cùng thiết bị Máy nén khí X.",
     "1. Chọn serial SN-001 cho dòng 1 và SN-002 cho dòng 2\n2. Bấm Lưu",
     "Serial dòng 1: SN-001 · Serial dòng 2: SN-002",
     "- Lưu thành công, không báo lỗi trùng serial"),

    ("009", "Nhập chữ vào ô số tiền", "P1",
     "Đang ở màn lập phiếu.",
     "1. Gõ chuỗi abc vào ô Đơn giá bán của một dòng vật tư\n2. Rời khỏi ô và xem cột Thành tiền",
     "Đơn giá bán: abc",
     "- Ô không nhận chuỗi chữ, tự đưa về 0\n- Thành tiền không hiện chữ lạ và không hiện dấu hiệu lỗi tính toán"),

    ("010", "Số lượng bằng 0", "P1",
     "Dòng vật tư có Đơn giá bán 150,000.",
     "1. Nhập Số lượng 0\n2. Đọc Thành tiền và khối D",
     "Số lượng: 0",
     "- Thành tiền hiện 0\n- Khối D giảm đúng phần của dòng đó"),

    ("011", "Số tiền lớn hiển thị đủ chữ số", "P2",
     "Dòng vật tư có Số lượng 1000 và Đơn giá bán 9,999,999.",
     "1. Nhập số liệu như trên\n2. Đọc Thành tiền và dòng Tổng cộng ở khối D",
     "Số lượng: 1,000 · Đơn giá bán: 9,999,999",
     "- Thành tiền hiện 9,999,999,000 đầy đủ, có dấu phân cách hàng nghìn\n- Ô không bị cắt chữ số"),

    ("012", "Lỗi báo đúng vị trí dòng khi có nhiều thiết bị", "P0",
     "Khối B-I có 3 thiết bị, mỗi thiết bị 2 vật tư.",
     "1. Xóa trắng ô Số lượng của vật tư thứ hai thuộc thiết bị thứ ba\n2. Bấm Lưu",
     "Số lượng: để trống",
     "- ⚠️ Lỗi đỏ hiện đúng dưới ô của vật tư thứ hai thuộc thiết bị thứ ba, "
     "không nhảy lên thiết bị thứ nhất"),
]

SEC_X = [
    ("001", "Hai người cùng lập phiếu từ một Phiếu xử lý", "P0",
     "Tài khoản A và tài khoản G cùng có quyền Tạo phiếu cung cấp thông tin. PXL-055 ở trạng thái "
     "Chờ cung cấp thông tin.",
     "1. Cả hai cùng mở màn lập phiếu từ PXL-055\n2. Tài khoản A bấm Lưu trước\n"
     "3. Tài khoản G bấm Lưu sau",
     "—",
     "- Tài khoản A lưu thành công\n"
     "- ⚠️ Tài khoản G phải bị chặn vì phiếu xử lý không còn ở trạng thái Chờ cung cấp thông tin; "
     "hệ thống từ chối và báo không có quyền, không được tạo phiếu thứ hai"),

    ("002", "Phiếu bị xóa trong lúc người khác đang mở", "P1",
     "Tài khoản A mở màn sửa PCCTT-102; sau đó chính tài khoản A xóa phiếu này ở một cửa sổ khác.",
     "1. Ở cửa sổ đang mở màn sửa, bấm Lưu",
     "—",
     "- Hệ thống báo dữ liệu đã thay đổi hoặc không tìm thấy phiếu\n- Trang không treo, không tạo lại phiếu đã xóa"),

    ("003", "Phiếu bị Không duyệt trong lúc đang mở màn xem", "P1",
     "Tài khoản A và tài khoản G cùng mở PCCTT-103 ở trạng thái Chờ làm báo giá; tài khoản A bấm Không duyệt.",
     "1. Tài khoản G tải lại màn xem chi tiết",
     "—",
     "- Trạng thái hiện Không duyệt\n- Khối Ghi chú duyệt hiện lý do tài khoản A đã nhập"),

    ("004", "Bấm Lưu hai lần liên tiếp", "P0",
     "Đang ở màn lập phiếu, đã nhập đủ.",
     "1. Bấm Lưu\n2. Bấm Lưu lần thứ hai thật nhanh trước khi trang chuyển",
     "—",
     "- Nút chuyển sang trạng thái đang xử lý và không bấm lại được\n"
     "- Chỉ tạo ra đúng 1 phiếu, không tạo trùng 2 phiếu"),

    ("005", "Dữ liệu công ty không lẫn sang phiếu công ty khác", "P0",
     "Tài khoản D thuộc công ty 1 lập phiếu mới.",
     "1. Lập và gửi 1 phiếu\n2. Đăng nhập tài khoản chỉ xem theo công ty 2 và mở danh sách",
     "—",
     "- Phiếu mới không xuất hiện trong danh sách của người thuộc công ty 2\n"
     "- Mã phiếu bắt đầu bằng mã công ty 1"),

    ("006", "Xóa dịch vụ trong danh mục sau khi đã lập phiếu", "P1",
     "Phiếu PCCTT-103 đã lưu dịch vụ Vệ sinh máy; sau đó dịch vụ này bị khóa trong danh mục.",
     "1. Mở màn xem chi tiết PCCTT-103\n2. In phiếu",
     "—",
     "- Dòng dịch vụ vẫn hiện đúng tên Vệ sinh máy và đúng số tiền đã lưu\n"
     "- Bản in cũng hiện đủ, không để trống tên dịch vụ"),
]

SEC_XI = [
    ("001", "Luồng đầy đủ: lập nháp, sửa, gửi, làm báo giá", "P0",
     "Có Phiếu yêu cầu YC-030 do tài khoản A lập, đã có Phiếu xử lý PXL-055 ở trạng thái "
     "Chờ cung cấp thông tin. Tài khoản G có quyền Tạo phiếu cung cấp thông tin.",
     "1. Tài khoản G lập phiếu từ PXL-055, nhập 1 thiết bị sửa chữa kèm 1 dịch vụ và 1 vật tư, bấm Lưu\n"
     "2. Kiểm tra PXL-055 và YC-030 đã chuyển sang trạng thái đang cung cấp thông tin\n"
     "3. Tài khoản G mở lại phiếu, bổ sung 1 dòng chi phí vận chuyển, bấm Lưu & Gửi duyệt\n"
     "4. Tài khoản A mở chuông thông báo và vào danh sách Chờ làm báo giá\n"
     "5. Tài khoản A bấm Tạo báo giá dịch vụ",
     "—",
     "- Mỗi bước chuyển trạng thái đúng như mô tả\n"
     "- Tài khoản A nhận đúng thông báo và thấy phiếu trong danh sách Chờ làm báo giá\n"
     "- Màn lập Báo giá dịch vụ mở ra với dữ liệu lấy từ phiếu cung cấp thông tin"),

    ("002", "Luồng bị từ chối rồi làm lại", "P0",
     "Phiếu PCCTT-103 vừa được tài khoản G gửi, đang Chờ làm báo giá.",
     "1. Tài khoản A nhập Ghi chú duyệt Thiếu chi phí vận chuyển và bấm Không duyệt\n"
     "2. Tài khoản G mở thông báo, vào màn sửa phiếu\n"
     "3. Tài khoản G bổ sung chi phí vận chuyển và bấm Lưu & Gửi duyệt\n"
     "4. Tài khoản A mở lại danh sách Chờ làm báo giá",
     "Ghi chú duyệt: Thiếu chi phí vận chuyển",
     "- Sau bước 1 phiếu về Không duyệt và 2 chứng từ phía trước quay về trạng thái đang cung cấp thông tin\n"
     "- Tài khoản G sửa và gửi lại được\n"
     "- Sau bước 3 phiếu quay lại Chờ làm báo giá và hiện lại trong danh sách của tài khoản A"),

    ("003", "Luồng phiếu chỉ có bảo hành", "P1",
     "PXL-060 có 1 thiết bị còn bảo hành.",
     "1. Lập phiếu từ PXL-060, chuyển thiết bị sang Loại công việc Bảo hành\n"
     "2. Bấm Lưu & Gửi duyệt\n3. Mở danh sách đầy đủ và danh sách Chờ làm báo giá",
     "Loại công việc: Bảo hành",
     "- Phiếu hiện ở danh sách đầy đủ với Trạng thái bảo hành là Đã tạo phiếu bảo hành\n"
     "- Phiếu KHÔNG hiện ở danh sách Chờ làm báo giá vì không có dòng sửa chữa và không có thiết bị bảo dưỡng\n"
     "- Người lập Phiếu yêu cầu không nhận thông báo"),

    ("004", "Luồng lập nháp rồi hủy bỏ bằng cách xóa", "P1",
     "PXL-055 ở trạng thái Chờ cung cấp thông tin.",
     "1. Lập phiếu và bấm Lưu\n2. Xóa phiếu vừa lập\n3. Lập lại phiếu mới từ PXL-055 và bấm Lưu & Gửi duyệt",
     "—",
     "- Sau bước 2, PXL-055 quay về Chờ cung cấp thông tin và lập lại được\n"
     "- Phiếu mới có mã khác phiếu đã xóa\n"
     "- Kết thúc, PXL-055 ở trạng thái đã cung cấp thông tin"),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", SEC_III),
    ("IV", "LẬP PHIẾU CUNG CẤP THÔNG TIN", SEC_IV),
    ("V", "SỬA PHIẾU", SEC_V),
    ("VI", "CÁC THAO TÁC TRẠNG THÁI", SEC_VI),
    ("VII", "XÓA", SEC_VII),
    ("VIII", "IN & XUẤT EXCEL", SEC_VIII),
    ("IX", "RÀNG BUỘC NHẬP LIỆU", SEC_IX),
    ("X", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", SEC_X),
    ("XI", "LUỒNG NGHIỆP VỤ ĐẦU CUỐI", SEC_XI),
]

if __name__ == "__main__":
    build(
        output_file=os.path.join(HERE, "testcase - Phiếu cung cấp thông tin làm báo giá (ERP).xlsx"),
        sheet_name="Trang tính1",
        feature_name="Phiếu cung cấp thông tin làm báo giá (ERP)",
        module_name="Phiếu CCTT làm báo giá",
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )
