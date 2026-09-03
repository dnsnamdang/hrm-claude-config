# -*- coding: utf-8 -*-
"""Sinh file testcase Excel cho man "Phieu chi tien" (phan he Tai chinh).

Nguon doc code 03/09/2026 (nhanh gop_db):
  BE  Modules/Finance/Routes/api.php (:299-324)
      Modules/Finance/Http/Controllers/V1/BillPaymentController.php
      Modules/Finance/Entities/BillPayment/{BillPayment,BillPaymentAccess,BillPaymentDetail}.php
      Modules/Finance/Http/Requests/BillPayment/*.php  (nguyen van thong bao loi)
      Modules/Finance/Services/BillPayment{Service,WriteService,ApprovalFlowService,
                                           AccountingService,PrintService,HistoryService}.php
      Modules/Finance/Transformers/BillPaymentResource/*.php
      Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (:1203, :1213-1215)
  FE  hrm-client/pages/finance/bill-payments/{index,create}.vue
      .../_id/{index,edit,print}.vue
      .../components/{BillPaymentForm,PaymentEmployeeTable,ApproveBillPaymentModal,
                      PaymentRequestSearchModal}.vue
      hrm-client/components/subsystem-menu/finance.js (:86)
  Anh that: pc_shots/ (cong dev hrm-crm.eteksofts.com; rieng man IN chup tren local)

Chay:  python .plans/gop-db/finance-bill-payment/gen_testcase.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills",
                                "testcase-documenter", "assets"))
from tc_engine import build  # noqa: E402

OUT = os.path.join(HERE, "testcase.xlsx")
MODULE = "Phiếu chi tiền"

MENU = "Phân hệ Tài chính > Quản lý tiền > Thanh toán tiền mặt > Phiếu chi"

# ════════════════════════════════════════════════════ 1. KHỐI MÔ TẢ (9 mục)
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Phiếu chi tiền là chứng từ kế toán ghi nhận khoản tiền doanh nghiệp chi ra. Màn hình cho "
     "phép: lập phiếu (Lưu nháp hoặc Lưu và gửi duyệt), sửa và xóa phiếu nháp, xem chi tiết, "
     "duyệt, hủy, in 2 liên, xuất Excel một phiếu, xem lịch sử thay đổi.\n"
     "Màn hình phục vụ HAI luồng nghiệp vụ khác hẳn nhau:\n"
     "- Luồng lập từ Đề nghị thanh toán (các loại chi: Chi trả nhà cung cấp, Chi trả lại khách "
     "hàng, Chi thưởng NVKD, Chi thưởng thực hiện hợp đồng, Chi khác, Thanh toán chi phí vận "
     "chuyển NCC): kế toán chọn phiếu đề nghị, chốt số tiền chi rồi gửi duyệt. Thủ quỹ duyệt là "
     "xong — MỘT cấp duyệt.\n"
     "- Luồng Chi thu nhập cho nhân viên: lập TRỰC TIẾP không qua đề nghị. Kế toán chọn phòng "
     "ban, hệ thống tự hút 6 khoản thu nhập của từng nhân viên từ sổ kế toán. Phiếu phải qua "
     "HAI cấp duyệt: Kế toán trưởng duyệt trước, rồi Thủ quỹ duyệt.\n"
     "Bước Thủ quỹ duyệt là thời điểm DUY NHẤT hệ thống ghi bút toán vào sổ kế toán.\n"
     "Đường dẫn màn hình: " + MENU + ". Chỉ có duy nhất MỘT mục menu trỏ vào màn này."),

    ("2. Đối tượng được tính / hiển thị",
     "Danh sách hiển thị phiếu chi theo phạm vi quyền của người đăng nhập:\n"
     "- Là quản trị hệ thống, hoặc có quyền 'Xem tất cả phiếu chi của tổng công ty': thấy phiếu "
     "của mọi công ty.\n"
     "- Có quyền 'Xem tất cả phiếu chi của công ty': chỉ phiếu thuộc công ty của mình.\n"
     "- Không có quyền nào trong hai quyền trên: chỉ thấy phiếu do chính mình lập.\n"
     "Ngoài ra, người đã duyệt một phiếu (Thủ quỹ hoặc Kế toán trưởng) luôn mở lại được phiếu đó "
     "ở màn chi tiết, và người có quyền duyệt luôn mở được phiếu CÙNG CÔNG TY đang chờ đúng cấp "
     "mình — kể cả khi không có quyền xem theo cấp nào.\n"
     "Đủ 5 trạng thái đều được hiển thị: Đang tạo, Chờ KT trưởng duyệt, Chờ chi tiền, Đã duyệt, "
     "Hủy.\n"
     "Đủ 7 loại chi đều hiển thị: Chi trả nhà cung cấp, Chi trả lại khách hàng, Chi thưởng NVKD, "
     "Chi thu nhập cho nhân viên, Chi thưởng thực hiện hợp đồng, Chi khác, Thanh toán chi phí "
     "vận chuyển NCC."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu ở trạng thái 'Đang tạo' (nháp) của NGƯỜI KHÁC luôn bị ẩn khỏi danh sách, và quyền "
     "xem theo cấp cũng KHÔNG mở được màn chi tiết của nháp người khác.\n"
     "- Người không xác định được là ai (phiên đăng nhập hỏng) thì danh sách RỖNG tuyệt đối.\n"
     "- Cửa sổ chọn phiếu đề nghị CHỈ liệt kê phiếu đề nghị thanh toán đang ở trạng thái 'Chờ "
     "tạo phiếu chi' VÀ chưa có phiếu chi nào.\n"
     "- Hai ô chọn tài khoản (Tài khoản có, Tài khoản nợ) chỉ liệt kê tài khoản đang hoạt động "
     "VÀ là tài khoản cấp cuối; tài khoản tổng hợp không cho chọn. Phiếu cũ đang gắn tài khoản "
     "đã khóa thì tài khoản đó vẫn hiện đúng tên khi mở màn Sửa / Xem.\n"
     "- Khối 'Ngân hàng nhận tiền' và 'Ngân hàng trung gian' chỉ hiện khi hình thức thanh toán "
     "là chuyển khoản; chọn tiền mặt thì hai khối này ẩn.\n"
     "- Bảng chi tiết của luồng Chi thu nhập cho nhân viên chỉ nạp khi đã chọn Phòng ban chi; "
     "phòng ban không có số liệu thu nhập thì bảng hiện 'Không có dữ liệu phù hợp'."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Hai ô 'Ngày lập từ' và 'Ngày lập đến' lọc theo NGÀY LẬP PHIẾU CHI (cột Ngày tạo trên "
     "lưới), không phải Ngày cập nhật và cũng không phải ngày hạch toán.\n"
     "Cả hai mốc lấy trọn ngày: chọn 'Ngày lập đến' là hôm nay thì phiếu lập chiều nay vẫn nằm "
     "trong kết quả. Bỏ trống một trong hai ô thì phía đó không giới hạn.\n"
     "Màn hình KHÔNG có ô lọc theo ngày hạch toán và không có ô lọc theo ngày duyệt."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Một phiếu chi gồm 2 tầng:\n"
     "- Tầng 1 (phiếu): mã phiếu sinh tự động dạng {mã công ty}.PC{tháng năm}.{5 chữ số}, loại "
     "chi, tài khoản có, người nhận, hình thức thanh toán, loại tiền, tỷ giá, lý do chi, trạng "
     "thái. Luồng lập từ đề nghị có thêm Số phiếu đề nghị và khối thông tin ngân hàng nhận "
     "tiền; luồng Chi thu nhập nhân viên có thêm Phòng ban chi.\n"
     "- Tầng 2 (dòng chi tiết): luồng lập từ đề nghị thì KÉO THẲNG từ phiếu đề nghị, mỗi dòng "
     "gồm tài khoản nợ, đối tượng nhận tiền, số hợp đồng, số tiền đề nghị chi (chỉ đọc), số "
     "tiền chi và ghi chú. Luồng Chi thu nhập nhân viên thì mỗi dòng là MỘT NHÂN VIÊN, gồm tài "
     "khoản nợ, tên nhân viên, số dư và 6 khoản thu nhập (chênh lệch, hoa hồng tháng, hoa hồng "
     "quý, thưởng quý, tiền giao hàng, chi phí khác).\n"
     "- Một phiếu đề nghị thanh toán chỉ lập được ĐÚNG MỘT phiếu chi."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Dòng 'Tổng cộng' cuối bảng chi tiết cộng dọc theo từng cột tiền của các dòng đang hiển "
     "thị.\n"
     "- Cột 'Số tiền' trên màn danh sách là tổng số tiền chi của phiếu, ngăn cách hàng nghìn "
     "bằng dấu chấm.\n"
     "- Phiếu ngoại tệ hiển thị THÊM một cột cho mỗi nhóm tiền: cột nguyên tệ và cột quy đổi ra "
     "đồng Việt Nam. Cột quy đổi tính theo ô Tỷ giá của phiếu.\n"
     "- Ở bảng Chi thu nhập nhân viên, cột 'Số dư' của một nhân viên ĐƯỢC PHÉP ÂM (trường hợp "
     "truy thu); hệ thống so trần số tiền chi theo GIÁ TRỊ TUYỆT ĐỐI của số dư, nên dòng số dư "
     "âm vẫn chi được.\n"
     "- Khi Thủ quỹ duyệt, số tiền chi của từng dòng phải nhỏ hơn hoặc bằng số tiền đề nghị chi "
     "của chính dòng đó; vượt là chặn cả phiếu."),

    ("7. Phân quyền cấp",
     "Hai quyền quyết định phạm vi dữ liệu nhìn thấy (đặt tên đúng như trong hệ thống):\n"
     "- Xem tất cả phiếu chi của tổng công ty\n"
     "- Xem tất cả phiếu chi của công ty\n"
     "Ba quyền thao tác:\n"
     "- Kế toán thanh toán: lập, sửa, xóa, gửi duyệt phiếu chi; mở được cửa sổ chọn phiếu đề "
     "nghị và xem được số liệu thu nhập nhân viên.\n"
     "- Kế toán trưởng duyệt phiếu chi: duyệt và hủy phiếu ở trạng thái 'Chờ KT trưởng duyệt' "
     "(chỉ phát sinh với loại Chi thu nhập cho nhân viên).\n"
     "- Thủ quỹ duyệt phiếu chi: duyệt và hủy phiếu ở trạng thái 'Chờ chi tiền'. Đây là cấp "
     "duyệt cuối, ghi bút toán vào sổ kế toán.\n"
     "Cả hai cấp duyệt đều bắt buộc CÙNG CÔNG TY với phiếu.\n"
     "Vai trò quản trị hệ thống được coi như có đủ các quyền trên, RIÊNG chức năng Sửa / Xóa thì "
     "quản trị hệ thống KHÔNG được miễn trừ: vẫn phải là người lập phiếu.\n"
     "Ba chức năng Xem chi tiết / In / Xuất Excel chỉ cần nhìn thấy được phiếu; Lịch sử không "
     "gắn quyền riêng."),

    ("8. Cách tính các ô thống kê",
     "- Dòng 'Hiển thị a–b / N' dưới lưới: a là số thứ tự dòng đầu trang, b là dòng cuối, N là "
     "tổng số phiếu khớp bộ lọc VÀ nằm trong phạm vi quyền.\n"
     "- Cột STT đánh theo trang: sang trang 2 với cỡ 10 dòng/trang thì bắt đầu từ 11.\n"
     "- Dòng 'Tổng cộng' trong bảng chi tiết = cộng dọc từng cột tiền của các dòng trong phiếu.\n"
     "- Ở bảng Chi thu nhập nhân viên, dòng 'Tổng cộng' cộng cả 6 khoản thu nhập lẫn cột Số tiền "
     "chi.\n"
     "- Bản in có dòng 'Bằng chữ' đọc số tiền tổng ra chữ tiếng Việt."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất của màn này:\n"
     "- DUYỆT PHIẾU Ở CẤP THỦ QUỸ LÀ THAO TÁC KHÔNG HOÀN TÁC: hệ thống ghi bút toán vào sổ kế "
     "toán dùng chung với cổng cũ. Khi kiểm thử phải dùng phiếu do chính mình tạo, TUYỆT ĐỐI "
     "không duyệt phiếu của người khác trên dữ liệu thật.\n"
     "- Kế toán trưởng duyệt (bước 1 của luồng Chi thu nhập nhân viên) thì CHƯA ghi sổ kế toán — "
     "chỉ chuyển phiếu sang 'Chờ chi tiền'. Ghi sổ chỉ xảy ra ở bước Thủ quỹ.\n"
     "- Chỉ có duy nhất MỘT nút 'Duyệt phiếu chi'; hệ thống tự biết đang duyệt ở cấp nào theo "
     "trạng thái phiếu. Người có quyền Kế toán trưởng mà mở phiếu 'Chờ chi tiền' thì không thấy "
     "nút, và ngược lại.\n"
     "- Lưu nháp KHÔNG bắt buộc trường nào, TRỪ 'Loại chi'. Toàn bộ ràng buộc bắt buộc chỉ áp "
     "khi bấm 'Lưu và gửi duyệt'. Đây là điểm khác cổng cũ có chủ đích.\n"
     "- Trong nhóm lập-từ-đề-nghị, chỉ 3 loại (Chi trả nhà cung cấp, Chi trả lại khách hàng, Chi "
     "thưởng NVKD) mới bắt buộc phải có phiếu đề nghị và dòng chi tiết. Ba loại còn lại (Chi "
     "thưởng thực hiện hợp đồng, Chi khác, Thanh toán chi phí vận chuyển NCC) gửi duyệt được dù "
     "trống cả hai — đây là quyết định nghiệp vụ đã chốt, KHÔNG phải sót kiểm tra.\n"
     "- Sửa và Xóa chỉ mở với phiếu 'Đang tạo' DO CHÍNH MÌNH lập và người đó phải có quyền Kế "
     "toán thanh toán; quản trị hệ thống cũng không sửa/xóa được phiếu người khác.\n"
     "- Người lập KHÔNG tự hủy được phiếu đã gửi duyệt — quyền hủy thuộc về cấp đang chờ duyệt.\n"
     "- Lý do hủy và Ghi chú của người duyệt KHÔNG được lưu vào phiếu mà lưu vào lịch sử thay "
     "đổi; muốn tra thì mở Lịch sử. Riêng phiếu đã hủy có thêm dải băng vàng ở đầu màn chi tiết "
     "hiện lại hai nội dung này.\n"
     "- Bộ lọc được ghi nhớ 10 phút: rời màn rồi quay lại trong 10 phút thì điều kiện lọc cũ vẫn "
     "còn."),
]

# ════════════════════════════════════════════════════ 2. PHÂN QUYỀN
ROLE_TCS = [
    ("00", "Không có quyền xem nào — chỉ thấy phiếu của chính mình", "P0",
     "Tài khoản A không có 'Xem tất cả phiếu chi của tổng công ty', không có 'Xem tất cả phiếu "
     "chi của công ty', không phải quản trị hệ thống. A đã lập 5 phiếu; công ty của A có 90 "
     "phiếu.",
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Vào " + MENU + "\n"
     "3. Đọc tổng số phiếu ở dòng 'Hiển thị a–b / N'",
     "—",
     "- Tổng N = 5, đúng bằng số phiếu A tự lập\n"
     "- Cột Người tạo của mọi dòng đều là tên A\n"
     "- Nút 'Tạo mới' vẫn hiện"),

    ("01", "Quyền 'Xem tất cả phiếu chi của công ty'", "P0",
     "Tài khoản B có quyền 'Xem tất cả phiếu chi của công ty', thuộc công ty 4. Công ty 4 có 90 "
     "phiếu, trong đó 3 phiếu nháp của người khác.",
     "1. Đăng nhập bằng tài khoản B\n"
     "2. Vào " + MENU + "\n"
     "3. Đếm tổng số phiếu",
     "—",
     "- Tổng N = 87 (90 trừ 3 nháp của người khác)\n"
     "- Không có phiếu nào của công ty khác"),

    ("02", "Quyền 'Xem tất cả phiếu chi của tổng công ty'", "P0",
     "Tài khoản C có quyền 'Xem tất cả phiếu chi của tổng công ty'. Toàn hệ thống có 1.334 "
     "phiếu, trong đó 6 nháp của người khác và 1 nháp của chính C.",
     "1. Đăng nhập bằng tài khoản C\n"
     "2. Vào " + MENU + "\n"
     "3. Đếm tổng số phiếu",
     "—",
     "- Tổng N = 1.328 (1.334 trừ 6 nháp người khác, vẫn giữ 1 nháp của C)\n"
     "- Thấy phiếu của mọi công ty"),

    ("03", "Quản trị hệ thống — xem như quyền tổng công ty", "P0",
     "Tài khoản D là quản trị hệ thống, KHÔNG được gán quyền xem nào.",
     "1. Đăng nhập bằng tài khoản D\n"
     "2. Vào " + MENU + "\n"
     "3. So tổng số phiếu với tài khoản C ở trường hợp trên",
     "—",
     "- D thấy phiếu của mọi công ty, phạm vi tương đương tài khoản C\n"
     "- Nháp của người khác vẫn bị ẩn với D"),

    ("04", "Quyền 'Kế toán thanh toán' — lập được phiếu chi", "P0",
     "Tài khoản E có quyền 'Kế toán thanh toán'. Hệ thống có 76 phiếu đề nghị thanh toán đang "
     "Chờ tạo phiếu chi và chưa lập phiếu chi.",
     "1. Đăng nhập bằng tài khoản E\n"
     "2. Bấm 'Tạo mới', chọn Loại chi = 'Chi trả nhà cung cấp'\n"
     "3. Bấm vào ô 'Số phiếu đề nghị'",
     "—",
     "- Vào được màn Thêm phiếu chi tiền\n"
     "- Cửa sổ 'Chọn phiếu đề nghị chi' mở ra và liệt kê 76 phiếu\n"
     "- Chọn được một phiếu, bảng Chi tiết nạp đủ dòng"),

    ("05", "Không có quyền 'Kế toán thanh toán' — không lập được phiếu chi", "P0",
     "Tài khoản A không có quyền 'Kế toán thanh toán', không phải quản trị hệ thống.",
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Bấm 'Tạo mới', chọn Loại chi bất kỳ\n"
     "3. Bấm vào ô 'Số phiếu đề nghị'\n"
     "4. Nếu vào được thì điền đủ và bấm 'Lưu nháp'",
     "—",
     "- Cửa sổ chọn phiếu đề nghị bị từ chối, báo không có quyền xem danh sách phiếu đề nghị chi\n"
     "- Ép lưu thì hệ thống từ chối, báo 'Bạn không có quyền lập phiếu chi tiền'\n"
     "- Không có phiếu chi nào được tạo"),

    ("06", "Không có quyền 'Kế toán thanh toán' — không xem được số liệu thu nhập nhân viên", "P0",
     "Tài khoản A không có quyền 'Kế toán thanh toán'.",
     "1. Đăng nhập tài khoản A\n"
     "2. Bấm 'Tạo mới', chọn Loại chi = 'Chi thu nhập cho nhân viên'\n"
     "3. Chọn một Phòng ban chi",
     "—",
     "- Bảng Chi tiết không nạp được, hệ thống báo không có quyền xem số liệu thu nhập nhân viên"),

    ("07", "Quyền 'Thủ quỹ duyệt phiếu chi' — thấy nút Duyệt và Hủy ở phiếu Chờ chi tiền", "P0",
     "Tài khoản F có quyền 'Thủ quỹ duyệt phiếu chi', cùng công ty với phiếu. Phiếu "
     "TPE.PC0826.00025 đang ở trạng thái 'Chờ chi tiền'.",
     "1. Đăng nhập bằng tài khoản F\n"
     "2. Mở màn chi tiết phiếu TPE.PC0826.00025\n"
     "3. Quan sát các nút cuối màn",
     "—",
     "- Có nút 'Duyệt phiếu chi' (xanh) và 'Hủy phiếu chi' (đỏ)\n"
     "- Có thêm nút 'In', 'Xuất Excel', 'Quay lại'\n"
     "- Không có nút 'Sửa' và 'Xóa'"),

    ("08", "Quyền Thủ quỹ nhưng phiếu đang chờ Kế toán trưởng", "P0",
     "Tài khoản F chỉ có quyền 'Thủ quỹ duyệt phiếu chi'. Phiếu X thuộc loại 'Chi thu nhập cho "
     "nhân viên', đang ở trạng thái 'Chờ KT trưởng duyệt', cùng công ty với F.",
     "1. Đăng nhập tài khoản F\n"
     "2. Mở màn chi tiết phiếu X\n"
     "3. Quan sát các nút",
     "—",
     "- ⚠️ KHÔNG có nút 'Duyệt phiếu chi' và 'Hủy phiếu chi'\n"
     "- Hệ thống tự nhận cấp duyệt theo trạng thái phiếu: trạng thái này thuộc về Kế toán trưởng"),

    ("09", "Quyền 'Kế toán trưởng duyệt phiếu chi'", "P0",
     "Tài khoản G có quyền 'Kế toán trưởng duyệt phiếu chi', cùng công ty với phiếu. Phiếu X "
     "đang ở 'Chờ KT trưởng duyệt'; phiếu Y đang ở 'Chờ chi tiền'.",
     "1. Đăng nhập tài khoản G\n"
     "2. Mở chi tiết phiếu X, quan sát các nút\n"
     "3. Mở chi tiết phiếu Y, quan sát các nút",
     "—",
     "- Phiếu X: CÓ nút 'Duyệt phiếu chi' và 'Hủy phiếu chi'\n"
     "- ⚠️ Phiếu Y: KHÔNG có hai nút đó (trạng thái đó thuộc về Thủ quỹ)"),

    ("10", "Người duyệt KHÁC công ty với phiếu", "P0",
     "Tài khoản H có quyền 'Thủ quỹ duyệt phiếu chi' nhưng thuộc công ty 1. Phiếu "
     "TPE.PC0826.00025 thuộc công ty 4, trạng thái 'Chờ chi tiền'.",
     "1. Đăng nhập tài khoản H\n"
     "2. Gõ thẳng đường dẫn màn chi tiết phiếu TPE.PC0826.00025 lên thanh địa chỉ",
     "—",
     "- Hệ thống từ chối, báo không có quyền xem phiếu chi này\n"
     "- ⚠️ Cả hai cấp duyệt đều bắt buộc cùng công ty với phiếu"),

    ("11", "Người duyệt luôn xem lại được phiếu mình đã xử lý", "P1",
     "Tài khoản F (thủ quỹ) đã duyệt phiếu X. Sau đó F bị thu hồi mọi quyền xem theo cấp.",
     "1. Đăng nhập tài khoản F\n"
     "2. Mở màn chi tiết phiếu X",
     "—",
     "- Mở được, không bị chặn — người đã duyệt luôn xem lại được phiếu mình xử lý\n"
     "- ⚠️ Nhưng trên DANH SÁCH phiếu X có thể không hiện, vì danh sách lọc theo quyền xem"),

    ("12", "Người có quyền duyệt xem được phiếu đang chờ đúng cấp mình", "P0",
     "Tài khoản F có quyền 'Thủ quỹ duyệt phiếu chi', cùng công ty với phiếu, nhưng KHÔNG có "
     "quyền xem theo tổng công ty lẫn theo công ty. Phiếu Y do người khác lập, đang 'Chờ chi "
     "tiền'.",
     "1. Đăng nhập tài khoản F\n"
     "2. Mở màn chi tiết phiếu Y",
     "—",
     "- Mở được và có nút Duyệt/Hủy\n"
     "- ⚠️ Không có nhánh này thì người sắp phải duyệt lại không mở nổi phiếu để duyệt"),

    ("13", "Bỏ qua giao diện, gọi thẳng chức năng Duyệt khi không đủ quyền", "P0",
     "Tài khoản E chỉ có 'Kế toán thanh toán'. Phiếu TPE.PC0826.00025 đang 'Chờ chi tiền'.",
     "1. Đăng nhập bằng tài khoản E\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Duyệt cho phiếu này, bỏ qua giao diện\n"
     "3. Mở lại phiếu kiểm tra trạng thái và sổ kế toán",
     "Số tiền chi: bằng số đề nghị chi",
     "- Hệ thống từ chối, báo 'Bạn không có quyền duyệt phiếu chi này.'\n"
     "- Phiếu vẫn ở 'Chờ chi tiền', KHÔNG phát sinh bút toán nào\n"
     "- Ghi chú: trường hợp này dành cho tester kỹ thuật"),

    ("14", "Bỏ qua giao diện, gọi thẳng chức năng Sửa phiếu nháp của người khác", "P0",
     "Tài khoản E có quyền 'Kế toán thanh toán'. Phiếu nháp do NGƯỜI KHÁC lập (E không nhìn thấy "
     "trên danh sách nhưng biết mã).",
     "1. Đăng nhập bằng tài khoản E\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Sửa cho phiếu nháp đó\n"
     "3. Đăng nhập lại bằng người lập phiếu để kiểm tra",
     "Người nhận: 'sửa lén'",
     "- Hệ thống từ chối; phiếu nháp còn nguyên, nội dung không đổi\n"
     "- ⚠️ Đây là điểm siết chặt hơn cổng cũ: cổng cũ chỉ kiểm trạng thái nên ai gọi được đường "
     "dẫn cũng sửa được nháp của người khác\n"
     "- Ghi chú: trường hợp này dành cho tester kỹ thuật"),

    ("15", "Quản trị hệ thống KHÔNG được miễn trừ ở chức năng Sửa / Xóa", "P0",
     "Tài khoản D là quản trị hệ thống. Phiếu nháp P do tài khoản E lập.",
     "1. Đăng nhập tài khoản D\n"
     "2. Mở màn chi tiết phiếu P (xem được vì quản trị hệ thống)\n"
     "3. Quan sát các nút cuối màn",
     "—",
     "- Xem được nội dung phiếu\n"
     "- ⚠️ KHÔNG có nút 'Sửa' và 'Xóa' — miễn trừ của quản trị hệ thống chỉ áp cho việc XEM"),
]

# ════════════════════════════════════════════════════ 3. SECTION NGHIỆP VỤ

S1 = [
    ("001", "Mở màn danh sách lần đầu — bố cục và các cột", "P0",
     "Tài khoản C (quyền xem tổng công ty), hệ thống có 1.334 phiếu.",
     "1. Đăng nhập\n"
     "2. Vào " + MENU + "\n"
     "3. Chờ lưới nạp xong rồi quan sát (kéo ngang để xem hết cột)",
     "—",
     "- Tiêu đề trang và tiêu đề lưới đều là 'Danh sách phiếu chi'\n"
     "- Lưới có 14 cột: STT, Mã phiếu, Mã phiếu đề nghị chi, Loại chi, Khách hàng / Nhà cung "
     "cấp, Số tiền, Người đề nghị, Phòng ban, Ngày tạo, Người tạo, Ngày cập nhật, Người cập "
     "nhật, Trạng thái, Hành động\n"
     "- Khối lọc có ô tìm nhanh ghi 'Tìm theo mã phiếu chi...', nút 'Tìm kiếm', 'Làm mới', "
     "'Cài đặt bộ lọc', 'Tìm kiếm nâng cao'\n"
     "- Thanh công cụ có nút 'Tạo mới' và nút biểu tượng cấu hình cột\n"
     "- Mặc định 10 dòng/trang, dòng đếm ghi 'Hiển thị 1–10 / 1334'"),

    ("002", "Thứ tự mặc định của danh sách", "P0",
     "Có phiếu lập hôm nay và phiếu lập tháng trước.",
     "1. Mở màn danh sách, không đụng vào cột sắp xếp\n"
     "2. So cột Ngày tạo giữa dòng 1 và dòng 10",
     "—",
     "- Phiếu mới nhất nằm trên cùng, Ngày tạo giảm dần từ trên xuống"),

    ("003", "Chỉ có duy nhất một mục menu trỏ vào màn này", "P1",
     "Tài khoản C.",
     "1. Mở phân hệ Tài chính\n"
     "2. Bấm nhóm 'Quản lý tiền'\n"
     "3. Rà toàn bộ chức năng trong bảng vừa mở",
     "—",
     "- Nhóm 'Thanh toán tiền mặt' có 5 chức năng: Phiếu thu, Phiếu chi, Phiếu báo có, Tổng hợp "
     "tiền về ngân hàng, Phiếu ủy nhiệm chi\n"
     "- Chỉ 'Phiếu chi' mở màn 'Danh sách phiếu chi'"),

    ("004", "Thêm tham số lạ vào thanh địa chỉ", "P1",
     "Tài khoản A (chỉ thấy 5 phiếu của mình).",
     "1. Mở màn danh sách, ghi lại tổng số phiếu\n"
     "2. Thêm đuôi ?mode=all vào cuối đường dẫn rồi nhấn Enter\n"
     "3. Đếm lại tổng số phiếu",
     "?mode=all",
     "- Trang mở bình thường, không báo lỗi\n"
     "- ⚠️ Tổng số phiếu KHÔNG đổi, vẫn là 5"),

    ("005", "Bộ lọc được ghi nhớ khi quay lại trong 10 phút", "P1",
     "Tài khoản C.",
     "1. Chọn Trạng thái = 'Chờ chi tiền', chờ lưới lọc xong\n"
     "2. Bấm vào một mã phiếu để sang màn chi tiết\n"
     "3. Bấm 'Quay lại' (trong vòng 10 phút)",
     "Trạng thái: Chờ chi tiền",
     "- Về lại danh sách, ô Trạng thái vẫn giữ 'Chờ chi tiền'\n"
     "- Lưới vẫn chỉ hiện phiếu Chờ chi tiền"),

    ("006", "Màn danh sách khi không có phiếu nào", "P1",
     "Tài khoản mới, chưa lập phiếu nào, không có quyền xem nào.",
     "1. Đăng nhập\n2. Vào " + MENU,
     "—",
     "- Lưới hiện 'Không có dữ liệu phù hợp bộ lọc.'\n"
     "- Nút 'Tạo mới' vẫn dùng được"),

    ("007", "Thông báo khi có phiếu chi gửi duyệt", "P0",
     "Tài khoản F có quyền 'Thủ quỹ duyệt phiếu chi' cùng công ty. Tài khoản E vừa lập và gửi "
     "duyệt 1 phiếu chi thuộc nhóm lập-từ-đề-nghị.",
     "1. Đăng nhập tài khoản F\n"
     "2. Mở chuông thông báo\n"
     "3. Bấm vào dòng thông báo mới nhất",
     "—",
     "- Có thông báo về phiếu chi đang chờ duyệt, kèm mã phiếu và tên người lập\n"
     "- Bấm vào thông báo mở đúng màn chi tiết của phiếu đó"),

    ("008", "Thông báo hai cấp của luồng Chi thu nhập nhân viên", "P0",
     "Tài khoản G có quyền Kế toán trưởng, tài khoản F có quyền Thủ quỹ, cùng công ty.",
     "1. E lập phiếu loại 'Chi thu nhập cho nhân viên' và gửi duyệt\n"
     "2. Kiểm tra chuông của G và của F\n"
     "3. G duyệt phiếu\n"
     "4. Kiểm tra lại chuông của F",
     "—",
     "- Sau bước 1: G nhận thông báo; F CHƯA nhận\n"
     "- Sau bước 3: F mới nhận thông báo phiếu chờ chi tiền\n"
     "- ⚠️ Thông báo đi đúng cấp đang chờ, không bắn cho cả hai cùng lúc"),

    ("009", "Lưu nháp KHÔNG bắn thông báo", "P1",
     "Tài khoản F là thủ quỹ cùng công ty với E.",
     "1. E lập phiếu chi và bấm 'Lưu nháp'\n"
     "2. Đăng nhập F, mở chuông thông báo và mở danh sách",
     "—",
     "- F không nhận thông báo nào\n"
     "- F cũng không thấy phiếu nháp này trên danh sách"),
]

S2 = [
    ("001", "Ô tìm nhanh tìm theo mã phiếu", "P0",
     "Có phiếu TPE.PC0826.00025 trong phạm vi quyền.",
     "1. Gõ '00025' vào ô tìm nhanh\n2. Bấm nút 'Tìm kiếm'",
     "Ô tìm nhanh: 00025",
     "- Lưới còn các phiếu có mã chứa 00025\n- Dòng đếm cập nhật theo số kết quả"),

    ("002", "Ô tìm nhanh KHÔNG tự tìm khi đang gõ", "P0",
     "Danh sách đang hiện 1.328 phiếu.",
     "1. Gõ '00025' vào ô tìm nhanh\n2. Chờ 5 giây, KHÔNG bấm nút\n3. Quan sát lưới",
     "Ô tìm nhanh: 00025",
     "- Lưới KHÔNG đổi\n- Chỉ khi bấm 'Tìm kiếm' danh sách mới lọc lại"),

    ("003", "Lọc theo mã phiếu đề nghị chi", "P0",
     "Có 1 phiếu chi lập từ phiếu đề nghị TPE.DNTT0826.00017.",
     "1. Mở 'Tìm kiếm nâng cao'\n2. Gõ 'TPE.DNTT0826.00017' vào ô 'Mã phiếu đề nghị chi'",
     "Mã phiếu đề nghị chi: TPE.DNTT0826.00017",
     "- ⚠️ Lưới tự lọc ngay khi gõ xong, không cần bấm nút\n"
     "- Kết quả có đúng phiếu chi gắn với phiếu đề nghị đó"),

    ("004", "Danh sách Loại chi trong ô lọc", "P0",
     "Tài khoản C.",
     "1. Mở 'Tìm kiếm nâng cao'\n2. Bấm vào ô Loại chi",
     "—",
     "- Danh sách có đủ 7 giá trị: Chi trả nhà cung cấp, Chi trả lại khách hàng, Chi thưởng "
     "NVKD, Chi thu nhập cho nhân viên, Chi thưởng thực hiện hợp đồng, Chi khác, Thanh toán chi "
     "phí vận chuyển NCC"),

    ("005", "Lọc theo Loại chi", "P0",
     "Phạm vi quyền có 708 phiếu 'Chi trả nhà cung cấp' và 116 phiếu 'Chi thu nhập cho nhân viên'.",
     "1. Mở 'Tìm kiếm nâng cao'\n2. Chọn Loại chi = 'Chi thu nhập cho nhân viên'",
     "Loại chi: Chi thu nhập cho nhân viên",
     "- Lưới còn 116 dòng, cột Loại chi của mọi dòng đều đúng giá trị đã chọn\n"
     "- ⚠️ Cột 'Mã phiếu đề nghị chi' của các dòng này hiện dấu gạch ngang (loại này không lập "
     "từ đề nghị)"),

    ("006", "Danh sách trạng thái trong ô lọc", "P1",
     "Tài khoản C.",
     "1. Mở 'Tìm kiếm nâng cao'\n2. Bấm vào ô Trạng thái",
     "—",
     "- Danh sách có đúng 5 giá trị: Đang tạo, Chờ chi tiền, Đã duyệt, Hủy, Chờ KT trưởng duyệt"),

    ("007", "Lọc theo Trạng thái", "P0",
     "Phạm vi quyền có 1.294 phiếu 'Đã duyệt' và 2 phiếu 'Chờ chi tiền'.",
     "1. Mở 'Tìm kiếm nâng cao'\n2. Chọn Trạng thái = 'Chờ chi tiền'",
     "Trạng thái: Chờ chi tiền",
     "- Lưới còn 2 dòng, cột Trạng thái của mọi dòng đều ghi 'Chờ chi tiền'"),

    ("008", "Lọc Trạng thái = Đang tạo chỉ ra nháp của chính mình", "P0",
     "Tài khoản C có quyền xem tổng công ty, tự lập 1 phiếu nháp; toàn hệ thống có 7 phiếu nháp.",
     "1. Lọc Trạng thái = 'Đang tạo'\n2. Đếm kết quả và xem cột Người tạo",
     "Trạng thái: Đang tạo",
     "- ⚠️ Chỉ ra 1 phiếu, không phải 7\n- Cột Người tạo là tên C"),

    ("009", "Lọc theo Người lập và Người đề nghị", "P1",
     "Có 12 phiếu do C lập; có 5 phiếu lập từ đề nghị của 'Vũ Thị Nhài'.",
     "1. Chọn Người lập = tên C, đếm kết quả\n"
     "2. Xóa điều kiện, chọn Người đề nghị = 'Vũ Thị Nhài', đếm kết quả",
     "—",
     "- Bước 1 ra 12 phiếu, cột Người tạo đều là C\n"
     "- Bước 2 ra 5 phiếu, cột Người đề nghị đều là Vũ Thị Nhài\n"
     "- ⚠️ Hai ô lọc khác nhau: Người lập là người lập PHIẾU CHI, Người đề nghị là người lập "
     "PHIẾU ĐỀ NGHỊ"),

    ("010", "Lọc theo Phòng ban", "P1",
     "Có 8 phiếu thuộc 'PHÒNG XUẤT NHẬP KHẨU'.",
     "1. Mở 'Tìm kiếm nâng cao'\n2. Chọn Phòng ban = 'PHÒNG XUẤT NHẬP KHẨU'",
     "Phòng ban: PHÒNG XUẤT NHẬP KHẨU",
     "- Lưới còn 8 dòng, cột Phòng ban đều đúng giá trị đã chọn"),

    ("011", "Lọc theo Khách hàng / Nhà cung cấp", "P0",
     "Có 3 phiếu chi cho nhà cung cấp 'ZELL - HAINING ZELL AUTOMOBILE TESTING'.",
     "1. Mở 'Tìm kiếm nâng cao'\n"
     "2. Gõ ít nhất 2 ký tự vào ô 'Khách hàng / Nhà cung cấp' rồi chọn trong danh sách gợi ý",
     "Khách hàng / Nhà cung cấp: ZELL",
     "- Ô này gộp chung nguồn khách hàng và nhà cung cấp\n"
     "- Lưới còn 3 dòng có dòng chi tiết gắn đối tượng đó"),

    ("012", "Lọc khoảng Số tiền", "P0",
     "Có 4 phiếu có Số tiền từ 100.000.000 đến 300.000.000.",
     "1. Nhập 'Số tiền từ' = 100.000.000\n2. Nhập 'Số tiền đến' = 300.000.000",
     "Số tiền từ: 100.000.000 · Số tiền đến: 300.000.000",
     "- Lưới còn 4 dòng, cột Số tiền đều nằm trong khoảng"),

    ("013", "Lọc khoảng ngày lập", "P0",
     "Có 9 phiếu lập trong tháng 8/2026.",
     "1. Chọn 'Ngày lập từ' = 01/08/2026\n2. Chọn 'Ngày lập đến' = 31/08/2026",
     "01/08/2026 – 31/08/2026",
     "- Lưới chỉ còn phiếu có Ngày tạo trong tháng 8/2026"),

    ("014", "Mốc 'Ngày lập đến' lấy trọn ngày", "P0",
     "Có 1 phiếu lập lúc 14:58 ngày 28/08/2026.",
     "1. Chọn 'Ngày lập đến' = 28/08/2026, để trống ô còn lại\n"
     "2. Tìm phiếu lập lúc 14:58 trong kết quả",
     "Ngày lập đến: 28/08/2026",
     "- ⚠️ Phiếu lập lúc 14:58 ngày 28/08/2026 VẪN nằm trong kết quả"),

    ("015", "Kết hợp nhiều điều kiện lọc", "P0",
     "Tài khoản C; có 2 phiếu 'Hủy' loại 'Chi trả nhà cung cấp' lập trong tháng 8/2026.",
     "1. Chọn Trạng thái = 'Hủy'\n"
     "2. Chọn Loại chi = 'Chi trả nhà cung cấp'\n"
     "3. Chọn khoảng ngày lập 01/08/2026 – 31/08/2026",
     "3 điều kiện như trên",
     "- Các điều kiện cộng dồn (VÀ), kết quả còn 2 phiếu thoả tất cả\n"
     "- Mỗi lần đổi một ô, lưới tự nạp lại"),

    ("016", "Nút 'Làm mới' xóa hết điều kiện lọc", "P0",
     "Đang lọc Trạng thái = 'Hủy' và ô tìm nhanh có chữ.",
     "1. Bấm nút 'Làm mới'\n2. Quan sát các ô lọc và lưới",
     "—",
     "- Tất cả ô lọc và ô tìm nhanh trở về trống\n"
     "- Lưới nạp lại đầy đủ theo phạm vi quyền, quay về trang 1\n"
     "- ⚠️ Phạm vi dữ liệu theo quyền KHÔNG đổi"),

    ("017", "Đổi điều kiện lọc khi đang ở trang 5", "P0",
     "Đang xem trang 5 của danh sách 1.328 phiếu.",
     "1. Chuyển tới trang 5\n2. Chọn Trạng thái = 'Chờ chi tiền'",
     "Trạng thái: Chờ chi tiền",
     "- Danh sách nhảy về TRANG 1 của kết quả mới\n- Không bị trang trắng"),

    ("018", "Cài đặt bộ lọc — bỏ bớt ô lọc hiển thị", "P1",
     "Khối lọc nâng cao đang có 9 nhóm ô.",
     "1. Bấm 'Cài đặt bộ lọc'\n2. Bỏ tích 'Phòng ban' và 'Khoảng ngày lập'\n3. Bấm 'Lưu'",
     "Bỏ tích 2 nhóm ô",
     "- Popup đóng, khối lọc nâng cao còn 7 nhóm ô\n"
     "- Rời màn rồi quay lại vẫn giữ cấu hình này"),

    ("019", "Cài đặt bộ lọc — khôi phục mặc định", "P2",
     "Đã bỏ tích 2 nhóm ô ở trường hợp trên.",
     "1. Bấm 'Cài đặt bộ lọc'\n2. Bấm 'Khôi phục mặc định' rồi 'Lưu'",
     "—",
     "- Khối lọc nâng cao trở lại đủ 9 nhóm ô theo thứ tự ban đầu"),

    ("020", "Bộ lọc không phá vỡ phạm vi quyền", "P0",
     "Tài khoản A chỉ thấy 5 phiếu; hệ thống có 12 phiếu do 'DNS Admin' lập nhưng đều ngoài phạm "
     "vi của A.",
     "1. Đăng nhập tài khoản A\n2. Chọn Người lập = 'DNS Admin'",
     "Người lập: DNS Admin",
     "- ⚠️ Kết quả RỖNG — lọc không mở rộng phạm vi dữ liệu ra ngoài quyền của A"),

    ("021", "Tìm từ khoá không khớp gì", "P1",
     "Tài khoản C.",
     "1. Gõ 'zzzz-khong-ton-tai' vào ô tìm nhanh rồi bấm 'Tìm kiếm'",
     "Ô tìm nhanh: zzzz-khong-ton-tai",
     "- Lưới hiện 'Không có dữ liệu phù hợp bộ lọc.'\n- Không báo lỗi"),
]

S3 = [
    ("001", "Sắp xếp theo Mã phiếu", "P0",
     "Danh sách đang ở thứ tự mặc định.",
     "1. Bấm vào tiêu đề cột 'Mã phiếu'\n2. Ghi lại thứ tự\n3. Bấm lần nữa",
     "—",
     "- Lần 1: mã sắp tăng dần; lần 2 đảo thành giảm dần\n"
     "- Danh sách quay về trang 1 sau mỗi lần đổi sắp xếp"),

    ("002", "Sắp xếp theo Số tiền", "P0",
     "Danh sách có phiếu nhiều mức tiền khác nhau.",
     "1. Bấm tiêu đề cột 'Số tiền'\n2. Kiểm tra dòng đầu và dòng cuối trang",
     "—",
     "- Số tiền sắp tăng dần; bấm lần nữa thì giảm dần"),

    ("003", "Sắp xếp theo Ngày tạo, Ngày cập nhật và Trạng thái", "P0",
     "Danh sách đủ 5 trạng thái.",
     "1. Bấm lần lượt tiêu đề 3 cột: Ngày tạo, Ngày cập nhật, Trạng thái\n"
     "2. Kiểm tra thứ tự sau mỗi lần bấm",
     "—",
     "- Cả 3 cột đều sắp xếp được thật, cả hai chiều\n"
     "- Giờ phút cũng được tính vào thứ tự với 2 cột ngày"),

    ("004", "Chuyển trang không làm mất bộ lọc", "P0",
     "Đang lọc Trạng thái = 'Đã duyệt', kết quả 1.294 phiếu.",
     "1. Bấm sang trang 10\n2. Kiểm tra cột Trạng thái và ô lọc",
     "—",
     "- Mọi dòng vẫn là 'Đã duyệt'\n"
     "- Ô lọc Trạng thái vẫn giữ giá trị, không nhảy về trang 1"),

    ("005", "Đổi số dòng/trang", "P0",
     "Đang xem 10 dòng/trang trên 1.328 phiếu.",
     "1. Đổi 'Số dòng/trang' sang 50",
     "Số dòng/trang: 50",
     "- Lưới hiện 50 dòng, dòng đếm cập nhật\n- Danh sách quay về trang 1"),

    ("006", "STT đánh số theo trang", "P1",
     "Đang xem 10 dòng/trang.",
     "1. Sang trang 2\n2. Đọc cột STT dòng đầu và dòng cuối",
     "—",
     "- STT trang 2 chạy từ 11 đến 20"),

    ("007", "Mã phiếu là đường dẫn sang màn chi tiết", "P0",
     "Danh sách có phiếu TPE.PC0826.00025.",
     "1. Bấm vào chữ 'TPE.PC0826.00025' ở cột Mã phiếu",
     "—",
     "- Chuyển sang màn chi tiết đúng phiếu đó\n"
     "- Tiêu đề màn ghi 'Chi tiết phiếu chi: TPE.PC0826.00025'"),

    ("008", "Mã phiếu đề nghị chi mở màn phiếu đề nghị", "P1",
     "Danh sách có phiếu gắn đề nghị TPE.DNTT0826.00017.",
     "1. Bấm vào chữ 'TPE.DNTT0826.00017' ở cột Mã phiếu đề nghị chi",
     "—",
     "- Mở màn chi tiết Phiếu đề nghị thanh toán tương ứng"),

    ("009", "Màu nhãn trạng thái phân biệt được 5 trạng thái", "P1",
     "Danh sách có cả 5 trạng thái.",
     "1. Quan sát cột Trạng thái",
     "—",
     "- 'Đang tạo' nhãn xám, 'Chờ chi tiền' và 'Chờ KT trưởng duyệt' nhãn vàng, 'Đã duyệt' nhãn "
     "xanh, 'Hủy' nhãn đỏ\n"
     "- ⚠️ Đây là điểm cải tiến so với cổng cũ (cổng cũ để cùng một màu đỏ cho 4 trạng thái, "
     "không phân biệt được 'đang chờ' với 'đã hủy')"),

    ("010", "Nút thao tác trên dòng đổi theo trạng thái và quyền", "P0",
     "Tài khoản F (thủ quỹ kiêm kế toán thanh toán) có: 1 phiếu 'Đang tạo' do mình lập, 1 phiếu "
     "'Chờ chi tiền', 1 phiếu 'Đã duyệt', 1 phiếu 'Hủy'.",
     "1. Kéo lưới sang phải để thấy cột Hành động\n2. Quan sát cả 4 dòng",
     "—",
     "- Dòng 'Đang tạo': nút Sửa (bút chì), Xóa (thùng rác đỏ) và menu ba chấm\n"
     "- Dòng 'Chờ chi tiền': nút In, Xuất Excel và menu ba chấm chứa nút Duyệt\n"
     "- Dòng 'Đã duyệt' và 'Hủy': chỉ In, Xuất Excel, Lịch sử\n"
     "- ⚠️ Nút không đủ điều kiện bị ẩn hẳn\n"
     "- ⚠️ Danh sách KHÔNG có nút 'Hủy phiếu' — hủy chỉ làm ở màn chi tiết"),

    ("011", "Nút Duyệt trên dòng chỉ điều hướng", "P1",
     "Tài khoản F, có phiếu 'Chờ chi tiền'.",
     "1. Bấm nút Duyệt (dấu tích tròn) trên dòng phiếu\n2. Quan sát",
     "—",
     "- ⚠️ Chỉ MỞ màn chi tiết, KHÔNG duyệt ngay\n"
     "- Phiếu vẫn ở trạng thái Chờ chi tiền"),

    ("012", "Cấu hình cột — ẩn bớt cột và 3 cột bị khoá", "P1",
     "Lưới đang hiện đủ 14 cột.",
     "1. Bấm nút biểu tượng cấu hình cột\n"
     "2. Bỏ tích 'Người cập nhật' và 'Ngày cập nhật'\n"
     "3. Thử bỏ tích 'STT', 'Mã phiếu', 'Hành động'\n"
     "4. Bấm 'Lưu'",
     "—",
     "- Hai cột cập nhật bị ẩn khỏi lưới\n"
     "- Ba cột STT, Mã phiếu, Hành động hiện biểu tượng ổ khoá, chữ mờ, không bỏ tích được\n"
     "- Rời màn rồi quay lại vẫn giữ cấu hình này"),

    ("013", "Cấu hình cột của màn này không ảnh hưởng màn khác", "P2",
     "Đã ẩn 2 cột ở màn Phiếu chi.",
     "1. Mở màn 'Phiếu thu'\n2. Quan sát các cột",
     "—",
     "- Màn kia giữ nguyên cấu hình cột riêng"),
]

S4 = [
    ("001", "Mở màn Tạo mới — giá trị điền sẵn", "P0",
     "Tài khoản E có quyền 'Kế toán thanh toán', thuộc PHÒNG THIẾT BỊ Ô TÔ 3.",
     "1. Bấm nút 'Tạo mới'\n2. Quan sát khối 'Thông tin chung'",
     "—",
     "- Tiêu đề màn: 'Thêm phiếu chi tiền'\n"
     "- 'Số phiếu đề nghị' trống, ghi gợi ý 'Nhấn vào đây để chọn phiếu đề nghị chi'\n"
     "- 'Tài khoản có' và 'Loại chi' trống, cả hai có dấu sao đỏ\n"
     "- 'Hình thức thanh toán' điền sẵn TM\n"
     "- 'Người nhận' trống, có dấu sao đỏ\n"
     "- 'Loại tiền' điền sẵn VietNamDong, 'Tỷ giá (VND)' điền sẵn 1\n"
     "- 'Người đề nghị' và 'Phòng ban' điền sẵn theo người đang đăng nhập\n"
     "- Khối Chi tiết hiện dòng đỏ 'Chưa chọn phiếu đề nghị chi'\n"
     "- Cuối trang có 3 nút: 'Lưu nháp', 'Lưu và gửi duyệt', 'Quay lại'"),

    ("002", "Danh sách Loại chi trên form", "P0",
     "Đang ở màn Tạo mới.",
     "1. Bấm vào ô 'Loại chi'",
     "—",
     "- Danh sách có đủ 7 giá trị, giống ô lọc ở màn danh sách"),

    ("003", "Hình thức thanh toán có 2 lựa chọn", "P1",
     "Đang ở màn Tạo mới.",
     "1. Bấm vào ô 'Hình thức thanh toán'",
     "Hình thức thanh toán: TM / CK",
     "- Danh sách có đúng 2 giá trị: TM (tiền mặt) và CK (chuyển khoản)"),

    ("004", "Chọn Loại chi thuộc nhóm lập-từ-đề-nghị", "P0",
     "Đang ở màn Tạo mới.",
     "1. Chọn Loại chi = 'Chi trả nhà cung cấp'\n2. Quan sát form",
     "Loại chi: Chi trả nhà cung cấp",
     "- Ô 'Số phiếu đề nghị' vẫn hiện và bấm được\n"
     "- KHÔNG có ô 'Phòng ban chi'\n"
     "- Khối Chi tiết vẫn báo 'Chưa chọn phiếu đề nghị chi'"),

    ("005", "Chọn Loại chi = Chi thu nhập cho nhân viên", "P0",
     "Đang ở màn Tạo mới.",
     "1. Chọn Loại chi = 'Chi thu nhập cho nhân viên'\n2. Quan sát form",
     "Loại chi: Chi thu nhập cho nhân viên",
     "- ⚠️ Ô 'Số phiếu đề nghị' BIẾN MẤT — loại này không lập từ đề nghị\n"
     "- Xuất hiện ô 'Phòng ban chi' có dấu sao đỏ\n"
     "- Ô 'Lý do chi' có thêm dấu sao đỏ (bắt buộc)\n"
     "- Khối Chi tiết báo 'Chưa chọn phòng ban chi — chọn phòng ban để hệ thống lấy số liệu thu "
     "nhập nhân viên.'"),

    ("006", "Cửa sổ chọn phiếu đề nghị chi", "P0",
     "Hệ thống có 76 phiếu đề nghị thanh toán đang Chờ tạo phiếu chi và chưa có phiếu chi.",
     "1. Chọn Loại chi = 'Chi trả nhà cung cấp'\n2. Bấm vào ô 'Số phiếu đề nghị'",
     "—",
     "- Cửa sổ 'Chọn phiếu đề nghị chi', phụ đề đỏ 'Chỉ phiếu Chờ tạo phiếu chi và chưa lập "
     "phiếu chi'\n"
     "- Có 3 ô tìm: 'Mã phiếu đề nghị', 'Loại chi', 'Người lập', kèm nút 'Tìm kiếm' và 'Làm mới'\n"
     "- Bảng có 7 cột: STT, Mã phiếu đề nghị, Loại chi, Khách hàng / Nhà cung cấp, Số tiền, "
     "Người lập, Ngày lập\n"
     "- Dòng đếm ghi 'Hiển thị 1–10 / 76 phiếu'"),

    ("007", "Cửa sổ chỉ liệt kê phiếu đề nghị đủ điều kiện", "P0",
     "Phiếu đề nghị X đang Chờ tạo phiếu chi và chưa có phiếu chi; phiếu Y đã có phiếu chi; "
     "phiếu Z chưa gửi duyệt.",
     "1. Mở cửa sổ chọn phiếu đề nghị\n2. Tìm lần lượt mã của X, Y, Z",
     "—",
     "- Chỉ X xuất hiện\n"
     "- ⚠️ Y không xuất hiện dù vẫn ở Chờ tạo phiếu chi — vì đã có phiếu chi\n"
     "- Z không xuất hiện vì chưa gửi duyệt"),

    ("008", "Chọn phiếu đề nghị — dữ liệu tự kéo về", "P0",
     "Phiếu đề nghị TPE.DNTT0826.00018 loại 'Chi trả nhà cung cấp', 1 dòng chi tiết, loại tiền "
     "CHECK, tỷ giá 2.564, hình thức CK.",
     "1. Bấm vào dòng TPE.DNTT0826.00018 trong cửa sổ\n2. Quan sát toàn màn",
     "—",
     "- Cửa sổ tự đóng, ô 'Số phiếu đề nghị' hiện mã vừa chọn\n"
     "- Hình thức thanh toán, Loại tiền, Tỷ giá, Lý do chi tự điền theo phiếu đề nghị\n"
     "- Xuất hiện khối thông tin nhà cung cấp và ngân hàng nhận tiền (Số tài khoản, Tên tài "
     "khoản, Tên ngân hàng, Chi nhánh, Thành phố)\n"
     "- Bảng Chi tiết nạp đúng 1 dòng, có dòng 'Tổng cộng'\n"
     "- ⚠️ Vì là ngoại tệ nên mỗi nhóm tiền có 2 cột: cột nguyên tệ và cột VND"),

    ("009", "Khối ngân hàng chỉ hiện với hình thức chuyển khoản", "P0",
     "Có phiếu đề nghị hình thức TM và phiếu đề nghị hình thức CK.",
     "1. Chọn phiếu đề nghị hình thức CK, quan sát form\n"
     "2. Đổi sang phiếu đề nghị hình thức TM, quan sát lại",
     "—",
     "- Hình thức CK: có khối 'NGÂN HÀNG NHẬN TIỀN' và 'NGÂN HÀNG TRUNG GIAN' (Ngân hàng, Số "
     "tài khoản, Tài khoản, Tên ngân hàng, Swift Code, IBAN Number, Địa chỉ)\n"
     "- ⚠️ Hình thức TM: hai khối này KHÔNG hiện"),

    ("010", "Chọn Phòng ban chi để nạp số liệu thu nhập nhân viên", "P0",
     "Loại chi = 'Chi thu nhập cho nhân viên'. Phòng 'PHÒNG THIẾT BỊ Ô TÔ 1' có số liệu thu nhập "
     "của 5 nhân viên.",
     "1. Chọn Phòng ban chi = 'PHÒNG THIẾT BỊ Ô TÔ 1'\n2. Quan sát bảng Chi tiết",
     "Phòng ban chi: PHÒNG THIẾT BỊ Ô TÔ 1",
     "- Bảng nạp 5 dòng, mỗi dòng là MỘT nhân viên\n"
     "- Bảng có 2 tab: 'Chi tiết' và 'Chi tiết vụ việc'\n"
     "- Cột: ô tích chọn, STT, Số tài khoản nợ (có dấu sao), Tên tài khoản, Nhân viên, Số dư, "
     "Số tiền chi (có dấu sao)\n"
     "- Mọi dòng được tích chọn sẵn, Số tài khoản nợ điền sẵn\n"
     "- Có dòng 'Tổng cộng' cuối bảng"),

    ("011", "Phòng ban không có số liệu thu nhập", "P1",
     "Loại chi = 'Chi thu nhập cho nhân viên'. Phòng 'BAN GIÁM ĐỐC' không có số liệu.",
     "1. Chọn Phòng ban chi = 'BAN GIÁM ĐỐC'\n2. Quan sát bảng Chi tiết",
     "Phòng ban chi: BAN GIÁM ĐỐC",
     "- Bảng hiện dòng đỏ 'Không có dữ liệu phù hợp'\n- Không báo lỗi hệ thống"),

    ("012", "Số dư nhân viên được phép ÂM", "P0",
     "Phòng 'PHÒNG THIẾT BỊ Ô TÔ 1' có nhân viên với số dư âm (ví dụ -571.120).",
     "1. Chọn phòng ban đó\n2. Quan sát cột 'Số dư'",
     "—",
     "- ⚠️ Cột Số dư hiển thị đúng giá trị âm, không bị chặn hay quy về 0\n"
     "- Dòng đó vẫn nhập được số tiền chi (trường hợp truy thu)"),

    ("013", "Bỏ tích một dòng nhân viên", "P1",
     "Bảng thu nhập nhân viên đang có 5 dòng, tất cả đều tích.",
     "1. Bỏ tích dòng số 3\n2. Quan sát dòng 'Tổng cộng'",
     "—",
     "- Dòng 3 bị loại khỏi phiếu, Tổng cộng giảm tương ứng\n"
     "- Ô tích ở tiêu đề bảng chuyển sang trạng thái chọn một phần"),

    ("014", "Lưu nháp KHÔNG bắt buộc trường nào (trừ Loại chi)", "P0",
     "Màn Tạo mới, chỉ chọn Loại chi, để trống mọi ô khác.",
     "1. Chọn Loại chi = 'Chi khác'\n2. Bấm 'Lưu nháp'",
     "Chỉ chọn Loại chi",
     "- ⚠️ Lưu THÀNH CÔNG, thông báo 'Thêm phiếu chi tiền thành công!'\n"
     "- Phiếu mới ở trạng thái 'Đang tạo'\n"
     "- Đây là điểm khác cổng cũ có chủ đích: cổng cũ bắt buộc đủ trường cho cả nút Lưu"),

    ("015", "Lưu nháp KHÔNG chọn Loại chi", "P0",
     "Màn Tạo mới, chưa chọn Loại chi.",
     "1. Bấm 'Lưu nháp'",
     "Loại chi: (trống)",
     "- Không lưu được\n- Hiện lỗi đỏ dưới ô Loại chi: 'Bắt buộc chọn loại chi'"),

    ("016", "Lưu và gửi duyệt — có hộp xác nhận", "P0",
     "Form đã điền đủ thông tin hợp lệ.",
     "1. Bấm nút 'Lưu và gửi duyệt'\n2. Đọc hộp thoại\n3. Bấm 'Xác nhận'",
     "—",
     "- Hộp 'Xác nhận lưu và gửi duyệt' hỏi 'Bạn đồng ý lưu và duyệt?'\n"
     "- Sau khi xác nhận, phiếu được lưu rồi gửi duyệt luôn\n"
     "- Phiếu nhóm lập-từ-đề-nghị chuyển sang 'Chờ chi tiền'\n"
     "- Phiếu loại 'Chi thu nhập cho nhân viên' chuyển sang 'Chờ KT trưởng duyệt'"),

    ("017", "Gửi duyệt thiếu trường bắt buộc — nhóm lập-từ-đề-nghị", "P0",
     "Đã chọn Loại chi = 'Chi trả nhà cung cấp' và chọn phiếu đề nghị, nhưng để trống Người nhận "
     "và Tài khoản nợ của dòng chi tiết.",
     "1. Bấm 'Lưu và gửi duyệt' rồi 'Xác nhận'\n2. Quan sát các ô",
     "—",
     "- Không lưu được\n"
     "- Ô 'Người nhận' viền đỏ, dưới ô hiện 'Bắt buộc nhập người nhận'\n"
     "- Ô 'Tài khoản nợ' của dòng chi tiết viền đỏ, dưới ô hiện 'Bắt buộc chọn tài khoản nợ'\n"
     "- ⚠️ Màn hình không đóng, mọi dữ liệu đã nhập vẫn còn"),

    ("018", "Gửi duyệt thiếu phiếu đề nghị — chỉ 3 loại bị bắt buộc", "P0",
     "Chuẩn bị 2 phiếu: phiếu P1 loại 'Chi trả nhà cung cấp', phiếu P2 loại 'Chi khác'. Cả hai "
     "đều trống Số phiếu đề nghị và trống dòng chi tiết, đã điền các ô còn lại.",
     "1. Với P1: bấm 'Lưu và gửi duyệt'\n2. Với P2: bấm 'Lưu và gửi duyệt'",
     "—",
     "- P1 bị chặn: 'Bắt buộc chọn phiếu đề nghị thanh toán' và 'Bắt buộc nhập chi tiết phiếu chi'\n"
     "- ⚠️ P2 gửi duyệt THÀNH CÔNG dù trống cả hai — 3 loại Chi thưởng thực hiện hợp đồng, Chi "
     "khác, Thanh toán chi phí vận chuyển NCC không bị bắt buộc\n"
     "- Đây là quyết định nghiệp vụ đã chốt, KHÔNG phải sót kiểm tra"),

    ("019", "Gửi duyệt thiếu trường bắt buộc — luồng Chi thu nhập nhân viên", "P0",
     "Loại chi = 'Chi thu nhập cho nhân viên', để trống Phòng ban chi và Lý do chi.",
     "1. Bấm 'Lưu và gửi duyệt' rồi 'Xác nhận'",
     "—",
     "- Không lưu được\n"
     "- Lỗi 'Bắt buộc chọn phòng ban được chi' dưới ô Phòng ban chi\n"
     "- Lỗi 'Bắt buộc nhập lý do chi' dưới ô Lý do chi\n"
     "- Nếu chưa nạp dòng nào thì thêm lỗi 'Bắt buộc nhập chi tiết phiếu chi'"),

    ("020", "Số tiền chi vượt số tiền đề nghị chi", "P0",
     "Dòng chi tiết có Số tiền đề nghị chi = 50.000.",
     "1. Nhập 'Số tiền chi' dòng đó = 90.000\n2. Bấm 'Lưu và gửi duyệt' rồi 'Xác nhận'",
     "Số tiền chi: 90.000",
     "- Bị chặn, hiện lỗi 'Không được lớn hơn số tiền đề nghị chi'\n"
     "- Phiếu không được lưu\n"
     "- ⚠️ Đây là lớp kiểm tra bổ sung so với cổng cũ (cổng cũ tự kẹp số về, không báo)"),

    ("021", "Số tiền chi âm", "P1",
     "Dòng chi tiết đã có số tiền đề nghị chi.",
     "1. Thử nhập số âm vào ô 'Số tiền chi'\n2. Bấm 'Lưu và gửi duyệt'",
     "Số tiền chi: -1000",
     "- Ô không nhận dấu trừ; nếu lọt thì hệ thống báo 'Số tiền duyệt chi không được âm'"),

    ("022", "Tỷ giá không phải số", "P1",
     "Phiếu ngoại tệ, ô Tỷ giá đang mở.",
     "1. Gõ 'abc' vào ô Tỷ giá\n2. Bấm 'Lưu và gửi duyệt'",
     "Tỷ giá: abc",
     "- Ô không nhận chữ; nếu lọt thì hệ thống báo 'Tỷ giá phải là số'"),

    ("023", "Người nhận quá 255 ký tự", "P1",
     "Màn Tạo mới, đã chọn Loại chi.",
     "1. Dán 300 ký tự vào ô 'Người nhận'\n2. Bấm 'Lưu và gửi duyệt'",
     "Chuỗi 300 ký tự",
     "- Hệ thống báo 'Người nhận tối đa 255 ký tự'\n- Phiếu không được gửi duyệt"),

    ("024", "Một phiếu đề nghị chỉ lập được một phiếu chi", "P0",
     "Phiếu đề nghị X đã có 1 phiếu chi (kể cả phiếu chi còn ở trạng thái nháp).",
     "1. Bấm 'Tạo mới', mở cửa sổ chọn phiếu đề nghị\n2. Tìm mã X",
     "—",
     "- Không tìm thấy — phiếu đề nghị đã bị loại khỏi danh sách chọn\n"
     "- Nếu ép lưu bằng cách khác thì hệ thống chặn và không tạo phiếu thứ hai"),

    ("025", "Hai người cùng lập phiếu chi cho một phiếu đề nghị", "P0",
     "Hai kế toán E1 và E2 cùng mở màn Tạo mới, cùng chọn phiếu đề nghị X.",
     "1. E1 bấm 'Lưu nháp' thành công\n2. E2 (chưa tải lại) bấm 'Lưu nháp'",
     "—",
     "- E2 bị chặn, không tạo được phiếu thứ hai\n"
     "- ⚠️ Chỉ có ĐÚNG MỘT phiếu chi được tạo cho phiếu đề nghị X"),

    ("026", "Chống bấm nút lưu hai lần", "P1",
     "Form đã điền đủ thông tin.",
     "1. Bấm 'Lưu nháp' rồi bấm liên tiếp thêm 2 lần thật nhanh\n2. Về danh sách đếm phiếu",
     "—",
     "- Chỉ tạo ra ĐÚNG 1 phiếu"),

    ("027", "Mã phiếu sinh tự động theo công ty và tháng", "P1",
     "Người lập thuộc công ty có mã 'TPE'; hôm nay là tháng 09/2026.",
     "1. Lập và lưu 1 phiếu mới\n2. Đọc mã phiếu vừa tạo",
     "—",
     "- Mã có dạng TPE.PC0926.00001 (mã công ty + PC + tháng năm + 5 chữ số)\n"
     "- Người dùng KHÔNG nhập được mã; ô Mã phiếu chỉ hiện ở màn Sửa và Xem, ở chế độ chỉ đọc"),

    ("028", "Cảnh báo khi rời form đang nhập dở", "P1",
     "Form Tạo mới đã chọn Loại chi và nhập Người nhận, chưa lưu.",
     "1. Bấm nút 'Quay lại' hoặc chuyển sang màn khác",
     "—",
     "- Hiện cảnh báo còn thông tin chưa lưu\n"
     "- Chọn ở lại thì dữ liệu còn nguyên; chọn thoát thì mất dữ liệu đang nhập"),
]

S5 = [
    ("001", "Mở màn Sửa từ danh sách", "P0",
     "Tài khoản E có phiếu TPE.PC0826.00030 ở trạng thái 'Đang tạo' do chính mình lập.",
     "1. Kéo lưới sang phải, bấm nút Sửa (bút chì) trên dòng phiếu\n2. Quan sát form",
     "—",
     "- Tiêu đề màn: 'Sửa phiếu chi tiền'\n"
     "- Có THÊM ô 'Mã phiếu', 'Người lập', 'Ngày lập' so với màn Tạo mới, cả ba chỉ đọc\n"
     "- Các ô còn lại nạp đúng dữ liệu đã lưu, bảng Chi tiết nạp đủ dòng"),

    ("002", "Sửa và lưu nháp lại", "P0",
     "Đang ở màn Sửa phiếu nháp.",
     "1. Sửa ô 'Người nhận' và ô 'Lý do chi'\n2. Bấm 'Lưu nháp'\n3. Mở lại phiếu kiểm tra",
     "Người nhận: Trần Thị B",
     "- Thông báo 'Cập nhật phiếu chi tiền thành công!'\n"
     "- Phiếu vẫn ở trạng thái 'Đang tạo'\n"
     "- Cột 'Người cập nhật' và 'Ngày cập nhật' trên lưới đổi theo người vừa sửa"),

    ("003", "Sửa rồi gửi duyệt luôn", "P0",
     "Đang ở màn Sửa phiếu nháp thuộc nhóm lập-từ-đề-nghị, đã điền đủ.",
     "1. Bấm 'Lưu và gửi duyệt' rồi 'Xác nhận'",
     "—",
     "- Phiếu chuyển sang 'Chờ chi tiền', mất nút Sửa/Xóa\n"
     "- Thủ quỹ cùng công ty nhận thông báo"),

    ("004", "Đổi Loại chi khi sửa — đổi luôn cấu trúc form", "P1",
     "Đang sửa phiếu nháp loại 'Chi trả nhà cung cấp'.",
     "1. Đổi Loại chi sang 'Chi thu nhập cho nhân viên'\n2. Quan sát form",
     "—",
     "- Ô 'Số phiếu đề nghị' biến mất, xuất hiện ô 'Phòng ban chi'\n"
     "- Bảng Chi tiết đổi sang bảng thu nhập nhân viên, dữ liệu cũ bị thay"),

    ("005", "Không sửa được phiếu đã gửi duyệt", "P0",
     "Phiếu TPE.PC0826.00025 do chính mình lập, đang ở 'Chờ chi tiền'.",
     "1. Kéo lưới sang phải quan sát cột Hành động\n"
     "2. Gõ thẳng đường dẫn màn Sửa của phiếu này lên thanh địa chỉ",
     "—",
     "- Trên lưới KHÔNG có nút Sửa\n"
     "- Gõ đường dẫn thì hệ thống chặn và đưa về danh sách"),

    ("006", "Không sửa được phiếu đã duyệt hoặc đã hủy", "P0",
     "Phiếu P1 'Đã duyệt' và phiếu P2 'Hủy'.",
     "1. Mở màn chi tiết từng phiếu\n2. Quan sát các nút cuối màn",
     "—",
     "- Cả hai đều KHÔNG có nút 'Sửa' và 'Xóa'\n"
     "- Chỉ còn 'In', 'Xuất Excel', 'Quay lại'"),

    ("007", "Tài khoản đã khóa trên phiếu cũ vẫn hiện đúng tên", "P0",
     "Phiếu nháp đang gắn tài khoản mà tài khoản đó vừa bị khóa trong danh mục.",
     "1. Mở màn Sửa phiếu này\n2. Quan sát ô tài khoản",
     "—",
     "- ⚠️ Ô vẫn hiện ĐÚNG tên tài khoản đã lưu, không bị trống\n"
     "- Mở danh sách chọn thì tài khoản đã khóa không nằm trong các lựa chọn mới\n"
     "- Lưu lại mà không đụng ô này thì giá trị cũ được giữ nguyên"),
]

S6 = [
    ("001", "Mở màn chi tiết", "P0",
     "Phiếu TPE.PC0826.00025 ở trạng thái 'Chờ chi tiền', loại 'Chi trả nhà cung cấp', hình thức "
     "CK, ngoại tệ USD.",
     "1. Bấm vào mã phiếu trên danh sách\n2. Quan sát toàn màn",
     "—",
     "- Tiêu đề: 'Chi tiết phiếu chi: TPE.PC0826.00025'\n"
     "- Khối 'Thông tin chung' đủ các ô ở chế độ chỉ đọc: Số phiếu đề nghị, Mã phiếu, Tài khoản "
     "có, Loại chi, Hình thức thanh toán, Người nhận, Loại tiền, Tỷ giá (VND), Người đề nghị, "
     "Phòng ban, Người lập, Ngày lập, Lý do chi\n"
     "- Có khối thông tin nhà cung cấp và ngân hàng nhận tiền\n"
     "- Khối 'Chi tiết' có bảng và dòng 'Tổng cộng'\n"
     "- Cuối trang có khối 'Lịch sử' thu gọn kèm nút 'Xem lịch sử'"),

    ("002", "Phiếu đã hủy hiện dải băng lý do hủy", "P0",
     "Phiếu TPE.PC0826.00032 ở trạng thái 'Hủy', đã nhập lý do hủy và ghi chú khi hủy.",
     "1. Mở màn chi tiết phiếu này\n2. Quan sát phần đầu màn",
     "—",
     "- ⚠️ Có dải băng vàng ở ngay đầu màn, hiện 'Lý do hủy: ...' và 'Ghi chú: ...'\n"
     "- Đây là cách duy nhất xem nhanh lý do hủy ngoài Lịch sử"),

    ("003", "Ô trống hiển thị dấu gạch ngang", "P1",
     "Phiếu không có đối tượng nhận tiền và dòng chi tiết không ghi chú.",
     "1. Mở màn chi tiết phiếu đó",
     "—",
     "- Các ô không có dữ liệu hiện dấu gạch ngang, không để trắng trơn"),

    ("004", "Nút cuối màn chi tiết theo trạng thái và quyền", "P0",
     "Tài khoản F (thủ quỹ kiêm kế toán thanh toán): phiếu P1 'Đang tạo' của F; P2 'Chờ chi "
     "tiền'; P3 'Đã duyệt'; P4 'Hủy'.",
     "1. Lần lượt mở chi tiết P1, P2, P3, P4\n2. Ghi lại các nút cuối màn",
     "—",
     "- P1: 'Sửa', 'In', 'Xuất Excel', 'Xóa', 'Quay lại'\n"
     "- P2: 'Duyệt phiếu chi', 'Hủy phiếu chi', 'In', 'Xuất Excel', 'Quay lại'\n"
     "- P3 và P4: 'In', 'Xuất Excel', 'Quay lại'\n"
     "- ⚠️ Thứ tự nút cố định: Sửa · Duyệt · Hủy · In · Xuất Excel · Xóa · Quay lại"),

    ("005", "Mở phiếu bằng mã không tồn tại", "P1",
     "Tài khoản C.",
     "1. Gõ đường dẫn màn chi tiết với mã phiếu không có thật",
     "—",
     "- Hệ thống báo không tìm thấy dữ liệu\n- Không treo trang"),

    ("006", "Nút Quay lại giữ bộ lọc", "P1",
     "Trước đó danh sách đang lọc Trạng thái 'Chờ chi tiền' ở trang 2.",
     "1. Mở một phiếu rồi bấm 'Quay lại'",
     "—",
     "- Về màn danh sách, điều kiện lọc vẫn còn"),
]

S7 = [
    ("001", "Thủ quỹ duyệt phiếu — luồng đầy đủ", "P0",
     "⚠️ CHỈ LÀM TRÊN PHIẾU DO CHÍNH MÌNH TẠO. Tài khoản F là thủ quỹ cùng công ty. Phiếu P "
     "thuộc nhóm lập-từ-đề-nghị, đang ở 'Chờ chi tiền'.",
     "1. Mở màn chi tiết phiếu P\n"
     "2. Bấm 'Duyệt phiếu chi'\n"
     "3. Trong cửa sổ, kiểm tra và điều chỉnh 'Số tiền thực chi' của từng dòng\n"
     "4. Nhập Ghi chú (nếu cần) rồi bấm 'Duyệt'\n"
     "5. Mở lại phiếu và mở phiếu đề nghị tương ứng",
     "Số tiền thực chi = số tiền đề nghị chi",
     "- Cửa sổ 'Duyệt phiếu chi tiền' hiện bảng chi tiết với cột 'Số tiền thực chi' là ô nhập, "
     "có dấu sao đỏ, kèm ô 'Ghi chú'\n"
     "- Sau khi duyệt: thông báo 'Duyệt phiếu chi thành công!'\n"
     "- Phiếu P chuyển sang 'Đã duyệt', ghi người duyệt và ngày hạch toán\n"
     "- Phiếu đề nghị tương ứng chuyển sang trạng thái duyệt phiếu chi\n"
     "- ⚠️ THAO TÁC NÀY KHÔNG HOÀN TÁC ĐƯỢC — hệ thống đã ghi bút toán vào sổ kế toán"),

    ("002", "Kế toán trưởng duyệt — bước 1 của luồng Chi thu nhập nhân viên", "P0",
     "⚠️ Phiếu do chính mình tạo, loại 'Chi thu nhập cho nhân viên', đang ở 'Chờ KT trưởng "
     "duyệt'. Tài khoản G có quyền Kế toán trưởng cùng công ty.",
     "1. G mở màn chi tiết phiếu\n"
     "2. Bấm 'Duyệt phiếu chi' rồi xác nhận\n"
     "3. Mở lại phiếu và đối chiếu sổ kế toán",
     "—",
     "- Phiếu chuyển sang 'Chờ chi tiền'\n"
     "- ⚠️ CHƯA ghi một dòng bút toán nào vào sổ kế toán — tiền chưa ra khỏi quỹ\n"
     "- Thủ quỹ cùng công ty nhận thông báo mới"),

    ("003", "Chỉ có một nút Duyệt, hệ thống tự nhận cấp", "P0",
     "Tài khoản có CẢ hai quyền Kế toán trưởng và Thủ quỹ. Phiếu X ở 'Chờ KT trưởng duyệt', "
     "phiếu Y ở 'Chờ chi tiền'.",
     "1. Mở chi tiết X, quan sát nút\n2. Mở chi tiết Y, quan sát nút",
     "—",
     "- Cả hai màn đều chỉ có MỘT nút tên 'Duyệt phiếu chi'\n"
     "- ⚠️ Hệ thống tự biết đang duyệt ở cấp nào theo trạng thái phiếu, người dùng không phải "
     "chọn cấp"),

    ("004", "Chặn số tiền thực chi vượt số tiền đề nghị chi", "P0",
     "Phiếu 'Chờ chi tiền', dòng 1 có số tiền đề nghị chi 50.000.",
     "1. Mở cửa sổ Duyệt\n2. Gõ 90.000 vào ô 'Số tiền thực chi' dòng 1\n3. Bấm 'Duyệt'",
     "Số tiền thực chi: 90.000",
     "- Bị chặn, hệ thống báo số tiền chi không được vượt quá số dư\n"
     "- Phiếu vẫn ở 'Chờ chi tiền', không ghi bút toán nào"),

    ("005", "Số dư âm ở luồng Chi thu nhập nhân viên vẫn chi được", "P0",
     "⚠️ Phiếu do chính mình tạo, loại 'Chi thu nhập cho nhân viên', có dòng nhân viên số dư "
     "-571.120.",
     "1. Mở cửa sổ Duyệt\n"
     "2. Nhập số tiền chi cho dòng số dư âm, giá trị không vượt quá trị tuyệt đối của số dư\n"
     "3. Bấm 'Duyệt'",
     "Số tiền chi: 500.000",
     "- ⚠️ Duyệt THÀNH CÔNG — hệ thống so trần theo giá trị tuyệt đối của số dư\n"
     "- Không bị chặn oan như khi so trực tiếp với số âm"),

    ("006", "Số tiền thực chi âm", "P1",
     "Cửa sổ Duyệt đang mở.",
     "1. Thử gõ số âm vào ô 'Số tiền thực chi'\n2. Bấm 'Duyệt'",
     "Số tiền thực chi: -1000",
     "- Ô không nhận dấu trừ; nếu lọt thì hệ thống báo 'Số tiền chi không được âm'"),

    ("007", "Ghi chú của người duyệt", "P1",
     "⚠️ Phiếu do chính mình tạo, đang 'Chờ chi tiền'.",
     "1. Mở cửa sổ Duyệt, nhập Ghi chú = 'Đã đối chiếu chứng từ'\n"
     "2. Bấm 'Duyệt'\n"
     "3. Mở Lịch sử của phiếu",
     "Ghi chú: Đã đối chiếu chứng từ",
     "- ⚠️ Ghi chú KHÔNG hiện trên phiếu mà nằm trong dòng lịch sử đổi trạng thái\n"
     "- Đây là điểm cải tiến so với cổng cũ (cổng cũ có ô này nhưng chữ gõ vào bị mất)"),

    ("008", "Ghi chú quá 500 ký tự", "P1",
     "Cửa sổ Duyệt đang mở.",
     "1. Dán 600 ký tự vào ô Ghi chú\n2. Bấm 'Duyệt'",
     "Chuỗi 600 ký tự",
     "- Hệ thống báo ghi chú không được quá 500 ký tự\n- Phiếu không được duyệt"),

    ("009", "Đóng cửa sổ Duyệt", "P0",
     "Cửa sổ 'Duyệt phiếu chi tiền' đang mở, đã sửa số tiền.",
     "1. Bấm 'Đóng'\n2. Tải lại màn chi tiết",
     "—",
     "- Cửa sổ đóng, phiếu VẪN ở trạng thái cũ\n- Không ghi gì vào sổ kế toán"),

    ("010", "Chặn duyệt lại phiếu đã duyệt", "P0",
     "Hai thủ quỹ F1 và F2 cùng mở phiếu P đang 'Chờ chi tiền'.",
     "1. F1 duyệt thành công\n"
     "2. F2 (chưa tải lại trang) bấm 'Duyệt'\n"
     "3. Kiểm tra sổ kế toán của phiếu P",
     "—",
     "- F2 nhận thông báo 'Phiếu chi đã được duyệt trước đó.'\n"
     "- ⚠️ Sổ kế toán chỉ có MỘT bộ bút toán, không bị ghi trùng\n"
     "- ⚠️ Thông báo này KHÁC với thông báo thiếu quyền — hai nguyên nhân được tách rõ để người "
     "vừa duyệt xong không đi tìm quyền bị thu hồi"),

    ("011", "Chống bấm nút Duyệt hai lần", "P0",
     "Cửa sổ Duyệt đang mở, đã nhập đủ số tiền.",
     "1. Bấm 'Duyệt' liên tiếp 3 lần thật nhanh\n2. Kiểm tra sổ kế toán và lịch sử phiếu",
     "—",
     "- Phiếu chỉ chuyển trạng thái MỘT lần\n"
     "- Chỉ một bộ bút toán được ghi, lịch sử không có bản ghi trùng"),

    ("012", "Duyệt phiếu không ở trạng thái chờ duyệt", "P0",
     "Phiếu nháp P1 do chính mình lập; tài khoản F là thủ quỹ.",
     "1. Mở màn chi tiết P1\n2. Quan sát các nút",
     "—",
     "- KHÔNG có nút 'Duyệt phiếu chi' và 'Hủy phiếu chi'\n"
     "- ⚠️ Chỉ phiếu ở 'Chờ chi tiền' hoặc 'Chờ KT trưởng duyệt' mới duyệt được"),
]

S8 = [
    ("001", "Hủy phiếu chi — luồng đầy đủ", "P0",
     "⚠️ CHỈ LÀM TRÊN PHIẾU DO CHÍNH MÌNH TẠO. Tài khoản F là thủ quỹ, phiếu P đang 'Chờ chi "
     "tiền'.",
     "1. Mở màn chi tiết phiếu P\n"
     "2. Bấm 'Hủy phiếu chi'\n"
     "3. Nhập 'Lý do hủy' và 'Ghi chú' (tuỳ chọn)\n"
     "4. Bấm 'Xác nhận'\n"
     "5. Mở lại phiếu và mở Lịch sử",
     "Lý do hủy: Sai thông tin tài khoản nhận",
     "- Cửa sổ 'Hủy phiếu chi tiền' có phụ đề 'Phiếu chi: <mã phiếu>', ô 'Lý do hủy' bắt buộc và "
     "ô 'Ghi chú' tuỳ chọn\n"
     "- Thông báo 'Hủy phiếu chi thành công!'\n"
     "- Phiếu P chuyển sang 'Hủy'\n"
     "- Đầu màn chi tiết xuất hiện dải băng vàng hiện lại Lý do hủy và Ghi chú\n"
     "- Lịch sử có dòng đổi trạng thái kèm lý do hủy\n"
     "- ⚠️ KHÔNG có bút toán nào được ghi vào sổ kế toán"),

    ("002", "Hủy khi chưa nhập lý do", "P0",
     "Cửa sổ 'Hủy phiếu chi tiền' đang mở, ô Lý do hủy còn trống.",
     "1. Bấm 'Xác nhận' mà không nhập gì",
     "—",
     "- Ô 'Lý do hủy' viền đỏ, dưới ô hiện chữ đỏ 'Lý do hủy – Bắt buộc nhập'\n"
     "- Cửa sổ KHÔNG đóng, phiếu giữ nguyên trạng thái"),

    ("003", "Đóng cửa sổ hủy", "P0",
     "Cửa sổ 'Hủy phiếu chi tiền' đang mở, đã nhập lý do.",
     "1. Bấm 'Đóng'\n2. Tải lại màn chi tiết",
     "—",
     "- Cửa sổ đóng, phiếu VẪN ở trạng thái cũ"),

    ("004", "Lý do hủy quá 500 ký tự", "P1",
     "Cửa sổ hủy đang mở.",
     "1. Dán 600 ký tự vào ô 'Lý do hủy'\n2. Bấm 'Xác nhận'",
     "Chuỗi 600 ký tự",
     "- Hệ thống báo 'Lý do hủy không được quá 500 ký tự.'\n- Phiếu không bị hủy"),

    ("005", "Kế toán trưởng hủy phiếu ở cấp mình", "P0",
     "⚠️ Phiếu do chính mình tạo, loại 'Chi thu nhập cho nhân viên', ở 'Chờ KT trưởng duyệt'. "
     "Tài khoản G có quyền Kế toán trưởng.",
     "1. G mở chi tiết phiếu, bấm 'Hủy phiếu chi', nhập lý do rồi xác nhận",
     "Lý do hủy: Số liệu thu nhập chưa chốt",
     "- Hủy thành công, phiếu chuyển sang 'Hủy'\n"
     "- ⚠️ Cả hai cấp duyệt đều hủy được phiếu đang chờ ĐÚNG cấp mình"),

    ("006", "Người lập KHÔNG tự hủy được phiếu đã gửi duyệt", "P0",
     "Tài khoản E lập phiếu P và đã gửi duyệt (đang 'Chờ chi tiền'). E không có quyền duyệt nào.",
     "1. E mở màn chi tiết phiếu P\n2. Quan sát các nút",
     "—",
     "- KHÔNG có nút 'Hủy phiếu chi'\n"
     "- ⚠️ Gửi đi rồi thì quyền định đoạt thuộc về người duyệt — đây là quy tắc đã chốt"),

    ("007", "Hủy phiếu không ở trạng thái chờ duyệt", "P0",
     "Phiếu đã 'Đã duyệt'; tài khoản F là thủ quỹ.",
     "1. Mở màn chi tiết phiếu đó\n2. Quan sát các nút",
     "—",
     "- KHÔNG có nút 'Hủy phiếu chi'\n- Phiếu đã duyệt không hủy được từ màn này"),

    ("008", "Không có nút Hủy trên màn danh sách", "P1",
     "Tài khoản F là thủ quỹ, danh sách có phiếu 'Chờ chi tiền'.",
     "1. Kéo lưới sang phải, mở menu ba chấm của dòng phiếu đó",
     "—",
     "- Không có mục 'Hủy phiếu' ở cột Hành động lẫn trong menu ba chấm\n"
     "- Muốn hủy phải vào màn chi tiết"),
]

S9 = [
    ("001", "Xóa phiếu nháp — luồng đầy đủ", "P0",
     "Tài khoản E có phiếu TPE.PC0826.00030 ở 'Đang tạo' do chính mình lập, có quyền Kế toán "
     "thanh toán.",
     "1. Bấm nút Xóa (thùng rác đỏ) trên dòng, hoặc nút 'Xóa' ở màn chi tiết\n"
     "2. Đọc hộp xác nhận rồi bấm 'Xóa'",
     "—",
     "- Hộp 'Xác nhận xóa' ghi 'Bạn có chắc muốn xóa phiếu chi tiền <mã phiếu>?'\n"
     "- Thông báo 'Xóa phiếu chi thành công!'\n"
     "- Dòng biến mất khỏi danh sách, tổng số phiếu giảm đúng 1"),

    ("002", "Hủy hộp xác nhận xóa", "P0",
     "Hộp 'Xác nhận xóa' đang mở.",
     "1. Bấm 'Hủy'",
     "—",
     "- Hộp đóng, phiếu còn nguyên, tổng số phiếu không đổi"),

    ("003", "Không xóa được phiếu đã gửi duyệt / đã duyệt / đã hủy", "P0",
     "Phiếu P2 'Chờ chi tiền', P3 'Đã duyệt', P4 'Hủy'.",
     "1. Quan sát cột Hành động của 3 dòng\n2. Mở màn chi tiết từng phiếu",
     "—",
     "- Cả trên lưới lẫn màn chi tiết đều KHÔNG có nút Xóa\n"
     "- Ép gọi chức năng Xóa thì hệ thống từ chối"),

    ("004", "Không xóa được phiếu nháp của người khác", "P0",
     "Tài khoản E có quyền Kế toán thanh toán; phiếu nháp P do người khác lập.",
     "1. E lọc Trạng thái = 'Đang tạo' và quan sát danh sách\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa cho phiếu P",
     "—",
     "- Phiếu P không hiện trên danh sách của E\n"
     "- Gọi thẳng thì hệ thống từ chối, phiếu còn nguyên\n"
     "- Ghi chú: bước 2 dành cho tester kỹ thuật"),

    ("005", "Xóa phiếu kéo theo toàn bộ dòng chi tiết", "P0",
     "Phiếu nháp có 3 dòng chi tiết.",
     "1. Xóa phiếu\n2. Lọc theo số hợp đồng của một dòng trong phiếu vừa xóa",
     "—",
     "- Phiếu vừa xóa không còn xuất hiện trong kết quả\n- Không còn dữ liệu sót"),

    ("006", "Xóa phiếu nháp thì phiếu đề nghị dùng lại được", "P1",
     "Phiếu nháp gắn phiếu đề nghị X.",
     "1. Xóa phiếu chi nháp\n2. Mở lại cửa sổ chọn phiếu đề nghị, tìm X",
     "—",
     "- X xuất hiện trở lại trong cửa sổ chọn, lập được phiếu chi mới"),
]

S10 = [
    ("001", "In phiếu nhóm lập-từ-đề-nghị", "P0",
     "Phiếu TPE.PC0826.00025 loại 'Chi trả nhà cung cấp'.",
     "1. Mở màn chi tiết, bấm 'In'",
     "—",
     "- Mở TAB MỚI hiển thị bản in\n"
     "- Bản in có ĐỦ 2 LIÊN, mỗi liên có ảnh tiêu đề thư công ty ở đầu trang\n"
     "- Tiêu đề 'PHIẾU CHI', dưới là ngày viết bằng chữ\n"
     "- Có 'Liên số', 'Quyển số', dòng 'Nợ:' và 'Có:' kèm số tiền\n"
     "- Có 'Họ và tên người nhận tiền', 'Phòng ban', 'Lý do chi', 'Số tiền thực chi', 'Bằng chữ'\n"
     "- Cuối liên có 5 ô ký: BAN GIÁM ĐỐC, KẾ TOÁN TRƯỞNG, NGƯỜI NHẬN TIỀN, NGƯỜI LẬP PHIẾU, "
     "THỦ QUỸ\n"
     "- Trình duyệt tự mở hộp thoại in"),

    ("002", "In phiếu loại Chi thu nhập cho nhân viên", "P0",
     "Phiếu TPE.PC0826.00008 loại 'Chi thu nhập cho nhân viên', 1 nhân viên.",
     "1. Mở màn chi tiết, bấm 'In'\n2. Cuộn hết bản in",
     "—",
     "- ⚠️ Bản in có THÊM 2 bảng kê so với mẫu ở trường hợp trên:\n"
     "  · 'BẢNG KÊ CHI TIẾT SỐ TIỀN CHI' (STT, Nhân viên, Số dư, Số tiền chi)\n"
     "  · 'BẢNG KÊ CHI TIẾT THEO VỤ VIỆC' (STT, Nhân viên và 6 cột thu nhập: Thưởng thực hiện "
     "hợp đồng, Thưởng năng suất tháng, Thưởng năng suất quý, Thưởng thêm, Tiền vận chuyển, Chi "
     "phí khác, Tổng cộng)\n"
     "- Cả hai bảng đều ghi 'Số phiếu' ở dòng tiêu đề"),

    ("003", "Nội dung bản in khớp dữ liệu phiếu", "P0",
     "Phiếu TPE.PC0826.00008: người nhận, phòng ban, lý do chi và số tiền đã biết.",
     "1. Mở bản in\n2. Đối chiếu từng dòng với màn chi tiết",
     "—",
     "- Người nhận tiền, Phòng ban, Lý do chi, Số tiền thực chi khớp màn chi tiết\n"
     "- Dòng 'Bằng chữ' đọc đúng số tiền tổng\n"
     "- Ô 'NGƯỜI NHẬN TIỀN' và 'NGƯỜI LẬP PHIẾU' có sẵn tên tương ứng"),

    ("004", "In phiếu từ danh sách", "P1",
     "Danh sách có phiếu bất kỳ.",
     "1. Kéo lưới sang phải, bấm nút In (máy in) trên dòng phiếu",
     "—",
     "- Mở tab mới đúng bản in của phiếu đó, giống hệt khi in từ màn chi tiết"),

    ("005", "In phiếu không có quyền xem", "P0",
     "Tài khoản A không xem được phiếu TPE.PC0826.00025.",
     "1. Gõ thẳng đường dẫn màn In của phiếu này",
     "—",
     "- Hệ thống từ chối, báo không có quyền in phiếu chi này\n"
     "- Không hiển thị nội dung phiếu"),

    ("006", "In lại phiếu không làm đổi dữ liệu", "P2",
     "Phiếu bất kỳ.",
     "1. In phiếu 3 lần\n2. Mở lịch sử thay đổi của phiếu",
     "—",
     "- Trạng thái, người cập nhật, ngày cập nhật KHÔNG đổi\n"
     "- Lịch sử không phát sinh bản ghi mới"),

    ("007", "Xuất Excel một phiếu", "P0",
     "Phiếu TPE.PC0826.00025.",
     "1. Mở màn chi tiết, bấm 'Xuất Excel'\n2. Mở tệp tải về",
     "—",
     "- Tệp tải về chứa ĐÚNG MỘT phiếu vừa xem, không phải cả danh sách\n"
     "- Các ô khớp với màn chi tiết và với bản in"),

    ("008", "Xuất Excel từ danh sách", "P1",
     "Danh sách có phiếu bất kỳ.",
     "1. Kéo lưới sang phải, bấm nút Xuất Excel trên dòng phiếu",
     "—",
     "- Tải về tệp của đúng phiếu đó\n"
     "- ⚠️ Màn này KHÔNG có chức năng xuất Excel cả danh sách"),

    ("009", "Xuất Excel không có quyền xem", "P0",
     "Tài khoản A không xem được phiếu.",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Xuất Excel cho phiếu đó",
     "—",
     "- Hệ thống từ chối, báo không có quyền xuất Excel phiếu chi này\n"
     "- Ghi chú: trường hợp này dành cho tester kỹ thuật"),
]

S11 = [
    ("001", "Mở lịch sử từ danh sách", "P0",
     "Phiếu TPE.PC0826.00028 đã từng bị hủy kèm lý do và ghi chú.",
     "1. Kéo lưới sang phải, bấm nút Lịch sử (đồng hồ quay ngược) trên dòng phiếu",
     "—",
     "- Cửa sổ 'Lịch sử thay đổi' mở, phụ đề ghi 'Phiếu: TPE.PC0826.00028'\n"
     "- Có mốc 'Thay đổi trạng thái' kèm thời điểm và dòng 'Người thực hiện: <tên> — <phòng ban>'\n"
     "- Hiện 'Trạng thái: Chờ chi tiền → Hủy'\n"
     "- Hiện 'Ghi chú: <nội dung ghi chú của người hủy>'\n"
     "- Hiện thêm dòng nền vàng chứa LÝ DO HỦY"),

    ("002", "Lịch sử ghi lại thao tác tạo và sửa", "P0",
     "Phiếu nháp vừa được tạo rồi sửa Người nhận.",
     "1. Mở cửa sổ Lịch sử của phiếu",
     "—",
     "- Có mốc 'Tạo mới' và mốc 'Thay đổi thông tin'\n"
     "- Mốc thay đổi ghi rõ trường bị đổi kèm giá trị cũ và giá trị mới\n"
     "- Mốc mới nhất nằm trên cùng"),

    ("003", "Lịch sử ghi lại từng cấp duyệt", "P0",
     "⚠️ Phiếu do chính mình tạo, loại 'Chi thu nhập cho nhân viên', đã qua cả 2 cấp duyệt.",
     "1. Mở cửa sổ Lịch sử",
     "—",
     "- Có mốc 'Đang tạo → Chờ KT trưởng duyệt' (gửi duyệt)\n"
     "- Có mốc 'Chờ KT trưởng duyệt → Chờ chi tiền' (Kế toán trưởng duyệt)\n"
     "- Có mốc 'Chờ chi tiền → Đã duyệt' (Thủ quỹ duyệt) kèm ghi chú đã ghi bút toán\n"
     "- Mỗi mốc ghi đúng tên người thực hiện của cấp đó"),

    ("004", "Khối Lịch sử ở màn chi tiết", "P0",
     "Phiếu đã có ít nhất 1 mốc lịch sử.",
     "1. Mở màn chi tiết phiếu\n2. Cuộn xuống cuối trang\n3. Bấm 'Xem lịch sử'",
     "—",
     "- Có khối 'Lịch sử', mặc định thu gọn\n"
     "- Bấm 'Xem lịch sử' thì bung ra, nút đổi thành 'Thu gọn'\n"
     "- Có nút 'Làm mới' và nút 'Bộ lọc'\n"
     "- Nội dung giống hệt cửa sổ Lịch sử mở từ danh sách"),

    ("005", "Phiếu chưa có lịch sử", "P1",
     "Phiếu cũ chuyển từ hệ thống trước, chưa từng thao tác trên hệ thống mới.",
     "1. Mở khối Lịch sử của phiếu đó",
     "—",
     "- Hiện dòng 'Chưa có lịch sử thao tác nào.'\n- Không báo lỗi"),

    ("006", "Ai cũng xem được lịch sử của phiếu mình thấy", "P1",
     "Tài khoản A không có quyền đặc biệt nào, đang thấy phiếu do mình lập.",
     "1. Bấm nút Lịch sử trên dòng phiếu đó",
     "—",
     "- Cửa sổ mở bình thường, không bị chặn quyền"),
]

S12 = [
    ("001", "Phiếu bị duyệt trong lúc người lập đang mở màn chi tiết", "P0",
     "Phiếu P đang 'Chờ chi tiền'; người lập mở màn chi tiết từ trước, thủ quỹ vừa duyệt xong.",
     "1. Người lập tải lại màn chi tiết",
     "—",
     "- Trạng thái đổi thành 'Đã duyệt'\n- Các nút cập nhật theo trạng thái mới"),

    ("002", "Phiếu bị xóa trong lúc đang mở màn chi tiết", "P1",
     "Cùng tài khoản mở phiếu nháp P ở tab 1; ở tab 2 xóa chính phiếu này.",
     "1. Ở tab 1, bấm nút 'Sửa'",
     "—",
     "- Hệ thống báo không tìm thấy dữ liệu\n- Không treo trang"),

    ("003", "Hai người cùng duyệt một phiếu", "P0",
     "Hai thủ quỹ cùng mở phiếu P đang 'Chờ chi tiền'.",
     "1. Người 1 duyệt thành công\n2. Người 2 bấm Duyệt\n3. Đối chiếu sổ kế toán",
     "—",
     "- Người 2 nhận thông báo phiếu đã được duyệt trước đó\n"
     "- ⚠️ Sổ kế toán chỉ có MỘT bộ bút toán"),

    ("004", "Một người duyệt, một người hủy cùng lúc", "P0",
     "Hai thủ quỹ cùng mở phiếu P đang 'Chờ chi tiền'.",
     "1. Người 1 bấm Duyệt thành công\n2. Người 2 bấm Hủy",
     "—",
     "- Người 2 bị từ chối, phiếu giữ nguyên trạng thái 'Đã duyệt'\n"
     "- Không có trường hợp phiếu vừa duyệt vừa hủy"),

    ("005", "Tải lại trang giữa lúc đang nhập form", "P1",
     "Màn Tạo mới đã chọn Loại chi và nhập Người nhận.",
     "1. Nhấn phím tải lại trang\n2. Đọc cảnh báo rồi chọn rời trang",
     "—",
     "- Trình duyệt cảnh báo dữ liệu chưa lưu\n"
     "- Chọn rời trang thì form về trắng, không có phiếu nào được tạo"),

    ("006", "Mất kết nối giữa lúc duyệt phiếu", "P0",
     "⚠️ Phiếu do chính mình tạo, đang 'Chờ chi tiền'. Ngắt mạng ngay sau khi bấm Duyệt.",
     "1. Bấm 'Duyệt' rồi ngắt mạng\n"
     "2. Nối lại mạng, mở lại phiếu và đối chiếu sổ kế toán",
     "—",
     "- Phiếu hoặc duyệt trọn vẹn (đổi trạng thái + ghi đủ bút toán), hoặc không đổi gì cả\n"
     "- ⚠️ TUYỆT ĐỐI không được có trường hợp phiếu 'Đã duyệt' mà sổ kế toán thiếu bút toán, "
     "hoặc ngược lại"),
]

S13 = [
    ("001", "Luồng trọn vẹn nhóm lập-từ-đề-nghị: lập → gửi duyệt → thủ quỹ duyệt", "P0",
     "⚠️ DÙNG PHIẾU ĐỀ NGHỊ TEST DO CHÍNH MÌNH LẬP. Tài khoản E có quyền Kế toán thanh toán; "
     "tài khoản F có quyền Thủ quỹ cùng công ty.",
     "1. E lập phiếu chi từ một phiếu đề nghị đang Chờ tạo phiếu chi, bấm 'Lưu nháp'\n"
     "2. E mở lại phiếu, bấm 'Sửa', bổ sung Tài khoản nợ, bấm 'Lưu và gửi duyệt'\n"
     "3. F mở phiếu, bấm 'Duyệt phiếu chi', xác nhận số tiền rồi bấm 'Duyệt'\n"
     "4. Mở màn Đề nghị thanh toán kiểm tra phiếu đề nghị\n"
     "5. Mở lịch sử phiếu chi",
     "—",
     "- Bước 1: trạng thái 'Đang tạo', chỉ E nhìn thấy\n"
     "- Bước 2: trạng thái 'Chờ chi tiền'; F nhận thông báo; phiếu mất nút Sửa/Xóa\n"
     "- Bước 3: trạng thái 'Đã duyệt', ghi người duyệt và ngày hạch toán, sổ kế toán có bút toán\n"
     "- Bước 4: phiếu đề nghị chuyển sang trạng thái duyệt phiếu chi\n"
     "- Bước 5: lịch sử có đủ các mốc theo đúng thứ tự thời gian"),

    ("002", "Luồng trọn vẹn Chi thu nhập nhân viên: 2 cấp duyệt", "P0",
     "⚠️ Phiếu do chính mình tạo. Tài khoản E (Kế toán thanh toán), G (Kế toán trưởng), "
     "F (Thủ quỹ), cùng công ty.",
     "1. E chọn Loại chi = 'Chi thu nhập cho nhân viên', chọn Phòng ban chi, điền Người nhận và "
     "Lý do chi, bấm 'Lưu và gửi duyệt'\n"
     "2. Kiểm tra chuông của G và F\n"
     "3. G mở phiếu, bấm 'Duyệt phiếu chi'\n"
     "4. Kiểm tra sổ kế toán\n"
     "5. F mở phiếu, bấm 'Duyệt phiếu chi', xác nhận số tiền rồi 'Duyệt'\n"
     "6. Kiểm tra lại sổ kế toán",
     "—",
     "- Bước 1: trạng thái 'Chờ KT trưởng duyệt'\n"
     "- Bước 2: chỉ G nhận thông báo, F chưa nhận\n"
     "- Bước 3: trạng thái 'Chờ chi tiền', F nhận thông báo\n"
     "- ⚠️ Bước 4: sổ kế toán VẪN TRỐNG — Kế toán trưởng duyệt chưa ghi sổ\n"
     "- Bước 5: trạng thái 'Đã duyệt'\n"
     "- Bước 6: sổ kế toán mới có bút toán"),

    ("003", "Luồng trọn vẹn: lập nháp rồi xóa bỏ", "P0",
     "Tài khoản E có quyền Kế toán thanh toán.",
     "1. E lập phiếu chi từ phiếu đề nghị X, bấm 'Lưu nháp'\n"
     "2. E mở lại phiếu kiểm tra nội dung\n"
     "3. E xóa phiếu\n"
     "4. Mở lại cửa sổ chọn phiếu đề nghị, tìm X",
     "—",
     "- Tổng số phiếu trở về đúng như trước khi lập\n"
     "- X xuất hiện lại trong cửa sổ chọn, lập được phiếu chi mới"),

    ("004", "Luồng trọn vẹn: gửi duyệt rồi bị hủy", "P0",
     "⚠️ Phiếu do chính mình tạo. Tài khoản E lập phiếu, F là thủ quỹ.",
     "1. E lập và gửi duyệt phiếu chi\n"
     "2. F mở phiếu, bấm 'Hủy phiếu chi', nhập lý do và ghi chú, xác nhận\n"
     "3. E mở lại phiếu\n"
     "4. Mở Lịch sử",
     "—",
     "- Phiếu chuyển 'Hủy'\n"
     "- Đầu màn chi tiết có dải băng vàng hiện Lý do hủy và Ghi chú\n"
     "- Lịch sử có dòng đổi trạng thái kèm lý do hủy\n"
     "- Sổ kế toán không phát sinh bút toán nào\n"
     "- E không sửa lại được phiếu đã hủy"),

    ("005", "Luồng trọn vẹn: theo dõi một phiếu qua đủ 5 trạng thái", "P1",
     "⚠️ Dùng phiếu test do chính mình tạo.",
     "1. Lập phiếu loại 'Chi thu nhập cho nhân viên', lưu nháp — ghi lại trạng thái và các nút\n"
     "2. Gửi duyệt — ghi lại\n"
     "3. Kế toán trưởng duyệt — ghi lại\n"
     "4. Thủ quỹ duyệt — ghi lại\n"
     "5. Trên một phiếu khác, thủ quỹ hủy — ghi lại",
     "—",
     "- Đang tạo (nhãn xám): có Sửa, Xóa; chỉ người lập thấy\n"
     "- Chờ KT trưởng duyệt (nhãn vàng): mất Sửa/Xóa; chỉ Kế toán trưởng có Duyệt/Hủy\n"
     "- Chờ chi tiền (nhãn vàng): chỉ Thủ quỹ có Duyệt/Hủy\n"
     "- Đã duyệt (nhãn xanh): chỉ còn In, Xuất Excel, Quay lại; đã ghi sổ kế toán\n"
     "- Hủy (nhãn đỏ): chỉ còn In, Xuất Excel, Quay lại; có dải băng lý do hủy"),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", S1),
    ("II", "BỘ LỌC & TÌM KIẾM", S2),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", S3),
    ("IV", "TẠO MỚI PHIẾU CHI", S4),
    ("V", "SỬA PHIẾU CHI", S5),
    ("VI", "XEM CHI TIẾT PHIẾU CHI", S6),
    ("VII", "DUYỆT PHIẾU CHI", S7),
    ("VIII", "HỦY PHIẾU CHI", S8),
    ("IX", "XÓA PHIẾU CHI", S9),
    ("X", "IN PHIẾU & XUẤT EXCEL", S10),
    ("XI", "LỊCH SỬ THAY ĐỔI", S11),
    ("XII", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", S12),
    ("XIII", "LUỒNG NGHIỆP VỤ TRỌN VẸN", S13),
]

if __name__ == "__main__":
    build(output_file=OUT,
          sheet_name="Trang tính1",
          feature_name="Phiếu chi tiền - Cập nhật ngày 03/09/2026",
          module_name=MODULE,
          description_block=DESCRIPTION_BLOCK,
          role_tcs=ROLE_TCS,
          sections=SECTIONS)
