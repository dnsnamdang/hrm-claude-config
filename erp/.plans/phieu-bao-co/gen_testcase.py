# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Phieu bao co" (admin/income-expenditure/bill_income_report).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

⚠️ Tai lieu nay viet theo LOGIC ERP dang chay tren nhanh gop_db (repo D:/laragon/www/erp),
KHONG phai ban da port sang HRM.

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :6541-6561
  app/Http/Controllers/IncomeExpenditure/BillIncomeReportController.php
  app/Model/IncomeExpenditure/BillIncomeReport.php (+ BillIncomeReportDetail)
  app/Http/Requests/IncomeExpenditure/BillIncomeReports/BillIncomeReportStoreRequest.php
  app/Http/Requests/IncomeExpenditure/BillIncomeReports/BillIncomeReportUpdateRequest.php (khong duoc dung)
  app/Model/Accounting/Account.php (getAccountsForSelect)
  app/ExcelImports/ImportIncomeReport.php + app/Jobs/ImportIncomeReportJob.php
  app/Jobs/StoreIncomeReportJob.php
  app/Helpers/FormatHelper.php :89 (autoGenerateCode), :987 (getStatus)
  database/seeds/PermissionsTableSeeder.php :286-288, :364
  resources/views/income_expenditure/bill_income_reports/*.blade.php
  resources/views/partials/classes/IncomeExpenditure/BillIncomeReport*.blade.php
  resources/views/partials/classes/base/Datatable.blade.php :142-195
  resources/views/layouts/topmenubar.blade.php :855, :1006

Chay:  python .plans/phieu-bao-co/gen_testcase.py
"""
import os
import sys

try:  # console Windows mac dinh cp1252
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

# .plans/phieu-bao-co -> .plans -> erp -> hrm-claude-config -> hrm/.claude/skills/...
sys.path.insert(0, os.path.join(
    HERE, "..", "..", "..", "hrm", ".claude", "skills", "testcase-documenter", "assets"))

from tc_engine import build  # noqa: E402

OUT = os.path.join(HERE, "testcase-phieu-bao-co.xlsx")

MODULE = "Phiếu báo có"

# ============================================================ 9 MUC MO TA
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Quản lý Phiếu báo có: chứng từ kế toán ghi nhận khoản tiền đã VỀ TÀI KHOẢN NGÂN HÀNG của công "
     "ty, thuộc nhóm Quản lý tiền - Thanh toán tiền mặt.\n"
     "Phiếu báo có lập ĐỘC LẬP, không bắt nguồn từ phiếu đề nghị nào, và người lập tự nhập toàn bộ "
     "dòng chi tiết.\n"
     "Người có quyền Quản lý phiếu báo có làm được: xem danh sách, lọc, tạo phiếu (Lưu nháp hoặc Lưu "
     "và duyệt), sửa, xóa, xem chi tiết và Import Báo có từ tệp Excel.\n"
     "⚠️ Màn hình KHÔNG có người duyệt thứ hai. Bấm \"Lưu và duyệt\" là chính người lập vừa lập vừa "
     "duyệt, phiếu chuyển ngay sang Đã duyệt và ghi thẳng vào sổ kế toán.\n"
     "Từ màn chi tiết của phiếu Đã duyệt, người dùng chọn các dòng còn tiền chưa điều chỉnh công nợ "
     "rồi bấm sang màn Tạo phiếu yêu cầu điều chỉnh công nợ — đó là bước gán tiền về cho từng hợp "
     "đồng, nằm ở màn khác.\n"
     "⚠️ Màn hình KHÔNG có chức năng In, KHÔNG có chức năng Xuất Excel danh sách."),

    ("2. Đối tượng được tính / hiển thị",
     "Phiếu báo có chỉ có 2 trạng thái: Đang tạo · Đã duyệt. Nhãn Đã duyệt tô XANH, nhãn Đang tạo tô "
     "ĐỎ. Không có trạng thái Chờ duyệt, không có trạng thái Hủy, không có trạng thái Không duyệt.\n"
     "Phạm vi phiếu nhìn thấy phụ thuộc chế độ danh sách đang mở:\n"
     "- Chế độ \"Tất cả\" (mục menu Phiếu báo có trỏ vào đây): lấy theo 2 quyền xem ở mục 7, và luôn "
     "ẩn phiếu nháp của người khác.\n"
     "- Chế độ \"Phiếu của tôi\" (vào thẳng đường dẫn không kèm tham số chế độ): chỉ phiếu do chính "
     "mình lập, gồm cả phiếu nháp của mình.\n"
     "- Chế độ \"Đã duyệt\": phiếu mà chính người đăng nhập là người đã duyệt.\n"
     "⚠️ Chỉ chế độ \"Tất cả\" có mục menu; hai chế độ còn lại phải dán đường dẫn — xem mục 9.\n"
     "Bảng danh sách có 13 cột: STT · Mã phiếu · Loại thu · Tổng PS · Tỷ giá · Tổng PS VND · Diễn giải "
     "· Khách hàng · Ngày lập · Ngày hạch toán · Người lập · Trạng thái · Hành động."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu nháp (Đang tạo) của NGƯỜI KHÁC bị ẩn ở chế độ \"Tất cả\" và không mở được chi tiết.\n"
     "- Mục \"Sửa\" và mục \"Xóa\" trong menu hành động chỉ hiện khi phiếu ở trạng thái Đang tạo VÀ do "
     "chính người đăng nhập lập. Phiếu Đã duyệt không có hai mục này, menu hành động rỗng nhưng nút "
     "bánh răng vẫn hiện.\n"
     "- Nút \"Tạo mới\" chỉ hiện với người có quyền Quản lý phiếu báo có.\n"
     "- Nút \"Import Báo có\" luôn hiện với mọi người vào được màn danh sách.\n"
     "- Ô lọc Công ty chỉ hiện với người có quyền xem tổng công ty; ô lọc Phòng ban hiện với cả hai "
     "quyền xem. Người không có quyền xem nào thì không có hai ô này.\n"
     "- Ô \"Loại thu\" trong form chỉ liệt kê 2 lựa chọn: Thu bán hàng · Thu nhà cung cấp. Loại \"Thu "
     "khác\" TỒN TẠI trong dữ liệu và giao diện có nhánh xử lý riêng nhưng KHÔNG chọn được từ ô này.\n"
     "- Bảng Chi tiết chỉ hiện sau khi đã chọn Loại thu; chưa chọn thì chỉ có dòng chữ \"Chưa chọn "
     "loại thu\".\n"
     "- Cột \"Số đơn hàng/Hợp đồng\", \"Phiếu yc xuất hàng\" chỉ hiện với loại Thu bán hàng; cột \"Nhà "
     "cung cấp\", \"Phiếu xuất hàng\", \"Hợp đồng mua\" chỉ hiện với loại Thu nhà cung cấp.\n"
     "- Ô tích \"Số dư nợ đầu kì\" chỉ hiện ở dòng đã gắn HỢP ĐỒNG NGUYÊN TẮC.\n"
     "- Cột tích chọn dòng để tạo yêu cầu điều chỉnh công nợ chỉ hiện khi phiếu là Thu bán hàng VÀ đã "
     "ở trạng thái Đã duyệt; trong cột đó, dòng đã điều chỉnh hết tiền thì không có ô tích.\n"
     "- Cột quy đổi VND của mỗi cặp cột tiền chỉ hiện khi phiếu là NGOẠI TỆ."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Màn có HAI cặp ô ngày, chỉ một cặp có tác dụng:\n"
     "- Cặp \"Hạch toán từ\" / \"Hạch toán đến\" (nằm trong nhóm ô lọc theo cột): CÓ tác dụng, lọc "
     "theo Ngày hạch toán của phiếu, lấy cả hai đầu mút.\n"
     "- ⚠️ Cặp \"Từ ngày\" / \"Đến ngày\" (nằm ở đầu khối tìm kiếm): KHÔNG có tác dụng. Hệ thống không "
     "dùng đến hai giá trị này khi lấy dữ liệu: chọn ngày nào cũng ra nguyên kết quả cũ, kể cả khoảng "
     "ngày không có phiếu nào. Đây là bẫy đối chiếu số liệu nặng nhất của màn, đã dựng ca test riêng ở "
     "mục II.\n"
     "Không có bộ lọc theo Ngày lập, cũng không có bộ lọc theo ngày cập nhật."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Hai cấp: Phiếu báo có → Dòng chi tiết. Không có cấp cha phía trên.\n"
     "- Phiếu giữ: Mã phiếu, Loại thu, Tài khoản nợ, Loại tiền, Tỷ giá, Ngày hạch toán, Diễn giải, "
     "Ngân hàng, Tài khoản ngân hàng, Chi nhánh, Trạng thái, Người lập, Người duyệt, Công ty, Phòng "
     "ban, Tổng PS, Tổng PS VND.\n"
     "- Mỗi dòng chi tiết giữ: Số tài khoản có · Tên tài khoản · Khách hàng (hoặc Nhà cung cấp) · Số "
     "đơn hàng - Hợp đồng · Phiếu yêu cầu xuất hàng (hoặc Phiếu xuất hàng) · NVKD · Số tiền · Số tiền "
     "quy đổi VND · Diễn giải · ô tích Không báo tiền về · ô tích Số dư nợ đầu kì.\n"
     "- Sau khi phiếu được duyệt, mỗi dòng còn mang thêm hai số do màn Điều chỉnh công nợ ghi vào: Số "
     "tiền đã DCCN và Số tiền chưa DCCN (bằng Số tiền trừ Số tiền đã DCCN).\n"
     "- Mã phiếu sinh tự động: mã công ty + \".PBC\" + tháng năm (4 số) + \".\" + 5 chữ số tăng dần, "
     "ví dụ TPE.PBC0826.00017. Không sửa tay được.\n"
     "- Công ty / Phòng ban của phiếu lấy từ hồ sơ nhân sự của NGƯỜI LẬP tại thời điểm tạo.\n"
     "- Tài khoản nợ mặc định là tài khoản tiền gửi ngân hàng đã cấu hình sẵn; Số tài khoản có mặc "
     "định là tài khoản phải thu khách hàng với loại Thu bán hàng, tài khoản phải trả nhà cung cấp với "
     "loại Thu nhà cung cấp.\n"
     "- ⚠️ Mỗi lần lưu, TOÀN BỘ dòng chi tiết cũ bị xóa và ghi lại từ đầu. Số tiền đã DCCN của các "
     "dòng cũ KHÔNG được giữ lại — xem mục 9.\n"
     "- Ba chế độ danh sách dùng CHUNG một nguồn dữ liệu và chung bộ lọc; khác nhau ở phạm vi lọc."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Cột \"Tổng PS\" ngoài danh sách = TỔNG Số tiền nguyên tệ của mọi dòng chi tiết, hiển thị 2 chữ "
     "số thập phân. Cột \"Tổng PS VND\" = TỔNG Số tiền quy đổi VND, hiển thị không có phần thập phân.\n"
     "- Hai con số này được chốt lại tại thời điểm lưu phiếu, không tính lại khi mở danh sách.\n"
     "- Trong form: ô quy đổi VND của mỗi dòng = Số tiền của dòng đó × Tỷ giá, giao diện tự tính lại "
     "ngay khi gõ. Dòng \"Tổng cộng\" cuối bảng cộng dồn cả cột nguyên tệ lẫn cột VND.\n"
     "- Ở màn chi tiết, dòng \"Tổng cộng\" cộng dồn đủ ba cặp cột: Số tiền · Số tiền đã DCCN · Số tiền "
     "chưa DCCN.\n"
     "- Cột \"Khách hàng\" ngoài danh sách chỉ lấy đối tượng của DÒNG ĐẦU TIÊN; phiếu gom nhiều khách "
     "hàng vẫn chỉ hiện một tên.\n"
     "- Khi ghi sổ: mỗi dòng chi tiết sinh MỘT bút toán ghi Có theo Số tài khoản có của dòng; toàn "
     "phiếu sinh THÊM MỘT bút toán ghi Nợ gộp bằng tổng tiền của các dòng, vào Tài khoản nợ của phiếu.\n"
     "- ⚠️ Khi ghi sổ, dòng có Số tiền bằng 0 bị BỎ QUA hoàn toàn. Phiếu mà mọi dòng đều bằng 0 thì "
     "không sinh bút toán nào, kể cả bút toán ghi Nợ.\n"
     "- Ghi sổ có tính chống trùng: ghi sổ lại cùng một phiếu sẽ xóa sạch bút toán cũ của chính phiếu "
     "đó rồi ghi lại, không cộng dồn.\n"
     "- Một phiếu khớp nhiều điều kiện lọc vẫn chỉ hiện một dòng."),

    ("7. Phân quyền cấp",
     "Ba quyền liên quan tới màn hình này:\n"
     "1. \"Quản lý phiếu báo có\" — được vào các đường dẫn Tạo mới, Sửa, Lưu, Cập nhật, Xóa. Người "
     "không có quyền này chỉ xem được.\n"
     "2. \"Xem tất cả phiếu báo có của tổng công ty\" — thấy phiếu của mọi công ty ở chế độ Tất cả; bộ "
     "lọc hiện thêm ô Công ty và ô Phòng ban; mở được chi tiết mọi phiếu đã duyệt.\n"
     "3. \"Xem tất cả phiếu báo có của công ty\" — chỉ phiếu công ty mình ở chế độ Tất cả; bộ lọc hiện "
     "ô Phòng ban.\n"
     "⚠️ Màn Phiếu báo có KHÔNG có quyền xem cấp phòng ban và cấp bộ phận. Ai không có một trong hai "
     "quyền xem trên thì ở chế độ Tất cả chỉ thấy phiếu do chính mình lập.\n"
     "Tài khoản có vai trò Super Admin luôn mở được chi tiết mọi phiếu.\n"
     "⚠️ Các đường dẫn sau KHÔNG gắn quyền ở phía hệ thống: xem danh sách, lấy dữ liệu bảng, xem chi "
     "tiết, Import Báo có, và thao tác tích ô \"Không báo tiền về\". Nhóm ca TC-ROLE cuối dựng riêng "
     "để đo mức độ rủi ro này."),

    ("8. Cách tính các ô thống kê",
     "- Ô \"Hiển thị a đến b trong tổng số N\" dưới bảng: a là dòng đầu trang đang xem, b là dòng "
     "cuối, N là tổng số phiếu khớp bộ lọc trong phạm vi chế độ đang mở.\n"
     "- Ô \"Số dòng mỗi trang\": mặc định 10; đổi số dòng thì bảng quay về trang 1.\n"
     "- Cột STT đánh liên tục theo trang: trang 2 với 10 dòng mỗi trang bắt đầu từ 11.\n"
     "- Cột \"Tổng PS\" phân cách nghìn bằng dấu phẩy và LUÔN có 2 chữ số thập phân, kể cả phiếu tiền "
     "Việt Nam. Cột \"Tổng PS VND\" phân cách nghìn nhưng KHÔNG có phần thập phân.\n"
     "- Cột \"Tỷ giá\" hiển thị làm tròn về số nguyên, phiếu tiền Việt Nam hiện 1.\n"
     "- Cột \"Ngày lập\" và cột \"Ngày hạch toán\" đều hiển thị dạng ngày/tháng/năm, không có giờ.\n"
     "- Chỉ có hai cột cho phép bấm tiêu đề để sắp xếp: Tổng PS và Tổng PS VND. Mọi cột còn lại không "
     "sắp xếp được.\n"
     "- Mặc định khi chưa bấm sắp xếp: phiếu mới nhất nằm trên cùng.\n"
     "- Ở màn Chi tiết, ba cặp ô Tổng cộng tính lại tại chỗ từ các dòng đang hiện, không lấy số đã "
     "chốt trong phiếu."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất của màn này — đọc trước khi chạy test:\n"
     "1. ⚠️ Hai ô lọc \"Từ ngày\" / \"Đến ngày\" KHÔNG có tác dụng (mục 4). Muốn lọc theo thời gian "
     "phải dùng cặp \"Hạch toán từ\" / \"Hạch toán đến\". Ghi nhận Failed.\n"
     "2. ⚠️ Ô lọc \"Loại thu\" cũng KHÔNG có tác dụng: gõ gì vào cũng ra nguyên danh sách cũ. Ghi nhận "
     "Failed.\n"
     "3. ⚠️ Đổi ô \"Loại thu\" trong form là TOÀN BỘ dòng chi tiết đang nhập bị xóa sạch, chỉ còn lại "
     "một dòng trống mới. Không có cảnh báo, không hoàn tác được.\n"
     "4. ⚠️ Sửa một phiếu ĐÃ DUYỆT rồi lưu là Số tiền đã DCCN của mọi dòng BỊ ĐẶT VỀ 0, trong khi "
     "phiếu điều chỉnh công nợ đã lập trước đó vẫn còn. Phiếu quay lại trạng thái \"chưa điều chỉnh "
     "hết công nợ\" và có thể bị điều chỉnh lần hai. Đây là lỗi số liệu nặng nhất của màn.\n"
     "5. ⚠️ Mục Sửa chỉ ẩn theo trạng thái ở phần hiển thị. Người có quyền Quản lý phiếu báo có dán "
     "thẳng đường dẫn sửa của một phiếu Đã duyệt, kể cả phiếu người khác lập, vẫn mở được form và lưu "
     "được.\n"
     "6. ⚠️ Mở phiếu Đã duyệt bằng đường dẫn sửa rồi bấm nút \"Lưu\" (không bấm \"Lưu và duyệt\") thì "
     "phiếu quay về trạng thái Đang tạo NHƯNG bút toán đã ghi trong sổ KHÔNG bị xóa. Sổ kế toán còn "
     "bút toán của một phiếu đang ở trạng thái nháp.\n"
     "7. ⚠️ Xóa phiếu: hệ thống KHÔNG kiểm tra trạng thái và KHÔNG kiểm tra người lập. Người có quyền "
     "Quản lý phiếu báo có dán thẳng đường dẫn xóa của một phiếu Đã duyệt đã ghi sổ là phiếu bị xóa "
     "trong khi TOÀN BỘ bút toán đã ghi vẫn còn nguyên trong sổ, không còn chứng từ gốc để lần ngược. "
     "Đây là lỗ hổng, ghi nhận Failed.\n"
     "8. ⚠️ Hai đường dẫn \"phiếu báo có cần duyệt\" và \"phiếu báo có đã duyệt\" nạp NHẦM dữ liệu: "
     "bảng hiện ra là danh sách PHIẾU ĐỀ NGHỊ THU TIỀN, không phải phiếu báo có. Bấm vào mã phiếu sẽ "
     "sang màn khác hẳn. Ghi nhận Failed.\n"
     "9. ⚠️ Đổi tham số chế độ trên thanh địa chỉ thành một giá trị lạ là hệ thống BỎ HẾT giới hạn "
     "phạm vi: người không có quyền xem nào cũng thấy phiếu của mọi công ty, kể cả phiếu nháp của "
     "người khác. Lỗ hổng phân quyền, ghi nhận Failed.\n"
     "10. ⚠️ Mỗi dòng chi tiết mới tự điền sẵn khách hàng \"KHÁCH KHÔNG RÕ\". Lưu vội là ra phiếu treo "
     "vào khách không rõ, hệ thống KHÔNG cảnh báo và cũng KHÔNG bắt chọn hợp đồng cho dòng đó.\n"
     "11. ⚠️ Ô tích \"Không báo tiền về\" ở màn Chi tiết lưu NGAY khi bấm, không cần bấm nút nào, và "
     "hệ thống không kiểm tra người thao tác là ai. Dòng đã tích sẽ biến mất khỏi màn Tổng hợp tiền về "
     "ngân hàng.\n"
     "12. ⚠️ Ô \"Loại thu\" thiếu lựa chọn \"Thu khác\" (mục 3). Phiếu loại này chỉ tồn tại ở dữ liệu "
     "cũ; mở chi tiết vẫn xem được nhưng mở form sửa thì ô Loại thu hiện trống.\n"
     "13. ⚠️ Ô Tỷ giá bị khóa khi Loại tiền là tiền Việt Nam. Đổi Loại tiền là tỷ giá TỰ NHẢY theo "
     "danh mục tiền tệ, ghi đè số đang gõ dở.\n"
     "14. ⚠️ Đổi ô \"Ngân hàng\" là ô Tài khoản và dòng Chi nhánh bị xóa trắng, phải chọn lại.\n"
     "15. ⚠️ Số tiền quy đổi VND do giao diện tính rồi gửi lên, hệ thống lưu nguyên không tính lại. "
     "Sửa Tỷ giá sau khi đã gõ Số tiền thì cột VND của các dòng cũ chỉ đổi khi gõ lại Số tiền.\n"
     "16. ⚠️ Số tiền bằng 0 vẫn lưu được nhưng khi ghi sổ dòng đó bị bỏ qua (mục 6). Phiếu toàn dòng 0 "
     "hiện là Đã duyệt mà không có bút toán nào.\n"
     "17. ⚠️ Import Báo có: mỗi DÒNG trong tệp Excel sinh ra MỘT phiếu báo có riêng, tự động ở trạng "
     "thái Đã duyệt, gắn khách hàng \"KHÁCH KHÔNG RÕ\", và ghi sổ ngay. Import 200 dòng là ra 200 "
     "phiếu.\n"
     "18. ⚠️ Import không kiểm tra trùng. Nạp lại đúng tệp cũ là sinh thêm một bộ phiếu mới y hệt.\n"
     "19. ⚠️ Khối \"Chi tiết: đã import / đã bỏ qua / không hợp lệ\" trong cửa sổ Import KHÔNG BAO GIỜ "
     "hiện số. Việc nạp chạy ngầm; kết quả về bằng thông báo trên chuông và bằng tệp nhật ký.\n"
     "20. ⚠️ Cột ngày trong tệp Import bắt buộc dạng năm-tháng-ngày. Sai dạng thì dòng bị bỏ qua. Dòng "
     "trống cả Số tiền lẫn Ngày thì bị bỏ qua LẶNG LẼ, không tính vào bất kỳ con số nào.\n"
     "21. Màn Phiếu báo có KHÔNG có In và KHÔNG có Xuất Excel. Chức năng xuất Excel nằm ở màn \"Tổng "
     "hợp tiền về ngân hàng\", là màn khác, có mục menu riêng.\n"
     "22. Bộ lọc được hệ thống ghi nhớ RIÊNG cho từng chế độ danh sách; rời màn rồi quay lại vẫn còn "
     "điều kiện lọc cũ — test xong nhớ bấm nút làm mới bộ lọc trước khi sang ca test khác."),
]

# ============================================================ TC PHAN QUYEN
ROLE_TCS = [
    ("00", "Tài khoản không có quyền xem nào chỉ thấy phiếu do chính mình lập", "P0",
     "Tài khoản NV-A không có quyền \"Xem tất cả phiếu báo có của tổng công ty\" và không có quyền "
     "\"Xem tất cả phiếu báo có của công ty\"; NV-A đã lập 9 phiếu báo có; công ty của NV-A có hơn 120 "
     "phiếu báo có của nhiều người",
     "1. Đăng nhập bằng NV-A\n"
     "2. Mở menu Quản lý tiền, nhóm Thanh toán tiền mặt, bấm mục Phiếu báo có\n"
     "3. Đọc số tổng dưới bảng\n"
     "4. Lật hết các trang, soát cột Người lập",
     "Tài khoản: NV-A (không quyền xem theo cấp)",
     "- Vào được màn hình, không bị chặn\n"
     "- Tổng hiện đúng 9\n"
     "- Mọi dòng đều có Người lập là NV-A\n"
     "- Khối lọc KHÔNG có ô Công ty, KHÔNG có ô Phòng ban"),

    ("01", "Quyền xem của tổng công ty thấy phiếu báo có của mọi công ty", "P0",
     "Tài khoản B chỉ có quyền \"Xem tất cả phiếu báo có của tổng công ty\"; hệ thống có phiếu báo có "
     "của ít nhất 3 công ty",
     "1. Đăng nhập bằng B, mở mục Phiếu báo có trên menu\n"
     "2. Bấm nút Bộ lọc để bung khối tìm kiếm\n"
     "3. Ghi lại các ô lọc theo đơn vị đang hiện\n"
     "4. Chọn lần lượt từng Công ty rồi bấm nút tìm kiếm",
     "Quyền: Xem tất cả phiếu báo có của tổng công ty",
     "- Khối lọc hiện CẢ ô Công ty và ô Phòng ban\n"
     "- Bỏ chọn công ty thì thấy phiếu của cả 3 công ty\n"
     "- Chọn công ty nào thì chỉ ra phiếu do người của công ty đó lập\n"
     "- Không có phiếu nháp của người khác lọt vào"),

    ("02", "Quyền xem của công ty chỉ thấy phiếu báo có công ty mình", "P0",
     "Tài khoản C chỉ có quyền \"Xem tất cả phiếu báo có của công ty\", thuộc công ty 3; công ty 3 có "
     "35 phiếu báo có (trong đó 2 phiếu nháp của người khác), công ty 1 có hơn 200 phiếu",
     "1. Đăng nhập bằng C, mở mục Phiếu báo có\n"
     "2. Bấm nút Bộ lọc, ghi lại các ô lọc theo đơn vị\n"
     "3. Đọc số tổng, soát danh sách qua tất cả các trang",
     "Quyền: Xem tất cả phiếu báo có của công ty",
     "- Khối lọc KHÔNG có ô Công ty, chỉ có ô Phòng ban\n"
     "- Tổng hiện đúng 33 (35 trừ 2 phiếu nháp của người khác)\n"
     "- Không có phiếu nào của công ty 1"),

    ("03", "Màn Phiếu báo có không có quyền xem cấp phòng ban và cấp bộ phận", "P1",
     "Tài khoản D là trưởng phòng, có các quyền xem cấp phòng ban của những màn khác nhưng KHÔNG có "
     "hai quyền xem của màn Phiếu báo có",
     "1. Đăng nhập bằng D, mở mục Phiếu báo có\n"
     "2. Đọc số tổng và soát cột Người lập\n"
     "3. Bấm nút Bộ lọc, soát các ô lọc theo đơn vị",
     "Quyền: chỉ có quyền xem cấp phòng ban của màn khác",
     "- CHỈ thấy phiếu do chính D lập, không thấy phiếu của nhân viên trong phòng\n"
     "- Khối lọc không có ô Công ty, không có ô Phòng ban, không có ô Bộ phận\n"
     "- ⚠️ Đúng hiện trạng — màn này không có quyền cấp phòng ban / bộ phận (mục 7)"),

    ("04", "Có cả hai quyền xem thì lấy phạm vi rộng nhất", "P1",
     "Tài khoản F có ĐỒNG THỜI quyền \"Xem tất cả phiếu báo có của tổng công ty\" và \"Xem tất cả "
     "phiếu báo có của công ty\"",
     "1. Đăng nhập bằng F, mở mục Phiếu báo có\n"
     "2. Đọc số tổng, so với số của tài khoản B ở TC-ROLE-01",
     "Quyền: tổng công ty + công ty",
     "- Tổng bằng đúng số của tài khoản chỉ có quyền tổng công ty\n"
     "- Không bị thu hẹp về phạm vi một công ty\n"
     "- Bộ lọc vẫn hiện đủ ô Công ty và ô Phòng ban"),

    ("05", "Người có quyền Quản lý phiếu báo có vào được màn Tạo mới", "P0",
     "Tài khoản KT-1 có quyền \"Quản lý phiếu báo có\"",
     "1. Đăng nhập bằng KT-1, mở mục Phiếu báo có\n"
     "2. Soát khu vực phía trên bảng\n"
     "3. Bấm nút Tạo mới",
     "Quyền: Quản lý phiếu báo có",
     "- Nút Tạo mới có hiển thị\n"
     "- Vào được form Tạo phiếu báo có, tiêu đề trang là Tạo phiếu báo có\n"
     "- Form đã có sẵn một dòng chi tiết trống"),

    ("06", "Không có quyền Quản lý phiếu báo có thì không tạo mới được", "P0",
     "Tài khoản NV-A ở TC-ROLE-00, không có quyền \"Quản lý phiếu báo có\"",
     "1. Đăng nhập bằng NV-A, mở mục Phiếu báo có\n"
     "2. Soát khu vực phía trên bảng\n"
     "3. Dán thẳng đường dẫn tạo mới vào thanh địa chỉ",
     "Đường dẫn Tạo phiếu báo có",
     "- Nút Tạo mới KHÔNG hiển thị (giao diện ẩn đúng theo quyền)\n"
     "- Dán đường dẫn: hệ thống từ chối, báo không có quyền, không mở được form\n"
     "- Nút Import Báo có VẪN hiển thị"),

    ("07", "Không có quyền Quản lý phiếu báo có thì bị chặn ở Sửa và Xóa", "P0",
     "Tài khoản NV-A không có quyền \"Quản lý phiếu báo có\"; tồn tại phiếu báo có trạng thái Đang tạo "
     "do chính NV-A lập từ trước",
     "1. Đăng nhập bằng NV-A, dán đường dẫn chế độ Phiếu của tôi\n"
     "2. Bấm biểu tượng bánh răng ở dòng phiếu Đang tạo\n"
     "3. Bấm mục Sửa\n"
     "4. Quay lại, bấm mục Xóa và xác nhận",
     "—",
     "- ⚠️ Hai mục Sửa và Xóa VẪN hiện trong menu hành động (chỉ xét trạng thái và người lập, không "
     "xét quyền)\n"
     "- Bấm Sửa: hệ thống từ chối, báo không có quyền\n"
     "- Bấm Xóa: hệ thống từ chối, phiếu vẫn còn nguyên trong danh sách"),

    ("08", "Chế độ Phiếu của tôi không đòi quyền nào", "P1",
     "Tài khoản NV-A không có quyền xem theo cấp nào và không có quyền Quản lý phiếu báo có; NV-A đã "
     "lập 9 phiếu trong đó có 3 phiếu nháp",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dán đường dẫn màn Phiếu báo có KHÔNG kèm tham số chế độ\n"
     "3. Đọc số tổng, soát cột Trạng thái",
     "Đường dẫn danh sách không kèm tham số",
     "- Vào được, không bị chặn\n"
     "- Đúng 9 dòng, cả 3 phiếu nháp của NV-A đều hiện\n"
     "- Không có phiếu của người khác"),

    ("09", "Không mở được chi tiết phiếu nháp của người khác", "P0",
     "Tài khoản B có quyền xem tổng công ty; KT-1 vừa Lưu nháp một phiếu báo có",
     "1. KT-1 lập phiếu, bấm Lưu (không bấm Lưu và duyệt), ghi lại mã phiếu và đường dẫn chi tiết\n"
     "2. Đăng nhập bằng B, dán thẳng đường dẫn chi tiết phiếu đó",
     "—",
     "- Hệ thống trả trang báo không tìm thấy dữ liệu\n"
     "- Không hiện bất kỳ thông tin nào của phiếu\n"
     "- ⚠️ Đúng thiết kế — phiếu nháp là riêng của người lập, quyền xem tổng công ty cũng không mở "
     "được"),

    ("10", "Không có quyền xem theo cấp thì không mở được chi tiết phiếu người khác", "P0",
     "Tài khoản NV-A không có quyền xem theo cấp; tồn tại phiếu báo có PBC-01 Đã duyệt do KT-1 cùng "
     "công ty lập",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dán thẳng đường dẫn chi tiết của PBC-01",
     "—",
     "- Hệ thống trả trang báo không tìm thấy dữ liệu\n"
     "- Không đọc được số tiền, không đọc được khách hàng của phiếu"),

    ("11", "Tham số chế độ lạ làm mất toàn bộ giới hạn phạm vi", "P0",
     "Tài khoản NV-A không có quyền xem theo cấp nào; hệ thống có phiếu báo có của nhiều công ty, có "
     "cả phiếu nháp của người khác",
     "1. Đăng nhập bằng NV-A, mở mục Phiếu báo có, ghi lại số tổng\n"
     "2. Sửa tham số chế độ trên thanh địa chỉ thành một chữ bất kỳ, ví dụ đổi \"all\" thành \"x\"\n"
     "3. Tải lại trang, đọc số tổng\n"
     "4. Soát cột Người lập và cột Trạng thái",
     "Tham số chế độ: một giá trị không hợp lệ",
     "- ⚠️ Số tổng nhảy lên bằng TOÀN BỘ số phiếu báo có của cả hệ thống\n"
     "- Thấy phiếu của công ty khác và thấy cả phiếu nháp của người khác\n"
     "- Đây là lỗ hổng phân quyền, ghi nhận Failed (mục 9 ghi chú 9)"),

    ("12", "Ô Không báo tiền về không kiểm tra quyền người thao tác", "P0",
     "Tài khoản NV-A không có quyền Quản lý phiếu báo có và không có quyền xem theo cấp; tồn tại phiếu "
     "PBC-02 Đã duyệt do NV-A lập, có 1 dòng chi tiết chưa tích Không báo tiền về",
     "1. Đăng nhập bằng NV-A, mở chi tiết PBC-02\n"
     "2. Tích ô Không báo tiền về ở dòng chi tiết\n"
     "3. Tải lại trang, đọc lại ô tích\n"
     "4. Mở màn Tổng hợp tiền về ngân hàng, tìm dòng đó",
     "—",
     "- Tích xong hiện thông báo cập nhật thành công NGAY, không cần bấm nút Lưu\n"
     "- Tải lại trang: ô vẫn còn tích\n"
     "- Dòng đó biến mất khỏi màn Tổng hợp tiền về ngân hàng\n"
     "- ⚠️ Thao tác này không đòi quyền Quản lý phiếu báo có (mục 9 ghi chú 11)"),
]

# ============================================================ I. HIEN THI TRANG
SEC_I = [
    (1, "Vào màn Phiếu báo có từ menu", "P0",
     "Tài khoản KT-1 có quyền Quản lý phiếu báo có và quyền xem của công ty",
     "1. Đăng nhập bằng KT-1\n"
     "2. Mở menu Quản lý tiền\n"
     "3. Trong nhóm Thanh toán tiền mặt, bấm mục Phiếu báo có",
     "—",
     "- Mở đúng màn danh sách, tiêu đề trang là Danh sách phiếu báo có\n"
     "- Bảng có đủ 13 cột theo thứ tự ở mục 2\n"
     "- Phía trên bảng có nút Bộ lọc, nút Tạo mới và nút Import Báo có"),

    (2, "Chế độ Tất cả ẩn phiếu nháp của người khác", "P0",
     "Tài khoản B có quyền xem tổng công ty; KT-1 vừa Lưu nháp một phiếu báo có mã kết thúc .00031",
     "1. Đăng nhập bằng B, mở mục Phiếu báo có trên menu\n"
     "2. Bấm Bộ lọc, gõ .00031 vào ô Mã phiếu, bấm tìm kiếm\n"
     "3. Xóa ô mã, chọn Trạng thái là Đang tạo rồi tìm lại",
     "Mã phiếu: .00031",
     "- Bước 2 không ra dòng nào\n"
     "- Bước 3 chỉ ra phiếu nháp do chính B lập, không có phiếu của KT-1"),

    (3, "Chế độ Phiếu của tôi chỉ hiện phiếu mình lập", "P0",
     "Tài khoản KT-1 có quyền xem của công ty; KT-1 đã lập 9 phiếu trong đó có 2 phiếu nháp; công ty "
     "có hơn 120 phiếu",
     "1. Đăng nhập bằng KT-1\n"
     "2. Dán đường dẫn màn Phiếu báo có KHÔNG kèm tham số chế độ\n"
     "3. Đọc số tổng, soát cột Người lập và cột Trạng thái",
     "—",
     "- Tổng hiện đúng 9\n"
     "- Mọi dòng đều có Người lập là KT-1\n"
     "- Cả 2 phiếu nháp của KT-1 đều hiện"),

    (4, "Chế độ Đã duyệt chỉ hiện phiếu mình đã duyệt", "P1",
     "Tài khoản KT-1 đã bấm Lưu và duyệt cho 6 phiếu; trong công ty còn 15 phiếu Đã duyệt do người "
     "khác duyệt",
     "1. Đăng nhập bằng KT-1\n"
     "2. Dán đường dẫn danh sách kèm tham số chế độ là đã duyệt\n"
     "3. Đọc số tổng và soát cột Người lập",
     "Chế độ: đã duyệt",
     "- Đúng 6 dòng\n"
     "- Mọi dòng đều ở trạng thái Đã duyệt và do KT-1 lập\n"
     "- Không có phiếu do người khác duyệt"),

    (5, "Đường dẫn phiếu báo có đã duyệt nạp nhầm dữ liệu", "P0",
     "Tài khoản KT-1 có quyền Quản lý phiếu báo có; hệ thống có cả phiếu báo có lẫn phiếu đề nghị thu "
     "tiền",
     "1. Đăng nhập bằng KT-1\n"
     "2. Dán thẳng đường dẫn màn phiếu báo có đã duyệt (đường dẫn có đuôi approved)\n"
     "3. Đọc tiêu đề trang, đọc mã phiếu ở cột Mã phiếu\n"
     "4. Bấm vào một mã phiếu bất kỳ",
     "Đường dẫn màn đã duyệt",
     "- Tiêu đề trang ghi Danh sách phiếu báo có đã duyệt\n"
     "- ⚠️ Nhưng mã phiếu trong bảng là mã PHIẾU ĐỀ NGHỊ THU TIỀN, không phải mã phiếu báo có\n"
     "- Bấm vào mã phiếu thì sang màn chi tiết Đề nghị thu tiền\n"
     "- Ghi nhận Failed (mục 9 ghi chú 8)"),

    (6, "Đường dẫn phiếu báo có cần duyệt nạp nhầm dữ liệu", "P1",
     "Tài khoản KT-1 có quyền Quản lý phiếu báo có",
     "1. Đăng nhập bằng KT-1\n"
     "2. Dán thẳng đường dẫn màn phiếu báo có cần duyệt (đường dẫn có đuôi for-accounting)\n"
     "3. Đọc tiêu đề trang và mã phiếu trong bảng",
     "Đường dẫn màn cần duyệt",
     "- Tiêu đề trang ghi Danh sách phiếu báo có cần duyệt\n"
     "- ⚠️ Dữ liệu trong bảng là phiếu đề nghị thu tiền đang chờ kế toán duyệt\n"
     "- Ghi nhận Failed"),

    (7, "Hai chế độ ngoài Tất cả không có mục menu", "P2",
     "Tài khoản KT-1 có đủ quyền của màn",
     "1. Đăng nhập bằng KT-1\n"
     "2. Mở menu Quản lý tiền, soát toàn bộ mục trong nhóm Thanh toán tiền mặt\n"
     "3. Soát cả các menu còn lại tìm mục dẫn tới Phiếu của tôi hoặc Đã duyệt",
     "—",
     "- Chỉ có đúng một mục Phiếu báo có, trỏ vào chế độ Tất cả\n"
     "- Không có mục nào dẫn tới chế độ Phiếu của tôi\n"
     "- Không có mục nào dẫn tới chế độ Đã duyệt\n"
     "- ⚠️ Ghi nhận là hạn chế điều hướng (mục 9)"),

    (8, "Màn hình không có nút In và không có nút Xuất Excel", "P1",
     "Tài khoản KT-1 có đủ quyền; danh sách có ít nhất 1 phiếu Đã duyệt",
     "1. Mở mục Phiếu báo có\n"
     "2. Soát toàn bộ khu vực phía trên bảng\n"
     "3. Bấm biểu tượng bánh răng ở một dòng phiếu nháp của mình, soát menu hành động\n"
     "4. Mở chi tiết một phiếu Đã duyệt, soát khu vực nút phía dưới",
     "—",
     "- Phía trên bảng chỉ có Bộ lọc, Tạo mới, Import Báo có — không có Xuất Excel\n"
     "- Menu hành động chỉ có Sửa và Xóa — không có In, không có Xuất Excel\n"
     "- Màn chi tiết chỉ có nút Quay lại và có thể có nút Tạo phiếu yêu cầu điều chỉnh công nợ"),

    (9, "Menu hành động rỗng ở phiếu Đã duyệt", "P1",
     "Tài khoản KT-1 có quyền Quản lý phiếu báo có; tồn tại phiếu PBC-03 Đã duyệt do chính KT-1 lập",
     "1. Mở mục Phiếu báo có\n"
     "2. Tìm dòng PBC-03\n"
     "3. Bấm biểu tượng bánh răng ở cột Hành động",
     "—",
     "- Nút bánh răng VẪN hiện\n"
     "- Bấm vào ra menu RỖNG, không có mục nào\n"
     "- Không có mục Sửa, không có mục Xóa"),

    (10, "Mở chi tiết bằng cách bấm vào Mã phiếu", "P0",
     "Tài khoản KT-1; tồn tại phiếu PBC-03 Đã duyệt loại Thu bán hàng, có 3 dòng chi tiết",
     "1. Mở mục Phiếu báo có\n"
     "2. Bấm vào Mã phiếu của PBC-03\n"
     "3. Soát khối Thông tin chung và bảng Chi tiết",
     "—",
     "- Mở màn Chi tiết phiếu báo có\n"
     "- Mọi ô ở khối Thông tin chung đều bị khóa, không sửa được\n"
     "- Bảng Chi tiết hiện đủ 3 dòng, có thêm hai cặp cột Số tiền đã DCCN và Số tiền chưa DCCN\n"
     "- Dòng Tổng cộng cuối bảng cộng đủ ba cặp cột"),
]

# ============================================================ II. BO LOC
SEC_II = [
    (1, "Lọc theo Mã phiếu khớp một phần", "P0",
     "Tài khoản B có quyền xem tổng công ty; tồn tại phiếu mã TPE.PBC0826.00017",
     "1. Mở mục Phiếu báo có, bấm nút Bộ lọc\n"
     "2. Gõ 00017 vào ô Mã phiếu, bấm tìm kiếm\n"
     "3. Xóa đi, gõ PBC0826 rồi tìm lại",
     "Mã phiếu: 00017 · PBC0826",
     "- Lần 1 ra đúng phiếu TPE.PBC0826.00017\n"
     "- Lần 2 ra toàn bộ phiếu lập trong tháng 08 năm 2026 của công ty TPE\n"
     "- Gõ chữ thường vẫn ra kết quả như gõ chữ hoa"),

    (2, "Ô lọc Loại thu không có tác dụng", "P0",
     "Tài khoản B có quyền xem tổng công ty; hệ thống có cả phiếu Thu bán hàng lẫn phiếu Thu nhà cung "
     "cấp",
     "1. Mở mục Phiếu báo có, bấm Bộ lọc, ghi lại số tổng đang có\n"
     "2. Gõ \"Thu bán hàng\" vào ô Loại thu, bấm tìm kiếm, đọc số tổng\n"
     "3. Xóa đi, gõ một chuỗi vô nghĩa như \"zzzz\", tìm lại, đọc số tổng",
     "Loại thu: Thu bán hàng · zzzz",
     "- ⚠️ Cả hai lần số tổng KHÔNG đổi so với bước 1\n"
     "- Danh sách vẫn còn nguyên phiếu Thu nhà cung cấp\n"
     "- Ghi nhận Failed (mục 9 ghi chú 2)"),

    (3, "Cặp ô Từ ngày / Đến ngày không có tác dụng", "P0",
     "Tài khoản B có quyền xem tổng công ty; hệ thống chắc chắn không có phiếu nào lập trong năm 2015",
     "1. Mở mục Phiếu báo có, bấm Bộ lọc, ghi lại số tổng đang có\n"
     "2. Điền Từ ngày 01/01/2015, Đến ngày 31/12/2015, bấm tìm kiếm\n"
     "3. Đọc số tổng và soát cột Ngày lập",
     "Từ ngày: 01/01/2015 · Đến ngày: 31/12/2015",
     "- ⚠️ Số tổng KHÔNG đổi, danh sách ra nguyên như cũ\n"
     "- Cột Ngày lập vẫn hiện các ngày ngoài khoảng đã chọn\n"
     "- Ghi nhận Failed (mục 4 và mục 9 ghi chú 1)"),

    (4, "Lọc theo Hạch toán từ - Hạch toán đến chạy đúng", "P0",
     "Tài khoản B có quyền xem tổng công ty; tồn tại phiếu hạch toán ngày 01/08/2026, phiếu ngày "
     "15/08/2026 và phiếu ngày 31/08/2026",
     "1. Mở mục Phiếu báo có, bấm Bộ lọc\n"
     "2. Điền Hạch toán từ 01/08/2026, Hạch toán đến 15/08/2026, tìm kiếm\n"
     "3. Soát cột Ngày hạch toán\n"
     "4. Đổi Hạch toán từ thành 16/08/2026, xóa ô Hạch toán đến, tìm lại",
     "Hạch toán từ: 01/08/2026 · Hạch toán đến: 15/08/2026",
     "- Bước 2 ra cả phiếu ngày 01/08 và phiếu ngày 15/08 (lấy cả hai đầu mút)\n"
     "- Không có phiếu ngày 31/08\n"
     "- Bước 4 ra phiếu ngày 31/08, không có hai phiếu kia"),

    (5, "Lọc theo Trạng thái", "P0",
     "Tài khoản KT-1; ở chế độ Phiếu của tôi KT-1 có 2 phiếu Đang tạo và 7 phiếu Đã duyệt",
     "1. Dán đường dẫn chế độ Phiếu của tôi, bấm Bộ lọc\n"
     "2. Chọn Trạng thái là Đang tạo, tìm kiếm\n"
     "3. Đổi sang Đã duyệt, tìm lại\n"
     "4. Bung lại ô Trạng thái, đếm số lựa chọn có trong đó",
     "Trạng thái: Đang tạo · Đã duyệt",
     "- Bước 2 ra đúng 2 dòng, nhãn Đang tạo tô đỏ\n"
     "- Bước 3 ra đúng 7 dòng, nhãn Đã duyệt tô xanh\n"
     "- Ô Trạng thái CHỈ có 2 lựa chọn, không có Chờ duyệt, không có Hủy"),

    (6, "Lọc theo Người lập", "P1",
     "Tài khoản B có quyền xem tổng công ty; KT-1 đã lập 9 phiếu, KT-2 đã lập 4 phiếu",
     "1. Mở mục Phiếu báo có, bấm Bộ lọc\n"
     "2. Gõ tên KT-1 vào ô Người lập, chọn từ danh sách gợi ý, tìm kiếm\n"
     "3. Đọc số tổng, soát cột Người lập",
     "Người lập: KT-1",
     "- Ra đúng 9 dòng, trừ đi phiếu nháp nếu KT-1 có phiếu nháp\n"
     "- Mọi dòng đều là KT-1\n"
     "- Ô gợi ý tìm được cả nhân viên đã nghỉ việc"),

    (7, "Lọc theo Ngân hàng", "P1",
     "Tài khoản B có quyền xem tổng công ty; có phiếu gắn ngân hàng NH-A và phiếu gắn ngân hàng NH-B",
     "1. Mở mục Phiếu báo có, bấm Bộ lọc\n"
     "2. Chọn Ngân hàng là NH-A, tìm kiếm\n"
     "3. Mở chi tiết một vài dòng để đối chiếu ô Ngân hàng",
     "Ngân hàng: NH-A",
     "- Chỉ ra phiếu gắn ngân hàng NH-A\n"
     "- Không có phiếu gắn NH-B\n"
     "- Ô Ngân hàng là ô chọn từ danh mục, không phải ô gõ tay"),

    (8, "Lọc theo Tài khoản ngân hàng", "P1",
     "Tài khoản B; ngân hàng NH-A có hai tài khoản của công ty, ký hiệu TK-1 và TK-2, mỗi tài khoản có "
     "ít nhất 2 phiếu",
     "1. Mở mục Phiếu báo có, bấm Bộ lọc\n"
     "2. Gõ đúng số của TK-1 vào ô Tài khoản ngân hàng, tìm kiếm\n"
     "3. Gõ một vài chữ số đầu của TK-1, tìm lại",
     "Tài khoản ngân hàng: số của TK-1",
     "- Bước 2 chỉ ra phiếu gắn TK-1\n"
     "- ⚠️ Bước 3: ô này so KHỚP TUYỆT ĐỐI, gõ thiếu chữ số thì KHÔNG ra dòng nào\n"
     "- Ghi nhận đúng hiện trạng, khác với ô Mã phiếu vốn khớp một phần"),

    (9, "Lọc theo Khách hàng", "P0",
     "Tài khoản B; khách hàng KH-01 mã 29TPHPTH-101 xuất hiện ở dòng chi tiết của 3 phiếu, trong đó "
     "có 1 phiếu mà KH-01 nằm ở DÒNG THỨ HAI",
     "1. Mở mục Phiếu báo có, bấm Bộ lọc\n"
     "2. Gõ 29TPHPTH-101 vào ô Khách hàng, tìm kiếm\n"
     "3. Đọc số tổng và soát cột Khách hàng\n"
     "4. Mở chi tiết phiếu có KH-01 ở dòng thứ hai",
     "Khách hàng: 29TPHPTH-101",
     "- Ra đủ 3 phiếu, kể cả phiếu mà KH-01 nằm ở dòng thứ hai\n"
     "- ⚠️ Với phiếu đó, cột Khách hàng ngoài danh sách hiện tên khách của DÒNG ĐẦU TIÊN, không phải "
     "KH-01 (mục 6)\n"
     "- Mở chi tiết mới thấy KH-01 ở dòng thứ hai"),

    (10, "Lọc theo Ghi chú khớp một phần", "P2",
     "Tài khoản B; tồn tại phiếu có Diễn giải chứa cụm \"chuyen khoan thang 8\"",
     "1. Mở mục Phiếu báo có, bấm Bộ lọc\n"
     "2. Gõ \"thang 8\" vào ô Ghi chú, tìm kiếm\n"
     "3. Soát cột Diễn giải",
     "Ghi chú: thang 8",
     "- Ra mọi phiếu có Diễn giải chứa cụm đó\n"
     "- Khớp một phần, không cần gõ đủ cả câu"),

    (11, "Lọc theo Không báo tiền về", "P1",
     "Tài khoản B; có 3 phiếu mà ÍT NHẤT MỘT dòng chi tiết đã tích Không báo tiền về, và nhiều phiếu "
     "không dòng nào tích",
     "1. Mở mục Phiếu báo có, bấm Bộ lọc\n"
     "2. Chọn Không báo tiền về là Có, tìm kiếm\n"
     "3. Đổi sang Không, tìm lại\n"
     "4. Mở chi tiết một phiếu ở nhóm Có, đếm số dòng đã tích",
     "Không báo tiền về: Có · Không",
     "- Nhóm Có ra đúng 3 phiếu\n"
     "- Nhóm Không ra các phiếu còn lại, hai nhóm cộng lại bằng tổng khi bỏ lọc\n"
     "- ⚠️ Phiếu chỉ cần MỘT dòng tích là lọt vào nhóm Có, dù các dòng khác không tích"),

    (12, "Lọc theo Công ty và Phòng ban", "P0",
     "Tài khoản B có quyền xem tổng công ty; công ty 1 và công ty 3 đều có phiếu báo có; trong công ty "
     "1 có phiếu của phòng P1 và phòng P2",
     "1. Mở mục Phiếu báo có, bấm Bộ lọc\n"
     "2. Chọn Công ty là công ty 1, tìm kiếm, đọc số tổng\n"
     "3. Chọn thêm Phòng ban là P1, tìm lại\n"
     "4. Mở chi tiết vài dòng, đối chiếu ô Phòng ban",
     "Công ty: công ty 1 · Phòng ban: P1",
     "- Bước 2 chỉ ra phiếu do người của công ty 1 lập\n"
     "- Bước 3 thu hẹp còn phiếu của người phòng P1\n"
     "- Đơn vị lọc theo là đơn vị của NGƯỜI LẬP tại thời điểm tạo phiếu"),

    (13, "Kết hợp nhiều điều kiện lọc", "P1",
     "Tài khoản B có quyền xem tổng công ty",
     "1. Mở mục Phiếu báo có, bấm Bộ lọc\n"
     "2. Chọn cùng lúc: Trạng thái Đã duyệt, Ngân hàng NH-A, Hạch toán từ 01/08/2026\n"
     "3. Bấm tìm kiếm, soát từng dòng",
     "Trạng thái + Ngân hàng + Hạch toán từ",
     "- Chỉ ra phiếu thỏa ĐỒNG THỜI cả ba điều kiện\n"
     "- Một phiếu thỏa nhiều điều kiện vẫn chỉ hiện một dòng\n"
     "- Bỏ bớt một điều kiện thì số dòng tăng lên hoặc giữ nguyên, không bao giờ giảm"),

    (14, "Bộ lọc được nhớ riêng theo từng chế độ danh sách", "P2",
     "Tài khoản KT-1 có quyền xem của công ty",
     "1. Mở chế độ Tất cả, đặt Trạng thái là Đã duyệt, tìm kiếm\n"
     "2. Chuyển sang chế độ Phiếu của tôi bằng đường dẫn, soát ô Trạng thái\n"
     "3. Đặt Trạng thái ở chế độ này là Đang tạo, tìm kiếm\n"
     "4. Quay lại chế độ Tất cả, soát lại ô Trạng thái",
     "—",
     "- Chế độ Phiếu của tôi mở ra với bộ lọc trống, không kế thừa của chế độ Tất cả\n"
     "- Quay lại chế độ Tất cả: ô Trạng thái vẫn còn là Đã duyệt như bước 1\n"
     "- Bấm nút làm mới bộ lọc thì mọi ô trở về trống"),
]

# ============================================================ III. DANH SACH
SEC_III = [
    (1, "Thứ tự mặc định là phiếu mới nhất trên cùng", "P0",
     "Tài khoản KT-1 vừa lập xong một phiếu mới trong ngày",
     "1. Mở mục Phiếu báo có\n"
     "2. Không bấm sắp xếp gì, đọc dòng đầu tiên\n"
     "3. Đọc Mã phiếu và Ngày lập của 5 dòng đầu",
     "—",
     "- Phiếu vừa lập nằm ở dòng đầu tiên\n"
     "- 5 dòng đầu có số thứ tự trong mã phiếu giảm dần"),

    (2, "Chỉ hai cột Tổng PS và Tổng PS VND sắp xếp được", "P1",
     "Tài khoản B có quyền xem tổng công ty, danh sách có hơn 3 trang",
     "1. Mở mục Phiếu báo có\n"
     "2. Bấm lần lượt vào tiêu đề từng cột: Mã phiếu, Loại thu, Khách hàng, Ngày lập, Người lập, "
     "Trạng thái\n"
     "3. Bấm tiêu đề cột Tổng PS, rồi bấm lần nữa\n"
     "4. Bấm tiêu đề cột Tổng PS VND",
     "—",
     "- Các cột ở bước 2 KHÔNG có biểu tượng sắp xếp và bấm không đổi thứ tự\n"
     "- Cột Tổng PS: bấm lần 1 sắp tăng dần, lần 2 giảm dần\n"
     "- Cột Tổng PS VND sắp xếp được tương tự"),

    (3, "Sắp xếp theo Tổng PS trên phiếu ngoại tệ", "P1",
     "Danh sách có cả phiếu tiền Việt Nam giá trị lớn và phiếu ngoại tệ giá trị nhỏ về số nguyên tệ",
     "1. Mở mục Phiếu báo có\n"
     "2. Bấm tiêu đề cột Tổng PS, sắp giảm dần\n"
     "3. Đọc 5 dòng đầu, đối chiếu cột Tổng PS và cột Tổng PS VND",
     "—",
     "- ⚠️ Cột Tổng PS sắp theo số NGUYÊN TỆ, không quy đổi. Phiếu tiền Việt Nam luôn đứng trên phiếu "
     "ngoại tệ dù giá trị thật nhỏ hơn\n"
     "- Muốn xếp theo giá trị thật phải bấm cột Tổng PS VND"),

    (4, "Phân trang và số dòng mỗi trang", "P1",
     "Chế độ Tất cả có hơn 35 phiếu",
     "1. Mở mục Phiếu báo có, đọc dòng \"Hiển thị a đến b trong tổng số N\"\n"
     "2. Sang trang 2, đọc cột STT của dòng đầu\n"
     "3. Đổi Số dòng mỗi trang sang 25\n"
     "4. Đọc lại vị trí trang hiện tại",
     "Số dòng mỗi trang: 25",
     "- Mặc định 10 dòng mỗi trang\n"
     "- Trang 2 bắt đầu từ STT 11\n"
     "- Đổi sang 25 thì bảng quay về trang 1 và hiện 25 dòng"),

    (5, "Định dạng cột Tổng PS và Tổng PS VND", "P0",
     "Tồn tại phiếu tiền Việt Nam tổng 15.000.000 và phiếu ngoại tệ tổng 1.234,56 với tỷ giá 24.500",
     "1. Mở mục Phiếu báo có, tìm hai phiếu trên\n"
     "2. Đọc cột Tổng PS, cột Tỷ giá và cột Tổng PS VND của từng phiếu",
     "—",
     "- Phiếu tiền Việt Nam: Tổng PS hiện 15,000,000.00 (LUÔN có 2 số lẻ), Tỷ giá hiện 1, Tổng PS VND "
     "hiện 15,000,000 (không số lẻ)\n"
     "- Phiếu ngoại tệ: Tổng PS hiện 1,234.56, Tỷ giá hiện 24,500, Tổng PS VND hiện số đã quy đổi làm "
     "tròn về số nguyên"),

    (6, "Cột Khách hàng chỉ lấy dòng đầu tiên", "P0",
     "Tồn tại phiếu PBC-04 có 3 dòng chi tiết gắn 3 khách hàng khác nhau",
     "1. Mở mục Phiếu báo có, tìm dòng PBC-04\n"
     "2. Đọc cột Khách hàng\n"
     "3. Mở chi tiết PBC-04, đọc cột Khách hàng của cả 3 dòng",
     "—",
     "- Ngoài danh sách chỉ hiện MỘT tên khách, là khách của dòng thứ nhất\n"
     "- Trong chi tiết hiện đủ 3 khách khác nhau\n"
     "- ⚠️ Không được kết luận phiếu chỉ có một khách khi đọc ngoài danh sách"),

    (7, "Cột Khách hàng của phiếu loại Thu nhà cung cấp", "P1",
     "Tồn tại phiếu PBC-05 loại Thu nhà cung cấp, các dòng chi tiết gắn nhà cung cấp, không gắn khách "
     "hàng",
     "1. Mở mục Phiếu báo có, tìm dòng PBC-05\n"
     "2. Đọc cột Khách hàng\n"
     "3. Mở chi tiết, đối chiếu cột Nhà cung cấp",
     "—",
     "- ⚠️ Cột Khách hàng ngoài danh sách để TRỐNG\n"
     "- Danh sách KHÔNG có cột nào hiện tên nhà cung cấp\n"
     "- Phải mở chi tiết mới biết phiếu gắn nhà cung cấp nào"),

    (8, "Mã phiếu bấm được để mở chi tiết", "P1",
     "Danh sách có ít nhất một phiếu Đã duyệt",
     "1. Mở mục Phiếu báo có\n"
     "2. Rê chuột lên Mã phiếu ở một dòng bất kỳ\n"
     "3. Bấm vào Mã phiếu",
     "—",
     "- Mã phiếu hiện dạng liên kết bấm được, có chú thích Xem\n"
     "- Bấm vào mở đúng màn Chi tiết của phiếu đó"),

    (9, "Đối chiếu số tổng khi lật hết trang", "P1",
     "Chế độ Tất cả có hơn 3 trang",
     "1. Mở mục Phiếu báo có, đọc số N trong dòng \"trong tổng số N\"\n"
     "2. Lật hết mọi trang, đếm tay số dòng thực tế\n"
     "3. So hai con số",
     "—",
     "- Hai con số khớp chính xác\n"
     "- Không có dòng nào bị lặp giữa hai trang"),
]

# ============================================================ IV. TAO / SUA / XEM
SEC_IV = [
    (1, "Giá trị mặc định của form Tạo mới", "P0",
     "Tài khoản KT-1 có quyền Quản lý phiếu báo có; hôm nay là 25/08/2026",
     "1. Mở mục Phiếu báo có, bấm Tạo mới\n"
     "2. Đọc từng ô ở khối Thông tin chung\n"
     "3. Đọc bảng Chi tiết",
     "—",
     "- Ô Loại thu đã chọn sẵn Thu bán hàng\n"
     "- Ô Tài khoản nợ đã chọn sẵn tài khoản tiền gửi ngân hàng\n"
     "- Ô Loại tiền là tiền Việt Nam, ô Tỷ giá là 1 và BỊ KHÓA\n"
     "- Ô Ngày hạch toán điền sẵn 25/08/2026\n"
     "- Bảng Chi tiết đã có SẴN MỘT DÒNG, tài khoản có điền sẵn tài khoản phải thu khách hàng, khách "
     "hàng điền sẵn KHÁCH KHÔNG RÕ\n"
     "- Không có ô Mã phiếu (mã sinh khi lưu)"),

    (2, "Ô Loại thu chỉ có hai lựa chọn", "P0",
     "Đang mở form Tạo phiếu báo có",
     "1. Bung ô Loại thu\n"
     "2. Đếm và ghi lại các lựa chọn",
     "—",
     "- Chỉ có Thu bán hàng và Thu nhà cung cấp\n"
     "- ⚠️ KHÔNG có lựa chọn Thu khác dù dữ liệu cũ vẫn tồn tại loại này (mục 9 ghi chú 12)"),

    (3, "Đổi Loại thu xóa sạch dòng chi tiết đang nhập", "P0",
     "Đang mở form Tạo phiếu báo có",
     "1. Chọn Loại thu là Thu bán hàng\n"
     "2. Bấm dấu cộng thêm 2 dòng nữa, nhập đủ khách hàng, hợp đồng, số tiền, diễn giải cho cả 3 dòng\n"
     "3. Đổi Loại thu sang Thu nhà cung cấp\n"
     "4. Đọc bảng Chi tiết",
     "—",
     "- ⚠️ Cả 3 dòng biến mất, chỉ còn lại MỘT dòng trống mới\n"
     "- Không có hộp cảnh báo nào trước khi xóa\n"
     "- Đổi ngược về Thu bán hàng cũng không lấy lại được dữ liệu cũ\n"
     "- Ghi nhận là bẫy mất dữ liệu (mục 9 ghi chú 3)"),

    (4, "Bộ cột của bảng Chi tiết đổi theo Loại thu", "P0",
     "Đang mở form Tạo phiếu báo có",
     "1. Chọn Loại thu là Thu bán hàng, ghi lại tiêu đề các cột\n"
     "2. Đổi sang Thu nhà cung cấp, ghi lại tiêu đề các cột\n"
     "3. So hai bộ cột",
     "—",
     "- Thu bán hàng: có Khách hàng, Tên khách hàng, Số đơn hàng/Hợp đồng, Phiếu yc xuất hàng, NVKD\n"
     "- Thu nhà cung cấp: có Nhà cung cấp, Tên nhà cung cấp, Phiếu xuất hàng, Hợp đồng mua, NVKD\n"
     "- Cả hai loại đều có: Số tài khoản có, Tên tài khoản, Số tiền, Diễn giải, Không báo tiền về"),

    (5, "Chưa chọn Loại thu thì không có bảng Chi tiết", "P1",
     "Đang mở form Tạo phiếu báo có",
     "1. Bung ô Loại thu, chọn dòng trống \"Chọn loại thu\"\n"
     "2. Đọc khối Chi tiết phía dưới",
     "—",
     "- Khối Chi tiết chỉ hiện dòng chữ \"Chưa chọn loại thu\"\n"
     "- Không có bảng, không có nút thêm dòng"),

    (6, "Đổi Loại tiền làm Tỷ giá tự nhảy", "P0",
     "Đang mở form Tạo phiếu báo có; danh mục tiền tệ có đô la Mỹ với tỷ giá 24.500",
     "1. Chọn Loại tiền là tiền Việt Nam, soát ô Tỷ giá\n"
     "2. Đổi Loại tiền sang đô la Mỹ, đọc ô Tỷ giá\n"
     "3. Gõ đè tỷ giá thành 26.000\n"
     "4. Đổi Loại tiền về tiền Việt Nam rồi đổi lại sang đô la Mỹ",
     "Loại tiền: đô la Mỹ · Tỷ giá gõ tay: 26.000",
     "- Bước 1: Tỷ giá là 1 và ô bị khóa\n"
     "- Bước 2: ô mở khóa, Tỷ giá tự điền 24.500 lấy từ danh mục\n"
     "- Bước 3: gõ đè được thành 26.000\n"
     "- ⚠️ Bước 4: Tỷ giá bị ghi đè về 24.500, mất số vừa gõ (mục 9 ghi chú 13)"),

    (7, "Cột quy đổi VND chỉ hiện với phiếu ngoại tệ", "P0",
     "Đang mở form Tạo phiếu báo có, Loại thu Thu bán hàng",
     "1. Để Loại tiền là tiền Việt Nam, soát tiêu đề nhóm cột Số tiền\n"
     "2. Đổi Loại tiền sang đô la Mỹ tỷ giá 24.500\n"
     "3. Gõ Số tiền dòng 1 là 100\n"
     "4. Đọc cột quy đổi VND",
     "Số tiền: 100 · Tỷ giá: 24.500",
     "- Tiền Việt Nam: nhóm Số tiền chỉ có MỘT cột\n"
     "- Ngoại tệ: nhóm Số tiền tách thành hai cột, cột trái ghi tên loại tiền, cột phải ghi VND\n"
     "- Gõ 100 thì cột VND tự hiện 2,450,000\n"
     "- Cột VND chỉ để đọc, không gõ được"),

    (8, "Sửa Tỷ giá sau khi đã gõ Số tiền", "P0",
     "Đang mở form, Loại tiền đô la Mỹ tỷ giá 24.500, đã gõ Số tiền dòng 1 là 100 và cột VND hiện "
     "2.450.000",
     "1. Sửa ô Tỷ giá thành 26.000\n"
     "2. Không động vào ô Số tiền, đọc lại cột VND của dòng 1\n"
     "3. Bấm vào ô Số tiền, gõ lại đúng số 100\n"
     "4. Đọc lại cột VND",
     "Tỷ giá mới: 26.000",
     "- ⚠️ Bước 2: cột VND VẪN là 2.450.000, không tự tính lại theo tỷ giá mới\n"
     "- Bước 4: sau khi gõ lại Số tiền, cột VND mới nhảy thành 2.600.000\n"
     "- Ghi nhận là bẫy số liệu (mục 9 ghi chú 15)"),

    (9, "Chọn Ngân hàng rồi chọn Tài khoản", "P0",
     "Đang mở form Tạo phiếu báo có; công ty có 2 tài khoản ở ngân hàng NH-A và 1 tài khoản ở NH-B",
     "1. Chưa chọn Ngân hàng, bung ô Tài khoản\n"
     "2. Chọn Ngân hàng là NH-A, bung lại ô Tài khoản\n"
     "3. Chọn một tài khoản, đọc dòng Chi nhánh\n"
     "4. Đổi Ngân hàng sang NH-B, đọc lại ô Tài khoản và dòng Chi nhánh",
     "Ngân hàng: NH-A rồi NH-B",
     "- Bước 1: ô Tài khoản RỖNG\n"
     "- Bước 2: chỉ hiện đúng 2 tài khoản của NH-A, mỗi dòng ghi số tài khoản, loại tiền và tên tài "
     "khoản\n"
     "- Bước 3: dòng Chi nhánh tự điền theo tài khoản đã chọn\n"
     "- ⚠️ Bước 4: ô Tài khoản bị xóa trắng và dòng Chi nhánh về dấu gạch, phải chọn lại (mục 9 ghi "
     "chú 14)"),

    (10, "Thêm dòng và xóa dòng chi tiết", "P0",
     "Đang mở form Tạo phiếu báo có, Loại thu Thu bán hàng, đang có 1 dòng",
     "1. Bấm dấu cộng ở góc phải tiêu đề bảng 3 lần\n"
     "2. Đếm số dòng, đọc STT\n"
     "3. Nhập số tiền khác nhau cho từng dòng, đọc dòng Tổng cộng\n"
     "4. Bấm biểu tượng thùng rác ở dòng thứ 2, đọc lại STT và Tổng cộng",
     "—",
     "- Sau bước 1 có 4 dòng, STT đánh từ 1 đến 4\n"
     "- Dòng Tổng cộng bằng đúng tổng các dòng\n"
     "- Xóa dòng 2: còn 3 dòng, STT đánh lại liên tục 1-2-3, Tổng cộng trừ đúng phần đã xóa\n"
     "- Xóa không có hộp xác nhận"),

    (11, "Chọn Khách hàng cho dòng chi tiết", "P0",
     "Đang mở form, Loại thu Thu bán hàng, dòng 1 đang là KHÁCH KHÔNG RÕ",
     "1. Bấm kính lúp ở ô Khách hàng dòng 1\n"
     "2. Gõ mã khách vào ô tìm trong cửa sổ, chọn khách KH-01\n"
     "3. Đọc ô Khách hàng và cột Tên khách hàng\n"
     "4. Bấm kính lúp lại, chọn khách KH-02",
     "Khách hàng: KH-01 rồi KH-02",
     "- Ô Khách hàng điền mã, cột bên cạnh điền tên, ô mã KHÔNG gõ tay được\n"
     "- Hiện thông báo thêm khách hàng thành công\n"
     "- ⚠️ Đổi sang KH-02 thì ô Số đơn hàng/Hợp đồng của dòng đó bị XÓA TRẮNG, phải chọn lại hợp "
     "đồng"),

    (12, "Chọn Hợp đồng cho dòng chi tiết", "P0",
     "Đang mở form, Loại thu Thu bán hàng, dòng 1 đã chọn khách KH-01 có ít nhất 2 hợp đồng",
     "1. Bấm kính lúp ở ô Số đơn hàng/Hợp đồng dòng 1\n"
     "2. Soát danh sách trong cửa sổ\n"
     "3. Chọn hợp đồng HD-01\n"
     "4. Bấm kính lúp ở dòng 2, chọn lại đúng HD-01",
     "Hợp đồng: HD-01",
     "- Cửa sổ chỉ liệt kê hợp đồng của KH-01\n"
     "- Chọn xong ô Số đơn hàng/Hợp đồng điền mã hợp đồng, cột NVKD tự điền người phụ trách\n"
     "- ⚠️ Bước 4: hệ thống cảnh báo Hợp đồng đã tồn tại và KHÔNG cho chọn trùng trên hai dòng"),

    (13, "Chưa chọn Khách hàng thì không mở được cửa sổ Hợp đồng", "P1",
     "Đang mở form, Loại thu Thu bán hàng; xóa trắng ô Khách hàng của dòng 1 bằng cách thêm dòng mới "
     "rồi bỏ khách",
     "1. Ở một dòng chưa có khách hàng, bấm kính lúp ô Số đơn hàng/Hợp đồng",
     "—",
     "- Hệ thống cảnh báo Chưa chọn khách hàng\n"
     "- Cửa sổ chọn hợp đồng KHÔNG mở ra"),

    (14, "Dòng gắn hợp đồng nguyên tắc có thêm ô Số dư nợ đầu kì và ô Phiếu yc xuất hàng", "P0",
     "Đang mở form, Loại thu Thu bán hàng; khách KH-01 có hợp đồng nguyên tắc HDNT-01 với số dư nợ đầu "
     "kì 50.000.000 và có ít nhất 2 phiếu yêu cầu xuất hàng",
     "1. Chọn khách KH-01 ở dòng 1\n"
     "2. Chọn hợp đồng HDNT-01\n"
     "3. Soát ngay dưới ô hợp đồng và soát cột Phiếu yc xuất hàng\n"
     "4. Bấm kính lúp ở cột Phiếu yc xuất hàng, chọn một phiếu\n"
     "5. Tích ô Số dư nợ đầu kì, soát lại cột Phiếu yc xuất hàng",
     "Hợp đồng: HDNT-01",
     "- Dưới ô hợp đồng hiện ô tích \"Số dư nợ đầu kì: 50,000,000\"\n"
     "- Cột Phiếu yc xuất hàng hiện ô chọn có kính lúp\n"
     "- Chọn được phiếu yêu cầu xuất hàng, mã phiếu điền vào ô\n"
     "- ⚠️ Tích Số dư nợ đầu kì thì ô Phiếu yc xuất hàng BIẾN MẤT khỏi dòng đó"),

    (15, "Chọn Phiếu xuất hàng ở phiếu loại Thu nhà cung cấp", "P1",
     "Đang mở form, Loại thu Thu nhà cung cấp; nhà cung cấp NCC-01 có ít nhất 2 phiếu xuất hàng",
     "1. Ở dòng 1 bấm kính lúp ô Nhà cung cấp, chọn NCC-01\n"
     "2. Bấm kính lúp ô Phiếu xuất hàng, soát danh sách, chọn một phiếu\n"
     "3. Đọc cột Hợp đồng mua và cột NVKD\n"
     "4. Ở dòng 2 thử chọn lại đúng phiếu xuất đó",
     "Nhà cung cấp: NCC-01",
     "- Cửa sổ chỉ liệt kê phiếu xuất hàng của NCC-01\n"
     "- Chọn xong: cột Hợp đồng mua và cột NVKD tự điền\n"
     "- ⚠️ Bước 4: hệ thống cảnh báo Phiếu đã tồn tại và không cho chọn trùng\n"
     "- Chưa chọn nhà cung cấp mà bấm kính lúp Phiếu xuất hàng thì bị cảnh báo Chưa chọn nhà cung cấp"),

    (16, "Sửa phiếu nháp của chính mình", "P0",
     "Tài khoản KT-1 có quyền Quản lý phiếu báo có; KT-1 có phiếu PBC-06 trạng thái Đang tạo, 2 dòng "
     "chi tiết, tổng 20.000.000",
     "1. Mở mục Phiếu báo có ở chế độ Phiếu của tôi\n"
     "2. Bấm bánh răng ở dòng PBC-06, bấm Sửa\n"
     "3. Soát ô Mã phiếu, ô Người đề nghị, ô Phòng ban\n"
     "4. Sửa số tiền dòng 1 và bấm Lưu\n"
     "5. Mở lại chi tiết, đối chiếu",
     "—",
     "- Form mở ra với đủ dữ liệu cũ, tiêu đề trang ghi Sửa phiếu báo có kèm mã phiếu\n"
     "- Ô Mã phiếu hiện và BỊ KHÓA\n"
     "- Ô Người đề nghị hiện tên người LẬP phiếu, ô Phòng ban hiện phòng của người lập, cả hai bị khóa\n"
     "- Lưu xong quay về danh sách, cột Tổng PS đổi theo số vừa sửa\n"
     "- Phiếu vẫn ở trạng thái Đang tạo"),
]

# ============================================================ V. LUU VA DUYET
SEC_V = [
    (1, "Lưu nháp phiếu báo có", "P0",
     "Tài khoản KT-1 có quyền Quản lý phiếu báo có; đã nhập đủ một phiếu Thu bán hàng 1 dòng, khách "
     "KH-01, hợp đồng HD-01, số tiền 10.000.000, diễn giải hợp lệ",
     "1. Bấm nút Lưu\n"
     "2. Đọc thông báo và trang được chuyển tới\n"
     "3. Tìm phiếu vừa lập trong danh sách, đọc Mã phiếu và Trạng thái\n"
     "4. Mở sổ kế toán, tìm bút toán của phiếu này",
     "Số tiền: 10.000.000",
     "- Hiện thông báo Thêm phiếu báo có thành công\n"
     "- Chuyển về danh sách ở chế độ Tất cả\n"
     "- Mã phiếu có dạng mã công ty chấm PBC tháng năm chấm 5 chữ số, ví dụ TPE.PBC0826.00017\n"
     "- Trạng thái là Đang tạo\n"
     "- ⚠️ KHÔNG có bút toán nào trong sổ kế toán"),

    (2, "Lưu và duyệt phiếu báo có", "P0",
     "Như ca trên nhưng chưa lưu; tài khoản nợ là tài khoản tiền gửi ngân hàng, tài khoản có là tài "
     "khoản phải thu khách hàng",
     "1. Bấm nút Lưu và duyệt\n"
     "2. Tìm phiếu trong danh sách, đọc Trạng thái\n"
     "3. Mở sổ kế toán, tìm bút toán của phiếu\n"
     "4. Mở báo cáo công nợ của KH-01",
     "Số tiền: 10.000.000",
     "- Trạng thái chuyển thẳng sang Đã duyệt, không qua Chờ duyệt\n"
     "- Sổ kế toán có ĐÚNG 2 bút toán: một ghi Có tài khoản phải thu 10.000.000 gắn KH-01 và HD-01, "
     "một ghi Nợ tài khoản tiền gửi ngân hàng 10.000.000\n"
     "- Cả hai bút toán mang Ngày hạch toán đã nhập trên phiếu\n"
     "- Công nợ phải thu của KH-01 giảm 10.000.000"),

    (3, "Người duyệt chính là người lập", "P0",
     "Tài khoản KT-1 vừa bấm Lưu và duyệt cho phiếu PBC-07",
     "1. Đăng nhập bằng KT-1, dán đường dẫn danh sách kèm tham số chế độ đã duyệt\n"
     "2. Tìm PBC-07\n"
     "3. Đăng nhập bằng KT-2, dán cùng đường dẫn, tìm PBC-07",
     "—",
     "- KT-1 thấy PBC-07 trong danh sách đã duyệt\n"
     "- KT-2 KHÔNG thấy PBC-07\n"
     "- ⚠️ Đúng thiết kế — màn này không có người duyệt thứ hai, người lập tự duyệt (mục 1)"),

    (4, "Thông báo gửi cho cả công ty khi phiếu được duyệt", "P1",
     "Tài khoản KT-1 và tài khoản NV-B cùng thuộc công ty 1; NV-B đang đăng nhập ở trình duyệt khác",
     "1. KT-1 bấm Lưu và duyệt một phiếu mới\n"
     "2. Bên NV-B, mở biểu tượng chuông thông báo\n"
     "3. Bấm vào thông báo mới nhất\n"
     "4. Kiểm tra bên tài khoản của công ty 3",
     "—",
     "- NV-B nhận thông báo nội dung \"Một phiếu báo có đã được tạo từ\" kèm tên KT-1\n"
     "- Bấm vào mở đúng màn chi tiết phiếu đó (nếu NV-B đủ quyền xem)\n"
     "- Người của công ty 3 KHÔNG nhận thông báo\n"
     "- Bấm Lưu nháp thì KHÔNG ai nhận thông báo"),

    (5, "Ghi sổ bỏ qua dòng có Số tiền bằng 0", "P0",
     "Đang mở form Tạo mới, Thu bán hàng, 3 dòng: dòng 1 là 5.000.000, dòng 2 là 0, dòng 3 là "
     "3.000.000; đủ khách hàng, hợp đồng, diễn giải cho cả 3 dòng",
     "1. Bấm Lưu và duyệt\n"
     "2. Mở danh sách, đọc cột Tổng PS của phiếu\n"
     "3. Mở sổ kế toán, đếm số bút toán ghi Có\n"
     "4. Đọc số tiền của bút toán ghi Nợ",
     "Ba dòng: 5.000.000 · 0 · 3.000.000",
     "- Lưu thành công, không có cảnh báo về dòng 0\n"
     "- Cột Tổng PS hiện 8.000.000\n"
     "- ⚠️ Sổ kế toán chỉ có 2 bút toán ghi Có (dòng 0 bị bỏ qua)\n"
     "- Bút toán ghi Nợ là 8.000.000\n"
     "- Mở chi tiết phiếu vẫn thấy đủ 3 dòng, dòng 2 hiện 0"),

    (6, "Phiếu toàn dòng bằng 0 được duyệt mà không có bút toán", "P1",
     "Đang mở form Tạo mới, Thu bán hàng, 2 dòng, cả hai đều để Số tiền là 0, diễn giải đã nhập",
     "1. Bấm Lưu và duyệt\n"
     "2. Mở danh sách, đọc Trạng thái và cột Tổng PS\n"
     "3. Mở sổ kế toán, tìm bút toán của phiếu",
     "Cả hai dòng: 0",
     "- Lưu thành công, trạng thái Đã duyệt\n"
     "- Cột Tổng PS hiện 0.00\n"
     "- ⚠️ KHÔNG có bút toán nào, kể cả bút toán ghi Nợ tài khoản ngân hàng\n"
     "- Ghi nhận là hiện trạng cần cảnh báo (mục 9 ghi chú 16)"),

    (7, "Nhiều dòng cùng một tài khoản có chỉ tạo một mối nối", "P2",
     "Đang mở form, Thu bán hàng, 3 dòng đều dùng cùng một Số tài khoản có, số tiền lần lượt "
     "1.000.000, 2.000.000, 3.000.000",
     "1. Bấm Lưu và duyệt\n"
     "2. Mở sổ kế toán, đọc bút toán ghi Nợ\n"
     "3. Đọc các tài khoản đối ứng của bút toán ghi Nợ",
     "—",
     "- Có 3 bút toán ghi Có riêng cho 3 dòng\n"
     "- Chỉ có 1 bút toán ghi Nợ, số tiền 6.000.000\n"
     "- Bút toán ghi Nợ chỉ nối tới MỘT tài khoản đối ứng dù có 3 dòng"),

    (8, "Ghi sổ lại không cộng dồn", "P0",
     "Tài khoản KT-1 có quyền Quản lý phiếu báo có; phiếu PBC-08 Đã duyệt số tiền 10.000.000 đã có 2 "
     "bút toán trong sổ",
     "1. Dán thẳng đường dẫn sửa của PBC-08\n"
     "2. Sửa số tiền dòng 1 thành 12.000.000\n"
     "3. Bấm Lưu và duyệt\n"
     "4. Mở sổ kế toán, đếm bút toán của phiếu và đọc số tiền",
     "Số tiền mới: 12.000.000",
     "- Vẫn đúng 2 bút toán, KHÔNG thành 4\n"
     "- Bút toán ghi Có là 12.000.000, bút toán ghi Nợ là 12.000.000\n"
     "- Bút toán cũ 10.000.000 đã bị xóa hẳn, không còn trong sổ"),

    (9, "Sửa phiếu đã duyệt rồi bấm Lưu làm phiếu về nháp mà bút toán còn nguyên", "P0",
     "Tài khoản KT-1 có quyền Quản lý phiếu báo có; phiếu PBC-09 Đã duyệt 10.000.000 đã có bút toán "
     "trong sổ",
     "1. Dán thẳng đường dẫn sửa của PBC-09\n"
     "2. Không sửa gì, bấm nút Lưu (KHÔNG bấm Lưu và duyệt)\n"
     "3. Mở danh sách, đọc Trạng thái của PBC-09\n"
     "4. Mở sổ kế toán, tìm bút toán của PBC-09",
     "—",
     "- Trạng thái đổi về Đang tạo\n"
     "- ⚠️ Bút toán 10.000.000 VẪN còn nguyên trong sổ\n"
     "- Sổ kế toán đang chứa bút toán của một phiếu ở trạng thái nháp\n"
     "- Ghi nhận Failed (mục 9 ghi chú 6)"),

    (10, "Sửa phiếu đã duyệt làm mất Số tiền đã điều chỉnh công nợ", "P0",
     "Phiếu PBC-10 Đã duyệt, 1 dòng 10.000.000, đã lập phiếu điều chỉnh công nợ gán trọn 10.000.000 "
     "nên dòng hiện Số tiền đã DCCN là 10.000.000 và Số tiền chưa DCCN là 0",
     "1. Mở chi tiết PBC-10, ghi lại ba cặp số ở dòng Tổng cộng\n"
     "2. Dán đường dẫn sửa của PBC-10, không sửa gì, bấm Lưu và duyệt\n"
     "3. Mở lại chi tiết PBC-10, đọc lại ba cặp số\n"
     "4. Mở màn Tổng hợp tiền về ngân hàng, tìm dòng của PBC-10\n"
     "5. Mở lại phiếu điều chỉnh công nợ đã lập trước đó",
     "—",
     "- ⚠️ Sau khi lưu: Số tiền đã DCCN về 0, Số tiền chưa DCCN nhảy lên 10.000.000\n"
     "- Màn Tổng hợp tiền về ngân hàng chuyển dòng này về trạng thái Chưa điều chỉnh hết công nợ và "
     "cho tích chọn lại\n"
     "- Phiếu điều chỉnh công nợ cũ vẫn còn nguyên, tiền có thể bị điều chỉnh lần hai\n"
     "- Đây là lỗi số liệu nặng nhất của màn, ghi nhận Failed (mục 9 ghi chú 4)"),

    (11, "Nút Tạo phiếu yêu cầu điều chỉnh công nợ ở màn chi tiết", "P0",
     "Phiếu PBC-11 Đã duyệt, loại Thu bán hàng, 2 dòng, cả hai đều chưa điều chỉnh công nợ",
     "1. Mở chi tiết PBC-11\n"
     "2. Soát khu vực nút phía dưới trước khi tích gì\n"
     "3. Tích ô chọn ở dòng 1, soát lại khu vực nút\n"
     "4. Tích ô chọn ở tiêu đề cột để chọn hết\n"
     "5. Bấm nút Tạo phiếu yêu cầu điều chỉnh công nợ",
     "—",
     "- Bước 2: chỉ có nút Quay lại\n"
     "- Bước 3: nút Tạo phiếu yêu cầu điều chỉnh công nợ MỚI hiện ra\n"
     "- Bước 4: cả hai dòng đều được tích\n"
     "- Bước 5: sang màn Tạo phiếu yêu cầu điều chỉnh công nợ, hai dòng đã được mang sang sẵn"),

    (12, "Cột tích chọn không hiện với phiếu nháp và phiếu Thu nhà cung cấp", "P1",
     "Có phiếu PBC-12 trạng thái Đang tạo loại Thu bán hàng, và phiếu PBC-13 Đã duyệt loại Thu nhà "
     "cung cấp còn tiền chưa điều chỉnh",
     "1. Mở chi tiết PBC-12, soát cột cuối bảng và khu vực nút\n"
     "2. Mở chi tiết PBC-13, soát cột cuối bảng và khu vực nút",
     "—",
     "- PBC-12: KHÔNG có cột tích chọn, không có nút Tạo phiếu yêu cầu điều chỉnh công nợ\n"
     "- PBC-13: cũng KHÔNG có cột tích chọn và không có nút đó\n"
     "- ⚠️ Tiền của phiếu Thu nhà cung cấp không gán về công nợ được từ màn này"),
]

# ============================================================ VI. XOA
SEC_VI = [
    (1, "Xóa phiếu nháp của chính mình", "P0",
     "Tài khoản KT-1 có quyền Quản lý phiếu báo có; KT-1 có phiếu PBC-14 trạng thái Đang tạo",
     "1. Mở chế độ Phiếu của tôi, ghi lại số tổng\n"
     "2. Bấm bánh răng ở dòng PBC-14, bấm Xóa\n"
     "3. Đọc hộp xác nhận, bấm Xác nhận\n"
     "4. Đọc thông báo và số tổng mới\n"
     "5. Dán đường dẫn chi tiết của PBC-14",
     "—",
     "- Có hộp xác nhận trước khi xóa\n"
     "- Hiện thông báo Xóa phiếu báo có thành công\n"
     "- Số tổng giảm đúng 1, PBC-14 biến mất\n"
     "- Dán đường dẫn chi tiết: hệ thống báo không tìm thấy dữ liệu"),

    (2, "Hủy hộp xác nhận thì không xóa", "P1",
     "Như ca trên, phiếu PBC-15 trạng thái Đang tạo",
     "1. Bấm bánh răng, bấm Xóa\n"
     "2. Ở hộp xác nhận bấm Hủy\n"
     "3. Đọc lại danh sách",
     "—",
     "- Không có thông báo nào\n"
     "- PBC-15 vẫn còn nguyên trong danh sách\n"
     "- Số tổng không đổi"),

    (3, "Xóa phiếu Đã duyệt bằng đường dẫn trực tiếp", "P0",
     "Tài khoản KT-1 có quyền Quản lý phiếu báo có; phiếu PBC-16 Đã duyệt 10.000.000 do chính KT-1 lập "
     "và đã ghi sổ",
     "1. Ghi lại số của phiếu PBC-16 trong sổ kế toán\n"
     "2. Xác nhận menu hành động của PBC-16 KHÔNG có mục Xóa\n"
     "3. Lấy đường dẫn xóa của một phiếu nháp bất kỳ, thay số định danh thành số của PBC-16\n"
     "4. Dán đường dẫn đó vào thanh địa chỉ\n"
     "5. Mở lại danh sách và mở lại sổ kế toán",
     "Đường dẫn xóa của phiếu Đã duyệt",
     "- ⚠️ Phiếu BỊ XÓA, hiện thông báo Xóa phiếu báo có thành công\n"
     "- ⚠️ Hai bút toán 10.000.000 VẪN còn nguyên trong sổ kế toán\n"
     "- Không còn chứng từ gốc để lần ngược bút toán\n"
     "- Đây là lỗ hổng, ghi nhận Failed (mục 9 ghi chú 7)"),

    (4, "Xóa phiếu do người khác lập bằng đường dẫn trực tiếp", "P0",
     "Tài khoản KT-2 có quyền Quản lý phiếu báo có; phiếu PBC-17 Đã duyệt do KT-1 lập",
     "1. Đăng nhập bằng KT-2, xác nhận menu hành động của PBC-17 rỗng\n"
     "2. Dán đường dẫn xóa của PBC-17 vào thanh địa chỉ\n"
     "3. Mở lại danh sách",
     "Đường dẫn xóa phiếu người khác",
     "- ⚠️ Phiếu của KT-1 BỊ KT-2 xóa mất\n"
     "- Hệ thống không kiểm tra người lập\n"
     "- Ghi nhận Failed"),

    (5, "Không có quyền Quản lý phiếu báo có thì xóa bị chặn", "P0",
     "Tài khoản NV-A không có quyền Quản lý phiếu báo có; phiếu PBC-18 trạng thái Đang tạo do NV-A lập",
     "1. Đăng nhập bằng NV-A, dán đường dẫn xóa của PBC-18\n"
     "2. Mở lại danh sách",
     "—",
     "- Hệ thống từ chối, báo không có quyền\n"
     "- PBC-18 vẫn còn nguyên"),

    (6, "Xóa phiếu thì các dòng chi tiết cũng mất theo", "P1",
     "Tài khoản KT-1; phiếu PBC-19 trạng thái Đang tạo có 3 dòng chi tiết",
     "1. Xóa PBC-19 qua menu hành động\n"
     "2. Mở màn Tổng hợp tiền về ngân hàng, lọc theo mã PBC-19\n"
     "3. Mở màn Tạo phiếu yêu cầu điều chỉnh công nợ, tìm dòng của PBC-19",
     "—",
     "- Không còn dòng nào của PBC-19 ở cả hai màn\n"
     "- Không có dòng chi tiết mồ côi nào hiện ra"),

    (7, "Xóa phiếu đã có phiếu điều chỉnh công nợ", "P0",
     "Phiếu PBC-20 Đã duyệt 10.000.000, đã lập phiếu điều chỉnh công nợ DCCN-01 gán trọn số tiền",
     "1. Dán đường dẫn xóa của PBC-20\n"
     "2. Mở lại danh sách phiếu báo có\n"
     "3. Mở chi tiết DCCN-01\n"
     "4. Mở báo cáo công nợ của khách hàng liên quan",
     "Đường dẫn xóa phiếu đã được điều chỉnh công nợ",
     "- ⚠️ PBC-20 bị xóa, hệ thống không cảnh báo gì về DCCN-01\n"
     "- DCCN-01 vẫn còn nhưng mất chứng từ gốc\n"
     "- Ghi lại chính xác con số công nợ trước và sau để đánh giá mức thiệt hại"),
]

# ============================================================ VII. IMPORT
SEC_VII = [
    (1, "Mở cửa sổ Import Báo có và tải tệp mẫu", "P0",
     "Tài khoản KT-1 vào được màn danh sách",
     "1. Mở mục Phiếu báo có\n"
     "2. Bấm nút Import Báo có\n"
     "3. Bấm liên kết File mẫu, mở tệp vừa tải\n"
     "4. Đọc tiêu đề các cột trong tệp mẫu",
     "—",
     "- Cửa sổ Import Excel mở ra, có ô Chọn file, liên kết File mẫu, nút Import và nút Hủy\n"
     "- Tải được tệp mẫu\n"
     "- Tệp mẫu có các cột theo thứ tự: Số tiền · Diễn giải · Ngày hạch toán · Mã ngân hàng · Số tài "
     "khoản · Tên chi nhánh · Loại tiền · Tỷ giá; dữ liệu bắt đầu từ dòng 2"),

    (2, "Import tệp hợp lệ 3 dòng", "P0",
     "Tệp Excel có 3 dòng hợp lệ, mỗi dòng số tiền khác nhau, ngày ghi dạng năm-tháng-ngày, mã ngân "
     "hàng, số tài khoản, tên chi nhánh, loại tiền đều đúng danh mục",
     "1. Bấm Import Báo có, chọn tệp, bấm Import\n"
     "2. Đọc thông báo hiện ra\n"
     "3. Đợi ít phút rồi mở biểu tượng chuông thông báo\n"
     "4. Đóng cửa sổ, tải lại danh sách, đếm số phiếu mới",
     "Tệp Excel: 3 dòng hợp lệ",
     "- Hiện thông báo File đã được tải lên và đang được xử lý\n"
     "- Sau ít phút có thông báo Import báo có thành công trên chuông\n"
     "- ⚠️ Danh sách có thêm ĐÚNG 3 PHIẾU RIÊNG BIỆT, không phải 1 phiếu 3 dòng (mục 9 ghi chú 17)"),

    (3, "Phiếu sinh từ Import có nội dung mặc định gì", "P0",
     "Vừa import xong 1 dòng số tiền 7.500.000, diễn giải \"CK thang 8\", ngày 2026-08-20, loại tiền "
     "tiền Việt Nam",
     "1. Mở chi tiết phiếu vừa sinh\n"
     "2. Đọc từng ô ở khối Thông tin chung\n"
     "3. Đọc dòng chi tiết duy nhất\n"
     "4. Mở sổ kế toán tìm bút toán của phiếu",
     "—",
     "- Trạng thái là ĐÃ DUYỆT ngay, không qua nháp\n"
     "- Loại thu là Thu bán hàng, Tài khoản nợ là tài khoản tiền gửi ngân hàng\n"
     "- Ngày hạch toán là 20/08/2026, Diễn giải là CK thang 8\n"
     "- Dòng chi tiết: khách hàng là KHÁCH KHÔNG RÕ, tài khoản có là tài khoản phải thu khách hàng, số "
     "tiền 7.500.000, không gắn hợp đồng\n"
     "- Sổ kế toán ĐÃ CÓ 2 bút toán của phiếu này"),

    (4, "Khối Chi tiết trong cửa sổ Import không bao giờ hiện số", "P0",
     "Tệp Excel có 2 dòng hợp lệ và 2 dòng sai định dạng ngày",
     "1. Bấm Import Báo có, chọn tệp, bấm Import\n"
     "2. Giữ nguyên cửa sổ, quan sát khu vực dưới ô Chọn file trong 2 phút\n"
     "3. Mở chuông thông báo, bấm vào liên kết trong thông báo",
     "Tệp Excel: 2 dòng đúng, 2 dòng sai ngày",
     "- ⚠️ Khối \"Chi tiết: Đã import / Đã bỏ qua / Không hợp lệ\" KHÔNG hiện ra, mọi con số đều trống\n"
     "- Kết quả thật chỉ đọc được qua tệp nhật ký mở từ liên kết trong thông báo\n"
     "- Trong tệp nhật ký: đã import 2, đã bỏ qua 2, không hợp lệ 2 kèm số dòng lỗi\n"
     "- Ghi nhận Failed (mục 9 ghi chú 19)"),

    (5, "Import dòng sai định dạng ngày", "P0",
     "Tệp Excel 3 dòng, dòng 2 ghi ngày dạng ngày/tháng/năm thay vì năm-tháng-ngày",
     "1. Import tệp\n"
     "2. Đợi xử lý xong, mở tệp nhật ký từ thông báo\n"
     "3. Đếm số phiếu mới trong danh sách",
     "Dòng 2 ghi ngày: 20/08/2026",
     "- Tệp nhật ký ghi \"Dòng 3: Ngày không đúng định dạng\" (dòng dữ liệu thứ 2 nằm ở dòng 3 của "
     "tệp)\n"
     "- Chỉ có 2 phiếu được tạo\n"
     "- ⚠️ Dòng lỗi được tính vào CẢ hai con số bỏ qua và không hợp lệ"),

    (6, "Import dòng có mã ngân hàng không tồn tại", "P1",
     "Tệp Excel 2 dòng, dòng 1 ghi mã ngân hàng không có trong danh mục",
     "1. Import tệp\n"
     "2. Mở tệp nhật ký\n"
     "3. Đếm số phiếu mới",
     "Mã ngân hàng: ZZZ",
     "- Tệp nhật ký ghi \"Ngân hàng không tồn tại\" kèm số dòng\n"
     "- Chỉ 1 phiếu được tạo"),

    (7, "Import dòng có số tài khoản hoặc chi nhánh không tồn tại", "P1",
     "Tệp Excel 3 dòng: dòng 1 sai tên chi nhánh, dòng 2 sai số tài khoản, dòng 3 đúng hết",
     "1. Import tệp\n"
     "2. Mở tệp nhật ký, đọc từng dòng lỗi\n"
     "3. Đếm số phiếu mới",
     "—",
     "- Nhật ký ghi rõ \"Tên chi nhánh không tồn tại\" và \"Số tài khoản không tồn tại\" kèm đúng số "
     "dòng\n"
     "- Chỉ 1 phiếu được tạo từ dòng 3\n"
     "- ⚠️ Tên chi nhánh phải khớp TUYỆT ĐỐI với danh mục, sai một dấu cách là bị loại"),

    (8, "Import dòng có loại tiền không tồn tại", "P1",
     "Tệp Excel 2 dòng, dòng 1 ghi mã loại tiền không có trong danh mục",
     "1. Import tệp\n"
     "2. Mở tệp nhật ký\n"
     "3. Đếm số phiếu mới",
     "Loại tiền: XYZ",
     "- Nhật ký ghi \"Loại tiền không tồn tại\" kèm số dòng\n"
     "- Chỉ 1 phiếu được tạo"),

    (9, "Dòng trống cả Số tiền và Ngày bị bỏ qua lặng lẽ", "P1",
     "Tệp Excel 4 dòng: dòng 1 và 2 hợp lệ, dòng 3 hoàn toàn trống, dòng 4 hợp lệ",
     "1. Import tệp\n"
     "2. Mở tệp nhật ký, đọc ba con số thống kê\n"
     "3. Đếm số phiếu mới",
     "—",
     "- 3 phiếu được tạo\n"
     "- ⚠️ Dòng trống KHÔNG được tính vào con số bỏ qua, cũng KHÔNG vào con số không hợp lệ, và không "
     "có dòng lỗi nào trong nhật ký\n"
     "- Đối chiếu số dòng trong tệp với ba con số thống kê sẽ LỆCH đúng bằng số dòng trống"),

    (10, "Import lại cùng một tệp sinh thêm bộ phiếu mới", "P0",
     "Vừa import xong tệp 3 dòng, đã có 3 phiếu mới trong danh sách",
     "1. Import lại đúng tệp đó lần thứ hai\n"
     "2. Đợi xử lý, tải lại danh sách\n"
     "3. Lọc theo Ghi chú bằng diễn giải trong tệp, đếm số dòng\n"
     "4. Mở sổ kế toán, đếm bút toán liên quan",
     "Cùng một tệp import 2 lần",
     "- ⚠️ Có 6 phiếu, mỗi dòng trong tệp sinh 2 phiếu trùng nội dung\n"
     "- Sổ kế toán có gấp đôi bút toán, tiền vào tài khoản ngân hàng bị đếm hai lần\n"
     "- Hệ thống KHÔNG cảnh báo trùng (mục 9 ghi chú 18)"),

    (11, "Import tệp sai định dạng tệp", "P1",
     "Có sẵn một tệp văn bản và một tệp ảnh",
     "1. Bấm Import Báo có, chọn tệp văn bản, bấm Import\n"
     "2. Đọc thông báo lỗi\n"
     "3. Thử lại với tệp ảnh\n"
     "4. Không chọn tệp nào, bấm Import",
     "Tệp .txt · tệp .png · không chọn tệp",
     "- Chọn tệp văn bản: hiện Import thất bại và dòng lỗi Không hợp lệ dưới ô Chọn file\n"
     "- Chọn tệp ảnh: kết quả tương tự\n"
     "- Không chọn tệp: hiện dòng lỗi Không được để trống\n"
     "- Không có phiếu nào được tạo trong cả ba trường hợp"),

    (12, "Import không đòi quyền Quản lý phiếu báo có", "P0",
     "Tài khoản NV-A KHÔNG có quyền Quản lý phiếu báo có; có sẵn tệp Excel 2 dòng hợp lệ",
     "1. Đăng nhập bằng NV-A, mở mục Phiếu báo có\n"
     "2. Soát nút Tạo mới và nút Import Báo có\n"
     "3. Bấm Import Báo có, chọn tệp, bấm Import\n"
     "4. Đợi xử lý rồi mở chế độ Phiếu của tôi",
     "—",
     "- Nút Tạo mới KHÔNG có nhưng nút Import Báo có VẪN có\n"
     "- ⚠️ Import chạy được, 2 phiếu ĐÃ DUYỆT được tạo dưới tên NV-A và đã ghi sổ\n"
     "- Người không được lập phiếu vẫn tạo được phiếu đã duyệt qua cửa này\n"
     "- Ghi nhận Failed"),
]

# ============================================================ VIII. RANG BUOC NHAP LIEU
SEC_VIII = [
    (1, "Bỏ trống các ô bắt buộc ở khối Thông tin chung", "P0",
     "Đang mở form Tạo phiếu báo có",
     "1. Xóa trắng ô Ngân hàng, ô Tài khoản, ô Ngày hạch toán, ô Tài khoản nợ\n"
     "2. Bấm Lưu\n"
     "3. Đọc dòng lỗi dưới từng ô",
     "—",
     "- Không lưu được\n"
     "- Ô Ngân hàng, Tài khoản, Ngày hạch toán, Tài khoản nợ đều hiện dòng lỗi Bắt buộc nhập hoặc Bắt "
     "buộc chọn\n"
     "- Bốn ô này đều có dấu sao đỏ ở nhãn"),

    (2, "Bỏ trống Diễn giải của dòng chi tiết", "P0",
     "Đang mở form, đã nhập đủ khối Thông tin chung, dòng 1 có khách hàng và số tiền nhưng để trống "
     "Diễn giải",
     "1. Bấm Lưu\n"
     "2. Đọc dòng lỗi ở cột Diễn giải\n"
     "3. Nhập Diễn giải rồi lưu lại",
     "Diễn giải: để trống",
     "- Lần 1 không lưu được, cột Diễn giải của dòng 1 hiện dòng lỗi Bắt buộc nhập\n"
     "- Nhập xong lưu được\n"
     "- ⚠️ Diễn giải bắt buộc cho TỪNG DÒNG, không phải chỉ ô Diễn giải ở khối Thông tin chung"),

    (3, "Bỏ trống Số tài khoản có của dòng chi tiết", "P0",
     "Đang mở form, xóa trắng ô Số tài khoản có của dòng 1",
     "1. Bấm Lưu\n"
     "2. Đọc dòng lỗi ở cột Số tài khoản có",
     "—",
     "- Không lưu được, cột Số tài khoản có hiện dòng lỗi Bắt buộc nhập"),

    (4, "Bắt buộc chọn Hợp đồng khi khách hàng không phải KHÁCH KHÔNG RÕ", "P0",
     "Đang mở form, Thu bán hàng; dòng 1 giữ nguyên tài khoản có mặc định, đã chọn khách KH-01, chưa "
     "chọn hợp đồng, đã nhập số tiền và diễn giải",
     "1. Bấm Lưu\n"
     "2. Đọc dòng lỗi ở cột Số đơn hàng/Hợp đồng\n"
     "3. Chọn hợp đồng rồi lưu lại",
     "Khách hàng: KH-01, chưa chọn hợp đồng",
     "- Lần 1 không lưu được, cột Số đơn hàng/Hợp đồng hiện dòng lỗi Bắt buộc nhập\n"
     "- Chọn hợp đồng xong thì lưu được"),

    (5, "Khách hàng KHÁCH KHÔNG RÕ thì không cần chọn Hợp đồng", "P0",
     "Đang mở form, Thu bán hàng; dòng 1 để nguyên khách mặc định KHÁCH KHÔNG RÕ, không chọn hợp đồng, "
     "đã nhập số tiền và diễn giải",
     "1. Bấm Lưu và duyệt\n"
     "2. Mở lại chi tiết phiếu\n"
     "3. Mở sổ kế toán đọc bút toán ghi Có",
     "Khách hàng: KHÁCH KHÔNG RÕ",
     "- ⚠️ Lưu được ngay, KHÔNG có dòng lỗi nào ở cột Hợp đồng\n"
     "- Bút toán ghi Có treo vào KHÁCH KHÔNG RÕ, không gắn hợp đồng nào\n"
     "- Đây là bẫy dễ sai nhất khi nhập nhanh (mục 9 ghi chú 10)"),

    (6, "Bắt buộc chọn Phiếu yc xuất hàng với hợp đồng nguyên tắc", "P0",
     "Đang mở form, Thu bán hàng; dòng 1 đã chọn khách KH-01 và hợp đồng nguyên tắc HDNT-01, chưa tích "
     "Số dư nợ đầu kì, chưa chọn Phiếu yc xuất hàng, đã nhập số tiền và diễn giải",
     "1. Bấm Lưu\n"
     "2. Đọc dòng lỗi ở cột Phiếu yc xuất hàng\n"
     "3. Chọn một phiếu yêu cầu xuất hàng rồi lưu lại",
     "Hợp đồng nguyên tắc, chưa chọn phiếu yc xuất hàng",
     "- Lần 1 không lưu được, cột Phiếu yc xuất hàng hiện dòng lỗi Bắt buộc nhập\n"
     "- Chọn phiếu xong thì lưu được"),

    (7, "Tích Số dư nợ đầu kì thì bỏ được Phiếu yc xuất hàng", "P0",
     "Như ca trên, dòng 1 gắn hợp đồng nguyên tắc HDNT-01 có số dư nợ đầu kì 50.000.000",
     "1. Tích ô Số dư nợ đầu kì\n"
     "2. Nhập Số tiền là 30.000.000\n"
     "3. Bấm Lưu và duyệt\n"
     "4. Mở lại chi tiết, soát ô tích Số dư đầu kì và cột Phiếu yc xuất hàng",
     "Số tiền: 30.000.000 · dư nợ đầu kì: 50.000.000",
     "- Lưu được, không đòi Phiếu yc xuất hàng\n"
     "- Chi tiết hiện ô tích Số dư đầu kì đã tích và bị khóa\n"
     "- Cột Phiếu yc xuất hàng để trống"),

    (8, "Số tiền vượt Số dư nợ đầu kì bị chặn", "P0",
     "Như ca trên, dòng 1 đã tích Số dư nợ đầu kì, dư nợ đầu kì là 50.000.000",
     "1. Nhập Số tiền là 60.000.000\n"
     "2. Bấm Lưu\n"
     "3. Đọc thông báo\n"
     "4. Sửa Số tiền về 50.000.000, lưu lại\n"
     "5. Thử với 50.000.001",
     "Số tiền: 60.000.000 · 50.000.000 · 50.000.001",
     "- 60.000.000: hiện cảnh báo \"Số tiền thu vượt quá dư nợ đầu kì hợp đồng\", KHÔNG lưu\n"
     "- ⚠️ Cảnh báo hiện ở góc màn hình, KHÔNG có dòng lỗi đỏ dưới ô Số tiền\n"
     "- 50.000.000: lưu được\n"
     "- 50.000.001: bị chặn"),

    (9, "Nhập Số tiền âm và Số tiền bằng chữ", "P0",
     "Đang mở form, đã nhập đủ các ô khác",
     "1. Nhập Số tiền dòng 1 là -1.000.000, bấm Lưu\n"
     "2. Nhập Số tiền là abc, bấm Lưu\n"
     "3. Nhập Số tiền là 0, bấm Lưu",
     "Số tiền: -1.000.000 · abc · 0",
     "- Số âm: không lưu được, hiện dòng lỗi ở cột Số tiền\n"
     "- Chữ: ô tự lọc bỏ ký tự không phải số, giá trị về 0\n"
     "- ⚠️ Số 0: LƯU ĐƯỢC bình thường, không có cảnh báo (xem mục V ca 5 và 6)"),

    (10, "Nhập Số tiền có phần thập phân", "P1",
     "Đang mở form, Loại tiền là đô la Mỹ tỷ giá 24.500",
     "1. Nhập Số tiền dòng 1 là 1234.56\n"
     "2. Đọc cột quy đổi VND\n"
     "3. Lưu và duyệt, mở danh sách đọc cột Tổng PS và Tổng PS VND",
     "Số tiền: 1.234,56 · Tỷ giá: 24.500",
     "- Cột VND hiện 30,246,720 (làm tròn về số nguyên)\n"
     "- Cột Tổng PS ngoài danh sách hiện 1,234.56 giữ đủ 2 số lẻ\n"
     "- Cột Tổng PS VND hiện 30,246,720 không có số lẻ"),

    (11, "Ngày hạch toán sai định dạng", "P1",
     "Đang mở form",
     "1. Xóa ô Ngày hạch toán, gõ tay 2026-08-25, bấm Lưu\n"
     "2. Gõ tay 32/08/2026, bấm Lưu\n"
     "3. Chọn ngày từ lịch, bấm Lưu",
     "Ngày: 2026-08-25 · 32/08/2026 · chọn từ lịch",
     "- Hai lần gõ tay sai dạng đều không lưu được, ô Ngày hạch toán hiện dòng lỗi Không đúng định "
     "dạng\n"
     "- Chọn từ lịch thì lưu được, giá trị ghi dạng ngày/tháng/năm"),

    (12, "Ngày hạch toán ở quá khứ xa và ở tương lai", "P1",
     "Đang mở form, đã nhập đủ mọi ô",
     "1. Chọn Ngày hạch toán là 01/01/2020, bấm Lưu và duyệt\n"
     "2. Mở sổ kế toán tìm bút toán\n"
     "3. Lập phiếu khác với Ngày hạch toán là 31/12/2030, lưu và duyệt",
     "Ngày: 01/01/2020 · 31/12/2030",
     "- ⚠️ Cả hai đều lưu được, hệ thống KHÔNG chặn ngày quá khứ và KHÔNG chặn ngày tương lai\n"
     "- Bút toán mang đúng ngày đã chọn, rơi vào kỳ kế toán đã khóa hoặc kỳ chưa tới\n"
     "- Ghi nhận là rủi ro nghiệp vụ cần báo lại"),

    (13, "Diễn giải và Ghi chú nhập chuỗi rất dài và ký tự đặc biệt", "P2",
     "Đang mở form",
     "1. Nhập Diễn giải dòng 1 dài hơn 500 ký tự có dấu tiếng Việt và ký tự & < >\n"
     "2. Nhập ô Diễn giải ở khối Thông tin chung tương tự\n"
     "3. Lưu và duyệt\n"
     "4. Mở lại chi tiết, mở danh sách đọc cột Diễn giải\n"
     "5. Mở màn Tổng hợp tiền về ngân hàng, xuất tệp Excel và mở ra",
     "Chuỗi dài hơn 500 ký tự có dấu và ký tự đặc biệt",
     "- Lưu được, nội dung hiển thị đúng nguyên văn ở chi tiết\n"
     "- Ngoài danh sách nội dung dài bị cắt ngắn theo bề rộng cột nhưng không mất dấu\n"
     "- Tệp Excel xuất ra không vỡ định dạng, ký tự & hiển thị đúng"),
]

# ============================================================ IX. CO LAP DU LIEU
SEC_IX = [
    (1, "Hai người cùng lập phiếu tại cùng thời điểm không trùng mã", "P0",
     "Tài khoản KT-1 và KT-2 cùng công ty TPE, cùng đang mở form Tạo mới với dữ liệu hợp lệ",
     "1. Cả hai bấm Lưu và duyệt trong vòng vài giây\n"
     "2. Mở danh sách, đọc mã của hai phiếu vừa lập\n"
     "3. Lọc theo tiền tố mã tháng hiện tại, soát toàn bộ mã",
     "—",
     "- Hai phiếu có mã KHÁC NHAU, số thứ tự liền nhau\n"
     "- Không có mã nào bị trùng trong danh sách"),

    (2, "Mã phiếu đổi tiền tố theo tháng lập", "P1",
     "Tài khoản KT-1 thuộc công ty TPE; đã có phiếu TPE.PBC0826.00017",
     "1. Lập một phiếu mới trong tháng 08 năm 2026, đọc mã\n"
     "2. Đổi ngày hệ thống sang tháng 09 năm 2026 hoặc đợi sang tháng mới\n"
     "3. Lập phiếu mới, đọc mã",
     "—",
     "- Phiếu tháng 08: mã TPE.PBC0826.00018, tăng tiếp số cũ\n"
     "- Phiếu tháng 09: mã TPE.PBC0926.00001, số thứ tự đếm lại từ đầu\n"
     "- ⚠️ Số thứ tự đếm riêng cho từng tháng và từng công ty"),

    (3, "Hai công ty có dãy mã riêng", "P1",
     "KT-1 thuộc công ty TPE, KT-3 thuộc công ty khác mã TPH",
     "1. KT-1 lập một phiếu, đọc mã\n"
     "2. KT-3 lập một phiếu, đọc mã",
     "—",
     "- Mã của KT-1 bắt đầu bằng TPE.PBC\n"
     "- Mã của KT-3 bắt đầu bằng TPH.PBC\n"
     "- Hai dãy số thứ tự chạy độc lập"),

    (4, "Hai người cùng sửa một phiếu nháp", "P0",
     "Phiếu PBC-21 trạng thái Đang tạo do KT-1 lập; KT-1 và KT-2 (đều có quyền Quản lý phiếu báo có) "
     "cùng mở form sửa PBC-21",
     "1. KT-1 sửa Số tiền dòng 1 thành 5.000.000, chưa lưu\n"
     "2. KT-2 sửa Số tiền dòng 1 thành 8.000.000, bấm Lưu\n"
     "3. KT-1 bấm Lưu\n"
     "4. Mở lại chi tiết PBC-21",
     "—",
     "- Cả hai lần lưu đều thành công, không có cảnh báo xung đột\n"
     "- ⚠️ Kết quả cuối là 5.000.000 — người lưu SAU ghi đè người lưu trước, thay đổi của KT-2 mất "
     "hoàn toàn\n"
     "- Ghi nhận là hiện trạng cần báo lại"),

    (5, "Một người xóa trong khi người khác đang sửa", "P1",
     "Phiếu PBC-22 trạng thái Đang tạo; KT-1 đang mở form sửa PBC-22; KT-2 xóa PBC-22 từ danh sách",
     "1. KT-2 xóa PBC-22 thành công\n"
     "2. KT-1 bấm Lưu ở form đang mở\n"
     "3. Đọc thông báo\n"
     "4. Mở lại danh sách",
     "—",
     "- KT-1 nhận thông báo Cập nhật phiếu báo có thất bại\n"
     "- Phiếu không sống lại, danh sách không có PBC-22\n"
     "- Không có dòng chi tiết mồ côi nào được tạo"),

    (6, "Đóng dấu đơn vị theo hồ sơ nhân sự tại thời điểm lập", "P1",
     "KT-1 thuộc phòng P1 công ty 1; KT-1 đã lập phiếu PBC-23; sau đó bộ phận nhân sự chuyển KT-1 sang "
     "phòng P2",
     "1. Ghi lại phòng ban của PBC-23 trước khi chuyển\n"
     "2. Chuyển KT-1 sang phòng P2 trong hồ sơ nhân sự\n"
     "3. Mở lại chi tiết PBC-23, đọc ô Phòng ban\n"
     "4. Ở chế độ Tất cả, lọc Phòng ban là P1 rồi lọc P2",
     "—",
     "- Ô Phòng ban của PBC-23 vẫn là P1, không đổi theo hồ sơ mới\n"
     "- Lọc P1 ra PBC-23, lọc P2 không ra\n"
     "- Phiếu KT-1 lập SAU khi chuyển thì thuộc P2"),

    (7, "Import chạy song song với thao tác lập tay", "P1",
     "KT-1 vừa bấm Import một tệp 50 dòng và việc nạp đang chạy ngầm",
     "1. Ngay sau khi bấm Import, mở form Tạo mới và lập một phiếu tay, bấm Lưu và duyệt\n"
     "2. Đợi việc nạp xong\n"
     "3. Lọc theo tiền tố mã tháng hiện tại, soát toàn bộ mã",
     "—",
     "- Phiếu lập tay lưu được, không bị lỗi\n"
     "- Không có mã nào bị trùng giữa phiếu lập tay và 50 phiếu từ tệp\n"
     "- Số thứ tự trong dãy mã liên tục, không nhảy cóc bất thường"),

    (8, "Tích Không báo tiền về ở hai cửa sổ cùng lúc", "P2",
     "Phiếu PBC-24 Đã duyệt có 1 dòng chi tiết; mở cùng một màn chi tiết ở hai cửa sổ trình duyệt",
     "1. Cửa sổ 1 tích ô Không báo tiền về\n"
     "2. Cửa sổ 2 (chưa tải lại) bỏ tích ô đó\n"
     "3. Tải lại cả hai cửa sổ, đọc trạng thái ô tích\n"
     "4. Mở màn Tổng hợp tiền về ngân hàng",
     "—",
     "- Kết quả cuối theo thao tác SAU CÙNG, không có cảnh báo xung đột\n"
     "- Hai cửa sổ sau khi tải lại hiện cùng một giá trị\n"
     "- Màn Tổng hợp tiền về ngân hàng khớp với giá trị đó"),

    (9, "Đối chiếu Tổng PS đã chốt với tổng dòng chi tiết", "P0",
     "Phiếu PBC-25 Đã duyệt, có 4 dòng chi tiết",
     "1. Mở chi tiết PBC-25, cộng tay cột Số tiền của 4 dòng\n"
     "2. Đọc ô Tổng cộng trong chi tiết\n"
     "3. Đọc cột Tổng PS của PBC-25 ngoài danh sách\n"
     "4. So ba con số",
     "—",
     "- Ba con số khớp nhau\n"
     "- ⚠️ Nếu lệch: cột ngoài danh sách là số ĐÃ CHỐT lúc lưu, ô Tổng cộng trong chi tiết là số tính "
     "lại tại chỗ; lệch nghĩa là dữ liệu bị sửa ngoài màn hình, phải báo lại ngay"),
]

# ============================================================ X. LUONG NGHIEP VU
SEC_X = [
    (1, "Luồng chuẩn: lập phiếu báo có bán hàng rồi điều chỉnh công nợ", "P0",
     "Tài khoản KT-1 có quyền Quản lý phiếu báo có; khách KH-01 có hợp đồng HD-01 còn nợ 20.000.000; "
     "tiền 20.000.000 đã về tài khoản ngân hàng TK-1",
     "1. Mở mục Phiếu báo có, bấm Tạo mới\n"
     "2. Chọn Thu bán hàng, ngân hàng NH-A, tài khoản TK-1, ngày hạch toán hôm nay\n"
     "3. Dòng 1: chọn KH-01, chọn HD-01, số tiền 20.000.000, diễn giải \"Thu tien HD-01\"\n"
     "4. Bấm Lưu và duyệt\n"
     "5. Mở chi tiết, tích chọn dòng 1, bấm Tạo phiếu yêu cầu điều chỉnh công nợ và hoàn tất phiếu "
     "điều chỉnh\n"
     "6. Quay lại chi tiết phiếu báo có, đọc ba cặp số\n"
     "7. Mở báo cáo công nợ KH-01 và mở màn Tổng hợp tiền về ngân hàng",
     "Số tiền: 20.000.000",
     "- Phiếu ở trạng thái Đã duyệt, mã có tiền tố PBC\n"
     "- Sổ kế toán có bút toán ghi Có phải thu 20.000.000 gắn KH-01 và HD-01, bút toán ghi Nợ tiền gửi "
     "ngân hàng 20.000.000\n"
     "- Sau khi điều chỉnh: Số tiền đã DCCN là 20.000.000, Số tiền chưa DCCN là 0\n"
     "- Công nợ HD-01 giảm 20.000.000\n"
     "- Màn Tổng hợp tiền về ngân hàng ghi dòng này là Đã điều chỉnh hết công nợ"),

    (2, "Luồng tiền về chưa rõ khách rồi gán lại sau", "P0",
     "Ngân hàng báo có 15.000.000 nhưng chưa biết của khách nào",
     "1. Lập phiếu báo có, để nguyên khách mặc định KHÁCH KHÔNG RÕ, số tiền 15.000.000, không chọn hợp "
     "đồng\n"
     "2. Bấm Lưu và duyệt\n"
     "3. Mở màn Tổng hợp tiền về ngân hàng, tìm dòng vừa tạo\n"
     "4. Tích chọn dòng đó và tạo phiếu yêu cầu điều chỉnh công nợ gán về KH-01 và HD-01\n"
     "5. Quay lại chi tiết phiếu báo có, đọc ba cặp số\n"
     "6. Mở báo cáo công nợ KH-01",
     "Số tiền: 15.000.000",
     "- Lưu được ngay dù không có hợp đồng\n"
     "- Dòng hiện ở màn Tổng hợp tiền về ngân hàng với trạng thái Chưa điều chỉnh hết công nợ\n"
     "- Sau khi điều chỉnh: Số tiền chưa DCCN về 0\n"
     "- Công nợ KH-01 giảm 15.000.000"),

    (3, "Luồng thu nhà cung cấp", "P1",
     "Nhà cung cấp NCC-01 hoàn lại 8.000.000, có phiếu xuất hàng PX-01 gắn hợp đồng mua HDM-01",
     "1. Lập phiếu báo có, chọn Thu nhà cung cấp\n"
     "2. Dòng 1: chọn NCC-01, chọn phiếu xuất PX-01, đọc cột Hợp đồng mua và cột Số tài khoản có mặc "
     "định\n"
     "3. Nhập số tiền 8.000.000 và diễn giải, bấm Lưu và duyệt\n"
     "4. Mở sổ kế toán, đọc tài khoản của bút toán ghi Có\n"
     "5. Mở báo cáo công nợ nhà cung cấp\n"
     "6. Mở màn Tổng hợp tiền về ngân hàng, tìm dòng này",
     "Số tiền: 8.000.000",
     "- Số tài khoản có mặc định là tài khoản phải trả nhà cung cấp\n"
     "- Cột Hợp đồng mua tự điền HDM-01\n"
     "- Bút toán ghi Có đúng tài khoản đó, gắn đúng NCC-01\n"
     "- Công nợ phải trả NCC-01 giảm 8.000.000\n"
     "- ⚠️ Dòng này KHÔNG hiện ở màn Tổng hợp tiền về ngân hàng (màn đó chỉ lấy các tài khoản phải thu "
     "và phải trả đã cấu hình sẵn)"),

    (4, "Luồng phiếu ngoại tệ đầu cuối", "P0",
     "Khách nước ngoài chuyển 2.000 đô la Mỹ, tỷ giá danh mục 24.500, hợp đồng HD-02 ghi bằng đô la Mỹ",
     "1. Lập phiếu báo có, chọn Loại tiền là đô la Mỹ, xác nhận tỷ giá tự điền 24.500\n"
     "2. Chọn ngân hàng và tài khoản ngoại tệ\n"
     "3. Dòng 1: chọn khách, chọn HD-02, nhập 2.000, đọc cột quy đổi VND\n"
     "4. Bấm Lưu và duyệt\n"
     "5. Đọc cột Tổng PS, Tỷ giá, Tổng PS VND ngoài danh sách\n"
     "6. Mở sổ kế toán đọc cả số nguyên tệ và số quy đổi của bút toán",
     "Số tiền: 2.000 · Tỷ giá: 24.500",
     "- Cột quy đổi VND trong form hiện 49,000,000\n"
     "- Ngoài danh sách: Tổng PS 2,000.00 · Tỷ giá 24,500 · Tổng PS VND 49,000,000\n"
     "- Bút toán lưu cả số nguyên tệ 2.000, số quy đổi 49.000.000 và tỷ giá 24.500"),

    (5, "Luồng Import hàng loạt tiền về cuối ngày", "P0",
     "Kế toán có sao kê ngân hàng 20 dòng tiền về trong ngày, đã chuyển thành tệp Excel theo mẫu",
     "1. Mở mục Phiếu báo có, bấm Import Báo có, chọn tệp, bấm Import\n"
     "2. Đợi xử lý, mở tệp nhật ký từ thông báo, đối chiếu ba con số\n"
     "3. Mở danh sách, lọc Hạch toán từ - đến đúng ngày sao kê, đếm số phiếu\n"
     "4. Cộng tay cột Tổng PS VND của 20 dòng, so với tổng tiền về trong sao kê\n"
     "5. Mở màn Tổng hợp tiền về ngân hàng, lọc cùng khoảng ngày\n"
     "6. Chọn từng dòng và tạo phiếu yêu cầu điều chỉnh công nợ về đúng khách hàng",
     "Tệp Excel: 20 dòng sao kê",
     "- Nhật ký ghi đã import 20, bỏ qua 0, không hợp lệ 0\n"
     "- Danh sách có đúng 20 PHIẾU RIÊNG, tất cả ở trạng thái Đã duyệt\n"
     "- Tổng cột Tổng PS VND khớp đúng tổng sao kê\n"
     "- Cả 20 dòng đều hiện ở màn Tổng hợp tiền về ngân hàng với trạng thái Chưa điều chỉnh hết công "
     "nợ\n"
     "- Sau khi điều chỉnh hết thì cả 20 dòng chuyển sang Đã điều chỉnh hết công nợ"),

    (6, "Luồng sửa sai sau khi đã duyệt nhầm", "P0",
     "KT-1 vừa bấm Lưu và duyệt nhầm một phiếu số tiền 100.000.000 lẽ ra là 10.000.000, chưa lập phiếu "
     "điều chỉnh công nợ",
     "1. Ghi lại bút toán hiện có trong sổ\n"
     "2. Dán đường dẫn sửa của phiếu, sửa Số tiền về 10.000.000\n"
     "3. Bấm Lưu và duyệt\n"
     "4. Mở lại sổ kế toán, đếm và đọc bút toán\n"
     "5. Mở báo cáo công nợ khách hàng liên quan\n"
     "6. Mở màn Tổng hợp tiền về ngân hàng",
     "Số tiền: từ 100.000.000 về 10.000.000",
     "- Vẫn đúng 2 bút toán, số tiền là 10.000.000, bút toán cũ đã bị xóa\n"
     "- Công nợ khách hàng đúng theo 10.000.000\n"
     "- ⚠️ Ghi nhận rằng đường đi này chỉ vào được bằng cách dán đường dẫn, giao diện không có nút "
     "(mục 9 ghi chú 5) — cần đề xuất bổ sung nút sửa hợp lệ cho phiếu đã duyệt"),

    (7, "Đối chiếu tổng số phiếu sau khi chạy hết bộ test", "P1",
     "Đã chạy xong các mục trên, biết số phiếu đã tạo tay, số phiếu sinh từ Import và số phiếu đã xóa "
     "trong quá trình test",
     "1. Mở chế độ Tất cả bằng tài khoản có quyền xem tổng công ty\n"
     "2. Bấm nút làm mới bộ lọc, đọc số tổng\n"
     "3. Đối chiếu với số ghi nhận đầu buổi cộng số phiếu mới trừ số phiếu đã xóa\n"
     "4. Lọc Hạch toán từ - đến đúng khoảng ngày test, cộng cột Tổng PS VND\n"
     "5. So với sổ kế toán phần tiền về tài khoản ngân hàng trong cùng khoảng",
     "—",
     "- Số phiếu khớp chính xác\n"
     "- ⚠️ Tổng tiền theo danh sách LỚN HƠN tổng ghi sổ đúng bằng phần tiền của các phiếu nháp và các "
     "dòng có số tiền bằng 0\n"
     "- ⚠️ KHÔNG dùng cặp ô Từ ngày / Đến ngày để đối chiếu vì hai ô đó không có tác dụng (mục 4)"),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", SEC_III),
    ("IV", "TẠO MỚI / SỬA / XEM CHI TIẾT", SEC_IV),
    ("V", "LƯU VÀ DUYỆT - GHI SỔ KẾ TOÁN", SEC_V),
    ("VI", "XÓA", SEC_VI),
    ("VII", "IMPORT BÁO CÓ", SEC_VII),
    ("VIII", "RÀNG BUỘC NHẬP LIỆU", SEC_VIII),
    ("IX", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", SEC_IX),
    ("X", "LUỒNG NGHIỆP VỤ ĐẦU - CUỐI", SEC_X),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Phiếu báo có (ERP) - Cập nhật ngày 25/08/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )
