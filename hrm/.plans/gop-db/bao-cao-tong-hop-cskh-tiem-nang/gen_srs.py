# -*- coding: utf-8 -*-
"""Sinh "SRS - Báo cáo tổng hợp chăm sóc khách hàng tiềm năng.docx" theo FORM CHUẨN hiện hành
(bản mẫu `.claude/skills/srs-documenter/assets/SRS_MAU.docx` = "SRS - Phiếu đề nghị thu tiền").

Chạy:  python3 .plans/gop-db/bao-cao-tong-hop-cskh-tiem-nang/gen_srs.py

Nguồn nội dung: design.md + plan.md cùng thư mục, spec
docs/superpowers/specs/gop-db/2026-10-04-bao-cao-tong-hop-cskh-tiem-nang-design.md, code nhánh gop_db
(hrm-api Modules/Assign/Services/Report/PotentialCustomerTracking*, Meeting::canView; hrm-client
pages/assign/report/potential-customer-tracking/**). Nội dung icon ⓘ chép NGUYÊN VĂN từ code FE.
Ảnh chụp thật ở `bao-cao-tong-hop-cskh_shots/` (1440×900, script chụp: scratchpad shoot.js).

Bổ sung theo yêu cầu user 05/10/2026: với các màn SỐ LIỆU (báo cáo chính, popup danh sách chi tiết) thêm mục
2.x.6 "Cách lấy dữ liệu và giải thích chỉ tiêu" — bảng 4 cột STT | Chỉ tiêu / Cột | Cách lấy dữ liệu |
Nội dung icon ⓘ. Đặt SAU 5 mục con cố định của form để không xáo thứ tự chuẩn.
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "..", "..", ".claude", "skills", "srs-documenter", "assets")
sys.path.insert(0, os.path.abspath(ASSETS))

# Thư viện vẽ UML trỏ cứng font Windows -> máy macOS trỏ sang Arial hệ thống (đủ dấu tiếng Việt),
# KHÔNG sửa file dùng chung trong .claude/skills/.
import srs_uml_render as uml  # noqa: E402

if not os.path.exists(uml.F_REG):
    _MAC = "/System/Library/Fonts/Supplemental"
    for _attr, _name in (("F_REG", "Arial.ttf"), ("F_BOLD", "Arial Bold.ttf"), ("F_ITAL", "Arial Italic.ttf")):
        _path = os.path.join(_MAC, _name)
        if os.path.exists(_path):
            setattr(uml, _attr, _path)

from srs_docx_lib import SrsDoc  # noqa: E402

SCREEN = "Báo cáo tổng hợp chăm sóc khách hàng tiềm năng"
OUT = os.path.join(HERE, "SRS - %s.docx" % SCREEN)
SHOTS = os.path.join(HERE, "bao-cao-tong-hop-cskh_shots")
MENU = "Phân hệ CSKH trước bán => Báo cáo => Báo cáo thị trường => Báo cáo tổng hợp CSKH tiềm năng"

ACT_QL = "Trưởng phòng / Quản lý kinh doanh"
ACT_SALES = "Nhân viên kinh doanh (Sales)"
TACNHAN = "%s; %s; Người dùng đã đăng nhập" % (ACT_QL, ACT_SALES)


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(out=OUT, menu=MENU, route="/assign/report/potential-customer-tracking",
           full_url="https://<host-hrm>/assign/report/potential-customer-tracking", img_prefix="pct_")

# ================================================================= TRANG ĐẦU
d.title_block(SCREEN)
d.h2("Mục lục")
d.toc()

# ================================================================= PHẦN 1
d.h1("Phần 1. Giới thiệu")

d.h2("1 Mục đích")
d.p("Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Báo cáo tổng hợp chăm sóc khách hàng tiềm năng thuộc "
    "phân hệ CSKH trước bán, nhằm:")
d.bullets([
    "Thống nhất yêu cầu giữa nghiệp vụ, phân tích, phát triển và kiểm thử cho báo cáo cho biết, TẠI THỜI ĐIỂM "
    "XEM, mỗi nhân viên kinh doanh (Sales) đang theo dõi những nhu cầu làm dự án và những dự án tiền khả thi "
    "(TKT) nào, với khách hàng nào, lần chăm sóc gần nhất là khi nào, nhu cầu nào sắp hết hạn theo dõi.",
    "Là căn cứ nghiệm thu chức năng, phạm vi dữ liệu theo 3 cấp quyền và cách tính từng con số.",
    "Mô tả rõ cách lấy dữ liệu của từng chỉ tiêu, từng cột số liệu và nội dung icon ⓘ giải thích trên giao "
    "diện (mục 2.1.6 và 2.5.6), để người dùng và người kiểm thử đối chiếu được số liệu.",
])

d.h2("2 Thuật ngữ và viết tắt")
d.table(["Thuật ngữ", "Mô tả"], [
    ("Nhu cầu (NC)", "Nhu cầu làm dự án của khách hàng, ghi nhận ở biên bản meeting “Họp tìm hiểu & giới "
     "thiệu sản phẩm”, mỗi dòng là một Lĩnh vực ▸ Nhóm ngành kèm giá trị dự kiến và ngày dự kiến triển khai."),
    ("Nhu cầu đang theo dõi", "Nhu cầu ở trạng thái Đang theo dõi (chưa lập dự án TKT, chưa đóng) và meeting "
     "ghi nhận nó đã Hoàn thành."),
    ("Dự án TKT (DA)", "Dự án tiền khả thi."),
    ("Dự án đang triển khai", "Dự án TKT có tiến trình từ “Thu thập thông tin dự án” tới “Thực hiện hợp đồng” "
     "(8 tiến trình). Không tính Đang tạo, Nghiệm thu và thanh lý hợp đồng, Đóng/Không thực hiện, Kết thúc và lưu trữ."),
    ("Sales phụ trách", "Nhu cầu: người đã nhận bàn giao nhu cầu; chưa bàn giao thì là người chủ trì meeting. "
     "Dự án TKT: Sales chủ trì của dự án."),
    ("Phòng / Công ty của Sales", "Phòng ban và công ty nơi Sales ĐANG làm việc tại thời điểm xem (theo hồ sơ "
     "nhân sự), không phải phòng ghi trên dự án."),
    ("Hạn theo dõi", "Ngày nhu cầu tự đóng nếu chưa lập dự án = ngày hoàn thành meeting + thời gian hiệu lực "
     "nhu cầu (N ngày) của Lĩnh vực, N lấy tại lúc tạo nhu cầu. N = 0 → không có hạn."),
    ("Cảnh báo trước khi đóng nhu cầu (M ngày)", "Tham số cấu hình theo công ty của meeting (mặc định 3 ngày). "
     "Nhu cầu đã vào khoảng M ngày trước hạn là “Sắp hết hạn theo dõi”."),
    ("Lần chăm sóc gần nhất", "Meeting Hoàn thành gần nhất với khách hàng, bất kể ai chủ trì."),
    ("Nhóm cấp 1", "Dòng Phòng ban — đơn vị phân trang của bảng."),
    ("ⓘ", "Icon thông tin; rê chuột để xem giải thích."),
], widths=[1.8, 4.2])

# ================================================================= PHẦN 2
d.h1("Phần 2. Phân quyền")

d.h2("1 Danh sách quyền")
d.p("Nhóm quyền thao tác:")
d.table(["Ký hiệu", "Tên quyền", "Tác dụng trên màn hình"], [
    ("—", "(không có)",
     "Màn hình KHÔNG gắn quyền thao tác: mọi người dùng đã đăng nhập đều mở được báo cáo và dùng được mọi "
     "chức năng (lọc, xem danh sách chi tiết, in, xuất Excel). Quyền chỉ quyết định PHẠM VI dữ liệu được thấy."),
], widths=[0.8, 2.0, 3.2])

d.p("Nhóm quyền quyết định phạm vi dữ liệu:")
d.table(["Ký hiệu", "Tên quyền", "Phạm vi dữ liệu"], [
    ("V1", "Xem báo cáo tổng hợp CSKH tiềm năng theo tổng công ty",
     "Toàn bộ nhu cầu và dự án của mọi công ty; ô Công ty mở để chọn (để trống = tất cả công ty)."),
    ("V2", "Xem báo cáo tổng hợp CSKH tiềm năng theo công ty",
     "Việc của các Sales đang làm việc ở công ty hiện tại + việc mình là Sales phụ trách. Ô Công ty khoá."),
    ("V3", "Xem báo cáo tổng hợp CSKH tiềm năng theo phòng ban",
     "Việc của các Sales thuộc các phòng ban mình được phân công quản lý + việc mình là Sales phụ trách. Ô "
     "Công ty khoá."),
    ("—", "(không có V1, V2, V3)", "Chỉ việc mình là Sales phụ trách. Ô Công ty khoá."),
], widths=[0.8, 2.2, 3.0])
d.p("Ràng buộc bổ sung: có nhiều quyền thì cấp cao nhất thắng (V1 > V2 > V3). Không có ngoại lệ cho tài khoản "
    "quản trị — kể cả Super admin cũng chỉ xét theo quyền được gán. Ba quyền nằm ở phân hệ CSKH trước bán, nhóm "
    "“Báo cáo tổng hợp CSKH tiềm năng” trên màn Phân quyền. Người có V1/V2/V3 xem được chi tiết meeting có nhu "
    "cầu trong phạm vi quyền của mình ngay từ báo cáo.")

d.h2("2 Ma trận phân quyền")
d.table(["Chức năng", "V1", "V2", "V3", "Không có quyền nào"], [
    ("FR-01 Xem báo cáo", "✅ (mọi công ty)", "✅ (công ty hiện tại)", "✅ (phòng được quản lý)", "✅ (việc của mình)"),
    ("FR-02 Tìm kiếm và lọc báo cáo", "✅ (chọn được Công ty)", "✅ (Công ty khoá)", "✅ (Công ty khoá)", "✅ (Công ty khoá)"),
    ("FR-03 Cài đặt bộ lọc", "✅", "✅", "✅", "✅"),
    ("FR-04 Chọn cấp xem và bung / thu gọn dòng", "✅", "✅", "✅", "✅"),
    ("FR-05 Xem danh sách chi tiết", "✅", "✅", "✅", "✅ (việc của mình)"),
    ("FR-06 Lọc và sắp xếp trong danh sách chi tiết", "✅", "✅", "✅", "✅"),
    ("FR-07 Xem chi tiết meeting", "✅", "✅ (Sales ở công ty hiện tại)", "✅ (Sales thuộc phòng được quản lý)",
     "✅ (meeting mình chủ trì / tham dự)"),
    ("FR-08 Xem lịch sử meeting với khách hàng", "✅", "✅", "✅", "✅"),
    ("FR-09 In danh sách", "✅", "✅", "✅", "✅ (việc của mình)"),
    ("FR-10 Xuất Excel", "✅", "✅", "✅", "✅ (việc của mình)"),
], widths=[2.2, 0.9, 1.0, 1.0, 0.9])

# ================================================================= PHẦN 3
d.h1("Phần 3. Đặc tả chi tiết theo từng chức năng")

d.h2("1 Sơ đồ UML tổng quan")
d.overview_figure2(
    [(ACT_QL, [0, 1]), (ACT_SALES, [0, 1])],
    [("FR-01", "Xem báo cáo tổng hợp CSKH tiềm năng", "view"),
     ("FR-05", "Xem danh sách chi tiết", "view")],
    [("FR-02", "Tìm kiếm và lọc báo cáo", "view", "extend", [0], None),
     ("FR-03", "Cài đặt bộ lọc", "view", "extend", [0], None),
     ("FR-04", "Chọn cấp xem và bung / thu gọn dòng", "view", "extend", [0], None),
     ("FR-08", "Xem lịch sử meeting với khách hàng", "view", "extend", [0], None),
     ("FR-06", "Lọc và sắp xếp trong danh sách chi tiết", "view", "extend", [1], None),
     ("FR-07", "Xem chi tiết meeting", "view", "extend", [0, 1], None),
     ("FR-09", "In danh sách", "io", "extend", [0, 1], None),
     ("FR-10", "Xuất Excel", "io", "extend", [0, 1], None)],
    "Sơ đồ Use Case tổng quan màn Báo cáo tổng hợp CSKH tiềm năng")

d.h2("2 Đặc tả chi tiết từng chức năng")

# ----------------------------------------------------------------- 2.1
d.h3("2.1 Xem báo cáo tổng hợp CSKH tiềm năng")
d.p("2.1.1 Giới thiệu")
d.rule_ref("- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các quy tắc riêng "
           "của Báo cáo tổng hợp CSKH tiềm năng tại phần mô tả chi tiết.", anchor="list")
d.intro_table(
    ten="Xem báo cáo tổng hợp CSKH tiềm năng",
    mota="Hiển thị TẠI THỜI ĐIỂM XEM các nhu cầu làm dự án đang theo dõi và các dự án TKT đang triển khai trong "
         "phạm vi quyền: dòng tóm tắt, hai khối tổng hợp (Nhu cầu đang theo dõi, Dự án TKT đang triển khai) và "
         "bảng cây Phòng ▸ Sales ▸ Khách hàng ▸ nhu cầu / dự án, phân trang theo phòng. Mọi con số khác 0 bấm "
         "được để mở danh sách chi tiết.",
    tacnhan=TACNHAN,
    dieukien="Người dùng đã đăng nhập. Màn hình không yêu cầu quyền riêng; quyền V1/V2/V3 chỉ quyết định phạm vi.",
    chinh="1. Người dùng vào menu Phân hệ CSKH trước bán → Báo cáo → Báo cáo thị trường → Báo cáo tổng hợp CSKH "
          "tiềm năng.\n"
          "2. Hệ thống xác định phạm vi theo quyền cao nhất người dùng có (V1 → V2 → V3 → việc của mình).\n"
          "3. Hệ thống lấy nhu cầu đang theo dõi và dự án đang triển khai trong phạm vi, gắn phòng / công ty nơi "
          "Sales đang làm việc.\n"
          "4. Hệ thống tính dòng tóm tắt, hai khối tổng hợp và dòng TỔNG trên toàn bộ dữ liệu đã lọc; dựng bảng "
          "cho trang 1 (20 phòng / trang), cấp xem mặc định “Đến Sales”.\n"
          "5. Màn hình hiển thị kết quả mà không cần bấm Tìm kiếm.",
    phu="• Không có việc nào trong phạm vi → bảng hiện “Không có nhu cầu / dự án nào khớp bộ lọc.”, các số = 0.\n"
        "• Tiến trình dự án có 0 dự án → không hiện ô của tiến trình đó ở khối tổng hợp; không có nhu cầu sắp "
        "hết hạn → không hiện ô “Sắp hết hạn theo dõi”.\n"
        "• Việc chưa có Sales phụ trách (hoặc Sales không còn hồ sơ) → gom vào nhóm “Chưa xác định phòng ▸ "
        "Chưa xác định Sales” ở cuối bảng (chỉ người có V1 thấy).\n"
        "• Bảng rộng hơn khung → xuất hiện thanh cuộn ngang ở cả trên và dưới bảng; tiêu đề cột dính khi cuộn dọc.\n"
        "• Bấm Thu gọn ở dòng tóm tắt → ẩn hai khối tổng hợp.",
    dacbiet=None)

d.p("2.1.2 Layout màn hình")
d.layout(menu=MENU, shot=shot("01-bao-cao.png"),
         shot_caption="Màn Báo cáo tổng hợp CSKH tiềm năng lúc mới truy cập (người dùng có quyền V1)")
d.figure(shot("12-khong-quyen.png"),
         "Cùng màn với người dùng không có quyền V1/V2/V3: ô Công ty khoá, chỉ thấy việc của mình", width_in=6.2)

d.p("2.1.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Tiêu đề trang", "Label", "Hiển thị", "–", "Báo cáo tổng hợp CSKH tiềm năng", "Trên thanh tiêu đề."),
    ("Dòng tóm tắt “Đang theo dõi tại <ngày giờ>”", "Label", "Hiển thị", "dd/mm/yyyy hh:mm", "Thời điểm tải",
     "Kèm số nhu cầu, số dự án TKT, số khách hàng, số Sales của toàn bộ dữ liệu đã lọc; có icon ⓘ."),
    ("Nút Thu gọn / Mở rộng", "Button", "Enable", "–", "Thu gọn", "Ẩn / hiện hai khối tổng hợp."),
    ("Khối Nhu cầu đang theo dõi", "Text", "Hiển thị", "≥ 0", "Theo dữ liệu",
     "Tiêu đề kèm “Giá trị dự kiến <tổng>” và icon ⓘ. Ô Nhu cầu đang theo dõi (luôn hiện); ô Sắp hết hạn theo "
     "dõi (nền cam, chỉ hiện khi > 0)."),
    ("Khối Dự án TKT đang triển khai", "Text", "Hiển thị", "≥ 0", "Theo dữ liệu",
     "Tiêu đề kèm “Giá trị HĐ dự kiến <tổng>” và icon ⓘ. Ô Dự án đang triển khai (luôn hiện) + mỗi tiến trình "
     "có ≥ 1 dự án một ô; thiếu chỗ thì các ô tự xuống hàng, nhãn luôn 1 dòng."),
    ("Bảng cây", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "10 cột: STT · Nội dung theo dõi · Loại · Trạng thái · Giá trị nhu cầu · Giá trị dự án · Mốc thời gian · "
     "Hạn theo dõi · Lần chăm sóc gần nhất · Nguồn. Cột Loại, Giá trị, Mốc thời gian, Hạn, Lần chăm sóc, Nguồn "
     "có icon ⓘ ở tiêu đề."),
    ("Ô chọn cấp xem (trong tiêu đề cột Nội dung theo dõi)", "Dropdown", "Enable", "Danh sách 4 giá trị",
     "Đến Sales", "Chỉ Phòng ban / Đến Sales / Đến Khách hàng / Tất cả cấp (đến Nhu cầu / Dự án) — FR-04."),
    ("Dòng TỔNG", "Label", "Read-only", "≥ 0", "Theo dữ liệu",
     "Nền cam, tính trên toàn bộ dữ liệu đã lọc (không theo trang); có icon ⓘ."),
    ("Dòng Phòng (I, II…) / Sales (1, 2…) / Khách hàng (1.1…)", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "Thụt lề theo cấp, mũi tên bung/thu. Phòng kèm mã phòng; Sales kèm mã nhân viên; khách hàng kèm mã khách "
     "hàng. Tên dài cắt bằng “…”, rê chuột xem đủ."),
    ("Dòng nhu cầu / dự án (1.1.1…)", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "Nhu cầu: “Lĩnh vực ▸ Nhóm ngành”. Dự án: mã dự án (liên kết mở dự án ở tab mới) - tên dự án."),
    ("Ô Loại ở dòng cha", "Number", "Read-only", "≥ 0", "Theo dữ liệu",
     "Dạng “a NC · b DA”; số khác 0 bấm được, số 0 hiện xám."),
    ("Badge Trạng thái", "Badge", "Read-only", "–", "Theo dữ liệu",
     "Nhu cầu: “Đang theo dõi”. Dự án: tên tiến trình. Chữ và màu theo hệ thống."),
    ("Ô Hạn theo dõi", "Text", "Read-only", "dd/mm/yyyy", "Theo dữ liệu",
     "Ngày hạn + “còn N ngày”; vào vùng cảnh báo thì chữ màu cam; không có hạn ghi “Không có hạn”."),
    ("Ô Lần chăm sóc gần nhất (dòng khách hàng)", "Text", "Read-only", "dd/mm/yyyy", "Theo dữ liệu",
     "Ngày bấm được (mở FR-08) + “N ngày”; chưa có meeting ghi “Chưa có meeting”."),
    ("Ô Nguồn", "Text", "Read-only", "–", "Theo dữ liệu", "Mã meeting, bấm mở panel chi tiết meeting (FR-07)."),
    ("Thanh cuộn ngang trên / dưới", "Scrollbar", "Hiển thị", "–", "Theo độ rộng",
     "Chỉ hiện khi bảng rộng hơn khung; hai thanh cuộn đồng bộ."),
    ("Phân trang", "Pagination", "Enable", "10 / 20 / 50 / 100", "20 phòng / trang",
     "Phân trang theo nhóm Phòng; dòng đếm “Hiển thị a–b / N phòng ban”; STT phòng chạy tiếp theo trang."),
    ("Trạng thái rỗng", "Label", "Hiển thị", "–", "Ẩn", "“Không có nhu cầu / dự án nào khớp bộ lọc.”"),
    ("Lớp mờ khi đang tải", "Loading", "Hiển thị", "–", "Ẩn", "Dữ liệu cũ mờ đi, không bấm được trong lúc tải lại."),
], required=False)

d.p("2.1.4 Danh sách event và xử lý event")
d.event_table([
    ("Mở màn hình", "System",
     "Before:\n– Xác định cấp quyền cao nhất của người dùng (V1/V2/V3/không quyền).\n"
     "During:\n– Nạp danh mục ô lọc (chỉ giá trị có trong phạm vi) và dữ liệu báo cáo, cấp xem Đến Sales.\n"
     "After:\n– Hiển thị dòng tóm tắt, hai khối tổng hợp, dòng TỔNG và trang 1 của bảng."),
    ("Bấm một con số khác 0 (khối tổng hợp / ô Loại)", "Click",
     "After:\n– Mở popup danh sách chi tiết đúng phạm vi dòng và đúng chỉ tiêu vừa bấm (FR-05)."),
    ("Bấm mã dự án", "Click", "After:\n– Mở màn chi tiết dự án TKT ở tab mới."),
    ("Bấm mã meeting ở cột Nguồn", "Click", "After:\n– Mở panel chi tiết meeting (FR-07)."),
    ("Bấm ngày ở cột Lần chăm sóc gần nhất", "Click", "After:\n– Mở popup lịch sử meeting với khách hàng (FR-08)."),
    ("Bấm số trang / đổi số dòng mỗi trang", "Click",
     "After:\n– Tải trang mới; dòng tóm tắt, khối tổng hợp và dòng TỔNG giữ nguyên. Đổi số dòng → về trang 1."),
    ("Bấm Thu gọn / Mở rộng", "Click", "After:\n– Ẩn hoặc hiện hai khối tổng hợp, đổi chữ trên nút."),
    ("Cuộn thanh cuộn ngang trên hoặc dưới", "Change", "After:\n– Thanh còn lại cuộn theo cùng vị trí."),
])
d.p("2.1.5 Quy tắc hiển thị")
d.bullets([
    "Số tiền và số đếm dùng dấu phẩy ngăn cách hàng nghìn (1,234,567); ngày dạng dd/mm/yyyy.",
    "Dòng tóm tắt, khối tổng hợp, dòng TỔNG, popup chi tiết, bản in và Excel cùng lấy một tập dữ liệu nên số "
    "luôn khớp nhau (khối tổng hợp = dòng TỔNG = số dòng popup tương ứng).",
    "Hai cột giá trị đứng riêng, không cộng lẫn: Giá trị nhu cầu chỉ cộng nhu cầu, Giá trị dự án chỉ cộng dự án.",
])
d.p("2.1.6 Cách lấy dữ liệu và giải thích chỉ tiêu")
d.p("Bảng dưới mô tả cách hệ thống tính từng chỉ tiêu, từng cột số liệu của báo cáo và nội dung icon ⓘ hiển "
    "thị khi rê chuột (nguyên văn trên giao diện). “Tập dữ liệu” là toàn bộ nhu cầu đang theo dõi và dự án đang "
    "triển khai sau khi áp phạm vi quyền và bộ lọc.")
d.data_table([
    ("Tiêu đề bộ lọc (ⓘ cạnh “Bộ lọc báo cáo tổng hợp CSKH tiềm năng”)", "Không phải số liệu.",
     "MỤC ĐÍCH BÁO CÁO • Xem tại thời điểm mở báo cáo mỗi Sales đang theo dõi những nhu cầu và dự án TKT nào • "
     "Nhu cầu: còn Đang theo dõi · Dự án TKT: chưa Đóng / chưa hoàn thành • Xem theo Phòng ▸ Sales ▸ Khách "
     "hàng; mỗi dòng lá là 1 nhu cầu hoặc 1 dự án"),
    ("Đang theo dõi tại <ngày giờ>", "Thời điểm máy chủ tính số liệu (lúc mở báo cáo / lúc tải lại). Báo cáo "
     "không có kỳ: luôn là ảnh chụp tại thời điểm này.",
     "MỤC ĐÍCH BÁO CÁO • Số liệu chụp TẠI THỜI ĐIỂM MỞ báo cáo — không theo kỳ • Nhu cầu: nhu cầu làm dự án "
     "còn Đang theo dõi (thu từ meeting tìm hiểu & giới thiệu sản phẩm) • Dự án TKT: tiến trình từ Thu thập "
     "thông tin tới Thực hiện hợp đồng • Bấm vào bất kỳ con số nào để mở danh sách chi tiết"),
    ("… nhu cầu (dòng tóm tắt)", "Đếm số nhu cầu trong tập dữ liệu: nhu cầu trạng thái Đang theo dõi, thuộc "
     "meeting đã Hoàn thành.", "—"),
    ("… dự án TKT (dòng tóm tắt)", "Đếm số dự án TKT trong tập dữ liệu: tiến trình từ Thu thập thông tin dự án "
     "tới Thực hiện hợp đồng.", "—"),
    ("… khách hàng", "Đếm KHÁC NHAU số khách hàng có ít nhất 1 nhu cầu hoặc 1 dự án trong tập dữ liệu "
     "(một khách vừa có nhu cầu vừa có dự án chỉ đếm 1).", "—"),
    ("… Sales", "Đếm KHÁC NHAU số Sales phụ trách có ít nhất 1 việc trong tập dữ liệu; không tính nhóm “Chưa "
     "xác định Sales”.", "—"),
    ("Khối Nhu cầu đang theo dõi — “Giá trị dự kiến”", "Tổng giá trị dự kiến của mọi nhu cầu trong tập dữ liệu.",
     "NHU CẦU ĐANG THEO DÕI • Nhu cầu làm dự án còn trạng thái Đang theo dõi, meeting thu thập đã Hoàn thành • "
     "Sales phụ trách = người nhận bàn giao, chưa bàn giao thì là người chủ trì meeting • Sắp hết hạn: còn "
     "trong số ngày \"Cảnh báo trước khi đóng nhu cầu\" của công ty"),
    ("Ô Nhu cầu đang theo dõi", "Bằng “… nhu cầu” ở dòng tóm tắt. Bấm số → popup toàn bộ nhu cầu.",
     "(dùng chung ⓘ của khối)"),
    ("Ô Sắp hết hạn theo dõi", "Đếm nhu cầu có hạn theo dõi, đã tới khoảng M ngày trước hạn (hôm nay ≥ hạn − M), "
     "với điều kiện N > M > 0. M = “Cảnh báo trước khi đóng nhu cầu” của công ty sở hữu meeting (chưa cấu hình "
     "= 3). Ô chỉ hiện khi > 0. Cùng luật với lệnh tự đóng nhu cầu và màn danh sách nhu cầu.",
     "(dùng chung ⓘ của khối)"),
    ("Khối Dự án TKT đang triển khai — “Giá trị HĐ dự kiến”", "Tổng giá trị hợp đồng dự kiến của mọi dự án trong "
     "tập dữ liệu.",
     "DỰ ÁN TKT ĐANG TRIỂN KHAI • Tiến trình từ Thu thập thông tin dự án tới Thực hiện hợp đồng • Không tính dự "
     "án Đang tạo, Nghiệm thu & thanh lý, Đóng, Kết thúc • Tiến trình chưa có dự án nào thì không hiện"),
    ("Ô Dự án đang triển khai", "Bằng “… dự án TKT” ở dòng tóm tắt.", "(dùng chung ⓘ của khối)"),
    ("Ô từng tiến trình (Thu thập thông tin dự án … Thực hiện hợp đồng)", "Đếm dự án trong tập dữ liệu đang ở "
     "đúng tiến trình đó. Tổng các ô tiến trình = ô Dự án đang triển khai. Tiến trình = 0 thì ẩn ô.",
     "(dùng chung ⓘ của khối)"),
    ("Dòng TỔNG — cột Nội dung theo dõi", "Không phải số liệu.",
     "PHÒNG / SALES / KHÁCH HÀNG • Phòng / công ty lấy theo nơi Sales ĐANG làm việc tại thời điểm xem • Mỗi dòng "
     "lá là 1 nhu cầu hoặc 1 dự án TKT; nhu cầu xếp trước • Việc chưa có Sales gom vào nhóm “Chưa xác định” ở "
     "cuối • Dòng TỔNG tính trên toàn bộ dữ liệu đã lọc, không theo trang"),
    ("Cột Loại (dòng TỔNG / Phòng / Sales / Khách hàng)", "“a NC · b DA”: a = số nhu cầu, b = số dự án của các "
     "dòng lá thuộc dòng đó. Phòng = phòng Sales đang làm việc; Sales = Sales phụ trách; Khách hàng = khách của "
     "nhu cầu (khách của meeting) / khách của dự án. Bấm a hoặc b → popup đúng phạm vi dòng.",
     "LOẠI • Dòng cha: số nhu cầu (NC) · số dự án TKT (DA) — bấm số để xem danh sách • Dòng lá: Nhu cầu hoặc "
     "Dự án TKT"),
    ("Cột Trạng thái (dòng lá)", "Nhu cầu: luôn “Đang theo dõi”. Dự án: tiến trình hiện tại của dự án.", "—"),
    ("Cột Giá trị nhu cầu", "Dòng lá nhu cầu: giá trị dự kiến của nhu cầu. Dòng cha: tổng giá trị dự kiến các "
     "nhu cầu thuộc dòng. Dòng lá dự án: để trống.",
     "GIÁ TRỊ NHU CẦU • Giá trị dự kiến khách hàng đầu tư, ghi ở biên bản meeting"),
    ("Cột Giá trị dự án", "Dòng lá dự án: giá trị hợp đồng dự kiến của dự án. Dòng cha: tổng giá trị hợp đồng dự "
     "kiến các dự án thuộc dòng. Dòng lá nhu cầu: để trống.",
     "GIÁ TRỊ DỰ ÁN • Giá trị hợp đồng dự kiến của dự án TKT"),
    ("Cột Mốc thời gian", "Nhu cầu: ngày dự kiến triển khai ghi ở biên bản. Dự án: ngày khách hàng cần giải pháp.",
     "MỐC THỜI GIAN • Nhu cầu: ngày dự kiến triển khai • Dự án TKT: ngày khách hàng cần giải pháp"),
    ("Cột Hạn theo dõi", "Chỉ nhu cầu. Hạn = ngày hoàn thành meeting + N ngày (thời gian hiệu lực của Lĩnh vực, "
     "lấy tại lúc tạo nhu cầu). “còn X ngày” = hạn − hôm nay. Chữ cam khi thuộc “Sắp hết hạn theo dõi”. N = 0 → "
     "“Không có hạn”. Dự án để trống.",
     "HẠN THEO DÕI • Hạn tự đóng nhu cầu = ngày hoàn thành meeting + thời gian hiệu lực của lĩnh vực • Màu cam: "
     "đã vào số ngày cảnh báo trước khi đóng • Không có hạn: lĩnh vực chưa đặt thời gian hiệu lực, nhu cầu "
     "không tự đóng"),
    ("Cột Lần chăm sóc gần nhất (dòng khách hàng)", "Ngày họp của meeting Hoàn thành mới nhất với khách hàng, "
     "BẤT KỂ ai chủ trì và không giới hạn loại meeting; “N ngày” = hôm nay − ngày đó. Không có meeting nào → "
     "“Chưa có meeting”.",
     "LẦN CHĂM SÓC GẦN NHẤT • Meeting Hoàn thành gần nhất với khách hàng (bất kỳ ai chủ trì) và số ngày tới hôm "
     "nay • Bấm ngày để xem lịch sử meeting"),
    ("Cột Nguồn", "Nhu cầu: mã meeting ghi nhận nhu cầu. Dự án: mã meeting của nhu cầu gốc nếu dự án được lập từ "
     "nhu cầu; lập trực tiếp thì để trống.",
     "NGUỒN • Meeting thu thập nhu cầu • Với dự án TKT: meeting của nhu cầu gốc (nếu dự án lập từ nhu cầu)"),
])

# ----------------------------------------------------------------- 2.2
d.h3("2.2 Tìm kiếm và lọc báo cáo")
d.p("2.2.1 Giới thiệu")
d.rule_ref("- Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang. Chỉ bổ sung các tiêu chí lọc riêng của Báo "
           "cáo tổng hợp CSKH tiềm năng.", anchor="search")
d.intro_table(
    ten="Tìm kiếm và lọc báo cáo",
    mota="Thu hẹp số liệu của toàn màn (tóm tắt, khối tổng hợp, bảng, popup, bản in, Excel) theo Công ty, Phòng "
         "ban, Sales phụ trách, Khách hàng, Loại, Tiến trình dự án, Lĩnh vực, Hạn theo dõi.",
    tacnhan=TACNHAN,
    dieukien="Đang ở màn Báo cáo tổng hợp CSKH tiềm năng.",
    chinh="1. Người dùng mở khối Tìm kiếm nâng cao (mặc định đang mở).\n"
          "2. Người dùng chọn giá trị ở một ô lọc → hệ thống tải lại báo cáo ngay, về trang 1.\n"
          "3. Bấm Tìm kiếm để tải lại với bộ lọc hiện tại; bấm Xóa lọc để về mặc định.",
    phu="• Không có V1 → ô Công ty khoá ở công ty của người dùng, Xóa lọc vẫn giữ công ty đó.\n"
        "• Đổi Công ty → xoá Phòng ban và Sales phụ trách đang chọn; đổi Phòng ban → xoá Sales phụ trách và chỉ "
        "liệt kê Sales của phòng đó.\n"
        "• Chọn Loại = Nhu cầu → xoá Tiến trình dự án; Loại = Dự án TKT → xoá Hạn theo dõi.\n"
        "• Ô Khách hàng: gõ tối thiểu 2 ký tự để tìm theo mã hoặc tên.\n"
        "• Giá trị đang chọn không còn trong danh mục mới vẫn được giữ trên ô để không lọc ngầm.",
    dacbiet=None)
d.p("2.2.2 Layout màn hình")
d.layout(menu=MENU, shot=shot("02-bo-loc.png"),
         shot_caption="Khối Tìm kiếm nâng cao, ô Tiến trình dự án (chọn nhiều) đang mở")
d.p("2.2.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Tiêu đề khối lọc", "Label", "Hiển thị", "–", "–", "Bộ lọc báo cáo tổng hợp CSKH tiềm năng", "Kèm icon ⓘ mục đích."),
    ("Nút Ẩn / Hiện tìm kiếm nâng cao", "Button", "Enable", "–", "–", "Hiện", "Thu/mở khối ô lọc."),
    ("Công ty", "Dropdown", "Enable / Disable", "Danh sách", "Không", "Theo quyền",
     "Có V1: chọn được, để trống = tất cả công ty. Không có V1: khoá ở công ty của người dùng. Icon ⓘ."),
    ("Phòng ban", "Dropdown", "Enable", "Danh sách", "Không", "Trống",
     "Phòng của các Sales có việc trong phạm vi, dạng “Tên phòng (mã)”. Có lựa chọn “Chưa xác định” khi có. Icon ⓘ."),
    ("Sales phụ trách", "Dropdown", "Enable", "Danh sách", "Không", "Trống",
     "Dạng “Tên nhân viên - Mã phòng - Mã nhân viên”, lọc theo Phòng ban đang chọn. Icon ⓘ."),
    ("Khách hàng", "Dropdown", "Enable", "Tối thiểu 2 ký tự", "Không", "Trống",
     "Tìm theo mã hoặc tên trong các khách có việc trong phạm vi."),
    ("Loại", "Dropdown", "Enable", "Danh sách 2 giá trị", "Không", "Trống", "Nhu cầu / Dự án TKT."),
    ("Tiến trình dự án", "Dropdown", "Enable", "Danh sách 8 giá trị, chọn nhiều", "Không", "Trống",
     "Thu thập thông tin dự án … Thực hiện hợp đồng. Chỉ áp cho dự án."),
    ("Lĩnh vực", "Dropdown", "Enable", "Danh sách", "Không", "Trống",
     "Nhu cầu: lĩnh vực của nhu cầu; dự án: lĩnh vực của nhu cầu gốc."),
    ("Hạn theo dõi", "Dropdown", "Enable", "Danh sách 3 giá trị", "Không", "Trống",
     "Sắp hết hạn / Có hạn theo dõi / Không có hạn. Chỉ áp cho nhu cầu. Icon ⓘ."),
    ("Nút Tìm kiếm", "Button", "Enable", "–", "–", "Hiển thị", "Tải lại báo cáo theo bộ lọc hiện tại."),
    ("Nút Xóa lọc", "Button", "Enable", "–", "–", "Hiển thị", "Đưa mọi ô về mặc định (giữ công ty bị khoá)."),
])
d.p("2.2.4 Danh sách event và xử lý event")
d.event_table([
    ("Chọn / bỏ giá trị ở một ô lọc", "Change",
     "Before:\n– Ô Công ty bị khoá thì bỏ qua thay đổi.\n"
     "During:\n– Xoá các ô phụ thuộc theo quy tắc (Công ty → Phòng ban, Sales; Phòng ban → Sales; Loại → Tiến "
     "trình hoặc Hạn).\n"
     "After:\n– Tải lại danh mục ô lọc và báo cáo, về trang 1."),
    ("Gõ tìm khách hàng", "Keypress", "During:\n– Từ 2 ký tự trở lên mới hiện kết quả (tối đa 20 khách)."),
    ("Bấm Tìm kiếm", "Click", "After:\n– Tải lại báo cáo, về trang 1."),
    ("Bấm Xóa lọc", "Click", "After:\n– Mọi ô về mặc định, tải lại báo cáo."),
])
d.p("2.2.5 Cách lấy dữ liệu của ô lọc")
d.data_table([
    ("Ô Công ty", "Công ty nơi Sales phụ trách ĐANG làm việc (không phải công ty ghi trên dự án / meeting). Chỉ "
     "người có V1 mới đổi được.",
     "Phòng ban / công ty lấy theo nơi SALES phụ trách ĐANG làm việc tại thời điểm xem — không theo phòng ghi "
     "trên dự án."),
    ("Ô Phòng ban", "Phòng nơi Sales phụ trách đang làm việc.",
     "Phòng ban / công ty lấy theo nơi SALES phụ trách ĐANG làm việc tại thời điểm xem — không theo phòng ghi "
     "trên dự án."),
    ("Ô Sales phụ trách", "Nhu cầu: người nhận bàn giao, chưa bàn giao thì người chủ trì meeting. Dự án: Sales "
     "chủ trì của dự án.",
     "Sales phụ trách nhu cầu = người nhận bàn giao, chưa bàn giao thì là người chủ trì meeting. Dự án: Sales "
     "chủ trì của dự án."),
    ("Ô Hạn theo dõi", "Sắp hết hạn = như ô “Sắp hết hạn theo dõi” (2.1.6); Có hạn = N > 0; Không có hạn = N = 0. "
     "Đang chọn ô này thì dự án không hiện.",
     "Chỉ áp cho nhu cầu. Sắp hết hạn = đã vào số ngày cảnh báo trước khi đóng nhu cầu."),
])

# ----------------------------------------------------------------- 2.3
d.h3("2.3 Cài đặt bộ lọc")
d.p("2.3.1 Biểu đồ Usecase")
d.uc_figure("FR-03", "Cài đặt bộ lọc", "view",
            [("include", "Lưu cấu hình theo từng người dùng"), ("extend", "Khôi phục cấu hình mặc định")],
            actor="Người dùng đã đăng nhập", caption="Biểu đồ Use Case — FR-03 Cài đặt bộ lọc")
d.p("2.3.2 Giới thiệu")
d.rule_ref("- Cấu hình bộ lọc. Chỉ bổ sung danh sách tiêu chí lọc riêng của Báo cáo tổng hợp CSKH tiềm năng.",
           anchor="excel")
d.intro_table(
    ten="Cài đặt bộ lọc",
    mota="Cho mỗi người dùng tự chọn các ô lọc hiển thị và thứ tự của chúng. Cấu hình lưu riêng cho màn hình này.",
    tacnhan="Người dùng đã đăng nhập",
    dieukien="Đang ở màn Báo cáo tổng hợp CSKH tiềm năng.",
    chinh="1. Người dùng bấm nút Cài đặt bộ lọc.\n"
          "2. Hệ thống mở cửa sổ với 8 tiêu chí, đánh số và tích theo cấu hình đang lưu.\n"
          "3. Người dùng tích/bỏ tích, kéo biểu tượng ⠿ để đổi thứ tự.\n"
          "4. Người dùng bấm Lưu → hệ thống lưu cấu hình, đóng cửa sổ và vẽ lại khối lọc.",
    phu="• Bấm Khôi phục mặc định → về thứ tự gốc, tích đủ 8 tiêu chí; phải bấm Lưu mới ghi.\n"
        "• Bấm Đóng hoặc × → bỏ mọi thay đổi chưa lưu.\n"
        "• Ẩn một ô đang có giá trị → giá trị của ô đó được xoá khỏi bộ lọc.",
    dacbiet=None)
d.p("2.3.3 Layout màn hình")
d.layout(menu=MENU + " => Cài đặt bộ lọc", modal="Cài đặt bộ lọc", shot=shot("03-cai-dat-bo-loc.png"),
         shot_caption="Cửa sổ Cài đặt bộ lọc với đủ 8 tiêu chí")
d.p("2.3.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Tiêu đề cửa sổ", "Label", "Hiển thị", "–", "–", "Cài đặt bộ lọc", "Kèm icon bánh răng."),
    ("Dòng hướng dẫn", "Label", "Hiển thị", "–", "–", "Hiển thị",
     "“Tích chọn trường lọc muốn hiển thị; kéo ⠿ để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”"),
    ("Ô tích từng tiêu chí", "Checkbox", "Enable", "Danh sách 8 tiêu chí", "Không", "Theo cấu hình đã lưu",
     "Công ty, Phòng ban, Sales phụ trách, Khách hàng, Loại, Tiến trình dự án, Lĩnh vực, Hạn theo dõi."),
    ("Tay kéo ⠿", "Icon Button", "Enable", "–", "–", "Hiển thị", "Kéo để đổi thứ tự."),
    ("Nút Lưu", "Button", "Enable", "–", "–", "Hiển thị", "Lưu cấu hình."),
    ("Nút Khôi phục mặc định", "Button", "Enable", "–", "–", "Hiển thị", "Chưa ghi, phải bấm Lưu."),
    ("Nút Đóng / ×", "Button", "Enable", "–", "–", "Hiển thị", "Đóng, bỏ thay đổi chưa lưu."),
])
d.p("2.3.5 Danh sách event và xử lý event")
d.event_table([
    ("Bấm Cài đặt bộ lọc", "Click", "After:\n– Mở cửa sổ, nạp cấu hình đang lưu."),
    ("Bấm Lưu", "Click",
     "During:\n– Ghi cấu hình (tiêu chí hiển thị + thứ tự) cho người dùng hiện tại.\n"
     "After:\n– Thành công: đóng cửa sổ, vẽ lại khối lọc. Lỗi: báo lỗi, giữ cửa sổ."),
    ("Bấm Khôi phục mặc định", "Click", "After:\n– Đưa danh sách về thứ tự gốc, tích đủ 8 tiêu chí."),
])

# ----------------------------------------------------------------- 2.4
d.h3("2.4 Chọn cấp xem và bung / thu gọn dòng")
d.p("2.4.1 Giới thiệu")
d.rule_ref("- Màn Danh sách và Cấu hình cột. Chỉ bổ sung cách bung / thu gọn bảng cây của Báo cáo tổng hợp "
           "CSKH tiềm năng.", anchor="list")
d.intro_table(
    ten="Chọn cấp xem và bung / thu gọn dòng",
    mota="Chọn bảng cây hiển thị sẵn tới cấp nào, hoặc bung / thu từng dòng bằng mũi tên. Chỉ là cách xem, "
         "không tải lại số liệu.",
    tacnhan=TACNHAN,
    dieukien="Bảng có dữ liệu.",
    chinh="1. Người dùng mở ô chọn cấp trong tiêu đề cột Nội dung theo dõi.\n"
          "2. Người dùng chọn: Chỉ Phòng ban / Đến Sales / Đến Khách hàng / Tất cả cấp (đến Nhu cầu / Dự án).\n"
          "3. Hệ thống bung toàn bộ các dòng tới đúng cấp đã chọn trên trang đang xem.",
    phu="• Bấm mũi tên ở một dòng → chỉ bung / thu dòng đó.\n"
        "• Đổi trang, đổi bộ lọc → bảng áp lại đúng cấp đang chọn.",
    dacbiet=None)
d.p("2.4.2 Layout màn hình")
d.layout(menu=MENU, shot=shot("04-tat-ca-cap.png"),
         shot_caption="Cấp xem “Tất cả cấp”: bung tới dòng nhu cầu / dự án")
d.p("2.4.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Ô chọn cấp xem", "Dropdown", "Enable", "Danh sách 4 giá trị", "Có", "Đến Sales",
     "Chỉ Phòng ban / Đến Sales / Đến Khách hàng / Tất cả cấp (đến Nhu cầu / Dự án)."),
    ("Mũi tên bung / thu", "Icon Button", "Enable", "–", "–", "Theo cấp đang chọn",
     "Ở dòng Phòng, Sales, Khách hàng; xoay xuống khi đang bung."),
    ("Thụt lề và vạch cấp", "Label", "Hiển thị", "4 cấp", "–", "Hiển thị",
     "Mỗi cấp lùi thêm một nấc, vạch trái nhạt dần theo cấp; dòng lá chữ xám."),
])
d.p("2.4.4 Danh sách event và xử lý event")
d.event_table([
    ("Đổi ô chọn cấp xem", "Change", "After:\n– Bung / thu toàn bộ dòng của trang đang xem theo cấp mới."),
    ("Bấm mũi tên ở một dòng", "Click", "After:\n– Bung hoặc thu riêng dòng đó."),
])

# ----------------------------------------------------------------- 2.5
d.h3("2.5 Xem danh sách chi tiết")
d.p("2.5.1 Giới thiệu")
d.rule_ref("- Màn Danh sách, Sắp xếp dữ liệu bảng và Phân trang. Chỉ bổ sung các quy tắc riêng của popup danh "
           "sách chi tiết.", anchor="list")
d.intro_table(
    ten="Xem danh sách chi tiết",
    mota="Popup liệt kê phẳng từng nhu cầu / dự án đứng sau con số vừa bấm, cùng phạm vi quyền và bộ lọc của báo "
         "cáo đang hiển thị.",
    tacnhan=TACNHAN,
    dieukien="Báo cáo đã tải xong; người dùng bấm một con số khác 0.",
    chinh="1. Người dùng bấm một con số (khối tổng hợp, dòng TỔNG, dòng Phòng / Sales / Khách hàng).\n"
          "2. Hệ thống mở popup, tải toàn bộ dòng của con số đó.\n"
          "3. Popup hiển thị danh sách, mặc định 20 dòng / trang.",
    phu="• Bấm số của một tiến trình → popup chỉ gồm dự án ở tiến trình đó, ẩn ô lọc Tiến trình.\n"
        "• Bấm số nhu cầu → ẩn ô lọc Loại và Tiến trình dự án.\n"
        "• Bấm số ở dòng Phòng / Sales → ẩn ô lọc Sales; nhóm “Chưa xác định” vẫn mở đúng tập của nhóm đó.\n"
        "• Mỗi lần mở là trạng thái sạch (không giữ lọc / sắp / trang của lần trước).",
    dacbiet=None)
d.p("2.5.2 Layout màn hình")
d.layout(menu=MENU, modal="Danh sách chi tiết", shot=shot("05-popup-chi-tiet.png"),
         shot_caption="Popup danh sách chi tiết mở từ số nhu cầu của dòng TỔNG")
d.p("2.5.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Đầu popup", "Label", "Hiển thị", "–", "Theo con số đã bấm",
     "“Bạn đang xem: <phạm vi> · <loại>” + dòng “a nhu cầu · b dự án TKT · Đang theo dõi tại <ngày giờ>”."),
    ("Nút Phóng to / ×", "Icon Button", "Enable", "–", "Hiển thị", "Phóng toàn màn hình / đóng popup."),
    ("Ô tìm", "Textbox", "Enable", "0–255 ký tự", "Trống", "Tìm theo khách hàng / dự án / meeting / Sales (FR-06)."),
    ("Ô lọc Loại · Sales phụ trách · Tiến trình dự án", "Dropdown", "Enable / Ẩn", "Danh sách", "Trống",
     "Danh mục lấy từ chính các dòng đang xem; ô đã bị con số cố định thì ẩn (FR-06)."),
    ("Dòng đếm “x / y dòng”", "Label", "Hiển thị", "≥ 0", "Theo dữ liệu", "x = sau lọc trong popup, y = tổng của con số."),
    ("Bảng danh sách", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "STT · Loại · Nội dung · Khách hàng · Sales phụ trách · Trạng thái · Giá trị dự kiến · Mốc thời gian · "
     "Hạn theo dõi · Nguồn. Cột có mũi tên sắp xếp."),
    ("Phân trang", "Pagination", "Enable", "Theo lựa chọn", "20 dòng / trang", "“Hiển thị a–b / N dòng”."),
    ("Nút In danh sách · Xuất Excel danh sách · Đóng", "Button", "Enable", "–", "Hiển thị", "FR-09, FR-10; Đóng tắt popup."),
], required=False)
d.p("2.5.4 Danh sách event và xử lý event")
d.event_table([
    ("Mở popup", "System",
     "During:\n– Tải toàn bộ dòng của con số đã bấm theo bộ lọc của báo cáo đang hiển thị (tải lặp từng lượt 500 dòng).\n"
     "After:\n– Hiển thị trang 1."),
    ("Bấm mã dự án", "Click", "After:\n– Mở chi tiết dự án ở tab mới."),
    ("Bấm mã meeting ở cột Nguồn", "Click", "After:\n– Mở panel chi tiết meeting NỔI TRÊN popup (FR-07)."),
    ("Bấm Đóng / ×", "Click", "After:\n– Đóng popup, giữ nguyên báo cáo."),
])
d.p("2.5.5 Quy tắc hiển thị")
d.bullets([
    "Số dòng của popup luôn bằng con số đã bấm (trước khi lọc trong popup).",
    "Ô chữ dài (Nội dung, Khách hàng, Sales) được xuống dòng trong ô; các cột còn lại một dòng.",
])
d.p("2.5.6 Cách lấy dữ liệu và giải thích chỉ tiêu")
d.p("Popup không có icon ⓘ riêng; các cột dùng đúng cách tính của báo cáo (2.1.6). Bảng dưới mô tả cách lấy "
    "dữ liệu của từng cột trong popup.")
d.data_table([
    ("Tập dòng của popup", "Các nhu cầu / dự án của tập dữ liệu báo cáo, thu hẹp theo phạm vi dòng đã bấm (Phòng, "
     "Sales, Khách hàng) và theo chỉ tiêu đã bấm (Loại, Sắp hết hạn, một Tiến trình).", "—"),
    ("Đầu popup — a nhu cầu · b dự án TKT", "Đếm số dòng nhu cầu và số dòng dự án trong tập dòng của popup.", "—"),
    ("Cột Loại", "Nhu cầu / Dự án TKT.", "—"),
    ("Cột Nội dung", "Nhu cầu: Lĩnh vực ▸ Nhóm ngành. Dự án: mã dự án + tên dự án.", "—"),
    ("Cột Khách hàng", "Tên + mã khách hàng của nhu cầu (khách của meeting) / của dự án.", "—"),
    ("Cột Sales phụ trách", "“Tên - Mã phòng - Mã nhân viên” của Sales phụ trách; phòng là phòng Sales đang làm "
     "việc. Chưa xác định thì để trống.", "—"),
    ("Cột Trạng thái", "Nhu cầu: Đang theo dõi. Dự án: tiến trình hiện tại.", "—"),
    ("Cột Giá trị dự kiến", "Nhu cầu: giá trị dự kiến của nhu cầu. Dự án: giá trị hợp đồng dự kiến.", "—"),
    ("Cột Mốc thời gian", "Nhu cầu: ngày dự kiến triển khai (ghi chú “dự kiến triển khai”). Dự án: ngày khách hàng "
     "cần giải pháp (ghi chú “KH cần giải pháp”).", "—"),
    ("Cột Hạn theo dõi", "Như cột Hạn theo dõi của báo cáo (2.1.6); dự án để trống.", "—"),
    ("Cột Nguồn", "Như cột Nguồn của báo cáo (2.1.6).", "—"),
])

# ----------------------------------------------------------------- 2.6
d.h3("2.6 Lọc và sắp xếp trong danh sách chi tiết")
d.p("2.6.1 Giới thiệu")
d.rule_ref("- Kịch bản tìm kiếm, Bộ lọc và Sắp xếp dữ liệu bảng. Chỉ bổ sung các ô lọc riêng của popup danh sách "
           "chi tiết.", anchor="search")
d.intro_table(
    ten="Lọc và sắp xếp trong danh sách chi tiết",
    mota="Lọc và sắp xếp NGAY TRONG popup trên tập dòng đã tải, không tải lại dữ liệu.",
    tacnhan=TACNHAN,
    dieukien="Popup danh sách chi tiết đang mở.",
    chinh="1. Người dùng gõ ô tìm hoặc chọn ô lọc → danh sách lọc ngay, về trang 1.\n"
          "2. Người dùng bấm tiêu đề cột có mũi tên → sắp tăng / giảm dần.",
    phu="• Ô tìm không phân biệt hoa thường và dấu, tìm trong: khách hàng (tên, mã), mã / tên dự án, mã meeting, "
        "Sales, nội dung.\n"
        "• Có ô lọc đang áp → hiện nút Xoá lọc (icon làm mới).\n"
        "• Ô trống luôn xếp cuối khi sắp xếp.",
    dacbiet=None)
d.p("2.6.2 Layout màn hình")
d.layout(menu=MENU, modal="Danh sách chi tiết", shot=shot("05-popup-chi-tiet.png"),
         shot_caption="Ô tìm, ô lọc và tiêu đề cột sắp xếp của popup danh sách chi tiết")
d.p("2.6.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Ô tìm", "Textbox", "Enable", "0–255 ký tự", "Không", "Trống", "Placeholder “Tìm khách hàng / dự án / meeting / Sales…”."),
    ("Ô Loại", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Trống", "Ẩn khi con số đã cố định loại."),
    ("Ô Sales phụ trách", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Trống",
     "Danh sách Sales có trong popup; ẩn khi con số đã cố định Sales."),
    ("Ô Tiến trình dự án", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Trống",
     "Ẩn khi con số là nhu cầu hoặc là một tiến trình."),
    ("Nút Xoá lọc", "Icon Button", "Enable / Ẩn", "–", "–", "Ẩn", "Chỉ hiện khi có ô lọc đang áp."),
    ("Tiêu đề cột sắp xếp", "Icon Button", "Enable", "–", "–", "Chưa sắp", "Bấm lần lượt: tăng → giảm dần."),
])
d.p("2.6.4 Danh sách event và xử lý event")
d.event_table([
    ("Gõ ô tìm / chọn ô lọc", "Change", "After:\n– Lọc tại chỗ, về trang 1, cập nhật dòng đếm x / y."),
    ("Bấm tiêu đề cột", "Click", "After:\n– Sắp xếp trên toàn bộ dòng đã lọc rồi mới cắt trang."),
    ("Bấm Xoá lọc", "Click", "After:\n– Bỏ mọi ô lọc của popup."),
])

# ----------------------------------------------------------------- 2.7
d.h3("2.7 Xem chi tiết meeting")
d.p("2.7.1 Giới thiệu")
d.rule_ref("- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung khối thông tin riêng khi mở từ Báo cáo tổng hợp CSKH "
           "tiềm năng.", anchor="detail")
d.intro_table(
    ten="Xem chi tiết meeting",
    mota="Panel bên phải hiển thị chi tiết meeting (thông tin cuộc họp, kết luận, thông tin khác) kèm khối thông "
         "tin của chính dòng đã bấm: “Nhu cầu làm dự án” hoặc “Dự án TKT”.",
    tacnhan=TACNHAN,
    dieukien="Người dùng bấm mã meeting ở cột Nguồn (bảng báo cáo hoặc popup danh sách chi tiết).",
    chinh="1. Người dùng bấm mã meeting.\n"
          "2. Hệ thống kiểm quyền xem meeting.\n"
          "3. Panel mở, đầu panel nền gradient; mở từ popup thì panel nổi trên popup.",
    phu="• Người có V1/V2/V3 xem được meeting có nhu cầu trong phạm vi quyền báo cáo (dù không chủ trì / tham dự).\n"
        "• Không đủ quyền → hệ thống báo không có quyền, panel không hiện nội dung.\n"
        "• Bấm ra ngoài panel / nút đóng → đóng panel, popup bên dưới giữ nguyên.",
    dacbiet=None)
d.p("2.7.2 Layout màn hình")
d.layout(menu=MENU, modal="Chi tiết meeting", shot=shot("06-panel-meeting.png"),
         shot_caption="Panel chi tiết meeting mở từ popup, có khối “Nhu cầu làm dự án”")
d.p("2.7.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Đầu panel", "Label", "Hiển thị", "–", "Theo dữ liệu", "Tên meeting, nền gradient của báo cáo."),
    ("Khối Thông tin cuộc họp / Kết luận & ghi chú / Thông tin khác", "Text", "Read-only", "–", "Theo dữ liệu",
     "Nội dung chuẩn của panel meeting dùng chung."),
    ("Khối Nhu cầu làm dự án (dòng nhu cầu)", "Text", "Read-only", "–", "Theo dữ liệu",
     "Lĩnh vực / Nhóm ngành · Trạng thái · Giá trị dự kiến · Dự kiến triển khai · Hạn theo dõi."),
    ("Khối Dự án TKT (dòng dự án)", "Text", "Read-only", "–", "Theo dữ liệu",
     "Dự án (mã - tên) · Tiến trình · Giá trị HĐ dự kiến · KH cần giải pháp."),
    ("Nút Xem biên bản / Sửa", "Button", "Enable / Ẩn", "–", "Theo quyền meeting",
     "Theo quy tắc của màn meeting."),
], required=False)
d.p("2.7.4 Danh sách event và xử lý event")
d.event_table([
    ("Bấm mã meeting", "Click",
     "Before:\n– Kiểm quyền xem meeting: người tạo / chủ trì / thành viên / quyền xem meeting theo cấp; hoặc quyền "
     "báo cáo V1 (mọi meeting có nhu cầu), V2 (Sales của nhu cầu ở công ty hiện tại), V3 (Sales thuộc phòng được "
     "quản lý).\n– Không đủ quyền → báo không có quyền và dừng.\n"
     "After:\n– Mở panel với nội dung meeting và khối thông tin của dòng."),
    ("Bấm Xem biên bản", "Click", "After:\n– Mở popup xem trước biên bản cuộc họp."),
])

# ----------------------------------------------------------------- 2.8
d.h3("2.8 Xem lịch sử meeting với khách hàng")
d.p("2.8.1 Giới thiệu")
d.rule_ref("- Màn Danh sách và Phân trang. Popup dùng lại nguyên của Báo cáo kết quả chăm sóc khách hàng tiềm "
           "năng.", anchor="list")
d.intro_table(
    ten="Xem lịch sử meeting với khách hàng",
    mota="Popup liệt kê các meeting đã Hoàn thành với khách hàng, sắp cũ → mới.",
    tacnhan=TACNHAN,
    dieukien="Dòng khách hàng có ngày ở cột Lần chăm sóc gần nhất.",
    chinh="1. Người dùng bấm ngày ở cột Lần chăm sóc gần nhất.\n"
          "2. Hệ thống mở popup “Lịch sử meeting với khách hàng”, tải meeting Hoàn thành của khách.\n"
          "3. Người dùng bấm tên meeting để mở chi tiết ở tab mới, hoặc icon Xem biên bản.",
    phu="• Phạm vi meeting trong popup theo quyền của Báo cáo kết quả chăm sóc khách hàng tiềm năng (dùng lại "
        "popup), nên có thể ít hơn số meeting tính vào “Lần chăm sóc gần nhất”.\n"
        "• Meeting chưa lập biên bản → không hiện icon Xem biên bản.",
    dacbiet=None)
d.p("2.8.2 Layout màn hình")
d.layout(menu=MENU, modal="Lịch sử meeting với khách hàng", shot=shot("07-lich-su-meeting.png"),
         shot_caption="Popup lịch sử meeting với khách hàng")
d.p("2.8.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Tiêu đề popup", "Label", "Hiển thị", "–", "Theo dữ liệu", "“Lịch sử meeting với khách hàng” + “Khách hàng: <tên>”."),
    ("Bảng meeting", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "STT · Tên meeting (kèm icon Xem biên bản) · Thời gian họp (Từ–Đến) · Người chủ trì · Người liên hệ KH · "
     "Nhu cầu (Có/Không)."),
    ("Phân trang", "Pagination", "Enable", "Theo lựa chọn", "20 dòng / trang", "–"),
    ("Nút đóng ×", "Icon Button", "Enable", "–", "Hiển thị", "Đóng popup."),
], required=False)
d.p("2.8.4 Danh sách event và xử lý event")
d.event_table([
    ("Bấm ngày Lần chăm sóc gần nhất", "Click", "After:\n– Mở popup, tải meeting Hoàn thành của khách, cũ → mới."),
    ("Bấm tên meeting", "Click", "After:\n– Mở chi tiết meeting ở tab mới."),
    ("Bấm icon Xem biên bản", "Click", "After:\n– Mở popup xem trước biên bản."),
])

# ----------------------------------------------------------------- 2.9
d.h3("2.9 In danh sách")
d.p("2.9.1 Biểu đồ Usecase")
d.uc_figure("FR-09", "In danh sách", "io",
            [("include", "Chọn chế độ in: bảng tổng hợp / danh sách chi tiết"),
             ("include", "Lấy toàn bộ dữ liệu theo bộ lọc đang hiển thị"),
             ("extend", "In danh sách từ popup chi tiết")],
            actor=ACT_QL, caption="Biểu đồ Use Case — FR-09 In danh sách")
d.p("2.9.2 Giới thiệu")
d.rule_ref("- Thông báo và UI/UX. Chỉ bổ sung bố cục và dữ liệu riêng của bản in Báo cáo tổng hợp CSKH tiềm năng.",
           anchor="notice")
d.intro_table(
    ten="In danh sách",
    mota="In khổ A4 ngang qua popup xem trước, ở 2 chế độ: In bảng tổng hợp (cây Phòng ▸ Sales ▸ Khách hàng ▸ "
         "nhu cầu / dự án, đủ mọi phòng) hoặc In danh sách chi tiết (mỗi nhu cầu / dự án một dòng).",
    tacnhan=TACNHAN,
    dieukien="Đang ở màn báo cáo (nút ở thanh tiêu đề) hoặc popup danh sách chi tiết (nút ở chân popup).",
    chinh="1. Người dùng bấm In danh sách ở thanh tiêu đề.\n"
          "2. Hệ thống mở cửa sổ chọn chế độ, mặc định In bảng tổng hợp.\n"
          "3. Người dùng chọn chế độ và bấm In.\n"
          "4. Hệ thống dựng bản in theo bộ lọc của báo cáo ĐANG HIỂN THỊ, lấy toàn bộ dữ liệu (không theo trang, "
          "không theo cấp đang bung).\n"
          "5. Popup xem trước hiện bản in; bấm In để mở hộp thoại in của trình duyệt.",
    phu="• Bấm In danh sách ở chân popup chi tiết → in danh sách chi tiết đúng phạm vi + bộ lọc của popup, kèm "
        "dòng phạm vi (tiêu đề popup).\n"
        "• Danh sách vượt 2,000 dòng → không in, nhắc thu hẹp bộ lọc hoặc dùng Xuất Excel.\n"
        "• Bấm Hủy hoặc × ở cửa sổ chọn chế độ → đóng, không in.",
    dacbiet="Bản in có letterhead công ty, tiêu đề, dòng “Đang theo dõi tại <ngày giờ>”, dòng Tổng cộng và Ngày "
            "in. Số dùng dấu phẩy ngăn cách hàng nghìn.")
d.p("2.9.3 Layout màn hình")
d.layout(menu=MENU + " => In danh sách", modal="In danh sách", shot=shot("08-in-chon-che-do.png"),
         shot_caption="Cửa sổ chọn chế độ In danh sách")
d.figure(shot("09-ban-in-bang.png"), "Bản xem trước In bảng tổng hợp", width_in=6.2)
d.figure(shot("10-ban-in-chi-tiet.png"), "Bản xem trước In danh sách chi tiết", width_in=6.2)
d.p("2.9.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Nút In danh sách (thanh tiêu đề)", "Button", "Enable", "–", "–", "Hiển thị", "Mở cửa sổ chọn chế độ."),
    ("Dòng ghi chú cửa sổ", "Label", "Hiển thị", "–", "–", "Hiển thị",
     "“Bản in A4 ngang, bám đúng bộ lọc báo cáo đang hiển thị.”"),
    ("Chế độ in", "Radio", "Enable", "Danh sách 2 giá trị", "Có", "In bảng tổng hợp",
     "In bảng tổng hợp / In danh sách chi tiết, mỗi lựa chọn có dòng mô tả."),
    ("Nút In · Hủy", "Button", "Enable", "–", "–", "Hiển thị", "In dựng bản xem trước; Hủy đóng cửa sổ."),
    ("Bản in bảng tổng hợp", "Table/Grid", "Read-only", "–", "–", "Theo dữ liệu",
     "Tiêu đề BÁO CÁO TỔNG HỢP CHĂM SÓC KHÁCH HÀNG TIỀM NĂNG; 10 cột như bảng; dòng TỔNG, Phòng (I), Sales (1), "
     "Khách hàng (1.1), nhu cầu / dự án (1.1.1)."),
    ("Bản in danh sách chi tiết", "Table/Grid", "Read-only", "–", "–", "Theo dữ liệu",
     "Tiêu đề DANH SÁCH NHU CẦU VÀ DỰ ÁN TKT ĐANG THEO DÕI; STT · Loại · Nội dung (kèm mã meeting) · Khách hàng "
     "· Sales phụ trách · Trạng thái · Giá trị dự kiến · Mốc thời gian · Hạn theo dõi."),
    ("Thông báo vượt trần in", "Toast / Alert", "Hiển thị", "> 2,000 dòng", "–", "Ẩn",
     "Nhắc thu hẹp bộ lọc hoặc dùng Xuất Excel."),
])
d.p("2.9.5 Danh sách event và xử lý event")
d.event_table([
    ("Bấm In danh sách (thanh tiêu đề)", "Click",
     "Before:\n– Báo cáo chưa tải xong → báo “Báo cáo chưa tải xong, vui lòng thử lại.”\n"
     "After:\n– Mở cửa sổ chọn chế độ."),
    ("Bấm In trong cửa sổ chọn chế độ", "Click",
     "During:\n– Dựng toàn bộ dữ liệu theo bộ lọc của báo cáo đang hiển thị; vượt 2,000 dòng → chỉ trả thông báo.\n"
     "After:\n– Mở popup xem trước."),
    ("Bấm In danh sách ở chân popup chi tiết", "Click",
     "After:\n– Mở xem trước danh sách chi tiết theo phạm vi + bộ lọc của popup."),
])

# ----------------------------------------------------------------- 2.10
d.h3("2.10 Xuất Excel")
d.p("2.10.1 Biểu đồ Usecase")
d.uc_figure("FR-10", "Xuất Excel", "io",
            [("include", "Lấy toàn bộ dữ liệu theo bộ lọc đang hiển thị"),
             ("extend", "Xuất danh sách chi tiết từ popup")],
            actor=ACT_QL, caption="Biểu đồ Use Case — FR-10 Xuất Excel")
d.p("2.10.2 Giới thiệu")
d.rule_ref("- Quy tắc Excel. Chỉ bổ sung bộ cột và cách trình bày cây của file Excel Báo cáo tổng hợp CSKH tiềm "
           "năng.", anchor="excel")
d.intro_table(
    ten="Xuất Excel",
    mota="Tải file Excel của bảng tổng hợp (đủ mọi cấp, nút ở thanh tiêu đề) hoặc của danh sách chi tiết (nút ở chân "
         "popup), lấy toàn bộ dữ liệu theo bộ lọc.",
    tacnhan=TACNHAN,
    dieukien="Đang ở màn báo cáo hoặc popup danh sách chi tiết.",
    chinh="1. Người dùng bấm Xuất Excel ở thanh tiêu đề.\n"
          "2. Hệ thống dựng file bảng tổng hợp theo bộ lọc đang hiển thị, đủ mọi cấp.\n"
          "3. Trình duyệt tải file “bao-cao-tong-hop-cskh-tiem-nang.xlsx”.",
    phu="• Bấm Xuất Excel danh sách ở chân popup → tải “danh-sach-cskh-tiem-nang-dang-theo-doi.xlsx” (10 cột, có dòng "
        "phạm vi).\n• Lỗi khi tạo đường tải → báo “Lỗi khi xuất Excel”.",
    dacbiet="File Excel không giới hạn số dòng. Ô tiền là số thật (cộng / lọc được trong Excel), hiển thị dấu phẩy "
            "ngăn cách hàng nghìn. Đầu file có logo công ty, tiêu đề và dòng “Đang theo dõi tại <ngày giờ>”.")
d.p("2.10.3 Layout màn hình")
d.layout(menu=MENU + " => Xuất Excel", shot=shot("11-xuat-excel.png"),
         shot_caption="Nút Xuất Excel trên thanh tiêu đề khối lọc")
d.p("2.10.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Nút Xuất Excel (thanh tiêu đề)", "Button", "Enable", "–", "–", "Hiển thị", "Tải file bảng tổng hợp."),
    ("Nút Xuất Excel danh sách (chân popup)", "Button", "Enable", "–", "–", "Hiển thị", "Tải file danh sách chi tiết."),
    ("File bảng tổng hợp", "Table/Grid", "Read-only", "–", "–", "Theo dữ liệu",
     "10 cột như bảng; dòng TỔNG, Phòng, Sales, Khách hàng, nhu cầu / dự án; cột Loại dòng cha ghi “a nhu cầu · b dự án”."),
    ("File danh sách chi tiết", "Table/Grid", "Read-only", "–", "–", "Theo dữ liệu",
     "STT · Loại · Nội dung · Khách hàng · Sales phụ trách · Trạng thái · Giá trị dự kiến · Mốc thời gian · Hạn "
     "theo dõi · Nguồn."),
])
d.p("2.10.5 Danh sách event và xử lý event")
d.event_table([
    ("Bấm Xuất Excel", "Click",
     "Before:\n– Báo cáo chưa tải xong → báo “Báo cáo chưa tải xong, vui lòng thử lại.”\n"
     "After:\n– Tải file theo bộ lọc của báo cáo đang hiển thị."),
    ("Bấm Xuất Excel danh sách (popup)", "Click", "After:\n– Tải file theo phạm vi + bộ lọc của popup."),
])

# ================================================================= PHẦN 4
d.h1("Phần 4. Quy tắc nghiệp vụ")
d.rule_ref(". Phần này chỉ ghi các quy tắc đặc thù của Báo cáo tổng hợp CSKH tiềm năng; không lặp lại các "
           "quy tắc đã có trong SRS quy tắc chung.",
           anchor="list", head="Quy tắc áp dụng",
           lead="Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ")
d.rule_table([
    ("BR-01", "Số liệu tại thời điểm xem", [
        "– Báo cáo không có kỳ; mỗi lần mở / tải lại là ảnh chụp tại thời điểm đó (hiện ở dòng “Đang theo dõi tại”).",
    ], ["Xem báo cáo", "In", "Xuất Excel"]),
    ("BR-02", "Nhu cầu được tính", [
        "– Nhu cầu ở trạng thái Đang theo dõi, thuộc meeting đã Hoàn thành.",
        "– Không tính nhu cầu đã lập dự án TKT (đã hiện ở dạng dự án) và nhu cầu đã đóng → không đếm trùng.",
    ], ["Xem báo cáo", "Danh sách chi tiết"]),
    ("BR-03", "Dự án được tính", [
        "– Dự án TKT có tiến trình từ Thu thập thông tin dự án tới Thực hiện hợp đồng.",
        "– Không tính Đang tạo, Nghiệm thu và thanh lý hợp đồng, Đóng/Không thực hiện dự án, Kết thúc và lưu trữ.",
    ], ["Xem báo cáo", "Danh sách chi tiết"]),
    ("BR-04", "Sales phụ trách", [
        "– Nhu cầu: người nhận bàn giao; chưa bàn giao thì người chủ trì meeting.",
        "– Dự án: Sales chủ trì của dự án.",
    ], ["Xem báo cáo", "Tìm kiếm và lọc"]),
    ("BR-05", "Phòng / công ty theo nơi Sales đang làm việc", [
        "– Gom cây và lọc quyền theo phòng / công ty Sales ĐANG làm việc; Sales chuyển phòng thì việc đi theo Sales.",
        "– Không dùng phòng ghi trên dự án.",
        "– Không có Sales (hoặc Sales không còn hồ sơ) → nhóm “Chưa xác định phòng ▸ Chưa xác định Sales” cuối bảng.",
    ], ["Xem báo cáo", "Tìm kiếm và lọc"]),
    ("BR-06", "Phạm vi dữ liệu theo quyền", [
        "– V1: mọi công ty, chọn được Công ty. V2: Sales ở công ty hiện tại + việc của mình. V3: Sales thuộc phòng "
        "được phân công quản lý + việc của mình. Không quyền: chỉ việc của mình.",
        "– Có nhiều quyền thì cấp cao nhất thắng; không có ngoại lệ cho Super admin.",
        "– Bản in, Excel, popup cùng phạm vi với màn hình.",
    ], ["Toàn màn"]),
    ("BR-07", "Hạn theo dõi và Sắp hết hạn", [
        "– Hạn = ngày hoàn thành meeting + N ngày (thời gian hiệu lực của Lĩnh vực lấy tại lúc tạo nhu cầu); N = 0 "
        "→ không có hạn.",
        "– Sắp hết hạn khi N > M > 0 và hôm nay ≥ hạn − M; M = “Cảnh báo trước khi đóng nhu cầu” của công ty sở hữu "
        "meeting, chưa cấu hình = 3.",
        "– Cùng luật với lệnh tự đóng nhu cầu và màn danh sách nhu cầu khách hàng.",
    ], ["Xem báo cáo", "Tìm kiếm và lọc", "Danh sách chi tiết"]),
    ("BR-08", "Lần chăm sóc gần nhất", [
        "– Meeting Hoàn thành mới nhất với khách hàng, bất kể ai chủ trì và loại meeting.",
        "– Popup lịch sử dùng lại của Báo cáo kết quả CSKH tiềm năng nên phạm vi meeting trong popup theo quyền "
        "của báo cáo đó.",
    ], ["Xem báo cáo", "Lịch sử meeting"]),
    ("BR-09", "Hai cột giá trị tách riêng", [
        "– Giá trị nhu cầu = tổng giá trị dự kiến của nhu cầu; Giá trị dự án = tổng giá trị hợp đồng dự kiến của "
        "dự án; không cộng lẫn.",
    ], ["Xem báo cáo", "In", "Xuất Excel"]),
    ("BR-10", "Khớp số và ẩn chỉ tiêu bằng 0", [
        "– Tóm tắt, khối tổng hợp, dòng TỔNG, popup, bản in, Excel tính từ cùng một tập dữ liệu.",
        "– Khối tổng hợp không hiện ô Sắp hết hạn và ô tiến trình khi bằng 0; ô tổng của khối luôn hiện.",
    ], ["Xem báo cáo"]),
    ("BR-11", "Quy tắc ô lọc", [
        "– Đổi Công ty xoá Phòng ban, Sales; đổi Phòng ban xoá Sales.",
        "– Loại = Nhu cầu xoá Tiến trình dự án; Loại = Dự án TKT xoá Hạn theo dõi.",
        "– Lọc Lĩnh vực với dự án theo lĩnh vực của nhu cầu gốc; dự án không có nhu cầu gốc không khớp.",
        "– Lọc Hạn theo dõi chỉ áp cho nhu cầu.",
    ], ["Tìm kiếm và lọc"]),
    ("BR-12", "Xem chi tiết meeting từ báo cáo", [
        "– Ngoài quy tắc xem meeting sẵn có, người có V1 xem mọi meeting có nhu cầu; V2 khi Sales của nhu cầu ở "
        "công ty hiện tại; V3 khi Sales thuộc phòng được quản lý.",
        "– Meeting không có nhu cầu: giữ quy tắc cũ.",
    ], ["Xem chi tiết meeting"]),
    ("BR-13", "In và Excel lấy toàn bộ dữ liệu", [
        "– Lấy theo bộ lọc của báo cáo ĐANG HIỂN THỊ, đủ mọi phòng, đủ mọi cấp bất kể cấp đang bung; từ popup thì "
        "theo phạm vi + bộ lọc của popup.",
        "– Bản in A4 ngang, trần 2,000 dòng; Excel không giới hạn.",
    ], ["In danh sách", "Xuất Excel"]),
])


def split_hyperlink_rels(doc):
    """Mỗi đoạn "Quy tắc chung" một liên kết RIÊNG (python-docx gộp hyperlink cùng URL vào 1 quan hệ, khiến
    srs_selfcheck đếm thiếu). Khuôn `.plans/gop-db/bao-cao-theo-doi-giu-hang/gen_srs.py`. KHÔNG đổi URL / anchor."""
    from docx.opc.constants import RELATIONSHIP_TYPE as RT
    from docx.oxml.ns import qn as _qn

    part = doc.part
    seen = set()
    for link in doc.element.body.iter(_qn("w:hyperlink")):
        rid = link.get(_qn("r:id"))
        if rid is None:
            continue
        if rid in seen:
            target = part.rels[rid].target_ref
            new_rid = part.rels._next_rId
            part.rels.add_relationship(RT.HYPERLINK, target, new_rid, is_external=True)
            link.set(_qn("r:id"), new_rid)
        else:
            seen.add(rid)


split_hyperlink_rels(d.doc)
# Máy Mac không có Word COM để cập nhật mục lục -> mở file trong Word rồi Update Field để có số trang.
d.save(update_fields=False)
