# -*- coding: utf-8 -*-
"""Sinh testcase (form 17 cot) cho man **Phieu chuyen hang nhap thang** ban HRM
(phan he Tai chinh - nhom Dieu chuyen), tuc phan da chuyen doi tu ERP sang HRM.

Chay:  python gen_testcase.py
Output: "testcase - Phieu chuyen hang nhap thang.xlsx" cung thu muc.

Nguon noi dung: design.md + plan.md cua feature, doc kem ma nguon man danh sach / form /
lich su va cac rang buoc ben may chu (trang thai, quyen, thong bao loi).
"""
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
OUTPUT = os.path.join(HERE, "testcase - Phieu chuyen hang nhap thang.xlsx")

MODULE_NAME = "Phiếu chuyển hàng nhập thẳng"
FEATURE_NAME = "Phiếu chuyển hàng nhập thẳng (Tài chính)"

# =====================================================================================
# 9 MỤC MÔ TẢ
# =====================================================================================
DESCRIPTION_BLOCK = [
    (
        "1. Mục đích tính năng",
        "Hàng \"nhập thẳng\" là hàng về thẳng tay nhân viên, không nhập qua kho, nên tồn được ghi "
        "theo từng nhân viên chứ không theo kho.\n"
        "Màn này dùng để nhân viên đang giữ hàng nhập thẳng lập phiếu chuyển số hàng đó sang một "
        "nhân viên khác cùng công ty. Phiếu phải được người có quyền Kế toán kho duyệt; khi duyệt, "
        "hệ thống trừ tồn của người lập (trừ theo thứ tự lô nhận trước dùng trước) và tạo tồn "
        "tương ứng cho người nhận.\n"
        "Đây là màn đã chuyển từ hệ thống ERP sang phân hệ Tài chính của HRM. Hai cổng chạy trên "
        "cùng một cơ sở dữ liệu nên số liệu phải khớp nhau.\n"
        "Đường dẫn: Tài chính > nhóm Điều chuyển > Phiếu chuyển hàng nhập thẳng.",
    ),
    (
        "2. Đối tượng được hiển thị",
        "Người dùng nhìn thấy phiếu theo phạm vi quyền được cấp:\n"
        "- Quyền xem theo tổng công ty: thấy phiếu của mọi công ty.\n"
        "- Quyền xem theo công ty: thấy phiếu cùng công ty với mình.\n"
        "- Quyền xem theo phòng ban: thấy phiếu thuộc các phòng ban mình quản lý.\n"
        "- Quyền xem theo bộ phận: thấy phiếu thuộc các bộ phận mình quản lý.\n"
        "- Ngoài ra, ai cũng luôn thấy phiếu do chính mình lập.\n"
        "- Người có quyền Kế toán kho còn thấy thêm mọi phiếu đang ở trạng thái Chờ duyệt của "
        "công ty mình, để duyệt được ngay trên danh sách chính (màn đã bỏ tab \"Chờ duyệt\" riêng).\n"
        "4 trạng thái phiếu: Đang tạo (nhãn xám) · Chờ duyệt (nhãn vàng) · Đã duyệt (nhãn xanh) · "
        "Không duyệt (nhãn đỏ).",
    ),
    (
        "3. Đối tượng bị ẩn / không hiển thị",
        "- Phiếu ngoài phạm vi quyền của người đăng nhập và không do người đó lập.\n"
        "- Phiếu \"Đang tạo\" (bản nháp) của người khác: chỉ người lập mới thấy bản nháp của mình.\n"
        "- Bộ lọc Bộ phận cố tình KHÔNG có trên màn này: phiếu không lưu bộ phận riêng nên lọc theo "
        "bộ phận sẽ luôn ra rỗng và gây hiểu nhầm là mất dữ liệu.\n"
        "- Hàng hóa không còn tồn nhập thẳng của người lập phiếu sẽ không xuất hiện trong cửa sổ "
        "chọn hàng.",
    ),
    (
        "4. Bộ lọc thời gian áp dụng cho",
        "Hai ô \"Ngày tạo từ\" và \"Ngày tạo đến\" lọc theo NGÀY LẬP PHIẾU (cột Ngày tạo trên lưới), "
        "không phải ngày duyệt và không phải ngày cập nhật.\n"
        "Lọc bao gồm cả ngày đầu và ngày cuối. Chỉ nhập một trong hai ô thì lọc một chiều "
        "(từ ngày đó trở đi, hoặc tới ngày đó).",
    ),
    (
        "5. Cấu trúc dữ liệu",
        "Mỗi phiếu gồm phần Thông tin chung (Người nhận, Phòng ban của người nhận, Ghi chú, Số phiếu, "
        "Trạng thái, Người duyệt) và bảng Chi tiết hàng hóa nhiều dòng.\n"
        "Mỗi dòng hàng gồm: Tên hàng · Mã hàng · ĐVT · Số lượng · SL theo ĐV cơ bản · Tồn hiện có.\n"
        "\"SL theo ĐV cơ bản\" = Số lượng nhân hệ số quy đổi của đơn vị tính đang chọn; đây là con số "
        "hệ thống dùng để trừ tồn khi duyệt.\n"
        "Số phiếu do hệ thống tự sinh theo mẫu <mã công ty>_CHNT_<số thứ tự>, người dùng không nhập.",
    ),
    (
        "6. Quy tắc cộng dồn khi kiểm tồn",
        "Khi lưu và khi duyệt, hệ thống GỘP các dòng cùng một hàng hóa lại rồi mới so với tồn hiện "
        "có của người lập phiếu. Nếu phiếu có 2 dòng cùng một hàng, mỗi dòng bằng nửa số tồn thì "
        "tổng vẫn vừa đủ và được lưu; nếu tổng vượt tồn thì bị chặn ngay.\n"
        "Khi duyệt, hệ thống trừ lần lượt từng lô tồn của người lập theo thứ tự nhận trước dùng "
        "trước cho tới khi đủ số lượng, ghi lại biến động của từng lô, rồi tạo một lô tồn mới cho "
        "người nhận.\n"
        "Việc duyệt GHI TỒN THẬT và không có chức năng hoàn tác.",
    ),
    (
        "7. Phân quyền",
        "Màn dùng lại nguyên bộ quyền của hệ thống ERP, không thêm quyền mới:\n"
        "- \"Xem phiếu chuyển hàng nhập thẳng theo tổng công ty\"\n"
        "- \"Xem phiếu chuyển hàng nhập thẳng theo công ty\"\n"
        "- \"Xem phiếu chuyển hàng nhập thẳng theo phòng ban\"\n"
        "- \"Xem phiếu chuyển hàng nhập thẳng theo bộ phận\"\n"
        "- \"Kế toán kho\": quyền Duyệt / Từ chối phiếu, và được thấy phiếu Chờ duyệt cùng công ty.\n"
        "Quy tắc thao tác: chỉ NGƯỜI LẬP mới được Sửa / Xóa, và chỉ khi phiếu ở trạng thái Đang tạo "
        "hoặc Không duyệt. Người có quyền Kế toán kho CÙNG CÔNG TY với phiếu mới được Duyệt / Từ chối, "
        "và chỉ khi phiếu đang Chờ duyệt.",
    ),
    (
        "8. Cách đọc các ô thống kê",
        "Dòng \"Hiển thị a–b / N phiếu\" dưới lưới: a là số thứ tự dòng đầu của trang đang xem, b là "
        "dòng cuối, N là tổng số phiếu khớp bộ lọc hiện tại (không phải tổng toàn hệ thống).\n"
        "Ô \"Tồn hiện có\" trên từng dòng hàng: số tồn nhập thẳng của NGƯỜI LẬP PHIẾU quy về đơn vị "
        "tính đang chọn ở dòng đó; đổi đơn vị tính thì con số này đổi theo.\n"
        "Con số cạnh tiêu đề khối Lịch sử thay đổi là số mốc lịch sử đã ghi nhận của phiếu.",
    ),
    (
        "9. Ghi chú đọc bảng (bẫy dễ sai)",
        "- Định dạng số theo chuẩn quốc tế: dấu phẩy ngăn cách hàng nghìn, dấu chấm ngăn phần thập "
        "phân (ví dụ 1,234.5).\n"
        "- Ô Số lượng KHÔNG tự sửa giá trị người dùng nhập. Nhập vượt tồn thì giữ nguyên con số vừa "
        "nhập và báo đỏ ngay dưới ô; hệ thống không tự kéo về mức tối đa.\n"
        "- Cột Ngày tạo hiển thị cả giờ và phút.\n"
        "- Các cột Công ty, Phòng ban, Ghi chú, Người duyệt, Người cập nhật, Ngày cập nhật mặc định "
        "ẩn; bật ở nút Cấu hình cột hiển thị.\n"
        "- Lưu nháp chỉ bắt buộc ô Người nhận; các ô khác để trống vẫn lưu được. Gửi duyệt thì bắt "
        "buộc có ít nhất một dòng hàng hóa hợp lệ.\n"
        "- Lịch sử thay đổi chỉ ghi nhận thao tác thực hiện trên hệ thống HRM. Phiếu được sửa hoặc "
        "duyệt bên cổng ERP sẽ không có mốc lịch sử ở đây - đây là hiện tượng đã biết, không ghi "
        "Failed.\n"
        "- Nhóm test bảo mật gọi thẳng chức năng bằng công cụ kiểm thử (bỏ qua giao diện) dành cho "
        "tester kỹ thuật.",
    ),
]

# =====================================================================================
# PHÂN QUYỀN & TRUY CẬP
# =====================================================================================
ROLE_TCS = [
    (
        "01",
        "Quyền xem theo tổng công ty thấy phiếu của mọi công ty",
        "P0",
        "Tài khoản A chỉ có quyền \"Xem phiếu chuyển hàng nhập thẳng theo tổng công ty\", không có "
        "quyền Kế toán kho. Hệ thống có phiếu của ít nhất 3 công ty khác nhau.",
        "1. Đăng nhập bằng tài khoản A\n"
        "2. Vào Tài chính > Điều chuyển > Phiếu chuyển hàng nhập thẳng\n"
        "3. Mở bộ lọc, xem danh sách công ty trong ô Công ty",
        "—",
        "- Danh sách hiện phiếu của cả 3 công ty\n"
        "- Ô lọc Công ty liệt kê đủ các công ty\n"
        "- Tổng số phiếu ở dòng \"Hiển thị a–b / N phiếu\" bằng tổng phiếu toàn hệ thống trừ các bản "
        "nháp \"Đang tạo\" của người khác",
    ),
    (
        "02",
        "Quyền xem theo công ty chỉ thấy phiếu cùng công ty",
        "P0",
        "Tài khoản B thuộc công ty 1, chỉ có quyền \"Xem phiếu chuyển hàng nhập thẳng theo công ty\". "
        "Công ty 1 có 12 phiếu, công ty 4 có 9 phiếu.",
        "1. Đăng nhập bằng tài khoản B\n"
        "2. Mở màn danh sách\n"
        "3. Đối chiếu cột Công ty (bật cột này ở Cấu hình cột hiển thị)",
        "—",
        "- Chỉ thấy 12 phiếu của công ty 1\n"
        "- Không có dòng nào thuộc công ty 4\n"
        "- ⚠️ Vẫn phải thấy phiếu do chính tài khoản B lập kể cả bản nháp",
    ),
    (
        "03",
        "Quyền xem theo phòng ban chỉ thấy phiếu phòng mình quản lý",
        "P0",
        "Tài khoản C quản lý phòng Kinh doanh 1, chỉ có quyền \"Xem phiếu chuyển hàng nhập thẳng "
        "theo phòng ban\". Phòng Kinh doanh 1 có 5 phiếu, phòng Kỹ thuật có 7 phiếu.",
        "1. Đăng nhập bằng tài khoản C\n"
        "2. Mở màn danh sách\n"
        "3. Bật cột Phòng ban ở Cấu hình cột hiển thị",
        "—",
        "- Chỉ thấy 5 phiếu của phòng Kinh doanh 1 (cộng thêm phiếu do chính mình lập nếu có)\n"
        "- Không thấy phiếu của phòng Kỹ thuật",
    ),
    (
        "04",
        "Quyền xem theo bộ phận chỉ thấy phiếu bộ phận mình quản lý",
        "P1",
        "Tài khoản D quản lý bộ phận Bán lẻ, chỉ có quyền \"Xem phiếu chuyển hàng nhập thẳng theo "
        "bộ phận\". Bộ phận Bán lẻ có 3 phiếu.",
        "1. Đăng nhập bằng tài khoản D\n"
        "2. Mở màn danh sách",
        "—",
        "- Chỉ thấy 3 phiếu của bộ phận Bán lẻ (cộng phiếu do chính mình lập)\n"
        "- ⚠️ Màn KHÔNG có ô lọc Bộ phận - đây là thiết kế cố ý, không phải thiếu chức năng",
    ),
    (
        "05",
        "Quyền Kế toán kho thấy phiếu Chờ duyệt của công ty mình",
        "P0",
        "Tài khoản E thuộc công ty 1, CHỈ có quyền Kế toán kho (không có quyền xem theo cấp nào). "
        "Công ty 1 có đúng 1 phiếu đang Chờ duyệt do người khác lập.",
        "1. Đăng nhập bằng tài khoản E\n"
        "2. Mở màn danh sách",
        "—",
        "- Thấy đúng 1 phiếu Chờ duyệt đó ngay trên danh sách chính, không cần vào tab riêng\n"
        "- Mở phiếu ra thấy nút Duyệt và nút Từ chối\n"
        "- Không thấy phiếu Đã duyệt / Không duyệt của người khác (trừ phiếu chính mình lập)",
    ),
    (
        "06",
        "Tài khoản không có quyền nào chỉ thấy phiếu của chính mình",
        "P0",
        "Tài khoản F không được cấp bất kỳ quyền nào trong 5 quyền của màn; tài khoản F đã lập 6 phiếu.",
        "1. Đăng nhập bằng tài khoản F\n"
        "2. Mở màn danh sách\n"
        "3. Bấm vào một phiếu của mình",
        "—",
        "- Chỉ thấy đúng 6 phiếu do mình lập\n"
        "- Mở được chi tiết phiếu của mình\n"
        "- Không có nút Duyệt / Từ chối",
    ),
    (
        "07",
        "Mở chi tiết phiếu ngoài phạm vi quyền",
        "P0",
        "Tài khoản B (quyền xem theo công ty 1). Lấy đường dẫn chi tiết của một phiếu thuộc công ty 4.",
        "1. Đăng nhập bằng tài khoản B\n"
        "2. Dán đường dẫn chi tiết phiếu của công ty 4 lên thanh địa chỉ, nhấn Enter",
        "—",
        "- Hệ thống từ chối, báo không có quyền xem phiếu này\n"
        "- Tự quay về màn danh sách, không treo trang trắng\n"
        "- ⚠️ Đây là điểm đã sửa so với hệ thống cũ: bên cũ người có quyền xem theo cấp thấy phiếu "
        "ở danh sách nhưng bấm vào lại báo không tìm thấy",
    ),
    (
        "08",
        "Người có quyền xem theo cấp mở được chi tiết phiếu nhìn thấy trên danh sách",
        "P0",
        "Tài khoản C (quyền xem theo phòng ban), danh sách đang hiện 5 phiếu của phòng mình quản lý, "
        "trong đó không có phiếu nào do C lập.",
        "1. Đăng nhập bằng tài khoản C\n"
        "2. Lần lượt bấm vào số phiếu của cả 5 dòng",
        "—",
        "- Cả 5 phiếu đều mở được màn chi tiết\n"
        "- Không phiếu nào báo không tìm thấy dữ liệu\n"
        "- Không có nút Sửa / Xóa vì C không phải người lập",
    ),
    (
        "09",
        "Chặn duyệt bằng cách gọi thẳng chức năng, bỏ qua giao diện",
        "P0",
        "Tài khoản F không có quyền Kế toán kho. Tồn tại phiếu đang Chờ duyệt của công ty khác.",
        "1. Đăng nhập bằng tài khoản F\n"
        "2. Dùng công cụ kiểm thử gọi thẳng chức năng Duyệt cho phiếu đó, bỏ qua giao diện\n"
        "3. Mở lại phiếu kiểm tra",
        "—",
        "- Hệ thống từ chối, báo không có quyền\n"
        "- Phiếu vẫn ở trạng thái Chờ duyệt\n"
        "- Tồn hàng nhập thẳng của cả hai nhân viên không thay đổi",
    ),
    (
        "10",
        "Chặn sửa / xóa phiếu người khác bằng cách gọi thẳng chức năng",
        "P0",
        "Tài khoản F. Phiếu đang Đang tạo do tài khoản khác lập.",
        "1. Đăng nhập bằng tài khoản F\n"
        "2. Dùng công cụ kiểm thử gọi thẳng chức năng Sửa rồi chức năng Xóa cho phiếu đó",
        "—",
        "- Cả hai lần đều bị từ chối, báo không có quyền\n"
        "- Phiếu và các dòng hàng hóa của phiếu còn nguyên",
    ),
    (
        "11",
        "Chặn tự đặt trạng thái Đã duyệt khi lưu phiếu",
        "P0",
        "Tài khoản F, đang có một phiếu nháp của chính mình.",
        "1. Dùng công cụ kiểm thử gọi thẳng chức năng Lưu phiếu, cố tình gán trạng thái Đã duyệt\n"
        "2. Mở lại phiếu",
        "—",
        "- Hệ thống báo lỗi dữ liệu không hợp lệ ở ô Trạng thái\n"
        "- Phiếu KHÔNG chuyển sang Đã duyệt\n"
        "- ⚠️ Đây là lỗ hổng của hệ thống cũ đã được vá: bên cũ gửi thẳng trạng thái Đã duyệt là "
        "phiếu tự duyệt, bỏ qua Kế toán kho",
    ),
    (
        "12",
        "Kế toán kho khác công ty không duyệt được",
        "P0",
        "Tài khoản G có quyền Kế toán kho nhưng thuộc công ty 4. Phiếu Chờ duyệt thuộc công ty 1.",
        "1. Đăng nhập bằng tài khoản G\n"
        "2. Tìm phiếu của công ty 1 (nếu nhìn thấy được qua quyền xem theo tổng công ty)\n"
        "3. Mở chi tiết",
        "—",
        "- Không có nút Duyệt và nút Từ chối\n"
        "- Gọi thẳng chức năng Duyệt bằng công cụ kiểm thử cũng bị từ chối",
    ),
]

# =====================================================================================
# SECTIONS NGHIỆP VỤ
# =====================================================================================
SEC_I = [
    (
        1,
        "Mở màn từ menu Tài chính",
        "P0",
        "Tài khoản A có quyền xem theo tổng công ty.",
        "1. Đăng nhập\n"
        "2. Vào phân hệ Tài chính\n"
        "3. Mở nhóm Điều chuyển ở menu bên trái\n"
        "4. Bấm \"Phiếu chuyển hàng nhập thẳng\"",
        "—",
        "- Mục menu nằm trong nhóm Điều chuyển, ngay cạnh mục Phiếu điều chuyển hàng\n"
        "- Trang mở ra có tiêu đề \"Phiếu chuyển hàng nhập thẳng\"\n"
        "- Mục menu đang mở được tô sáng",
    ),
    (
        2,
        "Bố cục mặc định của màn danh sách",
        "P0",
        "Tài khoản A, dữ liệu có ít nhất 30 phiếu.",
        "1. Mở màn danh sách\n"
        "2. Quan sát từ trên xuống",
        "—",
        "- Trên cùng là khối Bộ lọc danh sách với ô tìm nhanh\n"
        "- Dưới là bảng dữ liệu, hàng nút gồm: Tạo mới (xanh) · In (trắng) · Xuất Excel (xanh lá) · "
        "biểu tượng Cấu hình cột hiển thị\n"
        "- 7 cột mặc định: STT · Số phiếu · Người nhận · Người tạo · Ngày tạo · Trạng thái · Hành động",
    ),
    (
        3,
        "Cột STT và Số phiếu luôn dính khi cuộn ngang",
        "P1",
        "Đã bật đủ các cột ẩn để bảng rộng hơn màn hình.",
        "1. Bật tất cả cột ở Cấu hình cột hiển thị\n"
        "2. Cuộn bảng sang phải",
        "—",
        "- Cột STT và Số phiếu đứng yên bên trái, luôn nhìn thấy\n"
        "- Cột Hành động luôn nhìn thấy\n"
        "- Trang không bị đẩy tràn ngang, chỉ bảng cuộn",
    ),
    (
        4,
        "Số phiếu là liên kết mở chi tiết",
        "P0",
        "Danh sách có ít nhất 1 phiếu.",
        "1. Bấm vào số phiếu ở cột Số phiếu\n"
        "2. Quay lại, bấm chuột phải vào số phiếu chọn mở tab mới",
        "—",
        "- Bấm trái mở màn chi tiết đúng phiếu đó\n"
        "- Bấm chuột phải mở được tab mới (đây là liên kết thật, không phải nút giả)",
    ),
    (
        5,
        "Bật / tắt cột bằng Cấu hình cột hiển thị",
        "P1",
        "Tài khoản A đang xem màn danh sách.",
        "1. Bấm biểu tượng Cấu hình cột hiển thị\n"
        "2. Tick thêm Công ty, Phòng ban, Ghi chú, Người duyệt, Người cập nhật, Ngày cập nhật\n"
        "3. Lưu lại\n"
        "4. Tải lại trang",
        "—",
        "- 6 cột vừa tick hiện trên lưới\n"
        "- Sau khi tải lại trang, cấu hình cột vẫn giữ nguyên (hệ thống ghi nhớ theo từng người dùng)\n"
        "- ⚠️ Không tắt được cột STT, Số phiếu, Hành động (đã khóa)",
    ),
    (
        6,
        "Mở màn bằng đường dẫn xem tất cả",
        "P0",
        "Tài khoản A có quyền xem theo tổng công ty. Hệ thống có 120 phiếu.",
        "1. Mở màn danh sách kèm tham số xem tất cả trên thanh địa chỉ\n"
        "2. Đối chiếu tổng số phiếu ở dòng \"Hiển thị a–b / N phiếu\"",
        "Tham số: xem tất cả",
        "- Danh sách hiện đúng phạm vi quyền của tài khoản A\n"
        "- Con số N khớp với số phiếu đếm được bên cổng ERP với cùng người dùng",
    ),
    (
        7,
        "Mở màn bằng đường dẫn chờ duyệt (đường dẫn cũ của hệ thống ERP)",
        "P1",
        "Tài khoản E có quyền Kế toán kho, công ty 1 có 1 phiếu Chờ duyệt.",
        "1. Mở màn danh sách kèm tham số chờ duyệt trên thanh địa chỉ",
        "Tham số: chờ duyệt",
        "- Danh sách chỉ hiện phiếu đang Chờ duyệt của công ty mình\n"
        "- Đường dẫn cũ vẫn chạy được, không báo lỗi",
    ),
    (
        8,
        "Người không phải Kế toán kho mở đường dẫn chờ duyệt",
        "P1",
        "Tài khoản F không có quyền Kế toán kho, đã lập 6 phiếu.",
        "1. Mở màn danh sách kèm tham số chờ duyệt",
        "Tham số: chờ duyệt",
        "- Danh sách trả về rỗng kèm dòng \"Không có dữ liệu phù hợp bộ lọc.\"\n"
        "- ⚠️ KHÔNG được trả về 6 phiếu của chính mình - màn chờ duyệt của người không có quyền "
        "duyệt phải trống mới đúng nghĩa",
    ),
    (
        9,
        "Sửa tay tham số trên thanh địa chỉ thành giá trị lạ",
        "P1",
        "Tài khoản A.",
        "1. Gõ tay một giá trị vô nghĩa vào tham số phạm vi trên thanh địa chỉ\n"
        "2. Nhấn Enter",
        "Tham số: một chuỗi ký tự bất kỳ",
        "- Hệ thống bỏ qua giá trị lạ, quay về phạm vi mặc định\n"
        "- Không báo lỗi, không lộ thêm phiếu ngoài phạm vi quyền",
    ),
    (
        10,
        "Đổi bộ lọc rồi mở lại màn bằng đường dẫn khác",
        "P1",
        "Tài khoản A đã lọc theo công ty 4 ở lần vào trước.",
        "1. Lọc theo công ty 4, có kết quả\n"
        "2. Chuyển sang màn khác\n"
        "3. Quay lại màn bằng đường dẫn xem tất cả",
        "—",
        "- Đường dẫn vừa mở THẮNG bộ lọc lần trước, danh sách theo đúng phạm vi của đường dẫn\n"
        "- Không giữ lại phạm vi công ty 4 của lần trước",
    ),
    (
        11,
        "Trang trống khi không có phiếu nào",
        "P2",
        "Tài khoản mới chưa lập phiếu nào và không có quyền xem theo cấp.",
        "1. Mở màn danh sách",
        "—",
        "- Lưới hiện dòng \"Không có dữ liệu phù hợp bộ lọc.\"\n"
        "- Vẫn có đủ nút Tạo mới, In, Xuất Excel\n"
        "- Không hiện lỗi kỹ thuật",
    ),
    (
        12,
        "Tốc độ mở màn lần đầu",
        "P2",
        "Danh sách có trên 800 phiếu.",
        "1. Mở màn danh sách và bấm giờ tới khi bảng hiện dữ liệu",
        "—",
        "- Bảng hiện dữ liệu, trong lúc chờ có hiệu ứng đang tải\n"
        "- Không gọi trùng dữ liệu (không thấy lưới nhấp nháy nạp 2 lần)",
    ),
]

SEC_II = [
    (
        1,
        "Danh sách đầy đủ ô lọc",
        "P0",
        "Tài khoản A.",
        "1. Mở khối Bộ lọc danh sách\n"
        "2. Liệt kê các ô lọc",
        "—",
        "- Có: Công ty · Phòng ban · Số phiếu · Trạng thái · Tên/mã hàng hóa · Người nhận · "
        "Người tạo · Ngày tạo từ · Ngày tạo đến\n"
        "- ⚠️ KHÔNG có ô Bộ phận (cố ý bỏ)\n"
        "- Ô tìm nhanh có gợi ý \"Tìm theo số phiếu hoặc người tạo...\"",
    ),
    (
        2,
        "Lọc theo Công ty",
        "P0",
        "Công ty 1 có 12 phiếu, công ty 4 có 9 phiếu. Tài khoản A xem được cả hai.",
        "1. Chọn Công ty = công ty 1\n"
        "2. Chờ danh sách tự tải lại",
        "Công ty: công ty 1",
        "- Danh sách còn 12 phiếu\n"
        "- Bật cột Công ty thấy mọi dòng đều là công ty 1\n"
        "- Danh sách tự tải lại sau khi chọn, không cần bấm nút Tìm",
    ),
    (
        3,
        "Chọn Công ty rồi chọn Phòng ban theo tầng",
        "P0",
        "Công ty 1 có 4 phòng ban.",
        "1. Chọn Công ty = công ty 1\n"
        "2. Mở ô Phòng ban",
        "Công ty: công ty 1",
        "- Ô Phòng ban chỉ liệt kê 4 phòng của công ty 1\n"
        "- Đổi sang công ty khác thì ô Phòng ban tự xóa lựa chọn cũ và nạp lại danh sách mới",
    ),
    (
        4,
        "Lọc theo Số phiếu",
        "P0",
        "Tồn tại phiếu số TPV_CHNT_853.",
        "1. Nhập TPV_CHNT_853 vào ô Số phiếu\n"
        "2. Chờ danh sách tải lại",
        "Số phiếu: TPV_CHNT_853",
        "- Danh sách còn đúng 1 dòng, số phiếu khớp\n"
        "- ⚠️ Ô này là ô bổ sung so với hệ thống cũ; trước đây không lọc được theo số phiếu",
    ),
    (
        5,
        "Lọc theo Số phiếu bằng một phần chuỗi",
        "P1",
        "Có nhiều phiếu bắt đầu bằng TPV_CHNT.",
        "1. Nhập TPV_CHNT vào ô Số phiếu",
        "Số phiếu: TPV_CHNT",
        "- Danh sách hiện tất cả phiếu có số phiếu chứa chuỗi đó\n"
        "- Số lượng khớp với số đếm được khi lọc cùng điều kiện bên cổng ERP",
    ),
    (
        6,
        "Lọc theo Trạng thái",
        "P0",
        "Trong phạm vi quyền có: 4 phiếu Đang tạo, 3 Chờ duyệt, 20 Đã duyệt, 2 Không duyệt.",
        "1. Lần lượt chọn từng trạng thái trong ô Trạng thái",
        "Trạng thái: Đang tạo / Chờ duyệt / Đã duyệt / Không duyệt",
        "- Mỗi lần lọc ra đúng số phiếu tương ứng: 4 / 3 / 20 / 2\n"
        "- ⚠️ Thứ tự trong ô chọn là Đang tạo → Chờ duyệt → Đã duyệt → Không duyệt",
    ),
    (
        7,
        "Lọc theo Tên/mã hàng hóa",
        "P0",
        "Hàng \"Cáp mạng CAT6\" nằm trong 3 phiếu.",
        "1. Nhập Cáp mạng vào ô Tên/mã hàng hóa",
        "Tên/mã hàng hóa: Cáp mạng",
        "- Danh sách còn 3 phiếu\n"
        "- Mở từng phiếu đều thấy dòng hàng Cáp mạng CAT6 trong bảng chi tiết",
    ),
    (
        8,
        "Lọc theo Người nhận",
        "P0",
        "Nhân viên Nguyễn Văn A là người nhận của 5 phiếu.",
        "1. Chọn Người nhận = Nguyễn Văn A",
        "Người nhận: Nguyễn Văn A",
        "- Danh sách còn 5 phiếu, cột Người nhận đều là Nguyễn Văn A",
    ),
    (
        9,
        "Lọc theo Người tạo",
        "P0",
        "Nhân viên Trần Thị B đã lập 7 phiếu.",
        "1. Chọn Người tạo = Trần Thị B",
        "Người tạo: Trần Thị B",
        "- Danh sách còn 7 phiếu, cột Người tạo đều là Trần Thị B",
    ),
    (
        10,
        "Lọc khoảng Ngày tạo",
        "P0",
        "Có 6 phiếu lập trong tháng 7, 4 phiếu lập trong tháng 8.",
        "1. Nhập Ngày tạo từ = 01/07/2026, Ngày tạo đến = 31/07/2026",
        "Ngày tạo từ: 01/07/2026 · Ngày tạo đến: 31/07/2026",
        "- Danh sách còn 6 phiếu\n"
        "- Bao gồm cả phiếu lập đúng ngày 01/07/2026 và ngày 31/07/2026\n"
        "- Không lẫn phiếu tháng 8",
    ),
    (
        11,
        "Chỉ nhập Ngày tạo từ",
        "P1",
        "Như trên.",
        "1. Nhập Ngày tạo từ = 01/08/2026, để trống ô đến",
        "Ngày tạo từ: 01/08/2026",
        "- Danh sách hiện mọi phiếu lập từ 01/08/2026 trở đi\n"
        "- Không báo lỗi vì thiếu ô đến",
    ),
    (
        12,
        "Nhập Ngày tạo từ lớn hơn Ngày tạo đến",
        "P1",
        "Như trên.",
        "1. Nhập Ngày tạo từ = 31/08/2026, Ngày tạo đến = 01/08/2026",
        "Ngày tạo từ: 31/08/2026 · Ngày tạo đến: 01/08/2026",
        "- Danh sách trả về rỗng kèm dòng \"Không có dữ liệu phù hợp bộ lọc.\"\n"
        "- Không treo trang, không báo lỗi kỹ thuật",
    ),
    (
        13,
        "Tìm nhanh theo số phiếu",
        "P0",
        "Tồn tại phiếu TPE_CHNT_002.",
        "1. Nhập TPE_CHNT_002 vào ô tìm nhanh\n"
        "2. Chờ tối thiểu 3 giây cho danh sách tải xong",
        "Tìm nhanh: TPE_CHNT_002",
        "- Danh sách còn đúng 1 dòng\n"
        "- ⚠️ Chờ đủ 3 giây rồi hãy đối chiếu; kết quả có thể lệch một nhịp nếu đọc quá sớm",
    ),
    (
        14,
        "Tìm nhanh theo tên người tạo",
        "P0",
        "Trần Thị B đã lập 7 phiếu.",
        "1. Nhập Trần Thị B vào ô tìm nhanh",
        "Tìm nhanh: Trần Thị B",
        "- Danh sách hiện 7 phiếu của Trần Thị B\n"
        "- Dòng khớp sát nhất đứng trên đầu",
    ),
    (
        15,
        "Tìm nhanh với chuỗi không tồn tại",
        "P2",
        "—",
        "1. Nhập chuỗi zzzz vào ô tìm nhanh",
        "Tìm nhanh: zzzz",
        "- Danh sách rỗng kèm dòng \"Không có dữ liệu phù hợp bộ lọc.\"\n"
        "- Bấm Làm mới thì danh sách trở lại đầy đủ",
    ),
    (
        16,
        "Nút Làm mới xóa hết điều kiện lọc",
        "P0",
        "Đang lọc: Công ty = công ty 1, Trạng thái = Chờ duyệt, ô tìm nhanh có chữ.",
        "1. Bấm nút Làm mới\n"
        "2. Quan sát các ô lọc và lưới",
        "—",
        "- Mọi ô lọc và ô tìm nhanh trở về trống\n"
        "- Danh sách TỰ TẢI LẠI đầy đủ theo phạm vi quyền, không cần thao tác thêm\n"
        "- ⚠️ Trang trở về trang 1",
    ),
    (
        17,
        "Hệ thống nhớ bộ lọc khi quay lại màn",
        "P1",
        "Đang lọc Trạng thái = Đã duyệt.",
        "1. Bấm vào một phiếu để xem chi tiết\n"
        "2. Bấm Quay lại",
        "—",
        "- Màn danh sách giữ nguyên điều kiện Trạng thái = Đã duyệt và đúng trang đang xem trước đó",
    ),
    (
        18,
        "Cài đặt bộ lọc: bật / tắt và sắp xếp ô lọc",
        "P1",
        "Tài khoản A.",
        "1. Mở popup Cài đặt bộ lọc\n"
        "2. Tắt ô Người nhận, kéo ô Trạng thái lên đầu\n"
        "3. Lưu và tải lại trang",
        "—",
        "- Ô Người nhận không còn hiện\n"
        "- Ô Trạng thái đứng đầu khối lọc\n"
        "- Cấu hình giữ nguyên sau khi tải lại trang (lưu theo từng người dùng)\n"
        "- ⚠️ Nếu QA báo \"thiếu ô lọc\" thì kiểm tra popup này trước khi kết luận là lỗi",
    ),
    (
        19,
        "Thu gọn / mở rộng khối bộ lọc",
        "P2",
        "—",
        "1. Bấm mũi tên thu gọn khối Bộ lọc danh sách\n"
        "2. Chuyển màn rồi quay lại",
        "—",
        "- Khối lọc thu gọn, chỉ còn ô tìm nhanh\n"
        "- Trạng thái thu gọn được nhớ lại khi quay lại màn",
    ),
    (
        20,
        "Kết hợp nhiều ô lọc cùng lúc",
        "P0",
        "Công ty 1, Trạng thái Đã duyệt, người tạo Trần Thị B: có đúng 2 phiếu.",
        "1. Chọn đồng thời Công ty = công ty 1, Trạng thái = Đã duyệt, Người tạo = Trần Thị B",
        "—",
        "- Danh sách còn đúng 2 phiếu thỏa cả 3 điều kiện\n"
        "- Dòng \"Hiển thị a–b / N phiếu\" báo N = 2",
    ),
]

SEC_III = [
    (
        1,
        "Sắp xếp tăng dần theo Số phiếu",
        "P0",
        "Tài khoản A, danh sách trên 800 phiếu.",
        "1. Bấm tiêu đề cột Số phiếu 1 lần",
        "—",
        "- Mũi tên trên tiêu đề đổi sang chiều tăng dần\n"
        "- Dòng đầu là số phiếu nhỏ nhất theo thứ tự chữ cái (ví dụ TPE_CHNT_002)",
    ),
    (
        2,
        "Sắp xếp giảm dần theo Số phiếu",
        "P0",
        "Như trên.",
        "1. Bấm tiêu đề cột Số phiếu lần thứ hai",
        "—",
        "- Mũi tên đổi sang chiều giảm dần\n"
        "- Dòng đầu là số phiếu lớn nhất (ví dụ TPV_CHNT_853)\n"
        "- ⚠️ Đây là lỗi từng gặp: bấm lần 2 không đổi chiều. Phải kiểm cả biểu tượng mũi tên lẫn "
        "dữ liệu thật",
    ),
    (
        3,
        "Sắp xếp theo Ngày tạo hai chiều",
        "P0",
        "Như trên.",
        "1. Bấm tiêu đề cột Ngày tạo lần 1\n"
        "2. Bấm lần 2",
        "—",
        "- Lần 1: dòng đầu là phiếu cũ nhất (ví dụ 06/08/2025 08:37)\n"
        "- Lần 2: dòng đầu là phiếu mới nhất (ví dụ 27/07/2026 17:15)\n"
        "- Cột hiện đủ ngày và giờ phút",
    ),
    (
        4,
        "Các cột không sắp xếp được",
        "P2",
        "—",
        "1. Bấm tiêu đề cột Người nhận, Người tạo, Trạng thái",
        "—",
        "- Không có mũi tên sắp xếp, thứ tự danh sách không đổi\n"
        "- Không báo lỗi",
    ),
    (
        5,
        "Sắp xếp vẫn giữ khi đổi trang",
        "P1",
        "Đang sắp xếp giảm dần theo Ngày tạo, có ít nhất 3 trang.",
        "1. Sang trang 2, rồi trang 3",
        "—",
        "- Thứ tự giảm dần theo Ngày tạo được giữ liên tục qua các trang\n"
        "- Không có phiếu bị lặp giữa 2 trang liền nhau",
    ),
    (
        6,
        "Sắp xếp kết hợp bộ lọc",
        "P1",
        "Lọc Trạng thái = Đã duyệt (20 phiếu).",
        "1. Lọc Trạng thái = Đã duyệt\n"
        "2. Sắp xếp giảm dần theo Ngày tạo",
        "—",
        "- Vẫn đúng 20 phiếu, không phiếu nào ngoài trạng thái Đã duyệt lọt vào\n"
        "- Thứ tự đúng chiều giảm dần",
    ),
    (
        7,
        "Đổi số dòng trên trang",
        "P0",
        "Danh sách trên 100 phiếu.",
        "1. Đổi số dòng mỗi trang sang 50\n"
        "2. Quan sát lưới và dòng \"Hiển thị a–b / N phiếu\"",
        "Số dòng: 50",
        "- Lưới hiện 50 dòng\n"
        "- Dòng thống kê báo \"Hiển thị 1–50 / N phiếu\"\n"
        "- Trang tự về trang 1",
    ),
    (
        8,
        "Chuyển trang giữ nguyên bộ lọc",
        "P0",
        "Đang lọc Công ty = công ty 1, kết quả nhiều hơn 1 trang.",
        "1. Sang trang 2",
        "—",
        "- Ô lọc Công ty vẫn giữ giá trị công ty 1\n"
        "- Dữ liệu trang 2 vẫn thuộc công ty 1\n"
        "- ⚠️ Đổi trang KHÔNG được coi là đổi bộ lọc, không được tự nhảy về trang 1",
    ),
    (
        9,
        "Số thứ tự chạy liên tục qua các trang",
        "P1",
        "Số dòng mỗi trang là 20.",
        "1. Xem STT dòng cuối trang 1 và dòng đầu trang 2",
        "—",
        "- Dòng cuối trang 1 là 20, dòng đầu trang 2 là 21\n"
        "- Không đánh lại từ 1 ở mỗi trang",
    ),
    (
        10,
        "Ô trống hiển thị đúng quy ước",
        "P1",
        "Có phiếu chưa duyệt (chưa có người duyệt) và phiếu không nhập ghi chú.",
        "1. Bật cột Ghi chú và Người duyệt\n"
        "2. Xem các dòng đó",
        "—",
        "- Ô không có dữ liệu để trống theo đúng quy ước hiện hành của hệ thống\n"
        "- Không hiện chữ null hay giá trị kỹ thuật",
    ),
    (
        11,
        "Nhãn trạng thái đúng màu",
        "P1",
        "Có đủ 4 trạng thái trong danh sách.",
        "1. Quan sát cột Trạng thái",
        "—",
        "- Đang tạo: nhãn xám · Chờ duyệt: nhãn vàng · Đã duyệt: nhãn xanh lá · Không duyệt: nhãn đỏ\n"
        "- ⚠️ Đang tạo là bản nháp nên phải xám, không được đỏ",
    ),
    (
        12,
        "Cột Hành động hiện đúng nút theo quyền",
        "P0",
        "Tài khoản E (Kế toán kho) xem 1 phiếu Chờ duyệt của người khác và 1 phiếu nháp của mình.",
        "1. Xem cột Hành động của 2 dòng đó",
        "—",
        "- Phiếu nháp của mình: có Sửa và Xóa\n"
        "- Phiếu Chờ duyệt của người khác: có Duyệt, không có Sửa / Xóa\n"
        "- Nút không dùng được thì ẨN hẳn, không hiện nút mờ",
    ),
    (
        13,
        "Menu ba chấm ở cột Hành động",
        "P1",
        "Danh sách có phiếu bất kỳ.",
        "1. Bấm biểu tượng ba chấm ở cột Hành động",
        "—",
        "- Menu hiện thêm 2 mục: In và Lịch sử\n"
        "- Bấm In mở tab mới với bản in phiếu\n"
        "- Bấm Lịch sử mở cửa sổ Lịch sử thay đổi của đúng phiếu đó",
    ),
    (
        14,
        "Hành động Duyệt trên danh sách dẫn tới màn chi tiết",
        "P0",
        "Tài khoản E, dòng phiếu Chờ duyệt có nút Duyệt.",
        "1. Bấm nút Duyệt ở cột Hành động",
        "—",
        "- Hệ thống mở màn CHI TIẾT của phiếu, KHÔNG duyệt luôn từ danh sách\n"
        "- ⚠️ Cố ý như vậy vì duyệt là thao tác ghi tồn thật, người duyệt phải xem hàng hóa trước",
    ),
]

SEC_IV = [
    (
        1,
        "Mở màn Tạo mới",
        "P0",
        "Tài khoản B đang có tồn hàng nhập thẳng.",
        "1. Bấm nút Tạo mới",
        "—",
        "- Tiêu đề trang là \"Thêm phiếu chuyển hàng nhập thẳng\"\n"
        "- Có khối THÔNG TIN CHUNG (Người nhận, Phòng ban, Ghi chú) và khối CHI TIẾT\n"
        "- ⚠️ Màn Tạo mới KHÔNG có ô Số phiếu, Trạng thái, Người duyệt — 3 ô này chỉ hiện ở màn "
        "Chi tiết sau khi phiếu được lưu\n"
        "- Góc phải khối THÔNG TIN CHUNG hiện tên người lập và ngày lập\n"
        "- Bảng Chi tiết trống với dòng \"Chưa có hàng hóa\"\n"
        "- Cuối trang có nút Lưu nháp, Lưu và gửi duyệt, Quay lại",
    ),
    (
        2,
        "Ô Người nhận chỉ liệt kê nhân viên cùng công ty, trừ chính mình",
        "P0",
        "Tài khoản B thuộc công ty 1; công ty 1 có 40 nhân viên; công ty 4 có nhân viên khác.",
        "1. Mở ô Người nhận, gõ vài ký tự để tìm",
        "—",
        "- Chỉ hiện nhân viên công ty 1\n"
        "- KHÔNG có tên của chính tài khoản B trong danh sách\n"
        "- Không hiện nhân viên công ty 4",
    ),
    (
        3,
        "Chọn Người nhận thì tự điền Phòng ban",
        "P0",
        "Nhân viên Nguyễn Văn A thuộc phòng Kỹ thuật.",
        "1. Chọn Người nhận = Nguyễn Văn A",
        "Người nhận: Nguyễn Văn A",
        "- Ô Phòng ban tự điền \"Kỹ thuật\"\n"
        "- Ô Phòng ban ở trạng thái khóa, không sửa được\n"
        "- ⚠️ Ô khóa phải có dấu hiệu nhận biết để người dùng không tưởng là ô trống bị lỗi",
    ),
    (
        4,
        "Mở cửa sổ chọn hàng từ tồn nhập thẳng",
        "P0",
        "Tài khoản B đang giữ 8 mặt hàng nhập thẳng.",
        "1. Bấm nút thêm hàng hóa ở khối Chi tiết",
        "—",
        "- Mở cửa sổ với bảng gồm cột: STT · Mã hàng hóa · Tên hàng hóa · Hãng sản xuất · ĐVT · "
        "Số lượng tồn\n"
        "- Liệt kê đúng 8 mặt hàng đang tồn của tài khoản B\n"
        "- Có ô Tìm hàng hóa với gợi ý \"Nhập tên hoặc mã hàng hóa\"",
    ),
    (
        5,
        "Tìm hàng trong cửa sổ chọn hàng",
        "P1",
        "Trong 8 mặt hàng có 2 mặt hàng chứa chữ \"Cáp\".",
        "1. Nhập Cáp vào ô Tìm hàng hóa",
        "Tìm hàng hóa: Cáp",
        "- Bảng còn 2 dòng\n"
        "- Xóa ô tìm thì quay lại đủ 8 dòng",
    ),
    (
        6,
        "Chọn nhiều hàng cùng lúc",
        "P0",
        "Cửa sổ chọn hàng đang mở với 8 dòng.",
        "1. Tick 3 dòng\n"
        "2. Bấm nút áp dụng",
        "—",
        "- Cửa sổ đóng lại\n"
        "- Bảng Chi tiết có đúng 3 dòng vừa chọn, kèm Tên hàng, Mã hàng, ĐVT và Tồn hiện có",
    ),
    (
        7,
        "Hàng đã có trong phiếu bị khóa chọn lại",
        "P1",
        "Bảng Chi tiết đã có hàng Cáp mạng CAT6.",
        "1. Mở lại cửa sổ chọn hàng\n"
        "2. Rê chuột lên dòng Cáp mạng CAT6",
        "—",
        "- Ô tick của dòng đó bị khóa ngay từ đầu\n"
        "- Rê chuột hiện chú thích \"Hàng hóa đã có trong phiếu\"\n"
        "- ⚠️ Khác hệ thống cũ: bên cũ vẫn tick được rồi mới báo lỗi sau khi bấm",
    ),
    (
        8,
        "Nhập số lượng và xem SL theo ĐV cơ bản",
        "P0",
        "Dòng hàng có đơn vị Thùng, hệ số quy đổi 1 Thùng = 10 Cái, tồn 200 Cái.",
        "1. Nhập Số lượng = 5",
        "Số lượng: 5",
        "- Ô SL theo ĐV cơ bản hiện 50\n"
        "- Ô Tồn hiện có hiện 20 (200 quy về đơn vị Thùng)",
    ),
    (
        9,
        "Đổi đơn vị tính thì tính lại số lượng",
        "P0",
        "Như trên, đang là Thùng, số lượng 5.",
        "1. Đổi ĐVT sang Cái",
        "ĐVT: Cái",
        "- Số lượng và SL theo ĐV cơ bản được tính lại theo hệ số mới\n"
        "- Ô Tồn hiện có đổi sang 200\n"
        "- Không còn số lượng cũ tính theo đơn vị cũ",
    ),
    (
        10,
        "Xóa một dòng hàng khỏi phiếu",
        "P1",
        "Bảng Chi tiết có 3 dòng.",
        "1. Bấm biểu tượng xóa dòng ở dòng thứ 2",
        "—",
        "- Dòng thứ 2 biến mất, còn 2 dòng\n"
        "- STT của các dòng còn lại được đánh lại liên tục 1, 2",
    ),
    (
        11,
        "Lưu nháp chỉ cần Người nhận",
        "P0",
        "Tài khoản B, form Tạo mới trống.",
        "1. Chỉ chọn Người nhận\n"
        "2. Bấm Lưu nháp",
        "Người nhận: Nguyễn Văn A",
        "- Lưu thành công, thông báo Lưu phiếu thành công\n"
        "- Hệ thống quay về màn danh sách\n"
        "- Phiếu mới có Số phiếu tự sinh và trạng thái Đang tạo\n"
        "- ⚠️ Bảng hàng hóa để trống vẫn lưu được - đúng thiết kế",
    ),
    (
        12,
        "Lưu nháp khi bỏ trống Người nhận",
        "P0",
        "Form Tạo mới hoàn toàn trống.",
        "1. Bấm Lưu nháp mà không chọn gì",
        "—",
        "- Ô Người nhận viền đỏ, dưới ô hiện \"Bắt buộc phải nhập\"\n"
        "- Thông báo góc màn hình là câu \"Vui lòng kiểm tra lại dữ liệu nhập\"\n"
        "- ⚠️ KHÔNG được hiện câu Lưu phiếu thất bại (nghe như lỗi máy chủ)\n"
        "- Màn tự cuộn tới ô lỗi đầu tiên",
    ),
    (
        13,
        "Lưu và gửi duyệt đầy đủ thông tin",
        "P0",
        "Tài khoản B, tồn hàng Cáp mạng CAT6 là 100 Cái.",
        "1. Chọn Người nhận = Nguyễn Văn A\n"
        "2. Thêm hàng Cáp mạng CAT6, số lượng 10\n"
        "3. Nhập Ghi chú\n"
        "4. Bấm Lưu và gửi duyệt",
        "Số lượng: 10 · Ghi chú: Chuyển hàng dự án X",
        "- Lưu thành công, quay về màn danh sách\n"
        "- Phiếu mới ở trạng thái Chờ duyệt\n"
        "- Người có quyền Kế toán kho cùng công ty nhận được thông báo có phiếu cần duyệt",
    ),
    (
        14,
        "Gửi duyệt khi chưa có dòng hàng nào",
        "P0",
        "Đã chọn Người nhận, bảng Chi tiết trống.",
        "1. Bấm Lưu và gửi duyệt",
        "—",
        "- Hệ thống chặn, báo lỗi ở khối Danh sách hàng hoá là bắt buộc phải nhập\n"
        "- Phiếu không được tạo",
    ),
    (
        15,
        "Chọn Người nhận là chính mình",
        "P0",
        "Tài khoản B.",
        "1. Dùng công cụ kiểm thử gọi thẳng chức năng Lưu, đặt người nhận là chính tài khoản B",
        "—",
        "- Hệ thống chặn, báo \"Người nhận phải khác người lập phiếu\"\n"
        "- ⚠️ Trên giao diện ô Người nhận vốn đã loại tên mình, đây là lớp chặn thứ hai",
    ),
    (
        16,
        "Số phiếu sinh đúng định dạng",
        "P0",
        "Tài khoản B thuộc công ty có mã TPE.",
        "1. Lưu nháp một phiếu mới\n"
        "2. Xem cột Số phiếu trên danh sách",
        "—",
        "- Số phiếu có dạng TPE_CHNT_ kèm số thứ tự 3 chữ số trở lên\n"
        "- ⚠️ Định dạng phải giống hệt số phiếu sinh bên cổng ERP, hai cổng không được lệch quy tắc",
    ),
    (
        17,
        "Cảnh báo khi rời màn lúc chưa lưu",
        "P1",
        "Đã nhập Người nhận và 1 dòng hàng, chưa bấm lưu.",
        "1. Bấm nút Quay lại",
        "—",
        "- Hệ thống hỏi xác nhận rời trang vì dữ liệu chưa lưu\n"
        "- Chọn ở lại thì dữ liệu đang nhập còn nguyên",
    ),
    (
        18,
        "Không cảnh báo sau khi đã lưu",
        "P1",
        "Vừa Lưu nháp thành công.",
        "1. Bấm Quay lại ngay sau khi lưu",
        "—",
        "- Không hỏi xác nhận, về thẳng danh sách",
    ),
    (
        19,
        "Ghi chú vượt quá độ dài cho phép",
        "P1",
        "Form Tạo mới.",
        "1. Dán vào ô Ghi chú một đoạn dài hơn 255 ký tự\n"
        "2. Bấm Lưu nháp",
        "Ghi chú: chuỗi 300 ký tự",
        "- Hệ thống báo \"Không được nhập quá 255 ký tự\" ngay tại ô Ghi chú\n"
        "- Phiếu không được lưu, nội dung đã nhập vẫn còn trên form",
    ),
    (
        20,
        "Người lập không có tồn hàng nhập thẳng nào",
        "P1",
        "Tài khoản mới, chưa từng nhận hàng nhập thẳng.",
        "1. Mở màn Tạo mới\n"
        "2. Bấm nút thêm hàng hóa",
        "—",
        "- Cửa sổ chọn hàng mở ra nhưng không có dòng nào\n"
        "- Không báo lỗi kỹ thuật, chỉ là danh sách rỗng",
    ),
]

SEC_V = [
    (
        1,
        "Sửa phiếu ở trạng thái Đang tạo",
        "P0",
        "Tài khoản B có phiếu nháp TPE_CHNT_871.",
        "1. Bấm Sửa ở cột Hành động\n"
        "2. Đổi Người nhận và thêm 1 dòng hàng\n"
        "3. Bấm Lưu nháp",
        "—",
        "- Form nạp đúng dữ liệu cũ\n"
        "- Lưu thành công, quay về danh sách\n"
        "- Mở lại phiếu thấy dữ liệu đã đổi",
    ),
    (
        2,
        "Sửa phiếu ở trạng thái Không duyệt",
        "P0",
        "Tài khoản B có phiếu bị từ chối.",
        "1. Mở phiếu, bấm Sửa\n"
        "2. Sửa số lượng rồi bấm Lưu và gửi duyệt",
        "—",
        "- Sửa được\n"
        "- Sau khi gửi duyệt, phiếu chuyển sang Chờ duyệt\n"
        "- Lý do từ chối cũ vẫn xem được ở khối Lịch sử thay đổi",
    ),
    (
        3,
        "Không sửa được phiếu đang Chờ duyệt",
        "P0",
        "Tài khoản B có phiếu đang Chờ duyệt.",
        "1. Xem cột Hành động của dòng đó\n"
        "2. Mở chi tiết phiếu",
        "—",
        "- Không có nút Sửa ở cả danh sách lẫn màn chi tiết\n"
        "- Gọi thẳng chức năng Sửa bằng công cụ kiểm thử cũng bị chặn",
    ),
    (
        4,
        "Không sửa được phiếu đã duyệt",
        "P0",
        "Phiếu ở trạng thái Đã duyệt.",
        "1. Mở chi tiết phiếu\n"
        "2. Dùng công cụ kiểm thử gọi thẳng chức năng Sửa",
        "—",
        "- Không có nút Sửa trên giao diện\n"
        "- Gọi thẳng chức năng cũng bị chặn, dữ liệu phiếu không đổi",
    ),
    (
        5,
        "Cửa sổ chọn hàng khi sửa phiếu lấy tồn của NGƯỜI LẬP",
        "P0",
        "Phiếu do tài khoản B lập. Tài khoản B mở lại phiếu của mình để sửa; tồn của B khác tồn của "
        "người đang đăng nhập khác.",
        "1. Mở màn Sửa\n"
        "2. Bấm thêm hàng hóa, đối chiếu danh sách hàng với tồn của người lập phiếu",
        "—",
        "- Danh sách hàng đúng bằng tồn của người LẬP phiếu\n"
        "- ⚠️ Đây là lỗi đã sửa so với hệ thống cũ: bên cũ cửa sổ lấy tồn của người đang đăng nhập "
        "trong khi lúc lưu lại kiểm theo tồn của người lập, dẫn tới chọn được hàng rồi không lưu được",
    ),
    (
        6,
        "Sửa số lượng vượt tồn hiện có",
        "P0",
        "Dòng hàng có tồn 208 theo đơn vị đang chọn.",
        "1. Sửa Số lượng thành 209\n"
        "2. Bấm Lưu nháp",
        "Số lượng: 209",
        "- Ô Số lượng GIỮ NGUYÊN 209, không tự kéo về 208\n"
        "- Dưới ô hiện lỗi đỏ \"Chỉ còn 208 theo đơn vị đang chọn\"\n"
        "- Bấm Lưu không gửi đi bất cứ yêu cầu nào\n"
        "- ⚠️ Tuyệt đối không được tự sửa con số người dùng nhập",
    ),
    (
        7,
        "Hai dòng cùng một hàng, tổng vượt tồn",
        "P0",
        "Tồn hàng Cáp mạng CAT6 là 100 Cái.",
        "1. Thêm 2 dòng cùng hàng Cáp mạng CAT6, mỗi dòng 60 Cái\n"
        "2. Bấm Lưu và gửi duyệt",
        "Dòng 1: 60 · Dòng 2: 60",
        "- Hệ thống chặn, báo hàng \"Cáp mạng CAT6\" không đủ số lượng\n"
        "- ⚠️ Hệ thống cũ chỉ so từng dòng nên cho lưu, tới lúc duyệt mới lỗi",
    ),
    (
        8,
        "Hai dòng cùng một hàng, tổng vừa đủ tồn",
        "P1",
        "Tồn hàng Cáp mạng CAT6 là 100 Cái.",
        "1. Thêm 2 dòng cùng hàng đó, mỗi dòng 50 Cái\n"
        "2. Bấm Lưu và gửi duyệt",
        "Dòng 1: 50 · Dòng 2: 50",
        "- Lưu thành công\n"
        "- Phiếu chuyển Chờ duyệt",
    ),
    (
        9,
        "Sửa phiếu của người khác",
        "P0",
        "Tài khoản C mở phiếu do người khác lập, phiếu đang ở trạng thái Đang tạo.",
        "1. Mở chi tiết phiếu",
        "—",
        "- Không có nút Sửa và nút Xóa (chỉ người lập mới có)\n"
        "- ⚠️ Bản nháp của người khác vốn không hiện trên danh sách, chỉ tới được bằng đường dẫn trực tiếp",
    ),
    (
        10,
        "Mở màn Sửa của phiếu vừa bị xóa",
        "P1",
        "Phiếu vừa bị người khác xóa trong khi tab này còn mở.",
        "1. Bấm nút Sửa trên tab cũ",
        "—",
        "- Hệ thống báo \"Không tìm thấy dữ liệu\" rồi quay về màn danh sách\n"
        "- ⚠️ Không được hiện câu báo lỗi kỹ thuật tiếng Anh",
    ),
]

SEC_VI = [
    (
        1,
        "Mở màn Chi tiết",
        "P0",
        "Phiếu TPE_CHNT_870 ở trạng thái Đã duyệt.",
        "1. Bấm số phiếu trên danh sách",
        "—",
        "- Tiêu đề trang là \"Chi tiết phiếu chuyển hàng nhập thẳng: TPE_CHNT_870\"\n"
        "- Mọi ô ở dạng chỉ đọc, không sửa được\n"
        "- Có đủ Số phiếu, Trạng thái, Người duyệt",
    ),
    (
        2,
        "Khối Ghi chú duyệt",
        "P1",
        "Phiếu bị từ chối với lý do \"Hàng đã xuất cho khách\".",
        "1. Mở chi tiết phiếu đó",
        "—",
        "- Có khối \"Ghi chú duyệt\" hiện đúng nội dung lý do\n"
        "- Xuống dòng trong lý do được giữ nguyên",
    ),
    (
        3,
        "Khối Ghi chú duyệt không hiện khi chưa có ý kiến",
        "P2",
        "Phiếu đang Chờ duyệt, chưa ai duyệt.",
        "1. Mở chi tiết",
        "—",
        "- Không có khối Ghi chú duyệt (không hiện khối trống)",
    ),
    (
        4,
        "Bộ nút cuối màn chi tiết theo quyền",
        "P0",
        "Tài khoản E (Kế toán kho cùng công ty), phiếu đang Chờ duyệt do người khác lập.",
        "1. Mở chi tiết, xem hàng nút cuối trang",
        "—",
        "- Thứ tự nút: Duyệt (xanh) → In (trắng) → Từ chối (đỏ) → Quay lại\n"
        "- Không có nút Sửa và nút Xóa vì không phải người lập\n"
        "- ⚠️ Nút In phải là nút TRẮNG và chữ phải là \"Từ chối\", không phải \"Không duyệt\"",
    ),
    (
        5,
        "Bộ nút với người lập phiếu",
        "P0",
        "Tài khoản B mở phiếu nháp của chính mình.",
        "1. Mở chi tiết",
        "—",
        "- Có nút Sửa, In, Xóa (đỏ), Quay lại\n"
        "- Không có nút Duyệt / Từ chối",
    ),
    (
        6,
        "Bảng hàng hóa ở màn chi tiết",
        "P0",
        "Phiếu có 3 dòng hàng.",
        "1. Xem khối Chi tiết",
        "—",
        "- Bảng có cột: STT · Tên hàng · Mã hàng · ĐVT · Số lượng · SL theo ĐV cơ bản · Tồn hiện có\n"
        "- Số lượng hiện đúng định dạng số chuẩn quốc tế\n"
        "- Không có nút thêm / xóa dòng",
    ),
    (
        7,
        "Nút Quay lại",
        "P1",
        "Vào chi tiết từ trang 2 của danh sách.",
        "1. Bấm Quay lại",
        "—",
        "- Về màn danh sách, giữ nguyên bộ lọc và trang đang xem trước đó",
    ),
    (
        8,
        "Mở chi tiết phiếu không tồn tại",
        "P0",
        "Dùng một mã phiếu không có trong hệ thống trên đường dẫn.",
        "1. Dán đường dẫn chi tiết với mã phiếu không tồn tại",
        "—",
        "- Hệ thống báo \"Không tìm thấy dữ liệu\" rồi tự quay về màn danh sách\n"
        "- ⚠️ Không được hiện câu báo lỗi kỹ thuật tiếng Anh của hệ thống",
    ),
]

SEC_VII = [
    (
        1,
        "Duyệt phiếu hợp lệ",
        "P0",
        "Tài khoản E (Kế toán kho công ty 1). Phiếu Chờ duyệt chuyển 10 Cái hàng Cáp mạng CAT6 từ B "
        "sang Nguyễn Văn A. Trước khi duyệt: tồn của B là 100 Cái, tồn của A là 0.",
        "1. Mở chi tiết phiếu\n"
        "2. Bấm Duyệt\n"
        "3. Xác nhận ở cửa sổ hỏi lại\n"
        "4. Kiểm tra lại tồn hàng nhập thẳng của B và của A",
        "—",
        "- Thông báo Duyệt phiếu thành công\n"
        "- Hệ thống quay về màn danh sách\n"
        "- Phiếu chuyển sang trạng thái Đã duyệt, cột Người duyệt là tài khoản E\n"
        "- Tồn của B còn 90 Cái, tồn của A tăng thành 10 Cái\n"
        "- Người lập phiếu nhận được thông báo phiếu đã được duyệt",
    ),
    (
        2,
        "Có cửa sổ xác nhận trước khi duyệt",
        "P0",
        "Phiếu Chờ duyệt.",
        "1. Bấm Duyệt\n"
        "2. Chọn hủy ở cửa sổ xác nhận",
        "—",
        "- Có cửa sổ hỏi lại trước khi duyệt\n"
        "- Chọn hủy thì phiếu vẫn Chờ duyệt, tồn không đổi",
    ),
    (
        3,
        "Duyệt khi hàng đã không còn đủ tồn",
        "P0",
        "Phiếu lập chuyển 50 Cái. Sau khi lập, người lập đã chuyển bớt nên chỉ còn 20 Cái.",
        "1. Bấm Duyệt",
        "—",
        "- Hệ thống chặn, báo rõ tên hàng, cần bao nhiêu và hiện chỉ còn bao nhiêu theo đơn vị cơ bản\n"
        "- Phiếu VẪN ở trạng thái Chờ duyệt, tồn không thay đổi\n"
        "- ⚠️ KHÔNG được hiện câu \"Lỗi máy chủ\" - đây là lỗi nghiệp vụ, phải nói rõ hàng nào thiếu",
    ),
    (
        4,
        "Duyệt phiếu không còn dòng hàng nào có số lượng",
        "P0",
        "Phiếu Chờ duyệt nhưng mọi dòng hàng đều có số lượng bằng 0.",
        "1. Bấm Duyệt",
        "—",
        "- Hệ thống chặn, báo \"Phiếu không có dòng hàng hóa nào để chuyển.\"\n"
        "- Phiếu KHÔNG chuyển sang Đã duyệt\n"
        "- ⚠️ Trước đây phiếu kiểu này duyệt xong mà tồn không đổi - đúng hiện tượng QA từng báo",
    ),
    (
        5,
        "Từ chối phiếu có nhập lý do",
        "P0",
        "Tài khoản E, phiếu Chờ duyệt.",
        "1. Bấm Từ chối\n"
        "2. Nhập lý do \"Hàng đã xuất cho khách\"\n"
        "3. Bấm Từ chối trong cửa sổ",
        "Lý do từ chối: Hàng đã xuất cho khách",
        "- Thông báo Đã từ chối phiếu\n"
        "- Quay về màn danh sách, phiếu chuyển trạng thái Không duyệt\n"
        "- Tồn hàng của cả hai bên KHÔNG thay đổi\n"
        "- Người lập nhận được thông báo phiếu bị từ chối",
    ),
    (
        6,
        "Từ chối mà bỏ trống lý do",
        "P0",
        "Cửa sổ Từ chối phiếu đang mở.",
        "1. Bấm Từ chối khi ô lý do còn trống",
        "—",
        "- Ô lý do viền đỏ, hiện \"Bắt buộc phải nhập lý do từ chối\"\n"
        "- Cửa sổ không đóng, phiếu vẫn Chờ duyệt",
    ),
    (
        7,
        "Đóng cửa sổ Từ chối",
        "P2",
        "Đã gõ dở lý do.",
        "1. Bấm nút Đóng",
        "—",
        "- Cửa sổ đóng, phiếu không đổi trạng thái\n"
        "- Mở lại cửa sổ thì ô lý do sạch, không giữ nội dung gõ dở gây hiểu nhầm",
    ),
    (
        8,
        "Duyệt phiếu đã duyệt rồi",
        "P0",
        "Phiếu ở trạng thái Đã duyệt, mở sẵn trên một tab cũ.",
        "1. Trên tab cũ bấm Duyệt lần nữa",
        "—",
        "- Hệ thống từ chối, không duyệt lần hai\n"
        "- Tồn KHÔNG bị trừ thêm lần nữa\n"
        "- ⚠️ Đây là điểm nguy hiểm nhất của màn: trừ tồn hai lần không hoàn tác được",
    ),
    (
        9,
        "Từ chối phiếu đã duyệt",
        "P1",
        "Phiếu Đã duyệt.",
        "1. Dùng công cụ kiểm thử gọi thẳng chức năng Từ chối",
        "—",
        "- Bị chặn, phiếu giữ nguyên trạng thái Đã duyệt\n"
        "- Tồn không bị hoàn lại",
    ),
    (
        10,
        "Trừ tồn theo thứ tự nhận trước dùng trước",
        "P0",
        "Người lập có 3 lô tồn cùng một hàng: lô cũ nhất 30, lô giữa 40, lô mới nhất 50. Phiếu chuyển "
        "60 theo đơn vị cơ bản.",
        "1. Duyệt phiếu\n"
        "2. Kiểm tra biến động từng lô tồn của người lập",
        "—",
        "- Lô cũ nhất bị trừ hết 30, lô giữa bị trừ 30 còn lại 10, lô mới nhất giữ nguyên 50\n"
        "- Người nhận có thêm một lô tồn 60\n"
        "- Mỗi lần trừ đều có ghi nhận biến động tương ứng",
    ),
    (
        11,
        "Đối chiếu tồn sau khi duyệt với cổng ERP",
        "P0",
        "Vừa duyệt một phiếu bên HRM.",
        "1. Mở màn báo cáo tồn hàng nhập thẳng bên cổng ERP với cùng nhân viên",
        "—",
        "- Số tồn của người lập và người nhận bên ERP khớp đúng với kết quả sau khi duyệt bên HRM\n"
        "- ⚠️ Hai cổng dùng chung dữ liệu, lệch là lỗi nghiêm trọng phải báo ngay",
    ),
]

SEC_VIII = [
    (
        1,
        "Xóa phiếu nháp của chính mình",
        "P0",
        "Tài khoản B có phiếu Đang tạo.",
        "1. Bấm Xóa ở cột Hành động\n"
        "2. Đọc cửa sổ xác nhận\n"
        "3. Bấm Xóa",
        "—",
        "- Cửa sổ hỏi \"Bạn có chắc muốn xóa phiếu <số phiếu>?\" với nút Xóa màu đỏ\n"
        "- Thông báo \"Xóa thành công.\"\n"
        "- Danh sách tự tải lại, phiếu không còn\n"
        "- Các dòng hàng hóa của phiếu cũng bị xóa theo, không để lại dữ liệu rác",
    ),
    (
        2,
        "Hủy thao tác xóa",
        "P1",
        "Như trên.",
        "1. Bấm Xóa rồi chọn hủy ở cửa sổ xác nhận",
        "—",
        "- Phiếu còn nguyên trên danh sách",
    ),
    (
        3,
        "Xóa phiếu ở trạng thái Không duyệt",
        "P1",
        "Tài khoản B có phiếu bị từ chối.",
        "1. Bấm Xóa",
        "—",
        "- Xóa được (trạng thái Không duyệt vẫn cho xóa)\n"
        "- Tồn hàng của cả hai bên không đổi",
    ),
    (
        4,
        "Không xóa được phiếu Chờ duyệt / Đã duyệt",
        "P0",
        "Phiếu ở trạng thái Chờ duyệt và phiếu Đã duyệt.",
        "1. Xem cột Hành động của cả hai dòng\n"
        "2. Dùng công cụ kiểm thử gọi thẳng chức năng Xóa cho phiếu Đã duyệt",
        "—",
        "- Không có nút Xóa trên giao diện ở cả hai phiếu\n"
        "- Gọi thẳng chức năng cũng bị chặn, phiếu còn nguyên\n"
        "- Tồn đã ghi nhận khi duyệt không bị mất",
    ),
    (
        5,
        "Xóa phiếu đã bị người khác xóa trước đó",
        "P1",
        "Phiếu vừa bị xóa ở tab khác.",
        "1. Trên tab cũ bấm Xóa",
        "—",
        "- Hệ thống báo dữ liệu đã thay đổi hoặc không tìm thấy phiếu\n"
        "- Danh sách được tải lại, không treo trang",
    ),
    (
        6,
        "Xóa xong quay về danh sách",
        "P1",
        "Đang ở màn chi tiết phiếu nháp của mình.",
        "1. Bấm Xóa ở cuối màn chi tiết, xác nhận",
        "—",
        "- Thông báo xóa thành công\n"
        "- Hệ thống đưa về màn danh sách, không đứng lại ở màn chi tiết của phiếu vừa xóa",
    ),
]

SEC_IX = [
    (
        1,
        "In một phiếu",
        "P0",
        "Phiếu TPE_CHNT_870 có 3 dòng hàng.",
        "1. Mở chi tiết phiếu, bấm nút In",
        "—",
        "- Mở tab mới hiện bản in phiếu theo đúng biểu mẫu của hệ thống\n"
        "- Có đủ thông tin chung, bảng hàng hóa và khối ký\n"
        "- Nút In nằm bên phải theo chuẩn màn in",
    ),
    (
        2,
        "In phiếu từ menu ba chấm trên danh sách",
        "P1",
        "Danh sách có phiếu bất kỳ.",
        "1. Bấm ba chấm ở cột Hành động, chọn In",
        "—",
        "- Mở tab mới, nội dung bản in đúng phiếu đã chọn",
    ),
    (
        3,
        "Bản in giữ chữ in đậm và giãn dòng",
        "P0",
        "Phiếu bất kỳ.",
        "1. Mở bản in, quan sát tiêu đề và các nhãn",
        "—",
        "- Chữ cần in đậm hiện đậm rõ\n"
        "- Các dòng của khối thông tin chung và khối ký có khoảng cách, không dính sát nhau\n"
        "- ⚠️ Đây là 2 lỗi từng gặp: mất chữ đậm và mất giãn dòng ở bảng không viền",
    ),
    (
        4,
        "Số lượng trên bản in giữ phần thập phân",
        "P1",
        "Phiếu có dòng hàng số lượng 12.5.",
        "1. Mở bản in, xem cột số lượng",
        "—",
        "- Hiện 12.5, không bị làm tròn thành 13\n"
        "- Định dạng số theo chuẩn quốc tế",
    ),
    (
        5,
        "In danh sách theo bộ lọc đang áp",
        "P0",
        "Đang lọc Trạng thái = Đã duyệt, kết quả 20 phiếu.",
        "1. Bấm nút In trên màn danh sách",
        "—",
        "- Mở tab mới với bản in danh sách gồm đúng 20 phiếu đang lọc\n"
        "- Có 6 cột: STT · Số phiếu · Ngày lập · Người lập · Người nhận · Trạng thái\n"
        "- Bản in ở khổ ngang\n"
        "- Cuối bản in có khối ký với dòng ngày tháng và chữ Người lập",
    ),
    (
        6,
        "In danh sách khi không có dữ liệu",
        "P2",
        "Đang lọc ra 0 phiếu.",
        "1. Bấm nút In",
        "—",
        "- Bản in vẫn mở với tiêu đề và bảng trống, không lỗi",
    ),
    (
        7,
        "Cửa sổ chọn trường xuất Excel",
        "P0",
        "Đang ở màn danh sách.",
        "1. Bấm nút Xuất Excel",
        "—",
        "- Mở cửa sổ \"Chọn trường xuất Excel\" liệt kê: Số phiếu · Ngày tạo · Người tạo · Người nhận · "
        "Trạng thái · Người duyệt · Công ty · Phòng ban · Ghi chú · Người cập nhật · Ngày cập nhật\n"
        "- Chưa xuất file ngay khi bấm nút",
    ),
    (
        8,
        "Xuất Excel theo đúng thứ tự trường đã tick",
        "P0",
        "Cửa sổ chọn trường đang mở.",
        "1. Tick lần lượt Trạng thái, rồi Số phiếu, rồi Người nhận\n"
        "2. Bấm xuất\n"
        "3. Mở file tải về",
        "—",
        "- File tải về, thông báo Xuất Excel thành công\n"
        "- Thứ tự cột trong file đúng theo thứ tự đã tick\n"
        "- Số dòng khớp với số phiếu đang lọc trên màn (không chỉ trang đang xem)",
    ),
    (
        9,
        "File Excel có khối ký cuối bảng",
        "P0",
        "Vừa xuất file.",
        "1. Mở file, cuộn xuống cuối bảng",
        "—",
        "- Có dòng \"Ngày ...... tháng ...... năm ......\", chữ \"Người lập\" và tên người xuất file\n"
        "- ⚠️ Đây là điểm từng thiếu, in ra không có chỗ ký",
    ),
    (
        10,
        "Số phiếu trong file Excel không bị hiểu nhầm là số",
        "P1",
        "Vừa xuất file có cột Số phiếu.",
        "1. Mở file, xem cột Số phiếu",
        "—",
        "- Số phiếu hiện đầy đủ dạng chữ, không có cảnh báo định dạng của Excel\n"
        "- Cột Ngày tạo hiện dạng ngày/tháng/năm, không bị Excel tự đổi kiểu",
    ),
    (
        11,
        "Xuất Excel khi chưa tick trường nào",
        "P2",
        "Cửa sổ chọn trường đang mở.",
        "1. Bấm xuất khi chưa tick gì",
        "—",
        "- Hệ thống nhắc phải chọn ít nhất một trường, không tạo file rỗng",
    ),
    (
        12,
        "Xuất Excel với bộ lọc rỗng kết quả",
        "P2",
        "Đang lọc ra 0 phiếu.",
        "1. Xuất Excel",
        "—",
        "- File tạo ra có tiêu đề cột nhưng không có dòng dữ liệu\n"
        "- Không báo lỗi",
    ),
]

SEC_X = [
    (
        1,
        "Mở khối Lịch sử thay đổi ở màn chi tiết",
        "P0",
        "Phiếu đã qua các bước tạo, gửi duyệt, duyệt.",
        "1. Mở chi tiết phiếu\n"
        "2. Quan sát khối Lịch sử thay đổi ở cuối trang",
        "—",
        "- Khối có biểu tượng đồng hồ, chữ \"Lịch sử thay đổi\", con số mốc lịch sử và nút \"Xem lịch sử\"\n"
        "- Mặc định đang thu gọn, chưa tải dữ liệu\n"
        "- Bấm \"Xem lịch sử\" mới nạp và hiện danh sách mốc",
    ),
    (
        2,
        "Thu gọn lại khối Lịch sử",
        "P2",
        "Khối lịch sử đang mở.",
        "1. Bấm nút Thu gọn",
        "—",
        "- Danh sách mốc ẩn đi, nút đổi lại thành \"Xem lịch sử\"",
    ),
    (
        3,
        "Nút Làm mới trong khối Lịch sử",
        "P2",
        "Khối lịch sử đang mở, vừa có thao tác mới trên phiếu ở tab khác.",
        "1. Bấm nút Làm mới",
        "—",
        "- Danh sách mốc nạp lại, có thêm mốc mới nhất",
    ),
    (
        4,
        "Thứ tự các mốc lịch sử",
        "P0",
        "Phiếu có 5 mốc lịch sử.",
        "1. Mở khối lịch sử",
        "—",
        "- Mốc mới nhất nằm TRÊN CÙNG, cũ nhất nằm dưới\n"
        "- ⚠️ Quy ước chung của hệ thống là mới → cũ",
    ),
    (
        5,
        "Loại hành động được ghi nhận",
        "P0",
        "Phiếu đã trải qua: tạo, chỉnh sửa, gửi duyệt, không duyệt, rồi được duyệt.",
        "1. Mở khối lịch sử, đọc nhãn từng mốc",
        "—",
        "- Đủ 5 nhãn: Tạo phiếu · Chỉnh sửa · Gửi duyệt · Không duyệt · Duyệt\n"
        "- Mỗi mốc có tên người thực hiện và thời điểm",
    ),
    (
        6,
        "Nội dung thay đổi của các trường chính",
        "P0",
        "Phiếu vừa được sửa: đổi Người nhận từ Nguyễn Văn A sang Trần Văn C và sửa Ghi chú.",
        "1. Mở mốc Chỉnh sửa",
        "—",
        "- Hiện dòng \"Người nhận\": giá trị cũ Nguyễn Văn A → giá trị mới Trần Văn C\n"
        "- Hiện dòng \"Ghi chú\" với nội dung cũ và mới\n"
        "- Lưu tên người, không phải mã số",
    ),
    (
        7,
        "Ghi nhận thay đổi bảng hàng hóa",
        "P0",
        "Phiếu vừa được sửa: thêm 1 dòng hàng mới và đổi số lượng của 1 dòng cũ.",
        "1. Mở mốc Chỉnh sửa",
        "—",
        "- Hiện phần hàng hóa được thêm, kèm Tên hàng và Mã hàng\n"
        "- Hiện dòng hàng bị đổi Số lượng với giá trị cũ và mới\n"
        "- Có cả cột SL theo ĐV cơ bản",
    ),
    (
        8,
        "Lý do từ chối hiện trên lịch sử",
        "P0",
        "Phiếu bị từ chối với lý do \"Hàng đã xuất cho khách\".",
        "1. Mở khối lịch sử, xem mốc Không duyệt",
        "—",
        "- Mốc Không duyệt hiện đầy đủ nội dung lý do\n"
        "- ⚠️ Không có lý do thì người lập không biết vì sao bị từ chối - đây là yêu cầu bắt buộc",
    ),
    (
        9,
        "Lọc lịch sử theo loại hành động",
        "P1",
        "Phiếu có 5 mốc gồm 2 mốc Chỉnh sửa.",
        "1. Chọn Loại hành động = Chỉnh sửa",
        "Loại hành động: Chỉnh sửa",
        "- Chỉ còn 2 mốc Chỉnh sửa",
    ),
    (
        10,
        "Lọc lịch sử theo người thực hiện và khoảng ngày",
        "P1",
        "Phiếu có mốc của 2 người khác nhau ở 2 ngày khác nhau.",
        "1. Chọn Người thực hiện\n"
        "2. Nhập Từ ngày / Đến ngày",
        "—",
        "- Danh sách mốc lọc đúng theo người và khoảng ngày đã chọn\n"
        "- Xóa điều kiện thì hiện lại đủ mốc",
    ),
    (
        11,
        "Cửa sổ Lịch sử mở từ danh sách giống khối ở chi tiết",
        "P0",
        "Phiếu có 5 mốc lịch sử.",
        "1. Trên danh sách bấm ba chấm, chọn Lịch sử\n"
        "2. So sánh với khối Lịch sử ở màn chi tiết của cùng phiếu",
        "—",
        "- Nội dung, thứ tự và bộ lọc của 2 nơi giống hệt nhau\n"
        "- Tiêu đề cửa sổ nêu đúng số phiếu đang xem",
    ),
    (
        12,
        "Phiếu chưa có mốc lịch sử",
        "P1",
        "Phiếu cũ được tạo từ cổng ERP trước khi có tính năng lịch sử.",
        "1. Mở khối lịch sử của phiếu đó",
        "—",
        "- Hiện dòng \"Chưa có lịch sử thao tác nào.\"\n"
        "- ⚠️ Đây là hiện tượng đã biết: thao tác thực hiện bên cổng ERP không sinh mốc lịch sử. "
        "Không ghi Failed",
    ),
]

SEC_XI = [
    (
        1,
        "Gõ chữ và dán ký tự lạ vào ô Số lượng",
        "P0",
        "Form Tạo mới có 1 dòng hàng.",
        "1. Gõ lần lượt a, b, c vào ô Số lượng\n"
        "2. Gõ tiếp 12a3\n"
        "3. Bôi đen ô, dán chuỗi 5x7 vào",
        "Số lượng: abc → 12a3 → dán 5x7",
        "- Ô KHÔNG nhận ký tự chữ: gõ abc thì ô vẫn trống, gõ 12a3 thì ô chỉ còn 123\n"
        "- Dán 5x7 thì ô chỉ còn 57, chữ x bị loại ngay khi dán\n"
        "- ⚠️ Ô chỉ nhận chữ số, dấu chấm thập phân và dấu phẩy hàng nghìn; không cần bấm Lưu mới biết sai",
    ),
    (
        2,
        "Bấm lưu khi ô Số lượng còn trống",
        "P0",
        "Dòng hàng đã chọn nhưng chưa nhập số lượng.",
        "1. Bấm Lưu và gửi duyệt",
        "—",
        "- Ô hiện lỗi \"Số lượng – Chưa nhập số lượng\"\n"
        "- Không gửi yêu cầu lưu nào lên hệ thống",
    ),
    (
        3,
        "Nhập số lượng bằng 0",
        "P0",
        "Dòng hàng bất kỳ.",
        "1. Nhập Số lượng = 0\n"
        "2. Bấm Lưu và gửi duyệt",
        "Số lượng: 0",
        "- Ô hiện lỗi \"Số lượng – Phải lớn hơn 0\"\n"
        "- Phiếu không được lưu",
    ),
    (
        4,
        "Nhập số lượng âm",
        "P0",
        "Dòng hàng bất kỳ.",
        "1. Nhập Số lượng = -3",
        "Số lượng: -3",
        "- Ô GIỮ NGUYÊN giá trị -3 và báo lỗi đỏ\n"
        "- ⚠️ Hệ thống không tự sửa lại con số người dùng nhập",
    ),
    (
        5,
        "Nhập số lượng có phần thập phân",
        "P1",
        "Hàng cho phép số lẻ, tồn 100.",
        "1. Nhập Số lượng = 12.5",
        "Số lượng: 12.5",
        "- Chấp nhận, SL theo ĐV cơ bản tính đúng theo hệ số\n"
        "- Hiển thị theo chuẩn số quốc tế (dấu chấm ngăn phần thập phân)",
    ),
    (
        6,
        "Nhập số lượng có dấu ngăn hàng nghìn",
        "P1",
        "Tồn 5,000.",
        "1. Nhập Số lượng = 1,200",
        "Số lượng: 1,200",
        "- Chấp nhận, hiểu là một nghìn hai trăm\n"
        "- SL theo ĐV cơ bản tính đúng",
    ),
    (
        7,
        "Nhiều dòng cùng sai định dạng số lượng",
        "P1",
        "Phiếu có 3 dòng: dòng 1 để trống, dòng 2 nhập 0, dòng 3 hợp lệ.",
        "1. Bấm Lưu và gửi duyệt",
        "—",
        "- CẢ HAI dòng sai đều viền đỏ kèm câu lỗi riêng, không chỉ dòng đầu tiên\n"
        "- Thông báo góc màn hình nhắc kiểm tra lại số lượng các dòng hàng hóa",
    ),
    (
        8,
        "Sửa lỗi rồi lưu lại",
        "P0",
        "Đang còn lỗi ở ô Số lượng.",
        "1. Sửa lại số lượng cho hợp lệ\n"
        "2. Bấm Lưu và gửi duyệt",
        "—",
        "- Lỗi đỏ biến mất ngay khi giá trị hợp lệ\n"
        "- Lưu thành công, quay về danh sách",
    ),
    (
        9,
        "Dòng hàng thiếu đơn vị tính",
        "P1",
        "Dòng hàng chưa chọn ĐVT.",
        "1. Bấm Lưu và gửi duyệt",
        "—",
        "- Hệ thống chặn, báo bắt buộc phải nhập ở ô ĐVT\n"
        "- Phiếu không được lưu",
    ),
    (
        10,
        "Ghi chú đúng giới hạn 255 ký tự",
        "P2",
        "Form Tạo mới.",
        "1. Nhập Ghi chú đúng 255 ký tự rồi Lưu nháp",
        "Ghi chú: chuỗi 255 ký tự",
        "- Lưu thành công, nội dung ghi chú giữ đủ 255 ký tự",
    ),
]

SEC_XII = [
    (
        1,
        "Hai người cùng duyệt một phiếu",
        "P0",
        "Hai tài khoản Kế toán kho cùng công ty mở cùng một phiếu Chờ duyệt trên 2 trình duyệt.",
        "1. Người thứ nhất bấm Duyệt và thành công\n"
        "2. Người thứ hai bấm Duyệt trên tab đang mở",
        "—",
        "- Lần duyệt thứ hai bị chặn\n"
        "- Tồn CHỈ bị trừ đúng một lần\n"
        "- ⚠️ Trừ tồn hai lần là lỗi nghiêm trọng, không hoàn tác được",
    ),
    (
        2,
        "Người lập sửa phiếu trong lúc người duyệt đang mở",
        "P1",
        "Phiếu Đang tạo mở trên tab của người duyệt; người lập gửi duyệt rồi sửa số lượng.",
        "1. Người duyệt tải lại màn chi tiết",
        "—",
        "- Màn hiện số liệu mới nhất, không dùng số liệu cũ đã nạp",
    ),
    (
        3,
        "Duyệt sau khi tồn bị thay đổi bởi phiếu khác",
        "P0",
        "Người lập có 100 Cái; có 2 phiếu Chờ duyệt, mỗi phiếu chuyển 60 Cái.",
        "1. Duyệt phiếu thứ nhất (thành công)\n"
        "2. Duyệt phiếu thứ hai",
        "—",
        "- Phiếu thứ nhất duyệt được, tồn còn 40\n"
        "- Phiếu thứ hai bị chặn, báo rõ cần 60 nhưng chỉ còn 40\n"
        "- Phiếu thứ hai vẫn ở trạng thái Chờ duyệt",
    ),
    (
        4,
        "Cô lập dữ liệu giữa các công ty",
        "P0",
        "Tài khoản B công ty 1 và tài khoản G công ty 4.",
        "1. Mỗi người lập 1 phiếu\n"
        "2. Đối chiếu danh sách của nhau",
        "—",
        "- Không ai thấy phiếu của công ty còn lại (trừ người có quyền xem theo tổng công ty)\n"
        "- Kết quả xuất Excel và bản in cũng chỉ chứa phiếu trong phạm vi quyền của người thao tác",
    ),
    (
        5,
        "Xóa phiếu trong lúc người khác đang mở chi tiết",
        "P1",
        "Người lập xóa phiếu; người khác đang mở màn chi tiết phiếu đó.",
        "1. Người thứ hai bấm Duyệt hoặc In trên tab cũ",
        "—",
        "- Hệ thống báo không tìm thấy dữ liệu và đưa về danh sách\n"
        "- Không treo trang, không hiện câu lỗi kỹ thuật",
    ),
]

SEC_XIII = [
    (
        1,
        "Luồng đầy đủ: tạo nháp → gửi duyệt → duyệt",
        "P0",
        "Tài khoản B (người lập, tồn 100 Cái hàng Cáp mạng CAT6), tài khoản E (Kế toán kho cùng công ty), "
        "người nhận Nguyễn Văn A (tồn 0).",
        "1. Tài khoản B tạo phiếu, chọn Người nhận, thêm hàng 10 Cái, bấm Lưu nháp\n"
        "2. Mở lại phiếu, bấm Sửa, đổi số lượng thành 20, bấm Lưu và gửi duyệt\n"
        "3. Tài khoản E mở phiếu, bấm Duyệt\n"
        "4. Kiểm tra tồn của B và của Nguyễn Văn A\n"
        "5. Mở khối Lịch sử thay đổi",
        "Số lượng: 10 rồi 20",
        "- Sau bước 1: phiếu Đang tạo, có số phiếu tự sinh\n"
        "- Sau bước 2: phiếu Chờ duyệt, tài khoản E nhận thông báo\n"
        "- Sau bước 3: phiếu Đã duyệt, tài khoản B nhận thông báo\n"
        "- Tồn của B còn 80, tồn của Nguyễn Văn A là 20\n"
        "- Lịch sử có đủ 4 mốc: Tạo phiếu · Chỉnh sửa · Gửi duyệt · Duyệt, xếp mới → cũ",
    ),
    (
        2,
        "Luồng bị từ chối rồi sửa và gửi lại",
        "P0",
        "Như trên, phiếu đang Chờ duyệt.",
        "1. Tài khoản E bấm Từ chối, nhập lý do\n"
        "2. Tài khoản B mở phiếu, xem lý do, bấm Sửa\n"
        "3. Sửa số lượng, bấm Lưu và gửi duyệt\n"
        "4. Tài khoản E duyệt",
        "Lý do từ chối: Sai số lượng",
        "- Sau bước 1: phiếu Không duyệt, khối Ghi chú duyệt hiện lý do\n"
        "- Sau bước 3: phiếu trở lại Chờ duyệt\n"
        "- Sau bước 4: phiếu Đã duyệt, tồn được cập nhật đúng\n"
        "- Lịch sử giữ đủ mốc Không duyệt kèm lý do",
    ),
    (
        3,
        "Luồng tạo rồi xóa bản nháp",
        "P1",
        "Tài khoản B.",
        "1. Tạo phiếu, Lưu nháp\n"
        "2. Trên danh sách bấm Xóa, xác nhận\n"
        "3. Kiểm tra tồn của B",
        "—",
        "- Phiếu bị xóa khỏi danh sách\n"
        "- Tồn của B không đổi (bản nháp chưa bao giờ động vào tồn)",
    ),
    (
        4,
        "Đối chiếu số liệu hai cổng sau toàn bộ luồng",
        "P0",
        "Đã hoàn tất luồng tạo → duyệt bên HRM.",
        "1. Mở màn tương ứng bên cổng ERP với cùng người dùng\n"
        "2. So số phiếu, trạng thái, người nhận, danh sách hàng hóa và số tồn của hai nhân viên",
        "—",
        "- Mọi thông tin khớp nhau giữa hai cổng\n"
        "- ⚠️ Riêng phần Lịch sử thay đổi chỉ có bên HRM - đây là tính năng mới, không phải lệch dữ liệu",
    ),
    (
        5,
        "Kiểm tra thông báo tới đúng người",
        "P1",
        "Công ty 1 có 3 người được cấp quyền Kế toán kho.",
        "1. Tài khoản B gửi duyệt một phiếu\n"
        "2. Đăng nhập lần lượt 3 tài khoản Kế toán kho và 1 tài khoản không có quyền đó",
        "—",
        "- Cả 3 tài khoản Kế toán kho đều nhận được thông báo phiếu cần duyệt\n"
        "- Tài khoản không có quyền không nhận được thông báo\n"
        "- Bấm vào thông báo mở đúng phiếu",
    ),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", SEC_III),
    ("IV", "TẠO PHIẾU", SEC_IV),
    ("V", "SỬA PHIẾU", SEC_V),
    ("VI", "XEM CHI TIẾT", SEC_VI),
    ("VII", "DUYỆT / TỪ CHỐI", SEC_VII),
    ("VIII", "XÓA", SEC_VIII),
    ("IX", "IN & XUẤT EXCEL", SEC_IX),
    ("X", "LỊCH SỬ THAY ĐỔI", SEC_X),
    ("XI", "RÀNG BUỘC NHẬP LIỆU", SEC_XI),
    ("XII", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", SEC_XII),
    ("XIII", "LUỒNG NGHIỆP VỤ ĐẦU CUỐI", SEC_XIII),
]

if __name__ == "__main__":
    build(
        output_file=OUTPUT,
        sheet_name="Trang tính1",
        feature_name=FEATURE_NAME,
        module_name=MODULE_NAME,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )
