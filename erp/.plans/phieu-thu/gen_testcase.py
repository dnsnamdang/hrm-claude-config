# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Phieu thu tien" (admin/income-expenditure/bill_incomes).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

⚠️ Tai lieu nay viet theo LOGIC ERP dang chay tren nhanh gop_db (repo D:/laragon/www/erp),
KHONG phai ban da port sang HRM.

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :6526-6539
  app/Http/Controllers/IncomeExpenditure/BillIncomeController.php
  app/Model/IncomeExpenditure/BillIncome.php (+ BillIncomeDetail, BillIncomeDetailProductExportRequest)
  app/Http/Requests/IncomeExpenditure/BillIncomes/BillIncomeStoreRequest.php
  app/Http/Requests/IncomeExpenditure/BillIncomes/BillIncomeUpdateRequest.php
  app/Model/IncomeExpenditure/BillIncomeRequest.php (nguon phieu de nghi)
  app/Model/Accounting/Account.php (getAccountsForSelect)
  app/Helpers/NotificationHelper.php :40 (sendNotifyWithPermission)
  resources/views/income_expenditure/bill_incomes/*.blade.php
  resources/views/partials/classes/IncomeExpenditure/BillIncome*.blade.php
  resources/views/partials/classes/base/Datatable.blade.php :142-195
  resources/views/layouts/topmenubar.blade.php :1004

Chay:  python .plans/phieu-thu/gen_testcase.py
"""
import os
import sys

try:  # console Windows mac dinh cp1252
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

# .plans/phieu-thu -> .plans -> erp -> hrm-claude-config -> hrm/.claude/skills/...
sys.path.insert(0, os.path.join(
    HERE, "..", "..", "..", "hrm", ".claude", "skills", "testcase-documenter", "assets"))

from tc_engine import build  # noqa: E402

OUT = os.path.join(HERE, "testcase-phieu-thu.xlsx")

MODULE = "Phiếu thu tiền"

# ============================================================ 9 MUC MO TA
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Quản lý Phiếu thu tiền: chứng từ do Kế toán thanh toán lập để thu tiền theo một Phiếu đề nghị "
     "thu tiền đã được gửi duyệt, thuộc nhóm Công nợ - Thu - Chi.\n"
     "Phiếu thu KHÔNG lập độc lập được: bắt buộc gắn với đúng một Phiếu đề nghị thu tiền đang ở trạng "
     "thái Chờ KT duyệt, và toàn bộ dòng chi tiết được bê nguyên từ phiếu đề nghị sang.\n"
     "Kế toán thanh toán làm được: xem danh sách, lọc, tạo phiếu (Lưu nháp hoặc Lưu và gửi duyệt), "
     "sửa, xóa, xem chi tiết, in phiếu và xuất tệp Excel.\n"
     "Thủ quỹ làm được: mở phiếu ở trạng thái Chờ duyệt, nhập Số tiền thực nhận cho từng dòng, rồi "
     "bấm Duyệt phiếu thu (ghi sổ kế toán) hoặc Hủy phiếu thu.\n"
     "Màn hình có 4 chế độ danh sách khác nhau dùng chung một bảng dữ liệu — xem mục 5."),

    ("2. Đối tượng được tính / hiển thị",
     "Phiếu thu có đủ 4 trạng thái: Đang tạo · Chờ duyệt · Đã duyệt · Hủy. Nhãn Đã duyệt tô XANH, ba "
     "nhãn còn lại tô ĐỎ.\n"
     "Phạm vi phiếu nhìn thấy phụ thuộc chế độ danh sách đang mở:\n"
     "- Chế độ \"Phiếu của tôi\" (vào thẳng đường dẫn không kèm tham số): chỉ phiếu do chính mình lập, "
     "gồm cả phiếu nháp của mình.\n"
     "- Chế độ \"Tất cả\" (mục menu Phiếu thu trỏ vào đây): lấy theo 2 quyền xem ở mục 7, và luôn ẩn "
     "phiếu nháp của người khác.\n"
     "- Chế độ \"Phiếu thu chờ duyệt\": phiếu trạng thái Chờ duyệt thuộc công ty của người đăng nhập, "
     "KHÔNG áp thêm 2 quyền xem theo cấp. Đường dẫn này được chặn bằng quyền Thủ quỹ duyệt phiếu thu.\n"
     "- Chế độ \"Phiếu thu đã duyệt\": phiếu mà chính người đăng nhập là người đã duyệt VÀ đang ở "
     "trạng thái Đã duyệt.\n"
     "⚠️ Hai chế độ chờ duyệt và đã duyệt KHÔNG có mục menu nào trỏ tới — xem mục 9.\n"
     "Bảng danh sách có 11 cột: STT · Mã phiếu · Mã phiếu đề nghị thu · Loại thu · Khách hàng · Số tiền "
     "· Người đề nghị · Ngày lập · Người lập · Trạng thái · Hành động."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu nháp (Đang tạo) của NGƯỜI KHÁC bị ẩn ở chế độ \"Tất cả\".\n"
     "- Nút \"Sửa phiếu thu\" và nút \"Xóa\" chỉ hiện khi phiếu ở trạng thái Đang tạo. Phiếu Chờ duyệt, "
     "Đã duyệt, Hủy đều không có hai nút này.\n"
     "- Hai nút \"Duyệt phiếu thu\" và \"Hủy phiếu thu\" trong màn chi tiết chỉ hiện khi phiếu ở trạng "
     "thái Chờ duyệt VÀ người đăng nhập có quyền Thủ quỹ duyệt phiếu thu.\n"
     "- Hai mục \"In\" và \"Xuất Excel\" luôn hiện cho mọi dòng, mọi trạng thái.\n"
     "- Nút \"Tạo mới\" chỉ có ở chế độ \"Phiếu của tôi\" và \"Tất cả\".\n"
     "- Cửa sổ chọn Số phiếu đề nghị CHỈ liệt kê phiếu đề nghị thu đang ở trạng thái Chờ KT duyệt; "
     "phiếu đề nghị nháp, đã tạo phiếu thu, đã hạch toán, hủy, không duyệt đều không xuất hiện.\n"
     "- Ba ô lọc Công ty / Phòng ban / Bộ phận chỉ hiện ở chế độ \"Tất cả\" và chỉ với người có quyền "
     "xem theo cấp tương ứng.\n"
     "- Người dùng KHÔNG thêm được dòng chi tiết và KHÔNG xóa được dòng chi tiết trên phiếu thu; số "
     "dòng luôn đúng bằng số dòng của phiếu đề nghị gốc.\n"
     "- Màn hình KHÔNG có chức năng Nhập Excel."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "⚠️ KHÔNG ÁP DỤNG. Khối tìm kiếm vẫn hiển thị hai ô \"Từ ngày\" và \"Đến ngày\", nhưng hệ thống "
     "KHÔNG dùng đến hai giá trị này khi lấy dữ liệu: chọn ngày nào cũng ra nguyên kết quả cũ, kể cả "
     "khoảng ngày không có phiếu nào.\n"
     "Đây là bẫy đối chiếu số liệu nặng nhất của màn, đã dựng ca test riêng ở mục II. Muốn giới hạn "
     "theo thời gian thì phải lọc bằng Mã phiếu (mã có nhúng tháng - năm lập, xem mục 5).\n"
     "Không có bộ lọc theo ngày cập nhật, cũng không có bộ lọc theo Ngày hạch toán."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Ba cấp: Phiếu đề nghị thu tiền → Phiếu thu → Dòng chi tiết.\n"
     "- Một phiếu đề nghị thu chỉ được lập ĐÚNG MỘT phiếu thu. Lập lần hai bị hệ thống chặn.\n"
     "- Phiếu thu giữ: Mã phiếu, Số phiếu đề nghị, Tài khoản nợ, Người nộp, Tỷ giá, Ghi chú, Trạng "
     "thái, Ngày hạch toán, Người tạo, Người duyệt, Công ty, Phòng ban, Bộ phận.\n"
     "- Loại thu, Loại tiền, Lý do thu lấy từ phiếu đề nghị và bị KHÓA, không sửa trên phiếu thu.\n"
     "- Mỗi dòng chi tiết giữ: Số tài khoản có · Tên tài khoản · Khách hàng (hoặc Nhà cung cấp, hoặc "
     "Nhân viên) · Số đơn hàng - Hợp đồng · Số tiền đề nghị thu · Số tiền duyệt thu · Số tiền thực nhận "
     "· Ghi chú. Ba cột tiền đều có cột quy đổi VND đi kèm khi phiếu là ngoại tệ.\n"
     "- Dòng gắn hợp đồng nguyên tắc có thêm bảng con phân bổ theo từng Phiếu yêu cầu xuất hàng: Số "
     "phiếu · Giá trị · Đã thu · Số tiền thu.\n"
     "- Mã phiếu sinh tự động: mã công ty + \".PT\" + tháng năm (4 số) + \".\" + 5 chữ số tăng dần, ví "
     "dụ TPE.PT0826.00017. Không sửa tay được.\n"
     "- Công ty / Phòng ban / Bộ phận của phiếu thu lấy từ hồ sơ nhân sự của người LẬP PHIẾU THU tại "
     "thời điểm tạo, và không đổi về sau.\n"
     "- Bốn chế độ danh sách dùng CHUNG một nguồn dữ liệu và chung bộ lọc; khác nhau ở phạm vi lọc và "
     "ở bộ nút phía trên bảng.\n"
     "- Mỗi lần lưu, toàn bộ dòng chi tiết cũ (kể cả bảng con phân bổ) bị xóa và ghi lại từ đầu."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Cột \"Số tiền\" ngoài danh sách ĐỔI THEO TRẠNG THÁI phiếu: phiếu Đang tạo và Chờ duyệt lấy TỔNG "
     "Số tiền duyệt thu đã quy đổi VND; phiếu Đã duyệt lấy TỔNG Số tiền thực nhận đã quy đổi VND. "
     "Cùng một phiếu, con số này thay đổi ngay sau khi thủ quỹ duyệt nếu thực nhận nhỏ hơn duyệt thu.\n"
     "- Trong form: cột quy đổi VND của mỗi dòng = số tiền của dòng đó × Tỷ giá. Dòng \"Tổng cộng\" "
     "cuối bảng cộng dồn từng cặp cột: đề nghị thu, duyệt thu, thực nhận.\n"
     "- Hai ô lọc \"Số tiền từ - đến\" so với TỔNG đã quy đổi VND của cả phiếu, không so từng dòng.\n"
     "- Cột \"Khách hàng\" ngoài danh sách chỉ lấy đối tượng của DÒNG ĐẦU TIÊN; phiếu gom nhiều khách "
     "hàng vẫn chỉ hiện một tên.\n"
     "- Nút phân bổ ở ô \"Số tiền phân bổ\": rải tiền lần lượt từ dòng trên xuống, mỗi dòng nhận tối đa "
     "bằng Số tiền duyệt thu của dòng đó, hết tiền thì các dòng còn lại bằng 0.\n"
     "- Nút phân bổ trong bảng con phiếu yêu cầu xuất hàng: rải Số tiền thực nhận của dòng xuống từng "
     "phiếu xuất, mỗi phiếu tối đa bằng phần còn phải thu, dòng cuối nhận phần dư.\n"
     "- Khi ghi sổ, dòng có Số tiền thực nhận bằng 0 bị BỎ QUA, không sinh bút toán.\n"
     "- Một phiếu khớp nhiều điều kiện lọc vẫn chỉ hiện một dòng."),

    ("7. Phân quyền cấp",
     "Bốn quyền liên quan tới màn hình này:\n"
     "1. \"Kế toán thanh toán\" — được vào đường dẫn Tạo mới và đường dẫn Sửa phiếu thu. Đây là hai "
     "đường dẫn DUY NHẤT của màn được hệ thống chặn bằng quyền này.\n"
     "2. \"Thủ quỹ duyệt phiếu thu\" — được vào màn Phiếu thu chờ duyệt, và thấy hai nút Duyệt phiếu "
     "thu / Hủy phiếu thu trong màn chi tiết.\n"
     "3. \"Xem tất cả phiếu thu của tổng công ty\" — thấy phiếu của mọi công ty ở chế độ Tất cả; bộ lọc "
     "hiện thêm ô Công ty và ô Phòng ban.\n"
     "4. \"Xem tất cả phiếu thu của công ty\" — chỉ phiếu công ty mình ở chế độ Tất cả; bộ lọc hiện ô "
     "Phòng ban.\n"
     "⚠️ Màn Phiếu thu KHÔNG có quyền xem cấp phòng ban và cấp bộ phận (khác với màn Đề nghị thu tiền "
     "vốn có đủ bốn cấp). Ai không có một trong hai quyền xem trên thì ở chế độ Tất cả chỉ thấy phiếu "
     "do chính mình lập.\n"
     "Tài khoản có vai trò Super Admin luôn mở được chi tiết mọi phiếu.\n"
     "⚠️ Các chức năng còn lại — xem danh sách, lưu, cập nhật, xóa, in, xuất Excel — KHÔNG gắn quyền ở "
     "phía hệ thống, chỉ ẩn / hiện nút trên giao diện. Đây là hiện trạng của mã nguồn; nhóm test bỏ qua "
     "giao diện (mục IX và các ca TC-ROLE cuối) dựng riêng để đo mức độ rủi ro này."),

    ("8. Cách tính các ô thống kê",
     "- Ô \"Hiển thị a đến b trong tổng số N\" dưới bảng: a là dòng đầu trang đang xem, b là dòng cuối, "
     "N là tổng số phiếu khớp bộ lọc trong phạm vi chế độ đang mở.\n"
     "- Ô \"Số dòng mỗi trang\": mặc định 10; đổi số dòng thì bảng quay về trang 1.\n"
     "- Cột STT đánh liên tục theo trang: trang 2 với 10 dòng mỗi trang bắt đầu từ 11.\n"
     "- Cột \"Số tiền\": xem công thức đổi theo trạng thái ở mục 6, hiển thị phân cách nghìn bằng dấu "
     "phẩy, không có phần thập phân.\n"
     "- Cột \"Ngày lập\" hiển thị dạng ngày/tháng/năm, không có giờ.\n"
     "- Ngày hạch toán được hệ thống đóng dấu bằng NGÀY BẤM DUYỆT, không cho người dùng chọn, và không "
     "có cột nào ngoài danh sách hiển thị giá trị này.\n"
     "- Bản in có dòng \"Tổng cộng\" và dòng \"Bằng chữ\": đọc theo Số tiền thực nhận nếu số này lớn "
     "hơn 0, ngược lại đọc theo Số tiền đề nghị thu. Nghĩa là phiếu chưa duyệt in ra vẫn có số tiền.\n"
     "- Bản in luôn ra 2 liên: phiếu 1 khách hàng thì 2 liên nằm trên cùng một trang, phiếu nhiều khách "
     "hàng thì 2 liên tách thành 2 trang."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất của màn này — đọc trước khi chạy test:\n"
     "1. ⚠️ Hai ô lọc \"Từ ngày\" / \"Đến ngày\" KHÔNG có tác dụng (mục 4). Chọn khoảng ngày không có "
     "phiếu nào vẫn ra nguyên danh sách cũ. Ghi nhận Failed.\n"
     "2. ⚠️ Ba ô lọc Công ty / Phòng ban / Bộ phận lọc theo đơn vị của PHIẾU ĐỀ NGHỊ THU gốc, KHÔNG "
     "phải đơn vị của người lập phiếu thu. Kế toán công ty 1 lập phiếu thu cho đề nghị của công ty 3 "
     "thì lọc Công ty 3 vẫn ra phiếu đó, còn lọc Công ty 1 thì không.\n"
     "3. ⚠️ Xóa phiếu thu: hệ thống KHÔNG kiểm tra quyền và KHÔNG kiểm tra trạng thái. Dán thẳng đường "
     "dẫn xóa của một phiếu bất kỳ, kể cả phiếu Đã duyệt đã ghi sổ, là phiếu bị xóa trong khi bút toán "
     "đã ghi vẫn còn nguyên. Đây là lỗ hổng, ghi nhận Failed.\n"
     "4. ⚠️ Sửa phiếu thu chỉ ẩn NÚT theo trạng thái. Người có quyền Kế toán thanh toán dán thẳng đường "
     "dẫn sửa của phiếu Chờ duyệt hoặc phiếu Hủy vẫn mở được form và lưu được.\n"
     "5. ⚠️ Xóa phiếu thu KHÔNG trả phiếu đề nghị về trạng thái Chờ KT duyệt. Phiếu đề nghị kẹt ở Đã "
     "tạo phiếu thu, mất nút Tạo phiếu thu, không lập lại được từ giao diện.\n"
     "6. ⚠️ Hai màn Phiếu thu chờ duyệt và Phiếu thu đã duyệt KHÔNG có mục menu nào trỏ tới. Thủ quỹ "
     "vào được bằng thông báo hoặc bằng đường dẫn trực tiếp; sau khi bấm Duyệt thì hệ thống mới tự đưa "
     "sang màn đã duyệt.\n"
     "7. ⚠️ Ô \"Tỷ giá\" trong màn chi tiết dành cho thủ quỹ KHÔNG bị khóa. Sửa tỷ giá rồi bấm Duyệt là "
     "toàn bộ số quy đổi VND và số ghi sổ đổi theo, không có cảnh báo nào.\n"
     "8. ⚠️ Nhập Số tiền thực nhận lớn hơn Số tiền duyệt thu thì ô tự bị kéo về bằng số duyệt thu, "
     "KHÔNG có thông báo. Đừng nhầm là hệ thống nhận sai số.\n"
     "9. ⚠️ Ô \"Người nộp\" nhập trên phiếu thu KHÔNG lên bản in. Bản in lấy Người nộp của phiếu đề "
     "nghị thu, mà màn đề nghị lại không có ô này nên dòng Người nộp trên bản in thường TRỐNG.\n"
     "10. ⚠️ Dòng \"Người đề nghị\" trên bản in và trong tệp Excel ra hai người khác nhau: bản in lấy "
     "người lập phiếu đề nghị, tệp Excel lấy người lập phiếu thu.\n"
     "11. ⚠️ Cột Khách hàng ngoài danh sách chỉ lấy khách của dòng đầu tiên; phiếu gom nhiều khách vẫn "
     "chỉ hiện một tên.\n"
     "12. ⚠️ Phiếu gắn đề nghị loại \"Thu khác\" không có mẫu in — bấm In sẽ ra trang lỗi. Loại này "
     "không lập mới được từ màn đề nghị, chỉ tồn tại ở dữ liệu cũ.\n"
     "13. ⚠️ Ô Tỷ giá ở form tạo được khóa bằng phép so sánh nghiêm ngặt với loại tiền. Nếu loại tiền "
     "trả về dạng chữ thay vì dạng số thì ô vẫn sửa được — kiểm cả trường hợp phiếu tiền Việt Nam.\n"
     "14. ⚠️ Tỷ giá in trên bản in ngoại tệ lấy từ DANH MỤC tiền tệ ở thời điểm in, KHÔNG phải tỷ giá "
     "đã lưu trong phiếu. Phiếu cũ in lại sau khi danh mục đổi tỷ giá sẽ ra số khác.\n"
     "15. ⚠️ Với dòng gắn hợp đồng nguyên tắc, tổng cột Số tiền thu của bảng con phải BẰNG ĐÚNG Số tiền "
     "thực nhận của dòng thì mới duyệt được; lệch một đồng là bị chặn ngay trên giao diện.\n"
     "16. Bộ lọc được hệ thống ghi nhớ RIÊNG cho từng chế độ danh sách; rời màn rồi quay lại vẫn còn "
     "điều kiện lọc cũ — test xong nhớ bấm nút làm mới bộ lọc trước khi sang ca test khác."),
]

# ============================================================ TC PHAN QUYEN
ROLE_TCS = [
    ("00", "Tài khoản không có quyền xem nào chỉ thấy phiếu do chính mình lập", "P0",
     "Tài khoản NV-A không có quyền \"Xem tất cả phiếu thu của tổng công ty\" và không có quyền \"Xem "
     "tất cả phiếu thu của công ty\"; NV-A đã lập 12 phiếu thu; công ty của NV-A có hơn 150 phiếu thu "
     "của nhiều người",
     "1. Đăng nhập bằng NV-A\n"
     "2. Mở menu Công nợ - Thu - Chi, bấm mục Phiếu thu\n"
     "3. Đọc số tổng dưới bảng\n"
     "4. Lật hết các trang, soát cột Người lập",
     "Tài khoản: NV-A (không quyền xem theo cấp)",
     "- Vào được màn hình, không bị chặn\n"
     "- Tổng hiện đúng 12\n"
     "- Mọi dòng đều có Người lập là NV-A\n"
     "- Khối lọc KHÔNG có ô Công ty, KHÔNG có ô Phòng ban"),

    ("01", "Quyền xem của tổng công ty thấy phiếu thu của mọi công ty", "P0",
     "Tài khoản B chỉ có quyền \"Xem tất cả phiếu thu của tổng công ty\"; hệ thống có phiếu thu của ít "
     "nhất 3 công ty",
     "1. Đăng nhập bằng B, mở mục Phiếu thu trên menu\n"
     "2. Bấm nút Bộ lọc để bung khối tìm kiếm\n"
     "3. Ghi lại các ô lọc theo đơn vị đang hiện\n"
     "4. Chọn lần lượt từng Công ty rồi bấm nút tìm kiếm",
     "Quyền: Xem tất cả phiếu thu của tổng công ty",
     "- Khối lọc hiện CẢ ô Công ty và ô Phòng ban\n"
     "- Bỏ chọn công ty thì thấy phiếu của cả 3 công ty\n"
     "- ⚠️ Chọn công ty nào ra phiếu mà PHIẾU ĐỀ NGHỊ gốc thuộc công ty đó, không phải phiếu do người "
     "công ty đó lập (mục 9 ghi chú 2)"),

    ("02", "Quyền xem của công ty chỉ thấy phiếu thu công ty mình", "P0",
     "Tài khoản C chỉ có quyền \"Xem tất cả phiếu thu của công ty\", thuộc công ty 3; công ty 3 có 40 "
     "phiếu thu, công ty 1 có 260 phiếu thu",
     "1. Đăng nhập bằng C, mở mục Phiếu thu\n"
     "2. Bấm nút Bộ lọc, ghi lại các ô lọc theo đơn vị\n"
     "3. Đọc số tổng, soát danh sách qua tất cả các trang",
     "Quyền: Xem tất cả phiếu thu của công ty",
     "- Khối lọc KHÔNG có ô Công ty, chỉ có ô Phòng ban\n"
     "- Tổng bằng 40 trừ đi số phiếu nháp của người khác trong công ty 3\n"
     "- Không có phiếu nào của công ty 1"),

    ("03", "Màn Phiếu thu không có quyền xem cấp phòng ban và cấp bộ phận", "P1",
     "Tài khoản D có quyền \"Xem tất cả phiếu đề nghị thu của phòng ban\" (quyền của màn Đề nghị thu "
     "tiền) nhưng KHÔNG có hai quyền xem của màn Phiếu thu",
     "1. Đăng nhập bằng D, mở mục Đề nghị thu tiền, ghi lại số tổng\n"
     "2. Mở mục Phiếu thu, đọc số tổng và soát cột Người lập",
     "Quyền: chỉ có quyền xem cấp phòng ban của màn Đề nghị thu tiền",
     "- Màn Đề nghị thu tiền: thấy phiếu của các phòng ban D quản lý\n"
     "- Màn Phiếu thu: CHỈ thấy phiếu do chính D lập\n"
     "- ⚠️ Đúng hiện trạng — màn Phiếu thu không có quyền cấp phòng ban / bộ phận (mục 7)"),

    ("04", "Có cả hai quyền xem thì lấy phạm vi rộng nhất", "P1",
     "Tài khoản F có ĐỒNG THỜI quyền \"Xem tất cả phiếu thu của tổng công ty\" và \"Xem tất cả phiếu "
     "thu của công ty\"",
     "1. Đăng nhập bằng F, mở mục Phiếu thu\n"
     "2. Đọc số tổng, so với số của tài khoản B ở TC-ROLE-01",
     "Quyền: tổng công ty + công ty",
     "- Tổng bằng đúng số của tài khoản chỉ có quyền tổng công ty\n"
     "- Không bị thu hẹp về phạm vi một công ty"),

    ("05", "Kế toán thanh toán vào được màn Tạo mới", "P0",
     "Tài khoản KT-1 có quyền \"Kế toán thanh toán\"; có ít nhất 3 phiếu đề nghị thu đang Chờ KT duyệt",
     "1. Đăng nhập bằng KT-1, mở mục Phiếu thu\n"
     "2. Bấm nút Tạo mới\n"
     "3. Bấm kính lúp ở ô Số phiếu đề nghị",
     "Quyền: Kế toán thanh toán",
     "- Vào được form Tạo phiếu thu tiền, không bị chặn\n"
     "- Cửa sổ chọn hiện đúng 3 phiếu đề nghị đang Chờ KT duyệt"),

    ("06", "Không có quyền Kế toán thanh toán thì bị chặn ở màn Tạo mới", "P0",
     "Tài khoản NV-A ở TC-ROLE-00, không có quyền \"Kế toán thanh toán\"",
     "1. Đăng nhập bằng NV-A, mở mục Phiếu thu\n"
     "2. Bấm nút Tạo mới\n"
     "3. Nếu không có nút thì dán thẳng đường dẫn tạo mới vào thanh địa chỉ",
     "Đường dẫn Tạo phiếu thu",
     "- ⚠️ Nút Tạo mới VẪN hiển thị trên bảng (giao diện không ẩn theo quyền)\n"
     "- Bấm vào: hệ thống từ chối, báo không có quyền, không mở được form"),

    ("07", "Không có quyền Kế toán thanh toán thì bị chặn ở màn Sửa", "P0",
     "Tài khoản NV-A; tồn tại phiếu thu trạng thái Đang tạo do chính NV-A lập trước đó",
     "1. Đăng nhập bằng NV-A, mở mục Phiếu thu\n"
     "2. Bấm biểu tượng bánh răng ở dòng phiếu Đang tạo, bấm Sửa phiếu thu",
     "Đường dẫn Sửa phiếu thu",
     "- ⚠️ Mục Sửa phiếu thu VẪN hiện trong menu hành động\n"
     "- Bấm vào: hệ thống từ chối, báo không có quyền, phiếu không bị thay đổi"),

    ("08", "Thủ quỹ vào được màn Phiếu thu chờ duyệt", "P0",
     "Tài khoản TQ-1 có quyền \"Thủ quỹ duyệt phiếu thu\", thuộc công ty 3; công ty 3 có 5 phiếu thu "
     "Chờ duyệt, công ty 1 có 18 phiếu thu Chờ duyệt",
     "1. Đăng nhập bằng TQ-1\n"
     "2. Soát toàn bộ menu, tìm mục dẫn tới màn Phiếu thu chờ duyệt\n"
     "3. Dán thẳng đường dẫn màn chờ duyệt vào thanh địa chỉ\n"
     "4. Đọc số tổng và cột Trạng thái",
     "Quyền: Thủ quỹ duyệt phiếu thu",
     "- ⚠️ KHÔNG có mục menu nào dẫn tới màn này (mục 9 ghi chú 6)\n"
     "- Dán đường dẫn: vào được, đúng 5 dòng, tất cả đều là Chờ duyệt của công ty 3\n"
     "- KHÔNG thấy 18 phiếu của công ty 1\n"
     "- Phía trên bảng KHÔNG có nút Tạo mới"),

    ("09", "Không có quyền Thủ quỹ thì bị chặn ở màn chờ duyệt", "P0",
     "Tài khoản KT-1 chỉ có quyền \"Kế toán thanh toán\", không có quyền \"Thủ quỹ duyệt phiếu thu\"",
     "1. Đăng nhập bằng KT-1\n"
     "2. Dán thẳng đường dẫn màn Phiếu thu chờ duyệt vào thanh địa chỉ",
     "Đường dẫn màn chờ duyệt",
     "- Hệ thống từ chối, báo không có quyền, không hiện dữ liệu phiếu nào"),

    ("10", "Không có quyền Thủ quỹ thì không thấy nút duyệt trong màn chi tiết", "P0",
     "Tài khoản KT-1; tồn tại phiếu thu PT-01 đang ở trạng thái Chờ duyệt do chính KT-1 lập",
     "1. Đăng nhập bằng KT-1, mở mục Phiếu thu\n"
     "2. Bấm vào Mã phiếu của PT-01 để mở chi tiết\n"
     "3. Soát khu vực nút phía dưới form",
     "—",
     "- Mở được màn chi tiết (là người lập nên vẫn xem được)\n"
     "- KHÔNG có nút Duyệt phiếu thu, KHÔNG có nút Hủy phiếu thu\n"
     "- Chỉ có nút Quay lại\n"
     "- Ô Ghi chú và cột Số tiền thực nhận vẫn hiển thị nhưng không dùng để làm gì"),

    ("11", "Thủ quỹ thấy phiếu chờ duyệt của cả công ty dù không có quyền xem theo cấp", "P0",
     "Tài khoản TQ-2 chỉ có quyền \"Thủ quỹ duyệt phiếu thu\", KHÔNG có quyền xem theo cấp nào; công ty "
     "của TQ-2 có 5 phiếu thu Chờ duyệt do 3 người khác nhau lập",
     "1. Đăng nhập bằng TQ-2, mở mục Phiếu thu trên menu, đọc số tổng\n"
     "2. Dán đường dẫn màn Phiếu thu chờ duyệt, đọc số tổng",
     "—",
     "- Màn danh sách thường: chỉ thấy phiếu do chính TQ-2 lập\n"
     "- Màn chờ duyệt: thấy đủ 5 phiếu của 3 người khác\n"
     "- ⚠️ Đúng thiết kế — màn chờ duyệt chỉ lọc theo công ty, không áp quyền xem theo cấp"),

    ("12", "Người lập và người duyệt luôn mở được chi tiết phiếu của mình", "P1",
     "Phiếu thu PT-02 do KT-1 lập, đã được TQ-1 duyệt; tài khoản NV-A không có quyền xem theo cấp nào "
     "và không liên quan tới phiếu này",
     "1. Đăng nhập lần lượt bằng KT-1, TQ-1 rồi NV-A\n"
     "2. Mỗi lần đều dán đường dẫn chi tiết của PT-02",
     "—",
     "- KT-1 xem được (người lập)\n"
     "- TQ-1 xem được (người duyệt)\n"
     "- NV-A bị đưa sang màn báo không tìm thấy dữ liệu"),

    ("13", "Bỏ qua giao diện gọi thẳng chức năng Xóa", "P0",
     "Tài khoản NV-A không có quyền nào của màn Phiếu thu; phiếu thu PT-02 đang ở trạng thái Đã duyệt "
     "và đã ghi sổ kế toán",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dán thẳng đường dẫn xóa của PT-02 vào thanh địa chỉ\n"
     "3. Mở lại danh sách, tìm PT-02\n"
     "4. Mở sổ kế toán, tìm bút toán của PT-02",
     "Đường dẫn xóa phiếu PT-02",
     "- ⚠️ Phiếu BỊ XÓA thật, kèm thông báo Xóa phiếu thu thành công\n"
     "- Bút toán trong sổ kế toán vẫn còn, thành bút toán mồ côi\n"
     "- Đây là lỗ hổng, ghi nhận Failed và mô tả lại đúng các bước"),

    ("14", "Bỏ qua giao diện gọi thẳng chức năng Duyệt", "P0",
     "Tài khoản NV-A không có quyền \"Thủ quỹ duyệt phiếu thu\"; phiếu thu PT-03 đang Chờ duyệt",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dùng công cụ kiểm thử gọi thẳng chức năng Cập nhật của PT-03 với trạng thái Đã duyệt\n"
     "3. Mở lại chi tiết PT-03 và mở sổ kế toán",
     "Trạng thái gửi lên: Đã duyệt",
     "- Ghi nhận đúng kết quả quan sát được: phiếu có bị chuyển sang Đã duyệt hay không, có sinh bút "
     "toán hay không\n"
     "- ⚠️ Chức năng Cập nhật KHÔNG gắn quyền ở phía hệ thống (mục 7) nên nhiều khả năng thao tác lọt; "
     "nếu lọt thì ghi Failed kèm mã phiếu để dựng phiếu ghi nhận lỗi"),
]

# ============================================================ SECTIONS
SEC_I = [
    (1, "Vào màn Phiếu thu từ menu", "P0",
     "Tài khoản KT-1 có quyền Kế toán thanh toán",
     "1. Đăng nhập bằng KT-1\n"
     "2. Mở menu Công nợ - Thu - Chi\n"
     "3. Bấm mục Phiếu thu",
     "—",
     "- Mở đúng màn danh sách, tiêu đề trang là Danh sách phiếu thu tiền\n"
     "- Bảng có đủ 11 cột theo thứ tự ở mục 2\n"
     "- Phía trên bảng có nút Bộ lọc và nút Tạo mới"),

    (2, "Chế độ Phiếu của tôi chỉ hiện phiếu mình lập", "P0",
     "Tài khoản KT-1 có quyền xem của công ty; KT-1 đã lập 8 phiếu thu trong đó có 2 phiếu nháp; công "
     "ty có hơn 40 phiếu thu",
     "1. Đăng nhập bằng KT-1\n"
     "2. Dán đường dẫn màn Phiếu thu KHÔNG kèm tham số chế độ\n"
     "3. Đọc số tổng, soát cột Người lập và cột Trạng thái",
     "—",
     "- Tổng hiện đúng 8\n"
     "- Mọi dòng đều có Người lập là KT-1\n"
     "- Cả 2 phiếu nháp của KT-1 đều hiện"),

    (3, "Chế độ Tất cả ẩn phiếu nháp của người khác", "P0",
     "Tài khoản B có quyền xem tổng công ty; KT-1 vừa Lưu nháp một phiếu thu mã kết thúc .00031",
     "1. Đăng nhập bằng B, mở mục Phiếu thu trên menu\n"
     "2. Bấm Bộ lọc, gõ .00031 vào ô Mã phiếu, bấm tìm kiếm\n"
     "3. Xóa ô mã, chọn Trạng thái là Đang tạo rồi tìm lại",
     "Mã phiếu: .00031",
     "- Bước 2 không ra dòng nào\n"
     "- Bước 3 chỉ ra phiếu nháp do chính B lập, không có phiếu của KT-1"),

    (4, "Màn Phiếu thu đã duyệt chỉ hiện phiếu mình đã duyệt", "P1",
     "Tài khoản TQ-1 đã duyệt 6 phiếu thu; trong công ty còn 9 phiếu thu Đã duyệt do thủ quỹ khác duyệt",
     "1. Đăng nhập bằng TQ-1\n"
     "2. Dán đường dẫn màn Phiếu thu đã duyệt\n"
     "3. Đọc số tổng và cột Trạng thái",
     "—",
     "- Đúng 6 dòng\n"
     "- Mọi dòng đều ở trạng thái Đã duyệt\n"
     "- Không có phiếu do thủ quỹ khác duyệt"),

    (5, "Phiếu đã hủy không lọt vào màn đã duyệt", "P1",
     "Tài khoản TQ-1 đã hủy 2 phiếu thu và đã duyệt 6 phiếu thu",
     "1. Đăng nhập bằng TQ-1, dán đường dẫn màn Phiếu thu đã duyệt\n"
     "2. Đọc số tổng",
     "—",
     "- Đúng 6 dòng, không tính 2 phiếu Hủy\n"
     "- ⚠️ Màn này lọc đồng thời hai điều kiện: mình là người duyệt VÀ trạng thái Đã duyệt"),

    (6, "Mã phiếu là đường dẫn mở chi tiết", "P1",
     "Danh sách có ít nhất 1 phiếu thu",
     "1. Mở danh sách Phiếu thu\n"
     "2. Bấm vào Mã phiếu ở dòng đầu tiên",
     "—",
     "- Mở màn Chi tiết phiếu thu tiền của đúng phiếu vừa bấm, mở trong cùng thẻ\n"
     "- Mã phiếu trên form khớp với mã vừa bấm"),

    (7, "Mã phiếu đề nghị thu mở sang màn Đề nghị thu tiền ở thẻ mới", "P1",
     "Danh sách có ít nhất 1 phiếu thu",
     "1. Mở danh sách Phiếu thu\n"
     "2. Bấm vào Mã phiếu đề nghị thu ở dòng đầu tiên",
     "—",
     "- Mở THẺ MỚI, vào màn Chi tiết phiếu đề nghị thu tiền tương ứng\n"
     "- Thẻ danh sách Phiếu thu vẫn còn nguyên"),

    (8, "Menu hành động đủ mục theo trạng thái Đang tạo", "P0",
     "Tài khoản KT-1 có quyền Kế toán thanh toán; có phiếu thu PT-N ở trạng thái Đang tạo do KT-1 lập",
     "1. Đăng nhập bằng KT-1, mở danh sách\n"
     "2. Bấm biểu tượng bánh răng ở dòng PT-N\n"
     "3. Ghi lại các mục trong menu",
     "—",
     "- Có đủ 4 mục: In · Xuất Excel · Sửa phiếu thu · Xóa"),

    (9, "Menu hành động thu gọn với phiếu đã gửi duyệt hoặc đã duyệt", "P0",
     "Có phiếu thu PT-A ở trạng thái Chờ duyệt, PT-B ở trạng thái Đã duyệt, PT-C ở trạng thái Hủy",
     "1. Mở danh sách\n"
     "2. Bấm bánh răng lần lượt ở PT-A, PT-B, PT-C\n"
     "3. Ghi lại các mục trong từng menu",
     "—",
     "- Cả 3 phiếu chỉ còn 2 mục: In và Xuất Excel\n"
     "- KHÔNG có mục Sửa phiếu thu, KHÔNG có mục Xóa"),

    (10, "Mở chi tiết phiếu không thuộc phạm vi xem", "P1",
     "Tài khoản NV-A không có quyền xem theo cấp; phiếu thu PT-D do người khác lập, trạng thái Đang tạo",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dán đường dẫn chi tiết của PT-D",
     "—",
     "- Hệ thống đưa sang màn báo không tìm thấy dữ liệu\n"
     "- Không lộ bất kỳ thông tin nào của phiếu"),

    (11, "Mở chi tiết bằng mã phiếu không tồn tại", "P2",
     "—",
     "1. Dán đường dẫn chi tiết với một mã số không có trong hệ thống\n"
     "2. Quan sát màn hình",
     "Mã số: 999999",
     "- Hệ thống báo không tìm thấy dữ liệu, không treo trang, không hiện màn trắng"),

    (12, "Số dòng mỗi trang và cột STT", "P2",
     "Danh sách có ít nhất 25 phiếu",
     "1. Mở danh sách ở chế độ Tất cả\n"
     "2. Đọc ô Hiển thị a đến b trong tổng số N\n"
     "3. Sang trang 2, đọc lại cột STT\n"
     "4. Đổi số dòng mỗi trang sang 25",
     "Số dòng mỗi trang: 10 rồi 25",
     "- Mặc định 10 dòng, ô hiển thị ghi 1 đến 10\n"
     "- Trang 2 cột STT bắt đầu từ 11\n"
     "- Đổi sang 25 thì bảng quay về trang 1"),
]

SEC_II = [
    (1, "Lọc theo Mã phiếu", "P0",
     "Tồn tại phiếu thu mã TPE.PT0826.00017",
     "1. Mở danh sách, bấm nút Bộ lọc\n"
     "2. Gõ 00017 vào ô Mã phiếu\n"
     "3. Bấm nút tìm kiếm",
     "Mã phiếu: 00017",
     "- Ra đúng phiếu TPE.PT0826.00017\n"
     "- Tìm bằng một đoạn giữa của mã vẫn ra kết quả"),

    (2, "Lọc theo Mã phiếu đề nghị thu", "P0",
     "Phiếu thu TPE.PT0826.00017 gắn với phiếu đề nghị TPE.DNTT0826.00042",
     "1. Bấm Bộ lọc, gõ DNTT0826.00042 vào ô Mã phiếu đề nghị thu\n"
     "2. Bấm tìm kiếm",
     "Mã phiếu đề nghị thu: DNTT0826.00042",
     "- Ra đúng 1 dòng là phiếu thu TPE.PT0826.00017\n"
     "- Cột Mã phiếu đề nghị thu hiện đúng mã vừa lọc"),

    (3, "Lọc theo Loại thu", "P0",
     "Danh sách có cả phiếu Thu bán hàng và phiếu Thu nhà cung cấp",
     "1. Bấm Bộ lọc, chọn Loại thu là Thu bán hàng, tìm kiếm\n"
     "2. Đổi sang Thu nhà cung cấp, tìm lại\n"
     "3. Soát cột Loại thu ở cả hai lần",
     "Loại thu: Thu bán hàng / Thu nhà cung cấp",
     "- Mỗi lần chỉ ra phiếu đúng loại đã chọn\n"
     "- ⚠️ Loại thu lấy từ phiếu đề nghị gốc, không phải thuộc tính riêng của phiếu thu"),

    (4, "Lọc theo Người lập", "P1",
     "KT-1 đã lập 8 phiếu thu, KT-2 đã lập 5 phiếu thu",
     "1. Bấm Bộ lọc, chọn KT-1 ở ô Người lập, tìm kiếm\n"
     "2. Đổi sang KT-2, tìm lại",
     "Người lập: KT-1 rồi KT-2",
     "- Lần 1 ra 8 dòng, mọi dòng có Người lập là KT-1\n"
     "- Lần 2 ra 5 dòng, mọi dòng có Người lập là KT-2"),

    (5, "Lọc theo Người đề nghị", "P1",
     "Nhân viên kinh doanh NV-B đã lập 4 phiếu đề nghị thu và cả 4 đều đã có phiếu thu",
     "1. Bấm Bộ lọc, chọn NV-B ở ô Người đề nghị, tìm kiếm\n"
     "2. Soát cột Người đề nghị",
     "Người đề nghị: NV-B",
     "- Ra đúng 4 dòng\n"
     "- Mọi dòng có Người đề nghị là NV-B, dù Người lập là kế toán khác"),

    (6, "Lọc theo khoảng Số tiền", "P0",
     "Có phiếu thu tổng 5.000.000 và phiếu thu tổng 30.000.000",
     "1. Bấm Bộ lọc, nhập Số tiền từ là 1.000.000 và Số tiền đến là 10.000.000\n"
     "2. Tìm kiếm, soát cột Số tiền\n"
     "3. Đổi khoảng thành 20.000.000 đến 50.000.000, tìm lại",
     "Số tiền từ - đến: 1.000.000 - 10.000.000 rồi 20.000.000 - 50.000.000",
     "- Lần 1 có phiếu 5.000.000, không có phiếu 30.000.000\n"
     "- Lần 2 ngược lại\n"
     "- Nhập số có dấu phân cách nghìn vẫn lọc đúng"),

    (7, "Khoảng Số tiền so với tổng cả phiếu", "P1",
     "Phiếu thu PT-E có 3 dòng, mỗi dòng 4.000.000, tổng 12.000.000",
     "1. Lọc Số tiền từ 10.000.000 đến 15.000.000, tìm kiếm\n"
     "2. Lọc Số tiền từ 3.000.000 đến 5.000.000, tìm lại",
     "—",
     "- Lần 1 có PT-E\n"
     "- Lần 2 KHÔNG có PT-E\n"
     "- ⚠️ Bộ lọc so với TỔNG cả phiếu, không so từng dòng (mục 6)"),

    (8, "Số tiền dùng để lọc đổi theo trạng thái phiếu", "P0",
     "Phiếu thu PT-F có tổng duyệt thu 12.000.000; thủ quỹ duyệt với tổng thực nhận 9.000.000",
     "1. Trước khi duyệt: lọc Số tiền từ 11.000.000 đến 13.000.000, ghi kết quả\n"
     "2. Duyệt PT-F với tổng thực nhận 9.000.000\n"
     "3. Lọc lại đúng khoảng cũ\n"
     "4. Lọc khoảng 8.000.000 đến 10.000.000",
     "—",
     "- Bước 1 có PT-F\n"
     "- Bước 3 KHÔNG còn PT-F\n"
     "- Bước 4 có PT-F\n"
     "- ⚠️ Sau khi duyệt, Số tiền chuyển sang lấy theo thực nhận (mục 6)"),

    (9, "Lọc theo Khách hàng", "P1",
     "Khách hàng KH-01 xuất hiện ở 3 phiếu thu, trong đó 1 phiếu KH-01 nằm ở dòng thứ hai",
     "1. Bấm Bộ lọc, chọn KH-01 ở ô Khách hàng, tìm kiếm\n"
     "2. Soát cột Khách hàng của từng dòng kết quả",
     "Khách hàng: KH-01",
     "- Ra đủ 3 phiếu\n"
     "- ⚠️ Phiếu có KH-01 ở dòng thứ hai vẫn ra, nhưng cột Khách hàng hiển thị tên khách của dòng đầu "
     "tiên nên nhìn như lọc sai — không phải lỗi (mục 6)"),

    (10, "Lọc theo Số Hợp đồng / Đơn hàng", "P1",
     "Phiếu thu PT-G gắn hợp đồng HD-2026-118",
     "1. Bấm Bộ lọc, gõ 2026-118 vào ô Số Hợp đồng / ĐH\n"
     "2. Tìm kiếm, mở chi tiết dòng kết quả",
     "Số Hợp đồng / ĐH: 2026-118",
     "- Ra đúng PT-G\n"
     "- Mở chi tiết thấy hợp đồng HD-2026-118 trong bảng chi tiết"),

    (11, "Lọc theo Trạng thái", "P0",
     "Danh sách có đủ phiếu ở cả 4 trạng thái",
     "1. Bấm Bộ lọc, chọn lần lượt từng trạng thái, mỗi lần bấm tìm kiếm\n"
     "2. Soát cột Trạng thái sau mỗi lần lọc",
     "Trạng thái: Đang tạo · Chờ duyệt · Đã duyệt · Hủy",
     "- Mỗi lần chỉ ra phiếu đúng trạng thái đã chọn\n"
     "- Nhãn Đã duyệt tô xanh, ba nhãn còn lại tô đỏ"),

    (12, "Bộ lọc Từ ngày và Đến ngày không có tác dụng", "P0",
     "Danh sách ở chế độ Tất cả đang có 260 phiếu; không có phiếu nào lập trong năm 2019",
     "1. Bấm Bộ lọc, ghi lại số tổng hiện tại\n"
     "2. Nhập Từ ngày 01/01/2019 và Đến ngày 31/12/2019\n"
     "3. Bấm tìm kiếm, đọc lại số tổng",
     "Từ ngày: 01/01/2019 · Đến ngày: 31/12/2019",
     "- ⚠️ Số tổng KHÔNG đổi, vẫn là 260 — hai ô ngày bị hệ thống bỏ qua hoàn toàn (mục 4)\n"
     "- Ghi nhận Failed, đây là lỗi đã biết\n"
     "- Muốn khoanh theo thời gian phải lọc bằng đoạn tháng - năm trong Mã phiếu"),

    (13, "Ô lọc Công ty lọc theo đơn vị của phiếu đề nghị", "P0",
     "Kế toán KT-9 thuộc công ty 1 đã lập một phiếu thu cho phiếu đề nghị do người của CÔNG TY 3 lập; "
     "tài khoản B có quyền xem tổng công ty",
     "1. Đăng nhập bằng B, mở chế độ Tất cả, bấm Bộ lọc\n"
     "2. Chọn Công ty là công ty 1, tìm kiếm, tìm phiếu của KT-9\n"
     "3. Đổi sang công ty 3, tìm lại",
     "Công ty: công ty 1 rồi công ty 3",
     "- Bước 2 KHÔNG có phiếu của KT-9\n"
     "- Bước 3 CÓ phiếu của KT-9\n"
     "- ⚠️ Bộ lọc đơn vị chạy theo phiếu đề nghị gốc, không theo người lập phiếu thu (mục 9 ghi chú 2)"),

    (14, "Ô lọc Phòng ban", "P1",
     "Tài khoản C có quyền xem của công ty; trong công ty có 2 phòng ban cùng phát sinh phiếu thu",
     "1. Đăng nhập bằng C, mở chế độ Tất cả, bấm Bộ lọc\n"
     "2. Chọn lần lượt từng Phòng ban rồi tìm kiếm\n"
     "3. Soát cột trong kết quả",
     "Phòng ban: lần lượt 2 phòng ban",
     "- Mỗi lần chỉ ra phiếu thuộc phòng ban đã chọn\n"
     "- ⚠️ Cũng lấy theo phòng ban của phiếu đề nghị gốc"),

    (15, "Kết hợp nhiều điều kiện lọc", "P1",
     "Có phiếu thu Thu bán hàng, trạng thái Đã duyệt, người lập KT-1, tổng tiền 9.000.000",
     "1. Bấm Bộ lọc, đặt cùng lúc: Loại thu Thu bán hàng, Trạng thái Đã duyệt, Người lập KT-1, Số tiền "
     "từ 8.000.000 đến 10.000.000\n"
     "2. Bấm tìm kiếm",
     "—",
     "- Chỉ ra phiếu khớp ĐỒNG THỜI cả 4 điều kiện\n"
     "- Mỗi phiếu chỉ hiện một dòng, không bị nhân đôi"),

    (16, "Làm mới bộ lọc", "P1",
     "Đang có ít nhất 3 ô lọc được điền",
     "1. Điền Mã phiếu, Trạng thái, Người lập rồi tìm kiếm\n"
     "2. Bấm nút làm mới bộ lọc\n"
     "3. Quan sát các ô lọc và số tổng",
     "—",
     "- Mọi ô lọc trở về rỗng\n"
     "- Bảng quay lại đủ dữ liệu như khi mới vào màn"),

    (17, "Bộ lọc được ghi nhớ theo từng chế độ danh sách", "P2",
     "—",
     "1. Ở chế độ Tất cả, đặt Trạng thái là Hủy rồi tìm kiếm\n"
     "2. Rời sang màn khác rồi quay lại chế độ Tất cả\n"
     "3. Mở chế độ Phiếu của tôi, quan sát ô Trạng thái",
     "Trạng thái: Hủy",
     "- Quay lại chế độ Tất cả: ô Trạng thái vẫn là Hủy\n"
     "- Chế độ Phiếu của tôi: ô Trạng thái KHÔNG bị dính giá trị Hủy"),

    (18, "Lọc ra không có kết quả", "P2",
     "—",
     "1. Gõ một chuỗi chắc chắn không có vào ô Mã phiếu\n"
     "2. Bấm tìm kiếm",
     "Mã phiếu: ZZZZZZ",
     "- Bảng hiện thông báo không có dữ liệu\n"
     "- Số tổng bằng 0, không báo lỗi hệ thống"),
]

SEC_III = [
    (1, "Sắp xếp mặc định theo ngày lập mới nhất", "P1",
     "Danh sách có ít nhất 30 phiếu, lập vào nhiều ngày khác nhau",
     "1. Mở danh sách, không bấm sắp xếp\n"
     "2. Đọc cột Ngày lập của 10 dòng đầu",
     "—",
     "- Phiếu lập gần nhất nằm trên cùng\n"
     "- Ngày lập giảm dần từ trên xuống"),

    (2, "Sắp xếp theo cột Số tiền", "P1",
     "Danh sách có ít nhất 30 phiếu với số tiền khác nhau",
     "1. Bấm vào tiêu đề cột Số tiền\n"
     "2. Đọc 5 dòng đầu\n"
     "3. Bấm lần nữa để đảo chiều",
     "—",
     "- Lần 1 sắp tăng dần, lần 2 sắp giảm dần\n"
     "- Số tiền so sánh theo giá trị, không so theo chuỗi ký tự"),

    (3, "Các cột còn lại không sắp xếp được", "P2",
     "—",
     "1. Bấm lần lượt vào tiêu đề Mã phiếu, Loại thu, Trạng thái, Người lập",
     "—",
     "- Không cột nào đổi thứ tự\n"
     "- ⚠️ Đúng thiết kế — chỉ cột Số tiền cho phép sắp xếp"),

    (4, "Cột Số tiền định dạng phân cách nghìn", "P1",
     "Có phiếu thu tổng 1.234.567.890",
     "1. Tìm phiếu đó trên danh sách\n"
     "2. Đọc ô Số tiền",
     "—",
     "- Hiển thị đủ dấu phân cách nghìn, không mất chữ số\n"
     "- Không hiện phần thập phân"),

    (5, "Cột Ngày lập chỉ có ngày tháng năm", "P2",
     "—",
     "1. Đọc cột Ngày lập của vài dòng bất kỳ",
     "—",
     "- Hiển thị dạng ngày/tháng/năm\n"
     "- Không kèm giờ phút"),

    (6, "Cột Khách hàng chỉ lấy dòng đầu tiên", "P0",
     "Phiếu thu PT-H có 3 dòng chi tiết với 3 khách hàng khác nhau: KH-01, KH-02, KH-03",
     "1. Tìm PT-H trên danh sách, đọc cột Khách hàng\n"
     "2. Mở chi tiết PT-H, đếm số khách hàng trong bảng",
     "—",
     "- Ngoài danh sách chỉ hiện KH-01\n"
     "- Trong chi tiết thấy đủ 3 khách hàng\n"
     "- ⚠️ Hiện trạng đã biết (mục 9 ghi chú 11), không phải lọc sai"),

    (7, "Cột Loại thu lấy từ phiếu đề nghị", "P1",
     "Phiếu thu PT-I gắn phiếu đề nghị loại Thu nhà cung cấp",
     "1. Đọc cột Loại thu của PT-I trên danh sách\n"
     "2. Mở chi tiết, đọc ô Loại thu\n"
     "3. Mở phiếu đề nghị gốc, đọc ô Loại thu",
     "—",
     "- Cả 3 chỗ đều là Thu nhà cung cấp\n"
     "- Ô Loại thu trong chi tiết phiếu thu bị khóa, không sửa được"),

    (8, "Cột Người đề nghị và Người lập là hai người khác nhau", "P1",
     "Phiếu đề nghị do NV-B lập, phiếu thu do KT-1 lập",
     "1. Tìm phiếu thu đó trên danh sách\n"
     "2. Đọc cột Người đề nghị và cột Người lập",
     "—",
     "- Người đề nghị là NV-B\n"
     "- Người lập là KT-1\n"
     "- Hai cột KHÔNG trùng nhau"),

    (9, "Số tổng khớp với dữ liệu gốc", "P0",
     "Tài khoản B có quyền xem tổng công ty",
     "1. Đăng nhập bằng B, mở chế độ Tất cả, bấm làm mới bộ lọc\n"
     "2. Đọc số tổng dưới bảng\n"
     "3. Đối chiếu với số phiếu thu trong dữ liệu gốc trừ đi phiếu nháp của người khác",
     "—",
     "- Hai con số khớp chính xác\n"
     "- ⚠️ KHÔNG đối chiếu bằng khoảng ngày vì bộ lọc ngày không chạy (mục 4)"),

    (10, "Bảng ở màn chờ duyệt giống bảng danh sách thường", "P2",
     "Tài khoản TQ-1 có quyền Thủ quỹ duyệt phiếu thu",
     "1. Đăng nhập bằng TQ-1, dán đường dẫn màn Phiếu thu chờ duyệt\n"
     "2. So sánh tiêu đề các cột với màn danh sách thường",
     "—",
     "- Cùng bộ 11 cột\n"
     "- Khác ở chỗ không có nút Tạo mới và mọi dòng đều ở trạng thái Chờ duyệt"),
]

SEC_IV = [
    (1, "Tạo phiếu thu từ màn Đề nghị thu tiền", "P0",
     "Tài khoản KT-1 có quyền Kế toán thanh toán; phiếu đề nghị DN-01 đang ở trạng thái Chờ KT duyệt, "
     "có 2 dòng chi tiết",
     "1. Đăng nhập bằng KT-1, mở chi tiết DN-01\n"
     "2. Bấm nút Tạo phiếu thu\n"
     "3. Quan sát form vừa mở",
     "—",
     "- Mở form Tạo phiếu thu tiền\n"
     "- Ô Số phiếu đề nghị đã điền sẵn mã DN-01, có thông báo thêm thành công\n"
     "- Bảng chi tiết đổ sẵn đúng 2 dòng của DN-01"),

    (2, "Chọn phiếu đề nghị bằng cửa sổ tìm kiếm", "P0",
     "Có 3 phiếu đề nghị đang Chờ KT duyệt và 5 phiếu đề nghị ở các trạng thái khác",
     "1. Mở form Tạo phiếu thu từ nút Tạo mới\n"
     "2. Bấm kính lúp ở ô Số phiếu đề nghị\n"
     "3. Đọc danh sách trong cửa sổ, chọn một phiếu",
     "—",
     "- Cửa sổ chỉ liệt kê đúng 3 phiếu Chờ KT duyệt\n"
     "- Có ô lọc Mã phiếu đề nghị thu và ô lọc Người lập\n"
     "- Chọn xong: form đổ đủ thông tin và chi tiết, hiện thông báo thêm thành công"),

    (3, "Chưa chọn phiếu đề nghị thì chưa có bảng chi tiết", "P1",
     "—",
     "1. Mở form Tạo phiếu thu từ nút Tạo mới\n"
     "2. Không chọn phiếu đề nghị, kéo xuống khối Chi tiết",
     "—",
     "- Khối Chi tiết hiển thị dòng chữ Chưa chọn phiếu đề nghị thu\n"
     "- Không có bảng nhập liệu nào"),

    (4, "Thông tin lấy từ phiếu đề nghị bị khóa", "P0",
     "Phiếu đề nghị DN-02: Loại thu Thu bán hàng, Loại tiền VND, Lý do thu là Thu tiền hàng tháng 8",
     "1. Tạo phiếu thu từ DN-02\n"
     "2. Thử bấm và sửa lần lượt ô Loại thu, Loại tiền, Lý do thu",
     "—",
     "- Ba ô hiện đúng giá trị của DN-02\n"
     "- Cả ba đều bị khóa, không gõ và không chọn lại được"),

    (5, "Tài khoản nợ mặc định là tài khoản tiền Việt Nam", "P1",
     "—",
     "1. Mở form Tạo phiếu thu\n"
     "2. Đọc ô Tài khoản nợ khi form vừa mở\n"
     "3. Mở danh sách chọn, đổi sang tài khoản khác",
     "—",
     "- Ô Tài khoản nợ đã chọn sẵn tài khoản tiền Việt Nam\n"
     "- Vẫn đổi sang tài khoản khác được"),

    (6, "Tài khoản có mặc định theo Loại thu", "P0",
     "Có phiếu đề nghị DN-03 loại Thu bán hàng và DN-04 loại Thu nhà cung cấp",
     "1. Tạo phiếu thu từ DN-03, đọc cột Số tài khoản có và cột Tên tài khoản\n"
     "2. Quay lại, tạo phiếu thu từ DN-04, đọc lại hai cột đó",
     "—",
     "- Phiếu Thu bán hàng: mọi dòng chọn sẵn tài khoản Phải thu khách hàng\n"
     "- Phiếu Thu nhà cung cấp: mọi dòng chọn sẵn tài khoản Phải trả nhà cung cấp\n"
     "- Cột Tên tài khoản hiện đúng tên của tài khoản đang chọn"),

    (7, "Đổi Số tài khoản có thì Tên tài khoản đổi theo", "P1",
     "Đang mở form Tạo phiếu thu với ít nhất 1 dòng chi tiết",
     "1. Ở dòng 1, mở danh sách Số tài khoản có\n"
     "2. Chọn một tài khoản khác\n"
     "3. Đọc cột Tên tài khoản của dòng đó",
     "—",
     "- Tên tài khoản đổi ngay theo tài khoản vừa chọn, không cần tải lại trang"),

    (8, "Số tiền duyệt thu mặc định bằng Số tiền đề nghị thu", "P0",
     "Phiếu đề nghị DN-05 có 2 dòng: dòng 1 đề nghị 5.000.000, dòng 2 đề nghị 7.000.000",
     "1. Tạo phiếu thu từ DN-05\n"
     "2. Đọc cột Số tiền đề nghị thu và cột Số tiền duyệt thu của cả 2 dòng\n"
     "3. Đọc dòng Tổng cộng",
     "—",
     "- Dòng 1: đề nghị 5.000.000, duyệt thu điền sẵn 5.000.000\n"
     "- Dòng 2: đề nghị 7.000.000, duyệt thu điền sẵn 7.000.000\n"
     "- Tổng cộng cả hai cột đều là 12.000.000"),

    (9, "Sửa Số tiền duyệt thu thì tổng cập nhật ngay", "P0",
     "Đang mở phiếu thu từ DN-05 ở ca trên",
     "1. Sửa Số tiền duyệt thu dòng 1 thành 3.000.000\n"
     "2. Rời con trỏ khỏi ô\n"
     "3. Đọc dòng Tổng cộng",
     "Số tiền duyệt thu dòng 1: 3.000.000",
     "- Tổng cột Số tiền duyệt thu đổi thành 10.000.000\n"
     "- Tổng cột Số tiền đề nghị thu vẫn 12.000.000, không bị ảnh hưởng"),

    (10, "Cột Số tiền đề nghị thu không sửa được", "P1",
     "Đang mở form Tạo phiếu thu",
     "1. Bấm vào ô Số tiền đề nghị thu của dòng 1, thử gõ số khác",
     "—",
     "- Ô chỉ hiển thị, không nhập được\n"
     "- Giá trị giữ nguyên như trên phiếu đề nghị"),

    (11, "Phiếu ngoại tệ hiện đủ cặp cột quy đổi", "P0",
     "Phiếu đề nghị DN-06 loại tiền là ngoại tệ, tỷ giá 25.000, dòng 1 đề nghị 1.000",
     "1. Tạo phiếu thu từ DN-06\n"
     "2. Đọc tiêu đề bảng chi tiết\n"
     "3. Đọc dòng 1 ở cả hai nhóm cột tiền",
     "—",
     "- Nhóm Số tiền đề nghị thu và nhóm Số tiền duyệt thu đều tách 2 cột: tên loại ngoại tệ và VND\n"
     "- Dòng 1: cột ngoại tệ 1.000, cột VND 25.000.000"),

    (12, "Sửa Tỷ giá thì cột quy đổi tính lại", "P1",
     "Đang mở phiếu thu từ DN-06 ở ca trên",
     "1. Sửa ô Tỷ giá thành 26.000\n"
     "2. Rời con trỏ khỏi ô, đọc lại cột VND của dòng 1 và dòng Tổng cộng",
     "Tỷ giá: 26.000",
     "- Cột VND dòng 1 đổi thành 26.000.000\n"
     "- Dòng Tổng cộng đổi theo"),

    (13, "Ô Tỷ giá với phiếu tiền Việt Nam", "P1",
     "Phiếu đề nghị DN-07 loại tiền là VND",
     "1. Tạo phiếu thu từ DN-07\n"
     "2. Bấm vào ô Tỷ giá, thử gõ số khác",
     "Tỷ giá: gõ thử 5",
     "- Kỳ vọng nghiệp vụ: ô Tỷ giá bị khóa với phiếu tiền Việt Nam\n"
     "- ⚠️ Kiểm kỹ, ô này có thể vẫn sửa được do cách so sánh loại tiền (mục 9 ghi chú 13). Nếu sửa "
     "được thì ghi Failed kèm ảnh chụp màn hình"),

    (14, "Không thêm và không xóa được dòng chi tiết", "P1",
     "Đang mở form Tạo phiếu thu với 2 dòng chi tiết",
     "1. Soát toàn bộ bảng chi tiết tìm biểu tượng dấu cộng hoặc thùng rác\n"
     "2. Đếm số dòng, so với số dòng của phiếu đề nghị gốc",
     "—",
     "- Không có nút thêm dòng, không có nút xóa dòng\n"
     "- Số dòng đúng bằng số dòng của phiếu đề nghị"),

    (15, "Lưu nháp phiếu thu", "P0",
     "Đang mở form Tạo phiếu thu từ DN-05, đã nhập Người nộp là Nguyễn Văn A",
     "1. Bấm nút Lưu\n"
     "2. Đọc thông báo và màn hình đích\n"
     "3. Mở lại phiếu đề nghị DN-05, đọc trạng thái",
     "Người nộp: Nguyễn Văn A",
     "- Thông báo Thêm phiếu thu tiền thành công\n"
     "- Chuyển về danh sách chế độ Tất cả, phiếu mới ở trạng thái Đang tạo\n"
     "- ⚠️ DN-05 VẪN ở trạng thái Chờ KT duyệt, chưa đổi"),

    (16, "Lưu và gửi duyệt phiếu thu", "P0",
     "Đang mở form Tạo phiếu thu từ DN-08, đã nhập đủ Người nộp và Tài khoản nợ",
     "1. Bấm nút Lưu và gửi duyệt\n"
     "2. Đọc thông báo\n"
     "3. Mở danh sách, đọc trạng thái phiếu vừa tạo\n"
     "4. Mở phiếu đề nghị DN-08, đọc trạng thái",
     "—",
     "- Thông báo dài, nội dung là phiếu cần được duyệt trước khi có hiệu lực, theo dõi thông báo\n"
     "- Phiếu thu ở trạng thái Chờ duyệt\n"
     "- DN-08 chuyển sang trạng thái Đã tạo phiếu thu"),

    (17, "Mã phiếu sinh tự động và tăng dần", "P0",
     "Công ty của KT-1 có mã TPE; trong tháng hiện tại đã có phiếu thu TPE.PT0826.00016",
     "1. Tạo và lưu 2 phiếu thu liên tiếp\n"
     "2. Đọc Mã phiếu của cả hai trên danh sách",
     "—",
     "- Mã lần lượt là TPE.PT0826.00017 và TPE.PT0826.00018\n"
     "- Không trùng mã, không nhảy số"),

    (18, "Chặn lập phiếu thu thứ hai cho cùng một phiếu đề nghị", "P0",
     "Phiếu đề nghị DN-09 đã được lập phiếu thu và lưu thành công",
     "1. Mở form Tạo phiếu thu mới\n"
     "2. Chọn lại DN-09 ở cửa sổ Số phiếu đề nghị\n"
     "3. Nhập đủ thông tin bắt buộc rồi bấm Lưu",
     "—",
     "- Bước 2: nếu DN-09 đã sang trạng thái Đã tạo phiếu thu thì cửa sổ không còn liệt kê nó\n"
     "- Nếu vẫn chọn được: bấm Lưu hệ thống báo Đề nghị thu tiền đã lập phiếu thu tiền, không tạo "
     "phiếu thứ hai"),

    (19, "Mở màn Sửa phiếu thu", "P0",
     "Tài khoản KT-1; phiếu thu PT-N ở trạng thái Đang tạo do KT-1 lập, Người nộp là Nguyễn Văn A",
     "1. Bấm bánh răng ở PT-N, bấm Sửa phiếu thu\n"
     "2. Đọc các ô trên form",
     "—",
     "- Form hiện thêm ô Mã phiếu (bị khóa) so với màn tạo mới\n"
     "- Có thêm ô Người đề nghị, Người tạo, Phòng ban, đều bị khóa\n"
     "- Người nộp hiện Nguyễn Văn A, sửa được"),

    (20, "Sửa và lưu lại nháp", "P0",
     "Đang mở màn Sửa của PT-N",
     "1. Đổi Người nộp thành Trần Thị B\n"
     "2. Đổi Số tiền duyệt thu dòng 1 thành 2.000.000\n"
     "3. Bấm Lưu\n"
     "4. Mở lại chi tiết PT-N",
     "Người nộp: Trần Thị B · Duyệt thu dòng 1: 2.000.000",
     "- Thông báo Cập nhật phiếu thu tiền thành công\n"
     "- Mở lại thấy đúng hai giá trị vừa sửa\n"
     "- Cột Số tiền ngoài danh sách tính lại theo tổng duyệt thu mới"),

    (21, "Sửa rồi gửi duyệt", "P0",
     "Đang mở màn Sửa của PT-N ở trạng thái Đang tạo",
     "1. Bấm Lưu và gửi duyệt\n"
     "2. Mở danh sách, đọc trạng thái PT-N\n"
     "3. Mở phiếu đề nghị gốc, đọc trạng thái",
     "—",
     "- PT-N chuyển sang Chờ duyệt\n"
     "- Phiếu đề nghị gốc chuyển sang Đã tạo phiếu thu\n"
     "- Thủ quỹ nhận được thông báo"),

    (22, "Dán thẳng đường dẫn sửa phiếu đã gửi duyệt", "P0",
     "Tài khoản KT-1 có quyền Kế toán thanh toán; phiếu thu PT-A đang ở trạng thái Chờ duyệt",
     "1. Đăng nhập bằng KT-1\n"
     "2. Dán thẳng đường dẫn sửa của PT-A vào thanh địa chỉ\n"
     "3. Nếu form mở ra thì sửa Người nộp rồi bấm Lưu",
     "—",
     "- ⚠️ Form VẪN mở được và VẪN lưu được (mục 9 ghi chú 4)\n"
     "- Ghi nhận Failed, mô tả rõ phiếu ở trạng thái nào vẫn sửa được"),

    (23, "Xem chi tiết phiếu đã duyệt", "P1",
     "Phiếu thu PT-B ở trạng thái Đã duyệt, có Số tiền thực nhận và Ghi chú",
     "1. Mở chi tiết PT-B\n"
     "2. Soát các ô và các cột",
     "—",
     "- Hiện đủ 3 nhóm cột tiền: đề nghị thu, duyệt thu, thực nhận\n"
     "- Không có nút Duyệt phiếu thu và Hủy phiếu thu\n"
     "- Ghi chú hiện đúng nội dung đã nhập lúc duyệt"),
]

SEC_V = [
    (1, "Thủ quỹ mở phiếu chờ duyệt", "P0",
     "Tài khoản TQ-1 có quyền Thủ quỹ duyệt phiếu thu; phiếu PT-A ở trạng thái Chờ duyệt, cùng công ty",
     "1. Đăng nhập bằng TQ-1, dán đường dẫn màn Phiếu thu chờ duyệt\n"
     "2. Bấm Mã phiếu của PT-A\n"
     "3. Soát khu vực nút phía dưới form",
     "—",
     "- Mở được chi tiết\n"
     "- Có nút Duyệt phiếu thu và nút Hủy phiếu thu\n"
     "- Có ô Ghi chú nhập được, ô Số tiền phân bổ và cột Số tiền thực nhận nhập được"),

    (2, "Số tiền thực nhận mặc định bằng Số tiền duyệt thu", "P0",
     "Phiếu PT-A có 2 dòng: duyệt thu 5.000.000 và 7.000.000",
     "1. TQ-1 mở chi tiết PT-A\n"
     "2. Đọc cột Số tiền thực nhận của cả 2 dòng và dòng Tổng cộng",
     "—",
     "- Dòng 1 thực nhận 5.000.000, dòng 2 thực nhận 7.000.000\n"
     "- Tổng cột thực nhận là 12.000.000"),

    (3, "Nhập thực nhận nhỏ hơn duyệt thu", "P0",
     "Đang mở PT-A",
     "1. Sửa Số tiền thực nhận dòng 1 thành 3.000.000\n"
     "2. Rời con trỏ, đọc dòng Tổng cộng",
     "Thực nhận dòng 1: 3.000.000",
     "- Ô nhận đúng 3.000.000\n"
     "- Tổng cột thực nhận đổi thành 10.000.000\n"
     "- Cột duyệt thu không đổi"),

    (4, "Nhập thực nhận lớn hơn duyệt thu bị kéo về", "P0",
     "Đang mở PT-A, dòng 1 có duyệt thu 5.000.000",
     "1. Sửa Số tiền thực nhận dòng 1 thành 9.000.000\n"
     "2. Rời con trỏ, đọc lại ô",
     "Thực nhận dòng 1: 9.000.000",
     "- Ô tự đổi về 5.000.000\n"
     "- ⚠️ KHÔNG có thông báo nào báo là đã bị kéo về (mục 9 ghi chú 8)"),

    (5, "Nhập thực nhận bằng 0", "P1",
     "Đang mở PT-A với 2 dòng",
     "1. Sửa Số tiền thực nhận dòng 2 thành 0\n"
     "2. Bấm Duyệt phiếu thu\n"
     "3. Mở sổ kế toán tìm bút toán của phiếu",
     "Thực nhận dòng 2: 0",
     "- Duyệt được bình thường\n"
     "- Sổ kế toán CHỈ có bút toán của dòng 1, dòng 2 không sinh bút toán (mục 6)"),

    (6, "Phân bổ nhanh bằng ô Số tiền phân bổ", "P0",
     "Phiếu PT-J có 3 dòng, duyệt thu lần lượt 5.000.000 · 3.000.000 · 2.000.000",
     "1. TQ-1 mở chi tiết PT-J\n"
     "2. Nhập 7.000.000 vào ô Số tiền phân bổ\n"
     "3. Bấm nút phân bổ\n"
     "4. Đọc cột Số tiền thực nhận của cả 3 dòng",
     "Số tiền phân bổ: 7.000.000",
     "- Dòng 1 nhận 5.000.000\n"
     "- Dòng 2 nhận 2.000.000\n"
     "- Dòng 3 nhận 0"),

    (7, "Phân bổ vượt tổng duyệt thu", "P1",
     "Phiếu PT-J tổng duyệt thu 10.000.000",
     "1. Nhập 30.000.000 vào ô Số tiền phân bổ\n"
     "2. Bấm nút phân bổ\n"
     "3. Đọc cột thực nhận và dòng Tổng cộng",
     "Số tiền phân bổ: 30.000.000",
     "- Mỗi dòng chỉ nhận tối đa bằng duyệt thu của dòng đó\n"
     "- Tổng thực nhận bằng 10.000.000, phần dư bị bỏ"),

    (8, "Phân bổ bằng 0", "P2",
     "Phiếu PT-J",
     "1. Nhập 0 vào ô Số tiền phân bổ, bấm nút phân bổ\n"
     "2. Đọc cột thực nhận",
     "Số tiền phân bổ: 0",
     "- Ghi nhận đúng hiện tượng quan sát được ở cả 3 dòng\n"
     "- Không báo lỗi hệ thống, không treo trang"),

    (9, "Bảng con phiếu yêu cầu xuất hàng của hợp đồng nguyên tắc", "P0",
     "Phiếu PT-K có 1 dòng gắn hợp đồng nguyên tắc, không tích Thu dư nợ đầu kỳ, có 3 phiếu yêu cầu "
     "xuất hàng",
     "1. TQ-1 mở chi tiết PT-K\n"
     "2. Quan sát ô Số đơn hàng - Hợp đồng của dòng 1",
     "—",
     "- Dưới ô hợp đồng bung ra bảng con 4 cột: Số phiếu · Giá trị · Đã thu · Số tiền thu\n"
     "- Có đủ 3 dòng phiếu yêu cầu xuất hàng\n"
     "- Cột Số tiền thu nhập được, có nút phân bổ ở tiêu đề cột"),

    (10, "Phân bổ trong bảng con phiếu yêu cầu xuất hàng", "P0",
     "Phiếu PT-K, dòng 1 có thực nhận 8.000.000; ba phiếu xuất còn phải thu lần lượt 5.000.000 · "
     "2.000.000 · 6.000.000",
     "1. Đặt Số tiền thực nhận dòng 1 là 8.000.000\n"
     "2. Bấm nút phân bổ ở tiêu đề cột Số tiền thu trong bảng con\n"
     "3. Đọc cột Số tiền thu của 3 phiếu xuất",
     "Thực nhận dòng 1: 8.000.000",
     "- Phiếu xuất 1 nhận 5.000.000\n"
     "- Phiếu xuất 2 nhận 2.000.000\n"
     "- Phiếu xuất 3 nhận phần dư 1.000.000\n"
     "- Tổng cột Số tiền thu bằng đúng 8.000.000"),

    (11, "Chặn duyệt khi bảng con phân bổ lệch", "P0",
     "Phiếu PT-K, dòng 1 thực nhận 8.000.000 nhưng tổng cột Số tiền thu trong bảng con chỉ là 7.000.000",
     "1. Sửa Số tiền thu của phiếu xuất 3 xuống 0\n"
     "2. Bấm Duyệt phiếu thu\n"
     "3. Quan sát màn hình",
     "—",
     "- Hiện cảnh báo Tổng số tiền thu và số tiền thực nhận không khớp nhau\n"
     "- Phiếu KHÔNG được duyệt, vẫn ở trạng thái Chờ duyệt\n"
     "- Không có bút toán nào được ghi"),

    (12, "Duyệt phiếu thu thành công", "P0",
     "Phiếu PT-A, thực nhận dòng 1 là 3.000.000 và dòng 2 là 7.000.000; TQ-1 đã nhập Ghi chú",
     "1. Bấm Duyệt phiếu thu\n"
     "2. Đọc thông báo và màn hình đích\n"
     "3. Mở lại chi tiết PT-A\n"
     "4. Mở phiếu đề nghị gốc, đọc trạng thái",
     "Ghi chú: Thu đủ theo thỏa thuận",
     "- Thông báo Duyệt phiếu thu thành công\n"
     "- Hệ thống chuyển sang màn Phiếu thu đã duyệt\n"
     "- PT-A ở trạng thái Đã duyệt, Người duyệt là TQ-1\n"
     "- Phiếu đề nghị gốc chuyển sang trạng thái Đã hạch toán"),

    (13, "Ngày hạch toán đóng dấu ngày bấm duyệt", "P1",
     "Phiếu PT-L lập ngày 10/08/2026, hôm nay là 20/08/2026",
     "1. TQ-1 duyệt PT-L hôm nay\n"
     "2. Mở lại chi tiết, tìm giá trị Ngày hạch toán\n"
     "3. Mở sổ kế toán, đọc ngày của bút toán",
     "—",
     "- Ngày hạch toán là 20/08/2026, không phải 10/08/2026\n"
     "- Người dùng không chọn được ngày này"),

    (14, "Duyệt lại phiếu đã duyệt", "P0",
     "Phiếu PT-A đã ở trạng thái Đã duyệt",
     "1. Dùng công cụ kiểm thử gọi lại chức năng Duyệt cho PT-A\n"
     "2. Đọc thông báo\n"
     "3. Mở sổ kế toán, đếm số bút toán của PT-A",
     "Trạng thái gửi lên: Đã duyệt",
     "- Hệ thống báo Phiếu thu tiền đã được duyệt\n"
     "- Số bút toán KHÔNG tăng thêm, không bị ghi trùng"),

    (15, "Hủy phiếu thu khi chưa nhập Ghi chú", "P0",
     "Phiếu PT-M ở trạng thái Chờ duyệt, ô Ghi chú đang trống",
     "1. TQ-1 mở chi tiết PT-M\n"
     "2. Bấm Hủy phiếu thu\n"
     "3. Bấm Xác nhận trên hộp thoại\n"
     "4. Quan sát ô Ghi chú",
     "Ghi chú: để trống",
     "- Hộp thoại xác nhận hiện ra trước\n"
     "- Sau khi xác nhận: hệ thống báo lỗi Bắt buộc nhập ngay dưới ô Ghi chú\n"
     "- Phiếu KHÔNG bị hủy, vẫn ở Chờ duyệt"),

    (16, "Hủy phiếu thu thành công", "P0",
     "Phiếu PT-M ở trạng thái Chờ duyệt",
     "1. Nhập Ghi chú là Khách hủy thanh toán\n"
     "2. Bấm Hủy phiếu thu, bấm Xác nhận\n"
     "3. Mở danh sách, đọc trạng thái PT-M\n"
     "4. Mở phiếu đề nghị gốc, đọc trạng thái\n"
     "5. Mở sổ kế toán",
     "Ghi chú: Khách hủy thanh toán",
     "- Thông báo Hủy phiếu thu thành công\n"
     "- PT-M ở trạng thái Hủy\n"
     "- Phiếu đề nghị gốc chuyển sang trạng thái Hủy\n"
     "- KHÔNG có bút toán nào được ghi"),

    (17, "Bấm Hủy rồi chọn không xác nhận", "P1",
     "Phiếu PT-M ở trạng thái Chờ duyệt",
     "1. Bấm Hủy phiếu thu\n"
     "2. Trên hộp thoại, bấm nút Hủy để đóng\n"
     "3. Mở lại danh sách",
     "—",
     "- Hộp thoại đóng lại\n"
     "- Phiếu vẫn ở trạng thái Chờ duyệt, không có gì thay đổi"),

    (18, "Ô Tỷ giá trong màn chi tiết không bị khóa", "P0",
     "Phiếu PT-P là phiếu ngoại tệ, tỷ giá đang là 25.000, tổng thực nhận 1.000 ngoại tệ",
     "1. TQ-1 mở chi tiết PT-P\n"
     "2. Sửa ô Tỷ giá thành 30.000\n"
     "3. Đọc lại cột quy đổi VND và dòng Tổng cộng\n"
     "4. Bấm Duyệt phiếu thu rồi mở sổ kế toán",
     "Tỷ giá: 30.000",
     "- ⚠️ Ô Tỷ giá SỬA ĐƯỢC, không bị khóa (mục 9 ghi chú 7)\n"
     "- Cột VND nhảy từ 25.000.000 lên 30.000.000\n"
     "- Bút toán ghi theo số mới, không có cảnh báo nào\n"
     "- Ghi nhận Failed kèm ảnh chụp"),

    (19, "Thông báo tới thủ quỹ khi có phiếu cần duyệt", "P0",
     "Tài khoản TQ-1 và TQ-2 đều có quyền Thủ quỹ duyệt phiếu thu",
     "1. KT-1 bấm Lưu và gửi duyệt một phiếu thu\n"
     "2. Đăng nhập bằng TQ-1, mở khu vực thông báo\n"
     "3. Bấm vào thông báo mới nhất\n"
     "4. Đăng nhập bằng TQ-2, kiểm tra thông báo",
     "—",
     "- Cả TQ-1 và TQ-2 đều nhận thông báo, nội dung là có một phiếu thu tiền cần duyệt kèm tên KT-1\n"
     "- Bấm vào thông báo mở đúng chi tiết phiếu vừa gửi"),

    (20, "Chỉ Lưu nháp thì không gửi thông báo", "P1",
     "—",
     "1. KT-1 tạo phiếu thu và bấm Lưu (không gửi duyệt)\n"
     "2. Đăng nhập bằng TQ-1, mở khu vực thông báo",
     "—",
     "- Không có thông báo mới nào về phiếu thu này\n"
     "- Phiếu cũng không xuất hiện ở màn Phiếu thu chờ duyệt"),
]

SEC_VI = [
    (1, "Xóa phiếu thu ở trạng thái Đang tạo", "P0",
     "Tài khoản KT-1; phiếu PT-N ở trạng thái Đang tạo, có 2 dòng chi tiết",
     "1. Bấm bánh răng ở PT-N, bấm Xóa\n"
     "2. Bấm Xác nhận trên hộp thoại\n"
     "3. Tìm lại PT-N trên danh sách",
     "—",
     "- Thông báo Xóa phiếu thu thành công\n"
     "- PT-N biến mất khỏi danh sách\n"
     "- Mở lại đường dẫn chi tiết của PT-N thì báo không tìm thấy dữ liệu"),

    (2, "Bấm Xóa rồi chọn không xác nhận", "P1",
     "Phiếu PT-N ở trạng thái Đang tạo",
     "1. Bấm bánh răng, bấm Xóa\n"
     "2. Trên hộp thoại, bấm nút Hủy\n"
     "3. Tải lại danh sách",
     "—",
     "- Hộp thoại đóng, phiếu vẫn còn nguyên trên danh sách"),

    (3, "Phiếu đã gửi duyệt không có nút Xóa", "P0",
     "Phiếu PT-A ở trạng thái Chờ duyệt",
     "1. Bấm bánh răng ở PT-A\n"
     "2. Soát các mục trong menu",
     "—",
     "- Không có mục Xóa\n"
     "- Chỉ còn In và Xuất Excel"),

    (4, "Dán thẳng đường dẫn xóa phiếu đã duyệt", "P0",
     "Tài khoản KT-1; phiếu PT-B ở trạng thái Đã duyệt và đã ghi sổ kế toán",
     "1. Đăng nhập bằng KT-1\n"
     "2. Dán thẳng đường dẫn xóa của PT-B\n"
     "3. Tìm lại PT-B trên danh sách\n"
     "4. Mở sổ kế toán, tìm bút toán của PT-B",
     "—",
     "- ⚠️ Phiếu BỊ XÓA thật kèm thông báo thành công (mục 9 ghi chú 3)\n"
     "- Bút toán vẫn còn trong sổ, thành bút toán mồ côi\n"
     "- Ghi nhận Failed"),

    (5, "Phiếu đề nghị kẹt trạng thái sau khi xóa phiếu thu", "P0",
     "Phiếu đề nghị DN-10 đã có phiếu thu PT-Q ở trạng thái Chờ duyệt, DN-10 đang ở Đã tạo phiếu thu",
     "1. Xóa PT-Q\n"
     "2. Mở chi tiết DN-10, đọc trạng thái\n"
     "3. Soát khu vực nút phía dưới, tìm nút Tạo phiếu thu\n"
     "4. Mở form Tạo phiếu thu mới, tìm DN-10 trong cửa sổ chọn",
     "—",
     "- ⚠️ DN-10 VẪN ở trạng thái Đã tạo phiếu thu, không trở về Chờ KT duyệt\n"
     "- Không còn nút Tạo phiếu thu\n"
     "- Cửa sổ chọn không liệt kê DN-10 nữa, phiếu đề nghị bị kẹt (mục 9 ghi chú 5)\n"
     "- Ghi nhận Failed"),

    (6, "Xóa phiếu thu thì dòng chi tiết cũng bị xóa", "P1",
     "Phiếu PT-R ở trạng thái Đang tạo, có 3 dòng chi tiết và 1 bảng con phân bổ",
     "1. Xóa PT-R\n"
     "2. Tạo phiếu thu mới cho một phiếu đề nghị khác\n"
     "3. Soát bảng chi tiết của phiếu mới",
     "—",
     "- Bảng chi tiết của phiếu mới chỉ có dòng của phiếu đề nghị mới\n"
     "- Không lẫn dòng nào của PT-R vừa xóa"),
]

SEC_VII = [
    (1, "In phiếu thu bán hàng một khách hàng", "P0",
     "Phiếu PT-S gắn đề nghị loại Thu bán hàng, chỉ có 1 dòng chi tiết, đã duyệt với thực nhận 9.000.000",
     "1. Bấm bánh răng ở PT-S, bấm In\n"
     "2. Quan sát bản in",
     "—",
     "- Ra mẫu phiếu thu tiền bán hàng dành cho một khách hàng\n"
     "- Có đủ 2 liên, in trên CÙNG MỘT trang\n"
     "- Ô Liên số ghi lần lượt 1 và 2\n"
     "- Số tiền và dòng Bằng chữ đều theo 9.000.000"),

    (2, "In phiếu thu bán hàng nhiều khách hàng", "P0",
     "Phiếu PT-H gắn đề nghị loại Thu bán hàng, có 3 dòng chi tiết",
     "1. Bấm In ở PT-H\n"
     "2. Đếm số trang và số liên",
     "—",
     "- Ra mẫu dành cho nhiều khách hàng\n"
     "- Hai liên nằm ở HAI trang riêng\n"
     "- Bảng chi tiết liệt kê đủ 3 khách hàng"),

    (3, "In phiếu thu nhà cung cấp", "P1",
     "Có phiếu PT-T loại Thu nhà cung cấp 1 dòng và PT-U loại Thu nhà cung cấp 3 dòng",
     "1. Bấm In lần lượt ở PT-T và PT-U\n"
     "2. So sánh hai bản in",
     "—",
     "- PT-T ra mẫu phiếu thu tiền nhà cung cấp một nhà cung cấp\n"
     "- PT-U ra mẫu nhiều nhà cung cấp\n"
     "- Tiêu đề cột trên bản in ghi Nhà cung cấp, không ghi Khách hàng"),

    (4, "Bản in phiếu ngoại tệ", "P1",
     "Phiếu PT-P là phiếu ngoại tệ, tỷ giá lưu trong phiếu là 25.000",
     "1. Bấm In ở PT-P\n"
     "2. Đọc dòng Tỷ giá ngoại tệ và cột số tiền",
     "—",
     "- Bản in có dòng Tỷ giá ngoại tệ và dòng Số tiền quy đổi\n"
     "- ⚠️ Tỷ giá in ra lấy từ danh mục tiền tệ ở thời điểm in, có thể khác 25.000 đã lưu trong phiếu "
     "(mục 9 ghi chú 14). Đổi tỷ giá trong danh mục rồi in lại để xác nhận"),

    (5, "In phiếu chưa duyệt", "P1",
     "Phiếu PT-A ở trạng thái Chờ duyệt, tổng duyệt thu 12.000.000, chưa có thực nhận",
     "1. Bấm In ở PT-A\n"
     "2. Đọc số tiền và dòng Bằng chữ",
     "—",
     "- Vẫn in được, không bị chặn\n"
     "- Số tiền lấy theo Số tiền đề nghị thu vì thực nhận đang bằng 0 (mục 8)"),

    (6, "Dòng Người nộp trên bản in", "P0",
     "Phiếu PT-S đã nhập Người nộp là Nguyễn Văn A trên form phiếu thu; phiếu đề nghị gốc không có ô "
     "Người nộp",
     "1. Mở chi tiết PT-S, xác nhận ô Người nộp là Nguyễn Văn A\n"
     "2. Bấm In, đọc dòng Người nộp tiền trên bản in",
     "—",
     "- ⚠️ Dòng Người nộp tiền trên bản in TRỐNG, không hiện Nguyễn Văn A (mục 9 ghi chú 9)\n"
     "- Ghi nhận Failed"),

    (7, "Dòng Người đề nghị lệch nhau giữa bản in và tệp Excel", "P0",
     "Phiếu đề nghị do NV-B lập, phiếu thu PT-S do KT-1 lập",
     "1. Bấm In PT-S, đọc dòng Người đề nghị\n"
     "2. Bấm Xuất Excel PT-S, mở tệp, đọc dòng Người đề nghị",
     "—",
     "- ⚠️ Bản in ghi NV-B, tệp Excel ghi KT-1 (mục 9 ghi chú 10)\n"
     "- Ghi nhận Failed, nêu rõ chỗ nào mới đúng nghiệp vụ"),

    (8, "Xuất Excel", "P0",
     "Phiếu PT-S đã duyệt",
     "1. Bấm bánh răng ở PT-S, bấm Xuất Excel\n"
     "2. Mở tệp vừa tải\n"
     "3. Đối chiếu số tiền, khách hàng, số hợp đồng với màn chi tiết",
     "—",
     "- Tải về tệp có tên phieu_thu\n"
     "- Tệp mở được, không báo hỏng\n"
     "- Các giá trị khớp với màn chi tiết"),

    (9, "In phiếu gắn đề nghị loại Thu khác", "P1",
     "Trong dữ liệu cũ có phiếu thu PT-V gắn phiếu đề nghị loại Thu khác",
     "1. Tìm PT-V trên danh sách\n"
     "2. Bấm In",
     "—",
     "- ⚠️ Hệ thống không có mẫu in cho loại này, nhiều khả năng ra trang lỗi (mục 9 ghi chú 12)\n"
     "- Ghi nhận đúng hiện tượng quan sát được; nếu ra trang lỗi thì Failed"),

    (10, "In và Xuất Excel với phiếu không tồn tại", "P2",
     "—",
     "1. Dán đường dẫn in với một mã số không có trong hệ thống\n"
     "2. Làm tương tự với đường dẫn xuất Excel",
     "Mã số: 999999",
     "- Cả hai đều báo không tìm thấy dữ liệu\n"
     "- Không treo trang, không tải về tệp rỗng"),
]

SEC_VIII = [
    (1, "Bỏ trống Số phiếu đề nghị", "P0",
     "Đang mở form Tạo phiếu thu, chưa chọn phiếu đề nghị",
     "1. Nhập Người nộp là Nguyễn Văn A\n"
     "2. Bấm Lưu",
     "Người nộp: Nguyễn Văn A",
     "- Lỗi đỏ Bắt buộc nhập hiện ngay dưới ô Số phiếu đề nghị\n"
     "- Không tạo phiếu, dữ liệu đã nhập vẫn còn trên form"),

    (2, "Bỏ trống Tài khoản nợ", "P0",
     "Đang mở form Tạo phiếu thu đã chọn phiếu đề nghị",
     "1. Mở ô Tài khoản nợ, bỏ chọn về trạng thái rỗng\n"
     "2. Nhập đủ Người nộp rồi bấm Lưu",
     "Tài khoản nợ: để rỗng",
     "- Lỗi đỏ Bắt buộc nhập hiện dưới ô Tài khoản nợ\n"
     "- Không tạo phiếu"),

    (3, "Bỏ trống Người nộp", "P0",
     "Đang mở form Tạo phiếu thu đã chọn phiếu đề nghị",
     "1. Để trống ô Người nộp\n"
     "2. Bấm Lưu",
     "Người nộp: để trống",
     "- Lỗi đỏ Bắt buộc nhập hiện dưới ô Người nộp\n"
     "- Không tạo phiếu"),

    (4, "Bỏ trống Số tài khoản có ở một dòng chi tiết", "P0",
     "Đang mở form Tạo phiếu thu với 3 dòng chi tiết",
     "1. Ở dòng 2, mở danh sách Số tài khoản có rồi bỏ chọn\n"
     "2. Bấm Lưu",
     "Số tài khoản có dòng 2: để rỗng",
     "- Lỗi đỏ Bắt buộc nhập hiện ngay dưới ô của ĐÚNG DÒNG 2\n"
     "- Dòng 1 và dòng 3 không bị báo lỗi"),

    (5, "Bỏ trống Số tiền duyệt thu", "P0",
     "Đang mở form Tạo phiếu thu với 2 dòng",
     "1. Xóa trắng ô Số tiền duyệt thu dòng 1\n"
     "2. Bấm Lưu",
     "Số tiền duyệt thu dòng 1: để trống",
     "- Hệ thống báo lỗi ở dòng 1, ghi rõ bắt buộc nhập\n"
     "- Không tạo phiếu"),

    (6, "Nhập Số tiền duyệt thu là số âm", "P0",
     "Đang mở form Tạo phiếu thu",
     "1. Nhập -1.000.000 vào ô Số tiền duyệt thu dòng 1\n"
     "2. Bấm Lưu",
     "Số tiền duyệt thu dòng 1: -1.000.000",
     "- Hệ thống chặn, báo lỗi ở dòng 1\n"
     "- Không lưu giá trị âm vào phiếu"),

    (7, "Nhập chữ vào ô số tiền", "P1",
     "Đang mở form Tạo phiếu thu",
     "1. Gõ abc vào ô Số tiền duyệt thu dòng 1\n"
     "2. Rời con trỏ, đọc lại ô và dòng Tổng cộng\n"
     "3. Bấm Lưu",
     "Số tiền duyệt thu dòng 1: abc",
     "- Ô hiển thị 0 hoặc bị chặn ngay khi gõ\n"
     "- Dòng Tổng cộng không hiện giá trị lạ\n"
     "- Không lưu giá trị rác"),

    (8, "Nhập số tiền có dấu phân cách nghìn", "P1",
     "Đang mở form Tạo phiếu thu",
     "1. Gõ 1.234.567 vào ô Số tiền duyệt thu dòng 1\n"
     "2. Rời con trỏ, đọc dòng Tổng cộng\n"
     "3. Lưu rồi mở lại chi tiết",
     "Số tiền duyệt thu dòng 1: 1.234.567",
     "- Hệ thống hiểu đúng một triệu hai trăm ba mươi tư nghìn năm trăm sáu mươi bảy\n"
     "- Tổng cộng và cột quy đổi tính đúng\n"
     "- Mở lại thấy đúng số đã nhập"),

    (9, "Nhập số tiền có phần thập phân", "P1",
     "Phiếu ngoại tệ, tỷ giá 25.000",
     "1. Gõ 1234,56 vào ô Số tiền duyệt thu dòng 1\n"
     "2. Đọc cột quy đổi VND\n"
     "3. Lưu rồi mở lại chi tiết",
     "Số tiền duyệt thu dòng 1: 1234,56",
     "- Giữ đủ 2 chữ số thập phân ở cả ô nhập, cột quy đổi và dòng Tổng cộng\n"
     "- Mở lại không bị làm tròn mất số lẻ"),

    (10, "Nhập số tiền rất lớn", "P1",
     "Đang mở form Tạo phiếu thu, phiếu tiền Việt Nam",
     "1. Gõ 999.999.999.999 vào ô Số tiền duyệt thu dòng 1\n"
     "2. Lưu, mở danh sách đọc cột Số tiền\n"
     "3. Bấm In, đọc dòng Bằng chữ",
     "Số tiền duyệt thu dòng 1: 999.999.999.999",
     "- Cột Số tiền hiển thị đủ chữ số, không tràn cột\n"
     "- Dòng Bằng chữ đọc đúng, không cụt"),

    (11, "Bỏ trống Ghi chú khi hủy phiếu", "P0",
     "Phiếu PT-M ở trạng thái Chờ duyệt",
     "1. Thủ quỹ mở chi tiết, để trống Ghi chú\n"
     "2. Bấm Hủy phiếu thu, xác nhận",
     "Ghi chú: để trống",
     "- Lỗi đỏ Bắt buộc nhập hiện dưới ô Ghi chú\n"
     "- Phiếu không bị hủy"),

    (12, "Ký tự đặc biệt trong ô Người nộp và Ghi chú", "P1",
     "Đang mở form Tạo phiếu thu",
     "1. Nhập chuỗi có dấu ngoặc nhọn và chữ script vào ô Người nộp\n"
     "2. Lưu, mở danh sách, mở chi tiết, bấm In\n"
     "3. Quan sát cả ba chỗ",
     "Người nộp: chuỗi chứa thẻ script",
     "- Chuỗi hiển thị nguyên văn dạng chữ ở cả ba chỗ\n"
     "- Không có cửa sổ bật lên, không có đoạn mã nào chạy"),

    (13, "Nhập Người nộp rất dài", "P2",
     "Đang mở form Tạo phiếu thu",
     "1. Nhập chuỗi 300 ký tự vào ô Người nộp\n"
     "2. Lưu, mở lại chi tiết và bấm In",
     "Người nộp: chuỗi 300 ký tự",
     "- Hệ thống hoặc chặn kèm thông báo rõ ràng, hoặc lưu đủ và hiển thị xuống dòng\n"
     "- Bản in không bị vỡ khung, không đè lên dòng khác"),
]

SEC_IX = [
    (1, "Hai kế toán cùng lập phiếu thu cho một phiếu đề nghị", "P0",
     "Phiếu đề nghị DN-11 đang Chờ KT duyệt; KT-1 và KT-2 đều có quyền Kế toán thanh toán",
     "1. Mở form Tạo phiếu thu cho DN-11 trên hai trình duyệt khác nhau bằng KT-1 và KT-2\n"
     "2. Nhập đủ thông tin ở cả hai\n"
     "3. Bấm Lưu ở trình duyệt 1, sau đó bấm Lưu ở trình duyệt 2",
     "—",
     "- Trình duyệt 1 lưu thành công\n"
     "- Trình duyệt 2 bị chặn, báo Đề nghị thu tiền đã lập phiếu thu tiền\n"
     "- Chỉ có ĐÚNG MỘT phiếu thu tồn tại cho DN-11"),

    (2, "Hai thủ quỹ cùng duyệt một phiếu", "P0",
     "Phiếu PT-W ở trạng thái Chờ duyệt; TQ-1 và TQ-2 đều có quyền duyệt",
     "1. Mở chi tiết PT-W trên hai trình duyệt bằng TQ-1 và TQ-2\n"
     "2. Bấm Duyệt phiếu thu ở trình duyệt 1\n"
     "3. Bấm Duyệt phiếu thu ở trình duyệt 2\n"
     "4. Mở sổ kế toán, đếm bút toán của PT-W",
     "—",
     "- Trình duyệt 1 duyệt thành công\n"
     "- Trình duyệt 2 báo Phiếu thu tiền đã được duyệt\n"
     "- Bút toán KHÔNG bị ghi hai lần"),

    (3, "Một người duyệt, một người hủy cùng lúc", "P0",
     "Phiếu PT-X ở trạng thái Chờ duyệt",
     "1. Mở PT-X trên hai trình duyệt bằng TQ-1 và TQ-2\n"
     "2. TQ-1 bấm Duyệt phiếu thu\n"
     "3. TQ-2 nhập Ghi chú rồi bấm Hủy phiếu thu\n"
     "4. Mở lại chi tiết PT-X và phiếu đề nghị gốc",
     "—",
     "- Ghi nhận đúng trạng thái cuối cùng của cả phiếu thu và phiếu đề nghị\n"
     "- ⚠️ Nếu phiếu thành Hủy mà bút toán vẫn còn trong sổ thì ghi Failed kèm mã phiếu"),

    (4, "Sửa phiếu trong khi thủ quỹ đang duyệt", "P1",
     "Phiếu PT-Y ở trạng thái Chờ duyệt",
     "1. KT-1 dán đường dẫn sửa PT-Y, để form mở\n"
     "2. TQ-1 duyệt PT-Y ở trình duyệt khác\n"
     "3. KT-1 bấm Lưu trên form đang mở\n"
     "4. Mở lại chi tiết PT-Y",
     "—",
     "- Ghi nhận đúng trạng thái và số tiền cuối cùng\n"
     "- ⚠️ Nếu thao tác Lưu ghi đè được lên phiếu đã duyệt thì ghi Failed"),

    (5, "Xóa phiếu đề nghị gốc khi phiếu thu còn tồn tại", "P1",
     "Phiếu đề nghị DN-12 đã có phiếu thu PT-Z ở trạng thái Đang tạo",
     "1. Xóa DN-12 từ màn Đề nghị thu tiền\n"
     "2. Mở danh sách Phiếu thu, tìm PT-Z\n"
     "3. Mở chi tiết PT-Z",
     "—",
     "- Ghi nhận đúng hiện tượng: PT-Z còn hay mất khỏi danh sách, mở chi tiết có lỗi không\n"
     "- ⚠️ Bảng danh sách bắt buộc phải có phiếu đề nghị đi kèm, nên phiếu thu mồ côi có thể biến mất "
     "khỏi danh sách. Ghi rõ để dựng phiếu ghi nhận lỗi"),

    (6, "Người khác đã xóa phiếu trong lúc mình đang mở", "P1",
     "Phiếu PT-N ở trạng thái Đang tạo, đang mở màn Sửa trên trình duyệt của KT-1",
     "1. KT-2 xóa PT-N ở trình duyệt khác\n"
     "2. KT-1 bấm Lưu trên form đang mở",
     "—",
     "- Hệ thống báo dữ liệu đã thay đổi hoặc báo lỗi rõ ràng\n"
     "- Không treo trang, không tạo lại phiếu đã xóa"),

    (7, "Phiếu nháp không lọt sang thủ quỹ", "P0",
     "KT-1 vừa Lưu nháp phiếu PT-AA",
     "1. Đăng nhập bằng TQ-1, mở màn Phiếu thu chờ duyệt\n"
     "2. Tìm PT-AA",
     "—",
     "- PT-AA KHÔNG xuất hiện\n"
     "- Thủ quỹ cũng không nhận thông báo nào về phiếu này"),

    (8, "Cô lập dữ liệu giữa hai công ty ở màn chờ duyệt", "P0",
     "TQ-1 thuộc công ty 3; công ty 1 có 18 phiếu thu đang Chờ duyệt",
     "1. Đăng nhập bằng TQ-1, mở màn Phiếu thu chờ duyệt\n"
     "2. Soát toàn bộ các trang\n"
     "3. Lấy mã một phiếu Chờ duyệt của công ty 1, dán đường dẫn chi tiết",
     "—",
     "- Danh sách không có phiếu nào của công ty 1\n"
     "- Mở chi tiết phiếu của công ty 1: ghi nhận đúng kết quả quan sát được, nếu mở được thì đối "
     "chiếu tiếp là có thấy nút Duyệt hay không"),

    (9, "Cột Số tiền tính lại đúng sau mỗi lần lưu", "P1",
     "Phiếu PT-N có 2 dòng, tổng duyệt thu 12.000.000",
     "1. Mở màn Sửa, đổi duyệt thu dòng 1 từ 5.000.000 xuống 1.000.000, bấm Lưu\n"
     "2. Đọc cột Số tiền của PT-N trên danh sách\n"
     "3. Mở lại màn Sửa, đổi ngược lên 5.000.000, lưu lại\n"
     "4. Đọc lại cột Số tiền",
     "—",
     "- Bước 2 hiện 8.000.000\n"
     "- Bước 4 hiện lại 12.000.000\n"
     "- Không bị cộng dồn chồng lên nhau qua các lần lưu"),
]

SEC_X = [
    (1, "Luồng đầy đủ: đề nghị thu đến hạch toán", "P0",
     "NV-B là nhân viên kinh doanh, KT-1 có quyền Kế toán thanh toán, TQ-1 có quyền Thủ quỹ duyệt phiếu "
     "thu; khách hàng KH-01 đang còn nợ 20.000.000 trên hợp đồng HD-01",
     "1. NV-B lập phiếu đề nghị thu 20.000.000 cho KH-01 theo HD-01, bấm Lưu và gửi duyệt\n"
     "2. KT-1 nhận thông báo, mở phiếu đề nghị, bấm Tạo phiếu thu, nhập Người nộp, bấm Lưu và gửi duyệt\n"
     "3. TQ-1 nhận thông báo, mở phiếu thu, để thực nhận 20.000.000, nhập Ghi chú, bấm Duyệt phiếu thu\n"
     "4. Mở sổ kế toán và báo cáo công nợ của KH-01",
     "—",
     "- Sau bước 1: phiếu đề nghị ở Chờ KT duyệt\n"
     "- Sau bước 2: phiếu thu ở Chờ duyệt, phiếu đề nghị chuyển sang Đã tạo phiếu thu\n"
     "- Sau bước 3: phiếu thu ở Đã duyệt, phiếu đề nghị chuyển sang Đã hạch toán\n"
     "- Sổ kế toán có bút toán ghi Nợ tài khoản tiền và ghi Có tài khoản phải thu, cùng 20.000.000\n"
     "- Công nợ của KH-01 trên HD-01 giảm về 0"),

    (2, "Luồng thu một phần", "P0",
     "Khách hàng KH-02 còn nợ 30.000.000; đã có phiếu đề nghị thu 30.000.000 đang Chờ KT duyệt",
     "1. KT-1 tạo phiếu thu, để duyệt thu 30.000.000, gửi duyệt\n"
     "2. TQ-1 sửa Số tiền thực nhận xuống 12.000.000, nhập Ghi chú, bấm Duyệt phiếu thu\n"
     "3. Đọc cột Số tiền của phiếu trên danh sách\n"
     "4. Mở phiếu đề nghị gốc, đọc cột số tiền đã thu thực tế\n"
     "5. Mở báo cáo công nợ của KH-02",
     "Thực nhận: 12.000.000",
     "- Cột Số tiền ngoài danh sách hiện 12.000.000, không phải 30.000.000\n"
     "- Phiếu đề nghị gốc ghi nhận số thực nhận 12.000.000\n"
     "- Công nợ KH-02 giảm đúng 12.000.000, còn nợ 18.000.000"),

    (3, "Luồng thu ngoại tệ", "P0",
     "Phiếu đề nghị ngoại tệ, tỷ giá 25.000, đề nghị thu 2.000 ngoại tệ",
     "1. KT-1 tạo phiếu thu, giữ nguyên duyệt thu 2.000, gửi duyệt\n"
     "2. TQ-1 giữ nguyên tỷ giá 25.000 và thực nhận 2.000, bấm Duyệt phiếu thu\n"
     "3. Đọc cột Số tiền trên danh sách\n"
     "4. Mở sổ kế toán, đọc số tiền và tỷ giá của bút toán",
     "—",
     "- Cột Số tiền hiện 50.000.000\n"
     "- Bút toán ghi cả số ngoại tệ 2.000 và số quy đổi 50.000.000, kèm tỷ giá 25.000"),

    (4, "Luồng thu theo hợp đồng nguyên tắc", "P0",
     "Phiếu đề nghị gắn hợp đồng nguyên tắc HD-NT với 3 phiếu yêu cầu xuất hàng, tổng đề nghị 8.000.000",
     "1. KT-1 tạo phiếu thu, gửi duyệt\n"
     "2. TQ-1 để thực nhận 8.000.000, bấm nút phân bổ trong bảng con, bấm Duyệt phiếu thu\n"
     "3. Mở sổ kế toán, đếm số bút toán ghi Có\n"
     "4. Mở từng phiếu yêu cầu xuất hàng, đọc số tiền đã thu",
     "—",
     "- Sinh 3 bút toán ghi Có, mỗi phiếu yêu cầu xuất hàng một bút toán\n"
     "- Tổng 3 bút toán bằng đúng 8.000.000\n"
     "- Số đã thu của từng phiếu xuất tăng đúng phần được phân bổ"),

    (5, "Luồng hủy phiếu thu", "P0",
     "Phiếu đề nghị DN-13 đang Chờ KT duyệt",
     "1. KT-1 tạo phiếu thu từ DN-13, gửi duyệt\n"
     "2. TQ-1 nhập Ghi chú rồi bấm Hủy phiếu thu\n"
     "3. Mở lại DN-13, đọc trạng thái và soát nút\n"
     "4. Mở sổ kế toán và báo cáo công nợ",
     "Ghi chú: Khách không thanh toán",
     "- Phiếu thu ở trạng thái Hủy, phiếu đề nghị chuyển sang trạng thái Hủy\n"
     "- Không có bút toán nào được ghi\n"
     "- Công nợ khách hàng KHÔNG thay đổi\n"
     "- ⚠️ DN-13 không quay lại được Chờ KT duyệt nên không lập lại phiếu thu được, ghi nhận là hạn chế "
     "nghiệp vụ"),

    (6, "Luồng thu nhà cung cấp", "P1",
     "Phiếu đề nghị loại Thu nhà cung cấp cho nhà cung cấp NCC-01, hợp đồng mua HDM-01, đề nghị "
     "15.000.000",
     "1. KT-1 tạo phiếu thu, đọc cột Số tài khoản có mặc định\n"
     "2. Gửi duyệt, TQ-1 duyệt với thực nhận 15.000.000\n"
     "3. Mở sổ kế toán, đọc tài khoản của bút toán ghi Có\n"
     "4. Mở báo cáo công nợ nhà cung cấp",
     "—",
     "- Tài khoản có mặc định là tài khoản phải trả nhà cung cấp\n"
     "- Bút toán ghi Có đúng tài khoản đó, gắn đúng NCC-01 và HDM-01\n"
     "- Công nợ phải trả NCC-01 giảm 15.000.000"),

    (7, "Đối chiếu tổng số phiếu sau khi chạy hết bộ test", "P1",
     "Đã chạy xong các mục trên, biết số phiếu đã tạo và đã xóa trong quá trình test",
     "1. Mở chế độ Tất cả bằng tài khoản có quyền xem tổng công ty\n"
     "2. Bấm làm mới bộ lọc, đọc số tổng\n"
     "3. Đối chiếu với số ghi nhận đầu buổi cộng số phiếu mới trừ số phiếu đã xóa",
     "—",
     "- Hai con số khớp chính xác\n"
     "- ⚠️ KHÔNG dùng bộ lọc theo khoảng ngày để đối chiếu vì hai ô ngày không có tác dụng (mục 4)"),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", SEC_III),
    ("IV", "TẠO MỚI / SỬA / XEM CHI TIẾT", SEC_IV),
    ("V", "DUYỆT & HỦY PHIẾU THU", SEC_V),
    ("VI", "XÓA", SEC_VI),
    ("VII", "IN & XUẤT EXCEL", SEC_VII),
    ("VIII", "RÀNG BUỘC NHẬP LIỆU", SEC_VIII),
    ("IX", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", SEC_IX),
    ("X", "LUỒNG NGHIỆP VỤ ĐẦU - CUỐI", SEC_X),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Phiếu thu tiền (ERP) - Cập nhật ngày 20/08/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )
