# -*- coding: utf-8 -*-
"""Generate testcase Excel cho man ERP: Phieu Yeu cau dieu chuyen hang giu.

Chay:  python gen_testcase.py
Output: testcase.xlsx (cung thu muc)
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE_DIR = os.path.normpath(os.path.join(
    HERE, "..", "..", "..", "hrm", ".claude", "skills",
    "testcase-documenter", "assets"))
sys.path.insert(0, ENGINE_DIR)

from tc_engine import build  # noqa: E402

OUTPUT_FILE = os.path.join(HERE, "testcase.xlsx")
FEATURE_NAME = "Phiếu Yêu cầu điều chuyển hàng giữ"
MODULE_NAME = "Điều chuyển hàng giữ"

# =========================================================================
# 9 MUC MO TA
# =========================================================================
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Cho phép người đang giữ hàng chuyển phần hàng giữ đó sang cho một nhân viên khác và một khách "
     "hàng khác, giữ nguyên hạn giữ của dòng hàng nguồn.\n"
     "Phiếu đi qua các cấp duyệt: Trưởng phòng → (Ban giám đốc, khi vượt ngưỡng) → Kế toán. "
     "Khi Kế toán duyệt, số lượng mới thực sự chuyển từ người giữ cũ sang người nhận.\n"
     "Đường vào: menu Kho → nhóm Giữ hàng → Phiếu Yêu cầu điều chuyển hàng giữ (cũng có ở menu "
     "Kế toán → nhóm Giữ hàng). Người duyệt vào menu Kế toán → nhóm Hàng giữ → "
     "Phiếu yêu cầu điều chuyển hàng giữ chờ duyệt."),

    ("2. Đối tượng được tính / hiển thị",
     "► Màn danh sách hiển thị phiếu ở 5 trạng thái: Chờ TP duyệt · Chờ BGĐ duyệt · Chờ KT duyệt · "
     "Đã duyệt · Không duyệt.\n"
     "► Phiếu ở trạng thái Không duyệt CHỈ người lập ra nó mới nhìn thấy trên lưới.\n"
     "► Danh sách LUÔN bị giới hạn trong công ty của người đang đăng nhập, kể cả người có quyền xem "
     "theo tổng công ty.\n"
     "► Cửa sổ 'Tìm kiếm hàng hóa' (nút dấu cộng trên bảng Chi tiết) chỉ liệt kê hàng thỏa ĐỒNG THỜI: "
     "do chính người đang đăng nhập giữ · thuộc công ty người đang đăng nhập · số lượng giữ còn lớn "
     "hơn 0 · hạn giữ còn (từ hôm nay trở đi).\n"
     "► Cửa sổ 'Chi tiết xuất giữ' chỉ liệt kê các dòng hàng giữ của chính người đang đăng nhập, đúng "
     "mặt hàng của dòng, và CÒN HẠN GIỮ.\n"
     "► Ô 'Người nhận' chỉ liệt kê nhân viên đang làm việc thuộc cùng công ty với người lập."),

    ("3. Đối tượng bị ẩn / không tính",
     "► Phiếu Không duyệt của người khác — không hiện trên lưới của bất kỳ ai khác.\n"
     "► Phiếu của công ty khác — không hiện trên lưới trong mọi trường hợp.\n"
     "► Hàng đã hết hạn giữ, hàng còn số lượng 0, hàng của người khác — không hiện trong cửa sổ chọn "
     "hàng và cửa sổ chọn dòng xuất giữ.\n"
     "► Mục Sửa và Xóa bị ẩn khỏi menu Hành động khi phiếu không ở trạng thái Không duyệt hoặc người "
     "xem không phải người lập.\n"
     "► Cột tích 'Duyệt' từng dòng hàng hiện đang bị ẩn khỏi màn xem — người duyệt duyệt cả phiếu, "
     "không tách từng dòng.\n"
     "► Bảng 'Lịch sử ghi chú duyệt' trên BẢN IN chỉ liệt kê những cấp CÓ nhập ghi chú, trong khi màn "
     "xem liệt kê mọi cấp đã duyệt kể cả cấp không nhập ghi chú."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Ô 'Từ ngày' và 'Đến ngày' trên màn danh sách lọc theo cột NGÀY LẬP của phiếu.\n"
     "Cả hai đầu đều lấy trọn ngày được chọn (phiếu lập buổi chiều của ngày cuối vẫn phải lọt).\n"
     "Khi bấm In hoặc Xuất excel danh sách, khoảng ngày đang lọc được in thành dòng "
     "'Từ ngày … đến ngày …' ở đầu bản in."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Một phiếu gồm phần Thông tin chung (Người nhận, Khách hàng nhận, Ghi chú, File đính kèm, "
     "Phòng ban yêu cầu, Người lập, Ngày lập) và nhiều dòng hàng hóa.\n"
     "Mỗi dòng hàng phải trỏ tới đúng MỘT dòng hàng đang giữ nguồn (chọn qua cửa sổ 'Chi tiết xuất "
     "giữ'), và một dòng hàng giữ được xác định bởi: nhân viên giữ + khách hàng + hàng hóa + hạn giữ.\n"
     "Mỗi dòng có thể gắn thêm một Đơn hàng/Hợp đồng (không bắt buộc).\n"
     "Lịch sử duyệt nằm ngay trên phiếu, mỗi cấp một chỗ riêng: Trưởng phòng · Ban giám đốc · "
     "Kế toán — duyệt cấp sau không xóa vết cấp trước."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "► Hai dòng trong cùng một phiếu KHÔNG được trỏ về cùng một dòng hàng giữ nguồn.\n"
     "► Khi Kế toán duyệt, với từng dòng: TRỪ số lượng ở dòng hàng giữ nguồn của người lập và CỘNG "
     "vào dòng hàng giữ của người nhận + khách hàng nhận + ĐÚNG HẠN GIỮ CỦA DÒNG NGUỒN. Nếu người nhận "
     "đã có sẵn dòng cùng hàng hóa + khách hàng + hạn giữ thì cộng gộp vào dòng đó, không tạo dòng mới.\n"
     "► Hạn giữ KHÔNG bị đổi khi điều chuyển — hàng chuyển sang người nhận vẫn mang đúng hạn cũ.\n"
     "► Ngày bắt đầu giữ của dòng bên người nhận được ghi là ngày duyệt."),

    ("7. Phân quyền cấp",
     "• Xem phiếu hàng giữ theo tổng công ty — thấy phiếu của mọi phòng ban, nhưng VẪN chỉ trong công "
     "ty đang đăng nhập.\n"
     "• Xem phiếu hàng giữ theo công ty — thấy phiếu trong công ty mình.\n"
     "• Xem phiếu hàng giữ theo phòng ban — thấy phiếu của các phòng ban mình quản lý.\n"
     "• Không có ba quyền trên — chỉ thấy phiếu do chính mình lập.\n"
     "• Trưởng phòng duyệt hàng giữ — duyệt phiếu Chờ TP duyệt mà NGƯỜI NHẬN thuộc phòng ban mình "
     "quản lý.\n"
     "• Ban giám đốc duyệt hàng giữ — duyệt phiếu Chờ BGĐ duyệt trong công ty mình.\n"
     "• Kế toán duyệt hàng giữ — duyệt phiếu Chờ KT duyệt trong công ty mình (bước duyệt cuối).\n"
     "• Xem tất cả phiếu / Xem tất cả phiếu của công ty / Xem tất cả phiếu của phòng ban — quyết định "
     "màn danh sách có hiện thêm ô lọc Công ty và Phòng ban hay không."),

    ("8. Cách tính các ô thống kê",
     "► Ô 'Có thể giữ' = (tồn kho khả dụng của hàng hóa trừ đi phần hàng khuyến mại) chia hệ số đơn vị "
     "tính, làm tròn, không nhỏ hơn 0.\n"
     "► Ô 'Đang giữ' = số lượng còn lại của đúng dòng hàng giữ nguồn đã chọn ở ô 'Từ xuất giữ'.\n"
     "► Ô 'Từ xuất giữ' hiển thị theo mẫu: <số lượng đang giữ> - <tên khách hàng> - <hạn giữ>.\n"
     "► Ô 'Chuyển' bị hệ thống TỰ KẸP: nhập lớn hơn 'Đang giữ' thì bị kéo về đúng bằng 'Đang giữ'; "
     "nhập số âm thì bị kéo về 0.\n"
     "► Kiểm tra lúc duyệt: (tổng số đang giữ của hàng đó cho khách hàng nguồn) trừ (số đang nằm trong "
     "các yêu cầu xuất hàng chưa hoàn thành) phải lớn hơn hoặc bằng số Chuyển.\n"
     "► Điều kiện phiếu phải qua Ban giám đốc (thay vì đi thẳng xuống Kế toán): với dòng CÓ gắn đơn "
     "hàng/hợp đồng — số tiền khách đã thanh toán cho hợp đồng đó chiếm tỉ lệ nhỏ hơn '% đặt cọc' khai "
     "cho loại hợp đồng đó trong Quy chế công ty; với dòng KHÔNG gắn hợp đồng — tổng giá trị hàng xin "
     "điều chuyển vượt quá 'Giá trị giữ hàng khác' khai trong Quy chế công ty. Chỉ cần MỘT dòng thỏa "
     "là cả phiếu phải qua Ban giám đốc."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất của màn này — đọc trước khi test:\n"
     "① Màn này KHÔNG có bản nháp. Bấm 'Gửi' là phiếu đi thẳng sang Chờ TP duyệt, không quay lại được.\n"
     "② Chỉ SỬA và XÓA được phiếu ở trạng thái Không duyệt. Phiếu đang chờ duyệt thì không đụng vào "
     "được.\n"
     "③ Trưởng phòng duyệt xét theo phòng ban của NGƯỜI NHẬN, không phải phòng ban của người lập — "
     "đây là điểm khác với các phiếu hàng giữ khác.\n"
     "④ Ô 'Chuyển' TỰ SỬA giá trị người dùng nhập (kẹp về trần hoặc về 0) thay vì báo lỗi đỏ. Cần ghi "
     "nhận rõ hành vi này khi test.\n"
     "⑤ Mở màn XEM CHI TIẾT của một phiếu bằng liên kết trực tiếp hiện KHÔNG bị chặn — cần thử và ghi "
     "nhận kết quả thực tế.\n"
     "⑥ Quyền 'Xem phiếu hàng giữ theo tổng công ty' KHÔNG giúp nhìn sang công ty khác ở màn này, vì "
     "lưới luôn bị giới hạn theo công ty đang đăng nhập.\n"
     "⑦ Thông báo gửi cho Ban giám đốc và Kế toán đang ghi là 'yêu cầu xuất giữ' chứ không phải "
     "'điều chuyển hàng giữ' — ghi nhận đúng nội dung nhìn thấy.\n"
     "⑧ Bản in danh sách hiển thị Ngày lập theo thứ tự năm/tháng/ngày kèm giờ, khác với lưới hiển thị "
     "ngày/tháng/năm.\n"
     "⑨ Bản in danh sách phụ thuộc mẫu in khai trong hệ thống; nếu mẫu chưa được khai thì trang in ra "
     "trắng — không phải lỗi thao tác.\n"
     "⑩ Thông báo chặn khi hàng đã hết hạn giữ in ngày theo thứ tự năm-tháng-ngày.\n"
     "⑪ Người lập có hàng MƯỢN quá hạn hoặc hàng NHẬP THẲNG quá hạn có thể bị chặn tạo phiếu, tùy cấu "
     "hình chặn quá hạn của công ty.\n"
     "⑫ Nhóm test 'gọi thẳng chức năng, bỏ qua giao diện' dành cho tester kỹ thuật, dùng công cụ kiểm "
     "thử để kiểm tra hệ thống có chặn đúng khi người dùng không có quyền."),
]

# =========================================================================
# SECTION PHAN QUYEN
# =========================================================================
ROLE_TCS = [
    ("00", "Người dùng không có quyền xem mở rộng chỉ thấy phiếu của mình", "P0",
     "Tài khoản A thuộc công ty 1, không có quyền xem theo phòng ban/công ty/tổng công ty. "
     "Có 3 phiếu do A lập, 5 phiếu do người khác cùng phòng lập",
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Vào menu Kho → Giữ hàng → Phiếu Yêu cầu điều chuyển hàng giữ\n"
     "3. Đếm số dòng trên lưới",
     "Tài khoản: A (không quyền mở rộng)",
     "- Lưới chỉ hiện 3 phiếu do A lập\n"
     "- Không có ô lọc Công ty và ô lọc Phòng ban trên thanh tìm kiếm"),

    ("01", "Quyền 'Xem phiếu hàng giữ theo phòng ban'", "P0",
     "Tài khoản B có quyền 'Xem phiếu hàng giữ theo phòng ban', được phân quản lý phòng Kinh doanh 1. "
     "Có 4 phiếu của phòng Kinh doanh 1, 6 phiếu của phòng Kinh doanh 2",
     "1. Đăng nhập bằng tài khoản B\n2. Vào màn danh sách\n3. Quan sát phạm vi dữ liệu",
     "Tài khoản: B (quản lý phòng Kinh doanh 1)",
     "- Hiện đúng 4 phiếu của phòng Kinh doanh 1\n- Không hiện phiếu của phòng Kinh doanh 2"),

    ("02", "Quyền 'Xem phiếu hàng giữ theo công ty'", "P0",
     "Tài khoản C có quyền 'Xem phiếu hàng giữ theo công ty', thuộc công ty 1. Công ty 1 có 12 phiếu",
     "1. Đăng nhập bằng tài khoản C\n2. Vào màn danh sách\n3. Đếm số phiếu",
     "Tài khoản: C (công ty 1)",
     "- Hiện đủ 12 phiếu của công ty 1, không phân biệt phòng ban"),

    ("03", "Quyền xem theo tổng công ty vẫn không vượt ra ngoài công ty đang đăng nhập", "P0",
     "Tài khoản D có quyền 'Xem phiếu hàng giữ theo tổng công ty', đang đăng nhập ở công ty 1. "
     "Công ty 1 có 12 phiếu, công ty 4 có 9 phiếu",
     "1. Đăng nhập bằng tài khoản D\n2. Vào màn danh sách\n3. Đếm số phiếu",
     "Tài khoản: D (tổng công ty, đang ở công ty 1)",
     "- Chỉ hiện 12 phiếu của công ty 1\n"
     "⚠️ KHÔNG hiện 9 phiếu của công ty 4 — lưới luôn bị giới hạn theo công ty đang đăng nhập"),

    ("04", "Phiếu Không duyệt của người khác bị ẩn với mọi cấp quyền", "P0",
     "Tài khoản A có 1 phiếu bị Không duyệt. Tài khoản C có quyền xem theo công ty",
     "1. Đăng nhập tài khoản C\n2. Vào màn danh sách\n3. Lọc Trạng thái = Không duyệt",
     "Phiếu Không duyệt của A",
     "- Lưới không có phiếu Không duyệt của A\n"
     "- Đăng nhập lại bằng A thì phiếu này hiện bình thường"),

    ("05", "Quyền 'Trưởng phòng duyệt hàng giữ' xét theo phòng của NGƯỜI NHẬN", "P0",
     "Tài khoản E có quyền 'Trưởng phòng duyệt hàng giữ', quản lý phòng Kinh doanh 1. "
     "Phiếu P: người lập thuộc phòng Kinh doanh 2, người nhận thuộc phòng Kinh doanh 1. "
     "Phiếu Q: người lập thuộc phòng Kinh doanh 1, người nhận thuộc phòng Kinh doanh 2. "
     "Cả hai đều Chờ TP duyệt",
     "1. Đăng nhập tài khoản E\n"
     "2. Vào menu Kế toán → Hàng giữ → Phiếu yêu cầu điều chuyển hàng giữ chờ duyệt\n"
     "3. Quan sát danh sách",
     "Tài khoản: E (Trưởng phòng KD1)",
     "- Hiện phiếu P (người nhận thuộc KD1)\n"
     "- KHÔNG hiện phiếu Q (người nhận thuộc KD2) dù người lập thuộc KD1\n"
     "⚠️ Điểm khác biệt quan trọng so với các phiếu hàng giữ khác"),

    ("06", "Quyền 'Ban giám đốc duyệt hàng giữ'", "P0",
     "Tài khoản F có quyền 'Ban giám đốc duyệt hàng giữ', công ty 1. Có 3 phiếu Chờ BGĐ duyệt ở công "
     "ty 1, 2 phiếu Chờ TP duyệt",
     "1. Đăng nhập tài khoản F\n2. Vào màn chờ duyệt\n3. Đếm số phiếu",
     "Tài khoản: F (Ban giám đốc công ty 1)",
     "- Hiện đúng 3 phiếu Chờ BGĐ duyệt\n- Không hiện phiếu Chờ TP duyệt"),

    ("07", "Quyền 'Kế toán duyệt hàng giữ'", "P0",
     "Tài khoản G có quyền 'Kế toán duyệt hàng giữ', công ty 1. Có 4 phiếu Chờ KT duyệt, 1 phiếu "
     "Đã duyệt, 1 phiếu Không duyệt",
     "1. Đăng nhập tài khoản G\n2. Vào màn chờ duyệt\n3. Đếm số phiếu",
     "Tài khoản: G (Kế toán công ty 1)",
     "- Hiện đúng 4 phiếu Chờ KT duyệt\n- Không hiện phiếu Đã duyệt và Không duyệt"),

    ("08", "Người kiêm nhiều quyền duyệt thấy gộp các nhóm phiếu", "P1",
     "Tài khoản H vừa có 'Trưởng phòng duyệt hàng giữ' (quản lý phòng KD1) vừa có 'Ban giám đốc duyệt "
     "hàng giữ'. Có 2 phiếu Chờ TP duyệt có người nhận thuộc KD1, 3 phiếu Chờ BGĐ duyệt",
     "1. Đăng nhập tài khoản H\n2. Vào màn chờ duyệt\n3. Đếm số phiếu",
     "Tài khoản: H (kiêm 2 vai trò duyệt)",
     "- Hiện đủ 5 phiếu\n⚠️ Thiếu nhóm nào là lỗi gộp điều kiện quyền"),

    ("09", "Người không có quyền duyệt nào vào màn chờ duyệt", "P1",
     "Tài khoản A không có quyền duyệt nào, đã lập 2 phiếu",
     "1. Đăng nhập tài khoản A\n2. Mở màn chờ duyệt bằng liên kết trực tiếp\n3. Quan sát lưới",
     "Tài khoản: A",
     "- Chỉ hiện phiếu do chính A lập\n- Không hiện phiếu của người khác"),

    ("10", "Nút duyệt không hiện với người không tới lượt", "P0",
     "Phiếu P đang Chờ KT duyệt. Tài khoản E là Trưởng phòng duyệt hàng giữ",
     "1. Đăng nhập tài khoản E\n2. Mở màn xem phiếu P\n3. Quan sát khối nút cuối trang",
     "Phiếu P — Chờ KT duyệt",
     "- Không có nút 'TP duyệt', không có nút 'Không duyệt'\n"
     "- Không có khung nhập 'Ghi chú duyệt'\n- Chỉ có nút 'Quay lại'"),

    ("11", "Chặn duyệt khi gọi thẳng chức năng, bỏ qua giao diện", "P0",
     "Tài khoản A không có quyền duyệt nào. Phiếu P đang Chờ KT duyệt",
     "1. Dùng công cụ kiểm thử gọi thẳng chức năng Duyệt của phiếu P bằng tài khoản A\n"
     "2. Đọc phản hồi\n3. Mở lại phiếu P trên giao diện",
     "Tài khoản: A · Phiếu: P",
     "- Hệ thống từ chối, báo 'Không đủ quyền'\n- Trạng thái phiếu P không đổi"),

    ("12", "Trưởng phòng gọi thẳng chức năng duyệt phiếu ngoài phòng mình quản lý", "P0",
     "Tài khoản E là Trưởng phòng quản lý phòng KD1. Phiếu Q Chờ TP duyệt, người nhận thuộc phòng KD2",
     "1. Dùng công cụ kiểm thử gọi thẳng chức năng Duyệt phiếu Q bằng tài khoản E\n2. Đọc phản hồi",
     "Tài khoản: E · Phiếu: Q (người nhận KD2)",
     "- Hệ thống từ chối, báo 'Không đủ quyền'\n- Phiếu Q vẫn ở 'Chờ TP duyệt'"),

    ("13", "Chặn sửa và xóa khi gọi thẳng chức năng, bỏ qua giao diện", "P0",
     "Phiếu P do tài khoản B lập, đang ở trạng thái Không duyệt. Tài khoản A không phải người lập",
     "1. Dùng công cụ kiểm thử gọi thẳng chức năng Sửa phiếu P bằng tài khoản A\n"
     "2. Gọi tiếp chức năng Xóa phiếu P bằng tài khoản A\n3. Đăng nhập B kiểm tra lại phiếu P",
     "Tài khoản: A · Phiếu: P của B",
     "- Chức năng Sửa hiển thị trang báo không tìm thấy dữ liệu\n"
     "- Chức năng Xóa báo 'Không thể xóa!'\n- Phiếu P còn nguyên với đầy đủ dòng hàng"),

    ("14", "Chặn xóa tệp đính kèm của phiếu người khác", "P1",
     "Phiếu P do tài khoản B lập, trạng thái Không duyệt, có 1 tệp đính kèm. Tài khoản A không phải "
     "người lập",
     "1. Dùng công cụ kiểm thử gọi thẳng chức năng Xóa tệp đính kèm của phiếu P bằng tài khoản A\n"
     "2. Đăng nhập B mở lại phiếu P",
     "Tài khoản: A · Phiếu: P của B",
     "- Hệ thống từ chối, báo 'Không có quyền'\n- Tệp đính kèm vẫn còn trên phiếu"),

    ("15", "Mở màn xem chi tiết phiếu không thuộc phạm vi của mình", "P0",
     "Phiếu Q thuộc công ty 4, đang Chờ KT duyệt. Tài khoản A thuộc công ty 1, không liên quan",
     "1. Đăng nhập tài khoản A\n2. Mở màn xem phiếu Q bằng liên kết trực tiếp\n3. Ghi nhận kết quả",
     "Phiếu Q — công ty 4",
     "⚠️ Ghi nhận CHÍNH XÁC kết quả thực tế: màn xem chi tiết của phiếu này hiện không bị chặn, "
     "nội dung phiếu vẫn hiển thị\n"
     "- Nhưng phiếu Q KHÔNG được xuất hiện trên lưới danh sách của A\n"
     "- Và không có nút duyệt / sửa / xóa nào"),
]

# =========================================================================
# SECTIONS NGHIEP VU
# =========================================================================
SECTIONS = [
    # ------------------------------------------------------------------ I
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", [
        ("001", "Vào màn danh sách từ menu Kho", "P0",
         "Tài khoản A đã đăng nhập, có ít nhất 1 phiếu",
         "1. Bấm menu Kho\n2. Bấm nhóm Giữ hàng\n3. Bấm 'Phiếu Yêu cầu điều chuyển hàng giữ'",
         "Tài khoản: A",
         "- Trang mở với tiêu đề 'Danh sách yêu cầu điều chuyển hàng giữ'\n"
         "- Lưới có đủ 10 cột: STT · Mã phiếu · Ngày lập · Người nhận · Khách nhận · Người lập · "
         "Trạng thái · Người duyệt · Ngày duyệt · Hành động\n"
         "- Có nút 'Tạo mới', nút 'In' và nút 'Xuất excel' phía trên lưới"),

        ("002", "Vào màn danh sách từ menu Kế toán", "P2",
         "Tài khoản G đã đăng nhập",
         "1. Bấm menu Kế toán\n2. Bấm nhóm Giữ hàng\n"
         "3. Bấm 'Phiếu Yêu cầu điều chuyển hàng giữ'",
         "Tài khoản: G",
         "- Mở đúng màn danh sách với đầy đủ 10 cột như lối vào từ menu Kho"),

        ("003", "Vào màn chờ duyệt từ menu Kế toán", "P0",
         "Tài khoản G có quyền 'Kế toán duyệt hàng giữ', có 4 phiếu Chờ KT duyệt",
         "1. Bấm menu Kế toán\n2. Bấm nhóm Hàng giữ\n"
         "3. Bấm 'Phiếu yêu cầu điều chuyển hàng giữ chờ duyệt'",
         "Tài khoản: G",
         "- Lưới chỉ hiện phiếu đang chờ chính G duyệt"),

        ("004", "Cột Mã phiếu là liên kết mở màn xem", "P1",
         "Có ít nhất 1 phiếu trên lưới",
         "1. Vào màn danh sách\n2. Bấm vào mã phiếu ở cột Mã phiếu",
         "Phiếu: ĐCHG-00012",
         "- Mở màn xem của đúng phiếu đó\n"
         "- Tiêu đề trang có dạng 'Phiếu yêu cầu điều chuyển hàng giữ: ĐCHG-00012'"),

        ("005", "Định dạng mã phiếu tự sinh", "P1",
         "Tài khoản A vừa lập thành công 1 phiếu",
         "1. Vào màn danh sách\n2. Đọc mã phiếu mới nhất",
         "—",
         "- Mã phiếu bắt đầu bằng ĐCHG- và theo sau là dãy số\n- Mã không trùng phiếu nào đã có"),

        ("006", "Cột Người nhận, Người lập, Người duyệt hiển thị kèm mã phòng ban", "P1",
         "Có phiếu do nhân viên Nguyễn Văn A (phòng có mã KD1) lập, chuyển cho Trần Thị B "
         "(phòng có mã KD2)",
         "1. Vào màn danh sách\n2. Đọc cột Người lập và cột Người nhận",
         "—",
         "- Cột Người lập hiện 'KD1 - Nguyễn Văn A'\n- Cột Người nhận hiện 'KD2 - Trần Thị B'\n"
         "- Phiếu chưa duyệt thì cột Người duyệt và Ngày duyệt để trống"),

        ("007", "Cột Khách nhận hiển thị kèm mã khách hàng", "P1",
         "Có phiếu chuyển cho khách hàng mã KH001 tên 'Công ty TNHH Minh Long'",
         "1. Vào màn danh sách\n2. Đọc cột Khách nhận",
         "—",
         "- Cột Khách nhận hiện 'KH001 - Công ty TNHH Minh Long'"),

        ("008", "Nhãn màu của 5 trạng thái", "P0",
         "Trên lưới có đủ 5 phiếu ở 5 trạng thái khác nhau",
         "1. Vào màn danh sách\n2. Đọc cột Trạng thái của từng phiếu",
         "—",
         "- Đã duyệt: nhãn nền xanh lá\n"
         "- Chờ KT duyệt / Chờ BGĐ duyệt / Chờ TP duyệt: nhãn nền vàng\n"
         "- Không duyệt: nhãn nền đỏ\n- Không phiếu nào để trống cột Trạng thái"),

        ("009", "Menu Hành động của phiếu đang chờ duyệt", "P0",
         "Tài khoản A lập phiếu P đang ở 'Chờ TP duyệt'",
         "1. Đăng nhập A, vào màn danh sách\n2. Bấm nút bánh răng của phiếu P",
         "Phiếu P: Chờ TP duyệt",
         "- Menu chỉ có: Xem chi tiết · In\n- KHÔNG có Sửa, KHÔNG có Xóa"),

        ("010", "Menu Hành động của phiếu Không duyệt do mình lập", "P0",
         "Tài khoản A lập phiếu Q đã bị Không duyệt",
         "1. Đăng nhập A, vào màn danh sách\n2. Bấm nút bánh răng của phiếu Q",
         "Phiếu Q: Không duyệt",
         "- Menu có đủ: Xem chi tiết · Sửa · Xóa · In"),

        ("011", "Menu Hành động của phiếu Đã duyệt", "P0",
         "Phiếu R đã ở trạng thái Đã duyệt, do tài khoản A lập",
         "1. Đăng nhập A, bấm nút bánh răng của phiếu R",
         "Phiếu R: Đã duyệt",
         "- Menu chỉ có: Xem chi tiết · In\n- Không cho Sửa, không cho Xóa"),

        ("012", "Khối Thông tin chung ở màn xem", "P1",
         "Phiếu P do Nguyễn Văn A phòng Kinh doanh 1 lập ngày 05/03/2026, chuyển cho Trần Thị B, "
         "khách nhận KH001, ghi chú 'Chuyển theo yêu cầu khách'",
         "1. Mở màn xem phiếu P\n2. Đọc khối Thông tin chung",
         "Phiếu P",
         "- Góc phải hiện 'Nguyễn Văn A - 05/03/2026'\n"
         "- Ô Người nhận, Khách hàng nhận, Ghi chú, Phòng ban yêu cầu đều có dữ liệu và bị khóa\n"
         "- Ô Phòng ban yêu cầu hiện 'Kinh doanh 1'"),

        ("013", "Các cột bảng Chi tiết ở màn xem", "P1",
         "Phiếu P có 2 dòng hàng",
         "1. Mở màn xem phiếu P\n2. Đọc tiêu đề các cột trong bảng Chi tiết",
         "—",
         "- Đủ các cột: STT · Tên hàng · Mã hàng · Đơn vị tính · Từ xuất giữ · Có thể giữ · "
         "Đang giữ · Chuyển · Hạn giữ · Hợp đồng\n"
         "- Hai cột 'Đang giữ' và 'Chuyển' nằm chung nhóm tiêu đề 'Số lượng'\n"
         "- KHÔNG có cột tích 'Duyệt' từng dòng"),

        ("014", "Bảng Lịch sử ghi chú duyệt hiện đủ các cấp đã duyệt", "P0",
         "Phiếu P đã được Trưởng phòng duyệt KHÔNG nhập ghi chú, rồi Ban giám đốc duyệt có ghi chú "
         "'Đồng ý chuyển'",
         "1. Mở màn xem phiếu P\n2. Đọc bảng 'Lịch sử ghi chú duyệt'",
         "2 cấp đã duyệt",
         "- Bảng có 2 dòng: một dòng của Trưởng phòng (cột Nội dung ghi chú để trống) và một dòng của "
         "Ban giám đốc với nội dung 'Đồng ý chuyển'\n"
         "- Mỗi dòng có Người duyệt, Thời gian duyệt theo dạng ngày/tháng/năm giờ:phút\n"
         "⚠️ Cấp duyệt không nhập ghi chú VẪN phải có dòng riêng"),

        ("015", "Bảng Lịch sử ghi chú duyệt không hiện khi chưa ai duyệt", "P1",
         "Phiếu P vừa được gửi, đang Chờ TP duyệt, chưa ai duyệt",
         "1. Mở màn xem phiếu P\n2. Quan sát khu vực dưới bảng Chi tiết",
         "Phiếu P — chưa ai duyệt",
         "- Không hiện khối 'Lịch sử ghi chú duyệt'"),

        ("016", "Khung nhập Ghi chú duyệt chỉ hiện với người tới lượt duyệt", "P0",
         "Phiếu P Chờ KT duyệt. Tài khoản G có quyền Kế toán duyệt; tài khoản A là người lập",
         "1. Đăng nhập G, mở phiếu P, quan sát khối bên phải\n2. Đăng nhập A, mở lại phiếu P",
         "Phiếu P — Chờ KT duyệt",
         "- Với G: có khối 'Ghi chú duyệt' nhập được\n- Với A: không có khối này"),

        ("017", "Xem Lịch sử giữ hàng từ cột Đang giữ", "P1",
         "Phiếu P có dòng hàng X của khách KH001, đã có ít nhất 2 lần biến động số lượng giữ",
         "1. Mở màn xem phiếu P\n2. Bấm vào con số ở cột 'Đang giữ' của dòng hàng X",
         "Hàng X — khách KH001",
         "- Cửa sổ 'Lịch sử giữ hàng: <tên hàng>' mở ra\n"
         "- Bảng có các cột: STT · SL biến động · Ngày · SL giữ · Hạn giữ · Chứng từ\n"
         "- Số giảm hiện màu đỏ có dấu trừ, số tăng hiện màu xanh có dấu cộng"),

        ("018", "Nút Quay lại ở màn xem", "P2",
         "Đang mở màn xem 1 phiếu bất kỳ",
         "1. Kéo xuống cuối trang\n2. Bấm nút 'Quay lại'",
         "—",
         "- Quay về màn Danh sách yêu cầu điều chuyển hàng giữ"),
    ]),

    # ----------------------------------------------------------------- II
    ("II", "BỘ LỌC & TÌM KIẾM", [
        ("001", "Danh sách ô lọc trên màn danh sách", "P0",
         "Tài khoản A đã đăng nhập, không có quyền xem mở rộng",
         "1. Vào màn danh sách\n2. Đọc các ô lọc phía trên lưới",
         "Tài khoản: A",
         "- Có các ô: Từ ngày · Đến ngày · Mã phiếu · Tên, mã hàng · Người nhận · Khách nhận · "
         "Trạng thái · Người lập · Người duyệt\n"
         "- Có nút kính lúp (Tìm kiếm) và nút mũi tên vòng (Làm mới)\n"
         "- KHÔNG có ô lọc Công ty và Phòng ban"),

        ("002", "Ô lọc Công ty và Phòng ban hiện theo quyền", "P1",
         "Tài khoản D có quyền 'Xem tất cả phiếu'; tài khoản C có quyền 'Xem tất cả phiếu của công ty'",
         "1. Đăng nhập D, vào màn danh sách, đọc các ô lọc\n2. Đăng nhập C, làm lại",
         "Tài khoản D và C",
         "- Với D: có cả ô lọc Công ty và ô lọc Phòng ban\n"
         "- Với C: chỉ có ô lọc Phòng ban\n"
         "⚠️ Dù chọn Công ty khác thì lưới vẫn trống, vì phạm vi luôn bị giữ trong công ty đang "
         "đăng nhập"),

        ("003", "Lọc theo Mã phiếu — khớp một phần", "P0",
         "Có 3 phiếu mã ĐCHG-00011, ĐCHG-00012, ĐCHG-00120",
         "1. Nhập '0012' vào ô Mã phiếu\n2. Bấm nút kính lúp\n3. Chờ lưới nạp xong",
         "Mã phiếu: 0012",
         "- Lưới hiện ĐCHG-00012 và ĐCHG-00120\n- Không hiện ĐCHG-00011"),

        ("004", "Lọc theo Trạng thái", "P0",
         "Có 3 phiếu Đã duyệt, 2 phiếu Chờ KT duyệt, 1 phiếu Chờ TP duyệt",
         "1. Chọn ô Trạng thái = 'Chờ KT duyệt'\n2. Bấm nút kính lúp\n3. Chờ lưới nạp xong",
         "Trạng thái: Chờ KT duyệt",
         "- Lưới hiện đúng 2 phiếu, cả 2 đều là 'Chờ KT duyệt'"),

        ("005", "Danh sách giá trị của ô lọc Trạng thái", "P1",
         "Đang ở màn danh sách",
         "1. Bấm mở ô Trạng thái\n2. Đọc các giá trị",
         "—",
         "- Có đúng 5 giá trị: Chờ KT duyệt · Đã duyệt · Không duyệt · Chờ BGĐ duyệt · Chờ TP duyệt"),

        ("006", "Lọc theo Người nhận", "P0",
         "Trần Thị B là người nhận của 3 phiếu; các phiếu khác chuyển cho người khác",
         "1. Gõ 'Trần Thị B' vào ô Người nhận, chọn từ gợi ý\n2. Bấm nút kính lúp",
         "Người nhận: Trần Thị B",
         "- Lưới hiện đúng 3 phiếu\n- Cột Người nhận của mọi dòng đều là Trần Thị B"),

        ("007", "Lọc theo Khách nhận", "P0",
         "Khách hàng KH001 là khách nhận của 2 phiếu",
         "1. Chọn ô Khách nhận = 'KH001 - Công ty TNHH Minh Long'\n2. Bấm nút kính lúp",
         "Khách nhận: KH001",
         "- Lưới hiện đúng 2 phiếu\n- Cột Khách nhận của mọi dòng đều là KH001"),

        ("008", "Lọc theo Người lập", "P0",
         "Nguyễn Văn A lập 3 phiếu, Trần Thị B lập 4 phiếu",
         "1. Gõ 'Nguyễn Văn A' vào ô Người lập, chọn từ gợi ý\n2. Bấm nút kính lúp",
         "Người lập: Nguyễn Văn A",
         "- Lưới hiện đúng 3 phiếu"),

        ("009", "Lọc theo Người duyệt", "P1",
         "Kế toán Lê Văn C đã duyệt 2 phiếu",
         "1. Gõ 'Lê Văn C' vào ô Người duyệt, chọn từ gợi ý\n2. Bấm nút kính lúp",
         "Người duyệt: Lê Văn C",
         "- Lưới hiện đúng 2 phiếu\n- Không hiện phiếu chưa có người duyệt"),

        ("010", "Lọc theo Tên hàng", "P0",
         "Phiếu P có dòng hàng 'Máy nén khí Puma 5HP'; phiếu Q không có hàng nào tên chứa 'Puma'",
         "1. Nhập 'Puma' vào ô 'Tên, mã hàng'\n2. Bấm nút kính lúp\n3. Chờ lưới nạp xong",
         "Tên, mã hàng: Puma",
         "- Lưới hiện phiếu P\n- Không hiện phiếu Q"),

        ("011", "Lọc theo Mã hàng — phải nhập đủ mã", "P0",
         "Phiếu P có dòng hàng mã 'MNK-PUMA-5HP'",
         "1. Nhập 'MNK-PUMA-5HP' vào ô 'Tên, mã hàng', bấm kính lúp, ghi nhận kết quả\n"
         "2. Làm lại với 'PUMA-5', ghi nhận kết quả",
         "Mã đầy đủ và mã một phần",
         "- Bước 1: lưới hiện phiếu P\n"
         "⚠️ Bước 2: ghi nhận chính xác kết quả — ô này tìm theo tên hàng khớp một phần nhưng tìm "
         "theo mã hàng cần khớp đủ mã"),

        ("012", "Lọc Tên hàng kết hợp với Trạng thái", "P0",
         "Có 2 phiếu chứa hàng 'Puma': phiếu P (Đã duyệt) và phiếu S (Chờ KT duyệt). "
         "Ngoài ra còn 5 phiếu Đã duyệt không chứa hàng 'Puma'",
         "1. Nhập 'Puma' vào ô 'Tên, mã hàng'\n2. Chọn Trạng thái = Đã duyệt\n3. Bấm nút kính lúp\n"
         "4. Đếm và đọc từng dòng kết quả",
         "Puma + Đã duyệt",
         "- Lưới phải hiện ĐÚNG 1 phiếu: phiếu P\n"
         "⚠️ Nếu lưới hiện thêm phiếu S hoặc các phiếu Đã duyệt không chứa hàng 'Puma' thì hai điều "
         "kiện lọc đang không cùng thỏa — cần báo lỗi"),

        ("013", "Lọc Tên hàng kết hợp với Người lập", "P0",
         "Nguyễn Văn A lập 2 phiếu, không phiếu nào chứa hàng 'Puma'. Trần Thị B lập 1 phiếu có chứa "
         "hàng 'Puma'",
         "1. Chọn Người lập = Nguyễn Văn A\n2. Nhập 'Puma' vào ô 'Tên, mã hàng'\n3. Bấm nút kính lúp",
         "Nguyễn Văn A + Puma",
         "- Lưới TRỐNG\n"
         "⚠️ Nếu hiện phiếu của Trần Thị B thì bộ lọc đang bị lọt phạm vi"),

        ("014", "Lọc theo khoảng Ngày lập", "P0",
         "Có phiếu lập ngày 28/02/2026, 05/03/2026, 12/03/2026",
         "1. Nhập Từ ngày = 01/03/2026\n2. Nhập Đến ngày = 10/03/2026\n3. Bấm nút kính lúp",
         "Từ 01/03/2026 đến 10/03/2026",
         "- Lưới chỉ hiện phiếu lập ngày 05/03/2026"),

        ("015", "Ô 'Đến ngày' lấy trọn cả ngày được chọn", "P0",
         "Có phiếu lập lúc 17h30 ngày 10/03/2026",
         "1. Nhập Từ ngày = 10/03/2026 và Đến ngày = 10/03/2026\n2. Bấm nút kính lúp",
         "Từ 10/03/2026 đến 10/03/2026",
         "- Phiếu lập lúc 17h30 ngày 10/03/2026 VẪN hiện trên lưới"),

        ("016", "Kết hợp nhiều ô lọc cùng lúc", "P0",
         "Nguyễn Văn A có 3 phiếu: 1 Đã duyệt lập 05/03/2026, 1 Chờ KT duyệt lập 06/03/2026, "
         "1 Đã duyệt lập 20/03/2026",
         "1. Chọn Người lập = Nguyễn Văn A\n2. Chọn Trạng thái = Đã duyệt\n"
         "3. Nhập Từ ngày = 01/03/2026, Đến ngày = 10/03/2026\n4. Bấm nút kính lúp",
         "Nguyễn Văn A + Đã duyệt + 01/03–10/03/2026",
         "- Lưới hiện đúng 1 phiếu (Đã duyệt, lập 05/03/2026)"),

        ("017", "Nút Làm mới xóa hết điều kiện và nạp lại", "P0",
         "Đang lọc Trạng thái = Đã duyệt và Mã phiếu = 0012, lưới còn 1 dòng",
         "1. Bấm nút mũi tên vòng (Làm mới)\n2. Chờ lưới nạp xong\n3. Quan sát các ô lọc và số dòng",
         "—",
         "- Toàn bộ ô lọc trở về rỗng\n- Lưới nạp lại đầy đủ như lúc mới vào màn\n"
         "⚠️ Ô lọc trở về rỗng mà lưới vẫn giữ kết quả cũ là LỖI"),

        ("018", "Bộ lọc được nhớ khi quay lại màn", "P1",
         "Đang lọc Trạng thái = Đã duyệt trên màn danh sách",
         "1. Bấm mở một phiếu\n2. Bấm nút Quay lại\n3. Quan sát ô lọc và lưới",
         "Trạng thái: Đã duyệt",
         "- Ô Trạng thái vẫn là Đã duyệt\n- Lưới vẫn hiển thị kết quả đã lọc"),

        ("019", "Lọc không có kết quả", "P1",
         "Không có phiếu nào mang mã chứa 'ZZZZ'",
         "1. Nhập 'ZZZZ' vào ô Mã phiếu\n2. Bấm nút kính lúp",
         "Mã phiếu: ZZZZ",
         "- Lưới hiện dòng thông báo không có dữ liệu, trang không báo lỗi"),

        ("020", "Màn chờ duyệt giữ nguyên phạm vi khi lọc", "P0",
         "Tài khoản G là Kế toán duyệt, đang ở màn chờ duyệt với 4 phiếu Chờ KT duyệt. Công ty còn "
         "3 phiếu Chờ TP duyệt",
         "1. Chọn ô Trạng thái = Chờ TP duyệt\n2. Bấm nút kính lúp",
         "Trạng thái: Chờ TP duyệt",
         "- Lưới trống\n"
         "⚠️ Nếu 3 phiếu Chờ TP duyệt hiện ra thì phạm vi quyền của màn chờ duyệt đang bị phá vỡ"),
    ]),

    # ---------------------------------------------------------------- III
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", [
        ("001", "Thứ tự mặc định là phiếu mới nhất lên đầu", "P0",
         "Có phiếu lập ngày 05/03/2026, 10/03/2026, 12/03/2026",
         "1. Vào màn danh sách\n2. Đọc cột Ngày lập từ trên xuống",
         "—",
         "- Dòng đầu là phiếu 12/03/2026, kế tiếp 10/03/2026, cuối là 05/03/2026"),

        ("002", "Sắp xếp theo Ngày lập tăng dần và giảm dần", "P1",
         "Có ít nhất 5 phiếu với ngày lập khác nhau",
         "1. Bấm tiêu đề cột Ngày lập\n2. Đọc thứ tự\n3. Bấm lần nữa vào tiêu đề Ngày lập",
         "—",
         "- Lần bấm 1: ngày cũ nhất lên đầu\n- Lần bấm 2: ngày mới nhất lên đầu"),

        ("003", "Cột không cho sắp xếp", "P2",
         "Đang ở màn danh sách",
         "1. Bấm lần lượt tiêu đề các cột STT, Người nhận, Khách nhận, Người lập, Người duyệt, "
         "Hành động",
         "—",
         "- Các cột này không có biểu tượng sắp xếp và bấm vào không đổi thứ tự lưới"),

        ("004", "Đổi số dòng mỗi trang", "P1",
         "Có 30 phiếu thỏa bộ lọc hiện tại",
         "1. Vào màn danh sách\n2. Đổi ô số dòng mỗi trang sang 25\n3. Đếm số dòng hiển thị",
         "Số dòng/trang: 25",
         "- Lưới hiện đúng 25 dòng\n- Dòng thông tin bên dưới báo đang hiện 1 đến 25 trong tổng 30"),

        ("005", "Chuyển trang giữ nguyên bộ lọc", "P0",
         "Đang lọc Trạng thái = Đã duyệt, kết quả có 30 phiếu, đang xem 10 dòng mỗi trang",
         "1. Bấm sang trang 2\n2. Đọc cột Trạng thái\n3. Kiểm tra ô lọc Trạng thái",
         "Trạng thái: Đã duyệt",
         "- Mọi dòng ở trang 2 đều là Đã duyệt\n- Ô lọc vẫn giữ giá trị Đã duyệt"),

        ("006", "Số thứ tự chạy liên tục qua các trang", "P1",
         "Có 30 phiếu, đang xem 10 dòng mỗi trang",
         "1. Đọc cột STT ở trang 1\n2. Bấm sang trang 2 và đọc lại cột STT",
         "—",
         "- Trang 1 đánh số 1 đến 10\n- Trang 2 đánh số 11 đến 20"),

        ("007", "Sắp xếp giữ nguyên khi chuyển trang", "P1",
         "Đang sắp xếp theo Ngày lập tăng dần, kết quả có 30 phiếu",
         "1. Bấm sang trang 2\n2. So ngày lập của dòng đầu trang 2 với dòng cuối trang 1",
         "—",
         "- Ngày lập của dòng đầu trang 2 lớn hơn hoặc bằng dòng cuối trang 1\n"
         "- Không có phiếu nào bị lặp giữa 2 trang"),
    ]),

    # ----------------------------------------------------------------- IV
    ("IV", "CHỨC NĂNG CHÍNH (TẠO / SỬA / XEM)", [
        ("001", "Mở màn Tạo mới", "P0",
         "Tài khoản A đang giữ ít nhất 2 mặt hàng còn hạn",
         "1. Vào màn danh sách\n2. Bấm nút 'Tạo mới'",
         "Tài khoản: A",
         "- Trang mở với tiêu đề 'Tạo phiếu yêu cầu điều chuyển hàng giữ'\n"
         "- Khối Thông tin chung có: Người nhận (*) · Khách hàng nhận (*) · Ghi chú · File đính kèm\n"
         "- Bảng Chi tiết trống, hiện dòng chữ 'Không có hàng hóa'\n"
         "- Cuối trang có 2 nút: Gửi · Hủy\n"
         "⚠️ Không có nút Lưu nháp — màn này không có trạng thái nháp"),

        ("002", "Các cột của bảng Chi tiết khi tạo mới", "P0",
         "Đang ở màn Tạo mới",
         "1. Đọc tiêu đề các cột trong bảng Chi tiết",
         "—",
         "- Đủ các cột: STT · Tên hàng · Mã hàng · Đơn vị tính · Từ xuất giữ · Có thể giữ · "
         "Đang giữ · Chuyển · Hạn giữ · Hợp đồng · cột nút thao tác\n"
         "- Ở tiêu đề cột cuối có nút dấu cộng màu xanh để thêm hàng"),

        ("003", "Ô Người nhận chỉ liệt kê nhân viên cùng công ty", "P0",
         "Tài khoản A thuộc công ty 1. Công ty 1 có 20 nhân viên đang làm việc, công ty 4 có 15 nhân "
         "viên",
         "1. Bấm mở ô Người nhận\n2. Gõ tên một nhân viên thuộc công ty 4",
         "Tài khoản: A (công ty 1)",
         "- Danh sách chỉ có nhân viên công ty 1\n- Không tìm thấy nhân viên công ty 4"),

        ("004", "Ô Người nhận không liệt kê nhân viên đã nghỉ", "P1",
         "Công ty 1 có nhân viên 'Phạm Văn D' đã nghỉ việc",
         "1. Bấm mở ô Người nhận\n2. Gõ 'Phạm Văn D'",
         "Nhân viên đã nghỉ việc",
         "- Không tìm thấy nhân viên đã nghỉ trong danh sách"),

        ("005", "Chọn Khách hàng nhận", "P0",
         "Đang ở màn Tạo mới",
         "1. Bấm mở ô Khách hàng nhận\n2. Gõ 'Minh Long'\n3. Chọn khách hàng từ danh sách",
         "Khách hàng: KH001 - Công ty TNHH Minh Long",
         "- Ô hiện đúng khách hàng đã chọn"),

        ("006", "Thêm hàng vào bảng Chi tiết", "P0",
         "Tài khoản A đang giữ hàng 'Máy nén khí Puma 5HP' còn hạn, số lượng 12",
         "1. Bấm nút dấu cộng ở tiêu đề bảng Chi tiết\n2. Chọn hàng 'Máy nén khí Puma 5HP'\n"
         "3. Quan sát dòng vừa thêm",
         "Hàng: Máy nén khí Puma 5HP",
         "- Có thông báo 'Thêm thành công'\n"
         "- Bảng có 1 dòng với Tên hàng, Mã hàng, Đơn vị tính được điền sẵn\n"
         "- Ô 'Từ xuất giữ' còn trống, ô 'Chuyển' còn trống"),

        ("007", "Cửa sổ tìm hàng chỉ hiện hàng mình đang giữ và còn hạn", "P0",
         "Tài khoản A đang giữ hàng X (còn hạn, số lượng 12) và hàng Y (đã quá hạn giữ). "
         "Tài khoản B đang giữ hàng Z còn hạn",
         "1. Bấm nút dấu cộng\n2. Tìm lần lượt hàng X, hàng Y, hàng Z",
         "Tài khoản: A",
         "- Tìm thấy hàng X\n- KHÔNG tìm thấy hàng Y (đã hết hạn giữ)\n"
         "- KHÔNG tìm thấy hàng Z (của người khác)"),

        ("008", "Nút chọn 'Từ xuất giữ' bị khóa khi dòng chưa có hàng", "P1",
         "Đang ở màn Tạo mới, bảng Chi tiết trống",
         "1. Quan sát các dòng trong bảng Chi tiết trước khi thêm hàng",
         "—",
         "- Bảng chưa có dòng nào nên chưa dùng được nút chọn 'Từ xuất giữ'\n"
         "- Sau khi thêm hàng, nút kính lúp ở ô 'Từ xuất giữ' mới bấm được"),

        ("009", "Chọn dòng hàng giữ nguồn qua cửa sổ Chi tiết xuất giữ", "P0",
         "Hàng X của tài khoản A đang giữ cho khách KH001 số lượng 12, hạn 30/03/2026",
         "1. Thêm hàng X vào bảng\n2. Bấm nút kính lúp ở ô 'Từ xuất giữ'\n"
         "3. Chọn dòng trong cửa sổ 'Chi tiết xuất giữ'\n4. Quan sát dòng hàng",
         "Hàng X · KH001 · 12 · 30/03/2026",
         "- Cửa sổ có các cột: STT · Khách hàng · Số lượng · Thời hạn giữ và có ô lọc Khách hàng\n"
         "- Sau khi chọn: ô 'Từ xuất giữ' hiện '12 - Công ty TNHH Minh Long - 30/03/2026'\n"
         "- Cột 'Đang giữ' hiện 12, cột 'Hạn giữ' hiện 30/03/2026"),

        ("010", "Cửa sổ Chi tiết xuất giữ chỉ hiện dòng còn hạn", "P0",
         "Hàng X của tài khoản A có 2 dòng giữ: cho khách KH001 hạn 30/03/2026 và cho khách KH002 "
         "hạn 01/03/2026 (đã quá hạn). Hôm nay 05/03/2026",
         "1. Thêm hàng X vào bảng\n2. Bấm nút kính lúp ở ô 'Từ xuất giữ'\n3. Đếm số dòng",
         "Hôm nay = 05/03/2026",
         "- Cửa sổ chỉ hiện 1 dòng: khách KH001 hạn 30/03/2026\n"
         "- KHÔNG hiện dòng của khách KH002 đã quá hạn"),

        ("011", "Lọc theo Khách hàng trong cửa sổ Chi tiết xuất giữ", "P1",
         "Hàng X của tài khoản A đang giữ cho 3 khách hàng khác nhau, đều còn hạn",
         "1. Mở cửa sổ 'Chi tiết xuất giữ' của hàng X\n2. Chọn ô Khách hàng = KH001\n"
         "3. Bấm nút 'Tìm kiếm'",
         "Khách hàng: KH001",
         "- Cửa sổ chỉ còn dòng của khách KH001"),

        ("012", "Ô 'Chuyển' tự kẹp về số Đang giữ khi nhập vượt", "P0",
         "Dòng hàng X đã chọn dòng nguồn có số Đang giữ = 12",
         "1. Nhập ô 'Chuyển' = 20\n2. Bấm ra ngoài ô\n3. Đọc lại giá trị trong ô 'Chuyển'",
         "Đang giữ 12 · nhập 20",
         "⚠️ Ô 'Chuyển' TỰ ĐỔI về 12, hệ thống KHÔNG báo lỗi đỏ\n"
         "- Cần ghi nhận rõ hành vi này: giá trị người dùng gõ bị hệ thống sửa"),

        ("013", "Ô 'Chuyển' tự kẹp về 0 khi nhập số âm", "P0",
         "Dòng hàng X đã chọn dòng nguồn có số Đang giữ = 12",
         "1. Nhập ô 'Chuyển' = -5\n2. Bấm ra ngoài ô\n3. Đọc lại giá trị",
         "Nhập -5",
         "⚠️ Ô 'Chuyển' TỰ ĐỔI về 0, không báo lỗi đỏ"),

        ("014", "Ô 'Chuyển' nhận giá trị hợp lệ", "P0",
         "Dòng hàng X đã chọn dòng nguồn có số Đang giữ = 12",
         "1. Nhập ô 'Chuyển' = 5\n2. Bấm ra ngoài ô",
         "Chuyển: 5",
         "- Ô giữ nguyên giá trị 5, không bị đổi"),

        ("015", "Cột Hạn giữ tô đỏ khi dòng nguồn đã quá hạn", "P1",
         "Đang SỬA một phiếu bị Không duyệt có dòng hàng mà hạn giữ nguồn đã trôi qua",
         "1. Mở màn Sửa phiếu đó\n2. Quan sát ô ở cột 'Hạn giữ'",
         "Hạn giữ đã trôi qua",
         "- Ngày ở cột 'Hạn giữ' hiển thị màu đỏ"),

        ("016", "Xóa một dòng hàng khỏi bảng Chi tiết", "P1",
         "Bảng Chi tiết đang có 3 dòng hàng",
         "1. Bấm nút dấu trừ màu đỏ ở cuối dòng 2\n2. Đếm lại số dòng",
         "3 dòng → 2 dòng",
         "- Dòng 2 biến mất, còn 2 dòng\n- Số thứ tự được đánh lại từ 1"),

        ("017", "Chọn Hợp đồng cho dòng hàng", "P0",
         "Đã chọn Người nhận và Khách hàng nhận. Dòng hàng X có hợp đồng phù hợp",
         "1. Bấm nút kính lúp ở cột Hợp đồng của dòng X\n"
         "2. Chọn một dòng trong cửa sổ 'Đơn hàng/Hợp đồng'",
         "Hợp đồng: HDBH-00123",
         "- Cửa sổ hiện các cột STT · Số đơn hàng/Hợp đồng · Ngày lập\n"
         "- Sau khi chọn, ô Hợp đồng hiện HDBH-00123 và có thông báo 'Thêm thành công!'"),

        ("018", "Cửa sổ chọn hợp đồng lọc theo Khách hàng nhận và Người nhận", "P1",
         "Khách hàng nhận = KH001, Người nhận = Trần Thị B. Có hợp đồng của khách KH002 và hợp đồng "
         "của khách KH001 do Trần Thị B lập",
         "1. Bấm nút kính lúp ở cột Hợp đồng\n2. Quan sát danh sách hợp đồng",
         "KH001 + Trần Thị B",
         "- Chỉ hiện hợp đồng của khách KH001 do Trần Thị B lập\n"
         "- Không hiện hợp đồng của khách KH002"),

        ("019", "Xóa hợp đồng đã chọn khi đang tạo mới", "P1",
         "Dòng hàng X đã chọn hợp đồng HDBH-00123, đang ở màn Tạo mới",
         "1. Bấm nút dấu X ở cột Hợp đồng của dòng X",
         "—",
         "- Ô Hợp đồng trở về rỗng, hiện lại chữ mờ 'Chọn hợp đồng'"),

        ("020", "Nút xóa hợp đồng bị vô hiệu ở màn Sửa", "P1",
         "Phiếu P bị Không duyệt, có dòng hàng gắn hợp đồng HDBH-00123",
         "1. Mở màn Sửa phiếu P\n2. Bấm nút dấu X ở cột Hợp đồng",
         "Phiếu P — màn Sửa",
         "- Nút dấu X không bấm được, ô Hợp đồng vẫn giữ HDBH-00123\n"
         "⚠️ Điểm khác biệt giữa màn Tạo mới và màn Sửa"),

        ("021", "Ô Hợp đồng và ô Từ xuất giữ không gõ tay được", "P2",
         "Đang ở màn Tạo mới, đã thêm 1 dòng hàng",
         "1. Bấm vào ô ở cột Hợp đồng và gõ ký tự\n2. Làm tương tự với ô 'Từ xuất giữ'",
         "—",
         "- Cả hai ô đều không nhận ký tự, chỉ chọn được qua cửa sổ tìm kiếm"),

        ("022", "Thêm và bỏ ô chọn tệp đính kèm", "P1",
         "Đang ở màn Tạo mới",
         "1. Bấm nút dấu cộng ở khu vực File đính kèm 2 lần\n2. Bấm dấu X trên ô thứ hai",
         "—",
         "- Bước 1: có 2 ô chọn tệp\n- Bước 2: còn 1 ô"),

        ("023", "Hộp chọn tệp gợi ý đủ các loại tệp được nhận", "P1",
         "Đang ở màn Tạo mới, đã thêm 1 ô đính kèm. Trên máy có tệp 'bao-gia.xlsx'",
         "1. Bấm vào ô đính kèm\n2. Quan sát bộ lọc loại tệp\n3. Chọn tệp 'bao-gia.xlsx'",
         "Tệp: bao-gia.xlsx",
         "- Hộp chọn tệp gợi ý cả tệp Excel, không phải chỉ PDF\n"
         "- Chọn được tệp Excel, ô hiện tên 'bao-gia.xlsx'"),

        ("024", "Gửi phiếu thành công", "P0",
         "Đã chọn Người nhận, Khách hàng nhận, thêm 1 dòng hàng đủ 'Từ xuất giữ' và 'Chuyển' hợp lệ",
         "1. Bấm nút 'Gửi'\n2. Đọc thông báo\n3. Quan sát trang được chuyển tới",
         "Chuyển: 5",
         "- Thông báo 'Yêu cầu đã được gửi'\n- Hệ thống quay về màn danh sách\n"
         "- Phiếu mới nằm đầu lưới với trạng thái 'Chờ TP duyệt'"),

        ("025", "Trưởng phòng quản lý người nhận được thông báo khi phiếu được gửi", "P0",
         "Người nhận là Trần Thị B thuộc phòng Kinh doanh 2. Tài khoản E là Trưởng phòng duyệt hàng "
         "giữ quản lý phòng Kinh doanh 2, đang đăng nhập ở máy khác",
         "1. Tài khoản A bấm 'Gửi'\n2. Ở máy của E mở chuông thông báo",
         "Phiếu vừa gửi: ĐCHG-00050",
         "- E nhận thông báo 'Bạn có một yêu cầu điều chuyển hàng giữ cần duyệt: ĐCHG-00050'\n"
         "- Bấm vào thông báo mở đúng màn xem của phiếu đó"),

        ("026", "Trưởng phòng quản lý phòng của NGƯỜI LẬP không nhận thông báo", "P1",
         "Người lập thuộc phòng Kinh doanh 1, người nhận thuộc phòng Kinh doanh 2. Tài khoản E1 là "
         "Trưởng phòng quản lý Kinh doanh 1",
         "1. Người lập bấm 'Gửi'\n2. Ở máy của E1 mở chuông thông báo",
         "Người lập KD1 · người nhận KD2",
         "- E1 KHÔNG nhận được thông báo về phiếu này\n"
         "⚠️ Thông báo đi theo phòng ban của NGƯỜI NHẬN"),

        ("027", "Nút Hủy ở màn Tạo mới", "P1",
         "Đang ở màn Tạo mới, đã điền vài thông tin",
         "1. Bấm nút 'Hủy'\n2. Quan sát trang\n3. Kiểm tra lưới danh sách",
         "—",
         "- Quay về màn danh sách\n- Không có phiếu mới nào được tạo"),

        ("028", "Nút Gửi khóa lại trong lúc xử lý", "P1",
         "Đang ở màn Tạo mới, đã điền hợp lệ",
         "1. Bấm 'Gửi'\n2. Quan sát nút ngay sau khi bấm",
         "—",
         "- Nút đổi sang biểu tượng đang quay và không bấm lại được\n"
         "- Không tạo ra hai phiếu trùng nhau"),

        ("029", "Mở màn Sửa phiếu bị Không duyệt", "P0",
         "Tài khoản A lập phiếu P đã bị Không duyệt, có 2 dòng hàng, ghi chú 'Chuyển theo yêu cầu khách'",
         "1. Đăng nhập A, bấm bánh răng của phiếu P, chọn 'Sửa'\n2. Quan sát dữ liệu nạp lên",
         "Phiếu P — Không duyệt",
         "- Trang mở với đầy đủ dữ liệu cũ: Người nhận, Khách hàng nhận, Ghi chú, 2 dòng hàng\n"
         "- Ô Khách hàng nhận hiển thị đúng khách đã chọn, không để trống"),

        ("030", "Sửa và gửi lại phiếu bị Không duyệt", "P0",
         "Phiếu P bị Không duyệt, dòng hàng X có Chuyển = 12",
         "1. Mở màn Sửa phiếu P\n2. Sửa ô 'Chuyển' của hàng X thành 5\n3. Bấm 'Gửi'\n"
         "4. Kiểm tra trạng thái trên lưới",
         "Chuyển: 12 → 5",
         "- Thông báo 'Yêu cầu đã được gửi'\n- Phiếu P chuyển sang 'Chờ TP duyệt'\n"
         "- Mở lại phiếu thấy ô Chuyển là 5"),

        ("031", "Lịch sử ghi chú duyệt cũ vẫn còn sau khi gửi lại", "P1",
         "Phiếu P từng bị Trưởng phòng Không duyệt với ghi chú 'Sai khách hàng nhận', nay đã được sửa "
         "và gửi lại",
         "1. Mở màn xem phiếu P\n2. Đọc bảng 'Lịch sử ghi chú duyệt'",
         "Phiếu P gửi lần 2",
         "- Bảng vẫn hiện dòng ghi chú 'Sai khách hàng nhận' của lần từ chối trước\n"
         "⚠️ Đây là hành vi mong muốn: không xóa vết duyệt cũ"),

        ("032", "Xóa tệp đính kèm ở màn Sửa", "P1",
         "Phiếu P bị Không duyệt, đã đính kèm tệp 'bien-ban.pdf'",
         "1. Mở màn Sửa phiếu P\n2. Bấm dấu X trên tệp 'bien-ban.pdf'\n3. Xác nhận\n4. Tải lại trang",
         "Tệp: bien-ban.pdf",
         "- Hộp thoại hỏi 'Bạn chắc chắn muốn xóa file này?'\n"
         "- Sau khi xác nhận, tệp biến mất và có thông báo xóa thành công\n"
         "- Tải lại trang tệp vẫn không còn"),

        ("033", "Không mở được màn Sửa khi phiếu đang chờ duyệt", "P0",
         "Phiếu Q của tài khoản A đang ở 'Chờ TP duyệt'",
         "1. Đăng nhập A\n2. Mở màn Sửa phiếu Q bằng liên kết trực tiếp",
         "Phiếu Q — Chờ TP duyệt",
         "- Hệ thống hiển thị trang báo không tìm thấy dữ liệu"),

        ("034", "Không mở được màn Sửa khi phiếu đã duyệt", "P0",
         "Phiếu R của tài khoản A đang ở 'Đã duyệt'",
         "1. Đăng nhập A\n2. Mở màn Sửa phiếu R bằng liên kết trực tiếp",
         "Phiếu R — Đã duyệt",
         "- Hệ thống hiển thị trang báo không tìm thấy dữ liệu"),
    ]),

    # ------------------------------------------------------------------ V
    ("V", "CÁC THAO TÁC TRẠNG THÁI (DUYỆT / KHÔNG DUYỆT)", [
        ("001", "Trưởng phòng duyệt, phiếu xuống thẳng Kế toán", "P0",
         "Phiếu P Chờ TP duyệt, 1 dòng hàng không gắn hợp đồng, tổng giá trị 5.000.000 đ. "
         "Quy chế công ty khai 'Giá trị giữ hàng khác' = 50.000.000 đ. Tài khoản E là Trưởng phòng "
         "quản lý phòng của người nhận",
         "1. Đăng nhập E, mở phiếu P\n2. Bấm nút 'TP duyệt'\n3. Kiểm tra trạng thái phiếu",
         "Giá trị 5.000.000 đ < ngưỡng 50.000.000 đ",
         "- Phiếu P chuyển sang 'Chờ KT duyệt'\n"
         "- Hệ thống quay về màn chờ duyệt\n"
         "- Người có quyền Kế toán duyệt hàng giữ nhận được thông báo"),

        ("002", "Trưởng phòng duyệt, phiếu phải qua Ban giám đốc do vượt ngưỡng", "P0",
         "Phiếu P Chờ TP duyệt, 1 dòng hàng KHÔNG gắn hợp đồng, tổng giá trị 80.000.000 đ. "
         "Quy chế công ty khai 'Giá trị giữ hàng khác' = 50.000.000 đ",
         "1. Đăng nhập E, mở phiếu P\n2. Bấm 'TP duyệt'\n3. Kiểm tra trạng thái",
         "Giá trị 80.000.000 đ > ngưỡng 50.000.000 đ",
         "- Phiếu P chuyển sang 'Chờ BGĐ duyệt'\n"
         "- Người có quyền Ban giám đốc duyệt hàng giữ nhận được thông báo"),

        ("003", "Phiếu gắn hợp đồng chưa đủ tỉ lệ đặt cọc phải qua Ban giám đốc", "P0",
         "Phiếu P Chờ TP duyệt, dòng hàng gắn hợp đồng bán hàng HDBH-00123 tổng giá trị "
         "100.000.000 đ, khách mới thanh toán 10.000.000 đ. Quy chế công ty khai % đặt cọc cho loại "
         "Hợp đồng bán hàng = 30",
         "1. Đăng nhập E, mở phiếu P\n2. Bấm 'TP duyệt'\n3. Kiểm tra trạng thái",
         "Đã thu 10% < mức 30% yêu cầu",
         "- Phiếu chuyển sang 'Chờ BGĐ duyệt'"),

        ("004", "Phiếu gắn hợp đồng đã đủ tỉ lệ đặt cọc đi thẳng Kế toán", "P0",
         "Giống trên nhưng khách đã thanh toán 40.000.000 đ trên hợp đồng 100.000.000 đ, mức yêu cầu 30",
         "1. Đăng nhập E, mở phiếu P\n2. Bấm 'TP duyệt'\n3. Kiểm tra trạng thái",
         "Đã thu 40% > mức 30% yêu cầu",
         "- Phiếu chuyển sang 'Chờ KT duyệt'"),

        ("005", "Một dòng vượt ngưỡng là cả phiếu phải qua Ban giám đốc", "P0",
         "Phiếu P có 3 dòng: 2 dòng thỏa điều kiện đi thẳng, 1 dòng có hợp đồng chưa đủ tỉ lệ đặt cọc",
         "1. Đăng nhập E, mở phiếu P\n2. Bấm 'TP duyệt'\n3. Kiểm tra trạng thái",
         "3 dòng — 1 dòng vượt ngưỡng",
         "- Phiếu chuyển sang 'Chờ BGĐ duyệt'\n"
         "⚠️ Quy tắc là 'chỉ cần một dòng vượt ngưỡng'"),

        ("006", "Ban giám đốc duyệt", "P0",
         "Phiếu P đang 'Chờ BGĐ duyệt'. Tài khoản F có quyền Ban giám đốc duyệt hàng giữ, cùng công ty",
         "1. Đăng nhập F, mở phiếu P\n2. Bấm nút 'BGĐ duyệt'\n3. Kiểm tra trạng thái",
         "Phiếu P — Chờ BGĐ duyệt",
         "- Phiếu P chuyển sang 'Chờ KT duyệt'\n"
         "- Người có quyền Kế toán duyệt hàng giữ nhận thông báo\n"
         "- Người lập nhận thông báo '… vừa chuyển duyệt yêu cầu điều chuyển hàng giữ: ĐCHG-…'"),

        ("007", "Nội dung thông báo gửi cho cấp duyệt tiếp theo", "P2",
         "Phiếu P vừa được Trưởng phòng duyệt và chuyển sang Chờ KT duyệt",
         "1. Đăng nhập tài khoản G (Kế toán duyệt)\n2. Mở chuông thông báo\n3. Đọc nội dung",
         "Phiếu: ĐCHG-00050",
         "⚠️ Ghi nhận chính xác chữ hiển thị: thông báo đang ghi 'Bạn có một yêu cầu xuất giữ cần "
         "duyệt: ĐCHG-00050' chứ không phải 'điều chuyển hàng giữ'\n"
         "- Bấm vào thông báo vẫn mở đúng phiếu điều chuyển"),

        ("008", "Kế toán duyệt — bước cuối", "P0",
         "Phiếu P Chờ KT duyệt, 1 dòng hàng X: khách nguồn KH001, số Chuyển 12, hạn giữ 30/03/2026. "
         "Người nhận là Trần Thị B, khách nhận KH002. Tài khoản G có quyền Kế toán duyệt hàng giữ",
         "1. Đăng nhập G, mở phiếu P\n2. Bấm nút 'KT Duyệt'\n3. Kiểm tra trạng thái phiếu",
         "Hàng X · 12 · KH001 → KH002",
         "- Phiếu P chuyển sang 'Đã duyệt', cột Người duyệt và Ngày duyệt được điền\n"
         "- Hệ thống quay về màn chờ duyệt\n"
         "- Người lập nhận thông báo '… vừa duyệt yêu cầu điều chuyển hàng giữ: ĐCHG-…'"),

        ("009", "Số lượng thực sự chuyển sang người nhận sau khi Kế toán duyệt", "P0",
         "Tiếp theo trường hợp trên. Trước khi duyệt: Nguyễn Văn A giữ hàng X cho khách KH001 số "
         "lượng 12 hạn 30/03/2026; Trần Thị B chưa giữ hàng X",
         "1. Sau khi G bấm 'KT Duyệt'\n2. Vào menu Kho → Giữ hàng → Danh sách hàng giữ\n"
         "3. Tìm hàng X của Nguyễn Văn A và của Trần Thị B",
         "Chuyển 12 · KH001 → KH002",
         "- Dòng của Nguyễn Văn A cho khách KH001 giảm 12, còn 0\n"
         "- Xuất hiện dòng của Trần Thị B cho khách KH002, hàng X, số lượng 12"),

        ("010", "Hạn giữ được giữ nguyên khi điều chuyển", "P0",
         "Tiếp theo trường hợp trên. Dòng nguồn có hạn giữ 30/03/2026",
         "1. Sau khi duyệt, mở Danh sách hàng giữ tìm dòng mới của Trần Thị B",
         "Hạn nguồn 30/03/2026",
         "- Dòng mới của Trần Thị B có hạn giữ đúng 30/03/2026\n"
         "⚠️ Điều chuyển KHÔNG kéo dài hoặc rút ngắn hạn giữ"),

        ("011", "Ngày bắt đầu giữ của dòng mới là ngày duyệt", "P1",
         "Hôm nay 05/03/2026. Phiếu P vừa được Kế toán duyệt, tạo dòng giữ mới cho Trần Thị B",
         "1. Mở Danh sách hàng giữ tìm dòng mới của Trần Thị B\n2. Đọc cột Ngày bắt đầu giữ",
         "Hôm nay = 05/03/2026",
         "- Ngày bắt đầu giữ của dòng mới là 05/03/2026"),

        ("012", "Chuyển một phần thì tách số lượng", "P0",
         "Nguyễn Văn A giữ hàng X cho khách KH001 12 đơn vị hạn 30/03/2026. Phiếu P chỉ chuyển 5 sang "
         "Trần Thị B / khách KH002",
         "1. Duyệt hết cấp tới Kế toán duyệt\n2. Mở Danh sách hàng giữ",
         "Chuyển 5 trong 12",
         "- Nguyễn Văn A còn 7 cho khách KH001 hạn 30/03/2026\n"
         "- Trần Thị B có 5 cho khách KH002 hạn 30/03/2026\n- Tổng vẫn là 12"),

        ("013", "Chuyển vào dòng người nhận đã có sẵn thì cộng gộp", "P0",
         "Trần Thị B đã có sẵn dòng giữ hàng X cho khách KH002 hạn 30/03/2026 số lượng 4. "
         "Phiếu P chuyển thêm 12 hàng X hạn 30/03/2026 cho cùng người, cùng khách",
         "1. Duyệt hết cấp tới Kế toán duyệt\n2. Mở Danh sách hàng giữ, tìm hàng X của Trần Thị B "
         "cho khách KH002\n3. Đếm số dòng",
         "4 + 12",
         "- Chỉ có MỘT dòng hạn 30/03/2026 với số lượng 16\n"
         "- KHÔNG phát sinh dòng thứ hai cùng hạn"),

        ("014", "Hai dòng nguồn khác hạn giữ tạo hai dòng đích khác nhau", "P0",
         "Phiếu P có 2 dòng cùng hàng X: dòng 1 lấy từ hàng giữ hạn 20/03/2026 (chuyển 3), dòng 2 lấy "
         "từ hàng giữ hạn 30/03/2026 (chuyển 4). Cùng người nhận, cùng khách nhận",
         "1. Duyệt hết cấp tới Kế toán duyệt\n2. Mở Danh sách hàng giữ tìm hàng X của người nhận",
         "3 (hạn 20/03) + 4 (hạn 30/03)",
         "- Người nhận có 2 dòng riêng: hạn 20/03/2026 số lượng 3 và hạn 30/03/2026 số lượng 4\n"
         "- Hai dòng KHÔNG bị gộp làm một"),

        ("015", "Không duyệt ở cấp Trưởng phòng", "P0",
         "Phiếu P Chờ TP duyệt. Tài khoản E là Trưởng phòng quản lý phòng của người nhận",
         "1. Đăng nhập E, mở phiếu P\n2. Nhập 'Sai khách hàng nhận' vào khung 'Ghi chú duyệt'\n"
         "3. Bấm 'Không duyệt'\n4. Kiểm tra trạng thái",
         "Ghi chú: Sai khách hàng nhận",
         "- Phiếu P chuyển sang trạng thái 'Không duyệt'\n"
         "- Người lập nhận thông báo '… đã không duyệt yêu cầu điều chuyển hàng giữ: ĐCHG-…'\n"
         "- Hệ thống quay về màn chờ duyệt"),

        ("016", "Không duyệt ở cấp Ban giám đốc", "P0",
         "Phiếu P Chờ BGĐ duyệt. Tài khoản F có quyền Ban giám đốc duyệt hàng giữ",
         "1. Đăng nhập F, mở phiếu P\n2. Nhập ghi chú 'Giá trị quá lớn'\n3. Bấm 'Không duyệt'\n"
         "4. Kiểm tra trạng thái",
         "Ghi chú: Giá trị quá lớn",
         "- Phiếu P chuyển sang 'Không duyệt'\n- Người lập nhận thông báo"),

        ("017", "Không duyệt ở cấp Kế toán", "P0",
         "Phiếu P Chờ KT duyệt. Tài khoản G có quyền Kế toán duyệt hàng giữ",
         "1. Đăng nhập G, mở phiếu P\n2. Nhập ghi chú 'Hàng đã có người đặt'\n3. Bấm 'Không duyệt'\n"
         "4. Kiểm tra trạng thái và Danh sách hàng giữ",
         "Ghi chú: Hàng đã có người đặt",
         "- Phiếu P chuyển sang 'Không duyệt'\n"
         "- Số lượng hàng giữ của người lập và người nhận KHÔNG thay đổi"),

        ("018", "Ghi chú duyệt là bắt buộc khi Không duyệt", "P0",
         "Phiếu P Chờ KT duyệt, tài khoản G đang mở màn xem, khung 'Ghi chú duyệt' để trống",
         "1. Bấm 'Không duyệt'\n2. Đọc thông báo",
         "Ghi chú: (để trống)",
         "- Hệ thống báo 'Thao tác thất bại!' và hiện lỗi đỏ dưới khung Ghi chú duyệt\n"
         "- Phiếu vẫn ở 'Chờ KT duyệt'"),

        ("019", "Ghi chú duyệt không bắt buộc khi Duyệt", "P1",
         "Phiếu P Chờ TP duyệt, tài khoản E đang mở màn xem, khung 'Ghi chú duyệt' để trống",
         "1. Bấm 'TP duyệt'\n2. Kiểm tra trạng thái\n3. Mở lại phiếu đọc bảng Lịch sử ghi chú duyệt",
         "Ghi chú: (để trống)",
         "- Phiếu duyệt thành công, chuyển sang cấp tiếp theo\n"
         "- Bảng Lịch sử ghi chú duyệt VẪN có một dòng của Trưởng phòng với cột Nội dung ghi chú "
         "để trống"),

        ("020", "Ghi chú duyệt của mỗi cấp được lưu riêng", "P0",
         "Phiếu P đi qua: Trưởng phòng duyệt kèm ghi chú 'Đồng ý', Ban giám đốc duyệt kèm ghi chú "
         "'Đã kiểm tra hợp đồng', Kế toán duyệt kèm ghi chú 'Đã cập nhật kho'",
         "1. Sau khi duyệt xong hết cấp, mở màn xem phiếu P\n2. Đọc bảng 'Lịch sử ghi chú duyệt'",
         "3 cấp, 3 ghi chú khác nhau",
         "- Bảng có đúng 3 dòng, mỗi dòng đúng người duyệt và đúng nội dung ghi chú của cấp đó\n"
         "- Ghi chú cấp sau KHÔNG ghi đè ghi chú cấp trước"),

        ("021", "Duyệt khi số lượng nguồn đã bị dùng hết", "P0",
         "Phiếu P Chờ KT duyệt chuyển 12 hàng X. Trong lúc chờ, số hàng X mà người lập giữ cho khách "
         "nguồn đã bị xuất hết, còn 0",
         "1. Đăng nhập G, mở phiếu P\n2. Bấm 'KT Duyệt'\n3. Đọc thông báo",
         "Đang giữ còn 0 · chuyển 12",
         "- Hệ thống báo 'Hàng <tên hàng> Không đủ số lượng xuất do đã yêu cầu xuất hàng!'\n"
         "- Phiếu không chuyển sang Đã duyệt\n- Số lượng hàng giữ không đổi"),

        ("022", "Duyệt khi hàng đang nằm trong yêu cầu xuất hàng chưa hoàn thành", "P0",
         "Phiếu P Chờ KT duyệt chuyển 12 hàng X. Người lập đang giữ 12 hàng X cho khách nguồn NHƯNG "
         "có một yêu cầu xuất hàng chưa hoàn thành đang chiếm 5 trong số đó",
         "1. Đăng nhập G, mở phiếu P\n2. Bấm 'KT Duyệt'\n3. Đọc thông báo",
         "Đang giữ 12 · đã yêu cầu xuất 5 · chuyển 12",
         "- Hệ thống báo 'Hàng <tên hàng> Không đủ số lượng xuất do đã yêu cầu xuất hàng!'\n"
         "- Phiếu không chuyển sang Đã duyệt\n"
         "⚠️ Số khả dụng để điều chuyển = số đang giữ trừ số đã nằm trong yêu cầu xuất hàng"),

        ("023", "Trưởng phòng bị chặn duyệt khi phòng còn nhân viên quá hạn", "P0",
         "Công ty bật cấu hình chặn quá hạn với thao tác 'Duyệt điều chuyển hàng giữ'. Phòng do Trưởng "
         "phòng E quản lý còn nhân viên đang quá hạn. Phiếu P Chờ TP duyệt",
         "1. Đăng nhập E, mở phiếu P\n2. Bấm 'TP duyệt'\n3. Đọc thông báo\n4. Kiểm tra trạng thái",
         "Tài khoản: E · phòng có nhân viên quá hạn",
         "- Hệ thống chặn, hiện thông báo cảnh báo về tình trạng quá hạn\n"
         "- Phiếu P vẫn ở 'Chờ TP duyệt'"),

        ("024", "Nút duyệt khóa lại trong lúc xử lý", "P1",
         "Phiếu P Chờ KT duyệt, tài khoản G đang mở màn xem",
         "1. Bấm 'KT Duyệt'\n2. Quan sát nút ngay sau khi bấm",
         "—",
         "- Nút đổi sang biểu tượng đang quay và không bấm lại được\n"
         "- Không tạo ra hai lần duyệt cho cùng một phiếu"),

        ("025", "Sau khi duyệt và sau khi Không duyệt đều quay về màn chờ duyệt", "P1",
         "Tài khoản G đang mở phiếu P và phiếu S từ màn chờ duyệt",
         "1. Với phiếu P: bấm 'KT Duyệt', quan sát trang\n"
         "2. Với phiếu S: nhập ghi chú, bấm 'Không duyệt', quan sát trang",
         "—",
         "- Cả hai đều quay về màn danh sách chờ duyệt\n"
         "- Cả hai phiếu không còn trong lưới chờ duyệt"),
    ]),

    # ----------------------------------------------------------------- VI
    ("VI", "XÓA", [
        ("001", "Xóa phiếu bị Không duyệt do mình lập", "P0",
         "Tài khoản A lập phiếu P đã bị Không duyệt, có 2 dòng hàng",
         "1. Đăng nhập A, bấm bánh răng của phiếu P, chọn 'Xóa'\n2. Xác nhận\n"
         "3. Tìm lại phiếu P trên lưới",
         "Phiếu P — Không duyệt",
         "- Thông báo 'Xóa phiếu thành công!'\n- Phiếu P biến mất khỏi lưới\n"
         "- Các dòng hàng của phiếu cũng bị xóa theo"),

        ("002", "Xóa phiếu không làm đổi hàng đang giữ", "P0",
         "Phiếu P bị Không duyệt, chuyển 12 hàng X. Trước khi xóa, người lập đang giữ 12 hàng X cho "
         "khách KH001",
         "1. Xóa phiếu P\n2. Vào Danh sách hàng giữ tìm hàng X của người lập",
         "Hàng X: 12 · KH001",
         "- Hàng X vẫn 12 đơn vị cho khách KH001, hạn giữ không đổi\n"
         "- Người nhận không phát sinh dòng giữ nào"),

        ("003", "Không xóa được phiếu đang chờ duyệt", "P0",
         "Phiếu Q của tài khoản A đang ở 'Chờ TP duyệt'",
         "1. Đăng nhập A, bấm bánh răng của phiếu Q\n"
         "2. Dùng công cụ kiểm thử gọi thẳng chức năng Xóa phiếu Q\n3. Tìm lại phiếu Q trên lưới",
         "Phiếu Q — Chờ TP duyệt",
         "- Menu không có mục 'Xóa'\n- Gọi thẳng chức năng Xóa bị từ chối với 'Không thể xóa!'\n"
         "- Phiếu Q vẫn còn"),

        ("004", "Không xóa được phiếu Đã duyệt", "P0",
         "Phiếu R của tài khoản A đang ở 'Đã duyệt'",
         "1. Đăng nhập A, bấm bánh răng của phiếu R\n"
         "2. Dùng công cụ kiểm thử gọi thẳng chức năng Xóa phiếu R\n3. Tìm lại phiếu R",
         "Phiếu R — Đã duyệt",
         "- Menu không có mục 'Xóa'\n- Gọi thẳng chức năng Xóa báo 'Không thể xóa!'\n"
         "- Phiếu R vẫn còn và số lượng hàng giữ đã chuyển không bị hoàn lại"),

        ("005", "Xóa xong quay về màn danh sách", "P1",
         "Đang ở màn danh sách, có phiếu bị Không duyệt",
         "1. Xóa một phiếu bị Không duyệt\n2. Quan sát trang sau khi xóa",
         "—",
         "- Vẫn ở màn danh sách và lưới đã nạp lại\n"
         "⚠️ Ghi nhận: lưới sau khi xóa hiển thị theo phạm vi mặc định (chỉ phiếu do mình lập), "
         "không giữ bộ lọc đang dùng trước đó"),
    ]),

    # ---------------------------------------------------------------- VII
    ("VII", "XUẤT EXCEL / IN", [
        ("001", "Xuất Excel danh sách phiếu", "P0",
         "Lưới đang hiện 12 phiếu, không lọc gì",
         "1. Bấm nút 'Xuất excel' phía trên lưới\n2. Mở tệp tải về",
         "—",
         "- Tệp tải về tên 'danh_sach_phieu_dieu_chuyen_hang_giu'\n"
         "- Có tiêu đề 'DANH SÁCH PHIẾU YÊU CẦU ĐIỀU CHUYỂN HÀNG GIỮ' và phần đầu trang của công ty\n"
         "- Bảng có 9 cột: STT · Mã phiếu · Ngày lập · Người nhận · Khách nhận · Người lập · "
         "Trạng thái · Người duyệt · Ngày duyệt\n- Có đủ 12 dòng"),

        ("002", "Xuất Excel áp đúng bộ lọc đang dùng", "P0",
         "Đang lọc Trạng thái = Đã duyệt, lưới còn 4 dòng",
         "1. Bấm 'Xuất excel'\n2. Mở tệp và đếm số dòng",
         "Trạng thái: Đã duyệt",
         "- Tệp chỉ có 4 dòng, tất cả đều là Đã duyệt\n"
         "⚠️ Nếu tệp ra đủ 12 dòng thì bộ lọc chưa được truyền vào lúc xuất"),

        ("003", "Xuất Excel có dòng ghi khoảng ngày đang lọc", "P1",
         "Đang lọc Từ ngày = 01/03/2026, Đến ngày = 10/03/2026",
         "1. Bấm 'Xuất excel'\n2. Mở tệp và đọc phần đầu",
         "Từ 01/03/2026 đến 10/03/2026",
         "- Có dòng 'Từ ngày 01/03/2026 đến ngày 10/03/2026' phía trên bảng"),

        ("004", "Xuất Excel khi chỉ nhập một đầu ngày", "P2",
         "Đang lọc Từ ngày = 01/03/2026, để trống Đến ngày",
         "1. Bấm 'Xuất excel'\n2. Đọc dòng ghi khoảng ngày",
         "Từ 01/03/2026",
         "- Dòng ghi 'Từ ngày 01/03/2026', không hiện phần 'đến ngày' rỗng"),

        ("005", "Định dạng Ngày lập trong bản xuất khác với trên lưới", "P1",
         "Có phiếu lập lúc 14h05 ngày 05/03/2026",
         "1. Đọc cột Ngày lập của phiếu đó trên lưới\n2. Bấm 'Xuất excel' và đọc cột Ngày lập",
         "Phiếu lập 05/03/2026 14:05",
         "- Trên lưới: 05/03/2026\n"
         "⚠️ Trong bản xuất: hiển thị theo thứ tự năm/tháng/ngày kèm giờ phút giây "
         "(dạng 2026/03/05 14:05:00) — ghi nhận đúng như nhìn thấy"),

        ("006", "In danh sách phiếu", "P0",
         "Lưới đang hiện 12 phiếu",
         "1. Bấm nút 'In' phía trên lưới\n2. Quan sát tab mới mở ra",
         "—",
         "- Mở tab mới với bản in khổ ngang\n- Bảng có đủ 9 cột và đủ 12 dòng\n"
         "⚠️ Nếu trang in ra TRẮNG thì nguyên nhân là mẫu in của danh sách này chưa được khai trong "
         "hệ thống — ghi nhận rõ để đội cấu hình xử lý, không phải lỗi thao tác"),

        ("007", "In danh sách áp đúng bộ lọc đang dùng", "P0",
         "Đang lọc Trạng thái = Đã duyệt, lưới còn 4 dòng",
         "1. Bấm 'In'\n2. Đếm số dòng trên bản in",
         "Trạng thái: Đã duyệt",
         "- Bản in chỉ có 4 dòng, tất cả đều là Đã duyệt"),

        ("008", "In một phiếu", "P0",
         "Phiếu P có 2 dòng hàng, người nhận Trần Thị B, khách nhận KH001",
         "1. Bấm bánh răng của phiếu P, chọn 'In'\n2. Quan sát tab mới mở ra",
         "Phiếu P",
         "- Mở tab mới với bản in khổ ngang, tiêu đề 'Phiếu điều chuyển hàng giữ'\n"
         "- Có Số phiếu, Ngày lập, Người nhận, Khách hàng nhận, Ghi chú\n"
         "- Bảng có 8 cột: STT · Tên hàng · Mã hàng · ĐVT · Từ xuất giữ · Đang giữ · Chuyển · Hợp đồng"),

        ("009", "Bản in phiếu hiển thị ô Từ xuất giữ đầy đủ", "P1",
         "Phiếu P có dòng lấy từ hàng giữ: 12 đơn vị, khách 'Công ty TNHH Minh Long', hạn 30/03/2026",
         "1. Mở bản in phiếu P\n2. Đọc ô ở cột 'Từ xuất giữ'",
         "—",
         "- Ô hiện '12 - Công ty TNHH Minh Long - 30/03/2026'"),

        ("010", "Bản in phiếu có bảng Lịch sử ghi chú duyệt", "P0",
         "Phiếu P đã qua: Trưởng phòng duyệt KHÔNG nhập ghi chú, Ban giám đốc duyệt ghi chú "
         "'Đồng ý chuyển'",
         "1. Mở bản in phiếu P\n2. Đọc bảng 'Lịch sử ghi chú duyệt' cuối bản in\n"
         "3. So với bảng cùng tên trên màn xem",
         "2 cấp đã duyệt, 1 cấp có ghi chú",
         "⚠️ Bản in CHỈ hiện 1 dòng (cấp có ghi chú), trong khi màn xem hiện 2 dòng\n"
         "⚠️ Bản in cũng chỉ có 2 cột (Người duyệt · Nội dung ghi chú), thiếu cột Thời gian duyệt "
         "so với màn xem — ghi nhận đúng như nhìn thấy"),

        ("011", "Bản in phiếu khi chưa ai duyệt", "P2",
         "Phiếu P vừa gửi, đang Chờ TP duyệt",
         "1. Mở bản in phiếu P\n2. Quan sát phần cuối bản in",
         "Phiếu P — chưa ai duyệt",
         "- Không có bảng 'Lịch sử ghi chú duyệt'\n- Bản in vẫn có đủ phần bảng hàng hóa"),

        ("012", "Mục In luôn có trong menu Hành động", "P1",
         "Có phiếu ở các trạng thái Chờ TP duyệt, Đã duyệt, Không duyệt",
         "1. Bấm bánh răng của từng phiếu\n2. Kiểm tra sự có mặt của mục In",
         "—",
         "- Cả 3 phiếu đều có mục 'In' trong menu\n"
         "⚠️ Menu Hành động KHÔNG có mục 'Xuất excel' cho từng phiếu — chỉ danh sách mới xuất được"),
    ]),

    # --------------------------------------------------------------- VIII
    ("VIII", "RÀNG BUỘC NHẬP LIỆU", [
        ("001", "Bỏ trống Người nhận", "P0",
         "Đang ở màn Tạo mới, đã chọn Khách hàng nhận và thêm 1 dòng hàng hợp lệ",
         "1. Để trống ô Người nhận\n2. Bấm 'Gửi'",
         "Người nhận: (để trống)",
         "- Hệ thống báo 'Tạo thất bại!' và hiện lỗi đỏ ngay dưới ô Người nhận\n"
         "- Không tạo ra phiếu mới"),

        ("002", "Bỏ trống Khách hàng nhận", "P0",
         "Đang ở màn Tạo mới, đã chọn Người nhận và thêm 1 dòng hàng hợp lệ",
         "1. Để trống ô Khách hàng nhận\n2. Bấm 'Gửi'",
         "Khách hàng nhận: (để trống)",
         "- Hệ thống báo 'Tạo thất bại!' và hiện lỗi đỏ ngay dưới ô Khách hàng nhận\n"
         "- Không tạo ra phiếu mới"),

        ("003", "Gửi khi bảng Chi tiết trống", "P0",
         "Đang ở màn Tạo mới, đã chọn Người nhận và Khách hàng nhận, chưa thêm dòng hàng nào",
         "1. Bấm 'Gửi'\n2. Đọc thông báo",
         "0 dòng hàng",
         "- Hệ thống báo 'Tạo thất bại!' và hiện lỗi đỏ dưới bảng Chi tiết\n"
         "- Không tạo ra phiếu mới"),

        ("004", "Thêm hàng nhưng chưa chọn 'Từ xuất giữ'", "P0",
         "Đang ở màn Tạo mới, đã chọn Người nhận và Khách hàng nhận, đã thêm 1 dòng hàng nhưng chưa "
         "chọn dòng nguồn",
         "1. Nhập ô 'Chuyển' = 5\n2. Bấm 'Gửi'",
         "Từ xuất giữ: (chưa chọn)",
         "- Hệ thống báo lỗi đỏ ngay dưới ô 'Từ xuất giữ'\n- Không tạo ra phiếu mới"),

        ("005", "Bỏ trống ô 'Chuyển'", "P0",
         "Đang ở màn Tạo mới, đã chọn đủ Người nhận, Khách hàng nhận và dòng nguồn",
         "1. Xóa trắng ô 'Chuyển'\n2. Bấm 'Gửi'",
         "Chuyển: (rỗng)",
         "- Hệ thống báo lỗi đỏ ngay dưới ô 'Chuyển'\n- Không tạo ra phiếu mới"),

        ("006", "Ô 'Chuyển' bằng 0", "P0",
         "Đang ở màn Tạo mới, đã chọn đủ thông tin, dòng nguồn có Đang giữ = 12",
         "1. Nhập ô 'Chuyển' = 0\n2. Bấm 'Gửi'",
         "Chuyển: 0",
         "- Hệ thống báo lỗi đỏ ngay dưới ô 'Chuyển'\n"
         "- Không tạo ra phiếu mới (số chuyển phải từ 1 trở lên)"),

        ("007", "Ô 'Chuyển' bằng đúng số Đang giữ", "P0",
         "Dòng nguồn có Đang giữ = 12",
         "1. Nhập ô 'Chuyển' = 12\n2. Bấm 'Gửi'",
         "Chuyển = 12 = Đang giữ",
         "- Phiếu được tạo thành công, trạng thái 'Chờ TP duyệt'\n- Không có cảnh báo nào"),

        ("008", "Hai dòng cùng trỏ về một dòng hàng giữ nguồn", "P0",
         "Hàng X của người lập có 1 dòng giữ cho khách KH001 hạn 30/03/2026",
         "1. Thêm hàng X vào bảng, chọn dòng nguồn đó, nhập Chuyển = 3\n"
         "2. Thêm hàng X lần nữa, chọn CÙNG dòng nguồn đó, nhập Chuyển = 4\n3. Bấm 'Gửi'",
         "2 dòng cùng một dòng nguồn",
         "- Hệ thống báo 'Tạo thất bại!' và hiện lỗi đỏ ở ô 'Từ xuất giữ'\n"
         "- Không tạo ra phiếu mới\n"
         "⚠️ Muốn chuyển nhiều lần từ cùng một dòng giữ thì phải gộp vào một dòng"),

        ("009", "Hai dòng khác hàng hóa nhưng dòng nguồn khác nhau thì hợp lệ", "P1",
         "Người lập giữ hàng X (khách KH001) và hàng Y (khách KH001), đều còn hạn",
         "1. Thêm hàng X, chọn dòng nguồn của hàng X, nhập Chuyển = 3\n"
         "2. Thêm hàng Y, chọn dòng nguồn của hàng Y, nhập Chuyển = 4\n3. Bấm 'Gửi'",
         "2 dòng, 2 dòng nguồn khác nhau",
         "- Phiếu được tạo thành công với 2 dòng hàng"),

        ("010", "Chuyển hàng đã hết hạn giữ", "P0",
         "Hàng X của người lập có dòng giữ cho khách KH002 đã quá hạn giữ. Người dùng cố tình chọn "
         "dòng này bằng cách sửa phiếu bị Không duyệt được lập từ trước khi hàng hết hạn",
         "1. Mở màn Sửa phiếu đó\n2. Giữ nguyên dòng hàng đã hết hạn\n3. Bấm 'Gửi'\n4. Đọc thông báo",
         "Hàng X đã hết hạn giữ",
         "- Hệ thống báo 'Hàng <tên hàng> đã hết hạn giữ (…)!'\n- Không lưu được phiếu\n"
         "⚠️ Ngày trong thông báo in theo thứ tự năm-tháng-ngày, khác định dạng trên màn hình"),

        ("011", "Chuyển vượt quá số đang giữ khi số liệu thay đổi giữa chừng", "P0",
         "Phiếu P bị Không duyệt, có dòng hàng X chuyển 12. Sau đó số hàng X người lập đang giữ giảm "
         "xuống còn 7",
         "1. Mở màn Sửa phiếu P\n2. Không sửa gì, bấm 'Gửi'\n3. Đọc thông báo",
         "Đang giữ 7 · chuyển 12",
         "- Hệ thống báo 'Hàng <tên hàng>: số lượng chuyển (12) vượt quá số lượng đang giữ (7)!'\n"
         "- Không lưu được phiếu"),

        ("012", "Chọn dòng hàng giữ không thuộc về mình", "P0",
         "Tài khoản A đang lập phiếu. Có một dòng hàng giữ thuộc về tài khoản B",
         "1. Dùng công cụ kiểm thử gọi thẳng chức năng Tạo phiếu, trỏ dòng hàng về dòng hàng giữ "
         "của B\n2. Đọc phản hồi",
         "Dòng hàng giữ của B",
         "- Hệ thống báo 'Hàng <tên hàng> không hợp lệ!'\n- Không tạo ra phiếu mới"),

        ("013", "Đính kèm tệp quá 13 MB", "P1",
         "Có sẵn tệp PDF 15 MB. Đang ở màn Tạo mới, đã điền hợp lệ",
         "1. Thêm ô đính kèm và chọn tệp 15 MB\n2. Bấm 'Gửi'",
         "Tệp: 15 MB",
         "- Hệ thống báo lỗi 'File không lớn hơn 13 MB' trên ô đính kèm\n- Không tạo ra phiếu mới"),

        ("014", "Đính kèm tệp sai định dạng", "P1",
         "Có sẵn tệp 'ghi-am.mp3'. Đang ở màn Tạo mới, đã điền hợp lệ",
         "1. Thêm ô đính kèm, chuyển bộ lọc sang 'All files' và chọn tệp mp3\n2. Bấm 'Gửi'",
         "Tệp: ghi-am.mp3",
         "- Hệ thống báo lỗi 'Chỉ nhận file .pdf, .png, .jpg, .docx, .doc, .xls, .xlsx, .jpeg'\n"
         "- Không tạo ra phiếu mới"),

        ("015", "Thêm ô đính kèm nhưng không chọn tệp", "P1",
         "Đang ở màn Tạo mới, đã điền hợp lệ",
         "1. Bấm dấu cộng thêm 1 ô đính kèm nhưng KHÔNG chọn tệp\n2. Bấm 'Gửi'",
         "1 ô đính kèm rỗng",
         "- Hệ thống báo lỗi 'Bắt buộc phải chọn' trên ô đính kèm rỗng\n- Không tạo ra phiếu mới"),

        ("016", "Đính kèm nhiều tệp hợp lệ cùng lúc", "P1",
         "Có sẵn tệp 'bien-ban.pdf' và 'anh-hang.jpg'. Đang ở màn Tạo mới, đã điền hợp lệ",
         "1. Thêm 2 ô đính kèm, chọn 2 tệp trên\n2. Bấm 'Gửi'\n3. Mở màn xem của phiếu vừa tạo",
         "2 tệp hợp lệ",
         "- Phiếu tạo thành công\n- Màn xem hiện cả 2 tệp, bấm vào mở xem được"),

        ("017", "Ghi chú để trống", "P1",
         "Đang ở màn Tạo mới, đã điền hợp lệ, ô Ghi chú để trống",
         "1. Bấm 'Gửi'",
         "Ghi chú: (để trống)",
         "- Phiếu được tạo thành công, ô Ghi chú không bắt buộc"),

        ("018", "Ghi chú nhập chuỗi dài", "P2",
         "Đang ở màn Tạo mới, đã điền hợp lệ",
         "1. Dán đoạn văn dài 500 ký tự vào ô Ghi chú\n2. Bấm 'Gửi'\n"
         "3. Mở màn xem của phiếu vừa tạo và đọc ô Ghi chú",
         "Ghi chú: 500 ký tự",
         "- Ghi nhận kết quả thực tế: phiếu tạo được và nội dung ghi chú hiển thị lại đủ hay bị cắt "
         "bớt\n- Trang không báo lỗi hệ thống"),
    ]),

    # ----------------------------------------------------------------- IX
    ("IX", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", [
        ("001", "Chặn tạo phiếu khi người lập có hàng mượn quá hạn", "P0",
         "Công ty bật cấu hình chặn nhóm 'Hàng mượn quá hạn' với thao tác 'Điều chuyển hàng giữ'. "
         "Tài khoản A đang có phiếu mượn quá hạn chưa trả",
         "1. Đăng nhập A\n2. Bấm 'Tạo mới' ở màn danh sách\n3. Quan sát trang",
         "Tài khoản: A có hàng mượn quá hạn",
         "- Hệ thống không mở màn Tạo mới, quay lại màn danh sách kèm cảnh báo "
         "'Có hàng mượn quá hạn!'"),

        ("002", "Chặn tạo phiếu khi người lập có hàng nhập thẳng quá hạn", "P0",
         "Công ty bật cấu hình chặn nhóm 'Hàng nhập thẳng quá hạn' với thao tác 'Điều chuyển hàng "
         "giữ'. Tài khoản A có hàng nhập thẳng đã quá số ngày cho phép",
         "1. Đăng nhập A\n2. Bấm 'Tạo mới'\n3. Quan sát trang",
         "Tài khoản: A có hàng nhập thẳng quá hạn",
         "- Hệ thống không mở màn Tạo mới, quay lại kèm cảnh báo 'Có hàng nhập thẳng quá hạn!'"),

        ("003", "Hàng GIỮ quá hạn không chặn màn này", "P0",
         "Công ty bật cấu hình chặn nhóm 'Hàng giữ quá hạn' cho các thao tác khác. Tài khoản A đang "
         "có hàng giữ quá hạn nhưng vẫn còn hàng giữ CÒN HẠN để chuyển",
         "1. Đăng nhập A\n2. Bấm 'Tạo mới'\n3. Điền hợp lệ và bấm 'Gửi'",
         "Tài khoản: A có hàng giữ quá hạn",
         "- Màn Tạo mới mở bình thường\n- Phiếu được tạo thành công\n"
         "⚠️ Nhóm chặn 'Hàng giữ quá hạn' không áp cho màn điều chuyển hàng giữ"),

        ("004", "Người quản trị cao nhất không bị chặn quá hạn", "P1",
         "Tài khoản quản trị cao nhất đang có hàng mượn quá hạn, công ty đang bật cấu hình chặn",
         "1. Đăng nhập bằng tài khoản quản trị cao nhất\n2. Bấm 'Tạo mới'",
         "Tài khoản: quản trị cao nhất",
         "- Màn Tạo mới mở bình thường, không có cảnh báo chặn"),

        ("005", "Hai người duyệt cùng một phiếu gần như đồng thời", "P0",
         "Phiếu P Chờ KT duyệt chuyển 12 hàng X. Hai tài khoản G1 và G2 cùng có quyền Kế toán duyệt "
         "hàng giữ, cùng mở màn xem phiếu P",
         "1. G1 bấm 'KT Duyệt', chờ thành công\n2. G2 bấm 'KT Duyệt' trên tab đã mở sẵn\n"
         "3. Mở lại phiếu P kiểm tra\n4. Vào Danh sách hàng giữ kiểm tra số lượng",
         "Phiếu P · 2 người duyệt",
         "- Phiếu P chỉ ghi nhận 1 người duyệt và 1 ngày duyệt\n"
         "- Số lượng chỉ được chuyển MỘT lần: người lập giảm đúng 12, người nhận tăng đúng 12\n"
         "⚠️ Trường hợp dễ sinh sai lệch số lượng hàng giữ nhất — kiểm tra kỹ hai đầu"),

        ("006", "Người lập sửa phiếu trong lúc phiếu đã được gửi ở tab khác", "P1",
         "Phiếu P bị Không duyệt, tài khoản A mở màn Sửa ở 2 tab",
         "1. Ở tab 1 bấm 'Gửi' → phiếu sang Chờ TP duyệt\n2. Ở tab 2 bấm 'Gửi'\n3. Mở lại phiếu P",
         "Phiếu P",
         "- Ghi nhận kết quả thực tế ở tab 2 và trạng thái cuối cùng của phiếu\n"
         "- Phiếu P không được sinh thành hai phiếu khác nhau\n"
         "- Số dòng hàng của phiếu không bị nhân đôi"),

        ("007", "Xóa phiếu trên tab này rồi thao tác trên tab kia", "P1",
         "Phiếu P bị Không duyệt, tài khoản A mở phiếu P ở 2 tab",
         "1. Ở tab 1 xóa phiếu P\n2. Ở tab 2 bấm 'Gửi'\n3. Quan sát kết quả",
         "Phiếu P đã bị xóa",
         "- Hệ thống báo dữ liệu đã thay đổi, không treo trang\n- Không phục hồi phiếu đã xóa"),

        ("008", "Số Đang giữ trên màn xem được nạp lại theo thời gian thực", "P1",
         "Phiếu P Chờ KT duyệt chuyển hàng X. Trong lúc chờ, số hàng X mà người lập giữ giảm từ 12 "
         "xuống 7",
         "1. Đăng nhập G, mở màn xem phiếu P\n2. Đọc cột 'Đang giữ' của hàng X",
         "Đang giữ: 12 → 7",
         "- Cột 'Đang giữ' hiện 7, tức số hiện tại chứ không phải số lúc lập phiếu"),

        ("009", "Người lập đổi công ty thì không thấy hàng giữ ở công ty cũ", "P1",
         "Tài khoản A thuộc công ty 1, đang giữ hàng ở công ty 1. A được chuyển sang công ty 4",
         "1. Đăng nhập A (đang ở công ty 4)\n2. Bấm 'Tạo mới'\n3. Bấm nút dấu cộng tìm hàng",
         "Tài khoản: A · công ty 4",
         "- Cửa sổ tìm hàng không hiện hàng giữ thuộc công ty 1"),

        ("010", "Điều chuyển cho chính mình với khách hàng khác", "P1",
         "Tài khoản A giữ hàng X 12 đơn vị cho khách KH001, hạn 30/03/2026. Lập phiếu chuyển 5 sang "
         "chính tài khoản A nhưng khách nhận là KH002",
         "1. Lập phiếu với Người nhận = chính mình, Khách hàng nhận = KH002, Chuyển = 5\n"
         "2. Duyệt hết cấp tới Kế toán duyệt\n3. Mở Danh sách hàng giữ của tài khoản A",
         "A → A · KH001 → KH002",
         "- Tài khoản A còn 7 hàng X cho khách KH001 hạn 30/03/2026\n"
         "- Tài khoản A có thêm 5 hàng X cho khách KH002 hạn 30/03/2026\n- Tổng vẫn là 12"),
    ]),

    # ------------------------------------------------------------------ X
    ("X", "E2E FLOW", [
        ("001", "Luồng đầy đủ không qua Ban giám đốc", "P0",
         "Tài khoản A (phòng KD1) giữ hàng X 12 đơn vị cho khách KH001, hạn 30/03/2026, giá trị nhỏ "
         "hơn 'Giá trị giữ hàng khác'. Người nhận Trần Thị B thuộc phòng KD2, khách nhận KH002. "
         "E là Trưởng phòng quản lý KD2, G là Kế toán duyệt. Hôm nay 05/03/2026",
         "1. A: Tạo mới → Người nhận Trần Thị B → Khách hàng nhận KH002 → thêm hàng X → chọn dòng "
         "nguồn → Chuyển = 12 → 'Gửi'\n"
         "2. E: mở phiếu → 'TP duyệt'\n3. G: mở phiếu → 'KT Duyệt'\n"
         "4. Mở Danh sách hàng giữ kiểm tra cả A và Trần Thị B",
         "Hàng X · 12 · A/KH001 → B/KH002",
         "- Sau bước 1: trạng thái 'Chờ TP duyệt', E nhận thông báo\n"
         "- Sau bước 2: trạng thái 'Chờ KT duyệt', G nhận thông báo\n"
         "- Sau bước 3: trạng thái 'Đã duyệt', có Người duyệt và Ngày duyệt, A nhận thông báo\n"
         "- Danh sách hàng giữ: A còn 0 hàng X cho KH001; Trần Thị B có 12 hàng X cho KH002 "
         "hạn 30/03/2026"),

        ("002", "Luồng đầy đủ có qua Ban giám đốc", "P0",
         "Giống trên nhưng giá trị hàng xin điều chuyển vượt 'Giá trị giữ hàng khác'. F là Ban giám "
         "đốc duyệt hàng giữ",
         "1. A: Tạo mới → điền hợp lệ → 'Gửi'\n2. E: 'TP duyệt'\n3. F: 'BGĐ duyệt'\n"
         "4. G: 'KT Duyệt'\n5. Kiểm tra Danh sách hàng giữ",
         "Giá trị vượt ngưỡng",
         "- Sau bước 2: trạng thái 'Chờ BGĐ duyệt', F nhận thông báo\n"
         "- Sau bước 3: trạng thái 'Chờ KT duyệt', G nhận thông báo\n"
         "- Sau bước 4: trạng thái 'Đã duyệt' và số lượng đã chuyển sang người nhận\n"
         "- Bảng Lịch sử ghi chú duyệt có đủ 3 dòng của 3 cấp"),

        ("003", "Luồng bị Không duyệt rồi sửa và làm lại thành công", "P0",
         "Tài khoản A giữ hàng X 12 đơn vị cho khách KH001. Hôm nay 05/03/2026",
         "1. A: Tạo mới → Khách hàng nhận KH002 → Chuyển = 12 → 'Gửi'\n"
         "2. E: nhập ghi chú 'Sai khách hàng nhận' → 'Không duyệt'\n"
         "3. A: mở phiếu đọc ghi chú, vào Sửa → đổi Khách hàng nhận sang KH003 → 'Gửi'\n"
         "4. E: 'TP duyệt'\n5. G: 'KT Duyệt'\n6. Kiểm tra Danh sách hàng giữ",
         "KH002 → KH003",
         "- Sau bước 2: phiếu ở 'Không duyệt', A nhận thông báo, bảng Lịch sử ghi chú duyệt có dòng "
         "'Sai khách hàng nhận'\n"
         "- Sau bước 3: phiếu về 'Chờ TP duyệt', menu Hành động không còn Sửa và Xóa\n"
         "- Sau bước 5: phiếu 'Đã duyệt', hàng X chuyển sang người nhận với khách KH003\n"
         "- Bảng Lịch sử ghi chú duyệt vẫn giữ dòng của lần từ chối trước"),

        ("004", "Luồng chuyển một phần rồi chuyển tiếp phần còn lại", "P0",
         "Tài khoản A giữ hàng X 12 đơn vị cho khách KH001, hạn 30/03/2026. Hôm nay 05/03/2026",
         "1. A lập phiếu 1 chuyển 5 sang Trần Thị B / khách KH002, được duyệt hết cấp\n"
         "2. Kiểm tra Danh sách hàng giữ\n"
         "3. A lập phiếu 2 chuyển 7 còn lại sang cùng Trần Thị B / khách KH002, được duyệt hết cấp\n"
         "4. Kiểm tra lại Danh sách hàng giữ",
         "12 = 5 + 7",
         "- Sau bước 2: A còn 7, Trần Thị B có 5 hạn 30/03/2026\n"
         "- Ở bước 3, cửa sổ chọn dòng nguồn hiện dòng còn lại với số lượng 7\n"
         "- Sau bước 4: A còn 0, Trần Thị B có MỘT dòng duy nhất 12 hạn 30/03/2026 (cộng gộp)"),

        ("005", "Luồng nhiều dòng hàng nhiều dòng nguồn trong một phiếu", "P0",
         "Tài khoản A giữ: hàng X cho khách KH001 (12, hạn 20/03/2026), hàng Y cho khách KH001 "
         "(8, hạn 30/03/2026), hàng X cho khách KH002 (5, hạn 30/03/2026) — đều còn hạn",
         "1. A: Tạo mới → Người nhận Trần Thị B → Khách hàng nhận KH003 → thêm 3 dòng, mỗi dòng chọn "
         "đúng dòng nguồn tương ứng, nhập Chuyển lần lượt 12 · 8 · 5 → 'Gửi'\n"
         "2. E: 'TP duyệt'\n3. G: 'KT Duyệt'\n4. Kiểm tra Danh sách hàng giữ của A và Trần Thị B",
         "3 dòng · 3 dòng nguồn khác nhau",
         "- Phiếu tạo được, không báo lỗi trùng dòng nguồn\n"
         "- Sau bước 3: A còn 0 ở cả 3 dòng nguồn\n"
         "- Trần Thị B / khách KH003 có: hàng X hạn 20/03/2026 số lượng 12, hàng Y hạn 30/03/2026 "
         "số lượng 8, hàng X hạn 30/03/2026 số lượng 5\n"
         "⚠️ Hai dòng hàng X phải nằm riêng vì hạn giữ khác nhau"),

        ("006", "Luồng bị chặn ở bước duyệt cuối do hàng đã nằm trong yêu cầu xuất", "P0",
         "Tài khoản A giữ hàng X 12 đơn vị cho khách KH001. Sau khi phiếu điều chuyển đã qua Trưởng "
         "phòng, A lập một yêu cầu xuất hàng chiếm 5 hàng X cho khách KH001, chưa hoàn thành",
         "1. Phiếu điều chuyển 12 hàng X đang ở 'Chờ KT duyệt'\n2. G: bấm 'KT Duyệt'\n"
         "3. Đọc thông báo và kiểm tra trạng thái\n"
         "4. A sửa lại không được (phiếu chưa bị từ chối) — G nhập ghi chú và bấm 'Không duyệt'\n"
         "5. A: mở Sửa, đổi Chuyển thành 7, bấm 'Gửi'\n6. Duyệt lại hết cấp và kiểm tra kho",
         "Đang giữ 12 · đã yêu cầu xuất 5",
         "- Bước 2: hệ thống báo 'Hàng <tên hàng> Không đủ số lượng xuất do đã yêu cầu xuất hàng!', "
         "phiếu vẫn ở 'Chờ KT duyệt'\n"
         "- Bước 4: phiếu chuyển sang 'Không duyệt', khi đó mới sửa được\n"
         "- Sau bước 6: phiếu 'Đã duyệt', A còn 5 hàng X cho KH001, người nhận có 7"),

        ("007", "Luồng lập phiếu, bị từ chối rồi xóa hẳn", "P1",
         "Tài khoản A giữ hàng X 12 đơn vị cho khách KH001",
         "1. A: Tạo mới → điền hợp lệ → 'Gửi'\n2. E: nhập ghi chú → 'Không duyệt'\n"
         "3. Đăng nhập tài khoản C (quyền xem theo công ty) kiểm tra lưới\n"
         "4. A: xóa phiếu\n5. Kiểm tra Danh sách hàng giữ của A",
         "Phiếu bị Không duyệt rồi xóa",
         "- Sau bước 2: phiếu ở 'Không duyệt'\n"
         "- Bước 3: C KHÔNG thấy phiếu này trên lưới\n"
         "- Sau bước 4: phiếu biến mất, có thông báo 'Xóa phiếu thành công!'\n"
         "- Bước 5: A vẫn giữ đủ 12 hàng X cho khách KH001, hạn giữ không đổi"),
    ]),
]

build(
    output_file=OUTPUT_FILE,
    sheet_name="Trang tính1",
    feature_name=FEATURE_NAME,
    module_name=MODULE_NAME,
    description_block=DESCRIPTION_BLOCK,
    role_tcs=ROLE_TCS,
    sections=SECTIONS,
)
