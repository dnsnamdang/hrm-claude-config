# -*- coding: utf-8 -*-
"""Sinh tai lieu HDSD (.docx) cho man "Phieu chi tien" (phan he Tai chinh).

Khung + style lay tu `.claude/skills/hdsd-documenter/assets/HDSD_MAU.docx`.
Anh that: pc_shots/ (cong dev hrm-crm.eteksofts.com; rieng man IN chup tren local vi trang in
tu bat hop thoai in va khoa phien dieu khien) — KHONG commit.

Chay:  python .plans/gop-db/finance-bill-payment/gen_hdsd.py
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

OUT = os.path.join(HERE, "HDSD_Phiếu chi tiền.docx")
SHOTS = os.path.join(HERE, "pc_shots")

MENU = "Tài chính → Quản lý tiền → Thanh toán tiền mặt → Phiếu chi"

b = HdsdBuilder(output=OUT, shots_dir=SHOTS,
                cover_title="(Màn hình: Phiếu chi tiền)",
                doc_title="HDSD - Phiếu chi tiền")

# ══════════════════════════════════════════════════════════ TỔNG QUAN
b.h1("TỔNG QUAN")

b.h2("1. Thuật ngữ và từ viết tắt")
b.table([
    ["Thuật ngữ", "Giải thích"],
    ["Phiếu chi tiền",
     "Chứng từ kế toán ghi nhận khoản tiền doanh nghiệp chi ra. Mã phiếu do hệ thống sinh tự "
     "động dạng «mã công ty».PC«tháng năm»."
     "«5 chữ số», ví dụ TPE.PC0826.00025."],
    ["Luồng lập từ Đề nghị thanh toán",
     "Áp dụng với các loại chi: Chi trả nhà cung cấp, Chi trả lại khách hàng, Chi thưởng NVKD, "
     "Chi thưởng thực hiện hợp đồng, Chi khác, Thanh toán chi phí vận chuyển NCC. Kế toán chọn "
     "một phiếu đề nghị thanh toán rồi lập phiếu chi. Chỉ MỘT cấp duyệt (Thủ quỹ)."],
    ["Luồng Chi thu nhập cho nhân viên",
     "Lập TRỰC TIẾP, không qua phiếu đề nghị. Kế toán chọn phòng ban, hệ thống tự hút 6 khoản "
     "thu nhập của từng nhân viên từ sổ kế toán. Phải qua HAI cấp duyệt: Kế toán trưởng rồi "
     "Thủ quỹ."],
    ["Tài khoản có",
     "Tài khoản ghi bên Có của bút toán — thường là tài khoản tiền. Khai một lần cho cả phiếu."],
    ["Tài khoản nợ",
     "Tài khoản ghi bên Nợ, khai riêng cho từng dòng chi tiết."],
    ["Số tiền đề nghị chi", "Số tiền lấy từ phiếu đề nghị thanh toán. Chỉ đọc."],
    ["Số tiền chi",
     "Số tiền kế toán chốt sẽ chi, do người lập phiếu nhập. Không được lớn hơn số tiền đề nghị "
     "chi của chính dòng đó."],
    ["Số tiền thực chi",
     "Số tiền người duyệt xác nhận chi thật, nhập trong cửa sổ Duyệt trước khi bấm Duyệt."],
    ["Số dư (bảng thu nhập nhân viên)",
     "Số tiền hệ thống tính ra cho từng nhân viên từ sổ kế toán. ĐƯỢC PHÉP ÂM (trường hợp truy "
     "thu); hệ thống so trần số tiền chi theo giá trị tuyệt đối của số dư."],
    ["Hình thức thanh toán",
     "TM (tiền mặt) hoặc CK (chuyển khoản). Chọn CK thì form hiện thêm khối thông tin ngân hàng "
     "nhận tiền và ngân hàng trung gian."],
    ["Đang tạo", "Phiếu mới lưu nháp. Chỉ người lập nhìn thấy, sửa được và xoá được."],
    ["Chờ KT trưởng duyệt",
     "Chỉ phát sinh với loại Chi thu nhập cho nhân viên. Chờ Kế toán trưởng duyệt (bước 1)."],
    ["Chờ chi tiền", "Chờ Thủ quỹ duyệt — cấp duyệt cuối, ghi bút toán vào sổ kế toán."],
    ["Đã duyệt",
     "Thủ quỹ đã duyệt; hệ thống ĐÃ ghi bút toán vào sổ kế toán. Không sửa, không xoá, không hủy "
     "được nữa."],
    ["Hủy", "Người duyệt đã hủy phiếu kèm lý do. Không ghi bút toán nào."],
])

b.h2("2. Cập nhật tài liệu")
b.table([
    ["Phiên bản", "Ngày", "Nội dung", "Người thực hiện"],
    ["1.0", "03/09/2026", "Ban hành lần đầu cho màn Phiếu chi tiền "
     "(phân hệ Tài chính, nhóm Quản lý tiền).", "Nhóm phát triển HRM"],
])

b.h2("3. Giới thiệu chung")
b.para(
    "Màn hình Phiếu chi tiền dùng để lập và theo dõi chứng từ chi tiền của doanh nghiệp. Màn "
    "hình phục vụ hai luồng nghiệp vụ khác hẳn nhau, phân biệt bằng ô «Loại chi»:")
b.bullet(
    "Luồng lập từ Đề nghị thanh toán: kế toán chọn một phiếu đề nghị đang chờ, chốt số tiền chi "
    "rồi gửi duyệt. Thủ quỹ duyệt là xong — MỘT cấp duyệt.")
b.bullet(
    "Luồng Chi thu nhập cho nhân viên: lập trực tiếp, chọn phòng ban để hệ thống hút số liệu "
    "thu nhập từng nhân viên. Phiếu phải qua HAI cấp duyệt — Kế toán trưởng rồi Thủ quỹ.")
b.para("Đường dẫn vào màn hình:")
b.bullet("Menu: " + MENU)
b.bullet("Đường dẫn trực tiếp: /finance/bill-payments")
b.image("24-duong-dan-menu.png", "Đường dẫn menu tới màn Phiếu chi tiền")

b.para("CẢNH BÁO QUAN TRỌNG TRƯỚC KHI DÙNG:")
b.bullet(
    "Bước THỦ QUỸ duyệt là thao tác KHÔNG HOÀN TÁC ĐƯỢC. Hệ thống ghi ngay bút toán vào sổ kế "
    "toán, không có chức năng gỡ bút toán. Hãy kiểm tra kỹ số tiền thực chi của từng dòng trước "
    "khi bấm.")
b.bullet(
    "Bước KẾ TOÁN TRƯỞNG duyệt thì CHƯA ghi sổ kế toán — chỉ chuyển phiếu sang «Chờ chi tiền». "
    "Tiền chỉ thực sự ra khỏi quỹ ở bước Thủ quỹ.")
b.bullet(
    "Người lập KHÔNG tự hủy được phiếu đã gửi duyệt. Gửi đi rồi thì quyền định đoạt thuộc về "
    "cấp đang chờ duyệt.")

b.h2("4. Quyền và phạm vi dữ liệu")
b.para(
    "Màn này có năm quyền liên quan. Hai quyền quyết định NHÌN THẤY BAO NHIÊU PHIẾU, ba quyền "
    "quyết định LÀM ĐƯỢC GÌ.")
b.table([
    ["Tên quyền", "Cho phép làm gì", "Thể hiện trên giao diện"],
    ["Xem tất cả phiếu chi của tổng công ty",
     "Nhìn thấy phiếu chi của mọi công ty.",
     "Danh sách hiện phiếu của tất cả công ty."],
    ["Xem tất cả phiếu chi của công ty",
     "Nhìn thấy phiếu chi thuộc công ty của mình.",
     "Danh sách chỉ hiện phiếu cùng công ty."],
    ["Kế toán thanh toán",
     "Lập, sửa, xoá, gửi duyệt phiếu chi; mở được cửa sổ chọn phiếu đề nghị và xem được số liệu "
     "thu nhập nhân viên.",
     "Không có quyền này thì cửa sổ chọn phiếu đề nghị bị từ chối, bảng thu nhập nhân viên không "
     "nạp được, và thao tác lưu bị chặn — dù nút «Tạo mới» vẫn hiện."],
    ["Kế toán trưởng duyệt phiếu chi",
     "Duyệt và hủy phiếu ở trạng thái «Chờ KT trưởng duyệt» (chỉ phát sinh với loại Chi thu nhập "
     "cho nhân viên).",
     "Màn chi tiết phiếu ở trạng thái đó hiện nút «Duyệt phiếu chi» và «Hủy phiếu chi»."],
    ["Thủ quỹ duyệt phiếu chi",
     "Duyệt và hủy phiếu ở trạng thái «Chờ chi tiền». Đây là cấp duyệt cuối, ghi bút toán vào sổ "
     "kế toán.",
     "Màn chi tiết phiếu ở trạng thái đó hiện nút «Duyệt phiếu chi» và «Hủy phiếu chi»."],
    ["(Không có quyền xem nào)",
     "Chỉ nhìn thấy phiếu chi do chính mình lập.",
     "Danh sách chỉ có phiếu của mình."],
])
b.para("Ba quy tắc quan trọng về quyền:")
b.bullet(
    "Cả hai cấp duyệt đều bắt buộc CÙNG CÔNG TY với phiếu. Người có quyền duyệt nhưng khác công "
    "ty thì không mở được phiếu.")
b.bullet(
    "Hệ thống chỉ có MỘT nút «Duyệt phiếu chi» và tự biết đang duyệt ở cấp nào theo trạng thái "
    "phiếu. Người có quyền Kế toán trưởng mở phiếu «Chờ chi tiền» sẽ không thấy nút, và ngược lại.")
b.bullet(
    "Vai trò quản trị hệ thống được coi như có đủ các quyền trên, RIÊNG chức năng Sửa và Xóa thì "
    "KHÔNG được miễn trừ — vẫn phải là người lập phiếu.")
b.para("Hai lớp bảo vệ dữ liệu luôn được áp dụng:")
b.bullet(
    "Phiếu ở trạng thái «Đang tạo» của NGƯỜI KHÁC luôn bị ẩn khỏi danh sách, và quyền xem theo "
    "cấp cũng không mở được màn chi tiết của nháp người khác.")
b.bullet(
    "Người đã duyệt một phiếu luôn mở lại được phiếu đó; và người có quyền duyệt luôn mở được "
    "phiếu cùng công ty đang chờ đúng cấp mình — kể cả khi không có quyền xem theo cấp nào.")

# ══════════════════════════════════════════════════════════ PHẦN 1
b.h1("PHẦN 1: TRUY CẬP VÀ BỐ CỤC MÀN HÌNH")

b.h2("1. Cách vào màn hình")
b.para("1. Đăng nhập hệ thống, ở trang chọn phân hệ bấm ô «Tài chính».")
b.para("2. Trên thanh menu bên trái, bấm nhóm «Quản lý tiền».")
b.para("3. Trong bảng chức năng vừa mở, tìm nhóm «THANH TOÁN TIỀN MẶT».")
b.para("4. Bấm chức năng «Phiếu chi».")
b.para("Màn hình mở ra có tiêu đề «Danh sách phiếu chi».")

b.h2("2. Bố cục màn danh sách")
b.image("01-danh-sach.png", "Màn hình danh sách Phiếu chi tiền")
b.para("Màn hình chia làm 2 khối từ trên xuống:")
b.bullet(
    "Khối «Bộ lọc danh sách»: ô tìm nhanh, nút «Tìm kiếm», nút «Làm mới», nút «Cài đặt bộ lọc» "
    "và nút «Tìm kiếm nâng cao».")
b.bullet(
    "Khối lưới dữ liệu: tiêu đề «Danh sách phiếu chi», nút «Tạo mới» và nút biểu tượng cấu hình "
    "cột ở góc phải, bảng dữ liệu và thanh phân trang.")
b.para(
    "Bảng có 14 cột nên rộng hơn màn hình — dùng thanh cuộn ngang ngay phía trên và phía dưới "
    "bảng để xem các cột bên phải (Trạng thái, Hành động).")
b.image("02-danh-sach-cot-phai.png",
        "Danh sách sau khi cuộn ngang — thấy cột Trạng thái và Hành động")

b.h2("3. Các cột của bảng danh sách")
b.table([
    ["Cột", "Nội dung", "Sắp xếp được"],
    ["STT", "Số thứ tự dòng, đánh theo từng trang. Luôn hiển thị, không tắt được.", "Không"],
    ["Mã phiếu", "Mã phiếu chi. Bấm vào mã để mở màn chi tiết. Luôn hiển thị, không tắt được.",
     "Có"],
    ["Mã phiếu đề nghị chi", "Mã phiếu đề nghị thanh toán gốc. Loại Chi thu nhập cho nhân viên "
     "không có phiếu đề nghị nên hiện dấu gạch ngang.", "Không"],
    ["Loại chi", "Một trong 7 loại chi.", "Không"],
    ["Khách hàng / Nhà cung cấp", "Đối tượng nhận tiền của dòng chi tiết đầu tiên.", "Không"],
    ["Số tiền", "Tổng số tiền chi của phiếu, ngăn cách hàng nghìn bằng dấu chấm.", "Có"],
    ["Người đề nghị", "Người lập phiếu đề nghị thanh toán (khác Người tạo).", "Không"],
    ["Phòng ban", "Phòng ban gắn với phiếu.", "Không"],
    ["Ngày tạo", "Thời điểm lập phiếu chi, dạng ngày/tháng/năm giờ:phút.", "Có"],
    ["Người tạo", "Người lập phiếu chi.", "Không"],
    ["Ngày cập nhật", "Thời điểm sửa gần nhất.", "Có"],
    ["Người cập nhật", "Người sửa phiếu gần nhất.", "Không"],
    ["Trạng thái", "Nhãn màu: xám với Đang tạo, vàng với Chờ KT trưởng duyệt và Chờ chi tiền, "
     "xanh với Đã duyệt, đỏ với Hủy.", "Có"],
    ["Hành động", "Các nút thao tác của dòng. Luôn hiển thị, không tắt được.", "Không"],
])
b.para(
    "Mặc định danh sách sắp xếp theo Ngày tạo giảm dần — phiếu mới nhất nằm trên cùng. Màu nhãn "
    "trạng thái phân biệt được cả 5 trạng thái, đây là điểm cải tiến so với hệ thống cũ (hệ "
    "thống cũ để cùng một màu đỏ cho bốn trạng thái, không phân biệt được «đang chờ» với «đã hủy»).")

b.h2("4. Các nút thao tác trên một dòng")
b.table([
    ["Nút", "Biểu tượng", "Điều kiện hiện", "Tác dụng"],
    ["Sửa", "Bút chì", "Phiếu «Đang tạo» do chính mình lập và có quyền Kế toán thanh toán",
     "Mở màn Sửa phiếu chi."],
    ["Xóa", "Thùng rác đỏ", "Cùng điều kiện với nút Sửa", "Mở hộp xác nhận xoá phiếu."],
    ["In", "Máy in", "Xem được phiếu", "Mở tab mới hiển thị bản in 2 liên."],
    ["Xuất Excel", "Biểu tượng bảng tính", "Xem được phiếu",
     "Tải về tệp Excel của đúng phiếu đó."],
    ["Duyệt", "Dấu tích trong vòng tròn", "Phiếu đang chờ đúng cấp duyệt của người dùng, cùng "
     "công ty", "CHỈ MỞ màn chi tiết — không duyệt ngay."],
    ["Lịch sử", "Đồng hồ quay ngược", "Luôn hiện", "Mở cửa sổ Lịch sử thay đổi của phiếu."],
])
b.para("Lưu ý: màn danh sách KHÔNG có nút «Hủy phiếu». Muốn hủy phải vào màn chi tiết.")

# ══════════════════════════════════════════════════════════ PHẦN 2
b.h1("PHẦN 2: TÌM KIẾM VÀ LỌC DANH SÁCH")

b.h2("1. Ô tìm nhanh")
b.para(
    "Ô tìm nhanh ghi sẵn dòng gợi ý «Tìm theo mã phiếu chi...». Gõ một phần mã phiếu rồi bấm nút "
    "«Tìm kiếm» màu xanh (hoặc nhấn Enter).")
b.para(
    "LƯU Ý: ô tìm nhanh KHÔNG tự tìm khi đang gõ — bắt buộc phải bấm nút. Ngược lại, mọi ô trong "
    "«Tìm kiếm nâng cao» tự lọc ngay khi đổi giá trị.")

b.h2("2. Tìm kiếm nâng cao")
b.para(
    "Bấm nút «Tìm kiếm nâng cao» để mở thêm 9 ô lọc. Khi khối đang mở, nút đổi chữ thành «Ẩn "
    "tìm kiếm nâng cao».")
b.image("03-loc-nang-cao.png", "Khối Tìm kiếm nâng cao khi đang mở")
b.table([
    ["Ô lọc", "Kiểu nhập", "Cách hoạt động"],
    ["Mã phiếu đề nghị chi", "Gõ tay", "Tìm phiếu chi theo mã phiếu đề nghị gốc."],
    ["Loại chi", "Danh sách chọn", "Đủ 7 loại chi."],
    ["Trạng thái", "Danh sách chọn",
     "Năm giá trị: Đang tạo, Chờ chi tiền, Đã duyệt, Hủy, Chờ KT trưởng duyệt. Chọn «Đang tạo» "
     "chỉ ra nháp của chính mình."],
    ["Người lập", "Danh sách nhân viên", "Lọc theo người lập PHIẾU CHI."],
    ["Người đề nghị", "Danh sách nhân viên", "Lọc theo người lập PHIẾU ĐỀ NGHỊ."],
    ["Phòng ban", "Danh sách phòng ban", "Lọc theo phòng ban gắn với phiếu."],
    ["Khách hàng / Nhà cung cấp", "Danh sách tìm từ xa",
     "Phải gõ ít nhất 2 ký tự mới hiện gợi ý. Ô này gộp chung nguồn khách hàng và nhà cung cấp."],
    ["Số tiền từ – Số tiền đến", "Nhập số tiền", "So theo cột «Số tiền» của lưới."],
    ["Ngày lập từ – Ngày lập đến", "Chọn ngày trên lịch",
     "Lọc theo NGÀY LẬP PHIẾU CHI (cột Ngày tạo). Cả hai mốc lấy trọn ngày."],
])
b.para(
    "Các điều kiện cộng dồn với nhau. Mỗi lần đổi một ô, danh sách tự nạp lại và quay về trang 1.")

b.h2("3. Nút Làm mới")
b.para(
    "Bấm «Làm mới» để xoá toàn bộ điều kiện lọc và ô tìm nhanh, đưa danh sách về trang 1. Phạm "
    "vi dữ liệu theo quyền KHÔNG đổi.")

b.h2("4. Cài đặt bộ lọc — chọn ô lọc muốn hiển thị")
b.para("Bấm nút «Cài đặt bộ lọc» để mở cửa sổ ẩn bớt hoặc đổi thứ tự các ô lọc nâng cao.")
b.image("04-cai-dat-bo-loc.png", "Cửa sổ Cài đặt bộ lọc")
b.bullet("Bỏ tích một ô để ẩn ô lọc đó khỏi khối Tìm kiếm nâng cao.")
b.bullet("Kéo biểu tượng sáu chấm ở đầu mỗi ô để đổi thứ tự hiển thị.")
b.bullet("Bấm «Lưu» để áp dụng — cấu hình lưu riêng theo từng người và từng màn hình.")
b.bullet("Bấm «Khôi phục mặc định» để đưa về đủ 9 nhóm ô theo thứ tự ban đầu.")
b.bullet("Bấm «Đóng» để thoát mà không lưu thay đổi.")

b.h2("5. Ghi nhớ bộ lọc trong 10 phút")
b.para(
    "Hệ thống ghi nhớ điều kiện lọc trong 10 phút. Rời màn rồi quay lại trong khoảng thời gian "
    "này thì điều kiện cũ vẫn còn — nếu thấy danh sách «thiếu phiếu», hãy bấm «Làm mới» trước "
    "khi kết luận là mất dữ liệu.")

# ══════════════════════════════════════════════════════════ PHẦN 3
b.h1("PHẦN 3: SẮP XẾP, PHÂN TRANG VÀ CẤU HÌNH CỘT")

b.h2("1. Sắp xếp")
b.para(
    "Bấm vào tiêu đề cột có biểu tượng hai mũi tên để sắp xếp. Bấm lần một là tăng dần, bấm lần "
    "hai là giảm dần. Mỗi lần đổi sắp xếp, danh sách quay về trang 1 nhưng GIỮ NGUYÊN điều kiện "
    "lọc.")
b.para("Bốn cột sắp xếp được: Mã phiếu, Số tiền, Ngày tạo, Ngày cập nhật, Trạng thái.")

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
    "Bấm «Lưu» để áp dụng. Cấu hình lưu riêng theo từng người và riêng cho màn này.")

# ══════════════════════════════════════════════════════════ PHẦN 4
b.h1("PHẦN 4: TẠO MỚI PHIẾU CHI TIỀN")

b.h2("1. Ai làm được")
b.para(
    "Chức năng này cần quyền «Kế toán thanh toán» (hoặc vai trò quản trị hệ thống). Nút «Tạo "
    "mới» hiện với mọi người, nhưng nếu thiếu quyền thì cửa sổ chọn phiếu đề nghị bị từ chối, "
    "bảng thu nhập nhân viên không nạp được và thao tác lưu bị chặn với thông báo «Bạn không có "
    "quyền lập phiếu chi tiền».")

b.h2("2. Mở màn Tạo mới")
b.para(
    "Bấm nút «Tạo mới» (biểu tượng dấu cộng, màu xanh) ở góc phải khối lưới. Hệ thống mở màn "
    "riêng có tiêu đề «Thêm phiếu chi tiền».")
b.image("06-tao-moi.png", "Màn Thêm phiếu chi tiền khi vừa mở")

b.h2("3. Bước đầu tiên — chọn Loại chi")
b.para(
    "Đây là ô QUAN TRỌNG NHẤT của form: chọn xong loại chi thì toàn bộ cấu trúc form mới định "
    "hình. Loại chi cũng là trường DUY NHẤT bắt buộc ngay cả khi chỉ Lưu nháp.")
b.image("08-chon-loai-chi.png", "Danh sách 7 loại chi")
b.table([
    ["Loại chi", "Thuộc luồng nào", "Bắt buộc có phiếu đề nghị khi gửi duyệt?"],
    ["Chi trả nhà cung cấp", "Lập từ Đề nghị thanh toán", "CÓ"],
    ["Chi trả lại khách hàng", "Lập từ Đề nghị thanh toán", "CÓ"],
    ["Chi thưởng NVKD", "Lập từ Đề nghị thanh toán", "CÓ"],
    ["Chi thưởng thực hiện hợp đồng", "Lập từ Đề nghị thanh toán", "KHÔNG"],
    ["Chi khác", "Lập từ Đề nghị thanh toán", "KHÔNG"],
    ["Thanh toán chi phí vận chuyển NCC", "Lập từ Đề nghị thanh toán", "KHÔNG"],
    ["Chi thu nhập cho nhân viên", "Lập trực tiếp, 2 cấp duyệt", "Không áp dụng"],
])
b.para(
    "Lưu ý ở cột cuối: ba loại «Chi thưởng thực hiện hợp đồng», «Chi khác», «Thanh toán chi phí "
    "vận chuyển NCC» gửi duyệt được dù để trống cả phiếu đề nghị lẫn dòng chi tiết. Đây là quy "
    "tắc nghiệp vụ đã chốt, không phải sót kiểm tra.")

b.h2("4. Khối Thông tin chung")
b.table([
    ["Trường", "Kiểu nhập", "Bắt buộc khi gửi duyệt", "Giá trị điền sẵn khi tạo mới", "Ghi chú"],
    ["Số phiếu đề nghị", "Ô chỉ đọc, bấm vào để mở cửa sổ chọn", "Tuỳ loại chi (xem bảng trên)",
     "Trống", "Chỉ hiện với luồng lập từ Đề nghị thanh toán."],
    ["Tài khoản có", "Danh sách chọn", "Có", "Trống",
     "Chỉ liệt kê tài khoản đang hoạt động và là tài khoản cấp cuối."],
    ["Loại chi", "Danh sách chọn", "Có — kể cả khi Lưu nháp", "Trống", "Xem mục 3 ở trên."],
    ["Hình thức thanh toán", "Danh sách chọn", "Có với luồng Chi thu nhập nhân viên", "TM",
     "Hai giá trị TM và CK. Chọn phiếu đề nghị thì tự điền theo phiếu đề nghị."],
    ["Người nhận", "Ô nhập", "Có", "Trống", "Tối đa 255 ký tự."],
    ["Loại tiền", "Ô chỉ đọc / danh sách", "Có với luồng Chi thu nhập nhân viên", "VietNamDong",
     "Luồng lập từ đề nghị thì tự điền theo phiếu đề nghị."],
    ["Tỷ giá (VND)", "Ô nhập số", "Có với luồng Chi thu nhập nhân viên", "1",
     "Tự điền theo phiếu đề nghị khi chọn phiếu."],
    ["Người đề nghị", "Ô chỉ đọc", "–", "Người đang đăng nhập", "Đổi theo phiếu đề nghị đã chọn."],
    ["Phòng ban", "Ô chỉ đọc", "–", "Phòng ban của người đang đăng nhập", "–"],
    ["Phòng ban chi", "Danh sách chọn", "Có", "Trống",
     "CHỈ hiện với loại Chi thu nhập cho nhân viên. Chọn xong hệ thống mới nạp bảng chi tiết."],
    ["Lý do chi", "Ô nhập nhiều dòng", "Có với luồng Chi thu nhập nhân viên", "Trống",
     "Luồng lập từ đề nghị thì tự điền theo phiếu đề nghị."],
])
b.para(
    "Hộp «Giá trị điền sẵn khi tạo mới»: Hình thức thanh toán = TM; Loại tiền = VietNamDong; "
    "Tỷ giá = 1; Người đề nghị và Phòng ban = theo người đang đăng nhập; mọi ô còn lại để trống.")
b.image("07-hinh-thuc-thanh-toan.png", "Hai lựa chọn của ô Hình thức thanh toán")

b.h2("5. Luồng lập từ Đề nghị thanh toán")
b.h3("5.1. Chọn phiếu đề nghị chi")
b.para("1. Chọn Loại chi thuộc nhóm lập-từ-đề-nghị.")
b.para("2. Bấm vào ô «Số phiếu đề nghị».")
b.para(
    "3. Cửa sổ «Chọn phiếu đề nghị chi» mở ra, phụ đề ghi rõ «Chỉ phiếu Chờ tạo phiếu chi và "
    "chưa lập phiếu chi».")
b.image("11-popup-chon-de-nghi.png", "Cửa sổ Chọn phiếu đề nghị chi")
b.para(
    "4. Tìm phiếu cần lập: gõ mã vào ô «Mã phiếu đề nghị», chọn «Loại chi», hoặc chọn «Người "
    "lập», rồi bấm «Tìm kiếm». Bấm «Làm mới» để xoá điều kiện tìm.")
b.para("5. Bấm vào dòng phiếu đề nghị cần chọn.")
b.para("Cửa sổ tự đóng và hệ thống kéo về toàn bộ dữ liệu của phiếu đề nghị:")
b.bullet("Hình thức thanh toán, Loại tiền, Tỷ giá, Người đề nghị, Phòng ban, Lý do chi tự điền.")
b.bullet("Xuất hiện khối thông tin nhà cung cấp / khách hàng nhận tiền.")
b.bullet("Bảng «Chi tiết» nạp đủ các dòng của phiếu đề nghị.")
b.image("12-form-da-chon-de-nghi.png",
        "Màn Thêm phiếu chi sau khi chọn phiếu đề nghị — bảng Chi tiết đã nạp")
b.para(
    "Nếu không tìm thấy phiếu đề nghị cần lập, thường do một trong ba lý do: phiếu chưa được gửi "
    "duyệt; phiếu đã có phiếu chi khác; hoặc bạn không có quyền «Kế toán thanh toán».")

b.h3("5.2. Khối thông tin ngân hàng (chỉ với hình thức chuyển khoản)")
b.para(
    "Khi hình thức thanh toán là CK, form hiện thêm hai khối: «NGÂN HÀNG NHẬN TIỀN» và «NGÂN "
    "HÀNG TRUNG GIAN». Mỗi khối gồm: Ngân hàng, Số tài khoản, Tài khoản, Tên ngân hàng, Swift "
    "Code, IBAN Number, Địa chỉ. Chọn hình thức TM thì hai khối này ẩn.")

b.h3("5.3. Bảng Chi tiết")
b.para(
    "Bảng kéo thẳng từ phiếu đề nghị; số dòng luôn đúng bằng số dòng của phiếu đề nghị. Các cột:")
b.table([
    ["Cột", "Nội dung", "Nhập được?"],
    ["STT", "Số thứ tự dòng.", "Không"],
    ["Tài khoản nợ", "Tài khoản ghi bên Nợ.", "Có — bắt buộc khi gửi duyệt"],
    ["Tên tài khoản", "Tên của tài khoản vừa chọn, tự hiện.", "Không"],
    ["Đối tượng", "Khách hàng hoặc nhà cung cấp nhận tiền.", "Không"],
    ["Số đơn hàng/Hợp đồng", "Hợp đồng gắn với dòng.", "Không"],
    ["Số tiền đề nghị chi", "Số tiền trên phiếu đề nghị.", "Không"],
    ["Số tiền chi", "Số tiền kế toán chốt sẽ chi.", "Có"],
    ["Ghi chú", "Ghi chú của dòng.", "Có"],
])
b.para(
    "Cuối bảng có dòng «Tổng cộng» cộng dọc từng cột tiền. Với phiếu ngoại tệ, mỗi nhóm tiền có "
    "2 cột: cột nguyên tệ và cột quy đổi ra đồng Việt Nam.")
b.para(
    "QUY TẮC QUAN TRỌNG: «Số tiền chi» của một dòng KHÔNG được lớn hơn «Số tiền đề nghị chi» của "
    "chính dòng đó. Gõ vượt thì khi bấm lưu hệ thống báo «Không được lớn hơn số tiền đề nghị "
    "chi» và không lưu.")

b.h2("6. Luồng Chi thu nhập cho nhân viên")
b.para(
    "Chọn Loại chi = «Chi thu nhập cho nhân viên», form đổi cấu trúc ngay: ô «Số phiếu đề nghị» "
    "biến mất, xuất hiện ô «Phòng ban chi» có dấu sao đỏ, và ô «Lý do chi» cũng thành bắt buộc.")
b.image("09-form-chi-thu-nhap-nv.png",
        "Màn Tạo mới sau khi chọn loại Chi thu nhập cho nhân viên")
b.para("Các bước:")
b.para("1. Chọn «Phòng ban chi» — bấm vào ô rồi gõ để tìm nhanh trong danh sách phòng ban.")
b.para(
    "2. Hệ thống tự hút số liệu thu nhập của từng nhân viên trong phòng ban đó từ sổ kế toán và "
    "nạp vào bảng Chi tiết.")
b.image("10-bang-thu-nhap-nhan-vien.png",
        "Bảng thu nhập nhân viên sau khi chọn Phòng ban chi")
b.para("Bảng Chi tiết của luồng này có 2 tab và các cột sau:")
b.table([
    ["Cột / thành phần", "Nội dung", "Nhập được?"],
    ["Tab «Chi tiết»", "Bảng chính, mỗi dòng là MỘT nhân viên.", "–"],
    ["Tab «Chi tiết vụ việc»", "Bảng phụ tách 6 khoản thu nhập của từng nhân viên.", "–"],
    ["Ô tích chọn", "Tích để đưa nhân viên đó vào phiếu. Mặc định tích sẵn tất cả.", "Có"],
    ["STT", "Số thứ tự dòng.", "Không"],
    ["Số tài khoản nợ", "Tài khoản ghi bên Nợ. Điền sẵn theo dữ liệu hệ thống.",
     "Có — bắt buộc khi gửi duyệt"],
    ["Tên tài khoản", "Tên của tài khoản vừa chọn.", "Không"],
    ["Nhân viên", "Mã và họ tên nhân viên.", "Không"],
    ["Số dư", "Số tiền hệ thống tính ra từ sổ kế toán. ĐƯỢC PHÉP ÂM.", "Không"],
    ["Số tiền chi", "Số tiền chi cho nhân viên đó.", "Có — bắt buộc khi gửi duyệt"],
])
b.para(
    "Về cột «Số dư» âm: đây là trường hợp truy thu, hoàn toàn bình thường. Hệ thống so trần số "
    "tiền chi theo GIÁ TRỊ TUYỆT ĐỐI của số dư nên dòng số dư âm vẫn chi được.")
b.para(
    "Nếu phòng ban chưa có số liệu thu nhập, bảng hiện dòng đỏ «Không có dữ liệu phù hợp» — hãy "
    "kiểm tra lại kỳ số liệu hoặc chọn phòng ban khác.")

b.h2("7. Lưu phiếu")
b.para("Cuối trang có ba nút, luôn cố định ở đáy màn hình:")
b.table([
    ["Nút", "Có hỏi xác nhận?", "Kết quả"],
    ["Lưu nháp", "Không",
     "Lưu phiếu ở trạng thái «Đang tạo». KHÔNG bắt buộc trường nào, TRỪ «Loại chi». Thông báo "
     "«Thêm phiếu chi tiền thành công!». Phiếu chỉ mình nhìn thấy, KHÔNG gửi thông báo cho ai."],
    ["Lưu và gửi duyệt", "Có",
     "Mở hộp «Xác nhận lưu và gửi duyệt» hỏi «Bạn đồng ý lưu và duyệt?». Sau khi xác nhận, phiếu "
     "được lưu rồi gửi duyệt luôn: luồng lập-từ-đề-nghị chuyển sang «Chờ chi tiền», luồng Chi thu "
     "nhập nhân viên chuyển sang «Chờ KT trưởng duyệt»."],
    ["Quay lại", "Có (nếu đã nhập dở)", "Về màn danh sách."],
])
b.image("13-xac-nhan-gui-duyet.png", "Hộp Xác nhận lưu và gửi duyệt")
b.para(
    "ĐIỂM KHÁC HỆ THỐNG CŨ: nút «Lưu nháp» không bắt buộc trường nào (trừ Loại chi), nên bạn cất "
    "được form dở dang rồi hôm sau làm tiếp. Toàn bộ ràng buộc bắt buộc chỉ áp khi bấm «Lưu và "
    "gửi duyệt».")
b.para(
    "Nếu còn ô chưa hợp lệ, hệ thống không lưu mà hiện lỗi đỏ ngay dưới từng ô. Cửa sổ không "
    "đóng, mọi dữ liệu đã nhập vẫn còn.")
b.image("14-loi-validate.png",
        "Lỗi hiển thị ngay dưới ô Người nhận và ô Tài khoản nợ khi gửi duyệt")
b.table([
    ["Trường hợp", "Thông báo lỗi"],
    ["Chưa chọn Loại chi", "Bắt buộc chọn loại chi"],
    ["Chưa chọn Tài khoản có", "Bắt buộc chọn tài khoản có"],
    ["Chưa nhập Người nhận", "Bắt buộc nhập người nhận"],
    ["Người nhận quá 255 ký tự", "Người nhận tối đa 255 ký tự"],
    ["Chưa chọn phiếu đề nghị (với 3 loại bắt buộc)", "Bắt buộc chọn phiếu đề nghị thanh toán"],
    ["Chưa chọn Tài khoản nợ của một dòng", "Bắt buộc chọn tài khoản nợ"],
    ["Bảng chi tiết trống (với loại bắt buộc)", "Bắt buộc nhập chi tiết phiếu chi"],
    ["Số tiền chi vượt số tiền đề nghị chi", "Không được lớn hơn số tiền đề nghị chi"],
    ["Số tiền chi âm", "Số tiền duyệt chi không được âm"],
    ["Chưa chọn Phòng ban chi (luồng Chi thu nhập nhân viên)", "Bắt buộc chọn phòng ban được chi"],
    ["Chưa nhập Lý do chi (luồng Chi thu nhập nhân viên)", "Bắt buộc nhập lý do chi"],
    ["Tỷ giá không phải số", "Tỷ giá phải là số"],
    ["Thiếu quyền Kế toán thanh toán", "Bạn không có quyền lập phiếu chi tiền"],
])

b.h2("8. Một phiếu đề nghị chỉ lập được một phiếu chi")
b.para(
    "Phiếu đề nghị thanh toán đã có phiếu chi thì biến mất khỏi cửa sổ chọn — kể cả khi phiếu "
    "chi đó mới chỉ là nháp. Hai kế toán bấm lưu cùng lúc cho cùng một phiếu đề nghị thì chỉ một "
    "người thành công, người còn lại bị chặn.")
b.para(
    "Nếu xoá phiếu chi nháp đi thì phiếu đề nghị xuất hiện trở lại trong cửa sổ chọn và lập được "
    "phiếu chi mới.")

# ══════════════════════════════════════════════════════════ PHẦN 5
b.h1("PHẦN 5: SỬA PHIẾU CHI")

b.h2("1. Điều kiện được sửa")
b.para("Chỉ sửa được phiếu thoả ĐỦ BA điều kiện:")
b.bullet("Phiếu đang ở trạng thái «Đang tạo».")
b.bullet("Người sửa là NGƯỜI LẬP phiếu đó.")
b.bullet("Người sửa có quyền «Kế toán thanh toán».")
b.para(
    "Thiếu một trong ba thì nút «Sửa» không hiện, và gõ thẳng đường dẫn màn Sửa cũng bị chặn. "
    "Vai trò quản trị hệ thống KHÔNG được miễn trừ ở đây.")
b.para(
    "ĐIỂM SIẾT CHẶT HƠN HỆ THỐNG CŨ: hệ thống cũ chỉ kiểm trạng thái, nên ai gọi được đường dẫn "
    "đều sửa được phiếu nháp của người khác.")

b.h2("2. Mở màn Sửa")
b.para("Có hai đường vào:")
b.bullet("Từ danh sách: cuộn ngang tới cột Hành động, bấm nút Sửa (biểu tượng bút chì).")
b.bullet("Từ màn chi tiết: bấm nút «Sửa» ở thanh nút cuối trang.")
b.image("22-sua-phieu.png", "Màn Sửa phiếu chi tiền với dữ liệu đã lưu")

b.h2("3. Khác biệt so với màn Tạo mới")
b.table([
    ["Điểm", "Màn Tạo mới", "Màn Sửa"],
    ["Tiêu đề", "Thêm phiếu chi tiền", "Sửa phiếu chi tiền"],
    ["Ô Mã phiếu", "Không có", "Có, ở chế độ chỉ đọc"],
    ["Ô Người lập", "Không có", "Có, ở chế độ chỉ đọc — là người lập phiếu gốc"],
    ["Ô Ngày lập", "Không có", "Có, ở chế độ chỉ đọc"],
    ["Bảng Chi tiết", "Trống cho tới khi chọn phiếu đề nghị hoặc phòng ban",
     "Nạp sẵn dữ liệu đã lưu"],
])

b.h2("4. Những gì sửa được")
b.bullet(
    "Đổi Loại chi — lưu ý đổi sang loại thuộc luồng khác thì cấu trúc form và bảng chi tiết đổi "
    "theo, dữ liệu cũ bị thay.")
b.bullet("Đổi sang phiếu đề nghị khác — bảng Chi tiết nạp lại theo phiếu mới.")
b.bullet(
    "Đổi Tài khoản có, Người nhận, Hình thức thanh toán, Tỷ giá, Lý do chi và thông tin ngân hàng.")
b.bullet("Đổi Tài khoản nợ, Số tiền chi và Ghi chú của từng dòng chi tiết.")
b.para(
    "Trường hợp đặc biệt: nếu tài khoản đang gắn với phiếu đã bị KHÓA trong danh mục, ô vẫn hiện "
    "đúng tên tài khoản đó để bạn không vô tình lưu đè mất giá trị cũ; nhưng khi mở danh sách "
    "chọn thì tài khoản đã khóa không nằm trong các lựa chọn mới.")

b.h2("5. Lưu phiếu sau khi sửa")
b.bullet(
    "«Lưu nháp»: giữ phiếu ở «Đang tạo», thông báo «Cập nhật phiếu chi tiền thành công!». Cột "
    "«Người cập nhật» và «Ngày cập nhật» trên danh sách đổi theo người vừa sửa.")
b.bullet(
    "«Lưu và gửi duyệt»: hỏi xác nhận rồi chuyển phiếu sang trạng thái chờ duyệt tương ứng luồng "
    "nghiệp vụ. Phiếu lập tức mất nút Sửa và Xóa.")
b.bullet("«Quay lại»: về danh sách, có hỏi nếu đang sửa dở.")

# ══════════════════════════════════════════════════════════ PHẦN 6
b.h1("PHẦN 6: XEM CHI TIẾT PHIẾU CHI")

b.h2("1. Mở màn chi tiết")
b.para("Bấm vào mã phiếu (chữ xanh gạch chân) ở cột «Mã phiếu» của dòng phiếu.")
b.image("15-chi-tiet-cho-chi-tien.png",
        "Màn chi tiết phiếu đang Chờ chi tiền, xem bằng tài khoản Thủ quỹ")

b.h2("2. Nội dung màn chi tiết")
b.para(
    "Tiêu đề màn ghi «Chi tiết phiếu chi: «mã phiếu»». Toàn bộ thông tin ở chế độ chỉ đọc.")
b.table([
    ["Khối", "Nội dung"],
    ["Dải băng lý do hủy", "CHỈ hiện với phiếu đã hủy — nền vàng ở ngay đầu màn, hiện «Lý do "
     "hủy» và «Ghi chú» mà người duyệt đã nhập khi hủy."],
    ["Thông tin chung",
     "Số phiếu đề nghị, Mã phiếu, Tài khoản có, Loại chi, Hình thức thanh toán, Người nhận, Loại "
     "tiền, Tỷ giá (VND), Người đề nghị, Phòng ban, Người lập, Ngày lập, Lý do chi."],
    ["Thông tin nhà cung cấp và ngân hàng",
     "Chỉ với phiếu hình thức chuyển khoản: Nhà cung cấp, Phí, khối «Ngân hàng nhận tiền» và "
     "«Ngân hàng trung gian»."],
    ["Chi tiết", "Bảng các dòng chi tiết kèm dòng «Tổng cộng»."],
    ["Lịch sử", "Khối thu gọn ở cuối trang. Xem chi tiết ở Phần 9."],
])
b.image("25-chi-tiet-da-xu-ly.png",
        "Màn chi tiết phiếu đã hủy — dải băng vàng hiện Lý do hủy và Ghi chú")

b.h2("3. Thanh nút cuối màn chi tiết")
b.table([
    ["Nút", "Điều kiện hiện"],
    ["Sửa", "Phiếu «Đang tạo», do chính mình lập, có quyền Kế toán thanh toán."],
    ["Duyệt phiếu chi", "Phiếu đang chờ đúng cấp duyệt của người xem, cùng công ty."],
    ["Hủy phiếu chi", "Cùng điều kiện với nút «Duyệt phiếu chi»."],
    ["In", "Xem được phiếu."],
    ["Xuất Excel", "Xem được phiếu."],
    ["Xóa", "Cùng điều kiện với nút «Sửa»."],
    ["Quay lại", "Luôn hiện."],
])

# ══════════════════════════════════════════════════════════ PHẦN 7
b.h1("PHẦN 7: DUYỆT PHIẾU CHI")

b.h2("1. Cảnh báo trước khi làm")
b.para(
    "Bước THỦ QUỸ duyệt là thao tác KHÔNG HOÀN TÁC ĐƯỢC: ngay khi bấm, hệ thống ghi bút toán "
    "vào sổ kế toán. Không có chức năng gỡ bút toán hay «bỏ duyệt». Hãy kiểm tra kỹ số tiền thực "
    "chi của từng dòng trước khi bấm.")
b.para(
    "Bước KẾ TOÁN TRƯỞNG duyệt thì an toàn hơn: chỉ chuyển phiếu sang «Chờ chi tiền», CHƯA ghi "
    "một dòng sổ kế toán nào.")

b.h2("2. Hai cấp duyệt và một nút Duyệt")
b.para("Vòng đời phiếu chi theo từng luồng:")
b.table([
    ["Luồng", "Vòng đời"],
    ["Lập từ Đề nghị thanh toán",
     "Đang tạo → Chờ chi tiền → (Thủ quỹ duyệt) → Đã duyệt · hoặc → Hủy"],
    ["Chi thu nhập cho nhân viên",
     "Đang tạo → Chờ KT trưởng duyệt → (Kế toán trưởng duyệt) → Chờ chi tiền → (Thủ quỹ duyệt) → "
     "Đã duyệt · hoặc → Hủy ở bất kỳ cấp nào đang chờ"],
])
b.para(
    "Giao diện chỉ có MỘT nút «Duyệt phiếu chi». Hệ thống tự biết đang duyệt ở cấp nào theo "
    "trạng thái phiếu:")
b.bullet(
    "Phiếu «Chờ KT trưởng duyệt» → cần quyền «Kế toán trưởng duyệt phiếu chi». Người chỉ có "
    "quyền Thủ quỹ mở phiếu này sẽ KHÔNG thấy nút.")
b.bullet(
    "Phiếu «Chờ chi tiền» → cần quyền «Thủ quỹ duyệt phiếu chi». Người chỉ có quyền Kế toán "
    "trưởng mở phiếu này cũng KHÔNG thấy nút.")
b.bullet("Cả hai cấp đều bắt buộc CÙNG CÔNG TY với phiếu.")

b.h2("3. Các bước duyệt")
b.para("1. Mở màn chi tiết của phiếu đang chờ duyệt.")
b.para("2. Bấm nút «Duyệt phiếu chi» (màu xanh) ở thanh nút cuối trang.")
b.para(
    "3. Cửa sổ «Duyệt phiếu chi tiền» mở ra, phụ đề ghi «Phiếu chi: «mã phiếu»», hiện lại bảng "
    "chi tiết với cột «Số tiền thực chi» là ô nhập (có dấu sao đỏ).")
b.image("16-popup-duyet.png", "Cửa sổ Duyệt phiếu chi tiền")
b.para("4. Kiểm tra và điều chỉnh «Số tiền thực chi» của từng dòng nếu cần.")
b.para("5. Nhập «Ghi chú» của người duyệt (không bắt buộc, tối đa 500 ký tự).")
b.para("6. Bấm «Duyệt» để xác nhận, hoặc «Đóng» để thoát mà không duyệt.")
b.para("Kết quả sau khi duyệt:")
b.table([
    ["Cấp duyệt", "Kết quả"],
    ["Kế toán trưởng",
     "Phiếu chuyển sang «Chờ chi tiền». CHƯA ghi bút toán. Thủ quỹ cùng công ty nhận thông báo."],
    ["Thủ quỹ",
     "Phiếu chuyển sang «Đã duyệt», ghi người duyệt và ngày hạch toán. Hệ thống ghi bút toán vào "
     "sổ kế toán và cập nhật ngược trạng thái phiếu đề nghị thanh toán. Thông báo «Duyệt phiếu "
     "chi thành công!»."],
])
b.para("Quy tắc kiểm tra khi duyệt:")
b.bullet(
    "«Số tiền thực chi» của một dòng KHÔNG được vượt số tiền đề nghị chi của chính dòng đó. Vượt "
    "thì hệ thống báo số tiền chi không được vượt quá số dư và chặn cả phiếu.")
b.bullet(
    "Với luồng Chi thu nhập nhân viên, dòng có số dư ÂM vẫn chi được: hệ thống so trần theo giá "
    "trị tuyệt đối của số dư.")
b.bullet("Số tiền thực chi không được âm.")
b.para(
    "Nếu hai người cùng bấm Duyệt một phiếu, chỉ người bấm trước thành công; người sau nhận "
    "thông báo «Phiếu chi đã được duyệt trước đó.» và sổ kế toán KHÔNG bị ghi trùng. Thông báo "
    "này khác hẳn thông báo thiếu quyền, để bạn không phải đi tìm xem quyền có bị thu hồi không.")

b.h2("4. Ghi chú của người duyệt lưu ở đâu")
b.para(
    "Ghi chú bạn nhập trong cửa sổ Duyệt KHÔNG hiện trên phiếu mà được lưu vào Lịch sử thay đổi, "
    "trong dòng đổi trạng thái tương ứng. Đây là điểm cải tiến so với hệ thống cũ — hệ thống cũ "
    "có ô này nhưng chữ gõ vào bị mất.")

# ══════════════════════════════════════════════════════════ PHẦN 8
b.h1("PHẦN 8: HỦY PHIẾU CHI VÀ XOÁ PHIẾU")

b.h2("1. Hủy phiếu chi")
b.para(
    "Chỉ người có quyền duyệt ở ĐÚNG CẤP đang chờ mới hủy được, và phải cùng công ty với phiếu. "
    "Người lập KHÔNG tự hủy được phiếu đã gửi duyệt.")
b.para("Các bước:")
b.para("1. Mở màn chi tiết của phiếu đang chờ duyệt.")
b.para("2. Bấm nút «Hủy phiếu chi» (màu đỏ) ở thanh nút cuối trang.")
b.image("17-popup-huy.png", "Cửa sổ Hủy phiếu chi tiền")
b.para("3. Nhập «Lý do hủy» — BẮT BUỘC, tối đa 500 ký tự.")
b.para("4. Nhập «Ghi chú» nếu cần — không bắt buộc, tối đa 500 ký tự.")
b.para("5. Bấm «Xác nhận» để hủy, hoặc «Đóng» để thoát mà không hủy.")
b.para("Kết quả sau khi xác nhận:")
b.bullet("Thông báo «Hủy phiếu chi thành công!».")
b.bullet("Phiếu chuyển sang trạng thái «Hủy».")
b.bullet(
    "Màn chi tiết xuất hiện dải băng vàng ở đầu trang hiện lại Lý do hủy và Ghi chú.")
b.bullet("Lịch sử thay đổi có thêm một dòng đổi trạng thái kèm lý do hủy.")
b.bullet("KHÔNG có bút toán nào được ghi vào sổ kế toán.")
b.para("Nếu bấm «Xác nhận» khi ô Lý do hủy còn trống:")
b.bullet("Ô viền đỏ, dưới ô hiện chữ đỏ «Lý do hủy – Bắt buộc nhập».")
b.bullet("Cửa sổ KHÔNG đóng, phiếu giữ nguyên trạng thái.")
b.image("18-loi-ly-do-huy.png", "Lỗi khi bấm Xác nhận lúc chưa nhập lý do hủy")

b.h2("2. Xoá phiếu chi")
b.para(
    "Chỉ xoá được phiếu ở trạng thái «Đang tạo» DO CHÍNH MÌNH lập và người xoá phải có quyền «Kế "
    "toán thanh toán» — đúng bằng điều kiện Sửa. Phiếu đã gửi duyệt, đã duyệt hoặc đã hủy đều "
    "không có nút Xóa.")
b.para("Các bước:")
b.para("1. Bấm nút Xóa (thùng rác đỏ) trên dòng, hoặc nút «Xóa» ở màn chi tiết.")
b.para("2. Hộp «Xác nhận xóa» hiện ra, nêu rõ mã phiếu.")
b.image("21-xac-nhan-xoa.png", "Hộp Xác nhận xóa phiếu chi")
b.para("3. Bấm «Xóa» để xoá, hoặc «Hủy» để giữ lại.")
b.para(
    "Kết quả: thông báo «Xóa phiếu chi thành công!», dòng biến mất khỏi danh sách. Xoá phiếu kéo "
    "theo toàn bộ dòng chi tiết; đây là xoá thật, không khôi phục lại được. Sau khi xoá, phiếu "
    "đề nghị gắn với phiếu chi đó xuất hiện trở lại trong cửa sổ chọn.")

b.h2("3. Phân biệt Hủy và Xoá")
b.table([
    ["", "Hủy phiếu chi", "Xoá phiếu chi"],
    ["Ai làm được", "Người duyệt ở cấp đang chờ, cùng công ty", "Người lập phiếu, có quyền Kế "
     "toán thanh toán"],
    ["Trạng thái phiếu", "Chờ KT trưởng duyệt hoặc Chờ chi tiền", "Đang tạo"],
    ["Bắt buộc nhập lý do", "Có", "Không (chỉ xác nhận)"],
    ["Phiếu còn trong hệ thống?", "Còn, chuyển sang trạng thái Hủy", "Mất hẳn"],
    ["Ghi vào Lịch sử", "Có, kèm lý do hủy", "Có, kèm ảnh chụp nội dung phiếu trước khi xoá"],
])

# ══════════════════════════════════════════════════════════ PHẦN 9
b.h1("PHẦN 9: IN PHIẾU, XUẤT EXCEL VÀ LỊCH SỬ")

b.h2("1. In phiếu")
b.para(
    "Có hai đường: bấm nút In trên dòng danh sách, hoặc bấm «In» ở màn chi tiết. Cả hai đều mở "
    "TAB MỚI hiển thị bản in và trình duyệt tự mở hộp thoại in. Đóng hộp thoại vẫn xem được bản "
    "in trên trang; muốn in lại thì bấm nút «In» ở góc trên bên trái trang.")
b.image("23-man-in.png",
        "Bản in phiếu chi loại Chi thu nhập cho nhân viên — có thêm 2 bảng kê")
b.para("Bản in gồm ĐỦ 2 LIÊN, mỗi liên có:")
b.table([
    ["Vị trí", "Nội dung"],
    ["Đầu trang", "Ảnh tiêu đề thư của công ty (logo, tên, địa chỉ, điện thoại, email, website)."],
    ["Tiêu đề", "«PHIẾU CHI», dưới là ngày viết bằng chữ."],
    ["Góc phải tiêu đề", "«Liên số», «Quyển số», số phiếu, dòng «Nợ:» và «Có:» kèm số tiền."],
    ["Thông tin đầu phiếu",
     "Họ và tên người nhận tiền, Phòng ban, Lý do chi, Số tiền thực chi, dòng «Bằng chữ»."],
    ["Khối ô ký", "Năm ô: BAN GIÁM ĐỐC, KẾ TOÁN TRƯỞNG, NGƯỜI NHẬN TIỀN, NGƯỜI LẬP PHIẾU, "
     "THỦ QUỸ."],
])
b.para(
    "RIÊNG phiếu loại «Chi thu nhập cho nhân viên» có THÊM hai bảng kê ở cuối bản in:")
b.bullet(
    "«BẢNG KÊ CHI TIẾT SỐ TIỀN CHI» — cột STT, Nhân viên, Số dư, Số tiền chi.")
b.bullet(
    "«BẢNG KÊ CHI TIẾT THEO VỤ VIỆC» — cột STT, Nhân viên và 6 khoản thu nhập: Thưởng thực hiện "
    "hợp đồng, Thưởng năng suất tháng, Thưởng năng suất quý, Thưởng thêm, Tiền vận chuyển, Chi "
    "phí khác, kèm cột Tổng cộng.")
b.para("In phiếu không làm thay đổi trạng thái, người cập nhật hay lịch sử của phiếu.")

b.h2("2. Xuất Excel")
b.para(
    "Bấm nút «Xuất Excel» ở màn chi tiết, hoặc nút cùng tên trên dòng danh sách. Hệ thống tải về "
    "tệp chứa ĐÚNG MỘT phiếu vừa chọn.")
b.para(
    "Lưu ý: màn này KHÔNG có chức năng xuất Excel cả danh sách — mỗi lần chỉ xuất được một phiếu.")

b.h2("3. Lịch sử thay đổi")
b.para("Nội dung hai nơi giống hệt nhau, chọn nơi nào tiện hơn:")
b.bullet(
    "Từ danh sách: cuộn ngang tới cột Hành động, bấm nút Lịch sử (đồng hồ quay ngược).")
b.bullet(
    "Từ màn chi tiết: cuộn xuống khối «Lịch sử» ở cuối trang rồi bấm «Xem lịch sử». Khối bung ra "
    "ngay trong trang, nút đổi thành «Thu gọn».")
b.image("20-lich-su.png", "Cửa sổ Lịch sử thay đổi mở từ danh sách")
b.image("19-lich-su-man-chi-tiet.png", "Khối Lịch sử ở cuối màn chi tiết")
b.para("Các mốc xếp theo thời gian, mới nhất ở trên. Mỗi mốc gồm:")
b.bullet("Ngày giờ xảy ra thay đổi.")
b.bullet("Loại thao tác: «Tạo mới», «Thay đổi thông tin», hoặc «Thay đổi trạng thái».")
b.bullet("Dòng «Người thực hiện: Họ tên — Phòng ban».")
b.bullet(
    "Với «Thay đổi thông tin»: liệt kê từng trường bị đổi kèm giá trị cũ và giá trị mới.")
b.bullet(
    "Với «Thay đổi trạng thái»: ghi bằng TÊN trạng thái, ví dụ «Chờ chi tiền → Hủy», kèm Ghi chú "
    "của người duyệt và (với thao tác hủy) dòng nền vàng chứa lý do hủy.")
b.para("Hệ thống ghi lịch sử ở các thời điểm sau:")
b.table([
    ["Thao tác", "Lịch sử ghi lại"],
    ["Lập phiếu", "Một mốc «Tạo mới» kèm ảnh chụp toàn bộ nội dung."],
    ["Sửa phiếu", "Một mốc «Thay đổi thông tin» liệt kê các trường đã đổi."],
    ["Gửi duyệt", "Một mốc đổi trạng thái sang cấp chờ duyệt tương ứng."],
    ["Kế toán trưởng duyệt", "Một mốc «Chờ KT trưởng duyệt → Chờ chi tiền», kèm ghi chú nếu có."],
    ["Thủ quỹ duyệt", "Một mốc «Chờ chi tiền → Đã duyệt», kèm ghi chú và thông tin đã ghi bút "
     "toán."],
    ["Hủy phiếu", "Một mốc đổi trạng thái sang «Hủy», kèm ĐÚNG lý do hủy và ghi chú đã nhập."],
    ["Xoá phiếu", "Một mốc xoá kèm ảnh chụp nội dung phiếu trước khi xoá."],
])
b.para(
    "Nút «Bộ lọc» cho phép lọc theo nhóm thao tác. Phiếu cũ chuyển từ hệ thống trước, chưa từng "
    "thao tác trên hệ thống mới, sẽ hiện dòng «Chưa có lịch sử thao tác nào.». Xem lịch sử không "
    "cần quyền riêng.")

# ══════════════════════════════════════════════════════════ PHẦN 10
b.h1("PHẦN 10: HƯỚNG DẪN THEO TỪNG VAI TRÒ")

b.h2("1. Người dùng không có quyền nào")
b.para("Nhìn thấy: chỉ phiếu chi do chính mình lập, ở mọi trạng thái.")
b.para("Làm được: xem chi tiết, in, xuất Excel, xem lịch sử các phiếu của mình.")
b.para(
    "Không làm được: không lập được phiếu mới (cửa sổ chọn phiếu đề nghị và bảng thu nhập nhân "
    "viên đều bị từ chối); không có nút Duyệt và Hủy.")

b.h2("2. Kế toán thanh toán (quyền «Kế toán thanh toán»)")
b.para("Đây là vai trò LẬP phiếu chi. Làm được:")
b.bullet(
    "Bấm «Tạo mới», chọn loại chi, mở cửa sổ chọn phiếu đề nghị hoặc chọn phòng ban để nạp số "
    "liệu thu nhập nhân viên.")
b.bullet("Lưu nháp hoặc Lưu và gửi duyệt.")
b.bullet("Sửa và xoá phiếu «Đang tạo» DO CHÍNH MÌNH lập.")
b.bullet("Xem chi tiết, in, xuất Excel, xem lịch sử.")
b.para(
    "Không làm được: không có nút «Duyệt phiếu chi» và «Hủy phiếu chi» — kể cả với phiếu do "
    "chính mình lập. Cũng không sửa/xoá được phiếu nháp của người khác.")

b.h2("3. Kế toán trưởng (quyền «Kế toán trưởng duyệt phiếu chi»)")
b.para(
    "Đây là cấp duyệt THỨ NHẤT, chỉ áp dụng với loại «Chi thu nhập cho nhân viên». Làm được, với "
    "phiếu ở trạng thái «Chờ KT trưởng duyệt» và cùng công ty:")
b.bullet("Bấm «Duyệt phiếu chi» — phiếu chuyển sang «Chờ chi tiền», CHƯA ghi sổ kế toán.")
b.bullet("Bấm «Hủy phiếu chi» kèm lý do.")
b.para(
    "Không làm được: không thấy nút Duyệt/Hủy ở phiếu «Chờ chi tiền» (trạng thái đó thuộc về Thủ "
    "quỹ). Nếu không kiêm quyền «Kế toán thanh toán» thì cũng không lập được phiếu mới.")

b.h2("4. Thủ quỹ (quyền «Thủ quỹ duyệt phiếu chi»)")
b.para(
    "Đây là cấp duyệt CUỐI. Làm được, với phiếu ở trạng thái «Chờ chi tiền» và cùng công ty:")
b.bullet(
    "Bấm «Duyệt phiếu chi», xác nhận số tiền thực chi từng dòng — hệ thống ghi bút toán vào sổ "
    "kế toán và cập nhật ngược trạng thái phiếu đề nghị thanh toán.")
b.bullet("Bấm «Hủy phiếu chi» kèm lý do.")
b.para("Nhận thông báo trên chuông mỗi khi có phiếu chi chuyển sang «Chờ chi tiền».")
b.para(
    "Không làm được: không thấy nút Duyệt/Hủy ở phiếu «Chờ KT trưởng duyệt»; không sửa, không "
    "xoá phiếu của người khác.")

b.h2("5. Cấp công ty và cấp tổng công ty")
b.para(
    "Hai quyền «Xem tất cả phiếu chi của công ty» và «Xem tất cả phiếu chi của tổng công ty» CHỈ "
    "mở rộng phạm vi nhìn. Muốn lập phiếu vẫn phải có «Kế toán thanh toán», muốn duyệt vẫn phải "
    "có quyền duyệt tương ứng. Nháp của người khác vẫn bị ẩn.")

# ══════════════════════════════════════════════════════════ PHẦN 11
b.h1("PHẦN 11: CÁC LỖI THƯỜNG GẶP VÀ CÁCH XỬ LÝ")
b.table([
    ["Hiện tượng", "Nguyên nhân", "Cách xử lý"],
    ["Vào màn thấy thiếu phiếu so với lần trước",
     "Bộ lọc của lần trước vẫn còn (hệ thống ghi nhớ 10 phút).",
     "Bấm nút «Làm mới» rồi xem lại."],
    ["Gõ vào ô tìm nhanh mà danh sách không đổi",
     "Ô tìm nhanh không tự tìm khi gõ.",
     "Bấm nút «Tìm kiếm» hoặc nhấn Enter."],
    ["Bấm ô «Số phiếu đề nghị» thì bị báo không có quyền",
     "Thiếu quyền «Kế toán thanh toán».",
     "Liên hệ quản trị; hoặc nhờ kế toán thanh toán lập phiếu."],
    ["Chọn phòng ban mà bảng thu nhập nhân viên trống",
     "Phòng ban chưa có số liệu thu nhập trong kỳ, hoặc thiếu quyền «Kế toán thanh toán».",
     "Kiểm tra lại kỳ số liệu; nếu bị báo không có quyền thì liên hệ quản trị."],
    ["Không tìm thấy phiếu đề nghị cần lập trong cửa sổ chọn",
     "Phiếu chưa gửi duyệt, hoặc đã có phiếu chi khác (kể cả phiếu chi đang là nháp).",
     "Kiểm tra trạng thái phiếu đề nghị ở màn Đề nghị thanh toán."],
    ["Chọn Loại chi xong thì ô «Số phiếu đề nghị» biến mất",
     "Đã chọn loại «Chi thu nhập cho nhân viên» — loại này không lập từ đề nghị.",
     "Chọn «Phòng ban chi» thay thế; nếu chọn nhầm loại thì đổi lại."],
    ["Không thấy nút Sửa / Xóa trên phiếu của mình",
     "Phiếu đã rời trạng thái «Đang tạo», hoặc thiếu quyền «Kế toán thanh toán».",
     "Phiếu đã gửi duyệt chỉ người duyệt mới xử lý được."],
    ["Không thấy nút «Duyệt phiếu chi» dù có quyền duyệt",
     "Phiếu đang chờ cấp duyệt KHÁC, hoặc phiếu khác công ty với bạn.",
     "Kiểm tra lại trạng thái và công ty của phiếu."],
    ["Bấm Duyệt thì báo số tiền chi vượt quá số dư",
     "Số tiền thực chi của một dòng lớn hơn số tiền đề nghị chi của dòng đó.",
     "Sửa lại cho nhỏ hơn hoặc bằng rồi bấm Duyệt."],
    ["Bấm Duyệt thì báo «Phiếu chi đã được duyệt trước đó.»",
     "Người khác vừa duyệt phiếu này trước bạn.",
     "Tải lại màn để xem kết quả; sổ kế toán không bị ghi trùng."],
    ["Kế toán trưởng duyệt xong mà sổ kế toán vẫn trống",
     "Đúng thiết kế — chỉ bước Thủ quỹ mới ghi sổ.",
     "Chờ Thủ quỹ duyệt tiếp."],
    ["Lưu nháp mà bị báo lỗi",
     "Chưa chọn «Loại chi» — đây là trường duy nhất bắt buộc kể cả khi lưu nháp.",
     "Chọn loại chi rồi lưu lại."],
    ["Đã nhập Ghi chú khi duyệt nhưng không thấy trên phiếu",
     "Ghi chú của người duyệt được lưu vào Lịch sử thay đổi, không hiện trên phiếu.",
     "Mở khối Lịch sử ở cuối màn chi tiết để xem."],
    ["Không mở được phiếu của đồng nghiệp",
     "Không phải người lập, không phải người đã duyệt, không có quyền duyệt cấp đang chờ, và "
     "không có quyền xem theo công ty hoặc tổng công ty.",
     "Liên hệ quản trị để được cấp quyền xem phù hợp."],
])

b.finish()
