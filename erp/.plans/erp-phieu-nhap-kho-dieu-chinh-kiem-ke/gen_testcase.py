# -*- coding: utf-8 -*-
"""Generate testcase Excel cho man ERP: Phieu nhap kho dieu chinh kiem ke (kho vat ly).

Viet cho MAN ERP GOC (TanPhatDev, route warehouseInventoryImport.*), de tester nam luong ERP
truoc khi nghiem thu ban HRM.

Chay:  PYTHONIOENCODING=utf-8 python gen_testcase.py
Output: testcase - Phieu nhap kho dieu chinh kiem ke.xlsx (cung thu muc)
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

OUTPUT_FILE = os.path.join(HERE, "testcase - Phieu nhap kho dieu chinh kiem ke.xlsx")
FEATURE_NAME = "Phiếu nhập kho điều chỉnh kiểm kê (ERP)"
MODULE_NAME = "Kho - Nhập kho"

MENU = "menu Kho > Nhập kho > 'Phiếu nhập kho điều chỉnh kiểm kê'"
MENU_CHO_DUYET = ("menu Chờ duyệt > Hàng hóa - dịch vụ - vận chuyển > Nhập hàng > "
                  "'Phiếu nhập kho điều chỉnh kiểm kê chờ duyệt'")
MENU_KIEM_KE = "menu Kho > Kiểm kho > 'Kiểm kê theo hàng hóa'"
MENU_KT_NHAP = ("menu Kế toán > Hàng hoá - Dịch vụ - Vận chuyển > Nhập hàng > "
                "'Phiếu nhập hàng điều chỉnh kiểm kê'")
BC_THE_KHO = "menu Kho > Báo cáo kho > 'Thẻ kho'"
BC_XNT = "menu Kho > Báo cáo kho > 'Tổng hợp xuất nhập tồn'"
BC_TON_KHO = "menu Kho > Báo cáo kho > 'Báo cáo tồn theo kho'"
BC_XNT_KT = ("menu Kế toán > Hàng hoá - Dịch vụ - Vận chuyển > Báo cáo hàng tồn kho > "
             "'Tổng hợp xuất nhập tồn'")

# =========================================================================
# 9 MUC MO TA
# =========================================================================
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Thủ kho lập phiếu NHẬP KHO bổ sung cho phần hàng THỪA phát hiện khi kiểm kê theo hàng hóa, để tồn kho "
     "vật lý khớp với số thực kiểm.\n"
     "Đường vào: " + MENU + ". Kế toán kho xem danh sách chờ ở " + MENU_CHO_DUYET + ".\n"
     "Phiếu chỉ lập được từ một phiếu kiểm kê theo hàng hóa đang 'Chờ xử lý' hoặc 'Đang xử lý': mở phiếu "
     "kiểm kê, bấm nút 'Tạo phiếu nhập kho điều chuyển'.\n"
     "RANH GIỚI MÀN: màn này gồm lập phiếu, Lưu nháp, Gửi duyệt, Sửa phiếu nháp, Xem, In, In danh sách, "
     "Xuất Excel. Bấm 'Gửi duyệt' là CỘNG NGAY tồn kho vật lý (sinh lô mới). Bước sau thuộc màn khác: kế "
     "toán kho bấm 'Tạo phiếu nhập hàng' trên dòng phiếu chờ duyệt để lập 'Phiếu nhập hàng điều chỉnh kiểm "
     "kê' (" + MENU_KT_NHAP + "), bước đó mới cộng tồn kho KẾ TOÁN và chuyển phiếu sang 'Đang hạch toán' / "
     "'Đã hạch toán'. Bộ TC này chỉ kiểm bước kế toán ở mức trạng thái và số liệu để thấy ranh giới."),

    ("2. Đối tượng được tính / hiển thị",
     "Bảng Chi tiết của phiếu tự lấy từ phiếu kiểm kê: mỗi dòng là một dòng kết quả kiểm có Chênh lệch "
     "DƯƠNG (thừa) chưa xử lý, thuộc kho đang chọn. Số lượng = phần thừa còn chưa xử lý, đơn vị tính là "
     "'ĐVT kiểm kê' của dòng đó.\n"
     "Chỉ lấy hàng có TỔNG chênh lệch của mọi vị trí khác 0.\n"
     "Trạng thái phiếu: Đang tạo (bấm Lưu), Chờ duyệt (bấm Gửi duyệt), Đang hạch toán (kế toán đã lưu "
     "phiếu nhập hàng nháp), Đã hạch toán (kế toán đã 'Lưu và duyệt').\n"
     "Số phiếu dạng 'PNKĐCKK-' và 5 chữ số."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Hàng thừa ở vị trí này nhưng thiếu đúng bằng ở vị trí khác (tổng chênh lệch bằng 0) không vào phiếu "
     "nhập, vì thuộc phiếu điều chuyển vị trí.\n"
     "- Dòng thiếu (chênh lệch âm) không vào phiếu nhập, thuộc phiếu xuất kho điều chỉnh kiểm kê.\n"
     "- Hàng khai thêm ngoài danh sách ở phiếu kiểm kê không vào phiếu nhập.\n"
     "- Phiếu 'Đang tạo' chỉ người lập thấy, kể cả người có quyền xem theo tổng công ty cũng không thấy.\n"
     "- Mỗi phiếu kiểm kê chỉ lập được MỘT phiếu nhập kho điều chỉnh, lập xong nút tạo biến mất."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Danh sách có ô 'Từ ngày', 'Đến ngày' nhưng hiện không lọc được (xem lỗi ở mục 9).\n"
     "Cột 'Ngày kiểm kê' trên danh sách thực chất là ngày LẬP phiếu nhập, không phải ngày kiểm kê.\n"
     "Trên báo cáo kho, số nhập của phiếu được ghi vào NGÀY BẤM GỬI DUYỆT, không theo ngày kiểm kê."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Danh sách 7 cột: STT, Số phiếu, Ngày kiểm kê, Kho, Trạng thái, Người lập, Hành động (nút bánh răng "
     "gồm Sửa, Tạo phiếu nhập hàng, In tùy điều kiện).\n"
     "Phía trên bảng: Bộ lọc, Tạo mới, In, Xuất excel. Bộ lọc: Mã phiếu, Kho, Trạng thái, Người tạo, Nhập mã "
     "hàng hóa, Nhập tên hàng hóa, Từ ngày, Đến ngày, thêm Công ty / Phòng ban theo quyền.\n"
     "Trang lập phiếu: khung 'Thông tin chung' gồm Phiếu kiểm kho (link), Kho, Ghi chú, File đính kèm (PDF); "
     "khung 'Chi tiết' gồm STT, Tên hàng hóa, Model, Mã hàng hóa, ĐVT, Vị trí, Số lượng (chỉ xem, không sửa); "
     "nút Lưu, Gửi duyệt, Hủy.\n"
     "Bản in phiếu: Số phiếu, Ngày lập, Phiếu kiểm kê, Kho, Ghi chú và bảng STT, Tên hàng, Model, Mã hàng, "
     "ĐVT, Vị trí, SL nhập."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Gửi duyệt: mỗi dòng chi tiết sinh MỘT lô mới, số lô bắt đầu bằng 'NHAPDIEUCHINH-', đặt tại đúng vị "
     "trí của dòng, thuộc công ty của phiếu.\n"
     "- Số cộng vào tồn kho = Số lượng x hệ số quy đổi của ĐVT kiểm kê (quy về đơn vị cơ bản).\n"
     "- Công ty của phiếu là công ty của NGƯỜI LẬP PHIẾU KIỂM KÊ, không phải người lập phiếu nhập.\n"
     "- Bước kế toán chỉ cộng tồn kho kế toán, KHÔNG cộng lại tồn kho vật lý."),

    ("7. Phân quyền cấp",
     "- Vào danh sách, xem phiếu, in: chỉ cần đăng nhập, không kiểm quyền.\n"
     "- Lập phiếu: cần 'Xử lý phiếu kiểm kê hàng hóa' để thấy nút trên phiếu kiểm kê và nạp được hàng.\n"
     "- Phạm vi danh sách: 'Xem phiếu nhập kho điều chỉnh kiểm kê - theo tổng công ty' thấy mọi công ty; "
     "'Xem phiếu nhập kho điều chỉnh kiểm kê - theo công ty' thấy công ty mình; không có cả hai thì chỉ thấy "
     "phiếu mình lập.\n"
     "- Sửa: chỉ người lập, chỉ khi 'Đang tạo'.\n"
     "- Menu chờ duyệt và nút 'Tạo phiếu nhập hàng': cần 'Kế toán kho', phiếu đang 'Chờ duyệt'.\n"
     "- Ô lọc Công ty hiện với 'Xem tất cả phiếu' hoặc quyền xem theo tổng công ty; ô Phòng ban hiện thêm với "
     "quyền xem theo công ty."),

    ("8. Cách tính các ô thống kê",
     "Màn không có ô tổng. Số lượng mỗi dòng chi tiết = phần thừa còn chưa xử lý của dòng kết quả kiểm kê "
     "(Thực kiểm trừ Tồn theo lô, trừ phần đã xử lý).\n"
     "Tồn tăng trên báo cáo (đơn vị cơ bản) = Số lượng x hệ số của ĐVT kiểm kê."),

    ("9. Ghi chú đọc bảng",
     "Các lỗi ERP ĐÃ BIẾT được viết thành testcase với kết quả mong đợi ĐÚNG, kèm dòng 'Lỗi ERP đã biết'. "
     "Chạy thấy đúng hiện tượng lỗi thì ghi Failed và chép câu đó vào cột Ghi chú:\n"
     "(1) 'Báo cáo tồn theo kho': hàng có ĐVT kiểm kê hệ số lớn hơn 1, SL tồn chỉ tăng theo số lượng trên "
     "phiếu, không quy đổi (2 Thùng loại 24 Chai chỉ tăng 2 thay vì 48). Thẻ kho và Tổng hợp xuất nhập tồn "
     "vẫn đúng.\n"
     "(2) Bộ lọc Kho, Nhập mã hàng hóa, Nhập tên hàng hóa, Từ ngày, Đến ngày không có tác dụng.\n"
     "(3) Vừa mở trang Sửa đã báo 'Không có quyền'. Đổi Kho ở trang Sửa thì bảng Chi tiết không đổi theo, "
     "Gửi duyệt ghi tồn vào kho mới với vị trí của kho cũ.\n"
     "(4) Phiếu kiểm kê nhiều kho chỉ lập được một phiếu nhập cho một kho, hàng thừa ở kho còn lại không "
     "lập được, phiếu kiểm kê kẹt 'Đang xử lý'.\n"
     "(5) Hai tab cùng lập từ một phiếu kiểm kê thì ra 2 phiếu, tồn bị cộng 2 lần.\n"
     "(6) Lưu phiếu không kiểm quyền và không đối chiếu số thừa: gọi thẳng chức năng lưu được bằng tài khoản "
     "bất kỳ, số lượng tùy ý.\n"
     "(7) In danh sách: phiếu chưa duyệt vẫn hiện Ngày duyệt là ngày hôm nay.\n"
     "(8) Bấm 'Lưu' (nháp) vẫn báo 'Phiếu đã được gửi'.\n"
     "Ghi nhận hành vi ERP (thiết kế, không phải lỗi): Gửi duyệt ghi tồn ngay trước khi kế toán xử lý; "
     "màn không có Xóa, Hủy, Không duyệt nên KHÔNG có chiều ngược làm giảm lại số tồn; nút 'Tạo mới' trên "
     "danh sách mở trang trống không lập được phiếu.\n"
     "Nhóm 'Gọi thẳng chức năng' dành cho tester kỹ thuật, dùng công cụ kiểm thử API, bỏ qua giao diện.\n"
     "Dữ liệu mẫu: công ty TPE; kho LN có gắn kho kế toán của TPE, vị trí V1, V2, V3; kho MT của TPE. "
     "H1: đơn vị Cái (hệ số 1), tồn lô ở V1 là 10 Cái. H2: đơn vị cơ bản Chai, kiểm theo Thùng (1 Thùng = 24 "
     "Chai), tồn lô ở V1 là 5 Thùng. H3: có tồn ở V1 và V2. H4: có tồn ở V1. H5: có tồn ở kho MT. "
     "Phiếu kiểm kê KK1 (kho LN): H1 thực kiểm 13 (thừa 3), H2 thực kiểm 7 Thùng (thừa 2 Thùng = 48 Chai), "
     "H3 thừa 4 ở V1 và thiếu 4 ở V2, H4 thiếu 2. Phiếu kiểm kê KK2 gồm 2 kho LN và MT, thừa H1 ở LN và H5 "
     "ở MT. Tài khoản: TK (Thủ kho, có 'Xử lý phiếu kiểm kê hàng hóa', 'Xem phiếu nhập kho điều chỉnh kiểm "
     "kê - theo công ty', 'Xem báo cáo tồn kho theo công ty'); KT ('Kế toán kho'); BKS ('Ban kiểm soát duyệt "
     "kết quả kiểm kê'); A (xem theo tổng công ty); N (không có quyền xem nào); X (không có 'Xử lý phiếu "
     "kiểm kê hàng hóa')."),
]

# =========================================================================
# SECTION PHAN QUYEN
# =========================================================================
ROLE_TCS = [
    ("00", "Mở danh sách từ menu", "P0",
     "Tài khoản TK đăng nhập ERP",
     "1. Vào " + MENU,
     "Tài khoản: TK",
     "- Mở trang tiêu đề 'Phiếu nhập kho điều chỉnh kiểm kê'\n"
     "- Có nút Bộ lọc, Tạo mới, In, Xuất excel và bảng danh sách"),

    ("01", "Quyền xem theo tổng công ty thấy mọi công ty", "P0",
     "Tài khoản A có 'Xem phiếu nhập kho điều chỉnh kiểm kê - theo tổng công ty'. Có phiếu đã gửi duyệt của "
     "ít nhất 2 công ty",
     "1. Đăng nhập A, mở danh sách",
     "Tài khoản: A",
     "- Thấy phiếu của mọi công ty, trừ phiếu 'Đang tạo' của người khác"),

    ("02", "Quyền xem theo công ty chỉ thấy công ty mình", "P0",
     "Tài khoản TK thuộc TPE, có quyền xem theo công ty, không có quyền xem theo tổng công ty. Có phiếu đã "
     "gửi duyệt của công ty khác",
     "1. Đăng nhập TK, mở danh sách",
     "Tài khoản: TK",
     "- Chỉ thấy phiếu của công ty TPE\n- Không thấy phiếu của công ty khác"),

    ("03", "Không có quyền xem nào chỉ thấy phiếu mình lập", "P1",
     "Tài khoản N không có cả 2 quyền xem. N đã lập 1 phiếu, người khác cùng công ty cũng có phiếu",
     "1. Đăng nhập N, mở danh sách",
     "Tài khoản: N",
     "- Chỉ thấy phiếu do N lập"),

    ("04", "Phiếu Đang tạo chỉ người lập thấy", "P0",
     "TK vừa bấm 'Lưu' một phiếu, phiếu ở 'Đang tạo'. Tài khoản A có quyền xem theo tổng công ty",
     "1. Đăng nhập A, mở danh sách, lọc Mã phiếu của phiếu đó\n2. Đăng nhập TK, làm lại bước 1",
     "",
     "- Bước 1: không thấy phiếu\n- Bước 2: thấy phiếu, trạng thái 'Đang tạo'"),

    ("05", "Menu chờ duyệt chỉ hiện với Kế toán kho", "P0",
     "Tài khoản KT có 'Kế toán kho'. Tài khoản TK không có",
     "1. Đăng nhập KT, mở " + MENU_CHO_DUYET + "\n2. Đăng nhập TK, mở menu Chờ duyệt > Hàng hóa - dịch vụ - "
     "vận chuyển",
     "Tài khoản: KT, TK",
     "- Bước 1: thấy mục menu, danh sách chỉ có phiếu 'Chờ duyệt'\n- Bước 2: không có mục menu này"),

    ("06", "Danh sách chờ duyệt thấy phiếu của mọi công ty", "P2",
     "Tài khoản KT thuộc TPE. Có phiếu Chờ duyệt của công ty khác",
     "1. Đăng nhập KT, mở danh sách chờ duyệt",
     "",
     "- Ghi nhận hành vi ERP: thấy cả phiếu Chờ duyệt của công ty khác, không giới hạn theo công ty"),

    ("07", "Thiếu quyền xử lý kiểm kê không lập được phiếu", "P0",
     "Tài khoản X không có 'Xử lý phiếu kiểm kê hàng hóa'. Phiếu kiểm kê KK1 đang 'Chờ xử lý'",
     "1. Đăng nhập X, mở " + MENU_KIEM_KE + ", mở phiếu KK1",
     "Tài khoản: X",
     "- Không có nút 'Tạo phiếu nhập kho điều chuyển'"),

    ("08", "Ô lọc Công ty và Phòng ban theo quyền", "P2",
     "Tài khoản A có quyền xem theo tổng công ty, TK có quyền xem theo công ty, N không có quyền xem",
     "1. Lần lượt đăng nhập A, TK, N, mở danh sách, bấm 'Bộ lọc'",
     "",
     "- A: có ô Công ty và ô Phòng ban\n- TK: có ô Phòng ban, không có ô Công ty\n- N: không có 2 ô này"),

    ("09", "Gọi thẳng chức năng lưu phiếu khi thiếu quyền", "P1",
     "Tester kỹ thuật. Tài khoản N không có quyền xử lý kiểm kê. Biết mã phiếu kiểm kê KK1",
     "1. Đăng nhập N\n2. Dùng công cụ kiểm thử API gọi thẳng chức năng lưu phiếu nhập kho điều chỉnh với "
     "trạng thái Gửi duyệt, H1 số lượng 100",
     "Phiếu KK1, H1, 100",
     "- Hệ thống từ chối vì không có quyền và số lượng khác phần thừa\n"
     "- Lỗi ERP đã biết: lưu thành công, tồn H1 tăng 100"),

    ("10", "Gọi thẳng chức năng Sửa phiếu của người khác", "P2",
     "Tester kỹ thuật. Phiếu P1 'Đang tạo' do TK lập. Tài khoản N",
     "1. Đăng nhập N\n2. Gọi thẳng chức năng Sửa phiếu P1",
     "",
     "- Báo 'Bạn không có quyền sửa phiếu này'\n- Phiếu P1 không đổi"),
]

# =========================================================================
# CAC SECTION CHUC NANG
# =========================================================================
SECTIONS = [
    ("I", "Chuẩn bị dữ liệu test", [
        ("001", "Chuẩn bị tài khoản và quyền", "P0",
         "Có quyền quản trị phân quyền trên ERP dev",
         "1. Gán cho TK: 'Thủ kho', 'Xử lý phiếu kiểm kê hàng hóa', 'Xem phiếu nhập kho điều chỉnh kiểm kê - "
         "theo công ty', 'Xem báo cáo tồn kho theo công ty'\n"
         "2. Gán cho KT: 'Kế toán kho', 'Xem báo cáo tồn kho kế toán theo công ty'\n"
         "3. Gán cho BKS: 'Ban kiểm soát duyệt kết quả kiểm kê'\n4. Đăng xuất, đăng nhập lại từng tài khoản",
         "Tài khoản: TK, KT, BKS",
         "- Mỗi tài khoản thấy đúng menu: TK thấy " + BC_THE_KHO + "\n"
         "- KT thấy " + MENU_CHO_DUYET),

        ("002", "Tìm hàng đang có tồn theo lô để kiểm kê", "P0",
         "Có quyền chạy câu truy vấn chỉ đọc trên dữ liệu dev, hoặc dùng báo cáo kho",
         "1. Chạy câu truy vấn 'sql/3_hang_co_ton_de_lap_phieu_kiem_ke.sql'\n"
         "2. Chọn 1 hàng hệ số 1 làm H1 và 1 hàng có đơn vị hệ số lớn hơn 1 làm H2, cùng kho LN\n"
         "3. Hoặc mở " + BC_THE_KHO + " để xem tồn từng hàng",
         "Kho LN, H1, H2",
         "- Ghi được: mã kho, vị trí, mã hàng, tồn theo lô của H1, H2, H3, H4 tại LN\n"
         "- H2 có ĐVT như Thùng hệ số 24"),

        ("003", "Lập phiếu kiểm kê theo hàng hóa", "P0",
         "Tài khoản TK. H1 đến H4 không có phiếu nhập / xuất đang dở dang tại kho LN",
         "1. Vào " + MENU_KIEM_KE + ", bấm 'Tạo mới'\n"
         "2. Chọn Ngày kiểm kê, Kho LN, Công ty thuê kho TPE\n3. Thêm hàng H1, H2, H3, H4 cùng vị trí, lô\n"
         "4. Thêm thành viên kiểm kê\n5. Bấm 'Lưu & gửi'",
         "Kho LN, H1 đến H4",
         "- Lưu thành công, phiếu KK1 ở trạng thái 'Đang kiểm'\n"
         "- Nếu hàng đang có phiếu dở dang thì hệ thống chặn, phải chọn hàng khác"),

        ("004", "Nhập kết quả kiểm có hàng thừa", "P0",
         "Phiếu KK1 'Đang kiểm', TK là người lập",
         "1. Bánh răng dòng KK1, chọn 'Cập nhật kết quả'\n"
         "2. Cột Thực kiểm: H1 là 13, H2 chọn ĐVT kiểm kê Thùng và nhập 7, H3 ở V1 cộng thêm 4 và ở V2 bớt 4, "
         "H4 bớt 2\n3. Thêm File kết quả\n4. Bấm 'Gửi duyệt'",
         "H1 tồn 10, H2 tồn 5 Thùng",
         "- Cột Chênh lệch: H1 là 3, H2 là 2, H3 là 4 và -4, H4 là -2\n"
         "- Báo 'Thao tác thành công', KK1 sang 'Chờ KT duyệt'"),

        ("005", "Duyệt kết quả kiểm kê", "P0",
         "Phiếu KK1 'Chờ KT duyệt'",
         "1. Đăng nhập BKS, mở " + MENU_KIEM_KE + "\n2. Bánh răng dòng KK1, chọn 'Duyệt', bấm 'Duyệt'",
         "Tài khoản: BKS",
         "- KK1 sang 'Chờ xử lý'\n- Phiếu không có chênh lệch nào thì sang 'Hoàn thành', không lập được "
         "phiếu nhập"),

        ("006", "Nút lập phiếu xuất hiện trên phiếu kiểm kê", "P0",
         "Phiếu KK1 'Chờ xử lý'",
         "1. Đăng nhập TK, mở " + MENU_KIEM_KE + "\n2. Bánh răng dòng KK1, chọn 'Xử lý'",
         "Tài khoản: TK",
         "- Có nút 'Tạo phiếu nhập kho điều chuyển'\n"
         "- Có thêm 'Tạo phiếu điều chuyển vị trí' (do H3) và 'Tạo phiếu xuất kho điều chuyển' (do H4)"),

        ("007", "Dùng phiếu kiểm kê có sẵn trên dev", "P1",
         "Không muốn tự lập phiếu kiểm kê",
         "1. Chạy câu truy vấn 'sql/1_phieu_kiem_ke_lap_duoc_phieu_nhap.sql'\n"
         "2. Chọn một số phiếu kiểm kê trong kết quả, mở phiếu đó bằng tài khoản có 'Xử lý phiếu kiểm kê hàng "
         "hóa'",
         "",
         "- Mỗi dòng kết quả là một dòng sẽ hiện ở bảng Chi tiết, đúng kho, vị trí, số lượng\n"
         "- Phiếu mở ra có nút 'Tạo phiếu nhập kho điều chuyển'"),

        ("008", "Chuẩn bị phiếu kiểm kê 2 kho", "P2",
         "Như TC 003",
         "1. Lập phiếu kiểm kê KK2 chọn 2 kho LN và MT\n2. Kết quả: H1 thừa 1 ở LN, H5 thừa 2 ở MT\n"
         "3. Gửi duyệt, BKS duyệt",
         "Kho LN, MT",
         "- KK2 'Chờ xử lý', dùng cho TC lỗi phiếu nhiều kho"),

        ("009", "Tìm phiếu nhập kho điều chỉnh có sẵn", "P2",
         "",
         "1. Chạy câu truy vấn 'sql/2_phieu_nhap_dieu_chinh_da_co.sql'",
         "",
         "- Liệt kê phiếu theo trạng thái, kèm số lô đã sinh\n"
         "- Dòng ghi 'CO' ở cột ghi chú là hàng hệ số lớn hơn 1, dùng đối chiếu lỗi báo cáo tồn theo kho"),
    ]),

    ("II", "Giao diện danh sách", [
        ("001", "Bố cục danh sách", "P0",
         "Tài khoản TK, có sẵn phiếu",
         "1. Vào " + MENU,
         "",
         "- Tiêu đề 'Phiếu nhập kho điều chỉnh kiểm kê'\n- Nút Bộ lọc, Tạo mới, In, Xuất excel\n"
         "- Bảng 7 cột: STT, Số phiếu, Ngày kiểm kê, Kho, Trạng thái, Người lập, Hành động"),

        ("002", "Thứ tự mặc định", "P2",
         "Vừa gửi duyệt 1 phiếu mới",
         "1. Mở danh sách",
         "",
         "- Phiếu mới nhất nằm đầu bảng"),

        ("003", "Nội dung từng cột", "P1",
         "Phiếu P2 đã gửi duyệt từ KK1",
         "1. Xem dòng P2\n2. Bấm Số phiếu",
         "",
         "- Số phiếu dạng 'PNKĐCKK-' và 5 chữ số, bấm vào mở trang xem\n- Kho là tên kho LN\n"
         "- Trạng thái 'Chờ duyệt'\n- Người lập là TK"),

        ("004", "Cột Ngày kiểm kê", "P2",
         "KK1 kiểm ngày 10, phiếu nhập P2 lập ngày 12",
         "1. Xem cột Ngày kiểm kê dòng P2",
         "",
         "- Ghi nhận hành vi ERP: cột hiện ngày 12 (ngày lập phiếu nhập) dạng ngày/tháng/năm"),

        ("005", "Hành động của phiếu Đang tạo", "P0",
         "Phiếu P1 'Đang tạo' do TK lập",
         "1. Đăng nhập TK, bấm bánh răng dòng P1",
         "",
         "- Có 'Sửa' và 'In'\n- Không có 'Tạo phiếu nhập hàng'"),

        ("006", "Hành động của phiếu Chờ duyệt", "P0",
         "Phiếu P2 'Chờ duyệt'",
         "1. Đăng nhập TK, bấm bánh răng dòng P2\n2. Đăng nhập KT, bấm bánh răng dòng P2",
         "",
         "- Bước 1: chỉ có 'In'\n- Bước 2: có 'Tạo phiếu nhập hàng' và 'In'"),

        ("007", "Hành động của phiếu đã sang kế toán", "P1",
         "Phiếu P3 'Đã hạch toán'",
         "1. Đăng nhập KT, bấm bánh răng dòng P3",
         "",
         "- Chỉ có 'In'"),

        ("008", "Không có chức năng Xóa / Hủy phiếu", "P1",
         "Có phiếu ở mọi trạng thái",
         "1. Bấm bánh răng từng dòng",
         "",
         "- Ghi nhận hành vi ERP: không trạng thái nào có Xóa, Hủy hay Không duyệt"),

        ("009", "Nút Tạo mới trên danh sách", "P1",
         "Tài khoản TK",
         "1. Bấm 'Tạo mới'\n2. Nhập Ghi chú, thêm file, bấm 'Gửi duyệt'",
         "",
         "- Trang không có ô Phiếu kiểm kho, bảng Chi tiết trống\n- Báo 'Tạo thất bại!', dưới bảng báo "
         "'Bắt buộc phải nhập'\n- Ghi nhận hành vi ERP: chỉ lập được phiếu từ phiếu kiểm kê"),

        ("010", "Phân trang", "P2",
         "Có hơn 10 phiếu",
         "1. Chuyển sang trang 2\n2. Đổi số dòng mỗi trang",
         "",
         "- STT trang 2 nối tiếp trang 1\n- Bảng tải lại đúng số dòng"),
    ]),

    ("III", "Bộ lọc danh sách", [
        ("001", "Lọc Mã phiếu", "P0",
         "Có phiếu P2",
         "1. Bấm 'Bộ lọc'\n2. Ô Mã phiếu gõ một phần số phiếu P2",
         "",
         "- Bảng chỉ còn phiếu có số phiếu chứa chuỗi đã gõ"),

        ("002", "Lọc Trạng thái", "P0",
         "Có phiếu Đang tạo, Chờ duyệt, Đã hạch toán",
         "1. Ô Trạng thái chọn 'Chờ duyệt'",
         "",
         "- Chỉ còn phiếu 'Chờ duyệt'\n- Ô có đủ 4 lựa chọn: Đang tạo, Chờ duyệt, Đang hạch toán, Đã hạch toán"),

        ("003", "Lọc Người tạo", "P1",
         "TK và người khác cùng có phiếu",
         "1. Ô Người tạo gõ tên TK, chọn TK",
         "",
         "- Chỉ còn phiếu Người lập là TK"),

        ("004", "Lọc Kho", "P1",
         "Có phiếu ở kho LN và kho khác",
         "1. Ô Kho chọn LN",
         "Kho LN",
         "- Chỉ còn phiếu kho LN\n- Lỗi ERP đã biết: bảng không đổi, vẫn hiện phiếu mọi kho"),

        ("005", "Lọc theo mã hàng và tên hàng", "P1",
         "Phiếu P2 có H1. Phiếu khác không có H1",
         "1. Ô 'Nhập mã hàng hóa' gõ mã H1\n2. Xóa, ô 'Nhập tên hàng hóa' gõ tên H1",
         "",
         "- Chỉ còn phiếu có H1\n- Lỗi ERP đã biết: cả 2 ô không có tác dụng"),

        ("006", "Lọc khoảng ngày", "P1",
         "Có phiếu lập tháng trước và tháng này",
         "1. Từ ngày chọn ngày đầu tháng này, Đến ngày chọn hôm nay",
         "",
         "- Chỉ còn phiếu lập trong tháng này\n- Lỗi ERP đã biết: bảng không đổi"),

        ("007", "Lọc Công ty", "P1",
         "Tài khoản A có quyền xem theo tổng công ty. Có phiếu TPE và công ty khác",
         "1. Ô Công ty chọn TPE",
         "",
         "- Chỉ còn phiếu của TPE\n- Ô Phòng ban chỉ còn phòng ban của TPE"),

        ("008", "Lọc Phòng ban", "P2",
         "Tài khoản TK có quyền xem theo công ty",
         "1. Ô Phòng ban chọn phòng của người lập phiếu kiểm kê KK1",
         "",
         "- Chỉ còn phiếu thuộc phòng ban đó (phòng của người lập phiếu kiểm kê)"),

        ("009", "Kết hợp lọc và bỏ lọc", "P2",
         "",
         "1. Chọn Trạng thái 'Chờ duyệt' và gõ Mã phiếu\n2. Xóa hết điều kiện",
         "",
         "- Bước 1: bảng thu hẹp theo cả 2 điều kiện\n- Bước 2: hiện lại đủ phiếu theo phạm vi xem"),
    ]),

    ("IV", "Lập phiếu: mở trang và nạp hàng thừa", [
        ("001", "Mở trang lập từ phiếu kiểm kê", "P0",
         "Phiếu KK1 'Chờ xử lý'. Tài khoản TK",
         "1. Mở KK1, bấm 'Tạo phiếu nhập kho điều chuyển'",
         "",
         "- Trang 'Phiếu nhập kho điều chỉnh kiểm kê', khung 'Thông tin chung' và 'Chi tiết'\n"
         "- Ô Phiếu kiểm kho hiện số phiếu KK1, bấm vào mở phiếu kiểm kê ở tab mới\n"
         "- Có nút Lưu, Gửi duyệt, Hủy"),

        ("002", "Kho lấy sẵn theo phiếu kiểm kê", "P0",
         "Như TC trên",
         "1. Xem ô Kho\n2. Mở ô Kho",
         "",
         "- Ô Kho chọn sẵn kho LN\n- Danh sách chỉ có kho thuộc phiếu kiểm kê"),

        ("003", "Bảng Chi tiết chỉ có hàng thừa", "P0",
         "KK1: H1 thừa 3, H2 thừa 2 Thùng, H3 thừa 4 ở V1 và thiếu 4 ở V2, H4 thiếu 2",
         "1. Xem bảng Chi tiết",
         "",
         "- Có đúng 2 dòng: H1 số lượng 3 và H2 số lượng 2\n- Không có H3, không có H4"),

        ("004", "Thông tin từng dòng", "P0",
         "Như TC trên",
         "1. Xem dòng H1 và H2",
         "",
         "- Tên hàng hóa, Model, Mã hàng hóa đúng\n- Vị trí là mã vị trí kiểm ra thừa (V1)\n"
         "- ĐVT là ĐVT kiểm kê: H1 Cái, H2 Thùng"),

        ("005", "Số lượng không sửa được", "P1",
         "Như TC trên",
         "1. Bấm vào ô Số lượng dòng H1",
         "",
         "- Số lượng chỉ hiển thị, không có ô nhập\n- Không thêm, không bớt được dòng"),

        ("006", "Hàng thừa nhiều vị trí ra nhiều dòng", "P1",
         "Phiếu kiểm kê có H1 thừa 2 ở V1 và thừa 1 ở V2",
         "1. Mở trang lập phiếu từ phiếu kiểm kê đó",
         "",
         "- 2 dòng H1: V1 số lượng 2, V2 số lượng 1"),

        ("007", "Hàng vừa thừa vừa thiếu ở vị trí khác", "P2",
         "Phiếu kiểm kê có H1 thừa 5 ở V1 và thiếu 2 ở V2 (tổng thừa 3)",
         "1. Mở trang lập phiếu",
         "",
         "- Ghi nhận hành vi ERP: có dòng H1 V1 số lượng 5 (cả phần thừa của V1)\n"
         "- Phần thiếu 2 ở V2 xử lý ở phiếu xuất kho điều chỉnh"),

        ("008", "Phiếu kiểm kê nhiều kho: đổi kho", "P1",
         "Phiếu KK2 có 2 kho LN và MT",
         "1. Mở trang lập từ KK2\n2. Đổi ô Kho sang MT",
         "",
         "- Bước 1: Kho chọn sẵn kho đầu tiên, bảng chỉ có hàng thừa của kho đó\n"
         "- Bước 2: bảng nạp lại, chỉ còn H5 của kho MT"),

        ("009", "Kho không có hàng thừa", "P2",
         "Phiếu kiểm kê 2 kho, kho MT không có dòng thừa",
         "1. Đổi ô Kho sang MT",
         "",
         "- Bảng Chi tiết trống"),

        ("010", "Phiếu kiểm kê đã lập phiếu nhập thì không lập lại", "P0",
         "KK1 đã có phiếu nhập P2",
         "1. Mở lại KK1",
         "",
         "- Không còn nút 'Tạo phiếu nhập kho điều chuyển'\n- KK1 ở 'Đang xử lý'"),

        ("011", "Phiếu kiểm kê 2 kho chỉ lập được cho 1 kho", "P1",
         "KK2 (LN, MT). Đã lập và gửi duyệt phiếu nhập cho kho LN",
         "1. Mở lại KK2",
         "",
         "- Vẫn lập được phiếu nhập cho phần thừa H5 ở kho MT\n"
         "- Lỗi ERP đã biết: mất nút lập phiếu, H5 không được nhập, KK2 kẹt 'Đang xử lý'"),

        ("012", "Người không có quyền xử lý mở trang lập", "P2",
         "Tài khoản X không có 'Xử lý phiếu kiểm kê hàng hóa'. Đã có sẵn trang lập phiếu từ KK1 được TK "
         "gửi qua (sao chép từ thanh địa chỉ)",
         "1. Đăng nhập X, mở trang lập đó",
         "",
         "- Hiện cảnh báo 'Không có quyền'\n- Bảng Chi tiết trống, không lập được phiếu"),

        ("013", "Hủy lập phiếu", "P2",
         "Đang ở trang lập phiếu",
         "1. Bấm 'Hủy'",
         "",
         "- Về danh sách, không sinh phiếu\n- KK1 vẫn còn nút 'Tạo phiếu nhập kho điều chuyển'"),
    ]),

    ("V", "Ràng buộc nhập liệu khi lưu", [
        ("001", "Ghi chú bắt buộc", "P0",
         "Trang lập từ KK1, đã thêm file, Ghi chú để trống",
         "1. Bấm 'Gửi duyệt'",
         "",
         "- Báo 'Tạo thất bại!'\n- Dưới ô Ghi chú báo 'Bắt buộc phải nhập'\n- Không sinh phiếu"),

        ("002", "File đính kèm bắt buộc khi lập", "P0",
         "Trang lập từ KK1, có Ghi chú, chưa thêm file",
         "1. Bấm 'Lưu'",
         "",
         "- Báo 'Tạo thất bại!'\n- Dưới File đính kèm báo 'Bắt buộc phải nhập'"),

        ("003", "Thêm ô file nhưng không chọn file", "P1",
         "Có Ghi chú",
         "1. Bấm dấu cộng ở File đính kèm, không chọn file\n2. Bấm 'Gửi duyệt'",
         "",
         "- Báo 'Tạo thất bại!'\n- Ô file trống viền đỏ báo lỗi"),

        ("004", "Ô chọn file chỉ gợi ý PDF", "P2",
         "",
         "1. Bấm dấu cộng, bấm 'Chọn file'",
         "",
         "- Hộp chọn file chỉ lọc sẵn file PDF\n- Ghi nhận hành vi ERP: đổi sang xem mọi file thì chọn được ảnh "
         "PNG, JPG và lưu vẫn nhận"),

        ("005", "File sai định dạng", "P1",
         "Có Ghi chú",
         "1. Thêm file .docx\n2. Bấm 'Gửi duyệt'",
         "File .docx",
         "- Báo 'Tạo thất bại!', ô file viền đỏ\n- Không sinh phiếu"),

        ("006", "Bỏ một file đã thêm", "P2",
         "Đã thêm 2 file",
         "1. Bấm dấu x ở file thứ 2",
         "",
         "- File bị bỏ khỏi danh sách đính kèm"),

        ("007", "Bảng Chi tiết trống", "P1",
         "Kho đang chọn không có hàng thừa",
         "1. Nhập Ghi chú, thêm file\n2. Bấm 'Gửi duyệt'",
         "",
         "- Báo 'Tạo thất bại!', dưới bảng Chi tiết báo 'Bắt buộc phải nhập'"),

        ("008", "Bấm lưu liên tục", "P2",
         "Trang lập hợp lệ",
         "1. Bấm 'Gửi duyệt' 3 lần thật nhanh",
         "",
         "- Nút khóa và hiện biểu tượng xoay khi đang gửi\n- Chỉ sinh 1 phiếu"),
    ]),

    ("VI", "Lưu nháp và Gửi duyệt", [
        ("001", "Lưu nháp", "P0",
         "Trang lập từ KK1, có Ghi chú và file",
         "1. Bấm 'Lưu'",
         "",
         "- Hiện thông báo thành công, về danh sách\n- Có phiếu mới 'Đang tạo', Người lập TK\n"
         "- Thông báo phải là đã lưu. Lỗi ERP đã biết: báo 'Phiếu đã được gửi'"),

        ("002", "Gửi duyệt", "P0",
         "Trang lập từ KK1, có Ghi chú và file",
         "1. Bấm 'Gửi duyệt'",
         "",
         "- Báo 'Phiếu đã được gửi', về danh sách\n- Phiếu mới 'Chờ duyệt', số phiếu 'PNKĐCKK-' và 5 chữ số"),

        ("003", "Phiếu kiểm kê chuyển Đang xử lý", "P1",
         "Vừa Lưu hoặc Gửi duyệt phiếu từ KK1",
         "1. Mở " + MENU_KIEM_KE + ", xem KK1",
         "",
         "- KK1 sang 'Đang xử lý' (cả khi chỉ Lưu nháp)"),

        ("004", "Thông báo cho kế toán kho", "P1",
         "Vừa Gửi duyệt phiếu P2",
         "1. Đăng nhập KT, mở chuông thông báo\n2. Bấm thông báo",
         "",
         "- Có 'Bạn có 1 phiếu nhập kho điều chỉnh cần duyệt'\n- Bấm vào mở trang xem P2"),

        ("005", "Lưu nháp không báo cho kế toán", "P2",
         "Vừa Lưu nháp phiếu P1",
         "1. Đăng nhập KT, xem thông báo",
         "",
         "- Không có thông báo mới về P1"),

        ("006", "Công ty của phiếu theo người lập phiếu kiểm kê", "P2",
         "KK1 do nhân viên công ty TPE lập. Người lập phiếu nhập thuộc công ty khác, được xử lý kiểm kê",
         "1. Gửi duyệt phiếu nhập từ KK1\n2. Đăng nhập A, lọc Công ty TPE",
         "",
         "- Ghi nhận hành vi ERP: phiếu thuộc công ty TPE (công ty người lập phiếu kiểm kê)"),

        ("007", "Hai tab cùng lập từ một phiếu kiểm kê", "P1",
         "Tab 1 và tab 2 cùng mở trang lập từ KK1",
         "1. Tab 1 bấm 'Gửi duyệt'\n2. Tab 2 bấm 'Gửi duyệt'",
         "",
         "- Tab 2 bị chặn vì phiếu kiểm kê đã có phiếu nhập\n"
         "- Lỗi ERP đã biết: sinh 2 phiếu, tồn H1, H2 bị cộng 2 lần"),

        ("008", "Gọi thẳng chức năng lưu với số lượng khác phần thừa", "P2",
         "Tester kỹ thuật. Tài khoản TK, phiếu kiểm kê có H1 thừa 3",
         "1. Gọi thẳng chức năng lưu, H1 số lượng 30, trạng thái Gửi duyệt",
         "",
         "- Hệ thống chặn vì khác phần thừa 3\n- Lỗi ERP đã biết: lưu thành công, tồn H1 tăng 30"),
    ]),

    ("VII", "Sửa phiếu nháp", [
        ("001", "Mở trang Sửa", "P0",
         "Phiếu P1 'Đang tạo' do TK lập",
         "1. Bánh răng dòng P1, chọn 'Sửa'",
         "",
         "- Tiêu đề kèm số phiếu P1\n- Hiện đúng Kho, Ghi chú, file đã đính kèm, bảng Chi tiết như lúc lưu\n"
         "- Không có cảnh báo nào. Lỗi ERP đã biết: vừa mở đã báo 'Không có quyền'"),

        ("002", "Sửa Ghi chú và Lưu", "P0",
         "Trang Sửa P1",
         "1. Sửa Ghi chú\n2. Bấm 'Lưu'",
         "",
         "- Về danh sách, P1 vẫn 'Đang tạo'\n- Mở lại thấy Ghi chú mới"),

        ("003", "Gửi duyệt từ trang Sửa", "P0",
         "Trang Sửa P1",
         "1. Bấm 'Gửi duyệt'",
         "",
         "- Báo 'Phiếu đã được gửi', P1 sang 'Chờ duyệt'\n- Kế toán kho nhận thông báo"),

        ("004", "Thêm file khi đã có file", "P1",
         "P1 đã có 1 file",
         "1. Thêm 1 file mới, bấm 'Lưu'",
         "",
         "- P1 có 2 file: file cũ vẫn còn, file mới thêm vào"),

        ("005", "Không xóa được file cũ", "P2",
         "P1 đã có file",
         "1. Tìm nút bỏ ở file cũ",
         "",
         "- Ghi nhận hành vi ERP: file cũ chỉ xem, không bỏ được"),

        ("006", "Xóa trắng Ghi chú khi sửa", "P1",
         "Trang Sửa P1",
         "1. Xóa trắng Ghi chú, bấm 'Lưu'",
         "",
         "- Báo 'Sửa thất bại!', dưới Ghi chú báo 'Bắt buộc phải nhập'"),

        ("007", "Đổi Kho ở trang Sửa", "P1",
         "P1 lập từ KK2 cho kho LN, có dòng H1 V1",
         "1. Mở Sửa P1, đổi Kho sang MT\n2. Xem bảng Chi tiết, bấm 'Gửi duyệt'",
         "",
         "- Bảng nạp lại hàng thừa của kho MT, hoặc không cho đổi kho\n"
         "- Lỗi ERP đã biết: bảng vẫn giữ H1 V1 của kho LN, gửi duyệt ghi tồn H1 vào kho MT tại vị trí V1 "
         "của kho LN"),

        ("008", "Phiếu không còn Đang tạo thì không sửa", "P0",
         "P2 'Chờ duyệt'. Đã sao chép địa chỉ trang Sửa của P2 khi còn Đang tạo",
         "1. Dán lại địa chỉ trang Sửa P2",
         "",
         "- Ra trang không tìm thấy"),

        ("009", "Người khác không sửa được", "P1",
         "P1 'Đang tạo' do TK lập. Tài khoản A",
         "1. Đăng nhập A, mở địa chỉ trang Sửa P1 do TK gửi",
         "",
         "- Ra trang không tìm thấy"),

        ("010", "Hủy sửa", "P2",
         "Trang Sửa P1, đã sửa Ghi chú",
         "1. Bấm 'Hủy'",
         "",
         "- Về danh sách, Ghi chú không đổi"),
    ]),

    ("VIII", "Xem chi tiết, In, Xuất Excel", [
        ("001", "Trang xem phiếu", "P0",
         "Phiếu P2 'Chờ duyệt'",
         "1. Bấm Số phiếu P2",
         "",
         "- Tiêu đề kèm số phiếu\n- Phiếu kiểm kho, Kho, Ghi chú, file đính kèm hiện đúng và bị khóa\n"
         "- Bảng Chi tiết đúng hàng, vị trí, số lượng\n- Chỉ có nút 'Hủy' để quay về"),

        ("002", "Mở file đính kèm", "P2",
         "Trang xem P2",
         "1. Bấm biểu tượng file",
         "",
         "- File mở ở tab mới"),

        ("003", "Xem phiếu không cần quyền", "P2",
         "Tài khoản N không có quyền xem nào, có địa chỉ trang xem P2",
         "1. Đăng nhập N, mở trang xem P2",
         "",
         "- Ghi nhận hành vi ERP: xem được phiếu"),

        ("004", "In một phiếu", "P0",
         "Phiếu P2",
         "1. Bánh răng dòng P2, chọn 'In'",
         "",
         "- Bản in khổ ngang có Số phiếu, Ngày lập, Phiếu kiểm kê KK1, Kho, Ghi chú\n"
         "- Bảng STT, Tên hàng, Model, Mã hàng, ĐVT, Vị trí, SL nhập: H1 V1 3, H2 V1 2"),

        ("005", "In danh sách theo bộ lọc", "P1",
         "Lọc Trạng thái 'Chờ duyệt'",
         "1. Bấm 'In'",
         "",
         "- Tab mới mở bản in danh sách, chỉ có phiếu Chờ duyệt\n"
         "- Cột: STT, Số phiếu, Phiếu kiểm kê, Kho, Người lập, Ngày lập, Người duyệt, Ngày duyệt, Trạng thái"),

        ("006", "Ngày duyệt trên bản in danh sách", "P2",
         "Phiếu P2 'Chờ duyệt', chưa có người duyệt",
         "1. In danh sách có P2",
         "",
         "- Ô Ngày duyệt của P2 để trống\n- Lỗi ERP đã biết: hiện ngày hôm nay"),

        ("007", "Xuất Excel theo bộ lọc", "P0",
         "Lọc Mã phiếu P2",
         "1. Bấm 'Xuất excel'",
         "",
         "- Tải file 'danh_sach_phieu_nhap_kho_dieu_chinh_kiem_ke.xlsx'\n"
         "- Tiêu đề 'Danh sách phiếu nhập kho điều chỉnh kiểm kê', cùng các cột như bản in danh sách\n"
         "- Chỉ có dòng P2"),

        ("008", "Xuất Excel theo phạm vi xem", "P1",
         "Tài khoản TK chỉ xem theo công ty TPE",
         "1. Không lọc, bấm 'Xuất excel'",
         "",
         "- File chỉ có phiếu của TPE và phiếu Đang tạo của chính TK"),
    ]),

    ("IX", "Bước kế toán kho và trạng thái phiếu", [
        ("001", "Mở lập phiếu nhập hàng từ phiếu chờ duyệt", "P0",
         "Phiếu P2 'Chờ duyệt'. Tài khoản KT",
         "1. Mở " + MENU_CHO_DUYET + "\n2. Bánh răng dòng P2, chọn 'Tạo phiếu nhập hàng'",
         "",
         "- Mở trang 'Nhập điều chỉnh sau kiểm kho', nạp sẵn hàng H1, H2 và số lượng của P2\n"
         "- Có nút Lưu, Lưu và duyệt"),

        ("002", "Kế toán Lưu: phiếu sang Đang hạch toán", "P0",
         "Đang ở trang lập phiếu nhập hàng từ P2, đã chia số lượng vào kho kế toán",
         "1. Bấm 'Lưu'\n2. Mở lại " + MENU + ", xem P2",
         "",
         "- P2 sang 'Đang hạch toán'\n- P2 không còn ở danh sách chờ duyệt, không còn 'Tạo phiếu nhập hàng'"),

        ("003", "Kế toán Lưu và duyệt: phiếu sang Đã hạch toán", "P0",
         "Phiếu P4 'Chờ duyệt'",
         "1. KT lập phiếu nhập hàng từ P4, bấm 'Lưu và duyệt'\n2. Xem P4 ở danh sách",
         "",
         "- P4 sang 'Đã hạch toán'\n- Người duyệt trên bản in danh sách là KT, Ngày duyệt là hôm nay"),

        ("004", "Phiếu kiểm kê hoàn thành sau khi xử lý hết", "P1",
         "KK1 có H1, H2 thừa; H3 đã điều chuyển vị trí; H4 đã xuất điều chỉnh xong",
         "1. KT 'Lưu và duyệt' phiếu nhập hàng từ P2 đủ số lượng\n2. Mở KK1",
         "",
         "- KK1 sang 'Hoàn thành'"),

        ("005", "Phiếu kiểm kê vẫn Đang xử lý khi còn việc", "P2",
         "KK1 chưa lập phiếu xuất cho H4",
         "1. KT 'Lưu và duyệt' phiếu nhập hàng từ P2\n2. Mở KK1",
         "",
         "- KK1 vẫn 'Đang xử lý'"),

        ("006", "Kế toán thiếu quyền không lập được", "P1",
         "Tài khoản TK không có 'Kế toán kho', P2 'Chờ duyệt'",
         "1. KT bấm 'Tạo phiếu nhập hàng' ở dòng P2, sao chép địa chỉ trang vừa mở gửi cho TK\n"
         "2. Đăng nhập TK, mở địa chỉ đó",
         "",
         "- Hiện 'Không có quyền!', không nạp được hàng"),
    ]),

    ("X", "Ghi tồn kho vật lý khi Gửi duyệt", [
        ("001", "Sinh lô mới tại đúng vị trí", "P0",
         "Vừa Gửi duyệt P2 (H1 V1 3, H2 V1 2 Thùng)",
         "1. Lập phiếu xuất kho H1 từ kho LN\n2. Mở cửa sổ chọn lô / vị trí xuất",
         "",
         "- Có lô số bắt đầu bằng 'NHAPDIEUCHINH-' ở V1 với số lượng 3\n- Chọn lô này xuất được bình thường"),

        ("002", "Lô của hàng quy đổi đơn vị", "P1",
         "Như TC trên",
         "1. Lập phiếu xuất kho H2 từ kho LN, mở cửa sổ chọn lô",
         "",
         "- Lô 'NHAPDIEUCHINH-' của H2 ở V1 còn 48 Chai (bằng 2 Thùng)"),

        ("003", "Lô thuộc công ty của phiếu", "P2",
         "KK1 do nhân viên TPE lập",
         "1. Xem tồn H1 tại kho LN theo công ty trên " + BC_THE_KHO + ", chọn Tồn theo công ty TPE",
         "",
         "- Phần nhập 3 của P2 nằm ở công ty TPE"),

        ("004", "Lưu nháp không ghi tồn", "P0",
         "Phiếu P1 'Đang tạo' có H1 V1 3",
         "1. Mở cửa sổ chọn lô H1 ở phiếu xuất kho kho LN",
         "",
         "- Không có lô 'NHAPDIEUCHINH-' nào của P1"),

        ("005", "Kế toán duyệt không cộng tồn vật lý lần 2", "P0",
         "P2 đã gửi duyệt, lô H1 V1 đang 3",
         "1. KT 'Lưu và duyệt' phiếu nhập hàng từ P2\n2. Mở lại cửa sổ chọn lô H1",
         "",
         "- Lô 'NHAPDIEUCHINH-' của H1 vẫn 3, không tăng thêm"),

        ("006", "Tồn ở trang kiểm kê sau khi nhập", "P2",
         "P2 đã gửi duyệt",
         "1. Lập phiếu kiểm kê mới cho H1 kho LN\n2. Xem cột SL tồn kho của H1",
         "",
         "- SL tồn kho của H1 đã gồm 3 vừa nhập (10 cũ cộng 3 là 13)"),
    ]),

    ("XI", "Kiểm tra tăng / giảm số liệu trên báo cáo", [
        ("001", "Thẻ kho: cột Nhập tăng khi Gửi duyệt", "P0",
         "Tài khoản TK có 'Thủ kho'. Phiếu P2 từ KK1 đang ở trang lập, chưa gửi",
         "1. Mở " + BC_THE_KHO + ": Hàng hóa H1, Tồn theo công ty TPE, Kho LN, Từ ngày đầu tháng, Đến ngày "
         "hôm nay. Ghi lại tổng Nhập và SL tồn cuối (số nền)\n"
         "2. Gửi duyệt P2 (H1 V1 3 Cái)\n3. Tải lại Thẻ kho với cùng bộ lọc",
         "H1, kho LN",
         "- Có thêm 1 dòng Số chứng từ là số phiếu P2, ngày hôm nay, cột Nhập 3, Lô 'NHAPDIEUCHINH-', Vị trí V1\n"
         "- Tổng Nhập bằng số nền cộng 3, SL tồn cuối bằng số nền cộng 3 (đơn vị Cái)"),

        ("002", "Thẻ kho: hàng quy đổi tăng theo đơn vị cơ bản", "P0",
         "H2 kiểm theo Thùng, 1 Thùng = 24 Chai. P2 có H2 V1 2 Thùng",
         "1. Mở " + BC_THE_KHO + " cho H2 kho LN, ĐVT để Chai, ghi lại tổng Nhập\n2. Gửi duyệt P2\n"
         "3. Tải lại Thẻ kho",
         "H2, 2 Thùng",
         "- Dòng P2 cột Nhập 48\n- Tổng Nhập bằng số nền cộng 48 Chai\n- Đổi ĐVT sang Thùng thì thấy tăng 2"),

        ("003", "Tổng hợp xuất nhập tồn: Nhập trong kỳ tăng", "P0",
         "Tài khoản TK có 'Xem báo cáo tồn kho theo công ty'",
         "1. Mở " + BC_XNT + ": Từ ngày đầu tháng, Đến ngày hôm nay, Loại báo cáo 'Tất cả', Tồn theo công ty "
         "TPE, Kho LN, Hàng hóa H1. Ghi lại Nhập trong kỳ và Tồn cuối kỳ\n"
         "2. Gửi duyệt P2 (H1 3 Cái)\n3. Bấm tìm lại",
         "H1, kho LN",
         "- Nhập trong kỳ bằng số nền cộng 3\n- Tồn cuối kỳ bằng số nền cộng 3\n- Tồn đầu kỳ, Xuất trong kỳ "
         "không đổi (đơn vị cơ bản)"),

        ("004", "Tổng hợp xuất nhập tồn: hàng quy đổi", "P1",
         "Như TC trên, hàng H2",
         "1. Ghi lại Nhập trong kỳ của H2 kho LN\n2. Gửi duyệt P2 (H2 2 Thùng)\n3. Bấm tìm lại",
         "H2",
         "- Nhập trong kỳ của H2 tăng 48 theo đơn vị cơ bản Chai"),

        ("005", "Báo cáo tồn theo kho: SL tồn tăng", "P0",
         "Tài khoản TK có 'Xem báo cáo tồn kho theo công ty'",
         "1. Mở " + BC_TON_KHO + ": Tính ngày hôm nay, Tồn theo công ty TPE, Kho LN, Hàng hóa H1. Ghi lại SL "
         "tồn\n2. Gửi duyệt P2 (H1 3 Cái)\n3. Bấm tìm lại",
         "H1, kho LN",
         "- SL tồn H1 bằng số nền cộng 3 Cái"),

        ("006", "Báo cáo tồn theo kho: hàng quy đổi", "P0",
         "H2 kiểm theo Thùng hệ số 24",
         "1. Mở " + BC_TON_KHO + " cho H2 kho LN, ghi lại SL tồn (đơn vị Chai)\n2. Gửi duyệt P2 (H2 2 Thùng)\n"
         "3. Bấm tìm lại",
         "H2, 2 Thùng",
         "- SL tồn H2 bằng số nền cộng 48 Chai\n"
         "- Lỗi ERP đã biết: chỉ cộng 2, lệch với Thẻ kho và Tổng hợp xuất nhập tồn"),

        ("007", "Lưu nháp không làm đổi số", "P0",
         "Đã ghi số nền của H1 trên Thẻ kho, Tổng hợp xuất nhập tồn, Báo cáo tồn theo kho",
         "1. Lập phiếu từ phiếu kiểm kê có H1 thừa 3, bấm 'Lưu'\n2. Tải lại cả 3 báo cáo",
         "",
         "- Cả 3 báo cáo giữ nguyên số nền\n- Thẻ kho không có dòng của phiếu nháp"),

        ("008", "Gửi duyệt từ trang Sửa mới làm tăng số", "P1",
         "Phiếu P1 'Đang tạo' có H1 V1 3. Đã ghi số nền trên Thẻ kho",
         "1. Sửa Ghi chú, bấm 'Lưu', tải lại Thẻ kho\n2. Mở Sửa P1, bấm 'Gửi duyệt', tải lại Thẻ kho",
         "",
         "- Bước 1: không đổi\n- Bước 2: Nhập bằng số nền cộng 3"),

        ("009", "Ngày ghi số là ngày Gửi duyệt", "P1",
         "KK1 kiểm ngày tháng trước, P2 gửi duyệt hôm nay",
         "1. Mở " + BC_XNT + " lọc Từ ngày, Đến ngày là tháng trước\n2. Lọc tháng này",
         "",
         "- Bước 1: Nhập trong kỳ không có 3 của P2\n- Bước 2: Nhập trong kỳ có 3 của P2"),

        ("010", "Tổng hợp xuất nhập tồn kế toán không đổi khi Gửi duyệt", "P0",
         "Tài khoản KT có 'Xem báo cáo tồn kho kế toán theo công ty'",
         "1. Mở " + BC_XNT_KT + ": Từ ngày đầu tháng, Đến ngày hôm nay, Tồn theo công ty TPE, Kho LN, H1. Ghi "
         "lại SL Nhập trong kỳ\n2. TK gửi duyệt P2\n3. Bấm tìm lại",
         "H1",
         "- SL Nhập trong kỳ giữ nguyên (thủ kho gửi duyệt chưa ghi kế toán)"),

        ("011", "Tổng hợp xuất nhập tồn kế toán tăng khi kế toán Lưu và duyệt", "P1",
         "P2 'Chờ duyệt', đã ghi số nền ở báo cáo kế toán",
         "1. KT lập phiếu nhập hàng từ P2, bấm 'Lưu', tìm lại báo cáo\n2. Bấm 'Lưu và duyệt' (hoặc mở phiếu "
         "nháp duyệt tiếp), tìm lại báo cáo",
         "H1 3 Cái, H2 2 Thùng",
         "- Bước 1: không đổi\n- Bước 2: SL Nhập trong kỳ H1 cộng 3, H2 cộng 48"),

        ("012", "Kế toán duyệt không làm tăng thêm báo cáo kho", "P0",
         "P2 đã gửi duyệt, đã ghi số sau khi gửi trên Thẻ kho và " + BC_XNT,
         "1. KT 'Lưu và duyệt' phiếu nhập hàng từ P2\n2. Tải lại 2 báo cáo",
         "",
         "- Cả 2 báo cáo giữ nguyên, không bị cộng lần 2"),

        ("013", "Không có chiều ngược trên màn", "P1",
         "P2 đã gửi duyệt, số trên báo cáo đã tăng 3",
         "1. Tìm cách xóa, hủy hoặc không duyệt P2 trên danh sách, trang xem, danh sách chờ duyệt",
         "",
         "- Ghi nhận hành vi ERP: không có thao tác nào, số trên báo cáo không giảm lại\n"
         "- Muốn trả số phải lập phiếu xuất ở màn khác"),

        ("014", "Hàng không vào phiếu thì không đổi số", "P1",
         "KK1 có H3 thừa 4 ở V1, thiếu 4 ở V2. Đã ghi số nền H3 trên " + BC_XNT,
         "1. Gửi duyệt P2 từ KK1\n2. Tìm lại H3",
         "H3",
         "- Nhập trong kỳ của H3 không đổi"),

        ("015", "Hai tab lập trùng làm số tăng gấp đôi", "P2",
         "Đã ghi số nền H1 trên Thẻ kho",
         "1. Làm TC VI.007 (2 tab cùng gửi duyệt)\n2. Tải lại Thẻ kho",
         "",
         "- Nhập chỉ tăng 3\n- Lỗi ERP đã biết: có 2 dòng chứng từ, Nhập tăng 6"),
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
