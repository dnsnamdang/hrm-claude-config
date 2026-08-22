# -*- coding: utf-8 -*-
"""Sinh testcase Excel cho man "Phieu xu ly yeu cau" tren CONG ERP (TanPhatDev)."""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ENGINE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "..", "..", "hrm", ".claude", "skills",
                          "testcase-documenter", "assets")
sys.path.insert(0, os.path.abspath(ENGINE_DIR))
from tc_engine import build  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(HERE, "testcase.xlsx")
MODULE = "Phiếu xử lý yêu cầu (ERP)"

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Kiểm thử TOÀN BỘ chức năng “Phiếu xử lý yêu cầu” trên phần mềm ERP (CSKH → Kiểm tra bảo hành "
     "sửa chữa → Phiếu xử lý yêu cầu).\n"
     " ► Đây là chứng từ THỨ HAI của luồng dịch vụ. Phiếu LUÔN sinh ra từ một Phiếu yêu cầu kiểm "
     "tra sửa chữa – bảo hành đang ở trạng thái “Chờ xử lý”: mở phiếu yêu cầu rồi bấm “Tạo phiếu xử "
     "lý yêu cầu”. Màn danh sách KHÔNG có nút thêm mới.\n"
     " ► Có 2 lối vào từ menu, cùng một giao diện nhưng khác phạm vi dữ liệu: lối “của tôi” chỉ "
     "hiện phiếu do chính mình lập; lối “tất cả” hiện theo phạm vi quyền.\n"
     " ► Phạm vi kiểm thử: danh sách, bộ lọc từng cột, lọc thời gian, lọc theo công ty/phòng ban, "
     "lập phiếu, sửa, xem, Lưu, Lưu & Gửi duyệt, Không duyệt, Thêm nhanh nguyên nhân, chọn hàng hóa "
     "tương đương, Xóa, In phiếu, In danh sách, Xuất Excel, phân quyền, ràng buộc nhập liệu."),

    ("2. Đối tượng được tính / hiển thị",
     "► 6 trạng thái: “Đang tạo” · “Chờ CCTT” · “Đã CCTT” · “Chờ CCTT bổ sung” · “Đang CCTT” · "
     "“Đã tư vấn điện thoại”.\n"
     " ► Bảng danh sách 11 cột: STT | Số phiếu xử lí | Số phiếu yêu cầu | Khách hàng | Tên thiết bị "
     "liên quan | Người yêu cầu | Ngày nhận yêu cầu | Người xử lý | Ngày xử lý | Trạng thái | Hành động.\n"
     " ► Mỗi dòng thiết bị chọn được NHIỀU nguyên nhân (công việc / lỗi thiết bị) và MỘT hành động: "
     "“Tư vấn điện thoại” hoặc “Cung cấp thông tin làm báo giá”.\n"
     " ► Danh sách nguyên nhân của mỗi dòng chỉ gồm những lỗi đã khai cho ĐÚNG hàng hóa của dòng đó."),

    ("3. Đối tượng bị ẩn / không tính",
     "► Ở lối vào “tất cả”, phiếu “Đang tạo” của NGƯỜI KHÁC không hiện trong danh sách.\n"
     " ⚠️ Nhưng mở bằng đường dẫn trực tiếp thì tài khoản quản trị cấp cao VẪN đọc được phiếu nháp "
     "của người khác — ghi nhận hiện trạng để đối chiếu, đây là điểm hệ thống mới làm chặt hơn.\n"
     " ► Phiếu ngoài phạm vi quyền không hiện.\n"
     " ► Trong menu bánh răng, mục không đủ điều kiện thì không xuất hiện: phiếu đã gửi mất Sửa/Xóa; "
     "phiếu không ở “Chờ CCTT” mất mục Tạo phiếu cung cấp thông tin."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "► Ô chọn khoảng thời gian trên thanh lọc áp dụng cho NGÀY LẬP phiếu xử lý, tính trọn ngày ở "
     "cả hai đầu.\n ► Không lọc theo Ngày nhận yêu cầu hay Ngày xử lý.\n"
     " ► Để trống thì lấy toàn bộ."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "► Mỗi phiếu xử lý gắn với đúng 1 phiếu yêu cầu và 1 khách hàng; thông tin khách hàng và danh "
     "sách thiết bị chép từ phiếu yêu cầu, để chế độ chỉ đọc.\n"
     " ► Mỗi dòng thiết bị: tên hàng hóa, thương hiệu, model, serial, số biên bản, nội dung yêu cầu "
     "+ nguyên nhân, hành động, nội dung xử lý, tệp đính kèm.\n"
     " ► Thiết bị người dùng tự gõ (chưa gắn hàng hóa danh mục) bắt buộc chọn HÀNG HÓA TƯƠNG ĐƯƠNG.\n"
     " ► Phiếu xử lý → Phiếu cung cấp thông tin làm báo giá → báo giá → hợp đồng."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "► Cột “Tên thiết bị liên quan” gom tên các thiết bị của phiếu, mỗi tên một dòng.\n"
     " ► Bộ lọc “Tên, mã hàng hóa” và “Model” trả về phiếu nào có ít nhất một dòng khớp.\n"
     " ► Khi lưu, toàn bộ dòng thiết bị và nguyên nhân được ghi đè bằng dữ liệu đang có trên màn hình."),

    ("7. Phân quyền cấp",
     "Màn hình dùng 4 quyền:\n"
     " ► “Xem phiếu xử lý yêu cầu đi kiểm tra sửa chữa - bảo hành theo tổng công ty”\n"
     " ► “Xem phiếu xử lý yêu cầu đi kiểm tra sửa chữa - bảo hành theo công ty”\n"
     " ► “Xem phiếu xử lý yêu cầu đi kiểm tra sửa chữa - bảo hành theo phòng ban” — gồm phòng được "
     "giao quản lý VÀ phòng đang công tác\n"
     " ► “Tạo phiếu cung cấp thông tin” — để lập chứng từ tiếp theo và để “Không duyệt”\n"
     " ► Không có quyền xem nào thì chỉ thấy phiếu do chính mình lập."),

    ("8. Cách tính các ô thống kê",
     "► Dòng “Hiển thị x đến y trong tổng số N mục” dưới bảng: N là tổng phiếu khớp bộ lọc.\n"
     " ► In danh sách và Xuất Excel chạy theo ĐÚNG bộ lọc đang áp dụng, lấy toàn bộ kết quả chứ "
     "không chỉ trang đang xem.\n"
     " ► Đổi số dòng mỗi trang thì bảng tải lại từ trang 1."),

    ("9. Ghi chú đọc bảng",
     "⚠️ Các bẫy dễ sai nhất trên cổng ERP:\n"
     " ► **Chọn “Tư vấn điện thoại” cho TẤT CẢ thiết bị thì phiếu tự thành “Đã tư vấn điện thoại”, "
     "dù bấm nút “Lưu”.** Hành vi đúng, không phải lỗi.\n"
     " ► Nút “Lưu” và “Lưu & Gửi duyệt” dùng CHUNG một bộ ràng buộc: cả hai đều bắt nhập đủ nguyên "
     "nhân và hành động. Bấm “Lưu” không phải lưu nháp tự do.\n"
     " ► Nút “Không duyệt” CHỈ có ở màn xem chi tiết, ngoài danh sách không có.\n"
     " ► Khi Không duyệt, hệ thống KHÔNG gửi thông báo cho người lập — họ phải tự vào xem.\n"
     " ► “Không duyệt” KHÔNG trả phiếu yêu cầu gốc về “Chờ xử lý”; chỉ XÓA phiếu xử lý mới trả về.\n"
     " ► Ô Nguyên nhân chỉ hiện lỗi của đúng hàng hóa dòng đó; chưa có thì dùng “Thêm nhanh”."),
]

ROLE_TCS = [
    ("00", "Không có quyền xem nào thì chỉ thấy phiếu của mình", "P0",
     "Tài khoản A không có quyền xem nào của màn này, đã lập 2 phiếu; công ty của A có nhiều phiếu "
     "của người khác.",
     "1. Đăng nhập bằng A\n2. Vào menu Phiếu xử lý yêu cầu (lối “tất cả”)\n3. Đọc tổng số mục",
     "—",
     "- Chỉ hiện 2 phiếu của A"),

    ("01", "Quyền xem theo tổng công ty", "P0",
     "Tài khoản B chỉ có quyền xem theo tổng công ty; có phiếu của ít nhất 2 công ty.",
     "1. Đăng nhập bằng B\n2. Mở lối vào “tất cả”\n3. Lọc lần lượt từng công ty trên thanh lọc",
     "—",
     "- Thấy phiếu của cả 2 công ty\n- ⚠️ Vẫn không thấy phiếu “Đang tạo” của người khác"),

    ("02", "Quyền xem theo công ty", "P0",
     "Tài khoản C chỉ có quyền xem theo công ty, thuộc công ty 1.",
     "1. Đăng nhập bằng C\n2. Mở lối vào “tất cả”, đếm số phiếu",
     "—",
     "- Chỉ thấy phiếu của công ty 1 (cộng phiếu nháp của chính C)"),

    ("03", "Quyền xem theo phòng ban gồm cả phòng đang công tác", "P0",
     "Tài khoản D chỉ có quyền xem theo phòng ban, quản lý phòng Kinh doanh 1 và đang công tác tại "
     "phòng Kỹ thuật.",
     "1. Đăng nhập bằng D\n2. Mở lối vào “tất cả”",
     "—",
     "- Thấy phiếu của CẢ hai phòng\n- ⚠️ Khác màn Phiếu yêu cầu: màn đó không cộng phòng đang công tác"),

    ("04", "Quyền tạo phiếu cung cấp thông tin", "P0",
     "Tài khoản E có quyền “Tạo phiếu cung cấp thông tin”. Có phiếu “Chờ CCTT”.",
     "1. Đăng nhập bằng E\n2. Mở menu bánh răng của phiếu đó\n3. Mở tiếp màn xem chi tiết",
     "—",
     "- Menu có mục Tạo phiếu cung cấp thông tin và In\n- Màn chi tiết có thêm nút Không duyệt"),

    ("05", "Không có quyền tạo phiếu cung cấp thông tin", "P0",
     "Tài khoản C không có quyền đó. Có phiếu “Chờ CCTT”.",
     "1. Đăng nhập bằng C\n2. Mở menu bánh răng và màn xem chi tiết của phiếu",
     "—",
     "- Menu chỉ có In\n- Màn chi tiết không có nút Không duyệt và Tạo phiếu cung cấp thông tin"),

    ("06", "Chặn Không duyệt khi gọi thẳng chức năng", "P0",
     "Tài khoản C không có quyền “Tạo phiếu cung cấp thông tin”. Phiếu đang “Chờ CCTT”.",
     "1. Đăng nhập bằng C\n2. Dùng công cụ kiểm thử API gọi thẳng chức năng Không duyệt\n"
     "3. Mở lại phiếu",
     "Lý do: “test”",
     "- Thao tác bị từ chối\n- Phiếu giữ nguyên “Chờ CCTT”\n- (Nhóm test dành cho tester kỹ thuật)"),

    ("07", "Chặn Xóa phiếu đã gửi khi gọi thẳng chức năng", "P0",
     "Phiếu do chính người đăng nhập lập, đang “Chờ CCTT”.",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa phiếu đó\n2. Mở lại danh sách",
     "—",
     "- Phiếu vẫn còn nguyên cùng các dòng thiết bị"),

    ("08", "Ghi nhận: quản trị cấp cao đọc được phiếu nháp của người khác", "P1",
     "Phiếu nháp do nhân viên G lập. Đăng nhập bằng tài khoản quản trị cấp cao.",
     "1. Lấy đường dẫn màn xem chi tiết của phiếu nháp đó\n2. Dán thẳng vào trình duyệt",
     "—",
     "- ⚠️ ERP CHO PHÉP xem (trong khi danh sách lại ẩn phiếu đó)\n"
     "- Ghi nhận hiện trạng để đối chiếu: hệ thống mới đã chặn trường hợp này"),
]

SEC_I = [
    ("001", "Vào màn hình từ 2 lối menu khác nhau", "P0",
     "Người đăng nhập đã lập vài phiếu; đồng nghiệp cũng có phiếu đã gửi.",
     "1. Vào menu Phiếu xử lý yêu cầu (lối “của tôi”), đếm số phiếu\n"
     "2. Vào menu Phiếu xử lý yêu cầu ở nhóm CSKH (lối “tất cả”), đếm lại",
     "—",
     "- Lối “của tôi” chỉ có phiếu do mình lập\n- Lối “tất cả” nhiều hơn, gồm phiếu đã gửi của "
     "người khác trong phạm vi quyền\n- ⚠️ Phải kiểm đúng lối vào khi đối chiếu số liệu"),

    ("002", "Bảng danh sách đủ 11 cột", "P0",
     "Danh sách có dữ liệu.",
     "1. Mở màn hình, đọc tiêu đề các cột",
     "—",
     "- Đủ 11 cột từ STT đến Hành động, đúng thứ tự nêu ở mục 2"),

    ("003", "Nhãn trạng thái hiển thị đúng", "P0",
     "Có phiếu ở nhiều trạng thái.",
     "1. Đối chiếu cột Trạng thái",
     "—",
     "- Hiện đúng chữ tiếng Việt của 6 trạng thái, có nền màu phân biệt"),

    ("004", "Menu hành động theo trạng thái", "P0",
     "Phiếu P1 “Đang tạo” do mình lập; P2 “Chờ CCTT” (có quyền tạo phiếu CCTT); P3 “Đã CCTT”.",
     "1. Mở menu bánh răng của P1, P2, P3",
     "—",
     "- P1: Sửa, Xóa, In\n- P2: Tạo phiếu cung cấp thông tin, In\n- P3: chỉ In\n"
     "- ⚠️ Mục không đủ điều kiện phải biến mất, không hiện mờ"),

    ("005", "Nút Không duyệt chỉ có ở màn xem chi tiết", "P1",
     "Phiếu “Chờ CCTT”, người đăng nhập có quyền tạo phiếu CCTT.",
     "1. Xem menu bánh răng ngoài danh sách\n2. Mở màn xem chi tiết",
     "—",
     "- Ngoài danh sách KHÔNG có mục Không duyệt\n- Màn chi tiết CÓ nút Không duyệt\n"
     "- ⚠️ Ghi nhận để đối chiếu: hệ thống mới để nút này ở cả 2 nơi"),
]

SEC_II = [
    ("001", "Lọc theo Mã phiếu", "P0",
     "Biết số phiếu xử lý đầy đủ.",
     "1. Gõ mã phiếu vào ô lọc dưới tiêu đề cột Số phiếu xử lí\n2. Chờ bảng tải lại",
     "Số phiếu xử lý",
     "- Ra đúng 1 phiếu"),

    ("002", "Lọc theo Phiếu yêu cầu", "P0",
     "Biết số phiếu yêu cầu tương ứng.",
     "1. Gõ số phiếu yêu cầu vào ô lọc cột Số phiếu yêu cầu",
     "Số phiếu yêu cầu",
     "- Ra phiếu xử lý của phiếu yêu cầu đó"),

    ("003", "Lọc theo Trạng thái", "P0",
     "Có phiếu ở nhiều trạng thái.",
     "1. Chọn “Chờ CCTT” ở ô lọc cột Trạng thái",
     "Trạng thái: Chờ CCTT",
     "- Mọi dòng đều là “Chờ CCTT”"),

    ("004", "Lọc theo Tên, mã hàng hóa và Model", "P0",
     "Có phiếu chứa thiết bị tên “Bệ kiểm tra”, model “SL-580”.",
     "1. Gõ “Bệ kiểm tra” vào ô lọc Tên thiết bị liên quan\n2. Xóa đi, gõ “SL-580” vào ô lọc Model",
     "Bệ kiểm tra · SL-580",
     "- Mỗi lần chỉ còn phiếu có thiết bị khớp\n- ⚠️ Mở vài phiếu trong kết quả để đối chiếu"),

    ("005", "Lọc theo Khách hàng", "P0",
     "Khách hàng Z có nhiều phiếu.",
     "1. Ở ô lọc cột Khách hàng, gõ tên rồi chọn Z từ danh sách gợi ý",
     "Khách hàng: Z",
     "- Chỉ còn phiếu của khách Z\n- ⚠️ Phải chọn từ danh sách gợi ý, không chỉ gõ chữ"),

    ("006", "Lọc theo khoảng thời gian", "P0",
     "Có phiếu lập hôm nay và ngày khác.",
     "1. Mở ô chọn khoảng thời gian, chọn từ hôm nay đến hôm nay",
     "Cùng một ngày",
     "- Chỉ còn phiếu lập trong ngày đó"),

    ("007", "Lọc theo công ty và phòng ban", "P1",
     "Người đăng nhập có quyền xem tổng công ty, đang ở lối vào “tất cả”.",
     "1. Chọn công ty rồi chọn phòng ban trên thanh lọc",
     "—",
     "- Tổng số mục giảm dần đúng theo từng lần chọn\n"
     "- ⚠️ Khối lọc công ty/phòng ban chỉ hiện ở lối vào “tất cả”"),

    ("008", "Kết hợp nhiều điều kiện", "P0",
     "Có phiếu “Chờ CCTT” của khách Z trong tháng.",
     "1. Lọc trạng thái + khách hàng + khoảng thời gian",
     "—",
     "- Kết quả thỏa mãn đồng thời cả 3 điều kiện"),

    ("009", "Lọc không ra kết quả", "P1",
     "Không có phiếu nào khớp.",
     "1. Gõ “KHONG-TON-TAI-XYZ” vào ô lọc Mã phiếu",
     "KHONG-TON-TAI-XYZ",
     "- Bảng hiện thông báo không có dữ liệu, không treo trang"),
]

SEC_III = [
    ("001", "Sắp xếp theo cột cho phép", "P1",
     "Danh sách trên 20 phiếu.",
     "1. Bấm tiêu đề cột Số phiếu xử lí\n2. Bấm lần nữa\n3. Bấm tiêu đề cột Ngày xử lý",
     "—",
     "- Thứ tự đổi đúng chiều\n- ⚠️ Nhiều cột khác không sắp xếp được — thiết kế hiện tại"),

    ("002", "Chuyển trang và đổi số dòng", "P0",
     "Bộ lọc ra trên 100 phiếu.",
     "1. Sang trang 2\n2. Đổi số dòng mỗi trang\n3. Về trang 1",
     "—",
     "- Dòng thống kê cập nhật đúng, không dòng nào lặp\n- Đổi số dòng thì bảng tải lại từ trang 1"),

    ("003", "Giữ bộ lọc khi chuyển trang", "P1",
     "Đang lọc trạng thái, kết quả trên 2 trang.",
     "1. Sang trang 2, kiểm tra cột Trạng thái",
     "—",
     "- Bộ lọc không bị mất"),
]

SEC_IV = [
    ("001", "Lập phiếu xử lý từ phiếu yêu cầu", "P0",
     "Phiếu yêu cầu Y đang “Chờ xử lý”, gửi về phòng của người đăng nhập, chưa có phiếu xử lý.",
     "1. Mở màn Yêu cầu kiểm tra sửa chữa - bảo hành\n2. Ở menu bánh răng của Y, bấm “Tạo phiếu xử "
     "lý yêu cầu”",
     "—",
     "- Mở màn lập phiếu, khối trên điền sẵn và khóa: Phiếu yêu cầu, Người yêu cầu, Phòng yêu cầu, "
     "Ngày nhận yêu cầu, Khách hàng, Người liên hệ, SĐT, Địa chỉ sửa chữa\n"
     "- Bảng thiết bị chép đủ dòng của phiếu yêu cầu"),

    ("002", "Không lập được phiếu khi không đủ điều kiện", "P0",
     "Phiếu yêu cầu đã có phiếu xử lý, hoặc không thuộc phòng tiếp nhận của người đăng nhập.",
     "1. Gõ thẳng đường dẫn màn lập phiếu kèm mã phiếu yêu cầu đó",
     "—",
     "- Hệ thống báo không tìm thấy trang / không cho lập"),

    ("003", "Chọn nguyên nhân cho từng thiết bị", "P0",
     "Hàng hóa của dòng đã khai lỗi trong danh mục.",
     "1. Mở ô Nguyên nhân của dòng thiết bị\n2. Chọn 2 nguyên nhân",
     "—",
     "- Ô cho chọn nhiều nguyên nhân\n- ⚠️ Chỉ liệt kê lỗi đã khai cho ĐÚNG hàng hóa của dòng đó"),

    ("004", "Thêm nhanh nguyên nhân", "P0",
     "Đang ở màn lập/sửa phiếu.",
     "1. Bấm “Thêm nhanh” dưới ô Nguyên nhân\n2. Khai Loại công việc / lỗi, Tên, Định mức công\n"
     "3. Lưu",
     "Loại: Lỗi đã xác định — Tên: “Bục ống dẫn khí nén”",
     "- Popup có các ô: Loại, Tên, Định mức công, Hệ số giá bán dịch vụ, Định mức đàm phán giá, "
     "VAT, Công kỹ thuật, Đơn giá công kỹ thuật, Đơn giá bán, Hệ số công nghệ, Ghi chú, kèm bảng "
     "Thiết bị và bảng Dịch vụ sửa chữa\n- Lưu xong lỗi mới có trong ô Nguyên nhân của dòng và "
     "được tự chọn"),

    ("005", "Chọn hành động", "P0",
     "Đã chọn nguyên nhân.",
     "1. Mở ô Hành động\n2. Chọn “Tư vấn điện thoại”\n3. Bấm “Thêm nội dung xử lý”",
     "—",
     "- Ô Hành động có 2 lựa chọn: Tư vấn điện thoại · Cung cấp thông tin làm báo giá\n"
     "- Chọn “Tư vấn điện thoại” mới hiện nút thêm nội dung xử lý"),

    ("006", "Chọn hàng hóa tương đương cho thiết bị tự gõ", "P0",
     "Phiếu yêu cầu có dòng thiết bị người dùng tự gõ.",
     "1. Ở dòng đó, bấm biểu tượng bút chì cạnh tên thiết bị\n2. Tìm và chọn một hàng hóa",
     "—",
     "- Popup tìm hàng hóa mở ra\n- Chọn xong dòng thiết bị gắn được mã hàng, danh sách nguyên "
     "nhân nạp theo hàng hóa mới"),

    ("007", "Nhập số biên bản bàn giao / xác nhận công việc", "P2",
     "Dòng thiết bị chưa có số biên bản.",
     "1. Nhập số biên bản vào ô tương ứng\n2. Lưu và mở lại phiếu",
     "Số BBBGNT: “BB-001”",
     "- Giá trị được lưu và hiện lại đúng"),

    ("008", "Sửa phiếu ở trạng thái Đang tạo", "P0",
     "Phiếu “Đang tạo” do chính người đăng nhập lập.",
     "1. Mở menu bánh răng, bấm Sửa\n2. Đổi nguyên nhân\n3. Bấm Lưu\n4. Mở lại phiếu",
     "—",
     "- Lưu thành công, mở lại thấy nguyên nhân mới\n- Mã phiếu không đổi"),

    ("009", "Màn xem chi tiết ở chế độ chỉ đọc", "P1",
     "Phiếu bất kỳ.",
     "1. Mở màn xem chi tiết, thử gõ vào các ô",
     "—",
     "- Mọi ô khóa\n- Không có nút Lưu / Lưu & Gửi duyệt"),
]

SEC_V = [
    ("001", "Gửi phiếu đi để cung cấp thông tin", "P0",
     "Phiếu đã chọn nguyên nhân và hành động “Cung cấp thông tin làm báo giá”.",
     "1. Bấm “Lưu & Gửi duyệt”\n2. Đăng nhập bằng người có quyền “Tạo phiếu cung cấp thông tin” "
     "cùng công ty, mở phần thông báo",
     "—",
     "- Phiếu chuyển “Chờ CCTT”\n- Phiếu yêu cầu GỐC chuyển “Đã xử lý”, điền Người xử lý / Ngày xử lý\n"
     "- Người có quyền đó nhận được thông báo\n- ⚠️ Thông báo đi theo QUYỀN, không theo phòng ban"),

    ("002", "Mọi thiết bị đều Tư vấn điện thoại", "P0",
     "Phiếu có 1 thiết bị, chọn “Tư vấn điện thoại” và đã nhập nội dung xử lý.",
     "1. Bấm nút “Lưu” (KHÔNG bấm Lưu & Gửi duyệt)\n2. Kiểm tra trạng thái phiếu và phiếu yêu cầu gốc",
     "—",
     "- ⚠️ Phiếu vẫn thành “Đã tư vấn điện thoại” dù bấm Lưu\n"
     "- Phiếu yêu cầu gốc cũng thành “Đã tư vấn điện thoại”, luồng kết thúc"),

    ("003", "Phiếu nhiều thiết bị, một dòng cần báo giá", "P0",
     "Phiếu 2 thiết bị: dòng 1 Tư vấn điện thoại, dòng 2 Cung cấp thông tin làm báo giá.",
     "1. Bấm Lưu & Gửi duyệt",
     "—",
     "- Phiếu chuyển “Chờ CCTT”, không phải “Đã tư vấn điện thoại”"),

    ("004", "Không duyệt phiếu", "P0",
     "Phiếu “Chờ CCTT”, người đăng nhập có quyền tạo phiếu CCTT. Phiếu do nhân viên G lập.",
     "1. Mở màn xem chi tiết phiếu\n2. Nhập lý do vào ô ghi chú\n3. Bấm “Không duyệt”\n"
     "4. Đăng nhập bằng G, mở phần thông báo và mở phiếu",
     "Lý do: “Thiếu thông tin báo giá”",
     "- Phiếu trở lại “Đang tạo”, lý do lưu trên phiếu\n"
     "- ⚠️ G KHÔNG nhận được thông báo nào — hành vi hiện tại của ERP"),

    ("005", "Không duyệt mà bỏ trống lý do", "P0",
     "Màn xem chi tiết phiếu “Chờ CCTT”, ô lý do trống.",
     "1. Bấm “Không duyệt”",
     "—",
     "- Hệ thống báo bắt buộc nhập lý do\n- Phiếu chưa đổi trạng thái"),

    ("006", "Không duyệt KHÔNG trả phiếu yêu cầu gốc về Chờ xử lý", "P0",
     "Phiếu xử lý “Chờ CCTT”, phiếu yêu cầu gốc “Đã xử lý”.",
     "1. Không duyệt phiếu xử lý\n2. Mở màn Yêu cầu kiểm tra sửa chữa - bảo hành, tìm phiếu gốc",
     "Lý do: “test”",
     "- Phiếu xử lý về “Đang tạo”\n- ⚠️ Phiếu yêu cầu gốc VẪN “Đã xử lý”"),

    ("007", "Tạo phiếu cung cấp thông tin", "P0",
     "Phiếu “Chờ CCTT”, người đăng nhập có quyền tương ứng.",
     "1. Bấm “Tạo phiếu cung cấp thông tin”\n2. Hoàn tất phiếu bên màn tương ứng\n3. Quay lại danh sách",
     "—",
     "- Mở màn lập Phiếu cung cấp thông tin với dữ liệu lấy sẵn\n- Sau khi lập xong, phiếu xử lý "
     "chuyển sang trạng thái tiếp theo của luồng"),
]

SEC_VI = [
    ("001", "Xóa phiếu Đang tạo và trả phiếu yêu cầu về Chờ xử lý", "P0",
     "Phiếu xử lý “Đang tạo” do chính mình lập; phiếu yêu cầu gốc “Đã xử lý”.",
     "1. Mở menu bánh răng, bấm Xóa\n2. Xác nhận\n3. Mở màn Yêu cầu kiểm tra sửa chữa - bảo hành, "
     "tìm phiếu gốc",
     "—",
     "- Cửa sổ hỏi “Xác nhận xóa!”\n- Phiếu xử lý biến mất\n"
     "- ⚠️ Phiếu yêu cầu gốc TRỞ LẠI “Chờ xử lý”, xóa Người xử lý / Ngày xử lý"),

    ("002", "Hủy ở cửa sổ xác nhận xóa", "P1",
     "Phiếu nháp của chính mình.",
     "1. Bấm Xóa\n2. Bấm Hủy",
     "—",
     "- Phiếu vẫn còn, phiếu yêu cầu gốc không đổi"),

    ("003", "Không có mục Xóa với phiếu đã gửi", "P0",
     "Phiếu “Chờ CCTT” do chính mình lập.",
     "1. Mở menu bánh răng",
     "—",
     "- Không có mục Sửa và Xóa"),
]

SEC_VII = [
    ("001", "Xuất Excel theo bộ lọc", "P0",
     "Đang lọc trạng thái “Chờ CCTT”.",
     "1. Bấm nút xuất Excel\n2. Mở tệp",
     "—",
     "- Số dòng trong tệp bằng đúng tổng số mục đang lọc\n- ⚠️ Không dừng ở trang đang xem"),

    ("002", "In danh sách theo bộ lọc", "P0",
     "Đang lọc một trạng thái.",
     "1. Bấm nút in danh sách\n2. Xem tab mới",
     "—",
     "- Mở tab mới với mẫu danh sách khổ ngang, có khung tờ giấy\n- Bảng chứa đúng các phiếu đang lọc"),

    ("003", "In một phiếu", "P0",
     "Phiếu đã điền đủ nguyên nhân và hành động.",
     "1. Mở menu bánh răng, bấm In\n2. Xem tab mới\n3. Bấm nút In trên trang xem trước",
     "—",
     "- Mẫu phiếu khổ dọc trên khung tờ giấy\n- Bảng chi tiết có cột Nguyên nhân và Hành động\n"
     "- Không còn chỗ nào bỏ trống dạng ký hiệu chờ điền"),
]

SEC_VIII = [
    ("001", "Bấm Lưu khi thiếu Nguyên nhân / Hành động", "P0",
     "Phiếu có 1 thiết bị, chưa chọn gì.",
     "1. Bấm nút Lưu",
     "—",
     "- Không lưu được, báo lỗi đỏ dưới ô Nguyên nhân và ô Hành động\n"
     "- ⚠️ Nút “Lưu” cũng bắt buộc đủ như “Lưu & Gửi duyệt”"),

    ("002", "Tư vấn điện thoại thiếu nội dung xử lý", "P0",
     "Đã chọn nguyên nhân và hành động “Tư vấn điện thoại”, chưa nhập nội dung.",
     "1. Bấm Lưu",
     "—",
     "- Chặn, báo lỗi tại đúng dòng"),

    ("003", "Chọn trùng nguyên nhân cho cùng thiết bị", "P0",
     "Phiếu có 2 dòng cùng hàng hóa, cùng serial.",
     "1. Chọn cho 2 dòng ít nhất một nguyên nhân giống nhau\n2. Bấm Lưu",
     "—",
     "- Chặn, báo bị trùng ở cả hai dòng"),

    ("004", "Thiết bị tự gõ chưa chọn hàng hóa tương đương", "P0",
     "Phiếu có dòng thiết bị tự gõ, chưa gắn hàng hóa.",
     "1. Chọn nguyên nhân + hành động cho dòng đó\n2. Bấm Lưu",
     "—",
     "- Chặn, báo phải chọn hàng hóa tương đương"),

    ("005", "Lưu khi không có thiết bị nào", "P0",
     "Phiếu không có dòng thiết bị.",
     "1. Bấm Lưu",
     "—",
     "- Chặn, báo yêu cầu phải có ít nhất 1 thiết bị"),
]

SEC_IX = [
    ("001", "Hai người cùng xử lý một phiếu", "P1",
     "Phiếu “Chờ CCTT”, hai người cùng có quyền và cùng mở phiếu.",
     "1. Người thứ nhất bấm Không duyệt\n2. Người thứ hai (chưa tải lại) cũng bấm Không duyệt",
     "—",
     "- Thao tác thứ hai không được thực hiện hoặc báo trạng thái đã thay đổi\n- Không treo trang"),

    ("002", "Dữ liệu lập bên cổng mới hiện ngay bên ERP", "P0",
     "Có tài khoản dùng được cả 2 cổng.",
     "1. Lập 1 phiếu xử lý bên cổng mới\n2. Sang ERP, lọc theo mã phiếu vừa lập",
     "Mã phiếu vừa lập",
     "- Tìm thấy đúng phiếu, mở ra thấy đủ nguyên nhân và hành động"),
]

SEC_X = [
    ("001", "Luồng đầy đủ: lập → gửi → không duyệt → gửi lại → xóa", "P0",
     "Phiếu yêu cầu Y đang “Chờ xử lý”; G thuộc phòng tiếp nhận; E có quyền tạo phiếu CCTT.",
     "1. G lập phiếu xử lý từ Y, chọn nguyên nhân + hành động Cung cấp thông tin, Lưu & Gửi duyệt\n"
     "2. E mở phiếu, nhập lý do, bấm Không duyệt\n3. G sửa phiếu và gửi lại\n"
     "4. E không duyệt lần nữa, G xóa phiếu\n5. Tìm lại phiếu Y",
     "Lý do: “Thiếu thông tin báo giá”",
     "- Bước 1: phiếu “Chờ CCTT”, Y thành “Đã xử lý”\n"
     "- Bước 2: phiếu về “Đang tạo”, Y VẪN “Đã xử lý”, G không có thông báo\n"
     "- Bước 3: phiếu lại “Chờ CCTT”, mã phiếu không đổi\n"
     "- Bước 4-5: xóa xong Y TRỞ LẠI “Chờ xử lý”"),

    ("002", "Luồng kết thúc bằng tư vấn điện thoại", "P0",
     "Phiếu yêu cầu Z đang “Chờ xử lý”, có 1 thiết bị.",
     "1. Lập phiếu xử lý từ Z, chọn Tư vấn điện thoại + nội dung xử lý\n2. Bấm Lưu\n3. Kiểm tra 2 phiếu",
     "—",
     "- Cả phiếu xử lý và phiếu Z đều “Đã tư vấn điện thoại”\n- Luồng dịch vụ kết thúc"),
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
    ("X", "LUỒNG NGHIỆP VỤ ĐẦU – CUỐI", SEC_X),
]

build(output_file=OUTPUT_FILE,
      sheet_name="Trang tính1",
      feature_name="Phiếu xử lý yêu cầu (cổng ERP) - Cập nhật ngày 21/08/2026",
      module_name=MODULE,
      description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS,
      sections=SECTIONS)
