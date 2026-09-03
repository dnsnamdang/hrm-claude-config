# -*- coding: utf-8 -*-
"""Sinh file testcase Excel cho man "Phieu thu tien" (phan he Tai chinh).

Nguon doc code 03/09/2026 (nhanh gop_db):
  BE  Modules/Finance/Routes/api.php (:250-272)
      Modules/Finance/Http/Controllers/V1/BillIncomeController.php
      Modules/Finance/Entities/BillIncome/{BillIncome,BillIncomeAccess,BillIncomeDetail}.php
      Modules/Finance/Http/Requests/BillIncome/*.php  (nguyen van thong bao loi)
      Modules/Finance/Services/BillIncome{Service,WriteService,ApprovalService,AccountingService,
                                          PrintService,HistoryService}.php
      Modules/Finance/Transformers/BillIncomeResource/*.php
      Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (:1203-1205)
  FE  hrm-client/pages/finance/bill-incomes/{index,create}.vue
      .../_id/{index,edit,print}.vue
      .../components/{BillIncomeForm,IncomeRequestSearchModal}.vue
      hrm-client/components/subsystem-menu/finance.js (:85)
  Anh that: pt_shots/ (cong dev hrm-crm.eteksofts.com + local, 03/09/2026)

Chay:  python .plans/gop-db/finance-bill-income/gen_testcase.py
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
MODULE = "Phiếu thu tiền"

MENU = "Phân hệ Tài chính > Quản lý tiền > Thanh toán tiền mặt > Phiếu thu"

# ════════════════════════════════════════════════════ 1. KHỐI MÔ TẢ (9 mục)
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Phiếu thu tiền là chứng từ kế toán lập từ MỘT phiếu đề nghị thu tiền đang chờ duyệt, để ghi "
     "nhận khoản tiền thực tế thu về. Màn hình cho phép: lập phiếu (Lưu nháp hoặc Lưu và gửi "
     "duyệt), sửa và xóa phiếu nháp, xem chi tiết, in 2 liên, xuất Excel một phiếu, xem lịch sử "
     "thay đổi. Thủ quỹ mở phiếu đang chờ duyệt sẽ nhập số tiền THỰC THU cho từng dòng rồi bấm "
     "«Duyệt phiếu thu» — đây là thời điểm DUY NHẤT hệ thống ghi bút toán vào sổ kế toán; hoặc "
     "bấm «Hủy phiếu thu» kèm lý do.\n"
     "Đường dẫn màn hình: " + MENU + ". Chỉ có duy nhất MỘT mục menu trỏ vào màn này — không có "
     "màn «của tôi» / «chờ duyệt» / «đã duyệt» riêng, ba cách xem đó nay là ô lọc Người lập và ô "
     "lọc Trạng thái ngay trên màn."),

    ("2. Đối tượng được tính / hiển thị",
     "Danh sách hiển thị phiếu thu theo phạm vi quyền của người đăng nhập:\n"
     "- Là quản trị hệ thống, hoặc có quyền 'Xem tất cả phiếu thu của tổng công ty': thấy phiếu "
     "của mọi công ty.\n"
     "- Có quyền 'Xem tất cả phiếu thu của công ty': chỉ phiếu thuộc công ty của mình.\n"
     "- Không có quyền nào trong hai quyền trên: chỉ thấy phiếu do chính mình lập.\n"
     "Đủ 4 trạng thái đều được hiển thị: Đang tạo, Chờ duyệt, Đã duyệt, Hủy.\n"
     "Cột Loại thu và ba ô lọc Công ty / Phòng ban / Bộ phận lấy theo PHIẾU ĐỀ NGHỊ gắn với phiếu "
     "thu, không phải theo bản thân phiếu thu."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu ở trạng thái 'Đang tạo' (nháp) của NGƯỜI KHÁC luôn bị ẩn, kể cả với quản trị hệ "
     "thống và người có quyền xem toàn tổng công ty.\n"
     "- Người không xác định được là ai (phiên đăng nhập hỏng) thì danh sách RỖNG tuyệt đối.\n"
     "- Cửa sổ chọn phiếu đề nghị CHỈ liệt kê phiếu đề nghị đang ở trạng thái 'Chờ KT duyệt' VÀ "
     "chưa có phiếu thu nào; phiếu đề nghị đã lập phiếu thu (kể cả phiếu thu đã bị hủy) không còn "
     "xuất hiện.\n"
     "- Hai ô chọn tài khoản (Tài khoản nợ, Số tài khoản có) chỉ liệt kê tài khoản đang hoạt động "
     "VÀ là tài khoản cấp cuối; tài khoản tổng hợp (đang là cha của tài khoản khác) không cho "
     "chọn. Riêng phiếu cũ đang gắn tài khoản đã khóa thì tài khoản đó vẫn hiện đúng tên khi mở "
     "màn Sửa / Xem.\n"
     "- Ba ô lọc Công ty / Phòng ban / Bộ phận chỉ hiện với người có quyền xem theo tổng công ty "
     "hoặc theo công ty; người không có hai quyền đó không thấy nhóm ô lọc này.\n"
     "- Nút In không hiện với phiếu thuộc loại thu 'Thu khác' (loại này không có mẫu in)."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Hai ô 'Ngày lập từ' và 'Ngày lập đến' lọc theo NGÀY LẬP PHIẾU THU (cột Ngày tạo trên lưới), "
     "không phải Ngày cập nhật và cũng không phải ngày hạch toán.\n"
     "Cả hai mốc lấy trọn ngày: chọn 'Ngày lập đến' là hôm nay thì phiếu lập chiều nay vẫn nằm "
     "trong kết quả. Bỏ trống một trong hai ô thì phía đó không giới hạn.\n"
     "Màn hình KHÔNG có ô lọc theo ngày hạch toán."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Một phiếu thu gồm 2 tầng:\n"
     "- Tầng 1 (phiếu): mã phiếu sinh tự động dạng {mã công ty}.PT{tháng năm}.{5 chữ số}, số "
     "phiếu đề nghị, tài khoản nợ, người nộp, tỷ giá, ghi chú, trạng thái, ngày hạch toán, người "
     "duyệt. Loại thu, loại tiền, người đề nghị, phòng ban và lý do thu đọc từ phiếu đề nghị, "
     "không sửa được tại màn phiếu thu.\n"
     "- Tầng 2 (dòng chi tiết): KÉO THẲNG từ phiếu đề nghị, không thêm và không xóa dòng được. "
     "Mỗi dòng gồm số tài khoản có, đối tượng thu (khách hàng hoặc nhà cung cấp), số đơn hàng / "
     "hợp đồng, số tiền đề nghị thu (chỉ đọc), số tiền duyệt thu (người lập nhập), số tiền thực "
     "thu (thủ quỹ nhập lúc duyệt) và ghi chú.\n"
     "- Một phiếu đề nghị chỉ lập được ĐÚNG MỘT phiếu thu."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Dòng 'Tổng cộng' cuối bảng chi tiết cộng theo từng cột tiền của các dòng đang hiển thị.\n"
     "- Cột 'Số tiền' trên màn danh sách LUÔN là tổng số tiền DUYỆT THU, kể cả sau khi phiếu đã "
     "được duyệt và số thực thu khác số duyệt thu. Cột này cũng là cột mà hai ô lọc 'Số tiền từ – "
     "đến' và nút sắp xếp đang dùng.\n"
     "- Nút 'Phân bổ' rải tổng số tiền vừa gõ xuống cột 'Số tiền thực thu' theo thứ tự từ trên "
     "xuống: mỗi dòng nhận tối đa bằng số duyệt thu của chính nó, hết tiền thì các dòng còn lại "
     "về 0. Bấm xong vẫn sửa tay từng ô được và chưa ghi gì xuống hệ thống.\n"
     "- Khi duyệt, dòng nào có số thực thu bằng 0 thì KHÔNG sinh bút toán cho dòng đó."),

    ("7. Phân quyền cấp",
     "Hai quyền quyết định phạm vi dữ liệu nhìn thấy (đặt tên đúng như trong hệ thống):\n"
     "- Xem tất cả phiếu thu của tổng công ty\n"
     "- Xem tất cả phiếu thu của công ty\n"
     "Hai quyền thao tác:\n"
     "- Kế toán thanh toán: lập, sửa, xóa phiếu thu; mở được cửa sổ chọn phiếu đề nghị. Thiếu "
     "quyền này thì hệ thống từ chối ngay tại bước lưu, không phụ thuộc việc nút có hiện hay không.\n"
     "- Thủ quỹ duyệt phiếu thu: nhập số thực thu, bấm Duyệt phiếu thu và Hủy phiếu thu. Cũng là "
     "nhóm nhận thông báo khi có phiếu mới gửi duyệt.\n"
     "Vai trò quản trị hệ thống được coi như có đủ bốn quyền trên.\n"
     "Ba chức năng Xem chi tiết / In / Xuất Excel chỉ cần nhìn thấy được phiếu; Lịch sử không gắn "
     "quyền riêng."),

    ("8. Cách tính các ô thống kê",
     "- Dòng 'Hiển thị a–b / N' dưới lưới: a là số thứ tự dòng đầu trang, b là dòng cuối, N là "
     "tổng số phiếu khớp bộ lọc VÀ nằm trong phạm vi quyền.\n"
     "- Cột STT đánh theo trang: sang trang 2 với cỡ 10 dòng/trang thì bắt đầu từ 11.\n"
     "- Ô 'Số tiền' trên lưới = tổng số tiền duyệt thu của phiếu, ngăn cách hàng nghìn bằng dấu "
     "phẩy, không kèm ký hiệu tiền tệ.\n"
     "- Dòng 'Tổng cộng' trong bảng chi tiết = cộng dọc từng cột tiền của các dòng trong phiếu.\n"
     "- Phiếu ngoại tệ hiển thị THÊM một cột cho mỗi nhóm tiền: cột nguyên tệ (theo loại tiền của "
     "phiếu đề nghị) và cột VND. Cột VND tự quy đổi theo ô Tỷ giá; loại tiền là VNĐ thì ô Tỷ giá "
     "bị khóa ở giá trị 1 và bảng chỉ còn cột VND."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất của màn này:\n"
     "- DUYỆT PHIẾU LÀ THAO TÁC KHÔNG HOÀN TÁC: bấm xong hệ thống ghi bút toán vào sổ kế toán "
     "dùng chung với cổng cũ. Khi kiểm thử phải dùng phiếu do chính mình tạo, TUYỆT ĐỐI không "
     "duyệt phiếu của người khác trên dữ liệu thật.\n"
     "- Hủy phiếu thu là NGÕ CỤT theo thiết kế: phiếu đề nghị chuyển sang Hủy và KHÔNG lập lại "
     "được phiếu thu khác cho phiếu đề nghị đó. Đây là quy tắc nghiệp vụ đã chốt, không phải lỗi.\n"
     "- Xóa phiếu thu nháp KHÔNG trả trạng thái phiếu đề nghị về. An toàn vì phiếu nháp chưa hề "
     "đụng tới phiếu đề nghị; nhưng phiếu đề nghị vẫn hiện 'Chờ KT duyệt' trong khi người khác "
     "bấm lập phiếu thu sẽ nhận lỗi 'Đề nghị thu tiền đã lập phiếu thu tiền'.\n"
     "- Cột 'Số tiền' của lưới là DUYỆT THU chứ không phải THỰC THU. Phiếu đã duyệt có thực thu "
     "300.000 mà cột này vẫn hiện 500.000 là ĐÚNG.\n"
     "- Ô tìm nhanh (ghi 'Tìm theo mã phiếu...') phải bấm nút 'Tìm kiếm' mới chạy; mọi ô trong "
     "'Tìm kiếm nâng cao' tự lọc ngay khi đổi giá trị.\n"
     "- Nhóm cột 'Số tiền thực thu' chỉ xuất hiện ở màn XEM CHI TIẾT, không có ở màn Tạo mới và "
     "màn Sửa; và chỉ thành ô nhập khi người xem là thủ quỹ và phiếu đang Chờ duyệt.\n"
     "- Gõ số thực thu lớn hơn số duyệt thu thì hệ thống cho gõ nhưng báo đỏ dưới ô và chặn bấm "
     "Duyệt — khác cổng cũ (cổng cũ tự kéo số về bằng số duyệt thu).\n"
     "- Bộ lọc được ghi nhớ 10 phút: rời màn rồi quay lại trong 10 phút thì điều kiện lọc cũ vẫn "
     "còn, dễ tưởng nhầm là mất dữ liệu."),
]

# ════════════════════════════════════════════════════ 2. PHÂN QUYỀN
ROLE_TCS = [
    ("00", "Không có quyền xem nào — chỉ thấy phiếu của chính mình", "P0",
     "Tài khoản A không có 'Xem tất cả phiếu thu của tổng công ty', không có 'Xem tất cả phiếu "
     "thu của công ty', không phải quản trị hệ thống. A đã lập 4 phiếu; công ty của A có tổng "
     "60 phiếu.",
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Vào " + MENU + "\n"
     "3. Đọc tổng số phiếu ở dòng 'Hiển thị a–b / N'",
     "—",
     "- Tổng N = 4, đúng bằng số phiếu A tự lập\n"
     "- Cột Người tạo của mọi dòng đều là tên A\n"
     "- Khối lọc nâng cao KHÔNG có nhóm ô Công ty / Phòng ban / Bộ phận\n"
     "- Nút 'Tạo mới' vẫn hiện"),

    ("01", "Quyền 'Xem tất cả phiếu thu của công ty'", "P0",
     "Tài khoản B có quyền 'Xem tất cả phiếu thu của công ty', thuộc công ty 4. Công ty 4 có 60 "
     "phiếu, trong đó 3 phiếu nháp của người khác; công ty 1 có 120 phiếu.",
     "1. Đăng nhập bằng tài khoản B\n"
     "2. Vào " + MENU + "\n"
     "3. Đếm tổng số phiếu và rà cột Người tạo",
     "—",
     "- Tổng N = 57 (60 trừ 3 nháp của người khác)\n"
     "- Không có phiếu nào của công ty 1\n"
     "- Khối lọc nâng cao CÓ nhóm ô Công ty / Phòng ban / Bộ phận"),

    ("02", "Quyền 'Xem tất cả phiếu thu của tổng công ty'", "P0",
     "Tài khoản C có quyền 'Xem tất cả phiếu thu của tổng công ty'. Toàn hệ thống có 2.379 phiếu, "
     "trong đó 5 nháp của người khác và 1 nháp của chính C.",
     "1. Đăng nhập bằng tài khoản C\n"
     "2. Vào " + MENU + "\n"
     "3. Đếm tổng số phiếu",
     "—",
     "- Tổng N = 2.375 (2.379 trừ 5 nháp người khác, vẫn giữ 1 nháp của C)\n"
     "- Thấy phiếu của mọi công ty"),

    ("03", "Quản trị hệ thống — xem như quyền tổng công ty", "P0",
     "Tài khoản D là quản trị hệ thống, KHÔNG được gán quyền xem nào.",
     "1. Đăng nhập bằng tài khoản D\n"
     "2. Vào " + MENU + "\n"
     "3. So tổng số phiếu với tài khoản C ở trường hợp trên",
     "—",
     "- D thấy phiếu của mọi công ty, phạm vi tương đương tài khoản C\n"
     "- Nháp của người khác vẫn bị ẩn với D"),

    ("04", "Quyền 'Kế toán thanh toán' — lập được phiếu thu", "P0",
     "Tài khoản E có quyền 'Kế toán thanh toán'. Hệ thống có 7 phiếu đề nghị đang Chờ KT duyệt "
     "chưa lập phiếu thu.",
     "1. Đăng nhập bằng tài khoản E\n"
     "2. Bấm 'Tạo mới'\n"
     "3. Bấm vào ô 'Số phiếu đề nghị'",
     "—",
     "- Vào được màn Thêm phiếu thu tiền\n"
     "- Cửa sổ 'Chọn phiếu đề nghị thu' mở ra và liệt kê đúng 7 phiếu\n"
     "- Chọn được một phiếu, bảng Chi tiết nạp đủ dòng"),

    ("05", "Không có quyền 'Kế toán thanh toán' — không lập được phiếu thu", "P0",
     "Tài khoản A không có quyền 'Kế toán thanh toán', không phải quản trị hệ thống.",
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Bấm 'Tạo mới'\n"
     "3. Bấm vào ô 'Số phiếu đề nghị'\n"
     "4. Điền đủ thông tin (nếu vào được) rồi bấm 'Lưu'",
     "—",
     "- Cửa sổ chọn phiếu đề nghị bị từ chối, báo không có quyền xem danh sách phiếu đề nghị thu\n"
     "- Nếu ép lưu thì hệ thống từ chối, báo 'Bạn không có quyền lập phiếu thu'\n"
     "- Không có phiếu thu nào được tạo"),

    ("06", "Quyền 'Thủ quỹ duyệt phiếu thu' — thấy nút Duyệt và Hủy", "P0",
     "Tài khoản F có quyền 'Thủ quỹ duyệt phiếu thu'. Phiếu TPE.PT0826.00032 đang ở trạng thái "
     "Chờ duyệt.",
     "1. Đăng nhập bằng tài khoản F\n"
     "2. Mở màn chi tiết phiếu TPE.PT0826.00032\n"
     "3. Quan sát bảng Chi tiết và các nút cuối màn",
     "—",
     "- Cột 'Số tiền thực thu' là Ô NHẬP, có dấu sao đỏ ở tiêu đề\n"
     "- Có khối 'Số tiền phân bổ' kèm nút 'Phân bổ' phía trên bảng\n"
     "- Có nút 'Duyệt phiếu thu' và 'Hủy phiếu thu'"),

    ("07", "Không có quyền 'Thủ quỹ duyệt phiếu thu'", "P0",
     "Tài khoản E chỉ có 'Kế toán thanh toán', không có 'Thủ quỹ duyệt phiếu thu'. Phiếu "
     "TPE.PT0826.00032 đang Chờ duyệt.",
     "1. Đăng nhập bằng tài khoản E\n"
     "2. Mở màn chi tiết phiếu TPE.PT0826.00032\n"
     "3. Quan sát bảng Chi tiết và các nút cuối màn",
     "—",
     "- Cột 'Số tiền thực thu' chỉ HIỂN THỊ số, không nhập được\n"
     "- Không có khối 'Số tiền phân bổ' và nút 'Phân bổ'\n"
     "- Không có nút 'Duyệt phiếu thu' và 'Hủy phiếu thu'"),

    ("08", "Bỏ qua giao diện, gọi thẳng chức năng Duyệt khi không phải thủ quỹ", "P0",
     "Tài khoản E không có quyền 'Thủ quỹ duyệt phiếu thu'. Phiếu TPE.PT0826.00032 đang Chờ duyệt.",
     "1. Đăng nhập bằng tài khoản E\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Duyệt cho phiếu này, bỏ qua giao diện\n"
     "3. Mở lại phiếu kiểm tra trạng thái và sổ kế toán",
     "Số tiền thực thu: bằng số duyệt thu",
     "- Hệ thống từ chối, báo 'Bạn không có quyền duyệt phiếu thu'\n"
     "- Phiếu vẫn ở Chờ duyệt, KHÔNG phát sinh bút toán nào trong sổ kế toán\n"
     "- Ghi chú: trường hợp này dành cho tester kỹ thuật"),

    ("09", "Bỏ qua giao diện, gọi thẳng chức năng Sửa phiếu đã duyệt", "P0",
     "Tài khoản E có quyền 'Kế toán thanh toán'. Phiếu TPE.PT0826.00030 đã ở trạng thái Đã duyệt.",
     "1. Đăng nhập bằng tài khoản E\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Sửa cho phiếu này\n"
     "3. Mở lại phiếu kiểm tra",
     "Người nộp: 'sửa lén'",
     "- Hệ thống từ chối, báo 'Phiếu thu đã gửi duyệt hoặc đã duyệt, không sửa được'\n"
     "- Nội dung phiếu không đổi\n"
     "- Ghi chú: trường hợp này dành cho tester kỹ thuật"),

    ("10", "Bỏ qua giao diện, gọi thẳng chức năng Xóa phiếu của người khác", "P0",
     "Tài khoản E. Phiếu nháp do người khác lập (E không nhìn thấy trên danh sách nhưng biết mã).",
     "1. Đăng nhập bằng tài khoản E\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa cho phiếu nháp đó\n"
     "3. Đăng nhập lại bằng người lập phiếu để kiểm tra",
     "—",
     "- Hệ thống từ chối, báo 'Bạn không có quyền xóa phiếu thu này'\n"
     "- Phiếu nháp còn nguyên\n"
     "- Ghi chú: trường hợp này dành cho tester kỹ thuật"),

    ("11", "Xem chi tiết phiếu ngoài phạm vi quyền", "P0",
     "Tài khoản A (không quyền xem nào) biết mã một phiếu của người khác cùng công ty.",
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Gõ thẳng đường dẫn màn chi tiết phiếu đó lên thanh địa chỉ",
     "—",
     "- Hệ thống từ chối, báo 'Bạn không có quyền xem phiếu thu này'\n"
     "- Không hiển thị nội dung phiếu\n"
     "- Gõ đường dẫn màn In của cùng phiếu cũng bị chặn tương tự"),

    ("12", "Người duyệt luôn xem lại được phiếu mình đã duyệt", "P1",
     "Tài khoản F (thủ quỹ) thuộc công ty 4, đã duyệt phiếu X của công ty 1. F KHÔNG có quyền xem "
     "theo tổng công ty.",
     "1. Đăng nhập bằng tài khoản F\n"
     "2. Mở màn chi tiết phiếu X",
     "—",
     "- Mở được, không bị chặn — người duyệt luôn xem lại được phiếu mình đã xử lý\n"
     "- ⚠️ Nhưng trên DANH SÁCH thì phiếu X vẫn không hiện, vì danh sách lọc theo công ty"),
]

# ════════════════════════════════════════════════════ 3. SECTION NGHIỆP VỤ

S1 = [
    ("001", "Mở màn danh sách lần đầu — bố cục và các cột", "P0",
     "Tài khoản C (quyền xem tổng công ty), hệ thống có 2.379 phiếu, chưa chỉnh cấu hình cột.",
     "1. Đăng nhập\n"
     "2. Vào " + MENU + "\n"
     "3. Chờ lưới nạp xong rồi quan sát (kéo ngang để xem hết cột)",
     "—",
     "- Tiêu đề trang và tiêu đề lưới đều là 'Danh sách phiếu thu'\n"
     "- Lưới có 13 cột: STT, Mã phiếu, Mã phiếu đề nghị thu, Loại thu, Khách hàng, Số tiền, "
     "Người đề nghị, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật, Trạng thái, Hành động\n"
     "- Khối lọc phía trên có ô tìm nhanh ghi 'Tìm theo mã phiếu...', nút 'Tìm kiếm', 'Làm mới', "
     "'Cài đặt bộ lọc', 'Tìm kiếm nâng cao'\n"
     "- Thanh công cụ của lưới có nút 'Tạo mới' và nút biểu tượng cấu hình cột\n"
     "- Mặc định 10 dòng/trang, dòng đếm ghi 'Hiển thị 1–10 / 2379'"),

    ("002", "Thứ tự mặc định của danh sách", "P0",
     "Có phiếu lập hôm nay và phiếu lập tháng trước.",
     "1. Mở màn danh sách, không đụng vào cột sắp xếp\n"
     "2. So cột Ngày tạo giữa dòng 1 và dòng 10",
     "—",
     "- Phiếu mới nhất nằm trên cùng, Ngày tạo giảm dần từ trên xuống"),

    ("003", "Chỉ có duy nhất một mục menu trỏ vào màn này", "P1",
     "Tài khoản C.",
     "1. Mở phân hệ Tài chính\n"
     "2. Bấm nhóm 'Quản lý tiền' trên thanh menu trái\n"
     "3. Rà toàn bộ chức năng trong bảng vừa mở",
     "—",
     "- Nhóm 'Thanh toán tiền mặt' có 5 chức năng: Phiếu thu, Phiếu chi, Phiếu báo có, Tổng hợp "
     "tiền về ngân hàng, Phiếu ủy nhiệm chi\n"
     "- Chỉ 'Phiếu thu' mở màn 'Danh sách phiếu thu'\n"
     "- Không còn mục nào khác trỏ vào cùng màn này"),

    ("004", "Thêm tham số lạ vào thanh địa chỉ", "P1",
     "Tài khoản A (chỉ thấy 4 phiếu của mình).",
     "1. Mở màn danh sách, ghi lại tổng số phiếu\n"
     "2. Thêm đuôi ?mode=all vào cuối đường dẫn rồi nhấn Enter\n"
     "3. Đếm lại tổng số phiếu",
     "?mode=all",
     "- Trang mở bình thường, không báo lỗi\n"
     "- ⚠️ Tổng số phiếu KHÔNG đổi, vẫn là 4 — tham số lạ không mở rộng được phạm vi dữ liệu"),

    ("005", "Ba cách xem cũ nay là bộ lọc", "P1",
     "Tài khoản C; hệ thống có 8 phiếu Chờ duyệt và 2.304 phiếu Đã duyệt; C tự lập 12 phiếu.",
     "1. Lọc Trạng thái = 'Chờ duyệt' và đếm kết quả\n"
     "2. Đổi sang Trạng thái = 'Đã duyệt' và đếm kết quả\n"
     "3. Xóa lọc trạng thái, chọn Người lập = chính mình và đếm kết quả",
     "—",
     "- Bước 1 ra 8 phiếu, bước 2 ra 2.304 phiếu, bước 3 ra 12 phiếu\n"
     "- Không cần chuyển sang màn khác, tất cả làm ngay trên một màn"),

    ("006", "Bộ lọc được ghi nhớ khi quay lại trong 10 phút", "P1",
     "Tài khoản C.",
     "1. Chọn Trạng thái = 'Chờ duyệt', chờ lưới lọc xong\n"
     "2. Bấm vào một mã phiếu để sang màn chi tiết\n"
     "3. Bấm 'Quay lại' (trong vòng 10 phút)",
     "Trạng thái: Chờ duyệt",
     "- Về lại danh sách, ô Trạng thái vẫn giữ 'Chờ duyệt'\n"
     "- Lưới vẫn chỉ hiện phiếu Chờ duyệt"),

    ("007", "Màn danh sách khi không có phiếu nào", "P1",
     "Tài khoản mới, chưa lập phiếu nào, không có quyền xem nào.",
     "1. Đăng nhập\n"
     "2. Vào " + MENU,
     "—",
     "- Lưới hiện 'Không có dữ liệu phù hợp bộ lọc.'\n"
     "- Dòng đếm ghi 'Không có phiếu nào.'\n"
     "- Nút 'Tạo mới' vẫn dùng được"),

    ("008", "Thông báo khi có phiếu thu gửi duyệt", "P0",
     "Tài khoản F có quyền 'Thủ quỹ duyệt phiếu thu' công ty 4. Tài khoản E cùng công ty 4 vừa "
     "lập và gửi duyệt 1 phiếu thu.",
     "1. Đăng nhập tài khoản F\n"
     "2. Mở chuông thông báo\n"
     "3. Bấm vào dòng thông báo mới nhất",
     "—",
     "- Có thông báo dạng '[TC] Chờ duyệt phiếu thu: <mã phiếu>. Người lập: <tên>', mã phiếu in đậm\n"
     "- Bấm vào thông báo mở đúng màn chi tiết của phiếu đó"),

    ("009", "Thủ quỹ khác công ty không nhận thông báo", "P1",
     "Tài khoản G có quyền thủ quỹ nhưng thuộc công ty 1. Tài khoản E thuộc công ty 4 vừa gửi "
     "duyệt 1 phiếu thu.",
     "1. Đăng nhập tài khoản G\n"
     "2. Mở chuông thông báo",
     "—",
     "- Không có thông báo nào về phiếu vừa gửi của công ty 4"),

    ("010", "Lưu nháp KHÔNG bắn thông báo", "P1",
     "Tài khoản F là thủ quỹ cùng công ty với E.",
     "1. E lập phiếu thu và bấm 'Lưu' (lưu nháp)\n"
     "2. Đăng nhập F, mở chuông thông báo và mở danh sách",
     "—",
     "- F không nhận thông báo nào\n"
     "- F cũng không thấy phiếu nháp này trên danh sách"),
]

S2 = [
    ("001", "Ô tìm nhanh tìm theo mã phiếu", "P0",
     "Có phiếu TPE.PT0826.00032 trong phạm vi quyền.",
     "1. Gõ '00032' vào ô tìm nhanh\n"
     "2. Bấm nút 'Tìm kiếm'",
     "Ô tìm nhanh: 00032",
     "- Lưới còn các phiếu có mã chứa 00032\n"
     "- Dòng đếm cập nhật theo số kết quả"),

    ("002", "Ô tìm nhanh KHÔNG tự tìm khi đang gõ", "P0",
     "Danh sách đang hiện 2.375 phiếu.",
     "1. Gõ '00032' vào ô tìm nhanh\n"
     "2. Chờ 5 giây, KHÔNG bấm nút\n"
     "3. Quan sát lưới",
     "Ô tìm nhanh: 00032",
     "- Lưới KHÔNG đổi\n"
     "- Chỉ khi bấm 'Tìm kiếm' danh sách mới lọc lại"),

    ("003", "Lọc theo mã phiếu đề nghị thu", "P0",
     "Có 1 phiếu thu lập từ phiếu đề nghị TEST.DNTT.00016.",
     "1. Mở 'Tìm kiếm nâng cao'\n"
     "2. Gõ 'TEST.DNTT.00016' vào ô 'Mã phiếu đề nghị thu'",
     "Mã phiếu đề nghị thu: TEST.DNTT.00016",
     "- ⚠️ Lưới tự lọc ngay khi gõ xong, không cần bấm nút\n"
     "- Kết quả có đúng phiếu thu gắn với phiếu đề nghị đó"),

    ("004", "Lọc theo Loại thu", "P0",
     "Phạm vi quyền có 1.900 phiếu 'Thu bán hàng' và 379 phiếu 'Thu nhà cung cấp'.",
     "1. Mở 'Tìm kiếm nâng cao'\n"
     "2. Chọn Loại thu = 'Thu nhà cung cấp'",
     "Loại thu: Thu nhà cung cấp",
     "- Lưới còn 379 dòng, cột Loại thu đều ghi 'Thu nhà cung cấp'\n"
     "- ⚠️ Cột Khách hàng của các dòng này hiện dấu gạch ngang (phiếu thu nhà cung cấp không có "
     "khách hàng)"),

    ("005", "Danh sách Loại thu trong ô lọc", "P1",
     "Tài khoản C.",
     "1. Mở 'Tìm kiếm nâng cao'\n"
     "2. Bấm vào ô Loại thu",
     "—",
     "- Danh sách có 'Thu bán hàng' và 'Thu nhà cung cấp'\n"
     "- ⚠️ 'Thu khác' KHÔNG còn cho chọn, nhưng phiếu cũ mang loại này vẫn hiện đúng tên trên lưới"),

    ("006", "Lọc theo Trạng thái", "P0",
     "Phạm vi quyền có 8 phiếu 'Chờ duyệt'.",
     "1. Mở 'Tìm kiếm nâng cao'\n"
     "2. Chọn Trạng thái = 'Chờ duyệt'",
     "Trạng thái: Chờ duyệt",
     "- Lưới còn 8 dòng, cột Trạng thái của mọi dòng đều ghi 'Chờ duyệt'"),

    ("007", "Danh sách trạng thái trong ô lọc", "P1",
     "Tài khoản C.",
     "1. Mở 'Tìm kiếm nâng cao'\n"
     "2. Bấm vào ô Trạng thái",
     "—",
     "- Danh sách có đúng 4 giá trị: Đang tạo, Chờ duyệt, Đã duyệt, Hủy"),

    ("008", "Lọc Trạng thái = Đang tạo chỉ ra nháp của chính mình", "P0",
     "Tài khoản C có quyền xem tổng công ty, tự lập 1 phiếu nháp; toàn hệ thống có 6 phiếu nháp.",
     "1. Lọc Trạng thái = 'Đang tạo'\n"
     "2. Đếm kết quả và xem cột Người tạo",
     "Trạng thái: Đang tạo",
     "- ⚠️ Chỉ ra 1 phiếu, không phải 6\n"
     "- Cột Người tạo là tên C"),

    ("009", "Lọc theo Người lập", "P1",
     "Có 12 phiếu do tài khoản C lập.",
     "1. Mở 'Tìm kiếm nâng cao'\n"
     "2. Chọn Người lập = tên C",
     "Người lập: DNS Admin",
     "- Lưới còn 12 dòng, cột Người tạo đều là C"),

    ("010", "Lọc theo Người đề nghị", "P1",
     "Có 4 phiếu thu lập từ phiếu đề nghị của 'Bùi Hữu Hanh'.",
     "1. Mở 'Tìm kiếm nâng cao'\n"
     "2. Chọn Người đề nghị = 'Bùi Hữu Hanh'",
     "Người đề nghị: Bùi Hữu Hanh",
     "- Lưới còn 4 dòng, cột Người đề nghị đều là Bùi Hữu Hanh\n"
     "- ⚠️ Đây là người lập PHIẾU ĐỀ NGHỊ, khác cột Người tạo (người lập phiếu thu)"),

    ("011", "Lọc theo Khách hàng", "P0",
     "Có 3 phiếu thu của khách hàng '29TPHPCA-307 - BỘ TƯ LỆNH THỦ ĐÔ HÀ NỘI'.",
     "1. Mở 'Tìm kiếm nâng cao'\n"
     "2. Gõ ít nhất 2 ký tự vào ô Khách hàng rồi chọn khách hàng trong danh sách gợi ý",
     "Khách hàng: BỘ TƯ LỆNH THỦ ĐÔ HÀ NỘI",
     "- Ô này chỉ gợi ý sau khi gõ từ 2 ký tự trở lên\n"
     "- Lưới còn 3 dòng có dòng chi tiết gắn khách hàng đó"),

    ("012", "Lọc theo Số hợp đồng/đơn hàng", "P1",
     "Có 4 phiếu thu có dòng chi tiết gắn hợp đồng chứa 'HĐ-TEST-DNTT'.",
     "1. Mở 'Tìm kiếm nâng cao'\n"
     "2. Gõ 'HĐ-TEST-DNTT' vào ô 'Số hợp đồng/đơn hàng'",
     "Số hợp đồng/đơn hàng: HĐ-TEST-DNTT",
     "- Lưới lọc còn các phiếu có ít nhất một dòng chi tiết gắn hợp đồng khớp\n"
     "- Mở một phiếu trong kết quả thấy đúng số hợp đồng đó ở cột 'Số đơn hàng/Hợp đồng'"),

    ("013", "Lọc khoảng Số tiền", "P0",
     "Có 5 phiếu có Số tiền từ 1.000.000 đến 5.000.000.",
     "1. Nhập 'Số tiền từ' = 1.000.000\n"
     "2. Nhập 'Số tiền đến' = 5.000.000",
     "Số tiền từ: 1,000,000 · Số tiền đến: 5,000,000",
     "- Lưới còn 5 dòng, cột Số tiền đều nằm trong khoảng\n"
     "- ⚠️ So theo cột 'Số tiền' của lưới (là tổng DUYỆT THU), không phải theo số thực thu"),

    ("014", "Chỉ nhập một đầu khoảng Số tiền", "P1",
     "Có phiếu trải nhiều mức tiền.",
     "1. Nhập 'Số tiền từ' = 1.000.000.000, để trống ô còn lại",
     "Số tiền từ: 1,000,000,000",
     "- Kết quả gồm mọi phiếu có Số tiền từ 1 tỷ trở lên, không giới hạn phía trên"),

    ("015", "Lọc khoảng ngày lập", "P0",
     "Có 6 phiếu lập trong tháng 8/2026.",
     "1. Chọn 'Ngày lập từ' = 01/08/2026\n"
     "2. Chọn 'Ngày lập đến' = 31/08/2026",
     "Ngày lập từ: 01/08/2026 · Ngày lập đến: 31/08/2026",
     "- Lưới chỉ còn phiếu có Ngày tạo trong tháng 8/2026"),

    ("016", "Mốc 'Ngày lập đến' lấy trọn ngày", "P0",
     "Có 1 phiếu lập lúc 18:21 ngày 28/08/2026.",
     "1. Chọn 'Ngày lập đến' = 28/08/2026, để trống ô còn lại\n"
     "2. Tìm phiếu lập lúc 18:21 trong kết quả",
     "Ngày lập đến: 28/08/2026",
     "- ⚠️ Phiếu lập lúc 18:21 ngày 28/08/2026 VẪN nằm trong kết quả"),

    ("017", "Kết hợp nhiều điều kiện lọc", "P0",
     "Tài khoản C; có 2 phiếu 'Chờ duyệt' loại 'Thu bán hàng' lập trong tháng 8/2026.",
     "1. Chọn Trạng thái = 'Chờ duyệt'\n"
     "2. Chọn Loại thu = 'Thu bán hàng'\n"
     "3. Chọn khoảng ngày lập 01/08/2026 – 31/08/2026",
     "3 điều kiện như trên",
     "- Các điều kiện cộng dồn (VÀ), kết quả còn 2 phiếu thoả tất cả\n"
     "- Mỗi lần đổi một ô, lưới tự nạp lại"),

    ("018", "Nút 'Làm mới' xóa hết điều kiện lọc", "P0",
     "Đang lọc Trạng thái = 'Chờ duyệt' và ô tìm nhanh có chữ.",
     "1. Bấm nút 'Làm mới'\n"
     "2. Quan sát các ô lọc và lưới",
     "—",
     "- Tất cả ô lọc và ô tìm nhanh trở về trống\n"
     "- Lưới nạp lại đầy đủ theo phạm vi quyền, quay về trang 1\n"
     "- ⚠️ Phạm vi dữ liệu theo quyền KHÔNG đổi"),

    ("019", "Đổi điều kiện lọc khi đang ở trang 5", "P0",
     "Đang xem trang 5 của danh sách 2.375 phiếu.",
     "1. Chuyển tới trang 5\n"
     "2. Chọn Trạng thái = 'Chờ duyệt'",
     "Trạng thái: Chờ duyệt",
     "- Danh sách nhảy về TRANG 1 của kết quả mới\n"
     "- Không bị trang trắng do trang 5 vượt số trang mới"),

    ("020", "Cài đặt bộ lọc — bỏ bớt ô lọc hiển thị", "P1",
     "Khối lọc nâng cao đang có 10 nhóm ô.",
     "1. Bấm 'Cài đặt bộ lọc'\n"
     "2. Bỏ tích 'Số hợp đồng/đơn hàng' và 'Khoảng ngày lập'\n"
     "3. Bấm 'Lưu'",
     "Bỏ tích 2 nhóm ô",
     "- Popup đóng, khối lọc nâng cao còn 8 nhóm ô\n"
     "- Rời màn rồi quay lại vẫn giữ cấu hình này"),

    ("021", "Cài đặt bộ lọc — khôi phục mặc định", "P2",
     "Đã bỏ tích 2 nhóm ô ở trường hợp trên.",
     "1. Bấm 'Cài đặt bộ lọc'\n"
     "2. Bấm 'Khôi phục mặc định' rồi 'Lưu'",
     "—",
     "- Khối lọc nâng cao trở lại đủ 10 nhóm ô theo thứ tự ban đầu"),

    ("022", "Nhóm ô lọc Công ty – Phòng ban – Bộ phận theo quyền", "P0",
     "Tài khoản B có quyền xem theo công ty; tài khoản A không có quyền xem nào.",
     "1. Đăng nhập B, mở 'Tìm kiếm nâng cao', quan sát\n"
     "2. Đăng nhập A, làm lại bước 1",
     "—",
     "- B: có nhóm ô Công ty / Phòng ban / Bộ phận\n"
     "- ⚠️ A: KHÔNG có nhóm ô này, dù dòng 'Công ty – Phòng ban – Bộ phận' vẫn nằm trong cửa sổ "
     "'Cài đặt bộ lọc'"),

    ("023", "Lọc theo Công ty của phiếu đề nghị", "P1",
     "Tài khoản C (quyền tổng công ty); công ty 4 có 60 phiếu thu.",
     "1. Mở 'Tìm kiếm nâng cao'\n"
     "2. Chọn Công ty = công ty 4",
     "Công ty: TPE",
     "- Lưới còn 60 dòng\n"
     "- ⚠️ Lọc theo công ty ghi trên PHIẾU ĐỀ NGHỊ, không phải công ty của phiếu thu"),

    ("024", "Bộ lọc không phá vỡ phạm vi quyền", "P0",
     "Tài khoản A chỉ thấy 4 phiếu; hệ thống có 12 phiếu do 'DNS Admin' lập nhưng đều ngoài phạm "
     "vi của A.",
     "1. Đăng nhập tài khoản A\n"
     "2. Chọn Người lập = 'DNS Admin'",
     "Người lập: DNS Admin",
     "- ⚠️ Kết quả RỖNG — lọc không mở rộng phạm vi dữ liệu ra ngoài quyền của A"),

    ("025", "Tìm từ khoá không khớp gì", "P1",
     "Tài khoản C.",
     "1. Gõ 'zzzz-khong-ton-tai' vào ô tìm nhanh rồi bấm 'Tìm kiếm'",
     "Ô tìm nhanh: zzzz-khong-ton-tai",
     "- Lưới hiện 'Không có dữ liệu phù hợp bộ lọc.'\n"
     "- Không báo lỗi, các nút vẫn dùng được"),
]

S3 = [
    ("001", "Sắp xếp theo Mã phiếu", "P0",
     "Danh sách đang ở thứ tự mặc định.",
     "1. Bấm vào tiêu đề cột 'Mã phiếu'\n"
     "2. Ghi lại thứ tự\n"
     "3. Bấm lần nữa",
     "—",
     "- Lần 1: mã sắp tăng dần; lần 2 đảo thành giảm dần\n"
     "- Danh sách quay về trang 1 sau mỗi lần đổi sắp xếp"),

    ("002", "Sắp xếp theo Số tiền", "P0",
     "Danh sách có phiếu nhiều mức tiền khác nhau.",
     "1. Bấm tiêu đề cột 'Số tiền'\n"
     "2. Kiểm tra dòng đầu và dòng cuối trang",
     "—",
     "- Số tiền sắp tăng dần; bấm lần nữa thì giảm dần\n"
     "- ⚠️ Sắp theo tổng DUYỆT THU, không phải thực thu"),

    ("003", "Sắp xếp theo Ngày tạo và Ngày cập nhật", "P0",
     "Đã bật đủ 2 cột.",
     "1. Bấm tiêu đề cột 'Ngày tạo', kiểm tra thứ tự\n"
     "2. Bấm tiêu đề cột 'Ngày cập nhật', kiểm tra thứ tự",
     "—",
     "- Cả hai cột đều sắp xếp được thật, cả hai chiều\n"
     "- Giờ phút cũng được tính vào thứ tự"),

    ("004", "Sắp xếp vẫn giữ khi chuyển trang", "P1",
     "Đã sắp xếp theo Mã phiếu tăng dần.",
     "1. Bấm sang trang 2\n"
     "2. Quan sát mã phiếu dòng đầu trang 2",
     "—",
     "- Mã dòng đầu trang 2 lớn hơn mã dòng cuối trang 1\n"
     "- Mũi tên sắp xếp trên tiêu đề cột vẫn giữ chiều đã chọn"),

    ("005", "Chuyển trang không làm mất bộ lọc", "P0",
     "Đang lọc Trạng thái = 'Đã duyệt', kết quả 2.304 phiếu.",
     "1. Bấm sang trang 10\n"
     "2. Kiểm tra cột Trạng thái và ô lọc",
     "—",
     "- Mọi dòng vẫn là 'Đã duyệt'\n"
     "- Ô lọc Trạng thái vẫn giữ giá trị, không bị nhảy về trang 1"),

    ("006", "Đổi số dòng/trang", "P0",
     "Đang xem 10 dòng/trang trên 2.375 phiếu.",
     "1. Đổi 'Số dòng/trang' sang 50",
     "Số dòng/trang: 50",
     "- Lưới hiện 50 dòng, dòng đếm ghi 'Hiển thị 1–50 / 2375'\n"
     "- Danh sách quay về trang 1"),

    ("007", "STT đánh số theo trang", "P1",
     "Đang xem 10 dòng/trang.",
     "1. Sang trang 2\n"
     "2. Đọc cột STT dòng đầu và dòng cuối",
     "—",
     "- STT trang 2 chạy từ 11 đến 20, không bắt đầu lại từ 1"),

    ("008", "Mã phiếu là đường dẫn sang màn chi tiết", "P0",
     "Danh sách có phiếu TPE.PT0826.00032.",
     "1. Bấm vào chữ 'TPE.PT0826.00032' ở cột Mã phiếu",
     "—",
     "- Chuyển sang màn chi tiết đúng phiếu đó\n"
     "- Tiêu đề màn ghi 'Chi tiết phiếu thu tiền: TPE.PT0826.00032'"),

    ("009", "Mã phiếu đề nghị thu mở TAB MỚI", "P1",
     "Danh sách có phiếu gắn đề nghị TEST.DNTT.00016.",
     "1. Bấm vào chữ 'TEST.DNTT.00016' ở cột Mã phiếu đề nghị thu",
     "—",
     "- ⚠️ Mở TAB MỚI sang màn chi tiết Phiếu đề nghị thu tiền\n"
     "- Tab đang xem giữ nguyên danh sách, không mất bộ lọc và trang đang xem"),

    ("010", "Cột Khách hàng lấy từ dòng chi tiết đầu tiên", "P1",
     "Có phiếu thu 4 dòng chi tiết, dòng đầu là khách hàng '29TPHPCA-307 - BỘ TƯ LỆNH THỦ ĐÔ HÀ NỘI'.",
     "1. Xem cột Khách hàng của phiếu trên lưới\n"
     "2. Mở màn chi tiết của phiếu đó",
     "—",
     "- Lưới hiện đúng '29TPHPCA-307 - BỘ TƯ LỆNH THỦ ĐÔ HÀ NỘI' (mã - tên)\n"
     "- ⚠️ Màn chi tiết có 4 khách hàng khác nhau; lưới chỉ hiện khách hàng của dòng ĐẦU TIÊN"),

    ("011", "Màu nhãn trạng thái", "P2",
     "Danh sách có cả phiếu 'Chờ duyệt', 'Đang tạo', 'Đã duyệt', 'Hủy'.",
     "1. Quan sát cột Trạng thái",
     "—",
     "- 'Đang tạo', 'Chờ duyệt', 'Hủy' hiển thị nhãn màu đỏ\n"
     "- 'Đã duyệt' hiển thị nhãn màu xanh"),

    ("012", "Nút thao tác trên dòng đổi theo trạng thái và quyền", "P0",
     "Tài khoản F (thủ quỹ, kiêm kế toán thanh toán) có: 1 phiếu 'Đang tạo' do mình lập, 1 phiếu "
     "'Chờ duyệt', 1 phiếu 'Đã duyệt'.",
     "1. Kéo lưới sang phải để thấy cột Hành động\n"
     "2. Quan sát cả 3 dòng",
     "—",
     "- Dòng 'Đang tạo': nút Sửa (bút chì), Xóa (thùng rác đỏ) và menu ba chấm chứa In, Xuất "
     "Excel, Lịch sử\n"
     "- Dòng 'Chờ duyệt': nút Duyệt (dấu tích tròn), In, và menu ba chấm — KHÔNG có Sửa/Xóa\n"
     "- Dòng 'Đã duyệt': In, Xuất Excel, Lịch sử\n"
     "- ⚠️ Nút không đủ điều kiện bị ẩn hẳn, không hiện xám\n"
     "- ⚠️ Danh sách KHÔNG có nút 'Hủy phiếu' — hủy chỉ làm ở màn chi tiết"),

    ("013", "Nút Duyệt trên dòng chỉ điều hướng", "P1",
     "Tài khoản F, có phiếu 'Chờ duyệt'.",
     "1. Bấm nút Duyệt (dấu tích tròn) trên dòng phiếu\n"
     "2. Quan sát",
     "—",
     "- ⚠️ Chỉ MỞ màn chi tiết, KHÔNG duyệt ngay\n"
     "- Phiếu vẫn ở trạng thái Chờ duyệt; thao tác duyệt thật làm ở màn chi tiết"),

    ("014", "Cấu hình cột — ẩn bớt cột", "P1",
     "Lưới đang hiện đủ 13 cột.",
     "1. Bấm nút biểu tượng cấu hình cột\n"
     "2. Bỏ tích 'Người cập nhật' và 'Ngày cập nhật'\n"
     "3. Bấm 'Lưu'",
     "Bỏ tích 2 cột",
     "- Lưới không còn 2 cột đó\n"
     "- Rời màn rồi quay lại vẫn giữ cấu hình này"),

    ("015", "Cấu hình cột — 3 cột bị khoá", "P1",
     "Cửa sổ 'Tuỳ chỉnh cột' đang mở.",
     "1. Thử bỏ tích 'STT', 'Mã phiếu', 'Hành động'",
     "—",
     "- Cả 3 dòng hiện biểu tượng ổ khoá, chữ mờ, không bỏ tích được\n"
     "- Các cột còn lại bỏ tích bình thường"),

    ("016", "Cấu hình cột của màn này không ảnh hưởng màn khác", "P2",
     "Đã ẩn 2 cột ở màn Phiếu thu.",
     "1. Mở màn 'Phiếu chi'\n"
     "2. Quan sát các cột",
     "—",
     "- Màn kia giữ nguyên cấu hình cột riêng"),
]

S4 = [
    ("001", "Mở màn Tạo mới — giá trị điền sẵn", "P0",
     "Tài khoản E có quyền 'Kế toán thanh toán'.",
     "1. Bấm nút 'Tạo mới'\n"
     "2. Quan sát khối 'Thông tin chung'",
     "—",
     "- Tiêu đề màn: 'Thêm phiếu thu tiền'\n"
     "- 'Số phiếu đề nghị' trống, ghi gợi ý 'Nhấn vào đây để chọn phiếu đề nghị thu'\n"
     "- 'Tài khoản nợ' đã chọn sẵn một tài khoản tiền mặt mặc định\n"
     "- 'Tỷ giá (VND)' điền sẵn 1\n"
     "- Loại thu, Loại tiền, Người đề nghị, Phòng ban, Lý do thu đều trống, ghi gợi ý 'Theo phiếu "
     "đề nghị' và KHÔNG nhập được\n"
     "- Bảng Chi tiết trống, hiện dòng 'Chưa chọn phiếu đề nghị thu'\n"
     "- KHÔNG có ô Mã phiếu và ô Người tạo (chỉ có ở màn Sửa)\n"
     "- Cuối trang có 3 nút: 'Lưu', 'Lưu và gửi duyệt', 'Quay lại'"),

    ("002", "Các trường bắt buộc được đánh dấu", "P1",
     "Đang ở màn Tạo mới.",
     "1. Quan sát các dấu sao đỏ",
     "—",
     "- Có dấu sao đỏ: Số phiếu đề nghị, Tài khoản nợ, Người nộp, Tỷ giá (VND), cột 'Số tài khoản "
     "có' và cột 'Số tiền duyệt thu' trong bảng Chi tiết\n"
     "- KHÔNG có dấu sao: Ghi chú, và các ô lấy theo phiếu đề nghị"),

    ("003", "Cửa sổ chọn phiếu đề nghị thu", "P0",
     "Hệ thống có 7 phiếu đề nghị đang Chờ KT duyệt và chưa có phiếu thu.",
     "1. Bấm vào ô 'Số phiếu đề nghị'\n"
     "2. Quan sát cửa sổ mở ra",
     "—",
     "- Cửa sổ 'Chọn phiếu đề nghị thu', phụ đề 'Chỉ phiếu Chờ duyệt và chưa lập phiếu thu'\n"
     "- Có 2 ô tìm: 'Mã phiếu đề nghị' và 'Người lập', kèm nút 'Tìm kiếm' và 'Làm mới'\n"
     "- Bảng có 3 cột: STT, Mã phiếu đề nghị, Người lập\n"
     "- Dòng đếm ghi 'Hiển thị 1–7 / 7 phiếu'"),

    ("004", "Cửa sổ chỉ liệt kê phiếu đề nghị đủ điều kiện", "P0",
     "Phiếu đề nghị X đang Chờ KT duyệt và chưa có phiếu thu; phiếu Y đang Chờ KT duyệt nhưng đã "
     "có phiếu thu; phiếu Z đang ở trạng thái Đang tạo.",
     "1. Mở cửa sổ chọn phiếu đề nghị\n"
     "2. Tìm lần lượt mã của X, Y, Z",
     "—",
     "- Chỉ X xuất hiện\n"
     "- ⚠️ Y không xuất hiện dù vẫn đang Chờ KT duyệt — vì đã có phiếu thu\n"
     "- Z không xuất hiện vì chưa gửi duyệt"),

    ("005", "Tìm trong cửa sổ chọn phiếu đề nghị", "P1",
     "Cửa sổ đang mở với 7 phiếu.",
     "1. Gõ 'TEST.DNTT.00051' vào ô 'Mã phiếu đề nghị'\n"
     "2. Bấm 'Tìm kiếm'\n"
     "3. Bấm 'Làm mới'",
     "Mã phiếu đề nghị: TEST.DNTT.00051",
     "- Sau bước 2: còn đúng 1 dòng\n"
     "- Sau bước 3: điều kiện tìm bị xoá, danh sách trở lại 7 phiếu"),

    ("006", "Chọn phiếu đề nghị — dữ liệu tự kéo về", "P0",
     "Phiếu đề nghị TEST.DNTT.00051 có 3 dòng chi tiết, loại thu 'Thu bán hàng', loại tiền "
     "VietNamDong, người lập 'DNS Admin', phòng ban 'PHÒNG THIẾT BỊ Ô TÔ 3', lý do 'Thu công nợ "
     "quá hạn'.",
     "1. Bấm vào dòng TEST.DNTT.00051 trong cửa sổ\n"
     "2. Quan sát toàn màn",
     "—",
     "- Cửa sổ tự đóng, ô 'Số phiếu đề nghị' hiện mã vừa chọn\n"
     "- Loại thu, Loại tiền, Người đề nghị, Phòng ban, Lý do thu tự điền theo phiếu đề nghị\n"
     "- Bảng Chi tiết nạp đúng 3 dòng, mỗi dòng có sẵn 'Số tài khoản có' và 'Số tiền duyệt thu' "
     "bằng 'Số tiền đề nghị thu'\n"
     "- Có dòng 'Tổng cộng' cuối bảng"),

    ("007", "Không thêm và không xóa dòng chi tiết được", "P0",
     "Đã chọn phiếu đề nghị có 3 dòng.",
     "1. Rà toàn bộ bảng Chi tiết tìm nút thêm dòng / xóa dòng",
     "—",
     "- ⚠️ KHÔNG có nút thêm dòng và không có nút xóa dòng\n"
     "- Số dòng chi tiết luôn đúng bằng số dòng của phiếu đề nghị"),

    ("008", "Sửa Số tiền duyệt thu", "P0",
     "Dòng 1 có Số tiền đề nghị thu 3.000.000, Số tiền duyệt thu đang là 3.000.000.",
     "1. Sửa 'Số tiền duyệt thu' dòng 1 thành 2.000.000\n"
     "2. Quan sát dòng 'Tổng cộng'",
     "Số tiền duyệt thu: 2,000,000",
     "- Ô nhận giá trị mới, hiển thị 2,000,000\n"
     "- Dòng 'Tổng cộng' cột duyệt thu giảm tương ứng\n"
     "- Cột 'Số tiền đề nghị thu' KHÔNG đổi (chỉ đọc)"),

    ("009", "Ô Số tài khoản có chỉ liệt kê tài khoản cấp cuối", "P0",
     "Danh mục tài khoản có tài khoản tổng hợp (đang là cha) và tài khoản cấp cuối; có ít nhất 1 "
     "tài khoản đang khóa.",
     "1. Bấm vào ô 'Số tài khoản có' của một dòng\n"
     "2. Rà danh sách",
     "—",
     "- Chỉ có tài khoản đang hoạt động VÀ là tài khoản cấp cuối\n"
     "- ⚠️ Tài khoản tổng hợp (có tài khoản con) KHÔNG xuất hiện\n"
     "- Tài khoản đang khóa KHÔNG xuất hiện\n"
     "- Nhãn hiển thị dạng 'số hiệu - tên tài khoản'"),

    ("010", "Ô Tỷ giá bị khóa khi loại tiền là VNĐ", "P0",
     "Phiếu đề nghị TEST.DNTT.00051 có loại tiền VietNamDong.",
     "1. Chọn phiếu đề nghị này\n"
     "2. Thử sửa ô 'Tỷ giá (VND)'",
     "Tỷ giá: 25000",
     "- Ô Tỷ giá bị khóa ở giá trị 1, không sửa được\n"
     "- Bảng Chi tiết chỉ có một cột tiền cho mỗi nhóm, tiêu đề phụ ghi 'VND'"),

    ("011", "Phiếu ngoại tệ — bảng có 2 cột tiền mỗi nhóm", "P0",
     "Có phiếu đề nghị loại tiền USD, tỷ giá 25.000.",
     "1. Chọn phiếu đề nghị đó\n"
     "2. Quan sát tiêu đề bảng Chi tiết và ô Tỷ giá\n"
     "3. Nhập 'Số tiền duyệt thu' cột USD = 100",
     "Số tiền duyệt thu (USD): 100",
     "- Ô 'Tỷ giá (VND)' MỞ cho sửa, điền sẵn tỷ giá của phiếu đề nghị\n"
     "- Mỗi nhóm tiền có 2 cột: cột nguyên tệ (USD) và cột VND\n"
     "- Nhập cột USD thì cột VND tự tính = 100 × tỷ giá"),

    ("012", "Lưu nháp thành công", "P0",
     "Đã chọn phiếu đề nghị, nhập Người nộp, giữ nguyên các giá trị điền sẵn.",
     "1. Bấm nút 'Lưu'\n"
     "2. Quan sát thông báo và màn hình sau khi lưu",
     "Người nộp: Nguyễn Văn A",
     "- Thông báo 'Thêm phiếu thu tiền thành công!'\n"
     "- Quay về màn danh sách\n"
     "- Phiếu mới nằm dòng đầu, mã dạng {mã công ty}.PT{tháng năm}.{5 chữ số}, trạng thái 'Đang tạo'\n"
     "- ⚠️ Nút 'Lưu' KHÔNG hỏi xác nhận"),

    ("013", "Lưu và gửi duyệt — có hộp xác nhận", "P0",
     "Form đã điền đủ thông tin hợp lệ.",
     "1. Bấm nút 'Lưu và gửi duyệt'\n"
     "2. Đọc hộp thoại\n"
     "3. Bấm 'Xác nhận'",
     "—",
     "- Hộp 'Xác nhận lưu và gửi duyệt' hỏi 'Bạn đồng ý lưu và duyệt?'\n"
     "- Sau khi xác nhận: thông báo 'Phiếu thu tiền tạo thành công! Phiếu thu tiền cần được duyệt "
     "trước khi có hiệu lực, vui lòng theo dõi thông báo'\n"
     "- Về danh sách, phiếu mới ở trạng thái 'Chờ duyệt', mất nút Sửa/Xóa"),

    ("014", "Hủy hộp xác nhận gửi duyệt", "P1",
     "Hộp 'Xác nhận lưu và gửi duyệt' đang mở.",
     "1. Bấm 'Hủy'",
     "—",
     "- Hộp đóng, vẫn ở form, dữ liệu đã nhập còn nguyên\n"
     "- Không có phiếu nào được tạo"),

    ("015", "Gửi duyệt làm đổi trạng thái phiếu đề nghị", "P0",
     "Phiếu đề nghị TEST.DNTT.00051 đang ở trạng thái 'Chờ KT duyệt'.",
     "1. Lập phiếu thu từ phiếu đề nghị này và bấm 'Lưu và gửi duyệt'\n"
     "2. Mở màn Phiếu đề nghị thu tiền, tìm phiếu TEST.DNTT.00051",
     "—",
     "- Phiếu đề nghị chuyển sang trạng thái 'Đã tạo phiếu thu'\n"
     "- Lịch sử phiếu đề nghị có thêm một mốc đổi trạng thái"),

    ("016", "Lưu nháp KHÔNG đổi trạng thái phiếu đề nghị", "P0",
     "Phiếu đề nghị TEST.DNTT.00051 đang ở 'Chờ KT duyệt'.",
     "1. Lập phiếu thu từ phiếu đề nghị này và bấm 'Lưu' (lưu nháp)\n"
     "2. Mở màn Phiếu đề nghị thu tiền, tìm phiếu TEST.DNTT.00051",
     "—",
     "- ⚠️ Phiếu đề nghị VẪN ở 'Chờ KT duyệt' — lưu nháp không đụng tới phiếu đề nghị\n"
     "- Đây là hành vi đã chốt, không phải lỗi"),

    ("017", "Một phiếu đề nghị chỉ lập được một phiếu thu", "P0",
     "Phiếu đề nghị TEST.DNTT.00051 đã có 1 phiếu thu (kể cả phiếu thu còn ở trạng thái nháp).",
     "1. Bấm 'Tạo mới', mở cửa sổ chọn phiếu đề nghị\n"
     "2. Tìm mã TEST.DNTT.00051",
     "—",
     "- Không tìm thấy — phiếu đề nghị đã bị loại khỏi danh sách chọn\n"
     "- Nếu ép lưu bằng cách khác thì hệ thống báo 'Đề nghị thu tiền đã lập phiếu thu tiền' và "
     "không tạo phiếu thứ hai"),

    ("018", "Hai người cùng lập phiếu thu cho một phiếu đề nghị", "P0",
     "Hai kế toán E1 và E2 cùng mở màn Tạo mới, cùng chọn phiếu đề nghị TEST.DNTT.00051.",
     "1. E1 bấm 'Lưu' thành công\n"
     "2. E2 (chưa tải lại) bấm 'Lưu'",
     "—",
     "- E2 nhận lỗi 'Đề nghị thu tiền đã lập phiếu thu tiền'\n"
     "- ⚠️ Chỉ có ĐÚNG MỘT phiếu thu được tạo, không sinh 2 phiếu trùng"),

    ("019", "Chống bấm nút lưu hai lần", "P1",
     "Form đã điền đủ thông tin.",
     "1. Bấm 'Lưu' rồi bấm liên tiếp thêm 2 lần thật nhanh\n"
     "2. Về danh sách đếm số phiếu vừa tạo",
     "—",
     "- Chỉ tạo ra ĐÚNG 1 phiếu"),

    ("020", "Mã phiếu sinh tự động theo công ty và tháng", "P1",
     "Người lập thuộc công ty có mã 'TPE'; hôm nay là tháng 09/2026.",
     "1. Lập và lưu 1 phiếu mới\n"
     "2. Đọc mã phiếu vừa tạo",
     "—",
     "- Mã có dạng TPE.PT0926.00001 (mã công ty + PT + tháng năm + 5 chữ số)\n"
     "- Người dùng KHÔNG nhập được mã, ô Mã phiếu chỉ hiện ở màn Sửa và ở chế độ chỉ đọc"),

    ("021", "Cảnh báo khi rời form đang nhập dở", "P1",
     "Form Tạo mới đã chọn phiếu đề nghị và nhập Người nộp, chưa lưu.",
     "1. Bấm nút 'Quay lại'",
     "—",
     "- Hiện hộp cảnh báo còn thông tin chưa lưu\n"
     "- Chọn ở lại thì dữ liệu còn nguyên; chọn thoát thì về danh sách và mất dữ liệu"),
]

S5 = [
    ("001", "Mở màn Sửa từ danh sách", "P0",
     "Tài khoản E có phiếu thu TPE.PT0926.00001 ở trạng thái 'Đang tạo' do chính mình lập.",
     "1. Kéo lưới sang phải, bấm nút Sửa (bút chì) trên dòng phiếu\n"
     "2. Quan sát form",
     "—",
     "- Tiêu đề màn: 'Sửa phiếu thu tiền'\n"
     "- Có THÊM ô 'Mã phiếu' và ô 'Người tạo', cả hai ở chế độ chỉ đọc\n"
     "- Các ô còn lại nạp đúng dữ liệu đã lưu\n"
     "- Bảng Chi tiết nạp đủ dòng, cột 'Số tiền duyệt thu' vẫn sửa được\n"
     "- ⚠️ KHÔNG có nhóm cột 'Số tiền thực thu'"),

    ("002", "Sửa và lưu nháp lại", "P0",
     "Đang ở màn Sửa phiếu nháp.",
     "1. Sửa ô 'Người nộp' và ô 'Ghi chú'\n"
     "2. Bấm 'Lưu'\n"
     "3. Mở lại phiếu kiểm tra",
     "Người nộp: Trần Thị B · Ghi chú: Bổ sung ghi chú lần 2",
     "- Thông báo 'Cập nhật phiếu thu tiền thành công!'\n"
     "- Phiếu vẫn ở trạng thái 'Đang tạo'\n"
     "- Cột 'Người cập nhật' và 'Ngày cập nhật' trên lưới đổi theo người vừa sửa"),

    ("003", "Sửa rồi gửi duyệt luôn", "P0",
     "Đang ở màn Sửa phiếu nháp.",
     "1. Sửa 'Số tiền duyệt thu' của một dòng\n"
     "2. Bấm 'Lưu và gửi duyệt' rồi 'Xác nhận'",
     "—",
     "- Phiếu chuyển sang 'Chờ duyệt', mất nút Sửa/Xóa\n"
     "- Phiếu đề nghị chuyển sang 'Đã tạo phiếu thu'\n"
     "- Thủ quỹ cùng công ty nhận thông báo"),

    ("004", "Đổi sang phiếu đề nghị khác khi sửa", "P1",
     "Đang sửa phiếu nháp gắn đề nghị X; đề nghị Y đang Chờ KT duyệt và chưa có phiếu thu.",
     "1. Bấm vào ô 'Số phiếu đề nghị', chọn Y\n"
     "2. Quan sát bảng Chi tiết\n"
     "3. Bấm 'Lưu'",
     "Đổi từ X sang Y",
     "- Bảng Chi tiết nạp lại theo Y, các dòng cũ của X bị thay hết\n"
     "- Lưu thành công; phiếu thu nay gắn với Y"),

    ("005", "Không sửa được phiếu đã gửi duyệt", "P0",
     "Phiếu TPE.PT0826.00032 do chính mình lập, đang ở 'Chờ duyệt'.",
     "1. Kéo lưới sang phải quan sát cột Hành động của dòng đó\n"
     "2. Gõ thẳng đường dẫn màn Sửa của phiếu này lên thanh địa chỉ",
     "—",
     "- Trên lưới KHÔNG có nút Sửa\n"
     "- Gõ đường dẫn thì hệ thống chặn, báo 'Phiếu thu đã gửi duyệt hoặc đã duyệt, không sửa được'"),

    ("006", "Không sửa được phiếu đã duyệt", "P0",
     "Phiếu TPE.PT0826.00030 ở trạng thái 'Đã duyệt'.",
     "1. Mở màn chi tiết phiếu này\n"
     "2. Quan sát các nút cuối màn",
     "—",
     "- KHÔNG có nút 'Sửa' và không có nút 'Xóa'\n"
     "- Chỉ còn 'In', 'Xuất Excel', 'Quay lại'"),

    ("007", "Tài khoản đã khóa trên phiếu cũ vẫn hiện đúng tên", "P0",
     "Phiếu nháp đang gắn tài khoản 'Số tài khoản có' mà tài khoản đó vừa bị khóa trong danh mục.",
     "1. Mở màn Sửa phiếu này\n"
     "2. Quan sát ô 'Số tài khoản có' của dòng đó",
     "—",
     "- ⚠️ Ô vẫn hiện ĐÚNG tên tài khoản đã lưu, không bị trống\n"
     "- Nếu mở danh sách chọn thì tài khoản đã khóa không nằm trong các lựa chọn mới\n"
     "- Lưu lại mà không đụng ô này thì giá trị cũ được giữ nguyên"),

    ("008", "Cảnh báo khi rời màn Sửa đang nhập dở", "P1",
     "Đang sửa ô Người nộp, chưa bấm Lưu.",
     "1. Bấm 'Quay lại'",
     "—",
     "- Hiện hộp cảnh báo còn thông tin chưa lưu\n"
     "- ⚠️ Vừa mở màn Sửa mà chưa gõ gì thì bấm 'Quay lại' KHÔNG hiện hộp này"),
]

S6 = [
    ("001", "Mở màn chi tiết", "P0",
     "Phiếu TPE.PT0826.00032 ở trạng thái 'Chờ duyệt', 4 dòng chi tiết.",
     "1. Bấm vào mã phiếu trên danh sách\n"
     "2. Quan sát toàn màn",
     "—",
     "- Tiêu đề: 'Chi tiết phiếu thu tiền: TPE.PT0826.00032'\n"
     "- Khối 'Thông tin chung' đủ 11 ô ở chế độ chỉ đọc: Số phiếu đề nghị, Mã phiếu, Tài khoản "
     "nợ, Loại thu, Người nộp, Loại tiền, Tỷ giá (VND), Người đề nghị, Phòng ban, Người tạo, "
     "Lý do thu\n"
     "- Khối 'Chi tiết' có bảng đủ 4 dòng và dòng 'Tổng cộng'\n"
     "- Khối 'Ghi chú' ở dưới cùng\n"
     "- Có khối 'Lịch sử' thu gọn, kèm nút 'Xem lịch sử'"),

    ("002", "Nhóm cột Số tiền thực thu chỉ có ở màn chi tiết", "P0",
     "Cùng một phiếu nháp.",
     "1. Mở màn Tạo mới, quan sát tiêu đề bảng Chi tiết\n"
     "2. Mở màn Sửa của phiếu đó, quan sát tiêu đề bảng\n"
     "3. Mở màn chi tiết của phiếu đó, quan sát tiêu đề bảng",
     "—",
     "- Bước 1 và 2: bảng có 'Số tiền đề nghị thu' và 'Số tiền duyệt thu', KHÔNG có 'Số tiền thực thu'\n"
     "- ⚠️ Bước 3: bảng có THÊM nhóm cột 'Số tiền thực thu'"),

    ("003", "Ô Số tiền thực thu chỉ mở khi đủ điều kiện", "P0",
     "Tài khoản F là thủ quỹ. Phiếu X đang 'Chờ duyệt', phiếu Y đã 'Đã duyệt'.",
     "1. Mở chi tiết phiếu X, quan sát cột 'Số tiền thực thu'\n"
     "2. Mở chi tiết phiếu Y, quan sát cột tương ứng",
     "—",
     "- Phiếu X: ô NHẬP được, tiêu đề cột có dấu sao đỏ\n"
     "- ⚠️ Phiếu Y: chỉ hiện số, không nhập được, không có dấu sao"),

    ("004", "Ô trống hiển thị dấu gạch ngang", "P1",
     "Phiếu thu nhà cung cấp (không có khách hàng), có dòng chi tiết không ghi chú.",
     "1. Mở màn chi tiết phiếu đó",
     "—",
     "- Cột Khách hàng và cột Ghi chú của dòng hiện dấu gạch ngang, không để trắng trơn"),

    ("005", "Nút cuối màn chi tiết theo trạng thái và quyền", "P0",
     "Tài khoản F (thủ quỹ kiêm kế toán thanh toán): phiếu P1 'Đang tạo' của F; phiếu P2 'Chờ "
     "duyệt'; phiếu P3 'Đã duyệt'; phiếu P4 loại 'Thu khác'.",
     "1. Lần lượt mở chi tiết P1, P2, P3, P4\n"
     "2. Ghi lại các nút cuối màn",
     "—",
     "- P1: 'Sửa', 'In', 'Xuất Excel', 'Xóa', 'Quay lại'\n"
     "- P2: 'Duyệt phiếu thu', 'Hủy phiếu thu', 'In', 'Xuất Excel', 'Quay lại'\n"
     "- P3: 'In', 'Xuất Excel', 'Quay lại'\n"
     "- ⚠️ P4: KHÔNG có nút 'In' (loại Thu khác không có mẫu in)"),

    ("006", "Mở phiếu bằng mã không tồn tại", "P1",
     "Tài khoản C.",
     "1. Gõ đường dẫn màn chi tiết với mã phiếu không có thật",
     "—",
     "- Hệ thống báo không tìm thấy dữ liệu\n"
     "- Không treo trang, không hiện màn chi tiết trắng"),

    ("007", "Nút Quay lại giữ bộ lọc", "P1",
     "Trước đó danh sách đang lọc Trạng thái 'Chờ duyệt' ở trang 2.",
     "1. Mở một phiếu rồi bấm 'Quay lại'",
     "—",
     "- Về màn danh sách, điều kiện lọc 'Chờ duyệt' vẫn còn"),
]

S7 = [
    ("001", "Duyệt phiếu thu — luồng đầy đủ", "P0",
     "⚠️ CHỈ LÀM TRÊN PHIẾU DO CHÍNH MÌNH TẠO. Tài khoản F là thủ quỹ. Phiếu P đang 'Chờ duyệt', "
     "3 dòng, tổng duyệt thu 1.309.236.267.",
     "1. Mở màn chi tiết phiếu P\n"
     "2. Nhập 'Số tiền thực thu' cho từng dòng đúng bằng số duyệt thu\n"
     "3. Bấm 'Duyệt phiếu thu'\n"
     "4. Mở lại phiếu và mở màn Phiếu đề nghị thu tiền tương ứng",
     "Thực thu = duyệt thu từng dòng",
     "- Thông báo 'Duyệt phiếu thu thành công!'\n"
     "- Hệ thống quay về màn danh sách\n"
     "- Phiếu P chuyển sang 'Đã duyệt', ghi người duyệt và ngày hạch toán là hôm nay\n"
     "- Phiếu đề nghị tương ứng chuyển sang 'Đã hạch toán' và được ghi số tiền thực thu\n"
     "- ⚠️ THAO TÁC NÀY KHÔNG HOÀN TÁC ĐƯỢC — hệ thống đã ghi bút toán vào sổ kế toán"),

    ("002", "Duyệt với số thực thu nhỏ hơn duyệt thu", "P0",
     "⚠️ Phiếu do chính mình tạo. Dòng 1 duyệt thu 500.000.",
     "1. Nhập 'Số tiền thực thu' dòng 1 = 300.000\n"
     "2. Bấm 'Duyệt phiếu thu'\n"
     "3. Mở lại phiếu và xem cột 'Số tiền' trên màn danh sách",
     "Thực thu: 300,000",
     "- Duyệt thành công\n"
     "- Màn chi tiết hiện thực thu 300.000, duyệt thu vẫn 500.000\n"
     "- ⚠️ Cột 'Số tiền' trên LƯỚI vẫn hiện 500.000 (tổng duyệt thu) — đây là hành vi đúng"),

    ("003", "Chặn số thực thu vượt số duyệt thu", "P0",
     "Phiếu đang 'Chờ duyệt', dòng 1 có duyệt thu 3.000.000.",
     "1. Gõ 9.000.000 vào ô 'Số tiền thực thu' dòng 1\n"
     "2. Quan sát ô\n"
     "3. Bấm 'Duyệt phiếu thu'",
     "Thực thu: 9,000,000",
     "- ⚠️ Ô CHO GÕ (không tự kéo số về như cổng cũ) nhưng viền đỏ\n"
     "- Dưới ô hiện chữ đỏ 'Không được lớn hơn số tiền duyệt thu (3,000,000)'\n"
     "- Bấm Duyệt bị chặn, phiếu vẫn ở 'Chờ duyệt', không ghi bút toán nào"),

    ("004", "Số thực thu âm", "P1",
     "Phiếu đang 'Chờ duyệt'.",
     "1. Thử gõ số âm vào ô 'Số tiền thực thu'\n"
     "2. Bấm 'Duyệt phiếu thu'",
     "Thực thu: -1000",
     "- Ô không nhận dấu trừ, hoặc nếu lọt thì hệ thống báo 'Không được âm'\n"
     "- Phiếu không được duyệt"),

    ("005", "Nút Phân bổ rải tiền xuống từng dòng", "P0",
     "Phiếu 'Chờ duyệt' có 3 dòng, duyệt thu lần lượt 3.000.000 · 1.231.401.600 · 74.834.667.",
     "1. Nhập 'Số tiền phân bổ' = 5.000.000\n"
     "2. Bấm nút 'Phân bổ'\n"
     "3. Quan sát cột 'Số tiền thực thu' của cả 3 dòng",
     "Số tiền phân bổ: 5,000,000",
     "- Dòng 1 nhận 3.000.000 (tối đa bằng duyệt thu của nó)\n"
     "- Dòng 2 nhận 2.000.000 (phần còn lại)\n"
     "- Dòng 3 nhận 0\n"
     "- ⚠️ Chỉ điền hộ vào ô, CHƯA ghi gì xuống hệ thống; vẫn sửa tay từng ô được"),

    ("006", "Phân bổ nhiều hơn tổng duyệt thu", "P1",
     "Phiếu có tổng duyệt thu 1.309.236.267.",
     "1. Nhập 'Số tiền phân bổ' = 2.000.000.000\n"
     "2. Bấm 'Phân bổ'",
     "Số tiền phân bổ: 2,000,000,000",
     "- Mỗi dòng nhận tối đa bằng duyệt thu của nó, không dòng nào vượt\n"
     "- Phần tiền thừa không được rải đi đâu, không sinh dòng mới"),

    ("007", "Khối Phân bổ chỉ hiện với người được duyệt", "P1",
     "Tài khoản E (không phải thủ quỹ) mở phiếu 'Chờ duyệt'.",
     "1. Quan sát phía trên bảng Chi tiết",
     "—",
     "- KHÔNG có ô 'Số tiền phân bổ' và nút 'Phân bổ'\n"
     "- Cùng điều kiện hiện với ô nhập 'Số tiền thực thu'"),

    ("008", "Chặn duyệt lại phiếu đã duyệt", "P0",
     "Hai thủ quỹ F1 và F2 cùng mở phiếu P đang 'Chờ duyệt'.",
     "1. F1 nhập thực thu và bấm 'Duyệt phiếu thu' thành công\n"
     "2. F2 (chưa tải lại trang) bấm 'Duyệt phiếu thu'\n"
     "3. Kiểm tra sổ kế toán của phiếu P",
     "—",
     "- F2 nhận thông báo 'Phiếu thu tiền đã được duyệt!'\n"
     "- ⚠️ Sổ kế toán chỉ có MỘT bộ bút toán, không bị ghi trùng\n"
     "- Người duyệt trên phiếu vẫn là F1"),

    ("009", "Chống bấm nút Duyệt hai lần", "P0",
     "Phiếu 'Chờ duyệt', đã nhập đủ số thực thu.",
     "1. Bấm 'Duyệt phiếu thu' liên tiếp 3 lần thật nhanh\n"
     "2. Kiểm tra sổ kế toán và lịch sử phiếu",
     "—",
     "- Phiếu chỉ chuyển trạng thái MỘT lần\n"
     "- Chỉ một bộ bút toán được ghi\n"
     "- Lịch sử không có bản ghi trùng"),

    ("010", "Dòng có thực thu bằng 0 không sinh bút toán", "P1",
     "⚠️ Phiếu do chính mình tạo, có 3 dòng; để dòng 3 có thực thu = 0.",
     "1. Nhập thực thu dòng 1 và 2, để dòng 3 bằng 0\n"
     "2. Bấm 'Duyệt phiếu thu'\n"
     "3. Đối chiếu sổ kế toán",
     "Dòng 3: 0",
     "- Duyệt thành công\n"
     "- ⚠️ Sổ kế toán chỉ có bút toán cho dòng 1 và dòng 2, không có dòng 3"),

    ("011", "Ngày hạch toán mặc định là hôm nay", "P1",
     "⚠️ Phiếu do chính mình tạo. Hôm nay là 03/09/2026.",
     "1. Duyệt phiếu mà không đụng tới ngày hạch toán\n"
     "2. Mở lại phiếu",
     "—",
     "- Ngày hạch toán của phiếu là 03/09/2026"),

    ("012", "Duyệt phiếu không ở trạng thái Chờ duyệt", "P0",
     "Phiếu nháp P1 (Đang tạo) do chính mình lập; tài khoản F là thủ quỹ.",
     "1. Mở màn chi tiết P1\n"
     "2. Quan sát các nút",
     "—",
     "- KHÔNG có nút 'Duyệt phiếu thu' và 'Hủy phiếu thu'\n"
     "- Cột 'Số tiền thực thu' không nhập được\n"
     "- ⚠️ Chỉ phiếu ở đúng trạng thái 'Chờ duyệt' mới duyệt được"),
]

S8 = [
    ("001", "Hủy phiếu thu — luồng đầy đủ", "P0",
     "⚠️ CHỈ LÀM TRÊN PHIẾU DO CHÍNH MÌNH TẠO. Tài khoản F là thủ quỹ, phiếu P đang 'Chờ duyệt'.",
     "1. Mở màn chi tiết phiếu P\n"
     "2. Bấm 'Hủy phiếu thu'\n"
     "3. Nhập 'Lý do hủy'\n"
     "4. Bấm 'Xác nhận'\n"
     "5. Mở lại phiếu và mở phiếu đề nghị tương ứng",
     "Lý do hủy: Khách hàng chưa chuyển tiền",
     "- Cửa sổ 'Hủy phiếu thu tiền' có phụ đề 'Phiếu thu: <mã phiếu>' và ô 'Lý do hủy' bắt buộc\n"
     "- Thông báo 'Hủy phiếu thu thành công!'\n"
     "- Phiếu P chuyển sang 'Hủy', lý do hủy được ghi vào ô Ghi chú của phiếu\n"
     "- Phiếu đề nghị tương ứng chuyển sang 'Hủy'\n"
     "- ⚠️ KHÔNG có bút toán nào được ghi vào sổ kế toán"),

    ("002", "Hủy khi chưa nhập lý do", "P0",
     "Cửa sổ 'Hủy phiếu thu tiền' đang mở, ô Lý do hủy còn trống.",
     "1. Bấm 'Xác nhận' mà không nhập gì",
     "—",
     "- Ô 'Lý do hủy' viền đỏ, dưới ô hiện chữ đỏ 'Lý do hủy – Bắt buộc nhập'\n"
     "- Cửa sổ KHÔNG đóng, phiếu giữ nguyên trạng thái 'Chờ duyệt'"),

    ("003", "Đóng cửa sổ hủy", "P0",
     "Cửa sổ 'Hủy phiếu thu tiền' đang mở, đã nhập lý do.",
     "1. Bấm 'Đóng'\n"
     "2. Tải lại màn chi tiết",
     "—",
     "- Cửa sổ đóng, phiếu VẪN ở 'Chờ duyệt'\n"
     "- Ghi chú của phiếu chưa bị ghi đè bởi lý do hủy"),

    ("004", "Lý do hủy quá 1000 ký tự", "P1",
     "Cửa sổ hủy đang mở.",
     "1. Dán 1.200 ký tự vào ô 'Lý do hủy'\n"
     "2. Bấm 'Xác nhận'",
     "Chuỗi 1.200 ký tự",
     "- Hệ thống báo 'Tối đa 1000 ký tự'\n"
     "- Phiếu không bị hủy"),

    ("005", "Hủy phiếu là ngõ cụt — không lập lại được", "P0",
     "Phiếu thu P vừa bị hủy; phiếu đề nghị tương ứng là X.",
     "1. Mở màn Phiếu thu, bấm 'Tạo mới'\n"
     "2. Mở cửa sổ chọn phiếu đề nghị, tìm mã X\n"
     "3. Mở màn chi tiết phiếu đề nghị X, tìm nút 'Tạo phiếu thu'",
     "—",
     "- ⚠️ X KHÔNG xuất hiện trong cửa sổ chọn, dù phiếu thu đã bị hủy\n"
     "- ⚠️ Nút 'Tạo phiếu thu' ở màn đề nghị cũng không hiện\n"
     "- Đây là quy tắc nghiệp vụ ĐÃ CHỐT, không phải lỗi"),

    ("006", "Hủy phiếu không ở trạng thái Chờ duyệt", "P0",
     "Phiếu đã 'Đã duyệt'; tài khoản F là thủ quỹ.",
     "1. Mở màn chi tiết phiếu đó\n"
     "2. Quan sát các nút",
     "—",
     "- KHÔNG có nút 'Hủy phiếu thu'\n"
     "- Phiếu đã duyệt không hủy được từ màn này"),

    ("007", "Không có nút Hủy trên màn danh sách", "P1",
     "Tài khoản F là thủ quỹ, danh sách có phiếu 'Chờ duyệt'.",
     "1. Kéo lưới sang phải, mở menu ba chấm của dòng phiếu 'Chờ duyệt'",
     "—",
     "- Không có mục 'Hủy phiếu' ở cột Hành động lẫn trong menu ba chấm\n"
     "- Muốn hủy phải vào màn chi tiết"),

    ("008", "Chống bấm Xác nhận hủy hai lần", "P1",
     "Đã nhập lý do hủy, cửa sổ đang mở.",
     "1. Bấm 'Xác nhận' liên tiếp 3 lần thật nhanh\n"
     "2. Mở lịch sử phiếu",
     "—",
     "- Phiếu chỉ chuyển trạng thái MỘT lần\n"
     "- Lịch sử chỉ có một dòng đổi trạng thái"),
]

S9 = [
    ("001", "Xóa phiếu nháp — luồng đầy đủ", "P0",
     "Tài khoản E có phiếu TPE.PT0926.00001 ở trạng thái 'Đang tạo' do chính mình lập.",
     "1. Mở màn chi tiết phiếu (hoặc bấm nút Xóa trên dòng)\n"
     "2. Bấm 'Xóa'\n"
     "3. Đọc hộp xác nhận rồi bấm 'Xóa'",
     "—",
     "- Hộp 'Xác nhận xóa' ghi 'Bạn có chắc muốn xóa phiếu thu tiền <mã phiếu>?'\n"
     "- Thông báo 'Xóa phiếu thu thành công!'\n"
     "- Dòng biến mất khỏi danh sách, tổng số phiếu giảm đúng 1"),

    ("002", "Hủy hộp xác nhận xóa", "P0",
     "Hộp 'Xác nhận xóa' đang mở.",
     "1. Bấm 'Hủy'",
     "—",
     "- Hộp đóng, phiếu còn nguyên, tổng số phiếu không đổi"),

    ("003", "Xóa phiếu nháp KHÔNG trả trạng thái phiếu đề nghị", "P0",
     "Phiếu nháp gắn với phiếu đề nghị X đang ở 'Chờ KT duyệt'.",
     "1. Xóa phiếu thu nháp\n"
     "2. Mở màn Phiếu đề nghị thu tiền, tìm X\n"
     "3. Quay lại màn Phiếu thu, mở cửa sổ chọn phiếu đề nghị và tìm X",
     "—",
     "- X vẫn ở 'Chờ KT duyệt' (lưu nháp vốn không đụng tới phiếu đề nghị)\n"
     "- ⚠️ X XUẤT HIỆN LẠI trong cửa sổ chọn — lập được phiếu thu mới cho X"),

    ("004", "Không xóa được phiếu đã gửi duyệt hoặc đã duyệt", "P0",
     "Phiếu P2 'Chờ duyệt' và phiếu P3 'Đã duyệt', cả hai do chính mình lập.",
     "1. Kéo lưới sang phải, quan sát cột Hành động của 2 dòng\n"
     "2. Mở màn chi tiết từng phiếu",
     "—",
     "- Cả trên lưới lẫn màn chi tiết đều KHÔNG có nút Xóa\n"
     "- Ép gọi chức năng Xóa thì hệ thống báo 'Phiếu thu đã gửi duyệt hoặc đã duyệt, không xóa được'"),

    ("005", "Xóa phiếu kéo theo toàn bộ dòng chi tiết", "P0",
     "Phiếu nháp có 3 dòng chi tiết.",
     "1. Xóa phiếu\n"
     "2. Lọc theo số hợp đồng của một dòng trong phiếu vừa xóa",
     "—",
     "- Phiếu vừa xóa không còn xuất hiện trong kết quả\n"
     "- Không còn dữ liệu sót gây kết quả lạ"),

    ("006", "Xóa rồi lập phiếu mới — mã không dùng lại", "P2",
     "Vừa xóa phiếu TPE.PT0926.00001.",
     "1. Lập và lưu 1 phiếu mới",
     "—",
     "- Mã mới là TPE.PT0926.00002 hoặc lớn hơn, không dùng lại mã đã xóa"),
]

S10 = [
    ("001", "In phiếu từ màn chi tiết", "P0",
     "Phiếu TPE.PT0826.00032 loại 'Thu bán hàng', 4 dòng chi tiết.",
     "1. Mở màn chi tiết phiếu\n"
     "2. Bấm nút 'In'",
     "—",
     "- Mở TAB MỚI hiển thị bản in\n"
     "- Bản in có ĐỦ 2 LIÊN: 'Liên số: 1' và 'Liên số: 2', nội dung giống hệt nhau\n"
     "- Đầu mỗi liên có ảnh tiêu đề thư công ty (logo, tên, địa chỉ, điện thoại, email, website)\n"
     "- Trình duyệt tự mở hộp thoại in; đóng hộp thoại vẫn xem được bản in trên trang"),

    ("002", "Nội dung bản in khớp dữ liệu phiếu", "P0",
     "Phiếu TPE.PT0826.00032: ngày 28/08/2026, người nộp '1111', người đề nghị 'DNS Admin', "
     "phòng ban 'PHÒNG THIẾT BỊ Ô TÔ 3', lý do 'Thu tiền theo tiến độ hợp đồng', tài khoản nợ "
     "12131, tài khoản có 1311, tổng 3.811.802.567.",
     "1. Mở bản in\n"
     "2. Đối chiếu từng dòng với màn chi tiết",
     "—",
     "- Tiêu đề 'PHIẾU THU', dưới là ngày bằng chữ và 'Số: <mã phiếu>'\n"
     "- Có dòng 'Nợ: 12131' và 'Có: 1311' kèm số tiền\n"
     "- Có 'Người nộp tiền', 'Người đề nghị', 'Phòng ban', 'Lý do thu'\n"
     "- Bảng in có 4 cột: STT, Khách hàng, Số đơn hàng/Hợp đồng, Số tiền, Ghi chú; kèm dòng "
     "'Tổng cộng'\n"
     "- Có dòng 'Bằng chữ:' đọc đúng số tiền tổng\n"
     "- Cuối mỗi liên có 5 ô ký: BAN GIÁM ĐỐC, KẾ TOÁN TRƯỞNG, NGƯỜI NỘP TIỀN, NGƯỜI LẬP PHIẾU, "
     "THỦ QUỸ"),

    ("003", "Loại thu 'Thu khác' không in được", "P0",
     "Có phiếu cũ thuộc loại 'Thu khác'.",
     "1. Mở màn chi tiết phiếu đó, quan sát các nút\n"
     "2. Kéo lưới sang phải, quan sát cột Hành động của dòng đó\n"
     "3. Gõ thẳng đường dẫn màn In của phiếu này",
     "—",
     "- Cả màn chi tiết lẫn lưới đều KHÔNG có nút 'In'\n"
     "- Gõ đường dẫn thì hệ thống báo lỗi không có mẫu in, không hiện trang trắng"),

    ("004", "In phiếu từ danh sách", "P1",
     "Danh sách có phiếu TPE.PT0826.00032.",
     "1. Kéo lưới sang phải, bấm nút In (máy in) trên dòng phiếu",
     "—",
     "- Mở tab mới đúng bản in của phiếu đó, giống hệt khi in từ màn chi tiết"),

    ("005", "In phiếu không có quyền xem", "P0",
     "Tài khoản A không xem được phiếu TPE.PT0826.00032.",
     "1. Gõ thẳng đường dẫn màn In của phiếu này",
     "—",
     "- Hệ thống từ chối, báo 'Bạn không có quyền xem phiếu thu này'\n"
     "- Không hiển thị nội dung phiếu"),

    ("006", "In lại phiếu không làm đổi dữ liệu", "P2",
     "Phiếu TPE.PT0826.00032.",
     "1. In phiếu 3 lần\n"
     "2. Mở lịch sử thay đổi của phiếu",
     "—",
     "- Trạng thái, người cập nhật, ngày cập nhật KHÔNG đổi\n"
     "- Lịch sử không phát sinh bản ghi mới"),

    ("007", "Xuất Excel một phiếu", "P0",
     "Phiếu TPE.PT0826.00032.",
     "1. Mở màn chi tiết, bấm 'Xuất Excel'\n"
     "2. Mở tệp tải về",
     "—",
     "- Tên tệp tải về: phieu_thu.xlsx\n"
     "- Nội dung là ĐÚNG MỘT phiếu vừa xem, không phải cả danh sách\n"
     "- Các ô khớp với màn chi tiết và với bản in"),

    ("008", "Xuất Excel được cả loại 'Thu khác'", "P1",
     "Phiếu cũ thuộc loại 'Thu khác'.",
     "1. Mở màn chi tiết phiếu đó\n"
     "2. Bấm 'Xuất Excel'",
     "—",
     "- ⚠️ Xuất được bình thường, khác với nút In (In bị ẩn với loại này)"),

    ("009", "Xuất Excel từ danh sách", "P1",
     "Danh sách có phiếu bất kỳ.",
     "1. Kéo lưới sang phải, bấm nút Xuất Excel trên dòng phiếu",
     "—",
     "- Tải về tệp phieu_thu.xlsx của đúng phiếu đó\n"
     "- ⚠️ Màn này KHÔNG có chức năng xuất Excel cả danh sách"),

    ("010", "Xuất Excel không có quyền xem", "P0",
     "Tài khoản A không xem được phiếu.",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Xuất Excel cho phiếu đó",
     "—",
     "- Hệ thống từ chối, báo 'Bạn không có quyền xem phiếu thu này'\n"
     "- Ghi chú: trường hợp này dành cho tester kỹ thuật"),
]

S11 = [
    ("001", "Mở lịch sử từ danh sách", "P0",
     "Phiếu vừa được tạo, chưa sửa lần nào.",
     "1. Kéo lưới sang phải, mở menu ba chấm của dòng phiếu\n"
     "2. Bấm 'Lịch sử'",
     "—",
     "- Cửa sổ 'Lịch sử thay đổi' mở, phụ đề ghi 'Phiếu: <mã phiếu>'\n"
     "- Có đúng 1 mốc: nhãn 'Tạo mới', kèm thời điểm và dòng 'Người thực hiện: <tên> — <phòng ban>'"),

    ("002", "Lịch sử ghi lại thao tác sửa", "P0",
     "Phiếu nháp vừa được sửa: Người nộp từ 'Nguyễn Văn A' thành 'Trần Thị B', thêm ghi chú.",
     "1. Mở cửa sổ Lịch sử của phiếu",
     "—",
     "- Có mốc mới nhãn 'Thay đổi thông tin'\n"
     "- Ghi rõ 'Người nộp tiền: Nguyễn Văn A → Trần Thị B'\n"
     "- Ghi 'Diễn giải: <nội dung ghi chú mới>'\n"
     "- Mốc mới nằm TRÊN mốc 'Tạo mới'"),

    ("003", "Lịch sử ghi lại đổi trạng thái", "P0",
     "Phiếu vừa được gửi duyệt (từ 'Đang tạo' sang 'Chờ duyệt').",
     "1. Mở cửa sổ Lịch sử",
     "—",
     "- Có mốc riêng thuộc nhóm thay đổi trạng thái\n"
     "- Ghi bằng ĐÚNG TÊN trạng thái ('Đang tạo' → 'Chờ duyệt'), không phải con số"),

    ("004", "Lịch sử khi duyệt phiếu", "P0",
     "⚠️ Phiếu do chính mình tạo, vừa được duyệt.",
     "1. Mở cửa sổ Lịch sử",
     "—",
     "- Có 2 mốc riêng: một mốc 'Thay đổi thông tin' ghi số tiền thực thu từng dòng và ngày hạch "
     "toán; một mốc thay đổi trạng thái ('Chờ duyệt' → 'Đã duyệt') kèm ghi chú về việc đã ghi "
     "bút toán"),

    ("005", "Lịch sử khi hủy phiếu kèm lý do", "P1",
     "⚠️ Phiếu do chính mình tạo, vừa bị hủy với lý do 'Khách hàng chưa chuyển tiền'.",
     "1. Mở cửa sổ Lịch sử",
     "—",
     "- Có mốc thay đổi trạng thái ('Chờ duyệt' → 'Hủy') kèm đúng lý do hủy đã nhập\n"
     "- Không phải sang màn khác mới biết vì sao phiếu bị hủy"),

    ("006", "Khối Lịch sử ở màn chi tiết", "P0",
     "Phiếu đã có 2 mốc lịch sử.",
     "1. Mở màn chi tiết phiếu\n"
     "2. Cuộn xuống dưới khối 'Ghi chú'\n"
     "3. Bấm 'Xem lịch sử'",
     "—",
     "- Có khối 'Lịch sử' kèm con số đếm số mốc (ví dụ 2)\n"
     "- Mặc định thu gọn; bấm 'Xem lịch sử' thì bung ra, nút đổi thành 'Thu gọn'\n"
     "- Nội dung giống hệt cửa sổ Lịch sử mở từ danh sách\n"
     "- Có nút 'Làm mới' và nút 'Bộ lọc'"),

    ("007", "Phiếu chưa có lịch sử", "P1",
     "Phiếu cũ được chuyển từ hệ thống trước, chưa từng sửa trên hệ thống mới.",
     "1. Mở cửa sổ Lịch sử của phiếu đó",
     "—",
     "- Hiện dòng 'Chưa có lịch sử thao tác nào.'\n"
     "- Không báo lỗi"),

    ("008", "Ai cũng xem được lịch sử của phiếu mình thấy", "P1",
     "Tài khoản A không có quyền đặc biệt nào, đang thấy phiếu do mình lập.",
     "1. Mở menu ba chấm rồi bấm 'Lịch sử'",
     "—",
     "- Cửa sổ mở bình thường, không bị chặn quyền"),
]

S12 = [
    ("001", "Lưu khi chưa chọn phiếu đề nghị", "P0",
     "Màn Tạo mới, đã nhập Người nộp nhưng chưa chọn phiếu đề nghị.",
     "1. Bấm 'Lưu'",
     "—",
     "- Không lưu được\n"
     "- Hiện lỗi đỏ dưới ô 'Số phiếu đề nghị': 'Bắt buộc nhập'"),

    ("002", "Lưu khi chưa nhập Người nộp", "P0",
     "Đã chọn phiếu đề nghị, bảng Chi tiết đã nạp, nhưng ô Người nộp còn trống.",
     "1. Bấm 'Lưu và gửi duyệt' rồi 'Xác nhận'\n"
     "2. Quan sát ô Người nộp",
     "—",
     "- Không lưu được\n"
     "- Ô 'Người nộp' viền đỏ, dưới ô hiện chữ đỏ 'Bắt buộc nhập'\n"
     "- ⚠️ Màn hình không đóng, mọi dữ liệu đã nhập vẫn còn (kể cả bảng Chi tiết)"),

    ("003", "Người nộp quá 255 ký tự", "P1",
     "Màn Tạo mới, đã chọn phiếu đề nghị.",
     "1. Dán 300 ký tự vào ô 'Người nộp'\n"
     "2. Bấm 'Lưu'",
     "Chuỗi 300 ký tự",
     "- Hệ thống báo lỗi vượt độ dài cho phép ở ô Người nộp\n"
     "- Phiếu không được lưu"),

    ("004", "Bỏ trống Tài khoản nợ", "P0",
     "Màn Tạo mới, đã chọn phiếu đề nghị và nhập Người nộp.",
     "1. Xóa giá trị ô 'Tài khoản nợ'\n"
     "2. Bấm 'Lưu'",
     "Tài khoản nợ: (trống)",
     "- Lỗi đỏ dưới ô 'Tài khoản nợ': 'Bắt buộc nhập'\n"
     "- Không lưu được"),

    ("005", "Bỏ trống Số tài khoản có của một dòng", "P0",
     "Bảng Chi tiết có 3 dòng.",
     "1. Xóa giá trị ô 'Số tài khoản có' của dòng 2\n"
     "2. Bấm 'Lưu'",
     "Dòng 2: (trống)",
     "- Lỗi đỏ ngay dưới ô của dòng 2: 'Bắt buộc nhập'\n"
     "- Các dòng khác không bị báo lỗi\n"
     "- Không lưu được"),

    ("006", "Bỏ trống Số tiền duyệt thu của một dòng", "P0",
     "Bảng Chi tiết có 3 dòng.",
     "1. Xóa giá trị ô 'Số tiền duyệt thu' của dòng 1\n"
     "2. Bấm 'Lưu'",
     "Dòng 1: (trống)",
     "- Lỗi đỏ ngay dưới ô: 'Bắt buộc nhập'\n"
     "- Không lưu được"),

    ("007", "Số tiền duyệt thu bằng 0", "P1",
     "Bảng Chi tiết có 3 dòng.",
     "1. Nhập 'Số tiền duyệt thu' dòng 1 = 0\n"
     "2. Bấm 'Lưu'",
     "Dòng 1: 0",
     "- ⚠️ Lưu ĐƯỢC — số 0 là giá trị hợp lệ (chỉ không được âm)\n"
     "- Dòng 'Tổng cộng' cộng đúng, dòng đó góp 0 đồng"),

    ("008", "Số tiền duyệt thu âm", "P0",
     "Bảng Chi tiết có 3 dòng.",
     "1. Thử nhập số âm vào ô 'Số tiền duyệt thu'\n"
     "2. Bấm 'Lưu'",
     "Dòng 1: -1000",
     "- Ô không nhận dấu trừ; nếu lọt thì hệ thống báo lỗi và không lưu"),

    ("009", "Tỷ giá âm hoặc bằng 0", "P0",
     "Phiếu ngoại tệ, ô Tỷ giá đang mở.",
     "1. Nhập Tỷ giá = 0 rồi bấm 'Lưu'\n"
     "2. Nhập Tỷ giá = -1 rồi bấm 'Lưu'",
     "Tỷ giá: 0 / -1",
     "- Cả hai lần đều bị chặn, hiện lỗi dưới ô Tỷ giá\n"
     "- Phiếu không được lưu"),

    ("010", "Tỷ giá là chữ", "P1",
     "Phiếu ngoại tệ, ô Tỷ giá đang mở.",
     "1. Gõ 'abc' vào ô Tỷ giá",
     "Tỷ giá: abc",
     "- Ô không nhận chữ; nếu lọt thì hệ thống báo 'Phải là số'"),

    ("011", "Ghi chú quá 1000 ký tự", "P1",
     "Màn Tạo mới, đã điền đủ các mục bắt buộc.",
     "1. Dán 1.200 ký tự vào ô 'Ghi chú'\n"
     "2. Bấm 'Lưu'",
     "Chuỗi 1.200 ký tự",
     "- Hệ thống báo lỗi vượt độ dài cho phép\n"
     "- Nhập đúng 1.000 ký tự thì lưu được bình thường"),

    ("012", "Bỏ trống Ghi chú", "P1",
     "Đã điền đủ các mục bắt buộc, riêng ô 'Ghi chú' để trống.",
     "1. Bấm 'Lưu'",
     "Ghi chú: (trống)",
     "- ⚠️ Lưu THÀNH CÔNG — Ghi chú KHÔNG bắt buộc"),

    ("013", "Ký tự đặc biệt trong Người nộp và Ghi chú", "P2",
     "Màn Tạo mới.",
     "1. Nhập Người nộp và Ghi chú có dấu tiếng Việt và ký tự < > &\n"
     "2. Lưu rồi mở lại phiếu, rồi in phiếu",
     "Người nộp: 'Nguyễn Văn A <KD1> & cộng sự'",
     "- Nội dung hiển thị nguyên vẹn ở màn chi tiết\n"
     "- Bản in không hiện thẻ định dạng lạ, không vỡ bảng"),

    ("014", "Sửa lỗi xong thì lỗi tự biến mất", "P1",
     "Đang có lỗi đỏ 'Bắt buộc nhập' dưới ô Người nộp.",
     "1. Gõ nội dung vào ô Người nộp",
     "Người nộp: Nguyễn Văn A",
     "- Lỗi đỏ biến mất ngay khi gõ, không cần bấm Lưu lại"),
]

S13 = [
    ("001", "Phiếu bị xóa trong lúc người khác đang mở màn chi tiết", "P1",
     "Cùng tài khoản mở phiếu nháp P1 ở tab 1; ở tab 2 xóa chính phiếu này.",
     "1. Ở tab 1, bấm nút 'Sửa'",
     "—",
     "- Hệ thống báo không tìm thấy dữ liệu\n"
     "- Không treo trang, không hiện màn Sửa trắng"),

    ("002", "Phiếu bị duyệt trong lúc người lập đang mở màn Sửa", "P0",
     "Phiếu P đang 'Chờ duyệt'; người lập mở màn chi tiết từ trước, thủ quỹ vừa duyệt xong.",
     "1. Người lập tải lại màn chi tiết",
     "—",
     "- Trạng thái đổi thành 'Đã duyệt'\n"
     "- Nút Sửa và Xóa biến mất\n"
     "- Cột 'Số tiền thực thu' hiện số thủ quỹ vừa nhập, không nhập được nữa"),

    ("003", "Xóa phiếu ở tab khác rồi bấm Xóa lại ở tab cũ", "P1",
     "Cùng phiếu nháp mở trên 2 tab danh sách.",
     "1. Tab 1 xóa phiếu thành công\n"
     "2. Tab 2 (chưa tải lại) bấm Xóa dòng đó rồi xác nhận",
     "—",
     "- Tab 2 báo lỗi dữ liệu không còn\n"
     "- Danh sách tab 2 nạp lại, dòng biến mất"),

    ("004", "Tải lại trang giữa lúc đang nhập form", "P1",
     "Màn Tạo mới đã chọn phiếu đề nghị và nhập Người nộp.",
     "1. Nhấn phím tải lại trang\n"
     "2. Đọc cảnh báo của trình duyệt rồi chọn rời trang",
     "—",
     "- Trình duyệt cảnh báo dữ liệu chưa lưu\n"
     "- Chọn rời trang thì form về trắng, không có phiếu nào được tạo"),

    ("005", "Mất kết nối khi đang lưu phiếu", "P2",
     "Form đã điền đủ, ngắt mạng ngay trước khi bấm Lưu.",
     "1. Bấm 'Lưu'\n"
     "2. Nối mạng lại và mở danh sách",
     "—",
     "- Hệ thống báo lỗi lưu, vẫn ở form và giữ nguyên dữ liệu đã nhập\n"
     "- Không có phiếu rỗng hay phiếu thiếu dòng chi tiết được tạo ra"),

    ("006", "Mất kết nối giữa lúc duyệt phiếu", "P0",
     "⚠️ Phiếu do chính mình tạo, đang 'Chờ duyệt'. Ngắt mạng ngay sau khi bấm Duyệt.",
     "1. Bấm 'Duyệt phiếu thu' rồi ngắt mạng\n"
     "2. Nối lại mạng, mở lại phiếu và đối chiếu sổ kế toán",
     "—",
     "- Phiếu hoặc duyệt trọn vẹn (đổi trạng thái + ghi đủ bút toán), hoặc không đổi gì cả\n"
     "- ⚠️ TUYỆT ĐỐI không được có trường hợp phiếu đã 'Đã duyệt' mà sổ kế toán thiếu bút toán, "
     "hoặc ngược lại"),
]

S14 = [
    ("001", "Luồng trọn vẹn: lập nháp → sửa → gửi duyệt → duyệt", "P0",
     "⚠️ DÙNG PHIẾU ĐỀ NGHỊ TEST DO CHÍNH MÌNH LẬP. Tài khoản E có quyền 'Kế toán thanh toán'; "
     "tài khoản F có quyền 'Thủ quỹ duyệt phiếu thu' cùng công ty.",
     "1. E lập phiếu thu từ một phiếu đề nghị đang Chờ KT duyệt, bấm 'Lưu'\n"
     "2. E mở lại phiếu, bấm 'Sửa', đổi số duyệt thu, bấm 'Lưu và gửi duyệt'\n"
     "3. F mở phiếu, nhập số thực thu từng dòng, bấm 'Duyệt phiếu thu'\n"
     "4. Mở màn Phiếu đề nghị thu tiền kiểm tra phiếu đề nghị\n"
     "5. Mở lịch sử phiếu thu",
     "—",
     "- Bước 1: trạng thái 'Đang tạo', chỉ E nhìn thấy; phiếu đề nghị vẫn 'Chờ KT duyệt'\n"
     "- Bước 2: trạng thái 'Chờ duyệt'; phiếu đề nghị chuyển 'Đã tạo phiếu thu'; F nhận thông báo\n"
     "- Bước 3: trạng thái 'Đã duyệt', ghi người duyệt và ngày hạch toán\n"
     "- Bước 4: phiếu đề nghị chuyển 'Đã hạch toán' và mang số tiền thực thu\n"
     "- Bước 5: lịch sử có đủ các mốc theo đúng thứ tự thời gian"),

    ("002", "Luồng trọn vẹn: lập nháp rồi xóa bỏ", "P0",
     "Tài khoản E có quyền 'Kế toán thanh toán'.",
     "1. E lập phiếu thu từ phiếu đề nghị X, bấm 'Lưu'\n"
     "2. E mở lại phiếu kiểm tra nội dung\n"
     "3. E xóa phiếu\n"
     "4. Mở lại cửa sổ chọn phiếu đề nghị, tìm X",
     "—",
     "- Tổng số phiếu trở về đúng như trước khi lập\n"
     "- X xuất hiện lại trong cửa sổ chọn, lập được phiếu thu mới\n"
     "- Phiếu đề nghị X vẫn ở 'Chờ KT duyệt' suốt cả quá trình"),

    ("003", "Luồng trọn vẹn: gửi duyệt rồi bị hủy", "P0",
     "⚠️ DÙNG PHIẾU ĐỀ NGHỊ TEST. Tài khoản E lập phiếu, tài khoản F là thủ quỹ.",
     "1. E lập và gửi duyệt phiếu thu từ phiếu đề nghị X\n"
     "2. F mở phiếu, bấm 'Hủy phiếu thu', nhập lý do, xác nhận\n"
     "3. Mở phiếu đề nghị X\n"
     "4. Thử lập phiếu thu mới cho X",
     "—",
     "- Phiếu thu chuyển 'Hủy', ghi chú mang lý do hủy\n"
     "- Phiếu đề nghị X chuyển 'Hủy'\n"
     "- ⚠️ KHÔNG lập lại được phiếu thu cho X — đây là ngõ cụt đã chốt\n"
     "- Sổ kế toán không phát sinh bút toán nào"),

    ("004", "Luồng trọn vẹn: người kế toán không có quyền thủ quỹ", "P0",
     "Tài khoản E chỉ có 'Kế toán thanh toán'.",
     "1. E lập và gửi duyệt một phiếu thu\n"
     "2. E mở lại phiếu vừa gửi\n"
     "3. E quan sát các nút và bảng Chi tiết",
     "—",
     "- E xem được phiếu (là người lập)\n"
     "- Không có nút 'Duyệt phiếu thu' và 'Hủy phiếu thu'\n"
     "- Cột 'Số tiền thực thu' chỉ hiển thị, không nhập được\n"
     "- E vẫn In và Xuất Excel được"),

    ("005", "Luồng trọn vẹn: theo dõi một phiếu qua đủ 4 trạng thái", "P1",
     "⚠️ DÙNG PHIẾU ĐỀ NGHỊ TEST.",
     "1. Lập phiếu, lưu nháp — ghi lại trạng thái và các nút\n"
     "2. Gửi duyệt — ghi lại\n"
     "3. Thủ quỹ duyệt — ghi lại\n"
     "4. Trên một phiếu khác, thủ quỹ hủy — ghi lại",
     "—",
     "- Đang tạo: có Sửa, Xóa; nháp chỉ mình thấy\n"
     "- Chờ duyệt: mất Sửa/Xóa, thủ quỹ có Duyệt/Hủy\n"
     "- Đã duyệt: chỉ còn In, Xuất Excel, Quay lại; đã ghi sổ kế toán\n"
     "- Hủy: chỉ còn In, Xuất Excel, Quay lại; ghi chú mang lý do hủy\n"
     "- Nhãn màu: 3 trạng thái đầu và Hủy là đỏ, riêng Đã duyệt là xanh"),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", S1),
    ("II", "BỘ LỌC & TÌM KIẾM", S2),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", S3),
    ("IV", "TẠO MỚI PHIẾU THU", S4),
    ("V", "SỬA PHIẾU THU", S5),
    ("VI", "XEM CHI TIẾT PHIẾU THU", S6),
    ("VII", "DUYỆT PHIẾU THU", S7),
    ("VIII", "HỦY PHIẾU THU", S8),
    ("IX", "XÓA PHIẾU THU", S9),
    ("X", "IN PHIẾU & XUẤT EXCEL", S10),
    ("XI", "LỊCH SỬ THAY ĐỔI", S11),
    ("XII", "RÀNG BUỘC NHẬP LIỆU", S12),
    ("XIII", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", S13),
    ("XIV", "LUỒNG NGHIỆP VỤ TRỌN VẸN", S14),
]

if __name__ == "__main__":
    build(output_file=OUT,
          sheet_name="Trang tính1",
          feature_name="Phiếu thu tiền - Cập nhật ngày 03/09/2026",
          module_name=MODULE,
          description_block=DESCRIPTION_BLOCK,
          role_tcs=ROLE_TCS,
          sections=SECTIONS)
