# -*- coding: utf-8 -*-
"""Generate testcase Excel cho man ERP: Bao cao tong hop chi phi van chuyen theo lai xe.

Viet cho MAN ERP GOC (TanPhatDev, route report.transportByDriver*), de tester nam luong
truoc khi nghiem thu ban port sang HRM.

Chay:  PYTHONIOENCODING=utf-8 python gen_testcase.py
Output: testcase - Bao cao tong hop chi phi van chuyen theo lai xe.xlsx (cung thu muc)
SQL ho tro tester: thu muc sql/
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

OUTPUT_FILE = os.path.join(HERE, "testcase - Bao cao tong hop chi phi van chuyen theo lai xe.xlsx")
FEATURE_NAME = "Báo cáo tổng hợp chi phí vận chuyển theo lái xe (ERP)"
MODULE_NAME = "Kho - Báo cáo vận chuyển"

Q_TCT = "Xem báo cáo vận chuyển theo công ty theo tổng công ty"
Q_CT = "Xem báo cáo vận chuyển theo công ty"
Q_HT_CXCH = "Hạch toán chuyến xe chở hàng"
Q_HT_CXK = "Hạch toán chuyến xe khác"

MENU = ("menu Kho > Vận chuyển - Bốc xếp > nhóm 'Báo cáo vận chuyển' > "
        "'Báo cáo tổng hợp chi phí vận chuyển theo lái xe'")
MENU_CHI_TIET = ("menu Kho > Vận chuyển - Bốc xếp > nhóm 'Báo cáo vận chuyển' > "
                 "'Báo cáo chi tiết chi phí vận chuyển theo lái xe'")
MENU_CXCH = "menu Kho > Vận chuyển - Bốc xếp > 'Chuyến xe chở hàng'"
MENU_CXK = "menu Kho > Vận chuyển - Bốc xếp > 'Chuyến xe khác'"
MENU_CHO_HT = ("menu Kế toán > Hàng hoá - Dịch vụ - Vận chuyển > nhóm 'Vận chuyển' > "
               "'Chuyến xe chở hàng chờ hạch toán'")
MENU_CHO_HT_K = ("menu Kế toán > Hàng hoá - Dịch vụ - Vận chuyển > nhóm 'Vận chuyển' > "
                 "'Chuyến xe khác chờ hạch toán'")
MENU_PHT = ("menu Kế toán > Hàng hoá - Dịch vụ - Vận chuyển > nhóm 'Vận chuyển' > "
            "'Phiếu hạch toán chuyến xe chở hàng'")
MENU_PHT_K = ("menu Kế toán > Hàng hoá - Dịch vụ - Vận chuyển > nhóm 'Vận chuyển' > "
              "'Phiếu hạch toán chuyến xe khác'")

COT = ("STT · Mã lái xe · Nhân viên lái xe · Công lái xe · Chi phí (2 cột con: Xăng xe, Khác) · "
       "Công tác phí · Vé cầu đường · Cộng · KM định mức · KM thực chạy · Chênh lệch (KM) · % Chênh lệch")

# =========================================================================
# 9 MUC MO TA
# =========================================================================
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Báo cáo tổng hợp, mỗi LÁI XE một dòng, các khoản chi phí lái xe đã được hạch toán trong kỳ: Công lái "
     "xe, Xăng xe, Chi phí khác, Công tác phí, Vé cầu đường, kèm KM định mức, KM thực chạy và phần chênh "
     "lệch. Nguồn số là khối 'lái xe' trên 'Phiếu hạch toán chuyến xe chở hàng' và 'Phiếu hạch toán chuyến "
     "xe khác'. Màn chỉ để xem, không sửa dữ liệu.\n"
     "Lối vào duy nhất: " + MENU + ".\n"
     "Báo cáo anh em: 'Báo cáo chi tiết chi phí vận chuyển theo lái xe' cùng nhóm menu, dùng chung cách "
     "tính, có thêm bộ lọc và tách từng phiếu."),

    ("2. Đối tượng được tính / hiển thị",
     "Một khoản được cộng vào báo cáo khi thỏa ĐỦ:\n"
     "- Thuộc phiếu hạch toán chuyến xe chở hàng hoặc phiếu hạch toán chuyến xe khác ĐÃ bấm 'Lưu và duyệt' "
     "(trạng thái 'Đã hạch toán').\n"
     "- Là một trong 5 khoản của lái xe: Công lái xe, Chi phí xăng xe, Chi phí khác, Vé cầu đường, Công tác "
     "phí. Khoản nào bằng 0 thì không ghi sổ, báo cáo hiện '-'.\n"
     "- Chuyến dùng LÁI XE THUỘC CÔNG TY (trên phiếu có khối Tên lái xe / Công lái xe...).\n"
     "- Ngày hạch toán nằm trong Từ ngày - Đến ngày, lấy trọn 2 ngày đầu cuối.\n"
     "- Nằm trong phạm vi quyền xem (mục 7)."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu hạch toán trạng thái 'Đang tạo' (mới bấm 'Lưu'): chưa ghi sổ nên không tính.\n"
     "- Chuyến xe thuê ngoài / lái xe ngoài công ty: không có khối lái xe nên không có số.\n"
     "- Các khoản cước vận chuyển của nhân viên kinh doanh, thuế, công nợ nhà cung cấp trên cùng phiếu.\n"
     "- Phiếu hạch toán có ngày hạch toán ngoài khoảng lọc, kể cả khi ngày chạy chuyến nằm trong khoảng.\n"
     "- Lái xe của công ty khác (với tài khoản chỉ có quyền theo công ty)."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Từ ngày và Đến ngày là BẮT BUỘC (nút 'Lọc' khóa cho tới khi nhập đủ 2 ô).\n"
     "Lọc theo NGÀY HẠCH TOÁN = thời điểm bấm 'Lưu và duyệt' phiếu hạch toán, KHÔNG theo ngày tạo / ngày "
     "chạy chuyến xe. Ví dụ trên dev: chuyến chạy 01/06/2026 nhưng phiếu duyệt 30/06/2026 thì chỉ lên báo "
     "cáo khi khoảng lọc chứa 30/06/2026.\n"
     "Màn KHÔNG tự tải khi mở."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Bảng phẳng 1 cấp, mỗi dòng 1 lái xe, 13 cột: " + COT + ".\n"
     "- Mã lái xe: mã hồ sơ nhân sự của lái xe; không có hồ sơ thì để trống.\n"
     "- Nhân viên lái xe: họ tên, là link mở báo cáo chi tiết ở tab mới.\n"
     "- Sắp xếp theo họ tên lái xe A-Z. Hai hồ sơ trùng họ tên hiện 2 dòng riêng.\n"
     "- Dòng 'Tổng cộng' nằm ngay dưới tiêu đề.\n"
     "- Phân trang 20 lái xe mỗi trang, STT nối tiếp giữa các trang."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Mỗi cột tiền = tổng khoản tương ứng của mọi phiếu hạch toán (cả 2 loại phiếu) của lái xe trong kỳ.\n"
     "- Cột 'Khác' = khoản 'Chi phí khác' trên phiếu.\n"
     "- Cộng = Công lái xe + Xăng xe + Khác + Vé cầu đường + Công tác phí (đúng nghiệp vụ, xem lỗi (1) mục 9).\n"
     "- KM định mức: chuyến chở hàng = số km của tuyến đường, nhân 2 nếu chuyến 2 chiều; chuyến xe khác có "
     "chọn tuyến thì như trên, không chọn tuyến thì lấy số km nhập trên chuyến. KHÔNG dùng 'Km duyệt' của phiếu.\n"
     "- KM thực chạy = Km kết thúc trừ Km bắt đầu của chuyến xe. Mỗi phiếu tính 1 lần cho lái xe.\n"
     "- Chênh lệch (KM) = KM thực chạy trừ KM định mức; % Chênh lệch = Chênh lệch chia KM định mức nhân 100.\n"
     "- Dòng 'Tổng cộng' = tổng mọi lái xe của MỌI trang."),

    ("7. Phân quyền cấp",
     "Mọi tài khoản đăng nhập đều mở được màn (menu không ẩn theo quyền). Phạm vi dữ liệu theo quyền (tên "
     "hiển thị trong màn phân quyền, nhóm 'Vận chuyển - bốc xếp'):\n"
     "- '" + Q_TCT + "': thấy lái xe mọi công ty; có ô lọc Công ty; ô Nhân viên liệt kê nhân viên mọi công ty.\n"
     "- '" + Q_CT + "': chỉ lái xe thuộc công ty mình; không có ô Công ty.\n"
     "- Không có 2 quyền trên: chỉ thấy số từ các phiếu hạch toán do CHÍNH MÌNH LẬP (không phải số của "
     "chính mình khi mình là lái xe); không có ô Công ty.\n"
     "Có cả 2 quyền thì theo quyền tổng công ty.\n"
     "Lập dữ liệu nguồn cần: '" + Q_HT_CXCH + "', '" + Q_HT_CXK + "'."),

    ("8. Cách tính các ô thống kê",
     "- Tiền trên màn hình làm tròn, phân cách hàng nghìn bằng dấu phẩy (vd 1,250,000); khoản bằng 0 hiện '-'.\n"
     "- KM định mức, KM thực chạy: phân cách hàng nghìn, tối đa 2 chữ số thập phân.\n"
     "- Chênh lệch (KM): số nguyên, có thể âm; bằng 0 hiện '-'. % Chênh lệch: 2 chữ số thập phân.\n"
     "- Xuất excel: dưới 1000 lái xe thì tải file ngay; từ 1000 lái xe trở lên thì gửi file qua email với "
     "thông báo 'Báo cáo tổng hợp chi phí vận chuyển theo lái xe sẽ gửi về mail của bạn trong ít phút!'."),

    ("9. Ghi chú đọc bảng",
     "Dữ liệu mẫu dùng trong testcase:\n"
     "- LX1, LX2: lái xe thuộc công ty TPE. LX3: lái xe thuộc công ty TPV.\n"
     "- CX1: chuyến xe chở hàng của LX1; CXK1: chuyến xe khác của LX1; CX9: chuyến xe thuê ngoài.\n"
     "- PHT1: phiếu hạch toán của CX1; PHK1: phiếu hạch toán chuyến xe khác của CXK1.\n"
     "- Tài khoản A: kế toán TPE lập phiếu hạch toán. B: quyền theo công ty (TPE). G: quyền theo tổng công "
     "ty. N: không có quyền xem nào.\n"
     "- Câu truy vấn hỗ trợ trong thư mục sql: số 1 tính lại số từng lái xe, số 2 liệt kê từng phiếu của 1 "
     "lái xe. Trên dev đã có sẵn số tháng 06/2026 (vd lái xe Lê Văn Trình, 16 phiếu).\n"
     "Các lỗi ERP ĐÃ BIẾT, testcase ghi kết quả mong đợi ĐÚNG; chạy thấy hiện tượng lỗi thì ghi Failed và chép "
     "câu 'Lỗi ERP đã biết' vào Ghi chú:\n"
     "(1) Cột 'Cộng' (dòng lái xe, Tổng cộng, file Excel) không cộng Công tác phí. Cần nghiệp vụ xác nhận.\n"
     "(2) Dòng Tổng cộng cột '% Chênh lệch' trên màn hình là tổng các % của từng lái xe, không phải chênh "
     "lệch tổng chia KM định mức tổng. File Excel tính đúng nên 2 bên lệch nhau.\n"
     "(3) Dòng lái xe có % Chênh lệch bằng 0 hiện '-%' thay vì '-'; Chênh lệch (KM) từ 1,000 trở lên không có "
     "dấu phân cách.\n"
     "(4) Bấm làm mới xong, nút Xuất excel vẫn bấm được, tab mới báo lỗi không tải file.\n"
     "(5) Xuất excel lỗi khi tổng KM định mức của kết quả bằng 0.\n"
     "(6) Xuất từ 1000 lái xe trở lên: có thông báo gửi email nhưng email không tới.\n"
     "Hành vi ERP ghi nhận (không phải lỗi): lọc theo ngày hạch toán; KM định mức theo km tuyến, không theo "
     "Km duyệt; tài khoản không quyền xem theo người lập phiếu; phiếu đã hạch toán không sửa / xóa được nên "
     "không có thao tác làm GIẢM số trên giao diện."),
]

# =========================================================================
# SECTION PHAN QUYEN
# =========================================================================
ROLE_TCS = [
    ("00", "Không có quyền xem nào: chỉ thấy số từ phiếu do chính mình lập", "P0",
     "Tài khoản N (công ty TPE) không có 2 quyền xem báo cáo vận chuyển, có quyền '" + Q_HT_CXCH + "'.\n"
     "Trong tháng N đã lập và duyệt 1 phiếu hạch toán cho LX1; tài khoản A lập 3 phiếu khác cho LX1",
     "1. Đăng nhập N, mở " + MENU + "\n2. Quan sát bộ lọc\n"
     "3. Từ ngày đầu tháng, Đến ngày hôm nay, bấm 'Lọc'",
     "Tài khoản: N",
     "- Bộ lọc KHÔNG có ô Công ty\n"
     "- Bảng chỉ có LX1 với đúng số của 1 phiếu N lập, không cộng 3 phiếu của A\n"
     "- Ghi nhận hành vi ERP: phạm vi theo người lập phiếu hạch toán"),

    ("01", "Lái xe không có quyền xem không thấy số của chính mình", "P1",
     "Tài khoản của LX1 không có quyền xem nào, chưa từng lập phiếu hạch toán; LX1 có 3 phiếu trong tháng do A lập",
     "1. Đăng nhập bằng LX1, mở " + MENU + "\n2. Lọc từ đầu tháng đến hôm nay",
     "Tài khoản: LX1",
     "- Bảng 'Chưa có dữ liệu'\n"
     "- Ghi nhận hành vi ERP: muốn lái xe tự xem phải cấp quyền theo công ty"),

    ("02", "Quyền theo công ty", "P0",
     "Tài khoản B thuộc TPE chỉ có quyền '" + Q_CT + "'.\n"
     "Trong tháng LX1, LX2 (TPE) và LX3 (TPV) đều có phiếu đã hạch toán",
     "1. Đăng nhập B, mở màn\n2. Quan sát bộ lọc, mở ô Nhân viên\n3. Lọc từ đầu tháng đến hôm nay",
     "Tài khoản: B",
     "- Không có ô Công ty\n- Ô Nhân viên chỉ liệt kê nhân viên TPE\n"
     "- Bảng có LX1, LX2, không có LX3\n"
     "- Có cả phiếu do người khác lập (không giới hạn người lập)"),

    ("03", "Quyền theo tổng công ty", "P0",
     "Tài khoản G chỉ có quyền '" + Q_TCT + "'",
     "1. Đăng nhập G, mở màn\n2. Quan sát bộ lọc\n3. Lọc từ đầu tháng đến hôm nay, không chọn Công ty",
     "Tài khoản: G",
     "- Có ô Công ty (mặc định 'Chọn công ty') và ô Nhân viên\n"
     "- Bảng có lái xe của mọi công ty: LX1, LX2, LX3"),

    ("04", "Có cả 2 quyền thì theo quyền tổng công ty", "P1",
     "Tài khoản H có cả '" + Q_TCT + "' và '" + Q_CT + "', thuộc TPE",
     "1. Đăng nhập H, lọc từ đầu tháng đến hôm nay",
     "Tài khoản: H",
     "- Có ô Công ty\n- Bảng có cả LX3 của TPV, kết quả giống tài khoản G"),

    ("05", "Màn mở được với mọi tài khoản", "P1",
     "Tài khoản bất kỳ không thuộc khối kho / vận chuyển",
     "1. Đăng nhập, mở " + MENU,
     "",
     "- Menu có mục báo cáo, màn mở được, không báo thiếu quyền"),

    ("06", "Quyền theo công ty không vượt phạm vi khi sửa đường dẫn Xuất excel", "P2",
     "Tài khoản B (quyền theo công ty, TPE). Dành cho tester kỹ thuật",
     "1. Lọc tháng, bấm 'Xuất excel', sao chép đường dẫn tab tải file\n"
     "2. Thêm vào đường dẫn tham số công ty bằng mã của TPV, mở lại",
     "Tài khoản: B",
     "- File vẫn chỉ có lái xe TPE, không có LX3"),

    ("07", "Phạm vi quyền áp cả cho Xuất excel", "P1",
     "Tài khoản B (quyền theo công ty)",
     "1. Lọc từ đầu tháng đến hôm nay\n2. Bấm 'Xuất excel', mở file",
     "Tài khoản: B",
     "- File chỉ có lái xe TPE, số dòng và dòng Tổng cộng khớp màn hình"),

    ("08", "Không quyền: chọn nhân viên khác cũng không mở rộng phạm vi", "P1",
     "Tài khoản N như TC-ROLE-00",
     "1. Ô Nhân viên chọn LX1\n2. Bấm 'Lọc'",
     "Nhân viên: LX1",
     "- LX1 vẫn chỉ có số của 1 phiếu do N lập"),
]

# =========================================================================
# CAC SECTION CHUC NANG
# =========================================================================
SECTIONS = [
    ("I", "Chuẩn bị dữ liệu test", [
        ("001", "Tìm lái xe có sẵn số liệu trên dev", "P0",
         "Có người chạy được câu truy vấn trên dữ liệu dev (hoặc nhờ người hỗ trợ chạy)",
         "1. Chạy câu truy vấn số 1 thư mục sql, khoảng ngày 01/06/2026 đến 30/06/2026\n"
         "2. Chọn 2 lái xe cùng công ty có nhiều phiếu làm LX1, LX2, 1 lái xe công ty khác làm LX3\n"
         "3. Chạy câu số 2 với họ tên LX1 để có danh sách từng phiếu",
         "Khoảng ngày: 01/06/2026 đến 30/06/2026",
         "- Câu số 1 trả về danh sách lái xe kèm 5 khoản tiền và KM\n"
         "- Câu số 2 trả về từng phiếu hạch toán, số phiếu bằng cột số phiếu của câu số 1"),

        ("002", "Chuẩn bị đủ tài khoản test", "P0",
         "Quản trị có quyền phân quyền",
         "1. Gán cho A (kế toán TPE): '" + Q_HT_CXCH + "', '" + Q_HT_CXK + "'\n"
         "2. Gán cho B (TPE): '" + Q_CT + "'\n3. Gán cho G: '" + Q_TCT + "'\n"
         "4. Tài khoản N: chỉ '" + Q_HT_CXCH + "', không có 2 quyền xem",
         "Tài khoản A, B, G, N",
         "- A thấy mục 'Chuyến xe chở hàng chờ hạch toán' và 'Chuyến xe khác chờ hạch toán' trong menu Kế toán\n"
         "- B, G, N mở được báo cáo"),

        ("003", "Chuẩn bị xe, tuyến và công thức vận chuyển", "P1",
         "Công ty TPE có xe XE1 do công ty sở hữu, kiểu lái xe thuộc công ty, lái xe LX1",
         "1. Kiểm tra tuyến đường TD1 có số km 50\n"
         "2. Kiểm tra công thức vận chuyển của TPE có định mức công lái xe, xăng, chi phí khác cho dòng xe và "
         "tải trọng của XE1\n"
         "3. Kiểm tra 'Bảng giá hiệu lực vận chuyển' (menu Kho > Vận chuyển - Bốc xếp) còn hiệu lực",
         "Tuyến TD1: 50 km",
         "- Có đủ 3 điều kiện; thiếu bảng giá thì khi lưu phiếu hạch toán báo 'Chưa có bảng giá hiệu lực !'\n"
         "- Thiếu công thức thì báo 'Không tìm thấy xe, trọng tải tuyến đường phù hợp trong công thức vận chuyển'"),

        ("004", "Tạo chuyến xe chở hàng CX1 cho LX1", "P0",
         "Có phiếu xuất kho đã xuất của TPE cần giao",
         "1. Vào " + MENU_CXCH + ", tạo chuyến CX1: xe XE1, lái xe LX1, tuyến TD1, 2 chiều, gắn phiếu xuất kho\n"
         "2. Nhập Km bắt đầu 10,000, Km kết thúc 10,110, vé cầu đường 120,000, công tác phí 100,000\n"
         "3. Hoàn tất chuyến đến khi CX1 hiện ở " + MENU_CHO_HT,
         "CX1: TD1 2 chiều\nKm bắt đầu 10,000\nKm kết thúc 10,110\nVé cầu đường 120,000\nCông tác phí 100,000",
         "- CX1 nằm trong danh sách 'Chuyến xe chở hàng chờ hạch toán'\n"
         "- KM định mức dự kiến của CX1 = 50 x 2 = 100; KM thực chạy = 110"),

        ("005", "Tạo chuyến xe khác CXK1 cho LX1 không chọn tuyến", "P1",
         "Như TC trên",
         "1. Vào " + MENU_CXK + ", tạo CXK1: xe XE1, lái xe LX1, KHÔNG chọn tuyến, điểm đầu Kho Hà Nội, điểm "
         "cuối Bắc Ninh, km 40, 1 chiều\n2. Km bắt đầu 20,000, Km kết thúc 20,045\n"
         "3. Hoàn tất đến khi CXK1 hiện ở " + MENU_CHO_HT_K,
         "CXK1: km 40, 1 chiều\nKm bắt đầu 20,000\nKm kết thúc 20,045",
         "- CXK1 nằm trong danh sách 'Chuyến xe khác chờ hạch toán'\n"
         "- KM định mức dự kiến 40; KM thực chạy 45"),

        ("006", "Tạo chuyến đối chứng: lái xe công ty khác và xe thuê ngoài", "P1",
         "Công ty TPV có lái xe LX3; có xe thuê ngoài của nhà cung cấp",
         "1. Tạo chuyến xe chở hàng cho LX3 (TPV), hoàn tất đến chờ hạch toán\n"
         "2. Tạo chuyến CX9 dùng xe thuê ngoài, lái xe ngoài, hoàn tất đến chờ hạch toán",
         "",
         "- Có 2 chuyến chờ hạch toán để dùng ở section kiểm tra tăng / giảm"),

        ("007", "Nắm 2 trạng thái của phiếu hạch toán", "P1",
         "Đã có CX1 chờ hạch toán",
         "1. A mở " + MENU_CHO_HT + ", lập phiếu hạch toán cho CX1\n"
         "2. Quan sát khối lái xe và 2 nút cuối trang\n3. Mở " + MENU_PHT + ", quan sát cột trạng thái",
         "",
         "- Khối lái xe có: Tên lái xe, Công lái xe, Chi phí xăng xe, Chi phí khác, Vé cầu đường, Công tác phí\n"
         "- Nút 'Lưu' cho trạng thái 'Đang tạo'; nút 'Lưu và duyệt' cho trạng thái 'Đã hạch toán'\n"
         "- Chỉ phiếu 'Đã hạch toán' mới lên báo cáo"),
    ]),

    ("II", "Giao diện & mở màn", [
        ("001", "Mở màn từ menu", "P0",
         "Đăng nhập tài khoản G",
         "1. Bấm " + MENU,
         "",
         "- Mở màn tiêu đề 'BÁO CÁO TỔNG HỢP CHI PHÍ VẬN CHUYỂN THEO LÁI XE'\n"
         "- Đây là lối vào duy nhất, không có mục cùng tên ở menu khác"),

        ("002", "Bố cục màn hình", "P0",
         "Tài khoản G",
         "1. Quan sát khối 'Bộ lọc' và khối 'Chi tiết'",
         "",
         "- Bộ lọc: Từ ngày* · Đến ngày* · Công ty · Nhân viên\n"
         "- Nút 'Xuất excel', 'Lọc', nút làm mới (mũi tên xoay vòng)\n"
         "- Khối 'Chi tiết' chứa bảng và phân trang"),

        ("003", "Trạng thái mặc định khi mở", "P0",
         "Vừa mở màn",
         "1. Quan sát ô ngày, nút Lọc, bảng",
         "",
         "- Từ ngày, Đến ngày trống\n- Nút 'Lọc' bị khóa\n- Bảng hiện 'Chưa có dữ liệu'\n"
         "- Màn không tự tải dữ liệu"),

        ("004", "Tiêu đề 13 cột và dòng Tổng cộng", "P0",
         "Vừa mở màn",
         "1. Đọc tiêu đề bảng",
         "",
         "- Đúng thứ tự: " + COT + "\n"
         "- 'Chi phí' là tiêu đề gộp 2 tầng, bên dưới là Xăng xe và Khác\n"
         "- Ngay dưới tiêu đề là dòng 'Tổng cộng' gộp 3 cột đầu"),

        ("005", "Nút Xuất excel khi chưa có dữ liệu", "P1",
         "Vừa mở màn",
         "1. Bấm 'Xuất excel'",
         "",
         "- Nút mờ, bấm không mở tab mới"),

        ("006", "Trạng thái đang tải", "P2",
         "Đã nhập đủ 2 ngày, khoảng ngày 1 năm",
         "1. Bấm 'Lọc', quan sát ngay",
         "",
         "- Dòng Tổng cộng hiện 'Đang tải dữ liệu' có biểu tượng quay\n"
         "- Nút Lọc, làm mới, Xuất excel bị khóa trong lúc tải"),

        ("007", "Ô ngày và thu gọn bộ lọc", "P2",
         "Vừa mở màn",
         "1. Bấm ô Từ ngày, chọn ngày trên lịch\n2. Bấm mũi tên góc phải khối 'Bộ lọc' 2 lần",
         "",
         "- Ngày hiện dạng ngày/tháng/năm (vd 01/06/2026)\n"
         "- Khối Bộ lọc thu gọn rồi mở lại, giá trị đã nhập giữ nguyên"),
    ]),

    ("III", "Bộ lọc", [
        ("001", "Thiếu một ô ngày", "P0",
         "Vừa mở màn",
         "1. Nhập Từ ngày 01/06/2026, để trống Đến ngày\n2. Thử bấm 'Lọc'",
         "Từ ngày: 01/06/2026",
         "- Nút 'Lọc' vẫn khóa, không bấm được"),

        ("002", "Lọc theo ngày hạch toán, không theo ngày chạy chuyến", "P0",
         "Dữ liệu dev: phiếu TPE_HTCXCH_02402 của lái xe Lê Văn Trình, chuyến chạy 01/06/2026, phiếu duyệt "
         "30/06/2026 14:27 (xem câu truy vấn số 2)",
         "1. Tài khoản G, chọn nhân viên Lê Văn Trình\n2. Lọc 01/06/2026 đến 29/06/2026, ghi các số\n"
         "3. Lọc lại 01/06/2026 đến 30/06/2026",
         "",
         "- Bước 2: KHÔNG gồm số của phiếu TPE_HTCXCH_02402 (Công lái xe của phiếu là 231,000)\n"
         "- Bước 3: Công lái xe tăng thêm ít nhất 231,000\n"
         "- Ghi nhận hành vi ERP: tính theo ngày duyệt phiếu"),

        ("003", "Lấy trọn ngày cuối", "P1",
         "Có phiếu duyệt lúc 14:27 ngày 30/06/2026",
         "1. Lọc Từ ngày 30/06/2026, Đến ngày 30/06/2026",
         "",
         "- Phiếu đó được tính (lấy đến hết ngày 30/06)"),

        ("004", "Từ ngày lớn hơn Đến ngày", "P2",
         "Vừa mở màn",
         "1. Từ ngày 30/06/2026, Đến ngày 01/06/2026\n2. Bấm 'Lọc'",
         "",
         "- Không có cảnh báo\n- Bảng 'Chưa có dữ liệu', các ô Tổng cộng bằng 0"),

        ("005", "Chọn Công ty", "P0",
         "Tài khoản G; trong tháng có lái xe TPE và TPV",
         "1. Ô Công ty chọn TPV\n2. Mở ô Nhân viên\n3. Lọc tháng 06/2026",
         "Công ty: TPV",
         "- Ô Nhân viên chỉ còn nhân viên TPV\n- Bảng chỉ có lái xe thuộc TPV\n"
         "- Tổng cộng chỉ cộng lái xe TPV"),

        ("006", "Đổi Công ty xóa Nhân viên đã chọn", "P1",
         "Đã chọn công ty TPE và nhân viên LX1",
         "1. Đổi Công ty sang TPV",
         "",
         "- Ô Nhân viên về 'Chọn nhân viên'"),

        ("007", "Chọn Nhân viên", "P0",
         "LX1 có số trong tháng",
         "1. Ô Nhân viên chọn LX1\n2. Lọc tháng",
         "Nhân viên: LX1",
         "- Bảng chỉ còn 1 dòng LX1\n- Mỗi ô Tổng cộng bằng ô tương ứng của LX1"),

        ("008", "Ô Nhân viên liệt kê mọi nhân viên, không chỉ lái xe", "P2",
         "Tài khoản B",
         "1. Mở ô Nhân viên, chọn một nhân viên kinh doanh không lái xe\n2. Lọc tháng",
         "",
         "- Ghi nhận hành vi ERP: danh sách gồm mọi nhân viên của công ty\n"
         "- Chọn người không lái xe thì bảng 'Chưa có dữ liệu'"),

        ("009", "Bỏ chọn Công ty trở về tất cả", "P1",
         "Tài khoản G đang lọc công ty TPV",
         "1. Ô Công ty chọn lại 'Chọn công ty'\n2. Bấm 'Lọc'",
         "",
         "- Bảng có lái xe của mọi công ty như khi chưa chọn"),

        ("010", "Công ty của lái xe tính theo phòng ban lúc hạch toán", "P2",
         "LX2 thuộc TPE đến ngày 15/06/2026, sau đó chuyển sang phòng ban của TPV; cả 2 giai đoạn đều có phiếu",
         "1. Tài khoản G lọc tháng 06/2026, chọn công ty TPE\n2. Chọn công ty TPV",
         "",
         "- Bước 1: LX2 chỉ có số các phiếu duyệt khi còn ở TPE\n"
         "- Bước 2: LX2 chỉ có số các phiếu duyệt sau khi sang TPV"),
    ]),

    ("IV", "Bảng số liệu & cách tính từng cột", [
        ("001", "Thông tin mỗi dòng lái xe", "P0",
         "Tài khoản G, lọc tháng 06/2026",
         "1. Đọc 3 cột đầu của vài dòng",
         "",
         "- STT 1, 2, 3...\n- Mã lái xe là mã hồ sơ nhân sự; không có hồ sơ thì ô trống\n"
         "- Nhân viên lái xe là họ tên, có gạch chân link"),

        ("002", "Sắp xếp theo họ tên", "P1",
         "Như trên",
         "1. Đọc cột Nhân viên lái xe từ trên xuống",
         "",
         "- Họ tên xếp A-Z"),

        ("003", "Cột Công lái xe", "P0",
         "Câu truy vấn số 2 với lái xe Lê Văn Trình tháng 06/2026 ra 16 phiếu",
         "1. Lọc 01/06/2026 đến 30/06/2026, chọn Lê Văn Trình\n2. Cộng tay cột Công lái xe của 16 phiếu",
         "",
         "- Ô Công lái xe bằng tổng cộng tay (trên dev local là 2,986,500)\n"
         "- Gồm cả phiếu chuyến xe chở hàng và phiếu chuyến xe khác"),

        ("004", "Các cột Xăng xe, Khác, Công tác phí, Vé cầu đường", "P0",
         "Như trên",
         "1. So từng cột với tổng tương ứng của câu truy vấn số 2",
         "",
         "- Xăng xe = tổng 'Chi phí xăng xe'\n- Khác = tổng 'Chi phí khác'\n"
         "- Công tác phí = tổng 'Công tác phí'\n- Vé cầu đường = tổng 'Vé cầu đường'\n"
         "- Lưu ý: thứ tự cột là Xăng xe, Khác, Công tác phí, Vé cầu đường"),

        ("005", "Cột Cộng", "P0",
         "Lái xe Lê Văn Trình tháng 06/2026 có Công tác phí khác 0",
         "1. Đọc cột Cộng, so với tổng 5 cột tiền của cùng dòng",
         "",
         "- Cộng = Công lái xe + Xăng xe + Khác + Công tác phí + Vé cầu đường\n"
         "- Lỗi ERP đã biết: Cộng thiếu đúng phần Công tác phí (trên dev local thiếu 840,000)"),

        ("006", "KM định mức của chuyến xe chở hàng", "P0",
         "CX1 tuyến TD1 50 km, 2 chiều, phiếu PHT1 đã duyệt hôm nay, Km duyệt nhập 105",
         "1. Lọc hôm nay, chọn LX1 (chỉ có PHT1 trong ngày)",
         "",
         "- KM định mức = 100 (50 x 2)\n"
         "- Ghi nhận hành vi ERP: không lấy Km duyệt 105 của phiếu"),

        ("007", "KM định mức của chuyến xe khác không chọn tuyến", "P1",
         "CXK1 không chọn tuyến, km 40, 1 chiều, phiếu PHK1 duyệt hôm nay",
         "1. Lọc hôm nay, chọn LX1",
         "",
         "- KM định mức tăng thêm 40 so với khi chỉ có PHT1"),

        ("008", "KM thực chạy", "P0",
         "CX1 Km bắt đầu 10,000, Km kết thúc 10,110",
         "1. Lọc hôm nay, chọn LX1 (chỉ có PHT1)",
         "",
         "- KM thực chạy = 110"),

        ("009", "Chênh lệch và % Chênh lệch của dòng", "P0",
         "Như TC trên: KM định mức 100, KM thực chạy 110",
         "1. Đọc 2 cột cuối của LX1",
         "",
         "- Chênh lệch (KM) = 10\n- % Chênh lệch = 10% (tối đa 2 chữ số thập phân, làm tròn xuống)"),

        ("010", "Chênh lệch âm khi chạy ít hơn định mức", "P1",
         "Lái xe có KM định mức 72, KM thực chạy 63 (trên dev local: Nguyễn Đình Huỳnh tháng 06/2026)",
         "1. Lọc tháng 06/2026, chọn lái xe đó",
         "",
         "- Chênh lệch (KM) = -9\n- % Chênh lệch = -12.5%"),

        ("011", "Định dạng số trên dòng lái xe", "P1",
         "Lái xe có Chi phí khác bằng 0 và một lái xe có KM thực chạy bằng KM định mức",
         "1. Lọc tháng, đọc các ô",
         "",
         "- Tiền phân cách hàng nghìn bằng dấu phẩy, vd 2,986,500\n- Khoản bằng 0 hiện '-'\n"
         "- Chênh lệch bằng 0 hiện '-', % Chênh lệch bằng 0 hiện '-'\n"
         "- Lỗi ERP đã biết: ô % hiện '-%'; Chênh lệch từ 1,000 trở lên hiện không có dấu phẩy"),

        ("012", "Hai lái xe trùng họ tên", "P2",
         "Trên dev local tháng 06/2026 có 2 hồ sơ 'Đồng Xuân Thạch' (TPHP) với mã khác nhau",
         "1. Tài khoản G lọc tháng 06/2026",
         "",
         "- Có 2 dòng 'Đồng Xuân Thạch' liền nhau, Mã lái xe khác nhau, số liệu riêng từng dòng"),

        ("013", "Lái xe có cả 2 loại phiếu gộp 1 dòng", "P1",
         "LX1 có PHT1 (chuyến chở hàng) và PHK1 (chuyến xe khác) cùng ngày",
         "1. Lọc ngày đó, không chọn nhân viên",
         "",
         "- LX1 chỉ có 1 dòng, mỗi cột bằng tổng của 2 phiếu"),

        ("014", "Số KM bất thường vẫn hiện nguyên", "P2",
         "Trên dev local lái xe Nguyễn Hồng Thắng tháng 06/2026 có KM thực chạy rất lớn (1,136,789) do nhập "
         "sai Km trên chuyến",
         "1. Lọc tháng 06/2026, tìm dòng đó",
         "",
         "- Báo cáo hiện đúng số đã nhập, không tự bỏ qua\n- Dùng để báo bộ phận vận tải sửa chuyến xe nếu cần"),
    ]),

    ("V", "Phân trang & dòng Tổng cộng", [
        ("001", "Mỗi trang 20 lái xe", "P0",
         "Tài khoản G, khoảng ngày 01/08/2025 đến 30/06/2026 có trên 20 lái xe",
         "1. Lọc\n2. Đếm dòng trang 1, chuyển trang 2",
         "",
         "- Trang 1 có 20 dòng\n- Trang 2 STT bắt đầu từ 21"),

        ("002", "Tổng cộng tính mọi trang", "P0",
         "Như trên",
         "1. Ghi lại Tổng cộng cột Công lái xe\n2. Cộng tay cột đó ở trang 1 và trang 2\n3. Chuyển trang",
         "",
         "- Tổng cộng = tổng mọi lái xe ở mọi trang\n- Chuyển trang Tổng cộng không đổi"),

        ("003", "Tổng cộng từng cột bằng tổng các dòng", "P0",
         "Kết quả lọc chỉ 1 trang",
         "1. Cộng tay từng cột tiền và KM của các dòng",
         "",
         "- Mỗi ô Tổng cộng bằng tổng cột tương ứng\n"
         "- Tổng cộng cột Cộng bằng tổng 5 cột tiền (xem lỗi ERP đã biết số 1 về Công tác phí)"),

        ("004", "% Chênh lệch ở dòng Tổng cộng", "P0",
         "Kết quả có ít nhất 2 lái xe, vd A: định mức 100, thực chạy 110; B: định mức 200, thực chạy 190",
         "1. Đọc ô % Chênh lệch dòng Tổng cộng",
         "",
         "- % = Chênh lệch tổng chia KM định mức tổng nhân 100 = 0 / 300 = 0%\n"
         "- Lỗi ERP đã biết: màn hình cộng % từng dòng (10% cộng -5% ra 5%)"),

        ("005", "Chuyển trang giữ bộ lọc", "P1",
         "Đã lọc theo công ty TPE, có trên 20 lái xe",
         "1. Chuyển sang trang 2",
         "",
         "- Trang 2 vẫn chỉ có lái xe TPE"),

        ("006", "Bấm Lọc quay về trang 1", "P2",
         "Đang ở trang 2",
         "1. Bấm 'Lọc'",
         "",
         "- Quay về trang 1, STT bắt đầu từ 1"),
    ]),

    ("VI", "Nút làm mới", [
        ("001", "Làm mới xóa ngày, Công ty, Nhân viên", "P1",
         "Đã nhập đủ ngày, chọn Công ty và Nhân viên, đã bấm Lọc ra dữ liệu",
         "1. Bấm nút làm mới",
         "",
         "- Từ ngày, Đến ngày, Công ty, Nhân viên về trống\n- Nút 'Lọc' khóa lại\n"
         "- Ghi nhận hành vi ERP: bảng vẫn giữ kết quả cũ cho tới lần lọc sau"),

        ("002", "Xuất excel sau khi làm mới", "P1",
         "Vừa làm TC trên, bảng còn kết quả cũ",
         "1. Bấm 'Xuất excel'",
         "",
         "- Nút Xuất excel khóa, hoặc file ra đúng bảng đang hiện\n"
         "- Lỗi ERP đã biết: nút vẫn bấm được, tab mới báo lỗi, không tải được file"),

        ("003", "Đổi bộ lọc nhưng chưa bấm Lọc rồi xuất", "P2",
         "Bảng đang hiện kết quả tháng 06/2026 của mọi lái xe",
         "1. Chọn Nhân viên LX1, KHÔNG bấm Lọc\n2. Bấm 'Xuất excel'",
         "",
         "- Ghi nhận hành vi ERP: file lấy theo bộ lọc đang nhập (chỉ LX1), không theo bảng đang hiện"),
    ]),

    ("VII", "Xuất Excel", [
        ("001", "Tải file Excel", "P0",
         "Tài khoản G, lọc tháng 06/2026 ra dữ liệu",
         "1. Bấm 'Xuất excel'\n2. Mở file",
         "",
         "- Mở tab mới, tải file 'bao_cao_tong_hop_chi_phi_van_chuyen_theo_lai_xe.xlsx'\n"
         "- Đầu file có ảnh tiêu đề công ty của người xuất, tiêu đề 'BÁO CÁO TỔNG HỢP CHI PHÍ VẬN CHUYỂN THEO LÁI XE'\n"
         "- Dòng 'Từ ngày: 01/06/2026 đến ngày: 30/06/2026'"),

        ("002", "Cấu trúc bảng trong file", "P0",
         "File vừa tải",
         "1. Đọc tiêu đề, dòng Tổng cộng, các dòng và cuối file",
         "",
         "- 13 cột như màn hình, có tiêu đề gộp 'Chi phí'\n- Dòng 'Tổng cộng' ngay dưới tiêu đề\n"
         "- Mỗi lái xe 1 dòng, STT 1, 2, 3...\n- Cuối file có 'Ngày ... Tháng ... Năm ...' và 'Người lập'"),

        ("003", "Số liệu file khớp màn hình", "P0",
         "Như trên",
         "1. So từng cột của 3 lái xe và dòng Tổng cộng với màn hình",
         "",
         "- 5 cột tiền, KM định mức, KM thực chạy, Chênh lệch khớp màn hình\n"
         "- Ô bằng 0 trong file hiện 0 (màn hình hiện '-'), ghi nhận hành vi ERP"),

        ("004", "File áp đúng bộ lọc", "P0",
         "Đã lọc công ty TPE và nhân viên LX1",
         "1. Xuất excel",
         "",
         "- File chỉ có dòng LX1, Tổng cộng bằng dòng LX1"),

        ("005", "File gồm mọi trang", "P1",
         "Kết quả có trên 20 lái xe (2 trang)",
         "1. Đang ở trang 1, xuất excel",
         "",
         "- File có đủ mọi lái xe của cả 2 trang"),

        ("006", "% Chênh lệch dòng Tổng cộng trong file", "P1",
         "Kết quả có ít nhất 2 lái xe",
         "1. Tính tay Chênh lệch tổng chia KM định mức tổng nhân 100\n2. So với ô trong file và trên màn hình",
         "",
         "- File và màn hình cùng bằng số tính tay\n"
         "- Lỗi ERP đã biết: file đúng nhưng màn hình lệch (cộng % từng dòng)"),

        ("007", "Cột Cộng trong file", "P1",
         "Lái xe có Công tác phí khác 0",
         "1. Xuất excel, đọc cột Cộng của lái xe đó",
         "",
         "- Cộng gồm cả Công tác phí\n- Lỗi ERP đã biết: Cộng thiếu Công tác phí, giống màn hình"),

        ("008", "Xuất khi tổng KM định mức bằng 0", "P2",
         "Lái xe LX2 trong ngày chỉ có 1 phiếu hạch toán chuyến xe khác không chọn tuyến, km bằng 0",
         "1. Lọc ngày đó, chọn LX2, bấm 'Lọc' rồi 'Xuất excel'",
         "",
         "- Tải được file, ô % Chênh lệch Tổng cộng hiện 0.00% hoặc để trống\n"
         "- Lỗi ERP đã biết: tab mới báo lỗi, không tải được file"),

        ("009", "Xuất từ 1000 lái xe trở lên", "P2",
         "Kết quả lọc có từ 1000 lái xe trở lên. Dev hiện chỉ khoảng vài chục lái xe nên thường không dựng "
         "được, khi đó ghi Pending",
         "1. Bấm 'Xuất excel'\n2. Kiểm tra hộp thư",
         "",
         "- Thông báo 'Báo cáo tổng hợp chi phí vận chuyển theo lái xe sẽ gửi về mail của bạn trong ít phút!'\n"
         "- Vài phút sau nhận email kèm file\n- Lỗi ERP đã biết: email không tới"),
    ]),

    ("VIII", "Kiểm tra tăng / giảm số liệu", [
        ("001", "Ghi số nền của LX1", "P0",
         "Tài khoản G. Đã có CX1, CXK1 chờ hạch toán (section I)",
         "1. Mở báo cáo, Từ ngày đầu tháng, Đến ngày hôm nay, Công ty TPE, Nhân viên LX1, bấm 'Lọc'\n"
         "2. GHI LẠI cả 13 cột của LX1 và dòng Tổng cộng (gọi là số nền); nếu chưa có dòng thì số nền bằng 0\n"
         "3. Bỏ chọn Nhân viên, lọc lại, ghi Tổng cộng toàn TPE (gọi là T)",
         "Công ty: TPE\nNhân viên: LX1",
         "- Có số nền của LX1 và T để so ở các TC sau"),

        ("002", "Phiếu Đang tạo không làm tăng số", "P0",
         "Số nền LX1 đã ghi",
         "1. A lập phiếu hạch toán cho CX1, Km duyệt 100, bấm 'Lưu' (trạng thái Đang tạo)\n"
         "2. GHI LẠI 5 số ở khối lái xe trên phiếu, ví dụ Công lái xe 300,000, Chi phí xăng xe 600,000, Chi "
         "phí khác 50,000, Vé cầu đường 120,000, Công tác phí 100,000\n3. G lọc lại báo cáo như TC trước",
         "",
         "- Cả 13 cột của LX1 giữ nguyên số nền\n- Tổng cộng TPE vẫn bằng T"),

        ("003", "Duyệt phiếu chuyến chở hàng làm tăng đúng số", "P0",
         "Phiếu PHT1 của CX1 đang 'Đang tạo', 5 số đã ghi ở TC trước",
         "1. A mở " + MENU_PHT + ", Sửa PHT1, bấm 'Lưu và duyệt'\n2. G lọc lại báo cáo như TC 001",
         "",
         "- Công lái xe = nền + 300,000; Xăng xe = nền + 600,000; Khác = nền + 50,000\n"
         "- Công tác phí = nền + 100,000; Vé cầu đường = nền + 120,000\n"
         "- Cộng = nền + 1,170,000 (đủ 5 khoản)\n"
         "- KM định mức = nền + 100; KM thực chạy = nền + 110; Chênh lệch = nền + 10\n"
         "- Tổng cộng TPE = T cộng đúng các phần tăng trên\n"
         "- Lỗi ERP đã biết: Cộng chỉ tăng 1,070,000 (thiếu Công tác phí)"),

        ("004", "Duyệt phiếu chuyến xe khác làm tăng đúng số", "P0",
         "Đã làm TC trên, ghi lại số mới của LX1 làm số nền 2",
         "1. A mở " + MENU_CHO_HT_K + ", lập phiếu PHK1 cho CXK1, Km duyệt 40, ghi 5 số khối lái xe\n"
         "2. Bấm 'Lưu và duyệt'\n3. G lọc lại báo cáo",
         "",
         "- Mỗi cột tiền của LX1 = số nền 2 cộng đúng số tương ứng trên PHK1\n"
         "- KM định mức = số nền 2 + 40; KM thực chạy = số nền 2 + 45\n"
         "- LX1 vẫn chỉ 1 dòng"),

        ("005", "Khoản bằng 0 không làm đổi cột", "P1",
         "Chuyến CX2 của LX1 không có vé cầu đường và công tác phí",
         "1. A lập và 'Lưu và duyệt' phiếu cho CX2\n2. G lọc lại",
         "",
         "- Cột Vé cầu đường và Công tác phí của LX1 không đổi\n- Các cột khác tăng đúng số trên phiếu"),

        ("006", "Phiếu ngoài khoảng ngày không tính", "P0",
         "PHT1 duyệt hôm nay; CX1 chạy từ hôm qua",
         "1. G lọc Từ ngày đầu tháng, Đến ngày HÔM QUA, chọn LX1",
         "",
         "- Số của LX1 KHÔNG gồm PHT1 và PHK1\n- Lọc đến hôm nay thì có lại"),

        ("007", "Không có thao tác làm giảm số trên giao diện", "P1",
         "PHT1 đã hạch toán; có thêm phiếu PHT2 đang 'Đang tạo' do A lập",
         "1. A mở " + MENU_PHT + ", bấm bánh răng dòng PHT1\n2. Bấm bánh răng dòng PHT2, chọn 'Xóa'\n"
         "3. G lọc lại báo cáo",
         "",
         "- Bước 1: PHT1 chỉ còn In, Xuất excel, không có Sửa / Xóa\n"
         "- Bước 2: ghi nhận hành vi ERP, báo 'Không được xóa!'\n"
         "- Bước 3: số LX1 không đổi\n"
         "- Ghi nhận: muốn giảm số phải nhờ quản trị xử lý dữ liệu, không làm được trên giao diện"),

        ("008", "Chuyến xe thuê ngoài không làm tăng số", "P0",
         "CX9 dùng xe thuê ngoài, lái xe ngoài. Ghi Tổng cộng toàn công ty T2",
         "1. A lập phiếu cho CX9, bấm 'Lưu và duyệt'\n2. G lọc lại",
         "",
         "- Không xuất hiện dòng lái xe mới\n- Tổng cộng các cột vẫn bằng T2"),

        ("009", "Lái xe công ty khác", "P0",
         "Chuyến của LX3 (TPV) chờ hạch toán. Tài khoản B (quyền theo công ty TPE) ghi Tổng cộng T3",
         "1. Kế toán TPV lập và 'Lưu và duyệt' phiếu cho chuyến của LX3\n2. B lọc lại\n"
         "3. G lọc với Công ty TPV, chọn LX3",
         "",
         "- Bước 2: Tổng cộng của B vẫn bằng T3, không có dòng LX3\n"
         "- Bước 3: LX3 tăng đúng 5 số trên phiếu vừa duyệt"),

        ("010", "Chỉ lái xe có phiếu mới thay đổi", "P1",
         "Ghi số của LX2 trước TC 003",
         "1. Sau TC 003, lọc lại không chọn Nhân viên, tìm LX2",
         "",
         "- Mọi cột của LX2 không đổi\n- Phần tăng của Tổng cộng bằng đúng phần tăng của LX1"),

        ("011", "Tài khoản không quyền thấy số tăng khi chính mình lập phiếu", "P1",
         "Tài khoản N (không quyền xem, có quyền hạch toán). Ghi số LX1 mà N đang thấy (thường bằng 0)",
         "1. N lập phiếu cho chuyến CX3 của LX1, bấm 'Lưu và duyệt'\n2. N lọc lại báo cáo",
         "",
         "- LX1 tăng đúng 5 số trên phiếu N vừa duyệt\n- Không thấy số của PHT1, PHK1 do A lập"),
    ]),

    ("IX", "Đối chiếu với báo cáo chi tiết", [
        ("001", "Bấm tên lái xe mở báo cáo chi tiết", "P0",
         "Tài khoản G, lọc tháng 06/2026",
         "1. Bấm tên lái xe Lê Văn Trình\n2. Ở tab mới bấm 'Lọc'",
         "",
         "- Mở 'BÁO CÁO CHI TIẾT CHI PHÍ VẬN CHUYỂN THEO LÁI XE' ở tab mới, đã điền sẵn Từ ngày, Đến ngày và "
         "Nhân viên\n- Ghi nhận hành vi ERP: phải bấm 'Lọc' mới ra số\n"
         "- Dòng lái xe ở báo cáo chi tiết khớp từng cột với dòng ở báo cáo tổng hợp"),

        ("002", "Tổng cộng 2 báo cáo bằng nhau cùng bộ lọc", "P0",
         "Tài khoản G",
         "1. Báo cáo tổng hợp: lọc 01/06/2026 đến 30/06/2026, không chọn Công ty, Nhân viên, ghi dòng Tổng cộng\n"
         "2. Mở " + MENU_CHI_TIET + ", cùng khoảng ngày, để trống mọi ô lọc khác, bấm 'Lọc'",
         "",
         "- Tổng cộng 5 cột tiền, Cộng, KM định mức, KM thực chạy, Chênh lệch bằng nhau ở 2 báo cáo\n"
         "- Số lái xe 2 bên bằng nhau\n"
         "- Lỗi ERP đã biết: ô % Chênh lệch Tổng cộng lệch, báo cáo chi tiết tính đúng còn báo cáo tổng hợp cộng % từng dòng"),

        ("003", "Đối chiếu theo công ty", "P1",
         "Tài khoản G",
         "1. Lặp lại TC trên với Công ty TPV ở cả 2 báo cáo",
         "",
         "- Tổng cộng các cột tiền và KM của 2 báo cáo bằng nhau"),
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
