# -*- coding: utf-8 -*-
"""Generate testcase Excel cho man ERP: Phieu bao hang thua, thieu nhap kho.

Viet cho MAN ERP GOC (TanPhatDev, nhom duong dan excShortage cua phieu nhap kho), de tester
nam luong ERP tren dev-erp truoc khi port sang HRM.

Chay:  PYTHONIOENCODING=utf-8 python gen_testcase.py
Output: testcase - Phieu bao hang thua thieu nhap kho.xlsx (cung thu muc)
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

OUTPUT_FILE = os.path.join(HERE, "testcase - Phieu bao hang thua thieu nhap kho.xlsx")
FEATURE_NAME = "Phiếu báo hàng thừa, thiếu nhập kho (ERP)"
MODULE_NAME = "Kho - Nhập kho"

MENU = "menu Kho > Nhập kho > 'Phiếu báo hàng thừa, thiếu nhập kho'"
MENU2 = "menu Mua hàng > Xử lý hàng thừa - thiếu > 'Phiếu báo hàng thừa thiếu nhập kho'"
MENU_NGUON = "menu Kho > Nhập kho > 'Phiếu nhập kho chờ báo thừa, thiếu'"
MENU_XL = "menu Mua hàng > Xử lý hàng thừa - thiếu > 'Phiếu xử lý hàng thiếu nhập kho'"
MENU_TRA = "menu Mua hàng > Xử lý hàng thừa - thiếu > 'Tình trạng trả hàng thiếu nhập kho'"
MENU_PNK = "menu Kho > Nhập kho > 'Phiếu nhập kho'"
BC_TON = "menu Kho > Báo cáo kho > 'Báo cáo tồn kho tổng hợp theo mặt hàng'"
BC_THE = "menu Kho > Báo cáo kho > 'Thẻ kho'"
O_DUYET = "ô 'Phiếu báo thừa - thiếu nhập kho cần xử lý' ở tab 'Phê duyệt' của trang chủ"

# =========================================================================
# 9 MUC MO TA
# =========================================================================
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Ghi nhận chênh lệch giữa SỐ LƯỢNG ĐỀ NGHỊ NHẬP và SỐ LƯỢNG THỰC NHẬP của một phiếu nhập kho mua hàng, "
     "kèm diễn giải và file biên bản, để bộ phận mua hàng xử lý tiếp với nhà cung cấp (đòi tiền, đòi hàng).\n"
     "Đường vào: " + MENU + ", hoặc " + MENU2 + ". Tiêu đề trang: 'DANH SÁCH PHIẾU BÁO HÀNG THỪA, THIẾU NHẬP KHO'.\n"
     "Lối vào thứ 3: ở " + MENU_NGUON + ", nút bánh răng của phiếu > 'Báo hàng thừa thiếu' (mở sẵn trang Tạo "
     "mới đã chọn phiếu nhập kho đó).\n"
     "Luồng: Tạo phiếu (Đang tạo) > 'Lưu & gửi' (Chờ xử lý) > người duyệt bấm 'Xử lý' để lập Phiếu xử lý hàng "
     "thiếu nhập kho (phiếu báo thành Đã xử lý), hoặc bấm 'Không duyệt' (phiếu báo thành Không duyệt, người lập "
     "sửa và gửi lại).\n"
     "PHIẾU BÁO KHÔNG GHI TỒN KHO: tồn kho đã được ghi theo SL thực nhập ngay từ phiếu nhập kho. Phiếu báo và "
     "phiếu xử lý hàng thiếu đều không cộng / trừ tồn."),

    ("2. Đối tượng được tính / hiển thị",
     "Phiếu nhập kho chọn được để lập phiếu báo phải đủ cả các điều kiện:\n"
     "- Trạng thái 'Đã hạch toán'.\n"
     "- Loại nhập là một trong: Nhập hàng mua nước ngoài, Nhập hàng mua ngoài, Nhập hàng mua nước ngoài (mới), "
     "Nhập hàng mua trong nước, Nhập hàng mua trong nước (HĐNT), Nhập hàng mua trong nước (TỰ DO + HÃNG).\n"
     "- Có ít nhất 1 dòng hàng mà SL đề nghị nhập khác SL thực nhập (so phần nguyên, làm tròn).\n"
     "- Chưa có phiếu báo nào gắn với phiếu nhập kho đó (kể cả phiếu Đang tạo hoặc Không duyệt).\n"
     "- Nằm trong phạm vi xem của người lập (xem mục 7).\n"
     "Bảng 'Chi tiết' của phiếu báo chỉ hiện các dòng hàng bị lệch, dòng khớp số không hiện.\n"
     "Danh sách phiếu báo: mỗi dòng là một phiếu báo, phiếu lập mới nhất lên đầu."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu nhập kho chưa hạch toán, đã hủy, loại nhập điều chuyển / trả lại / nhập ghép... không hiện ở cửa sổ "
     "chọn phiếu nhập kho.\n"
     "- Dòng lệch chỉ ở phần thập phân (ví dụ đề nghị 2.4, thực nhập 2.2) không được tính là lệch.\n"
     "- Phiếu nhập kho đã có phiếu báo thì biến khỏi màn 'Phiếu nhập kho chờ báo thừa, thiếu' và cửa sổ chọn; "
     "xóa phiếu báo thì phiếu nhập kho hiện lại.\n"
     "- Phiếu báo chỉ có hàng THỪA (không có dòng thiếu) không chọn được ở màn lập Phiếu xử lý hàng thiếu."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Ô 'Từ ngày' và 'Đến ngày' lọc theo cột 'Ngày lập' (ngày giờ tạo phiếu báo), không theo ngày của phiếu nhập "
     "kho. Bảng tự lọc khoảng nửa giây sau khi gõ / chọn, nút kính lúp để lọc lại, nút làm mới để xóa hết điều "
     "kiện."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Danh sách 9 cột: STT, Số phiếu, Ngày lập, Phiếu nhập kho, Yêu cầu nhập, Nhà cung cấp, Số hợp đồng, Trạng "
     "thái, Hành động (nút bánh răng).\n"
     "Ô lọc: Phiếu nhập kho, Số phiếu, Nhà cung cấp, Hợp đồng, Yêu cầu nhập, Tên mã hàng hóa, Trạng thái, Từ ngày, "
     "Đến ngày. Nút trên bảng: Tạo mới, In, Xuất excel.\n"
     "Trang Tạo mới: khung 'Thông tin chung' (Phiếu nhập kho bắt buộc, Yêu cầu nhập, Nhà cung cấp, Số hợp đồng, "
     "Diễn giải bắt buộc, File đính kèm bắt buộc) và khung 'Chi tiết' tab 'Hàng hóa' gồm STT, Tên hàng hóa, Model, "
     "Mã hàng hóa, ĐVT, SL đề nghị nhập, SL thực nhập, SL thiếu, SL thừa. Nút Lưu, Lưu & gửi, Hủy.\n"
     "Số phiếu tự sinh dạng mã công ty của người lập + '_BHNK-' + 5 chữ số.\n"
     "4 trạng thái: Đang tạo, Chờ xử lý, Đã xử lý, Không duyệt."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- SL thiếu = SL đề nghị nhập trừ SL thực nhập, chỉ khi đề nghị lớn hơn; ngược lại ô hiện '-'.\n"
     "- SL thừa = SL thực nhập trừ SL đề nghị nhập, chỉ khi thực nhập lớn hơn; ngược lại ô hiện '-'.\n"
     "- Yêu cầu nhập, Nhà cung cấp, Số hợp đồng, bảng hàng đều lấy tự động từ phiếu nhập kho, không sửa được.\n"
     "- Đơn giá của từng dòng lấy theo giá nhà cung cấp trong yêu cầu nhập hàng, dùng cho phiếu xử lý về sau "
     "(không hiện trên phiếu báo).\n"
     "- Một phiếu nhập kho chỉ được lập một phiếu báo."),

    ("7. Phân quyền cấp",
     "Nhóm quyền 'Xử lý thừa, thiếu nhập kho' (phân hệ Kho):\n"
     "- 'Xem xử lý thừa thiếu nhập kho theo tổng công ty' / 'theo công ty': phạm vi phiếu nhập kho được chọn để "
     "lập phiếu báo. Không có cả 2 quyền thì chỉ chọn được phiếu nhập kho do mình lập.\n"
     "- 'Tạo phiếu báo hàng thừa, thiếu nhập kho' (hoặc 'Thủ kho'): hiện nút 'Báo hàng thừa thiếu' ở màn Phiếu "
     "nhập kho chờ báo thừa, thiếu.\n"
     "- 'Duyệt phiếu báo hàng thừa, thiếu nhập kho': xem chi tiết phiếu của người khác, bấm Xử lý / Không duyệt "
     "khi phiếu Chờ xử lý, nhận thông báo khi có phiếu gửi.\n"
     "- 'Tạo xử lý hàng thiếu nhập kho': mở được trang lập Phiếu xử lý hàng thiếu (sau khi bấm Xử lý).\n"
     "- Sửa / Xóa: chỉ NGƯỜI LẬP, khi phiếu Đang tạo hoặc Không duyệt.\n"
     "Menu và danh sách hiện cho mọi người đăng nhập."),

    ("8. Cách tính các ô thống kê",
     "Danh sách không có ô tổng. Ở trang chủ, tab 'Phê duyệt', người có quyền duyệt thấy ô 'Phiếu báo thừa - "
     "thiếu nhập kho cần xử lý' = số phiếu báo Chờ xử lý của CÔNG TY người đăng nhập; ô chỉ hiện khi số lớn hơn 0, "
     "bấm vào mở danh sách duyệt phiếu báo.\n"
     "In / Xuất excel: lấy đúng các phiếu đang lọc, 8 cột STT, Số phiếu, Ngày lập, Phiếu nhập kho, Yêu cầu nhập, "
     "Nhà cung cấp, Số hợp đồng, Trạng thái."),

    ("9. Ghi chú đọc bảng",
     "Các lỗi ERP ĐÃ BIẾT được viết thành testcase với kết quả mong đợi ĐÚNG, kèm dòng 'Lỗi ERP đã biết'. Chạy "
     "thấy đúng hiện tượng lỗi thì ghi Failed và chép câu đó vào cột Ghi chú:\n"
     "(1) Danh sách hiện phiếu báo của MỌI công ty, mọi người lập, không theo quyền xem.\n"
     "(2) Lọc 'Từ ngày' làm bảng trống hoàn toàn. Lọc 'Đến ngày' bỏ sót phiếu lập trong chính ngày đó.\n"
     "(3) Người không có quyền tạo phiếu báo vẫn bấm 'Tạo mới' và lưu được phiếu.\n"
     "(4) Hai người cùng lập phiếu báo cho một phiếu nhập kho (2 tab) đều lưu được, ra 2 phiếu báo.\n"
     "(5) Sửa phiếu rồi lưu làm mất đơn giá các dòng hàng; phiếu xử lý lập sau đó không có đơn giá, thành tiền.\n"
     "(6) Chức năng duyệt không kiểm quyền duyệt và trạng thái: người lập tự gọi thẳng được Không duyệt / Đã xử lý.\n"
     "(7) Người có quyền duyệt nhưng thiếu quyền 'Tạo xử lý hàng thiếu nhập kho' vẫn thấy nút Xử lý, bấm vào ra "
     "trang không tìm thấy.\n"
     "(8) Danh sách duyệt hiện phiếu Chờ xử lý của mọi công ty, trong khi ô đếm ở trang chủ chỉ đếm công ty mình.\n"
     "(9) Xóa phiếu xử lý hàng thiếu thì phiếu báo vẫn 'Đã xử lý', không lập lại phiếu xử lý được.\n"
     "(10) Thông báo sai chữ: lỗi hệ thống khi lưu báo 'Tạo tổng hợp vận chuyển quốc tế thất bại!'; thông báo "
     "không duyệt ghi 'Phiểu báo...'.\n"
     "(11) Sửa phiếu xóa được hết file đính kèm dù khi tạo bắt buộc có file.\n"
     "Nhóm 'Gọi thẳng chức năng' dành cho tester kỹ thuật, dùng công cụ kiểm thử API, bỏ qua giao diện.\n"
     "Dữ liệu mẫu dùng trong bộ TC: công ty TPE, kho LN. Phiếu nhập kho PNK-A (Đã hạch toán, loại Nhập hàng mua "
     "trong nước) gồm hàng H1 đề nghị 10 Cái thực nhập 6 Cái (thiếu 4), H2 đề nghị 5 Cái thực nhập 7 Cái (thừa 2), "
     "H3 đề nghị 10 thực nhập 10 (khớp). PNK-B chỉ có H2 thừa. PNK-C khớp hết. PNK-D chưa hạch toán có lệch.\n"
     "Tài khoản: A thuộc TPE có 'Thủ kho', 'Tạo phiếu báo hàng thừa, thiếu nhập kho', 'Xem xử lý thừa thiếu nhập "
     "kho theo công ty'. D thuộc TPE có 'Duyệt phiếu báo hàng thừa, thiếu nhập kho' và 'Tạo xử lý hàng thiếu nhập "
     "kho'. G có 'Xem xử lý thừa thiếu nhập kho theo tổng công ty'. B không có quyền nào ở nhóm này. E thuộc công "
     "ty khác.\n"
     "Câu truy vấn tìm phiếu nhập kho thật trên dev nằm ở thư mục sql cạnh file này."),
]

# =========================================================================
# SECTION PHAN QUYEN
# =========================================================================
ROLE_TCS = [
    ("00", "Mở màn từ menu Kho", "P0",
     "Tài khoản A",
     "1. Đăng nhập ERP bằng A\n2. Vào " + MENU,
     "Tài khoản: A",
     "- Mở trang 'DANH SÁCH PHIẾU BÁO HÀNG THỪA, THIẾU NHẬP KHO'\n"
     "- Có nút Tạo mới, In, Xuất excel và bảng danh sách"),

    ("01", "Mở màn từ menu Mua hàng", "P1",
     "Tài khoản A",
     "1. Vào " + MENU2,
     "",
     "- Mở đúng cùng một trang danh sách như từ menu Kho"),

    ("02", "Người không có quyền nào vẫn thấy menu và danh sách", "P1",
     "Tài khoản B không có quyền nào trong nhóm 'Xử lý thừa, thiếu nhập kho'",
     "1. Đăng nhập B\n2. Vào " + MENU,
     "Tài khoản: B",
     "- Ghi nhận hành vi ERP: menu hiện, trang danh sách mở được, không bị chặn"),

    ("03", "Danh sách chỉ hiện phiếu trong phạm vi được xem", "P0",
     "Công ty khác đã có phiếu báo do E lập. Tài khoản A chỉ có quyền xem theo công ty TPE",
     "1. Đăng nhập A, mở màn\n2. Tìm phiếu báo do E lập",
     "Tài khoản: A",
     "- A chỉ thấy phiếu báo của công ty TPE\n"
     "- Lỗi ERP đã biết: A thấy cả phiếu báo của công ty khác, bấm vào Số phiếu thì ra trang không tìm thấy"),

    ("04", "Xem chi tiết phiếu của người khác khi không có quyền duyệt", "P0",
     "Phiếu báo do E lập. Tài khoản A không có quyền 'Duyệt phiếu báo hàng thừa, thiếu nhập kho'",
     "1. Đăng nhập A, mở danh sách\n2. Bấm vào Số phiếu của phiếu do E lập",
     "",
     "- Ra trang không tìm thấy, không xem được nội dung phiếu"),

    ("05", "Người có quyền duyệt xem được phiếu của người khác", "P0",
     "Phiếu báo do A lập. Tài khoản D có quyền duyệt",
     "1. Đăng nhập D\n2. Bấm vào Số phiếu của phiếu do A lập",
     "Tài khoản: D",
     "- Mở trang 'CHI TIẾT PHIẾU BÁO HÀNG THỪA, THIẾU NHẬP KHO' kèm số phiếu"),

    ("06", "Sửa / Xóa chỉ hiện cho người lập", "P0",
     "Phiếu báo Đang tạo do A lập",
     "1. Đăng nhập A, bấm bánh răng dòng phiếu\n2. Đăng nhập D, bấm bánh răng cùng dòng",
     "Tài khoản: A, D",
     "- Bước 1: có 'Sửa phiếu' và 'Xóa'\n- Bước 2: không có 'Sửa phiếu', không có 'Xóa'"),

    ("07", "Nút Xử lý chỉ hiện cho người có quyền duyệt", "P0",
     "Phiếu báo Chờ xử lý do A lập",
     "1. Đăng nhập A, bấm bánh răng dòng phiếu\n2. Đăng nhập D, bấm bánh răng cùng dòng",
     "",
     "- Bước 1: không có lựa chọn nào\n- Bước 2: có lựa chọn 'Xử lý'"),

    ("08", "Phạm vi phiếu nhập kho theo quyền xem theo tổng công ty", "P1",
     "Tài khoản G có quyền xem theo tổng công ty. Có phiếu nhập kho đủ điều kiện của TPE và của công ty khác",
     "1. Đăng nhập G, bấm Tạo mới\n2. Bấm nút dấu cộng ở ô Phiếu nhập kho",
     "Tài khoản: G",
     "- Cửa sổ chọn liệt kê phiếu nhập kho của mọi công ty"),

    ("09", "Phạm vi phiếu nhập kho theo quyền xem theo công ty", "P1",
     "Tài khoản A chỉ có quyền xem theo công ty TPE",
     "1. Đăng nhập A, bấm Tạo mới\n2. Mở cửa sổ chọn phiếu nhập kho",
     "",
     "- Chỉ có phiếu nhập kho của công ty TPE"),

    ("10", "Không có quyền xem nào thì chỉ chọn được phiếu nhập kho mình lập", "P1",
     "Tài khoản B không có quyền xem nào. B đã lập phiếu nhập kho PNK-B đủ điều kiện",
     "1. Đăng nhập B, bấm Tạo mới\n2. Mở cửa sổ chọn phiếu nhập kho",
     "Tài khoản: B",
     "- Chỉ có các phiếu nhập kho do B lập, có PNK-B"),

    ("11", "Người không có quyền tạo phiếu báo bấm Tạo mới", "P0",
     "Tài khoản B không có 'Tạo phiếu báo hàng thừa, thiếu nhập kho' và không có 'Thủ kho'",
     "1. Đăng nhập B, bấm Tạo mới\n2. Chọn PNK-B, nhập Diễn giải, đính kèm file\n3. Bấm Lưu",
     "PNK-B",
     "- Hệ thống chặn, không cho lập phiếu báo khi thiếu quyền tạo\n"
     "- Lỗi ERP đã biết: B lưu được phiếu báo bình thường"),

    ("12", "Nút 'Báo hàng thừa thiếu' ở màn nguồn theo quyền tạo", "P1",
     "PNK-A chưa có phiếu báo. Tài khoản A có quyền tạo phiếu báo. Tài khoản G chỉ có quyền xem theo tổng công ty",
     "1. Đăng nhập A, vào " + MENU_NGUON + ", bấm bánh răng dòng PNK-A\n2. Đăng nhập G, làm lại bước 1",
     "",
     "- Bước 1: có lựa chọn 'Báo hàng thừa thiếu'\n- Bước 2: danh sách thả xuống trống"),
]

# =========================================================================
# CAC SECTION CHUC NANG
# =========================================================================
SECTIONS = [
    ("I", "Chuẩn bị dữ liệu test", [
        ("001", "Tìm phiếu nhập kho có sẵn đủ điều kiện", "P0",
         "Tài khoản A. Có quyền chạy câu truy vấn trên dữ liệu dev, hoặc nhờ người hỗ trợ chạy",
         "1. Chạy câu truy vấn số 1 trong thư mục sql\n2. Ghi lại vài số phiếu nhập kho, cột số dòng thiếu / thừa\n"
         "3. Chạy câu số 2 với một số phiếu để xem từng dòng lệch\n"
         "4. Vào " + MENU_NGUON + ", gõ số phiếu vào ô Mã phiếu",
         "Phiếu nhập kho lấy từ câu truy vấn",
         "- Phiếu nhập kho tìm được hiện ở màn 'Phiếu nhập kho chờ báo thừa, thiếu'\n"
         "- Số dòng lệch khớp với câu truy vấn số 2"),

        ("002", "Tự tạo phiếu nhập kho bị THIẾU hàng", "P0",
         "Có yêu cầu nhập hàng mua trong nước đã duyệt cho hàng H1 số lượng 10 Cái, đã có phiếu đề nghị nhập kho kho LN",
         "1. Vào " + MENU_PNK + ", lập phiếu nhập kho từ phiếu đề nghị đó\n"
         "2. Ở dòng H1 nhập SL thực nhập 6, sắp xếp vị trí, hoàn tất nhập kho\n"
         "3. Kế toán kho hạch toán phiếu nhập kho\n4. Mở " + MENU_NGUON,
         "H1: đề nghị 10, thực nhập 6",
         "- Phiếu nhập kho ở trạng thái 'Đã hạch toán'\n- Phiếu hiện ở màn 'Phiếu nhập kho chờ báo thừa, thiếu'"),

        ("003", "Tự tạo phiếu nhập kho bị THỪA hàng", "P1",
         "Yêu cầu nhập hàng có H2 số lượng 5 Cái",
         "1. Lập phiếu nhập kho, dòng H2 nhập SL thực nhập 7\n2. Hoàn tất nhập kho và hạch toán\n"
         "3. Mở " + MENU_NGUON,
         "H2: đề nghị 5, thực nhập 7",
         "- Phiếu hiện ở màn 'Phiếu nhập kho chờ báo thừa, thiếu' (dùng làm PNK-B)"),

        ("004", "Phiếu nhập kho chưa hạch toán chưa dùng được", "P1",
         "Phiếu nhập kho PNK-D có dòng lệch nhưng chưa được kế toán hạch toán",
         "1. Mở " + MENU_NGUON + ", tìm PNK-D\n2. Ở màn phiếu báo bấm Tạo mới, mở cửa sổ chọn phiếu nhập kho, tìm PNK-D",
         "PNK-D",
         "- Cả 2 nơi đều không có PNK-D\n- Hạch toán xong PNK-D thì mới hiện"),

        ("005", "Phiếu nhập kho khớp số không dùng được", "P2",
         "PNK-C mọi dòng SL thực nhập bằng SL đề nghị",
         "1. Mở cửa sổ chọn phiếu nhập kho ở trang Tạo mới, tìm PNK-C",
         "PNK-C",
         "- Không có PNK-C"),

        ("006", "Chuẩn bị đủ tài khoản test", "P1",
         "Quản trị có quyền phân quyền",
         "1. Gán cho A: 'Thủ kho', 'Tạo phiếu báo hàng thừa, thiếu nhập kho', 'Xem xử lý thừa thiếu nhập kho theo "
         "công ty'\n2. Gán cho D: 'Duyệt phiếu báo hàng thừa, thiếu nhập kho', 'Tạo xử lý hàng thiếu nhập kho'\n"
         "3. Gán cho G: 'Xem xử lý thừa thiếu nhập kho theo tổng công ty'\n4. Để B không có quyền nào trong nhóm",
         "Tài khoản A, D, G, B",
         "- Đăng nhập lại, mỗi tài khoản thấy đúng nút theo mục 7 phần mô tả"),

        ("007", "Chuẩn bị phiếu báo ở đủ 4 trạng thái", "P1",
         "Đã có PNK-A, PNK-B và 2 phiếu nhập kho lệch khác",
         "1. A lập phiếu từ phiếu nhập kho thứ nhất, bấm Lưu (Đang tạo)\n"
         "2. A lập phiếu từ PNK-A, bấm Lưu & gửi (Chờ xử lý)\n"
         "3. A lập phiếu từ phiếu thứ hai, Lưu & gửi, D bấm Không duyệt (Không duyệt)\n"
         "4. A lập phiếu từ PNK-B, Lưu & gửi, D bấm Xử lý và lưu phiếu xử lý (Đã xử lý)",
         "",
         "- Danh sách có đủ 4 trạng thái Đang tạo, Chờ xử lý, Không duyệt, Đã xử lý\n"
         "- Bước 4: PNK-B chỉ có hàng thừa nên không lập được phiếu xử lý, dùng phiếu nhập kho khác có hàng thiếu"),
    ]),

    ("II", "Giao diện danh sách", [
        ("001", "Bố cục danh sách", "P0",
         "Tài khoản A, đã có phiếu báo",
         "1. Vào " + MENU,
         "",
         "- Tiêu đề 'DANH SÁCH PHIẾU BÁO HÀNG THỪA, THIẾU NHẬP KHO'\n"
         "- Có khung lọc, nút kính lúp, nút làm mới, nút Tạo mới, In, Xuất excel\n"
         "- Bảng có 9 cột: STT, Số phiếu, Ngày lập, Phiếu nhập kho, Yêu cầu nhập, Nhà cung cấp, Số hợp đồng, Trạng "
         "thái, Hành động"),

        ("002", "Thứ tự mặc định: phiếu lập mới nhất lên đầu", "P1",
         "A vừa lập một phiếu báo",
         "1. Mở danh sách",
         "",
         "- Dòng đầu tiên là phiếu vừa lập"),

        ("003", "Định dạng các cột", "P1",
         "Phiếu báo lập từ PNK-A",
         "1. Xem dòng phiếu báo",
         "",
         "- Số phiếu dạng 'TPE_BHNK-' và 5 chữ số, là link\n- Ngày lập dạng ngày/tháng/năm giờ:phút\n"
         "- Phiếu nhập kho hiện số PNK-A, là link\n- Yêu cầu nhập, Nhà cung cấp, Số hợp đồng đúng theo PNK-A"),

        ("004", "Link Số phiếu và Phiếu nhập kho", "P1",
         "Tài khoản A là người lập",
         "1. Bấm vào Số phiếu\n2. Quay lại, bấm vào số phiếu nhập kho",
         "",
         "- Bước 1: mở trang chi tiết phiếu báo\n- Bước 2: mở trang chi tiết phiếu nhập kho PNK-A"),

        ("005", "Nhãn trạng thái", "P1",
         "Có phiếu ở đủ 4 trạng thái",
         "1. Xem cột Trạng thái",
         "",
         "- Hiện đúng chữ: Đang tạo, Chờ xử lý, Đã xử lý, Không duyệt\n- 'Đã xử lý' màu xanh, các trạng thái còn lại màu đỏ"),

        ("006", "Nút Hành động theo trạng thái với người lập", "P0",
         "Tài khoản A là người lập, có đủ 4 trạng thái",
         "1. Bấm bánh răng từng dòng",
         "",
         "- Đang tạo và Không duyệt: có 'Sửa phiếu', 'Xóa'\n- Chờ xử lý và Đã xử lý: danh sách thả xuống trống"),

        ("007", "Phân trang", "P2",
         "Có hơn 10 phiếu báo",
         "1. Chuyển trang 2\n2. Đổi số dòng mỗi trang",
         "",
         "- STT trang 2 nối tiếp trang 1\n- Bảng tải lại đúng số dòng đã chọn"),
    ]),

    ("III", "Bộ lọc danh sách", [
        ("001", "Lọc Phiếu nhập kho gõ một phần số phiếu", "P0",
         "Có phiếu báo lập từ PNK-A",
         "1. Ô 'Phiếu nhập kho' gõ một phần số PNK-A\n2. Bấm nút kính lúp",
         "Một phần số PNK-A",
         "- Chỉ còn phiếu báo của PNK-A\n- Bảng tự lọc ngay sau khi gõ, không bắt buộc bấm kính lúp"),

        ("002", "Lọc Số phiếu", "P1",
         "Có phiếu báo số TPE_BHNK-00012",
         "1. Ô 'Số phiếu' gõ đủ TPE_BHNK-00012, bấm kính lúp\n2. Gõ một phần 'BHNK-0001', bấm kính lúp",
         "",
         "- Bước 1: ra đúng phiếu đó\n- Bước 2: Ghi nhận hành vi ERP: ô Số phiếu phải gõ đủ số, gõ một phần bảng trống"),

        ("003", "Lọc Nhà cung cấp", "P1",
         "Có phiếu báo của nhiều nhà cung cấp",
         "1. Ô 'Nhà cung cấp' chọn nhà cung cấp của PNK-A, bấm kính lúp",
         "",
         "- Chỉ còn phiếu báo có cột Nhà cung cấp đúng nhà đã chọn"),

        ("004", "Lọc Hợp đồng và Yêu cầu nhập", "P1",
         "Phiếu báo PNK-A có Số hợp đồng và Yêu cầu nhập",
         "1. Ô 'Hợp đồng' gõ một phần số hợp đồng, bấm kính lúp\n"
         "2. Làm mới, ô 'Yêu cầu nhập' gõ một phần số yêu cầu, bấm kính lúp",
         "",
         "- Cả 2 lần đều ra phiếu báo của PNK-A"),

        ("005", "Lọc Tên, mã hàng hóa", "P0",
         "Phiếu báo PNK-A có dòng H1",
         "1. Ô 'Tên, mã hàng hóa' gõ một phần tên H1, bấm kính lúp\n2. Gõ một phần mã H1, bấm kính lúp",
         "",
         "- Cả 2 lần đều ra phiếu báo có hàng H1"),

        ("006", "Lọc Trạng thái", "P0",
         "Có đủ 4 trạng thái",
         "1. Ô 'Trạng thái' chọn 'Chờ xử lý', bấm kính lúp\n2. Lần lượt chọn 3 trạng thái còn lại",
         "",
         "- Mỗi lần chỉ còn phiếu đúng trạng thái đã chọn"),

        ("007", "Lọc Từ ngày", "P0",
         "Có phiếu báo lập hôm nay và phiếu lập tuần trước",
         "1. Ô 'Từ ngày' chọn ngày hôm qua, bấm kính lúp",
         "",
         "- Chỉ còn phiếu lập từ hôm qua đến nay\n- Lỗi ERP đã biết: bảng trống hoàn toàn"),

        ("008", "Lọc Đến ngày gồm cả ngày cuối", "P1",
         "Có phiếu báo lập hôm nay",
         "1. Ô 'Đến ngày' chọn ngày hôm nay, bấm kính lúp",
         "",
         "- Có phiếu lập hôm nay\n- Lỗi ERP đã biết: phiếu lập hôm nay bị loại, chỉ còn phiếu đến hết ngày hôm qua"),

        ("009", "Kết hợp nhiều điều kiện và làm mới", "P1",
         "Có nhiều phiếu báo",
         "1. Chọn Trạng thái 'Đang tạo' và gõ Phiếu nhập kho, bấm kính lúp\n2. Bấm nút làm mới",
         "",
         "- Bước 1: chỉ còn phiếu thỏa cả 2 điều kiện\n- Bước 2: ô lọc trống, bảng hiện lại đầy đủ"),

        ("010", "Không có kết quả phù hợp", "P2",
         "",
         "1. Ô 'Phiếu nhập kho' gõ chuỗi không có thật, bấm kính lúp",
         "XYZ-KHONG-CO",
         "- Bảng báo không có dữ liệu, không lỗi trang"),
    ]),

    ("IV", "Tạo mới: chọn phiếu nhập kho", [
        ("001", "Bố cục trang Tạo mới", "P0",
         "Tài khoản A",
         "1. Ở danh sách bấm 'Tạo mới'",
         "",
         "- Tiêu đề 'PHIẾU BÁO HÀNG THỪA, THIẾU NHẬP KHO'\n"
         "- Khung 'Thông tin chung', góc phải hiện tên A và ngày hôm nay\n"
         "- Ô Phiếu nhập kho ghi 'Chưa chọn phiếu nhập kho' kèm nút dấu cộng\n"
         "- Yêu cầu nhập, Nhà cung cấp, Số hợp đồng bị khóa\n"
         "- Diễn giải và File đính kèm có dấu bắt buộc\n"
         "- Bảng hàng ghi 'Chưa có dữ liệu'\n- Nút Lưu, Lưu & gửi, Hủy"),

        ("002", "Cửa sổ chọn phiếu nhập kho", "P0",
         "Đang ở trang Tạo mới",
         "1. Bấm nút dấu cộng ở ô Phiếu nhập kho",
         "",
         "- Cửa sổ 'Phiếu nhập kho hàng thừa thiếu'\n"
         "- Cột STT, Mã phiếu, Nhà cung cấp, Ngày lập, Phiếu ĐNNK, Người đề nghị, Người yêu cầu, Người lập\n"
         "- Ô tìm 'Tên, mã hàng hóa' và 'Mã phiếu'"),

        ("003", "Chỉ liệt kê phiếu nhập kho đủ điều kiện", "P0",
         "Có PNK-A (đủ điều kiện), PNK-C (khớp), PNK-D (chưa hạch toán), một phiếu nhập điều chuyển có lệch",
         "1. Mở cửa sổ chọn phiếu nhập kho\n2. Tìm lần lượt từng phiếu theo Mã phiếu",
         "",
         "- Chỉ tìm thấy PNK-A\n- Không có PNK-C, PNK-D và phiếu nhập điều chuyển"),

        ("004", "Phiếu nhập kho đã có phiếu báo không hiện lại", "P0",
         "PNK-A đã có phiếu báo (bất kỳ trạng thái nào, kể cả Không duyệt)",
         "1. Mở cửa sổ chọn, tìm PNK-A",
         "PNK-A",
         "- Không có PNK-A"),

        ("005", "Tìm theo tên, mã hàng hóa", "P2",
         "PNK-A có hàng H1",
         "1. Trong cửa sổ, ô 'Tên, mã hàng hóa' gõ mã H1",
         "",
         "- Ra các phiếu nhập kho có H1, có PNK-A"),

        ("006", "Chọn phiếu nhập kho thì điền sẵn thông tin", "P0",
         "Mở cửa sổ chọn",
         "1. Bấm chọn PNK-A",
         "PNK-A",
         "- Cửa sổ đóng, ô Phiếu nhập kho hiện thẻ xanh số PNK-A kèm dấu x\n"
         "- Yêu cầu nhập hiện số yêu cầu nhập hàng của PNK-A, là link\n"
         "- Nhà cung cấp hiện đúng nhà cung cấp của PNK-A\n"
         "- Số hợp đồng hiện số hợp đồng mua (nếu có), là link"),

        ("007", "Bảng chi tiết chỉ có dòng lệch", "P0",
         "Vừa chọn PNK-A",
         "1. Xem tab 'Hàng hóa'",
         "",
         "- Có 2 dòng H1, H2. Không có H3 (khớp số)\n"
         "- Cột đủ: STT, Tên hàng hóa, Model, Mã hàng hóa, ĐVT, SL đề nghị nhập, SL thực nhập, SL thiếu, SL thừa"),

        ("008", "Tính SL thiếu và SL thừa", "P0",
         "Vừa chọn PNK-A",
         "1. Xem dòng H1 và H2",
         "H1: 10 / 6, H2: 5 / 7",
         "- H1: SL thiếu 4, SL thừa '-'\n- H2: SL thiếu '-', SL thừa 2"),

        ("009", "Định dạng số lớn", "P2",
         "Phiếu nhập kho có dòng đề nghị 1,500 thực nhập 1,200",
         "1. Chọn phiếu đó, xem dòng hàng",
         "",
         "- SL đề nghị nhập 1,500, SL thực nhập 1,200, SL thiếu 300 có dấu phẩy ngăn hàng nghìn"),

        ("010", "Bỏ chọn phiếu nhập kho: Xác nhận", "P1",
         "Đã chọn PNK-A, đã gõ Diễn giải",
         "1. Bấm dấu x trên thẻ PNK-A\n2. Ở hộp thoại bấm 'Xác nhận'",
         "",
         "- Hộp thoại 'Nếu bạn hủy phiếu nhập kho này, các thông tin đã nhập sẽ bị hủy!'\n"
         "- Xác nhận xong: ô Phiếu nhập kho về 'Chưa chọn phiếu nhập kho', bảng hàng và Diễn giải trống"),

        ("011", "Bỏ chọn phiếu nhập kho: Hủy", "P2",
         "Đã chọn PNK-A",
         "1. Bấm dấu x trên thẻ PNK-A\n2. Ở hộp thoại bấm 'Hủy'",
         "",
         "- Vẫn giữ PNK-A và bảng hàng"),

        ("012", "Mở Tạo mới từ màn Phiếu nhập kho chờ báo thừa, thiếu", "P0",
         "PNK-A chưa có phiếu báo. Tài khoản A",
         "1. Vào " + MENU_NGUON + "\n2. Bấm bánh răng dòng PNK-A, chọn 'Báo hàng thừa thiếu'",
         "PNK-A",
         "- Mở trang Tạo mới đã chọn sẵn PNK-A, bảng hàng có H1 và H2"),
    ]),

    ("V", "Tạo mới: nhập thông tin và lưu", [
        ("001", "Lưu phiếu ở trạng thái Đang tạo", "P0",
         "Đã chọn PNK-A, Diễn giải 'Thiếu 4 H1, thừa 2 H2', đính kèm 1 file pdf",
         "1. Bấm 'Lưu'",
         "",
         "- Báo 'Phiếu báo hàng thừa thiếu thành công!'\n- Quay về danh sách\n"
         "- Dòng đầu là phiếu mới, Trạng thái 'Đang tạo', Phiếu nhập kho PNK-A"),

        ("002", "Lưu & gửi", "P0",
         "Đã chọn phiếu nhập kho lệch khác, nhập Diễn giải, đính kèm file",
         "1. Bấm 'Lưu & gửi'",
         "",
         "- Báo 'Yêu cầu phiếu báo hàng thừa thiếu đã được gửi!'\n- Phiếu mới có Trạng thái 'Chờ xử lý'"),

        ("003", "Người duyệt nhận thông báo khi gửi", "P1",
         "Tài khoản D có quyền duyệt",
         "1. A lập phiếu và bấm 'Lưu & gửi'\n2. Đăng nhập D, mở chuông thông báo\n3. Bấm vào thông báo",
         "",
         "- Có thông báo 'Bạn có một phiếu báo hàng thừa thiếu cần duyệt từ' kèm tên A\n"
         "- Bấm vào mở trang chi tiết phiếu đó"),

        ("004", "Bấm Lưu không gửi thì không có thông báo", "P2",
         "",
         "1. A lập phiếu, bấm 'Lưu'\n2. Đăng nhập D xem thông báo",
         "",
         "- D không nhận thông báo về phiếu này"),

        ("005", "Chưa chọn phiếu nhập kho", "P0",
         "Vừa mở trang Tạo mới",
         "1. Nhập Diễn giải, đính kèm file\n2. Bấm Lưu",
         "",
         "- Báo 'Phiếu báo hàng thừa thiếu nhập kho thất bại!'\n"
         "- Dưới ô Phiếu nhập kho báo 'Bắt buộc phải nhập'\n- Vẫn ở trang Tạo mới"),

        ("006", "Bỏ trống Diễn giải", "P0",
         "Đã chọn PNK-A, đã đính kèm file",
         "1. Để trống Diễn giải, bấm Lưu",
         "",
         "- Báo 'Phiếu báo hàng thừa thiếu nhập kho thất bại!'\n- Dưới ô Diễn giải báo 'Bắt buộc phải nhập'"),

        ("007", "Diễn giải quá 255 ký tự", "P2",
         "Đã chọn PNK-A, đã đính kèm file",
         "1. Dán vào Diễn giải chuỗi 256 ký tự\n2. Bấm Lưu",
         "Chuỗi 256 ký tự",
         "- Báo lưu thất bại, dưới ô Diễn giải báo lỗi vượt 255 ký tự\n- Chuỗi đúng 255 ký tự thì lưu được"),

        ("008", "Không đính kèm file", "P0",
         "Đã chọn PNK-A, đã nhập Diễn giải",
         "1. Không thêm file nào, bấm Lưu",
         "",
         "- Báo 'Phiếu báo hàng thừa thiếu nhập kho thất bại!'\n- Dưới mục File đính kèm báo 'Bắt buộc phải nhập'"),

        ("009", "Thêm ô file nhưng chưa chọn file", "P2",
         "Đã chọn PNK-A, đã nhập Diễn giải",
         "1. Bấm dấu cộng ở File đính kèm, không chọn file\n2. Bấm Lưu",
         "",
         "- Lưu thất bại, ô file trống bị viền đỏ"),

        ("010", "Đính kèm nhiều file và bỏ một file", "P1",
         "Đã chọn PNK-A, đã nhập Diễn giải",
         "1. Thêm 3 ô file, chọn 3 file pdf, xlsx, png\n2. Bấm dấu x ở file thứ 2\n3. Bấm Lưu\n4. Mở chi tiết phiếu",
         "3 file",
         "- Lưu thành công\n- Trang chi tiết có 2 file pdf và png, bấm vào mở được file"),

        ("011", "File sai định dạng hoặc quá dung lượng", "P1",
         "Đã chọn PNK-A, đã nhập Diễn giải",
         "1. Đính kèm file .txt, bấm Lưu\n2. Bỏ file đó, đính kèm file pdf 20 MB, bấm Lưu",
         "File .txt, file pdf 20 MB",
         "- Cả 2 lần lưu thất bại, ô file bị viền đỏ\n- Hộp chọn file chỉ gợi ý pdf, ảnh, Word, Excel, PowerPoint, zip"),

        ("012", "Hủy không lưu", "P1",
         "Đã chọn PNK-A, đã nhập Diễn giải",
         "1. Bấm 'Hủy'",
         "",
         "- Quay về danh sách, không có phiếu mới\n- PNK-A vẫn còn ở màn 'Phiếu nhập kho chờ báo thừa, thiếu'"),

        ("013", "Bấm Lưu liên tục", "P2",
         "Phiếu hợp lệ",
         "1. Bấm Lưu 3 lần thật nhanh",
         "",
         "- Nút khóa và hiện biểu tượng xoay trong lúc chờ\n- Chỉ sinh đúng 1 phiếu báo"),

        ("014", "Hai người cùng lập phiếu cho một phiếu nhập kho", "P0",
         "Tab 1 và tab 2 cùng đã chọn PNK-A, đủ Diễn giải và file",
         "1. Tab 1 bấm Lưu\n2. Tab 2 bấm Lưu",
         "",
         "- Tab 1 thành công, tab 2 bị chặn vì PNK-A đã có phiếu báo\n"
         "- Lỗi ERP đã biết: tab 2 cũng lưu được, danh sách có 2 phiếu báo cùng PNK-A"),

        ("015", "Công ty và số phiếu của phiếu báo", "P2",
         "Tài khoản G thuộc TPE, quyền xem theo tổng công ty. Có phiếu nhập kho đủ điều kiện của công ty X",
         "1. G lập phiếu báo từ phiếu nhập kho của công ty X, Lưu & gửi\n2. Xem Số phiếu\n"
         "3. Người duyệt của công ty X xem ô đếm ở trang chủ",
         "",
         "- Ghi nhận hành vi ERP: số phiếu mang mã TPE, phiếu tính cho công ty TPE của người lập\n"
         "- Ô đếm của người duyệt công ty X không tăng (cần hỏi lại nghiệp vụ)"),
    ]),

    ("VI", "Xem chi tiết phiếu", [
        ("001", "Bố cục trang chi tiết với người lập", "P0",
         "Phiếu báo Đang tạo do A lập từ PNK-A",
         "1. A bấm vào Số phiếu",
         "",
         "- Tiêu đề 'CHI TIẾT PHIẾU BÁO HÀNG THỪA, THIẾU NHẬP KHO:' kèm số phiếu\n"
         "- Góc phải khung Thông tin chung hiện tên người lập và ngày lập\n"
         "- Mọi ô bị khóa, không có dấu x bỏ phiếu nhập kho, không thêm / xóa file được\n"
         "- Bảng hàng H1, H2 đúng số đã lưu\n- Có nút 'Sửa' và 'Quay lại'"),

        ("002", "Phiếu Chờ xử lý với người lập", "P1",
         "Phiếu báo Chờ xử lý do A lập",
         "1. A mở chi tiết",
         "",
         "- Chỉ có nút 'Quay lại', không có 'Sửa'"),

        ("003", "Phiếu Chờ xử lý với người duyệt", "P0",
         "Phiếu báo Chờ xử lý do A lập",
         "1. D mở chi tiết",
         "",
         "- Có khung 'Ghi chú duyệt' nhập được\n- Có nút 'Xử lý', 'Không duyệt', 'Quay lại'"),

        ("004", "Phiếu Không duyệt hiện ghi chú duyệt", "P1",
         "Phiếu đã bị D không duyệt với ghi chú 'Thiếu biên bản'",
         "1. A mở chi tiết",
         "",
         "- Khung 'Ghi chú duyệt' hiện 'Thiếu biên bản', bị khóa\n- Có nút 'Sửa'"),

        ("005", "Nút Quay lại", "P2",
         "Đang ở trang chi tiết",
         "1. A bấm 'Quay lại'\n2. D (phiếu Chờ xử lý) bấm 'Quay lại'",
         "",
         "- Bước 1: về danh sách phiếu báo\n- Bước 2: về danh sách duyệt phiếu báo"),
    ]),

    ("VII", "Sửa phiếu", [
        ("001", "Mở trang Sửa", "P0",
         "Phiếu báo Đang tạo do A lập",
         "1. Bấm bánh răng, chọn 'Sửa phiếu'",
         "",
         "- Tiêu đề 'CHỈNH SỬA PHIẾU BÁO HÀNG THỪA, THIẾU NHẬP KHO:' kèm số phiếu\n"
         "- Phiếu nhập kho không có dấu x, không đổi được\n- Diễn giải sửa được, thêm / xóa file được\n"
         "- Có nút Lưu, Lưu & gửi, Hủy"),

        ("002", "Sửa Diễn giải và Lưu", "P0",
         "Trang Sửa phiếu Đang tạo",
         "1. Sửa Diễn giải thành 'Đã đối chiếu biên bản'\n2. Bấm Lưu\n3. Mở chi tiết",
         "",
         "- Báo 'Phiếu báo hàng thừa thiếu thành công!', về danh sách\n- Chi tiết hiện Diễn giải mới, trạng thái vẫn Đang tạo"),

        ("003", "Sửa xong bấm Lưu & gửi", "P0",
         "Trang Sửa phiếu Đang tạo",
         "1. Bấm 'Lưu & gửi'",
         "",
         "- Báo 'Yêu cầu phiếu báo hàng thừa thiếu đã được gửi!'\n- Trạng thái thành 'Chờ xử lý'\n- D nhận thông báo"),

        ("004", "Sửa phiếu Không duyệt và gửi lại", "P0",
         "Phiếu A lập đã bị D không duyệt",
         "1. A bấm 'Sửa phiếu'\n2. Thêm file biên bản, bấm 'Lưu & gửi'",
         "",
         "- Gửi thành công, trạng thái 'Chờ xử lý'\n- Phiếu lại hiện ở danh sách duyệt của D"),

        ("005", "Xóa file đính kèm ở trang Sửa", "P1",
         "Phiếu Đang tạo có 2 file",
         "1. Bấm dấu x ở 1 file\n2. Ở hộp thoại 'Xác nhận!' với nội dung 'Bạn chắc chắn muốn xóa file này?' bấm Xác nhận",
         "",
         "- Báo 'Xóa thành công', file biến mất, còn 1 file"),

        ("006", "Xóa hết file rồi lưu", "P2",
         "Phiếu Đang tạo có 1 file",
         "1. Xóa file đó\n2. Bấm Lưu",
         "",
         "- Hệ thống chặn vì phiếu phải có ít nhất 1 file như khi tạo\n"
         "- Lỗi ERP đã biết: lưu thành công, phiếu không còn file nào"),

        ("007", "Đơn giá còn nguyên sau khi sửa", "P1",
         "Phiếu Đang tạo từ PNK-A. D có quyền lập phiếu xử lý",
         "1. A sửa Diễn giải, bấm 'Lưu & gửi'\n2. D bấm 'Xử lý', xem cột đơn giá, thành tiền của H1",
         "",
         "- Đơn giá H1 đúng giá nhà cung cấp trong yêu cầu nhập hàng, thành tiền khác 0\n"
         "- Lỗi ERP đã biết: đơn giá trống, thành tiền bằng 0 vì đơn giá bị mất khi sửa"),

        ("008", "Không mở được trang Sửa khi phiếu đã gửi", "P1",
         "A đã sao chép đường dẫn trang Sửa khi phiếu còn Đang tạo, sau đó đã Lưu & gửi",
         "1. Dán lại đường dẫn trang Sửa",
         "",
         "- Ra trang không tìm thấy"),

        ("009", "Hủy sửa", "P2",
         "Trang Sửa, đã đổi Diễn giải",
         "1. Bấm 'Hủy'",
         "",
         "- Về danh sách, Diễn giải giữ như cũ"),
    ]),

    ("VIII", "Xóa phiếu", [
        ("001", "Hộp thoại xác nhận xóa", "P1",
         "Phiếu Đang tạo do A lập",
         "1. Bấm bánh răng, chọn 'Xóa'",
         "",
         "- Hộp thoại 'Xác nhận xóa!' nội dung 'Bạn chắc chắn muốn xóa bản ghi này?'"),

        ("002", "Xóa thành công", "P0",
         "Phiếu Đang tạo do A lập từ PNK-A",
         "1. Chọn 'Xóa', xác nhận",
         "",
         "- Báo 'Xóa yêu cầu thành công!'\n- Phiếu mất khỏi danh sách"),

        ("003", "Xóa phiếu Không duyệt", "P1",
         "Phiếu Không duyệt do A lập",
         "1. Chọn 'Xóa', xác nhận",
         "",
         "- Xóa thành công"),

        ("004", "Hủy ở hộp thoại xóa", "P2",
         "Đang ở hộp thoại xác nhận xóa",
         "1. Bấm Hủy",
         "",
         "- Hộp thoại đóng, phiếu vẫn còn"),

        ("005", "Xóa phiếu đã gửi bị chặn", "P1",
         "Danh sách đang mở, phiếu Đang tạo còn nút Xóa. Ở tab khác A đã Lưu & gửi phiếu đó",
         "1. Ở tab cũ chọn 'Xóa', xác nhận",
         "",
         "- Báo 'Không thể xóa phiếu báo hàng thừa thiếu nhập kho'\n- Phiếu vẫn còn, trạng thái Chờ xử lý"),
    ]),

    ("IX", "Duyệt: Xử lý và Không duyệt", [
        ("001", "Danh sách duyệt từ trang chủ", "P0",
         "Có 2 phiếu Chờ xử lý của TPE. Tài khoản D thuộc TPE",
         "1. Đăng nhập D, vào trang chủ, tab 'Phê duyệt'\n2. Bấm " + O_DUYET,
         "",
         "- Ô hiện số 2\n- Mở trang 'DANH SÁCH DUYỆT PHIẾU BÁO HÀNG THỪA, THIẾU NHẬP KHO', chỉ có phiếu Chờ xử lý"),

        ("002", "Danh sách duyệt chỉ có phiếu của công ty mình", "P1",
         "Công ty khác có phiếu Chờ xử lý",
         "1. D mở danh sách duyệt",
         "",
         "- Chỉ có phiếu của TPE, khớp với số ở ô trang chủ\n"
         "- Lỗi ERP đã biết: có cả phiếu Chờ xử lý của công ty khác"),

        ("003", "Không duyệt khi chưa nhập ghi chú", "P0",
         "D mở chi tiết phiếu Chờ xử lý",
         "1. Để trống 'Ghi chú duyệt'\n2. Bấm 'Không duyệt'",
         "",
         "- Báo 'Thao tác thất bại!'\n- Dưới ô Ghi chú duyệt báo 'Bắt buộc phải nhập'\n- Phiếu vẫn Chờ xử lý"),

        ("004", "Không duyệt thành công", "P0",
         "D mở chi tiết phiếu Chờ xử lý do A lập",
         "1. Nhập Ghi chú duyệt 'Thiếu biên bản'\n2. Bấm 'Không duyệt'",
         "",
         "- Báo 'Thao tác thành công', về danh sách duyệt, phiếu không còn ở đó\n"
         "- Ở danh sách phiếu báo, trạng thái 'Không duyệt'\n"
         "- A nhận thông báo 'Phiếu báo hàng thừa thiếu nhập kho không được duyệt bởi' kèm tên D\n"
         "- Lỗi ERP đã biết: thông báo ghi sai chữ 'Phiểu báo...'"),

        ("005", "Bấm Xử lý mở trang lập phiếu xử lý hàng thiếu", "P0",
         "Phiếu Chờ xử lý có H1 thiếu 4 Cái và H2 thừa 2 Cái. D có 'Tạo xử lý hàng thiếu nhập kho'",
         "1. D bấm bánh răng dòng phiếu, chọn 'Xử lý' (hoặc nút 'Xử lý' ở trang chi tiết)",
         "",
         "- Mở trang lập Phiếu xử lý hàng thiếu nhập kho, ô 'Phiếu báo thừa, thiếu' chọn sẵn phiếu này\n"
         "- Bảng chỉ có H1 với SL thiếu 4, không có H2 (chỉ thừa)"),

        ("006", "Lưu phiếu xử lý làm phiếu báo thành Đã xử lý", "P0",
         "Đang ở trang lập phiếu xử lý từ phiếu báo trên",
         "1. Điền đủ thông tin phiếu xử lý, phương án 'Trả hàng' 4 Cái cho H1, bấm Lưu\n2. Mở lại danh sách phiếu báo",
         "",
         "- Phiếu báo có trạng thái 'Đã xử lý', không còn nút nào ở bánh răng\n"
         "- Phiếu báo biến khỏi danh sách duyệt và ô đếm ở trang chủ giảm 1"),

        ("007", "Thiếu quyền tạo phiếu xử lý", "P1",
         "Tài khoản D2 có quyền duyệt phiếu báo nhưng không có 'Tạo xử lý hàng thiếu nhập kho'",
         "1. D2 bấm bánh răng phiếu Chờ xử lý",
         "",
         "- Không hiện 'Xử lý' với người không lập được phiếu xử lý\n"
         "- Lỗi ERP đã biết: vẫn có 'Xử lý', bấm vào ra trang không tìm thấy"),

        ("008", "Phiếu báo chỉ có hàng thừa", "P2",
         "Phiếu Chờ xử lý lập từ PNK-B (chỉ H2 thừa)",
         "1. D bấm 'Xử lý'\n2. Thử lưu phiếu xử lý",
         "",
         "- Ghi nhận hành vi ERP: bảng hàng trống, không lưu được, phiếu báo đứng mãi ở 'Chờ xử lý'\n"
         "- Hàng thừa chưa có luồng xử lý trên ERP"),

        ("009", "Xóa phiếu xử lý thì phiếu báo về Chờ xử lý", "P2",
         "Phiếu báo đã Đã xử lý nhờ phiếu xử lý Đang tạo",
         "1. Vào " + MENU_XL + ", xóa phiếu xử lý đó\n2. Xem phiếu báo",
         "",
         "- Phiếu báo trở lại 'Chờ xử lý' để lập phiếu xử lý khác\n"
         "- Lỗi ERP đã biết: phiếu báo vẫn 'Đã xử lý', không chọn lại được ở trang lập phiếu xử lý"),
    ]),

    ("X", "In và Xuất excel", [
        ("001", "In danh sách", "P1",
         "Lọc Trạng thái 'Chờ xử lý', bấm kính lúp",
         "1. Bấm nút 'In'",
         "",
         "- Mở tab mới bản in khổ ngang, tiêu đề 'DANH SÁCH PHIẾU BÁO HÀNG THỪA, THIẾU NHẬP KHO'\n"
         "- 8 cột: STT, Số phiếu, Ngày lập, Phiếu nhập kho, Yêu cầu nhập, Nhà cung cấp, Số hợp đồng, Trạng thái\n"
         "- Chỉ có các phiếu Chờ xử lý"),

        ("002", "Xuất excel", "P0",
         "Lọc Phiếu nhập kho PNK-A, bấm kính lúp",
         "1. Bấm 'Xuất excel'\n2. Mở file",
         "",
         "- Tải file 'danh_sach_phieu_bao_hang_thua_thieu_nhap_kho.xlsx'\n"
         "- Tiêu đề 'DANH SÁCH PHIẾU BÁO HÀNG THỪA THIẾU NHẬP KHO', 8 cột như bản in\n- Chỉ có phiếu báo của PNK-A"),

        ("003", "Xuất toàn bộ khi không lọc", "P1",
         "Không lọc gì, danh sách có nhiều trang",
         "1. Xuất excel",
         "",
         "- File có đủ mọi phiếu của mọi trang, số dòng bằng tổng số bản ghi trên màn"),

        ("004", "Ngày lập trong bản in và file", "P2",
         "Phiếu lập ngày 20/10/2026 lúc 14:30",
         "1. In và Xuất excel",
         "",
         "- Ngày lập hiện 20/10/2026, không có giờ"),
    ]),

    ("XI", "Kiểm tra tăng / giảm số liệu trên báo cáo", [
        ("001", "Đối chứng: tồn kho đã ghi theo SL thực nhập từ phiếu nhập kho", "P0",
         "PNK-A đã hạch toán, kho LN: H1 đề nghị 10 thực nhập 6",
         "1. Mở " + BC_THE + ", chọn hàng H1, kho LN, khoảng ngày chứa ngày nhập PNK-A, bấm tìm\n"
         "2. Tìm dòng có Số chứng từ PNK-A",
         "H1, kho LN",
         "- Dòng PNK-A có cột Nhập = 6 (SL thực nhập), không phải 10\n"
         "- Đây là lý do phiếu báo không cần ghi tồn: phần thiếu 4 chưa từng vào kho"),

        ("002", "Lưu phiếu báo không làm đổi tồn kho tổng hợp", "P0",
         "PNK-A chưa có phiếu báo",
         "1. Mở " + BC_TON + ", Tính đến ngày hôm nay, Tồn theo công ty TPE, Kho LN, Hàng hóa H1 và H2, bấm tìm, "
         "GHI LẠI cột SL tồn của H1 (ví dụ T1) và H2 (ví dụ T2)\n"
         "2. Lập phiếu báo từ PNK-A (H1 thiếu 4, H2 thừa 2), bấm 'Lưu & gửi'\n3. Mở lại báo cáo với đúng bộ lọc",
         "H1, H2, kho LN",
         "- SL tồn H1 vẫn bằng T1, H2 vẫn bằng T2, không cộng / trừ 4 hay 2"),

        ("003", "Phiếu báo không xuất hiện trên Thẻ kho", "P1",
         "Vừa lập phiếu báo từ PNK-A",
         "1. Mở " + BC_THE + ", chọn H1, kho LN, khoảng ngày đến hôm nay",
         "",
         "- Không có dòng chứng từ nào mang số phiếu báo 'TPE_BHNK-'\n- SL tồn cuối của H1 không đổi so với trước khi lập"),

        ("004", "Không duyệt và Xóa phiếu báo không làm đổi tồn", "P1",
         "Ghi lại SL tồn H1 tại kho LN trên " + BC_TON + " (T1)",
         "1. D bấm 'Không duyệt' phiếu báo của PNK-A\n2. A xóa phiếu đó\n3. Mở lại báo cáo sau mỗi bước",
         "",
         "- Sau cả 2 bước SL tồn H1 vẫn bằng T1"),

        ("005", "Lập phiếu báo làm giảm 1 phiếu ở màn Phiếu nhập kho chờ báo thừa, thiếu", "P0",
         "PNK-A chưa có phiếu báo",
         "1. Mở " + MENU_NGUON + ", không lọc, GHI LẠI tổng số bản ghi ở chân bảng (ví dụ N)\n"
         "2. Lập phiếu báo từ PNK-A, chỉ bấm 'Lưu' (Đang tạo)\n3. Mở lại màn đó, tìm PNK-A",
         "PNK-A",
         "- Tổng số bản ghi còn N trừ 1\n- Không tìm thấy PNK-A, kể cả khi phiếu báo mới chỉ Đang tạo"),

        ("006", "Xóa phiếu báo làm tăng lại 1 phiếu", "P0",
         "Đã làm TC trên, tổng số bản ghi đang là N trừ 1",
         "1. Xóa phiếu báo của PNK-A\n2. Mở lại " + MENU_NGUON,
         "",
         "- Tổng số bản ghi trở lại N\n- PNK-A hiện lại, còn nút 'Báo hàng thừa thiếu'"),

        ("007", "Không duyệt không trả phiếu nhập kho về màn chờ", "P1",
         "Phiếu báo của PNK-A đang Chờ xử lý. Tổng số bản ghi màn chờ đang là M",
         "1. D bấm 'Không duyệt'\n2. Mở lại " + MENU_NGUON,
         "",
         "- Tổng số bản ghi vẫn là M, PNK-A không hiện lại\n- Muốn lập lại phải sửa phiếu Không duyệt hoặc xóa nó"),

        ("008", "Ô đếm 'cần xử lý' ở trang chủ tăng / giảm", "P0",
         "Tài khoản D thuộc TPE. Ghi lại số ở " + O_DUYET + " (ví dụ K, ô ẩn nghĩa là 0)",
         "1. A lập phiếu báo, bấm 'Lưu'. D tải lại trang chủ\n2. A sửa phiếu, bấm 'Lưu & gửi'. D tải lại\n"
         "3. D bấm 'Không duyệt'. D tải lại",
         "",
         "- Bước 1: vẫn K\n- Bước 2: K cộng 1\n- Bước 3: trở về K"),

        ("009", "Lập phiếu xử lý làm giảm ô đếm và danh sách duyệt", "P1",
         "Phiếu báo Chờ xử lý có hàng thiếu. Ô đếm đang là K",
         "1. D bấm 'Xử lý', lưu phiếu xử lý\n2. Tải lại trang chủ và danh sách duyệt",
         "",
         "- Ô đếm còn K trừ 1\n- Danh sách duyệt mất phiếu đó\n- Phiếu báo trạng thái 'Đã xử lý'"),

        ("010", "Phiếu xử lý hàng thiếu cũng không đổi tồn", "P1",
         "Ghi lại SL tồn H1 kho LN trên " + BC_TON + " (T1)",
         "1. D lập phiếu xử lý từ phiếu báo PNK-A, phương án 'Trả hàng' 4 Cái, gửi và duyệt phiếu xử lý\n"
         "2. Mở lại báo cáo",
         "",
         "- SL tồn H1 vẫn bằng T1\n"
         "- Tồn chỉ tăng khi nhà cung cấp giao bù và kho lập phiếu nhập kho mới cho 4 Cái đó: khi đó Thẻ kho có "
         "dòng nhập mới và SL tồn tăng đúng 4"),

        ("011", "Tình trạng trả hàng thiếu chỉ tính theo phiếu xử lý", "P2",
         "Có phiếu báo PNK-A đã gửi nhưng chưa có phiếu xử lý",
         "1. Mở " + MENU_TRA + ", lọc theo hàng H1\n2. Sau khi phiếu xử lý phương án 'Trả hàng' được duyệt và "
         "hoàn tất, mở lại",
         "",
         "- Bước 1: chưa có dòng nào của H1 từ phiếu báo này\n"
         "- Bước 2: mới có dòng H1 theo số phiếu xử lý, SL thiếu 4"),
    ]),

    ("XII", "Gọi thẳng chức năng", [
        ("001", "Người lập tự gọi Không duyệt phiếu của mình", "P1",
         "Tester kỹ thuật. A lập phiếu Chờ xử lý, A không có quyền duyệt",
         "1. Đăng nhập A\n2. Dùng công cụ kiểm thử API gọi thẳng chức năng duyệt phiếu với lựa chọn Không duyệt, kèm ghi chú",
         "",
         "- Hệ thống báo 'Bạn không có quyền', phiếu vẫn Chờ xử lý\n"
         "- Lỗi ERP đã biết: thao tác thành công, phiếu thành Không duyệt"),

        ("002", "Gọi duyệt chuyển thẳng sang Đã xử lý", "P1",
         "Tester kỹ thuật. Phiếu Đang tạo do A lập",
         "1. Đăng nhập A\n2. Gọi thẳng chức năng duyệt phiếu với trạng thái Đã xử lý",
         "",
         "- Hệ thống từ chối vì phiếu chưa gửi và A không có quyền duyệt\n"
         "- Lỗi ERP đã biết: phiếu thành Đã xử lý mà không có phiếu xử lý nào"),

        ("003", "Gọi thẳng chức năng Sửa phiếu của người khác", "P1",
         "Tester kỹ thuật. Phiếu Đang tạo do A lập",
         "1. Đăng nhập D\n2. Gọi thẳng chức năng cập nhật phiếu đó",
         "",
         "- Báo 'Bạn không có quyền', phiếu không đổi"),

        ("004", "Gọi thẳng chức năng Xóa phiếu của người khác", "P1",
         "Phiếu Đang tạo do A lập",
         "1. Đăng nhập D\n2. Gọi thẳng chức năng Xóa phiếu đó",
         "",
         "- Báo 'Không thể xóa phiếu báo hàng thừa thiếu nhập kho', phiếu vẫn còn"),

        ("005", "Gọi thẳng chức năng xóa file của phiếu đã gửi", "P2",
         "Phiếu Chờ xử lý do A lập có 1 file",
         "1. Đăng nhập A\n2. Gọi thẳng chức năng xóa file của phiếu",
         "",
         "- Báo 'Không có quyền', file vẫn còn"),

        ("006", "Gọi thẳng chức năng Thêm với phiếu nhập kho đã có phiếu báo", "P2",
         "Tester kỹ thuật. PNK-A đã có phiếu báo",
         "1. Gọi thẳng chức năng Thêm phiếu báo cho PNK-A, đủ Diễn giải, file, dòng hàng",
         "",
         "- Hệ thống chặn vì PNK-A đã có phiếu báo\n- Lỗi ERP đã biết: tạo thêm được phiếu báo thứ 2"),
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
