"""Generate testcase Excel (ngôn ngữ người dùng) cho màn Sổ Nhật ký chung."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

OUTPUT_FILE  = ".plans/so-nhat-ky-chung-hrm/testcase.xlsx"
SHEET_NAME   = "SoNhatKyChung"
FEATURE_NAME = "Sổ Nhật ký chung (S03a-DN)"
MODULE_NAME  = "Kế toán"

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Sổ Nhật ký chung là báo cáo kế toán liệt kê toàn bộ các bút toán phát sinh theo trình tự thời gian (mẫu S03a-DN theo Thông tư 99/2025). "
     "Kế toán dùng màn này để: tra soát các nghiệp vụ đã ghi sổ, kiểm tra tính cân đối Nợ = Có, lọc theo kỳ / công ty / tài khoản, in sổ và xuất Excel."),
    ("2. Đối tượng được tính / hiển thị",
     "► Mỗi dòng = một bút toán (một dòng ghi Nợ hoặc ghi Có) đã được ghi sổ, thuộc công ty và kỳ đang lọc.\n"
     "► 20 cột: STT dòng, Ngày ghi sổ, Số CT, Ngày CT, Diễn giải, Số hiệu TK, Phát sinh Nợ, Phát sinh Có, "
     "Mã phí, Đối tượng, Vụ việc, Hợp đồng, Hàng hóa, Loại tiền, Tỷ giá, GD nội bộ, Công ty, Phòng ban, Bộ phận, Nhân viên.\n"
     "► Cột nào chứng từ chưa nhập thông tin thì để trống (không phải lỗi)."),
    ("3. Đối tượng bị ẩn / không tính",
     "► Bút toán không thuộc kỳ (Từ ngày – Đến ngày) đang lọc.\n"
     "► Bút toán không thuộc công ty đang chọn.\n"
     "► Các bút toán không thoả điều kiện lọc nâng cao (tài khoản, đối tượng, số tiền…) đang áp dụng."),
    ("4. Bộ lọc thời gian áp dụng cho",
     "Lọc theo NGÀY GHI SỔ. Người dùng chọn nhanh 'Kỳ báo cáo' (Cả năm / Quý / Tháng) để tự điền Từ – Đến ngày, "
     "hoặc tự chọn Từ ngày – Đến ngày. Ngày hiển thị dạng ngày/tháng/năm (VD 06/01/2026)."),
    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Danh sách phẳng theo thời gian (không phân cấp). Sắp xếp mặc định: Ngày ghi sổ tăng dần → theo chứng từ → dòng Nợ trước, Có sau. "
     "Bảng có phân trang; có thể bấm tiêu đề cột để sắp xếp."),
    ("6. Quy tắc cộng dồn / deduplicate",
     "► Dòng 'Cộng phát sinh': tổng Phát sinh Nợ và tổng Phát sinh Có của TOÀN BỘ kết quả lọc (mọi trang), KHÔNG phải chỉ trang đang xem.\n"
     "► 'Số lũy kế kỳ trước chuyển sang' (tuỳ chọn): tổng phát sinh của các bút toán TRƯỚC 'Từ ngày' theo cùng điều kiện lọc."),
    ("7. Phân quyền cấp",
     "• Xem sổ nhật ký chung — quyền để xem được dữ liệu báo cáo. Không có quyền này thì không xem được nội dung sổ.\n"
     "(Tile 'Kế toán' ở màn chọn phân hệ hiển thị cho mọi người dùng; quyền chỉ chặn ở bước xem dữ liệu sổ.)"),
    ("8. Cách tính các ô thống kê",
     "► Ô 'Cộng phát sinh — Nợ' = tổng cột Phát sinh Nợ của toàn bộ kết quả lọc.\n"
     "► Ô 'Cộng phát sinh — Có' = tổng cột Phát sinh Có của toàn bộ kết quả lọc.\n"
     "► Nhãn 'CÂN ĐỐI' hiện khi Tổng Nợ = Tổng Có; ngược lại hiện 'LỆCH <số chênh lệch>'.\n"
     "► 'Số lũy kế kỳ trước' = tổng Nợ / tổng Có các bút toán trước Từ ngày (cùng điều kiện lọc)."),
    ("9. Ghi chú đọc bảng",
     "► Bảng phân trang, chọn số dòng/trang. Số tiền hiển thị có dấu phân cách hàng nghìn.\n"
     "► 8 cột chuẩn (STT dòng, Ngày ghi sổ, Số CT, Ngày CT, Diễn giải, Số hiệu TK, Phát sinh Nợ, Phát sinh Có) luôn hiển thị, cố định ở đầu bảng.\n"
     "► 12 cột còn lại có thể ẩn/hiện và sắp xếp qua nút 'Cấu hình cột'.\n"
     "► Cài đặt cột và cài đặt bộ lọc được lưu lại theo máy/người dùng."),
]

HAS_ROLE_SECTION = True
ROLE_TCS = [
    ("01", "Người dùng CÓ quyền 'Xem sổ nhật ký chung'", "P0",
     "Tài khoản được gán quyền 'Xem sổ nhật ký chung'; đã đăng nhập.",
     "1. Vào phân hệ Kế toán\n2. Mở menu 'Sổ nhật ký chung'\n3. Quan sát bảng dữ liệu",
     "User: có quyền xem sổ",
     "- Màn hình mở, bảng hiển thị các bút toán của kỳ mặc định.\n- Không có thông báo chặn quyền.",
     "Quyền: Xem sổ nhật ký chung"),
    ("02", "Người dùng KHÔNG có quyền 'Xem sổ nhật ký chung'", "P0",
     "Tài khoản KHÔNG được gán quyền 'Xem sổ nhật ký chung'; đã đăng nhập.",
     "1. Vào phân hệ Kế toán\n2. Mở menu 'Sổ nhật ký chung'\n3. Quan sát",
     "User: không có quyền xem sổ",
     "- Không xem được nội dung sổ (bảng không tải dữ liệu / báo không có quyền).",
     "Quyền: Xem sổ nhật ký chung"),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", [
        ("001", "Vào màn Sổ nhật ký chung từ menu Kế toán", "P0",
         "Đã đăng nhập, có quyền xem sổ.",
         "1. Ở màn chọn phân hệ bấm ô 'Kế toán'\n2. Vào trang Tổng quan Kế toán\n3. Bấm menu trái 'Sổ nhật ký chung'",
         "User bất kỳ có quyền",
         "- Mở đúng màn 'Sổ nhật ký chung'.\n- Có khối Bộ lọc phía trên, bảng dữ liệu phía dưới.",
         "Điều hướng cơ bản"),
        ("002", "Vào phân hệ Kế toán từ dropdown cạnh chuông thông báo", "P1",
         "Đã đăng nhập, đang ở một phân hệ bất kỳ.",
         "1. Bấm icon lưới (ô vuông) cạnh chuông thông báo\n2. Bấm ô 'Kế toán'",
         "—",
         "- Chuyển sang phân hệ Kế toán, vào màn Tổng quan Kế toán.",
         "Dropdown chuyển phân hệ"),
        ("003", "Kỳ báo cáo mặc định khi vừa mở màn", "P1",
         "Vừa mở màn Sổ nhật ký chung lần đầu.",
         "1. Quan sát ô 'Kỳ báo cáo' và Từ/Đến ngày\n2. Quan sát bảng",
         "Năm hiện tại",
         "- 'Kỳ báo cáo' mặc định là 'Cả năm', Từ ngày = 01/01 và Đến ngày = 31/12 của năm hiện tại.\n- Bảng hiển thị dữ liệu theo kỳ đó.",
         "Mặc định kỳ = cả năm hiện tại"),
        ("004", "Bảng hiển thị đủ các cột theo mẫu S03a-DN", "P1",
         "Đang ở màn, có dữ liệu.",
         "1. Quan sát tiêu đề các cột của bảng",
         "—",
         "- Có 8 cột chuẩn ở đầu: STT dòng, Ngày ghi sổ, Số CT, Ngày CT, Diễn giải, Số hiệu TK, Phát sinh Nợ, Phát sinh Có.\n- Tiếp theo là các cột chi tiết (Mã phí, Đối tượng, Vụ việc, Hợp đồng, Hàng hóa, Loại tiền, Tỷ giá, GD nội bộ, Công ty, Phòng ban, Bộ phận, Nhân viên).",
         "20 cột theo mẫu"),
    ]),
    ("II", "BỘ LỌC & TÌM KIẾM", [
        ("001", "Chọn Kỳ báo cáo là một Tháng", "P0",
         "Đang ở màn, có dữ liệu nhiều tháng.",
         "1. Mở 'Kỳ báo cáo' chọn 'Tháng 7'\n2. Quan sát Từ/Đến ngày và bảng",
         "Tháng 7 năm hiện tại",
         "- Từ ngày tự điền 01/07, Đến ngày 31/07.\n- Bảng chỉ còn bút toán trong tháng 7.",
         "Kỳ báo cáo tự set Từ–Đến ngày"),
        ("002", "Chọn Kỳ báo cáo là một Quý", "P1",
         "Đang ở màn, có dữ liệu cả năm.",
         "1. Mở 'Kỳ báo cáo' chọn 'Quý 1'\n2. Quan sát Từ/Đến ngày",
         "Quý 1",
         "- Từ ngày 01/01, Đến ngày 31/03.\n- Bảng chỉ còn bút toán trong quý 1.",
         "Quý = 3 tháng"),
        ("003", "Tự chọn Từ ngày – Đến ngày", "P0",
         "Đang ở màn.",
         "1. Chọn Từ ngày = 01/03/2026\n2. Chọn Đến ngày = 31/03/2026\n3. Quan sát bảng",
         "01/03/2026 – 31/03/2026",
         "- Bảng chỉ hiện bút toán có Ngày ghi sổ trong khoảng đó.\n- 'Kỳ báo cáo' tự chuyển thành 'Tùy chọn'.",
         "Lọc theo Ngày ghi sổ"),
        ("004", "Ngày hiển thị đúng định dạng ngày/tháng/năm", "P1",
         "Bảng có dữ liệu.",
         "1. Quan sát cột 'Ngày ghi sổ' và 'Ngày CT'",
         "—",
         "- Hiển thị dạng dd/mm/yyyy (VD 06/01/2026), không phải yyyy-mm-dd.",
         "Định dạng ngày d/m/Y"),
        ("005", "Lọc theo Công ty", "P0",
         "Có dữ liệu của nhiều công ty.",
         "1. Chọn 'Công ty' = một công ty cụ thể\n2. Quan sát bảng",
         "Công ty A",
         "- Bảng chỉ còn bút toán thuộc công ty đã chọn.",
         "Bộ lọc công ty"),
        ("006", "Lọc phân cấp Công ty → Phòng ban → Bộ phận → Nhân viên", "P1",
         "Có dữ liệu gắn phòng ban / nhân viên.",
         "1. Chọn Công ty\n2. Chọn Phòng ban trong công ty đó\n3. Chọn Bộ phận, rồi Nhân viên\n4. Quan sát bảng",
         "Công ty A → PB Kế toán → NV X",
         "- Danh sách Phòng ban chỉ hiện phòng của công ty đã chọn; tương tự Bộ phận theo phòng, Nhân viên theo bộ phận.\n- Đổi cấp trên thì cấp dưới được xoá chọn lại.\n- Bảng lọc đúng theo lựa chọn.",
         "Cascade tổ chức"),
        ("007", "Lọc theo Tài khoản (bao gồm tài khoản con)", "P0",
         "Có bút toán ở TK 331 và các TK con 3311, 3312…",
         "1. Nhập/chọn Tài khoản = 331\n2. Quan sát bảng",
         "TK 331",
         "- Bảng hiện bút toán của 331 và cả các tài khoản con (3311, 3312, …).",
         "TK tổng gồm TK con"),
        ("008", "Tìm nhanh theo Số CT / Diễn giải / Số hiệu TK", "P1",
         "Bảng có nhiều bút toán.",
         "1. Gõ từ khoá vào ô tìm nhanh (VD số chứng từ)\n2. Quan sát",
         "Từ khoá: PN-001",
         "- Bảng chỉ còn dòng khớp từ khoá ở Số CT hoặc Diễn giải hoặc Số hiệu TK.",
         "Quick search"),
        ("009", "Lọc theo khoảng Số tiền (từ – đến)", "P2",
         "Có bút toán nhiều mức tiền.",
         "1. Nhập 'Số tiền từ' và 'Số tiền đến'\n2. Quan sát",
         "Từ 1.000.000 đến 50.000.000",
         "- Chỉ còn bút toán có số tiền (Nợ hoặc Có) nằm trong khoảng.",
         "Lọc theo số tiền"),
        ("010", "Lọc theo Giao dịch nội bộ (Y/N)", "P2",
         "Có bút toán nội bộ và bên ngoài.",
         "1. Chọn 'GD nội bộ' = Có\n2. Quan sát",
         "GD nội bộ = Có",
         "- Chỉ còn bút toán là giao dịch nội bộ.",
         "Cờ GD nội bộ"),
        ("011", "Bật 'Số lũy kế kỳ trước chuyển sang'", "P1",
         "Có bút toán phát sinh trước 'Từ ngày' đang lọc.",
         "1. Mở Tìm kiếm nâng cao\n2. Tick 'Số lũy kế kỳ trước chuyển sang'\n3. Quan sát khối tổng",
         "Từ ngày = 01/07/2026",
         "- Hiện thêm số lũy kế Nợ/Có của các bút toán trước 01/07 (cùng điều kiện lọc).",
         "Lũy kế đầu kỳ kiểu MISA"),
        ("012", "Nút 'Nhập lại' (reset) bộ lọc", "P1",
         "Đã đổi nhiều điều kiện lọc.",
         "1. Bấm 'Nhập lại'\n2. Quan sát",
         "—",
         "- Các điều kiện lọc trở về mặc định (kỳ = cả năm hiện tại), bảng tải lại.",
         "Reset bộ lọc"),
        ("013", "Ẩn / hiện khu vực bộ lọc", "P2",
         "Đang ở màn.",
         "1. Bấm nút thu gọn/mở khu bộ lọc\n2. Quan sát",
         "—",
         "- Khu bộ lọc ẩn đi để xem bảng rộng hơn; bấm lại thì hiện lại.",
         "Toggle panel"),
    ]),
    ("III", "TỔNG & CÂN ĐỐI", [
        ("001", "Dòng 'Cộng phát sinh' là tổng toàn bộ kết quả lọc", "P0",
         "Kết quả lọc có nhiều trang.",
         "1. Xem 'Cộng phát sinh' Nợ/Có\n2. Chuyển sang trang khác\n3. Xem lại 'Cộng phát sinh'",
         "Kết quả > 1 trang",
         "- 'Cộng phát sinh' KHÔNG đổi khi chuyển trang (luôn là tổng của toàn bộ kết quả lọc, không chỉ trang đang xem).",
         "Tổng toàn tập, không theo trang"),
        ("002", "Nhãn 'CÂN ĐỐI' khi Tổng Nợ = Tổng Có", "P0",
         "Kỳ có dữ liệu cân đối.",
         "1. Lọc một kỳ có Nợ = Có\n2. Quan sát nhãn cạnh Cộng phát sinh",
         "Kỳ cân đối",
         "- Hiển thị nhãn 'CÂN ĐỐI'.",
         "Nợ = Có → cân đối"),
        ("003", "Nhãn 'LỆCH' khi Tổng Nợ ≠ Tổng Có", "P1",
         "Kỳ có dữ liệu lệch.",
         "1. Lọc kỳ có Nợ ≠ Có\n2. Quan sát nhãn",
         "Kỳ lệch",
         "- Hiển thị 'LỆCH' kèm số chênh lệch.",
         "Nợ ≠ Có → lệch"),
        ("004", "Vị trí khối 'Cộng phát sinh'", "P2",
         "Có dữ liệu.",
         "1. Quan sát vị trí khối tổng",
         "—",
         "- Khối 'Cộng phát sinh / Cân đối' nằm gọn trong khung bảng, ở đầu bảng.",
         "Bố cục"),
    ]),
    ("IV", "BẢNG DỮ LIỆU & PHÂN TRANG", [
        ("001", "Số tiền có phân cách hàng nghìn", "P1",
         "Có bút toán số tiền lớn.",
         "1. Quan sát cột Phát sinh Nợ / Có",
         "—",
         "- Số tiền hiển thị có dấu phân cách nghìn (VD 50.000.000).",
         "Định dạng số"),
        ("002", "Ô Nợ hoặc Có để trống khi bằng 0", "P2",
         "Bút toán chỉ ghi Nợ hoặc chỉ ghi Có.",
         "1. Quan sát 1 dòng ghi Nợ",
         "—",
         "- Cột Phát sinh Nợ có số, cột Phát sinh Có để trống (không hiện số 0).",
         "Trống thay vì 0"),
        ("003", "Đổi số dòng / trang", "P1",
         "Kết quả nhiều dòng.",
         "1. Đổi 'Số dòng/trang' sang 50\n2. Quan sát",
         "50 dòng/trang",
         "- Bảng hiển thị tối đa 50 dòng mỗi trang.",
         "Page size"),
        ("004", "Chuyển trang", "P1",
         "Kết quả nhiều trang.",
         "1. Bấm sang trang 2\n2. Quan sát",
         "—",
         "- Hiện nhóm dòng của trang 2; STT dòng chạy tiếp tục đúng thứ tự.",
         "Phân trang"),
        ("005", "Sắp xếp theo cột (bấm tiêu đề)", "P2",
         "Bảng có dữ liệu.",
         "1. Bấm tiêu đề cột 'Ngày ghi sổ'\n2. Quan sát",
         "—",
         "- Dữ liệu sắp xếp theo cột đã bấm (tăng/giảm dần).",
         "Sort cột"),
        ("006", "Không có dữ liệu phù hợp", "P1",
         "Chọn kỳ/điều kiện không có bút toán nào.",
         "1. Lọc một kỳ tương lai không có dữ liệu\n2. Quan sát",
         "Kỳ trống",
         "- Bảng hiện thông báo 'Không có dữ liệu phù hợp'.\n- Cộng phát sinh = 0.",
         "Empty state"),
    ]),
    ("V", "CẤU HÌNH CỘT & CÀI ĐẶT BỘ LỌC", [
        ("001", "Mở 'Cấu hình cột'", "P1",
         "Đang ở màn.",
         "1. Bấm nút 'Cấu hình cột'\n2. Quan sát hộp thoại",
         "—",
         "- Hộp thoại 'Cấu hình cột hiển thị' mở ra, gồm 2 khối: 8 cột chuẩn (cố định, bắt buộc) và các cột mở rộng tích chọn/kéo.",
         "Modal cấu hình cột"),
        ("002", "Ẩn một cột mở rộng", "P1",
         "Đang mở hộp cấu hình cột.",
         "1. Bỏ tích cột 'Tỷ giá'\n2. Bấm 'Lưu'\n3. Quan sát bảng",
         "Bỏ cột Tỷ giá",
         "- Cột 'Tỷ giá' biến mất khỏi bảng; các cột khác giữ nguyên.",
         "Ẩn cột"),
        ("003", "8 cột chuẩn không thể ẩn", "P0",
         "Đang mở hộp cấu hình cột.",
         "1. Quan sát khối 8 cột chuẩn",
         "—",
         "- 8 cột chuẩn hiển thị dạng khoá (không cho bỏ tích), luôn cố định ở đầu bảng.",
         "8 cột S03a-DN bắt buộc"),
        ("004", "Kéo sắp xếp lại thứ tự cột mở rộng", "P2",
         "Đang mở hộp cấu hình cột.",
         "1. Kéo 'Nhân viên' lên trên 'Công ty'\n2. Lưu\n3. Quan sát bảng",
         "—",
         "- Thứ tự các cột mở rộng thay đổi theo thao tác kéo.",
         "Kéo-thả thứ tự"),
        ("005", "Cấu hình cột được lưu sau khi tải lại trang", "P1",
         "Đã lưu một cấu hình cột (ẩn vài cột).",
         "1. Tải lại trang (F5)\n2. Quan sát bảng",
         "—",
         "- Cấu hình cột được giữ nguyên như đã lưu.",
         "Lưu cấu hình"),
        ("006", "Mở 'Cài đặt bộ lọc'", "P1",
         "Đang ở màn.",
         "1. Bấm 'Cài đặt bộ lọc'\n2. Quan sát hộp thoại",
         "—",
         "- Hộp thoại mở, liệt kê các trường lọc với ô tích 'hiển thị mặc định'. Từ ngày / Đến ngày bị khoá (bắt buộc mặc định).",
         "Modal cài đặt bộ lọc"),
        ("007", "Đưa một trường vào 'mặc định'", "P1",
         "Đang mở hộp cài đặt bộ lọc.",
         "1. Tích 'GD nội bộ'\n2. Bấm 'Lưu'\n3. Quan sát khu bộ lọc",
         "Tích GD nội bộ",
         "- Trường 'GD nội bộ' hiển thị ngay ở khu lọc mặc định (không cần mở Tìm kiếm nâng cao).",
         "Trường mặc định"),
        ("008", "Trường không tích nằm trong 'Tìm kiếm nâng cao'", "P2",
         "Một trường không được tích mặc định.",
         "1. Đảm bảo 'Hợp đồng' không tích\n2. Đóng cài đặt\n3. Xem khu lọc khi chưa mở nâng cao",
         "—",
         "- Trường 'Hợp đồng' chỉ hiện khi bấm 'Tìm kiếm nâng cao'.",
         "Trường nâng cao"),
        ("009", "Khôi phục cài đặt bộ lọc mặc định", "P2",
         "Đã đổi cài đặt bộ lọc.",
         "1. Mở 'Cài đặt bộ lọc'\n2. Bấm 'Khôi phục mặc định'",
         "—",
         "- Danh sách trường mặc định trở về ban đầu.",
         "Reset cài đặt lọc"),
        ("010", "Cài đặt bộ lọc được lưu sau khi tải lại trang", "P1",
         "Đã lưu cài đặt bộ lọc.",
         "1. Tải lại trang\n2. Quan sát khu lọc",
         "—",
         "- Các trường mặc định giữ đúng như đã cài.",
         "Lưu cài đặt lọc"),
    ]),
    ("VI", "IN & XUẤT EXCEL", [
        ("001", "Xuất Excel theo đúng bộ lọc đang xem", "P0",
         "Đang lọc một kỳ/điều kiện cụ thể, có dữ liệu.",
         "1. Bấm 'Xuất Excel'\n2. Mở file tải về",
         "Kỳ Tháng 7, Công ty A",
         "- Tải về file .xlsx.\n- Nội dung khớp đúng bộ lọc đang xem; có dòng 'Cộng phát sinh' và dòng cân đối.",
         "Excel theo bộ lọc"),
        ("002", "In sổ mẫu S03a-DN", "P0",
         "Đang lọc kỳ có dữ liệu.",
         "1. Bấm 'In S03a-DN'\n2. Quan sát trang in",
         "Kỳ có dữ liệu",
         "- Mở trang in theo mẫu S03a-DN (9 cột chuẩn: Ngày ghi sổ, Số hiệu CT, Ngày CT, Diễn giải, Đã ghi Sổ Cái, STT dòng, TK đối ứng, Nợ, Có), có dòng 'Cộng phát sinh' và khối chữ ký.",
         "Mẫu in chuẩn TT99"),
        ("003", "Tổng ở file in/Excel khớp với dòng in ra", "P1",
         "Kỳ có dữ liệu.",
         "1. Xuất Excel / In\n2. Cộng tay vài dòng đối chiếu 'Cộng phát sinh'",
         "—",
         "- Dòng 'Cộng phát sinh' bằng tổng các dòng thực tế trong file (không lệch).",
         "Tổng khớp dòng in"),
        ("004", "Trang in không dính menu / sidebar", "P2",
         "Mở trang in.",
         "1. Xem preview in",
         "—",
         "- Trang in sạch (chỉ nội dung sổ), không có thanh menu/sidebar của hệ thống.",
         "Bố cục trang in"),
    ]),
    ("VII", "EDGE CASES & KIỂM TRA THÊM", [
        ("001", "Chọn Từ ngày > Đến ngày", "P1",
         "Đang ở màn.",
         "1. Chọn Từ ngày = 20/07/2026, Đến ngày = 13/07/2026\n2. Quan sát",
         "Ngược ngày",
         "- Hệ thống không cho ra kết quả sai; cần cảnh báo/không lọc (đối chiếu quy tắc nghiệp vụ nếu đã áp dụng chặn ngược ngày).",
         "Chặn/khoanh vùng ngược ngày"),
        ("002", "Kỳ có rất nhiều bút toán (hiệu năng)", "P2",
         "Kỳ có hàng nghìn dòng.",
         "1. Lọc kỳ rộng (cả năm, mọi công ty)\n2. Quan sát thời gian tải",
         "Cả năm",
         "- Bảng tải trong thời gian chấp nhận được, phân trang mượt.",
         "Hiệu năng"),
        ("003", "Cột chi tiết trống khi chứng từ chưa nhập", "P2",
         "Có bút toán chưa nhập Mã phí / Vụ việc.",
         "1. Quan sát các cột chi tiết",
         "—",
         "- Ô để trống, không hiện lỗi. Đây là hành vi đúng.",
         "Cột khuyết để trống"),
        ("004", "Số CT hiển thị dạng chữ (chưa có link)", "P2",
         "Có bút toán gắn chứng từ.",
         "1. Quan sát cột 'Số CT'",
         "—",
         "- Số CT hiển thị dạng chữ (bản này chưa có liên kết mở chứng từ gốc).",
         "Số CT text"),
    ]),
]

# ===== STYLES =====
THIN   = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
DESC_LABEL_FONT = Font(name="Calibri", size=11, bold=True)
DESC_LABEL_FILL = PatternFill("solid", fgColor="FFF2CC")
DESC_BODY_FONT  = Font(name="Calibri", size=11)
WRAP_TOP_LEFT   = Alignment(wrap_text=True, vertical="top", horizontal="left")
WRAP_TOP_CENTER = Alignment(wrap_text=True, vertical="top", horizontal="center")
TITLE_FONT = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
TITLE_FILL = PatternFill("solid", fgColor="4472C4")
SUMMARY_LABEL_FONT = Font(name="Calibri", size=11, bold=True)
SUMMARY_LABEL_FILL = PatternFill("solid", fgColor="D9E1F2")
SUMMARY_VALUE_FONT = Font(name="Calibri", size=11, bold=True)
SUMMARY_VALUE_ALIGN = Alignment(horizontal="center", vertical="center")
HEADER_FONT = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
HEADER_FILL = PatternFill("solid", fgColor="4472C4")
HEADER_ALIGN = Alignment(wrap_text=True, vertical="center", horizontal="center")
SECTION_FONT = Font(name="Calibri", size=12, bold=True, color="1F4E79")
SECTION_FILL = PatternFill("solid", fgColor="D6E4F0")
SECTION_ALIGN = Alignment(wrap_text=True, vertical="center", horizontal="left", indent=1)
EVEN_FILL = PatternFill("solid", fgColor="F2F2F2")
COL_WIDTHS = {'A':18,'B':24,'C':14,'D':44,'E':9,'F':34,'G':52,'H':22,'I':60,'J':30,'K':16,'L':15,'M':15,'N':15,'O':20}

wb = Workbook(); ws = wb.active; ws.title = SHEET_NAME
for col, w in COL_WIDTHS.items():
    ws.column_dimensions[col].width = w

ws.cell(1, 1, "MÔ TẢ TÍNH NĂNG (đọc trước khi xem testcase)").font = Font(bold=True, size=12)
ws.merge_cells("B1:O1"); ws.row_dimensions[1].height = 22
for idx, (label, body) in enumerate(DESCRIPTION_BLOCK, start=2):
    a = ws.cell(idx, 1, label); a.font=DESC_LABEL_FONT; a.fill=DESC_LABEL_FILL; a.alignment=WRAP_TOP_LEFT; a.border=BORDER
    b = ws.cell(idx, 2, body); b.font=DESC_BODY_FONT; b.alignment=WRAP_TOP_LEFT; b.border=BORDER
    ws.merge_cells(start_row=idx, start_column=2, end_row=idx, end_column=15)
    ws.row_dimensions[idx].height = max(40, body.count("\n")*16 + 30)

t = ws.cell(11, 1, f"Testcase _ {FEATURE_NAME}"); t.font=TITLE_FONT; t.fill=TITLE_FILL
t.alignment = Alignment(vertical="center", horizontal="left", indent=1)
ws.merge_cells("B11:E11"); ws.merge_cells("F11:H11")
fs = ws.cell(11, 6, "TEST SUMMARY"); fs.font=Font(name="Calibri", size=12, bold=True, color="FFFFFF"); fs.fill=TITLE_FILL
fs.alignment = Alignment(vertical="center", horizontal="center")
ws.row_dimensions[11].height = 28
summary_rows = [
    (11, "Số trường hợp kiểm thử đạt (P):",              '=COUNTIF(L18:N500,"Passed")'),
    (12, "Số trường hợp kiểm thử không đạt (F):",         '=COUNTIF(L18:N500,"Failed")'),
    (13, "Số trường hợp kiểm thử đang xem xét:",          '=COUNTIF(L18:N500,"Pending")'),
    (14, "Số trường hợp kiểm thử chưa thực hiện:",        '=COUNTIF(L18:N500,"Not Executed")'),
    (15, "Tổng số trường hợp kiểm thử:",                  '=COUNTIF(L18:N500,"<>")'),
]
for r, label, formula in summary_rows:
    lc = ws.cell(r, 9, label); lc.font=SUMMARY_LABEL_FONT; lc.fill=SUMMARY_LABEL_FILL
    lc.alignment = Alignment(vertical="center", horizontal="right"); lc.border=BORDER
    ws.merge_cells(start_row=r, start_column=9, end_row=r, end_column=11)
    vc = ws.cell(r, 12, formula); vc.font=SUMMARY_VALUE_FONT; vc.fill=SUMMARY_LABEL_FILL
    vc.alignment=SUMMARY_VALUE_ALIGN; vc.border=BORDER
    ws.merge_cells(start_row=r, start_column=12, end_row=r, end_column=15)
    if r > 11: ws.row_dimensions[r].height = 22
ws.row_dimensions[16].height = 8

HEADERS = ["Module","Nhóm chức năng","TC ID","Chức năng","Priority","Tiền điều kiện","Bước thực hiện","Test Data",
           "Expected Result (chi tiết)","Giải thích nghiệp vụ","KQ thực tế","trạng thái check lần 1","trạng thái check lần 2","trạng thái check lần 3","Ghi chú"]
for i, h in enumerate(HEADERS, start=1):
    c = ws.cell(17, i, h); c.font=HEADER_FONT; c.fill=HEADER_FILL; c.alignment=HEADER_ALIGN; c.border=BORDER
ws.row_dimensions[17].height = 36

current_row = 18; data_row_idx = 0
def write_section_row(title):
    global current_row
    cell = ws.cell(current_row, 3, title); cell.font=SECTION_FONT; cell.fill=SECTION_FILL
    cell.alignment=SECTION_ALIGN; cell.border=BORDER
    ws.merge_cells(start_row=current_row, start_column=3, end_row=current_row, end_column=15)
    for col in (1,2):
        ws.cell(current_row, col).fill=SECTION_FILL; ws.cell(current_row, col).border=BORDER
    ws.row_dimensions[current_row].height = 26; current_row += 1
def write_tc(tc_id, function, priority, pre, steps, td, exp, note, group=""):
    global current_row, data_row_idx
    values = [MODULE_NAME, group, tc_id, function, priority, pre, steps, td, exp, note, "",
              "Not Executed","Not Executed","Not Executed",""]
    fill = EVEN_FILL if data_row_idx % 2 == 1 else None
    for i, v in enumerate(values, start=1):
        c = ws.cell(current_row, i, v); c.font=Font(name="Calibri", size=11)
        c.alignment = WRAP_TOP_CENTER if i == 5 else WRAP_TOP_LEFT; c.border=BORDER
        if fill: c.fill = fill
    longest = max(len(str(v)) for v in values)
    ws.row_dimensions[current_row].height = max(30, min(190, longest // 3))
    current_row += 1; data_row_idx += 1

if HAS_ROLE_SECTION:
    write_section_row("Phân quyền & truy cập")
    for suffix, func, prio, pre, steps, td, exp, note in ROLE_TCS:
        write_tc(f"TC-ROLE-{suffix}", func, prio, pre, steps, td, exp, note, group="Phân quyền & truy cập")

ROMAN = ["I","II","III","IV","V","VI","VII","VIII","IX","X"]
for roman, title, tcs in SECTIONS:
    write_section_row(f"{roman}. {title}")
    sec_idx = ROMAN.index(roman) + 1
    for tc_num, func, prio, pre, steps, td, exp, note in tcs:
        tc_id = f"TC_{sec_idx:02d}.{int(tc_num):03d}"
        write_tc(tc_id, func, prio, pre, steps, td, exp, note, group=title)

dv = DataValidation(type="list", formula1='"Passed,Failed,Pending,Not Executed"', allow_blank=True, showDropDown=False)
dv.add(f"L18:N{current_row + 100}"); ws.add_data_validation(dv)

wb.save(OUTPUT_FILE)
total = data_row_idx
print(f"OK -> {OUTPUT_FILE} | {total} test cases, data rows 18-{current_row-1}")
