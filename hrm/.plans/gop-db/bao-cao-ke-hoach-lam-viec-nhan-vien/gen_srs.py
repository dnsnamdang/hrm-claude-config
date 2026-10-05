# -*- coding: utf-8 -*-
"""Sinh "SRS - Báo cáo kế hoạch & kết quả làm việc theo nhân viên.docx" theo FORM CHUẨN 2026-08-28.

Chạy:  python3 .plans/gop-db/bao-cao-ke-hoach-lam-viec-nhan-vien/gen_srs.py
Thư viện dùng chung: .claude/skills/srs-documenter/assets/{srs_docx_lib,srs_uml_render}.py
Ảnh chụp thật (Playwright 1440x900, kỳ Năm nay, công ty id=1): klv_shots/ — chỉ để local.

Nguồn đối chiếu (nhánh gop_db, 03/10/2026):
- FE  hrm-client/pages/assign/report/employee-work-performance/ (index + 6 component)
- BE  hrm-api/Modules/Assign/Services/Report/EmployeeWorkPerformanceService.php
      + EmployeeWorkPerformance/{WorkAssignmentCollector,EmployeeWorkTreeBuilder,WorkMetrics,
        WorkStatusLabel}.php + EmployeeWorkPerformancePrintService.php + controller
- Quyền: Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (id 1612-1614)
- Menu: components/subsystem-menu/presale.js + components/menu-sidebar.js (2 lối vào)
- Thiết kế: design.md (mockup) + design-phase4.md (code thật, ưu tiên khi 2 file lệch nhau)
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "..", "..", ".claude", "skills", "srs-documenter", "assets")
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

# `part.relate_to()` của python-docx GỘP các liên kết trùng URL vào 1 quan hệ -> nhiều đoạn
# "Quy tắc chung" trỏ cùng 1 mục chỉ đẻ ra 1 quan hệ, bộ tự kiểm (đếm quan hệ) báo nhầm là thiếu
# liên kết. Mỗi đoạn tạo 1 quan hệ riêng — liên kết vẫn y nguyên, KHÔNG sửa file dùng chung.
_add_hyperlink = srs_docx_lib.add_hyperlink


def _add_hyperlink_rieng(paragraph, url, text):
    link = _add_hyperlink(paragraph, url, text)
    r_id = paragraph.part.rels._next_rId
    paragraph.part.rels.add_relationship(srs_docx_lib.RT.HYPERLINK, url, r_id, is_external=True)
    link.set(srs_docx_lib.qn('r:id'), r_id)
    return link


srs_docx_lib.add_hyperlink = _add_hyperlink_rieng

TEN_MAN = "Báo cáo kế hoạch & kết quả làm việc theo nhân viên"
OUT = os.path.join(HERE, "SRS - %s.docx" % TEN_MAN)
SHOTS = os.path.join(HERE, "klv_shots")
MENU = ("Phân hệ CSKH trước bán => Báo cáo => Báo cáo dự án tiền khả thi => "
        "Báo cáo kế hoạch & kết quả làm việc theo nhân viên")
MENU_2 = "Phân hệ Công việc => Báo cáo => Báo cáo kế hoạch & kết quả làm việc theo nhân viên"

ACTOR_TP = "Trưởng phòng / Trưởng bộ phận"
ACTOR_BGD = "Ban giám đốc"
TAC_NHAN = ("Trưởng bộ phận; Trưởng phòng; Ban giám đốc — người dùng có ít nhất 1 trong 3 quyền "
            "xem báo cáo")
TYPES = "Meeting, Task, Issue, Phiếu công tác, Phiếu giao việc"


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(out=OUT, menu=MENU,
           route="/assign/report/employee-work-performance",
           full_url="https://hrm.eteksofts.com/assign/report/employee-work-performance",
           img_prefix="klv_")

# =================================================================== TRANG ĐẦU
d.title_block(TEN_MAN)
d.h2("Mục lục")
d.toc()

# ========================================================= PHẦN 1. GIỚI THIỆU
d.h1("Phần 1. Giới thiệu")

d.h2("1 Mục đích")
d.p("Tài liệu này đặc tả yêu cầu phần mềm cho màn hình %s — theo dõi khối lượng và kết quả làm "
    "việc của từng nhân viên, biết được ai đang nhiều việc, có khả năng thực hiện công việc hay "
    "không. Tài liệu nhằm:" % TEN_MAN)
d.bullets([
    "Là căn cứ nghiệm thu chức năng và phân quyền của báo cáo.",
    "Làm rõ cách gom 5 loại đầu việc (%s) về cùng một bảng." % TYPES,
    "Làm rõ cơ chế đếm khác nhau giữa dòng Nhân viên (mỗi người tham gia +1) và dòng cha (đếm theo "
    "phiếu) — để người đọc không tưởng báo cáo cộng sai.",
    "Làm rõ cách xếp mỗi đầu việc vào 1 trong 4 nhóm trạng thái và phạm vi dữ liệu theo quyền.",
])

d.h2("2 Thuật ngữ và viết tắt")
d.table(["Thuật ngữ", "Mô tả"], [
    ("Đầu việc", "Một chứng từ thuộc 1 trong 5 loại: %s." % TYPES),
    ("Phiếu", "Cách gọi chung một đầu việc khi đếm theo chứng từ (1 phiếu nhiều người tham gia "
              "vẫn là 1)."),
    ("Lượt tham gia", "Mỗi cặp (đầu việc × người tham gia) là 1 lượt."),
    ("Người tham gia", "Meeting: người chủ trì + nhân viên dự họp phía công ty. Task, Issue: người "
                       "được giao. Phiếu công tác: mọi người trong đoàn. Phiếu giao việc: nhân viên "
                       "thực hiện."),
    ("Chủ trì", "Meeting: người chủ trì. Task, Issue: người được giao. Phiếu công tác: trưởng đoàn. "
                "Phiếu giao việc: người lập phiếu."),
    ("Kỳ báo cáo", "Đầu việc được tính khi KHOẢNG THỜI GIAN của nó (bắt đầu → kết thúc / hạn) "
                   "giao nhau với kỳ."),
    ("4 nhóm trạng thái", "Đã hoàn thành; Đang thực hiện; Quá hạn; Dừng / Huỷ / Từ chối."),
    ("Trạng thái chứng từ", "Trạng thái gốc của chứng từ (vd Hoàn thành, Đã duyệt kết quả), khác "
                            "với 4 nhóm trạng thái theo dõi."),
], widths=[1.8, 4.2])

# ========================================================= PHẦN 2. PHÂN QUYỀN
d.h1("Phần 2. Phân quyền")

d.h2("1 Danh sách quyền")
d.p("Nhóm quyền thao tác: màn hình không có quyền thao tác riêng. Người dùng có ít nhất 1 quyền "
    "xem dưới đây thì dùng được mọi chức năng (lọc, xem chi tiết, in, xuất Excel).")

d.p("Nhóm quyền quyết định phạm vi dữ liệu "
    "(xét theo thứ tự ưu tiên từ trên xuống, cấp nào có trước thì áp cấp đó):")
d.table(["Ký hiệu", "Tên quyền", "Phạm vi dữ liệu"], [
    ("V1", "Xem báo cáo kế hoạch & kết quả làm việc theo công ty",
     "Mọi phòng ban của công ty đang làm việc."),
    ("V2", "Xem báo cáo kế hoạch & kết quả làm việc theo phòng ban",
     "Nhân viên thuộc các phòng ban người đăng nhập được phân công quản lý, trong công ty đang "
     "làm việc."),
    ("V3", "Xem báo cáo kế hoạch & kết quả làm việc theo bộ phận",
     "Nhân viên thuộc các bộ phận người đăng nhập được phân công quản lý, trong công ty đang "
     "làm việc."),
    ("—", "(không có cấp nào)",
     "KHÔNG được xem báo cáo: menu ẩn mục này; vào thẳng đường dẫn thì màn hiển thị “Bạn không có "
     "quyền xem báo cáo này.”. Không có mức “chỉ xem việc của mình”."),
], widths=[0.8, 2.3, 2.9])

d.h2("2 Ma trận phân quyền")
_ALL = ("✅", "✅", "✅", "❌")
d.table(["Chức năng", "V1", "V2", "V3", "Không có quyền nào"], [
    ("FR-01 Xem báo cáo",) + _ALL,
    ("FR-02 Tìm kiếm và lọc báo cáo",) + _ALL,
    ("FR-03 Cài đặt bộ lọc",) + _ALL,
    ("FR-04 Chọn cấp xem",) + _ALL,
    ("FR-05 In báo cáo",) + _ALL,
    ("FR-06 Xuất Excel",) + _ALL,
    ("FR-07 Xem danh sách đầu việc chi tiết",) + _ALL,
    ("FR-08 Lọc, sắp xếp, tổng hợp trong danh sách",) + _ALL,
    ("FR-09 Xem chi tiết đầu việc",) + _ALL,
    ("FR-10 In danh sách chi tiết",) + _ALL,
    ("FR-11 Xuất Excel danh sách chi tiết",) + _ALL,
], widths=[2.4, 0.7, 0.7, 0.7, 1.5])
d.p("Ghi chú: chỉ xem được công ty đang làm việc — quyền được cấp theo từng công ty nên quyền ở "
    "công ty A không cho xem báo cáo của công ty B. Bản in, Excel và danh sách chi tiết dùng đúng "
    "phạm vi của màn hình.")

# ================================================ PHẦN 3. ĐẶC TẢ CHI TIẾT
d.h1("Phần 3. Đặc tả chi tiết theo từng chức năng")

d.h2("1 Sơ đồ UML tổng quan")
d.overview_figure2(
    [(ACTOR_TP, [0, 1]), (ACTOR_BGD, [0, 1])],
    [("FR-01", "Xem báo cáo", "view"),
     ("FR-07", "Xem danh sách đầu việc", "view")],
    [("FR-02", "Tìm kiếm và lọc báo cáo", "view", "extend", [0], None),
     ("FR-03", "Cài đặt bộ lọc", "view", "extend", [0], None),
     ("FR-04", "Chọn cấp xem", "view", "extend", [0], None),
     ("FR-05", "In báo cáo", "io", "extend", [0], None),
     ("FR-06", "Xuất Excel", "io", "extend", [0], None),
     ("FR-08", "Lọc, sắp xếp, tổng hợp", "view", "extend", [1], None),
     ("FR-09", "Xem chi tiết đầu việc", "view", "extend", [1], None),
     ("FR-10", "In danh sách chi tiết", "io", "extend", [1], None),
     ("FR-11", "Xuất Excel danh sách", "io", "extend", [1], None)],
    "Sơ đồ Use Case tổng quan màn %s" % TEN_MAN)
d.p("Danh sách đầu việc chi tiết (FR-07) không có lối vào riêng trên menu: nó mở ra khi bấm một "
    "con số trên bảng của màn báo cáo (FR-01).")

d.h2("2 Đặc tả chi tiết từng chức năng")

# --------------------------------------------------------------- 2.1 FR-01
d.h3("2.1 Xem báo cáo")
d.p("2.1.1 Giới thiệu")
d.rule_ref("- Màn Danh sách. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi tiết."
           % TEN_MAN, anchor="list")
d.intro_table(
    ten="Xem báo cáo kế hoạch & kết quả làm việc theo nhân viên",
    mota="Dải tổng hợp + bảng theo dõi Phòng ban ▸ Bộ phận ▸ Nhân viên, mỗi dòng có số đầu việc "
         "theo 5 loại, Tổng, Đã HT, Tỷ lệ HT.",
    tacnhan=TAC_NHAN,
    dieukien="Người dùng đã đăng nhập và có ít nhất 1 trong 3 quyền V1, V2, V3.",
    chinh="1. Người dùng vào menu theo một trong 2 đường dẫn ở mục Layout.\n"
          "2. Hệ thống kiểm tra quyền và công ty đang làm việc.\n"
          "3. Hệ thống áp bộ lọc mặc định: công ty đang làm việc, Tháng này, đủ 5 loại, bật "
          "“Chỉ hiện NV có việc”.\n"
          "4. Hệ thống tính dải tổng hợp, dòng TỔNG và cây theo dõi.\n"
          "5. Bảng hiển thị ở cấp “Chỉ Phòng ban”, kèm chú thích cách đếm dưới bảng.",
    phu="• Không có quyền nào → màn chỉ hiện “Bạn không có quyền xem báo cáo này.”.\n"
        "• Không có đầu việc nào khớp bộ lọc → “Không có đầu việc nào khớp bộ lọc.”.\n"
        "• Lỗi khi tải → hiển thị “Lỗi khi tải dữ liệu”.\n"
        "• Bấm mũi tên đầu dòng → mở / thu gọn riêng dòng đó.\n"
        "• Bấm một con số khác 0 → mở danh sách đầu việc chi tiết (FR-07).")

d.p("2.1.2 Layout màn hình")
d.layout(menu=MENU,
         note="Lối vào thứ hai, cùng phạm vi dữ liệu: Menu: %s" % MENU_2,
         shot=shot("01-man-chinh.png"),
         shot_caption="Màn %s, kỳ Năm nay" % TEN_MAN)

d.p("2.1.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Tiêu đề trang", "Label", "Hiển thị", "–", TEN_MAN,
     "Kèm icon ⓘ: “Theo dõi khối lượng và kết quả làm việc của từng nhân viên, biết được ai đang "
     "nhiều việc, có khả năng thực hiện công việc hay không.”"),
    ("Nút In báo cáo", "Button", "Enable", "–", "Hiển thị", "Xem FR-05."),
    ("Nút Xuất Excel", "Button", "Enable", "–", "Hiển thị", "Màu xanh lá. Xem FR-06."),
    ("Nút Cài đặt bộ lọc / Tìm kiếm nâng cao", "Button", "Enable", "–", "Bộ lọc thu gọn",
     "Xem FR-03 / FR-02."),
    ("Dòng “Tổng hợp kỳ dd/mm/yyyy – dd/mm/yyyy”", "Label", "Read-only", "–", "Theo kỳ",
     "Số đầu việc, số nhân viên có việc và cơ cấu 5 loại, mỗi loại tô đúng màu của loại đó. "
     "Có nút Thu gọn / Mở rộng."),
    ("Khối “Khối lượng trong kỳ”", "Text", "Read-only", "–", "Theo dữ liệu",
     "Meta “Đếm theo phiếu” (hoặc “Chỉ việc chủ trì”). 2 ô: Tổng đầu việc (kèm “x/5 loại”), Nhân "
     "viên có việc (kèm “/ tổng NV”)."),
    ("Khối “Trạng thái xử lý”", "Text", "Read-only", "–", "Theo dữ liệu",
     "Meta “4 nhóm chia hết tổng”. 4 ô: Đã hoàn thành, Đang thực hiện, Quá hạn, Dừng / Huỷ / Từ "
     "chối, mỗi ô kèm tỷ lệ %."),
    ("Icon ⓘ", "Icon Button", "Hover", "–", "Hiển thị",
     "Rê chuột hiện giải thích cách đếm của khối / ô / cột."),
    ("Ô chọn Cấp xem", "Dropdown", "Enable", "Danh sách 3 giá trị", "Chỉ Phòng ban", "Xem FR-04."),
    ("Cột STT", "Table/Grid", "Read-only", "–", "Theo vị trí", "Đánh số nối chuỗi 1 → 1.1 → 1.1.1."),
    ("Cột Nội dung theo dõi", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "Tên phòng ban / bộ phận / nhân viên, thụt lề theo cấp, mũi tên ở dòng có cấp con."),
    ("5 cột loại (Meeting, Task, Issue, P. công tác, P. giao việc)", "Table/Grid", "Read-only",
     "≥ 0", "Theo dữ liệu", "Chỉ hiện các loại đang bật ở ô lọc Loại công việc. Bấm số để xem danh sách."),
    ("Cột Tổng", "Table/Grid", "Read-only", "≥ 0", "Theo dữ liệu",
     "Cộng các loại đang bật. Ở dòng cha, rê chuột hiện “N phiếu · M lượt tham gia”."),
    ("Cột Đã HT", "Table/Grid", "Read-only", "≥ 0", "Theo dữ liệu", "Bấm số để xem danh sách."),
    ("Cột Tỷ lệ HT", "Table/Grid", "Read-only", "0.0% – 100.0%", "Theo dữ liệu",
     "Đã HT ÷ Tổng của chính dòng đó. Không bấm được."),
    ("Dòng TỔNG", "Table/Grid", "Read-only", "–", "Hiển thị", "Đứng đầu bảng, tổng cả kỳ, đếm theo phiếu."),
    ("Chú thích dưới bảng", "Label", "Hiển thị", "–", "Hiển thị",
     "Giải thích dòng Nhân viên +1 mỗi người, dòng cha đếm theo phiếu nên nhỏ hơn tổng dòng con; "
     "đổi câu khi bật “Chỉ tính việc chủ trì”."),
    ("Trạng thái rỗng", "Label", "Hiển thị", "–", "Ẩn", "“Không có đầu việc nào khớp bộ lọc.”"),
    ("Thông báo không có quyền", "Label", "Hiển thị", "–", "Ẩn",
     "“Bạn không có quyền xem báo cáo này.” — thay toàn bộ nội dung màn."),
    ("Đang tải", "Loading", "Hiển thị", "–", "Ẩn", "“Đang tải dữ liệu...”"),
], required=False)

d.p("2.1.4 Danh sách event và xử lý event")
d.event_table([
    ("Mở màn hình", "System",
     "Before:\n– Kiểm tra quyền V1 / V2 / V3.\n"
     "– Không có quyền nào → hiển thị “Bạn không có quyền xem báo cáo này.” và dừng xử lý.\n"
     "– Công ty khác công ty đang làm việc → từ chối với “Bạn không có quyền xem báo cáo của công "
     "ty này.”.\n"
     "During:\n– Áp bộ lọc mặc định và phạm vi dữ liệu.\n"
     "After:\n– Hiển thị dải tổng hợp, dòng TỔNG, cây ở cấp “Chỉ Phòng ban”.\n"
     "– Lỗi khi tải → hiển thị “Lỗi khi tải dữ liệu”."),
    ("Bấm mũi tên đầu dòng", "Click", "After:\n– Mở / thu gọn riêng dòng đó; ô Cấp xem giữ nguyên."),
    ("Bấm con số khác 0", "Click",
     "After:\n– Mở danh sách đầu việc của đúng dòng + đúng cột (FR-07)."),
])

# --------------------------------------------------------------- 2.2 FR-02
d.h3("2.2 Tìm kiếm và lọc báo cáo")
d.p("2.2.1 Giới thiệu")
d.rule_ref("- Kịch bản tìm kiếm, Bộ lọc, Dropdown. Chỉ bổ sung các quy tắc riêng của %s tại "
           "phần mô tả chi tiết." % TEN_MAN, anchor="search")
d.intro_table(
    ten="Tìm kiếm và lọc báo cáo",
    mota="Thu hẹp báo cáo theo kỳ, loại công việc, trạng thái, cơ cấu tổ chức và 2 công tắc đổi "
         "cách đếm / cách hiển thị.",
    tacnhan=TAC_NHAN,
    dieukien="Người dùng đang ở màn báo cáo.",
    chinh="1. Người dùng bấm “Tìm kiếm nâng cao” để mở panel bộ lọc.\n"
          "2. Người dùng chọn giá trị ở một ô lọc hoặc bật / tắt công tắc.\n"
          "3. Hệ thống tải lại báo cáo ngay (không cần bấm nút tìm).",
    phu="• Chọn Kỳ báo cáo = Tuỳ chọn → hiện ô Thời gian.\n"
        "• Bỏ tick hết Loại công việc → ô viền đỏ, bảng và dải tổng hợp trống, hiện “Chưa bật loại "
        "công việc nào trong bộ lọc nên bảng và dải tổng hợp đang trống.”.\n"
        "• Đổi Công ty → xoá Phòng ban / Bộ phận / Nhân viên đã chọn.\n"
        "• Bấm “Xóa lọc” → về mặc định (công ty đang làm việc, Tháng này, đủ 5 loại, tắt Chỉ tính "
        "việc chủ trì, bật Chỉ hiện NV có việc) và Cấp xem về “Chỉ Phòng ban”.")

d.p("2.2.2 Layout màn hình")
d.layout(menu=MENU + " => Tìm kiếm nâng cao", shot=shot("02-bo-loc.png"),
         shot_caption="Panel bộ lọc báo cáo đang mở")

d.p("2.2.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Công ty", "Dropdown", "Enable", "Công ty người dùng có vai trò", "Có",
     "Công ty đang làm việc", "Không xoá trống được. Chọn công ty khác công ty đang làm việc thì "
     "bị từ chối (xem FR-01)."),
    ("Kỳ báo cáo", "Dropdown", "Enable", "Danh sách 8 giá trị", "Có", "Tháng này",
     "Ngày hôm nay, Tuần này, Tuần tiếp theo, Tháng này, Tháng tiếp theo, Quý này, Năm nay, "
     "Tuỳ chọn. Không có “Tất cả”."),
    ("Thời gian", "Datepicker", "Enable / Ẩn", "dd/mm/yyyy – dd/mm/yyyy", "Không", "Ẩn",
     "Chỉ hiện khi Kỳ = Tuỳ chọn."),
    ("Loại công việc", "Dropdown", "Enable", "Chọn nhiều — %s" % TYPES, "Có (≥ 1 loại)",
     "Đủ 5 loại", "Bỏ loại nào thì ẩn cột loại đó và trừ khỏi Tổng, Đã HT, dải tổng hợp."),
    ("Trạng thái", "Dropdown", "Enable", "4 nhóm trạng thái", "Không", "Trống", "–"),
    ("Phòng ban", "Dropdown", "Enable", "Danh sách theo công ty + quyền", "Không", "Trống", "–"),
    ("Bộ phận", "Dropdown", "Enable", "Danh sách theo phòng ban", "Không", "Trống", "–"),
    ("Nhân viên", "Dropdown", "Enable", "Danh sách", "Không", "Trống", "–"),
    ("Chỉ tính việc chủ trì", "Checkbox", "Enable", "Bật / Tắt", "Không", "Tắt",
     "Bật: mỗi đầu việc chỉ tính cho người chủ trì (1 đầu việc = 1 người)."),
    ("Chỉ hiện NV có việc", "Checkbox", "Enable", "Bật / Tắt", "Không", "Bật",
     "Tắt: hiện cả nhân viên có Tổng = 0."),
    ("Nút Xóa lọc", "Button", "Enable", "–", "–", "Hiển thị", "Đưa bộ lọc và Cấp xem về mặc định."),
])

d.p("2.2.4 Danh sách event và xử lý event")
d.event_table([
    ("Chọn giá trị ô lọc / bật tắt công tắc", "Change",
     "During:\n– Kỳ chuyển khỏi Tuỳ chọn → xoá khoảng ngày.\n"
     "– Đổi Công ty → xoá Phòng ban / Bộ phận / Nhân viên.\n"
     "– Loại công việc rỗng → không tính, bảng trống, ô viền đỏ.\n"
     "After:\n– Tải lại báo cáo theo bộ lọc mới.\n– Lỗi → hiển thị “Lỗi khi tải dữ liệu”."),
    ("Bấm Xóa lọc", "Click", "After:\n– Đưa bộ lọc và Cấp xem về mặc định, tải lại."),
])

# --------------------------------------------------------------- 2.3 FR-03
d.h3("2.3 Cài đặt bộ lọc")
d.p("2.3.1 Giới thiệu")
d.rule_ref("- Kịch bản tìm kiếm, Bộ lọc. Màn này dùng nguyên chức năng Cài đặt bộ lọc dùng "
           "chung của hệ thống, không có quy tắc riêng.", anchor="search")
d.intro_table(
    ten="Cài đặt bộ lọc",
    mota="Cho người dùng chọn ô lọc nào hiển thị trên panel bộ lọc. Cấu hình lưu riêng cho từng "
         "người dùng.",
    tacnhan=TAC_NHAN,
    dieukien="Người dùng đang ở màn báo cáo.",
    chinh="1. Người dùng bấm “Cài đặt bộ lọc”.\n"
          "2. Hệ thống mở cửa sổ Cài đặt bộ lọc.\n"
          "3. Người dùng chọn các ô lọc muốn hiển thị và lưu.\n"
          "4. Panel bộ lọc hiển thị theo cấu hình mới.",
    phu="• Đóng cửa sổ mà không lưu → giữ nguyên cấu hình cũ.")

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
d.h3("2.4 Chọn cấp xem")
d.p("2.4.1 Giới thiệu")
d.rule_ref("- Màn Danh sách. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi tiết."
           % TEN_MAN, anchor="list")
d.intro_table(
    ten="Chọn cấp xem",
    mota="Bung sẵn cây theo dõi tới một cấp xác định.",
    tacnhan=TAC_NHAN,
    dieukien="Bảng đang có dữ liệu.",
    chinh="1. Người dùng chọn giá trị ở ô Cấp xem.\n"
          "2. Hệ thống bung mọi dòng tới đúng cấp đã chọn.",
    phu="• “Đến Bộ phận”: chỉ phòng có chia bộ phận mới bung ra bộ phận; nhân viên chưa gán bộ "
        "phận (treo thẳng dưới phòng ban) chưa hiện tới khi chọn “Tất cả cấp”.\n"
        "• Bấm mũi tên từng dòng không làm đổi ô Cấp xem.")

d.p("2.4.2 Layout màn hình")
d.layout(menu=MENU + " => Cấp xem", shot=shot("04-cap-xem-tat-ca.png"),
         shot_caption="Bảng ở cấp xem “Tất cả cấp (đến Nhân viên)”")

d.p("2.4.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Ô Cấp xem", "Dropdown", "Enable", "Chỉ Phòng ban / Đến Bộ phận / Tất cả cấp (đến Nhân viên)",
     "Không", "Chỉ Phòng ban", "Không xoá trống được."),
    ("Mũi tên đầu dòng", "Icon Button", "Enable / Ẩn", "–", "–", "Theo dữ liệu",
     "Chỉ hiện ở dòng có cấp con."),
    ("Phân tầng màu dòng cha", "Table/Grid", "Read-only", "–", "–", "Hiển thị",
     "Mỗi cấp một nền đậm → nhạt và vạch cấp bên trái ô tên."),
])

d.p("2.4.4 Danh sách event và xử lý event")
d.event_table([
    ("Chọn giá trị ô Cấp xem", "Change",
     "After:\n– Bung các dòng có con thuộc cấp nằm trong phạm vi đã chọn (xét theo TÊN cấp của "
     "từng dòng con), thu gọn phần còn lại."),
])

# --------------------------------------------------------------- 2.5 FR-05
d.h3("2.5 In báo cáo")
d.p("2.5.1 Biểu đồ Usecase")
d.uc_figure("FR-05", "In báo cáo", "io",
            [("include", "Chọn kiểu in"), ("include", "Xem trước bản in"),
             ("extend", "Gửi lệnh in tới máy in")],
            actor=ACTOR_BGD, caption="Biểu đồ Use Case — FR-05 In báo cáo")

d.p("2.5.2 Giới thiệu")
d.rule_ref("- Quy tắc Excel và In ấn. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi "
           "tiết." % TEN_MAN, anchor="excel")
d.intro_table(
    ten="In báo cáo",
    mota="In bảng theo dõi hoặc danh sách chi tiết đầu việc theo đúng bộ lọc đang áp dụng.",
    tacnhan=TAC_NHAN,
    dieukien="Người dùng đang ở màn báo cáo.",
    chinh="1. Người dùng bấm “In báo cáo”.\n"
          "2. Hệ thống mở popup chọn 1 trong 2 kiểu in.\n"
          "3. Người dùng chọn kiểu và bấm “In”.\n"
          "4. Hệ thống mở popup xem trước bản in.",
    phu="• Bấm “Hủy” hoặc × → đóng popup.\n"
        "• Lỗi khi dựng bản in → popup xem trước hiển thị thông báo lỗi.",
    dacbiet="Bản in luôn có đủ mọi cấp, không phụ thuộc Cấp xem. Bản in danh sách chi tiết gộp 1 "
            "dòng / phiếu nên số dòng in ra khớp con số Tổng đầu việc.")

d.p("2.5.3 Layout màn hình")
d.layout(menu=MENU + " => In báo cáo", modal="In báo cáo",
         shot=shot("08-in-bao-cao.png"), shot_caption="Popup chọn kiểu in")
d.figure(shot("09-xem-truoc-ban-in.png"), "Popup xem trước bản in bảng theo dõi", width_in=6.2)

d.p("2.5.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Kiểu “In bảng theo dõi”", "Radio", "Enable", "–", "Có", "Được chọn",
     "“Đúng bảng đang xem, đủ mọi cấp (Phòng ban ▸ Bộ phận ▸ Nhân viên), kèm dòng TỔNG.”"),
    ("Kiểu “In danh sách chi tiết đầu việc”", "Radio", "Enable", "–", "Có", "Không chọn",
     "“Từng đầu việc một dòng (đã gộp theo phiếu), kèm loại · người tham gia · thời gian · "
     "trạng thái.”"),
    ("Nút Hủy / In", "Button", "Enable", "–", "–", "Hiển thị", "–"),
    ("Popup xem trước", "Modal", "Hiển thị", "–", "–", "Ẩn",
     "Tiêu đề “Xem trước báo cáo kế hoạch & kết quả làm việc theo nhân viên” hoặc “Xem trước danh "
     "sách chi tiết đầu việc”."),
])

d.p("2.5.5 Danh sách event và xử lý event")
d.event_table([
    ("Bấm In (trong popup chọn kiểu)", "Click",
     "During:\n– Lấy bộ lọc đang áp dụng và kiểu in.\n"
     "After:\n– Mở popup xem trước.\n– Lỗi → hiển thị thông báo lỗi trong popup."),
])

# --------------------------------------------------------------- 2.6 FR-06
d.h3("2.6 Xuất Excel")
d.p("2.6.1 Biểu đồ Usecase")
d.uc_figure("FR-06", "Xuất Excel", "io",
            [("include", "Lấy bộ lọc đang áp dụng"), ("include", "Tải file về máy")],
            actor=ACTOR_BGD, caption="Biểu đồ Use Case — FR-06 Xuất Excel")

d.p("2.6.2 Giới thiệu")
d.rule_ref("- Quy tắc Excel. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi tiết."
           % TEN_MAN, anchor="excel")
d.intro_table(
    ten="Xuất Excel",
    mota="Tải file Excel bảng theo dõi theo bộ lọc đang áp dụng.",
    tacnhan=TAC_NHAN,
    dieukien="Người dùng đang ở màn báo cáo.",
    chinh="1. Người dùng bấm “Xuất Excel”.\n"
          "2. Trình duyệt tải file “bao-cao-ke-hoach-lam-viec-nhan-vien.xlsx”.",
    phu="• Lỗi khi xuất → hiển thị “Lỗi khi xuất Excel”.",
    dacbiet="File có dòng TỔNG và đủ mọi cấp, không phụ thuộc Cấp xem.")

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
     "Before:\n– Kiểm tra quyền và công ty như khi xem báo cáo.\n"
     "After:\n– Tải file “bao-cao-ke-hoach-lam-viec-nhan-vien.xlsx”.\n"
     "– Lỗi → hiển thị “Lỗi khi xuất Excel”."),
])

# --------------------------------------------------------------- 2.7 FR-07
d.h3("2.7 Xem danh sách đầu việc chi tiết")
d.p("2.7.1 Giới thiệu")
d.rule_ref("- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang. Chỉ bổ sung các quy tắc riêng "
           "của %s tại phần mô tả chi tiết." % TEN_MAN, anchor="list")
d.intro_table(
    ten="Xem danh sách đầu việc chi tiết",
    mota="Liệt kê từng đầu việc tạo nên con số vừa bấm, số dòng khớp đúng con số đó ở mọi cấp.",
    tacnhan=TAC_NHAN,
    dieukien="Người dùng bấm một con số khác 0 trên bảng.",
    chinh="1. Người dùng bấm con số.\n"
          "2. Hệ thống mở popup, tiêu đề “Đang xem <chỉ tiêu> theo <Cấp>: <Tên>”.\n"
          "3. Dòng phụ ghi số đầu việc, số lượt tham gia (nếu khác), số hoàn thành, quá hạn và kỳ.\n"
          "4. Bảng hiển thị, sắp mặc định theo Bắt đầu tăng dần, 20 dòng / trang.",
    phu="• Mở từ dòng Nhân viên → 1 dòng / đầu việc, có cột Vai trò.\n"
        "• Mở từ dòng cha / dòng TỔNG → gộp 1 dòng / phiếu; ô Nhân viên, Phòng ban, Bộ phận hiện "
        "người / đơn vị đại diện kèm “+N”; bỏ cột Vai trò.\n"
        "• Cột của chiều đã cố định (phòng ban / bộ phận / nhân viên trên đường dẫn, loại đã bấm, "
        "nhóm trạng thái đã bấm) bị bỏ cùng ô lọc tương ứng.\n"
        "• Lỗi khi tải → hiển thị “Lỗi khi tải danh sách chi tiết”.")

d.p("2.7.2 Layout màn hình")
d.layout(menu=MENU + " => Bấm số trên bảng", modal="Danh sách đầu việc chi tiết",
         shot=shot("05-popup-chi-tiet.png"),
         shot_caption="Danh sách Tổng đầu việc theo Phòng ban (gộp theo phiếu)")

d.p("2.7.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Tiêu đề", "Label", "Hiển thị", "–", "Theo ô đã bấm",
     "“Đang xem <chỉ tiêu> theo <Cấp>: <Tên>”. Chỉ tiêu: Tổng đầu việc, Đầu việc đã hoàn thành / "
     "đang thực hiện / quá hạn / dừng-huỷ-từ chối, Meeting, Task, Issue, Phiếu công tác, Phiếu "
     "giao việc."),
    ("Dòng phụ", "Label", "Hiển thị", "–", "Theo dữ liệu",
     "Đường dẫn cấp cha (nếu có) · “N đầu việc · M lượt tham gia · hoàn thành a · quá hạn b” · kỳ."),
    ("Bộ cột đầy đủ", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "STT · Loại · Phòng ban · Bộ phận · Nhân viên · Vai trò · Mã/Số phiếu · Tên công việc · Bắt "
     "đầu · Kết thúc/Hạn · Trạng thái. Số cột co lại theo chiều đã cố định."),
    ("Ô Nhân viên / Phòng ban / Bộ phận (popup gộp)", "Text", "Read-only", "–", "Theo dữ liệu",
     "Người đại diện (ưu tiên người chủ trì trong phạm vi đang xem) + “+N”; rê chuột hiện đủ tên."),
    ("Cột Vai trò", "Badge", "Read-only", "Chủ trì / Tham gia", "Theo dữ liệu",
     "Chỉ có ở popup mở từ dòng Nhân viên (trừ Task / Issue luôn là Chủ trì nên bỏ)."),
    ("Cột Tên công việc", "Button", "Enable", "–", "Theo dữ liệu", "Bấm mở chi tiết đầu việc (FR-09)."),
    ("Cột Bắt đầu / Kết thúc/Hạn", "Text", "Read-only", "dd/mm/yyyy HH:mm", "Theo dữ liệu",
     "Luôn có giờ. Task chưa có giờ bắt đầu nên hiển thị 00:00."),
    ("Cột Trạng thái", "Badge", "Read-only", "4 nhóm", "Theo dữ liệu", "Mỗi nhóm một màu."),
    ("Phân trang", "Pagination", "Enable", "20 / 50 / 100", "20 dòng / trang", "–"),
    ("Nút In danh sách / Xuất Excel danh sách / Đóng", "Button", "Enable", "–", "Hiển thị",
     "Xem FR-10 / FR-11; Đóng thì đóng popup."),
], required=False)

d.p("2.7.4 Danh sách event và xử lý event")
d.event_table([
    ("Bấm con số khác 0", "Click",
     "During:\n– Lọc theo bộ lọc báo cáo + dòng + chỉ tiêu, lọc trên từng lượt tham gia TRƯỚC rồi "
     "mới gộp theo phiếu.\n"
     "After:\n– Mở popup ở trạng thái mặc định: khối tổng hợp thu gọn, sắp theo Bắt đầu tăng dần, "
     "trang 1.\n– Lỗi → hiển thị “Lỗi khi tải danh sách chi tiết”."),
    ("Bấm Đóng", "Click", "After:\n– Đóng popup."),
])

# --------------------------------------------------------------- 2.8 FR-08
d.h3("2.8 Lọc, sắp xếp và tổng hợp trong danh sách chi tiết")
d.p("2.8.1 Giới thiệu")
d.rule_ref("- Kịch bản tìm kiếm, Bộ lọc, Dropdown. Chỉ bổ sung các quy tắc riêng của %s tại "
           "phần mô tả chi tiết." % TEN_MAN, anchor="search")
d.intro_table(
    ten="Lọc, sắp xếp và tổng hợp trong danh sách chi tiết",
    mota="Lọc sâu hơn trong popup, sắp xếp theo cột, xem KPI và phân bổ của tập đang lọc.",
    tacnhan=TAC_NHAN,
    dieukien="Popup danh sách đầu việc chi tiết đang mở.",
    chinh="1. Người dùng gõ ô tìm nhanh hoặc chọn ô lọc của popup.\n"
          "2. Popup lọc lại, về trang 1.\n"
          "3. Người dùng bấm tiêu đề cột để sắp xếp.\n"
          "4. Người dùng bấm “Xem tổng hợp” để xem KPI và phân bổ.",
    phu="• Bấm chip phân bổ → lọc nhanh theo mục đó; bấm lại để bỏ.\n"
        "• Mở popup khác → bộ lọc, sắp xếp, khối tổng hợp về mặc định.")

d.p("2.8.2 Layout màn hình")
d.layout(menu=MENU + " => Bấm số trên bảng => Xem tổng hợp", modal="Danh sách đầu việc chi tiết",
         shot=shot("06-popup-tong-hop.png"), shot_caption="Popup với khối tổng hợp đang mở")

d.p("2.8.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Ô tìm nhanh", "Textbox", "Enable", "0–255 ký tự", "Không", "Trống",
     "Gợi ý “Tìm mã, tên công việc…”."),
    ("Ô lọc Loại công việc / Phòng ban / Bộ phận / Nhân viên / Trạng thái", "Dropdown",
     "Enable / Ẩn", "Giá trị có trong popup", "Không", "“<tên>: tất cả”",
     "Ẩn ô của chiều đã cố định."),
    ("Tiêu đề cột sắp xếp được", "Icon Button", "Enable", "Tăng / giảm", "–", "Bắt đầu tăng dần",
     "Loại, Phòng ban, Bộ phận, Nhân viên, Bắt đầu, Kết thúc/Hạn, Trạng thái. Trạng thái sắp "
     "theo thứ tự Đã hoàn thành → Đang thực hiện → Quá hạn → Dừng/Huỷ/Từ chối; Bộ phận trống "
     "xếp cuối."),
    ("Nút Xem tổng hợp / Thu gọn", "Button", "Enable", "–", "–", "Thu gọn",
     "Mở / thu gọn khối “Tổng hợp danh sách đang xem”."),
    ("KPI Tỷ lệ hoàn thành / Tỷ lệ quá hạn", "Text", "Read-only", "0.0% – 100.0%", "–",
     "Theo dữ liệu", "Tính trên tập đang lọc."),
    ("KPI Tỷ lệ việc chủ trì / Tỷ lệ phiếu đơn vị chủ trì", "Text", "Read-only", "0.0% – 100.0%",
     "–", "Theo dữ liệu",
     "Popup Nhân viên: “Tỷ lệ việc chủ trì”; popup gộp: “Tỷ lệ phiếu đơn vị chủ trì”; ẩn hẳn ở "
     "popup gộp không cố định đơn vị nào (dòng TỔNG) vì luôn là 100%."),
    ("Dải chip “Phân bổ đầu việc theo cơ cấu”", "Button", "Enable", "–", "–", "Theo dữ liệu",
     "2 nhóm Loại công việc, Phòng ban; ẩn theo cùng luật ẩn ô lọc."),
])

d.p("2.8.4 Danh sách event và xử lý event")
d.event_table([
    ("Gõ tìm nhanh / chọn ô lọc / bấm chip", "Keypress / Change / Click",
     "After:\n– Lọc lại danh sách, về trang 1, cập nhật KPI và chip."),
    ("Bấm tiêu đề cột sắp xếp", "Click", "After:\n– Lần 1 tăng dần, lần 2 giảm dần."),
    ("Bấm Xem tổng hợp / Thu gọn", "Click", "After:\n– Mở / thu gọn khối tổng hợp."),
])

# --------------------------------------------------------------- 2.9 FR-09
d.h3("2.9 Xem chi tiết đầu việc")
d.p("2.9.1 Giới thiệu")
d.rule_ref("- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của %s tại phần mô "
           "tả chi tiết." % TEN_MAN, anchor="detail")
d.intro_table(
    ten="Xem chi tiết đầu việc",
    mota="Khung trượt bên phải hiển thị thông tin đầy đủ của 1 đầu việc, nằm trên popup danh sách.",
    tacnhan=TAC_NHAN,
    dieukien="Popup danh sách đầu việc chi tiết đang mở.",
    chinh="1. Người dùng bấm tên công việc.\n"
          "2. Hệ thống mở khung chi tiết đè lên popup.\n"
          "3. Khung hiển thị thông tin đầu việc và thành phần tham gia.",
    phu="• Bấm × hoặc bấm ra ngoài khung → đóng khung, popup danh sách giữ nguyên.")

d.p("2.9.2 Layout màn hình")
d.layout(menu=MENU + " => Bấm số trên bảng => Bấm tên công việc", modal="Chi tiết đầu việc",
         shot=shot("07-chi-tiet-dau-viec.png"), shot_caption="Khung chi tiết một đầu việc (Meeting)")

d.p("2.9.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Đầu khung", "Label", "Hiển thị", "–", "Theo dữ liệu",
     "Tên công việc, chip loại, chip mã phiếu, thời gian (gọn 1 ngày: “dd/mm/yyyy HH:mm – HH:mm”)."),
    ("Trạng thái", "Badge", "Read-only", "4 nhóm", "Theo dữ liệu", "Nhóm trạng thái theo dõi."),
    ("Trạng thái chứng từ", "Text", "Read-only", "–", "Theo dữ liệu",
     "Trạng thái gốc của chứng từ, có thể khác ô Trạng thái (vd Quá hạn / Đã duyệt)."),
    ("Bắt đầu (Meeting: Ngày họp)", "Text", "Read-only", "dd/mm/yyyy HH:mm", "Theo dữ liệu", "–"),
    ("Kết thúc / Hạn hoàn thành (Meeting: Kết thúc)", "Text", "Read-only", "dd/mm/yyyy HH:mm",
     "Theo dữ liệu", "–"),
    ("Tiến độ (Meeting: Biên bản họp)", "Text", "Read-only", "0 – 100 / –", "Theo dữ liệu",
     "Chỉ Task có % tiến độ; loại khác hiện “—”. Meeting: “Đã chốt biên bản” / “Chưa có biên "
     "bản” / “— (meeting đã huỷ)”."),
    ("Phòng ban / Bộ phận", "Text", "Read-only", "–", "Theo dữ liệu", "–"),
    ("Bảng Thành phần tham gia (N người)", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "STT · Nhân viên · Vai trò · Phòng ban · Bộ phận."),
    ("Nút ×", "Icon Button", "Enable", "–", "Hiển thị", "Đóng khung."),
], required=False)

d.p("2.9.4 Danh sách event và xử lý event")
d.event_table([
    ("Bấm tên công việc", "Click", "After:\n– Mở khung chi tiết từ dữ liệu sẵn có của popup."),
    ("Bấm × / bấm nền", "Click", "After:\n– Đóng khung."),
])

# --------------------------------------------------------------- 2.10 FR-10
d.h3("2.10 In danh sách chi tiết")
d.p("2.10.1 Biểu đồ Usecase")
d.uc_figure("FR-10", "In danh sách chi tiết", "io",
            [("include", "Lấy bộ lọc báo cáo + bộ lọc popup"), ("include", "Xem trước bản in")],
            actor=ACTOR_BGD, caption="Biểu đồ Use Case — FR-10 In danh sách chi tiết")

d.p("2.10.2 Giới thiệu")
d.rule_ref("- Quy tắc Excel và In ấn. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi "
           "tiết." % TEN_MAN, anchor="excel")
d.intro_table(
    ten="In danh sách chi tiết",
    mota="In đủ mọi dòng của tập đang lọc trong popup, đúng bộ cột và thứ tự đang xem.",
    tacnhan=TAC_NHAN,
    dieukien="Popup danh sách đầu việc chi tiết đang mở.",
    chinh="1. Người dùng bấm “In danh sách”.\n"
          "2. Hệ thống mở popup xem trước bản in.",
    phu="• Lỗi khi dựng bản in → popup xem trước hiển thị thông báo lỗi.")

d.p("2.10.3 Layout màn hình")
d.layout(menu=MENU + " => Bấm số trên bảng => In danh sách", modal="Danh sách đầu việc chi tiết",
         shot=shot("05-popup-chi-tiet.png"), shot_caption="Nút In danh sách ở chân popup")

d.p("2.10.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Nút In danh sách", "Button", "Enable", "–", "–", "Hiển thị", "Mở popup xem trước bản in."),
])

d.p("2.10.5 Danh sách event và xử lý event")
d.event_table([
    ("Bấm In danh sách", "Click", "After:\n– Mở popup xem trước bản in danh sách đang lọc."),
])

# --------------------------------------------------------------- 2.11 FR-11
d.h3("2.11 Xuất Excel danh sách chi tiết")
d.p("2.11.1 Biểu đồ Usecase")
d.uc_figure("FR-11", "Xuất Excel danh sách chi tiết", "io",
            [("include", "Lấy tập dòng đang lọc + thứ tự đang sắp"), ("include", "Tải file về máy")],
            actor=ACTOR_BGD, caption="Biểu đồ Use Case — FR-11 Xuất Excel danh sách chi tiết")

d.p("2.11.2 Giới thiệu")
d.rule_ref("- Quy tắc Excel. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi tiết."
           % TEN_MAN, anchor="excel")
d.intro_table(
    ten="Xuất Excel danh sách chi tiết",
    mota="Tải file Excel đủ mọi dòng của tập đang lọc trong popup, đúng bộ cột đang hiển thị.",
    tacnhan=TAC_NHAN,
    dieukien="Popup danh sách đầu việc chi tiết đang mở.",
    chinh="1. Người dùng bấm “Xuất Excel danh sách”.\n"
          "2. Trình duyệt tải file “Danh-sach-dau-viec.xls”.",
    phu="• Tập đang lọc rỗng → file chỉ có dòng tiêu đề cột.")

d.p("2.11.3 Layout màn hình")
d.layout(menu=MENU + " => Bấm số trên bảng => Xuất Excel danh sách", modal="Danh sách đầu việc chi tiết",
         shot=shot("05-popup-chi-tiet.png"), shot_caption="Nút Xuất Excel danh sách ở chân popup")

d.p("2.11.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Nút Xuất Excel danh sách", "Button", "Enable", "–", "–", "Hiển thị", "Tải file .xls về máy."),
])

d.p("2.11.5 Danh sách event và xử lý event")
d.event_table([
    ("Bấm Xuất Excel danh sách", "Click",
     "After:\n– Tải file “Danh-sach-dau-viec.xls” theo tập đang lọc, thứ tự đang sắp."),
])

# ==================================================== PHẦN 4. QUY TẮC NGHIỆP VỤ
d.h1("Phần 4. Quy tắc nghiệp vụ")
d.rule_ref(". Phần này chỉ ghi các quy tắc đặc thù của %s; không lặp lại các quy tắc đã có "
           "trong SRS quy tắc chung." % TEN_MAN,
           anchor="list", head="Quy tắc áp dụng",
           lead="Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ")

d.rule_table([
    ("BR-01", "Đầu việc thuộc kỳ khi GIAO NHAU với kỳ", [
        "– Đầu việc được tính khi khoảng (bắt đầu → kết thúc / hạn) chạm vào kỳ, không xét ngày "
        "tạo.",
        "– Một đầu việc kéo dài qua nhiều kỳ được đếm ở MỌI kỳ nó chạm — cộng 12 tháng có thể lớn "
        "hơn số cả năm.",
        "– Issue tính từ ngày phát hiện tới hạn xử lý. Task / Issue chưa đặt hạn lấy ngày tạo làm "
        "mốc để không bị bỏ sót.",
    ], "Toàn màn hình"),
    ("BR-02", "Người được tính", [
        "– Mọi người tham gia đều được tính, không chỉ người chủ trì (xem Thuật ngữ).",
        "– Meeting chỉ tính người phía công ty, không tính người phía khách hàng.",
        "– Phòng ban / Bộ phận của một dòng lấy theo hồ sơ của NGƯỜI ĐƯỢC TÍNH, không theo đơn vị "
        "ghi trên chứng từ.",
    ], "Toàn màn hình"),
    ("BR-03", "Cơ chế đếm theo cấp", [
        "– Dòng Nhân viên: có tham gia là +1.",
        "– Dòng Bộ phận, Phòng ban, TỔNG và dải tổng hợp: đếm THEO PHIẾU (1 phiếu nhiều người vẫn "
        "là 1).",
        "– Hệ quả có chủ đích: dòng cha nhỏ hơn tổng dòng con; cộng các phòng ban có thể lớn hơn "
        "dòng TỔNG (phiếu liên phòng được tính ở mỗi phòng).",
        "– Bật “Chỉ tính việc chủ trì”: mỗi phiếu chỉ còn 1 người nên 2 cách đếm trùng nhau.",
    ], ["Bảng theo dõi", "Dải tổng hợp"]),
    ("BR-04", "4 nhóm trạng thái", [
        "– Xét theo thứ tự: Dừng / Huỷ / Từ chối → Đã hoàn thành → Quá hạn → Đang thực hiện.",
        "– Đã hoàn thành: Meeting Hoàn thành; Task Hoàn thành; Issue Đã xử lý / Đã đóng / Hoàn "
        "thành; Phiếu công tác, Phiếu giao việc từ Đã duyệt kết quả trở đi.",
        "– Dừng / Huỷ / Từ chối: Meeting Huỷ; Task Tạm dừng / Huỷ / Từ chối; Issue Từ chối; Phiếu "
        "công tác Không duyệt; Phiếu giao việc Từ chối.",
        "– Quá hạn: ngày kết thúc / hạn đã qua ĐẦU NGÀY hôm nay mà chưa xong — việc hạn hôm nay "
        "chưa bị tính quá hạn.",
        "– 4 nhóm chia hết Tổng đầu việc; việc đã dừng / huỷ không bị tính quá hạn.",
    ], ["Dải tổng hợp", "Cột Đã HT", "Bộ lọc Trạng thái"]),
    ("BR-05", "Nháp và huỷ vẫn nằm trong Tổng", [
        "– Không loại trạng thái nào khỏi Tổng: bản nháp, chờ duyệt, huỷ, từ chối đều được tính.",
    ], "Toàn màn hình"),
    ("BR-06", "Loại công việc", [
        "– Bỏ loại nào thì ẩn cột loại đó và trừ khỏi Tổng, Đã HT, Tỷ lệ HT, dải tổng hợp.",
        "– Bỏ hết 5 loại → báo cáo trống (không hiểu là “tất cả”).",
    ], "Bộ lọc Loại công việc"),
    ("BR-07", "Cấu trúc cây", [
        "– Phòng ban ▸ Bộ phận ▸ Nhân viên; Công ty là ô lọc, không phải cấp cây.",
        "– Cấp Bộ phận chỉ xuất hiện ở phòng có chia bộ phận; nhân viên chưa gán bộ phận treo thẳng "
        "dưới phòng ban.",
        "– Nhân viên chưa gán phòng ban gom vào nhóm “Chưa phân phòng ban”.",
        "– “Chỉ hiện NV có việc” (mặc định bật) ẩn nhân viên có Tổng = 0.",
    ], ["Bảng theo dõi", "Bản in", "Excel"]),
    ("BR-08", "Phạm vi dữ liệu và quyền", [
        "– Chỉ xem được CÔNG TY ĐANG LÀM VIỆC; chọn công ty khác bị từ chối.",
        "– V1: cả công ty; V2: phòng ban được quản lý; V3: bộ phận được quản lý.",
        "– Không có quyền nào: không xem được báo cáo, không có mức “việc của mình”.",
    ], "Toàn màn hình"),
    ("BR-09", "Danh sách chi tiết khớp con số", [
        "– Popup mở từ dòng cha gộp 1 dòng / phiếu nên số dòng bằng đúng con số đã bấm.",
        "– Lọc trên từng lượt tham gia TRƯỚC rồi mới gộp: lọc 1 nhân viên trong popup phòng ban "
        "chỉ còn đầu việc của người đó, không kéo theo người khác.",
        "– Bỏ cột theo CHIỀU đã cố định, không bỏ theo dữ liệu (cột không nhảy ra vào khi lọc).",
    ], "FR-07, FR-08"),
    ("BR-10", "Bản in và Excel đủ dữ liệu", [
        "– In / Xuất Excel báo cáo luôn đủ mọi cấp, không phụ thuộc Cấp xem.",
        "– In / Xuất Excel danh sách chi tiết đủ mọi dòng của tập đang lọc, đúng thứ tự đang sắp.",
    ], ["FR-05", "FR-06", "FR-10", "FR-11"]),
])

d.save()
