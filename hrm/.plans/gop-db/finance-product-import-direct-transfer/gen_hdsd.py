# -*- coding: utf-8 -*-
"""Sinh HDSD Word cho man **Phieu chuyen hang nhap thang** ban HRM (phan he Tai chinh).

Chay:  python gen_hdsd.py
Output: "HDSD_Phieu chuyen hang nhap thang.docx" cung thu muc.
Anh nguon: hdsd_product_import_direct_transfer_shots/ (CHI DE LOCAL, khong commit).
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", ".claude", "skills",
                                "hdsd-documenter", "assets"))
from hdsd_engine import HdsdBuilder  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, "hdsd_product_import_direct_transfer_shots")
OUTPUT = os.path.join(HERE, "HDSD_Phieu chuyen hang nhap thang.docx")

b = HdsdBuilder(
    output=OUTPUT,
    shots_dir=SHOTS,
    cover_title="(Màn hình: Phiếu chuyển hàng nhập thẳng)",
    doc_title="HDSD - Phiếu chuyển hàng nhập thẳng",
)

# =====================================================================================
b.h1("TỔNG QUAN")

b.h2("1. Thuật ngữ sử dụng trong tài liệu")
b.table([
    ["Thuật ngữ", "Giải thích"],
    ["Hàng nhập thẳng",
     "Hàng được nhà cung cấp giao thẳng cho nhân viên, không nhập qua kho. Vì vậy tồn của loại "
     "hàng này được ghi nhận theo từng NHÂN VIÊN chứ không theo kho."],
    ["Phiếu chuyển hàng nhập thẳng",
     "Chứng từ để nhân viên đang giữ hàng nhập thẳng chuyển số hàng đó sang một nhân viên khác "
     "cùng công ty."],
    ["Người lập phiếu", "Người tạo phiếu, cũng chính là người đang giữ hàng và sẽ bị trừ tồn."],
    ["Người nhận", "Nhân viên được nhận hàng; sau khi phiếu được duyệt sẽ có tồn tương ứng."],
    ["Kế toán kho", "Vai trò duyệt hoặc từ chối phiếu."],
    ["ĐVT", "Đơn vị tính của hàng hóa (Cái, Bộ, Thùng…)."],
    ["SL theo ĐV cơ bản",
     "Số lượng quy về đơn vị nhỏ nhất của hàng hóa. Đây là con số hệ thống dùng để trừ tồn."],
    ["Lô tồn",
     "Một lần nhận hàng của nhân viên. Một nhân viên có thể có nhiều lô của cùng một mặt hàng."],
])

b.h2("2. Lịch sử cập nhật tài liệu")
b.table([
    ["Phiên bản", "Ngày", "Nội dung", "Người thực hiện"],
    ["1.0", "28/08/2026", "Ban hành lần đầu cho bản chạy trên hệ thống HRM.", "Tri Lee"],
])

b.h2("3. Giới thiệu chung")
b.para(
    "Màn hình \"Phiếu chuyển hàng nhập thẳng\" dùng để chuyển hàng nhập thẳng đang do một nhân "
    "viên nắm giữ sang một nhân viên khác trong cùng công ty. Do hàng nhập thẳng không nằm trong "
    "kho, việc chuyển giao giữa hai người phải được lập thành phiếu và được Kế toán kho duyệt "
    "thì tồn mới được ghi nhận lại."
)
b.para("Đường dẫn: /finance/product-import-direct-transfers")
b.para(
    "Vị trí trên menu: phân hệ Tài chính, nhóm Điều chuyển, mục \"Phiếu chuyển hàng nhập thẳng\"."
)

b.h3("3.1. Luồng nghiệp vụ")
b.bullet("Người lập phiếu chọn người nhận và các mặt hàng muốn chuyển từ tồn nhập thẳng của mình.")
b.bullet(
    "Người lập có thể Lưu nháp (phiếu ở trạng thái Đang tạo, chưa ai phải xử lý) hoặc Lưu và gửi "
    "duyệt (phiếu chuyển sang Chờ duyệt và Kế toán kho nhận được thông báo)."
)
b.bullet(
    "Kế toán kho cùng công ty mở phiếu và quyết định Duyệt hoặc Từ chối. Khi Từ chối, bắt buộc "
    "nhập lý do."
)
b.bullet(
    "Khi phiếu được Duyệt, hệ thống trừ tồn của người lập theo thứ tự nhận trước dùng trước, ghi "
    "lại biến động của từng lô, rồi tạo tồn mới cho người nhận. Thao tác này KHÔNG hoàn tác được."
)
b.bullet(
    "Phiếu bị Từ chối vẫn thuộc quyền của người lập: có thể sửa lại rồi gửi duyệt lần nữa, hoặc xóa."
)

b.h3("3.2. Các trạng thái của phiếu")
b.table([
    ["Trạng thái", "Ý nghĩa", "Ai thao tác tiếp được"],
    ["Đang tạo", "Bản nháp, chỉ người lập nhìn thấy.", "Người lập: Sửa, Xóa, Gửi duyệt."],
    ["Chờ duyệt", "Đã gửi, đang đợi Kế toán kho xử lý.",
     "Kế toán kho cùng công ty: Duyệt hoặc Từ chối. Không ai sửa/xóa được."],
    ["Đã duyệt", "Tồn đã được chuyển sang người nhận.",
     "Chỉ xem, in, xuất dữ liệu. Không sửa, không xóa, không duyệt lại."],
    ["Không duyệt", "Bị từ chối, có ghi lý do.", "Người lập: Sửa rồi gửi lại, hoặc Xóa."],
])

b.h2("4. Phân quyền và phạm vi dữ liệu")
b.para(
    "Màn hình dùng lại nguyên bộ quyền sẵn có, không phát sinh quyền mới. Bảng dưới đây liệt kê "
    "đầy đủ các quyền liên quan."
)
b.table([
    ["Tên quyền", "Cho phép làm gì", "Nút / khu vực tương ứng"],
    ["Xem phiếu chuyển hàng nhập thẳng theo tổng công ty",
     "Xem phiếu của mọi công ty.", "Danh sách, màn Chi tiết, In, Xuất Excel."],
    ["Xem phiếu chuyển hàng nhập thẳng theo công ty",
     "Xem phiếu cùng công ty với mình.", "Danh sách, màn Chi tiết, In, Xuất Excel."],
    ["Xem phiếu chuyển hàng nhập thẳng theo phòng ban",
     "Xem phiếu thuộc các phòng ban mình quản lý.", "Danh sách, màn Chi tiết, In, Xuất Excel."],
    ["Xem phiếu chuyển hàng nhập thẳng theo bộ phận",
     "Xem phiếu thuộc các bộ phận mình quản lý.", "Danh sách, màn Chi tiết, In, Xuất Excel."],
    ["Kế toán kho",
     "Duyệt hoặc Từ chối phiếu Chờ duyệt của công ty mình; đồng thời nhìn thấy các phiếu Chờ "
     "duyệt đó trên danh sách.",
     "Nút Duyệt và Từ chối ở màn Chi tiết; biểu tượng Duyệt ở cột Hành động."],
])
b.para(
    "Ngoài các quyền trên, mọi người dùng LUÔN nhìn thấy và mở được phiếu do chính mình lập, kể "
    "cả khi không được cấp quyền xem theo cấp nào."
)
b.para(
    "Nếu không có quyền tương ứng, nút sẽ không hiển thị; trường hợp truy cập trực tiếp bằng "
    "đường dẫn, hệ thống báo lỗi không có quyền và đưa về màn danh sách."
)

b.h3("4.1. Người dùng chỉ có quyền xem theo cấp (tổng công ty / công ty / phòng ban / bộ phận)")
b.bullet("Nhìn thấy danh sách phiếu trong đúng phạm vi cấp được cấp quyền, cộng thêm phiếu của chính mình.")
b.bullet("Mở được màn Chi tiết của mọi phiếu nhìn thấy trên danh sách.")
b.bullet("In được phiếu, in được danh sách, xuất được Excel trong phạm vi đó.")
b.bullet("KHÔNG có nút Duyệt, Từ chối. Chỉ có Sửa / Xóa ở phiếu do chính mình lập và phiếu đang ở trạng thái Đang tạo hoặc Không duyệt.")

b.h3("4.2. Người dùng có quyền \"Kế toán kho\"")
b.bullet("Nhìn thấy thêm mọi phiếu đang Chờ duyệt của công ty mình ngay trên danh sách chính, không cần vào mục riêng.")
b.bullet("Mở phiếu Chờ duyệt sẽ thấy nút Duyệt (màu xanh) và Từ chối (màu đỏ) ở cuối màn.")
b.bullet("Chỉ duyệt được phiếu CÙNG CÔNG TY với mình. Phiếu của công ty khác vẫn không có nút Duyệt kể cả khi nhìn thấy nhờ quyền xem theo tổng công ty.")
b.bullet("Không tự sửa hay xóa được phiếu của người khác.")

b.h3("4.3. Người dùng không có quyền nào của màn")
b.bullet("Vẫn vào được màn nhưng chỉ thấy phiếu do chính mình lập.")
b.bullet("Vẫn tạo được phiếu mới và gửi duyệt bình thường.")
b.bullet("Không thấy phiếu của đồng nghiệp, không có nút Duyệt / Từ chối.")

# =====================================================================================
b.h1("PHẦN 1: TRUY CẬP VÀ BỐ CỤC MÀN DANH SÁCH")

b.h2("1.1. Cách vào màn hình")
b.para("Đăng nhập hệ thống, chọn phân hệ Tài chính ở thanh bên trái.")
b.para("Mở nhóm Điều chuyển rồi bấm mục \"Phiếu chuyển hàng nhập thẳng\".")
b.para("Hoặc gõ thẳng đường dẫn /finance/product-import-direct-transfers vào thanh địa chỉ trình duyệt.")
b.image("01-danh-sach.png", "Màn hình danh sách Phiếu chuyển hàng nhập thẳng")

b.h2("1.2. Bố cục màn hình")
b.bullet("Khối trên cùng là \"Bộ lọc danh sách\": ô tìm nhanh, nút Tìm kiếm, nút Làm mới, nút Cài đặt bộ lọc và nút Tìm kiếm nâng cao.")
b.bullet("Khối dưới là bảng dữ liệu, phía trên bảng là hàng nút thao tác của màn.")
b.bullet("Cuối bảng là dòng \"Hiển thị a–b / N\" cho biết đang xem những dòng nào trong tổng số phiếu khớp bộ lọc, kèm ô chọn Số dòng/trang và các nút chuyển trang.")

b.h2("1.3. Các cột của bảng")
b.para(
    "Sáu cột đầu và cột Hành động luôn có mặt. Các cột còn lại có thể bật hoặc tắt ở nút Cấu hình "
    "cột hiển thị (xem mục 2.5)."
)
b.table([
    ["Cột", "Ý nghĩa"],
    ["STT", "Số thứ tự, chạy liên tục qua các trang."],
    ["Số phiếu", "Mã phiếu do hệ thống tự sinh. Bấm vào để mở màn Chi tiết."],
    ["Người nhận", "Nhân viên sẽ nhận hàng."],
    ["Công ty", "Công ty của phiếu."],
    ["Phòng ban", "Phòng ban ghi trên phiếu."],
    ["Ghi chú", "Ghi chú do người lập nhập."],
    ["Người duyệt", "Người đã duyệt hoặc từ chối phiếu; để trống khi chưa ai xử lý."],
    ["Người tạo", "Người lập phiếu."],
    ["Ngày tạo", "Ngày và giờ lập phiếu."],
    ["Người cập nhật", "Người sửa phiếu gần nhất."],
    ["Ngày cập nhật", "Thời điểm sửa gần nhất."],
    ["Trạng thái", "Đang tạo (xám) · Chờ duyệt (vàng) · Đã duyệt (xanh) · Không duyệt (đỏ)."],
    ["Hành động", "Các nút thao tác trên từng dòng."],
])
b.para(
    "Cột STT và Số phiếu luôn dính bên trái, cột Hành động luôn dính bên phải khi cuộn bảng "
    "sang ngang, nên không bị mất dấu dòng đang xem."
)

b.h2("1.4. Các nút trên thanh công cụ của bảng")
b.table([
    ["Nút", "Tác dụng", "Quyền yêu cầu"],
    ["Tạo mới", "Mở màn lập phiếu mới.", "Không yêu cầu quyền riêng."],
    ["In", "Mở bản in danh sách theo đúng bộ lọc đang áp dụng.", "Theo phạm vi quyền xem của người dùng."],
    ["Xuất Excel", "Mở cửa sổ chọn trường rồi tải file danh sách.", "Theo phạm vi quyền xem của người dùng."],
    ["Cấu hình cột hiển thị", "Bật / tắt và sắp xếp các cột của bảng.", "Không yêu cầu quyền riêng."],
])

b.h2("1.5. Thao tác trên từng dòng")
b.para(
    "Cột Hành động hiển thị các nút phù hợp với trạng thái phiếu và quyền của người đang đăng "
    "nhập. Nút không dùng được sẽ được ẨN hẳn chứ không hiện dạng mờ."
)
b.image("06-cot-hanh-dong.png", "Cột Hành động thay đổi theo trạng thái phiếu")
b.table([
    ["Nút", "Biểu tượng", "Khi nào hiện"],
    ["Sửa", "Bút chì", "Phiếu Đang tạo hoặc Không duyệt và do chính mình lập."],
    ["Xóa", "Thùng rác đỏ", "Cùng điều kiện với nút Sửa."],
    ["Duyệt", "Dấu tích trong vòng tròn",
     "Phiếu đang Chờ duyệt và người dùng có quyền Kế toán kho cùng công ty. Bấm vào sẽ MỞ MÀN CHI "
     "TIẾT để xem hàng hóa trước, không duyệt ngay tại danh sách."],
    ["In", "Máy in", "Luôn có."],
    ["Lịch sử", "Đồng hồ quay ngược", "Luôn có."],
])
b.para(
    "Khi một dòng có nhiều nút, các nút phụ được gom vào biểu tượng ba chấm \"Hành động khác\"."
)
b.image("07-menu-hanh-dong-khac.png", "Menu Hành động khác gom nút In và Lịch sử")

b.h2("1.6. Sắp xếp và phân trang")
b.bullet("Hai cột Số phiếu và Ngày tạo có biểu tượng sắp xếp. Bấm lần đầu là tăng dần, bấm lần nữa là giảm dần.")
b.bullet("Thứ tự sắp xếp được giữ nguyên khi chuyển trang và khi đổi bộ lọc.")
b.bullet("Ô \"Số dòng/trang\" cho chọn số dòng hiển thị; đổi số dòng thì hệ thống quay về trang 1.")
b.bullet("Chuyển trang KHÔNG làm mất điều kiện lọc đang áp dụng.")

# =====================================================================================
b.h1("PHẦN 2: TÌM KIẾM VÀ LỌC DỮ LIỆU")

b.h2("2.1. Ô tìm nhanh")
b.para(
    "Ô tìm nhanh nằm ngay dưới tiêu đề khối lọc, có dòng gợi ý \"Tìm theo số phiếu hoặc người "
    "tạo...\". Gõ vào đây và bấm Tìm kiếm (hoặc chờ hệ thống tự tải lại) để lọc nhanh theo số "
    "phiếu hoặc tên người lập. Dòng khớp sát nhất được đưa lên đầu."
)

b.h2("2.2. Bộ lọc nâng cao")
b.para("Bấm nút \"Tìm kiếm nâng cao\" để mở đầy đủ các tiêu chí lọc. Bấm lại để thu gọn.")
b.image("02-bo-loc-nang-cao.png", "Bộ lọc nâng cao với đầy đủ tiêu chí")
b.table([
    ["Tiêu chí", "Kiểu nhập", "Ghi chú"],
    ["Công ty", "Chọn từ danh sách", "Chỉ liệt kê công ty trong phạm vi quyền của người dùng."],
    ["Phòng ban", "Chọn từ danh sách", "Danh sách phụ thuộc công ty đã chọn ở ô trên."],
    ["Số phiếu", "Gõ tay", "Tìm theo một phần của số phiếu cũng được."],
    ["Trạng thái", "Chọn từ danh sách", "Đang tạo · Chờ duyệt · Đã duyệt · Không duyệt."],
    ["Tên/mã hàng hóa", "Gõ tay", "Lọc ra những phiếu có chứa mặt hàng đó trong bảng chi tiết."],
    ["Người nhận", "Chọn từ danh sách", "Lọc theo nhân viên được nhận hàng."],
    ["Người tạo", "Chọn từ danh sách", "Lọc theo người lập phiếu."],
    ["Ngày tạo từ", "Chọn ngày", "Tính theo ngày lập phiếu, bao gồm cả ngày đã chọn."],
    ["Ngày tạo đến", "Chọn ngày", "Tính theo ngày lập phiếu, bao gồm cả ngày đã chọn."],
])
b.para(
    "Màn hình này KHÔNG có ô lọc Bộ phận. Đây là thiết kế cố ý vì phiếu không lưu bộ phận riêng, "
    "lọc theo bộ phận sẽ luôn ra danh sách rỗng."
)
b.para(
    "Các tiêu chí kết hợp với nhau theo kiểu \"và\": chọn càng nhiều ô thì kết quả càng thu hẹp."
)

b.h2("2.3. Nút Làm mới")
b.para(
    "Bấm Làm mới để xóa toàn bộ điều kiện đang lọc, kể cả ô tìm nhanh. Danh sách tự tải lại đầy "
    "đủ theo phạm vi quyền và quay về trang 1."
)

b.h2("2.4. Cài đặt bộ lọc")
b.para(
    "Nút \"Cài đặt bộ lọc\" cho phép chọn những ô lọc muốn hiển thị và kéo thả để đổi thứ tự. "
    "Cấu hình được lưu riêng cho từng người dùng và từng màn hình, giữ nguyên sau khi đăng xuất."
)
b.image("03-cai-dat-bo-loc.png", "Cửa sổ Cài đặt bộ lọc")
b.bullet("Bỏ tick một ô để ẩn ô lọc đó khỏi khối tìm kiếm nâng cao.")
b.bullet("Kéo biểu tượng chấm ở đầu mỗi ô để đổi thứ tự hiển thị.")
b.bullet("Bấm Lưu để áp dụng, Khôi phục mặc định để trả về cấu hình gốc, Đóng để thoát mà không lưu.")
b.para(
    "Nếu không tìm thấy một ô lọc quen dùng, hãy mở cửa sổ này kiểm tra xem ô đó có đang bị tắt "
    "hay không trước khi báo lỗi."
)

b.h2("2.5. Tuỳ chỉnh cột hiển thị")
b.para(
    "Bấm biểu tượng cột ở cuối hàng nút (chú thích khi rê chuột là \"Cấu hình cột hiển thị\") để "
    "mở cửa sổ Tuỳ chỉnh cột."
)
b.image("04-cau-hinh-cot.png", "Cửa sổ Tuỳ chỉnh cột")
b.bullet("Tick hoặc bỏ tick để hiện / ẩn từng cột.")
b.bullet("Kéo biểu tượng ba gạch bên phải mỗi dòng để đổi thứ tự cột.")
b.bullet("Cột STT và Số phiếu có biểu tượng ổ khoá: luôn hiển thị, không tắt được.")
b.bullet("Bấm Lưu để áp dụng. Cấu hình được ghi nhớ theo từng người dùng.")

# =====================================================================================
b.h1("PHẦN 3: LẬP PHIẾU MỚI")

b.h2("3.1. Mở màn lập phiếu")
b.para(
    "Trên màn danh sách, bấm nút \"Tạo mới\". Hệ thống mở màn \"Thêm phiếu chuyển hàng nhập "
    "thẳng\" gồm hai khối: THÔNG TIN CHUNG và CHI TIẾT."
)
b.image("09-form-tao-moi.png", "Màn lập phiếu chuyển hàng nhập thẳng")
b.para(
    "Góc phải khối THÔNG TIN CHUNG hiển thị tên người lập và ngày lập phiếu. Màn lập phiếu chưa "
    "có ô Số phiếu, Trạng thái và Người duyệt — ba thông tin này chỉ xuất hiện ở màn Chi tiết sau "
    "khi phiếu đã được lưu."
)

b.h2("3.2. Các trường của khối Thông tin chung")
b.table([
    ["Trường", "Kiểu nhập", "Bắt buộc", "Giá trị điền sẵn khi tạo mới", "Ghi chú"],
    ["Người nhận", "Chọn từ danh sách nhân viên", "Có", "Để trống",
     "Chỉ liệt kê nhân viên cùng công ty với người lập và KHÔNG có tên của chính người lập."],
    ["Phòng ban", "Ô chỉ đọc", "Không", "Để trống",
     "Tự điền theo người nhận vừa chọn; không sửa tay được."],
    ["Ghi chú", "Gõ tay", "Không", "Để trống", "Tối đa 255 ký tự."],
])

b.h2("3.3. Thêm hàng hóa vào phiếu")
b.para(
    "Bấm nút \"Thêm hàng hóa\" ở góc phải khối CHI TIẾT. Hệ thống mở cửa sổ \"Tồn hàng nhập thẳng "
    "của nhân viên\", chỉ liệt kê những mặt hàng người lập phiếu còn tồn."
)
b.image("10-popup-chon-hang.png", "Cửa sổ chọn hàng từ tồn nhập thẳng của người lập phiếu")
b.bullet("Ô \"Tìm hàng hóa\" cho gõ tên hoặc mã hàng rồi bấm Tìm kiếm; bấm Làm mới để xóa điều kiện tìm.")
b.bullet("Bảng \"Danh sách tồn\" gồm các cột: STT · Mã hàng hóa · Tên hàng hóa · Hãng sản xuất · ĐVT · Số lượng tồn.")
b.bullet("Tick chọn nhiều dòng cùng lúc rồi bấm nút Chọn (con số trong ngoặc là số dòng đang tick).")
b.bullet("Mặt hàng đã có trong phiếu bị khoá tick sẵn, rê chuột hiện chú thích \"Hàng hóa đã có trong phiếu\".")
b.bullet("Nếu người lập phiếu không còn tồn nhập thẳng nào, cửa sổ hiện dòng \"Nhân viên không còn tồn hàng nhập thẳng nào.\"")

b.h2("3.4. Nhập số lượng trên từng dòng hàng")
b.table([
    ["Cột", "Nhập được", "Ý nghĩa"],
    ["Tên hàng", "Không", "Lấy từ mặt hàng đã chọn."],
    ["Mã hàng", "Không", "Lấy từ mặt hàng đã chọn."],
    ["ĐVT", "Có, chọn từ danh sách", "Đổi đơn vị tính thì số lượng và tồn hiện có được tính lại theo hệ số quy đổi."],
    ["Số lượng", "Có, gõ tay", "Số lượng muốn chuyển, tính theo đơn vị đang chọn ở cột ĐVT."],
    ["SL theo ĐV cơ bản", "Không", "Bằng Số lượng nhân hệ số quy đổi; đây là con số dùng để trừ tồn."],
    ["Tồn hiện có", "Không", "Tồn của người lập phiếu, quy về đơn vị đang chọn ở dòng đó."],
])
b.para("Quy tắc nhập số lượng:")
b.bullet("Chỉ nhập chữ số. Dùng dấu phẩy để ngăn cách hàng nghìn và dấu chấm cho phần thập phân, ví dụ 1,200.5.")
b.bullet("Ô chỉ nhận chữ số: gõ chữ hoặc ký tự lạ thì ô bỏ qua luôn, dán chuỗi có lẫn chữ thì chỉ phần số được giữ lại.")
b.bullet("Để trống hoặc nhập 0 thì khi bấm lưu sẽ báo \"Số lượng – Chưa nhập số lượng\" hoặc \"Số lượng – Phải lớn hơn 0\".")
b.bullet(
    "Nhập vượt quá tồn hiện có thì hệ thống GIỮ NGUYÊN con số vừa gõ và báo đỏ \"Chỉ còn … theo "
    "đơn vị đang chọn\". Hệ thống không tự kéo về mức tối đa."
)
b.bullet(
    "Nếu phiếu có nhiều dòng cùng một mặt hàng, hệ thống cộng dồn các dòng đó rồi mới so với tồn. "
    "Tổng vượt tồn là bị chặn, dù từng dòng riêng lẻ vẫn nhỏ hơn tồn."
)
b.bullet("Bấm biểu tượng thùng rác ở cuối dòng để xóa dòng hàng khỏi phiếu.")

b.h2("3.5. Lưu phiếu")
b.table([
    ["Nút", "Kết quả", "Điều kiện"],
    ["Lưu nháp",
     "Phiếu được lưu ở trạng thái Đang tạo, chưa ai phải xử lý. Hệ thống sinh Số phiếu và quay về "
     "màn danh sách.",
     "Chỉ bắt buộc điền Người nhận. Bảng hàng hóa để trống vẫn lưu được."],
    ["Lưu và gửi duyệt",
     "Phiếu chuyển sang trạng thái Chờ duyệt. Những người có quyền Kế toán kho cùng công ty nhận "
     "được thông báo. Hệ thống quay về màn danh sách.",
     "Bắt buộc có Người nhận và ít nhất một dòng hàng hóa hợp lệ."],
    ["Quay lại", "Thoát về màn danh sách.",
     "Nếu đang có dữ liệu chưa lưu, hệ thống hỏi xác nhận trước khi rời trang."],
])
b.para(
    "Khi thiếu thông tin bắt buộc, hệ thống báo lỗi đỏ ngay tại ô bị thiếu, hiện thông báo \"Vui "
    "lòng kiểm tra lại dữ liệu nhập\" và tự cuộn tới ô lỗi đầu tiên. Dữ liệu đã nhập vẫn được giữ "
    "nguyên trên màn hình."
)
b.para(
    "Số phiếu do hệ thống tự sinh theo mẫu <mã công ty>_CHNT_<số thứ tự>, ví dụ TPE_CHNT_906. "
    "Người dùng không nhập và không sửa được số phiếu."
)

# =====================================================================================
b.h1("PHẦN 4: SỬA PHIẾU")

b.para(
    "Chỉ NGƯỜI LẬP PHIẾU mới sửa được, và chỉ khi phiếu đang ở trạng thái Đang tạo hoặc Không "
    "duyệt. Phiếu Chờ duyệt và Đã duyệt không sửa được: nút Sửa sẽ không hiển thị."
)
b.para(
    "Cách vào: bấm biểu tượng bút chì ở cột Hành động trên màn danh sách, hoặc mở màn Chi tiết "
    "rồi bấm nút Sửa ở cuối màn."
)
b.image("13-man-sua.png", "Màn sửa phiếu chuyển hàng nhập thẳng")
b.bullet("Các trường và quy tắc nhập giống hệt màn lập phiếu ở Phần 3.")
b.bullet(
    "Cửa sổ chọn hàng hóa liệt kê tồn của NGƯỜI LẬP PHIẾU (không phải tồn của người đang mở màn "
    "sửa), đúng bằng nguồn mà hệ thống dùng để kiểm tra khi lưu."
)
b.bullet("Hai nút lưu giống màn lập phiếu: Lưu nháp giữ phiếu ở trạng thái nháp, Lưu và gửi duyệt đẩy phiếu sang Chờ duyệt.")
b.bullet("Nếu phiếu vừa bị người khác xóa, hệ thống báo \"Không tìm thấy dữ liệu\" và đưa về màn danh sách.")

# =====================================================================================
b.h1("PHẦN 5: XEM CHI TIẾT PHIẾU")

b.para(
    "Bấm vào Số phiếu trên danh sách để mở màn Chi tiết. Tiêu đề trang có dạng \"Chi tiết phiếu "
    "chuyển hàng nhập thẳng: <số phiếu>\". Toàn bộ ô ở màn này chỉ để đọc."
)
b.image("11-chi-tiet-cho-duyet.png", "Màn chi tiết một phiếu đang Chờ duyệt")
b.bullet("Khối THÔNG TIN CHUNG hiển thị thêm ba ô so với màn lập phiếu: Số phiếu, Trạng thái và Người duyệt.")
b.bullet("Góc phải khối THÔNG TIN CHUNG hiển thị người lập và thời điểm lập phiếu.")
b.bullet("Khối CHI TIẾT liệt kê đầy đủ các dòng hàng hóa đã chọn, kèm số lượng và tồn hiện có.")
b.bullet(
    "Nếu phiếu đã có ý kiến duyệt, màn hiện thêm khối \"Ghi chú duyệt\" chứa nguyên văn lý do "
    "người duyệt đã nhập. Phiếu chưa ai xử lý thì không có khối này."
)
b.bullet("Cuối trang là khối \"LỊCH SỬ THAY ĐỔI\" (xem Phần 9).")
b.para("Hàng nút cuối màn thay đổi theo trạng thái phiếu và quyền của người đang xem:")
b.table([
    ["Nút", "Màu", "Khi nào hiện"],
    ["Duyệt", "Xanh", "Phiếu Chờ duyệt và người xem có quyền Kế toán kho cùng công ty."],
    ["Sửa", "Xanh", "Phiếu Đang tạo hoặc Không duyệt và người xem là người lập."],
    ["In", "Trắng", "Luôn có."],
    ["Từ chối", "Đỏ", "Cùng điều kiện với nút Duyệt."],
    ["Xóa", "Đỏ", "Cùng điều kiện với nút Sửa."],
    ["Quay lại", "Trắng", "Luôn có. Trở về màn danh sách, giữ nguyên bộ lọc và trang đang xem."],
])
b.image("16-chi-tiet-nguoi-lap.png", "Màn chi tiết một phiếu nháp do chính mình lập")

# =====================================================================================
b.h1("PHẦN 6: DUYỆT VÀ TỪ CHỐI PHIẾU")

b.para(
    "Thao tác Duyệt và Từ chối yêu cầu quyền \"Kế toán kho\" và người duyệt phải cùng công ty với "
    "phiếu. Phiếu phải đang ở trạng thái Chờ duyệt."
)

b.h2("6.1. Duyệt phiếu")
b.para("Các bước:")
b.bullet("Mở màn Chi tiết của phiếu (bấm Số phiếu trên danh sách, hoặc bấm biểu tượng Duyệt ở cột Hành động).")
b.bullet("Kiểm tra người nhận và toàn bộ dòng hàng hóa, đặc biệt là cột Tồn hiện có.")
b.bullet("Bấm nút Duyệt màu xanh ở cuối màn, rồi xác nhận ở cửa sổ hỏi lại.")
b.para("Kết quả khi duyệt thành công:")
b.bullet("Hệ thống báo \"Duyệt phiếu thành công\" và quay về màn danh sách.")
b.bullet("Phiếu chuyển sang trạng thái Đã duyệt, cột Người duyệt ghi tên người vừa duyệt.")
b.bullet("Tồn của người lập bị trừ theo thứ tự lô nhận trước dùng trước; người nhận được ghi nhận một lô tồn mới đúng bằng số lượng chuyển.")
b.bullet("Người lập phiếu nhận được thông báo phiếu đã được duyệt.")
b.para(
    "Việc duyệt ghi tồn thật và KHÔNG hoàn tác được. Vì vậy hệ thống buộc phải mở màn Chi tiết "
    "để xem hàng hóa trước, không cho duyệt thẳng từ danh sách."
)
b.para("Hai trường hợp hệ thống chặn duyệt:")
b.bullet(
    "Hàng không còn đủ tồn (đã được chuyển hoặc dùng sang việc khác sau khi lập phiếu): hệ thống "
    "báo rõ tên hàng, cần bao nhiêu và hiện chỉ còn bao nhiêu. Phiếu vẫn giữ trạng thái Chờ duyệt."
)
b.bullet(
    "Phiếu không có dòng hàng hóa nào có số lượng: hệ thống báo \"Phiếu không có dòng hàng hóa "
    "nào để chuyển.\" và không cho duyệt."
)

b.h2("6.2. Từ chối phiếu")
b.bullet("Mở màn Chi tiết của phiếu đang Chờ duyệt.")
b.bullet("Bấm nút \"Từ chối\" màu đỏ ở cuối màn.")
b.bullet("Cửa sổ \"Từ chối phiếu\" mở ra với ô \"Lý do từ chối\" có dấu sao đỏ — đây là ô BẮT BUỘC.")
b.bullet("Nhập lý do rồi bấm nút Từ chối trong cửa sổ. Bấm Đóng nếu muốn hủy thao tác.")
b.para("Kết quả:")
b.bullet("Hệ thống báo \"Đã từ chối phiếu\" và quay về màn danh sách.")
b.bullet("Phiếu chuyển sang trạng thái Không duyệt; lý do hiện ở khối \"Ghi chú duyệt\" của màn Chi tiết và ở Lịch sử thay đổi.")
b.bullet("Tồn hàng của cả hai bên KHÔNG thay đổi.")
b.bullet("Người lập phiếu nhận được thông báo phiếu bị từ chối, có thể sửa lại rồi gửi duyệt lần nữa.")
b.para(
    "Nếu bỏ trống ô lý do rồi bấm Từ chối, hệ thống báo đỏ \"Bắt buộc phải nhập lý do từ chối\", "
    "cửa sổ không đóng và phiếu giữ nguyên trạng thái."
)

# =====================================================================================
b.h1("PHẦN 7: XÓA PHIẾU")

b.para(
    "Chỉ người lập phiếu mới xóa được, và chỉ với phiếu ở trạng thái Đang tạo hoặc Không duyệt. "
    "Phiếu Chờ duyệt và Đã duyệt không xóa được — nút Xóa sẽ không hiển thị."
)
b.bullet("Cách 1: bấm biểu tượng thùng rác đỏ ở cột Hành động trên màn danh sách.")
b.bullet("Cách 2: mở màn Chi tiết rồi bấm nút Xóa màu đỏ ở cuối màn.")
b.para(
    "Hệ thống mở cửa sổ xác nhận với nội dung \"Bạn có chắc muốn xóa phiếu <số phiếu>?\". Bấm "
    "Xóa để thực hiện, bấm hủy để giữ lại phiếu."
)
b.bullet("Xóa thành công: hệ thống báo \"Xóa thành công.\", danh sách tự tải lại và phiếu biến mất.")
b.bullet("Các dòng hàng hóa của phiếu cũng bị xóa theo, không để lại dữ liệu thừa.")
b.bullet("Tồn hàng của người lập và người nhận KHÔNG thay đổi, vì phiếu chưa duyệt thì chưa từng động vào tồn.")
b.bullet("Xóa từ màn Chi tiết thì hệ thống đưa về màn danh sách sau khi xóa xong.")

# =====================================================================================
b.h1("PHẦN 8: IN VÀ XUẤT DỮ LIỆU")

b.h2("8.1. In một phiếu")
b.para(
    "Bấm nút In ở cuối màn Chi tiết, hoặc chọn In trong menu Hành động khác trên màn danh sách. "
    "Bản in mở ở tab mới theo biểu mẫu \"PHIẾU YÊU CẦU CHUYỂN HÀNG\"."
)
b.image("14-ban-in-phieu.png", "Bản in một phiếu chuyển hàng nhập thẳng")
b.bullet("Đầu trang là tên và địa chỉ công ty của phiếu.")
b.bullet("Phần thông tin chung gồm số phiếu, ngày yêu cầu, người yêu cầu và ghi chú.")
b.bullet("Bảng hàng hóa gồm: STT · Tên hàng · Mã hàng · ĐVT · SL · SL theo ĐV cơ bản.")
b.bullet("Cuối bản in là khối ký của người lập phiếu.")
b.bullet("Bấm nút In màu xanh ở góc phải trên để gửi lệnh in ra máy in hoặc lưu thành tệp PDF.")

b.h2("8.2. In danh sách phiếu")
b.para(
    "Trên màn danh sách, bấm nút In. Bản in danh sách mở ở tab mới, in theo khổ ngang và chứa "
    "ĐÚNG những phiếu đang khớp bộ lọc hiện tại (không chỉ trang đang xem)."
)
b.image("15-ban-in-danh-sach.png", "Bản in danh sách phiếu chuyển hàng nhập thẳng")
b.bullet("Đầu trang là logo và thông tin liên hệ của công ty.")
b.bullet("Bảng gồm 6 cột: STT · Số phiếu · Ngày tạo · Người tạo · Người nhận · Trạng thái.")
b.bullet("Cuối bản in có khối ký với dòng ngày tháng và chữ \"Người lập\".")

b.h2("8.3. Xuất Excel danh sách")
b.para(
    "Bấm nút \"Xuất Excel\" trên màn danh sách. Hệ thống KHÔNG tải file ngay mà mở cửa sổ \"Chọn "
    "trường xuất Excel\" để người dùng chọn các cột cần có trong file."
)
b.image("05-chon-truong-xuat-excel.png", "Cửa sổ chọn trường xuất Excel")
b.bullet(
    "Có 11 trường để chọn: Số phiếu · Ngày tạo · Người tạo · Người nhận · Trạng thái · Người "
    "duyệt · Công ty · Phòng ban · Ghi chú · Người cập nhật · Ngày cập nhật."
)
b.bullet(
    "Thứ tự cột trong file chạy theo ĐÚNG thứ tự bạn tick. Muốn đổi vị trí một cột thì bỏ chọn "
    "rồi chọn lại theo trình tự mong muốn; dòng chữ dưới ô chọn luôn hiển thị thứ tự hiện tại."
)
b.bullet("Nút \"Chọn tất cả\" và \"Bỏ chọn hết\" giúp thao tác nhanh; dòng \"Đang chọn x/11 trường\" cho biết số trường đã tick.")
b.bullet("Bấm \"Xuất file\" để tải file về máy; bấm Đóng để thoát mà không xuất.")
b.para(
    "File Excel chứa toàn bộ phiếu khớp bộ lọc (không chỉ trang đang xem) và có sẵn khối ký ở "
    "cuối bảng gồm dòng \"Ngày ...... tháng ...... năm ......\", chữ \"Người lập\" và tên người "
    "xuất file."
)

# =====================================================================================
b.h1("PHẦN 9: LỊCH SỬ THAY ĐỔI")

b.para(
    "Mọi thao tác trên phiếu đều được ghi lại để tra cứu về sau. Có thể xem lịch sử ở hai nơi, "
    "nội dung hoàn toàn giống nhau."
)

b.h2("9.1. Khối Lịch sử ở màn Chi tiết")
b.para(
    "Cuối màn Chi tiết có khối \"LỊCH SỬ THAY ĐỔI\" kèm biểu tượng đồng hồ và con số cho biết số "
    "mốc đã ghi nhận. Khối này mặc định thu gọn; bấm nút \"Xem lịch sử\" để mở, bấm \"Thu gọn\" "
    "để đóng lại, bấm \"Làm mới\" để nạp lại dữ liệu mới nhất."
)
b.image("12-khoi-lich-su-chi-tiet.png", "Khối Lịch sử thay đổi ở màn chi tiết")

b.h2("9.2. Cửa sổ Lịch sử mở từ màn danh sách")
b.para(
    "Trên màn danh sách, chọn Lịch sử trong menu Hành động khác của dòng phiếu. Cửa sổ hiện tên "
    "phiếu ở phần tiêu đề và danh sách mốc y hệt khối ở màn Chi tiết."
)
b.image("08-popup-lich-su.png", "Cửa sổ Lịch sử mở từ màn danh sách")

b.h2("9.3. Cách đọc lịch sử")
b.bullet("Các mốc xếp theo thứ tự MỚI NHẤT ở trên cùng, cũ nhất ở dưới.")
b.bullet("Mỗi mốc ghi rõ thời điểm, loại thao tác, mã và tên người thực hiện kèm phòng ban.")
b.table([
    ["Loại thao tác", "Ý nghĩa"],
    ["Tạo phiếu", "Lần lập phiếu đầu tiên, kèm ảnh chụp toàn bộ thông tin ban đầu."],
    ["Chỉnh sửa", "Một lần sửa phiếu, chỉ liệt kê những gì thực sự thay đổi."],
    ["Gửi duyệt", "Người lập bấm Lưu và gửi duyệt."],
    ["Duyệt", "Kế toán kho duyệt phiếu."],
    ["Không duyệt", "Kế toán kho từ chối phiếu, kèm nguyên văn lý do."],
])
b.para("Mỗi mốc hiển thị chi tiết những nội dung đã đổi:")
b.bullet("Người nhận, Ghi chú, Trạng thái: hiện giá trị cũ và giá trị mới.")
b.bullet(
    "Hàng hóa: hiện dòng hàng được thêm hoặc bị bỏ, và với dòng bị sửa thì nêu rõ đổi ĐVT hay "
    "đổi Số lượng, từ giá trị nào sang giá trị nào."
)
b.bullet("Lý do từ chối luôn được hiển thị đầy đủ ở mốc \"Không duyệt\".")
b.para(
    "Nút \"Bộ lọc\" trong khối lịch sử cho lọc theo Loại hành động, Người thực hiện, Từ ngày và "
    "Đến ngày khi phiếu có nhiều mốc."
)
b.para(
    "Lưu ý: lịch sử chỉ ghi nhận thao tác thực hiện trên hệ thống này. Phiếu cũ hoặc phiếu được "
    "xử lý ở cổng phần mềm trước đó sẽ hiển thị \"Chưa có lịch sử thao tác nào.\" — đây là hiện "
    "tượng bình thường, không phải lỗi mất dữ liệu."
)

# =====================================================================================
b.h1("PHẦN 10: NHỮNG LƯU Ý QUAN TRỌNG")

b.bullet(
    "Duyệt phiếu là thao tác ghi tồn thật và không hoàn tác được. Hãy kiểm tra kỹ người nhận và "
    "từng dòng hàng hóa trước khi bấm Duyệt."
)
b.bullet(
    "Tồn hiển thị trên phiếu là tồn tại thời điểm mở màn. Nếu để phiếu chờ lâu, hàng có thể đã "
    "được chuyển đi nơi khác nên lúc duyệt hệ thống mới báo không đủ."
)
b.bullet(
    "Hệ thống không bao giờ tự sửa con số bạn nhập. Nhập sai thì màn hình báo đỏ ngay tại ô và "
    "giữ nguyên giá trị để bạn tự sửa lại."
)
b.bullet(
    "Số liệu hiển thị theo chuẩn quốc tế: dấu phẩy ngăn hàng nghìn, dấu chấm ngăn phần thập phân."
)
b.bullet(
    "Không tìm thấy một ô lọc hoặc một cột quen dùng thì hãy kiểm tra cửa sổ \"Cài đặt bộ lọc\" "
    "và \"Tuỳ chỉnh cột\" trước — rất có thể mục đó đang bị tắt trong cấu hình cá nhân của bạn."
)
b.bullet(
    "Sau mỗi thao tác Lưu, Duyệt, Từ chối hay Xóa, hệ thống đều đưa bạn về màn danh sách để tiện "
    "xử lý phiếu tiếp theo."
)

n = b.finish()
print("Da tao HDSD:", OUTPUT)
