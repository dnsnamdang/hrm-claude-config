# -*- coding: utf-8 -*-
"""Generate testcase Excel cho man ERP: Bao cao chi phi van chuyen theo nhan vien kinh doanh.

Viet cho MAN ERP GOC (TanPhatDev, route report.transportByStaff*), de tester nam luong
truoc khi nghiem thu ban HRM da port (sale-transport-cost-by-staff).

Chay:  python gen_testcase.py
Output: testcase - Bao cao chi phi van chuyen theo NVKD.xlsx (cung thu muc)
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

OUTPUT_FILE = os.path.join(HERE, "testcase - Bao cao chi phi van chuyen theo NVKD.xlsx")
FEATURE_NAME = "Báo cáo chi phí vận chuyển theo nhân viên kinh doanh (ERP)"
MODULE_NAME = "Kinh doanh - Báo cáo vận chuyển"

Q_TCT_MOI = "Xem báo cáo chi phí vận chuyển theo nhân viên kinh doanh - Theo tổng công ty"
Q_CT_MOI = "Xem báo cáo chi phí vận chuyển theo nhân viên kinh doanh - Theo công ty"
Q_PB = "Xem báo cáo chi phí vận chuyển theo nhân viên kinh doanh - Theo phòng ban"
Q_TCT_CU = "Xem báo cáo vận chuyển theo công ty theo tổng công ty"
Q_CT_CU = "Xem báo cáo vận chuyển theo công ty"

# =========================================================================
# 9 MUC MO TA
# =========================================================================
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Báo cáo tổng hợp CƯỚC VẬN CHUYỂN đã hạch toán cho từng nhân viên kinh doanh, gom theo "
     "Phòng ban > Nhân viên > từng chuyến xe. Nguồn số là các dòng hạch toán trên 'Phiếu hạch toán chuyến "
     "xe' (chuyến chở hàng) và 'Phiếu hạch toán chuyến xe khác'. Màn chỉ để xem, không sửa dữ liệu.\n"
     "Có 2 đường vào, cùng mở một màn:\n"
     "- Menu Kinh doanh > Báo cáo bán hàng > nhóm 'Báo cáo Vận chuyển' > 'Báo cáo chi phí vận chuyển "
     "theo nhân viên kinh doanh'.\n"
     "- Menu Kho > Vận chuyển - Bốc xếp > nhóm 'Báo cáo vận chuyển' > cùng tên."),

    ("2. Đối tượng được tính / hiển thị",
     "Một dòng hạch toán được cộng vào báo cáo khi thỏa ĐỦ:\n"
     "- Thuộc phiếu hạch toán chuyến xe hoặc phiếu hạch toán chuyến xe khác.\n"
     "- Có gắn nhân viên (nhân viên kinh doanh chịu cước).\n"
     "- Ngày hạch toán nằm trong khoảng Từ ngày - Đến ngày (lấy trọn cả 2 ngày đầu và cuối).\n"
     "- Có mã công việc và mã đó KHÔNG thuộc 5 loại bị loại ở mục 3.\n"
     "- Nằm trong phạm vi quyền xem của người đăng nhập (mục 7)."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Dòng hạch toán không gắn nhân viên.\n"
     "- Dòng có mã công việc thuộc 5 loại: Công lái xe · Xăng xe · Chi phí khác · Vé cầu đường · "
     "Công tác phí. Đây là chi phí nội bộ của xe, không phải cước tính cho kinh doanh.\n"
     "- Dòng KHÔNG có mã công việc cũng bị loại (hành vi hiện tại của ERP, giữ nguyên).\n"
     "- Khi đã nhập một trong các ô Số chuyến xe / Hợp đồng / Yêu cầu xuất hàng / Đối tượng chịu phí: "
     "chuyến không chở phiếu xuất kho nào bị loại hẳn."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Từ ngày và Đến ngày là BẮT BUỘC (nút 'Lọc' khóa cho tới khi nhập đủ 2 ô).\n"
     "- Cấp Phòng ban và cấp Nhân viên lọc theo NGÀY HẠCH TOÁN của dòng hạch toán.\n"
     "- Cấp chi tiết chuyến lại lọc theo NGÀY CẬP NHẬT CUỐI của phiếu hạch toán, và cột 'Thời gian' cũng "
     "hiện ngày cập nhật cuối này. Phiếu bị sửa sau ngày hạch toán sẽ lệch (xem mục 9).\n"
     "Màn không tự tải khi mở."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Bảng 3 cấp, 11 cột: STT · Mã NVKD · Thời gian · Tải trọng tính cước · Dòng xe tính cước · Xe chạy "
     "thực tế · Tuyến đường · Cước vận chuyển · Yêu cầu xuất hàng · Hợp đồng · Số chuyến xe.\n"
     "- Cấp 1 Phòng ban (STT 1, 2...; chữ đậm): tên phòng + tổng cước. Xếp theo tên phòng A-Z.\n"
     "- Cấp 2 Nhân viên (STT 1.1, 1.2...; chữ xanh): mã nhân viên, họ tên, tổng cước. Xếp theo họ tên A-Z.\n"
     "- Cấp 3 Chuyến (STT 1.1.1...): chỉ hiện khi tích 'Show chi tiết'.\n"
     "Nhân viên được xếp vào phòng ban GHI TRÊN DÒNG HẠCH TOÁN (phòng lúc hạch toán), nên nhân viên đã "
     "chuyển phòng có thể xuất hiện ở 2 phòng.\n"
     "Phân trang: 20 PHÒNG BAN mỗi trang."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Cước 1 chuyến của 1 nhân viên = tổng các dòng hạch toán của nhân viên đó trong phiếu.\n"
     "- Cước nhân viên = tổng cước các chuyến của nhân viên trong phòng đó.\n"
     "- Cước phòng ban = tổng cước nhân viên thuộc phòng.\n"
     "- Dòng 'Tổng cộng' (ngay dưới tiêu đề) = tổng mọi phòng ban của MỌI trang, không chỉ trang đang xem.\n"
     "- Lọc theo Số chuyến / Hợp đồng / Yêu cầu xuất hàng / Đối tượng chịu phí là lọc theo CHUYẾN: chuyến "
     "có ít nhất một dòng khớp thì lấy toàn bộ cước của chuyến đó."),

    ("7. Phân quyền cấp",
     "Mọi tài khoản đăng nhập đều mở được màn. Phạm vi dữ liệu theo quyền (tên hiển thị trong màn "
     "phân quyền):\n"
     "- '" + Q_TCT_MOI + "' hoặc quyền cũ '" + Q_TCT_CU + "': thấy mọi công ty; có ô lọc Công ty, Phòng "
     "ban, Nhân viên.\n"
     "- '" + Q_CT_MOI + "' hoặc quyền cũ '" + Q_CT_CU + "': chỉ công ty mình; có ô Phòng ban, Nhân viên.\n"
     "- '" + Q_PB + "': chỉ phòng ban hiện tại của mình; chỉ có ô Nhân viên.\n"
     "- Không có quyền nào: chỉ cước gắn chính mình; không có ô Công ty, Phòng ban, Nhân viên."),

    ("8. Cách tính các ô thống kê",
     "- Số tiền làm tròn, phân cách hàng nghìn bằng dấu phẩy (vd 1,250,000).\n"
     "- Cước bằng 0 hoặc âm hiển thị dấu '-' ở cấp phòng, nhân viên, chuyến.\n"
     "- Xuất excel: dưới 50 phòng ban thì tải file ngay; từ 50 phòng ban trở lên thì gửi file qua email."),

    ("9. Ghi chú đọc bảng",
     "Các lỗi ERP ĐÃ BIẾT, đã viết thành testcase với kết quả mong đợi ĐÚNG - khi chạy thấy hiện tượng "
     "lỗi như mô tả thì ghi Failed và chép câu 'Lỗi ERP đã biết' vào cột Ghi chú:\n"
     "(1) Chỉ có quyền MỚI theo tổng công ty / theo công ty (không có quyền cũ): cấp Nhân viên và cấp "
     "Chuyến vẫn bị giới hạn như không có quyền đó, nên nhiều phòng hiện tổng cước nhưng không có nhân "
     "viên bên dưới; tổng phòng cũng thiếu cước của chuyến xe khác.\n"
     "(2) Cấp chuyến lọc theo ngày cập nhật cuối của phiếu hạch toán, không theo ngày hạch toán; cột "
     "'Thời gian' cũng hiện ngày cập nhật cuối.\n"
     "(3) Ô Hợp đồng nhập dấu nháy kép làm báo 'Đã có lỗi xảy ra'.\n"
     "(4) Nút làm mới không xóa ô Số chuyến xe, Hợp đồng, Yêu cầu xuất hàng, Đối tượng chịu phí.\n"
     "(5) File Excel cột 'Tuyến đường' hiện TÊN CHUYẾN thay vì tuyến đường như màn hình.\n"
     "(6) Excel mẫu đầy đủ: nhân viên có mặt ở 2 phòng bị lặp toàn bộ chuyến ở cả 2 phòng.\n"
     "(7) Phiếu hạch toán chuyến xe khác chưa hạch toán xong vẫn được cộng vào tổng phòng / nhân viên nhưng "
     "không hiện ở cấp chuyến."),
]

# =========================================================================
# SECTION PHAN QUYEN
# =========================================================================
ROLE_TCS = [
    ("00", "Không có quyền xem nào: chỉ thấy cước của chính mình", "P0",
     "Tài khoản A là nhân viên kinh doanh, không có quyền nào trong 5 quyền xem báo cáo. Trong tháng "
     "09/2026 A có 3 chuyến được hạch toán cước, đồng nghiệp cùng phòng có 5 chuyến",
     "1. Đăng nhập bằng A, mở màn báo cáo\n2. Quan sát bộ lọc\n"
     "3. Từ ngày 01/09/2026, Đến ngày 30/09/2026, bấm 'Lọc', tích 'Show chi tiết'",
     "Tài khoản: A",
     "- Bộ lọc KHÔNG có ô Công ty, Phòng ban, Nhân viên\n"
     "- Bảng chỉ có 1 phòng (phòng của A), dưới đó chỉ có A với 3 chuyến\n"
     "- Không thấy cước của đồng nghiệp"),

    ("01", "Quyền theo phòng ban", "P0",
     "Tài khoản B có quyền '" + Q_PB + "', thuộc phòng Kinh doanh 1, đồng thời được phân quản lý phòng "
     "Kinh doanh 2",
     "1. Đăng nhập B, mở màn\n2. Quan sát bộ lọc, mở ô Nhân viên\n3. Lọc tháng 09/2026",
     "Tài khoản: B",
     "- Chỉ có ô Nhân viên, liệt kê nhân viên phòng Kinh doanh 1\n"
     "- Bảng chỉ có phòng Kinh doanh 1\n"
     "- Ghi nhận: phòng Kinh doanh 2 (phòng B quản lý) KHÔNG hiện; quyền này chỉ lấy phòng hiện tại của B"),

    ("02", "Quyền cũ theo công ty", "P0",
     "Tài khoản C chỉ có quyền cũ '" + Q_CT_CU + "', thuộc công ty 1",
     "1. Đăng nhập C, mở màn\n2. Lọc tháng 09/2026, tích 'Show chi tiết'",
     "Tài khoản: C",
     "- Có ô Phòng ban, Nhân viên (chỉ phòng / nhân viên công ty 1); không có ô Công ty\n"
     "- Đủ mọi phòng của công ty 1, mỗi phòng đủ nhân viên và chuyến\n- Không có phòng của công ty khác"),

    ("03", "Quyền mới theo công ty", "P0",
     "Tài khoản D chỉ có quyền mới '" + Q_CT_MOI + "' (không có quyền cũ), thuộc công ty 1",
     "1. Đăng nhập D, mở màn\n2. Lọc tháng 09/2026, tích 'Show chi tiết'\n"
     "3. So kết quả với tài khoản C ở TC trước cùng khoảng ngày",
     "Tài khoản: D",
     "- Kết quả giống hệt tài khoản C: đủ mọi phòng, mỗi phòng đủ nhân viên và chuyến, tổng cộng bằng nhau\n"
     "- Lỗi ERP đã biết: phòng khác phòng của D chỉ hiện dòng tổng, không có nhân viên bên dưới; tổng "
     "cộng nhỏ hơn của C vì thiếu cước chuyến xe khác"),

    ("04", "Quyền cũ theo tổng công ty", "P0",
     "Tài khoản E chỉ có quyền cũ '" + Q_TCT_CU + "'",
     "1. Đăng nhập E, mở màn\n2. Quan sát bộ lọc\n3. Lọc tháng 09/2026",
     "Tài khoản: E",
     "- Có đủ 3 ô Công ty, Phòng ban, Nhân viên\n- Bảng có phòng ban của mọi công ty, đủ 3 cấp"),

    ("05", "Quyền mới theo tổng công ty", "P0",
     "Tài khoản F chỉ có quyền mới '" + Q_TCT_MOI + "'",
     "1. Đăng nhập F, mở màn\n2. Lọc tháng 09/2026, tích 'Show chi tiết'\n3. So với tài khoản E",
     "Tài khoản: F",
     "- Có ô Công ty; kết quả giống hệt tài khoản E\n"
     "- Lỗi ERP đã biết: phần lớn phòng chỉ hiện dòng tổng, không có nhân viên / chuyến bên dưới; tổng "
     "cộng lệch so với E"),

    ("06", "Màn mở được với mọi tài khoản đăng nhập", "P1",
     "Tài khoản bất kỳ không thuộc khối kinh doanh",
     "1. Đăng nhập, mở màn từ menu",
     "",
     "- Màn mở được, không báo thiếu quyền\n- Dữ liệu chỉ gồm cước gắn chính tài khoản đó (thường trống)"),

    ("07", "Không vượt phạm vi bằng cách sửa đường dẫn xuất excel", "P2",
     "Tài khoản C (quyền công ty, công ty 1). Dành cho tester kỹ thuật",
     "1. Chọn mẫu Xuất excel, sao chép đường dẫn tab tải file\n"
     "2. Thêm vào đường dẫn tham số công ty = mã công ty 4, mở lại",
     "Tài khoản: C",
     "- File không có dữ liệu của công ty 4 (phạm vi quyền vẫn giữ nguyên)"),

    ("08", "Phạm vi quyền áp cả cho Xuất excel", "P1",
     "Tài khoản B (quyền phòng ban)",
     "1. Lọc tháng 09/2026\n2. Xuất excel mẫu đầy đủ",
     "Tài khoản: B",
     "- File chỉ có phòng Kinh doanh 1, khớp màn hình"),
]

# =========================================================================
# CAC SECTION CHUC NANG
# =========================================================================
SECTIONS = [
    ("I", "Giao diện & mở màn", [
        ("001", "Bố cục màn hình khi mở", "P0",
         "Tài khoản có quyền theo tổng công ty",
         "1. Menu Kinh doanh > Báo cáo bán hàng > 'Báo cáo chi phí vận chuyển theo nhân viên kinh doanh'\n"
         "2. Quan sát",
         "",
         "- Tiêu đề trang 'BÁO CÁO CHI PHÍ VẬN CHUYỂN THEO NHÂN VIÊN KINH DOANH'\n"
         "- Khối 'Bộ lọc': Từ ngày* · Đến ngày* · Công ty · Phòng ban · Nhân viên · Số chuyến xe · Hợp đồng "
         "· Yêu cầu xuất hàng · Đối tượng chịu phí\n"
         "- Nút 'Lọc', nút làm mới (mũi tên xoay vòng), nút 'Xuất excel'\n"
         "- Khối 'Chi tiết' có ô tích 'Show chi tiết' ở góc phải"),

        ("002", "Mở từ menu Kho", "P1",
         "Đã đăng nhập",
         "1. Menu Kho > Vận chuyển - Bốc xếp > 'Báo cáo chi phí vận chuyển theo nhân viên kinh doanh'",
         "",
         "- Mở đúng cùng màn như đường vào từ menu Kinh doanh"),

        ("003", "Trạng thái mặc định khi mở", "P0",
         "Đã mở màn",
         "1. Quan sát ô ngày, nút Lọc, bảng",
         "",
         "- Từ ngày, Đến ngày để trống\n- Nút 'Lọc' bị khóa (mờ)\n"
         "- Bảng hiện 'Chưa có dữ liệu', dòng Tổng cộng trống"),

        ("004", "Nút Xuất excel khi chưa có dữ liệu", "P1",
         "Vừa mở màn",
         "1. Bấm 'Xuất excel'",
         "",
         "- Nút mờ, bấm không mở cửa sổ xuất"),

        ("005", "Tiêu đề 11 cột và dòng Tổng cộng", "P0",
         "Đã mở màn",
         "1. Đọc tiêu đề bảng",
         "",
         "- Đúng thứ tự: STT · Mã NVKD · Thời gian · Tải trọng tính cước · Dòng xe tính cước · Xe chạy "
         "thực tế · Tuyến đường · Cước vận chuyển · Yêu cầu xuất hàng · Hợp đồng · Số chuyến xe\n"
         "- Ngay dưới là dòng 'Tổng cộng', ô tổng nằm ở cột Cước vận chuyển"),

        ("006", "Ô ngày", "P1",
         "Đã mở màn",
         "1. Bấm vào ô Từ ngày, chọn ngày trên lịch\n2. Quan sát nhãn hai ô ngày",
         "",
         "- Ngày hiện dạng ngày/tháng/năm (vd 01/09/2026)\n- Nhãn Từ ngày, Đến ngày có dấu * bắt buộc"),

        ("007", "Lựa chọn ô Đối tượng chịu phí", "P2",
         "Đã mở màn",
         "1. Mở ô 'Đối tượng chịu phí'",
         "",
         "- 3 lựa chọn: Tất cả · Nhân viên chịu · Công ty chịu; mặc định 'Tất cả'"),

        ("008", "Trạng thái đang tải", "P2",
         "Đã nhập đủ 2 ngày",
         "1. Bấm 'Lọc', quan sát ngay",
         "",
         "- Dòng Tổng cộng hiện 'Đang tải dữ liệu' có biểu tượng quay\n"
         "- Nút Lọc, làm mới, Xuất excel bị khóa trong lúc tải"),

        ("009", "Thu gọn / mở khối Bộ lọc", "P2",
         "Đã mở màn",
         "1. Bấm mũi tên ở góc phải khối 'Bộ lọc'\n2. Bấm lại",
         "",
         "- Khối Bộ lọc thu gọn rồi mở lại, giá trị đã nhập được giữ nguyên"),
    ]),

    ("II", "Bộ lọc ngày", [
        ("001", "Chỉ nhập một ô ngày", "P0",
         "Đã mở màn",
         "1. Nhập Từ ngày 01/09/2026, để trống Đến ngày\n2. Thử bấm 'Lọc'",
         "",
         "- Nút 'Lọc' vẫn khóa, không bấm được"),

        ("002", "Lọc theo khoảng ngày hạch toán", "P0",
         "Phiếu hạch toán chuyến xe PHT1 hạch toán ngày 15/09/2026, PHT2 ngày 02/10/2026, cùng nhân viên A",
         "1. Từ ngày 01/09/2026, Đến ngày 30/09/2026\n2. Bấm 'Lọc', tích 'Show chi tiết'",
         "",
         "- Chỉ cước của PHT1 được tính cho A\n- PHT2 không xuất hiện"),

        ("003", "Lấy trọn ngày cuối", "P1",
         "Phiếu PHT3 hạch toán lúc 17:30 ngày 30/09/2026",
         "1. Từ ngày 30/09/2026, Đến ngày 30/09/2026\n2. Bấm 'Lọc'",
         "",
         "- PHT3 được tính (lấy đến hết ngày 30/09)"),

        ("004", "Từ ngày lớn hơn Đến ngày", "P2",
         "Đã mở màn",
         "1. Từ ngày 30/09/2026, Đến ngày 01/09/2026\n2. Bấm 'Lọc'",
         "",
         "- Ghi nhận hiện tượng: không có cảnh báo; bảng 'Chưa có dữ liệu', Tổng cộng trống"),

        ("005", "Phiếu hạch toán bị sửa sau ngày hạch toán", "P1",
         "Phiếu PHT4 của nhân viên A hạch toán ngày 30/09/2026, sau đó được sửa (cập nhật) ngày 02/10/2026",
         "1. Lọc 01/09/2026 - 30/09/2026, tích 'Show chi tiết'\n2. Tìm A và chuyến PHT4",
         "",
         "- A có cước của PHT4 và dòng chuyến PHT4 hiện bên dưới; cước nhân viên = tổng các chuyến\n"
         "- Lỗi ERP đã biết: A có cước nhưng không có dòng chuyến PHT4 (cấp chuyến lọc theo ngày cập nhật cuối)"),

        ("006", "Cột Thời gian ở cấp chuyến", "P2",
         "Phiếu PHT4 như TC trước",
         "1. Đọc cột 'Thời gian' của chuyến PHT4 (lọc tháng 10 nếu cần)",
         "",
         "- Hiện ngày hạch toán 30/09/2026\n- Lỗi ERP đã biết: hiện ngày cập nhật cuối 02/10/2026"),
    ]),

    ("III", "Bộ lọc Công ty / Phòng ban / Nhân viên", [
        ("001", "Chọn Công ty", "P0",
         "Tài khoản quyền theo tổng công ty (quyền cũ)",
         "1. Ô Công ty chọn công ty 1\n2. Mở ô Phòng ban, mở ô Nhân viên\n3. Lọc tháng 09/2026",
         "",
         "- Ô Phòng ban, Nhân viên chỉ còn phòng / nhân viên của công ty 1\n- Bảng chỉ có phòng của công ty 1"),

        ("002", "Đổi Công ty xóa Phòng ban và Nhân viên đã chọn", "P1",
         "Đã chọn công ty 1, phòng P1, nhân viên A",
         "1. Đổi Công ty sang công ty 4",
         "",
         "- Ô Phòng ban và Nhân viên về trống"),

        ("003", "Chọn Phòng ban", "P0",
         "Tài khoản quyền theo công ty",
         "1. Ô Phòng ban chọn P1\n2. Mở ô Nhân viên\n3. Lọc tháng 09/2026",
         "",
         "- Ô Nhân viên chỉ còn nhân viên của P1\n- Bảng chỉ có phòng P1"),

        ("004", "Đổi Phòng ban xóa Nhân viên đã chọn", "P2",
         "Đã chọn P1 và nhân viên A",
         "1. Đổi Phòng ban sang P2",
         "",
         "- Ô Nhân viên về trống"),

        ("005", "Chọn Nhân viên", "P0",
         "Nhân viên A có cước trong tháng",
         "1. Ô Nhân viên chọn A\n2. Lọc tháng 09/2026, tích 'Show chi tiết'",
         "",
         "- Chỉ còn A dưới phòng của A\n- Tổng phòng = tổng cước của A = Tổng cộng"),

        ("006", "Nhân viên đã chuyển phòng", "P1",
         "Nhân viên A thuộc P1 đến 15/09/2026, từ 16/09 chuyển sang P2; cả 2 giai đoạn đều có cước",
         "1. Lọc 01/09/2026 - 30/09/2026, chọn nhân viên A",
         "",
         "- A xuất hiện ở cả P1 (cước trước 16/09) và P2 (cước từ 16/09)\n- Tổng 2 dòng bằng tổng cước của A"),

        ("007", "Danh sách Nhân viên theo phòng hiện tại", "P2",
         "Nhân viên A như TC trước (hiện đang ở P2)",
         "1. Ô Phòng ban chọn P1\n2. Mở ô Nhân viên, tìm A",
         "",
         "- Ghi nhận hiện tượng: không tìm thấy A trong danh sách của P1 (danh sách theo phòng hiện tại), "
         "dù báo cáo vẫn xếp một phần cước của A vào P1"),

        ("008", "Phòng ban và Nhân viên không khớp", "P2",
         "Tài khoản quyền theo tổng công ty",
         "1. Chọn nhân viên A (thuộc P1)\n2. Đổi về chọn phòng P2 rồi chọn lại A bằng cách gõ tìm\n3. Lọc",
         "",
         "- Không chọn được A khi đang chọn P2; nếu chỉ còn P2 thì bảng chỉ có cước của P2"),
    ]),

    ("IV", "Bộ lọc Số chuyến / Hợp đồng / Yêu cầu xuất hàng / Đối tượng chịu phí", [
        ("001", "Lọc theo Số chuyến xe", "P0",
         "Phiếu hạch toán chuyến xe mã HTCX-0915 của nhân viên A trong tháng 09/2026",
         "1. Lọc tháng 09/2026, ô 'Số chuyến xe' nhập '0915'\n2. Bấm 'Lọc', tích 'Show chi tiết'",
         "Số chuyến xe: 0915",
         "- Chỉ còn chuyến có mã chứa '0915'\n"
         "- Tổng nhân viên, tổng phòng, Tổng cộng tính lại chỉ theo chuyến khớp"),

        ("002", "Lọc theo Yêu cầu xuất hàng", "P0",
         "Chuyến C1 chở hàng của yêu cầu xuất hàng YCXH-0101",
         "1. Lọc tháng, ô 'Yêu cầu xuất hàng' nhập 'YCXH-0101'\n2. Bấm 'Lọc', tích 'Show chi tiết'",
         "YCXH-0101",
         "- Chỉ còn các chuyến chở hàng của YCXH-0101\n- Cột 'Yêu cầu xuất hàng' của chuyến có YCXH-0101"),

        ("003", "Lọc theo Hợp đồng", "P1",
         "Yêu cầu xuất hàng của chuyến C1 thuộc hợp đồng HD-123, dòng hạch toán của C1 cũng ghi HD-123",
         "1. Lọc tháng, ô 'Hợp đồng' nhập 'HD-123'\n2. Bấm 'Lọc', tích 'Show chi tiết'",
         "HD-123",
         "- Hiện chuyến C1, cột Hợp đồng có HD-123\n"
         "- Chỉ lấy dòng hạch toán ghi hợp đồng khớp VÀ chuyến có yêu cầu xuất hàng thuộc hợp đồng khớp"),

        ("004", "Ô Hợp đồng nhập dấu nháy kép", "P1",
         "Đã nhập ngày",
         "1. Ô 'Hợp đồng' nhập: HD\"1\n2. Bấm 'Lọc'",
         "HD\"1",
         "- Không lỗi, bảng 'Chưa có dữ liệu'\n- Lỗi ERP đã biết: báo 'Đã có lỗi xảy ra'"),

        ("005", "Đối tượng chịu phí = Nhân viên chịu", "P1",
         "Chuyến C2 có dòng hàng nhân viên chịu phí; chuyến C3 toàn bộ công ty chịu",
         "1. Lọc tháng, 'Đối tượng chịu phí' chọn 'Nhân viên chịu'\n2. Tích 'Show chi tiết'",
         "",
         "- Có C2, không có C3"),

        ("006", "Đối tượng chịu phí = Công ty chịu", "P1",
         "Như TC trước",
         "1. Chọn 'Công ty chịu', bấm 'Lọc'",
         "",
         "- Có C3, không có C2 (trừ khi C2 có thêm dòng công ty chịu)"),

        ("007", "Lọc theo chuyến lấy toàn bộ cước của chuyến", "P2",
         "Chuyến C4 chở 2 yêu cầu xuất hàng YCXH-A và YCXH-B, cước của nhân viên trong chuyến là 2,000,000",
         "1. Lọc với 'Yêu cầu xuất hàng' = YCXH-A",
         "",
         "- Chuyến C4 hiện với cước 2,000,000 (không chia theo yêu cầu xuất hàng)"),

        ("008", "Chuyến xe khác không chở hàng khi lọc Số chuyến", "P1",
         "Phiếu hạch toán chuyến xe khác HTK-0920 (không gắn phiếu xuất kho nào) của nhân viên A",
         "1. Lọc tháng, ô 'Số chuyến xe' nhập đúng 'HTK-0920'",
         "",
         "- Hiện chuyến HTK-0920 của A\n"
         "- Lỗi ERP đã biết: 'Chưa có dữ liệu', vì khi nhập ô này chuyến không chở hàng bị loại"),

        ("009", "Không phân biệt hoa thường", "P2",
         "Mã chuyến HTCX-0915",
         "1. Ô 'Số chuyến xe' nhập 'htcx-0915'",
         "",
         "- Vẫn tìm thấy chuyến HTCX-0915"),

        ("010", "Kết hợp nhiều ô", "P1",
         "Chuyến C1 thỏa đồng thời số chuyến, yêu cầu xuất hàng và nhân viên A",
         "1. Nhập ngày, chọn nhân viên A, nhập Số chuyến và Yêu cầu xuất hàng của C1\n2. Bấm 'Lọc'",
         "",
         "- Chỉ còn C1 (các điều kiện kết hợp theo kiểu cùng thỏa)"),
    ]),

    ("V", "Bảng 3 cấp & số liệu", [
        ("001", "Cấp Phòng ban", "P0",
         "Lọc tháng có nhiều phòng",
         "1. Bấm 'Lọc'\n2. Quan sát các dòng cấp 1",
         "",
         "- STT 1, 2, 3..., tên phòng chữ đậm, tổng cước ở cột Cước vận chuyển\n- Phòng xếp theo tên A-Z"),

        ("002", "Cấp Nhân viên", "P0",
         "Như trên",
         "1. Quan sát dòng dưới mỗi phòng",
         "",
         "- STT dạng 1.1, 1.2; chữ màu xanh\n- Cột Mã NVKD là mã nhân viên, họ tên ở các cột kế bên\n"
         "- Nhân viên trong phòng xếp theo họ tên A-Z"),

        ("003", "Tích / bỏ tích Show chi tiết", "P0",
         "Đã lọc ra dữ liệu",
         "1. Tích 'Show chi tiết'\n2. Bỏ tích",
         "",
         "- Bước 1: dưới mỗi nhân viên hiện các dòng chuyến STT 1.1.1, 1.1.2...\n"
         "- Bước 2: dòng chuyến ẩn đi\n- Không tải lại dữ liệu khi tích / bỏ tích"),

        ("004", "Các cột của dòng chuyến", "P1",
         "Đã tích Show chi tiết",
         "1. Đọc một dòng chuyến chở hàng và một dòng chuyến xe khác",
         "",
         "- Tải trọng tính cước, Dòng xe tính cước lấy theo chuyến xe\n"
         "- Xe chạy thực tế dạng 'Biển số - Tải trọng - Dòng xe'\n"
         "- Tuyến đường: tên tuyến; chuyến xe khác không chọn tuyến thì hiện 'Điểm đầu - Điểm cuối'\n"
         "- Cước vận chuyển là cước của nhân viên trong chuyến"),

        ("005", "Link Yêu cầu xuất hàng", "P1",
         "Dòng chuyến có 2 yêu cầu xuất hàng",
         "1. Quan sát cột 'Yêu cầu xuất hàng'\n2. Bấm một mã",
         "",
         "- 2 mã cách nhau dấu phẩy, mỗi mã một dòng; mỗi mã chỉ hiện một lần\n"
         "- Bấm mở phiếu yêu cầu xuất hàng ở tab mới"),

        ("006", "Link Hợp đồng", "P1",
         "Dòng chuyến chở hàng của hợp đồng hãng và hợp đồng dịch vụ sửa chữa",
         "1. Bấm mã hợp đồng ở cột 'Hợp đồng'",
         "",
         "- Mở đúng màn chi tiết hợp đồng tương ứng ở tab mới"),

        ("007", "Link Số chuyến xe", "P1",
         "Có cả chuyến chở hàng và chuyến xe khác",
         "1. Bấm mã ở cột 'Số chuyến xe' của từng loại",
         "",
         "- Chuyến chở hàng mở 'Phiếu hạch toán chuyến xe', chuyến khác mở 'Phiếu hạch toán chuyến xe khác', "
         "đều ở tab mới, đúng phiếu"),

        ("008", "Cộng dồn 3 cấp", "P0",
         "Phòng P1 có nhân viên A (2 chuyến: 1,500,000 và 500,000) và B (1 chuyến 800,000)",
         "1. Lọc khoảng ngày chứa 3 chuyến, tích 'Show chi tiết'",
         "",
         "- A = 2,000,000; B = 800,000\n- P1 = 2,800,000"),

        ("009", "Tổng cộng tính mọi trang", "P0",
         "Có trên 20 phòng ban trong khoảng ngày",
         "1. Lọc, ghi lại Tổng cộng\n2. Cộng tay cước các phòng của trang 1 và trang 2",
         "",
         "- Tổng cộng = tổng mọi phòng ở mọi trang (lớn hơn tổng trang 1)\n- Chuyển trang Tổng cộng không đổi"),

        ("010", "Định dạng số tiền", "P1",
         "Có cước lẻ (vd 1250000.6) và một nhân viên tổng cước bằng 0 do bút toán điều chỉnh",
         "1. Lọc, đọc các ô tiền",
         "",
         "- Số làm tròn, phân cách hàng nghìn bằng dấu phẩy: 1,250,001\n- Cước bằng 0 hiện dấu '-'"),

        ("011", "Loại 5 mã công việc chi phí nội bộ", "P0",
         "Phiếu hạch toán của nhân viên A có 1 dòng cước vận chuyển 1,000,000 và các dòng Công lái xe "
         "300,000, Xăng xe 200,000, Vé cầu đường 50,000, Công tác phí 100,000, Chi phí khác 70,000, đều gắn A",
         "1. Lọc khoảng ngày của phiếu, tích 'Show chi tiết'",
         "",
         "- Chuyến của A chỉ tính 1,000,000\n- 5 dòng chi phí nội bộ không được cộng"),

        ("012", "Dòng không có mã công việc", "P1",
         "Phiếu hạch toán có dòng cước 450,000 gắn nhân viên A nhưng không chọn mã công việc",
         "1. Lọc khoảng ngày của phiếu",
         "",
         "- Ghi nhận: dòng này KHÔNG được tính (hành vi hiện tại của ERP)"),

        ("013", "Dòng không gắn nhân viên", "P1",
         "Phiếu hạch toán có dòng cước không gắn nhân viên",
         "1. Lọc khoảng ngày của phiếu",
         "",
         "- Dòng đó không được tính vào phòng / nhân viên nào"),

        ("014", "Phiếu hạch toán chuyến xe khác chưa hạch toán", "P2",
         "Phiếu hạch toán chuyến xe khác của nhân viên A đang ở trạng thái chưa hạch toán, có dòng cước "
         "600,000 gắn A",
         "1. Lọc khoảng ngày của phiếu, tích 'Show chi tiết'",
         "",
         "- Cước 600,000 hoặc không tính ở cả 3 cấp, hoặc tính ở cả 3 cấp; tổng nhân viên = tổng chuyến\n"
         "- Lỗi ERP đã biết: tổng của A có 600,000 nhưng không có dòng chuyến tương ứng"),
    ]),

    ("VI", "Phân trang & tốc độ", [
        ("001", "Mỗi trang 20 phòng ban", "P0",
         "Khoảng ngày có trên 20 phòng (tài khoản quyền tổng công ty)",
         "1. Lọc\n2. Đếm số phòng trang 1, chuyển sang trang 2",
         "",
         "- Trang 1 có 20 phòng\n- Trang 2 STT bắt đầu từ 21"),

        ("002", "Chuyển trang giữ bộ lọc", "P0",
         "Đã lọc với Đối tượng chịu phí = Công ty chịu",
         "1. Chuyển sang trang 2",
         "",
         "- Trang 2 vẫn áp bộ lọc\n- Trạng thái 'Show chi tiết' giữ nguyên"),

        ("003", "Bấm Lọc về trang 1", "P1",
         "Đang ở trang 2",
         "1. Bấm 'Lọc'",
         "",
         "- Quay về trang 1"),

        ("004", "Tốc độ tải", "P2",
         "Tài khoản quyền tổng công ty, khoảng ngày 1 năm",
         "1. Bấm 'Lọc', bấm giờ",
         "",
         "- Bảng hiện xong trong khoảng 10 giây, không báo lỗi"),
    ]),

    ("VII", "Nút làm mới", [
        ("001", "Làm mới xóa ngày và Công ty / Phòng ban / Nhân viên", "P1",
         "Đã nhập đủ ngày, chọn Công ty, Phòng ban, Nhân viên",
         "1. Bấm nút làm mới",
         "",
         "- Từ ngày, Đến ngày, Công ty, Phòng ban, Nhân viên về trống\n- Nút 'Lọc' khóa lại"),

        ("002", "Làm mới xóa cả các ô chữ và Đối tượng chịu phí", "P2",
         "Đã nhập Số chuyến xe, Hợp đồng, Yêu cầu xuất hàng, chọn Đối tượng chịu phí = Công ty chịu",
         "1. Bấm nút làm mới",
         "",
         "- Cả 4 ô về trống / 'Tất cả'\n"
         "- Lỗi ERP đã biết: 4 ô này giữ nguyên giá trị cũ; bảng vẫn giữ kết quả cũ"),
    ]),

    ("VIII", "Xuất Excel", [
        ("001", "Mở cửa sổ Xuất Excel", "P0",
         "Đã lọc ra dữ liệu",
         "1. Bấm 'Xuất excel'",
         "",
         "- Hiện cửa sổ 'Xuất Excel' có ô 'Mẫu excel' (Xuất excel đầy đủ · Xuất excel ngắn gọn) và nút "
         "'Xuất EXCEL'"),

        ("002", "Không chọn mẫu", "P1",
         "Cửa sổ Xuất Excel đang mở",
         "1. Để trống Mẫu excel, bấm 'Xuất EXCEL'",
         "",
         "- Cảnh báo 'Vui lòng chọn mẫu xuất excel.'\n- Không tải file"),

        ("003", "Mẫu đầy đủ", "P0",
         "Kết quả lọc dưới 50 phòng ban",
         "1. Chọn 'Xuất excel đầy đủ', bấm 'Xuất EXCEL'\n2. Mở file",
         "",
         "- Mở tab mới, tải file 'bao_cao_chi_phi_van_chuyen_theo_nhan_vien_kinh_doanh.xlsx'\n"
         "- Tiêu đề 'BÁO CÁO CHI PHÍ VẬN CHUYỂN THEO NHÂN VIÊN KINH DOANH', dòng 'Từ ngày: ... đến ngày: ...'\n"
         "- 11 cột như màn hình, dòng Tổng cộng, đủ 3 cấp Phòng ban > Nhân viên > Chuyến"),

        ("004", "Mẫu ngắn gọn", "P0",
         "Như trên",
         "1. Chọn 'Xuất excel ngắn gọn', xuất",
         "",
         "- File chỉ có cấp Phòng ban và Nhân viên, không có dòng chuyến\n- Tổng cộng bằng mẫu đầy đủ"),

        ("005", "Từ 50 phòng ban trở lên gửi qua email", "P1",
         "Tài khoản quyền tổng công ty, khoảng ngày có từ 50 phòng trở lên",
         "1. Xuất excel mẫu đầy đủ\n2. Kiểm tra hộp thư của tài khoản",
         "",
         "- Thông báo 'Báo cáo chi phí vận chuyển theo nhân viên kinh doanh sẽ gửi về mail của bạn trong ít "
         "phút!'\n- Vài phút sau nhận được email kèm file"),

        ("006", "Excel áp đúng bộ lọc", "P0",
         "Đã lọc với nhân viên A, Đối tượng chịu phí = Công ty chịu",
         "1. Xuất excel mẫu đầy đủ\n2. So với màn hình",
         "",
         "- File chỉ có cước của A, đúng các chuyến như màn hình\n- Tổng cộng khớp màn hình"),

        ("007", "Excel gồm mọi trang", "P1",
         "Có 25 phòng (2 trang)",
         "1. Đang ở trang 1, xuất excel",
         "",
         "- File có đủ 25 phòng"),

        ("008", "Cột Tuyến đường trong Excel", "P1",
         "Chuyến C1 có tuyến 'Hà Nội - Hải Phòng'",
         "1. Xuất excel mẫu đầy đủ\n2. So cột 'Tuyến đường' của C1 với màn hình",
         "",
         "- Excel hiện 'Hà Nội - Hải Phòng' giống màn hình\n"
         "- Lỗi ERP đã biết: Excel hiện tên chuyến xe thay vì tuyến đường"),

        ("009", "Nhân viên có mặt ở 2 phòng", "P2",
         "Nhân viên A chuyển phòng giữa kỳ như TC III.006",
         "1. Xuất excel mẫu đầy đủ\n2. Đếm các dòng chuyến của A ở mỗi phòng",
         "",
         "- Mỗi phòng chỉ có các chuyến thuộc giai đoạn A ở phòng đó\n"
         "- Lỗi ERP đã biết: toàn bộ chuyến của A lặp lại ở cả 2 phòng"),

        ("010", "Ô tiền trong Excel là số", "P2",
         "File mẫu đầy đủ",
         "1. Chọn vài ô cột Cước vận chuyển, dùng hàm tính tổng",
         "",
         "- Ô tiền là số có phân cách hàng nghìn, tính tổng được"),

        ("011", "Mã yêu cầu xuất hàng / hợp đồng trong Excel", "P2",
         "Chuyến có 2 yêu cầu xuất hàng",
         "1. Xuất mẫu đầy đủ, đọc cột Yêu cầu xuất hàng và Hợp đồng",
         "",
         "- Các mã cách nhau dấu phẩy, dạng chữ thường (không phải link)"),
    ]),

    ("IX", "Luồng nghiệp vụ đầu - cuối", [
        ("001", "Luồng chuẩn: chuyến chở hàng đến báo cáo", "P0",
         "Nhân viên A (phòng P1) có yêu cầu xuất hàng YCXH-1 đã xuất kho",
         "1. Lập chuyến xe chở hàng cho phiếu xuất của YCXH-1\n"
         "2. Lập và hạch toán 'Phiếu hạch toán chuyến xe' ngày hôm nay: dòng cước vận chuyển 1,200,000 gắn A\n"
         "3. Mở báo cáo, lọc hôm nay, tích 'Show chi tiết'",
         "",
         "- Có P1 > A > 1 chuyến cước 1,200,000\n- Cột Yêu cầu xuất hàng có YCXH-1, Số chuyến xe là mã "
         "phiếu hạch toán vừa lập\n- Tổng cộng tăng đúng 1,200,000"),

        ("002", "Dòng chi phí nội bộ không làm tăng báo cáo", "P0",
         "Tiếp TC trước",
         "1. Sửa phiếu hạch toán, thêm dòng Xăng xe 300,000 gắn A, hạch toán lại\n2. Lọc lại báo cáo",
         "",
         "- Cước của A vẫn 1,200,000"),

        ("003", "Chuyến xe khác đến báo cáo", "P1",
         "Nhân viên B (phòng P2)",
         "1. Lập 'Phiếu hạch toán chuyến xe khác' không chọn tuyến (điểm đầu Kho Hà Nội, điểm cuối Bắc Ninh), "
         "dòng cước 500,000 gắn B, hạch toán\n2. Lọc báo cáo hôm nay, tích 'Show chi tiết'",
         "",
         "- Có P2 > B > chuyến 500,000, Tuyến đường 'Kho Hà Nội - Bắc Ninh'\n"
         "- Bấm Số chuyến xe mở đúng phiếu hạch toán chuyến xe khác"),

        ("004", "Đối chiếu tổng cước một nhân viên với phiếu gốc", "P1",
         "Chọn một nhân viên có nhiều chuyến trong tháng",
         "1. Lọc tháng, chọn nhân viên đó\n"
         "2. Mở từng phiếu hạch toán (từ link Số chuyến xe), cộng tay các dòng cước gắn nhân viên, trừ 5 mã "
         "chi phí nội bộ",
         "",
         "- Tổng cộng tay bằng cước nhân viên trên báo cáo"),
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
