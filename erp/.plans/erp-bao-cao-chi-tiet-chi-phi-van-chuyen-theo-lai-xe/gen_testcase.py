# -*- coding: utf-8 -*-
"""Generate testcase Excel cho man ERP: Bao cao chi tiet chi phi van chuyen theo lai xe.

Viet cho MAN ERP GOC (TanPhatDev, nhom duong dan report.detailTransportByDriver*), de tester
nam luong ERP tren dev truoc khi port sang HRM.

Chay:  PYTHONIOENCODING=utf-8 python gen_testcase.py
Output: testcase - Bao cao chi tiet chi phi van chuyen theo lai xe.xlsx (cung thu muc)
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

OUTPUT_FILE = os.path.join(HERE, "testcase - Bao cao chi tiet chi phi van chuyen theo lai xe.xlsx")
FEATURE_NAME = "Báo cáo chi tiết chi phí vận chuyển theo lái xe (ERP)"
MODULE_NAME = "Kho - Báo cáo vận chuyển"

MENU = ("menu Kho > Vận chuyển - Bốc xếp > nhóm 'Báo cáo vận chuyển' > 'Báo cáo chi tiết chi phí vận "
        "chuyển theo lái xe'")
MENU_TH = ("menu Kho > Vận chuyển - Bốc xếp > nhóm 'Báo cáo vận chuyển' > 'Báo cáo tổng hợp chi phí vận "
           "chuyển theo lái xe'")
MENU_CX = "menu Kho > Vận chuyển - Bốc xếp > 'Chuyến xe chở hàng'"
MENU_CK = "menu Kho > Vận chuyển - Bốc xếp > 'Chuyến xe khác'"
MENU_CHO_HT = ("menu Kế toán > Hàng hoá - Dịch vụ - Vận chuyển > nhóm 'Vận chuyển' > 'Chuyến xe chở hàng "
               "chờ hạch toán'")
MENU_CHO_HT_K = ("menu Kế toán > Hàng hoá - Dịch vụ - Vận chuyển > nhóm 'Vận chuyển' > 'Chuyến xe khác chờ "
                 "hạch toán'")
MENU_PHT = ("menu Kế toán > Hàng hoá - Dịch vụ - Vận chuyển > nhóm 'Vận chuyển' > 'Phiếu hạch toán chuyến "
            "xe chở hàng'")

Q_TCT = "Xem báo cáo vận chuyển theo công ty theo tổng công ty"
Q_CT = "Xem báo cáo vận chuyển theo công ty"
Q_HT = "Hạch toán chuyến xe chở hàng"
Q_HT_K = "Hạch toán chuyến xe khác"
Q_DUYET = "Duyệt hạch toán chuyến xe"

COLS = ("STT · Mã lái xe · Thời gian · Tải trọng tính cước · Dòng xe tính cước · Xe chạy thực tế · Phiếu "
        "hoạch toán · Chuyến xe · Tuyến đường · Công lái xe · Chi phí (2 cột con Xăng xe, Khác) · Công tác "
        "phí · Vé cầu đường · Cộng · KM định mức · KM thực chạy · Chênh lệch (KM) · % Chênh lệch")

# =========================================================================
# 9 MUC MO TA
# =========================================================================
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Báo cáo liệt kê CHI PHÍ CỦA LÁI XE CÔNG TY theo từng chuyến: công lái xe, xăng xe, chi phí khác, công "
     "tác phí, vé cầu đường, kèm KM định mức, KM thực chạy và phần chênh lệch KM. Gom theo Lái xe > từng "
     "phiếu hạch toán chuyến xe. Màn chỉ để xem, không sửa dữ liệu.\n"
     "Đường vào: " + MENU + ". Tiêu đề trang 'BÁO CÁO CHI TIẾT CHI PHÍ VẬN CHUYỂN THEO LÁI XE'.\n"
     "Lối vào thứ 2: ở " + MENU_TH + ", bấm tên một lái xe, báo cáo chi tiết mở ở tab mới, điền sẵn Từ ngày, "
     "Đến ngày và lái xe đó, nhưng KHÔNG tự lọc, phải bấm 'Lọc' mới ra số.\n"
     "Nguồn số: các dòng hạch toán chi phí lái xe sinh ra khi kế toán bấm 'Lưu và duyệt' trên 'Phiếu hạch "
     "toán chuyến xe chở hàng' hoặc 'Phiếu hạch toán chuyến xe khác'."),

    ("2. Đối tượng được tính / hiển thị",
     "Một khoản tiền được cộng vào báo cáo khi thỏa ĐỦ:\n"
     "- Thuộc phiếu hạch toán chuyến xe chở hàng hoặc phiếu hạch toán chuyến xe khác ở trạng thái 'Đã hạch "
     "toán' (bấm 'Lưu và duyệt').\n"
     "- Chuyến xe có lái xe là NHÂN VIÊN CÔNG TY (xe chọn lái xe thuộc công ty).\n"
     "- Là 1 trong 5 khoản: Công lái xe, Xăng xe, Chi phí khác, Vé cầu đường, Công tác phí.\n"
     "- Ngày hạch toán nằm trong khoảng Từ ngày - Đến ngày (lấy trọn 2 ngày đầu và cuối).\n"
     "- Nằm trong phạm vi quyền xem (mục 7).\n"
     "Giá trị 5 khoản lấy đúng số hiện ở khối lái xe của phiếu hạch toán: Công lái xe, Chi phí xăng xe, Chi "
     "phí khác tính theo công thức vận chuyển (dòng xe + tải trọng) nhân Km duyệt; Vé cầu đường và Công tác "
     "phí lấy từ chuyến xe."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu hạch toán còn 'Đang tạo' (mới bấm 'Lưu'): chưa có số, không hiện.\n"
     "- Chuyến xe dùng lái xe thuê ngoài: không có chi phí lái xe, không hiện.\n"
     "- Khoản bằng 0 không được ghi nhận (ô hiện '-').\n"
     "- Các khoản cước vận chuyển chia cho kinh doanh, thuế, công nợ nhà xe không thuộc báo cáo này.\n"
     "- Khi lọc Tải trọng xe, Dòng xe, Tuyến đường, Biển số xe, Phiếu hoạch toán: chuyến không khớp bị loại "
     "ở cả dòng lái xe và dòng chi tiết; lái xe không còn chuyến nào khớp thì biến mất."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Từ ngày và Đến ngày là BẮT BUỘC (nút 'Lọc' khóa tới khi nhập đủ 2 ô). Lọc theo NGÀY HẠCH TOÁN = thời "
     "điểm kế toán bấm 'Lưu và duyệt' phiếu hạch toán, không theo ngày chạy chuyến xe.\n"
     "Cột 'Thời gian' ở dòng chi tiết hiện ngày cập nhật cuối của phiếu hạch toán (thường trùng ngày hạch "
     "toán vì phiếu đã hạch toán không sửa được).\n"
     "Màn không tự tải dữ liệu, kể cả khi mở từ báo cáo tổng hợp: phải bấm 'Lọc'."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Bảng 2 cấp, 19 cột: " + COLS + ".\n"
     "- Cấp 1 Lái xe (STT 1, 2...; chữ đậm): Mã lái xe là mã nhân viên trong hồ sơ nhân sự, tên lái xe gộp "
     "qua 7 cột, các cột tiền và KM là tổng của lái xe. Lái xe xếp theo họ tên A-Z.\n"
     "- Cấp 2 Chi tiết (STT 1.1, 1.2...): mỗi PHIẾU HẠCH TOÁN của lái xe là 1 dòng. Dòng chuyến xe chở hàng "
     "đứng trước, dòng chuyến xe khác đứng sau. Luôn hiện, không có ô bật / tắt.\n"
     "- Dòng 'Tổng cộng' ngay dưới tiêu đề.\n"
     "Phân trang: 20 LÁI XE mỗi trang."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Dòng chi tiết = tổng từng khoản của lái xe trên 1 phiếu hạch toán.\n"
     "- Dòng lái xe = tổng các dòng chi tiết của lái xe đó.\n"
     "- KM định mức = KM của tuyến đường nhân 2 nếu chuyến tích 'Đi 2 chiều'. Chuyến xe khác không chọn "
     "tuyến thì lấy KM nhập trên chuyến. KHÔNG dùng Km duyệt.\n"
     "- KM thực chạy = Km lúc về trừ Km lúc đi. Chênh lệch (KM) = KM thực chạy trừ KM định mức.\n"
     "- % Chênh lệch = Chênh lệch chia KM định mức nhân 100. Ở dòng lái xe và dòng Tổng cộng tính bằng "
     "tổng chênh lệch chia tổng KM định mức (không cộng các %).\n"
     "- Dòng 'Tổng cộng' = tổng mọi lái xe của MỌI trang.\n"
     "- Cùng một người có 2 tài khoản nhân viên thì thành 2 dòng lái xe riêng."),

    ("7. Phân quyền cấp",
     "Menu và màn mở được với mọi tài khoản đăng nhập. Phạm vi dữ liệu theo quyền (tên hiển thị trong màn "
     "phân quyền):\n"
     "- '" + Q_TCT + "': thấy lái xe của mọi công ty; có ô Công ty (lọc theo công ty của lái xe lúc hạch "
     "toán); ô Nhân viên có nhân viên mọi công ty.\n"
     "- '" + Q_CT + "': chỉ lái xe thuộc công ty mình; không có ô Công ty.\n"
     "- Không có 2 quyền trên: chỉ thấy các phiếu hạch toán DO CHÍNH MÌNH LẬP (không phải chi phí của chính "
     "mình). Lái xe tự mở báo cáo sẽ không thấy gì nếu không tự lập phiếu.\n"
     "Phạm vi quyền áp cả cho Xuất excel.\n"
     "Quyền liên quan khi chuẩn bị dữ liệu: '" + Q_HT + "', '" + Q_HT_K + "' (lập phiếu hạch toán), '" +
     Q_DUYET + "' (xem danh sách chuyến chờ hạch toán)."),

    ("8. Cách tính các ô thống kê",
     "- Ô tiền làm tròn, phân cách hàng nghìn bằng dấu phẩy (vd 1,250,000). Ở dòng lái xe và dòng chi tiết, "
     "ô bằng 0 hiện dấu '-'; ở dòng Tổng cộng hiện số 0.\n"
     "- Cột 'Cộng' hiện tại = Công lái xe + Xăng xe + Khác + Vé cầu đường (KHÔNG gồm Công tác phí), xem lỗi "
     "(1) mục 9.\n"
     "- % Chênh lệch ở dòng lái xe / chi tiết làm tròn XUỐNG 2 chữ số thập phân; ở dòng Tổng cộng làm tròn "
     "thường 2 chữ số.\n"
     "- Xuất excel: lấy toàn bộ lái xe khớp bộ lọc (mọi trang) kèm dòng chi tiết, tải file ngay."),

    ("9. Ghi chú đọc bảng",
     "Các lỗi ERP ĐÃ BIẾT được viết thành testcase với kết quả mong đợi ĐÚNG, kèm dòng 'Lỗi ERP đã biết'. "
     "Chạy thấy đúng hiện tượng lỗi thì ghi Failed và chép câu đó vào cột Ghi chú:\n"
     "(1) Cột 'Cộng' trên màn hình (dòng lái xe, dòng chi tiết, dòng Tổng cộng) và dòng Tổng cộng của Excel "
     "KHÔNG cộng Công tác phí, trong khi dòng lái xe / dòng chi tiết của Excel CÓ cộng. Hai nơi lệch nhau "
     "đúng bằng Công tác phí. Bộ TC lấy kết quả đúng là 'Cộng' gồm đủ 5 khoản đứng trước nó; cần nghiệp vụ "
     "xác nhận lại.\n"
     "(2) File Excel: ô Công tác phí ở dòng Tổng cộng luôn bằng 0.\n"
     "(3) File Excel: tiêu đề cột ghi sai chính tả 'Xe chạy thức tế'.\n"
     "Hành vi lạ nhưng là thiết kế hiện tại (ghi 'Ghi nhận hành vi ERP', không tính Failed): tài khoản không "
     "có quyền chỉ thấy phiếu do mình lập; nút làm mới không xóa bảng; Excel lấy bộ lọc đang nhập chứ không "
     "phải bộ lọc của lần Lọc gần nhất; nhiều lái xe vẫn tải file ngay, không chuyển sang gửi email; phiếu "
     "hạch toán đã hạch toán không có Sửa / Xóa nên số liệu không giảm được qua giao diện.\n"
     "Nhóm TC dùng công cụ kiểm thử API dành cho tester kỹ thuật.\n"
     "Câu truy vấn trong thư mục sql (chỉ đọc): câu 1 tìm lái xe có số liệu theo tháng, câu 2 liệt kê từng "
     "phiếu hạch toán của 1 lái xe để đối chiếu từng dòng chi tiết.\n"
     "Dữ liệu mẫu dùng trong bộ TC:\n"
     "- Công ty TPE và TPV. Lái xe LX1, LX2 là nhân viên TPE; LX3 là nhân viên TPV.\n"
     "- Xe XE1 của TPE, lái xe thuộc công ty, dòng xe 'Xe tải', tải trọng '1 tấn', biển số 29D-11111. Xe XE9 "
     "dùng lái xe thuê ngoài.\n"
     "- Tuyến TD1 dài 50 km.\n"
     "- Chuyến CX1 (chở hàng): XE1, lái xe LX1, tuyến TD1, tích 'Đi 2 chiều', Km lúc đi 12,000, Km lúc về "
     "12,110. Phiếu hạch toán PHT1 của CX1, ví dụ khối lái xe hiện: Công lái xe 150,000, Chi phí xăng xe "
     "300,000, Chi phí khác 50,000, Vé cầu đường 40,000, Công tác phí 100,000.\n"
     "- Chuyến CK1 (chuyến xe khác): XE1, lái xe LX1, không chọn tuyến, điểm đầu 'Kho Liên Ninh', điểm cuối "
     "'Bắc Ninh', KM 40, một chiều, Km lúc đi 12,200, Km lúc về 12,236. Phiếu PHT2: Công lái xe 80,000, Xăng "
     "120,000, Khác 0, Vé cầu đường 20,000, Công tác phí 0.\n"
     "- Tài khoản: TCT có quyền '" + Q_TCT + "'. CT thuộc TPE có quyền '" + Q_CT + "'. KT là kế toán TPE có '" +
     Q_HT + "', '" + Q_HT_K + "', '" + Q_DUYET + "', không có quyền xem báo cáo. TK-LX1 là tài khoản của "
     "lái xe LX1, không có quyền nào.\n"
     "Số tiền thật trên dev phụ thuộc công thức vận chuyển đang khai báo: tester ghi lại đúng số hiện trên "
     "phiếu hạch toán rồi thay vào các con số ví dụ."),
]

# =========================================================================
# SECTION PHAN QUYEN
# =========================================================================
ROLE_TCS = [
    ("00", "Quyền theo tổng công ty thấy mọi công ty", "P0",
     "Tài khoản TCT có quyền '" + Q_TCT + "'\n"
     "Tháng 09/2026 có PHT1 của LX1 (TPE) và một phiếu của LX3 (TPV) đã hạch toán",
     "1. Đăng nhập TCT, mở " + MENU + "\n2. Quan sát bộ lọc, mở ô Nhân viên\n"
     "3. Từ ngày 01/09/2026, Đến ngày 30/09/2026, bấm 'Lọc'",
     "Tài khoản: TCT",
     "- Có ô 'Công ty' với danh sách mọi công ty\n- Ô Nhân viên có nhân viên của mọi công ty\n"
     "- Bảng có cả LX1 và LX3"),

    ("01", "Ô Công ty lọc theo công ty của lái xe", "P0",
     "Như TC trước",
     "1. Ô Công ty chọn TPV\n2. Mở ô Nhân viên\n3. Bấm 'Lọc'",
     "Công ty: TPV",
     "- Ô Nhân viên chỉ còn nhân viên TPV\n- Bảng chỉ còn lái xe của TPV (có LX3, không có LX1)\n"
     "- Tổng cộng chỉ tính lái xe TPV\n"
     "- Lọc theo công ty của LÁI XE, không theo công ty của người lập phiếu"),

    ("02", "Quyền theo công ty chỉ thấy lái xe công ty mình", "P0",
     "Tài khoản CT thuộc TPE, chỉ có quyền '" + Q_CT + "'",
     "1. Đăng nhập CT, mở màn\n2. Quan sát bộ lọc, mở ô Nhân viên\n3. Lọc tháng 09/2026",
     "Tài khoản: CT",
     "- KHÔNG có ô Công ty\n- Ô Nhân viên chỉ có nhân viên TPE\n"
     "- Bảng có LX1, LX2; KHÔNG có LX3 (TPV)"),

    ("03", "Không có quyền xem: chỉ thấy phiếu do mình lập", "P0",
     "Tài khoản KT không có 2 quyền xem báo cáo, đã tự lập PHT1 (LX1). Phiếu hạch toán của LX2 trong tháng "
     "do người khác lập",
     "1. Đăng nhập KT, mở màn\n2. Lọc tháng 09/2026",
     "Tài khoản: KT",
     "- Không có ô Công ty\n- Bảng chỉ có LX1 với dòng chi tiết PHT1\n- Không có LX2\n"
     "- Ghi nhận hành vi ERP: phạm vi theo NGƯỜI LẬP phiếu hạch toán, không theo lái xe"),

    ("04", "Lái xe không có quyền tự mở báo cáo", "P1",
     "Tài khoản TK-LX1 không có quyền nào; tháng 09/2026 LX1 có PHT1 do KT lập",
     "1. Đăng nhập TK-LX1, mở màn\n2. Lọc tháng 09/2026",
     "Tài khoản: TK-LX1",
     "- Màn mở được, không báo thiếu quyền\n- Bảng 'Chưa có dữ liệu'\n"
     "- Ghi nhận hành vi ERP: lái xe không xem được chi phí của chính mình nếu không tự lập phiếu"),

    ("05", "Menu hiện với mọi tài khoản", "P1",
     "Tài khoản bất kỳ không thuộc khối vận tải, không có quyền nào",
     "1. Đăng nhập, mở menu Kho > Vận chuyển - Bốc xếp",
     "",
     "- Thấy mục 'Báo cáo chi tiết chi phí vận chuyển theo lái xe' trong nhóm 'Báo cáo vận chuyển'\n"
     "- Bấm vào mở được màn"),

    ("06", "Có cả 2 quyền thì theo phạm vi rộng hơn", "P2",
     "Tài khoản có cả '" + Q_TCT + "' và '" + Q_CT + "'",
     "1. Mở màn, lọc tháng 09/2026",
     "",
     "- Có ô Công ty, thấy lái xe mọi công ty (giống tài khoản TCT)"),

    ("07", "Phạm vi quyền áp cả cho Xuất excel", "P1",
     "Tài khoản CT (TPE)",
     "1. Lọc tháng 09/2026\n2. Bấm 'Xuất excel', mở file",
     "Tài khoản: CT",
     "- File chỉ có lái xe TPE, khớp màn hình\n- Không có LX3"),

    ("08", "Không vượt phạm vi khi gọi thẳng chức năng", "P2",
     "Tài khoản CT (TPE). Dành cho tester kỹ thuật",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng tìm dữ liệu của báo cáo, kèm điều kiện Công ty = TPV\n"
     "2. Lặp lại với chức năng Xuất excel",
     "Công ty: TPV",
     "- Cả 2 lần đều chỉ ra lái xe TPE, điều kiện công ty bị bỏ qua\n- Không lộ số liệu của TPV"),
]

# =========================================================================
# CAC SECTION CHUC NANG
# =========================================================================
SECTIONS = [
    ("I", "Chuẩn bị dữ liệu test", [
        ("001", "Tìm lái xe có sẵn số liệu trên dev", "P0",
         "Có quyền chạy câu truy vấn trên dữ liệu dev, hoặc nhờ người hỗ trợ chạy",
         "1. Chạy câu số 1 trong thư mục sql, sửa khoảng ngày cho đúng tháng cần test\n"
         "2. Chọn 1 lái xe có nhiều phiếu, có Công tác phí khác 0, ghi lại tên, công ty và các cột tiền\n"
         "3. Chạy câu số 2 với lái xe đó và cùng khoảng ngày\n"
         "4. Mở báo cáo bằng tài khoản TCT, lọc đúng khoảng ngày, chọn lái xe đó",
         "Lái xe lấy từ câu truy vấn",
         "- Số dòng chi tiết dưới lái xe = số dòng của câu số 2\n"
         "- Các cột Công lái xe, Xăng xe, Khác, Công tác phí, Vé cầu đường của dòng lái xe khớp câu số 1\n"
         "- Cột 'Cộng' khớp cột cộng 4 khoản của câu số 1 (xem lỗi (1) mục 9)"),

        ("002", "Chuẩn bị đủ tài khoản test", "P0",
         "Quản trị có quyền phân quyền",
         "1. Gán cho TCT quyền '" + Q_TCT + "'\n2. Gán cho CT (TPE) quyền '" + Q_CT + "'\n"
         "3. Gán cho KT (TPE) quyền '" + Q_HT + "', '" + Q_HT_K + "', '" + Q_DUYET + "', KHÔNG gán 2 quyền xem "
         "báo cáo\n4. Để TK-LX1 không có quyền nào",
         "Tài khoản TCT, CT, KT, TK-LX1",
         "- Đăng nhập lại, KT thấy mục 'Chuyến xe chở hàng chờ hạch toán' ở menu Kế toán\n"
         "- TCT thấy ô Công ty trên báo cáo, CT và KT không thấy"),

        ("003", "Chuẩn bị xe, tuyến và công thức vận chuyển", "P1",
         "Xe XE1 của TPE, lái xe thuộc công ty, có lái xe LX1 và LX2; tuyến TD1 dài 50 km",
         "1. Kiểm tra XE1 có dòng xe 'Xe tải', tải trọng '1 tấn', biển số 29D-11111\n"
         "2. Kiểm tra công thức vận chuyển của TPE có khai báo dòng xe 'Xe tải' tải trọng '1 tấn'\n"
         "3. Kiểm tra TPE đang có bảng giá vận chuyển hiệu lực",
         "XE1, TD1",
         "- Đủ 3 điều kiện thì phiếu hạch toán mới tính được chi phí lái xe\n"
         "- Thiếu công thức thì khi lưu phiếu hạch toán báo 'Không tìm thấy xe, trọng tải tuyến đường phù hợp "
         "trong công thức vận chuyển'\n- Thiếu bảng giá báo 'Chưa có bảng giá hiệu lực !'"),

        ("004", "Tạo chuyến xe chở hàng CX1 cho LX1", "P0",
         "Có ít nhất 1 phiếu xuất kho của TPE chưa xếp chuyến",
         "1. Vào " + MENU_CX + ", lập chuyến mới: chọn XE1, lái xe LX1, tuyến TD1, tích 'Đi 2 chiều', gắn "
         "phiếu xuất kho\n2. Nhập Km lúc đi 12,000, Km lúc về 12,110, Vé cầu đường 40,000, Công tác phí "
         "100,000\n3. Làm tiếp các bước của chuyến cho tới khi chuyến ở trạng thái 'Chờ hạch toán'\n"
         "4. Đăng nhập KT, mở " + MENU_CHO_HT,
         "Km lúc đi: 12,000\nKm lúc về: 12,110\nVé cầu đường: 40,000\nCông tác phí: 100,000",
         "- CX1 hiện trong danh sách 'Chuyến xe chở hàng chờ hạch toán' của KT\n"
         "- Nút bánh răng của CX1 có mục 'Hạch toán chuyến xe'"),

        ("005", "Lập phiếu hạch toán PHT1 ở trạng thái Đang tạo", "P0",
         "Đã có CX1 chờ hạch toán. Đăng nhập KT",
         "1. Ở dòng CX1 bấm bánh răng > 'Hạch toán chuyến xe'\n2. Nhập Km duyệt, chia hết cước vận chuyển cho "
         "các phiếu xuất của chuyến\n3. Đọc khối lái xe: Tên lái xe, Công lái xe, Chi phí xăng xe, Chi phí "
         "khác, Vé cầu đường, Công tác phí và GHI LẠI 5 số tiền\n4. Bấm 'Lưu'",
         "Km duyệt: 100",
         "- Khối lái xe hiện 'Tên lái xe: LX1' và 5 số tiền (ví dụ 150,000 · 300,000 · 50,000 · 40,000 · "
         "100,000)\n- Lưu xong phiếu PHT1 trạng thái 'Đang tạo', chuyến CX1 chuyển 'Đang hạch toán'\n"
         "- Tổng cước đã chia khác cước thực tế thì báo 'Tổng cước đã chia không bằng tổng cước vận chuyển "
         "thực tế', không lưu"),

        ("006", "Tạo chuyến xe khác CK1 và phiếu hạch toán PHT2", "P1",
         "XE1, lái xe LX1",
         "1. Vào " + MENU_CK + ", lập chuyến không chọn tuyến: điểm đầu 'Kho Liên Ninh', điểm cuối 'Bắc Ninh', "
         "KM 40, không tích 'Đi 2 chiều', Km lúc đi 12,200, Km lúc về 12,236\n"
         "2. Đưa chuyến tới trạng thái chờ hạch toán\n3. KT vào " + MENU_CHO_HT_K + ", lập phiếu hạch toán "
         "PHT2, ghi lại 5 số tiền ở khối lái xe, bấm 'Lưu'",
         "KM: 40\nKm lúc đi: 12,200\nKm lúc về: 12,236",
         "- PHT2 ở trạng thái 'Đang tạo'\n- Khối lái xe ví dụ: Công lái xe 80,000, Chi phí xăng xe 120,000, "
         "Chi phí khác 0, Vé cầu đường 20,000, Công tác phí 0"),

        ("007", "Chuẩn bị dữ liệu đối chứng", "P1",
         "Có LX2 (TPE), LX3 (TPV), xe XE9 dùng lái xe thuê ngoài",
         "1. Lập và 'Lưu và duyệt' 1 phiếu hạch toán cho chuyến của LX2 trong tháng 09/2026\n"
         "2. Lập và 'Lưu và duyệt' 1 phiếu hạch toán cho chuyến của LX3 (TPV)\n"
         "3. Lập chuyến CX9 bằng XE9 (lái xe thuê ngoài) và 'Lưu và duyệt' phiếu hạch toán của CX9",
         "",
         "- Phiếu của LX2, LX3 ở trạng thái 'Đã hạch toán'\n"
         "- Phiếu của CX9 không có khối lái xe công ty (không có Công lái xe, Chi phí xăng xe...)"),
    ]),

    ("II", "Giao diện & mở màn", [
        ("001", "Bố cục màn hình khi mở", "P0",
         "Tài khoản TCT",
         "1. Mở " + MENU + "\n2. Quan sát",
         "",
         "- Tiêu đề trang 'BÁO CÁO CHI TIẾT CHI PHÍ VẬN CHUYỂN THEO LÁI XE'\n"
         "- Khối 'Bộ lọc': Từ ngày* · Đến ngày* · Công ty · Nhân viên · Phiếu hoạch toán · Tải trọng xe · Dòng "
         "xe · Tuyến đường · Biển số xe\n"
         "- Nút 'Xuất excel', nút 'Lọc', nút làm mới (mũi tên xoay vòng)\n- Khối 'Chi tiết' chứa bảng và phân "
         "trang"),

        ("002", "Trạng thái mặc định khi mở từ menu", "P0",
         "Vừa mở màn",
         "1. Quan sát ô ngày, nút Lọc, bảng",
         "",
         "- Từ ngày, Đến ngày để trống, nhãn có dấu * bắt buộc\n- Nút 'Lọc' bị khóa (mờ)\n"
         "- Bảng hiện 'Chưa có dữ liệu'; dòng Tổng cộng trống\n- Màn không tự tải dữ liệu"),

        ("003", "Tiêu đề 19 cột và dòng Tổng cộng", "P0",
         "Đã mở màn",
         "1. Đọc tiêu đề bảng",
         "",
         "- Đúng thứ tự: " + COLS + "\n"
         "- Ngay dưới tiêu đề là dòng 'Tổng cộng' gộp 9 cột đầu, các ô tổng nằm từ cột Công lái xe"),

        ("004", "Nút Xuất excel khi chưa có dữ liệu", "P1",
         "Vừa mở màn, hoặc lọc ra 'Chưa có dữ liệu'",
         "1. Bấm 'Xuất excel'",
         "",
         "- Nút mờ, bấm không mở tab tải file"),

        ("005", "Mở từ báo cáo tổng hợp theo lái xe", "P0",
         "Tài khoản TCT\nỞ " + MENU_TH + " đã lọc 01/09/2026 - 30/09/2026, có dòng LX1",
         "1. Bấm tên LX1 ở cột 'Nhân viên lái xe'\n2. Quan sát tab mới\n3. Bấm 'Lọc'",
         "",
         "- Báo cáo chi tiết mở ở tab mới\n- Từ ngày 01/09/2026, Đến ngày 30/09/2026, Nhân viên LX1 đã điền sẵn\n"
         "- Bước 2: bảng chưa có số. Ghi nhận hành vi ERP: không tự lọc\n"
         "- Bước 3: chỉ có LX1 kèm các dòng chi tiết"),

        ("006", "Ô ngày", "P2",
         "Đã mở màn",
         "1. Bấm ô Từ ngày, chọn ngày trên lịch",
         "",
         "- Ngày hiện dạng ngày/tháng/năm (vd 01/09/2026)"),

        ("007", "Trạng thái đang tải", "P2",
         "Đã nhập đủ 2 ngày, khoảng ngày dài",
         "1. Bấm 'Lọc', quan sát ngay",
         "",
         "- Dòng Tổng cộng hiện 'Đang tải dữ liệu' có biểu tượng quay\n"
         "- Nút Lọc, làm mới, Xuất excel bị khóa trong lúc tải"),

        ("008", "Thu gọn / mở khối Bộ lọc", "P2",
         "Đã nhập vài ô lọc",
         "1. Bấm mũi tên góc phải khối 'Bộ lọc'\n2. Bấm lại",
         "",
         "- Khối thu gọn rồi mở lại, giá trị đã nhập giữ nguyên"),

        ("009", "Danh sách ô Nhân viên", "P2",
         "Tài khoản TCT",
         "1. Mở ô Nhân viên, gõ tìm một nhân viên kinh doanh (không phải lái xe)\n"
         "2. Chọn Công ty TPE, mở lại ô Nhân viên",
         "",
         "- Bước 1: danh sách gồm mọi nhân viên, không chỉ lái xe\n"
         "- Bước 2: chỉ còn nhân viên TPE; nhân viên đã chọn trước đó bị xóa khỏi ô"),
    ]),

    ("III", "Bộ lọc", [
        ("001", "Chỉ nhập một ô ngày", "P0",
         "Đã mở màn",
         "1. Nhập Từ ngày 01/09/2026, để trống Đến ngày\n2. Thử bấm 'Lọc'",
         "",
         "- Nút 'Lọc' vẫn khóa"),

        ("002", "Lọc theo ngày hạch toán", "P0",
         "PHT1 của LX1 bấm 'Lưu và duyệt' ngày 15/09/2026; phiếu PHT3 của LX1 bấm 'Lưu và duyệt' ngày 02/10/2026",
         "1. Lọc 01/09/2026 - 30/09/2026\n2. Đọc các dòng chi tiết của LX1",
         "",
         "- Có PHT1, không có PHT3\n- Lọc 01/10/2026 - 31/10/2026 thì ngược lại"),

        ("003", "Lấy trọn ngày đầu và ngày cuối", "P1",
         "Phiếu PHT1 hạch toán lúc 17:30 ngày 30/09/2026",
         "1. Lọc 30/09/2026 - 30/09/2026",
         "",
         "- PHT1 có trong kết quả"),

        ("004", "Ngày chạy chuyến khác ngày hạch toán", "P1",
         "Chuyến CX1 chạy ngày 29/09/2026, PHT1 được 'Lưu và duyệt' ngày 01/10/2026",
         "1. Lọc 01/09/2026 - 30/09/2026\n2. Lọc 01/10/2026 - 31/10/2026",
         "",
         "- Lần 1 không có PHT1\n- Lần 2 có PHT1 (lọc theo ngày hạch toán, không theo ngày chạy)"),

        ("005", "Từ ngày lớn hơn Đến ngày", "P2",
         "Đã mở màn",
         "1. Từ ngày 30/09/2026, Đến ngày 01/09/2026, bấm 'Lọc'",
         "",
         "- Không có cảnh báo; bảng 'Chưa có dữ liệu'"),

        ("006", "Lọc theo Nhân viên", "P0",
         "Tháng 09/2026 có LX1 và LX2",
         "1. Ô Nhân viên chọn LX1, bấm 'Lọc'",
         "Nhân viên: LX1",
         "- Chỉ còn 1 dòng lái xe LX1 kèm chi tiết\n- Tổng cộng = dòng LX1"),

        ("007", "Lọc theo Phiếu hoạch toán", "P0",
         "PHT1 có số phiếu dạng TPE_HTCXCH_0xxxx",
         "1. Ô 'Phiếu hoạch toán' nhập 5 số cuối của PHT1, bấm 'Lọc'\n2. Nhập lại bằng chữ thường toàn bộ số "
         "phiếu, bấm 'Lọc'",
         "Phiếu hoạch toán: 5 số cuối của PHT1",
         "- Cả 2 lần chỉ còn LX1 với đúng 1 dòng chi tiết PHT1 (tìm theo chứa chuỗi, không phân biệt hoa thường)\n"
         "- Dòng LX1 và Tổng cộng chỉ còn số của PHT1"),

        ("008", "Lọc theo Tải trọng xe", "P1",
         "LX1 có chuyến bằng xe tải trọng '1 tấn' và chuyến bằng xe '2.5 tấn'",
         "1. Ô 'Tải trọng xe' chọn '1 tấn', bấm 'Lọc'",
         "Tải trọng xe: 1 tấn",
         "- Chỉ còn dòng chi tiết có cột 'Tải trọng tính cước' = '1 tấn'\n- Dòng LX1 cộng lại chỉ theo các dòng "
         "còn lại"),

        ("009", "Lọc theo Dòng xe", "P1",
         "Có chuyến dòng xe 'Xe tải' và dòng xe khác",
         "1. Ô 'Dòng xe' chọn 'Xe tải', bấm 'Lọc'",
         "Dòng xe: Xe tải",
         "- Chỉ còn dòng chi tiết có cột 'Dòng xe tính cước' = 'Xe tải'"),

        ("010", "Lọc theo Tuyến đường", "P1",
         "LX1 có CX1 (tuyến TD1) và CK1 (chuyến xe khác không chọn tuyến)",
         "1. Ô 'Tuyến đường' chọn TD1, bấm 'Lọc'",
         "Tuyến đường: TD1",
         "- Còn dòng CX1, cột Tuyến đường là tên TD1\n- Dòng CK1 không còn (chuyến không chọn tuyến bị loại "
         "khi lọc tuyến)"),

        ("011", "Lọc theo Biển số xe", "P1",
         "LX1 chạy cả XE1 (29D-11111) và xe khác",
         "1. Ô 'Biển số xe' chọn 29D-11111, bấm 'Lọc'",
         "Biển số xe: 29D-11111",
         "- Chỉ còn dòng chi tiết có cột 'Xe chạy thực tế' bắt đầu bằng 29D-11111"),

        ("012", "Kết hợp lọc: lái xe không còn chuyến khớp thì biến mất", "P0",
         "LX2 trong tháng chỉ chạy xe tải trọng '2.5 tấn'",
         "1. Lọc tháng 09/2026, ghi Tổng cộng\n2. Chọn Tải trọng xe '1 tấn', bấm 'Lọc'",
         "",
         "- LX2 không còn trong bảng\n- Tổng cộng giảm đúng bằng phần của các chuyến không phải '1 tấn'\n"
         "- Các điều kiện lọc kết hợp kiểu cùng thỏa"),

        ("013", "Nút làm mới", "P1",
         "Đã lọc ra dữ liệu, đã chọn Công ty, Nhân viên, nhập Phiếu hoạch toán, chọn Tải trọng, Dòng xe, Tuyến, "
         "Biển số",
         "1. Bấm nút làm mới",
         "",
         "- Mọi ô lọc về trống, nút 'Lọc' khóa lại\n"
         "- Ghi nhận hành vi ERP: bảng và dòng Tổng cộng vẫn giữ kết quả cũ, chỉ đổi khi Lọc lại"),
    ]),

    ("IV", "Bảng số liệu", [
        ("001", "Dòng lái xe", "P0",
         "Lọc tháng 09/2026 có LX1",
         "1. Quan sát dòng LX1",
         "",
         "- STT 1, 2...; chữ đậm\n- Cột 'Mã lái xe' là mã nhân viên của LX1 trong hồ sơ nhân sự\n"
         "- Tên LX1 gộp qua 7 cột từ Thời gian tới Tuyến đường\n- Các ô tiền, KM là tổng của LX1"),

        ("002", "Dòng chi tiết", "P0",
         "LX1 có PHT1 và PHT2 đã hạch toán trong tháng",
         "1. Quan sát các dòng dưới LX1",
         "",
         "- STT dạng 1.1, 1.2; cột Mã lái xe để trống\n"
         "- Dòng chi tiết luôn hiện, không cần tích ô nào\n"
         "- Mỗi phiếu hạch toán là đúng 1 dòng"),

        ("003", "Cột thông tin xe của dòng chi tiết", "P1",
         "Dòng PHT1 (chuyến CX1, xe XE1)",
         "1. Đọc các cột Tải trọng tính cước, Dòng xe tính cước, Xe chạy thực tế, Phiếu hoạch toán, Chuyến xe, "
         "Tuyến đường",
         "",
         "- Tải trọng tính cước '1 tấn', Dòng xe tính cước 'Xe tải' (theo chuyến xe)\n"
         "- Xe chạy thực tế dạng 'Biển số - Tải trọng - Dòng xe': '29D-11111 - 1 tấn - Xe tải'\n"
         "- Phiếu hoạch toán là số phiếu PHT1, Chuyến xe là tên chuyến CX1, Tuyến đường là tên TD1"),

        ("004", "5 cột tiền lấy đúng số trên phiếu hạch toán", "P0",
         "Đã ghi lại khối lái xe của PHT1 ở TC_01.005",
         "1. Đọc 5 cột tiền của dòng PHT1",
         "",
         "- Công lái xe 150,000 · Xăng xe 300,000 · Khác 50,000 · Công tác phí 100,000 · Vé cầu đường 40,000\n"
         "- Khớp từng số với khối lái xe của phiếu PHT1"),

        ("005", "Cột Cộng", "P0",
         "Dòng PHT1 như TC trước",
         "1. Đọc cột 'Cộng' ở dòng PHT1, dòng LX1 và dòng Tổng cộng",
         "",
         "- Cộng của PHT1 = 150,000 + 300,000 + 50,000 + 100,000 + 40,000 = 640,000\n"
         "- Dòng LX1 và Tổng cộng cũng cộng đủ 5 khoản\n"
         "- Lỗi ERP đã biết: màn hình hiện 540,000 (không cộng Công tác phí); Excel dòng chi tiết lại hiện 640,000"),

        ("006", "Dòng lái xe bằng tổng các dòng chi tiết", "P0",
         "LX1 có PHT1 và PHT2 trong tháng 09/2026",
         "1. Cộng tay từng cột tiền và KM của 2 dòng chi tiết\n2. So với dòng LX1",
         "",
         "- Công lái xe 230,000 · Xăng xe 420,000 · Khác 50,000 · Công tác phí 100,000 · Vé cầu đường 60,000\n"
         "- KM định mức 140 · KM thực chạy 146 · Chênh lệch 6\n- Dòng LX1 khớp từng cột"),

        ("007", "KM định mức theo tuyến và Đi 2 chiều", "P0",
         "CX1: tuyến TD1 50 km, tích 'Đi 2 chiều'; Km duyệt trên PHT1 là 100",
         "1. Đọc cột 'KM định mức' của dòng PHT1",
         "",
         "- KM định mức = 50 x 2 = 100\n- Đổi Km duyệt trên phiếu không làm đổi KM định mức (không lấy theo Km "
         "duyệt)"),

        ("008", "KM thực chạy, Chênh lệch, % Chênh lệch", "P0",
         "CX1: Km lúc đi 12,000, Km lúc về 12,110",
         "1. Đọc 3 cột cuối của dòng PHT1",
         "",
         "- KM thực chạy 110\n- Chênh lệch (KM) 10\n- % Chênh lệch 10%"),

        ("009", "Chuyến xe khác không chọn tuyến", "P1",
         "CK1: không chọn tuyến, điểm đầu 'Kho Liên Ninh', điểm cuối 'Bắc Ninh', KM 40, một chiều, thực chạy 36",
         "1. Đọc dòng PHT2",
         "",
         "- Tuyến đường 'Kho Liên Ninh - Bắc Ninh'\n- KM định mức 40, KM thực chạy 36\n"
         "- Chênh lệch (KM) -4, % Chênh lệch -10%"),

        ("010", "% Chênh lệch ở dòng lái xe", "P1",
         "LX1 chỉ có PHT1 (10%) và PHT2 (-10%) trong tháng",
         "1. Đọc % Chênh lệch dòng LX1",
         "",
         "- Bằng tổng chênh lệch chia tổng KM định mức: 6 / 140 x 100 = 4.28%\n"
         "- KHÔNG phải cộng 2 phần trăm (0%)\n- Làm tròn xuống 2 chữ số"),

        ("011", "Link Phiếu hoạch toán và Chuyến xe", "P1",
         "Có dòng PHT1 (chở hàng) và PHT2 (chuyến xe khác)",
         "1. Bấm số phiếu ở cột 'Phiếu hoạch toán' của từng dòng\n2. Bấm tên ở cột 'Chuyến xe'",
         "",
         "- PHT1 mở 'Phiếu hạch toán chuyến xe chở hàng', PHT2 mở 'Phiếu hạch toán chuyến xe khác'\n"
         "- Chuyến xe mở đúng màn chi tiết chuyến CX1 / CK1\n- Đều mở ở tab mới"),

        ("012", "Định dạng ô số", "P1",
         "Dòng PHT2 có Khác = 0, Công tác phí = 0",
         "1. Đọc các ô tiền dòng PHT2 và dòng Tổng cộng",
         "",
         "- Số phân cách hàng nghìn bằng dấu phẩy (80,000)\n- Ô bằng 0 ở dòng chi tiết / lái xe hiện '-'\n"
         "- Ô bằng 0 ở dòng Tổng cộng hiện 0"),

        ("013", "Thứ tự sắp xếp", "P1",
         "Tháng có nhiều lái xe; LX1 có cả phiếu chuyến xe khác lập trước và phiếu chở hàng lập sau",
         "1. Đọc thứ tự dòng lái xe\n2. Đọc thứ tự dòng chi tiết dưới LX1",
         "",
         "- Lái xe xếp theo họ tên A-Z\n- Dòng chuyến xe chở hàng đứng trước, dòng chuyến xe khác đứng sau"),

        ("014", "Cột Thời gian của dòng chi tiết", "P2",
         "PHT1 lưu 'Đang tạo' ngày 14/09/2026, sửa và bấm 'Lưu và duyệt' ngày 15/09/2026",
         "1. Lọc tháng 09/2026, đọc cột 'Thời gian' của PHT1",
         "",
         "- Hiện 15/09/2026 (ngày hạch toán)\n"
         "- Ghi nhận hành vi ERP: cột lấy ngày cập nhật cuối của phiếu, trùng ngày hạch toán khi phiếu không bị "
         "sửa sau đó"),

        ("015", "Một người có 2 tài khoản nhân viên", "P2",
         "Lái xe có 2 tài khoản nhân viên cùng họ tên, cả 2 đều có phiếu trong tháng (câu truy vấn số 1 thấy 2 "
         "dòng cùng tên)",
         "1. Lọc tháng đó",
         "",
         "- Ghi nhận hành vi ERP: hiện 2 dòng lái xe trùng tên, mỗi dòng mang mã riêng và chi tiết riêng"),
    ]),

    ("V", "Phân trang & Tổng cộng", [
        ("001", "Mỗi trang 20 lái xe", "P0",
         "Tài khoản TCT, khoảng ngày có trên 20 lái xe",
         "1. Lọc\n2. Đếm dòng lái xe trang 1, chuyển sang trang 2",
         "",
         "- Trang 1 có 20 lái xe\n- Trang 2 STT bắt đầu từ 21, dòng chi tiết dạng 21.1"),

        ("002", "Tổng cộng tính mọi trang", "P0",
         "Như TC trước",
         "1. Ghi Tổng cộng\n2. Cộng tay cột Công lái xe các lái xe của mọi trang",
         "",
         "- Tổng cộng = tổng mọi lái xe mọi trang\n- Chuyển trang Tổng cộng không đổi"),

        ("003", "Chuyển trang giữ bộ lọc", "P1",
         "Đã lọc với Tải trọng xe '1 tấn', có 2 trang",
         "1. Chuyển sang trang 2",
         "",
         "- Trang 2 vẫn chỉ có chuyến '1 tấn'"),

        ("004", "Bấm Lọc về trang 1", "P1",
         "Đang ở trang 2",
         "1. Bấm 'Lọc'",
         "",
         "- Quay về trang 1"),
    ]),

    ("VI", "Xuất Excel", [
        ("001", "Tải file Excel", "P0",
         "Đã lọc tháng 09/2026 ra dữ liệu",
         "1. Bấm 'Xuất excel'\n2. Mở file",
         "",
         "- Mở tab mới và tải ngay file 'bao_cao_chi_tiet_chi_phi_van_chuyen_theo_lai_xe.xlsx'\n"
         "- Đầu file có ảnh tiêu đề công ty, dòng 'BÁO CÁO CHI TIẾT CHI PHÍ VẬN CHUYỂN THEO LÁI XE', dòng 'Từ "
         "ngày: 01/09/2026 đến ngày: 30/09/2026'\n- 19 cột giống màn hình, dòng Tổng cộng ngay dưới tiêu đề"),

        ("002", "Excel có đủ mọi trang và dòng chi tiết", "P0",
         "Kết quả lọc có 25 lái xe (2 trang)",
         "1. Đang ở trang 1, xuất excel",
         "",
         "- File có đủ 25 lái xe, mỗi lái xe kèm các dòng chi tiết STT 1.1, 1.2...\n"
         "- Số tiền từng dòng khớp màn hình"),

        ("003", "Excel áp đúng bộ lọc", "P0",
         "Đã lọc Nhân viên LX1, Tuyến đường TD1",
         "1. Xuất excel\n2. So với màn hình",
         "",
         "- File chỉ có LX1 với các dòng chi tiết tuyến TD1, khớp màn hình"),

        ("004", "Công tác phí ở dòng Tổng cộng của Excel", "P0",
         "Kết quả lọc có PHT1 (Công tác phí 100,000)",
         "1. Xuất excel, đọc ô Công tác phí ở dòng Tổng cộng",
         "",
         "- Bằng ô Công tác phí ở dòng Tổng cộng trên màn hình (từ 100,000 trở lên)\n"
         "- Lỗi ERP đã biết: ô này luôn là 0"),

        ("005", "Cột Cộng trong Excel khớp màn hình", "P1",
         "Như trên",
         "1. Xuất excel, so cột 'Cộng' của dòng PHT1, dòng LX1, dòng Tổng cộng với màn hình",
         "",
         "- Cả 3 dòng bằng nhau giữa Excel và màn hình, đều cộng đủ 5 khoản (PHT1 = 640,000)\n"
         "- Lỗi ERP đã biết: Excel dòng PHT1 và LX1 là 640,000, dòng Tổng cộng và màn hình là 540,000"),

        ("006", "Ô số trong Excel", "P2",
         "File đã xuất",
         "1. Chọn vài ô cột Công lái xe, dùng hàm tính tổng\n2. Đọc ô có giá trị 0",
         "",
         "- Ô tiền là số có phân cách hàng nghìn, tính tổng được\n"
         "- Ghi nhận hành vi ERP: ô bằng 0 hiện số 0, không hiện '-' như màn hình"),

        ("007", "Tiêu đề cột trong Excel", "P2",
         "File đã xuất",
         "1. Đọc tiêu đề cột thứ 6",
         "",
         "- Ghi 'Xe chạy thực tế' giống màn hình\n- Lỗi ERP đã biết: ghi sai chính tả 'Xe chạy thức tế'"),

        ("008", "Đổi bộ lọc mà chưa bấm Lọc lại", "P2",
         "Đã lọc tháng 09/2026 ra dữ liệu",
         "1. Chọn thêm Nhân viên LX2 nhưng KHÔNG bấm 'Lọc'\n2. Bấm 'Xuất excel'",
         "",
         "- Ghi nhận hành vi ERP: file chỉ có LX2 (theo bộ lọc đang nhập), trong khi màn hình vẫn hiện mọi lái xe"),

        ("009", "Nhiều lái xe vẫn tải file ngay", "P2",
         "Tài khoản TCT, khoảng ngày 1 năm, càng nhiều lái xe càng tốt",
         "1. Lọc, bấm 'Xuất excel'",
         "",
         "- Ghi nhận hành vi ERP: file tải về ngay, không hiện thông báo 'Báo cáo chi tiết chi phí vận chuyển "
         "theo lái xe sẽ gửi về mail của bạn trong ít phút!'\n- File đủ mọi lái xe, không lỗi"),

        ("010", "Chân file Excel", "P2",
         "File đã xuất",
         "1. Cuộn xuống cuối file",
         "",
         "- Có dòng 'Ngày ... Tháng ... Năm ...' theo ngày xuất và chữ 'Người lập'"),
    ]),

    ("VII", "Kiểm tra tăng / giảm số liệu trên báo cáo", [
        ("001", "Ghi số nền của LX1", "P0",
         "Tài khoản TCT. Đã chuẩn bị PHT1 và PHT2 ở trạng thái 'Đang tạo' (TC_01.005, TC_01.006)",
         "1. Mở báo cáo, Từ ngày = Đến ngày = hôm nay, Công ty TPE, bấm 'Lọc'\n"
         "2. GHI LẠI dòng LX1 (nếu có): Công lái xe, Xăng xe, Khác, Công tác phí, Vé cầu đường, KM định mức, KM "
         "thực chạy, số dòng chi tiết\n3. GHI LẠI các cột của dòng Tổng cộng",
         "Ngày: hôm nay\nCông ty: TPE",
         "- Có số nền N của LX1 (LX1 chưa có thì coi mọi cột bằng 0, số dòng chi tiết 0)\n"
         "- Có số nền T của dòng Tổng cộng"),

        ("002", "Phiếu Đang tạo không làm tăng số", "P0",
         "PHT1, PHT2 đang ở trạng thái 'Đang tạo'",
         "1. Mở lại báo cáo với đúng bộ lọc TC trước\n2. Ô 'Phiếu hoạch toán' nhập số phiếu PHT1, bấm 'Lọc'",
         "",
         "- Bước 1: dòng LX1 và Tổng cộng vẫn bằng N và T\n- Bước 2: 'Chưa có dữ liệu'"),

        ("003", "Lưu và duyệt PHT1 thêm đúng 1 dòng chi tiết", "P0",
         "Tài khoản KT. PHT1 đang 'Đang tạo'",
         "1. KT mở " + MENU_PHT + ", sửa PHT1, bấm 'Lưu và duyệt' (nếu hỏi vé cầu đường vượt định mức thì bấm "
         "'Xác nhận')\n2. TCT mở lại báo cáo với bộ lọc TC_07.001",
         "PHT1: Công lái xe 150,000 · Xăng 300,000 · Khác 50,000 · Công tác phí 100,000 · Vé cầu đường 40,000",
         "- PHT1 chuyển 'Đã hạch toán', chuyến CX1 chuyển 'Đã hạch toán'\n"
         "- Dưới LX1 có thêm đúng 1 dòng: Phiếu hoạch toán = PHT1, Chuyến xe = CX1, Tuyến đường = TD1, Xe chạy "
         "thực tế '29D-11111 - 1 tấn - Xe tải'\n"
         "- Dòng mới: Công lái xe 150,000, Xăng xe 300,000, Khác 50,000, Công tác phí 100,000, Vé cầu đường "
         "40,000, KM định mức 100, KM thực chạy 110, Chênh lệch 10, % 10%"),

        ("004", "Dòng LX1 và Tổng cộng tăng đúng bằng PHT1", "P0",
         "Vừa làm TC trước",
         "1. So dòng LX1 và dòng Tổng cộng với số nền N, T",
         "",
         "- Công lái xe tăng 150,000; Xăng xe tăng 300,000; Khác tăng 50,000; Công tác phí tăng 100,000; Vé cầu "
         "đường tăng 40,000\n- Cộng tăng 640,000 (đủ 5 khoản)\n"
         "- KM định mức tăng 100, KM thực chạy tăng 110\n- Số dòng chi tiết của LX1 tăng 1\n"
         "- Lỗi ERP đã biết: cột Cộng chỉ tăng 540,000"),

        ("005", "Hạch toán chuyến xe khác PHT2", "P0",
         "PHT2 đang 'Đang tạo'. Đã làm TC trước",
         "1. KT mở 'Phiếu hạch toán chuyến xe khác', sửa PHT2, bấm 'Lưu và duyệt'\n2. Mở lại báo cáo cùng bộ lọc",
         "PHT2: Công lái xe 80,000 · Xăng 120,000 · Khác 0 · Vé cầu đường 20,000 · Công tác phí 0",
         "- Dưới LX1 có thêm dòng PHT2, đứng sau dòng PHT1, Tuyến đường 'Kho Liên Ninh - Bắc Ninh'\n"
         "- Dòng PHT2: Công lái xe 80,000, Xăng xe 120,000, Khác '-', Công tác phí '-', Vé cầu đường 20,000, KM "
         "định mức 40, KM thực chạy 36, Chênh lệch -4\n"
         "- Dòng LX1 so với N: Công lái xe tăng 230,000, Xăng xe tăng 420,000, Vé cầu đường tăng 60,000"),

        ("006", "Ngoài khoảng ngày không hiện", "P0",
         "PHT1, PHT2 hạch toán hôm nay",
         "1. Lọc Từ ngày = Đến ngày = hôm qua, chọn LX1\n2. Lọc Từ ngày = Đến ngày = ngày mai\n"
         "3. Lọc từ hôm qua đến ngày mai",
         "",
         "- Bước 1 và 2: không có dòng PHT1, PHT2\n- Bước 3: có đủ 2 dòng"),

        ("007", "Phiếu của lái xe công ty khác", "P0",
         "Phiếu của LX3 (TPV) vừa 'Lưu và duyệt' hôm nay với Công lái xe 90,000",
         "1. CT (TPE) mở báo cáo, lọc hôm nay\n2. TCT mở báo cáo, lọc hôm nay, Công ty TPE\n"
         "3. TCT đổi Công ty sang TPV",
         "",
         "- Bước 1 và 2: không có LX3, Tổng cộng không tăng 90,000\n- Bước 3: có LX3 với Công lái xe 90,000"),

        ("008", "Chuyến lái xe thuê ngoài không làm tăng", "P1",
         "Ghi Tổng cộng hôm nay của TPE (T2). Phiếu hạch toán của CX9 (XE9, lái xe thuê ngoài) vừa 'Lưu và duyệt'",
         "1. Mở lại báo cáo cùng bộ lọc\n2. Ô 'Phiếu hoạch toán' nhập số phiếu của CX9",
         "",
         "- Bước 1: Tổng cộng vẫn T2\n- Bước 2: 'Chưa có dữ liệu'"),

        ("009", "Chiều ngược: không giảm được số qua giao diện", "P1",
         "PHT1 đã hạch toán; tài khoản KT là người lập",
         "1. KT mở " + MENU_PHT + ", bấm bánh răng của PHT1\n2. Lập phiếu PHT4 cho chuyến khác, chỉ 'Lưu', "
         "bấm bánh răng > 'Xóa'\n3. Mở lại báo cáo",
         "",
         "- Bước 1: PHT1 chỉ còn 'In', 'Xuất excel', không có 'Sửa', 'Xóa'\n"
         "- Bước 2: hiện 'Không được xóa!', PHT4 vẫn còn\n- Bước 3: dòng PHT1 vẫn còn, số không đổi\n"
         "- Ghi nhận hành vi ERP: phiếu đã hạch toán không hủy được nên báo cáo không giảm; cần hỏi nghiệp vụ "
         "cách xử lý phiếu hạch toán sai"),

        ("010", "Lọc theo số phiếu chỉ còn đúng phần của phiếu", "P1",
         "Đã làm TC_07.003",
         "1. Ô 'Phiếu hoạch toán' nhập số phiếu PHT1, bấm 'Lọc'",
         "",
         "- Chỉ còn LX1 với 1 dòng PHT1\n- Dòng LX1 và Tổng cộng: Công lái xe 150,000, Xăng xe 300,000, Khác "
         "50,000, Công tác phí 100,000, Vé cầu đường 40,000"),
    ]),

    ("VIII", "Đối chiếu với báo cáo tổng hợp theo lái xe", [
        ("001", "Dòng lái xe khớp báo cáo tổng hợp", "P0",
         "Tài khoản TCT. Tháng 09/2026 có LX1, LX2",
         "1. Báo cáo chi tiết: lọc 01/09/2026 - 30/09/2026, Công ty TPE, không chọn ô lọc chuyến nào\n"
         "2. Mở " + MENU_TH + ", lọc cùng ngày, cùng Công ty\n3. So dòng LX1 ở 2 báo cáo",
         "",
         "- Công lái xe, Xăng xe, Khác, Công tác phí, Vé cầu đường, Cộng, KM định mức, KM thực chạy, Chênh "
         "lệch, % Chênh lệch của LX1 bằng nhau ở 2 báo cáo\n- Dòng Tổng cộng 2 báo cáo bằng nhau"),

        ("002", "Cộng dòng chi tiết bằng dòng ở báo cáo tổng hợp", "P0",
         "Như TC trước",
         "1. Cộng tay cột Công lái xe và KM thực chạy của mọi dòng chi tiết dưới LX1\n"
         "2. So với dòng LX1 ở báo cáo tổng hợp",
         "",
         "- 2 tổng bằng đúng 2 cột tương ứng ở báo cáo tổng hợp"),

        ("003", "Lọc thêm điều kiện chuyến thì không còn so được", "P2",
         "Như TC trước",
         "1. Ở báo cáo chi tiết chọn thêm Tuyến đường TD1, bấm 'Lọc'",
         "",
         "- Dòng LX1 nhỏ hơn báo cáo tổng hợp (báo cáo tổng hợp không có các ô lọc chuyến)\n"
         "- Chỉ so 2 báo cáo khi bộ lọc chỉ gồm ngày, Công ty, Nhân viên"),
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

# Thong ke nhanh
_all = [t[2] for t in ROLE_TCS] + [t[2] for _, _, tcs in SECTIONS for t in tcs]
print("Tong TC: %d, P0: %d (%.0f%%)" % (len(_all), _all.count("P0"), 100.0 * _all.count("P0") / len(_all)))
