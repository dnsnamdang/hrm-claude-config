# -*- coding: utf-8 -*-
"""Generate testcase Excel cho cap man ERP: Phieu Yeu cau xuat giu + Phieu xuat giu.

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
FEATURE_NAME = "Phiếu Yêu cầu xuất giữ & Phiếu xuất giữ"
MODULE_NAME = "Giữ hàng - Xuất giữ"

# =========================================================================
# 9 MUC MO TA
# =========================================================================
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Hai màn này là MỘT cặp cha – con, phải test cùng nhau:\n"
     "► 'Phiếu Yêu cầu xuất giữ' (trên màn hình viết tắt là YCXG) — người kinh doanh xin giữ hàng "
     "trong kho cho một khách hàng đến một ngày nhất định. Phiếu đi qua các cấp duyệt: "
     "Trưởng phòng → (Ban giám đốc, khi vượt ngưỡng) → Kế toán.\n"
     "► 'Phiếu xuất giữ' — kế toán lập ra từ một phiếu yêu cầu đã tới lượt mình. Đây mới là nơi hàng "
     "THẬT SỰ được ghi thành hàng giữ. Trước bước này không có một đơn vị hàng nào bị giữ.\n"
     "Đường vào Phiếu Yêu cầu xuất giữ: menu Khởi tạo → Hàng hóa → nhóm Giữ hàng → "
     "'Phiếu Yêu cầu xuất giữ'; hoặc menu Kế toán → Hàng hóa - Dịch vụ - Vận chuyển → nhóm Giữ hàng → "
     "'Yêu cầu xuất giữ'. Người duyệt vào menu Chờ duyệt → nhóm Hàng giữ → "
     "'Phiếu yêu cầu xuất giữ chờ duyệt'.\n"
     "Đường vào Phiếu xuất giữ: CHỈ có ở menu Kế toán → Hàng hóa - Dịch vụ - Vận chuyển → nhóm "
     "Giữ hàng → 'Phiếu xuất giữ'. Ngoài ra vào được từ nút 'Tạo phiếu xuất giữ' trên phiếu yêu cầu."),

    ("2. Đối tượng được tính / hiển thị",
     "► Màn 'Danh sách yêu cầu xuất giữ' hiển thị phiếu ở 6 trạng thái: Đang tạo · Chờ TP duyệt · "
     "Chờ BGĐ duyệt · Chờ KT duyệt · Đang xuất giữ · Đã duyệt.\n"
     "► Phiếu ở trạng thái 'Đang tạo' CHỈ người lập ra nó mới nhìn thấy và mới mở xem được.\n"
     "► Màn 'Danh sách phiếu xuất giữ' hiển thị phiếu ở 2 trạng thái: Đang tạo (bản nháp của kế "
     "toán) và Đã duyệt.\n"
     "► Cửa sổ 'Phiếu yêu cầu xuất giữ' (bấm kính lúp ở ô 'Chọn phiếu yêu cầu xuất giữ') chỉ liệt kê "
     "những phiếu yêu cầu đang ở trạng thái 'Chờ KT duyệt'.\n"
     "► Cửa sổ chọn hàng hóa của loại 'Xuất giữ khác' chỉ liệt kê hàng còn tồn kho.\n"
     "► Với 5 loại yêu cầu có hợp đồng, bảng Chi tiết được nạp SẴN toàn bộ hàng của hợp đồng — người "
     "lập không thêm/bớt dòng được, chỉ tích 'Cần xuất' và nhập 'Đề nghị'."),

    ("3. Đối tượng bị ẩn / không tính",
     "► Phiếu 'Đang tạo' của người khác — không hiện trên lưới của bất kỳ ai khác, kể cả người có "
     "quyền xem theo công ty.\n"
     "► Trên màn 'Danh sách phiếu xuất giữ', người KHÔNG có quyền 'Trưởng phòng kế toán' chỉ thấy "
     "phiếu do chính mình lập, dù có đủ ba quyền xem theo tổng công ty / công ty / phòng ban. Đây là "
     "điểm rất dễ báo nhầm thành 'mất dữ liệu'.\n"
     "► Mục 'Sửa yêu cầu' và 'Xóa' bị ẩn khỏi menu Hành động khi phiếu yêu cầu không còn ở trạng "
     "thái 'Đang tạo', hoặc người xem không phải người lập.\n"
     "► Nút 'Sửa' và 'Xóa' của Phiếu xuất giữ chỉ hiện khi phiếu còn là bản nháp 'Đang tạo' VÀ người "
     "xem chính là người lập phiếu.\n"
     "► Ô 'Loại yêu cầu' bị khóa ngay khi phiếu đã được lưu — mở lại màn Sửa không đổi loại được.\n"
     "► Ô 'Loại đề nghị' trên Phiếu xuất giữ luôn bị khóa, lấy theo phiếu yêu cầu cha.\n"
     "► Bộ lọc Trạng thái của màn 'Danh sách phiếu xuất giữ' chỉ có hai lựa chọn 'Đã duyệt' và "
     "'Chờ duyệt' — không có lựa chọn để lọc riêng phiếu nháp."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Ô 'Từ ngày' và 'Đến ngày' trên cả hai màn danh sách lọc theo NGÀY LẬP phiếu.\n"
     "Cả hai đầu đều lấy trọn ngày được chọn (phiếu lập buổi chiều của ngày cuối vẫn phải lọt).\n"
     "Ô 'Giữ đến ngày' KHÔNG phải bộ lọc — đó là hạn giữ hàng, nằm trong phiếu.\n"
     "Khi bấm In hoặc Xuất excel danh sách, khoảng ngày đang lọc được in thành dòng "
     "'Từ ngày … đến ngày …' ở đầu bản in."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Một phiếu yêu cầu xuất giữ gồm phần Thông tin chung (Loại yêu cầu, Hợp đồng hoặc Khách hàng, "
     "Phòng ban yêu cầu, Giữ đến ngày, Ghi chú, File đính kèm) và nhiều dòng hàng hóa.\n"
     "Có 6 loại yêu cầu, chia làm hai kiểu form khác hẳn nhau:\n"
     "• 'Xuất giữ thường' · 'Xuất giữ khuyến mại' · 'Xuất giữ HĐDV' · 'Xuất giữ HĐDA' · "
     "'Xuất giữ HĐ hãng' — bắt buộc chọn một hợp đồng, hàng tự nạp theo hợp đồng.\n"
     "• 'Xuất giữ khác' — không có hợp đồng; bắt buộc chọn Khách hàng, nhập Ghi chú và đính kèm ít "
     "nhất một file; hàng hóa thêm tay từng dòng và tự chọn Đơn vị tính.\n"
     "Một phiếu yêu cầu sinh ra TỐI ĐA MỘT phiếu xuất giữ. Phiếu xuất giữ chép lại danh sách hàng của "
     "phiếu yêu cầu; kế toán được sửa 'SL đề nghị' và bỏ tích 'Cần xuất' từng dòng.\n"
     "Khi phiếu xuất giữ được duyệt, mỗi dòng hàng sinh ra một lô hàng giữ. Một lô hàng giữ được xác "
     "định bởi: nhân viên giữ + khách hàng + hàng hóa + hạn giữ. Trùng đủ bốn yếu tố thì cộng dồn vào "
     "lô cũ, không tạo lô mới."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "► Người đứng tên giữ hàng là NGƯỜI LẬP PHIẾU YÊU CẦU, không phải kế toán lập phiếu xuất giữ. "
     "Đây là điểm sai nhiều nhất khi đối chiếu với màn 'Danh sách hàng giữ'.\n"
     "► Hạn giữ của lô hàng lấy theo ô 'Giữ đến ngày' trên PHIẾU XUẤT GIỮ tại thời điểm duyệt — Ban "
     "giám đốc và kế toán đều được sửa lại ô này, nên nó có thể khác ngày người lập xin ban đầu.\n"
     "► Số lượng ghi vào kho hàng giữ được quy về đơn vị tính gốc của hàng hóa: nhập 2 với đơn vị "
     "'Thùng (x10)' thì kho hàng giữ ghi 20.\n"
     "► Dòng bị bỏ tích 'Cần xuất' hoặc có SL đề nghị bằng 0 thì KHÔNG sinh lô hàng giữ nào.\n"
     "► Không thể duyệt hai lần cho cùng một phiếu yêu cầu — sau lần duyệt đầu, phiếu yêu cầu đã sang "
     "'Đã duyệt' và không lập được phiếu xuất giữ thứ hai."),

    ("7. Phân quyền cấp",
     "• Xem phiếu hàng giữ theo tổng công ty — thấy phiếu của mọi công ty.\n"
     "• Xem phiếu hàng giữ theo công ty — thấy phiếu trong công ty mình.\n"
     "• Xem phiếu hàng giữ theo phòng ban — thấy phiếu của các phòng ban mình quản lý.\n"
     "• Không có ba quyền trên — chỉ thấy phiếu do chính mình lập.\n"
     "• Trưởng phòng duyệt hàng giữ — duyệt phiếu 'Chờ TP duyệt' của phòng ban mình quản lý, cùng "
     "công ty với mình.\n"
     "• Ban giám đốc duyệt hàng giữ — duyệt phiếu 'Chờ BGĐ duyệt' trong công ty mình.\n"
     "• Kế toán duyệt hàng giữ — nhìn thấy phiếu 'Chờ KT duyệt' và được bấm 'Tạo phiếu xuất giữ'.\n"
     "• Trưởng phòng kế toán — điều kiện BẮT BUỘC để nhìn thấy phiếu của người khác trên màn "
     "'Danh sách phiếu xuất giữ'.\n"
     "• Quản lý giữ hàng — quyền phụ, cho phép mở xem chi tiết phiếu yêu cầu."),

    ("8. Cách tính các ô thống kê",
     "► Cột 'Có thể giữ' (màn yêu cầu) và 'SL có thể giữ' (màn phiếu xuất giữ) = số hàng còn trong "
     "KHO có thể đem giữ, đã trừ phần đang nằm ở các phiếu chờ xử lý; đổi Đơn vị tính thì số này được "
     "quy đổi lại theo hệ số của đơn vị vừa chọn.\n"
     "► Cột 'Hợp đồng' = số lượng ghi trên hợp đồng. Cột 'Đã xuất kho' = số đã giao cho khách. Loại "
     "'Xuất giữ HĐDV' ẩn hai cột này.\n"
     "► Kiểm tra khi lưu phiếu yêu cầu: 'Đề nghị' không được vượt quá (số lượng Hợp đồng trừ Đã xuất "
     "kho). Riêng hợp đồng nguyên tắc thì bỏ qua kiểm tra này; loại 'Xuất giữ khác' cũng không kiểm "
     "tra.\n"
     "► Kiểm tra khi kế toán bấm 'Duyệt giữ hàng': tồn kho còn lại (đã trừ hàng khuyến mại) phải lớn "
     "hơn hoặc bằng số đề nghị đã quy đổi. Lưu nháp thì bỏ qua kiểm tra này.\n"
     "► Hạn giữ tối đa: 'Giữ đến ngày' không được vượt quá ngày hôm nay cộng số ngày giữ tối đa khai "
     "trong Cấu hình hệ thống; riêng loại 'Xuất giữ HĐDA' dùng cấu hình số ngày giữ riêng cho hợp "
     "đồng dự án.\n"
     "► Điều kiện phiếu phải qua Ban giám đốc (thay vì Trưởng phòng duyệt xong đi thẳng xuống Kế "
     "toán): với 5 loại có hợp đồng — số tiền khách đã thanh toán cho hợp đồng đó chiếm tỉ lệ nhỏ hơn "
     "'% đặt cọc' khai cho loại hợp đồng đó trong Quy chế công ty; với loại 'Xuất giữ khác' — tổng "
     "giá trị hàng xin giữ vượt quá 'Giá trị giữ hàng khác' khai trong Quy chế công ty."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất của cặp màn này — đọc trước khi test:\n"
     "① Không duyệt ở BẤT KỲ cấp nào đều đưa phiếu yêu cầu VỀ 'Đang tạo' kèm ghi chú, chứ không có "
     "trạng thái 'Từ chối' riêng. Người lập sửa lại rồi gửi tiếp.\n"
     "② Kế toán KHÔNG có nút 'Duyệt' trên phiếu yêu cầu — thay vào đó là nút 'Tạo phiếu xuất giữ'. "
     "Phiếu yêu cầu chỉ sang 'Đã duyệt' khi phiếu xuất giữ được duyệt.\n"
     "③ Kế toán bấm 'Lưu' ở màn tạo phiếu xuất giữ là LƯU NHÁP: phiếu yêu cầu cha chuyển sang "
     "'Đang xuất giữ' và kho hàng giữ CHƯA thay đổi gì.\n"
     "④ Ở màn tạo phiếu xuất giữ, nút 'Không duyệt' hiện đang làm đúng việc mà nút 'Lưu' làm — lưu "
     "bản nháp — chứ không trả phiếu về cho người lập. Ghi nhận đúng hiện tượng thấy được.\n"
     "⑤ Nút 'Duyệt' và 'Không duyệt' trên màn XEM phiếu xuất giữ thuộc luồng Ban kiểm soát đã bị tắt "
     "trong hệ thống — thực tế không bao giờ hiện.\n"
     "⑥ Nút 'Xuất excel' ở màn 'Danh sách phiếu xuất giữ' hiện đang lỗi, bấm vào ra trang báo lỗi. "
     "Lỗi đã biết, vẫn phải ghi nhận.\n"
     "⑦ Bản in một phiếu yêu cầu CHƯA duyệt vẫn in ra ngày hôm nay ở ô Ngày duyệt. Lỗi đã biết.\n"
     "⑧ Phiếu bị trả về sửa lại vẫn còn hiện tên người duyệt của cấp trước ở màn xem chi tiết. Lỗi "
     "đã biết.\n"
     "⑨ Màu trạng thái không theo quy ước: 'Đang tạo', 'Chờ BGĐ duyệt', 'Chờ KT duyệt', "
     "'Đang xuất giữ' đều hiển thị màu ĐỎ; chỉ 'Chờ TP duyệt' màu cam và 'Đã duyệt' màu xanh.\n"
     "⑩ Người lập đang còn hàng giữ / hàng mượn / hàng nhập thẳng quá hạn có thể bị chặn tạo phiếu "
     "mới, tùy cấu hình chặn quá hạn của công ty. Nếu bị chặn, hệ thống báo ngay khi mở màn tạo.\n"
     "⑪ Nhóm test 'gọi thẳng chức năng, bỏ qua giao diện' dành cho tester kỹ thuật, dùng công cụ "
     "kiểm thử để kiểm tra hệ thống có chặn đúng khi người dùng không có quyền."),
]

# =========================================================================
# SECTION PHAN QUYEN
# =========================================================================
ROLE_TCS = [
    ("00", "Người dùng không có quyền xem mở rộng chỉ thấy phiếu yêu cầu của mình", "P0",
     "Tài khoản A thuộc công ty 1, không có quyền xem theo phòng ban / công ty / tổng công ty. "
     "Có 3 phiếu yêu cầu do A lập, 5 phiếu do người khác cùng phòng lập",
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Vào menu Khởi tạo → Hàng hóa → Giữ hàng → 'Phiếu Yêu cầu xuất giữ'\n"
     "3. Đếm số dòng trên lưới",
     "Tài khoản: A (không quyền mở rộng)",
     "- Lưới chỉ hiện 3 phiếu do A lập\n"
     "- Không có ô lọc Công ty và ô lọc Phòng ban trên thanh tìm kiếm"),

    ("01", "Quyền 'Xem phiếu hàng giữ theo phòng ban'", "P0",
     "Tài khoản B có quyền 'Xem phiếu hàng giữ theo phòng ban', được phân quản lý phòng Kinh doanh 1. "
     "Có 4 phiếu của phòng Kinh doanh 1, 6 phiếu của phòng Kinh doanh 2 (không tính phiếu Đang tạo)",
     "1. Đăng nhập bằng tài khoản B\n2. Vào màn 'Danh sách yêu cầu xuất giữ'\n"
     "3. Quan sát phạm vi dữ liệu",
     "Tài khoản: B (quản lý phòng Kinh doanh 1)",
     "- Hiện đúng 4 phiếu của phòng Kinh doanh 1\n- Không hiện phiếu của phòng Kinh doanh 2\n"
     "- Thanh tìm kiếm có thêm ô lọc Phòng ban"),

    ("02", "Quyền 'Xem phiếu hàng giữ theo công ty'", "P0",
     "Tài khoản C có quyền 'Xem phiếu hàng giữ theo công ty', thuộc công ty 1. Công ty 1 có 12 phiếu "
     "yêu cầu không ở trạng thái Đang tạo",
     "1. Đăng nhập bằng tài khoản C\n2. Vào màn 'Danh sách yêu cầu xuất giữ'\n3. Đếm số phiếu",
     "Tài khoản: C (công ty 1)",
     "- Hiện đủ 12 phiếu của công ty 1, không phân biệt phòng ban\n"
     "- Không hiện phiếu của công ty khác"),

    ("03", "Quyền 'Xem phiếu hàng giữ theo tổng công ty'", "P0",
     "Tài khoản D có quyền 'Xem phiếu hàng giữ theo tổng công ty'. Công ty 1 có 12 phiếu, công ty 4 "
     "có 9 phiếu",
     "1. Đăng nhập bằng tài khoản D\n2. Vào màn 'Danh sách yêu cầu xuất giữ'\n3. Đếm số phiếu",
     "Tài khoản: D (tổng công ty)",
     "- Hiện đủ 21 phiếu của cả hai công ty\n"
     "- Thanh tìm kiếm có cả ô lọc Công ty và ô lọc Phòng ban"),

    ("04", "Phiếu 'Đang tạo' của người khác bị ẩn với mọi cấp quyền", "P0",
     "Tài khoản A có 1 phiếu yêu cầu ở trạng thái 'Đang tạo'. Tài khoản D có quyền xem theo tổng "
     "công ty",
     "1. Đăng nhập tài khoản D\n2. Vào màn danh sách\n3. Lọc Trạng thái = 'Đang tạo'",
     "Phiếu Đang tạo của A",
     "- Lưới không có phiếu 'Đang tạo' của A\n"
     "- Đăng nhập lại bằng A thì phiếu này hiện bình thường"),

    ("05", "Quyền 'Trưởng phòng duyệt hàng giữ'", "P0",
     "Tài khoản E có quyền 'Trưởng phòng duyệt hàng giữ', quản lý phòng Kinh doanh 1, công ty 1. "
     "Có 3 phiếu 'Chờ TP duyệt' của phòng Kinh doanh 1 và 2 phiếu 'Chờ TP duyệt' của phòng Kinh doanh 2",
     "1. Đăng nhập tài khoản E\n"
     "2. Vào menu Chờ duyệt → Hàng giữ → 'Phiếu yêu cầu xuất giữ chờ duyệt'\n"
     "3. Đếm số phiếu",
     "Tài khoản: E (Trưởng phòng KD1)",
     "- Hiện đúng 3 phiếu của phòng Kinh doanh 1\n"
     "- Không hiện phiếu của phòng Kinh doanh 2\n"
     "- Mở một phiếu ra thấy nút 'TP duyệt' và nút 'Không duyệt'"),

    ("06", "Quyền 'Ban giám đốc duyệt hàng giữ'", "P0",
     "Tài khoản F có quyền 'Ban giám đốc duyệt hàng giữ', công ty 1. Có 3 phiếu 'Chờ BGĐ duyệt' ở "
     "công ty 1, 2 phiếu 'Chờ TP duyệt'",
     "1. Đăng nhập tài khoản F\n2. Vào màn 'Phiếu yêu cầu xuất giữ chờ duyệt'\n3. Đếm số phiếu",
     "Tài khoản: F (Ban giám đốc công ty 1)",
     "- Hiện đúng 3 phiếu 'Chờ BGĐ duyệt'\n- Không hiện phiếu 'Chờ TP duyệt'\n"
     "- Mở một phiếu ra thấy nút 'BGĐ duyệt' và nút 'Không duyệt'"),

    ("07", "Quyền 'Kế toán duyệt hàng giữ'", "P0",
     "Tài khoản G có quyền 'Kế toán duyệt hàng giữ', công ty 1. Có 4 phiếu 'Chờ KT duyệt', 1 phiếu "
     "'Đã duyệt', 1 phiếu 'Đang xuất giữ'",
     "1. Đăng nhập tài khoản G\n2. Vào màn 'Phiếu yêu cầu xuất giữ chờ duyệt'\n3. Đếm số phiếu",
     "Tài khoản: G (Kế toán công ty 1)",
     "- Hiện đúng 4 phiếu 'Chờ KT duyệt'\n"
     "- Mở một phiếu ra thấy nút 'Tạo phiếu xuất giữ', KHÔNG có nút 'Duyệt'"),

    ("08", "Người kiêm nhiều quyền duyệt thấy gộp các nhóm phiếu", "P1",
     "Tài khoản H vừa có 'Trưởng phòng duyệt hàng giữ' (quản lý phòng KD1) vừa có 'Ban giám đốc duyệt "
     "hàng giữ'. Có 2 phiếu 'Chờ TP duyệt' của KD1 và 3 phiếu 'Chờ BGĐ duyệt'",
     "1. Đăng nhập tài khoản H\n2. Vào màn 'Phiếu yêu cầu xuất giữ chờ duyệt'\n3. Đếm số phiếu",
     "Tài khoản: H (kiêm 2 vai trò duyệt)",
     "- Hiện đủ 5 phiếu\n- Mở phiếu 'Chờ TP duyệt' thấy nút 'TP duyệt'; mở phiếu 'Chờ BGĐ duyệt' "
     "thấy nút 'BGĐ duyệt'"),

    ("09", "Trưởng phòng khác công ty không duyệt được", "P0",
     "Tài khoản I có quyền 'Trưởng phòng duyệt hàng giữ', quản lý phòng Kinh doanh 1 của công ty 4. "
     "Phiếu P thuộc phòng Kinh doanh 1 của công ty 1, đang 'Chờ TP duyệt'",
     "1. Đăng nhập tài khoản I\n2. Vào màn chờ duyệt\n3. Tìm phiếu P",
     "Phiếu P — công ty 1",
     "- Phiếu P không nằm trong danh sách chờ duyệt của I\n"
     "- Mở phiếu P bằng liên kết trực tiếp cũng không có nút 'TP duyệt'"),

    ("10", "Không có quyền 'Trưởng phòng kế toán' thì màn Phiếu xuất giữ chỉ thấy phiếu của mình", "P0",
     "Tài khoản G có 'Kế toán duyệt hàng giữ' và 'Xem phiếu hàng giữ theo công ty' nhưng KHÔNG có "
     "'Trưởng phòng kế toán'. Công ty 1 có 30 phiếu xuất giữ, trong đó 4 phiếu do G lập",
     "1. Đăng nhập tài khoản G\n"
     "2. Vào menu Kế toán → Hàng hóa - Dịch vụ - Vận chuyển → Giữ hàng → 'Phiếu xuất giữ'\n"
     "3. Đếm số phiếu",
     "Tài khoản: G (thiếu quyền Trưởng phòng kế toán)",
     "⚠️ Chỉ hiện 4 phiếu do G lập, KHÔNG phải 30 — đây là hành vi đúng của hệ thống, không phải lỗi "
     "mất dữ liệu\n"
     "- Cấp thêm quyền 'Trưởng phòng kế toán' rồi tải lại thì hiện đủ 30 phiếu"),

    ("11", "Người không có quyền nào của nhóm giữ hàng không vào được màn danh sách", "P0",
     "Tài khoản J không có bất kỳ quyền nào thuộc nhóm hàng giữ",
     "1. Đăng nhập tài khoản J\n2. Mở menu Khởi tạo → Hàng hóa\n"
     "3. Thử mở màn 'Danh sách yêu cầu xuất giữ' bằng liên kết trực tiếp",
     "Tài khoản: J (không quyền)",
     "- Menu không hiện mục 'Phiếu Yêu cầu xuất giữ'\n"
     "- Vào bằng liên kết trực tiếp thì hệ thống từ chối, báo không có quyền"),

    ("12", "Quyền 'Quản lý giữ hàng' mở được màn xem chi tiết phiếu yêu cầu", "P1",
     "Tài khoản K chỉ có quyền 'Quản lý giữ hàng'. Phiếu P đang 'Chờ TP duyệt', do người khác lập",
     "1. Đăng nhập tài khoản K\n2. Mở màn xem phiếu P bằng liên kết trực tiếp\n3. Ghi nhận kết quả",
     "Phiếu P — người khác lập",
     "⚠️ Ghi nhận CHÍNH XÁC kết quả thực tế: màn xem chi tiết hiện nội dung phiếu\n"
     "- Không có nút duyệt / sửa / xóa nào\n"
     "- Phiếu P vẫn KHÔNG xuất hiện trên lưới danh sách của K"),

    ("13", "Gọi thẳng chức năng duyệt khi không có quyền", "P0",
     "Phiếu P đang 'Chờ TP duyệt'. Tài khoản A không có quyền duyệt nào",
     "1. Đăng nhập tài khoản A\n"
     "2. Dùng công cụ kiểm thử gọi thẳng chức năng 'TP duyệt' cho phiếu P, bỏ qua giao diện\n"
     "3. Kiểm tra lại trạng thái phiếu P",
     "Phiếu P — Chờ TP duyệt",
     "- Hệ thống từ chối, báo 'Không có quyền'\n- Phiếu P vẫn ở 'Chờ TP duyệt'"),

    ("14", "Gọi thẳng chức năng xóa phiếu của người khác", "P0",
     "Phiếu P ở trạng thái 'Đang tạo' do tài khoản A lập. Tài khoản C là người khác",
     "1. Đăng nhập tài khoản C\n"
     "2. Dùng công cụ kiểm thử gọi thẳng chức năng Xóa cho phiếu P, bỏ qua giao diện\n"
     "3. Đăng nhập lại tài khoản A kiểm tra",
     "Phiếu P của A",
     "- Hệ thống từ chối thao tác\n- Phiếu P vẫn còn nguyên trong danh sách của A"),

    ("15", "Gọi thẳng chức năng duyệt giữ hàng khi không phải người lập phiếu xuất giữ", "P0",
     "Phiếu xuất giữ X đang là bản nháp 'Đang tạo' do kế toán G lập. Tài khoản C là người khác",
     "1. Đăng nhập tài khoản C\n"
     "2. Dùng công cụ kiểm thử gọi thẳng chức năng cập nhật phiếu X với trạng thái duyệt\n"
     "3. Kiểm tra kho hàng giữ",
     "Phiếu xuất giữ X của G",
     "- Hệ thống từ chối, báo 'Không đủ quyền!'\n- Không có lô hàng giữ nào được sinh ra"),
]

# =========================================================================
# SECTIONS NGHIEP VU
# =========================================================================
SECTIONS = [
    # ------------------------------------------------------------------ I
    ("I", "YÊU CẦU XUẤT GIỮ - HIỂN THỊ TRANG & TRUY CẬP", [
        ("001", "Vào màn danh sách từ menu Khởi tạo", "P0",
         "Tài khoản A đã đăng nhập, có ít nhất 1 phiếu",
         "1. Bấm menu Khởi tạo\n2. Bấm Hàng hóa → nhóm Giữ hàng\n"
         "3. Bấm 'Phiếu Yêu cầu xuất giữ'",
         "Tài khoản: A",
         "- Trang mở với tiêu đề 'Danh sách yêu cầu xuất giữ'\n"
         "- Lưới có đủ 10 cột: STT · Mã phiếu · Loại yêu cầu · Người lập · Ngày lập · Hợp đồng · "
         "Trạng thái · Người duyệt · Ngày duyệt · Hành động\n"
         "- Có nút 'Tạo mới', nút 'In' và nút 'Xuất excel' phía trên lưới"),

        ("002", "Vào màn danh sách từ menu Kế toán", "P2",
         "Tài khoản G đã đăng nhập",
         "1. Bấm menu Kế toán\n2. Bấm Hàng hóa - Dịch vụ - Vận chuyển → nhóm Giữ hàng\n"
         "3. Bấm 'Yêu cầu xuất giữ'",
         "Tài khoản: G",
         "- Mở đúng màn 'Danh sách yêu cầu xuất giữ' với đủ 10 cột như lối vào từ menu Khởi tạo"),

        ("003", "Vào màn chờ duyệt từ menu Chờ duyệt", "P0",
         "Tài khoản E có quyền 'Trưởng phòng duyệt hàng giữ', có 3 phiếu chờ mình duyệt",
         "1. Bấm menu Chờ duyệt\n2. Bấm nhóm Hàng giữ\n"
         "3. Bấm 'Phiếu yêu cầu xuất giữ chờ duyệt'",
         "Tài khoản: E",
         "- Lưới chỉ hiện phiếu đang chờ chính E duyệt\n"
         "- Không có nút 'Tạo mới' ở màn này"),

        ("004", "Cột Mã phiếu là liên kết mở màn xem", "P1",
         "Có ít nhất 1 phiếu không ở trạng thái 'Đang tạo' trên lưới",
         "1. Bấm vào mã phiếu ở cột 'Mã phiếu'\n2. Quan sát",
         "Một phiếu bất kỳ",
         "- Mở màn xem chi tiết của đúng phiếu đó\n"
         "- Màn xem có 3 khối: Thông tin chung · Chi tiết · Ghi chú duyệt (khi phiếu có ghi chú)"),

        ("005", "Menu Hành động của phiếu 'Đang tạo' do chính mình lập", "P0",
         "Tài khoản A có phiếu P ở trạng thái 'Đang tạo'",
         "1. Đăng nhập A\n2. Vào màn danh sách\n3. Bấm nút bánh răng ở cột Hành động của phiếu P",
         "Phiếu P — Đang tạo",
         "- Menu có: 'Sửa yêu cầu' · 'Xóa' · 'In yêu cầu'\n"
         "- Không có 'Tạo phiếu xuất giữ', không có 'Duyệt'"),

        ("006", "Menu Hành động của phiếu 'Chờ TP duyệt' với người lập", "P0",
         "Tài khoản A có phiếu P ở trạng thái 'Chờ TP duyệt'",
         "1. Đăng nhập A\n2. Bấm nút bánh răng của phiếu P",
         "Phiếu P — Chờ TP duyệt",
         "- Menu CHỈ có 'In yêu cầu'\n- Không có 'Sửa yêu cầu', không có 'Xóa'"),

        ("007", "Menu Hành động của phiếu 'Chờ TP duyệt' với Trưởng phòng", "P0",
         "Tài khoản E là Trưởng phòng quản lý phòng của người lập phiếu P",
         "1. Đăng nhập E\n2. Bấm nút bánh răng của phiếu P",
         "Phiếu P — Chờ TP duyệt",
         "- Menu có 'Duyệt' và 'In yêu cầu'\n- Bấm 'Duyệt' mở màn xem chi tiết phiếu"),

        ("008", "Menu Hành động của phiếu 'Chờ KT duyệt' với Kế toán", "P0",
         "Tài khoản G là Kế toán duyệt hàng giữ, phiếu P đang 'Chờ KT duyệt'",
         "1. Đăng nhập G\n2. Bấm nút bánh răng của phiếu P",
         "Phiếu P — Chờ KT duyệt",
         "- Menu có 'Tạo phiếu xuất giữ' và 'In yêu cầu'\n"
         "- Bấm 'Tạo phiếu xuất giữ' mở màn 'Tạo phiếu xuất giữ' đã điền sẵn phiếu yêu cầu P"),

        ("009", "Nút trên màn xem chi tiết khớp với menu Hành động", "P0",
         "Lần lượt xem một phiếu ở mỗi trạng thái với đúng tài khoản có quyền tương ứng",
         "1. Mở màn xem chi tiết\n2. Đối chiếu các nút cuối trang với menu Hành động ngoài lưới",
         "6 trạng thái × các vai trò",
         "- Trưởng phòng: thấy 'Không duyệt' + 'TP duyệt' + 'Quay lại'\n"
         "- Ban giám đốc: thấy 'Không duyệt' + 'BGĐ duyệt' + 'Quay lại'\n"
         "- Kế toán: thấy 'Không duyệt' + 'Tạo phiếu xuất giữ' + 'Quay lại'\n"
         "- Người lập xem phiếu của mình: chỉ thấy 'Quay lại'"),

        ("010", "Màu và nhãn của 6 trạng thái", "P1",
         "Có sẵn phiếu ở đủ 6 trạng thái",
         "1. Vào màn danh sách\n2. Quan sát cột Trạng thái",
         "Đang tạo · Chờ TP duyệt · Chờ BGĐ duyệt · Chờ KT duyệt · Đang xuất giữ · Đã duyệt",
         "- Nhãn hiển thị đúng 6 tên trên\n"
         "⚠️ Ghi nhận thực tế: 'Đã duyệt' màu xanh, 'Chờ TP duyệt' màu cam, bốn trạng thái còn lại "
         "đều màu ĐỎ — không phân biệt được nháp với chờ duyệt"),

        ("011", "Cột Hợp đồng của phiếu loại 'Xuất giữ khác'", "P1",
         "Có phiếu loại 'Xuất giữ khác' trên lưới",
         "1. Vào màn danh sách\n2. Tìm phiếu loại 'Xuất giữ khác'\n3. Xem cột Hợp đồng",
         "Phiếu loại Xuất giữ khác",
         "- Cột Hợp đồng để trống vì loại này không gắn hợp đồng nào"),

        ("012", "Cột Người duyệt và Ngày duyệt của phiếu chưa duyệt xong", "P1",
         "Phiếu P đang 'Chờ BGĐ duyệt', đã qua Trưởng phòng",
         "1. Vào màn danh sách\n2. Xem cột Người duyệt và Ngày duyệt của phiếu P",
         "Phiếu P — Chờ BGĐ duyệt",
         "- Hai cột để trống vì phiếu chưa duyệt xong toàn bộ"),

        ("013", "Mở màn xem phiếu 'Đang tạo' của người khác", "P0",
         "Phiếu P của tài khoản A đang ở 'Đang tạo'. Tài khoản C có quyền xem theo công ty",
         "1. Đăng nhập C\n2. Mở màn xem phiếu P bằng liên kết trực tiếp\n3. Ghi nhận kết quả",
         "Phiếu P — Đang tạo",
         "- Hệ thống từ chối, báo không có quyền xem\n"
         "- Phiếu P cũng không có trên lưới của C"),
    ]),

    # ------------------------------------------------------------------ II
    ("II", "YÊU CẦU XUẤT GIỮ - BỘ LỌC & TÌM KIẾM", [
        ("001", "Lọc theo Mã phiếu", "P0",
         "Biết trước mã một phiếu trên lưới",
         "1. Gõ đầy đủ mã phiếu vào ô 'Mã phiếu'\n2. Chờ lưới tải lại",
         "Mã phiếu đầy đủ",
         "- Lưới chỉ còn đúng 1 phiếu có mã đó"),

        ("002", "Lọc theo Mã phiếu bằng một đoạn mã", "P1",
         "Có nhiều phiếu cùng tiền tố mã",
         "1. Gõ vài ký tự giữa của mã phiếu\n2. Chờ lưới tải lại",
         "Đoạn giữa của mã",
         "- Lưới hiện tất cả phiếu có mã chứa đoạn vừa gõ"),

        ("003", "Lọc theo Người lập", "P0",
         "Nhân viên A có 3 phiếu, nhân viên khác có 5 phiếu",
         "1. Chọn nhân viên A ở ô 'Người lập'\n2. Chờ lưới tải lại",
         "Người lập: A",
         "- Lưới hiện đúng 3 phiếu của A\n- Cột Người lập toàn bộ là A"),

        ("004", "Lọc theo Trạng thái", "P0",
         "Có phiếu ở nhiều trạng thái khác nhau",
         "1. Chọn 'Chờ TP duyệt' ở ô Trạng thái\n2. Chờ lưới tải lại",
         "Trạng thái: Chờ TP duyệt",
         "- Lưới chỉ còn phiếu 'Chờ TP duyệt'"),

        ("005", "Lọc theo Loại yêu cầu", "P0",
         "Có phiếu thuộc nhiều loại khác nhau",
         "1. Chọn 'Xuất giữ HĐ hãng' ở ô 'Loại yêu cầu'\n2. Chờ lưới tải lại",
         "Loại: Xuất giữ HĐ hãng",
         "- Lưới chỉ còn phiếu loại 'Xuất giữ HĐ hãng'\n"
         "- Ô lọc có đủ 6 lựa chọn: Xuất giữ thường · Xuất giữ khuyến mại · Xuất giữ HĐDV · "
         "Xuất giữ HĐDA · Xuất giữ HĐ hãng · Xuất giữ khác"),

        ("006", "Lọc theo Hợp đồng", "P1",
         "Biết trước số hợp đồng gắn với một phiếu",
         "1. Gõ số hợp đồng vào ô 'Hợp đồng'\n2. Chờ lưới tải lại",
         "Số hợp đồng",
         "- Lưới chỉ còn phiếu gắn hợp đồng đó"),

        ("007", "Lọc theo Người duyệt", "P1",
         "Có phiếu đã duyệt xong bởi nhiều người khác nhau",
         "1. Chọn một nhân viên ở ô 'Người duyệt'\n2. Chờ lưới tải lại",
         "Người duyệt",
         "- Lưới chỉ còn phiếu do người đó duyệt"),

        ("008", "Lọc theo Tên, mã hàng hóa", "P0",
         "Hàng X nằm trong 2 phiếu, hàng Y nằm trong 3 phiếu khác",
         "1. Gõ tên hàng X vào ô 'Tên, mã hàng hóa'\n2. Chờ lưới tải lại",
         "Tên hàng X",
         "- Lưới hiện đúng 2 phiếu có chứa hàng X\n"
         "- Gõ mã hàng của X cho kết quả giống hệt"),

        ("009", "Lọc theo khoảng ngày lập", "P0",
         "Có phiếu lập rải trong tháng, biết trước số phiếu trong khoảng cần lọc",
         "1. Chọn 'Từ ngày' 01/03/2026 và 'Đến ngày' 10/03/2026\n2. Chờ lưới tải lại",
         "01/03/2026 → 10/03/2026",
         "- Chỉ hiện phiếu có Ngày lập nằm trong khoảng, tính trọn cả hai ngày đầu và cuối"),

        ("010", "Phiếu lập buổi chiều của ngày cuối khoảng lọc", "P0",
         "Phiếu P lập lúc 17:30 ngày 10/03/2026",
         "1. Lọc 'Từ ngày' 01/03/2026 'Đến ngày' 10/03/2026\n2. Tìm phiếu P",
         "Phiếu lập 17:30 ngày cuối",
         "- Phiếu P PHẢI có trong kết quả"),

        ("011", "Lọc theo Công ty", "P0",
         "Tài khoản D có quyền xem theo tổng công ty; công ty 1 có 12 phiếu, công ty 4 có 9 phiếu",
         "1. Đăng nhập D\n2. Chọn công ty 4 ở ô lọc Công ty\n3. Chờ lưới tải lại",
         "Công ty 4",
         "- Lưới hiện đúng 9 phiếu của công ty 4"),

        ("012", "Lọc theo Phòng ban", "P1",
         "Tài khoản D chọn sẵn công ty 1; phòng Kinh doanh 1 có 4 phiếu",
         "1. Chọn phòng Kinh doanh 1 ở ô lọc Phòng ban\n2. Chờ lưới tải lại",
         "Phòng Kinh doanh 1",
         "- Lưới hiện đúng 4 phiếu của phòng Kinh doanh 1"),

        ("013", "Kết hợp nhiều bộ lọc", "P0",
         "Có dữ liệu đủ đa dạng để giao nhau",
         "1. Chọn Trạng thái 'Chờ KT duyệt'\n2. Chọn thêm Loại yêu cầu 'Xuất giữ khác'\n"
         "3. Chọn thêm khoảng ngày lập\n4. Chờ lưới tải lại",
         "3 điều kiện cùng lúc",
         "- Kết quả thỏa ĐỒNG THỜI cả 3 điều kiện\n- Không có phiếu nào chỉ thỏa một điều kiện"),

        ("014", "Xóa bộ lọc trả lại danh sách đầy đủ", "P1",
         "Đang có bộ lọc làm lưới còn 2 dòng",
         "1. Xóa hết nội dung các ô lọc\n2. Chờ lưới tải lại",
         "Bộ lọc rỗng",
         "- Lưới quay lại đúng số phiếu ban đầu theo phạm vi quyền"),

        ("015", "Lọc không ra kết quả", "P1",
         "Không có phiếu nào khớp",
         "1. Gõ một mã phiếu không tồn tại vào ô 'Mã phiếu'\n2. Chờ lưới tải lại",
         "Mã không tồn tại",
         "- Lưới hiện dòng thông báo không có dữ liệu\n- Không báo lỗi hệ thống"),
    ]),

    # ------------------------------------------------------------------ III
    ("III", "YÊU CẦU XUẤT GIỮ - LẬP PHIẾU LOẠI CÓ HỢP ĐỒNG", [
        ("001", "Mở màn tạo mới", "P0",
         "Tài khoản A có quyền lập phiếu, không bị chặn quá hạn",
         "1. Vào màn 'Danh sách yêu cầu xuất giữ'\n2. Bấm 'Tạo mới'",
         "Tài khoản: A",
         "- Trang mở với tiêu đề 'Tạo phiếu yêu cầu xuất giữ'\n"
         "- Khối 'Thông tin chung' có ô 'Loại yêu cầu' bắt buộc, chưa chọn gì\n"
         "- Khối 'Chi tiết' chưa có bảng hàng hóa\n"
         "- Cuối trang có 3 nút: 'Lưu' · 'Lưu & Gửi duyệt' · 'Hủy'"),

        ("002", "Chọn loại 'Xuất giữ HĐ hãng' hiện đúng ô chọn hợp đồng", "P0",
         "Đang ở màn tạo mới",
         "1. Chọn 'Loại yêu cầu' = 'Xuất giữ HĐ hãng'\n2. Quan sát khối Thông tin chung",
         "Loại: Xuất giữ HĐ hãng",
         "- Hiện ô 'Chọn hợp đồng hãng' có dấu (*) và nút kính lúp\n"
         "- Hiện các dòng thông tin khách hàng còn trống: Mã khách hàng · Khách hàng · Số điện thoại · "
         "Địa chỉ · Địa chỉ giao hàng\n"
         "- Hiện ô 'Phòng ban yêu cầu' đã điền sẵn phòng của người lập và bị khóa\n"
         "- Hiện ô 'Giữ đến ngày' bắt buộc, ô 'Ghi chú' và 'File đính kèm' không bắt buộc"),

        ("003", "Chọn hợp đồng và nạp hàng hóa", "P0",
         "Hợp đồng hãng HĐ01 có 5 dòng hàng",
         "1. Bấm kính lúp ở ô 'Chọn hợp đồng hãng'\n2. Tìm và chọn hợp đồng HĐ01\n"
         "3. Quan sát khối Thông tin chung và khối Chi tiết",
         "Hợp đồng HĐ01 — 5 dòng hàng",
         "- Ô hợp đồng hiện mã HĐ01\n"
         "- Các dòng thông tin khách hàng được điền tự động theo hợp đồng\n"
         "- Bảng Chi tiết hiện đủ 5 dòng hàng của hợp đồng\n"
         "- Bảng có các cột: STT · ô tích 'Cần xuất' · Tên hàng hóa · Model · Mã hàng hóa · "
         "Thương hiệu · nhóm 'Số lượng' gồm Có thể giữ / Hợp đồng / Đã xuất kho / Đề nghị · Đơn giá · "
         "Thành tiền · Đơn vị tính · Hình ảnh tham khảo\n"
         "- Có dòng 'Tổng cộng' cuối bảng"),

        ("004", "Ô tích chọn tất cả trên đầu cột 'Cần xuất'", "P1",
         "Bảng Chi tiết đang có 5 dòng, chưa tích dòng nào",
         "1. Bấm ô tích ở đầu cột 'Cần xuất'\n2. Quan sát\n3. Bấm lại lần nữa",
         "5 dòng hàng",
         "- Lần 1: cả 5 dòng được tích, ô nhập 'Đề nghị' của cả 5 dòng mở khóa\n"
         "- Lần 2: cả 5 dòng bỏ tích, ô nhập 'Đề nghị' bị khóa lại"),

        ("005", "Ô 'Đề nghị' bị khóa khi dòng chưa tích 'Cần xuất'", "P0",
         "Bảng Chi tiết có 5 dòng, chưa tích dòng nào",
         "1. Thử gõ số vào ô 'Đề nghị' của dòng 1\n2. Tích 'Cần xuất' dòng 1 rồi gõ lại",
         "Dòng 1",
         "- Trước khi tích: ô 'Đề nghị' không gõ được, dòng hiển thị mờ\n"
         "- Sau khi tích: gõ được bình thường"),

        ("006", "Cột 'Có thể giữ' hiển thị đúng tồn kho", "P0",
         "Hàng X còn 30 đơn vị có thể đem giữ theo màn Danh sách hàng hóa",
         "1. Chọn hợp đồng có hàng X\n2. Xem cột 'Có thể giữ' của dòng hàng X",
         "Hàng X — tồn 30",
         "- Cột 'Có thể giữ' hiện 30, khớp số liệu tồn kho\n"
         "- Ô để trống nếu hệ thống chưa tính được, KHÔNG hiện 0 thay cho ô trống"),

        ("007", "Cột 'Hợp đồng' và 'Đã xuất kho'", "P0",
         "Hàng X trên hợp đồng HĐ01 có số lượng 20, đã giao khách 8",
         "1. Chọn hợp đồng HĐ01\n2. Xem hai cột 'Hợp đồng' và 'Đã xuất kho' của dòng hàng X",
         "Hàng X: hợp đồng 20 · đã xuất 8",
         "- Cột 'Hợp đồng' hiện 20\n- Cột 'Đã xuất kho' hiện 8"),

        ("008", "Loại 'Xuất giữ HĐDV' ẩn hai cột Hợp đồng và Đã xuất kho", "P1",
         "Có hợp đồng dịch vụ HĐDV01 còn hàng",
         "1. Chọn 'Loại yêu cầu' = 'Xuất giữ HĐDV'\n2. Chọn hợp đồng dịch vụ HĐDV01\n"
         "3. Quan sát bảng Chi tiết",
         "Loại: Xuất giữ HĐDV",
         "- Nhóm 'Số lượng' chỉ còn 2 cột: 'Có thể giữ' và 'Đề nghị'\n"
         "- Không có cột 'Hợp đồng', không có cột 'Đã xuất kho'"),

        ("009", "Dòng 'Tổng cộng' cộng đúng", "P1",
         "Bảng có 3 dòng, Đề nghị lần lượt 2 · 3 · 5; Thành tiền lần lượt 200,000 · 300,000 · 500,000",
         "1. Nhập Đề nghị cho 3 dòng\n2. Xem dòng 'Tổng cộng'",
         "2 + 3 + 5 = 10",
         "- Ô tổng của cột Đề nghị hiện 10\n- Ô tổng của cột Thành tiền hiện 1,000,000"),

        ("010", "Nhập Đề nghị vượt quá số còn lại của hợp đồng", "P0",
         "Hàng X: Hợp đồng 20, Đã xuất kho 8 (còn lại 12)",
         "1. Tích 'Cần xuất' dòng hàng X\n2. Nhập Đề nghị = 15\n3. Bấm 'Lưu'",
         "Đề nghị 15 > còn lại 12",
         "- Hệ thống chặn, báo 'Số lượng xuất không hợp lệ!'\n- Phiếu không được tạo"),

        ("011", "Nhập Đề nghị đúng bằng số còn lại của hợp đồng", "P0",
         "Hàng X: Hợp đồng 20, Đã xuất kho 8 (còn lại 12)",
         "1. Tích 'Cần xuất' dòng hàng X\n2. Nhập Đề nghị = 12\n3. Chọn 'Giữ đến ngày' hợp lệ\n"
         "4. Bấm 'Lưu'",
         "Đề nghị 12 = còn lại 12",
         "- Lưu thành công, hệ thống báo 'Yêu cầu của bạn đã được lưu. Bạn cần gửi để yêu cầu được "
         "xử lý'\n- Phiếu ở trạng thái 'Đang tạo'"),

        ("012", "Lưu nháp bằng nút 'Lưu'", "P0",
         "Đã điền đủ thông tin hợp lệ",
         "1. Bấm 'Lưu'\n2. Vào màn danh sách tìm phiếu vừa tạo",
         "Phiếu hợp lệ",
         "- Báo 'Yêu cầu của bạn đã được lưu. Bạn cần gửi để yêu cầu được xử lý'\n"
         "- Phiếu ở trạng thái 'Đang tạo', mã phiếu được sinh tự động\n"
         "- Trưởng phòng chưa nhìn thấy phiếu này ở màn chờ duyệt"),

        ("013", "Gửi duyệt bằng nút 'Lưu & Gửi duyệt'", "P0",
         "Đã điền đủ thông tin hợp lệ",
         "1. Bấm 'Lưu & Gửi duyệt'\n2. Vào màn danh sách\n"
         "3. Đăng nhập Trưởng phòng E kiểm tra màn chờ duyệt",
         "Phiếu hợp lệ",
         "- Báo 'Yêu cầu của bạn đã được gửi'\n- Phiếu ở trạng thái 'Chờ TP duyệt'\n"
         "- Trưởng phòng E nhìn thấy phiếu ở màn chờ duyệt"),

        ("014", "Không chọn hợp đồng mà bấm Lưu", "P0",
         "Chỉ chọn 'Loại yêu cầu' = 'Xuất giữ HĐ hãng', chưa chọn hợp đồng",
         "1. Bấm 'Lưu'",
         "Thiếu hợp đồng",
         "- Hệ thống báo 'Tạo yêu cầu thất bại!'\n"
         "- Dưới ô chọn hợp đồng hiện dòng chữ đỏ 'Bắt buộc phải chọn'"),

        ("015", "Không nhập 'Giữ đến ngày'", "P0",
         "Đã chọn hợp đồng và tích hàng, để trống 'Giữ đến ngày'",
         "1. Bấm 'Lưu'",
         "Thiếu Giữ đến ngày",
         "- Dưới ô 'Giữ đến ngày' hiện dòng chữ đỏ 'Bắt buộc phải nhập'\n- Phiếu không được tạo"),

        ("016", "Nhập 'Giữ đến ngày' là ngày quá khứ", "P0",
         "Hôm nay 05/03/2026",
         "1. Chọn 'Giữ đến ngày' = 01/03/2026\n2. Bấm 'Lưu'",
         "Ngày quá khứ",
         "- Dưới ô 'Giữ đến ngày' hiện dòng chữ đỏ 'Phải nhập ngày tương lai'"),

        ("017", "Nhập 'Giữ đến ngày' vượt hạn giữ tối đa", "P0",
         "Cấu hình hệ thống cho giữ tối đa 30 ngày, hôm nay 05/03/2026",
         "1. Chọn 'Giữ đến ngày' = 30/06/2026\n2. Bấm 'Lưu'",
         "Vượt 30 ngày",
         "- Hệ thống báo 'Không thể giữ quá 04/04/2026'\n- Phiếu không được tạo"),

        ("018", "Không tích dòng hàng nào", "P0",
         "Đã chọn hợp đồng, chưa tích 'Cần xuất' dòng nào",
         "1. Chọn 'Giữ đến ngày' hợp lệ\n2. Bấm 'Lưu'",
         "0 dòng được tích",
         "- Hệ thống chặn, báo 'SL đề nghị tất cả = 0. Không hợp lệ!'"),

        ("019", "Tích dòng hàng nhưng để Đề nghị bằng 0", "P0",
         "Đã tích 2 dòng, cả hai nhập 0",
         "1. Bấm 'Lưu'",
         "Đề nghị = 0 ở mọi dòng",
         "- Hệ thống chặn, báo 'SL đề nghị tất cả = 0. Không hợp lệ!'"),

        ("020", "Một dòng có số, một dòng để 0", "P1",
         "Dòng 1 nhập Đề nghị 5, dòng 2 tích nhưng để 0",
         "1. Bấm 'Lưu'\n2. Mở lại phiếu vừa tạo",
         "Dòng 1: 5 · dòng 2: 0",
         "- Lưu thành công\n- Phiếu chỉ có tác dụng với dòng 1; dòng có số lượng 0 không được xuất giữ"),

        ("021", "Chọn hợp đồng chưa đủ điều kiện xuất giữ", "P0",
         "Hợp đồng HĐ02 chưa đủ điều kiện xuất giữ theo quy định (chưa duyệt xong hoặc đã đóng)",
         "1. Chọn hợp đồng HĐ02\n2. Điền đủ thông tin\n3. Bấm 'Lưu'",
         "Hợp đồng HĐ02",
         "- Hệ thống chặn, báo 'Chưa thể xuất giữ cho hợp đồng này!'\n- Phiếu không được tạo"),

        ("022", "Ghi chú vượt quá độ dài cho phép", "P1",
         "Đã điền hợp lệ các ô khác",
         "1. Nhập Ghi chú dài hơn 255 ký tự\n2. Bấm 'Lưu'",
         "Ghi chú 300 ký tự",
         "- Dưới ô Ghi chú hiện dòng chữ đỏ 'Không được vượt quá 255 ký tự'"),

        ("023", "Đính kèm file sai định dạng", "P1",
         "Có sẵn file định dạng không được phép",
         "1. Bấm dấu cộng ở 'File đính kèm'\n2. Chọn một file không thuộc danh sách cho phép\n"
         "3. Bấm 'Lưu'",
         "File sai định dạng",
         "- Hệ thống báo 'Chỉ nhận file .pdf, .png, .jpg, .docx, .doc, .xls, .xlsx, .jpeg'"),

        ("024", "Đính kèm file quá dung lượng", "P1",
         "Có sẵn file lớn hơn 13 MB đúng định dạng",
         "1. Đính kèm file đó\n2. Bấm 'Lưu'",
         "File 20 MB",
         "- Hệ thống báo 'File không lớn hơn 13 MB'"),

        ("025", "Đính kèm nhiều file rồi gỡ bớt trước khi lưu", "P2",
         "Đang ở màn tạo",
         "1. Bấm dấu cộng 3 lần, chọn 3 file hợp lệ\n2. Bấm dấu × ở file thứ 2\n3. Bấm 'Lưu'\n"
         "4. Mở lại phiếu",
         "3 file, gỡ 1",
         "- Phiếu lưu đúng 2 file còn lại, mở xem được cả 2"),

        ("026", "Bấm nút 'Hủy' ở màn tạo", "P2",
         "Đang điền dở màn tạo",
         "1. Bấm 'Hủy'",
         "Điền dở",
         "- Quay về màn 'Danh sách yêu cầu xuất giữ'\n- Không có phiếu mới được tạo"),

        ("027", "Nút xóa hợp đồng đã chọn", "P2",
         "Đã chọn hợp đồng loại 'Xuất giữ thường', bảng Chi tiết đã có hàng",
         "1. Bấm nút dấu × cạnh ô hợp đồng\n2. Quan sát",
         "Loại: Xuất giữ thường",
         "- Ô hợp đồng trống trở lại\n- Bảng Chi tiết không còn hàng hóa"),

        ("028", "Người bị chặn do còn hàng quá hạn", "P1",
         "Công ty có bật cấu hình chặn khi còn hàng quá hạn; tài khoản A đang còn hàng nhập thẳng "
         "quá hạn chưa xử lý",
         "1. Đăng nhập A\n2. Bấm 'Tạo mới'\n3. Chọn loại yêu cầu và chọn hợp đồng",
         "Tài khoản A còn hàng quá hạn",
         "- Hệ thống hiện cảnh báo còn hàng quá hạn và không cho lập phiếu tiếp\n"
         "- Xử lý xong hàng quá hạn rồi làm lại thì lập được bình thường"),
    ]),

    # ------------------------------------------------------------------ IV
    ("IV", "YÊU CẦU XUẤT GIỮ - LẬP PHIẾU LOẠI 'XUẤT GIỮ KHÁC'", [
        ("001", "Chọn loại 'Xuất giữ khác' đổi hẳn cấu trúc form", "P0",
         "Đang ở màn tạo mới",
         "1. Chọn 'Loại yêu cầu' = 'Xuất giữ khác'\n2. Quan sát khối Thông tin chung",
         "Loại: Xuất giữ khác",
         "- KHÔNG có ô chọn hợp đồng\n"
         "- Có ô 'Khách hàng' bắt buộc kèm nút kính lúp\n"
         "- Có ô 'Phòng ban yêu cầu' bị khóa, ô 'Giữ đến ngày' bắt buộc\n"
         "- Ô 'Ghi chú' và 'File đính kèm' đều có dấu (*) bắt buộc\n"
         "- Không hiện các dòng thông tin khách hàng lấy từ hợp đồng"),

        ("002", "Bảng Chi tiết của loại 'Xuất giữ khác'", "P0",
         "Đã chọn loại 'Xuất giữ khác'",
         "1. Quan sát bảng Chi tiết",
         "Loại: Xuất giữ khác",
         "- Bảng có các cột: STT · Tên hàng hóa · Model · Mã hàng hóa · Thương hiệu · nhóm "
         "'Số lượng' gồm Có thể giữ / Đề nghị · Đơn vị tính · Đơn giá · Thành tiền · cột nút\n"
         "- KHÔNG có cột tích 'Cần xuất'\n"
         "- Trên đầu cột cuối có nút dấu cộng để thêm hàng\n"
         "- Bảng đang trống, hiện dòng 'Không có hàng hóa'"),

        ("003", "Chọn khách hàng", "P0",
         "Đã chọn loại 'Xuất giữ khác'",
         "1. Bấm kính lúp ở ô 'Khách hàng'\n2. Tìm và chọn khách hàng KH001",
         "Khách hàng KH001",
         "- Ô 'Khách hàng' hiện mã và tên khách hàng vừa chọn, ở dạng chỉ đọc"),

        ("004", "Thêm hàng hóa bằng tay", "P0",
         "Đã chọn khách hàng",
         "1. Bấm dấu cộng trên đầu bảng Chi tiết\n2. Tìm hàng X trong cửa sổ tìm kiếm hàng hóa\n"
         "3. Chọn hàng X",
         "Hàng X",
         "- Bảng thêm 1 dòng hàng X, các cột Tên hàng hóa / Model / Mã hàng hóa / Thương hiệu điền "
         "tự động\n- Cột 'Có thể giữ' hiện tồn kho của hàng X\n"
         "- Ô 'Đề nghị' để trống, chờ nhập"),

        ("005", "Thêm cùng một hàng hai lần", "P1",
         "Bảng đã có hàng X",
         "1. Bấm dấu cộng, chọn lại hàng X\n2. Quan sát bảng",
         "Hàng X thêm lần 2",
         "⚠️ Ghi nhận CHÍNH XÁC hiện tượng thấy được: bảng có hai dòng cùng hàng X hay hệ thống chặn "
         "trùng — ghi lại kết quả thực tế kèm ảnh chụp màn hình"),

        ("006", "Chọn Đơn vị tính cho dòng hàng", "P0",
         "Hàng X có 2 đơn vị tính: 'Cái' (hệ số 1) và 'Thùng' (hệ số 10). Tồn kho 30 cái",
         "1. Ở dòng hàng X, mở ô 'Đơn vị tính'\n2. Chọn 'Cái'\n3. Đổi sang 'Thùng (x10)'",
         "30 cái = 3 thùng",
         "- Ô 'Đơn vị tính' liệt kê đủ các đơn vị của hàng X kèm hệ số\n"
         "- Chọn 'Cái': cột 'Có thể giữ' hiện 30\n"
         "- Đổi 'Thùng': cột 'Có thể giữ' tính lại thành 3"),

        ("007", "Không chọn Đơn vị tính", "P0",
         "Đã thêm hàng X, nhập Đề nghị 5, để trống Đơn vị tính",
         "1. Bấm 'Lưu'",
         "Thiếu Đơn vị tính",
         "- Dưới ô 'Đơn vị tính' của dòng đó hiện dòng chữ đỏ 'Bắt buộc phải chọn'\n"
         "- Phiếu không được tạo"),

        ("008", "Xóa một dòng hàng", "P1",
         "Bảng đang có 3 dòng hàng",
         "1. Bấm nút dấu trừ ở dòng thứ 2\n2. Quan sát bảng",
         "3 dòng, xóa dòng 2",
         "- Bảng còn 2 dòng, cột STT đánh lại thành 1 và 2\n- Dòng 'Tổng cộng' tính lại"),

        ("009", "Xóa hết hàng rồi bấm Lưu", "P0",
         "Bảng Chi tiết đang trống",
         "1. Điền đủ Khách hàng, Ghi chú, File đính kèm, Giữ đến ngày\n2. Bấm 'Lưu'",
         "0 dòng hàng",
         "- Hệ thống chặn, báo 'Tạo yêu cầu thất bại!' kèm dòng chữ đỏ 'Bắt buộc phải chọn' ở phần "
         "hàng hóa"),

        ("010", "Không chọn Khách hàng", "P0",
         "Đã thêm hàng và nhập đủ số lượng, để trống Khách hàng",
         "1. Bấm 'Lưu'",
         "Thiếu Khách hàng",
         "- Dưới ô 'Khách hàng' hiện dòng chữ đỏ 'Bắt buộc phải chọn'\n- Phiếu không được tạo"),

        ("011", "Không nhập Ghi chú", "P0",
         "Đã điền đủ các ô khác, để trống Ghi chú",
         "1. Bấm 'Lưu'",
         "Thiếu Ghi chú",
         "- Dưới ô Ghi chú hiện dòng chữ đỏ 'Bắt buộc phải nhập'\n"
         "⚠️ Điểm khác biệt: 5 loại có hợp đồng thì Ghi chú KHÔNG bắt buộc"),

        ("012", "Không đính kèm file nào", "P0",
         "Đã điền đủ các ô khác, không đính kèm file",
         "1. Bấm 'Lưu'",
         "Không có file",
         "- Hệ thống chặn, báo bắt buộc phải có file đính kèm\n"
         "⚠️ Điểm khác biệt: 5 loại có hợp đồng thì File đính kèm KHÔNG bắt buộc"),

        ("013", "Đề nghị vượt quá tồn kho ở loại 'Xuất giữ khác'", "P1",
         "Hàng X có 'Có thể giữ' = 30, đơn vị 'Cái'",
         "1. Nhập Đề nghị = 100\n2. Điền đủ các ô bắt buộc\n3. Bấm 'Lưu'",
         "Đề nghị 100 > tồn 30",
         "⚠️ Loại 'Xuất giữ khác' KHÔNG kiểm tra tồn kho lúc lưu — phiếu vẫn tạo được. Việc chặn xảy "
         "ra về sau, khi kế toán bấm 'Duyệt giữ hàng'. Ghi nhận đúng như vậy"),

        ("014", "Lập phiếu 'Xuất giữ khác' đầy đủ và gửi duyệt", "P0",
         "Tài khoản A, hàng X còn tồn 30 cái",
         "1. Chọn loại 'Xuất giữ khác'\n2. Chọn khách hàng KH001\n3. Chọn 'Giữ đến ngày' 30/03/2026\n"
         "4. Nhập Ghi chú, đính kèm 1 file\n5. Thêm hàng X, chọn đơn vị 'Cái', nhập Đề nghị 10\n"
         "6. Bấm 'Lưu & Gửi duyệt'",
         "Hàng X · 10 cái · KH001",
         "- Báo 'Yêu cầu của bạn đã được gửi'\n- Phiếu ở 'Chờ TP duyệt'\n"
         "- Trên lưới, cột 'Loại yêu cầu' hiện 'Xuất giữ khác' và cột 'Hợp đồng' để trống"),

        ("015", "Số lượng đề nghị vượt 6 chữ số", "P1",
         "Đã thêm hàng X",
         "1. Nhập Đề nghị = 1234567\n2. Bấm 'Lưu'",
         "7 chữ số",
         "- Dưới ô Đề nghị hiện dòng chữ đỏ 'Không được vượt quá 6 chữ số'"),

        ("016", "Nhập chữ vào ô Đề nghị", "P1",
         "Đã thêm hàng X",
         "1. Gõ 'abc' vào ô Đề nghị\n2. Bấm 'Lưu'",
         "Ký tự chữ",
         "- Dưới ô Đề nghị hiện dòng chữ đỏ 'Không hợp lệ'"),

        ("017", "Nhập số âm vào ô Đề nghị", "P1",
         "Đã thêm hàng X",
         "1. Gõ -5 vào ô Đề nghị\n2. Bấm 'Lưu'",
         "Số âm",
         "- Hệ thống báo lỗi ở dòng đó, phiếu không được tạo\n"
         "- Ghi nhận đúng nội dung thông báo nhìn thấy"),
    ]),

    # ------------------------------------------------------------------ V
    ("V", "YÊU CẦU XUẤT GIỮ - SỬA & XÓA", [
        ("001", "Sửa phiếu ở trạng thái 'Đang tạo'", "P0",
         "Tài khoản A có phiếu P ở 'Đang tạo', loại 'Xuất giữ khác', 1 dòng hàng số lượng 10",
         "1. Bấm bánh răng → 'Sửa yêu cầu'\n2. Đổi Đề nghị thành 6\n3. Bấm 'Lưu'\n4. Mở lại phiếu",
         "10 → 6",
         "- Màn sửa mở với dữ liệu cũ đã điền sẵn\n- Lưu thành công\n"
         "- Mở lại thấy số lượng 6"),

        ("002", "Ô 'Loại yêu cầu' bị khóa ở màn sửa", "P0",
         "Phiếu P loại 'Xuất giữ khác' ở 'Đang tạo'",
         "1. Mở màn 'Sửa yêu cầu' của phiếu P\n2. Thử đổi 'Loại yêu cầu'",
         "Phiếu P",
         "- Ô 'Loại yêu cầu' bị khóa, không đổi được\n"
         "- Với loại có hợp đồng, nút chọn hợp đồng và nút xóa hợp đồng cũng bị khóa"),

        ("003", "Sửa rồi gửi duyệt luôn", "P0",
         "Phiếu P ở 'Đang tạo'",
         "1. Mở màn sửa\n2. Sửa số lượng\n3. Bấm 'Lưu & Gửi duyệt'\n4. Kiểm tra trạng thái",
         "Phiếu P",
         "- Báo 'Yêu cầu của bạn đã được gửi'\n- Phiếu chuyển sang 'Chờ TP duyệt'"),

        ("004", "Không sửa được phiếu đang chờ duyệt", "P0",
         "Phiếu P đang ở 'Chờ TP duyệt', do A lập",
         "1. Đăng nhập A\n2. Bấm bánh răng của phiếu P\n"
         "3. Thử mở màn sửa bằng liên kết trực tiếp",
         "Phiếu P — Chờ TP duyệt",
         "- Menu Hành động không có mục 'Sửa yêu cầu'\n"
         "- Mở bằng liên kết trực tiếp thì hệ thống từ chối"),

        ("005", "Không sửa được phiếu 'Đang tạo' của người khác", "P0",
         "Phiếu P ở 'Đang tạo' do A lập; tài khoản C là người khác",
         "1. Đăng nhập C\n2. Mở màn sửa phiếu P bằng liên kết trực tiếp",
         "Phiếu P của A",
         "- Hệ thống từ chối, không mở được màn sửa"),

        ("006", "Sửa phiếu bị trả về sau khi Trưởng phòng không duyệt", "P0",
         "Phiếu P bị Trưởng phòng không duyệt, đã quay về 'Đang tạo' với ghi chú 'Số lượng quá nhiều'",
         "1. Đăng nhập A\n2. Mở màn xem phiếu P đọc ghi chú\n3. Mở màn sửa, giảm số lượng\n"
         "4. Bấm 'Lưu & Gửi duyệt'\n5. Đăng nhập Trưởng phòng E kiểm tra",
         "Phiếu P bị trả về",
         "- Màn xem hiện khối 'Ghi chú duyệt' với nội dung 'Số lượng quá nhiều'\n"
         "- Sửa và gửi lại được, phiếu về 'Chờ TP duyệt'\n"
         "- Trưởng phòng E lại thấy phiếu trong danh sách chờ duyệt"),

        ("007", "Thông tin người duyệt cấp trước sau khi phiếu bị trả về", "P1",
         "Phiếu P đã được Trưởng phòng duyệt, sau đó bị Ban giám đốc không duyệt và về 'Đang tạo'",
         "1. Mở màn xem chi tiết phiếu P\n2. Quan sát phần thông tin người duyệt",
         "Phiếu bị trả về từ cấp 2",
         "⚠️ Ghi nhận thực tế: phiếu vẫn còn hiện tên Trưởng phòng đã duyệt ở lần trước, dù phiếu đã "
         "quay về 'Đang tạo' và sẽ phải duyệt lại từ đầu. Lỗi đã biết"),

        ("008", "Sửa 'Giữ đến ngày' vượt hạn tối đa", "P1",
         "Cấu hình cho giữ tối đa 30 ngày, hôm nay 05/03/2026",
         "1. Mở màn sửa phiếu P\n2. Đổi 'Giữ đến ngày' thành 30/06/2026\n3. Bấm 'Lưu'",
         "Vượt hạn",
         "- Hệ thống báo 'Không thể giữ quá 04/04/2026'\n- Phiếu không được lưu"),

        ("009", "Xóa phiếu ở 'Đang tạo'", "P0",
         "Tài khoản A có phiếu P ở 'Đang tạo'",
         "1. Bấm bánh răng → 'Xóa'\n2. Bấm 'Xác nhận' ở cửa sổ hỏi lại\n3. Quan sát lưới",
         "Phiếu P",
         "- Có cửa sổ hỏi lại trước khi xóa\n- Báo 'Xóa phiếu thành công!'\n"
         "- Phiếu biến mất khỏi lưới"),

        ("010", "Hủy bỏ ở cửa sổ xác nhận xóa", "P2",
         "Tài khoản A có phiếu P ở 'Đang tạo'",
         "1. Bấm bánh răng → 'Xóa'\n2. Bấm nút hủy ở cửa sổ hỏi lại",
         "Phiếu P",
         "- Cửa sổ đóng lại\n- Phiếu P vẫn còn trên lưới"),

        ("011", "Không xóa được phiếu đang chờ duyệt", "P0",
         "Phiếu P đang 'Chờ KT duyệt'",
         "1. Bấm bánh răng của phiếu P\n"
         "2. Dùng công cụ kiểm thử gọi thẳng chức năng Xóa, bỏ qua giao diện",
         "Phiếu P — Chờ KT duyệt",
         "- Menu Hành động không có mục 'Xóa'\n- Gọi thẳng chức năng cũng bị từ chối\n"
         "- Phiếu vẫn còn"),

        ("012", "Xóa phiếu đã đính kèm file", "P2",
         "Phiếu P ở 'Đang tạo' có 2 file đính kèm",
         "1. Xóa phiếu P\n2. Kiểm tra lưới",
         "Phiếu có file",
         "- Xóa thành công, không báo lỗi\n- Phiếu và các dòng hàng của nó biến mất khỏi hệ thống"),

        ("013", "Gỡ một file đính kèm ở màn sửa", "P2",
         "Phiếu P loại 'Xuất giữ khác' có 2 file đính kèm",
         "1. Mở màn sửa\n2. Bấm dấu × ở file thứ nhất\n3. Bấm 'Lưu'\n4. Mở lại phiếu",
         "2 file, gỡ 1",
         "- Phiếu còn 1 file\n"
         "⚠️ Loại 'Xuất giữ khác' bắt buộc có file: gỡ hết cả 2 file rồi lưu phải bị chặn"),
    ]),

    # ------------------------------------------------------------------ VI
    ("VI", "YÊU CẦU XUẤT GIỮ - DUYỆT & KHÔNG DUYỆT", [
        ("001", "Trưởng phòng duyệt, phiếu đi thẳng xuống Kế toán", "P0",
         "Phiếu P 'Chờ TP duyệt', gắn hợp đồng khách đã thanh toán 80%, trong khi Quy chế công ty "
         "yêu cầu tối thiểu 30%",
         "1. Đăng nhập Trưởng phòng E\n2. Mở phiếu P\n3. Bấm 'TP duyệt'\n4. Kiểm tra trạng thái",
         "Đã thu 80% ≥ ngưỡng 30%",
         "- Báo 'Thao tác thành công!'\n- Phiếu chuyển thẳng sang 'Chờ KT duyệt'\n"
         "- Kế toán G nhìn thấy phiếu ở màn chờ duyệt"),

        ("002", "Trưởng phòng duyệt, phiếu phải qua Ban giám đốc", "P0",
         "Phiếu P 'Chờ TP duyệt', gắn hợp đồng khách mới thanh toán 10%, Quy chế công ty yêu cầu "
         "tối thiểu 30%",
         "1. Đăng nhập Trưởng phòng E\n2. Mở phiếu P\n3. Bấm 'TP duyệt'\n4. Kiểm tra trạng thái",
         "Đã thu 10% < ngưỡng 30%",
         "- Báo 'Yêu cầu đã được chuyển đến BGĐ'\n- Phiếu chuyển sang 'Chờ BGĐ duyệt'\n"
         "- Kế toán G CHƯA nhìn thấy phiếu"),

        ("003", "Phiếu 'Xuất giữ khác' vượt ngưỡng giá trị phải qua Ban giám đốc", "P0",
         "Quy chế công ty khai 'Giá trị giữ hàng khác' là 50,000,000. Phiếu P loại 'Xuất giữ khác' có "
         "tổng thành tiền 80,000,000",
         "1. Đăng nhập Trưởng phòng E\n2. Bấm 'TP duyệt'\n3. Kiểm tra trạng thái",
         "80,000,000 > 50,000,000",
         "- Phiếu chuyển sang 'Chờ BGĐ duyệt', báo 'Yêu cầu đã được chuyển đến BGĐ'"),

        ("004", "Phiếu 'Xuất giữ khác' dưới ngưỡng đi thẳng xuống Kế toán", "P0",
         "Quy chế công ty khai 'Giá trị giữ hàng khác' là 50,000,000. Phiếu P có tổng thành tiền "
         "20,000,000",
         "1. Đăng nhập Trưởng phòng E\n2. Bấm 'TP duyệt'\n3. Kiểm tra trạng thái",
         "20,000,000 < 50,000,000",
         "- Phiếu chuyển thẳng sang 'Chờ KT duyệt'"),

        ("005", "Ban giám đốc duyệt và nhập lại 'Giữ đến ngày'", "P0",
         "Phiếu P 'Chờ BGĐ duyệt', 'Giữ đến ngày' đang là 30/03/2026",
         "1. Đăng nhập Ban giám đốc F\n2. Mở phiếu P\n3. Đổi 'Giữ đến ngày' thành 20/03/2026\n"
         "4. Bấm 'BGĐ duyệt'\n5. Mở lại phiếu",
         "30/03/2026 → 20/03/2026",
         "- Báo 'Thao tác thành công!'\n- Phiếu chuyển sang 'Chờ KT duyệt'\n"
         "- 'Giữ đến ngày' trên phiếu là 20/03/2026"),

        ("006", "Ban giám đốc nhập 'Giữ đến ngày' là ngày quá khứ", "P0",
         "Phiếu P 'Chờ BGĐ duyệt', hôm nay 05/03/2026",
         "1. Đăng nhập F\n2. Đổi 'Giữ đến ngày' thành 01/03/2026\n3. Bấm 'BGĐ duyệt'",
         "Ngày quá khứ",
         "- Hệ thống chặn, báo 'Phải nhập ngày tương lai!'\n- Phiếu vẫn ở 'Chờ BGĐ duyệt'"),

        ("007", "Trưởng phòng không duyệt", "P0",
         "Phiếu P 'Chờ TP duyệt'",
         "1. Đăng nhập E\n2. Mở phiếu P\n3. Bấm 'Không duyệt'\n"
         "4. Nhập ghi chú 'Số lượng quá nhiều' ở cửa sổ 'Ghi chú duyệt'\n5. Bấm nút xác nhận\n"
         "6. Đăng nhập A kiểm tra",
         "Ghi chú: Số lượng quá nhiều",
         "- Báo 'Thao tác thành công!'\n- Phiếu quay về 'Đang tạo'\n"
         "- A mở phiếu thấy khối 'Ghi chú duyệt' với đúng nội dung trên\n"
         "- A sửa lại được phiếu"),

        ("008", "Không duyệt mà bỏ trống ghi chú", "P1",
         "Phiếu P 'Chờ TP duyệt'",
         "1. Bấm 'Không duyệt'\n2. Để trống ô ghi chú\n3. Bấm nút xác nhận",
         "Ghi chú rỗng",
         "- Ghi nhận CHÍNH XÁC hiện tượng: hệ thống có bắt nhập ghi chú hay cho qua\n"
         "- Nếu cho qua thì kiểm tra phiếu vẫn về 'Đang tạo' và khối 'Ghi chú duyệt' để trống"),

        ("009", "Ghi chú không duyệt vượt độ dài cho phép", "P2",
         "Phiếu P 'Chờ TP duyệt'",
         "1. Bấm 'Không duyệt'\n2. Nhập ghi chú dài hơn 255 ký tự\n3. Bấm nút xác nhận",
         "Ghi chú 300 ký tự",
         "- Hệ thống báo 'Thao tác thất bại!' kèm dòng chữ đỏ 'Không được vượt quá 255 ký tự'"),

        ("010", "Ban giám đốc không duyệt cũng đưa phiếu về 'Đang tạo'", "P0",
         "Phiếu P 'Chờ BGĐ duyệt', đã qua Trưởng phòng",
         "1. Đăng nhập F\n2. Bấm 'Không duyệt', nhập ghi chú\n3. Kiểm tra trạng thái",
         "Phiếu P",
         "⚠️ Phiếu về thẳng 'Đang tạo', KHÔNG quay lại 'Chờ TP duyệt'\n"
         "- Người lập sửa xong gửi lại thì phải duyệt lại từ cấp Trưởng phòng"),

        ("011", "Kế toán không duyệt", "P1",
         "Phiếu P 'Chờ KT duyệt'",
         "1. Đăng nhập Kế toán G\n2. Mở phiếu P\n3. Quan sát các nút\n"
         "4. Bấm 'Không duyệt', nhập ghi chú, xác nhận",
         "Phiếu P — Chờ KT duyệt",
         "- Màn xem có cả nút 'Không duyệt' lẫn nút 'Tạo phiếu xuất giữ'\n"
         "- Sau khi không duyệt: phiếu về 'Đang tạo' kèm ghi chú"),

        ("012", "Trưởng phòng duyệt phiếu của phòng khác", "P0",
         "Phiếu P do người phòng Kinh doanh 2 lập, đang 'Chờ TP duyệt'. Tài khoản E chỉ quản lý "
         "phòng Kinh doanh 1",
         "1. Đăng nhập E\n2. Mở phiếu P bằng liên kết trực tiếp\n3. Quan sát các nút",
         "Phiếu của phòng khác",
         "- Không có nút 'TP duyệt', không có nút 'Không duyệt'\n"
         "- Phiếu P cũng không nằm trong màn chờ duyệt của E"),

        ("013", "Duyệt phiếu đã được người khác duyệt trước đó", "P0",
         "Hai người cùng có quyền Trưởng phòng cho phòng Kinh doanh 1, cùng mở phiếu P "
         "'Chờ TP duyệt' trên hai máy",
         "1. Máy 1 bấm 'TP duyệt' thành công\n2. Máy 2 (chưa tải lại trang) bấm 'TP duyệt'\n"
         "3. Ghi nhận kết quả trên máy 2",
         "Duyệt đồng thời",
         "- Máy 2 bị từ chối, không duyệt được lần hai\n"
         "- Phiếu chỉ ghi nhận một lần duyệt, trạng thái không nhảy sai"),

        ("014", "Bảng Chi tiết ở màn xem có cột 'Được duyệt'", "P1",
         "Phiếu P đã qua ít nhất một cấp duyệt",
         "1. Mở màn xem phiếu P\n2. Quan sát bảng Chi tiết",
         "Phiếu P",
         "- Nhóm 'Số lượng' ở màn xem có thêm cột 'Được duyệt' so với màn tạo/sửa\n"
         "- Cột này cho biết số lượng thực tế được duyệt cho từng dòng hàng"),

        ("015", "In yêu cầu từ menu Hành động", "P1",
         "Phiếu P đã duyệt xong",
         "1. Bấm bánh răng → 'In yêu cầu'\n2. Quan sát trang in mở ra",
         "Phiếu P — Đã duyệt",
         "- Mở tab mới hiển thị bản in của đúng phiếu P\n"
         "- Bản in có mã phiếu, thông tin khách hàng, bảng hàng hóa, người lập và người duyệt"),

        ("016", "In yêu cầu của phiếu chưa duyệt", "P1",
         "Phiếu P đang ở 'Chờ TP duyệt', chưa ai duyệt",
         "1. Bấm bánh răng → 'In yêu cầu'\n2. Xem ô Ngày duyệt trên bản in",
         "Phiếu chưa duyệt",
         "⚠️ Ghi nhận thực tế: bản in vẫn in ra NGÀY HÔM NAY ở ô Ngày duyệt thay vì để trống. "
         "Lỗi đã biết, cần ghi nhận lại"),
    ]),

    # ------------------------------------------------------------------ VII
    ("VII", "PHIẾU XUẤT GIỮ - DANH SÁCH & BỘ LỌC", [
        ("001", "Vào màn danh sách phiếu xuất giữ", "P0",
         "Tài khoản G có quyền 'Kế toán duyệt hàng giữ' và 'Trưởng phòng kế toán'",
         "1. Bấm menu Kế toán\n2. Bấm Hàng hóa - Dịch vụ - Vận chuyển → nhóm Giữ hàng\n"
         "3. Bấm 'Phiếu xuất giữ'",
         "Tài khoản: G",
         "- Trang mở với tiêu đề 'Danh sách phiếu xuất giữ'\n"
         "- Lưới có đủ 9 cột: STT · Mã phiếu · YCXG · Người yêu cầu · Phòng yêu cầu · Người lập · "
         "Ngày lập · Trạng thái · Hành động"),

        ("002", "Màn này không có ở menu Khởi tạo", "P2",
         "Tài khoản G đã đăng nhập",
         "1. Mở menu Khởi tạo → Hàng hóa → nhóm Giữ hàng\n2. Tìm mục 'Phiếu xuất giữ'",
         "Menu Khởi tạo",
         "- Menu Khởi tạo KHÔNG có mục 'Phiếu xuất giữ'\n"
         "- Màn này chỉ vào được từ menu Kế toán"),

        ("003", "Cột YCXG là liên kết mở phiếu yêu cầu cha", "P0",
         "Phiếu xuất giữ X được lập từ phiếu yêu cầu P",
         "1. Bấm mã phiếu ở cột 'YCXG' của dòng phiếu X\n2. Quan sát",
         "Phiếu X ← phiếu P",
         "- Mở màn xem chi tiết của đúng phiếu yêu cầu P\n"
         "- Cột 'Người yêu cầu' và 'Phòng yêu cầu' của phiếu X khớp người lập và phòng của phiếu P"),

        ("004", "Cột Người lập khác cột Người yêu cầu", "P0",
         "Phiếu yêu cầu P do nhân viên kinh doanh A lập; phiếu xuất giữ X do kế toán G lập",
         "1. Xem dòng phiếu X trên lưới\n2. So hai cột",
         "A ≠ G",
         "- Cột 'Người yêu cầu' hiện A\n- Cột 'Người lập' hiện G\n"
         "⚠️ Đây là hai người khác nhau, không được lẫn"),

        ("005", "Cột Hành động của phiếu nháp do chính mình lập", "P0",
         "Kế toán G có phiếu X ở 'Đang tạo'",
         "1. Đăng nhập G\n2. Xem cột Hành động của dòng phiếu X",
         "Phiếu X — Đang tạo",
         "- Có 3 nút: bút chì 'Sửa' · thùng rác 'Xóa' · máy in 'In đề nghị'"),

        ("006", "Cột Hành động của phiếu đã duyệt", "P0",
         "Phiếu X đã ở trạng thái 'Đã duyệt'",
         "1. Xem cột Hành động của dòng phiếu X",
         "Phiếu X — Đã duyệt",
         "- Chỉ còn nút máy in 'In đề nghị'\n- Không có nút Sửa, không có nút Xóa"),

        ("007", "Cột Hành động của phiếu nháp do người khác lập", "P1",
         "Phiếu X ở 'Đang tạo' do kế toán G lập; tài khoản G2 cũng là kế toán, có quyền "
         "'Trưởng phòng kế toán'",
         "1. Đăng nhập G2\n2. Tìm phiếu X trên lưới\n3. Xem cột Hành động",
         "Phiếu X của G",
         "- G2 nhìn thấy phiếu X nhưng chỉ có nút 'In đề nghị'\n"
         "- Không sửa, không xóa được phiếu nháp của người khác"),

        ("008", "Lọc theo Mã phiếu", "P0",
         "Biết trước mã một phiếu xuất giữ",
         "1. Gõ mã phiếu vào ô 'Mã phiếu'\n2. Chờ lưới tải lại",
         "Mã phiếu",
         "- Lưới chỉ còn đúng phiếu đó"),

        ("009", "Lọc theo YCXG", "P0",
         "Biết trước mã phiếu yêu cầu cha",
         "1. Gõ mã phiếu yêu cầu vào ô 'YCXG'\n2. Chờ lưới tải lại",
         "Mã phiếu yêu cầu",
         "- Lưới chỉ còn phiếu xuất giữ sinh ra từ phiếu yêu cầu đó\n"
         "- Tối đa 1 dòng, vì mỗi phiếu yêu cầu chỉ sinh một phiếu xuất giữ"),

        ("010", "Lọc theo Người yêu cầu", "P0",
         "Nhân viên A đã lập 3 phiếu yêu cầu đều đã được kế toán lập phiếu xuất giữ",
         "1. Chọn nhân viên A ở ô 'Người yêu cầu'\n2. Chờ lưới tải lại",
         "Người yêu cầu: A",
         "- Lưới hiện đúng 3 phiếu xuất giữ tương ứng"),

        ("011", "Lọc theo Người lập", "P1",
         "Kế toán G đã lập 4 phiếu",
         "1. Chọn G ở ô 'Người lập'\n2. Chờ lưới tải lại",
         "Người lập: G",
         "- Lưới hiện đúng 4 phiếu do G lập"),

        ("012", "Bộ lọc Trạng thái chỉ có hai lựa chọn", "P1",
         "Đang ở màn danh sách phiếu xuất giữ",
         "1. Mở ô lọc 'Trạng thái'\n2. Liệt kê các lựa chọn",
         "Ô lọc Trạng thái",
         "⚠️ Ghi nhận thực tế: chỉ có 'Đã duyệt' và 'Chờ duyệt'\n"
         "- Không có lựa chọn để lọc riêng phiếu nháp 'Đang tạo', dù lưới vẫn hiện phiếu nháp"),

        ("013", "Lọc theo Tên, mã hàng hóa", "P0",
         "Hàng X nằm trong 2 phiếu xuất giữ",
         "1. Gõ tên hàng X vào ô 'Tên, mã hàng hóa'\n2. Chờ lưới tải lại",
         "Tên hàng X",
         "- Lưới hiện đúng 2 phiếu có chứa hàng X"),

        ("014", "Lọc theo khoảng ngày lập", "P0",
         "Có phiếu lập rải trong tháng",
         "1. Chọn 'Từ ngày' 01/03/2026 và 'Đến ngày' 10/03/2026\n2. Chờ lưới tải lại",
         "01/03/2026 → 10/03/2026",
         "- Chỉ hiện phiếu có Ngày lập nằm trong khoảng, tính trọn cả hai ngày đầu và cuối"),

        ("015", "Bấm nút In danh sách", "P1",
         "Đang lọc khoảng ngày 01/03/2026 → 10/03/2026, lưới còn 5 phiếu",
         "1. Bấm nút 'In'\n2. Quan sát trang in",
         "5 phiếu",
         "- Mở tab mới in đúng 5 phiếu đang lọc\n"
         "- Đầu bản in có dòng 'Từ ngày 01/03/2026 đến ngày 10/03/2026'"),

        ("016", "Bấm nút Xuất excel danh sách", "P0",
         "Đang ở màn 'Danh sách phiếu xuất giữ'",
         "1. Bấm nút 'Xuất excel'\n2. Ghi nhận kết quả",
         "Nút Xuất excel",
         "⚠️ Ghi nhận thực tế: nút này đang LỖI, bấm vào ra trang báo lỗi thay vì tải file. "
         "Lỗi đã biết, vẫn phải ghi nhận lại kèm ảnh chụp màn hình\n"
         "- Đối chiếu: nút 'Xuất excel' ở màn 'Danh sách yêu cầu xuất giữ' tải file bình thường"),
    ]),

    # ------------------------------------------------------------------ VIII
    ("VIII", "PHIẾU XUẤT GIỮ - LẬP & DUYỆT GIỮ HÀNG", [
        ("001", "Mở màn tạo từ nút trên phiếu yêu cầu", "P0",
         "Phiếu yêu cầu P đang 'Chờ KT duyệt', kế toán G có quyền",
         "1. Đăng nhập G\n2. Mở màn xem phiếu P\n3. Bấm 'Tạo phiếu xuất giữ'",
         "Phiếu P",
         "- Trang mở với tiêu đề 'Tạo phiếu xuất giữ'\n"
         "- Ô 'Chọn phiếu yêu cầu xuất giữ' đã điền sẵn mã phiếu P và bị khóa\n"
         "- Bảng Chi tiết đã chép sẵn hàng hóa của phiếu P"),

        ("002", "Mở màn tạo từ menu và tự chọn phiếu yêu cầu", "P0",
         "Có 3 phiếu yêu cầu ở 'Chờ KT duyệt', 2 phiếu ở 'Chờ TP duyệt', 1 phiếu 'Đã duyệt'",
         "1. Vào 'Danh sách phiếu xuất giữ' → bấm 'Tạo mới'\n"
         "2. Bấm kính lúp ở ô 'Chọn phiếu yêu cầu xuất giữ'\n3. Quan sát cửa sổ",
         "6 phiếu yêu cầu ở các trạng thái khác nhau",
         "- Cửa sổ 'Phiếu yêu cầu xuất giữ' chỉ liệt kê đúng 3 phiếu 'Chờ KT duyệt'\n"
         "- Cửa sổ có 4 cột: STT · Mã phiếu · Người tạo · Ngày tạo và ô tìm theo Mã phiếu, Người tạo"),

        ("003", "Chọn phiếu yêu cầu nạp dữ liệu vào form", "P0",
         "Phiếu yêu cầu P loại 'Xuất giữ khác', khách hàng KH001, 'Giữ đến ngày' 30/03/2026, "
         "2 dòng hàng",
         "1. Chọn phiếu P trong cửa sổ\n2. Quan sát toàn bộ form",
         "Phiếu P",
         "- Ô 'Loại đề nghị' hiện 'Xuất giữ khác' và bị khóa\n"
         "- Ô 'Khách hàng' hiện KH001, chỉ đọc\n"
         "- Ô 'Giữ đến ngày' điền 30/03/2026 và SỬA ĐƯỢC\n"
         "- Ô 'Người yêu cầu' và 'Phòng yêu cầu' điền theo người lập phiếu P, bị khóa\n"
         "- Bảng Chi tiết có 2 dòng, cột 'Cần xuất' đã tích sẵn, cột 'SL đề nghị' điền theo phiếu P"),

        ("004", "Bảng Chi tiết của phiếu xuất giữ", "P0",
         "Đã chọn phiếu yêu cầu P",
         "1. Quan sát bảng Chi tiết",
         "Phiếu P",
         "- Bảng có 10 cột: STT · Cần xuất · Tên hàng hóa · Model · Mã hàng hóa · Thương hiệu · "
         "SL có thể giữ · SL đề nghị · Đơn vị tính · Hình ảnh tham khảo\n"
         "- Không có cột Đơn giá, không có cột Thành tiền\n"
         "- Không có nút thêm hàng: kế toán không thêm hàng ngoài phiếu yêu cầu được"),

        ("005", "Kế toán giảm 'SL đề nghị' của một dòng", "P0",
         "Phiếu yêu cầu P xin 10 hàng X, tồn kho chỉ còn 6",
         "1. Sửa 'SL đề nghị' dòng hàng X thành 6\n2. Bấm 'Duyệt giữ hàng'\n"
         "3. Vào màn 'Danh sách hàng giữ' kiểm tra",
         "10 → 6",
         "- Lưu và duyệt thành công\n- Lô hàng giữ sinh ra có số lượng 6, không phải 10"),

        ("006", "Kế toán bỏ tích 'Cần xuất' một dòng", "P0",
         "Phiếu yêu cầu P có 2 dòng: hàng X 10, hàng Y 5",
         "1. Bỏ tích 'Cần xuất' ở dòng hàng Y\n2. Bấm 'Duyệt giữ hàng'\n"
         "3. Kiểm tra 'Danh sách hàng giữ'",
         "Bỏ dòng Y",
         "- Chỉ sinh lô hàng giữ cho hàng X số lượng 10\n- Không có lô nào cho hàng Y"),

        ("007", "Lưu nháp bằng nút 'Lưu'", "P0",
         "Đã chọn phiếu yêu cầu P đang 'Chờ KT duyệt'",
         "1. Bấm 'Lưu'\n2. Vào 'Danh sách phiếu xuất giữ'\n"
         "3. Vào 'Danh sách yêu cầu xuất giữ' xem phiếu P\n4. Vào 'Danh sách hàng giữ' kiểm tra",
         "Lưu nháp",
         "- Báo 'Phiếu đã được lưu.'\n- Phiếu xuất giữ mới ở trạng thái 'Đang tạo'\n"
         "- Phiếu yêu cầu P chuyển sang 'Đang xuất giữ'\n"
         "⚠️ 'Danh sách hàng giữ' CHƯA có lô hàng nào — lưu nháp không ghi kho"),

        ("008", "Duyệt giữ hàng sinh lô hàng giữ", "P0",
         "Phiếu yêu cầu P do nhân viên A lập cho khách KH001, xin giữ 10 hàng X đến 30/03/2026. "
         "Kế toán G lập phiếu xuất giữ. Hôm nay 05/03/2026",
         "1. Đăng nhập G, mở màn tạo phiếu xuất giữ từ phiếu P\n2. Bấm 'Duyệt giữ hàng'\n"
         "3. Vào 'Danh sách yêu cầu xuất giữ' xem phiếu P\n"
         "4. Vào 'Danh sách hàng giữ' tìm hàng X",
         "10 hàng X · KH001 · hạn 30/03/2026",
         "- Phiếu xuất giữ ở trạng thái 'Đã duyệt'\n- Phiếu yêu cầu P chuyển sang 'Đã duyệt'\n"
         "- 'Danh sách hàng giữ' có 1 lô: hàng X · số lượng 10 · khách KH001 · hạn 30/03/2026 · "
         "ngày bắt đầu giữ 05/03/2026\n"
         "⚠️ Người giữ ghi là NHÂN VIÊN A (người lập phiếu yêu cầu), KHÔNG phải kế toán G"),

        ("009", "Kế toán sửa 'Giữ đến ngày' trước khi duyệt", "P0",
         "Phiếu yêu cầu P có 'Giữ đến ngày' 30/03/2026",
         "1. Ở màn tạo phiếu xuất giữ, đổi 'Giữ đến ngày' thành 20/03/2026\n2. Bấm 'Duyệt giữ hàng'\n"
         "3. Kiểm tra 'Danh sách hàng giữ'",
         "30/03/2026 → 20/03/2026",
         "- Lô hàng giữ sinh ra có hạn 20/03/2026, theo ngày kế toán nhập\n"
         "- Phiếu yêu cầu P vẫn hiện ngày ban đầu người lập xin"),

        ("010", "Số lượng quy đổi theo đơn vị tính", "P0",
         "Phiếu yêu cầu P xin 2 hàng X với đơn vị 'Thùng' hệ số 10",
         "1. Bấm 'Duyệt giữ hàng'\n2. Vào 'Danh sách hàng giữ' xem số lượng hàng X",
         "2 thùng × 10",
         "- Lô hàng giữ ghi 20 theo đơn vị gốc, không phải 2"),

        ("011", "Duyệt khi tồn kho không đủ", "P0",
         "Phiếu yêu cầu P xin 10 hàng X, nhưng tồn kho khả dụng chỉ còn 4",
         "1. Bấm 'Duyệt giữ hàng'\n2. Đọc thông báo\n3. Kiểm tra 'Danh sách hàng giữ'",
         "Xin 10 · tồn 4",
         "- Hệ thống chặn, báo 'Kho không đủ số lượng. Vui lòng cập nhật lại số liệu!'\n"
         "- Không có lô hàng giữ nào được sinh ra\n- Phiếu yêu cầu P vẫn ở trạng thái cũ"),

        ("012", "Lưu nháp không bị chặn bởi tồn kho", "P0",
         "Phiếu yêu cầu P xin 10 hàng X, tồn kho khả dụng chỉ còn 4",
         "1. Bấm 'Lưu' (không phải 'Duyệt giữ hàng')\n2. Ghi nhận kết quả",
         "Xin 10 · tồn 4",
         "⚠️ Bản nháp lưu được bình thường, KHÔNG kiểm tra tồn kho\n"
         "- Việc chặn chỉ xảy ra khi bấm 'Duyệt giữ hàng'"),

        ("013", "Nút 'Không duyệt' ở màn tạo phiếu xuất giữ", "P0",
         "Đã chọn phiếu yêu cầu P đang 'Chờ KT duyệt'",
         "1. Bấm nút 'Không duyệt'\n2. Kiểm tra trạng thái phiếu xuất giữ vừa tạo\n"
         "3. Kiểm tra trạng thái phiếu yêu cầu P\n4. Đăng nhập người lập A kiểm tra",
         "Nút Không duyệt",
         "⚠️ Ghi nhận CHÍNH XÁC hiện tượng thực tế: nút này hiện đang lưu BẢN NHÁP giống hệt nút "
         "'Lưu', chứ không trả phiếu về cho người lập\n"
         "- Phiếu yêu cầu P chuyển sang 'Đang xuất giữ'\n"
         "- A KHÔNG sửa lại được phiếu P\n"
         "- Muốn trả phiếu về cho A, kế toán phải dùng nút 'Không duyệt' ở màn XEM phiếu yêu cầu"),

        ("014", "Cộng dồn vào lô hàng giữ đã có", "P0",
         "Nhân viên A đã giữ sẵn 5 hàng X cho khách KH001 hạn 30/03/2026. Phiếu yêu cầu P của A xin "
         "thêm 7 hàng X cho cùng khách KH001, cùng hạn 30/03/2026",
         "1. Kế toán duyệt giữ hàng cho phiếu P\n2. Vào 'Danh sách hàng giữ' tìm hàng X của A",
         "5 + 7 = 12",
         "- Chỉ có MỘT dòng hàng X của A cho KH001 hạn 30/03/2026, số lượng 12\n"
         "- Không sinh dòng thứ hai"),

        ("015", "Hạn giữ khác nhau thì tách lô riêng", "P0",
         "Nhân viên A đã giữ 5 hàng X cho KH001 hạn 30/03/2026. Phiếu yêu cầu P xin thêm 7 hàng X "
         "cho KH001 nhưng hạn 20/03/2026",
         "1. Kế toán duyệt giữ hàng cho phiếu P\n2. Vào 'Danh sách hàng giữ' tìm hàng X của A",
         "Hai hạn khác nhau",
         "- Có HAI dòng riêng: 5 hàng X hạn 30/03/2026 và 7 hàng X hạn 20/03/2026\n"
         "- Không cộng gộp vì hạn giữ khác nhau"),

        ("016", "Khách hàng khác nhau thì tách lô riêng", "P1",
         "Nhân viên A đã giữ 5 hàng X cho KH001 hạn 30/03/2026. Phiếu yêu cầu P xin 7 hàng X cho "
         "KH002 cùng hạn 30/03/2026",
         "1. Kế toán duyệt giữ hàng cho phiếu P\n2. Kiểm tra 'Danh sách hàng giữ'",
         "Hai khách khác nhau",
         "- Có hai dòng riêng theo từng khách hàng, không cộng gộp"),

        ("017", "Không lập được phiếu xuất giữ thứ hai cho cùng phiếu yêu cầu", "P0",
         "Phiếu yêu cầu P đã được duyệt giữ hàng xong, đang ở 'Đã duyệt'",
         "1. Vào màn tạo phiếu xuất giữ\n2. Mở cửa sổ chọn phiếu yêu cầu\n3. Tìm phiếu P",
         "Phiếu P — Đã duyệt",
         "- Phiếu P không có trong cửa sổ chọn vì không còn ở 'Chờ KT duyệt'\n"
         "- Gọi thẳng chức năng bằng công cụ kiểm thử cũng bị từ chối, báo 'Không thể chọn phiếu này'"),

        ("018", "Không chọn phiếu yêu cầu mà bấm Lưu", "P0",
         "Đang ở màn tạo, chưa chọn phiếu yêu cầu nào",
         "1. Bấm 'Lưu'",
         "Thiếu phiếu yêu cầu",
         "- Hệ thống báo 'Tạo thất bại!'\n"
         "- Dưới ô 'Chọn phiếu yêu cầu xuất giữ' hiện dòng chữ đỏ 'Bắt buộc phải chọn'"),

        ("019", "Bỏ tích 'Cần xuất' toàn bộ các dòng rồi duyệt", "P0",
         "Phiếu yêu cầu P có 2 dòng hàng",
         "1. Bỏ tích 'Cần xuất' cả 2 dòng\n2. Bấm 'Duyệt giữ hàng'\n3. Ghi nhận kết quả",
         "0 dòng cần xuất",
         "⚠️ Ghi nhận CHÍNH XÁC hiện tượng: hệ thống có chặn hay vẫn cho lưu ra phiếu rỗng\n"
         "- Nếu lưu được thì kiểm tra 'Danh sách hàng giữ' không có lô nào và phiếu yêu cầu vẫn "
         "chuyển sang 'Đã duyệt' — ghi nhận lại kèm ảnh chụp màn hình"),

        ("020", "Nhập 'SL đề nghị' vượt số của phiếu yêu cầu", "P1",
         "Phiếu yêu cầu P xin 10 hàng X, tồn kho còn 50",
         "1. Sửa 'SL đề nghị' thành 20\n2. Bấm 'Duyệt giữ hàng'\n3. Kiểm tra 'Danh sách hàng giữ'",
         "Xin 10 · kế toán ghi 20",
         "⚠️ Ghi nhận CHÍNH XÁC hiện tượng: kế toán có bị chặn khi ghi nhiều hơn số người lập xin hay "
         "không. Nếu không bị chặn, kiểm tra lô hàng giữ sinh ra là 20 và ghi nhận lại"),

        ("021", "Ghi chú và file đính kèm trên phiếu xuất giữ", "P2",
         "Đang ở màn tạo phiếu xuất giữ",
         "1. Nhập Ghi chú, đính kèm 1 file hợp lệ\n2. Bấm 'Lưu'\n3. Mở lại phiếu",
         "Ghi chú + 1 file",
         "- Ghi chú và file được lưu, mở xem lại được\n"
         "- Ghi chú và file KHÔNG bắt buộc ở màn này"),

        ("022", "'Giữ đến ngày' là ngày quá khứ trên phiếu xuất giữ", "P1",
         "Hôm nay 05/03/2026",
         "1. Đổi 'Giữ đến ngày' thành 01/03/2026\n2. Bấm 'Duyệt giữ hàng'",
         "Ngày quá khứ",
         "- Hệ thống chặn, báo phải nhập ngày tương lai\n- Không sinh lô hàng giữ nào"),

        ("023", "Bấm 'Hủy' ở màn tạo phiếu xuất giữ", "P2",
         "Đã chọn phiếu yêu cầu P, đang điền dở",
         "1. Bấm 'Hủy'\n2. Kiểm tra trạng thái phiếu yêu cầu P",
         "Điền dở",
         "- Quay về 'Danh sách phiếu xuất giữ'\n- Không có phiếu xuất giữ nào được tạo\n"
         "- Phiếu yêu cầu P vẫn ở 'Chờ KT duyệt'"),

        ("024", "Hai kế toán cùng lập phiếu xuất giữ cho một phiếu yêu cầu", "P0",
         "Phiếu yêu cầu P đang 'Chờ KT duyệt'. Hai kế toán G và G2 cùng mở màn tạo cho phiếu P",
         "1. G bấm 'Duyệt giữ hàng' thành công\n2. G2 bấm 'Duyệt giữ hàng'\n"
         "3. Ghi nhận kết quả trên máy của G2\n4. Kiểm tra 'Danh sách hàng giữ'",
         "Hai người thao tác đồng thời",
         "- G2 bị từ chối, không tạo được phiếu thứ hai\n"
         "- 'Danh sách hàng giữ' chỉ ghi một lần, không nhân đôi số lượng"),
    ]),

    # ------------------------------------------------------------------ IX
    ("IX", "PHIẾU XUẤT GIỮ - SỬA, XÓA & XEM", [
        ("001", "Sửa bản nháp phiếu xuất giữ", "P0",
         "Kế toán G có phiếu xuất giữ X ở 'Đang tạo', hàng X số lượng 10",
         "1. Bấm nút bút chì ở cột Hành động\n2. Đổi 'SL đề nghị' thành 8\n3. Bấm 'Lưu'\n"
         "4. Mở lại phiếu",
         "10 → 8",
         "- Màn sửa mở với dữ liệu cũ\n- Ô 'Chọn phiếu yêu cầu xuất giữ' bị khóa, không đổi được\n"
         "- Lưu thành công, mở lại thấy số lượng 8"),

        ("002", "Sửa bản nháp rồi duyệt luôn", "P0",
         "Phiếu xuất giữ X ở 'Đang tạo', phiếu yêu cầu cha P đang 'Đang xuất giữ'",
         "1. Mở màn sửa phiếu X\n2. Bấm 'Duyệt giữ hàng'\n3. Kiểm tra hai phiếu và kho hàng giữ",
         "Nháp → duyệt",
         "- Phiếu X sang 'Đã duyệt'\n- Phiếu yêu cầu P sang 'Đã duyệt'\n"
         "- Lô hàng giữ được sinh ra"),

        ("003", "Không sửa được phiếu đã duyệt", "P0",
         "Phiếu xuất giữ X ở 'Đã duyệt'",
         "1. Xem cột Hành động của phiếu X\n"
         "2. Thử mở màn sửa bằng liên kết trực tiếp",
         "Phiếu X — Đã duyệt",
         "- Không có nút bút chì trên lưới\n- Mở bằng liên kết trực tiếp thì hệ thống từ chối"),

        ("004", "Không sửa được phiếu nháp của người khác", "P0",
         "Phiếu X ở 'Đang tạo' do kế toán G lập; G2 là kế toán khác có quyền xem",
         "1. Đăng nhập G2\n2. Mở màn sửa phiếu X bằng liên kết trực tiếp",
         "Phiếu X của G",
         "- Hệ thống từ chối, không mở được màn sửa"),

        ("005", "Xóa bản nháp phiếu xuất giữ", "P0",
         "Kế toán G có phiếu X ở 'Đang tạo'; phiếu yêu cầu cha P đang 'Đang xuất giữ'",
         "1. Bấm nút thùng rác ở cột Hành động\n2. Xác nhận ở cửa sổ hỏi lại\n"
         "3. Kiểm tra 'Danh sách phiếu xuất giữ'\n4. Kiểm tra trạng thái phiếu yêu cầu P",
         "Xóa nháp",
         "- Phiếu X biến mất khỏi lưới\n"
         "⚠️ Phiếu yêu cầu P quay trở lại 'Chờ KT duyệt' và lập lại phiếu xuất giữ được"),

        ("006", "Không xóa được phiếu đã duyệt", "P0",
         "Phiếu X ở 'Đã duyệt', đã sinh lô hàng giữ",
         "1. Xem cột Hành động\n"
         "2. Dùng công cụ kiểm thử gọi thẳng chức năng Xóa, bỏ qua giao diện\n"
         "3. Kiểm tra 'Danh sách hàng giữ'",
         "Phiếu X — Đã duyệt",
         "- Không có nút thùng rác\n- Gọi thẳng chức năng cũng bị từ chối\n"
         "- Lô hàng giữ vẫn còn nguyên"),

        ("007", "Màn xem chi tiết phiếu xuất giữ", "P0",
         "Phiếu X đã duyệt",
         "1. Bấm mã phiếu trên lưới\n2. Quan sát toàn bộ màn xem",
         "Phiếu X",
         "- Có khối 'Thông tin chung' và khối 'Chi tiết'\n"
         "- Bảng Chi tiết có 9 cột: STT · Tên hàng hóa · Model · Mã hàng hóa · Thương hiệu · "
         "SL có thể giữ · SL đề nghị · Đơn vị tính · Hình ảnh tham khảo\n"
         "- Có nút 'Quay lại' cuối trang"),

        ("008", "Nút Duyệt / Không duyệt ở màn xem phiếu xuất giữ", "P1",
         "Xem lần lượt phiếu ở 'Đang tạo' và 'Đã duyệt', với các tài khoản kế toán khác nhau",
         "1. Mở màn xem\n2. Quan sát các nút cuối trang",
         "Mọi trạng thái",
         "⚠️ Ghi nhận thực tế: nút 'Duyệt' và 'Không duyệt' ở màn xem thuộc luồng Ban kiểm soát đã "
         "bị tắt trong hệ thống, nên KHÔNG BAO GIỜ hiện\n"
         "- Chỉ thấy nút 'Sửa' (khi còn nháp và là người lập) và nút 'Quay lại'"),

        ("009", "In đề nghị xuất giữ", "P1",
         "Phiếu X đã duyệt",
         "1. Bấm nút máy in ở cột Hành động\n2. Quan sát bản in",
         "Phiếu X",
         "- Bản in hiện mã phiếu, thông tin khách hàng, người yêu cầu, phòng yêu cầu, "
         "'Giữ đến ngày' và bảng hàng hóa\n- Số lượng in ra khớp với số trên màn xem"),

        ("010", "Mở màn xem phiếu xuất giữ ngoài phạm vi của mình", "P1",
         "Phiếu X thuộc công ty 4. Tài khoản G thuộc công ty 1, không phải người lập",
         "1. Đăng nhập G\n2. Mở màn xem phiếu X bằng liên kết trực tiếp\n3. Ghi nhận kết quả",
         "Phiếu X — công ty 4",
         "- Hệ thống từ chối, báo không có quyền xem\n"
         "- Phiếu X cũng không có trên lưới của G"),
    ]),

    # ------------------------------------------------------------------ X
    ("X", "IN & XUẤT EXCEL DANH SÁCH YÊU CẦU", [
        ("001", "In danh sách yêu cầu xuất giữ", "P1",
         "Đang lọc khoảng ngày 01/03/2026 → 10/03/2026, lưới còn 7 phiếu",
         "1. Bấm nút 'In'\n2. Quan sát trang in",
         "7 phiếu",
         "- Mở tab mới in đúng 7 phiếu đang lọc, khổ ngang\n"
         "- Đầu bản in có dòng 'Từ ngày 01/03/2026 đến ngày 10/03/2026'"),

        ("002", "In danh sách khi không lọc gì", "P2",
         "Không đặt bộ lọc nào",
         "1. Bấm nút 'In'\n2. Quan sát",
         "Không lọc",
         "- In toàn bộ phiếu trong phạm vi quyền của người đang đăng nhập\n"
         "- Không có dòng khoảng ngày ở đầu bản in, hoặc dòng đó để trống"),

        ("003", "Xuất excel danh sách yêu cầu xuất giữ", "P0",
         "Đang lọc Trạng thái = 'Đã duyệt', lưới còn 5 phiếu",
         "1. Bấm nút 'Xuất excel'\n2. Mở file tải về",
         "5 phiếu đã duyệt",
         "- File tải về chứa đúng 5 phiếu đang lọc\n"
         "- Các cột trong file khớp các cột trên lưới"),

        ("004", "Bản in giữ đúng thứ tự và số liệu của lưới", "P1",
         "Lưới đang sắp xếp mặc định",
         "1. Ghi lại 5 dòng đầu trên lưới\n2. Bấm 'In'\n3. So 5 dòng đầu của bản in",
         "5 dòng đầu",
         "- Thứ tự và nội dung 5 dòng đầu của bản in trùng khớp với lưới"),

        ("005", "In khi lưới không có dữ liệu", "P2",
         "Đang lọc điều kiện không ra kết quả nào",
         "1. Bấm 'In'\n2. Quan sát",
         "0 phiếu",
         "- Bản in mở ra với bảng rỗng, có tiêu đề và tiêu đề cột\n- Không báo lỗi hệ thống"),
    ]),

    # ------------------------------------------------------------------ XI
    ("XI", "RÀNG BUỘC NHẬP LIỆU & GIAO DIỆN", [
        ("001", "Định dạng số lượng và tiền trên bảng Chi tiết", "P1",
         "Có dòng hàng đơn giá 1234567.89 và số lượng 1234",
         "1. Quan sát cột Đơn giá, Thành tiền, các cột số lượng",
         "1234567.89 · 1234",
         "- Số hiển thị có dấu ngăn cách hàng nghìn, dễ đọc\n"
         "- Ô không có dữ liệu để TRỐNG, không hiện dấu gạch ngang cũng không hiện 0"),

        ("002", "Ô số lượng chấp nhận số thập phân", "P2",
         "Hàng X bán theo đơn vị lẻ",
         "1. Nhập 'Đề nghị' = 2.5\n2. Bấm 'Lưu'\n3. Mở lại phiếu",
         "2.5",
         "- Ghi nhận CHÍNH XÁC: hệ thống có nhận số thập phân hay làm tròn\n"
         "- Nếu nhận thì bản in và màn xem phải hiện đúng 2.5, không làm tròn thành 3"),

        ("003", "Ô bị khóa phải nhìn ra được là ô khóa", "P1",
         "Màn tạo phiếu xuất giữ",
         "1. Quan sát các ô 'Loại đề nghị', 'Khách hàng', 'Người yêu cầu', 'Phòng yêu cầu'",
         "Các ô chỉ đọc",
         "- Các ô này có dữ liệu và hiển thị mờ, gõ vào không được\n"
         "- Không bị nhầm thành ô trống chưa điền"),

        ("004", "Ô 'Giữ đến ngày' chỉ chọn được bằng lịch", "P2",
         "Màn tạo phiếu yêu cầu",
         "1. Bấm vào ô 'Giữ đến ngày'\n2. Thử gõ tay một chuỗi không phải ngày",
         "Chuỗi 'abcxyz'",
         "- Có lịch bật lên để chọn ngày\n"
         "- Gõ chuỗi sai định dạng thì khi lưu hệ thống báo 'Không hợp lệ'"),

        ("005", "Bấm nút Lưu hai lần liên tiếp", "P0",
         "Đã điền đủ thông tin hợp lệ",
         "1. Bấm 'Lưu'\n2. Bấm 'Lưu' lần nữa ngay lập tức\n3. Vào màn danh sách đếm phiếu",
         "Bấm 2 lần",
         "- Nút bị khóa lại trong lúc đang xử lý\n- Chỉ tạo ra ĐÚNG 1 phiếu, không tạo trùng"),

        ("006", "Ô Ghi chú nhận đúng 255 ký tự", "P2",
         "Đang ở màn tạo",
         "1. Nhập Ghi chú đúng 255 ký tự\n2. Bấm 'Lưu'",
         "255 ký tự",
         "- Lưu thành công, không báo lỗi độ dài\n- Mở lại phiếu thấy đủ nội dung ghi chú"),

        ("007", "Đính kèm file đúng dung lượng giới hạn", "P2",
         "Có file đúng định dạng, dung lượng khoảng 12 MB",
         "1. Đính kèm file đó\n2. Bấm 'Lưu'\n3. Mở lại phiếu, bấm vào file",
         "File 12 MB",
         "- Lưu thành công\n- Bấm vào tên file mở xem được nội dung"),

        ("008", "Bảng nhiều dòng vẫn thao tác được", "P1",
         "Hợp đồng có 50 dòng hàng",
         "1. Chọn hợp đồng đó\n2. Cuộn xuống cuối bảng, tích 'Cần xuất' dòng cuối\n"
         "3. Nhập số lượng và Lưu",
         "50 dòng",
         "- Bảng cuộn được, tiêu đề cột vẫn nhìn thấy khi cuộn\n"
         "- Lưu thành công, mở lại đúng dòng cuối có số lượng"),

        ("009", "Rời trang khi đang điền dở", "P2",
         "Đang điền dở màn tạo, chưa lưu",
         "1. Bấm sang một menu khác\n2. Ghi nhận kết quả",
         "Điền dở",
         "- Ghi nhận CHÍNH XÁC: hệ thống có cảnh báo chưa lưu hay rời đi luôn\n"
         "- Ghi lại kết quả thực tế"),

        ("010", "Cột Hình ảnh tham khảo", "P2",
         "Có hàng đã gắn ảnh và hàng chưa gắn ảnh",
         "1. Quan sát cột 'Hình ảnh tham khảo' của cả hai dòng",
         "Có ảnh · không ảnh",
         "- Dòng có ảnh: hiện ảnh nhỏ đúng của hàng hóa đó\n"
         "- Dòng không ảnh: ô để trống hoặc hiện ảnh mặc định, không vỡ khung bảng"),
    ]),

    # ------------------------------------------------------------------ XII
    ("XII", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", [
        ("001", "Phiếu của công ty khác không lọt sang", "P0",
         "Công ty 1 có 12 phiếu yêu cầu, công ty 4 có 9 phiếu. Tài khoản C chỉ có quyền xem theo "
         "công ty, thuộc công ty 1",
         "1. Đăng nhập C\n2. Vào màn danh sách\n3. Đếm và kiểm tra mã phiếu",
         "12 vs 9",
         "- Chỉ hiện 12 phiếu của công ty 1\n- Không có phiếu nào của công ty 4"),

        ("002", "Phiếu xuất giữ lấy công ty theo người lập phiếu yêu cầu", "P0",
         "Phiếu yêu cầu P do nhân viên A thuộc công ty 1 lập. Kế toán G thuộc công ty 4 lập phiếu "
         "xuất giữ cho P",
         "1. G lập và duyệt phiếu xuất giữ cho P\n"
         "2. Đăng nhập tài khoản chỉ xem được công ty 1, tìm phiếu xuất giữ vừa tạo\n"
         "3. Đăng nhập tài khoản chỉ xem được công ty 4, tìm phiếu đó",
         "Người yêu cầu công ty 1 · người lập công ty 4",
         "⚠️ Phiếu xuất giữ phải thuộc CÔNG TY 1 (theo người lập phiếu yêu cầu), không phải công ty "
         "của kế toán\n- Lô hàng giữ sinh ra cũng thuộc công ty 1"),

        ("003", "Người lập sửa phiếu trong lúc Trưởng phòng đang mở xem", "P1",
         "Phiếu P đang 'Đang tạo', A mở màn sửa; E cũng đang mở màn danh sách",
         "1. A sửa và bấm 'Lưu & Gửi duyệt'\n2. E tải lại màn chờ duyệt",
         "Sửa song song",
         "- E thấy phiếu P xuất hiện trong danh sách chờ duyệt với dữ liệu mới nhất"),

        ("004", "Trưởng phòng duyệt trong lúc người lập đang mở màn sửa", "P0",
         "Phiếu P ở 'Đang tạo', A đang mở màn sửa nhưng chưa lưu. Trong lúc đó phiếu được A gửi "
         "duyệt từ một cửa sổ khác và E đã duyệt",
         "1. Ở cửa sổ cũ, A bấm 'Lưu'\n2. Ghi nhận kết quả",
         "Phiếu đã đổi trạng thái",
         "- Hệ thống từ chối, báo dữ liệu đã thay đổi hoặc không còn quyền sửa\n"
         "- Trạng thái phiếu không bị kéo ngược về 'Đang tạo'"),

        ("005", "Tồn kho thay đổi giữa lúc lập phiếu và lúc duyệt", "P0",
         "Lúc kế toán mở màn tạo, hàng X còn 20. Trước khi bấm duyệt, phiếu khác đã lấy mất 18",
         "1. Kế toán mở màn tạo, cột 'SL có thể giữ' hiện 20\n"
         "2. Chờ tồn kho thay đổi\n3. Bấm 'Duyệt giữ hàng' với số lượng 10",
         "Còn 2 tại thời điểm duyệt",
         "- Hệ thống chặn, báo 'Kho không đủ số lượng. Vui lòng cập nhật lại số liệu!'\n"
         "- Kiểm tra bằng tồn kho tại THỜI ĐIỂM DUYỆT, không phải số hiển thị lúc mở màn"),

        ("006", "Xóa phiếu yêu cầu trong lúc kế toán đang lập phiếu xuất giữ", "P1",
         "Phiếu yêu cầu P đang 'Chờ KT duyệt'. Kế toán G đã mở màn tạo phiếu xuất giữ cho P",
         "1. Người lập A (hoặc quản trị) đưa phiếu P về 'Đang tạo' rồi xóa\n"
         "2. G bấm 'Duyệt giữ hàng'\n3. Ghi nhận kết quả",
         "Phiếu cha biến mất",
         "- Hệ thống báo lỗi rõ ràng, không tạo phiếu xuất giữ mồ côi\n"
         "- Không có lô hàng giữ nào được sinh ra"),

        ("007", "Đổi công ty đang làm việc rồi quay lại màn danh sách", "P2",
         "Tài khoản D có quyền ở nhiều công ty",
         "1. Đang xem danh sách ở công ty 1\n2. Đổi sang công ty 4 trên thanh trên cùng\n"
         "3. Quay lại màn danh sách",
         "Đổi công ty",
         "- Lưới nạp lại theo đúng công ty vừa chọn\n- Không còn phiếu của công ty cũ"),
    ]),

    # ------------------------------------------------------------------ XIII
    ("XIII", "E2E FLOW", [
        ("001", "Luồng đầy đủ 2 cấp duyệt: lập → Trưởng phòng → Kế toán → sinh hàng giữ", "P0",
         "Nhân viên A thuộc phòng Kinh doanh 1, công ty 1. Hàng X còn tồn 50. Hợp đồng hãng HĐ01 của "
         "khách KH001 đã thu 80%, ngưỡng Quy chế công ty là 30%. Hôm nay 05/03/2026",
         "1. A: 'Tạo mới' → loại 'Xuất giữ HĐ hãng' → chọn HĐ01 → 'Giữ đến ngày' 30/03/2026 → "
         "tích hàng X, Đề nghị 10 → 'Lưu & Gửi duyệt'\n"
         "2. E (Trưởng phòng KD1): mở phiếu → 'TP duyệt'\n"
         "3. G (Kế toán): mở phiếu → 'Tạo phiếu xuất giữ' → 'Duyệt giữ hàng'\n"
         "4. Kiểm tra hai màn danh sách và 'Danh sách hàng giữ'",
         "10 hàng X · KH001 · hạn 30/03/2026",
         "- Bước 1: phiếu ở 'Chờ TP duyệt'\n"
         "- Bước 2: báo 'Thao tác thành công!', phiếu sang 'Chờ KT duyệt' (bỏ qua Ban giám đốc vì "
         "đã thu 80%)\n"
         "- Bước 3: phiếu xuất giữ 'Đã duyệt', phiếu yêu cầu 'Đã duyệt'\n"
         "- Bước 4: 'Danh sách hàng giữ' có 1 lô: NHÂN VIÊN A giữ 10 hàng X cho KH001, "
         "bắt đầu 05/03/2026, hạn 30/03/2026"),

        ("002", "Luồng đầy đủ 3 cấp duyệt có Ban giám đốc", "P0",
         "Như trên nhưng hợp đồng HĐ02 mới thu 10%, dưới ngưỡng 30%",
         "1. A lập phiếu với HĐ02, 'Giữ đến ngày' 30/03/2026, 'Lưu & Gửi duyệt'\n"
         "2. E: 'TP duyệt'\n3. F (Ban giám đốc): đổi 'Giữ đến ngày' thành 20/03/2026 → 'BGĐ duyệt'\n"
         "4. G: 'Tạo phiếu xuất giữ' → 'Duyệt giữ hàng'\n5. Kiểm tra 'Danh sách hàng giữ'",
         "Đã thu 10% < ngưỡng 30%",
         "- Bước 2: báo 'Yêu cầu đã được chuyển đến BGĐ', phiếu sang 'Chờ BGĐ duyệt'\n"
         "- Bước 3: phiếu sang 'Chờ KT duyệt', 'Giữ đến ngày' đổi thành 20/03/2026\n"
         "- Bước 5: lô hàng giữ có hạn 20/03/2026 theo ngày Ban giám đốc nhập lại"),

        ("003", "Luồng loại 'Xuất giữ khác' từ đầu đến cuối", "P0",
         "Nhân viên A, khách KH001, hàng X tồn 50, đơn vị 'Thùng' hệ số 10. Ngưỡng 'Giá trị giữ hàng "
         "khác' là 50,000,000; tổng phiếu chỉ 20,000,000",
         "1. A: 'Tạo mới' → loại 'Xuất giữ khác' → chọn KH001 → 'Giữ đến ngày' 30/03/2026 → "
         "nhập Ghi chú → đính kèm 1 file → thêm hàng X, đơn vị 'Thùng', Đề nghị 2 → 'Lưu & Gửi duyệt'\n"
         "2. E: 'TP duyệt'\n3. G: 'Tạo phiếu xuất giữ' → 'Duyệt giữ hàng'\n"
         "4. Kiểm tra 'Danh sách hàng giữ'",
         "2 thùng = 20 đơn vị gốc",
         "- Bước 2: phiếu đi thẳng 'Chờ KT duyệt' vì dưới ngưỡng\n"
         "- Bước 4: lô hàng giữ ghi 20, không phải 2\n"
         "- Người giữ là A, khách hàng KH001, hạn 30/03/2026"),

        ("004", "Luồng bị trả về, sửa lại rồi duyệt tiếp", "P0",
         "Nhân viên A, hàng X tồn 50",
         "1. A lập phiếu xin 30 hàng X, gửi duyệt\n"
         "2. E: 'Không duyệt', ghi chú 'Giảm còn 10'\n"
         "3. A: mở phiếu đọc ghi chú, sửa Đề nghị thành 10, 'Lưu & Gửi duyệt'\n"
         "4. E: 'TP duyệt'\n5. G: 'Tạo phiếu xuất giữ' → 'Duyệt giữ hàng'\n"
         "6. Kiểm tra 'Danh sách hàng giữ'",
         "30 → bị trả → 10",
         "- Bước 2: phiếu về 'Đang tạo', A thấy ghi chú 'Giảm còn 10'\n"
         "- Bước 3: sửa được, phiếu về 'Chờ TP duyệt'\n"
         "- Bước 6: lô hàng giữ chỉ có 10, không phải 30"),

        ("005", "Luồng kế toán lưu nháp rồi xóa, phiếu yêu cầu quay lại chờ duyệt", "P0",
         "Phiếu yêu cầu P đang 'Chờ KT duyệt'",
         "1. G: 'Tạo phiếu xuất giữ' → bấm 'Lưu'\n2. Kiểm tra trạng thái phiếu P\n"
         "3. Kiểm tra 'Danh sách hàng giữ'\n4. G: xóa phiếu xuất giữ nháp\n"
         "5. Kiểm tra lại trạng thái phiếu P\n6. G: lập lại phiếu xuất giữ và 'Duyệt giữ hàng'",
         "Nháp → xóa → lập lại",
         "- Bước 2: phiếu P ở 'Đang xuất giữ'\n"
         "- Bước 3: chưa có lô hàng giữ nào\n"
         "- Bước 5: phiếu P quay lại 'Chờ KT duyệt'\n"
         "- Bước 6: lập lại được, lô hàng giữ sinh ra bình thường"),

        ("006", "Luồng kế toán cắt giảm số lượng khi tồn kho không đủ", "P0",
         "Phiếu yêu cầu P xin 30 hàng X, nhưng tồn kho khả dụng chỉ còn 12",
         "1. G: 'Tạo phiếu xuất giữ' → giữ nguyên 30 → 'Duyệt giữ hàng'\n2. Đọc thông báo\n"
         "3. G: sửa 'SL đề nghị' thành 12 → 'Duyệt giữ hàng'\n4. Kiểm tra 'Danh sách hàng giữ'",
         "Xin 30 · tồn 12",
         "- Bước 1: bị chặn, báo 'Kho không đủ số lượng. Vui lòng cập nhật lại số liệu!'\n"
         "- Bước 3: duyệt thành công\n"
         "- Bước 4: lô hàng giữ có 12, phiếu yêu cầu P sang 'Đã duyệt'"),

        ("007", "Luồng nhiều dòng hàng, kế toán bỏ bớt một dòng", "P0",
         "Phiếu yêu cầu P có 3 dòng: hàng X 10, hàng Y 5, hàng Z 8. Cả ba đều đủ tồn",
         "1. Duyệt phiếu P qua Trưởng phòng\n"
         "2. G: 'Tạo phiếu xuất giữ' → bỏ tích 'Cần xuất' dòng hàng Y → sửa hàng Z còn 6 → "
         "'Duyệt giữ hàng'\n3. Kiểm tra 'Danh sách hàng giữ'",
         "X 10 · Y bỏ · Z 6",
         "- Sinh 2 lô: hàng X 10 và hàng Z 6\n- Không có lô nào cho hàng Y\n"
         "- Phiếu yêu cầu P vẫn sang 'Đã duyệt'"),

        ("008", "Luồng giữ nhiều đợt cho cùng khách, cùng hạn", "P0",
         "Nhân viên A, khách KH001, hàng X tồn 50",
         "1. A lập và duyệt xong phiếu 1: giữ 5 hàng X cho KH001 hạn 30/03/2026\n"
         "2. Kiểm tra 'Danh sách hàng giữ'\n"
         "3. A lập và duyệt xong phiếu 2: giữ 7 hàng X cho KH001 cũng hạn 30/03/2026\n"
         "4. Kiểm tra lại 'Danh sách hàng giữ'",
         "5 + 7 = 12",
         "- Bước 2: A có 1 dòng hàng X số lượng 5\n"
         "- Bước 4: vẫn chỉ MỘT dòng, số lượng 12 — cộng dồn, không tạo dòng mới"),

        ("009", "Luồng hai nhân viên giữ cùng một hàng cho cùng khách", "P1",
         "Nhân viên A và nhân viên B cùng công ty, hàng X tồn 50, khách KH001",
         "1. A lập và duyệt xong phiếu giữ 10 hàng X cho KH001 hạn 30/03/2026\n"
         "2. B lập và duyệt xong phiếu giữ 8 hàng X cho KH001 cũng hạn 30/03/2026\n"
         "3. Kiểm tra 'Danh sách hàng giữ'",
         "A 10 · B 8",
         "- Có HAI dòng riêng, mỗi người một dòng\n"
         "- Không cộng gộp vì người giữ khác nhau"),

        ("010", "Luồng hàng giữ sinh ra dùng được cho các nghiệp vụ giữ hàng khác", "P0",
         "Đã duyệt xong phiếu xuất giữ, A đang giữ 10 hàng X cho KH001 hạn 30/03/2026",
         "1. Vào màn 'Phiếu Yêu cầu gia hạn giữ hàng', A lập phiếu gia hạn cho lô này\n"
         "2. Vào màn 'Phiếu Yêu cầu điều chuyển hàng giữ', mở cửa sổ chọn hàng\n"
         "3. Vào màn 'Phiếu Yêu cầu hủy hàng giữ', mở cửa sổ chọn hàng",
         "Lô hàng giữ vừa sinh",
         "- Cả ba màn đều nhìn thấy lô 10 hàng X của A cho KH001\n"
         "- Cột Hợp đồng của lô hiển thị đúng hợp đồng gốc (nếu phiếu yêu cầu có gắn hợp đồng)\n"
         "⚠️ Đây là bước xác nhận phiếu xuất giữ đã ghi kho hàng giữ đúng chuẩn"),

        ("011", "Luồng phiếu bị Ban giám đốc trả về phải duyệt lại từ đầu", "P1",
         "Phiếu P đã qua Trưởng phòng, đang 'Chờ BGĐ duyệt'",
         "1. F: 'Không duyệt', ghi chú 'Không đồng ý'\n2. Kiểm tra trạng thái\n"
         "3. A: sửa lại và 'Lưu & Gửi duyệt'\n4. Kiểm tra ai nhìn thấy phiếu ở màn chờ duyệt",
         "Trả về từ cấp Ban giám đốc",
         "- Bước 2: phiếu về 'Đang tạo', KHÔNG về 'Chờ TP duyệt'\n"
         "- Bước 4: Trưởng phòng E lại thấy phiếu, phải duyệt lại từ cấp 1"),

        ("012", "Luồng đối chiếu bản in với dữ liệu trên màn hình", "P1",
         "Phiếu đã duyệt xong toàn bộ",
         "1. In yêu cầu từ màn 'Danh sách yêu cầu xuất giữ'\n"
         "2. In đề nghị từ màn 'Danh sách phiếu xuất giữ'\n"
         "3. So từng ô với màn xem chi tiết và với 'Danh sách hàng giữ'",
         "2 bản in",
         "- Số lượng, đơn vị tính, khách hàng, hạn giữ trên hai bản in khớp nhau và khớp màn hình\n"
         "- Tên người yêu cầu trên bản in đề nghị là người lập phiếu yêu cầu, không phải kế toán"),
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
