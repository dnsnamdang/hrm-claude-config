# -*- coding: utf-8 -*-
"""Sinh testcase Excel cho man "Yeu cau kiem tra sua chua - bao hanh" tren CONG ERP (TanPhatDev)."""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Engine dung chung nam trong bo skill cua HRM (cung repo cau hinh hrm-claude-config).
ENGINE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "..", "..", "hrm", ".claude", "skills",
                          "testcase-documenter", "assets")
sys.path.insert(0, os.path.abspath(ENGINE_DIR))
from tc_engine import build  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(HERE, "testcase.xlsx")
MODULE = "YC sửa chữa - bảo hành (ERP)"

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Kiểm thử TOÀN BỘ chức năng “Yêu cầu kiểm tra sửa chữa – bảo hành” trên phần mềm ERP.\n"
     " ► Có 2 lối vào từ thanh menu, cùng một màn hình danh sách nhưng khác phạm vi dữ liệu:\n"
     "   • “Yêu cầu kiểm tra sửa chữa - bảo hành” → chỉ hiện phiếu do CHÍNH MÌNH lập.\n"
     "   • “Phiếu yêu cầu kiểm tra sửa chữa - bảo hành” (nhóm CSKH) → hiện phiếu theo phạm vi "
     "quyền, gồm cả phiếu gửi về phòng tiếp nhận của mình.\n"
     " ► Phạm vi kiểm thử: danh sách, bộ lọc từng cột, lọc thời gian, lọc theo công ty/phòng ban, "
     "Thêm mới, Sửa, Xem, Lưu, Lưu & Gửi duyệt, Chuyển phòng tiếp nhận, Không duyệt, Tạo phiếu xử "
     "lý yêu cầu, Xóa, In phiếu, In danh sách, Xuất Excel, thêm trang thiết bị cho khách hàng, "
     "phân quyền và ràng buộc nhập liệu.\n"
     " ► Đây là chứng từ mở đầu luồng dịch vụ: từ phiếu này phòng tiếp nhận lập Phiếu xử lý yêu "
     "cầu, rồi mới tới các chứng từ phía sau."),

    ("2. Đối tượng được tính / hiển thị",
     "► Lối vào “của tôi”: chỉ phiếu do người đăng nhập lập, mọi trạng thái.\n"
     " ► Lối vào “tất cả”: phiếu theo phạm vi quyền (xem mục 7), cộng phiếu gửi về phòng tiếp nhận "
     "của người đăng nhập nếu người này có quyền xử lý.\n"
     " ► 9 trạng thái: “Đang tạo” · “Chờ xử lý” · “Đang xử lý” · “Đang CCTT” · “Đã CCTT báo giá” · "
     "“Đã báo giá” · “Đã lập hợp đồng” · “Đã xử lý” · “Đã tư vấn điện thoại”.\n"
     " ► Bảng danh sách có 11 cột: STT | Mã phiếu | Khách hàng | Tên thiết bị liên quan | Địa chỉ "
     "sửa chữa | Người yêu cầu | Ngày yêu cầu | Ngày xử lý | Người xử lý | Trạng thái | Hành động.\n"
     " ► Bảng “Danh mục trang thiết bị hiện có của khách hàng” trong form gom thiết bị từ 3 nguồn: "
     "hàng công ty đã bán, thiết bị cũ của khách và thiết bị mua từ nhà cung cấp khác."),

    ("3. Đối tượng bị ẩn / không tính",
     "► Ở lối vào “tất cả”, phiếu “Đang tạo” của NGƯỜI KHÁC không hiện với bất kỳ ai.\n"
     " ► Phiếu ngoài phạm vi quyền không hiện.\n"
     " ► Danh sách chọn khách hàng chỉ hiện khách đang hoạt động; tab khách hàng cá nhân để trống "
     "cho tới khi nhập số điện thoại.\n"
     " ► Trong menu bánh răng của mỗi dòng, mục nào không đủ điều kiện thì không xuất hiện: phiếu "
     "đã gửi đi không còn Sửa/Xóa; phiếu đã có Phiếu xử lý yêu cầu không còn Tạo phiếu xử lý yêu "
     "cầu và Chuyển phòng tiếp nhận."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "► Ô chọn khoảng thời gian trên thanh lọc áp dụng cho NGÀY YÊU CẦU (ngày lập phiếu), tính "
     "trọn ngày ở cả hai đầu.\n"
     " ► Không lọc theo Ngày xử lý — cột này chỉ để hiển thị, in và xuất file.\n"
     " ► Để trống thì lấy toàn bộ, không giới hạn khoảng thời gian tối đa."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "► Mỗi phiếu gắn 1 khách hàng và nhiều dòng thiết bị cần kiểm tra. Mỗi dòng gồm: tên thiết "
     "bị, thương hiệu, model, nhà cung cấp, serial, mô tả yêu cầu, tệp đính kèm.\n"
     " ► Serial nhập theo 2 cách: chọn trong danh sách serial hệ thống đang quản lý hoặc gõ tay "
     "serial mới. Cùng một serial của cùng loại thiết bị không được đưa vào phiếu 2 lần.\n"
     " ► Trong form còn có chức năng “Thêm trang thiết bị của khách hàng” để khai bổ sung thiết bị "
     "cho khách ngay tại chỗ, chia 2 loại: “Thiết bị Tân Phát CC” và “Thiết bị mua NCC khác”.\n"
     " ► Phiếu → Phiếu xử lý yêu cầu → các chứng từ dịch vụ phía sau. Trạng thái từ “Đang xử lý” "
     "trở đi do các chứng từ sau cập nhật ngược về."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "► Cột “Tên thiết bị liên quan” gom tên các thiết bị của phiếu, mỗi tên một dòng, tên trùng "
     "chỉ hiện một lần.\n"
     " ► Khi lưu, danh sách thiết bị trên màn hình thay thế toàn bộ danh sách cũ của phiếu.\n"
     " ► Bảng thiết bị của khách loại bỏ bớt những thiết bị đã được đưa hết số lượng vào phiếu."),

    ("7. Phân quyền cấp",
     "Màn hình dùng 4 quyền:\n"
     " ► “Xem yêu cầu đi kiểm tra sửa chữa - bảo hành theo tổng công ty” — thấy phiếu của mọi công ty.\n"
     " ► “Xem yêu cầu đi kiểm tra sửa chữa - bảo hành theo công ty” — thấy phiếu của công ty mình, "
     "cộng phiếu do chính mình lập.\n"
     " ► “Xem yêu cầu đi kiểm tra sửa chữa - bảo hành theo phòng ban” — thấy phiếu của các phòng "
     "mình quản lý, cộng phiếu do chính mình lập.\n"
     " ► “Xử lý yêu cầu sửa chữa” — quyền của phòng tiếp nhận: Tạo phiếu xử lý yêu cầu, Chuyển "
     "phòng tiếp nhận, Không duyệt; đồng thời thấy mọi phiếu gửi về phòng mình.\n"
     " ► Không có quyền xem nào thì chỉ thấy phiếu của chính mình.\n"
     " ► Người mang vai trò quản trị cấp cao thao tác được với phiếu của mọi phòng tiếp nhận."),

    ("8. Cách tính các ô thống kê",
     "► Dòng “Hiển thị x đến y trong tổng số N mục” dưới bảng: N là tổng phiếu khớp bộ lọc, không "
     "phải tổng toàn hệ thống.\n"
     " ► Ô chọn số dòng mỗi trang đổi được; đổi xong bảng tải lại từ trang 1.\n"
     " ► Nút In danh sách và Xuất Excel chạy theo ĐÚNG bộ lọc đang áp dụng, lấy toàn bộ kết quả "
     "chứ không chỉ trang đang xem.\n"
     " ► Bảng thiết bị của khách trong form hiển thị theo trang, dòng thống kê đếm trên tổng thiết "
     "bị của khách sau khi lọc."),

    ("9. Ghi chú đọc bảng",
     "⚠️ Các bẫy dễ sai nhất trên cổng ERP:\n"
     " ► Nút “Lưu” và nút “Lưu & Gửi duyệt” dùng CHUNG một bộ ràng buộc: cả hai đều bắt nhập đủ "
     "Khách hàng, Người liên hệ, Địa chỉ sửa chữa, Ghi chú, Phòng tiếp nhận xử lý, ít nhất 1 thiết "
     "bị và mô tả yêu cầu từng thiết bị. Bấm “Lưu” không phải là lưu nháp tự do.\n"
     " ► Hai lối vào menu khác nhau nhưng cùng giao diện — phải kiểm đúng lối vào khi đối chiếu số "
     "phiếu, dễ nhầm là lỗi phạm vi dữ liệu.\n"
     " ► Nút “Không duyệt” (từ chối) CHỈ có ở màn xem chi tiết, ngoài danh sách không có.\n"
     " ► Khi từ chối, hệ thống KHÔNG gửi thông báo cho người lập — người lập phải tự vào xem mới "
     "biết. Đây là hành vi hiện tại của ERP, không phải lỗi.\n"
     " ► Bấm nút xóa là hỏi xác nhận ngay, không có bước trung gian; xóa xong quay về đầu danh sách.\n"
     " ► Bộ lọc từng cột nằm ngay dưới dòng tiêu đề bảng, gõ xong phải chờ bảng tự tải lại."),
]

ROLE_TCS = [
    ("00", "Không có quyền xem nào thì chỉ thấy phiếu của chính mình", "P0",
     "Tài khoản A không được gán quyền xem nào của màn này. A đã lập 2 phiếu; công ty của A có 30 "
     "phiếu do người khác lập.",
     "1. Đăng nhập bằng A\n2. Vào menu “Phiếu yêu cầu kiểm tra sửa chữa - bảo hành”\n"
     "3. Đọc dòng tổng số mục dưới bảng",
     "—",
     "- Vào được màn hình, không bị chặn\n- Chỉ hiện đúng 2 phiếu của A\n- Không thấy 30 phiếu còn lại"),

    ("01", "Quyền xem theo tổng công ty thấy phiếu mọi công ty", "P0",
     "Tài khoản B chỉ có quyền “Xem yêu cầu đi kiểm tra sửa chữa - bảo hành theo tổng công ty”. Hệ "
     "thống có phiếu của ít nhất 2 công ty.",
     "1. Đăng nhập bằng B\n2. Mở lối vào “Phiếu yêu cầu kiểm tra sửa chữa - bảo hành”\n"
     "3. Dùng ô lọc công ty trên thanh lọc, chọn lần lượt từng công ty",
     "—",
     "- Thấy phiếu của cả 2 công ty\n- ⚠️ Vẫn không thấy phiếu “Đang tạo” của người khác"),

    ("02", "Quyền xem theo công ty", "P0",
     "Tài khoản C chỉ có quyền “Xem yêu cầu đi kiểm tra sửa chữa - bảo hành theo công ty”, thuộc "
     "công ty 1. Công ty 1 có 12 phiếu đã gửi, công ty 2 có 8 phiếu đã gửi; C từng lập 1 phiếu ở "
     "công ty 2.",
     "1. Đăng nhập bằng C\n2. Mở lối vào “Phiếu yêu cầu kiểm tra sửa chữa - bảo hành”\n3. Đếm số phiếu",
     "—",
     "- Thấy 12 phiếu công ty 1 và 1 phiếu do C lập ở công ty 2\n- Không thấy 7 phiếu còn lại"),

    ("03", "Quyền xem theo phòng ban", "P0",
     "Tài khoản D chỉ có quyền “Xem yêu cầu đi kiểm tra sửa chữa - bảo hành theo phòng ban”, quản "
     "lý phòng Kinh doanh 1 (6 phiếu). Phòng Kinh doanh 2 có 4 phiếu.",
     "1. Đăng nhập bằng D\n2. Mở lối vào “Phiếu yêu cầu kiểm tra sửa chữa - bảo hành”",
     "—",
     "- Thấy 6 phiếu phòng Kinh doanh 1 cộng phiếu do chính D lập\n- Không thấy phiếu phòng Kinh doanh 2"),

    ("04", "Quyền xử lý yêu cầu thấy phiếu gửi về phòng mình", "P0",
     "Tài khoản E chỉ có quyền “Xử lý yêu cầu sửa chữa”, công tác tại phòng Kỹ thuật. Có 3 phiếu "
     "“Chờ xử lý” gửi về phòng Kỹ thuật do người phòng khác lập.",
     "1. Đăng nhập bằng E\n2. Mở lối vào “Phiếu yêu cầu kiểm tra sửa chữa - bảo hành”\n"
     "3. Mở menu bánh răng của 1 phiếu",
     "—",
     "- Thấy đủ 3 phiếu\n- Menu có: Tạo phiếu xử lý yêu cầu, Chuyển phòng tiếp nhận, In"),

    ("05", "Không có quyền xử lý thì không có mục Chuyển phòng tiếp nhận", "P0",
     "Tài khoản C không có quyền “Xử lý yêu cầu sửa chữa”. Có phiếu “Chờ xử lý” gửi về phòng của C.",
     "1. Đăng nhập bằng C\n2. Mở menu bánh răng của phiếu đó\n3. Mở tiếp màn xem chi tiết phiếu",
     "—",
     "- Menu chỉ có mục In\n- Màn chi tiết không có nút Chuyển phòng tiếp nhận, Không duyệt, Tạo "
     "phiếu xử lý yêu cầu"),

    ("06", "Chặn Chuyển phòng tiếp nhận khi gọi thẳng chức năng, bỏ qua giao diện", "P0",
     "Tài khoản C không có quyền “Xử lý yêu cầu sửa chữa”. Phiếu đang “Chờ xử lý”, phòng tiếp nhận "
     "là Kỹ thuật.",
     "1. Đăng nhập bằng C\n2. Dùng công cụ kiểm thử gọi thẳng chức năng Chuyển phòng tiếp nhận "
     "sang phòng Bảo hành\n3. Mở lại phiếu",
     "Phòng tiếp nhận mới: Bảo hành",
     "- Hệ thống từ chối, báo không có quyền\n- Phòng tiếp nhận vẫn là Kỹ thuật\n"
     "- (Nhóm test này dành cho tester kỹ thuật)"),

    ("07", "Chặn Xóa phiếu đã gửi đi khi gọi thẳng chức năng", "P0",
     "Phiếu do chính người đăng nhập lập, đang “Chờ xử lý”.",
     "1. Dùng công cụ kiểm thử gọi thẳng chức năng Xóa phiếu đó\n2. Mở lại danh sách",
     "—",
     "- Phiếu vẫn còn nguyên trong danh sách cùng các dòng thiết bị\n- ⚠️ Chỉ phiếu “Đang tạo” mới "
     "xóa được"),
]

SEC_I = [
    ("001", "Vào màn hình từ lối vào “của tôi”", "P0",
     "Người đăng nhập đã lập 3 phiếu; đồng nghiệp cùng phòng lập 10 phiếu.",
     "1. Vào menu “Yêu cầu kiểm tra sửa chữa - bảo hành”\n2. Đọc tiêu đề trang và đếm số phiếu",
     "—",
     "- Tiêu đề: “Danh sách yêu cầu đi kiểm tra sửa chữa - bảo hành”\n- Chỉ hiện 3 phiếu của mình\n"
     "- Bảng có đủ 11 cột từ STT đến Hành động"),

    ("002", "Vào màn hình từ lối vào “tất cả”", "P0",
     "Cùng tài khoản trên, có quyền xem theo công ty.",
     "1. Vào menu “Phiếu yêu cầu kiểm tra sửa chữa - bảo hành” (nhóm CSKH)\n2. Đếm số phiếu",
     "—",
     "- Số phiếu nhiều hơn lối vào “của tôi”, gồm cả phiếu của đồng nghiệp đã gửi đi\n"
     "- ⚠️ Vẫn không có phiếu “Đang tạo” của người khác"),

    ("003", "Nhãn trạng thái hiển thị đúng", "P0",
     "Có phiếu ở các trạng thái Đang tạo, Chờ xử lý, Đã xử lý.",
     "1. Mở danh sách\n2. Đối chiếu cột Trạng thái",
     "—",
     "- Hiện đúng chữ tiếng Việt của từng trạng thái, có nền màu phân biệt\n- Không dòng nào hiện "
     "ra số hoặc chữ tiếng Anh"),

    ("004", "Bấm mã phiếu mở màn xem chi tiết ở tab mới", "P1",
     "Có ít nhất 1 phiếu trong danh sách.",
     "1. Bấm vào mã phiếu ở cột Mã phiếu",
     "—",
     "- Mở tab mới hiển thị đúng phiếu vừa bấm\n- Toàn bộ ô ở chế độ chỉ đọc"),

    ("005", "Menu hành động theo trạng thái phiếu", "P0",
     "Phiếu P1 “Đang tạo” do chính mình lập; phiếu P2 “Chờ xử lý” gửi về phòng mình (có quyền xử "
     "lý); phiếu P3 “Đã xử lý”.",
     "1. Mở menu bánh răng của P1, P2, P3",
     "—",
     "- P1: Sửa, Xóa, In\n- P2: Tạo phiếu xử lý yêu cầu, Chuyển phòng tiếp nhận, In\n- P3: chỉ In\n"
     "- ⚠️ Mục không đủ điều kiện phải biến mất khỏi menu, không hiện mờ"),
]

SEC_II = [
    ("001", "Lọc theo Mã phiếu", "P0",
     "Tồn tại phiếu có mã đầy đủ dạng TPE.YCSCBH.26.xxxxxx.",
     "1. Gõ mã phiếu vào ô lọc dưới tiêu đề cột Mã phiếu\n2. Chờ bảng tải lại",
     "TPE.YCSCBH.26.005682",
     "- Ra đúng 1 phiếu\n- Dòng thống kê dưới bảng hiện tổng số 1 mục"),

    ("002", "Lọc theo Trạng thái", "P0",
     "Có phiếu ở ít nhất 3 trạng thái.",
     "1. Chọn “Chờ xử lý” ở ô lọc cột Trạng thái",
     "Trạng thái: Chờ xử lý",
     "- Mọi dòng đều là “Chờ xử lý”\n- Tổng số mục giảm đúng"),

    ("003", "Lọc theo Khách hàng", "P0",
     "Khách hàng Z có 18 phiếu.",
     "1. Ở ô lọc cột Khách hàng, gõ tên khách rồi chọn Z từ danh sách gợi ý",
     "Khách hàng: Z",
     "- Ra đúng 18 phiếu, tất cả cùng khách Z\n- ⚠️ Ô này tìm theo gợi ý, phải chọn từ danh sách "
     "chứ không chỉ gõ chữ"),

    ("004", "Lọc theo Tên, mã hàng hóa", "P0",
     "Có phiếu chứa thiết bị tên “Bệ kiểm tra phanh ô tô tải”.",
     "1. Gõ “Bệ kiểm tra” vào ô lọc cột Tên thiết bị liên quan",
     "Bệ kiểm tra",
     "- Kết quả trả về là phiếu có thiết bị khớp từ khóa\n- ⚠️ Mở vài phiếu trong kết quả đối "
     "chiếu tên thiết bị; báo lại nếu có phiếu không chứa thiết bị nào khớp"),

    ("005", "Lọc theo Người yêu cầu", "P1",
     "Nhân viên “Nguyễn Minh Hoàng” có phiếu trong hệ thống.",
     "1. Ở ô lọc cột Người yêu cầu, gõ tên rồi chọn từ danh sách gợi ý",
     "Người yêu cầu: Nguyễn Minh Hoàng",
     "- Mọi dòng đều có Người yêu cầu là người đã chọn"),

    ("006", "Lọc theo Tỉnh/TP", "P1",
     "Có khách hàng ở Hà Nội và ở Ninh Bình, mỗi bên đều có phiếu.",
     "1. Chọn “Hà Nội” ở ô lọc Tỉnh/TP",
     "Tỉnh/TP: Hà Nội",
     "- Chỉ còn phiếu của khách có địa chỉ thuộc Hà Nội"),

    ("007", "Lọc theo khoảng thời gian", "P0",
     "Có phiếu lập ngày 28/07/2026 và phiếu lập ngày 19/08/2026.",
     "1. Mở ô chọn khoảng thời gian trên thanh lọc\n2. Chọn từ 28/07/2026 đến 28/07/2026",
     "28/07/2026 - 28/07/2026",
     "- Chỉ còn phiếu lập trong ngày 28/07/2026\n- ⚠️ Chọn cùng một ngày ở cả hai đầu vẫn phải ra "
     "kết quả"),

    ("008", "Lọc theo công ty và phòng ban", "P1",
     "Người đăng nhập có quyền xem tổng công ty.",
     "1. Chọn công ty trên thanh lọc\n2. Chọn tiếp phòng ban",
     "Công ty: 1 — Phòng ban: Kinh doanh 1",
     "- Tổng số mục giảm dần đúng theo từng lần chọn\n- Ô phòng ban chỉ liệt kê phòng thuộc công "
     "ty đã chọn"),

    ("009", "Kết hợp nhiều điều kiện lọc", "P0",
     "Có ít nhất 1 phiếu “Chờ xử lý” của khách Z lập trong tháng 7/2026.",
     "1. Lọc trạng thái “Chờ xử lý”\n2. Lọc khách hàng Z\n3. Chọn khoảng 01/07/2026 - 31/07/2026",
     "—",
     "- Kết quả thỏa mãn đồng thời cả 3 điều kiện"),

    ("010", "Xóa điều kiện lọc", "P1",
     "Đang áp dụng 3 điều kiện, danh sách còn vài phiếu.",
     "1. Xóa nội dung từng ô lọc / chọn lại giá trị trống",
     "—",
     "- Danh sách trở lại tổng số ban đầu"),

    ("011", "Lọc không ra kết quả", "P1",
     "Không có phiếu nào mang mã “KHONG-TON-TAI-XYZ”.",
     "1. Gõ “KHONG-TON-TAI-XYZ” vào ô lọc Mã phiếu",
     "KHONG-TON-TAI-XYZ",
     "- Bảng hiện dòng thông báo không có dữ liệu\n- Không báo lỗi, không treo trang"),
]

SEC_III = [
    ("001", "Sắp xếp theo cột cho phép sắp xếp", "P1",
     "Danh sách có trên 20 phiếu.",
     "1. Bấm tiêu đề cột Mã phiếu\n2. Bấm lần nữa để đảo chiều\n3. Bấm tiêu đề cột Trạng thái",
     "—",
     "- Thứ tự đổi đúng chiều\n- ⚠️ Các cột Khách hàng, Tên thiết bị liên quan, Người yêu cầu… "
     "không sắp xếp được — đây là thiết kế hiện tại"),

    ("002", "Chuyển trang và đổi số dòng mỗi trang", "P0",
     "Bộ lọc hiện tại ra trên 100 phiếu.",
     "1. Bấm sang trang 2\n2. Đổi số dòng mỗi trang sang 50\n3. Quay về trang 1",
     "Số dòng: 50",
     "- Dòng thống kê cập nhật đúng x–y và tổng N\n- Không dòng nào lặp giữa 2 trang\n"
     "- Đổi số dòng thì bảng tải lại từ trang 1"),

    ("003", "Giữ bộ lọc khi chuyển trang", "P1",
     "Đang lọc trạng thái “Chờ xử lý”, kết quả trên 2 trang.",
     "1. Bấm sang trang 2\n2. Kiểm tra cột Trạng thái",
     "—",
     "- Trang 2 vẫn chỉ có phiếu “Chờ xử lý”, bộ lọc không bị mất"),
]

SEC_IV = [
    ("001", "Thêm mới phiếu đầy đủ và Lưu", "P0",
     "Khách hàng “CÔNG TY CỔ PHẦN SẢN XUẤT Ô TÔ HYUNDAI THÀNH CÔNG VIỆT NAM” đã có thiết bị trong "
     "hệ thống.",
     "1. Bấm nút thêm mới trên thanh công cụ\n2. Bấm nút kính lúp cạnh ô Khách hàng, tìm và chọn "
     "khách\n3. Chọn Người liên hệ, Địa chỉ sửa chữa, nhập Ghi chú, chọn Phòng tiếp nhận xử lý\n"
     "4. Ở bảng thiết bị của khách, bấm chọn 1 thiết bị\n5. Nhập serial và Mô tả yêu cầu cho dòng "
     "thiết bị\n6. Bấm nút Lưu",
     "Ghi chú: “Khách báo máy không lên nguồn”",
     "- Lưu thành công, chuyển về danh sách\n- Phiếu mới có mã phiếu, trạng thái “Đang tạo”"),

    ("002", "Chọn khách hàng tự điền thông tin liên quan", "P0",
     "Khách hàng đã khai nhiều người liên hệ và nhiều địa chỉ giao nhận.",
     "1. Bấm nút kính lúp cạnh ô Khách hàng\n2. Ở tab khách hàng tổ chức, gõ tên khách rồi bấm tìm\n"
     "3. Bấm chọn khách trong kết quả\n4. Mở ô Người liên hệ và ô Địa chỉ sửa chữa",
     "HYUNDAI THÀNH CÔNG",
     "- Ô Khách hàng hiện “<mã khách> - <tên khách>”\n- Ô Loại hình tổ chức tự điền\n"
     "- Danh sách người liên hệ và địa chỉ nạp đúng của khách vừa chọn\n- Bảng thiết bị của khách tự nạp"),

    ("003", "Tìm khách hàng cá nhân trong cửa sổ chọn", "P0",
     "Có khách hàng cá nhân đã khai số điện thoại.",
     "1. Mở cửa sổ chọn khách hàng\n2. Chuyển sang tab khách hàng cá nhân\n3. Bấm tìm khi chưa "
     "nhập gì\n4. Nhập đúng số điện thoại rồi tìm lại",
     "Số điện thoại: đúng số đã khai",
     "- Khi chưa nhập số điện thoại: không ra kết quả nào\n- Nhập đúng số: ra đúng khách cần tìm\n"
     "- ⚠️ Khách cá nhân chỉ tìm được bằng số điện thoại, không tìm bằng tên"),

    ("004", "Chọn thiết bị từ bảng thiết bị của khách", "P0",
     "Khách hàng đang chọn có nhiều thiết bị.",
     "1. Ở bảng “Danh mục trang thiết bị hiện có của khách hàng”, bấm chọn 2 thiết bị khác nhau",
     "—",
     "- Bảng thiết bị cần kiểm tra có thêm đúng 2 dòng\n- Tên, thương hiệu, model, nhà cung cấp "
     "chép đúng từ thiết bị đã chọn"),

    ("005", "Tìm kiếm trong bảng thiết bị của khách", "P1",
     "Khách hàng có thiết bị tên chứa “Bệ kiểm tra”.",
     "1. Nhập “Bệ kiểm tra” vào ô tìm của bảng thiết bị khách\n2. Bấm nút tìm\n3. Bấm nút làm mới",
     "Bệ kiểm tra",
     "- Bảng chỉ còn thiết bị khớp\n- Bấm làm mới thì trở lại danh sách đầy đủ"),

    ("006", "Phân trang bảng thiết bị của khách", "P1",
     "Khách hàng có trên 10 thiết bị.",
     "1. Xem dòng thống kê dưới bảng thiết bị\n2. Chuyển sang trang 2\n3. Chọn 1 thiết bị ở trang 2",
     "—",
     "- Trang 1 hiện 10 dòng\n- Chọn thiết bị ở trang 2 vẫn thêm đúng dòng đó vào bảng phía trên"),

    ("007", "Thêm trang thiết bị Tân Phát cho khách hàng", "P0",
     "Khách hàng đang chọn còn thiếu một thiết bị trong danh mục.",
     "1. Bấm nút “Thêm trang thiết bị của khách hàng”\n2. Chọn loại “Thiết bị Tân Phát CC”, bấm "
     "nút xác nhận loại\n3. Chọn trang thiết bị, nhập số lượng và các thông tin còn lại\n"
     "4. Bấm nút cập nhật",
     "Loại thiết bị: Thiết bị Tân Phát CC — Số lượng: 1",
     "- Cửa sổ đóng, bảng thiết bị của khách có thêm dòng vừa khai\n- Chọn được ngay dòng mới đó "
     "vào phiếu"),

    ("008", "Thêm trang thiết bị mua nhà cung cấp khác", "P1",
     "Khách hàng có thiết bị mua ngoài chưa khai.",
     "1. Bấm “Thêm trang thiết bị của khách hàng”\n2. Chọn loại “Thiết bị mua NCC khác”, xác nhận "
     "loại\n3. Khai tên thiết bị, nhà cung cấp, số lượng\n4. Bấm cập nhật",
     "Loại thiết bị: Thiết bị mua NCC khác",
     "- Thiết bị mới xuất hiện trong bảng thiết bị của khách với đúng loại"),

    ("009", "Đính kèm tài liệu cho dòng thiết bị", "P1",
     "Đang lập phiếu, đã có 1 dòng thiết bị. Có sẵn tệp PDF.",
     "1. Ở cột đính kèm của dòng thiết bị, chọn tệp\n2. Lưu phiếu\n3. Mở lại phiếu",
     "Tệp: bien-ban-hien-trang.pdf",
     "- Sau khi lưu, dòng thiết bị hiện tên tệp và tải xuống được\n- Tệp tải về đúng nội dung đã gửi"),

    ("010", "Sửa phiếu đang ở trạng thái Đang tạo", "P0",
     "Phiếu “Đang tạo” do chính người đăng nhập lập.",
     "1. Mở menu bánh răng, bấm Sửa\n2. Đổi Ghi chú, thêm 1 thiết bị\n3. Bấm Lưu\n4. Mở lại phiếu",
     "Ghi chú: “Cập nhật lần 2”",
     "- Lưu thành công\n- Mở lại thấy ghi chú mới và đủ số dòng thiết bị\n- Mã phiếu không đổi"),

    ("011", "Xóa dòng thiết bị khỏi phiếu", "P1",
     "Phiếu đang sửa có 2 dòng thiết bị.",
     "1. Xóa dòng thứ 2\n2. Bấm Lưu\n3. Mở lại phiếu",
     "—",
     "- Sau khi lưu, phiếu chỉ còn 1 dòng thiết bị"),

    ("012", "Màn xem chi tiết ở chế độ chỉ đọc", "P1",
     "Phiếu bất kỳ.",
     "1. Bấm mã phiếu để mở màn xem\n2. Thử gõ vào các ô",
     "—",
     "- Mọi ô đều khóa, không gõ được\n- Không có nút Lưu / Lưu & Gửi duyệt"),
]

SEC_V = [
    ("001", "Gửi phiếu cho phòng tiếp nhận", "P0",
     "Phiếu đã nhập đủ thông tin, phòng tiếp nhận là phòng Kỹ thuật (có 2 nhân viên).",
     "1. Mở màn sửa phiếu\n2. Bấm nút “Lưu & Gửi duyệt”\n3. Đăng nhập bằng nhân viên phòng Kỹ "
     "thuật, mở phần thông báo",
     "—",
     "- Phiếu chuyển sang “Chờ xử lý”\n- Cột Ngày yêu cầu ghi nhận thời điểm gửi\n"
     "- Nhân viên phòng Kỹ thuật nhận được thông báo “Xử lý yêu cầu sửa chữa”, bấm vào mở đúng phiếu"),

    ("002", "Chuyển phòng tiếp nhận từ danh sách", "P0",
     "Phiếu “Chờ xử lý”, phòng tiếp nhận là Kỹ thuật, người đăng nhập có quyền xử lý. Phòng Bảo "
     "hành có 3 nhân viên.",
     "1. Mở menu bánh răng, bấm “Chuyển phòng tiếp nhận”\n2. Ở cửa sổ “Xác nhận chuyển phòng tiếp "
     "nhận!”, chọn phòng Bảo hành\n3. Bấm nút xác nhận\n4. Đăng nhập bằng nhân viên phòng Bảo hành, "
     "mở phần thông báo",
     "Phòng tiếp nhận: Bảo hành",
     "- Báo thao tác thành công, danh sách tải lại\n- Phiếu vẫn “Chờ xử lý” nhưng phòng tiếp nhận "
     "là Bảo hành\n- Nhân viên phòng Bảo hành nhận được thông báo"),

    ("003", "Chặn chuyển sang đúng phòng đang tiếp nhận", "P0",
     "Phiếu “Chờ xử lý”, phòng tiếp nhận là Kỹ thuật.",
     "1. Bấm “Chuyển phòng tiếp nhận”\n2. Chọn lại đúng phòng Kỹ thuật\n3. Bấm xác nhận",
     "Phòng tiếp nhận: Kỹ thuật",
     "- Hệ thống báo trùng phòng tiếp nhận trước đó\n- Phiếu không đổi gì"),

    ("004", "Chưa chọn phòng mà bấm xác nhận", "P1",
     "Cửa sổ chuyển phòng đang mở, chưa chọn gì.",
     "1. Bấm nút xác nhận",
     "—",
     "- Hệ thống báo bắt buộc phải nhập\n- Cửa sổ không đóng"),

    ("005", "Từ chối phiếu bằng nút Không duyệt", "P0",
     "Phiếu “Chờ xử lý” gửi về phòng của người đăng nhập, người này có quyền xử lý. Phiếu do nhân "
     "viên G lập.",
     "1. Mở màn xem chi tiết phiếu\n2. Nhập lý do vào ô ghi chú xử lý\n3. Bấm nút “Không duyệt”\n"
     "4. Đăng nhập bằng G, mở phiếu",
     "Lý do: “Thiết bị còn hạn bảo hành hãng”",
     "- Phiếu trở lại “Đang tạo”, lý do được lưu trên phiếu\n- G sửa và gửi lại được, mã phiếu "
     "không đổi\n- ⚠️ G KHÔNG nhận được thông báo nào — hành vi hiện tại của hệ thống"),

    ("006", "Không duyệt mà bỏ trống lý do", "P0",
     "Đang ở màn xem chi tiết phiếu “Chờ xử lý”, ô lý do để trống.",
     "1. Bấm nút “Không duyệt”",
     "—",
     "- Hệ thống báo bắt buộc nhập lý do\n- Phiếu chưa đổi trạng thái"),

    ("007", "Nút Không duyệt chỉ có ở màn xem chi tiết", "P1",
     "Phiếu “Chờ xử lý” gửi về phòng của người đăng nhập.",
     "1. Mở menu bánh răng của phiếu ngoài danh sách\n2. Mở màn xem chi tiết của cùng phiếu đó",
     "—",
     "- Ngoài danh sách không có mục Không duyệt\n- Trong màn chi tiết có nút Không duyệt\n"
     "- ⚠️ Đây là thiết kế hiện tại, ghi nhận để đối chiếu khi so với cổng mới"),

    ("008", "Tạo phiếu xử lý yêu cầu", "P0",
     "Phiếu “Chờ xử lý”, người đăng nhập có quyền xử lý, phiếu chưa có phiếu xử lý nào.",
     "1. Mở menu bánh răng, bấm “Tạo phiếu xử lý yêu cầu”\n2. Hoàn tất phiếu xử lý\n3. Quay lại "
     "danh sách yêu cầu",
     "—",
     "- Màn lập phiếu xử lý mở ra với thông tin lấy sẵn từ phiếu yêu cầu\n- Sau khi lập xong, "
     "phiếu yêu cầu chuyển sang “Đang xử lý”"),

    ("009", "Phiếu đã có phiếu xử lý thì hết mục xử lý", "P1",
     "Phiếu đã được lập Phiếu xử lý yêu cầu.",
     "1. Mở menu bánh răng của phiếu\n2. Mở màn xem chi tiết",
     "—",
     "- Không còn mục Tạo phiếu xử lý yêu cầu và Chuyển phòng tiếp nhận\n- Màn chi tiết cũng không "
     "còn nút Không duyệt"),
]

SEC_VI = [
    ("001", "Xóa phiếu Đang tạo của chính mình", "P0",
     "Phiếu “Đang tạo” do chính người đăng nhập lập, có 2 dòng thiết bị.",
     "1. Mở menu bánh răng, bấm Xóa\n2. Đọc cửa sổ xác nhận\n3. Bấm Xác nhận",
     "—",
     "- Cửa sổ hỏi “Xác nhận xóa!”\n- Sau khi xác nhận, phiếu biến mất khỏi danh sách\n"
     "- Các dòng thiết bị của phiếu cũng bị xóa theo"),

    ("002", "Hủy ở cửa sổ xác nhận xóa", "P1",
     "Phiếu nháp của chính mình.",
     "1. Bấm Xóa\n2. Bấm Hủy",
     "—",
     "- Phiếu vẫn còn nguyên"),

    ("003", "Không có mục Xóa với phiếu đã gửi đi", "P0",
     "Phiếu “Chờ xử lý” do chính mình lập.",
     "1. Mở menu bánh răng của phiếu",
     "—",
     "- Không có mục Sửa và Xóa\n- Chỉ còn các mục xử lý (nếu đủ quyền) và In"),
]

SEC_VII = [
    ("001", "Xuất Excel theo bộ lọc", "P0",
     "Đang lọc trạng thái “Chờ xử lý”, kết quả 106 phiếu.",
     "1. Bấm nút xuất Excel trên thanh công cụ\n2. Mở tệp tải về",
     "—",
     "- Tệp chứa đúng 106 dòng\n- ⚠️ Phải là toàn bộ kết quả lọc, không dừng ở trang đang xem"),

    ("002", "Xuất Excel khi không lọc gì", "P1",
     "Không áp dụng bộ lọc nào.",
     "1. Bấm nút xuất Excel\n2. Mở tệp",
     "—",
     "- Số dòng bằng tổng số mục hiển thị dưới bảng\n- Các cột có tiêu đề tiếng Việt đọc được"),

    ("003", "In danh sách theo bộ lọc", "P0",
     "Đang lọc trạng thái “Đang tạo”, còn 4 phiếu.",
     "1. Bấm nút in danh sách\n2. Xem tab mới",
     "—",
     "- Mở tab mới với mẫu danh sách khổ ngang, có khung tờ giấy\n- Tiêu đề “DANH SÁCH PHIẾU YÊU "
     "CẦU KIỂM TRA SỬA CHỮA BẢO HÀNH”\n- Bảng có đúng 4 phiếu đang lọc\n- Dòng Thời gian in ra "
     "đúng khoảng đã lọc"),

    ("004", "In một phiếu", "P0",
     "Phiếu có 2 dòng thiết bị, đã điền đủ thông tin.",
     "1. Mở menu bánh răng, bấm In\n2. Xem tab mới\n3. Bấm nút In trên trang xem trước",
     "—",
     "- Trang hiển thị mẫu phiếu khổ dọc trên khung tờ giấy\n- Có mã phiếu, khách hàng, đủ 2 dòng "
     "thiết bị và khối ký tên\n- Không còn chỗ nào bỏ trống dạng ký hiệu chờ điền\n"
     "- Bấm In mở hộp thoại in của trình duyệt"),

    ("005", "Ngắt trang thủ công trên bản in", "P2",
     "Phiếu có nhiều thiết bị, bản in dài hơn 1 trang.",
     "1. Mở trang in phiếu\n2. Bấm vào vạch ngắt trang trong nội dung",
     "—",
     "- Vạch ngắt trang bật/tắt được, nội dung sau đó chuyển sang trang mới khi in"),
]

SEC_VIII = [
    ("001", "Bấm Lưu khi bỏ trống thông tin bắt buộc", "P0",
     "Phiếu mới chỉ chọn khách hàng, chưa nhập gì thêm, chưa chọn thiết bị.",
     "1. Bấm nút Lưu",
     "—",
     "- Không lưu được, vẫn ở màn nhập\n- Báo lỗi đỏ ngay dưới từng ô thiếu: Người liên hệ, Địa "
     "chỉ sửa chữa, Ghi chú, Phòng tiếp nhận xử lý\n- ⚠️ Nút Lưu cũng bắt buộc đủ như nút Lưu & "
     "Gửi duyệt, không phải lưu nháp tự do"),

    ("002", "Bấm Lưu & Gửi duyệt khi chưa chọn thiết bị", "P0",
     "Đã nhập đủ thông tin chung nhưng bảng thiết bị trống.",
     "1. Bấm “Lưu & Gửi duyệt”",
     "—",
     "- Hệ thống chặn, báo phải có ít nhất 1 thiết bị"),

    ("003", "Thiếu mô tả yêu cầu của dòng thiết bị", "P0",
     "Đã chọn 1 thiết bị nhưng để trống ô Mô tả yêu cầu.",
     "1. Bấm Lưu",
     "—",
     "- Hệ thống chặn, báo lỗi tại đúng dòng thiết bị thiếu mô tả"),

    ("004", "Chọn trùng serial trong cùng phiếu", "P0",
     "Thiết bị đã có serial khai trong hệ thống.",
     "1. Thêm cùng một thiết bị 2 lần\n2. Chọn cùng một serial cho cả 2 dòng\n3. Nhập mô tả yêu "
     "cầu\n4. Bấm Lưu",
     "Serial: cùng một số cho 2 dòng",
     "- Hệ thống chặn, báo bị trùng serial thiết bị"),

    ("005", "Thiết bị chưa có serial thì bắt nhập tay", "P0",
     "Chọn thiết bị chưa được khai serial nào.",
     "1. Thêm thiết bị đó, để trống ô serial\n2. Nhập mô tả yêu cầu\n3. Bấm Lưu",
     "Serial: (để trống)",
     "- Hệ thống chặn, báo bắt buộc nhập tại ô serial của dòng đó"),

    ("006", "Khách hàng cá nhân không có danh sách người liên hệ", "P1",
     "Có khách hàng cá nhân.",
     "1. Chọn khách hàng cá nhân qua tab tìm theo số điện thoại\n2. Xem ô Người liên hệ",
     "—",
     "- Ô Người liên hệ khóa lại, lấy luôn thông tin của chính khách\n- Nút thêm người liên hệ "
     "không dùng được"),

    ("007", "Chưa chọn khách hàng thì các ô liên quan bị khóa", "P1",
     "Màn thêm mới, chưa chọn khách.",
     "1. Thử mở ô Người liên hệ, ô Địa chỉ sửa chữa và ô tìm của bảng thiết bị",
     "—",
     "- Các ô này đều khóa cho tới khi chọn xong khách hàng"),
]

SEC_IX = [
    ("001", "Hai người cùng xử lý một phiếu", "P1",
     "Phiếu “Chờ xử lý”, hai nhân viên E và F cùng phòng tiếp nhận, cùng mở phiếu.",
     "1. E bấm Không duyệt kèm lý do\n2. F (chưa tải lại trang) bấm Chuyển phòng tiếp nhận",
     "—",
     "- Thao tác của F không được thực hiện hoặc hệ thống báo trạng thái đã thay đổi\n- Không treo "
     "trang; tải lại thấy phiếu ở “Đang tạo”"),

    ("002", "Xóa phiếu vừa bị người khác xóa", "P2",
     "Hai cửa sổ cùng mở danh sách, cùng thấy phiếu nháp X.",
     "1. Cửa sổ 1 xóa phiếu X\n2. Cửa sổ 2 (chưa tải lại) cũng bấm Xóa phiếu X",
     "—",
     "- Cửa sổ 2 không gây lỗi trắng trang\n- Tải lại danh sách không còn phiếu X"),

    ("003", "Dữ liệu lập bên cổng mới hiện ngay bên ERP", "P0",
     "Có tài khoản dùng được cả 2 cổng.",
     "1. Lập và gửi 1 phiếu bên cổng mới\n2. Sang ERP, lọc theo mã phiếu vừa lập",
     "Mã phiếu vừa lập bên cổng mới",
     "- Tìm thấy đúng phiếu, trạng thái “Chờ xử lý”\n- Mở ra thấy đủ khách hàng và các dòng thiết bị"),
]

SEC_X = [
    ("001", "Luồng đầy đủ: lập → gửi → không duyệt → sửa → gửi lại → chuyển phòng", "P0",
     "Nhân viên G (người lập); phòng Kỹ thuật có E; phòng Bảo hành có H. Khách hàng đã có thiết bị.",
     "1. G lập phiếu đủ thông tin, chọn 1 thiết bị, bấm Lưu\n2. G mở lại, bấm “Lưu & Gửi duyệt” "
     "(phòng tiếp nhận: Kỹ thuật)\n3. E nhận thông báo, mở phiếu, nhập lý do và bấm Không duyệt\n"
     "4. G mở lại phiếu, sửa và gửi lại\n5. E bấm Chuyển phòng tiếp nhận sang Bảo hành\n"
     "6. H mở phần thông báo",
     "Lý do: “Thiếu ảnh hiện trạng thiết bị”",
     "- Bước 1: phiếu “Đang tạo”, đã có mã phiếu\n- Bước 2: phiếu “Chờ xử lý”, E có thông báo\n"
     "- Bước 3: phiếu về “Đang tạo”, lý do lưu trên phiếu, ⚠️ G không có thông báo\n"
     "- Bước 4: phiếu lại “Chờ xử lý”, mã phiếu không đổi\n- Bước 5-6: phòng tiếp nhận là Bảo "
     "hành, H có thông báo"),

    ("002", "Luồng lập rồi xóa", "P1",
     "Nhân viên G lập phiếu được.",
     "1. G lập phiếu, bấm Lưu\n2. G mở lại, thêm thiết bị, Lưu\n3. G xóa phiếu\n4. Lọc theo mã "
     "phiếu vừa xóa",
     "—",
     "- Không tìm thấy phiếu\n- Tổng số mục trở về như trước khi lập"),

    ("003", "Luồng đi tiếp sang Phiếu xử lý yêu cầu", "P0",
     "Phiếu “Chờ xử lý”, người đăng nhập có quyền xử lý.",
     "1. Bấm “Tạo phiếu xử lý yêu cầu”\n2. Hoàn tất phiếu xử lý\n3. Quay lại danh sách yêu cầu",
     "—",
     "- Phiếu yêu cầu chuyển sang “Đang xử lý”\n- Cột Người xử lý và Ngày xử lý được điền\n"
     "- Không còn mục chuyển phòng / không duyệt"),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", SEC_III),
    ("IV", "THÊM MỚI, SỬA & XEM", SEC_IV),
    ("V", "GỬI DUYỆT, CHUYỂN PHÒNG TIẾP NHẬN & KHÔNG DUYỆT", SEC_V),
    ("VI", "XÓA", SEC_VI),
    ("VII", "XUẤT EXCEL / IN", SEC_VII),
    ("VIII", "RÀNG BUỘC NHẬP LIỆU", SEC_VIII),
    ("IX", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", SEC_IX),
    ("X", "LUỒNG NGHIỆP VỤ ĐẦU – CUỐI", SEC_X),
]

build(output_file=OUTPUT_FILE,
      sheet_name="Trang tính1",
      feature_name="Yêu cầu kiểm tra sửa chữa – bảo hành (cổng ERP) - Cập nhật ngày 20/08/2026",
      module_name=MODULE,
      description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS,
      sections=SECTIONS)
