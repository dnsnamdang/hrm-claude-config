# -*- coding: utf-8 -*-
"""Generate testcase Excel cho man ERP: Phieu nhap kho cho bao thua, thieu.

Viet cho MAN ERP GOC (TanPhatDev, route warehouseImport.discrepancy), de tester nam luong ERP
tren dev-erp. Man nay chi la DANH SACH CHO: khong ghi ton, khong hach toan; loi sang lap
"Phieu bao hang thua, thieu nhap kho" (man khac).

Chay:  PYTHONIOENCODING=utf-8 python gen_testcase.py
Output: testcase - Phieu nhap kho cho bao thua thieu.xlsx (cung thu muc)
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

OUTPUT_FILE = os.path.join(HERE, "testcase - Phieu nhap kho cho bao thua thieu.xlsx")
FEATURE_NAME = "Phiếu nhập kho chờ báo thừa, thiếu (ERP)"
MODULE_NAME = "Kho - Nhập kho"

MENU = "menu Kho > Nhập kho > 'Phiếu nhập kho chờ báo thừa, thiếu'"
MENU_PNK = "menu Kho > Nhập kho > 'Phiếu nhập kho'"
MENU_DNNK = "menu Kho > Nhập kho > 'Phiếu đề nghị nhập kho'"
MENU_PBAO = "menu Kho > Nhập kho > 'Phiếu báo hàng thừa, thiếu nhập kho'"
MENU_PNH = "menu Kế toán > Hàng hoá - Dịch vụ - Vận chuyển > Nhập hàng > 'Phiếu nhập hàng'"
MENU_YCNH = "menu Kế toán > Hàng hoá - Dịch vụ - Vận chuyển > Nhập hàng > 'Yêu cầu nhập hàng'"
MENU_BC_KHO = "menu Kho > Báo cáo kho > 'Báo cáo tồn theo kho'"

# =========================================================================
# 9 MUC MO TA
# =========================================================================
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Danh sách các PHIẾU NHẬP KHO hàng mua đã hạch toán xong nhưng có hàng nhập lệch số (SL thực nhập khác "
     "SL đề nghị nhập) và CHƯA được lập phiếu báo hàng thừa, thiếu. Thủ kho dùng màn này để biết phiếu nào "
     "còn phải báo thừa thiếu với nhà cung cấp.\n"
     "Đường vào: " + MENU + ". Tiêu đề trang: 'DANH SÁCH PHIẾU NHẬP KHO CHỜ BÁO THỪA, THIẾU'.\n"
     "Màn chỉ xem: không tạo, không sửa, không xóa phiếu nhập kho. Có nút Bộ lọc, In, Xuất excel và ở mỗi "
     "dòng có nút bánh răng chứa lựa chọn 'Báo hàng thừa thiếu' để sang trang lập Phiếu báo hàng thừa, thiếu "
     "nhập kho.\n"
     "Màn này KHÔNG làm thay đổi tồn kho hay số liệu kế toán. Tồn kho vật lý đã tăng theo SL thực nhập từ lúc "
     "phiếu nhập kho được gửi."),

    ("2. Đối tượng được tính / hiển thị",
     "Một phiếu nhập kho hiện trên danh sách khi đủ CẢ 4 điều kiện:\n"
     "- Trạng thái phiếu nhập kho là 'Đã hạch toán' (kế toán kho đã lập Phiếu nhập hàng và bấm 'Lưu & Duyệt').\n"
     "- Loại phiếu là loại nhập mua: Nhập hàng mua nước ngoài, Nhập hàng mua ngoài, Nhập hàng mua nước "
     "ngoài (mới), Nhập hàng mua trong nước, Nhập hàng mua trong nước (HĐNT), Nhập hàng mua trong nước "
     "(TỰ DO + HÃNG).\n"
     "- Có ít nhất một dòng hàng mà SL đề nghị nhập khác SL thực nhập (thiếu hoặc thừa đều tính).\n"
     "- Chưa có Phiếu báo hàng thừa, thiếu nhập kho nào gắn với phiếu đó, ở bất kỳ trạng thái nào.\n"
     "Mỗi dòng là một phiếu nhập kho. Mặc định phiếu lập mới nhất lên đầu."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu nhập kho chưa hạch toán (Đang tạo, Chờ duyệt, Đang hạch toán, Không duyệt...).\n"
     "- Phiếu nhập kho loại không phải nhập mua: hàng bán trả lại, hàng mượn trả lại, điều chuyển, nhập ghép, "
     "nhập tách, nhập hàng gửi, nhập hàng khác...\n"
     "- Phiếu mà mọi dòng có SL thực nhập bằng SL đề nghị.\n"
     "- Phiếu đã có phiếu báo thừa thiếu (kể cả phiếu báo mới 'Lưu' ở trạng thái Đang tạo, hoặc đã 'Không "
     "duyệt'). Chỉ khi XÓA phiếu báo thì phiếu nhập kho mới quay lại danh sách.\n"
     "- Phiếu ngoài phạm vi xem của người đăng nhập (xem mục 7)."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Ô 'Từ ngày' và 'Đến ngày' lọc theo NGÀY LẬP phiếu nhập kho (cột 'Ngày lập'), tính trọn ngày 'Đến ngày'. "
     "Không lọc theo ngày hạch toán. Để trống thì không giới hạn thời gian."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Danh sách 10 cột: STT, Mã phiếu, Loại, Nhà cung cấp, Ngày lập, Phiếu ĐNNK, Người đề nghị, Người yêu cầu, "
     "Người lập, Hành động.\n"
     "- Mã phiếu là đường dẫn mở phiếu nhập kho. Phiếu nhập lại có thêm dòng chữ nghiêng 'Nhập lại cho phiếu' "
     "kèm mã phiếu gốc.\n"
     "- Phiếu ĐNNK là đường dẫn mở phiếu đề nghị nhập kho.\n"
     "- Người đề nghị: mã phòng ban kèm tên người lập phiếu đề nghị nhập kho. Người yêu cầu: mã phòng ban kèm "
     "tên người lập Yêu cầu nhập hàng.\n"
     "Bộ lọc: Công ty, Phòng ban (tùy quyền), Từ ngày, Đến ngày, Kho hàng, Tên mã hàng hóa, Mã phiếu, Loại, "
     "Nhà cung cấp, Phiếu ĐNNK, Người đề nghị."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Một phiếu nhập kho chỉ ra MỘT dòng dù có nhiều dòng hàng lệch.\n"
     "- Mỗi phiếu nhập kho chỉ được lập MỘT phiếu báo thừa thiếu. Lập xong (kể cả chỉ bấm 'Lưu') phiếu biến "
     "khỏi danh sách và khỏi cửa sổ chọn phiếu ở trang lập phiếu báo.\n"
     "- So sánh SL đề nghị và SL thực nhập của ERP làm tròn về số nguyên trước khi so (xem lỗi (1))."),

    ("7. Phân quyền cấp",
     "- Vào màn: KHÔNG cần quyền riêng, mọi tài khoản đăng nhập đều mở được từ menu.\n"
     "- Phạm vi xem: 'Xem xử lý thừa thiếu nhập kho theo tổng công ty' thấy mọi công ty; 'Xem xử lý thừa "
     "thiếu nhập kho theo công ty' chỉ thấy phiếu của công ty mình; không có 2 quyền này thì chỉ thấy phiếu "
     "nhập kho do CHÍNH MÌNH lập.\n"
     "- Lựa chọn 'Báo hàng thừa thiếu' chỉ hiện với người có quyền 'Tạo phiếu báo hàng thừa, thiếu nhập kho' "
     "hoặc 'Thủ kho'.\n"
     "- Ô lọc Kho hàng: có quyền xem theo tổng công ty thì liệt kê mọi kho đang hoạt động, không thì chỉ kho "
     "của người đăng nhập.\n"
     "- Ô lọc Công ty chỉ hiện với quyền 'Xem tất cả phiếu'; ô Phòng ban hiện với 'Xem tất cả phiếu', 'Xem "
     "tất cả phiếu của công ty' hoặc 'Xem tất cả phiếu của phòng ban'."),

    ("8. Cách tính các ô thống kê",
     "Màn không có ô tổng. Bản In và file Xuất excel lấy TOÀN BỘ phiếu khớp bộ lọc đang chọn (không theo phân "
     "trang), 9 cột: STT, Mã phiếu, Loại, Nhà cung cấp, Ngày lập, Phiếu ĐNNK, Người đề nghị, Người yêu cầu, "
     "Người lập. File excel tên 'danh_sach_phieu_nhap_kho_cho_bao_thua_thieu.xlsx', tiêu đề 'DANH SÁCH PHIẾU "
     "NHẬP KHO CHỜ BÁO THỪA THIẾU'."),

    ("9. Ghi chú đọc bảng",
     "Các lỗi ERP ĐÃ BIẾT được viết thành testcase với kết quả mong đợi ĐÚNG, kèm dòng 'Lỗi ERP đã biết'. "
     "Chạy thấy đúng hiện tượng lỗi thì ghi Failed và chép câu đó vào cột Ghi chú:\n"
     "(1) Dòng hàng lệch phần lẻ dưới nửa đơn vị (vd đề nghị 10, thực nhập 9.6) KHÔNG lên danh sách, vì hệ "
     "thống làm tròn cả hai số rồi mới so.\n"
     "(2) Người chỉ có quyền 'Xem tất cả phiếu của phòng ban' thấy ô lọc 'Bộ phận' nhưng chọn Bộ phận không "
     "lọc được gì.\n"
     "(3) Người thiếu quyền 'Tạo phiếu báo hàng thừa, thiếu nhập kho' và 'Thủ kho' không thấy lựa chọn ở bánh "
     "răng, nhưng gọi thẳng chức năng lưu phiếu báo vẫn lưu được.\n"
     "(4) Gọi thẳng chức năng lưu phiếu báo lần hai cho cùng một phiếu nhập kho: hệ thống không chặn, sinh "
     "phiếu báo trùng.\n"
     "Ghi nhận hành vi ERP (không phải lỗi): ô lọc 'Tên, mã hàng hóa' tìm theo hàng trên PHIẾU ĐỀ NGHỊ NHẬP "
     "KHO; phiếu báo 'Không duyệt' vẫn giữ phiếu nhập kho ngoài danh sách.\n"
     "Nhóm 'Gọi thẳng chức năng' dành cho tester kỹ thuật, dùng công cụ kiểm thử API, bỏ qua giao diện.\n"
     "Dữ liệu mẫu dùng trong bộ TC: công ty TPE; kho LN, vị trí V1 thuộc kho LN; nhà cung cấp NCC1; hàng H1 "
     "(Cái), H2 (Cái).\n"
     "- P1: phiếu nhập kho loại 'Nhập hàng mua trong nước (TỰ DO + HÃNG)', kho LN, H1 đề nghị 10, thực nhập 8 "
     "(thiếu 2).\n"
     "- P2: cùng loại, H2 đề nghị 5, thực nhập 7 (thừa 2).\n"
     "- P3: cùng loại, H1 đề nghị 10, thực nhập 10 (khớp).\n"
     "- P4: loại 'Nhập hàng bán trả lại', H1 đề nghị 10, thực nhập 8.\n"
     "- P5: loại nhập mua, H1 đề nghị 10, thực nhập 9.6.\n"
     "Tài khoản: A có 'Thủ kho' và 'Xem xử lý thừa thiếu nhập kho theo tổng công ty'; C thuộc TPE, có 'Xem xử "
     "lý thừa thiếu nhập kho theo công ty' và 'Tạo phiếu báo hàng thừa, thiếu nhập kho'; D không có quyền xem "
     "và tạo nào ở trên; K có 'Kế toán kho' của TPE. Câu truy vấn tìm dữ liệu sẵn có nằm trong thư mục sql."),
]

# =========================================================================
# SECTION PHAN QUYEN
# =========================================================================
ROLE_TCS = [
    ("00", "Mở màn từ menu", "P0",
     "Tài khoản A",
     "1. Đăng nhập ERP bằng tài khoản A\n2. Vào " + MENU,
     "Tài khoản: A",
     "- Mở được trang 'DANH SÁCH PHIẾU NHẬP KHO CHỜ BÁO THỪA, THIẾU'\n"
     "- Có nút Bộ lọc, In, Xuất excel và bảng danh sách"),

    ("01", "Không cần quyền riêng vẫn vào được màn", "P1",
     "Tài khoản D không có quyền xem, tạo phiếu báo, không có 'Thủ kho'",
     "1. Đăng nhập D\n2. Vào " + MENU,
     "Tài khoản: D",
     "- Mở được trang, không báo thiếu quyền\n- Bảng chỉ có phiếu nhập kho do D lập, hoặc không có dòng nào"),

    ("02", "Quyền xem theo tổng công ty thấy mọi công ty", "P0",
     "Tài khoản A. Có phiếu chờ báo của ít nhất 2 công ty",
     "1. Đăng nhập A, mở màn\n2. Xem danh sách, không lọc",
     "Tài khoản: A",
     "- Thấy phiếu chờ báo của mọi công ty, không phân biệt người lập"),

    ("03", "Quyền xem theo công ty chỉ thấy công ty mình", "P0",
     "Tài khoản C thuộc TPE. Có phiếu chờ báo của TPE và của công ty khác",
     "1. Đăng nhập C, mở màn\n2. Lọc Mã phiếu của một phiếu chờ báo thuộc công ty khác",
     "Tài khoản: C",
     "- Bước 1: chỉ thấy phiếu của TPE, kể cả phiếu do người khác lập\n- Bước 2: bảng không có dòng nào"),

    ("04", "Không có quyền xem chỉ thấy phiếu mình lập", "P0",
     "Tài khoản D đã lập phiếu nhập kho P1 (đủ điều kiện chờ báo). Có phiếu chờ báo khác do người khác lập "
     "cùng công ty",
     "1. Đăng nhập D, mở màn",
     "Tài khoản: D",
     "- Chỉ thấy P1\n- Không thấy phiếu chờ báo do người khác lập"),

    ("05", "Có quyền tạo phiếu báo thì thấy lựa chọn ở bánh răng", "P0",
     "Tài khoản C có 'Tạo phiếu báo hàng thừa, thiếu nhập kho'. P1 đang trên danh sách",
     "1. Đăng nhập C, mở màn\n2. Bấm nút bánh răng ở dòng P1",
     "Tài khoản: C",
     "- Hiện lựa chọn 'Báo hàng thừa thiếu'"),

    ("06", "Quyền 'Thủ kho' cũng thấy lựa chọn báo thừa thiếu", "P1",
     "Tài khoản A có 'Thủ kho', không có 'Tạo phiếu báo hàng thừa, thiếu nhập kho'",
     "1. Đăng nhập A\n2. Bấm bánh răng ở dòng P1",
     "Tài khoản: A",
     "- Hiện lựa chọn 'Báo hàng thừa thiếu'"),

    ("07", "Thiếu cả 2 quyền thì bánh răng trống", "P0",
     "Tài khoản D, đang thấy P1 do D lập",
     "1. Đăng nhập D\n2. Bấm bánh răng ở dòng P1",
     "Tài khoản: D",
     "- Danh sách thả xuống trống, không có 'Báo hàng thừa thiếu'"),

    ("08", "Ô lọc Công ty và Phòng ban theo quyền", "P1",
     "Tài khoản A có thêm 'Xem tất cả phiếu'. Tài khoản E có 'Xem tất cả phiếu của công ty'. Tài khoản D "
     "không có quyền xem tất cả phiếu nào",
     "1. Lần lượt đăng nhập A, E, D\n2. Mở màn, bấm 'Bộ lọc'",
     "Tài khoản: A, E, D",
     "- A: có ô Công ty và ô Phòng ban\n- E: chỉ có ô Phòng ban, chỉ gồm phòng ban của công ty E\n"
     "- D: không có ô Công ty, không có ô Phòng ban"),

    ("09", "Gọi thẳng chức năng lưu phiếu báo khi thiếu quyền", "P1",
     "Tài khoản D không có 'Tạo phiếu báo hàng thừa, thiếu nhập kho', không có 'Thủ kho'. P1 đang chờ báo. "
     "Tester kỹ thuật có công cụ kiểm thử API",
     "1. Đăng nhập D\n2. Dùng công cụ kiểm thử API gọi thẳng chức năng lưu Phiếu báo hàng thừa, thiếu cho "
     "P1 với đủ Diễn giải, file đính kèm, dòng hàng",
     "Phiếu nhập kho P1",
     "- Hệ thống từ chối, báo không có quyền\n- P1 vẫn còn trên danh sách chờ\n"
     "- Lỗi ERP đã biết: lưu thành công, P1 biến khỏi danh sách"),
]

# =========================================================================
# CAC SECTION CHUC NANG
# =========================================================================
SECTIONS = [
    ("I", "Giao diện danh sách", [
        ("001", "Bố cục màn danh sách", "P0",
         "Tài khoản A. Có sẵn phiếu chờ báo",
         "1. Vào " + MENU + "\n2. Quan sát",
         "",
         "- Tiêu đề 'DANH SÁCH PHIẾU NHẬP KHO CHỜ BÁO THỪA, THIẾU'\n"
         "- Phía trên bảng có nút 'Bộ lọc', 'In', 'Xuất excel'\n"
         "- Không có nút Tạo mới\n"
         "- Bảng có đủ 10 cột: STT, Mã phiếu, Loại, Nhà cung cấp, Ngày lập, Phiếu ĐNNK, Người đề nghị, "
         "Người yêu cầu, Người lập, Hành động"),

        ("002", "Thứ tự mặc định: phiếu lập mới nhất lên đầu", "P1",
         "Có ít nhất 3 phiếu chờ báo lập ở các ngày khác nhau",
         "1. Mở màn\n2. So cột Ngày lập từ trên xuống",
         "",
         "- Ngày lập giảm dần, phiếu lập gần nhất ở dòng 1"),

        ("003", "Dữ liệu từng cột của một dòng", "P0",
         "P1 lập từ phiếu đề nghị nhập kho DN1 (người lập NV1 phòng KD1), DN1 lập từ Yêu cầu nhập hàng YC1 "
         "(người lập NV2 phòng MH). Nhà cung cấp NCC1. Thủ kho A lập P1",
         "1. Lọc Mã phiếu P1\n2. Đọc từng cột",
         "Phiếu nhập kho P1",
         "- Loại 'Nhập hàng mua trong nước (TỰ DO + HÃNG)'\n- Nhà cung cấp NCC1\n- Phiếu ĐNNK là mã DN1\n"
         "- Người đề nghị dạng mã phòng KD1 kèm tên NV1\n- Người yêu cầu dạng mã phòng MH kèm tên NV2\n"
         "- Người lập là tên A"),

        ("004", "Bấm Mã phiếu mở phiếu nhập kho", "P1",
         "P1 trên danh sách",
         "1. Bấm mã P1",
         "",
         "- Mở trang xem phiếu nhập kho P1\n- Trên phiếu thấy dòng H1 có SL đề nghị 10, SL thực nhập 8"),

        ("005", "Bấm Phiếu ĐNNK mở phiếu đề nghị", "P2",
         "P1 trên danh sách",
         "1. Bấm mã ở cột Phiếu ĐNNK",
         "",
         "- Mở trang xem phiếu đề nghị nhập kho DN1"),

        ("006", "Phiếu nhập lại hiện mã phiếu gốc", "P2",
         "Có phiếu nhập lại P6 cho phiếu gốc P0, P6 đủ điều kiện chờ báo",
         "1. Lọc Mã phiếu P6",
         "Phiếu nhập kho P6",
         "- Dưới mã P6 có chữ nghiêng 'Nhập lại cho phiếu' kèm mã P0, bấm được"),

        ("007", "Sắp xếp theo cột", "P2",
         "Có nhiều phiếu chờ báo",
         "1. Bấm tiêu đề cột Ngày lập hai lần\n2. Bấm tiêu đề cột Mã phiếu\n3. Bấm tiêu đề cột Nhà cung cấp\n"
         "4. Bấm tiêu đề cột Phiếu ĐNNK",
         "",
         "- Bước 1: xếp tăng rồi giảm theo Ngày lập\n- Bước 2: xếp theo Mã phiếu\n"
         "- Bước 3: xếp theo Nhà cung cấp, không lỗi trang\n- Bước 4: cột Phiếu ĐNNK không sắp xếp được"),

        ("008", "Phân trang danh sách", "P2",
         "Có hơn 10 phiếu chờ báo",
         "1. Chuyển sang trang 2\n2. Đổi số dòng mỗi trang",
         "",
         "- STT trang 2 nối tiếp trang 1\n- Bảng tải lại đúng số dòng đã chọn"),
    ]),

    ("II", "Điều kiện phiếu vào danh sách", [
        ("001", "Phiếu thiếu hàng đã hạch toán hiện trên danh sách", "P0",
         "P1 đã hạch toán: H1 đề nghị 10, thực nhập 8, chưa có phiếu báo",
         "1. Mở màn, lọc Mã phiếu P1",
         "Phiếu nhập kho P1",
         "- P1 có trên danh sách"),

        ("002", "Phiếu thừa hàng cũng hiện", "P0",
         "P2 đã hạch toán: H2 đề nghị 5, thực nhập 7",
         "1. Lọc Mã phiếu P2",
         "Phiếu nhập kho P2",
         "- P2 có trên danh sách"),

        ("003", "Phiếu nhập đủ số không hiện", "P0",
         "P3 đã hạch toán, mọi dòng SL thực nhập bằng SL đề nghị",
         "1. Lọc Mã phiếu P3",
         "Phiếu nhập kho P3",
         "- Bảng không có dòng nào"),

        ("004", "Phiếu nhiều dòng, chỉ một dòng lệch", "P1",
         "Phiếu P7 có 3 dòng hàng: 2 dòng khớp, 1 dòng đề nghị 4 thực nhập 5",
         "1. Lọc Mã phiếu P7",
         "Phiếu nhập kho P7",
         "- P7 hiện đúng 1 dòng trên danh sách"),

        ("005", "Phiếu chưa hạch toán không hiện", "P0",
         "Phiếu P8 loại nhập mua, có dòng lệch, đang 'Chờ duyệt' (kế toán kho chưa lập Phiếu nhập hàng)",
         "1. Lọc Mã phiếu P8",
         "Phiếu nhập kho P8",
         "- Bảng không có dòng nào"),

        ("006", "Phiếu loại không phải nhập mua không hiện", "P0",
         "P4 loại 'Nhập hàng bán trả lại' đã hạch toán, H1 đề nghị 10 thực nhập 8",
         "1. Lọc Mã phiếu P4",
         "Phiếu nhập kho P4",
         "- Bảng không có dòng nào"),

        ("007", "Phiếu đã có phiếu báo không hiện", "P0",
         "P1 đã được lập phiếu báo thừa thiếu (bất kỳ trạng thái nào)",
         "1. Lọc Mã phiếu P1",
         "Phiếu nhập kho P1",
         "- Bảng không có dòng nào"),

        ("008", "Lệch phần lẻ dưới nửa đơn vị", "P2",
         "P5 đã hạch toán: H1 đề nghị 10, thực nhập 9.6",
         "1. Lọc Mã phiếu P5",
         "Phiếu nhập kho P5",
         "- P5 có trên danh sách vì thiếu 0.4 Cái\n"
         "- Lỗi ERP đã biết: P5 không lên danh sách"),

        ("009", "Lệch phần lẻ từ nửa đơn vị trở lên", "P2",
         "Phiếu P9 đã hạch toán: đề nghị 2.5, thực nhập 0",
         "1. Lọc Mã phiếu P9",
         "Phiếu nhập kho P9",
         "- P9 có trên danh sách"),

        ("010", "Hàng thực nhập 0 (không về)", "P1",
         "Phiếu P10 đã hạch toán: một dòng đề nghị 15, thực nhập 0",
         "1. Lọc Mã phiếu P10",
         "Phiếu nhập kho P10",
         "- P10 có trên danh sách"),
    ]),

    ("III", "Bộ lọc danh sách", [
        ("001", "Lọc Kho hàng", "P0",
         "Có phiếu chờ báo ở kho LN và kho khác",
         "1. Bấm 'Bộ lọc'\n2. Ô Kho hàng chọn LN",
         "Kho LN",
         "- Chỉ còn phiếu nhập vào kho LN"),

        ("002", "Danh sách ô Kho hàng theo quyền", "P1",
         "Tài khoản A có quyền xem theo tổng công ty. Tài khoản C không có, chỉ phụ trách kho LN",
         "1. Đăng nhập A, mở ô Kho hàng\n2. Đăng nhập C, mở ô Kho hàng",
         "Tài khoản: A, C",
         "- A: có mọi kho đang hoạt động\n- C: chỉ có kho của C"),

        ("003", "Lọc Mã phiếu theo một phần mã", "P0",
         "P1 trên danh sách",
         "1. Ô Mã phiếu gõ 4 số cuối của P1",
         "",
         "- Ra các phiếu có mã chứa chuỗi đã gõ, có P1"),

        ("004", "Lọc Tên, mã hàng hóa", "P1",
         "P1 có hàng H1, lập từ phiếu đề nghị DN1 cũng có H1",
         "1. Ô 'Tên, mã hàng hóa' gõ một phần tên H1\n2. Xóa, gõ một phần mã H1",
         "",
         "- Cả 2 lần đều có P1\n"
         "- Ghi nhận hành vi ERP: hệ thống tìm theo hàng trên phiếu đề nghị nhập kho, không theo dòng lệch"),

        ("005", "Lọc Loại", "P1",
         "Có phiếu chờ báo loại 'Nhập hàng mua trong nước (TỰ DO + HÃNG)' và 'Nhập hàng mua nước ngoài(mới)'",
         "1. Ô Loại chọn 'Nhập hàng mua nước ngoài(mới)'\n2. Đổi sang 'Nhập hàng bán trả lại'",
         "",
         "- Bước 1: chỉ còn phiếu có cột Loại đúng loại đã chọn\n"
         "- Bước 2: bảng trống (Ghi nhận hành vi ERP: ô Loại liệt kê cả loại không bao giờ vào danh sách)"),

        ("006", "Lọc Nhà cung cấp", "P1",
         "Có phiếu chờ báo của NCC1 và nhà cung cấp khác",
         "1. Ô Nhà cung cấp chọn NCC1",
         "Nhà cung cấp NCC1",
         "- Chỉ còn phiếu có cột Nhà cung cấp là NCC1"),

        ("007", "Lọc Phiếu ĐNNK", "P1",
         "P1 lập từ phiếu đề nghị DN1",
         "1. Ô Phiếu ĐNNK gõ một phần mã DN1",
         "",
         "- Ra P1 và các phiếu có Phiếu ĐNNK chứa chuỗi đã gõ"),

        ("008", "Lọc Người đề nghị", "P1",
         "NV1 lập phiếu đề nghị DN1 của P1",
         "1. Ô Người đề nghị gõ tên NV1, chọn NV1",
         "Nhân viên NV1",
         "- Chỉ còn phiếu có cột Người đề nghị là NV1"),

        ("009", "Lọc Từ ngày, Đến ngày theo Ngày lập", "P0",
         "P1 lập ngày 05/10/2026, P2 lập ngày 10/10/2026",
         "1. Từ ngày 01/10/2026, Đến ngày 05/10/2026\n2. Đổi Đến ngày thành 10/10/2026",
         "",
         "- Bước 1: có P1, không có P2 (P1 lập trong ngày 05/10 vẫn được tính)\n- Bước 2: có cả P1 và P2"),

        ("010", "Lọc Công ty và Phòng ban", "P1",
         "Tài khoản A có 'Xem tất cả phiếu'. Có phiếu chờ báo của TPE và công ty khác",
         "1. Ô Công ty chọn TPE\n2. Mở ô Phòng ban\n3. Chọn một phòng ban của TPE",
         "Công ty TPE",
         "- Bước 1: chỉ còn phiếu của TPE\n- Bước 2: ô Phòng ban chỉ còn phòng ban của TPE\n"
         "- Bước 3: chỉ còn phiếu của phòng ban đã chọn"),

        ("011", "Lọc Bộ phận với quyền xem phiếu phòng ban", "P2",
         "Tài khoản F chỉ có 'Xem tất cả phiếu của phòng ban' và 'Xem xử lý thừa thiếu nhập kho theo công ty'",
         "1. Đăng nhập F, bấm 'Bộ lọc'\n2. Ô Bộ phận chọn một bộ phận",
         "Tài khoản: F",
         "- Bảng chỉ còn phiếu của bộ phận đã chọn\n"
         "- Lỗi ERP đã biết: bảng không đổi, ô Bộ phận không có tác dụng"),

        ("012", "Kết hợp nhiều điều kiện và bỏ lọc", "P2",
         "Có dữ liệu nhiều kho, nhiều nhà cung cấp",
         "1. Chọn Kho LN\n2. Chọn Nhà cung cấp NCC1\n3. Bỏ hết điều kiện",
         "",
         "- Sau bước 2 chỉ còn phiếu kho LN của NCC1\n- Bước 3 bảng hiện lại đủ theo phạm vi xem"),
    ]),

    ("IV", "Sang lập phiếu báo hàng thừa, thiếu", [
        ("001", "Bấm 'Báo hàng thừa thiếu' mở trang lập phiếu báo", "P0",
         "Tài khoản C, P1 trên danh sách",
         "1. Bấm bánh răng dòng P1\n2. Chọn 'Báo hàng thừa thiếu'",
         "Phiếu nhập kho P1",
         "- Mở trang 'PHIẾU BÁO HÀNG THỪA, THIẾU NHẬP KHO'\n"
         "- Ô Phiếu nhập kho đã điền sẵn mã P1, Nhà cung cấp NCC1, Yêu cầu nhập là mã YC1"),

        ("002", "Trang lập phiếu báo chỉ mang sang dòng lệch", "P0",
         "P7 có 3 dòng hàng, chỉ 1 dòng đề nghị 4 thực nhập 5",
         "1. Bánh răng dòng P7, chọn 'Báo hàng thừa thiếu'\n2. Xem bảng hàng",
         "Phiếu nhập kho P7",
         "- Bảng hàng chỉ có 1 dòng lệch\n- Cột SL đề nghị nhập 4, SL thực nhập 5, SL thừa 1"),

        ("003", "Số thiếu mang sang đúng", "P1",
         "P1: H1 đề nghị 10, thực nhập 8",
         "1. Mở trang lập phiếu báo từ P1",
         "",
         "- Dòng H1: SL đề nghị nhập 10, SL thực nhập 8, SL thiếu 2"),

        ("004", "Lưu phiếu báo thì phiếu nhập kho rời danh sách", "P0",
         "Đang ở trang lập phiếu báo từ P1",
         "1. Nhập Diễn giải, chọn 1 file đính kèm\n2. Bấm 'Lưu'\n3. Mở lại " + MENU + ", lọc P1",
         "Diễn giải: Thiếu 2 Cái H1",
         "- Bước 2 báo 'Phiếu báo hàng thừa thiếu thành công!', chuyển sang danh sách phiếu báo\n"
         "- Bước 3: bảng không có P1"),

        ("005", "Lưu & gửi cũng làm phiếu rời danh sách", "P1",
         "Đang ở trang lập phiếu báo từ P2",
         "1. Nhập Diễn giải, chọn file\n2. Bấm 'Lưu & gửi'\n3. Mở lại màn, lọc P2",
         "",
         "- Bước 2 báo 'Yêu cầu phiếu báo hàng thừa thiếu đã được gửi!'\n- Bước 3: không còn P2"),

        ("006", "Lập phiếu báo thiếu thông tin bắt buộc", "P1",
         "Đang ở trang lập phiếu báo từ P1",
         "1. Để trống Diễn giải, không chọn file\n2. Bấm 'Lưu'\n3. Mở lại màn chờ báo",
         "",
         "- Bước 2 báo 'Phiếu báo hàng thừa thiếu nhập kho thất bại!', lỗi đỏ ở Diễn giải và File đính kèm\n"
         "- Bước 3: P1 vẫn còn trên danh sách"),

        ("007", "Cửa sổ chọn phiếu nhập kho ở trang lập phiếu báo dùng cùng danh sách", "P1",
         "Tài khoản C. P1 đang chờ báo, P3 khớp số, P1 sau đó được lập phiếu báo",
         "1. Vào " + MENU_PBAO + ", bấm Tạo mới\n2. Bấm chọn phiếu nhập kho, xem cửa sổ "
         "'Phiếu nhập kho hàng thừa thiếu'\n3. Lập phiếu báo cho P1, quay lại mở cửa sổ này",
         "",
         "- Bước 2: cửa sổ có đúng các phiếu như màn chờ báo, có P1, không có P3\n"
         "- Bước 3: cửa sổ không còn P1"),

        ("008", "Gọi thẳng chức năng lưu phiếu báo lần hai cho cùng phiếu", "P2",
         "P1 đã có phiếu báo. Tester kỹ thuật có công cụ kiểm thử API",
         "1. Gọi thẳng chức năng lưu phiếu báo cho P1 lần nữa\n2. Mở " + MENU_PBAO + ", lọc theo P1",
         "Phiếu nhập kho P1",
         "- Hệ thống chặn, báo phiếu nhập kho đã được lập phiếu báo\n"
         "- Lỗi ERP đã biết: lưu thành công, P1 có 2 phiếu báo"),
    ]),

    ("V", "In danh sách", [
        ("001", "In theo bộ lọc đang chọn", "P0",
         "Lọc Kho LN, ra 3 phiếu",
         "1. Bấm 'In'",
         "",
         "- Mở tab mới bản in khổ ngang, có tiêu đề danh sách phiếu nhập kho chờ báo thừa thiếu\n"
         "- Bảng 9 cột: STT, Mã phiếu, Loại, Nhà cung cấp, Ngày lập, Phiếu ĐNNK, Người đề nghị, Người yêu cầu, "
         "Người lập\n- Đúng 3 dòng như trên màn"),

        ("002", "Bản in lấy hết, không theo phân trang", "P1",
         "Có 25 phiếu chờ báo, màn đang hiện 10 dòng mỗi trang",
         "1. Bấm 'In'",
         "",
         "- Bản in có đủ 25 dòng"),

        ("003", "Định dạng bản in", "P2",
         "P6 là phiếu nhập lại",
         "1. Lọc P6, bấm 'In'",
         "",
         "- Ngày lập dạng ngày/tháng/năm\n- Dưới mã P6 có 'Nhập lại cho phiếu' kèm mã phiếu gốc"),

        ("004", "Bản in theo phạm vi xem", "P1",
         "Tài khoản C chỉ có quyền xem theo công ty TPE",
         "1. Đăng nhập C, không lọc, bấm 'In'",
         "Tài khoản: C",
         "- Bản in chỉ có phiếu của TPE"),
    ]),

    ("VI", "Xuất Excel", [
        ("001", "Xuất excel theo bộ lọc", "P0",
         "Lọc Nhà cung cấp NCC1, ra 2 phiếu",
         "1. Bấm 'Xuất excel'\n2. Mở file",
         "",
         "- Tải file 'danh_sach_phieu_nhap_kho_cho_bao_thua_thieu.xlsx'\n"
         "- Dòng tiêu đề 'DANH SÁCH PHIẾU NHẬP KHO CHỜ BÁO THỪA THIẾU'\n"
         "- Đủ 9 cột như bản in, đúng 2 dòng"),

        ("002", "File lấy hết, không theo phân trang", "P1",
         "Có 25 phiếu chờ báo, màn hiện 10 dòng mỗi trang",
         "1. Xuất excel",
         "",
         "- File có đủ 25 dòng"),

        ("003", "File theo phạm vi xem", "P1",
         "Tài khoản D chỉ thấy phiếu mình lập",
         "1. Đăng nhập D, bấm 'Xuất excel'",
         "Tài khoản: D",
         "- File chỉ có phiếu do D lập"),

        ("004", "Danh sách trống", "P2",
         "Lọc Mã phiếu không tồn tại",
         "1. Bấm 'Xuất excel'",
         "XYZ-KHONG-CO",
         "- Vẫn tải được file, chỉ có dòng tiêu đề, không lỗi trang"),
    ]),

    ("VII", "Chuẩn bị dữ liệu test", [
        ("001", "Tìm phiếu đang chờ báo có sẵn trên dev", "P0",
         "Tester có quyền đọc dữ liệu dev, có câu truy vấn số 1 trong thư mục sql",
         "1. Chạy câu truy vấn số 1\n2. Lấy mã phiếu nhập kho ở cột đầu, ghi lại kho, công ty, người lập\n"
         "3. Đăng nhập tài khoản A, mở " + MENU + ", lọc theo mã đó",
         "",
         "- Bước 3 thấy đúng phiếu đó\n- Cột chi tiết lệch của câu truy vấn khớp số trên trang lập phiếu báo"),

        ("002", "Tạo Yêu cầu nhập hàng mua trong nước", "P0",
         "Tài khoản kinh doanh hoặc mua hàng của TPE. Hàng H1 đang kinh doanh",
         "1. Vào " + MENU_YCNH + "\n2. Tạo yêu cầu nhập hàng loại mua trong nước, nhà cung cấp NCC1, H1 "
         "số lượng 10, kho nhận LN\n3. Đi hết luồng duyệt của yêu cầu",
         "H1: 10 Cái",
         "- Yêu cầu nhập hàng YC1 được duyệt\n- Sinh phiếu đề nghị nhập kho DN1 cho kho LN, H1 SL 10"),

        ("003", "Thủ kho lập phiếu nhập kho thiếu hàng", "P0",
         "Tài khoản A là thủ kho kho LN. DN1 đã sẵn sàng nhập",
         "1. Vào " + MENU_DNNK + ", bánh răng dòng DN1, chọn 'Tạo phiếu nhập kho'\n"
         "2. Dòng H1: chọn vị trí V1, SL nhập 8\n3. Lưu và gửi phiếu",
         "H1: SL nhập 8",
         "- Phiếu nhập kho P1 có SL đề nghị 10, SL thực nhập 8\n- P1 ở trạng thái 'Chờ duyệt'\n"
         "- P1 CHƯA có trên màn chờ báo"),

        ("004", "Kế toán kho hạch toán phiếu nhập kho", "P0",
         "Tài khoản K có 'Kế toán kho' của TPE. P1 đang 'Chờ duyệt'",
         "1. Vào " + MENU_PNK + ", bánh răng dòng P1, chọn 'Tạo phiếu nhập hàng'\n"
         "2. Hoàn tất phân bổ, bấm 'Lưu & Duyệt'\n3. Xem trạng thái P1",
         "",
         "- P1 chuyển 'Đã hạch toán'\n- P1 xuất hiện trên " + MENU),

        ("005", "Tạo phiếu thừa hàng và phiếu khớp số để đối chứng", "P1",
         "Như các TC trên",
         "1. Lặp lại luồng với H2 đề nghị 5, ở phiếu nhập kho nhập SL 7, ra P2\n"
         "2. Lặp lại luồng với H1 đề nghị 10, nhập đủ 10, ra P3\n3. Hạch toán cả P2, P3",
         "",
         "- P2 có trên màn chờ báo\n- P3 không có trên màn chờ báo"),

        ("006", "Lấy lại phiếu đã báo để test lần nữa", "P2",
         "P1 đã có phiếu báo ở trạng thái 'Đang tạo', do chính tài khoản C lập",
         "1. Vào " + MENU_PBAO + "\n2. Xóa phiếu báo của P1\n3. Mở lại màn chờ báo",
         "",
         "- Bước 2 báo 'Xóa yêu cầu thành công!'\n- P1 quay lại danh sách chờ, dùng tiếp được"),
    ]),

    ("VIII", "Kiểm tra tăng / giảm số liệu trên báo cáo", [
        ("001", "Danh sách chờ tăng 1 khi phiếu nhập kho lệch được hạch toán", "P0",
         "P1 đang 'Chờ duyệt' (thiếu 2 H1). Tài khoản A và K",
         "1. Đăng nhập A, mở " + MENU + ", lọc Kho LN, ghi lại tổng số bản ghi ở chân bảng là N\n"
         "2. Đăng nhập K, tạo Phiếu nhập hàng cho P1 và bấm 'Lưu & Duyệt'\n"
         "3. Đăng nhập A, mở lại màn, lọc Kho LN",
         "",
         "- Tổng số bản ghi bằng N + 1\n- P1 ở dòng đầu nếu là phiếu lập mới nhất"),

        ("002", "Phiếu nhập hàng mới 'Lưu' thì danh sách không đổi", "P0",
         "P8 đang 'Chờ duyệt', có dòng lệch",
         "1. Ghi tổng số bản ghi màn chờ báo, lọc Kho LN, là N\n"
         "2. K tạo Phiếu nhập hàng cho P8, chỉ bấm 'Lưu'\n3. Mở lại màn",
         "",
         "- Tổng số bản ghi vẫn là N, không có P8"),

        ("003", "Phiếu khớp số hoặc phiếu không phải nhập mua hạch toán thì danh sách không đổi", "P1",
         "P3 (khớp số) và P4 (Nhập hàng bán trả lại, có lệch) đang chờ hạch toán",
         "1. Ghi tổng số bản ghi màn chờ báo là N\n2. Hạch toán P3 và P4\n3. Mở lại màn",
         "",
         "- Tổng số bản ghi vẫn là N"),

        ("004", "Danh sách chờ giảm 1 khi lập phiếu báo", "P0",
         "P1 và P2 đang chờ báo",
         "1. Ghi tổng số bản ghi màn chờ báo là N\n2. Từ dòng P1 chọn 'Báo hàng thừa thiếu', nhập đủ, bấm "
         "'Lưu'\n3. Mở lại màn",
         "",
         "- Tổng số bản ghi giảm còn N trừ 1\n- Không còn P1, P2 vẫn còn"),

        ("005", "Xóa phiếu báo thì danh sách tăng lại 1", "P0",
         "Vừa lập phiếu báo cho P1 ở trạng thái 'Đang tạo', màn chờ báo đang có N bản ghi",
         "1. Vào " + MENU_PBAO + ", xóa phiếu báo của P1\n2. Mở lại màn chờ báo",
         "",
         "- Tổng số bản ghi bằng N + 1, P1 quay lại"),

        ("006", "Phiếu báo bị 'Không duyệt' không trả phiếu về danh sách", "P1",
         "P2 có phiếu báo đã gửi. Người có quyền 'Duyệt phiếu báo hàng thừa, thiếu nhập kho' bấm không duyệt",
         "1. Ghi tổng số bản ghi màn chờ báo là N\n2. Không duyệt phiếu báo của P2\n3. Mở lại màn",
         "",
         "- Tổng số bản ghi vẫn là N, P2 không quay lại\n"
         "- Ghi nhận hành vi ERP: muốn báo lại phải sửa hoặc xóa phiếu báo bị không duyệt"),

        ("007", "Tồn kho tăng theo SL thực nhập, không theo SL đề nghị", "P1",
         "Tài khoản có quyền 'Xem báo cáo tồn kho theo công ty'. H1 chưa có phiếu nhập P1",
         "1. Mở " + MENU_BC_KHO + ", Tính ngày hôm nay, Kho LN, Hàng hóa H1, bấm Lọc, ghi SL tồn là T\n"
         "2. Thủ kho lập và gửi phiếu nhập kho P1 (đề nghị 10, nhập 8)\n3. Lọc lại báo cáo như bước 1",
         "",
         "- SL tồn H1 kho LN bằng T + 8, không phải T + 10\n- Phần thiếu 2 chỉ được ghi nhận ở màn chờ báo"),

        ("008", "Lập phiếu báo không làm đổi báo cáo tồn kho", "P0",
         "P1 đang chờ báo, đã gửi từ trước",
         "1. Mở " + MENU_BC_KHO + ", Kho LN, Hàng hóa H1, bấm Lọc, ghi SL tồn là T\n"
         "2. Lập phiếu báo cho P1, bấm 'Lưu & gửi'\n3. Lọc lại báo cáo",
         "",
         "- SL tồn H1 kho LN vẫn là T, không tăng không giảm\n"
         "- Màn chờ báo và phiếu báo KHÔNG làm thay đổi tồn kho"),

        ("009", "Hạch toán phiếu nhập hàng không làm đổi tồn kho vật lý", "P1",
         "P1 đã gửi (Chờ duyệt), báo cáo tồn kho đã có SL tồn H1 kho LN là T",
         "1. K lập Phiếu nhập hàng cho P1, bấm 'Lưu & Duyệt'\n2. Lọc lại " + MENU_BC_KHO + " cho H1 kho LN",
         "",
         "- SL tồn vẫn là T\n- Chỉ màn chờ báo thay đổi (thêm P1)"),

        ("010", "Xóa phiếu báo không làm đổi báo cáo tồn kho", "P2",
         "P1 có phiếu báo 'Đang tạo', SL tồn H1 kho LN trên báo cáo là T",
         "1. Xóa phiếu báo của P1\n2. Lọc lại " + MENU_BC_KHO,
         "",
         "- SL tồn vẫn là T"),
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
