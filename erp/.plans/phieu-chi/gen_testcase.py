# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Phieu chi tien" (admin/income-expenditure/bill_payments).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

⚠️ Tai lieu nay viet theo LOGIC ERP dang chay tren nhanh gop_db (repo D:/laragon/www/erp),
KHONG phai ban da port sang HRM.

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :6629-6644
  app/Http/Controllers/IncomeExpenditure/BillPaymentController.php
  app/Model/IncomeExpenditure/BillPayment.php (+ BillPaymentDetail, BillPaymentDetailProductExportRequest)
  app/Http/Requests/IncomeExpenditure/BillPayments/BillPaymentStoreRequest.php
  app/Http/Requests/IncomeExpenditure/BillPayments/BillPaymentUpdateRequest.php
  app/Model/IncomeExpenditure/BillPaymentRequest.php (TYPE, STATUSES, nguon phieu de nghi chi)
  app/Model/Accounting/AccountDetail.php (getDataAdPaymentEmployee)
  app/Jobs/HandleAccountingPaymentEmployee.php
  app/Helpers/NotificationHelper.php :40 (sendNotifyWithPermission)
  database/seeds/PermissionsTableSeeder.php :207, :220, :221, :319
  resources/views/income_expenditure/bill_payments/*.blade.php
  resources/views/partials/classes/IncomeExpenditure/BillPayment*.blade.php
  resources/views/partials/classes/base/Datatable.blade.php :142-195
  resources/views/layouts/topmenubar.blade.php :1005

Chay:  python .plans/phieu-chi/gen_testcase.py
"""
import os
import sys

try:  # console Windows mac dinh cp1252
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

# .plans/phieu-chi -> .plans -> erp -> hrm-claude-config -> hrm/.claude/skills/...
sys.path.insert(0, os.path.join(
    HERE, "..", "..", "..", "hrm", ".claude", "skills", "testcase-documenter", "assets"))

from tc_engine import build  # noqa: E402

OUT = os.path.join(HERE, "testcase-phieu-chi.xlsx")

MODULE = "Phiếu chi tiền"

# ============================================================ 9 MUC MO TA
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Quản lý Phiếu chi tiền: chứng từ do Kế toán thanh toán lập để chi tiền ra, thuộc nhóm Công nợ - "
     "Thu - Chi.\n"
     "Có HAI cách lập phiếu chi:\n"
     "- Lập từ một Phiếu đề nghị chi đã đi hết luồng duyệt và đang ở trạng thái Đợi kế toán thanh toán "
     "tạo phiếu chi. Dùng cho các loại: Chi trả nhà cung cấp · Chi trả lại khách hàng · Chi thưởng "
     "NVKD · Chi thưởng thực hiện hợp đồng · Thanh toán chi phí vận chuyển NCC · Chi khác.\n"
     "- Lập ĐỘC LẬP, không cần phiếu đề nghị, với loại Chi thu nhập cho nhân viên: kế toán chọn Phòng "
     "ban rồi hệ thống tự nạp danh sách nhân viên còn số dư phải trả.\n"
     "Luồng duyệt cũng chia đôi theo loại chi — xem mục 5.\n"
     "Kế toán thanh toán làm được: xem danh sách, lọc, tạo phiếu (Lưu nháp hoặc Lưu và gửi duyệt), "
     "sửa, xóa, xem chi tiết, in phiếu và xuất tệp Excel.\n"
     "Kế toán trưởng và Thủ quỹ làm được: mở phiếu ở đúng trạng thái của mình để duyệt hoặc hủy."),

    ("2. Đối tượng được tính / hiển thị",
     "Phiếu chi có đủ 5 trạng thái: Đang tạo · Chờ KT trưởng duyệt · Chờ chi tiền · Đã duyệt · Hủy. "
     "Nhãn Đã duyệt tô XANH, bốn nhãn còn lại tô ĐỎ.\n"
     "Phạm vi phiếu nhìn thấy phụ thuộc chế độ danh sách đang mở:\n"
     "- Chế độ \"Phiếu của tôi\" (vào thẳng đường dẫn không kèm tham số): chỉ phiếu do chính mình lập, "
     "gồm cả phiếu nháp của mình.\n"
     "- Chế độ \"Tất cả\" (mục menu Phiếu chi trỏ vào đây): lấy theo 2 quyền xem ở mục 7, và luôn ẩn "
     "phiếu nháp của người khác.\n"
     "- Chế độ \"Phiếu chi cần duyệt\": phiếu cùng công ty với người đăng nhập; ai có quyền Thủ quỹ thì "
     "thấy thêm phiếu Chờ chi tiền, ai có quyền Kế toán trưởng thì thấy thêm phiếu Chờ KT trưởng duyệt. "
     "⚠️ Đường dẫn này KHÔNG được chặn bằng quyền nào — xem mục 9.\n"
     "- Chế độ \"Đã duyệt\": phiếu mà chính người đăng nhập là người duyệt, tính cả vai kế toán trưởng "
     "lẫn vai thủ quỹ.\n"
     "⚠️ Ba chế độ Phiếu của tôi, cần duyệt và đã duyệt KHÔNG có mục menu nào trỏ tới.\n"
     "Bảng danh sách có 12 cột: STT · Mã phiếu · Mã phiếu đề nghị chi · Loại chi · Khách hàng · Số tiền "
     "· Người đề nghị · Phòng ban · Ngày lập · Người lập · Trạng thái · Hành động."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu nháp (Đang tạo) của NGƯỜI KHÁC bị ẩn ở chế độ \"Tất cả\".\n"
     "- Nút \"Sửa phiếu chi\" và nút \"Xóa\" ngoài danh sách chỉ hiện khi phiếu ở trạng thái Đang tạo.\n"
     "- Trong màn chi tiết, hai nút Sửa và Xóa chỉ hiện khi phiếu Đang tạo VÀ người đang xem đúng là "
     "người lập phiếu.\n"
     "- Hai nút \"Duyệt phiếu chi\" và \"Hủy phiếu chi\" chỉ hiện khi phiếu ở Chờ chi tiền VÀ người "
     "đăng nhập có quyền Thủ quỹ duyệt phiếu chi.\n"
     "- Hai nút \"Kế toán duyệt phiếu chi\" và \"Hủy phiếu chi\" chỉ hiện khi phiếu ở Chờ KT trưởng "
     "duyệt VÀ người đăng nhập có quyền Kế toán trưởng duyệt phiếu chi.\n"
     "- Hai mục \"In\" và \"Xuất Excel\" luôn hiện cho mọi dòng, mọi trạng thái.\n"
     "- Cửa sổ chọn Số phiếu đề nghị CHỈ liệt kê phiếu đề nghị chi đang ở trạng thái Đợi kế toán thanh "
     "toán tạo phiếu chi; phiếu đề nghị ở các trạng thái khác đều không xuất hiện.\n"
     "- Với loại Chi thu nhập cho nhân viên: nhân viên có toàn bộ 6 khoản số dư bằng 0 sẽ KHÔNG được "
     "nạp vào bảng chi tiết.\n"
     "- Người dùng KHÔNG thêm và KHÔNG xóa được dòng chi tiết ở phiếu lập từ phiếu đề nghị.\n"
     "- Màn hình KHÔNG có chức năng Nhập Excel."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Hai ô \"Từ ngày\" và \"Đến ngày\" lọc theo NGÀY LẬP PHIẾU CHI.\n"
     "⚠️ Hai đầu mút KHÔNG được tính trọn ngày: hệ thống so sánh với mốc 0 giờ của ngày nhập vào, nên "
     "phiếu lập trong chính ngày điền ở ô \"Đến ngày\" sẽ bị loại khỏi kết quả, và phiếu lập đúng 0 giờ "
     "của ngày điền ở ô \"Từ ngày\" cũng bị loại. Đây là bẫy đối chiếu số liệu, xem mục 9.\n"
     "Không có bộ lọc theo Ngày hạch toán, cũng không có bộ lọc theo ngày cập nhật."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Hai hoặc ba cấp tùy loại chi:\n"
     "- Loại lập từ đề nghị: Phiếu đề nghị chi → Phiếu chi → Dòng chi tiết. Dòng gắn hợp đồng nguyên "
     "tắc có thêm bảng con phân bổ theo Phiếu yêu cầu xuất hàng.\n"
     "- Loại Chi thu nhập cho nhân viên: Phiếu chi → Dòng chi tiết theo từng nhân viên, mỗi dòng tách "
     "6 khoản: Chênh lệch nhân viên · Hoa hồng tháng · Hoa hồng quý · Thưởng quý · Tiền giao hàng · Chi "
     "phí khác, mỗi khoản có cặp cột số dư và số chi.\n"
     "LUỒNG DUYỆT chia đôi theo loại chi:\n"
     "- Loại KHÁC Chi thu nhập nhân viên: Đang tạo → bấm Lưu và gửi duyệt → Chờ chi tiền → Thủ quỹ bấm "
     "Duyệt phiếu chi → Đã duyệt.\n"
     "- Loại Chi thu nhập cho nhân viên: Đang tạo → bấm Lưu và gửi duyệt → Chờ KT trưởng duyệt → Kế "
     "toán trưởng bấm Kế toán duyệt phiếu chi → Chờ chi tiền → Thủ quỹ bấm Duyệt phiếu chi → Đã duyệt.\n"
     "- Ở bất kỳ bước duyệt nào cũng có thể bấm Hủy phiếu chi để đưa phiếu về trạng thái Hủy.\n"
     "Phiếu chi giữ: Mã phiếu, Số phiếu đề nghị, Tài khoản có, Loại chi, Hình thức thanh toán, Người "
     "nhận tiền, Loại tiền, Tỷ giá, Lý do chi, Ghi chú, Trạng thái, Ngày hạch toán, Người tạo, Người "
     "duyệt, Công ty, Phòng ban, Bộ phận.\n"
     "Mã phiếu sinh tự động: mã công ty + \".PC\" + tháng năm (4 số) + \".\" + 5 chữ số tăng dần, ví dụ "
     "TPE.PC0826.00017. Không sửa tay được.\n"
     "Công ty / Phòng ban / Bộ phận của phiếu chi lấy từ hồ sơ nhân sự của người LẬP PHIẾU CHI tại thời "
     "điểm tạo, và không đổi về sau.\n"
     "Mỗi lần lưu, toàn bộ dòng chi tiết cũ (kể cả bảng con phân bổ) bị xóa và ghi lại từ đầu."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Cột \"Số tiền\" ngoài danh sách LUÔN lấy tổng Số tiền chi đã quy đổi VND của mọi dòng chi tiết, "
     "kể cả khi phiếu chưa được duyệt.\n"
     "- Trong form: cột quy đổi VND của mỗi dòng = số tiền của dòng đó × Tỷ giá. Dòng \"Tổng cộng\" cuối "
     "bảng cộng dồn từng cặp cột: đề nghị chi và số tiền chi.\n"
     "- Với loại Chi thu nhập cho nhân viên: Số tiền chi của mỗi dòng phải BẰNG ĐÚNG tổng 6 khoản chi "
     "của dòng đó, lệch là bị chặn khi lưu.\n"
     "- Hai ô lọc \"Số tiền từ - đến\" so với TỔNG đã quy đổi VND của cả phiếu, không so từng dòng.\n"
     "- Cột \"Khách hàng\" ngoài danh sách chỉ lấy đối tượng của DÒNG ĐẦU TIÊN; phiếu gom nhiều đối tác "
     "vẫn chỉ hiện một tên. Loại Chi trả nhà cung cấp hiện tên nhà cung cấp, các loại còn lại hiện tên "
     "khách hàng.\n"
     "- Cột \"Phòng ban\" ngoài danh sách: loại Chi thu nhập nhân viên lấy Phòng ban được chọn trên "
     "phiếu chi, các loại còn lại lấy phòng ban của phiếu đề nghị chi.\n"
     "- Khi ghi sổ, chỉ những dòng thực sự được chi mới sinh bút toán.\n"
     "- Một phiếu khớp nhiều điều kiện lọc vẫn chỉ hiện một dòng."),

    ("7. Phân quyền cấp",
     "Năm quyền liên quan tới màn hình này:\n"
     "1. \"Kế toán thanh toán\" — được vào đường dẫn Tạo mới, đường dẫn Sửa và thao tác Lưu phiếu chi. "
     "Đây là ba chỗ DUY NHẤT của màn được hệ thống chặn bằng quyền.\n"
     "2. \"Kế toán trưởng duyệt phiếu chi\" — thấy nút Kế toán duyệt phiếu chi với phiếu đang Chờ KT "
     "trưởng duyệt, và thấy nhóm phiếu đó ở màn cần duyệt.\n"
     "3. \"Thủ quỹ duyệt phiếu chi\" — thấy nút Duyệt phiếu chi với phiếu đang Chờ chi tiền, và thấy "
     "nhóm phiếu đó ở màn cần duyệt.\n"
     "4. \"Xem tất cả phiếu chi của tổng công ty\" — thấy phiếu của mọi công ty ở chế độ Tất cả; bộ lọc "
     "hiện thêm ô Công ty và ô Phòng ban.\n"
     "5. \"Xem tất cả phiếu chi của công ty\" — chỉ phiếu công ty mình ở chế độ Tất cả; bộ lọc hiện ô "
     "Phòng ban.\n"
     "⚠️ Màn Phiếu chi KHÔNG có quyền xem cấp phòng ban và cấp bộ phận. Ai không có một trong hai quyền "
     "xem trên thì ở chế độ Tất cả chỉ thấy phiếu do chính mình lập.\n"
     "Tài khoản có vai trò Super Admin luôn mở được chi tiết mọi phiếu.\n"
     "⚠️ Thao tác Cập nhật — bao gồm cả gửi duyệt, kế toán duyệt, thủ quỹ duyệt và hủy phiếu — KHÔNG "
     "gắn quyền ở đường dẫn. Chỉ riêng nhánh chuyển sang Đã duyệt mới kiểm tra quyền Thủ quỹ ở phía hệ "
     "thống; ba nhánh còn lại chỉ ẩn / hiện nút trên giao diện. Nhóm test bỏ qua giao diện (mục IX và "
     "các ca TC-ROLE cuối) dựng riêng để đo mức độ rủi ro này."),

    ("8. Cách tính các ô thống kê",
     "- Ô \"Hiển thị a đến b trong tổng số N\" dưới bảng: a là dòng đầu trang đang xem, b là dòng cuối, "
     "N là tổng số phiếu khớp bộ lọc trong phạm vi chế độ đang mở.\n"
     "- Ô \"Số dòng mỗi trang\": mặc định 10; đổi số dòng thì bảng quay về trang 1.\n"
     "- Cột STT đánh liên tục theo trang: trang 2 với 10 dòng mỗi trang bắt đầu từ 11.\n"
     "- Cột \"Số tiền\": xem công thức ở mục 6, hiển thị phân cách nghìn.\n"
     "- Cột \"Ngày lập\" hiển thị dạng ngày/tháng/năm, không có giờ.\n"
     "- Ngày hạch toán được hệ thống đóng dấu bằng NGÀY THỦ QUỸ BẤM DUYỆT, không cho người dùng chọn.\n"
     "- Với loại Chi thu nhập cho nhân viên, mỗi khoản trong 6 khoản có một ô tổng riêng ở dòng cuối "
     "bảng, và một ô tổng chung cộng cả 6 khoản.\n"
     "- Bản in các loại chi thông thường luôn ra 2 liên: phiếu 1 đối tác thì 2 liên nằm trên cùng một "
     "trang, phiếu nhiều đối tác thì 2 liên tách thành 2 trang. Riêng bản in loại Chi thu nhập cho nhân "
     "viên chỉ ra MỘT liên."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất của màn này — đọc trước khi chạy test:\n"
     "1. ⚠️ Màn \"Phiếu chi cần duyệt\" KHÔNG chặn quyền. Người không có quyền duyệt nào mà dán thẳng "
     "đường dẫn thì điều kiện lọc theo trạng thái trở thành rỗng, nên nhìn thấy TOÀN BỘ phiếu chi của "
     "công ty, đủ mọi trạng thái. Đây là lỗ hổng, ghi nhận Failed.\n"
     "2. ⚠️ Ở màn duyệt, cảnh báo lệch tiền KHÔNG BAO GIỜ hiện ra do cách kiểm tra bị sai kiểu dữ liệu. "
     "Nghĩa là thủ quỹ và kế toán trưởng bấm duyệt được cả khi bảng con phân bổ lệch với số tiền chi. "
     "Test kỹ nhánh này.\n"
     "3. ⚠️ Thao tác Lưu ở màn SỬA chỉ ghi lại đúng ba thứ: Số phiếu đề nghị, Tài khoản có và Người "
     "nhận tiền. Sửa Lý do chi, Ghi chú, Hình thức thanh toán, Tỷ giá, Loại tiền, Phòng ban rồi bấm Lưu "
     "thì các giá trị đó KHÔNG được lưu lại, dù màn hình báo cập nhật thành công.\n"
     "4. ⚠️ Hệ quả của điểm 3: khi Hủy phiếu chi, ô Ghi chú BẮT BUỘC nhập nhưng nội dung nhập vào lại "
     "KHÔNG được lưu. Mở lại phiếu đã hủy sẽ thấy Ghi chú trống.\n"
     "5. ⚠️ Hệ thống KHÔNG chặn lập hai phiếu chi cho cùng một phiếu đề nghị chi (khác với màn Phiếu "
     "thu vốn có chặn). Cần thử lập trùng và ghi nhận kết quả.\n"
     "6. ⚠️ Xóa phiếu chi: hệ thống KHÔNG kiểm tra quyền và KHÔNG kiểm tra trạng thái. Dán thẳng đường "
     "dẫn xóa của một phiếu bất kỳ, kể cả phiếu Đã duyệt đã ghi sổ, là phiếu bị xóa.\n"
     "7. ⚠️ Xóa phiếu chi chỉ xóa phần đầu phiếu, KHÔNG xóa các dòng chi tiết. Các dòng đó ở lại trong "
     "kho dữ liệu và có thể làm sai số liệu báo cáo.\n"
     "8. ⚠️ Xóa phiếu chi KHÔNG trả phiếu đề nghị chi về trạng thái Đợi kế toán thanh toán tạo phiếu "
     "chi, nên phiếu đề nghị bị kẹt.\n"
     "9. ⚠️ Ô lọc \"Đối tác\" có dấu hiệu sai trong mã nguồn. Chọn một đối tác rồi tìm kiếm có thể làm "
     "bảng báo lỗi và không tải được dữ liệu. Test riêng ca này.\n"
     "10. ⚠️ Ô lọc \"Phòng ban\" lọc theo phòng ban của NGƯỜI LẬP PHIẾU CHI, trong khi CỘT Phòng ban "
     "ngoài danh sách lại hiển thị phòng ban của phiếu đề nghị (hoặc phòng ban được chọn với loại chi "
     "thu nhập nhân viên). Hai chỗ này không cùng nguồn nên lọc ra kết quả nhìn như sai.\n"
     "11. ⚠️ Khi bấm Lưu và gửi duyệt một phiếu loại Chi thu nhập cho nhân viên, hệ thống ghi luôn "
     "chính NGƯỜI LẬP vào ô người kế toán duyệt, dù kế toán trưởng chưa bấm gì. Hệ quả: phiếu đó xuất "
     "hiện ở màn \"Đã duyệt\" của người lập ngay từ lúc mới gửi.\n"
     "12. ⚠️ Ô \"Đến ngày\" làm rụng trọn ngày cuối (mục 4). Khi đối chiếu số liệu phải cộng bù.\n"
     "13. ⚠️ Duyệt phiếu loại Chi thu nhập cho nhân viên thì bút toán KHÔNG xuất hiện ngay: hệ thống "
     "đẩy việc ghi sổ sang chạy nền. Chờ vài phút rồi mở lại sổ kế toán, đừng vội kết luận là mất bút "
     "toán.\n"
     "14. ⚠️ Mã phiếu ngoài danh sách mở chi tiết ở THẺ MỚI, khác với đa số màn khác.\n"
     "15. Bộ lọc được hệ thống ghi nhớ RIÊNG cho từng chế độ danh sách; rời màn rồi quay lại vẫn còn "
     "điều kiện lọc cũ — test xong nhớ bấm nút làm mới bộ lọc trước khi sang ca test khác."),
]

# ============================================================ TC PHAN QUYEN
ROLE_TCS = [
    ("00", "Tài khoản không có quyền xem nào chỉ thấy phiếu do chính mình lập", "P0",
     "Tài khoản NV-A không có quyền \"Xem tất cả phiếu chi của tổng công ty\" và không có quyền \"Xem "
     "tất cả phiếu chi của công ty\"; NV-A đã lập 9 phiếu chi; công ty của NV-A có hơn 120 phiếu chi "
     "của nhiều người",
     "1. Đăng nhập bằng NV-A\n"
     "2. Mở menu Công nợ - Thu - Chi, bấm mục Phiếu chi\n"
     "3. Đọc số tổng dưới bảng\n"
     "4. Lật hết các trang, soát cột Người lập",
     "Tài khoản: NV-A (không quyền xem theo cấp)",
     "- Vào được màn hình, không bị chặn\n"
     "- Tổng hiện đúng 9\n"
     "- Mọi dòng đều có Người lập là NV-A\n"
     "- Khối lọc KHÔNG có ô Công ty, KHÔNG có ô Phòng ban theo đơn vị"),

    ("01", "Quyền xem của tổng công ty thấy phiếu chi của mọi công ty", "P0",
     "Tài khoản B chỉ có quyền \"Xem tất cả phiếu chi của tổng công ty\"; hệ thống có phiếu chi của ít "
     "nhất 3 công ty",
     "1. Đăng nhập bằng B, mở mục Phiếu chi trên menu\n"
     "2. Bấm nút Bộ lọc để bung khối tìm kiếm\n"
     "3. Ghi lại các ô lọc theo đơn vị đang hiện\n"
     "4. Chọn lần lượt từng Công ty rồi bấm nút tìm kiếm",
     "Quyền: Xem tất cả phiếu chi của tổng công ty",
     "- Khối lọc hiện CẢ ô Công ty và ô Phòng ban\n"
     "- Bỏ chọn công ty thì thấy phiếu của cả 3 công ty\n"
     "- Chọn công ty nào ra phiếu do người của công ty đó lập"),

    ("02", "Quyền xem của công ty chỉ thấy phiếu chi công ty mình", "P0",
     "Tài khoản C chỉ có quyền \"Xem tất cả phiếu chi của công ty\", thuộc công ty 3; công ty 3 có 35 "
     "phiếu chi, công ty 1 có 210 phiếu chi",
     "1. Đăng nhập bằng C, mở mục Phiếu chi\n"
     "2. Bấm nút Bộ lọc, ghi lại các ô lọc theo đơn vị\n"
     "3. Đọc số tổng, soát danh sách qua tất cả các trang",
     "Quyền: Xem tất cả phiếu chi của công ty",
     "- Khối lọc KHÔNG có ô Công ty, chỉ có ô Phòng ban\n"
     "- Tổng bằng 35 trừ đi số phiếu nháp của người khác trong công ty 3\n"
     "- Không có phiếu nào của công ty 1"),

    ("03", "Màn Phiếu chi không có quyền xem cấp phòng ban và cấp bộ phận", "P1",
     "Tài khoản D có quyền xem cấp phòng ban của màn khác nhưng KHÔNG có hai quyền xem của màn Phiếu chi",
     "1. Đăng nhập bằng D, mở mục Phiếu chi\n"
     "2. Đọc số tổng và soát cột Người lập\n"
     "3. Bấm Bộ lọc, quan sát các ô lọc theo đơn vị",
     "—",
     "- CHỈ thấy phiếu do chính D lập\n"
     "- ⚠️ Đúng hiện trạng — màn Phiếu chi không có quyền cấp phòng ban / bộ phận (mục 7)"),

    ("04", "Kế toán thanh toán vào được màn Tạo mới", "P0",
     "Tài khoản KT-1 có quyền \"Kế toán thanh toán\"; có ít nhất 3 phiếu đề nghị chi đang ở trạng thái "
     "Đợi kế toán thanh toán tạo phiếu chi",
     "1. Đăng nhập bằng KT-1, mở mục Phiếu chi\n"
     "2. Bấm nút Tạo mới\n"
     "3. Bấm kính lúp ở ô Số phiếu đề nghị",
     "Quyền: Kế toán thanh toán",
     "- Vào được form Tạo phiếu chi, không bị chặn\n"
     "- Cửa sổ chọn hiện đúng 3 phiếu đề nghị đang đợi lập phiếu chi"),

    ("05", "Không có quyền Kế toán thanh toán thì bị chặn ở màn Tạo mới", "P0",
     "Tài khoản NV-A ở TC-ROLE-00, không có quyền \"Kế toán thanh toán\"",
     "1. Đăng nhập bằng NV-A, mở mục Phiếu chi\n"
     "2. Bấm nút Tạo mới, hoặc dán thẳng đường dẫn tạo mới nếu không có nút",
     "Đường dẫn Tạo phiếu chi",
     "- Hệ thống từ chối, báo không có quyền, không mở được form"),

    ("06", "Không có quyền Kế toán thanh toán thì bị chặn ở màn Sửa và ở thao tác Lưu", "P0",
     "Tài khoản NV-A; tồn tại phiếu chi trạng thái Đang tạo",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dán thẳng đường dẫn sửa của phiếu đó\n"
     "3. Dùng công cụ kiểm thử gọi thẳng thao tác Lưu phiếu chi mới",
     "—",
     "- Bước 2: hệ thống từ chối, báo không có quyền\n"
     "- Bước 3: cũng bị từ chối, không tạo được phiếu mới"),

    ("07", "Kế toán trưởng thấy nút duyệt với phiếu Chờ KT trưởng duyệt", "P0",
     "Tài khoản KTT-1 có quyền \"Kế toán trưởng duyệt phiếu chi\"; phiếu PC-01 loại Chi thu nhập cho "
     "nhân viên đang ở trạng thái Chờ KT trưởng duyệt, cùng công ty",
     "1. Đăng nhập bằng KTT-1\n"
     "2. Mở chi tiết PC-01\n"
     "3. Soát khu vực nút phía dưới form",
     "Quyền: Kế toán trưởng duyệt phiếu chi",
     "- Có nút Kế toán duyệt phiếu chi và nút Hủy phiếu chi\n"
     "- KHÔNG có nút Duyệt phiếu chi của thủ quỹ"),

    ("08", "Thủ quỹ thấy nút duyệt với phiếu Chờ chi tiền", "P0",
     "Tài khoản TQ-1 có quyền \"Thủ quỹ duyệt phiếu chi\"; phiếu PC-02 đang ở trạng thái Chờ chi tiền, "
     "cùng công ty",
     "1. Đăng nhập bằng TQ-1\n"
     "2. Mở chi tiết PC-02\n"
     "3. Soát khu vực nút phía dưới form",
     "Quyền: Thủ quỹ duyệt phiếu chi",
     "- Có nút Duyệt phiếu chi và nút Hủy phiếu chi\n"
     "- KHÔNG có nút Kế toán duyệt phiếu chi"),

    ("09", "Kế toán trưởng không thấy nút duyệt khi phiếu đã sang Chờ chi tiền", "P0",
     "Tài khoản KTT-1; phiếu PC-02 đang ở trạng thái Chờ chi tiền",
     "1. Đăng nhập bằng KTT-1, mở chi tiết PC-02\n"
     "2. Soát khu vực nút phía dưới form",
     "—",
     "- KHÔNG có nút duyệt nào\n"
     "- Chỉ còn In, Xuất Excel và Quay lại"),

    ("10", "Thủ quỹ không thấy nút duyệt khi phiếu còn Chờ KT trưởng duyệt", "P0",
     "Tài khoản TQ-1; phiếu PC-01 đang ở trạng thái Chờ KT trưởng duyệt",
     "1. Đăng nhập bằng TQ-1, mở chi tiết PC-01\n"
     "2. Soát khu vực nút phía dưới form",
     "—",
     "- KHÔNG có nút duyệt nào, phải chờ kế toán trưởng xử lý trước"),

    ("11", "Màn cần duyệt gom đúng nhóm phiếu theo quyền", "P0",
     "Công ty 3 có 4 phiếu Chờ chi tiền và 6 phiếu Chờ KT trưởng duyệt; TQ-1 chỉ có quyền thủ quỹ, "
     "KTT-1 chỉ có quyền kế toán trưởng, cả hai thuộc công ty 3",
     "1. Đăng nhập bằng TQ-1, dán đường dẫn màn Phiếu chi cần duyệt, đọc số tổng\n"
     "2. Đăng nhập bằng KTT-1, làm lại bước trên",
     "—",
     "- TQ-1 thấy đúng 4 phiếu, tất cả ở Chờ chi tiền\n"
     "- KTT-1 thấy đúng 6 phiếu, tất cả ở Chờ KT trưởng duyệt"),

    ("12", "Có cả hai quyền duyệt thì thấy cả hai nhóm", "P1",
     "Tài khoản KTQ có ĐỒNG THỜI quyền thủ quỹ và quyền kế toán trưởng, thuộc công ty 3",
     "1. Đăng nhập bằng KTQ, dán đường dẫn màn Phiếu chi cần duyệt\n"
     "2. Đọc số tổng và cột Trạng thái",
     "—",
     "- Thấy đủ 10 phiếu\n"
     "- Cột Trạng thái có cả Chờ chi tiền và Chờ KT trưởng duyệt, không có trạng thái nào khác"),

    ("13", "Không có quyền duyệt nào vẫn vào được màn cần duyệt", "P0",
     "Tài khoản NV-A không có quyền thủ quỹ và không có quyền kế toán trưởng, thuộc công ty 3; công ty "
     "3 có tổng 60 phiếu chi ở đủ 5 trạng thái",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dán thẳng đường dẫn màn Phiếu chi cần duyệt\n"
     "3. Đọc số tổng và soát cột Trạng thái",
     "Đường dẫn màn cần duyệt",
     "- ⚠️ Vào được, KHÔNG bị chặn\n"
     "- Thấy TOÀN BỘ 60 phiếu của công ty, đủ mọi trạng thái kể cả Đang tạo và Đã duyệt (mục 9 ghi chú "
     "1)\n"
     "- Ghi nhận Failed, đây là lỗ hổng phân quyền"),

    ("14", "Người lập và người duyệt luôn mở được chi tiết phiếu của mình", "P1",
     "Phiếu PC-03 do KT-1 lập, đã được TQ-1 duyệt; tài khoản NV-A không liên quan và không có quyền xem "
     "theo cấp nào",
     "1. Đăng nhập lần lượt bằng KT-1, TQ-1 rồi NV-A\n"
     "2. Mỗi lần đều dán đường dẫn chi tiết của PC-03",
     "—",
     "- KT-1 xem được (người lập)\n"
     "- TQ-1 xem được (người duyệt)\n"
     "- NV-A bị đưa sang màn báo không tìm thấy dữ liệu"),

    ("15", "Bỏ qua giao diện gọi thẳng thao tác Duyệt của thủ quỹ", "P0",
     "Tài khoản NV-A không có quyền \"Thủ quỹ duyệt phiếu chi\"; phiếu PC-02 đang ở Chờ chi tiền",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dùng công cụ kiểm thử gọi thẳng thao tác Cập nhật của PC-02 với trạng thái Đã duyệt\n"
     "3. Mở lại chi tiết PC-02 và mở sổ kế toán",
     "Trạng thái gửi lên: Đã duyệt",
     "- Hệ thống từ chối, báo không có quyền\n"
     "- Phiếu vẫn ở Chờ chi tiền, không sinh bút toán\n"
     "- ⚠️ Đây là nhánh DUY NHẤT có kiểm tra quyền ở phía hệ thống (mục 7)"),

    ("16", "Bỏ qua giao diện gọi thẳng thao tác Kế toán duyệt", "P0",
     "Tài khoản NV-A không có quyền \"Kế toán trưởng duyệt phiếu chi\"; phiếu PC-01 đang Chờ KT trưởng "
     "duyệt",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dùng công cụ kiểm thử gọi thẳng thao tác Cập nhật của PC-01 với trạng thái Chờ chi tiền\n"
     "3. Mở lại chi tiết PC-01",
     "Trạng thái gửi lên: Chờ chi tiền",
     "- ⚠️ Nhánh này KHÔNG kiểm tra quyền, nhiều khả năng phiếu bị đẩy sang Chờ chi tiền\n"
     "- Nếu lọt thì ghi Failed kèm mã phiếu để dựng phiếu ghi nhận lỗi"),

    ("17", "Bỏ qua giao diện gọi thẳng thao tác Hủy", "P0",
     "Tài khoản NV-A; phiếu PC-02 đang ở Chờ chi tiền, gắn phiếu đề nghị chi DNC-02",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dùng công cụ kiểm thử gọi thẳng thao tác Cập nhật của PC-02 với trạng thái Hủy\n"
     "3. Mở lại chi tiết PC-02 và mở DNC-02",
     "Trạng thái gửi lên: Hủy",
     "- ⚠️ Nhánh này KHÔNG kiểm tra quyền, nhiều khả năng phiếu bị hủy và phiếu đề nghị cũng chuyển "
     "sang Hủy theo\n"
     "- Nếu lọt thì ghi Failed"),

    ("18", "Bỏ qua giao diện gọi thẳng thao tác Xóa", "P0",
     "Tài khoản NV-A không có quyền nào của màn Phiếu chi; phiếu PC-03 đang ở Đã duyệt và đã ghi sổ",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dán thẳng đường dẫn xóa của PC-03\n"
     "3. Mở lại danh sách, tìm PC-03\n"
     "4. Mở sổ kế toán, tìm bút toán của PC-03",
     "Đường dẫn xóa phiếu PC-03",
     "- ⚠️ Phiếu BỊ XÓA thật kèm thông báo thành công (mục 9 ghi chú 6)\n"
     "- Bút toán vẫn còn trong sổ, thành bút toán mồ côi\n"
     "- Ghi nhận Failed"),
]

# ============================================================ SECTIONS
SEC_I = [
    (1, "Vào màn Phiếu chi từ menu", "P0",
     "Tài khoản KT-1 có quyền Kế toán thanh toán",
     "1. Đăng nhập bằng KT-1\n"
     "2. Mở menu Công nợ - Thu - Chi\n"
     "3. Bấm mục Phiếu chi",
     "—",
     "- Mở đúng màn danh sách phiếu chi\n"
     "- Bảng có đủ 12 cột theo thứ tự ở mục 2\n"
     "- Phía trên bảng có nút Bộ lọc và nút Tạo mới"),

    (2, "Chế độ Phiếu của tôi chỉ hiện phiếu mình lập", "P0",
     "Tài khoản KT-1 có quyền xem của công ty; KT-1 đã lập 9 phiếu chi trong đó có 2 phiếu nháp; công "
     "ty có hơn 35 phiếu chi",
     "1. Đăng nhập bằng KT-1\n"
     "2. Dán đường dẫn màn Phiếu chi KHÔNG kèm tham số chế độ\n"
     "3. Đọc số tổng, soát cột Người lập và cột Trạng thái",
     "—",
     "- Tổng hiện đúng 9\n"
     "- Mọi dòng đều có Người lập là KT-1\n"
     "- Cả 2 phiếu nháp của KT-1 đều hiện"),

    (3, "Chế độ Tất cả ẩn phiếu nháp của người khác", "P0",
     "Tài khoản B có quyền xem tổng công ty; KT-1 vừa Lưu nháp một phiếu chi mã kết thúc .00031",
     "1. Đăng nhập bằng B, mở mục Phiếu chi trên menu\n"
     "2. Bấm Bộ lọc, gõ .00031 vào ô Mã phiếu, bấm tìm kiếm\n"
     "3. Xóa ô mã, chọn Trạng thái là Đang tạo rồi tìm lại",
     "Mã phiếu: .00031",
     "- Bước 2 không ra dòng nào\n"
     "- Bước 3 chỉ ra phiếu nháp do chính B lập"),

    (4, "Màn Đã duyệt gom phiếu của cả hai vai duyệt", "P0",
     "Tài khoản KTQ vừa có quyền thủ quỹ vừa có quyền kế toán trưởng; KTQ đã kế toán duyệt 3 phiếu và "
     "đã thủ quỹ duyệt 5 phiếu",
     "1. Đăng nhập bằng KTQ\n"
     "2. Dán đường dẫn màn Phiếu chi đã duyệt\n"
     "3. Đọc số tổng và cột Trạng thái",
     "—",
     "- Thấy đủ 8 phiếu\n"
     "- Có cả phiếu đang Chờ chi tiền (mình mới kế toán duyệt) lẫn phiếu Đã duyệt\n"
     "- ⚠️ Màn này KHÔNG lọc theo trạng thái, chỉ lọc theo việc mình có tên ở một trong hai ô người "
     "duyệt"),

    (5, "Phiếu chi thu nhập nhân viên vào màn Đã duyệt ngay khi vừa gửi", "P0",
     "Tài khoản KT-1 vừa bấm Lưu và gửi duyệt một phiếu loại Chi thu nhập cho nhân viên; kế toán trưởng "
     "chưa bấm gì",
     "1. Đăng nhập bằng KT-1\n"
     "2. Dán đường dẫn màn Phiếu chi đã duyệt\n"
     "3. Tìm phiếu vừa gửi",
     "—",
     "- ⚠️ Phiếu ĐÃ xuất hiện ở màn Đã duyệt của KT-1 dù chưa ai duyệt, trạng thái vẫn là Chờ KT trưởng "
     "duyệt (mục 9 ghi chú 11)\n"
     "- Ghi nhận Failed"),

    (6, "Mã phiếu mở chi tiết ở thẻ mới", "P1",
     "Danh sách có ít nhất 1 phiếu chi",
     "1. Mở danh sách Phiếu chi\n"
     "2. Bấm vào Mã phiếu ở dòng đầu tiên",
     "—",
     "- Mở THẺ MỚI vào màn Chi tiết phiếu chi tiền\n"
     "- Thẻ danh sách vẫn còn nguyên (mục 9 ghi chú 14)"),

    (7, "Mã phiếu đề nghị chi mở sang màn Đề nghị thanh toán ở thẻ mới", "P1",
     "Có phiếu chi lập từ phiếu đề nghị chi",
     "1. Mở danh sách, bấm vào Mã phiếu đề nghị chi của dòng đó",
     "—",
     "- Mở thẻ mới vào màn Chi tiết phiếu đề nghị thanh toán tương ứng"),

    (8, "Phiếu chi thu nhập nhân viên không có mã phiếu đề nghị", "P1",
     "Có phiếu chi loại Chi thu nhập cho nhân viên",
     "1. Tìm phiếu đó trên danh sách\n"
     "2. Đọc ô ở cột Mã phiếu đề nghị chi",
     "—",
     "- Ô để TRỐNG, không có đường dẫn nào\n"
     "- Cột Người đề nghị cũng trống\n"
     "- ⚠️ Đúng thiết kế — loại này lập độc lập, không có phiếu đề nghị"),

    (9, "Menu hành động đủ mục với phiếu Đang tạo", "P0",
     "Tài khoản KT-1; có phiếu PC-N ở trạng thái Đang tạo do KT-1 lập",
     "1. Bấm biểu tượng bánh răng ở dòng PC-N\n"
     "2. Ghi lại các mục trong menu",
     "—",
     "- Có đủ 4 mục: In · Xuất Excel · Sửa phiếu chi · Xóa"),

    (10, "Menu hành động thu gọn với phiếu đã gửi duyệt", "P0",
     "Có phiếu ở Chờ KT trưởng duyệt, Chờ chi tiền, Đã duyệt và Hủy",
     "1. Bấm bánh răng lần lượt ở 4 phiếu\n"
     "2. Ghi lại các mục trong từng menu",
     "—",
     "- Cả 4 phiếu chỉ còn 2 mục: In và Xuất Excel"),

    (11, "Nút Sửa và Xóa trong màn chi tiết xét cả người lập", "P0",
     "Phiếu PC-N ở trạng thái Đang tạo do KT-1 lập; KT-2 cũng có quyền Kế toán thanh toán",
     "1. Đăng nhập bằng KT-1, mở chi tiết PC-N, soát nút\n"
     "2. Đăng nhập bằng KT-2, mở chi tiết PC-N, soát nút",
     "—",
     "- KT-1 thấy nút Sửa và nút Xóa\n"
     "- KT-2 KHÔNG thấy hai nút đó\n"
     "- ⚠️ Màn chi tiết xét cả người lập, còn menu ngoài danh sách chỉ xét trạng thái"),

    (12, "Mở chi tiết phiếu không thuộc phạm vi xem", "P1",
     "Tài khoản NV-A không có quyền xem theo cấp; phiếu PC-D do người khác lập, trạng thái Đang tạo",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dán đường dẫn chi tiết của PC-D",
     "—",
     "- Hệ thống đưa sang màn báo không tìm thấy dữ liệu"),

    (13, "Mở chi tiết bằng mã phiếu không tồn tại", "P2",
     "—",
     "1. Dán đường dẫn chi tiết với một mã số không có trong hệ thống",
     "Mã số: 999999",
     "- Hệ thống báo không tìm thấy dữ liệu, không treo trang"),

    (14, "Số dòng mỗi trang và cột STT", "P2",
     "Danh sách có ít nhất 25 phiếu",
     "1. Mở danh sách ở chế độ Tất cả\n"
     "2. Đọc ô Hiển thị a đến b trong tổng số N\n"
     "3. Sang trang 2, đọc cột STT\n"
     "4. Đổi số dòng mỗi trang sang 25",
     "Số dòng mỗi trang: 10 rồi 25",
     "- Mặc định 10 dòng\n"
     "- Trang 2 cột STT bắt đầu từ 11\n"
     "- Đổi sang 25 thì bảng quay về trang 1"),
]

SEC_II = [
    (1, "Lọc theo Mã phiếu", "P0",
     "Tồn tại phiếu chi mã TPE.PC0826.00017",
     "1. Mở danh sách, bấm nút Bộ lọc\n"
     "2. Gõ 00017 vào ô Mã phiếu, bấm tìm kiếm",
     "Mã phiếu: 00017",
     "- Ra đúng phiếu TPE.PC0826.00017\n"
     "- Tìm bằng một đoạn giữa của mã vẫn ra kết quả"),

    (2, "Lọc theo Mã phiếu đề nghị chi", "P0",
     "Phiếu chi TPE.PC0826.00017 gắn phiếu đề nghị TPE.DNTT0826.00042",
     "1. Bấm Bộ lọc, gõ 00042 vào ô Mã phiếu đề nghị chi, tìm kiếm",
     "Mã phiếu đề nghị chi: 00042",
     "- Ra đúng phiếu chi gắn phiếu đề nghị đó\n"
     "- Phiếu loại Chi thu nhập nhân viên không bao giờ lọt vào kết quả của ô lọc này"),

    (3, "Lọc theo Loại chi", "P0",
     "Danh sách có phiếu ở nhiều loại chi khác nhau",
     "1. Bấm Bộ lọc, chọn lần lượt từng Loại chi rồi tìm kiếm\n"
     "2. Soát cột Loại chi sau mỗi lần lọc",
     "Loại chi: Chi trả nhà cung cấp · Chi trả lại khách hàng · Chi thưởng NVKD · Chi thu nhập cho nhân "
     "viên · Chi thưởng thực hiện hợp đồng · Chi khác · Thanh toán chi phí vận chuyển NCC",
     "- Mỗi lần chỉ ra phiếu đúng loại đã chọn\n"
     "- Ô chọn liệt kê đủ 7 loại chi"),

    (4, "Lọc theo Người lập", "P1",
     "KT-1 đã lập 9 phiếu chi, KT-2 đã lập 6 phiếu chi",
     "1. Bấm Bộ lọc, chọn KT-1 ở ô Người lập, tìm kiếm\n"
     "2. Đổi sang KT-2, tìm lại",
     "Người lập: KT-1 rồi KT-2",
     "- Lần 1 ra 9 dòng, lần 2 ra 6 dòng\n"
     "- Cột Người lập khớp lựa chọn"),

    (5, "Lọc theo Người đề nghị", "P1",
     "Nhân viên NV-B đã lập 4 phiếu đề nghị chi và cả 4 đều đã có phiếu chi",
     "1. Bấm Bộ lọc, chọn NV-B ở ô Người đề nghị, tìm kiếm",
     "Người đề nghị: NV-B",
     "- Ra đúng 4 dòng\n"
     "- Mọi dòng có Người đề nghị là NV-B, dù Người lập là kế toán khác"),

    (6, "Lọc theo khoảng Số tiền", "P0",
     "Có phiếu chi tổng 5.000.000 và phiếu chi tổng 30.000.000",
     "1. Bấm Bộ lọc, nhập Số tiền từ 1.000.000 đến 10.000.000, tìm kiếm\n"
     "2. Đổi khoảng thành 20.000.000 đến 50.000.000, tìm lại",
     "Số tiền từ - đến",
     "- Lần 1 có phiếu 5.000.000, không có phiếu 30.000.000\n"
     "- Lần 2 ngược lại\n"
     "- Nhập số có dấu phân cách nghìn vẫn lọc đúng"),

    (7, "Khoảng Số tiền so với tổng cả phiếu", "P1",
     "Phiếu PC-E có 3 dòng, mỗi dòng 4.000.000, tổng 12.000.000",
     "1. Lọc Số tiền từ 10.000.000 đến 15.000.000\n"
     "2. Lọc Số tiền từ 3.000.000 đến 5.000.000",
     "—",
     "- Lần 1 có PC-E, lần 2 không có\n"
     "- ⚠️ Bộ lọc so với TỔNG cả phiếu, không so từng dòng (mục 6)"),

    (8, "Số tiền dùng để lọc không đổi sau khi duyệt", "P1",
     "Phiếu PC-F tổng số tiền chi 12.000.000, đang Chờ chi tiền",
     "1. Lọc Số tiền từ 11.000.000 đến 13.000.000, ghi kết quả\n"
     "2. Thủ quỹ duyệt PC-F\n"
     "3. Lọc lại đúng khoảng cũ",
     "—",
     "- Cả hai lần đều có PC-F\n"
     "- ⚠️ Khác màn Phiếu thu: cột Số tiền của phiếu chi luôn lấy theo số tiền chi, không đổi theo "
     "trạng thái (mục 6)"),

    (9, "Lọc theo Trạng thái", "P0",
     "Danh sách có phiếu ở đủ 5 trạng thái",
     "1. Bấm Bộ lọc, chọn lần lượt từng trạng thái rồi tìm kiếm\n"
     "2. Soát cột Trạng thái sau mỗi lần",
     "Trạng thái: Đang tạo · Chờ KT trưởng duyệt · Chờ chi tiền · Đã duyệt · Hủy",
     "- Mỗi lần chỉ ra phiếu đúng trạng thái đã chọn\n"
     "- Nhãn Đã duyệt tô xanh, bốn nhãn còn lại tô đỏ"),

    (10, "Lọc theo Phòng ban", "P0",
     "Kế toán KT-9 thuộc phòng Kế toán đã lập phiếu chi cho phiếu đề nghị của phòng Kinh doanh 1",
     "1. Bấm Bộ lọc, chọn Phòng ban là phòng Kế toán, tìm kiếm\n"
     "2. Đọc cột Phòng ban của dòng kết quả\n"
     "3. Đổi sang phòng Kinh doanh 1, tìm lại",
     "Phòng ban: Kế toán rồi Kinh doanh 1",
     "- ⚠️ Bước 1 RA phiếu của KT-9 nhưng cột Phòng ban lại hiển thị Kinh doanh 1, nhìn như lọc sai\n"
     "- Bước 3 KHÔNG ra phiếu đó\n"
     "- Đây là hiện trạng đã biết (mục 9 ghi chú 10)"),

    (11, "Lọc theo Đối tác", "P0",
     "Nhà cung cấp NCC-01 xuất hiện ở 3 phiếu chi",
     "1. Bấm Bộ lọc, chọn NCC-01 ở ô Đối tác\n"
     "2. Bấm tìm kiếm\n"
     "3. Quan sát bảng dữ liệu",
     "Đối tác: NCC-01",
     "- Kỳ vọng nghiệp vụ: ra đúng 3 phiếu chi có NCC-01\n"
     "- ⚠️ Ô lọc này có dấu hiệu sai trong mã nguồn (mục 9 ghi chú 9). Nếu bảng báo lỗi hoặc không tải "
     "được dữ liệu thì ghi Failed kèm ảnh chụp"),

    (12, "Lọc theo khoảng ngày lập", "P0",
     "Có phiếu chi lập ngày 05/08/2026 và phiếu chi lập ngày 25/08/2026",
     "1. Bấm Bộ lọc, nhập Từ ngày 01/08/2026 và Đến ngày 10/08/2026, tìm kiếm\n"
     "2. Đổi khoảng thành 20/08/2026 đến 31/08/2026, tìm lại",
     "Từ ngày - Đến ngày",
     "- Lần 1 có phiếu ngày 05/08, không có phiếu ngày 25/08\n"
     "- Lần 2 ngược lại"),

    (13, "Ô Đến ngày làm rụng phiếu của chính ngày đó", "P0",
     "Có đúng 3 phiếu chi lập trong ngày 20/08/2026",
     "1. Nhập Từ ngày 01/08/2026 và Đến ngày 20/08/2026, tìm kiếm\n"
     "2. Đếm số phiếu lập ngày 20/08 trong kết quả\n"
     "3. Đổi Đến ngày thành 21/08/2026, tìm lại",
     "Đến ngày: 20/08/2026 rồi 21/08/2026",
     "- ⚠️ Lần 1 KHÔNG có phiếu nào của ngày 20/08 (mục 4)\n"
     "- Lần 2 mới đủ 3 phiếu\n"
     "- Ghi nhận Failed, khi đối chiếu số liệu phải cộng bù"),

    (14, "Ô lọc Công ty", "P1",
     "Tài khoản B có quyền xem tổng công ty; có phiếu chi của công ty 1 và công ty 3",
     "1. Mở chế độ Tất cả, bấm Bộ lọc\n"
     "2. Chọn lần lượt từng Công ty rồi tìm kiếm",
     "Công ty: công ty 1 rồi công ty 3",
     "- Mỗi lần chỉ ra phiếu do người của công ty đã chọn lập\n"
     "- ⚠️ Ô này lọc theo công ty của NGƯỜI LẬP PHIẾU CHI"),

    (15, "Kết hợp nhiều điều kiện lọc", "P1",
     "Có phiếu Chi trả nhà cung cấp, trạng thái Đã duyệt, người lập KT-1, tổng tiền 9.000.000",
     "1. Đặt cùng lúc: Loại chi Chi trả nhà cung cấp, Trạng thái Đã duyệt, Người lập KT-1, Số tiền từ "
     "8.000.000 đến 10.000.000\n"
     "2. Bấm tìm kiếm",
     "—",
     "- Chỉ ra phiếu khớp ĐỒNG THỜI cả 4 điều kiện\n"
     "- Mỗi phiếu chỉ hiện một dòng"),

    (16, "Làm mới bộ lọc", "P1",
     "Đang có ít nhất 3 ô lọc được điền",
     "1. Điền Mã phiếu, Trạng thái, Người lập rồi tìm kiếm\n"
     "2. Bấm nút làm mới bộ lọc",
     "—",
     "- Mọi ô lọc trở về rỗng, kể cả hai ô ngày\n"
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
     "1. Gõ một chuỗi chắc chắn không có vào ô Mã phiếu, tìm kiếm",
     "Mã phiếu: ZZZZZZ",
     "- Bảng hiện thông báo không có dữ liệu, số tổng bằng 0\n"
     "- Không báo lỗi hệ thống"),
]

SEC_III = [
    (1, "Sắp xếp mặc định theo ngày lập mới nhất", "P1",
     "Danh sách có ít nhất 30 phiếu, lập vào nhiều ngày khác nhau",
     "1. Mở danh sách, không bấm sắp xếp\n"
     "2. Đọc cột Ngày lập của 10 dòng đầu",
     "—",
     "- Phiếu lập gần nhất nằm trên cùng, ngày giảm dần"),

    (2, "Không cột nào sắp xếp được", "P2",
     "—",
     "1. Bấm lần lượt vào tiêu đề Mã phiếu, Loại chi, Số tiền, Trạng thái, Người lập",
     "—",
     "- Không cột nào đổi thứ tự\n"
     "- ⚠️ Khác màn Phiếu thu vốn cho sắp xếp cột Số tiền"),

    (3, "Cột Số tiền định dạng phân cách nghìn", "P1",
     "Có phiếu chi tổng 1.234.567.890",
     "1. Tìm phiếu đó trên danh sách, đọc ô Số tiền",
     "—",
     "- Hiển thị đủ dấu phân cách nghìn, không mất chữ số"),

    (4, "Cột Ngày lập chỉ có ngày tháng năm", "P2",
     "—",
     "1. Đọc cột Ngày lập của vài dòng bất kỳ",
     "—",
     "- Hiển thị dạng ngày/tháng/năm, không kèm giờ phút"),

    (5, "Cột Khách hàng theo loại chi", "P0",
     "Có phiếu loại Chi trả nhà cung cấp gắn NCC-01, và phiếu loại Chi trả lại khách hàng gắn KH-01",
     "1. Tìm cả hai phiếu trên danh sách\n"
     "2. Đọc cột Khách hàng của từng phiếu",
     "—",
     "- Phiếu Chi trả nhà cung cấp hiện mã và tên NHÀ CUNG CẤP\n"
     "- Phiếu Chi trả lại khách hàng hiện mã và tên KHÁCH HÀNG"),

    (6, "Cột Khách hàng chỉ lấy dòng đầu tiên", "P0",
     "Phiếu PC-H có 3 dòng chi tiết với 3 đối tác khác nhau",
     "1. Tìm PC-H trên danh sách, đọc cột Khách hàng\n"
     "2. Mở chi tiết PC-H, đếm số đối tác trong bảng",
     "—",
     "- Ngoài danh sách chỉ hiện đối tác của dòng 1\n"
     "- Trong chi tiết thấy đủ 3 đối tác\n"
     "- ⚠️ Hiện trạng đã biết (mục 6), không phải lọc sai"),

    (7, "Cột Khách hàng trống với loại chi khác", "P2",
     "Có phiếu loại Chi khác và phiếu loại Chi thu nhập cho nhân viên",
     "1. Tìm hai phiếu đó trên danh sách, đọc cột Khách hàng",
     "—",
     "- Cả hai đều để trống ô Khách hàng\n"
     "- ⚠️ Đúng thiết kế — hai loại này không gắn khách hàng hay nhà cung cấp ở cột này"),

    (8, "Cột Phòng ban theo loại chi", "P0",
     "Phiếu PC-I loại Chi thu nhập cho nhân viên chọn Phòng ban chi là Kinh doanh 2; phiếu PC-J lập từ "
     "phiếu đề nghị của phòng Kinh doanh 1",
     "1. Tìm cả hai phiếu trên danh sách\n"
     "2. Đọc cột Phòng ban của từng phiếu",
     "—",
     "- PC-I hiện Kinh doanh 2 (phòng ban chọn trên phiếu chi)\n"
     "- PC-J hiện Kinh doanh 1 (phòng ban của phiếu đề nghị)"),

    (9, "Cột Người đề nghị và Người lập là hai người khác nhau", "P1",
     "Phiếu đề nghị do NV-B lập, phiếu chi do KT-1 lập",
     "1. Tìm phiếu chi đó, đọc cột Người đề nghị và cột Người lập",
     "—",
     "- Người đề nghị là NV-B, Người lập là KT-1, hai cột không trùng nhau"),

    (10, "Số tổng khớp với dữ liệu gốc", "P0",
     "Tài khoản B có quyền xem tổng công ty",
     "1. Mở chế độ Tất cả, bấm làm mới bộ lọc\n"
     "2. Đọc số tổng dưới bảng\n"
     "3. Đối chiếu với số phiếu chi trong dữ liệu gốc trừ đi phiếu nháp của người khác\n"
     "4. Lặp lại phép đối chiếu với bộ lọc theo khoảng ngày",
     "—",
     "- Bước 3 khớp chính xác\n"
     "- ⚠️ Bước 4 phải cộng bù phần bị ô Đến ngày làm rụng (mục 4)"),

    (11, "Bảng ở màn cần duyệt giống bảng danh sách thường", "P2",
     "Tài khoản TQ-1 có quyền thủ quỹ",
     "1. Dán đường dẫn màn Phiếu chi cần duyệt\n"
     "2. So sánh tiêu đề các cột với màn danh sách thường",
     "—",
     "- Cùng bộ 12 cột\n"
     "- Vẫn có nút Tạo mới ở phía trên bảng"),
]

SEC_IV = [
    (1, "Tạo phiếu chi từ màn Đề nghị thanh toán", "P0",
     "Tài khoản KT-1 có quyền Kế toán thanh toán; phiếu đề nghị chi DNC-01 đang ở trạng thái Đợi kế "
     "toán thanh toán tạo phiếu chi, có 2 dòng chi tiết",
     "1. Đăng nhập bằng KT-1, mở chi tiết DNC-01\n"
     "2. Bấm nút tạo phiếu chi\n"
     "3. Quan sát form vừa mở",
     "—",
     "- Mở form Tạo phiếu chi\n"
     "- Ô Số phiếu đề nghị điền sẵn mã DNC-01, có thông báo thêm thành công\n"
     "- Loại chi, Hình thức thanh toán, Loại tiền, Tỷ giá, Lý do chi đổ sẵn theo DNC-01\n"
     "- Bảng chi tiết đổ sẵn đúng 2 dòng"),

    (2, "Chọn phiếu đề nghị bằng cửa sổ tìm kiếm", "P0",
     "Có 3 phiếu đề nghị chi đang Đợi kế toán thanh toán tạo phiếu chi và 5 phiếu đề nghị ở các trạng "
     "thái khác",
     "1. Mở form Tạo phiếu chi từ nút Tạo mới\n"
     "2. Bấm kính lúp ở ô Số phiếu đề nghị\n"
     "3. Đọc danh sách trong cửa sổ, chọn một phiếu",
     "—",
     "- Cửa sổ chỉ liệt kê đúng 3 phiếu đang đợi lập phiếu chi\n"
     "- Có ô lọc Mã phiếu đề nghị chi và ô lọc Người lập\n"
     "- Chọn xong: form đổ đủ thông tin và chi tiết"),

    (3, "Tài khoản có tự chọn khi trả bằng tiền mặt", "P1",
     "Phiếu đề nghị DNC-02 có Hình thức thanh toán là tiền mặt, đối tượng là khách hàng",
     "1. Tạo phiếu chi từ DNC-02\n"
     "2. Đọc ô Tài khoản có",
     "—",
     "- Ô Tài khoản có tự chọn sẵn tài khoản tiền Việt Nam\n"
     "- Vẫn đổi sang tài khoản khác được"),

    (4, "Lập phiếu Chi thu nhập cho nhân viên không cần phiếu đề nghị", "P0",
     "Tài khoản KT-1; phòng Kinh doanh 2 có 5 nhân viên còn số dư phải trả và 3 nhân viên số dư bằng 0 "
     "ở cả 6 khoản",
     "1. Mở form Tạo phiếu chi từ nút Tạo mới\n"
     "2. Chọn Loại chi là Chi thu nhập cho nhân viên\n"
     "3. Chọn Phòng ban là Kinh doanh 2\n"
     "4. Đọc bảng chi tiết",
     "Loại chi: Chi thu nhập cho nhân viên · Phòng ban: Kinh doanh 2",
     "- Ô Số phiếu đề nghị KHÔNG bắt buộc, để trống được\n"
     "- Tài khoản có và Loại tiền tự đặt về tiền Việt Nam\n"
     "- Bảng nạp đúng 5 nhân viên còn số dư, KHÔNG nạp 3 nhân viên số dư bằng 0 (mục 3)\n"
     "- Mỗi dòng tách đủ 6 khoản: Chênh lệch nhân viên · Hoa hồng tháng · Hoa hồng quý · Thưởng quý · "
     "Tiền giao hàng · Chi phí khác"),

    (5, "Chưa chọn Phòng ban thì chưa nạp được nhân viên", "P1",
     "Đang mở form Tạo phiếu chi, đã chọn Loại chi là Chi thu nhập cho nhân viên",
     "1. Để trống ô Phòng ban\n"
     "2. Bấm nút nạp danh sách nhân viên",
     "Phòng ban: để trống",
     "- Hệ thống báo không tìm thấy phòng ban\n"
     "- Bảng chi tiết vẫn trống"),

    (6, "Đổi Phòng ban thì nạp lại danh sách nhân viên", "P1",
     "Đã nạp danh sách nhân viên của phòng Kinh doanh 2",
     "1. Đổi ô Phòng ban sang Kinh doanh 1\n"
     "2. Đọc lại bảng chi tiết",
     "Phòng ban: Kinh doanh 1",
     "- Bảng nạp lại theo nhân viên của Kinh doanh 1\n"
     "- Không còn dòng nào của Kinh doanh 2"),

    (7, "Số tiền chi mặc định bằng số dư", "P0",
     "Nhân viên NV-C có Chênh lệch nhân viên 3.000.000 và Hoa hồng tháng 2.000.000, các khoản còn lại 0",
     "1. Nạp danh sách nhân viên phòng của NV-C\n"
     "2. Đọc dòng của NV-C ở cả cặp cột số dư và số chi",
     "—",
     "- Cột số chi của Chênh lệch nhân viên điền sẵn 3.000.000\n"
     "- Cột số chi của Hoa hồng tháng điền sẵn 2.000.000\n"
     "- Ô tổng Số tiền chi của dòng là 5.000.000"),

    (8, "Sửa số chi thì tổng dòng và tổng bảng cập nhật", "P0",
     "Đang mở phiếu Chi thu nhập nhân viên với dòng NV-C ở ca trên",
     "1. Sửa số chi của Hoa hồng tháng xuống 1.000.000\n"
     "2. Đọc ô tổng của dòng và dòng Tổng cộng cuối bảng",
     "Hoa hồng tháng: 1.000.000",
     "- Tổng của dòng đổi thành 4.000.000\n"
     "- Dòng Tổng cộng của cả bảng giảm tương ứng"),

    (9, "Chặn chi vượt số dư từng khoản", "P0",
     "Nhân viên NV-C có Hoa hồng tháng số dư 2.000.000",
     "1. Sửa số chi của Hoa hồng tháng thành 5.000.000\n"
     "2. Bấm Lưu",
     "Hoa hồng tháng: 5.000.000",
     "- Hiện cảnh báo Số tiền chi theo mã vụ việc không được lớn hơn số dư\n"
     "- Phiếu KHÔNG được lưu"),

    (10, "Chặn khi tổng 6 khoản khác ô Số tiền chi của dòng", "P0",
     "Đang mở phiếu Chi thu nhập nhân viên",
     "1. Sửa ô Số tiền chi của dòng NV-C thành một số khác tổng 6 khoản\n"
     "2. Bấm Lưu",
     "—",
     "- Hiện cảnh báo Tổng số tiền chi theo mã vụ việc và tổng số tiền đề nghị chi khác nhau\n"
     "- Phiếu KHÔNG được lưu"),

    (11, "Phiếu ngoại tệ hiện đủ cặp cột quy đổi", "P0",
     "Phiếu đề nghị DNC-06 loại tiền là ngoại tệ, tỷ giá 25.000, dòng 1 đề nghị chi 1.000",
     "1. Tạo phiếu chi từ DNC-06\n"
     "2. Đọc tiêu đề bảng chi tiết và dòng 1",
     "—",
     "- Nhóm Số tiền đề nghị chi và nhóm Số tiền chi đều tách 2 cột: tên loại ngoại tệ và VND\n"
     "- Dòng 1: cột ngoại tệ 1.000, cột VND 25.000.000"),

    (12, "Sửa Tỷ giá thì cột quy đổi tính lại", "P1",
     "Đang mở phiếu chi từ DNC-06",
     "1. Sửa ô Tỷ giá thành 26.000\n"
     "2. Đọc lại cột VND của dòng 1 và dòng Tổng cộng",
     "Tỷ giá: 26.000",
     "- Cột VND dòng 1 đổi thành 26.000.000, dòng Tổng cộng đổi theo"),

    (13, "Bảng con phân bổ theo phiếu yêu cầu xuất hàng", "P0",
     "Phiếu đề nghị DNC-07 có 1 dòng gắn hợp đồng nguyên tắc, không tích chi đầu kỳ, có 3 phiếu yêu cầu "
     "xuất hàng",
     "1. Tạo phiếu chi từ DNC-07\n"
     "2. Quan sát ô hợp đồng của dòng 1",
     "—",
     "- Dưới ô hợp đồng bung ra bảng con theo từng phiếu yêu cầu xuất hàng\n"
     "- Có ô nhập số tiền phân bổ cho từng phiếu"),

    (14, "Lưu nháp phiếu chi", "P0",
     "Đang mở form Tạo phiếu chi từ DNC-01, đã nhập Người nhận tiền là Nguyễn Văn A",
     "1. Bấm nút Lưu\n"
     "2. Đọc thông báo và màn hình đích\n"
     "3. Mở lại phiếu đề nghị DNC-01, đọc trạng thái",
     "Người nhận tiền: Nguyễn Văn A",
     "- Thông báo Thêm phiếu chi tiền thành công\n"
     "- Chuyển về danh sách chế độ Tất cả, phiếu mới ở trạng thái Đang tạo\n"
     "- ⚠️ DNC-01 VẪN ở trạng thái Đợi kế toán thanh toán tạo phiếu chi"),

    (15, "Lưu và gửi duyệt phiếu chi loại thường", "P0",
     "Đang mở form Tạo phiếu chi từ DNC-01 loại Chi trả nhà cung cấp, đã nhập đủ thông tin bắt buộc",
     "1. Bấm nút Lưu và gửi duyệt\n"
     "2. Đọc thông báo\n"
     "3. Mở danh sách, đọc trạng thái phiếu vừa tạo\n"
     "4. Mở phiếu đề nghị DNC-01, đọc trạng thái",
     "—",
     "- Thông báo Phiếu chi tiền tạo thành công\n"
     "- Phiếu chi ở trạng thái Chờ chi tiền\n"
     "- DNC-01 chuyển sang trạng thái đợi duyệt phiếu chi\n"
     "- Thủ quỹ nhận được thông báo"),

    (16, "Lưu và gửi duyệt phiếu Chi thu nhập cho nhân viên", "P0",
     "Đang mở form phiếu Chi thu nhập cho nhân viên, đã nạp nhân viên và nhập đủ thông tin bắt buộc",
     "1. Bấm nút Lưu và gửi duyệt\n"
     "2. Mở danh sách, đọc trạng thái phiếu vừa tạo",
     "—",
     "- Phiếu ở trạng thái Chờ KT trưởng duyệt, KHÔNG phải Chờ chi tiền\n"
     "- Người có quyền Kế toán trưởng duyệt phiếu chi nhận được thông báo\n"
     "- Thủ quỹ CHƯA nhận thông báo nào"),

    (17, "Mã phiếu sinh tự động và tăng dần", "P0",
     "Công ty của KT-1 có mã TPE; trong tháng hiện tại đã có phiếu chi TPE.PC0826.00016",
     "1. Tạo và lưu 2 phiếu chi liên tiếp\n"
     "2. Đọc Mã phiếu của cả hai trên danh sách",
     "—",
     "- Mã lần lượt là TPE.PC0826.00017 và TPE.PC0826.00018\n"
     "- Không trùng mã, không nhảy số"),

    (18, "Lập hai phiếu chi cho cùng một phiếu đề nghị", "P0",
     "Phiếu đề nghị DNC-09 đã được lập phiếu chi và lưu thành công",
     "1. Mở form Tạo phiếu chi mới\n"
     "2. Chọn lại DNC-09 ở cửa sổ Số phiếu đề nghị nếu còn liệt kê\n"
     "3. Nhập đủ thông tin rồi bấm Lưu\n"
     "4. Lọc danh sách theo mã DNC-09",
     "—",
     "- ⚠️ Hệ thống KHÔNG chặn như màn Phiếu thu (mục 9 ghi chú 5)\n"
     "- Nếu tạo được phiếu chi thứ hai cho cùng một đề nghị thì ghi Failed kèm cả hai mã phiếu"),

    (19, "Gán tự động công ty, phòng ban, bộ phận", "P1",
     "KT-1 thuộc công ty 3, phòng Kế toán",
     "1. KT-1 tạo và lưu một phiếu chi\n"
     "2. Mở chế độ Tất cả bằng tài khoản có quyền xem tổng công ty\n"
     "3. Lọc Công ty là công ty 3 và Phòng ban là Kế toán",
     "—",
     "- Phiếu vừa tạo nằm trong kết quả lọc\n"
     "- Đơn vị của phiếu lấy theo hồ sơ nhân sự của KT-1"),

    (20, "Rollback khi lỗi giữa chừng", "P1",
     "—",
     "1. Giả lập lỗi khi lưu chi tiết phiếu chi\n"
     "2. Bấm Lưu\n"
     "3. Mở danh sách tìm phiếu vừa thao tác",
     "—",
     "- Thông báo Thêm phiếu chi thất bại\n"
     "- Không còn bản ghi phiếu chi lẫn dòng chi tiết nào được tạo"),

    (21, "Mở màn Sửa phiếu chi", "P0",
     "Tài khoản KT-1; phiếu PC-N ở trạng thái Đang tạo do KT-1 lập",
     "1. Bấm bánh răng ở PC-N, bấm Sửa phiếu chi\n"
     "2. Đọc các ô trên form",
     "—",
     "- Form hiện thêm ô Mã phiếu (bị khóa)\n"
     "- Có thêm ô Người đề nghị và Phòng ban, đều bị khóa\n"
     "- Ô Người nhận tiền và Tài khoản có sửa được"),

    (22, "Sửa Người nhận tiền và Tài khoản có rồi lưu", "P0",
     "Đang mở màn Sửa của PC-N, Người nhận tiền đang là Nguyễn Văn A",
     "1. Đổi Người nhận tiền thành Trần Thị B\n"
     "2. Đổi Tài khoản có sang một tài khoản khác\n"
     "3. Bấm Lưu\n"
     "4. Mở lại chi tiết PC-N",
     "Người nhận tiền: Trần Thị B",
     "- Thông báo Cập nhật phiếu chi tiền thành công\n"
     "- Mở lại thấy đúng hai giá trị vừa sửa"),

    (23, "Sửa Lý do chi và Ghi chú rồi lưu", "P0",
     "Đang mở màn Sửa của PC-N, Lý do chi đang là Thanh toán đợt 1",
     "1. Đổi Lý do chi thành Thanh toán đợt 2\n"
     "2. Nhập Ghi chú là Ghi chú kiểm thử\n"
     "3. Bấm Lưu\n"
     "4. Mở lại chi tiết PC-N, đọc hai ô đó",
     "Lý do chi: Thanh toán đợt 2 · Ghi chú: Ghi chú kiểm thử",
     "- Màn hình báo Cập nhật phiếu chi tiền thành công\n"
     "- ⚠️ Mở lại thấy Lý do chi VẪN là Thanh toán đợt 1 và Ghi chú VẪN trống — hai giá trị không được "
     "lưu (mục 9 ghi chú 3)\n"
     "- Ghi nhận Failed"),

    (24, "Sửa Hình thức thanh toán, Loại tiền, Tỷ giá rồi lưu", "P0",
     "Đang mở màn Sửa của một phiếu chi ngoại tệ",
     "1. Đổi Hình thức thanh toán sang chuyển khoản\n"
     "2. Đổi Tỷ giá thành một số khác\n"
     "3. Bấm Lưu, mở lại chi tiết",
     "—",
     "- ⚠️ Cả hai giá trị đều KHÔNG được lưu, dù báo cập nhật thành công (mục 9 ghi chú 3)\n"
     "- Ghi nhận Failed"),

    (25, "Sửa rồi gửi duyệt", "P0",
     "Đang mở màn Sửa của PC-N ở trạng thái Đang tạo, loại Chi trả nhà cung cấp",
     "1. Bấm Lưu và gửi duyệt\n"
     "2. Mở danh sách, đọc trạng thái PC-N\n"
     "3. Mở phiếu đề nghị gốc, đọc trạng thái",
     "—",
     "- PC-N chuyển sang Chờ chi tiền\n"
     "- Phiếu đề nghị gốc chuyển sang trạng thái đợi duyệt phiếu chi\n"
     "- Thủ quỹ nhận được thông báo"),

    (26, "Dán thẳng đường dẫn sửa phiếu đã gửi duyệt", "P0",
     "Tài khoản KT-1 có quyền Kế toán thanh toán; phiếu PC-A đang ở trạng thái Chờ chi tiền",
     "1. Dán thẳng đường dẫn sửa của PC-A\n"
     "2. Nếu form mở ra thì sửa Người nhận tiền rồi bấm Lưu\n"
     "3. Mở lại chi tiết PC-A",
     "—",
     "- ⚠️ Form VẪN mở được và VẪN lưu được, hệ thống chỉ ẩn nút chứ không chặn\n"
     "- Ghi nhận Failed, mô tả rõ phiếu ở trạng thái nào vẫn sửa được"),

    (27, "Xem chi tiết phiếu đã duyệt", "P1",
     "Phiếu PC-B ở trạng thái Đã duyệt",
     "1. Mở chi tiết PC-B, soát các ô và các nút",
     "—",
     "- Hiện đủ thông tin phiếu và bảng chi tiết\n"
     "- Không có nút duyệt, nút Sửa, nút Xóa\n"
     "- Vẫn có nút In, Xuất Excel và Quay lại"),
]

SEC_V = [
    (1, "Kế toán trưởng duyệt phiếu Chi thu nhập nhân viên", "P0",
     "Tài khoản KTT-1 có quyền Kế toán trưởng duyệt phiếu chi; phiếu PC-01 loại Chi thu nhập cho nhân "
     "viên đang ở Chờ KT trưởng duyệt",
     "1. Đăng nhập bằng KTT-1, mở chi tiết PC-01\n"
     "2. Bấm nút Kế toán duyệt phiếu chi\n"
     "3. Đọc thông báo và màn hình đích\n"
     "4. Mở lại chi tiết PC-01",
     "—",
     "- Hệ thống chuyển sang màn Phiếu chi đã duyệt\n"
     "- PC-01 chuyển sang trạng thái Chờ chi tiền, chưa phải Đã duyệt\n"
     "- Thủ quỹ nhận được thông báo cần duyệt"),

    (2, "Thủ quỹ duyệt phiếu chi thành công", "P0",
     "Tài khoản TQ-1 có quyền Thủ quỹ duyệt phiếu chi; phiếu PC-02 loại Chi trả nhà cung cấp đang ở "
     "Chờ chi tiền, gắn phiếu đề nghị DNC-02",
     "1. Đăng nhập bằng TQ-1, mở chi tiết PC-02\n"
     "2. Bấm nút Duyệt phiếu chi\n"
     "3. Đọc thông báo\n"
     "4. Mở lại chi tiết PC-02 và mở DNC-02\n"
     "5. Mở sổ kế toán",
     "—",
     "- Thông báo Duyệt phiếu chi thành công\n"
     "- PC-02 ở trạng thái Đã duyệt, Người duyệt là TQ-1\n"
     "- DNC-02 chuyển sang trạng thái đã duyệt phiếu chi\n"
     "- Sổ kế toán có bút toán ghi Nợ và ghi Có tương ứng"),

    (3, "Ngày hạch toán đóng dấu ngày thủ quỹ bấm duyệt", "P1",
     "Phiếu PC-L lập ngày 10/08/2026, hôm nay là 20/08/2026",
     "1. TQ-1 duyệt PC-L hôm nay\n"
     "2. Mở lại chi tiết, tìm Ngày hạch toán\n"
     "3. Mở sổ kế toán, đọc ngày của bút toán",
     "—",
     "- Ngày hạch toán là 20/08/2026, không phải 10/08/2026\n"
     "- Người dùng không chọn được ngày này"),

    (4, "Số tiền chi được đẩy ngược về phiếu đề nghị", "P0",
     "Phiếu PC-02 có dòng chi 8.000.000 trong khi phiếu đề nghị DNC-02 đề nghị 10.000.000",
     "1. TQ-1 duyệt PC-02\n"
     "2. Mở chi tiết DNC-02, đọc cột số tiền đã duyệt chi của dòng tương ứng",
     "—",
     "- Dòng trên DNC-02 ghi nhận số tiền chi thực tế 8.000.000\n"
     "- Số đề nghị 10.000.000 vẫn giữ nguyên để đối chiếu"),

    (5, "Duyệt phiếu Chi thu nhập nhân viên thì ghi sổ chạy nền", "P0",
     "Phiếu PC-01 loại Chi thu nhập cho nhân viên đang ở Chờ chi tiền",
     "1. TQ-1 bấm Duyệt phiếu chi\n"
     "2. Mở ngay sổ kế toán, tìm bút toán của PC-01\n"
     "3. Chờ vài phút rồi mở lại sổ kế toán",
     "—",
     "- Phiếu chuyển sang Đã duyệt ngay\n"
     "- ⚠️ Bút toán CHƯA có ở bước 2, chỉ xuất hiện ở bước 3 vì hệ thống ghi sổ chạy nền (mục 9 ghi chú "
     "13)\n"
     "- Không kết luận mất bút toán khi chưa chờ đủ"),

    (6, "Cảnh báo lệch tiền ở màn duyệt", "P0",
     "Phiếu PC-K có dòng gắn hợp đồng nguyên tắc, tổng phân bổ theo phiếu yêu cầu xuất hàng KHÁC số "
     "tiền chi của dòng",
     "1. TQ-1 mở chi tiết PC-K\n"
     "2. Bấm nút Duyệt phiếu chi\n"
     "3. Quan sát màn hình và trạng thái phiếu",
     "—",
     "- Kỳ vọng nghiệp vụ: hiện cảnh báo lệch tiền và chặn duyệt\n"
     "- ⚠️ Thực tế cảnh báo KHÔNG hiện, phiếu duyệt lọt (mục 9 ghi chú 2)\n"
     "- Ghi nhận Failed kèm mã phiếu và số tiền lệch"),

    (7, "Duyệt lại phiếu đã duyệt", "P0",
     "Phiếu PC-02 đã ở trạng thái Đã duyệt",
     "1. Dùng công cụ kiểm thử gọi lại thao tác duyệt cho PC-02\n"
     "2. Mở sổ kế toán, đếm số bút toán của PC-02",
     "Trạng thái gửi lên: Đã duyệt",
     "- Hệ thống từ chối vì phiếu không còn ở Chờ chi tiền\n"
     "- Bút toán KHÔNG bị ghi hai lần"),

    (8, "Thủ quỹ hủy phiếu chi", "P0",
     "Phiếu PC-M đang ở Chờ chi tiền, gắn phiếu đề nghị DNC-M",
     "1. TQ-1 mở chi tiết PC-M, nhập Ghi chú là Không đủ tiền quỹ\n"
     "2. Bấm Hủy phiếu chi, bấm Xác nhận\n"
     "3. Mở danh sách, đọc trạng thái PC-M\n"
     "4. Mở DNC-M, đọc trạng thái\n"
     "5. Mở sổ kế toán",
     "Ghi chú: Không đủ tiền quỹ",
     "- Thông báo Hủy phiếu chi thành công\n"
     "- PC-M ở trạng thái Hủy, DNC-M chuyển sang trạng thái Hủy\n"
     "- KHÔNG có bút toán nào được ghi"),

    (9, "Ghi chú lý do hủy không được lưu lại", "P0",
     "Vừa hủy PC-M ở ca trên với Ghi chú là Không đủ tiền quỹ",
     "1. Mở lại chi tiết PC-M\n"
     "2. Đọc ô Ghi chú",
     "—",
     "- ⚠️ Ô Ghi chú TRỐNG, nội dung lý do hủy không được lưu (mục 9 ghi chú 4)\n"
     "- Ghi nhận Failed — bắt buộc nhập mà không lưu là mất dấu vết nghiệp vụ"),

    (10, "Kế toán trưởng hủy phiếu chi", "P0",
     "Phiếu PC-01 đang ở Chờ KT trưởng duyệt",
     "1. KTT-1 mở chi tiết PC-01, nhập Ghi chú\n"
     "2. Bấm Hủy phiếu chi, bấm Xác nhận\n"
     "3. Mở danh sách, đọc trạng thái",
     "—",
     "- PC-01 chuyển sang trạng thái Hủy\n"
     "- Phiếu không đi tiếp sang thủ quỹ"),

    (11, "Bấm Hủy rồi chọn không xác nhận", "P1",
     "Phiếu PC-M đang ở Chờ chi tiền",
     "1. Bấm Hủy phiếu chi\n"
     "2. Trên hộp thoại, bấm nút Hủy để đóng\n"
     "3. Tải lại danh sách",
     "—",
     "- Hộp thoại đóng, phiếu vẫn ở Chờ chi tiền"),

    (12, "Hủy phiếu khi chưa nhập Ghi chú", "P0",
     "Phiếu PC-M đang ở Chờ chi tiền, ô Ghi chú đang trống",
     "1. Bấm Hủy phiếu chi, bấm Xác nhận\n"
     "2. Quan sát màn hình",
     "Ghi chú: để trống",
     "- Hộp thoại xác nhận hiện ra trước\n"
     "- Sau khi xác nhận: hệ thống báo lỗi Bắt buộc nhập ở ô Ghi chú\n"
     "- Phiếu KHÔNG bị hủy"),

    (13, "Thông báo tới thủ quỹ khi gửi duyệt phiếu loại thường", "P0",
     "Tài khoản TQ-1 và TQ-2 đều có quyền Thủ quỹ duyệt phiếu chi",
     "1. KT-1 bấm Lưu và gửi duyệt một phiếu loại Chi trả nhà cung cấp\n"
     "2. Đăng nhập bằng TQ-1, mở khu vực thông báo, bấm vào thông báo mới nhất\n"
     "3. Kiểm tra thông báo của TQ-2",
     "—",
     "- Cả TQ-1 và TQ-2 nhận thông báo có một phiếu chi tiền cần duyệt kèm tên người lập\n"
     "- Bấm vào thông báo mở đúng chi tiết phiếu vừa gửi"),

    (14, "Thông báo tới kế toán trưởng khi gửi duyệt phiếu chi thu nhập nhân viên", "P0",
     "Tài khoản KTT-1 có quyền Kế toán trưởng duyệt phiếu chi",
     "1. KT-1 bấm Lưu và gửi duyệt một phiếu loại Chi thu nhập cho nhân viên\n"
     "2. Đăng nhập bằng KTT-1, mở khu vực thông báo\n"
     "3. Đăng nhập bằng TQ-1, mở khu vực thông báo",
     "—",
     "- KTT-1 nhận thông báo cần duyệt\n"
     "- TQ-1 CHƯA nhận thông báo nào ở bước này"),

    (15, "Thông báo tới thủ quỹ sau khi kế toán trưởng duyệt", "P0",
     "Phiếu PC-01 vừa được KTT-1 bấm Kế toán duyệt phiếu chi",
     "1. Đăng nhập bằng TQ-1, mở khu vực thông báo\n"
     "2. Bấm vào thông báo mới nhất",
     "—",
     "- TQ-1 nhận thông báo có phiếu chi cần duyệt\n"
     "- Bấm vào mở đúng PC-01, trạng thái đang là Chờ chi tiền"),

    (16, "Chỉ Lưu nháp thì không gửi thông báo", "P1",
     "—",
     "1. KT-1 tạo phiếu chi và bấm Lưu (không gửi duyệt)\n"
     "2. Kiểm tra thông báo của TQ-1 và KTT-1",
     "—",
     "- Không ai nhận thông báo nào\n"
     "- Phiếu cũng không xuất hiện ở màn Phiếu chi cần duyệt"),

    (17, "Người lập tự đứng tên ở ô người kế toán duyệt", "P0",
     "Tài khoản KT-1 lập phiếu loại Chi thu nhập cho nhân viên",
     "1. KT-1 bấm Lưu và gửi duyệt\n"
     "2. Dán đường dẫn màn Phiếu chi đã duyệt bằng chính KT-1\n"
     "3. Tìm phiếu vừa gửi",
     "—",
     "- ⚠️ Phiếu đã nằm ở màn Đã duyệt của KT-1 dù kế toán trưởng chưa bấm gì (mục 9 ghi chú 11)\n"
     "- Ghi nhận Failed"),

    (18, "Duyệt phiếu chi ngoại tệ", "P1",
     "Phiếu PC-P là phiếu ngoại tệ, tỷ giá 25.000, tổng chi 2.000 ngoại tệ",
     "1. TQ-1 duyệt PC-P\n"
     "2. Đọc cột Số tiền trên danh sách\n"
     "3. Mở sổ kế toán, đọc số tiền và tỷ giá của bút toán",
     "—",
     "- Cột Số tiền hiện 50.000.000\n"
     "- Bút toán ghi cả số ngoại tệ 2.000 và số quy đổi 50.000.000, kèm tỷ giá 25.000"),

    (19, "Duyệt phiếu chi có nhiều đối tác", "P1",
     "Phiếu PC-H có 3 dòng với 3 nhà cung cấp khác nhau",
     "1. TQ-1 duyệt PC-H\n"
     "2. Mở sổ kế toán, đếm bút toán ghi Nợ\n"
     "3. Mở báo cáo công nợ của từng nhà cung cấp",
     "—",
     "- Sinh bút toán ghi Nợ riêng cho từng nhà cung cấp\n"
     "- Công nợ phải trả của cả 3 nhà cung cấp đều giảm đúng phần của mình"),

    (20, "Phiếu chi thu nhập nhân viên khi hủy không đụng phiếu đề nghị", "P1",
     "Phiếu PC-01 loại Chi thu nhập cho nhân viên, không gắn phiếu đề nghị nào",
     "1. KTT-1 nhập Ghi chú rồi bấm Hủy phiếu chi\n"
     "2. Mở danh sách, đọc trạng thái PC-01\n"
     "3. Mở màn Đề nghị thanh toán, kiểm tra không có phiếu nào bị đổi trạng thái oan",
     "—",
     "- PC-01 chuyển sang Hủy\n"
     "- Không phiếu đề nghị nào bị ảnh hưởng"),

    (21, "Duyệt phiếu chi bằng tài khoản không phải người được giao", "P1",
     "Phiếu PC-02 đang ở Chờ chi tiền, thuộc công ty 3; TQ-9 có quyền thủ quỹ nhưng thuộc công ty 1",
     "1. Đăng nhập bằng TQ-9\n"
     "2. Dán đường dẫn chi tiết của PC-02",
     "—",
     "- Hệ thống đưa sang màn báo không tìm thấy dữ liệu\n"
     "- ⚠️ Quyền duyệt chỉ mở phiếu CÙNG CÔNG TY (mục 7)"),

    (22, "Kiểm tra lại toàn bộ luồng trạng thái", "P0",
     "Một phiếu loại thường và một phiếu loại Chi thu nhập cho nhân viên, cả hai đang ở Đang tạo",
     "1. Gửi duyệt cả hai, ghi lại trạng thái\n"
     "2. Duyệt tiếp từng bước theo đúng vai, ghi lại trạng thái sau mỗi bước",
     "—",
     "- Phiếu loại thường đi qua đúng 3 trạng thái: Đang tạo → Chờ chi tiền → Đã duyệt\n"
     "- Phiếu chi thu nhập nhân viên đi qua đúng 4 trạng thái: Đang tạo → Chờ KT trưởng duyệt → Chờ chi "
     "tiền → Đã duyệt\n"
     "- Không bước nào bị nhảy cóc"),
]

SEC_VI = [
    (1, "Xóa phiếu chi ở trạng thái Đang tạo từ danh sách", "P0",
     "Tài khoản KT-1; phiếu PC-N ở trạng thái Đang tạo do KT-1 lập",
     "1. Bấm bánh răng ở PC-N, bấm Xóa\n"
     "2. Bấm Xác nhận trên hộp thoại\n"
     "3. Tìm lại PC-N trên danh sách",
     "—",
     "- Thông báo Xóa phiếu chi thành công\n"
     "- PC-N biến mất khỏi danh sách"),

    (2, "Xóa phiếu chi từ màn chi tiết", "P1",
     "Phiếu PC-N ở trạng thái Đang tạo do KT-1 lập",
     "1. Mở chi tiết PC-N bằng KT-1\n"
     "2. Bấm nút Xóa, bấm Xác nhận\n"
     "3. Quan sát màn hình đích",
     "—",
     "- Xóa thành công và chuyển về danh sách phiếu chi"),

    (3, "Bấm Xóa rồi chọn không xác nhận", "P1",
     "Phiếu PC-N ở trạng thái Đang tạo",
     "1. Bấm Xóa\n"
     "2. Trên hộp thoại, bấm nút Hủy\n"
     "3. Tải lại danh sách",
     "—",
     "- Hộp thoại đóng, phiếu vẫn còn nguyên"),

    (4, "Phiếu đã gửi duyệt không có nút Xóa", "P0",
     "Phiếu PC-A ở trạng thái Chờ chi tiền",
     "1. Bấm bánh răng ở PC-A, soát các mục\n"
     "2. Mở chi tiết PC-A, soát các nút",
     "—",
     "- Cả hai chỗ đều không có mục Xóa"),

    (5, "Dán thẳng đường dẫn xóa phiếu đã duyệt", "P0",
     "Tài khoản KT-1; phiếu PC-B ở trạng thái Đã duyệt và đã ghi sổ",
     "1. Dán thẳng đường dẫn xóa của PC-B\n"
     "2. Tìm lại PC-B trên danh sách\n"
     "3. Mở sổ kế toán, tìm bút toán của PC-B",
     "—",
     "- ⚠️ Phiếu BỊ XÓA thật kèm thông báo thành công (mục 9 ghi chú 6)\n"
     "- Bút toán vẫn còn trong sổ, thành bút toán mồ côi\n"
     "- Ghi nhận Failed"),

    (6, "Dòng chi tiết không bị xóa theo phiếu", "P0",
     "Phiếu PC-R ở trạng thái Đang tạo, có 3 dòng chi tiết",
     "1. Xóa PC-R\n"
     "2. Mở các báo cáo có dùng số liệu chi tiết phiếu chi, đối chiếu tổng tiền",
     "—",
     "- ⚠️ Ba dòng chi tiết của PC-R vẫn còn trong kho dữ liệu (mục 9 ghi chú 7)\n"
     "- Nếu báo cáo nào cộng nhầm phần này thì ghi Failed kèm tên báo cáo"),

    (7, "Phiếu đề nghị kẹt trạng thái sau khi xóa phiếu chi", "P0",
     "Phiếu đề nghị DNC-10 đã có phiếu chi PC-Q ở Chờ chi tiền, DNC-10 đang ở trạng thái đợi duyệt "
     "phiếu chi",
     "1. Xóa PC-Q\n"
     "2. Mở chi tiết DNC-10, đọc trạng thái\n"
     "3. Mở form Tạo phiếu chi mới, tìm DNC-10 trong cửa sổ chọn",
     "—",
     "- ⚠️ DNC-10 VẪN ở trạng thái đợi duyệt phiếu chi, không trở về đợi lập phiếu chi\n"
     "- Cửa sổ chọn không liệt kê DNC-10 nữa, phiếu đề nghị bị kẹt (mục 9 ghi chú 8)\n"
     "- Ghi nhận Failed"),
]

SEC_VII = [
    (1, "In phiếu chi một đối tác", "P0",
     "Phiếu PC-S loại Chi trả nhà cung cấp, chỉ có 1 dòng chi tiết, đã duyệt",
     "1. Bấm bánh răng ở PC-S, bấm In\n"
     "2. Quan sát bản in",
     "—",
     "- Ra mẫu Phiếu chi tiền\n"
     "- Có đủ 2 liên, in trên CÙNG MỘT trang\n"
     "- Ô Liên số ghi lần lượt 1 và 2"),

    (2, "In phiếu chi nhiều đối tác", "P0",
     "Phiếu PC-H loại Chi trả nhà cung cấp, có 3 dòng chi tiết",
     "1. Bấm In ở PC-H\n"
     "2. Đếm số trang và số liên",
     "—",
     "- Ra mẫu Phiếu chi tiền nhiều khách hàng\n"
     "- Hai liên nằm ở HAI trang riêng\n"
     "- Bảng chi tiết liệt kê đủ 3 đối tác"),

    (3, "In phiếu Chi thu nhập cho nhân viên", "P0",
     "Phiếu PC-01 loại Chi thu nhập cho nhân viên có 5 dòng nhân viên",
     "1. Bấm In ở PC-01\n"
     "2. Đếm số liên và soát bảng trong bản in",
     "—",
     "- Ra mẫu Phiếu chi thu nhập nhân viên\n"
     "- ⚠️ Chỉ có MỘT liên, khác hẳn các loại chi còn lại (mục 8)\n"
     "- Bảng liệt kê đủ 5 nhân viên và các khoản chi"),

    (4, "In phiếu Thanh toán chi phí vận chuyển NCC", "P1",
     "Có phiếu chi loại Thanh toán chi phí vận chuyển NCC",
     "1. Bấm In ở phiếu đó\n"
     "2. Đếm số liên và số trang",
     "—",
     "- Ra mẫu Phiếu chi tiền, 2 liên trên cùng một trang, không phụ thuộc số dòng chi tiết"),

    (5, "Bản in phiếu ngoại tệ", "P1",
     "Phiếu PC-P là phiếu ngoại tệ, tỷ giá lưu trong phiếu là 25.000",
     "1. Bấm In ở PC-P\n"
     "2. Đọc dòng tỷ giá và cột số tiền",
     "—",
     "- Bản in có dòng tỷ giá và dòng số tiền quy đổi\n"
     "- Đối chiếu tỷ giá in ra với tỷ giá lưu trong phiếu, ghi nhận nếu lệch"),

    (6, "Nội dung bản in khớp dữ liệu", "P0",
     "Phiếu PC-S đã duyệt",
     "1. Mở chi tiết PC-S, ghi lại Người nhận tiền, Lý do chi, số tiền\n"
     "2. Bấm In, đối chiếu từng mục",
     "—",
     "- Số phiếu, Người nhận tiền, Lý do chi, danh sách hợp đồng và số tiền đều khớp\n"
     "- Dòng Bằng chữ đọc đúng tổng tiền\n"
     "- Không còn ô trống dạng mã thay thế chưa được điền"),

    (7, "In phiếu chưa duyệt", "P1",
     "Phiếu PC-A đang ở Chờ chi tiền",
     "1. Bấm In ở PC-A\n"
     "2. Đọc số tiền và dòng Bằng chữ",
     "—",
     "- Vẫn in được, không bị chặn\n"
     "- Số tiền lấy theo số tiền chi đang có trên phiếu"),

    (8, "Xuất Excel", "P0",
     "Phiếu PC-S mã TPE.PC0826.00017 đã duyệt",
     "1. Bấm bánh răng ở PC-S, bấm Xuất Excel\n"
     "2. Mở tệp vừa tải\n"
     "3. Đối chiếu số tiền, đối tác, số hợp đồng với màn chi tiết",
     "—",
     "- Tên tệp có kèm mã phiếu TPE.PC0826.00017\n"
     "- Tệp mở được, không báo hỏng, các giá trị khớp màn chi tiết"),

    (9, "In và Xuất Excel từ màn chi tiết", "P1",
     "Phiếu PC-S đã duyệt",
     "1. Mở chi tiết PC-S\n"
     "2. Bấm nút In, rồi bấm nút Xuất Excel",
     "—",
     "- Nút In mở bản in ở thẻ mới\n"
     "- Nút Xuất Excel tải tệp về, nội dung giống khi xuất từ danh sách"),

    (10, "In và Xuất Excel với phiếu không tồn tại", "P2",
     "—",
     "1. Dán đường dẫn in với một mã số không có trong hệ thống\n"
     "2. Làm tương tự với đường dẫn xuất Excel",
     "Mã số: 999999",
     "- Cả hai đều báo không tìm thấy dữ liệu, không treo trang"),
]

SEC_VIII = [
    (1, "Bỏ trống Loại chi", "P0",
     "Đang mở form Tạo phiếu chi, chưa chọn gì",
     "1. Nhập Người nhận tiền rồi bấm Lưu",
     "Loại chi: để trống",
     "- Hệ thống báo bắt buộc nhập Loại chi, không tạo phiếu"),

    (2, "Bỏ trống Tài khoản có", "P0",
     "Đang mở form Tạo phiếu chi đã chọn phiếu đề nghị",
     "1. Bỏ chọn ô Tài khoản có\n"
     "2. Nhập đủ các ô còn lại rồi bấm Lưu",
     "Tài khoản có: để rỗng",
     "- Lỗi đỏ Bắt buộc nhập hiện dưới ô Tài khoản có\n"
     "- Không tạo phiếu"),

    (3, "Bỏ trống Người nhận tiền", "P0",
     "Đang mở form Tạo phiếu chi đã chọn phiếu đề nghị",
     "1. Để trống ô Người nhận tiền rồi bấm Lưu",
     "Người nhận tiền: để trống",
     "- Lỗi đỏ Bắt buộc nhập hiện dưới ô Người nhận tiền\n"
     "- Không tạo phiếu"),

    (4, "Bỏ trống Số phiếu đề nghị với loại chi cần đề nghị", "P0",
     "Đang mở form Tạo phiếu chi, chọn Loại chi là Chi trả nhà cung cấp nhưng không chọn phiếu đề nghị",
     "1. Nhập Người nhận tiền và Tài khoản có\n"
     "2. Bấm Lưu",
     "Số phiếu đề nghị: để trống",
     "- Hệ thống báo bắt buộc nhập Số phiếu đề nghị\n"
     "- Không tạo phiếu"),

    (5, "Bỏ trống Số phiếu đề nghị với loại Chi thu nhập nhân viên", "P0",
     "Đang mở form Tạo phiếu chi, chọn Loại chi là Chi thu nhập cho nhân viên, đã nạp nhân viên",
     "1. Để trống ô Số phiếu đề nghị\n"
     "2. Nhập đủ Người nhận tiền, Lý do chi, Phòng ban rồi bấm Lưu",
     "Số phiếu đề nghị: để trống",
     "- Lưu thành công\n"
     "- ⚠️ Đúng thiết kế — loại này không cần phiếu đề nghị (mục 1)"),

    (6, "Bỏ trống Lý do chi với loại Chi thu nhập nhân viên", "P0",
     "Đang mở form phiếu Chi thu nhập cho nhân viên",
     "1. Để trống ô Lý do chi rồi bấm Lưu",
     "Lý do chi: để trống",
     "- Hệ thống báo bắt buộc nhập Lý do chi\n"
     "- Không tạo phiếu"),

    (7, "Bỏ trống Tài khoản nợ ở dòng chi tiết", "P0",
     "Đang mở form Tạo phiếu chi với 3 dòng chi tiết",
     "1. Ở dòng 2, bỏ chọn ô tài khoản nợ\n"
     "2. Bấm Lưu",
     "—",
     "- Lỗi Bắt buộc nhập hiện ở ĐÚNG DÒNG 2\n"
     "- Dòng 1 và dòng 3 không bị báo lỗi"),

    (8, "Bỏ trống Ghi chú khi hủy phiếu", "P0",
     "Phiếu PC-M đang ở Chờ chi tiền",
     "1. Để trống ô Ghi chú\n"
     "2. Bấm Hủy phiếu chi, bấm Xác nhận",
     "Ghi chú: để trống",
     "- Hệ thống báo bắt buộc nhập Ghi chú\n"
     "- Phiếu không bị hủy"),

    (9, "Nhập số tiền phân bổ là số âm", "P0",
     "Đang mở phiếu chi có bảng con phân bổ theo phiếu yêu cầu xuất hàng",
     "1. Nhập -1.000.000 vào ô số tiền phân bổ của một phiếu xuất\n"
     "2. Bấm Lưu",
     "Số tiền phân bổ: -1.000.000",
     "- Hệ thống chặn, báo lỗi ở đúng dòng\n"
     "- Không lưu giá trị âm"),

    (10, "Nhập chữ vào ô số tiền", "P1",
     "Đang mở form Tạo phiếu chi",
     "1. Gõ abc vào ô Số tiền chi của dòng 1\n"
     "2. Rời con trỏ, đọc lại ô và dòng Tổng cộng\n"
     "3. Bấm Lưu",
     "Số tiền chi dòng 1: abc",
     "- Ô hiển thị 0 hoặc bị chặn ngay khi gõ\n"
     "- Dòng Tổng cộng không hiện giá trị lạ, không lưu giá trị rác"),

    (11, "Nhập số tiền có dấu phân cách nghìn", "P1",
     "Đang mở form Tạo phiếu chi",
     "1. Gõ 1.234.567 vào ô Số tiền chi của dòng 1\n"
     "2. Đọc dòng Tổng cộng\n"
     "3. Lưu rồi mở lại chi tiết",
     "Số tiền chi dòng 1: 1.234.567",
     "- Hệ thống hiểu đúng giá trị, tổng cộng và cột quy đổi tính đúng\n"
     "- Mở lại thấy đúng số đã nhập"),

    (12, "Nhập số tiền có phần thập phân", "P1",
     "Phiếu ngoại tệ, tỷ giá 25.000",
     "1. Gõ 1234,56 vào ô Số tiền chi của dòng 1\n"
     "2. Đọc cột quy đổi VND\n"
     "3. Lưu rồi mở lại chi tiết",
     "Số tiền chi dòng 1: 1234,56",
     "- Giữ đủ 2 chữ số thập phân ở ô nhập, cột quy đổi và dòng Tổng cộng\n"
     "- Mở lại không bị làm tròn mất số lẻ"),

    (13, "Nhập số tiền rất lớn", "P1",
     "Đang mở form Tạo phiếu chi, phiếu tiền Việt Nam",
     "1. Gõ 999.999.999.999 vào ô Số tiền chi của dòng 1\n"
     "2. Lưu, mở danh sách đọc cột Số tiền\n"
     "3. Bấm In, đọc dòng Bằng chữ",
     "Số tiền chi dòng 1: 999.999.999.999",
     "- Cột Số tiền hiển thị đủ chữ số, không tràn cột\n"
     "- Dòng Bằng chữ đọc đúng, không cụt"),

    (14, "Ký tự đặc biệt trong ô Người nhận tiền và Lý do chi", "P1",
     "Đang mở form Tạo phiếu chi",
     "1. Nhập chuỗi có dấu ngoặc nhọn và chữ script vào ô Người nhận tiền\n"
     "2. Lưu, mở danh sách, mở chi tiết, bấm In",
     "Người nhận tiền: chuỗi chứa thẻ script",
     "- Chuỗi hiển thị nguyên văn dạng chữ ở cả ba chỗ\n"
     "- Không có cửa sổ bật lên, không có đoạn mã nào chạy"),

    (15, "Nhập Người nhận tiền rất dài", "P2",
     "Đang mở form Tạo phiếu chi",
     "1. Nhập chuỗi 300 ký tự vào ô Người nhận tiền\n"
     "2. Lưu, mở lại chi tiết và bấm In",
     "Người nhận tiền: chuỗi 300 ký tự",
     "- Hệ thống hoặc chặn kèm thông báo rõ ràng, hoặc lưu đủ và hiển thị xuống dòng\n"
     "- Bản in không bị vỡ khung"),
]

SEC_IX = [
    (1, "Hai kế toán cùng lập phiếu chi cho một phiếu đề nghị", "P0",
     "Phiếu đề nghị DNC-11 đang đợi lập phiếu chi; KT-1 và KT-2 đều có quyền Kế toán thanh toán",
     "1. Mở form Tạo phiếu chi cho DNC-11 trên hai trình duyệt bằng KT-1 và KT-2\n"
     "2. Nhập đủ thông tin ở cả hai\n"
     "3. Bấm Lưu ở trình duyệt 1, sau đó bấm Lưu ở trình duyệt 2\n"
     "4. Lọc danh sách theo mã DNC-11",
     "—",
     "- ⚠️ Hệ thống không chặn trùng nên nhiều khả năng tạo ra HAI phiếu chi cho cùng một đề nghị\n"
     "- Ghi nhận Failed kèm cả hai mã phiếu (mục 9 ghi chú 5)"),

    (2, "Hai thủ quỹ cùng duyệt một phiếu", "P0",
     "Phiếu PC-W đang ở Chờ chi tiền; TQ-1 và TQ-2 đều có quyền duyệt",
     "1. Mở chi tiết PC-W trên hai trình duyệt bằng TQ-1 và TQ-2\n"
     "2. Bấm Duyệt phiếu chi ở trình duyệt 1, rồi ở trình duyệt 2\n"
     "3. Mở sổ kế toán, đếm bút toán của PC-W",
     "—",
     "- Trình duyệt 1 duyệt thành công\n"
     "- Trình duyệt 2 bị từ chối vì phiếu không còn ở Chờ chi tiền\n"
     "- Bút toán KHÔNG bị ghi hai lần"),

    (3, "Kế toán trưởng duyệt trong khi thủ quỹ đang mở phiếu", "P1",
     "Phiếu PC-01 đang ở Chờ KT trưởng duyệt",
     "1. TQ-1 mở chi tiết PC-01, để nguyên màn hình\n"
     "2. KTT-1 bấm Kế toán duyệt phiếu chi ở trình duyệt khác\n"
     "3. TQ-1 tải lại trang",
     "—",
     "- Sau khi tải lại, TQ-1 mới thấy nút Duyệt phiếu chi\n"
     "- Trước khi tải lại, bấm nút cũ không gây ra thao tác sai"),

    (4, "Một người duyệt, một người hủy cùng lúc", "P0",
     "Phiếu PC-X đang ở Chờ chi tiền",
     "1. Mở PC-X trên hai trình duyệt bằng TQ-1 và TQ-2\n"
     "2. TQ-1 bấm Duyệt phiếu chi\n"
     "3. TQ-2 nhập Ghi chú rồi bấm Hủy phiếu chi\n"
     "4. Mở lại chi tiết PC-X, phiếu đề nghị gốc và sổ kế toán",
     "—",
     "- Ghi nhận đúng trạng thái cuối cùng của cả phiếu chi và phiếu đề nghị\n"
     "- ⚠️ Nếu phiếu thành Hủy mà bút toán vẫn còn thì ghi Failed kèm mã phiếu"),

    (5, "Sửa phiếu trong khi thủ quỹ đang duyệt", "P1",
     "Phiếu PC-Y đang ở Chờ chi tiền",
     "1. KT-1 dán đường dẫn sửa PC-Y, để form mở\n"
     "2. TQ-1 duyệt PC-Y ở trình duyệt khác\n"
     "3. KT-1 bấm Lưu trên form đang mở\n"
     "4. Mở lại chi tiết PC-Y",
     "—",
     "- Ghi nhận đúng trạng thái và số tiền cuối cùng\n"
     "- ⚠️ Nếu thao tác Lưu ghi đè được lên phiếu đã duyệt thì ghi Failed"),

    (6, "Người khác đã xóa phiếu trong lúc mình đang mở", "P1",
     "Phiếu PC-N ở trạng thái Đang tạo, đang mở màn Sửa trên trình duyệt của KT-1",
     "1. KT-2 xóa PC-N ở trình duyệt khác\n"
     "2. KT-1 bấm Lưu trên form đang mở",
     "—",
     "- Hệ thống báo dữ liệu đã thay đổi hoặc báo lỗi rõ ràng\n"
     "- Không treo trang, không tạo lại phiếu đã xóa"),

    (7, "Phiếu nháp không lọt sang người duyệt", "P0",
     "KT-1 vừa Lưu nháp phiếu PC-AA",
     "1. Đăng nhập bằng TQ-1, dán đường dẫn màn Phiếu chi cần duyệt, tìm PC-AA\n"
     "2. Đăng nhập bằng KTT-1, làm lại bước trên",
     "—",
     "- Cả hai đều KHÔNG thấy PC-AA\n"
     "- Không ai nhận thông báo nào về phiếu này"),

    (8, "Cô lập dữ liệu giữa hai công ty ở màn cần duyệt", "P0",
     "TQ-1 thuộc công ty 3; công ty 1 có 18 phiếu chi đang Chờ chi tiền",
     "1. Đăng nhập bằng TQ-1, mở màn Phiếu chi cần duyệt\n"
     "2. Soát toàn bộ các trang\n"
     "3. Lấy mã một phiếu Chờ chi tiền của công ty 1, dán đường dẫn chi tiết",
     "—",
     "- Danh sách không có phiếu nào của công ty 1\n"
     "- Mở chi tiết phiếu của công ty 1 bị đưa sang màn báo không tìm thấy dữ liệu"),

    (9, "Số dư nhân viên thay đổi giữa lúc lập phiếu", "P0",
     "Nhân viên NV-C có Hoa hồng tháng số dư 2.000.000; KT-1 đã nạp danh sách và để form mở",
     "1. Trong lúc form đang mở, một phiếu chi khác chi hết 2.000.000 của NV-C\n"
     "2. KT-1 bấm Lưu trên form đang mở\n"
     "3. Mở lại số dư của NV-C",
     "—",
     "- Kỳ vọng: hệ thống chặn vì số dư không còn đủ\n"
     "- Ghi nhận đúng kết quả quan sát được; nếu chi âm số dư thì ghi Failed"),

    (10, "Số tổng tính lại đúng sau mỗi lần lưu", "P1",
     "Phiếu PC-N có 2 dòng, tổng số tiền chi 12.000.000",
     "1. Mở màn Sửa, đổi số tiền chi dòng 1 từ 5.000.000 xuống 1.000.000, bấm Lưu\n"
     "2. Đọc cột Số tiền của PC-N trên danh sách\n"
     "3. Mở lại màn Sửa, đổi ngược lên 5.000.000, lưu lại\n"
     "4. Đọc lại cột Số tiền",
     "—",
     "- Bước 2 hiện 8.000.000, bước 4 hiện lại 12.000.000\n"
     "- Không bị cộng dồn chồng lên nhau qua các lần lưu"),
]

SEC_X = [
    (1, "Luồng đầy đủ chi trả nhà cung cấp", "P0",
     "NV-B lập đề nghị, KT-1 có quyền Kế toán thanh toán, TQ-1 có quyền Thủ quỹ duyệt phiếu chi; công "
     "nợ phải trả nhà cung cấp NCC-01 đang là 20.000.000 trên hợp đồng mua HDM-01",
     "1. NV-B lập phiếu đề nghị chi 20.000.000 cho NCC-01 theo HDM-01 và đưa qua hết luồng duyệt tới "
     "trạng thái đợi lập phiếu chi\n"
     "2. KT-1 tạo phiếu chi từ phiếu đề nghị, nhập Người nhận tiền, bấm Lưu và gửi duyệt\n"
     "3. TQ-1 nhận thông báo, mở phiếu chi, bấm Duyệt phiếu chi\n"
     "4. Mở sổ kế toán và báo cáo công nợ phải trả của NCC-01",
     "—",
     "- Sau bước 2: phiếu chi ở Chờ chi tiền, phiếu đề nghị chuyển sang đợi duyệt phiếu chi\n"
     "- Sau bước 3: phiếu chi ở Đã duyệt, phiếu đề nghị chuyển sang đã duyệt phiếu chi\n"
     "- Sổ kế toán có bút toán ghi Nợ tài khoản phải trả và ghi Có tài khoản tiền, cùng 20.000.000\n"
     "- Công nợ phải trả NCC-01 trên HDM-01 giảm về 0"),

    (2, "Luồng chi một phần", "P0",
     "Nhà cung cấp NCC-02 đang được đề nghị chi 30.000.000",
     "1. KT-1 tạo phiếu chi, sửa Số tiền chi xuống 12.000.000, gửi duyệt\n"
     "2. TQ-1 duyệt phiếu chi\n"
     "3. Đọc cột Số tiền của phiếu trên danh sách\n"
     "4. Mở phiếu đề nghị gốc, đọc số tiền đã duyệt chi\n"
     "5. Mở báo cáo công nợ phải trả NCC-02",
     "Số tiền chi: 12.000.000",
     "- Cột Số tiền ngoài danh sách hiện 12.000.000\n"
     "- Phiếu đề nghị gốc ghi nhận số chi thực tế 12.000.000\n"
     "- Công nợ phải trả NCC-02 giảm đúng 12.000.000, còn 18.000.000"),

    (3, "Luồng đầy đủ chi thu nhập cho nhân viên", "P0",
     "Phòng Kinh doanh 2 có 5 nhân viên còn số dư, tổng 40.000.000; KTT-1 và TQ-1 có quyền duyệt tương "
     "ứng",
     "1. KT-1 tạo phiếu Chi thu nhập cho nhân viên, chọn Phòng ban Kinh doanh 2, giữ nguyên số chi, "
     "nhập Người nhận tiền và Lý do chi, bấm Lưu và gửi duyệt\n"
     "2. KTT-1 mở phiếu, bấm Kế toán duyệt phiếu chi\n"
     "3. TQ-1 mở phiếu, bấm Duyệt phiếu chi\n"
     "4. Chờ vài phút rồi mở sổ kế toán và số dư của 5 nhân viên",
     "—",
     "- Sau bước 1: phiếu ở Chờ KT trưởng duyệt\n"
     "- Sau bước 2: phiếu ở Chờ chi tiền\n"
     "- Sau bước 3: phiếu ở Đã duyệt\n"
     "- Sau khi hệ thống chạy nền xong: sổ kế toán có bút toán tổng 40.000.000, số dư 5 nhân viên về 0"),

    (4, "Luồng chi ngoại tệ", "P0",
     "Phiếu đề nghị chi ngoại tệ, tỷ giá 25.000, đề nghị chi 2.000 ngoại tệ",
     "1. KT-1 tạo phiếu chi, giữ nguyên số chi 2.000, gửi duyệt\n"
     "2. TQ-1 duyệt phiếu chi\n"
     "3. Đọc cột Số tiền trên danh sách\n"
     "4. Mở sổ kế toán, đọc số tiền và tỷ giá của bút toán",
     "—",
     "- Cột Số tiền hiện 50.000.000\n"
     "- Bút toán ghi cả số ngoại tệ 2.000 và số quy đổi 50.000.000, kèm tỷ giá 25.000"),

    (5, "Luồng hủy ở bước kế toán trưởng", "P0",
     "Phiếu chi loại Chi thu nhập cho nhân viên đang ở Chờ KT trưởng duyệt",
     "1. KTT-1 nhập Ghi chú rồi bấm Hủy phiếu chi\n"
     "2. Mở danh sách, đọc trạng thái\n"
     "3. Mở lại chi tiết, đọc ô Ghi chú\n"
     "4. Mở sổ kế toán và số dư nhân viên",
     "Ghi chú: Chưa đủ chứng từ",
     "- Phiếu chuyển sang trạng thái Hủy\n"
     "- ⚠️ Ô Ghi chú TRỐNG khi mở lại (mục 9 ghi chú 4), ghi nhận Failed\n"
     "- Không có bút toán nào, số dư nhân viên KHÔNG thay đổi"),

    (6, "Luồng hủy ở bước thủ quỹ", "P0",
     "Phiếu chi loại Chi trả nhà cung cấp đang ở Chờ chi tiền, gắn phiếu đề nghị DNC-13",
     "1. TQ-1 nhập Ghi chú rồi bấm Hủy phiếu chi\n"
     "2. Mở lại DNC-13, đọc trạng thái và soát nút\n"
     "3. Mở sổ kế toán và báo cáo công nợ",
     "—",
     "- Phiếu chi ở trạng thái Hủy, DNC-13 chuyển sang Hủy\n"
     "- Không có bút toán nào, công nợ KHÔNG thay đổi\n"
     "- ⚠️ DNC-13 không quay lại được trạng thái đợi lập phiếu chi nên không lập lại được, ghi nhận là "
     "hạn chế nghiệp vụ"),

    (7, "Luồng chi trả lại khách hàng", "P1",
     "Phiếu đề nghị chi loại Chi trả lại khách hàng cho KH-01, số tiền 6.000.000",
     "1. KT-1 tạo phiếu chi, gửi duyệt\n"
     "2. TQ-1 duyệt phiếu chi\n"
     "3. Đọc cột Khách hàng trên danh sách\n"
     "4. Mở sổ kế toán và báo cáo công nợ của KH-01",
     "—",
     "- Cột Khách hàng hiện mã và tên KH-01\n"
     "- Bút toán gắn đúng KH-01\n"
     "- Công nợ của KH-01 đổi đúng 6.000.000 theo chiều trả lại"),

    (8, "Đối chiếu tổng số phiếu sau khi chạy hết bộ test", "P1",
     "Đã chạy xong các mục trên, biết số phiếu đã tạo và đã xóa trong quá trình test",
     "1. Mở chế độ Tất cả bằng tài khoản có quyền xem tổng công ty\n"
     "2. Bấm làm mới bộ lọc, đọc số tổng\n"
     "3. Đối chiếu với số ghi nhận đầu buổi cộng số phiếu mới trừ số phiếu đã xóa\n"
     "4. Lặp lại phép đối chiếu với bộ lọc theo khoảng ngày",
     "—",
     "- Bước 3 khớp chính xác\n"
     "- ⚠️ Bước 4 phải cộng bù phần bị ô Đến ngày làm rụng (mục 4)"),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", SEC_III),
    ("IV", "TẠO MỚI / SỬA / XEM CHI TIẾT", SEC_IV),
    ("V", "DUYỆT & HỦY PHIẾU CHI", SEC_V),
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
        feature_name="Phiếu chi tiền (ERP) - Cập nhật ngày 20/08/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )
