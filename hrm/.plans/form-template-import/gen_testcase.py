# -*- coding: utf-8 -*-
"""Sinh testcase Excel cho chuc nang Import noi dung mau khao sat (man Tao mau phieu thu thap thong tin)."""
import os, sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", ".claude", "skills",
                                "testcase-documenter", "assets"))
from tc_engine import build

FEATURE = "Import mẫu khảo sát"
MODULE = "Phiếu thu thập thông tin"

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Nạp nhanh danh sách Section và câu hỏi khảo sát từ file Excel vào màn Tạo mẫu phiếu thu thập "
     "thông tin, thay cho việc gõ tay/kéo thả từng câu. Có kiểm tra dữ liệu theo dòng và tự chống "
     "trùng câu hỏi trong Ngân hàng câu hỏi khảo sát."),
    ("2. Đối tượng được nạp / hiển thị",
     "Các dòng Excel HỢP LỆ: có đủ Tên Section, Nội dung câu hỏi; Loại câu hỏi thuộc danh sách "
     "(Text ngắn, Text dài, Số, Dropdown, Radio 1 lựa chọn, Checkbox nhiều lựa chọn, Ngày, File, "
     "Có / Không); Bắt buộc = Có hoặc Không; Phạm vi câu hỏi = Tất cả hoặc Theo ứng dụng; với loại "
     "Dropdown/Radio/Checkbox thì Danh sách đáp án có tối thiểu 2 đáp án. Các dòng này hiện trên "
     "bảng xem trước và được nạp vào biểu mẫu."),
    ("3. Đối tượng bị ẩn / không nạp",
     "Dòng lỗi: thiếu Tên Section hoặc Nội dung câu hỏi; Loại câu hỏi không có trong danh sách; "
     "Bắt buộc không phải Có/Không; Phạm vi không phải Tất cả/Theo ứng dụng; loại lựa chọn nhưng "
     "Danh sách đáp án dưới 2 đáp án. Dòng lỗi KHÔNG được nạp vào biểu mẫu."),
    ("4. Bộ lọc thời gian áp dụng cho",
     "Không áp dụng. Chức năng import không có bộ lọc thời gian."),
    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "File phẳng: mỗi dòng là 1 câu hỏi kèm Tên Section của nó. Khi nạp, các câu cùng Tên Section "
     "được gom vào một Section trên biểu mẫu. Khi bấm Lưu, câu hỏi được ghi vào Ngân hàng câu hỏi "
     "khảo sát và mẫu phiếu được ghi vào Danh sách mẫu phiếu thu thập thông tin."),
    ("6. Quy tắc chống trùng câu hỏi",
     "Chống trùng theo tổ hợp 4 yếu tố: Nội dung câu hỏi + Loại câu hỏi + Danh sách đáp án + Phạm "
     "vi câu hỏi (so đáp án không phân biệt thứ tự và hoa/thường). Trùng thì tái dùng câu hỏi có "
     "sẵn, không tạo bản ghi mới. Với Phạm vi = Tất cả: xét trong nhóm câu hỏi dùng chung. Với "
     "Phạm vi = Theo ứng dụng: chỉ xét trong cùng Ứng dụng đang chọn; trùng ở Ứng dụng khác vẫn "
     "tạo câu mới cho Ứng dụng hiện tại."),
    ("7. Phân quyền cấp",
     "Quản lý danh mục mẫu phiếu thu thập thông tin (quyền dùng chung cho toàn màn Mẫu phiếu, gồm "
     "cả tải file mẫu, kiểm tra dữ liệu import và lưu mẫu phiếu)."),
    ("8. Cách hiểu các ô thống kê trong cửa sổ Import",
     "Ô 'Tổng' = số dòng dữ liệu đọc được từ file. Sau khi bấm Validate: ô 'Hợp lệ' = số dòng "
     "không có lỗi, ô 'Lỗi' = số dòng có lỗi. Nút 'Import' chỉ nạp các dòng Hợp lệ."),
    ("9. Ghi chú đọc bảng / các bẫy dễ sai",
     "- Nút Import Excel chỉ bật khi ĐÃ chọn Ứng dụng (vì phạm vi Theo ứng dụng cần biết Ứng dụng).\n"
     "- Câu hỏi CHỈ được ghi vào hệ thống khi bấm LƯU mẫu phiếu, KHÔNG phải lúc bấm Import (Import "
     "chỉ nạp vào biểu mẫu để xem/chỉnh).\n"
     "- Import là NẠP THÊM (append) vào cuối, không xoá các Section đang có trên biểu mẫu.\n"
     "- Đáp án nhiều lựa chọn phân tách bằng dấu phẩy; loại lựa chọn cần tối thiểu 2 đáp án.\n"
     "- Phạm vi câu hỏi nay chỉ còn Tất cả / Theo ứng dụng (đã bỏ 'Theo nhóm giải pháp'); file cũ "
     "ghi 'Theo nhóm giải pháp' vẫn được hiểu là Theo ứng dụng."),
]

ROLE_TCS = [
    ("01", "Tài khoản CÓ quyền quản lý mẫu phiếu import được", "P0",
     "Tài khoản A có quyền 'Quản lý danh mục mẫu phiếu thu thập thông tin'.",
     "1. Đăng nhập tài khoản A.\n2. Vào Danh mục > Phiếu thu thập thông tin > Tạo mới.\n"
     "3. Chọn Ứng dụng, bấm Import Excel, tải file mẫu, chọn file và thao tác.",
     "—",
     "- Vào được màn Tạo mẫu phiếu.\n- Tải được file mẫu, mở được cửa sổ Import và thực hiện đủ "
     "các bước Load / Validate / Import / Lưu."),
    ("02", "Tài khoản KHÔNG có quyền không thao tác được", "P0",
     "Tài khoản B không được cấp quyền 'Quản lý danh mục mẫu phiếu thu thập thông tin'.",
     "1. Đăng nhập tài khoản B.\n2. Thử vào màn Tạo mẫu phiếu và thử tải file mẫu / import.",
     "—",
     "- Không vào được màn Tạo mẫu phiếu (hoặc không thấy chức năng).\n- Không tải được file mẫu, "
     "không import, không lưu được mẫu phiếu."),
    ("03", "Chặn thao tác khi bỏ qua giao diện", "P1",
     "Tài khoản B không có quyền quản lý mẫu phiếu.",
     "1. Dùng công cụ kiểm thử gọi thẳng chức năng Tải file mẫu và Kiểm tra dữ liệu import bằng "
     "tài khoản B, bỏ qua giao diện.",
     "—",
     "- Hệ thống từ chối, báo không có quyền; không trả về file mẫu, không kiểm tra dữ liệu."),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", [
        ("001", "Nút Import Excel hiển thị đúng vị trí", "P1",
         "Đã đăng nhập tài khoản có quyền quản lý mẫu phiếu.",
         "1. Vào Danh mục > Phiếu thu thập thông tin.\n2. Bấm Tạo mới.",
         "—",
         "- Màn 'Tạo Form thu thập thông tin' mở ra.\n- Có nút 'Import Excel' nằm CÙNG HÀNG với ô "
         "'Ứng dụng' (thẳng hàng, không lệch dòng)."),
        ("002", "Nút Import bị mờ khi chưa chọn Ứng dụng", "P0",
         "Đang ở màn Tạo mẫu phiếu, ô Ứng dụng còn trống.",
         "1. Quan sát nút 'Import Excel' khi chưa chọn Ứng dụng.",
         "Ứng dụng: (để trống)",
         "- Nút 'Import Excel' bị mờ, không bấm được.\n- Ngay dưới nút hiện dòng hướng dẫn 'Chọn "
         "Ứng dụng trước khi import'."),
        ("003", "Nút Import bật khi đã chọn Ứng dụng", "P0",
         "Đang ở màn Tạo mẫu phiếu.",
         "1. Chọn một Ứng dụng ở ô 'Ứng dụng'.\n2. Quan sát nút Import.",
         "Ứng dụng: Vision",
         "- Nút 'Import Excel' sáng lên, bấm được.\n- Dòng hướng dẫn 'Chọn Ứng dụng trước khi "
         "import' biến mất."),
        ("004", "Mở cửa sổ Import", "P1",
         "Đã chọn Ứng dụng 'Vision'.",
         "1. Bấm nút 'Import Excel'.",
         "—",
         "- Cửa sổ 'Import nội dung mẫu khảo sát' mở ra, có các nút: Chọn file Excel, Tải file "
         "mẫu, Load lên bảng, Validate, Import."),
    ]),
    ("II", "TẢI FILE MẪU", [
        ("001", "Tải file mẫu thành công, đủ cột", "P0",
         "Đang mở cửa sổ Import.",
         "1. Bấm 'Tải file mẫu'.\n2. Mở file vừa tải.",
         "—",
         "- Tải về file Excel tên 'Mau_import_mau_khao_sat.xlsx'.\n- File có đúng 6 cột: Tên "
         "Section, Nội dung câu hỏi, Loại câu hỏi, Bắt buộc, Danh sách đáp án, Phạm vi câu hỏi."),
        ("002", "File mẫu có danh sách chọn sẵn đúng", "P1",
         "Đã tải file mẫu.",
         "1. Bấm vào ô của cột Loại câu hỏi / Bắt buộc / Phạm vi câu hỏi để xem danh sách chọn.",
         "—",
         "- Cột 'Loại câu hỏi' chọn: Text ngắn, Text dài, Số, Dropdown, Radio 1 lựa chọn, Checkbox "
         "nhiều lựa chọn, Ngày, File, Có / Không.\n- Cột 'Bắt buộc' chọn: Có / Không.\n- Cột 'Phạm "
         "vi câu hỏi' chọn: Tất cả / Theo ứng dụng.\n- ⚠️ Phạm vi KHÔNG còn 'Theo nhóm giải pháp'."),
        ("003", "File mẫu có dòng ví dụ", "P2",
         "Đã tải file mẫu.",
         "1. Xem các dòng bên dưới tiêu đề.",
         "—",
         "- Có sẵn vài dòng ví dụ (một câu Text ngắn Phạm vi Tất cả, một câu Radio có Danh sách "
         "đáp án 'Nhà nước, Tư nhân, FDI' Phạm vi Theo ứng dụng)."),
    ]),
    ("III", "CHỌN & ĐỌC FILE", [
        ("001", "Chọn file đúng mẫu và Load lên bảng", "P0",
         "Có file .xlsx đúng mẫu: 2 Section, 4 câu hỏi.",
         "1. Bấm 'Chọn file Excel', chọn file.\n2. Bấm 'Load lên bảng'.",
         "File: 2 Section (Thông tin chung, Khảo sát kỹ thuật), 4 câu hỏi",
         "- Tên file hiện cạnh nút chọn.\n- Bảng xem trước hiện đủ 4 dòng, đủ 6 cột.\n- Ô 'Tổng' "
         "bằng 4."),
        ("002", "Chọn file sai định dạng", "P1",
         "Có file định dạng .pdf hoặc .docx.",
         "1. Bấm 'Chọn file Excel', chọn file .pdf.",
         "File: tai_lieu.pdf",
         "- Hệ thống báo 'Vui lòng chọn file .xlsx hoặc .xls'.\n- Không nạp dữ liệu."),
        ("003", "File thiếu cột bắt buộc", "P0",
         "File Excel thiếu hẳn cột 'Loại câu hỏi'.",
         "1. Chọn file.\n2. Bấm 'Load lên bảng'.",
         "File: thiếu cột Loại câu hỏi",
         "- Hệ thống báo file không đúng mẫu (thiếu cột), nêu rõ các cột cần có.\n- Không hiện "
         "bảng xem trước."),
        ("004", "File trống (chỉ có dòng tiêu đề)", "P1",
         "File chỉ có dòng tiêu đề, không có dòng dữ liệu.",
         "1. Chọn file.\n2. Bấm 'Load lên bảng'.",
         "File: chỉ có tiêu đề",
         "- Hệ thống báo sheet dữ liệu trống / không có dòng dữ liệu.\n- Không nạp."),
    ]),
    ("IV", "KIỂM TRA DỮ LIỆU (VALIDATE)", [
        ("001", "Tất cả dòng hợp lệ", "P0",
         "File 4 dòng đều hợp lệ, đã Load lên bảng.",
         "1. Bấm 'Validate'.",
         "4 câu hợp lệ",
         "- Hiện 'Hợp lệ: 4, Lỗi: 0'.\n- Thông báo xanh 'Tất cả 4 câu hỏi hợp lệ. Bấm Import để "
         "nạp vào biểu mẫu.'\n- Nút 'Import' bật lên."),
        ("002", "Thiếu Nội dung câu hỏi", "P0",
         "Có 1 dòng để trống cột Nội dung câu hỏi.",
         "1. Load lên bảng.\n2. Bấm 'Validate'.",
         "Dòng 3: Nội dung câu hỏi để trống",
         "- Dòng đó bị đánh dấu lỗi 'Thiếu Nội dung câu hỏi', có kèm số thứ tự dòng trong file.\n"
         "- Dòng lỗi không được nạp."),
        ("003", "Loại câu hỏi không hợp lệ", "P0",
         "Có 1 dòng Loại câu hỏi ghi sai (không có trong danh sách).",
         "1. Load lên bảng.\n2. Bấm 'Validate'.",
         "Dòng 2: Loại câu hỏi = 'Chọn nhiều'",
         "- Báo lỗi 'Loại câu hỏi không hợp lệ' kèm số dòng.\n- Dòng lỗi không được nạp."),
        ("004", "Bắt buộc sai giá trị", "P1",
         "Có 1 dòng cột Bắt buộc ghi 'Yes'.",
         "1. Load lên bảng.\n2. Bấm 'Validate'.",
         "Dòng 2: Bắt buộc = 'Yes'",
         "- Báo lỗi 'Bắt buộc chỉ nhận: Có / Không' kèm số dòng."),
        ("005", "Phạm vi câu hỏi sai giá trị", "P1",
         "Có 1 dòng Phạm vi ghi 'Toàn bộ'.",
         "1. Load lên bảng.\n2. Bấm 'Validate'.",
         "Dòng 2: Phạm vi = 'Toàn bộ'",
         "- Báo lỗi 'Phạm vi chỉ nhận: Tất cả / Theo ứng dụng' kèm số dòng."),
        ("006", "Loại lựa chọn thiếu đáp án", "P0",
         "Có 1 câu Radio 1 lựa chọn nhưng Danh sách đáp án để trống (hoặc chỉ 1 đáp án).",
         "1. Load lên bảng.\n2. Bấm 'Validate'.",
         "Dòng 4: Radio 1 lựa chọn, Danh sách đáp án = trống",
         "- Báo lỗi 'Loại câu hỏi này cần ít nhất 2 đáp án' kèm số dòng."),
        ("007", "File vừa có dòng đúng vừa có dòng lỗi", "P0",
         "File 4 dòng: 2 hợp lệ, 2 lỗi.",
         "1. Load lên bảng.\n2. Bấm 'Validate'.\n3. Bấm 'Chỉ dòng lỗi'.",
         "2 hợp lệ + 2 lỗi",
         "- Hiện 'Hợp lệ: 2, Lỗi: 2'.\n- Nút 'Chỉ dòng lỗi' lọc ra đúng 2 dòng lỗi để sửa.\n"
         "- ⚠️ Dòng hợp lệ bị khoá, chỉ sửa được dòng lỗi rồi validate lại."),
        ("008", "Thiếu Tên Section", "P1",
         "Có 1 dòng để trống Tên Section.",
         "1. Load lên bảng.\n2. Bấm 'Validate'.",
         "Dòng 2: Tên Section để trống",
         "- Báo lỗi 'Thiếu Tên Section' kèm số dòng.\n- Dòng lỗi không được nạp."),
    ]),
    ("V", "NẠP VÀO BIỂU MẪU (IMPORT)", [
        ("001", "Nạp câu hỏi hợp lệ vào biểu mẫu", "P0",
         "Đã Validate 4/4 hợp lệ, 2 Section: Thông tin chung, Khảo sát kỹ thuật.",
         "1. Bấm 'Import'.",
         "—",
         "- Cửa sổ Import đóng lại.\n- Có thông báo dạng 'Đã nạp 4 câu hỏi (2 section) vào biểu "
         "mẫu...'.\n- Trên biểu mẫu hiện 2 Section với đúng câu hỏi, đúng loại (chữ / một lựa chọn "
         "/ số) và đúng dấu Bắt buộc."),
        ("002", "Chỉ nạp các dòng hợp lệ", "P0",
         "Đã Validate: 2 hợp lệ, 2 lỗi.",
         "1. Bấm 'Import'.",
         "—",
         "- Chỉ 2 câu hợp lệ được nạp vào biểu mẫu.\n- 2 dòng lỗi bị bỏ qua, không nạp."),
        ("003", "Nạp thêm không xoá Section đang có", "P0",
         "Trên biểu mẫu đã tự thêm sẵn 1 Section 'Khảo sát ban đầu'. File import có Section 'Thông "
         "tin chung'.",
         "1. Import file, Validate, bấm Import.",
         "—",
         "- Section 'Khảo sát ban đầu' vẫn còn nguyên.\n- Section 'Thông tin chung' được thêm vào "
         "CUỐI danh sách.\n- ⚠️ Không mất dữ liệu đang nhập dở."),
        ("004", "Gom câu hỏi theo Tên Section", "P1",
         "File có 3 câu cùng Tên Section 'Thông tin chung' và 1 câu Section 'Khảo sát kỹ thuật'.",
         "1. Import, Validate, bấm Import.",
         "3 câu + 1 câu",
         "- Biểu mẫu tạo đúng 2 Section.\n- Section 'Thông tin chung' chứa đủ 3 câu, đúng thứ tự."),
    ]),
    ("VI", "LƯU & CHỐNG TRÙNG CÂU HỎI", [
        ("001", "Lưu tạo câu hỏi mới trong Ngân hàng", "P0",
         "Ứng dụng 'Vision'; import 3 câu hỏi chưa từng có; Ngân hàng câu hỏi chưa có các câu này.",
         "1. Import 3 câu, nhập Tên form.\n2. Bấm 'Lưu'.",
         "3 câu mới (1 câu Radio đáp án A/B/C)",
         "- Lưu thành công, quay về danh sách mẫu phiếu.\n- Mở Thư viện câu hỏi của Ứng dụng "
         "'Vision' thấy 3 câu mới.\n- Câu Radio giữ đúng danh sách đáp án A / B / C."),
        ("002", "Trùng đủ 4 yếu tố trong cùng Ứng dụng thì tái dùng", "P0",
         "Ngân hàng đã có câu 'Loại hình doanh nghiệp?' (Radio; đáp án Nhà nước, Tư nhân, FDI; "
         "Phạm vi Theo ứng dụng; Ứng dụng 'Vision'). Import lại đúng câu đó cho Ứng dụng 'Vision'.",
         "1. Import câu đó, Validate, Import.\n2. Bấm 'Lưu'.",
         "Câu trùng đủ 4 yếu tố",
         "- KHÔNG sinh thêm câu mới trong Ngân hàng.\n- Biểu mẫu dùng lại câu có sẵn.\n- ⚠️ 4 yếu "
         "tố so trùng: Nội dung + Loại + Danh sách đáp án + Phạm vi."),
        ("003", "Trùng câu 'Tất cả' hai lần trong cùng file thì chỉ tạo 1", "P0",
         "File có 2 dòng y hệt nhau: câu 'Tên công ty là gì?' (Text ngắn, Phạm vi Tất cả) đặt ở "
         "2 Section khác nhau. Ngân hàng chưa có câu này.",
         "1. Import file, Validate, Import.\n2. Bấm 'Lưu'.",
         "2 dòng trùng nhau",
         "- Ngân hàng chỉ tạo 1 câu 'Tên công ty là gì?'.\n- Cả 2 vị trí trên biểu mẫu dùng chung "
         "1 câu hỏi đó."),
        ("004", "Trùng nội dung nhưng Ứng dụng khác thì tạo mới", "P0",
         "Ngân hàng đã có câu 'Loại hình doanh nghiệp?' Phạm vi Theo ứng dụng gắn Ứng dụng 'Vision'. "
         "Nay tạo mẫu phiếu cho Ứng dụng 'Nhà máy thông minh' và import đúng câu đó.",
         "1. Chọn Ứng dụng 'Nhà máy thông minh'.\n2. Import câu đó, Validate, Import.\n3. Bấm 'Lưu'.",
         "Câu trùng nội dung, khác Ứng dụng",
         "- Hệ thống TẠO câu mới gắn Ứng dụng 'Nhà máy thông minh'.\n- Không tái dùng câu của "
         "Ứng dụng 'Vision'."),
        ("005", "Phạm vi Theo ứng dụng bắt buộc đã chọn Ứng dụng", "P1",
         "Câu hỏi có Phạm vi 'Theo ứng dụng' nhưng chưa chọn Ứng dụng.",
         "1. Dùng công cụ kiểm thử gọi thẳng chức năng Lưu mẫu phiếu với câu Phạm vi 'Theo ứng "
         "dụng' mà bỏ trống Ứng dụng, bỏ qua giao diện.",
         "Phạm vi: Theo ứng dụng; Ứng dụng: trống",
         "- Hệ thống từ chối, báo cần chọn Ứng dụng cho phạm vi 'Theo ứng dụng'.\n- Không tạo câu "
         "hỏi, không tạo mẫu phiếu."),
    ]),
    ("VII", "RÀNG BUỘC NHẬP LIỆU", [
        ("001", "Đáp án phân tách bằng dấu phẩy", "P1",
         "Câu Checkbox nhiều lựa chọn, cột Danh sách đáp án = 'A, B, C'.",
         "1. Import, Validate, Import.",
         "Danh sách đáp án: A, B, C",
         "- Câu hỏi nhận đúng 3 đáp án A / B / C (bỏ khoảng trắng thừa quanh mỗi đáp án)."),
        ("002", "Nhãn thừa khoảng trắng / khác hoa-thường vẫn nhận", "P2",
         "Loại câu hỏi = ' radio 1 lựa chọn ' (thừa khoảng trắng); Phạm vi = 'tất cả'.",
         "1. Load lên bảng.\n2. Bấm 'Validate'.",
         "Loại: ' radio 1 lựa chọn '; Phạm vi: 'tất cả'",
         "- Vẫn hiểu đúng loại và phạm vi, không báo lỗi."),
        ("003", "Nhãn cũ 'Theo nhóm giải pháp' vẫn được chấp nhận", "P2",
         "File cũ có cột Phạm vi ghi 'Theo nhóm giải pháp'.",
         "1. Load lên bảng.\n2. Bấm 'Validate'.",
         "Phạm vi: Theo nhóm giải pháp",
         "- Hệ thống vẫn hiểu là 'Theo ứng dụng', không báo lỗi.\n- ⚠️ File mẫu mới chỉ còn "
         "'Theo ứng dụng'."),
        ("004", "Đáp án nhập cho loại không phải lựa chọn thì bỏ qua", "P2",
         "Câu Text ngắn nhưng cột Danh sách đáp án vẫn có nhập.",
         "1. Import, Validate, Import, Lưu.",
         "Text ngắn + Danh sách đáp án: 'a, b'",
         "- Câu được nạp và lưu bình thường.\n- Phần đáp án bị bỏ qua, không lưu vào câu hỏi."),
    ]),
    ("VIII", "LUỒNG ĐẦU-CUỐI", [
        ("001", "Luồng đầy đủ từ tải mẫu đến lưu", "P0",
         "Tài khoản có quyền quản lý mẫu phiếu; Ứng dụng 'Vision'.",
         "1. Chọn Ứng dụng 'Vision'.\n2. Bấm Import Excel > Tải file mẫu, điền 2 Section 4 câu.\n"
         "3. Chọn file > Load lên bảng > Validate (4/4 hợp lệ) > Import.\n4. Nhập Tên form.\n"
         "5. Bấm 'Lưu'.",
         "2 Section, 4 câu hỏi",
         "- Về danh sách mẫu phiếu, mẫu mới xuất hiện.\n- Mở lại mẫu phiếu thấy đủ 2 Section và "
         "4 câu hỏi đúng loại, đúng đáp án.\n- Thư viện câu hỏi của Ứng dụng 'Vision' có các câu mới."),
    ]),
]

build(
    output_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "testcase.xlsx"),
    sheet_name="Trang tính1",
    feature_name=FEATURE + " - Cập nhật ngày 28/08/2026",
    module_name=MODULE,
    description_block=DESCRIPTION_BLOCK,
    role_tcs=ROLE_TCS,
    sections=SECTIONS,
)
