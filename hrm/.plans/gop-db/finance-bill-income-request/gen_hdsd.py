# -*- coding: utf-8 -*-
"""Sinh tai lieu HDSD (.docx) cho man "Phieu de nghi thu tien" (phan he Tai chinh).

Khung + style lay tu `.claude/skills/hdsd-documenter/assets/HDSD_MAU.docx`
(chinh la ban HDSD Danh muc khach hang — man mau user chi dinh).

Anh that: dntt_shots/ (cong dev hrm-crm.eteksofts.com, 28/08/2026) — KHONG commit.

Chay:  python .plans/gop-db/finance-bill-income-request/gen_hdsd.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills",
                                "hdsd-documenter", "assets"))
from hdsd_engine import HdsdBuilder  # noqa: E402

OUT = os.path.join(HERE, "HDSD_Phiếu đề nghị thu tiền.docx")
SHOTS = os.path.join(HERE, "dntt_shots")

b = HdsdBuilder(output=OUT, shots_dir=SHOTS,
                cover_title="(Màn hình: Phiếu đề nghị thu tiền)",
                doc_title="HDSD - Phiếu đề nghị thu tiền")

# ══════════════════════════════════════════════════════════ TỔNG QUAN
b.h1("TỔNG QUAN")

b.h2("1. Thuật ngữ và từ viết tắt")
b.table([
    ["Thuật ngữ", "Giải thích"],
    ["Phiếu đề nghị thu tiền",
     "Chứng từ do người kinh doanh lập để đề nghị kế toán thu tiền của khách hàng (hoặc thu lại "
     "tiền từ nhà cung cấp) theo một hoặc nhiều hợp đồng."],
    ["Loại thu",
     "Phân loại nguồn tiền đề nghị thu. Có 2 giá trị chọn được: Thu bán hàng (thu của khách "
     "hàng theo hợp đồng bán) và Thu nhà cung cấp (thu lại của nhà cung cấp theo hợp đồng mua)."],
    ["Dòng chi tiết",
     "Một dòng trong bảng Chi tiết của phiếu, gồm một khách hàng (hoặc nhà cung cấp), một hợp "
     "đồng của chính đối tượng đó và số tiền đề nghị thu. Một phiếu có thể có nhiều dòng, "
     "nhiều khách hàng."],
    ["Số tiền còn nợ",
     "Số dư công nợ của hợp đồng theo sổ kế toán tại thời điểm mở phiếu. Hệ thống tự tính, "
     "người dùng không nhập và cũng không lưu vào phiếu."],
    ["Số tiền đề nghị thu",
     "Số tiền người lập phiếu đề nghị kế toán thu trên hợp đồng đó."],
    ["Tỷ giá (VND)",
     "Tỷ lệ quy đổi từ loại tiền của phiếu sang đồng Việt Nam. Chọn loại tiền là VNĐ thì tỷ "
     "giá luôn bằng 1 và ô bị khóa."],
    ["Đang tạo", "Phiếu mới lưu nháp, chỉ người lập nhìn thấy và sửa được."],
    ["Chờ KT duyệt", "Phiếu đã gửi, đang chờ kế toán thanh toán xử lý."],
    ["Không duyệt", "Kế toán từ chối phiếu kèm lý do; người lập sửa lại và gửi lại được."],
    ["Đã tạo phiếu thu", "Kế toán đã lập phiếu thu từ phiếu đề nghị này."],
    ["Đã hạch toán", "Phiếu thu tương ứng đã được duyệt và vào sổ kế toán."],
    ["Hủy", "Phiếu thu tương ứng đã bị hủy."],
])

b.h2("2. Cập nhật tài liệu")
b.table([
    ["Phiên bản", "Ngày", "Nội dung", "Người thực hiện"],
    ["1.0", "28/08/2026", "Ban hành lần đầu cho màn Phiếu đề nghị thu tiền và màn Phiếu đề "
                          "nghị thu tiền chờ duyệt.", "Nhóm phát triển HRM"],
])

b.h2("3. Giới thiệu chung")
b.para("Màn hình Phiếu đề nghị thu tiền dùng để lập, theo dõi và xử lý các đề nghị thu tiền "
       "giữa bộ phận kinh doanh và bộ phận kế toán. Người kinh doanh lập phiếu ghi rõ thu của "
       "ai, theo hợp đồng nào, bao nhiêu tiền, vì việc gì; kế toán thanh toán nhận phiếu và "
       "quyết định lập phiếu thu hay từ chối kèm lý do.")
b.para("Màn hình nằm trong phân hệ Tài chính. Có hai đường vào cùng một màn danh sách và một "
       "màn riêng dành cho kế toán:")
b.bullet("Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi → Đề nghị thu tiền — đường dẫn "
         "/finance/bill-income-requests")
b.bullet("Đề nghị → Đề nghị thu tiền — cùng đường dẫn /finance/bill-income-requests")
b.bullet("Phê duyệt - Công nợ - Thu - Chi → Phiếu đề nghị thu tiền chờ duyệt — đường dẫn "
         "/finance/bill-income-requests/pending")
b.para("Các màn con: thêm mới /finance/bill-income-requests/create, xem chi tiết "
       "/finance/bill-income-requests/{số hiệu bản ghi}, chỉnh sửa "
       "/finance/bill-income-requests/{số hiệu bản ghi}/edit, bản in "
       "/finance/bill-income-requests/{số hiệu bản ghi}/print.")

b.h2("4. Quyền và phạm vi dữ liệu")
b.para("Màn hình gắn với 5 quyền. Bốn quyền đầu chỉ quyết định người dùng NHÌN THẤY phiếu của "
       "ai; quyền thứ năm mở phần việc của kế toán.")
b.table([
    ["Tên quyền", "Cho phép làm gì", "Nút / tab tương ứng trên giao diện"],
    ["Xem tất cả phiếu đề nghị thu của tổng công ty",
     "Nhìn thấy phiếu của mọi công ty trong hệ thống.",
     "Bộ lọc nâng cao hiện thêm ô Công ty, Phòng ban, Bộ phận."],
    ["Xem tất cả phiếu đề nghị thu của công ty",
     "Nhìn thấy phiếu thuộc công ty của mình.",
     "Bộ lọc nâng cao hiện ô Phòng ban (và Bộ phận nếu có thêm quyền cấp bộ phận)."],
    ["Xem tất cả phiếu đề nghị thu của phòng ban",
     "Nhìn thấy phiếu thuộc các phòng ban mà mình được giao quản lý, trong công ty của mình.",
     "Bộ lọc nâng cao hiện ô Phòng ban."],
    ["Xem tất cả phiếu đề nghị thu của bộ phận",
     "Nhìn thấy phiếu thuộc các bộ phận mà mình được giao quản lý, trong công ty của mình.",
     "Bộ lọc nâng cao hiện ô Bộ phận."],
    ["Kế toán thanh toán",
     "Mở màn Phiếu đề nghị thu tiền chờ duyệt; từ chối phiếu bằng nút Không duyệt; chuyển sang "
     "lập phiếu thu bằng nút Tạo phiếu thu.",
     "Mục menu Phiếu đề nghị thu tiền chờ duyệt; nút Không duyệt và Tạo phiếu thu ở màn chi tiết."],
])
b.para("Người dùng không có quyền nào trong bốn quyền xem ở trên vẫn vào được màn hình, nhưng "
       "chỉ nhìn thấy phiếu do chính mình lập. Việc lập phiếu không gắn quyền: ai vào được màn "
       "cũng lập được phiếu của mình.")
b.para("Nếu không có quyền Kế toán thanh toán, mục menu Phiếu đề nghị thu tiền chờ duyệt sẽ "
       "không hiển thị; trường hợp truy cập trực tiếp bằng đường dẫn, hệ thống không trả về "
       "phiếu nào và danh sách hiện rỗng.")

# ══════════════════════════════════════════════════════════ PHẦN 1
b.h1("PHẦN 1: TRUY CẬP VÀ BỐ CỤC MÀN HÌNH")

b.h2("1.1. Cách vào màn hình")
b.para("Bước 1: Đăng nhập hệ thống. Bước 2: Chọn phân hệ Tài chính ở góc trên bên trái. "
       "Bước 3: Ở thanh menu bên trái, bấm nhóm Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi, "
       "sau đó bấm Đề nghị thu tiền. Có thể vào cùng màn này bằng nhóm menu Đề nghị → "
       "Đề nghị thu tiền.")

b.h2("1.2. Bố cục chung")
b.image("01-danh-sach.png", "Màn hình danh sách Phiếu đề nghị thu tiền")
b.para("Màn hình chia làm hai khối:")
b.bullet("Khối Bộ lọc danh sách ở trên: ô tìm nhanh theo mã phiếu, nút Tìm kiếm, nút Làm mới, "
         "nút Cài đặt bộ lọc và nút Tìm kiếm nâng cao.")
b.bullet("Khối bảng danh sách ở dưới: tiêu đề bảng, nút Tạo mới, nút Cấu hình cột hiển thị "
         "(biểu tượng hai cột), bảng dữ liệu và thanh phân trang.")

# ══════════════════════════════════════════════════════════ PHẦN 2
b.h1("PHẦN 2: DANH SÁCH PHIẾU ĐỀ NGHỊ THU TIỀN")

b.h2("2.1. Phân quyền và hướng dẫn theo quyền")
b.para("Trước khi làm theo các mục sau, hãy xác định mình đang thuộc nhóm quyền nào — nội dung "
       "nhìn thấy trên cùng một màn hình sẽ khác nhau.")
b.h3("2.1.1. Người dùng không có quyền xem nào")
b.para("Danh sách chỉ hiển thị phiếu do chính người dùng lập. Bộ lọc nâng cao không có ô Công "
       "ty, Phòng ban, Bộ phận. Người dùng vẫn có nút Tạo mới, vẫn sửa và xóa được phiếu của "
       "mình khi phiếu còn ở trạng thái Đang tạo hoặc Không duyệt.")
b.h3("2.1.2. Người dùng có quyền “Xem tất cả phiếu đề nghị thu của bộ phận”")
b.para("Nhìn thấy phiếu của các bộ phận mà mình được giao quản lý, trong công ty của mình. "
       "Bộ lọc nâng cao có thêm ô Bộ phận để thu hẹp danh sách. Người dùng chỉ xem, không sửa "
       "và không xóa được phiếu của người khác.")
b.h3("2.1.3. Người dùng có quyền “Xem tất cả phiếu đề nghị thu của phòng ban”")
b.para("Nhìn thấy phiếu của các phòng ban mà mình được giao quản lý, trong công ty của mình. "
       "Bộ lọc nâng cao có thêm ô Phòng ban.")
b.h3("2.1.4. Người dùng có quyền “Xem tất cả phiếu đề nghị thu của công ty”")
b.para("Nhìn thấy toàn bộ phiếu thuộc công ty của mình, không phân biệt phòng ban hay bộ phận.")
b.h3("2.1.5. Người dùng có quyền “Xem tất cả phiếu đề nghị thu của tổng công ty”")
b.para("Nhìn thấy phiếu của mọi công ty. Bộ lọc nâng cao hiện đủ ba ô Công ty, Phòng ban, "
       "Bộ phận; chọn công ty nào thì ô Phòng ban chỉ liệt kê phòng của công ty đó.")
b.h3("2.1.6. Người dùng có quyền “Kế toán thanh toán”")
b.para("Ngoài màn danh sách, người dùng có thêm mục menu Phiếu đề nghị thu tiền chờ duyệt. "
       "Ở màn chi tiết của phiếu đang Chờ KT duyệt, người dùng thấy thêm hai nút: Tạo phiếu thu "
       "và Không duyệt. Hướng dẫn chi tiết ở PHẦN 6.")
b.para("Lưu ý chung cho mọi quyền: phiếu ở trạng thái Đang tạo của người khác luôn bị ẩn, kể cả "
       "với người có quyền xem toàn tổng công ty.")

b.h2("2.2. Tìm kiếm nhanh")
b.para("Ô Tìm theo mã phiếu ở đầu màn hình tìm theo mã phiếu. Gõ một phần mã rồi bấm nút "
       "Tìm kiếm. Đây là ô duy nhất phải bấm nút mới lọc; mọi tiêu chí trong Tìm kiếm nâng cao "
       "lọc ngay khi vừa chọn hoặc vừa nhập.")
b.para("Nút Làm mới xóa sạch mọi tiêu chí đang lọc, kể cả ô tìm nhanh, và tải lại danh sách "
       "từ trang 1.")

b.h2("2.3. Bộ lọc nâng cao")
b.para("Bấm nút Tìm kiếm nâng cao để mở khối tiêu chí. Bấm lại (nút đổi tên thành "
       "Ẩn tìm kiếm nâng cao) để thu gọn.")
b.image("02-bo-loc.png", "Bộ lọc nâng cao ở trạng thái mở đầy đủ tiêu chí")
b.table([
    ["Tiêu chí", "Kiểu nhập", "Cách dùng"],
    ["Công ty", "Danh sách chọn",
     "Chỉ hiện với người có quyền xem tổng công ty. Đổi công ty thì ô Phòng ban và Bộ phận tự "
     "xóa giá trị cũ."],
    ["Phòng ban", "Danh sách chọn",
     "Chỉ liệt kê phòng ban thuộc công ty đang chọn."],
    ["Bộ phận", "Danh sách chọn",
     "Chỉ hiện với người có quyền xem theo cấp bộ phận."],
    ["Loại thu", "Danh sách chọn", "Hai giá trị: Thu bán hàng, Thu nhà cung cấp."],
    ["Trạng thái", "Danh sách chọn",
     "Sáu giá trị: Đang tạo, Chờ KT duyệt, Đã tạo phiếu thu, Đã hạch toán, Hủy, Không duyệt."],
    ["Số đơn hàng/hợp đồng", "Ô gõ tay",
     "Tìm theo số hợp đồng nằm trong các dòng chi tiết của phiếu, không phải mã phiếu."],
    ["Khách hàng", "Ô gõ tay", "Gõ mã hoặc tên khách hàng đều ra kết quả."],
    ["Nhà cung cấp", "Danh sách chọn có tìm kiếm",
     "Gõ từ 2 ký tự trở lên để hệ thống gợi ý, chọn một nhà cung cấp trong danh sách gợi ý."],
    ["Người tạo", "Danh sách chọn", "Chọn nhân sự đã lập phiếu."],
    ["Số tiền đề nghị từ / đến", "Hai ô số tiền",
     "So sánh trên TỔNG tiền đề nghị (đã quy đổi VND) của cả phiếu. Bỏ trống một đầu thì phía "
     "đó không giới hạn."],
    ["Ngày tạo từ / đến", "Hai ô chọn ngày",
     "Lọc theo ngày lập phiếu. Cả hai mốc lấy trọn ngày."],
])

b.h2("2.4. Cài đặt bộ lọc (chọn tiêu chí muốn hiển thị)")
b.para("Nút Cài đặt bộ lọc mở cửa sổ cho phép bật/tắt và sắp xếp lại các tiêu chí lọc. Cấu hình "
       "này lưu riêng cho từng tài khoản và từng màn hình.")
b.image("04-cai-dat-bo-loc.png", "Cửa sổ Cài đặt bộ lọc với đủ 9 tiêu chí")
b.bullet("Tích hoặc bỏ tích ô vuông trước tên tiêu chí để hiện hoặc ẩn tiêu chí đó.")
b.bullet("Kéo biểu tượng sáu chấm để đổi thứ tự tiêu chí.")
b.bullet("Bấm Lưu để ghi nhận; hệ thống báo Cập nhật thành công và bộ lọc đổi ngay.")
b.bullet("Bấm Khôi phục mặc định để bật lại đủ 9 tiêu chí theo thiết kế, sau đó vẫn phải bấm Lưu.")
b.bullet("Bấm Đóng để thoát mà không lưu.")
b.para("Lưu ý: bỏ tích một tiêu chí thì giá trị đang lọc của tiêu chí đó cũng bị xóa, danh sách "
       "không bị lọc ngầm bởi ô không nhìn thấy.")

b.h2("2.5. Các cột của danh sách")
b.image("05-danh-sach-hanh-dong.png", "Phần bên phải của bảng: Trạng thái và cột Hành động")
b.table([
    ["Cột", "Ý nghĩa"],
    ["STT", "Số thứ tự, chạy liên tục qua các trang. Cột bắt buộc, không ẩn được."],
    ["Mã phiếu",
     "Mã do hệ thống tự sinh theo dạng <mã công ty>.DNTT<tháng năm>.<5 chữ số>. Bấm vào mã để "
     "mở màn chi tiết. Sắp xếp được. Cột bắt buộc, không ẩn được."],
    ["Loại thu", "Thu bán hàng hoặc Thu nhà cung cấp."],
    ["Khách hàng / Nhà cung cấp",
     "Đối tượng của dòng chi tiết ĐẦU TIÊN trong phiếu, hiển thị dạng mã - tên."],
    ["Lý do thu", "Nội dung người lập nhập ở ô Lý do thu."],
    ["Phòng ban", "Phòng ban của người lập phiếu tại thời điểm lập."],
    ["Tổng tiền đề nghị",
     "Tổng số tiền đề nghị thu (đã quy đổi VND) của mọi dòng chi tiết."],
    ["Người tạo", "Người đã lập phiếu."],
    ["Ngày tạo", "Ngày giờ lập phiếu, dạng ngày/tháng/năm giờ:phút. Sắp xếp được."],
    ["Người cập nhật", "Người sửa phiếu gần nhất."],
    ["Ngày cập nhật", "Ngày giờ sửa gần nhất. Sắp xếp được."],
    ["Trạng thái",
     "Một trong sáu trạng thái. Đã tạo phiếu thu và Đã hạch toán hiện nền xanh; bốn trạng thái "
     "còn lại hiện nền đỏ."],
    ["Hành động", "Các nút thao tác của dòng. Cột bắt buộc, không ẩn được."],
])

b.h2("2.6. Tuỳ chỉnh cột hiển thị")
b.para("Bấm nút biểu tượng hai cột bên phải nút Tạo mới để mở cửa sổ Tuỳ chỉnh cột.")
b.image("03-cau-hinh-cot.png", "Cửa sổ Tuỳ chỉnh cột")
b.bullet("Bỏ tích một cột để ẩn cột đó khỏi bảng.")
b.bullet("Kéo biểu tượng ba gạch để đổi thứ tự cột.")
b.bullet("Ba cột STT, Mã phiếu và Hành động bị khóa (biểu tượng ổ khóa, chú thích “Cột bắt buộc "
         "— không thể ẩn hoặc đổi vị trí”).")
b.bullet("Bấm Lưu để ghi nhận, bấm Đóng để thoát mà không lưu.")
b.para("Cấu hình cột lưu riêng cho từng tài khoản và dùng chung cho cả màn danh sách lẫn màn "
       "Phiếu đề nghị thu tiền chờ duyệt.")

b.h2("2.7. Sắp xếp và phân trang")
b.para("Bấm vào tiêu đề các cột có biểu tượng mũi tên (Mã phiếu, Ngày tạo, Ngày cập nhật) để "
       "sắp xếp; bấm lần nữa để đảo chiều. Mỗi lần sắp xếp, danh sách quay về trang 1. Mặc định "
       "khi mới vào màn, phiếu lập gần nhất đứng đầu.")
b.para("Dưới bảng có dòng đếm dạng “Hiển thị 1–10 / 2496”: hai số đầu là khoảng dòng của trang "
       "đang xem, số cuối là tổng số phiếu khớp bộ lọc hiện tại. Ô Số dòng/trang cho phép đổi "
       "số dòng mỗi trang; đổi xong danh sách quay về trang 1.")
b.para("Hệ thống ghi nhớ bộ lọc trong 10 phút: bấm vào một phiếu rồi quay lại, các tiêu chí vừa "
       "đặt vẫn còn. Muốn bắt đầu lại từ đầu thì bấm Làm mới.")

b.h2("2.8. Các nút thao tác trên từng dòng")
b.para("Cột Hành động hiển thị tối đa ba nút; các thao tác còn lại nằm trong nút ba chấm.")
b.image("18-menu-hanh-dong.png", "Nút ba chấm mở thêm hai thao tác Xóa và Lịch sử")
b.table([
    ["Nút", "Tác dụng", "Điều kiện hiển thị"],
    ["Sửa (biểu tượng bút chì)", "Mở màn chỉnh sửa phiếu.",
     "Phiếu do chính người đăng nhập lập và đang ở trạng thái Đang tạo hoặc Không duyệt. "
     "Không hiện ở màn chờ duyệt."],
    ["In phiếu (biểu tượng máy in)", "Mở bản in của phiếu ở tab mới.", "Luôn hiển thị."],
    ["Tạo phiếu thu", "Chuyển sang màn lập Phiếu thu, gắn sẵn phiếu đề nghị này.",
     "Người dùng có quyền Kế toán thanh toán, phiếu đang Chờ KT duyệt và chưa có phiếu thu nào "
     "lập từ phiếu này."],
    ["Xóa (trong nút ba chấm)", "Xóa hẳn phiếu và toàn bộ dòng chi tiết.",
     "Cùng điều kiện với nút Sửa."],
    ["Lịch sử (trong nút ba chấm)", "Mở cửa sổ Lịch sử thay đổi của phiếu.", "Luôn hiển thị."],
])
b.para("Màn hình không có nút Xem chi tiết riêng — bấm vào mã phiếu ở cột Mã phiếu để mở chi "
       "tiết. Bấm chuột phải vào mã phiếu để mở ở tab mới.")

# ══════════════════════════════════════════════════════════ PHẦN 3
b.h1("PHẦN 3: LẬP PHIẾU ĐỀ NGHỊ THU TIỀN")

b.h2("3.1. Mở màn lập phiếu")
b.para("Ở màn danh sách, bấm nút Tạo mới (biểu tượng dấu cộng) trên thanh công cụ của bảng. "
       "Hệ thống mở màn Thêm phiếu đề nghị thu tiền theo đường dẫn "
       "/finance/bill-income-requests/create.")
b.image("06-tao-moi.png", "Màn lập phiếu khi vừa mở")
b.para("Màn hình gồm ba khối: Thông tin chung, Chi tiết và Ghi chú; thanh nút Lưu nháp, "
       "Lưu và gửi duyệt, Quay lại nằm cố định ở đáy màn hình.")

b.h2("3.2. Khối Thông tin chung — từng trường nhập")
b.table([
    ["Trường", "Kiểu nhập", "Bắt buộc", "Giá trị điền sẵn khi tạo mới", "Ghi chú"],
    ["Loại thu", "Danh sách chọn", "Có", "Thu bán hàng",
     "Hai giá trị: Thu bán hàng, Thu nhà cung cấp. Quyết định bảng Chi tiết chọn khách hàng hay "
     "nhà cung cấp."],
    ["Loại tiền", "Danh sách chọn", "Có", "VNĐ — VietNamDong",
     "Danh sách hiển thị dạng mã — tên. Đổi loại tiền sẽ tự điền tỷ giá tương ứng."],
    ["Tỷ giá (VND)", "Ô số tiền", "Có", "1 (ô bị khóa)",
     "Ô mở khóa khi loại tiền khác VNĐ. Phải lớn hơn 0."],
    ["Lý do thu", "Ô gõ tay", "Có khi gửi duyệt", "Trống",
     "Lưu nháp thì được phép bỏ trống; bấm Lưu và gửi duyệt mà bỏ trống sẽ báo lỗi."],
    ["Ghi chú", "Ô nhiều dòng", "Không", "Trống",
     "Nằm ở khối Ghi chú cuối màn hình. Khi phiếu bị từ chối, ô này chứa lý do không duyệt của "
     "kế toán."],
])
b.para("Giá trị điền sẵn khi tạo mới: Loại thu = Thu bán hàng; Loại tiền = VNĐ — VietNamDong; "
       "Tỷ giá (VND) = 1 và bị khóa; Lý do thu, Ghi chú và bảng Chi tiết đều trống. Màn lập "
       "phiếu KHÔNG có ô Mã phiếu, ô Người tạo và ô Phòng ban — ba thông tin này hệ thống tự "
       "gán khi lưu: mã phiếu sinh tự động, người tạo là người đang đăng nhập, phòng ban là "
       "phòng ban của người đó.")

b.h2("3.3. Nhập bảng Chi tiết")
b.h3("3.3.1. Thêm một dòng")
b.para("Bấm dấu cộng ở góc phải hàng tiêu đề của bảng Chi tiết. Một dòng trống được thêm vào "
       "với số thứ tự tăng dần.")
b.image("07-tao-moi-them-dong.png", "Bảng Chi tiết sau khi thêm một dòng trống")
b.para("Ô khách hàng hiện gợi ý “Nhấn vào đây để chọn khách hàng”. Ô hợp đồng đang bị khóa và "
       "hiện gợi ý “Chọn khách hàng trước” — phải chọn đối tượng trước rồi mới chọn được hợp đồng.")

b.h3("3.3.2. Chọn khách hàng cho dòng")
b.para("Bấm thẳng vào ô khách hàng của dòng đó, cửa sổ Chọn khách hàng mở ra.")
b.image("08-popup-khach-hang.png", "Cửa sổ Chọn khách hàng")
b.bullet("Có ba ô tìm: Tên / Mã khách hàng, Mã số thuế, Số điện thoại. Nhập rồi bấm Tìm kiếm; "
         "bấm Làm mới để xóa điều kiện tìm.")
b.bullet("Bảng kết quả gồm các cột: STT, Mã KH - Tên khách hàng, Loại, MST, SĐT, Email, "
         "Nhóm KH, Địa chỉ, Tỉnh/TP; có phân trang ở cuối.")
b.bullet("Bấm vào dòng khách hàng cần chọn. Cửa sổ tự đóng, ô khách hàng của dòng hiện "
         "mã - tên khách hàng, đồng thời ô hợp đồng được mở khóa.")
b.para("Mỗi dòng chi tiết chọn khách hàng riêng, vì vậy một phiếu có thể gom nhiều khách hàng "
       "khác nhau.")

b.h3("3.3.3. Chọn hợp đồng cho dòng")
b.para("Bấm vào ô hợp đồng của dòng, cửa sổ Chọn đơn hàng/hợp đồng mở ra. Dòng phụ dưới tiêu "
       "đề cửa sổ hiển thị đúng khách hàng của dòng đang thao tác.")
b.image("09-popup-hop-dong.png", "Cửa sổ Chọn đơn hàng/hợp đồng của một khách hàng")
b.bullet("Bảng gồm các cột: STT, Số đơn hàng/Hợp đồng, Ngày lập, Giá trị hợp đồng, "
         "Số tiền còn nợ.")
b.bullet("Ô Số đơn hàng/Hợp đồng cùng nút Tìm kiếm và Làm mới dùng để lọc nhanh khi khách hàng "
         "có nhiều hợp đồng.")
b.bullet("Bấm vào dòng hợp đồng để chọn. Cửa sổ tự đóng; ô hợp đồng hiện số hợp đồng và cột "
         "Số tiền còn nợ của dòng được điền tự động theo sổ kế toán.")
b.bullet("Hợp đồng đã được chọn ở một dòng khác của cùng phiếu sẽ hiện chú thích “Hợp đồng đã "
         "có trong phiếu” và không bấm chọn lại được.")
b.para("Danh sách hợp đồng bán chỉ gồm hợp đồng từ trạng thái Có hiệu lực trở lên, cùng với "
       "hợp đồng đầu kỳ và hợp đồng bảo dưỡng của khách hàng đó. Hợp đồng còn nháp hoặc chưa "
       "hiệu lực sẽ không xuất hiện.")

b.h3("3.3.4. Nhập số tiền và ghi chú của dòng")
b.para("Nhập số tiền vào ô Số tiền đề nghị thu. Ô tự thêm dấu phẩy ngăn nghìn. Dòng Tổng cộng "
       "ở cuối bảng cập nhật ngay theo từng phím gõ, gồm tổng Số tiền còn nợ và tổng Số tiền "
       "đề nghị thu. Ô Ghi chú của dòng không bắt buộc.")
b.image("10-tao-moi-da-chon.png", "Một dòng chi tiết đã chọn đủ khách hàng và hợp đồng")

b.h3("3.3.5. Xóa một dòng")
b.para("Bấm biểu tượng thùng rác ở cuối dòng. Dòng bị xóa ngay, các dòng sau được đánh số lại "
       "và dòng Tổng cộng tính lại.")

b.h3("3.3.6. Đổi khách hàng của dòng đã chọn hợp đồng")
b.para("Bấm lại vào ô khách hàng và chọn khách hàng khác. Hệ thống xóa hợp đồng đã chọn của "
       "dòng đó và đưa Số tiền còn nợ về 0, vì hợp đồng của khách hàng cũ không còn hợp lệ. "
       "Người dùng phải chọn lại hợp đồng.")

b.h2("3.4. Đổi Loại thu")
b.para("Nếu bảng Chi tiết đang có dòng, việc đổi Loại thu sẽ xóa hết các dòng đó. Hệ thống hỏi "
       "lại trước khi xóa.")
b.image("25-xac-nhan-doi-loai-thu.png", "Hộp thoại xác nhận khi đổi Loại thu")
b.bullet("Bấm Xác nhận: toàn bộ dòng chi tiết bị xóa; tiêu đề cột đổi thành Nhà cung cấp và "
         "Hợp đồng mua (hoặc ngược lại).")
b.bullet("Bấm Hủy: các dòng chi tiết được giữ nguyên.")
b.para("Với loại thu Thu nhà cung cấp, ô đối tượng của dòng mở cửa sổ Chọn nhà cung cấp — có "
       "một ô tìm Mã / Tên nhà cung cấp và bảng ba cột STT, Mã nhà cung cấp, Tên nhà cung cấp.")
b.image("22-popup-nha-cung-cap.png", "Cửa sổ Chọn nhà cung cấp")

b.h2("3.5. Lập phiếu bằng ngoại tệ")
b.para("Đổi ô Loại tiền sang một loại tiền khác VNĐ: ô Tỷ giá (VND) mở khóa và tự điền tỷ giá "
       "của loại tiền đó, người dùng vẫn sửa tay được. Bảng Chi tiết tách cột Số tiền đề nghị "
       "thu thành hai cột con: cột theo ngoại tệ để nhập và cột VND để hiển thị số quy đổi. "
       "Số quy đổi bằng số tiền nhập nhân với tỷ giá. Đổi lại về VNĐ thì tỷ giá tự về 1, ô bị "
       "khóa và cột quy đổi biến mất.")

b.h2("3.6. Lưu phiếu")
b.image("11-tao-moi-ghi-chu.png", "Toàn bộ màn lập phiếu: Thông tin chung, Chi tiết và Ghi chú")
b.table([
    ["Nút", "Tác dụng", "Ràng buộc dữ liệu", "Kết quả"],
    ["Lưu nháp", "Lưu phiếu ở trạng thái Đang tạo.",
     "Được phép bỏ trống Lý do thu và chưa có dòng chi tiết nào. Dòng chi tiết đã thêm thì vẫn "
     "phải có đủ đối tượng, hợp đồng và số tiền.",
     "Báo “Lưu phiếu đề nghị thu thành công!”, quay về danh sách, phiếu ở trạng thái Đang tạo "
     "và chỉ người lập nhìn thấy."],
    ["Lưu và gửi duyệt", "Lưu phiếu và chuyển sang trạng thái Chờ KT duyệt.",
     "Bắt buộc có Lý do thu và ít nhất một dòng chi tiết đầy đủ.",
     "Hiện hộp xác nhận; sau khi xác nhận báo “Gửi duyệt phiếu đề nghị thu thành công!”, phiếu "
     "vào màn chờ duyệt của kế toán cùng công ty."],
    ["Quay lại", "Thoát về danh sách.", "—",
     "Nếu đã nhập dở, hệ thống hỏi lại trước khi thoát."],
])
b.para("Bấm Lưu và gửi duyệt, hệ thống hiện hộp thoại Xác nhận lưu và gửi duyệt với câu hỏi "
       "“Bạn đồng ý lưu và duyệt?”. Bấm Xác nhận để gửi, bấm Hủy để quay lại form.")
b.image("12-xac-nhan-gui-duyet.png", "Hộp thoại xác nhận trước khi gửi duyệt")
b.para("Khi phiếu được gửi duyệt, hệ thống gửi thông báo qua chuông tới các kế toán thanh toán "
       "CÙNG CÔNG TY với phiếu, nội dung dạng “[DNTT] Chờ duyệt: <mã phiếu>. Người đề nghị: "
       "<tên>. Số tiền: <tổng tiền>”. Bấm vào thông báo sẽ mở đúng phiếu. Sửa lại một phiếu đã "
       "ở trạng thái Chờ KT duyệt không làm gửi thông báo thêm lần nữa.")

b.h2("3.7. Báo lỗi khi thiếu thông tin bắt buộc")
b.para("Bấm Lưu và gửi duyệt khi còn thiếu dữ liệu, hệ thống báo lỗi đỏ ngay dưới từng ô thiếu "
       "và không lưu gì cả.")
b.image("24-loi-validate.png", "Thông báo bắt buộc nhập ở ô Lý do thu và dưới bảng Chi tiết")
b.table([
    ["Trường hợp", "Thông báo hiển thị"],
    ["Bỏ trống Lý do thu khi gửi duyệt", "Bắt buộc nhập (ngay dưới ô Lý do thu, ô viền đỏ)"],
    ["Chưa có dòng chi tiết nào khi gửi duyệt", "Bắt buộc nhập (ngay dưới bảng Chi tiết)"],
    ["Dòng chi tiết chưa chọn khách hàng / nhà cung cấp",
     "Bắt buộc nhập (dưới ô đối tượng của đúng dòng đó)"],
    ["Dòng chi tiết chưa chọn hợp đồng", "Bắt buộc nhập (dưới ô hợp đồng của đúng dòng đó)"],
    ["Tỷ giá bằng 0 hoặc bỏ trống", "Phải lớn hơn 0"],
])
b.para("Thêm một dòng chi tiết mới thì câu báo lỗi dưới bảng biến mất ngay. Xóa một dòng đang "
       "báo lỗi cũng xóa luôn câu báo lỗi của dòng đó, không dính sang dòng khác.")

b.h2("3.8. Cảnh báo khi thoát mà chưa lưu")
b.para("Nếu đã nhập hoặc sửa bất kỳ ô nào rồi bấm Quay lại (hoặc rời khỏi màn hình), hệ thống "
       "hiện hộp thoại Thông tin chưa lưu.")
b.image("13-canh-bao-chua-luu.png", "Hộp thoại cảnh báo thông tin chưa lưu")
b.bullet("Bấm Thoát: rời màn hình, dữ liệu đang nhập bị bỏ, không phiếu nào được tạo.")
b.bullet("Bấm Ở lại: quay lại form, dữ liệu vẫn còn nguyên.")
b.para("Chưa chạm vào ô nào mà bấm Quay lại thì hệ thống thoát thẳng, không hỏi.")

# ══════════════════════════════════════════════════════════ PHẦN 4
b.h1("PHẦN 4: CHỈNH SỬA PHIẾU")
b.para("Yêu cầu: phiếu do CHÍNH người đăng nhập lập và đang ở trạng thái Đang tạo hoặc "
       "Không duyệt. Phiếu của người khác, hoặc phiếu đã ở trạng thái khác, sẽ không có nút Sửa.")
b.para("Cách mở: bấm nút Sửa (biểu tượng bút chì) ở cột Hành động của dòng, hoặc mở chi tiết "
       "phiếu rồi bấm nút Sửa ở thanh nút dưới cùng.")
b.image("21-sua.png", "Màn chỉnh sửa phiếu đề nghị thu tiền")
b.para("So với màn lập mới, màn chỉnh sửa có thêm ba ô chỉ để xem, không sửa được:")
b.table([
    ["Trường", "Nội dung"],
    ["Mã phiếu", "Mã hệ thống đã sinh khi lưu lần đầu, không đổi được."],
    ["Người tạo", "Người đã lập phiếu."],
    ["Phòng ban", "Phòng ban của người lập tại thời điểm lập phiếu."],
])
b.para("Góc phải tiêu đề khối Thông tin chung hiển thị người tạo và ngày lập phiếu.")
b.para("Cách nhập bảng Chi tiết, đổi loại thu, chọn khách hàng / nhà cung cấp và hợp đồng giống "
       "hệt PHẦN 3. Hai nút lưu cũng giống: Lưu nháp giữ phiếu ở trạng thái hiện tại, "
       "Lưu và gửi duyệt đưa phiếu sang Chờ KT duyệt.")
b.para("Trường hợp phiếu bị kế toán từ chối: người lập mở phiếu ở trạng thái Không duyệt, đọc "
       "lý do trong ô Ghi chú, sửa lại nội dung rồi bấm Lưu và gửi duyệt để gửi lại. Phiếu quay "
       "về màn chờ duyệt của kế toán.")
b.para("Nếu trong lúc đang sửa, phiếu bị người khác đổi trạng thái (ví dụ mở hai tab và tab kia "
       "vừa gửi duyệt), khi bấm lưu hệ thống báo: “Thao tác không thành công. Dữ liệu đã được "
       "thay đổi hoặc chuyển trạng thái bởi người dùng khác. Vui lòng tải lại trang để cập nhật "
       "thông tin mới nhất.” Hãy tải lại trang rồi thao tác lại.")

# ══════════════════════════════════════════════════════════ PHẦN 5
b.h1("PHẦN 5: XEM CHI TIẾT PHIẾU")
b.para("Bấm vào mã phiếu ở cột Mã phiếu để mở màn chi tiết. Tiêu đề trang hiển thị "
       "“Chi tiết phiếu đề nghị thu tiền: <mã phiếu>”.")
b.image("15-chi-tiet.png", "Màn chi tiết phiếu đề nghị thu tiền")
b.para("Màn chi tiết dùng chung bố cục với màn nhập nhưng mọi ô đều bị khóa: không gõ được, "
       "bấm vào ô khách hàng cũng không mở cửa sổ chọn. Bảng Chi tiết hiển thị đầy đủ các dòng "
       "kèm dòng Tổng cộng.")
b.para("Số tiền còn nợ trên màn chi tiết được tính lại theo sổ kế toán tại thời điểm mở phiếu, "
       "không phải số đã lưu lúc lập. Vì vậy giá trị này có thể khác giữa hai lần xem nếu sổ kế "
       "toán có phát sinh mới.")
b.para("Thanh nút dưới cùng thay đổi theo trạng thái phiếu và quyền của người xem:")
b.table([
    ["Nút", "Khi nào hiển thị"],
    ["Sửa", "Phiếu do chính mình lập, đang ở trạng thái Đang tạo hoặc Không duyệt."],
    ["Xóa", "Cùng điều kiện với nút Sửa."],
    ["In phiếu", "Luôn hiển thị."],
    ["Tạo phiếu thu",
     "Người xem có quyền Kế toán thanh toán, phiếu đang Chờ KT duyệt và chưa có phiếu thu nào "
     "lập từ phiếu này."],
    ["Không duyệt",
     "Người xem có quyền Kế toán thanh toán và phiếu đang ở trạng thái Chờ KT duyệt."],
    ["Quay lại", "Luôn hiển thị, đưa về màn danh sách."],
])
b.para("Cuối màn chi tiết là khối Lịch sử — xem PHẦN 9.")

# ══════════════════════════════════════════════════════════ PHẦN 6
b.h1("PHẦN 6: MÀN CHỜ DUYỆT VÀ THAO TÁC KHÔNG DUYỆT")
b.para("Phần này chỉ áp dụng cho người dùng có quyền Kế toán thanh toán.")

b.h2("6.1. Mở màn chờ duyệt")
b.para("Ở menu bên trái, bấm nhóm Phê duyệt - Công nợ - Thu - Chi rồi bấm "
       "Phiếu đề nghị thu tiền chờ duyệt (đường dẫn /finance/bill-income-requests/pending).")
b.image("14-cho-duyet.png", "Màn Phiếu đề nghị thu tiền chờ duyệt")
b.para("Màn này dùng chung bố cục, bộ cột và bộ tiêu chí lọc với màn danh sách, chỉ khác:")
b.bullet("Chỉ hiển thị phiếu ở trạng thái Chờ KT duyệt và thuộc công ty của người đăng nhập, "
         "kể cả người đó có quyền xem toàn tổng công ty.")
b.bullet("Không có nút Tạo mới; cột Hành động không có nút Sửa và nút Xóa.")
b.bullet("Bộ lọc của màn này lưu riêng, không dùng chung với màn danh sách.")
b.para("Nếu không có quyền Kế toán thanh toán, mục menu này sẽ không hiển thị; trường hợp truy "
       "cập trực tiếp bằng đường dẫn, danh sách hiện rỗng.")

b.h2("6.2. Xử lý một phiếu chờ duyệt")
b.para("Bấm vào mã phiếu để mở chi tiết. Kế toán có hai lựa chọn:")
b.bullet("Đồng ý: bấm Tạo phiếu thu — hệ thống chuyển sang màn lập Phiếu thu và gắn sẵn phiếu "
         "đề nghị này. Trạng thái phiếu đề nghị chỉ đổi khi phiếu thu được lập và duyệt ở màn "
         "Phiếu thu, không đổi ngay tại đây.")
b.bullet("Từ chối: bấm Không duyệt — xem mục 6.3.")
b.para("Nút Tạo phiếu thu sẽ không hiển thị nếu phiếu đề nghị này đã có một phiếu thu (kể cả "
       "phiếu thu còn ở dạng nháp). Nút Không duyệt vẫn hiển thị trong trường hợp đó.")

b.h2("6.3. Không duyệt phiếu — yêu cầu quyền Kế toán thanh toán")
b.para("Bấm nút Không duyệt ở thanh nút dưới cùng của màn chi tiết. Hộp thoại Không duyệt phiếu "
       "mở ra, dòng phụ hiển thị mã phiếu đang xử lý.")
b.image("17-khong-duyet.png", "Hộp thoại Không duyệt phiếu")
b.table([
    ["Trường", "Kiểu nhập", "Bắt buộc", "Giá trị điền sẵn", "Ghi chú"],
    ["Lý do không duyệt", "Ô nhiều dòng", "Có", "Trống",
     "Nội dung này được ghi vào ô Ghi chú của phiếu và hiện trên bản in cũng như trong lịch sử "
     "thay đổi. Người lập phiếu sẽ đọc được."],
])
b.bullet("Bỏ trống hoặc chỉ gõ khoảng trắng rồi bấm Không duyệt: hệ thống báo lỗi đỏ ngay dưới "
         "ô — “Bắt buộc nhập lý do không duyệt”, hộp thoại không đóng.")
b.bullet("Nhập lý do rồi bấm nút Không duyệt: hệ thống báo “Không duyệt phiếu đề nghị thu thành "
         "công!”, hộp thoại đóng, màn chi tiết nạp lại với trạng thái Không duyệt và ô Ghi chú "
         "chứa lý do vừa nhập.")
b.bullet("Bấm Đóng: thoát hộp thoại, phiếu không đổi. Mở lại lần sau ô lý do trở về trống.")
b.para("Sau khi bị không duyệt, phiếu rời khỏi màn chờ duyệt và quay lại cho người lập chỉnh "
       "sửa. Nếu một kế toán khác vừa xử lý phiếu này trước đó, hệ thống báo dữ liệu đã được "
       "thay đổi và đề nghị tải lại trang — phiếu chỉ ghi nhận một lần xử lý.")

# ══════════════════════════════════════════════════════════ PHẦN 7
b.h1("PHẦN 7: XÓA PHIẾU")
b.para("Yêu cầu: phiếu do chính người đăng nhập lập và đang ở trạng thái Đang tạo hoặc "
       "Không duyệt. Phiếu đã gửi duyệt hoặc phiếu của người khác không có nút Xóa.")
b.para("Cách 1 — từ danh sách: bấm nút ba chấm ở cột Hành động của dòng, chọn Xóa. "
       "Cách 2 — từ màn chi tiết: bấm nút Xóa ở thanh nút dưới cùng.")
b.image("19-xac-nhan-xoa.png", "Hộp thoại xác nhận xóa phiếu")
b.bullet("Hộp thoại Xác nhận xóa hiển thị câu hỏi kèm đúng mã phiếu sắp xóa.")
b.bullet("Bấm Xóa: hệ thống báo “Xóa thành công”, phiếu và toàn bộ dòng chi tiết bị xóa hẳn, "
         "danh sách tự tải lại.")
b.bullet("Bấm Hủy: đóng hộp thoại, phiếu giữ nguyên.")
b.para("Lưu ý: phiếu đã xóa không khôi phục được, và mã phiếu đã dùng không được cấp lại cho "
       "phiếu mới.")

# ══════════════════════════════════════════════════════════ PHẦN 8
b.h1("PHẦN 8: IN PHIẾU")
b.para("Bấm nút hình máy in ở cột Hành động của dòng, hoặc nút In phiếu ở màn chi tiết. Hệ "
       "thống mở một tab mới hiển thị bản in. Chức năng này không gắn quyền riêng: ai xem được "
       "phiếu thì in được phiếu.")
b.image("23-in-phieu.png", "Bản in Giấy đề nghị thu tiền")
b.para("Bản in gồm các phần:")
b.bullet("Đầu trang: logo và thông tin công ty.")
b.bullet("Tiêu đề: GIẤY ĐỀ NGHỊ THU TIỀN, kèm dòng “Số phiếu: <mã phiếu> · Ngày lập: <ngày giờ>”.")
b.bullet("Khối thông tin chia đều hai cột — bên trái: Người đề nghị, Loại thu, Trạng thái; "
         "bên phải: Phòng ban, Loại tiền (kèm tỷ giá), Lý do thu.")
b.bullet("Bảng chi tiết: STT, Khách hàng (hoặc Nhà cung cấp), Số đơn hàng/Hợp đồng (hoặc "
         "Hợp đồng mua), Số tiền còn nợ, Số tiền đề nghị thu, Ghi chú; dòng cuối là "
         "“Tổng cộng (quy đổi VND)”.")
b.bullet("Dòng ghi chú: với phiếu đang ở trạng thái Không duyệt, nhãn là “Lý do không duyệt:”; "
         "các trạng thái khác nhãn là “Ghi chú:”.")
b.bullet("Khối ký tên ba ô: NGƯỜI ĐỀ NGHỊ, KẾ TOÁN, GIÁM ĐỐC, mỗi ô có dòng "
         "“(Ký, ghi rõ họ tên)”. Ô NGƯỜI ĐỀ NGHỊ điền sẵn tên người lập; ô KẾ TOÁN điền sẵn tên "
         "người đã xử lý phiếu (nếu có).")
b.para("Bấm nút In màu xanh ở góc trên bên trái để mở hộp thoại in của trình duyệt. Nút In và "
       "menu bên trái không xuất hiện trên bản in.")

# ══════════════════════════════════════════════════════════ PHẦN 9
b.h1("PHẦN 9: LỊCH SỬ THAY ĐỔI")
b.para("Mọi thao tác ghi dữ liệu trên phiếu đều được lưu vết. Chức năng này không gắn quyền "
       "riêng, hiển thị ở cả màn danh sách lẫn màn chờ duyệt.")
b.para("Cách 1 — từ danh sách: bấm nút hình đồng hồ quay ngược ở cột Hành động (nếu dòng có "
       "nhiều nút, mở nút ba chấm rồi chọn Lịch sử).")
b.image("20-popup-lich-su.png", "Cửa sổ Lịch sử thay đổi của một phiếu")
b.para("Cách 2 — từ màn chi tiết: cuộn xuống cuối trang, bấm nút Xem lịch sử ở khối Lịch sử. "
       "Nội dung hiển thị giống hệt cửa sổ ở màn danh sách; nút đổi thành Thu gọn và có thêm "
       "nút Làm mới.")
b.image("16-lich-su.png", "Khối Lịch sử ở cuối màn chi tiết")
b.para("Mỗi mốc trong lịch sử gồm: ngày giờ, tên thao tác (Tạo mới / Thay đổi thông tin / "
       "Thay đổi trạng thái), người thực hiện kèm phòng ban, và phần chi tiết thay đổi:")
b.bullet("Thay đổi thông tin: liệt kê từng trường đã sửa, có mũi tên từ giá trị cũ sang giá "
         "trị mới, dùng tên tiếng Việt (ví dụ Loại thu, Loại tiền, Trạng thái).")
b.bullet("Thay đổi ở bảng chi tiết: ghi rõ dòng nào được thêm, sửa hay bỏ, kèm khách hàng, "
         "hợp đồng và số tiền đề nghị thu của dòng đó.")
b.bullet("Thay đổi trạng thái: ghi trạng thái cũ và trạng thái mới; riêng thao tác Không duyệt "
         "còn kèm lý do mà kế toán đã nhập.")
b.para("Phiếu chưa từng có thao tác nào trên màn hình này sẽ hiện dòng “Chưa có lịch sử thao "
       "tác nào.”.")

# ══════════════════════════════════════════════════════════ PHẦN 10
b.h1("PHẦN 10: CÂU HỎI THƯỜNG GẶP")
b.table([
    ["Tình huống", "Nguyên nhân và cách xử lý"],
    ["Gõ vào ô Tìm theo mã phiếu nhưng danh sách không đổi",
     "Ô tìm nhanh chờ bấm nút Tìm kiếm mới lọc. Bấm nút Tìm kiếm hoặc nhấn phím Enter."],
    ["Quay lại màn hình thì vẫn thấy danh sách đang bị lọc",
     "Hệ thống ghi nhớ bộ lọc trong 10 phút. Bấm Làm mới để xóa hết tiêu chí."],
    ["Không thấy một tiêu chí lọc hoặc một cột quen thuộc",
     "Tiêu chí và cột lưu riêng theo tài khoản. Mở Cài đặt bộ lọc hoặc Tuỳ chỉnh cột để bật lại; "
     "ở Cài đặt bộ lọc có nút Khôi phục mặc định."],
    ["Bấm vào ô hợp đồng nhưng không mở được cửa sổ chọn",
     "Chưa chọn khách hàng (hoặc nhà cung cấp) cho dòng đó. Gợi ý trong ô ghi “Chọn khách hàng "
     "trước”."],
    ["Không tìm thấy hợp đồng cần chọn trong cửa sổ",
     "Cửa sổ chỉ liệt kê hợp đồng của đúng khách hàng đã chọn ở dòng đó, và với hợp đồng bán "
     "thì chỉ lấy hợp đồng từ trạng thái Có hiệu lực trở lên."],
    ["Hợp đồng hiện trong danh sách nhưng bấm không chọn được",
     "Hợp đồng đã được chọn ở một dòng khác của cùng phiếu. Mỗi hợp đồng chỉ chọn một lần trong "
     "một phiếu."],
    ["Số tiền còn nợ hiển thị 0",
     "Hợp đồng chưa phát sinh bút toán kế toán nên chưa có số dư công nợ. Đây là hiện trạng "
     "bình thường, không ảnh hưởng tới việc lập phiếu."],
    ["Bấm Lưu nhưng báo dữ liệu đã được thay đổi",
     "Phiếu vừa bị người khác gửi duyệt hoặc xử lý ở nơi khác. Tải lại trang để xem trạng thái "
     "mới nhất rồi thao tác lại."],
    ["Không thấy nút Sửa hoặc nút Xóa",
     "Chỉ người lập phiếu mới sửa và xóa được, và chỉ khi phiếu ở trạng thái Đang tạo hoặc "
     "Không duyệt."],
    ["Không thấy mục menu Phiếu đề nghị thu tiền chờ duyệt",
     "Tài khoản chưa được cấp quyền Kế toán thanh toán. Liên hệ quản trị hệ thống."],
    ["Đổi Loại thu thì mất hết dòng chi tiết",
     "Đúng thiết kế: hai loại thu dùng hai nguồn dữ liệu khác nhau. Hệ thống có hỏi xác nhận "
     "trước khi xóa; bấm Hủy nếu chưa muốn đổi."],
    ["Phiếu bị từ chối, muốn gửi lại",
     "Mở phiếu ở trạng thái Không duyệt, đọc lý do trong ô Ghi chú, bấm Sửa, chỉnh lại rồi bấm "
     "Lưu và gửi duyệt."],
])

info = b.finish()
print(info)
