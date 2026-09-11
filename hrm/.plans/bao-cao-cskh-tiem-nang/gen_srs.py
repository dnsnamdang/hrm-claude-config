# -*- coding: utf-8 -*-
"""Sinh "SRS - Bao cao ket qua cham soc khach hang tiem nang.docx" theo FORM CHUAN
(ban mau doi ngay 2026-08-17: 4 chuong).

Chay:  python3 .plans/bao-cao-cskh-tiem-nang/gen_srs.py
Thu vien dung chung: .claude/skills/srs-documenter/assets/{srs_docx_lib,srs_uml_render}.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "..", ".claude", "skills", "srs-documenter", "assets")
sys.path.insert(0, ASSETS)

# Thu vien ve UML cua skill tro cung font Windows (C:\Windows\Fonts\segoeui.ttf).
# May dang lam la macOS -> tro lai font he thong CO DU DAU TIENG VIET, KHONG sua file
# dung chung trong .claude/skills/.
import srs_uml_render as uml  # noqa: E402

if not os.path.exists(uml.F_REG):
    _MAC = "/System/Library/Fonts/Supplemental"
    for _attr, _name in (("F_REG", "Arial.ttf"), ("F_BOLD", "Arial Bold.ttf"),
                         ("F_ITAL", "Arial Italic.ttf")):
        _path = os.path.join(_MAC, _name)
        if os.path.exists(_path):
            setattr(uml, _attr, _path)

from srs_docx_lib import SrsDoc  # noqa: E402

OUT = os.path.join(HERE, "SRS - Báo cáo kết quả chăm sóc khách hàng tiềm năng.docx")
SHOTS = os.path.join(HERE, "bao-cao-cskh_shots")
ROUTE = "/assign/report/potential-customer-care"
FULL_URL = "https://hrm.eteksofts.com/assign/report/potential-customer-care"

ACTOR_KD = "Nhân viên kinh doanh / Trưởng phòng kinh doanh"
ACTOR_QL = "Ban lãnh đạo, Trưởng phòng"
ACTOR_HT = "Hệ thống (tác vụ định kỳ)"


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(out=OUT, menu="Báo cáo ▸ Kết quả CSKH tiềm năng", route=ROUTE, full_url=FULL_URL)

d.title_block("Báo cáo kết quả chăm sóc khách hàng tiềm năng")
d.h2("Mục lục")
d.toc()

# ==================================================== PHẦN 1
d.h1("Phần 1. Giới thiệu")

d.h2("1. Mục đích")
d.p("Tài liệu đặc tả màn hình “Báo cáo kết quả chăm sóc khách hàng tiềm năng” của phân hệ Dự án & "
    "Giao việc. Màn hình phục vụ các mục tiêu sau:")
d.bullets([
    "Tổng hợp toàn bộ nhu cầu đầu tư mà kinh doanh thu thập được qua meeting “Họp tìm hiểu & Giới "
    "thiệu sản phẩm” trong một kỳ báo cáo.",
    "Theo dõi vòng đời của từng nhu cầu: đang theo dõi, đã chuyển đổi thành dự án tiền khả thi, "
    "hoặc hết hạn không tiếp tục.",
    "Đo tỷ lệ chuyển đổi nhu cầu thành dự án tiền khả thi qua ba chỉ tiêu KPI.",
    "Bóc tách kết quả theo ba cơ cấu: Lĩnh vực kinh doanh ▸ Nhóm ngành, Tỉnh/Thành phố ▸ Phường/xã, "
    "Phòng ban ▸ Nhân viên chủ trì.",
    "Cho phép đi từ mỗi con số tổng hợp xuống danh sách nhu cầu chi tiết, in và xuất tệp Excel theo "
    "đúng phạm vi đang xem.",
])

d.h2("2. Thuật ngữ và viết tắt")
d.table(["Thuật ngữ", "Mô tả"], [
    ("Nhu cầu đầu tư", "Một dòng trong biên bản meeting, ghi lại việc khách hàng có nhu cầu đầu tư "
     "vào một nhóm ngành cụ thể, kèm giá trị đầu tư dự kiến và thời gian dự kiến triển khai. Một "
     "meeting có thể sinh nhiều nhu cầu."),
    ("Dự án TKT", "Dự án tiền khả thi — bước tiếp theo sau khi nhu cầu của khách được xác nhận là "
     "khả thi để theo đuổi."),
    ("Kỳ báo cáo", "Khoảng thời gian từ ngày đầu kỳ đến ngày cuối kỳ, do người dùng chọn: Tháng "
     "này, Quý này, Năm nay hoặc Tuỳ chỉnh."),
    ("Ngày họp", "Ngày diễn ra meeting thu thập nhu cầu; dùng để xác định nhu cầu phát sinh trong kỳ."),
    ("Ngày đóng", "Ngày một nhu cầu ngừng được theo dõi, do đã lập dự án TKT hoặc do quá thời gian "
     "dự kiến triển khai."),
    ("Tiêu chí theo dõi", "Cách bổ dọc số liệu thành các phần của bảng theo dõi: Tất cả, Lĩnh vực "
     "kinh doanh / Nhóm ngành, Thị trường, hoặc Phòng ban / Nhân viên."),
    ("Cửa sổ chi tiết", "Cửa sổ bật lên khi bấm vào một con số bất kỳ trên màn, liệt kê từng nhu cầu "
     "tạo nên con số đó."),
    ("Chỉ tiêu I / II", "I là “Tổng nhu cầu trong kỳ”, II là “Tổng nhu cầu bị đóng trong kỳ”."),
], widths=[1.5, 4.5])

# ==================================================== PHẦN 2
d.h1("Phần 2. Phân quyền")

d.h2("1. Danh sách quyền")
d.p("Nhóm quyền thao tác:")
d.table(["Ký hiệu", "Tên quyền", "Tác dụng trên màn hình"], [
    ("Q1", "Quản lý dự án tiền khả thi",
     "Hiển thị nút “+ Tạo mới” ở từng dòng trong cửa sổ chi tiết, cho phép chuyển sang màn tạo dự "
     "án tiền khả thi từ một nhu cầu. Thiếu quyền này thì nút bị ẩn hoàn toàn."),
], widths=[0.7, 2.1, 3.2])

d.p("Nhóm quyền quyết định phạm vi dữ liệu:")
d.table(["Ký hiệu", "Tên quyền", "Phạm vi dữ liệu"], [
    ("V1", "Xem báo cáo kết quả chăm sóc khách hàng tiềm năng theo tổng công ty",
     "Thấy nhu cầu của mọi công ty trong tập đoàn. Hiển thị thêm ô lọc “Công ty”."),
    ("V2", "Xem báo cáo kết quả chăm sóc khách hàng tiềm năng theo công ty",
     "Chỉ thấy nhu cầu thuộc công ty của người đăng nhập."),
    ("V3", "Xem báo cáo kết quả chăm sóc khách hàng tiềm năng theo phòng ban",
     "Chỉ thấy nhu cầu thuộc các phòng ban mà người đăng nhập được phân công quản lý."),
    ("—", "Không có quyền nào trong V1, V2, V3",
     "Vẫn vào được màn hình nhưng chỉ thấy nhu cầu từ meeting do chính mình chủ trì hoặc mình có "
     "tham dự."),
], widths=[0.7, 2.1, 3.2])

d.h2("2. Ma trận phân quyền")
d.table(["Chức năng", "Q1", "V1", "V2", "V3", "Không có quyền nào"], [
    ("FR-01 Xem báo cáo tổng hợp", "—", "✅", "✅", "✅", "✅ (chỉ meeting của mình)"),
    ("FR-02 Lọc báo cáo", "—", "✅", "✅", "✅", "✅ (chỉ meeting của mình)"),
    ("FR-03 Xem danh sách nhu cầu chi tiết", "—", "✅", "✅", "✅", "✅ (chỉ meeting của mình)"),
    ("FR-04 Lọc và thống kê nhanh trong danh sách chi tiết", "—", "✅", "✅", "✅",
     "✅ (chỉ meeting của mình)"),
    ("FR-05 In báo cáo", "—", "✅", "✅", "✅", "✅ (chỉ meeting của mình)"),
    ("FR-06 Xuất tệp Excel", "—", "✅", "✅", "✅", "✅ (chỉ meeting của mình)"),
    ("FR-07 Tạo dự án tiền khả thi từ nhu cầu", "✅", "—", "—", "—", "❌"),
    ("FR-08 Tự động đóng nhu cầu hết hạn theo dõi", "—", "—", "—", "—",
     "Hệ thống tự chạy, không phụ thuộc quyền người dùng"),
], widths=[2.1, 0.4, 0.4, 0.4, 0.4, 2.3])
d.p("Ghi chú: ba quyền V1, V2, V3 không chặn việc mở màn hình mà chỉ thu hẹp phạm vi dữ liệu nhìn "
    "thấy. Người dùng không có quyền nào vẫn mở được màn hình và thấy phần dữ liệu của chính mình.")

# ==================================================== PHẦN 3
d.h1("Phần 3. Đặc tả chi tiết theo từng chức năng")

d.h2("1. Sơ đồ UML tổng quan")
d.overview_figure(
    "HỆ THỐNG HRM — BÁO CÁO KẾT QUẢ CHĂM SÓC KHÁCH HÀNG TIỀM NĂNG",
    [(ACTOR_QL, [0, 1, 2, 3, 4, 5]),
     (ACTOR_KD, [0, 1, 2, 3, 6]),
     (ACTOR_HT, [7])],
    [("FR-01", "Xem báo cáo tổng hợp", "view", None),
     ("FR-02", "Lọc báo cáo", "view", None),
     ("FR-03", "Xem danh sách nhu cầu chi tiết", "view", None),
     ("FR-04", "Lọc & thống kê nhanh", "view", None),
     ("FR-05", "In báo cáo", "io", None),
     ("FR-06", "Xuất tệp Excel", "io", None),
     ("FR-07", "Tạo dự án tiền khả thi", "crud", "«extend» chỉ khi có quyền Q1"),
     ("FR-08", "Tự động đóng nhu cầu hết hạn", "action", None)],
    "Sơ đồ Use Case tổng quan màn Báo cáo kết quả chăm sóc khách hàng tiềm năng")

d.h2("2. Đặc tả chi tiết từng chức năng")

# ---------------------------------------------------------------- 2.1
d.h3("2.1 Xem báo cáo tổng hợp")
d.p("2.1.1 Giới thiệu")
d.intro_table(
    ten="Xem báo cáo tổng hợp",
    mota="Hiển thị kết quả chăm sóc khách hàng tiềm năng của kỳ đang chọn gồm hai khối tổng hợp, ba "
         "ô kết quả KPI và bảng theo dõi tối đa ba phần hai cấp.",
    tacnhan="%s; %s; Người dùng đã đăng nhập" % (ACTOR_QL, ACTOR_KD),
    dieukien="Người dùng đã đăng nhập và mở màn hình từ menu Báo cáo ▸ Kết quả CSKH tiềm năng.",
    chinh="1. Người dùng mở màn hình.\n"
          "2. Hệ thống lấy kỳ mặc định là Tháng này và tiêu chí theo dõi mặc định là Tất cả.\n"
          "3. Hệ thống lọc tập nhu cầu theo phạm vi quyền của người dùng.\n"
          "4. Hệ thống tính hai khối tổng hợp, ba ô KPI và dựng bảng theo dõi.\n"
          "5. Màn hình hiển thị kết quả; mọi con số đều bấm được để mở danh sách chi tiết.",
    phu="• Kỳ không có nhu cầu nào: mọi ô hiển thị 0, ba ô KPI hiển thị 0,0%, bảng vẫn hiện đủ dòng "
        "tiêu đề phần với số 0.\n"
        "• Người dùng không có quyền phạm vi nào: chỉ thấy nhu cầu từ meeting mình chủ trì hoặc "
        "tham dự.\n"
        "• Nhu cầu thiếu thông tin phân nhóm: gom vào dòng “Chưa xác định …”, không bị loại khỏi tổng.",
    dacbiet=None)

d.p("2.1.2 Layout màn hình")
d.layout(shot=shot("01-bao-cao.png"),
         shot_caption="Hình 2: Màn hình Báo cáo kết quả chăm sóc khách hàng tiềm năng")

d.p("2.1.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Tiêu đề màn hình", "Label", "Hiển thị", "–", "Theo dữ liệu",
     "“Báo cáo kết quả chăm sóc khách hàng tiềm năng” trên thanh trên cùng."),
    ("Dòng tổng hợp kỳ", "Label", "Hiển thị", "–", "Theo dữ liệu",
     "“Tổng hợp kỳ dd/mm/yyyy – dd/mm/yyyy”, kèm tổng số nhu cầu và tổng giá trị đầu tư dự kiến."),
    ("Nút Thu gọn / Mở rộng", "Button", "Enable", "–", "“Thu gọn”",
     "Ẩn hoặc hiện hai khối tổng hợp và ba ô KPI để nhường chỗ cho bảng theo dõi."),
    ("Khối Tổng nhu cầu trong kỳ", "Text", "Hiển thị", "≥ 0", "Theo dữ liệu",
     "Số nhu cầu và giá trị của chỉ tiêu I. Bấm vào số để mở danh sách chi tiết."),
    ("Ô Tổng nhu cầu còn hiệu lực theo dõi", "Text", "Hiển thị", "≥ 0", "Theo dữ liệu",
     "Nhu cầu họp từ trước ngày đầu kỳ, tới đầu kỳ vẫn chưa bị đóng."),
    ("Ô Tổng nhu cầu phát sinh trong kỳ", "Text", "Hiển thị", "≥ 0", "Theo dữ liệu",
     "Nhu cầu có ngày họp nằm trong kỳ."),
    ("Khối Tổng nhu cầu bị đóng trong kỳ", "Text", "Hiển thị", "≥ 0", "Theo dữ liệu",
     "Số nhu cầu và giá trị của chỉ tiêu II."),
    ("Ô Chuyển đổi thành dự án TKT", "Text", "Hiển thị", "≥ 0", "Theo dữ liệu",
     "Nhu cầu đã lập dự án tiền khả thi, có ngày đóng nằm trong kỳ."),
    ("Ô Hết hạn, không tiếp tục", "Text", "Hiển thị", "≥ 0", "Theo dữ liệu",
     "Nhu cầu quá thời gian dự kiến triển khai mà chưa lập dự án, ngày đóng nằm trong kỳ."),
    ("Ô KPI Tỷ lệ chuyển đổi thành công", "Text", "Hiển thị", "0 – 100", "Theo dữ liệu",
     "Chuyển đổi thành dự án TKT chia Tổng nhu cầu trong kỳ, kèm tử số / mẫu số và thanh tiến độ."),
    ("Ô KPI Thành công / tổng nhu cầu đóng", "Text", "Hiển thị", "0 – 100", "Theo dữ liệu",
     "Chuyển đổi thành dự án TKT chia Tổng nhu cầu bị đóng trong kỳ."),
    ("Ô KPI Thất bại / tổng nhu cầu đóng", "Text", "Hiển thị", "0 – 100", "Theo dữ liệu",
     "Hết hạn không tiếp tục chia Tổng nhu cầu bị đóng trong kỳ."),
    ("Icon chữ i giải thích", "Icon Button", "Enable", "–", "Hiển thị",
     "Bung khung giải thích cách tính của chỉ tiêu tương ứng, có ghép số liệu thật của kỳ."),
    ("Bảng theo dõi", "Table/Grid", "Hiển thị", "–", "Theo dữ liệu",
     "Tám cột: STT, Nội dung theo dõi, Số nhu cầu, Giá trị dự kiến, Chuyển đổi thành công, Tỷ lệ "
     "thành công, Không tiếp tục, Tỷ trọng giá trị."),
    ("Dòng tiêu đề phần", "Label", "Hiển thị", "–", "Theo dữ liệu",
     "Ba phần I, II, III; dòng tiêu đề mang luôn số tổng của phần, không có dòng Tổng cộng riêng."),
    ("Nút Hiện chi tiết / Ẩn chi tiết", "Button", "Enable", "–", "“Hiện chi tiết”",
     "Bung hoặc thu toàn bộ cấp con của cả ba phần cùng lúc."),
    ("Mũi tên bung dòng cha", "Icon Button", "Enable", "–", "Thu",
     "Bung hoặc thu riêng cấp con của một dòng cha."),
    ("Con số bấm được", "Button", "Enable", "≥ 0", "Theo dữ liệu",
     "Mọi con số ở khối tổng hợp và trong bảng đều mở được cửa sổ danh sách chi tiết, kể cả số 0."),
    ("Thanh tỷ trọng giá trị", "Text", "Hiển thị", "0 – 100", "Theo dữ liệu",
     "Dòng cha so với tổng kỳ; dòng con so trong nội bộ dòng cha."),
    ("Trạng thái rỗng của bảng", "Label", "Hiển thị", "–", "Ẩn",
     "Kỳ không có dữ liệu thì các dòng tiêu đề phần vẫn hiện với số 0, không có dòng con."),
], required=False)

d.p("2.1.4 Danh sách event và xử lý event")
d.event_table([
    ("Mở màn hình", "System",
     "Before:\n– Xác định phạm vi dữ liệu theo quyền của người đăng nhập.\n"
     "During:\n– Lấy kỳ mặc định Tháng này và tiêu chí Tất cả.\n"
     "After:\n– Tính hai khối tổng hợp, ba ô KPI và dựng bảng theo dõi.\n"
     "– Hiển thị kết quả mà không cần người dùng bấm Tìm kiếm."),
    ("Bấm nút Thu gọn / Mở rộng", "Click",
     "After:\n– Ẩn hoặc hiện hai khối tổng hợp và ba ô KPI.\n– Đổi chữ trên nút tương ứng."),
    ("Bấm nút Hiện chi tiết", "Click",
     "After:\n– Bung toàn bộ cấp con của cả ba phần.\n– Đổi chữ trên nút thành “Ẩn chi tiết”."),
    ("Bấm mũi tên ở dòng cha", "Click",
     "After:\n– Bung hoặc thu cấp con của riêng dòng đó, các dòng cha khác giữ nguyên."),
    ("Bấm vào một con số", "Click",
     "After:\n– Mở cửa sổ danh sách nhu cầu chi tiết đúng phạm vi của con số vừa bấm.\n"
     "– Tiêu đề cửa sổ ghi tên chỉ tiêu hoặc tên dòng vừa bấm."),
    ("Rê chuột vào icon chữ i", "Hover",
     "After:\n– Bung khung giải thích cách tính của chỉ tiêu tương ứng."),
])

# ---------------------------------------------------------------- 2.2
d.h3("2.2 Lọc báo cáo")
d.p("2.2.1 Biểu đồ Usecase")
d.uc_figure("FR-02", "Lọc báo cáo", "view",
            [("include", "Xác định phạm vi dữ liệu theo quyền"),
             ("extend", "Hiện khối lọc riêng của tiêu chí đang chọn")],
            actor=ACTOR_QL,
            caption="Hình 3: Biểu đồ Use Case — FR-02 Lọc báo cáo")

d.p("2.2.2 Giới thiệu")
d.intro_table(
    ten="Lọc báo cáo",
    mota="Chọn kỳ báo cáo, tiêu chí theo dõi và các điều kiện lọc theo cơ cấu để thu hẹp phạm vi số "
         "liệu của toàn màn hình.",
    tacnhan="%s; %s; Người dùng đã đăng nhập" % (ACTOR_QL, ACTOR_KD),
    dieukien="Đang ở màn hình báo cáo.",
    chinh="1. Người dùng bấm nút “Hiện bộ lọc”.\n"
          "2. Người dùng chọn Kỳ báo cáo và Tiêu chí theo dõi.\n"
          "3. Hệ thống hiện khối lọc riêng ứng với tiêu chí vừa chọn và tải lại số liệu.\n"
          "4. Người dùng chọn thêm điều kiện lọc theo cơ cấu nếu cần.\n"
          "5. Người dùng bấm “Tìm kiếm”.\n"
          "6. Hệ thống tính lại hai khối tổng hợp, ba ô KPI và bảng theo dõi theo bộ lọc mới.",
    phu="• Chọn Kỳ báo cáo là “Tuỳ chỉnh” thì hiện thêm hai ô Từ ngày và Đến ngày.\n"
        "• Nhập Từ ngày lớn hơn Đến ngày: hệ thống tự đảo lại hai mốc thay vì trả kỳ rỗng.\n"
        "• Bỏ trống hai ô ngày ở kỳ Tuỳ chỉnh: hệ thống lấy mặc định là tháng hiện tại.\n"
        "• Đổi Tiêu chí theo dõi: hệ thống xoá giá trị của khối lọc không còn hiển thị.\n"
        "• Bấm “Xóa lọc”: mọi ô trở về mặc định và số liệu tải lại.",
    dacbiet="Ô lọc chỉ liệt kê những mục thật sự có dữ liệu trong kỳ đang xem, không đổ toàn bộ danh "
            "mục.")

d.p("2.2.3 Layout màn hình")
d.layout(shot=shot("02-bo-loc.png"), shot_caption="Hình 4: Khối bộ lọc đang mở")

d.p("2.2.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Nút Hiện bộ lọc / Ẩn bộ lọc", "Button", "Enable", "–", "–", "“Hiện bộ lọc”",
     "Mở hoặc đóng khối bộ lọc."),
    ("Kỳ báo cáo", "Dropdown", "Enable", "Danh sách 4 giá trị", "Có", "Tháng này",
     "Tháng này, Quý này, Năm nay, Tuỳ chỉnh. Không có lựa chọn “Tất cả”."),
    ("Từ ngày", "Datepicker", "Enable / Ẩn", "dd/mm/yyyy", "Không", "Trống",
     "Chỉ hiện khi Kỳ báo cáo là Tuỳ chỉnh. Bỏ trống thì lấy đầu tháng hiện tại."),
    ("Đến ngày", "Datepicker", "Enable / Ẩn", "dd/mm/yyyy", "Không", "Trống",
     "Chỉ hiện khi Kỳ báo cáo là Tuỳ chỉnh. Bỏ trống thì lấy cuối tháng hiện tại."),
    ("Tiêu chí theo dõi", "Dropdown", "Enable", "Danh sách 4 giá trị", "Có", "Tất cả",
     "Quyết định bảng dựng phần nào và khối lọc nào hiển thị."),
    ("Lĩnh vực công ty kinh doanh", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Trống",
     "Chỉ hiện khi tiêu chí là Lĩnh vực kinh doanh / Nhóm ngành. Là ô cha của Nhóm ngành."),
    ("Nhóm ngành", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Trống",
     "Lọc theo lĩnh vực đang chọn; đổi ô cha thì giá trị ở đây bị xoá."),
    ("Tỉnh / Thành phố", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Trống",
     "Chỉ hiện khi tiêu chí là Thị trường. Là ô cha của Phường / xã."),
    ("Phường / xã", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Trống",
     "Lọc theo tỉnh đang chọn; đổi ô cha thì giá trị ở đây bị xoá."),
    ("Công ty", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Trống",
     "Chỉ hiện với người có quyền V1. Là ô cha của Phòng ban."),
    ("Phòng ban", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Trống",
     "Chỉ hiện khi tiêu chí là Tất cả hoặc Phòng ban / Nhân viên. Là ô cha của Nhân viên."),
    ("Nhân viên", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Trống",
     "Lọc theo phòng ban đang chọn. Lọc theo người chủ trì meeting."),
    ("Nút Tìm kiếm", "Button", "Enable", "–", "–", "Hiển thị", "Áp dụng bộ lọc và tải lại số liệu."),
    ("Nút Xóa lọc", "Button", "Enable", "–", "–", "Hiển thị",
     "Đưa mọi ô về mặc định và tải lại số liệu."),
])

d.p("2.2.5 Danh sách event và xử lý event")
d.event_table([
    ("Đổi Kỳ báo cáo", "Change",
     "During:\n– Chọn “Tuỳ chỉnh” thì hiện thêm hai ô Từ ngày và Đến ngày.\n"
     "After:\n– Giữ nguyên số liệu cho tới khi người dùng bấm Tìm kiếm."),
    ("Đổi Tiêu chí theo dõi", "Change",
     "During:\n– Xoá giá trị của khối lọc không còn hiển thị để tránh lọc ngầm.\n"
     "After:\n– Hiện khối lọc riêng của tiêu chí mới.\n"
     "– Dựng lại bảng chỉ với phần tương ứng và tải lại số liệu ngay."),
    ("Đổi ô lọc cha (Lĩnh vực, Tỉnh/Thành phố, Công ty, Phòng ban)", "Change",
     "After:\n– Xoá giá trị của ô con tương ứng.\n– Thu hẹp danh sách lựa chọn của ô con."),
    ("Bấm Tìm kiếm", "Click",
     "Before:\n– Xác định phạm vi dữ liệu theo quyền của người đăng nhập.\n"
     "During:\n– Từ ngày lớn hơn Đến ngày → tự đảo lại hai mốc.\n"
     "– Bỏ trống hai ô ngày ở kỳ Tuỳ chỉnh → lấy tháng hiện tại.\n"
     "After:\n– Tính lại hai khối tổng hợp, ba ô KPI và bảng theo dõi.\n"
     "– Bộ lọc này áp dụng cho cả cửa sổ chi tiết, bản in và tệp Excel."),
    ("Bấm Xóa lọc", "Click",
     "After:\n– Đưa Kỳ báo cáo về Tháng này, Tiêu chí về Tất cả, các ô còn lại về trống.\n"
     "– Tải lại số liệu."),
])

# ---------------------------------------------------------------- 2.3
d.h3("2.3 Xem danh sách nhu cầu chi tiết")
d.p("2.3.1 Giới thiệu")
d.intro_table(
    ten="Xem danh sách nhu cầu chi tiết",
    mota="Mở cửa sổ liệt kê từng nhu cầu tạo nên con số vừa bấm, kèm khối kết quả KPI và khối phân "
         "bổ nhu cầu theo cơ cấu của chính tập đang xem.",
    tacnhan="%s; %s; Người dùng đã đăng nhập" % (ACTOR_QL, ACTOR_KD),
    dieukien="Đang ở màn hình báo cáo và đã có số liệu.",
    chinh="1. Người dùng bấm vào một con số bất kỳ trên khối tổng hợp hoặc trong bảng theo dõi.\n"
          "2. Hệ thống mở cửa sổ chi tiết với tiêu đề là tên chỉ tiêu hoặc tên dòng vừa bấm.\n"
          "3. Hệ thống tính khối KPI và khối phân bổ trên chính tập nhu cầu đang xem.\n"
          "4. Hệ thống hiển thị bảng chi tiết, thứ tự cột bám theo thứ tự hàng của khối phân bổ.",
    phu="• Bấm vào con số 0: cửa sổ vẫn mở, bảng hiện dòng “Không có nhu cầu nào khớp bộ lọc.”\n"
        "• Mở từ nhóm “Hết hạn, không tiếp tục”: cửa sổ bỏ hẳn khối kết quả KPI.\n"
        "• Mở theo một cơ cấu: ô lọc và hàng phân bổ của chính cơ cấu đó bị ẩn.\n"
        "• Bấm nút phóng to: cửa sổ phủ kín màn hình; bấm lại để thu nhỏ.",
    dacbiet=None)

d.p("2.3.2 Layout màn hình")
d.layout(modal="Danh sách nhu cầu chi tiết", shot=shot("03-popup.png"),
         shot_caption="Hình 5: Cửa sổ danh sách nhu cầu chi tiết")

d.p("2.3.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Tiêu đề cửa sổ", "Label", "Hiển thị", "–", "Theo dữ liệu",
     "Câu dẫn “Bạn đang xem kết quả CSKH tiềm năng:” và tên đối tượng in đậm."),
    ("Dòng tóm tắt", "Label", "Hiển thị", "–", "Theo dữ liệu",
     "Số nhu cầu, tổng giá trị và kỳ đang xem; có thêm “đang lọc trong n nhu cầu” khi đang lọc."),
    ("Nút phóng to / thu nhỏ", "Icon Button", "Enable", "–", "Thu nhỏ",
     "Phủ kín màn hình hoặc trở về kích thước thường."),
    ("Nút đóng", "Icon Button", "Enable", "–", "Hiển thị", "Đóng cửa sổ, trở về màn báo cáo."),
    ("Nút Thu gọn / Mở rộng", "Button", "Enable", "–", "“Thu gọn”",
     "Ẩn hoặc hiện khối KPI và khối phân bổ."),
    ("Số đếm nhu cầu", "Label", "Hiển thị", "–", "Theo dữ liệu",
     "Dạng “n / N nhu cầu”: n là số dòng sau khi lọc trong cửa sổ, N là tổng của tập đang xem."),
    ("Khối kết quả KPI", "Text", "Hiển thị", "0 – 100", "Theo dữ liệu",
     "Ba ô KPI tính trên chính tập đang xem. Ẩn hoàn toàn với nhóm “Hết hạn, không tiếp tục”."),
    ("Khối Phân bổ nhu cầu theo cơ cấu", "Text", "Hiển thị", "–", "Theo dữ liệu",
     "Tối đa ba hàng: Lĩnh vực KD, Thị trường, Phòng ban. Bỏ hàng của cơ cấu đang xem."),
    ("Bảng chi tiết", "Table/Grid", "Hiển thị", "–", "Theo dữ liệu",
     "Mỗi nhu cầu một dòng; thứ tự cột cơ cấu bám theo thứ tự hàng của khối phân bổ."),
    ("Cột Khách hàng", "Text", "Hiển thị", "–", "Theo dữ liệu", "Hiển thị cả mã và tên khách hàng."),
    ("Cột Giá trị đầu tư dự kiến", "Number", "Hiển thị", "≥ 0", "Theo dữ liệu",
     "Số đầy đủ có dấu phân cách hàng nghìn, không rút gọn theo tỷ như bảng theo dõi."),
    ("Cột Thời gian triển khai", "Text", "Hiển thị", "mm/yyyy", "Theo dữ liệu",
     "Chỉ hiển thị tháng và năm; để trống thì hiện dấu gạch."),
    ("Cột DV sửa chữa", "Text", "Hiển thị", "Danh sách 2 giá trị", "Theo dữ liệu",
     "“Có” hoặc “Không”; thông tin ở cấp meeting nên các nhu cầu cùng meeting có giá trị giống nhau."),
    ("Cột Meeting thu thập nhu cầu", "Text", "Hiển thị", "–", "Theo dữ liệu",
     "Mã và tên meeting sinh ra nhu cầu."),
    ("Cột Trạng thái", "Badge", "Hiển thị", "Danh sách 3 giá trị", "Theo dữ liệu",
     "Đang theo dõi, Đã lập dự án TKT, Không tiếp tục — mỗi trạng thái một màu riêng."),
    ("Cột Dự án TKT", "Text", "Hiển thị", "–", "Theo dữ liệu",
     "Mã và tên dự án đã gắn; để trống khi nhu cầu chưa chuyển đổi."),
    ("Trạng thái rỗng", "Label", "Hiển thị", "–", "Ẩn",
     "“Không có nhu cầu nào khớp bộ lọc.” khi tập rỗng."),
    ("Nút Đóng", "Button", "Enable", "–", "Hiển thị", "Đóng cửa sổ."),
], required=False)

d.p("2.3.4 Danh sách event và xử lý event")
d.event_table([
    ("Bấm vào con số trên màn báo cáo", "Click",
     "Before:\n– Giữ nguyên phạm vi quyền và bộ lọc của màn báo cáo.\n"
     "During:\n– Xác định tập nhu cầu ứng với con số vừa bấm.\n"
     "After:\n– Mở cửa sổ, tính khối KPI và khối phân bổ trên chính tập đó.\n"
     "– Đặt lại toàn bộ ô lọc riêng của cửa sổ về trống."),
    ("Bấm nút phóng to", "Click", "After:\n– Cửa sổ phủ kín màn hình, không hở bốn mép."),
    ("Bấm nút Thu gọn", "Click", "After:\n– Ẩn khối KPI và khối phân bổ, bảng chi tiết trồi lên."),
    ("Bấm nút Đóng hoặc dấu X", "Click",
     "After:\n– Đóng cửa sổ, màn báo cáo giữ nguyên bộ lọc và số liệu."),
    ("Cuộn bảng chi tiết", "System",
     "After:\n– Chỉ phần thân cửa sổ cuộn; tiêu đề và hàng nút dưới cùng đứng yên."),
])

# ---------------------------------------------------------------- 2.4
d.h3("2.4 Lọc và thống kê nhanh trong danh sách chi tiết")
d.p("2.4.1 Biểu đồ Usecase")
d.uc_figure("FR-04", "Lọc & thống kê nhanh", "view",
            [("include", "Xem danh sách nhu cầu chi tiết"),
             ("extend", "Ẩn ô lọc của cơ cấu đang xem")],
            actor=ACTOR_KD,
            caption="Hình 6: Biểu đồ Use Case — FR-04 Lọc và thống kê nhanh trong danh sách chi tiết")

d.p("2.4.2 Giới thiệu")
d.intro_table(
    ten="Lọc và thống kê nhanh trong danh sách chi tiết",
    mota="Thu hẹp danh sách nhu cầu đang xem bằng ô tìm kiếm, bảy ô lọc và các chip trong khối phân "
         "bổ nhu cầu theo cơ cấu.",
    tacnhan="%s; %s; Người dùng đã đăng nhập" % (ACTOR_QL, ACTOR_KD),
    dieukien="Cửa sổ danh sách nhu cầu chi tiết đang mở.",
    chinh="1. Người dùng gõ từ khoá hoặc chọn giá trị ở một ô lọc.\n"
          "2. Hệ thống lọc lại danh sách và cập nhật số đếm “n / N nhu cầu”.\n"
          "3. Hệ thống tính lại khối KPI và khối phân bổ theo tập vừa lọc.",
    phu="• Bấm một chip trong khối phân bổ: lọc nhanh theo mục đó, chip được tô sáng; bấm lại để bỏ "
        "lọc.\n"
        "• Đổi ô lọc cha: giá trị của ô lọc con bị xoá.\n"
        "• Bấm nút Xoá lọc: mọi ô lọc, ô tìm kiếm và chip trở về trạng thái ban đầu.\n"
        "• Mở cửa sổ theo một cơ cấu: ô lọc của cơ cấu đó không hiển thị và không lọc ngầm.",
    dacbiet="Bộ lọc trong cửa sổ chỉ thu hẹp tập đang xem, không thay đổi số liệu trên màn báo cáo.")

d.p("2.4.3 Layout màn hình")
d.layout(modal="Danh sách nhu cầu chi tiết", shot=shot("04-popup-loc.png"),
         shot_caption="Hình 7: Cửa sổ chi tiết đang lọc nhanh bằng chip trong khối phân bổ")

d.p("2.4.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Ô tìm kiếm", "Textbox", "Enable", "0–255 ký tự", "Không", "Trống",
     "Tìm theo tên khách hàng, mã khách hàng, tên và mã meeting, tên người chủ trì, tên tỉnh, "
     "phường, nhóm ngành và lĩnh vực."),
    ("Chọn lĩnh vực công ty kinh doanh", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Trống",
     "Ô cha của Nhóm ngành. Ẩn khi cửa sổ đang mở theo cơ cấu lĩnh vực."),
    ("Chọn nhóm ngành", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Trống",
     "Lọc theo lĩnh vực đang chọn."),
    ("Chọn tỉnh / thành phố", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Trống",
     "Ô cha của Phường / xã. Ẩn khi cửa sổ đang mở theo cơ cấu thị trường."),
    ("Chọn phường / xã", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Trống",
     "Lọc theo tỉnh đang chọn."),
    ("Chọn phòng ban", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Trống",
     "Ô cha của Nhân viên chủ trì. Ẩn khi cửa sổ đang mở theo cơ cấu phòng ban."),
    ("Chọn nhân viên chủ trì", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Trống",
     "Lọc theo phòng ban đang chọn."),
    ("Chọn trạng thái nhu cầu", "Dropdown", "Enable", "Danh sách 3 giá trị", "Không", "Trống",
     "Đang theo dõi, Đã lập dự án TKT, Không tiếp tục. Luôn đứng cuối hàng lọc."),
    ("Nút Xoá lọc", "Icon Button", "Enable", "–", "–", "Hiển thị",
     "Đưa mọi ô lọc, ô tìm kiếm và chip về trạng thái ban đầu. Nằm cùng hàng với các ô lọc."),
    ("Chip trong khối phân bổ", "Button", "Enable", "–", "–", "Theo dữ liệu",
     "Mỗi chip là một mục của cơ cấu, kèm số nhu cầu và tỷ lệ phần trăm. Bấm để lọc nhanh, bấm lại "
     "để bỏ lọc."),
])

d.p("2.4.5 Danh sách event và xử lý event")
d.event_table([
    ("Gõ vào ô tìm kiếm", "Keypress",
     "During:\n– Lọc theo chuỗi vừa gõ, không phân biệt chữ hoa chữ thường.\n"
     "After:\n– Cập nhật bảng, số đếm, khối KPI và khối phân bổ.\n"
     "– Con trỏ vẫn nằm trong ô tìm kiếm."),
    ("Chọn giá trị ở một ô lọc", "Change",
     "During:\n– Ô lọc cha đổi giá trị thì xoá giá trị ô lọc con.\n"
     "After:\n– Lọc lại danh sách và cập nhật số đếm, khối KPI, khối phân bổ."),
    ("Bấm một chip trong khối phân bổ", "Click",
     "After:\n– Lọc danh sách theo mục của chip và tô sáng chip đó.\n"
     "– Bấm lại chip đang tô sáng thì bỏ lọc."),
    ("Bấm nút Xoá lọc", "Click",
     "After:\n– Xoá mọi ô lọc, ô tìm kiếm và bỏ tô sáng mọi chip.\n"
     "– Danh sách trở về đầy đủ tập đang xem."),
])

# ---------------------------------------------------------------- 2.5
d.h3("2.5 In báo cáo")
d.p("2.5.1 Biểu đồ Usecase")
d.uc_figure("FR-05", "In báo cáo", "io",
            [("include", "Chọn kiểu in: bảng theo dõi hoặc danh sách chi tiết"),
             ("include", "Áp dụng bộ lọc đang xem"),
             ("extend", "In danh sách ngay từ cửa sổ chi tiết")],
            actor=ACTOR_QL,
            caption="Hình 8: Biểu đồ Use Case — FR-05 In báo cáo")

d.p("2.5.2 Giới thiệu")
d.intro_table(
    ten="In báo cáo",
    mota="Tạo bản in khổ A4 ngang theo đúng bộ lọc đang áp dụng, với hai kiểu: in bảng theo dõi hoặc "
         "in danh sách nhu cầu chi tiết.",
    tacnhan="%s; %s; Người dùng đã đăng nhập" % (ACTOR_QL, ACTOR_KD),
    dieukien="Đang ở màn hình báo cáo và đã có số liệu.",
    chinh="1. Người dùng bấm nút “In báo cáo”.\n"
          "2. Hệ thống mở cửa sổ chọn kiểu in với hai lựa chọn.\n"
          "3. Người dùng chọn kiểu in rồi bấm “In”.\n"
          "4. Hệ thống dựng nội dung bản in theo bộ lọc đang áp dụng và mở cửa sổ xem trước.\n"
          "5. Người dùng bấm nút “In” trên cửa sổ xem trước để gửi ra máy in.",
    phu="• Bấm “Hủy” ở cửa sổ chọn kiểu in: đóng cửa sổ, không tạo bản in.\n"
        "• Bấm “In danh sách” ngay trong cửa sổ chi tiết: bản in bám theo tập đang xem kèm cả bộ lọc "
        "riêng của cửa sổ.\n"
        "• Trình duyệt chặn cửa sổ bật lên: hệ thống báo để người dùng cho phép rồi bấm In lại.",
    dacbiet="Bản in luôn có ảnh tiêu đề thư của công ty người đăng nhập ở đầu trang và dòng ngày in "
            "ở cuối trang.")

d.p("2.5.3 Layout màn hình")
d.layout(modal="In báo cáo", shot=shot("05-chon-kieu-in.png"),
         shot_caption="Hình 9: Cửa sổ chọn kiểu in")
d.figure(shot("05b-xem-truoc.png"), "Hình 10: Cửa sổ xem trước bản in bảng theo dõi", width_in=6.2)

d.p("2.5.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Nút In báo cáo", "Button", "Enable", "–", "–", "Hiển thị",
     "Nằm ở góc phải khối bộ lọc, mở cửa sổ chọn kiểu in."),
    ("Dòng nhắc kiểu in", "Label", "Hiển thị", "–", "–", "Hiển thị",
     "“Bản in A4 ngang, bám đúng bộ lọc đang áp dụng.”"),
    ("Lựa chọn In bảng theo dõi", "Dropdown", "Enable", "Danh sách 2 giá trị", "Có",
     "Được chọn sẵn", "In đúng bảng đang xem, kèm khối tổng hợp và kết quả KPI."),
    ("Lựa chọn In danh sách chi tiết", "Dropdown", "Enable", "Danh sách 2 giá trị", "Có", "Trống",
     "In từng nhu cầu một dòng, đủ cột Lĩnh vực KD, Thị trường, Khách hàng."),
    ("Nút Hủy", "Button", "Enable", "–", "–", "Hiển thị", "Đóng cửa sổ chọn kiểu in."),
    ("Nút In (cửa sổ chọn kiểu)", "Button", "Enable", "–", "–", "Hiển thị",
     "Dựng bản in và mở cửa sổ xem trước."),
    ("Cửa sổ xem trước", "Modal", "Hiển thị", "–", "–", "Ẩn",
     "Hiển thị nội dung bản in khổ ngang; mở đè lên cửa sổ chi tiết nếu in từ đó."),
    ("Nút In (cửa sổ xem trước)", "Button", "Enable", "–", "–", "Hiển thị",
     "Mở hộp thoại in của trình duyệt với nội dung sạch, không kèm menu và thanh trên cùng."),
    ("Nút In danh sách", "Button", "Enable", "–", "–", "Hiển thị",
     "Nằm ở hàng nút dưới cùng của cửa sổ chi tiết, in ngay danh sách đang xem."),
], required=True)

d.p("2.5.5 Danh sách event và xử lý event")
d.event_table([
    ("Bấm nút In báo cáo", "Click",
     "After:\n– Mở cửa sổ chọn kiểu in, đặt sẵn lựa chọn “In bảng theo dõi”."),
    ("Bấm nút Hủy", "Click", "After:\n– Đóng cửa sổ chọn kiểu in, không tạo bản in."),
    ("Bấm nút In ở cửa sổ chọn kiểu", "Click",
     "Before:\n– Xác định phạm vi dữ liệu theo quyền của người đăng nhập.\n"
     "During:\n– Ghép bộ lọc đang áp dụng của màn báo cáo vào yêu cầu tạo bản in.\n"
     "After:\n– Dựng nội dung bản in kèm ảnh tiêu đề thư của công ty và dòng ngày in.\n"
     "– Mở cửa sổ xem trước khổ A4 ngang."),
    ("Bấm nút In danh sách trong cửa sổ chi tiết", "Click",
     "During:\n– Ghép thêm tập đang xem và bộ lọc riêng của cửa sổ.\n"
     "After:\n– Bản in gồm tên đối tượng đang xem, bộ lọc màn báo cáo, dòng “Lọc trong danh sách”, "
     "tổng số nhu cầu, khối kết quả KPI, khối phân bổ và bảng chi tiết."),
    ("Bấm nút In ở cửa sổ xem trước", "Click",
     "During:\n– Chờ ảnh tiêu đề thư tải xong rồi mới gửi lệnh in.\n"
     "After:\n– Mở hộp thoại in của trình duyệt với khổ A4 ngang.\n"
     "– Trình duyệt chặn cửa sổ bật lên → hiển thị “Trình duyệt đã chặn cửa sổ in. Vui lòng cho "
     "phép pop-up rồi bấm In lại.”"),
    ("Đóng cửa sổ xem trước", "Click",
     "After:\n– Chỉ đóng cửa sổ xem trước; cửa sổ chi tiết bên dưới vẫn mở và dùng được."),
])

# ---------------------------------------------------------------- 2.6
d.h3("2.6 Xuất tệp Excel")
d.p("2.6.1 Biểu đồ Usecase")
d.uc_figure("FR-06", "Xuất tệp Excel", "io",
            [("include", "Áp dụng bộ lọc đang xem"),
             ("extend", "Xuất danh sách nhu cầu từ cửa sổ chi tiết")],
            actor=ACTOR_QL,
            caption="Hình 11: Biểu đồ Use Case — FR-06 Xuất tệp Excel")

d.p("2.6.2 Giới thiệu")
d.intro_table(
    ten="Xuất tệp Excel",
    mota="Tải về tệp Excel của bảng theo dõi hoặc của danh sách nhu cầu chi tiết, bám đúng bộ lọc "
         "đang áp dụng.",
    tacnhan="%s; %s; Người dùng đã đăng nhập" % (ACTOR_QL, ACTOR_KD),
    dieukien="Đang ở màn hình báo cáo và đã có số liệu.",
    chinh="1. Người dùng bấm nút “Xuất Excel” trên khối bộ lọc.\n"
          "2. Hệ thống dựng tệp theo bộ lọc đang áp dụng và gửi về trình duyệt.\n"
          "3. Trình duyệt lưu tệp với tên do hệ thống đặt sẵn.",
    phu="• Bấm “Xuất Excel danh sách” trong cửa sổ chi tiết: tệp chứa đúng tập đang xem kèm bộ lọc "
        "riêng của cửa sổ.\n"
        "• Tập rỗng: tệp vẫn tải về được, chỉ có dòng tiêu đề và dòng “Không có dữ liệu”.\n"
        "• Màn báo cáo không tải lại và không mất bộ lọc sau khi xuất tệp.",
    dacbiet="Mọi ô số và ô tỷ lệ trong tệp là số thật, cộng và lọc được bằng công cụ của Excel; ô "
            "tỷ lệ được định dạng phần trăm.")

d.p("2.6.3 Layout màn hình")
d.layout(shot=shot("06-xuat-excel.png"),
         shot_caption="Hình 12: Cụm nút In báo cáo và Xuất Excel trên khối bộ lọc")

d.p("2.6.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Nút Xuất Excel", "Button", "Enable", "–", "–", "Hiển thị",
     "Tải tệp Excel của bảng theo dõi theo bộ lọc đang áp dụng."),
    ("Nút Xuất Excel danh sách", "Button", "Enable", "–", "–", "Hiển thị",
     "Nằm ở hàng nút dưới cùng của cửa sổ chi tiết, tải tệp của tập nhu cầu đang xem."),
    ("Tệp bảng theo dõi", "Text", "Hiển thị", "–", "–", "Theo dữ liệu",
     "Gồm ba phần: tổng hợp kỳ, kết quả KPI và bảng theo dõi. Chỉ chứa phần bảng ứng với tiêu chí "
     "theo dõi đang chọn."),
    ("Tệp danh sách nhu cầu", "Text", "Hiển thị", "–", "–", "Theo dữ liệu",
     "Mỗi nhu cầu một dòng, đủ mười sáu cột kể cả Mã KH và Ngày đóng; thứ tự cột cố định, không đổi "
     "theo cơ cấu đang xem."),
    ("Phân cấp trong tệp", "Text", "Hiển thị", "–", "–", "Theo dữ liệu",
     "Dòng tiêu đề phần đánh số La Mã, dòng cha đánh số thường, dòng con để trống ô số thứ tự và "
     "tên bắt đầu bằng dấu gạch dài."),
    ("Thông báo lỗi khi tải", "Toast / Alert", "Hiển thị", "–", "–", "Ẩn",
     "“Lỗi khi xuất Excel” khi không tạo được tệp."),
], required=True)

d.p("2.6.5 Danh sách event và xử lý event")
d.event_table([
    ("Bấm nút Xuất Excel", "Click",
     "Before:\n– Xác định phạm vi dữ liệu theo quyền của người đăng nhập.\n"
     "During:\n– Ghép bộ lọc đang áp dụng vào yêu cầu tạo tệp.\n"
     "After:\n– Dựng tệp và tải trực tiếp về máy, tên tệp do máy chủ đặt sẵn.\n"
     "– Màn báo cáo giữ nguyên bộ lọc và số liệu, không tải lại."),
    ("Bấm nút Xuất Excel danh sách", "Click",
     "During:\n– Ghép thêm tập đang xem và bộ lọc riêng của cửa sổ chi tiết.\n"
     "After:\n– Tệp tải về chứa đúng số dòng đang hiển thị trong cửa sổ."),
    ("Không tạo được tệp", "System",
     "After:\n– Hiển thị thông báo “Lỗi khi xuất Excel”, không tải tệp rỗng về máy."),
])

# ---------------------------------------------------------------- 2.7
d.h3("2.7 Tạo dự án tiền khả thi từ nhu cầu")
d.p("2.7.1 Biểu đồ Usecase")
d.uc_figure("FR-07", "Tạo dự án tiền khả thi từ nhu cầu", "crud",
            [("include", "Kiểm tra quyền Quản lý dự án tiền khả thi"),
             ("extend", "Gắn nhu cầu vào dự án ở màn tạo dự án")],
            actor=ACTOR_KD,
            caption="Hình 13: Biểu đồ Use Case — FR-07 Tạo dự án tiền khả thi từ nhu cầu")

d.p("2.7.2 Giới thiệu")
d.intro_table(
    ten="Tạo dự án tiền khả thi từ nhu cầu",
    mota="Từ một dòng nhu cầu trong cửa sổ chi tiết, chuyển sang màn tạo dự án tiền khả thi với "
         "khách hàng đã được chọn sẵn.",
    tacnhan="%s; Người dùng đã đăng nhập" % ACTOR_KD,
    dieukien="Người dùng có quyền “Quản lý dự án tiền khả thi” và cửa sổ chi tiết đang mở.",
    chinh="1. Người dùng bấm nút “+ Tạo mới” ở dòng nhu cầu cần chuyển đổi.\n"
          "2. Hệ thống mở tab mới vào màn tạo dự án tiền khả thi, khách hàng đã chọn sẵn.\n"
          "3. Người dùng chọn đúng nhu cầu ở ô “Nhu cầu khách hàng” rồi lưu dự án.\n"
          "4. Hệ thống chuyển nhu cầu sang trạng thái “Đã lập dự án TKT” và ghi ngày đóng.\n"
          "5. Người dùng quay lại tab báo cáo và bấm “Tìm kiếm” để thấy số liệu mới.",
    phu="• Không có quyền “Quản lý dự án tiền khả thi”: nút “+ Tạo mới” bị ẩn hoàn toàn.\n"
        "• Lưu dự án mà chưa chọn nhu cầu: hệ thống hỏi lại bằng một cửa sổ xác nhận, người dùng vẫn "
        "có thể tiếp tục lưu.\n"
        "• Đổi sang nhu cầu khác khi sửa dự án: nhu cầu cũ được trả về “Đang theo dõi”.\n"
        "• Bỏ chọn nhu cầu khi sửa dự án: nhu cầu được trả về “Đang theo dõi” và xoá ngày đóng.",
    dacbiet="Việc gắn nhu cầu vào dự án được thực hiện ở màn dự án tiền khả thi, không thực hiện "
            "trực tiếp trên màn báo cáo.")

d.p("2.7.3 Layout màn hình")
d.layout(modal="Danh sách nhu cầu chi tiết", shot=shot("07-tao-du-an.png"),
         shot_caption="Hình 14: Nút “+ Tạo mới” ở cột cuối của bảng chi tiết")

d.p("2.7.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Nút + Tạo mới", "Button", "Enable / Ẩn", "–", "–", "Ẩn khi thiếu quyền",
     "Chỉ hiện khi có quyền “Quản lý dự án tiền khả thi”. Mở tab mới sang màn tạo dự án tiền khả thi."),
    ("Ô Nhu cầu khách hàng (ở màn dự án)", "Dropdown", "Enable", "Danh sách", "Không", "Trống",
     "Chỉ liệt kê nhu cầu của đúng khách hàng, thuộc meeting đã Hoàn thành do chính mình chủ trì và "
     "còn ở trạng thái “Đang theo dõi”."),
    ("Cửa sổ xác nhận khi chưa chọn nhu cầu", "Modal", "Hiển thị", "–", "–", "Ẩn",
     "Nhắc người dùng chưa chọn nhu cầu khách hàng; chỉ cảnh báo, không chặn lưu."),
], required=True)

d.p("2.7.5 Danh sách event và xử lý event")
d.event_table([
    ("Bấm nút + Tạo mới", "Click",
     "Before:\n– Kiểm tra quyền “Quản lý dự án tiền khả thi”.\n"
     "– Không có quyền → nút đã bị ẩn nên không phát sinh thao tác.\n"
     "After:\n– Mở tab mới vào màn tạo dự án tiền khả thi kèm khách hàng của dòng vừa bấm.\n"
     "– Tab báo cáo giữ nguyên bộ lọc đang xem."),
    ("Lưu dự án có chọn nhu cầu", "Click",
     "During:\n– Nhu cầu không thuộc khách hàng của dự án → hiển thị thông báo từ chối và không lưu.\n"
     "– Nhu cầu đã được dự án khác gắn → hiển thị thông báo từ chối và không lưu.\n"
     "After:\n– Chuyển nhu cầu sang trạng thái “Đã lập dự án TKT” và ghi ngày đóng là ngày hiện tại.\n"
     "– Nhu cầu xuất hiện ở ô “Chuyển đổi thành dự án TKT” của kỳ chứa ngày đóng."),
    ("Đổi hoặc bỏ nhu cầu khi sửa dự án", "Change",
     "After:\n– Trả nhu cầu cũ về trạng thái “Đang theo dõi”, xoá ngày đóng và liên kết dự án.\n"
     "– Gắn nhu cầu mới nếu người dùng chọn giá trị khác."),
    ("Lưu dự án mà chưa chọn nhu cầu", "Click",
     "During:\n– Hiển thị cửa sổ xác nhận nhắc chưa chọn nhu cầu khách hàng.\n"
     "After:\n– Người dùng bấm Hủy → không lưu, giữ nguyên dữ liệu đã nhập.\n"
     "– Người dùng đồng ý → vẫn lưu dự án, không gắn nhu cầu nào."),
])

# ---------------------------------------------------------------- 2.8
d.h3("2.8 Tự động đóng nhu cầu hết hạn theo dõi")
d.p("2.8.1 Biểu đồ Usecase")
d.uc_figure("FR-08", "Tự động đóng nhu cầu hết hạn theo dõi", "action",
            [("include", "Ghi ngày đóng bằng ngày dự kiến triển khai"),
             ("extend", "Bỏ qua nhu cầu không có ngày dự kiến triển khai")],
            actor=ACTOR_HT,
            caption="Hình 15: Biểu đồ Use Case — FR-08 Tự động đóng nhu cầu hết hạn theo dõi")

d.p("2.8.2 Giới thiệu")
d.intro_table(
    ten="Tự động đóng nhu cầu hết hạn theo dõi",
    mota="Tác vụ chạy định kỳ hằng ngày, chuyển những nhu cầu đã quá thời gian dự kiến triển khai mà "
         "chưa lập dự án tiền khả thi sang trạng thái “Không tiếp tục”.",
    tacnhan="%s" % ACTOR_HT,
    dieukien="Tác vụ định kỳ đã được bật trên môi trường đang chạy.",
    chinh="1. Tác vụ chạy vào rạng sáng mỗi ngày.\n"
          "2. Hệ thống tìm các nhu cầu còn “Đang theo dõi” có thời gian dự kiến triển khai đã qua.\n"
          "3. Hệ thống chuyển từng nhu cầu sang trạng thái “Không tiếp tục”.\n"
          "4. Hệ thống ghi ngày đóng bằng đúng thời gian dự kiến triển khai của nhu cầu.\n"
          "5. Kết quả xuất hiện ở ô “Hết hạn, không tiếp tục” của kỳ chứa ngày đóng.",
    phu="• Nhu cầu không có thời gian dự kiến triển khai: bỏ qua, giữ nguyên “Đang theo dõi”.\n"
        "• Nhu cầu đã gắn dự án tiền khả thi: bỏ qua.\n"
        "• Tác vụ chạy lại nhiều lần: không đóng thêm lần nữa và không đổi ngày đóng đã ghi.",
    dacbiet="Ngày đóng lấy theo thời gian dự kiến triển khai chứ không lấy ngày tác vụ chạy, nhờ đó "
            "tác vụ chạy trễ hoặc chạy bù không làm lệch số liệu giữa các kỳ.")

d.p("2.8.3 Layout màn hình")
d.layout(note="Chức năng chạy tự động phía máy chủ, không có giao diện thao tác riêng. Kết quả được "
              "quan sát trên chính màn hình báo cáo, ở khối “Tổng nhu cầu bị đóng trong kỳ”.",
         shot=shot("08-het-han.png"),
         shot_caption="Hình 16: Kết quả của tác vụ hiển thị ở ô “Hết hạn, không tiếp tục”")

d.p("2.8.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Ô Hết hạn, không tiếp tục", "Text", "Hiển thị", "≥ 0", "Theo dữ liệu",
     "Số nhu cầu bị tác vụ đóng, có ngày đóng nằm trong kỳ đang xem."),
    ("Cột Trạng thái trong cửa sổ chi tiết", "Badge", "Hiển thị", "Danh sách 3 giá trị",
     "Theo dữ liệu", "Nhu cầu bị tác vụ đóng hiển thị nhãn “Không tiếp tục”."),
    ("Cột Ngày đóng trong tệp Excel", "Text", "Hiển thị", "dd/mm/yyyy", "Theo dữ liệu",
     "Bằng đúng thời gian dự kiến triển khai của nhu cầu."),
], required=False)

d.p("2.8.5 Danh sách event và xử lý event")
d.event_table([
    ("Tác vụ định kỳ chạy hằng ngày", "System",
     "During:\n– Bỏ qua nhu cầu không có thời gian dự kiến triển khai.\n"
     "– Bỏ qua nhu cầu đã gắn dự án tiền khả thi.\n"
     "After:\n– Chuyển nhu cầu quá hạn sang trạng thái “Không tiếp tục”.\n"
     "– Ghi ngày đóng bằng đúng thời gian dự kiến triển khai.\n"
     "– Ghi lại số dòng đã xử lý vào nhật ký hệ thống."),
    ("Tác vụ chạy lại lần nữa trong ngày", "System",
     "After:\n– Không đóng thêm nhu cầu nào đã đóng trước đó và không đổi ngày đóng đã ghi."),
])

# ==================================================== PHẦN 4
d.h1("Phần 4. Quy tắc nghiệp vụ")

BR = [
    ("BR-01 — Điều kiện để một nhu cầu được đưa vào báo cáo", [
        "Nhu cầu phải nằm trong biên bản của meeting loại “Họp tìm hiểu & Giới thiệu sản phẩm”.",
        "Meeting phải ở trạng thái “Hoàn thành”.",
        "Biên bản phải ghi nhận khách hàng CÓ nhu cầu đầu tư.",
        "Không thoả một trong ba điều kiện trên thì nhu cầu không xuất hiện ở bất kỳ chỉ tiêu nào.",
    ]),
    ("BR-02 — Một nhóm ngành là một nhu cầu", [
        "Mỗi nhóm ngành khách hàng quan tâm trong biên bản được ghi thành một dòng nhu cầu riêng, "
        "có giá trị đầu tư dự kiến và thời gian dự kiến triển khai riêng.",
        "Cùng một khách hàng trong cùng một meeting có thể sinh nhiều nhu cầu; đây không phải dữ "
        "liệu trùng.",
    ]),
    ("BR-03 — Ba trạng thái của nhu cầu", [
        "“Đang theo dõi”: chưa lập dự án tiền khả thi và chưa quá thời gian dự kiến triển khai.",
        "“Đã lập dự án TKT”: đã được gắn vào một dự án tiền khả thi.",
        "“Không tiếp tục”: đã quá thời gian dự kiến triển khai mà vẫn chưa lập dự án.",
        "Nhu cầu chuyển sang “Đã lập dự án TKT” hoặc “Không tiếp tục” đều được ghi ngày đóng.",
    ]),
    ("BR-04 — Cách tính hai khối tổng hợp", [
        "Chỉ tiêu I “Tổng nhu cầu trong kỳ” bằng tổng của hai ô con: nhu cầu còn hiệu lực theo dõi "
        "và nhu cầu phát sinh trong kỳ.",
        "“Còn hiệu lực theo dõi” là nhu cầu có ngày họp trước ngày đầu kỳ và tới đầu kỳ vẫn chưa bị "
        "đóng.",
        "“Phát sinh trong kỳ” là nhu cầu có ngày họp nằm trong kỳ.",
        "Chỉ tiêu II “Tổng nhu cầu bị đóng trong kỳ” bằng tổng của hai ô con: chuyển đổi thành dự án "
        "tiền khả thi và hết hạn không tiếp tục, xét theo ngày đóng nằm trong kỳ.",
    ]),
    ("BR-05 — Nhu cầu được đếm ở cả hai khối", [
        "Một nhu cầu vừa có ngày họp trong kỳ vừa có ngày đóng trong kỳ sẽ xuất hiện ở cả chỉ tiêu I "
        "và chỉ tiêu II.",
        "Đây là hành vi đúng: khối I là tập đang theo dõi, khối II là kết quả xử lý trong kỳ.",
    ]),
    ("BR-06 — Nhu cầu đóng từ kỳ trước bị loại hoàn toàn", [
        "Nhu cầu có ngày đóng nằm trước ngày đầu kỳ không được tính vào bất kỳ chỉ tiêu nào của kỳ "
        "đang xem.",
    ]),
    ("BR-07 — Cách tính ba ô kết quả KPI", [
        "“Tỷ lệ chuyển đổi thành công” bằng số nhu cầu chuyển đổi thành dự án tiền khả thi chia cho "
        "chỉ tiêu I.",
        "“Thành công / tổng nhu cầu đóng” bằng số nhu cầu chuyển đổi chia cho chỉ tiêu II.",
        "“Thất bại / tổng nhu cầu đóng” bằng số nhu cầu hết hạn không tiếp tục chia cho chỉ tiêu II.",
        "Kết quả làm tròn một chữ số thập phân; mẫu số bằng 0 thì hiển thị 0,0%.",
    ]),
    ("BR-08 — Ba phần của bảng theo dõi luôn có cùng tổng", [
        "Ba phần chỉ là ba cách bổ dọc cùng một tập nhu cầu nên tổng của mỗi phần luôn bằng chỉ tiêu I.",
        "Nhu cầu thiếu thông tin phân nhóm được gom vào dòng “Chưa xác định …” chứ không bị loại "
        "khỏi tổng.",
        "Nhu cầu có giá trị phân nhóm nhưng không tra được tên (danh mục đã bị xoá) cũng được gom "
        "vào đúng dòng “Chưa xác định …” đó, không tách thành hai dòng cùng nhãn.",
    ]),
    ("BR-09 — Cách tính tỷ trọng giá trị", [
        "Dòng cha tính tỷ trọng so với tổng giá trị của cả kỳ; tổng tỷ trọng các dòng cha trong một "
        "phần bằng 100%.",
        "Dòng con tính tỷ trọng trong nội bộ dòng cha; tổng tỷ trọng các dòng con của một cha bằng "
        "100%.",
        "Tổng giá trị bằng 0 thì mọi ô tỷ trọng hiển thị 0,0%.",
    ]),
    ("BR-10 — Một dự án tiền khả thi gắn đúng một nhu cầu", [
        "Ô chọn nhu cầu ở màn dự án chỉ liệt kê nhu cầu của đúng khách hàng, thuộc meeting đã Hoàn "
        "thành do chính người đang thao tác chủ trì, và còn ở trạng thái “Đang theo dõi”.",
        "Nhu cầu đã được một dự án khác gắn thì không xuất hiện trong danh sách chọn.",
        "Đổi hoặc bỏ nhu cầu khi sửa dự án thì nhu cầu cũ được trả về “Đang theo dõi”, xoá ngày đóng "
        "và xoá liên kết dự án.",
    ]),
    ("BR-11 — Sửa biên bản không được làm mất liên kết dự án", [
        "Lưu lại biên bản meeting chỉ cập nhật các nhu cầu theo nhóm ngành được chọn, giữ nguyên "
        "trạng thái, ngày đóng và liên kết dự án của những nhu cầu đã có.",
        "Bỏ chọn một nhóm ngành mà nhu cầu tương ứng đã gắn dự án tiền khả thi thì hệ thống từ chối "
        "lưu và hướng dẫn gỡ liên kết ở màn dự án trước.",
    ]),
    ("BR-12 — Quy tắc đóng nhu cầu hết hạn theo dõi", [
        "Tác vụ định kỳ chạy hằng ngày, đóng những nhu cầu còn “Đang theo dõi” đã quá thời gian dự "
        "kiến triển khai.",
        "Ngày đóng được ghi bằng đúng thời gian dự kiến triển khai, không phải ngày tác vụ chạy.",
        "Nhu cầu không có thời gian dự kiến triển khai thì không bao giờ bị đóng tự động.",
        "Chạy lại tác vụ nhiều lần không làm thay đổi kết quả đã ghi.",
    ]),
    ("BR-13 — Phạm vi dữ liệu theo quyền", [
        "Ba quyền phạm vi không chặn việc mở màn hình mà chỉ thu hẹp tập nhu cầu nhìn thấy được.",
        "Người dùng không có quyền phạm vi nào chỉ thấy nhu cầu từ meeting do chính mình chủ trì "
        "hoặc mình có tham dự.",
        "Phạm vi này áp dụng đồng thời cho bảng theo dõi, cửa sổ chi tiết, bản in và tệp Excel.",
    ]),
    ("BR-14 — Bộ lọc áp dụng thống nhất cho mọi đầu ra", [
        "Bộ lọc trên màn báo cáo áp dụng cho khối tổng hợp, ba ô KPI, bảng theo dõi, cửa sổ chi "
        "tiết, bản in và tệp Excel.",
        "Bộ lọc riêng trong cửa sổ chi tiết chỉ thu hẹp tập đang xem trong cửa sổ đó, đồng thời được "
        "ghi lại trên bản in và tệp Excel xuất từ chính cửa sổ.",
        "Đổi tiêu chí theo dõi thì giá trị của khối lọc không còn hiển thị bị xoá để tránh lọc ngầm.",
    ]),
]

for title, items in BR:
    d.p(title)
    d.bullets(items)

d.save()
