# -*- coding: utf-8 -*-
"""Testcase man "Danh sach dang ky khach hang toan cong ty" (HRM, CSKH truoc ban > Bao cao thi truong).

User yeu cau 19/10/2026: du lieu TAO TU ERP (nut "Dang ky khach hang" tren bao gia hang), nguoi test xem hien thi o
man danh sach HRM va doi chieu 2 ben. Nguon:
  - HRM: hrm-client/pages/assign/report/customer-registers/index.vue, hrm-api/Modules/Assign/Services/Report/
    CustomerRegisterService.php, Transformers/CustomerRegisterResource
  - ERP: FirmQuotationController@registerCustomerInfo/registerCustomer, Employee::canRegisterCustomer/registedCustomer,
    FirmQuotationDatatable (dieu kien hien nut), CustomerRegistersController (index/forEmployee/cancel),
    CustomerRegister::searchByFilter, views sale/customer_registers/index + firm/quotations/partials/customerRegister
Chay: python gen_testcase.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills", "testcase-documenter", "assets"))
from tc_engine import build  # noqa: E402

NGAY = "19/10/2026"
TEN = "Danh sách đăng ký khách hàng toàn công ty"
MODULE = "ĐK khách hàng toàn công ty"

HRM_MENU = ("HRM: vào phân hệ CSKH trước bán > nhóm Báo cáo > mục Báo cáo thị trường > "
            "\"Danh sách đăng ký khách hàng toàn công ty\"")
ERP_MENU = ("ERP: menu Kinh doanh > Báo cáo thị trường > \"Danh sách đăng ký khách hàng toàn công ty\"")
ERP_CA_NHAN = "ERP: menu Kinh doanh > Báo cáo thị trường > \"Danh sách khách hàng đã đăng ký\""
ERP_BG = ("ERP: menu Kinh doanh > Báo giá > \"Báo giá vật tư- hàng hóa - thiết bị\" (hoặc \"Báo giá dự án\", "
          "\"Báo giá hợp đồng nguyên tắc\")")
ERP_DK = ("Ở dòng báo giá, bấm nút bánh răng (cột cuối) > chọn \"Đăng ký khách hàng\"")

DU_LIEU = (
    "Dữ liệu mẫu dùng xuyên suốt (lập trên ERP trước khi test, ghi lại mã thật vào cột Ghi chú):\n"
    "- Nhân viên A (phòng mã KD1) và nhân viên B (phòng mã KD2): đều có quyền \"Thêm báo giá\" trên ERP.\n"
    "- Khách KH-DN: loại Doanh nghiệp tư nhân, có 2 người liên hệ LH1 và LH2.\n"
    "- Khách KH-CN: loại Cá nhân.\n"
    "- BG-01: báo giá hãng do A lập, khách KH-DN / LH1, trạng thái Đã duyệt, CÓ file đính kèm.\n"
    "- BG-02: do B lập, KH-DN / LH1, Đã duyệt, có file đính kèm.\n"
    "- BG-03: do B lập, KH-DN / LH2, Đã duyệt, có file đính kèm.\n"
    "- BG-04: do A lập, trạng thái Đang tạo.\n"
    "- BG-05: do A lập, Đã duyệt, KHÔNG có file đính kèm.\n"
    "- BG-06: do A lập, khách KH-CN, trạng thái Đã lập hợp đồng, có file đính kèm.\n"
    "- BG-07: do B lập, khách KH-CN, Đã duyệt, có file đính kèm.\n"
    "- Tài khoản Q: có quyền \"Xem danh sách khách hàng đã đăng ký\" ở CẢ ERP và HRM. Tài khoản Z: không có quyền này ở cả 2 bên.\n"
    "- Cấu hình ERP \"Thời gian đăng ký khách hàng\" (menu Cấu hình ERP > Cấu hình hệ thống): ghi lại số ngày đang đặt, "
    "gọi là N (ví dụ 30)."
)

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Màn HRM \"Danh sách đăng ký khách hàng toàn công ty\" hiển thị mọi lượt nhân viên kinh doanh ĐĂNG KÝ giữ khách "
     "hàng (để người khác không chen vào cùng khách trong một thời hạn). Màn CHỈ ĐỂ XEM: không thêm, sửa, xóa.\n"
     "Đăng ký được tạo bên ERP: trên danh sách báo giá hãng, người lập báo giá bấm \"Đăng ký khách hàng\", nhập Ghi "
     "chú, bấm Lưu. Hủy đăng ký cũng làm bên ERP (màn \"Danh sách khách hàng đã đăng ký\" của từng người).\n"
     "Bộ testcase này: tạo / hủy đăng ký trên ERP, rồi mở màn danh sách ở CẢ ERP và HRM để đối chiếu từng dòng, từng "
     "cột. ERP và HRM ở môi trường test dùng chung dữ liệu nên đăng ký vừa tạo phải hiện ngay ở cả 2 bên.\n"
     "Đường vào: " + HRM_MENU + ". Bên ERP: " + ERP_MENU + "."),

    ("2. Đối tượng được tính / hiển thị",
     "Mọi lượt đăng ký khách hàng của TOÀN công ty, gồm cả Còn hạn và Hết hạn, của mọi nhân viên, mọi phòng ban.\n"
     "Mỗi dòng: Khách hàng đăng ký (dòng dưới in nghiêng, chữ nhỏ là người liên hệ nếu có) · Ngày đăng ký (ngày giờ) · "
     "Thời hạn đăng ký (ngày) · Người đăng ký (\"Mã phòng - Họ tên\") · Số báo giá (bấm được, mở báo giá) · Ghi chú.\n"
     "Đăng ký sinh từ báo giá hãng ở 3 loại: Vật tư - Hàng hoá - Thiết bị, Dự án, Hợp đồng nguyên tắc. Dữ liệu cũ có "
     "thể có đăng ký sinh từ báo giá thường (màn cũ) — vẫn hiện, Số báo giá mở màn báo giá của HRM.\n"
     "Điều kiện để ERP CHO đăng ký (nút \"Đăng ký khách hàng\" hiện và lưu được):\n"
     "- Người bấm là người LẬP báo giá.\n"
     "- Báo giá ở trạng thái Đã duyệt hoặc Đã lập hợp đồng.\n"
     "- Báo giá đã có file đính kèm.\n"
     "- Chưa có NGƯỜI KHÁC đang giữ đăng ký còn hạn với cùng khách hàng (khách Cá nhân) hoặc cùng khách hàng + cùng "
     "người liên hệ (khách là tổ chức: doanh nghiệp, cơ quan…).\n"
     "- Chính mình chưa có đăng ký còn hạn với cùng khách / người liên hệ đó.\n"
     "- Ghi chú bắt buộc nhập."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Báo giá Đang tạo / Không hiệu lực, hoặc báo giá do người khác lập: KHÔNG có mục \"Đăng ký khách hàng\" nên "
     "không sinh dòng nào.\n"
     "- Lượt đăng ký bị chặn (thiếu file, trùng người khác, đã tự đăng ký, thiếu Ghi chú): không sinh dòng.\n"
     "- Đăng ký đã HỦY bên ERP: bị xóa hẳn, biến mất khỏi danh sách ở cả 2 hệ thống (không chuyển thành Hết hạn).\n"
     "- Màn HRM không có khối thống kê, không có nút Hủy đăng ký (chức năng hủy vẫn ở ERP)."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Không có bộ lọc khoảng ngày. Ô \"Thời hạn đăng ký\" (Còn hạn / Hết hạn) so Thời hạn đăng ký với HÔM NAY:\n"
     "- HRM so theo NGÀY: Thời hạn bằng hôm nay vẫn là Còn hạn đến hết ngày.\n"
     "- ERP so theo cả GIỜ: Thời hạn = ngày đăng ký + N ngày, giữ nguyên giờ phút lúc đăng ký; đến đúng giờ đó của ngày "
     "hết hạn thì ERP đã tính Hết hạn, trong khi HRM vẫn Còn hạn tới cuối ngày. Đây là khác biệt ĐÃ CHỐT, không ghi lỗi.\n"
     "Thời hạn đăng ký = Ngày đăng ký + N ngày (N lấy từ cấu hình ERP tại thời điểm đăng ký; đổi cấu hình sau đó không "
     "làm đổi thời hạn của đăng ký cũ).\n"
     "Hệ thống ghi nhớ bộ lọc trong 10 phút khi rời màn rồi quay lại."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Danh sách phẳng, mỗi dòng một lượt đăng ký. Một khách hàng có thể có nhiều dòng: nhiều người đăng ký nối tiếp nhau "
     "qua các thời kỳ, hoặc nhiều người liên hệ khác nhau của cùng một khách tổ chức.\n"
     "HRM có 7 cột: STT | Khách hàng đăng ký | Ngày đăng ký | Thời hạn đăng ký | Người đăng ký | Số báo giá | Ghi chú. "
     "ERP có 6 cột (không có STT). Cột STT và Khách hàng đăng ký của HRM đứng yên khi cuộn ngang."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "Không cộng dồn, không gộp: hai lượt đăng ký cùng khách hàng là 2 dòng.\n"
     "Chống trùng nằm ở bước tạo bên ERP (xem mục 2): cùng lúc chỉ MỘT người giữ đăng ký còn hạn cho cùng khách cá "
     "nhân / cùng cặp khách tổ chức + người liên hệ. Khi đăng ký của người trước hết hạn hoặc bị hủy, người khác mới "
     "đăng ký được."),

    ("7. Phân quyền cấp",
     "- Quyền \"Xem danh sách khách hàng đã đăng ký\" (nhóm Quản lý khách hàng). Có quyền là xem TOÀN công ty, không "
     "chia theo công ty / phòng ban / bộ phận.\n"
     "- HRM: không có quyền thì mục menu bị ẩn và mở màn cũng bị từ chối.\n"
     "- ERP: mục menu luôn hiện với mọi người, nhưng không có quyền thì mở ra trang không tìm thấy.\n"
     "- Quyền được cấp RIÊNG ở từng hệ thống (tên giống nhau). Khi đối chiếu phải chắc tài khoản có quyền ở cả 2 bên.\n"
     "- Tạo đăng ký trên ERP cần quyền \"Thêm báo giá\" và phải là người lập báo giá."),

    ("8. Cách tính các ô thống kê",
     "Không có ô thống kê. Chân bảng HRM: \"Hiển thị a - b / N đăng ký\" — a, b là STT dòng đầu / cuối trang, N là tổng "
     "số đăng ký khớp bộ lọc. N phải BẰNG tổng số mục ở chân bảng ERP với cùng điều kiện lọc.\n"
     "Ngày đăng ký hiển thị dạng ngày/tháng/năm giờ:phút; Thời hạn đăng ký dạng ngày/tháng/năm.\n"
     "Người đăng ký = \"Mã phòng - Họ tên\" theo hồ sơ HIỆN TẠI của nhân viên (đổi phòng thì hiện phòng mới ở cả 2 bên)."),

    ("9. Ghi chú đọc bảng",
     DU_LIEU + "\n"
     "Các khác biệt ERP - HRM ĐÃ CHỐT (không ghi Failed):\n"
     "- Ngày hết hạn: HRM còn hạn cả ngày, ERP hết hạn từ đúng giờ đăng ký (mục 4).\n"
     "- HRM có thêm: ô tìm nhanh, sắp xếp theo Ngày đăng ký / Thời hạn đăng ký, Cấu hình cột, Xuất Excel chọn trường. "
     "ERP không có các chức năng này.\n"
     "- Số báo giá: HRM luôn là link, khi mở ERP tự kiểm quyền xem báo giá; ERP chỉ hiện link khi người xem có quyền "
     "xem báo giá đó.\n"
     "- Nhân viên chưa có phòng ban: HRM vẫn hiện Họ tên; ERP để trống cả ô Người đăng ký.\n"
     "Ô lọc gõ chữ (Khách hàng đăng ký, Số báo giá, ô tìm nhanh) chỉ lọc khi bấm Tìm kiếm hoặc nhấn Enter; ô chọn "
     "(Thời hạn đăng ký, Người đăng ký) tự lọc ngay khi chọn.\n"
     "Testcase có ghi \"dùng công cụ kiểm thử API\" dành cho tester kỹ thuật."),
]

ROLE_TCS = [
    ("00", "HRM: không có quyền xem - menu ẩn, màn bị chặn", "P0",
     "Tài khoản Z: KHÔNG có quyền \"Xem danh sách khách hàng đã đăng ký\" trên HRM\n"
     "Đã lưu dấu trang (bookmark) màn này từ tài khoản Q",
     "1. Đăng nhập HRM bằng Z\n2. Vào phân hệ CSKH trước bán > Báo cáo > Báo cáo thị trường\n"
     "3. Mở dấu trang đã lưu",
     "Tài khoản Z",
     "- Mục \"Danh sách đăng ký khách hàng toàn công ty\" KHÔNG có trong menu\n"
     "- Mở dấu trang: hệ thống từ chối, bảng không có dòng dữ liệu nào, không hiện thông báo \"Lỗi khi tải dữ liệu\""),
    ("01", "HRM: có quyền xem - thấy menu và toàn bộ dữ liệu", "P0",
     "Tài khoản Q có quyền \"Xem danh sách khách hàng đã đăng ký\" trên HRM",
     "1. Đăng nhập HRM bằng Q\n2. Bấm theo đường menu ở mục 1",
     "Tài khoản Q",
     "- Mục menu hiện, mở được màn\n- Bảng có dữ liệu, chân bảng ghi tổng số đăng ký"),
    ("02", "ERP: không có quyền - menu vẫn hiện nhưng mở ra trang không tìm thấy", "P1",
     "Tài khoản Z không có quyền trên ERP",
     "1. Đăng nhập ERP bằng Z\n2. Bấm " + ERP_MENU,
     "Tài khoản Z",
     "- Mục menu VẪN hiện (ERP không ẩn menu theo quyền)\n- Bấm vào: ERP hiện trang không tìm thấy, không có bảng\n"
     "- Đây là hành vi của ERP; bên HRM thì menu bị ẩn (TC-ROLE-00) - không ghi lỗi"),
    ("03", "Có quyền ở ERP nhưng chưa có ở HRM", "P1",
     "Tài khoản Y: có quyền trên ERP, CHƯA được cấp trên HRM",
     "1. Đăng nhập ERP bằng Y, mở danh sách\n2. Đăng nhập HRM bằng Y, tìm mục menu",
     "Tài khoản Y",
     "- ERP: xem được danh sách\n- HRM: mục menu bị ẩn\n"
     "- Lưu ý: quyền phải cấp riêng ở từng hệ thống; muốn đối chiếu thì cấp cho Y trên HRM rồi đăng nhập lại"),
    ("04", "Có quyền là xem toàn công ty, không chia phạm vi", "P0",
     "Tài khoản Q thuộc công ty 1, phòng KD1\n"
     "Đã có đăng ký của nhân viên công ty khác và phòng khác (ví dụ của B phòng KD2)",
     "1. Đăng nhập HRM bằng Q, không lọc gì\n2. Đăng nhập ERP bằng Q, không lọc gì\n3. So tổng số dòng ở chân bảng 2 bên",
     "Tài khoản Q",
     "- Thấy đăng ký của mọi phòng, mọi công ty, gồm cả dòng của B\n- Tổng số dòng HRM BẰNG tổng số mục của ERP"),
    ("05", "Không có quyền - gọi thẳng chức năng xem danh sách và Xuất Excel", "P1",
     "Tài khoản Z đã đăng nhập HRM hợp lệ (không có quyền xem)",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng lấy danh sách\n2. Gọi thẳng chức năng Xuất Excel",
     "Tài khoản Z",
     "- Cả 2 lần đều bị hệ thống từ chối, báo không có quyền\n- Không trả về dòng dữ liệu nào, không tải được file"),
]

S1 = [
    ("001", "Mở màn từ menu HRM", "P0",
     "Tài khoản Q có quyền xem trên HRM",
     "1. Đăng nhập HRM\n2. Vào phân hệ CSKH trước bán\n3. Nhóm Báo cáo > Báo cáo thị trường > bấm \"Danh sách đăng ký khách hàng toàn công ty\"",
     "Tài khoản Q",
     "- Mở đúng màn, tiêu đề bảng \"Danh sách đăng ký khách hàng toàn công ty\"\n- Bảng tự tải dữ liệu, không cần bấm Tìm kiếm"),
    ("002", "Mở màn tương ứng bên ERP để đối chiếu", "P0",
     "Tài khoản Q có quyền xem trên ERP",
     "1. Đăng nhập ERP\n2. Bấm " + ERP_MENU,
     "Tài khoản Q",
     "- Mở màn ERP cùng tên, có 6 cột: Khách hàng đăng ký, Ngày đăng ký, Thời hạn đăng ký, Người đăng ký, Số báo giá, Ghi chú"),
    ("003", "Bố cục màn HRM khi vào lần đầu", "P1",
     "Chưa từng đặt bộ lọc ở màn này (hoặc đã quá 10 phút)",
     "1. Mở màn HRM\n2. Quan sát phần trên bảng và hàng nút",
     "-",
     "- Có ô tìm nhanh với chữ gợi ý \"Tìm theo khách hàng, người liên hệ, người đăng ký, số báo giá\", nút Tìm kiếm, Làm mới\n"
     "- Bộ lọc nâng cao đang thu gọn\n- Có nút \"Xuất Excel\" và nút Cấu hình cột hiển thị\n"
     "- KHÔNG có nút Thêm, Sửa, Xóa, Hủy đăng ký"),
    ("004", "Đủ và đúng thứ tự cột HRM", "P0",
     "Danh sách có dữ liệu",
     "1. Đọc tiêu đề cột từ trái sang phải",
     "-",
     "- 7 cột: STT | Khách hàng đăng ký | Ngày đăng ký | Thời hạn đăng ký | Người đăng ký | Số báo giá | Ghi chú\n"
     "- 6 cột sau STT trùng tên và thứ tự với ERP\n- Cuộn ngang: STT và Khách hàng đăng ký đứng yên"),
    ("005", "Tổng số dòng 2 bên bằng nhau khi không lọc", "P0",
     "Tài khoản Q có quyền ở cả 2 bên",
     "1. HRM: mở màn, không lọc, đọc chân bảng\n2. ERP: mở màn, không lọc, đọc chân bảng",
     "-",
     "- Tổng số đăng ký ở chân bảng HRM bằng tổng số mục ở chân bảng ERP"),
    ("006", "Thứ tự mặc định: đăng ký mới nhất lên đầu, giống ERP", "P0",
     "Có ít nhất 3 đăng ký ở các thời điểm khác nhau",
     "1. Mở màn HRM, không bấm sắp xếp\n2. Mở màn ERP\n3. So 10 dòng đầu 2 bên",
     "-",
     "- Cả 2 bên xếp Ngày đăng ký giảm dần\n- 10 dòng đầu trùng nhau về khách hàng, ngày đăng ký, người đăng ký, số báo giá"),
    ("007", "Không có dữ liệu phù hợp", "P1",
     "Danh sách có dữ liệu",
     "1. Nhập \"ZZZ999\" vào ô tìm nhanh\n2. Bấm Tìm kiếm",
     "Từ khóa: ZZZ999",
     "- Bảng hiện \"Không có dữ liệu phù hợp bộ lọc.\"\n- Không báo lỗi"),
    ("008", "Ghi nhớ bộ lọc trong 10 phút", "P2",
     "Đã chọn Thời hạn đăng ký = Còn hạn rồi chuyển sang màn khác",
     "1. Quay lại màn sau 2 phút\n2. Quay lại màn sau hơn 10 phút",
     "-",
     "- Lần 1: bộ lọc Còn hạn vẫn giữ, danh sách vẫn đang lọc\n- Lần 2: bộ lọc về trống, hiện toàn bộ"),
]

S2 = [
    ("001", "Cửa sổ Đăng ký khách hàng trên ERP hiện đúng thông tin", "P0",
     "Đăng nhập ERP bằng A. BG-01 như dữ liệu mẫu (mục 9)",
     "1. Vào " + ERP_BG + "\n2. Tìm BG-01\n3. " + ERP_DK,
     "BG-01",
     "- Cửa sổ \"Đăng ký khách hàng\" mở ra, các ô chỉ đọc: Số báo giá = mã BG-01, Khách hàng = KH-DN, "
     "Người liên hệ = LH1, Chức vụ của LH1, Người đăng ký = họ tên A, Thời gian đăng ký = \"N ngày\"\n"
     "- Ô Ghi chú có dấu (*) bắt buộc\n- Có nút Lưu và Đóng"),
    ("002", "Đăng ký thành công trên ERP - dòng mới hiện ở CẢ 2 bên, khớp từng cột", "P0",
     "Ghi lại tổng số dòng hiện tại của HRM và ERP (gọi là T)\nA chưa có đăng ký nào với KH-DN / LH1",
     "1. ERP, đăng nhập A: mở cửa sổ đăng ký của BG-01\n2. Nhập Ghi chú, bấm Lưu\n"
     "3. Q mở danh sách ERP, đọc dòng đầu\n4. Q mở danh sách HRM (hoặc bấm Làm mới), đọc dòng đầu",
     "Ghi chú: \"KH đang làm dự án kho lạnh - test 01\"",
     "- ERP báo \"Đăng ký khách hàng thành công!\", cửa sổ đóng\n- Tổng số dòng cả 2 bên = T + 1, dòng mới nằm ĐẦU danh sách\n"
     "- Khách hàng đăng ký: tên KH-DN, dòng dưới in nghiêng là LH1 (HRM và ERP giống nhau)\n"
     "- Ngày đăng ký: hôm nay, đúng giờ phút lúc bấm Lưu, 2 bên trùng nhau\n"
     "- Thời hạn đăng ký = hôm nay + N ngày, 2 bên trùng nhau\n- Người đăng ký: \"KD1 - <họ tên A>\"\n"
     "- Số báo giá: mã BG-01\n- Ghi chú: đúng nội dung đã nhập"),
    ("003", "Bỏ trống Ghi chú - ERP chặn, HRM không có dòng mới", "P0",
     "A chưa đăng ký KH-CN. Tổng số dòng HRM hiện tại = T",
     "1. ERP, A mở cửa sổ đăng ký của BG-06\n2. Để trống Ghi chú, bấm Lưu\n3. Mở danh sách HRM",
     "Ghi chú: để trống",
     "- ERP báo \"Thao tác thất bại\", chữ đỏ \"Bắt buộc phải nhập\" ngay dưới ô Ghi chú; cửa sổ không đóng\n"
     "- HRM: tổng số dòng vẫn = T"),
    ("004", "Ghi chú dài, có xuống dòng và ký tự đặc biệt hiển thị đúng ở HRM", "P1",
     "A chưa đăng ký KH-CN",
     "1. ERP, A đăng ký BG-06 với Ghi chú bên dưới\n2. Mở HRM, xem cột Ghi chú của dòng mới\n3. Rê chuột lên ô Ghi chú",
     "Ghi chú khoảng 200 ký tự, có 2 dòng, có ký tự & < > \" %",
     "- HRM hiện tối đa 2 dòng rồi cắt bằng dấu ba chấm; rê chuột thấy đủ nội dung\n"
     "- Ký tự đặc biệt hiện đúng như đã nhập, không bị biến thành mã lạ\n- Nội dung trùng với ERP"),
    ("005", "Báo giá ở trạng thái Đã lập hợp đồng vẫn đăng ký được; khách Cá nhân không có dòng người liên hệ", "P0",
     "BG-06: A lập, khách KH-CN (Cá nhân), Đã lập hợp đồng",
     "1. ERP, A đăng ký BG-06 (nếu TC_02.004 đã đăng ký thì xem lại dòng đó)\n2. Xem dòng đó ở HRM và ERP",
     "BG-06",
     "- Đăng ký thành công\n- Cột Khách hàng đăng ký chỉ có tên KH-CN, KHÔNG có dòng in nghiêng người liên hệ (cả 2 bên)\n"
     "- Số báo giá = mã BG-06"),
    ("006", "Báo giá Đang tạo - không có mục Đăng ký khách hàng", "P0",
     "BG-04: A lập, trạng thái Đang tạo",
     "1. ERP, A mở danh sách báo giá, bấm nút bánh răng ở dòng BG-04",
     "BG-04",
     "- KHÔNG có mục \"Đăng ký khách hàng\" trong danh sách thao tác\n- HRM: không có dòng nào mang số báo giá BG-04"),
    ("007", "Người không lập báo giá - không có mục Đăng ký khách hàng", "P0",
     "BG-01 do A lập",
     "1. ERP, đăng nhập B, bấm nút bánh răng ở dòng BG-01",
     "Tài khoản B, BG-01",
     "- KHÔNG có mục \"Đăng ký khách hàng\""),
    ("008", "Báo giá chưa có file đính kèm - ERP hỏi cập nhật file, không sinh đăng ký", "P0",
     "BG-05: A lập, Đã duyệt, không có file đính kèm. Tổng số dòng HRM = T",
     "1. ERP, A bấm \"Đăng ký khách hàng\" ở BG-05\n2. Bấm Hủy ở hộp thoại\n3. Làm lại, lần này bấm Xác nhận\n4. Mở HRM",
     "BG-05",
     "- Hộp thoại cảnh báo \"Báo giá chưa có file đính kèm!\", câu hỏi \"Bạn có muốn cập nhật file đính kèm không?\"\n"
     "- Bấm Hủy: đóng hộp thoại, ở lại danh sách\n- Bấm Xác nhận: chuyển sang trang xem chi tiết BG-05 để thêm file\n"
     "- KHÔNG mở cửa sổ đăng ký; HRM vẫn T dòng"),
    ("009", "Tự đăng ký lại khách mình đang giữ - ERP chặn", "P0",
     "A đã có đăng ký còn hạn KH-DN / LH1 (TC_02.002). Có thêm báo giá BG-08 do A lập, KH-DN / LH1, Đã duyệt, có file",
     "1. ERP, A đăng ký BG-08, nhập Ghi chú, bấm Lưu\n2. Mở HRM, lọc Khách hàng đăng ký = tên KH-DN",
     "BG-08",
     "- ERP báo \"Bạn đã đăng ký khách hàng này rồi!\"\n- HRM: KH-DN / LH1 vẫn chỉ có 1 dòng của A"),
    ("010", "Người khác đăng ký trùng khách + trùng người liên hệ đang còn hạn - ERP chặn", "P0",
     "A đang giữ KH-DN / LH1 còn hạn. BG-02 do B lập, KH-DN / LH1",
     "1. ERP, B đăng ký BG-02, nhập Ghi chú, bấm Lưu\n2. Mở HRM, lọc theo KH-DN",
     "BG-02",
     "- ERP báo \"Không có quyền đăng ký khách hàng này!\"\n- HRM: không có dòng mới của B cho KH-DN / LH1"),
    ("011", "Khách tổ chức, KHÁC người liên hệ - người khác vẫn đăng ký được", "P0",
     "A đang giữ KH-DN / LH1. BG-03 do B lập, KH-DN / LH2",
     "1. ERP, B đăng ký BG-03\n2. Mở HRM và ERP, lọc theo KH-DN",
     "BG-03",
     "- Đăng ký thành công\n- Cả 2 bên có 2 dòng KH-DN: dòng của A (in nghiêng LH1) và dòng của B (in nghiêng LH2)\n"
     "- Người đăng ký dòng mới = \"KD2 - <họ tên B>\""),
    ("012", "Khách Cá nhân - người khác bị chặn dù khác người liên hệ", "P0",
     "A đang giữ KH-CN còn hạn (TC_02.005). BG-07 do B lập, khách KH-CN",
     "1. ERP, B đăng ký BG-07\n2. Mở HRM, lọc theo KH-CN",
     "BG-07",
     "- ERP báo \"Không có quyền đăng ký khách hàng này!\"\n- HRM: KH-CN chỉ có 1 dòng của A"),
    ("013", "Đăng ký của người trước hết hạn / bị hủy thì người khác đăng ký được", "P1",
     "A đã HỦY đăng ký KH-DN / LH1 (TC_04.004) hoặc đăng ký đó đã hết hạn",
     "1. ERP, B đăng ký BG-02 (KH-DN / LH1)\n2. Mở HRM, lọc theo KH-DN",
     "BG-02",
     "- Đăng ký thành công\n- HRM có dòng mới của B, LH1, Còn hạn"),
    ("014", "Đăng ký từ đủ 3 loại báo giá hãng", "P1",
     "A lập 3 báo giá Đã duyệt, có file, 3 khách khác nhau: 1 báo giá vật tư - hàng hóa - thiết bị, 1 báo giá dự án, 1 báo giá hợp đồng nguyên tắc",
     "1. ERP, A đăng ký lần lượt cả 3 (vào từ 3 mục menu Báo giá tương ứng)\n2. Mở HRM",
     "3 báo giá",
     "- Cả 3 đăng ký thành công\n- HRM có đủ 3 dòng, cột Số báo giá đúng mã từng báo giá"),
    ("015", "Bấm Số báo giá trên HRM mở báo giá hãng bên ERP", "P1",
     "Dòng đăng ký của BG-01. Tài khoản Q có quyền xem báo giá trên ERP",
     "1. HRM, bấm số báo giá BG-01",
     "BG-01",
     "- Mở thẻ trình duyệt MỚI, hiện trang chi tiết BG-01 bên ERP\n- Màn danh sách HRM vẫn giữ nguyên ở thẻ cũ"),
    ("016", "Người xem không có quyền xem báo giá - khác nhau 2 bên đã chốt", "P2",
     "Tài khoản Q2: có quyền xem danh sách đăng ký, KHÔNG có quyền xem BG-01 trên ERP",
     "1. ERP, Q2 xem cột Số báo giá của dòng BG-01\n2. HRM, Q2 bấm số báo giá BG-01",
     "Tài khoản Q2",
     "- ERP: mã BG-01 là chữ thường, không bấm được\n- HRM: mã là link, bấm mở ERP và ERP từ chối xem báo giá\n"
     "- Khác biệt đã chốt, không ghi lỗi"),
    ("017", "Thông báo cho người có quyền xem khi có đăng ký mới", "P2",
     "Tài khoản Q có quyền xem trên ERP",
     "1. A đăng ký một báo giá mới trên ERP\n2. Q đăng nhập ERP, mở chuông thông báo",
     "-",
     "- Q nhận thông báo \"<họ tên A> - Phòng <tên phòng> vừa đăng ký khách hàng <mã KH> - <tên KH>\"\n"
     "- Bấm thông báo mở danh sách đăng ký toàn công ty của ERP"),
    ("018", "Nhân viên đổi phòng - Người đăng ký hiện phòng mới ở cả 2 bên", "P2",
     "A đã có đăng ký. Sau đó hồ sơ A được chuyển từ KD1 sang KD3",
     "1. Mở HRM và ERP, xem cột Người đăng ký của các dòng của A",
     "-",
     "- Cả 2 bên hiện \"KD3 - <họ tên A>\" (theo hồ sơ hiện tại), kể cả dòng đăng ký trước khi chuyển phòng"),
]

S3 = [
    ("001", "Tìm nhanh theo tên khách hàng - so với ERP", "P0",
     "Có đăng ký của KH-DN",
     "1. HRM: nhập một phần tên KH-DN vào ô tìm nhanh, bấm Tìm kiếm\n2. ERP: gõ cùng từ vào ô lọc cột Khách hàng đăng ký, nhấn Enter",
     "Một phần tên KH-DN",
     "- HRM chỉ còn các dòng có tên khách chứa từ khóa\n- Số dòng HRM bằng số dòng ERP"),
    ("002", "Tìm nhanh theo mã khách hàng (chỉ HRM có)", "P1",
     "Biết mã của KH-DN",
     "1. HRM: nhập mã KH-DN vào ô tìm nhanh, bấm Tìm kiếm",
     "Mã KH-DN",
     "- Ra các dòng của KH-DN\n- ERP không tìm được theo mã khách (khác biệt đã chốt)"),
    ("003", "Tìm nhanh theo người liên hệ", "P1",
     "KH-DN có dòng của LH1 và LH2",
     "1. HRM: nhập tên LH2 vào ô tìm nhanh, bấm Tìm kiếm",
     "Tên LH2",
     "- Chỉ còn dòng có người liên hệ LH2"),
    ("004", "Tìm nhanh theo tên người đăng ký", "P1",
     "B có ít nhất 1 đăng ký",
     "1. HRM: nhập họ tên B, bấm Tìm kiếm",
     "Họ tên B",
     "- Chỉ còn các dòng có Người đăng ký là B"),
    ("005", "Tìm nhanh theo số báo giá", "P1",
     "Có dòng của BG-01",
     "1. HRM: nhập mã BG-01, bấm Tìm kiếm",
     "Mã BG-01",
     "- Chỉ còn dòng có Số báo giá chứa mã đó"),
    ("006", "Ô chữ không tự lọc khi đang gõ", "P1",
     "Danh sách đang hiện toàn bộ",
     "1. Gõ từ khóa vào ô tìm nhanh, chờ 5 giây, không bấm gì\n2. Nhấn Enter",
     "-",
     "- Bước 1: bảng giữ nguyên\n- Bước 2: bảng lọc theo từ khóa"),
    ("007", "Lọc Khách hàng đăng ký (bộ lọc nâng cao) - so với ERP", "P0",
     "Có đăng ký của KH-DN và KH-CN",
     "1. HRM: mở Tìm kiếm nâng cao, nhập tên KH-CN vào ô Khách hàng đăng ký, bấm Tìm kiếm\n2. ERP: lọc cột Khách hàng đăng ký cùng tên",
     "Tên KH-CN",
     "- Chỉ còn dòng của KH-CN\n- Số dòng 2 bên bằng nhau"),
    ("008", "Lọc Thời hạn đăng ký = Còn hạn - so với ERP", "P0",
     "Có cả đăng ký còn hạn và đã hết hạn; KHÔNG có đăng ký nào hết hạn đúng hôm nay",
     "1. HRM: chọn Thời hạn đăng ký = Còn hạn\n2. ERP: chọn Còn hạn ở cột Thời hạn đăng ký",
     "Còn hạn",
     "- HRM tự lọc ngay, mọi dòng có Thời hạn đăng ký từ hôm nay trở đi\n- Số dòng 2 bên bằng nhau"),
    ("009", "Lọc Thời hạn đăng ký = Hết hạn - so với ERP", "P0",
     "Như TC trước",
     "1. HRM: chọn Hết hạn\n2. ERP: chọn Hết hạn",
     "Hết hạn",
     "- Mọi dòng có Thời hạn đăng ký trước hôm nay\n- Số dòng 2 bên bằng nhau\n"
     "- Còn hạn + Hết hạn = tổng khi không lọc"),
    ("010", "Lọc Người đăng ký - so với ERP", "P0",
     "A có 3 đăng ký, B có 1 (sau các TC phần II)",
     "1. HRM: chọn Người đăng ký = A\n2. ERP: chọn A ở cột Người đăng ký",
     "Người đăng ký: A",
     "- HRM tự lọc ngay, chỉ còn dòng của A (đúng 3 dòng)\n- Số dòng 2 bên bằng nhau"),
    ("011", "Lọc Số báo giá theo một phần mã", "P1",
     "Có nhiều báo giá cùng tiền tố mã",
     "1. HRM: nhập phần đầu mã báo giá vào ô Số báo giá, bấm Tìm kiếm\n2. ERP: lọc cột Số báo giá cùng chuỗi",
     "Phần đầu mã",
     "- Ra mọi dòng có số báo giá chứa chuỗi đó\n- Số dòng 2 bên bằng nhau"),
    ("012", "Kết hợp nhiều điều kiện", "P1",
     "A có đăng ký còn hạn và hết hạn",
     "1. HRM: Người đăng ký = A, Thời hạn đăng ký = Còn hạn\n2. ERP: lọc cùng 2 điều kiện",
     "-",
     "- Chỉ còn dòng của A còn hạn (thỏa đồng thời 2 điều kiện)\n- Số dòng 2 bên bằng nhau"),
    ("013", "Làm mới xóa mọi điều kiện", "P0",
     "Đang lọc Người đăng ký = A và từ khóa tìm nhanh",
     "1. Bấm Làm mới",
     "-",
     "- Ô tìm nhanh và các ô lọc về trống\n- Bảng tải lại toàn bộ, về trang 1"),
    ("014", "Ký tự đặc biệt không bị hiểu là ký tự đại diện", "P2",
     "Không có khách hàng nào tên chứa ký tự %",
     "1. Nhập \"%\" vào ô tìm nhanh, bấm Tìm kiếm",
     "%",
     "- Không trả về toàn bộ danh sách; không báo lỗi"),
]

S4 = [
    ("001", "Thời hạn đăng ký = Ngày đăng ký + N ngày", "P0",
     "Cấu hình ERP Thời gian đăng ký khách hàng = N (ví dụ 30)",
     "1. Tạo một đăng ký mới trên ERP hôm nay\n2. Xem dòng đó ở HRM và ERP",
     "N = 30",
     "- Thời hạn đăng ký = hôm nay + 30 ngày ở cả 2 bên\n- Thời hạn hiện dạng ngày/tháng/năm, không có giờ"),
    ("002", "Đổi cấu hình không làm đổi thời hạn của đăng ký cũ", "P1",
     "Đã có đăng ký tạo khi N = 30. Người có quyền cấu hình đổi Thời gian đăng ký khách hàng thành 15",
     "1. Xem lại đăng ký cũ ở HRM\n2. Tạo đăng ký mới, xem thời hạn\n3. Trả cấu hình về 30",
     "N: 30 rồi 15",
     "- Đăng ký cũ giữ thời hạn +30 ngày\n- Đăng ký mới có thời hạn +15 ngày\n- Cửa sổ đăng ký trên ERP hiện \"15 ngày\""),
    ("003", "Ngày hết hạn đúng hôm nay - HRM Còn hạn cả ngày, ERP Hết hạn từ giờ đăng ký", "P1",
     "Người có quyền cấu hình đặt Thời gian đăng ký khách hàng = 0 ngày (nhớ trả lại sau khi test)",
     "1. A đăng ký một báo giá còn trống khách (lúc 10:00)\n2. Sau đó vài phút, xem dòng đó ở HRM với lọc Còn hạn\n"
     "3. Xem ở ERP với lọc Còn hạn và Hết hạn\n4. B thử đăng ký cùng khách đó trên ERP\n5. Sáng hôm sau xem lại HRM\n6. Trả cấu hình về N",
     "N = 0",
     "- Thời hạn đăng ký = hôm nay ở cả 2 bên\n- HRM: dòng nằm trong Còn hạn suốt hôm nay\n"
     "- ERP: dòng đã nằm trong Hết hạn (đã qua giờ đăng ký)\n- B đăng ký được ngay vì ERP coi đăng ký của A đã hết hạn\n"
     "- Hôm sau HRM cũng chuyển sang Hết hạn\n- Lệch hôm nay là khác biệt ĐÃ CHỐT, không ghi lỗi"),
    ("004", "Hủy đăng ký trên ERP - dòng biến mất ở cả 2 bên", "P0",
     "A đang giữ KH-DN / LH1 còn hạn. Tổng số dòng HRM = T",
     "1. ERP, đăng nhập A, vào " + ERP_CA_NHAN + "\n2. Bấm nút Hủy đăng ký (dấu x đỏ) ở dòng KH-DN / LH1, xác nhận\n"
     "3. Q mở danh sách toàn công ty ở ERP và HRM",
     "-",
     "- ERP báo \"Hủy đăng ký thành công!\"\n- Dòng biến mất ở cả ERP và HRM (bị xóa hẳn, KHÔNG chuyển thành Hết hạn)\n"
     "- Tổng số dòng HRM = T - 1"),
    ("005", "Không hủy được đăng ký đã hết hạn hoặc của người khác", "P1",
     "A có 1 đăng ký đã hết hạn",
     "1. ERP, A mở \"Danh sách khách hàng đã đăng ký\"",
     "-",
     "- Danh sách cá nhân chỉ có đăng ký CÒN HẠN của chính A, mỗi dòng có nút Hủy\n"
     "- Đăng ký hết hạn không có ở danh sách cá nhân nhưng vẫn hiện ở danh sách toàn công ty của 2 bên"),
]

S5 = [
    ("001", "Sắp xếp theo Ngày đăng ký (chỉ HRM có)", "P1",
     "Có từ 15 đăng ký trở lên",
     "1. Bấm tiêu đề cột Ngày đăng ký\n2. Bấm lần nữa",
     "-",
     "- Lần 1 và lần 2 sắp ngược chiều nhau theo ngày giờ đăng ký\n- Mũi tên trên tiêu đề đổi chiều\n"
     "- ERP không sắp xếp được theo cột (khác biệt đã chốt)"),
    ("002", "Sắp xếp theo Thời hạn đăng ký", "P1",
     "Có đăng ký với nhiều thời hạn khác nhau",
     "1. Bấm tiêu đề cột Thời hạn đăng ký",
     "-",
     "- Sắp đúng theo ngày (so cả năm, tháng), không sắp theo chữ"),
    ("003", "Chỉ 2 cột có sắp xếp", "P2",
     "-",
     "1. Quan sát biểu tượng sắp xếp trên tiêu đề cột",
     "-",
     "- Chỉ Ngày đăng ký và Thời hạn đăng ký có biểu tượng sắp xếp"),
    ("004", "Phân trang mặc định 10 dòng", "P0",
     "Có trên 10 đăng ký",
     "1. Mở màn, đọc chân bảng",
     "-",
     "- Bảng 10 dòng; chân bảng \"Hiển thị 1 - 10 / N đăng ký\"\n- ERP mặc định cũng 10 mục / trang"),
    ("005", "Chuyển trang giữ bộ lọc, STT liên tục", "P1",
     "Đang lọc Thời hạn đăng ký = Hết hạn, có trên 10 dòng",
     "1. Sang trang 2",
     "-",
     "- STT trang 2 bắt đầu từ 11\n- Bộ lọc Hết hạn vẫn giữ"),
    ("006", "Đổi số dòng mỗi trang", "P1",
     "Có trên 20 đăng ký",
     "1. Chọn Số dòng/trang = 20",
     "20",
     "- Bảng 20 dòng, quay về trang 1, chân bảng cập nhật"),
    ("007", "Cấu hình cột hiển thị", "P2",
     "-",
     "1. Bấm nút Cấu hình cột hiển thị\n2. Ẩn cột Ghi chú, lưu\n3. Tải lại trang",
     "Ẩn Ghi chú",
     "- Cột Ghi chú biến mất và vẫn ẩn sau khi tải lại\n- Không bỏ được cột STT và Khách hàng đăng ký"),
]

S6 = [
    ("001", "Cửa sổ chọn trường xuất Excel", "P1",
     "-",
     "1. Bấm Xuất Excel",
     "-",
     "- Cửa sổ chọn trường có 7 trường: Khách hàng đăng ký, Người liên hệ, Ngày đăng ký, Thời hạn đăng ký, Người đăng ký, Số báo giá, Ghi chú\n"
     "- Mặc định chọn sẵn các cột đang hiện trên bảng"),
    ("002", "Xuất Excel theo bộ lọc đang áp, đủ mọi trang", "P0",
     "Đang lọc Người đăng ký = A (ví dụ 3 dòng)",
     "1. Bấm Xuất Excel, giữ mặc định, bấm xuất\n2. Mở file",
     "-",
     "- Báo \"Xuất Excel thành công\", tải về file danh sách đăng ký khách hàng\n"
     "- File có đúng 3 dòng của A, đủ mọi trang (không chỉ trang đang xem)\n- Giá trị từng ô trùng màn hình"),
    ("003", "Người liên hệ là cột riêng trong file", "P2",
     "Có dòng KH-DN / LH1",
     "1. Xuất Excel có chọn trường Người liên hệ",
     "-",
     "- File có cột Người liên hệ riêng, dòng KH-DN ghi LH1; dòng khách Cá nhân để trống"),
    ("004", "Bỏ bớt trường khi xuất", "P2",
     "-",
     "1. Bấm Xuất Excel, bỏ chọn Ghi chú và Số báo giá, bấm xuất",
     "-",
     "- File không có 2 cột đã bỏ chọn"),
    ("005", "ERP không có xuất Excel", "P2",
     "-",
     "1. Mở màn ERP, tìm nút xuất",
     "-",
     "- ERP không có nút xuất Excel ở màn này; chức năng chỉ có ở HRM (khác biệt đã chốt)"),
]

S7 = [
    ("001", "Luồng đầy đủ: tạo, chặn, hủy - đếm khớp 2 bên sau mỗi bước", "P0",
     "Dữ liệu mẫu mục 9; ghi tổng số dòng ban đầu HRM = ERP = T",
     "1. A đăng ký BG-01 (KH-DN / LH1)\n2. B đăng ký BG-02 (KH-DN / LH1) - bị chặn\n3. B đăng ký BG-03 (KH-DN / LH2)\n"
     "4. A đăng ký BG-06 (KH-CN)\n5. B đăng ký BG-07 (KH-CN) - bị chặn\n6. A hủy đăng ký KH-DN / LH1\n"
     "7. B đăng ký lại BG-02\n8. Sau mỗi bước, Q đếm tổng số dòng ở HRM và ERP",
     "-",
     "- Tổng số dòng sau từng bước: T+1, T+1, T+2, T+3, T+3, T+2, T+3 ở CẢ 2 bên\n"
     "- Cuối luồng, lọc theo KH-DN: 2 dòng của B (LH1, LH2); lọc theo KH-CN: 1 dòng của A\n"
     "- Mọi cột của các dòng này trùng nhau giữa HRM và ERP"),
    ("002", "Đối chiếu từng dòng một trang dữ liệu thật", "P0",
     "Dữ liệu thật trên môi trường test",
     "1. HRM và ERP: không lọc, trang 1, 10 dòng\n2. So lần lượt 10 dòng, 6 cột",
     "-",
     "- 10 dòng trùng nhau về thứ tự và nội dung 6 cột\n"
     "- Chỉ được khác ở các điểm đã chốt (mục 9): ô Người đăng ký của nhân viên chưa có phòng, link số báo giá"),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", S1),
    ("II", "TẠO ĐĂNG KÝ TỪ ERP & ĐỐI CHIẾU HIỂN THỊ HRM", S2),
    ("III", "BỘ LỌC & TÌM KIẾM", S3),
    ("IV", "THỜI HẠN, HẾT HẠN & HỦY ĐĂNG KÝ", S4),
    ("V", "SẮP XẾP, PHÂN TRANG & CẤU HÌNH CỘT", S5),
    ("VI", "XUẤT EXCEL", S6),
    ("VII", "E2E FLOW ĐỐI CHIẾU ERP - HRM", S7),
]

if __name__ == "__main__":
    build(output_file=os.path.join(HERE, "testcase - Danh sach dang ky khach hang toan cong ty.xlsx"),
          sheet_name="Trang tính1",
          feature_name=TEN + " - Cập nhật ngày " + NGAY,
          module_name=MODULE,
          description_block=DESCRIPTION_BLOCK, role_tcs=ROLE_TCS, sections=SECTIONS)
