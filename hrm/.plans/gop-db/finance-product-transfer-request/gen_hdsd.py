# -*- coding: utf-8 -*-
"""Sinh tai lieu HDSD (.docx) cho man "Phieu yeu cau chuyen hang" (phan he Tai chinh).

Khung + style lay tu `.claude/skills/hdsd-documenter/assets/HDSD_MAU.docx`.
Anh that: pycch_shots/ (cong dev hrm-crm.eteksofts.com, 03/09/2026) — KHONG commit.

Chay:  python .plans/gop-db/finance-product-transfer-request/gen_hdsd.py
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

OUT = os.path.join(HERE, "HDSD_Phiếu yêu cầu chuyển hàng.docx")
SHOTS = os.path.join(HERE, "pycch_shots")

MENU = ("Tài chính → Hàng hoá - Dịch vụ - Vận chuyển → Điều chuyển → "
        "Phiếu điều chuyển hàng")

b = HdsdBuilder(output=OUT, shots_dir=SHOTS,
                cover_title="(Màn hình: Phiếu yêu cầu chuyển hàng)",
                doc_title="HDSD - Phiếu yêu cầu chuyển hàng")

# ══════════════════════════════════════════════════════════ TỔNG QUAN
b.h1("TỔNG QUAN")

b.h2("1. Thuật ngữ và từ viết tắt")
b.table([
    ["Thuật ngữ", "Giải thích"],
    ["Phiếu yêu cầu chuyển hàng",
     "Chứng từ do người kinh doanh lập để đề nghị bộ phận kho chuyển hàng về phục vụ một hoặc "
     "nhiều khách hàng. Mã phiếu do hệ thống sinh tự động, dạng PYCCH kèm 5 chữ số."],
    ["Dòng hàng hoá",
     "Một dòng trong bảng Danh sách hàng hóa của phiếu, ứng với một mã hàng. Mỗi mã hàng chỉ "
     "được xuất hiện một lần trong cùng một phiếu."],
    ["Dòng khách hàng",
     "Dòng con nằm trong ô Khách hàng của một dòng hàng hoá, gồm: khách hàng cần hàng, số "
     "lượng, ngày cần và ghi chú. Một dòng hàng hoá phải có ít nhất một dòng khách hàng."],
    ["ĐVT (đơn vị tính)",
     "Đơn vị của hàng hoá trên phiếu. Một hàng có thể có nhiều đơn vị kèm hệ số quy đổi, hiển "
     "thị trong danh sách dạng «Thùng (x10)»."],
    ["Giá niêm yết",
     "Giá tham khảo của hàng hoá theo đơn vị tính đang chọn. Chỉ để người lập tham khảo — "
     "KHÔNG được lưu vào phiếu và không xuất hiện trên bản in."],
    ["SL tồn",
     "Số lượng tồn tham khảo của hàng hoá tại kho đang chọn ở ô «Xem tồn theo kho», đã quy đổi "
     "theo đơn vị tính đang chọn. Hệ thống KHÔNG chặn khi số lượng đề nghị vượt tồn."],
    ["Người tiếp nhận",
     "Người của bộ phận kho đã xử lý phiếu. Ô này được ghi khi phiếu bị Không duyệt hoặc khi "
     "chuỗi nghiệp vụ kho tiếp nhận phiếu."],
    ["Đang tạo", "Phiếu mới lưu nháp. Chỉ người lập nhìn thấy, sửa được và xoá được."],
    ["Chờ duyệt", "Phiếu đã gửi, đang chờ bộ phận kho tiếp nhận hoặc từ chối."],
    ["Đã tiếp nhận / Đang đề nghị / Đang xuất kho / Đã xuất kho / Đang vận chuyển / "
     "Đang nhập kho / Đã nhập kho / Đã nhập hàng / Đã phân bổ",
     "Các bước tiếp theo do chuỗi nghiệp vụ kho cập nhật. Người lập chỉ theo dõi, không thao "
     "tác được trên màn này."],
    ["Đã hủy", "Phiếu đã bị hủy trong chuỗi nghiệp vụ kho."],
    ["Không duyệt",
     "Thao tác của người có quyền Kế toán kho: trả phiếu về trạng thái Đang tạo kèm lý do để "
     "người lập sửa và gửi lại. Đây KHÔNG phải huỷ phiếu."],
    ["Tổng hợp",
     "Thao tác mở màn lập phiếu đề nghị xuất hàng ở cổng cũ (mở tab mới), mang sẵn phiếu đang "
     "xem để kho gom vào lệnh xuất."],
])

b.h2("2. Cập nhật tài liệu")
b.table([
    ["Phiên bản", "Ngày", "Nội dung", "Người thực hiện"],
    ["1.0", "03/09/2026", "Ban hành lần đầu cho màn Phiếu yêu cầu chuyển hàng "
     "(phân hệ Tài chính, nhóm Hàng hoá - Dịch vụ - Vận chuyển).", "Nhóm phát triển HRM"],
])

b.h2("3. Giới thiệu chung")
b.para(
    "Màn hình Phiếu yêu cầu chuyển hàng dùng để lập và theo dõi các đề nghị chuyển hàng gửi bộ "
    "phận kho. Người kinh doanh lập phiếu, đính kèm chứng từ dạng PDF, ghi rõ từng khách hàng "
    "cần hàng cùng số lượng và ngày cần, rồi gửi duyệt. Bộ phận kho tiếp nhận phiếu để lập lệnh "
    "xuất, hoặc trả phiếu về cho người lập sửa lại nếu thông tin chưa đạt.")
b.para("Đường dẫn vào màn hình:", bold_prefix=None)
b.bullet("Menu: " + MENU)
b.bullet("Đường dẫn trực tiếp: /finance/product-transfer-requests")
b.para(
    "Lưu ý: chỉ có duy nhất MỘT mục menu trỏ vào màn này. Không có màn «chờ duyệt» riêng — "
    "phiếu đang chờ duyệt nằm chung trong danh sách và được lọc bằng ô Trạng thái.")
b.image("31-duong-dan-menu.png",
        "Đường dẫn menu tới màn Phiếu yêu cầu chuyển hàng")

b.h2("4. Quyền và phạm vi dữ liệu")
b.para(
    "Màn này KHÔNG yêu cầu quyền riêng cho các thao tác Tạo mới, Sửa, Xóa, In, Xuất Excel và "
    "Lịch sử: bất kỳ ai đăng nhập được vào phân hệ Tài chính đều lập được phiếu. Quyền chỉ "
    "quyết định hai việc: NHÌN THẤY BAO NHIÊU PHIẾU và CÓ ĐƯỢC KHÔNG DUYỆT / TỔNG HỢP HAY KHÔNG.")
b.table([
    ["Tên quyền", "Cho phép làm gì", "Thể hiện trên giao diện"],
    ["Xem yêu cầu chuyển hàng theo tổng công ty",
     "Nhìn thấy phiếu của mọi công ty trong tập đoàn.",
     "Danh sách hiện phiếu của tất cả công ty."],
    ["Xem yêu cầu chuyển hàng theo công ty",
     "Nhìn thấy phiếu thuộc công ty của mình.",
     "Danh sách chỉ hiện phiếu cùng công ty với người đăng nhập."],
    ["Xem yêu cầu chuyển hàng theo phòng ban",
     "Nhìn thấy phiếu thuộc các phòng ban mình được giao quản lý trong công ty mình, cộng thêm "
     "mọi phiếu do chính mình lập.",
     "Danh sách hiện phiếu của phòng ban quản lý + phiếu của chính mình."],
    ["Xem yêu cầu chuyển hàng theo bộ phận",
     "Nhìn thấy phiếu thuộc các bộ phận mình được giao quản lý trong công ty mình, cộng thêm "
     "mọi phiếu do chính mình lập.",
     "Danh sách hiện phiếu của bộ phận quản lý + phiếu của chính mình."],
    ["Kế toán kho",
     "Mở được phiếu của người khác trong CÙNG CÔNG TY; với phiếu đang ở trạng thái Chờ duyệt và "
     "cùng công ty thì được Không duyệt và Tổng hợp. Đồng thời là nhóm nhận thông báo khi có "
     "phiếu mới gửi duyệt.",
     "Màn chi tiết hiện thêm khối «Ghi chú duyệt» và hai nút «Không duyệt», «Tổng hợp». Trên "
     "danh sách, dòng phiếu Chờ duyệt hiện nút Tổng hợp (biểu tượng dấu tích kép)."],
    ["(Không có quyền nào ở trên)",
     "Chỉ nhìn thấy phiếu do chính mình lập; vẫn lập, sửa, xoá, in, xuất Excel bình thường.",
     "Danh sách chỉ có phiếu của mình; không có nút Không duyệt / Tổng hợp."],
])
b.para(
    "Vai trò quản trị hệ thống được coi như có đủ bốn quyền xem ở trên. Tuy nhiên với hai nút "
    "«Không duyệt» và «Tổng hợp» thì quản trị hệ thống VẪN phải cùng công ty với phiếu mới thấy "
    "nút — xem phiếu công ty khác thì chỉ đọc được nội dung.")
b.para(
    "Hai quy tắc luôn được áp dụng, không quyền nào gỡ được:")
b.bullet(
    "Phiếu ở trạng thái «Đang tạo» của NGƯỜI KHÁC luôn bị ẩn khỏi danh sách, kể cả với quản trị "
    "hệ thống. Mỗi người chỉ thấy nháp của chính mình.")
b.bullet(
    "Chỉ sửa và xoá được phiếu ở trạng thái «Đang tạo» DO CHÍNH MÌNH lập. Thiếu một trong hai "
    "điều kiện là nút Sửa / Xóa không hiện.")

# ══════════════════════════════════════════════════════════ PHẦN 1
b.h1("PHẦN 1: TRUY CẬP VÀ BỐ CỤC MÀN HÌNH")

b.h2("1. Cách vào màn hình")
b.para("Thực hiện lần lượt:")
b.para("1. Đăng nhập hệ thống, ở trang chọn phân hệ bấm ô «Tài chính».")
b.para("2. Trên thanh menu bên trái, bấm nhóm «Hàng hoá - Dịch vụ - Vận chuyển».")
b.para("3. Trong bảng chức năng vừa mở, bấm nhóm «Điều chuyển» ở cột bên trái.")
b.para("4. Bấm chức năng «Phiếu điều chuyển hàng» ở cột bên phải.")
b.para(
    "Màn hình mở ra có tiêu đề «Phiếu yêu cầu chuyển hàng». Nhóm «Điều chuyển» có đúng 2 chức "
    "năng — chức năng còn lại là «Phiếu chuyển hàng nhập thẳng», thuộc màn hình khác.")

b.h2("2. Bố cục màn danh sách")
b.image("01-danh-sach.png", "Màn hình danh sách Phiếu yêu cầu chuyển hàng")
b.para("Màn hình chia làm 2 khối từ trên xuống:")
b.bullet(
    "Khối «Bộ lọc danh sách»: ô tìm nhanh, nút «Tìm kiếm», nút «Làm mới», nút «Cài đặt bộ lọc» "
    "và nút «Tìm kiếm nâng cao».", bold_prefix=None)
b.bullet(
    "Khối lưới dữ liệu: tiêu đề «Phiếu yêu cầu chuyển hàng», ba nút thao tác ở góc phải "
    "(«Tạo mới», «Xuất Excel», nút biểu tượng cấu hình cột), bảng dữ liệu và thanh phân trang.")

b.h2("3. Các cột của bảng danh sách")
b.table([
    ["Cột", "Nội dung", "Mặc định hiển thị"],
    ["STT", "Số thứ tự dòng, đánh theo từng trang (sang trang 2 với cỡ 10 dòng thì bắt đầu từ "
     "11).", "Có (không tắt được)"],
    ["Mã yêu cầu", "Mã phiếu dạng PYCCH kèm 5 chữ số. Bấm vào mã để mở màn chi tiết. Sắp xếp "
     "được.", "Có (không tắt được)"],
    ["Người tiếp nhận", "Người của bộ phận kho đã xử lý phiếu. Chưa ai xử lý thì hiện dấu "
     "gạch ngang.", "Có"],
    ["Ngày tiếp nhận", "Ngày giờ tiếp nhận, dạng ngày/tháng/năm giờ:phút. Sắp xếp được.",
     "Ẩn — bật trong Tuỳ chỉnh cột"],
    ["Người cập nhật", "Người sửa phiếu gần nhất.", "Ẩn — bật trong Tuỳ chỉnh cột"],
    ["Ngày cập nhật", "Thời điểm sửa gần nhất. LƯU Ý: cột này có mũi tên nhưng bấm vào KHÔNG "
     "sắp xếp được, danh sách quay về thứ tự mặc định.", "Ẩn — bật trong Tuỳ chỉnh cột"],
    ["Người tạo", "Người lập phiếu.", "Có"],
    ["Ngày tạo", "Thời điểm lập phiếu, dạng ngày/tháng/năm giờ:phút. Sắp xếp được.", "Có"],
    ["Trạng thái", "Nhãn màu: đỏ với Chờ duyệt / Đang tạo / Đã hủy, xanh với các trạng thái "
     "còn lại.", "Có"],
    ["Hành động", "Các nút thao tác của dòng, thay đổi theo trạng thái và quyền.",
     "Có (không tắt được)"],
])
b.para(
    "Mặc định danh sách sắp xếp theo Ngày tạo giảm dần — phiếu mới nhất nằm trên cùng. Chỉ ba "
    "cột sắp xếp được thật: Mã yêu cầu, Ngày tạo và Ngày tiếp nhận.")

b.h2("4. Các nút thao tác trên một dòng")
b.para(
    "Cột «Hành động» hiển thị tối đa 2 nút chính, các nút còn lại nằm trong menu ba chấm. Nút "
    "không đủ điều kiện bị ẩn hẳn chứ không hiện mờ.")
b.table([
    ["Nút", "Biểu tượng", "Điều kiện hiện", "Tác dụng"],
    ["Sửa", "Bút chì", "Phiếu ở trạng thái «Đang tạo» VÀ do chính mình lập",
     "Mở màn Sửa phiếu."],
    ["Xóa", "Thùng rác đỏ", "Phiếu ở trạng thái «Đang tạo» VÀ do chính mình lập",
     "Mở hộp xác nhận xoá phiếu."],
    ["Tổng hợp", "Dấu tích kép", "Phiếu ở trạng thái «Chờ duyệt», người dùng có quyền Kế toán "
     "kho (hoặc là quản trị hệ thống) VÀ cùng công ty với phiếu",
     "Mở tab mới sang màn lập phiếu đề nghị xuất hàng của cổng cũ."],
    ["In", "Máy in", "Luôn hiện", "Mở tab mới hiển thị bản in của phiếu."],
    ["Lịch sử", "Đồng hồ quay ngược", "Luôn hiện", "Mở popup Lịch sử thay đổi của phiếu."],
])
b.image("25-menu-hanh-dong.png",
        "Menu ba chấm trên dòng phiếu «Đang tạo» — chứa nút In và Lịch sử")

# ══════════════════════════════════════════════════════════ PHẦN 2
b.h1("PHẦN 2: TÌM KIẾM VÀ LỌC DANH SÁCH")

b.h2("1. Ô tìm nhanh")
b.para(
    "Ô tìm nhanh nằm ngay dưới tiêu đề «Bộ lọc danh sách», ghi sẵn dòng gợi ý «Tìm theo mã yêu "
    "cầu...». Thực tế ô này tìm theo MÃ YÊU CẦU HOẶC TÊN NGƯỜI TẠO.")
b.para("Cách dùng:")
b.para("1. Gõ mã phiếu (ví dụ 07365) hoặc tên người tạo (ví dụ Phạm Ngọc Thái) vào ô.")
b.para("2. Bấm nút «Tìm kiếm» màu xanh bên phải, hoặc nhấn phím Enter.")
b.para(
    "LƯU Ý: ô tìm nhanh KHÔNG tự tìm khi đang gõ — bắt buộc phải bấm nút «Tìm kiếm». Đây là "
    "điểm khác với các ô trong «Tìm kiếm nâng cao».")

b.h2("2. Tìm kiếm nâng cao")
b.para(
    "Bấm nút «Tìm kiếm nâng cao» ở góc phải khối lọc để mở thêm 6 ô lọc. Khi khối đang mở, nút "
    "đổi chữ thành «Ẩn tìm kiếm nâng cao».")
b.image("02-loc-nang-cao.png", "Khối Tìm kiếm nâng cao khi đang mở")
b.table([
    ["Ô lọc", "Kiểu nhập", "Cách hoạt động"],
    ["Trạng thái", "Danh sách chọn một giá trị",
     "Liệt kê đủ các trạng thái: Đã tiếp nhận, Chờ duyệt, Đang tạo, Đang đề nghị, Đang xuất "
     "kho, Đã xuất kho, Đang vận chuyển, Đang nhập kho, Đã nhập kho, Đã nhập hàng, Đã phân bổ, "
     "Đã hủy. Tên «Đang nhập kho» xuất hiện hai lần vì kho có hai bước khác nhau cùng tên."],
    ["Tên/mã hàng hóa", "Gõ tay",
     "Tìm phiếu có chứa hàng hoá khớp tên hoặc mã hàng. TỰ TÌM ngay khi gõ, không cần bấm nút."],
    ["Người tạo", "Danh sách nhân viên", "Lọc theo người lập phiếu."],
    ["Người tiếp nhận", "Danh sách nhân viên",
     "Lọc theo người của kho đã xử lý phiếu. Phiếu chưa ai tiếp nhận sẽ không nằm trong kết quả."],
    ["Ngày tạo từ", "Chọn ngày trên lịch", "Lọc theo NGÀY TẠO PHIẾU, tính từ ngày này trở đi."],
    ["Ngày tạo đến", "Chọn ngày trên lịch",
     "Lọc theo NGÀY TẠO PHIẾU, tính tới hết ngày này. Chọn ngày hôm nay thì phiếu lập chiều nay "
     "vẫn nằm trong kết quả."],
])
b.image("20-loc-trang-thai.png", "Danh sách trạng thái trong ô lọc Trạng thái")
b.para(
    "Các điều kiện cộng dồn với nhau: chọn Trạng thái «Chờ duyệt» và Người tạo «Phạm Ngọc Thái» "
    "thì chỉ ra phiếu thoả CẢ HAI. Mỗi lần đổi một ô, danh sách tự nạp lại và quay về trang 1.")
b.para(
    "LƯU Ý QUAN TRỌNG: lọc Trạng thái = «Đang tạo» chỉ ra nháp của CHÍNH MÌNH, dù người dùng có "
    "quyền xem toàn tổng công ty. Nháp của người khác không bao giờ hiện.")

b.h2("3. Nút Làm mới")
b.para(
    "Bấm «Làm mới» để xoá toàn bộ điều kiện lọc và ô tìm nhanh, đưa danh sách về trang 1. Phạm "
    "vi dữ liệu theo quyền KHÔNG đổi — «Làm mới» chỉ xoá điều kiện lọc chứ không mở rộng phạm vi.")

b.h2("4. Cài đặt bộ lọc — chọn ô lọc muốn hiển thị")
b.para(
    "Bấm nút «Cài đặt bộ lọc» để mở cửa sổ cho phép ẩn bớt hoặc đổi thứ tự các ô lọc nâng cao.")
b.image("05-cai-dat-bo-loc.png", "Cửa sổ Cài đặt bộ lọc")
b.para("Trong cửa sổ này:")
b.bullet("Bỏ tích một ô để ẩn ô lọc đó khỏi khối Tìm kiếm nâng cao.")
b.bullet("Kéo biểu tượng sáu chấm ở đầu mỗi ô để đổi thứ tự hiển thị.")
b.bullet("Bấm «Lưu» để áp dụng — cấu hình được ghi nhớ riêng cho từng người và từng màn hình.")
b.bullet("Bấm «Khôi phục mặc định» để đưa về đủ 6 ô theo thứ tự ban đầu.")
b.bullet("Bấm «Đóng» để thoát mà không lưu thay đổi.")

b.h2("5. Ghi nhớ bộ lọc trong 10 phút")
b.para(
    "Hệ thống ghi nhớ điều kiện lọc và trạng thái đóng/mở của khối Tìm kiếm nâng cao trong 10 "
    "phút. Rời màn rồi quay lại trong khoảng thời gian này thì điều kiện cũ vẫn còn — nếu thấy "
    "danh sách «thiếu phiếu», hãy bấm «Làm mới» trước khi kết luận là mất dữ liệu.")

# ══════════════════════════════════════════════════════════ PHẦN 3
b.h1("PHẦN 3: SẮP XẾP, PHÂN TRANG VÀ CẤU HÌNH CỘT")

b.h2("1. Sắp xếp")
b.para(
    "Bấm vào tiêu đề cột có biểu tượng hai mũi tên để sắp xếp. Bấm lần một là tăng dần, bấm lần "
    "hai là giảm dần. Mỗi lần đổi sắp xếp, danh sách quay về trang 1 nhưng GIỮ NGUYÊN điều kiện "
    "lọc.")
b.bullet("Sắp xếp được thật: Mã yêu cầu, Ngày tạo, Ngày tiếp nhận.")
b.bullet(
    "Cột «Ngày cập nhật» tuy có biểu tượng mũi tên nhưng bấm vào KHÔNG sắp xếp theo cột đó — "
    "danh sách quay về thứ tự mặc định (mới tạo nhất trước). Đây là hạn chế đã biết.")

b.h2("2. Phân trang")
b.para(
    "Cuối bảng có dòng «Hiển thị a–b / N»: a là số thứ tự dòng đầu trang, b là dòng cuối trang, "
    "N là tổng số phiếu khớp bộ lọc và nằm trong phạm vi quyền.")
b.bullet("Ô «Số dòng/trang» có 5 lựa chọn: 5, 10, 20, 50, 100. Mặc định là 10.")
b.bullet("Đổi số dòng/trang sẽ đưa danh sách về trang 1.")
b.bullet("Chuyển trang KHÔNG làm mất điều kiện lọc và không đổi chiều sắp xếp.")

b.h2("3. Tuỳ chỉnh cột hiển thị")
b.para(
    "Bấm nút biểu tượng cột (nút thứ ba, bên phải nút «Xuất Excel») để mở cửa sổ «Tuỳ chỉnh cột».")
b.image("03-cau-hinh-cot.png", "Cửa sổ Tuỳ chỉnh cột hiển thị")
b.para("Trong cửa sổ này:")
b.bullet("Bỏ tích một cột để ẩn cột đó khỏi bảng.")
b.bullet(
    "Ba cột STT, Mã yêu cầu và Hành động có biểu tượng ổ khoá, chữ mờ — luôn hiển thị, không "
    "bỏ tích được.")
b.bullet("Kéo biểu tượng ba gạch ở cuối mỗi dòng để đổi thứ tự cột.")
b.bullet(
    "Bấm «Lưu» để áp dụng. Cấu hình được ghi nhớ riêng cho từng người và riêng cho màn này, "
    "không ảnh hưởng các màn khác.")
b.bullet("Bấm «Đóng» để thoát mà không lưu.")

# ══════════════════════════════════════════════════════════ PHẦN 4
b.h1("PHẦN 4: TẠO MỚI PHIẾU YÊU CẦU CHUYỂN HÀNG")

b.h2("1. Mở màn Tạo mới")
b.para(
    "Bấm nút «Tạo mới» (biểu tượng dấu cộng, màu xanh) ở góc phải khối lưới. Hệ thống mở màn "
    "riêng có tiêu đề «Thêm phiếu yêu cầu chuyển hàng». Chức năng này KHÔNG cần quyền riêng — "
    "ai đăng nhập được vào phân hệ Tài chính đều lập phiếu được.")
b.image("06-tao-moi.png", "Màn Thêm phiếu yêu cầu chuyển hàng khi vừa mở")

b.h2("2. Khối Thông tin chung")
b.table([
    ["Trường", "Kiểu nhập", "Bắt buộc", "Giá trị điền sẵn khi tạo mới", "Ghi chú"],
    ["Ngày lập", "Ô chỉ đọc (nền xám)", "—", "Ngày hôm nay, dạng ngày/tháng/năm",
     "Không sửa được. Hệ thống tự ghi thời điểm lưu phiếu."],
    ["Người lập", "Ô chỉ đọc (nền xám)", "—", "Họ tên người đang đăng nhập",
     "Không sửa được, không đổi sang người khác được."],
    ["Ghi chú", "Ô nhập nhiều dòng", "Không", "Để trống",
     "Tối đa 255 ký tự. Vượt quá sẽ hiện lỗi đỏ ngay khi gõ."],
])
b.para(
    "Hộp «Giá trị điền sẵn khi tạo mới»: Ngày lập = ngày hôm nay; Người lập = người đang đăng "
    "nhập; Ghi chú = trống; bảng hàng hoá = trống (hiện dòng «Chưa có hàng hóa»); ô «Xem tồn "
    "theo kho» = kho mặc định của hệ thống; khối File đính kèm = chưa có file nào.")

b.h2("3. Khối Danh sách hàng hóa")
b.para(
    "Tiêu đề khối có dấu sao đỏ — phiếu phải có ít nhất một hàng hoá. Bảng có 7 cột:")
b.table([
    ["Cột", "Nội dung", "Bắt buộc"],
    ["STT", "Số thứ tự dòng hàng hoá, hệ thống tự đánh.", "—"],
    ["Hàng hóa", "Tên hàng, dòng phụ bên dưới ghi Model và Mã hàng. Chỉ đọc — chọn từ popup.",
     "Có"],
    ["ĐVT", "Danh sách đơn vị tính của hàng đó. Đơn vị có hệ số khác 1 hiển thị kèm hệ số, "
     "ví dụ «Thùng (x10)». Mặc định chọn đơn vị đầu tiên.", "Có"],
    ["Giá niêm yết", "Giá tham khảo theo đơn vị đang chọn. Chỉ đọc, không lưu vào phiếu.", "—"],
    ["SL tồn", "Tồn tham khảo tại kho đang chọn, quy đổi theo đơn vị đang chọn. Chưa chọn kho "
     "thì hiện dấu gạch ngang.", "—"],
    ["Khách hàng", "Vùng chứa các dòng khách hàng cần hàng, nút «+ Thêm khách hàng» và dòng "
     "«Tổng cộng».", "Có"],
    ["(cột cuối)", "Nút dấu cộng ở tiêu đề để thêm hàng hoá; nút dấu trừ trên mỗi dòng để xoá "
     "hàng hoá đó.", "—"],
])

b.h3("3.1. Thêm hàng hoá")
b.para("1. Bấm nút dấu cộng màu xanh ở góc phải tiêu đề bảng (cột cuối cùng).")
b.para("2. Cửa sổ «Thêm hàng hoá» mở toàn màn hình.")
b.image("07-popup-hang-hoa.png", "Cửa sổ Thêm hàng hoá")
b.para(
    "3. Tìm hàng cần thêm: gõ tên, mã hoặc model vào ô tìm rồi bấm «Tìm kiếm»; hoặc bấm "
    "«Tìm kiếm nâng cao» để lọc chi tiết hơn.")
b.para("4. Tích vào ô vuông ở đầu mỗi dòng hàng muốn thêm (chọn được nhiều hàng cùng lúc).")
b.para("5. Bấm nút «Thêm N hàng hoá» ở góc dưới bên phải (N là số hàng vừa tích).")
b.para("6. Cửa sổ VẪN MỞ để chọn tiếp. Chọn xong hết thì bấm «Đóng».")
b.para("Sau khi đóng cửa sổ, mỗi hàng vừa thêm thành một dòng trong bảng, đã có sẵn:")
b.bullet("Đơn vị tính = đơn vị đầu tiên của hàng đó.")
b.bullet("Giá niêm yết và SL tồn tương ứng đơn vị đó.")
b.bullet("Một dòng khách hàng trống để bắt đầu nhập.")
b.image("08-bang-hang-hoa.png", "Bảng hàng hoá sau khi thêm một hàng")
b.para("Hai điều cửa sổ này KHÔNG cho làm:")
b.bullet(
    "Không thêm được hàng đã có trong phiếu. Cửa sổ đánh dấu hàng đó là đã có và không cho tích "
    "chọn lại; nếu vẫn lọt thì hệ thống bỏ qua và báo «Hàng hóa đã có trong phiếu: ...».")
b.bullet(
    "Không thêm được hàng tạm. Cửa sổ chỉ liệt kê hàng hoá có thật trong danh mục và không có "
    "đường tạo hàng tạm.")

b.h3("3.2. Đổi đơn vị tính")
b.para(
    "Bấm vào ô ĐVT của dòng hàng rồi chọn đơn vị khác. Ngay lập tức, hai ô «Giá niêm yết» và "
    "«SL tồn» đổi theo hệ số của đơn vị mới. Ví dụ tồn 100 «Cái», đổi sang «Thùng (x10)» thì "
    "SL tồn hiển thị 10.")

b.h3("3.3. Xem tồn kho tham khảo")
b.para(
    "Ô «Xem tồn theo kho» nằm ở góc phải tiêu đề khối. Bấm vào ô để mở danh sách kho — có cả "
    "kho tổng và các kho con thụt đầu dòng. Chọn kho khác thì cột «SL tồn» của TẤT CẢ các dòng "
    "nạp lại theo kho đó.")
b.image("10-xem-ton-kho.png", "Danh sách kho trong ô Xem tồn theo kho")
b.para(
    "Chọn dòng đầu tiên (ghi «Xem tồn», giá trị rỗng) thì cột SL tồn của mọi dòng chuyển thành "
    "dấu gạch ngang. LƯU Ý: số tồn chỉ để tham khảo — hệ thống KHÔNG chặn khi số lượng đề nghị "
    "vượt tồn, kể cả khi tồn bằng 0.")

b.h3("3.4. Nhập dòng khách hàng cần hàng")
b.para(
    "Mỗi dòng hàng hoá phải có ít nhất một dòng khách hàng. Một dòng khách hàng gồm 4 ô nằm "
    "ngang và một nút xoá:")
b.table([
    ["Ô", "Kiểu nhập", "Bắt buộc", "Giá trị điền sẵn", "Ghi chú"],
    ["Khách hàng", "Ô chỉ đọc, bấm vào để mở cửa sổ chọn", "Có", "Trống",
     "Sau khi chọn hiển thị dạng «mã khách hàng - tên khách hàng»."],
    ["SL", "Ô nhập số", "Có", "Trống",
     "Số nguyên từ 1 tới 999.999.999. Nhập 0 báo «Không được nhỏ hơn 1»."],
    ["Ngày cần", "Chọn ngày trên lịch", "Có", "Trống",
     "Phải LỚN HƠN ngày hôm nay. Trên lịch, hôm nay và các ngày trước đó bị mờ."],
    ["Ghi chú", "Ô nhập một dòng", "Có", "Trống",
     "BẮT BUỘC nhập (khác với ô Ghi chú của phiếu — ô đó không bắt buộc). Tối đa 255 ký tự."],
])
b.para("Cách chọn khách hàng:")
b.para("1. Bấm vào ô «Khách hàng» của dòng cần nhập.")
b.para("2. Cửa sổ «Chọn khách hàng» mở ra, có 3 ô tìm: Tên / Mã khách hàng, Mã số thuế, "
       "Số điện thoại.")
b.image("09-popup-khach-hang.png", "Cửa sổ Chọn khách hàng")
b.para("3. Gõ điều kiện tìm rồi bấm «Tìm kiếm» (hoặc bấm «Làm mới» để xoá điều kiện).")
b.para("4. Bấm vào dòng khách hàng cần chọn — cửa sổ TỰ ĐÓNG và điền vào ô.")
b.para("Cách chọn ngày cần:")
b.para("1. Bấm vào ô «Ngày cần» — lịch mở ra.")
b.para("2. Chọn một ngày từ NGÀY MAI trở đi. Hôm nay và các ngày trước đó bị mờ, không bấm được.")
b.image("22-chon-ngay-can.png",
        "Lịch chọn Ngày cần — hôm nay và các ngày trước đó bị mờ")
b.para("Thêm và bớt dòng khách hàng:")
b.bullet("Bấm «+ Thêm khách hàng» (chữ xanh, dưới các dòng) để thêm một dòng trống.")
b.bullet("Bấm dấu × đỏ ở cuối một dòng để xoá dòng đó — không hỏi xác nhận.")
b.bullet(
    "Không xoá được dòng cuối cùng của một hàng hoá: hệ thống báo «Mỗi hàng hóa phải có ít nhất "
    "1 dòng khách hàng — hãy xóa cả hàng hóa nếu không cần».")
b.bullet(
    "Dòng «Tổng cộng» ngay dưới các dòng khách hàng là tổng số lượng của chính hàng hoá đó, "
    "cập nhật tức thời khi gõ số lượng.")
b.para(
    "Được phép đặt CÙNG một khách hàng ở nhiều dòng của cùng một hàng hoá (ví dụ hai đợt giao "
    "với ngày cần khác nhau) — hệ thống không chặn và không gộp.")

b.h3("3.5. Xoá cả một hàng hoá")
b.para("1. Bấm nút dấu trừ đỏ ở cột cuối của dòng hàng hoá cần xoá.")
b.para(
    "2. Hộp «Xác nhận xóa hàng hóa» hiện ra, báo rằng xoá hàng sẽ xoá toàn bộ dòng khách hàng "
    "của hàng đó.")
b.para("3. Bấm «Xác nhận» để xoá, hoặc «Hủy» để giữ nguyên.")
b.para("Sau khi xoá, cột STT được đánh lại từ 1.")

b.h2("4. Khối File đính kèm (PDF)")
b.para(
    "Khi TẠO MỚI, khối này có dấu sao đỏ — bắt buộc đính kèm ít nhất một file PDF. Cách thêm:")
b.para("1. Cuộn xuống cuối trang tới khối «FILE ĐÍNH KÈM (PDF)».")
b.para("2. Bấm ô «Thêm file» (ô viền đứt nét, có dấu cộng).")
b.para("3. Chọn một hoặc nhiều file PDF từ máy rồi bấm Open.")
b.para(
    "Mỗi file được thêm hiện thành một thẻ có biểu tượng PDF đỏ, tên file và dấu × để bỏ. File "
    "CHƯA được tải lên lúc này — chỉ gửi đi khi bấm nút Lưu.")
b.para("Hệ thống kiểm tra file ngay tại bước chọn, không chờ tới lúc lưu:")
b.bullet(
    "Chọn file không phải PDF (ví dụ .xlsx): file không được thêm, hiện dòng chữ đỏ dưới khối "
    "«File \"tên-file\" không phải PDF».")
b.bullet(
    "Chọn file mang đuôi .pdf nhưng nội dung hỏng (thường gặp với file tải về lỗi từ cổng hoá "
    "đơn): hiện dòng chữ đỏ «File \"tên-file\" không phải PDF hợp lệ (file hỏng hoặc tải về "
    "lỗi) — hãy tải lại file».")
b.image("23-form-da-nhap-day-du.png",
        "Form Tạo mới đã nhập đầy đủ: hàng hoá, dòng khách hàng và file đính kèm")

b.h2("5. Lưu phiếu")
b.para("Cuối trang có ba nút, luôn cố định ở đáy màn hình:")
b.table([
    ["Nút", "Có hỏi xác nhận?", "Kết quả"],
    ["Lưu nháp", "Không",
     "Lưu phiếu ở trạng thái «Đang tạo». Thông báo: «Yêu cầu của bạn đã được lưu. Bạn cần gửi "
     "để yêu cầu được xử lý». Hệ thống quay về màn danh sách. Phiếu chỉ mình nhìn thấy, KHÔNG "
     "gửi thông báo cho ai."],
    ["Lưu và gửi duyệt", "Có",
     "Mở hộp «Xác nhận lưu và gửi duyệt» hỏi «Bạn đồng ý lưu và duyệt?». Bấm «Xác nhận» thì "
     "phiếu lưu ở trạng thái «Chờ duyệt», thông báo «Yêu cầu của bạn đã được gửi», hệ thống "
     "quay về danh sách và gửi thông báo cho những người có quyền Kế toán kho cùng công ty."],
    ["Quay lại", "Có (nếu đã nhập dở)",
     "Về màn danh sách. Nếu đã nhập dở mà chưa lưu, hiện hộp «Thông tin chưa lưu»."],
])
b.image("12-xac-nhan-gui-duyet.png", "Hộp Xác nhận lưu và gửi duyệt")
b.para(
    "Nếu còn ô chưa hợp lệ, hệ thống không lưu mà cuộn tới ô lỗi đầu tiên và hiện lỗi đỏ ngay "
    "dưới từng ô. Cửa sổ không đóng, mọi dữ liệu đã nhập vẫn còn.")
b.image("13-loi-validate.png",
        "Lỗi hiển thị ngay dưới từng ô của dòng khách hàng khi bấm Lưu")
b.image("14-loi-file-dinh-kem.png",
        "Lỗi «Bắt buộc phải nhập» dưới khối File đính kèm")
b.table([
    ["Trường hợp", "Thông báo lỗi"],
    ["Chưa thêm hàng hoá nào", "Bắt buộc phải có ít nhất 1 hàng hóa"],
    ["Chưa chọn đơn vị tính", "Bắt buộc chọn"],
    ["Chưa chọn khách hàng", "Bắt buộc chọn"],
    ["Số lượng để trống hoặc bằng 0", "Không được nhỏ hơn 1"],
    ["Số lượng vượt 999.999.999", "Tối đa 999999999"],
    ["Chưa chọn ngày cần", "Bắt buộc chọn"],
    ["Ngày cần là hôm nay hoặc đã qua", "Ngày cần hàng phải sau ngày hôm nay"],
    ["Chưa nhập ghi chú của dòng khách hàng", "Bắt buộc nhập"],
    ["Ghi chú (phiếu hoặc dòng) quá 255 ký tự", "Vui lòng nhập tối đa 255 ký tự."],
    ["Chưa đính kèm file khi tạo mới", "Bắt buộc phải nhập"],
    ["File đính kèm không phải PDF", "File đính kèm phải là file PDF"],
    ["Thêm trùng hàng hoá trong phiếu", "Hàng hóa bị trùng trong phiếu"],
])

b.h2("6. Cảnh báo khi rời màn chưa lưu")
b.para(
    "Nếu đã nhập dở mà bấm «Quay lại» hoặc chuyển sang màn khác, hệ thống hiện hộp «Thông tin "
    "chưa lưu» với câu hỏi «Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?».")
b.image("11-canh-bao-chua-luu.png", "Hộp cảnh báo Thông tin chưa lưu")
b.bullet("Bấm «Ở lại» để tiếp tục nhập, dữ liệu còn nguyên.")
b.bullet("Bấm «Thoát» để rời màn — toàn bộ dữ liệu đang nhập bị mất.")
b.para("Nếu form còn trắng (chưa nhập gì) thì bấm «Quay lại» sẽ về thẳng danh sách, không hỏi.")

b.h2("7. Sau khi lưu")
b.para(
    "Phiếu mới nằm ở dòng đầu danh sách với mã do hệ thống sinh tự động dạng PYCCH kèm 5 chữ "
    "số. Người dùng không nhập được mã và mã đã dùng không bao giờ được cấp lại, kể cả khi "
    "phiếu bị xoá.")
b.image("24-luu-nhap-thanh-cong.png",
        "Danh sách sau khi lưu nháp — phiếu mới ở trạng thái Đang tạo")

# ══════════════════════════════════════════════════════════ PHẦN 5
b.h1("PHẦN 5: SỬA PHIẾU")

b.h2("1. Điều kiện được sửa")
b.para(
    "Chỉ sửa được phiếu thoả ĐỒNG THỜI hai điều kiện: đang ở trạng thái «Đang tạo» VÀ do chính "
    "mình lập. Thiếu một trong hai thì nút «Sửa» không hiện. Gõ thẳng đường dẫn màn Sửa lên "
    "thanh địa chỉ cũng bị chặn, hệ thống báo «Chỉ sửa được phiếu Đang tạo do chính bạn lập» và "
    "đưa về danh sách.")

b.h2("2. Mở màn Sửa")
b.para("Có hai đường vào:")
b.bullet("Từ danh sách: bấm nút Sửa (biểu tượng bút chì) trên dòng phiếu.")
b.bullet("Từ màn chi tiết: bấm nút «Sửa» ở thanh nút cuối trang.")
b.image("26-sua-phieu.png", "Màn Sửa phiếu yêu cầu chuyển hàng")

b.h2("3. Khác biệt so với màn Tạo mới")
b.table([
    ["Điểm", "Màn Tạo mới", "Màn Sửa"],
    ["Tiêu đề", "Thêm phiếu yêu cầu chuyển hàng", "Sửa phiếu yêu cầu chuyển hàng"],
    ["Ngày lập", "Ngày hôm nay", "Ngày giờ lập phiếu gốc — không đổi theo lần sửa"],
    ["Người lập", "Người đang đăng nhập", "Người lập phiếu gốc — không đổi sang người sửa"],
    ["File đính kèm", "Bắt buộc (có dấu sao đỏ)",
     "Không bắt buộc chọn thêm (không có dấu sao) — file cũ vẫn giữ nguyên"],
    ["Ngày cần đã qua", "Không nhập được", "Dòng cũ giữ nguyên ngày cũ vẫn lưu được — xem mục 5"],
])

b.h2("4. Thêm và xoá file đính kèm khi sửa")
b.para("Thêm file mới: làm y như màn Tạo mới. File mới được NỐI THÊM vào danh sách, không ghi "
       "đè file cũ. Sau khi lưu, phiếu có đủ cả file cũ lẫn file mới.")
b.para("Xoá file đã lưu:")
b.para("1. Bấm dấu × ở góc trên bên phải thẻ file cần xoá.")
b.para("2. Hộp «Xác nhận xóa file» hiện ra, ghi rõ tên file và câu «File sẽ bị xóa vĩnh viễn».")
b.image("27-xac-nhan-xoa-file.png", "Hộp Xác nhận xóa file đính kèm")
b.para("3. Bấm «Xác nhận» — hệ thống báo «Xóa file thành công» và thẻ file biến mất.")
b.para(
    "LƯU Ý QUAN TRỌNG: xoá file đã lưu có hiệu lực NGAY LẬP TỨC và vĩnh viễn, không chờ bấm nút "
    "Lưu. Rời màn mà không lưu phiếu thì file vẫn đã mất. Muốn giữ file thì bấm «Hủy» ở hộp xác "
    "nhận.")

b.h2("5. Quy tắc Ngày cần khi sửa phiếu cũ")
b.para(
    "Ngày cần bắt buộc phải lớn hơn ngày hôm nay khi thêm mới. Riêng khi SỬA phiếu cũ, quy tắc "
    "được nới:")
b.bullet(
    "Dòng khách hàng cũ GIỮ NGUYÊN ngày cần cũ — kể cả ngày đã qua — thì vẫn lưu được bình "
    "thường. Nhờ vậy phiếu nháp để lâu vẫn sửa được các phần khác.")
b.bullet(
    "Dòng khách hàng mới thêm, hoặc dòng cũ vừa ĐỔI ngày cần, thì bị kiểm tra như bình thường: "
    "ngày phải lớn hơn hôm nay, nếu không sẽ hiện lỗi «Ngày cần hàng phải sau ngày hôm nay».")

b.h2("6. Lưu phiếu sau khi sửa")
b.para("Thanh nút cuối trang giống hệt màn Tạo mới:")
b.bullet(
    "«Lưu nháp»: giữ phiếu ở trạng thái «Đang tạo», thông báo «Yêu cầu của bạn đã được lưu. Bạn "
    "cần gửi để yêu cầu được xử lý». Cột «Người cập nhật» và «Ngày cập nhật» trên danh sách đổi "
    "theo người vừa sửa.")
b.bullet(
    "«Lưu và gửi duyệt»: hỏi xác nhận rồi chuyển phiếu sang «Chờ duyệt», thông báo «Yêu cầu của "
    "bạn đã được gửi» và gửi thông báo cho Kế toán kho cùng công ty. Phiếu lập tức mất nút Sửa "
    "và Xóa.")
b.bullet("«Quay lại»: về danh sách, có hỏi nếu đang sửa dở.")

# ══════════════════════════════════════════════════════════ PHẦN 6
b.h1("PHẦN 6: XEM CHI TIẾT PHIẾU")

b.h2("1. Mở màn chi tiết")
b.para("Bấm vào mã yêu cầu (chữ xanh gạch chân) ở cột «Mã yêu cầu» của dòng phiếu.")
b.image("15-chi-tiet.png",
        "Màn chi tiết phiếu đang Chờ duyệt, xem bằng tài khoản có quyền Kế toán kho")

b.h2("2. Nội dung màn chi tiết")
b.para(
    "Tiêu đề màn ghi «Chi tiết phiếu yêu cầu chuyển hàng · mã phiếu», góc phải là nhãn trạng "
    "thái. Toàn bộ thông tin ở chế độ chỉ đọc.")
b.table([
    ["Khối", "Nội dung"],
    ["Thông tin chung",
     "Mã yêu cầu, Ngày lập, Người lập, Người tiếp nhận (hiện kèm ngày tiếp nhận, dạng «Họ tên · "
     "ngày giờ»), Ghi chú. Ô không có dữ liệu hiện dấu gạch ngang."],
    ["File đính kèm",
     "Các thẻ file PDF. Bấm vào tên file để mở ở tab mới. Không có nút xoá file ở màn này. "
     "Phiếu không có file thì hiện dòng «Không có file đính kèm.»"],
    ["Danh sách hàng hóa",
     "Bảng cha có các cột STT, Hàng hóa, ĐVT, Giá niêm yết, SL cần. Ngay dưới mỗi dòng hàng là "
     "bảng con các dòng khách hàng với cột Khách hàng, SL cần, Ngày cần, Ghi chú."],
    ["Ghi chú duyệt",
     "Chỉ hiện khi phiếu đã có lý do từ chối (hiển thị chỉ đọc), hoặc khi người xem được phép "
     "Không duyệt (hiển thị ô nhập kèm dấu sao đỏ)."],
])
b.para(
    "Cột «Được nhận» trong bảng con CHỈ xuất hiện khi phiếu đã ở trạng thái «Đã phân bổ». Các "
    "trạng thái khác không có cột này.")

b.h2("3. Thanh nút cuối màn chi tiết")
b.para(
    "Các nút hiện theo trạng thái phiếu và quyền của người xem, theo thứ tự cố định: Sửa · In · "
    "Không duyệt · Tổng hợp · Quay lại.")
b.table([
    ["Nút", "Điều kiện hiện"],
    ["Sửa", "Phiếu ở trạng thái «Đang tạo» và do chính mình lập."],
    ["In", "Luôn hiện với mọi người xem được phiếu."],
    ["Không duyệt", "Phiếu ở trạng thái «Chờ duyệt», người xem có quyền Kế toán kho (hoặc là "
     "quản trị hệ thống) VÀ cùng công ty với phiếu."],
    ["Tổng hợp", "Cùng điều kiện với nút «Không duyệt»."],
    ["Quay lại", "Luôn hiện."],
])
b.image("28-chi-tiet-phieu-nhap.png",
        "Màn chi tiết phiếu nháp của chính mình — chỉ có Sửa, In, Quay lại")

# ══════════════════════════════════════════════════════════ PHẦN 7
b.h1("PHẦN 7: KHÔNG DUYỆT VÀ TỔNG HỢP (DÀNH CHO KẾ TOÁN KHO)")

b.h2("1. Ai làm được")
b.para(
    "Hai thao tác trong phần này chỉ dành cho người có quyền «Kế toán kho» (hoặc vai trò quản "
    "trị hệ thống), và phải thoả cả hai điều kiện:")
b.bullet("Phiếu đang ở trạng thái «Chờ duyệt».")
b.bullet("Phiếu thuộc CÙNG CÔNG TY với người đang xem.")
b.para(
    "Thiếu một trong hai điều kiện thì hai nút không hiện và khối «Ghi chú duyệt» cũng không có "
    "ô nhập. Người khác công ty — kể cả quản trị hệ thống — chỉ đọc được nội dung phiếu.")

b.h2("2. Không duyệt phiếu")
b.para("1. Mở màn chi tiết của phiếu đang ở trạng thái «Chờ duyệt».")
b.para(
    "2. Cuộn xuống khối «GHI CHÚ DUYỆT» (có dấu sao đỏ), nhập lý do từ chối vào ô. Ô này có "
    "dòng gợi ý «Nhập ghi chú duyệt (bắt buộc khi Không duyệt)».")
b.para("3. Bấm nút «Không duyệt» (màu đỏ) ở thanh nút cuối trang.")
b.para(
    "4. Hộp «Xác nhận không duyệt» hiện ra, ghi rõ mã phiếu và câu «Phiếu sẽ chuyển về trạng "
    "thái Đang tạo để người lập sửa lại».")
b.image("17-xac-nhan-khong-duyet.png", "Hộp Xác nhận không duyệt")
b.para("5. Bấm «Không duyệt» trong hộp để xác nhận, hoặc «Hủy» để dừng lại.")
b.para("Kết quả sau khi xác nhận:")
b.bullet("Thông báo «Đã từ chối yêu cầu chuyển hàng».")
b.bullet("Phiếu chuyển về trạng thái «Đang tạo».")
b.bullet("Ô «Người tiếp nhận» ghi tên người vừa từ chối, «Ngày tiếp nhận» ghi thời điểm bấm.")
b.bullet("Lý do từ chối được lưu vào khối «Ghi chú duyệt» của phiếu.")
b.bullet(
    "Người lập phiếu nhận thông báo trên chuông: «Họ tên người từ chối vừa từ chối yêu cầu "
    "chuyển hàng: mã phiếu». Bấm vào thông báo mở đúng màn chi tiết phiếu.")
b.para(
    "LƯU Ý: «Không duyệt» KHÔNG phải huỷ phiếu. Phiếu quay về nháp để người lập sửa và gửi lại. "
    "Ghi chú duyệt của lần từ chối trước vẫn được giữ trên phiếu sau khi gửi lại.")
b.para("Nếu bấm «Không duyệt» khi ô ghi chú còn trống:")
b.bullet("Hộp xác nhận KHÔNG mở.")
b.bullet("Ô «Ghi chú duyệt» viền đỏ, bên dưới hiện chữ đỏ «Vui lòng nhập ghi chú duyệt».")
b.bullet("Gõ nội dung vào ô thì lỗi đỏ tự biến mất.")
b.image("16-loi-ghi-chu-duyet.png",
        "Lỗi «Vui lòng nhập ghi chú duyệt» khi bấm Không duyệt lúc ô còn trống")

b.h2("3. Tổng hợp phiếu sang màn xuất hàng")
b.para(
    "Nút «Tổng hợp» dùng khi kế toán kho chấp nhận phiếu và muốn gom vào lệnh xuất hàng. Bấm "
    "nút này (ở thanh nút cuối màn chi tiết, hoặc nút dấu tích kép trên dòng danh sách), hệ "
    "thống MỞ TAB MỚI sang màn lập phiếu đề nghị xuất hàng của cổng cũ, mang sẵn phiếu đang xem.")
b.para(
    "Tab đang xem giữ nguyên màn chi tiết và phiếu CHƯA đổi trạng thái. Trạng thái chỉ đổi khi "
    "bộ phận kho hoàn tất thao tác của họ ở màn bên kia.")

b.h2("4. Thông báo khi có phiếu mới gửi duyệt")
b.para(
    "Khi có người lập phiếu và bấm «Lưu và gửi duyệt», mọi người có quyền «Kế toán kho» thuộc "
    "CÙNG CÔNG TY với phiếu nhận được thông báo trên chuông với nội dung «Họ tên người lập vừa "
    "tạo yêu cầu chuyển hàng: mã phiếu». Bấm vào thông báo mở đúng màn chi tiết phiếu.")
b.para(
    "Phiếu chỉ «Lưu nháp» thì KHÔNG gửi thông báo cho ai và cũng không ai khác nhìn thấy.")

# ══════════════════════════════════════════════════════════ PHẦN 8
b.h1("PHẦN 8: XOÁ PHIẾU")

b.h2("1. Điều kiện được xoá")
b.para(
    "Giống điều kiện sửa: chỉ xoá được phiếu ở trạng thái «Đang tạo» DO CHÍNH MÌNH lập. Phiếu "
    "đã gửi duyệt hoặc phiếu của người khác đều không có nút Xóa, và cũng không xoá được bằng "
    "cách gõ đường dẫn.")

b.h2("2. Các bước xoá")
b.para("1. Trên danh sách, tìm dòng phiếu cần xoá (trạng thái «Đang tạo», Người tạo là mình).")
b.para("2. Bấm nút Xóa (biểu tượng thùng rác màu đỏ) ở cột «Hành động».")
b.para(
    "3. Hộp «Xác nhận xóa» hiện ra với câu hỏi «Bạn có chắc muốn xóa phiếu yêu cầu chuyển hàng "
    "'mã phiếu'?».")
b.image("29-xac-nhan-xoa.png", "Hộp Xác nhận xóa phiếu")
b.para("4. Bấm «Xóa» để xoá, hoặc «Hủy» để giữ lại.")
b.para("Kết quả: thông báo «Xóa thành công», dòng biến mất khỏi danh sách và tổng số phiếu giảm "
       "đúng 1.")
b.image("30-xoa-thanh-cong.png", "Danh sách sau khi xoá phiếu")

b.h2("3. Những gì bị xoá theo")
b.para(
    "Xoá phiếu sẽ xoá luôn toàn bộ dòng hàng hoá và dòng khách hàng của phiếu. Đây là xoá thật, "
    "không phải chuyển vào thùng rác — không khôi phục lại được. Mã phiếu đã dùng cũng không "
    "được cấp lại cho phiếu mới.")

b.h2("4. Trường hợp phiếu vừa bị người khác đổi trạng thái")
b.para(
    "Nếu bấm Xóa trên một dòng mà phiếu vừa được đổi trạng thái ở nơi khác, hệ thống từ chối và "
    "báo «Chỉ xóa được phiếu Đang tạo do chính bạn lập», đồng thời TỰ nạp lại danh sách cho "
    "khớp hiện trạng.")

# ══════════════════════════════════════════════════════════ PHẦN 9
b.h1("PHẦN 9: IN PHIẾU")

b.h2("1. Cách in")
b.para("Có hai đường:")
b.bullet("Từ danh sách: bấm nút In (biểu tượng máy in) ở cột «Hành động».")
b.bullet("Từ màn chi tiết: bấm nút «In» ở thanh nút cuối trang.")
b.para(
    "Cả hai đều mở TAB MỚI hiển thị bản in. Ở tab đó, bấm nút «In» góc trên bên phải để mở hộp "
    "thoại in của trình duyệt.")
b.image("18-man-in.png", "Bản in phiếu yêu cầu chuyển hàng")

b.h2("2. Nội dung bản in")
b.table([
    ["Vị trí", "Nội dung"],
    ["Đầu trang", "Ảnh tiêu đề thư của công ty (logo, tên công ty, địa chỉ, điện thoại, email, "
     "website), chiếm hết chiều ngang trang."],
    ["Tiêu đề", "«PHIẾU YÊU CẦU CHUYỂN HÀNG», dưới là dòng «No: mã phiếu»."],
    ["Thông tin đầu phiếu", "Ngày yêu cầu, Người yêu cầu và Ghi chú."],
    ["Bảng nội dung", "Cột STT, Hàng hóa (tên và mã), ĐVT, SL; nhóm cột «Chi tiết» gồm Khách "
     "hàng, SL, Ngày cần, Ghi chú."],
    ["Cuối trang", "Hai ô ký: «Người lập phiếu» (có sẵn tên người lập bên dưới) và "
     "«Giám đốc công ty»."],
])
b.para("Bản in KHÔNG có cột «Giá niêm yết» — giá chỉ để tham khảo lúc lập phiếu.")

b.h2("3. Tiêu đề thư lấy theo công ty nào")
b.para(
    "Ảnh tiêu đề thư đầu trang lấy theo CÔNG TY GHI TRÊN PHIẾU, không phải công ty của người "
    "đang in và cũng không phải công ty của người tạo phiếu. Nhờ vậy khi kế toán công ty A in "
    "phiếu của công ty B thì bản in vẫn mang tiêu đề thư của công ty B.")

b.h2("4. Ai in được")
b.para(
    "Ai xem được phiếu thì in được phiếu — không cần quyền riêng. Người không xem được phiếu mà "
    "gõ thẳng đường dẫn màn in sẽ bị từ chối, hệ thống báo không có quyền xem phiếu này.")
b.para("In phiếu không làm thay đổi trạng thái, người cập nhật hay lịch sử của phiếu.")

# ══════════════════════════════════════════════════════════ PHẦN 10
b.h1("PHẦN 10: XUẤT EXCEL DANH SÁCH")

b.h2("1. Các bước")
b.para("1. Đặt các điều kiện lọc mong muốn trên màn danh sách (nếu cần).")
b.para("2. Bấm nút «Xuất Excel» (biểu tượng bảng tính, viền xanh lá) ở góc phải khối lưới.")
b.para("3. Cửa sổ «Chọn trường xuất file» mở ra với 6 trường được chọn sẵn.")
b.image("04-xuat-excel.png", "Cửa sổ Chọn trường xuất file")
b.para(
    "4. Bỏ chọn hoặc chọn lại các trường theo nhu cầu. Thứ tự cột trong file chạy theo ĐÚNG thứ "
    "tự bạn chọn — muốn đổi vị trí thì bỏ chọn rồi chọn lại theo trình tự mong muốn.")
b.para("5. Bấm «Xuất file» để tải về, hoặc «Đóng» để huỷ.")

b.h2("2. Các trường xuất được")
b.table([
    ["Trường", "Nội dung"],
    ["Mã yêu cầu", "Mã phiếu dạng PYCCH kèm 5 chữ số."],
    ["Người tiếp nhận", "Người của kho đã xử lý phiếu; chưa ai xử lý thì để trống."],
    ["Ngày tiếp nhận", "Ngày tiếp nhận, chỉ ngày/tháng/năm (không kèm giờ)."],
    ["Trạng thái", "Tên trạng thái của phiếu."],
    ["Người tạo", "Người lập phiếu."],
    ["Ngày tạo", "Ngày lập phiếu, chỉ ngày/tháng/năm (không kèm giờ)."],
])
b.para("Hai nút phụ trong cửa sổ: «Chọn tất cả» tích lại đủ 6 trường, «Bỏ chọn hết» xoá hết lựa "
       "chọn. Dòng «Đang chọn n/6 trường» cho biết số trường đang chọn.")

b.h2("3. Phạm vi dữ liệu trong file")
b.bullet(
    "File chứa TOÀN BỘ phiếu khớp bộ lọc đang áp dụng, không chỉ các dòng đang hiển thị trên "
    "trang. Đang xem trang 1 với 10 dòng mà bộ lọc ra 2.500 phiếu thì file có đủ 2.500 dòng.")
b.bullet(
    "File không bao giờ vượt phạm vi quyền: người chỉ thấy 13 phiếu trên lưới thì file cũng chỉ "
    "có 13 dòng.")
b.bullet(
    "Nếu có đặt điều kiện ngày tạo, phía trên bảng trong file có thêm dòng tiêu đề dạng «Từ "
    "ngày ... đến ngày ...» (hoặc chỉ một vế nếu chỉ đặt một mốc).")
b.para("Tên file tải về: danh_sach_yeu_cau_chuyen_hang.xlsx. Sau khi tải xong, hệ thống báo "
       "«Xuất Excel thành công».")

# ══════════════════════════════════════════════════════════ PHẦN 11
b.h1("PHẦN 11: LỊCH SỬ THAY ĐỔI")

b.h2("1. Cách xem")
b.para(
    "Bấm nút Lịch sử (biểu tượng đồng hồ quay ngược) ở cột «Hành động» của dòng phiếu — với "
    "phiếu nháp thì nút này nằm trong menu ba chấm. Nút Lịch sử luôn hiện với mọi phiếu mà "
    "người dùng nhìn thấy, không cần quyền riêng.")
b.image("19-lich-su.png", "Popup Lịch sử thay đổi của một phiếu")

b.h2("2. Nội dung popup")
b.para(
    "Popup có tiêu đề «Lịch sử thay đổi» và phụ đề «Phiếu yêu cầu: mã phiếu». Bên dưới là các "
    "mốc thời gian xếp theo thứ tự, mỗi mốc gồm:")
b.bullet("Ngày giờ xảy ra thay đổi.")
b.bullet("Loại thao tác: Tạo mới, chỉnh sửa, hoặc thay đổi trạng thái.")
b.bullet("Dòng «Người thực hiện: Họ tên — Phòng ban».")
b.bullet(
    "Với thao tác chỉnh sửa: liệt kê trường bị đổi cùng giá trị cũ và giá trị mới. Riêng thay "
    "đổi trạng thái được ghi bằng TÊN trạng thái (ví dụ «Đang tạo» → «Chờ duyệt»).")
b.para(
    "Nút «Bộ lọc» ở góc phải cho phép lọc theo nhóm thao tác. Bấm «Đóng» để trở về danh sách — "
    "danh sách giữ nguyên trang và bộ lọc đang xem.")

# ══════════════════════════════════════════════════════════ PHẦN 12
b.h1("PHẦN 12: HƯỚNG DẪN THEO TỪNG VAI TRÒ")

b.h2("1. Người kinh doanh không có quyền xem nào")
b.para("Nhìn thấy: chỉ phiếu do chính mình lập, ở mọi trạng thái.")
b.para("Làm được:")
b.bullet("Lập phiếu mới (Tạo mới), lưu nháp hoặc gửi duyệt.")
b.bullet("Sửa và xoá phiếu nháp của chính mình.")
b.bullet("Xem chi tiết, in, xuất Excel, xem lịch sử các phiếu của mình.")
b.para("Không làm được: không thấy phiếu của người khác; không có nút «Không duyệt» và «Tổng "
       "hợp» trên bất kỳ phiếu nào.")

b.h2("2. Người phụ trách bộ phận (quyền Xem yêu cầu chuyển hàng theo bộ phận)")
b.para(
    "Nhìn thấy: phiếu thuộc các bộ phận được giao quản lý trong công ty mình, CỘNG THÊM mọi "
    "phiếu do chính mình lập (kể cả phiếu thuộc bộ phận khác). Nháp của người khác vẫn bị ẩn.")
b.para("Làm được: mọi thao tác như mục 1, trên phạm vi dữ liệu rộng hơn.")

b.h2("3. Người phụ trách phòng ban (quyền Xem yêu cầu chuyển hàng theo phòng ban)")
b.para(
    "Nhìn thấy: phiếu thuộc các phòng ban được giao quản lý trong công ty mình, cộng thêm mọi "
    "phiếu do chính mình lập. Nháp của người khác vẫn bị ẩn.")
b.para("Làm được: mọi thao tác như mục 1, trên phạm vi phòng ban.")

b.h2("4. Cấp công ty (quyền Xem yêu cầu chuyển hàng theo công ty)")
b.para(
    "Nhìn thấy: toàn bộ phiếu thuộc công ty của mình, không phân biệt phòng ban hay bộ phận. "
    "Nháp của người khác vẫn bị ẩn.")
b.para(
    "Lưu ý: người chưa được gắn hồ sơ nhân viên (không xác định được thuộc công ty nào) mà chỉ "
    "có quyền này sẽ thấy danh sách RỖNG — cần liên hệ quản trị để bổ sung thông tin công ty.")

b.h2("5. Cấp tổng công ty (quyền Xem yêu cầu chuyển hàng theo tổng công ty)")
b.para("Nhìn thấy: phiếu của mọi công ty trong tập đoàn. Nháp của người khác vẫn bị ẩn.")
b.para(
    "Vai trò quản trị hệ thống có phạm vi xem tương đương, dù không được gán quyền này.")

b.h2("6. Kế toán kho (quyền Kế toán kho)")
b.para(
    "Nhìn thấy: ngoài phạm vi do các quyền xem quyết định, quyền này còn cho phép mở màn chi "
    "tiết phiếu của người khác trong CÙNG CÔNG TY.")
b.para("Làm được thêm, với phiếu «Chờ duyệt» cùng công ty:")
b.bullet("Nhập «Ghi chú duyệt» và bấm «Không duyệt» để trả phiếu về cho người lập sửa lại.")
b.bullet("Bấm «Tổng hợp» để mở màn lập phiếu đề nghị xuất hàng ở tab mới.")
b.para("Nhận thông báo trên chuông mỗi khi có phiếu mới được gửi duyệt trong công ty mình.")
b.para(
    "Không làm được: không sửa, không xoá phiếu của người khác — kể cả phiếu nháp. Với phiếu "
    "khác công ty thì không có hai nút trên, kể cả khi là quản trị hệ thống.")

# ══════════════════════════════════════════════════════════ PHẦN 13
b.h1("PHẦN 13: CÁC LỖI THƯỜNG GẶP VÀ CÁCH XỬ LÝ")
b.table([
    ["Hiện tượng", "Nguyên nhân", "Cách xử lý"],
    ["Vào màn thấy thiếu phiếu so với lần trước",
     "Bộ lọc của lần trước vẫn còn (hệ thống ghi nhớ 10 phút).",
     "Bấm nút «Làm mới» để xoá điều kiện lọc rồi xem lại."],
    ["Gõ vào ô tìm nhanh mà danh sách không đổi",
     "Ô tìm nhanh không tự tìm khi gõ.",
     "Bấm nút «Tìm kiếm» hoặc nhấn Enter."],
    ["Bấm sắp xếp cột «Ngày cập nhật» mà thứ tự không đổi",
     "Cột này không hỗ trợ sắp xếp; danh sách quay về thứ tự mặc định.",
     "Dùng cột «Ngày tạo» hoặc «Ngày tiếp nhận» để sắp xếp."],
    ["Lọc trạng thái «Đang tạo» mà chỉ thấy vài phiếu của mình",
     "Nháp của người khác luôn bị ẩn, kể cả với quyền xem toàn tổng công ty.",
     "Đây là quy tắc cố định, không phải lỗi."],
    ["Không thấy nút Sửa / Xóa trên phiếu của mình",
     "Phiếu đã rời trạng thái «Đang tạo» (đã gửi duyệt hoặc kho đã xử lý).",
     "Nhờ người có quyền Kế toán kho bấm «Không duyệt» để đưa phiếu về «Đang tạo»."],
    ["Không thấy nút «Không duyệt» dù có quyền Kế toán kho",
     "Phiếu khác công ty với người xem, hoặc phiếu không ở trạng thái «Chờ duyệt».",
     "Kiểm tra lại trạng thái và công ty của phiếu."],
    ["Bấm «Không duyệt» mà không mở hộp xác nhận",
     "Ô «Ghi chú duyệt» còn trống.",
     "Nhập lý do vào ô rồi bấm lại."],
    ["Chọn file PDF mà hệ thống báo không hợp lệ",
     "File mang đuôi .pdf nhưng nội dung hỏng (thường do tải về lỗi).",
     "Mở thử file trên máy; tải lại file từ nguồn rồi chọn lại."],
    ["Xoá nhầm file đính kèm",
     "Xoá file đã lưu có hiệu lực ngay và vĩnh viễn, không chờ bấm Lưu.",
     "Không khôi phục được — phải chọn lại file từ máy và lưu phiếu."],
    ["Sửa phiếu nháp cũ bị báo «Ngày cần hàng phải sau ngày hôm nay»",
     "Đã đổi ngày cần của một dòng cũ sang ngày quá khứ khác.",
     "Chọn ngày lớn hơn hôm nay, hoặc để nguyên ngày cũ không đụng tới."],
    ["Số lượng nhập vượt tồn mà hệ thống vẫn cho lưu",
     "SL tồn chỉ để tham khảo, hệ thống không chặn.",
     "Người lập tự kiểm tra trước khi gửi duyệt."],
    ["Không mở được phiếu của đồng nghiệp",
     "Không phải người lập, không có quyền Kế toán kho cùng công ty, hoặc phiếu khác công ty.",
     "Liên hệ quản trị để được cấp quyền xem phù hợp."],
])

b.finish()
