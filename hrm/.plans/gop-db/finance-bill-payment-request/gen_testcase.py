# -*- coding: utf-8 -*-
"""Sinh file testcase Excel cho man "Phieu de nghi thanh toan" (phan he Tai chinh).

Nguon doc code 28/08/2026 (nhanh gop_db):
  BE  Modules/Finance/Routes/api.php (:527-560) — 15 route
      Modules/Finance/Http/Controllers/V1/BillPaymentRequestController.php
      Modules/Finance/Entities/BillPaymentRequest/BillPaymentRequest.php
      Modules/Finance/Services/{BillPaymentRequestService,BillPaymentApprovalService,
                                BillPaymentRequestNotifyService,BillPaymentAttachmentService}.php
      Modules/Finance/Http/Requests/BillPaymentRequest/*.php  (nguyen van thong bao loi)
      Modules/Finance/Exports/BillPaymentRequestExport.php
      Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (:1180-1190)
  FE  hrm-client/pages/finance/bill-payment-requests/{index,create}.vue
      .../_id/{index,edit,print}.vue
      .../components/{BillPaymentRequestForm,BillPaymentRequestDetailTable,BankInfoSection,
                      AttachmentSection,ApproveActions,RejectModal,DeliveryTripDetailModal}.vue
  Anh that: dntt_chi_shots/ (cong dev hrm-crm.eteksofts.com, 28/08/2026)

Chay:  python .plans/gop-db/finance-bill-payment-request/gen_testcase.py
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

OUT = os.path.join(HERE, "testcase - Phiếu đề nghị thanh toán.xlsx")
MODULE = "Phiếu đề nghị thanh toán"

# ════════════════════════════════════════════════════ 1. KHỐI MÔ TẢ (9 mục)
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Phiếu đề nghị thanh toán là chứng từ đề nghị chi tiền, do bộ phận kinh doanh lập và đi qua "
     "LUỒNG DUYỆT 5 CẤP: Trưởng phòng → Kế toán công nợ → Kế toán trưởng → (tuỳ chọn) Ban giám "
     "đốc → Chờ tạo phiếu chi. Mỗi cấp duyệt được sửa số tiền duyệt của từng dòng chi tiết và "
     "số tiền đó ghi vào cột riêng của cấp mình.\n"
     "Màn hình cho phép: lập phiếu (lưu nháp / gửi duyệt), sửa, xóa, xem chi tiết, duyệt theo "
     "cấp, từ chối kèm ghi chú, đính kèm file, in và xuất Excel.\n"
     "Một màn hình dùng cho 4 chế độ xem: Tất cả (mặc định) · Của tôi · Chờ duyệt · Đã duyệt. "
     "Menu chỉ có 2 lối vào (Đề nghị thanh toán và Phiếu đề nghị thanh toán chờ duyệt); 2 chế độ "
     "Của tôi và Đã duyệt vào bằng đường dẫn."),

    ("2. Đối tượng được tính / hiển thị",
     "Chế độ **Tất cả** hiển thị phiếu theo phạm vi quyền của người đăng nhập:\n"
     "- Có 'Xem tất cả phiếu đề nghị thanh toán của tổng công ty' (hoặc quản trị hệ thống): mọi "
     "công ty.\n"
     "- Có 'Xem tất cả phiếu đề nghị thanh toán của công ty': phiếu công ty mình.\n"
     "- Có 'Xem tất cả phiếu đề nghị thanh toán của phòng ban': phiếu các phòng ban mình quản lý.\n"
     "- Có 'Xem tất cả phiếu đề nghị thanh toán của bộ phận': phiếu các bộ phận mình quản lý.\n"
     "- Không có quyền nào: chỉ phiếu do chính mình lập.\n"
     "Chế độ **Của tôi**: mọi phiếu do chính mình lập, kể cả phiếu nháp.\n"
     "Chế độ **Chờ duyệt**: chỉ phiếu trong công ty mình VÀ đang ở đúng trạng thái mà mình có "
     "quyền duyệt (5 vai: Trưởng phòng · Kế toán công nợ · Kế toán trưởng · Ban giám đốc · Kế "
     "toán thanh toán).\n"
     "Chế độ **Đã duyệt**: phiếu mà chính mình đã duyệt ở bất kỳ cấp nào.\n"
     "Đủ 10 trạng thái đều hiển thị: Đang tạo, Chờ TP duyệt, Chờ kế toán công nợ duyệt, Chờ kế "
     "toán trưởng duyệt, Chờ ban giám đốc duyệt, Chờ tạo phiếu chi, Chờ duyệt phiếu chi, Duyệt "
     "phiếu chi, Đã hủy, Không duyệt."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu ở trạng thái Đang tạo (nháp) của NGƯỜI KHÁC luôn bị ẩn ở chế độ Tất cả, kể cả với "
     "người xem toàn tổng công ty.\n"
     "- Chế độ Chờ duyệt bỏ phiếu của công ty khác (kể cả người có quyền xem tổng công ty) và bỏ "
     "phiếu ở trạng thái mà mình không giữ vai duyệt. Không giữ vai nào thì danh sách rỗng.\n"
     "- Cấp Trưởng phòng chỉ thấy phiếu của các phòng ban mình được giao quản lý, không thấy "
     "phiếu phòng ban khác dù cùng công ty.\n"
     "- Danh sách chọn Loại chi chỉ có 4 giá trị còn dùng: Chi trả nhà cung cấp, Chi trả lại "
     "khách hàng, Chi thưởng thực hiện hợp đồng, Thanh toán chi phí vận chuyển NCC. Ba loại cũ "
     "(Chi thưởng NVKD, Chi thu nhập cho nhân viên, Chi khác) không chọn mới được nhưng phiếu cũ "
     "vẫn hiển thị đúng tên.\n"
     "- Cửa sổ chọn hợp đồng chỉ liệt kê hợp đồng đúng bản chất của loại chi: loại Chi trả nhà "
     "cung cấp chỉ có hợp đồng MUA; loại Chi trả lại khách hàng và Chi thưởng thực hiện hợp đồng "
     "chỉ có hợp đồng BÁN. Loại Thanh toán chi phí vận chuyển NCC không gắn hợp đồng mà gắn "
     "chuyến xe."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Hai ô 'Ngày lập từ' và 'Ngày lập đến' lọc theo NGÀY LẬP PHIẾU (cột Ngày lập trên lưới), "
     "không phải Ngày nhận (ngày trưởng phòng duyệt) và cũng không phải Ngày cập nhật.\n"
     "Cả hai mốc lấy trọn ngày: chọn 'đến ngày' là hôm nay thì phiếu vừa lập sáng nay vẫn nằm "
     "trong kết quả. Bỏ trống một đầu thì phía đó không giới hạn.\n"
     "Riêng ô 'Đến ngày' trên FORM (chỉ có ở loại chi Thanh toán chi phí vận chuyển NCC) KHÔNG "
     "phải bộ lọc — đó là mốc để hệ thống lấy các chuyến xe phát sinh tới ngày đó."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Một phiếu gồm 4 khối:\n"
     "- Thông tin chung: Mã phiếu, Loại chi, Hình thức thanh toán, Loại tiền, Tỷ giá, Người tạo, "
     "Phòng ban, Lý do chi; thêm 'Đến ngày' với loại vận chuyển, thêm ô chọn Khách hàng / Nhà "
     "cung cấp khi hình thức là chuyển khoản.\n"
     "- Thông tin ngân hàng: chỉ hiện khi hình thức thanh toán là chuyển khoản. Nhà cung cấp "
     "trong nước dùng bộ 5 ô (Số tài khoản, Tên tài khoản, Tên ngân hàng, Chi nhánh, Thành phố); "
     "nhà cung cấp nước ngoài dùng bộ ô có Swift Code, IBAN Number, Địa chỉ, Phí và cả khối ngân "
     "hàng trung gian.\n"
     "- Chi tiết: nhiều dòng. Cột thay đổi theo loại chi và hình thức thanh toán (xem mục 9).\n"
     "- File đính kèm: danh sách file, bắt buộc ít nhất 1 file với loại Chi trả nhà cung cấp.\n"
     "Ở màn xem chi tiết, bảng Chi tiết có thêm 4 cột tiền: TP duyệt, KT công nợ duyệt, "
     "KT trưởng / BGĐ duyệt và Số tiền chi."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Dòng 'Tổng cộng' dưới bảng chi tiết cộng dồn ngay tại chỗ cho mọi cột số, đổi theo từng "
     "phím gõ.\n"
     "- Cột 'Số tiền' trên lưới danh sách hiển thị số tiền của CẤP DUYỆT GẦN NHẤT đã ghi: phiếu "
     "chưa qua cấp nào thì lấy số đề nghị, qua Trưởng phòng thì lấy số Trưởng phòng duyệt, và cứ "
     "thế. Kèm mã loại tiền của phiếu.\n"
     "- Cột 'Khách hàng / Nhà cung cấp' trên lưới đổi nguồn theo loại chi và hình thức thanh "
     "toán: loại vận chuyển và loại Chi trả nhà cung cấp + chuyển khoản lấy nhà cung cấp của "
     "phiếu; các loại còn lại + chuyển khoản lấy khách hàng của phiếu; hình thức tiền mặt lấy "
     "đối tượng của DÒNG CHI TIẾT ĐẦU TIÊN; loại Chi thưởng thực hiện hợp đồng + tiền mặt thì "
     "cột này luôn trống.\n"
     "- Cột quy đổi VND của mỗi dòng = số tiền nhập × tỷ giá; chọn loại tiền VNĐ thì không có "
     "cột quy đổi.\n"
     "- Số tiền còn nợ / công nợ còn lại KHÔNG lưu trong phiếu mà tính lại theo sổ kế toán mỗi "
     "lần mở."),

    ("7. Phân quyền cấp",
     "Mười quyền liên quan tới màn (tên nguyên văn trong hệ thống phân quyền):\n"
     "- Kinh doanh đề nghị thanh toán\n"
     "- Trưởng phòng duyệt đề nghị thanh toán\n"
     "- Kế toán công nợ duyệt đề nghị thanh toán\n"
     "- Kế toán trưởng duyệt đề nghi thanh toán\n"
     "- Ban giám đốc duyệt đề nghi thanh toán\n"
     "- Kế toán thanh toán\n"
     "- Xem tất cả phiếu đề nghị thanh toán của tổng công ty\n"
     "- Xem tất cả phiếu đề nghị thanh toán của công ty\n"
     "- Xem tất cả phiếu đề nghị thanh toán của phòng ban\n"
     "- Xem tất cả phiếu đề nghị thanh toán của bộ phận\n"
     "⚠️ Hai tên quyền có chữ 'đề nghi' (thiếu dấu) là ĐÚNG NGUYÊN VĂN của hệ thống cũ, cố ý giữ "
     "nguyên — không phải lỗi chính tả cần báo.\n"
     "Bốn quyền 'Xem tất cả…' chỉ quyết định phạm vi dữ liệu ở chế độ Tất cả, xét theo đúng thứ "
     "tự trên. Năm quyền duyệt quyết định phiếu nào vào chế độ Chờ duyệt và nút duyệt nào hiện "
     "ra. Quyền 'Kinh doanh đề nghị thanh toán' chỉ dùng để chọn người nhận thông báo khi phiếu "
     "bị từ chối. Việc lập phiếu KHÔNG gắn quyền."),

    ("8. Cách tính các ô thống kê",
     "- Ô 'Hiển thị a–b / N' dưới lưới: a là dòng đầu trang đang xem, b là dòng cuối, N là tổng "
     "số phiếu khớp bộ lọc của CHẾ ĐỘ đang xem (không phải tổng toàn hệ thống).\n"
     "- Ô 'Số dòng/trang': đổi giá trị thì quay về trang 1 và tải lại danh sách.\n"
     "- Bảng chi tiết, dòng 'Tổng cộng' cộng dồn từng cột: Tổng cước, Đã thanh toán, Số tiền còn "
     "nợ, Số tiền đề nghị chi (và cột quy đổi), TP duyệt, KT công nợ duyệt, KT trưởng / BGĐ "
     "duyệt, Số tiền chi.\n"
     "- Cột 'Số tiền chi' hiển thị dấu gạch dưới khi phiếu chưa có phiếu chi hoặc giấy ủy nhiệm "
     "chi tương ứng — KHÔNG hiển thị số 0."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất của màn:\n"
     "- **Từ chối ở cấp Trưởng phòng đưa phiếu về 'Đang tạo'**, không phải 'Không duyệt'. Chỉ "
     "các cấp từ Kế toán công nợ trở lên mới đẩy phiếu sang 'Không duyệt'. Đây là quy tắc nghiệp "
     "vụ cố ý giữ nguyên từ hệ thống cũ.\n"
     "- Ô ghi chú bắt buộc trong cửa sổ Từ chối ĐỔI TÊN theo cấp đang giữ phiếu (Ghi chú của "
     "Trưởng phòng / Kế toán công nợ / Kế toán trưởng / Ban giám đốc). Ô 'Lý do không duyệt' "
     "phía dưới KHÔNG bắt buộc.\n"
     "- Ở cấp Kế toán trưởng có HAI nút: 'Duyệt' đẩy thẳng sang Chờ tạo phiếu chi, "
     "'Chuyển duyệt BGĐ' đẩy sang Chờ ban giám đốc duyệt.\n"
     "- Bảng chi tiết ĐỔI CỘT theo loại chi và hình thức thanh toán. Tiền mặt mới có cột đối "
     "tượng theo dòng; chuyển khoản chọn đối tượng một lần ở Thông tin chung.\n"
     "- Lưu nháp và Lưu và gửi duyệt khác nhau về ràng buộc: lưu nháp không bắt buộc dòng chi "
     "tiết, file đính kèm và khối ngân hàng.\n"
     "- Loại Chi trả nhà cung cấp BẮT BUỘC có ít nhất 1 file đính kèm khi gửi duyệt; ba loại còn "
     "lại không bắt buộc.\n"
     "- Loại Thanh toán chi phí vận chuyển NCC KHÔNG thêm dòng bằng tay: bấm 'Lấy dữ liệu' để hệ "
     "thống sinh dòng theo nhà cung cấp và mốc 'Đến ngày', rồi tích chọn dòng cần thanh toán.\n"
     "- Ô tìm nhanh theo mã phiếu chờ bấm nút 'Tìm kiếm'; mọi tiêu chí trong Tìm kiếm nâng cao "
     "lọc ngay khi đổi giá trị.\n"
     "- Hệ thống nhớ bộ lọc 10 phút và nhớ RIÊNG cho từng chế độ xem; bộ cột thì dùng chung cho "
     "cả 4 chế độ.\n"
     "- Gõ tên nhà cung cấp vào ô lọc 'Khách hàng' luôn ra 0 kết quả — hai ô lọc này lấy từ hai "
     "danh sách khác nhau. Dùng đúng ô 'Nhà cung cấp'.\n"
     "- Số tiền hiển thị kiểu 1,234,567 (dấu phẩy ngăn nghìn).\n"
     "- Trạng thái 'Chờ duyệt phiếu chi', 'Duyệt phiếu chi', 'Đã hủy' do màn Phiếu chi / Ủy nhiệm "
     "chi đặt; màn này chỉ hiển thị."),
]

# ════════════════════════════════════════════════════ 2. TC PHÂN QUYỀN
ROLE_TCS = [
    ("00", "Không có quyền xem nào — chỉ thấy phiếu của chính mình", "P0",
     "Tài khoản A thuộc công ty 1, phòng Kinh doanh 1, KHÔNG có bất kỳ quyền nào trong nhóm "
     "'Xem tất cả phiếu đề nghị thanh toán…' và không giữ vai duyệt nào. Dữ liệu: A đã lập 4 "
     "phiếu; người khác cùng phòng đã lập 9 phiếu.",
     "1. Đăng nhập bằng tài khoản A.\n"
     "2. Vào menu Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi > Đề nghị thanh toán.\n"
     "3. Đọc dòng đếm dưới lưới và cột Người lập.",
     "—",
     "- Danh sách chỉ có đúng 4 phiếu, đều do tài khoản A lập.\n"
     "- Vẫn có nút 'Tạo mới' (việc lập phiếu không gắn quyền).\n"
     "- ⚠️ Bộ lọc nâng cao KHÔNG hiện ô Công ty / Phòng ban / Bộ phận."),

    ("01", "Quyền 'Xem tất cả phiếu đề nghị thanh toán của bộ phận'", "P0",
     "Tài khoản B chỉ có quyền này, được giao quản lý bộ phận 'Tổ kỹ thuật 1' của công ty 1. "
     "Dữ liệu: 5 phiếu thuộc bộ phận này, 8 phiếu thuộc bộ phận khác cùng công ty.",
     "1. Đăng nhập bằng tài khoản B, mở màn Đề nghị thanh toán.\n"
     "2. Mở 'Tìm kiếm nâng cao' và quan sát các ô cấp tổ chức.",
     "—",
     "- Danh sách đúng 5 phiếu của bộ phận được giao.\n"
     "- Bộ lọc có ô 'Bộ phận', không có ô 'Công ty'.\n"
     "- ⚠️ Phiếu nháp của người khác trong cùng bộ phận vẫn KHÔNG hiện."),

    ("02", "Quyền 'Xem tất cả phiếu đề nghị thanh toán của phòng ban'", "P0",
     "Tài khoản C chỉ có quyền này, quản lý phòng 'Kinh doanh 1' và 'Kinh doanh 2' của công ty 1. "
     "Dữ liệu: 11 phiếu thuộc 2 phòng này, 15 phiếu phòng khác.",
     "1. Đăng nhập bằng tài khoản C, mở màn Đề nghị thanh toán.\n"
     "2. Đọc cột Phòng ban của toàn bộ danh sách.",
     "—",
     "- Chỉ có 11 phiếu, cột Phòng ban chỉ chứa 2 phòng được giao.\n"
     "- Bộ lọc có ô 'Phòng ban', không có ô 'Công ty'."),

    ("03", "Quyền 'Xem tất cả phiếu đề nghị thanh toán của công ty'", "P0",
     "Tài khoản D chỉ có quyền này, thuộc công ty 1. Dữ liệu: 30 phiếu công ty 1, 12 phiếu công "
     "ty 4.",
     "1. Đăng nhập bằng tài khoản D, mở màn Đề nghị thanh toán.\n"
     "2. Mở 'Tìm kiếm nâng cao'.",
     "—",
     "- Thấy 30 phiếu công ty 1, không thấy phiếu công ty 4.\n"
     "- Bộ lọc hiện ô 'Phòng ban', không hiện ô 'Công ty'."),

    ("04", "Quyền 'Xem tất cả phiếu đề nghị thanh toán của tổng công ty'", "P0",
     "Tài khoản E có quyền này. Hệ thống có phiếu của ít nhất 2 công ty.",
     "1. Đăng nhập bằng tài khoản E, mở màn Đề nghị thanh toán.\n"
     "2. Mở 'Tìm kiếm nâng cao', chọn lần lượt từng công ty.",
     "Công ty: chọn từng giá trị",
     "- Danh sách gồm phiếu của mọi công ty.\n"
     "- Bộ lọc hiện đủ ô Công ty, Phòng ban, Bộ phận.\n"
     "- Chọn 1 công ty thì danh sách rút lại đúng phiếu của công ty đó."),

    ("05", "Quyền 'Trưởng phòng duyệt đề nghị thanh toán'", "P0",
     "Tài khoản F có quyền này, quản lý phòng 'Kinh doanh 1' của công ty 1. Dữ liệu: 3 phiếu ở "
     "trạng thái 'Chờ TP duyệt' thuộc phòng Kinh doanh 1; 4 phiếu 'Chờ TP duyệt' thuộc phòng "
     "khác cùng công ty; 2 phiếu 'Chờ kế toán công nợ duyệt'.",
     "1. Đăng nhập bằng tài khoản F.\n"
     "2. Vào menu Phê duyệt - Công nợ - Thu - Chi > Phiếu đề nghị thanh toán chờ duyệt.\n"
     "3. Đọc cột Trạng thái và cột Phòng ban.",
     "—",
     "- Danh sách đúng 3 phiếu, tất cả ở trạng thái 'Chờ TP duyệt' và thuộc phòng Kinh doanh 1.\n"
     "- ⚠️ KHÔNG có phiếu 'Chờ TP duyệt' của phòng ban khác.\n"
     "- ⚠️ KHÔNG có phiếu ở trạng thái của cấp khác.\n"
     "- Thanh công cụ không có nút 'Tạo mới'."),

    ("06", "Quyền 'Kế toán công nợ duyệt đề nghị thanh toán'", "P0",
     "Tài khoản G có quyền này, thuộc công ty 1. Dữ liệu công ty 1: 6 phiếu 'Chờ kế toán công nợ "
     "duyệt' (thuộc nhiều phòng ban khác nhau), 3 phiếu 'Chờ TP duyệt'.",
     "1. Đăng nhập bằng tài khoản G, mở màn chờ duyệt.",
     "—",
     "- Danh sách đúng 6 phiếu, tất cả ở trạng thái 'Chờ kế toán công nợ duyệt'.\n"
     "- ⚠️ Cấp này KHÔNG bị giới hạn theo phòng ban, chỉ giới hạn theo công ty."),

    ("07", "Quyền 'Kế toán trưởng duyệt đề nghi thanh toán'", "P0",
     "Tài khoản H có quyền này, thuộc công ty 1. Dữ liệu: 4 phiếu 'Chờ kế toán trưởng duyệt'.",
     "1. Đăng nhập bằng tài khoản H, mở màn chờ duyệt.\n"
     "2. Mở chi tiết một phiếu, đọc thanh nút dưới cùng.",
     "—",
     "- Danh sách đúng 4 phiếu ở trạng thái 'Chờ kế toán trưởng duyệt'.\n"
     "- Màn chi tiết có ĐỦ HAI nút: 'Duyệt' và 'Chuyển duyệt BGĐ'."),

    ("08", "Quyền 'Ban giám đốc duyệt đề nghi thanh toán'", "P0",
     "Tài khoản I có quyền này, thuộc công ty 1. Dữ liệu: 2 phiếu 'Chờ ban giám đốc duyệt'.",
     "1. Đăng nhập bằng tài khoản I, mở màn chờ duyệt.\n"
     "2. Mở chi tiết một phiếu.",
     "—",
     "- Danh sách đúng 2 phiếu ở trạng thái 'Chờ ban giám đốc duyệt'.\n"
     "- Màn chi tiết chỉ có một nút 'Duyệt' (không có nút chuyển cấp)."),

    ("09", "Quyền 'Kế toán thanh toán'", "P0",
     "Tài khoản K có quyền này, thuộc công ty 1. Dữ liệu: 5 phiếu 'Chờ tạo phiếu chi' — 3 phiếu "
     "hình thức tiền mặt, 2 phiếu hình thức chuyển khoản.",
     "1. Đăng nhập bằng tài khoản K, mở màn chờ duyệt.\n"
     "2. Xem cột Hành động của các dòng.",
     "—",
     "- Danh sách đúng 5 phiếu ở trạng thái 'Chờ tạo phiếu chi'.\n"
     "- Dòng hình thức tiền mặt có nút 'Tạo phiếu chi'; dòng hình thức chuyển khoản có nút "
     "'Tạo ủy nhiệm chi'.\n"
     "- ⚠️ Hai nút này LOẠI TRỪ nhau, không dòng nào hiện cả hai."),

    ("10", "Người giữ nhiều vai duyệt cùng lúc", "P1",
     "Tài khoản L có ĐỒNG THỜI 'Kế toán công nợ duyệt đề nghị thanh toán' và "
     "'Kế toán trưởng duyệt đề nghi thanh toán', thuộc công ty 1.",
     "1. Đăng nhập bằng tài khoản L, mở màn chờ duyệt.\n"
     "2. Đọc cột Trạng thái.",
     "—",
     "- Danh sách gồm CẢ phiếu 'Chờ kế toán công nợ duyệt' LẪN phiếu 'Chờ kế toán trưởng duyệt'.\n"
     "- Mở từng phiếu, nút duyệt hiện đúng theo trạng thái của phiếu đó."),

    ("11", "Không giữ vai duyệt nào — màn chờ duyệt rỗng", "P0",
     "Tài khoản A (không có quyền duyệt nào) đã đăng nhập.",
     "1. Quan sát menu Phê duyệt - Công nợ - Thu - Chi.\n"
     "2. Mở đường dẫn /finance/bill-payment-requests?mode=pending.",
     "—",
     "- Mục menu vẫn hiển thị (mục này không gắn quyền ẩn hiện).\n"
     "- ⚠️ Danh sách RỖNG, hiện 'Không có dữ liệu phù hợp bộ lọc.', trang không báo lỗi."),

    ("12", "Chế độ Đã duyệt chỉ hiện phiếu chính mình đã duyệt", "P0",
     "Tài khoản F đã duyệt 3 phiếu ở cấp Trưởng phòng; tài khoản G đã duyệt 6 phiếu khác.",
     "1. Đăng nhập tài khoản F, mở đường dẫn "
     "/finance/bill-payment-requests?mode=approved.",
     "—",
     "- Danh sách đúng 3 phiếu F đã duyệt.\n"
     "- Không có phiếu nào do G duyệt.\n"
     "- Tiêu đề trang là 'Phiếu đề nghị thanh toán đã duyệt', không có nút 'Tạo mới'."),

    ("13", "Chặn bỏ qua giao diện — duyệt phiếu khi không đúng vai", "P0",
     "Tài khoản A (không giữ vai duyệt nào). Phiếu P đang ở trạng thái 'Chờ TP duyệt'.",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Duyệt cho phiếu P, bỏ qua giao diện, bằng "
     "phiên đăng nhập của tài khoản A.\n"
     "2. Mở lại chi tiết phiếu P trên giao diện.",
     "Trạng thái chuyển sang: Chờ kế toán công nợ duyệt",
     "- Hệ thống từ chối, báo không có quyền duyệt phiếu này ở trạng thái hiện tại.\n"
     "- Trạng thái phiếu không đổi, lịch sử không sinh thêm mốc nào.\n"
     "- ⚠️ Nhóm test này dành cho tester kỹ thuật."),

    ("14", "Chặn bỏ qua giao diện — nhảy cóc cấp duyệt", "P0",
     "Tài khoản F (Trưởng phòng, đúng phòng ban). Phiếu P đang ở 'Chờ TP duyệt'.",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Duyệt cho phiếu P, khai trạng thái chuyển "
     "sang là 'Chờ tạo phiếu chi' (bỏ qua 2 cấp giữa).",
     "Trạng thái chuyển sang: Chờ tạo phiếu chi",
     "- Hệ thống từ chối với thông báo 'Không thể chuyển phiếu sang trạng thái này'.\n"
     "- Phiếu vẫn ở 'Chờ TP duyệt'."),

    ("15", "Chặn bỏ qua giao diện — sửa / xóa phiếu của người khác", "P0",
     "Tài khoản A đã đăng nhập. Phiếu Q do người khác lập, đang ở trạng thái 'Đang tạo'.",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Sửa cho phiếu Q.\n"
     "2. Làm tương tự với chức năng Xóa.",
     "Lý do chi: 'sửa trộm'",
     "- Cả 2 lần hệ thống đều từ chối, báo không có quyền sửa / xóa phiếu này.\n"
     "- Phiếu Q còn nguyên."),

    ("16", "Chặn xem phiếu ngoài phạm vi bằng đường dẫn trực tiếp", "P0",
     "Tài khoản D chỉ có quyền xem theo công ty (công ty 1). Phiếu R thuộc công ty 4, trạng thái "
     "'Chờ kế toán trưởng duyệt'.",
     "1. Gõ thẳng đường dẫn chi tiết của phiếu R vào trình duyệt.",
     "—",
     "- Hệ thống từ chối, báo không có quyền xem phiếu này và đưa về màn danh sách.\n"
     "- Không lộ bất kỳ dữ liệu nào của phiếu R."),
]

# ════════════════════════════════════════════════════ 3. SECTIONS
S1 = [
    (1, "Mở màn danh sách từ menu Khởi tạo", "P0",
     "Tài khoản có ít nhất 1 phiếu nhìn thấy được.",
     "1. Đăng nhập, chọn phân hệ Tài chính.\n"
     "2. Bấm menu 'Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi'.\n"
     "3. Bấm 'Đề nghị thanh toán'.",
     "—",
     "- Tiêu đề trang là 'Phiếu đề nghị thanh toán'.\n"
     "- Có khối 'Bộ lọc danh sách' phía trên và bảng danh sách phía dưới.\n"
     "- Thanh công cụ có nút 'Tạo mới' và nút hình 2 cột (Cấu hình cột hiển thị)."),

    (2, "Mở màn danh sách từ menu Đề nghị", "P1",
     "Như trên.",
     "1. Bấm menu 'Đề nghị' > 'Đề nghị thanh toán'.",
     "—",
     "- Mở đúng màn 'Phiếu đề nghị thanh toán', nội dung y hệt lối vào ở menu Khởi tạo."),

    (3, "Mở chế độ Chờ duyệt từ menu", "P0",
     "Tài khoản giữ ít nhất 1 vai duyệt.",
     "1. Bấm menu 'Phê duyệt - Công nợ - Thu - Chi'.\n"
     "2. Bấm 'Phiếu đề nghị thanh toán chờ duyệt'.",
     "—",
     "- Tiêu đề trang đổi thành 'Phiếu đề nghị thanh toán chờ duyệt'.\n"
     "- Không có nút 'Tạo mới'.\n"
     "- Bộ cột và bộ tiêu chí lọc giống hệt chế độ Tất cả."),

    (4, "Mở chế độ Của tôi bằng đường dẫn", "P1",
     "Tài khoản đã lập ít nhất 1 phiếu, trong đó có 1 phiếu nháp.",
     "1. Gõ đường dẫn /finance/bill-payment-requests?mode=mine.",
     "—",
     "- Tiêu đề trang là 'Phiếu đề nghị thanh toán của tôi'.\n"
     "- Mọi dòng đều có cột Người lập là chính mình, gồm cả phiếu 'Đang tạo'.\n"
     "- Vẫn có nút 'Tạo mới'."),

    (5, "Mở chế độ Đã duyệt bằng đường dẫn", "P1",
     "Tài khoản đã duyệt ít nhất 1 phiếu.",
     "1. Gõ đường dẫn /finance/bill-payment-requests?mode=approved.",
     "—",
     "- Tiêu đề trang là 'Phiếu đề nghị thanh toán đã duyệt'.\n"
     "- Không có nút 'Tạo mới'."),

    (6, "Giá trị lạ ở tham số chế độ", "P2",
     "Tài khoản bất kỳ.",
     "1. Gõ đường dẫn /finance/bill-payment-requests?mode=abcxyz.",
     "—",
     "- Màn mở ở chế độ 'Tất cả', tiêu đề 'Phiếu đề nghị thanh toán', không báo lỗi."),

    (7, "Danh sách hiển thị đủ các cột mặc định", "P0",
     "Tài khoản chưa từng tuỳ chỉnh cột ở màn này.",
     "1. Mở màn Đề nghị thanh toán, cuộn ngang bảng từ trái sang phải.",
     "—",
     "- Có đủ các cột theo thứ tự: STT, Mã phiếu, Loại chi, Hình thức TT, "
     "Khách hàng / Nhà cung cấp, Lý do chi, Số tiền, Ngày lập, Ngày nhận, Người lập, Phòng ban, "
     "Người cập nhật, Ngày cập nhật, Trạng thái, Hành động."),

    (8, "Cột Mã phiếu là liên kết mở chi tiết", "P0",
     "Danh sách có ít nhất 1 phiếu.",
     "1. Bấm vào mã phiếu ở dòng đầu tiên.\n"
     "2. Quay lại, bấm chuột phải vào mã phiếu chọn mở ở tab mới.",
     "—",
     "- Bấm trái mở màn chi tiết đúng phiếu, tiêu đề 'Chi tiết phiếu đề nghị thanh toán: <mã>'.\n"
     "- Bấm phải mở được ở tab mới.\n"
     "- ⚠️ Cột Hành động KHÔNG có nút 'Xem chi tiết' riêng."),

    (9, "Màu và chữ của cột Trạng thái", "P1",
     "Có phiếu ở nhiều trạng thái khác nhau.",
     "1. Mở màn danh sách, đối chiếu từng dòng ở cột Trạng thái.",
     "—",
     "- Chỉ 'Duyệt phiếu chi' hiển thị nền xanh kèm dấu tích; 9 trạng thái còn lại nền đỏ kèm "
     "biểu tượng đồng hồ.\n"
     "- Chữ trong ô đúng nguyên văn 10 trạng thái."),

    (10, "Cột Số tiền hiển thị kèm mã loại tiền", "P0",
     "Có phiếu loại tiền VNĐ và phiếu loại tiền ngoại tệ.",
     "1. Đọc cột 'Số tiền' của các dòng.",
     "—",
     "- Số tiền canh phải, có dấu phẩy ngăn nghìn, kèm mã loại tiền phía sau (ví dụ VNĐ, USD).\n"
     "- ⚠️ Hiển thị MÃ loại tiền chứ không phải tên gọi đầy đủ."),

    (11, "Bảng rỗng khi bộ lọc không khớp phiếu nào", "P1",
     "Tài khoản có dữ liệu.",
     "1. Mở 'Tìm kiếm nâng cao', nhập 'Lý do chi' = 'ZZZZZZZZZ'.",
     "Lý do chi: ZZZZZZZZZ",
     "- Bảng hiện 'Không có dữ liệu phù hợp bộ lọc.', dòng đếm hiện tổng bằng 0."),
]

S2 = [
    (1, "Tìm nhanh theo mã phiếu — phải bấm nút Tìm kiếm", "P0",
     "Có phiếu mã TPE.DNTT0826.00016.",
     "1. Gõ 'DNTT0826' vào ô 'Tìm theo mã phiếu...'.\n"
     "2. Quan sát bảng trước khi bấm nút.\n"
     "3. Bấm nút 'Tìm kiếm'.",
     "Ô tìm nhanh: DNTT0826",
     "- ⚠️ Trước khi bấm nút danh sách KHÔNG đổi (đúng thiết kế).\n"
     "- Sau khi bấm: chỉ còn phiếu có mã chứa chuỗi đó, quay về trang 1."),

    (2, "Nút Làm mới xóa sạch mọi tiêu chí", "P0",
     "Đang lọc Loại chi = 'Chi trả nhà cung cấp', Trạng thái = 'Duyệt phiếu chi', ô tìm nhanh có "
     "nội dung.",
     "1. Bấm nút 'Làm mới'.",
     "—",
     "- Mọi ô lọc và ô tìm nhanh trở về trống.\n"
     "- Bảng tải lại toàn bộ danh sách của chế độ đang xem, về trang 1."),

    (3, "Lọc theo Loại chi", "P0",
     "Có phiếu ở cả 4 loại chi.",
     "1. Mở 'Tìm kiếm nâng cao', chọn Loại chi = 'Thanh toán chi phí vận chuyển NCC'.",
     "Loại chi: Thanh toán chi phí vận chuyển NCC",
     "- Danh sách tự lọc NGAY khi chọn, không cần bấm 'Tìm kiếm'.\n"
     "- Mọi dòng đều đúng loại chi đó.\n"
     "- ⚠️ Danh sách chọn chỉ có 4 giá trị."),

    (4, "Lọc theo Hình thức thanh toán", "P0",
     "Có phiếu cả tiền mặt và chuyển khoản.",
     "1. Chọn Hình thức thanh toán = 'CK'.",
     "Hình thức thanh toán: CK",
     "- Mọi dòng có cột 'Hình thức TT' bằng CK."),

    (5, "Lọc theo Trạng thái", "P0",
     "Có phiếu ở nhiều trạng thái.",
     "1. Chọn Trạng thái = 'Chờ kế toán công nợ duyệt'.\n"
     "2. Đổi sang 'Không duyệt'.",
     "Trạng thái: Chờ kế toán công nợ duyệt → Không duyệt",
     "- Mỗi lần chọn, danh sách chỉ còn phiếu đúng trạng thái đó.\n"
     "- Danh sách chọn có đủ 10 giá trị."),

    (6, "Lọc theo Lý do chi", "P0",
     "Có phiếu có lý do chi chứa chuỗi 'Thanh toán NCC'.",
     "1. Nhập 'Thanh toán NCC' vào ô 'Lý do chi'.",
     "Lý do chi: Thanh toán NCC",
     "- Chỉ còn phiếu có lý do chi chứa chuỗi này."),

    (7, "Lọc theo Khách hàng", "P0",
     "Có phiếu của khách hàng mã 29TPHPTH-1.",
     "1. Bấm ô 'Khách hàng', gõ 'ETEK GREEN' (từ 2 ký tự), chọn trong danh sách gợi ý.",
     "Khách hàng: ETEK GREEN",
     "- Danh sách gợi ý hiện dạng 'mã - tên'.\n"
     "- Sau khi chọn, chỉ còn phiếu gắn khách hàng đó (ở phiếu hoặc ở dòng chi tiết)."),

    (8, "Gõ tên nhà cung cấp vào ô lọc Khách hàng", "P1",
     "Nhà cung cấp 'CÔNG TY CỔ PHẦN CÔNG NGHỆ HỢP LONG' có nhiều phiếu.",
     "1. Bấm ô 'Khách hàng', gõ 'HỢP LONG'.",
     "Khách hàng: HỢP LONG",
     "- ⚠️ Danh sách gợi ý KHÔNG có kết quả — đây là đúng thiết kế: ô Khách hàng và ô Nhà cung "
     "cấp lấy từ hai danh sách khác nhau. Phải dùng ô 'Nhà cung cấp'."),

    (9, "Lọc theo Nhà cung cấp", "P0",
     "Có phiếu gắn nhà cung cấp 0104509916 - CÔNG TY CỔ PHẦN CÔNG NGHỆ HỢP LONG.",
     "1. Bấm ô 'Nhà cung cấp', gõ 'HỢP LONG', chọn trong danh sách gợi ý.",
     "Nhà cung cấp: HỢP LONG",
     "- Chỉ còn phiếu gắn nhà cung cấp đó.\n"
     "- ⚠️ Gõ dưới 2 ký tự thì chưa gợi ý gì."),

    (10, "Lọc theo Người lập", "P1",
     "Có phiếu của ít nhất 2 người lập trong phạm vi xem.",
     "1. Chọn một người ở ô 'Người lập'.",
     "Người lập: chọn 1 nhân sự",
     "- Cột Người lập của mọi dòng đều là người đã chọn."),

    (11, "Lọc theo khoảng Số tiền đề nghị", "P0",
     "Có phiếu tổng tiền 4,000,000 và phiếu tổng tiền 51,111,111,111.",
     "1. Nhập 'Số tiền đề nghị từ' = 10,000,000.\n"
     "2. Nhập 'Số tiền đề nghị đến' = 100,000,000,000.",
     "Từ 10.000.000 · đến 100.000.000.000",
     "- Phiếu 51,111,111,111 còn trong danh sách, phiếu 4,000,000 bị loại.\n"
     "- ⚠️ Ngưỡng so trên TỔNG tiền đề nghị quy đổi của cả phiếu, không phải từng dòng."),

    (12, "Lọc theo khoảng Ngày lập", "P0",
     "Có phiếu lập ngày 20/08/2026 và phiếu lập ngày 27/08/2026.",
     "1. Chọn 'Ngày lập từ' = 25/08/2026, 'Ngày lập đến' = 27/08/2026.",
     "Từ 25/08/2026 · đến 27/08/2026",
     "- Phiếu ngày 27/08/2026 CÒN trong kết quả (mốc 'đến' lấy trọn ngày).\n"
     "- Phiếu ngày 20/08/2026 bị loại."),

    (13, "Lọc theo Công ty / Phòng ban / Bộ phận", "P0",
     "Tài khoản có quyền xem tổng công ty; hệ thống có phiếu ở ít nhất 2 công ty.",
     "1. Chọn 'Công ty' = công ty 1.\n"
     "2. Chọn tiếp 'Phòng ban' = một phòng của công ty 1.\n"
     "3. Đổi 'Công ty' sang công ty khác.",
     "Công ty: công ty 1 → công ty khác",
     "- Ô Phòng ban chỉ liệt kê phòng của công ty đang chọn.\n"
     "- ⚠️ Đổi công ty thì ô Phòng ban và Bộ phận tự xóa giá trị, không lọc ngầm."),

    (14, "Kết hợp nhiều tiêu chí", "P0",
     "Có phiếu loại 'Chi trả nhà cung cấp', hình thức CK, trạng thái 'Duyệt phiếu chi'.",
     "1. Chọn Loại chi = Chi trả nhà cung cấp.\n"
     "2. Chọn Hình thức thanh toán = CK.\n"
     "3. Chọn Trạng thái = Duyệt phiếu chi.",
     "3 tiêu chí như bước thực hiện",
     "- Kết quả thỏa ĐỒNG THỜI cả 3 tiêu chí, số bản ghi giảm dần sau mỗi lần thêm tiêu chí."),

    (15, "Popup Cài đặt bộ lọc liệt kê đủ 10 tiêu chí", "P0",
     "Tài khoản bất kỳ.",
     "1. Bấm nút 'Cài đặt bộ lọc'.",
     "—",
     "- Popup liệt kê đúng 10 mục: Công ty – Phòng ban – Bộ phận, Loại chi, Hình thức thanh "
     "toán, Trạng thái, Lý do chi, Khách hàng, Nhà cung cấp, Người lập, Số tiền đề nghị "
     "(từ – đến), Khoảng ngày lập.\n"
     "- Có nút 'Lưu', 'Khôi phục mặc định', 'Đóng'."),

    (16, "Bỏ tích một tiêu chí thì tiêu chí đó biến mất", "P0",
     "Đang mở popup 'Cài đặt bộ lọc'.",
     "1. Bỏ tích 'Khoảng ngày lập'.\n2. Bấm 'Lưu'.\n3. Mở lại 'Tìm kiếm nâng cao'.",
     "Bỏ tích: Khoảng ngày lập",
     "- Thông báo cập nhật thành công.\n"
     "- Hai ô 'Ngày lập từ' và 'Ngày lập đến' không còn hiển thị.\n"
     "- ⚠️ Giá trị đang lọc của 2 ô đó cũng bị xóa."),

    (17, "Nút Khôi phục mặc định của Cài đặt bộ lọc", "P1",
     "Đang tắt bớt vài tiêu chí lọc.",
     "1. Mở 'Cài đặt bộ lọc', bấm 'Khôi phục mặc định', bấm 'Lưu'.",
     "—",
     "- Toàn bộ 10 tiêu chí được tích lại và hiện đủ ở bộ lọc nâng cao."),

    (18, "Bộ lọc lưu riêng cho từng chế độ xem", "P0",
     "Tài khoản giữ ít nhất 1 vai duyệt.",
     "1. Ở chế độ Tất cả, lọc Loại chi = 'Chi trả lại khách hàng'.\n"
     "2. Chuyển sang chế độ Chờ duyệt.\n"
     "3. Quay lại chế độ Tất cả.",
     "Loại chi: Chi trả lại khách hàng",
     "- ⚠️ Chế độ Chờ duyệt KHÔNG bị lọc theo tiêu chí vừa đặt ở chế độ Tất cả.\n"
     "- Quay lại chế độ Tất cả thì tiêu chí cũ vẫn còn (trong 10 phút)."),

    (19, "Hệ thống nhớ bộ lọc trong 10 phút", "P1",
     "Đang lọc Trạng thái = 'Duyệt phiếu chi'.",
     "1. Bấm vào một mã phiếu để vào chi tiết.\n2. Bấm 'Quay lại'.",
     "—",
     "- Về danh sách, ô Trạng thái vẫn giữ giá trị và danh sách vẫn đang lọc.\n"
     "- ⚠️ Ghi nhớ hết hiệu lực sau 10 phút; muốn bỏ ngay thì bấm 'Làm mới'."),

    (20, "Nhãn đối tượng đã chọn sau khi khôi phục bộ lọc", "P2",
     "Đang lọc theo Nhà cung cấp, vừa quay lại màn danh sách.",
     "1. Quan sát ô 'Nhà cung cấp' trong bộ lọc nâng cao.",
     "—",
     "- Danh sách vẫn đang lọc đúng nhà cung cấp đó.\n"
     "- ⚠️ Ô hiển thị có thể chưa hiện lại tên cho tới khi người dùng gõ tìm lại — bộ lọc vẫn "
     "chạy đúng, không phải lỗi mất dữ liệu."),
]

S3 = [
    (1, "Sắp xếp theo Mã phiếu", "P0",
     "Danh sách có từ 3 phiếu trở lên.",
     "1. Bấm tiêu đề cột 'Mã phiếu'.\n2. Bấm lần nữa.",
     "—",
     "- Lần 1 sắp xếp theo mã phiếu, lần 2 đảo chiều; mỗi lần quay về trang 1."),

    (2, "Sắp xếp theo Khách hàng / Nhà cung cấp", "P0",
     "Danh sách có phiếu nhiều loại chi và cả 2 hình thức thanh toán.",
     "1. Bấm tiêu đề cột 'Khách hàng / Nhà cung cấp' 2 lần.",
     "—",
     "- Thứ tự dòng đổi đúng theo NỘI DUNG đang hiển thị ở cột đó.\n"
     "- ⚠️ Dòng có ô này trống dồn lên đầu khi sắp xếp tăng dần — đúng thiết kế.\n"
     "- Danh sách trả về trong vài giây, không treo trang."),

    (3, "Sắp xếp theo Ngày lập và Ngày cập nhật", "P0",
     "Có phiếu lập ở nhiều ngày khác nhau.",
     "1. Bấm tiêu đề cột 'Ngày lập' 2 lần.\n2. Bấm tiêu đề cột 'Ngày cập nhật' 2 lần.",
     "—",
     "- Thứ tự dòng đảo đúng theo từng cột; giá trị hiển thị dạng ngày/tháng/năm giờ:phút."),

    (4, "Sắp xếp theo Trạng thái", "P1",
     "Có phiếu ở nhiều trạng thái.",
     "1. Bấm tiêu đề cột 'Trạng thái' 2 lần.",
     "—",
     "- Thứ tự dòng thay đổi theo trạng thái (không phải theo bảng chữ cái của nhãn).\n"
     "- ⚠️ Cột này TRƯỚC ĐÂY bấm không ăn — nay phải đổi thứ tự thật."),

    (5, "Cột không hỗ trợ sắp xếp", "P2",
     "Danh sách có dữ liệu.",
     "1. Bấm tiêu đề cột 'Loại chi', 'Hình thức TT', 'Lý do chi', 'Số tiền', 'Ngày nhận', "
     "'Người lập', 'Phòng ban'.",
     "—",
     "- Các cột này không có biểu tượng sắp xếp, thứ tự dòng không đổi."),

    (6, "Mặc định sắp xếp phiếu mới nhất lên đầu", "P0",
     "Chưa bấm sắp xếp cột nào.",
     "1. Mở màn danh sách lần đầu, so cột Ngày lập của dòng 1 và dòng cuối trang.",
     "—",
     "- Dòng đầu là phiếu lập gần nhất."),

    (7, "Chuyển trang", "P0",
     "Danh sách có trên 10 phiếu.",
     "1. Bấm số trang 2.\n2. Bấm nút chuyển tới trang cuối.",
     "—",
     "- Nội dung bảng đổi theo trang, số thứ tự chạy liên tục (trang 2 bắt đầu từ 11).\n"
     "- ⚠️ Chuyển trang KHÔNG làm mất tiêu chí lọc."),

    (8, "Đổi số dòng mỗi trang", "P0",
     "Danh sách có trên 20 phiếu.",
     "1. Đổi 'Số dòng/trang' sang 20.",
     "Số dòng/trang: 20",
     "- Bảng hiện 20 dòng, quay về trang 1, dòng đếm cập nhật đúng."),

    (9, "Popup Tuỳ chỉnh cột — cột bắt buộc bị khóa", "P0",
     "Tài khoản bất kỳ.",
     "1. Bấm nút hình 2 cột trên thanh công cụ.\n"
     "2. Thử bỏ tích 'STT', 'Mã phiếu', 'Hành động'.",
     "—",
     "- Popup có tiêu đề 'Tuỳ chỉnh cột'.\n"
     "- 3 cột trên bị xám, có biểu tượng ổ khóa và không bỏ tích được."),

    (10, "Ẩn một cột rồi lưu", "P0",
     "Đang mở popup 'Tuỳ chỉnh cột'.",
     "1. Bỏ tích cột 'Ngày nhận'.\n2. Bấm 'Lưu'.\n3. Tải lại trang.",
     "Bỏ tích: Ngày nhận",
     "- Cột 'Ngày nhận' biến mất khỏi bảng; tải lại trang vẫn giữ cấu hình."),

    (11, "Cấu hình cột dùng chung cho cả 4 chế độ", "P0",
     "Vừa ẩn cột 'Ngày nhận' ở chế độ Tất cả.",
     "1. Chuyển sang chế độ Chờ duyệt, rồi Của tôi, rồi Đã duyệt.",
     "—",
     "- ⚠️ Cả 4 chế độ đều không hiện cột 'Ngày nhận' (dùng chung một bộ cột)."),

    (12, "Cấu hình cột lưu riêng theo tài khoản", "P1",
     "Tài khoản A đã ẩn cột 'Ngày cập nhật'.",
     "1. Đăng nhập tài khoản B, mở màn Đề nghị thanh toán.",
     "—",
     "- Tài khoản B vẫn thấy đầy đủ cột theo mặc định."),
]

S4 = [
    (1, "Mở form Tạo mới và kiểm tra giá trị mặc định", "P0",
     "Tài khoản bất kỳ vào được màn danh sách.",
     "1. Bấm nút 'Tạo mới'.\n2. Đọc từng ô trên khối 'Thông tin chung'.",
     "—",
     "- Tiêu đề trang 'Thêm phiếu đề nghị thanh toán'.\n"
     "- Loại chi điền sẵn 'Chi trả nhà cung cấp'; Hình thức thanh toán điền sẵn 'TM'; Loại tiền "
     "'VNĐ — VietNamDong'; Tỷ giá (VND) = 1 và bị khóa.\n"
     "- Người tạo và Phòng ban điền sẵn theo người đang đăng nhập, chỉ để xem.\n"
     "- Lý do chi để trống.\n"
     "- ⚠️ KHÔNG có ô 'Mã phiếu' (sinh tự động khi lưu) và KHÔNG có khối 'Thông tin ngân hàng' "
     "(chỉ hiện với hình thức chuyển khoản).\n"
     "- Thanh nút: 'Lưu nháp', 'Lưu và gửi duyệt', 'Quay lại'."),

    (2, "Đổi Loại tiền sang ngoại tệ", "P0",
     "Đang mở form Tạo mới, Loại tiền đang là VNĐ.",
     "1. Đổi 'Loại tiền' sang USD.",
     "Loại tiền: USD",
     "- Ô 'Tỷ giá (VND)' mở khóa và tự điền tỷ giá của loại tiền đó.\n"
     "- Bảng chi tiết tách cột 'Số tiền đề nghị chi' thành 2 cột con: USD và VND."),

    (3, "Đổi lại Loại tiền về VNĐ", "P1",
     "Đang chọn ngoại tệ, tỷ giá khác 1.",
     "1. Đổi 'Loại tiền' về 'VNĐ — VietNamDong'.",
     "Loại tiền: VNĐ",
     "- Tỷ giá tự về 1 và ô bị khóa lại; bảng chi tiết bỏ cột quy đổi."),

    (4, "Đổi Hình thức thanh toán sang chuyển khoản", "P0",
     "Loại chi = 'Chi trả nhà cung cấp', hình thức đang là TM.",
     "1. Đổi 'Hình thức thanh toán' sang 'CK'.",
     "Hình thức thanh toán: CK",
     "- Khối 'Thông tin chung' hiện thêm ô bắt buộc 'Nhà cung cấp'.\n"
     "- Xuất hiện khối 'Thông tin ngân hàng'.\n"
     "- ⚠️ Bảng chi tiết BỎ cột 'Nhà cung cấp' theo dòng (đối tượng chọn 1 lần cho cả phiếu)."),

    (5, "Đổi Hình thức thanh toán về tiền mặt", "P0",
     "Đang ở hình thức CK và đã chọn nhà cung cấp.",
     "1. Đổi 'Hình thức thanh toán' về 'TM'.",
     "Hình thức thanh toán: TM",
     "- Khối 'Thông tin ngân hàng' biến mất, ô 'Nhà cung cấp' ở Thông tin chung biến mất.\n"
     "- Bảng chi tiết hiện lại cột 'Nhà cung cấp' theo dòng."),

    (6, "Hộp xác nhận khi đổi Loại chi lúc đã có dòng chi tiết", "P0",
     "Bảng chi tiết đang có 1 dòng đã chọn hợp đồng.",
     "1. Đổi ô 'Loại chi' sang loại khác.",
     "Loại chi: Thanh toán chi phí vận chuyển NCC",
     "- Hộp thoại 'Đổi loại chi' hiện với nội dung 'Đổi loại chi sẽ xóa toàn bộ dòng chi tiết và "
     "thông tin đối tượng đã chọn. Bạn có chắc chắn?' cùng 2 nút 'Xác nhận' và 'Hủy'."),

    (7, "Xác nhận đổi Loại chi", "P0",
     "Đang hiện hộp thoại 'Đổi loại chi'.",
     "1. Bấm 'Xác nhận'.",
     "—",
     "- Toàn bộ dòng chi tiết bị xóa, ô đối tượng đã chọn cũng bị xóa.\n"
     "- Tiêu đề cột của bảng chi tiết đổi theo loại chi mới."),

    (8, "Hủy hộp thoại đổi Loại chi", "P1",
     "Đang hiện hộp thoại 'Đổi loại chi'.",
     "1. Bấm 'Hủy'.",
     "—",
     "- Hộp thoại đóng, các dòng chi tiết đã chọn vẫn còn nguyên."),

    (9, "Loại chi vận chuyển hiện thêm ô Đến ngày", "P0",
     "Đang mở form Tạo mới.",
     "1. Chọn Loại chi = 'Thanh toán chi phí vận chuyển NCC'.",
     "Loại chi: Thanh toán chi phí vận chuyển NCC",
     "- Khối Thông tin chung hiện thêm ô bắt buộc 'Đến ngày' (chọn ngày).\n"
     "- Hiện ô bắt buộc 'Nhà cung cấp' kể cả khi hình thức là tiền mặt.\n"
     "- Bảng chi tiết đổi cột: Số chuyến xe, Hạch toán, Tổng cước, Đã thanh toán, Số tiền còn "
     "lại, Số tiền đề nghị chi; có thêm cột ô tích chọn ở đầu bảng và nút 'Lấy dữ liệu'."),

    (10, "Loại chi thưởng hợp đồng không có ô đối tượng", "P1",
     "Đang mở form Tạo mới.",
     "1. Chọn Loại chi = 'Chi thưởng thực hiện hợp đồng', hình thức 'TM'.",
     "Loại chi: Chi thưởng thực hiện hợp đồng",
     "- ⚠️ Bảng chi tiết KHÔNG có cột đối tượng, chỉ có 'Số đơn hàng/Hợp đồng'.\n"
     "- Cột công nợ có nhãn 'Số tiền còn lại'.\n"
     "- Khối 'File đính kèm' KHÔNG có dấu sao đỏ (không bắt buộc)."),

    (11, "Nhãn cột theo từng loại chi", "P0",
     "Đang mở form Tạo mới, hình thức TM.",
     "1. Lần lượt chọn 4 loại chi và đọc tiêu đề cột của bảng Chi tiết.",
     "4 loại chi",
     "- Chi trả nhà cung cấp: 'Nhà cung cấp' + 'Số hợp đồng nhập mua' + cột công nợ.\n"
     "- Chi trả lại khách hàng: 'Khách hàng' + 'Hợp đồng' + 'Công nợ còn lại'.\n"
     "- Chi thưởng thực hiện hợp đồng: 'Số đơn hàng/Hợp đồng' + 'Số tiền còn lại'.\n"
     "- Thanh toán chi phí vận chuyển NCC: nhóm cột chuyến xe như trường hợp trên."),

    (12, "Cảnh báo chưa lưu khi rời form", "P0",
     "Đang mở form Tạo mới và đã nhập Lý do chi.",
     "1. Bấm 'Quay lại'.",
     "—",
     "- Hộp thoại 'Thông tin chưa lưu' hiện với 2 nút 'Thoát' và 'Ở lại'.\n"
     "- Bấm 'Ở lại': vẫn ở form, dữ liệu còn nguyên.\n"
     "- Bấm 'Thoát': về danh sách và KHÔNG có phiếu mới nào được tạo."),

    (13, "Không cảnh báo khi chưa nhập gì", "P1",
     "Vừa mở form Tạo mới, chưa chạm vào ô nào.",
     "1. Bấm 'Quay lại'.",
     "—",
     "- Về thẳng danh sách, không hiện hộp thoại 'Thông tin chưa lưu'."),
]

S5 = [
    (1, "Thêm một dòng chi tiết", "P0",
     "Đang mở form Tạo mới, Loại chi = 'Chi trả nhà cung cấp', hình thức 'TM'.",
     "1. Bấm dấu cộng ở góc phải tiêu đề bảng Chi tiết.",
     "—",
     "- Bảng có 1 dòng trống, số thứ tự 1.\n"
     "- Ô nhà cung cấp hiện gợi ý 'Nhấn vào đây để chọn nhà cung cấp'.\n"
     "- Ô hợp đồng bị khóa với gợi ý 'Chọn nhà cung cấp trước'.\n"
     "- Dòng 'Tổng cộng' xuất hiện với giá trị 0."),

    (2, "Chọn nhà cung cấp cho dòng", "P0",
     "Đang có 1 dòng chi tiết trống.",
     "1. Bấm vào ô nhà cung cấp của dòng 1.\n"
     "2. Gõ 'HỢP LONG' vào ô tìm, bấm 'Tìm kiếm', bấm vào dòng kết quả.",
     "Mã / Tên nhà cung cấp: HỢP LONG",
     "- Cửa sổ 'Chọn nhà cung cấp' mở với bảng 3 cột STT, Mã nhà cung cấp, Tên nhà cung cấp.\n"
     "- Chọn xong cửa sổ tự đóng, ô hiện 'mã - tên', ô hợp đồng mở khóa."),

    (3, "Cửa sổ chọn hợp đồng mua", "P0",
     "Dòng 1 đã chọn nhà cung cấp.",
     "1. Bấm vào ô 'Số hợp đồng nhập mua' của dòng 1.",
     "—",
     "- Cửa sổ tiêu đề 'Chọn hợp đồng mua', dòng phụ hiện đúng nhà cung cấp đã chọn.\n"
     "- Bảng có cột: STT, Số đơn hàng/Hợp đồng, Ngày lập, Giá trị hợp đồng, Số tiền còn nợ.\n"
     "- Có ô tìm 'Số đơn hàng/Hợp đồng', nút 'Tìm kiếm', 'Làm mới', 'Đóng' và phân trang."),

    (4, "Chọn hợp đồng — tự điền công nợ", "P0",
     "Đang mở cửa sổ hợp đồng mua.",
     "1. Bấm vào một dòng hợp đồng.",
     "—",
     "- Cửa sổ tự đóng, ô hợp đồng hiện số hợp đồng.\n"
     "- Cột công nợ của dòng được điền theo sổ kế toán.\n"
     "- Dòng 'Tổng cộng' cập nhật theo."),

    (5, "Không cho chọn trùng hợp đồng trong cùng phiếu", "P0",
     "Dòng 1 đã chọn hợp đồng X. Đã thêm dòng 2 và chọn cùng nhà cung cấp.",
     "1. Ở dòng 2, mở cửa sổ hợp đồng và bấm vào hợp đồng X.",
     "—",
     "- Dòng hợp đồng X hiển thị khác biệt kèm chú thích hợp đồng đã có trong phiếu.\n"
     "- Bấm vào không chọn được, ô hợp đồng của dòng 2 vẫn trống."),

    (6, "Cửa sổ hợp đồng của loại Chi trả lại khách hàng", "P0",
     "Loại chi = 'Chi trả lại khách hàng', hình thức TM, dòng 1 đã chọn khách hàng.",
     "1. Bấm vào ô 'Hợp đồng' của dòng 1.",
     "—",
     "- Cửa sổ chỉ liệt kê hợp đồng BÁN của khách hàng đó.\n"
     "- ⚠️ Không có hợp đồng mua nào trong danh sách."),

    (7, "Cửa sổ hợp đồng của loại Chi thưởng thực hiện hợp đồng", "P0",
     "Loại chi = 'Chi thưởng thực hiện hợp đồng'. Người lập được hưởng thưởng ở ít nhất 1 hợp "
     "đồng.",
     "1. Thêm 1 dòng chi tiết.\n2. Bấm vào ô 'Số đơn hàng/Hợp đồng'.",
     "—",
     "- ⚠️ Cửa sổ mở NGAY dù chưa chọn đối tượng nào (loại này không chọn khách hàng trước).\n"
     "- Cửa sổ có thêm ô lọc 'Khách hàng' và cột 'Khách hàng' trong bảng.\n"
     "- Danh sách chỉ gồm hợp đồng mà người lập được hưởng thưởng."),

    (8, "Nhập Số tiền đề nghị chi", "P0",
     "Dòng 1 đã có đối tượng và hợp đồng.",
     "1. Nhập 5,000,000 vào ô 'Số tiền đề nghị chi'.",
     "Số tiền đề nghị chi: 5.000.000",
     "- Ô hiển thị 5,000,000 với dấu phẩy ngăn nghìn.\n"
     "- Dòng 'Tổng cộng' cập nhật ngay."),

    (9, "Quy đổi VND theo tỷ giá", "P0",
     "Loại tiền USD, tỷ giá 25,000; dòng 1 đã đủ dữ liệu.",
     "1. Nhập Số tiền đề nghị chi = 100.",
     "Số tiền: 100 · Tỷ giá: 25.000",
     "- Cột VND của dòng hiện 2,500,000; dòng Tổng cộng cột VND cũng là 2,500,000."),

    (10, "Xóa một dòng chi tiết", "P0",
     "Bảng chi tiết đang có 2 dòng.",
     "1. Bấm biểu tượng thùng rác ở cuối dòng 1.",
     "—",
     "- Dòng 1 biến mất, dòng còn lại được đánh số lại thành 1.\n"
     "- Dòng 'Tổng cộng' tính lại đúng."),

    (11, "Nhiều dòng, nhiều đối tượng trong một phiếu tiền mặt", "P0",
     "Loại chi 'Chi trả nhà cung cấp', hình thức TM.",
     "1. Thêm dòng 1: nhà cung cấp X + hợp đồng của X + 5,000,000.\n"
     "2. Thêm dòng 2: nhà cung cấp Y (khác X) + hợp đồng của Y + 3,000,000.",
     "Dòng 1: 5.000.000 · Dòng 2: 3.000.000",
     "- Hai dòng giữ 2 nhà cung cấp khác nhau; cửa sổ hợp đồng của mỗi dòng lọc theo đúng đối "
     "tượng của dòng đó.\n"
     "- Tổng cộng = 8,000,000."),

    (12, "Đổi đối tượng của dòng đã chọn hợp đồng", "P0",
     "Dòng 1 đã chọn nhà cung cấp X và hợp đồng của X.",
     "1. Bấm lại vào ô nhà cung cấp dòng 1, chọn nhà cung cấp Y.",
     "Nhà cung cấp mới: Y",
     "- ⚠️ Ô hợp đồng của dòng bị XÓA TRẮNG, công nợ về 0.\n"
     "- Mở cửa sổ hợp đồng lần nữa thì danh sách là hợp đồng của Y."),

    (13, "Loại vận chuyển — Lấy dữ liệu khi thiếu điều kiện", "P0",
     "Loại chi 'Thanh toán chi phí vận chuyển NCC', chưa chọn nhà cung cấp và chưa chọn Đến ngày.",
     "1. Bấm nút 'Lấy dữ liệu'.",
     "—",
     "- Hệ thống báo phải chọn nhà cung cấp trước (hoặc chọn Đến ngày trước), không sinh dòng nào."),

    (14, "Loại vận chuyển — Lấy dữ liệu thành công", "P0",
     "Loại chi 'Thanh toán chi phí vận chuyển NCC'. Nhà cung cấp Z có 5 chuyến xe phát sinh "
     "trước ngày 25/08/2026.",
     "1. Chọn nhà cung cấp Z, chọn 'Đến ngày' = 25/08/2026.\n"
     "2. Bấm 'Lấy dữ liệu'.",
     "Nhà cung cấp Z · Đến ngày 25/08/2026",
     "- Bảng sinh ra 5 dòng, mỗi dòng có Số chuyến xe, Tổng cước, Đã thanh toán, Số tiền còn lại.\n"
     "- ⚠️ KHÔNG thêm / xóa dòng bằng tay được ở loại chi này (không có nút dấu cộng và nút "
     "thùng rác)."),

    (15, "Loại vận chuyển — tích chọn dòng cần thanh toán", "P0",
     "Bảng đã có 5 dòng chuyến xe.",
     "1. Bỏ tích ô ở đầu 3 dòng, chỉ để 2 dòng được tích.\n"
     "2. Nhập số tiền cho 2 dòng còn tích.\n"
     "3. Bấm 'Lưu và gửi duyệt' rồi xác nhận.",
     "2 dòng có tích, mỗi dòng 1.000.000",
     "- ⚠️ Chỉ dòng ĐƯỢC TÍCH mới bắt buộc nhập số tiền; 3 dòng không tích để trống vẫn lưu được.\n"
     "- Phiếu lưu thành công."),

    (16, "Loại vận chuyển — tích / bỏ tích tất cả", "P1",
     "Bảng đã có 5 dòng chuyến xe.",
     "1. Bấm ô tích ở HÀNG TIÊU ĐỀ để bỏ tích tất cả.\n2. Bấm lại để tích tất cả.",
     "—",
     "- Lần 1: cả 5 dòng bỏ tích. Lần 2: cả 5 dòng được tích."),

    (17, "Loại vận chuyển — mở chi tiết chuyến xe", "P1",
     "Bảng đã có dòng chuyến xe kèm mã hạch toán.",
     "1. Bấm vào mã ở cột 'Hạch toán' của một dòng.",
     "—",
     "- Cửa sổ 'Chi tiết chuyến xe' mở ra với đầy đủ thông tin chuyến xe (13 cột).\n"
     "- Bấm Đóng thì về lại form, dữ liệu không đổi."),
]

S6 = [
    (1, "Khối ngân hàng tự điền theo đối tượng trong nước", "P0",
     "Loại chi 'Chi trả nhà cung cấp', hình thức CK. Nhà cung cấp HỢP LONG có khai tài khoản "
     "ngân hàng trong hồ sơ.",
     "1. Chọn nhà cung cấp HỢP LONG ở ô 'Nhà cung cấp'.\n"
     "2. Đọc khối 'Thông tin ngân hàng'.",
     "Nhà cung cấp: HỢP LONG",
     "- Năm ô tự điền: Số tài khoản, Tên tài khoản, Tên ngân hàng, Chi nhánh, Thành phố.\n"
     "- ⚠️ Cả 5 ô đều CHỈ ĐỌC, người dùng không gõ tay được."),

    (2, "Đối tượng chưa khai tài khoản ngân hàng", "P0",
     "Chọn một nhà cung cấp CHƯA khai tài khoản ngân hàng trong hồ sơ.",
     "1. Chọn nhà cung cấp đó ở ô 'Nhà cung cấp'.",
     "—",
     "- Khối ngân hàng để trống và hiện dòng chữ đỏ hướng dẫn: đối tượng nhận tiền chưa khai tài "
     "khoản ngân hàng, cập nhật ở màn Khách hàng / Nhà cung cấp rồi chọn lại.\n"
     "- ⚠️ Vẫn LƯU NHÁP được; chỉ khi gửi duyệt mới bị chặn."),

    (3, "Đối tượng có nhiều tài khoản ngân hàng", "P1",
     "Chọn một nhà cung cấp có từ 2 tài khoản ngân hàng trở lên.",
     "1. Chọn nhà cung cấp đó.\n2. Mở ô 'Tài khoản ngân hàng'.",
     "—",
     "- Có ô chọn 'Tài khoản ngân hàng' liệt kê các tài khoản.\n"
     "- Đổi tài khoản thì 5 ô bên dưới đổi theo."),

    (4, "Nhà cung cấp nước ngoài — khối ngân hàng khác hẳn", "P0",
     "Loại chi 'Chi trả nhà cung cấp', hình thức CK, chọn nhà cung cấp NƯỚC NGOÀI.",
     "1. Chọn nhà cung cấp nước ngoài.\n2. Đọc khối 'Thông tin ngân hàng'.",
     "—",
     "- Khối hiện ô chọn 'Ngân hàng' (bắt buộc), 'Ngân hàng trung gian', và các ô Số tài khoản, "
     "Tài khoản, Tên ngân hàng, Swift Code, IBAN Number, Địa chỉ — kèm bộ ô tương ứng cho ngân "
     "hàng trung gian.\n"
     "- Có ô chọn 'Phí' (bắt buộc) với 3 giá trị: Phí do người chuyển tiền chịu, Phí do người "
     "hưởng chịu, Phí chia sẻ cho 2 bên."),

    (5, "Loại chi thưởng + chuyển khoản tự lấy ngân hàng người lập", "P0",
     "Loại chi 'Chi thưởng thực hiện hợp đồng', hình thức CK. Người lập có khai tài khoản ngân "
     "hàng trong hồ sơ nhân sự.",
     "1. Chọn loại chi và hình thức như trên.",
     "—",
     "- ⚠️ Khối ngân hàng tự điền theo tài khoản của CHÍNH NGƯỜI LẬP, không có ô chọn đối tượng "
     "(người nhận thưởng luôn là người lập)."),

    (6, "Gửi duyệt khi khối ngân hàng còn trống", "P0",
     "Hình thức CK, đối tượng chưa khai tài khoản ngân hàng, đã nhập đủ Lý do chi và 1 dòng chi "
     "tiết hợp lệ.",
     "1. Bấm 'Lưu và gửi duyệt' rồi xác nhận.",
     "—",
     "- Hệ thống báo lỗi 'Bắt buộc nhập' tại các ô Số tài khoản, Tên tài khoản, Tên ngân hàng.\n"
     "- Phiếu không được lưu."),

    (7, "Lưu nháp không bắt buộc khối ngân hàng", "P0",
     "Như trên.",
     "1. Bấm 'Lưu nháp'.",
     "—",
     "- ⚠️ Lưu thành công, phiếu ở trạng thái 'Đang tạo' dù khối ngân hàng còn trống."),
]

S7 = [
    (1, "Khối File đính kèm ở loại Chi trả nhà cung cấp", "P0",
     "Đang mở form Tạo mới, Loại chi = 'Chi trả nhà cung cấp'.",
     "1. Cuộn xuống khối 'File đính kèm'.",
     "—",
     "- Tiêu đề khối có dấu sao đỏ (bắt buộc).\n"
     "- Có nút 'Thêm tài liệu'; bảng có các cột STT, UPLOAD / FILE, DUNG LƯỢNG."),

    (2, "Khối File đính kèm ở 3 loại chi còn lại", "P1",
     "Đang mở form Tạo mới.",
     "1. Lần lượt chọn 3 loại chi còn lại và đọc tiêu đề khối 'File đính kèm'.",
     "—",
     "- ⚠️ Không có dấu sao đỏ — 3 loại này không bắt buộc đính kèm file."),

    (3, "Thêm dòng và chọn tệp", "P0",
     "Đang mở form Tạo mới.",
     "1. Bấm 'Thêm tài liệu'.\n2. Bấm nút 'Chọn tệp' của dòng vừa thêm, chọn 1 file PDF 1MB.",
     "File: hop-dong.pdf (1MB)",
     "- Trong lúc tải lên hiện dòng chữ đang tải kèm vòng quay.\n"
     "- Tải xong dòng hiện tên file, dung lượng, và 3 nút: Xem trước, Tải xuống, Thay đổi.\n"
     "- ⚠️ File được tải lên NGAY khi chọn, không chờ tới lúc lưu phiếu."),

    (4, "Xem trước file đính kèm", "P1",
     "Dòng file đã có file PDF.",
     "1. Bấm nút Xem trước (biểu tượng con mắt).",
     "—",
     "- Cửa sổ xem trước mở và hiển thị nội dung file."),

    (5, "Tải xuống file đính kèm", "P2",
     "Dòng file đã có file.",
     "1. Bấm nút Tải xuống.",
     "—",
     "- Trình duyệt tải file về, tên file đúng như hiển thị."),

    (6, "Thay đổi file chưa lưu", "P1",
     "Dòng file vừa tải lên, phiếu CHƯA lưu.",
     "1. Bấm nút Thay đổi, chọn file khác.",
     "File mới: bien-ban.pdf",
     "- Dòng đổi sang file mới.\n"
     "- ⚠️ Nút Thay đổi CHỈ có ở file chưa gắn vào phiếu; file đã lưu thì phải xóa rồi thêm lại."),

    (7, "Xóa một dòng file", "P0",
     "Dòng file đã có file.",
     "1. Bấm nút Xóa (thùng rác) ở cuối dòng.\n2. Đọc hộp thoại và bấm nút xác nhận.",
     "—",
     "- Hộp thoại 'Xác nhận xóa' hỏi 'Bạn có chắc muốn xóa file đính kèm này?'.\n"
     "- Xác nhận thì dòng file biến mất."),

    (8, "Chọn file sai định dạng", "P0",
     "Đang ở dòng file trống.",
     "1. Bấm 'Chọn tệp', chọn 1 file đuôi .exe.",
     "File: virus.exe",
     "- Hệ thống báo chỉ nhận file pdf, png, jpg, jpeg, doc, docx, xls, xlsx, zip.\n"
     "- File không được tải lên."),

    (9, "Chọn file quá dung lượng", "P1",
     "Đang ở dòng file trống.",
     "1. Bấm 'Chọn tệp', chọn 1 file PDF dung lượng 25MB.",
     "File: tai-lieu-lon.pdf (25MB)",
     "- Hệ thống báo dung lượng tối đa 20MB, file không được tải lên."),

    (10, "Gửi duyệt loại Chi trả nhà cung cấp mà chưa có file", "P0",
     "Loại chi 'Chi trả nhà cung cấp', đã nhập đủ Lý do chi và 1 dòng chi tiết, chưa chọn file.",
     "1. Bấm 'Lưu và gửi duyệt' rồi xác nhận.",
     "—",
     "- Khối File đính kèm viền đỏ, hiện lỗi 'Bắt buộc đính kèm ít nhất 1 file'.\n"
     "- Phiếu không được lưu."),

    (11, "Lưu nháp không bắt buộc file", "P0",
     "Như trên.",
     "1. Bấm 'Lưu nháp'.",
     "—",
     "- ⚠️ Lưu thành công, phiếu ở trạng thái 'Đang tạo' dù chưa có file nào."),

    (12, "File đính kèm ở màn xem chi tiết", "P1",
     "Phiếu đã lưu có 1 file đính kèm.",
     "1. Mở màn chi tiết phiếu, cuộn tới khối 'File đính kèm'.",
     "—",
     "- Hiện tên file và dung lượng, có nút Xem trước và Tải xuống.\n"
     "- ⚠️ Không có nút 'Thêm tài liệu' và nút Xóa (màn xem chỉ đọc)."),
]

S8 = [
    (1, "Lưu nháp với dữ liệu tối thiểu", "P0",
     "Đang mở form Tạo mới, chỉ nhập Lý do chi, chưa có dòng chi tiết, chưa có file.",
     "1. Nhập Lý do chi = 'Tạm lưu phiếu'.\n2. Bấm 'Lưu nháp'.",
     "Lý do chi: Tạm lưu phiếu",
     "- ⚠️ Lưu thành công, hệ thống báo 'Lưu phiếu đề nghị thanh toán thành công!'.\n"
     "- Quay về danh sách, phiếu mới ở trạng thái 'Đang tạo'.\n"
     "- Mã phiếu tự sinh theo dạng <mã công ty>.DNTT<tháng năm>.<5 chữ số>."),

    (2, "Lưu nháp khi bỏ trống Lý do chi", "P0",
     "Đang mở form Tạo mới, chưa nhập gì.",
     "1. Bấm 'Lưu nháp'.",
     "—",
     "- ⚠️ Ô Lý do chi viền đỏ, hiện 'Bắt buộc nhập' — Lý do chi bắt buộc ở CẢ hai nút lưu.\n"
     "- Phiếu không được tạo."),

    (3, "Hộp xác nhận khi bấm Lưu và gửi duyệt", "P0",
     "Form đã nhập đủ dữ liệu hợp lệ.",
     "1. Bấm 'Lưu và gửi duyệt'.",
     "—",
     "- Hộp thoại 'Xác nhận lưu và gửi duyệt' hiện với 2 nút 'Xác nhận' và 'Hủy'.\n"
     "- Bấm 'Hủy' thì không lưu gì, vẫn ở lại form."),

    (4, "Lưu và gửi duyệt thành công", "P0",
     "Như trên, đang mở hộp xác nhận.",
     "1. Bấm 'Xác nhận'.",
     "—",
     "- Hệ thống báo 'Gửi duyệt phiếu đề nghị thanh toán thành công!'.\n"
     "- Về danh sách, phiếu mới ở trạng thái 'Chờ TP duyệt'.\n"
     "- ⚠️ Thông báo khác với khi lưu nháp — đừng nhầm 2 câu."),

    (5, "Gửi duyệt bắn thông báo cho trưởng phòng", "P0",
     "Người lập thuộc phòng Kinh doanh 1, công ty 1. Tài khoản F có quyền Trưởng phòng duyệt và "
     "quản lý phòng Kinh doanh 1. Tài khoản M có quyền Trưởng phòng duyệt nhưng thuộc công ty 4.",
     "1. Lập phiếu và bấm 'Lưu và gửi duyệt'.\n"
     "2. Đăng nhập tài khoản F, mở chuông thông báo.\n"
     "3. Đăng nhập tài khoản M, mở chuông thông báo.",
     "—",
     "- Tài khoản F nhận thông báo mở đầu bằng dấu hiệu riêng của phiếu chi, kèm mã phiếu; bấm "
     "vào mở đúng phiếu.\n"
     "- ⚠️ Tài khoản M (công ty khác) KHÔNG nhận thông báo."),

    (6, "Gửi duyệt khi thiếu Lý do chi và dòng chi tiết", "P0",
     "Form trống hoàn toàn.",
     "1. Bấm 'Lưu và gửi duyệt' rồi 'Xác nhận'.",
     "—",
     "- Ô 'Lý do chi' viền đỏ với 'Bắt buộc nhập'.\n"
     "- Dưới bảng Chi tiết hiện 'Bắt buộc nhập'.\n"
     "- ⚠️ Không có phiếu nào được tạo, vẫn ở lại form."),

    (7, "Gửi duyệt khi dòng chi tiết chưa chọn đối tượng", "P0",
     "Đã nhập Lý do chi, có 1 dòng chi tiết trống hoàn toàn, hình thức TM.",
     "1. Bấm 'Lưu và gửi duyệt' rồi 'Xác nhận'.",
     "—",
     "- Ô đối tượng của dòng viền đỏ kèm 'Bắt buộc nhập'.\n"
     "- Ô hợp đồng của dòng cũng báo 'Bắt buộc nhập'."),

    (8, "Số tiền đề nghị chi bằng 0", "P0",
     "Dòng chi tiết đã đủ đối tượng và hợp đồng, số tiền để 0.",
     "1. Bấm 'Lưu và gửi duyệt' rồi 'Xác nhận'.",
     "Số tiền đề nghị chi: 0",
     "- ⚠️ Báo lỗi 'Không được nhỏ hơn 1' ngay dưới ô số tiền — khác màn Đề nghị thu tiền "
     "(bên đó cho phép 0).\n"
     "- Phiếu không được lưu."),

    (9, "Tỷ giá bằng 0", "P0",
     "Loại tiền là ngoại tệ.",
     "1. Xóa tỷ giá và nhập 0.\n2. Bấm 'Lưu nháp'.",
     "Tỷ giá (VND): 0",
     "- Ô Tỷ giá viền đỏ, hiện 'Phải lớn hơn 0'; phiếu không được lưu."),

    (10, "Tỷ giá nhập chữ", "P1",
     "Loại tiền là ngoại tệ.",
     "1. Gõ 'abc' vào ô Tỷ giá.",
     "Tỷ giá (VND): abc",
     "- Ô chỉ nhận số, chữ không vào được hoặc bị báo phải là số."),

    (11, "Loại vận chuyển thiếu Đến ngày", "P0",
     "Loại chi 'Thanh toán chi phí vận chuyển NCC', đã có nhà cung cấp và dòng chi tiết, chưa "
     "chọn 'Đến ngày'.",
     "1. Bấm 'Lưu và gửi duyệt' rồi 'Xác nhận'.",
     "—",
     "- Ô 'Đến ngày' viền đỏ kèm 'Bắt buộc nhập'; phiếu không được lưu."),

    (12, "Lý do chi rất dài", "P2",
     "Đang mở form Tạo mới.",
     "1. Nhập Lý do chi dài 500 ký tự.\n2. Lưu nháp và mở lại phiếu.",
     "Lý do chi: chuỗi 500 ký tự",
     "- Lưu được, mở lại thấy đúng nội dung; cột 'Lý do chi' trên lưới xuống dòng chứ không phá "
     "vỡ bố cục bảng."),

    (13, "Lý do chi chứa ký tự đặc biệt và dấu tiếng Việt", "P2",
     "Đang mở form Tạo mới.",
     "1. Nhập Lý do chi = \"Chi trả đợt 1 <&'> — công nợ quá hạn\".\n2. Lưu nháp, mở lại.",
     "Lý do chi: Chi trả đợt 1 <&'> — công nợ quá hạn",
     "- Hiển thị đúng nguyên văn ở màn chi tiết, lưới danh sách và bản in."),
]

S9 = [
    (1, "Nút Sửa chỉ hiện với phiếu của mình ở trạng thái cho sửa", "P0",
     "Tài khoản A có: phiếu P1 do A lập trạng thái 'Đang tạo'; P2 do A lập 'Không duyệt'; P3 do "
     "A lập 'Chờ TP duyệt'; P4 do người khác lập 'Chờ kế toán công nợ duyệt'.",
     "1. Mở màn danh sách bằng tài khoản A.\n2. Xem cột Hành động của từng phiếu.",
     "—",
     "- P1 và P2 có nút Sửa (hình bút chì) và mục Xóa.\n"
     "- P3 và P4 KHÔNG có nút Sửa và không có mục Xóa."),

    (2, "Mở form Sửa và kiểm tra dữ liệu nạp lên", "P0",
     "Phiếu P1 'Đang tạo' của tài khoản A có 2 dòng chi tiết và 1 file đính kèm.",
     "1. Bấm nút Sửa ở dòng phiếu P1.",
     "—",
     "- Tiêu đề trang 'Sửa phiếu đề nghị thanh toán'.\n"
     "- Có thêm ô 'Mã phiếu' (khóa); góc phải tiêu đề khối Thông tin chung hiện người lập và "
     "ngày lập.\n"
     "- Mọi ô còn lại nạp đúng dữ liệu đã lưu; bảng chi tiết đủ 2 dòng; khối file hiện file cũ."),

    (3, "Mã phiếu không sửa được", "P0",
     "Đang mở form Sửa.",
     "1. Bấm vào ô 'Mã phiếu' và gõ ký tự.",
     "Gõ: ABC",
     "- Ô bị khóa, không nhập được, giá trị giữ nguyên."),

    (4, "Sửa và lưu nháp", "P0",
     "Phiếu P1 'Đang tạo'.",
     "1. Đổi Lý do chi.\n2. Bấm 'Lưu nháp'.\n3. Mở lại phiếu.",
     "Lý do chi: (nội dung mới)",
     "- Báo 'Lưu phiếu đề nghị thanh toán thành công!'.\n"
     "- Trạng thái vẫn 'Đang tạo', Lý do chi đã đổi.\n"
     "- Cột 'Người cập nhật' và 'Ngày cập nhật' trên lưới đổi theo."),

    (5, "Thêm và xóa dòng chi tiết khi sửa", "P0",
     "Phiếu P1 đang có 1 dòng chi tiết.",
     "1. Bấm Sửa, thêm dòng 2 với hợp đồng khác + số tiền 2,000,000, bấm 'Lưu nháp'.\n"
     "2. Mở lại phiếu, bấm Sửa, xóa dòng 2, bấm 'Lưu nháp'.\n"
     "3. Mở lại phiếu.",
     "Dòng 2: 2.000.000",
     "- Sau bước 1 phiếu có 2 dòng; sau bước 2 phiếu chỉ còn 1 dòng.\n"
     "- Tổng tiền trên lưới tính lại đúng ở cả 2 lần."),

    (6, "Thêm file đính kèm khi sửa", "P1",
     "Phiếu P1 đã có 1 file.",
     "1. Bấm Sửa, bấm 'Thêm tài liệu', chọn thêm 1 file.\n2. Bấm 'Lưu nháp'.\n3. Mở lại phiếu.",
     "File mới: phu-luc.pdf",
     "- Phiếu có 2 file đính kèm."),

    (7, "Xóa file đã lưu của phiếu", "P0",
     "Phiếu P1 đang có 2 file.",
     "1. Bấm Sửa, bấm nút Xóa ở dòng file thứ 2, xác nhận.\n2. Mở lại phiếu.",
     "—",
     "- Phiếu chỉ còn 1 file.\n"
     "- ⚠️ File bị xóa hẳn khỏi kho lưu trữ, không hoàn tác được."),

    (8, "Sửa phiếu Không duyệt rồi gửi lại", "P0",
     "Phiếu P2 do A lập, trạng thái 'Không duyệt', ghi chú của cấp từ chối đang hiển thị.",
     "1. Bấm Sửa phiếu P2, chỉnh số tiền đề nghị chi.\n"
     "2. Bấm 'Lưu và gửi duyệt' rồi 'Xác nhận'.",
     "Số tiền đề nghị chi: 4.000.000",
     "- Báo 'Gửi duyệt phiếu đề nghị thanh toán thành công!'.\n"
     "- Trạng thái phiếu chuyển sang 'Chờ TP duyệt' và phiếu quay lại màn chờ duyệt của trưởng "
     "phòng."),

    (9, "Cảnh báo chưa lưu ở form Sửa", "P0",
     "Đang mở form Sửa và vừa đổi Lý do chi.",
     "1. Bấm 'Quay lại'.",
     "—",
     "- Hộp thoại 'Thông tin chưa lưu' hiện; bấm 'Thoát' thì dữ liệu phiếu KHÔNG bị thay đổi."),

    (10, "Sửa từ màn chi tiết", "P1",
     "Đang xem chi tiết phiếu 'Đang tạo' của chính mình.",
     "1. Bấm nút 'Sửa' ở thanh nút dưới cùng.",
     "—",
     "- Chuyển sang màn 'Sửa phiếu đề nghị thanh toán' đúng phiếu đó."),
]

S10 = [
    (1, "Mở chi tiết phiếu — mọi ô ở chế độ chỉ đọc", "P0",
     "Có phiếu ở trạng thái 'Chờ kế toán trưởng duyệt' với 1 dòng chi tiết và 1 file đính kèm.",
     "1. Bấm mã phiếu để vào chi tiết.\n2. Thử gõ vào ô 'Lý do chi' và ô số tiền đề nghị.",
     "—",
     "- Mọi ô đều khóa, không nhập được; bấm ô đối tượng không mở cửa sổ chọn.\n"
     "- Có thêm ô 'Trạng thái' (chỉ đọc) trong khối Thông tin chung."),

    (2, "Bảng chi tiết ở màn xem có 4 cột tiền của các cấp", "P0",
     "Phiếu đã qua cấp Trưởng phòng và Kế toán công nợ.",
     "1. Mở chi tiết phiếu, cuộn ngang bảng Chi tiết.",
     "—",
     "- Có thêm 4 cột: 'TP duyệt', 'KT công nợ duyệt', 'KT trưởng / BGĐ duyệt', 'Số tiền chi'.\n"
     "- Các cấp đã duyệt hiện số tiền; cấp chưa duyệt hiện 0.\n"
     "- ⚠️ Cột 'Số tiền chi' hiện dấu gạch dưới khi chưa có phiếu chi — KHÔNG hiện số 0."),

    (3, "Ô nhập số tiền chỉ mở ở cột của cấp đang duyệt", "P0",
     "Tài khoản là Kế toán trưởng, phiếu đang 'Chờ kế toán trưởng duyệt'.",
     "1. Mở chi tiết phiếu, thử gõ vào từng cột tiền của bảng chi tiết.",
     "—",
     "- ⚠️ CHỈ cột 'KT trưởng / BGĐ duyệt' là ô nhập được; 3 cột còn lại chỉ đọc."),

    (4, "Dòng Tổng cộng của bảng chi tiết màn xem", "P0",
     "Phiếu có 2 dòng chi tiết.",
     "1. Đọc dòng cuối bảng chi tiết.",
     "—",
     "- Dòng 'Tổng cộng' cộng đủ mọi cột số, kể cả 4 cột tiền của các cấp."),

    (5, "Bộ nút màn chi tiết — phiếu nháp của mình", "P0",
     "Phiếu 'Đang tạo' do chính người đăng nhập lập.",
     "1. Mở chi tiết phiếu, đọc thanh nút dưới cùng.",
     "—",
     "- Có nút 'Sửa', 'In', 'Xuất Excel', 'Xóa', 'Quay lại'.\n"
     "- Không có nút duyệt và nút 'Từ chối'."),

    (6, "Bộ nút màn chi tiết — người duyệt đúng cấp", "P0",
     "Tài khoản là Kế toán công nợ, phiếu đang 'Chờ kế toán công nợ duyệt'.",
     "1. Mở chi tiết phiếu.",
     "—",
     "- Có nút 'Duyệt', 'In', 'Xuất Excel', 'Từ chối', 'Quay lại'.\n"
     "- Không có nút 'Sửa' và 'Xóa'."),

    (7, "Bộ nút màn chi tiết — phiếu đã hoàn tất", "P1",
     "Phiếu ở trạng thái 'Duyệt phiếu chi'.",
     "1. Mở chi tiết phiếu.",
     "—",
     "- Chỉ còn 'In', 'Xuất Excel' và 'Quay lại'.\n"
     "- ⚠️ Không có nút nào làm thay đổi phiếu."),

    (8, "Nút Tạo phiếu chi và Tạo ủy nhiệm chi", "P0",
     "Tài khoản có quyền 'Kế toán thanh toán'. Phiếu X 'Chờ tạo phiếu chi' hình thức TM; phiếu Y "
     "'Chờ tạo phiếu chi' hình thức CK; cả 2 chưa có chứng từ chi.",
     "1. Mở chi tiết phiếu X.\n2. Mở chi tiết phiếu Y.",
     "—",
     "- Phiếu X có nút 'Tạo phiếu chi'; phiếu Y có nút 'Tạo ủy nhiệm chi'.\n"
     "- ⚠️ Không phiếu nào hiện cả 2 nút cùng lúc.\n"
     "- Bấm nút chuyển sang màn lập chứng từ tương ứng, phiếu đề nghị đã gắn sẵn."),

    (9, "Tiêu đề trang chi tiết kèm mã phiếu", "P2",
     "Phiếu TPE.DNTT0826.00002.",
     "1. Mở chi tiết phiếu, đọc tiêu đề trang và tiêu đề tab trình duyệt.",
     "—",
     "- Cả hai đều hiện 'Chi tiết phiếu đề nghị thanh toán: TPE.DNTT0826.00002'."),

    (10, "Công nợ tính lại theo sổ kế toán khi mở phiếu", "P1",
     "Phiếu gắn hợp đồng H; sổ kế toán vừa phát sinh thêm khoản chi cho hợp đồng H.",
     "1. Mở chi tiết phiếu, ghi lại cột công nợ.\n2. Tải lại trang và đọc lại.",
     "—",
     "- Giá trị phản ánh số dư công nợ mới nhất.\n"
     "- ⚠️ Số này KHÔNG lưu trong phiếu nên có thể khác lần xem trước — không phải lỗi."),
]

S11 = [
    (1, "Trưởng phòng duyệt", "P0",
     "Tài khoản F là Trưởng phòng phòng Kinh doanh 1. Phiếu P đang 'Chờ TP duyệt', thuộc phòng "
     "Kinh doanh 1, có 1 dòng chi tiết số tiền đề nghị 5,000,000.",
     "1. Đăng nhập F, mở chi tiết phiếu P.\n"
     "2. Nhập 5,000,000 vào cột 'TP duyệt' của dòng 1.\n"
     "3. Bấm nút 'Duyệt'.\n4. Đọc hộp xác nhận rồi bấm nút xác nhận.",
     "TP duyệt: 5.000.000",
     "- Hộp thoại 'Xác nhận duyệt' nêu rõ mã phiếu và cấp sẽ nhận phiếu tiếp theo.\n"
     "- Sau khi xác nhận: báo duyệt thành công kèm tên cấp nhận phiếu.\n"
     "- Trạng thái phiếu chuyển sang 'Chờ kế toán công nợ duyệt'.\n"
     "- Cột 'Ngày nhận' trên lưới được điền."),

    (2, "Kế toán công nợ duyệt và sửa số tiền", "P0",
     "Tài khoản G là Kế toán công nợ. Phiếu P đang 'Chờ kế toán công nợ duyệt', cột TP duyệt là "
     "5,000,000.",
     "1. Đăng nhập G, mở chi tiết phiếu P.\n"
     "2. Nhập 4,500,000 vào cột 'KT công nợ duyệt'.\n3. Bấm 'Duyệt' rồi xác nhận.",
     "KT công nợ duyệt: 4.500.000",
     "- Duyệt thành công, trạng thái chuyển sang 'Chờ kế toán trưởng duyệt'.\n"
     "- Cột 'KT công nợ duyệt' lưu đúng 4,500,000, cột 'TP duyệt' giữ nguyên 5,000,000."),

    (3, "Kế toán trưởng duyệt thẳng", "P0",
     "Tài khoản H là Kế toán trưởng. Phiếu P đang 'Chờ kế toán trưởng duyệt'.",
     "1. Đăng nhập H, mở chi tiết phiếu P.\n"
     "2. Nhập số tiền vào cột 'KT trưởng / BGĐ duyệt'.\n3. Bấm nút 'Duyệt' rồi xác nhận.",
     "KT trưởng / BGĐ duyệt: 4.500.000",
     "- Trạng thái chuyển thẳng sang 'Chờ tạo phiếu chi' (bỏ qua cấp Ban giám đốc).\n"
     "- Thông báo thành công nêu cấp nhận phiếu là kế toán thanh toán."),

    (4, "Kế toán trưởng chuyển Ban giám đốc duyệt", "P0",
     "Tài khoản H là Kế toán trưởng. Phiếu Q đang 'Chờ kế toán trưởng duyệt'.",
     "1. Mở chi tiết phiếu Q, nhập số tiền vào cột 'KT trưởng / BGĐ duyệt'.\n"
     "2. Bấm nút 'Chuyển duyệt BGĐ' rồi xác nhận.",
     "KT trưởng / BGĐ duyệt: 10.000.000",
     "- ⚠️ Câu hỏi xác nhận và chữ trên nút xác nhận KHÁC với nút 'Duyệt' (đây là chuyển cấp, "
     "không phải duyệt xong).\n"
     "- Trạng thái chuyển sang 'Chờ ban giám đốc duyệt'."),

    (5, "Ban giám đốc duyệt", "P0",
     "Tài khoản I là Ban giám đốc. Phiếu Q đang 'Chờ ban giám đốc duyệt'.",
     "1. Đăng nhập I, mở chi tiết phiếu Q, nhập số tiền, bấm 'Duyệt' rồi xác nhận.",
     "KT trưởng / BGĐ duyệt: 9.000.000",
     "- Trạng thái chuyển sang 'Chờ tạo phiếu chi'.\n"
     "- ⚠️ Số tiền của Ban giám đốc ghi CHUNG cột với Kế toán trưởng — đúng thiết kế."),

    (6, "Thông báo khi duyệt xong một cấp", "P0",
     "Phiếu P vừa được Trưởng phòng duyệt.",
     "1. Đăng nhập tài khoản kế toán công nợ, mở chuông thông báo.\n"
     "2. Đăng nhập tài khoản người lập phiếu, mở chuông thông báo.",
     "—",
     "- Kế toán công nợ nhận thông báo có việc cần duyệt, kèm mã phiếu.\n"
     "- Người lập nhận thông báo phiếu đã được duyệt, có ghi rõ cấp vừa duyệt.\n"
     "- Bấm vào thông báo mở đúng phiếu."),

    (7, "Nút Duyệt ở cột Hành động của danh sách", "P1",
     "Tài khoản giữ vai duyệt, đang ở chế độ Chờ duyệt.",
     "1. Bấm nút Duyệt (biểu tượng dấu tích) ở một dòng.",
     "—",
     "- ⚠️ KHÔNG duyệt ngay tại danh sách mà mở màn chi tiết của phiếu đó — người duyệt phải xem "
     "và sửa số tiền trước khi duyệt."),

    (8, "Không có nút duyệt khi sai cấp", "P0",
     "Tài khoản G là Kế toán công nợ. Phiếu R đang ở 'Chờ kế toán trưởng duyệt' (G vẫn xem được "
     "vì đã duyệt phiếu này ở cấp trước).",
     "1. Mở chi tiết phiếu R.",
     "—",
     "- KHÔNG có nút 'Duyệt' và KHÔNG có nút 'Từ chối'.\n"
     "- Chỉ còn 'In', 'Xuất Excel', 'Quay lại'."),

    (9, "Trưởng phòng không duyệt được phiếu phòng ban khác", "P0",
     "Tài khoản F quản lý phòng Kinh doanh 1. Phiếu S đang 'Chờ TP duyệt' nhưng thuộc phòng "
     "Kinh doanh 2 (F không quản lý).",
     "1. Mở chi tiết phiếu S bằng đường dẫn trực tiếp.",
     "—",
     "- Hệ thống từ chối cho xem, hoặc mở được nhưng KHÔNG có nút 'Duyệt' và 'Từ chối'."),

    (10, "Duyệt khi bỏ trống số tiền của cấp mình", "P1",
     "Tài khoản đúng cấp duyệt, phiếu có 1 dòng chi tiết, ô số tiền của cấp mình để 0.",
     "1. Bấm 'Duyệt' rồi xác nhận.",
     "Số tiền của cấp: 0",
     "- ⚠️ Duyệt được, số 0 được ghi nhận — hệ thống không chặn số 0 ở bước duyệt."),
]

S12 = [
    (1, "Mở cửa sổ Từ chối", "P0",
     "Tài khoản là Kế toán trưởng, phiếu đang 'Chờ kế toán trưởng duyệt'.",
     "1. Mở chi tiết phiếu, bấm nút 'Từ chối'.",
     "—",
     "- Cửa sổ 'Từ chối phiếu' mở ra, dòng phụ hiện mã phiếu.\n"
     "- Có ô bắt buộc 'Ghi chú của Kế toán trưởng' và ô không bắt buộc 'Lý do không duyệt'.\n"
     "- Có nút 'Từ chối' và 'Đóng'."),

    (2, "Tên ô ghi chú đổi theo cấp đang giữ phiếu", "P0",
     "Có phiếu ở 4 trạng thái: Chờ TP duyệt, Chờ kế toán công nợ duyệt, Chờ kế toán trưởng "
     "duyệt, Chờ ban giám đốc duyệt; tài khoản giữ đủ 4 vai.",
     "1. Lần lượt mở từng phiếu và bấm 'Từ chối'.",
     "—",
     "- Nhãn ô bắt buộc đổi đúng theo cấp: 'Ghi chú của Trưởng phòng', 'Ghi chú của Kế toán công "
     "nợ', 'Ghi chú của Kế toán trưởng', 'Ghi chú của Ban giám đốc'."),

    (3, "Từ chối khi bỏ trống ô ghi chú", "P0",
     "Đang mở cửa sổ 'Từ chối phiếu'.",
     "1. Để trống ô ghi chú bắt buộc.\n2. Bấm nút 'Từ chối'.",
     "Ghi chú: (bỏ trống)",
     "- Ô viền đỏ, hiện 'Bắt buộc nhập'.\n"
     "- Cửa sổ KHÔNG đóng, trạng thái phiếu không đổi."),

    (4, "Từ chối chỉ nhập khoảng trắng", "P1",
     "Đang mở cửa sổ 'Từ chối phiếu'.",
     "1. Gõ 3 dấu cách vào ô ghi chú bắt buộc, bấm 'Từ chối'.",
     "Ghi chú: '   '",
     "- Vẫn báo lỗi bắt buộc nhập, không cho gửi."),

    (5, "Từ chối ở cấp Trưởng phòng — phiếu về Đang tạo", "P0",
     "Tài khoản F là Trưởng phòng. Phiếu P đang 'Chờ TP duyệt'.",
     "1. Mở chi tiết phiếu P, bấm 'Từ chối'.\n"
     "2. Nhập 'Ghi chú của Trưởng phòng' = 'Sai số tiền, lập lại'.\n3. Bấm 'Từ chối'.",
     "Ghi chú của Trưởng phòng: Sai số tiền, lập lại",
     "- Báo 'Không duyệt phiếu đề nghị thanh toán thành công!'.\n"
     "- ⚠️ Trạng thái phiếu về **'Đang tạo'**, KHÔNG phải 'Không duyệt' — đây là quy tắc nghiệp "
     "vụ riêng của cấp Trưởng phòng.\n"
     "- Người lập mở phiếu thấy nút 'Sửa' và 'Xóa'."),

    (6, "Từ chối ở cấp Kế toán công nợ — phiếu sang Không duyệt", "P0",
     "Tài khoản G là Kế toán công nợ. Phiếu P đang 'Chờ kế toán công nợ duyệt'.",
     "1. Mở chi tiết, bấm 'Từ chối', nhập ghi chú, bấm 'Từ chối'.",
     "Ghi chú của Kế toán công nợ: Thiếu chứng từ",
     "- ⚠️ Trạng thái phiếu chuyển sang **'Không duyệt'**.\n"
     "- Phiếu rời khỏi màn chờ duyệt."),

    (7, "Lý do không duyệt hiển thị cho người lập", "P0",
     "Vừa từ chối phiếu ở trường hợp trên, có nhập cả ô 'Lý do không duyệt' = 'Bổ sung hoá đơn'.",
     "1. Đăng nhập tài khoản người lập, mở chuông thông báo và mở chi tiết phiếu.",
     "—",
     "- Thông báo trên chuông có kèm lý do.\n"
     "- Màn chi tiết / bản in hiển thị ghi chú của cấp đã từ chối và lý do không duyệt."),

    (8, "Thông báo từ chối gửi cho các cấp đã đi qua", "P1",
     "Phiếu đang ở 'Chờ kế toán trưởng duyệt' (đã qua Trưởng phòng và Kế toán công nợ) bị từ chối.",
     "1. Kiểm tra chuông của: người lập, tài khoản Trưởng phòng, tài khoản Kế toán công nợ.",
     "—",
     "- Cả 3 đều nhận được thông báo phiếu bị từ chối.\n"
     "- ⚠️ Cấp CHƯA đi qua (Ban giám đốc) không nhận thông báo."),

    (9, "Đóng cửa sổ Từ chối không làm gì", "P1",
     "Đang mở cửa sổ và đã gõ ghi chú.",
     "1. Bấm nút 'Đóng'.\n2. Mở lại cửa sổ.",
     "Ghi chú: thử",
     "- Cửa sổ đóng, trạng thái phiếu không đổi.\n"
     "- Mở lại thì 2 ô đã trống (không giữ nội dung cũ)."),

    (10, "Không có nút Từ chối ở danh sách", "P1",
     "Tài khoản giữ vai duyệt, đang ở chế độ Chờ duyệt.",
     "1. Xem cột Hành động và mở nút ba chấm của các dòng.",
     "—",
     "- ⚠️ KHÔNG có mục 'Từ chối' ở danh sách — hành động này chỉ đặt ở màn chi tiết vì phải "
     "nhập ghi chú."),
]

S13 = [
    (1, "Hộp xác nhận xóa từ danh sách", "P0",
     "Phiếu 'Đang tạo' do người đăng nhập lập, mã TPE.DNTT0826.00017.",
     "1. Bấm nút ba chấm ở cột Hành động.\n2. Bấm 'Xóa'.",
     "—",
     "- Hộp thoại 'Xác nhận xóa' hiện: Bạn có chắc muốn xóa phiếu đề nghị thanh toán "
     "'TPE.DNTT0826.00017'?\n"
     "- Có 2 nút 'Xóa' và 'Hủy'."),

    (2, "Hủy hộp xác nhận xóa", "P0",
     "Đang mở hộp 'Xác nhận xóa'.",
     "1. Bấm 'Hủy'.",
     "—",
     "- Hộp đóng, phiếu vẫn còn nguyên trong danh sách."),

    (3, "Xóa phiếu thành công", "P0",
     "Phiếu 'Đang tạo' do chính mình lập, có dòng chi tiết và file đính kèm.",
     "1. Bấm ba chấm > 'Xóa'.\n2. Bấm 'Xóa' trong hộp xác nhận.",
     "—",
     "- Hệ thống báo xóa thành công.\n"
     "- Danh sách tự tải lại, phiếu biến mất, tổng số phiếu giảm 1."),

    (4, "Không có mục Xóa với phiếu đã gửi duyệt", "P0",
     "Phiếu do chính mình lập, trạng thái 'Chờ TP duyệt'.",
     "1. Bấm nút ba chấm ở cột Hành động.",
     "—",
     "- Menu chỉ còn 'Xuất Excel' và 'Lịch sử'; không có 'Xóa'."),

    (5, "Xóa từ màn chi tiết", "P1",
     "Đang xem chi tiết phiếu 'Đang tạo' của chính mình.",
     "1. Bấm nút 'Xóa' ở thanh nút dưới cùng, xác nhận.",
     "—",
     "- Báo xóa thành công và quay về màn danh sách; phiếu không còn."),

    (6, "Mở màn in từ danh sách", "P0",
     "Phiếu bất kỳ xem được.",
     "1. Bấm nút hình máy in ở cột Hành động.",
     "—",
     "- Mở TAB MỚI hiển thị bản in của đúng phiếu, tiêu đề tab 'In phiếu <mã phiếu>'."),

    (7, "Nội dung phần đầu bản in", "P0",
     "Như trên.",
     "1. Đọc phần đầu bản in.",
     "—",
     "- Có logo và thông tin công ty ở đầu trang.\n"
     "- Tiêu đề giữa trang: 'PHIẾU ĐỀ NGHỊ THANH TOÁN', dưới là dòng 'Ngày … tháng … năm …' và "
     "'Số phiếu: <mã>'.\n"
     "- Khối thông tin 2 cột gồm: Hình thức thanh toán, Ngày lập, Loại thanh toán, Người lập, "
     "Lý do chi, Phòng ban, Tỷ giá; thêm 'Đến ngày' với loại vận chuyển và dòng đối tượng nhận "
     "tiền nếu có."),

    (8, "Khối ngân hàng trên bản in", "P1",
     "Phiếu hình thức CK có đủ thông tin ngân hàng.",
     "1. Đọc khối ngay dưới phần thông tin chung.",
     "—",
     "- In các dòng Chủ tài khoản, Số tài khoản, Ngân hàng, Chi nhánh, Thành phố; với nhà cung "
     "cấp nước ngoài in thêm Swift Code, IBAN Number và Phí."),

    (9, "Bảng chi tiết trên bản in", "P0",
     "Phiếu đã qua vài cấp duyệt.",
     "1. Đọc bảng trên bản in.",
     "—",
     "- Tiêu đề bảng 2 dòng, dòng dưới ghi đơn vị tiền của từng cột.\n"
     "- Có các cột số tiền theo cấp duyệt và dòng 'Tổng cộng'.\n"
     "- ⚠️ Cột 'Số tiền chi' CHỈ in khi phiếu đã ở trạng thái 'Duyệt phiếu chi'."),

    (10, "Khối ký tên trên bản in", "P1",
     "Phiếu đã qua vài cấp duyệt.",
     "1. Xem phần cuối bản in.",
     "—",
     "- Năm ô ký: BAN GIÁM ĐỐC, KẾ TOÁN TRƯỞNG, KẾ TOÁN CÔNG NỢ, TRƯỞNG PHÒNG, NGƯỜI ĐỀ NGHỊ.\n"
     "- Cấp đã duyệt hiện tên người duyệt kèm chữ 'Đã duyệt'; người lập hiện tên kèm 'Đã ký'."),

    (11, "Bấm nút In để mở hộp thoại in", "P0",
     "Đang ở màn in.",
     "1. Bấm nút 'In' màu xanh góc trên trái.",
     "—",
     "- Hộp thoại in của trình duyệt mở ra.\n"
     "- Bản xem trước KHÔNG có nút 'In' và không có menu bên trái."),

    (12, "Xuất Excel một phiếu", "P0",
     "Phiếu bất kỳ xem được.",
     "1. Bấm mục 'Xuất Excel' ở cột Hành động (hoặc nút 'Xuất Excel' ở màn chi tiết).",
     "—",
     "- Trình duyệt tải về file có đuôi .xlsx, tên file chứa mã phiếu.\n"
     "- Mở file: có logo/letterhead công ty, bảng chi tiết và số liệu KHỚP với bản in."),

    (13, "Xuất Excel phiếu ngoại tệ", "P1",
     "Phiếu loại tiền USD, đã qua vài cấp duyệt.",
     "1. Xuất Excel phiếu này.",
     "—",
     "- File có cả cột nguyên tệ và cột quy đổi VND, khớp với bản in.\n"
     "- ⚠️ Ô tiền hiển thị theo định dạng số kiểu Việt Nam."),
]

S14 = [
    (1, "Mở cửa sổ Lịch sử từ danh sách", "P0",
     "Phiếu đã trải qua tạo mới, sửa và vài lần đổi trạng thái.",
     "1. Bấm nút ba chấm ở cột Hành động, chọn 'Lịch sử'.",
     "—",
     "- Cửa sổ 'Lịch sử thay đổi' mở, dòng phụ ghi 'Phiếu: <mã phiếu>'.\n"
     "- Có nút 'Bộ lọc' và nút 'Đóng'."),

    (2, "Nội dung một mốc lịch sử", "P0",
     "Như trên.",
     "1. Đọc các mốc trong cửa sổ từ dưới lên.",
     "—",
     "- Mốc dưới cùng là 'Tạo mới' kèm ngày giờ và 'Người thực hiện: <tên> – <phòng ban>'.\n"
     "- Mốc 'Thay đổi thông tin' liệt kê từng trường đã đổi với mũi tên từ giá trị cũ sang mới.\n"
     "- Mốc 'Thay đổi trạng thái' ghi rõ trạng thái cũ → trạng thái mới bằng tên tiếng Việt."),

    (3, "Lịch sử ghi số tiền của từng cấp duyệt", "P0",
     "Phiếu vừa được Trưởng phòng duyệt với số tiền 111,111.",
     "1. Mở lịch sử phiếu.",
     "—",
     "- Mốc duyệt ghi trạng thái 'Chờ TP duyệt' → 'Chờ kế toán công nợ duyệt'.\n"
     "- ⚠️ Kèm khối 'Số tiền TP duyệt sửa thông tin' liệt kê ĐÚNG DÒNG chi tiết và giá trị cũ → "
     "giá trị mới."),

    (4, "Lịch sử ghi lý do từ chối", "P0",
     "Phiếu vừa bị một cấp từ chối kèm ghi chú.",
     "1. Mở lịch sử phiếu.",
     "—",
     "- Mốc mới nhất là đổi trạng thái sang 'Đang tạo' (nếu cấp Trưởng phòng) hoặc 'Không duyệt' "
     "(các cấp sau), kèm ghi chú đã nhập.\n"
     "- Người thực hiện là tài khoản đã từ chối."),

    (5, "Khối Lịch sử ở màn chi tiết", "P0",
     "Đang xem chi tiết một phiếu.",
     "1. Cuộn xuống cuối trang, bấm nút 'Xem lịch sử'.",
     "—",
     "- Khối 'Lịch sử' mở ra với nội dung y hệt cửa sổ ngoài danh sách; có số đếm số mốc.\n"
     "- Nút đổi thành 'Thu gọn', bên cạnh có nút 'Làm mới'."),

    (6, "Phiếu chưa có thao tác nào", "P1",
     "Phiếu cũ được nạp sẵn, chưa từng thao tác trên màn này.",
     "1. Mở lịch sử phiếu đó.",
     "—",
     "- Hiện dòng 'Chưa có lịch sử thao tác nào.', không báo lỗi."),

    (7, "Hai người cùng lập phiếu — mã phiếu không trùng", "P0",
     "Hai tài khoản cùng công ty, cùng đăng nhập.",
     "1. Cả hai cùng mở form Tạo mới, nhập Lý do chi.\n"
     "2. Bấm 'Lưu nháp' gần như cùng lúc.\n3. Đối chiếu mã 2 phiếu vừa tạo.",
     "—",
     "- Hai mã phiếu khác nhau, số cuối chạy liên tiếp.\n"
     "- ⚠️ Không có phiếu nào bị lỗi lưu."),

    (8, "Hai cấp duyệt cùng xử lý một phiếu", "P0",
     "Hai tài khoản cùng giữ vai Kế toán công nợ, cùng mở chi tiết một phiếu 'Chờ kế toán công "
     "nợ duyệt'.",
     "1. Người thứ nhất bấm 'Duyệt' và xác nhận thành công.\n"
     "2. Người thứ hai cũng bấm 'Duyệt' và xác nhận.",
     "—",
     "- Người thứ hai bị từ chối: hệ thống báo không chuyển được phiếu sang trạng thái này (hoặc "
     "không còn quyền duyệt ở trạng thái hiện tại).\n"
     "- ⚠️ Phiếu chỉ ghi 1 lần duyệt, lịch sử không có 2 mốc trùng."),

    (9, "Mở 2 tab cùng một phiếu — tab kia gửi duyệt trước", "P0",
     "Phiếu 'Đang tạo' của chính mình, mở form Sửa ở 2 tab.",
     "1. Tab 1 bấm 'Lưu và gửi duyệt' và xác nhận.\n"
     "2. Sang tab 2 bấm 'Lưu nháp'.",
     "—",
     "- Tab 2 bị từ chối với thông báo không có quyền sửa phiếu này (phiếu đã rời trạng thái cho "
     "sửa).\n"
     "- Nội dung của tab 2 KHÔNG đè lên phiếu."),

    (10, "Mở chi tiết phiếu vừa bị người khác xóa", "P1",
     "Người lập vừa xóa phiếu R ở máy khác; người kiểm thử đang mở danh sách cũ có phiếu R.",
     "1. Bấm vào mã phiếu R.",
     "—",
     "- Hệ thống báo không tải được phiếu và đưa về màn danh sách, không treo trang trắng."),
]

S15 = [
    (1, "Luồng đầy đủ 5 cấp: lập → TP → KT công nợ → KT trưởng → BGĐ → chờ tạo phiếu chi", "P0",
     "Tài khoản A (người lập, phòng Kinh doanh 1, công ty 1); F (Trưởng phòng phòng Kinh doanh "
     "1); G (Kế toán công nợ); H (Kế toán trưởng); I (Ban giám đốc) — đều thuộc công ty 1. "
     "Nhà cung cấp X có hợp đồng mua.",
     "1. A: Tạo mới, Loại chi 'Chi trả nhà cung cấp', hình thức 'TM', Lý do chi 'Thanh toán đợt "
     "1'; thêm dòng chi tiết chọn nhà cung cấp X + hợp đồng, số tiền 10,000,000; đính kèm 1 "
     "file; bấm 'Lưu và gửi duyệt' và xác nhận.\n"
     "2. F: mở màn chờ duyệt, mở phiếu, nhập TP duyệt 10,000,000, bấm 'Duyệt'.\n"
     "3. G: mở phiếu, nhập KT công nợ duyệt 9,000,000, bấm 'Duyệt'.\n"
     "4. H: mở phiếu, nhập KT trưởng / BGĐ duyệt 9,000,000, bấm 'Chuyển duyệt BGĐ'.\n"
     "5. I: mở phiếu, bấm 'Duyệt'.\n"
     "6. Mở lịch sử phiếu.",
     "10.000.000 → 9.000.000",
     "- Bước 1: trạng thái 'Chờ TP duyệt', F nhận thông báo.\n"
     "- Bước 2: 'Chờ kế toán công nợ duyệt', cột Ngày nhận được điền.\n"
     "- Bước 3: 'Chờ kế toán trưởng duyệt'.\n"
     "- Bước 4: 'Chờ ban giám đốc duyệt'.\n"
     "- Bước 5: 'Chờ tạo phiếu chi'; kế toán thanh toán nhận thông báo.\n"
     "- Bước 6: lịch sử đủ mọi mốc theo thứ tự thời gian, mỗi mốc có người thực hiện và số tiền "
     "cấp đó duyệt."),

    (2, "Luồng bị từ chối ở cấp Trưởng phòng rồi gửi lại", "P0",
     "Tài khoản A (người lập) và F (Trưởng phòng cùng phòng ban).",
     "1. A lập phiếu và gửi duyệt.\n"
     "2. F mở phiếu, bấm 'Từ chối', nhập 'Ghi chú của Trưởng phòng' = 'Sai hợp đồng'.\n"
     "3. A mở phiếu, đọc ghi chú, bấm 'Sửa', đổi hợp đồng, bấm 'Lưu và gửi duyệt'.\n"
     "4. F mở lại màn chờ duyệt.",
     "—",
     "- Bước 2: ⚠️ trạng thái về **'Đang tạo'** (không phải 'Không duyệt').\n"
     "- Bước 3: sửa được vì phiếu đang ở trạng thái cho sửa; sau khi gửi lại trạng thái là "
     "'Chờ TP duyệt'.\n"
     "- Bước 4: phiếu xuất hiện lại trong danh sách chờ duyệt của F."),

    (3, "Luồng bị từ chối ở cấp Kế toán công nợ rồi gửi lại", "P0",
     "Tài khoản A (người lập) và G (Kế toán công nợ).",
     "1. Phiếu đã qua Trưởng phòng, đang 'Chờ kế toán công nợ duyệt'.\n"
     "2. G bấm 'Từ chối', nhập ghi chú và lý do không duyệt.\n"
     "3. A mở phiếu, sửa lại và gửi duyệt lại.",
     "—",
     "- Bước 2: ⚠️ trạng thái sang **'Không duyệt'**.\n"
     "- Bước 3: phiếu quay về 'Chờ TP duyệt' — phải đi lại từ cấp đầu."),

    (4, "Luồng phiếu chuyển khoản nhà cung cấp có file đính kèm", "P0",
     "Nhà cung cấp X trong nước, đã khai tài khoản ngân hàng.",
     "1. Tạo mới, Loại chi 'Chi trả nhà cung cấp', hình thức 'CK', chọn nhà cung cấp X.\n"
     "2. Kiểm tra khối ngân hàng tự điền.\n"
     "3. Thêm 1 dòng chi tiết (chỉ chọn hợp đồng, không có cột đối tượng), nhập số tiền.\n"
     "4. Đính kèm 1 file PDF.\n5. 'Lưu và gửi duyệt' và xác nhận.\n"
     "6. Mở chi tiết và bản in.",
     "Nhà cung cấp X · 20.000.000",
     "- Khối ngân hàng tự điền đủ 5 ô và ở chế độ chỉ đọc.\n"
     "- Bảng chi tiết KHÔNG có cột đối tượng.\n"
     "- Phiếu lưu thành công ở 'Chờ TP duyệt'; cột 'Khách hàng / Nhà cung cấp' trên lưới hiện "
     "nhà cung cấp X.\n"
     "- Bản in có khối ngân hàng và file đính kèm hiện ở màn chi tiết."),

    (5, "Luồng phiếu vận chuyển nhiều chuyến xe", "P0",
     "Nhà cung cấp Z có ít nhất 3 chuyến xe phát sinh trước ngày chọn.",
     "1. Tạo mới, Loại chi 'Thanh toán chi phí vận chuyển NCC', chọn nhà cung cấp Z, chọn "
     "'Đến ngày'.\n"
     "2. Bấm 'Lấy dữ liệu'.\n3. Tích 2 dòng, nhập số tiền cho 2 dòng đó.\n"
     "4. Nhập Lý do chi, bấm 'Lưu và gửi duyệt' và xác nhận.\n5. Mở chi tiết và bản in.",
     "2 dòng có tích",
     "- Bảng sinh dòng theo chuyến xe, không thêm/xóa dòng bằng tay được.\n"
     "- Phiếu lưu thành công; bảng chi tiết ở màn xem giữ đủ cột chuyến xe.\n"
     "- Bản in in đúng nhóm cột của loại vận chuyển và có dòng 'Đến ngày'."),

    (6, "Luồng lập nháp rồi xóa", "P1",
     "Tài khoản A đang ở màn danh sách.",
     "1. Tạo mới, chỉ nhập Lý do chi, bấm 'Lưu nháp'.\n2. Ghi lại mã phiếu vừa sinh.\n"
     "3. Xóa phiếu đó.\n4. Tạo mới thêm 1 phiếu và bấm 'Lưu nháp'.",
     "—",
     "- Phiếu nháp tạo và xóa được bình thường.\n"
     "- ⚠️ Mã phiếu mới KHÔNG dùng lại số vừa xóa mà tiếp tục số kế tiếp."),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & 4 CHẾ ĐỘ XEM", S1),
    ("II", "BỘ LỌC & TÌM KIẾM", S2),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", S3),
    ("IV", "LẬP PHIẾU — THÔNG TIN CHUNG", S4),
    ("V", "LẬP PHIẾU — BẢNG CHI TIẾT THEO LOẠI CHI", S5),
    ("VI", "KHỐI THÔNG TIN NGÂN HÀNG", S6),
    ("VII", "FILE ĐÍNH KÈM", S7),
    ("VIII", "RÀNG BUỘC NHẬP LIỆU KHI LƯU", S8),
    ("IX", "SỬA PHIẾU", S9),
    ("X", "XEM CHI TIẾT PHIẾU", S10),
    ("XI", "LUỒNG DUYỆT 5 CẤP", S11),
    ("XII", "TỪ CHỐI PHIẾU", S12),
    ("XIII", "XÓA · IN · XUẤT EXCEL", S13),
    ("XIV", "LỊCH SỬ THAY ĐỔI & THAO TÁC ĐỒNG THỜI", S14),
    ("XV", "LUỒNG NGHIỆP VỤ TRỌN VẸN", S15),
]

if __name__ == "__main__":
    build(output_file=OUT,
          sheet_name="Trang tính1",
          feature_name="Phiếu đề nghị thanh toán - Cập nhật ngày 28/08/2026",
          module_name=MODULE,
          description_block=DESCRIPTION_BLOCK,
          role_tcs=ROLE_TCS,
          sections=SECTIONS)
