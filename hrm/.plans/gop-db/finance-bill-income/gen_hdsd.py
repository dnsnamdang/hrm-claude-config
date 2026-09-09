# -*- coding: utf-8 -*-
"""Sinh tai lieu HDSD (.docx) cho man "Phieu thu tien" (phan he Tai chinh).

Khung + style lay tu `.claude/skills/hdsd-documenter/assets/HDSD_MAU.docx`.
Anh that: pt_shots/ (cong dev hrm-crm.eteksofts.com; rieng 3 anh muc Lich su chup tren cong
local vi cong dev chua deploy Phase L) — KHONG commit.

Chay:  python .plans/gop-db/finance-bill-income/gen_hdsd.py
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

OUT = os.path.join(HERE, "HDSD_Phiếu thu tiền.docx")
SHOTS = os.path.join(HERE, "pt_shots")

MENU = "Tài chính → Quản lý tiền → Thanh toán tiền mặt → Phiếu thu"

b = HdsdBuilder(output=OUT, shots_dir=SHOTS,
                cover_title="(Màn hình: Phiếu thu tiền)",
                doc_title="HDSD - Phiếu thu tiền")

# ══════════════════════════════════════════════════════════ TỔNG QUAN
b.h1("TỔNG QUAN")

b.h2("1. Thuật ngữ và từ viết tắt")
b.table([
    ["Thuật ngữ", "Giải thích"],
    ["Phiếu thu tiền",
     "Chứng từ kế toán lập từ MỘT phiếu đề nghị thu tiền đang chờ duyệt, để ghi nhận khoản tiền "
     "thực tế thu về. Mã phiếu do hệ thống sinh tự động dạng «mã công ty».PT«tháng năm»."
     "«5 chữ số», ví dụ TPE.PT0926.00001."],
    ["Phiếu đề nghị thu tiền",
     "Chứng từ do người kinh doanh lập trước đó để đề nghị kế toán thu tiền. Một phiếu đề nghị "
     "chỉ lập được ĐÚNG MỘT phiếu thu."],
    ["Dòng chi tiết",
     "Một dòng trong bảng Chi tiết của phiếu thu, kéo thẳng từ phiếu đề nghị. Không thêm và "
     "không xoá dòng được — muốn đổi thì phải đổi phiếu đề nghị."],
    ["Tài khoản nợ",
     "Tài khoản ghi bên Nợ của bút toán — thường là tài khoản tiền mặt hoặc tiền gửi. Khai ở "
     "khối Thông tin chung, áp cho cả phiếu."],
    ["Số tài khoản có",
     "Tài khoản ghi bên Có của bút toán, khai riêng cho từng dòng chi tiết — thường là tài khoản "
     "phải thu của khách hàng."],
    ["Số tiền đề nghị thu",
     "Số tiền người kinh doanh đề nghị thu, lấy từ phiếu đề nghị. Chỉ đọc."],
    ["Số tiền duyệt thu",
     "Số tiền kế toán chốt sẽ thu, do người lập phiếu thu nhập. Đây cũng là số hiển thị ở cột "
     "«Số tiền» của màn danh sách."],
    ["Số tiền thực thu",
     "Số tiền thủ quỹ thực nhận, nhập ngay trong bảng ở màn xem chi tiết trước khi bấm Duyệt. "
     "Không được lớn hơn số tiền duyệt thu của chính dòng đó."],
    ["Phân bổ",
     "Thao tác điền hộ: thủ quỹ gõ tổng tiền thực nhận rồi bấm nút, hệ thống rải xuống cột Số "
     "tiền thực thu theo thứ tự từ trên xuống, mỗi dòng tối đa bằng số duyệt thu của nó."],
    ["Ngày hạch toán",
     "Ngày ghi bút toán vào sổ kế toán. Hệ thống lấy ngày duyệt phiếu."],
    ["Đang tạo", "Phiếu mới lưu nháp. Chỉ người lập nhìn thấy, sửa được và xoá được."],
    ["Chờ duyệt", "Phiếu đã gửi, đang chờ thủ quỹ duyệt hoặc hủy."],
    ["Đã duyệt",
     "Thủ quỹ đã duyệt; hệ thống ĐÃ ghi bút toán vào sổ kế toán. Không sửa, không xoá, không hủy "
     "được nữa."],
    ["Hủy", "Thủ quỹ đã hủy phiếu kèm lý do. Không ghi bút toán nào."],
])

b.h2("2. Cập nhật tài liệu")
b.table([
    ["Phiên bản", "Ngày", "Nội dung", "Người thực hiện"],
    ["1.0", "03/09/2026", "Ban hành lần đầu cho màn Phiếu thu tiền "
     "(phân hệ Tài chính, nhóm Quản lý tiền).", "Nhóm phát triển HRM"],
])

b.h2("3. Giới thiệu chung")
b.para(
    "Màn hình Phiếu thu tiền dùng để lập và theo dõi chứng từ thu tiền của doanh nghiệp. Kế toán "
    "chọn một phiếu đề nghị thu tiền đang chờ duyệt, chốt số tiền duyệt thu cho từng dòng rồi gửi "
    "duyệt. Thủ quỹ nhận thông báo, mở phiếu, nhập số tiền thực nhận và bấm Duyệt — đúng lúc đó "
    "hệ thống ghi bút toán vào sổ kế toán và cập nhật số thực thu ngược về phiếu đề nghị. Nếu "
    "khoản thu không thành, thủ quỹ bấm Hủy kèm lý do.")
b.para("Đường dẫn vào màn hình:")
b.bullet("Menu: " + MENU)
b.bullet("Đường dẫn trực tiếp: /finance/bill-incomes")
b.para(
    "Lưu ý: chỉ có duy nhất MỘT mục menu trỏ vào màn này. Trước đây có ba lối vào riêng «của "
    "tôi» / «chờ duyệt» / «đã duyệt»; nay gộp về một màn, ba cách xem đó thành ô lọc Người lập và "
    "ô lọc Trạng thái ngay trên màn.")
b.image("18-duong-dan-menu.png", "Đường dẫn menu tới màn Phiếu thu tiền")

b.para("CẢNH BÁO QUAN TRỌNG TRƯỚC KHI DÙNG:")
b.bullet(
    "Bấm «Duyệt phiếu thu» là thao tác KHÔNG HOÀN TÁC ĐƯỢC. Hệ thống ghi ngay bút toán vào sổ kế "
    "toán, không có chức năng gỡ bút toán. Hãy kiểm tra kỹ số tiền thực thu của từng dòng trước "
    "khi bấm.")
b.bullet(
    "Bấm «Hủy phiếu thu» đưa cả phiếu thu lẫn phiếu đề nghị về trạng thái Hủy, và KHÔNG lập lại "
    "được phiếu thu khác cho phiếu đề nghị đó. Đây là quy tắc nghiệp vụ đã chốt.")

b.h2("4. Quyền và phạm vi dữ liệu")
b.para(
    "Màn này có bốn quyền liên quan. Hai quyền quyết định NHÌN THẤY BAO NHIÊU PHIẾU, hai quyền "
    "quyết định LÀM ĐƯỢC GÌ.")
b.table([
    ["Tên quyền", "Cho phép làm gì", "Thể hiện trên giao diện"],
    ["Xem tất cả phiếu thu của tổng công ty",
     "Nhìn thấy phiếu thu của mọi công ty.",
     "Danh sách hiện phiếu của tất cả công ty; khối lọc nâng cao có nhóm ô Công ty – Phòng ban – "
     "Bộ phận."],
    ["Xem tất cả phiếu thu của công ty",
     "Nhìn thấy phiếu thu thuộc công ty của mình.",
     "Danh sách chỉ hiện phiếu cùng công ty; khối lọc nâng cao có nhóm ô Công ty – Phòng ban – "
     "Bộ phận."],
    ["Kế toán thanh toán",
     "Lập, sửa, xoá phiếu thu; mở được cửa sổ chọn phiếu đề nghị.",
     "Không có quyền này thì cửa sổ chọn phiếu đề nghị bị từ chối và thao tác lưu bị chặn, dù nút "
     "«Tạo mới» vẫn hiện."],
    ["Thủ quỹ duyệt phiếu thu",
     "Nhập số tiền thực thu, bấm Duyệt phiếu thu và Hủy phiếu thu. Đồng thời là nhóm nhận thông "
     "báo khi có phiếu mới gửi duyệt.",
     "Màn chi tiết hiện thêm khối «Số tiền phân bổ», cột «Số tiền thực thu» thành ô nhập, và hai "
     "nút «Duyệt phiếu thu», «Hủy phiếu thu»."],
    ["(Không có quyền xem nào)",
     "Chỉ nhìn thấy phiếu thu do chính mình lập.",
     "Danh sách chỉ có phiếu của mình; khối lọc nâng cao KHÔNG có nhóm ô Công ty – Phòng ban – "
     "Bộ phận."],
])
b.para("Vai trò quản trị hệ thống được coi như có đủ bốn quyền trên.")
b.para("Ba quy tắc luôn được áp dụng, không quyền nào gỡ được:")
b.bullet(
    "Phiếu ở trạng thái «Đang tạo» của NGƯỜI KHÁC luôn bị ẩn khỏi danh sách, kể cả với quản trị "
    "hệ thống.")
b.bullet(
    "Chỉ sửa và xoá được phiếu ở trạng thái «Đang tạo»; phiếu đã gửi duyệt hoặc đã duyệt thì "
    "không sửa, không xoá.")
b.bullet(
    "Người đã duyệt một phiếu thì luôn mở lại được phiếu đó, kể cả khi phiếu thuộc công ty khác "
    "(dù trên danh sách vẫn không hiện).")
b.para(
    "Ba chức năng Xem chi tiết, In và Xuất Excel chỉ cần nhìn thấy được phiếu là dùng được. Chức "
    "năng Lịch sử không gắn quyền riêng.")

# ══════════════════════════════════════════════════════════ PHẦN 1
b.h1("PHẦN 1: TRUY CẬP VÀ BỐ CỤC MÀN HÌNH")

b.h2("1. Cách vào màn hình")
b.para("Thực hiện lần lượt:")
b.para("1. Đăng nhập hệ thống, ở trang chọn phân hệ bấm ô «Tài chính».")
b.para("2. Trên thanh menu bên trái, bấm nhóm «Quản lý tiền».")
b.para("3. Trong bảng chức năng vừa mở, tìm nhóm «THANH TOÁN TIỀN MẶT».")
b.para("4. Bấm chức năng «Phiếu thu».")
b.para(
    "Màn hình mở ra có tiêu đề «Danh sách phiếu thu». Nhóm «Thanh toán tiền mặt» còn 4 chức năng "
    "khác (Phiếu chi, Phiếu báo có, Tổng hợp tiền về ngân hàng, Phiếu ủy nhiệm chi) — đó là các "
    "màn hình khác.")

b.h2("2. Bố cục màn danh sách")
b.image("01-danh-sach.png", "Màn hình danh sách Phiếu thu tiền")
b.para("Màn hình chia làm 2 khối từ trên xuống:")
b.bullet(
    "Khối «Bộ lọc danh sách»: ô tìm nhanh, nút «Tìm kiếm», nút «Làm mới», nút «Cài đặt bộ lọc» "
    "và nút «Tìm kiếm nâng cao».")
b.bullet(
    "Khối lưới dữ liệu: tiêu đề «Danh sách phiếu thu», nút «Tạo mới» và nút biểu tượng cấu hình "
    "cột ở góc phải, bảng dữ liệu và thanh phân trang.")
b.para(
    "Bảng có 13 cột nên rộng hơn màn hình — dùng thanh cuộn ngang ngay phía trên và phía dưới "
    "bảng để xem các cột bên phải (Trạng thái, Hành động).")
b.image("02-danh-sach-cot-phai.png",
        "Danh sách sau khi cuộn ngang — thấy cột Trạng thái và Hành động")

b.h2("3. Các cột của bảng danh sách")
b.table([
    ["Cột", "Nội dung", "Sắp xếp được"],
    ["STT", "Số thứ tự dòng, đánh theo từng trang (sang trang 2 với cỡ 10 dòng thì bắt đầu từ "
     "11). Luôn hiển thị, không tắt được.", "Không"],
    ["Mã phiếu", "Mã phiếu thu. Bấm vào mã để mở màn chi tiết. Luôn hiển thị, không tắt được.",
     "Có"],
    ["Mã phiếu đề nghị thu", "Mã phiếu đề nghị gốc. Bấm vào mã sẽ mở TAB MỚI sang màn chi tiết "
     "phiếu đề nghị.", "Không"],
    ["Loại thu", "Thu bán hàng / Thu nhà cung cấp / Thu khác. Lấy theo phiếu đề nghị.", "Không"],
    ["Khách hàng", "Mã và tên khách hàng của DÒNG CHI TIẾT ĐẦU TIÊN. Phiếu thu nhà cung cấp "
     "không có khách hàng nên hiện dấu gạch ngang.", "Không"],
    ["Số tiền", "Tổng số tiền DUYỆT THU của phiếu. Xem thêm cảnh báo ở Phần 9.", "Có"],
    ["Người đề nghị", "Người lập phiếu đề nghị (khác Người tạo).", "Không"],
    ["Người tạo", "Người lập phiếu thu.", "Không"],
    ["Ngày tạo", "Thời điểm lập phiếu thu, dạng ngày/tháng/năm giờ:phút.", "Có"],
    ["Người cập nhật", "Người sửa phiếu gần nhất.", "Không"],
    ["Ngày cập nhật", "Thời điểm sửa gần nhất.", "Có"],
    ["Trạng thái", "Nhãn màu: đỏ với Đang tạo / Chờ duyệt / Hủy, xanh với Đã duyệt.", "Không"],
    ["Hành động", "Các nút thao tác của dòng. Luôn hiển thị, không tắt được.", "Không"],
])
b.para("Mặc định danh sách sắp xếp theo Ngày tạo giảm dần — phiếu mới nhất nằm trên cùng.")

b.h2("4. Các nút thao tác trên một dòng")
b.para(
    "Cột «Hành động» hiển thị tối đa 2–3 nút chính, các nút còn lại nằm trong menu ba chấm. Nút "
    "không đủ điều kiện bị ẩn hẳn chứ không hiện xám.")
b.table([
    ["Nút", "Biểu tượng", "Điều kiện hiện", "Tác dụng"],
    ["Sửa", "Bút chì", "Phiếu ở trạng thái «Đang tạo»", "Mở màn Sửa phiếu thu."],
    ["Xóa", "Thùng rác đỏ", "Phiếu ở trạng thái «Đang tạo»", "Mở hộp xác nhận xoá phiếu."],
    ["Duyệt", "Dấu tích trong vòng tròn", "Phiếu ở «Chờ duyệt» và người dùng là thủ quỹ",
     "CHỈ MỞ màn chi tiết — không duyệt ngay. Thao tác duyệt làm ở màn chi tiết."],
    ["In", "Máy in", "Phiếu KHÔNG thuộc loại thu «Thu khác»",
     "Mở tab mới hiển thị bản in 2 liên."],
    ["Xuất Excel", "Biểu tượng bảng tính", "Luôn hiện", "Tải về tệp Excel của đúng phiếu đó."],
    ["Lịch sử", "Đồng hồ quay ngược", "Luôn hiện", "Mở cửa sổ Lịch sử thay đổi của phiếu."],
])
b.image("20-hanh-dong-phieu-nhap.png",
        "Cột Hành động: dòng «Đang tạo» có Sửa và Xóa, dòng «Chờ duyệt» có nút Duyệt")
b.image("25-menu-hanh-dong-khac.png",
        "Menu ba chấm — chứa In, Xuất Excel và Lịch sử")
b.para("Lưu ý: màn danh sách KHÔNG có nút «Hủy phiếu». Muốn hủy phải vào màn chi tiết.")

# ══════════════════════════════════════════════════════════ PHẦN 2
b.h1("PHẦN 2: TÌM KIẾM VÀ LỌC DANH SÁCH")

b.h2("1. Ô tìm nhanh")
b.para(
    "Ô tìm nhanh nằm ngay dưới tiêu đề «Bộ lọc danh sách», ghi sẵn dòng gợi ý «Tìm theo mã "
    "phiếu...». Cách dùng:")
b.para("1. Gõ một phần mã phiếu vào ô (ví dụ 00032).")
b.para("2. Bấm nút «Tìm kiếm» màu xanh bên phải, hoặc nhấn phím Enter.")
b.para(
    "LƯU Ý: ô tìm nhanh KHÔNG tự tìm khi đang gõ — bắt buộc phải bấm nút. Ngược lại, mọi ô trong "
    "«Tìm kiếm nâng cao» tự lọc ngay khi đổi giá trị.")

b.h2("2. Tìm kiếm nâng cao")
b.para(
    "Bấm nút «Tìm kiếm nâng cao» ở góc phải khối lọc để mở thêm các ô lọc. Khi khối đang mở, nút "
    "đổi chữ thành «Ẩn tìm kiếm nâng cao».")
b.image("03-loc-nang-cao.png", "Khối Tìm kiếm nâng cao khi đang mở")
b.table([
    ["Ô lọc", "Kiểu nhập", "Cách hoạt động"],
    ["Công ty – Phòng ban – Bộ phận", "Danh sách chọn",
     "CHỈ hiện với người có quyền xem theo tổng công ty hoặc theo công ty. Lọc theo đơn vị ghi "
     "trên PHIẾU ĐỀ NGHỊ, không phải theo phiếu thu."],
    ["Mã phiếu đề nghị thu", "Gõ tay", "Tìm phiếu thu theo mã phiếu đề nghị gốc."],
    ["Loại thu", "Danh sách chọn",
     "Có «Thu bán hàng» và «Thu nhà cung cấp». Giá trị «Thu khác» không còn cho chọn, nhưng phiếu "
     "cũ mang loại này vẫn hiện đúng tên trên lưới."],
    ["Trạng thái", "Danh sách chọn",
     "Bốn giá trị: Đang tạo, Chờ duyệt, Đã duyệt, Hủy. Chọn «Đang tạo» chỉ ra nháp của chính "
     "mình."],
    ["Người lập", "Danh sách nhân viên", "Lọc theo người lập PHIẾU THU."],
    ["Người đề nghị", "Danh sách nhân viên", "Lọc theo người lập PHIẾU ĐỀ NGHỊ."],
    ["Khách hàng", "Danh sách tìm từ xa",
     "Phải gõ ít nhất 2 ký tự mới hiện gợi ý. Lọc phiếu có dòng chi tiết gắn khách hàng đó."],
    ["Số hợp đồng/đơn hàng", "Gõ tay",
     "Lọc phiếu có ít nhất một dòng chi tiết gắn hợp đồng khớp."],
    ["Số tiền từ – Số tiền đến", "Nhập số tiền",
     "So theo cột «Số tiền» của lưới, tức tổng số tiền DUYỆT THU."],
    ["Ngày lập từ – Ngày lập đến", "Chọn ngày trên lịch",
     "Lọc theo NGÀY LẬP PHIẾU THU (cột Ngày tạo). Cả hai mốc lấy trọn ngày."],
])
b.para(
    "Các điều kiện cộng dồn với nhau: chọn Trạng thái «Chờ duyệt» và Loại thu «Thu bán hàng» thì "
    "chỉ ra phiếu thoả CẢ HAI. Mỗi lần đổi một ô, danh sách tự nạp lại và quay về trang 1.")
b.image("17-loc-dang-tao.png",
        "Lọc Trạng thái = Đang tạo — chỉ ra nháp của chính người đăng nhập")

b.h2("3. Ba cách xem cũ nay là bộ lọc")
b.para(
    "Trước đây màn hình có ba lối vào riêng. Nay làm trực tiếp trên một màn:")
b.table([
    ["Muốn xem", "Cách làm"],
    ["Phiếu của tôi", "Mở «Tìm kiếm nâng cao», chọn Người lập = chính mình."],
    ["Phiếu chờ duyệt", "Mở «Tìm kiếm nâng cao», chọn Trạng thái = «Chờ duyệt»."],
    ["Phiếu đã duyệt", "Mở «Tìm kiếm nâng cao», chọn Trạng thái = «Đã duyệt»."],
])

b.h2("4. Nút Làm mới")
b.para(
    "Bấm «Làm mới» để xoá toàn bộ điều kiện lọc và ô tìm nhanh, đưa danh sách về trang 1. Phạm vi "
    "dữ liệu theo quyền KHÔNG đổi — «Làm mới» chỉ xoá điều kiện lọc.")

b.h2("5. Cài đặt bộ lọc — chọn ô lọc muốn hiển thị")
b.para("Bấm nút «Cài đặt bộ lọc» để mở cửa sổ ẩn bớt hoặc đổi thứ tự các ô lọc nâng cao.")
b.image("04-cai-dat-bo-loc.png", "Cửa sổ Cài đặt bộ lọc")
b.bullet("Bỏ tích một ô để ẩn ô lọc đó khỏi khối Tìm kiếm nâng cao.")
b.bullet("Kéo biểu tượng sáu chấm ở đầu mỗi ô để đổi thứ tự hiển thị.")
b.bullet("Bấm «Lưu» để áp dụng — cấu hình lưu riêng theo từng người và từng màn hình.")
b.bullet("Bấm «Khôi phục mặc định» để đưa về đủ 10 nhóm ô theo thứ tự ban đầu.")
b.bullet("Bấm «Đóng» để thoát mà không lưu thay đổi.")
b.para(
    "Lưu ý: dòng «Công ty – Phòng ban – Bộ phận» luôn có trong cửa sổ này, nhưng nếu bạn không có "
    "quyền xem theo tổng công ty hoặc theo công ty thì nhóm ô đó vẫn không hiện trên màn.")

b.h2("6. Ghi nhớ bộ lọc trong 10 phút")
b.para(
    "Hệ thống ghi nhớ điều kiện lọc trong 10 phút. Rời màn rồi quay lại trong khoảng thời gian "
    "này thì điều kiện cũ vẫn còn — nếu thấy danh sách «thiếu phiếu», hãy bấm «Làm mới» trước khi "
    "kết luận là mất dữ liệu.")

# ══════════════════════════════════════════════════════════ PHẦN 3
b.h1("PHẦN 3: SẮP XẾP, PHÂN TRANG VÀ CẤU HÌNH CỘT")

b.h2("1. Sắp xếp")
b.para(
    "Bấm vào tiêu đề cột có biểu tượng hai mũi tên để sắp xếp. Bấm lần một là tăng dần, bấm lần "
    "hai là giảm dần. Mỗi lần đổi sắp xếp, danh sách quay về trang 1 nhưng GIỮ NGUYÊN điều kiện lọc.")
b.bullet("Bốn cột sắp xếp được: Mã phiếu, Số tiền, Ngày tạo, Ngày cập nhật.")
b.bullet(
    "Sắp theo «Số tiền» là sắp theo tổng số tiền DUYỆT THU, không phải số thực thu.")

b.h2("2. Phân trang")
b.para(
    "Cuối bảng có dòng «Hiển thị a–b / N»: a là số thứ tự dòng đầu trang, b là dòng cuối, N là "
    "tổng số phiếu khớp bộ lọc và nằm trong phạm vi quyền.")
b.bullet("Ô «Số dòng/trang» có các lựa chọn 5, 10, 20, 50, 100. Mặc định là 10.")
b.bullet("Đổi số dòng/trang sẽ đưa danh sách về trang 1.")
b.bullet("Chuyển trang KHÔNG làm mất điều kiện lọc và không đổi chiều sắp xếp.")

b.h2("3. Tuỳ chỉnh cột hiển thị")
b.para("Bấm nút biểu tượng cột (bên phải nút «Tạo mới») để mở cửa sổ «Tuỳ chỉnh cột».")
b.image("05-cau-hinh-cot.png", "Cửa sổ Tuỳ chỉnh cột hiển thị")
b.bullet("Bỏ tích một cột để ẩn cột đó khỏi bảng.")
b.bullet(
    "Ba cột STT, Mã phiếu và Hành động có biểu tượng ổ khoá, chữ mờ — luôn hiển thị, không bỏ "
    "tích được.")
b.bullet("Kéo biểu tượng ba gạch ở cuối mỗi dòng để đổi thứ tự cột.")
b.bullet(
    "Bấm «Lưu» để áp dụng. Cấu hình lưu riêng theo từng người và riêng cho màn này, không ảnh "
    "hưởng màn khác.")

# ══════════════════════════════════════════════════════════ PHẦN 4
b.h1("PHẦN 4: TẠO MỚI PHIẾU THU TIỀN")

b.h2("1. Ai làm được và điều kiện")
b.para(
    "Chức năng này cần quyền «Kế toán thanh toán» (hoặc vai trò quản trị hệ thống). Nút «Tạo "
    "mới» hiện với mọi người, nhưng nếu thiếu quyền thì cửa sổ chọn phiếu đề nghị sẽ bị từ chối "
    "và thao tác lưu bị chặn với thông báo «Bạn không có quyền lập phiếu thu».")
b.para(
    "Phiếu thu luôn lập TỪ MỘT phiếu đề nghị thu tiền: phiếu đề nghị đó phải đang ở trạng thái "
    "«Chờ KT duyệt» và chưa có phiếu thu nào.")

b.h2("2. Mở màn Tạo mới")
b.para(
    "Bấm nút «Tạo mới» (biểu tượng dấu cộng, màu xanh) ở góc phải khối lưới. Hệ thống mở màn "
    "riêng có tiêu đề «Thêm phiếu thu tiền».")
b.image("06-tao-moi.png", "Màn Thêm phiếu thu tiền khi vừa mở")

b.h2("3. Khối Thông tin chung")
b.table([
    ["Trường", "Kiểu nhập", "Bắt buộc", "Giá trị điền sẵn khi tạo mới", "Ghi chú"],
    ["Số phiếu đề nghị", "Ô chỉ đọc, bấm vào để mở cửa sổ chọn", "Có", "Trống",
     "Dòng gợi ý «Nhấn vào đây để chọn phiếu đề nghị thu». Không có nút riêng — bấm thẳng vào ô."],
    ["Tài khoản nợ", "Danh sách chọn", "Có", "Một tài khoản tiền mặt mặc định",
     "Chỉ liệt kê tài khoản đang hoạt động và là tài khoản cấp cuối."],
    ["Loại thu", "Ô chỉ đọc", "–", "Trống, ghi «Theo phiếu đề nghị»",
     "Tự điền sau khi chọn phiếu đề nghị."],
    ["Người nộp", "Ô nhập", "Có", "Trống", "Tên người mang tiền đến nộp. Tối đa 255 ký tự."],
    ["Loại tiền", "Ô chỉ đọc", "–", "Trống, ghi «Theo phiếu đề nghị»",
     "Tự điền sau khi chọn phiếu đề nghị."],
    ["Tỷ giá (VND)", "Ô nhập số", "Có", "1",
     "BỊ KHOÁ khi loại tiền là VNĐ. Chỉ mở khi phiếu đề nghị dùng ngoại tệ."],
    ["Người đề nghị", "Ô chỉ đọc", "–", "Trống, ghi «Theo phiếu đề nghị»",
     "Người lập phiếu đề nghị."],
    ["Phòng ban", "Ô chỉ đọc", "–", "Trống, ghi «Theo phiếu đề nghị»",
     "Phòng ban của người đề nghị."],
    ["Lý do thu", "Ô chỉ đọc nhiều dòng", "–", "Trống, ghi «Theo phiếu đề nghị»",
     "Lý do ghi trên phiếu đề nghị."],
    ["Ghi chú", "Ô nhập nhiều dòng", "Không", "Trống", "Nằm ở khối riêng cuối trang, tối đa 1.000 "
     "ký tự."],
])
b.para(
    "Hộp «Giá trị điền sẵn khi tạo mới»: Tài khoản nợ = tài khoản tiền mặt mặc định; Tỷ giá = 1; "
    "mọi ô còn lại để trống. Màn Tạo mới KHÔNG có ô «Mã phiếu» và ô «Người tạo» — hai ô này chỉ "
    "xuất hiện ở màn Sửa và màn Xem chi tiết.")

b.h2("4. Chọn phiếu đề nghị thu")
b.para("1. Bấm vào ô «Số phiếu đề nghị».")
b.para(
    "2. Cửa sổ «Chọn phiếu đề nghị thu» mở ra, phụ đề ghi rõ «Chỉ phiếu Chờ duyệt và chưa lập "
    "phiếu thu».")
b.image("07-popup-chon-de-nghi.png", "Cửa sổ Chọn phiếu đề nghị thu")
b.para(
    "3. Tìm phiếu cần lập: gõ mã vào ô «Mã phiếu đề nghị», hoặc chọn người ở ô «Người lập», rồi "
    "bấm «Tìm kiếm». Bấm «Làm mới» để xoá điều kiện tìm.")
b.para("4. Bấm vào dòng phiếu đề nghị cần chọn.")
b.para("Cửa sổ tự đóng và hệ thống kéo về toàn bộ dữ liệu của phiếu đề nghị:")
b.bullet("Loại thu, Loại tiền, Người đề nghị, Phòng ban, Lý do thu tự điền.")
b.bullet(
    "Bảng «Chi tiết» nạp đủ các dòng của phiếu đề nghị, mỗi dòng đã có sẵn Số tài khoản có và "
    "Số tiền duyệt thu (bằng Số tiền đề nghị thu).")
b.bullet("Nếu phiếu đề nghị dùng ngoại tệ thì ô «Tỷ giá (VND)» mở ra cho sửa.")
b.image("08-form-da-chon-de-nghi.png",
        "Màn Thêm phiếu thu sau khi chọn phiếu đề nghị — bảng Chi tiết đã nạp 3 dòng")
b.para(
    "Nếu không tìm thấy phiếu đề nghị cần lập, thường do một trong ba lý do: phiếu chưa được gửi "
    "duyệt; phiếu đã có phiếu thu khác (kể cả phiếu thu đang là nháp hoặc đã bị hủy); hoặc bạn "
    "không có quyền «Kế toán thanh toán».")

b.h2("5. Bảng Chi tiết")
b.para(
    "Bảng này KHÔNG có nút thêm dòng và không có nút xoá dòng — số dòng luôn đúng bằng số dòng "
    "của phiếu đề nghị. Muốn đổi thì phải chọn phiếu đề nghị khác.")
b.table([
    ["Cột", "Nội dung", "Nhập được?"],
    ["STT", "Số thứ tự dòng.", "Không"],
    ["Số tài khoản có", "Tài khoản ghi bên Có. Điền sẵn theo phiếu đề nghị.", "Có — bắt buộc"],
    ["Tên tài khoản", "Tên của tài khoản vừa chọn, tự hiện.", "Không"],
    ["Khách hàng (hoặc Nhà cung cấp)", "Đối tượng thu của dòng. Tiêu đề cột đổi theo loại thu.",
     "Không"],
    ["Số đơn hàng/Hợp đồng", "Hợp đồng gắn với dòng.", "Không"],
    ["Số tiền đề nghị thu", "Số tiền trên phiếu đề nghị.", "Không"],
    ["Số tiền duyệt thu", "Số tiền kế toán chốt sẽ thu.", "Có — bắt buộc"],
    ["Số tiền thực thu", "CHỈ có ở màn Xem chi tiết, không có ở màn Tạo mới và màn Sửa.", "–"],
    ["Ghi chú", "Ghi chú của dòng.", "Có"],
])
b.para(
    "Cuối bảng có dòng «Tổng cộng» cộng dọc từng cột tiền, cập nhật ngay khi bạn sửa số. Với "
    "phiếu ngoại tệ, mỗi nhóm tiền có 2 cột: cột nguyên tệ và cột VND; nhập cột nguyên tệ thì "
    "cột VND tự quy đổi theo ô Tỷ giá.")

b.h2("6. Lưu phiếu")
b.para("Cuối trang có ba nút, luôn cố định ở đáy màn hình:")
b.table([
    ["Nút", "Có hỏi xác nhận?", "Kết quả"],
    ["Lưu", "Không",
     "Lưu phiếu ở trạng thái «Đang tạo». Thông báo «Thêm phiếu thu tiền thành công!». Quay về màn "
     "danh sách. Phiếu chỉ mình nhìn thấy; KHÔNG gửi thông báo và KHÔNG đổi trạng thái phiếu đề "
     "nghị."],
    ["Lưu và gửi duyệt", "Có",
     "Mở hộp «Xác nhận lưu và gửi duyệt» hỏi «Bạn đồng ý lưu và duyệt?». Sau khi xác nhận: phiếu "
     "ở trạng thái «Chờ duyệt», phiếu đề nghị chuyển sang «Đã tạo phiếu thu», và thủ quỹ cùng "
     "công ty nhận thông báo."],
    ["Quay lại", "Có (nếu đã nhập dở)", "Về màn danh sách."],
])
b.image("09-xac-nhan-gui-duyet.png", "Hộp Xác nhận lưu và gửi duyệt")
b.para(
    "Nếu còn ô chưa hợp lệ, hệ thống không lưu mà hiện lỗi đỏ ngay dưới từng ô. Cửa sổ không "
    "đóng, mọi dữ liệu đã nhập vẫn còn (kể cả bảng Chi tiết).")
b.image("10-loi-validate.png", "Lỗi «Bắt buộc nhập» hiện ngay dưới ô Người nộp")
b.table([
    ["Trường hợp", "Thông báo lỗi"],
    ["Chưa chọn phiếu đề nghị", "Bắt buộc nhập"],
    ["Chưa chọn Tài khoản nợ", "Bắt buộc nhập"],
    ["Chưa nhập Người nộp", "Bắt buộc nhập"],
    ["Chưa nhập Tỷ giá", "Bắt buộc nhập"],
    ["Tỷ giá không phải số", "Phải là số"],
    ["Chưa chọn Số tài khoản có của một dòng", "Bắt buộc nhập"],
    ["Chưa nhập Số tiền duyệt thu của một dòng", "Bắt buộc nhập"],
    ["Số tiền duyệt thu không phải số", "Phải là số"],
    ["Phiếu đề nghị đã có phiếu thu khác", "Đề nghị thu tiền đã lập phiếu thu tiền"],
    ["Thiếu quyền Kế toán thanh toán", "Bạn không có quyền lập phiếu thu"],
])

b.h2("7. Sau khi lưu")
b.para(
    "Phiếu mới nằm ở dòng đầu danh sách với mã do hệ thống sinh tự động, dạng «mã công ty».PT"
    "«tháng năm»."
    "«5 chữ số». Người dùng không nhập được mã và mã đã dùng không bao giờ được cấp lại.")
b.image("19-luu-nhap-thanh-cong.png",
        "Danh sách sau khi lưu nháp — phiếu mới ở dòng đầu")

# ══════════════════════════════════════════════════════════ PHẦN 5
b.h1("PHẦN 5: SỬA PHIẾU THU")

b.h2("1. Điều kiện được sửa")
b.para(
    "Chỉ sửa được phiếu đang ở trạng thái «Đang tạo». Phiếu đã gửi duyệt hoặc đã duyệt thì nút "
    "«Sửa» không hiện; gõ thẳng đường dẫn màn Sửa cũng bị chặn với thông báo «Phiếu thu đã gửi "
    "duyệt hoặc đã duyệt, không sửa được». Ngoài ra vẫn cần quyền «Kế toán thanh toán».")

b.h2("2. Mở màn Sửa")
b.para("Có hai đường vào:")
b.bullet("Từ danh sách: cuộn ngang tới cột Hành động, bấm nút Sửa (biểu tượng bút chì).")
b.bullet("Từ màn chi tiết: bấm nút «Sửa» ở thanh nút cuối trang.")
b.image("21-sua-phieu.png", "Màn Sửa phiếu thu tiền với dữ liệu đã lưu")

b.h2("3. Khác biệt so với màn Tạo mới")
b.table([
    ["Điểm", "Màn Tạo mới", "Màn Sửa"],
    ["Tiêu đề", "Thêm phiếu thu tiền", "Sửa phiếu thu tiền"],
    ["Ô Mã phiếu", "Không có", "Có, ở chế độ chỉ đọc"],
    ["Ô Người tạo", "Không có", "Có, ở chế độ chỉ đọc — là người lập phiếu gốc"],
    ["Bảng Chi tiết", "Trống cho tới khi chọn phiếu đề nghị", "Nạp sẵn dữ liệu đã lưu"],
])

b.h2("4. Những gì sửa được")
b.bullet("Đổi sang phiếu đề nghị khác — bảng Chi tiết sẽ nạp lại theo phiếu mới, dòng cũ mất hết.")
b.bullet("Đổi Tài khoản nợ, Người nộp, Tỷ giá (nếu là phiếu ngoại tệ), Ghi chú.")
b.bullet("Đổi Số tài khoản có, Số tiền duyệt thu và Ghi chú của từng dòng chi tiết.")
b.para(
    "Không sửa được: Mã phiếu, Người tạo, và các ô lấy theo phiếu đề nghị (Loại thu, Loại tiền, "
    "Người đề nghị, Phòng ban, Lý do thu).")
b.para(
    "Trường hợp đặc biệt: nếu tài khoản đang gắn với phiếu đã bị KHÓA trong danh mục, ô vẫn hiện "
    "đúng tên tài khoản đó để bạn không vô tình lưu đè mất giá trị cũ; nhưng khi mở danh sách "
    "chọn thì tài khoản đã khóa không nằm trong các lựa chọn mới.")

b.h2("5. Lưu phiếu sau khi sửa")
b.bullet(
    "«Lưu»: giữ phiếu ở «Đang tạo», thông báo «Cập nhật phiếu thu tiền thành công!». Cột «Người "
    "cập nhật» và «Ngày cập nhật» trên danh sách đổi theo người vừa sửa.")
b.bullet(
    "«Lưu và gửi duyệt»: hỏi xác nhận rồi chuyển phiếu sang «Chờ duyệt», phiếu đề nghị chuyển "
    "«Đã tạo phiếu thu», thủ quỹ nhận thông báo. Phiếu lập tức mất nút Sửa và Xóa.")
b.bullet("«Quay lại»: về danh sách, có hỏi nếu đang sửa dở.")

# ══════════════════════════════════════════════════════════ PHẦN 6
b.h1("PHẦN 6: XEM CHI TIẾT PHIẾU THU")

b.h2("1. Mở màn chi tiết")
b.para("Bấm vào mã phiếu (chữ xanh gạch chân) ở cột «Mã phiếu» của dòng phiếu.")
b.image("11-chi-tiet-cho-duyet.png",
        "Màn chi tiết phiếu đang Chờ duyệt, xem bằng tài khoản thủ quỹ")

b.h2("2. Nội dung màn chi tiết")
b.para(
    "Tiêu đề màn ghi «Chi tiết phiếu thu tiền: «mã phiếu»». Toàn bộ thông tin chung ở chế độ chỉ "
    "đọc.")
b.table([
    ["Khối", "Nội dung"],
    ["Thông tin chung",
     "Số phiếu đề nghị, Mã phiếu, Tài khoản nợ, Loại thu, Người nộp, Loại tiền, Tỷ giá (VND), "
     "Người đề nghị, Phòng ban, Người tạo, Lý do thu."],
    ["Chi tiết",
     "Bảng các dòng chi tiết. Khác màn Tạo mới và màn Sửa ở chỗ CÓ THÊM nhóm cột «Số tiền thực "
     "thu». Cuối bảng có dòng «Tổng cộng»."],
    ["Ghi chú", "Ghi chú của phiếu; với phiếu đã hủy thì đây là nơi hiện lý do hủy."],
    ["Lịch sử", "Khối thu gọn ở cuối trang, kèm số đếm số mốc. Xem chi tiết ở Phần 10."],
])

b.h2("3. Nhóm cột Số tiền thực thu")
b.para("Nhóm cột này có ba trạng thái khác nhau:")
b.table([
    ["Tình huống", "Hiển thị"],
    ["Ở màn Tạo mới hoặc màn Sửa", "KHÔNG có nhóm cột này."],
    ["Ở màn chi tiết, người xem KHÔNG phải thủ quỹ (hoặc phiếu không ở «Chờ duyệt»)",
     "Chỉ hiển thị số, không nhập được, tiêu đề cột không có dấu sao."],
    ["Ở màn chi tiết, người xem là thủ quỹ VÀ phiếu đang «Chờ duyệt»",
     "Là Ô NHẬP, tiêu đề cột có dấu sao đỏ; phía trên bảng có thêm khối «Số tiền phân bổ» và nút "
     "«Phân bổ»."],
])

b.h2("4. Thanh nút cuối màn chi tiết")
b.table([
    ["Nút", "Điều kiện hiện"],
    ["Sửa", "Phiếu ở trạng thái «Đang tạo»."],
    ["Duyệt phiếu thu", "Phiếu ở «Chờ duyệt» và người xem là thủ quỹ."],
    ["Hủy phiếu thu", "Cùng điều kiện với nút «Duyệt phiếu thu»."],
    ["In", "Phiếu KHÔNG thuộc loại thu «Thu khác»."],
    ["Xuất Excel", "Luôn hiện."],
    ["Xóa", "Phiếu ở trạng thái «Đang tạo»."],
    ["Quay lại", "Luôn hiện."],
])
b.image("16-chi-tiet-da-duyet.png",
        "Màn chi tiết phiếu Đã duyệt — chỉ còn In, Xuất Excel, Quay lại")

# ══════════════════════════════════════════════════════════ PHẦN 7
b.h1("PHẦN 7: DUYỆT PHIẾU THU (DÀNH CHO THỦ QUỸ)")

b.h2("1. Cảnh báo trước khi làm")
b.para(
    "Duyệt phiếu thu là thao tác KHÔNG HOÀN TÁC ĐƯỢC. Ngay khi bấm, hệ thống ghi bút toán vào sổ "
    "kế toán và cập nhật số tiền thực thu ngược về phiếu đề nghị. Không có chức năng gỡ bút toán "
    "hay «bỏ duyệt». Hãy kiểm tra kỹ số tiền thực thu của từng dòng trước khi bấm.")

b.h2("2. Ai làm được")
b.para("Cần đủ hai điều kiện:")
b.bullet("Người dùng có quyền «Thủ quỹ duyệt phiếu thu» (hoặc là quản trị hệ thống).")
b.bullet("Phiếu đang ở trạng thái «Chờ duyệt».")
b.para("Thiếu một trong hai thì nút không hiện và cột «Số tiền thực thu» không nhập được.")

b.h2("3. Nhập số tiền thực thu")
b.para(
    "Ô nhập nằm ngay trong bảng Chi tiết ở màn xem chi tiết — không có cửa sổ riêng. Có hai cách "
    "điền:")
b.para("Cách 1 — gõ tay từng dòng:")
b.para("1. Mở màn chi tiết phiếu đang «Chờ duyệt».")
b.para("2. Gõ số tiền thực nhận vào ô «Số tiền thực thu» của từng dòng.")
b.para("Cách 2 — dùng nút Phân bổ (nhanh hơn khi có nhiều dòng):")
b.para("1. Gõ TỔNG số tiền thực nhận vào ô «Số tiền phân bổ» phía trên bảng.")
b.para("2. Bấm nút «Phân bổ».")
b.para(
    "3. Hệ thống rải số tiền xuống cột «Số tiền thực thu» theo thứ tự từ trên xuống: mỗi dòng "
    "nhận tối đa bằng số duyệt thu của chính nó, hết tiền thì các dòng còn lại về 0.")
b.para(
    "4. Bấm xong vẫn sửa tay từng ô được. Nút này chỉ ĐIỀN HỘ, chưa ghi gì xuống hệ thống.")
b.para("Quy tắc kiểm tra khi nhập:")
b.bullet("Số thực thu không được âm.")
b.bullet(
    "Số thực thu KHÔNG được lớn hơn số duyệt thu của chính dòng đó. Gõ vượt thì ô viền đỏ và "
    "hiện chữ đỏ «Không được lớn hơn số tiền duyệt thu («số duyệt thu»)»; nút Duyệt bị chặn cho "
    "tới khi sửa lại.")
b.bullet(
    "Số thực thu ĐƯỢC PHÉP nhỏ hơn số duyệt thu (thu thiếu) và được phép bằng 0 — dòng bằng 0 "
    "thì không sinh bút toán cho dòng đó.")
b.image("14-loi-thuc-thu-vuot.png",
        "Lỗi khi gõ số thực thu lớn hơn số duyệt thu")

b.h2("4. Bấm Duyệt")
b.para("1. Kiểm tra lại số thực thu của tất cả các dòng và dòng «Tổng cộng».")
b.para("2. Bấm nút «Duyệt phiếu thu» (màu xanh) ở thanh nút cuối trang.")
b.para("Kết quả:")
b.bullet("Thông báo «Duyệt phiếu thu thành công!» và hệ thống quay về màn danh sách.")
b.bullet("Phiếu thu chuyển sang trạng thái «Đã duyệt», ghi người duyệt và ngày hạch toán là hôm nay.")
b.bullet("Phiếu đề nghị tương ứng chuyển sang «Đã hạch toán» và được ghi số tiền thực thu.")
b.bullet("Hệ thống ghi bút toán vào sổ kế toán cho từng dòng có số thực thu lớn hơn 0.")
b.para(
    "Nếu hai thủ quỹ cùng bấm Duyệt một phiếu, chỉ người bấm trước thành công; người sau nhận "
    "thông báo «Phiếu thu tiền đã được duyệt!» và sổ kế toán KHÔNG bị ghi trùng.")

b.h2("5. Sau khi duyệt")
b.para(
    "Phiếu chỉ còn các nút «In», «Xuất Excel», «Quay lại». Cột «Số tiền thực thu» chuyển sang chỉ "
    "hiển thị. Lưu ý cột «Số tiền» trên màn danh sách VẪN là tổng số tiền duyệt thu, không đổi "
    "theo số thực thu — xem thêm Phần 9.")

# ══════════════════════════════════════════════════════════ PHẦN 8
b.h1("PHẦN 8: HỦY PHIẾU THU (DÀNH CHO THỦ QUỸ)")

b.h2("1. Cảnh báo trước khi làm")
b.para(
    "Hủy phiếu thu đưa cả phiếu thu lẫn phiếu đề nghị về trạng thái «Hủy», và KHÔNG lập lại được "
    "phiếu thu khác cho phiếu đề nghị đó. Đây là quy tắc nghiệp vụ đã chốt, không phải lỗi. Nếu "
    "chỉ muốn sửa lại số tiền thì đừng hủy — hãy trao đổi với kế toán để họ báo lại, vì phiếu "
    "«Chờ duyệt» không sửa được nữa.")

b.h2("2. Các bước hủy")
b.para("1. Mở màn chi tiết phiếu đang ở trạng thái «Chờ duyệt».")
b.para("2. Bấm nút «Hủy phiếu thu» (màu đỏ) ở thanh nút cuối trang.")
b.para(
    "3. Cửa sổ «Hủy phiếu thu tiền» mở ra, phụ đề ghi «Phiếu thu: «mã phiếu»».")
b.image("12-popup-huy-phieu.png", "Cửa sổ Hủy phiếu thu tiền")
b.para("4. Nhập «Lý do hủy» — đây là trường BẮT BUỘC, tối đa 1.000 ký tự.")
b.para("5. Bấm «Xác nhận» để hủy, hoặc «Đóng» để thoát mà không hủy.")
b.para("Kết quả sau khi xác nhận:")
b.bullet("Thông báo «Hủy phiếu thu thành công!».")
b.bullet("Phiếu thu chuyển sang «Hủy»; lý do hủy được ghi vào ô Ghi chú của phiếu.")
b.bullet("Phiếu đề nghị tương ứng chuyển sang «Hủy».")
b.bullet("KHÔNG có bút toán nào được ghi vào sổ kế toán.")
b.para("Nếu bấm «Xác nhận» khi ô Lý do hủy còn trống:")
b.bullet("Ô viền đỏ, dưới ô hiện chữ đỏ «Lý do hủy – Bắt buộc nhập».")
b.bullet("Cửa sổ KHÔNG đóng, phiếu giữ nguyên trạng thái «Chờ duyệt».")
b.image("13-loi-ly-do-huy.png", "Lỗi khi bấm Xác nhận lúc chưa nhập lý do hủy")

# ══════════════════════════════════════════════════════════ PHẦN 9
b.h1("PHẦN 9: XÓA PHIẾU, IN VÀ XUẤT EXCEL")

b.h2("1. Xóa phiếu thu")
b.para(
    "Chỉ xóa được phiếu ở trạng thái «Đang tạo» do chính mình lập. Phiếu đã gửi duyệt hoặc đã "
    "duyệt đều không có nút Xóa.")
b.para("Các bước:")
b.para("1. Bấm nút Xóa (thùng rác đỏ) trên dòng, hoặc nút «Xóa» ở màn chi tiết.")
b.para("2. Hộp «Xác nhận xóa» hiện ra, nêu rõ mã phiếu.")
b.image("22-xac-nhan-xoa.png", "Hộp Xác nhận xóa phiếu thu")
b.para("3. Bấm «Xóa» để xoá, hoặc «Hủy» để giữ lại.")
b.para(
    "Kết quả: thông báo «Xóa phiếu thu thành công!», dòng biến mất khỏi danh sách. Xoá phiếu kéo "
    "theo toàn bộ dòng chi tiết; đây là xoá thật, không khôi phục lại được.")
b.image("23-xoa-thanh-cong.png", "Danh sách sau khi xoá phiếu")
b.para(
    "Điểm cần biết: xoá phiếu thu nháp KHÔNG làm đổi trạng thái phiếu đề nghị (vì lưu nháp vốn "
    "chưa đụng tới phiếu đề nghị). Sau khi xoá, phiếu đề nghị đó xuất hiện trở lại trong cửa sổ "
    "chọn và lập được phiếu thu mới.")

b.h2("2. In phiếu")
b.para("Có hai đường: bấm nút In trên dòng danh sách, hoặc bấm «In» ở màn chi tiết.")
b.para(
    "Cả hai đều mở TAB MỚI hiển thị bản in và trình duyệt tự mở hộp thoại in. Đóng hộp thoại vẫn "
    "xem được bản in trên trang; muốn in lại thì bấm nút «In» ở góc trên bên trái trang.")
b.image("15-man-in.png", "Bản in phiếu thu — có đủ 2 liên")
b.para("Bản in gồm ĐỦ 2 LIÊN, nội dung giống hệt nhau, mỗi liên có:")
b.table([
    ["Vị trí", "Nội dung"],
    ["Đầu trang", "Ảnh tiêu đề thư của công ty (logo, tên, địa chỉ, điện thoại, email, website)."],
    ["Tiêu đề", "«PHIẾU THU», dưới là ngày viết bằng chữ."],
    ["Góc phải tiêu đề", "«Liên số: 1» hoặc «Liên số: 2», «Số: «mã phiếu»», dòng «Nợ:» và «Có:» "
     "kèm số tiền."],
    ["Thông tin đầu phiếu", "Người nộp tiền, Người đề nghị, Phòng ban, Lý do thu."],
    ["Bảng nội dung", "Cột STT, Khách hàng, Số đơn hàng/Hợp đồng, Số tiền, Ghi chú; kèm dòng "
     "«Tổng cộng»."],
    ["Dưới bảng", "Dòng «Bằng chữ:» đọc số tiền tổng."],
    ["Cuối liên", "Năm ô ký: BAN GIÁM ĐỐC, KẾ TOÁN TRƯỞNG, NGƯỜI NỘP TIỀN, NGƯỜI LẬP PHIẾU, "
     "THỦ QUỸ."],
])
b.para(
    "Phiếu thuộc loại thu «Thu khác» KHÔNG in được — nút In không hiện, vì loại này không có mẫu "
    "in. In phiếu không làm thay đổi trạng thái hay lịch sử của phiếu.")

b.h2("3. Xuất Excel")
b.para(
    "Bấm nút «Xuất Excel» ở màn chi tiết, hoặc nút cùng tên trên dòng danh sách. Hệ thống tải về "
    "tệp có tên phieu_thu.xlsx chứa ĐÚNG MỘT phiếu vừa chọn.")
b.para(
    "Lưu ý: màn này KHÔNG có chức năng xuất Excel cả danh sách — mỗi lần chỉ xuất được một phiếu. "
    "Khác với nút In, chức năng Xuất Excel dùng được cả với phiếu loại «Thu khác».")

b.h2("4. Cột «Số tiền» trên danh sách — điểm dễ hiểu nhầm")
b.para(
    "Cột «Số tiền» LUÔN là tổng số tiền DUYỆT THU của phiếu, kể cả sau khi phiếu đã được duyệt "
    "với số thực thu khác. Ví dụ: phiếu có duyệt thu 500.000 và thực thu 300.000 thì cột này vẫn "
    "hiện 500.000 — đây là hành vi ĐÚNG, khớp với hệ thống cũ.")
b.para(
    "Hai ô lọc «Số tiền từ – đến» và nút sắp xếp trên cột này cũng chạy theo số duyệt thu. Muốn "
    "xem số thực thu thì phải mở màn chi tiết của phiếu.")

# ══════════════════════════════════════════════════════════ PHẦN 10
b.h1("PHẦN 10: LỊCH SỬ THAY ĐỔI")

b.h2("1. Hai nơi xem lịch sử")
b.para("Nội dung hai nơi giống hệt nhau, chọn nơi nào tiện hơn:")
b.bullet(
    "Từ danh sách: cuộn ngang tới cột Hành động, mở menu ba chấm rồi bấm «Lịch sử». Cửa sổ «Lịch "
    "sử thay đổi» mở ra.")
b.bullet(
    "Từ màn chi tiết: cuộn xuống khối «Lịch sử» ở cuối trang rồi bấm «Xem lịch sử». Khối bung ra "
    "ngay trong trang, nút đổi thành «Thu gọn».")
b.image("24-lich-su.png", "Cửa sổ Lịch sử thay đổi mở từ danh sách")
b.image("26-lich-su-man-chi-tiet.png", "Khối Lịch sử ở cuối màn chi tiết, đang bung ra")

b.h2("2. Nội dung mỗi mốc lịch sử")
b.para("Các mốc xếp theo thời gian, mới nhất ở trên. Mỗi mốc gồm:")
b.bullet("Ngày giờ xảy ra thay đổi.")
b.bullet("Loại thao tác: «Tạo mới», «Thay đổi thông tin», hoặc thay đổi trạng thái.")
b.bullet("Dòng «Người thực hiện: Họ tên — Phòng ban».")
b.bullet(
    "Với «Thay đổi thông tin»: liệt kê từng trường bị đổi kèm giá trị cũ và giá trị mới, ví dụ "
    "«Người nộp tiền: Nguyễn Văn A → Trần Thị B».")
b.bullet(
    "Với thay đổi trạng thái: ghi bằng TÊN trạng thái, ví dụ «Đang tạo» chuyển thành «Chờ duyệt».")
b.para("Hệ thống ghi lịch sử ở các thời điểm sau:")
b.table([
    ["Thao tác", "Lịch sử ghi lại"],
    ["Lập phiếu (Lưu hoặc Lưu và gửi duyệt)", "Một mốc «Tạo mới» kèm ảnh chụp toàn bộ nội dung."],
    ["Sửa phiếu", "Một mốc «Thay đổi thông tin» liệt kê các trường đã đổi."],
    ["Gửi duyệt khi sửa", "Thêm một mốc thay đổi trạng thái («Đang tạo» → «Chờ duyệt»)."],
    ["Duyệt phiếu", "Hai mốc riêng: một mốc ghi số tiền thực thu từng dòng và ngày hạch toán; "
     "một mốc thay đổi trạng thái («Chờ duyệt» → «Đã duyệt») kèm ghi chú đã ghi bút toán."],
    ["Hủy phiếu", "Một mốc thay đổi trạng thái («Chờ duyệt» → «Hủy») kèm ĐÚNG lý do hủy đã nhập."],
    ["Xóa phiếu", "Một mốc xoá kèm ảnh chụp nội dung phiếu trước khi xoá."],
])
b.para(
    "Nút «Bộ lọc» cho phép lọc theo nhóm thao tác. Nút «Làm mới» nạp lại danh sách mốc. Phiếu cũ "
    "chuyển từ hệ thống trước, chưa từng thao tác trên hệ thống mới, sẽ hiện dòng «Chưa có lịch "
    "sử thao tác nào.».")
b.para("Xem lịch sử không cần quyền riêng — ai nhìn thấy phiếu thì xem được lịch sử của phiếu đó.")

# ══════════════════════════════════════════════════════════ PHẦN 11
b.h1("PHẦN 11: HƯỚNG DẪN THEO TỪNG VAI TRÒ")

b.h2("1. Người dùng không có quyền nào")
b.para("Nhìn thấy: chỉ phiếu thu do chính mình lập, ở mọi trạng thái.")
b.para("Làm được: xem chi tiết, in, xuất Excel, xem lịch sử các phiếu của mình.")
b.para(
    "Không làm được: không lập được phiếu mới (cửa sổ chọn phiếu đề nghị bị từ chối); không có "
    "nút Duyệt và Hủy; khối lọc nâng cao không có nhóm ô Công ty – Phòng ban – Bộ phận.")

b.h2("2. Kế toán thanh toán (quyền «Kế toán thanh toán»)")
b.para("Đây là vai trò LẬP phiếu thu. Làm được:")
b.bullet("Bấm «Tạo mới», mở cửa sổ chọn phiếu đề nghị, lập phiếu thu mới.")
b.bullet("Lưu nháp hoặc Lưu và gửi duyệt.")
b.bullet("Sửa và xoá phiếu ở trạng thái «Đang tạo».")
b.bullet("Xem chi tiết, in, xuất Excel, xem lịch sử.")
b.para(
    "Không làm được: không nhập được số tiền thực thu; không có nút «Duyệt phiếu thu» và «Hủy "
    "phiếu thu» — kể cả với phiếu do chính mình lập.")

b.h2("3. Thủ quỹ (quyền «Thủ quỹ duyệt phiếu thu»)")
b.para("Đây là vai trò DUYỆT phiếu thu. Làm được thêm, với phiếu ở trạng thái «Chờ duyệt»:")
b.bullet("Nhập số tiền thực thu cho từng dòng, hoặc dùng nút «Phân bổ» để điền hộ.")
b.bullet("Bấm «Duyệt phiếu thu» — hệ thống ghi bút toán vào sổ kế toán.")
b.bullet("Bấm «Hủy phiếu thu» kèm lý do.")
b.para("Nhận thông báo trên chuông mỗi khi có phiếu thu mới được gửi duyệt trong công ty mình.")
b.para(
    "Không làm được: không sửa, không xoá phiếu của người khác. Nếu không kiêm quyền «Kế toán "
    "thanh toán» thì cũng không lập được phiếu mới.")

b.h2("4. Cấp công ty (quyền «Xem tất cả phiếu thu của công ty»)")
b.para(
    "Nhìn thấy: toàn bộ phiếu thu thuộc công ty của mình, không phân biệt người lập. Nháp của "
    "người khác vẫn bị ẩn. Khối lọc nâng cao có thêm nhóm ô Công ty – Phòng ban – Bộ phận.")
b.para(
    "Quyền này CHỈ mở rộng phạm vi nhìn — muốn lập phiếu vẫn phải có «Kế toán thanh toán», muốn "
    "duyệt vẫn phải có «Thủ quỹ duyệt phiếu thu».")

b.h2("5. Cấp tổng công ty (quyền «Xem tất cả phiếu thu của tổng công ty»)")
b.para(
    "Nhìn thấy: phiếu thu của mọi công ty. Nháp của người khác vẫn bị ẩn. Vai trò quản trị hệ "
    "thống có phạm vi xem tương đương và được coi như có đủ cả bốn quyền của màn.")

# ══════════════════════════════════════════════════════════ PHẦN 12
b.h1("PHẦN 12: CÁC LỖI THƯỜNG GẶP VÀ CÁCH XỬ LÝ")
b.table([
    ["Hiện tượng", "Nguyên nhân", "Cách xử lý"],
    ["Vào màn thấy thiếu phiếu so với lần trước",
     "Bộ lọc của lần trước vẫn còn (hệ thống ghi nhớ 10 phút).",
     "Bấm nút «Làm mới» rồi xem lại."],
    ["Gõ vào ô tìm nhanh mà danh sách không đổi",
     "Ô tìm nhanh không tự tìm khi gõ.",
     "Bấm nút «Tìm kiếm» hoặc nhấn Enter."],
    ["Không thấy nhóm ô lọc Công ty – Phòng ban – Bộ phận",
     "Thiếu quyền xem theo tổng công ty và theo công ty.",
     "Liên hệ quản trị để được cấp quyền phù hợp."],
    ["Bấm ô «Số phiếu đề nghị» thì bị báo không có quyền",
     "Thiếu quyền «Kế toán thanh toán».",
     "Liên hệ quản trị; hoặc nhờ kế toán thanh toán lập phiếu."],
    ["Không tìm thấy phiếu đề nghị cần lập trong cửa sổ chọn",
     "Phiếu chưa gửi duyệt, hoặc đã có phiếu thu khác (kể cả phiếu thu đang là nháp hoặc đã hủy).",
     "Kiểm tra trạng thái phiếu đề nghị ở màn Phiếu đề nghị thu tiền."],
    ["Lập phiếu thì báo «Đề nghị thu tiền đã lập phiếu thu tiền»",
     "Người khác vừa lập phiếu thu cho cùng phiếu đề nghị đó.",
     "Tải lại màn, tìm phiếu thu đã có thay vì lập phiếu thứ hai."],
    ["Không thấy nút Sửa / Xóa trên phiếu của mình",
     "Phiếu đã rời trạng thái «Đang tạo».",
     "Phiếu «Chờ duyệt» chỉ thủ quỹ mới xử lý được (duyệt hoặc hủy)."],
    ["Không thấy nút «Duyệt phiếu thu» dù là thủ quỹ",
     "Phiếu không ở trạng thái «Chờ duyệt».",
     "Kiểm tra lại trạng thái phiếu."],
    ["Gõ số thực thu bị báo đỏ «Không được lớn hơn số tiền duyệt thu»",
     "Số thực thu vượt số duyệt thu của chính dòng đó.",
     "Sửa lại cho nhỏ hơn hoặc bằng; nếu thực tế thu nhiều hơn thì phải lập phiếu thu khác."],
    ["Bấm Duyệt thì báo «Phiếu thu tiền đã được duyệt!»",
     "Thủ quỹ khác vừa duyệt phiếu này trước.",
     "Tải lại màn để xem kết quả; sổ kế toán không bị ghi trùng."],
    ["Cột «Số tiền» trên danh sách khác số thực thu của phiếu đã duyệt",
     "Cột này luôn là tổng số tiền DUYỆT THU.",
     "Đây là hành vi đúng. Mở màn chi tiết để xem số thực thu."],
    ["Không thấy nút In trên một phiếu",
     "Phiếu thuộc loại thu «Thu khác» — loại này không có mẫu in.",
     "Dùng nút «Xuất Excel» thay thế."],
    ["Đã hủy phiếu thu, giờ muốn lập lại nhưng không được",
     "Hủy phiếu thu là ngõ cụt theo thiết kế.",
     "Liên hệ bộ phận kinh doanh lập phiếu đề nghị thu tiền mới."],
    ["Không mở được phiếu của đồng nghiệp",
     "Không phải người lập, không phải người duyệt, và không có quyền xem theo công ty hoặc tổng "
     "công ty.",
     "Liên hệ quản trị để được cấp quyền xem phù hợp."],
])

b.finish()
