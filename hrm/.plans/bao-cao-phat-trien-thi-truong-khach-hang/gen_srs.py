# -*- coding: utf-8 -*-
"""Sinh "SRS - Báo cáo phát triển thị trường - Khách hàng.docx" theo FORM CHUẨN 2026-08-28.

Chạy:  python3 .plans/bao-cao-phat-trien-thi-truong-khach-hang/gen_srs.py
Thư viện dùng chung: .claude/skills/srs-documenter/assets/{srs_docx_lib,srs_uml_render}.py
Ảnh chụp thật (Playwright 1440x900, kỳ "Năm nay"): ptt-kh_shots/ — chỉ để local, không commit.

Nguồn đối chiếu (nhánh gop_db, 03/10/2026):
- FE  hrm-client/pages/assign/report/customer-market-development/ (index + 6 component)
- BE  hrm-api/Modules/Assign/Services/Report/CustomerMarketDevelopmentService.php
      + CustomerMarketDevelopmentPrintService.php + CustomerMarketDevelopmentReportController.php
- Quyền: Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (id 1187-1189)
- Menu: hrm-client/components/subsystem-menu/presale.js (nhóm "Báo cáo thị trường")
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

# Thư viện vẽ UML của skill trỏ cứng font Windows -> trên macOS trỏ lại font hệ thống có đủ
# dấu tiếng Việt. KHÔNG sửa file dùng chung trong .claude/skills/.
import srs_uml_render as uml  # noqa: E402

if not os.path.exists(uml.F_REG):
    _MAC = "/System/Library/Fonts/Supplemental"
    for _attr, _name in (("F_REG", "Arial.ttf"), ("F_BOLD", "Arial Bold.ttf"),
                         ("F_ITAL", "Arial Italic.ttf")):
        _path = os.path.join(_MAC, _name)
        if os.path.exists(_path):
            setattr(uml, _attr, _path)

import srs_docx_lib  # noqa: E402
from srs_docx_lib import SrsDoc  # noqa: E402

# `part.relate_to()` của python-docx GỘP các liên kết trùng URL vào 1 quan hệ -> 10 đoạn
# "Quy tắc chung" trỏ tới 3 mục chỉ đẻ ra 3 quan hệ, bộ tự kiểm (đếm quan hệ) báo nhầm là thiếu
# liên kết. Mỗi đoạn tạo 1 quan hệ riêng — liên kết vẫn y nguyên, KHÔNG sửa file dùng chung.
_add_hyperlink = srs_docx_lib.add_hyperlink


def _add_hyperlink_rieng(paragraph, url, text):
    link = _add_hyperlink(paragraph, url, text)
    r_id = paragraph.part.rels._next_rId
    paragraph.part.rels.add_relationship(srs_docx_lib.RT.HYPERLINK, url, r_id, is_external=True)
    link.set(srs_docx_lib.qn('r:id'), r_id)
    return link


srs_docx_lib.add_hyperlink = _add_hyperlink_rieng

TEN_MAN = "Báo cáo phát triển thị trường - Khách hàng"
OUT = os.path.join(HERE, "SRS - %s.docx" % TEN_MAN)
SHOTS = os.path.join(HERE, "ptt-kh_shots")
MENU = ("Phân hệ CSKH trước bán => Báo cáo => Báo cáo thị trường => "
        "Báo cáo phát triển thị trường - Khách hàng")

ACTOR_KD = "Nhân viên kinh doanh"
ACTOR_QL = "Trưởng phòng / Ban giám đốc"
TAC_NHAN = "Nhân viên kinh doanh; Trưởng phòng kinh doanh; Ban giám đốc; Người dùng đã đăng nhập"


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(out=OUT, menu=MENU,
           route="/assign/report/customer-market-development",
           full_url="https://hrm.eteksofts.com/assign/report/customer-market-development",
           img_prefix="pttkh_")

# =================================================================== TRANG ĐẦU
d.title_block(TEN_MAN)
d.h2("Mục lục")
d.toc()

# ========================================================= PHẦN 1. GIỚI THIỆU
d.h1("Phần 1. Giới thiệu")

d.h2("1 Mục đích")
d.p("Tài liệu này đặc tả yêu cầu phần mềm cho màn hình %s, nhằm:" % TEN_MAN)
d.bullets([
    "Là căn cứ nghiệm thu chức năng và phân quyền của báo cáo.",
    "Làm rõ cách đếm từng chỉ tiêu (Meeting KH, Hoàn thành, Huỷ, Tỷ lệ HT, KH mới, Nhu cầu, "
    "Giá trị dự kiến) và vì sao số của dòng cha luôn bằng tổng các dòng con.",
    "Làm rõ 3 tiêu chí theo dõi (Thị trường / Khách hàng / Phòng kinh doanh) quyết định cấu trúc "
    "cây của bảng và bộ cột của danh sách chi tiết.",
    "Làm rõ phạm vi dữ liệu theo 3 cấp quyền xem và trường hợp không có quyền nào.",
])

d.h2("2 Thuật ngữ và viết tắt")
d.table(["Thuật ngữ", "Mô tả"], [
    ("Meeting KH", "Cuộc meeting có gắn khách hàng, có ngày họp nằm trong kỳ báo cáo, ở mọi trạng "
                   "thái: Lên lịch, Chốt lịch, Hoàn thành, Hủy."),
    ("Kỳ báo cáo", "Khoảng thời gian xét NGÀY HỌP của meeting và NGÀY TẠO của khách hàng. Có 7 mốc "
                   "dựng sẵn (Ngày hôm nay, Tuần này, Tuần tiếp theo, Tháng này, Tháng tiếp theo, "
                   "Quý này, Năm nay) và Tuỳ chọn."),
    ("Tiêu chí theo dõi", "Cách gom nhóm các dòng của bảng thành cây nhiều cấp. Có 3 tiêu chí: "
                          "Thị trường, Khách hàng, Phòng kinh doanh."),
    ("Thị trường", "Tỉnh/Thành phố của khách hàng, được ghi lại trên meeting tại thời điểm lưu "
                   "meeting. Khách hàng chưa có tỉnh/thành phố được gom vào nhóm "
                   "“Chưa xác định thị trường”."),
    ("Nhân viên chủ trì", "Người chủ trì meeting. Phòng ban, Bộ phận của một meeting lấy theo hồ "
                          "sơ của người chủ trì, không theo người tạo meeting."),
    ("KH mới", "Khách hàng có NGÀY TẠO nằm trong kỳ báo cáo, được tính cho NGƯỜI TẠO khách hàng. "
               "Không cần có meeting trong kỳ vẫn được đếm."),
    ("Nhu cầu", "Meeting mà biên bản họp có ghi nhận ít nhất một nhu cầu đầu tư của khách hàng."),
    ("Giá trị dự kiến", "Tổng giá trị đầu tư dự kiến của các nhu cầu ghi nhận được."),
    ("Lập trước kỳ / Lập trong kỳ", "Chia meeting của kỳ theo NGÀY TẠO meeting: tạo trước ngày "
                                    "đầu kỳ là Lập trước kỳ, còn lại là Lập trong kỳ."),
    ("Popup chi tiết", "Cửa sổ liệt kê từng meeting (hoặc từng khách hàng) đứng sau một con số trên "
                       "báo cáo, mở ra khi bấm vào con số đó."),
    ("Cấp xem", "Số cấp của cây được bung sẵn trên bảng theo dõi."),
], widths=[1.8, 4.2])

# ========================================================= PHẦN 2. PHÂN QUYỀN
d.h1("Phần 2. Phân quyền")

d.h2("1 Danh sách quyền")
d.p("Nhóm quyền thao tác: màn hình không có quyền thao tác riêng. Mọi người dùng đã đăng nhập "
    "đều mở được màn hình và dùng được toàn bộ chức năng (lọc, xem chi tiết, in, xuất Excel); "
    "quyền chỉ quyết định phạm vi dữ liệu nhìn thấy.")

d.p("Nhóm quyền quyết định phạm vi dữ liệu "
    "(xét theo thứ tự ưu tiên từ trên xuống, cấp nào có trước thì áp cấp đó):")
d.table(["Ký hiệu", "Tên quyền", "Phạm vi dữ liệu"], [
    ("V1", "Xem báo cáo phát triển thị trường - khách hàng theo tổng công ty",
     "Toàn bộ meeting và khách hàng mới của mọi công ty. Bộ lọc hiện thêm ô Công ty."),
    ("V2", "Xem báo cáo phát triển thị trường - khách hàng theo công ty",
     "Meeting thuộc công ty đang làm việc của người đăng nhập, cộng meeting do chính mình chủ trì. "
     "Khách hàng mới do nhân viên của công ty đó tạo, cộng khách hàng do chính mình tạo."),
    ("V3", "Xem báo cáo phát triển thị trường - khách hàng theo phòng ban",
     "Meeting thuộc các phòng ban / bộ phận người đăng nhập được phân công quản lý, cộng meeting do "
     "chính mình chủ trì. Khách hàng mới do nhân viên các phòng ban / bộ phận đó tạo, cộng khách "
     "hàng do chính mình tạo."),
    ("—", "(không có cấp nào)",
     "Vẫn mở được màn hình. Chỉ thấy meeting do chính mình chủ trì hoặc mình là thành viên, và "
     "khách hàng mới do chính mình tạo. Ẩn các ô lọc Công ty, Phòng ban, Bộ phận, Nhân viên."),
], widths=[0.8, 2.3, 2.9])

d.h2("2 Ma trận phân quyền")
_ALL = ("✅", "✅", "✅", "✅ (chỉ dữ liệu của mình)")
d.table(["Chức năng", "V1", "V2", "V3", "Không có quyền nào"], [
    ("FR-01 Xem báo cáo",) + _ALL,
    ("FR-02 Tìm kiếm và lọc báo cáo",
     "✅", "✅ (không có ô Công ty)", "✅ (không có ô Công ty)",
     "✅ (chỉ Kỳ, Tiêu chí, Thị trường / Khách hàng, Loại meeting, Trạng thái)"),
    ("FR-03 Cài đặt bộ lọc", "✅", "✅", "✅", "✅"),
    ("FR-04 Chọn cấp xem và bung / thu gọn dòng",) + _ALL,
    ("FR-05 In báo cáo",) + _ALL,
    ("FR-06 Xuất Excel báo cáo",) + _ALL,
    ("FR-07 Xem danh sách chi tiết",) + _ALL,
    ("FR-08 Lọc, sắp xếp và tổng hợp trong danh sách chi tiết",) + _ALL,
    ("FR-09 In danh sách chi tiết",) + _ALL,
    ("FR-10 Xuất Excel danh sách chi tiết",) + _ALL,
], widths=[2.3, 0.7, 0.9, 0.9, 1.2])
d.p("Ghi chú: ba quyền V1, V2, V3 không chặn việc mở màn hình mà chỉ thu hẹp phạm vi dữ liệu. "
    "Bản in, file Excel và popup chi tiết dùng đúng phạm vi dữ liệu của màn hình.")

# ================================================ PHẦN 3. ĐẶC TẢ CHI TIẾT
d.h1("Phần 3. Đặc tả chi tiết theo từng chức năng")

d.h2("1 Sơ đồ UML tổng quan")
d.overview_figure2(
    [(ACTOR_KD, [0, 1]), (ACTOR_QL, [0, 1])],
    [("FR-01", "Xem báo cáo", "view"),
     ("FR-07", "Xem danh sách chi tiết", "view")],
    [("FR-02", "Tìm kiếm và lọc báo cáo", "view", "extend", [0], None),
     ("FR-03", "Cài đặt bộ lọc", "view", "extend", [0], None),
     ("FR-04", "Chọn cấp xem", "view", "extend", [0], None),
     ("FR-05", "In báo cáo", "io", "extend", [0], None),
     ("FR-06", "Xuất Excel báo cáo", "io", "extend", [0], None),
     ("FR-08", "Lọc, sắp xếp, tổng hợp", "view", "extend", [1], None),
     ("FR-09", "In danh sách chi tiết", "io", "extend", [1], None),
     ("FR-10", "Xuất Excel danh sách", "io", "extend", [1], None)],
    "Sơ đồ Use Case tổng quan màn %s" % TEN_MAN)
d.p("Danh sách chi tiết (FR-07) không có lối vào riêng trên menu: nó mở ra khi bấm một con số "
    "trên dải tổng hợp hoặc bảng theo dõi của màn báo cáo (FR-01).")

d.h2("2 Đặc tả chi tiết từng chức năng")

# --------------------------------------------------------------- 2.1 FR-01
d.h3("2.1 Xem báo cáo")
d.p("2.1.1 Giới thiệu")
d.rule_ref("- Màn Danh sách, Phân trang. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả "
           "chi tiết." % TEN_MAN, anchor="list")
d.intro_table(
    ten="Xem báo cáo phát triển thị trường - khách hàng",
    mota="Hiển thị dải tổng hợp của kỳ và bảng theo dõi dạng cây theo tiêu chí đang chọn, đo kế "
         "hoạch và kết quả phát triển thị trường - khách hàng qua các cuộc meeting với khách hàng.",
    tacnhan=TAC_NHAN,
    dieukien="Người dùng đã đăng nhập vào hệ thống.",
    chinh="1. Người dùng vào menu theo đường dẫn ở mục Layout.\n"
          "2. Hệ thống xác định cấp quyền xem (V1 → V2 → V3 → không có quyền).\n"
          "3. Hệ thống áp bộ lọc mặc định: Kỳ báo cáo = Tháng này, Tiêu chí theo dõi = Thị trường.\n"
          "4. Hệ thống tính dải tổng hợp, dòng TỔNG và cây theo dõi trong phạm vi dữ liệu.\n"
          "5. Màn hình hiển thị dải tổng hợp, bảng theo dõi ở cấp “Chỉ <cấp gốc>” và phân trang.",
    phu="• Không có meeting và khách hàng mới nào khớp bộ lọc → bảng hiện dòng "
        "“Không có meeting nào khớp bộ lọc.”, dòng TỔNG mang toàn số 0.\n"
        "• Lỗi khi tải → hiển thị thông báo “Lỗi khi tải dữ liệu”, bảng để trống.\n"
        "• Bấm “Thu gọn” trên dải tổng hợp → ẩn 2 khối chỉ tiêu, chỉ giữ dòng tiêu đề; "
        "bấm “Mở rộng” để hiện lại.\n"
        "• Bấm mũi tên ở đầu dòng → bung / thu gọn riêng dòng đó.\n"
        "• Bấm một con số khác 0 → mở danh sách chi tiết (FR-07). Số 0 hiển thị mờ, không bấm được.")

d.p("2.1.2 Layout màn hình")
d.layout(menu=MENU, shot=shot("01-man-chinh.png"),
         shot_caption="Màn %s, kỳ Năm nay, tiêu chí Thị trường" % TEN_MAN)

d.p("2.1.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Tiêu đề trang", "Label", "Hiển thị", "–", TEN_MAN,
     "Kèm icon ⓘ: “Theo dõi kế hoạch và kết quả phát triển thị trường - khách hàng của các Phòng "
     "ban - Nhân viên thông qua các cuộc meeting với khách hàng.”"),
    ("Nút In báo cáo", "Button", "Enable", "–", "Hiển thị", "Mở popup chọn kiểu in (FR-05)."),
    ("Nút Xuất Excel", "Button", "Enable", "–", "Hiển thị", "Tải file Excel bảng theo dõi (FR-06)."),
    ("Nút Cài đặt bộ lọc", "Button", "Enable", "–", "Hiển thị", "Mở cửa sổ cài đặt bộ lọc (FR-03)."),
    ("Nút Tìm kiếm nâng cao", "Button", "Enable", "–", "Bộ lọc thu gọn",
     "Mở / thu gọn panel bộ lọc (FR-02)."),
    ("Dòng “Tổng hợp kỳ dd/mm/yyyy – dd/mm/yyyy”", "Label", "Read-only", "–", "Theo kỳ",
     "Ghi khoảng ngày của kỳ, số meeting, số khách hàng đã tiếp cận (đếm không trùng) và "
     "“Nhu cầu thu thập N (x.x tỷ)”."),
    ("Nút Thu gọn / Mở rộng", "Button", "Enable", "–", "Mở rộng",
     "Ẩn / hiện 2 khối chỉ tiêu của dải tổng hợp."),
    ("Khối “Kế hoạch meeting trong kỳ”", "Text", "Read-only", "–", "Theo dữ liệu",
     "3 ô: Tổng meeting (kèm số KH), Lập trước kỳ, Lập trong kỳ (kèm tỷ lệ % trên Tổng meeting). "
     "Dòng meta ghi số khách hàng đã tiếp cận."),
    ("Khối “Kết quả phát triển trong kỳ”", "Text", "Read-only", "–", "Theo dữ liệu",
     "3 ô: Meeting hoàn thành, Meeting bị huỷ (kèm tỷ lệ %), Nhu cầu thu thập được (kèm tổng tỷ "
     "đồng). Dòng meta ghi “N KH mới tạo trong kỳ”."),
    ("Icon ⓘ trên khối / ô / tiêu đề cột", "Icon Button", "Hover", "–", "Hiển thị",
     "Rê chuột hiện giải thích cách đếm của chỉ tiêu tương ứng."),
    ("Ô chọn Cấp xem", "Dropdown", "Enable", "Danh sách 4 giá trị", "Chỉ <cấp gốc>", "Xem FR-04."),
    ("Cột STT", "Table/Grid", "Read-only", "–", "Theo vị trí",
     "Đánh số nối chuỗi theo cấp: 1 → 1.1 → 1.1.1. Trang sau tiếp tục số thật (trang 2 bắt đầu "
     "từ 51 khi 50 dòng/trang)."),
    ("Cột Nội dung theo dõi", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "Tên thị trường / khách hàng / phòng ban / bộ phận / nhân viên, thụt lề theo cấp, có mũi tên "
     "bung / thu gọn ở dòng có cấp con."),
    ("Cột Meeting KH", "Table/Grid", "Read-only", "≥ 0", "Theo dữ liệu", "Bấm số để xem danh sách."),
    ("Cột Hoàn thành", "Table/Grid", "Read-only", "≥ 0", "Theo dữ liệu", "Bấm số để xem danh sách."),
    ("Cột Huỷ", "Table/Grid", "Read-only", "≥ 0", "Theo dữ liệu",
     "Bấm số để xem danh sách kèm lý do huỷ."),
    ("Cột Tỷ lệ HT", "Table/Grid", "Read-only", "0.0% – 100.0%", "Theo dữ liệu",
     "Hoàn thành ÷ Meeting KH của chính dòng đó, 1 chữ số thập phân. Không bấm được."),
    ("Cột KH mới", "Table/Grid", "Read-only", "≥ 0", "Theo dữ liệu",
     "Bấm số để xem danh sách khách hàng mới."),
    ("Cột Nhu cầu", "Table/Grid", "Read-only", "≥ 0", "Theo dữ liệu", "Bấm số để xem danh sách."),
    ("Cột Giá trị dự kiến", "Table/Grid", "Read-only", "≥ 0", "Theo dữ liệu",
     "Quy ra tỷ đồng, 1 chữ số thập phân (vd “1.3 tỷ”). Không bấm được."),
    ("Dòng TỔNG", "Table/Grid", "Read-only", "–", "Hiển thị",
     "Luôn đứng đầu bảng, tên là chuỗi cấp của tiêu chí viết hoa (vd “THỊ TRƯỜNG / PHÒNG BAN / "
     "BỘ PHẬN / NHÂN VIÊN”). Mang tổng cả kỳ, không theo trang."),
    ("Phân trang", "Pagination", "Enable", "20 / 50 / 100", "50 dòng / trang",
     "Đếm theo dòng cấp 1; mỗi dòng cấp 1 luôn đi kèm nguyên nhánh con trên cùng một trang. "
     "Nhãn đơn vị là tên cấp 1 (Thị trường / Khách hàng / Phòng ban)."),
    ("Trạng thái rỗng", "Label", "Hiển thị", "–", "Ẩn", "“Không có meeting nào khớp bộ lọc.”"),
    ("Đang tải", "Loading", "Hiển thị", "–", "Ẩn", "“Đang tải dữ liệu...” trong lúc nạp."),
], required=False)

d.p("2.1.4 Danh sách event và xử lý event")
d.event_table([
    ("Mở màn hình", "System",
     "Before:\n– Xác định cấp quyền xem theo thứ tự V1 → V2 → V3 → không có quyền.\n"
     "During:\n– Áp bộ lọc mặc định (Tháng này, Thị trường) và phạm vi dữ liệu.\n"
     "After:\n– Hiển thị dải tổng hợp, dòng TỔNG, cây ở cấp “Chỉ Thị trường”, trang 1.\n"
     "– Lỗi khi tải → hiển thị “Lỗi khi tải dữ liệu”."),
    ("Bấm mũi tên đầu dòng", "Click",
     "After:\n– Bung / thu gọn riêng dòng đó. Ô Cấp xem giữ nguyên lựa chọn."),
    ("Bấm Thu gọn / Mở rộng trên dải tổng hợp", "Click",
     "After:\n– Ẩn / hiện 2 khối chỉ tiêu, nhãn nút đổi giữa “Thu gọn” và “Mở rộng”."),
    ("Bấm con số trên dải tổng hợp hoặc bảng", "Click",
     "Before:\n– Chỉ số khác 0 mới bấm được.\n"
     "After:\n– Mở danh sách chi tiết của đúng dòng + chỉ tiêu đó (FR-07)."),
    ("Đổi trang / đổi số dòng mỗi trang", "Click / Change",
     "After:\n– Hiển thị các dòng cấp 1 của trang mới kèm nhánh con; đổi số dòng thì về trang 1."),
])

# --------------------------------------------------------------- 2.2 FR-02
d.h3("2.2 Tìm kiếm và lọc báo cáo")
d.p("2.2.1 Giới thiệu")
d.rule_ref("- Kịch bản tìm kiếm, Bộ lọc, Dropdown. Chỉ bổ sung các quy tắc riêng của %s tại "
           "phần mô tả chi tiết." % TEN_MAN, anchor="search")
d.intro_table(
    ten="Tìm kiếm và lọc báo cáo",
    mota="Thu hẹp số liệu của báo cáo theo kỳ, tiêu chí theo dõi, thị trường / khách hàng, loại "
         "meeting, trạng thái và cơ cấu tổ chức.",
    tacnhan=TAC_NHAN,
    dieukien="Người dùng đang ở màn báo cáo.",
    chinh="1. Người dùng bấm “Tìm kiếm nâng cao” để mở panel bộ lọc.\n"
          "2. Người dùng chọn giá trị ở một ô lọc.\n"
          "3. Hệ thống tải lại báo cáo ngay theo bộ lọc mới (không cần bấm nút tìm).\n"
          "4. Dải tổng hợp, dòng TỔNG và cây theo dõi cập nhật; bảng về trang 1.",
    phu="• Chọn Kỳ báo cáo = Tuỳ chọn → hiện thêm ô Thời gian để chọn khoảng ngày.\n"
        "• Đổi từ Tuỳ chọn sang kỳ dựng sẵn → ô Thời gian ẩn và khoảng ngày đã chọn bị xoá.\n"
        "• Đổi Tiêu chí theo dõi → cây dựng lại theo tiêu chí mới, Cấp xem về “Chỉ <cấp gốc>”, "
        "giá trị của ô lọc bị ẩn theo tiêu chí bị xoá.\n"
        "• Bấm “Xóa lọc” → mọi ô về mặc định (Tháng này, Thị trường), Cấp xem về mặc định, tải lại.")

d.p("2.2.2 Layout màn hình")
d.layout(menu=MENU + " => Tìm kiếm nâng cao", shot=shot("02-bo-loc.png"),
         shot_caption="Panel bộ lọc báo cáo đang mở")

d.p("2.2.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Kỳ báo cáo", "Dropdown", "Enable", "Danh sách 8 giá trị", "Không", "Tháng này",
     "Ngày hôm nay, Tuần này, Tuần tiếp theo, Tháng này, Tháng tiếp theo, Quý này, Năm nay, "
     "Tuỳ chọn. Không xoá trống được."),
    ("Tiêu chí theo dõi", "Dropdown", "Enable", "Danh sách 3 giá trị", "Không",
     "Thị trường ▸ Phòng ban ▸ Bộ phận ▸ Nhân viên",
     "Thị trường ▸ Phòng ban ▸ Bộ phận ▸ Nhân viên; Khách hàng ▸ Phòng ban ▸ Bộ phận ▸ Nhân viên; "
     "Phòng ban ▸ Bộ phận ▸ Nhân viên ▸ Thị trường. Không xoá trống được."),
    ("Thời gian", "Datepicker", "Enable / Ẩn", "dd/mm/yyyy – dd/mm/yyyy", "Không", "Ẩn",
     "Chỉ hiện khi Kỳ báo cáo = Tuỳ chọn. Một ô chọn khoảng ngày. Để trống thì lấy tháng hiện "
     "tại; chọn ngược (từ > đến) thì hệ thống tự đảo lại."),
    ("Thị trường", "Dropdown", "Enable / Ẩn", "Danh sách tỉnh/TP", "Không", "Trống",
     "Chỉ hiện ở tiêu chí Thị trường và Phòng kinh doanh."),
    ("Khách hàng", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Trống",
     "Chỉ hiện ở tiêu chí Khách hàng."),
    ("Loại meeting", "Dropdown", "Enable", "Danh mục loại meeting", "Không", "Trống",
     "Không áp cho chỉ tiêu KH mới."),
    ("Trạng thái", "Dropdown", "Enable", "Lên lịch / Chốt lịch / Hoàn thành / Hủy", "Không",
     "Trống", "Không áp cho chỉ tiêu KH mới."),
    ("Công ty", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Ẩn khi thiếu quyền",
     "Chỉ hiện với quyền V1."),
    ("Phòng ban", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Ẩn khi thiếu quyền",
     "Hiện với V1, V2, V3. Lọc theo phòng ban trong hồ sơ người chủ trì meeting "
     "(với KH mới: hồ sơ người tạo khách hàng)."),
    ("Bộ phận", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Ẩn khi thiếu quyền",
     "Hiện với V1, V2, V3; danh sách theo phòng ban đã chọn."),
    ("Nhân viên", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Ẩn khi thiếu quyền",
     "Hiện với V1, V2, V3. Lọc theo người chủ trì meeting / người tạo khách hàng."),
    ("Nút Xóa lọc", "Button", "Enable", "–", "–", "Hiển thị", "Đưa bộ lọc và Cấp xem về mặc định."),
])

d.p("2.2.4 Danh sách event và xử lý event")
d.event_table([
    ("Bấm Tìm kiếm nâng cao", "Click", "After:\n– Mở / thu gọn panel bộ lọc."),
    ("Chọn giá trị ở một ô lọc", "Change",
     "During:\n– Kỳ chuyển khỏi Tuỳ chọn → xoá khoảng ngày đã chọn.\n"
     "– Đổi tiêu chí → xoá giá trị ô Thị trường / Khách hàng bị ẩn, Cấp xem về mặc định.\n"
     "After:\n– Tải lại báo cáo theo bộ lọc mới, bảng về trang 1.\n"
     "– Lỗi khi tải → hiển thị “Lỗi khi tải dữ liệu”."),
    ("Bấm Xóa lọc", "Click",
     "After:\n– Đưa mọi ô về mặc định (Tháng này, Thị trường, các ô khác trống), Cấp xem về mặc "
     "định và tải lại báo cáo."),
])

# --------------------------------------------------------------- 2.3 FR-03
d.h3("2.3 Cài đặt bộ lọc")
d.p("2.3.1 Giới thiệu")
d.rule_ref("- Kịch bản tìm kiếm, Bộ lọc. Màn này dùng nguyên chức năng Cài đặt bộ lọc dùng "
           "chung của hệ thống, không có quy tắc riêng.", anchor="search")
d.intro_table(
    ten="Cài đặt bộ lọc",
    mota="Cho người dùng chọn ô lọc nào hiển thị trên panel bộ lọc của báo cáo. Cấu hình lưu "
         "riêng cho từng người dùng.",
    tacnhan=TAC_NHAN,
    dieukien="Người dùng đang ở màn báo cáo.",
    chinh="1. Người dùng bấm “Cài đặt bộ lọc”.\n"
          "2. Hệ thống mở cửa sổ Cài đặt bộ lọc.\n"
          "3. Người dùng chọn các ô lọc muốn hiển thị và lưu.\n"
          "4. Panel bộ lọc hiển thị theo cấu hình mới.",
    phu="• Đóng cửa sổ mà không lưu → giữ nguyên cấu hình cũ.\n"
        "• Ô lọc bị ẩn theo quyền (Công ty, Phòng ban, Bộ phận, Nhân viên) vẫn ẩn dù đã chọn hiển thị.")

d.p("2.3.2 Layout màn hình")
d.layout(menu=MENU + " => Cài đặt bộ lọc", modal="Cài đặt bộ lọc",
         shot=shot("03-cai-dat-bo-loc.png"), shot_caption="Cửa sổ Cài đặt bộ lọc")

d.p("2.3.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Tiêu đề “Cài đặt bộ lọc”", "Label", "Hiển thị", "–", "–", "Hiển thị", "Kèm nút đóng ×."),
    ("Danh sách ô lọc", "Table/Grid", "Enable", "Danh sách ô lọc của màn", "Không",
     "Theo cấu hình đã lưu", "Chọn / bỏ chọn ô lọc hiển thị trên panel."),
    ("Nút Lưu", "Button", "Enable", "–", "–", "Hiển thị", "Lưu cấu hình cho người dùng hiện tại."),
    ("Nút Đóng", "Button", "Enable", "–", "–", "Hiển thị", "Đóng cửa sổ, không lưu."),
])

d.p("2.3.4 Danh sách event và xử lý event")
d.event_table([
    ("Bấm Cài đặt bộ lọc", "Click", "After:\n– Mở cửa sổ với cấu hình đã lưu của người dùng."),
    ("Bấm Lưu", "Click",
     "After:\n– Lưu cấu hình, đóng cửa sổ, panel bộ lọc hiển thị theo cấu hình mới."),
])

# --------------------------------------------------------------- 2.4 FR-04
d.h3("2.4 Chọn cấp xem và bung / thu gọn dòng")
d.p("2.4.1 Giới thiệu")
d.rule_ref("- Màn Danh sách. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi tiết."
           % TEN_MAN, anchor="list")
d.intro_table(
    ten="Chọn cấp xem",
    mota="Bung sẵn cây theo dõi tới một cấp xác định, thay vì bấm mũi tên từng dòng.",
    tacnhan=TAC_NHAN,
    dieukien="Bảng theo dõi đã có dữ liệu.",
    chinh="1. Người dùng chọn một giá trị ở ô Cấp xem phía trên bảng.\n"
          "2. Hệ thống bung mọi dòng tới đúng cấp đã chọn.\n"
          "3. Bảng hiển thị lại, phân trang giữ nguyên.",
    phu="• Chọn “Đến Bộ phận” → chỉ phòng ban có chia bộ phận mới bung thêm cấp Bộ phận; phòng "
        "không chia bộ phận dừng ở cấp Phòng ban, không hiện nhân viên.\n"
        "• Sau đó bấm mũi tên từng dòng → chỉ dòng đó đổi, ô Cấp xem giữ nguyên lựa chọn.\n"
        "• Đổi bộ lọc / tiêu chí → cây mới bung theo Cấp xem đang chọn (đổi tiêu chí thì về "
        "“Chỉ <cấp gốc>”).")

d.p("2.4.2 Layout màn hình")
d.layout(menu=MENU + " => Cấp xem", shot=shot("04-cap-xem-tat-ca.png"),
         shot_caption="Bảng theo dõi ở cấp xem “Tất cả cấp (đến Nhân viên)”")

d.p("2.4.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Ô Cấp xem", "Dropdown", "Enable", "Danh sách 4 giá trị", "Không", "Chỉ <cấp gốc>",
     "Nhãn theo tiêu chí. Tiêu chí Thị trường: Chỉ Thị trường, Đến Phòng ban, Đến Bộ phận, "
     "Tất cả cấp (đến Nhân viên). Tiêu chí Phòng kinh doanh: Chỉ Phòng ban, Đến Bộ phận, "
     "Đến Nhân viên, Tất cả cấp (đến Thị trường). Không xoá trống được."),
    ("Mũi tên đầu dòng", "Icon Button", "Enable / Ẩn", "–", "–", "Theo dữ liệu",
     "Chỉ hiện ở dòng có cấp con. Hướng mũi tên cho biết dòng đang bung hay thu gọn."),
    ("Phân tầng màu dòng cha", "Table/Grid", "Read-only", "–", "–", "Hiển thị",
     "Dòng cha mỗi cấp một nền đậm → nhạt dần, có vạch cấp bên trái ô tên; dòng cấp 1 có đường "
     "kẻ đậm phía trên để tách khối."),
])

d.p("2.4.4 Danh sách event và xử lý event")
d.event_table([
    ("Chọn giá trị ô Cấp xem", "Change",
     "After:\n– Bung mọi dòng có cấp con nằm trong phạm vi cấp đã chọn (xét theo TÊN cấp, không "
     "theo độ sâu), thu gọn các dòng còn lại."),
    ("Bấm mũi tên đầu dòng", "Click", "After:\n– Bung / thu gọn riêng dòng đó."),
])

# --------------------------------------------------------------- 2.5 FR-05
d.h3("2.5 In báo cáo")
d.p("2.5.1 Biểu đồ Usecase")
d.uc_figure("FR-05", "In báo cáo", "io",
            [("include", "Chọn kiểu in"),
             ("include", "Xem trước bản in"),
             ("extend", "Gửi lệnh in tới máy in")],
            actor=ACTOR_QL, caption="Biểu đồ Use Case — FR-05 In báo cáo")

d.p("2.5.2 Giới thiệu")
d.rule_ref("- Quy tắc Excel và In ấn. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi "
           "tiết." % TEN_MAN, anchor="excel")
d.intro_table(
    ten="In báo cáo",
    mota="In bảng theo dõi hoặc danh sách chi tiết meeting của kỳ, theo đúng bộ lọc đang áp dụng.",
    tacnhan=TAC_NHAN,
    dieukien="Người dùng đang ở màn báo cáo.",
    chinh="1. Người dùng bấm “In báo cáo”.\n"
          "2. Hệ thống mở popup In báo cáo với 2 kiểu in.\n"
          "3. Người dùng chọn kiểu in và bấm “In”.\n"
          "4. Hệ thống dựng bản in A4 ngang và mở popup xem trước.\n"
          "5. Người dùng bấm in trên popup xem trước.",
    phu="• Bấm “Hủy” hoặc × → đóng popup, không in.\n"
        "• Lỗi khi dựng bản in → popup xem trước hiển thị thông báo lỗi.",
    dacbiet="Bản in luôn có đủ mọi cấp của cây, không phụ thuộc Cấp xem và trang đang xem trên "
            "màn hình. Dưới tiêu đề in 1 dòng mô tả bộ lọc; ô lọc để trống ghi “Tất cả”. "
            "Cột Giá trị dự kiến trên bản in ghi số đồng đầy đủ (vd 108,009,464,724), không quy "
            "ra tỷ như trên màn hình.")

d.p("2.5.3 Layout màn hình")
d.layout(menu=MENU + " => In báo cáo", modal="In báo cáo",
         shot=shot("09-in-bao-cao.png"), shot_caption="Popup chọn kiểu in")
d.figure(shot("10-xem-truoc-ban-in.png"), "Popup xem trước bản in bảng theo dõi", width_in=6.2)

d.p("2.5.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Tiêu đề “In báo cáo”", "Label", "Hiển thị", "–", "–", "Hiển thị", "Kèm nút đóng ×."),
    ("Ghi chú", "Label", "Hiển thị", "–", "–", "Hiển thị",
     "“Bản in A4 ngang, bám đúng bộ lọc đang áp dụng.”"),
    ("Kiểu in “In bảng theo dõi”", "Radio", "Enable", "–", "Có", "Được chọn",
     "“Đúng bảng đang xem, đủ mọi cấp, kèm dòng TỔNG. 9 cột như trên màn.”"),
    ("Kiểu in “In danh sách chi tiết meeting”", "Radio", "Enable", "–", "Có", "Không chọn",
     "“Từng meeting một dòng, kèm thị trường / phòng ban / bộ phận / người chủ trì / khách hàng.”"),
    ("Nút Hủy", "Button", "Enable", "–", "–", "Hiển thị", "Đóng popup."),
    ("Nút In", "Button", "Enable", "–", "–", "Hiển thị", "Mở popup xem trước bản in."),
    ("Popup xem trước", "Modal", "Hiển thị", "–", "–", "Ẩn",
     "Tiêu đề “Xem trước báo cáo phát triển thị trường - khách hàng” hoặc “Xem trước danh sách "
     "chi tiết meeting”. Có tiêu đề công ty (letterhead) và giờ in."),
])

d.p("2.5.5 Danh sách event và xử lý event")
d.event_table([
    ("Bấm In báo cáo", "Click", "After:\n– Mở popup In báo cáo."),
    ("Bấm In", "Click",
     "During:\n– Lấy đúng bộ lọc đang áp dụng trên màn hình và kiểu in đã chọn.\n"
     "After:\n– Đóng popup chọn kiểu, mở popup xem trước bản in.\n"
     "– Lỗi → hiển thị thông báo lỗi trong popup xem trước."),
])

# --------------------------------------------------------------- 2.6 FR-06
d.h3("2.6 Xuất Excel báo cáo")
d.p("2.6.1 Biểu đồ Usecase")
d.uc_figure("FR-06", "Xuất Excel báo cáo", "io",
            [("include", "Lấy bộ lọc đang áp dụng"),
             ("include", "Tải file về máy")],
            actor=ACTOR_QL, caption="Biểu đồ Use Case — FR-06 Xuất Excel báo cáo")

d.p("2.6.2 Giới thiệu")
d.rule_ref("- Quy tắc Excel. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi tiết."
           % TEN_MAN, anchor="excel")
d.intro_table(
    ten="Xuất Excel báo cáo",
    mota="Tải file Excel bảng theo dõi theo bộ lọc đang áp dụng.",
    tacnhan=TAC_NHAN,
    dieukien="Người dùng đang ở màn báo cáo.",
    chinh="1. Người dùng bấm “Xuất Excel”.\n"
          "2. Hệ thống dựng file theo bộ lọc đang áp dụng.\n"
          "3. Trình duyệt tải file “bao-cao-phat-trien-thi-truong-khach-hang.xlsx”.",
    phu="• Lỗi khi xuất → hiển thị thông báo “Lỗi khi xuất Excel”.",
    dacbiet="File có dòng TỔNG và đủ mọi cấp của cây, STT nối chuỗi và tên thụt lề theo cấp, "
            "không phụ thuộc Cấp xem và trang đang xem.")

d.p("2.6.3 Layout màn hình")
d.layout(menu=MENU + " => Xuất Excel", shot=shot("01-man-chinh.png"),
         shot_caption="Nút Xuất Excel ở góc phải thanh bộ lọc")

d.p("2.6.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Nút Xuất Excel", "Button", "Enable", "–", "–", "Hiển thị", "Tải file .xlsx về máy."),
    ("Thông báo lỗi", "Toast / Alert", "Hiển thị", "–", "–", "Ẩn", "“Lỗi khi xuất Excel”."),
])

d.p("2.6.5 Danh sách event và xử lý event")
d.event_table([
    ("Bấm Xuất Excel", "Click",
     "During:\n– Lấy đúng bộ lọc đang áp dụng (bỏ các ô trống).\n"
     "After:\n– Tải file “bao-cao-phat-trien-thi-truong-khach-hang.xlsx” gồm 9 cột như trên màn.\n"
     "– Lỗi → hiển thị “Lỗi khi xuất Excel”."),
])

# --------------------------------------------------------------- 2.7 FR-07
d.h3("2.7 Xem danh sách chi tiết")
d.p("2.7.1 Giới thiệu")
d.rule_ref("- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang. Chỉ bổ sung các quy tắc riêng "
           "của %s tại phần mô tả chi tiết." % TEN_MAN, anchor="list")
d.intro_table(
    ten="Xem danh sách chi tiết đứng sau một con số",
    mota="Liệt kê từng meeting (hoặc từng khách hàng mới) tạo nên con số người dùng vừa bấm, "
         "đúng dòng và đúng chỉ tiêu đó.",
    tacnhan=TAC_NHAN,
    dieukien="Người dùng bấm một con số khác 0 trên dải tổng hợp hoặc bảng theo dõi.",
    chinh="1. Người dùng bấm con số.\n"
          "2. Hệ thống mở popup, tiêu đề nêu rõ chỉ tiêu và đối tượng đang xem.\n"
          "3. Hệ thống tải danh sách theo bộ lọc của báo cáo + dòng + chỉ tiêu đã bấm.\n"
          "4. Popup hiển thị bảng, sắp mặc định theo Ngày họp tăng dần (popup KH mới: Ngày tạo KH).",
    phu="• Chỉ tiêu Huỷ → bộ cột riêng có Lý do huỷ, bỏ cột Trạng thái, Nhu cầu, Giá trị dự kiến.\n"
        "• Chỉ tiêu KH mới → danh sách khách hàng, không phải meeting.\n"
        "• Bấm từ một dòng của cây → bỏ cột của các cấp đã cố định trên đường dẫn của dòng đó.\n"
        "• Lỗi khi tải → hiển thị “Lỗi khi tải danh sách chi tiết”.")

d.p("2.7.2 Layout màn hình")
d.layout(menu=MENU + " => Bấm số Meeting KH", modal="Danh sách chi tiết",
         shot=shot("05-popup-meeting.png"),
         shot_caption="Danh sách chi tiết Kế hoạch meeting — toàn bộ báo cáo")
d.figure(shot("07-popup-huy.png"), "Danh sách chi tiết Meeting bị huỷ (bộ cột riêng)", width_in=6.2)
d.figure(shot("08-popup-kh-moi.png"),
         "Danh sách Khách hàng mới tạo trong kỳ theo Thị trường: Thành phố Hải Phòng", width_in=6.2)

d.p("2.7.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Tiêu đề popup", "Label", "Hiển thị", "–", "Theo dòng + chỉ tiêu",
     "“Bạn đang xem phát triển thị trường:” + “<chỉ tiêu> theo <Cấp>: <Tên>” (vd “Kế hoạch "
     "meeting theo Thị trường: Thành phố Hà Nội”). Bấm từ dòng TỔNG / dải tổng hợp thì ghi "
     "“— toàn bộ báo cáo”. Chỉ tiêu: Kế hoạch meeting, Meeting hoàn thành, Meeting bị huỷ, "
     "Khách hàng mới tạo trong kỳ, Nhu cầu đầu tư thu thập, Meeting lập trước kỳ, Meeting lập "
     "trong kỳ."),
    ("Dòng phụ", "Label", "Hiển thị", "–", "Theo dữ liệu",
     "Số dòng (vd “783 meeting”). Dòng nằm sâu trong cây thì thêm “Thuộc: <Cấp>: <Tên> › …”."),
    ("Bảng meeting (Meeting KH, Hoàn thành, Nhu cầu, Lập trước / trong kỳ)", "Table/Grid",
     "Read-only", "–", "Theo dữ liệu",
     "STT · Tên meeting · Ngày họp (có giờ) · Ngày tạo meeting · Loại meeting · Trạng thái · các "
     "cấp theo dõi (Khách hàng, Thị trường, Phòng ban, Bộ phận, Nhân viên chủ trì) · Nhu cầu đầu "
     "tư ghi nhận · Giá trị dự kiến (đ)."),
    ("Bảng Meeting bị huỷ", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "STT · Tên meeting · Ngày tạo meeting · Ngày họp · Lý do huỷ · Loại meeting · các cấp theo "
     "dõi. Ô Lý do huỷ 2 dòng: lý do chọn từ danh mục (đậm) và ghi chú huỷ (chữ nhỏ)."),
    ("Bảng Khách hàng mới", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "STT · Khách hàng · Thị trường · Phòng ban · Bộ phận · Người tạo KH · Ngày tạo KH."),
    ("Cột của cấp đã cố định", "Table/Grid", "Ẩn", "–", "Theo dòng đã bấm",
     "Cấp nào nằm trên đường dẫn của dòng đã bấm thì bỏ cột đó. Riêng popup cố định Khách hàng "
     "vẫn giữ cột Thị trường."),
    ("Cột Bộ phận", "Table/Grid", "Enable / Ẩn", "–", "Theo dữ liệu",
     "Bỏ khi không có dòng nào thuộc bộ phận."),
    ("Chip “KH mới”", "Badge", "Hiển thị", "–", "Theo dữ liệu",
     "Ở ô Khách hàng của meeting có khách hàng mới tạo trong kỳ; khi cột Khách hàng bị bỏ thì "
     "chip nằm ở ô Tên meeting."),
    ("Ô trống dữ liệu", "Text", "Read-only", "–", "—", "Hiển thị “—” khi không có giá trị."),
    ("Phân trang", "Pagination", "Enable", "20 / 50 / 100", "20 dòng / trang", "–"),
    ("Trạng thái rỗng", "Label", "Hiển thị", "–", "Ẩn",
     "“Không có meeting nào khớp bộ lọc.” (popup KH mới: “Không có khách hàng nào khớp bộ lọc.”)."),
    ("Nút Đóng", "Button", "Enable", "–", "Hiển thị", "Đóng popup."),
], required=False)

d.p("2.7.4 Danh sách event và xử lý event")
d.event_table([
    ("Bấm con số khác 0", "Click",
     "Before:\n– Ghi nhận dòng (hoặc dòng TỔNG) và chỉ tiêu đã bấm.\n"
     "During:\n– Lọc tập dữ liệu theo bộ lọc báo cáo, phạm vi quyền, đường dẫn của dòng và chỉ "
     "tiêu.\n"
     "After:\n– Mở popup ở trạng thái mặc định: bộ lọc popup trống, khối tổng hợp thu gọn, sắp "
     "theo Ngày họp (KH mới: Ngày tạo KH) tăng dần, trang 1.\n"
     "– Lỗi → hiển thị “Lỗi khi tải danh sách chi tiết”."),
    ("Bấm Đóng", "Click", "After:\n– Đóng popup, màn báo cáo giữ nguyên."),
])

# --------------------------------------------------------------- 2.8 FR-08
d.h3("2.8 Lọc, sắp xếp và tổng hợp trong danh sách chi tiết")
d.p("2.8.1 Giới thiệu")
d.rule_ref("- Kịch bản tìm kiếm, Bộ lọc, Dropdown. Chỉ bổ sung các quy tắc riêng của %s tại "
           "phần mô tả chi tiết." % TEN_MAN, anchor="search")
d.intro_table(
    ten="Lọc, sắp xếp và tổng hợp trong danh sách chi tiết",
    mota="Lọc sâu hơn trong tập dòng của popup, sắp xếp theo cột và xem khối tổng hợp của tập "
         "đang lọc.",
    tacnhan=TAC_NHAN,
    dieukien="Popup danh sách chi tiết đang mở.",
    chinh="1. Người dùng gõ ô tìm nhanh hoặc chọn giá trị ở một ô lọc của popup.\n"
          "2. Popup lọc ngay trên tập dòng đã tải, về trang 1, cập nhật bộ đếm “x / y”.\n"
          "3. Người dùng bấm tiêu đề cột có biểu tượng sắp xếp để đổi thứ tự.\n"
          "4. Người dùng bấm “Xem tổng hợp” để xem khối KPI và dải phân bổ của tập đang lọc.",
    phu="• Bấm một chip phân bổ → lọc nhanh theo mục đó; bấm lại chip đang chọn → bỏ lọc.\n"
        "• Bấm “Xoá lọc” → bỏ mọi ô lọc và từ khoá của popup.\n"
        "• Đóng rồi mở popup khác → bộ lọc, sắp xếp, khối tổng hợp về mặc định.")

d.p("2.8.2 Layout màn hình")
d.layout(menu=MENU + " => Bấm số Meeting KH => Xem tổng hợp", modal="Danh sách chi tiết",
         shot=shot("06-popup-tong-hop.png"),
         shot_caption="Popup danh sách chi tiết với khối tổng hợp đang mở")

d.p("2.8.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Ô tìm nhanh", "Textbox", "Enable", "0–255 ký tự", "Không", "Trống",
     "Gợi ý “Tìm trong N meeting…”. Tìm theo tên meeting, khách hàng, nhân viên, nhu cầu; không "
     "phân biệt hoa thường."),
    ("Ô lọc Thị trường", "Dropdown", "Enable / Ẩn", "Giá trị có trong popup", "Không",
     "Thị trường: tất cả", "Ẩn khi popup đã cố định Thị trường hoặc Khách hàng."),
    ("Ô lọc Khách hàng", "Dropdown", "Enable / Ẩn", "Giá trị có trong popup", "Không",
     "Khách hàng: tất cả", "Ẩn khi popup đã cố định Khách hàng."),
    ("Ô lọc Phòng ban", "Dropdown", "Enable / Ẩn", "Giá trị có trong popup", "Không",
     "Phòng ban: tất cả", "Ẩn khi popup đã cố định Phòng ban."),
    ("Ô lọc Bộ phận", "Dropdown", "Enable / Ẩn", "Giá trị có trong popup", "Không",
     "Bộ phận: tất cả", "Ẩn khi đã cố định Bộ phận hoặc không dòng nào thuộc bộ phận."),
    ("Ô lọc Nhân viên", "Dropdown", "Enable / Ẩn", "Giá trị có trong popup", "Không",
     "Nhân viên: tất cả", "Ẩn khi popup đã cố định Nhân viên."),
    ("Ô lọc Loại meeting", "Dropdown", "Enable / Ẩn", "Giá trị có trong popup", "Không",
     "Loại meeting: tất cả", "Ẩn ở popup KH mới."),
    ("Ô lọc Trạng thái", "Dropdown", "Enable / Ẩn", "Giá trị có trong popup", "Không",
     "Trạng thái: tất cả", "Ẩn ở popup KH mới."),
    ("Nút Xoá lọc", "Button", "Enable / Ẩn", "–", "–", "Ẩn",
     "Chỉ hiện khi có từ khoá hoặc ô lọc đang chọn."),
    ("Bộ đếm “x / y meeting”", "Label", "Read-only", "–", "–", "y / y",
     "x = số dòng sau lọc, y = tổng số dòng của popup."),
    ("Tiêu đề cột sắp xếp được", "Icon Button", "Enable", "Tăng / giảm", "–",
     "Ngày họp tăng dần",
     "Popup meeting: Ngày họp, Ngày tạo meeting, Phòng ban, Nhân viên chủ trì. Popup KH mới: "
     "Ngày tạo KH, Phòng ban, Người tạo KH. Bấm lần 1 tăng, lần 2 giảm."),
    ("Nút Xem tổng hợp / Thu gọn", "Button", "Enable", "–", "–", "Thu gọn",
     "Mở / thu gọn khối “Tổng hợp danh sách đang xem”."),
    ("Ô KPI Tỷ lệ hoàn thành meeting", "Text", "Read-only", "0.0% – 100.0%", "–", "Theo dữ liệu",
     "Meeting hoàn thành ÷ meeting trong danh sách đang lọc, kèm “a / b” và thanh tỷ lệ. "
     "Ẩn ở popup KH mới."),
    ("Ô KPI KH mới tạo trong kỳ", "Text", "Read-only", "≥ 0", "–", "Theo dữ liệu",
     "Số KH mới của nhánh đang xem; KHÔNG đổi theo bộ lọc của popup. Ẩn ở popup KH mới."),
    ("Ô KPI Tỷ lệ meeting huỷ", "Text", "Read-only", "0.0% – 100.0%", "–", "Theo dữ liệu",
     "Meeting huỷ ÷ meeting trong danh sách đang lọc. Ẩn ở popup KH mới."),
    ("Dải chip “Phân bổ … theo cơ cấu”", "Button", "Enable", "Tối đa 12 chip / nhóm", "–",
     "Theo dữ liệu",
     "2 nhóm Thị trường, Phòng ban; mỗi chip ghi tên, số dòng, tỷ lệ %. Nhóm bị ẩn theo cùng luật "
     "ẩn của ô lọc."),
])

d.p("2.8.4 Danh sách event và xử lý event")
d.event_table([
    ("Gõ ô tìm nhanh / chọn ô lọc", "Keypress / Change",
     "After:\n– Lọc trên tập dòng của popup, về trang 1, cập nhật bộ đếm, KPI và dải chip."),
    ("Bấm chip phân bổ", "Click",
     "After:\n– Đặt ô lọc tương ứng theo chip; bấm lại chip đang chọn thì bỏ lọc. Về trang 1."),
    ("Bấm tiêu đề cột sắp xếp", "Click",
     "After:\n– Cột mới: sắp tăng dần; cột đang sắp: đảo chiều. Dòng hoà nhau giữ thứ tự ổn định "
     "theo mã."),
    ("Bấm Xoá lọc", "Click", "After:\n– Bỏ từ khoá và mọi ô lọc của popup, về trang 1."),
    ("Bấm Xem tổng hợp / Thu gọn", "Click", "After:\n– Mở / thu gọn khối tổng hợp."),
])

# --------------------------------------------------------------- 2.9 FR-09
d.h3("2.9 In danh sách chi tiết")
d.p("2.9.1 Biểu đồ Usecase")
d.uc_figure("FR-09", "In danh sách chi tiết", "io",
            [("include", "Lấy bộ lọc báo cáo + bộ lọc popup"),
             ("include", "Xem trước bản in")],
            actor=ACTOR_QL, caption="Biểu đồ Use Case — FR-09 In danh sách chi tiết")

d.p("2.9.2 Giới thiệu")
d.rule_ref("- Quy tắc Excel và In ấn. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi "
           "tiết." % TEN_MAN, anchor="excel")
d.intro_table(
    ten="In danh sách chi tiết",
    mota="In đúng tập dòng đang lọc trong popup danh sách chi tiết.",
    tacnhan=TAC_NHAN,
    dieukien="Popup danh sách chi tiết đang mở.",
    chinh="1. Người dùng bấm “In danh sách” ở chân popup.\n"
          "2. Hệ thống dựng bản in theo bộ lọc báo cáo + dòng + chỉ tiêu + bộ lọc của popup.\n"
          "3. Hệ thống mở popup xem trước “Xem trước danh sách chi tiết meeting” (popup KH mới: "
          "“Xem trước danh sách khách hàng mới”).",
    phu="• Lỗi khi dựng bản in → popup xem trước hiển thị thông báo lỗi.",
    dacbiet="Bản in gồm đủ mọi dòng của tập đang lọc (không chỉ trang đang xem). Tiêu đề bản in: "
            "“DANH SÁCH CHI TIẾT MEETING” hoặc “DANH SÁCH KHÁCH HÀNG MỚI”.")

d.p("2.9.3 Layout màn hình")
d.layout(menu=MENU + " => Bấm số Meeting KH => In danh sách", modal="Danh sách chi tiết",
         shot=shot("05-popup-meeting.png"),
         shot_caption="Nút In danh sách ở chân popup danh sách chi tiết")

d.p("2.9.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Nút In danh sách", "Button", "Enable", "–", "–", "Hiển thị", "Mở popup xem trước bản in."),
    ("Popup xem trước", "Modal", "Hiển thị", "–", "–", "Ẩn",
     "Có tiêu đề công ty (letterhead), dòng mô tả bộ lọc và giờ in."),
])

d.p("2.9.5 Danh sách event và xử lý event")
d.event_table([
    ("Bấm In danh sách", "Click",
     "During:\n– Ghép bộ lọc của báo cáo với dòng, chỉ tiêu và bộ lọc riêng của popup.\n"
     "After:\n– Mở popup xem trước bản in.\n– Lỗi → hiển thị thông báo lỗi trong popup xem trước."),
])

# --------------------------------------------------------------- 2.10 FR-10
d.h3("2.10 Xuất Excel danh sách chi tiết")
d.p("2.10.1 Biểu đồ Usecase")
d.uc_figure("FR-10", "Xuất Excel danh sách chi tiết", "io",
            [("include", "Lấy tập dòng đang lọc + thứ tự đang sắp"),
             ("include", "Tải file về máy")],
            actor=ACTOR_QL, caption="Biểu đồ Use Case — FR-10 Xuất Excel danh sách chi tiết")

d.p("2.10.2 Giới thiệu")
d.rule_ref("- Quy tắc Excel. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi tiết."
           % TEN_MAN, anchor="excel")
d.intro_table(
    ten="Xuất Excel danh sách chi tiết",
    mota="Tải file Excel đúng tập dòng đang lọc trong popup, theo thứ tự đang sắp.",
    tacnhan=TAC_NHAN,
    dieukien="Popup danh sách chi tiết đang mở.",
    chinh="1. Người dùng bấm “Xuất Excel danh sách”.\n"
          "2. Hệ thống dựng file từ tập dòng đang lọc, đúng bộ cột đang hiển thị.\n"
          "3. Trình duyệt tải file “Chi-tiet-meeting.xls” (popup KH mới: "
          "“Danh-sach-khach-hang-moi.xls”).",
    phu="• Tập đang lọc rỗng → file chỉ có dòng tiêu đề cột.",
    dacbiet="File gồm đủ mọi dòng của tập đang lọc, không chỉ trang đang xem.")

d.p("2.10.3 Layout màn hình")
d.layout(menu=MENU + " => Bấm số Meeting KH => Xuất Excel danh sách", modal="Danh sách chi tiết",
         shot=shot("05-popup-meeting.png"),
         shot_caption="Nút Xuất Excel danh sách ở chân popup danh sách chi tiết")

d.p("2.10.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Nút Xuất Excel danh sách", "Button", "Enable", "–", "–", "Hiển thị",
     "Màu xanh lá, tải file .xls về máy."),
])

d.p("2.10.5 Danh sách event và xử lý event")
d.event_table([
    ("Bấm Xuất Excel danh sách", "Click",
     "During:\n– Lấy tập dòng sau lọc, theo thứ tự đang sắp, đúng bộ cột đang hiển thị.\n"
     "After:\n– Tải file về máy."),
])

# ==================================================== PHẦN 4. QUY TẮC NGHIỆP VỤ
d.h1("Phần 4. Quy tắc nghiệp vụ")
d.rule_ref(". Phần này chỉ ghi các quy tắc đặc thù của %s; không lặp lại các quy tắc đã có "
           "trong SRS quy tắc chung." % TEN_MAN,
           anchor="list", head="Quy tắc áp dụng",
           lead="Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ")

d.rule_table([
    ("BR-01", "Tập meeting của báo cáo", [
        "– Chỉ lấy meeting CÓ gắn khách hàng, có NGÀY HỌP nằm trong kỳ báo cáo.",
        "– Lấy cả 4 trạng thái: Lên lịch, Chốt lịch, Hoàn thành, Hủy.",
    ], "Toàn màn hình"),
    ("BR-02", "Cách đếm các chỉ tiêu meeting", [
        "– Meeting KH: mọi meeting của tập (BR-01).",
        "– Hoàn thành: meeting trạng thái Hoàn thành. Huỷ: meeting trạng thái Hủy.",
        "– Tỷ lệ HT = Hoàn thành ÷ Meeting KH của chính dòng đó, làm tròn 1 chữ số thập phân; "
        "Meeting KH = 0 thì là 0.0%.",
        "– Nhu cầu: số meeting có ít nhất 1 nhu cầu đầu tư ghi nhận; Giá trị dự kiến: tổng giá "
        "trị đầu tư dự kiến của các nhu cầu đó.",
    ], ["Bảng theo dõi", "Dải tổng hợp"]),
    ("BR-03", "Khách hàng mới", [
        "– Là khách hàng có NGÀY TẠO trong kỳ, tính cho NGƯỜI TẠO khách hàng; thị trường lấy theo "
        "tỉnh/thành phố của khách hàng.",
        "– Không cần có meeting trong kỳ vẫn được đếm, nên có thể xuất hiện dòng có Meeting KH = 0 "
        "nhưng KH mới > 0.",
        "– Bộ lọc Loại meeting và Trạng thái KHÔNG áp cho chỉ tiêu này.",
        "– Người tạo không khớp được với nhân viên → gom vào “Không xác định người tạo” / "
        "“Chưa xác định phòng ban”.",
    ], ["Cột KH mới", "Popup KH mới"]),
    ("BR-04", "Dòng cha bằng tổng dòng con", [
        "– Mọi chỉ tiêu trên bảng tính theo TỪNG meeting (không đếm trùng khách hàng) và mỗi khách "
        "hàng mới chỉ rơi vào đúng 1 nhánh, nên số của dòng cha luôn bằng tổng các dòng con.",
        "– Riêng “số khách hàng đã tiếp cận” đếm không trùng nên KHÔNG cộng được theo cấp, chỉ "
        "hiển thị ở dải tổng hợp.",
    ], "Bảng theo dõi"),
    ("BR-05", "Cấu trúc cây theo tiêu chí", [
        "– Thị trường: Thị trường ▸ Phòng ban ▸ Bộ phận ▸ Nhân viên.",
        "– Khách hàng: Khách hàng ▸ Phòng ban ▸ Bộ phận ▸ Nhân viên.",
        "– Phòng kinh doanh: Phòng ban ▸ Bộ phận ▸ Nhân viên ▸ Thị trường.",
        "– Cấp Bộ phận chỉ xuất hiện ở phòng ban có chia bộ phận; phòng không chia thì cây đi thẳng "
        "Phòng ban ▸ Nhân viên.",
        "– Trong mỗi cấp, dòng nhiều meeting đứng trước; bằng nhau thì xếp theo tên.",
    ], ["Bảng theo dõi", "Bản in", "Excel"]),
    ("BR-06", "Phòng ban / bộ phận theo người chủ trì", [
        "– Phòng ban, Bộ phận, Nhân viên của một meeting lấy theo hồ sơ của NGƯỜI CHỦ TRÌ, không "
        "theo người tạo meeting. Các ô lọc Phòng ban / Bộ phận / Nhân viên cũng lọc theo đó.",
        "– Với khách hàng mới: lấy theo hồ sơ của người tạo khách hàng.",
    ], ["Bảng theo dõi", "Bộ lọc", "Popup chi tiết"]),
    ("BR-07", "Thị trường của meeting", [
        "– Thị trường là tỉnh/thành phố của khách hàng, được ghi lại trên meeting tại thời điểm "
        "lưu meeting.",
        "– Khách hàng chưa có tỉnh/thành phố (thường là khách hàng nước ngoài) được gom vào nhóm "
        "“Chưa xác định thị trường” — là nhóm cần bổ sung tỉnh/thành phố cho khách hàng.",
    ], ["Bảng theo dõi", "Bộ lọc Thị trường"]),
    ("BR-08", "Lập trước kỳ / Lập trong kỳ", [
        "– Chia meeting của kỳ theo NGÀY TẠO meeting: tạo trước ngày đầu kỳ là Lập trước kỳ, còn "
        "lại là Lập trong kỳ. Hai số luôn cộng lại bằng Tổng meeting.",
    ], "Dải tổng hợp"),
    ("BR-09", "Kỳ báo cáo", [
        "– Tuần tính từ thứ Hai. Tuần tiếp theo / Tháng tiếp theo là kỳ tương lai: Hoàn thành, "
        "Huỷ, Nhu cầu thường bằng 0 vì chưa tới ngày họp — đúng bản chất, không phải lỗi.",
        "– Tuỳ chọn: để trống ngày thì lấy tháng hiện tại; chọn ngày bắt đầu sau ngày kết thúc thì "
        "hệ thống tự đảo lại.",
    ], "Bộ lọc Kỳ báo cáo"),
    ("BR-10", "Phạm vi dữ liệu theo quyền", [
        "– Xét theo thứ tự V1 → V2 → V3 → không có quyền (xem Phần 2).",
        "– Ở mọi cấp, meeting do chính người dùng chủ trì và khách hàng do chính người dùng tạo "
        "luôn nằm trong phạm vi.",
        "– Bản in, Excel và popup chi tiết dùng đúng phạm vi của màn hình.",
    ], "Toàn màn hình"),
    ("BR-11", "Bản in và Excel xuất đủ dữ liệu", [
        "– In báo cáo và Xuất Excel báo cáo luôn có đủ mọi cấp và mọi trang, không phụ thuộc Cấp "
        "xem và trang đang xem.",
        "– In / Xuất Excel danh sách chi tiết gồm đủ mọi dòng của tập đang lọc trong popup, đúng "
        "thứ tự đang sắp.",
    ], ["FR-05", "FR-06", "FR-09", "FR-10"]),
    ("BR-12", "Bỏ cột và ô lọc của cấp đã cố định", [
        "– Popup mở từ một dòng của cây: mọi cấp nằm trên đường dẫn của dòng đó bị bỏ cột và bỏ "
        "ô lọc (cột chỉ lặp lại điều tiêu đề đã nói).",
        "– Cố định Khách hàng thì ẩn thêm ô lọc Thị trường (1 khách hàng chỉ thuộc 1 thị trường), "
        "nhưng CỘT Thị trường vẫn giữ.",
        "– Popup mở từ dòng TỔNG hoặc dải tổng hợp không bỏ cột nào.",
    ], "Popup chi tiết"),
])

d.save()
