# -*- coding: utf-8 -*-
"""Generate testcase Excel cho man ERP: Bao cao phan chia thi truong.

Viet cho MAN ERP GOC (TanPhatDev, route division_market_report.*), de tester nam luong
truoc khi nghiem thu ban HRM da port (presale-division-market-report).

Chay:  python gen_testcase.py
Output: testcase - Bao cao phan chia thi truong.xlsx (cung thu muc)
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

OUTPUT_FILE = os.path.join(HERE, "testcase - Bao cao phan chia thi truong.xlsx")
FEATURE_NAME = "Báo cáo phân chia thị trường (ERP)"
MODULE_NAME = "Kinh doanh - Báo cáo thị trường"

# =========================================================================
# 9 MUC MO TA
# =========================================================================
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Báo cáo cho biết mỗi Tỉnh/TP, mỗi Phường/Xã đang do PHÒNG BAN nào và NHÂN VIÊN nào phụ trách, "
     "kèm số điện thoại nhân viên và hãng xe nhân viên đó phụ trách. Màn chỉ để xem, không thêm/sửa/xóa.\n"
     "Đường vào: menu Kinh doanh > Báo cáo thị trường > 'Báo cáo phân chia thị trường'.\n"
     "Dữ liệu của báo cáo được sinh ra từ 2 màn nhập liệu (cùng nằm ở menu Kinh doanh > Kế hoạch):\n"
     "- 'Phiếu phân chia thị trường theo phòng ban': giao tỉnh/xã cho phòng ban.\n"
     "- 'Phiếu phân chia thị trường theo nhân viên': phòng ban chia tiếp tỉnh/xã cho từng nhân viên, "
     "tích 'Phụ trách tất cả các hãng' hoặc chọn hãng xe cụ thể."),

    ("2. Đối tượng được tính / hiển thị",
     "Một dòng báo cáo xuất hiện khi thỏa ĐỦ cả 3 điều kiện:\n"
     "- Phòng ban được giao tỉnh/xã đó trên một phiếu phân chia theo phòng ban ĐÃ DUYỆT.\n"
     "- Phòng ban đó có phiếu phân chia theo nhân viên ĐÃ DUYỆT.\n"
     "- Trên phiếu theo nhân viên, nhân viên được giao ĐÚNG tỉnh và ĐÚNG xã đó.\n"
     "Mỗi nhân viên phụ trách một xã là một dòng."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu phân chia (phòng ban hoặc nhân viên) đang tạo / chờ duyệt: không lên báo cáo.\n"
     "- Xã phòng ban được giao nhưng KHÔNG có nhân viên nào của phòng phụ trách: không hiện dòng nào "
     "(không có dòng 'phòng có, nhân viên trống').\n"
     "- Nhân viên được giao tỉnh/xã nằm ngoài phạm vi phòng ban của mình: không hiện.\n"
     "- Danh sách chọn ở ô Tỉnh/TP và Phường/Xã lấy TOÀN BỘ danh mục địa lý đang hoạt động, không chỉ "
     "nơi đã phân chia, nên chọn tỉnh/xã chưa phân chia sẽ ra 'Chưa có dữ liệu' - đúng, không phải lỗi."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Màn KHÔNG có bộ lọc thời gian. Báo cáo luôn phản ánh tình trạng phân chia hiện tại theo các phiếu "
     "đã duyệt.\n"
     "Màn không tự tải dữ liệu khi mở: phải bấm 'Lọc' mới có số liệu."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Bảng gộp ô 4 cấp: Tỉnh/TP > Phường/Xã > Phòng phụ trách > Nhân viên phụ trách.\n"
     "8 cột: STT · Tỉnh/TP · Phường/Xã · Phòng phụ trách · Nhân viên phụ trách · Số điện thoại · "
     "Phụ trách tất cả các hãng · Hãng xe phụ trách.\n"
     "STT đánh theo TỈNH (không theo dòng), liên tục qua các trang.\n"
     "Phân trang: 15 TỈNH mỗi trang (không phải 15 dòng). Một tỉnh lớn có thể có hàng nghìn dòng."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Cột 'Hãng xe phụ trách': gom tên các hãng của nhân viên ở xã đó, ngăn bằng dấu phẩy, bỏ trùng.\n"
     "- Cột 'Phụ trách tất cả các hãng': hiện chữ X khi nhân viên được tích 'Phụ trách tất cả các hãng' "
     "cho xã đó; để trống khi không tích.\n"
     "- Cột 'Số điện thoại' lấy số điện thoại HIỆN TẠI trong hồ sơ nhân viên, không lấy số ghi trên phiếu."),

    ("7. Phân quyền cấp",
     "Màn ERP KHÔNG kiểm quyền: mọi tài khoản đăng nhập được đều mở được màn, thấy toàn bộ dữ liệu của "
     "mọi công ty, mọi phòng ban. Không có giới hạn theo công ty / phòng ban của người xem.\n"
     "(Bản chuyển sang HRM sẽ thêm quyền riêng 'Xem báo cáo phân chia thị trường' - không thuộc phạm vi "
     "bộ testcase này.)"),

    ("8. Cách tính các ô thống kê",
     "Màn không có ô tổng / ô thống kê. Số trang = số tỉnh thỏa bộ lọc chia cho 15, làm tròn lên.\n"
     "Ô 'Phụ trách hãng' lọc theo cột 'Phụ trách tất cả các hãng': Có = chỉ dòng có X; Không = chỉ dòng "
     "trống X; Tất cả = không lọc."),

    ("9. Ghi chú đọc bảng",
     "Các lỗi ERP ĐÃ BIẾT, đã viết thành testcase với kết quả mong đợi ĐÚNG - khi chạy thấy hiện tượng "
     "lỗi như mô tả thì ghi Failed và chép câu 'Lỗi ERP đã biết' vào cột Ghi chú:\n"
     "(1) Lọc 'Phụ trách hãng = Có' luôn ra 'Chưa có dữ liệu'; '= Không' ra toàn bộ, kể cả dòng có X.\n"
     "(2) Chọn từ 2 Khu vực trở lên: chỉ khu vực chọn ĐẦU TIÊN có tác dụng.\n"
     "(3) Mỗi trang 15 tỉnh có thể tới hàng chục nghìn dòng: trang tải rất chậm, trình duyệt có thể treo.\n"
     "(4) Đổi Quốc gia / Phòng phụ trách nhiều lần: danh sách Khu vực / Nhân viên bị thu hẹp chồng lên "
     "nhau, không tự khôi phục; nút làm mới cũng không khôi phục, phải tải lại trang.\n"
     "(5) In / Xuất excel không giới hạn số dòng.\n"
     "(6) Cùng một nhân viên - xã, nếu có nhiều phiếu theo nhân viên đã duyệt với lựa chọn khác nhau, "
     "chữ X có thể hiện hoặc không một cách ngẫu nhiên.\n"
     "Ghi nhận dữ liệu hiện tại: CHƯA có nhân viên nào được chọn hãng xe cụ thể, nên cột 'Hãng xe phụ "
     "trách' trống và lọc theo Hãng xe ra 'Chưa có dữ liệu' - đúng với dữ liệu, không phải lỗi."),
]

# =========================================================================
# SECTION PHAN QUYEN
# =========================================================================
ROLE_TCS = [
    ("00", "Tài khoản kinh doanh thông thường mở được màn từ menu", "P0",
     "Tài khoản A là nhân viên kinh doanh, không có quyền quản lý đặc biệt",
     "1. Đăng nhập ERP bằng tài khoản A\n"
     "2. Vào menu Kinh doanh > Báo cáo thị trường > 'Báo cáo phân chia thị trường'",
     "Tài khoản: A",
     "- Màn mở được, tiêu đề trang 'Báo cáo phân chia thị trường'\n"
     "- Không có thông báo thiếu quyền"),

    ("01", "Màn không giới hạn dữ liệu theo công ty của người xem", "P0",
     "Tài khoản B thuộc công ty 1. Có phòng ban của công ty khác (công ty 4) đã được phân chia thị "
     "trường và phiếu đã duyệt",
     "1. Đăng nhập bằng tài khoản B\n2. Mở màn, bấm 'Lọc' không chọn bộ lọc nào\n"
     "3. Tìm dòng có phòng phụ trách thuộc công ty 4",
     "Tài khoản: B (công ty 1)",
     "- Vẫn thấy dòng của phòng ban công ty 4\n"
     "- Màn không có ô lọc Công ty; dữ liệu của mọi công ty hiển thị chung"),

    ("02", "Màn không giới hạn dữ liệu theo phòng ban của người xem", "P1",
     "Tài khoản C thuộc phòng Kinh doanh 1. Phòng Kinh doanh 2 có dữ liệu phân chia đã duyệt",
     "1. Đăng nhập bằng tài khoản C\n2. Ô 'Phòng phụ trách' chọn phòng Kinh doanh 2\n3. Bấm 'Lọc'",
     "Tài khoản: C",
     "- Hiện đầy đủ dữ liệu của phòng Kinh doanh 2\n"
     "- Danh sách 'Phòng phụ trách' liệt kê mọi phòng ban, không chỉ phòng của C"),

    ("03", "Mở thẳng đường dẫn khi chưa đăng nhập", "P1",
     "Đã đăng xuất ERP. Có sẵn đường dẫn của màn báo cáo",
     "1. Dán đường dẫn màn báo cáo vào trình duyệt\n2. Quan sát",
     "Đường dẫn màn báo cáo",
     "- Hệ thống chuyển về trang đăng nhập\n"
     "- Đăng nhập xong vào lại được màn báo cáo"),

    ("04", "Đường dẫn In / Xuất excel cũng không kiểm quyền", "P2",
     "Tài khoản A (không quyền quản lý). Đã mở màn",
     "1. Bấm 'In'\n2. Quay lại, bấm 'Xuất excel'",
     "Tài khoản: A",
     "- In mở được bản in, Xuất excel tải được file\n"
     "- Nội dung gồm dữ liệu của mọi công ty, mọi phòng ban (đúng với thiết kế ERP: không kiểm quyền)"),
]

# =========================================================================
# CAC SECTION CHUC NANG
# =========================================================================
SECTIONS = [
    ("I", "Giao diện & mở màn", [
        ("001", "Bố cục màn hình khi mở", "P0",
         "Đã đăng nhập ERP",
         "1. Vào menu Kinh doanh > Báo cáo thị trường > 'Báo cáo phân chia thị trường'\n"
         "2. Quan sát toàn bộ màn hình",
         "",
         "- Tiêu đề trang: 'Báo cáo phân chia thị trường'\n"
         "- Khối 'Thông tin chung' có 8 ô lọc: Quốc gia · Khu vực · Tỉnh/TP · Phường/Xã · Phụ trách hãng · "
         "Phòng phụ trách · Nhân viên phụ trách · Hãng xe\n"
         "- Góc phải có 4 nút: 'Lọc' · 'In' · 'Xuất excel' · nút làm mới (biểu tượng mũi tên xoay vòng)\n"
         "- Khối bảng bên dưới và thanh phân trang"),

        ("002", "Màn không tự tải dữ liệu khi mở", "P0",
         "Đã đăng nhập ERP",
         "1. Mở màn báo cáo\n2. Chưa bấm gì, quan sát bảng",
         "",
         "- Bảng hiện một dòng 'Chưa có dữ liệu'\n"
         "- Thanh phân trang không có số trang\n"
         "- Chỉ khi bấm 'Lọc' bảng mới có số liệu"),

        ("003", "Giá trị mặc định của các ô lọc", "P1",
         "Mở màn lần đầu",
         "1. Quan sát giá trị từng ô lọc",
         "",
         "- Ô 'Quốc gia' đã chọn sẵn 'Việt Nam'\n"
         "- Ô 'Phụ trách hãng' hiện 'Tất cả'\n"
         "- Các ô còn lại để trống"),

        ("004", "Tiêu đề 8 cột của bảng", "P0",
         "Đã mở màn",
         "1. Đọc dòng tiêu đề bảng từ trái sang phải",
         "",
         "- Đúng thứ tự: STT · Tỉnh/TP · Phường/Xã · Phòng phụ trách · Nhân viên phụ trách · Số điện thoại · "
         "Phụ trách tất cả các hãng · Hãng xe phụ trách"),

        ("005", "Các lựa chọn của ô 'Phụ trách hãng'", "P2",
         "Đã mở màn",
         "1. Bấm mở ô 'Phụ trách hãng'",
         "",
         "- Có đúng 3 lựa chọn: Tất cả · Có · Không\n- Chỉ chọn được một lựa chọn"),

        ("006", "Trạng thái đang tải dữ liệu", "P2",
         "Đã mở màn",
         "1. Bấm 'Lọc' không chọn bộ lọc\n2. Quan sát ngay trong lúc chờ",
         "",
         "- Bảng hiện dòng 'Đang tải dữ liệu' có biểu tượng quay\n"
         "- Nút 'Lọc' bị khóa, biểu tượng phễu đổi thành biểu tượng quay\n"
         "- Tải xong nút 'Lọc' mở lại"),

        ("007", "Tiêu đề bảng dính khi cuộn", "P2",
         "Đã lọc ra dữ liệu nhiều dòng",
         "1. Cuộn bảng xuống dưới\n2. Cuộn ngang bảng",
         "",
         "- Dòng tiêu đề cột luôn dính ở đầu bảng khi cuộn dọc\n"
         "- Bảng có thanh cuộn riêng, không làm vỡ bố cục trang"),

        ("008", "Không có ô lọc nào bắt buộc", "P1",
         "Đã mở màn, để trống mọi ô trừ Quốc gia mặc định",
         "1. Bấm 'Lọc'",
         "",
         "- Không có thông báo bắt buộc nhập\n- Bảng ra dữ liệu của toàn bộ tỉnh đã phân chia"),

        ("009", "Dòng 'Đang tải' và 'Chưa có dữ liệu' phủ đủ chiều rộng bảng", "P2",
         "Đã mở màn",
         "1. Quan sát dòng 'Chưa có dữ liệu'\n2. Bấm 'Lọc', quan sát dòng 'Đang tải dữ liệu'",
         "",
         "- Hai dòng thông báo trải hết cả 8 cột\n"
         "- Ghi nhận: nếu dòng chỉ phủ 7 cột, chừa trống cột cuối - lỗi hiển thị nhỏ"),
    ]),

    ("II", "Cấu trúc bảng & hiển thị dữ liệu", [
        ("001", "Bảng gộp ô 4 cấp Tỉnh > Xã > Phòng > Nhân viên", "P0",
         "Tỉnh T có 2 xã X1, X2. Xã X1 do phòng P1 phụ trách với 2 nhân viên NV1, NV2. Xã X2 do phòng P1 "
         "(NV1) và phòng P2 (NV3) phụ trách. Mọi phiếu đã duyệt",
         "1. Ô 'Tỉnh/TP' chọn tỉnh T\n2. Bấm 'Lọc'\n3. Quan sát cách gộp ô",
         "Tỉnh T",
         "- Ô STT và ô Tỉnh/TP gộp dọc cho toàn bộ 4 dòng của tỉnh T\n"
         "- Ô X1 gộp 2 dòng (NV1, NV2), ô X2 gộp 2 dòng (P1-NV1, P2-NV3)\n"
         "- Ô phòng P1 dưới X1 gộp 2 dòng\n"
         "- Mỗi nhân viên một dòng riêng với Số điện thoại, cột X, Hãng xe"),

        ("002", "STT đánh theo tỉnh và liên tục qua trang", "P0",
         "Có ít nhất 16 tỉnh đã phân chia",
         "1. Bấm 'Lọc' không chọn bộ lọc\n2. Quan sát cột STT trang 1\n3. Chuyển sang trang 2",
         "",
         "- Trang 1: STT chạy 1 đến 15, mỗi số ứng với một tỉnh (không đánh theo dòng)\n"
         "- Trang 2: STT bắt đầu từ 16"),

        ("003", "Thứ tự sắp xếp tỉnh và phòng", "P2",
         "Có nhiều tỉnh, nhiều phòng phụ trách",
         "1. Bấm 'Lọc'\n2. Quan sát thứ tự tỉnh và thứ tự phòng trong một xã",
         "",
         "- Tỉnh xếp theo thứ tự trong danh mục Tỉnh/TP, KHÔNG theo bảng chữ cái\n"
         "- Phòng trong cùng xã xếp theo thứ tự danh mục phòng ban"),

        ("004", "Cột Số điện thoại lấy theo hồ sơ nhân viên hiện tại", "P1",
         "Nhân viên NV1 đang phụ trách một xã. Số điện thoại trong hồ sơ NV1 là 0912000111",
         "1. Lọc theo nhân viên NV1\n2. Đọc cột Số điện thoại\n"
         "3. Sửa số điện thoại hồ sơ NV1 thành 0912000222\n4. Lọc lại",
         "NV1",
         "- Bước 2: hiện 0912000111\n- Bước 4: hiện 0912000222, không phải số cũ"),

        ("005", "Cột 'Phụ trách tất cả các hãng' hiện chữ X", "P0",
         "Trên phiếu phân chia theo nhân viên đã duyệt: NV1 được tích 'Phụ trách tất cả các hãng' ở xã X1; "
         "NV2 không tích ở xã X1",
         "1. Lọc theo xã X1\n2. Đọc cột 'Phụ trách tất cả các hãng'",
         "Xã X1",
         "- Dòng NV1 hiện chữ X, căn giữa\n- Dòng NV2 để trống"),

        ("006", "Chữ X ổn định khi nhân viên có nhiều phiếu đã duyệt", "P2",
         "Phòng P1 có 2 phiếu phân chia theo nhân viên đều đã duyệt. Phiếu 1 tích 'Phụ trách tất cả các "
         "hãng' cho NV1 ở xã X1, phiếu 2 không tích",
         "1. Lọc theo xã X1 và nhân viên NV1\n2. Bấm 'Lọc' lại 3 lần, mỗi lần đọc cột X",
         "Xã X1, NV1",
         "- NV1 hiện MỘT dòng ở xã X1, chữ X hiện ổn định ở cả 3 lần\n"
         "- Lỗi ERP đã biết: chữ X có thể hiện hoặc không tùy lần, do hệ thống lấy ngẫu nhiên một trong "
         "hai phiếu"),

        ("007", "Cột 'Hãng xe phụ trách'", "P1",
         "Có nhân viên được chọn hãng xe cụ thể (nếu dữ liệu hiện tại chưa có thì lập một phiếu theo nhân "
         "viên, chọn 2 hãng cho một xã rồi duyệt)",
         "1. Lọc theo nhân viên đó\n2. Đọc cột 'Hãng xe phụ trách'",
         "Hãng xe H1, H2",
         "- Hiện 'H1,H2', ngăn bằng dấu phẩy, không lặp tên\n"
         "- Ghi nhận: với dữ liệu hiện tại chưa ai được chọn hãng nên cột trống ở mọi dòng - đúng"),

        ("008", "Chỉ phiếu đã duyệt mới lên báo cáo", "P0",
         "Phòng P3 có phiếu phân chia theo phòng ban đang ở trạng thái chờ duyệt, giao tỉnh T3",
         "1. Lọc theo phòng P3\n2. Duyệt phiếu phân chia theo phòng ban của P3\n"
         "3. Lập + duyệt phiếu phân chia theo nhân viên cho P3, giao tỉnh T3 cho NV5\n4. Lọc lại",
         "Phòng P3",
         "- Bước 1: 'Chưa có dữ liệu'\n"
         "- Bước 2 xong lọc lại vẫn 'Chưa có dữ liệu' (chưa có phiếu theo nhân viên)\n"
         "- Bước 4: hiện tỉnh T3 với NV5"),

        ("009", "Xã không có nhân viên phụ trách thì không hiện", "P1",
         "Phòng P1 được giao xã X9 trên phiếu theo phòng ban, nhưng không nhân viên nào của P1 được giao X9",
         "1. Lọc theo xã X9",
         "Xã X9",
         "- 'Chưa có dữ liệu'\n"
         "- Không có dòng hiện phòng P1 với cột nhân viên để trống"),

        ("010", "Nhân viên giao ngoài phạm vi phòng ban thì không hiện", "P1",
         "Phòng P1 chỉ được giao tỉnh T1. Phiếu theo nhân viên của P1 giao NV1 thêm xã thuộc tỉnh T2",
         "1. Lọc theo nhân viên NV1",
         "NV1",
         "- Chỉ hiện các xã thuộc tỉnh T1\n- Xã thuộc tỉnh T2 không xuất hiện"),

        ("011", "Tên có ký tự đặc biệt hiển thị đúng", "P2",
         "Có phòng ban tên chứa ký tự '&' (vd 'Kinh doanh & Dự án')",
         "1. Lọc theo phòng đó",
         "",
         "- Tên phòng hiển thị đầy đủ, đúng ký tự '&'"),
    ]),

    ("III", "Bộ lọc Quốc gia / Khu vực / Tỉnh / Xã", [
        ("001", "Quốc gia mặc định không giới hạn dữ liệu", "P1",
         "Mở màn, ô Quốc gia đang là 'Việt Nam'",
         "1. Bấm 'Lọc'",
         "Quốc gia: Việt Nam",
         "- Ra toàn bộ tỉnh đã phân chia"),

        ("002", "Chọn quốc gia khác", "P2",
         "Danh mục có quốc gia khác Việt Nam và có tỉnh thuộc quốc gia đó",
         "1. Ô Quốc gia chọn quốc gia khác\n2. Bấm 'Lọc'",
         "",
         "- Chỉ hiện tỉnh thuộc quốc gia đã chọn\n"
         "- Thường ra 'Chưa có dữ liệu' vì chỉ phân chia trong nước - đúng"),

        ("003", "Đổi quốc gia nhiều lần, danh sách Khu vực phải theo quốc gia mới", "P2",
         "Danh mục có ít nhất 2 quốc gia có khu vực",
         "1. Ô Quốc gia chọn quốc gia A, mở ô Khu vực\n"
         "2. Đổi Quốc gia sang quốc gia B, mở lại ô Khu vực\n3. Đổi về Việt Nam, mở ô Khu vực",
         "",
         "- Bước 1: chỉ khu vực của A\n- Bước 2: chỉ khu vực của B\n- Bước 3: đủ 8 khu vực của Việt Nam\n"
         "- Lỗi ERP đã biết: từ bước 2 danh sách Khu vực trống, không khôi phục, phải tải lại trang"),

        ("004", "Lọc theo 1 khu vực", "P0",
         "Khu vực 'Đồng bằng sông Hồng' có tỉnh đã phân chia",
         "1. Ô Khu vực chọn 'Đồng bằng sông Hồng'\n2. Bấm 'Lọc'",
         "Khu vực: Đồng bằng sông Hồng",
         "- Chỉ hiện tỉnh thuộc Đồng bằng sông Hồng"),

        ("005", "Lọc theo 2 khu vực", "P1",
         "Cả 'Đồng bằng sông Hồng' và 'Đông Nam Bộ' đều có tỉnh đã phân chia",
         "1. Ô Khu vực chọn 'Đồng bằng sông Hồng' rồi chọn thêm 'Đông Nam Bộ'\n2. Bấm 'Lọc'",
         "2 khu vực",
         "- Hiện tỉnh của CẢ HAI khu vực\n"
         "- Lỗi ERP đã biết: chỉ hiện tỉnh của khu vực chọn đầu tiên (Đồng bằng sông Hồng)"),

        ("006", "Chọn khu vực làm ô Tỉnh/TP thu hẹp và xóa tỉnh đã chọn", "P1",
         "Ô Tỉnh/TP đang chọn 'Hà Nội'",
         "1. Ô Khu vực chọn 'Đông Nam Bộ'\n2. Quan sát ô Tỉnh/TP và mở danh sách",
         "",
         "- 'Hà Nội' bị bỏ chọn\n- Danh sách Tỉnh/TP chỉ còn tỉnh thuộc Đông Nam Bộ"),

        ("007", "Bỏ hết khu vực thì ô Tỉnh/TP hiện lại toàn bộ", "P2",
         "Ô Khu vực đang chọn 1 khu vực",
         "1. Bỏ chọn khu vực đó\n2. Mở danh sách Tỉnh/TP",
         "",
         "- Danh sách Tỉnh/TP hiện lại đủ tỉnh của mọi khu vực"),

        ("008", "Lọc theo 1 tỉnh", "P0",
         "Tỉnh 'Hà Nội' đã phân chia",
         "1. Ô Tỉnh/TP chọn 'Hà Nội'\n2. Bấm 'Lọc'",
         "Tỉnh: Hà Nội",
         "- Chỉ hiện Hà Nội, STT = 1\n- Thanh phân trang chỉ 1 trang"),

        ("009", "Lọc theo nhiều tỉnh", "P0",
         "Hà Nội và Hải Phòng đều đã phân chia",
         "1. Ô Tỉnh/TP chọn 'Hà Nội' và 'Hải Phòng'\n2. Bấm 'Lọc'",
         "2 tỉnh",
         "- Hiện đúng 2 tỉnh, STT 1 và 2"),

        ("010", "Chọn tỉnh làm ô Phường/Xã thu hẹp theo tỉnh", "P1",
         "Mở màn",
         "1. Ô Tỉnh/TP chọn 'Hà Nội'\n2. Mở danh sách Phường/Xã\n3. Bỏ chọn tỉnh, mở lại Phường/Xã",
         "",
         "- Bước 2: chỉ còn phường/xã thuộc Hà Nội\n- Bước 3: hiện lại toàn bộ phường/xã"),

        ("011", "Lọc theo 1 phường/xã", "P0",
         "Xã X1 thuộc tỉnh T đã có nhân viên phụ trách",
         "1. Ô Tỉnh/TP chọn tỉnh T\n2. Ô Phường/Xã chọn X1\n3. Bấm 'Lọc'",
         "Xã X1",
         "- Chỉ hiện tỉnh T với một xã X1\n- Đủ các phòng và nhân viên phụ trách X1"),

        ("012", "Tỉnh và xã không khớp nhau", "P2",
         "Mở màn",
         "1. Ô Phường/Xã chọn một xã thuộc Hà Nội\n2. Ô Tỉnh/TP chọn 'Hải Phòng'\n3. Bấm 'Lọc'",
         "",
         "- 'Chưa có dữ liệu' (các ô lọc kết hợp theo kiểu cùng thỏa)\n- Không báo lỗi hệ thống"),

        ("013", "Chọn tỉnh chưa được phân chia", "P2",
         "Có tỉnh trong danh mục chưa phòng nào được giao",
         "1. Ô Tỉnh/TP chọn tỉnh đó\n2. Bấm 'Lọc'",
         "",
         "- 'Chưa có dữ liệu', đúng vì danh sách chọn lấy toàn bộ danh mục"),
    ]),

    ("IV", "Bộ lọc Phụ trách hãng / Phòng / Nhân viên / Hãng xe", [
        ("001", "Phụ trách hãng = Có", "P0",
         "Có dòng hiện chữ X ở cột 'Phụ trách tất cả các hãng' (kiểm bằng cách lọc 'Tất cả' trước)",
         "1. Ô 'Phụ trách hãng' chọn 'Có'\n2. Bấm 'Lọc'",
         "Phụ trách hãng: Có",
         "- Chỉ hiện các dòng có chữ X\n"
         "- Lỗi ERP đã biết: ra 'Chưa có dữ liệu' dù có dòng mang chữ X"),

        ("002", "Phụ trách hãng = Không", "P0",
         "Có cả dòng có X và dòng không có X",
         "1. Ô 'Phụ trách hãng' chọn 'Không'\n2. Bấm 'Lọc'\n3. Tìm dòng có chữ X",
         "Phụ trách hãng: Không",
         "- Chỉ hiện dòng trống chữ X, không còn dòng nào có X\n"
         "- Lỗi ERP đã biết: ra toàn bộ dữ liệu, vẫn còn dòng có chữ X"),

        ("003", "Phụ trách hãng = Tất cả", "P1",
         "Đã lọc 'Có' trước đó",
         "1. Đổi ô 'Phụ trách hãng' về 'Tất cả'\n2. Bấm 'Lọc'",
         "",
         "- Ra cả dòng có X và dòng trống X"),

        ("004", "Lọc theo 1 phòng phụ trách", "P0",
         "Phòng P1 đã được phân chia",
         "1. Ô 'Phòng phụ trách' chọn P1\n2. Bấm 'Lọc'",
         "Phòng P1",
         "- Mọi dòng có cột 'Phòng phụ trách' = P1\n"
         "- Xã có nhiều phòng phụ trách chỉ còn dòng của P1"),

        ("005", "Lọc theo nhiều phòng", "P1",
         "P1 và P2 đều đã được phân chia",
         "1. Ô 'Phòng phụ trách' chọn P1 và P2\n2. Bấm 'Lọc'",
         "P1, P2",
         "- Hiện dòng của cả P1 và P2, không có phòng khác"),

        ("006", "Ô Nhân viên thu hẹp theo phòng và khôi phục khi đổi phòng", "P1",
         "Mở màn",
         "1. Ô 'Phòng phụ trách' chọn P1, mở danh sách Nhân viên\n"
         "2. Bỏ P1, chọn P2, mở danh sách Nhân viên\n3. Bỏ hết phòng, mở danh sách Nhân viên",
         "",
         "- Bước 1: chỉ nhân viên của P1\n- Bước 2: chỉ nhân viên của P2\n- Bước 3: toàn bộ nhân viên\n"
         "- Lỗi ERP đã biết: từ bước 2 danh sách trống hoặc thiếu, không khôi phục; phải tải lại trang"),

        ("007", "Danh sách Phòng phụ trách", "P2",
         "Mở màn",
         "1. Mở ô 'Phòng phụ trách'",
         "",
         "- Liệt kê mọi phòng ban (kể cả phòng chưa phân chia), chọn được nhiều phòng\n"
         "- Ghi nhận: có một dòng 'Chọn phòng ban' nằm lẫn trong danh sách lựa chọn"),

        ("008", "Lọc theo 1 nhân viên", "P0",
         "NV1 phụ trách nhiều xã ở 2 tỉnh",
         "1. Ô 'Nhân viên phụ trách' chọn NV1\n2. Bấm 'Lọc'",
         "NV1",
         "- Chỉ hiện dòng của NV1, đủ 2 tỉnh và các xã\n- Cột Phòng phụ trách đúng phòng của NV1"),

        ("009", "Danh sách Nhân viên phụ trách", "P2",
         "Mở màn",
         "1. Mở ô 'Nhân viên phụ trách', gõ tìm một tên",
         "",
         "- Mỗi dòng dạng 'Mã phòng - Họ tên'\n- Tìm được theo họ tên hoặc mã phòng"),

        ("010", "Lọc theo Hãng xe", "P1",
         "Mở màn",
         "1. Ô 'Hãng xe' chọn một hãng bất kỳ\n2. Bấm 'Lọc'",
         "",
         "- Chỉ hiện dòng có hãng đó ở cột 'Hãng xe phụ trách'\n"
         "- Ghi nhận: dữ liệu hiện tại chưa ai được chọn hãng nên ra 'Chưa có dữ liệu' - đúng"),

        ("011", "Kết hợp nhiều bộ lọc", "P0",
         "NV1 thuộc P1 phụ trách xã ở Hà Nội và Hải Phòng",
         "1. Tỉnh/TP: Hà Nội\n2. Phòng phụ trách: P1\n3. Nhân viên phụ trách: NV1\n4. Bấm 'Lọc'",
         "",
         "- Chỉ hiện dòng thỏa CẢ BA điều kiện: Hà Nội, P1, NV1"),

        ("012", "Đổi ô lọc nhưng chưa bấm Lọc", "P1",
         "Đang xem kết quả lọc Hà Nội",
         "1. Đổi Tỉnh/TP sang Hải Phòng, không bấm 'Lọc'",
         "",
         "- Bảng vẫn giữ kết quả Hà Nội, không tự tải lại"),
    ]),

    ("V", "Phân trang & tốc độ", [
        ("001", "Mỗi trang 15 tỉnh", "P0",
         "Có từ 16 tỉnh đã phân chia trở lên",
         "1. Bấm 'Lọc' không chọn bộ lọc\n2. Đếm số tỉnh trang 1\n3. Đếm số trang",
         "",
         "- Trang 1 có đúng 15 tỉnh\n- Số trang = số tỉnh chia 15, làm tròn lên"),

        ("002", "Chuyển trang giữ bộ lọc", "P0",
         "Lọc theo Khu vực có trên 15 tỉnh hoặc không lọc",
         "1. Bấm 'Lọc'\n2. Bấm sang trang 2",
         "",
         "- Trang 2 vẫn áp bộ lọc đang chọn\n- STT nối tiếp trang 1"),

        ("003", "Bấm Lọc đưa về trang 1", "P1",
         "Đang ở trang 2",
         "1. Bấm 'Lọc'",
         "",
         "- Bảng quay về trang 1"),

        ("004", "Nút điều hướng trang", "P2",
         "Có nhiều trang",
         "1. Bấm các nút trang đầu, trang trước, trang sau, trang cuối",
         "",
         "- Mỗi nút chuyển đúng trang\n- Thanh phân trang hiện tối đa 10 số trang"),

        ("005", "Tốc độ tải trang khi không lọc", "P1",
         "Dữ liệu thật có hàng chục nghìn dòng phân chia",
         "1. Bấm 'Lọc' không chọn bộ lọc\n2. Bấm giờ đến khi bảng hiện xong\n3. Thử cuộn bảng",
         "",
         "- Bảng hiện xong trong khoảng 10 giây, cuộn mượt, trình duyệt không treo\n"
         "- Lỗi ERP đã biết: một trang 15 tỉnh có thể tới hàng chục nghìn dòng, tải rất lâu, trình duyệt "
         "báo trang không phản hồi"),

        ("006", "Đổi ô lọc rồi chuyển trang mà không bấm Lọc", "P2",
         "Đang xem trang 1 kết quả không lọc",
         "1. Ô Tỉnh/TP chọn Hà Nội, KHÔNG bấm 'Lọc'\n2. Bấm sang trang 2",
         "",
         "- Ghi nhận hiện tượng: trang mới được tải theo ô lọc đang hiển thị (Hà Nội), nên có thể ra trống"),
    ]),

    ("VI", "Nút làm mới", [
        ("001", "Làm mới xóa các ô lọc", "P1",
         "Đã chọn Khu vực, Tỉnh/TP, Phòng phụ trách, Phụ trách hãng = Có",
         "1. Bấm nút làm mới (biểu tượng mũi tên xoay vòng)\n2. Quan sát các ô lọc và bảng",
         "",
         "- Mọi ô lọc về trống\n"
         "- Ghi nhận: ô Quốc gia cũng bị xóa trắng (không quay về 'Việt Nam' như lúc mở màn)\n"
         "- Bảng không tự tải lại, vẫn giữ kết quả cũ cho tới khi bấm 'Lọc'"),

        ("002", "Làm mới khôi phục danh sách Phường/Xã", "P2",
         "Đã chọn tỉnh Hà Nội (danh sách Phường/Xã đã thu hẹp)",
         "1. Bấm làm mới\n2. Mở danh sách Phường/Xã",
         "",
         "- Hiện lại đủ phường/xã của mọi tỉnh"),

        ("003", "Làm mới khôi phục các danh sách đã bị thu hẹp", "P2",
         "Đã chọn Khu vực (Tỉnh/TP thu hẹp) và Phòng phụ trách (Nhân viên thu hẹp)",
         "1. Bấm làm mới\n2. Mở danh sách Tỉnh/TP\n3. Mở danh sách Nhân viên phụ trách",
         "",
         "- Hai danh sách hiện lại đầy đủ\n"
         "- Lỗi ERP đã biết: danh sách Tỉnh/TP và Nhân viên vẫn giữ trạng thái đã thu hẹp; phải tải lại trang"),
    ]),

    ("VII", "In báo cáo", [
        ("001", "Bấm In mở bản in khổ ngang", "P0",
         "Đã lọc theo một Khu vực",
         "1. Bấm 'In'",
         "",
         "- Mở tab mới với bản in khổ NGANG\n"
         "- Đầu trang là phần đầu trang (logo, tên) của công ty người đăng nhập\n"
         "- Bảng 8 cột như trên màn hình"),

        ("002", "Bản in theo bộ lọc và không phân trang", "P0",
         "Lọc ra 20 tỉnh (2 trang trên màn hình)",
         "1. Bấm 'In'\n2. Đếm số tỉnh và đọc cột STT",
         "",
         "- Bản in có đủ 20 tỉnh, STT 1 đến 20\n- Không có tỉnh ngoài bộ lọc"),

        ("003", "Bản in gộp ô giống màn hình", "P1",
         "Lọc 1 tỉnh có nhiều xã, nhiều phòng",
         "1. Bấm 'In'\n2. So cách gộp ô với màn hình",
         "",
         "- Ô Tỉnh, Xã, Phòng gộp dọc đúng số dòng như màn hình\n- Chữ X và Số điện thoại khớp màn hình"),

        ("004", "In dùng giá trị ô lọc hiện tại kể cả chưa bấm Lọc", "P2",
         "Bảng đang hiện kết quả không lọc",
         "1. Chọn Tỉnh/TP = Hà Nội, KHÔNG bấm 'Lọc'\n2. Bấm 'In'",
         "",
         "- Ghi nhận hiện tượng: bản in chỉ có Hà Nội (theo ô lọc), khác với bảng đang hiển thị"),

        ("005", "In toàn bộ khi không lọc", "P1",
         "Không chọn bộ lọc",
         "1. Bấm 'In'\n2. Bấm giờ đến khi bản in hiện xong",
         "",
         "- Bản in mở được trong thời gian chấp nhận được\n"
         "- Lỗi ERP đã biết: không giới hạn số dòng; với toàn bộ dữ liệu bản in rất lâu hoặc không mở được"),
    ]),

    ("VIII", "Xuất Excel", [
        ("001", "Bấm Xuất excel tải file", "P0",
         "Đã lọc theo một tỉnh",
         "1. Bấm 'Xuất excel'",
         "",
         "- Trình duyệt tải về file 'bao_cao_phan_chia_thi_truong.xlsx'\n- Màn hình không bị chuyển trang"),

        ("002", "Nội dung file Excel", "P0",
         "Đã tải file ở TC trước",
         "1. Mở file Excel",
         "",
         "- Dòng đầu là ảnh đầu trang công ty người đăng nhập\n"
         "- Tiêu đề 'BÁO CÁO PHÂN CHIA THỊ TRƯỜNG'\n"
         "- Bảng 8 cột như màn hình, ô Tỉnh/Xã/Phòng gộp dọc"),

        ("003", "File theo bộ lọc, gồm mọi trang", "P0",
         "Lọc ra 20 tỉnh",
         "1. Bấm 'Xuất excel'\n2. Đếm số tỉnh trong file",
         "",
         "- File có đủ 20 tỉnh, không chỉ 15 tỉnh của trang đang xem"),

        ("004", "Số điện thoại giữ số 0 đầu", "P1",
         "Có nhân viên số điện thoại bắt đầu bằng 0",
         "1. Xuất excel\n2. Đọc ô Số điện thoại của nhân viên đó",
         "",
         "- Hiện đủ số, giữ số 0 đầu (vd 0912000111), không bị đổi thành 912000111"),

        ("005", "Số liệu Excel khớp màn hình", "P1",
         "Lọc 1 tỉnh",
         "1. Đếm số dòng, đọc cột X và Hãng xe trên màn hình\n2. Xuất excel, so từng dòng",
         "",
         "- Số dòng, tên xã, phòng, nhân viên, số điện thoại, chữ X khớp hoàn toàn"),

        ("006", "Xuất toàn bộ khi không lọc", "P2",
         "Không chọn bộ lọc",
         "1. Bấm 'Xuất excel'\n2. Chờ tải file",
         "",
         "- File tải được và mở được\n"
         "- Lỗi ERP đã biết: không giới hạn số dòng; với toàn bộ dữ liệu có thể chờ rất lâu hoặc báo lỗi"),
    ]),

    ("IX", "Luồng nghiệp vụ đầu - cuối", [
        ("001", "Luồng chuẩn: phân chia phòng ban, chia cho nhân viên, xem báo cáo", "P0",
         "Phòng P5 chưa có dữ liệu phân chia. Có tài khoản người lập và người duyệt 2 loại phiếu",
         "1. Menu Kinh doanh > Kế hoạch > 'Phiếu phân chia thị trường theo phòng ban': lập phiếu giao "
         "tỉnh T, xã X1, X2 cho P5, gửi duyệt và duyệt\n"
         "2. 'Phiếu phân chia thị trường theo nhân viên': lập phiếu cho P5, giao X1 cho NV1 (tích Phụ trách "
         "tất cả các hãng), X2 cho NV2, gửi duyệt và duyệt\n"
         "3. Mở báo cáo, lọc phòng P5",
         "Phòng P5, NV1, NV2",
         "- Hiện tỉnh T với 2 xã\n- X1: P5 - NV1, có chữ X\n- X2: P5 - NV2, trống chữ X\n"
         "- Số điện thoại đúng hồ sơ từng nhân viên"),

        ("002", "Phiếu theo nhân viên chưa duyệt thì chưa lên báo cáo", "P0",
         "Đã làm xong bước 1 của TC trước cho phòng P6",
         "1. Lập phiếu theo nhân viên cho P6, chỉ gửi duyệt, chưa duyệt\n2. Lọc báo cáo theo P6\n"
         "3. Duyệt phiếu\n4. Lọc lại",
         "Phòng P6",
         "- Bước 2: 'Chưa có dữ liệu'\n- Bước 4: có dữ liệu của P6"),

        ("003", "Đối chiếu một xã với phiếu gốc", "P1",
         "Chọn ngẫu nhiên một xã đang có dữ liệu",
         "1. Lọc theo xã đó, ghi lại phòng và nhân viên\n"
         "2. Mở các phiếu phân chia đã duyệt của từng phòng, tìm xã đó",
         "",
         "- Mọi phòng / nhân viên trên báo cáo đều có trong phiếu đã duyệt\n"
         "- Không thiếu nhân viên nào được giao xã đó trên phiếu đã duyệt"),

        ("004", "Báo cáo cập nhật ngay khi có phiếu mới duyệt", "P1",
         "Đang mở báo cáo ở một tab, lọc phòng P1",
         "1. Ở tab khác, duyệt một phiếu theo nhân viên mới của P1 giao thêm xã X7 cho NV3\n"
         "2. Quay lại tab báo cáo, bấm 'Lọc'",
         "",
         "- Xuất hiện thêm dòng X7 / P1 / NV3, không cần đăng nhập lại"),
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
