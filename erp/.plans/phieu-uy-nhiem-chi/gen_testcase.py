# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Phieu uy nhiem chi" (admin/income-expenditure/bill_payment_authorizations).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

⚠️ Tai lieu nay viet theo LOGIC ERP dang chay tren nhanh gop_db (repo D:/laragon/www/erp),
KHONG phai ban da port sang HRM.

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :6646-6656
  app/Http/Controllers/IncomeExpenditure/BillPaymentAuthorizationController.php
  app/Model/IncomeExpenditure/BillPaymentAuthorization.php (+ BillPaymentAuthorizationDetail)
  app/Http/Requests/IncomeExpenditure/BillPaymentAuthorizations/BillPaymentAuthorizationStoreRequest.php
  app/Http/Requests/IncomeExpenditure/BillPaymentAuthorizations/BillPaymentAuthorizationUpdateRequest.php
  app/Model/IncomeExpenditure/BillPaymentRequest.php (nguon phieu de nghi thanh toan)
  app/Http/Controllers/IncomeExpenditure/BillPaymentRequestController.php :447-475 (getData)
  app/Model/Accounting/AccountDetail.php
  database/seeds/PermissionsTableSeeder.php :273, 313, 345-346
  resources/views/income_expenditure/bill_payment_authorizations/*.blade.php
  resources/views/income_expenditure/bill_payment_requests/show.blade.php :20-31
  resources/views/partials/classes/IncomeExpenditure/BillPayment*.blade.php
  resources/views/partials/classes/base/Datatable.blade.php :30-40, 187-194
  resources/views/layouts/topmenubar.blade.php :1007

Chay:  python .plans/phieu-uy-nhiem-chi/gen_testcase.py
"""
import os
import sys

try:  # console Windows mac dinh cp1252
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

# .plans/phieu-uy-nhiem-chi -> .plans -> erp -> hrm-claude-config -> hrm/.claude/skills/...
sys.path.insert(0, os.path.join(
    HERE, "..", "..", "..", "hrm", ".claude", "skills", "testcase-documenter", "assets"))

from tc_engine import build  # noqa: E402

OUT = os.path.join(HERE, "testcase-phieu-uy-nhiem-chi.xlsx")

MODULE = "Phiếu ủy nhiệm chi"

# ============================================================ 9 MUC MO TA
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Quản lý Phiếu ủy nhiệm chi: chứng từ do Kế toán thanh toán lập để chi tiền bằng hình thức "
     "CHUYỂN KHOẢN, thuộc nhóm Công nợ - Thu - Chi (mục menu Thanh toán tiền mặt).\n"
     "Phiếu ủy nhiệm chi là bản chuyển khoản song song với Phiếu chi tiền mặt: cùng bắt nguồn từ một "
     "Phiếu đề nghị thanh toán đã duyệt xong các cấp và đang ở trạng thái Chờ tạo phiếu chi, nhưng chỉ "
     "phiếu đề nghị có Hình thức thanh toán là CK mới ra nút Tạo phiếu ủy nhiệm chi.\n"
     "Riêng loại chi \"Chi thu nhập cho nhân viên\" lập ĐỘC LẬP, không cần phiếu đề nghị: người lập "
     "chọn phòng ban rồi bấm Lấy nhân viên để hệ thống nạp danh sách nhân viên kèm số dư từng khoản.\n"
     "Kế toán thanh toán làm được: xem danh sách, lọc, tạo phiếu (Lưu nháp hoặc Lưu và duyệt), sửa "
     "phiếu nháp, xóa phiếu nháp, xem chi tiết.\n"
     "⚠️ Màn hình KHÔNG có bước gửi duyệt: chỉ có hai nút Lưu và Lưu và duyệt. Bấm Lưu và duyệt là "
     "phiếu ghi sổ kế toán ngay, do chính người lập bấm. Xem mục 3 và mục 9 ghi chú 1.\n"
     "Màn hình có 4 chế độ danh sách khác nhau dùng chung một bảng dữ liệu — xem mục 5."),

    ("2. Đối tượng được tính / hiển thị",
     "Phiếu ủy nhiệm chi có đủ 4 trạng thái: Đang tạo · Chờ duyệt · Đã hạch toán · Hủy. Nhãn Đã hạch "
     "toán tô XANH, ba nhãn còn lại tô ĐỎ.\n"
     "⚠️ Trên thực tế chỉ gặp 3 trạng thái Đang tạo, Đã hạch toán, Hủy. Trạng thái Chờ duyệt không "
     "sinh ra được từ giao diện — xem mục 3.\n"
     "Phạm vi phiếu nhìn thấy phụ thuộc chế độ danh sách đang mở:\n"
     "- Chế độ \"Phiếu của tôi\" (vào thẳng đường dẫn không kèm tham số): chỉ phiếu do chính mình lập, "
     "gồm cả phiếu nháp của mình.\n"
     "- Chế độ \"Tất cả\" (mục menu Phiếu ủy nhiệm chi trỏ vào đây): lấy theo 2 quyền xem ở mục 7, và "
     "luôn ẩn phiếu nháp của người khác.\n"
     "- Chế độ \"Phiếu chờ duyệt\": phiếu đang ở trạng thái Chờ duyệt. Đường dẫn được chặn bằng quyền "
     "Thủ quỹ duyệt phiếu chi, nhưng bên trong KHÔNG áp thêm bất kỳ giới hạn phạm vi nào — xem mục 9 "
     "ghi chú 3.\n"
     "- Chế độ \"Phiếu đã duyệt\": phiếu mà chính người đăng nhập là người đã bấm duyệt, KHÔNG lọc "
     "theo trạng thái nên phiếu đã bị hủy vẫn nằm trong danh sách này.\n"
     "⚠️ Hai chế độ chờ duyệt và đã duyệt KHÔNG có mục menu nào trỏ tới.\n"
     "Bảng danh sách có 9 cột: STT · Mã phiếu · Mã phiếu đề nghị chi · Loại chi · Người đề nghị · Ngày "
     "lập · Người lập · Trạng thái · Hành động.\n"
     "Bảy loại chi lập được phiếu ủy nhiệm chi: Chi trả nhà cung cấp · Chi trả lại khách hàng · Chi "
     "thưởng NVKD · Chi thu nhập cho nhân viên · Chi thưởng thực hiện hợp đồng · Chi khác · Thanh toán "
     "chi phí vận chuyển NCC."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu nháp (Đang tạo) của NGƯỜI KHÁC bị ẩn ở chế độ \"Tất cả\".\n"
     "- Nút \"Sửa\" và nút \"Xóa\" chỉ hiện khi phiếu ở trạng thái Đang tạo. Phiếu Đã hạch toán và "
     "phiếu Hủy có menu Hành động RỖNG — bấm vào chỉ ra một khung trắng.\n"
     "- ⚠️ Màn hình KHÔNG có chức năng In và KHÔNG có chức năng Xuất Excel (khác hẳn màn Phiếu thu và "
     "màn Phiếu chi vốn có đủ hai mục này trong menu Hành động).\n"
     "- ⚠️ Hai nút \"Duyệt phiếu ủy nhiệm chi\" và \"Hủy phiếu ủy nhiệm chi\" trong màn chi tiết chỉ "
     "hiện khi phiếu ở trạng thái Chờ duyệt VÀ người đăng nhập có quyền Thủ quỹ duyệt phiếu chi. Vì "
     "màn Tạo và màn Sửa chỉ đẩy phiếu sang Đang tạo hoặc Đã hạch toán, trạng thái Chờ duyệt không bao "
     "giờ xuất hiện nên trong luồng nghiệp vụ thật HAI NÚT NÀY KHÔNG BAO GIỜ HIỆN và màn Phiếu chờ "
     "duyệt LUÔN RỖNG.\n"
     "- Nút \"Tạo phiếu ủy nhiệm chi\" ở màn Phiếu đề nghị thanh toán chỉ hiện khi hội đủ 3 điều kiện: "
     "người đăng nhập có quyền Kế toán thanh toán, phiếu đề nghị đang ở trạng thái Chờ tạo phiếu chi, "
     "và Hình thức thanh toán của phiếu đề nghị là CK. Phiếu đề nghị TM ra nút Tạo phiếu chi.\n"
     "- Cửa sổ chọn Số phiếu đề nghị CHỈ liệt kê phiếu đề nghị thanh toán đang ở trạng thái Chờ tạo "
     "phiếu chi VÀ có Hình thức thanh toán là CK.\n"
     "- Ba ô lọc Công ty / Phòng ban / Bộ phận chỉ hiện ở chế độ \"Tất cả\" và chỉ với người có quyền "
     "xem theo cấp tương ứng.\n"
     "- Ô lọc \"Loại chi\" cố tình BỎ mục Chi thu nhập cho nhân viên; loại này vẫn hiển thị ở cột Loại "
     "chi nhưng không lọc riêng ra được.\n"
     "- Người dùng KHÔNG thêm được dòng chi tiết và KHÔNG xóa được dòng chi tiết trên phiếu; số dòng "
     "luôn đúng bằng số dòng của phiếu đề nghị gốc (hoặc số nhân viên đã tick với loại chi thu nhập "
     "nhân viên).\n"
     "- Màn hình KHÔNG có chức năng Nhập Excel."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "⚠️ KHÔNG ÁP DỤNG. Khối tìm kiếm vẫn hiển thị hai ô \"Từ ngày\" và \"Đến ngày\", nhưng hệ thống "
     "KHÔNG dùng đến hai giá trị này khi lấy dữ liệu: chọn ngày nào cũng ra nguyên kết quả cũ, kể cả "
     "khoảng ngày không có phiếu nào.\n"
     "Đây là bẫy đối chiếu số liệu nặng nhất của khối tìm kiếm, đã dựng ca test riêng ở mục II. Muốn "
     "giới hạn theo thời gian thì phải lọc bằng Mã phiếu (mã có nhúng tháng - năm lập, xem mục 5).\n"
     "Không có bộ lọc theo Ngày hạch toán, cũng không có bộ lọc theo ngày cập nhật."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Ba cấp: Phiếu đề nghị thanh toán → Phiếu ủy nhiệm chi → Dòng chi tiết.\n"
     "- ⚠️ Hệ thống KHÔNG chặn một phiếu đề nghị lập nhiều phiếu ủy nhiệm chi (khác màn Phiếu thu vốn "
     "chặn chặt). Chừng nào phiếu ủy nhiệm chi đầu còn ở trạng thái Đang tạo thì phiếu đề nghị vẫn giữ "
     "trạng thái Chờ tạo phiếu chi và nút Tạo phiếu ủy nhiệm chi vẫn còn.\n"
     "- Phiếu ủy nhiệm chi giữ: Mã phiếu, Số phiếu đề nghị, Tài khoản có, Tài khoản nợ, Ngày hạch "
     "toán, Loại chi, Phương thức thanh toán, Ngân hàng chuyển, Số tài khoản chuyển khoản, Tỷ giá, "
     "Người nhận tiền, Ghi chú, Trạng thái, Người tạo, Người duyệt, Công ty, Phòng ban, Bộ phận.\n"
     "- Loại chi, Hình thức thanh toán, Loại tiền, Lý do chi, Người đề nghị, Phòng ban lấy từ phiếu đề "
     "nghị và bị KHÓA, không sửa trên phiếu ủy nhiệm chi.\n"
     "- Mỗi dòng chi tiết giữ: Số đơn hàng - Hợp đồng (hoặc Phiếu hạch toán chuyến với loại Thanh toán "
     "chi phí vận chuyển NCC) · Số tiền đề nghị chi · Số tiền duyệt chi · Ghi chú. Hai cột tiền đều có "
     "cột quy đổi VND đi kèm khi phiếu là ngoại tệ.\n"
     "- Riêng loại chi \"Chi thưởng thực hiện hợp đồng\": ô Tài khoản nợ ở khối chung BỊ ẨN, thay bằng "
     "hai cột \"Số tài khoản nợ\" và \"Tên tài khoản nợ\" nhập theo TỪNG DÒNG.\n"
     "- Dòng gắn hợp đồng nguyên tắc (loại Chi trả lại khách hàng và Chi thưởng NVKD) có thêm bảng con "
     "hiển thị theo từng Phiếu yêu cầu xuất hàng: Số phiếu · Công nợ còn lại · Số tiền.\n"
     "- Loại chi \"Chi thu nhập cho nhân viên\" không có phiếu đề nghị, dòng chi tiết là từng nhân "
     "viên với 5 khoản: chênh lệch, hoa hồng tháng, hoa hồng quý, thưởng quý, tiền vận chuyển; có hai "
     "thẻ Chi tiết và Chi tiết vụ việc.\n"
     "- Mã phiếu sinh tự động: mã công ty + \".UNC\" + tháng năm (4 số) + \".\" + 5 chữ số tăng dần, "
     "ví dụ TPE.UNC0826.00017. Không sửa tay được.\n"
     "- Công ty / Phòng ban / Bộ phận của phiếu ủy nhiệm chi lấy từ hồ sơ nhân sự của người LẬP PHIẾU "
     "tại thời điểm tạo, và không đổi về sau.\n"
     "- Bốn chế độ danh sách dùng CHUNG một nguồn dữ liệu và chung bộ lọc; khác nhau ở phạm vi lọc và "
     "ở bộ nút phía trên bảng.\n"
     "- Mỗi lần lưu, toàn bộ dòng chi tiết cũ (kể cả bảng con theo phiếu yêu cầu xuất hàng) bị xóa và "
     "ghi lại từ đầu."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Bảng danh sách KHÔNG có cột số tiền: muốn biết giá trị phiếu phải mở chi tiết. Đây là khác "
     "biệt so với màn Phiếu thu.\n"
     "- Trong form: cột quy đổi VND của mỗi dòng = số tiền của dòng đó × Tỷ giá đang hiển thị trên "
     "phiếu. Đổi Tỷ giá thì mọi cột quy đổi đổi theo ngay.\n"
     "- Ô \"Số tiền duyệt chi\" của mỗi dòng bị chặn trần bằng \"Số tiền đề nghị chi\" của chính dòng "
     "đó: nhập lớn hơn thì ô tự kéo về bằng trần, nhập số âm thì tự về 0, KHÔNG có thông báo nào.\n"
     "- Khi ghi sổ, dòng có Số tiền duyệt chi bằng 0 bị BỎ QUA, không sinh bút toán cho dòng đó.\n"
     "- ⚠️ Số tiền của vế ghi CÓ (tài khoản chuyển tiền đi) KHÔNG cộng dồn các dòng: hệ thống chỉ lấy "
     "số của DÒNG CUỐI CÙNG có số tiền lớn hơn 0. Phiếu từ 2 dòng trở lên là hai vế Nợ và Có lệch "
     "nhau. Xem mục 9 ghi chú 5 — đây là lỗi số liệu nặng nhất của màn.\n"
     "- ⚠️ Dòng gắn hợp đồng nguyên tắc có nhiều Phiếu yêu cầu xuất hàng: mỗi phiếu xuất sinh một bút "
     "toán mang NGUYÊN số tiền duyệt chi của cả dòng, không chia theo từng phiếu. Ba phiếu xuất là số "
     "tiền ghi sổ gấp ba.\n"
     "- Với loại chi thu nhập nhân viên: mỗi khoản dương ghi vế Nợ, mỗi khoản âm ghi vế Có; hai bút "
     "toán đối ứng cộng riêng tổng các khoản dương và tổng các khoản âm.\n"
     "- Chỉ những nhân viên được TICK ở cột đầu bảng mới được lưu; nhân viên bỏ tick bị loại hoàn "
     "toàn khỏi phiếu.\n"
     "- Một phiếu khớp nhiều điều kiện lọc vẫn chỉ hiện một dòng."),

    ("7. Phân quyền cấp",
     "Bốn quyền liên quan tới màn hình này:\n"
     "1. \"Kế toán thanh toán\" — được vào đường dẫn Tạo mới, đường dẫn Sửa, và được lưu phiếu mới. "
     "Đây cũng là quyền quyết định nút Tạo phiếu ủy nhiệm chi có hiện ở màn Phiếu đề nghị thanh toán "
     "hay không.\n"
     "2. \"Thủ quỹ duyệt phiếu chi\" — được vào màn Phiếu chờ duyệt, và thấy hai nút Duyệt phiếu ủy "
     "nhiệm chi / Hủy phiếu ủy nhiệm chi trong màn chi tiết.\n"
     "3. \"Xem tất cả phiếu ủy nhiệm chi của tổng công ty\" — thấy phiếu của mọi công ty ở chế độ Tất "
     "cả; bộ lọc hiện thêm ô Công ty và ô Phòng ban.\n"
     "4. \"Xem tất cả phiếu ủy nhiệm chi của công ty\" — chỉ phiếu công ty mình ở chế độ Tất cả; bộ "
     "lọc hiện ô Phòng ban.\n"
     "⚠️ Màn này KHÔNG có quyền xem cấp phòng ban và cấp bộ phận. Ai không có một trong hai quyền xem "
     "trên thì ở chế độ Tất cả chỉ thấy phiếu mà PHIẾU ĐỀ NGHỊ do chính mình lập — không phải phiếu do "
     "chính mình lập. Xem mục 9 ghi chú 8.\n"
     "Tài khoản có vai trò Super Admin luôn mở được chi tiết mọi phiếu.\n"
     "⚠️ Quyền Thủ quỹ duyệt phiếu chi trên thực tế KHÔNG tham gia luồng ủy nhiệm chi, vì trạng thái "
     "Chờ duyệt không sinh ra được (mục 3). Kế toán thanh toán vừa lập vừa duyệt phiếu của chính mình.\n"
     "⚠️ Các chức năng còn lại — xem danh sách, xem chi tiết, cập nhật, xóa — KHÔNG gắn quyền ở phía "
     "hệ thống, chỉ ẩn / hiện nút trên giao diện. Đây là hiện trạng của mã nguồn; nhóm test bỏ qua giao "
     "diện (mục IX và các ca phân quyền cuối) dựng riêng để đo mức độ rủi ro này."),

    ("8. Cách tính các ô thống kê",
     "- Ô \"Hiển thị a đến b trong tổng số N\" dưới bảng: a là dòng đầu trang đang xem, b là dòng "
     "cuối, N là tổng số phiếu khớp bộ lọc trong phạm vi chế độ đang mở.\n"
     "- Ô \"Số dòng mỗi trang\": mặc định 10; đổi số dòng thì bảng quay về trang 1.\n"
     "- Cột STT đánh liên tục theo trang: trang 2 với 10 dòng mỗi trang bắt đầu từ 11.\n"
     "- Cột \"Ngày lập\" hiển thị dạng ngày/tháng/năm, không có giờ.\n"
     "- Cột \"Loại chi\" ưu tiên lấy loại của PHIẾU ĐỀ NGHỊ gốc; phiếu không gắn đề nghị (chi thu nhập "
     "nhân viên) thì lấy loại ghi trên chính phiếu ủy nhiệm chi.\n"
     "- Cột \"Người đề nghị\" là người lập phiếu đề nghị; cột \"Người lập\" là người lập phiếu ủy "
     "nhiệm chi. Phiếu không gắn đề nghị thì cột Người đề nghị để trống.\n"
     "- Trong form, dòng \"Tổng cộng\" cuối bảng chi tiết cộng dồn từng cặp cột: đề nghị chi và duyệt "
     "chi, mỗi cặp gồm cột nguyên tệ và cột quy đổi VND.\n"
     "- Ngày hạch toán do người lập chọn, mặc định là ngày hiện tại, và bị chặn KHÔNG cho chọn ngày "
     "trong quá khứ.\n"
     "- Tỷ giá hiển thị làm tròn 2 chữ số thập phân; số tiền nguyên tệ làm tròn 2 chữ số thập phân; "
     "số tiền quy đổi VND làm tròn về số nguyên."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất của màn này — đọc trước khi chạy test:\n"
     "1. ⚠️ Màn hình KHÔNG có bước gửi duyệt. Chỉ có Lưu (thành phiếu nháp) và Lưu và duyệt (ghi sổ "
     "ngay). Hệ quả dây chuyền: trạng thái Chờ duyệt không bao giờ xuất hiện, hai nút Duyệt / Hủy "
     "trong màn chi tiết không bao giờ hiện, màn Phiếu chờ duyệt luôn rỗng, và quyền Thủ quỹ duyệt "
     "phiếu chi vô tác dụng trên luồng này.\n"
     "2. ⚠️ Hai ô lọc \"Từ ngày\" / \"Đến ngày\" KHÔNG có tác dụng (mục 4). Chọn khoảng ngày không có "
     "phiếu nào vẫn ra nguyên danh sách cũ. Ghi nhận Failed.\n"
     "3. ⚠️ Màn Phiếu chờ duyệt KHÔNG áp bất kỳ giới hạn phạm vi nào: chỉ lọc theo trạng thái. Nếu "
     "trong dữ liệu có phiếu ở trạng thái Chờ duyệt thì mọi người vào được màn này đều thấy phiếu của "
     "MỌI công ty, mọi người lập.\n"
     "4. ⚠️ Ba ô lọc Công ty / Phòng ban / Bộ phận lọc theo đơn vị của PHIẾU ĐỀ NGHỊ THANH TOÁN gốc, "
     "KHÔNG phải đơn vị của người lập phiếu ủy nhiệm chi.\n"
     "5. ⚠️ LỖI SỐ LIỆU NẶNG NHẤT: với phiếu từ 2 dòng chi tiết trở lên, số tiền ghi bên vế CÓ chỉ "
     "bằng số tiền của DÒNG CUỐI CÙNG, không phải tổng các dòng. Phiếu 3 dòng 5 triệu - 3 triệu - 2 "
     "triệu thì vế Nợ ghi đủ 10 triệu còn vế Có chỉ ghi 2 triệu. Bắt buộc đối chiếu sổ sau mỗi lần "
     "duyệt phiếu nhiều dòng.\n"
     "6. ⚠️ Dòng gắn hợp đồng nguyên tắc có N phiếu yêu cầu xuất hàng sẽ ghi sổ N lần NGUYÊN số tiền "
     "duyệt chi của dòng, thay vì chia số tiền cho từng phiếu xuất.\n"
     "7. ⚠️ Loại chi \"Thanh toán chi phí vận chuyển NCC\": duyệt ngay ở màn Tạo thì có ghi sổ, nhưng "
     "lưu nháp rồi mở Sửa để duyệt thì phiếu vẫn chuyển sang Đã hạch toán và phiếu đề nghị vẫn chuyển "
     "sang Duyệt phiếu chi mà KHÔNG có bút toán nào được ghi. Đây là hai kết quả khác nhau cho cùng "
     "một nghiệp vụ.\n"
     "8. ⚠️ Ở chế độ Tất cả, người KHÔNG có quyền xem theo cấp bị lọc theo người lập PHIẾU ĐỀ NGHỊ. "
     "Kế toán thanh toán tự lập phiếu ủy nhiệm chi cho đề nghị của người khác sẽ KHÔNG thấy phiếu do "
     "chính mình lập trong danh sách này (phải mở chế độ Phiếu của tôi).\n"
     "9. ⚠️ Phiếu loại \"Chi thu nhập cho nhân viên\" không gắn phiếu đề nghị nên ở chế độ Tất cả chỉ "
     "người có quyền xem của tổng công ty mới thấy; người có quyền xem của công ty cũng không thấy.\n"
     "10. ⚠️ Sửa phiếu chỉ ẩn NÚT theo trạng thái. Người có quyền Kế toán thanh toán dán thẳng đường "
     "dẫn sửa của phiếu Đã hạch toán vẫn mở được form, và bấm Lưu và duyệt là hệ thống ghi sổ THÊM một "
     "bộ bút toán nữa cho cùng phiếu đó.\n"
     "11. ⚠️ Xóa phiếu: hệ thống KHÔNG kiểm tra quyền và KHÔNG kiểm tra trạng thái. Dán thẳng đường "
     "dẫn xóa của một phiếu bất kỳ, kể cả phiếu Đã hạch toán, là phiếu bị xóa trong khi bút toán đã "
     "ghi vẫn còn nguyên; các dòng chi tiết của phiếu cũng không được dọn theo.\n"
     "12. ⚠️ Xóa phiếu ủy nhiệm chi KHÔNG trả phiếu đề nghị về trạng thái Chờ tạo phiếu chi. Nếu phiếu "
     "đã duyệt thì phiếu đề nghị kẹt ở Duyệt phiếu chi, mất nút Tạo phiếu ủy nhiệm chi, không lập lại "
     "được từ giao diện.\n"
     "13. ⚠️ Với phiếu ngoại tệ, ô Tỷ giá bị đặt về 0 ngay khi nạp dữ liệu từ phiếu đề nghị, làm toàn "
     "bộ cột quy đổi VND về 0 cho tới khi người lập nhập tay tỷ giá. Phiếu tiền Việt Nam thì lại kế "
     "thừa đúng tỷ giá của phiếu đề nghị.\n"
     "14. ⚠️ Người lập sửa Tỷ giá trên phiếu thì số tiền quy đổi ghi sổ đổi theo, NHƯNG ô tỷ giá lưu "
     "kèm bút toán vẫn là tỷ giá của phiếu đề nghị. Bút toán tự mâu thuẫn: số tiền tính theo một tỷ "
     "giá, tỷ giá ghi kèm lại là số khác.\n"
     "15. ⚠️ Bỏ chọn ô \"Ngân hàng chuyển\" (chọn lại dòng trống) làm màn hình đứng: các ô sau đó "
     "không phản hồi nữa, phải tải lại trang. Đừng nhầm là mạng chậm.\n"
     "16. ⚠️ Ô \"Số tiền duyệt chi\" bắt buộc lớn hơn 0 với ba loại Chi trả nhà cung cấp, Chi trả lại "
     "khách hàng, Chi thưởng NVKD. Để một dòng bằng 0 là KHÔNG lưu được CẢ phiếu, không riêng dòng đó.\n"
     "17. ⚠️ Phiếu nháp để qua ngày sẽ không lưu lại được: Ngày hạch toán giữ ngày cũ mà hệ thống chặn "
     "ngày quá khứ. Phải tự sửa Ngày hạch toán về hôm nay rồi mới lưu được, và thông báo lỗi hiện bằng "
     "TIẾNG ANH chứ không phải tiếng Việt như các ô khác.\n"
     "18. ⚠️ Với loại chi thu nhập nhân viên, cảnh báo lệch số tiền theo mã vụ việc CHỈ chạy ở màn chi "
     "tiết — mà màn đó không bấm duyệt được. Duyệt từ màn Tạo hoặc màn Sửa thì phiếu lệch vẫn ghi sổ "
     "bình thường.\n"
     "19. ⚠️ Khoản \"thưởng quý\" mang giá trị ÂM bị ghi nhầm sang vế Nợ, trong khi bốn khoản còn lại "
     "âm thì ghi đúng vế Có.\n"
     "20. ⚠️ Danh sách \"Số tài khoản chuyển khoản\" ở màn Tạo chỉ lấy tài khoản đang hoạt động, còn "
     "màn Sửa và màn chi tiết lấy cả tài khoản đã ngừng hoạt động.\n"
     "21. ⚠️ Nhãn ô người đề nghị ở màn Tạo bị lặp chữ, hiển thị \"Người người đề nghị\"; màn chi tiết "
     "hiển thị đúng \"Người đề nghị\".\n"
     "22. ⚠️ Luồng ủy nhiệm chi KHÔNG gửi thông báo cho ai, trong khi màn Phiếu chi tiền mặt tương ứng "
     "vẫn gửi thông báo cho nhóm thủ quỹ. Đừng chờ chuông báo.\n"
     "23. Bộ lọc được hệ thống ghi nhớ RIÊNG cho từng chế độ danh sách; rời màn rồi quay lại vẫn còn "
     "điều kiện lọc cũ — test xong nhớ bấm nút làm mới bộ lọc trước khi sang ca test khác."),
]

# ============================================================ TC PHAN QUYEN
ROLE_TCS = [
    ("00", "Tài khoản không có quyền xem nào chỉ thấy phiếu của phiếu đề nghị do mình lập", "P0",
     "Tài khoản NV-A không có quyền \"Xem tất cả phiếu ủy nhiệm chi của tổng công ty\" và không có "
     "quyền \"Xem tất cả phiếu ủy nhiệm chi của công ty\"; NV-A đã lập 8 phiếu đề nghị thanh toán "
     "chuyển khoản, cả 8 đã được kế toán lập phiếu ủy nhiệm chi; công ty của NV-A có hơn 120 phiếu ủy "
     "nhiệm chi của nhiều người",
     "1. Đăng nhập bằng NV-A\n"
     "2. Mở menu Công nợ - Thu - Chi, nhóm Thanh toán tiền mặt, bấm mục Phiếu ủy nhiệm chi\n"
     "3. Đọc số tổng dưới bảng\n"
     "4. Lật hết các trang, soát cột Người đề nghị và cột Người lập",
     "Tài khoản: NV-A (không quyền xem theo cấp)",
     "- Vào được màn hình, không bị chặn\n"
     "- Tổng hiện đúng 8\n"
     "- ⚠️ Mọi dòng đều có Người ĐỀ NGHỊ là NV-A, còn cột Người LẬP là kế toán thanh toán — hệ thống "
     "lọc theo người lập phiếu đề nghị chứ không theo người lập phiếu ủy nhiệm chi (mục 9 ghi chú 8)\n"
     "- Khối lọc KHÔNG có ô Công ty, KHÔNG có ô Phòng ban"),

    ("01", "Kế toán thanh toán không thấy phiếu do chính mình lập ở chế độ Tất cả", "P0",
     "Tài khoản KT-B có quyền \"Kế toán thanh toán\" nhưng KHÔNG có hai quyền xem theo cấp; KT-B vừa "
     "lập 5 phiếu ủy nhiệm chi từ 5 phiếu đề nghị do NV-A lập; KT-B chưa từng lập phiếu đề nghị nào",
     "1. Đăng nhập bằng KT-B\n"
     "2. Mở mục Phiếu ủy nhiệm chi trên menu (chế độ Tất cả)\n"
     "3. Đọc số tổng, tìm 5 phiếu vừa lập\n"
     "4. Xóa phần tham số phía sau đường dẫn để về chế độ Phiếu của tôi, đọc lại số tổng",
     "Tài khoản: KT-B (có quyền Kế toán thanh toán, không có quyền xem theo cấp)",
     "- ⚠️ Chế độ Tất cả: tổng bằng 0, KHÔNG thấy phiếu nào trong 5 phiếu vừa lập\n"
     "- Chế độ Phiếu của tôi: thấy đủ 5 phiếu\n"
     "- Ghi nhận Failed — người lập phiếu phải thấy được phiếu của mình ở danh sách chính (mục 9 ghi "
     "chú 8)"),

    ("02", "Quyền xem của tổng công ty thấy phiếu của mọi công ty", "P0",
     "Tài khoản C chỉ có quyền \"Xem tất cả phiếu ủy nhiệm chi của tổng công ty\"; hệ thống có phiếu "
     "ủy nhiệm chi của ít nhất 3 công ty",
     "1. Đăng nhập bằng C, mở mục Phiếu ủy nhiệm chi trên menu\n"
     "2. Bấm nút Bộ lọc để bung khối tìm kiếm\n"
     "3. Ghi lại các ô lọc theo đơn vị đang hiện\n"
     "4. Chọn lần lượt từng Công ty rồi bấm nút tìm kiếm",
     "Quyền: Xem tất cả phiếu ủy nhiệm chi của tổng công ty",
     "- Khối lọc hiện CẢ ô Công ty và ô Phòng ban\n"
     "- Bỏ chọn công ty thì thấy phiếu của cả 3 công ty\n"
     "- ⚠️ Chọn công ty nào ra phiếu mà PHIẾU ĐỀ NGHỊ gốc thuộc công ty đó, không phải phiếu do người "
     "công ty đó lập (mục 9 ghi chú 4)"),

    ("03", "Quyền xem của công ty chỉ thấy phiếu công ty mình", "P0",
     "Tài khoản D chỉ có quyền \"Xem tất cả phiếu ủy nhiệm chi của công ty\", thuộc công ty 3; công ty "
     "3 có 35 phiếu ủy nhiệm chi, công ty 1 có 210 phiếu",
     "1. Đăng nhập bằng D, mở mục Phiếu ủy nhiệm chi\n"
     "2. Bấm nút Bộ lọc, ghi lại các ô lọc theo đơn vị\n"
     "3. Đọc số tổng, soát danh sách qua tất cả các trang",
     "Quyền: Xem tất cả phiếu ủy nhiệm chi của công ty",
     "- Khối lọc KHÔNG có ô Công ty, chỉ có ô Phòng ban\n"
     "- Tổng bằng 35 trừ đi số phiếu nháp của người khác trong công ty 3\n"
     "- Không có phiếu nào của công ty 1"),

    ("04", "Quyền xem của công ty vẫn không thấy phiếu chi thu nhập nhân viên", "P0",
     "Tài khoản D (quyền \"Xem tất cả phiếu ủy nhiệm chi của công ty\", công ty 3); trong công ty 3 có "
     "4 phiếu loại Chi thu nhập cho nhân viên do kế toán khác lập, đều ở trạng thái Đã hạch toán",
     "1. Đăng nhập bằng D, mở mục Phiếu ủy nhiệm chi\n"
     "2. Soát cột Loại chi trên tất cả các trang, tìm mục Chi thu nhập cho nhân viên\n"
     "3. Đăng nhập lại bằng tài khoản có quyền xem của tổng công ty, lặp lại bước 2",
     "Quyền: Xem tất cả phiếu ủy nhiệm chi của công ty",
     "- ⚠️ Tài khoản D KHÔNG thấy phiếu nào loại Chi thu nhập cho nhân viên\n"
     "- Tài khoản quyền tổng công ty thấy đủ 4 phiếu\n"
     "- Ghi nhận Failed — phiếu không gắn phiếu đề nghị bị loại khỏi mọi phạm vi trừ tổng công ty "
     "(mục 9 ghi chú 9)"),

    ("05", "Màn Phiếu ủy nhiệm chi không có quyền xem cấp phòng ban và cấp bộ phận", "P1",
     "Tài khoản E có quyền \"Xem tất cả phiếu đề nghị thanh toán của phòng ban\" (quyền của màn Đề "
     "nghị thanh toán) nhưng KHÔNG có hai quyền xem của màn Phiếu ủy nhiệm chi",
     "1. Đăng nhập bằng E, mở mục Đề nghị thanh toán, ghi lại số tổng\n"
     "2. Mở mục Phiếu ủy nhiệm chi, đọc số tổng và soát cột Người đề nghị",
     "Quyền: chỉ có quyền xem cấp phòng ban của màn Đề nghị thanh toán",
     "- Màn Đề nghị thanh toán: thấy phiếu của các phòng ban E quản lý\n"
     "- Màn Phiếu ủy nhiệm chi: CHỈ thấy phiếu gắn với đề nghị do chính E lập\n"
     "- ⚠️ Đúng hiện trạng — màn này không có quyền cấp phòng ban / bộ phận (mục 7)"),

    ("06", "Không có quyền Kế toán thanh toán thì không vào được màn Tạo mới", "P0",
     "Tài khoản NV-A không có quyền \"Kế toán thanh toán\"; có sẵn 1 phiếu đề nghị thanh toán chuyển "
     "khoản đang ở trạng thái Chờ tạo phiếu chi",
     "1. Đăng nhập bằng NV-A, mở chi tiết phiếu đề nghị đó, soát dãy nút cuối trang\n"
     "2. Mở mục Phiếu ủy nhiệm chi, soát nút phía trên bảng\n"
     "3. Nhờ kế toán gửi đường dẫn màn Tạo mới, dán thẳng vào thanh địa chỉ",
     "Tài khoản: NV-A (không có quyền Kế toán thanh toán)",
     "- Màn chi tiết phiếu đề nghị KHÔNG có nút Tạo phiếu ủy nhiệm chi\n"
     "- ⚠️ Nút Tạo mới phía trên bảng danh sách VẪN hiện (giao diện không ẩn theo quyền)\n"
     "- Bấm nút Tạo mới hoặc dán đường dẫn: hệ thống từ chối, báo không có quyền"),

    ("07", "Không có quyền Kế toán thanh toán thì không vào được màn Sửa", "P0",
     "Tài khoản NV-A không có quyền \"Kế toán thanh toán\"; có sẵn 1 phiếu ủy nhiệm chi ở trạng thái "
     "Đang tạo",
     "1. Đăng nhập bằng NV-A, mở mục Phiếu ủy nhiệm chi\n"
     "2. Dán thẳng đường dẫn màn Sửa của phiếu nháp đó vào thanh địa chỉ",
     "Tài khoản: NV-A (không có quyền Kế toán thanh toán)",
     "- Hệ thống từ chối, báo không có quyền, không mở được form sửa"),

    ("08", "Không có quyền Thủ quỹ duyệt phiếu chi thì không vào được màn Phiếu chờ duyệt", "P0",
     "Tài khoản KT-B có quyền \"Kế toán thanh toán\" nhưng KHÔNG có quyền \"Thủ quỹ duyệt phiếu chi\"",
     "1. Đăng nhập bằng KT-B\n"
     "2. Dán thẳng đường dẫn màn Phiếu ủy nhiệm chi chờ duyệt vào thanh địa chỉ",
     "Tài khoản: KT-B (không có quyền Thủ quỹ duyệt phiếu chi)",
     "- Hệ thống từ chối, báo không có quyền"),

    ("09", "Quyền Thủ quỹ duyệt phiếu chi vào được màn chờ duyệt nhưng danh sách rỗng", "P0",
     "Tài khoản TQ-F có quyền \"Thủ quỹ duyệt phiếu chi\"; trong hệ thống đã có hơn 100 phiếu ủy nhiệm "
     "chi ở các trạng thái Đang tạo, Đã hạch toán, Hủy — không có phiếu nào ở trạng thái Chờ duyệt",
     "1. Đăng nhập bằng TQ-F\n"
     "2. Dán đường dẫn màn Phiếu ủy nhiệm chi chờ duyệt\n"
     "3. Đọc số tổng dưới bảng",
     "Quyền: Thủ quỹ duyệt phiếu chi",
     "- Vào được màn hình\n"
     "- ⚠️ Danh sách RỖNG, tổng bằng 0 — vì luồng không có bước gửi duyệt nên không phiếu nào tới được "
     "trạng thái Chờ duyệt (mục 9 ghi chú 1)"),

    ("10", "Người duyệt luôn mở được chi tiết phiếu mình đã duyệt", "P1",
     "Tài khoản KT-B đã bấm Lưu và duyệt 3 phiếu; KT-B KHÔNG có hai quyền xem theo cấp",
     "1. Đăng nhập bằng KT-B\n"
     "2. Dán đường dẫn màn Phiếu ủy nhiệm chi đã duyệt\n"
     "3. Mở chi tiết từng phiếu trong danh sách",
     "Tài khoản: KT-B",
     "- Màn Phiếu đã duyệt hiện đủ 3 phiếu\n"
     "- Mở được chi tiết cả 3 phiếu, không ra trang báo không tìm thấy"),

    ("11", "Không mở được chi tiết phiếu nháp của người khác", "P0",
     "Kế toán KT-B lập 1 phiếu và để ở trạng thái Đang tạo; tài khoản G có quyền \"Xem tất cả phiếu ủy "
     "nhiệm chi của tổng công ty\"",
     "1. Đăng nhập bằng G\n"
     "2. Xin mã phiếu nháp của KT-B, dán đường dẫn màn chi tiết phiếu đó",
     "Tài khoản: G (quyền xem tổng công ty)",
     "- Hệ thống hiện trang báo không tìm thấy dữ liệu, KHÔNG hiện nội dung phiếu\n"
     "- Trang không bị treo, vẫn quay lại được menu"),

    ("12", "Tài khoản bất kỳ gọi thẳng chức năng Cập nhật, bỏ qua giao diện", "P0",
     "Tài khoản NV-A không có quyền \"Kế toán thanh toán\" và không có quyền \"Thủ quỹ duyệt phiếu "
     "chi\"; có sẵn 1 phiếu ủy nhiệm chi ở trạng thái Đang tạo, tổng số tiền 20.000.000",
     "1. Đăng nhập bằng NV-A trên trình duyệt\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Cập nhật của phiếu đó, gửi kèm trạng thái Đã "
     "hạch toán\n"
     "3. Đăng nhập lại bằng kế toán, mở danh sách và sổ kế toán kiểm tra",
     "Tài khoản: NV-A · Trạng thái gửi lên: Đã hạch toán",
     "- Mong đợi: hệ thống từ chối, báo không có quyền\n"
     "- ⚠️ Hiện trạng cần kiểm chứng: chức năng Cập nhật KHÔNG gắn quyền, phiếu chuyển sang Đã hạch "
     "toán và sổ kế toán được ghi bởi người không có quyền nào. Nếu đúng như vậy, ghi nhận Failed và "
     "báo lỗ hổng"),

    ("13", "Tài khoản bất kỳ gọi thẳng chức năng Xóa, bỏ qua giao diện", "P0",
     "Tài khoản NV-A không có quyền \"Kế toán thanh toán\"; có sẵn 1 phiếu ủy nhiệm chi ở trạng thái "
     "Đã hạch toán, đã ghi sổ 20.000.000",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dán thẳng đường dẫn Xóa của phiếu đó vào thanh địa chỉ\n"
     "3. Mở lại danh sách và sổ kế toán kiểm tra",
     "Tài khoản: NV-A",
     "- Mong đợi: hệ thống từ chối, báo không có quyền\n"
     "- ⚠️ Hiện trạng cần kiểm chứng: phiếu bị xóa khỏi danh sách trong khi bút toán 20.000.000 vẫn "
     "còn nguyên trong sổ. Nếu đúng như vậy, ghi nhận Failed và báo lỗ hổng (mục 9 ghi chú 11)"),
]

# ============================================================ SECTION I
SEC_I = [
    (1, "Vào màn Phiếu ủy nhiệm chi từ menu", "P0",
     "Tài khoản KT-B có quyền Kế toán thanh toán; công ty có ít nhất 20 phiếu ủy nhiệm chi",
     "1. Đăng nhập bằng KT-B\n"
     "2. Mở menu Công nợ - Thu - Chi\n"
     "3. Vào nhóm Thanh toán tiền mặt, bấm mục Phiếu ủy nhiệm chi\n"
     "4. Đọc tiêu đề trang và các cột của bảng",
     "—",
     "- Trang mở ra với tiêu đề \"Danh sách phiếu ủy nhiệm chi tiền\"\n"
     "- Bảng hiện đúng 9 cột: STT, Mã phiếu, Mã phiếu đề nghị chi, Loại chi, Người đề nghị, Ngày lập, "
     "Người lập, Trạng thái, Hành động\n"
     "- Màn mở ở chế độ Tất cả (mục menu trỏ vào chế độ này)\n"
     "- Có nút Tạo mới phía trên bảng"),

    (2, "Chế độ Phiếu của tôi", "P0",
     "Tài khoản KT-B đã lập 6 phiếu ủy nhiệm chi, trong đó 2 phiếu còn ở trạng thái Đang tạo; công ty "
     "có hơn 100 phiếu của nhiều người",
     "1. Đăng nhập bằng KT-B, mở mục Phiếu ủy nhiệm chi trên menu\n"
     "2. Xóa phần tham số phía sau đường dẫn rồi tải lại trang\n"
     "3. Đọc số tổng, soát cột Người lập và cột Trạng thái",
     "—",
     "- Tổng đúng bằng 6\n"
     "- Mọi dòng đều có Người lập là KT-B\n"
     "- Thấy được cả 2 phiếu nháp của chính mình\n"
     "- Có nút Tạo mới phía trên bảng"),

    (3, "Chế độ Phiếu đã duyệt", "P1",
     "Tài khoản KT-B đã bấm Lưu và duyệt 4 phiếu; trong đó 1 phiếu sau đó bị chuyển sang trạng thái "
     "Hủy bằng dữ liệu",
     "1. Đăng nhập bằng KT-B\n"
     "2. Dán đường dẫn màn Phiếu ủy nhiệm chi đã duyệt\n"
     "3. Đọc số tổng, soát cột Trạng thái",
     "—",
     "- Tổng bằng 4\n"
     "- ⚠️ Phiếu ở trạng thái Hủy VẪN nằm trong danh sách \"đã duyệt\" — màn này chỉ lọc theo người "
     "duyệt, không lọc theo trạng thái. Ghi nhận Failed\n"
     "- KHÔNG có nút Tạo mới ở màn này"),

    (4, "Hai chế độ chờ duyệt và đã duyệt không có mục menu", "P1",
     "Tài khoản TQ-F có quyền Thủ quỹ duyệt phiếu chi",
     "1. Đăng nhập bằng TQ-F\n"
     "2. Mở toàn bộ menu Công nợ - Thu - Chi, soát từng nhóm mục\n"
     "3. Ghi lại các mục có chữ ủy nhiệm chi",
     "—",
     "- ⚠️ Chỉ có DUY NHẤT một mục \"Phiếu ủy nhiệm chi\" trong nhóm Thanh toán tiền mặt\n"
     "- Không có mục nào trỏ tới màn chờ duyệt hay màn đã duyệt — chỉ vào được bằng đường dẫn trực "
     "tiếp"),

    (5, "Mã phiếu là liên kết mở chi tiết", "P0",
     "Có ít nhất 1 phiếu ủy nhiệm chi ở trạng thái Đã hạch toán",
     "1. Mở mục Phiếu ủy nhiệm chi\n"
     "2. Bấm vào Mã phiếu ở một dòng bất kỳ",
     "—",
     "- Mở màn chi tiết đúng phiếu vừa bấm, NGAY TẠI TAB đang mở\n"
     "- Tiêu đề trang là \"Chi tiết phiếu ủy nhiệm chi tiền\"\n"
     "- Mã phiếu trên form khớp với mã vừa bấm"),

    (6, "Mã phiếu đề nghị chi là liên kết mở phiếu đề nghị", "P1",
     "Có 1 phiếu ủy nhiệm chi gắn phiếu đề nghị và 1 phiếu loại Chi thu nhập cho nhân viên",
     "1. Mở mục Phiếu ủy nhiệm chi\n"
     "2. Bấm vào Mã phiếu đề nghị chi của phiếu gắn đề nghị\n"
     "3. Quay lại, soát ô Mã phiếu đề nghị chi của phiếu chi thu nhập nhân viên",
     "—",
     "- Phiếu gắn đề nghị: mở màn Chi tiết phiếu đề nghị thanh toán đúng phiếu gốc\n"
     "- Phiếu chi thu nhập nhân viên: ô Mã phiếu đề nghị chi để TRỐNG, không có liên kết, không lỗi"),

    (7, "Cột Loại chi lấy theo phiếu đề nghị", "P1",
     "Có 1 phiếu gắn đề nghị loại Chi trả nhà cung cấp và 1 phiếu loại Chi thu nhập cho nhân viên",
     "1. Mở mục Phiếu ủy nhiệm chi\n"
     "2. Đọc cột Loại chi của cả hai phiếu",
     "—",
     "- Phiếu gắn đề nghị hiện \"Chi trả nhà cung cấp\"\n"
     "- Phiếu không gắn đề nghị hiện \"Chi thu nhập cho nhân viên\"\n"
     "- Cả hai đều là chữ tiếng Việt đầy đủ, không phải số"),

    (8, "Cột Người đề nghị và Người lập là hai người khác nhau", "P1",
     "Phiếu đề nghị do NV-A lập, phiếu ủy nhiệm chi do KT-B lập",
     "1. Mở mục Phiếu ủy nhiệm chi, tìm phiếu đó\n"
     "2. Đọc cột Người đề nghị và cột Người lập",
     "—",
     "- Người đề nghị: NV-A\n"
     "- Người lập: KT-B\n"
     "- Ngày lập hiển thị dạng ngày/tháng/năm, không có giờ"),

    (9, "Menu Hành động theo trạng thái", "P0",
     "Chuẩn bị 3 phiếu: một Đang tạo, một Đã hạch toán, một Hủy",
     "1. Mở mục Phiếu ủy nhiệm chi\n"
     "2. Bấm biểu tượng bánh răng ở cột Hành động của từng phiếu\n"
     "3. Ghi lại các mục hiện ra",
     "—",
     "- Phiếu Đang tạo: có 2 mục Sửa và Xóa\n"
     "- Phiếu Đã hạch toán và phiếu Hủy: khung menu RỖNG, không có mục nào\n"
     "- ⚠️ Không có mục In, không có mục Xuất Excel ở bất kỳ trạng thái nào (mục 3)"),

    (10, "Mở chi tiết bằng mã phiếu không tồn tại", "P2",
     "Không có phiếu ủy nhiệm chi nào mang số thứ tự 999999",
     "1. Đăng nhập bằng KT-B\n"
     "2. Dán đường dẫn màn chi tiết với số thứ tự 999999",
     "—",
     "- Hệ thống báo dữ liệu không tồn tại, không treo trang, không hiện form trắng\n"
     "- Bấm nút quay lại của trình duyệt vẫn về được danh sách"),

    (11, "Nhãn ô người đề nghị ở màn Tạo bị lặp chữ", "P2",
     "Tài khoản KT-B, có 1 phiếu đề nghị thanh toán chuyển khoản ở trạng thái Chờ tạo phiếu chi",
     "1. Mở chi tiết phiếu đề nghị, bấm Tạo phiếu ủy nhiệm chi\n"
     "2. Đọc nhãn của ô hiển thị tên người lập phiếu đề nghị\n"
     "3. Lưu phiếu rồi mở màn chi tiết, đọc lại nhãn ô đó",
     "—",
     "- ⚠️ Màn Tạo hiển thị nhãn \"Người người đề nghị\" (lặp chữ Người)\n"
     "- Màn chi tiết hiển thị đúng \"Người đề nghị\"\n"
     "- Ghi nhận Failed về mặt hiển thị"),
]

# ============================================================ SECTION II
SEC_II = [
    (1, "Lọc theo Mã phiếu", "P0",
     "Công ty có ít nhất 30 phiếu; biết trước một mã phiếu đầy đủ, ví dụ TPE.UNC0826.00017",
     "1. Mở mục Phiếu ủy nhiệm chi, bấm nút Bộ lọc\n"
     "2. Nhập chuỗi UNC0826 vào ô Mã phiếu, bấm nút tìm kiếm\n"
     "3. Nhập tiếp chuỗi 00017, bấm tìm kiếm\n"
     "4. Nhập chuỗi ZZZZZ, bấm tìm kiếm",
     "Mã phiếu: UNC0826 · 00017 · ZZZZZ",
     "- Bước 2: ra toàn bộ phiếu lập trong tháng 8 năm 2026 của công ty đó\n"
     "- Bước 3: ra đúng 1 phiếu có đuôi 00017\n"
     "- Bước 4: bảng trống, hiện dòng không có dữ liệu, tổng bằng 0\n"
     "- Ô lọc chấp nhận nhập một phần mã, không cần gõ đủ"),

    (2, "Lọc theo Mã phiếu đề nghị chi", "P0",
     "Có ít nhất 3 phiếu ủy nhiệm chi gắn với 3 phiếu đề nghị khác nhau; biết một phần mã của một "
     "phiếu đề nghị",
     "1. Bấm nút Bộ lọc\n"
     "2. Nhập một phần mã phiếu đề nghị vào ô Mã phiếu đề nghị chi, bấm tìm kiếm\n"
     "3. Soát cột Mã phiếu đề nghị chi của kết quả",
     "Mã phiếu đề nghị chi: DNTT0826",
     "- Chỉ ra các phiếu ủy nhiệm chi gắn với phiếu đề nghị khớp chuỗi vừa nhập\n"
     "- Phiếu loại Chi thu nhập cho nhân viên (không gắn đề nghị) KHÔNG xuất hiện"),

    (3, "Danh sách của ô lọc Loại chi thiếu mục chi thu nhập nhân viên", "P0",
     "Trong hệ thống có phiếu thuộc cả 7 loại chi",
     "1. Bấm nút Bộ lọc\n"
     "2. Bung ô lọc Loại chi, ghi lại đầy đủ các mục trong danh sách\n"
     "3. So với các giá trị đang hiển thị ở cột Loại chi của bảng",
     "—",
     "- Danh sách lọc có 6 mục: Chi trả nhà cung cấp, Chi trả lại khách hàng, Chi thưởng NVKD, Chi "
     "thưởng thực hiện hợp đồng, Chi khác, Thanh toán chi phí vận chuyển NCC\n"
     "- ⚠️ THIẾU mục \"Chi thu nhập cho nhân viên\" dù cột Loại chi vẫn hiển thị giá trị này — không "
     "có cách nào lọc riêng loại đó. Ghi nhận Failed"),

    (4, "Lọc theo từng Loại chi", "P0",
     "Mỗi loại chi có ít nhất 2 phiếu",
     "1. Bấm nút Bộ lọc\n"
     "2. Chọn lần lượt từng mục trong ô Loại chi, mỗi lần bấm tìm kiếm\n"
     "3. Soát cột Loại chi của kết quả",
     "Loại chi: lần lượt 6 mục trong danh sách",
     "- Mỗi lần chỉ ra phiếu đúng loại đã chọn\n"
     "- Số tổng khớp với số phiếu của loại đó\n"
     "- Bỏ chọn thì ra lại toàn bộ danh sách"),

    (5, "Lọc theo Người lập", "P0",
     "KT-B lập 6 phiếu, kế toán KT-C lập 4 phiếu; tài khoản đang đăng nhập có quyền xem của tổng công ty",
     "1. Bấm nút Bộ lọc\n"
     "2. Gõ tên KT-B vào ô Người lập, chọn từ danh sách gợi ý, bấm tìm kiếm\n"
     "3. Đổi sang KT-C, bấm tìm kiếm",
     "Người lập: KT-B · KT-C",
     "- Chọn KT-B: tổng bằng 6, mọi dòng có Người lập là KT-B\n"
     "- Chọn KT-C: tổng bằng 4\n"
     "- Ô lọc là ô tìm kiếm gõ tên, không phải danh sách xổ sẵn toàn bộ nhân viên"),

    (6, "Lọc theo Người đề nghị", "P0",
     "NV-A lập 8 phiếu đề nghị đã có phiếu ủy nhiệm chi; NV-H lập 3 phiếu đề nghị đã có phiếu",
     "1. Bấm nút Bộ lọc\n"
     "2. Gõ tên NV-A vào ô Người đề nghị, chọn từ gợi ý, bấm tìm kiếm\n"
     "3. Soát cột Người đề nghị và cột Người lập của kết quả",
     "Người đề nghị: NV-A",
     "- Tổng bằng 8\n"
     "- Cột Người đề nghị đều là NV-A, cột Người lập là các kế toán khác nhau\n"
     "- Phiếu loại Chi thu nhập cho nhân viên không xuất hiện vì không có người đề nghị"),

    (7, "Lọc theo Trạng thái", "P0",
     "Có phiếu ở cả 3 trạng thái Đang tạo, Đã hạch toán, Hủy",
     "1. Bấm nút Bộ lọc\n"
     "2. Chọn lần lượt từng trạng thái trong ô Trạng thái, mỗi lần bấm tìm kiếm\n"
     "3. Ghi lại màu nhãn trạng thái của kết quả",
     "Trạng thái: Đang tạo · Chờ duyệt · Đã hạch toán · Hủy",
     "- Danh sách có đủ 4 mục trạng thái\n"
     "- Chọn Đã hạch toán: mọi nhãn tô XANH\n"
     "- Chọn Đang tạo và Hủy: nhãn tô ĐỎ\n"
     "- ⚠️ Chọn Chờ duyệt: bảng trống, tổng bằng 0 — trạng thái này không tồn tại trong dữ liệu thật "
     "(mục 9 ghi chú 1)"),

    (8, "Bộ lọc thời gian không có tác dụng", "P0",
     "Công ty có phiếu lập rải rác nhiều tháng; biết chắc trong tháng 1 năm 2020 KHÔNG có phiếu nào",
     "1. Mở mục Phiếu ủy nhiệm chi, ghi lại số tổng đang có\n"
     "2. Bấm nút Bộ lọc, nhập Từ ngày 01/01/2020 và Đến ngày 31/01/2020\n"
     "3. Bấm nút tìm kiếm, đọc lại số tổng\n"
     "4. Đổi khoảng ngày sang một tuần bất kỳ trong tháng hiện tại, bấm tìm kiếm",
     "Từ ngày: 01/01/2020 · Đến ngày: 31/01/2020",
     "- ⚠️ Sau bước 3 số tổng KHÔNG đổi, danh sách giữ nguyên như bước 1 dù khoảng ngày không có phiếu "
     "nào\n"
     "- Bước 4 cũng ra kết quả y hệt\n"
     "- Ghi nhận Failed — hai ô lọc thời gian không được hệ thống dùng đến (mục 4)"),

    (9, "Lọc theo Công ty", "P1",
     "Tài khoản C có quyền xem của tổng công ty; phiếu đề nghị của công ty 3 có 12 phiếu ủy nhiệm chi, "
     "trong đó 4 phiếu do kế toán công ty 1 lập",
     "1. Đăng nhập bằng C, bấm nút Bộ lọc\n"
     "2. Chọn Công ty 3, bấm tìm kiếm\n"
     "3. Soát cột Người lập của kết quả",
     "Công ty: Công ty 3",
     "- Tổng bằng 12\n"
     "- ⚠️ Trong kết quả CÓ 4 phiếu do kế toán công ty 1 lập, vì hệ thống lọc theo công ty của PHIẾU "
     "ĐỀ NGHỊ chứ không theo công ty của người lập phiếu (mục 9 ghi chú 4)"),

    (10, "Lọc kết hợp nhiều điều kiện", "P1",
     "Có ít nhất 2 phiếu thỏa đồng thời: loại Chi trả nhà cung cấp, người lập KT-B, trạng thái Đã hạch "
     "toán",
     "1. Bấm nút Bộ lọc\n"
     "2. Chọn cùng lúc Loại chi là Chi trả nhà cung cấp, Người lập là KT-B, Trạng thái là Đã hạch toán\n"
     "3. Bấm tìm kiếm",
     "Loại chi: Chi trả nhà cung cấp · Người lập: KT-B · Trạng thái: Đã hạch toán",
     "- Kết quả thỏa ĐỒNG THỜI cả 3 điều kiện\n"
     "- Một phiếu khớp nhiều điều kiện vẫn chỉ hiện đúng một dòng, không nhân đôi"),

    (11, "Làm mới bộ lọc", "P1",
     "Đã đặt sẵn 3 điều kiện lọc và đang xem kết quả đã lọc",
     "1. Bấm nút làm mới bộ lọc\n"
     "2. Đọc lại các ô lọc và số tổng\n"
     "3. Rời sang màn khác rồi quay lại mục Phiếu ủy nhiệm chi",
     "—",
     "- Mọi ô lọc trở về trống, danh sách về đầy đủ\n"
     "- ⚠️ Nếu KHÔNG bấm làm mới mà rời màn rồi quay lại, các điều kiện lọc cũ vẫn còn — nhớ làm mới "
     "trước mỗi ca test (mục 9 ghi chú 23)"),

    (12, "Bộ lọc ở màn chờ duyệt và màn đã duyệt", "P2",
     "Tài khoản TQ-F có quyền Thủ quỹ duyệt phiếu chi",
     "1. Mở màn Phiếu ủy nhiệm chi chờ duyệt, bấm nút Bộ lọc, ghi lại các ô lọc\n"
     "2. Mở màn Phiếu ủy nhiệm chi đã duyệt, làm tương tự\n"
     "3. So với bộ lọc ở màn chính",
     "—",
     "- Màn chờ duyệt: có Mã phiếu, Mã phiếu đề nghị chi, Loại chi, Người lập, Người đề nghị — KHÔNG "
     "có ô Trạng thái\n"
     "- ⚠️ Ô Loại chi ở màn chờ duyệt là ô GÕ CHỮ chứ không phải danh sách chọn như màn chính — gõ tên "
     "loại chi không ra kết quả. Ghi nhận Failed"),
]

# ============================================================ SECTION III
SEC_III = [
    (1, "Sắp xếp mặc định theo ngày lập mới nhất", "P1",
     "Công ty có ít nhất 25 phiếu lập ở nhiều ngày khác nhau",
     "1. Mở mục Phiếu ủy nhiệm chi\n"
     "2. Đọc cột Ngày lập từ dòng đầu xuống dòng cuối trang 1\n"
     "3. Sang trang 2, đọc tiếp",
     "—",
     "- Phiếu mới nhất nằm trên cùng, cũ dần xuống dưới\n"
     "- Thứ tự giữ liên tục khi sang trang"),

    (2, "Không có cột nào sắp xếp được", "P1",
     "Đang ở màn danh sách với ít nhất 25 phiếu",
     "1. Bấm lần lượt vào tiêu đề từng cột: Mã phiếu, Loại chi, Ngày lập, Người lập\n"
     "2. Quan sát thứ tự dòng sau mỗi lần bấm",
     "—",
     "- Không cột nào có biểu tượng mũi tên sắp xếp\n"
     "- Thứ tự dòng KHÔNG đổi sau mỗi lần bấm\n"
     "- Đây là hiện trạng thiết kế, không phải lỗi"),

    (3, "Phân trang và số dòng mỗi trang", "P1",
     "Công ty có ít nhất 35 phiếu",
     "1. Mở mục Phiếu ủy nhiệm chi, đọc dòng thông tin dưới bảng\n"
     "2. Sang trang 2, đọc lại dòng thông tin và cột STT\n"
     "3. Đổi Số dòng mỗi trang sang 25\n"
     "4. Đọc lại dòng thông tin",
     "Số dòng mỗi trang: 10 rồi 25",
     "- Mặc định 10 dòng mỗi trang\n"
     "- Trang 2 có STT bắt đầu từ 11\n"
     "- Đổi sang 25 dòng thì bảng quay về trang 1, STT bắt đầu từ 1\n"
     "- Dòng thông tin ghi đúng số bản ghi đang xem trên tổng số khớp bộ lọc"),

    (4, "Số tổng đổi theo bộ lọc", "P1",
     "Công ty có 40 phiếu, trong đó 12 phiếu loại Chi trả nhà cung cấp",
     "1. Mở danh sách, đọc số tổng\n"
     "2. Lọc Loại chi là Chi trả nhà cung cấp, đọc lại số tổng\n"
     "3. Bấm làm mới bộ lọc, đọc lại",
     "Loại chi: Chi trả nhà cung cấp",
     "- Bước 1: tổng bằng 40\n"
     "- Bước 2: tổng bằng 12, số trang tính lại theo 12\n"
     "- Bước 3: tổng về lại 40"),

    (5, "Phiếu nháp của người khác bị ẩn ở chế độ Tất cả", "P0",
     "Kế toán KT-B lập 1 phiếu và để trạng thái Đang tạo; tài khoản G có quyền xem của tổng công ty",
     "1. Đăng nhập bằng G, mở mục Phiếu ủy nhiệm chi\n"
     "2. Lọc Trạng thái là Đang tạo, bấm tìm kiếm\n"
     "3. Soát cột Người lập của kết quả",
     "Trạng thái: Đang tạo",
     "- Chỉ hiện phiếu nháp do chính G lập\n"
     "- KHÔNG thấy phiếu nháp của KT-B\n"
     "- Ở chế độ Phiếu của tôi, KT-B vẫn thấy phiếu nháp của mình"),

    (6, "Bảng danh sách không có cột số tiền", "P1",
     "Có ít nhất 1 phiếu giá trị 250.000.000",
     "1. Mở mục Phiếu ủy nhiệm chi\n"
     "2. Soát toàn bộ tiêu đề cột\n"
     "3. Mở chi tiết phiếu, đọc dòng Tổng cộng của bảng chi tiết",
     "—",
     "- ⚠️ Bảng danh sách KHÔNG có cột số tiền nào — muốn biết giá trị phiếu phải mở chi tiết (khác "
     "màn Phiếu thu vốn có cột Số tiền)\n"
     "- Dòng Tổng cộng trong chi tiết hiện 250.000.000"),

    (7, "Danh sách khi không có dữ liệu", "P2",
     "Tài khoản mới chưa lập phiếu nào và không có quyền xem theo cấp",
     "1. Đăng nhập bằng tài khoản đó\n"
     "2. Mở mục Phiếu ủy nhiệm chi rồi mở tiếp chế độ Phiếu của tôi",
     "—",
     "- Bảng hiện dòng thông báo không có dữ liệu\n"
     "- Tổng bằng 0, không có nút phân trang\n"
     "- Nút Tạo mới vẫn hiện, bấm vào vẫn mở được form (nếu có quyền Kế toán thanh toán)"),
]

# ============================================================ SECTION IV
SEC_IV = [
    (1, "Tạo phiếu từ màn Đề nghị thanh toán", "P0",
     "Tài khoản KT-B có quyền Kế toán thanh toán; phiếu đề nghị DNTT-01 loại Chi trả nhà cung cấp, "
     "Hình thức thanh toán CK, trạng thái Chờ tạo phiếu chi, có 2 dòng chi tiết 6.000.000 và 4.000.000",
     "1. Đăng nhập bằng KT-B, mở chi tiết DNTT-01\n"
     "2. Bấm nút Tạo phiếu ủy nhiệm chi ở cuối trang\n"
     "3. Quan sát toàn bộ form vừa mở",
     "Phiếu đề nghị: DNTT-01",
     "- Mở màn Tạo phiếu ủy nhiệm chi, hiện thông báo xanh \"Thêm thành công!\"\n"
     "- Ô Số phiếu đề nghị điền sẵn mã DNTT-01\n"
     "- Bảng chi tiết đổ đúng 2 dòng với Số tiền đề nghị chi 6.000.000 và 4.000.000\n"
     "- Ngày hạch toán mặc định là ngày hôm nay"),

    (2, "Nút Tạo phiếu ủy nhiệm chi chỉ hiện với phiếu đề nghị chuyển khoản", "P0",
     "Hai phiếu đề nghị cùng ở trạng thái Chờ tạo phiếu chi: DNTT-CK có Hình thức thanh toán CK, "
     "DNTT-TM có Hình thức thanh toán TM; tài khoản KT-B có quyền Kế toán thanh toán",
     "1. Mở chi tiết DNTT-CK, ghi lại tên nút ở cuối trang\n"
     "2. Mở chi tiết DNTT-TM, ghi lại tên nút ở cuối trang",
     "—",
     "- DNTT-CK: hiện nút \"Tạo phiếu ủy nhiệm chi\"\n"
     "- DNTT-TM: hiện nút \"Tạo phiếu chi\" (sang màn Phiếu chi tiền mặt, không phải màn này)"),

    (3, "Nút Tạo phiếu ủy nhiệm chi biến mất khi phiếu đề nghị chưa duyệt xong", "P0",
     "Bốn phiếu đề nghị chuyển khoản ở các trạng thái: Chờ TP duyệt, Chờ kế toán công nợ duyệt, Chờ kế "
     "toán trưởng duyệt, Chờ ban giám đốc duyệt",
     "1. Đăng nhập bằng KT-B\n"
     "2. Mở chi tiết lần lượt 4 phiếu đề nghị\n"
     "3. Soát dãy nút cuối trang của từng phiếu",
     "—",
     "- Cả 4 phiếu đều KHÔNG có nút Tạo phiếu ủy nhiệm chi\n"
     "- Nút chỉ xuất hiện khi phiếu đề nghị đã sang trạng thái Chờ tạo phiếu chi"),

    (4, "Cửa sổ chọn Số phiếu đề nghị", "P0",
     "Trong hệ thống có: 3 phiếu đề nghị chuyển khoản ở trạng thái Chờ tạo phiếu chi, 2 phiếu đề nghị "
     "tiền mặt cùng trạng thái, 5 phiếu đề nghị chuyển khoản ở trạng thái khác",
     "1. Vào thẳng màn Tạo phiếu ủy nhiệm chi từ nút Tạo mới\n"
     "2. Bấm biểu tượng kính lúp bên phải ô Số phiếu đề nghị\n"
     "3. Đọc danh sách trong cửa sổ, đếm số dòng\n"
     "4. Thử lọc bằng ô Mã phiếu đề nghị chi và ô Người lập trong cửa sổ",
     "—",
     "- Cửa sổ tên \"Phiếu đề nghị chi\", có 3 cột: STT, Mã phiếu đề nghị, Người lập\n"
     "- Chỉ liệt kê đúng 3 phiếu chuyển khoản ở trạng thái Chờ tạo phiếu chi\n"
     "- Không có phiếu tiền mặt, không có phiếu ở trạng thái khác\n"
     "- Hai ô lọc trong cửa sổ hoạt động đúng"),

    (5, "Các ô kế thừa từ phiếu đề nghị bị khóa", "P0",
     "Phiếu đề nghị DNTT-01 loại Chi trả nhà cung cấp, tiền Việt Nam, lý do chi \"Thanh toán tiền hàng "
     "tháng 8\", do NV-A phòng Kinh doanh 1 lập",
     "1. Mở màn Tạo, chọn DNTT-01\n"
     "2. Thử bấm đổi từng ô: Loại chi, Hình thức thanh toán, Loại tiền, Lý do chi, Người người đề "
     "nghị, Phòng ban\n"
     "3. Đọc giá trị đang hiển thị của các ô đó",
     "Phiếu đề nghị: DNTT-01",
     "- Cả 6 ô đều MỜ, không bấm đổi được\n"
     "- Loại chi: Chi trả nhà cung cấp · Loại tiền: tiền Việt Nam · Lý do chi: Thanh toán tiền hàng "
     "tháng 8 · Người đề nghị: NV-A · Phòng ban: Kinh doanh 1"),

    (6, "Tài khoản nợ mặc định theo đối tượng của phiếu đề nghị", "P1",
     "Ba phiếu đề nghị chuyển khoản ở trạng thái Chờ tạo phiếu chi: một chi cho khách hàng, một chi "
     "cho nhà cung cấp, một chi phí vận chuyển nhà cung cấp",
     "1. Lần lượt tạo phiếu ủy nhiệm chi từ 3 phiếu đề nghị trên\n"
     "2. Sau mỗi lần chọn phiếu đề nghị, đọc ô Tài khoản nợ đang được chọn sẵn\n"
     "3. Thử đổi sang tài khoản khác",
     "—",
     "- Chi cho khách hàng, chi cho nhà cung cấp, chi phí vận chuyển: mỗi trường hợp Tài khoản nợ được "
     "chọn sẵn một tài khoản tương ứng, không để trống\n"
     "- Cả 3 trường hợp vẫn cho phép đổi tay sang tài khoản khác\n"
     "- Ô Tài khoản có được chọn sẵn tài khoản tiền gửi ngân hàng"),

    (7, "Phiếu đề nghị chi cho nhân viên có hợp đồng để trống tài khoản nợ", "P1",
     "Phiếu đề nghị DNTT-NV loại Chi thưởng thực hiện hợp đồng cho nhân viên, chuyển khoản, trạng thái "
     "Chờ tạo phiếu chi",
     "1. Tạo phiếu ủy nhiệm chi từ DNTT-NV\n"
     "2. Đọc bảng chi tiết, soát cột Số tài khoản nợ của từng dòng\n"
     "3. Bấm Lưu mà không chọn tài khoản nợ",
     "Phiếu đề nghị: DNTT-NV",
     "- ⚠️ Cột Số tài khoản nợ của các dòng để TRỐNG, người lập phải tự chọn\n"
     "- Bấm Lưu khi còn trống: hiện lỗi đỏ Bắt buộc nhập ngay dưới ô của đúng dòng đó, phiếu không "
     "được lưu"),

    (8, "Loại chi thưởng thực hiện hợp đồng nhập tài khoản nợ theo dòng", "P0",
     "Phiếu đề nghị DNTT-06 loại Chi thưởng thực hiện hợp đồng, chuyển khoản, có 3 dòng chi tiết",
     "1. Tạo phiếu ủy nhiệm chi từ DNTT-06\n"
     "2. Soát khối Thông tin chung, tìm ô Tài khoản nợ\n"
     "3. Soát tiêu đề bảng chi tiết\n"
     "4. Đổi Số tài khoản nợ của dòng 1, quan sát cột Tên tài khoản nợ cùng dòng",
     "Phiếu đề nghị: DNTT-06",
     "- ⚠️ Khối Thông tin chung KHÔNG có ô Tài khoản nợ (bị ẩn với loại chi này)\n"
     "- Bảng chi tiết có thêm 2 cột: Số tài khoản nợ (bắt buộc) và Tên tài khoản nợ\n"
     "- Đổi số tài khoản thì cột Tên tài khoản nợ cùng dòng đổi theo ngay"),

    (9, "Số tiền duyệt chi mặc định bằng số tiền đề nghị chi", "P0",
     "Phiếu đề nghị DNTT-01 có 2 dòng: 6.000.000 và 4.000.000",
     "1. Tạo phiếu ủy nhiệm chi từ DNTT-01\n"
     "2. Đọc cột Số tiền duyệt chi của 2 dòng ngay khi form vừa nạp xong\n"
     "3. Đọc dòng Tổng cộng",
     "Phiếu đề nghị: DNTT-01",
     "- Dòng 1: Số tiền duyệt chi bằng 6.000.000; dòng 2 bằng 4.000.000\n"
     "- Dòng Tổng cộng: cột đề nghị chi và cột duyệt chi đều bằng 10.000.000"),

    (10, "Chặn số tiền duyệt chi vượt số tiền đề nghị chi", "P0",
     "Phiếu ủy nhiệm chi đang mở, dòng 1 có Số tiền đề nghị chi 6.000.000",
     "1. Nhập 9.000.000 vào ô Số tiền duyệt chi dòng 1, bấm ra ngoài ô\n"
     "2. Đọc lại giá trị trong ô và dòng Tổng cộng\n"
     "3. Nhập tiếp -2.000.000, bấm ra ngoài ô",
     "Số tiền duyệt chi: 9.000.000 rồi -2.000.000",
     "- ⚠️ Ô tự kéo về 6.000.000, KHÔNG có thông báo nào — đừng nhầm là hệ thống nhận sai số\n"
     "- Nhập số âm thì ô tự về 0\n"
     "- Dòng Tổng cộng cập nhật theo ngay"),

    (11, "Phiếu ngoại tệ hiển thị hai cột tiền", "P0",
     "Phiếu đề nghị DNTT-USD loại tiền đô la Mỹ, chuyển khoản, trạng thái Chờ tạo phiếu chi, tỷ giá "
     "trên phiếu đề nghị là 25.000",
     "1. Tạo phiếu ủy nhiệm chi từ DNTT-USD\n"
     "2. Soát tiêu đề bảng chi tiết\n"
     "3. Đọc ô Tỷ giá và các cột quy đổi VND",
     "Phiếu đề nghị: DNTT-USD",
     "- Nhóm Số tiền đề nghị chi và nhóm Số tiền duyệt chi mỗi nhóm tách thành 2 cột: cột đô la Mỹ và "
     "cột VND\n"
     "- ⚠️ Ô Tỷ giá bị đặt về 0, toàn bộ cột VND hiển thị 0 dù phiếu đề nghị có tỷ giá 25.000 — phải "
     "nhập tay tỷ giá mới ra số (mục 9 ghi chú 13)"),

    (12, "Nhập tỷ giá cho phiếu ngoại tệ", "P0",
     "Đang mở phiếu ủy nhiệm chi từ DNTT-USD, dòng 1 có Số tiền duyệt chi 1.000 đô la Mỹ",
     "1. Nhập 25.000 vào ô Tỷ giá\n"
     "2. Đọc cột VND của dòng 1 và dòng Tổng cộng\n"
     "3. Đổi Tỷ giá thành 26.000, đọc lại",
     "Tỷ giá: 25.000 rồi 26.000",
     "- Cột VND dòng 1 hiện 25.000.000, đổi thành 26.000.000 sau bước 3\n"
     "- Dòng Tổng cộng cập nhật theo ngay\n"
     "- Số quy đổi làm tròn về số nguyên, có dấu phân cách nghìn"),

    (13, "Ô Tỷ giá bị khóa với phiếu tiền Việt Nam", "P1",
     "Phiếu đề nghị DNTT-01 loại tiền Việt Nam",
     "1. Tạo phiếu ủy nhiệm chi từ DNTT-01\n"
     "2. Bấm vào ô Tỷ giá, thử gõ số\n"
     "3. Đọc giá trị đang hiển thị",
     "Phiếu đề nghị: DNTT-01",
     "- Ô Tỷ giá MỜ, không gõ được\n"
     "- Giá trị hiển thị đúng tỷ giá của phiếu đề nghị"),

    (14, "Phương thức thanh toán lọc danh sách số tài khoản chuyển", "P0",
     "Công ty có 3 tài khoản mở tại ngân hàng X và 5 tài khoản ở các ngân hàng khác, tất cả đang hoạt "
     "động",
     "1. Đang ở màn Tạo, chọn Ngân hàng chuyển là ngân hàng X\n"
     "2. Chọn Phương thức thanh toán là Tiền tự có, bung ô Số tài khoản chuyển khoản, đếm số dòng\n"
     "3. Đổi Phương thức thanh toán sang Tiền vay, bung lại ô đó",
     "Ngân hàng chuyển: X · Phương thức: Tiền tự có rồi Tiền vay",
     "- Tiền tự có: danh sách chỉ còn 3 tài khoản của ngân hàng X\n"
     "- Tiền vay: danh sách hiện lại đủ 8 tài khoản\n"
     "- Nếu ngân hàng chỉ có đúng 1 tài khoản thì hệ thống tự chọn sẵn tài khoản đó"),

    (15, "Bỏ chọn Ngân hàng chuyển làm màn hình đứng", "P0",
     "Đang ở màn Tạo, đã chọn xong Ngân hàng chuyển và Số tài khoản chuyển khoản",
     "1. Bung ô Ngân hàng chuyển, chọn lại dòng trống \"Chọn ngân hàng chuyển\"\n"
     "2. Thử gõ vào ô Số tiền duyệt chi của dòng 1\n"
     "3. Thử bấm nút Lưu",
     "Ngân hàng chuyển: bỏ chọn",
     "- Mong đợi: hệ thống xóa trắng Số tài khoản chuyển khoản và cho thao tác tiếp bình thường\n"
     "- ⚠️ Hiện trạng cần kiểm chứng: màn hình ĐỨNG, số vừa gõ không hiện, nút Lưu không phản hồi, "
     "phải tải lại trang. Nếu đúng như vậy, ghi nhận Failed (mục 9 ghi chú 15)"),

    (16, "Chọn số tài khoản chuyển tự điền thông tin tài khoản", "P1",
     "Công ty có tài khoản số 0011 0000 1234 tên \"CTY TAN PHAT\" tại ngân hàng X",
     "1. Chọn Ngân hàng chuyển là X, chọn Số tài khoản chuyển khoản là 0011 0000 1234\n"
     "2. Điền nốt các ô bắt buộc, bấm Lưu\n"
     "3. Mở màn chi tiết phiếu vừa lưu, đọc khối thông tin tài khoản chuyển",
     "Số tài khoản chuyển khoản: 0011 0000 1234",
     "- Màn chi tiết hiện đúng số tài khoản 0011 0000 1234 và tên tài khoản CTY TAN PHAT\n"
     "- Tên ngân hàng chuyển hiện đúng ngân hàng X"),

    (17, "Thông tin ngân hàng thụ hưởng theo loại đối tượng", "P1",
     "Hai phiếu đề nghị chuyển khoản ở trạng thái Chờ tạo phiếu chi: DNTT-NN chi cho nhà cung cấp nước "
     "ngoài, DNTT-TN chi cho nhà cung cấp trong nước",
     "1. Tạo phiếu ủy nhiệm chi từ DNTT-NN, ghi lại khối thông tin ngân hàng thụ hưởng\n"
     "2. Làm tương tự với DNTT-TN",
     "—",
     "- DNTT-NN: hiện khối chọn Ngân hàng và khối Ngân hàng trung gian, mỗi khối có Số tài khoản, Tài "
     "khoản, Tên ngân hàng, Swift Code, IBAN Number, Địa chỉ; thêm ô Phí\n"
     "- DNTT-TN: chỉ hiện Số tài khoản, Tên tài khoản, Tên ngân hàng, Chi nhánh, Thành phố dạng chỉ "
     "đọc\n"
     "- Thông tin nào chưa có thì hiện dấu gạch dưới thay vì để trống hẳn"),

    (18, "Lưu phiếu ở trạng thái nháp", "P0",
     "Đã điền đủ thông tin hợp lệ trên màn Tạo từ DNTT-01; phiếu đề nghị đang ở trạng thái Chờ tạo "
     "phiếu chi",
     "1. Bấm nút Lưu\n"
     "2. Đọc thông báo và trang được chuyển tới\n"
     "3. Tìm phiếu vừa lưu trong danh sách, đọc cột Trạng thái\n"
     "4. Mở lại chi tiết DNTT-01, đọc trạng thái phiếu đề nghị\n"
     "5. Mở sổ kế toán, tìm bút toán của phiếu vừa lưu",
     "—",
     "- Thông báo xanh \"Thêm phiếu ủy nhiệm chi tiền thành công!\"\n"
     "- Chuyển về danh sách chế độ Tất cả\n"
     "- Phiếu mới ở trạng thái Đang tạo, nhãn đỏ\n"
     "- Phiếu đề nghị VẪN ở trạng thái Chờ tạo phiếu chi\n"
     "- Sổ kế toán CHƯA có bút toán nào của phiếu này"),

    (19, "Lưu và duyệt phiếu", "P0",
     "Đã điền đủ thông tin hợp lệ trên màn Tạo từ DNTT-01 (2 dòng 6.000.000 và 4.000.000)",
     "1. Bấm nút Lưu và duyệt\n"
     "2. Đọc thông báo\n"
     "3. Tìm phiếu trong danh sách, đọc cột Trạng thái\n"
     "4. Mở lại DNTT-01, đọc trạng thái và cột Số tiền duyệt chi của từng dòng\n"
     "5. Mở sổ kế toán, đối chiếu bút toán",
     "—",
     "- Thông báo xanh \"Duyệt phiếu ủy nhiệm chi thành công!\"\n"
     "- Phiếu ở trạng thái Đã hạch toán, nhãn xanh\n"
     "- DNTT-01 chuyển sang trạng thái Duyệt phiếu chi; Số tiền duyệt chi của 2 dòng được cập nhật "
     "đúng 6.000.000 và 4.000.000\n"
     "- ⚠️ Sổ kế toán: vế Nợ ghi đủ 2 dòng tổng 10.000.000, nhưng vế Có CHỈ ghi 4.000.000 của dòng "
     "cuối. Ghi nhận Failed (mục 9 ghi chú 5)"),

    (20, "Quy tắc sinh mã phiếu", "P0",
     "Tài khoản KT-B thuộc công ty có mã TPE; đang là tháng 8 năm 2026; phiếu ủy nhiệm chi gần nhất "
     "của công ty này trong tháng có đuôi 00016",
     "1. Tạo và lưu 2 phiếu ủy nhiệm chi liên tiếp\n"
     "2. Đọc Mã phiếu của cả hai\n"
     "3. Thử sửa ô Mã phiếu trên form",
     "—",
     "- Phiếu thứ nhất: TPE.UNC0826.00017; phiếu thứ hai: TPE.UNC0826.00018\n"
     "- Mã không trùng nhau\n"
     "- Ô Mã phiếu MỜ, không sửa tay được"),

    (21, "Đơn vị của phiếu lấy theo người lập", "P1",
     "Kế toán KT-B thuộc công ty 1, phòng Kế toán; phiếu đề nghị DNTT-C3 do NV thuộc công ty 3 lập",
     "1. Đăng nhập bằng KT-B, tạo phiếu ủy nhiệm chi từ DNTT-C3, bấm Lưu\n"
     "2. Đăng nhập bằng tài khoản quyền tổng công ty, lọc Công ty là Công ty 1, tìm phiếu vừa lập\n"
     "3. Lọc lại Công ty là Công ty 3, tìm phiếu đó",
     "—",
     "- ⚠️ Lọc Công ty 1: KHÔNG ra phiếu vừa lập\n"
     "- Lọc Công ty 3: RA phiếu đó — bộ lọc chạy theo công ty của phiếu đề nghị, còn đơn vị lưu trên "
     "phiếu lại là công ty của người lập (mục 9 ghi chú 4)"),

    (22, "Sửa phiếu nháp và lưu lại", "P0",
     "Phiếu ủy nhiệm chi UNC-01 ở trạng thái Đang tạo, 2 dòng 6.000.000 và 4.000.000, Ghi chú để trống",
     "1. Mở menu Hành động của UNC-01, bấm Sửa\n"
     "2. Đổi Số tiền duyệt chi dòng 2 thành 3.000.000, nhập Ghi chú \"Chi đợt 1\"\n"
     "3. Kiểm tra Ngày hạch toán còn đúng hôm nay, bấm Lưu\n"
     "4. Mở lại chi tiết phiếu",
     "Số tiền duyệt chi dòng 2: 3.000.000 · Ghi chú: Chi đợt 1",
     "- Thông báo xanh \"Cập nhật phiếu ủy nhiệm chi tiền thành công!\"\n"
     "- Mở lại chi tiết: dòng 2 bằng 3.000.000, Ghi chú hiện Chi đợt 1, Tổng cộng bằng 9.000.000\n"
     "- Phiếu vẫn ở trạng thái Đang tạo"),

    (23, "Sửa phiếu nháp rồi bấm Lưu và duyệt", "P0",
     "Phiếu ủy nhiệm chi UNC-02 ở trạng thái Đang tạo, gắn phiếu đề nghị DNTT-02 loại Chi trả nhà cung "
     "cấp, 1 dòng 8.000.000",
     "1. Mở Sửa UNC-02\n"
     "2. Bấm nút Lưu và duyệt\n"
     "3. Đọc thông báo, kiểm tra trạng thái phiếu và trạng thái DNTT-02\n"
     "4. Mở sổ kế toán đối chiếu",
     "—",
     "- Thông báo xanh \"Duyệt phiếu ủy nhiệm chi thành công!\"\n"
     "- Phiếu chuyển sang Đã hạch toán, DNTT-02 chuyển sang Duyệt phiếu chi\n"
     "- Sổ kế toán ghi 8.000.000 cả hai vế Nợ và Có (phiếu 1 dòng nên không dính lỗi ở ghi chú 5)"),

    (24, "Mở đường dẫn Sửa của phiếu đã hạch toán", "P0",
     "Phiếu ủy nhiệm chi UNC-03 ở trạng thái Đã hạch toán, đã ghi sổ 8.000.000; tài khoản KT-B có "
     "quyền Kế toán thanh toán",
     "1. Mở danh sách, xác nhận menu Hành động của UNC-03 không có mục Sửa\n"
     "2. Dán thẳng đường dẫn màn Sửa của UNC-03 vào thanh địa chỉ\n"
     "3. Nếu form mở ra, bấm nút Lưu và duyệt\n"
     "4. Mở sổ kế toán, đếm số bút toán của UNC-03",
     "—",
     "- Mong đợi: hệ thống chặn hoặc đưa về danh sách\n"
     "- ⚠️ Hiện trạng cần kiểm chứng: form Sửa VẪN mở được, và bấm Lưu và duyệt sinh THÊM một bộ bút "
     "toán nữa cho cùng phiếu — sổ có 2 bộ bút toán trùng. Nếu đúng như vậy, ghi nhận Failed (mục 9 "
     "ghi chú 10)"),

    (25, "Phiếu nháp để qua ngày không lưu lại được", "P0",
     "Phiếu ủy nhiệm chi UNC-04 lập từ HÔM QUA, còn ở trạng thái Đang tạo",
     "1. Hôm nay mở Sửa UNC-04\n"
     "2. Đọc ô Ngày hạch toán\n"
     "3. Bấm Lưu mà không sửa gì\n"
     "4. Sửa Ngày hạch toán về hôm nay, bấm Lưu lại",
     "—",
     "- Ô Ngày hạch toán vẫn hiển thị ngày hôm qua\n"
     "- ⚠️ Bước 3: hệ thống báo lỗi dưới ô Ngày hạch toán và KHÔNG lưu; nội dung lỗi hiện bằng TIẾNG "
     "ANH chứ không phải tiếng Việt như các ô khác. Ghi nhận Failed\n"
     "- Bước 4: lưu thành công"),

    (26, "Loại chi phí vận chuyển duyệt ở màn Sửa không ghi sổ", "P0",
     "Phiếu đề nghị DNTT-VC loại Thanh toán chi phí vận chuyển NCC, chuyển khoản, trạng thái Chờ tạo "
     "phiếu chi, 1 dòng 5.000.000",
     "1. Tạo phiếu ủy nhiệm chi từ DNTT-VC, bấm Lưu (để nháp)\n"
     "2. Mở Sửa phiếu vừa lưu, bấm Lưu và duyệt\n"
     "3. Kiểm tra trạng thái phiếu và trạng thái DNTT-VC\n"
     "4. Mở sổ kế toán, tìm bút toán của phiếu này\n"
     "5. Mở lại DNTT-VC, đọc cột Số tiền duyệt chi của dòng chi tiết",
     "Phiếu đề nghị: DNTT-VC",
     "- Phiếu chuyển sang Đã hạch toán, DNTT-VC chuyển sang Duyệt phiếu chi\n"
     "- ⚠️ Sổ kế toán KHÔNG có bút toán nào của phiếu này\n"
     "- ⚠️ Cột Số tiền duyệt chi trên DNTT-VC vẫn bằng 0, không được cập nhật\n"
     "- Ghi nhận Failed — cùng nghiệp vụ nhưng duyệt ngay ở màn Tạo thì có ghi sổ (mục 9 ghi chú 7)"),

    (27, "Loại chi phí vận chuyển duyệt ngay ở màn Tạo thì ghi sổ đúng", "P0",
     "Phiếu đề nghị DNTT-VC2 loại Thanh toán chi phí vận chuyển NCC, chuyển khoản, trạng thái Chờ tạo "
     "phiếu chi, 1 dòng 5.000.000 gắn phiếu hạch toán chuyến CH-001",
     "1. Tạo phiếu ủy nhiệm chi từ DNTT-VC2\n"
     "2. Bấm thẳng nút Lưu và duyệt, KHÔNG lưu nháp trước\n"
     "3. Mở sổ kế toán đối chiếu",
     "Phiếu đề nghị: DNTT-VC2",
     "- Có bút toán 5.000.000 gắn đúng phiếu hạch toán chuyến CH-001 và đúng nhà cung cấp của chuyến "
     "đó\n"
     "- Đối chiếu với ca trước để chứng minh khác biệt giữa hai đường vào"),

    (28, "Bảng chi tiết khi chưa chọn phiếu đề nghị", "P1",
     "Vào thẳng màn Tạo phiếu ủy nhiệm chi bằng nút Tạo mới",
     "1. Không chọn phiếu đề nghị, không chọn loại chi\n"
     "2. Cuộn xuống khối Chi tiết\n"
     "3. Bấm Lưu",
     "—",
     "- Khối Chi tiết hiện dòng \"Không có dữ liệu\"\n"
     "- Bấm Lưu: hiện lỗi đỏ Bắt buộc nhập ở các ô bắt buộc, không tạo được phiếu"),

    (29, "Ghi chú theo từng dòng chi tiết", "P2",
     "Phiếu ủy nhiệm chi đang lập từ phiếu đề nghị có 3 dòng",
     "1. Nhập Ghi chú riêng cho dòng 1 và dòng 3, để trống dòng 2\n"
     "2. Bấm Lưu\n"
     "3. Mở lại màn chi tiết, đọc cột Ghi chú của 3 dòng",
     "Ghi chú dòng 1: Đợt 1 · Ghi chú dòng 3: Còn lại",
     "- Ghi chú lưu đúng theo từng dòng, không bị lệch dòng\n"
     "- Dòng 2 để trống"),

    (30, "Màn chi tiết chỉ đọc", "P0",
     "Phiếu ủy nhiệm chi UNC-05 ở trạng thái Đã hạch toán",
     "1. Bấm mã phiếu UNC-05 để mở chi tiết\n"
     "2. Thử sửa lần lượt: Tài khoản có, Tài khoản nợ, Ngày hạch toán, Tỷ giá, Số tiền duyệt chi, Ghi "
     "chú\n"
     "3. Soát dãy nút cuối trang",
     "—",
     "- Mọi ô đều MỜ, không sửa được, TRỪ ô Ghi chú vẫn gõ được\n"
     "- ⚠️ Ô Ghi chú gõ được nhưng KHÔNG có nút nào để gửi đi — gõ xong thoát trang là mất\n"
     "- Dãy nút cuối trang chỉ có nút Quay lại"),

    (31, "Liên kết mở phiếu đề nghị từ màn chi tiết", "P2",
     "Phiếu ủy nhiệm chi UNC-05 gắn phiếu đề nghị DNTT-05",
     "1. Mở chi tiết UNC-05\n"
     "2. Bấm mã phiếu trong ô Số phiếu đề nghị",
     "—",
     "- Mở màn Chi tiết phiếu đề nghị thanh toán DNTT-05 ở TAB MỚI\n"
     "- Tab cũ vẫn giữ nguyên màn chi tiết phiếu ủy nhiệm chi"),

    (32, "Dữ liệu màn chi tiết khớp với lúc lưu", "P0",
     "Phiếu ủy nhiệm chi UNC-06 vừa lưu với: Tài khoản có tiền gửi ngân hàng, Phương thức Tiền tự có, "
     "Ngân hàng chuyển X, số tài khoản 0011 0000 1234, 2 dòng 6.000.000 và 3.000.000, Ghi chú \"Đợt 1\"",
     "1. Mở chi tiết UNC-06\n"
     "2. Đối chiếu từng ô với dữ liệu đã nhập ở bước lưu\n"
     "3. Đối chiếu bảng chi tiết và dòng Tổng cộng",
     "—",
     "- Toàn bộ 6 thông tin trên khớp chính xác\n"
     "- Bảng chi tiết đúng 2 dòng, Tổng cộng bằng 9.000.000\n"
     "- Hai ô Người đề nghị và Người tạo hiển thị đúng hai người khác nhau"),
]

# ============================================================ SECTION V
SEC_V = [
    (1, "Màn chi tiết không có nút duyệt trong luồng thật", "P0",
     "Tài khoản TQ-F có quyền Thủ quỹ duyệt phiếu chi; chuẩn bị 3 phiếu ủy nhiệm chi ở 3 trạng thái "
     "Đang tạo, Đã hạch toán, Hủy",
     "1. Đăng nhập bằng TQ-F\n"
     "2. Mở chi tiết lần lượt 3 phiếu\n"
     "3. Soát dãy nút cuối trang của từng phiếu",
     "Tài khoản: TQ-F (quyền Thủ quỹ duyệt phiếu chi)",
     "- ⚠️ Cả 3 phiếu đều CHỈ có nút Quay lại\n"
     "- Không phiếu nào hiện nút Duyệt phiếu ủy nhiệm chi hay Hủy phiếu ủy nhiệm chi\n"
     "- Ghi nhận Failed — quyền thủ quỹ không dùng được trên luồng này (mục 9 ghi chú 1)"),

    (2, "Ép một phiếu về trạng thái Chờ duyệt để mở khóa nhóm nút", "P0",
     "Nhờ đội kỹ thuật chỉnh 1 phiếu ủy nhiệm chi sang trạng thái Chờ duyệt bằng dữ liệu; tài khoản "
     "TQ-F có quyền Thủ quỹ duyệt phiếu chi, tài khoản KT-B không có quyền này",
     "1. Đăng nhập bằng TQ-F, mở chi tiết phiếu đó, ghi lại dãy nút\n"
     "2. Đăng nhập bằng KT-B, mở chi tiết cùng phiếu, ghi lại dãy nút",
     "Trạng thái phiếu: Chờ duyệt",
     "- TQ-F: hiện đủ nút Duyệt phiếu ủy nhiệm chi, Hủy phiếu ủy nhiệm chi, Quay lại\n"
     "- KT-B: chỉ có nút Quay lại\n"
     "- Ca này chỉ để kiểm chứng nhóm nút, không phải luồng nghiệp vụ thật"),

    (3, "Duyệt phiếu từ màn chi tiết", "P0",
     "Phiếu ủy nhiệm chi đã ép sang trạng thái Chờ duyệt, gắn phiếu đề nghị DNTT-07, 1 dòng 7.000.000; "
     "đăng nhập bằng TQ-F",
     "1. Mở chi tiết phiếu, bấm Duyệt phiếu ủy nhiệm chi\n"
     "2. Đọc thông báo và trang được chuyển tới\n"
     "3. Kiểm tra trạng thái phiếu, trạng thái DNTT-07 và người duyệt\n"
     "4. Mở sổ kế toán đối chiếu",
     "—",
     "- Thông báo xanh \"Duyệt phiếu ủy nhiệm chi thành công!\"\n"
     "- Hệ thống tự chuyển sang màn Phiếu ủy nhiệm chi đã duyệt\n"
     "- Phiếu ở trạng thái Đã hạch toán, người duyệt là TQ-F\n"
     "- DNTT-07 chuyển sang Duyệt phiếu chi; sổ kế toán ghi 7.000.000 hai vế"),

    (4, "Hủy phiếu khi chưa nhập Ghi chú", "P0",
     "Phiếu ủy nhiệm chi đã ép sang trạng thái Chờ duyệt; ô Ghi chú đang trống; đăng nhập bằng TQ-F",
     "1. Mở chi tiết phiếu, để trống ô Ghi chú\n"
     "2. Bấm Hủy phiếu ủy nhiệm chi\n"
     "3. Bấm Xác nhận trên cửa sổ hỏi lại\n"
     "4. Đọc màn hình",
     "Ghi chú: để trống",
     "- Hiện lỗi đỏ \"Bắt buộc nhập\" ngay dưới ô Ghi chú\n"
     "- Phiếu VẪN ở trạng thái Chờ duyệt, chưa bị hủy\n"
     "- Dữ liệu trên form không bị mất"),

    (5, "Bỏ qua cửa sổ xác nhận hủy", "P1",
     "Phiếu ủy nhiệm chi đã ép sang trạng thái Chờ duyệt; đăng nhập bằng TQ-F",
     "1. Nhập Ghi chú \"Hủy do sai tài khoản\"\n"
     "2. Bấm Hủy phiếu ủy nhiệm chi\n"
     "3. Trên cửa sổ \"Bạn chắc chắn muốn thực hiện hành động này?\" bấm nút Hủy\n"
     "4. Đọc lại trạng thái phiếu",
     "Ghi chú: Hủy do sai tài khoản",
     "- Cửa sổ đóng lại, không gửi gì lên hệ thống\n"
     "- Phiếu giữ nguyên trạng thái Chờ duyệt"),

    (6, "Hủy phiếu không trả trạng thái phiếu đề nghị", "P0",
     "Phiếu ủy nhiệm chi đã ép sang trạng thái Chờ duyệt, gắn phiếu đề nghị DNTT-08 đang ở trạng thái "
     "Chờ tạo phiếu chi; đăng nhập bằng TQ-F",
     "1. Nhập Ghi chú \"Hủy do sai tài khoản\"\n"
     "2. Bấm Hủy phiếu ủy nhiệm chi, bấm Xác nhận\n"
     "3. Đọc thông báo\n"
     "4. Kiểm tra trạng thái phiếu ủy nhiệm chi và trạng thái DNTT-08",
     "Ghi chú: Hủy do sai tài khoản",
     "- Phiếu ủy nhiệm chi chuyển sang trạng thái Hủy\n"
     "- ⚠️ Thông báo hiện ra là \"Cập nhật phiếu ủy nhiệm chi tiền thành công!\" chứ không phải \"Hủy "
     "... thành công!\" — sai nội dung thông báo\n"
     "- ⚠️ DNTT-08 KHÔNG đổi trạng thái, vẫn ở Chờ tạo phiếu chi. Cần chốt nghiệp vụ: có phải mong "
     "muốn để lập lại phiếu khác hay là thiếu xử lý"),

    (7, "Duyệt lại phiếu đã hạch toán", "P0",
     "Phiếu ủy nhiệm chi UNC-07 ở trạng thái Đã hạch toán, đã ghi sổ 7.000.000",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Cập nhật của UNC-07, gửi kèm trạng thái Đã hạch "
     "toán một lần nữa\n"
     "2. Mở sổ kế toán, đếm số bút toán gắn với UNC-07",
     "Trạng thái gửi lên: Đã hạch toán",
     "- Mong đợi: hệ thống báo phiếu đã được duyệt, không xử lý tiếp\n"
     "- ⚠️ Hiện trạng cần kiểm chứng: sổ có THÊM một bộ bút toán 7.000.000 nữa. Nếu đúng như vậy, ghi "
     "nhận Failed và báo lỗ hổng"),

    (8, "Không có thông báo nào được gửi trong luồng ủy nhiệm chi", "P0",
     "Tài khoản NV-A lập phiếu đề nghị DNTT-09; KT-B là kế toán thanh toán; TQ-F có quyền Thủ quỹ "
     "duyệt phiếu chi",
     "1. KT-B tạo phiếu ủy nhiệm chi từ DNTT-09, bấm Lưu\n"
     "2. Sau đó mở Sửa và bấm Lưu và duyệt\n"
     "3. Đăng nhập lần lượt bằng NV-A và TQ-F, mở chuông thông báo\n"
     "4. Lặp lại toàn bộ nghiệp vụ trên màn Phiếu chi tiền mặt với một phiếu đề nghị tiền mặt, kiểm "
     "tra chuông của TQ-F",
     "—",
     "- ⚠️ Sau bước 3: cả NV-A và TQ-F đều KHÔNG nhận được thông báo nào\n"
     "- Bước 4: màn Phiếu chi tiền mặt VẪN gửi thông báo cho nhóm thủ quỹ\n"
     "- Ghi nhận Failed — cần chốt nghiệp vụ đây là cố ý bỏ hay thiếu (mục 9 ghi chú 22)"),
]

# ============================================================ SECTION VI
SEC_VI = [
    (1, "Xóa phiếu ở trạng thái Đang tạo", "P0",
     "Phiếu ủy nhiệm chi UNC-08 ở trạng thái Đang tạo, có 3 dòng chi tiết; tài khoản KT-B là người lập",
     "1. Mở menu Hành động của UNC-08, bấm Xóa\n"
     "2. Bấm Xác nhận trên cửa sổ hỏi lại\n"
     "3. Đọc thông báo và danh sách",
     "—",
     "- Thông báo xanh \"Xóa phiếu ủy nhiệm chi thành công!\"\n"
     "- Quay lại danh sách, UNC-08 biến mất\n"
     "- Tổng giảm đúng 1 đơn vị"),

    (2, "Bỏ qua cửa sổ xác nhận xóa", "P1",
     "Phiếu ủy nhiệm chi UNC-09 ở trạng thái Đang tạo",
     "1. Bấm Xóa ở menu Hành động\n"
     "2. Bấm nút Hủy trên cửa sổ xác nhận\n"
     "3. Đọc lại danh sách",
     "—",
     "- Không xóa gì, UNC-09 còn nguyên\n"
     "- Tổng không đổi"),

    (3, "Dán thẳng đường dẫn xóa phiếu đã hạch toán", "P0",
     "Phiếu ủy nhiệm chi UNC-10 ở trạng thái Đã hạch toán, đã ghi sổ 12.000.000; tài khoản KT-B có "
     "quyền Kế toán thanh toán",
     "1. Xác nhận menu Hành động của UNC-10 KHÔNG có mục Xóa\n"
     "2. Ghi lại mã phiếu, dán thẳng đường dẫn Xóa của phiếu đó\n"
     "3. Mở lại danh sách và sổ kế toán",
     "—",
     "- Mong đợi: hệ thống từ chối vì phiếu đã ghi sổ\n"
     "- ⚠️ Hiện trạng cần kiểm chứng: phiếu bị xóa khỏi danh sách trong khi bút toán 12.000.000 vẫn "
     "còn nguyên trong sổ, không có cách nào lần ngược về chứng từ gốc. Nếu đúng như vậy, ghi nhận "
     "Failed và báo lỗ hổng (mục 9 ghi chú 11)"),

    (4, "Dòng chi tiết còn sót lại sau khi xóa phiếu", "P1",
     "Phiếu ủy nhiệm chi UNC-11 ở trạng thái Đang tạo, có 3 dòng chi tiết",
     "1. Nhờ đội kỹ thuật đếm số dòng chi tiết đang gắn với UNC-11\n"
     "2. Xóa UNC-11 từ giao diện\n"
     "3. Nhờ đội kỹ thuật đếm lại số dòng chi tiết còn gắn mã phiếu đó",
     "—",
     "- Mong đợi: 3 dòng chi tiết bị xóa theo\n"
     "- ⚠️ Hiện trạng cần kiểm chứng: 3 dòng chi tiết VẪN còn, trở thành dữ liệu mồ côi. Nếu đúng như "
     "vậy, ghi nhận Failed"),

    (5, "Phiếu đề nghị kẹt sau khi xóa phiếu đã duyệt", "P0",
     "Phiếu đề nghị DNTT-10 ở trạng thái Chờ tạo phiếu chi",
     "1. Tạo phiếu ủy nhiệm chi từ DNTT-10, bấm Lưu và duyệt (DNTT-10 chuyển sang Duyệt phiếu chi)\n"
     "2. Dán đường dẫn Xóa của phiếu ủy nhiệm chi vừa duyệt\n"
     "3. Mở lại chi tiết DNTT-10, đọc trạng thái và soát dãy nút cuối trang",
     "—",
     "- ⚠️ DNTT-10 giữ nguyên trạng thái Duyệt phiếu chi, KHÔNG quay về Chờ tạo phiếu chi\n"
     "- ⚠️ Nút Tạo phiếu ủy nhiệm chi biến mất, không lập lại phiếu được từ giao diện — phiếu đề nghị "
     "kẹt vĩnh viễn\n"
     "- Ghi nhận Failed (mục 9 ghi chú 12)"),

    (6, "Xóa phiếu nháp không ảnh hưởng phiếu đề nghị", "P1",
     "Phiếu đề nghị DNTT-11 ở trạng thái Chờ tạo phiếu chi; đã tạo 1 phiếu ủy nhiệm chi từ đó và để "
     "trạng thái Đang tạo",
     "1. Xóa phiếu ủy nhiệm chi nháp đó\n"
     "2. Mở lại chi tiết DNTT-11, đọc trạng thái và soát nút\n"
     "3. Bấm Tạo phiếu ủy nhiệm chi lại",
     "—",
     "- DNTT-11 vẫn ở Chờ tạo phiếu chi\n"
     "- Nút Tạo phiếu ủy nhiệm chi vẫn còn, bấm vào lập lại được bình thường"),
]

# ============================================================ SECTION VII
SEC_VII = [
    (1, "Chuyển form sang chế độ chi thu nhập nhân viên", "P0",
     "Tài khoản KT-B có quyền Kế toán thanh toán",
     "1. Bấm nút Tạo mới ở màn danh sách\n"
     "2. Không chọn phiếu đề nghị, bung ô Loại chi và chọn Chi thu nhập cho nhân viên\n"
     "3. Quan sát toàn bộ form",
     "Loại chi: Chi thu nhập cho nhân viên",
     "- Khối Số phiếu đề nghị biến mất\n"
     "- Hiện khối riêng gồm: Người nhận tiền, Phòng ban, Lý do chi, Ngân hàng chuyển, Số tài khoản "
     "chuyển khoản\n"
     "- Khối Chi tiết có thêm nút \"Lấy nhân viên\""),

    (2, "Tài khoản có và Loại tiền bị ép cứng", "P0",
     "Đang ở màn Tạo với Loại chi là Chi thu nhập cho nhân viên",
     "1. Đọc ô Tài khoản có và ô Loại tiền\n"
     "2. Thử bấm đổi hai ô đó\n"
     "3. Thử gõ vào ô Tỷ giá",
     "—",
     "- Tài khoản có được đặt sẵn tài khoản tiền gửi ngân hàng và bị KHÓA\n"
     "- Loại tiền bị đặt về tiền Việt Nam và bị KHÓA\n"
     "- Ô Tỷ giá cũng bị khóa theo"),

    (3, "Bấm Lấy nhân viên khi chưa chọn Phòng ban", "P0",
     "Đang ở màn Tạo với Loại chi là Chi thu nhập cho nhân viên, ô Phòng ban còn trống",
     "1. Bấm nút Lấy nhân viên\n"
     "2. Đọc thông báo và khối Chi tiết",
     "Phòng ban: để trống",
     "- Thông báo vàng \"Chưa chọn phòng ban\"\n"
     "- Khối Chi tiết vẫn rỗng, không gọi dữ liệu"),

    (4, "Lấy danh sách nhân viên theo phòng ban", "P0",
     "Phòng Kinh doanh 1 có 6 nhân viên đang có số dư các khoản thu nhập",
     "1. Chọn Phòng ban là Kinh doanh 1\n"
     "2. Bấm nút Lấy nhân viên\n"
     "3. Đọc bảng chi tiết và tiêu đề các cột",
     "Phòng ban: Kinh doanh 1",
     "- Bảng đổ đúng 6 dòng, mỗi dòng một nhân viên\n"
     "- Các cột gồm: ô tick, STT, Số tài khoản nợ, Tên tài khoản, Nhân viên, Số dư, Số tiền chi, Tài "
     "khoản, Tên ngân hàng, Chi nhánh\n"
     "- Cột Số dư hiện đúng số dư từng khoản của nhân viên"),

    (5, "Phòng ban không có nhân viên", "P1",
     "Phòng Hành chính không có nhân viên nào có số dư thu nhập",
     "1. Chọn Phòng ban là Hành chính\n"
     "2. Bấm Lấy nhân viên",
     "Phòng ban: Hành chính",
     "- Thông báo vàng \"Không có dữ liệu nhân viên\"\n"
     "- Khối Chi tiết hiện dòng Không có dữ liệu"),

    (6, "Đổi phòng ban xóa sạch dữ liệu đã lấy", "P0",
     "Đã lấy 6 nhân viên phòng Kinh doanh 1 và nhập số tiền chi cho 3 người",
     "1. Đổi ô Phòng ban sang Kinh doanh 2\n"
     "2. Quan sát bảng chi tiết\n"
     "3. Bấm Lấy nhân viên lại",
     "Phòng ban: đổi sang Kinh doanh 2",
     "- ⚠️ Toàn bộ 6 dòng và số tiền vừa nhập bị XÓA SẠCH ngay khi đổi phòng ban, không có cảnh báo\n"
     "- Bấm Lấy nhân viên mới nạp lại danh sách của Kinh doanh 2"),

    (7, "Hai thẻ Chi tiết và Chi tiết vụ việc", "P1",
     "Đã lấy danh sách nhân viên phòng Kinh doanh 1 và nhập số tiền cho 2 người",
     "1. Đọc bảng ở thẻ Chi tiết\n"
     "2. Chuyển sang thẻ Chi tiết vụ việc\n"
     "3. Đối chiếu tổng số tiền của 2 thẻ",
     "—",
     "- Thẻ Chi tiết: một dòng một nhân viên, có tài khoản nợ và thông tin ngân hàng\n"
     "- Thẻ Chi tiết vụ việc: tách theo từng mã vụ việc của nhân viên\n"
     "- Tổng số tiền hai thẻ khớp nhau"),

    (8, "Ô tick chọn nhân viên cần chi", "P0",
     "Đã lấy 6 nhân viên; cả 6 đang được tick sẵn",
     "1. Bỏ tick dòng 3, quan sát dòng đó\n"
     "2. Bỏ tick ô chọn tất cả ở tiêu đề bảng\n"
     "3. Tick lại ô chọn tất cả",
     "—",
     "- Dòng bỏ tick bị làm MỜ và ô Số tiền chi của dòng đó bị khóa\n"
     "- Bỏ tick ô tiêu đề: cả 6 dòng cùng bỏ tick\n"
     "- Tick lại: cả 6 dòng cùng được tick"),

    (9, "Chỉ nhân viên được tick mới được lưu", "P0",
     "Đã lấy 6 nhân viên, chỉ tick 2 người và nhập số tiền chi cho 2 người đó",
     "1. Điền nốt các ô bắt buộc, bấm Lưu\n"
     "2. Mở lại chi tiết phiếu vừa lưu\n"
     "3. Đếm số dòng trong bảng chi tiết",
     "Số nhân viên được tick: 2",
     "- Phiếu chỉ có đúng 2 dòng, đúng 2 nhân viên đã tick\n"
     "- 4 nhân viên bỏ tick không xuất hiện"),

    (10, "Đổi tài khoản nợ ở dòng đầu áp cho toàn bộ dòng", "P1",
     "Đã lấy 6 nhân viên, các dòng đang cùng một tài khoản nợ mặc định",
     "1. Đổi Số tài khoản nợ của DÒNG ĐẦU TIÊN sang tài khoản khác\n"
     "2. Soát cột Số tài khoản nợ của 5 dòng còn lại\n"
     "3. Đọc lại cột Số dư của các dòng",
     "—",
     "- Cả 6 dòng cùng đổi sang tài khoản vừa chọn\n"
     "- Số dư từng dòng được nạp lại theo tài khoản mới\n"
     "- Đổi tài khoản ở dòng 3 thì CHỈ dòng 3 đổi, không lan sang dòng khác"),

    (11, "Ràng buộc nhập liệu riêng cho chi thu nhập nhân viên", "P0",
     "Đã lấy danh sách nhân viên, tick 2 người",
     "1. Xóa trắng ô Lý do chi, bấm Lưu\n"
     "2. Điền lại Lý do chi, xóa trắng Số tài khoản nợ của dòng 1, bấm Lưu\n"
     "3. Điền lại tài khoản, gõ chữ abc vào ô Số tiền chi, bấm Lưu",
     "Lý do chi: để trống · Số tài khoản nợ: để trống · Số tiền chi: abc",
     "- Bước 1: lỗi đỏ Bắt buộc nhập dưới ô Lý do chi\n"
     "- Bước 2: lỗi đỏ Bắt buộc nhập dưới ô Số tài khoản nợ của đúng dòng 1\n"
     "- Bước 3: hệ thống báo giá trị phải là số, hoặc ô tự về 0; không lưu được phiếu sai kiểu"),

    (12, "Cảnh báo lệch số tiền theo vụ việc không chạy ở màn Tạo", "P0",
     "Đã lấy nhân viên, tick 1 người; ở thẻ Chi tiết vụ việc nhập tổng các khoản LỆCH so với Số tiền "
     "chi ở thẻ Chi tiết",
     "1. Đối chiếu tổng hai thẻ, xác nhận có lệch\n"
     "2. Bấm nút Lưu và duyệt ở màn Tạo\n"
     "3. Đọc thông báo và trạng thái phiếu\n"
     "4. Mở sổ kế toán đối chiếu",
     "Tổng theo vụ việc lệch so với Số tiền chi",
     "- Mong đợi: hệ thống chặn, báo tổng số tiền chi theo mã vụ việc và tổng số tiền đề nghị chi khác "
     "nhau\n"
     "- ⚠️ Hiện trạng cần kiểm chứng: KHÔNG có cảnh báo nào, phiếu lệch vẫn ghi sổ. Nếu đúng như vậy, "
     "ghi nhận Failed (mục 9 ghi chú 18)"),

    (13, "Số tiền chi vượt số dư của nhân viên", "P0",
     "Nhân viên NV-K có số dư hoa hồng tháng là 3.000.000",
     "1. Nhập Số tiền chi khoản hoa hồng tháng của NV-K là 5.000.000\n"
     "2. Bấm Lưu và duyệt\n"
     "3. Đọc thông báo, kiểm tra sổ kế toán",
     "Số tiền chi hoa hồng tháng: 5.000.000 (số dư 3.000.000)",
     "- Mong đợi: hệ thống chặn, báo số tiền chi không được lớn hơn số dư\n"
     "- ⚠️ Hiện trạng cần kiểm chứng: cảnh báo này cũng chỉ chạy ở màn chi tiết nên duyệt từ màn Tạo "
     "vẫn ghi sổ 5.000.000. Nếu đúng như vậy, ghi nhận Failed"),

    (14, "Dòng Tổng cộng của bảng nhân viên", "P1",
     "Đã lấy nhân viên, tick 3 người với số tiền chi lần lượt 2.000.000, 3.000.000, 5.000.000",
     "1. Nhập số tiền cho 3 người\n"
     "2. Đọc dòng Tổng cộng của bảng\n"
     "3. Sửa số của người thứ hai thành 1.000.000, đọc lại",
     "Số tiền chi: 2.000.000 · 3.000.000 · 5.000.000",
     "- Tổng cộng bằng 10.000.000\n"
     "- Sau khi sửa: Tổng cộng bằng 8.000.000, cập nhật ngay không cần bấm gì"),

    (15, "Lưu và duyệt phiếu chi thu nhập nhân viên", "P0",
     "Đã lấy nhân viên, tick 2 người, mỗi người có đủ 5 khoản dương",
     "1. Bấm Lưu và duyệt\n"
     "2. Đọc thông báo, kiểm tra trạng thái phiếu\n"
     "3. Mở sổ kế toán, soát bút toán theo từng mã vụ việc\n"
     "4. Kiểm tra xem có phiếu đề nghị nào bị đổi trạng thái không",
     "—",
     "- Thông báo xanh \"Duyệt phiếu ủy nhiệm chi thành công!\"\n"
     "- Phiếu ở trạng thái Đã hạch toán\n"
     "- Sổ kế toán có bút toán tách theo từng mã vụ việc: chênh lệch, hoa hồng tháng, hoa hồng quý, "
     "thưởng quý, tiền vận chuyển; kèm đúng nhân viên và phòng ban chi\n"
     "- KHÔNG có phiếu đề nghị nào bị đổi trạng thái (phiếu này không gắn đề nghị)"),

    (16, "Khoản âm đảo chiều ghi sổ", "P0",
     "Nhân viên NV-K có khoản chênh lệch ÂM 2.000.000, các khoản khác bằng 0",
     "1. Nhập Số tiền chi khoản chênh lệch là -2.000.000\n"
     "2. Bấm Lưu và duyệt\n"
     "3. Mở sổ kế toán, đọc vế ghi của bút toán chênh lệch",
     "Chênh lệch: -2.000.000",
     "- Bút toán chênh lệch ghi vế CÓ với giá trị tuyệt đối 2.000.000\n"
     "- Bút toán đối ứng tài khoản ngân hàng ghi vế NỢ"),

    (17, "Khoản thưởng quý âm ghi sai vế", "P0",
     "Nhân viên NV-L có khoản thưởng quý ÂM 1.000.000, bốn khoản còn lại bằng 0",
     "1. Nhập Số tiền chi khoản thưởng quý là -1.000.000\n"
     "2. Bấm Lưu và duyệt\n"
     "3. Mở sổ kế toán, đọc vế ghi của bút toán thưởng quý\n"
     "4. So với ca trước (khoản chênh lệch âm)",
     "Thưởng quý: -1.000.000",
     "- Mong đợi: ghi vế CÓ giống khoản chênh lệch âm\n"
     "- ⚠️ Hiện trạng cần kiểm chứng: bút toán thưởng quý ghi vế NỢ, ngược chiều so với bốn khoản còn "
     "lại và lệch với bút toán đối ứng. Nếu đúng như vậy, ghi nhận Failed (mục 9 ghi chú 19)"),
]

# ============================================================ SECTION VIII
SEC_VIII = [
    (1, "Bỏ trống Tài khoản có", "P0",
     "Đang ở màn Tạo với đầy đủ dữ liệu hợp lệ từ phiếu đề nghị DNTT-01",
     "1. Xóa lựa chọn ở ô Tài khoản có\n"
     "2. Bấm Lưu",
     "Tài khoản có: để trống",
     "- Lỗi đỏ \"Bắt buộc nhập\" ngay dưới ô Tài khoản có\n"
     "- Có thông báo vàng phía trên màn hình\n"
     "- Phiếu không được tạo, dữ liệu đã nhập vẫn còn trên form"),

    (2, "Bỏ trống Tài khoản nợ", "P0",
     "Đang ở màn Tạo từ phiếu đề nghị loại Chi trả nhà cung cấp",
     "1. Xóa lựa chọn ở ô Tài khoản nợ\n"
     "2. Bấm Lưu",
     "Tài khoản nợ: để trống",
     "- Lỗi đỏ \"Bắt buộc nhập\" ngay dưới ô Tài khoản nợ\n"
     "- Phiếu không được tạo"),

    (3, "Bỏ trống Phương thức thanh toán", "P0",
     "Đang ở màn Tạo với đầy đủ dữ liệu hợp lệ",
     "1. Xóa lựa chọn ở ô Phương thức thanh toán\n"
     "2. Bấm Lưu",
     "Phương thức thanh toán: để trống",
     "- Lỗi đỏ \"Bắt buộc nhập\" ngay dưới ô Phương thức thanh toán\n"
     "- Phiếu không được tạo"),

    (4, "Bỏ trống Ngân hàng chuyển và Số tài khoản chuyển khoản", "P0",
     "Đang ở màn Tạo với đầy đủ dữ liệu hợp lệ",
     "1. Không chọn Ngân hàng chuyển, không chọn Số tài khoản chuyển khoản\n"
     "2. Bấm Lưu",
     "Ngân hàng chuyển: để trống · Số tài khoản chuyển khoản: để trống",
     "- Lỗi đỏ \"Bắt buộc nhập\" dưới CẢ HAI ô\n"
     "- Phiếu không được tạo"),

    (5, "Bỏ trống Số phiếu đề nghị với ba loại chi bắt buộc", "P0",
     "Vào thẳng màn Tạo, chọn Loại chi là Chi trả nhà cung cấp, không chọn phiếu đề nghị",
     "1. Điền các ô khác, bấm Lưu\n"
     "2. Lặp lại với Loại chi là Chi trả lại khách hàng, rồi Chi thưởng NVKD",
     "Loại chi: Chi trả nhà cung cấp / Chi trả lại khách hàng / Chi thưởng NVKD",
     "- Cả 3 lần đều hiện lỗi đỏ \"Bắt buộc nhập\" dưới ô Số phiếu đề nghị\n"
     "- Phiếu không được tạo"),

    (6, "Số tiền duyệt chi bằng 0 chặn cả phiếu", "P0",
     "Phiếu đề nghị DNTT-03 loại Chi trả nhà cung cấp có 3 dòng: 5.000.000, 3.000.000, 2.000.000",
     "1. Tạo phiếu ủy nhiệm chi từ DNTT-03\n"
     "2. Xóa trắng ô Số tiền duyệt chi của DÒNG 2 (để bằng 0)\n"
     "3. Bấm Lưu\n"
     "4. Đọc thông báo và soát các dòng còn lại",
     "Số tiền duyệt chi dòng 2: 0",
     "- ⚠️ Hệ thống chặn CẢ PHIẾU, không lưu được dòng nào, dù nghiệp vụ chỉ muốn bỏ qua dòng 2\n"
     "- Lỗi hiện dưới ô Số tiền duyệt chi của dòng 2\n"
     "- Ghi nhận và chốt nghiệp vụ: nếu muốn bỏ qua một dòng thì hiện chưa có cách nào (mục 9 ghi "
     "chú 16)"),

    (7, "Số tiền duyệt chi bằng 0 với các loại chi khác", "P1",
     "Phiếu đề nghị DNTT-06 loại Chi thưởng thực hiện hợp đồng có 3 dòng",
     "1. Tạo phiếu ủy nhiệm chi từ DNTT-06\n"
     "2. Để dòng 2 bằng 0, bấm Lưu và duyệt\n"
     "3. Mở sổ kế toán đối chiếu",
     "Số tiền duyệt chi dòng 2: 0",
     "- Loại chi này KHÔNG bị chặn, phiếu lưu được\n"
     "- Sổ kế toán chỉ ghi bút toán cho dòng 1 và dòng 3, bỏ qua dòng 2\n"
     "- ⚠️ Nếu để DÒNG CUỐI bằng 0 thì số tiền vế Có lấy nhầm của dòng liền trước — kiểm cả trường hợp "
     "này (mục 9 ghi chú 5)"),

    (8, "Ngày hạch toán không được ở quá khứ", "P0",
     "Đang ở màn Tạo với đầy đủ dữ liệu hợp lệ",
     "1. Đổi Ngày hạch toán về ngày hôm qua, bấm Lưu\n"
     "2. Đọc nội dung lỗi\n"
     "3. Đổi sang ngày mai, bấm Lưu",
     "Ngày hạch toán: hôm qua rồi ngày mai",
     "- Hôm qua: hệ thống báo lỗi dưới ô Ngày hạch toán, không lưu\n"
     "- ⚠️ Nội dung lỗi hiện bằng TIẾNG ANH, không đồng bộ với các ô khác. Ghi nhận Failed về hiển thị\n"
     "- Ngày mai: lưu thành công"),

    (9, "Tỷ giá bằng 0 với phiếu ngoại tệ", "P0",
     "Đang ở màn Tạo từ phiếu đề nghị loại tiền đô la Mỹ, ô Tỷ giá đang là 0",
     "1. Không nhập tỷ giá, bấm Lưu\n"
     "2. Đọc nội dung lỗi\n"
     "3. Nhập chữ abc vào ô Tỷ giá, bấm Lưu\n"
     "4. Nhập 25.000, bấm Lưu",
     "Tỷ giá: 0 · abc · 25.000",
     "- Bước 1 và 3: lỗi đỏ dưới ô Tỷ giá, nội dung \"Nhập số lớn hơn 0\"\n"
     "- Bước 4: lưu thành công"),

    (10, "Nhập chữ vào ô số tiền", "P1",
     "Đang ở màn Tạo với bảng chi tiết đã có dữ liệu",
     "1. Gõ abc vào ô Số tiền duyệt chi dòng 1, bấm ra ngoài ô\n"
     "2. Đọc lại giá trị trong ô và cột quy đổi VND",
     "Số tiền duyệt chi: abc",
     "- Ô tự về 0, KHÔNG hiện chữ lạ hay báo lỗi kỹ thuật\n"
     "- Cột quy đổi VND về 0 theo\n"
     "- Dòng Tổng cộng tính lại đúng"),

    (11, "Số tiền rất lớn", "P1",
     "Phiếu đề nghị có 1 dòng với Số tiền đề nghị chi 1.234.567.890.123",
     "1. Tạo phiếu ủy nhiệm chi từ phiếu đề nghị đó\n"
     "2. Đọc ô Số tiền duyệt chi và dòng Tổng cộng\n"
     "3. Lưu rồi mở lại chi tiết",
     "Số tiền: 1.234.567.890.123",
     "- Hiển thị đủ chữ số, có dấu phân cách nghìn, không bị cắt hay hiện dạng rút gọn\n"
     "- Dòng Tổng cộng đúng\n"
     "- Mở lại chi tiết vẫn đúng con số đó"),

    (12, "Số thập phân với phiếu ngoại tệ", "P1",
     "Đang ở màn Tạo từ phiếu đề nghị loại tiền đô la Mỹ, tỷ giá 25.000",
     "1. Nhập 1000.55 vào ô Số tiền duyệt chi\n"
     "2. Nhập tiếp 1000.5555\n"
     "3. Nhập tỷ giá 25123.456789",
     "Số tiền: 1000.55 rồi 1000.5555 · Tỷ giá: 25123.456789",
     "- Số tiền giữ tối đa 2 chữ số thập phân\n"
     "- Tỷ giá làm tròn còn 2 chữ số thập phân\n"
     "- Con trỏ không nhảy về đầu ô khi đang gõ dấu chấm"),

    (13, "Ô nhập tự do chống mã độc", "P1",
     "Đang ở màn Tạo với đầy đủ dữ liệu hợp lệ",
     "1. Nhập đoạn mã kịch bản vào các ô Ghi chú, Người nhận tiền, Lý do chi\n"
     "2. Bấm Lưu\n"
     "3. Mở danh sách và mở chi tiết phiếu vừa lưu",
     "Ghi chú: đoạn mã kịch bản mở cửa sổ cảnh báo",
     "- Chuỗi hiển thị nguyên văn dạng chữ ở cả danh sách và chi tiết\n"
     "- KHÔNG có cửa sổ cảnh báo nào bật lên"),

    (14, "Danh sách tài khoản chuyển ở màn Tạo và màn Sửa khác nhau", "P1",
     "Công ty có tài khoản 0011 0000 9999 đã chuyển sang trạng thái ngừng hoạt động; đã có 1 phiếu ủy "
     "nhiệm chi nháp dùng tài khoản khác",
     "1. Mở màn Tạo, bung ô Số tài khoản chuyển khoản, tìm tài khoản 0011 0000 9999\n"
     "2. Mở màn Sửa phiếu nháp, bung ô đó, tìm lại\n"
     "3. Mở màn chi tiết một phiếu đã lưu, bung ô đó",
     "Tài khoản: 0011 0000 9999 (đã ngừng hoạt động)",
     "- Màn Tạo: KHÔNG có tài khoản đã ngừng\n"
     "- ⚠️ Màn Sửa và màn chi tiết: VẪN có tài khoản đã ngừng trong danh sách. Cần chốt nghiệp vụ "
     "(mục 9 ghi chú 20)"),

    (15, "Bấm Lưu nhiều lần liên tiếp", "P0",
     "Đang ở màn Tạo với đầy đủ dữ liệu hợp lệ",
     "1. Bấm nút Lưu 3 lần thật nhanh\n"
     "2. Quan sát nút và biểu tượng trên nút\n"
     "3. Mở danh sách, đếm số phiếu vừa tạo",
     "—",
     "- Ngay lần bấm đầu, nút chuyển sang mờ và hiện biểu tượng đang xử lý\n"
     "- Chỉ đúng 1 phiếu được tạo"),

    (16, "Mất kết nối khi đang lưu", "P2",
     "Đang ở màn Tạo với đầy đủ dữ liệu hợp lệ",
     "1. Ngắt kết nối mạng\n"
     "2. Bấm nút Lưu\n"
     "3. Đọc thông báo và kiểm tra dữ liệu trên form",
     "—",
     "- Thông báo đỏ \"Đã có lỗi xảy ra\"\n"
     "- Nút Lưu bật sáng trở lại, bấm lại được\n"
     "- Dữ liệu đang nhập trên form KHÔNG bị mất"),

    (17, "Gọi chức năng Lưu mà không kèm dấu xác thực phiên", "P1",
     "Tài khoản KT-B đang đăng nhập hợp lệ",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Lưu phiếu, cố tình bỏ dấu xác thực phiên làm "
     "việc\n"
     "2. Mở danh sách kiểm tra",
     "—",
     "- Hệ thống từ chối, không tạo phiếu nào\n"
     "- Danh sách không có bản ghi mới"),

    (18, "Hiển thị trên màn hình nhỏ", "P2",
     "Đang ở màn Tạo với bảng chi tiết có 5 dòng, phiếu ngoại tệ (nhiều cột)",
     "1. Thu nhỏ cửa sổ trình duyệt còn khoảng nửa màn hình\n"
     "2. Cuộn ngang bảng chi tiết\n"
     "3. Kiểm tra các nút cuối trang",
     "—",
     "- Bảng chi tiết cuộn ngang trong khung riêng, không làm vỡ bố cục trang\n"
     "- Các nút Lưu, Lưu và duyệt, Quay lại vẫn bấm được"),
]

# ============================================================ SECTION IX
SEC_IX = [
    (1, "Hai kế toán cùng lập phiếu cho một phiếu đề nghị", "P0",
     "Phiếu đề nghị DNTT-12 ở trạng thái Chờ tạo phiếu chi, 1 dòng 9.000.000; hai kế toán KT-B và KT-C "
     "đều có quyền Kế toán thanh toán",
     "1. KT-B và KT-C cùng mở chi tiết DNTT-12, cùng bấm Tạo phiếu ủy nhiệm chi\n"
     "2. Hai người cùng bấm Lưu và duyệt gần như đồng thời\n"
     "3. Mở danh sách, lọc theo mã DNTT-12\n"
     "4. Mở sổ kế toán, đếm bút toán liên quan DNTT-12",
     "Phiếu đề nghị: DNTT-12",
     "- Mong đợi: chỉ 1 phiếu được tạo, người thứ hai nhận thông báo phiếu đề nghị đã lập phiếu\n"
     "- ⚠️ Hiện trạng cần kiểm chứng: cả 2 phiếu ủy nhiệm chi cùng được tạo và sổ kế toán có 2 bộ bút "
     "toán 9.000.000 cho cùng một khoản chi. Nếu đúng như vậy, ghi nhận Failed và báo lỗ hổng"),

    (2, "Lập phiếu thứ hai sau khi phiếu thứ nhất còn ở trạng thái nháp", "P0",
     "Phiếu đề nghị DNTT-13 ở trạng thái Chờ tạo phiếu chi; đã tạo 1 phiếu ủy nhiệm chi từ đó và bấm "
     "Lưu (nháp)",
     "1. Mở lại chi tiết DNTT-13, đọc trạng thái và soát dãy nút\n"
     "2. Bấm Tạo phiếu ủy nhiệm chi lần thứ hai\n"
     "3. Bấm Lưu\n"
     "4. Lọc danh sách theo mã DNTT-13, đếm số phiếu",
     "Phiếu đề nghị: DNTT-13",
     "- Mong đợi: hệ thống chặn ngay từ nút hoặc lúc lưu\n"
     "- ⚠️ Hiện trạng cần kiểm chứng: DNTT-13 vẫn ở Chờ tạo phiếu chi nên nút vẫn còn, tạo được phiếu "
     "thứ hai; 2 phiếu cùng trỏ một phiếu đề nghị. Nếu đúng như vậy, ghi nhận Failed (mục 5)"),

    (3, "Đổi sang phiếu đề nghị đã có phiếu khác", "P1",
     "Phiếu ủy nhiệm chi UNC-12 ở trạng thái Đang tạo gắn DNTT-14; phiếu đề nghị DNTT-15 đã có một "
     "phiếu ủy nhiệm chi khác ở trạng thái nháp",
     "1. Mở Sửa UNC-12\n"
     "2. Bấm kính lúp, chọn lại phiếu đề nghị là DNTT-15\n"
     "3. Bấm Lưu\n"
     "4. Lọc danh sách theo mã DNTT-15",
     "Phiếu đề nghị mới: DNTT-15",
     "- Bảng chi tiết bị thay hoàn toàn theo DNTT-15\n"
     "- ⚠️ Không có cảnh báo trùng, kết quả là 2 phiếu ủy nhiệm chi cùng trỏ DNTT-15. Ghi nhận và chốt "
     "nghiệp vụ"),

    (4, "Xóa phiếu trong khi người khác đang mở màn Sửa", "P1",
     "Phiếu ủy nhiệm chi UNC-13 ở trạng thái Đang tạo; KT-B đang mở màn Sửa UNC-13",
     "1. KT-C xóa UNC-13 từ danh sách\n"
     "2. KT-B (vẫn đang ở màn Sửa) bấm Lưu\n"
     "3. Đọc thông báo trên màn của KT-B",
     "—",
     "- KT-B nhận thông báo lỗi rõ ràng, không treo trang\n"
     "- Không tạo lại bản ghi đã bị xóa\n"
     "- Ghi nhận nội dung thông báo thực tế để đối chiếu với mong muốn nghiệp vụ"),

    (5, "Duyệt phiếu trong khi phiếu đề nghị đã bị hủy", "P1",
     "Phiếu ủy nhiệm chi UNC-14 ở trạng thái Đang tạo gắn DNTT-16; sau đó DNTT-16 bị chuyển sang trạng "
     "thái Đã hủy",
     "1. Mở Sửa UNC-14, bấm Lưu và duyệt\n"
     "2. Đọc thông báo, kiểm tra trạng thái hai phiếu\n"
     "3. Mở sổ kế toán đối chiếu",
     "—",
     "- Ghi nhận hành vi thực tế: phiếu ủy nhiệm chi có được duyệt không, DNTT-16 có bị ghi đè trạng "
     "thái không, sổ có ghi bút toán không\n"
     "- ⚠️ Đây là ca chốt nghiệp vụ: chi tiền cho một đề nghị đã hủy là rủi ro tiền thật"),

    (6, "Sửa tỷ giá làm sổ kế toán tự mâu thuẫn", "P0",
     "Phiếu đề nghị DNTT-USD loại đô la Mỹ, tỷ giá trên phiếu đề nghị là 24.000; 1 dòng 1.000 đô la Mỹ",
     "1. Tạo phiếu ủy nhiệm chi từ DNTT-USD\n"
     "2. Nhập Tỷ giá là 25.000, đọc cột quy đổi VND\n"
     "3. Bấm Lưu và duyệt\n"
     "4. Mở sổ kế toán, đọc số tiền quy đổi và ô tỷ giá ghi kèm bút toán",
     "Tỷ giá nhập trên phiếu: 25.000 · Tỷ giá của phiếu đề nghị: 24.000",
     "- Cột quy đổi VND trên form hiện 25.000.000\n"
     "- ⚠️ Sổ kế toán ghi số tiền quy đổi 25.000.000 nhưng ô tỷ giá kèm theo lại là 24.000 — bút toán "
     "tự mâu thuẫn, nhân lại không ra số đã ghi. Ghi nhận Failed (mục 9 ghi chú 14)"),

    (7, "Bút toán vế Có lệch với vế Nợ khi phiếu nhiều dòng", "P0",
     "Phiếu đề nghị DNTT-17 loại Chi trả nhà cung cấp, tiền Việt Nam, 3 dòng: 5.000.000, 3.000.000, "
     "2.000.000",
     "1. Tạo phiếu ủy nhiệm chi từ DNTT-17, giữ nguyên Số tiền duyệt chi mặc định\n"
     "2. Bấm Lưu và duyệt\n"
     "3. Mở sổ kế toán, cộng tổng vế Nợ và đọc số của vế Có",
     "Ba dòng: 5.000.000 · 3.000.000 · 2.000.000",
     "- Vế Nợ: 3 bút toán, tổng 10.000.000\n"
     "- ⚠️ Vế Có: CHỈ 2.000.000 (bằng dòng cuối), lệch 8.000.000 so với vế Nợ\n"
     "- Ghi nhận Failed — đây là lỗi số liệu nặng nhất của màn (mục 9 ghi chú 5)"),

    (8, "Bút toán nhân bản theo phiếu yêu cầu xuất hàng", "P0",
     "Phiếu đề nghị DNTT-18 loại Chi trả lại khách hàng, 1 dòng 6.000.000 gắn hợp đồng nguyên tắc có "
     "3 phiếu yêu cầu xuất hàng",
     "1. Tạo phiếu ủy nhiệm chi từ DNTT-18, mở bảng con của dòng chi tiết, ghi lại 3 phiếu xuất\n"
     "2. Bấm Lưu và duyệt\n"
     "3. Mở sổ kế toán, đếm bút toán vế Nợ và cộng tổng",
     "Một dòng 6.000.000 · 3 phiếu yêu cầu xuất hàng",
     "- Mong đợi: tổng vế Nợ bằng 6.000.000, chia theo 3 phiếu xuất\n"
     "- ⚠️ Hiện trạng cần kiểm chứng: có 3 bút toán, MỖI bút toán 6.000.000, tổng 18.000.000 — gấp 3 "
     "lần số tiền thật. Nếu đúng như vậy, ghi nhận Failed (mục 9 ghi chú 6)"),

    (9, "Ghi sổ bỏ qua dòng có số tiền bằng 0", "P1",
     "Phiếu đề nghị DNTT-19 loại Chi thưởng thực hiện hợp đồng, 3 dòng; đặt dòng 2 bằng 0, dòng 1 và "
     "dòng 3 có số tiền",
     "1. Tạo phiếu ủy nhiệm chi từ DNTT-19, đặt dòng 2 bằng 0\n"
     "2. Bấm Lưu và duyệt\n"
     "3. Mở sổ kế toán, đếm bút toán vế Nợ",
     "Dòng 2: 0",
     "- Chỉ có 2 bút toán vế Nợ, cho dòng 1 và dòng 3\n"
     "- Dòng 2 hoàn toàn không xuất hiện trong sổ"),

    (10, "Toàn bộ dòng bằng 0 thì không có vế Có", "P1",
     "Phiếu đề nghị DNTT-20 loại Chi khác, 2 dòng; đặt cả hai dòng bằng 0",
     "1. Tạo phiếu ủy nhiệm chi từ DNTT-20, đặt cả 2 dòng bằng 0\n"
     "2. Bấm Lưu và duyệt\n"
     "3. Mở sổ kế toán tìm bút toán của phiếu này",
     "Cả hai dòng: 0",
     "- ⚠️ KHÔNG có bút toán nào được ghi, kể cả vế Có, trong khi phiếu vẫn chuyển sang Đã hạch toán "
     "và phiếu đề nghị vẫn chuyển sang Duyệt phiếu chi\n"
     "- Ghi nhận và chốt nghiệp vụ: có nên cho duyệt một phiếu 0 đồng không"),
]

# ============================================================ SECTION X
SEC_X = [
    (1, "Luồng đầy đủ: đề nghị thanh toán đến ghi sổ", "P0",
     "Tài khoản NV-A (nhân viên đề nghị), các cấp duyệt đầy đủ, KT-B (Kế toán thanh toán); nhà cung "
     "cấp NCC-01 có sẵn thông tin ngân hàng; hợp đồng HD-01 còn công nợ 10.000.000",
     "1. NV-A lập phiếu đề nghị thanh toán loại Chi trả nhà cung cấp, Hình thức thanh toán CK, gắn "
     "HD-01, số tiền đề nghị 10.000.000, gửi duyệt\n"
     "2. Các cấp duyệt lần lượt cho tới khi phiếu đề nghị sang trạng thái Chờ tạo phiếu chi\n"
     "3. KT-B mở chi tiết phiếu đề nghị, bấm Tạo phiếu ủy nhiệm chi\n"
     "4. Chọn Phương thức thanh toán, Ngân hàng chuyển, Số tài khoản chuyển khoản; giữ nguyên Số tiền "
     "duyệt chi\n"
     "5. Bấm Lưu và duyệt\n"
     "6. Mở lại phiếu đề nghị và sổ kế toán đối chiếu",
     "Số tiền: 10.000.000 · Hình thức thanh toán: CK",
     "- Bước 3: nút Tạo phiếu ủy nhiệm chi hiện đúng (không phải nút Tạo phiếu chi)\n"
     "- Bước 5: thông báo \"Duyệt phiếu ủy nhiệm chi thành công!\", phiếu ở trạng thái Đã hạch toán\n"
     "- Phiếu đề nghị chuyển sang Duyệt phiếu chi, Số tiền duyệt chi cập nhật 10.000.000\n"
     "- Sổ kế toán ghi 10.000.000 cả hai vế, gắn đúng nhà cung cấp NCC-01 và hợp đồng HD-01\n"
     "- Công nợ của HD-01 giảm tương ứng"),

    (2, "Luồng lưu nháp rồi duyệt sau", "P0",
     "Phiếu đề nghị DNTT-21 loại Chi trả nhà cung cấp, chuyển khoản, trạng thái Chờ tạo phiếu chi, 1 "
     "dòng 8.000.000",
     "1. KT-B tạo phiếu ủy nhiệm chi từ DNTT-21, bấm Lưu\n"
     "2. Kiểm tra: phiếu Đang tạo, DNTT-21 vẫn Chờ tạo phiếu chi, sổ chưa có bút toán\n"
     "3. Cùng ngày, mở Sửa phiếu nháp, bấm Lưu và duyệt\n"
     "4. Đối chiếu lại trạng thái hai phiếu và sổ kế toán",
     "Số tiền: 8.000.000",
     "- Bước 2 đúng như mô tả\n"
     "- Bước 4: phiếu Đã hạch toán, DNTT-21 sang Duyệt phiếu chi, sổ ghi 8.000.000 hai vế\n"
     "- Toàn luồng không phát sinh thông báo nào cho ai (mục 9 ghi chú 22)"),

    (3, "Luồng ngoại tệ đầy đủ", "P0",
     "Phiếu đề nghị DNTT-USD2 loại Chi trả nhà cung cấp nước ngoài, đô la Mỹ, tỷ giá 25.000, 1 dòng "
     "2.000 đô la Mỹ, trạng thái Chờ tạo phiếu chi",
     "1. KT-B tạo phiếu ủy nhiệm chi từ DNTT-USD2\n"
     "2. Ghi lại giá trị ô Tỷ giá ngay khi form vừa nạp\n"
     "3. Nhập Tỷ giá 25.000, kiểm tra cột quy đổi VND\n"
     "4. Chọn ngân hàng thụ hưởng và ngân hàng trung gian, chọn Phí\n"
     "5. Bấm Lưu và duyệt, đối chiếu sổ kế toán",
     "Số tiền: 2.000 đô la Mỹ · Tỷ giá: 25.000",
     "- ⚠️ Bước 2: ô Tỷ giá bằng 0, cột quy đổi VND bằng 0 (mục 9 ghi chú 13)\n"
     "- Bước 3: cột quy đổi hiện 50.000.000\n"
     "- Bước 5: phiếu Đã hạch toán, sổ ghi số nguyên tệ 2.000 và số quy đổi 50.000.000\n"
     "- Kiểm chứng thêm ô tỷ giá ghi kèm bút toán có đúng 25.000 hay không (liên quan ca lệch tỷ giá)"),

    (4, "Luồng chi thu nhập nhân viên đầy đủ", "P0",
     "Phòng Kinh doanh 1 có 6 nhân viên, trong đó 3 người có số dư các khoản thu nhập",
     "1. KT-B bấm Tạo mới, chọn Loại chi là Chi thu nhập cho nhân viên\n"
     "2. Nhập Người nhận tiền, chọn Phòng ban Kinh doanh 1, nhập Lý do chi\n"
     "3. Bấm Lấy nhân viên, bỏ tick 3 người không có số dư\n"
     "4. Nhập Số tiền chi cho 3 người còn lại, kiểm tra thẻ Chi tiết vụ việc khớp\n"
     "5. Chọn Ngân hàng chuyển và Số tài khoản chuyển khoản, bấm Lưu và duyệt\n"
     "6. Mở danh sách và sổ kế toán đối chiếu",
     "Phòng ban: Kinh doanh 1 · Số nhân viên chi: 3",
     "- Phiếu tạo thành công, trạng thái Đã hạch toán\n"
     "- Danh sách: cột Loại chi hiện Chi thu nhập cho nhân viên, cột Mã phiếu đề nghị chi và cột Người "
     "đề nghị để trống\n"
     "- Chi tiết phiếu chỉ có 3 dòng đúng 3 nhân viên đã tick\n"
     "- Sổ kế toán tách bút toán theo từng mã vụ việc, gắn đúng nhân viên và phòng ban chi\n"
     "- ⚠️ Phiếu này chỉ hiện ở chế độ Tất cả với người có quyền xem của tổng công ty (mục 9 ghi "
     "chú 9)"),

    (5, "Luồng hủy phiếu và lập lại", "P1",
     "Phiếu ủy nhiệm chi đã ép sang trạng thái Chờ duyệt, gắn phiếu đề nghị DNTT-22 đang ở Chờ tạo "
     "phiếu chi; TQ-F có quyền Thủ quỹ duyệt phiếu chi",
     "1. TQ-F nhập Ghi chú lý do, bấm Hủy phiếu ủy nhiệm chi, xác nhận\n"
     "2. Kiểm tra trạng thái hai phiếu\n"
     "3. KT-B mở lại DNTT-22, bấm Tạo phiếu ủy nhiệm chi lần nữa\n"
     "4. Lưu và duyệt phiếu mới, đối chiếu sổ kế toán",
     "—",
     "- Phiếu cũ ở trạng thái Hủy, DNTT-22 vẫn ở Chờ tạo phiếu chi nên lập lại được\n"
     "- Phiếu mới ghi sổ bình thường\n"
     "- Sổ KHÔNG có bút toán nào của phiếu đã hủy"),

    (6, "Đối chiếu tổng thể sau một ngày làm việc", "P0",
     "Trong ngày đã lập 10 phiếu ủy nhiệm chi: 6 phiếu 1 dòng, 3 phiếu nhiều dòng, 1 phiếu chi thu "
     "nhập nhân viên; tất cả đã duyệt",
     "1. Mở danh sách, lọc Trạng thái là Đã hạch toán\n"
     "2. Mở lần lượt từng phiếu, ghi lại dòng Tổng cộng\n"
     "3. Cộng tổng 10 phiếu\n"
     "4. Mở sổ kế toán, cộng tổng vế Nợ và tổng vế Có của 10 phiếu đó\n"
     "5. So ba con số",
     "10 phiếu đã duyệt trong ngày",
     "- Tổng theo phiếu và tổng vế Nợ khớp nhau\n"
     "- ⚠️ Tổng vế Có NHỎ HƠN vì 3 phiếu nhiều dòng chỉ ghi số của dòng cuối. Ghi nhận Failed và báo "
     "số chênh lệch cụ thể (mục 9 ghi chú 5)\n"
     "- Đây là ca chốt để đánh giá mức độ ảnh hưởng tới sổ sách"),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", SEC_III),
    ("IV", "TẠO MỚI / SỬA / XEM CHI TIẾT", SEC_IV),
    ("V", "DUYỆT & HỦY PHIẾU ỦY NHIỆM CHI", SEC_V),
    ("VI", "XÓA", SEC_VI),
    ("VII", "CHI THU NHẬP CHO NHÂN VIÊN", SEC_VII),
    ("VIII", "RÀNG BUỘC NHẬP LIỆU", SEC_VIII),
    ("IX", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", SEC_IX),
    ("X", "LUỒNG NGHIỆP VỤ ĐẦU - CUỐI", SEC_X),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Phiếu ủy nhiệm chi (ERP) - Cập nhật ngày 21/08/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )
