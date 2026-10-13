# -*- coding: utf-8 -*-
"""Sinh "SRS - Báo cáo kết quả meeting theo thị trường.docx" theo FORM CHUẨN 2026-08-28.

Chạy:  python3 .plans/meeting-by-market/gen_srs.py
Thư viện dùng chung: .claude/skills/srs-documenter/assets/{srs_docx_lib,srs_uml_render}.py
Ảnh chụp thật (Playwright 1440x900, kỳ mặc định "Tất cả"): mbm_shots/ — chỉ để local, không commit.

Nguồn đối chiếu (nhánh gop_db, 03/10/2026):
- FE  hrm-client/pages/assign/report/meeting-by-market/ (index + 4 component)
      + pages/assign/my-todo/components/calendar/WorkItemDetailDrawer.vue (panel chi tiết dùng chung)
- BE  hrm-api/Modules/Assign/Services/Report/MeetingByMarketService.php
      + MeetingByMarketReportController.php + resources/views/exports/assign/meeting_by_market_report
- Quyền: Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (id 1174-1176)
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

TEN_MAN = "Báo cáo kết quả meeting theo thị trường"
OUT = os.path.join(HERE, "SRS - %s.docx" % TEN_MAN)
SHOTS = os.path.join(HERE, "mbm_shots")
MENU = ("Phân hệ CSKH trước bán => Báo cáo => Báo cáo thị trường => "
        "Báo cáo kết quả meeting theo thị trường")

ACTOR_KD = "Nhân viên kinh doanh"
ACTOR_QL = "Trưởng phòng / Ban giám đốc"
TAC_NHAN = "Nhân viên kinh doanh; Trưởng phòng kinh doanh; Ban giám đốc; Người dùng đã đăng nhập"


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(out=OUT, menu=MENU,
           route="/assign/report/meeting-by-market",
           full_url="https://hrm.eteksofts.com/assign/report/meeting-by-market",
           img_prefix="mbm_")

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
    "Làm rõ cách nhóm meeting theo 3 cấp Thị trường ▸ Khách hàng ▸ Meeting và cách đánh số.",
    "Làm rõ cách tính các chỉ tiêu của dải tổng hợp (Dự án, KH mới, Tỷ lệ hoàn thành, phân bổ "
    "theo trạng thái / phòng chủ trì / thị trường).",
    "Làm rõ phạm vi dữ liệu theo 3 cấp quyền xem và trường hợp không có quyền nào.",
])

d.h2("2 Thuật ngữ và viết tắt")
d.table(["Thuật ngữ", "Mô tả"], [
    ("Meeting", "Cuộc họp có gắn khách hàng, ở một trong 4 trạng thái: Lên lịch, Chốt lịch, "
                "Hoàn thành, Hủy. Meeting chưa gắn khách hàng không vào báo cáo."),
    ("Thị trường", "Tỉnh/Thành phố của khách hàng. Khách hàng chưa có tỉnh/thành phố được gom vào "
                   "nhóm “Chưa xác định thị trường”."),
    ("Kỳ báo cáo", "Khoảng thời gian xét NGÀY BẮT ĐẦU của meeting. Để trống là Tất cả (không giới "
                   "hạn thời gian)."),
    ("Người chủ trì", "Người chủ trì meeting; meeting không ghi người chủ trì thì lấy người tạo "
                      "meeting."),
    ("Phòng chủ trì", "Phòng ban trong hồ sơ của người chủ trì."),
    ("Thành phần công ty / bên KH", "Danh sách người tham dự phía công ty / phía khách hàng của "
                                    "meeting."),
    ("Phiếu công tác", "Phiếu công tác được lập từ meeting. Chấm công GPS của phiếu công tác là "
                       "nguồn của Lịch sử chấm công."),
    ("Dự án TKT", "Dự án tiền khả thi được gắn với meeting."),
    ("Panel chi tiết", "Khung trượt từ bên phải màn hình hiển thị thông tin đầy đủ của 1 meeting."),
], widths=[1.8, 4.2])

# ========================================================= PHẦN 2. PHÂN QUYỀN
d.h1("Phần 2. Phân quyền")

d.h2("1 Danh sách quyền")
d.p("Nhóm quyền thao tác: màn hình không có quyền thao tác riêng. Mọi người dùng đã đăng nhập "
    "đều mở được màn hình và dùng được các chức năng xem, lọc, xuất Excel; quyền chỉ quyết định "
    "phạm vi dữ liệu nhìn thấy. Riêng nút Sửa trên panel chi tiết meeting theo quyền sửa của "
    "chính meeting đó.")

d.p("Nhóm quyền quyết định phạm vi dữ liệu "
    "(xét theo thứ tự ưu tiên từ trên xuống, cấp nào có trước thì áp cấp đó):")
d.table(["Ký hiệu", "Tên quyền", "Phạm vi dữ liệu"], [
    ("V1", "Xem báo cáo kết quả meeting theo thị trường theo tổng công ty",
     "Toàn bộ meeting của mọi công ty. Bộ lọc hiện thêm ô Công ty."),
    ("V2", "Xem báo cáo kết quả meeting theo thị trường theo công ty",
     "Meeting thuộc công ty đang làm việc của người đăng nhập, cộng meeting do chính mình tạo."),
    ("V3", "Xem báo cáo kết quả meeting theo thị trường theo phòng ban",
     "Meeting thuộc các phòng ban / bộ phận người đăng nhập được phân công quản lý, cộng meeting "
     "do chính mình tạo."),
    ("—", "(không có cấp nào)",
     "Vẫn mở được màn hình. Chỉ thấy meeting do chính mình tạo hoặc mình là thành viên tham dự. "
     "Ẩn các ô lọc Công ty, Phòng ban, Bộ phận, Nhân viên."),
], widths=[0.8, 2.3, 2.9])

d.h2("2 Ma trận phân quyền")
_ALL = ("✅", "✅", "✅", "✅ (chỉ meeting của mình)")
d.table(["Chức năng", "V1", "V2", "V3", "Không có quyền nào"], [
    ("FR-01 Xem báo cáo",) + _ALL,
    ("FR-02 Tìm kiếm và lọc báo cáo",
     "✅", "✅ (không có ô Công ty)", "✅ (không có ô Công ty)",
     "✅ (chỉ Kỳ, Thị trường, Trạng thái, Loại meeting)"),
    ("FR-03 Cài đặt bộ lọc", "✅", "✅", "✅", "✅"),
    ("FR-04 Mở hết / thu gọn nhóm",) + _ALL,
    ("FR-05 Xuất Excel",) + _ALL,
    ("FR-06 Xem thành phần tham dự",) + _ALL,
    ("FR-07 Xem lịch sử chấm công GPS",) + _ALL,
    ("FR-08 Xem chi tiết meeting",) + _ALL,
    ("FR-09 Xem biên bản cuộc họp",) + _ALL,
    ("FR-10 Mở dự án TKT",
     "✅ (theo quyền màn Dự án TKT)", "✅ (theo quyền màn Dự án TKT)",
     "✅ (theo quyền màn Dự án TKT)", "✅ (theo quyền màn Dự án TKT)"),
], widths=[2.3, 0.7, 0.9, 0.9, 1.2])
d.p("Ghi chú: ba quyền V1, V2, V3 không chặn việc mở màn hình mà chỉ thu hẹp phạm vi dữ liệu. "
    "File Excel và Lịch sử chấm công dùng đúng phạm vi dữ liệu của màn hình.")

# ================================================ PHẦN 3. ĐẶC TẢ CHI TIẾT
d.h1("Phần 3. Đặc tả chi tiết theo từng chức năng")

d.h2("1 Sơ đồ UML tổng quan")
d.overview_figure2(
    [(ACTOR_KD, [0, 1]), (ACTOR_QL, [0, 1])],
    [("FR-01", "Xem báo cáo", "view"),
     ("FR-08", "Xem chi tiết meeting", "view")],
    [("FR-02", "Tìm kiếm và lọc báo cáo", "view", "extend", [0], None),
     ("FR-03", "Cài đặt bộ lọc", "view", "extend", [0], None),
     ("FR-04", "Mở hết / thu gọn nhóm", "view", "extend", [0], None),
     ("FR-05", "Xuất Excel", "io", "extend", [0], None),
     ("FR-06", "Xem thành phần tham dự", "view", "extend", [0], None),
     ("FR-07", "Xem lịch sử chấm công", "view", "extend", [0], None),
     ("FR-10", "Mở dự án TKT", "view", "extend", [0], None),
     ("FR-09", "Xem biên bản cuộc họp", "io", "extend", [0, 1], None)],
    "Sơ đồ Use Case tổng quan màn %s" % TEN_MAN)
d.p("Panel chi tiết meeting (FR-08) không có lối vào riêng trên menu: nó mở ra khi bấm tên "
    "meeting trên bảng của màn báo cáo (FR-01). Biên bản (FR-09) mở được từ cả bảng lẫn panel.")

d.h2("2 Đặc tả chi tiết từng chức năng")

# --------------------------------------------------------------- 2.1 FR-01
d.h3("2.1 Xem báo cáo")
d.p("2.1.1 Giới thiệu")
d.rule_ref("- Màn Danh sách, Phân trang. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả "
           "chi tiết." % TEN_MAN, anchor="list")
d.intro_table(
    ten="Xem báo cáo kết quả meeting theo thị trường",
    mota="Liệt kê các meeting với khách hàng, nhóm theo Thị trường ▸ Khách hàng ▸ Meeting, kèm "
         "dải tổng hợp, để theo dõi mỗi thị trường đã tổ chức bao nhiêu meeting với khách hàng "
         "nào và kết quả ra sao.",
    tacnhan=TAC_NHAN,
    dieukien="Người dùng đã đăng nhập vào hệ thống.",
    chinh="1. Người dùng vào menu theo đường dẫn ở mục Layout.\n"
          "2. Hệ thống xác định cấp quyền xem (V1 → V2 → V3 → không có quyền).\n"
          "3. Hệ thống lấy meeting trong phạm vi, Kỳ báo cáo mặc định để trống (Tất cả).\n"
          "4. Hệ thống tính dải tổng hợp trên toàn bộ tập meeting.\n"
          "5. Bảng hiển thị trang 1 (20 meeting), mọi nhóm đều đang mở.",
    phu="• Không có meeting nào khớp bộ lọc → hiển thị “Không có dữ liệu”, ẩn bảng.\n"
        "• Lỗi khi tải → hiển thị thông báo “Lỗi khi tải dữ liệu”.\n"
        "• Bấm dòng thị trường / khách hàng → thu gọn hoặc mở riêng nhóm đó.\n"
        "• Bấm tên meeting → mở panel chi tiết meeting (FR-08).\n"
        "• Bảng rộng hơn màn hình → có thanh cuộn ngang ở cả phía trên và phía dưới bảng; tên "
        "nhóm thị trường / khách hàng đứng yên khi cuộn ngang.")

d.p("2.1.2 Layout màn hình")
d.layout(menu=MENU, shot=shot("01-man-chinh.png"),
         shot_caption="Màn %s lúc mới truy cập (kỳ Tất cả)" % TEN_MAN)
d.figure(shot("08-cot-ket-qua.png"),
         "Phần cuối bảng: Trạng thái, Biên bản họp / Lý do huỷ, Dự án TKT, Phiếu công tác",
         width_in=6.2)

d.p("2.1.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Tiêu đề trang", "Label", "Hiển thị", "–", TEN_MAN,
     "Kèm icon ⓘ: “Theo dõi mỗi thị trường (tỉnh/thành) đã tổ chức bao nhiêu cuộc meeting với "
     "khách hàng nào, kết quả ra sao.”"),
    ("Nút Xuất Excel", "Button", "Enable", "–", "Hiển thị", "Xem FR-05."),
    ("Nút Cài đặt bộ lọc", "Button", "Enable", "–", "Hiển thị", "Xem FR-03."),
    ("Nút Tìm kiếm nâng cao", "Button", "Enable", "–", "Bộ lọc thu gọn", "Xem FR-02."),
    ("Ô “Số meeting”", "Text", "Read-only", "≥ 0", "Theo dữ liệu",
     "Tổng số meeting của toàn bộ tập đang lọc (không theo trang)."),
    ("Khối “Tổng hợp”", "Text", "Read-only", "–", "Theo dữ liệu",
     "Dự án (số dự án TKT khác nhau gắn với các meeting), KH mới, Tỷ lệ hoàn thành (%)."),
    ("Khối “Theo trạng thái”", "Text", "Read-only", "–", "Theo dữ liệu",
     "Số meeting Lên lịch, Chốt lịch, Hoàn thành, Hủy; mỗi trạng thái một màu."),
    ("Khối “Theo phòng chủ trì”", "Text", "Read-only", "–", "Theo dữ liệu",
     "Số meeting theo phòng của người chủ trì, sắp A→Z, nhóm “—” (không xác định) xuống cuối."),
    ("Khối “Theo thị trường”", "Text", "Read-only", "–", "Theo dữ liệu",
     "Số meeting theo thị trường, sắp A→Z, “Chưa xác định thị trường” xuống cuối."),
    ("Dải tổng hợp", "Text", "Read-only", "–", "Hiển thị",
     "4 khối trên 1 hàng ngang; tràn bề ngang thì cuộn ngang."),
    ("Nút Mở hết / Thu gọn (tiêu đề cột Tên meeting)", "Button", "Enable", "–", "Thu gọn",
     "Xem FR-04."),
    ("Cột STT", "Table/Grid", "Read-only", "–", "Theo vị trí",
     "Thị trường đánh số La Mã (I, II, …); khách hàng đánh 1, 2, … đếm lại theo từng thị trường; "
     "meeting đánh 1.1, 1.2, …"),
    ("Dòng nhóm Thị trường", "Table/Grid", "Read-only", "–", "Đang mở",
     "Tên thị trường viết hoa + “N khách hàng · M meeting” (đếm trên trang đang xem). Bấm để thu gọn / mở."),
    ("Dòng nhóm Khách hàng", "Table/Grid", "Read-only", "–", "Đang mở",
     "Tên khách hàng + mã khách hàng + “M meeting”. Bấm để thu gọn / mở."),
    ("Cột Tên meeting", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "Liên kết, bấm mở panel chi tiết (FR-08)."),
    ("Cột Loại meeting", "Table/Grid", "Read-only", "–", "Theo dữ liệu", "–"),
    ("Cột Thời gian", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "Cùng ngày: “HH:mm–HH:mm dd/mm/yyyy”; khác ngày: “dd/mm/yyyy – dd/mm/yyyy”; không có giờ "
     "kết thúc: “HH:mm dd/mm/yyyy”."),
    ("Cột Địa điểm", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "Họp trực tuyến: “Trực tuyến” + đường link (chỉ link http/https mới bấm được)."),
    ("Cột Người chủ trì", "Table/Grid", "Read-only", "–", "Theo dữ liệu", "–"),
    ("Cột Phòng chủ trì", "Table/Grid", "Read-only", "–", "Theo dữ liệu", "Phòng của người chủ trì."),
    ("Cột Thành phần công ty", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "Hiện người đầu tiên + chip “+N” bấm được (FR-06)."),
    ("Cột Thành phần bên KH", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "Hiện người đầu tiên kèm chức vụ + chip “+N” bấm được (FR-06)."),
    ("Cột Trạng thái", "Badge", "Read-only", "Lên lịch / Chốt lịch / Hoàn thành / Hủy",
     "Theo dữ liệu", "Mỗi trạng thái một màu."),
    ("Cột Biên bản họp / Lý do huỷ", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "Hoàn thành + có biên bản: nút “Xem biên bản” (FR-09). Hủy: lý do huỷ (chữ đỏ). Còn lại: “—”."),
    ("Cột Dự án TKT", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "Mã các dự án TKT gắn với meeting, bấm được (FR-10)."),
    ("Cột Phiếu công tác / Lịch sử chấm công", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "Mã phiếu công tác lập từ meeting; có chấm công thì thêm nút “Xem lịch sử chấm công” (FR-07)."),
    ("Ô trống dữ liệu", "Text", "Read-only", "–", "—", "Hiển thị “—” khi không có giá trị."),
    ("Dòng “Hiển thị a–b / N meeting”", "Label", "Read-only", "–", "Theo kết quả",
     "N là tổng số meeting khớp bộ lọc."),
    ("Phân trang", "Pagination", "Enable", "10 / 20 / 50 / 100", "20 meeting / trang",
     "Đếm theo meeting; nhóm thị trường / khách hàng dựng lại trên từng trang."),
    ("Trạng thái rỗng", "Label", "Hiển thị", "–", "Ẩn", "“Không có dữ liệu”."),
    ("Đang tải", "Loading", "Hiển thị", "–", "Ẩn", "“Đang tải dữ liệu...”."),
], required=False)

d.p("2.1.4 Danh sách event và xử lý event")
d.event_table([
    ("Mở màn hình", "System",
     "Before:\n– Xác định cấp quyền xem theo thứ tự V1 → V2 → V3 → không có quyền.\n"
     "During:\n– Áp phạm vi dữ liệu, Kỳ báo cáo để trống (Tất cả).\n"
     "After:\n– Hiển thị dải tổng hợp và trang 1 của bảng, mọi nhóm đang mở.\n"
     "– Lỗi khi tải → hiển thị “Lỗi khi tải dữ liệu”."),
    ("Bấm dòng nhóm Thị trường / Khách hàng", "Click",
     "After:\n– Thu gọn / mở riêng nhóm đó. Thu gọn thị trường ẩn cả khách hàng lẫn meeting bên "
     "dưới; thu gọn khách hàng chỉ ẩn meeting của khách hàng đó."),
    ("Bấm tên meeting", "Click", "After:\n– Mở panel chi tiết meeting (FR-08)."),
    ("Đổi trang / đổi số dòng mỗi trang", "Click / Change",
     "After:\n– Tải lại trang tương ứng theo bộ lọc hiện tại; đổi số dòng thì về trang 1. "
     "Mọi nhóm của trang mới đều đang mở."),
])

# --------------------------------------------------------------- 2.2 FR-02
d.h3("2.2 Tìm kiếm và lọc báo cáo")
d.p("2.2.1 Giới thiệu")
d.rule_ref("- Kịch bản tìm kiếm, Bộ lọc, Dropdown. Chỉ bổ sung các quy tắc riêng của %s tại "
           "phần mô tả chi tiết." % TEN_MAN, anchor="search")
d.intro_table(
    ten="Tìm kiếm và lọc báo cáo",
    mota="Thu hẹp danh sách meeting theo kỳ, thị trường, trạng thái, loại meeting và cơ cấu tổ chức.",
    tacnhan=TAC_NHAN,
    dieukien="Người dùng đang ở màn báo cáo.",
    chinh="1. Người dùng bấm “Tìm kiếm nâng cao” để mở panel bộ lọc.\n"
          "2. Người dùng chọn giá trị ở một ô lọc.\n"
          "3. Hệ thống tải lại báo cáo ngay (không cần bấm nút tìm), bảng về trang 1.\n"
          "4. Dải tổng hợp và bảng cập nhật theo bộ lọc mới.",
    phu="• Chọn Kỳ báo cáo = Tuỳ chỉnh → hiện thêm ô Thời gian để chọn khoảng ngày.\n"
        "• Đổi từ Tuỳ chỉnh sang kỳ dựng sẵn → ô Thời gian ẩn, khoảng ngày đã chọn bị xoá.\n"
        "• Bấm “Xóa lọc” → mọi ô về trống (Kỳ = Tất cả), tải lại trang 1.")

d.p("2.2.2 Layout màn hình")
d.layout(menu=MENU + " => Tìm kiếm nâng cao", shot=shot("02-bo-loc.png"),
         shot_caption="Panel bộ lọc báo cáo đang mở")

d.p("2.2.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Kỳ báo cáo", "Dropdown", "Enable", "Danh sách 6 giá trị", "Không", "Trống (Tất cả)",
     "Hôm nay, Tuần này, Tháng này, Quý này, Năm nay, Tuỳ chỉnh. Để trống là không giới hạn "
     "thời gian."),
    ("Thời gian", "Datepicker", "Enable / Ẩn", "dd/mm/yyyy – dd/mm/yyyy", "Không", "Ẩn",
     "Chỉ hiện khi Kỳ báo cáo = Tuỳ chỉnh. Chỉ chọn 1 mốc thì lọc 1 chiều (từ ngày / đến ngày); "
     "bỏ trống cả 2 mốc thì không giới hạn thời gian."),
    ("Thị trường", "Dropdown", "Enable", "Danh sách tỉnh/TP", "Không", "Trống", "–"),
    ("Trạng thái", "Dropdown", "Enable", "Lên lịch / Chốt lịch / Hoàn thành / Hủy", "Không",
     "Trống", "–"),
    ("Loại meeting", "Dropdown", "Enable", "Danh mục loại meeting", "Không", "Trống", "–"),
    ("Công ty", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Ẩn khi thiếu quyền",
     "Chỉ hiện với quyền V1. Lọc theo công ty của meeting."),
    ("Phòng ban", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Ẩn khi thiếu quyền",
     "Hiện với V1, V2, V3. Lọc theo phòng ban ghi trên meeting (phòng của người tạo meeting)."),
    ("Bộ phận", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Ẩn khi thiếu quyền",
     "Hiện với V1, V2, V3. Lọc theo bộ phận ghi trên meeting."),
    ("Nhân viên", "Dropdown", "Enable / Ẩn", "Danh sách", "Không", "Ẩn khi thiếu quyền",
     "Hiện với V1, V2, V3. Lấy meeting do nhân viên đó tạo hoặc nhân viên đó là thành viên."),
    ("Nút Xóa lọc", "Button", "Enable", "–", "–", "Hiển thị", "Đưa mọi ô lọc về trống."),
])

d.p("2.2.4 Danh sách event và xử lý event")
d.event_table([
    ("Bấm Tìm kiếm nâng cao", "Click", "After:\n– Mở / thu gọn panel bộ lọc."),
    ("Chọn giá trị ở một ô lọc", "Change",
     "During:\n– Kỳ chuyển khỏi Tuỳ chỉnh → xoá khoảng ngày đã chọn.\n"
     "After:\n– Tải lại báo cáo theo bộ lọc mới, bảng về trang 1.\n"
     "– Lỗi khi tải → hiển thị “Lỗi khi tải dữ liệu”."),
    ("Bấm Xóa lọc", "Click", "After:\n– Đưa mọi ô lọc về trống, tải lại trang 1."),
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
d.h3("2.4 Mở hết / thu gọn nhóm")
d.p("2.4.1 Giới thiệu")
d.rule_ref("- Màn Danh sách. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi tiết."
           % TEN_MAN, anchor="list")
d.intro_table(
    ten="Mở hết / thu gọn nhóm",
    mota="Thu gọn toàn bộ bảng về các dòng Thị trường để nhìn tổng quan, hoặc mở lại tất cả.",
    tacnhan=TAC_NHAN,
    dieukien="Bảng đang có dữ liệu.",
    chinh="1. Người dùng bấm nút “Thu gọn” ở tiêu đề cột Tên meeting.\n"
          "2. Hệ thống thu gọn mọi nhóm Thị trường, chỉ còn các dòng thị trường.\n"
          "3. Nhãn nút đổi thành “Mở hết”; bấm lần nữa để mở lại toàn bộ.",
    phu="• Còn bất kỳ nhóm nào đang thu gọn (kể cả thu gọn tay từng nhóm) → nút hiện “Mở hết”.\n"
        "• Đổi trang hoặc đổi bộ lọc → mọi nhóm của dữ liệu mới đều mở lại.")

d.p("2.4.2 Layout màn hình")
d.layout(menu=MENU + " => Thu gọn", shot=shot("04-thu-gon-nhom.png"),
         shot_caption="Bảng sau khi bấm Thu gọn — chỉ còn dòng thị trường")

d.p("2.4.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Nút Mở hết / Thu gọn", "Button", "Enable", "–", "–", "Thu gọn",
     "Nằm trong tiêu đề cột Tên meeting. Rê chuột: “Thu gọn toàn bộ nhóm” / “Mở toàn bộ nhóm”."),
    ("Mũi tên ở dòng nhóm", "Icon Button", "Enable", "–", "–", "Đang mở",
     "Hướng mũi tên cho biết nhóm đang mở hay thu gọn. Rê chuột: “Mở nhóm” / “Thu gọn nhóm”."),
])

d.p("2.4.4 Danh sách event và xử lý event")
d.event_table([
    ("Bấm Thu gọn", "Click", "After:\n– Thu gọn mọi nhóm Thị trường; nhãn nút đổi thành “Mở hết”."),
    ("Bấm Mở hết", "Click", "After:\n– Mở lại mọi nhóm Thị trường và Khách hàng."),
])

# --------------------------------------------------------------- 2.5 FR-05
d.h3("2.5 Xuất Excel")
d.p("2.5.1 Biểu đồ Usecase")
d.uc_figure("FR-05", "Xuất Excel", "io",
            [("include", "Lấy bộ lọc đang áp dụng"),
             ("include", "Tải file về máy")],
            actor=ACTOR_QL, caption="Biểu đồ Use Case — FR-05 Xuất Excel")

d.p("2.5.2 Giới thiệu")
d.rule_ref("- Quy tắc Excel. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi tiết."
           % TEN_MAN, anchor="excel")
d.intro_table(
    ten="Xuất Excel",
    mota="Tải file Excel toàn bộ meeting khớp bộ lọc, mỗi meeting một dòng.",
    tacnhan=TAC_NHAN,
    dieukien="Người dùng đang ở màn báo cáo.",
    chinh="1. Người dùng bấm “Xuất Excel”.\n"
          "2. Hệ thống lấy đúng bộ lọc đang áp dụng, bỏ phân trang.\n"
          "3. Trình duyệt tải file “bao-cao-ket-qua-meeting-theo-thi-truong.xlsx”.",
    phu="• Lỗi khi xuất → hiển thị thông báo “Lỗi khi xuất Excel”.",
    dacbiet="File có đủ mọi meeting khớp bộ lọc (không chỉ trang đang xem), sắp theo cùng thứ tự "
            "nhóm của bảng. File là danh sách phẳng 15 cột: Thị trường, Khách hàng, Mã KH, Tên "
            "meeting, Loại meeting, Thời gian, Địa điểm, Người chủ trì, Thành phần công ty, "
            "Thành phần bên KH, Trạng thái, Biên bản/Lý do huỷ, Dự án TKT, Phiếu công tác, "
            "Chấm công. Cột Phòng chủ trì của màn hình KHÔNG có trong file.")

d.p("2.5.3 Layout màn hình")
d.layout(menu=MENU + " => Xuất Excel", shot=shot("01-man-chinh.png"),
         shot_caption="Nút Xuất Excel ở góc phải thanh bộ lọc")

d.p("2.5.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Nút Xuất Excel", "Button", "Enable", "–", "–", "Hiển thị", "Tải file .xlsx về máy."),
    ("Cột Biên bản/Lý do huỷ (trong file)", "Text", "Read-only", "–", "–", "Theo dữ liệu",
     "Hoàn thành có biên bản: “Có biên bản”; Hủy: lý do huỷ; còn lại để trống."),
    ("Cột Chấm công (trong file)", "Text", "Read-only", "–", "–", "Theo dữ liệu",
     "“Có” khi ít nhất 1 phiếu công tác của meeting đã có chấm công; còn lại để trống."),
    ("Thông báo lỗi", "Toast / Alert", "Hiển thị", "–", "–", "Ẩn", "“Lỗi khi xuất Excel”."),
])

d.p("2.5.5 Danh sách event và xử lý event")
d.event_table([
    ("Bấm Xuất Excel", "Click",
     "During:\n– Lấy bộ lọc đang áp dụng, bỏ các ô trống và bỏ phân trang.\n"
     "After:\n– Tải file “bao-cao-ket-qua-meeting-theo-thi-truong.xlsx”.\n"
     "– Lỗi → hiển thị “Lỗi khi xuất Excel”."),
])

# --------------------------------------------------------------- 2.6 FR-06
d.h3("2.6 Xem thành phần tham dự")
d.p("2.6.1 Giới thiệu")
d.rule_ref("- Màn Xem chi tiết. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi tiết."
           % TEN_MAN, anchor="detail")
d.intro_table(
    ten="Xem thành phần tham dự",
    mota="Xem đầy đủ danh sách người tham dự phía công ty hoặc phía khách hàng của 1 meeting.",
    tacnhan=TAC_NHAN,
    dieukien="Meeting có từ 2 người trở lên ở phía tương ứng (ô hiện chip “+N”).",
    chinh="1. Người dùng bấm chip “+N” ở cột Thành phần công ty hoặc Thành phần bên KH.\n"
          "2. Hệ thống mở popup liệt kê toàn bộ người tham dự của phía đó.",
    phu="• Bấm × → đóng popup.")

d.p("2.6.2 Layout màn hình")
d.layout(menu=MENU + " => Bấm chip “+N”", modal="Thành phần tham dự",
         shot=shot("05-popup-thanh-phan.png"), shot_caption="Popup Thành phần công ty")

d.p("2.6.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Tiêu đề popup", "Label", "Hiển thị", "–", "Theo phía",
     "“Thành phần công ty” hoặc “Thành phần bên khách hàng”, dòng phụ là tên meeting."),
    ("Dòng “N người tham dự”", "Label", "Read-only", "≥ 1", "Theo dữ liệu", "–"),
    ("Danh sách người", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "Mỗi dòng: số thứ tự, ảnh đại diện chữ viết tắt, họ tên, chức vụ (nếu có)."),
    ("Nút ×", "Icon Button", "Enable", "–", "Hiển thị", "Đóng popup."),
], required=False)

d.p("2.6.4 Danh sách event và xử lý event")
d.event_table([
    ("Bấm chip “+N”", "Click",
     "After:\n– Mở popup với danh sách đã có sẵn trên bảng (không tải lại dữ liệu)."),
    ("Bấm ×", "Click", "After:\n– Đóng popup."),
])

# --------------------------------------------------------------- 2.7 FR-07
d.h3("2.7 Xem lịch sử chấm công GPS")
d.p("2.7.1 Giới thiệu")
d.rule_ref("- Màn Xem chi tiết. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi tiết."
           % TEN_MAN, anchor="detail")
d.intro_table(
    ten="Xem lịch sử chấm công GPS",
    mota="Xem các lần chấm công GPS của nhân viên trên những phiếu công tác lập từ meeting, để "
         "đối chiếu nhân viên có thực sự có mặt tại địa điểm họp.",
    tacnhan=TAC_NHAN,
    dieukien="Meeting có phiếu công tác và ít nhất 1 lần chấm công (ô hiện nút "
             "“Xem lịch sử chấm công”).",
    chinh="1. Người dùng bấm “Xem lịch sử chấm công”.\n"
          "2. Hệ thống tải các lần chấm công của mọi phiếu công tác lập từ meeting.\n"
          "3. Popup hiển thị theo từng nhân viên: thời gian, nhãn vào/ra, địa chỉ, toạ độ GPS.",
    phu="• Không có lần chấm công nào → “Chưa có lịch sử chấm công”.\n"
        "• Meeting nằm ngoài phạm vi quyền → popup trống như không có chấm công.\n"
        "• Lỗi khi tải → hiển thị “Lỗi khi tải lịch sử chấm công”.")

d.p("2.7.2 Layout màn hình")
d.layout(menu=MENU + " => Xem lịch sử chấm công", modal="Lịch sử chấm công GPS",
         shot=shot("06-popup-cham-cong.png"), shot_caption="Popup Lịch sử chấm công GPS")

d.p("2.7.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Tiêu đề “Lịch sử chấm công GPS”", "Label", "Hiển thị", "–", "–",
     "Dòng phụ là mã + tên meeting."),
    ("Tên nhân viên", "Label", "Read-only", "–", "Theo dữ liệu", "Mỗi nhân viên 1 khối."),
    ("Cột Thời gian", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "Nhãn (Vào (suy đoán) / Ra (suy đoán) / Chấm công giữa / Chấm công (chưa rõ vào/ra)) + giờ "
     "và ngày chấm công."),
    ("Cột Vị trí chấm công (GPS)", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "Địa chỉ + toạ độ “GPS: vĩ độ, kinh độ” + liên kết “Xem bản đồ” (mở tab mới)."),
    ("Trạng thái rỗng", "Label", "Hiển thị", "–", "Ẩn", "“Chưa có lịch sử chấm công”."),
    ("Đang tải", "Loading", "Hiển thị", "–", "Ẩn", "“Đang tải lịch sử chấm công...”."),
    ("Nút Đóng", "Button", "Enable", "–", "Hiển thị", "Đóng popup."),
], required=False)

d.p("2.7.4 Danh sách event và xử lý event")
d.event_table([
    ("Bấm Xem lịch sử chấm công", "Click",
     "Before:\n– Kiểm tra meeting nằm trong phạm vi quyền xem của người dùng.\n"
     "During:\n– Lấy chấm công GPS của mọi phiếu công tác lập từ meeting, nhóm theo nhân viên rồi "
     "theo ngày.\n"
     "After:\n– Hiển thị popup.\n– Lỗi → hiển thị “Lỗi khi tải lịch sử chấm công”."),
    ("Bấm Xem bản đồ", "Click", "After:\n– Mở bản đồ tại toạ độ chấm công trong tab mới."),
])

# --------------------------------------------------------------- 2.8 FR-08
d.h3("2.8 Xem chi tiết meeting")
d.p("2.8.1 Giới thiệu")
d.rule_ref("- Màn Xem chi tiết và Phân quyền. Panel dùng chung với màn Lịch của tôi; chỉ bổ "
           "sung các quy tắc riêng của %s tại phần mô tả chi tiết." % TEN_MAN, anchor="detail")
d.intro_table(
    ten="Xem chi tiết meeting",
    mota="Xem nhanh thông tin đầy đủ của 1 meeting ngay trên màn báo cáo, không rời trang.",
    tacnhan=TAC_NHAN,
    dieukien="Người dùng bấm tên meeting trên bảng.",
    chinh="1. Người dùng bấm tên meeting.\n"
          "2. Hệ thống mở panel chi tiết từ bên phải màn hình.\n"
          "3. Panel hiển thị thông tin cuộc họp, khách hàng & người liên hệ, thành phần tham dự, "
          "kết luận & ghi chú, thông tin khác.",
    phu="• Meeting có biên bản → chân panel có nút “Xem biên bản” (FR-09).\n"
        "• Người dùng có quyền sửa meeting → chân panel có nút “Sửa”, bấm mở màn sửa meeting "
        "trong tab mới.\n"
        "• Bấm × → đóng panel, màn báo cáo giữ nguyên.")

d.p("2.8.2 Layout màn hình")
d.layout(menu=MENU + " => Bấm tên meeting", modal="Panel chi tiết meeting",
         shot=shot("07-panel-chi-tiet.png"), shot_caption="Panel chi tiết meeting")

d.p("2.8.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Đầu panel", "Label", "Hiển thị", "–", "Theo dữ liệu",
     "Tên meeting, nhãn “Meeting”, trạng thái, mã meeting, ngày và khung giờ họp."),
    ("Khối Thông tin cuộc họp", "Text", "Read-only", "–", "Theo dữ liệu",
     "Loại meeting, Hình thức, Địa điểm."),
    ("Khối Khách hàng & người liên hệ", "Text", "Read-only", "–", "Theo dữ liệu",
     "Khách hàng, Người liên hệ."),
    ("Khối Thành phần tham dự", "Text", "Read-only", "–", "Theo dữ liệu",
     "Thành phần công ty, Thành phần khách hàng (dạng chip)."),
    ("Khối Kết luận & ghi chú", "Text", "Read-only", "–", "Theo dữ liệu", "Kết luận / Biên bản."),
    ("Khối Thông tin khác", "Text", "Read-only", "–", "Theo dữ liệu", "Người tạo."),
    ("Nút Xem biên bản", "Button", "Enable / Ẩn", "–", "Ẩn khi chưa có biên bản", "Xem FR-09."),
    ("Nút Sửa", "Button", "Enable / Ẩn", "–", "Ẩn khi thiếu quyền",
     "Chỉ hiện khi người dùng có quyền sửa meeting đó."),
    ("Nút ×", "Icon Button", "Enable", "–", "Hiển thị", "Đóng panel."),
], required=False)

d.p("2.8.4 Danh sách event và xử lý event")
d.event_table([
    ("Bấm tên meeting", "Click", "After:\n– Mở panel, tải chi tiết meeting."),
    ("Bấm Sửa", "Click",
     "Before:\n– Nút chỉ hiện khi hệ thống xác nhận người dùng có quyền sửa meeting.\n"
     "After:\n– Mở màn sửa meeting trong tab mới."),
    ("Bấm ×", "Click", "After:\n– Đóng panel."),
])

# --------------------------------------------------------------- 2.9 FR-09
d.h3("2.9 Xem biên bản cuộc họp")
d.p("2.9.1 Biểu đồ Usecase")
d.uc_figure("FR-09", "Xem biên bản cuộc họp", "io",
            [("include", "Dựng bản in biên bản"),
             ("extend", "In biên bản")],
            actor=ACTOR_QL, caption="Biểu đồ Use Case — FR-09 Xem biên bản cuộc họp")

d.p("2.9.2 Giới thiệu")
d.rule_ref("- Quy tắc Excel và In ấn. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi "
           "tiết." % TEN_MAN, anchor="excel")
d.intro_table(
    ten="Xem biên bản cuộc họp",
    mota="Xem trước bản in biên bản của meeting đã hoàn thành và in nếu cần.",
    tacnhan=TAC_NHAN,
    dieukien="Meeting ở trạng thái Hoàn thành và đã có biên bản.",
    chinh="1. Người dùng bấm “Xem biên bản” (trên bảng hoặc trên panel chi tiết).\n"
          "2. Hệ thống dựng bản in biên bản theo mẫu in của hệ thống.\n"
          "3. Hệ thống mở popup “Xem biên bản cuộc họp”.\n"
          "4. Người dùng bấm “In” để in.",
    phu="• Lỗi khi dựng bản in → popup hiển thị thông báo lỗi.\n"
        "• Bấm × → đóng popup.",
    dacbiet="Bản in gồm: số và ngày lập biên bản; thông tin cuộc họp; thời gian; thành phần tham "
            "gia phía công ty và phía khách hàng (kèm trạng thái tham dự, ô chữ ký); nội dung "
            "meeting (khảo sát nhu cầu, các nội dung khác với phương án xử lý, người đề xuất, "
            "người thực hiện, hạn dự kiến).")

d.p("2.9.3 Layout màn hình")
d.layout(menu=MENU + " => Xem biên bản", modal="Xem biên bản cuộc họp",
         shot=shot("09-xem-bien-ban.png"), shot_caption="Popup Xem biên bản cuộc họp")

d.p("2.9.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Tiêu đề “Xem biên bản cuộc họp”", "Label", "Hiển thị", "–", "–", "Hiển thị", "–"),
    ("Nút In", "Button", "Enable", "–", "–", "Hiển thị", "Mở hộp thoại in của trình duyệt."),
    ("Khung xem trước", "Modal", "Read-only", "–", "–", "Theo dữ liệu", "Bản in khổ dọc."),
    ("Nút ×", "Icon Button", "Enable", "–", "–", "Hiển thị", "Đóng popup."),
])

d.p("2.9.5 Danh sách event và xử lý event")
d.event_table([
    ("Bấm Xem biên bản", "Click",
     "After:\n– Mở popup xem trước biên bản.\n– Lỗi → hiển thị thông báo lỗi trong popup."),
    ("Bấm In", "Click", "After:\n– Mở hộp thoại in của trình duyệt với nội dung biên bản."),
])

# --------------------------------------------------------------- 2.10 FR-10
d.h3("2.10 Mở dự án TKT")
d.p("2.10.1 Giới thiệu")
d.rule_ref("- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của %s tại phần "
           "mô tả chi tiết." % TEN_MAN, anchor="detail")
d.intro_table(
    ten="Mở dự án TKT gắn với meeting",
    mota="Chuyển sang màn chi tiết dự án tiền khả thi từ mã dự án trên bảng.",
    tacnhan=TAC_NHAN,
    dieukien="Meeting có gắn ít nhất 1 dự án TKT.",
    chinh="1. Người dùng bấm mã dự án ở cột Dự án TKT.\n"
          "2. Hệ thống chuyển sang màn chi tiết dự án TKT đó.",
    phu="• Người dùng không có quyền xem dự án → màn chi tiết dự án xử lý theo quy tắc phân quyền "
        "của chính màn đó.")

d.p("2.10.2 Layout màn hình")
d.layout(menu=MENU + " => Bấm mã Dự án TKT", shot=shot("08-cot-ket-qua.png"),
         shot_caption="Cột Dự án TKT với các mã dự án bấm được")

d.p("2.10.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Mã dự án TKT", "Button", "Enable", "–", "Theo dữ liệu",
     "Mỗi dự án 1 chip mã; meeting không gắn dự án hiển thị “—”."),
], required=False)

d.p("2.10.4 Danh sách event và xử lý event")
d.event_table([
    ("Bấm mã dự án", "Click", "After:\n– Chuyển sang màn chi tiết dự án TKT ngay trên tab hiện tại."),
])

# ==================================================== PHẦN 4. QUY TẮC NGHIỆP VỤ
d.h1("Phần 4. Quy tắc nghiệp vụ")
d.rule_ref(". Phần này chỉ ghi các quy tắc đặc thù của %s; không lặp lại các quy tắc đã có "
           "trong SRS quy tắc chung." % TEN_MAN,
           anchor="list", head="Quy tắc áp dụng",
           lead="Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ")

d.rule_table([
    ("BR-01", "Tập meeting của báo cáo", [
        "– Chỉ lấy meeting CÓ gắn khách hàng, ở 4 trạng thái Lên lịch, Chốt lịch, Hoàn thành, Hủy.",
        "– Kỳ báo cáo xét theo NGÀY BẮT ĐẦU của meeting.",
    ], "Toàn màn hình"),
    ("BR-02", "Kỳ báo cáo mặc định là Tất cả", [
        "– Khi mở màn, Kỳ báo cáo để trống: không giới hạn thời gian.",
        "– Tuần tính từ thứ Hai. Tuỳ chỉnh chỉ chọn 1 mốc thì lọc 1 chiều; bỏ trống cả 2 mốc thì "
        "không giới hạn.",
    ], "Bộ lọc Kỳ báo cáo"),
    ("BR-03", "Thị trường của meeting", [
        "– Thị trường là tỉnh/thành phố hiện tại của khách hàng.",
        "– Khách hàng chưa có tỉnh/thành phố → nhóm “Chưa xác định thị trường”, luôn đứng cuối.",
    ], ["Bảng", "Khối Theo thị trường", "Bộ lọc Thị trường"]),
    ("BR-04", "Thứ tự hiển thị", [
        "– Thị trường A→Z (“Chưa xác định thị trường” cuối) → Khách hàng A→Z → Ngày bắt đầu meeting "
        "tăng dần.",
        "– Phân trang cắt theo meeting sau khi đã sắp; nhóm thị trường / khách hàng dựng lại trên "
        "từng trang nên số đếm trên dòng nhóm là số của trang đang xem.",
    ], ["Bảng", "Excel"]),
    ("BR-05", "Dải tổng hợp tính trên toàn bộ tập", [
        "– Số meeting, các khối theo trạng thái / phòng chủ trì / thị trường tính trên TOÀN BỘ "
        "meeting khớp bộ lọc, không theo trang.",
        "– Dự án: số dự án TKT khác nhau gắn với các meeting.",
        "– Tỷ lệ hoàn thành = meeting Hoàn thành ÷ tổng meeting, 1 chữ số thập phân.",
    ], "Dải tổng hợp"),
    ("BR-06", "KH mới", [
        "– Đếm khách hàng KHÁC NHAU có meeting trong tập và có NGÀY TẠO khách hàng nằm trong kỳ.",
        "– Kỳ = Tất cả (hoặc Tuỳ chỉnh bỏ trống cả 2 mốc) → không xét ngày tạo, KH mới bằng tổng "
        "số khách hàng khác nhau có meeting trong tập.",
        "– Khách hàng mới tạo nhưng chưa có meeting nào KHÔNG được đếm.",
    ], "Khối Tổng hợp"),
    ("BR-07", "Người chủ trì và phòng chủ trì", [
        "– Người chủ trì lấy theo người chủ trì của meeting; meeting không ghi người chủ trì thì lấy "
        "người tạo meeting.",
        "– Phòng chủ trì lấy theo phòng ban trong hồ sơ của người chủ trì; không xác định được thì "
        "ghi “—” và xếp cuối khối Theo phòng chủ trì.",
    ], ["Cột Người chủ trì", "Cột Phòng chủ trì", "Khối Theo phòng chủ trì"]),
    ("BR-08", "Bộ lọc tổ chức theo meeting", [
        "– Công ty, Phòng ban, Bộ phận lọc theo thông tin ghi trên meeting (đơn vị của người tạo "
        "meeting), KHÔNG theo phòng của người chủ trì.",
        "– Nhân viên: lấy meeting do nhân viên đó tạo hoặc nhân viên đó là thành viên tham dự.",
    ], "Bộ lọc"),
    ("BR-09", "Phạm vi dữ liệu theo quyền", [
        "– Xét theo thứ tự V1 → V2 → V3 → không có quyền (xem Phần 2).",
        "– Với V2, V3: meeting do chính người dùng tạo luôn nằm trong phạm vi.",
        "– Không có quyền nào: meeting do mình tạo hoặc mình là thành viên tham dự.",
        "– File Excel và Lịch sử chấm công dùng đúng phạm vi của màn hình.",
    ], "Toàn màn hình"),
    ("BR-10", "Biên bản và lý do huỷ", [
        "– Nút “Xem biên bản” chỉ hiện với meeting Hoàn thành và đã có biên bản.",
        "– Meeting Hủy hiển thị lý do huỷ thay cho biên bản.",
    ], ["Cột Biên bản họp / Lý do huỷ", "Excel"]),
    ("BR-11", "Phiếu công tác và chấm công", [
        "– Chỉ tính phiếu công tác được lập TỪ meeting; phiếu công tác lập trước khi hệ thống ghi "
        "nhận liên kết với meeting không hiển thị.",
        "– Nhãn vào/ra là SUY ĐOÁN theo thứ tự thời gian trong từng ngày: lần đầu là Vào, lần cuối "
        "là Ra, ở giữa là Chấm công giữa; ngày chỉ có 1 lần là “Chấm công (chưa rõ vào/ra)”.",
    ], ["Cột Phiếu công tác", "FR-07"]),
    ("BR-12", "Excel xuất đủ dữ liệu", [
        "– File Excel luôn có đủ mọi meeting khớp bộ lọc, không phụ thuộc trang đang xem và trạng "
        "thái mở / thu gọn nhóm.",
        "– File là danh sách phẳng (mỗi meeting 1 dòng, có cột Thị trường / Khách hàng / Mã KH), "
        "không có cột Phòng chủ trì.",
    ], "FR-05"),
])

d.save()
