# -*- coding: utf-8 -*-
"""Sinh testcase Excel cho man "Phieu xu ly yeu cau" tren HRM (phan he CSKH)."""
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
OUTPUT_FILE = os.path.join(HERE, "testcase.xlsx")
MODULE = "Phiếu xử lý yêu cầu"

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Kiểm thử TOÀN BỘ màn hình “Phiếu xử lý yêu cầu” (CSKH → Kiểm tra bảo hành sửa chữa → Phiếu "
     "xử lý yêu cầu).\n"
     " ► Đây là chứng từ THỨ HAI của luồng dịch vụ. Phiếu LUÔN sinh ra từ một Phiếu yêu cầu kiểm "
     "tra sửa chữa – bảo hành: phòng tiếp nhận mở phiếu yêu cầu đang “Chờ xử lý” rồi bấm “Tạo phiếu "
     "xử lý yêu cầu”. Không có nút Tạo mới trên màn này.\n"
     " ► Người xử lý xem lại thiết bị khách báo hỏng, chọn NGUYÊN NHÂN cho từng thiết bị và quyết "
     "định HÀNH ĐỘNG: tư vấn qua điện thoại là xong, hoặc chuyển tiếp để cung cấp thông tin làm báo giá.\n"
     " ► Phạm vi kiểm thử: danh sách, tìm nhanh, bộ lọc, sắp xếp, phân trang, tùy chỉnh cột, lập "
     "phiếu, sửa, xem, Lưu nháp, Lưu và gửi, Không duyệt, Thêm nhanh nguyên nhân, chọn hàng "
     "hóa tương đương, đính kèm tài liệu, Lịch sử, Xóa, In phiếu, In danh sách, Xuất Excel, phân "
     "quyền và ràng buộc nhập liệu.\n"
     " ► Màn hình dùng CHUNG dữ liệu với màn tương ứng bên phần mềm ERP."),

    ("2. Đối tượng được tính / hiển thị",
     "► Danh sách hiển thị theo phạm vi quyền của người đăng nhập (xem mục 7).\n"
     " ► 6 trạng thái: “Đang tạo” (xám) · “Chờ CCTT” (cam) · “Đã CCTT” (xanh nhạt) · “Chờ CCTT bổ "
     "sung” (cam) · “Đang CCTT” (xanh dương) · “Đã tư vấn điện thoại” (xanh lá). Chữ và màu do hệ "
     "thống quyết định, màn hình chỉ hiển thị lại.\n"
     " ► 7 cột mặc định: STT | Số phiếu xử lý | Khách hàng | Người xử lý | Ngày tạo | Trạng thái | "
     "Hành động. Các cột Số phiếu yêu cầu, Tên thiết bị liên quan, Người yêu cầu, Ngày nhận yêu "
     "cầu, Địa chỉ sửa chữa, Ngày xử lý, Người/Ngày cập nhật bật thêm ở “Cấu hình cột hiển thị”.\n"
     " ► Mỗi thiết bị chọn được NHIỀU nguyên nhân, nhưng chỉ MỘT hành động."),

    ("3. Đối tượng bị ẩn / không tính",
     "► Phiếu ở trạng thái “Đang tạo” của NGƯỜI KHÁC không hiện trong danh sách, và mở bằng đường "
     "dẫn trực tiếp cũng bị từ chối — kể cả tài khoản quản trị cấp cao. In phiếu đó cũng bị chặn.\n"
     " ► Phiếu ngoài phạm vi quyền của người đăng nhập không hiện.\n"
     " ► Ô “Nguyên nhân” của mỗi dòng CHỈ liệt kê những công việc / lỗi thiết bị đã được khai cho "
     "chính hàng hóa đó, không phải toàn bộ danh mục.\n"
     " ► Nút không đủ điều kiện thì ẨN HẲN, không hiện dạng mờ: phiếu đã gửi đi thì mất nút Sửa và "
     "Xóa; phiếu không ở “Chờ CCTT” thì mất nút Tạo phiếu cung cấp thông tin và Không duyệt."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "► Hai ô “Ngày tạo từ” / “Ngày tạo đến” lọc theo NGÀY LẬP phiếu xử lý, tính trọn ngày ở cả hai đầu.\n"
     " ► Không lọc theo Ngày nhận yêu cầu hay Ngày xử lý — 2 mốc này chỉ hiển thị, in và xuất file.\n"
     " ► Để trống cả hai ô thì lấy toàn bộ."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "► Mỗi phiếu xử lý gắn với đúng 1 phiếu yêu cầu và 1 khách hàng. Toàn bộ thông tin khách hàng "
     "và danh sách thiết bị được CHÉP từ phiếu yêu cầu, để ở chế độ chỉ đọc.\n"
     " ► Mỗi dòng thiết bị gồm: tên hàng hóa, thương hiệu, model, serial, số biên bản, nội dung yêu "
     "cầu (chép sang) + nguyên nhân, hành động, nội dung xử lý và tệp đính kèm (người xử lý điền).\n"
     " ► Thiết bị do người dùng tự gõ (chưa gắn hàng hóa trong danh mục) bắt buộc phải chọn HÀNG "
     "HÓA TƯƠNG ĐƯƠNG thì mới gửi đi được — các chứng từ phía sau cần mã hàng để chạy tiếp.\n"
     " ► Phiếu xử lý → Phiếu cung cấp thông tin làm báo giá → báo giá → hợp đồng. Các trạng thái "
     "“Đã CCTT”, “Chờ CCTT bổ sung”, “Đang CCTT” do chứng từ phía sau cập nhật ngược về."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "► Cột “Tên thiết bị liên quan” gom tên các thiết bị của phiếu, bỏ trùng, mỗi tên một dòng.\n"
     " ► Bộ lọc “Tên thiết bị” và “Model” trả về phiếu NÀO CÓ ÍT NHẤT MỘT dòng khớp từ khóa; mỗi "
     "phiếu chỉ đếm một lần.\n"
     " ► Khi lưu, toàn bộ dòng thiết bị và danh sách nguyên nhân của phiếu được ghi đè bằng những "
     "gì đang có trên màn hình."),

    ("7. Phân quyền cấp",
     "Màn hình dùng 4 quyền:\n"
     " ► “Xem phiếu xử lý yêu cầu đi kiểm tra sửa chữa - bảo hành theo tổng công ty”\n"
     " ► “Xem phiếu xử lý yêu cầu đi kiểm tra sửa chữa - bảo hành theo công ty”\n"
     " ► “Xem phiếu xử lý yêu cầu đi kiểm tra sửa chữa - bảo hành theo phòng ban” — gồm cả phòng "
     "mình được giao quản lý VÀ phòng đang công tác\n"
     " ► “Tạo phiếu cung cấp thông tin” — quyền để lập chứng từ tiếp theo và để “Không duyệt”\n"
     " ► Không có quyền xem nào thì chỉ thấy phiếu do chính mình lập.\n"
     " ► Nút “Thêm nhanh” nguyên nhân đòi thêm quyền “Quản lý danh mục công việc - lỗi thiết bị”.\n"
     " ► Xem Lịch sử KHÔNG cần quyền riêng: ai vào được màn thì xem được."),

    ("8. Cách tính các ô thống kê",
     "► Ô “Hiển thị a–b / N” dưới bảng: N là tổng số phiếu khớp bộ lọc.\n"
     " ► Số dòng/trang chọn được 5 / 10 / 20 / 50 / 100, mặc định 10.\n"
     " ► Chỉ cột Số phiếu xử lý và các cột ngày mới sắp xếp được; cột chữ và cột trạng thái không "
     "sắp xếp.\n"
     " ► Xuất Excel chạy theo từng đợt và có dòng báo tiến độ; số dòng trong file bằng đúng N."),

    ("9. Ghi chú đọc bảng",
     "⚠️ Các bẫy dễ sai nhất của màn này:\n"
     " ► **Chọn “Tư vấn điện thoại” cho TẤT CẢ thiết bị thì phiếu tự thành “Đã tư vấn điện thoại”, "
     "dù bấm nút “Lưu nháp”.** Đây là hành vi đúng, không phải lỗi.\n"
     " ► “Không duyệt” KHÔNG trả phiếu yêu cầu gốc về “Chờ xử lý” (phiếu yêu cầu vẫn là “Đã xử "
     "lý”). Chỉ khi XÓA phiếu xử lý thì phiếu yêu cầu mới quay lại “Chờ xử lý”.\n"
     " ► Ô Nguyên nhân chỉ hiện lỗi của đúng hàng hóa ở dòng đó; hàng hóa chưa khai lỗi nào thì ô "
     "trống và có dòng chữ xám nhắc — dùng “Thêm nhanh” để khai ngay.\n"
     " ► Lưu nháp chỉ cần phiếu yêu cầu gốc; “Lưu và gửi” mới bắt đủ Nguyên nhân + Hành động "
     "của mọi dòng.\n"
     " ► Phiếu nháp là việc riêng của người lập: người khác mở link trực tiếp sẽ bị từ chối và đưa "
     "về danh sách."),
]

ROLE_TCS = [
    ("00", "Không có quyền xem nào thì chỉ thấy phiếu của mình", "P0",
     "Tài khoản A không được gán quyền xem nào của màn này, đã lập 2 phiếu; công ty của A có 30 "
     "phiếu do người khác lập.",
     "1. Đăng nhập bằng A\n2. Vào CSKH → Kiểm tra bảo hành sửa chữa → Phiếu xử lý yêu cầu\n"
     "3. Đọc dòng “Hiển thị a–b / N”",
     "—",
     "- Vào được màn hình\n- Chỉ hiện 2 phiếu của A\n- Không thấy 30 phiếu còn lại"),

    ("01", "Quyền xem theo tổng công ty", "P0",
     "Tài khoản B chỉ có quyền xem theo tổng công ty; hệ thống có phiếu của ít nhất 2 công ty.",
     "1. Đăng nhập bằng B\n2. Mở danh sách\n3. Bật cột Công ty rồi lọc lần lượt từng công ty",
     "—",
     "- Thấy phiếu của cả 2 công ty\n- ⚠️ Vẫn KHÔNG thấy phiếu “Đang tạo” của người khác"),

    ("02", "Quyền xem theo công ty", "P0",
     "Tài khoản C chỉ có quyền xem theo công ty, thuộc công ty 1. Công ty 1 có 5.167 phiếu (kể cả "
     "phiếu nháp của chính C), công ty khác có phiếu riêng.",
     "1. Đăng nhập bằng C\n2. Mở danh sách, đọc tổng số phiếu",
     "—",
     "- Tổng đúng bằng số phiếu công ty 1 đã gửi đi cộng phiếu nháp của chính C\n"
     "- Không thấy phiếu của công ty khác"),

    ("03", "Quyền xem theo phòng ban gồm cả phòng đang công tác", "P0",
     "Tài khoản D chỉ có quyền xem theo phòng ban, quản lý phòng Kinh doanh 1 và đang công tác tại "
     "phòng Kỹ thuật. Cả 2 phòng đều có phiếu.",
     "1. Đăng nhập bằng D\n2. Mở danh sách",
     "—",
     "- Thấy phiếu của CẢ phòng Kinh doanh 1 (được giao quản lý) VÀ phòng Kỹ thuật (đang công tác)\n"
     "- ⚠️ Đây là điểm khác với màn Phiếu yêu cầu: màn đó không cộng phòng đang công tác"),

    ("04", "Quyền tạo phiếu cung cấp thông tin mở được nút xử lý", "P0",
     "Tài khoản E có quyền “Tạo phiếu cung cấp thông tin”. Có phiếu đang “Chờ CCTT”.",
     "1. Đăng nhập bằng E\n2. Mở danh sách, lọc trạng thái “Chờ CCTT”\n3. Xem cột Hành động",
     "—",
     "- Mỗi dòng có: Tạo phiếu cung cấp thông tin · Không duyệt · In · Lịch sử"),

    ("05", "Không có quyền tạo phiếu cung cấp thông tin thì mất 2 nút", "P0",
     "Tài khoản C không có quyền “Tạo phiếu cung cấp thông tin”. Có phiếu đang “Chờ CCTT”.",
     "1. Đăng nhập bằng C\n2. Xem cột Hành động của phiếu đó và mở màn chi tiết",
     "—",
     "- Cả 2 nơi đều KHÔNG có nút Tạo phiếu cung cấp thông tin và Không duyệt\n"
     "- ⚠️ Nút phải ẩn hẳn, không hiện dạng mờ"),

    ("06", "Xem phiếu NHÁP của người khác bị từ chối — kể cả quản trị cấp cao", "P0",
     "Phiếu nháp do nhân viên G lập. Đăng nhập bằng tài khoản quản trị cấp cao.",
     "1. Lấy đường dẫn màn chi tiết của phiếu nháp đó\n2. Dán thẳng vào trình duyệt",
     "—",
     "- Hệ thống báo không có quyền xem phiếu này và đưa về màn danh sách\n"
     "- ⚠️ Đây là điểm HRM làm CHẶT HƠN phần mềm ERP (bên đó quản trị đọc được)"),

    ("07", "In phiếu nháp của người khác cũng bị chặn", "P0",
     "Phiếu nháp do người khác lập.",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng In phiếu đó, bỏ qua giao diện",
     "—",
     "- Hệ thống từ chối, không trả về nội dung phiếu\n- (Nhóm test này dành cho tester kỹ thuật)"),

    ("08", "Chặn Không duyệt khi gọi thẳng chức năng", "P0",
     "Tài khoản C không có quyền “Tạo phiếu cung cấp thông tin”. Phiếu đang “Chờ CCTT”.",
     "1. Đăng nhập bằng C\n2. Dùng công cụ kiểm thử API gọi thẳng chức năng Không duyệt\n"
     "3. Mở lại phiếu",
     "Lý do: “test”",
     "- Hệ thống từ chối, báo không có quyền\n- Trạng thái phiếu giữ nguyên “Chờ CCTT”"),

    ("09", "Chặn Thêm nhanh nguyên nhân khi thiếu quyền danh mục", "P1",
     "Tài khoản E có quyền xử lý nhưng KHÔNG có quyền “Quản lý danh mục công việc - lỗi thiết bị”.",
     "1. Đăng nhập bằng E\n2. Dùng công cụ kiểm thử API gọi thẳng chức năng Thêm nhanh nguyên nhân",
     "Tên: “Lỗi test”",
     "- Hệ thống từ chối, báo không có quyền\n- Không có bản ghi mới trong danh mục"),

    ("10", "Chặn sửa phiếu của người khác khi gọi thẳng chức năng", "P0",
     "Phiếu nháp do nhân viên G lập. Đăng nhập bằng tài khoản khác.",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Sửa phiếu nháp của G\n2. Đăng nhập lại bằng "
     "G, mở phiếu kiểm tra",
     "—",
     "- Hệ thống từ chối, báo phiếu không thuộc quyền chỉnh sửa\n- Nội dung phiếu của G không đổi"),

    ("11", "Xem Lịch sử không cần quyền riêng", "P1",
     "Tài khoản chỉ có quyền xem theo công ty, không có quyền quản trị nào.",
     "1. Mở menu hành động của một phiếu xem được\n2. Bấm mục Lịch sử",
     "—",
     "- Popup Lịch sử mở bình thường, hiện các mốc thay đổi\n- Không đòi thêm quyền nào"),
]

SEC_I = [
    ("001", "Mở màn hình từ menu", "P0",
     "Tài khoản có quyền xem, hệ thống có trên 5.000 phiếu.",
     "1. Vào CSKH → Kiểm tra bảo hành sửa chữa → Phiếu xử lý yêu cầu",
     "—",
     "- Tiêu đề màn hình: “Phiếu xử lý yêu cầu”\n"
     "- Bảng hiện đúng 7 cột: STT | Số phiếu xử lý | Khách hàng | Người xử lý | Ngày tạo | Trạng "
     "thái | Hành động\n- Có các nút Xuất Excel, In danh sách, Cấu hình cột hiển thị\n"
     "- ⚠️ KHÔNG có nút Tạo mới — phiếu chỉ sinh từ Phiếu yêu cầu"),

    ("002", "Nhãn trạng thái đúng chữ và đúng màu", "P0",
     "Có phiếu ở các trạng thái Đang tạo, Chờ CCTT, Đã CCTT, Đã tư vấn điện thoại.",
     "1. Mở danh sách, đối chiếu cột Trạng thái",
     "—",
     "- “Đang tạo” nền xám · “Chờ CCTT” nền cam · “Đã CCTT” nền xanh nhạt · “Đã tư vấn điện thoại” "
     "nền xanh lá\n- Không dòng nào hiện ra số hoặc chữ tiếng Anh"),

    ("003", "Bấm số phiếu mở màn chi tiết", "P1",
     "Có ít nhất 1 phiếu trong danh sách.",
     "1. Bấm vào số phiếu ở cột Số phiếu xử lý",
     "—",
     "- Mở màn chi tiết đúng phiếu\n- Tiêu đề: “Chi tiết phiếu xử lý yêu cầu: <số phiếu>”\n"
     "- Mọi ô ở chế độ chỉ đọc"),

    ("004", "Link ngược sang Phiếu yêu cầu gốc", "P1",
     "Phiếu xử lý bất kỳ.",
     "1. Mở màn chi tiết\n2. Bấm vào số phiếu ở ô “Phiếu yêu cầu”",
     "—",
     "- Chuyển sang màn chi tiết của Phiếu yêu cầu kiểm tra sửa chữa – bảo hành đúng số phiếu đó"),

    ("005", "Màn chi tiết hiện đúng số nút như ngoài danh sách", "P0",
     "Phiếu X đang “Chờ CCTT”, người đăng nhập có quyền “Tạo phiếu cung cấp thông tin”.",
     "1. Đếm nút hành động của phiếu X ngoài danh sách (mở cả menu “Hành động khác”)\n"
     "2. Mở màn chi tiết phiếu X, đếm nút ở cuối màn",
     "—",
     "- Danh sách: Tạo phiếu cung cấp thông tin · Không duyệt · In · Lịch sử\n"
     "- Chi tiết: đúng các nút đó (trừ Lịch sử vì đã có khối Lịch sử trong trang) cộng nút Quay lại"),

    ("006", "Khối Lịch sử nằm trong thân màn chi tiết", "P1",
     "Phiếu đã có ít nhất 1 thao tác được ghi nhận.",
     "1. Mở màn chi tiết\n2. Kéo xuống cuối trang, bấm mở khối Lịch sử",
     "—",
     "- Khối “Lịch sử” nằm trong trang, mặc định thu gọn\n- Mở ra hiện các mốc: thời gian, tên "
     "hành động, người thực hiện kèm phòng ban, nội dung thay đổi\n"
     "- ⚠️ KHÔNG có nút Lịch sử ở hàng nút cuối trang"),

    ("007", "Vào màn Sửa phiếu đã gửi bằng đường dẫn trực tiếp", "P0",
     "Phiếu đang “Chờ CCTT”.",
     "1. Gõ thẳng đường dẫn màn Sửa của phiếu đó",
     "—",
     "- Hệ thống không cho ở lại màn Sửa, chuyển về màn Chi tiết\n- Không có nút Lưu nháp / Lưu và "
     "gửi"),
]

SEC_II = [
    ("001", "Tìm nhanh theo số phiếu xử lý", "P0",
     "Tồn tại phiếu có số hiệu đầy đủ.",
     "1. Gõ số phiếu xử lý vào ô tìm nhanh\n2. Bấm Tìm kiếm",
     "Số phiếu xử lý đầy đủ",
     "- Ra đúng 1 phiếu"),

    ("002", "Tìm nhanh theo số phiếu yêu cầu", "P0",
     "Phiếu xử lý sinh ra từ một phiếu yêu cầu đã biết số hiệu.",
     "1. Gõ số phiếu YÊU CẦU vào ô tìm nhanh\n2. Bấm Tìm kiếm",
     "Số phiếu yêu cầu đầy đủ",
     "- Ra phiếu xử lý tương ứng\n- ⚠️ Đây là ngoại lệ riêng của màn này, tra ngược từ phiếu yêu cầu"),

    ("003", "Tìm nhanh theo tên khách hàng và người xử lý", "P0",
     "Có phiếu của khách hàng chứa chữ “HYUNDAI”; có phiếu do “DNS Admin” lập.",
     "1. Gõ “HYUNDAI”, bấm Tìm kiếm\n2. Xóa đi, gõ “DNS Admin”, bấm Tìm kiếm",
     "HYUNDAI · DNS Admin",
     "- Lần 1: mọi dòng đều có chữ HYUNDAI ở cột Khách hàng\n"
     "- Lần 2: mọi dòng đều có Người xử lý là DNS Admin\n"
     "- Chữ gợi ý trong ô liệt kê đủ 4 thứ tìm được"),

    ("004", "Lọc theo trạng thái", "P0",
     "Có phiếu ở nhiều trạng thái.",
     "1. Mở Tìm kiếm nâng cao\n2. Chọn trạng thái “Chờ CCTT”",
     "Trạng thái: Chờ CCTT",
     "- Danh sách tự tải lại ngay khi chọn, không phải bấm nút\n- Cột Trạng thái đồng nhất"),

    ("005", "Lọc theo số phiếu yêu cầu", "P1",
     "Biết số phiếu yêu cầu của một phiếu xử lý.",
     "1. Nhập số phiếu yêu cầu vào ô “Số phiếu yêu cầu”",
     "Số phiếu yêu cầu",
     "- Chỉ còn phiếu xử lý của phiếu yêu cầu đó"),

    ("006", "Lọc theo khách hàng", "P1",
     "Khách hàng Z có 18 phiếu xử lý.",
     "1. Ở ô Chọn khách hàng, gõ tên rồi chọn Z",
     "Khách hàng: Z",
     "- Ra đúng 18 phiếu, tất cả cùng khách hàng Z"),

    ("007", "Lọc theo tên thiết bị và model", "P0",
     "Có phiếu chứa thiết bị “Bệ kiểm tra phanh ô tô tải”, model “SL-580”.",
     "1. Nhập “Bệ kiểm tra” vào ô Tên thiết bị\n2. Xóa đi, nhập “SL-580” vào ô Model",
     "Bệ kiểm tra · SL-580",
     "- Mỗi lần lọc chỉ còn phiếu có ít nhất một thiết bị khớp\n- Mở vài phiếu để đối chiếu"),

    ("008", "Lọc theo khoảng ngày tạo", "P0",
     "Có phiếu lập trong ngày hôm nay và ngày khác.",
     "1. Chọn Ngày tạo từ = Ngày tạo đến = hôm nay",
     "Cùng một ngày ở cả hai ô",
     "- Ra đúng các phiếu lập hôm nay\n- ⚠️ Chọn cùng một ngày vẫn phải ra kết quả"),

    ("009", "Lọc theo công ty và phòng ban", "P1",
     "Người đăng nhập có quyền xem tổng công ty.",
     "1. Chọn công ty\n2. Chọn tiếp phòng ban",
     "Công ty 1 — Phòng ban 111",
     "- Tổng số giảm dần đúng theo từng lần chọn\n- Đổi công ty thì ô phòng ban tự xóa lựa chọn cũ"),

    ("010", "Kết hợp nhiều điều kiện lọc", "P0",
     "Có phiếu “Chờ CCTT” của khách Z trong tháng này.",
     "1. Lọc trạng thái + khách hàng + khoảng ngày",
     "—",
     "- Kết quả thỏa mãn đồng thời cả 3 điều kiện"),

    ("011", "Nút Làm mới xóa hết điều kiện lọc", "P1",
     "Đang áp dụng 3 điều kiện lọc.",
     "1. Bấm Làm mới",
     "—",
     "- Mọi ô lọc trở về rỗng, tổng số trở lại như ban đầu"),

    ("012", "Lọc không ra kết quả", "P1",
     "Không có phiếu nào khớp từ khóa lạ.",
     "1. Gõ “KHONG-TON-TAI-XYZ” vào ô tìm nhanh, bấm Tìm kiếm",
     "KHONG-TON-TAI-XYZ",
     "- Hiện dòng “Không có dữ liệu phù hợp bộ lọc.”\n- ⚠️ Dòng chữ này phải màu xám, không đỏ"),

    ("013", "Chữ gợi ý các ô lọc nói đúng ô đó lọc gì", "P1",
     "Mở Tìm kiếm nâng cao.",
     "1. Đọc chữ mờ trong từng ô",
     "—",
     "- Ô chọn ghi “Chọn <tên trường>”, ô gõ tay ghi “Nhập <tên trường>”\n"
     "- Không ô nào để trống hoặc ghi “Tất cả”"),
]

SEC_III = [
    ("001", "Sắp xếp theo cột được phép", "P1",
     "Danh sách có trên 20 phiếu.",
     "1. Bấm tiêu đề cột Số phiếu xử lý\n2. Bấm lần nữa để đảo chiều\n3. Bấm tiêu đề cột Ngày tạo",
     "—",
     "- Thứ tự đổi đúng chiều mỗi lần bấm"),

    ("002", "Cột KHÔNG được phép sắp xếp", "P1",
     "Danh sách đang hiển thị.",
     "1. Bấm tiêu đề cột Khách hàng\n2. Bấm tiêu đề cột Trạng thái",
     "—",
     "- Hai cột này không có biểu tượng sắp xếp và bấm vào không đổi thứ tự\n"
     "- ⚠️ Đây là thiết kế: chỉ cột định danh và cột ngày mới sắp xếp được"),

    ("003", "Chuyển trang và đổi số dòng mỗi trang", "P0",
     "Bộ lọc hiện tại ra trên 100 phiếu.",
     "1. Sang trang 2\n2. Đổi số dòng/trang sang 50\n3. Về trang 1",
     "Số dòng/trang: 50",
     "- Dòng “Hiển thị a–b / N” cập nhật đúng\n- Không dòng nào lặp giữa 2 trang"),

    ("004", "Tùy chỉnh cột hiển thị", "P1",
     "Đang ở danh sách với 7 cột mặc định.",
     "1. Bấm Cấu hình cột hiển thị\n2. Bật thêm Số phiếu yêu cầu, Người yêu cầu, Ngày nhận yêu cầu\n"
     "3. Lưu lại, thoát ra rồi vào lại màn hình",
     "—",
     "- Bảng hiện thêm đúng 3 cột vừa bật\n- Vào lại vẫn giữ nguyên lựa chọn"),
]

SEC_IV = [
    ("001", "Lập phiếu xử lý từ Phiếu yêu cầu", "P0",
     "Phiếu yêu cầu Y đang “Chờ xử lý”, gửi về phòng của người đăng nhập, chưa có phiếu xử lý nào.",
     "1. Mở màn Yêu cầu kiểm tra sửa chữa – bảo hành\n2. Ở dòng phiếu Y, bấm “Tạo phiếu xử lý yêu cầu”",
     "—",
     "- Mở màn “Lập phiếu xử lý yêu cầu”\n- Khối Thông tin yêu cầu điền sẵn và KHÓA: Phiếu yêu cầu, "
     "Người yêu cầu, Phòng yêu cầu, Ngày nhận yêu cầu, Khách hàng, Người liên hệ, SĐT, Địa chỉ sửa chữa\n"
     "- Bảng thiết bị chép đủ số dòng của phiếu yêu cầu"),

    ("002", "Không lập được phiếu khi phiếu yêu cầu không đủ điều kiện", "P0",
     "Phiếu yêu cầu đã có phiếu xử lý; và một phiếu yêu cầu khác đang ở “Đang tạo”.",
     "1. Gõ thẳng đường dẫn màn lập phiếu kèm mã của 2 phiếu yêu cầu trên",
     "—",
     "- Cả 2 lần đều bị từ chối, báo phiếu yêu cầu không ở trạng thái chờ xử lý của phòng bạn hoặc "
     "đã có phiếu xử lý\n- Được đưa về màn danh sách"),

    ("003", "Chọn nguyên nhân cho từng thiết bị", "P0",
     "Đang ở màn lập phiếu, hàng hóa của dòng đã khai lỗi trong danh mục.",
     "1. Mở ô Nguyên nhân của dòng thiết bị\n2. Chọn 2 nguyên nhân",
     "—",
     "- Ô cho chọn NHIỀU nguyên nhân, hiện dạng thẻ\n"
     "- ⚠️ Danh sách chỉ gồm lỗi đã khai cho ĐÚNG hàng hóa của dòng đó, không phải cả danh mục"),

    ("004", "Hàng hóa chưa khai lỗi nào", "P1",
     "Dòng thiết bị có hàng hóa chưa được khai lỗi trong danh mục.",
     "1. Mở ô Nguyên nhân của dòng đó",
     "—",
     "- Ô không có lựa chọn nào\n- Có dòng chữ xám: “Hàng hóa này chưa khai lỗi thiết bị nào trong "
     "danh mục.”\n- Có nút “Thêm nhanh” ngay dưới"),

    ("005", "Chọn hành động Cung cấp thông tin làm báo giá", "P0",
     "Đang ở màn lập phiếu, đã chọn nguyên nhân.",
     "1. Mở ô Hành động, chọn “Cung cấp thông tin làm báo giá”",
     "—",
     "- Ô Hành động có đúng 2 lựa chọn: Tư vấn điện thoại · Cung cấp thông tin làm báo giá\n"
     "- Không hiện ô nhập nội dung xử lý"),

    ("006", "Chọn hành động Tư vấn điện thoại thì hiện ô nội dung xử lý", "P0",
     "Đang ở màn lập phiếu.",
     "1. Chọn hành động “Tư vấn điện thoại”",
     "—",
     "- Hiện thêm ô nhập “Nhập nội dung xử lý” ngay dưới\n- Đổi sang hành động khác thì ô này biến "
     "mất và nội dung đã gõ bị bỏ"),

    ("007", "Thêm nhanh nguyên nhân ngay trong form", "P0",
     "Đang ở màn lập/sửa phiếu, người dùng có quyền quản lý danh mục công việc - lỗi thiết bị.",
     "1. Bấm “Thêm nhanh” dưới ô Nguyên nhân\n2. Chọn Loại công việc / lỗi, nhập Tên\n3. Bấm Lưu",
     "Loại: Lỗi đã xác định — Tên: “Bục ống dẫn khí nén”",
     "- Popup có các ô: Loại, Tên, Định mức công, Định mức đàm phán giá, VAT, Đơn giá bán, Hệ số "
     "công nghệ, Ghi chú\n- Lưu xong popup ĐÓNG lại\n- Lỗi mới xuất hiện trong ô Nguyên nhân của "
     "đúng dòng đó và được TỰ TÍCH CHỌN"),

    ("008", "Thêm nhanh thiếu trường bắt buộc", "P1",
     "Popup Thêm nhanh đang mở, chưa nhập gì.",
     "1. Bấm Lưu",
     "—",
     "- Báo lỗi đỏ ngay dưới ô Loại và ô Tên\n- Popup không đóng"),

    ("009", "Chọn hàng hóa tương đương cho thiết bị tự gõ", "P0",
     "Phiếu yêu cầu gốc có dòng thiết bị người dùng tự gõ (chưa gắn hàng hóa trong danh mục).",
     "1. Ở dòng đó, bấm “Chọn hàng hóa tương đương”\n2. Tìm và chọn một hàng hóa\n3. Xem lại ô Nguyên nhân",
     "—",
     "- Popup chọn hàng hóa mở ra, tìm được theo tên/mã/model\n- Chọn xong tên hàng hóa hiện thành "
     "dòng phụ “Thiết bị tương đương”\n- Danh sách Nguyên nhân nạp lại theo hàng hóa mới"),

    ("010", "Hiển thị tên thiết bị và thiết bị tương đương", "P1",
     "Phiếu có dòng thiết bị đã gắn hàng hóa tương đương.",
     "1. Mở màn chi tiết, xem cột Tên hàng hóa",
     "—",
     "- Dòng đầu là tên thiết bị khách báo\n- Dòng phụ nhỏ màu xám: “Thiết bị tương đương: <tên "
     "hàng hóa trong danh mục>”"),

    ("011", "Đính kèm tài liệu cho dòng thiết bị", "P1",
     "Đang lập/sửa phiếu, có sẵn tệp PDF dưới 20MB.",
     "1. Bấm Chọn tệp ở cột File đính kèm\n2. Chờ tải xong",
     "Tệp: bien-ban.pdf",
     "- Trong lúc tải có báo đang tải lên\n- Xong thì hiện biểu tượng loại tệp, tên tệp và 3 nút "
     "Tải xuống / Thay đổi / Xóa"),

    ("012", "Chặn đính kèm tệp sai định dạng", "P1",
     "Có sẵn tệp .txt.",
     "1. Chọn tệp .txt ở cột File đính kèm",
     "Tệp: ghi-chu.txt",
     "- Báo chỉ nhận tệp PDF, ảnh, Word hoặc Excel\n- Không tệp nào được gắn vào dòng"),

    ("013", "Lưu nháp", "P0",
     "Đang ở màn lập phiếu, chưa chọn nguyên nhân và hành động.",
     "1. Bấm Lưu nháp",
     "—",
     "- Lưu thành công, quay về danh sách\n- Phiếu mới ở trạng thái “Đang tạo”, đã có số phiếu\n"
     "- ⚠️ Lưu nháp KHÔNG đòi Nguyên nhân / Hành động"),

    ("014", "Sửa phiếu nháp", "P0",
     "Phiếu nháp do chính người đăng nhập lập.",
     "1. Bấm Sửa ở dòng phiếu\n2. Chọn nguyên nhân và hành động\n3. Bấm Lưu nháp\n4. Mở lại phiếu",
     "—",
     "- Lưu thành công, mở lại thấy đúng nguyên nhân + hành động đã chọn\n- Số phiếu KHÔNG đổi"),

    ("015", "Xóa dòng thiết bị khỏi phiếu", "P1",
     "Phiếu đang sửa có 2 dòng thiết bị.",
     "1. Bấm nút xóa ở dòng thứ 2\n2. Lưu nháp rồi mở lại phiếu",
     "—",
     "- Sau khi lưu, phiếu chỉ còn 1 dòng thiết bị"),

    ("016", "Cảnh báo khi thoát lúc chưa lưu", "P0",
     "Đang ở màn lập phiếu.",
     "1. Chọn một nguyên nhân\n2. Bấm Quay lại",
     "—",
     "- Hiện cửa sổ “Thông tin chưa lưu”\n- Bấm Ở lại thì dữ liệu còn nguyên; bấm Thoát mới rời đi"),

    ("017", "Bảng thiết bị cuộn ngang được ở cả trên và dưới", "P2",
     "Thu hẹp cửa sổ trình duyệt để bảng bị tràn ngang.",
     "1. Kéo thanh cuộn phía TRÊN bảng\n2. Kéo thanh cuộn phía DƯỚI bảng",
     "—",
     "- Có thanh cuộn ở cả trên và dưới, kéo bên nào bên kia chạy theo\n- Phóng rộng thì thanh trên tự ẩn"),
]

SEC_V = [
    ("001", "Gửi phiếu đi để cung cấp thông tin", "P0",
     "Phiếu nháp có 1 thiết bị, đã chọn nguyên nhân và hành động “Cung cấp thông tin làm báo giá”.",
     "1. Bấm “Lưu và gửi”\n2. Xác nhận ở cửa sổ hỏi lại",
     "—",
     "- Phiếu chuyển sang “Chờ CCTT”\n- Ghi nhận thời điểm gửi\n"
     "- Phiếu yêu cầu GỐC chuyển sang “Đã xử lý”, điền Người xử lý và Ngày xử lý"),

    ("002", "Thông báo cho người lập phiếu cung cấp thông tin", "P0",
     "Công ty có 7 người được cấp quyền “Tạo phiếu cung cấp thông tin”.",
     "1. Gửi phiếu đi\n2. Đăng nhập lần lượt bằng vài người trong số đó, mở chuông thông báo",
     "—",
     "- Những người có quyền đó và CÙNG CÔNG TY đều nhận được thông báo\n"
     "- Nội dung dạng: [PXL] Chờ duyệt: <số phiếu>. Khách hàng: <tên khách>.\n"
     "- Bấm vào mở đúng màn chi tiết phiếu\n- ⚠️ Thông báo đi theo QUYỀN, không theo phòng ban"),

    ("003", "Mọi thiết bị đều Tư vấn điện thoại", "P0",
     "Phiếu có 1 thiết bị duy nhất, chọn hành động “Tư vấn điện thoại” và đã nhập nội dung xử lý.",
     "1. Bấm nút “Lưu nháp” (KHÔNG bấm Lưu và gửi)\n2. Xem trạng thái phiếu và phiếu yêu cầu gốc",
     "Nội dung xử lý: “Đã hướng dẫn khách kiểm tra nguồn điện”",
     "- ⚠️ Phiếu vẫn chuyển thành “Đã tư vấn điện thoại” dù bấm Lưu nháp — đây là hành vi đúng\n"
     "- Phiếu yêu cầu gốc cũng chuyển “Đã tư vấn điện thoại”, luồng kết thúc tại đây\n"
     "- Không ai nhận thông báo chờ cung cấp thông tin"),

    ("004", "Phiếu nhiều thiết bị, chỉ một dòng cần báo giá", "P0",
     "Phiếu có 2 thiết bị: dòng 1 chọn Tư vấn điện thoại (có nội dung xử lý), dòng 2 chọn Cung cấp "
     "thông tin làm báo giá.",
     "1. Bấm Lưu và gửi, xác nhận",
     "—",
     "- Phiếu chuyển sang “Chờ CCTT” (KHÔNG phải Đã tư vấn điện thoại)\n"
     "- Phiếu yêu cầu gốc chuyển “Đã xử lý”"),

    ("005", "Không duyệt phiếu", "P0",
     "Phiếu đang “Chờ CCTT”, người đăng nhập có quyền “Tạo phiếu cung cấp thông tin”. Phiếu do "
     "nhân viên G lập.",
     "1. Bấm “Không duyệt” ở dòng phiếu\n2. Nhập lý do\n3. Bấm nút Không duyệt trong popup\n"
     "4. Đăng nhập bằng G, mở chuông thông báo và mở phiếu",
     "Lý do: “Thiếu thông tin báo giá”",
     "- Phiếu trở lại “Đang tạo”, lý do lưu trên phiếu và hiện ở khối thông tin (chữ xám)\n"
     "- G nhận thông báo: [PXL] Từ chối: <số phiếu>. Lý do: …\n"
     "- G sửa lại và gửi lần nữa được"),

    ("006", "Không duyệt mà bỏ trống lý do", "P0",
     "Popup Không duyệt đang mở.",
     "1. Bấm nút Không duyệt",
     "—",
     "- Báo lỗi đỏ dưới ô Lý do không duyệt\n- Popup không đóng, phiếu chưa đổi trạng thái"),

    ("007", "Không duyệt KHÔNG trả phiếu yêu cầu gốc về Chờ xử lý", "P0",
     "Phiếu xử lý đang “Chờ CCTT”, phiếu yêu cầu gốc đang “Đã xử lý”.",
     "1. Không duyệt phiếu xử lý\n2. Mở màn Yêu cầu kiểm tra sửa chữa – bảo hành, tìm phiếu gốc",
     "Lý do: “test”",
     "- Phiếu xử lý về “Đang tạo”\n- ⚠️ Phiếu yêu cầu gốc VẪN là “Đã xử lý”, không quay lại “Chờ "
     "xử lý” — đúng nghiệp vụ, chỉ khi XÓA phiếu xử lý mới trả về"),

    ("008", "Không duyệt lần 2 khi phiếu đã về Đang tạo", "P1",
     "Phiếu vừa bị Không duyệt, đang ở “Đang tạo”.",
     "1. Dùng công cụ kiểm thử API gọi lại chức năng Không duyệt",
     "Lý do: “lần 2”",
     "- Hệ thống chặn, báo phiếu không ở trạng thái Chờ CCTT"),

    ("009", "Tạo phiếu cung cấp thông tin", "P1",
     "Phiếu đang “Chờ CCTT”, người đăng nhập có quyền tương ứng.",
     "1. Bấm “Tạo phiếu cung cấp thông tin”",
     "—",
     "- ⚠️ Màn Phiếu cung cấp thông tin chưa có trên hệ thống mới: hệ thống báo hướng dẫn xử lý tạm "
     "trên phần mềm ERP\n- Khi màn đó hoàn thành sẽ chuyển thẳng sang màn lập phiếu"),
]

SEC_VI = [
    ("001", "Xóa phiếu nháp và trả phiếu yêu cầu về Chờ xử lý", "P0",
     "Phiếu xử lý “Đang tạo” do chính người đăng nhập lập; phiếu yêu cầu gốc đang “Đã xử lý”.",
     "1. Bấm Xóa ở dòng phiếu\n2. Xác nhận\n3. Mở màn Yêu cầu kiểm tra sửa chữa – bảo hành, tìm "
     "phiếu yêu cầu gốc",
     "—",
     "- Cửa sổ hỏi “Bạn có chắc muốn xóa phiếu '<số phiếu>'?”\n- Phiếu xử lý biến mất khỏi danh sách\n"
     "- ⚠️ Phiếu yêu cầu gốc TRỞ LẠI “Chờ xử lý”, xóa Người xử lý và Ngày xử lý, và lại có nút "
     "“Tạo phiếu xử lý yêu cầu”"),

    ("002", "Hủy ở cửa sổ xác nhận xóa", "P1",
     "Phiếu nháp của chính mình.",
     "1. Bấm Xóa\n2. Bấm Hủy",
     "—",
     "- Phiếu vẫn còn nguyên, phiếu yêu cầu gốc không đổi"),

    ("003", "Không có nút Xóa với phiếu đã gửi", "P0",
     "Phiếu đang “Chờ CCTT” do chính mình lập.",
     "1. Xem cột Hành động ở danh sách và ở màn chi tiết",
     "—",
     "- Không có nút Sửa và Xóa ở cả hai nơi"),
]

SEC_VII = [
    ("001", "Xuất Excel theo bộ lọc", "P0",
     "Đang lọc trạng thái “Chờ CCTT”, còn 22 phiếu.",
     "1. Bấm Xuất Excel\n2. Giữ nguyên trường mặc định, bấm Xuất file\n3. Mở tệp",
     "—",
     "- Tệp tải về tên gợi nhớ tới màn hình\n- Có đúng 22 dòng dữ liệu\n- Cột đầu là STT"),

    ("002", "Chọn trường và thứ tự cột khi xuất", "P1",
     "Cửa sổ chọn trường đang mở.",
     "1. Bỏ chọn hết\n2. Chọn theo thứ tự: Số phiếu xử lý, Số phiếu yêu cầu, Trạng thái\n3. Xuất file",
     "—",
     "- Tệp chỉ có 3 cột (cộng STT), đúng thứ tự vừa chọn"),

    ("003", "In một phiếu", "P0",
     "Phiếu đã điền đủ nguyên nhân và hành động.",
     "1. Bấm In ở dòng phiếu\n2. Xem trang xem trước",
     "—",
     "- Mở tab mới, thấy khung tờ giấy dọc, nền quanh giấy màu trắng\n"
     "- Bảng chi tiết có đủ 9 cột, trong đó có Nguyên nhân và Hành động\n"
     "- Có số phiếu xử lý, số phiếu yêu cầu, người yêu cầu, ngày nhận yêu cầu\n"
     "- Không còn chỗ nào bỏ trống dạng ký hiệu chờ điền"),

    ("004", "In danh sách theo bộ lọc", "P0",
     "Đang lọc trạng thái “Đã tư vấn điện thoại”.",
     "1. Bấm In danh sách\n2. Xem trang xem trước",
     "—",
     "- Mở tab mới với mẫu danh sách khổ ngang, có khung tờ giấy\n- Bảng chứa đúng các phiếu đang lọc"),

    ("005", "Nút In trên trang xem trước", "P1",
     "Đang ở trang xem trước bản in.",
     "1. Quan sát vị trí nút In\n2. Bấm nút In",
     "—",
     "- Nút In nằm bên phải, thẳng mép phải tờ giấy\n- Mở hộp thoại in của trình duyệt, bản xem "
     "không có nút In và không có khung viền"),
]

SEC_VIII = [
    ("001", "Gửi đi khi thiếu Nguyên nhân và Hành động", "P0",
     "Phiếu có 1 thiết bị, chưa chọn gì.",
     "1. Bấm Lưu và gửi, xác nhận",
     "—",
     "- Không gửi được\n- Báo lỗi đỏ ngay dưới ô Nguyên nhân và ô Hành động của đúng dòng"),

    ("002", "Tư vấn điện thoại thiếu nội dung xử lý", "P0",
     "Đã chọn nguyên nhân và hành động “Tư vấn điện thoại”, để trống nội dung xử lý.",
     "1. Bấm Lưu và gửi, xác nhận",
     "—",
     "- Chặn, báo lỗi đỏ dưới ô nội dung xử lý của đúng dòng"),

    ("003", "Chọn trùng nguyên nhân cho cùng một thiết bị", "P0",
     "Phiếu có 2 dòng cùng hàng hóa, cùng serial.",
     "1. Chọn cho 2 dòng ít nhất một nguyên nhân giống nhau\n2. Bấm Lưu và gửi, xác nhận",
     "—",
     "- Chặn, báo “Bị trùng nguyên nhân của cùng thiết bị” ở CẢ HAI dòng"),

    ("004", "Thiết bị tự gõ chưa chọn hàng hóa tương đương", "P0",
     "Phiếu có dòng thiết bị người dùng tự gõ, chưa gắn hàng hóa.",
     "1. Chọn nguyên nhân + hành động cho dòng đó\n2. Bấm Lưu và gửi, xác nhận",
     "—",
     "- Chặn, báo “Phải chọn hàng hóa tương đương” tại đúng dòng"),

    ("005", "Gửi đi khi không có thiết bị nào", "P0",
     "Phiếu đã xóa hết dòng thiết bị.",
     "1. Bấm Lưu và gửi, xác nhận",
     "—",
     "- Chặn, báo yêu cầu phải có ít nhất 1 thiết bị"),

    ("006", "Lưu nháp không đòi nguyên nhân", "P1",
     "Màn lập phiếu, chưa chọn gì.",
     "1. Bấm Lưu nháp",
     "—",
     "- Lưu thành công\n- ⚠️ Ràng buộc nguyên nhân/hành động chỉ áp dụng khi gửi đi"),

    ("007", "Ô chỉ đọc không gõ được", "P1",
     "Màn lập phiếu.",
     "1. Bấm vào các ô của khối Thông tin yêu cầu, thử gõ",
     "abc",
     "- Không gõ được vào bất kỳ ô nào trong khối này\n- Ô có nền xám phân biệt với ô nhập được"),
]

SEC_IX = [
    ("001", "Hai người cùng xử lý một phiếu", "P1",
     "Phiếu “Chờ CCTT”, hai người E và F cùng có quyền và cùng mở phiếu.",
     "1. E bấm Không duyệt kèm lý do\n2. F (chưa tải lại trang) cũng bấm Không duyệt",
     "—",
     "- Thao tác của F bị chặn, báo phiếu không ở trạng thái Chờ CCTT\n- Không treo trang"),

    ("002", "Xóa phiếu vừa bị người khác xóa", "P2",
     "Hai cửa sổ cùng mở danh sách, cùng thấy phiếu nháp X.",
     "1. Cửa sổ 1 xóa phiếu X\n2. Cửa sổ 2 (chưa tải lại) cũng bấm Xóa phiếu X",
     "—",
     "- Cửa sổ 2 báo dữ liệu đã thay đổi, không treo trang"),

    ("003", "Dữ liệu lập bên ERP hiện ngay bên đây", "P0",
     "Có tài khoản dùng được cả 2 cổng.",
     "1. Lập 1 phiếu xử lý bên phần mềm ERP\n2. Sang màn hình này, tìm theo số phiếu vừa lập",
     "Số phiếu vừa lập bên ERP",
     "- Tìm thấy đúng phiếu, mở ra thấy đủ nguyên nhân và hành động đã chọn bên ERP"),
]

SEC_X = [
    ("001", "Lịch sử ghi nhận đủ các thao tác", "P0",
     "Phiếu vừa trải qua: lập mới → sửa và gửi đi → bị Không duyệt.",
     "1. Mở menu hành động của phiếu, bấm Lịch sử\n2. Đọc các mốc từ trên xuống",
     "—",
     "- Danh sách sắp xếp MỚI → CŨ\n- Có đủ 3 mốc: Từ chối · Thay đổi thông tin · Tạo mới\n"
     "- Mỗi mốc hiện: thời gian, tên hành động, người thực hiện kèm phòng ban\n"
     "- Mốc Từ chối hiện ĐÚNG lý do đã nhập"),

    ("002", "Bộ lọc trong Lịch sử", "P1",
     "Phiếu có nhiều mốc lịch sử.",
     "1. Mở popup Lịch sử\n2. Mở ô Loại hành động\n3. Chọn “Thay đổi trạng thái”\n4. Bấm Tìm kiếm",
     "—",
     "- Ô Loại hành động có đúng 3 lựa chọn: Tạo mới · Thay đổi thông tin · Thay đổi trạng thái\n"
     "- Ô Người thực hiện liệt kê đầy đủ nhân sự, không chỉ vài người có trong log\n"
     "- Lọc xong chỉ còn mốc thuộc nhóm đã chọn"),

    ("003", "Lịch sử ở màn chi tiết giống popup ngoài danh sách", "P1",
     "Cùng một phiếu.",
     "1. Mở popup Lịch sử từ danh sách, ghi lại nội dung\n2. Mở màn chi tiết, mở khối Lịch sử",
     "—",
     "- Hai nơi hiện cùng số mốc, cùng nội dung, cùng thứ tự, cùng bộ lọc"),

    ("004", "Lịch sử không ghi nhiễu khi chỉ đổi dòng thiết bị", "P2",
     "Phiếu nháp có 2 dòng thiết bị.",
     "1. Sửa phiếu, chỉ đổi nguyên nhân của một dòng rồi Lưu nháp\n2. Mở Lịch sử",
     "—",
     "- ⚠️ Lịch sử KHÔNG ghi nhận thay đổi ở dòng thiết bị (hiện chỉ theo dõi thông tin chung của "
     "phiếu và trạng thái) — đây là giới hạn đã biết, không phải lỗi mất dữ liệu"),
]

SEC_XI = [
    ("001", "Luồng đầy đủ: lập → gửi → không duyệt → gửi lại → xóa", "P0",
     "Phiếu yêu cầu Y đang “Chờ xử lý”. Nhân viên G thuộc phòng tiếp nhận, E có quyền tạo phiếu "
     "cung cấp thông tin.",
     "1. G lập phiếu xử lý từ Y, chọn nguyên nhân + hành động Cung cấp thông tin, Lưu và gửi\n"
     "2. E nhận thông báo, mở phiếu, bấm Không duyệt kèm lý do\n"
     "3. G nhận thông báo, sửa phiếu và gửi lại\n"
     "4. G xóa phiếu (sau khi Không duyệt lần nữa)\n"
     "5. Mở màn Yêu cầu kiểm tra sửa chữa – bảo hành, tìm phiếu Y",
     "Lý do: “Thiếu thông tin báo giá”",
     "- Bước 1: phiếu “Chờ CCTT”, phiếu Y thành “Đã xử lý”\n"
     "- Bước 2: phiếu về “Đang tạo”, phiếu Y VẪN “Đã xử lý”\n"
     "- Bước 3: phiếu lại “Chờ CCTT”, số phiếu không đổi\n"
     "- Bước 4-5: xóa xong phiếu Y TRỞ LẠI “Chờ xử lý” và lại lập được phiếu xử lý mới"),

    ("002", "Luồng kết thúc bằng tư vấn điện thoại", "P0",
     "Phiếu yêu cầu Z đang “Chờ xử lý”, có 1 thiết bị.",
     "1. Lập phiếu xử lý từ Z\n2. Chọn nguyên nhân, hành động “Tư vấn điện thoại”, nhập nội dung "
     "xử lý\n3. Lưu\n4. Kiểm tra phiếu xử lý và phiếu Z",
     "Nội dung xử lý: “Hướng dẫn khách tự khắc phục”",
     "- Phiếu xử lý: “Đã tư vấn điện thoại”\n- Phiếu Z: “Đã tư vấn điện thoại”\n"
     "- Không ai nhận thông báo chờ cung cấp thông tin\n- Luồng dịch vụ kết thúc, không đi tiếp"),

    ("003", "Đối chiếu số liệu 2 cổng", "P1",
     "Cùng bộ lọc trạng thái “Chờ CCTT” trên cả 2 cổng, cùng tài khoản.",
     "1. Đếm số phiếu bên phần mềm ERP\n2. Đếm số phiếu trên màn hình này",
     "—",
     "- Hai con số bằng nhau (cùng đọc một nguồn dữ liệu)"),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", SEC_III),
    ("IV", "LẬP PHIẾU, SỬA & XEM", SEC_IV),
    ("V", "GỬI DUYỆT & KHÔNG DUYỆT", SEC_V),
    ("VI", "XÓA", SEC_VI),
    ("VII", "XUẤT EXCEL / IN", SEC_VII),
    ("VIII", "RÀNG BUỘC NHẬP LIỆU", SEC_VIII),
    ("IX", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", SEC_IX),
    ("X", "LỊCH SỬ THAY ĐỔI", SEC_X),
    ("XI", "LUỒNG NGHIỆP VỤ ĐẦU – CUỐI", SEC_XI),
]

build(output_file=OUTPUT_FILE,
      sheet_name="Trang tính1",
      feature_name="Phiếu xử lý yêu cầu - Cập nhật ngày 21/08/2026",
      module_name=MODULE,
      description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS,
      sections=SECTIONS)
