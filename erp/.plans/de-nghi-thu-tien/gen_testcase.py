# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Phieu de nghi thu tien" (admin/income-expenditure/bill_income_requests).

Form mau: 17 cot (bang dung chuan `.plans/gop-db/banks-cut-mysql2/testcase.xlsx`), dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

⚠️ Tai lieu nay viet theo LOGIC ERP dang chay tren nhanh gop_db (repo D:/laragon/www/erp),
KHONG phai ban da port sang HRM.

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :6509-6523
  app/Http/Controllers/IncomeExpenditure/BillIncomeRequestController.php
  app/Model/IncomeExpenditure/BillIncomeRequest.php (+ BillIncomeRequestDetail.php)
  app/Http/Requests/IncomeExpenditure/BillIncomeRequest/*.php
  app/Model/Accounting/AccountDetail.php :1746 (getDebtAfterIncomeMoney)
  app/Contract.php :926 (getDataForBillIncomeRequest)
  app/Services/Contracts/SearchContractService.php :175-180, :273-283, :468-478
  app/Helpers/NotificationHelper.php :40 (sendNotifyWithPermission)
  resources/views/income_expenditure/bill_income_requests/*.blade.php
  resources/views/partials/classes/IncomeExpenditure/BillIncomeRequest*.blade.php
  resources/views/partials/classes/base/Datatable.blade.php
  resources/views/partials/confirm.blade.php
  resources/views/layouts/topmenubar.blade.php :418, :1013, :2155

Chay:  python .plans/de-nghi-thu-tien/gen_testcase.py
"""
import os
import sys

try:  # console Windows mac dinh cp1252
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

# .plans/de-nghi-thu-tien -> .plans -> erp -> hrm-claude-config -> hrm/.claude/skills/...
sys.path.insert(0, os.path.join(
    HERE, "..", "..", "..", "hrm", ".claude", "skills", "testcase-documenter", "assets"))

from tc_engine import build  # noqa: E402

OUT = os.path.join(HERE, "testcase.xlsx")

MODULE = "Đề nghị thu tiền"

# ============================================================ 9 MUC MO TA
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Quản lý Phiếu đề nghị thu tiền: chứng từ do người kinh doanh lập để đề nghị kế toán thu tiền "
     "theo một hoặc nhiều hợp đồng, thuộc nhóm Công nợ - Thu - Chi.\n"
     "Người dùng làm được: xem danh sách, lọc, tạo phiếu (Lưu nháp hoặc Lưu và gửi duyệt), sửa, xóa, "
     "xem chi tiết và in phiếu.\n"
     "Kế toán thanh toán có màn riêng \"Phiếu đề nghị thu tiền chờ duyệt\" với 2 lựa chọn xử lý: "
     "\"Tạo phiếu thu\" (đồng ý, chuyển sang màn Phiếu thu) hoặc \"Không duyệt\" (từ chối, bắt buộc "
     "nhập Ghi chú duyệt).\n"
     "Màn hình có 4 chế độ danh sách khác nhau dùng chung một bảng dữ liệu — xem mục 5."),

    ("2. Đối tượng được tính / hiển thị",
     "Phiếu hiển thị đủ 6 trạng thái: Đang tạo · Chờ KT duyệt · Đã tạo phiếu thu · Đã hạch toán · Hủy · "
     "Không duyệt. Nhãn Đã tạo phiếu thu và Đã hạch toán tô XANH, bốn nhãn còn lại tô ĐỎ.\n"
     "Phạm vi phiếu nhìn thấy phụ thuộc chế độ danh sách đang mở:\n"
     "- Chế độ \"Phiếu của tôi\" (vào thẳng đường dẫn không kèm tham số): chỉ phiếu do chính mình lập, "
     "gồm cả phiếu nháp của mình.\n"
     "- Chế độ \"Tất cả\" (mục menu Đề nghị thu tiền trỏ vào đây): lấy theo 4 quyền xem ở mục 7, và "
     "luôn ẩn phiếu nháp của người khác.\n"
     "- Chế độ \"Chờ duyệt\" (mục menu Phiếu đề nghị thu tiền chờ duyệt): phiếu trạng thái Chờ KT duyệt "
     "thuộc công ty của người đăng nhập, KHÔNG áp thêm 4 quyền xem theo cấp.\n"
     "- Chế độ \"Đã xử lý\": phiếu mà chính người đăng nhập là người đã duyệt / không duyệt. Chế độ này "
     "KHÔNG có mục menu nào trỏ tới, chỉ vào được bằng đường dẫn trực tiếp.\n"
     "Hai chế độ Chờ duyệt và Đã xử lý có thêm cột \"Người nộp\" so với hai chế độ còn lại."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu nháp (Đang tạo) của NGƯỜI KHÁC bị ẩn ở chế độ \"Tất cả\". Ở chế độ \"Chờ duyệt\" thì "
     "không có phép ẩn này, chỉ nhờ điều kiện trạng thái Chờ KT duyệt mà nháp không lọt vào.\n"
     "- Nút Sửa và nút Xóa chỉ hiện khi phiếu ở trạng thái Đang tạo hoặc Không duyệt. ⚠️ Hệ thống "
     "KHÔNG xét người lập: phiếu Không duyệt của người khác mà mình nhìn thấy thì vẫn hiện đủ 2 nút này.\n"
     "- Nút \"Tạo phiếu thu\" chỉ hiện khi phiếu ở Chờ KT duyệt VÀ người đăng nhập có quyền "
     "\"Kế toán thanh toán\".\n"
     "- Nút \"In\" luôn hiện cho mọi dòng, mọi trạng thái.\n"
     "- Nút \"Tạo mới\" chỉ có ở chế độ \"Phiếu của tôi\" và \"Tất cả\"; hai chế độ Chờ duyệt và Đã xử "
     "lý KHÔNG có nút này.\n"
     "- Ô lọc Trạng thái chỉ có ở chế độ \"Phiếu của tôi\" và \"Tất cả\".\n"
     "- Ba ô lọc Công ty / Phòng ban / Bộ phận chỉ hiện ở chế độ \"Tất cả\" và chỉ với người có quyền "
     "xem theo cấp tương ứng.\n"
     "- Ô chọn Loại thu chỉ có 2 lựa chọn Thu bán hàng và Thu nhà cung cấp; giá trị \"Thu khác\" chỉ "
     "dùng để hiển thị phiếu cũ, không lập mới được.\n"
     "- Nhánh Hợp đồng nguyên tắc (ô tích \"Thu dư nợ đầu kỳ\" + bảng phân bổ theo phiếu yêu cầu xuất "
     "hàng) KHÔNG kích hoạt được khi tạo phiếu mới vì hệ thống không nhận diện loại hợp đồng lúc chọn — "
     "xem mục 9.\n"
     "- Màn hình KHÔNG có chức năng Xuất Excel và Nhập Excel."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Hai ô \"Từ ngày\" và \"Đến ngày\" lọc theo NGÀY LẬP PHIẾU.\n"
     "⚠️ Hai đầu mút KHÔNG được tính trọn ngày: hệ thống so sánh với mốc 0 giờ của ngày nhập vào, nên "
     "phiếu lập trong chính ngày điền ở ô \"Đến ngày\" sẽ bị loại khỏi kết quả, và phiếu lập đúng 0 giờ "
     "của ngày điền ở ô \"Từ ngày\" cũng bị loại. Đây là bẫy đối chiếu số liệu, xem mục 9.\n"
     "Không có bộ lọc theo ngày cập nhật."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Hai cấp: Phiếu → Dòng chi tiết.\n"
     "- Phiếu giữ: Mã phiếu, Loại thu, Loại tiền, Tỷ giá, Lý do thu, Ghi chú duyệt, Trạng thái, Người "
     "tạo, Phòng ban, Công ty, Bộ phận.\n"
     "- Mỗi dòng chi tiết gắn một Khách hàng (hoặc Nhà cung cấp) và một hợp đồng: Khách hàng / Nhà cung "
     "cấp · Số đơn hàng - Hợp đồng · Số tiền còn nợ · Số tiền đề nghị thu · Ghi chú.\n"
     "- Khách hàng chọn theo TỪNG DÒNG, nên một phiếu gom được nhiều khách hàng khác nhau.\n"
     "- Mã phiếu sinh tự động: mã công ty + \".DNTT\" + tháng năm (4 số) + \".\" + 5 chữ số tăng dần, "
     "ví dụ TPE.DNTT0826.00017. Không sửa tay được.\n"
     "- Công ty / Phòng ban / Bộ phận của phiếu lấy từ hồ sơ nhân sự của người lập tại thời điểm tạo "
     "phiếu, và không đổi về sau.\n"
     "- Bốn chế độ danh sách (Phiếu của tôi · Tất cả · Chờ duyệt · Đã xử lý) là 4 đường dẫn khác nhau "
     "nhưng dùng CHUNG một nguồn dữ liệu và chung bộ lọc; khác nhau ở phạm vi lọc, ở cột Người nộp và "
     "ở bộ nút phía trên bảng.\n"
     "- Mỗi lần lưu, toàn bộ dòng chi tiết cũ bị xóa và ghi lại từ đầu."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Cột \"Số tiền\" ngoài danh sách = TỔNG cột Số tiền đề nghị thu ĐÃ QUY ĐỔI VND của mọi dòng chi "
     "tiết trong phiếu, hiển thị có 2 chữ số thập phân.\n"
     "- Trong form: cột quy đổi VND của mỗi dòng = Số tiền đề nghị thu × Tỷ giá. Dòng \"Tổng cộng\" "
     "cuối bảng cộng dồn 3 cột: Số tiền còn nợ, Số tiền đề nghị thu, và cột quy đổi VND (nếu có).\n"
     "- Hai ô lọc \"Số tiền đề nghị thu từ - đến\" so với TỔNG QUY ĐỔI VND của cả phiếu, không so từng "
     "dòng.\n"
     "- Cột \"Khách hàng/Nhà cung cấp\" ngoài danh sách chỉ lấy đối tượng của DÒNG ĐẦU TIÊN; phiếu gom "
     "nhiều khách hàng vẫn chỉ hiện một tên.\n"
     "- Không cho chọn TRÙNG một hợp đồng ở hai dòng trong cùng một phiếu: chọn lại thì hệ thống báo "
     "\"Hợp đồng đã tồn tại!\".\n"
     "- Một phiếu khớp nhiều điều kiện lọc vẫn chỉ hiện một dòng."),

    ("7. Phân quyền cấp",
     "Năm quyền liên quan tới màn hình này:\n"
     "1. \"Xem tất cả phiếu đề nghị thu của tổng công ty\" — thấy phiếu của mọi công ty; bộ lọc hiện "
     "thêm ô Công ty và ô Phòng ban.\n"
     "2. \"Xem tất cả phiếu đề nghị thu của công ty\" — chỉ phiếu công ty mình; bộ lọc hiện ô Phòng ban.\n"
     "3. \"Xem tất cả phiếu đề nghị thu của phòng ban\" — chỉ phiếu thuộc các phòng ban mình được phân "
     "công quản lý trong công ty mình; bộ lọc hiện ô Phòng ban và ô Bộ phận.\n"
     "4. \"Xem tất cả phiếu đề nghị thu của bộ phận\" — chỉ phiếu thuộc các bộ phận mình được phân công "
     "quản lý trong công ty mình.\n"
     "5. \"Kế toán thanh toán\" — thấy mục menu và vào được màn Phiếu đề nghị thu tiền chờ duyệt, được "
     "nhập Ghi chú duyệt, bấm Không duyệt và bấm Tạo phiếu thu.\n"
     "Bốn quyền xem xét theo THỨ TỰ TRÊN XUỐNG, ai có quyền cao hơn thì lấy phạm vi rộng hơn; ai không "
     "có quyền nào trong bốn quyền trên thì chỉ thấy phiếu do chính mình lập.\n"
     "Tài khoản có vai trò Super Admin luôn mở được chi tiết mọi phiếu.\n"
     "⚠️ Chỉ DUY NHẤT đường dẫn màn chờ duyệt được hệ thống chặn bằng quyền \"Kế toán thanh toán\". "
     "Các chức năng còn lại — xem danh sách, tạo, sửa, xóa, in, đổi trạng thái — KHÔNG gắn quyền ở phía "
     "hệ thống, chỉ ẩn / hiện nút trên giao diện. Đây là hiện trạng của mã nguồn, nhóm test bỏ qua giao "
     "diện (mục IX và các ca TC-ROLE cuối) dựng riêng để đo mức độ rủi ro này."),

    ("8. Cách tính các ô thống kê",
     "- Ô \"Hiển thị a đến b trong tổng số N\" dưới bảng: a là dòng đầu trang đang xem, b là dòng cuối, "
     "N là tổng số phiếu khớp bộ lọc trong phạm vi chế độ đang mở.\n"
     "- Ô \"Số dòng mỗi trang\": mặc định 10; đổi số dòng thì bảng quay về trang 1.\n"
     "- Cột STT đánh liên tục theo trang: trang 2 với 10 dòng mỗi trang bắt đầu từ 11.\n"
     "- Cột \"Số tiền\": xem công thức ở mục 6, luôn hiện 2 chữ số thập phân (ví dụ 15.000.000,00).\n"
     "- Cột \"Số tiền còn nợ\" (trong form, trong cửa sổ chọn hợp đồng và trên bản in): lấy từ sổ kế "
     "toán của chính hợp đồng đó — tổng phát sinh bên Nợ trừ tổng phát sinh bên Có, trên tài khoản Phải "
     "thu khách hàng (Thu bán hàng) hoặc tài khoản Phải trả nhà cung cấp (Thu nhà cung cấp). Số này "
     "TÍNH LẠI mỗi lần mở phiếu và mỗi lần in, KHÔNG lưu trong phiếu.\n"
     "- Bản in có dòng \"Tổng cộng\" (cộng Số tiền còn nợ và Số tiền đề nghị thu) và dòng \"Bằng chữ\" "
     "đọc theo tổng tiền đã quy đổi VND.\n"
     "- Cột \"Ngày lập\" hiển thị dạng ngày/tháng/năm, không có giờ."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất của màn này — đọc trước khi chạy test:\n"
     "1. ⚠️ Cửa sổ chọn hợp đồng của phiếu Thu bán hàng CHỈ hiện hợp đồng do CHÍNH NGƯỜI ĐANG ĐĂNG NHẬP "
     "lập. Không thấy hợp đồng của khách hàng vừa chọn thường là do hợp đồng đó của người khác chứ "
     "không phải lỗi. Cửa sổ chọn hợp đồng MUA (Thu nhà cung cấp) thì KHÔNG lọc theo người lập.\n"
     "2. ⚠️ Sau khi bấm Lưu ở màn SỬA, hệ thống chuyển thẳng sang màn \"Phiếu đề nghị thu tiền chờ "
     "duyệt\". Người không có quyền \"Kế toán thanh toán\" sẽ bị chặn ngay sau khi lưu thành công — "
     "phiếu ĐÃ lưu nhưng màn hình báo không có quyền. Ghi nhận Failed và ghi rõ phiếu vẫn lưu được.\n"
     "3. ⚠️ Ô lọc \"Người nộp\" không có tác dụng: gõ gì vào cũng ra nguyên kết quả cũ. Ngoài ra form "
     "nhập KHÔNG có ô Người nộp nên cột này luôn trống với phiếu lập từ màn này.\n"
     "4. ⚠️ Ô \"Đến ngày\" làm rụng trọn ngày cuối (xem mục 4). Khi đối chiếu số liệu phải cộng bù.\n"
     "5. ⚠️ Nút Sửa / Xóa hiện theo TRẠNG THÁI, không xét người lập. Phiếu Không duyệt của người khác "
     "mà mình nhìn thấy thì mình sửa và xóa được.\n"
     "6. ⚠️ Xóa phiếu: hệ thống không kiểm tra quyền và không kiểm tra trạng thái. Dán thẳng đường dẫn "
     "xóa của một phiếu bất kỳ (kể cả Đã hạch toán, kể cả của người khác) là phiếu bị xóa. Đây là lỗ "
     "hổng, ghi nhận Failed.\n"
     "7. ⚠️ Tỷ giá in trên bản in ngoại tệ lấy từ DANH MỤC tiền tệ ở thời điểm in, KHÔNG phải tỷ giá đã "
     "lưu trong phiếu. Phiếu cũ in lại sau khi danh mục đổi tỷ giá sẽ ra số khác với số trong phiếu.\n"
     "8. ⚠️ Số tiền còn nợ trên bản in và trên màn chi tiết được tính lại theo sổ kế toán tại thời điểm "
     "mở, nên có thể khác con số nhìn thấy lúc lập phiếu. Không phải lỗi.\n"
     "9. ⚠️ Đổi Loại thu sẽ XÓA SẠCH các dòng chi tiết đã nhập và KHÔNG hỏi xác nhận.\n"
     "10. ⚠️ Nhánh Hợp đồng nguyên tắc (ô tích \"Thu dư nợ đầu kỳ\" và bảng phân bổ phiếu yêu cầu xuất "
     "hàng) không hiện ra khi tạo phiếu mới, kể cả khi chọn đúng hợp đồng nguyên tắc — hệ thống không "
     "gán loại hợp đồng cho dòng vừa chọn. Nhánh này chỉ thấy ở phiếu cũ. Ghi nhận là hiện trạng đã biết.\n"
     "11. ⚠️ Bấm Không duyệt khi ô \"Ghi chú duyệt\" đang trống thì hệ thống chặn; nhưng hộp thoại xác "
     "nhận vẫn hiện ra trước rồi mới báo lỗi. Kiểm cả 2 bước.\n"
     "12. Bộ lọc được hệ thống ghi nhớ RIÊNG cho từng chế độ danh sách; rời màn rồi quay lại vẫn còn "
     "điều kiện lọc cũ — test xong nhớ bấm nút làm mới bộ lọc trước khi sang ca test khác.\n"
     "13. Số liệu tham chiếu của môi trường test khi viết tài liệu: khoảng 2.413 phiếu trong kho dữ "
     "liệu; gần một nửa số phiếu có từ 2 khách hàng trở lên, cao nhất 25 khách hàng trong một phiếu."),
]

# ============================================================ TC PHAN QUYEN
ROLE_TCS = [
    ("00", "Tài khoản không có quyền xem nào chỉ thấy phiếu do chính mình lập", "P0",
     "Tài khoản NV-A không được gán quyền nào trong 4 quyền xem theo cấp; NV-A đã lập 30 phiếu; công ty "
     "của NV-A có hơn 300 phiếu của nhiều người",
     "1. Đăng nhập bằng NV-A\n"
     "2. Mở menu Công nợ - Thu - Chi, bấm mục Đề nghị thu tiền\n"
     "3. Đọc số tổng dưới bảng\n"
     "4. Lật hết các trang, soát cột Người lập",
     "Tài khoản: NV-A (không quyền xem theo cấp)",
     "- Vào được màn hình, không bị chặn\n"
     "- Tổng hiện đúng 30\n"
     "- Mọi dòng đều có Người lập là NV-A\n"
     "- Nút Tạo mới VẪN hiển thị (hành vi tạo phiếu không gắn quyền — xem mục 7)"),

    ("01", "Quyền xem của tổng công ty thấy phiếu của mọi công ty", "P0",
     "Tài khoản B chỉ có quyền \"Xem tất cả phiếu đề nghị thu của tổng công ty\"; hệ thống có phiếu của "
     "ít nhất 3 công ty",
     "1. Đăng nhập bằng B, mở mục Đề nghị thu tiền trên menu\n"
     "2. Bấm nút Bộ lọc để bung khối tìm kiếm\n"
     "3. Ghi lại các ô lọc theo đơn vị đang hiện\n"
     "4. Chọn lần lượt từng Công ty rồi bấm nút tìm kiếm",
     "Quyền: Xem tất cả phiếu đề nghị thu của tổng công ty",
     "- Khối lọc hiện CẢ ô Công ty và ô Phòng ban\n"
     "- Chọn công ty nào ra phiếu của công ty đó\n"
     "- Bỏ chọn công ty thì thấy phiếu của cả 3 công ty"),

    ("02", "Quyền xem của công ty chỉ thấy phiếu công ty mình", "P0",
     "Tài khoản C chỉ có quyền \"Xem tất cả phiếu đề nghị thu của công ty\", thuộc công ty 3; công ty 3 "
     "có 120 phiếu, công ty 1 có 800 phiếu",
     "1. Đăng nhập bằng C, mở mục Đề nghị thu tiền\n"
     "2. Bấm nút Bộ lọc, ghi lại các ô lọc theo đơn vị\n"
     "3. Đọc số tổng và soát cột Phòng ban",
     "Quyền: Xem tất cả phiếu đề nghị thu của công ty",
     "- Khối lọc KHÔNG có ô Công ty, chỉ có ô Phòng ban\n"
     "- Tổng bằng 120 trừ đi số phiếu nháp của người khác trong công ty 3\n"
     "- Không có phiếu nào của công ty 1"),

    ("03", "Quyền xem của phòng ban chỉ thấy phiếu phòng ban mình quản lý", "P0",
     "Tài khoản D chỉ có quyền \"Xem tất cả phiếu đề nghị thu của phòng ban\", được phân công quản lý "
     "đúng 2 phòng ban trong công ty mình; 2 phòng ban đó có 25 phiếu",
     "1. Đăng nhập bằng D, mở mục Đề nghị thu tiền\n"
     "2. Bấm nút Bộ lọc, ghi lại các ô lọc theo đơn vị\n"
     "3. Soát cột Phòng ban của mọi dòng qua tất cả các trang",
     "Quyền: Xem tất cả phiếu đề nghị thu của phòng ban",
     "- Khối lọc hiện ô Phòng ban và ô Bộ phận\n"
     "- Ô Phòng ban CHỈ liệt kê 2 phòng ban D được phân công, không liệt kê phòng ban khác\n"
     "- Chỉ hiện phiếu thuộc 2 phòng ban đó, cộng phiếu nháp của chính D"),

    ("04", "Quyền xem của bộ phận chỉ thấy phiếu bộ phận mình quản lý", "P1",
     "Tài khoản E chỉ có quyền \"Xem tất cả phiếu đề nghị thu của bộ phận\", quản lý 1 bộ phận trong "
     "công ty mình",
     "1. Đăng nhập bằng E, mở mục Đề nghị thu tiền\n"
     "2. Đọc số tổng và soát danh sách\n"
     "3. Bấm nút Bộ lọc, quan sát các ô lọc theo đơn vị",
     "Quyền: Xem tất cả phiếu đề nghị thu của bộ phận",
     "- Chỉ hiện phiếu thuộc đúng bộ phận được phân công, cộng phiếu nháp của chính E\n"
     "- ⚠️ Khối lọc KHÔNG hiện ô Công ty / Phòng ban / Bộ phận cho mức quyền này — ghi nhận đúng hiện "
     "trạng, không suy đoán"),

    ("05", "Có nhiều quyền cùng lúc thì lấy phạm vi rộng nhất", "P1",
     "Tài khoản F có ĐỒNG THỜI quyền \"Xem tất cả phiếu đề nghị thu của tổng công ty\" và \"Xem tất cả "
     "phiếu đề nghị thu của bộ phận\"",
     "1. Đăng nhập bằng F, mở mục Đề nghị thu tiền\n"
     "2. Đọc số tổng, so với số của tài khoản B ở TC-ROLE-01",
     "Quyền: tổng công ty + bộ phận",
     "- Tổng bằng đúng số của tài khoản chỉ có quyền tổng công ty\n"
     "- Không bị thu hẹp về phạm vi bộ phận"),

    ("06", "Kế toán thanh toán vào được màn chờ duyệt", "P0",
     "Tài khoản KT-1 có quyền \"Kế toán thanh toán\", thuộc công ty 3; công ty 3 có 4 phiếu Chờ KT "
     "duyệt, công ty 1 có 17 phiếu Chờ KT duyệt",
     "1. Đăng nhập bằng KT-1\n"
     "2. Mở nhóm menu Công nợ - Thu - Chi ở khu vực phê duyệt\n"
     "3. Bấm mục Phiếu đề nghị thu tiền chờ duyệt\n"
     "4. Đọc số tổng, cột Trạng thái và bộ nút phía trên bảng",
     "Quyền: Kế toán thanh toán",
     "- Mục menu HIỂN THỊ\n"
     "- Vào được màn, đúng 4 dòng, tất cả đều là Chờ KT duyệt của công ty 3\n"
     "- KHÔNG thấy 17 phiếu của công ty 1\n"
     "- Phía trên bảng chỉ có nút Bộ lọc, KHÔNG có nút Tạo mới\n"
     "- Bảng có thêm cột \"Người nộp\" so với màn danh sách thường"),

    ("07", "Không có quyền Kế toán thanh toán thì bị chặn ở màn chờ duyệt", "P0",
     "Tài khoản NV-A ở TC-ROLE-00, không có quyền \"Kế toán thanh toán\"",
     "1. Đăng nhập bằng NV-A\n"
     "2. Mở nhóm menu phê duyệt, tìm mục Phiếu đề nghị thu tiền chờ duyệt\n"
     "3. Dán thẳng đường dẫn màn chờ duyệt vào thanh địa chỉ",
     "Đường dẫn màn chờ duyệt",
     "- Mục menu KHÔNG hiển thị\n"
     "- Dán thẳng đường dẫn: hệ thống từ chối, báo không có quyền, không hiện dữ liệu phiếu nào"),

    ("08", "Kế toán thấy phiếu chờ duyệt của cả công ty dù không có quyền xem theo cấp", "P0",
     "Tài khoản KT-2 chỉ có quyền \"Kế toán thanh toán\", KHÔNG có quyền xem theo cấp nào; công ty của "
     "KT-2 có 4 phiếu Chờ KT duyệt của 4 người khác nhau",
     "1. Đăng nhập bằng KT-2, mở mục Đề nghị thu tiền trên menu, đọc số tổng\n"
     "2. Mở màn Phiếu đề nghị thu tiền chờ duyệt, đọc số tổng",
     "—",
     "- Màn danh sách thường: chỉ thấy phiếu do chính KT-2 lập\n"
     "- Màn chờ duyệt: thấy đủ 4 phiếu của 4 người khác\n"
     "- ⚠️ Đúng thiết kế — màn chờ duyệt chỉ lọc theo công ty, không áp 4 quyền xem theo cấp"),

    ("09", "Phiếu nháp của người khác bị ẩn ở chế độ Tất cả", "P0",
     "Tài khoản B có quyền xem tổng công ty; NV-A vừa Lưu nháp 1 phiếu mã kết thúc .00031",
     "1. Đăng nhập bằng B, mở mục Đề nghị thu tiền trên menu\n"
     "2. Bấm Bộ lọc, gõ .00031 vào ô Mã phiếu, bấm nút tìm kiếm\n"
     "3. Xóa ô mã, chọn Trạng thái = Đang tạo, tìm lại",
     "Mã phiếu nháp của NV-A kết thúc .00031",
     "- Tìm theo mã: không ra dòng nào\n"
     "- Lọc Đang tạo: chỉ ra phiếu nháp của chính B\n"
     "- ⚠️ Quy tắc cố định, KHÔNG ghi Failed"),

    ("10", "Mở chi tiết phiếu ngoài phạm vi quyền bị chặn", "P0",
     "Tài khoản NV-A (không quyền xem theo cấp); lấy đường dẫn chi tiết của 1 phiếu do người khác lập, "
     "trạng thái Đã hạch toán",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dán đường dẫn chi tiết phiếu người khác vào thanh địa chỉ",
     "Phiếu người khác, trạng thái Đã hạch toán",
     "- Hệ thống hiện trang báo không tìm thấy nội dung\n"
     "- Không hiển thị bất kỳ dữ liệu nào của phiếu"),

    ("11", "Người đã xử lý phiếu vẫn xem lại được phiếu đó", "P1",
     "Tài khoản KT-1 đã từng bấm Không duyệt 1 phiếu của người khác; KT-1 không có quyền xem theo cấp nào",
     "1. Đăng nhập bằng KT-1\n"
     "2. Dán thẳng đường dẫn chi tiết phiếu đã từng không duyệt\n"
     "3. Mở chế độ danh sách \"Đã xử lý\" bằng đường dẫn trực tiếp",
     "Phiếu trạng thái Không duyệt, do người khác lập",
     "- Mở được màn chi tiết bình thường\n"
     "- Chế độ \"Đã xử lý\" liệt kê đúng những phiếu KT-1 đã xử lý"),

    ("12", "Bỏ qua giao diện gọi thẳng chức năng Xóa phiếu của người khác", "P0",
     "Tài khoản NV-A; lấy đường dẫn xóa của 1 phiếu trạng thái Đã hạch toán do người khác lập",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dán thẳng đường dẫn xóa của phiếu đó vào thanh địa chỉ\n"
     "3. Kiểm tra phiếu còn hay mất",
     "Phiếu Đã hạch toán của người khác",
     "- ⚠️ Hiện trạng: phiếu BỊ XÓA, hệ thống báo xóa thành công. Đây là LỖ HỔNG nghiêm trọng — hệ "
     "thống không kiểm tra quyền và không kiểm tra trạng thái khi xóa. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: hệ thống phải từ chối và giữ nguyên phiếu\n"
     "- Sau khi test xong phải khôi phục dữ liệu"),

    ("13", "Bỏ qua giao diện gọi thẳng chức năng Sửa phiếu của người khác", "P0",
     "Tài khoản NV-A; 1 phiếu trạng thái Đã hạch toán do người khác lập",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dán thẳng đường dẫn màn Sửa của phiếu đó\n"
     "3. Nếu mở được, sửa Lý do thu rồi bấm Lưu\n"
     "4. Kiểm tra lại nội dung phiếu",
     "Phiếu Đã hạch toán của người khác",
     "- ⚠️ Hiện trạng: màn Sửa MỞ ĐƯỢC và lưu được đè lên phiếu. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: hệ thống phải từ chối ngay khi mở màn Sửa"),

    ("14", "Bỏ qua giao diện đổi trạng thái phiếu khi không phải kế toán", "P0",
     "Tài khoản NV-A không có quyền \"Kế toán thanh toán\"; 1 phiếu đang Chờ KT duyệt",
     "1. Đăng nhập bằng NV-A, lấy phiên đăng nhập\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng đổi trạng thái phiếu, gửi trạng thái Không duyệt "
     "kèm ghi chú bất kỳ\n"
     "3. Gọi lần nữa, lần này gửi trạng thái Đã hạch toán\n"
     "4. Mở lại phiếu, đọc Trạng thái",
     "Trạng thái gửi lên: Không duyệt, rồi Đã hạch toán",
     "- ⚠️ Hiện trạng: cả 2 lần đều thành công, phiếu bị đẩy sang trạng thái gửi lên. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: từ chối vì không có quyền, và chỉ cho chuyển sang Không duyệt\n"
     "- Nhóm test này dành cho tester kỹ thuật"),

    ("15", "Bỏ qua giao diện lấy dữ liệu danh sách theo chế độ chờ duyệt", "P1",
     "Tài khoản NV-A không có quyền \"Kế toán thanh toán\"; công ty của NV-A có phiếu nháp của nhiều người",
     "1. Đăng nhập bằng NV-A, lấy phiên đăng nhập\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng nguồn dữ liệu của bảng danh sách, đặt chế độ là chờ duyệt "
     "và KHÔNG truyền điều kiện trạng thái\n"
     "3. Đọc kết quả trả về",
     "Chế độ: chờ duyệt, không truyền trạng thái",
     "- ⚠️ Hiện trạng: trả về TẤT CẢ phiếu của công ty, gồm cả phiếu nháp của người khác, dù NV-A không "
     "có quyền gì. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: chặn bằng quyền \"Kế toán thanh toán\" như đường dẫn màn chờ duyệt"),

    ("16", "In phiếu của người khác không bị chặn", "P1",
     "Tài khoản NV-A; lấy đường dẫn in của 1 phiếu do người khác lập ở công ty khác",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dán thẳng đường dẫn in của phiếu đó",
     "Phiếu công ty khác",
     "- ⚠️ Hiện trạng: bản in hiện ra đầy đủ nội dung phiếu. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: kiểm tra quyền xem trước khi cho in, như màn chi tiết"),
]

# ============================================================ SECTIONS
SEC_I = [
    ("001", "Vào màn từ mục menu Công nợ - Thu - Chi", "P0",
     "Tài khoản bất kỳ đã đăng nhập",
     "1. Mở menu trên cùng, vào nhóm Công nợ - Thu - Chi\n"
     "2. Bấm mục Đề nghị thu tiền\n"
     "3. Quan sát tiêu đề trang và bảng",
     "—",
     "- Mở đúng màn Danh sách phiếu đề nghị thu tiền\n"
     "- Bảng nạp dữ liệu, không báo lỗi\n"
     "- Đây là chế độ \"Tất cả\": phạm vi phiếu theo quyền xem của người đăng nhập"),

    ("002", "Vào màn từ lối vào thứ hai trong nhóm Đề nghị", "P1",
     "Vẫn tài khoản ở TC_01.001",
     "1. Mở menu, vào nhóm chứa mục \"Đề nghị\"\n"
     "2. Bấm mục Đề nghị thu tiền\n"
     "3. So với kết quả của TC_01.001",
     "—",
     "- Mở đúng cùng một màn, cùng chế độ, cùng số tổng\n"
     "- Không mở nhầm màn khác"),

    ("003", "Chế độ Phiếu của tôi khác chế độ Tất cả", "P0",
     "Tài khoản C có quyền xem theo công ty; công ty có 120 phiếu, C tự lập 12 phiếu",
     "1. Vào màn bằng mục menu (chế độ Tất cả), đọc số tổng\n"
     "2. Dán đường dẫn màn danh sách KHÔNG kèm tham số chế độ, đọc số tổng\n"
     "3. Soát cột Người lập ở chế độ thứ hai",
     "—",
     "- Chế độ Tất cả: tổng theo phạm vi công ty\n"
     "- Chế độ không kèm tham số: chỉ 12 phiếu, mọi dòng đều do C lập\n"
     "- Chế độ này hiện CẢ phiếu nháp của C"),

    ("004", "Bố cục mặc định của màn danh sách", "P0",
     "Tài khoản có quyền xem tổng công ty",
     "1. Mở màn Đề nghị thu tiền\n"
     "2. Quan sát từ trên xuống",
     "—",
     "- Phía trên bảng có nút \"Bộ lọc\" và nút \"Tạo mới\"\n"
     "- Khối tìm kiếm mặc định ĐANG THU GỌN, bấm nút Bộ lọc mới bung ra\n"
     "- Bảng có các cột: STT, Mã phiếu, Loại thu, Khách hàng/Nhà cung cấp, Số tiền, Lý do nộp, Ngày lập, "
     "Người lập, Phòng ban, Trạng thái, Hành động\n"
     "- Mặc định 10 dòng mỗi trang, phiếu mới nhất lên đầu"),

    ("005", "Màn chờ duyệt và màn Đã xử lý có thêm cột Người nộp", "P1",
     "Tài khoản KT-1 có quyền Kế toán thanh toán",
     "1. Mở màn Phiếu đề nghị thu tiền chờ duyệt, đếm và ghi tên các cột\n"
     "2. Mở chế độ Đã xử lý bằng đường dẫn trực tiếp, ghi tên các cột\n"
     "3. So với màn danh sách thường",
     "—",
     "- Cả 2 màn đều có thêm cột \"Người nộp\" nằm sau cột Lý do nộp\n"
     "- Cả 2 màn đều KHÔNG có nút Tạo mới\n"
     "- ⚠️ Cột Người nộp thường TRỐNG vì form nhập không có ô này (mục 9 ghi chú 3)"),

    ("006", "Chế độ Đã xử lý không có mục menu", "P2",
     "Tài khoản KT-1",
     "1. Rà toàn bộ menu, tìm mục dẫn tới danh sách phiếu mình đã xử lý\n"
     "2. Mở chế độ đó bằng đường dẫn trực tiếp",
     "—",
     "- Không có mục menu nào trỏ tới chế độ này\n"
     "- Mở bằng đường dẫn thì màn chạy bình thường, liệt kê phiếu KT-1 đã xử lý\n"
     "- ⚠️ Ghi nhận là hiện trạng: chức năng có nhưng không có lối vào"),

    ("007", "Nhãn trạng thái hiển thị đúng màu cho cả 6 trạng thái", "P0",
     "Dữ liệu có phiếu ở đủ 6 trạng thái",
     "1. Bấm Bộ lọc, chọn lần lượt từng giá trị trong ô Trạng thái rồi tìm kiếm\n"
     "2. Quan sát nhãn ở cột Trạng thái",
     "6 trạng thái",
     "- Ô Trạng thái có đúng 6 lựa chọn: Đang tạo, Chờ KT duyệt, Đã tạo phiếu thu, Đã hạch toán, Hủy, "
     "Không duyệt\n"
     "- Đã tạo phiếu thu và Đã hạch toán: nhãn XANH\n"
     "- Bốn trạng thái còn lại: nhãn ĐỎ\n"
     "- ⚠️ Chờ KT duyệt hiện nhãn ĐỎ là đúng thiết kế"),

    ("008", "Cột Khách hàng/Nhà cung cấp chỉ lấy dòng đầu tiên", "P0",
     "Phiếu X loại Thu bán hàng có 3 dòng chi tiết của 3 khách hàng, dòng đầu là KH-001",
     "1. Tìm phiếu X trong danh sách, đọc cột Khách hàng/Nhà cung cấp\n"
     "2. Bấm Mã phiếu để mở chi tiết, đếm số khách hàng trong bảng chi tiết",
     "Phiếu X: 3 khách hàng",
     "- Ngoài danh sách chỉ hiện \"KH-001-<tên khách hàng>\"\n"
     "- Chi tiết hiện đủ 3 khách hàng\n"
     "- ⚠️ Đúng thiết kế, không phải mất dữ liệu"),

    ("009", "Phiếu Thu nhà cung cấp hiện tên nhà cung cấp ở cột đối tượng", "P1",
     "Có phiếu loại Thu nhà cung cấp trong dữ liệu",
     "1. Lọc Loại thu = Thu nhà cung cấp, tìm kiếm\n"
     "2. Đọc cột Khách hàng/Nhà cung cấp",
     "Loại thu: Thu nhà cung cấp",
     "- Cột hiện mã và tên NHÀ CUNG CẤP\n"
     "- Không hiện tên khách hàng"),

    ("010", "Phiếu loại Thu khác của dữ liệu cũ vẫn hiển thị", "P2",
     "Kho dữ liệu có phiếu cũ loại Thu khác (nếu môi trường test không có thì ghi Không áp dụng)",
     "1. Bấm Bộ lọc, mở ô Loại thu, đếm số lựa chọn\n"
     "2. Tìm phiếu cũ loại Thu khác bằng ô Mã phiếu\n"
     "3. Đọc cột Loại thu và cột Khách hàng/Nhà cung cấp",
     "—",
     "- Ô lọc Loại thu chỉ có 2 lựa chọn: Thu bán hàng, Thu nhà cung cấp\n"
     "- Phiếu cũ vẫn hiện nhãn \"Thu khác\" ở cột Loại thu\n"
     "- Cột Khách hàng/Nhà cung cấp của phiếu Thu khác để TRỐNG"),

    ("011", "Bấm mã phiếu mở màn chi tiết", "P1",
     "Danh sách đang có phiếu",
     "1. Bấm vào Mã phiếu ở dòng đầu\n"
     "2. Quan sát trang mở ra",
     "—",
     "- Mở màn Chi tiết phiếu đề nghị thu tiền đúng phiếu vừa bấm\n"
     "- Mã phiếu trên màn chi tiết khớp với dòng vừa bấm"),

    ("012", "Bảng rỗng khi bộ lọc không khớp phiếu nào", "P1",
     "Danh sách đang có dữ liệu",
     "1. Bấm Bộ lọc, gõ chuỗi chắc chắn không tồn tại vào ô Mã phiếu\n"
     "2. Bấm nút tìm kiếm",
     "Mã phiếu: ZZZZ-KHONG-TON-TAI",
     "- Bảng hiện dòng báo không có dữ liệu\n"
     "- Tổng hiện 0, không có lỗi đỏ\n"
     "- Nút Tạo mới vẫn còn"),
]

SEC_II = [
    ("001", "Bung và thu gọn khối bộ lọc", "P1",
     "Vừa mở màn danh sách",
     "1. Quan sát khối tìm kiếm trước khi bấm gì\n"
     "2. Bấm nút Bộ lọc\n"
     "3. Bấm lại lần nữa",
     "—",
     "- Ban đầu khối tìm kiếm ẩn\n"
     "- Bấm lần 1 bung ra đủ các ô lọc, có nút kính lúp (tìm kiếm) và nút mũi tên tròn (làm mới)\n"
     "- Bấm lần 2 thu gọn lại"),

    ("002", "Danh sách các ô lọc ở chế độ Tất cả", "P0",
     "Tài khoản có quyền xem tổng công ty, đang ở chế độ Tất cả",
     "1. Bấm Bộ lọc\n"
     "2. Ghi lại toàn bộ ô lọc theo thứ tự",
     "—",
     "- Có các ô: Công ty, Phòng ban, Từ ngày, Đến ngày, Mã phiếu, Số tiền đề nghị thu từ, Số tiền đề "
     "nghị thu đến, Loại thu, Người nộp, Người lập, Số đơn hàng/hợp đồng, Trạng thái, Khách hàng, "
     "Nhà cung cấp\n"
     "- Có 2 nút: tìm kiếm và làm mới"),

    ("003", "Màn chờ duyệt không có ô lọc Trạng thái", "P1",
     "Tài khoản KT-1, đang ở màn chờ duyệt",
     "1. Bấm Bộ lọc\n"
     "2. Tìm ô Trạng thái và các ô lọc theo đơn vị",
     "—",
     "- KHÔNG có ô Trạng thái (màn này đã cố định lọc trạng thái Chờ KT duyệt)\n"
     "- KHÔNG có ô Công ty / Phòng ban / Bộ phận"),

    ("004", "Lọc theo Mã phiếu tìm được khớp một phần", "P0",
     "Có phiếu mã kết thúc bằng .00017",
     "1. Gõ 00017 vào ô Mã phiếu\n"
     "2. Bấm nút tìm kiếm",
     "Mã phiếu: 00017",
     "- Chỉ còn phiếu có chuỗi 00017 nằm trong mã\n"
     "- Bảng về trang 1, tổng đổi theo"),

    ("005", "Bộ lọc chỉ chạy khi bấm nút tìm kiếm", "P0",
     "Khối lọc đang bung",
     "1. Gõ 00017 vào ô Mã phiếu, KHÔNG bấm gì thêm, chờ 5 giây\n"
     "2. Bấm nút tìm kiếm",
     "—",
     "- Trong lúc gõ, bảng KHÔNG đổi\n"
     "- Chỉ sau khi bấm nút tìm kiếm bảng mới lọc lại"),

    ("006", "Lọc theo Loại thu", "P0",
     "Dữ liệu có cả phiếu Thu bán hàng và Thu nhà cung cấp",
     "1. Chọn Loại thu = Thu bán hàng, tìm kiếm, soát cột Loại thu\n"
     "2. Đổi sang Thu nhà cung cấp, tìm kiếm, soát lại",
     "Thu bán hàng → Thu nhà cung cấp",
     "- Mỗi lần lọc, mọi dòng đều đúng loại thu vừa chọn\n"
     "- Phiếu cũ loại Thu khác không lọt vào cả 2 tập kết quả"),

    ("007", "Lọc theo Trạng thái", "P0",
     "Dữ liệu có phiếu ở đủ 6 trạng thái",
     "1. Chọn Trạng thái = Chờ KT duyệt, tìm kiếm\n"
     "2. Lặp lại với Không duyệt và Hủy",
     "3 trạng thái",
     "- Mỗi lần lọc, mọi dòng đều đúng trạng thái đang chọn\n"
     "- Lọc Đang tạo ở chế độ Tất cả chỉ ra phiếu nháp của chính người đăng nhập"),

    ("008", "Lọc theo Số đơn hàng/hợp đồng", "P0",
     "Phiếu Y có dòng chi tiết gắn hợp đồng mã HD-2026-001",
     "1. Gõ HD-2026-001 vào ô Số đơn hàng/hợp đồng, tìm kiếm\n"
     "2. Mở chi tiết một dòng kết quả\n"
     "3. Gõ lại một phần mã (HD-2026), tìm kiếm",
     "Số hợp đồng: HD-2026-001 rồi HD-2026",
     "- Ra các phiếu có ÍT NHẤT MỘT dòng chi tiết gắn hợp đồng đó\n"
     "- Mở chi tiết thấy đúng mã hợp đồng vừa lọc\n"
     "- Gõ một phần mã vẫn ra kết quả"),

    ("009", "Lọc theo Khách hàng", "P0",
     "Khách hàng KH-001 xuất hiện trong ít nhất 5 phiếu",
     "1. Bấm ô Khách hàng, gõ từ khóa, chờ danh sách gợi ý\n"
     "2. Chọn KH-001, bấm tìm kiếm\n"
     "3. Mở chi tiết 2 dòng kết quả để đối chiếu",
     "Khách hàng: KH-001",
     "- Ô Khách hàng là ô chọn có tìm kiếm từ xa, gõ mới ra gợi ý\n"
     "- Kết quả chỉ gồm phiếu có dòng chi tiết gắn KH-001\n"
     "- Phiếu gom nhiều khách hàng vẫn ra nếu KH-001 nằm ở dòng bất kỳ, không riêng dòng đầu"),

    ("010", "Lọc theo Nhà cung cấp", "P1",
     "Nhà cung cấp NCC-01 xuất hiện trong ít nhất 2 phiếu Thu nhà cung cấp",
     "1. Mở ô Nhà cung cấp, chọn NCC-01, tìm kiếm\n"
     "2. Soát kết quả",
     "Nhà cung cấp: NCC-01",
     "- Ô Nhà cung cấp là danh sách chọn sẵn (không phải gõ tìm)\n"
     "- Kết quả chỉ gồm phiếu có dòng chi tiết gắn NCC-01"),

    ("011", "Lọc theo Người lập", "P1",
     "NV-B đã lập 12 phiếu trong phạm vi người đăng nhập nhìn thấy",
     "1. Bấm ô Người lập, gõ tên NV-B, chọn từ gợi ý\n"
     "2. Bấm tìm kiếm, đọc cột Người lập",
     "Người lập: NV-B",
     "- Mọi dòng đều có Người lập là NV-B\n"
     "- Số dòng khớp số phiếu của NV-B trong phạm vi được xem"),

    ("012", "Ô lọc Người nộp không có tác dụng", "P0",
     "Danh sách đang có ít nhất 20 phiếu",
     "1. Ghi lại tổng số phiếu hiện tại\n"
     "2. Gõ một chuỗi bất kỳ vào ô Người nộp, bấm tìm kiếm\n"
     "3. Gõ chuỗi chắc chắn vô nghĩa, tìm kiếm lại",
     "Người nộp: \"Nguyen Van A\", rồi \"ZZZZZZ\"",
     "- ⚠️ Hiện trạng: cả 2 lần tổng số phiếu KHÔNG đổi, hệ thống bỏ qua ô này. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: lọc theo tên người nộp tiền, hoặc bỏ hẳn ô lọc này khỏi màn hình"),

    ("013", "Lọc theo khoảng Số tiền đề nghị thu", "P0",
     "Có phiếu tổng tiền 5.000.000; có phiếu 20.000.000; có phiếu 90.000.000",
     "1. Nhập Số tiền đề nghị thu từ = 10.000.000, để trống ô đến, tìm kiếm\n"
     "2. Kiểm cột Số tiền của kết quả\n"
     "3. Nhập thêm Số tiền đề nghị thu đến = 50.000.000, tìm kiếm",
     "Từ 10.000.000 · Đến 50.000.000",
     "- Bước 1: mất phiếu 5.000.000; còn phiếu 20.000.000 và 90.000.000\n"
     "- Bước 3: chỉ còn phiếu có Số tiền trong đoạn 10.000.000 đến 50.000.000, tính cả 2 đầu mút\n"
     "- ⚠️ So với TỔNG QUY ĐỔI VND của cả phiếu, không so từng dòng"),

    ("014", "Lọc khoảng tiền trên phiếu ngoại tệ so đúng số quy đổi", "P0",
     "Phiếu Z loại tiền USD, 1 dòng 1.000 USD, tỷ giá 25.000 nên tổng quy đổi 25.000.000",
     "1. Nhập khoảng tiền từ 20.000.000 đến 30.000.000, tìm kiếm, tìm phiếu Z\n"
     "2. Đổi khoảng lọc thành từ 500 đến 2.000, tìm kiếm lại",
     "Hai khoảng lọc",
     "- Bước 1: phiếu Z CÓ trong kết quả\n"
     "- Bước 2: phiếu Z KHÔNG có trong kết quả\n"
     "- ⚠️ Bộ lọc so số đã quy đổi VND, không so số nguyên tệ"),

    ("015", "Ô lọc tiền tự thêm dấu ngăn nghìn", "P2",
     "Khối lọc đang bung",
     "1. Gõ 10000000 vào ô Số tiền đề nghị thu từ\n"
     "2. Rời khỏi ô\n"
     "3. Thử gõ chữ cái vào ô này",
     "Nhập 10000000, rồi chữ cái",
     "- Số hiện thành 10.000.000 với dấu ngăn nghìn\n"
     "- Chữ cái không vào được ô\n"
     "- Bấm tìm kiếm vẫn lọc đúng"),

    ("016", "Lọc theo Từ ngày", "P0",
     "Có phiếu lập ngày 31/07/2026 và phiếu lập ngày 05/08/2026",
     "1. Nhập Từ ngày = 01/08/2026, tìm kiếm\n"
     "2. Đọc cột Ngày lập của dòng cũ nhất trong kết quả",
     "Từ ngày: 01/08/2026",
     "- Phiếu 31/07/2026 bị loại\n"
     "- Phiếu 05/08/2026 còn trong kết quả\n"
     "- ⚠️ Phiếu lập đúng 0 giờ ngày 01/08/2026 (nếu có) bị loại — bẫy ở mục 4"),

    ("017", "Ô Đến ngày làm rụng trọn ngày cuối", "P0",
     "Có phiếu lập lúc 09:15 ngày 31/08/2026 và phiếu lập ngày 30/08/2026",
     "1. Nhập Đến ngày = 31/08/2026, tìm kiếm\n"
     "2. Tìm phiếu lập ngày 31/08/2026 trong kết quả\n"
     "3. Đổi Đến ngày = 01/09/2026, tìm lại",
     "Đến ngày: 31/08/2026, rồi 01/09/2026",
     "- ⚠️ Hiện trạng: đặt Đến ngày 31/08/2026 thì phiếu lập trong chính ngày 31/08 BỊ MẤT; phải đặt "
     "01/09/2026 mới thấy. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: Đến ngày phải tính trọn ngày đó\n"
     "- Phiếu 30/08/2026 có mặt ở cả 2 lần"),

    ("018", "Kết hợp nhiều điều kiện lọc cùng lúc", "P0",
     "Có ít nhất 3 phiếu Thu bán hàng, trạng thái Chờ KT duyệt, tổng tiền trên 10.000.000",
     "1. Chọn Loại thu = Thu bán hàng\n"
     "2. Chọn Trạng thái = Chờ KT duyệt\n"
     "3. Nhập Số tiền đề nghị thu từ = 10.000.000\n"
     "4. Bấm tìm kiếm, kiểm TỪNG dòng kết quả",
     "3 điều kiện cùng lúc",
     "- Mọi dòng thỏa ĐỒNG THỜI cả 3 điều kiện\n"
     "- ⚠️ Kiểm từng dòng, đừng chỉ nhìn số tổng"),

    ("019", "Nút làm mới xóa sạch điều kiện lọc", "P0",
     "Đang lọc bằng ít nhất 4 điều kiện",
     "1. Bấm nút làm mới (biểu tượng mũi tên tròn)\n"
     "2. Quan sát các ô lọc và bảng",
     "—",
     "- Mọi ô lọc về trống, kể cả ô chọn Khách hàng và Nhà cung cấp\n"
     "- Bảng nạp lại đầy đủ từ trang 1"),

    ("020", "Đổi Công ty thì danh sách Phòng ban đổi theo", "P1",
     "Tài khoản có quyền xem tổng công ty",
     "1. Chọn Công ty A, mở ô Phòng ban, ghi lại danh sách\n"
     "2. Đổi Công ty sang B, mở lại ô Phòng ban",
     "Công ty A → B",
     "- Danh sách Phòng ban đổi theo công ty đang chọn\n"
     "- Không còn phòng ban của công ty A trong danh sách"),

    ("021", "Bộ lọc được ghi nhớ khi rời màn rồi quay lại", "P1",
     "Đang lọc Trạng thái = Hủy ở chế độ Tất cả",
     "1. Sang màn khác\n"
     "2. Quay lại mục Đề nghị thu tiền trên menu\n"
     "3. Bấm Bộ lọc, quan sát các ô",
     "Trạng thái: Hủy",
     "- Điều kiện Trạng thái = Hủy vẫn còn, bảng hiện đúng tập đã lọc\n"
     "- ⚠️ Test xong nhớ bấm nút làm mới trước khi sang ca test khác"),

    ("022", "Bộ lọc của các chế độ danh sách không dùng chung", "P1",
     "Tài khoản KT-1",
     "1. Ở chế độ Tất cả, lọc Loại thu = Thu nhà cung cấp\n"
     "2. Sang màn chờ duyệt, bấm Bộ lọc, quan sát\n"
     "3. Quay lại chế độ Tất cả",
     "—",
     "- Màn chờ duyệt mở ra với bộ lọc TRẮNG\n"
     "- Quay lại chế độ Tất cả vẫn còn điều kiện Loại thu = Thu nhà cung cấp"),
]

SEC_III = [
    ("001", "Thứ tự mặc định là phiếu mới nhất lên đầu", "P0",
     "Danh sách chưa bấm sắp xếp cột nào",
     "1. Mở màn danh sách\n"
     "2. Đọc cột Ngày lập của 10 dòng đầu",
     "—",
     "- Ngày lập giảm dần từ trên xuống\n"
     "- Dòng đầu là phiếu lập gần đây nhất trong phạm vi đang xem"),

    ("002", "Chỉ cột Số tiền cho phép sắp xếp", "P1",
     "Danh sách đang có dữ liệu",
     "1. Bấm lần lượt tiêu đề các cột: Mã phiếu, Loại thu, Khách hàng/Nhà cung cấp, Lý do nộp, Ngày lập, "
     "Người lập, Phòng ban, Trạng thái\n"
     "2. Quan sát thứ tự dòng sau mỗi lần bấm\n"
     "3. Bấm tiêu đề cột Số tiền",
     "—",
     "- Tám cột ở bước 1 KHÔNG có mũi tên sắp xếp, bấm không đổi thứ tự\n"
     "- Chỉ cột Số tiền có mũi tên sắp xếp"),

    ("003", "Sắp xếp theo cột Số tiền", "P0",
     "Danh sách có nhiều hơn 1 trang, số tiền các phiếu khác nhau rõ rệt",
     "1. Bấm tiêu đề cột Số tiền\n"
     "2. Đọc cột Số tiền từ trên xuống\n"
     "3. Bấm lần nữa để đổi chiều",
     "—",
     "- Bảng sắp xếp đúng theo giá trị số tiền, tăng rồi giảm\n"
     "- Bảng KHÔNG báo lỗi tải dữ liệu\n"
     "- ⚠️ Đây là điểm rủi ro: cột Số tiền là số cộng dồn, không phải dữ liệu gốc. Nếu bảng báo lỗi "
     "hoặc thứ tự không đổi thì ghi Failed kèm ảnh chụp"),

    ("004", "Chuyển trang giữ nguyên bộ lọc", "P0",
     "Đang lọc Loại thu = Thu bán hàng, kết quả hơn 3 trang",
     "1. Sang trang 2, soát cột Loại thu\n"
     "2. Đọc ô hiển thị số dòng\n"
     "3. Sang trang 3 rồi quay về trang 1",
     "Loại thu: Thu bán hàng",
     "- Mọi trang đều chỉ có Thu bán hàng\n"
     "- Tổng N giữ nguyên, khoảng a đến b đổi theo trang\n"
     "- Chuyển trang không làm mất điều kiện lọc"),

    ("005", "Cột STT đánh số liên tục theo trang", "P0",
     "10 dòng mỗi trang, kết quả hơn 20 dòng",
     "1. Đọc STT dòng cuối trang 1\n"
     "2. Sang trang 2, đọc STT dòng đầu và dòng cuối",
     "10 dòng mỗi trang",
     "- Trang 1 kết thúc ở 10\n"
     "- Trang 2 chạy từ 11 tới 20"),

    ("006", "Đổi số dòng mỗi trang", "P0",
     "Kết quả hơn 100 dòng, đang ở trang 3",
     "1. Đổi số dòng mỗi trang sang 25\n"
     "2. Quan sát trang hiện tại và số dòng\n"
     "3. Đổi tiếp sang 100",
     "25 rồi 100 dòng mỗi trang",
     "- Mỗi lần đổi đều quay về trang 1\n"
     "- Số dòng trên màn đúng bằng số vừa chọn (trừ trang cuối)\n"
     "- Ô hiển thị số dòng cập nhật theo"),

    ("007", "Ô tìm kiếm nhanh sẵn có của bảng", "P2",
     "Danh sách đang có dữ liệu",
     "1. Tìm ô tìm kiếm nhanh ở góc bảng (nếu có)\n"
     "2. Gõ một mã phiếu vào đó",
     "—",
     "- Ghi nhận hành vi thực tế: có lọc được hay không, có gọi lại dữ liệu hay không\n"
     "- Không được làm bảng báo lỗi"),

    ("008", "Định dạng số tiền trên lưới có 2 chữ số thập phân", "P1",
     "Có phiếu tổng tiền tròn 15.000.000 và phiếu có phần lẻ",
     "1. Tìm 2 phiếu trên\n"
     "2. Đọc cột Số tiền",
     "—",
     "- Số tiền hiện dấu chấm ngăn nghìn và LUÔN có 2 chữ số thập phân, ví dụ 15.000.000,00\n"
     "- Phiếu tổng tiền 0 hiện 0,00, không để trống"),

    ("009", "Định dạng Ngày lập trên lưới", "P2",
     "Danh sách đang có dữ liệu",
     "1. Đọc cột Ngày lập của vài dòng",
     "—",
     "- Hiện dạng ngày/tháng/năm, KHÔNG có giờ phút\n"
     "- Không có dòng nào hiện ngày sai định dạng"),

    ("010", "Menu hành động của từng dòng", "P0",
     "4 dòng ở 4 trạng thái: Đang tạo (của mình), Chờ KT duyệt, Không duyệt (của mình), Đã hạch toán",
     "1. Bấm nút bánh răng ở cột Hành động của từng dòng\n"
     "2. Ghi lại các mục trong menu",
     "4 trạng thái",
     "- Đang tạo: In, Sửa, Xóa\n"
     "- Chờ KT duyệt: In (thêm Tạo phiếu thu nếu người đăng nhập là kế toán thanh toán)\n"
     "- Không duyệt: In, Sửa, Xóa\n"
     "- Đã hạch toán: chỉ In"),

    ("011", "Nút Sửa và Xóa hiện trên phiếu Không duyệt của NGƯỜI KHÁC", "P0",
     "Tài khoản C có quyền xem theo công ty; phiếu W trạng thái Không duyệt do NV-B lập, cùng công ty",
     "1. Đăng nhập bằng C, tìm phiếu W trong danh sách\n"
     "2. Mở menu hành động của dòng phiếu W",
     "Phiếu W của NV-B, trạng thái Không duyệt",
     "- ⚠️ Hiện trạng: menu vẫn có Sửa và Xóa dù C không phải người lập. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: chỉ người lập phiếu mới thấy 2 nút này\n"
     "- Bấm Sửa mở được màn Sửa của phiếu người khác"),
]

SEC_IV = [
    ("001", "Bố cục màn Tạo mới", "P0",
     "Tài khoản bất kỳ, đang ở màn danh sách",
     "1. Bấm nút Tạo mới\n"
     "2. Quan sát từ trên xuống",
     "—",
     "- Tiêu đề trang \"Tạo phiếu đề nghị thu tiền\"\n"
     "- Khối \"Thông tin chung\", góc phải khối hiện tên người đang đăng nhập và ngày hôm nay\n"
     "- Có 4 ô: Loại thu, Loại tiền, Tỷ giá, Lý do thu — cả 4 đều gắn dấu bắt buộc\n"
     "- KHÔNG có ô Mã phiếu, Người tạo, Phòng ban (3 ô này chỉ có ở màn Sửa)\n"
     "- KHÔNG có ô Người nộp tiền\n"
     "- Khối \"Chi tiết\" và 3 nút dưới cùng: Lưu, Lưu và gửi duyệt, Quay lại"),

    ("002", "Chưa chọn Loại thu thì chưa hiện bảng chi tiết", "P0",
     "Vừa mở màn Tạo mới",
     "1. Quan sát khối Chi tiết khi ô Loại thu còn để trống\n"
     "2. Chọn Loại thu = Thu bán hàng",
     "—",
     "- Khi chưa chọn: khối Chi tiết chỉ hiện dòng chữ \"Chưa chọn loại thu\"\n"
     "- Chọn xong thì bảng chi tiết hiện ra ngay, đã có sẵn 1 dòng trống"),

    ("003", "Giá trị mặc định của Loại tiền và Tỷ giá", "P0",
     "Vừa mở màn Tạo mới",
     "1. Đọc ô Loại tiền và ô Tỷ giá\n"
     "2. Thử gõ vào ô Tỷ giá",
     "—",
     "- Loại tiền mặc định là VND\n"
     "- Ô Tỷ giá bị KHÓA, không gõ được, bên phải ô có nhãn VND\n"
     "- Giá trị tỷ giá lấy theo tỷ giá của VND trong danh mục tiền tệ"),

    ("004", "Tiêu đề bảng chi tiết đổi theo Loại thu", "P0",
     "Đang ở màn Tạo mới",
     "1. Chọn Loại thu = Thu bán hàng, đọc tiêu đề cột 2 và cột 3\n"
     "2. Đổi sang Thu nhà cung cấp, đọc lại",
     "Thu bán hàng → Thu nhà cung cấp",
     "- Thu bán hàng: cột 2 \"Khách hàng\", cột 3 \"Số đơn hàng/Hợp đồng\"\n"
     "- Thu nhà cung cấp: cột 2 \"Nhà cung cấp\", cột 3 \"Hợp đồng mua\"\n"
     "- Cột 4 luôn là \"Số tiền còn nợ\""),

    ("005", "Đổi Loại thu xóa sạch dòng chi tiết và không hỏi xác nhận", "P0",
     "Đang ở màn Tạo mới, đã nhập 3 dòng chi tiết đủ khách hàng, hợp đồng và số tiền",
     "1. Đổi ô Loại thu sang Thu nhà cung cấp\n"
     "2. Quan sát ngay lập tức",
     "3 dòng chi tiết đã nhập",
     "- ⚠️ KHÔNG có hộp thoại xác nhận nào\n"
     "- Toàn bộ 3 dòng biến mất, bảng còn đúng 1 dòng trống\n"
     "- Ghi nhận đúng hiện trạng; nếu nghiệp vụ muốn cảnh báo thì mở lỗi cải tiến"),

    ("006", "Thêm và xóa dòng chi tiết", "P0",
     "Đang ở màn Tạo mới, Loại thu = Thu bán hàng, có 1 dòng trống",
     "1. Bấm dấu cộng ở góc phải tiêu đề bảng 2 lần\n"
     "2. Đếm số dòng\n"
     "3. Bấm biểu tượng thùng rác ở dòng 2\n"
     "4. Quan sát",
     "—",
     "- Sau bước 1 có 3 dòng, STT đánh 1, 2, 3\n"
     "- Xóa dòng 2 thì còn 2 dòng, STT đánh lại 1 và 2, dữ liệu 2 dòng còn lại không xáo trộn\n"
     "- Xóa dòng KHÔNG hỏi xác nhận"),

    ("007", "Chọn khách hàng cho từng dòng", "P0",
     "Đang có 2 dòng chi tiết trống, Loại thu = Thu bán hàng",
     "1. Bấm nút kính lúp ở ô Khách hàng của dòng 1\n"
     "2. Quan sát cửa sổ mở ra: tiêu đề và các cột\n"
     "3. Tìm và chọn KH-001\n"
     "4. Làm tương tự cho dòng 2 với KH-002",
     "Dòng 1: KH-001 · Dòng 2: KH-002",
     "- Cửa sổ tên \"Khách hàng\", 4 cột: STT, Mã khách hàng, Tên khách hàng, Loại khách hàng\n"
     "- Có 2 ô tìm: Mã khách hàng và Tên khách hàng\n"
     "- Chọn xong hiện thông báo xanh \"Thêm khách hàng thành công!\", ô hiển thị \"mã - tên\"\n"
     "- 2 dòng giữ 2 khách hàng KHÁC NHAU, chọn dòng sau không ghi đè dòng trước"),

    ("008", "Chọn nhà cung cấp cho dòng của phiếu Thu nhà cung cấp", "P0",
     "Loại thu = Thu nhà cung cấp, có 1 dòng trống",
     "1. Bấm kính lúp ở ô Nhà cung cấp của dòng 1\n"
     "2. Quan sát cửa sổ: tiêu đề, các cột, các ô tìm\n"
     "3. Tìm theo mã rồi chọn một nhà cung cấp",
     "—",
     "- Cửa sổ tên \"Nhà cung cấp\", 3 cột: STT, Mã nhà cung cấp, Tên nhà cung cấp\n"
     "- Chọn xong hiện thông báo \"Thêm nhà cung cấp thành công!\"\n"
     "- Ô hiển thị \"mã - tên nhà cung cấp\""),

    ("009", "Chưa chọn khách hàng mà bấm chọn hợp đồng", "P0",
     "Vừa thêm 1 dòng chi tiết trống, Loại thu = Thu bán hàng",
     "1. Bấm kính lúp ở ô Số đơn hàng/Hợp đồng của dòng đó\n"
     "2. Quan sát\n"
     "3. Đổi Loại thu sang Thu nhà cung cấp và lặp lại",
     "—",
     "- Thu bán hàng: hiện cảnh báo vàng \"Chưa chọn khách hàng\", cửa sổ KHÔNG mở\n"
     "- Thu nhà cung cấp: hiện cảnh báo \"Chưa chọn nhà cung cấp\", cửa sổ KHÔNG mở"),

    ("010", "Cửa sổ chọn hợp đồng của phiếu Thu bán hàng", "P0",
     "Dòng 1 đã chọn khách hàng KH-001; người đang đăng nhập là NGƯỜI LẬP của ít nhất 3 hợp đồng còn "
     "hiệu lực của KH-001",
     "1. Bấm kính lúp ở ô Số đơn hàng/Hợp đồng của dòng 1\n"
     "2. Quan sát tiêu đề, các cột và ô tìm kiếm\n"
     "3. Đếm số dòng",
     "Khách hàng: KH-001",
     "- Cửa sổ tên \"Đơn hàng/Hợp đồng\", 3 cột: STT, Số đơn hàng/Hợp đồng, Ngày lập\n"
     "- Chỉ có 1 ô tìm: Số đơn hàng/Hợp đồng\n"
     "- Hiện đủ 3 hợp đồng của KH-001 do chính người đăng nhập lập"),

    ("011", "Cửa sổ hợp đồng bán chỉ hiện hợp đồng do chính mình lập", "P0",
     "Khách hàng KH-001 có 3 hợp đồng còn hiệu lực do NV-A lập và 4 hợp đồng còn hiệu lực do NV-B lập",
     "1. Đăng nhập bằng NV-A, tạo phiếu, chọn KH-001 cho dòng 1\n"
     "2. Mở cửa sổ chọn hợp đồng, đếm và ghi lại các mã\n"
     "3. Đăng nhập bằng NV-B, làm lại từ bước 1",
     "KH-001: 3 hợp đồng của NV-A + 4 của NV-B",
     "- NV-A chỉ thấy đúng 3 hợp đồng của mình\n"
     "- NV-B chỉ thấy đúng 4 hợp đồng của mình\n"
     "- ⚠️ Đây là quy tắc CÓ CHỦ ĐÍCH (mục 9 ghi chú 1), không phải mất dữ liệu"),

    ("012", "Cửa sổ hợp đồng bán loại bỏ hợp đồng chưa đủ điều kiện", "P0",
     "Người đăng nhập là người lập của: 2 hợp đồng khách hàng KH-002 còn hiệu lực, 1 hợp đồng KH-002 "
     "đang ở trạng thái nháp, 1 hợp đồng KH-002 đã hủy",
     "1. Chọn KH-002 cho dòng 1\n"
     "2. Mở cửa sổ chọn hợp đồng\n"
     "3. Đối chiếu với 4 hợp đồng đã biết",
     "KH-002: 4 hợp đồng, 2 hợp lệ",
     "- Chỉ hiện 2 hợp đồng còn hiệu lực trở lên\n"
     "- Hợp đồng nháp và hợp đồng đã hủy KHÔNG hiện"),

    ("013", "Cửa sổ hợp đồng bán gộp đủ 3 nguồn hợp đồng", "P1",
     "Khách hàng KH-003 do chính người đăng nhập phụ trách, có: 1 hợp đồng bán, 1 hợp đồng bảo hành sửa "
     "chữa, 1 hợp đồng đầu kỳ — tất cả đều đủ điều kiện",
     "1. Chọn KH-003 cho dòng 1\n"
     "2. Mở cửa sổ chọn hợp đồng, đọc các mã",
     "KH-003: 3 hợp đồng khác loại",
     "- Cả 3 hợp đồng đều xuất hiện trong cùng một danh sách\n"
     "- Chọn hợp đồng nào cũng gán được vào dòng"),

    ("014", "Cửa sổ chọn hợp đồng mua của phiếu Thu nhà cung cấp", "P0",
     "Dòng 1 đã chọn nhà cung cấp NCC-01; NCC-01 có hợp đồng mua đã duyệt do NGƯỜI KHÁC lập",
     "1. Bấm kính lúp ở ô Hợp đồng mua của dòng 1\n"
     "2. Quan sát tiêu đề, cột và số dòng",
     "Nhà cung cấp: NCC-01",
     "- Cửa sổ tên \"Hợp đồng\", 3 cột: STT, Hợp đồng, Ngày lập, ô tìm theo Số hợp đồng\n"
     "- ⚠️ Hợp đồng mua do NGƯỜI KHÁC lập VẪN hiện — khác hẳn cửa sổ hợp đồng bán ở TC_04.011"),

    ("015", "Tìm kiếm trong cửa sổ chọn hợp đồng", "P1",
     "Cửa sổ chọn hợp đồng đang mở với hơn 10 dòng",
     "1. Gõ một phần số hợp đồng vào ô tìm, bấm tìm kiếm\n"
     "2. Đọc kết quả\n"
     "3. Xóa từ khóa, tìm lại",
     "Từ khóa: một phần số hợp đồng",
     "- Chỉ còn hợp đồng có chuỗi vừa gõ\n"
     "- Xóa từ khóa thì danh sách trở lại đầy đủ\n"
     "- Phân trang trong cửa sổ hoạt động bình thường"),

    ("016", "Chọn hợp đồng tự điền mã và Số tiền còn nợ", "P0",
     "Cửa sổ chọn hợp đồng đang mở; hợp đồng HD-2026-001 có công nợ phải thu 25.000.000",
     "1. Bấm chọn dòng HD-2026-001\n"
     "2. Quan sát dòng chi tiết trên form",
     "Hợp đồng: HD-2026-001",
     "- Hiện thông báo xanh \"Thêm thành công\", cửa sổ đóng lại\n"
     "- Ô hợp đồng của dòng hiện HD-2026-001\n"
     "- Cột Số tiền còn nợ của dòng hiện 25.000.000\n"
     "- Dòng Tổng cộng cuối bảng cộng thêm 25.000.000 vào cột Số tiền còn nợ"),

    ("017", "Không chọn trùng một hợp đồng ở hai dòng", "P0",
     "Dòng 1 đã chọn HD-2026-001; dòng 2 đã chọn cùng khách hàng",
     "1. Mở cửa sổ chọn hợp đồng ở dòng 2\n"
     "2. Bấm chọn lại HD-2026-001",
     "Hợp đồng đã dùng: HD-2026-001",
     "- Hiện cảnh báo vàng \"Hợp đồng đã tồn tại!\"\n"
     "- Dòng 2 không được gán hợp đồng, cửa sổ vẫn mở"),

    ("018", "Đổi khách hàng của một dòng thì xóa hợp đồng và số tiền của dòng đó", "P0",
     "Dòng 1 đã chọn KH-001, hợp đồng HD-2026-001, Số tiền còn nợ 25.000.000, Số tiền đề nghị thu "
     "10.000.000, Ghi chú \"Đợt 1\"",
     "1. Bấm lại kính lúp ở ô Khách hàng của dòng 1, chọn KH-002\n"
     "2. Quan sát toàn bộ dòng 1",
     "Đổi KH-001 → KH-002",
     "- Ô hợp đồng về trống\n"
     "- Số tiền còn nợ về 0, Số tiền đề nghị thu về 0, Ghi chú bị xóa\n"
     "- ⚠️ Ghi chú của dòng cũng bị xóa theo — kiểm kỹ điểm này"),

    ("019", "Cột quy đổi VND chỉ hiện với loại tiền khác VND", "P0",
     "Đang ở màn Tạo mới, Loại thu = Thu bán hàng, có 1 dòng",
     "1. Để Loại tiền = VND, đếm số cột con của nhóm \"Số tiền đề nghị thu\"\n"
     "2. Đổi Loại tiền sang USD\n"
     "3. Đếm lại và đọc tiêu đề 2 cột con",
     "VND → USD",
     "- VND: nhóm chỉ có 1 cột\n"
     "- USD: tách thành 2 cột con, cột trái mang tên loại tiền (USD), cột phải là VND\n"
     "- Cột VND chỉ hiển thị, không gõ được"),

    ("020", "Đổi Loại tiền tự lấy tỷ giá của loại tiền đó", "P0",
     "Danh mục tiền tệ: USD có tỷ giá 25.000",
     "1. Đổi Loại tiền từ VND sang USD\n"
     "2. Đọc ô Tỷ giá\n"
     "3. Sửa tay tỷ giá thành 26.000\n"
     "4. Đổi Loại tiền về VND rồi lại sang USD",
     "USD tỷ giá 25.000 rồi 26.000",
     "- Đổi sang USD: ô Tỷ giá MỞ KHÓA và tự điền 25.000\n"
     "- Sửa tay được, hệ thống không chặn\n"
     "- Đổi qua lại thì tỷ giá tự nạp lại theo danh mục, số sửa tay bị mất"),

    ("021", "Cột quy đổi VND tính đúng theo tỷ giá", "P0",
     "Loại tiền USD, tỷ giá 25.000, 2 dòng chi tiết",
     "1. Nhập dòng 1: Số tiền đề nghị thu = 1.000\n"
     "2. Nhập dòng 2: Số tiền đề nghị thu = 2.000\n"
     "3. Đọc cột VND của từng dòng và dòng Tổng cộng\n"
     "4. Sửa tỷ giá thành 26.000, đọc lại",
     "1.000 và 2.000 USD",
     "- Dòng 1 cột VND hiện 25.000.000, dòng 2 hiện 50.000.000\n"
     "- Tổng cộng: cột USD 3.000, cột VND 75.000.000\n"
     "- Sau khi đổi tỷ giá thành 26.000, các số quy đổi tính lại thành 26.000.000 / 52.000.000 / 78.000.000"),

    ("022", "Dòng Tổng cộng cộng đúng 3 cột", "P0",
     "Phiếu VND, 3 dòng: Số tiền còn nợ 25.000.000 / 10.000.000 / 5.000.000; Số tiền đề nghị thu "
     "10.000.000 / 5.000.000 / 2.000.000",
     "1. Nhập đủ 3 dòng như trên\n"
     "2. Đọc dòng Tổng cộng cuối bảng",
     "3 dòng chi tiết",
     "- Tổng Số tiền còn nợ = 40.000.000\n"
     "- Tổng Số tiền đề nghị thu = 17.000.000\n"
     "- Số cập nhật ngay khi gõ, không phải bấm nút nào"),

    ("023", "Lưu nháp phiếu Thu bán hàng hợp lệ", "P0",
     "Màn Tạo mới, đã điền: Loại thu Thu bán hàng, Loại tiền VND, Lý do thu \"Thu tiền hợp đồng tháng 8\", "
     "2 dòng chi tiết đủ khách hàng, hợp đồng, số tiền 10.000.000 và 5.000.000",
     "1. Bấm nút Lưu\n"
     "2. Đọc thông báo\n"
     "3. Quan sát trang sau khi lưu\n"
     "4. Tìm phiếu vừa tạo",
     "Tổng 15.000.000",
     "- Thông báo xanh \"Thêm phiếu đề nghị thu tiền thành công!\"\n"
     "- Chuyển về màn danh sách chế độ Tất cả\n"
     "- Phiếu mới nằm đầu danh sách, trạng thái Đang tạo, cột Số tiền hiện 15.000.000,00\n"
     "- Mã phiếu sinh tự động dạng mã công ty + DNTT + tháng năm + 5 số"),

    ("024", "Lưu và gửi duyệt", "P0",
     "Màn Tạo mới đã điền hợp lệ như TC_04.023",
     "1. Bấm nút Lưu và gửi duyệt\n"
     "2. Đọc thông báo\n"
     "3. Tìm phiếu vừa tạo, đọc Trạng thái",
     "—",
     "- ⚠️ KHÔNG có hộp thoại xác nhận trước khi lưu\n"
     "- Thông báo: \"Phiếu đề nghị thu tiền tạo thành công! Phiếu đề nghị cần được duyệt trước khi có "
     "hiệu lực, vui lòng theo dõi thông báo\"\n"
     "- Chuyển về danh sách, phiếu ở trạng thái Chờ KT duyệt\n"
     "- Phiếu KHÔNG còn nút Sửa / Xóa"),

    ("025", "Gửi duyệt bắn thông báo cho kế toán cùng công ty", "P1",
     "NV-A thuộc công ty 3; KT-1 là kế toán thanh toán công ty 3; KT-9 là kế toán thanh toán công ty 1",
     "1. NV-A tạo phiếu và bấm Lưu và gửi duyệt\n"
     "2. Đăng nhập KT-1, mở chuông thông báo\n"
     "3. Bấm vào thông báo\n"
     "4. Đăng nhập KT-9, mở chuông thông báo",
     "Phiếu của công ty 3",
     "- KT-1 nhận thông báo nội dung \"Bạn có một phiếu đề nghị thu tiền cần duyệt từ <tên NV-A>\"\n"
     "- Bấm vào thông báo mở đúng màn chi tiết phiếu\n"
     "- KT-9 (công ty khác) KHÔNG nhận được thông báo"),

    ("026", "Nút Quay lại ở màn Tạo mới", "P2",
     "Đang ở màn Tạo mới, đã nhập dở dữ liệu",
     "1. Bấm nút Quay lại",
     "—",
     "- Về màn danh sách chế độ Tất cả\n"
     "- ⚠️ KHÔNG có cảnh báo \"thông tin chưa lưu\", dữ liệu đang nhập mất hẳn. Ghi nhận đúng hiện trạng"),

    ("027", "Bố cục màn Sửa", "P0",
     "Phiếu P trạng thái Đang tạo do chính người đăng nhập lập, 2 dòng chi tiết",
     "1. Mở menu hành động dòng phiếu P, bấm Sửa\n"
     "2. Quan sát khối Thông tin chung",
     "—",
     "- Tiêu đề trang \"Sửa đề nghị thu tiền - <mã phiếu>\"\n"
     "- Có thêm 3 ô CHỈ ĐỌC: Mã phiếu, Người tạo, Phòng ban\n"
     "- Góc phải khối hiện tên người tạo và ngày lập của phiếu\n"
     "- Bảng chi tiết nạp đủ 2 dòng cũ kèm Số tiền còn nợ và Ghi chú"),

    ("028", "Sửa phiếu và lưu lại", "P0",
     "Phiếu P trạng thái Đang tạo, 2 dòng, tổng 15.000.000; người đăng nhập CÓ quyền \"Kế toán thanh toán\"",
     "1. Đổi Lý do thu\n"
     "2. Sửa số tiền dòng 1 từ 10.000.000 thành 12.000.000\n"
     "3. Xóa dòng 2, thêm dòng mới với hợp đồng khác, số tiền 3.000.000\n"
     "4. Bấm Lưu\n"
     "5. Mở lại chi tiết phiếu P",
     "Tổng mới 15.000.000",
     "- Thông báo \"Cập nhật phiếu đề nghị thu tiền thành công!\"\n"
     "- Mở lại thấy Lý do thu mới và 2 dòng đúng như vừa sửa\n"
     "- Mã phiếu và Người tạo KHÔNG đổi"),

    ("029", "Sau khi Lưu ở màn Sửa hệ thống chuyển sang màn chờ duyệt", "P0",
     "Phiếu P trạng thái Đang tạo do NV-A lập; NV-A KHÔNG có quyền \"Kế toán thanh toán\"",
     "1. NV-A mở màn Sửa phiếu P, đổi Lý do thu\n"
     "2. Bấm Lưu\n"
     "3. Quan sát màn hình ngay sau đó\n"
     "4. Quay lại danh sách, mở chi tiết phiếu P",
     "—",
     "- ⚠️ Hiện trạng: thông báo lưu thành công rồi hệ thống chuyển sang màn \"Phiếu đề nghị thu tiền "
     "chờ duyệt\" và NV-A bị chặn vì không có quyền. Ghi nhận Failed\n"
     "- Dữ liệu ĐÃ lưu thành công (bước 4 xác nhận Lý do thu mới)\n"
     "- Kỳ vọng đúng: quay về màn danh sách như khi tạo mới"),

    ("030", "Sửa phiếu ở trạng thái Không duyệt rồi gửi duyệt lại", "P0",
     "Phiếu Q do chính người đăng nhập lập, trạng thái Không duyệt, Ghi chú duyệt đang có lý do từ chối",
     "1. Mở menu hành động, kiểm nút Sửa\n"
     "2. Bấm Sửa, đổi số tiền cho đúng\n"
     "3. Bấm Lưu và gửi duyệt\n"
     "4. Mở lại phiếu Q",
     "—",
     "- Nút Sửa CÓ hiển thị với phiếu Không duyệt\n"
     "- Sau khi lưu, phiếu chuyển sang Chờ KT duyệt\n"
     "- Kế toán cùng công ty nhận được thông báo mới"),

    ("031", "Không sửa được phiếu đã gửi duyệt qua giao diện", "P0",
     "Phiếu R do chính người đăng nhập lập, trạng thái Chờ KT duyệt",
     "1. Tìm phiếu R, mở menu hành động\n"
     "2. Mở màn chi tiết phiếu R, xem hàng nút dưới cùng",
     "Phiếu Chờ KT duyệt của chính mình",
     "- Menu hành động chỉ có In, không có Sửa và Xóa\n"
     "- Màn chi tiết cũng không có nút Sửa"),

    ("032", "Bố cục màn Chi tiết", "P0",
     "Phiếu S trạng thái Đã hạch toán, 3 dòng chi tiết, loại tiền USD; người đăng nhập KHÔNG phải kế toán",
     "1. Bấm Mã phiếu để mở chi tiết\n"
     "2. Quan sát toàn màn",
     "—",
     "- Tiêu đề trang \"Chi tiết phiếu đề nghị thu tiền\"\n"
     "- Khối Thông tin chung có: Mã phiếu, Loại thu, Loại tiền, Tỷ giá, Người tạo, Phòng ban, Lý do thu, "
     "Ngày lập, Ghi chú duyệt — TẤT CẢ đều khóa\n"
     "- Bảng chi tiết chỉ hiển thị, không có nút thêm dòng và không có nút xóa dòng\n"
     "- Dưới cùng chỉ có nút Quay lại\n"
     "- ⚠️ Màn chi tiết KHÔNG có nút In và KHÔNG có nút Sửa / Xóa"),

    ("033", "Màn chi tiết của kế toán trên phiếu chờ duyệt", "P0",
     "Tài khoản KT-1 có quyền Kế toán thanh toán; phiếu đang ở Chờ KT duyệt",
     "1. Mở chi tiết phiếu đó bằng KT-1\n"
     "2. Quan sát ô Ghi chú duyệt và hàng nút dưới cùng",
     "—",
     "- Ô \"Ghi chú duyệt\" MỞ, gõ được\n"
     "- Hàng nút có: Tạo phiếu thu, Không duyệt, Quay lại"),

    ("034", "Số tiền còn nợ trên màn chi tiết được tính lại", "P1",
     "Phiếu T lập từ tháng trước, Số tiền còn nợ lúc lập là 25.000.000; sau đó hợp đồng đã được thu thêm "
     "10.000.000",
     "1. Mở chi tiết phiếu T\n"
     "2. Đọc cột Số tiền còn nợ\n"
     "3. So với con số ghi nhận lúc lập phiếu",
     "—",
     "- Cột Số tiền còn nợ hiện 15.000.000, KHÔNG phải 25.000.000\n"
     "- ⚠️ Đúng thiết kế: số này tính lại theo sổ kế toán mỗi lần mở, không lưu trong phiếu"),

    ("035", "Phiếu có nhiều khách hàng hiển thị đúng trên chi tiết", "P0",
     "Phiếu U có 4 dòng của 4 khách hàng khác nhau",
     "1. Mở chi tiết phiếu U\n"
     "2. Đọc cột Khách hàng của cả 4 dòng",
     "4 khách hàng",
     "- Hiện đủ 4 khách hàng khác nhau, đúng từng dòng\n"
     "- Mỗi dòng gắn đúng hợp đồng của khách hàng đó"),

    ("036", "Mở màn Sửa phiếu Thu khác của dữ liệu cũ", "P2",
     "Có phiếu cũ loại Thu khác (nếu không có thì ghi Không áp dụng)",
     "1. Mở màn Sửa phiếu đó\n"
     "2. Quan sát ô Loại thu và bảng chi tiết",
     "—",
     "- Ô Loại thu KHÔNG có lựa chọn Thu khác nên hiển thị trống hoặc lệch\n"
     "- Ghi nhận đúng hiện trạng và không lưu đè lên phiếu cũ trong lúc test"),

    ("037", "Nhánh Hợp đồng nguyên tắc không kích hoạt được khi tạo mới", "P1",
     "Người đăng nhập là người lập của một Đơn hàng nguyên tắc còn hiệu lực",
     "1. Tạo phiếu Thu bán hàng, chọn khách hàng của hợp đồng nguyên tắc đó\n"
     "2. Mở cửa sổ chọn hợp đồng, chọn đúng hợp đồng nguyên tắc\n"
     "3. Quan sát dòng chi tiết",
     "Đơn hàng nguyên tắc",
     "- ⚠️ Hiện trạng: KHÔNG hiện ô tích \"Thu dư nợ đầu kỳ\" và KHÔNG hiện bảng phân bổ theo phiếu yêu "
     "cầu xuất hàng\n"
     "- Dòng chi tiết chỉ có mã hợp đồng và Số tiền còn nợ như hợp đồng thường\n"
     "- Ghi nhận là hiện trạng đã biết (mục 9 ghi chú 10), không phải lỗi mới phát sinh"),
]

SEC_V = [
    ("001", "Kế toán mở phiếu từ màn chờ duyệt", "P0",
     "KT-1 có quyền Kế toán thanh toán; công ty có phiếu mã kết thúc .00021 trạng thái Chờ KT duyệt",
     "1. Mở màn Phiếu đề nghị thu tiền chờ duyệt\n"
     "2. Bấm Mã phiếu .00021\n"
     "3. Quan sát hàng nút dưới cùng",
     "Phiếu .00021",
     "- Mở được chi tiết\n"
     "- Hàng nút có: Tạo phiếu thu, Không duyệt, Quay lại\n"
     "- Ô Ghi chú duyệt mở, gõ được"),

    ("002", "Bấm Không duyệt hiện hộp thoại xác nhận", "P0",
     "Đang ở màn chi tiết phiếu chờ duyệt bằng tài khoản kế toán, đã nhập Ghi chú duyệt \"Sai số tiền\"",
     "1. Bấm nút Không duyệt\n"
     "2. Đọc hộp thoại\n"
     "3. Bấm Hủy\n"
     "4. Kiểm trạng thái phiếu",
     "Ghi chú duyệt: Sai số tiền",
     "- Hộp thoại tiêu đề \"Xác nhận!\", nội dung \"Bạn chắc chắn muốn thực hiện hành động này?\", có 2 "
     "nút Xác nhận và Hủy\n"
     "- Bấm Hủy: đóng hộp thoại, trạng thái phiếu KHÔNG đổi, Ghi chú duyệt vẫn còn trên màn"),

    ("003", "Không duyệt thành công", "P0",
     "Vẫn phiếu ở TC_05.002, Ghi chú duyệt đã nhập",
     "1. Bấm Không duyệt, bấm Xác nhận\n"
     "2. Đọc thông báo và quan sát trang chuyển tới\n"
     "3. Mở lại chi tiết phiếu",
     "Ghi chú duyệt: Sai số tiền, đề nghị lập lại",
     "- Hiện thông báo xanh báo thao tác thành công\n"
     "- Hệ thống chuyển về màn Phiếu đề nghị thu tiền chờ duyệt\n"
     "- Phiếu KHÔNG còn trong màn chờ duyệt\n"
     "- Mở lại chi tiết: trạng thái Không duyệt, ô Ghi chú duyệt hiện đúng lý do vừa nhập"),

    ("004", "Không duyệt khi Ghi chú duyệt để trống", "P0",
     "Phiếu chờ duyệt, tài khoản kế toán, ô Ghi chú duyệt để TRỐNG",
     "1. Bấm nút Không duyệt\n"
     "2. Bấm Xác nhận trên hộp thoại\n"
     "3. Quan sát",
     "Ghi chú duyệt: để trống",
     "- ⚠️ Hộp thoại xác nhận VẪN hiện ra trước, chỉ sau khi Xác nhận mới báo lỗi\n"
     "- Hệ thống chặn, hiện lỗi đỏ ngay dưới ô Ghi chú duyệt\n"
     "- Trạng thái phiếu KHÔNG đổi"),

    ("005", "Người lập sửa lại phiếu bị không duyệt", "P0",
     "Phiếu .00021 trạng thái Không duyệt, do NV-A lập",
     "1. Đăng nhập NV-A, tìm phiếu .00021\n"
     "2. Bấm Sửa, quan sát ô Ghi chú duyệt trên form\n"
     "3. Sửa số tiền, bấm Lưu và gửi duyệt\n"
     "4. Đăng nhập KT-1, mở màn chờ duyệt",
     "—",
     "- NV-A sửa được\n"
     "- ⚠️ Màn Sửa KHÔNG hiện ô Ghi chú duyệt, người lập không đọc được lý do bị từ chối ngay trên form — "
     "phải mở màn chi tiết mới xem được. Ghi nhận là điểm bất tiện\n"
     "- Sau khi gửi duyệt lại, phiếu trở về Chờ KT duyệt và xuất hiện lại trên màn chờ duyệt của KT-1"),

    ("006", "Nút Tạo phiếu thu chuyển sang màn Phiếu thu", "P0",
     "KT-1; phiếu .00022 đang Chờ KT duyệt",
     "1. Mở chi tiết phiếu .00022\n"
     "2. Bấm nút Tạo phiếu thu\n"
     "3. Quan sát màn mở ra\n"
     "4. Quay lại kiểm trạng thái phiếu .00022",
     "—",
     "- Chuyển sang màn tạo Phiếu thu, phiếu đề nghị .00022 đã được gắn sẵn\n"
     "- Trạng thái phiếu đề nghị CHƯA đổi ở bước này (vẫn Chờ KT duyệt)"),

    ("007", "Thao tác Tạo phiếu thu ngay từ danh sách", "P1",
     "KT-1 ở màn chờ duyệt, có phiếu Chờ KT duyệt",
     "1. Mở menu hành động của dòng phiếu\n"
     "2. Bấm mục Tạo phiếu thu",
     "—",
     "- Menu có mục Tạo phiếu thu\n"
     "- Bấm vào chuyển đúng sang màn tạo Phiếu thu kèm sẵn phiếu đề nghị của dòng đó"),

    ("008", "Người không phải kế toán không thấy nút xử lý", "P0",
     "NV-A không có quyền Kế toán thanh toán; phiếu Chờ KT duyệt trong phạm vi NV-A xem được",
     "1. Mở chi tiết phiếu đó bằng NV-A\n"
     "2. Quan sát hàng nút và ô Ghi chú duyệt\n"
     "3. Mở menu hành động của dòng đó ngoài danh sách",
     "—",
     "- Chỉ có nút Quay lại\n"
     "- Ô Ghi chú duyệt bị KHÓA\n"
     "- Menu hành động chỉ có In, không có Tạo phiếu thu"),

    ("009", "Phiếu ở trạng thái cuối không còn thao tác xử lý", "P1",
     "Phiếu Đã hạch toán và phiếu Hủy",
     "1. Mở chi tiết từng phiếu bằng tài khoản kế toán\n"
     "2. Quan sát hàng nút\n"
     "3. Mở menu hành động ngoài danh sách",
     "Đã hạch toán, Hủy",
     "- Màn chi tiết chỉ có nút Quay lại\n"
     "- Menu hành động chỉ có In\n"
     "- Không có Không duyệt, không có Tạo phiếu thu"),

    ("010", "Không duyệt không làm mất dòng chi tiết", "P1",
     "Phiếu có 3 dòng chi tiết, đang Chờ KT duyệt",
     "1. Kế toán nhập Ghi chú duyệt và bấm Không duyệt\n"
     "2. Mở lại chi tiết, đếm dòng và đọc số tiền từng dòng",
     "3 dòng chi tiết",
     "- Vẫn đủ 3 dòng, số tiền từng dòng không đổi\n"
     "- Tổng tiền ngoài danh sách không đổi"),

    ("011", "Sửa lại phiếu đang chờ duyệt bắn thông báo thêm một lần", "P1",
     "Phiếu đang ở Chờ KT duyệt; dùng công cụ kiểm thử API gọi thẳng chức năng Sửa, giữ nguyên trạng thái "
     "Chờ KT duyệt",
     "1. Ghi lại số thông báo hiện có của kế toán cùng công ty\n"
     "2. Gọi chức năng Sửa với trạng thái vẫn là Chờ KT duyệt\n"
     "3. Kiểm chuông thông báo của kế toán",
     "—",
     "- ⚠️ Hiện trạng: kế toán nhận THÊM một thông báo nữa dù phiếu không chuyển trạng thái. Ghi nhận là "
     "điểm gây nhiễu\n"
     "- Kỳ vọng đúng: chỉ bắn thông báo khi phiếu CHUYỂN TỪ nháp sang chờ duyệt"),

    ("012", "Màn chờ duyệt cập nhật khi có phiếu mới gửi lên", "P1",
     "KT-1 đang mở màn chờ duyệt thấy 4 phiếu; NV-A cùng công ty vừa gửi duyệt 1 phiếu",
     "1. Bấm nút làm mới bộ lọc hoặc tải lại trang\n"
     "2. Đọc lại số tổng",
     "—",
     "- Số phiếu tăng thành 5\n"
     "- Phiếu mới nằm đầu danh sách"),
]

SEC_VI = [
    ("001", "Xóa phiếu nháp từ danh sách", "P0",
     "Phiếu T trạng thái Đang tạo do chính người đăng nhập lập, 2 dòng chi tiết",
     "1. Mở menu hành động dòng phiếu T, bấm Xóa\n"
     "2. Đọc hộp thoại\n"
     "3. Bấm Xác nhận\n"
     "4. Quan sát danh sách",
     "Phiếu T",
     "- Hộp thoại tiêu đề \"Xác nhận xóa!\", nội dung \"Bạn chắc chắn muốn xóa bản ghi này?\"\n"
     "- Bấm Xác nhận: hiện thông báo xanh \"Xóa phiếu đề nghị thu thành công!\"\n"
     "- Phiếu T biến mất khỏi danh sách, tổng giảm 1"),

    ("002", "Hủy hộp thoại xác nhận xóa", "P0",
     "Phiếu T trạng thái Đang tạo",
     "1. Bấm Xóa ở dòng phiếu T\n"
     "2. Bấm nút Hủy\n"
     "3. Quan sát danh sách",
     "—",
     "- Hộp thoại đóng\n"
     "- Phiếu T còn nguyên, tổng không đổi"),

    ("003", "Xóa phiếu ở trạng thái Không duyệt", "P0",
     "Phiếu U trạng thái Không duyệt do chính người đăng nhập lập",
     "1. Mở menu hành động, bấm Xóa, xác nhận\n"
     "2. Tìm lại phiếu U bằng ô Mã phiếu",
     "Phiếu U",
     "- Xóa thành công, thông báo xanh\n"
     "- Tìm lại không ra dòng nào"),

    ("004", "Xóa phiếu là xóa theo toàn bộ dòng chi tiết", "P1",
     "Phiếu V trạng thái Đang tạo, 4 dòng chi tiết gắn 4 hợp đồng",
     "1. Xóa phiếu V\n"
     "2. Tạo phiếu mới, chọn lại đúng 4 hợp đồng của phiếu V",
     "4 dòng chi tiết",
     "- Xóa thành công\n"
     "- 4 hợp đồng chọn lại được bình thường, không bị báo đã tồn tại\n"
     "- Không còn dòng chi tiết mồ côi của phiếu đã xóa"),

    ("005", "Menu không có nút Xóa với phiếu đã gửi duyệt hoặc đã xử lý", "P0",
     "4 phiếu ở 4 trạng thái Chờ KT duyệt, Đã tạo phiếu thu, Đã hạch toán, Hủy — đều do chính người "
     "đăng nhập lập",
     "1. Mở menu hành động của từng phiếu",
     "4 trạng thái",
     "- Cả 4 phiếu đều KHÔNG có mục Xóa và không có mục Sửa\n"
     "- Chỉ còn mục In"),

    ("006", "Xóa được phiếu đã hạch toán bằng đường dẫn trực tiếp", "P0",
     "Phiếu trạng thái Đã hạch toán; đã sao lưu dữ liệu trước khi test",
     "1. Lấy đường dẫn xóa của phiếu đó (thay số phiếu vào đường dẫn xóa của một phiếu nháp)\n"
     "2. Dán vào thanh địa chỉ\n"
     "3. Kiểm tra phiếu còn hay mất",
     "Phiếu Đã hạch toán",
     "- ⚠️ Hiện trạng: phiếu BỊ XÓA, hệ thống báo xóa thành công dù trạng thái không cho phép. LỖ HỔNG, "
     "ghi nhận Failed\n"
     "- Kỳ vọng đúng: từ chối và giữ nguyên phiếu\n"
     "- Khôi phục dữ liệu ngay sau khi test"),

    ("007", "Xóa phiếu xong quay lại đúng trang trước đó", "P2",
     "Đang ở trang 2 của danh sách, lọc Trạng thái = Đang tạo",
     "1. Xóa 1 phiếu ở trang 2\n"
     "2. Quan sát trang hiện ra sau khi xóa",
     "—",
     "- Quay lại màn danh sách kèm thông báo xanh\n"
     "- Ghi nhận thực tế trang và bộ lọc có được giữ hay không"),
]

SEC_VII = [
    ("001", "In phiếu từ menu hành động", "P0",
     "Danh sách đang có phiếu Thu bán hàng loại tiền VND",
     "1. Mở menu hành động của dòng, bấm In\n"
     "2. Quan sát trang mở ra",
     "—",
     "- Mở trang bản in của đúng phiếu đó\n"
     "- Bản in dựng theo mẫu Phiếu đề nghị thu tiền bán hàng"),

    ("002", "Nội dung khối đầu bản in", "P0",
     "Phiếu Thu bán hàng, VND, có Ghi chú duyệt",
     "1. Mở bản in\n"
     "2. Đọc từ trên xuống",
     "—",
     "- Trên cùng là phần đầu trang của công ty người lập\n"
     "- Có: Số phiếu, Ngày / Tháng / Năm lập, Người đề nghị, Phòng ban, Lý do thu, Diễn giải (lấy từ "
     "Ghi chú duyệt)\n"
     "- Mọi thông tin khớp với màn chi tiết"),

    ("003", "Bảng chi tiết trên bản in phiếu VND", "P0",
     "Phiếu Thu bán hàng VND, 3 dòng, tổng đề nghị thu 17.000.000, tổng còn nợ 40.000.000",
     "1. Mở bản in\n"
     "2. Đọc tiêu đề cột, các dòng và dòng Tổng cộng\n"
     "3. Đọc dòng Bằng chữ",
     "3 dòng chi tiết",
     "- 6 cột: STT, Khách hàng, Số đơn hàng/Hợp đồng, Số tiền còn nợ, Số tiền đề nghị thu, Ghi chú\n"
     "- Đủ 3 dòng, cột Khách hàng hiện TÊN khách hàng (không có mã)\n"
     "- Dòng Tổng cộng: 40.000.000 và 17.000.000\n"
     "- Dòng \"Bằng chữ\" đọc đúng số 17.000.000, kết thúc bằng chữ đồng"),

    ("004", "Bản in phiếu Thu nhà cung cấp đổi tiêu đề cột", "P1",
     "Phiếu Thu nhà cung cấp, VND",
     "1. Mở bản in\n"
     "2. Đọc tiêu đề cột 2 và cột 3",
     "—",
     "- Cột 2 là \"Nhà cung cấp\", cột 3 là \"Hợp đồng mua\"\n"
     "- Nội dung cột 2 hiện tên nhà cung cấp\n"
     "- Bản in dựng theo mẫu Phiếu đề nghị thu tiền nhà cung cấp"),

    ("005", "Bản in phiếu ngoại tệ tách 2 cột tiền", "P0",
     "Phiếu Thu bán hàng loại tiền USD, tỷ giá lưu trong phiếu 25.000, 1 dòng 1.000 USD",
     "1. Mở bản in\n"
     "2. Đọc tiêu đề nhóm cột Số tiền đề nghị thu\n"
     "3. Đọc dòng dữ liệu và dòng Tổng cộng\n"
     "4. Đọc dòng Tỷ giá",
     "USD 1.000, tỷ giá 25.000",
     "- Nhóm \"Số tiền đề nghị thu\" tách 2 cột con: USD và VND\n"
     "- Dòng dữ liệu: cột USD hiện 1.000, cột VND hiện 25.000.000\n"
     "- Tổng cộng có đủ 3 số: tổng còn nợ, tổng nguyên tệ, tổng quy đổi\n"
     "- Bản in có dòng Tỷ giá"),

    ("006", "Tỷ giá trên bản in lấy từ danh mục chứ không phải từ phiếu", "P0",
     "Phiếu W loại tiền USD lập lúc tỷ giá 25.000; sau đó danh mục tiền tệ đổi tỷ giá USD thành 26.000",
     "1. Mở màn chi tiết phiếu W, đọc ô Tỷ giá\n"
     "2. Mở bản in của phiếu W, đọc dòng Tỷ giá\n"
     "3. Đọc cột VND của các dòng trên bản in",
     "Tỷ giá phiếu 25.000, danh mục hiện tại 26.000",
     "- ⚠️ Hiện trạng: màn chi tiết hiện 25.000 nhưng bản in hiện 26.000 — hai chỗ LỆCH nhau. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: bản in dùng tỷ giá đã lưu trong phiếu\n"
     "- Cột VND trên bản in vẫn lấy số quy đổi đã lưu trong phiếu, nên bản in tự mâu thuẫn với dòng Tỷ giá"),

    ("007", "Số tiền còn nợ trên bản in được tính lại", "P1",
     "Phiếu lập từ tháng trước, Số tiền còn nợ lúc lập 25.000.000; hợp đồng đã thu thêm 10.000.000",
     "1. Mở bản in của phiếu đó\n"
     "2. Đọc cột Số tiền còn nợ",
     "—",
     "- Hiện 15.000.000, không phải 25.000.000\n"
     "- ⚠️ Đúng thiết kế (mục 9 ghi chú 8), không ghi Failed"),

    ("008", "In phiếu mà một dòng có hợp đồng không xác định", "P2",
     "Phiếu cũ có dòng chi tiết trỏ tới loại hợp đồng hệ thống không nhận diện được",
     "1. Mở bản in của phiếu đó",
     "—",
     "- Bản in VẪN hiện ra, không trắng trang và không báo lỗi\n"
     "- Dòng đó hiện Số tiền còn nợ bằng 0"),

    ("009", "Bốn mẫu in ứng với bốn tổ hợp loại thu và loại tiền", "P1",
     "4 phiếu: (Thu bán hàng + VND), (Thu bán hàng + USD), (Thu nhà cung cấp + VND), (Thu nhà cung cấp + USD)",
     "1. Mở bản in của lần lượt 4 phiếu\n"
     "2. So bố cục và tiêu đề cột",
     "4 tổ hợp",
     "- Mỗi tổ hợp dùng một mẫu riêng, đúng tiêu đề cột và đúng có / không có cột quy đổi\n"
     "- Không tổ hợp nào báo lỗi thiếu mẫu in"),
]

SEC_VIII = [
    ("001", "Lưu khi để trống Lý do thu", "P0",
     "Màn Tạo mới, đã có 1 dòng chi tiết hợp lệ, để trống Lý do thu",
     "1. Bấm Lưu\n"
     "2. Quan sát",
     "Lý do thu: để trống",
     "- Không lưu\n"
     "- Lỗi đỏ \"Bắt buộc nhập\" hiện ngay dưới ô Lý do thu\n"
     "- Ở lại form, dữ liệu đã nhập còn nguyên"),

    ("002", "Lưu khi để trống Loại thu", "P0",
     "Màn Tạo mới, chưa chọn Loại thu, đã điền Lý do thu",
     "1. Bấm Lưu\n"
     "2. Quan sát",
     "Loại thu: để trống",
     "- Không lưu\n"
     "- Lỗi đỏ \"Bắt buộc nhập\" dưới ô Loại thu\n"
     "- Ngoài ra còn báo lỗi ở phần Chi tiết vì chưa có dòng nào"),

    ("003", "Lưu khi để trống Loại tiền hoặc Tỷ giá", "P0",
     "Màn Tạo mới, đã điền các ô khác hợp lệ",
     "1. Xóa lựa chọn ở ô Loại tiền, bấm Lưu, quan sát\n"
     "2. Chọn lại Loại tiền là USD, xóa sạch ô Tỷ giá, bấm Lưu",
     "Loại tiền trống, rồi Tỷ giá trống",
     "- Cả 2 lần đều không lưu\n"
     "- Lỗi đỏ \"Bắt buộc nhập\" hiện đúng dưới ô đang thiếu"),

    ("004", "Lưu khi bảng chi tiết không có dòng nào", "P0",
     "Màn Tạo mới, đã chọn Loại thu rồi xóa hết dòng chi tiết, đã điền Lý do thu",
     "1. Bấm Lưu\n"
     "2. Quan sát dưới bảng chi tiết",
     "0 dòng chi tiết",
     "- Không lưu\n"
     "- Lỗi đỏ \"Bắt buộc nhập\" hiện ngay dưới bảng chi tiết"),

    ("005", "Lưu khi dòng chi tiết chưa chọn khách hàng", "P0",
     "Màn Tạo mới, Lý do thu đã điền, có 1 dòng trống hoàn toàn",
     "1. Bấm Lưu\n"
     "2. Quan sát dòng chi tiết",
     "Dòng 1 trống",
     "- Không lưu\n"
     "- Ô Khách hàng của dòng 1 có lỗi đỏ \"Bắt buộc nhập\"\n"
     "- Ô Số đơn hàng/Hợp đồng cũng có lỗi đỏ \"Bắt buộc nhập\""),

    ("006", "Lưu khi dòng đã chọn khách hàng nhưng chưa chọn hợp đồng", "P0",
     "1 dòng đã chọn khách hàng, chưa chọn hợp đồng, số tiền 5.000.000",
     "1. Bấm Lưu\n"
     "2. Quan sát",
     "—",
     "- Không lưu\n"
     "- Chỉ ô Số đơn hàng/Hợp đồng báo lỗi; ô Khách hàng không báo lỗi"),

    ("007", "Lưu phiếu Thu nhà cung cấp khi chưa chọn nhà cung cấp", "P0",
     "Loại thu = Thu nhà cung cấp, 1 dòng trống, Lý do thu đã điền",
     "1. Bấm Lưu\n"
     "2. Quan sát dòng chi tiết",
     "—",
     "- Không lưu\n"
     "- Ô Nhà cung cấp báo lỗi đỏ \"Bắt buộc nhập\""),

    ("008", "Lỗi báo đúng dòng khi có nhiều dòng", "P0",
     "3 dòng: dòng 1 và 3 đầy đủ, dòng 2 thiếu hợp đồng",
     "1. Bấm Lưu\n"
     "2. Quan sát cả 3 dòng",
     "Dòng 2 thiếu hợp đồng",
     "- Chỉ DÒNG 2 hiện lỗi đỏ, dòng 1 và 3 sạch\n"
     "- ⚠️ Kiểm kỹ lỗi có gắn đúng dòng không, đây là chỗ dễ lệch"),

    ("009", "Số tiền đề nghị thu bằng 0 vẫn lưu được", "P1",
     "1 dòng đủ khách hàng và hợp đồng, để Số tiền đề nghị thu = 0",
     "1. Bấm Lưu\n"
     "2. Tìm phiếu vừa lưu trong danh sách",
     "Số tiền đề nghị thu: 0",
     "- Lưu được, không báo lỗi\n"
     "- Cột Số tiền ngoài danh sách hiện 0,00"),

    ("010", "Số tiền đề nghị thu âm bị chặn", "P0",
     "1 dòng đủ khách hàng và hợp đồng",
     "1. Gõ dấu trừ rồi số vào ô Số tiền đề nghị thu\n"
     "2. Bấm Lưu",
     "Số tiền: -1.000.000",
     "- Nếu ô nhận số âm thì khi Lưu hệ thống báo lỗi đỏ ở dòng đó\n"
     "- Không tạo được phiếu có số tiền âm"),

    ("011", "Ô Số tiền chỉ nhận số và tự thêm dấu ngăn nghìn", "P1",
     "Đang ở dòng chi tiết",
     "1. Gõ chữ cái vào ô Số tiền đề nghị thu\n"
     "2. Gõ 12000000, rời ô\n"
     "3. Quan sát cột quy đổi và dòng Tổng cộng",
     "Nhập chữ, rồi 12000000",
     "- Chữ cái không được nhận\n"
     "- Số hiện thành 12.000.000\n"
     "- Cột quy đổi và dòng Tổng cộng cập nhật theo"),

    ("012", "Số tiền có phần thập phân", "P2",
     "1 dòng đủ khách hàng và hợp đồng",
     "1. Nhập Số tiền đề nghị thu = 1.234.567,89\n"
     "2. Bấm Lưu\n"
     "3. Xem cột Số tiền ngoài danh sách và mở lại chi tiết",
     "1.234.567,89",
     "- Lưu được, giữ nguyên phần thập phân\n"
     "- Cột Số tiền ngoài danh sách hiện 1.234.567,89"),

    ("013", "Tỷ giá nhận số thập phân", "P2",
     "Loại tiền JPY, ô Tỷ giá mở",
     "1. Nhập tỷ giá 168,5\n"
     "2. Nhập 1 dòng số tiền 1.000\n"
     "3. Đọc cột quy đổi VND, bấm Lưu rồi mở lại",
     "Tỷ giá 168,5 · 1.000 JPY",
     "- Cột quy đổi hiện 168.500\n"
     "- Lưu được, mở lại tỷ giá vẫn là 168,5"),

    ("014", "Lý do thu và Ghi chú dòng nhận chuỗi dài có dấu tiếng Việt", "P2",
     "Màn Tạo mới hợp lệ",
     "1. Nhập Lý do thu dài khoảng 200 ký tự có dấu\n"
     "2. Nhập Ghi chú dòng khoảng 200 ký tự có dấu\n"
     "3. Lưu rồi mở lại chi tiết",
     "Chuỗi dài có dấu",
     "- Lưu được, không cắt chữ, không lỗi font\n"
     "- Cột Lý do nộp ngoài danh sách hiển thị đầy đủ hoặc rút gọn nhưng không vỡ bố cục"),

    ("015", "Ghi chú của từng dòng lưu đúng dòng", "P1",
     "3 dòng chi tiết",
     "1. Nhập Ghi chú dòng 1 = \"Đợt 1\", dòng 2 = \"Đợt 2\", dòng 3 để trống\n"
     "2. Lưu, mở lại chi tiết",
     "Đợt 1 / Đợt 2 / trống",
     "- Ghi chú gắn đúng từng dòng, không lệch\n"
     "- Dòng 3 để trống"),

    ("016", "Bỏ qua giao diện gửi lên Loại thu không hợp lệ", "P1",
     "Tài khoản bất kỳ; dùng công cụ kiểm thử API",
     "1. Gọi thẳng chức năng Tạo phiếu, gửi Loại thu = 99\n"
     "2. Quan sát kết quả và danh sách phiếu",
     "Loại thu: 99",
     "- ⚠️ Hiện trạng: hệ thống chỉ kiểm tra Loại thu phải là số, nên phiếu Loại thu 99 TẠO ĐƯỢC và "
     "hiện trong danh sách với cột Loại thu để trống. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: chỉ nhận Thu bán hàng hoặc Thu nhà cung cấp"),

    ("017", "Bỏ qua giao diện gửi lên trạng thái tùy ý khi tạo phiếu", "P0",
     "Tài khoản bất kỳ; dùng công cụ kiểm thử API",
     "1. Gọi thẳng chức năng Tạo phiếu với trạng thái là Đã hạch toán\n"
     "2. Tìm phiếu vừa tạo trong danh sách, đọc Trạng thái",
     "Trạng thái gửi lên: Đã hạch toán",
     "- ⚠️ Hiện trạng: phiếu được tạo NGAY ở trạng thái Đã hạch toán, bỏ qua toàn bộ luồng duyệt. LỖ "
     "HỔNG, ghi nhận Failed\n"
     "- Kỳ vọng đúng: khi tạo chỉ cho 2 trạng thái Đang tạo hoặc Chờ KT duyệt"),

    ("018", "Bỏ qua giao diện gửi lên loại hợp đồng bịa", "P1",
     "Tài khoản bất kỳ; dùng công cụ kiểm thử API",
     "1. Gọi thẳng chức năng Tạo phiếu, gửi dòng chi tiết có loại hợp đồng là chuỗi bịa\n"
     "2. Tìm phiếu vừa tạo, mở màn chi tiết và mở bản in",
     "Loại hợp đồng: chuỗi bịa",
     "- ⚠️ Hiện trạng: phiếu tạo được; mở chi tiết thì ô hợp đồng trống, Số tiền còn nợ bằng 0. Ghi "
     "nhận Failed\n"
     "- Kỳ vọng đúng: chặn ngay khi lưu vì loại hợp đồng không hợp lệ"),
]

SEC_IX = [
    ("001", "Hai người cùng lập phiếu tại một thời điểm", "P0",
     "2 tài khoản cùng công ty, cùng chuẩn bị sẵn form Tạo mới hợp lệ",
     "1. Cả 2 bấm Lưu gần như cùng lúc\n"
     "2. Đối chiếu mã của 2 phiếu vừa tạo\n"
     "3. Lặp lại 3 lần để tăng khả năng va chạm",
     "2 phiếu tạo đồng thời",
     "- Cả 2 phiếu đều lưu thành công\n"
     "- ⚠️ Mã phiếu sinh không có khóa chống va chạm: nếu 2 phiếu ra TRÙNG mã thì ghi Failed kèm ảnh "
     "chụp; nếu 2 mã liên tiếp thì đạt"),

    ("002", "Hai người ở hai công ty lập phiếu có tiền tố mã khác nhau", "P1",
     "Tài khoản công ty A và tài khoản công ty B",
     "1. Mỗi người lập 1 phiếu nháp\n"
     "2. Đọc mã 2 phiếu",
     "—",
     "- Tiền tố mã công ty khác nhau\n"
     "- Phần 5 số đếm riêng theo từng tiền tố và theo từng tháng"),

    ("003", "Tài khoản chưa gắn hồ sơ nhân sự lập phiếu", "P1",
     "Tài khoản đăng nhập được nhưng chưa gắn công ty / phòng ban trong hồ sơ nhân sự",
     "1. Mở màn Tạo mới, điền hợp lệ\n"
     "2. Bấm Lưu\n"
     "3. Quan sát thông báo và kiểm tra phiếu có được tạo không",
     "—",
     "- Ghi nhận đúng hiện trạng: hệ thống báo lỗi hay tạo được phiếu thiếu công ty\n"
     "- ⚠️ Nếu phiếu tạo được nhưng thiếu công ty thì nó lọt khỏi mọi bộ lọc theo cấp — ghi nhận Failed"),

    ("004", "Sửa phiếu đã bị người khác đổi trạng thái", "P0",
     "Mở 2 tab: tab 1 là màn Sửa phiếu nháp của NV-A đang mở dở; tab 2 dùng NV-A gửi duyệt chính phiếu đó",
     "1. Ở tab 2, mở phiếu và gửi duyệt\n"
     "2. Quay lại tab 1, sửa Lý do thu rồi bấm Lưu\n"
     "3. Mở lại phiếu, đọc Trạng thái và Lý do thu",
     "—",
     "- ⚠️ Hiện trạng: tab 1 lưu ĐÈ được, phiếu quay lại trạng thái Đang tạo và mất trạng thái Chờ KT "
     "duyệt. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: chặn lưu vì phiếu đã rời trạng thái cho phép sửa"),

    ("005", "Hai kế toán cùng không duyệt một phiếu", "P0",
     "2 tài khoản kế toán cùng công ty, cùng mở chi tiết một phiếu Chờ KT duyệt",
     "1. Kế toán 1 nhập Ghi chú duyệt, bấm Không duyệt, xác nhận\n"
     "2. Kế toán 2 (chưa tải lại) nhập Ghi chú duyệt khác, bấm Không duyệt, xác nhận\n"
     "3. Mở lại phiếu, đọc Ghi chú duyệt",
     "—",
     "- ⚠️ Hiện trạng: kế toán 2 vẫn thực hiện được, Ghi chú duyệt của kế toán 1 bị GHI ĐÈ. Ghi nhận "
     "Failed\n"
     "- Kỳ vọng đúng: báo phiếu không còn ở trạng thái chờ duyệt và giữ nguyên kết quả của người xử lý "
     "trước"),

    ("006", "Phạm vi dữ liệu không rò rỉ giữa các công ty", "P0",
     "Tài khoản chỉ có quyền xem theo công ty, thuộc công ty 3",
     "1. Lọc Số đơn hàng/hợp đồng bằng mã hợp đồng của một khách hàng công ty 1\n"
     "2. Lọc Khách hàng bằng một khách hàng chỉ có ở công ty 1\n"
     "3. Nhập khoảng tiền rất rộng từ 0 đến 999.999.999.999",
     "—",
     "- Cả 3 cách đều không làm lộ phiếu của công ty 1\n"
     "- Tổng luôn nằm trong phạm vi công ty 3"),

    ("007", "Xóa phiếu xong danh sách nạp lại đúng số tổng", "P1",
     "Đang lọc Trạng thái = Đang tạo, có 5 phiếu",
     "1. Xóa 1 phiếu\n"
     "2. Đọc lại số tổng và các ô lọc",
     "—",
     "- Tổng còn 4\n"
     "- Ghi nhận thực tế bộ lọc Trạng thái có được giữ lại hay không"),

    ("008", "Đổi tỷ giá trong danh mục không làm đổi phiếu đã lưu", "P1",
     "Phiếu W ngoại tệ đã lưu với tỷ giá 25.000; sau đó danh mục đổi tỷ giá USD thành 26.000",
     "1. Mở màn chi tiết phiếu W, đọc Tỷ giá, cột quy đổi và cột Số tiền ngoài danh sách\n"
     "2. So với số lúc lập phiếu",
     "—",
     "- Tỷ giá và số quy đổi trong phiếu GIỮ NGUYÊN theo lúc lập\n"
     "- Cột Số tiền ngoài danh sách cũng không đổi\n"
     "- ⚠️ Chỉ riêng BẢN IN bị lệch — xem TC_07.006"),

    ("009", "Mở màn Sửa phiếu của nhân sự không còn phòng ban", "P2",
     "Phiếu do một nhân viên đã bị gỡ khỏi phòng ban lập",
     "1. Mở màn Sửa hoặc màn Chi tiết phiếu đó",
     "—",
     "- Ghi nhận đúng hiện trạng: màn mở được với ô Phòng ban trống, hay hệ thống báo lỗi trang\n"
     "- Nếu báo lỗi trang thì ghi Failed"),
]

SEC_X = [
    ("001", "Vòng đời đầy đủ: lập nháp - sửa - gửi duyệt - không duyệt - sửa lại - gửi lại", "P0",
     "NV-A thuộc công ty 3, là người lập của ít nhất 2 hợp đồng còn hiệu lực của KH-001; KT-1 là kế toán "
     "thanh toán công ty 3",
     "1. NV-A tạo phiếu Thu bán hàng, 2 dòng của KH-001, tổng 15.000.000, bấm Lưu\n"
     "2. NV-A mở lại phiếu bằng nút Sửa, đổi số tiền dòng 1 thành 12.000.000, bấm Lưu\n"
     "3. NV-A mở lại phiếu, bấm Lưu và gửi duyệt\n"
     "4. KT-1 mở màn chờ duyệt, mở phiếu, nhập Ghi chú duyệt \"Sai hợp đồng\", bấm Không duyệt, xác nhận\n"
     "5. NV-A mở lại phiếu, đổi hợp đồng dòng 1, bấm Lưu và gửi duyệt\n"
     "6. KT-1 mở lại màn chờ duyệt",
     "Toàn bộ vòng đời một phiếu",
     "- Bước 1: trạng thái Đang tạo, chỉ NV-A nhìn thấy ở chế độ Tất cả\n"
     "- Bước 2: sửa được; ⚠️ sau khi Lưu, NV-A bị đẩy sang màn chờ duyệt và bị chặn quyền (TC_04.029) — "
     "dữ liệu vẫn lưu\n"
     "- Bước 3: trạng thái Chờ KT duyệt, nút Sửa và Xóa biến mất, KT-1 nhận thông báo\n"
     "- Bước 4: trạng thái Không duyệt, Ghi chú duyệt lưu đúng lý do, phiếu rời màn chờ duyệt\n"
     "- Bước 5: sửa lại được, quay về Chờ KT duyệt\n"
     "- Bước 6: phiếu xuất hiện lại trên màn chờ duyệt"),

    ("002", "Vòng đời phiếu Thu nhà cung cấp", "P0",
     "NV-A; nhà cung cấp NCC-01 có ít nhất 2 hợp đồng mua đủ điều kiện (kể cả do người khác lập)",
     "1. Tạo phiếu, đổi Loại thu = Thu nhà cung cấp\n"
     "2. Thêm 2 dòng, mỗi dòng chọn NCC-01 và một hợp đồng mua khác nhau\n"
     "3. Nhập số tiền, bấm Lưu và gửi duyệt\n"
     "4. Xem danh sách, xem chi tiết, mở bản in",
     "2 dòng, cùng nhà cung cấp",
     "- Bảng chi tiết dùng tiêu đề \"Nhà cung cấp\" và \"Hợp đồng mua\"\n"
     "- Cửa sổ hợp đồng mua hiện cả hợp đồng do người khác lập\n"
     "- Ngoài danh sách cột đối tượng hiện mã và tên nhà cung cấp\n"
     "- Bản in dùng mẫu Phiếu đề nghị thu tiền nhà cung cấp\n"
     "- Số tiền còn nợ lấy theo tài khoản Phải trả nhà cung cấp"),

    ("003", "Vòng đời phiếu ngoại tệ", "P0",
     "NV-A; danh mục có USD tỷ giá 25.000",
     "1. Tạo phiếu Thu bán hàng, đổi Loại tiền sang USD\n"
     "2. Thêm 2 dòng, mỗi dòng 1.000 USD\n"
     "3. Bấm Lưu\n"
     "4. Xem cột Số tiền ngoài danh sách, xem chi tiết, xem bản in\n"
     "5. Lọc khoảng tiền từ 40.000.000 đến 60.000.000",
     "USD, tỷ giá 25.000, 2 dòng x 1.000",
     "- Bảng chi tiết tách 2 cột USD và VND, mỗi dòng cột VND hiện 25.000.000\n"
     "- Cột Số tiền ngoài danh sách hiện 50.000.000,00\n"
     "- Bản in tách 2 cột tiền, tổng quy đổi 50.000.000, dòng Bằng chữ đọc theo 50.000.000\n"
     "- Bộ lọc khoảng tiền TÌM RA phiếu này"),

    ("004", "Phiếu gom nhiều khách hàng trong cùng một phiếu", "P0",
     "NV-A là người lập của hợp đồng còn hiệu lực của 3 khách hàng khác nhau",
     "1. Tạo phiếu Thu bán hàng, thêm 3 dòng\n"
     "2. Mỗi dòng chọn một khách hàng khác nhau và hợp đồng của chính khách hàng đó\n"
     "3. Nhập số tiền từng dòng, bấm Lưu\n"
     "4. Xem danh sách, xem chi tiết, lọc theo khách hàng thứ ba, mở bản in",
     "3 khách hàng trong 1 phiếu",
     "- Lưu được, không bị ép về một khách hàng\n"
     "- Ngoài danh sách chỉ hiện khách hàng của dòng đầu\n"
     "- Chi tiết và bản in hiện đủ 3 khách hàng\n"
     "- Lọc theo khách hàng thứ ba VẪN tìm ra phiếu này"),

    ("005", "Vòng đời kết thúc bằng Tạo phiếu thu", "P1",
     "KT-1 và một phiếu đang Chờ KT duyệt",
     "1. KT-1 mở chi tiết phiếu, bấm Tạo phiếu thu\n"
     "2. Ở màn Phiếu thu, hoàn tất lập và duyệt phiếu thu theo luồng của màn đó\n"
     "3. Quay lại xem phiếu đề nghị: kiểm Trạng thái, nhãn màu và menu hành động",
     "—",
     "- Phiếu đề nghị chuyển sang Đã tạo phiếu thu rồi Đã hạch toán theo luồng của màn Phiếu thu\n"
     "- Nhãn đổi sang màu XANH\n"
     "- Menu hành động chỉ còn In"),

    ("006", "Đối chiếu số liệu tổng của màn với dữ liệu gốc", "P1",
     "Tài khoản có quyền xem tổng công ty; đã có bản trích dữ liệu gốc để đối chiếu",
     "1. Mở chế độ Tất cả, không đặt bộ lọc nào, ghi lại số tổng\n"
     "2. Đếm số phiếu nháp của người khác trong dữ liệu gốc\n"
     "3. Đối chiếu: tổng trên màn = tổng dữ liệu gốc trừ số phiếu nháp của người khác\n"
     "4. Lặp lại phép đối chiếu với bộ lọc theo khoảng ngày",
     "—",
     "- Bước 3 khớp chính xác\n"
     "- ⚠️ Bước 4 phải cộng bù phần bị ô \"Đến ngày\" làm rụng (mục 9 ghi chú 4), nếu không sẽ lệch"),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", SEC_III),
    ("IV", "TẠO MỚI / SỬA / XEM CHI TIẾT", SEC_IV),
    ("V", "GỬI DUYỆT & KHÔNG DUYỆT", SEC_V),
    ("VI", "XÓA", SEC_VI),
    ("VII", "IN PHIẾU", SEC_VII),
    ("VIII", "RÀNG BUỘC NHẬP LIỆU", SEC_VIII),
    ("IX", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", SEC_IX),
    ("X", "LUỒNG NGHIỆP VỤ ĐẦU - CUỐI", SEC_X),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Phiếu đề nghị thu tiền (ERP) - Cập nhật ngày 19/08/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )
