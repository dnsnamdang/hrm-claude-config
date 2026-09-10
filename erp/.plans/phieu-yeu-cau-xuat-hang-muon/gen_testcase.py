# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Phieu yeu cau xuat hang muon"
(admin/warehouse/borrow_export_requests).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.
Doi chieu voi ban da xuat cho man "De nghi thu tien"
(`.plans/de-nghi-thu-tien/gen_testcase.py`).

⚠️ Tai lieu nay viet theo LOGIC ERP dang chay tren nhanh gop_db (repo D:/laragon/www/erp).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :1170-1183 (nhom borrow_export_requests), :1052 (getDataForBorrowExport)
  app/Http/Controllers/Warehouse/BorrowExportRequestController.php (toan bo)
  app/Model/Warehouse/BorrowExportRequest.php (searchByFilter, canView, canApprove,
      canEdit, canReturn, approve, generateCode, print_data, product_table)
  app/Model/Warehouse/ProductExportRequest.php :1320 getDataForBorrowExport,
      :1486 getCanBorrowExportAttribute, :2296 nhanh mac dinh cua searchByFilter
  app/Model/Warehouse/ProductExportRequestDetail.php :65 getReturningQty
  app/Http/Controllers/Warehouse/BorrowExportController.php :99-225 (duyet = tao phieu xuat)
  app/Model/Warehouse/BorrowExport.php :197-204 (ghi so luong duoc duyet)
  app/Helpers/NotificationHelper.php :40 sendNotifyWithPermission
  app/Helpers/FormatHelper.php :80 generateCode, :804 addDay
  app/Model/Common/ReportTemplate.php (KHONG co hang so mau in yeu cau xuat hang muon)
  app/ExcelExports/BorrowExportRequestExcel.php
      + resources/views/reports/exports/borrow_export_request_export.blade.php
  resources/views/warehouse/borrow_export_requests/*.blade.php
  resources/views/partials/classes/Warehouse/BorrowExportRequest*.blade.php
  resources/views/partials/classes/base/Datatable.blade.php
  resources/views/warehouse/borrow_exports/formJs.blade.php
  resources/views/layouts/topmenubar.blade.php :324, :1059, :2295
  database/seeds/PermissionsTableSeeder.php :1225-1227

Chay:  python .plans/phieu-yeu-cau-xuat-hang-muon/gen_testcase.py
"""
import os
import sys

try:  # console Windows mac dinh cp1252
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

# .plans/phieu-yeu-cau-xuat-hang-muon -> .plans -> erp -> hrm-claude-config -> hrm/.claude/...
sys.path.insert(0, os.path.join(
    HERE, "..", "..", "..", "hrm", ".claude", "skills", "testcase-documenter", "assets"))

from tc_engine import build  # noqa: E402

OUT = os.path.join(HERE, "testcase.xlsx")

MODULE = "Yêu cầu xuất hàng mượn"

# ============================================================ 9 MUC MO TA
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Quản lý Phiếu yêu cầu xuất hàng mượn: chứng từ do người kinh doanh lập để xin xuất tiếp "
     "phần hàng mà khách hàng ĐANG MƯỢN theo một hoặc nhiều Phiếu yêu cầu xuất hàng loại "
     "\"Xuất mượn\" đã hạch toán trước đó.\n"
     "Người dùng làm được: xem danh sách, lọc, tạo phiếu, xem chi tiết và xuất excel danh sách.\n"
     "Kế toán kho có màn riêng để xử lý, với 2 lựa chọn: \"Tạo phiếu xuất hàng mượn\" (đồng ý — "
     "chuyển sang màn lập Phiếu xuất hàng mượn) hoặc \"Không duyệt\" (từ chối, bắt buộc nhập "
     "Ghi chú duyệt).\n"
     "⚠️ KHÔNG có nút Duyệt riêng: phiếu chỉ chuyển sang Đã duyệt tại thời điểm Kế toán kho LƯU "
     "THÀNH CÔNG Phiếu xuất hàng mượn sinh ra từ nó. Bỏ dở giữa chừng thì phiếu vẫn ở Chờ duyệt.\n"
     "Màn hình có 5 lối vào dùng chung một bảng dữ liệu — xem mục 5."),

    ("2. Đối tượng được tính / hiển thị",
     "Bảng khai báo đủ 4 trạng thái: Đã duyệt · Chờ duyệt · Đang tạo · Không duyệt. Nhãn Đã duyệt "
     "tô XANH, ba nhãn còn lại tô ĐỎ.\n"
     "⚠️ Trạng thái \"Đang tạo\" trên thực tế KHÔNG BAO GIỜ sinh ra: màn tạo chỉ có nút Gửi và "
     "luôn lưu thẳng ở trạng thái Chờ duyệt. Không có chức năng lưu nháp. Lọc Trạng thái = Đang "
     "tạo luôn ra 0 dòng.\n"
     "Phạm vi phiếu nhìn thấy phụ thuộc lối vào đang mở:\n"
     "- Lối vào \"Phiếu của tôi\" (đường dẫn danh sách không kèm tham số): chỉ phiếu do chính "
     "mình lập.\n"
     "- Lối vào \"Tất cả\" (mục menu Phiếu Yêu cầu xuất hàng mượn): lấy theo 3 quyền xem ở mục 7.\n"
     "- Lối vào \"Chờ duyệt\" (mục menu Phiếu yêu cầu xuất hàng mượn chờ duyệt): mọi phiếu trạng "
     "thái Chờ duyệt thuộc công ty của người đăng nhập, KHÔNG áp 3 quyền xem theo cấp.\n"
     "- Lối vào \"Kế toán kho\" (mục menu Yêu cầu xuất hàng mượn): mọi phiếu KHÁC Đang tạo thuộc "
     "công ty của người đăng nhập, chỉ khi người đó có quyền \"Kế toán kho\".\n"
     "- Lối vào \"Trả hàng\": chỉ phiếu Đã duyệt do chính mình lập; không có mục menu nào trỏ tới.\n"
     "Bốn cột luôn hiển thị như nhau ở mọi lối vào: Mã phiếu, Người lập, Ngày lập, Trạng thái, "
     "Người duyệt, Ngày duyệt, Hành động."),

    ("3. Đối tượng bị ẩn / không tính",
     "- ⚠️ Ở MỌI lối vào, hệ thống luôn chèn thêm điều kiện cuối cùng: chỉ lấy phiếu thuộc ĐÚNG "
     "công ty của người đang đăng nhập. Vì vậy quyền \"Xem phiếu hàng mượn theo tổng công ty\" "
     "trên thực tế KHÔNG mở thêm được dòng nào — xem mục 7 và mục 9.\n"
     "- Cũng ở mọi lối vào, phiếu trạng thái Đang tạo của NGƯỜI KHÁC bị ẩn. Do trạng thái này "
     "không bao giờ sinh ra nên luật này không quan sát được từ giao diện.\n"
     "- Ô \"Hành động\" chỉ có duy nhất mục \"Tạo phiếu xuất hàng mượn\", và chỉ hiện khi phiếu "
     "đang ở Chờ duyệt VÀ người đăng nhập có quyền \"Kế toán kho\". Với mọi dòng khác, bấm vào "
     "biểu tượng bánh răng chỉ ra một khung rỗng.\n"
     "- KHÔNG có nút Sửa, KHÔNG có nút Xóa, KHÔNG có nút In ở ngoài danh sách — cả ba chức năng "
     "này đều đã bị gỡ khỏi hệ thống hoặc khỏi giao diện.\n"
     "- Nút \"Không duyệt\" chỉ hiện trong màn chi tiết, cùng điều kiện với mục Hành động.\n"
     "- Nút \"Tạo mới\" và nút \"Xuất excel\" hiện ở CẢ 4 lối vào dùng chung màn danh sách, kể cả "
     "màn Chờ duyệt — xem mục 9.\n"
     "- Riêng lối vào \"Kế toán kho\" có bố cục khác hẳn: KHÔNG có nút Bộ lọc, KHÔNG có nút Tạo "
     "mới, KHÔNG có nút Xuất excel; các ô lọc nằm sẵn trên màn, không thu gọn.\n"
     "- Cửa sổ chọn \"Phiếu yêu cầu xuất hàng\" khi lập phiếu chỉ liệt kê phiếu do CHÍNH MÌNH "
     "lập, loại \"Xuất mượn\", trạng thái \"Đã hạch toán\", tình trạng mượn \"Đã mượn\".\n"
     "- Trong cửa sổ đó, hàng hóa đã trả hết (số đã trả bằng số đã xuất) hoặc dòng không cần xuất "
     "kho sẽ không được kéo về bảng Chi tiết.\n"
     "- Màn hình KHÔNG có chức năng Nhập excel."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Hai ô \"Từ ngày\" và \"Đến ngày\" lọc theo NGÀY LẬP PHIẾU (cột Ngày lập).\n"
     "Ô \"Từ ngày\" tính từ 0 giờ của ngày điền vào — trọn ngày đầu được lấy.\n"
     "Ô \"Đến ngày\" tính tới 0 giờ của NGÀY KẾ TIẾP — trọn ngày cuối được lấy. ⚠️ Kèm theo một "
     "sai số nhỏ: phiếu lập đúng 0 giờ 0 phút 0 giây của ngày liền sau ngày điền ở ô \"Đến ngày\" "
     "vẫn lọt vào kết quả. Rất hiếm gặp nhưng cần biết khi đối chiếu số liệu.\n"
     "Không có bộ lọc theo Ngày duyệt, dù cột Ngày duyệt vẫn hiển thị và vẫn sắp xếp được.\n"
     "Hai ô ngày KHÔNG được hệ thống ghi nhớ khi rời màn — xem mục 9."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Ba cấp: Phiếu → Hàng hóa → Dòng theo từng phiếu mượn.\n"
     "- Phiếu giữ: Mã phiếu, Ghi chú, File đính kèm, Trạng thái, Ghi chú duyệt, Người lập, Người "
     "duyệt, Ngày duyệt, Công ty / Phòng ban / Bộ phận, và danh sách \"Phiếu xuất mượn\" nguồn.\n"
     "- Một phiếu gắn được NHIỀU Phiếu yêu cầu xuất hàng nguồn cùng lúc.\n"
     "- Mỗi hàng hóa giữ: Tên hàng hóa, Mã, Model, Thương hiệu, Đơn vị tính, Đơn giá, Số lượng "
     "xuất, Thành tiền.\n"
     "- Dưới mỗi hàng hóa là các dòng con, mỗi dòng ứng với một phiếu mượn nguồn: Phiếu mượn · "
     "Đang mượn · Xuất (ở màn chi tiết là Xuất · Được duyệt).\n"
     "- Mã phiếu sinh tự động dạng PYCXHM- kèm 5 chữ số, ví dụ PYCXHM-00317. ⚠️ Số này chạy "
     "chung cho toàn hệ thống, KHÔNG có mã công ty, KHÔNG reset theo tháng hay theo năm; khi số "
     "thứ tự vượt quá 5 chữ số thì mã dài thêm chứ không cắt bớt. Không sửa tay được.\n"
     "- Công ty / Phòng ban / Bộ phận của phiếu lấy từ hồ sơ nhân sự của người lập tại thời điểm "
     "lập phiếu, và không đổi về sau.\n"
     "- Năm lối vào (Phiếu của tôi · Tất cả · Chờ duyệt · Kế toán kho · Trả hàng) dùng CHUNG một "
     "nguồn dữ liệu; khác nhau ở phạm vi lọc và ở bố cục nút phía trên bảng."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- \"Số lượng xuất\" của một hàng hóa = TỔNG cột Xuất của mọi dòng phiếu mượn nằm dưới nó.\n"
     "- \"Thành tiền\" của một hàng hóa = Đơn giá × Số lượng xuất.\n"
     "- Dòng \"Tổng cộng\" cuối bảng = tổng cột Thành tiền của mọi hàng hóa.\n"
     "- Cột \"Đang mượn\" của mỗi dòng = (Số đã xuất mượn − Số đã trả) chia cho hệ số đơn vị "
     "đang chọn, rồi LÀM TRÒN XUỐNG, và ĐÃ TRỪ tiếp phần đang bị giữ chỗ bởi các phiếu chưa xử "
     "lý xong: phiếu yêu cầu nhập trả hàng mượn chưa hoàn tất, phiếu yêu cầu xuất bán hàng mượn "
     "đang Chờ duyệt, và phiếu yêu cầu xuất hàng mượn khác đang Chờ duyệt.\n"
     "- Một hàng hóa nằm trong 2 phiếu mượn khác nhau thì hiện 2 dòng con, KHÔNG gộp.\n"
     "- Không cho chọn TRÙNG một Phiếu yêu cầu xuất hàng trong cùng một phiếu: chọn lại thì hệ "
     "thống báo \"Không thể chọn yêu cầu này! Nguyên nhân: Yêu cầu đã được chọn.\"\n"
     "- Không cho thêm TRÙNG một hàng hóa bằng nút dấu cộng: báo \"Hàng hóa đã tồn tại\".\n"
     "- Hai ô lọc Mã hàng và Tên hàng dò trong TOÀN BỘ hàng hóa của phiếu: khớp một dòng là cả "
     "phiếu hiện ra. Điền cả hai ô thì phiếu phải khớp cả hai, nhưng được phép khớp ở 2 hàng hóa "
     "khác nhau.\n"
     "- Một phiếu khớp nhiều điều kiện lọc vẫn chỉ hiện một dòng."),

    ("7. Phân quyền cấp",
     "Bốn quyền liên quan trực tiếp tới màn hình này:\n"
     "1. \"Xem phiếu hàng mượn theo tổng công ty\" — ý đồ là thấy phiếu của mọi công ty; bộ lọc "
     "hiện thêm ô Công ty và ô Phòng ban. ⚠️ Trên thực tế KHÔNG mở thêm dòng nào, xem mục 3 và "
     "mục 9.\n"
     "2. \"Xem phiếu hàng mượn theo công ty\" — thấy mọi phiếu trong công ty mình; bộ lọc hiện "
     "thêm ô Phòng ban.\n"
     "3. \"Xem phiếu hàng mượn theo phòng ban\" — chỉ phiếu thuộc các phòng ban mình được phân "
     "công quản lý trong công ty mình, cộng phiếu do chính mình lập; bộ lọc hiện ô Phòng ban và "
     "ô Bộ phận.\n"
     "4. \"Kế toán kho\" — thấy 2 mục menu riêng (Yêu cầu xuất hàng mượn và Phiếu yêu cầu xuất "
     "hàng mượn chờ duyệt), được bấm Không duyệt và được bấm Tạo phiếu xuất hàng mượn.\n"
     "Ba quyền xem xét theo THỨ TỰ TRÊN XUỐNG, ai có quyền cao hơn thì lấy nhánh rộng hơn; ai "
     "không có quyền nào trong ba quyền trên thì chỉ thấy phiếu do chính mình lập.\n"
     "Ngoài ra ba quyền dùng chung toàn hệ thống — \"Xem tất cả phiếu\", \"Xem tất cả phiếu của "
     "công ty\", \"Xem tất cả phiếu của phòng ban\" — CHỈ làm hiện thêm các ô lọc Công ty / Phòng "
     "ban / Bộ phận, KHÔNG mở thêm phạm vi dữ liệu. Xem mục 9.\n"
     "⚠️ KHÔNG có bất kỳ đường dẫn nào của màn này được hệ thống chặn bằng quyền. Cả màn Kế toán "
     "kho lẫn màn Chờ duyệt đều mở được bằng cách dán đường dẫn, chỉ khác là mục menu bị ẩn. "
     "Nhóm test bỏ qua giao diện (các ca TC-ROLE cuối và mục IX) dựng riêng để đo mức rủi ro này."),

    ("8. Cách tính các ô thống kê",
     "- Ô \"Hiển thị a đến b trong tổng số N\" dưới bảng: a là dòng đầu trang đang xem, b là dòng "
     "cuối, N là tổng số phiếu khớp bộ lọc trong phạm vi lối vào đang mở.\n"
     "- Ô \"Số dòng mỗi trang\": mặc định 10; đổi số dòng thì bảng quay về trang 1.\n"
     "- Cột STT đánh liên tục theo trang: trang 2 với 10 dòng mỗi trang bắt đầu từ 11.\n"
     "- Cột \"Ngày lập\" và \"Ngày duyệt\" hiển thị ngày/tháng/năm kèm giờ:phút.\n"
     "- Cột \"Người lập\" hiển thị dạng \"Mã phòng ban - Họ tên\"; cột \"Người duyệt\" chỉ hiện "
     "họ tên, để trống khi phiếu chưa được xử lý.\n"
     "- File excel danh sách có đúng 7 cột: STT, Mã phiếu, Người lập, Ngày lập, Trạng thái, Người "
     "duyệt, Ngày duyệt; ngày ở file excel chỉ có ngày/tháng/năm, KHÔNG có giờ.\n"
     "- File excel xuất TOÀN BỘ kết quả khớp bộ lọc, không giới hạn theo trang đang xem, và có "
     "thêm một dòng \"Từ ngày ... đến ngày ...\" ngay dưới tiêu đề nếu có điền ô ngày."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất của màn này — đọc trước khi chạy test:\n"
     "1. ⚠️ Quyền \"Xem phiếu hàng mượn theo tổng công ty\" KHÔNG có tác dụng. Hệ thống luôn "
     "chèn thêm điều kiện lọc theo công ty của người đăng nhập ở bước cuối cùng, đè lên mọi "
     "nhánh quyền. Chọn một công ty khác ở ô lọc Công ty luôn ra 0 dòng. Ghi nhận Failed.\n"
     "2. ⚠️ Cùng điều kiện đó cũng làm mất tác dụng của luật \"vẫn luôn thấy phiếu do chính mình "
     "lập\": người vừa chuyển công ty sẽ KHÔNG còn thấy phiếu cũ do chính mình lập ở công ty cũ.\n"
     "3. ⚠️ Đường dẫn màn \"Chờ duyệt\" KHÔNG được chặn bằng quyền. Người không có quyền \"Kế "
     "toán kho\" dán thẳng đường dẫn này vào thanh địa chỉ sẽ thấy MỌI phiếu Chờ duyệt của công "
     "ty, kể cả phiếu của người khác mà bình thường họ không được thấy. Đây là lỗ hổng lộ dữ "
     "liệu, ghi nhận Failed.\n"
     "4. ⚠️ Chức năng In phiếu HỎNG HẲN: đường dẫn in luôn báo lỗi vì hệ thống trỏ tới một mẫu "
     "in chưa được khai báo. Nút In cũng đã bị gỡ khỏi giao diện nên chỉ vào được bằng đường "
     "dẫn. Ghi nhận Failed và ghi rõ là lỗi cấu hình mẫu in.\n"
     "5. ⚠️ Ở màn Chờ duyệt vẫn hiện nút \"Tạo mới\" và nút \"Xuất excel\", tuy nghiệp vụ của "
     "màn này chỉ là phê duyệt. Bấm Tạo mới ở đây vẫn mở màn lập phiếu bình thường.\n"
     "6. ⚠️ Người có quyền \"Kế toán kho\" mở được màn chi tiết của MỌI phiếu khác Đang tạo, kể "
     "cả phiếu của công ty khác, chỉ cần biết đường dẫn — trong khi danh sách không bao giờ hiện "
     "phiếu công ty khác. Ghi nhận Failed.\n"
     "7. ⚠️ Ô lọc \"Bộ phận\" (hiện với người có quyền theo phòng ban) KHÔNG có tác dụng: chọn "
     "bộ phận nào cũng ra nguyên kết quả cũ.\n"
     "8. ⚠️ Ba quyền dùng chung \"Xem tất cả phiếu\" / \"...của công ty\" / \"...của phòng ban\" "
     "làm hiện thêm ô lọc Công ty / Phòng ban / Bộ phận nhưng KHÔNG mở thêm dữ liệu. Người chỉ "
     "có quyền chung sẽ thấy ô lọc Công ty mà bên dưới vẫn chỉ là phiếu của chính mình.\n"
     "9. ⚠️ Không có nút Duyệt. Phiếu chỉ chuyển Đã duyệt khi Kế toán kho LƯU THÀNH CÔNG Phiếu "
     "xuất hàng mượn. Bấm \"Tạo phiếu xuất hàng mượn\" rồi thoát giữa chừng thì phiếu vẫn Chờ "
     "duyệt — đây là hành vi đúng, KHÔNG ghi Failed.\n"
     "10. ⚠️ Gõ chữ hoặc ký tự lạ vào ô \"Xuất\" thì ô tự trả về 0 và KHÔNG báo lỗi gì. Dễ nhầm "
     "là đã nhập được số.\n"
     "11. ⚠️ Đổi \"Đơn vị tính\" của một hàng hóa làm đổi cả Đơn giá và cột \"Đang mượn\" (chia "
     "theo hệ số quy đổi) nhưng KHÔNG xóa số đã nhập ở cột Xuất. Số vừa nhập có thể lập tức vượt "
     "trần và dòng chuyển sang màu báo lỗi. Kiểm lại sau mỗi lần đổi đơn vị.\n"
     "12. ⚠️ Trạng thái \"Đang tạo\" có trong ô lọc nhưng không bao giờ có phiếu nào mang trạng "
     "thái đó. Lọc ra 0 dòng là ĐÚNG, không ghi Failed.\n"
     "13. Bộ lọc được ghi nhớ RIÊNG cho từng lối vào, gồm cả số trang đang xem, nhưng KHÔNG nhớ "
     "hai ô Từ ngày / Đến ngày. Rời màn rồi quay lại vẫn còn điều kiện lọc cũ — test xong nhớ "
     "bấm nút làm mới bộ lọc trước khi sang ca test khác.\n"
     "14. Không cần bấm nút tìm kiếm: gõ hoặc chọn xong, chờ khoảng nửa giây là bảng tự nạp lại.\n"
     "15. ⚠️ Kiểm tra ở phía hệ thống khi lưu phiếu chỉ xét \"phiếu nguồn có phải của chính mình "
     "không\", KHÔNG xét trạng thái và KHÔNG xét loại xuất. Nhóm test bỏ qua giao diện khai thác "
     "được điều này — xem TC-ROLE-15 và TC-ROLE-16."),
]

# ============================================================ TC PHAN QUYEN
ROLE_TCS = [
    ("00", "Tài khoản không có quyền xem nào chỉ thấy phiếu do chính mình lập", "P0",
     "Tài khoản NV-A không được gán quyền nào trong 3 quyền xem phiếu hàng mượn; NV-A đã lập 12 "
     "phiếu; công ty của NV-A có 90 phiếu của nhiều người",
     "1. Đăng nhập bằng NV-A\n"
     "2. Mở menu Khởi tạo, nhóm Hàng hóa, khối Mượn hàng, bấm mục Phiếu Yêu cầu xuất hàng mượn\n"
     "3. Đọc số tổng dưới bảng\n"
     "4. Lật hết các trang, soát cột Người lập",
     "Tài khoản: NV-A (không quyền xem theo cấp)",
     "- Vào được màn hình, không bị chặn\n"
     "- Tổng hiện đúng 12\n"
     "- Mọi dòng đều có Người lập là NV-A\n"
     "- Nút Tạo mới VẪN hiển thị (hành vi lập phiếu không gắn quyền)\n"
     "- Khối lọc KHÔNG có ô Công ty / Phòng ban / Bộ phận"),

    ("01", "Quyền xem theo tổng công ty không mở được phiếu của công ty khác", "P0",
     "Tài khoản B chỉ có quyền \"Xem phiếu hàng mượn theo tổng công ty\", thuộc công ty 3; công ty "
     "3 có 90 phiếu, công ty 1 có 250 phiếu",
     "1. Đăng nhập bằng B, mở mục Phiếu Yêu cầu xuất hàng mượn\n"
     "2. Bấm nút Bộ lọc để bung khối tìm kiếm, ghi lại các ô lọc theo đơn vị đang hiện\n"
     "3. Đọc số tổng khi chưa chọn gì\n"
     "4. Chọn Công ty = công ty 1 rồi đọc lại số tổng",
     "Công ty: công ty 1",
     "- Khối lọc hiện CẢ ô Công ty và ô Phòng ban\n"
     "- Khi chưa chọn gì: tổng đúng 90, toàn bộ là phiếu công ty 3\n"
     "- ⚠️ Chọn Công ty = công ty 1 ra 0 dòng, KHÔNG ra 250 phiếu. Hiện trạng: quyền theo tổng "
     "công ty không có tác dụng vì hệ thống luôn khóa theo công ty của người đăng nhập. Ghi nhận "
     "Failed\n"
     "- Kỳ vọng đúng: thấy được phiếu của cả 2 công ty"),

    ("02", "Quyền xem theo công ty thấy đủ phiếu công ty mình", "P0",
     "Tài khoản C chỉ có quyền \"Xem phiếu hàng mượn theo công ty\", thuộc công ty 3; công ty 3 "
     "có 90 phiếu của 8 người khác nhau; C tự lập 5 phiếu",
     "1. Đăng nhập bằng C, mở mục Phiếu Yêu cầu xuất hàng mượn\n"
     "2. Bấm nút Bộ lọc, ghi lại các ô lọc theo đơn vị\n"
     "3. Đọc số tổng và soát cột Người lập qua các trang",
     "Quyền: Xem phiếu hàng mượn theo công ty",
     "- Khối lọc KHÔNG có ô Công ty, chỉ có ô Phòng ban\n"
     "- Tổng đúng 90, gồm phiếu của cả 8 người\n"
     "- Không có phiếu nào của công ty khác"),

    ("03", "Quyền xem theo phòng ban chỉ thấy phòng ban mình quản lý", "P0",
     "Tài khoản D chỉ có quyền \"Xem phiếu hàng mượn theo phòng ban\", được phân công quản lý "
     "đúng 2 phòng ban trong công ty mình; 2 phòng ban đó có 18 phiếu; D tự lập 3 phiếu trong đó",
     "1. Đăng nhập bằng D, mở mục Phiếu Yêu cầu xuất hàng mượn\n"
     "2. Bấm nút Bộ lọc, ghi lại các ô lọc theo đơn vị và các lựa chọn trong ô Phòng ban\n"
     "3. Đọc số tổng, soát danh sách qua tất cả các trang",
     "Quyền: Xem phiếu hàng mượn theo phòng ban",
     "- Khối lọc hiện ô Phòng ban và ô Bộ phận\n"
     "- Ô Phòng ban CHỈ liệt kê 2 phòng ban D được phân công\n"
     "- Tổng đúng 18\n"
     "- Không có phiếu của phòng ban khác trong cùng công ty"),

    ("04", "Có nhiều quyền cùng lúc thì lấy phạm vi rộng nhất", "P1",
     "Tài khoản E có ĐỒNG THỜI quyền \"Xem phiếu hàng mượn theo công ty\" và \"Xem phiếu hàng "
     "mượn theo phòng ban\"; E chỉ quản lý 1 phòng ban có 6 phiếu; công ty của E có 90 phiếu",
     "1. Đăng nhập bằng E, mở mục Phiếu Yêu cầu xuất hàng mượn\n"
     "2. Đọc số tổng\n"
     "3. So với số của tài khoản C ở TC-ROLE-02",
     "Quyền: công ty + phòng ban",
     "- Tổng đúng 90, bằng số của tài khoản chỉ có quyền theo công ty\n"
     "- Không bị thu hẹp về 6 phiếu của phòng ban"),

    ("05", "Kế toán kho vào được màn Yêu cầu xuất hàng mượn", "P0",
     "Tài khoản KT-1 có quyền \"Kế toán kho\", thuộc công ty 3; công ty 3 có 90 phiếu gồm 7 phiếu "
     "Chờ duyệt; công ty 1 có 250 phiếu",
     "1. Đăng nhập bằng KT-1\n"
     "2. Mở menu Kế toán, nhóm Hàng hoá - Dịch vụ - Vận chuyển, khối Mượn hàng\n"
     "3. Bấm mục Yêu cầu xuất hàng mượn\n"
     "4. Đọc số tổng, quan sát bố cục phía trên bảng",
     "Quyền: Kế toán kho",
     "- Mục menu HIỂN THỊ\n"
     "- Vào được màn, thấy đủ 90 phiếu của công ty 3\n"
     "- KHÔNG thấy phiếu nào của công ty 1\n"
     "- Phía trên bảng KHÔNG có nút Bộ lọc, KHÔNG có nút Tạo mới, KHÔNG có nút Xuất excel\n"
     "- Các ô lọc Từ ngày / Đến ngày / Tên hàng / Mã hàng nằm sẵn trên màn, kèm nút Tìm kiếm"),

    ("06", "Không có quyền Kế toán kho vẫn mở được màn Yêu cầu xuất hàng mượn bằng đường dẫn", "P0",
     "Tài khoản NV-A ở TC-ROLE-00, không có quyền \"Kế toán kho\"; NV-A tự lập 12 phiếu; công ty "
     "của NV-A có 90 phiếu",
     "1. Đăng nhập bằng NV-A\n"
     "2. Mở menu Kế toán, nhóm Hàng hoá - Dịch vụ - Vận chuyển, tìm mục Yêu cầu xuất hàng mượn\n"
     "3. Dán thẳng đường dẫn màn đó vào thanh địa chỉ\n"
     "4. Đọc số tổng và soát cột Người lập",
     "Đường dẫn màn Yêu cầu xuất hàng mượn",
     "- Mục menu KHÔNG hiển thị\n"
     "- ⚠️ Dán thẳng đường dẫn: màn hình VẪN MỞ ĐƯỢC, không báo thiếu quyền. Ghi nhận Failed\n"
     "- Giảm nhẹ: bảng chỉ ra 12 phiếu do chính NV-A lập, không lộ phiếu người khác\n"
     "- Kỳ vọng đúng: hệ thống từ chối ngay, báo không có quyền"),

    ("07", "Kế toán kho vào được màn Phiếu yêu cầu xuất hàng mượn chờ duyệt", "P0",
     "Tài khoản KT-1 có quyền \"Kế toán kho\", thuộc công ty 3; công ty 3 có 7 phiếu Chờ duyệt "
     "của 4 người khác nhau; công ty 1 có 20 phiếu Chờ duyệt",
     "1. Đăng nhập bằng KT-1\n"
     "2. Mở menu Chờ duyệt, nhóm Hàng hóa - dịch vụ - vận chuyển, khối Hàng mượn\n"
     "3. Bấm mục Phiếu yêu cầu xuất hàng mượn chờ duyệt\n"
     "4. Đọc số tổng và soát cột Trạng thái",
     "Quyền: Kế toán kho",
     "- Mục menu HIỂN THỊ\n"
     "- Vào được màn, đúng 7 dòng, tất cả đều là Chờ duyệt của công ty 3\n"
     "- KHÔNG thấy 20 phiếu của công ty 1\n"
     "- Mỗi dòng đều có mục Hành động \"Tạo phiếu xuất hàng mượn\""),

    ("08", "Người không có quyền Kế toán kho vẫn xem được toàn bộ phiếu chờ duyệt của công ty", "P0",
     "Tài khoản NV-A không có quyền \"Kế toán kho\" và không có quyền xem theo cấp nào; công ty "
     "của NV-A có 7 phiếu Chờ duyệt của 4 người khác, NV-A không lập phiếu nào trong số đó",
     "1. Đăng nhập bằng NV-A\n"
     "2. Mở menu Chờ duyệt, tìm mục Phiếu yêu cầu xuất hàng mượn chờ duyệt\n"
     "3. Dán thẳng đường dẫn màn chờ duyệt vào thanh địa chỉ\n"
     "4. Đọc số tổng và soát cột Người lập\n"
     "5. Bấm vào một mã phiếu của người khác để mở chi tiết",
     "Đường dẫn màn Phiếu yêu cầu xuất hàng mượn chờ duyệt",
     "- Mục menu KHÔNG hiển thị\n"
     "- ⚠️ Dán thẳng đường dẫn: màn hình MỞ ĐƯỢC và liệt kê đủ 7 phiếu Chờ duyệt của 4 người "
     "khác. LỘ DỮ LIỆU. Ghi nhận Failed\n"
     "- Mở chi tiết một phiếu người khác: hệ thống báo không tìm thấy nội dung (chặn được ở màn "
     "chi tiết, nhưng danh sách đã lộ mã phiếu, người lập, ngày lập)\n"
     "- Kỳ vọng đúng: chặn ngay ở đường dẫn danh sách như mục menu đã chặn"),

    ("09", "Kế toán kho mở được chi tiết phiếu của công ty khác bằng đường dẫn", "P0",
     "Tài khoản KT-1 có quyền \"Kế toán kho\", thuộc công ty 3; lấy đường dẫn chi tiết của 1 phiếu "
     "trạng thái Đã duyệt thuộc công ty 1",
     "1. Đăng nhập bằng KT-1\n"
     "2. Xác nhận màn danh sách không có phiếu nào của công ty 1\n"
     "3. Dán đường dẫn chi tiết phiếu công ty 1 vào thanh địa chỉ",
     "Phiếu Đã duyệt thuộc công ty 1",
     "- ⚠️ Hiện trạng: màn chi tiết MỞ ĐƯỢC đầy đủ, hiện tên hàng hóa, số lượng, đơn giá, thành "
     "tiền, file đính kèm của phiếu công ty khác. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: chỉ cho xem phiếu trong phạm vi công ty của người đăng nhập"),

    ("10", "Người không quyền mở chi tiết phiếu của người khác bị chặn", "P0",
     "Tài khoản NV-A (không quyền xem theo cấp, không quyền Kế toán kho); lấy đường dẫn chi tiết "
     "của 1 phiếu do người khác trong cùng công ty lập, trạng thái Đã duyệt",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dán đường dẫn chi tiết phiếu người khác vào thanh địa chỉ",
     "Phiếu Đã duyệt của người khác",
     "- Hệ thống hiện trang báo không tìm thấy nội dung\n"
     "- Không hiển thị bất kỳ dữ liệu nào của phiếu"),

    ("11", "Mục Tạo phiếu xuất hàng mượn chỉ hiện với Kế toán kho và phiếu Chờ duyệt", "P0",
     "Công ty có sẵn 4 phiếu, mỗi trạng thái 1 phiếu: Đã duyệt, Chờ duyệt, Không duyệt, Đang tạo; "
     "tài khoản KT-1 có quyền Kế toán kho, tài khoản C chỉ có quyền xem theo công ty",
     "1. Đăng nhập bằng KT-1, mở mục Phiếu Yêu cầu xuất hàng mượn\n"
     "2. Bấm biểu tượng bánh răng ở cột Hành động của từng dòng, ghi lại nội dung\n"
     "3. Đăng xuất, đăng nhập bằng C, lặp lại bước 2",
     "4 phiếu 4 trạng thái khác nhau",
     "- Với KT-1: chỉ dòng Chờ duyệt có mục \"Tạo phiếu xuất hàng mượn\"; ba dòng còn lại bung ra "
     "một khung rỗng\n"
     "- Với C: KHÔNG dòng nào có mục nào, kể cả dòng Chờ duyệt\n"
     "- Không dòng nào có mục Sửa, Xóa hay In"),

    ("12", "Nút Không duyệt chỉ hiện với Kế toán kho và phiếu Chờ duyệt", "P0",
     "Dùng lại 4 phiếu ở TC-ROLE-11",
     "1. Đăng nhập bằng KT-1, mở chi tiết lần lượt 4 phiếu, ghi lại các nút cuối màn\n"
     "2. Đăng xuất, đăng nhập bằng C, mở chi tiết phiếu Chờ duyệt",
     "4 phiếu 4 trạng thái khác nhau",
     "- Với KT-1 ở phiếu Chờ duyệt: có đủ 3 nút Không duyệt, Tạo phiếu xuất hàng mượn, Quay lại\n"
     "- Với KT-1 ở 3 phiếu còn lại: chỉ có nút Quay lại\n"
     "- Với C ở phiếu Chờ duyệt: chỉ có nút Quay lại"),

    ("13", "Bỏ qua giao diện gọi thẳng chức năng Không duyệt khi không phải Kế toán kho", "P0",
     "Tài khoản NV-A không có quyền \"Kế toán kho\"; 1 phiếu đang Chờ duyệt trong cùng công ty",
     "1. Đăng nhập bằng NV-A, lấy phiên đăng nhập\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Không duyệt của phiếu đó, gửi kèm một ghi "
     "chú bất kỳ\n"
     "3. Mở lại phiếu bằng tài khoản Kế toán kho, đọc Trạng thái",
     "Ghi chú duyệt: \"test bỏ qua giao diện\"",
     "- Hệ thống từ chối, báo \"Không đủ quyền!\"\n"
     "- Phiếu vẫn ở Chờ duyệt, Ghi chú duyệt vẫn trống\n"
     "- Đây là kết quả ĐÚNG, ghi Passed"),

    ("14", "Bỏ qua giao diện lấy dữ liệu phiếu xuất mượn của người khác", "P0",
     "Tài khoản NV-A; lấy mã của 1 Phiếu yêu cầu xuất hàng loại Xuất mượn, trạng thái Đã hạch "
     "toán, do NGƯỜI KHÁC lập",
     "1. Đăng nhập bằng NV-A, mở màn Tạo phiếu yêu cầu xuất hàng mượn\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng lấy dữ liệu phiếu xuất mượn, truyền mã "
     "phiếu của người khác\n"
     "3. Đọc kết quả trả về",
     "Phiếu xuất mượn của người khác",
     "- Hệ thống từ chối, báo \"Không thể chọn phiếu này\"\n"
     "- Không trả về hàng hóa nào\n"
     "- Đây là kết quả ĐÚNG, ghi Passed"),

    ("15", "Bỏ qua giao diện lập phiếu từ phiếu xuất mượn chưa hạch toán", "P0",
     "Tài khoản NV-A tự lập 1 Phiếu yêu cầu xuất hàng loại Xuất mượn, tình trạng mượn \"Đã mượn\" "
     "nhưng trạng thái mới là \"Chờ duyệt\" (chưa Đã hạch toán), có 1 hàng hóa còn đang mượn 5 cái",
     "1. Đăng nhập bằng NV-A, mở màn Tạo phiếu yêu cầu xuất hàng mượn\n"
     "2. Bấm dấu cộng ở ô Phiếu xuất mượn, tìm mã phiếu đó trong cửa sổ chọn\n"
     "3. Dùng công cụ kiểm thử API gọi thẳng chức năng lấy dữ liệu phiếu xuất mượn với mã đó\n"
     "4. Gọi tiếp chức năng lưu phiếu, truyền mã phiếu nguồn đó kèm 1 dòng số lượng bằng 1 và 1 "
     "file đính kèm dạng pdf\n"
     "5. Mở màn danh sách, tìm phiếu vừa tạo",
     "Phiếu nguồn trạng thái Chờ duyệt, số lượng xuất: 1",
     "- Bước 2: cửa sổ chọn KHÔNG liệt kê phiếu đó (giao diện đã lọc đúng)\n"
     "- ⚠️ Bước 3 và 4: hệ thống VẪN chấp nhận, phiếu được tạo ở trạng thái Chờ duyệt. Kiểm tra "
     "phía hệ thống chỉ xét người lập, không xét trạng thái. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: từ chối, báo \"Có yêu cầu xuất mượn không hợp lệ!\"\n"
     "- Sau khi test xong phải xóa dữ liệu rác ở cơ sở dữ liệu"),

    ("16", "Bỏ qua giao diện lập phiếu từ phiếu xuất hàng không phải loại Xuất mượn", "P1",
     "Tài khoản NV-A tự lập 1 Phiếu yêu cầu xuất hàng loại \"Xuất hàng thường\", trạng thái Đã "
     "hạch toán, còn hàng chưa trả",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng lấy dữ liệu phiếu xuất mượn với mã phiếu "
     "xuất hàng thường đó\n"
     "3. Nếu có dữ liệu trả về, gọi tiếp chức năng lưu phiếu\n"
     "4. Mở màn danh sách, tìm phiếu vừa tạo",
     "Phiếu nguồn loại Xuất hàng thường",
     "- ⚠️ Hiện trạng: hệ thống KHÔNG kiểm tra loại xuất, vẫn trả dữ liệu và vẫn lưu được phiếu. "
     "Ghi nhận Failed\n"
     "- Kỳ vọng đúng: chỉ nhận phiếu loại Xuất mượn\n"
     "- Sau khi test xong phải xóa dữ liệu rác ở cơ sở dữ liệu\n"
     "- Nhóm test này dành cho tester kỹ thuật"),

    ("17", "Bỏ qua giao diện xuất excel danh sách chờ duyệt khi không có quyền", "P1",
     "Tài khoản NV-A không có quyền \"Kế toán kho\"; công ty có 7 phiếu Chờ duyệt của người khác",
     "1. Đăng nhập bằng NV-A\n"
     "2. Dán đường dẫn màn chờ duyệt vào thanh địa chỉ\n"
     "3. Bấm nút Xuất excel trên màn đó\n"
     "4. Mở file tải về",
     "Lối vào: Chờ duyệt",
     "- ⚠️ Hiện trạng: tải được file, trong file có đủ 7 phiếu của người khác kèm Mã phiếu, Người "
     "lập, Ngày lập. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: chặn cùng lúc với đường dẫn danh sách"),

    ("18", "Quyền dùng chung chỉ mở thêm ô lọc chứ không mở thêm dữ liệu", "P1",
     "Tài khoản F CHỈ có quyền dùng chung \"Xem tất cả phiếu\", KHÔNG có quyền nào trong 3 quyền "
     "xem phiếu hàng mượn; F tự lập 4 phiếu; công ty của F có 90 phiếu",
     "1. Đăng nhập bằng F, mở mục Phiếu Yêu cầu xuất hàng mượn\n"
     "2. Bấm nút Bộ lọc, ghi lại các ô lọc theo đơn vị đang hiện\n"
     "3. Đọc số tổng và soát cột Người lập\n"
     "4. Chọn Công ty = công ty của F rồi đọc lại số tổng",
     "Quyền: Xem tất cả phiếu (quyền dùng chung)",
     "- ⚠️ Khối lọc HIỆN ô Công ty và ô Phòng ban dù F không có quyền xem phiếu hàng mượn nào\n"
     "- Nhưng bảng chỉ ra 4 phiếu do chính F lập, KHÔNG phải 90\n"
     "- Chọn Công ty của chính mình cũng vẫn chỉ 4 phiếu\n"
     "- Ghi nhận Failed vì giao diện hứa nhiều hơn dữ liệu thực sự cho xem"),
]

# ============================================================ SECTIONS
SEC_I = [
    ("001", "Vào màn từ mục menu Phiếu Yêu cầu xuất hàng mượn", "P0",
     "Tài khoản C có quyền \"Xem phiếu hàng mượn theo công ty\"; công ty có 90 phiếu",
     "1. Mở menu Khởi tạo\n"
     "2. Vào nhóm Hàng hóa, tìm khối Mượn hàng\n"
     "3. Bấm mục Phiếu Yêu cầu xuất hàng mượn\n"
     "4. Quan sát tiêu đề trang và bảng",
     "—",
     "- Mở đúng màn Danh sách yêu cầu xuất hàng mượn\n"
     "- Bảng nạp dữ liệu, không báo lỗi\n"
     "- Tổng đúng 90 — đây là lối vào \"Tất cả\", phạm vi theo quyền xem"),

    ("002", "Lối vào Phiếu của tôi khác lối vào Tất cả", "P0",
     "Vẫn tài khoản C ở TC_01.001; C tự lập 5 phiếu trong tổng 90 phiếu của công ty",
     "1. Vào màn bằng mục menu, đọc số tổng\n"
     "2. Xóa phần tham số ở cuối đường dẫn trên thanh địa chỉ rồi tải lại trang\n"
     "3. Đọc số tổng, soát cột Người lập",
     "—",
     "- Lối vào menu: tổng 90\n"
     "- Lối vào không kèm tham số: tổng đúng 5, mọi dòng đều do C lập\n"
     "- Cùng một bộ cột, cùng bố cục nút"),

    ("003", "Vào màn Kế toán kho từ mục menu", "P0",
     "Tài khoản KT-1 có quyền \"Kế toán kho\"; công ty có 90 phiếu, không phiếu nào ở Đang tạo",
     "1. Mở menu Kế toán, nhóm Hàng hoá - Dịch vụ - Vận chuyển\n"
     "2. Tìm khối Mượn hàng, bấm mục Yêu cầu xuất hàng mượn\n"
     "3. Quan sát tiêu đề trang, các ô lọc và bảng",
     "—",
     "- Mở đúng màn Danh sách yêu cầu xuất hàng mượn\n"
     "- Tổng đúng 90\n"
     "- Bố cục khác hẳn màn kia: 4 ô lọc Từ ngày / Đến ngày / Tên hàng / Mã hàng nằm sẵn, có nút "
     "Tìm kiếm, KHÔNG có nút Bộ lọc, KHÔNG có nút Tạo mới, KHÔNG có nút Xuất excel"),

    ("004", "Vào màn Chờ duyệt từ mục menu", "P0",
     "Tài khoản KT-1 có quyền \"Kế toán kho\"; công ty có 7 phiếu Chờ duyệt trong tổng 90 phiếu",
     "1. Mở menu Chờ duyệt, nhóm Hàng hóa - dịch vụ - vận chuyển\n"
     "2. Tìm khối Hàng mượn, bấm mục Phiếu yêu cầu xuất hàng mượn chờ duyệt\n"
     "3. Đọc số tổng và soát cột Trạng thái",
     "—",
     "- Tổng đúng 7\n"
     "- Mọi dòng đều mang nhãn Chờ duyệt\n"
     "- ⚠️ Phía trên bảng VẪN có nút Tạo mới và nút Xuất excel dù đây là màn phê duyệt — ghi nhận "
     "đúng hiện trạng, ghi Failed ở mức nhẹ"),

    ("005", "Vào lối vào Trả hàng bằng đường dẫn", "P1",
     "Tài khoản NV-A tự lập 12 phiếu, trong đó 5 phiếu Đã duyệt, 4 Chờ duyệt, 3 Không duyệt",
     "1. Đăng nhập bằng NV-A, mở màn danh sách bằng mục menu\n"
     "2. Sửa tham số trên thanh địa chỉ thành giá trị dành cho việc trả hàng rồi tải lại trang\n"
     "3. Đọc số tổng, soát cột Trạng thái và cột Người lập",
     "Tham số lối vào: trả hàng",
     "- Không có mục menu nào trỏ tới lối vào này\n"
     "- Tổng đúng 5, chỉ gồm phiếu Đã duyệt do chính NV-A lập\n"
     "- Không có phiếu Chờ duyệt hay Không duyệt"),

    ("006", "Sửa tham số lối vào thành giá trị lạ", "P0",
     "Tài khoản C có quyền xem theo công ty; công ty có 90 phiếu, C tự lập 5 phiếu",
     "1. Vào màn bằng mục menu, đọc số tổng\n"
     "2. Sửa tham số trên thanh địa chỉ thành một chuỗi vô nghĩa rồi tải lại trang\n"
     "3. Đọc số tổng và soát cột Người lập",
     "Tham số lối vào: chuỗi vô nghĩa",
     "- Trang mở bình thường, KHÔNG báo lỗi, KHÔNG trắng màn\n"
     "- Hệ thống bỏ qua giá trị lạ và quay về phạm vi mặc định: chỉ 5 phiếu do C lập\n"
     "- KHÔNG lộ thêm phiếu nào ngoài phạm vi"),

    ("007", "Đường dẫn thắng bộ lọc đã lưu của lối vào khác", "P0",
     "Tài khoản C; công ty có 90 phiếu, C tự lập 5 phiếu",
     "1. Vào lối vào Tất cả, gõ một mã phiếu vào ô Mã phiếu, chờ bảng nạp lại\n"
     "2. Chuyển sang lối vào Chờ duyệt bằng cách dán đường dẫn\n"
     "3. Quan sát các ô lọc và phạm vi dữ liệu\n"
     "4. Quay lại lối vào Tất cả bằng mục menu",
     "Mã phiếu: PYCXHM-00317",
     "- Ở lối vào Chờ duyệt: ô Mã phiếu TRỐNG, phạm vi đúng là phiếu Chờ duyệt của công ty\n"
     "- Quay lại lối vào Tất cả: ô Mã phiếu vẫn còn giá trị PYCXHM-00317 đã gõ lúc đầu\n"
     "- Mỗi lối vào ghi nhớ bộ lọc RIÊNG, không lẫn sang nhau"),

    ("008", "Nút làm mới bộ lọc giữ nguyên phạm vi lối vào", "P0",
     "Tài khoản KT-1 đang ở lối vào Chờ duyệt với 7 phiếu",
     "1. Mở lối vào Chờ duyệt, bấm nút Bộ lọc\n"
     "2. Gõ một phần mã phiếu vào ô Mã phiếu, chờ bảng nạp lại, ghi số tổng\n"
     "3. Bấm nút làm mới (biểu tượng vòng xoay màu xanh lá)\n"
     "4. Đọc số tổng và cột Trạng thái",
     "Mã phiếu: 003",
     "- Sau khi làm mới: mọi ô lọc trống, bảng nạp lại\n"
     "- Tổng quay về đúng 7, KHÔNG nhảy lên 90\n"
     "- Mọi dòng vẫn là Chờ duyệt — phạm vi lối vào được giữ nguyên"),

    ("009", "Bố cục mặc định của màn danh sách", "P0",
     "Tài khoản C có quyền xem theo công ty",
     "1. Mở màn Phiếu Yêu cầu xuất hàng mượn\n"
     "2. Quan sát từ trên xuống dưới",
     "—",
     "- Phía trên bảng có 3 nút: Bộ lọc, Tạo mới, Xuất excel\n"
     "- Khối tìm kiếm mặc định ĐANG THU GỌN, bấm nút Bộ lọc mới bung ra\n"
     "- Bảng có đúng 8 cột: STT, Mã phiếu, Người lập, Ngày lập, Trạng thái, Người duyệt, Ngày "
     "duyệt, Hành động\n"
     "- Mặc định 10 dòng mỗi trang, phiếu mới nhất lên đầu"),

    ("010", "Bảng không có cột số tiền", "P1",
     "Một phiếu bất kỳ có 3 hàng hóa, tổng thành tiền 45.000.000",
     "1. Mở màn danh sách, tìm phiếu đó\n"
     "2. Soát các cột của dòng\n"
     "3. Mở chi tiết phiếu, đọc dòng Tổng cộng",
     "—",
     "- Ngoài danh sách KHÔNG có cột nào hiện số tiền\n"
     "- Chỉ trong màn chi tiết mới thấy Đơn giá, Thành tiền và dòng Tổng cộng 45.000.000"),

    ("011", "Bấm mã phiếu mở màn chi tiết", "P0",
     "Một phiếu Đã duyệt mã PYCXHM-00317 do chính mình lập",
     "1. Mở màn danh sách\n"
     "2. Bấm vào mã phiếu PYCXHM-00317",
     "Mã phiếu: PYCXHM-00317",
     "- Mở màn chi tiết, tiêu đề trang là \"Phiếu yêu cầu xuất hàng mượn: PYCXHM-00317\"\n"
     "- Hiện đủ khối Thông tin chung và khối Chi tiết"),

    ("012", "Bấm Tạo mới mở màn lập phiếu", "P0",
     "Tài khoản bất kỳ đã đăng nhập",
     "1. Mở màn Phiếu Yêu cầu xuất hàng mượn\n"
     "2. Bấm nút Tạo mới",
     "—",
     "- Mở màn \"Tạo phiếu yêu cầu xuất hàng mượn\"\n"
     "- Có khối Thông tin chung với 3 mục: Phiếu xuất mượn, Ghi chú, File đính kèm\n"
     "- Có khối Chi tiết với bảng trống, ghi \"Không có hàng hóa\"\n"
     "- Cuối màn có nút Gửi (đang bị khóa) và nút Hủy"),

    ("013", "Bấm Hủy ở màn lập phiếu quay về lối vào Tất cả", "P1",
     "Đang ở màn Tạo phiếu yêu cầu xuất hàng mượn, đã chọn 1 phiếu xuất mượn và nhập ghi chú",
     "1. Bấm nút Hủy\n"
     "2. Quan sát màn hình đích và thanh địa chỉ\n"
     "3. Mở lại màn lập phiếu",
     "—",
     "- Quay về màn danh sách ở lối vào Tất cả\n"
     "- Không có hộp thoại hỏi lại, dữ liệu vừa nhập mất hẳn\n"
     "- Mở lại màn lập phiếu: mọi ô đều trống, không lưu nháp"),

    ("014", "Bấm Quay lại ở màn chi tiết", "P1",
     "Đang mở chi tiết một phiếu, vào từ lối vào Chờ duyệt",
     "1. Bấm nút Quay lại cuối màn chi tiết\n"
     "2. Quan sát màn hình đích",
     "—",
     "- ⚠️ Quay về lối vào \"Tất cả\" chứ KHÔNG quay lại lối vào Chờ duyệt vừa đi ra\n"
     "- Ghi nhận đúng hiện trạng, ghi Failed ở mức nhẹ vì gây mất mạch thao tác duyệt hàng loạt"),
]

SEC_II = [
    ("001", "Lọc theo Mã phiếu khớp một phần", "P0",
     "Công ty có 3 phiếu mã PYCXHM-00317, PYCXHM-00318, PYCXHM-00417",
     "1. Mở màn danh sách, bấm nút Bộ lọc\n"
     "2. Gõ 0031 vào ô Mã phiếu, chờ bảng tự nạp lại\n"
     "3. Đọc số tổng và các mã hiện ra\n"
     "4. Gõ tiếp thành 003170 rồi chờ nạp lại",
     "Mã phiếu: 0031, sau đó 003170",
     "- Gõ 0031: ra đúng 2 dòng PYCXHM-00317 và PYCXHM-00318\n"
     "- Gõ 003170: ra 0 dòng, hiện dòng chữ không có dữ liệu\n"
     "- Không cần bấm nút nào, bảng tự nạp sau khoảng nửa giây"),

    ("002", "Lọc theo Trạng thái từng giá trị", "P0",
     "Công ty có 90 phiếu: 60 Đã duyệt, 7 Chờ duyệt, 23 Không duyệt, 0 Đang tạo",
     "1. Mở màn danh sách, bấm nút Bộ lọc\n"
     "2. Chọn lần lượt từng giá trị trong ô Trạng thái, mỗi lần đọc số tổng\n"
     "3. Bỏ chọn để về trạng thái rỗng",
     "Trạng thái: Đã duyệt / Chờ duyệt / Đang tạo / Không duyệt",
     "- Đã duyệt: 60 dòng, nhãn tô XANH\n"
     "- Chờ duyệt: 7 dòng, nhãn tô ĐỎ\n"
     "- Không duyệt: 23 dòng, nhãn tô ĐỎ\n"
     "- ⚠️ Đang tạo: 0 dòng — ĐÚNG, vì màn này không tạo được phiếu nháp. KHÔNG ghi Failed\n"
     "- Bỏ chọn: quay về 90 dòng"),

    ("003", "Lọc theo Người lập", "P0",
     "Công ty có 90 phiếu, trong đó nhân viên Nguyễn Văn A lập 12 phiếu",
     "1. Mở màn danh sách, bấm nút Bộ lọc\n"
     "2. Bấm ô Người lập, gõ vài ký tự tên để tìm, chọn Nguyễn Văn A\n"
     "3. Đọc số tổng và soát cột Người lập",
     "Người lập: Nguyễn Văn A",
     "- Ô Người lập tìm được cả nhân viên đã nghỉ việc\n"
     "- Ra đúng 12 dòng\n"
     "- Mọi dòng đều có Người lập kết thúc bằng \"Nguyễn Văn A\""),

    ("004", "Lọc theo Người duyệt", "P0",
     "Công ty có 60 phiếu Đã duyệt, trong đó Kế toán kho Trần Thị B xử lý 25 phiếu; 23 phiếu "
     "Không duyệt, Trần Thị B xử lý 8 phiếu trong số đó",
     "1. Mở màn danh sách, bấm nút Bộ lọc\n"
     "2. Chọn Người duyệt là Trần Thị B\n"
     "3. Đọc số tổng và soát cột Trạng thái",
     "Người duyệt: Trần Thị B",
     "- Ra đúng 33 dòng (25 Đã duyệt + 8 Không duyệt)\n"
     "- Ô lọc này KHÔNG phân biệt duyệt hay từ chối, cả hai đều tính là đã xử lý\n"
     "- Không có dòng nào ở trạng thái Chờ duyệt"),

    ("005", "Lọc theo Mã hàng", "P0",
     "Phiếu PYCXHM-00317 có 2 hàng hóa mã SP-A001 và SP-B002; phiếu PYCXHM-00318 chỉ có SP-A001; "
     "trong công ty có 5 phiếu chứa SP-A001",
     "1. Mở màn danh sách, bấm nút Bộ lọc\n"
     "2. Gõ SP-A001 vào ô Mã hàng, chờ bảng nạp lại\n"
     "3. Đọc số tổng\n"
     "4. Gõ SP-A vào ô Mã hàng, đọc lại số tổng",
     "Mã hàng: SP-A001, sau đó SP-A",
     "- Gõ SP-A001: ra đúng 5 dòng, có cả PYCXHM-00317 và PYCXHM-00318\n"
     "- Gõ SP-A: ra số dòng lớn hơn hoặc bằng 5 — ô này khớp một phần chuỗi\n"
     "- Khớp một hàng hóa là cả phiếu hiện ra, không hiện từng dòng hàng hóa riêng"),

    ("006", "Lọc theo Tên hàng", "P0",
     "Trong công ty có 5 phiếu chứa hàng hóa tên \"Máy in laser HP 1020\"",
     "1. Mở màn danh sách, bấm nút Bộ lọc\n"
     "2. Gõ \"máy in\" vào ô Tên hàng, chờ nạp lại\n"
     "3. Mở chi tiết một dòng bất kỳ để đối chiếu",
     "Tên hàng: máy in",
     "- Ra các phiếu có ít nhất một hàng hóa mà tên chứa cụm \"máy in\"\n"
     "- Mở chi tiết: nhìn thấy đúng hàng hóa tên chứa cụm đó trong bảng Chi tiết"),

    ("007", "Điền đồng thời Mã hàng và Tên hàng", "P1",
     "Phiếu PYCXHM-00317 có 2 hàng hóa: SP-A001 tên \"Máy in laser HP 1020\" và SP-B002 tên "
     "\"Mực in HP 12A\"; không phiếu nào khác có cả hai",
     "1. Mở màn danh sách, bấm nút Bộ lọc\n"
     "2. Gõ SP-B002 vào ô Mã hàng và \"máy in\" vào ô Tên hàng\n"
     "3. Đọc kết quả",
     "Mã hàng: SP-B002 · Tên hàng: máy in",
     "- ⚠️ PYCXHM-00317 VẪN hiện ra, dù mã và tên khớp ở HAI hàng hóa khác nhau chứ không phải "
     "cùng một hàng hóa\n"
     "- Đây là hiện trạng thiết kế: hai ô lọc chạy độc lập trên toàn bộ hàng hóa của phiếu. Ghi "
     "nhận là hiện trạng đã biết, không ghi Failed"),

    ("008", "Lọc theo khoảng ngày lập", "P0",
     "Công ty có 4 phiếu lập lần lượt ngày 01/09/2026 lúc 08:15, 05/09/2026 lúc 09:00, "
     "05/09/2026 lúc 23:50 và 06/09/2026 lúc 07:30",
     "1. Mở màn danh sách, bấm nút Bộ lọc\n"
     "2. Điền Từ ngày 01/09/2026, Đến ngày 05/09/2026\n"
     "3. Đọc số tổng và cột Ngày lập",
     "Từ ngày: 01/09/2026 · Đến ngày: 05/09/2026",
     "- Ra đúng 3 dòng: 01/09 08:15, 05/09 09:00 và 05/09 23:50\n"
     "- Phiếu 05/09 lúc 23:50 PHẢI có mặt — trọn ngày cuối được tính\n"
     "- Phiếu 06/09 07:30 KHÔNG có mặt"),

    ("009", "Chỉ điền một đầu mút của khoảng ngày", "P1",
     "Dùng lại 4 phiếu ở TC_02.008",
     "1. Chỉ điền Từ ngày 05/09/2026, để trống Đến ngày, đọc kết quả\n"
     "2. Xóa ô Từ ngày, chỉ điền Đến ngày 05/09/2026, đọc kết quả",
     "Từ ngày: 05/09/2026 · Đến ngày: 05/09/2026",
     "- Chỉ Từ ngày: ra 3 dòng (05/09 09:00, 05/09 23:50, 06/09 07:30)\n"
     "- Chỉ Đến ngày: ra 3 dòng (01/09 08:15, 05/09 09:00, 05/09 23:50)\n"
     "- Không báo lỗi khi bỏ trống một đầu mút"),

    ("010", "Đến ngày kéo theo phiếu lập đúng nửa đêm ngày kế tiếp", "P2",
     "Có 1 phiếu lập ngày 06/09/2026 đúng 00:00:00; các phiếu khác lập trong giờ hành chính",
     "1. Mở màn danh sách, bấm nút Bộ lọc\n"
     "2. Điền Đến ngày 05/09/2026, để trống Từ ngày\n"
     "3. Soát cột Ngày lập tìm phiếu 06/09/2026 00:00",
     "Đến ngày: 05/09/2026",
     "- ⚠️ Phiếu lập 06/09/2026 00:00 VẪN lọt vào kết quả dù đã quá ngày cuối\n"
     "- Ghi nhận Failed ở mức nhẹ, ghi rõ đây là sai số một khoảnh khắc, chỉ ảnh hưởng khi có "
     "phiếu lập đúng nửa đêm"),

    ("011", "Đến ngày trước Từ ngày", "P1",
     "Công ty có 90 phiếu",
     "1. Mở màn danh sách, bấm nút Bộ lọc\n"
     "2. Điền Từ ngày 05/09/2026 và Đến ngày 01/09/2026\n"
     "3. Đọc kết quả",
     "Từ ngày: 05/09/2026 · Đến ngày: 01/09/2026",
     "- Bảng ra 0 dòng, hiện dòng chữ không có dữ liệu\n"
     "- KHÔNG báo lỗi đỏ, KHÔNG treo trang\n"
     "- Hệ thống không tự đảo hai đầu mút"),

    ("012", "Lọc theo Công ty với người có quyền tổng công ty", "P0",
     "Tài khoản B có quyền \"Xem phiếu hàng mượn theo tổng công ty\", thuộc công ty 3; hệ thống "
     "có 3 công ty đều có phiếu",
     "1. Đăng nhập bằng B, mở màn danh sách, bấm nút Bộ lọc\n"
     "2. Bung ô Công ty, ghi lại số lựa chọn\n"
     "3. Chọn lần lượt từng công ty, mỗi lần đọc số tổng",
     "Công ty: lần lượt cả 3 công ty",
     "- Ô Công ty liệt kê đủ cả 3 công ty\n"
     "- Chọn công ty 3 (công ty của B): ra đúng số phiếu công ty 3\n"
     "- ⚠️ Chọn công ty 1 hoặc công ty 2: ra 0 dòng. Ghi nhận Failed — xem mục 9 bẫy số 1"),

    ("013", "Lọc theo Phòng ban", "P0",
     "Tài khoản C có quyền \"Xem phiếu hàng mượn theo công ty\"; phòng Kinh doanh 1 có 30 phiếu, "
     "phòng Kinh doanh 2 có 22 phiếu, tổng công ty 90 phiếu",
     "1. Đăng nhập bằng C, mở màn danh sách, bấm nút Bộ lọc\n"
     "2. Chọn Phòng ban = Kinh doanh 1, đọc số tổng\n"
     "3. Đổi sang Kinh doanh 2, đọc số tổng\n"
     "4. Bỏ chọn, đọc số tổng",
     "Phòng ban: Kinh doanh 1, sau đó Kinh doanh 2",
     "- Kinh doanh 1: đúng 30 dòng\n"
     "- Kinh doanh 2: đúng 22 dòng\n"
     "- Bỏ chọn: quay về 90 dòng\n"
     "- Ô Phòng ban chỉ liệt kê phòng ban trong công ty của C"),

    ("014", "Ô lọc Bộ phận không có tác dụng", "P0",
     "Tài khoản D có quyền \"Xem phiếu hàng mượn theo phòng ban\", quản lý 2 phòng ban với 18 "
     "phiếu; trong đó bộ phận Bán lẻ có 4 phiếu",
     "1. Đăng nhập bằng D, mở màn danh sách, bấm nút Bộ lọc\n"
     "2. Xác nhận có ô Bộ phận\n"
     "3. Chọn Bộ phận = Bán lẻ, chờ bảng nạp lại\n"
     "4. Đọc số tổng",
     "Bộ phận: Bán lẻ",
     "- ⚠️ Hiện trạng: số tổng VẪN là 18, không thu về 4. Chọn bộ phận nào cũng ra kết quả như "
     "nhau. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: ra đúng 4 phiếu thuộc bộ phận Bán lẻ"),

    ("015", "Kết hợp nhiều ô lọc cùng lúc", "P0",
     "Công ty có 90 phiếu; nhân viên Nguyễn Văn A lập 12 phiếu, trong đó 3 phiếu Chờ duyệt và "
     "2 trong 3 phiếu đó lập trong tháng 09/2026",
     "1. Mở màn danh sách, bấm nút Bộ lọc\n"
     "2. Chọn Người lập = Nguyễn Văn A\n"
     "3. Chọn thêm Trạng thái = Chờ duyệt\n"
     "4. Điền thêm Từ ngày 01/09/2026 và Đến ngày 30/09/2026\n"
     "5. Đọc số tổng sau mỗi bước",
     "Người lập: Nguyễn Văn A · Trạng thái: Chờ duyệt · Từ 01/09/2026 đến 30/09/2026",
     "- Sau bước 2: 12 dòng\n"
     "- Sau bước 3: 3 dòng\n"
     "- Sau bước 4: 2 dòng\n"
     "- Các điều kiện cộng dồn theo kiểu VÀ, không thay thế nhau"),

    ("016", "Nút làm mới xóa hết điều kiện lọc", "P0",
     "Đang ở màn danh sách với 5 ô lọc đã điền và đang xem trang 3",
     "1. Điền đủ Mã phiếu, Trạng thái, Người lập, Từ ngày, Đến ngày\n"
     "2. Lật sang trang 3\n"
     "3. Bấm nút làm mới (biểu tượng vòng xoay)\n"
     "4. Quan sát các ô lọc và bảng",
     "—",
     "- Cả 5 ô lọc trống trở lại\n"
     "- Bảng nạp lại toàn bộ phạm vi của lối vào đang mở\n"
     "- Bảng quay về trang 1"),

    ("017", "Bộ lọc được ghi nhớ khi rời màn rồi quay lại", "P0",
     "Đang ở lối vào Tất cả",
     "1. Bấm nút Bộ lọc, chọn Trạng thái = Chờ duyệt và gõ 003 vào ô Mã phiếu\n"
     "2. Lật sang trang 2\n"
     "3. Điền thêm Từ ngày 01/09/2026\n"
     "4. Mở một màn hình khác bất kỳ rồi quay lại bằng mục menu\n"
     "5. Bấm nút Bộ lọc để bung khối tìm kiếm, soát từng ô",
     "Trạng thái: Chờ duyệt · Mã phiếu: 003 · Từ ngày: 01/09/2026",
     "- Ô Trạng thái và ô Mã phiếu GIỮ NGUYÊN giá trị cũ\n"
     "- Bảng mở lại đúng trang 2\n"
     "- ⚠️ Ô Từ ngày TRỐNG — hai ô ngày không được ghi nhớ. Ghi nhận đúng hiện trạng, ghi Failed "
     "ở mức nhẹ vì gây lệch số liệu khi quay lại màn"),

    ("018", "Màn Kế toán kho có bộ ô lọc riêng", "P0",
     "Tài khoản KT-1 có quyền Kế toán kho; công ty có 90 phiếu",
     "1. Mở màn Yêu cầu xuất hàng mượn từ menu Kế toán\n"
     "2. Liệt kê các ô lọc phía trên bảng và các ô lọc trong dòng tiêu đề bảng\n"
     "3. Gõ một mã phiếu vào ô Mã phiếu trong dòng tiêu đề rồi bấm nút Tìm kiếm",
     "Mã phiếu: PYCXHM-00317",
     "- Phía trên bảng có 4 ô: Từ ngày, Đến ngày, Tên hàng, Mã hàng, kèm nút Tìm kiếm\n"
     "- Trong dòng tiêu đề bảng có thêm 3 ô: Mã phiếu, Người lập, Người duyệt, và ô chọn Trạng "
     "thái\n"
     "- KHÔNG có ô Công ty / Phòng ban / Bộ phận dù tài khoản có quyền dùng chung\n"
     "- Tìm theo mã: ra đúng 1 dòng"),
]

SEC_III = [
    ("001", "Sắp xếp mặc định theo ngày lập giảm dần", "P0",
     "Công ty có 90 phiếu lập rải rác nhiều ngày",
     "1. Mở màn danh sách\n"
     "2. Đọc cột Ngày lập của 10 dòng đầu",
     "—",
     "- Phiếu mới nhất nằm dòng đầu\n"
     "- Ngày lập giảm dần từ trên xuống\n"
     "- Không có mũi tên sắp xếp nào đang bật ở tiêu đề cột"),

    ("002", "Sắp xếp theo Mã phiếu", "P1",
     "Công ty có 90 phiếu mã từ PYCXHM-00120 đến PYCXHM-00520",
     "1. Mở màn danh sách\n"
     "2. Bấm tiêu đề cột Mã phiếu, đọc 3 dòng đầu\n"
     "3. Bấm lần nữa, đọc 3 dòng đầu",
     "—",
     "- Lần 1: sắp tăng dần, dòng đầu là PYCXHM-00120\n"
     "- Lần 2: sắp giảm dần, dòng đầu là PYCXHM-00520\n"
     "- Số tổng không đổi qua 2 lần bấm"),

    ("003", "Sắp xếp theo Ngày duyệt với phiếu chưa duyệt", "P1",
     "Công ty có 90 phiếu, trong đó 7 phiếu Chờ duyệt chưa có Ngày duyệt",
     "1. Mở màn danh sách\n"
     "2. Bấm tiêu đề cột Ngày duyệt để sắp tăng dần\n"
     "3. Đọc các dòng đầu và cuối",
     "—",
     "- Bảng sắp xếp được, không báo lỗi\n"
     "- 7 phiếu chưa duyệt dồn về một phía (ô Ngày duyệt trống)\n"
     "- Số tổng vẫn 90"),

    ("004", "Các cột không sắp xếp được", "P1",
     "Công ty có 90 phiếu",
     "1. Mở màn danh sách\n"
     "2. Lần lượt bấm tiêu đề các cột STT, Người lập, Người duyệt, Hành động\n"
     "3. Quan sát thứ tự dòng sau mỗi lần bấm",
     "—",
     "- 4 cột này KHÔNG có mũi tên sắp xếp và bấm vào không đổi thứ tự\n"
     "- Chỉ 4 cột Mã phiếu, Ngày lập, Trạng thái, Ngày duyệt sắp xếp được"),

    ("005", "Đổi số dòng mỗi trang", "P0",
     "Công ty có 90 phiếu",
     "1. Mở màn danh sách, ghi lại ô \"Hiển thị 1 đến 10 trong tổng số 90\"\n"
     "2. Lật sang trang 4\n"
     "3. Đổi số dòng mỗi trang thành 25\n"
     "4. Đọc lại ô thống kê và số trang",
     "Số dòng mỗi trang: 25",
     "- Sau khi đổi: ô thống kê ghi \"Hiển thị 1 đến 25 trong tổng số 90\"\n"
     "- Bảng quay về trang 1, KHÔNG giữ trang 4\n"
     "- Số trang giảm từ 9 xuống 4"),

    ("006", "Số thứ tự đánh liên tục qua các trang", "P0",
     "Công ty có 90 phiếu, đang để 10 dòng mỗi trang",
     "1. Mở màn danh sách, đọc STT dòng đầu và dòng cuối trang 1\n"
     "2. Lật sang trang 2, đọc STT dòng đầu\n"
     "3. Lật sang trang 9, đọc STT dòng cuối",
     "—",
     "- Trang 1: STT từ 1 đến 10\n"
     "- Trang 2: STT bắt đầu từ 11\n"
     "- Trang 9: STT cuối là 90"),

    ("007", "Phân trang giữ nguyên bộ lọc", "P0",
     "Công ty có 90 phiếu, lọc Trạng thái = Đã duyệt ra 60 dòng",
     "1. Mở màn danh sách, chọn Trạng thái = Đã duyệt\n"
     "2. Đọc số tổng, lật sang trang 5\n"
     "3. Soát cột Trạng thái của mọi dòng trang 5",
     "Trạng thái: Đã duyệt",
     "- Ô thống kê ghi tổng số 60 ở mọi trang\n"
     "- Trang 5 vẫn chỉ có phiếu Đã duyệt\n"
     "- Bộ lọc không bị mất khi lật trang"),

    ("008", "Đổi bộ lọc khi đang ở trang cuối", "P1",
     "Công ty có 90 phiếu, đang xem trang 9",
     "1. Lật tới trang 9\n"
     "2. Chọn Trạng thái = Chờ duyệt (chỉ có 7 phiếu, tức 1 trang)\n"
     "3. Quan sát bảng",
     "Trạng thái: Chờ duyệt",
     "- Bảng hiện đúng 7 dòng, không trống\n"
     "- Không kẹt ở trang 9 rỗng\n"
     "- Ô thống kê ghi \"Hiển thị 1 đến 7 trong tổng số 7\""),

    ("009", "Bảng rỗng khi bộ lọc không khớp gì", "P1",
     "Công ty có 90 phiếu",
     "1. Mở màn danh sách, gõ ZZZZZZ vào ô Mã phiếu\n"
     "2. Quan sát bảng và ô thống kê",
     "Mã phiếu: ZZZZZZ",
     "- Bảng hiện dòng chữ báo không có dữ liệu\n"
     "- Ô thống kê ghi tổng số 0\n"
     "- Không báo lỗi đỏ, không treo trang"),

    ("010", "Định dạng cột Người lập và các cột ngày", "P1",
     "Phiếu PYCXHM-00317 do Nguyễn Văn A thuộc phòng ban mã KD1 lập ngày 05/09/2026 lúc 09:00, "
     "được Trần Thị B duyệt ngày 06/09/2026 lúc 14:30",
     "1. Mở màn danh sách, tìm phiếu PYCXHM-00317\n"
     "2. Đọc 4 cột Người lập, Ngày lập, Người duyệt, Ngày duyệt",
     "—",
     "- Người lập hiện \"KD1 - Nguyễn Văn A\" (mã phòng ban rồi tới họ tên)\n"
     "- Ngày lập hiện 05/09/2026 09:00\n"
     "- Người duyệt hiện \"Trần Thị B\", không có mã phòng ban\n"
     "- Ngày duyệt hiện 06/09/2026 14:30"),
]

SEC_IV = [
    ("001", "Lập phiếu đủ thông tin với một phiếu xuất mượn", "P0",
     "Tài khoản NV-A tự lập 1 Phiếu yêu cầu xuất hàng loại Xuất mượn mã PYCXH-00901, trạng thái "
     "Đã hạch toán, tình trạng Đã mượn, có 1 hàng hóa SP-A001 đã xuất 10 cái, đã trả 0 cái; sẵn "
     "1 file pdf trên máy",
     "1. Mở màn Tạo phiếu yêu cầu xuất hàng mượn\n"
     "2. Bấm dấu cộng ở ô Phiếu xuất mượn, tìm và chọn PYCXH-00901\n"
     "3. Nhập Ghi chú \"Khách đề nghị mượn thêm\"\n"
     "4. Bấm dấu cộng ở mục File đính kèm, chọn file pdf\n"
     "5. Nhập 3 vào ô Xuất của dòng SP-A001\n"
     "6. Bấm nút Gửi",
     "Phiếu xuất mượn: PYCXH-00901 · Ghi chú: Khách đề nghị mượn thêm · Xuất: 3 · File: 1 file pdf",
     "- Sau bước 2: bảng Chi tiết tự nạp hàng hóa SP-A001, cột Đang mượn hiện 10\n"
     "- Sau bước 5: cột Số lượng xuất hiện 3, Thành tiền = Đơn giá × 3, dòng Tổng cộng cập nhật\n"
     "- Nút Gửi chuyển từ khóa sang bấm được ngay khi có số lượng lớn hơn 0\n"
     "- Sau bước 6: hiện thông báo xanh \"Yêu cầu của bạn đã được gửi\", chuyển về màn danh sách "
     "lối vào Tất cả\n"
     "- Phiếu mới nằm dòng đầu, trạng thái Chờ duyệt, mã dạng PYCXHM- kèm 5 chữ số"),

    ("002", "Lập phiếu gộp nhiều phiếu xuất mượn", "P0",
     "Tài khoản NV-A có 2 phiếu xuất mượn PYCXH-00901 và PYCXH-00902, cả hai đều Đã hạch toán và "
     "Đã mượn, cùng chứa hàng hóa SP-A001 (còn mượn lần lượt 10 và 6 cái)",
     "1. Mở màn Tạo phiếu, chọn PYCXH-00901\n"
     "2. Bấm dấu cộng lần nữa, chọn thêm PYCXH-00902\n"
     "3. Quan sát bảng Chi tiết\n"
     "4. Nhập Xuất = 2 ở dòng PYCXH-00901 và Xuất = 4 ở dòng PYCXH-00902\n"
     "5. Nhập Ghi chú, đính kèm 1 file pdf, bấm Gửi\n"
     "6. Mở chi tiết phiếu vừa tạo",
     "Xuất: 2 và 4",
     "- Sau bước 2: ô Phiếu xuất mượn hiện 2 thẻ mã phiếu\n"
     "- Bảng Chi tiết chỉ có 1 hàng hóa SP-A001 nhưng có 2 dòng con, mỗi dòng một mã phiếu mượn\n"
     "- Sau bước 4: cột Số lượng xuất của SP-A001 hiện 6 (bằng 2 + 4)\n"
     "- Màn chi tiết sau khi lưu: giữ đúng 2 dòng con với số 2 và 4"),

    ("003", "Bỏ một phiếu xuất mượn khỏi phiếu đang lập", "P0",
     "Đang lập phiếu, đã chọn PYCXH-00901 và PYCXH-00902, đã nhập Xuất = 2 và 4 như TC_04.002",
     "1. Bấm dấu nhân trên thẻ PYCXH-00902 để bỏ phiếu này ra\n"
     "2. Quan sát bảng Chi tiết\n"
     "3. Chọn lại PYCXH-00902\n"
     "4. Quan sát lại số đã nhập",
     "—",
     "- Sau bước 1: thẻ PYCXH-00902 biến mất, dòng con tương ứng biến mất, Số lượng xuất của "
     "SP-A001 còn 2\n"
     "- Sau bước 3: dòng con quay lại VÀ số 4 đã nhập trước đó ĐƯỢC GIỮ NGUYÊN\n"
     "- Số lượng xuất trở lại 6"),

    ("004", "Không cho chọn trùng một phiếu xuất mượn", "P0",
     "Đang lập phiếu, đã chọn PYCXH-00901",
     "1. Bấm dấu cộng ở ô Phiếu xuất mượn\n"
     "2. Chọn lại PYCXH-00901",
     "Phiếu xuất mượn: PYCXH-00901 (lần 2)",
     "- Hiện hộp thoại đỏ tiêu đề \"Không thể chọn yêu cầu này!\" kèm dòng \"Nguyên nhân: Yêu cầu "
     "đã được chọn.\"\n"
     "- Ô Phiếu xuất mượn vẫn chỉ có 1 thẻ\n"
     "- Bảng Chi tiết không đổi"),

    ("005", "Cửa sổ chọn phiếu xuất mượn chỉ có phiếu của chính mình", "P0",
     "Trong công ty có 20 phiếu xuất mượn Đã hạch toán và Đã mượn, trong đó NV-A lập 4 phiếu, "
     "16 phiếu còn lại của người khác",
     "1. Đăng nhập bằng NV-A, mở màn Tạo phiếu\n"
     "2. Bấm dấu cộng ở ô Phiếu xuất mượn\n"
     "3. Đọc số tổng trong cửa sổ và soát cột Người tạo\n"
     "4. Gõ mã của một phiếu người khác vào ô Mã phiếu trong cửa sổ",
     "Mã phiếu của người khác",
     "- Cửa sổ tiêu đề \"Phiếu yêu cầu xuất hàng\", có 4 cột STT, Mã phiếu, Người tạo, Ngày tạo\n"
     "- Tổng đúng 4, mọi dòng đều có Người tạo là NV-A\n"
     "- Tìm mã phiếu người khác: ra 0 dòng\n"
     "- ⚠️ Không thấy phiếu thường là do phiếu đó của người khác, KHÔNG phải lỗi"),

    ("006", "Cửa sổ chọn không có phiếu chưa hạch toán hoặc chưa mượn", "P0",
     "NV-A có 4 phiếu xuất mượn: 1 phiếu Đã hạch toán + Đã mượn, 1 phiếu Chờ duyệt + Đã mượn, "
     "1 phiếu Đã hạch toán + Chờ mượn, 1 phiếu loại Xuất hàng thường Đã hạch toán",
     "1. Mở màn Tạo phiếu, bấm dấu cộng ở ô Phiếu xuất mượn\n"
     "2. Đọc số tổng và các mã hiện ra",
     "—",
     "- Cửa sổ chỉ liệt kê đúng 1 phiếu: loại Xuất mượn, Đã hạch toán, Đã mượn\n"
     "- Ba phiếu còn lại không xuất hiện"),

    ("007", "Chọn phiếu xuất mượn đã trả hết hàng", "P1",
     "NV-A có phiếu xuất mượn PYCXH-00903 Đã hạch toán, Đã mượn, nhưng cả 2 hàng hóa đã được trả "
     "hết (số đã trả bằng số đã xuất)",
     "1. Mở màn Tạo phiếu, bấm dấu cộng, chọn PYCXH-00903\n"
     "2. Quan sát ô Phiếu xuất mượn và bảng Chi tiết\n"
     "3. Quan sát nút Gửi",
     "Phiếu xuất mượn: PYCXH-00903",
     "- Thẻ mã phiếu ĐƯỢC thêm vào ô Phiếu xuất mượn\n"
     "- Bảng Chi tiết vẫn trống, hiện dòng \"Không có hàng hóa\"\n"
     "- Nút Gửi vẫn bị khóa"),

    ("008", "Thêm hàng hóa bằng nút dấu cộng trên bảng Chi tiết", "P1",
     "Đang lập phiếu, đã chọn PYCXH-00901 chứa SP-A001; hàng hóa SP-C003 KHÔNG nằm trong phiếu đó",
     "1. Bấm nút dấu cộng ở góc phải tiêu đề bảng Chi tiết\n"
     "2. Tìm và chọn hàng hóa SP-C003\n"
     "3. Quan sát dòng mới thêm",
     "Hàng hóa: SP-C003",
     "- Hiện thông báo \"Thêm thành công\"\n"
     "- Dòng SP-C003 được thêm nhưng bị làm mờ, ba cột Chi tiết gộp lại ghi \"Chưa có phiếu mượn\"\n"
     "- Không nhập được số lượng cho dòng này\n"
     "- Dòng này không tính vào Tổng cộng"),

    ("009", "Không cho thêm trùng hàng hóa", "P1",
     "Đang lập phiếu, bảng Chi tiết đã có SP-A001",
     "1. Bấm nút dấu cộng ở tiêu đề bảng Chi tiết\n"
     "2. Chọn lại SP-A001",
     "Hàng hóa: SP-A001 (lần 2)",
     "- Hiện thông báo vàng \"Hàng hóa đã tồn tại\"\n"
     "- Bảng Chi tiết không thêm dòng mới"),

    ("010", "Bỏ một hàng hóa khỏi bảng Chi tiết", "P1",
     "Đang lập phiếu với 2 hàng hóa SP-A001 (đã nhập Xuất = 3) và SP-B002 (đã nhập Xuất = 2)",
     "1. Đọc dòng Tổng cộng\n"
     "2. Bấm nút dấu trừ ở cuối dòng SP-A001\n"
     "3. Đọc lại dòng Tổng cộng và nút Gửi",
     "—",
     "- Dòng SP-A001 cùng các dòng con biến mất ngay, không hỏi lại\n"
     "- Tổng cộng giảm đúng phần Thành tiền của SP-A001\n"
     "- Nút Gửi vẫn bấm được vì SP-B002 còn số lượng lớn hơn 0"),

    ("011", "Đơn giá lấy theo bảng giá của đơn vị tính đang chọn", "P0",
     "Hàng hóa SP-A001 có 2 đơn vị tính: Cái (hệ số 1, giá bán 500.000) và Hộp (hệ số 10, giá bán "
     "4.800.000); phiếu mượn PYCXH-00901 đã xuất 25 Cái, chưa trả cái nào",
     "1. Mở màn Tạo phiếu, chọn PYCXH-00901\n"
     "2. Đọc Đơn vị tính, Đơn giá và cột Đang mượn của SP-A001\n"
     "3. Đổi Đơn vị tính sang Hộp\n"
     "4. Đọc lại Đơn giá và cột Đang mượn",
     "Đơn vị tính: Cái, sau đó Hộp",
     "- Với Cái: Đơn giá 500.000, Đang mượn 25\n"
     "- Với Hộp: Đơn giá 4.800.000, Đang mượn 2 (25 chia 10 rồi làm tròn xuống)\n"
     "- Ô chọn đơn vị hiện thêm hệ số quy đổi bên cạnh tên, dạng \"Hộp (x10)\""),

    ("012", "Đổi đơn vị tính không xóa số lượng đã nhập", "P0",
     "Dùng lại dữ liệu TC_04.011; đang chọn đơn vị Cái và đã nhập Xuất = 20",
     "1. Xác nhận dòng đang hợp lệ, Số lượng xuất hiện 20\n"
     "2. Đổi Đơn vị tính sang Hộp\n"
     "3. Quan sát dòng và nút Gửi",
     "Xuất: 20 · Đơn vị: Cái đổi sang Hộp",
     "- ⚠️ Số 20 ở ô Xuất KHÔNG bị xóa, trong khi cột Đang mượn tụt xuống 2\n"
     "- Dòng chuyển sang màu báo lỗi, nút Gửi bị khóa lại\n"
     "- Ghi nhận là bẫy đã biết: phải rà lại toàn bộ số lượng sau mỗi lần đổi đơn vị"),

    ("013", "Cột Đang mượn đã trừ phần đang chờ xử lý", "P0",
     "Phiếu mượn PYCXH-00901 có SP-A001 đã xuất 10 cái, chưa trả; NV-A đã lập sẵn 1 phiếu yêu cầu "
     "xuất hàng mượn khác đang Chờ duyệt xin 4 cái từ chính PYCXH-00901",
     "1. Mở màn Tạo phiếu mới, chọn PYCXH-00901\n"
     "2. Đọc cột Đang mượn của SP-A001\n"
     "3. Nhập Xuất = 7, quan sát dòng\n"
     "4. Sửa thành 6, quan sát lại",
     "Xuất: 7, sau đó 6",
     "- Cột Đang mượn hiện 6 chứ không phải 10 — đã trừ 4 cái đang bị phiếu Chờ duyệt giữ chỗ\n"
     "- Nhập 7: dòng chuyển màu báo lỗi, nút Gửi bị khóa\n"
     "- Nhập 6: dòng trở lại bình thường, nút Gửi bấm được"),

    ("014", "Thành tiền và Tổng cộng tính đúng", "P0",
     "Đang lập phiếu với SP-A001 đơn giá 500.000 và SP-B002 đơn giá 120.000",
     "1. Nhập Xuất = 3 cho SP-A001 và Xuất = 5 cho SP-B002\n"
     "2. Đọc cột Thành tiền của từng dòng và dòng Tổng cộng\n"
     "3. Sửa SP-A001 thành 4, đọc lại",
     "Xuất: 3 và 5, sau đó 4 và 5",
     "- SP-A001: Thành tiền 1.500.000 · SP-B002: Thành tiền 600.000 · Tổng cộng 2.100.000\n"
     "- Sau khi sửa: SP-A001 thành 2.000.000, Tổng cộng 2.600.000\n"
     "- Số cập nhật ngay khi gõ, không phải bấm nút nào"),

    ("015", "Một hàng hóa chia số lượng cho nhiều phiếu mượn", "P0",
     "Hàng hóa SP-A001 nằm trong cả PYCXH-00901 (đang mượn 10) và PYCXH-00902 (đang mượn 6); đơn "
     "giá 500.000",
     "1. Mở màn Tạo phiếu, chọn cả 2 phiếu mượn\n"
     "2. Nhập Xuất = 8 ở dòng PYCXH-00901 và Xuất = 5 ở dòng PYCXH-00902\n"
     "3. Đọc cột Số lượng xuất và Thành tiền của SP-A001\n"
     "4. Gửi phiếu, mở lại chi tiết",
     "Xuất: 8 và 5",
     "- Số lượng xuất hiện 13\n"
     "- Thành tiền 6.500.000\n"
     "- Màn chi tiết giữ đúng 2 dòng con 8 và 5, không gộp thành một dòng 13"),

    ("016", "Xem chi tiết phiếu Chờ duyệt", "P0",
     "Phiếu PYCXHM-00317 trạng thái Chờ duyệt, 2 hàng hóa, 1 file đính kèm, ghi chú \"Khách đề "
     "nghị mượn thêm\"",
     "1. Mở màn danh sách, bấm mã phiếu PYCXHM-00317\n"
     "2. Soát khối Thông tin chung\n"
     "3. Soát bảng Chi tiết\n"
     "4. Kéo xuống cuối màn",
     "—",
     "- Tiêu đề trang là \"Phiếu yêu cầu xuất hàng mượn: PYCXHM-00317\"\n"
     "- Thông tin chung có: thẻ mã Phiếu xuất mượn, ô Ghi chú (khóa, không sửa được), ô Phòng ban "
     "yêu cầu, mục File đính kèm\n"
     "- Góc phải khối Thông tin chung ghi tên người lập và ngày lập\n"
     "- Bảng Chi tiết có cột Số lượng và 3 cột con Phiếu mượn / Xuất / Được duyệt\n"
     "- Cột Được duyệt hiện 0 vì phiếu chưa duyệt\n"
     "- KHÔNG có khối Ghi chú duyệt"),

    ("017", "Xem chi tiết phiếu Đã duyệt", "P0",
     "Phiếu PYCXHM-00318 Đã duyệt, xin xuất 6 cái nhưng Kế toán kho chỉ duyệt 4 cái",
     "1. Mở chi tiết PYCXHM-00318\n"
     "2. Đọc cột Xuất và cột Được duyệt của từng dòng con\n"
     "3. Kéo xuống cuối màn",
     "—",
     "- Cột Xuất hiện 6, cột Được duyệt hiện 4 — hai số khác nhau là ĐÚNG\n"
     "- Cột Số lượng ở dòng hàng hóa vẫn là 6 (số đã xin), không đổi theo số được duyệt\n"
     "- Cuối màn chỉ có nút Quay lại"),

    ("018", "Xem chi tiết phiếu Không duyệt", "P0",
     "Phiếu PYCXHM-00319 trạng thái Không duyệt, Ghi chú duyệt \"Khách còn nợ quá hạn\"",
     "1. Mở chi tiết PYCXHM-00319\n"
     "2. Kéo xuống dưới bảng Chi tiết",
     "—",
     "- Có thêm khối \"Ghi chú duyệt\" hiện đúng nội dung \"Khách còn nợ quá hạn\"\n"
     "- Ô ghi chú duyệt bị khóa, không sửa được\n"
     "- Cột Được duyệt của mọi dòng đều là 0"),

    ("019", "Mở file đính kèm ở màn chi tiết", "P1",
     "Phiếu PYCXHM-00317 có 2 file đính kèm dạng pdf tên \"cam-ket-muon.pdf\" và \"bien-ban.pdf\"",
     "1. Mở chi tiết PYCXHM-00317\n"
     "2. Quan sát mục File đính kèm\n"
     "3. Bấm vào biểu tượng file thứ nhất",
     "—",
     "- Hiện đúng 2 biểu tượng file kèm tên đầy đủ bên dưới\n"
     "- Bấm vào: mở file pdf ở tab mới, đọc được nội dung\n"
     "- Ở màn chi tiết KHÔNG có nút thêm hay xóa file"),

    ("020", "Bấm mã phiếu mượn ở màn chi tiết", "P1",
     "Phiếu PYCXHM-00317 sinh từ phiếu mượn PYCXH-00901",
     "1. Mở chi tiết PYCXHM-00317\n"
     "2. Bấm thẻ mã PYCXH-00901 ở ô Phiếu xuất mượn\n"
     "3. Quay lại, bấm mã PYCXH-00901 ở cột Phiếu mượn trong bảng Chi tiết",
     "—",
     "- Cả hai chỗ đều mở màn chi tiết Phiếu yêu cầu xuất hàng PYCXH-00901 ở tab mới\n"
     "- Không mất dữ liệu ở màn đang xem"),

    ("021", "Người lập và ngày lập hiện sẵn khi lập phiếu mới", "P2",
     "Tài khoản NV-A đăng nhập ngày 07/09/2026",
     "1. Mở màn Tạo phiếu yêu cầu xuất hàng mượn\n"
     "2. Đọc góc phải khối Thông tin chung",
     "—",
     "- Hiện tên NV-A và ngày 07/09/2026\n"
     "- Hai thông tin này chỉ để xem, không sửa được"),

    ("022", "Thông báo tới Kế toán kho sau khi gửi phiếu", "P1",
     "Tài khoản NV-A thuộc công ty 3; công ty 3 có 2 tài khoản mang quyền \"Kế toán kho\"; công "
     "ty 1 cũng có 1 tài khoản mang quyền đó",
     "1. Đăng nhập bằng NV-A, lập và gửi 1 phiếu\n"
     "2. Đăng nhập lần lượt 2 tài khoản Kế toán kho công ty 3, mở chuông thông báo\n"
     "3. Đăng nhập tài khoản Kế toán kho công ty 1, mở chuông thông báo\n"
     "4. Bấm vào thông báo",
     "—",
     "- Hai tài khoản công ty 3 đều nhận thông báo nội dung \"<tên NV-A> vừa tạo yêu cầu xuất "
     "hàng mượn: <mã phiếu>\"\n"
     "- Tài khoản công ty 1 KHÔNG nhận được — thông báo chỉ gửi trong cùng công ty\n"
     "- Bấm vào thông báo mở đúng màn chi tiết phiếu"),
]

SEC_V = [
    ("001", "Kế toán kho từ chối phiếu", "P0",
     "Tài khoản KT-1 có quyền Kế toán kho; phiếu PYCXHM-00317 đang Chờ duyệt do NV-A lập",
     "1. Đăng nhập KT-1, mở chi tiết PYCXHM-00317\n"
     "2. Bấm nút Không duyệt\n"
     "3. Nhập \"Khách còn nợ quá hạn\" vào ô Ghi chú duyệt\n"
     "4. Bấm nút Xác nhận\n"
     "5. Quan sát màn hình đích, mở lại phiếu",
     "Ghi chú duyệt: Khách còn nợ quá hạn",
     "- Bước 2 mở hộp thoại \"Ghi chú duyệt\" có ô nhập, nút Xác nhận và nút Hủy\n"
     "- Sau bước 4: thông báo xanh \"Thao tác thành công!\", chuyển sang màn Yêu cầu xuất hàng mượn\n"
     "- Phiếu chuyển sang Không duyệt, cột Người duyệt là KT-1, Ngày duyệt là thời điểm vừa bấm\n"
     "- Mở lại phiếu: có khối Ghi chú duyệt với đúng nội dung đã nhập"),

    ("002", "Bắt buộc nhập Ghi chú duyệt khi từ chối", "P0",
     "Phiếu PYCXHM-00320 đang Chờ duyệt; tài khoản KT-1",
     "1. Mở chi tiết PYCXHM-00320, bấm Không duyệt\n"
     "2. Để trống ô Ghi chú duyệt, bấm Xác nhận\n"
     "3. Quan sát hộp thoại\n"
     "4. Nhập 1 khoảng trắng rồi bấm Xác nhận",
     "Ghi chú duyệt: để trống, sau đó 1 khoảng trắng",
     "- Hiện thông báo vàng \"Thao tác thất bại!\" và dòng chữ đỏ \"Bắt buộc phải nhập\" ngay "
     "dưới ô nhập\n"
     "- Hộp thoại KHÔNG đóng, phiếu vẫn ở Chờ duyệt\n"
     "- Nhập 1 khoảng trắng: vẫn bị chặn với cùng thông báo"),

    ("003", "Ghi chú duyệt vượt quá độ dài cho phép", "P1",
     "Phiếu PYCXHM-00320 đang Chờ duyệt; tài khoản KT-1",
     "1. Mở chi tiết, bấm Không duyệt\n"
     "2. Dán một đoạn văn bản dài 256 ký tự vào ô Ghi chú duyệt, bấm Xác nhận\n"
     "3. Xóa bớt còn đúng 255 ký tự, bấm Xác nhận",
     "Ghi chú duyệt: 256 ký tự, sau đó 255 ký tự",
     "- Với 256 ký tự: báo đỏ \"Không được vượt quá 255 ký tự\", hộp thoại không đóng\n"
     "- Với 255 ký tự: lưu thành công, phiếu chuyển Không duyệt\n"
     "- Mở lại phiếu: khối Ghi chú duyệt hiện đủ 255 ký tự, không bị cắt"),

    ("004", "Bấm Hủy trong hộp thoại từ chối", "P1",
     "Phiếu PYCXHM-00320 đang Chờ duyệt; tài khoản KT-1",
     "1. Mở chi tiết, bấm Không duyệt\n"
     "2. Nhập \"thử\" vào ô Ghi chú duyệt\n"
     "3. Bấm nút Hủy trong hộp thoại\n"
     "4. Tải lại trang, đọc Trạng thái",
     "Ghi chú duyệt: thử",
     "- Hộp thoại đóng lại, không có thông báo nào\n"
     "- Phiếu vẫn ở Chờ duyệt, không có Người duyệt, không có Ghi chú duyệt"),

    ("005", "Kế toán kho chuyển sang lập Phiếu xuất hàng mượn", "P0",
     "Phiếu PYCXHM-00321 Chờ duyệt, xin xuất 6 cái SP-A001; tài khoản KT-1 có quyền Kế toán kho",
     "1. Đăng nhập KT-1, mở chi tiết PYCXHM-00321\n"
     "2. Bấm nút \"Tạo phiếu xuất hàng mượn\"\n"
     "3. Quan sát màn hình vừa mở",
     "—",
     "- Mở màn lập Phiếu xuất hàng mượn\n"
     "- Bảng chi tiết đã nạp sẵn hàng hóa SP-A001 với số lượng đề nghị 6\n"
     "- Mã phiếu nguồn PYCXHM-00321 hiện ở khối thông tin chung"),

    ("006", "Phiếu chỉ chuyển Đã duyệt khi lưu xong Phiếu xuất hàng mượn", "P0",
     "Phiếu PYCXHM-00321 Chờ duyệt; tài khoản KT-1",
     "1. Mở chi tiết PYCXHM-00321, bấm Tạo phiếu xuất hàng mượn\n"
     "2. KHÔNG lưu, bấm quay lại hoặc đóng tab\n"
     "3. Mở lại PYCXHM-00321, đọc Trạng thái\n"
     "4. Lặp lại bước 1, lần này nhập đủ và lưu Phiếu xuất hàng mượn\n"
     "5. Mở lại PYCXHM-00321",
     "—",
     "- Sau bước 3: phiếu VẪN ở Chờ duyệt, chưa có Người duyệt — ĐÚNG, không ghi Failed\n"
     "- Sau bước 5: phiếu chuyển Đã duyệt, Người duyệt là KT-1, Ngày duyệt là thời điểm lưu\n"
     "- Cột Được duyệt trong bảng Chi tiết hiện đúng số Kế toán kho đã nhập"),

    ("007", "Duyệt ít hơn số đề nghị", "P0",
     "Phiếu PYCXHM-00322 Chờ duyệt, xin xuất 6 cái SP-A001",
     "1. Đăng nhập KT-1, mở chi tiết, bấm Tạo phiếu xuất hàng mượn\n"
     "2. Sửa số lượng từ 6 xuống 4, lưu phiếu\n"
     "3. Mở lại PYCXHM-00322, đọc bảng Chi tiết",
     "Số lượng duyệt: 4",
     "- Phiếu chuyển Đã duyệt\n"
     "- Cột Xuất vẫn hiện 6, cột Được duyệt hiện 4\n"
     "- Cột Số lượng ở dòng hàng hóa vẫn là 6"),

    ("008", "Người lập nhận thông báo khi phiếu bị từ chối", "P1",
     "NV-A vừa gửi phiếu PYCXHM-00323; KT-1 sẽ từ chối phiếu này",
     "1. Đăng nhập KT-1, mở chi tiết PYCXHM-00323, bấm Không duyệt, nhập ghi chú và Xác nhận\n"
     "2. Đăng nhập bằng NV-A, mở chuông thông báo\n"
     "3. Bấm vào thông báo",
     "Ghi chú duyệt: Khách còn nợ quá hạn",
     "- NV-A nhận thông báo nội dung \"<tên KT-1> vừa từ chối yêu cầu xuất hàng mượn: "
     "PYCXHM-00323\"\n"
     "- Bấm vào thông báo mở đúng màn chi tiết phiếu đó\n"
     "- Chỉ người lập nhận, người khác không nhận"),

    ("009", "Phiếu đã xử lý không xử lý lại được", "P0",
     "Phiếu PYCXHM-00317 đã ở trạng thái Không duyệt; phiếu PYCXHM-00318 đã Đã duyệt",
     "1. Đăng nhập KT-1, mở chi tiết PYCXHM-00317, quan sát cuối màn\n"
     "2. Mở chi tiết PYCXHM-00318, quan sát cuối màn\n"
     "3. Mở màn Chờ duyệt, tìm 2 mã phiếu này",
     "—",
     "- Cả 2 phiếu chỉ còn nút Quay lại, KHÔNG có nút Không duyệt, KHÔNG có nút Tạo phiếu xuất "
     "hàng mượn\n"
     "- Màn Chờ duyệt không liệt kê 2 phiếu này"),

    ("010", "Cửa sổ chọn phiếu ở màn lập Phiếu xuất hàng mượn", "P1",
     "Tài khoản KT-1; công ty có 7 phiếu Chờ duyệt và 60 phiếu Đã duyệt",
     "1. Đăng nhập KT-1, mở màn lập Phiếu xuất hàng mượn từ menu\n"
     "2. Bấm nút chọn Phiếu yêu cầu xuất hàng mượn\n"
     "3. Đọc số tổng trong cửa sổ và soát cột Trạng thái\n"
     "4. Chọn một phiếu",
     "—",
     "- Cửa sổ tiêu đề \"Phiếu yêu cầu xuất hàng mượn\", có 4 cột STT, Mã phiếu, Người tạo, Ngày "
     "tạo\n"
     "- Chỉ liệt kê 7 phiếu Chờ duyệt của công ty, không có phiếu Đã duyệt\n"
     "- Chọn xong: bảng chi tiết nạp đúng hàng hóa và số lượng của phiếu đó"),
]

SEC_VI = [
    ("001", "Màn hình không có chức năng Sửa", "P0",
     "Công ty có sẵn phiếu ở cả 3 trạng thái Chờ duyệt, Đã duyệt, Không duyệt; tài khoản NV-A là "
     "người lập các phiếu đó",
     "1. Đăng nhập NV-A, mở màn danh sách\n"
     "2. Bấm biểu tượng bánh răng ở cột Hành động của từng dòng\n"
     "3. Mở chi tiết từng phiếu, soát toàn màn\n"
     "4. Thử đổi nội dung ô Ghi chú ở màn chi tiết",
     "—",
     "- Không dòng nào có mục Sửa\n"
     "- Màn chi tiết không có nút Sửa và không có nút Lưu\n"
     "- Ô Ghi chú ở màn chi tiết bị khóa, gõ không vào\n"
     "- Lập sai thì phải nhờ Kế toán kho từ chối rồi lập phiếu mới"),

    ("002", "Màn hình không có chức năng Xóa", "P0",
     "Dùng lại dữ liệu TC_06.001",
     "1. Đăng nhập NV-A, mở màn danh sách\n"
     "2. Bấm biểu tượng bánh răng ở cột Hành động của từng dòng\n"
     "3. Mở chi tiết từng phiếu, soát toàn màn",
     "—",
     "- Không dòng nào có mục Xóa\n"
     "- Màn chi tiết không có nút Xóa\n"
     "- Không có hộp thoại xác nhận xóa nào trên màn"),

    ("003", "Bỏ qua giao diện gọi thẳng chức năng Sửa và Xóa", "P1",
     "Tài khoản NV-A; 1 phiếu Chờ duyệt do chính NV-A lập",
     "1. Đăng nhập NV-A, lấy phiên đăng nhập\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Sửa phiếu theo mã phiếu đó\n"
     "3. Gọi tiếp chức năng Xóa phiếu\n"
     "4. Mở lại màn danh sách, tìm phiếu",
     "—",
     "- Cả 2 lần đều bị hệ thống từ chối vì không tồn tại chức năng tương ứng\n"
     "- Phiếu còn nguyên, trạng thái không đổi\n"
     "- Đây là kết quả ĐÚNG, ghi Passed"),
]

SEC_VII = [
    ("001", "Xuất excel danh sách không kèm bộ lọc", "P0",
     "Tài khoản C có quyền xem theo công ty; công ty có 90 phiếu",
     "1. Mở màn danh sách bằng mục menu\n"
     "2. Bấm nút Xuất excel\n"
     "3. Mở file tải về",
     "—",
     "- File tên danh_sach_yeu_cau_xuat_hang_muon\n"
     "- Đầu file có ảnh tiêu đề công ty và dòng chữ in đậm \"DANH SÁCH YÊU CẦU XUẤT HÀNG MƯỢN\"\n"
     "- Bảng có đúng 7 cột: STT, Mã phiếu, Người lập, Ngày lập, Trạng thái, Người duyệt, Ngày duyệt\n"
     "- Đủ 90 dòng, KHÔNG bị cắt còn 10 dòng của trang đang xem\n"
     "- Cuối file có khối ký tên \"Ngày...Tháng...Năm...\" và \"Người lập\""),

    ("002", "Xuất excel mang theo bộ lọc đang đặt", "P0",
     "Công ty có 90 phiếu; lọc Trạng thái = Chờ duyệt ra 7 dòng",
     "1. Mở màn danh sách, bấm nút Bộ lọc\n"
     "2. Chọn Trạng thái = Chờ duyệt, chờ bảng nạp lại\n"
     "3. Bấm nút Xuất excel, mở file",
     "Trạng thái: Chờ duyệt",
     "- File chỉ có đúng 7 dòng\n"
     "- Cột Trạng thái trong file đều ghi \"Chờ duyệt\"\n"
     "- Cột Người duyệt và Ngày duyệt để trống"),

    ("003", "Dòng khoảng ngày trong file excel", "P0",
     "Công ty có phiếu lập rải rác trong tháng 09/2026",
     "1. Điền Từ ngày 01/09/2026 và Đến ngày 05/09/2026, chờ nạp lại\n"
     "2. Bấm Xuất excel, mở file\n"
     "3. Xóa ô Đến ngày, chỉ giữ Từ ngày, xuất lại\n"
     "4. Xóa cả hai ô, xuất lại",
     "Từ ngày: 01/09/2026 · Đến ngày: 05/09/2026",
     "- Lần 1: dưới tiêu đề có dòng \"Từ ngày 01/09/2026 đến ngày 05/09/2026\"\n"
     "- Lần 2: dòng đó chỉ còn \"Từ ngày 01/09/2026\"\n"
     "- Lần 3: KHÔNG có dòng khoảng ngày"),

    ("004", "Định dạng ngày trong file excel", "P1",
     "Phiếu PYCXHM-00317 lập 05/09/2026 lúc 09:00, duyệt 06/09/2026 lúc 14:30",
     "1. Lọc ra đúng phiếu PYCXHM-00317, bấm Xuất excel\n"
     "2. Mở file, đọc 2 cột ngày",
     "—",
     "- Ngày lập ghi 05/09/2026, KHÔNG có giờ\n"
     "- Ngày duyệt ghi 06/09/2026, KHÔNG có giờ\n"
     "- Khác với ngoài danh sách (có kèm giờ:phút) — ghi nhận là hiện trạng đã biết"),

    ("005", "Xuất excel khi bảng rỗng", "P1",
     "Lọc ra 0 dòng",
     "1. Gõ ZZZZZZ vào ô Mã phiếu, chờ bảng nạp lại\n"
     "2. Bấm nút Xuất excel, mở file",
     "Mã phiếu: ZZZZZZ",
     "- Vẫn tải được file, không báo lỗi\n"
     "- File có đủ tiêu đề và dòng tiêu đề bảng nhưng không có dòng dữ liệu nào"),

    ("006", "Màn Kế toán kho không có nút Xuất excel", "P1",
     "Tài khoản KT-1 có quyền Kế toán kho",
     "1. Mở màn Yêu cầu xuất hàng mượn từ menu Kế toán\n"
     "2. Soát toàn bộ nút phía trên bảng",
     "—",
     "- KHÔNG có nút Xuất excel, KHÔNG có nút Tạo mới, KHÔNG có nút Bộ lọc\n"
     "- Muốn xuất excel phải quay về màn Phiếu Yêu cầu xuất hàng mượn"),

    ("007", "Chức năng In phiếu bị hỏng", "P0",
     "Phiếu PYCXHM-00317 bất kỳ, do chính mình lập",
     "1. Mở màn danh sách, bấm biểu tượng bánh răng ở dòng PYCXHM-00317\n"
     "2. Mở chi tiết phiếu, soát toàn màn tìm nút In\n"
     "3. Dán thẳng đường dẫn in của phiếu vào thanh địa chỉ",
     "Đường dẫn in của PYCXHM-00317",
     "- Bước 1 và 2: KHÔNG có nút In ở bất kỳ đâu trên giao diện\n"
     "- ⚠️ Bước 3: trang báo lỗi hệ thống, không hiện bản in. Nguyên nhân: hệ thống trỏ tới một "
     "mẫu in chưa được khai báo. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: có bản in gồm tiêu đề công ty, số phiếu, danh sách phiếu mượn nguồn, người "
     "lập, ghi chú và bảng hàng hóa kèm dòng Tổng cộng"),

    ("008", "Màn hình không có chức năng Nhập excel", "P2",
     "Tài khoản bất kỳ",
     "1. Mở màn danh sách ở cả 4 lối vào\n"
     "2. Soát toàn bộ nút phía trên bảng\n"
     "3. Mở màn Tạo phiếu, soát toàn màn",
     "—",
     "- Không lối vào nào có nút Nhập excel hay Import\n"
     "- Màn Tạo phiếu cũng không có\n"
     "- Chỉ nhập tay được từng phiếu"),
]

SEC_VIII = [
    ("001", "Gửi phiếu khi chưa chọn phiếu xuất mượn", "P0",
     "Đang ở màn Tạo phiếu, chưa thao tác gì",
     "1. Mở màn Tạo phiếu\n"
     "2. Quan sát nút Gửi\n"
     "3. Nhập Ghi chú và đính kèm 1 file pdf rồi quan sát lại",
     "—",
     "- Ô Phiếu xuất mượn ghi \"Chưa chọn phiếu xuất mượn\"\n"
     "- Bảng Chi tiết ghi \"Không có hàng hóa\"\n"
     "- Nút Gửi bị khóa (mờ, bấm không được) ở cả hai lần quan sát"),

    ("002", "Gửi phiếu khi mọi dòng đều để số lượng 0", "P0",
     "Đang lập phiếu, đã chọn PYCXH-00901 với 2 hàng hóa, đã nhập Ghi chú và đính kèm 1 file pdf, "
     "để nguyên số lượng mặc định",
     "1. Xác nhận cả 2 ô Xuất đang là 0\n"
     "2. Quan sát nút Gửi\n"
     "3. Nhập 1 vào một ô Xuất rồi xóa về 0, quan sát lại",
     "Xuất: 0 và 0",
     "- Nút Gửi bị khóa ở cả hai lần quan sát\n"
     "- Nút chỉ mở khi có ít nhất một dòng có số lớn hơn 0"),

    ("003", "Ghi chú là bắt buộc", "P0",
     "Đang lập phiếu, đã chọn phiếu mượn, đã nhập Xuất = 3, đã đính kèm 1 file pdf, để trống Ghi chú",
     "1. Bấm nút Gửi\n"
     "2. Quan sát thông báo và ô Ghi chú\n"
     "3. Nhập Ghi chú rồi bấm Gửi lại",
     "Ghi chú: để trống, sau đó \"Khách đề nghị mượn thêm\"",
     "- Lần 1: thông báo vàng \"Tạo yêu cầu thất bại!\" và dòng chữ đỏ \"Bắt buộc nhập\" ngay "
     "dưới ô Ghi chú\n"
     "- Màn hình không chuyển đi, mọi dữ liệu đã nhập còn nguyên\n"
     "- Lần 2: lưu thành công"),

    ("004", "Ghi chú vượt quá độ dài cho phép", "P1",
     "Đang lập phiếu đủ điều kiện gửi",
     "1. Dán một đoạn dài 256 ký tự vào ô Ghi chú, bấm Gửi\n"
     "2. Xóa bớt còn đúng 255 ký tự, bấm Gửi\n"
     "3. Mở chi tiết phiếu vừa tạo",
     "Ghi chú: 256 ký tự, sau đó 255 ký tự",
     "- Với 256 ký tự: báo đỏ \"Không được vượt quá 255 ký tự\" dưới ô Ghi chú\n"
     "- Với 255 ký tự: lưu được\n"
     "- Màn chi tiết hiện đủ 255 ký tự"),

    ("005", "File đính kèm là bắt buộc", "P0",
     "Đang lập phiếu, đã chọn phiếu mượn, đã nhập Xuất = 3 và Ghi chú, chưa chọn file nào",
     "1. Bấm nút Gửi\n"
     "2. Quan sát thông báo và mục File đính kèm\n"
     "3. Bấm dấu cộng, chọn 1 file pdf rồi bấm Gửi lại",
     "File đính kèm: không có, sau đó 1 file pdf",
     "- Lần 1: thông báo vàng \"Tạo yêu cầu thất bại!\" và dòng chữ đỏ \"Bắt buộc phải chọn\" ở "
     "mục File đính kèm\n"
     "- Lần 2: lưu thành công"),

    ("006", "Chỉ nhận file định dạng pdf", "P0",
     "Đang lập phiếu đủ điều kiện gửi, chuẩn bị sẵn 1 file ảnh và 1 file bảng tính",
     "1. Bấm dấu cộng ở mục File đính kèm\n"
     "2. Bấm vào ô chọn file, quan sát bộ lọc định dạng của hộp thoại chọn file\n"
     "3. Chuyển bộ lọc sang tất cả, chọn file ảnh, bấm Gửi\n"
     "4. Đổi sang file bảng tính, bấm Gửi",
     "File: 1 file ảnh, sau đó 1 file bảng tính",
     "- Hộp thoại chọn file mặc định chỉ hiện file pdf\n"
     "- Chọn file ảnh hoặc file bảng tính rồi gửi: báo \"Tạo yêu cầu thất bại!\" và dòng chữ đỏ "
     "\"Không hợp lệ\" ở ô file đó\n"
     "- Ô file bị lỗi có viền báo lỗi, phiếu không được tạo"),

    ("007", "Thêm và bỏ nhiều file đính kèm", "P1",
     "Đang lập phiếu đủ điều kiện gửi; có sẵn 3 file pdf",
     "1. Bấm dấu cộng 3 lần, chọn lần lượt 3 file pdf\n"
     "2. Quan sát tên file hiện dưới mỗi biểu tượng\n"
     "3. Bấm dấu nhân ở góc file thứ hai để bỏ ra\n"
     "4. Bấm Gửi, mở chi tiết phiếu vừa tạo",
     "File: 3 file pdf, bỏ 1 còn 2",
     "- Mỗi ô file hiện đúng tên file đã chọn\n"
     "- Bỏ file thứ hai: chỉ còn 2 ô\n"
     "- Màn chi tiết hiện đúng 2 file, mở được cả hai"),

    ("008", "Nhập số lượng vượt số đang mượn", "P0",
     "Đang lập phiếu, dòng SP-A001 có cột Đang mượn hiện 6",
     "1. Nhập 7 vào ô Xuất, quan sát dòng và nút Gửi\n"
     "2. Nhập 6, quan sát lại\n"
     "3. Nhập 6,5 rồi quan sát",
     "Xuất: 7, sau đó 6, sau đó 6,5",
     "- Nhập 7: dòng chuyển màu báo lỗi, nút Gửi bị khóa\n"
     "- Nhập 6: dòng trở lại bình thường, nút Gửi mở\n"
     "- Nhập 6,5: dòng chuyển màu báo lỗi vì vượt trần 6"),

    ("009", "Nhập số âm vào ô Xuất", "P0",
     "Đang lập phiếu, dòng SP-A001 có cột Đang mượn hiện 6",
     "1. Nhập -3 vào ô Xuất\n"
     "2. Quan sát dòng, cột Số lượng xuất, Thành tiền và nút Gửi\n"
     "3. Nếu nút Gửi mở thì bấm Gửi",
     "Xuất: -3",
     "- Dòng KHÔNG bị đánh dấu lỗi trên giao diện vì số âm vẫn nhỏ hơn trần\n"
     "- Cột Số lượng xuất hiện -3, Thành tiền hiện số âm\n"
     "- Nút Gửi bị khóa vì không có dòng nào lớn hơn 0\n"
     "- Nếu ghép thêm một dòng khác lớn hơn 0 để mở nút Gửi: hệ thống chặn khi lưu, báo \"Tạo yêu "
     "cầu thất bại!\" kèm dòng chữ đỏ \"Phải lớn hơn 0\" ở ô đó"),

    ("010", "Nhập chữ vào ô Xuất", "P0",
     "Đang lập phiếu, dòng SP-A001 có cột Đang mượn hiện 6",
     "1. Gõ \"abc\" vào ô Xuất\n"
     "2. Bấm ra ngoài ô rồi quan sát cột Số lượng xuất và Thành tiền\n"
     "3. Quan sát nút Gửi",
     "Xuất: abc",
     "- ⚠️ Không có thông báo lỗi nào; cột Số lượng xuất hiện 0 và Thành tiền hiện 0\n"
     "- Nút Gửi bị khóa như khi để 0\n"
     "- Ghi nhận là bẫy đã biết: người dùng dễ tưởng đã nhập được số"),

    ("011", "Nhập số quá 6 chữ số", "P1",
     "Đang lập phiếu; hàng hóa SP-D004 có cột Đang mượn hiện 2.000.000",
     "1. Nhập 1000000 vào ô Xuất, bấm Gửi\n"
     "2. Sửa thành 999999, bấm Gửi",
     "Xuất: 1000000, sau đó 999999",
     "- Với 1000000: giao diện không chặn (vẫn nhỏ hơn trần Đang mượn) nhưng khi lưu báo \"Tạo "
     "yêu cầu thất bại!\" kèm dòng chữ đỏ \"Không được vượt quá 6 chữ số\"\n"
     "- Với 999999: lưu thành công"),

    ("012", "Nhập số lẻ hợp lệ", "P1",
     "Đang lập phiếu; dòng SP-A001 đơn vị Cái, cột Đang mượn hiện 6, Đơn giá 500.000",
     "1. Nhập 2,5 vào ô Xuất\n"
     "2. Đọc cột Số lượng xuất và Thành tiền\n"
     "3. Bấm Gửi, mở chi tiết phiếu vừa tạo",
     "Xuất: 2,5",
     "- Số lượng xuất hiện 2,5 · Thành tiền hiện 1.250.000\n"
     "- Lưu thành công\n"
     "- Màn chi tiết giữ đúng số 2,5, không làm tròn"),
]

SEC_IX = [
    ("001", "Hai tab cùng lập phiếu từ một phiếu mượn", "P0",
     "Phiếu mượn PYCXH-00901 có SP-A001 đang mượn 6 cái; tài khoản NV-A mở 2 tab màn Tạo phiếu",
     "1. Ở cả 2 tab đều chọn PYCXH-00901, cả 2 đều thấy cột Đang mượn hiện 6\n"
     "2. Tab 1 nhập Xuất = 5, nhập ghi chú, đính kèm file, bấm Gửi\n"
     "3. Tab 2 nhập Xuất = 4, nhập ghi chú, đính kèm file, bấm Gửi\n"
     "4. Mở màn danh sách",
     "Xuất: 5 ở tab 1, 4 ở tab 2",
     "- Tab 1 lưu thành công\n"
     "- Tab 2 bị chặn, hiện thông báo vàng \"Số lượng không hợp lệ\", phiếu KHÔNG được tạo\n"
     "- Danh sách chỉ có 1 phiếu mới\n"
     "- Đây là kết quả ĐÚNG, ghi Passed"),

    ("002", "Số đang mượn đổi trong lúc đang lập phiếu", "P0",
     "Phiếu mượn PYCXH-00901 có SP-A001 đang mượn 6 cái; NV-A mở màn Tạo phiếu và chọn phiếu này, "
     "để yên không thao tác",
     "1. Ở màn Tạo phiếu, ghi lại cột Đang mượn là 6, nhập Xuất = 6\n"
     "2. Ở màn khác, lập và gửi 1 phiếu yêu cầu xuất bán hàng mượn xin 3 cái từ chính PYCXH-00901\n"
     "3. Quay lại màn Tạo phiếu (KHÔNG tải lại trang), bấm Gửi\n"
     "4. Tải lại màn Tạo phiếu, chọn lại PYCXH-00901, đọc cột Đang mượn",
     "Xuất: 6",
     "- Bước 3: bị chặn với thông báo \"Số lượng không hợp lệ\"\n"
     "- Bước 4: cột Đang mượn giờ chỉ còn 3\n"
     "- ⚠️ Số trên màn KHÔNG tự cập nhật, phải tải lại trang mới thấy số mới"),

    ("003", "Phiếu bị Kế toán kho xử lý trong lúc người khác đang mở chi tiết", "P0",
     "Phiếu PYCXHM-00324 đang Chờ duyệt; NV-A mở chi tiết phiếu này và để yên",
     "1. NV-A mở chi tiết PYCXHM-00324, ghi lại Trạng thái\n"
     "2. KT-1 ở máy khác từ chối phiếu này\n"
     "3. NV-A tải lại trang chi tiết",
     "—",
     "- Trước khi tải lại: màn hình của NV-A vẫn hiện thông tin cũ, không tự đổi\n"
     "- Sau khi tải lại: hiện thêm khối Ghi chú duyệt, không còn nút xử lý nào\n"
     "- Không treo trang, không báo lỗi"),

    ("004", "Hai Kế toán kho cùng xử lý một phiếu", "P0",
     "Phiếu PYCXHM-00325 đang Chờ duyệt; KT-1 và KT-2 cùng mở chi tiết phiếu này",
     "1. KT-1 bấm Không duyệt, nhập ghi chú, Xác nhận\n"
     "2. KT-2 (chưa tải lại trang) cũng bấm Không duyệt, nhập ghi chú khác, Xác nhận\n"
     "3. Mở lại phiếu, đọc Người duyệt và Ghi chú duyệt",
     "Ghi chú của KT-1 và ghi chú khác của KT-2",
     "- KT-1 thành công\n"
     "- KT-2 bị chặn, hiện thông báo \"Không đủ quyền!\" vì phiếu không còn ở Chờ duyệt\n"
     "- Phiếu giữ đúng Người duyệt KT-1 và ghi chú của KT-1"),

    ("005", "Vừa từ chối vừa lập phiếu xuất từ cùng một phiếu", "P1",
     "Phiếu PYCXHM-00326 đang Chờ duyệt; KT-1 mở chi tiết ở 2 tab",
     "1. Tab 1 bấm Tạo phiếu xuất hàng mượn, nhập đủ và lưu\n"
     "2. Tab 2 (chưa tải lại) bấm Không duyệt, nhập ghi chú, Xác nhận\n"
     "3. Mở lại phiếu, đọc Trạng thái",
     "—",
     "- Tab 1 thành công, phiếu chuyển Đã duyệt\n"
     "- Tab 2 bị chặn, thông báo \"Không đủ quyền!\"\n"
     "- Phiếu giữ trạng thái Đã duyệt, không bị đè thành Không duyệt"),

    ("006", "Người lập chuyển sang công ty khác", "P1",
     "Tài khoản NV-A đã lập 12 phiếu khi còn ở công ty 3; bộ phận nhân sự chuyển hồ sơ NV-A sang "
     "công ty 1",
     "1. Cập nhật hồ sơ nhân sự của NV-A sang công ty 1\n"
     "2. Đăng nhập lại bằng NV-A, mở màn danh sách ở lối vào Phiếu của tôi\n"
     "3. Đọc số tổng\n"
     "4. Mở lối vào Tất cả, đọc số tổng",
     "—",
     "- ⚠️ Hiện trạng: cả 2 lối vào đều ra 0 dòng. 12 phiếu cũ do chính NV-A lập biến mất hoàn "
     "toàn vì hệ thống khóa theo công ty hiện tại của người đăng nhập. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: vẫn xem lại được phiếu do chính mình lập\n"
     "- Sau khi test xong phải trả hồ sơ NV-A về công ty 3"),
]

SEC_X = [
    ("001", "Luồng đủ: lập phiếu, Kế toán kho duyệt đủ số lượng", "P0",
     "Tài khoản NV-A có phiếu mượn PYCXH-00901 Đã hạch toán, Đã mượn, SP-A001 đang mượn 10 cái; "
     "tài khoản KT-1 có quyền Kế toán kho cùng công ty",
     "1. NV-A lập phiếu xin xuất 6 cái, nhập ghi chú, đính 1 file pdf, bấm Gửi\n"
     "2. NV-A mở lại danh sách, ghi lại mã phiếu và trạng thái\n"
     "3. KT-1 mở màn Chờ duyệt, xác nhận thấy phiếu mới\n"
     "4. KT-1 mở chi tiết, bấm Tạo phiếu xuất hàng mượn, giữ nguyên số 6, lưu\n"
     "5. NV-A mở lại phiếu, đọc trạng thái và cột Được duyệt\n"
     "6. NV-A mở lại màn Tạo phiếu, chọn lại PYCXH-00901, đọc cột Đang mượn",
     "Xuất: 6",
     "- Bước 2: phiếu ở Chờ duyệt, mã dạng PYCXHM- kèm 5 chữ số\n"
     "- Bước 3: phiếu có mặt ở màn Chờ duyệt của KT-1\n"
     "- Bước 5: phiếu chuyển Đã duyệt, Người duyệt là KT-1, cột Xuất 6 và cột Được duyệt 6\n"
     "- Bước 6: cột Đang mượn giảm từ 10 xuống 4"),

    ("002", "Luồng đủ: lập phiếu, Kế toán kho duyệt thiếu", "P0",
     "Như TC_10.001 nhưng KT-1 chỉ duyệt 4 trong 6 cái được xin",
     "1. NV-A lập phiếu xin xuất 6 cái, gửi\n"
     "2. KT-1 bấm Tạo phiếu xuất hàng mượn, sửa số xuống 4, lưu\n"
     "3. NV-A mở lại phiếu, đọc bảng Chi tiết\n"
     "4. NV-A mở màn Tạo phiếu, chọn lại PYCXH-00901, đọc cột Đang mượn",
     "Xuất: 6 · Duyệt: 4",
     "- Phiếu chuyển Đã duyệt\n"
     "- Cột Xuất 6, cột Được duyệt 4\n"
     "- Cột Đang mượn giảm từ 10 xuống 6, đúng bằng phần thực sự được xuất\n"
     "- Hai cái chênh lệch KHÔNG tự sinh phiếu mới, muốn xin tiếp phải lập phiếu khác"),

    ("003", "Luồng từ chối rồi lập lại", "P0",
     "Tài khoản NV-A và KT-1 như TC_10.001",
     "1. NV-A lập phiếu xin 6 cái, gửi\n"
     "2. KT-1 từ chối với ghi chú \"Khách còn nợ quá hạn\"\n"
     "3. NV-A mở lại phiếu, đọc trạng thái và khối Ghi chú duyệt\n"
     "4. NV-A tìm nút sửa hoặc gửi lại phiếu\n"
     "5. NV-A mở màn Tạo phiếu, chọn lại PYCXH-00901, đọc cột Đang mượn\n"
     "6. NV-A lập phiếu mới xin 3 cái, gửi",
     "Xuất lần 1: 6 · Xuất lần 2: 3",
     "- Bước 3: phiếu ở Không duyệt, có khối Ghi chú duyệt đúng nội dung\n"
     "- Bước 4: KHÔNG có nút sửa và KHÔNG có nút gửi lại — phải lập phiếu mới\n"
     "- Bước 5: cột Đang mượn quay về 10, phần bị từ chối được nhả lại\n"
     "- Bước 6: lưu được phiếu mới, mã khác phiếu cũ"),

    ("004", "Luồng gộp nhiều phiếu mượn đầu tới cuối", "P0",
     "NV-A có 2 phiếu mượn PYCXH-00901 (SP-A001 đang mượn 10) và PYCXH-00902 (SP-A001 đang mượn "
     "6, SP-B002 đang mượn 4)",
     "1. NV-A lập 1 phiếu gộp cả 2 phiếu mượn\n"
     "2. Nhập Xuất = 3 ở dòng PYCXH-00901, Xuất = 2 ở dòng PYCXH-00902 của SP-A001, Xuất = 4 cho "
     "SP-B002\n"
     "3. Nhập ghi chú, đính 1 file pdf, gửi\n"
     "4. KT-1 duyệt đủ số\n"
     "5. NV-A mở lại phiếu và mở lại màn Tạo phiếu để đọc số còn mượn",
     "Xuất: 3 + 2 cho SP-A001, 4 cho SP-B002",
     "- Bảng Chi tiết có 2 hàng hóa: SP-A001 số lượng 5 (2 dòng con), SP-B002 số lượng 4 (1 dòng "
     "con)\n"
     "- Sau khi duyệt: PYCXH-00901 còn mượn 7, PYCXH-00902 còn mượn 4 cái SP-A001 và 0 cái SP-B002\n"
     "- SP-B002 đã trả hết nên lần sau chọn PYCXH-00902 sẽ không còn dòng SP-B002"),

    ("005", "Đối chiếu số tổng giữa các lối vào sau khi chạy hết luồng", "P1",
     "Sau khi chạy xong TC_10.001 đến TC_10.004 trong cùng công ty; tài khoản KT-1 có cả quyền "
     "Kế toán kho và quyền xem theo công ty",
     "1. Đăng nhập KT-1, ghi số tổng ở lối vào Tất cả\n"
     "2. Ghi số tổng ở lối vào Kế toán kho\n"
     "3. Ghi số tổng ở lối vào Chờ duyệt\n"
     "4. Lọc Trạng thái = Chờ duyệt ở lối vào Tất cả, ghi số tổng\n"
     "5. So sánh 4 con số",
     "—",
     "- Số ở bước 1 và bước 2 BẰNG NHAU (vì không có phiếu nào ở Đang tạo)\n"
     "- Số ở bước 3 và bước 4 BẰNG NHAU\n"
     "- Lệch nhau thì phải truy nguyên trước khi ghi kết quả, không đoán"),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", SEC_III),
    ("IV", "LẬP PHIẾU & XEM CHI TIẾT", SEC_IV),
    ("V", "DUYỆT & KHÔNG DUYỆT", SEC_V),
    ("VI", "SỬA & XÓA", SEC_VI),
    ("VII", "XUẤT EXCEL & IN PHIẾU", SEC_VII),
    ("VIII", "RÀNG BUỘC NHẬP LIỆU", SEC_VIII),
    ("IX", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", SEC_IX),
    ("X", "LUỒNG NGHIỆP VỤ ĐẦU - CUỐI", SEC_X),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Phiếu yêu cầu xuất hàng mượn (ERP) - Cập nhật ngày 07/09/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )
