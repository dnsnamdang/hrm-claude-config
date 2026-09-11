# -*- coding: utf-8 -*-
"""Generate testcase Excel cho man ERP: Phieu Yeu cau gia han giu hang.

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
# tc_engine.py nam trong skill testcase-documenter cua repo config (nhanh hrm/)
ENGINE_DIR = os.path.normpath(os.path.join(
    HERE, "..", "..", "..", "hrm", ".claude", "skills",
    "testcase-documenter", "assets"))
sys.path.insert(0, ENGINE_DIR)

from tc_engine import build  # noqa: E402

OUTPUT_FILE = os.path.join(HERE, "testcase.xlsx")
FEATURE_NAME = "Phiếu Yêu cầu gia hạn giữ hàng"
MODULE_NAME = "Gia hạn hàng giữ"

# =========================================================================
# 9 MUC MO TA
# =========================================================================
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Cho phép người phụ trách hàng giữ lập phiếu xin kéo dài thời gian giữ hàng cho những mặt hàng "
     "đang giữ sắp hết hạn.\n"
     "Phiếu đi qua các cấp duyệt: Trưởng phòng → (Ban giám đốc, khi vượt ngưỡng) → Kế toán. "
     "Khi Kế toán duyệt, hệ thống mới thực sự dời hạn giữ của hàng sang ngày mới.\n"
     "Đường vào: menu Kho → nhóm Giữ hàng → Phiếu Yêu cầu gia hạn giữ hàng. "
     "Người duyệt vào menu Kế toán → nhóm Hàng giữ → Phiếu yêu cầu gia hạn hàng giữ chờ duyệt."),

    ("2. Đối tượng được tính / hiển thị",
     "► Màn danh sách hiển thị phiếu ở 5 trạng thái: Đang tạo · Chờ TP duyệt · Chờ BGĐ duyệt · "
     "Chờ KT duyệt · Đã duyệt.\n"
     "► Phiếu ở trạng thái Đang tạo CHỈ người lập ra nó mới nhìn thấy, kể cả người có quyền xem "
     "toàn công ty.\n"
     "► Bảng Chi tiết ở màn Tạo mới chỉ nạp những dòng hàng đang giữ thỏa ĐỒNG THỜI 4 điều kiện:\n"
     "   - do chính người đang đăng nhập giữ;\n"
     "   - thuộc công ty người đang đăng nhập;\n"
     "   - số lượng đang giữ còn lớn hơn 0;\n"
     "   - hạn giữ hiện tại rơi vào khoảng từ hôm nay trở về trước cho tới hôm nay cộng thêm "
     "'Số ngày cảnh báo (mượn/giữ hàng)' khai trong Cấu hình hệ thống.\n"
     "► Màn Xem của người ĐANG có lượt duyệt hiển thị TẤT CẢ dòng hàng của phiếu (kể cả dòng không "
     "tích chọn) để người duyệt còn tích thêm; người xem thường chỉ thấy dòng đã tích 'cần gia hạn'."),

    ("3. Đối tượng bị ẩn / không tính",
     "► Phiếu Đang tạo của người khác — không ai khác thấy.\n"
     "► Hàng giữ của nhân viên khác, hàng giữ đã hết số lượng, hàng giữ còn hạn xa hơn 'Số ngày cảnh "
     "báo (mượn/giữ hàng)' — không nạp vào bảng Chi tiết.\n"
     "► Màn 'Phiếu yêu cầu gia hạn hàng giữ chờ duyệt' ẩn phiếu Đang tạo và ẩn phiếu của công ty khác.\n"
     "► Dòng hàng có 'Cần gia hạn' bằng 0 không hiển thị ở màn Xem.\n"
     "► Cột 'Đang giữ' bị ẩn khi phiếu đã ở trạng thái Đã duyệt.\n"
     "► Nút Sửa / Xóa bị ẩn khi phiếu không còn ở trạng thái Đang tạo hoặc người xem không phải "
     "người lập."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Ô 'Từ ngày' và 'Đến ngày' trên màn danh sách lọc theo cột NGÀY LẬP của phiếu (không phải Ngày "
     "duyệt, cũng không phải hạn giữ).\n"
     "'Đến ngày' lấy trọn cả ngày được chọn.\n"
     "Khi bấm Xuất excel, khoảng ngày đang lọc được in thành dòng 'Từ ngày … đến ngày …' ở đầu file."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Một phiếu gồm phần Thông tin chung (Ghi chú, File đính kèm, Phòng ban yêu cầu, Người lập, "
     "Ngày lập) và nhiều dòng hàng hóa.\n"
     "Mỗi dòng hàng hóa gắn với đúng MỘT dòng hàng đang giữ, mà một dòng hàng đang giữ được xác định "
     "bởi bộ ba: nhân viên giữ + khách hàng + hàng hóa + hạn giữ.\n"
     "Mỗi dòng có thể gắn thêm một Đơn hàng/Hợp đồng chọn từ cửa sổ tìm kiếm (không bắt buộc)."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "► Dòng 'Tổng cộng' chỉ cộng những dòng ĐƯỢC TÍCH CHỌN; bỏ tích là số tổng giảm ngay.\n"
     "► 'Đang giữ' và 'Cần gia hạn' luôn quy đổi theo Đơn vị tính đang chọn trên dòng đó; đổi đơn vị "
     "tính là hai con số này đổi theo hệ số.\n"
     "► Khi Kế toán duyệt: hệ thống TRỪ số lượng ở dòng hàng giữ hạn cũ và CỘNG vào dòng hàng giữ hạn "
     "mới. Nếu đã tồn tại sẵn một dòng cùng nhân viên + khách hàng + hàng hóa + đúng hạn mới thì cộng "
     "gộp vào dòng đó chứ không tạo dòng mới.\n"
     "► Dòng nào có hạn giữ mới TRÙNG y hệt hạn giữ hiện tại thì được bỏ qua, không phát sinh chuyển "
     "số lượng."),

    ("7. Phân quyền cấp",
     "• Xem phiếu hàng giữ theo tổng công ty — thấy phiếu của mọi công ty.\n"
     "• Xem phiếu hàng giữ theo công ty — thấy phiếu trong công ty mình.\n"
     "• Xem phiếu hàng giữ theo phòng ban — thấy phiếu của các phòng ban mình quản lý.\n"
     "• Không có ba quyền trên — chỉ thấy phiếu do chính mình lập.\n"
     "• Trưởng phòng duyệt hàng giữ — duyệt phiếu Chờ TP duyệt thuộc phòng ban mình quản lý.\n"
     "• Ban giám đốc duyệt hàng giữ — duyệt phiếu Chờ BGĐ duyệt trong công ty mình.\n"
     "• Kế toán duyệt hàng giữ — duyệt phiếu Chờ KT duyệt trong công ty mình (bước duyệt cuối).\n"
     "• Kế toán kho — vào được màn danh sách dành cho kế toán kho.\n"
     "• Xem tất cả phiếu / Xem tất cả phiếu của công ty / Xem tất cả phiếu của phòng ban — quyết định "
     "màn danh sách có hiện thêm ô lọc Công ty và Phòng ban hay không."),

    ("8. Cách tính các ô thống kê",
     "► Ô 'Có thể giữ' = (tồn kho khả dụng của hàng hóa trừ đi phần hàng khuyến mại) chia cho hệ số "
     "đơn vị tính đang chọn, làm tròn, và không bao giờ nhỏ hơn 0.\n"
     "► Ô 'Đang giữ' = số lượng đang giữ của dòng hàng giữ chia cho hệ số đơn vị tính đang chọn.\n"
     "► Ô 'Cần gia hạn' khi mới mở màn Tạo mới = đúng bằng ô 'Đang giữ' của dòng đó.\n"
     "► Ô 'Tổng cộng' cột Đang giữ = tổng ô 'Đang giữ' của các dòng ĐANG TÍCH CHỌN.\n"
     "► Ô 'Tổng cộng' cột Cần gia hạn = tổng ô 'Cần gia hạn' của các dòng ĐANG TÍCH CHỌN.\n"
     "► Điều kiện phiếu phải qua Ban giám đốc (thay vì đi thẳng xuống Kế toán): với dòng CÓ gắn đơn "
     "hàng/hợp đồng — số tiền khách đã thanh toán cho hợp đồng đó chiếm tỉ lệ nhỏ hơn '% đặt cọc' khai "
     "cho loại hợp đồng đó trong Quy chế công ty; với dòng KHÔNG gắn hợp đồng — tổng giá trị hàng xin "
     "gia hạn vượt quá 'Giá trị giữ hàng khác' khai trong Quy chế công ty. Chỉ cần MỘT dòng thỏa là cả "
     "phiếu phải qua Ban giám đốc.\n"
     "► Ngày tối đa được phép chọn cho 'Hạn giữ mới' = ngày hôm nay cộng 'Số ngày giữ tối đa' khai "
     "trong Cấu hình hệ thống."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất của màn này — đọc trước khi test:\n"
     "① Ô 'Ghi chú' có dấu sao đỏ như trường bắt buộc NHƯNG hệ thống vẫn cho lưu khi bỏ trống. "
     "Đây là điểm cần ghi nhận khi test, không phải lỗi thao tác.\n"
     "② Ở màn TẠO/SỬA: nhập 'Hạn giữ mới' cho một dòng thì hệ thống tự điền ngày đó cho các dòng "
     "CHƯA có ngày, và KHÔNG đụng vào dòng đã có ngày.\n"
     "③ Ở màn DUYỆT: sửa 'Hạn giữ mới' của DÒNG ĐẦU TIÊN sẽ GHI ĐÈ ngày cho TOÀN BỘ các dòng, kể cả "
     "dòng đã có ngày khác. Sửa từ dòng thứ hai trở đi thì chỉ đổi dòng đó.\n"
     "④ Hộp chọn tệp đính kèm mặc định chỉ lọc tệp PDF, trong khi hệ thống nhận cả ảnh, Word, Excel — "
     "phải chuyển bộ lọc sang 'All files' mới chọn được các loại còn lại.\n"
     "⑤ Nút xóa hợp đồng (dấu X) bị vô hiệu khi đang SỬA phiếu, chỉ dùng được lúc tạo mới.\n"
     "⑥ Ô 'Cần gia hạn' mặc định điền sẵn toàn bộ số đang giữ — dễ gửi nhầm số lượng.\n"
     "⑦ Người có hàng MƯỢN quá hạn hoặc hàng NHẬP THẲNG quá hạn có thể bị chặn tạo/lưu phiếu này, tùy "
     "cấu hình chặn quá hạn của công ty. Hàng GIỮ quá hạn thì KHÔNG chặn màn này.\n"
     "⑧ Trưởng phòng có thể bị chặn duyệt nếu phòng ban mình quản lý còn nhân viên đang quá hạn.\n"
     "⑨ Bị Không duyệt ở bất kỳ cấp nào, phiếu quay về trạng thái Đang tạo để người lập sửa và gửi lại.\n"
     "⑩ Nhóm test 'gọi thẳng chức năng, bỏ qua giao diện' dành cho tester kỹ thuật, dùng công cụ kiểm "
     "thử để kiểm tra hệ thống có chặn đúng khi người dùng không có quyền."),
]

# =========================================================================
# SECTION PHAN QUYEN
# =========================================================================
ROLE_TCS = [
    ("00", "Người dùng không có quyền xem mở rộng chỉ thấy phiếu của mình", "P0",
     "Tài khoản A thuộc công ty 1, không có quyền xem theo phòng ban/công ty/tổng công ty. "
     "Trên hệ thống có: 3 phiếu do A lập, 5 phiếu do người khác cùng phòng lập",
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Vào menu Kho → Giữ hàng → Phiếu Yêu cầu gia hạn giữ hàng\n"
     "3. Đếm số dòng trên lưới",
     "Tài khoản: A (không quyền mở rộng)",
     "- Lưới chỉ hiện đúng 3 phiếu do A lập\n"
     "- Không thấy phiếu của 5 người khác\n"
     "- Không có ô lọc Công ty và ô lọc Phòng ban trên thanh tìm kiếm"),

    ("01", "Quyền 'Xem phiếu hàng giữ theo phòng ban'", "P0",
     "Tài khoản B có quyền 'Xem phiếu hàng giữ theo phòng ban', được phân quản lý phòng Kinh doanh 1. "
     "Có 4 phiếu của phòng Kinh doanh 1 (không có phiếu Đang tạo), 6 phiếu của phòng Kinh doanh 2",
     "1. Đăng nhập bằng tài khoản B\n"
     "2. Vào menu Kho → Giữ hàng → Phiếu Yêu cầu gia hạn giữ hàng\n"
     "3. Quan sát phạm vi dữ liệu",
     "Tài khoản: B (quản lý phòng Kinh doanh 1)",
     "- Hiện đúng 4 phiếu của phòng Kinh doanh 1\n"
     "- Không hiện 6 phiếu của phòng Kinh doanh 2"),

    ("02", "Quyền 'Xem phiếu hàng giữ theo công ty'", "P0",
     "Tài khoản C có quyền 'Xem phiếu hàng giữ theo công ty', thuộc công ty 1. "
     "Công ty 1 có 12 phiếu (không tính phiếu Đang tạo), công ty 4 có 9 phiếu",
     "1. Đăng nhập bằng tài khoản C\n"
     "2. Vào màn danh sách\n"
     "3. Quan sát phạm vi dữ liệu và các ô lọc",
     "Tài khoản: C (công ty 1)",
     "- Hiện đúng 12 phiếu của công ty 1\n"
     "- Không hiện phiếu công ty 4"),

    ("03", "Quyền 'Xem phiếu hàng giữ theo tổng công ty'", "P0",
     "Tài khoản D có quyền 'Xem phiếu hàng giữ theo tổng công ty'. Hệ thống có phiếu ở công ty 1 và "
     "công ty 4",
     "1. Đăng nhập bằng tài khoản D\n"
     "2. Vào màn danh sách\n"
     "3. Quan sát phạm vi dữ liệu",
     "Tài khoản: D (tổng công ty)",
     "- Hiện phiếu của cả công ty 1 và công ty 4\n"
     "- Vẫn KHÔNG thấy phiếu Đang tạo của người khác"),

    ("04", "Phiếu Đang tạo của người khác bị ẩn với mọi cấp quyền", "P0",
     "Tài khoản A lập 1 phiếu và bấm Lưu (dừng ở Đang tạo). Tài khoản D có quyền xem tổng công ty",
     "1. Đăng nhập tài khoản D\n"
     "2. Vào màn danh sách\n"
     "3. Lọc Trạng thái = Đang tạo\n"
     "4. Tìm mã phiếu vừa lập",
     "Phiếu Đang tạo của A",
     "- Lưới không có phiếu Đang tạo của A\n"
     "⚠️ Đây là quy tắc chặn riêng: phiếu Đang tạo chỉ hiện với đúng người lập"),

    ("05", "Quyền 'Trưởng phòng duyệt hàng giữ' thấy đúng phiếu chờ mình", "P0",
     "Tài khoản E có quyền 'Trưởng phòng duyệt hàng giữ', quản lý phòng Kinh doanh 1. "
     "Có 2 phiếu Chờ TP duyệt của phòng Kinh doanh 1, 3 phiếu Chờ TP duyệt của phòng Kinh doanh 2, "
     "1 phiếu Chờ KT duyệt",
     "1. Đăng nhập tài khoản E\n"
     "2. Vào menu Kế toán → Hàng giữ → Phiếu yêu cầu gia hạn hàng giữ chờ duyệt\n"
     "3. Đếm số phiếu",
     "Tài khoản: E (Trưởng phòng KD1)",
     "- Chỉ hiện 2 phiếu Chờ TP duyệt của phòng Kinh doanh 1\n"
     "- Không hiện 3 phiếu của phòng Kinh doanh 2\n"
     "- Không hiện phiếu Chờ KT duyệt"),

    ("06", "Quyền 'Ban giám đốc duyệt hàng giữ' thấy đúng phiếu chờ mình", "P0",
     "Tài khoản F có quyền 'Ban giám đốc duyệt hàng giữ', công ty 1. "
     "Có 3 phiếu Chờ BGĐ duyệt ở công ty 1, 2 phiếu Chờ BGĐ duyệt ở công ty 4",
     "1. Đăng nhập tài khoản F\n"
     "2. Vào màn Phiếu yêu cầu gia hạn hàng giữ chờ duyệt\n"
     "3. Đếm số phiếu",
     "Tài khoản: F (Ban giám đốc công ty 1)",
     "- Hiện đúng 3 phiếu Chờ BGĐ duyệt của công ty 1\n"
     "- Không hiện phiếu của công ty 4"),

    ("07", "Quyền 'Kế toán duyệt hàng giữ' thấy đúng phiếu chờ mình", "P0",
     "Tài khoản G có quyền 'Kế toán duyệt hàng giữ', công ty 1. "
     "Có 4 phiếu Chờ KT duyệt ở công ty 1, 1 phiếu Chờ TP duyệt, 1 phiếu Đã duyệt",
     "1. Đăng nhập tài khoản G\n"
     "2. Vào màn Phiếu yêu cầu gia hạn hàng giữ chờ duyệt\n"
     "3. Đếm số phiếu",
     "Tài khoản: G (Kế toán công ty 1)",
     "- Hiện đúng 4 phiếu Chờ KT duyệt\n"
     "- Không hiện phiếu Chờ TP duyệt và phiếu Đã duyệt"),

    ("08", "Người kiêm nhiều quyền duyệt thấy gộp các nhóm phiếu", "P1",
     "Tài khoản H vừa có 'Trưởng phòng duyệt hàng giữ' (quản lý phòng KD1) vừa có 'Kế toán duyệt hàng "
     "giữ'. Có 2 phiếu Chờ TP duyệt của KD1 và 3 phiếu Chờ KT duyệt",
     "1. Đăng nhập tài khoản H\n"
     "2. Vào màn Phiếu yêu cầu gia hạn hàng giữ chờ duyệt\n"
     "3. Đếm số phiếu",
     "Tài khoản: H (kiêm 2 vai trò duyệt)",
     "- Hiện đủ 5 phiếu (2 Chờ TP duyệt + 3 Chờ KT duyệt)\n"
     "⚠️ Thiếu nhóm nào là lỗi gộp điều kiện quyền"),

    ("09", "Người không có quyền duyệt nào vào màn chờ duyệt", "P1",
     "Tài khoản A không có quyền duyệt nào, đã lập 2 phiếu (1 Chờ TP duyệt, 1 Đã duyệt)",
     "1. Đăng nhập tài khoản A\n"
     "2. Mở màn Phiếu yêu cầu gia hạn hàng giữ chờ duyệt (qua liên kết trực tiếp)\n"
     "3. Quan sát lưới",
     "Tài khoản: A",
     "- Chỉ hiện phiếu do chính A lập\n"
     "- Không hiện phiếu của người khác"),

    ("10", "Trưởng phòng không quản lý phòng của phiếu thì không được duyệt", "P0",
     "Tài khoản E là Trưởng phòng quản lý phòng KD1. Phiếu P thuộc phòng KD2, đang Chờ TP duyệt",
     "1. Đăng nhập tài khoản E\n"
     "2. Mở màn xem của phiếu P bằng liên kết trực tiếp\n"
     "3. Quan sát khối nút cuối trang",
     "Phiếu P — phòng KD2 — Chờ TP duyệt",
     "- Không có nút 'TP Duyệt' và không có nút 'Không duyệt'\n"
     "- Nếu tài khoản không được xem thì hệ thống hiển thị trang báo không tìm thấy dữ liệu"),

    ("11", "Chặn duyệt khi gọi thẳng chức năng, bỏ qua giao diện", "P0",
     "Tài khoản A không có quyền duyệt nào. Phiếu P đang ở Chờ KT duyệt",
     "1. Dùng công cụ kiểm thử gọi thẳng chức năng Duyệt của phiếu P bằng tài khoản A\n"
     "2. Quan sát phản hồi\n"
     "3. Mở lại phiếu P trên giao diện",
     "Tài khoản: A · Phiếu: P",
     "- Hệ thống từ chối, báo 'Không đủ quyền!'\n"
     "- Trạng thái phiếu P vẫn là Chờ KT duyệt, không đổi"),

    ("12", "Chặn sửa và xóa khi gọi thẳng chức năng, bỏ qua giao diện", "P0",
     "Tài khoản A không phải người lập phiếu P. Phiếu P đang ở trạng thái Đang tạo, do B lập",
     "1. Dùng công cụ kiểm thử gọi thẳng chức năng Sửa phiếu P bằng tài khoản A\n"
     "2. Gọi tiếp chức năng Xóa phiếu P bằng tài khoản A\n"
     "3. Đăng nhập tài khoản B kiểm tra lại phiếu P",
     "Tài khoản: A · Phiếu: P của B",
     "- Chức năng Sửa bị từ chối với thông báo không có quyền sửa phiếu này\n"
     "- Chức năng Xóa báo 'Không thể xóa!'\n"
     "- Phiếu P vẫn còn nguyên với đầy đủ dòng hàng"),

    ("13", "Chặn xem phiếu của công ty khác", "P1",
     "Tài khoản G là Kế toán duyệt hàng giữ của công ty 1. Phiếu Q thuộc công ty 4, đang Chờ KT duyệt",
     "1. Đăng nhập tài khoản G\n"
     "2. Mở màn xem phiếu Q bằng liên kết trực tiếp",
     "Phiếu Q — công ty 4",
     "- Hệ thống hiển thị trang báo không tìm thấy dữ liệu\n"
     "- Không hiển thị nội dung phiếu Q"),
]

# =========================================================================
# SECTIONS NGHIEP VU
# =========================================================================
SECTIONS = [
    # ------------------------------------------------------------------ I
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", [
        ("001", "Vào màn danh sách từ menu Kho", "P0",
         "Tài khoản A đã đăng nhập, có ít nhất 1 phiếu",
         "1. Bấm menu Kho\n2. Bấm nhóm Giữ hàng\n3. Bấm 'Phiếu Yêu cầu gia hạn giữ hàng'",
         "Tài khoản: A",
         "- Trang mở với tiêu đề 'Danh sách yêu cầu gia hạn giữ'\n"
         "- Lưới có đủ 8 cột: STT · Mã phiếu · Người lập · Ngày lập · Trạng thái · Người duyệt · "
         "Ngày duyệt · Hành động\n"
         "- Có nút 'Tạo mới' và nút 'Xuất excel' phía trên lưới"),

        ("002", "Vào màn danh sách từ thanh tắt trên đầu trang", "P2",
         "Tài khoản A đã đăng nhập",
         "1. Mở thanh tắt ở đầu trang\n2. Bấm mục 'Gia hạn hàng giữ'",
         "Tài khoản: A",
         "- Mở đúng màn Danh sách yêu cầu gia hạn giữ\n"
         "⚠️ Lối vào này KHÔNG kèm phạm vi 'tất cả' nên chỉ hiện phiếu do chính mình lập"),

        ("003", "Vào màn danh sách chờ duyệt từ menu Kế toán", "P0",
         "Tài khoản G có quyền 'Kế toán duyệt hàng giữ', có 4 phiếu Chờ KT duyệt",
         "1. Bấm menu Kế toán\n2. Bấm nhóm Hàng giữ\n"
         "3. Bấm 'Phiếu yêu cầu gia hạn hàng giữ chờ duyệt'",
         "Tài khoản: G",
         "- Trang mở với tiêu đề 'Danh sách yêu cầu gia hạn giữ'\n"
         "- Lưới chỉ hiện phiếu đang chờ chính G duyệt"),

        ("004", "Cột Mã phiếu là liên kết mở màn xem", "P1",
         "Có ít nhất 1 phiếu trên lưới",
         "1. Vào màn danh sách\n2. Bấm vào mã phiếu ở cột Mã phiếu",
         "Phiếu: PGHHG-00012",
         "- Mở màn xem của đúng phiếu đó\n"
         "- Tiêu đề trang có dạng 'Phiếu yêu cầu gia hạn giữ: PGHHG-00012'"),

        ("005", "Định dạng mã phiếu tự sinh", "P1",
         "Tài khoản A vừa lập thành công 1 phiếu",
         "1. Vào màn danh sách\n2. Đọc mã phiếu mới nhất",
         "—",
         "- Mã phiếu bắt đầu bằng PGHHG- và theo sau là dãy số\n"
         "- Mã không trùng với bất kỳ phiếu nào đã có"),

        ("006", "Định dạng ngày trên lưới", "P1",
         "Có phiếu lập ngày 05/03/2026, duyệt ngày 09/03/2026",
         "1. Vào màn danh sách\n2. Đọc cột Ngày lập và Ngày duyệt",
         "—",
         "- Ngày lập hiển thị 05/03/2026\n"
         "- Ngày duyệt hiển thị 09/03/2026\n"
         "- Phiếu chưa duyệt thì cột Ngày duyệt và Người duyệt để trống"),

        ("007", "Nhãn màu của 5 trạng thái", "P0",
         "Trên lưới có đủ 5 phiếu ở 5 trạng thái khác nhau",
         "1. Vào màn danh sách\n2. Đọc cột Trạng thái của từng phiếu",
         "—",
         "- Đã duyệt: nhãn nền xanh lá\n"
         "- Chờ KT duyệt / Chờ BGĐ duyệt / Chờ TP duyệt: nhãn nền vàng\n"
         "- Đang tạo: nhãn nền đỏ\n"
         "- Không có phiếu nào để trống cột Trạng thái"),

        ("008", "Menu Hành động theo trạng thái phiếu — người lập", "P0",
         "Tài khoản A lập phiếu P đang ở Đang tạo và phiếu Q đang ở Chờ TP duyệt",
         "1. Đăng nhập A, vào màn danh sách\n"
         "2. Bấm nút bánh răng ở cột Hành động của phiếu P\n"
         "3. Làm tương tự với phiếu Q",
         "Phiếu P: Đang tạo · Phiếu Q: Chờ TP duyệt",
         "- Phiếu P có mục: Sửa · Xóa · In · Xuất excel\n"
         "- Phiếu Q chỉ có: In · Xuất excel (không còn Sửa, Xóa)"),

        ("009", "Menu Hành động hiện mục Duyệt cho người có lượt duyệt", "P0",
         "Tài khoản G là Kế toán duyệt hàng giữ. Phiếu R đang Chờ KT duyệt",
         "1. Đăng nhập G, vào màn chờ duyệt\n2. Bấm nút bánh răng của phiếu R",
         "Phiếu R: Chờ KT duyệt",
         "- Menu có mục 'Duyệt' dẫn tới màn xem của phiếu R\n"
         "- Có thêm mục In và Xuất excel"),

        ("010", "Khối Thông tin chung ở màn xem", "P1",
         "Phiếu R do nhân viên Nguyễn Văn A phòng Kinh doanh 1 lập ngày 05/03/2026, ghi chú "
         "'Khách xin lùi lịch nhận hàng'",
         "1. Mở màn xem phiếu R\n2. Đọc khối Thông tin chung",
         "Phiếu R",
         "- Góc phải hiện 'Nguyễn Văn A - 05/03/2026'\n"
         "- Ô 'Phòng ban yêu cầu' hiện Kinh doanh 1 và bị khóa không sửa được\n"
         "- Ô 'Ghi chú (Yêu cầu)' hiện đúng nội dung và bị khóa"),

        ("011", "Ô 'Ghi chú duyệt' chỉ hiện khi đã có nội dung", "P1",
         "Phiếu R chưa ai ghi chú duyệt; phiếu S đã bị Không duyệt kèm ghi chú 'Chưa đủ căn cứ'",
         "1. Mở màn xem phiếu R, quan sát khối Thông tin chung\n2. Mở màn xem phiếu S",
         "Phiếu R và phiếu S",
         "- Phiếu R: không hiện ô 'Ghi chú duyệt'\n"
         "- Phiếu S: hiện ô 'Ghi chú duyệt' với nội dung 'Chưa đủ căn cứ', ô bị khóa"),

        ("012", "Màn xem của người duyệt hiện thêm dòng chưa tích chọn", "P0",
         "Phiếu R có 5 dòng hàng, người lập chỉ tích 3 dòng cần gia hạn. Phiếu đang Chờ KT duyệt",
         "1. Đăng nhập tài khoản G (Kế toán duyệt), mở phiếu R\n"
         "2. Đếm số dòng trong bảng Chi tiết\n"
         "3. Đăng nhập tài khoản D (chỉ có quyền xem), mở lại phiếu R\n"
         "4. Đếm số dòng",
         "Phiếu R: 5 dòng, tích 3",
         "- Với G: hiện đủ 5 dòng, có cột ô tích ở đầu, 3 dòng đang được tích sẵn\n"
         "- Với D: chỉ hiện 3 dòng đã tích, không có cột ô tích"),

        ("013", "Cột 'Đang giữ' bị ẩn khi phiếu Đã duyệt", "P1",
         "Phiếu T đang Chờ KT duyệt; phiếu U đã ở trạng thái Đã duyệt",
         "1. Mở màn xem phiếu T, đọc tiêu đề cột trong bảng Chi tiết\n2. Mở màn xem phiếu U",
         "Phiếu T và phiếu U",
         "- Phiếu T: có cột 'Đang giữ'\n"
         "- Phiếu U: KHÔNG có cột 'Đang giữ', các cột còn lại vẫn đủ"),

        ("014", "Nút Quay lại ở màn xem", "P2",
         "Đang mở màn xem 1 phiếu bất kỳ",
         "1. Kéo xuống cuối trang\n2. Bấm nút 'Quay lại'",
         "—",
         "- Quay về màn Danh sách yêu cầu gia hạn giữ"),

        ("015", "Liên kết hợp đồng ở màn xem mở tab mới", "P2",
         "Phiếu R có dòng hàng gắn hợp đồng mã HDBH-00123",
         "1. Mở màn xem phiếu R\n2. Bấm vào mã hợp đồng ở cột Hợp đồng",
         "Hợp đồng: HDBH-00123",
         "- Mở tab mới tới màn hợp đồng tương ứng\n"
         "- Tab đang xem phiếu không bị mất"),
    ]),

    # ----------------------------------------------------------------- II
    ("II", "BỘ LỌC & TÌM KIẾM", [
        ("001", "Danh sách ô lọc trên màn danh sách", "P0",
         "Tài khoản A đã đăng nhập, không có quyền xem mở rộng",
         "1. Vào màn danh sách\n2. Đọc các ô lọc phía trên lưới",
         "Tài khoản: A",
         "- Có các ô: Từ ngày · Đến ngày · Mã phiếu · Người lập · Trạng thái · Người duyệt · "
         "Tên hàng hóa · Mã hàng hóa\n"
         "- Có nút kính lúp (Tìm kiếm) và nút mũi tên vòng (Làm mới)\n"
         "- KHÔNG có ô lọc Công ty và Phòng ban"),

        ("002", "Ô lọc Công ty và Phòng ban hiện theo quyền", "P0",
         "Tài khoản D có quyền 'Xem tất cả phiếu'; tài khoản C có quyền 'Xem tất cả phiếu của công ty'",
         "1. Đăng nhập D, vào màn danh sách, đọc các ô lọc\n2. Đăng nhập C, làm lại",
         "Tài khoản D và C",
         "- Với D: có cả ô lọc Công ty và ô lọc Phòng ban\n"
         "- Với C: chỉ có ô lọc Phòng ban, không có ô lọc Công ty"),

        ("003", "Chọn Công ty thì danh sách Phòng ban lọc theo công ty đó", "P1",
         "Tài khoản D có quyền xem tất cả phiếu. Công ty 1 có 5 phòng ban, công ty 4 có 3 phòng ban",
         "1. Đăng nhập D, vào màn danh sách\n2. Chọn ô Công ty = Công ty 4\n3. Mở ô Phòng ban",
         "Công ty: Công ty 4",
         "- Ô Phòng ban chỉ liệt kê 3 phòng ban của công ty 4\n"
         "- Không còn phòng ban của công ty 1 trong danh sách"),

        ("004", "Lọc theo Mã phiếu — khớp một phần", "P0",
         "Có 3 phiếu mã PGHHG-00011, PGHHG-00012, PGHHG-00120",
         "1. Nhập '0012' vào ô Mã phiếu\n2. Bấm nút kính lúp\n3. Chờ lưới nạp xong",
         "Mã phiếu: 0012",
         "- Lưới hiện PGHHG-00012 và PGHHG-00120\n"
         "- Không hiện PGHHG-00011"),

        ("005", "Lọc theo Trạng thái", "P0",
         "Có 3 phiếu Đã duyệt, 2 phiếu Chờ KT duyệt, 1 phiếu Chờ TP duyệt",
         "1. Chọn ô Trạng thái = 'Chờ KT duyệt'\n2. Bấm nút kính lúp\n3. Chờ lưới nạp xong",
         "Trạng thái: Chờ KT duyệt",
         "- Lưới hiện đúng 2 phiếu\n"
         "- Cột Trạng thái của cả 2 dòng đều là 'Chờ KT duyệt'"),

        ("006", "Danh sách giá trị của ô lọc Trạng thái", "P1",
         "Đang ở màn danh sách",
         "1. Bấm mở ô Trạng thái\n2. Đọc các giá trị",
         "—",
         "- Có đúng 5 giá trị: Đã duyệt · Chờ KT duyệt · Đang tạo · Chờ BGĐ duyệt · Chờ TP duyệt"),

        ("007", "Lọc theo Người lập", "P0",
         "Nhân viên Nguyễn Văn A lập 3 phiếu, nhân viên Trần Thị B lập 4 phiếu",
         "1. Gõ 'Nguyễn Văn A' vào ô Người lập, chọn từ danh sách gợi ý\n"
         "2. Bấm nút kính lúp\n3. Chờ lưới nạp xong",
         "Người lập: Nguyễn Văn A",
         "- Lưới hiện đúng 3 phiếu\n- Cột Người lập của mọi dòng đều là Nguyễn Văn A"),

        ("008", "Lọc theo Người duyệt", "P1",
         "Kế toán Lê Văn C đã duyệt 2 phiếu; các phiếu còn lại do người khác duyệt hoặc chưa duyệt",
         "1. Gõ 'Lê Văn C' vào ô Người duyệt, chọn từ gợi ý\n2. Bấm nút kính lúp",
         "Người duyệt: Lê Văn C",
         "- Lưới hiện đúng 2 phiếu\n"
         "- Không hiện phiếu chưa có người duyệt"),

        ("009", "Lọc theo Tên hàng hóa", "P0",
         "Phiếu P có dòng hàng 'Máy nén khí Puma 5HP' (đã tích cần gia hạn); phiếu Q không có hàng nào "
         "tên chứa 'Puma'",
         "1. Nhập 'Puma' vào ô Tên hàng hóa\n2. Bấm nút kính lúp\n3. Chờ lưới nạp xong",
         "Tên hàng hóa: Puma",
         "- Lưới hiện phiếu P\n- Không hiện phiếu Q\n"
         "⚠️ Chỉ tính dòng hàng ĐÃ TÍCH cần gia hạn; dòng bỏ tích không làm phiếu lọt vào kết quả"),

        ("010", "Lọc theo Mã hàng hóa", "P0",
         "Phiếu P có dòng hàng mã 'MNK-PUMA-5HP' đã tích cần gia hạn",
         "1. Nhập 'PUMA-5' vào ô Mã hàng hóa\n2. Bấm nút kính lúp",
         "Mã hàng hóa: PUMA-5",
         "- Lưới hiện phiếu P\n- Các phiếu không chứa mã hàng này bị loại"),

        ("011", "Lọc theo khoảng Ngày lập", "P0",
         "Có phiếu lập ngày 28/02/2026, 05/03/2026, 12/03/2026",
         "1. Nhập Từ ngày = 01/03/2026\n2. Nhập Đến ngày = 10/03/2026\n3. Bấm nút kính lúp",
         "Từ 01/03/2026 đến 10/03/2026",
         "- Lưới chỉ hiện phiếu lập ngày 05/03/2026\n"
         "- Không hiện phiếu 28/02/2026 và 12/03/2026"),

        ("012", "Ô 'Đến ngày' lấy trọn cả ngày được chọn", "P0",
         "Có phiếu lập lúc 17h30 ngày 10/03/2026",
         "1. Nhập Từ ngày = 10/03/2026 và Đến ngày = 10/03/2026\n2. Bấm nút kính lúp",
         "Từ 10/03/2026 đến 10/03/2026",
         "- Phiếu lập lúc 17h30 ngày 10/03/2026 VẪN hiện trên lưới\n"
         "⚠️ Đây là bẫy hay sai: nếu phiếu buổi chiều bị mất thì khoảng ngày đang cắt sai"),

        ("013", "Chỉ nhập Từ ngày, bỏ trống Đến ngày", "P1",
         "Có phiếu lập ngày 28/02/2026, 05/03/2026, 12/03/2026",
         "1. Nhập Từ ngày = 05/03/2026, để trống Đến ngày\n2. Bấm nút kính lúp",
         "Từ 05/03/2026",
         "- Lưới hiện phiếu 05/03/2026 và 12/03/2026\n- Không hiện phiếu 28/02/2026"),

        ("014", "Kết hợp nhiều ô lọc cùng lúc", "P0",
         "Nguyễn Văn A có 3 phiếu: 1 Đã duyệt lập 05/03/2026, 1 Chờ KT duyệt lập 06/03/2026, "
         "1 Đã duyệt lập 20/03/2026",
         "1. Chọn Người lập = Nguyễn Văn A\n2. Chọn Trạng thái = Đã duyệt\n"
         "3. Nhập Từ ngày = 01/03/2026, Đến ngày = 10/03/2026\n4. Bấm nút kính lúp",
         "Nguyễn Văn A + Đã duyệt + 01/03–10/03/2026",
         "- Lưới hiện đúng 1 phiếu (Đã duyệt, lập 05/03/2026)\n"
         "- Các điều kiện lọc phải cùng thỏa, không phải chỉ một trong số đó"),

        ("015", "Nút Làm mới xóa hết điều kiện và nạp lại", "P0",
         "Đang lọc Trạng thái = Đã duyệt và Mã phiếu = 0012, lưới còn 1 dòng",
         "1. Bấm nút mũi tên vòng (Làm mới)\n2. Chờ lưới nạp xong\n3. Quan sát các ô lọc và số dòng",
         "—",
         "- Toàn bộ ô lọc trở về rỗng\n"
         "- Lưới nạp lại đầy đủ danh sách như lúc mới vào màn\n"
         "⚠️ Ô lọc trở về rỗng mà lưới vẫn giữ kết quả cũ là LỖI"),

        ("016", "Bộ lọc được nhớ khi quay lại màn", "P1",
         "Đang lọc Trạng thái = Đã duyệt trên màn danh sách",
         "1. Bấm mở một phiếu\n2. Bấm nút Quay lại\n3. Quan sát ô lọc Trạng thái và lưới",
         "Trạng thái: Đã duyệt",
         "- Ô Trạng thái vẫn đang là Đã duyệt\n- Lưới vẫn đang hiển thị kết quả đã lọc"),

        ("017", "Lọc không có kết quả", "P1",
         "Không có phiếu nào mang mã chứa 'ZZZZ'",
         "1. Nhập 'ZZZZ' vào ô Mã phiếu\n2. Bấm nút kính lúp",
         "Mã phiếu: ZZZZ",
         "- Lưới hiện dòng thông báo không có dữ liệu\n"
         "- Trang không báo lỗi, các ô lọc vẫn dùng được"),

        ("018", "Màn chờ duyệt giữ nguyên phạm vi khi lọc", "P0",
         "Tài khoản G là Kế toán duyệt, đang ở màn chờ duyệt với 4 phiếu Chờ KT duyệt. Ngoài ra công ty "
         "còn 3 phiếu Chờ TP duyệt",
         "1. Chọn ô Trạng thái = Chờ TP duyệt\n2. Bấm nút kính lúp",
         "Trạng thái: Chờ TP duyệt",
         "- Lưới trống (G không có lượt duyệt với phiếu Chờ TP duyệt)\n"
         "⚠️ Nếu 3 phiếu Chờ TP duyệt hiện ra thì phạm vi quyền của màn chờ duyệt đang bị bộ lọc phá vỡ"),
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
         "1. Bấm lần lượt tiêu đề các cột STT, Người lập, Người duyệt, Hành động",
         "—",
         "- Bốn cột này không có biểu tượng sắp xếp và bấm vào không đổi thứ tự lưới"),

        ("004", "Đổi số dòng mỗi trang", "P1",
         "Có 30 phiếu thỏa bộ lọc hiện tại",
         "1. Vào màn danh sách\n2. Đổi ô số dòng mỗi trang sang 25\n3. Đếm số dòng hiển thị",
         "Số dòng/trang: 25",
         "- Lưới hiện đúng 25 dòng\n- Dòng thông tin bên dưới báo đang hiện 1 đến 25 trong tổng 30"),

        ("005", "Chuyển trang giữ nguyên bộ lọc", "P0",
         "Đang lọc Trạng thái = Đã duyệt, kết quả có 30 phiếu, đang xem 10 dòng mỗi trang",
         "1. Bấm sang trang 2\n2. Đọc cột Trạng thái của các dòng\n3. Kiểm tra ô lọc Trạng thái",
         "Trạng thái: Đã duyệt",
         "- Mọi dòng ở trang 2 đều là Đã duyệt\n- Ô lọc vẫn giữ giá trị Đã duyệt"),

        ("006", "Số thứ tự chạy liên tục qua các trang", "P1",
         "Có 30 phiếu, đang xem 10 dòng mỗi trang",
         "1. Đọc cột STT ở trang 1\n2. Bấm sang trang 2 và đọc lại cột STT",
         "—",
         "- Trang 1 đánh số 1 đến 10\n- Trang 2 đánh số 11 đến 20, không quay lại từ 1"),

        ("007", "Sắp xếp giữ nguyên khi chuyển trang", "P1",
         "Đang sắp xếp theo Ngày lập tăng dần, kết quả có 30 phiếu",
         "1. Bấm sang trang 2\n2. So ngày lập của dòng đầu trang 2 với dòng cuối trang 1",
         "—",
         "- Ngày lập của dòng đầu trang 2 lớn hơn hoặc bằng dòng cuối trang 1\n"
         "- Không có phiếu nào bị lặp lại giữa 2 trang"),
    ]),

    # ----------------------------------------------------------------- IV
    ("IV", "CHỨC NĂNG CHÍNH (TẠO / SỬA / XEM)", [
        ("001", "Mở màn Tạo mới", "P0",
         "Tài khoản A đang giữ 4 mặt hàng có hạn giữ trong vùng cảnh báo",
         "1. Vào màn danh sách\n2. Bấm nút 'Tạo mới'\n3. Chờ bảng Chi tiết nạp xong",
         "Tài khoản: A",
         "- Trang mở với tiêu đề 'Tạo phiếu gia hạn hàng giữ'\n"
         "- Khối Thông tin chung có ô Ghi chú và khu vực File đính kèm\n"
         "- Bảng Chi tiết hiện đúng 4 dòng hàng\n"
         "- Cuối trang có 3 nút: Lưu · Lưu & Gửi · Hủy"),

        ("002", "Các cột của bảng Chi tiết khi tạo mới", "P0",
         "Màn Tạo mới đã nạp xong ít nhất 1 dòng hàng",
         "1. Đọc tiêu đề các cột trong bảng Chi tiết",
         "—",
         "- Đủ các cột: STT · ô tích chọn · Tên hàng hóa · Khách hàng · Hợp đồng · Đơn vị tính · "
         "Có thể giữ · Đang giữ · Cần gia hạn · Ngày bắt đầu giữ · Hạn giữ hiện tại · "
         "Hạn giữ mới (*) · Lịch sử\n"
         "- Hai cột 'Đang giữ' và 'Cần gia hạn' nằm chung nhóm tiêu đề 'Số lượng'"),

        ("003", "Bảng Chi tiết chỉ nạp hàng giữ trong vùng cảnh báo", "P0",
         "Cấu hình 'Số ngày cảnh báo (mượn/giữ hàng)' = 7. Hôm nay 05/03/2026. Tài khoản A đang giữ: "
         "hàng X hạn 03/03/2026, hàng Y hạn 10/03/2026, hàng Z hạn 25/03/2026",
         "1. Đăng nhập A\n2. Bấm Tạo mới\n3. Đọc danh sách hàng trong bảng Chi tiết",
         "Hôm nay = 05/03/2026 · Số ngày cảnh báo = 7",
         "- Hiện hàng X (đã quá hạn) và hàng Y (hạn 10/03/2026)\n"
         "- KHÔNG hiện hàng Z vì hạn 25/03/2026 vượt quá vùng cảnh báo"),

        ("004", "Bảng Chi tiết không nạp hàng giữ của người khác", "P0",
         "Tài khoản A đang giữ 4 mặt hàng; tài khoản B đang giữ 6 mặt hàng đều trong vùng cảnh báo",
         "1. Đăng nhập A\n2. Bấm Tạo mới\n3. Đếm số dòng",
         "Tài khoản: A",
         "- Bảng Chi tiết chỉ có 4 dòng của A\n- Không có mặt hàng nào của B"),

        ("005", "Hàng giữ đã hết số lượng không được nạp", "P1",
         "Tài khoản A có 1 dòng hàng giữ đã bị hủy hết, số lượng còn 0, hạn giữ 06/03/2026",
         "1. Đăng nhập A\n2. Bấm Tạo mới\n3. Tìm mặt hàng đó trong bảng",
         "Hàng có số lượng giữ = 0",
         "- Mặt hàng có số lượng 0 không xuất hiện trong bảng Chi tiết"),

        ("006", "Không có hàng nào thỏa điều kiện", "P1",
         "Tài khoản E không giữ mặt hàng nào trong vùng cảnh báo",
         "1. Đăng nhập E\n2. Bấm Tạo mới\n3. Quan sát bảng Chi tiết",
         "Tài khoản: E",
         "- Bảng hiện đúng một dòng chữ 'Không có hàng hóa'\n"
         "- Trang không báo lỗi"),

        ("007", "Ô 'Cần gia hạn' điền sẵn bằng ô 'Đang giữ'", "P0",
         "Tài khoản A đang giữ hàng X số lượng 12 (đơn vị Cái, hệ số 1)",
         "1. Bấm Tạo mới\n2. Đọc ô 'Đang giữ' và ô 'Cần gia hạn' của dòng hàng X",
         "Hàng X: đang giữ 12 Cái",
         "- Ô 'Đang giữ' hiện 12\n- Ô 'Cần gia hạn' điền sẵn 12\n"
         "⚠️ Đây là bẫy: nếu chỉ muốn gia hạn một phần thì phải tự sửa lại"),

        ("008", "Ô nhập bị khóa khi dòng chưa được tích chọn", "P0",
         "Màn Tạo mới có ít nhất 1 dòng hàng, chưa tích dòng nào",
         "1. Không tích ô chọn của dòng 1\n2. Bấm vào ô 'Cần gia hạn' và ô 'Hạn giữ mới' của dòng 1",
         "—",
         "- Cả hai ô đều không nhập được\n- Dòng hiển thị mờ đi so với dòng đã tích"),

        ("009", "Tích chọn mở khóa ô nhập của dòng", "P0",
         "Màn Tạo mới có ít nhất 1 dòng hàng",
         "1. Tích ô chọn của dòng 1\n2. Bấm vào ô 'Cần gia hạn' và ô 'Hạn giữ mới'",
         "—",
         "- Hai ô nhập được bình thường\n- Dòng hết mờ"),

        ("010", "Ô tích tất cả ở tiêu đề bảng", "P0",
         "Màn Tạo mới có 4 dòng hàng, chưa tích dòng nào",
         "1. Tích ô chọn ở tiêu đề cột\n2. Đếm số dòng được tích\n3. Bỏ tích ô ở tiêu đề",
         "4 dòng hàng",
         "- Bước 2: cả 4 dòng đều được tích\n- Bước 3: cả 4 dòng đều bỏ tích"),

        ("011", "Ô tích tất cả tự bỏ khi có dòng lẻ bị bỏ tích", "P1",
         "Đang tích cả 4 dòng, ô tích ở tiêu đề đang bật",
         "1. Bỏ tích dòng 3\n2. Quan sát ô tích ở tiêu đề",
         "—",
         "- Ô tích ở tiêu đề tự động tắt\n- Ba dòng còn lại vẫn giữ tích"),

        ("012", "Dòng Tổng cộng chỉ cộng dòng được tích", "P0",
         "Có 3 dòng: X đang giữ 12 · Y đang giữ 8 · Z đang giữ 5. Cần gia hạn để nguyên mặc định",
         "1. Tích cả 3 dòng, đọc dòng Tổng cộng\n2. Bỏ tích dòng Z, đọc lại dòng Tổng cộng",
         "X=12 · Y=8 · Z=5",
         "- Bước 1: Tổng cộng cột Đang giữ = 25, cột Cần gia hạn = 25\n"
         "- Bước 2: Tổng cộng cột Đang giữ = 20, cột Cần gia hạn = 20"),

        ("013", "Sửa ô 'Cần gia hạn' làm đổi dòng Tổng cộng ngay", "P0",
         "Đang tích 2 dòng: X cần gia hạn 12, Y cần gia hạn 8. Tổng cộng đang là 20",
         "1. Sửa ô 'Cần gia hạn' của dòng X thành 5\n2. Đọc lại dòng Tổng cộng",
         "X: 12 → 5",
         "- Tổng cộng cột Cần gia hạn đổi thành 13 ngay, không cần bấm nút nào"),

        ("014", "Nhập 'Hạn giữ mới' cho một dòng tự điền sang dòng chưa có ngày", "P0",
         "Màn Tạo mới có 3 dòng, tích cả 3, chưa dòng nào có Hạn giữ mới",
         "1. Nhập Hạn giữ mới của dòng 1 = 30/03/2026\n2. Đọc ô Hạn giữ mới của dòng 2 và dòng 3",
         "Hạn giữ mới dòng 1 = 30/03/2026",
         "- Dòng 2 và dòng 3 tự điền 30/03/2026\n"
         "⚠️ Người nhập rất dễ bỏ qua bước kiểm lại các dòng còn lại"),

        ("015", "Dòng đã có ngày thì không bị ghi đè khi tạo", "P0",
         "Màn Tạo mới có 3 dòng, tích cả 3. Dòng 2 đã được nhập Hạn giữ mới = 25/03/2026",
         "1. Nhập Hạn giữ mới của dòng 1 = 30/03/2026\n"
         "2. Đọc ô Hạn giữ mới của dòng 2 và dòng 3",
         "Dòng 2 đã có 25/03/2026",
         "- Dòng 2 GIỮ NGUYÊN 25/03/2026\n- Dòng 3 được điền 30/03/2026"),

        ("016", "Đổi Đơn vị tính làm đổi số lượng quy đổi", "P0",
         "Hàng X đang giữ 24 Cái; hàng X có đơn vị Thùng với hệ số 12 (1 Thùng = 12 Cái)",
         "1. Bấm Tạo mới\n2. Ở dòng hàng X đổi Đơn vị tính từ Cái sang Thùng\n"
         "3. Đọc lại ô 'Đang giữ' và 'Có thể giữ'",
         "1 Thùng = 12 Cái",
         "- Ô 'Đang giữ' đổi từ 24 thành 2\n- Ô 'Có thể giữ' cũng được chia theo hệ số\n"
         "- Danh sách đơn vị hiện kèm hệ số dạng 'Thùng (x12)' khi hệ số khác 1"),

        ("017", "Chọn Hợp đồng cho dòng hàng", "P0",
         "Hàng X thuộc khách hàng KH001 và có ít nhất 1 hợp đồng phù hợp",
         "1. Ở dòng hàng X bấm nút kính lúp ở cột Hợp đồng\n"
         "2. Chọn một dòng trong cửa sổ 'Đơn hàng/Hợp đồng'\n3. Quan sát ô Hợp đồng của dòng",
         "Hợp đồng: HDBH-00123",
         "- Cửa sổ hiện các cột STT · Số đơn hàng/Hợp đồng · Ngày lập, có ô tìm theo số hợp đồng\n"
         "- Sau khi chọn, ô Hợp đồng hiện HDBH-00123 và có thông báo 'Thêm thành công'"),

        ("018", "Xóa hợp đồng đã chọn khi đang tạo mới", "P1",
         "Dòng hàng X đã chọn hợp đồng HDBH-00123, đang ở màn Tạo mới",
         "1. Bấm nút dấu X ở cột Hợp đồng của dòng X\n2. Quan sát ô Hợp đồng",
         "—",
         "- Ô Hợp đồng trở về rỗng, hiện lại chữ mờ 'Chọn hợp đồng'"),

        ("019", "Nút xóa hợp đồng bị vô hiệu ở màn Sửa", "P1",
         "Phiếu P đang ở Đang tạo, có dòng hàng gắn hợp đồng HDBH-00123",
         "1. Mở màn Sửa phiếu P\n2. Bấm nút dấu X ở cột Hợp đồng",
         "Phiếu P — màn Sửa",
         "- Nút dấu X không bấm được\n- Ô Hợp đồng vẫn giữ HDBH-00123\n"
         "⚠️ Đây là điểm khác biệt giữa màn Tạo mới và màn Sửa, cần ghi nhận"),

        ("020", "Ô Hợp đồng không gõ tay được", "P2",
         "Đang ở màn Tạo mới, có ít nhất 1 dòng hàng",
         "1. Bấm vào ô nhập ở cột Hợp đồng và gõ ký tự bất kỳ",
         "—",
         "- Ô không nhận ký tự nào, chỉ chọn được qua cửa sổ tìm kiếm"),

        ("021", "Xem Lịch sử giữ hàng của một dòng", "P1",
         "Hàng X của khách hàng KH001 đã có ít nhất 2 lần biến động số lượng giữ",
         "1. Ở dòng hàng X bấm nút biểu tượng đồng hồ ở cột Lịch sử\n2. Quan sát cửa sổ mở ra",
         "Hàng X — khách hàng KH001",
         "- Cửa sổ 'Lịch sử giữ hàng' mở ra với các lần biến động của đúng hàng X, đúng khách hàng "
         "và đúng người giữ\n- Đóng cửa sổ thì dữ liệu đang nhập trên phiếu không bị mất"),

        ("022", "Thêm và bỏ ô chọn tệp đính kèm", "P1",
         "Đang ở màn Tạo mới",
         "1. Bấm nút dấu cộng ở khu vực File đính kèm 2 lần\n"
         "2. Bấm dấu X trên ô đính kèm thứ hai",
         "—",
         "- Bước 1: có 2 ô chọn tệp, cùng hiện chữ 'Chọn file'\n- Bước 2: chỉ còn 1 ô"),

        ("023", "Chọn tệp đính kèm và hiển thị tên tệp", "P1",
         "Đang ở màn Tạo mới, đã thêm 1 ô đính kèm",
         "1. Bấm vào ô đính kèm\n2. Chọn tệp 'bien-ban.pdf'\n3. Quan sát ô đính kèm",
         "Tệp: bien-ban.pdf",
         "- Ô hiện tên 'bien-ban.pdf' và biểu tượng đổi thành biểu tượng tài liệu"),

        ("024", "Hộp chọn tệp mặc định chỉ lọc tệp PDF", "P1",
         "Đang ở màn Tạo mới, đã thêm 1 ô đính kèm. Trên máy có sẵn tệp 'bao-gia.xlsx'",
         "1. Bấm vào ô đính kèm\n2. Quan sát bộ lọc loại tệp trong hộp thoại của máy\n"
         "3. Chuyển bộ lọc sang 'All files' và chọn 'bao-gia.xlsx'",
         "Tệp: bao-gia.xlsx",
         "- Bộ lọc mặc định chỉ hiện tệp PDF, không thấy tệp Excel\n"
         "- Sau khi chuyển sang 'All files' thì chọn được và hệ thống nhận tệp Excel\n"
         "⚠️ Bẫy: hệ thống nhận PDF, ảnh, Word, Excel nhưng hộp chọn chỉ gợi ý PDF"),

        ("025", "Lưu phiếu ở trạng thái Đang tạo", "P0",
         "Đang ở màn Tạo mới, đã tích 2 dòng, điền đủ Cần gia hạn và Hạn giữ mới hợp lệ",
         "1. Bấm nút 'Lưu'\n2. Đọc thông báo\n3. Quan sát trang được chuyển tới",
         "Hạn giữ mới: 30/03/2026",
         "- Thông báo: 'Yêu cầu của bạn đã được lưu. Bạn cần gửi để yêu cầu được xử lý'\n"
         "- Hệ thống quay về màn danh sách\n"
         "- Phiếu mới nằm đầu lưới với trạng thái 'Đang tạo'"),

        ("026", "Lưu và gửi phiếu đi duyệt", "P0",
         "Đang ở màn Tạo mới, đã tích 2 dòng, điền đủ và hợp lệ",
         "1. Bấm nút 'Lưu & Gửi'\n2. Đọc thông báo\n3. Quan sát trạng thái phiếu trên lưới",
         "Hạn giữ mới: 30/03/2026",
         "- Thông báo: 'Yêu cầu của bạn đã được gửi'\n"
         "- Hệ thống quay về màn danh sách\n"
         "- Phiếu mới có trạng thái 'Chờ TP duyệt'"),

        ("027", "Trưởng phòng nhận thông báo khi phiếu được gửi", "P0",
         "Tài khoản E là Trưởng phòng duyệt hàng giữ, quản lý phòng của người lập A. E đang đăng nhập "
         "ở máy khác",
         "1. Tài khoản A bấm 'Lưu & Gửi'\n2. Ở máy của E mở chuông thông báo",
         "Phiếu vừa gửi: PGHHG-00050",
         "- E nhận thông báo 'Bạn có 1 phiếu yêu cầu gia hạn hàng giữ cần duyệt: PGHHG-00050'\n"
         "- Bấm vào thông báo mở đúng màn xem của phiếu đó"),

        ("028", "Nút Hủy ở màn Tạo mới", "P1",
         "Đang ở màn Tạo mới, đã tích và nhập vài dòng",
         "1. Bấm nút 'Hủy'\n2. Quan sát trang\n3. Kiểm tra lưới danh sách",
         "—",
         "- Quay về màn danh sách\n- Không có phiếu mới nào được tạo"),

        ("029", "Mở màn Sửa phiếu Đang tạo", "P0",
         "Tài khoản A lập phiếu P (Đang tạo) có 2 dòng đã tích, ghi chú 'Khách xin lùi lịch'",
         "1. Đăng nhập A, vào màn danh sách\n2. Bấm bánh răng của phiếu P, chọn 'Sửa'\n"
         "3. Quan sát dữ liệu nạp lên",
         "Phiếu P",
         "- Trang mở với tiêu đề 'Sửa phiếu gia hạn hàng giữ'\n"
         "- Ô Ghi chú hiện 'Khách xin lùi lịch'\n"
         "- Bảng Chi tiết hiện 2 dòng đã tích, đúng số lượng và đúng Hạn giữ mới đã lưu"),

        ("030", "Sửa và lưu lại phiếu Đang tạo", "P0",
         "Phiếu P Đang tạo, dòng hàng X có Cần gia hạn = 12",
         "1. Mở màn Sửa phiếu P\n2. Sửa Cần gia hạn của hàng X thành 5\n3. Bấm 'Lưu'\n"
         "4. Mở lại màn Sửa phiếu P",
         "Cần gia hạn: 12 → 5",
         "- Thông báo lưu thành công và quay về màn danh sách\n"
         "- Mở lại thấy Cần gia hạn của hàng X là 5"),

        ("031", "Sửa rồi gửi đi duyệt", "P0",
         "Phiếu P đang ở trạng thái Đang tạo",
         "1. Mở màn Sửa phiếu P\n2. Bấm 'Lưu & Gửi'\n3. Kiểm tra trạng thái trên lưới",
         "Phiếu P",
         "- Thông báo 'Yêu cầu của bạn đã được gửi'\n- Phiếu P chuyển sang 'Chờ TP duyệt'"),

        ("032", "Xóa tệp đính kèm ở màn Sửa", "P1",
         "Phiếu P Đang tạo, đã đính kèm tệp 'bien-ban.pdf'",
         "1. Mở màn Sửa phiếu P\n2. Bấm dấu X trên tệp 'bien-ban.pdf'\n3. Xác nhận trong hộp thoại\n"
         "4. Tải lại trang",
         "Tệp: bien-ban.pdf",
         "- Hộp thoại hỏi 'Bạn chắc chắn muốn xóa file này?'\n"
         "- Sau khi xác nhận, tệp biến mất và có thông báo xóa thành công\n"
         "- Tải lại trang tệp vẫn không còn"),

        ("033", "Không mở được màn Sửa khi phiếu đã gửi", "P0",
         "Phiếu Q đang ở 'Chờ TP duyệt', do tài khoản A lập",
         "1. Đăng nhập A\n2. Mở màn Sửa phiếu Q bằng liên kết trực tiếp",
         "Phiếu Q — Chờ TP duyệt",
         "- Hệ thống hiển thị trang báo không tìm thấy dữ liệu\n- Không mở được biểu mẫu sửa"),
    ]),

    # ------------------------------------------------------------------ V
    ("V", "CÁC THAO TÁC TRẠNG THÁI (DUYỆT / KHÔNG DUYỆT)", [
        ("001", "Trưởng phòng duyệt, phiếu xuống thẳng Kế toán", "P0",
         "Phiếu P Chờ TP duyệt, chỉ có 1 dòng hàng không gắn hợp đồng, tổng giá trị 5.000.000 đ. "
         "Quy chế công ty đang khai 'Giá trị giữ hàng khác' = 50.000.000 đ. Tài khoản E là Trưởng phòng "
         "quản lý phòng của phiếu",
         "1. Đăng nhập E, mở màn xem phiếu P\n2. Bấm nút 'TP Duyệt'\n3. Đọc thông báo\n"
         "4. Kiểm tra trạng thái phiếu P",
         "Giá trị hàng 5.000.000 đ < ngưỡng 50.000.000 đ",
         "- Thông báo 'Yêu cầu đã được chuyển đến Kế toán'\n"
         "- Phiếu P chuyển sang 'Chờ KT duyệt'\n"
         "- Hệ thống quay về màn danh sách chờ duyệt"),

        ("002", "Trưởng phòng duyệt, phiếu phải qua Ban giám đốc do vượt ngưỡng", "P0",
         "Phiếu P Chờ TP duyệt, 1 dòng hàng KHÔNG gắn hợp đồng, tổng giá trị 80.000.000 đ. "
         "Quy chế công ty khai 'Giá trị giữ hàng khác' = 50.000.000 đ",
         "1. Đăng nhập E, mở phiếu P\n2. Bấm 'TP Duyệt'\n3. Đọc thông báo\n4. Kiểm tra trạng thái",
         "Giá trị hàng 80.000.000 đ > ngưỡng 50.000.000 đ",
         "- Thông báo 'Yêu cầu đã được chuyển đến BGĐ'\n"
         "- Phiếu P chuyển sang 'Chờ BGĐ duyệt'\n"
         "- Người có quyền Ban giám đốc duyệt hàng giữ nhận được thông báo"),

        ("003", "Phiếu gắn hợp đồng chưa đủ tỉ lệ đặt cọc phải qua Ban giám đốc", "P0",
         "Phiếu P Chờ TP duyệt, dòng hàng gắn hợp đồng bán hàng HDBH-00123 tổng giá trị 100.000.000 đ, "
         "khách mới thanh toán 10.000.000 đ. Quy chế công ty khai % đặt cọc cho loại Hợp đồng bán hàng "
         "= 30",
         "1. Đăng nhập E, mở phiếu P\n2. Bấm 'TP Duyệt'\n3. Kiểm tra trạng thái",
         "Đã thu 10% < mức 30% yêu cầu",
         "- Phiếu chuyển sang 'Chờ BGĐ duyệt'\n"
         "- Thông báo 'Yêu cầu đã được chuyển đến BGĐ'"),

        ("004", "Phiếu gắn hợp đồng đã đủ tỉ lệ đặt cọc đi thẳng Kế toán", "P0",
         "Giống trên nhưng khách đã thanh toán 40.000.000 đ trên hợp đồng 100.000.000 đ, mức yêu cầu 30",
         "1. Đăng nhập E, mở phiếu P\n2. Bấm 'TP Duyệt'\n3. Kiểm tra trạng thái",
         "Đã thu 40% > mức 30% yêu cầu",
         "- Phiếu chuyển sang 'Chờ KT duyệt'\n"
         "- Thông báo 'Yêu cầu đã được chuyển đến Kế toán'"),

        ("005", "Một dòng vượt ngưỡng là cả phiếu phải qua Ban giám đốc", "P0",
         "Phiếu P có 3 dòng: 2 dòng thỏa điều kiện đi thẳng, 1 dòng có hợp đồng chưa đủ tỉ lệ đặt cọc",
         "1. Đăng nhập E, mở phiếu P\n2. Bấm 'TP Duyệt'\n3. Kiểm tra trạng thái",
         "3 dòng — 1 dòng vượt ngưỡng",
         "- Phiếu chuyển sang 'Chờ BGĐ duyệt'\n"
         "⚠️ Quy tắc là 'chỉ cần một dòng vượt ngưỡng', không phải 'tất cả các dòng'"),

        ("006", "Ban giám đốc duyệt", "P0",
         "Phiếu P đang 'Chờ BGĐ duyệt'. Tài khoản F có quyền Ban giám đốc duyệt hàng giữ, cùng công ty",
         "1. Đăng nhập F, mở phiếu P\n2. Bấm nút 'BGĐ Duyệt'\n3. Đọc thông báo và kiểm tra trạng thái",
         "Phiếu P — Chờ BGĐ duyệt",
         "- Thông báo 'Yêu cầu đã được chuyển đến Kế toán'\n"
         "- Phiếu P chuyển sang 'Chờ KT duyệt'\n"
         "- Người có quyền Kế toán duyệt hàng giữ nhận thông báo"),

        ("007", "Kế toán duyệt — bước cuối", "P0",
         "Phiếu P đang 'Chờ KT duyệt', có 1 dòng hàng X: đang giữ 12, cần gia hạn 12, hạn hiện tại "
         "10/03/2026, hạn mới 30/03/2026. Tài khoản G có quyền Kế toán duyệt hàng giữ",
         "1. Đăng nhập G, mở phiếu P\n2. Bấm nút 'KT Duyệt'\n3. Đọc thông báo\n"
         "4. Kiểm tra trạng thái phiếu",
         "Hàng X: 12 · 10/03/2026 → 30/03/2026",
         "- Thông báo 'Thao tác thành công!'\n"
         "- Phiếu P chuyển sang 'Đã duyệt', cột Người duyệt và Ngày duyệt được điền\n"
         "- Người lập nhận thông báo '… vừa duyệt yêu cầu gia hạn hàng giữ: PGHHG-…'"),

        ("008", "Hạn giữ thực sự được dời sau khi Kế toán duyệt", "P0",
         "Tiếp theo trường hợp trên. Trước khi duyệt, danh sách hàng giữ của người lập có dòng hàng X "
         "khách KH001 hạn 10/03/2026 số lượng 12",
         "1. Sau khi G bấm 'KT Duyệt'\n"
         "2. Vào menu Kho → Giữ hàng → Danh sách hàng giữ\n3. Tìm hàng X của khách KH001",
         "Hàng X · KH001 · 12",
         "- Dòng hạn 10/03/2026 giảm 12, còn 0\n"
         "- Xuất hiện dòng hàng X khách KH001 hạn 30/03/2026 số lượng 12"),

        ("009", "Gia hạn một phần thì tách số lượng", "P0",
         "Phiếu P có hàng X: đang giữ 12, chỉ nhập Cần gia hạn = 5, hạn hiện tại 10/03/2026, "
         "hạn mới 30/03/2026. Phiếu đang Chờ KT duyệt",
         "1. Đăng nhập G, bấm 'KT Duyệt'\n2. Vào Danh sách hàng giữ tìm hàng X khách KH001",
         "Gia hạn 5 trong 12",
         "- Dòng hạn 10/03/2026 còn 7\n- Dòng hạn 30/03/2026 có 5\n- Tổng vẫn là 12"),

        ("010", "Gia hạn vào hạn đã có sẵn thì cộng gộp", "P0",
         "Người lập đang có 2 dòng giữ hàng X của khách KH001: hạn 10/03/2026 số lượng 12 và "
         "hạn 30/03/2026 số lượng 4. Phiếu P xin gia hạn 12 của dòng 10/03/2026 sang 30/03/2026",
         "1. Đăng nhập G, bấm 'KT Duyệt'\n2. Vào Danh sách hàng giữ tìm hàng X khách KH001\n"
         "3. Đếm số dòng của hàng X",
         "12 + 4",
         "- Chỉ còn dòng hạn 30/03/2026 với số lượng 16\n"
         "- Dòng hạn 10/03/2026 còn 0\n"
         "- KHÔNG phát sinh dòng 30/03/2026 thứ hai"),

        ("011", "Hạn giữ mới trùng hạn cũ thì không đổi gì", "P1",
         "Phiếu P có hàng X hạn hiện tại 30/03/2026, người duyệt để Hạn giữ mới đúng bằng 30/03/2026",
         "1. Đăng nhập G, bấm 'KT Duyệt'\n2. Vào Danh sách hàng giữ tìm hàng X",
         "Hạn cũ = hạn mới = 30/03/2026",
         "- Số lượng của dòng hạn 30/03/2026 không thay đổi\n- Không phát sinh dòng giữ hàng mới"),

        ("012", "Người duyệt sửa Hạn giữ mới trước khi duyệt", "P0",
         "Phiếu P Chờ KT duyệt, hàng X đang có Hạn giữ mới = 30/03/2026",
         "1. Đăng nhập G, mở phiếu P\n2. Sửa Hạn giữ mới của hàng X thành 25/03/2026\n"
         "3. Bấm 'KT Duyệt'\n4. Vào Danh sách hàng giữ kiểm tra",
         "30/03/2026 → 25/03/2026",
         "- Hàng X được chuyển sang dòng hạn 25/03/2026, không phải 30/03/2026\n"
         "- Ngày người duyệt sửa mới là ngày có hiệu lực"),

        ("013", "Sửa Hạn giữ mới ở DÒNG ĐẦU tại màn duyệt ghi đè toàn bộ", "P0",
         "Phiếu P Chờ KT duyệt, có 3 dòng với Hạn giữ mới lần lượt 25/03/2026 · 28/03/2026 · 30/03/2026",
         "1. Đăng nhập G, mở phiếu P\n2. Sửa Hạn giữ mới của DÒNG 1 thành 20/03/2026\n"
         "3. Đọc ô Hạn giữ mới của dòng 2 và dòng 3",
         "Dòng 1: 25/03/2026 → 20/03/2026",
         "- Dòng 2 và dòng 3 bị ĐỔI HẾT thành 20/03/2026, kể cả khi trước đó đã có ngày khác\n"
         "⚠️ Bẫy nặng nhất của màn duyệt — phải kiểm lại toàn bộ các dòng trước khi bấm duyệt"),

        ("014", "Sửa Hạn giữ mới ở dòng thứ hai trở đi chỉ đổi dòng đó", "P0",
         "Phiếu P Chờ KT duyệt, có 3 dòng với Hạn giữ mới 25/03/2026 · 28/03/2026 · 30/03/2026",
         "1. Đăng nhập G, mở phiếu P\n2. Sửa Hạn giữ mới của DÒNG 2 thành 26/03/2026\n"
         "3. Đọc ô Hạn giữ mới của dòng 1 và dòng 3",
         "Dòng 2: 28/03/2026 → 26/03/2026",
         "- Dòng 1 vẫn 25/03/2026, dòng 3 vẫn 30/03/2026\n- Chỉ dòng 2 thay đổi"),

        ("015", "Người duyệt tích thêm dòng chưa được chọn", "P0",
         "Phiếu P Chờ KT duyệt, có 5 dòng, người lập chỉ tích 3",
         "1. Đăng nhập G, mở phiếu P\n2. Tích thêm dòng thứ 4, nhập Hạn giữ mới hợp lệ\n"
         "3. Bấm 'KT Duyệt'\n4. Mở lại màn xem phiếu P",
         "3 dòng → 4 dòng",
         "- Phiếu chuyển sang Đã duyệt\n- Màn xem hiển thị đủ 4 dòng đã tích\n"
         "- Danh sách hàng giữ được dời hạn cho cả 4 mặt hàng"),

        ("016", "Người duyệt bỏ tích một dòng", "P1",
         "Phiếu P Chờ KT duyệt, có 3 dòng đều đã tích",
         "1. Đăng nhập G, mở phiếu P\n2. Bỏ tích dòng 3\n3. Bấm 'KT Duyệt'\n"
         "4. Vào Danh sách hàng giữ kiểm tra mặt hàng của dòng 3",
         "3 dòng → còn 2 dòng tích",
         "- Phiếu chuyển sang Đã duyệt\n"
         "- Hàng của dòng 3 giữ nguyên hạn cũ, không bị dời"),

        ("017", "Không duyệt ở cấp Trưởng phòng", "P0",
         "Phiếu P Chờ TP duyệt. Tài khoản E là Trưởng phòng quản lý phòng của phiếu",
         "1. Đăng nhập E, mở phiếu P\n2. Bấm 'Không duyệt'\n"
         "3. Nhập ghi chú 'Chưa đủ căn cứ gia hạn'\n4. Bấm 'Xác nhận'\n5. Kiểm tra trạng thái phiếu",
         "Ghi chú: Chưa đủ căn cứ gia hạn",
         "- Cửa sổ 'Ghi chú duyệt' mở ra với 1 ô nhập\n"
         "- Sau khi xác nhận: thông báo 'Thao tác thành công!'\n"
         "- Phiếu P quay về trạng thái 'Đang tạo'\n"
         "- Người lập nhận thông báo '… vừa từ chối yêu cầu gia hạn hàng giữ: PGHHG-…'"),

        ("018", "Không duyệt ở cấp Ban giám đốc", "P0",
         "Phiếu P Chờ BGĐ duyệt. Tài khoản F có quyền Ban giám đốc duyệt hàng giữ",
         "1. Đăng nhập F, mở phiếu P\n2. Bấm 'Không duyệt', nhập ghi chú 'Giá trị quá lớn'\n"
         "3. Bấm 'Xác nhận'\n4. Kiểm tra trạng thái",
         "Ghi chú: Giá trị quá lớn",
         "- Phiếu P quay về 'Đang tạo'\n- Người lập nhận thông báo từ chối"),

        ("019", "Không duyệt ở cấp Kế toán", "P0",
         "Phiếu P Chờ KT duyệt. Tài khoản G có quyền Kế toán duyệt hàng giữ",
         "1. Đăng nhập G, mở phiếu P\n2. Bấm 'Không duyệt', nhập ghi chú 'Hàng đã có người đặt'\n"
         "3. Bấm 'Xác nhận'\n4. Kiểm tra trạng thái và Danh sách hàng giữ",
         "Ghi chú: Hàng đã có người đặt",
         "- Phiếu P quay về 'Đang tạo'\n- Hạn giữ của hàng KHÔNG bị thay đổi"),

        ("020", "Ghi chú khi Không duyệt là bắt buộc", "P0",
         "Phiếu P Chờ KT duyệt, tài khoản G đang mở cửa sổ 'Ghi chú duyệt'",
         "1. Để trống ô ghi chú\n2. Bấm 'Xác nhận'",
         "Ghi chú: (để trống)",
         "- Hệ thống báo lỗi đỏ 'Bắt buộc phải nhập' ngay dưới ô ghi chú\n"
         "- Cửa sổ không đóng, phiếu vẫn ở Chờ KT duyệt"),

        ("021", "Ghi chú khi Không duyệt tối đa 255 ký tự", "P1",
         "Phiếu P Chờ KT duyệt, đang mở cửa sổ 'Ghi chú duyệt'",
         "1. Dán đoạn văn dài 300 ký tự vào ô ghi chú\n2. Bấm 'Xác nhận'",
         "Ghi chú: 300 ký tự",
         "- Hệ thống báo lỗi đỏ 'Không được vượt quá 255 ký tự'\n- Phiếu không đổi trạng thái"),

        ("022", "Ghi chú duyệt hiển thị lại trên phiếu bị từ chối", "P1",
         "Phiếu P vừa bị Không duyệt kèm ghi chú 'Chưa đủ căn cứ gia hạn'",
         "1. Đăng nhập bằng người lập\n2. Mở màn xem phiếu P\n3. Đọc khối Thông tin chung",
         "—",
         "- Có ô 'Ghi chú duyệt' hiện đúng nội dung 'Chưa đủ căn cứ gia hạn'"),

        ("023", "Phiếu bị từ chối sửa lại và gửi lần hai", "P0",
         "Phiếu P vừa bị Không duyệt, đang ở 'Đang tạo', do tài khoản A lập",
         "1. Đăng nhập A, mở màn Sửa phiếu P\n2. Sửa Hạn giữ mới thành 25/03/2026\n"
         "3. Bấm 'Lưu & Gửi'\n4. Kiểm tra trạng thái",
         "Hạn giữ mới: 25/03/2026",
         "- Phiếu P quay lại 'Chờ TP duyệt'\n- Trưởng phòng nhận lại thông báo cần duyệt"),

        ("024", "Nút duyệt chỉ hiện đúng cấp đang tới lượt", "P0",
         "Phiếu P đang 'Chờ KT duyệt'. Tài khoản E là Trưởng phòng có quyền duyệt và được xem phiếu",
         "1. Đăng nhập E, mở màn xem phiếu P\n2. Quan sát khối nút cuối trang",
         "Phiếu P — Chờ KT duyệt · Tài khoản E là Trưởng phòng",
         "- Không có nút 'TP Duyệt', không có nút 'Không duyệt'\n- Chỉ có nút 'Quay lại'"),

        ("025", "Trưởng phòng bị chặn duyệt khi phòng còn nhân viên quá hạn", "P0",
         "Công ty bật cấu hình chặn quá hạn với thao tác 'Duyệt gia hạn hàng giữ'. Phòng do Trưởng "
         "phòng E quản lý còn nhân viên đang có phiếu quá hạn. Phiếu P đang Chờ TP duyệt",
         "1. Đăng nhập E, mở phiếu P\n2. Bấm 'TP Duyệt'\n3. Đọc thông báo\n4. Kiểm tra trạng thái",
         "Tài khoản: E · phòng có nhân viên quá hạn",
         "- Hệ thống chặn, hiện thông báo cảnh báo về tình trạng quá hạn\n"
         "- Phiếu P vẫn ở 'Chờ TP duyệt'"),

        ("026", "Sau khi duyệt hệ thống quay về màn chờ duyệt", "P1",
         "Tài khoản G đang mở phiếu P từ màn Phiếu yêu cầu gia hạn hàng giữ chờ duyệt",
         "1. Bấm 'KT Duyệt'\n2. Quan sát trang được chuyển tới",
         "—",
         "- Hệ thống quay về màn danh sách chờ duyệt\n- Phiếu P không còn trong lưới chờ duyệt"),

        ("027", "Sau khi Không duyệt hệ thống quay về màn chờ duyệt", "P1",
         "Tài khoản G đang mở phiếu P từ màn chờ duyệt",
         "1. Bấm 'Không duyệt', nhập ghi chú, bấm 'Xác nhận'\n2. Quan sát trang được chuyển tới",
         "—",
         "- Hệ thống quay về màn danh sách chờ duyệt\n- Phiếu P không còn trong lưới chờ duyệt"),

        ("028", "Nút duyệt khóa lại trong lúc xử lý", "P1",
         "Phiếu P Chờ KT duyệt, tài khoản G đang mở màn xem",
         "1. Bấm 'KT Duyệt'\n2. Quan sát nút ngay sau khi bấm",
         "—",
         "- Nút đổi sang biểu tượng đang quay và không bấm lại được cho tới khi có phản hồi\n"
         "- Không tạo ra hai lần duyệt cho cùng một phiếu"),
    ]),

    # ----------------------------------------------------------------- VI
    ("VI", "XÓA", [
        ("001", "Xóa phiếu Đang tạo do mình lập", "P0",
         "Tài khoản A lập phiếu P đang ở 'Đang tạo' với 3 dòng hàng",
         "1. Đăng nhập A, vào màn danh sách\n2. Bấm bánh răng của phiếu P, chọn 'Xóa'\n"
         "3. Xác nhận\n4. Tìm lại phiếu P trên lưới",
         "Phiếu P — Đang tạo",
         "- Thông báo 'Xóa thành công!'\n- Phiếu P biến mất khỏi lưới\n"
         "- Các dòng hàng của phiếu cũng bị xóa theo"),

        ("002", "Xóa phiếu không làm đổi hàng đang giữ", "P0",
         "Phiếu P Đang tạo xin gia hạn hàng X 12 đơn vị. Trước khi xóa, hàng X đang giữ 12 với hạn "
         "10/03/2026",
         "1. Xóa phiếu P\n2. Vào Danh sách hàng giữ tìm hàng X",
         "Hàng X: 12 · hạn 10/03/2026",
         "- Hàng X vẫn giữ nguyên 12 đơn vị, hạn vẫn 10/03/2026\n"
         "- Phiếu Đang tạo chưa hề tác động tới hàng giữ"),

        ("003", "Không xóa được phiếu đã gửi đi duyệt", "P0",
         "Phiếu Q của tài khoản A đang ở 'Chờ TP duyệt'",
         "1. Đăng nhập A, vào màn danh sách\n2. Bấm bánh răng của phiếu Q",
         "Phiếu Q — Chờ TP duyệt",
         "- Menu không có mục 'Xóa' và không có mục 'Sửa'"),

        ("004", "Không xóa được phiếu Đã duyệt", "P0",
         "Phiếu U của tài khoản A đang ở 'Đã duyệt'",
         "1. Đăng nhập A, bấm bánh răng của phiếu U\n"
         "2. Dùng công cụ kiểm thử gọi thẳng chức năng Xóa phiếu U\n3. Tìm lại phiếu U trên lưới",
         "Phiếu U — Đã duyệt",
         "- Menu không có mục 'Xóa'\n- Gọi thẳng chức năng Xóa bị từ chối với thông báo "
         "'Không thể xóa!'\n- Phiếu U vẫn còn trên lưới"),

        ("005", "Xóa xong quay về màn danh sách", "P1",
         "Đang ở màn danh sách, có phiếu Đang tạo",
         "1. Xóa một phiếu Đang tạo\n2. Quan sát trang sau khi xóa",
         "—",
         "- Vẫn ở màn danh sách, không bị đẩy sang trang khác\n- Lưới đã được nạp lại"),
    ]),

    # ---------------------------------------------------------------- VII
    ("VII", "XUẤT EXCEL / IN", [
        ("001", "Xuất Excel danh sách phiếu", "P0",
         "Lưới đang hiện 12 phiếu, không lọc gì",
         "1. Bấm nút 'Xuất excel' phía trên lưới\n2. Mở tệp tải về",
         "—",
         "- Tệp tải về tên 'danh_sach_yeu_cau_gia_han_giu'\n"
         "- Có tiêu đề 'Danh sách yêu cầu gia hạn giữ' và phần đầu trang của công ty\n"
         "- Bảng có 7 cột: STT · Mã phiếu · Người lập · Ngày lập · Trạng thái · Người duyệt · "
         "Ngày duyệt\n- Có đủ 12 dòng"),

        ("002", "Xuất Excel áp đúng bộ lọc đang dùng", "P0",
         "Đang lọc Trạng thái = Đã duyệt, lưới còn 4 dòng",
         "1. Bấm 'Xuất excel'\n2. Mở tệp tải về và đếm số dòng",
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

        ("005", "In một phiếu", "P0",
         "Phiếu P có 3 dòng hàng đã tích cần gia hạn",
         "1. Bấm bánh răng của phiếu P, chọn 'In'\n2. Quan sát tab mới mở ra",
         "Phiếu P",
         "- Mở tab mới với bản in khổ ngang, tiêu đề 'Phiếu yêu cầu gia hạn giữ'\n"
         "- Có Số phiếu, Ngày lập, Ghi chú và phần đầu trang của công ty\n"
         "- Bảng có 8 cột: STT · Tên hàng hóa · Khách hàng · Hợp đồng · Đơn vị tính · Cần gia hạn · "
         "Hạn giữ hiện tại · Hạn giữ mới"),

        ("006", "Bản in hiển thị đủ Model và mã hàng hóa", "P1",
         "Phiếu P có hàng 'Máy nén khí Puma 5HP', model 'PK-5100', mã 'MNK-PUMA-5HP'",
         "1. Mở bản in của phiếu P\n2. Đọc ô Tên hàng hóa của dòng đầu",
         "—",
         "- Ô hiện tên hàng, dòng 'Model: PK-5100' và dòng 'Mã hàng hóa: MNK-PUMA-5HP'"),

        ("007", "Bản in hiển thị đúng ngày", "P1",
         "Phiếu P có hàng hạn hiện tại 10/03/2026, hạn mới 30/03/2026",
         "1. Mở bản in phiếu P\n2. Đọc hai cột hạn giữ",
         "—",
         "- Cột Hạn giữ hiện tại: 10/03/2026\n- Cột Hạn giữ mới: 30/03/2026\n"
         "- Không có ô nào hiện chữ lạ thay cho ngày trống"),

        ("008", "Xuất Excel một phiếu", "P1",
         "Phiếu P có 3 dòng hàng",
         "1. Bấm bánh răng của phiếu P, chọn 'Xuất excel'\n2. Mở tệp tải về",
         "Phiếu P",
         "- Tệp tên 'phieu_yeu_cau_gia_han_giu'\n"
         "- Nội dung khớp bản in: đủ 8 cột và đủ 3 dòng hàng"),

        ("009", "Người không được xem thì không In / Xuất được phiếu", "P0",
         "Tài khoản A không phải người lập và không có quyền duyệt nào. Phiếu Q của tài khoản B, "
         "đang Chờ KT duyệt",
         "1. Đăng nhập A\n2. Mở đường dẫn In của phiếu Q\n3. Mở đường dẫn Xuất excel của phiếu Q",
         "Phiếu Q của B",
         "- Cả hai đều hiển thị trang báo không tìm thấy dữ liệu\n"
         "- Không tải về tệp nào"),

        ("010", "Bản in của phiếu Đang tạo", "P2",
         "Tài khoản A lập phiếu P đang ở 'Đang tạo'",
         "1. Đăng nhập A, bấm bánh răng phiếu P, chọn 'In'",
         "Phiếu P — Đang tạo",
         "- Bản in mở được bình thường với đầy đủ dòng hàng đã tích"),
    ]),

    # --------------------------------------------------------------- VIII
    ("VIII", "RÀNG BUỘC NHẬP LIỆU", [
        ("001", "Không tích dòng nào mà vẫn gửi", "P0",
         "Đang ở màn Tạo mới, bảng Chi tiết có 3 dòng, không tích dòng nào",
         "1. Bấm 'Lưu & Gửi'\n2. Đọc thông báo",
         "0 dòng được tích",
         "- Hệ thống báo 'Chưa chọn hàng nào'\n- Không tạo ra phiếu mới"),

        ("002", "Tích dòng nhưng để Cần gia hạn bằng 0", "P0",
         "Đang ở màn Tạo mới, tích 1 dòng, sửa Cần gia hạn thành 0",
         "1. Nhập Hạn giữ mới hợp lệ\n2. Bấm 'Lưu & Gửi'\n3. Đọc thông báo",
         "Cần gia hạn: 0",
         "- Hệ thống báo 'Chưa chọn hàng nào'\n- Không tạo ra phiếu mới"),

        ("003", "Xóa trắng ô Cần gia hạn", "P0",
         "Đang ở màn Tạo mới, tích 1 dòng",
         "1. Xóa trắng ô Cần gia hạn của dòng đó\n2. Nhập Hạn giữ mới hợp lệ\n3. Bấm 'Lưu & Gửi'",
         "Cần gia hạn: (rỗng)",
         "- Hệ thống báo lỗi đỏ ngay dưới ô Cần gia hạn với nội dung 'Bắt buộc nhập' hoặc "
         "'Chưa chọn hàng nào'\n- Không tạo ra phiếu mới"),

        ("004", "Cần gia hạn vượt quá 6 chữ số", "P1",
         "Đang ở màn Tạo mới, tích 1 dòng",
         "1. Nhập Cần gia hạn = 1000000\n2. Nhập Hạn giữ mới hợp lệ\n3. Bấm 'Lưu & Gửi'",
         "Cần gia hạn: 1000000",
         "- Hệ thống báo lỗi đỏ 'Không được vượt quá 6 chữ số' ngay dưới ô\n"
         "- Không tạo ra phiếu mới"),

        ("005", "Cần gia hạn là số âm", "P0",
         "Đang ở màn Tạo mới, tích 1 dòng",
         "1. Nhập Cần gia hạn = -3\n2. Nhập Hạn giữ mới hợp lệ\n3. Bấm 'Lưu & Gửi'",
         "Cần gia hạn: -3",
         "- Hệ thống báo lỗi, không cho tạo phiếu\n"
         "⚠️ Kiểm tra kỹ: không được âm thầm quy về 0 rồi vẫn lưu"),

        ("006", "Cần gia hạn lớn hơn số đang giữ", "P0",
         "Hàng X đang giữ 12 đơn vị. Đang ở màn Tạo mới, đã tích dòng hàng X",
         "1. Nhập Cần gia hạn = 20\n2. Nhập Hạn giữ mới hợp lệ\n3. Bấm 'Lưu & Gửi'",
         "Đang giữ 12 · nhập 20",
         "- Dòng hàng được tô cảnh báo ngay khi nhập\n"
         "- Khi gửi, hệ thống báo 'Hàng <tên hàng> không đủ số lượng'\n"
         "- Không tạo ra phiếu mới"),

        ("007", "Cần gia hạn quy đổi theo đơn vị tính khi kiểm tra tồn", "P0",
         "Hàng X đang giữ 24 Cái, có đơn vị Thùng hệ số 12. Đang ở màn Tạo mới",
         "1. Đổi Đơn vị tính của dòng hàng X sang Thùng\n2. Nhập Cần gia hạn = 3\n"
         "3. Nhập Hạn giữ mới hợp lệ\n4. Bấm 'Lưu & Gửi'",
         "3 Thùng = 36 Cái > 24 Cái đang giữ",
         "- Hệ thống báo 'Hàng <tên hàng> không đủ số lượng'\n"
         "⚠️ Phải so theo số quy đổi, không phải so 3 với 24"),

        ("008", "Nhập Cần gia hạn đúng bằng số đang giữ", "P0",
         "Hàng X đang giữ 12 đơn vị. Đang ở màn Tạo mới, đã tích dòng hàng X",
         "1. Nhập Cần gia hạn = 12\n2. Nhập Hạn giữ mới hợp lệ\n3. Bấm 'Lưu & Gửi'",
         "Cần gia hạn = 12 = đang giữ",
         "- Phiếu được tạo thành công, trạng thái 'Chờ TP duyệt'\n- Không có cảnh báo nào"),

        ("009", "Bỏ trống Hạn giữ mới của dòng đã tích", "P0",
         "Đang ở màn Tạo mới, tích 1 dòng, Cần gia hạn hợp lệ",
         "1. Xóa trắng ô Hạn giữ mới\n2. Bấm 'Lưu & Gửi'",
         "Hạn giữ mới: (rỗng)",
         "- Hệ thống báo lỗi đỏ 'Bắt buộc phải nhập' ngay dưới ô Hạn giữ mới\n"
         "- Không tạo ra phiếu mới"),

        ("010", "Hạn giữ mới là ngày trong quá khứ", "P0",
         "Hôm nay 05/03/2026. Đang ở màn Tạo mới, tích 1 dòng",
         "1. Nhập Hạn giữ mới = 01/03/2026\n2. Bấm 'Lưu & Gửi'",
         "Hôm nay = 05/03/2026 · nhập 01/03/2026",
         "- Hệ thống báo lỗi đỏ 'Phải nhập ngày tương lai'\n- Không tạo ra phiếu mới"),

        ("011", "Hạn giữ mới đúng bằng ngày hôm nay", "P0",
         "Hôm nay 05/03/2026. Đang ở màn Tạo mới, tích 1 dòng",
         "1. Nhập Hạn giữ mới = 05/03/2026\n2. Bấm 'Lưu & Gửi'",
         "Hạn giữ mới = hôm nay",
         "- Hệ thống báo lỗi đỏ 'Phải nhập ngày tương lai'\n"
         "⚠️ Ngày hôm nay KHÔNG được chấp nhận, phải từ ngày mai trở đi"),

        ("012", "Hạn giữ mới vượt số ngày giữ tối đa", "P0",
         "Cấu hình 'Số ngày giữ tối đa' = 30. Hôm nay 05/03/2026. Đang ở màn Tạo mới, tích 1 dòng",
         "1. Nhập Hạn giữ mới = 20/05/2026\n2. Bấm 'Lưu & Gửi'\n3. Đọc thông báo",
         "Hôm nay = 05/03/2026 · Số ngày giữ tối đa = 30",
         "- Hệ thống báo 'Không thể giữ quá 04/04/2026'\n- Không tạo ra phiếu mới\n"
         "⚠️ Ngày trần được tính từ HÔM NAY, không tính từ hạn giữ hiện tại"),

        ("013", "Hạn giữ mới đúng ngày trần", "P1",
         "Cấu hình 'Số ngày giữ tối đa' = 30. Hôm nay 05/03/2026",
         "1. Nhập Hạn giữ mới = 04/04/2026\n2. Bấm 'Lưu & Gửi'",
         "Ngày trần = 04/04/2026",
         "- Phiếu được tạo thành công, không hiện thông báo chặn"),

        ("014", "Hạn giữ mới sớm hơn hạn giữ hiện tại", "P1",
         "Hôm nay 05/03/2026. Hàng X có hạn giữ hiện tại 20/03/2026",
         "1. Nhập Hạn giữ mới = 10/03/2026\n2. Bấm 'Lưu & Gửi'\n3. Ghi nhận kết quả",
         "Hạn hiện tại 20/03/2026 · nhập 10/03/2026",
         "- Hệ thống cho lưu (chỉ chặn ngày quá khứ và ngày vượt trần)\n"
         "⚠️ Ghi nhận rõ kết quả thực tế: đây là trường hợp rút ngắn hạn giữ chứ không phải gia hạn"),

        ("015", "Ghi chú vượt 255 ký tự", "P1",
         "Đang ở màn Tạo mới, đã tích và điền hợp lệ 1 dòng",
         "1. Dán đoạn văn dài 300 ký tự vào ô Ghi chú\n2. Bấm 'Lưu & Gửi'",
         "Ghi chú: 300 ký tự",
         "- Hệ thống báo lỗi đỏ 'Không được vượt quá 255 ký tự' ngay dưới ô Ghi chú\n"
         "- Không tạo ra phiếu mới"),

        ("016", "Ghi chú để trống", "P1",
         "Đang ở màn Tạo mới, đã tích và điền hợp lệ 1 dòng, ô Ghi chú để trống",
         "1. Bấm 'Lưu & Gửi'\n2. Ghi nhận kết quả",
         "Ghi chú: (để trống)",
         "- Phiếu được tạo thành công dù ô Ghi chú có dấu sao đỏ như trường bắt buộc\n"
         "⚠️ Ghi nhận rõ: nhãn có dấu sao nhưng hệ thống KHÔNG bắt buộc"),

        ("017", "Đính kèm tệp quá 13 MB", "P1",
         "Có sẵn tệp PDF dung lượng 15 MB. Đang ở màn Tạo mới, đã tích và điền hợp lệ 1 dòng",
         "1. Thêm ô đính kèm và chọn tệp 15 MB\n2. Bấm 'Lưu & Gửi'",
         "Tệp: 15 MB",
         "- Hệ thống báo lỗi 'File đính kèm không được quá 13 MB.' trên ô đính kèm\n"
         "- Không tạo ra phiếu mới"),

        ("018", "Đính kèm tệp sai định dạng", "P1",
         "Có sẵn tệp 'ghi-am.mp3'. Đang ở màn Tạo mới, đã tích và điền hợp lệ 1 dòng",
         "1. Thêm ô đính kèm, chuyển bộ lọc sang 'All files' và chọn tệp mp3\n2. Bấm 'Lưu & Gửi'",
         "Tệp: ghi-am.mp3",
         "- Hệ thống báo lỗi 'File đính kèm phải là file PDF, PNG, JPG, DOCX, DOC, XLS, XLSX, JPEG.'\n"
         "- Không tạo ra phiếu mới"),

        ("019", "Đính kèm nhiều tệp hợp lệ cùng lúc", "P1",
         "Có sẵn tệp 'bien-ban.pdf' và 'anh-hang.jpg'. Đang ở màn Tạo mới, đã tích và điền hợp lệ",
         "1. Thêm 2 ô đính kèm, chọn 2 tệp trên\n2. Bấm 'Lưu & Gửi'\n3. Mở màn xem của phiếu vừa tạo",
         "2 tệp hợp lệ",
         "- Phiếu tạo thành công\n- Màn xem hiện cả 2 tệp, bấm vào mở xem được"),

        ("020", "Thêm ô đính kèm nhưng không chọn tệp", "P1",
         "Đang ở màn Tạo mới, đã tích và điền hợp lệ 1 dòng",
         "1. Bấm dấu cộng thêm 1 ô đính kèm nhưng KHÔNG chọn tệp\n2. Bấm 'Lưu & Gửi'",
         "1 ô đính kèm rỗng",
         "- Hệ thống báo lỗi 'Bắt buộc phải đính kèm.' trên ô đính kèm rỗng\n"
         "- Không tạo ra phiếu mới"),

        ("021", "Người duyệt bỏ trống Hạn giữ mới rồi bấm duyệt", "P0",
         "Phiếu P Chờ KT duyệt, có 2 dòng đã tích. Tài khoản G đang mở màn xem",
         "1. Xóa trắng ô Hạn giữ mới của dòng 2\n2. Bấm 'KT Duyệt'",
         "Hạn giữ mới dòng 2: (rỗng)",
         "- Hệ thống báo lỗi đỏ 'Bắt buộc phải nhập' ngay dưới ô Hạn giữ mới của dòng 2\n"
         "- Phiếu vẫn ở 'Chờ KT duyệt'"),

        ("022", "Người duyệt nhập Hạn giữ mới là ngày quá khứ", "P0",
         "Hôm nay 05/03/2026. Phiếu P Chờ KT duyệt. Tài khoản G đang mở màn xem",
         "1. Sửa Hạn giữ mới của dòng 1 thành 01/03/2026\n2. Bấm 'KT Duyệt'",
         "Nhập 01/03/2026 · hôm nay 05/03/2026",
         "- Hệ thống báo lỗi đỏ 'Phải nhập ngày tương lai'\n- Phiếu không đổi trạng thái"),

        ("023", "Số lượng đã bị dùng hết trước khi Kế toán duyệt", "P0",
         "Phiếu P Chờ KT duyệt xin gia hạn hàng X 12 đơn vị. Trong lúc chờ, hàng X của người lập đã bị "
         "xuất hết, số đang giữ còn 0",
         "1. Đăng nhập G, mở phiếu P\n2. Bấm 'KT Duyệt'\n3. Đọc thông báo",
         "Đang giữ còn 0 · xin gia hạn 12",
         "- Hệ thống báo 'Hàng <tên hàng> không đủ số lượng'\n"
         "- Phiếu không chuyển sang Đã duyệt"),
    ]),

    # ----------------------------------------------------------------- IX
    ("IX", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", [
        ("001", "Chặn tạo phiếu khi người lập có hàng mượn quá hạn", "P0",
         "Công ty bật cấu hình chặn nhóm 'Hàng mượn quá hạn' với thao tác 'Gia hạn hàng giữ'. "
         "Tài khoản A đang có 1 phiếu mượn quá hạn chưa trả",
         "1. Đăng nhập A\n2. Bấm 'Tạo mới' ở màn danh sách\n3. Quan sát trang",
         "Tài khoản: A có hàng mượn quá hạn",
         "- Hệ thống không mở màn Tạo mới, quay lại màn danh sách kèm cảnh báo "
         "'Có hàng mượn quá hạn!'"),

        ("002", "Chặn lưu phiếu khi người lập có hàng nhập thẳng quá hạn", "P0",
         "Công ty bật cấu hình chặn nhóm 'Hàng nhập thẳng quá hạn' với thao tác 'Gia hạn hàng giữ'. "
         "Tài khoản A có hàng nhập thẳng đã quá số ngày cho phép",
         "1. Đăng nhập A\n2. Bấm 'Tạo mới'\n3. Quan sát trang",
         "Tài khoản: A có hàng nhập thẳng quá hạn",
         "- Hệ thống không mở màn Tạo mới, quay lại kèm cảnh báo 'Có hàng nhập thẳng quá hạn!'"),

        ("003", "Hàng GIỮ quá hạn không chặn màn này", "P0",
         "Công ty bật cấu hình chặn nhóm 'Hàng giữ quá hạn' cho các thao tác khác. Tài khoản A đang có "
         "hàng giữ quá hạn",
         "1. Đăng nhập A\n2. Bấm 'Tạo mới'\n3. Điền hợp lệ và bấm 'Lưu & Gửi'",
         "Tài khoản: A có hàng giữ quá hạn",
         "- Màn Tạo mới mở bình thường\n- Phiếu được tạo thành công\n"
         "⚠️ Đúng ra phải vậy: nhóm chặn 'Hàng giữ quá hạn' không áp cho màn gia hạn hàng giữ"),

        ("004", "Người quản trị cao nhất không bị chặn quá hạn", "P1",
         "Tài khoản quản trị cao nhất đang có hàng mượn quá hạn, công ty đang bật cấu hình chặn",
         "1. Đăng nhập bằng tài khoản quản trị cao nhất\n2. Bấm 'Tạo mới'",
         "Tài khoản: quản trị cao nhất",
         "- Màn Tạo mới mở bình thường, không có cảnh báo chặn"),

        ("005", "Hai người duyệt cùng một phiếu gần như đồng thời", "P0",
         "Phiếu P Chờ KT duyệt. Hai tài khoản G1 và G2 cùng có quyền Kế toán duyệt hàng giữ, cùng mở "
         "màn xem phiếu P",
         "1. G1 bấm 'KT Duyệt', chờ thành công\n2. G2 bấm 'KT Duyệt' trên tab đã mở sẵn\n"
         "3. Mở lại phiếu P kiểm tra\n4. Vào Danh sách hàng giữ kiểm tra số lượng",
         "Phiếu P · 2 người duyệt",
         "- Phiếu P chỉ ghi nhận 1 người duyệt và 1 ngày duyệt\n"
         "- Số lượng hàng giữ chỉ được dời MỘT lần, không bị trừ hai lần\n"
         "⚠️ Đây là trường hợp dễ sinh sai lệch số lượng hàng giữ nhất"),

        ("006", "Người lập sửa phiếu trong lúc người duyệt đang mở", "P1",
         "Phiếu P Đang tạo, tài khoản A mở màn Sửa. Cùng lúc phiếu P bị A gửi đi ở một tab khác",
         "1. Ở tab 1 tài khoản A bấm 'Lưu & Gửi' → phiếu sang Chờ TP duyệt\n"
         "2. Quay lại tab 2 đang mở màn Sửa, bấm 'Lưu'\n3. Đọc thông báo",
         "Phiếu P",
         "- Hệ thống từ chối với thông báo không có quyền sửa phiếu này\n"
         "- Phiếu P vẫn ở 'Chờ TP duyệt', dữ liệu không bị ghi đè"),

        ("007", "Xóa phiếu trên tab này rồi thao tác trên tab kia", "P1",
         "Phiếu P Đang tạo, tài khoản A mở phiếu P ở 2 tab",
         "1. Ở tab 1 xóa phiếu P\n2. Ở tab 2 bấm 'Lưu'\n3. Quan sát kết quả",
         "Phiếu P đã bị xóa",
         "- Hệ thống báo dữ liệu đã thay đổi, không treo trang\n"
         "- Không phục hồi lại phiếu đã xóa"),

        ("008", "Dữ liệu bảng Chi tiết được nạp lại theo thời gian thực khi xem phiếu chưa duyệt", "P1",
         "Phiếu P đang Chờ KT duyệt xin gia hạn hàng X. Trong lúc chờ, số lượng đang giữ của hàng X "
         "giảm từ 12 xuống 7 do một phiếu xuất khác",
         "1. Đăng nhập G, mở màn xem phiếu P\n2. Đọc cột 'Đang giữ' của hàng X",
         "Đang giữ: 12 → 7",
         "- Cột 'Đang giữ' hiện 7, tức số hiện tại chứ không phải số lúc lập phiếu"),

        ("009", "Người lập khác công ty không thấy hàng giữ của công ty cũ", "P1",
         "Tài khoản A thuộc công ty 1, đang giữ hàng ở công ty 1. Tài khoản A được chuyển sang công ty 4",
         "1. Đăng nhập A (đang ở công ty 4)\n2. Bấm 'Tạo mới'\n3. Quan sát bảng Chi tiết",
         "Tài khoản: A · công ty 4",
         "- Bảng Chi tiết không nạp hàng giữ thuộc công ty 1"),
    ]),

    # ------------------------------------------------------------------ X
    ("X", "E2E FLOW", [
        ("001", "Luồng đầy đủ không qua Ban giám đốc", "P0",
         "Tài khoản A giữ hàng X 12 đơn vị, hạn 10/03/2026, không gắn hợp đồng, giá trị nhỏ hơn "
         "'Giá trị giữ hàng khác'. E là Trưởng phòng quản lý phòng của A, G là Kế toán duyệt. "
         "Hôm nay 05/03/2026",
         "1. A: Tạo mới → tích hàng X → Cần gia hạn 12 → Hạn giữ mới 30/03/2026 → 'Lưu & Gửi'\n"
         "2. E: mở phiếu → 'TP Duyệt'\n"
         "3. G: mở phiếu → 'KT Duyệt'\n"
         "4. A: mở màn danh sách và mở Danh sách hàng giữ kiểm tra",
         "Hàng X: 12 · 10/03/2026 → 30/03/2026",
         "- Sau bước 1: trạng thái 'Chờ TP duyệt', E nhận thông báo\n"
         "- Sau bước 2: trạng thái 'Chờ KT duyệt', G nhận thông báo\n"
         "- Sau bước 3: trạng thái 'Đã duyệt', có Người duyệt và Ngày duyệt, A nhận thông báo\n"
         "- Danh sách hàng giữ: dòng hạn 10/03/2026 còn 0, dòng hạn 30/03/2026 có 12"),

        ("002", "Luồng đầy đủ có qua Ban giám đốc", "P0",
         "Giống trên nhưng giá trị hàng xin gia hạn vượt 'Giá trị giữ hàng khác'. F là Ban giám đốc "
         "duyệt hàng giữ",
         "1. A: Tạo mới → điền hợp lệ → 'Lưu & Gửi'\n2. E: 'TP Duyệt'\n3. F: 'BGĐ Duyệt'\n"
         "4. G: 'KT Duyệt'\n5. Kiểm tra Danh sách hàng giữ",
         "Giá trị vượt ngưỡng",
         "- Sau bước 2: trạng thái 'Chờ BGĐ duyệt', F nhận thông báo\n"
         "- Sau bước 3: trạng thái 'Chờ KT duyệt', G nhận thông báo\n"
         "- Sau bước 4: trạng thái 'Đã duyệt' và hạn giữ được dời"),

        ("003", "Luồng bị từ chối rồi làm lại thành công", "P0",
         "Tài khoản A giữ hàng X, hôm nay 05/03/2026",
         "1. A: Tạo mới → điền Hạn giữ mới 30/03/2026 → 'Lưu & Gửi'\n"
         "2. E: 'Không duyệt', ghi chú 'Cần rút ngắn thời gian'\n"
         "3. A: mở phiếu, đọc ghi chú duyệt, vào Sửa → đổi Hạn giữ mới 20/03/2026 → 'Lưu & Gửi'\n"
         "4. E: 'TP Duyệt'\n5. G: 'KT Duyệt'\n6. Kiểm tra Danh sách hàng giữ",
         "30/03/2026 → 20/03/2026",
         "- Sau bước 2: phiếu về 'Đang tạo', A nhận thông báo từ chối, ô 'Ghi chú duyệt' hiện nội dung\n"
         "- Sau bước 3: phiếu về 'Chờ TP duyệt'\n"
         "- Sau bước 5: phiếu 'Đã duyệt', hàng X được dời sang hạn 20/03/2026"),

        ("004", "Luồng gia hạn một phần rồi gia hạn tiếp phần còn lại", "P0",
         "Tài khoản A giữ hàng X 12 đơn vị hạn 10/03/2026. Hôm nay 05/03/2026",
         "1. A lập phiếu 1 gia hạn 5 sang 20/03/2026, gửi và được duyệt hết cấp\n"
         "2. Kiểm tra Danh sách hàng giữ\n"
         "3. A lập phiếu 2 gia hạn 7 còn lại sang 25/03/2026, gửi và được duyệt hết cấp\n"
         "4. Kiểm tra lại Danh sách hàng giữ",
         "12 = 5 + 7",
         "- Sau bước 2: hạn 10/03/2026 còn 7, hạn 20/03/2026 có 5\n"
         "- Ở bước 3, bảng Chi tiết chỉ hiện dòng hàng còn hạn trong vùng cảnh báo\n"
         "- Sau bước 4: hạn 10/03/2026 còn 0, hạn 20/03/2026 có 5, hạn 25/03/2026 có 7\n"
         "- Tổng số lượng giữ vẫn đúng 12"),

        ("005", "Luồng nhiều dòng hàng nhiều khách hàng trong một phiếu", "P0",
         "Tài khoản A giữ: hàng X cho khách KH001 (12 đơn vị), hàng Y cho khách KH002 (8 đơn vị), "
         "hàng Z cho khách KH001 (5 đơn vị) — cả 3 đều trong vùng cảnh báo",
         "1. A: Tạo mới → tích cả 3 dòng → nhập Hạn giữ mới dòng 1 = 30/03/2026 (2 dòng còn lại tự "
         "điền) → 'Lưu & Gửi'\n2. E: 'TP Duyệt'\n3. G: 'KT Duyệt'\n"
         "4. Kiểm tra Danh sách hàng giữ cho cả KH001 và KH002",
         "3 dòng · 2 khách hàng",
         "- Dòng Tổng cộng ở bước 1 hiện 25 cho cả cột Đang giữ và Cần gia hạn\n"
         "- Sau bước 3: cả 3 mặt hàng đều xuất hiện ở hạn 30/03/2026 với đúng số lượng 12 · 8 · 5\n"
         "- Số lượng giữ theo từng khách hàng không bị trộn lẫn"),

        ("006", "Luồng phiếu lưu nháp rồi xóa", "P1",
         "Tài khoản A giữ hàng X 12 đơn vị hạn 10/03/2026",
         "1. A: Tạo mới → điền hợp lệ → bấm 'Lưu' (không gửi)\n"
         "2. Đăng nhập tài khoản D (quyền xem tổng công ty) kiểm tra lưới\n"
         "3. A: mở màn danh sách, xóa phiếu nháp\n4. Kiểm tra Danh sách hàng giữ của hàng X",
         "Phiếu nháp",
         "- Sau bước 1: phiếu ở 'Đang tạo', chỉ A nhìn thấy\n"
         "- Bước 2: D không thấy phiếu này\n"
         "- Sau bước 3: phiếu biến mất\n"
         "- Bước 4: hàng X vẫn 12 đơn vị hạn 10/03/2026, không bị ảnh hưởng"),

        ("007", "Luồng người duyệt sửa lại số dòng và ngày trước khi duyệt cuối", "P1",
         "Tài khoản A lập phiếu có 4 dòng nhưng chỉ tích 2, gửi đi. Phiếu đã qua Trưởng phòng, đang "
         "Chờ KT duyệt",
         "1. G: mở phiếu, thấy đủ 4 dòng\n2. G: tích thêm dòng 3, nhập Hạn giữ mới cho dòng 3\n"
         "3. G: sửa Hạn giữ mới của DÒNG 2 thành 22/03/2026\n"
         "4. G: đọc lại Hạn giữ mới của cả 3 dòng đang tích\n5. G: bấm 'KT Duyệt'\n"
         "6. Mở lại màn xem và kiểm tra Danh sách hàng giữ",
         "4 dòng · tích 2 → tích 3",
         "- Bước 3 chỉ đổi dòng 2, không ghi đè dòng khác (vì không phải dòng đầu)\n"
         "- Sau bước 5: phiếu 'Đã duyệt', màn xem hiện 3 dòng\n"
         "- Danh sách hàng giữ dời hạn cho đúng 3 mặt hàng, mỗi mặt hàng theo đúng ngày trên dòng của nó"),
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
