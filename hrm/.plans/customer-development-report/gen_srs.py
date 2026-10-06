# -*- coding: utf-8 -*-
"""Sinh "SRS - Báo cáo phát triển khách hàng theo NVKD.docx" theo FORM CHUẨN 2026-08-28.

Chạy:  python3 .plans/customer-development-report/gen_srs.py
Thư viện dùng chung: .claude/skills/srs-documenter/assets/{srs_docx_lib,srs_uml_render}.py
Ảnh chụp thật (Playwright 1440x900, kỳ Quý III/2026): cdr_shots/ — chỉ để local, không commit.

Nguồn đối chiếu (nhánh gop_db, 03/10/2026):
- FE  hrm-client/pages/assign/report/customer-development/ (index, print, constants, 2 component)
- BE  hrm-api/Modules/Assign/Services/Report/CustomerDevelopmentReportService.php
      + CustomerDevelopmentReportController.php
- Quyền: Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (id 1087-1089)
- Menu: hrm-client/components/subsystem-menu/presale.js (nhóm "Báo cáo thị trường")

⚠️ Phần 2 + BR-09 ghi phạm vi dữ liệu THEO Ý NGHĨA TÊN QUYỀN. Code gop_db ngày 03/10/2026 còn
lệch 2 chỗ (đã báo user): (1) ô "Chưa tiềm năng" nhóm Phát triển KH mới không áp phạm vi quyền
— applyPermissionScopeToEmployees() là code chết; (2) FE gán cứng is_all_company/is_company = true
nên mọi người dùng đều thấy ô lọc Công ty – Phòng ban – Bộ phận – Nhân viên.
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

TEN_MAN = "Báo cáo phát triển khách hàng theo NVKD"
OUT = os.path.join(HERE, "SRS - %s.docx" % TEN_MAN)
SHOTS = os.path.join(HERE, "cdr_shots")
MENU = ("Phân hệ CSKH trước bán => Báo cáo => Báo cáo thị trường => "
        "Báo cáo phát triển khách hàng theo NVKD")

ACTOR_KD = "Nhân viên kinh doanh"
ACTOR_QL = "Trưởng phòng / Ban giám đốc"
TAC_NHAN = "Nhân viên kinh doanh; Trưởng phòng kinh doanh; Ban giám đốc; Người dùng đã đăng nhập"
STAGES = "Chưa tiềm năng, Đang trao đổi, Đang làm GP, Đang thương thảo, Đang thực hiện HĐ"


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(out=OUT, menu=MENU,
           route="/assign/report/customer-development",
           full_url="https://hrm.eteksofts.com/assign/report/customer-development",
           img_prefix="cdr_")

# =================================================================== TRANG ĐẦU
d.title_block(TEN_MAN)
d.h2("Mục lục")
d.toc()

# ========================================================= PHẦN 1. GIỚI THIỆU
d.h1("Phần 1. Giới thiệu")

d.h2("1 Mục đích")
d.p("Tài liệu này đặc tả yêu cầu phần mềm cho màn hình %s (tiêu đề trên màn: “Báo cáo kết quả "
    "phát triển khách hàng theo nhân viên”), nhằm:" % TEN_MAN)
d.bullets([
    "Là căn cứ nghiệm thu chức năng và phân quyền của báo cáo.",
    "Làm rõ 2 góc nhìn song song trong cùng một kỳ: Phát triển khách hàng mới và Kết quả chăm sóc "
    "trong kỳ — mỗi góc nhìn đếm theo cách khác nhau.",
    "Làm rõ cách xếp một khách hàng vào 1 trong 5 nhóm trạng thái theo tiến độ dự án tiền khả thi "
    "tại ngày cuối kỳ.",
    "Làm rõ phạm vi dữ liệu theo 3 cấp quyền xem và trường hợp không có quyền nào.",
])

d.h2("2 Thuật ngữ và viết tắt")
d.table(["Thuật ngữ", "Mô tả"], [
    ("NVKD", "Nhân viên kinh doanh. Với khách hàng đã có dự án TKT: là NVKD chính của dự án; với "
             "khách hàng chưa có dự án TKT: là người tạo khách hàng."),
    ("Dự án TKT", "Dự án tiền khả thi gắn với khách hàng."),
    ("Khách hàng tổ chức", "Khách hàng loại Tổ chức. Báo cáo chỉ xét loại khách hàng này."),
    ("Phát triển KH mới", "Khách hàng tổ chức có NGÀY TẠO nằm trong kỳ, đếm theo từng cặp "
                          "(khách hàng, NVKD)."),
    ("Kết quả chăm sóc trong kỳ", "Khách hàng (cả cũ lẫn mới) có dự án TKT được TẠO trong kỳ, đếm "
                                  "theo từng cặp (khách hàng, NVKD chính của dự án)."),
    ("Nhóm trạng thái", "5 nhóm theo tiến độ dự án TKT: %s." % STAGES),
    ("Trạng thái tại cuối kỳ", "Trạng thái của dự án TKT tại NGÀY CUỐI KỲ, lấy từ lịch sử thay đổi "
                               "trạng thái — xem lại kỳ cũ vẫn ra đúng số của kỳ đó."),
    ("Lĩnh vực / Ngành hàng / Ứng dụng", "Phân loại của dự án TKT, dùng để lọc báo cáo."),
], widths=[1.8, 4.2])

# ========================================================= PHẦN 2. PHÂN QUYỀN
d.h1("Phần 2. Phân quyền")

d.h2("1 Danh sách quyền")
d.p("Nhóm quyền thao tác: màn hình không có quyền thao tác riêng. Mọi người dùng đã đăng nhập "
    "đều mở được màn hình và dùng được các chức năng xem, lọc, in, xuất Excel; quyền chỉ quyết "
    "định phạm vi dữ liệu nhìn thấy.")

d.p("Nhóm quyền quyết định phạm vi dữ liệu "
    "(xét theo thứ tự ưu tiên từ trên xuống, cấp nào có trước thì áp cấp đó):")
d.table(["Ký hiệu", "Tên quyền", "Phạm vi dữ liệu"], [
    ("V1", "Xem báo cáo phát triển khách hàng theo tổng công ty",
     "Toàn bộ khách hàng và dự án TKT của mọi công ty."),
    ("V2", "Xem báo cáo phát triển khách hàng theo công ty",
     "Dự án TKT thuộc công ty đang làm việc của người đăng nhập, cộng dự án do chính mình tạo; "
     "khách hàng chưa có dự án do nhân viên của công ty đó tạo."),
    ("V3", "Xem báo cáo phát triển khách hàng theo phòng ban",
     "Dự án TKT thuộc các phòng ban / bộ phận người đăng nhập được phân công quản lý, cộng dự án "
     "do chính mình tạo; khách hàng chưa có dự án do nhân viên các phòng ban / bộ phận đó tạo."),
    ("—", "(không có cấp nào)",
     "Vẫn mở được màn hình. Chỉ thấy dự án TKT do mình tạo hoặc mình là NVKD chính, và khách "
     "hàng chưa có dự án do chính mình tạo."),
], widths=[0.8, 2.3, 2.9])

d.h2("2 Ma trận phân quyền")
_ALL = ("✅", "✅", "✅", "✅ (chỉ dữ liệu của mình)")
d.table(["Chức năng", "V1", "V2", "V3", "Không có quyền nào"], [
    ("FR-01 Xem báo cáo",) + _ALL,
    ("FR-02 Tìm kiếm và lọc báo cáo",) + _ALL,
    ("FR-03 Cài đặt bộ lọc", "✅", "✅", "✅", "✅"),
    ("FR-04 Xem chi tiết / Chỉ xem cấp gốc",) + _ALL,
    ("FR-05 Xuất Excel",) + _ALL,
    ("FR-06 In báo cáo",) + _ALL,
    ("FR-07 Xem danh sách khách hàng chi tiết",) + _ALL,
    ("FR-08 Tìm kiếm trong danh sách chi tiết",) + _ALL,
], widths=[2.3, 0.7, 0.9, 0.9, 1.2])
d.p("Ghi chú: ba quyền V1, V2, V3 không chặn việc mở màn hình mà chỉ thu hẹp phạm vi dữ liệu. "
    "Bản in, file Excel và danh sách chi tiết dùng đúng phạm vi dữ liệu của màn hình.")

# ================================================ PHẦN 3. ĐẶC TẢ CHI TIẾT
d.h1("Phần 3. Đặc tả chi tiết theo từng chức năng")

d.h2("1 Sơ đồ UML tổng quan")
d.overview_figure2(
    [(ACTOR_KD, [0, 1]), (ACTOR_QL, [0, 1])],
    [("FR-01", "Xem báo cáo", "view"),
     ("FR-07", "Xem danh sách KH chi tiết", "view")],
    [("FR-02", "Tìm kiếm và lọc báo cáo", "view", "extend", [0], None),
     ("FR-03", "Cài đặt bộ lọc", "view", "extend", [0], None),
     ("FR-04", "Xem chi tiết / cấp gốc", "view", "extend", [0], None),
     ("FR-05", "Xuất Excel", "io", "extend", [0], None),
     ("FR-06", "In báo cáo", "io", "extend", [0], None),
     ("FR-08", "Tìm kiếm trong danh sách", "view", "extend", [1], None)],
    "Sơ đồ Use Case tổng quan màn %s" % TEN_MAN)
d.p("Danh sách khách hàng chi tiết (FR-07) không có lối vào riêng trên menu: nó mở ra khi bấm "
    "một con số khác 0 trên bảng của màn báo cáo (FR-01).")

d.h2("2 Đặc tả chi tiết từng chức năng")

# --------------------------------------------------------------- 2.1 FR-01
d.h3("2.1 Xem báo cáo")
d.p("2.1.1 Giới thiệu")
d.rule_ref("- Màn Danh sách. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi tiết."
           % TEN_MAN, anchor="list")
d.intro_table(
    ten="Xem báo cáo phát triển khách hàng theo NVKD",
    mota="Bảng tổng hợp theo Công ty ▸ Phòng ban ▸ Nhân viên KD, mỗi dòng có 2 khối số: Phát "
         "triển khách hàng mới và Kết quả chăm sóc trong kỳ, mỗi khối chia theo 5 nhóm trạng thái.",
    tacnhan=TAC_NHAN,
    dieukien="Người dùng đã đăng nhập vào hệ thống.",
    chinh="1. Người dùng vào menu theo đường dẫn ở mục Layout.\n"
          "2. Hệ thống áp kỳ mặc định: Xem theo Tháng, tháng và năm hiện tại.\n"
          "3. Hệ thống xác định phạm vi dữ liệu theo cấp quyền xem.\n"
          "4. Hệ thống tính số liệu 2 khối cho từng NVKD rồi cộng lên Phòng ban, Công ty.\n"
          "5. Bảng hiển thị ở chế độ “chỉ cấp gốc” (chỉ các dòng Công ty).",
    phu="• Không có dữ liệu → “Không có dữ liệu phù hợp bộ lọc.”.\n"
        "• Bấm dòng Công ty / Phòng ban (hoặc mũi tên đầu dòng) → mở / thu gọn riêng dòng đó.\n"
        "• Bấm một con số khác 0 → mở danh sách khách hàng chi tiết (FR-07). Số 0 không bấm được.\n"
        "• Ô “Chưa tiềm năng” của khối Kết quả chăm sóc luôn bằng 0 và không bấm được.")

d.p("2.1.2 Layout màn hình")
d.layout(menu=MENU, shot=shot("01-man-chinh.png"),
         shot_caption="Màn %s, kỳ Quý III/2026, chế độ chỉ cấp gốc" % TEN_MAN)

d.p("2.1.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Tiêu đề trang", "Label", "Hiển thị", "–", "Báo cáo kết quả phát triển khách hàng theo nhân viên", "–"),
    ("Tiêu đề bảng", "Label", "Hiển thị", "–",
     "Danh sách kết quả phát triển khách hàng theo Công ty – Phòng ban – Nhân viên KD", "–"),
    ("Nút Xem chi tiết / Chỉ xem cấp gốc", "Button", "Enable", "–", "Xem chi tiết", "Xem FR-04."),
    ("Nút Xuất Excel", "Button", "Enable", "–", "Hiển thị", "Xem FR-05."),
    ("Nút In báo cáo", "Button", "Enable", "–", "Hiển thị", "Xem FR-06."),
    ("Cột STT", "Table/Grid", "Read-only", "–", "–", "Ô mũi tên mở / thu gọn ở dòng Công ty, Phòng ban."),
    ("Cột Công ty / Phòng ban / Nhân viên KD", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "Dòng Công ty: “Công ty: <tên>” + “N KH mới · M KH chăm sóc”. Dòng Phòng ban: "
     "“Phòng ban: <tên>” + “N nhân viên”. Dòng nhân viên: họ tên + mã nhân viên · bộ phận. "
     "Không xác định công ty / phòng ban thì ghi “Không xác định”."),
    ("Khối “Phát triển khách hàng mới”", "Table/Grid", "Read-only", "≥ 0", "Theo dữ liệu",
     "6 cột: Số lượng, Chưa tiềm năng, Đang trao đổi, Đang làm GP, Đang thương thảo, Đang thực "
     "hiện HĐ. Số lượng = tổng 5 nhóm."),
    ("Khối “Kết quả chăm sóc trong kỳ (gồm KH cũ & mới)”", "Table/Grid", "Read-only", "≥ 0",
     "Theo dữ liệu", "6 cột như khối trên; cột Chưa tiềm năng luôn bằng 0, chữ mờ."),
    ("Ô số khác 0", "Button", "Enable", "–", "Theo dữ liệu", "Bấm mở danh sách chi tiết (FR-07)."),
    ("Ô số bằng 0", "Text", "Read-only", "–", "Theo dữ liệu", "Chữ mờ, không bấm được."),
    ("Trạng thái rỗng", "Label", "Hiển thị", "–", "Ẩn", "“Không có dữ liệu phù hợp bộ lọc.”"),
    ("Đang tải", "Loading", "Hiển thị", "–", "Ẩn", "“Đang tải dữ liệu...”"),
], required=False)

d.p("2.1.4 Danh sách event và xử lý event")
d.event_table([
    ("Mở màn hình", "System",
     "Before:\n– Xác định cấp quyền xem theo thứ tự V1 → V2 → V3 → không có quyền.\n"
     "During:\n– Áp kỳ mặc định (tháng hiện tại) và phạm vi dữ liệu.\n"
     "After:\n– Hiển thị bảng ở chế độ chỉ cấp gốc."),
    ("Bấm dòng Công ty / Phòng ban", "Click", "After:\n– Mở / thu gọn riêng dòng đó."),
    ("Bấm con số khác 0", "Click",
     "After:\n– Mở danh sách khách hàng chi tiết đúng dòng (Công ty / Phòng ban / Nhân viên), "
     "đúng khối và đúng nhóm trạng thái (FR-07)."),
])

# --------------------------------------------------------------- 2.2 FR-02
d.h3("2.2 Tìm kiếm và lọc báo cáo")
d.p("2.2.1 Giới thiệu")
d.rule_ref("- Kịch bản tìm kiếm, Bộ lọc, Dropdown. Chỉ bổ sung các quy tắc riêng của %s tại "
           "phần mô tả chi tiết." % TEN_MAN, anchor="search")
d.intro_table(
    ten="Tìm kiếm và lọc báo cáo",
    mota="Chọn kỳ báo cáo và thu hẹp số liệu theo cơ cấu tổ chức, nhóm khách hàng và phân loại "
         "dự án TKT.",
    tacnhan=TAC_NHAN,
    dieukien="Người dùng đang ở màn báo cáo. Panel bộ lọc mở sẵn khi vào màn.",
    chinh="1. Người dùng chọn giá trị ở một ô lọc.\n"
          "2. Hệ thống tải lại báo cáo ngay (không cần bấm nút tìm).\n"
          "3. Bảng cập nhật theo bộ lọc mới.",
    phu="• Đổi Xem theo thời gian → hiện đúng các ô của kiểu đó (Năm + Tháng / Năm + Quý / Năm / "
        "Thời gian), giá trị của ô bị ẩn được xoá.\n"
        "• Chọn Lĩnh vực / Ngành hàng / Ứng dụng → khối Phát triển KH mới chỉ còn khách hàng có dự "
        "án khớp phân loại; khách hàng chưa có dự án (Chưa tiềm năng) bị loại hẳn.\n"
        "• Bấm “Xóa lọc” → mọi ô về mặc định (Tháng hiện tại), tải lại.")

d.p("2.2.2 Layout màn hình")
d.layout(menu=MENU + " => Bộ lọc", shot=shot("02-bo-loc.png"),
         shot_caption="Panel bộ lọc báo cáo (mở sẵn khi vào màn), kỳ Quý III/2026")

d.p("2.2.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Xem theo thời gian", "Dropdown", "Enable", "Tuỳ chỉnh / Tháng / Quý / Năm", "Có", "Tháng",
     "Không xoá trống được."),
    ("Năm", "Dropdown", "Enable / Ẩn", "Năm hiện tại − 5 → năm hiện tại + 1", "Có",
     "Năm hiện tại", "Hiện khi xem theo Tháng, Quý, Năm."),
    ("Tháng", "Dropdown", "Enable / Ẩn", "Tháng 1 – Tháng 12", "Có", "Tháng hiện tại",
     "Hiện khi xem theo Tháng."),
    ("Quý", "Dropdown", "Enable / Ẩn", "Quý I – Quý IV", "Có", "Trống", "Hiện khi xem theo Quý."),
    ("Thời gian", "Datepicker", "Enable / Ẩn", "dd/mm/yyyy – dd/mm/yyyy", "Không", "Ẩn",
     "Hiện khi xem theo Tuỳ chỉnh. Phải chọn đủ 2 mốc mới có hiệu lực."),
    ("Công ty", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Ẩn khi thiếu quyền",
     "Chỉ hiện với quyền V1. Lọc theo công ty trong hồ sơ NVKD."),
    ("Phòng ban", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Ẩn khi thiếu quyền",
     "Hiện với V1, V2, V3. Lọc theo phòng ban trong hồ sơ NVKD."),
    ("Bộ phận", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Ẩn khi thiếu quyền",
     "Hiện với V1, V2, V3."),
    ("Nhân viên", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Ẩn khi thiếu quyền",
     "Hiện với V1, V2, V3."),
    ("Nhóm khách hàng", "Dropdown", "Enable", "Danh sách 6 giá trị", "Không", "Trống",
     "KH mới nhập ERP (chưa có hoạt động), KH chưa tiềm năng, KH đang trao đổi thông tin, KH đang "
     "xây dựng giải pháp, KH đang thương thảo HĐ, KH đang triển khai HĐ. Chỉ giữ lại NVKD có số "
     "> 0 ở nhóm đó (ở một trong 2 khối); các cột khác của NVKD vẫn hiển thị đủ."),
    ("Lĩnh vực", "Dropdown", "Enable", "Lĩnh vực có trong dự án TKT thuộc phạm vi", "Không",
     "Trống", "–"),
    ("Ngành hàng", "Dropdown", "Enable", "Ngành hàng có trong dự án TKT thuộc phạm vi", "Không",
     "Trống", "Không lọc dây chuyền theo Lĩnh vực."),
    ("Ứng dụng", "Dropdown", "Enable", "Ứng dụng có trong dự án TKT thuộc phạm vi", "Không",
     "Trống", "Không lọc dây chuyền theo Ngành hàng."),
    ("Nút Xóa lọc", "Button", "Enable", "–", "–", "Hiển thị", "Đưa bộ lọc về mặc định."),
])

d.p("2.2.4 Danh sách event và xử lý event")
d.event_table([
    ("Chọn giá trị ở một ô lọc", "Change",
     "During:\n– Đổi Xem theo thời gian → xoá giá trị Tháng / Quý / Thời gian không còn dùng.\n"
     "After:\n– Tải lại báo cáo theo bộ lọc mới."),
    ("Bấm Xóa lọc", "Click", "After:\n– Đưa mọi ô về mặc định (Tháng hiện tại) và tải lại."),
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
d.h3("2.4 Xem chi tiết / Chỉ xem cấp gốc")
d.p("2.4.1 Giới thiệu")
d.rule_ref("- Màn Danh sách. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi tiết."
           % TEN_MAN, anchor="list")
d.intro_table(
    ten="Xem chi tiết / Chỉ xem cấp gốc",
    mota="Bung toàn bộ bảng tới cấp Nhân viên KD hoặc thu về chỉ các dòng Công ty.",
    tacnhan=TAC_NHAN,
    dieukien="Bảng đang có dữ liệu.",
    chinh="1. Người dùng bấm “Xem chi tiết”.\n"
          "2. Hệ thống mở mọi dòng Công ty và Phòng ban, hiện tới từng nhân viên.\n"
          "3. Nhãn nút đổi thành “Chỉ xem cấp gốc”; bấm lần nữa để thu về các dòng Công ty.",
    phu="• Bấm từng dòng Công ty / Phòng ban vẫn mở / thu gọn riêng dòng đó, không đổi nhãn nút.")

d.p("2.4.2 Layout màn hình")
d.layout(menu=MENU + " => Xem chi tiết", shot=shot("04-xem-chi-tiet.png"),
         shot_caption="Bảng sau khi bấm Xem chi tiết — hiện tới từng nhân viên KD")

d.p("2.4.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Nút Xem chi tiết / Chỉ xem cấp gốc", "Button", "Enable", "–", "–", "Xem chi tiết",
     "Nút nền đặc khi đang ở chế độ cấp gốc, nút viền khi đang xem chi tiết."),
    ("Mũi tên đầu dòng", "Icon Button", "Enable", "–", "–", "Thu gọn",
     "Ở dòng Công ty và Phòng ban."),
])

d.p("2.4.4 Danh sách event và xử lý event")
d.event_table([
    ("Bấm Xem chi tiết", "Click", "After:\n– Mở mọi dòng Công ty, Phòng ban; nhãn đổi thành "
                                  "“Chỉ xem cấp gốc”."),
    ("Bấm Chỉ xem cấp gốc", "Click", "After:\n– Thu gọn mọi dòng; nhãn đổi thành “Xem chi tiết”."),
])

# --------------------------------------------------------------- 2.5 FR-05
d.h3("2.5 Xuất Excel")
d.p("2.5.1 Biểu đồ Usecase")
d.uc_figure("FR-05", "Xuất Excel", "io",
            [("include", "Lấy bộ lọc đang áp dụng"), ("include", "Tải file về máy")],
            actor=ACTOR_QL, caption="Biểu đồ Use Case — FR-05 Xuất Excel")

d.p("2.5.2 Giới thiệu")
d.rule_ref("- Quy tắc Excel. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi tiết."
           % TEN_MAN, anchor="excel")
d.intro_table(
    ten="Xuất Excel",
    mota="Tải file Excel bảng tổng hợp theo bộ lọc đang áp dụng.",
    tacnhan=TAC_NHAN,
    dieukien="Người dùng đang ở màn báo cáo.",
    chinh="1. Người dùng bấm “Xuất Excel”.\n"
          "2. Hệ thống dựng file theo bộ lọc đang áp dụng.\n"
          "3. Trình duyệt tải file “bao_cao_phat_trien_khach_hang.xls”.\n"
          "4. Hệ thống hiển thị thông báo “Xuất Excel thành công”.",
    phu="• Lỗi khi xuất → hiển thị “Lỗi khi xuất Excel”.",
    dacbiet="File có đủ mọi cấp Công ty ▸ Phòng ban ▸ Nhân viên, không phụ thuộc chế độ xem "
            "trên màn hình.")

d.p("2.5.3 Layout màn hình")
d.layout(menu=MENU + " => Xuất Excel", shot=shot("01-man-chinh.png"),
         shot_caption="Nút Xuất Excel ở góc phải tiêu đề bảng")

d.p("2.5.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Nút Xuất Excel", "Button", "Enable", "–", "–", "Hiển thị", "Tải file .xls về máy."),
    ("Thông báo", "Toast / Alert", "Hiển thị", "–", "–", "Ẩn",
     "“Xuất Excel thành công” / “Lỗi khi xuất Excel”."),
])

d.p("2.5.5 Danh sách event và xử lý event")
d.event_table([
    ("Bấm Xuất Excel", "Click",
     "During:\n– Lấy bộ lọc đang áp dụng.\n"
     "After:\n– Tải file “bao_cao_phat_trien_khach_hang.xls”, hiển thị “Xuất Excel thành công”.\n"
     "– Lỗi → hiển thị “Lỗi khi xuất Excel”."),
])

# --------------------------------------------------------------- 2.6 FR-06
d.h3("2.6 In báo cáo")
d.p("2.6.1 Biểu đồ Usecase")
d.uc_figure("FR-06", "In báo cáo", "io",
            [("include", "Mở trang in theo bộ lọc"), ("extend", "Gửi lệnh in tới máy in")],
            actor=ACTOR_QL, caption="Biểu đồ Use Case — FR-06 In báo cáo")

d.p("2.6.2 Giới thiệu")
d.rule_ref("- Quy tắc Excel và In ấn. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi "
           "tiết." % TEN_MAN, anchor="excel")
d.intro_table(
    ten="In báo cáo",
    mota="Mở trang in bảng tổng hợp theo bộ lọc đang áp dụng.",
    tacnhan=TAC_NHAN,
    dieukien="Người dùng đang ở màn báo cáo.",
    chinh="1. Người dùng bấm “In báo cáo”.\n"
          "2. Hệ thống mở trang in trong tab mới, mang theo bộ lọc đang áp dụng.\n"
          "3. Trang in hiển thị tiêu đề công ty, tên báo cáo, bảng và chỗ ký “Người lập”.\n"
          "4. Người dùng bấm “In” để in.",
    phu="• Lỗi khi tải dữ liệu → trang in hiển thị thông báo lỗi.",
    dacbiet="Bản in có đủ mọi cấp Công ty ▸ Phòng ban ▸ Nhân viên, STT nối chuỗi 1 → 1.1 → 1.1.1; "
            "tên cột rút gọn (SL, Chưa, Trao đổi, Làm GP, Thương thảo, Thực hiện HĐ).")

d.p("2.6.3 Layout màn hình")
d.layout(menu=MENU + " => In báo cáo", shot=shot("06-ban-in.png"),
         shot_caption="Trang in báo cáo (mở ở tab mới)")

d.p("2.6.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Nút In", "Button", "Enable", "–", "–", "Hiển thị", "Mở hộp thoại in; nút không xuất hiện trên bản in."),
    ("Tiêu đề công ty", "Label", "Hiển thị", "–", "–", "Hiển thị", "Ảnh tiêu đề của công ty."),
    ("Tên báo cáo", "Label", "Hiển thị", "–", "–",
     "BÁO CÁO KẾT QUẢ PHÁT TRIỂN KHÁCH HÀNG THEO NHÂN VIÊN", "–"),
    ("Bảng in", "Table/Grid", "Read-only", "–", "–", "Theo dữ liệu",
     "Cùng 14 cột như trên màn; dòng nhân viên ghi “Họ tên (mã nhân viên)”."),
    ("Chỗ ký", "Label", "Hiển thị", "–", "–", "Hiển thị", "“Ngày ...., tháng ...., năm ....” + Người lập."),
])

d.p("2.6.5 Danh sách event và xử lý event")
d.event_table([
    ("Bấm In báo cáo", "Click", "After:\n– Mở trang in trong tab mới với bộ lọc đang áp dụng."),
    ("Bấm In", "Click", "After:\n– Mở hộp thoại in của trình duyệt."),
])

# --------------------------------------------------------------- 2.7 FR-07
d.h3("2.7 Xem danh sách khách hàng chi tiết")
d.p("2.7.1 Giới thiệu")
d.rule_ref("- Màn Danh sách, Phân trang. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả "
           "chi tiết." % TEN_MAN, anchor="list")
d.intro_table(
    ten="Xem danh sách khách hàng chi tiết",
    mota="Liệt kê từng cặp (khách hàng, NVKD) tạo nên con số vừa bấm.",
    tacnhan=TAC_NHAN,
    dieukien="Người dùng bấm một con số khác 0 trên bảng.",
    chinh="1. Người dùng bấm con số.\n"
          "2. Hệ thống mở popup, dòng nhỏ phía trên ghi khối + nhóm trạng thái (vd “PHÁT TRIỂN KH "
          "MỚI · ĐANG LÀM GP”), tiêu đề là tên công ty / “công ty — phòng ban” / tên nhân viên.\n"
          "3. Hệ thống tải danh sách theo bộ lọc báo cáo + dòng + khối + nhóm trạng thái.\n"
          "4. Popup hiển thị toàn bộ danh sách trên 1 trang.",
    phu="• Bấm cột Số lượng → nhóm trạng thái là “Tất cả trạng thái”.\n"
        "• Không có dòng nào → “Không có dữ liệu phù hợp.”.\n"
        "• Bấm × → đóng popup.")

d.p("2.7.2 Layout màn hình")
d.layout(menu=MENU + " => Bấm số trên bảng", modal="Danh sách khách hàng chi tiết",
         shot=shot("05-popup-chi-tiet.png"),
         shot_caption="Danh sách khách hàng — Phát triển KH mới · Đang làm GP của một công ty")

d.p("2.7.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Dòng phụ trên tiêu đề", "Label", "Hiển thị", "–", "Theo ô đã bấm",
     "“Phát triển KH mới” / “Kết quả chăm sóc trong kỳ” · tên nhóm trạng thái."),
    ("Tiêu đề popup", "Label", "Hiển thị", "–", "Theo dòng đã bấm",
     "Tên công ty, “công ty — phòng ban” hoặc tên nhân viên."),
    ("Cột STT", "Table/Grid", "Read-only", "–", "–", "–"),
    ("Cột Khách hàng", "Table/Grid", "Read-only", "–", "Theo dữ liệu", "Mã khách hàng (chữ nhỏ) + tên."),
    ("Cột NVKD phụ trách", "Table/Grid", "Read-only", "–", "Theo dữ liệu", "–"),
    ("Cột Công ty / PB / BP", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "Công ty; dòng dưới: phòng ban · bộ phận của NVKD."),
    ("Cột Nhóm trạng thái", "Badge", "Read-only", "5 nhóm", "Theo dữ liệu", "Mỗi nhóm một màu."),
    ("Cột Dự án TKT gần nhất", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "Mã + tên dự án TKT mới tạo gần nhất của cặp khách hàng – NVKD; chưa có thì “—”."),
    ("Cột #Meeting", "Table/Grid", "Read-only", "≥ 0", "Theo dữ liệu",
     "Số meeting gắn với dự án TKT gần nhất."),
    ("Cột #Dự án TKT", "Table/Grid", "Read-only", "≥ 0", "Theo dữ liệu",
     "Tổng số dự án TKT của khách hàng do NVKD đó phụ trách (mọi thời điểm)."),
    ("Dòng “Hiển thị 1–N / N”", "Label", "Read-only", "–", "Theo kết quả", "Không phân trang."),
    ("Trạng thái rỗng", "Label", "Hiển thị", "–", "Ẩn", "“Không có dữ liệu phù hợp.”"),
], required=False)

d.p("2.7.4 Danh sách event và xử lý event")
d.event_table([
    ("Bấm con số khác 0", "Click",
     "During:\n– Ghép bộ lọc báo cáo với dòng đã bấm (thay ô Công ty / Phòng ban / Nhân viên bằng "
     "đúng dòng đó), khối và nhóm trạng thái.\n"
     "After:\n– Mở popup và tải danh sách."),
    ("Bấm ×", "Click", "After:\n– Đóng popup."),
])

# --------------------------------------------------------------- 2.8 FR-08
d.h3("2.8 Tìm kiếm trong danh sách chi tiết")
d.p("2.8.1 Giới thiệu")
d.rule_ref("- Kịch bản tìm kiếm. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi tiết."
           % TEN_MAN, anchor="search")
d.intro_table(
    ten="Tìm kiếm trong danh sách chi tiết",
    mota="Tìm nhanh khách hàng trong popup danh sách chi tiết.",
    tacnhan=TAC_NHAN,
    dieukien="Popup danh sách khách hàng chi tiết đang mở.",
    chinh="1. Người dùng nhập từ khoá vào ô Tìm kiếm.\n"
          "2. Người dùng bấm “Tìm kiếm” hoặc nhấn Enter.\n"
          "3. Hệ thống tải lại danh sách chỉ gồm dòng khớp từ khoá.",
    phu="• Bấm “Làm mới” → xoá từ khoá, tải lại toàn bộ danh sách.")

d.p("2.8.2 Layout màn hình")
d.layout(menu=MENU + " => Bấm số trên bảng => Tìm kiếm", modal="Danh sách khách hàng chi tiết",
         shot=shot("05-popup-chi-tiet.png"), shot_caption="Ô Tìm kiếm ở đầu popup danh sách chi tiết")

d.p("2.8.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Ô Tìm kiếm", "Textbox", "Enable", "0–255 ký tự", "Không", "Trống",
     "Gợi ý “Tên / mã KH / NVKD”. Tìm theo tên khách hàng, mã khách hàng, tên NVKD; không phân "
     "biệt hoa thường; khoảng trắng đầu cuối bị bỏ qua."),
    ("Nút Tìm kiếm", "Button", "Enable", "–", "–", "Hiển thị", "Áp từ khoá."),
    ("Nút Làm mới", "Button", "Enable", "–", "–", "Hiển thị", "Xoá từ khoá, tải lại."),
])

d.p("2.8.4 Danh sách event và xử lý event")
d.event_table([
    ("Bấm Tìm kiếm / nhấn Enter", "Click / Keypress",
     "After:\n– Tải lại danh sách theo từ khoá. Gõ chữ mà chưa bấm thì danh sách chưa đổi."),
    ("Bấm Làm mới", "Click", "After:\n– Xoá từ khoá và tải lại toàn bộ danh sách."),
])

# ==================================================== PHẦN 4. QUY TẮC NGHIỆP VỤ
d.h1("Phần 4. Quy tắc nghiệp vụ")
d.rule_ref(". Phần này chỉ ghi các quy tắc đặc thù của %s; không lặp lại các quy tắc đã có "
           "trong SRS quy tắc chung." % TEN_MAN,
           anchor="list", head="Quy tắc áp dụng",
           lead="Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ")

d.rule_table([
    ("BR-01", "Chỉ xét khách hàng tổ chức", [
        "– Khối Phát triển KH mới chỉ xét khách hàng loại Tổ chức.",
    ], "Khối Phát triển KH mới"),
    ("BR-02", "Khối Phát triển KH mới", [
        "– Khách hàng tổ chức có NGÀY TẠO trong kỳ.",
        "– Đã có dự án TKT (tạo trước hoặc trong ngày cuối kỳ): mỗi NVKD chính của các dự án đó là "
        "1 dòng đếm.",
        "– Chưa có dự án TKT tính tới ngày cuối kỳ: đếm 1 lần cho NGƯỜI TẠO khách hàng, nhóm Chưa "
        "tiềm năng. Dự án tạo sau ngày cuối kỳ coi như chưa có.",
    ], "Khối Phát triển KH mới"),
    ("BR-03", "Khối Kết quả chăm sóc trong kỳ", [
        "– Dự án TKT có NGÀY TẠO trong kỳ, của khách hàng cũ hay mới đều được tính.",
        "– Mỗi cặp (khách hàng, NVKD chính) là 1 dòng đếm.",
        "– Nhóm Chưa tiềm năng của khối này luôn bằng 0.",
    ], "Khối Kết quả chăm sóc"),
    ("BR-04", "Một khách hàng — nhiều NVKD", [
        "– Một khách hàng có thể xuất hiện ở nhiều NVKD và ở cả 2 khối, nhưng không lặp ở cùng 1 "
        "NVKD trong cùng 1 khối.",
    ], "Bảng tổng hợp"),
    ("BR-05", "Xếp nhóm trạng thái", [
        "– Lấy trạng thái của dự án TKT tại NGÀY CUỐI KỲ (theo lịch sử đổi trạng thái).",
        "– Thu thập thông tin dự án → Đang trao đổi; Chờ tiếp nhận làm GP / Đang làm GP / Đã duyệt "
        "GP / Dự toán → Đang làm GP; Thương thảo giá / Thương thảo dự án – hợp đồng → Đang thương "
        "thảo; Thực hiện HĐ / Nghiệm thu và thanh lý HĐ → Đang thực hiện HĐ.",
        "– Dự án Đang tạo, Đóng, Kết thúc và lưu trữ không được tính.",
        "– Cặp khách hàng – NVKD có nhiều dự án: lấy trạng thái CAO NHẤT.",
    ], "Toàn màn hình"),
    ("BR-06", "Kỳ báo cáo", [
        "– Mặc định: tháng hiện tại.",
        "– Tuỳ chỉnh phải chọn đủ 2 mốc; thiếu mốc thì hệ thống lấy năm hiện tại.",
    ], "Bộ lọc"),
    ("BR-07", "Lọc theo phân loại dự án", [
        "– Chọn Lĩnh vực / Ngành hàng / Ứng dụng: chỉ giữ dự án khớp phân loại; khách hàng chưa có "
        "dự án (Chưa tiềm năng) bị loại khỏi khối Phát triển KH mới.",
    ], "Bộ lọc"),
    ("BR-08", "Lọc Nhóm khách hàng", [
        "– Giữ NVKD có số > 0 ở nhóm đã chọn, ở khối bất kỳ; không ẩn các cột khác.",
        "– “KH mới nhập ERP (chưa có hoạt động)” và “KH chưa tiềm năng” cùng lọc theo nhóm Chưa "
        "tiềm năng.",
    ], "Bộ lọc Nhóm khách hàng"),
    ("BR-09", "Phạm vi dữ liệu theo quyền", [
        "– Xét theo thứ tự V1 → V2 → V3 → không có quyền (xem Phần 2), áp cho CẢ dự án TKT lẫn "
        "khách hàng chưa có dự án.",
        "– Ô lọc Công ty chỉ hiện với V1; Phòng ban / Bộ phận / Nhân viên hiện với V1, V2, V3.",
        "– Danh sách chi tiết, bản in, Excel dùng đúng phạm vi của màn hình.",
    ], "Toàn màn hình"),
    ("BR-10", "Cấu trúc bảng", [
        "– Công ty ▸ Phòng ban ▸ Nhân viên theo hồ sơ của NVKD. Số dòng cha là tổng các dòng con.",
        "– Chỉ hiện NVKD có ít nhất 1 dòng đếm trong kỳ.",
    ], ["Bảng tổng hợp", "Bản in", "Excel"]),
])

d.save()
