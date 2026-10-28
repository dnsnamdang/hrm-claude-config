# -*- coding: utf-8 -*-
"""Generate testcase Excel cho man ERP: Khai bao ton kho dau ky (kho vat ly).

Viet cho MAN ERP GOC (TanPhatDev, route beginningStock.*), de tester nam luong ERP
truoc khi nghiem thu ban HRM da port (hrm/.plans/gop-db/ton-kho-dau-ky).

Chay:  python gen_testcase.py
Output: testcase - Khai bao ton kho dau ky.xlsx (cung thu muc)
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

OUTPUT_FILE = os.path.join(HERE, "testcase - Khai bao ton kho dau ky.xlsx")
FEATURE_NAME = "Khai báo tồn kho đầu kỳ (ERP)"
MODULE_NAME = "Kho - Tồn kho đầu kỳ"

MENU = "menu Kho > Tồn kho đầu kỳ > 'Khai báo tồn kho đầu kỳ'"

# =========================================================================
# 9 MUC MO TA
# =========================================================================
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Khai báo số lượng hàng đang nằm thực tế trong KHO VẬT LÝ tại thời điểm bắt đầu dùng hệ thống, "
     "chi tiết đến từng VỊ TRÍ trong kho, theo từng CÔNG TY sở hữu hàng.\n"
     "Đường vào: " + MENU + ". Tiêu đề trang: 'Khai báo tồn đầu kỳ'.\n"
     "Màn gồm: danh sách đã khai, trang Tạo mới (khai nhiều hàng một lần), trang Sửa (chỉ sửa số lượng "
     "của một dòng), Xóa từng dòng, Import Excel và Xuất Excel.\n"
     "Điều kiện nền: hàng phải được khai TỒN KHO KẾ TOÁN ĐẦU KỲ trước (màn Khai báo tồn kho kế toán đầu "
     "kỳ) tại kho kế toán gắn với kho vật lý đó của cùng công ty. Số lượng vật lý phải bằng số kế toán."),

    ("2. Đối tượng được tính / hiển thị",
     "Mỗi dòng danh sách là một cặp HÀNG x VỊ TRÍ đã khai. Một hàng khai ở 3 vị trí sẽ ra 3 dòng.\n"
     "Danh sách mặc định xếp dòng khai mới nhất lên đầu.\n"
     "Sau khi khai, số lượng được cộng ngay vào tồn kho vật lý của kho / vị trí đó và sinh một lô hàng tồn "
     "đầu có số lô bắt đầu bằng 'TONDAUKHO-' để các phiếu xuất về sau chọn được."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Hàng đã khai cho cùng KHO + CÔNG TY thì không chọn lại được ở trang Tạo mới, Import cũng chặn.\n"
     "- Hàng ĐÃ CÓ GIAO DỊCH tại kho đó của công ty đó (đã nhập, xuất, chuyển vị trí, kể cả phiếu xuất "
     "đang lập) thì không khai tồn đầu được nữa, và các dòng đã khai mất nút Sửa / Xóa.\n"
     "- Giao dịch của CÔNG TY KHÁC trên cùng kho không làm khóa dòng khai của công ty mình.\n"
     "- Kho ở trang Tạo mới chỉ gồm kho vật lý đang hoạt động có gắn kho kế toán của công ty người đăng nhập."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Màn KHÔNG có bộ lọc thời gian. Cột 'Ngày tạo' là ngày người dùng bấm lưu, không phải ngày tồn đầu.\n"
     "Ngày tồn đầu ghi vào sổ tồn kho là mốc cấu hình chung của hệ thống (ngày bắt đầu sổ), giống nhau cho "
     "mọi dòng, không theo ngày tạo."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Danh sách 10 cột: STT, Tên hàng, Mã hàng, Kho, Vị trí, ĐVT, Số lượng, Người tạo, Ngày tạo, Hành động "
     "(nút bánh răng, gồm Sửa / Xóa).\n"
     "Bộ lọc: Công ty (chỉ người có quyền 'Xem tất cả phiếu'), Tên hàng, Mã hàng, Kho, Vị trí, Người tạo. "
     "Lọc chạy ngay khi gõ / chọn, không có nút Lọc.\n"
     "Trang Tạo mới: ô Kho, ô Công ty, rồi bảng hàng: STT, Tên hàng hóa, Model, Mã hàng hóa, Đơn vị tính, "
     "Tổng số lượng, Vị trí, Số lượng. Mỗi hàng có nhiều dòng vị trí (link 'Thêm kho'). Dòng 'Tổng cộng' cộng "
     "số lượng mọi vị trí.\n"
     "File Import: 7 cột Tên hàng hóa, Mã hàng hóa, Đơn vị tính, Kho (mã kho), Vị trí (mã vị trí), Số lượng, "
     "Công ty (mã công ty); dữ liệu từ dòng 2; tối đa 200 dòng."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Tổng số lượng của một hàng ở trang Tạo mới lấy sẵn bằng số tồn kế toán đầu kỳ, quy theo đơn vị tính "
     "đã khai kế toán, KHÔNG sửa được. Đơn vị tính cũng khóa theo đơn vị kế toán.\n"
     "- Tổng số lượng các vị trí của một hàng phải bằng Tổng số lượng. Ô số lượng vị trí không cho nhập quá "
     "phần còn lại; để trống thì tự lấy phần còn lại.\n"
     "- Import: các dòng cùng Mã hàng + Kho + Công ty được cộng dồn rồi so với số kế toán (quy về đơn vị cơ "
     "bản), nên một hàng chia được ra nhiều vị trí trên nhiều dòng file.\n"
     "- Import là tất cả hoặc không: chỉ một dòng lỗi thì không dòng nào được ghi."),

    ("7. Phân quyền cấp",
     "- Vào màn và mọi thao tác (xem, thêm, sửa, xóa, import, xuất) cần quyền 'Thủ kho'. Menu hiện cho mọi "
     "người, thiếu quyền bấm vào ra trang không tìm thấy.\n"
     "- Phạm vi xem danh sách: 'Xem khai báo tồn kho vật lý theo tổng công ty' thấy mọi công ty; 'Xem khai "
     "báo tồn kho vật lý theo công ty' chỉ thấy công ty của người đăng nhập.\n"
     "- Ô Công ty ở trang Tạo mới chỉ liệt kê các công ty người đăng nhập được thao tác."),

    ("8. Cách tính các ô thống kê",
     "Màn danh sách không có ô tổng. Trang Tạo mới có dòng 'Tổng cộng' = tổng số lượng của mọi vị trí của mọi "
     "hàng đang chọn.\n"
     "Xuất Excel: dưới 300 dòng tải file ngay; từ 300 dòng trở lên hệ thống gửi file về email người bấm."),

    ("9. Ghi chú đọc bảng",
     "Các lỗi ERP ĐÃ BIẾT được viết thành testcase với kết quả mong đợi ĐÚNG, kèm dòng 'Lỗi ERP đã biết'. "
     "Chạy thấy đúng hiện tượng lỗi thì ghi Failed và chép câu đó vào cột Ghi chú:\n"
     "(1) Người không có quyền xem nào trong 2 quyền xem khai báo vẫn thấy dữ liệu của MỌI công ty.\n"
     "(2) Ô Kho ở trang Tạo mới luôn lấy kho của công ty người đăng nhập, không đổi theo ô Công ty.\n"
     "(3) Hàng chưa khai tồn kế toán vẫn thêm được vào bảng với số lượng 0, bấm Lưu chỉ báo 'Thêm thất bại!' "
     "không nói lý do.\n"
     "(4) Trang Sửa cho lưu số lượng khác số tồn kế toán (thêm tay và Import thì bắt khớp).\n"
     "(5) Khai cho công ty khác công ty mình: tồn theo công ty có thể bị cộng nhầm vào công ty người đăng nhập.\n"
     "(6) Sau khi Sửa số lượng, tồn theo công ty không đổi theo. Sau khi Xóa, tồn vị trí theo công ty ra số âm.\n"
     "(7) Hàng khai ở nhiều vị trí, đã xuất kho từ lô của vị trí thứ 2 trở đi: dòng khai vẫn còn nút Sửa / Xóa.\n"
     "(8) Nhãn sai: ô Công ty ở trang Tạo mới ghi sẵn 'Chọn kho'; ô lọc Người tạo ghi 'Người duyệt'.\n"
     "Nhóm 'Gọi thẳng chức năng' dành cho tester kỹ thuật, dùng công cụ kiểm thử API, bỏ qua giao diện.\n"
     "Dữ liệu mẫu dùng trong bộ TC: công ty TPE; kho LN có kho kế toán gắn; hàng H1 đã khai kế toán 100 Cái, "
     "chưa khai vật lý, chưa có giao dịch; hàng H2 đã khai kế toán 10 Hộp (1 Hộp = 12 Cái); hàng H3 chưa khai "
     "kế toán; vị trí V1, V2, V3 thuộc kho LN; vị trí K1 thuộc kho khác."),
]

# =========================================================================
# SECTION PHAN QUYEN
# =========================================================================
ROLE_TCS = [
    ("00", "Có quyền 'Thủ kho' mở được màn từ menu", "P0",
     "Tài khoản A có quyền 'Thủ kho' và 'Xem khai báo tồn kho vật lý theo tổng công ty'",
     "1. Đăng nhập ERP bằng tài khoản A\n2. Vào " + MENU,
     "Tài khoản: A",
     "- Mở được trang 'Khai báo tồn đầu kỳ'\n"
     "- Có nút Bộ lọc, Tạo mới, Import Excel, Xuất Excel và bảng danh sách"),

    ("01", "Thiếu quyền 'Thủ kho' vẫn thấy menu nhưng không vào được", "P0",
     "Tài khoản B không có quyền 'Thủ kho'",
     "1. Đăng nhập bằng tài khoản B\n2. Mở menu Kho > Tồn kho đầu kỳ\n3. Bấm 'Khai báo tồn kho đầu kỳ'",
     "Tài khoản: B",
     "- Bước 2: menu vẫn hiện mục 'Khai báo tồn kho đầu kỳ'\n"
     "- Bước 3: hiện trang không tìm thấy, không thấy dữ liệu khai báo"),

    ("02", "Thiếu quyền 'Thủ kho' không mở được trang Tạo mới và trang Sửa", "P1",
     "Tài khoản B không có quyền 'Thủ kho'. Tài khoản A đã sao chép sẵn đường dẫn trang Tạo mới và "
     "trang Sửa của một dòng",
     "1. Đăng nhập bằng tài khoản B\n2. Dán đường dẫn trang Tạo mới vào trình duyệt\n"
     "3. Dán đường dẫn trang Sửa",
     "Tài khoản: B",
     "- Cả 2 trang đều ra trang không tìm thấy"),

    ("03", "Quyền xem theo tổng công ty thấy mọi công ty", "P0",
     "Tài khoản A có 'Thủ kho' và 'Xem khai báo tồn kho vật lý theo tổng công ty'. Có dòng khai của ít "
     "nhất 2 công ty",
     "1. Đăng nhập bằng A, mở màn\n2. Xem danh sách, không lọc",
     "Tài khoản: A",
     "- Thấy dòng khai của mọi công ty"),

    ("04", "Quyền xem theo công ty chỉ thấy công ty của mình", "P0",
     "Tài khoản C thuộc công ty TPE, có 'Thủ kho' và 'Xem khai báo tồn kho vật lý theo công ty', không có "
     "quyền xem theo tổng công ty. Có dòng khai của công ty khác",
     "1. Đăng nhập bằng C, mở màn\n2. Xem danh sách\n3. Lọc Mã hàng của một hàng chỉ khai ở công ty khác",
     "Tài khoản: C",
     "- Bước 2: chỉ thấy dòng khai của công ty TPE\n- Bước 3: bảng không có dòng nào"),

    ("05", "Không có quyền xem nào thì không thấy dữ liệu công ty khác", "P0",
     "Tài khoản D có 'Thủ kho' nhưng KHÔNG có cả 2 quyền 'Xem khai báo tồn kho vật lý theo tổng công ty' "
     "và 'theo công ty'",
     "1. Đăng nhập bằng D, mở màn\n2. Xem danh sách",
     "Tài khoản: D",
     "- Chỉ thấy dòng khai của công ty mình, hoặc không thấy dòng nào\n"
     "- Lỗi ERP đã biết: D thấy dòng khai của MỌI công ty"),

    ("06", "Ô lọc Công ty chỉ hiện với người có quyền xem tất cả phiếu", "P1",
     "Tài khoản A có thêm quyền 'Xem tất cả phiếu'. Tài khoản C không có quyền này",
     "1. Đăng nhập A, mở màn, bấm 'Bộ lọc'\n2. Đăng nhập C, mở màn, bấm 'Bộ lọc'",
     "Tài khoản: A, C",
     "- Bước 1: có ô lọc Công ty\n- Bước 2: không có ô lọc Công ty"),

    ("07", "Ô Công ty ở trang Tạo mới chỉ có công ty được thao tác", "P1",
     "Tài khoản C thuộc công ty TPE, chỉ được thao tác công ty TPE",
     "1. Đăng nhập C, vào trang Tạo mới\n2. Mở ô Công ty",
     "Tài khoản: C",
     "- Chỉ liệt kê công ty TPE, không có công ty khác"),

    ("08", "Gọi thẳng chức năng Thêm khi thiếu quyền 'Thủ kho'", "P1",
     "Tài khoản B không có quyền 'Thủ kho'. Tester kỹ thuật có công cụ kiểm thử API",
     "1. Đăng nhập B\n2. Dùng công cụ kiểm thử API gọi thẳng chức năng Thêm khai báo với dữ liệu hợp lệ",
     "Hàng H1, kho LN, công ty TPE",
     "- Hệ thống từ chối, báo 'Không có quyền!'\n- Không sinh dòng khai, tồn kho không đổi"),

    ("09", "Gọi thẳng chức năng Xóa khi thiếu quyền 'Thủ kho'", "P1",
     "Tài khoản B không có quyền 'Thủ kho'. Có một dòng khai chưa giao dịch",
     "1. Đăng nhập B\n2. Gọi thẳng chức năng Xóa của dòng đó",
     "Tài khoản: B",
     "- Ra trang không tìm thấy\n- Dòng khai vẫn còn trong danh sách"),
]

# =========================================================================
# CAC SECTION CHUC NANG
# =========================================================================
SECTIONS = [
    ("I", "Giao diện danh sách", [
        ("001", "Bố cục màn danh sách", "P0",
         "Tài khoản A. Có sẵn dòng khai",
         "1. Vào " + MENU + "\n2. Quan sát",
         "",
         "- Tiêu đề trang 'Khai báo tồn đầu kỳ'\n"
         "- Góc phải có nút 'Import Excel' và 'Xuất Excel'\n"
         "- Phía trên bảng có nút 'Bộ lọc' và 'Tạo mới'\n"
         "- Bảng có đủ 10 cột: STT, Tên hàng, Mã hàng, Kho, Vị trí, ĐVT, Số lượng, Người tạo, Ngày tạo, "
         "Hành động"),

        ("002", "Thứ tự mặc định: dòng khai mới nhất lên đầu", "P1",
         "Vừa khai xong hàng H1",
         "1. Mở màn danh sách\n2. Xem dòng đầu tiên",
         "Hàng H1",
         "- Dòng đầu tiên là dòng của H1 vừa khai"),

        ("003", "Một hàng khai nhiều vị trí ra nhiều dòng", "P0",
         "Hàng H1 đã khai 60 Cái ở V1 và 40 Cái ở V2",
         "1. Lọc Mã hàng H1",
         "Hàng H1",
         "- Ra 2 dòng: V1 số lượng 60, V2 số lượng 40\n- Cột Kho cùng là LN, ĐVT cùng là Cái"),

        ("004", "Định dạng cột Ngày tạo và Người tạo", "P2",
         "Tài khoản A vừa khai hàng H1",
         "1. Xem dòng H1",
         "",
         "- Ngày tạo dạng ngày/tháng/năm, là ngày bấm lưu\n- Người tạo là họ tên của tài khoản A"),

        ("005", "Sắp xếp theo cột Số lượng và Ngày tạo", "P2",
         "Có nhiều dòng khai",
         "1. Bấm tiêu đề cột Số lượng\n2. Bấm lại lần nữa\n3. Bấm tiêu đề cột Ngày tạo\n"
         "4. Bấm tiêu đề cột Tên hàng",
         "",
         "- Bước 1, 2: bảng xếp tăng rồi giảm theo Số lượng\n- Bước 3: xếp theo Ngày tạo\n"
         "- Bước 4: cột Tên hàng không sắp xếp được"),

        ("006", "Nút Hành động của dòng chưa có giao dịch", "P0",
         "Hàng H1 đã khai, chưa có phiếu nhập / xuất / chuyển vị trí nào",
         "1. Bấm nút bánh răng ở dòng H1",
         "",
         "- Hiện 2 lựa chọn 'Sửa' và 'Xóa'"),

        ("007", "Nút Hành động của dòng đã có giao dịch", "P0",
         "Hàng H1 đã khai ở kho LN, sau đó đã có phiếu xuất kho H1 từ kho LN của công ty TPE",
         "1. Bấm nút bánh răng ở dòng H1",
         "",
         "- Danh sách thả xuống trống, không có 'Sửa', không có 'Xóa'"),

        ("008", "Phân trang danh sách", "P2",
         "Có hơn 10 dòng khai",
         "1. Chuyển sang trang 2\n2. Đổi số dòng mỗi trang",
         "",
         "- STT trang 2 nối tiếp trang 1\n- Đổi số dòng mỗi trang thì bảng tải lại đúng số dòng"),
    ]),

    ("II", "Bộ lọc danh sách", [
        ("001", "Lọc Tên hàng tìm theo cả tên và mã", "P0",
         "Có dòng khai hàng H1",
         "1. Bấm 'Bộ lọc'\n2. Ô Tên hàng gõ một phần tên của H1\n3. Xóa, gõ một phần mã của H1",
         "Một phần tên / mã H1",
         "- Cả 2 lần đều ra các dòng của H1\n- Bảng lọc ngay khi gõ, không cần bấm nút"),

        ("002", "Lọc Mã hàng chỉ tìm theo mã", "P1",
         "Có dòng khai hàng H1",
         "1. Ô Mã hàng gõ một phần mã H1\n2. Xóa, gõ một phần TÊN H1 không trùng mã hàng nào",
         "",
         "- Bước 1: ra các dòng H1\n- Bước 2: bảng không có dòng nào"),

        ("003", "Lọc Kho", "P0",
         "Có dòng khai ở kho LN và kho khác",
         "1. Ô Kho chọn LN",
         "Kho LN",
         "- Chỉ còn dòng có cột Kho là LN"),

        ("004", "Danh sách ô lọc Kho", "P2",
         "Hệ thống có kho loại thường, kho thanh lý và kho loại khác",
         "1. Mở ô lọc Kho",
         "",
         "- Chỉ có kho loại thường và kho thanh lý\n- Có cả kho của công ty khác"),

        ("005", "Lọc Vị trí theo tên vị trí", "P1",
         "Có dòng khai ở V1 và V2",
         "1. Ô Vị trí gõ tên V1",
         "Tên vị trí V1",
         "- Chỉ còn dòng có cột Vị trí là V1"),

        ("006", "Lọc Người tạo", "P1",
         "Tài khoản A và tài khoản E cùng có dòng khai",
         "1. Ô Người tạo gõ tên E, chọn E",
         "Nhân viên E",
         "- Chỉ còn dòng có Người tạo là E\n"
         "- Ô lọc phải ghi nhãn 'Người tạo'. Lỗi ERP đã biết: ô ghi 'Người duyệt'"),

        ("007", "Lọc Công ty", "P1",
         "Tài khoản A có quyền 'Xem tất cả phiếu'. Có dòng khai của TPE và công ty khác",
         "1. Ô Công ty chọn TPE",
         "Công ty TPE",
         "- Chỉ còn dòng khai của công ty TPE"),

        ("008", "Kết hợp nhiều điều kiện lọc", "P1",
         "Có dữ liệu nhiều kho, nhiều hàng",
         "1. Chọn Kho LN\n2. Gõ Mã hàng H1\n3. Gõ Vị trí V1",
         "",
         "- Sau mỗi bước bảng thu hẹp lại\n- Cuối cùng chỉ còn dòng H1 ở V1 kho LN"),

        ("009", "Không có kết quả phù hợp", "P2",
         "",
         "1. Ô Mã hàng gõ chuỗi không có thật",
         "XYZ-KHONG-CO",
         "- Bảng báo không có dữ liệu, không lỗi trang"),

        ("010", "Bỏ điều kiện lọc", "P2",
         "Đang lọc Kho LN",
         "1. Bỏ chọn ô Kho",
         "",
         "- Bảng hiện lại đầy đủ dòng theo phạm vi xem"),
    ]),

    ("III", "Tạo mới: chọn kho, công ty và hàng", [
        ("001", "Bố cục trang Tạo mới", "P0",
         "Tài khoản A",
         "1. Ở danh sách bấm 'Tạo mới'",
         "",
         "- Có ô Kho (bắt buộc) và ô Công ty (bắt buộc)\n"
         "- Bảng hàng có cột STT, Tên hàng hóa, Model, Mã hàng hóa, Đơn vị tính, Tổng số lượng, Vị trí, "
         "Số lượng và nút dấu cộng chọn hàng\n"
         "- Dòng 'Tổng cộng' bằng 0 và dòng 'Chưa chọn hàng hóa'\n"
         "- Dưới cùng có nút Lưu, Lưu & Thêm, Hủy"),

        ("002", "Nhãn ô Công ty", "P2",
         "Đang ở trang Tạo mới",
         "1. Xem chữ gợi ý trong ô Công ty khi chưa chọn",
         "",
         "- Ô ghi 'Chọn công ty'\n- Lỗi ERP đã biết: ô ghi 'Chọn kho'"),

        ("003", "Danh sách ô Kho", "P1",
         "Tài khoản A thuộc công ty TPE. Kho LN có gắn kho kế toán của TPE. Có kho vật lý chưa gắn kho kế "
         "toán nào và kho đã ngừng hoạt động",
         "1. Mở ô Kho",
         "",
         "- Có kho LN\n- Không có kho chưa gắn kho kế toán, không có kho ngừng hoạt động\n"
         "- Tên kho hiện dạng 'Mã - Tên'"),

        ("004", "Ô Kho đổi theo công ty đã chọn", "P1",
         "Tài khoản A thuộc TPE, được thao tác cả công ty X. Kho KX chỉ gắn kho kế toán của công ty X",
         "1. Ô Công ty chọn X\n2. Mở ô Kho",
         "Công ty X, kho KX",
         "- Ô Kho có kho KX của công ty X\n"
         "- Lỗi ERP đã biết: ô Kho vẫn chỉ có kho của TPE, không thấy KX"),

        ("005", "Nút chọn hàng khóa khi chưa chọn kho", "P0",
         "Đang ở trang Tạo mới, chưa chọn kho",
         "1. Bấm nút dấu cộng ở đầu bảng hàng",
         "",
         "- Nút bị mờ, không mở được cửa sổ chọn hàng"),

        ("006", "Chọn hàng đã khai kế toán", "P0",
         "Chọn Kho LN, Công ty TPE",
         "1. Bấm nút dấu cộng\n2. Tìm và chọn hàng H1",
         "Hàng H1 (kế toán 100 Cái)",
         "- Báo 'Thêm thành công'\n- Bảng có dòng H1: Tên, Model, Mã hàng đúng\n"
         "- Đơn vị tính Cái, bị khóa\n- Tổng số lượng 100\n"
         "- Có sẵn 1 dòng vị trí trống, ô số lượng hiện 100"),

        ("007", "Đơn vị tính lấy theo đơn vị khai kế toán", "P1",
         "Chọn Kho LN, Công ty TPE. H2 khai kế toán 10 Hộp, 1 Hộp = 12 Cái",
         "1. Chọn hàng H2",
         "Hàng H2",
         "- Đơn vị tính là Hộp, kèm '(x12)', bị khóa\n- Tổng số lượng 10"),

        ("008", "Hàng đã khai vật lý cho cùng kho và công ty", "P0",
         "H1 đã khai ở kho LN cho TPE",
         "1. Chọn Kho LN, Công ty TPE\n2. Chọn hàng H1",
         "Hàng H1",
         "- Báo 'Hàng hóa đã được khai báo tồn đầu kì. Kho :' kèm mã kho LN\n- H1 không vào bảng"),

        ("009", "Cùng hàng nhưng khác công ty vẫn chọn được", "P1",
         "H1 đã khai kho LN cho TPE. Công ty X đã khai kế toán H1 ở kho kế toán gắn kho LN",
         "1. Chọn Kho LN, Công ty X\n2. Chọn hàng H1",
         "",
         "- H1 vào bảng bình thường với số lượng kế toán của công ty X"),

        ("010", "Hàng chưa khai tồn kế toán", "P0",
         "Chọn Kho LN, Công ty TPE",
         "1. Chọn hàng H3\n2. Chọn vị trí V1\n3. Bấm Lưu",
         "Hàng H3",
         "- Hệ thống chặn ngay khi chọn hàng, báo rõ hàng chưa khai kho kế toán\n"
         "- Lỗi ERP đã biết: H3 vào bảng với Tổng số lượng 0, bấm Lưu chỉ báo 'Thêm thất bại!', không nói "
         "lý do"),

        ("011", "Chọn hàng khi chưa chọn công ty", "P1",
         "Chọn Kho LN, ô Công ty để trống",
         "1. Chọn hàng H1\n2. Bấm Lưu",
         "",
         "- Bước 1: H1 vào bảng với Tổng số lượng 0\n"
         "- Bước 2: báo 'Thêm thất bại!', ô Công ty báo lỗi đỏ bắt buộc chọn"),

        ("012", "Chọn nhiều hàng cùng lúc", "P1",
         "Chọn Kho LN, Công ty TPE",
         "1. Chọn H1\n2. Chọn tiếp H2",
         "",
         "- Bảng có 2 hàng, STT 1 và 2\n- Dòng 'Tổng cộng' = tổng số lượng các vị trí của cả 2 hàng"),

        ("013", "Bỏ một hàng khỏi bảng", "P1",
         "Bảng đang có H1 và H2",
         "1. Bấm nút dấu trừ ở dòng H1",
         "",
         "- H1 bị bỏ khỏi bảng, H2 lên STT 1\n- Tổng cộng giảm tương ứng"),

        ("014", "Đổi kho khi bảng đã có hàng: chọn Xác nhận", "P0",
         "Đã chọn Kho LN, bảng có H1",
         "1. Đổi ô Kho sang kho khác\n2. Ở hộp thoại bấm 'Xác nhận'",
         "",
         "- Hiện hộp thoại 'Nếu bạn thay đổi kho, danh sách hàng hóa sẽ được làm mới!'\n"
         "- Xác nhận xong bảng hàng trống"),

        ("015", "Đổi kho khi bảng đã có hàng: chọn Hủy", "P1",
         "Đã chọn Kho LN, bảng có H1",
         "1. Đổi ô Kho sang kho khác\n2. Ở hộp thoại bấm 'Hủy'",
         "",
         "- Ô Kho trở lại LN\n- Bảng vẫn giữ H1"),

        ("016", "Đổi công ty khi bảng đã có hàng", "P1",
         "Đã chọn Kho LN, Công ty TPE, bảng có H1",
         "1. Đổi ô Công ty",
         "",
         "- Bảng hàng bị làm trống ngay, không hỏi xác nhận"),
    ]),

    ("IV", "Tạo mới: chia vị trí và số lượng", [
        ("001", "Nút chọn vị trí khóa khi chưa có kho", "P2",
         "Bảng có H1",
         "1. Quan sát nút kính lúp ở ô Vị trí",
         "",
         "- Nút bấm được khi đã có Kho và Đơn vị tính"),

        ("002", "Cửa sổ chọn vị trí chỉ có vị trí của kho đã chọn", "P0",
         "Chọn Kho LN, bảng có H1",
         "1. Bấm nút kính lúp ở ô Vị trí\n2. Xem danh sách vị trí",
         "",
         "- Chỉ có vị trí thuộc kho LN (V1, V2, V3), không có K1\n"
         "- Bấm mã V1 thì cửa sổ đóng, ô Vị trí hiện mã V1"),

        ("003", "Khai 1 vị trí đủ số lượng", "P0",
         "Bảng có H1, Tổng số lượng 100",
         "1. Chọn vị trí V1\n2. Giữ số lượng 100",
         "",
         "- Ô số lượng V1 là 100\n- Tổng cộng 100"),

        ("004", "Thêm vị trí bằng link 'Thêm kho'", "P0",
         "Bảng có H1, V1 đang 100",
         "1. Sửa số lượng V1 thành 60\n2. Bấm 'Thêm kho' dưới Tổng số lượng\n3. Chọn V2",
         "",
         "- Có thêm dòng vị trí mới\n- Ô số lượng dòng mới tự hiện 40, phần còn lại"),

        ("005", "Không nhập quá phần còn lại", "P0",
         "H1 Tổng 100, V1 đang 60, V2 đang trống",
         "1. Ở V2 gõ 70",
         "70",
         "- Ô V2 tự về 40, không vượt phần còn lại"),

        ("006", "Nhập số âm", "P2",
         "H1 có dòng V1",
         "1. Ở V1 gõ -5",
         "-5",
         "- Ô không nhận số âm, tự về phần còn lại"),

        ("007", "Chọn trùng vị trí trong cùng một hàng", "P0",
         "H1 đã có dòng V1",
         "1. Bấm 'Thêm kho'\n2. Ở dòng mới chọn lại V1",
         "",
         "- Báo 'Vị trí đã được chọn!'\n- Dòng mới vẫn trống vị trí"),

        ("008", "Hai hàng khác nhau dùng chung một vị trí", "P1",
         "Bảng có H1 và H2",
         "1. H1 chọn V1\n2. H2 cũng chọn V1",
         "",
         "- Cả 2 đều chọn được V1, không báo lỗi"),

        ("009", "Bỏ một dòng vị trí", "P1",
         "H1 có V1 60 và V2 40",
         "1. Bấm dấu x đỏ cạnh V2",
         "",
         "- Dòng V2 bị bỏ\n- Tổng cộng giảm 40"),

        ("010", "Dòng Tổng cộng cập nhật theo số nhập", "P1",
         "Bảng có H1 (V1 60, V2 40) và H2 (V1 10)",
         "1. Xem dòng Tổng cộng\n2. Sửa V1 của H1 thành 50",
         "",
         "- Bước 1: Tổng cộng 110\n- Bước 2: Tổng cộng còn 100"),

        ("011", "Chưa chọn vị trí mà bấm Lưu", "P0",
         "H1 có 1 dòng vị trí chưa chọn",
         "1. Bấm Lưu",
         "",
         "- Báo 'Thêm thất bại!'\n- Ô Vị trí báo lỗi đỏ bắt buộc chọn\n- Vẫn ở trang Tạo mới, dữ liệu còn nguyên"),

        ("012", "Tổng các vị trí nhỏ hơn Tổng số lượng", "P0",
         "H1 Tổng 100, có V1 60 và V2 40",
         "1. Bấm dấu x bỏ dòng V2\n2. Bấm Lưu",
         "",
         "- Báo 'Số lượng hàng hóa không khớp.' kèm mã H1\n- Không sinh dòng khai nào"),

        ("013", "Chưa chọn hàng nào mà bấm Lưu", "P1",
         "Đã chọn Kho, Công ty, bảng trống",
         "1. Bấm Lưu",
         "",
         "- Báo 'Thêm thất bại!', có lỗi đỏ dưới bảng hàng"),

        ("014", "Chưa chọn kho mà bấm Lưu", "P2",
         "Vừa mở trang Tạo mới",
         "1. Bấm Lưu",
         "",
         "- Báo 'Thêm thất bại!'\n- Ô Kho và ô Công ty báo lỗi đỏ bắt buộc chọn"),
    ]),

    ("V", "Tạo mới: lưu", [
        ("001", "Lưu khai báo hợp lệ", "P0",
         "Kho LN, Công ty TPE, H1 Tổng 100, V1 60, V2 40",
         "1. Bấm Lưu",
         "",
         "- Báo 'Thêm thành công!'\n- Quay về danh sách\n"
         "- Có 2 dòng H1: V1 60 Cái, V2 40 Cái, Người tạo là mình, Ngày tạo hôm nay"),

        ("002", "Lưu & Thêm", "P0",
         "Kho LN, Công ty TPE, bảng có H2 V1 10",
         "1. Bấm 'Lưu & Thêm'",
         "",
         "- Báo 'Thêm thành công!'\n- Vẫn ở trang Tạo mới, ô Kho trống, bảng hàng trống\n"
         "- Về danh sách thấy dòng H2 đã khai"),

        ("003", "Lưu nhiều hàng một lần", "P1",
         "Bảng có H1 (V1 100) và H2 (V2 10)",
         "1. Bấm Lưu",
         "",
         "- Danh sách có thêm 1 dòng H1 và 1 dòng H2"),

        ("004", "Hủy không lưu", "P1",
         "Bảng có H1 đã chọn vị trí",
         "1. Bấm 'Hủy'",
         "",
         "- Quay về danh sách\n- Không có dòng khai H1 mới"),

        ("005", "Hàng có giao dịch phát sinh trong lúc đang lập", "P1",
         "Tab 1 đang ở trang Tạo mới, đã chọn H1 kho LN công ty TPE",
         "1. Ở tab 2 lập phiếu nhập kho có H1 vào kho LN cho TPE\n2. Quay lại tab 1, bấm Lưu",
         "",
         "- Báo 'Hàng hóa' kèm tên H1 'đã có giao dịch, không thể nhập tồn đầu!'\n- Không sinh dòng khai"),

        ("006", "Hai người cùng khai một hàng", "P2",
         "Tab 1 và tab 2 cùng đã chọn H1 kho LN công ty TPE, cùng vị trí V1",
         "1. Tab 1 bấm Lưu\n2. Tab 2 bấm Lưu",
         "",
         "- Tab 1 thành công\n- Tab 2 báo 'Hàng hóa' kèm mã H1 'đã được thêm tồn kho! Vị trí:' kèm mã V1"),

        ("007", "Bấm Lưu liên tục", "P2",
         "Bảng có H1 hợp lệ",
         "1. Bấm Lưu 3 lần thật nhanh",
         "",
         "- Nút Lưu khóa và hiện biểu tượng xoay trong lúc chờ\n- Chỉ sinh đúng 1 bộ dòng khai"),

        ("008", "Gọi thẳng chức năng Thêm với vị trí của kho khác", "P1",
         "Tester kỹ thuật, tài khoản A",
         "1. Gọi thẳng chức năng Thêm: kho LN, công ty TPE, H1 số lượng 100, vị trí K1",
         "Vị trí K1 thuộc kho khác",
         "- Báo 'Thông tin vị trí không khớp!'\n- Không sinh dòng khai"),

        ("009", "Gọi thẳng chức năng Thêm với số lượng khác tồn kế toán", "P1",
         "Tester kỹ thuật. H1 khai kế toán 100 Cái",
         "1. Gọi thẳng chức năng Thêm: H1 tổng 80, V1 80",
         "",
         "- Hệ thống chặn vì khác số kế toán, giống luật của Import\n"
         "- Lỗi ERP đã biết: lưu thành công 80 Cái, chỉ giao diện mới khóa số lượng"),
    ]),

    ("VI", "Tạo mới: ghi tồn kho", [
        ("001", "Tồn kho vật lý tăng sau khi khai", "P0",
         "Ghi lại tồn của H1 tại kho LN trên báo cáo tồn kho trước khi khai (bằng 0)",
         "1. Khai H1: V1 60, V2 40\n2. Mở lại báo cáo tồn kho, lọc kho LN, hàng H1",
         "",
         "- Tồn H1 tại kho LN tăng đúng 100 Cái"),

        ("002", "Tồn theo vị trí tăng sau khi khai", "P0",
         "Như TC trên",
         "1. Mở màn xem tồn kho theo vị trí của kho LN\n2. Tìm H1",
         "",
         "- V1 có 60 Cái, V2 có 40 Cái"),

        ("003", "Đơn vị khác đơn vị cơ bản được quy đổi", "P1",
         "Khai H2 10 Hộp ở V1 (1 Hộp = 12 Cái)",
         "1. Xem tồn H2 trên báo cáo tồn kho theo đơn vị cơ bản",
         "",
         "- Tồn tăng 120 Cái (bằng 10 Hộp)"),

        ("004", "Sinh lô hàng tồn đầu để xuất kho", "P0",
         "Đã khai H1 V1 60, V2 40",
         "1. Lập phiếu xuất kho H1 từ kho LN cho TPE\n2. Mở cửa sổ chọn lô / vị trí xuất",
         "",
         "- Có lô số bắt đầu bằng 'TONDAUKHO-' ở V1 (60) và V2 (40)\n- Chọn lô xuất được bình thường"),

        ("005", "Tồn theo công ty ghi đúng công ty khai báo", "P1",
         "Tài khoản A thuộc TPE. Công ty X đã có tồn H4 ở kho LN từ trước. Khai H4 cho công ty TPE",
         "1. Khai H4 kho LN cho TPE\n2. Xem tồn H4 của từng công ty tại kho LN",
         "",
         "- Tồn của TPE tăng, tồn của X không đổi"),

        ("006", "Khai cho công ty khác công ty người đăng nhập", "P1",
         "Tài khoản A thuộc TPE, được thao tác công ty X. TPE đã có tồn H5 ở kho LN. Công ty X đã khai kế "
         "toán H5 ở kho LN, chưa có giao dịch",
         "1. Khai H5 kho LN cho công ty X\n2. Xem tồn H5 của từng công ty tại kho LN",
         "",
         "- Tồn của công ty X tăng, tồn của TPE không đổi\n"
         "- Lỗi ERP đã biết: tồn của TPE bị cộng thêm, công ty X không có tồn"),
    ]),

    ("VII", "Sửa khai báo", [
        ("001", "Mở trang Sửa", "P0",
         "Dòng H1 V1 60 chưa có giao dịch",
         "1. Bấm bánh răng dòng H1 V1, chọn 'Sửa'",
         "",
         "- Trang 'Sửa khai báo tồn đầu kỳ', khung 'Chi tiết'\n"
         "- Hàng hóa, Đơn vị, Kho, Vị trí hiện đúng và bị khóa\n- Chỉ ô Số lượng sửa được, đang là 60\n"
         "- Có nút Cập nhật và Hủy"),

        ("002", "Sửa số lượng thành công", "P0",
         "Trang Sửa dòng H1 V1 60",
         "1. Sửa Số lượng thành 50\n2. Bấm 'Cập nhật'",
         "50",
         "- Báo 'Cập nhật thành công!', quay về danh sách\n- Dòng H1 V1 hiện 50"),

        ("003", "Tồn kho đổi theo khi sửa", "P0",
         "Đã sửa H1 V1 từ 60 thành 50",
         "1. Xem báo cáo tồn kho H1 kho LN\n2. Xem tồn vị trí V1",
         "",
         "- Tồn H1 kho LN giảm 10\n- Tồn V1 còn 50"),

        ("004", "Sửa làm tổng khác tồn kế toán", "P0",
         "H1 khai kế toán 100, vật lý V1 60, V2 40",
         "1. Sửa V1 thành 70, bấm Cập nhật",
         "70",
         "- Hệ thống chặn vì tổng vật lý 110 khác kế toán 100\n"
         "- Lỗi ERP đã biết: cập nhật thành công, tổng vật lý thành 110"),

        ("005", "Số lượng để trống hoặc bằng 0", "P0",
         "Trang Sửa dòng H1 V1",
         "1. Xóa trắng ô Số lượng, bấm Cập nhật\n2. Gõ 0, bấm Cập nhật",
         "Trống, 0",
         "- Cả 2 lần báo 'Cập nhật thất bại!', lỗi đỏ dưới ô Số lượng\n- Dữ liệu không đổi"),

        ("006", "Số lượng âm", "P2",
         "Trang Sửa dòng H1 V1",
         "1. Gõ -10",
         "-10",
         "- Ô không nhận số âm"),

        ("007", "Hủy sửa", "P1",
         "Trang Sửa dòng H1 V1 60, đã gõ 30",
         "1. Bấm 'Hủy'",
         "",
         "- Quay về danh sách, dòng vẫn 60"),

        ("008", "Mở trang Sửa của dòng đã có giao dịch", "P0",
         "Đã sao chép đường dẫn trang Sửa dòng H1 V1. Sau đó H1 đã được xuất kho",
         "1. Dán lại đường dẫn trang Sửa",
         "",
         "- Ra trang không tìm thấy"),

        ("009", "Bấm Cập nhật khi hàng vừa có giao dịch", "P1",
         "Tab 1 mở trang Sửa dòng H1 V1. Tab 2 lập phiếu xuất kho H1",
         "1. Tab 1 sửa Số lượng, bấm Cập nhật",
         "",
         "- Báo 'Hàng hóa đã có giao dịch, không thể cập nhật tồn đầu!'\n- Dữ liệu không đổi"),

        ("010", "Tồn theo công ty đổi theo khi sửa", "P2",
         "Đã sửa H1 V1 từ 60 thành 50",
         "1. Xem tồn H1 của công ty TPE tại kho LN và tại vị trí V1",
         "",
         "- Cả 2 cùng giảm 10\n- Lỗi ERP đã biết: tồn theo công ty vẫn như trước khi sửa"),
    ]),

    ("VIII", "Xóa khai báo", [
        ("001", "Hộp thoại xác nhận xóa", "P0",
         "Dòng H1 V1 chưa có giao dịch",
         "1. Bấm bánh răng, chọn 'Xóa'",
         "",
         "- Hộp thoại 'Xác nhận xóa!' với nội dung 'Bạn chắc chắn muốn xóa bản ghi này?'"),

        ("002", "Hủy ở hộp thoại xóa", "P1",
         "Đang ở hộp thoại xác nhận xóa",
         "1. Bấm Hủy",
         "",
         "- Hộp thoại đóng, dòng vẫn còn"),

        ("003", "Xóa thành công", "P0",
         "Dòng H1 V2 40 chưa có giao dịch",
         "1. Chọn 'Xóa', xác nhận",
         "",
         "- Báo 'Xóa thành công!'\n- Dòng H1 V2 mất khỏi danh sách, dòng H1 V1 vẫn còn"),

        ("004", "Tồn kho giảm khi xóa", "P0",
         "Vừa xóa dòng H1 V2 40",
         "1. Xem tồn H1 kho LN\n2. Xem tồn vị trí V2\n3. Mở cửa sổ chọn lô ở phiếu xuất kho H1",
         "",
         "- Tồn H1 kho LN giảm 40\n- V2 không còn H1\n- Không còn lô 'TONDAUKHO-' ở V2"),

        ("005", "Xóa một vị trí làm lệch tồn kế toán", "P1",
         "H1 khai kế toán 100. Vật lý còn V1 60 sau khi xóa V2",
         "1. Vào Tạo mới, chọn Kho LN, Công ty TPE, chọn H1 để khai lại V2 40",
         "",
         "- Ghi nhận hành vi ERP: không khai lại được, báo 'Hàng hóa đã được khai báo tồn đầu kì'\n"
         "- Muốn khai lại phải xóa hết các vị trí của H1 rồi khai từ đầu"),

        ("006", "Xóa hết các vị trí rồi khai lại", "P1",
         "H1 chỉ còn dòng V1",
         "1. Xóa dòng V1\n2. Vào Tạo mới, chọn H1, khai V1 60, V2 40, Lưu",
         "",
         "- Bước 2 chọn được H1, lưu thành công\n- Tồn H1 kho LN đúng 100"),

        ("007", "Xóa khi hàng vừa có giao dịch", "P1",
         "Danh sách đang mở, dòng H1 còn nút Xóa. Ở tab khác vừa lập phiếu xuất kho H1",
         "1. Chọn 'Xóa' dòng H1, xác nhận",
         "",
         "- Báo 'Hàng hóa đã có giao dịch, không thể xóa tồn đầu!'\n- Dòng vẫn còn"),

        ("008", "Tồn vị trí theo công ty sau khi xóa", "P2",
         "Vừa xóa dòng H1 V2 40 của TPE",
         "1. Xem tồn vị trí V2 theo công ty TPE",
         "",
         "- Không còn H1 ở V2 của TPE\n- Lỗi ERP đã biết: hiện số âm -40"),
    ]),

    ("IX", "Khóa Sửa / Xóa theo giao dịch", [
        ("001", "Phiếu nhập kho làm khóa dòng khai", "P0",
         "H1 đã khai kho LN cho TPE",
         "1. Lập và duyệt phiếu nhập kho thêm H1 vào kho LN cho TPE\n2. Xem nút bánh răng dòng H1",
         "",
         "- Không còn Sửa / Xóa"),

        ("002", "Phiếu xuất đang lập cũng làm khóa", "P1",
         "H1 đã khai kho LN cho TPE",
         "1. Lập phiếu xuất kho H1 từ kho LN, chọn lô tồn đầu, chưa duyệt\n2. Xem dòng H1",
         "",
         "- Không còn Sửa / Xóa"),

        ("003", "Chuyển vị trí làm khóa", "P1",
         "H1 đã khai V1 60",
         "1. Lập phiếu chuyển vị trí H1 từ V1 sang V3\n2. Xem dòng H1",
         "",
         "- Không còn Sửa / Xóa"),

        ("004", "Giao dịch của công ty khác không làm khóa", "P1",
         "H1 đã khai kho LN cho TPE. Công ty X có phiếu nhập H1 vào kho LN",
         "1. Xem dòng H1 của TPE",
         "",
         "- Vẫn còn Sửa / Xóa"),

        ("005", "Giao dịch ở kho khác không làm khóa", "P2",
         "H1 đã khai kho LN cho TPE. TPE nhập H1 vào kho khác",
         "1. Xem dòng H1 kho LN",
         "",
         "- Vẫn còn Sửa / Xóa"),

        ("006", "Xuất từ lô của vị trí thứ 2", "P2",
         "H1 khai V1 60, V2 40. Lập và duyệt phiếu xuất kho H1 chỉ lấy lô tồn đầu ở V2",
         "1. Xem nút bánh răng các dòng H1",
         "",
         "- Không còn Sửa / Xóa ở cả 2 dòng\n- Lỗi ERP đã biết: vẫn còn Sửa / Xóa"),
    ]),

    ("X", "Import Excel", [
        ("001", "Mở cửa sổ Import và tải file mẫu", "P0",
         "Tài khoản A ở danh sách",
         "1. Bấm 'Import Excel'\n2. Bấm link '(File mẫu)'",
         "",
         "- Cửa sổ 'Import Excel' có ô 'Chọn file' bắt buộc, nút Import và Hủy\n"
         "- Tải về file mẫu có 7 cột: Tên hàng hóa, Mã hàng hóa, Đơn vị tính, Kho, Vị trí, Số lượng, Công ty "
         "và 1 dòng ví dụ"),

        ("002", "Import không chọn file", "P1",
         "Cửa sổ Import đang mở",
         "1. Bấm Import",
         "",
         "- Báo 'Import thất bại!', dưới ô báo 'Không được để trống'"),

        ("003", "Import file không phải Excel", "P1",
         "",
         "1. Chọn file .pdf\n2. Bấm Import",
         "File .pdf",
         "- Báo 'Import thất bại!', dưới ô báo 'Không hợp lệ'"),

        ("004", "Import file hợp lệ", "P0",
         "File: H1, mã H1, Cái, LN, V1, 100, TPE",
         "1. Chọn file, bấm Import",
         "",
         "- Báo 'Import thành công 1 bản ghi'\n- Cửa sổ đóng, danh sách tải lại có dòng H1 V1 100"),

        ("005", "Một hàng chia nhiều vị trí trên nhiều dòng", "P0",
         "File 2 dòng: H1 LN V1 60 TPE và H1 LN V2 40 TPE",
         "1. Import",
         "",
         "- 'Import thành công 2 bản ghi'\n- Danh sách có H1 V1 60 và H1 V2 40"),

        ("006", "Tổng các dòng khác tồn kế toán", "P0",
         "File 2 dòng: H1 V1 60, H1 V2 30 (kế toán 100)",
         "1. Import",
         "",
         "- 'Import thất bại!', mục 'Chi tiết' báo dòng đầu tiên của H1: 'Hàng hóa' kèm tên H1 'khác số "
         "lượng đã khai kho kế toán, không thể nhập tồn đầu!'\n- Không dòng nào được ghi"),

        ("007", "Hàng chưa khai tồn kế toán", "P0",
         "File 1 dòng: H3, LN, V1, 5, TPE",
         "1. Import",
         "",
         "- Báo dòng 2: 'Hàng hóa' kèm tên H3 'chưa khai kho kế toán, không thể nhập tồn đầu!'"),

        ("008", "Import theo đơn vị khác đơn vị kế toán", "P1",
         "H2 khai kế toán 10 Hộp (1 Hộp = 12 Cái). File: H2, Cái, LN, V1, 120, TPE",
         "1. Import",
         "",
         "- Thành công, dòng H2 V1 120 Cái\n- Tồn kho tăng 120 Cái"),

        ("009", "Hàng đã khai vật lý", "P0",
         "H1 đã khai kho LN cho TPE. File 1 dòng H1 LN V3 10 TPE",
         "1. Import",
         "",
         "- Báo dòng 2: 'Hàng hóa' kèm tên H1 'đã nhập tồn đầu, không thể nhập tiếp!'"),

        ("010", "Hàng đã có giao dịch", "P1",
         "H6 đã có phiếu nhập vào kho LN của TPE, chưa khai tồn đầu vật lý",
         "1. Import 1 dòng H6 kho LN TPE",
         "",
         "- Báo 'Hàng hóa' kèm tên H6 'đã có giao dịch, không thể nhập tồn đầu!'"),

        ("011", "Thiếu cột bắt buộc", "P0",
         "File 1 dòng thiếu Vị trí",
         "1. Import",
         "",
         "- Báo dòng 2: 'Thiếu trường bắt buộc'"),

        ("012", "Số lượng bằng 0", "P1",
         "File 1 dòng H1 đầy đủ, Số lượng 0",
         "1. Import",
         "",
         "- Báo 'Thiếu trường bắt buộc'"),

        ("013", "Công ty không tồn tại", "P1",
         "File 1 dòng, cột Công ty ghi 'ABCXYZ'",
         "1. Import",
         "",
         "- Báo 'Công ty không tồn tại'"),

        ("014", "Hàng không tồn tại hoặc tên lệch mã", "P0",
         "File 1: mã hàng không có thật. File 2: mã H1 nhưng tên ghi sai 1 ký tự",
         "1. Import file 1\n2. Import file 2",
         "",
         "- Cả 2 lần báo 'Hàng hóa không tồn tại'"),

        ("015", "Hàng đã bị xóa", "P2",
         "Hàng H7 đã bị xóa khỏi danh mục hàng hóa",
         "1. Import 1 dòng H7",
         "",
         "- Báo 'Hàng hóa đã bị xoá'"),

        ("016", "Đơn vị tính sai", "P1",
         "File 1: Đơn vị 'Thùng ABC' không có thật. File 2: đơn vị có thật nhưng H1 không dùng",
         "1. Import file 1\n2. Import file 2",
         "",
         "- File 1: 'Đơn vị không tồn tại'\n- File 2: 'Hàng hóa với đơn vị đã nhập không tồn tại'"),

        ("017", "Kho hoặc vị trí sai", "P0",
         "File 1: mã kho không có thật. File 2: kho LN, vị trí K1 của kho khác",
         "1. Import file 1\n2. Import file 2",
         "",
         "- File 1: 'Kho không tồn tại'\n- File 2: 'Vị trí không tồn tại trong kho'"),

        ("018", "Một dòng lỗi thì cả file không ghi", "P0",
         "File 3 dòng: dòng 2 và 3 hợp lệ, dòng 4 mã kho sai",
         "1. Import\n2. Xem danh sách",
         "",
         "- 'Import thất bại!', 'Không hợp lệ: 1 bản ghi', bấm vào thấy '- Dòng 4: Kho không tồn tại'\n"
         "- Danh sách không có dòng nào của dòng 2, 3"),

        ("019", "Một dòng nhiều lỗi", "P2",
         "File 1 dòng: mã hàng sai, mã kho sai, công ty sai",
         "1. Import",
         "",
         "- Dòng 2 liệt kê đủ các lỗi, ngăn bằng dấu phẩy"),

        ("020", "File quá 200 dòng", "P1",
         "File 201 dòng dữ liệu",
         "1. Import",
         "201 dòng",
         "- Báo 'Số lượng bản ghi không vượt quá 200'\n- Không dòng nào được ghi"),

        ("021", "Dòng trống giữa file được bỏ qua", "P2",
         "File: dòng 2 hợp lệ, dòng 3 trống hết, dòng 4 hợp lệ",
         "1. Import",
         "",
         "- 'Import thành công 2 bản ghi'"),

        ("022", "Hai dòng trùng hàng và trùng vị trí", "P2",
         "File 2 dòng: H1 LN V1 60 TPE và H1 LN V1 40 TPE",
         "1. Import\n2. Lọc H1",
         "",
         "- Hệ thống chặn trùng vị trí như ở trang Tạo mới\n"
         "- Lỗi ERP đã biết: import thành công, danh sách có 2 dòng H1 cùng V1"),

        ("023", "Đóng cửa sổ thì xóa thông báo lỗi cũ", "P2",
         "Vừa import lỗi, cửa sổ đang hiện mục 'Chi tiết'",
         "1. Bấm Hủy\n2. Mở lại 'Import Excel'",
         "",
         "- Ô chọn file trống, không còn thông báo lỗi cũ"),

        ("024", "Import ghi tồn kho", "P1",
         "Vừa import thành công H1 V1 60, V2 40",
         "1. Xem báo cáo tồn kho H1 kho LN\n2. Xem lô ở phiếu xuất kho",
         "",
         "- Tồn tăng 100\n- Có lô 'TONDAUKHO-' ở V1 và V2, giống khai bằng trang Tạo mới"),
    ]),

    ("XI", "Xuất Excel", [
        ("001", "Xuất dưới 300 dòng", "P0",
         "Lọc Kho LN, ra dưới 300 dòng",
         "1. Bấm 'Xuất Excel'",
         "",
         "- Tải ngay file 'Khai_bao_ton_dau_vat_ly.xlsx'\n"
         "- Cột: Tên hàng, Mã hàng, Kho, Vị trí, Công ty, ĐVT, Số lượng, Người nhập, Ngày nhập\n"
         "- Số dòng bằng số dòng đang lọc trên màn"),

        ("002", "File xuất theo đúng bộ lọc", "P0",
         "Lọc Mã hàng H1",
         "1. Xuất Excel",
         "",
         "- File chỉ có các dòng H1"),

        ("003", "Xuất từ 300 dòng trở lên", "P1",
         "Không lọc, danh sách từ 300 dòng trở lên. Tài khoản có email",
         "1. Bấm 'Xuất Excel'\n2. Kiểm tra hộp thư",
         "",
         "- Báo 'Danh sách sẽ được gửi về mail sau ít phút!'\n- Sau ít phút email nhận được file"),

        ("004", "File xuất theo phạm vi xem", "P1",
         "Tài khoản C chỉ có quyền xem theo công ty TPE",
         "1. Đăng nhập C, bấm Xuất Excel",
         "",
         "- File chỉ có dòng của TPE, cột Công ty đều là TPE"),

        ("005", "Định dạng số lượng và ngày trong file", "P2",
         "Có dòng số lượng 1250",
         "1. Xuất Excel, mở file",
         "",
         "- Số lượng hiện có dấu phân cách hàng nghìn\n- Ngày nhập dạng ngày/tháng/năm"),
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
