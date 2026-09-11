# -*- coding: utf-8 -*-
"""Sinh file testcase Excel cho man "Phieu de nghi thu tien" (phan he Tai chinh).

Nguon doc code 28/08/2026 (nhanh gop_db):
  BE  Modules/Finance/Routes/api.php (:220-245)
      Modules/Finance/Http/Controllers/V1/BillIncomeRequestController.php
      Modules/Finance/Services/BillIncomeRequestService.php
      Modules/Finance/Entities/BillIncomeRequest/BillIncomeRequest.php
      Modules/Finance/Http/Requests/BillIncomeRequest/*.php  (nguyen van thong bao loi)
      Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (:1152-1156)
  FE  hrm-client/pages/finance/bill-income-requests/{index,pending,create}.vue
      .../_id/{index,edit,print}.vue
      .../components/{BillIncomeRequestForm,ContractSearchModal,SupplierSearchModal}.vue
  Anh that: dntt_shots/ (cong dev hrm-crm.eteksofts.com, 28/08/2026)

Chay:  python .plans/gop-db/finance-bill-income-request/gen_testcase.py
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

OUT = os.path.join(HERE, "testcase - Phiếu đề nghị thu tiền.xlsx")
MODULE = "Phiếu đề nghị thu tiền"

# ════════════════════════════════════════════════════ 1. KHỐI MÔ TẢ (9 mục)
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Phiếu đề nghị thu tiền là chứng từ do người kinh doanh lập để đề nghị kế toán thu tiền "
     "của khách hàng theo một hoặc nhiều hợp đồng. Màn hình cho phép: lập phiếu (lưu nháp hoặc "
     "gửi duyệt), sửa, xóa, xem chi tiết, in, xem lịch sử thay đổi. Kế toán thanh toán có thêm "
     "màn 'Phiếu đề nghị thu tiền chờ duyệt' để xử lý phiếu: đồng ý thì bấm 'Tạo phiếu thu', "
     "không đồng ý thì bấm 'Không duyệt' kèm lý do.\n"
     "Có 2 lối vào cùng một màn danh sách: menu Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi > "
     "Đề nghị thu tiền, và menu Đề nghị > Đề nghị thu tiền. Màn chờ duyệt nằm ở menu "
     "Phê duyệt - Công nợ - Thu - Chi > Phiếu đề nghị thu tiền chờ duyệt."),

    ("2. Đối tượng được tính / hiển thị",
     "Màn danh sách hiển thị phiếu đề nghị thu tiền theo phạm vi quyền của người đăng nhập:\n"
     "- Có quyền 'Xem tất cả phiếu đề nghị thu của tổng công ty' (hoặc là quản trị hệ thống): "
     "thấy phiếu của mọi công ty.\n"
     "- Có quyền 'Xem tất cả phiếu đề nghị thu của công ty': chỉ phiếu thuộc công ty mình.\n"
     "- Có quyền 'Xem tất cả phiếu đề nghị thu của phòng ban': chỉ phiếu thuộc các phòng ban "
     "mà mình được giao quản lý trong công ty mình.\n"
     "- Có quyền 'Xem tất cả phiếu đề nghị thu của bộ phận': chỉ phiếu thuộc các bộ phận mà "
     "mình được giao quản lý trong công ty mình.\n"
     "- Không có quyền nào trong 4 quyền trên: chỉ thấy phiếu do chính mình lập.\n"
     "Đủ 6 trạng thái đều hiển thị: Đang tạo, Chờ KT duyệt, Đã tạo phiếu thu, Đã hạch toán, "
     "Hủy, Không duyệt.\n"
     "Màn 'chờ duyệt' chỉ hiển thị phiếu ở trạng thái Chờ KT duyệt và thuộc công ty của người "
     "đăng nhập."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu ở trạng thái Đang tạo (nháp) của NGƯỜI KHÁC luôn bị ẩn, kể cả với người có quyền "
     "xem toàn tổng công ty. Người lập chỉ nhìn thấy nháp của chính mình.\n"
     "- Màn chờ duyệt bỏ hết phiếu khác trạng thái Chờ KT duyệt, và bỏ phiếu của công ty khác "
     "(kể cả người xem có quyền xem tổng công ty).\n"
     "- Loại thu 'Thu khác' không còn cho chọn khi lập phiếu mới; phiếu cũ mang loại này vẫn "
     "hiển thị đúng tên trên lưới.\n"
     "- Popup chọn hợp đồng bán chỉ lấy hợp đồng bán từ trạng thái 'Có hiệu lực' trở lên "
     "(gồm cả Đang xuất hàng, Đã xuất hàng, Đã thanh lý, Đang quyết toán, Đã quyết toán); "
     "hợp đồng còn nháp, chờ duyệt, đã duyệt chưa hiệu lực, chờ hiệu lực đều không hiện.\n"
     "- Hợp đồng đã được chọn ở một dòng khác trong cùng phiếu thì popup vẫn hiện nhưng không "
     "bấm chọn lại được."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Hai ô 'Ngày tạo từ' và 'Ngày tạo đến' lọc theo NGÀY TẠO PHIẾU (cột Ngày tạo trên lưới), "
     "không phải ngày cập nhật và cũng không phải ngày ký hợp đồng.\n"
     "Cả 2 mốc đều lấy trọn ngày: chọn 'đến ngày' là ngày hôm nay thì phiếu vừa lập sáng nay "
     "vẫn nằm trong kết quả. Bỏ trống một trong hai ô thì phía đó không giới hạn."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Một phiếu gồm 2 tầng:\n"
     "- Thông tin chung: Mã phiếu, Loại thu, Loại tiền, Tỷ giá, Lý do thu, Ghi chú, Người tạo, "
     "Phòng ban, Trạng thái.\n"
     "- Bảng Chi tiết: nhiều dòng, MỖI DÒNG chọn riêng một khách hàng (hoặc nhà cung cấp) và "
     "một hợp đồng của chính đối tượng đó, kèm Số tiền còn nợ, Số tiền đề nghị thu, Ghi chú. "
     "Một phiếu được phép gom nhiều khách hàng và nhiều hợp đồng.\n"
     "Loại thu quyết định nguồn dữ liệu của bảng chi tiết: 'Thu bán hàng' chọn khách hàng và "
     "hợp đồng bán; 'Thu nhà cung cấp' chọn nhà cung cấp và hợp đồng mua. Đổi loại thu thì "
     "toàn bộ dòng chi tiết đang có bị xóa (có hỏi xác nhận trước)."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Dòng 'Tổng cộng' dưới bảng chi tiết cộng dồn tại chỗ trên màn hình, đổi ngay theo từng "
     "phím gõ: tổng Số tiền còn nợ, tổng Số tiền đề nghị thu, và tổng cột quy đổi khi dùng "
     "ngoại tệ.\n"
     "- Cột 'Tổng tiền đề nghị' trên lưới danh sách = tổng số tiền đề nghị thu (đã quy đổi về "
     "VND) của tất cả dòng chi tiết trong phiếu.\n"
     "- Cột 'Khách hàng / Nhà cung cấp' trên lưới lấy đối tượng của DÒNG CHI TIẾT ĐẦU TIÊN; "
     "phiếu nhiều khách hàng vẫn chỉ hiện một tên ở cột này.\n"
     "- Một hợp đồng chỉ được chọn một lần trong cùng một phiếu.\n"
     "- Số tiền còn nợ KHÔNG lưu vào phiếu mà tính lại theo sổ kế toán mỗi lần mở phiếu, nên "
     "số này có thể khác nhau giữa 2 lần xem nếu sổ có phát sinh mới."),

    ("7. Phân quyền cấp",
     "Năm quyền liên quan tới màn (tên nguyên văn trong hệ thống phân quyền):\n"
     "- Xem tất cả phiếu đề nghị thu của tổng công ty\n"
     "- Xem tất cả phiếu đề nghị thu của công ty\n"
     "- Xem tất cả phiếu đề nghị thu của phòng ban\n"
     "- Xem tất cả phiếu đề nghị thu của bộ phận\n"
     "- Kế toán thanh toán\n"
     "Bốn quyền đầu chỉ quyết định PHẠM VI DỮ LIỆU nhìn thấy, xét theo đúng thứ tự trên "
     "(ai có nhiều quyền thì lấy quyền rộng nhất). Quyền 'Kế toán thanh toán' mở màn chờ duyệt, "
     "nút 'Không duyệt' và nút 'Tạo phiếu thu'.\n"
     "Việc lập phiếu KHÔNG gắn quyền: ai vào được màn cũng lập được phiếu của mình (giữ nguyên "
     "cách làm của hệ thống cũ). Sửa và xóa chỉ áp cho phiếu do chính mình lập."),

    ("8. Cách tính các ô thống kê",
     "- Ô 'Hiển thị a–b / N' dưới lưới: a là số thứ tự dòng đầu của trang đang xem, b là dòng "
     "cuối của trang, N là tổng số phiếu khớp bộ lọc hiện tại (không phải tổng toàn hệ thống).\n"
     "- Ô 'Số dòng/trang': đổi giá trị thì quay về trang 1 và tải lại danh sách.\n"
     "- Cột 'Tổng tiền đề nghị' = cộng số tiền đề nghị thu quy đổi VND của mọi dòng chi tiết.\n"
     "- Bảng chi tiết, cột quy đổi VND của mỗi dòng = Số tiền đề nghị thu × Tỷ giá. Chọn loại "
     "tiền VND thì tỷ giá luôn bằng 1 và cột quy đổi không hiện.\n"
     "- Số tiền còn nợ = số dư công nợ của hợp đồng đó theo sổ kế toán tại thời điểm mở phiếu."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất của màn:\n"
     "- Ô tìm nhanh (Tìm theo mã phiếu) CHỜ bấm nút 'Tìm kiếm' mới lọc; mọi tiêu chí trong "
     "'Tìm kiếm nâng cao' lọc ngay khi vừa đổi giá trị. Đừng báo lỗi vì ô tìm nhanh 'không tự "
     "chạy'.\n"
     "- Hệ thống nhớ bộ lọc trong 10 phút khi bấm vào một phiếu rồi quay lại. Muốn kiểm thử "
     "trạng thái sạch thì bấm 'Làm mới' trước.\n"
     "- Bộ tiêu chí lọc và bộ cột hiển thị lưu RIÊNG cho từng tài khoản (nút 'Cài đặt bộ lọc' "
     "và nút 'Tuỳ chỉnh cột'). Người kiểm thử thấy thiếu tiêu chí/cột thì mở 2 popup đó xem "
     "đã tắt hay chưa, đừng vội kết luận thiếu chức năng.\n"
     "- Lưu nháp và Lưu và gửi duyệt KHÁC nhau về ràng buộc: lưu nháp cho phép bỏ trống Lý do "
     "thu và chưa có dòng chi tiết nào; gửi duyệt thì bắt buộc cả hai.\n"
     "- Đổi loại thu sẽ XÓA SẠCH dòng chi tiết đã chọn — hộp xác nhận hiện ra sau khi ô Loại "
     "thu đã đổi nhãn, bấm Hủy thì dòng chi tiết được giữ nguyên.\n"
     "- Số tiền hiển thị theo kiểu 1,234,567 (dấu phẩy ngăn nghìn).\n"
     "- Số tiền còn nợ của hợp đồng mới lập bên hệ thống nhân sự thường bằng 0 vì chưa có bút "
     "toán kế toán — đây là hiện trạng đã được chấp nhận, không phải lỗi.\n"
     "- Trạng thái 'Đã tạo phiếu thu', 'Đã hạch toán', 'Hủy' KHÔNG đặt từ màn này mà do màn "
     "Phiếu thu đặt; màn này chỉ hiển thị."),
]

# ════════════════════════════════════════════════════ 2. TC PHÂN QUYỀN
ROLE_TCS = [
    ("00", "Người dùng không có quyền xem nào — chỉ thấy phiếu của chính mình", "P0",
     "Tài khoản A thuộc công ty 1, phòng Kinh doanh 1, KHÔNG có bất kỳ quyền nào trong nhóm "
     "'Xem tất cả phiếu đề nghị thu…'. Dữ liệu: A đã lập 3 phiếu (1 Đang tạo, 2 Chờ KT duyệt); "
     "người khác cùng phòng đã lập 5 phiếu Chờ KT duyệt.",
     "1. Đăng nhập bằng tài khoản A.\n"
     "2. Vào menu Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi > Đề nghị thu tiền.\n"
     "3. Đọc dòng 'Hiển thị a–b / N' dưới lưới và cột Người tạo.",
     "—",
     "- Danh sách chỉ có đúng 3 phiếu, cột Người tạo đều là tài khoản A.\n"
     "- Tổng số phiếu là 3, không thấy 5 phiếu của người khác.\n"
     "- Vẫn có nút 'Tạo mới' (việc lập phiếu không gắn quyền).\n"
     "- ⚠️ Bộ lọc nâng cao KHÔNG hiện ô Công ty / Phòng ban / Bộ phận."),

    ("01", "Quyền 'Xem tất cả phiếu đề nghị thu của bộ phận'", "P0",
     "Tài khoản B chỉ có quyền 'Xem tất cả phiếu đề nghị thu của bộ phận', được giao quản lý "
     "bộ phận 'Tổ kỹ thuật 1' của công ty 1. Dữ liệu: 4 phiếu thuộc bộ phận này (đã gửi duyệt), "
     "6 phiếu thuộc bộ phận khác cùng công ty.",
     "1. Đăng nhập bằng tài khoản B.\n"
     "2. Mở màn Đề nghị thu tiền.\n"
     "3. Mở 'Tìm kiếm nâng cao' và quan sát các ô cấp tổ chức.",
     "—",
     "- Danh sách đúng 4 phiếu của bộ phận được giao, không có phiếu của bộ phận khác.\n"
     "- Bộ lọc có ô 'Bộ phận' để chọn, không có ô Công ty.\n"
     "- ⚠️ Phiếu Đang tạo của người khác trong cùng bộ phận vẫn KHÔNG hiện."),

    ("02", "Quyền 'Xem tất cả phiếu đề nghị thu của phòng ban'", "P0",
     "Tài khoản C chỉ có quyền 'Xem tất cả phiếu đề nghị thu của phòng ban', được giao quản lý "
     "phòng 'Kinh doanh 1' và 'Kinh doanh 2' của công ty 1. Dữ liệu: 7 phiếu thuộc 2 phòng này, "
     "9 phiếu thuộc phòng khác cùng công ty.",
     "1. Đăng nhập bằng tài khoản C.\n"
     "2. Mở màn Đề nghị thu tiền.\n"
     "3. Đọc cột Phòng ban của toàn bộ danh sách.",
     "—",
     "- Chỉ có 7 phiếu, cột Phòng ban chỉ chứa 'Kinh doanh 1' hoặc 'Kinh doanh 2'.\n"
     "- Bộ lọc có ô 'Phòng ban', không có ô 'Công ty'."),

    ("03", "Quyền 'Xem tất cả phiếu đề nghị thu của công ty'", "P0",
     "Tài khoản D chỉ có quyền 'Xem tất cả phiếu đề nghị thu của công ty', thuộc công ty 1. "
     "Dữ liệu: 20 phiếu công ty 1 (đã gửi duyệt), 15 phiếu công ty 4.",
     "1. Đăng nhập bằng tài khoản D.\n"
     "2. Mở màn Đề nghị thu tiền.\n"
     "3. Mở 'Tìm kiếm nâng cao'.",
     "—",
     "- Thấy 20 phiếu của công ty 1, không thấy phiếu công ty 4.\n"
     "- Bộ lọc hiện ô 'Phòng ban' (và 'Bộ phận' nếu có thêm quyền cấp bộ phận), không hiện ô "
     "'Công ty' vì phạm vi đã bị khóa trong 1 công ty."),

    ("04", "Quyền 'Xem tất cả phiếu đề nghị thu của tổng công ty'", "P0",
     "Tài khoản E có quyền 'Xem tất cả phiếu đề nghị thu của tổng công ty'. Dữ liệu: hệ thống "
     "có phiếu của ít nhất 2 công ty khác nhau.",
     "1. Đăng nhập bằng tài khoản E.\n"
     "2. Mở màn Đề nghị thu tiền.\n"
     "3. Mở 'Tìm kiếm nâng cao', chọn lần lượt từng công ty ở ô 'Công ty'.",
     "Công ty: chọn từng giá trị trong danh sách",
     "- Danh sách gồm phiếu của mọi công ty.\n"
     "- Bộ lọc hiện đủ ô Công ty, Phòng ban, Bộ phận.\n"
     "- Chọn 1 công ty thì danh sách rút lại đúng phiếu của công ty đó."),

    ("05", "Người có nhiều quyền xem cùng lúc — lấy phạm vi rộng nhất", "P1",
     "Tài khoản F có ĐỒNG THỜI 'Xem tất cả phiếu đề nghị thu của công ty' và 'Xem tất cả phiếu "
     "đề nghị thu của phòng ban', thuộc công ty 1, quản lý 1 phòng.",
     "1. Đăng nhập bằng tài khoản F.\n"
     "2. Mở màn Đề nghị thu tiền.\n"
     "3. Đếm số phiếu và đối chiếu với tổng số phiếu của công ty 1.",
     "—",
     "- Thấy toàn bộ phiếu của công ty 1, không bị bó lại trong 1 phòng ban.\n"
     "- ⚠️ Quyền rộng hơn phải thắng, không được lấy giao của 2 phạm vi."),

    ("06", "Quyền 'Kế toán thanh toán' — vào được màn chờ duyệt", "P0",
     "Tài khoản G có quyền 'Kế toán thanh toán', thuộc công ty 1. Dữ liệu: công ty 1 có 7 phiếu "
     "ở trạng thái Chờ KT duyệt; công ty 4 có 3 phiếu Chờ KT duyệt.",
     "1. Đăng nhập bằng tài khoản G.\n"
     "2. Vào menu Phê duyệt - Công nợ - Thu - Chi > Phiếu đề nghị thu tiền chờ duyệt.\n"
     "3. Đọc cột Trạng thái và tổng số bản ghi.",
     "—",
     "- Mục menu 'Phiếu đề nghị thu tiền chờ duyệt' có hiển thị.\n"
     "- Danh sách đúng 7 phiếu, tất cả đều ở trạng thái Chờ KT duyệt.\n"
     "- ⚠️ Không có phiếu nào của công ty 4 dù người dùng có thể có quyền xem tổng công ty.\n"
     "- Thanh công cụ KHÔNG có nút 'Tạo mới'."),

    ("07", "Không có quyền 'Kế toán thanh toán' — không vào được màn chờ duyệt", "P0",
     "Tài khoản A (không có quyền 'Kế toán thanh toán') đã đăng nhập.",
     "1. Quan sát menu Phê duyệt - Công nợ - Thu - Chi.\n"
     "2. Gõ thẳng đường dẫn /finance/bill-income-requests/pending vào trình duyệt.",
     "—",
     "- Mục 'Phiếu đề nghị thu tiền chờ duyệt' KHÔNG hiển thị trong menu.\n"
     "- Truy cập thẳng đường dẫn: màn mở ra nhưng bảng rỗng, hệ thống không trả về phiếu nào và "
     "không treo trang."),

    ("08", "Không có quyền 'Kế toán thanh toán' — không thấy nút Không duyệt", "P0",
     "Tài khoản A đã đăng nhập. Có sẵn 1 phiếu Chờ KT duyệt mà A được phép xem (do A lập).",
     "1. Mở chi tiết phiếu Chờ KT duyệt đó.\n"
     "2. Quan sát thanh nút phía dưới màn hình.",
     "—",
     "- KHÔNG có nút 'Không duyệt' và KHÔNG có nút 'Tạo phiếu thu'.\n"
     "- Chỉ còn 'In phiếu' và 'Quay lại' (phiếu đã gửi duyệt nên cũng không còn nút Sửa/Xóa)."),

    ("09", "Chặn bỏ qua giao diện — không duyệt phiếu khi không phải kế toán", "P0",
     "Tài khoản A (không có quyền 'Kế toán thanh toán'). Phiếu số hiệu TEST.DNTT.00062 đang ở "
     "trạng thái Chờ KT duyệt.",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Không duyệt cho phiếu TEST.DNTT.00062, "
     "bỏ qua giao diện, bằng phiên đăng nhập của tài khoản A.\n"
     "2. Mở lại chi tiết phiếu trên giao diện.",
     "Lý do không duyệt: 'thử bỏ qua giao diện'",
     "- Hệ thống từ chối, báo không có quyền duyệt phiếu đề nghị thu.\n"
     "- Trạng thái phiếu vẫn là Chờ KT duyệt, không có dòng lịch sử đổi trạng thái nào sinh ra.\n"
     "- ⚠️ Nhóm test này dành cho tester kỹ thuật."),

    ("10", "Chặn bỏ qua giao diện — không sửa/xóa được phiếu của người khác", "P0",
     "Tài khoản A đã đăng nhập. Phiếu P do tài khoản khác lập, đang ở trạng thái Đang tạo.",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Sửa cho phiếu P, bỏ qua giao diện.\n"
     "2. Làm tương tự với chức năng Xóa.\n"
     "3. Mở lại danh sách của người lập phiếu P.",
     "Lý do thu: 'sửa trộm'",
     "- Cả 2 lần hệ thống đều từ chối, báo không có quyền sửa / xóa phiếu này.\n"
     "- Phiếu P còn nguyên, nội dung không đổi."),
]

# ════════════════════════════════════════════════════ 3. SECTIONS
S1 = [
    (1, "Mở màn danh sách từ menu Khởi tạo", "P0",
     "Tài khoản có ít nhất 1 phiếu để nhìn thấy dữ liệu.",
     "1. Đăng nhập.\n2. Chọn phân hệ Tài chính.\n"
     "3. Bấm menu 'Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi'.\n"
     "4. Bấm 'Đề nghị thu tiền'.",
     "—",
     "- Tiêu đề trang là 'Phiếu đề nghị thu tiền'.\n"
     "- Có khối 'Bộ lọc danh sách' phía trên và bảng danh sách phía dưới.\n"
     "- Thanh công cụ của bảng có nút 'Tạo mới' và nút hình 2 cột (Cấu hình cột hiển thị)."),

    (2, "Mở màn danh sách từ menu Đề nghị", "P1",
     "Như trên.",
     "1. Bấm menu 'Đề nghị'.\n2. Bấm 'Đề nghị thu tiền'.",
     "—",
     "- Mở đúng màn 'Phiếu đề nghị thu tiền', nội dung y hệt lối vào ở menu Khởi tạo."),

    (3, "Danh sách hiển thị đủ các cột mặc định", "P0",
     "Tài khoản chưa từng tuỳ chỉnh cột ở màn này.",
     "1. Mở màn Đề nghị thu tiền.\n2. Cuộn ngang bảng từ trái sang phải.",
     "—",
     "- Có đủ các cột theo thứ tự: STT, Mã phiếu, Loại thu, Khách hàng / Nhà cung cấp, "
     "Lý do thu, Phòng ban, Tổng tiền đề nghị, Người tạo, Ngày tạo, Người cập nhật, "
     "Ngày cập nhật, Trạng thái, Hành động.\n"
     "- ⚠️ Màn KHÔNG có cột 'Người nộp' (đã bỏ hẳn)."),

    (4, "Cột Mã phiếu là liên kết mở chi tiết", "P0",
     "Danh sách có ít nhất 1 phiếu.",
     "1. Bấm vào mã phiếu ở dòng đầu tiên.\n"
     "2. Quay lại danh sách, bấm chuột phải vào mã phiếu chọn mở ở tab mới.",
     "—",
     "- Bấm trái: mở màn chi tiết đúng phiếu đó, tiêu đề trang là "
     "'Chi tiết phiếu đề nghị thu tiền: <mã phiếu>'.\n"
     "- Bấm phải: mở được ở tab mới.\n"
     "- ⚠️ Cột Hành động KHÔNG có nút 'Xem chi tiết' riêng — vào chi tiết bằng liên kết mã phiếu."),

    (5, "Màu và chữ của cột Trạng thái", "P1",
     "Có sẵn phiếu ở đủ các trạng thái: Đang tạo, Chờ KT duyệt, Đã tạo phiếu thu, Đã hạch toán, "
     "Hủy, Không duyệt.",
     "1. Mở màn danh sách.\n2. Đối chiếu từng dòng ở cột Trạng thái.",
     "—",
     "- 'Đã tạo phiếu thu' và 'Đã hạch toán' hiển thị nền xanh kèm dấu tích.\n"
     "- 'Đang tạo', 'Chờ KT duyệt', 'Hủy', 'Không duyệt' hiển thị nền đỏ kèm biểu tượng đồng hồ.\n"
     "- Chữ trong ô đúng nguyên văn 6 trạng thái nêu trên."),

    (6, "Bảng rỗng khi bộ lọc không khớp phiếu nào", "P1",
     "Tài khoản có dữ liệu.",
     "1. Mở 'Tìm kiếm nâng cao'.\n"
     "2. Nhập 'Số đơn hàng/hợp đồng' = 'ZZZZZZZZZ'.",
     "Số đơn hàng/hợp đồng: ZZZZZZZZZ",
     "- Bảng hiện dòng chữ 'Không có dữ liệu phù hợp bộ lọc.'\n"
     "- Dòng đếm dưới bảng hiện tổng bằng 0, không báo lỗi đỏ."),

    (7, "Màn chờ duyệt dùng chung khuôn với màn danh sách", "P1",
     "Tài khoản có quyền 'Kế toán thanh toán', công ty có ít nhất 1 phiếu Chờ KT duyệt.",
     "1. Mở màn 'Phiếu đề nghị thu tiền chờ duyệt'.\n"
     "2. So sánh bộ cột và bộ tiêu chí lọc với màn danh sách.",
     "—",
     "- Tiêu đề trang là 'Phiếu đề nghị thu tiền chờ duyệt'.\n"
     "- Bộ cột và bộ tiêu chí lọc giống hệt màn danh sách.\n"
     "- ⚠️ Không có nút 'Tạo mới'; cột Hành động không có nút Sửa và nút Xóa."),
]

S2 = [
    (1, "Tìm nhanh theo mã phiếu — phải bấm nút Tìm kiếm", "P0",
     "Có phiếu mã TPE.DNTT0826.00009.",
     "1. Gõ 'DNTT0826' vào ô 'Tìm theo mã phiếu...'.\n"
     "2. Quan sát bảng trước khi bấm nút.\n"
     "3. Bấm nút 'Tìm kiếm'.",
     "Ô tìm nhanh: DNTT0826",
     "- ⚠️ Trước khi bấm nút: danh sách KHÔNG đổi (đúng thiết kế).\n"
     "- Sau khi bấm: chỉ còn phiếu có mã chứa 'DNTT0826', quay về trang 1."),

    (2, "Tìm nhanh không phân biệt vị trí chuỗi trong mã", "P1",
     "Có phiếu mã TEST.DNTT.00061.",
     "1. Gõ '00061' vào ô tìm nhanh.\n2. Bấm 'Tìm kiếm'.",
     "Ô tìm nhanh: 00061",
     "- Phiếu TEST.DNTT.00061 vẫn ra kết quả dù chuỗi nằm ở cuối mã."),

    (3, "Nút Làm mới xóa sạch mọi tiêu chí", "P0",
     "Đang có 3 tiêu chí đang lọc: Loại thu = Thu bán hàng, Trạng thái = Chờ KT duyệt, "
     "ô tìm nhanh = 'DNTT'.",
     "1. Bấm nút 'Làm mới'.\n2. Quan sát các ô lọc và bảng.",
     "—",
     "- Mọi ô lọc trở về trống, ô tìm nhanh trống.\n"
     "- Bảng tải lại toàn bộ danh sách theo phạm vi quyền, về trang 1."),

    (4, "Lọc theo Loại thu", "P0",
     "Có cả phiếu 'Thu bán hàng' và phiếu 'Thu nhà cung cấp'.",
     "1. Mở 'Tìm kiếm nâng cao'.\n2. Chọn Loại thu = 'Thu nhà cung cấp'.",
     "Loại thu: Thu nhà cung cấp",
     "- Danh sách tự lọc NGAY khi chọn, không cần bấm 'Tìm kiếm'.\n"
     "- Mọi dòng đều có cột Loại thu = 'Thu nhà cung cấp'.\n"
     "- ⚠️ Danh sách chọn chỉ có 2 giá trị: Thu bán hàng, Thu nhà cung cấp (không có Thu khác)."),

    (5, "Lọc theo Trạng thái", "P0",
     "Có phiếu ở đủ 6 trạng thái.",
     "1. Chọn Trạng thái = 'Không duyệt'.\n2. Đổi sang 'Đã hạch toán'.",
     "Trạng thái: Không duyệt → Đã hạch toán",
     "- Mỗi lần chọn, danh sách chỉ còn phiếu đúng trạng thái đó.\n"
     "- Danh sách chọn có đủ 6 giá trị."),

    (6, "Lọc theo Số đơn hàng/hợp đồng", "P0",
     "Có phiếu chứa dòng chi tiết gắn hợp đồng số 'HĐ-TEST-DNTT-02'.",
     "1. Nhập 'HĐ-TEST-DNTT' vào ô 'Số đơn hàng/hợp đồng'.",
     "Số đơn hàng/hợp đồng: HĐ-TEST-DNTT",
     "- Chỉ còn phiếu có ít nhất một dòng chi tiết gắn hợp đồng khớp chuỗi này.\n"
     "- ⚠️ Ô này lọc theo hợp đồng nằm TRONG dòng chi tiết, không phải mã phiếu."),

    (7, "Lọc theo Khách hàng bằng mã", "P0",
     "Có phiếu của khách hàng mã 29TPHPTH-1.",
     "1. Nhập '29TPHPTH-1' vào ô 'Khách hàng'.",
     "Khách hàng: 29TPHPTH-1",
     "- Chỉ còn phiếu có dòng chi tiết thuộc khách hàng đó."),

    (8, "Lọc theo Khách hàng bằng tên", "P1",
     "Khách hàng 29TPHPTH-1 tên là 'CÔNG TY CỔ PHẦN GIẢI PHÁP ETEK GREEN'.",
     "1. Nhập 'ETEK GREEN' vào ô 'Khách hàng'.",
     "Khách hàng: ETEK GREEN",
     "- Vẫn ra đúng nhóm phiếu của khách hàng đó (ô này tìm được cả theo mã lẫn theo tên)."),

    (9, "Lọc theo Nhà cung cấp", "P0",
     "Có phiếu 'Thu nhà cung cấp' gắn nhà cung cấp 0104509916 - CÔNG TY CỔ PHẦN CÔNG NGHỆ "
     "HỢP LONG.",
     "1. Bấm vào ô 'Nhà cung cấp'.\n"
     "2. Gõ 'HỢP LONG' (ít nhất 2 ký tự) và chờ danh sách gợi ý.\n"
     "3. Chọn nhà cung cấp trong danh sách gợi ý.",
     "Nhà cung cấp: HỢP LONG",
     "- Danh sách gợi ý hiện dạng 'mã - tên'.\n"
     "- Sau khi chọn, danh sách chỉ còn phiếu gắn nhà cung cấp đó.\n"
     "- ⚠️ Gõ dưới 2 ký tự thì chưa gợi ý gì."),

    (10, "Lọc theo Người tạo", "P1",
     "Có phiếu của ít nhất 2 người tạo khác nhau trong phạm vi xem.",
     "1. Chọn một người ở ô 'Người tạo'.",
     "Người tạo: chọn 1 nhân sự",
     "- Cột Người tạo của mọi dòng đều là người đã chọn."),

    (11, "Lọc theo khoảng Số tiền đề nghị", "P0",
     "Có phiếu tổng tiền 8,000,000 và phiếu tổng tiền 50,000,000.",
     "1. Nhập 'Số tiền đề nghị từ' = 10,000,000.\n"
     "2. Nhập 'Số tiền đề nghị đến' = 60,000,000.",
     "Số tiền đề nghị từ: 10.000.000 · đến: 60.000.000",
     "- Phiếu 50,000,000 còn trong danh sách, phiếu 8,000,000 bị loại.\n"
     "- ⚠️ Ngưỡng so trên TỔNG tiền đề nghị quy đổi của cả phiếu, không phải từng dòng."),

    (12, "Lọc khoảng số tiền chỉ nhập một đầu", "P1",
     "Như trên.",
     "1. Chỉ nhập 'Số tiền đề nghị từ' = 10,000,000, để trống ô đến.",
     "Số tiền đề nghị từ: 10.000.000",
     "- Mọi phiếu có tổng tiền từ 10,000,000 trở lên đều hiện, không bị chặn trên."),

    (13, "Lọc theo khoảng Ngày tạo", "P0",
     "Có phiếu lập ngày 19/08/2026 và phiếu lập ngày 25/08/2026.",
     "1. Chọn 'Ngày tạo từ' = 20/08/2026.\n2. Chọn 'Ngày tạo đến' = 25/08/2026.",
     "Ngày tạo từ: 20/08/2026 · đến: 25/08/2026",
     "- Phiếu ngày 25/08/2026 CÒN trong kết quả (mốc 'đến' lấy trọn ngày).\n"
     "- Phiếu ngày 19/08/2026 bị loại."),

    (14, "Lọc theo Công ty / Phòng ban / Bộ phận", "P0",
     "Tài khoản có quyền 'Xem tất cả phiếu đề nghị thu của tổng công ty'. Hệ thống có phiếu ở "
     "ít nhất 2 công ty.",
     "1. Chọn 'Công ty' = công ty 1.\n"
     "2. Chọn tiếp 'Phòng ban' = một phòng của công ty 1.\n"
     "3. Đổi 'Công ty' sang công ty khác.",
     "Công ty: công ty 1 → công ty khác",
     "- Ô Phòng ban chỉ liệt kê phòng của công ty đang chọn.\n"
     "- ⚠️ Đổi công ty thì ô Phòng ban và Bộ phận tự xóa giá trị cũ, không lọc ngầm."),

    (15, "Kết hợp nhiều tiêu chí", "P0",
     "Có phiếu 'Thu bán hàng' trạng thái 'Đã hạch toán' của khách hàng ETEK GREEN.",
     "1. Chọn Loại thu = Thu bán hàng.\n"
     "2. Chọn Trạng thái = Đã hạch toán.\n"
     "3. Nhập Khách hàng = 'ETEK GREEN'.",
     "3 tiêu chí như bước thực hiện",
     "- Kết quả thỏa ĐỒNG THỜI cả 3 tiêu chí.\n"
     "- Số bản ghi giảm dần sau mỗi lần thêm tiêu chí."),

    (16, "Popup 'Cài đặt bộ lọc' liệt kê đủ 9 tiêu chí", "P0",
     "Tài khoản bất kỳ.",
     "1. Bấm nút 'Cài đặt bộ lọc'.\n2. Đọc danh sách tiêu chí.",
     "—",
     "- Popup 'Cài đặt bộ lọc' liệt kê đúng 9 mục: Công ty – Phòng ban – Bộ phận, Loại thu, "
     "Trạng thái, Số đơn hàng/hợp đồng, Khách hàng, Nhà cung cấp, Người tạo, "
     "Số tiền đề nghị (từ – đến), Khoảng ngày tạo.\n"
     "- Có nút 'Lưu', 'Khôi phục mặc định', 'Đóng'."),

    (17, "Bỏ tích một tiêu chí thì tiêu chí đó biến mất khỏi bộ lọc", "P0",
     "Đang mở popup 'Cài đặt bộ lọc'.",
     "1. Bỏ tích 'Khoảng ngày tạo'.\n2. Bấm 'Lưu'.\n3. Mở lại 'Tìm kiếm nâng cao'.",
     "Bỏ tích: Khoảng ngày tạo",
     "- Thông báo cập nhật thành công.\n"
     "- Hai ô 'Ngày tạo từ' và 'Ngày tạo đến' không còn hiển thị.\n"
     "- ⚠️ Giá trị đang lọc của 2 ô đó cũng bị xóa, danh sách không bị lọc ngầm."),

    (18, "Nút Khôi phục mặc định của Cài đặt bộ lọc", "P1",
     "Đang tắt bớt vài tiêu chí lọc.",
     "1. Mở 'Cài đặt bộ lọc'.\n2. Bấm 'Khôi phục mặc định'.\n3. Bấm 'Lưu'.",
     "—",
     "- Toàn bộ 9 tiêu chí được tích lại.\n"
     "- Bộ lọc nâng cao hiện đủ 9 tiêu chí."),

    (19, "Cấu hình bộ lọc lưu riêng theo từng tài khoản", "P1",
     "Tài khoản A đã tắt tiêu chí 'Người tạo' và lưu.",
     "1. Đăng xuất, đăng nhập bằng tài khoản B.\n2. Mở màn Đề nghị thu tiền.",
     "—",
     "- Tài khoản B vẫn thấy đủ tiêu chí 'Người tạo'.\n"
     "- Đăng nhập lại tài khoản A thì tiêu chí đó vẫn đang tắt."),

    (20, "Hệ thống nhớ bộ lọc trong 10 phút", "P1",
     "Đang lọc Trạng thái = 'Đã hạch toán'.",
     "1. Bấm vào một mã phiếu để vào chi tiết.\n2. Bấm 'Quay lại'.",
     "—",
     "- Về danh sách, ô Trạng thái vẫn giữ 'Đã hạch toán' và danh sách vẫn đang lọc.\n"
     "- ⚠️ Ghi nhớ này hết hiệu lực sau 10 phút; muốn bỏ ngay thì bấm 'Làm mới'."),

    (21, "Bộ lọc màn chờ duyệt không dính sang màn danh sách", "P1",
     "Tài khoản có quyền 'Kế toán thanh toán'.",
     "1. Ở màn chờ duyệt, lọc Loại thu = 'Thu bán hàng'.\n"
     "2. Chuyển sang màn Đề nghị thu tiền.",
     "Loại thu: Thu bán hàng (đặt ở màn chờ duyệt)",
     "- Màn danh sách KHÔNG bị lọc theo tiêu chí vừa đặt bên màn chờ duyệt."),
]

S3 = [
    (1, "Sắp xếp theo Mã phiếu", "P0",
     "Danh sách có từ 3 phiếu trở lên.",
     "1. Bấm vào tiêu đề cột 'Mã phiếu'.\n2. Bấm lần nữa.",
     "—",
     "- Lần 1: sắp xếp theo mã phiếu, biểu tượng mũi tên đổi chiều.\n"
     "- Lần 2: đảo chiều sắp xếp.\n"
     "- Sau mỗi lần bấm, danh sách quay về trang 1."),

    (2, "Sắp xếp theo Ngày tạo", "P0",
     "Có phiếu lập ở nhiều ngày khác nhau.",
     "1. Bấm tiêu đề cột 'Ngày tạo' 2 lần.",
     "—",
     "- Thứ tự dòng đảo đúng theo ngày tạo (cũ nhất trước / mới nhất trước)."),

    (3, "Sắp xếp theo Ngày cập nhật", "P1",
     "Có phiếu vừa được sửa gần đây.",
     "1. Bấm tiêu đề cột 'Ngày cập nhật'.",
     "—",
     "- Phiếu sửa gần nhất lên đầu (hoặc xuống cuối tùy chiều), giá trị hiển thị dạng "
     "ngày/tháng/năm giờ:phút."),

    (4, "Cột không hỗ trợ sắp xếp", "P2",
     "Danh sách có dữ liệu.",
     "1. Bấm tiêu đề cột 'Lý do thu', 'Khách hàng / Nhà cung cấp', 'Phòng ban'.",
     "—",
     "- Không có biểu tượng sắp xếp ở các cột này, thứ tự dòng không đổi."),

    (5, "Mặc định sắp xếp phiếu mới nhất lên đầu", "P0",
     "Chưa bấm sắp xếp cột nào.",
     "1. Mở màn danh sách lần đầu.\n2. So cột Ngày tạo của dòng 1 và dòng cuối trang.",
     "—",
     "- Dòng đầu là phiếu tạo gần nhất."),

    (6, "Chuyển trang", "P0",
     "Danh sách có trên 10 phiếu.",
     "1. Bấm số trang 2.\n2. Bấm nút chuyển tới trang cuối.",
     "—",
     "- Nội dung bảng đổi theo trang, số thứ tự chạy liên tục (trang 2 bắt đầu từ 11).\n"
     "- ⚠️ Chuyển trang KHÔNG làm mất tiêu chí lọc đang áp dụng."),

    (7, "Đổi số dòng mỗi trang", "P0",
     "Danh sách có trên 20 phiếu.",
     "1. Đổi 'Số dòng/trang' sang 20.",
     "Số dòng/trang: 20",
     "- Bảng hiện 20 dòng, quay về trang 1, dòng đếm cập nhật đúng."),

    (8, "Popup Tuỳ chỉnh cột — cột bắt buộc bị khóa", "P0",
     "Tài khoản bất kỳ.",
     "1. Bấm nút hình 2 cột (Cấu hình cột hiển thị) trên thanh công cụ.\n"
     "2. Thử bỏ tích 'STT', 'Mã phiếu', 'Hành động'.",
     "—",
     "- Popup có tiêu đề 'Tuỳ chỉnh cột'.\n"
     "- 3 cột trên bị xám, có biểu tượng ổ khóa, chú thích 'Cột bắt buộc — không thể ẩn hoặc "
     "đổi vị trí' và không bỏ tích được."),

    (9, "Ẩn một cột rồi lưu", "P0",
     "Đang mở popup 'Tuỳ chỉnh cột'.",
     "1. Bỏ tích cột 'Người cập nhật'.\n2. Bấm 'Lưu'.\n3. Tải lại trang.",
     "Bỏ tích: Người cập nhật",
     "- Thông báo cập nhật thành công, cột 'Người cập nhật' biến mất khỏi bảng.\n"
     "- Tải lại trang vẫn giữ nguyên cấu hình."),

    (10, "Đổi thứ tự cột bằng kéo thả", "P1",
     "Đang mở popup 'Tuỳ chỉnh cột'.",
     "1. Kéo dòng 'Phòng ban' lên ngay dưới 'Mã phiếu'.\n2. Bấm 'Lưu'.",
     "—",
     "- Trên bảng, cột 'Phòng ban' đứng ngay sau cột 'Mã phiếu'."),

    (11, "Cấu hình cột dùng chung cho màn chờ duyệt", "P1",
     "Tài khoản có quyền 'Kế toán thanh toán', vừa ẩn cột 'Người cập nhật' ở màn danh sách.",
     "1. Mở màn 'Phiếu đề nghị thu tiền chờ duyệt'.",
     "—",
     "- Màn chờ duyệt cũng không hiện cột 'Người cập nhật' (2 màn dùng chung một bộ cột)."),

    (12, "Cấu hình cột lưu riêng theo tài khoản", "P1",
     "Tài khoản A đã ẩn cột 'Ngày cập nhật'.",
     "1. Đăng nhập tài khoản B, mở màn Đề nghị thu tiền.",
     "—",
     "- Tài khoản B vẫn thấy đầy đủ cột theo mặc định."),
]

S4 = [
    (1, "Mở form Tạo mới và kiểm tra giá trị mặc định", "P0",
     "Tài khoản bất kỳ vào được màn danh sách.",
     "1. Bấm nút 'Tạo mới'.\n2. Đọc từng ô trên khối 'Thông tin chung'.",
     "—",
     "- Tiêu đề trang 'Thêm phiếu đề nghị thu tiền'.\n"
     "- Loại thu điền sẵn 'Thu bán hàng'; Loại tiền điền sẵn 'VNĐ — VietNamDong'; "
     "Tỷ giá (VND) = 1 và bị khóa; Lý do thu để trống.\n"
     "- ⚠️ KHÔNG có ô 'Mã phiếu' (mã sinh tự động khi lưu) và không có ô Người tạo/Phòng ban.\n"
     "- Bảng Chi tiết hiện dòng 'Không có dữ liệu'; dưới cùng có khối 'Ghi chú'.\n"
     "- Thanh nút dưới cùng: 'Lưu nháp', 'Lưu và gửi duyệt', 'Quay lại'."),

    (2, "Thêm một dòng chi tiết", "P0",
     "Đang mở form Tạo mới, Loại thu = 'Thu bán hàng'.",
     "1. Bấm dấu cộng ở góc phải tiêu đề bảng Chi tiết.",
     "—",
     "- Bảng có 1 dòng trống, số thứ tự 1.\n"
     "- Ô khách hàng hiện gợi ý 'Nhấn vào đây để chọn khách hàng'.\n"
     "- Ô hợp đồng bị khóa, hiện gợi ý 'Chọn khách hàng trước'.\n"
     "- Dòng 'Tổng cộng' xuất hiện với giá trị 0."),

    (3, "Popup chọn khách hàng", "P0",
     "Đang có 1 dòng chi tiết trống, Loại thu = 'Thu bán hàng'.",
     "1. Bấm vào ô khách hàng của dòng 1.\n2. Đọc các ô tìm kiếm và tiêu đề cột.",
     "—",
     "- Popup tiêu đề 'Chọn khách hàng'.\n"
     "- Có 3 ô tìm: 'Tên / Mã khách hàng', 'Mã số thuế', 'Số điện thoại' cùng nút 'Tìm kiếm' "
     "và 'Làm mới'.\n"
     "- Bảng có các cột: STT, Mã KH - Tên khách hàng, Loại, MST, SĐT, Email, Nhóm KH, Địa chỉ, "
     "Tỉnh/TP; có phân trang."),

    (4, "Chọn khách hàng cho dòng chi tiết", "P0",
     "Đang mở popup 'Chọn khách hàng'.",
     "1. Nhập 'ETEK GREEN' vào ô 'Tên / Mã khách hàng', bấm 'Tìm kiếm'.\n"
     "2. Bấm vào dòng khách hàng tìm được.",
     "Tên / Mã khách hàng: ETEK GREEN",
     "- Popup tự đóng.\n"
     "- Ô khách hàng của dòng 1 hiện 'mã - tên khách hàng'.\n"
     "- Ô hợp đồng mở khóa, gợi ý đổi thành 'Nhấn vào đây để chọn hợp đồng'."),

    (5, "Popup chọn hợp đồng bán", "P0",
     "Dòng 1 đã chọn khách hàng ETEK GREEN.",
     "1. Bấm vào ô hợp đồng của dòng 1.",
     "—",
     "- Popup tiêu đề 'Chọn đơn hàng/hợp đồng', dòng phụ hiện đúng 'mã - tên khách hàng' vừa chọn.\n"
     "- Bảng có các cột: STT, Số đơn hàng/Hợp đồng, Ngày lập, Giá trị hợp đồng, Số tiền còn nợ.\n"
     "- Có ô tìm 'Số đơn hàng/Hợp đồng', nút 'Tìm kiếm', 'Làm mới', 'Đóng' và phân trang."),

    (6, "Chọn hợp đồng — tự điền Số tiền còn nợ", "P0",
     "Đang mở popup hợp đồng của khách hàng ETEK GREEN, hợp đồng '05012026' có số tiền còn nợ "
     "10,235,010.",
     "1. Bấm vào dòng hợp đồng '05012026'.",
     "—",
     "- Popup tự đóng, ô hợp đồng hiện '05012026'.\n"
     "- Cột 'Số tiền còn nợ' của dòng 1 hiện 10,235,010.\n"
     "- Dòng 'Tổng cộng' cột Số tiền còn nợ cũng là 10,235,010."),

    (7, "Tìm hợp đồng theo số trong popup", "P1",
     "Khách hàng có nhiều hợp đồng.",
     "1. Nhập một phần số hợp đồng vào ô 'Số đơn hàng/Hợp đồng'.\n2. Bấm 'Tìm kiếm'.",
     "Số đơn hàng/Hợp đồng: HDDV",
     "- Chỉ còn hợp đồng có số chứa chuỗi vừa nhập.\n"
     "- Bấm 'Làm mới' thì danh sách trở về đầy đủ."),

    (8, "Không cho chọn trùng hợp đồng trong cùng phiếu", "P0",
     "Dòng 1 đã chọn hợp đồng '05012026' của khách hàng ETEK GREEN. Đã thêm dòng 2 và chọn "
     "cùng khách hàng đó.",
     "1. Ở dòng 2, bấm ô hợp đồng để mở popup.\n"
     "2. Rê chuột vào dòng hợp đồng '05012026' và bấm chọn.",
     "—",
     "- Dòng '05012026' hiển thị khác biệt và chú thích 'Hợp đồng đã có trong phiếu'.\n"
     "- Bấm vào không chọn được, ô hợp đồng của dòng 2 vẫn trống."),

    (9, "Nhập Số tiền đề nghị thu", "P0",
     "Dòng 1 đã có khách hàng và hợp đồng.",
     "1. Nhập 5,000,000 vào ô Số tiền đề nghị thu của dòng 1.",
     "Số tiền đề nghị thu: 5.000.000",
     "- Ô hiển thị 5,000,000 với dấu phẩy ngăn nghìn.\n"
     "- Dòng 'Tổng cộng' cột Số tiền đề nghị thu cập nhật ngay thành 5,000,000."),

    (10, "Nhiều dòng chi tiết, nhiều khách hàng trong một phiếu", "P0",
     "Đang mở form Tạo mới, Loại thu = 'Thu bán hàng'.",
     "1. Thêm dòng 1: khách hàng X, hợp đồng của X, số tiền 5,000,000.\n"
     "2. Bấm dấu cộng thêm dòng 2: khách hàng Y (khác X), hợp đồng của Y, số tiền 3,000,000.",
     "Dòng 1: 5.000.000 · Dòng 2: 3.000.000",
     "- Hai dòng giữ 2 khách hàng khác nhau, mỗi dòng có popup hợp đồng lọc theo đúng khách "
     "hàng của dòng đó.\n"
     "- Tổng cộng Số tiền đề nghị thu = 8,000,000."),

    (11, "Đổi khách hàng của một dòng đã chọn hợp đồng", "P0",
     "Dòng 1 đã chọn khách hàng X và hợp đồng của X, số tiền còn nợ đang hiện.",
     "1. Bấm lại vào ô khách hàng dòng 1, chọn khách hàng Y.",
     "Khách hàng mới: Y",
     "- ⚠️ Ô hợp đồng của dòng 1 bị XÓA TRẮNG, Số tiền còn nợ về 0.\n"
     "- Bấm mở popup hợp đồng lần nữa thì danh sách là hợp đồng của khách hàng Y."),

    (12, "Xóa một dòng chi tiết", "P0",
     "Bảng chi tiết đang có 2 dòng.",
     "1. Bấm biểu tượng thùng rác ở cuối dòng 1.",
     "—",
     "- Dòng 1 biến mất, dòng còn lại được đánh số lại thành 1.\n"
     "- Dòng 'Tổng cộng' tính lại đúng theo dòng còn lại."),

    (13, "Đổi loại thu khi đã có dòng chi tiết — hộp xác nhận", "P0",
     "Bảng chi tiết đang có 1 dòng đã chọn khách hàng và hợp đồng.",
     "1. Đổi ô 'Loại thu' sang 'Thu nhà cung cấp'.",
     "Loại thu: Thu nhà cung cấp",
     "- Hộp thoại 'Đổi loại thu' hiện với nội dung 'Đổi loại thu sẽ xóa toàn bộ dòng chi tiết "
     "đã chọn. Bạn có chắc chắn?' cùng 2 nút 'Xác nhận' và 'Hủy'."),

    (14, "Xác nhận đổi loại thu", "P0",
     "Đang hiện hộp thoại 'Đổi loại thu'.",
     "1. Bấm 'Xác nhận'.",
     "—",
     "- Toàn bộ dòng chi tiết bị xóa, bảng hiện 'Không có dữ liệu'.\n"
     "- Tiêu đề cột đổi thành 'Nhà cung cấp' và 'Hợp đồng mua'.\n"
     "- Gợi ý trong ô đổi thành 'Nhấn vào đây để chọn nhà cung cấp'."),

    (15, "Hủy hộp thoại đổi loại thu", "P1",
     "Đang hiện hộp thoại 'Đổi loại thu'.",
     "1. Bấm 'Hủy'.",
     "—",
     "- Hộp thoại đóng, các dòng chi tiết đã chọn vẫn còn nguyên."),

    (16, "Popup chọn nhà cung cấp", "P0",
     "Loại thu = 'Thu nhà cung cấp', đã thêm 1 dòng chi tiết trống.",
     "1. Bấm vào ô nhà cung cấp của dòng 1.",
     "—",
     "- Popup tiêu đề 'Chọn nhà cung cấp', có ô 'Mã / Tên nhà cung cấp', nút 'Tìm kiếm', "
     "'Làm mới', 'Đóng'.\n"
     "- Bảng 3 cột: STT, Mã nhà cung cấp, Tên nhà cung cấp; có phân trang."),

    (17, "Chọn nhà cung cấp và hợp đồng mua", "P0",
     "Đang mở popup 'Chọn nhà cung cấp'.",
     "1. Gõ 'HỢP LONG', bấm 'Tìm kiếm', chọn nhà cung cấp tìm được.\n"
     "2. Bấm vào ô hợp đồng của dòng đó.",
     "Mã / Tên nhà cung cấp: HỢP LONG",
     "- Ô nhà cung cấp hiện 'mã - tên'.\n"
     "- Popup hợp đồng mở ra chỉ chứa hợp đồng MUA của nhà cung cấp đó."),

    (18, "Đổi Loại tiền sang ngoại tệ — tự lấy tỷ giá", "P0",
     "Đang mở form Tạo mới, Loại tiền đang là VNĐ.",
     "1. Đổi 'Loại tiền' sang một ngoại tệ (ví dụ USD).",
     "Loại tiền: USD",
     "- Ô 'Tỷ giá (VND)' mở khóa và tự điền tỷ giá của loại tiền đó.\n"
     "- Bảng chi tiết tách cột 'Số tiền đề nghị thu' thành 2 cột con: tên ngoại tệ và VND."),

    (19, "Quy đổi VND theo tỷ giá", "P0",
     "Loại tiền = USD, Tỷ giá = 25,000. Dòng 1 đã chọn khách hàng và hợp đồng.",
     "1. Nhập Số tiền đề nghị thu = 100.",
     "Số tiền đề nghị thu: 100 · Tỷ giá: 25.000",
     "- Cột VND của dòng 1 hiện 2,500,000.\n"
     "- Dòng 'Tổng cộng' cột VND cũng là 2,500,000."),

    (20, "Sửa tay tỷ giá thì cột quy đổi tính lại", "P1",
     "Loại tiền = USD, Tỷ giá đang là 25,000, dòng 1 có số tiền 100.",
     "1. Sửa Tỷ giá thành 26,000.\n2. Gõ lại số tiền dòng 1 (nhập lại 100).",
     "Tỷ giá: 26.000",
     "- Cột VND của dòng 1 thành 2,600,000."),

    (21, "Đổi lại Loại tiền về VNĐ", "P1",
     "Đang chọn ngoại tệ, tỷ giá khác 1.",
     "1. Đổi 'Loại tiền' về 'VNĐ — VietNamDong'.",
     "Loại tiền: VNĐ",
     "- Tỷ giá tự về 1 và ô bị khóa lại.\n"
     "- Bảng chi tiết bỏ cột ngoại tệ, chỉ còn 1 cột số tiền."),

    (22, "Lưu nháp với dữ liệu tối thiểu", "P0",
     "Đang mở form Tạo mới, chưa nhập Lý do thu, chưa thêm dòng chi tiết nào.",
     "1. Bấm 'Lưu nháp'.",
     "—",
     "- ⚠️ Lưu thành công, hệ thống báo 'Lưu phiếu đề nghị thu thành công!'.\n"
     "- Quay về danh sách, phiếu mới đứng đầu với trạng thái 'Đang tạo'.\n"
     "- Mã phiếu tự sinh theo dạng <mã công ty>.DNTT<tháng năm>.<5 chữ số>."),

    (23, "Lưu nháp phiếu có dữ liệu đầy đủ", "P0",
     "Đã nhập Lý do thu = 'Thu tiền hàng đợt 1', 1 dòng chi tiết đủ khách hàng, hợp đồng, "
     "số tiền 5,000,000, Ghi chú = 'Đợt 1'.",
     "1. Bấm 'Lưu nháp'.\n2. Mở lại phiếu vừa lưu.",
     "Lý do thu: Thu tiền hàng đợt 1 · Số tiền: 5.000.000",
     "- Báo lưu thành công, trạng thái 'Đang tạo'.\n"
     "- Mở lại thấy đủ dữ liệu vừa nhập, cột Tổng tiền đề nghị trên lưới là 5,000,000."),

    (24, "Hộp xác nhận khi bấm Lưu và gửi duyệt", "P0",
     "Form đã nhập đủ Lý do thu và 1 dòng chi tiết hợp lệ.",
     "1. Bấm 'Lưu và gửi duyệt'.",
     "—",
     "- Hộp thoại 'Xác nhận lưu và gửi duyệt' hiện với câu hỏi 'Bạn đồng ý lưu và duyệt?' và "
     "2 nút 'Xác nhận', 'Hủy'.\n"
     "- Bấm 'Hủy' thì không lưu gì, vẫn ở lại form."),

    (25, "Lưu và gửi duyệt thành công", "P0",
     "Như trên, đang mở hộp xác nhận.",
     "1. Bấm 'Xác nhận'.",
     "—",
     "- Hệ thống báo 'Gửi duyệt phiếu đề nghị thu thành công!'.\n"
     "- Về danh sách, phiếu mới ở trạng thái 'Chờ KT duyệt'.\n"
     "- ⚠️ Thông báo khác với khi lưu nháp — đừng nhầm 2 câu."),

    (26, "Gửi duyệt bắn thông báo cho kế toán cùng công ty", "P0",
     "Người lập thuộc công ty 1. Tài khoản kế toán G có quyền 'Kế toán thanh toán' thuộc công "
     "ty 1; tài khoản kế toán H có quyền đó nhưng thuộc công ty 4.",
     "1. Lập phiếu và bấm 'Lưu và gửi duyệt'.\n"
     "2. Đăng nhập tài khoản G, mở chuông thông báo.\n"
     "3. Đăng nhập tài khoản H, mở chuông thông báo.",
     "—",
     "- Tài khoản G nhận thông báo dạng '[DNTT] Chờ duyệt: <mã phiếu>. Người đề nghị: <tên>. "
     "Số tiền: <tổng>' và bấm vào mở đúng phiếu.\n"
     "- ⚠️ Tài khoản H (công ty khác) KHÔNG nhận thông báo."),

    (27, "Cảnh báo chưa lưu khi rời form", "P0",
     "Đang mở form Tạo mới và đã nhập Lý do thu.",
     "1. Bấm 'Quay lại'.",
     "—",
     "- Hộp thoại 'Thông tin chưa lưu' hiện: 'Bạn có thông tin chưa lưu. Có chắc chắn muốn "
     "thoát?' với 2 nút 'Thoát' và 'Ở lại'.\n"
     "- Bấm 'Ở lại': vẫn ở form, dữ liệu còn nguyên.\n"
     "- Bấm 'Thoát': về danh sách và KHÔNG có phiếu mới nào được tạo."),

    (28, "Không cảnh báo khi chưa nhập gì", "P1",
     "Vừa mở form Tạo mới, chưa chạm vào ô nào.",
     "1. Bấm 'Quay lại'.",
     "—",
     "- Về thẳng danh sách, không hiện hộp thoại 'Thông tin chưa lưu'."),
]

S5 = [
    (1, "Nút Sửa chỉ hiện với phiếu của mình ở trạng thái cho sửa", "P0",
     "Tài khoản A có: phiếu P1 do A lập trạng thái 'Đang tạo'; P2 do A lập trạng thái "
     "'Không duyệt'; P3 do A lập trạng thái 'Chờ KT duyệt'; P4 do người khác lập trạng thái "
     "'Đang tạo' (A nhìn thấy nhờ quyền xem).",
     "1. Mở màn danh sách bằng tài khoản A.\n2. Xem cột Hành động của từng phiếu.",
     "—",
     "- P1 và P2 có nút Sửa (hình bút chì).\n"
     "- P3 và P4 KHÔNG có nút Sửa.\n"
     "- ⚠️ P4 cũng không có nút Xóa."),

    (2, "Mở form Sửa và kiểm tra dữ liệu nạp lên", "P0",
     "Phiếu P1 'Đang tạo' của tài khoản A có 1 dòng chi tiết.",
     "1. Bấm nút Sửa ở dòng phiếu P1.",
     "—",
     "- Tiêu đề trang 'Sửa phiếu đề nghị thu tiền'.\n"
     "- Có thêm ô 'Mã phiếu' (khóa), 'Người tạo' (khóa), 'Phòng ban' (khóa).\n"
     "- Góc phải tiêu đề khối 'Thông tin chung' hiện 'người tạo - ngày lập'.\n"
     "- Mọi ô còn lại nạp đúng dữ liệu đã lưu, bảng chi tiết đủ số dòng."),

    (3, "Mã phiếu không sửa được", "P0",
     "Đang mở form Sửa.",
     "1. Bấm vào ô 'Mã phiếu' và gõ ký tự.",
     "Gõ: ABC",
     "- Ô bị khóa, không nhập được, giá trị giữ nguyên."),

    (4, "Sửa Lý do thu và lưu nháp", "P0",
     "Phiếu P1 'Đang tạo', lý do thu hiện tại là 'Thu tiền hàng đợt 1'.",
     "1. Đổi Lý do thu thành 'Thu tiền hàng đợt 1 (sửa)'.\n2. Bấm 'Lưu nháp'.\n"
     "3. Mở lại phiếu.",
     "Lý do thu: Thu tiền hàng đợt 1 (sửa)",
     "- Báo 'Lưu phiếu đề nghị thu thành công!'.\n"
     "- Trạng thái vẫn 'Đang tạo', Lý do thu đã đổi.\n"
     "- Cột 'Người cập nhật' và 'Ngày cập nhật' trên lưới đổi theo người vừa sửa."),

    (5, "Thêm dòng chi tiết khi sửa", "P0",
     "Phiếu P1 đang có 1 dòng chi tiết.",
     "1. Bấm Sửa, thêm dòng 2 với khách hàng và hợp đồng khác, số tiền 2,000,000.\n"
     "2. Bấm 'Lưu nháp'.\n3. Mở lại phiếu.",
     "Dòng 2: 2.000.000",
     "- Phiếu có 2 dòng chi tiết, Tổng tiền đề nghị trên lưới cộng cả 2 dòng."),

    (6, "Xóa dòng chi tiết khi sửa", "P0",
     "Phiếu P1 đang có 2 dòng chi tiết.",
     "1. Bấm Sửa, xóa dòng 2.\n2. Bấm 'Lưu nháp'.\n3. Mở lại phiếu.",
     "—",
     "- Phiếu chỉ còn 1 dòng, tổng tiền tính lại đúng."),

    (7, "Sửa phiếu Không duyệt rồi gửi duyệt lại", "P0",
     "Phiếu P2 do A lập, trạng thái 'Không duyệt', ô Ghi chú đang chứa lý do không duyệt của "
     "kế toán.",
     "1. Bấm Sửa phiếu P2, chỉnh số tiền đề nghị thu.\n"
     "2. Bấm 'Lưu và gửi duyệt' rồi 'Xác nhận'.",
     "Số tiền đề nghị thu: 4.000.000",
     "- Báo 'Gửi duyệt phiếu đề nghị thu thành công!'.\n"
     "- Trạng thái phiếu chuyển sang 'Chờ KT duyệt'.\n"
     "- Phiếu xuất hiện lại ở màn chờ duyệt của kế toán."),

    (8, "Cảnh báo chưa lưu ở form Sửa", "P0",
     "Đang mở form Sửa và vừa đổi Lý do thu.",
     "1. Bấm 'Quay lại'.",
     "—",
     "- Hộp thoại 'Thông tin chưa lưu' hiện.\n"
     "- Bấm 'Thoát' thì dữ liệu phiếu KHÔNG bị thay đổi."),

    (9, "Mở form Sửa mà không sửa gì thì không cảnh báo", "P1",
     "Vừa mở form Sửa, chưa chạm vào ô nào.",
     "1. Bấm 'Quay lại'.",
     "—",
     "- ⚠️ Về thẳng danh sách, KHÔNG hiện hộp 'Thông tin chưa lưu'."),

    (10, "Sửa từ màn chi tiết", "P1",
     "Đang xem chi tiết phiếu P1 'Đang tạo' của chính mình.",
     "1. Bấm nút 'Sửa' ở thanh nút dưới cùng.",
     "—",
     "- Chuyển sang màn 'Sửa phiếu đề nghị thu tiền' đúng phiếu đó."),
]

S6 = [
    (1, "Mở chi tiết phiếu — mọi ô ở chế độ chỉ đọc", "P0",
     "Có phiếu TEST.DNTT.00062 trạng thái 'Chờ KT duyệt' với 2 dòng chi tiết.",
     "1. Bấm mã phiếu để vào chi tiết.\n2. Thử gõ vào ô 'Lý do thu' và ô số tiền.",
     "—",
     "- Mọi ô đều khóa, không nhập được.\n"
     "- Hiện đủ Mã phiếu, Loại thu, Loại tiền, Tỷ giá, Người tạo, Phòng ban, Lý do thu, "
     "bảng Chi tiết, Ghi chú và khối 'Lịch sử'.\n"
     "- Bấm vào ô khách hàng KHÔNG mở popup chọn."),

    (2, "Bảng chi tiết ở màn xem có dòng Tổng cộng", "P0",
     "Phiếu có 2 dòng: 234,298,377 và 10,850,000.",
     "1. Mở chi tiết phiếu.\n2. Đọc dòng cuối bảng chi tiết.",
     "—",
     "- Dòng 'Tổng cộng' hiện tổng Số tiền còn nợ và tổng Số tiền đề nghị thu của cả 2 dòng "
     "(245,148,377)."),

    (3, "Bộ nút ở màn chi tiết theo trạng thái và quyền — phiếu nháp của mình", "P0",
     "Phiếu 'Đang tạo' do chính người đăng nhập lập.",
     "1. Mở chi tiết phiếu.\n2. Đọc thanh nút dưới cùng.",
     "—",
     "- Có nút 'Sửa', 'In phiếu', 'Xóa', 'Quay lại'.\n"
     "- Không có 'Không duyệt' và 'Tạo phiếu thu'."),

    (4, "Bộ nút ở màn chi tiết — kế toán xem phiếu chờ duyệt", "P0",
     "Tài khoản có quyền 'Kế toán thanh toán', phiếu đang 'Chờ KT duyệt', chưa có phiếu thu nào "
     "lập từ phiếu này.",
     "1. Mở chi tiết phiếu.",
     "—",
     "- Có nút 'Tạo phiếu thu', 'In phiếu', 'Không duyệt', 'Quay lại'.\n"
     "- Không có nút 'Sửa' và 'Xóa' (phiếu không phải của mình / đã gửi duyệt)."),

    (5, "Bộ nút ở màn chi tiết — phiếu đã hạch toán", "P1",
     "Phiếu ở trạng thái 'Đã hạch toán'.",
     "1. Mở chi tiết phiếu.",
     "—",
     "- Chỉ còn 'In phiếu' và 'Quay lại'.\n"
     "- ⚠️ Không có nút nào có thể làm thay đổi phiếu."),

    (6, "Tiêu đề trang chi tiết kèm mã phiếu", "P2",
     "Phiếu TEST.DNTT.00062.",
     "1. Mở chi tiết phiếu, đọc tiêu đề trên thanh trên cùng và tiêu đề tab trình duyệt.",
     "—",
     "- Cả hai đều hiện 'Chi tiết phiếu đề nghị thu tiền: TEST.DNTT.00062'."),

    (7, "Số tiền còn nợ tính lại theo sổ kế toán khi mở phiếu", "P1",
     "Phiếu gắn hợp đồng H; sổ kế toán vừa ghi nhận thêm một khoản thu của hợp đồng H.",
     "1. Mở chi tiết phiếu, ghi lại 'Số tiền còn nợ'.\n"
     "2. Tải lại trang và đọc lại giá trị.",
     "—",
     "- Giá trị phản ánh số dư công nợ mới nhất.\n"
     "- ⚠️ Số này KHÔNG được lưu trong phiếu nên có thể khác lần xem trước — không phải lỗi."),

    (8, "Quay lại danh sách từ màn chi tiết", "P2",
     "Đang xem chi tiết một phiếu.",
     "1. Bấm nút 'Quay lại'.",
     "—",
     "- Về màn danh sách Đề nghị thu tiền, không hiện cảnh báo chưa lưu."),
]

S7 = [
    (1, "Mở hộp thoại Không duyệt", "P0",
     "Tài khoản có quyền 'Kế toán thanh toán'; phiếu TEST.DNTT.00062 đang 'Chờ KT duyệt'.",
     "1. Mở chi tiết phiếu.\n2. Bấm nút 'Không duyệt'.",
     "—",
     "- Hộp thoại 'Không duyệt phiếu' mở ra, dòng phụ hiện đúng mã phiếu.\n"
     "- Có ô 'Lý do không duyệt' bắt buộc (dấu sao đỏ), nút 'Không duyệt' và 'Đóng'."),

    (2, "Không duyệt mà bỏ trống lý do", "P0",
     "Đang mở hộp thoại 'Không duyệt phiếu'.",
     "1. Để trống ô 'Lý do không duyệt'.\n2. Bấm nút 'Không duyệt'.",
     "Lý do không duyệt: (bỏ trống)",
     "- Hệ thống báo lỗi đỏ ngay dưới ô: 'Bắt buộc nhập lý do không duyệt'.\n"
     "- Hộp thoại KHÔNG đóng, trạng thái phiếu không đổi."),

    (3, "Không duyệt mà chỉ nhập khoảng trắng", "P1",
     "Đang mở hộp thoại 'Không duyệt phiếu'.",
     "1. Gõ 3 dấu cách vào ô lý do.\n2. Bấm 'Không duyệt'.",
     "Lý do không duyệt: '   '",
     "- Vẫn báo lỗi bắt buộc nhập, không cho gửi."),

    (4, "Không duyệt thành công", "P0",
     "Đang mở hộp thoại; phiếu ở trạng thái 'Chờ KT duyệt'.",
     "1. Nhập lý do 'Sai số tiền đề nghị, đề nghị lập lại'.\n2. Bấm 'Không duyệt'.",
     "Lý do không duyệt: Sai số tiền đề nghị, đề nghị lập lại",
     "- Báo 'Không duyệt phiếu đề nghị thu thành công!'.\n"
     "- Hộp thoại đóng, màn chi tiết nạp lại, Trạng thái thành 'Không duyệt'.\n"
     "- Ô 'Ghi chú' của phiếu hiện đúng lý do vừa nhập.\n"
     "- Thanh nút không còn 'Không duyệt' và 'Tạo phiếu thu'."),

    (5, "Phiếu bị không duyệt rời khỏi màn chờ duyệt", "P0",
     "Vừa không duyệt phiếu ở trường hợp trên.",
     "1. Mở lại màn 'Phiếu đề nghị thu tiền chờ duyệt'.",
     "—",
     "- Phiếu vừa xử lý không còn trong danh sách.\n"
     "- Tổng số phiếu chờ duyệt giảm 1."),

    (6, "Người lập nhìn thấy lý do không duyệt", "P0",
     "Phiếu vừa bị không duyệt là do tài khoản A lập.",
     "1. Đăng nhập tài khoản A, mở chi tiết phiếu đó.",
     "—",
     "- Trạng thái 'Không duyệt', ô Ghi chú hiện lý do của kế toán.\n"
     "- Có nút 'Sửa' và 'Xóa' (phiếu quay lại trạng thái cho sửa)."),

    (7, "Đóng hộp thoại Không duyệt không làm gì", "P1",
     "Đang mở hộp thoại và đã gõ lý do.",
     "1. Bấm nút 'Đóng'.\n2. Mở lại hộp thoại.",
     "Lý do không duyệt: thử",
     "- Hộp đóng, trạng thái phiếu không đổi.\n"
     "- Mở lại thì ô lý do đã trống (không giữ nội dung cũ)."),

    (8, "Nút Tạo phiếu thu điều hướng đúng", "P1",
     "Tài khoản có quyền 'Kế toán thanh toán'; phiếu 'Chờ KT duyệt' chưa có phiếu thu.",
     "1. Mở chi tiết phiếu, bấm 'Tạo phiếu thu'.",
     "—",
     "- Chuyển sang màn lập Phiếu thu, phiếu đề nghị hiện tại đã được gắn sẵn.\n"
     "- ⚠️ Màn Phiếu thu là chức năng khác, không thuộc phạm vi tài liệu này."),

    (9, "Nút Tạo phiếu thu biến mất khi đã có phiếu thu", "P1",
     "Phiếu 'Chờ KT duyệt' đã được lập 1 phiếu thu (kể cả phiếu thu còn ở dạng nháp).",
     "1. Mở lại chi tiết phiếu đề nghị.",
     "—",
     "- Nút 'Tạo phiếu thu' KHÔNG còn hiển thị.\n"
     "- Nút 'Không duyệt' VẪN còn (2 nút không cùng điều kiện)."),
]

S8 = [
    (1, "Hộp xác nhận xóa từ danh sách", "P0",
     "Phiếu TPE.DNTT0826.00009 'Đang tạo' do người đăng nhập lập.",
     "1. Ở dòng phiếu, bấm nút ba chấm ở cột Hành động.\n2. Bấm 'Xóa'.",
     "—",
     "- Hộp thoại 'Xác nhận xóa' hiện với nội dung: Bạn có chắc muốn xóa phiếu đề nghị thu tiền "
     "'TPE.DNTT0826.00009'?\n"
     "- Có 2 nút 'Xóa' và 'Hủy'."),

    (2, "Hủy hộp xác nhận xóa", "P0",
     "Đang mở hộp 'Xác nhận xóa'.",
     "1. Bấm 'Hủy'.\n2. Kiểm tra lại danh sách.",
     "—",
     "- Hộp đóng, phiếu vẫn còn nguyên trong danh sách."),

    (3, "Xóa phiếu thành công", "P0",
     "Phiếu 'Đang tạo' do chính mình lập, có 2 dòng chi tiết.",
     "1. Bấm ba chấm > 'Xóa'.\n2. Bấm 'Xóa' trong hộp xác nhận.",
     "—",
     "- Hệ thống báo 'Xóa thành công'.\n"
     "- Danh sách tự tải lại, phiếu biến mất, tổng số phiếu giảm 1.\n"
     "- Mở lại lịch sử của phiếu khác không bị ảnh hưởng."),

    (4, "Xóa phiếu Không duyệt", "P1",
     "Phiếu do chính mình lập, trạng thái 'Không duyệt'.",
     "1. Xóa phiếu như trên.",
     "—",
     "- Xóa được, báo 'Xóa thành công'."),

    (5, "Không có nút Xóa với phiếu đã gửi duyệt", "P0",
     "Phiếu do chính mình lập, trạng thái 'Chờ KT duyệt'.",
     "1. Bấm nút ba chấm ở cột Hành động (nếu có).",
     "—",
     "- Không có mục 'Xóa' trong menu, chỉ còn 'Lịch sử'.\n"
     "- Cột hành động của dòng chỉ còn nút In phiếu và Lịch sử."),

    (6, "Xóa từ màn chi tiết", "P1",
     "Đang xem chi tiết phiếu 'Đang tạo' của chính mình.",
     "1. Bấm nút 'Xóa' ở thanh nút dưới cùng.\n2. Bấm 'Xóa' trong hộp xác nhận.",
     "—",
     "- Báo 'Xóa thành công' và quay về màn danh sách.\n"
     "- Phiếu không còn trong danh sách."),

    (7, "Màn chờ duyệt không cho xóa", "P0",
     "Tài khoản kế toán đang ở màn chờ duyệt.",
     "1. Xem cột Hành động của các dòng.",
     "—",
     "- Không dòng nào có nút Xóa hoặc nút Sửa."),
]

S9 = [
    (1, "Mở màn in từ danh sách", "P0",
     "Phiếu TEST.DNTT.00062 có 2 dòng chi tiết.",
     "1. Ở dòng phiếu, bấm nút hình máy in.",
     "—",
     "- Mở TAB MỚI hiển thị bản in của đúng phiếu đó.\n"
     "- Tiêu đề tab là 'In phiếu <mã phiếu>'."),

    (2, "Nội dung phần đầu bản in", "P0",
     "Như trên.",
     "1. Đọc phần đầu bản in.",
     "—",
     "- Có logo và dòng thông tin công ty ở đầu trang.\n"
     "- Tiêu đề in đậm giữa trang: 'GIẤY ĐỀ NGHỊ THU TIỀN'.\n"
     "- Dòng dưới tiêu đề: 'Số phiếu: <mã> · Ngày lập: <ngày giờ>'."),

    (3, "Khối thông tin chia đều 2 cột", "P0",
     "Như trên.",
     "1. Đọc khối thông tin ngay dưới tiêu đề.",
     "—",
     "- Cột trái đúng 3 dòng: Người đề nghị, Loại thu, Trạng thái.\n"
     "- Cột phải đúng 3 dòng: Phòng ban, Loại tiền (kèm tỷ giá), Lý do thu.\n"
     "- ⚠️ Bản in KHÔNG có dòng 'Người nộp tiền'."),

    (4, "Bảng chi tiết trên bản in", "P0",
     "Phiếu 'Thu bán hàng' có 2 dòng.",
     "1. Đọc bảng trên bản in.",
     "—",
     "- Cột: STT, Khách hàng, Số đơn hàng/Hợp đồng, Số tiền còn nợ, Số tiền đề nghị thu, Ghi chú.\n"
     "- Dòng cuối: 'Tổng cộng (quy đổi VND)' kèm tổng số tiền đề nghị."),

    (5, "Bản in phiếu Thu nhà cung cấp đổi nhãn cột", "P1",
     "Phiếu 'Thu nhà cung cấp'.",
     "1. Mở bản in của phiếu đó.",
     "—",
     "- Hai cột đổi nhãn thành 'Nhà cung cấp' và 'Hợp đồng mua'."),

    (6, "Khối ký tên", "P1",
     "Phiếu bất kỳ.",
     "1. Xem phần cuối bản in.",
     "—",
     "- Ba ô ký ngang hàng: NGƯỜI ĐỀ NGHỊ, KẾ TOÁN, GIÁM ĐỐC, mỗi ô có dòng '(Ký, ghi rõ họ tên)'.\n"
     "- Ô NGƯỜI ĐỀ NGHỊ có sẵn tên người lập phiếu; ô KẾ TOÁN có tên người xử lý nếu phiếu đã "
     "được xử lý."),

    (7, "Bản in phiếu bị không duyệt hiện lý do", "P0",
     "Phiếu ở trạng thái 'Không duyệt', ghi chú chứa lý do.",
     "1. Mở bản in.",
     "—",
     "- ⚠️ Dòng dưới bảng ghi 'Lý do không duyệt:' kèm nội dung (không phải nhãn 'Ghi chú:')."),

    (8, "Bản in phiếu bình thường hiện nhãn Ghi chú", "P1",
     "Phiếu 'Chờ KT duyệt' có ghi chú.",
     "1. Mở bản in.",
     "—",
     "- Dòng dưới bảng ghi 'Ghi chú:' kèm nội dung."),

    (9, "Bấm nút In để mở hộp thoại in", "P0",
     "Đang ở màn in.",
     "1. Bấm nút 'In' màu xanh góc trên trái.",
     "—",
     "- Hộp thoại in của trình duyệt mở ra.\n"
     "- Bản xem trước KHÔNG có nút 'In', không có menu bên trái, bảng không tràn mép phải."),

    (10, "In từ màn chi tiết", "P1",
     "Đang xem chi tiết một phiếu.",
     "1. Bấm nút 'In phiếu'.",
     "—",
     "- Mở tab mới đúng bản in của phiếu đang xem."),

    (11, "In từ màn chờ duyệt", "P1",
     "Tài khoản kế toán ở màn chờ duyệt.",
     "1. Bấm nút hình máy in ở một dòng.",
     "—",
     "- Mở bản in đúng phiếu đó."),
]

S10 = [
    (1, "Mở popup Lịch sử từ danh sách", "P0",
     "Phiếu TPE.DNTT0826.00007 đã trải qua tạo mới, sửa và đổi trạng thái.",
     "1. Ở dòng phiếu, bấm nút hình đồng hồ quay ngược (Lịch sử).",
     "—",
     "- Popup 'Lịch sử thay đổi' mở, dòng phụ ghi 'Phiếu: <mã phiếu>'.\n"
     "- Có nút 'Bộ lọc' và nút 'Đóng'."),

    (2, "Nội dung một mốc lịch sử", "P0",
     "Như trên.",
     "1. Đọc các mốc trong popup từ dưới lên.",
     "—",
     "- Mốc dưới cùng là 'Tạo mới' kèm ngày giờ và 'Người thực hiện: <tên> – <phòng ban>'.\n"
     "- Mốc 'Thay đổi thông tin' liệt kê từng trường đã đổi, có mũi tên từ giá trị cũ sang mới.\n"
     "- Mốc 'Thay đổi trạng thái' ghi rõ 'Trạng thái: <cũ> → <mới>' bằng tên tiếng Việt."),

    (3, "Lịch sử ghi lại thay đổi dòng chi tiết", "P0",
     "Phiếu vừa được thêm 1 dòng chi tiết mới.",
     "1. Mở lịch sử phiếu.",
     "—",
     "- Có mục 'Bảng chi tiết thêm mới:' liệt kê dòng vừa thêm kèm khách hàng, hợp đồng và "
     "số tiền đề nghị thu.\n"
     "- ⚠️ Sửa 1 ô số tiền chỉ in đúng dòng đó, không in lại cả bảng."),

    (4, "Lịch sử ghi lý do không duyệt", "P0",
     "Phiếu vừa bị kế toán không duyệt với lý do 'Sai số tiền đề nghị'.",
     "1. Mở lịch sử phiếu.",
     "—",
     "- Mốc mới nhất là đổi trạng thái từ 'Chờ KT duyệt' sang 'Không duyệt', kèm lý do đã nhập.\n"
     "- Người thực hiện là tài khoản kế toán."),

    (5, "Khối Lịch sử ở màn chi tiết", "P0",
     "Đang xem chi tiết một phiếu.",
     "1. Cuộn xuống cuối trang.\n2. Bấm nút 'Xem lịch sử'.",
     "—",
     "- Khối 'Lịch sử' mở ra với nội dung y hệt popup ngoài danh sách.\n"
     "- Nút đổi thành 'Thu gọn', bên cạnh có nút 'Làm mới'."),

    (6, "Phiếu chưa có thao tác nào", "P1",
     "Phiếu được nạp sẵn từ dữ liệu cũ, chưa từng sửa trên màn này.",
     "1. Mở lịch sử phiếu đó.",
     "—",
     "- Hiện dòng 'Chưa có lịch sử thao tác nào.' kèm biểu tượng, không báo lỗi."),

    (7, "Lịch sử hiện cả ở màn chờ duyệt", "P1",
     "Tài khoản kế toán ở màn chờ duyệt.",
     "1. Bấm nút Lịch sử ở một dòng.",
     "—",
     "- Popup lịch sử mở bình thường (chức năng này không gắn quyền riêng)."),
]

S11 = [
    (1, "Gửi duyệt khi bỏ trống Lý do thu", "P0",
     "Đang mở form Tạo mới, chưa nhập gì.",
     "1. Bấm 'Lưu và gửi duyệt'.\n2. Bấm 'Xác nhận'.",
     "—",
     "- Ô 'Lý do thu' viền đỏ, dưới ô hiện 'Bắt buộc nhập'.\n"
     "- Dưới bảng Chi tiết cũng hiện 'Bắt buộc nhập'.\n"
     "- ⚠️ Không có phiếu nào được tạo, vẫn ở lại form."),

    (2, "Gửi duyệt khi có Lý do thu nhưng chưa có dòng chi tiết", "P0",
     "Đã nhập Lý do thu, bảng chi tiết trống.",
     "1. Bấm 'Lưu và gửi duyệt' rồi 'Xác nhận'.",
     "Lý do thu: Thu tiền hàng",
     "- Chỉ còn lỗi 'Bắt buộc nhập' dưới bảng Chi tiết; ô Lý do thu hết viền đỏ."),

    (3, "Lỗi bắt buộc mất ngay khi thêm dòng", "P1",
     "Đang hiện lỗi 'Bắt buộc nhập' dưới bảng Chi tiết.",
     "1. Bấm dấu cộng thêm 1 dòng.",
     "—",
     "- Dòng lỗi dưới bảng biến mất ngay."),

    (4, "Gửi duyệt khi dòng chi tiết chưa chọn khách hàng", "P0",
     "Đã nhập Lý do thu, có 1 dòng chi tiết trống hoàn toàn.",
     "1. Bấm 'Lưu và gửi duyệt' rồi 'Xác nhận'.",
     "—",
     "- Ô khách hàng của dòng 1 viền đỏ kèm 'Bắt buộc nhập'.\n"
     "- Ô hợp đồng của dòng 1 cũng báo 'Bắt buộc nhập'."),

    (5, "Lỗi dòng chi tiết dồn đúng vị trí khi xóa dòng", "P0",
     "Có 2 dòng chi tiết, dòng 1 đang báo 'Bắt buộc nhập' ở ô khách hàng, dòng 2 đã điền đủ.",
     "1. Xóa dòng 1.\n2. Quan sát dòng còn lại.",
     "—",
     "- ⚠️ Dòng còn lại (dữ liệu của dòng 2 cũ) KHÔNG bị dính câu 'Bắt buộc nhập' của dòng đã xóa."),

    (6, "Lỗi dòng chi tiết bị xóa sạch khi đổi loại thu", "P1",
     "Đang có lỗi 'Bắt buộc nhập' ở dòng 1.",
     "1. Đổi Loại thu và bấm 'Xác nhận' ở hộp thoại.\n2. Thêm 1 dòng mới.",
     "—",
     "- Dòng mới sạch lỗi, không hứng câu báo lỗi của dòng cũ."),

    (7, "Tỷ giá bằng 0", "P0",
     "Loại tiền là ngoại tệ.",
     "1. Xóa tỷ giá và nhập 0.\n2. Bấm 'Lưu nháp'.",
     "Tỷ giá (VND): 0",
     "- Ô Tỷ giá viền đỏ, hiện thông báo 'Phải lớn hơn 0'.\n"
     "- Phiếu không được lưu."),

    (8, "Tỷ giá nhập chữ", "P1",
     "Loại tiền là ngoại tệ.",
     "1. Gõ 'abc' vào ô Tỷ giá.",
     "Tỷ giá (VND): abc",
     "- Ô chỉ nhận số, chữ không vào được hoặc bị báo phải là số."),

    (9, "Số tiền đề nghị thu âm", "P1",
     "Dòng chi tiết đã đủ khách hàng và hợp đồng.",
     "1. Nhập '-1000' vào ô Số tiền đề nghị thu.\n2. Bấm 'Lưu nháp'.",
     "Số tiền đề nghị thu: -1000",
     "- Không nhập được dấu trừ, hoặc hệ thống báo không được nhỏ hơn 0 và không lưu."),

    (10, "Số tiền đề nghị thu để 0", "P1",
     "Dòng chi tiết đã đủ khách hàng và hợp đồng, số tiền để 0.",
     "1. Bấm 'Lưu và gửi duyệt' rồi 'Xác nhận'.",
     "Số tiền đề nghị thu: 0",
     "- ⚠️ Lưu được (0 là giá trị hợp lệ). Đây là thiết kế, không phải lỗi."),

    (11, "Lý do thu rất dài", "P2",
     "Đang mở form Tạo mới.",
     "1. Nhập Lý do thu dài 500 ký tự.\n2. Lưu nháp và mở lại phiếu.",
     "Lý do thu: chuỗi 500 ký tự",
     "- Lưu được, mở lại thấy đúng nội dung, cột 'Lý do thu' trên lưới xuống dòng chứ không "
     "phá vỡ bố cục bảng."),

    (12, "Lý do thu chứa ký tự đặc biệt và dấu tiếng Việt", "P2",
     "Đang mở form Tạo mới.",
     "1. Nhập Lý do thu = \"Thu tiền đợt 1 <&'> — công nợ quá hạn\".\n2. Lưu nháp, mở lại.",
     "Lý do thu: Thu tiền đợt 1 <&'> — công nợ quá hạn",
     "- Hiển thị đúng nguyên văn ở màn chi tiết, lưới danh sách và bản in."),

    (13, "Ghi chú dòng chi tiết bỏ trống", "P2",
     "Dòng chi tiết đủ khách hàng, hợp đồng, số tiền, ô Ghi chú để trống.",
     "1. Bấm 'Lưu và gửi duyệt' rồi 'Xác nhận'.",
     "—",
     "- Lưu thành công, Ghi chú dòng để trống là hợp lệ."),

    (14, "Mở popup hợp đồng khi chưa chọn khách hàng", "P0",
     "Dòng chi tiết mới thêm, chưa chọn khách hàng.",
     "1. Bấm vào ô hợp đồng của dòng đó.",
     "—",
     "- Ô bị khóa, không mở popup, gợi ý trong ô ghi 'Chọn khách hàng trước'."),
]

S12 = [
    (1, "Hai người cùng lập phiếu một lúc — mã phiếu không trùng", "P0",
     "Hai tài khoản cùng công ty, cùng đăng nhập.",
     "1. Cả hai cùng mở form Tạo mới.\n2. Bấm 'Lưu nháp' gần như cùng lúc.\n"
     "3. Đối chiếu mã 2 phiếu vừa tạo.",
     "—",
     "- Hai mã phiếu khác nhau, số cuối chạy liên tiếp.\n"
     "- ⚠️ Không có phiếu nào bị lỗi lưu."),

    (2, "Mở 2 tab cùng một phiếu — tab kia gửi duyệt trước rồi tab này bấm Lưu", "P0",
     "Phiếu 'Đang tạo' do chính mình lập, mở form Sửa ở 2 tab.",
     "1. Tab 1 bấm 'Lưu và gửi duyệt' rồi 'Xác nhận'.\n"
     "2. Sang tab 2 (vẫn đang mở form Sửa) bấm 'Lưu nháp'.",
     "—",
     "- ⚠️ Tab 2 báo: 'Thao tác không thành công. Dữ liệu đã được thay đổi hoặc chuyển trạng "
     "thái bởi người dùng khác. Vui lòng tải lại trang để cập nhật thông tin mới nhất.'\n"
     "- Phiếu vẫn ở trạng thái 'Chờ KT duyệt', nội dung của tab 2 không đè lên."),

    (3, "Mở 2 tab cùng một phiếu — tab kia gửi duyệt trước rồi tab này bấm Xóa", "P0",
     "Như trên.",
     "1. Tab 1 gửi duyệt phiếu.\n2. Tab 2 bấm ba chấm > Xóa > 'Xóa'.",
     "—",
     "- Hiện đúng câu thông báo dữ liệu đã thay đổi, phiếu KHÔNG bị xóa.\n"
     "- Danh sách tự tải lại cho khớp hiện trạng."),

    (4, "Hai kế toán cùng xử lý một phiếu chờ duyệt", "P0",
     "Hai tài khoản đều có quyền 'Kế toán thanh toán', cùng mở chi tiết một phiếu 'Chờ KT duyệt'.",
     "1. Kế toán 1 bấm 'Không duyệt' và nhập lý do, gửi thành công.\n"
     "2. Kế toán 2 cũng bấm 'Không duyệt', nhập lý do và gửi.",
     "Lý do (cả hai): kiểm thử đồng thời",
     "- Kế toán 2 nhận đúng câu thông báo dữ liệu đã thay đổi, đề nghị tải lại trang.\n"
     "- ⚠️ Phiếu chỉ ghi 1 lần đổi trạng thái, lịch sử không có 2 mốc trùng."),

    (5, "Xem phiếu công ty khác bằng đường dẫn trực tiếp", "P0",
     "Tài khoản D chỉ có quyền 'Xem tất cả phiếu đề nghị thu của công ty' (công ty 1). Phiếu Q "
     "thuộc công ty 4.",
     "1. Gõ thẳng đường dẫn chi tiết của phiếu Q vào trình duyệt.",
     "—",
     "- Hệ thống từ chối, báo không có quyền xem phiếu này và đưa về màn danh sách.\n"
     "- Không lộ bất kỳ dữ liệu nào của phiếu Q."),

    (6, "Xem phiếu nháp của người khác bằng đường dẫn trực tiếp", "P0",
     "Tài khoản E có quyền 'Xem tất cả phiếu đề nghị thu của tổng công ty'. Phiếu N ở trạng "
     "thái 'Đang tạo' do người khác lập.",
     "1. Gõ thẳng đường dẫn chi tiết của phiếu N.",
     "—",
     "- ⚠️ Hệ thống vẫn từ chối: nháp của người khác không ai xem được, kể cả người xem tổng "
     "công ty."),

    (7, "Mở chi tiết phiếu vừa bị người khác xóa", "P1",
     "Người lập vừa xóa phiếu R ở máy khác; người kiểm thử đang mở danh sách cũ có phiếu R.",
     "1. Bấm vào mã phiếu R.",
     "—",
     "- Hệ thống báo không tải được phiếu và đưa về màn danh sách, không treo trang trắng."),
]

S13 = [
    (1, "Luồng đầy đủ: lập nháp → gửi duyệt → không duyệt → sửa → gửi lại", "P0",
     "Tài khoản A (người lập, công ty 1) và tài khoản G (quyền 'Kế toán thanh toán', công ty 1). "
     "Khách hàng X có ít nhất 1 hợp đồng còn hiệu lực.",
     "1. Tài khoản A: Tạo mới, chọn khách hàng X + hợp đồng, số tiền 5,000,000, "
     "Lý do thu 'Thu tiền hàng đợt 1' → 'Lưu nháp'.\n"
     "2. Mở lại phiếu, bấm 'Sửa', đổi số tiền thành 6,000,000 → 'Lưu và gửi duyệt' → 'Xác nhận'.\n"
     "3. Tài khoản G: mở màn chờ duyệt, mở phiếu, bấm 'Không duyệt', lý do 'Sai số tiền'.\n"
     "4. Tài khoản A: mở phiếu, bấm 'Sửa', đổi số tiền thành 5,500,000 → 'Lưu và gửi duyệt'.\n"
     "5. Tài khoản G: mở lại màn chờ duyệt.\n"
     "6. Mở popup Lịch sử của phiếu.",
     "5.000.000 → 6.000.000 → 5.500.000",
     "- Bước 1: trạng thái 'Đang tạo', mã phiếu sinh tự động.\n"
     "- Bước 2: trạng thái 'Chờ KT duyệt', tài khoản G nhận thông báo.\n"
     "- Bước 3: trạng thái 'Không duyệt', Ghi chú hiện 'Sai số tiền'.\n"
     "- Bước 4: trạng thái 'Chờ KT duyệt' trở lại.\n"
     "- Bước 5: phiếu xuất hiện lại trong màn chờ duyệt.\n"
     "- Bước 6: lịch sử đủ các mốc theo thứ tự thời gian, mốc nào cũng có người thực hiện."),

    (2, "Luồng phiếu nhiều khách hàng và ngoại tệ", "P0",
     "Khách hàng X và Y đều có hợp đồng còn hiệu lực. Loại tiền USD có tỷ giá trong danh mục.",
     "1. Tạo mới, đổi Loại tiền sang USD (tỷ giá tự điền).\n"
     "2. Thêm dòng 1: khách hàng X, hợp đồng của X, số tiền 100.\n"
     "3. Thêm dòng 2: khách hàng Y, hợp đồng của Y, số tiền 200.\n"
     "4. 'Lưu và gửi duyệt' → 'Xác nhận'.\n"
     "5. Mở lại chi tiết và bản in.",
     "USD · dòng 1: 100 · dòng 2: 200",
     "- Bảng chi tiết có 2 cột số tiền (USD và VND); tổng cộng đúng cả 2 cột.\n"
     "- Trên lưới, cột 'Khách hàng / Nhà cung cấp' hiện khách hàng của DÒNG ĐẦU TIÊN.\n"
     "- Cột 'Tổng tiền đề nghị' bằng tổng quy đổi VND của cả 2 dòng.\n"
     "- Bản in hiện đủ 2 dòng và dòng 'Tổng cộng (quy đổi VND)'."),

    (3, "Luồng phiếu Thu nhà cung cấp", "P0",
     "Nhà cung cấp Z có ít nhất 1 hợp đồng mua.",
     "1. Tạo mới, đổi Loại thu sang 'Thu nhà cung cấp'.\n"
     "2. Thêm dòng, chọn nhà cung cấp Z và hợp đồng mua, số tiền 3,000,000.\n"
     "3. Lý do thu 'Thu lại tiền hàng trả về' → 'Lưu và gửi duyệt' → 'Xác nhận'.\n"
     "4. Mở chi tiết và bản in.",
     "Nhà cung cấp Z · 3.000.000",
     "- Bảng chi tiết dùng nhãn 'Nhà cung cấp' và 'Hợp đồng mua' ở cả màn nhập, màn xem và "
     "bản in.\n"
     "- Cột 'Loại thu' trên lưới là 'Thu nhà cung cấp'; cột 'Khách hàng / Nhà cung cấp' hiện "
     "tên nhà cung cấp Z."),

    (4, "Luồng lập nháp rồi xóa", "P1",
     "Tài khoản A đang ở màn danh sách.",
     "1. Tạo mới, bấm 'Lưu nháp' ngay khi form còn trống.\n"
     "2. Ghi lại mã phiếu vừa sinh.\n"
     "3. Xóa phiếu đó từ danh sách.\n"
     "4. Tạo mới thêm 1 phiếu và bấm 'Lưu nháp'.",
     "—",
     "- Phiếu nháp tạo và xóa được bình thường.\n"
     "- ⚠️ Mã phiếu mới KHÔNG dùng lại số vừa xóa mà tiếp tục số kế tiếp."),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", S1),
    ("II", "BỘ LỌC & TÌM KIẾM", S2),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", S3),
    ("IV", "TẠO MỚI PHIẾU", S4),
    ("V", "SỬA PHIẾU", S5),
    ("VI", "XEM CHI TIẾT PHIẾU", S6),
    ("VII", "KHÔNG DUYỆT (MÀN CHỜ DUYỆT CỦA KẾ TOÁN)", S7),
    ("VIII", "XÓA PHIẾU", S8),
    ("IX", "IN PHIẾU", S9),
    ("X", "LỊCH SỬ THAY ĐỔI", S10),
    ("XI", "RÀNG BUỘC NHẬP LIỆU", S11),
    ("XII", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", S12),
    ("XIII", "LUỒNG NGHIỆP VỤ TRỌN VẸN", S13),
]

if __name__ == "__main__":
    build(output_file=OUT,
          sheet_name="Trang tính1",
          feature_name="Phiếu đề nghị thu tiền - Cập nhật ngày 28/08/2026",
          module_name=MODULE,
          description_block=DESCRIPTION_BLOCK,
          role_tcs=ROLE_TCS,
          sections=SECTIONS)
