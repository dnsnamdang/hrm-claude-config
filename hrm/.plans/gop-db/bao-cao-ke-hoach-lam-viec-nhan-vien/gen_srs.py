# -*- coding: utf-8 -*-
"""Sinh "SRS - Báo cáo kế hoạch & kết quả làm việc theo nhân viên.docx" theo FORM CHUẨN hiện hành
(bản mẫu `.claude/skills/srs-documenter/assets/SRS_MAU.docx`; bản mẫu màn báo cáo
`.plans/gop-db/bao-cao-tong-hop-cskh-tiem-nang/gen_srs.py` — CHỈ chép cấu trúc 2.1.6, 2.1.7, popup; bảng giao
diện viết theo 7 quy tắc "Viết bảng giao diện cho người đọc" của skill).

Chạy:  python3 .plans/gop-db/bao-cao-ke-hoach-lam-viec-nhan-vien/gen_srs.py

Nguồn nội dung: code nhánh `gop_db-update-style-ewp` (hrm-api Modules/Assign/Services/Report/EmployeeWorkPerformance*,
EmployeeWorkPerformancePrintService, Controller + routes; hrm-client pages/assign/report/employee-work-performance/**),
plan.md cùng thư mục. Nội dung icon ⓘ chép NGUYÊN VĂN từ code FE (InfoTip / title-suffix); số trong ⓘ đổi theo dữ
liệu thì ghi <…>.
Ảnh chụp thật + icon menu ở `ewp_shots/` (1440×900; script chụp: e2e/tests/assign/_tmp-ewp-srs-shots.spec.ts — file
tạm, đã xoá; cấp quyền 1612 qua role tạm, kỳ "Năm nay"; bản in chụp với ERP_URL khai tạm để letterhead tải được).
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

import srs_uml_render as uml  # noqa: E402

if not os.path.exists(uml.F_REG):
    _MAC = "/System/Library/Fonts/Supplemental"
    for _attr, _name in (("F_REG", "Arial.ttf"), ("F_BOLD", "Arial Bold.ttf"), ("F_ITAL", "Arial Italic.ttf")):
        _path = os.path.join(_MAC, _name)
        if os.path.exists(_path):
            setattr(uml, _attr, _path)

from srs_docx_lib import SrsDoc  # noqa: E402

SCREEN = "Báo cáo kế hoạch & kết quả làm việc theo nhân viên"
OUT = os.path.join(HERE, "SRS - %s.docx" % SCREEN)
SHOTS = os.path.join(HERE, "ewp_shots")
MAN = "Báo cáo kế hoạch & kết quả làm việc theo nhân viên"
MENU = "Phân hệ CSKH trước bán => Báo cáo => Báo cáo thị trường => %s" % MAN
MENU_CV = "Phân hệ Công việc => Báo cáo => %s" % MAN

ACT = "Quản lý (Ban giám đốc / Trưởng phòng / Trưởng bộ phận)"
TACNHAN = "%s; Người dùng đã đăng nhập có ít nhất 1 trong 3 quyền V1–V3" % ACT


def shot(name):
    return os.path.join(SHOTS, name)


ICONS_PRESALE = {
    "Phân hệ CSKH trước bán": shot("icon_phanhe.png"), "Báo cáo": shot("icon_baocao.png"),
    "Báo cáo thị trường": shot("icon_nhom.png"), MAN: shot("icon_man.png"),
    "Cài đặt bộ lọc": shot("icon_caidat.png"), "In danh sách": shot("icon_in.png"), "Xuất Excel": shot("icon_xuat.png"),
}
ICONS_CV = {
    "Phân hệ Công việc": shot("icon_phanhe_cv.png"), "Báo cáo": shot("icon_baocao_cv.png"), MAN: shot("icon_man_cv.png"),
}

d = SrsDoc(out=OUT, menu=MENU, route="/assign/report/employee-work-performance",
           full_url="https://<host-hrm>/assign/report/employee-work-performance", img_prefix="ewp_")
d.set_menu_icons(ICONS_PRESALE)

# ================================================================= TRANG ĐẦU
d.title_block(SCREEN)
d.h2("Mục lục")
d.toc()

# ================================================================= PHẦN 1
d.h1("Phần 1. Giới thiệu")

d.h2("1 Mục đích")
d.p("Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Báo cáo kế hoạch & kết quả làm việc theo nhân viên (có ở "
    "phân hệ CSKH trước bán và phân hệ Công việc), nhằm:")
d.bullets([
    "Thống nhất yêu cầu giữa nghiệp vụ, phân tích, phát triển và kiểm thử cho báo cáo cho biết, TRONG MỘT KỲ, mỗi "
    "phòng ban, bộ phận, nhân viên có bao nhiêu đầu việc (Meeting, Task, Issue, Phiếu công tác, Phiếu giao việc), "
    "đã hoàn thành bao nhiêu, bao nhiêu đang quá hạn, tỷ lệ hoàn thành ra sao.",
    "Là căn cứ nghiệm thu chức năng, phạm vi dữ liệu theo 3 cấp quyền (công ty / phòng ban / bộ phận) và cách tính "
    "từng con số.",
    "Mô tả rõ cách lấy dữ liệu của từng chỉ tiêu, từng cột số liệu và nội dung icon ⓘ trên giao diện (mục 2.1.6, "
    "2.5.7, 2.6.7) để người dùng và người kiểm thử đối chiếu được số liệu.",
    "Đặc tả mọi popup mở ra khi bấm vào số liệu: bấm ở đâu ra popup nào (mục 2.1.7), mục đích thiết kế và các biến "
    "thể của popup danh sách đầu việc (mục 2.5) và panel chi tiết đầu việc (mục 2.6).",
])

d.h2("2 Thuật ngữ và viết tắt")
d.table(["Thuật ngữ", "Mô tả"], [
    ("Đầu việc", "Một chứng từ công việc thuộc 1 trong 5 loại: Meeting, Task, Issue, Phiếu công tác, Phiếu giao việc."),
    ("Người thực hiện", "Người có tên trong danh sách thực hiện của đầu việc: Meeting = chủ trì + thành phần dự họp; "
     "Task / Issue = người được giao; Phiếu công tác = mọi nhân viên trong đoàn; Phiếu giao việc = mọi nhân viên thực "
     "hiện. Ai có tên đều được tính như nhau (chỉ Meeting mới có người chủ trì)."),
    ("Lượt tham gia", "Một cặp (đầu việc × người thực hiện). 1 cuộc họp 3 người dự = 1 đầu việc, 3 lượt tham gia."),
    ("Đếm theo phiếu", "Dòng Phòng ban / Bộ phận / TỔNG và khối tổng hợp đếm số ĐẦU VIỆC khác nhau (1 phiếu nhiều "
     "người vẫn là 1). Dòng Nhân viên đếm số đầu việc của người đó (mỗi người +1)."),
    ("Kỳ báo cáo", "Khoảng thời gian xem. Đầu việc thuộc kỳ khi khoảng thời gian của nó GIAO NHAU với kỳ (cách lấy "
     "mốc thời gian theo từng loại ở mục 2.1.6)."),
    ("Nhóm trạng thái", "4 nhóm theo dõi chia hết tổng: Đã hoàn thành · Đang thực hiện · Quá hạn · Dừng / Huỷ / Từ "
     "chối. Khác với “Trạng thái chứng từ” là trạng thái gốc của từng phiếu."),
    ("Nhóm cấp 1", "Dòng Phòng ban — đơn vị phân trang của bảng."),
    ("P. công tác / P. giao việc", "Phiếu công tác (phiếu giao công tác) / Phiếu giao việc tại công ty."),
    ("ⓘ", "Icon thông tin; rê chuột để xem giải thích."),
], widths=[1.8, 4.2])

# ================================================================= PHẦN 2
d.h1("Phần 2. Phân quyền")

d.h2("1 Danh sách quyền")
d.p("Nhóm quyền thao tác:")
d.table(["Ký hiệu", "Tên quyền", "Tác dụng trên màn hình"], [
    ("—", "(không có quyền thao tác riêng)",
     "Màn hình chỉ đọc. Có ít nhất 1 trong 3 quyền V1–V3 là mở được báo cáo và dùng được mọi chức năng (lọc, xem danh "
     "sách chi tiết, xem chi tiết đầu việc, in, xuất Excel). Không có quyền nào thì menu không hiện và không vào được "
     "màn (không có mức “chỉ xem việc của mình”)."),
], widths=[0.8, 2.0, 3.2])

d.p("Nhóm quyền quyết định phạm vi dữ liệu:")
d.table(["Ký hiệu", "Tên quyền", "Phạm vi dữ liệu"], [
    ("V1", "Xem báo cáo kế hoạch & kết quả làm việc theo công ty",
     "Mọi nhân viên có hồ sơ thuộc công ty đang làm việc."),
    ("V2", "Xem báo cáo kế hoạch & kết quả làm việc theo phòng ban",
     "Nhân viên thuộc các phòng ban mình được phân công quản lý (trong công ty đang làm việc)."),
    ("V3", "Xem báo cáo kế hoạch & kết quả làm việc theo bộ phận",
     "Nhân viên thuộc các bộ phận mình được phân công quản lý (trong công ty đang làm việc)."),
], widths=[0.8, 2.2, 3.0])
d.p("Ràng buộc bổ sung: có nhiều quyền thì cấp cao nhất thắng (V1 > V2 > V3). Báo cáo không có cấp tổng công ty: ô "
    "Công ty luôn khoá ở công ty đang làm việc, xem công ty khác bị chặn. Không có ngoại lệ cho tài khoản quản trị — "
    "kể cả Super admin cũng chỉ xét theo quyền được gán. Phạm vi áp lên NGƯỜI THỰC HIỆN: một đầu việc hiện trong báo "
    "cáo khi có ít nhất 1 người thực hiện nằm trong phạm vi; bản in, Excel, popup, panel chi tiết cùng phạm vi.")

d.h2("2 Ma trận phân quyền")
d.table(["Chức năng", "V1", "V2", "V3", "Không có quyền nào"], [
    ("FR-01 Xem báo cáo", "✅ (cả công ty)", "✅ (phòng được quản lý)", "✅ (bộ phận được quản lý)", "❌"),
    ("FR-02 Tìm kiếm và lọc báo cáo", "✅ (Công ty khoá)", "✅ (Công ty khoá)", "✅ (Công ty khoá)", "❌"),
    ("FR-03 Cài đặt bộ lọc", "✅", "✅", "✅", "❌"),
    ("FR-04 Chọn cấp xem và bung / thu gọn dòng", "✅", "✅", "✅", "❌"),
    ("FR-05 Xem danh sách đầu việc chi tiết", "✅", "✅", "✅", "❌"),
    ("FR-06 Xem chi tiết đầu việc", "✅", "✅", "✅", "❌"),
    ("FR-07 In danh sách", "✅", "✅", "✅", "❌"),
    ("FR-08 Xuất Excel", "✅", "✅", "✅", "❌"),
], widths=[2.2, 0.9, 1.0, 1.0, 0.9])

# ================================================================= PHẦN 3
d.h1("Phần 3. Đặc tả chi tiết theo từng chức năng")

d.h2("1 Sơ đồ UML tổng quan")
d.overview_figure2(
    [(ACT, [0, 1, 2])],
    [("FR-01", "Xem báo cáo kế hoạch & kết quả làm việc", "view"),
     ("FR-07", "In danh sách", "io"),
     ("FR-08", "Xuất Excel", "io")],
    [("FR-02", "Tìm kiếm và lọc báo cáo", "view", "extend", [0], None),
     ("FR-03", "Cài đặt bộ lọc", "view", "extend", [0], None),
     ("FR-04", "Chọn cấp xem và bung / thu gọn dòng", "view", "extend", [0], None),
     ("FR-05", "Xem danh sách đầu việc chi tiết (popup)", "view", "extend", [0], None),
     ("FR-06", "Xem chi tiết đầu việc (panel)", "view", "extend", [0], None)],
    "Sơ đồ Use Case tổng quan màn Báo cáo kế hoạch & kết quả làm việc theo nhân viên")

d.h2("2 Đặc tả chi tiết từng chức năng")

# ----------------------------------------------------------------- 2.1
d.h3("2.1 Xem báo cáo kế hoạch & kết quả làm việc theo nhân viên")
d.p("2.1.1 Giới thiệu")
d.rule_ref("- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của Báo "
           "cáo kế hoạch & kết quả làm việc theo nhân viên tại phần mô tả chi tiết.", anchor="list")
d.intro_table(
    ten="Xem báo cáo kế hoạch & kết quả làm việc theo nhân viên",
    mota="Hiển thị khối lượng và kết quả làm việc trong kỳ của các nhân viên trong phạm vi quyền: dòng tóm tắt, hai "
         "khối tổng hợp (Khối lượng trong kỳ, Trạng thái xử lý) và bảng chi tiết báo cáo Phòng ban ▸ Bộ phận ▸ Nhân "
         "viên, phân trang theo phòng ban. Mọi con số đếm đầu việc khác 0 bấm được để mở danh sách chi tiết.",
    tacnhan=TACNHAN,
    dieukien="Người dùng đã đăng nhập và có ít nhất 1 trong 3 quyền V1, V2, V3.",
    chinh="1. Người dùng mở báo cáo từ menu (2 lối vào — mục 2.1.2).\n"
          "2. Hệ thống xác định phạm vi theo quyền cao nhất người dùng có (V1 → V2 → V3), công ty = công ty đang làm việc.\n"
          "3. Hệ thống gom đầu việc của 5 loại có thời gian giao nhau với kỳ mặc định “Tháng này”, của các nhân viên "
          "trong phạm vi.\n"
          "4. Hệ thống tính dòng tóm tắt, hai khối tổng hợp và dòng TỔNG trên toàn bộ dữ liệu đã lọc; dựng bảng cho "
          "trang 1 (20 phòng ban / trang), cấp xem mặc định “Đến Bộ phận”.\n"
          "5. Màn hình hiển thị kết quả mà không cần bấm Tìm kiếm.",
    phu="• Không có đầu việc nào → bảng hiện “Không có đầu việc nào khớp bộ lọc.”, các số = 0.\n"
        "• Nhóm trạng thái có 0 đầu việc → không hiện ô của nhóm đó ở khối Trạng thái xử lý.\n"
        "• Bỏ tích “Chỉ hiện nhân viên có việc” (dòng tiêu đề khối tổng hợp) → bảng hiện cả nhân viên không có đầu "
        "việc nào (dòng toàn số 0).\n"
        "• Nhân viên chưa gán phòng ban → nhóm “Chưa phân phòng ban” (chữ nghiêng). Phòng ban không chia bộ phận / "
        "nhân viên chưa gán bộ phận → dòng nhân viên nằm thẳng dưới phòng ban.\n"
        "• Bảng rộng hơn khung → thanh cuộn ngang ở cả trên và dưới bảng; tiêu đề cột dính khi cuộn dọc.\n"
        "• Bấm Thu gọn ở dòng tiêu đề khối tổng hợp → ẩn hai khối tổng hợp.\n"
        "• Đang tải lại (đổi lọc, đổi trang) → dữ liệu cũ mờ đi, không bị xoá trắng; lỗi tải thì giữ dữ liệu cũ và "
        "báo lỗi.",
    dacbiet=None)

d.p("2.1.2 Layout màn hình")
d.p("Đường dẫn màn hình (2 lối vào, cùng một màn, cùng phạm vi dữ liệu):")
d.set_menu_icons(ICONS_CV)
d._menu_para(MENU_CV)
d.p("Hiển thị: toàn bộ đầu việc trong phạm vi quyền của người đang đăng nhập.")
d.set_menu_icons(ICONS_PRESALE)
d._menu_para(MENU)
d.p("Hiển thị: giống lối vào trên (cùng phạm vi quyền).")
d.figure(shot("01-bao-cao.png"), "Màn Báo cáo kế hoạch & kết quả làm việc theo nhân viên, kỳ Năm nay (người dùng có "
                                 "quyền V1)", width_in=6.2)
d.figure(shot("05-phan-trang.png"), "Cuối bảng: phân trang theo phòng ban, cấp xem “Tất cả cấp”", width_in=6.2)

TIP_MUC_DICH = ("MỤC ĐÍCH BÁO CÁO • Theo dõi KHỐI LƯỢNG và KẾT QUẢ làm việc của Phòng ban - Bộ phận - Nhân viên "
                "trong kỳ • Gom 5 nguồn: Meeting · Task · Issue · Phiếu công tác · Phiếu giao việc • Biết được ai đang "
                "nhiều việc, việc nào quá hạn, tỷ lệ hoàn thành của từng người • Bấm vào con số để mở danh sách đầu "
                "việc chi tiết")
TIP_KHOI_LUONG = ("KHỐI LƯỢNG CÔNG VIỆC TRONG KỲ • Mọi đầu việc có khoảng thời gian GIAO NHAU với kỳ; gom 5 nguồn "
                  "Meeting · Task · Issue · Phiếu công tác · Phiếu giao việc • Tổng đầu việc: số CẤP CÔNG TY nên đếm "
                  "theo PHIẾU (<S> lượt tham gia gộp còn <T> phiếu) • Nhân viên có việc: số người có ít nhất 1 đầu "
                  "việc / <N> nhân viên trong phạm vi đang lọc • Ai có tên trong danh sách thực hiện của phiếu đều "
                  "được tính (chỉ meeting mới có người chủ trì) • Tắt bớt loại ở ô \"Loại công việc\" thì các số "
                  "giảm theo")
TIP_TRANG_THAI = ("TRẠNG THÁI XỬ LÝ • Đã hoàn thành + Đang thực hiện + Quá hạn + Dừng / Huỷ / Từ chối = Tổng đầu "
                  "việc • Đã hoàn thành — Meeting / Task Hoàn thành · Issue Đã xử lý / Đã đóng · Phiếu công tác & "
                  "giao việc đã duyệt kết quả • Đang thực hiện — chưa xong, chưa dừng/huỷ, CHƯA quá hạn (gồm cả nháp / "
                  "chờ duyệt còn hạn) • Quá hạn — hạn đã qua ĐẦU NGÀY hôm nay mà việc chưa xong • Dừng / Huỷ / Từ "
                  "chối — vẫn tính vào Tổng, không tính quá hạn (gồm Task Tạm dừng) • Nhóm nào bằng 0 thì không hiện")
TIP_CACH_DEM = ("CÁCH ĐẾM • Ai có tên trong danh sách thực hiện của phiếu đều được tính (chỉ meeting mới có người chủ "
                "trì) • Dòng Nhân viên tính +1 cho MỖI người tham gia (1 cuộc họp 3 người dự = 3) • Dòng Bộ phận / "
                "Phòng ban / TỔNG đếm theo PHIẾU (cuộc họp đó chỉ là 1) nên dòng cha nhỏ hơn tổng các dòng con • 1 "
                "phiếu có người ở 2 phòng được tính 1 ở MỖI phòng nên cộng các phòng có thể lớn hơn dòng TỔNG • Hover "
                "ô Tổng của dòng cha để xem số lượt tham gia • Dòng TỔNG tính trên toàn bộ dữ liệu đã lọc, không theo "
                "trang")
TIP_TYPE = {
    "Meeting": ("SỐ MEETING • Nguồn: màn Lịch meeting (/assign/meeting) • Mốc thời gian: ngày họp nằm trong kỳ • Tính "
                "cho chủ trì + mọi thành viên dự họp • Cấp Bộ phận / Phòng ban đếm theo phiếu: 1 cuộc họp nhiều người "
                "dự vẫn là 1"),
    "Task": ("SỐ TASK • Nguồn: màn Công việc (/assign/tasks) • Mốc thời gian: khoảng Ngày bắt đầu – Hạn hoàn thành giao "
             "nhau với kỳ • Tính cho người được giao"),
    "Issue": ("SỐ ISSUE • Nguồn: màn Vấn đề (/assign/issues) • Mốc thời gian: khoảng Ngày phát hiện – Hạn xử lý giao "
              "nhau với kỳ • Tính cho người được giao"),
    "P. công tác": ("SỐ PHIẾU CÔNG TÁC • Nguồn: màn Phiếu giao công tác (/assign/assign_business) • Mốc thời gian: "
                    "khoảng Ngày đi – Ngày về giao nhau với kỳ • Tính cho MỌI nhân viên trong đoàn • Cấp Bộ phận / "
                    "Phòng ban đếm theo phiếu: cả đoàn đi chung vẫn là 1"),
    "P. giao việc": ("SỐ PHIẾU GIAO VIỆC • Nguồn: màn Phiếu giao việc tại Công ty (/assign/assign_jobs) • Mốc thời "
                     "gian: khoảng Ngày giao – Hạn hoàn thành giao nhau với kỳ • Tính cho mọi nhân viên thực hiện • Cấp "
                     "Bộ phận / Phòng ban đếm theo phiếu: nhiều người thực hiện vẫn là 1"),
}
TIP_TONG = ("TỔNG KHỐI LƯỢNG • Cộng ngang các cột loại công việc ĐANG BẬT của chính dòng đó • Dòng NHÂN VIÊN: mỗi người "
            "tham gia tính +1 • Dòng BỘ PHẬN / PHÒNG BAN / TỔNG: đếm theo PHIẾU, nhiều người vẫn là 1 • Hover vào ô số "
            "của dòng cha để xem \"N phiếu · M lượt tham gia\"")
TIP_DA_HT = "ĐÃ HOÀN THÀNH • Số đầu việc thuộc nhóm trạng thái \"Đã hoàn thành\" • Bấm vào số để mở danh sách chi tiết"
TIP_TY_LE = ("TỶ LỆ HOÀN THÀNH • Đã HT ÷ Tổng của CHÍNH dòng đó • Mẫu số gồm cả việc đang thực hiện, quá hạn và "
             "huỷ/từ chối")


def icon_lines(text, where=""):
    """Nội dung ⓘ nguyên văn, mỗi ý 1 dòng (quy tắc 1 + 2 "Viết bảng giao diện cho người đọc")."""
    parts = text.split(" • ")
    out = ["- Icon ⓘ: “%s" % parts[0]]
    out += ["   • %s" % x for x in parts[1:]]
    out[-1] += "”"
    if where:
        out.append("- Icon nằm ở%s" % where.strip(" ()").join([" ", ""]))
    return out

d.p("2.1.3 Mô tả chi tiết giao diện")
ui = [
    ("Tiêu đề trang", "Label", "Hiển thị", "–", MAN, ["- Trên thanh tiêu đề"] + icon_lines(
        "Theo dõi khối lượng và kết quả làm việc của từng nhân viên, biết được ai đang nhiều việc, có khả năng thực "
        "hiện công việc hay không.")),
    ("Tiêu đề khối lọc “Bộ lọc báo cáo kế hoạch & kết quả làm việc theo nhân viên”", "Label", "Hiển thị", "–",
     "Hiển thị", icon_lines(TIP_MUC_DICH)),
    ("Dòng tóm tắt “Tổng hợp <kỳ> (<từ ngày> – <đến ngày>)”", "Label", "Hiển thị", "dd/mm/yyyy", "Theo kỳ", [
        "- <kỳ>: tên kỳ đang xem viết thường (tháng này, năm nay, tuỳ chọn…); ngày đầu / cuối kỳ dạng dd/mm/yyyy",
        "- Nối tiếp: “· a đầu việc · b nhân viên có việc · Meeting x · Task y · Issue z · P. công tác u · P. giao việc v”",
        "- a = Tổng đầu việc (ô ở khối Khối lượng); b = Nhân viên có việc; x…v = số đầu việc từng loại ĐANG BẬT ở ô Loại "
        "công việc (loại tắt thì không ghi)",
        "- Số không bấm được",
    ]),
    ("Ô tích “Chỉ hiện nhân viên có việc”", "Checkbox", "Enable", "Có / Không", "Có", [
        "- Nằm bên phải dòng tóm tắt, ngay trái nút Thu gọn",
        "- Mặc định: tích",
        "- Tích: bảng ẩn dòng nhân viên có Tổng = 0 (và phòng / bộ phận không còn dòng con)",
        "- Bỏ tích: tải lại báo cáo, hiện cả nhân viên không có đầu việc",
        "- Không làm đổi số ở khối tổng hợp và dòng TỔNG",
    ]),
    ("Nút Thu gọn / Mở rộng", "Button", "Enable", "–", "Thu gọn", ["- Ẩn / hiện hai khối tổng hợp, đổi chữ trên nút"]),
    ("Khối Khối lượng trong kỳ", "Text", "Hiển thị", "≥ 0", "Theo dữ liệu", [
        "- Tiêu đề kèm chữ “Đếm theo phiếu” bên phải",
    ] + icon_lines(TIP_KHOI_LUONG) + ["- <S>, <T>, <N> là số thật của dữ liệu đang xem"]),
    ("Ô Tổng đầu việc", "Number", "Read-only", "≥ 0", "Theo dữ liệu", [
        "- Số đầu việc (đếm theo phiếu) + chữ phụ “k/5 loại”: k = số loại đang bật ở ô Loại công việc",
        "- Luôn hiện (ô tổng của khối)",
        "- Bấm số → mở popup Danh sách đầu việc chi tiết (mục 2.5), toàn bộ đầu việc của báo cáo",
        "- Số 0: hiện thường, không bấm được",
    ]),
    ("Ô Nhân viên có việc", "Number", "Read-only", "≥ 0", "Theo dữ liệu", [
        "- Dạng “b / N NV”: b = số nhân viên có ít nhất 1 đầu việc; N = số nhân viên trong phạm vi đang lọc (kể cả người "
        "không có việc)",
        "- Không bấm được (đếm người, không có danh sách đầu việc tương ứng)",
    ]),
    ("Khối Trạng thái xử lý", "Text", "Hiển thị", "≥ 0", "Theo dữ liệu", [
        "- Tiêu đề kèm chữ “4 nhóm chia hết tổng” bên phải",
    ] + icon_lines(TIP_TRANG_THAI)),
    ("Ô Đã hoàn thành · Đang thực hiện · Quá hạn · Dừng / Huỷ / Từ chối", "Number", "Read-only", "≥ 0",
     "Theo dữ liệu", [
         "- Mỗi ô: số đầu việc của nhóm + tỷ lệ % = số của nhóm ÷ Tổng đầu việc (1 chữ số thập phân)",
         "- Ô Quá hạn: nền cam, số màu cam",
         "- Nhóm bằng 0 thì không hiện ô",
         "- Bấm số → mở popup Danh sách đầu việc chi tiết (mục 2.5) chỉ gồm đầu việc của nhóm đó",
     ]),
    ("Bảng chi tiết báo cáo", "Table/Grid", "Read-only", "–", "Theo dữ liệu", [
        "- Các cột: STT",
        "- Nội dung theo dõi",
        "- Meeting · Task · Issue · P. công tác · P. giao việc (chỉ các loại đang bật ở ô Loại công việc)",
        "- Tổng",
        "- Đã HT",
        "- Tỷ lệ HT",
        "- Mỗi cột mô tả ở dòng riêng bên dưới",
    ]),
    ("Cột STT", "Text", "Read-only", "–", "Theo dữ liệu", [
        "- Dòng TỔNG: chữ “TỔNG”",
        "- Phòng ban: số La Mã I, II… chạy tiếp theo trang (trang 2, cỡ 10 bắt đầu từ XI)",
        "- Bộ phận (hoặc nhân viên nằm thẳng dưới phòng): 1, 2…",
        "- Nhân viên dưới bộ phận: 1.1, 1.2…",
    ]),
    ("Cột Nội dung theo dõi", "Text", "Read-only", "–", "Theo dữ liệu", [
        "- Tên phòng ban / bộ phận / nhân viên, thụt lề theo cấp, có vạch màu bên trái theo cấp",
        "- Dòng có cấp con có mũi tên bung / thu (mục 2.4); dòng nhân viên chữ xám, nền trắng",
        "- Nhóm “Chưa phân phòng ban”: chữ nghiêng",
        "- Tên dài cắt bằng “…”, rê chuột xem đủ",
        "- Tiêu đề cột chứa ô chọn cấp xem (mục 2.4)",
    ]),
    ("Ô chọn cấp xem (trong tiêu đề cột Nội dung theo dõi)", "Dropdown", "Enable", "Danh sách 3 giá trị",
     "Đến Bộ phận", [
         "- Mặc định: Đến Bộ phận",
         "- Chỉ Phòng ban",
         "- Đến Bộ phận",
         "- Tất cả cấp (đến Nhân viên)",
         "- Chỉ là cách xem, không tải lại số liệu (mục 2.4)",
     ]),
]
for label, tip_key in [("Meeting", "Meeting"), ("Task", "Task"), ("Issue", "Issue"), ("P. công tác", "P. công tác"),
                       ("P. giao việc", "P. giao việc")]:
    ui.append(("Cột %s" % label, "Number", "Read-only", "≥ 0", "Theo dữ liệu", [
        "- Số đầu việc loại %s của dòng (dòng nhân viên: mỗi đầu việc +1; dòng phòng / bộ phận / TỔNG: đếm theo phiếu)"
        % label,
        "- Chỉ hiện khi loại đang bật ở ô Loại công việc",
        "- Bấm số → popup Danh sách đầu việc chi tiết (mục 2.5) chỉ gồm loại %s của dòng đó" % label,
        "- Số 0: chữ xám, không bấm được",
    ] + icon_lines(TIP_TYPE[tip_key], " (tiêu đề cột)")))
ui += [
    ("Cột Tổng", "Number", "Read-only", "≥ 0", "Theo dữ liệu", [
        "- Tổng đầu việc của dòng (các loại đang bật)",
        "- Rê chuột ở dòng phòng / bộ phận / TỔNG (khi có chênh lệch): “N phiếu · M lượt tham gia” — N = số đầu việc, "
        "M = số lượt tham gia",
        "- Bấm số → popup Danh sách đầu việc chi tiết (mục 2.5), mọi đầu việc của dòng",
        "- Số 0: chữ xám, không bấm được",
    ] + icon_lines(TIP_TONG, " (tiêu đề cột)")),
    ("Cột Đã HT", "Number", "Read-only", "≥ 0", "Theo dữ liệu", [
        "- Số đầu việc nhóm Đã hoàn thành của dòng",
        "- Bấm số → popup Danh sách đầu việc chi tiết (mục 2.5) chỉ gồm đầu việc đã hoàn thành của dòng",
        "- Số 0: chữ xám, không bấm được",
    ] + icon_lines(TIP_DA_HT, " (tiêu đề cột)")),
    ("Cột Tỷ lệ HT", "Text", "Read-only", "0.0% – 100.0%", "Theo dữ liệu", [
        "- = Đã HT ÷ Tổng của chính dòng, 1 chữ số thập phân (vd 41.9%)",
        "- Tổng = 0 → 0.0%",
        "- Không bấm được",
    ] + icon_lines(TIP_TY_LE, " (tiêu đề cột)")),
    ("Dòng TỔNG", "Table/Grid", "Read-only", "≥ 0", "Theo dữ liệu", [
        "- Dòng đầu bảng, nền cam, chữ “PHÒNG BAN / BỘ PHẬN / NHÂN VIÊN” viết hoa",
        "- Số tính trên toàn bộ dữ liệu đã lọc, không theo trang; bằng các ô của khối tổng hợp",
        "- Bấm số ở từng cột → popup toàn bộ báo cáo theo cột đó (mục 2.5)",
    ] + icon_lines(TIP_CACH_DEM)),
    ("Thanh cuộn ngang trên / dưới", "Scrollbar", "Hiển thị", "–", "Theo độ rộng", [
        "- Chỉ hiện khi bảng rộng hơn khung (đủ 8 cột số cần ≥ 1,364px)",
        "- Hai thanh cuộn đồng bộ vị trí",
    ]),
    ("Phân trang", "Pagination", "Enable", "10 / 20 / 50 / 100", "20 phòng ban / trang", [
        "- Mặc định: 20 phòng ban / trang",
        "- Phân trang theo nhóm Phòng ban: 1 phòng không bị cắt giữa 2 trang",
        "- Dòng đếm “Hiển thị a–b / N phòng ban”: N = tổng số phòng ban của báo cáo",
    ]),
    ("Trạng thái rỗng", "Label", "Hiển thị", "–", "Ẩn", ["- “Không có đầu việc nào khớp bộ lọc.”"]),
    ("Lớp mờ khi đang tải", "Loading", "Hiển thị", "–", "Ẩn",
     ["- Dữ liệu cũ mờ đi, không bấm được trong lúc tải lại", "- Lỗi tải: giữ dữ liệu cũ, báo câu lỗi của hệ thống"]),
]
d.ui_table(ui, required=False)

d.p("2.1.4 Danh sách event và xử lý event")
d.event_table([
    ("Mở màn hình", "System",
     "Before:\n– Kiểm quyền: không có V1/V2/V3 → menu không hiện, mở thẳng đường dẫn thì báo không được cấp quyền truy "
     "cập.\n"
     "During:\n– Nạp danh mục ô Công ty (công ty đang làm việc, khoá) và dữ liệu báo cáo kỳ Tháng này, trang 1.\n"
     "After:\n– Hiển thị dòng tóm tắt, hai khối tổng hợp, dòng TỔNG và trang 1 của bảng, cấp xem Đến Bộ phận."),
    ("Bấm một số đếm khác 0 (khối tổng hợp / dòng TỔNG / dòng phòng, bộ phận, nhân viên)", "Click",
     "After:\n– Mở popup Danh sách đầu việc chi tiết đúng phạm vi dòng và đúng chỉ tiêu vừa bấm (mục 2.5; bảng vị trí "
     "bấm: 2.1.7)."),
    ("Tích / bỏ tích “Chỉ hiện nhân viên có việc”", "Change", "After:\n– Tải lại báo cáo, về trang 1."),
    ("Bấm số trang / đổi số dòng mỗi trang", "Click",
     "After:\n– Tải trang mới; dòng tóm tắt, khối tổng hợp và dòng TỔNG giữ nguyên. Đổi số dòng → về trang 1. Trang "
     "vượt quá số trang (sau khi đổi lọc) → về trang cuối."),
    ("Bấm Thu gọn / Mở rộng", "Click", "After:\n– Ẩn hoặc hiện hai khối tổng hợp, đổi chữ trên nút."),
    ("Rê chuột ô Tổng của dòng phòng / bộ phận / TỔNG", "Hover", "After:\n– Hiện “N phiếu · M lượt tham gia”."),
    ("Cuộn thanh cuộn ngang trên hoặc dưới", "Change", "After:\n– Thanh còn lại cuộn theo cùng vị trí."),
])

d.p("2.1.5 Quy tắc hiển thị")
d.bullets([
    "Số đếm dùng dấu phẩy ngăn cách hàng nghìn (4,049); tỷ lệ 1 chữ số thập phân (84.2%); ngày dd/mm/yyyy.",
    "Dòng tóm tắt, khối tổng hợp, dòng TỔNG, popup chi tiết, bản in và Excel cùng lấy một tập dữ liệu nên số luôn "
    "khớp (ô Tổng đầu việc = Tổng ở dòng TỔNG = số dòng popup tương ứng).",
    "Dòng phòng / bộ phận / TỔNG đếm theo phiếu nên nhỏ hơn tổng các dòng con khi có việc làm chung — đây là chủ đích.",
])

d.p("2.1.6 Cách lấy dữ liệu và giải thích chỉ tiêu")
d.p("Bảng dưới mô tả cách hệ thống tính từng chỉ tiêu, từng cột số liệu và nội dung icon ⓘ hiển thị khi rê chuột "
    "(nguyên văn trên giao diện; <S>, <T>, <N> là số thật). “Tập dữ liệu” là toàn bộ cặp (đầu việc × người thực hiện) "
    "của 5 loại có thời gian giao nhau với kỳ, người thực hiện thuộc phạm vi quyền, sau khi áp bộ lọc (Phòng ban, Bộ "
    "phận, Nhân viên, Loại công việc, Trạng thái).")
d.data_table([
    ("Tiêu đề bộ lọc (ⓘ cạnh “Bộ lọc báo cáo …”)", "Không phải số liệu.", TIP_MUC_DICH),
    ("Kỳ và ngày đầu / cuối kỳ (dòng tóm tắt)", "Ngày hôm nay → Ngày hôm nay; Tuần này / Tuần tiếp theo → thứ Hai – "
     "Chủ nhật; Tháng này / Tháng tiếp theo → ngày 1 – ngày cuối tháng; Quý này; Năm nay; Tuỳ chọn → khoảng ngày người "
     "dùng chọn (ngày đầu > ngày cuối thì tự đảo). Đầu ngày 00:00, cuối ngày 23:59.", "—"),
    ("Mốc thời gian của từng loại (để xét giao nhau với kỳ)", "Meeting: thời gian họp. Task: Ngày bắt đầu – Hạn hoàn "
     "thành. Issue: Ngày phát hiện – Hạn xử lý. Phiếu công tác: Ngày đi – Ngày về. Phiếu giao việc: Ngày giao – Hạn hoàn "
     "thành (thiếu ngày thì lấy ngày tạo phiếu). Đầu việc vào báo cáo khi khoảng này chạm kỳ.",
     "(ⓘ ở tiêu đề từng cột loại — xem dòng Cột Meeting … Cột P. giao việc)"),
    ("Người thực hiện được tính", "Meeting: chủ trì + mọi thành phần phía công ty. Task / Issue: người được giao. Phiếu "
     "công tác: mọi nhân viên trong đoàn. Phiếu giao việc: mọi nhân viên thực hiện. Ai có tên đều tính như nhau.",
     "(dùng chung ⓘ của khối Khối lượng và dòng TỔNG)"),
    ("Ô Tổng đầu việc", "Đếm số ĐẦU VIỆC khác nhau trong tập dữ liệu (1 phiếu nhiều người = 1).", TIP_KHOI_LUONG),
    ("Chữ phụ “k/5 loại”", "k = số loại đang bật ở ô Loại công việc.", "(dùng chung ⓘ của khối)"),
    ("Ô Nhân viên có việc — b / N", "b = số nhân viên KHÁC NHAU có ít nhất 1 lượt tham gia trong tập dữ liệu. N = số "
     "nhân viên trong phạm vi quyền + bộ lọc Phòng ban / Bộ phận / Nhân viên (kể cả người không có việc).",
     "(dùng chung ⓘ của khối)"),
    ("Ô Đã hoàn thành", "Đếm đầu việc thuộc nhóm Đã hoàn thành: Meeting Hoàn thành; Task Hoàn thành; Issue Đã xử lý / "
     "Đã đóng / Hoàn thành; Phiếu công tác & Phiếu giao việc từ bước đã duyệt kết quả. Tỷ lệ = ô ÷ Tổng đầu việc.",
     TIP_TRANG_THAI),
    ("Ô Đang thực hiện", "Đếm đầu việc chưa hoàn thành, chưa dừng / huỷ / từ chối và hạn kết thúc chưa qua đầu ngày hôm "
     "nay (gồm nháp, chờ duyệt còn hạn).", "(dùng chung ⓘ của khối)"),
    ("Ô Quá hạn", "Đếm đầu việc chưa hoàn thành, chưa dừng / huỷ / từ chối mà hạn kết thúc đã qua đầu ngày hôm nay "
     "(Meeting: đã tới ngày họp mà chưa chốt biên bản; Phiếu công tác / giao việc: hết hạn mà chưa duyệt kết quả).",
     "(dùng chung ⓘ của khối)"),
    ("Ô Dừng / Huỷ / Từ chối", "Đếm Meeting Huỷ; Task Tạm dừng / Huỷ / Từ chối; Issue Từ chối; Phiếu công tác Không "
     "duyệt; Phiếu giao việc Từ chối. Vẫn nằm trong Tổng, không tính quá hạn.", "(dùng chung ⓘ của khối)"),
    ("Ràng buộc khớp số khối Trạng thái", "Đã hoàn thành + Đang thực hiện + Quá hạn + Dừng / Huỷ / Từ chối = Tổng đầu "
     "việc. Nhóm = 0 thì ẩn ô.", "(dùng chung ⓘ của khối)"),
    ("Dòng TỔNG", "Mọi cột tính trên toàn bộ tập dữ liệu, đếm theo phiếu — bằng ô Tổng đầu việc / Đã hoàn thành.",
     TIP_CACH_DEM),
    ("Dòng Phòng ban", "Đầu việc có ít nhất 1 người thực hiện thuộc phòng (theo hồ sơ hiện tại của nhân viên), đếm theo "
     "phiếu. Phiếu có người ở 2 phòng được tính ở cả 2 phòng.", "(dùng chung ⓘ dòng TỔNG)"),
    ("Dòng Bộ phận", "Như dòng Phòng ban, thu hẹp theo bộ phận; chỉ có khi phòng chia bộ phận.",
     "(dùng chung ⓘ dòng TỔNG)"),
    ("Dòng Nhân viên", "Số đầu việc người đó có tên trong danh sách thực hiện (mỗi đầu việc +1).",
     "(dùng chung ⓘ dòng TỔNG)"),
    ("Cột Meeting", "Đếm đầu việc loại Meeting của dòng.", TIP_TYPE["Meeting"]),
    ("Cột Task", "Đếm đầu việc loại Task của dòng.", TIP_TYPE["Task"]),
    ("Cột Issue", "Đếm đầu việc loại Issue của dòng.", TIP_TYPE["Issue"]),
    ("Cột P. công tác", "Đếm Phiếu công tác của dòng.", TIP_TYPE["P. công tác"]),
    ("Cột P. giao việc", "Đếm Phiếu giao việc của dòng.", TIP_TYPE["P. giao việc"]),
    ("Cột Tổng", "Tổng đầu việc của dòng (các loại đang bật). Dòng cha: đếm theo phiếu; rê chuột: N phiếu · M lượt "
     "tham gia.", TIP_TONG),
    ("Cột Đã HT", "Đầu việc nhóm Đã hoàn thành của dòng.", TIP_DA_HT),
    ("Cột Tỷ lệ HT", "Đã HT ÷ Tổng của chính dòng, 1 chữ số thập phân.", TIP_TY_LE),
])

d.p("2.1.7 Danh sách popup mở từ số liệu")
d.p("Mọi vị trí bấm được trên báo cáo và cửa sổ mở ra. Đặc tả chi tiết từng loại popup ở mục được trỏ tới.")
d.popup_table([
    ("Số ở ô Tổng đầu việc (khối Khối lượng)", "Danh sách đầu việc chi tiết (mục 2.5)",
     "Tất cả đầu việc trong kỳ là những việc gì, của ai, đang ở trạng thái nào",
     "Mọi đầu việc của tập dữ liệu, gộp theo phiếu; số dòng = số trên ô"),
    ("Số ở ô Đã hoàn thành / Đang thực hiện / Quá hạn / Dừng – Huỷ – Từ chối", "Danh sách đầu việc chi tiết (mục 2.5)",
     "Việc nào đã xong, việc nào đang trễ hạn để nhắc người thực hiện",
     "Đầu việc của đúng nhóm trạng thái; số dòng = số trên ô"),
    ("Số ở dòng TỔNG (cột loại / Tổng / Đã HT)", "Danh sách đầu việc chi tiết (mục 2.5)",
     "Toàn bộ đầu việc của một loại / đã hoàn thành, dạng phẳng để lọc, in, xuất",
     "Đầu việc của tập dữ liệu theo cột đã bấm; số dòng = số đã bấm"),
    ("Số ở dòng Phòng ban / Bộ phận (cột loại / Tổng / Đã HT)", "Danh sách đầu việc chi tiết (mục 2.5)",
     "Phòng / bộ phận đó đang gánh những việc gì",
     "Thu hẹp theo phòng / bộ phận (biến thể ở 2.5.6); gộp theo phiếu; số dòng = số đã bấm"),
    ("Số ở dòng Nhân viên (cột loại / Tổng / Đã HT)", "Danh sách đầu việc chi tiết (mục 2.5)",
     "Nhân viên đó có những việc nào, việc nào đã xong / trễ",
     "Đầu việc người đó có tên, mỗi đầu việc 1 dòng; số dòng = số đã bấm"),
    ("Số 0 ở bất kỳ ô nào; ô Nhân viên có việc; cột Tỷ lệ HT", "Không mở gì — số 0 chữ xám, không bấm được",
     "Tránh mở popup rỗng / chỉ tiêu không có danh sách đầu việc tương ứng", "–"),
    ("Mã/Số phiếu (hoặc tên công việc) trong popup danh sách", "Chi tiết đầu việc — panel bên phải (mục 2.6)",
     "Đầu việc đó gồm những ai, thời gian, trạng thái; phiếu công tác / giao việc có thêm thông tin phiếu",
     "Thông tin của dòng đã bấm + Thông tin phiếu (P. công tác / P. giao việc, tải khi mở)"),
])

# ----------------------------------------------------------------- 2.2
d.h3("2.2 Tìm kiếm và lọc báo cáo")
d.p("2.2.1 Giới thiệu")
d.rule_ref("- Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang. Chỉ bổ sung các tiêu chí lọc riêng của Báo cáo kế "
           "hoạch & kết quả làm việc theo nhân viên.", anchor="search")
d.intro_table(
    ten="Tìm kiếm và lọc báo cáo",
    mota="Thu hẹp số liệu của toàn màn (tóm tắt, khối tổng hợp, bảng, popup, bản in, Excel) theo Kỳ báo cáo, Trạng "
         "thái, Phòng ban, Bộ phận, Nhân viên và Loại công việc.",
    tacnhan=TACNHAN,
    dieukien="Đang ở màn báo cáo.",
    chinh="1. Khối Tìm kiếm nâng cao mặc định đang mở.\n"
          "2. Người dùng chọn giá trị ở một ô lọc → hệ thống tải lại báo cáo ngay, về trang 1.\n"
          "3. Bấm Tìm kiếm để tải lại với bộ lọc hiện tại; bấm Xóa lọc để về mặc định.",
    phu="• Kỳ = Tuỳ chọn → hiện ô Thời gian; chưa chọn đủ ngày đầu và ngày cuối thì CHƯA tải lại.\n"
        "• Đổi Kỳ sang giá trị khác Tuỳ chọn → ô Thời gian biến mất và xoá khoảng ngày đã chọn.\n"
        "• Ô Công ty luôn khoá ở công ty đang làm việc; Xóa lọc vẫn giữ công ty đó.\n"
        "• Bỏ tích hết Loại công việc → khung ô và nhãn chuyển đỏ, báo cáo trống kèm dòng “Chưa bật loại công việc nào "
        "trong bộ lọc nên bảng và khối tổng hợp đang trống.”\n"
        "• Xóa lọc → mọi ô về mặc định, cấp xem về Đến Bộ phận.",
    dacbiet=None)
d.p("2.2.2 Layout màn hình")
d.layout(menu=MENU, shot=shot("02-bo-loc.png"), shot_caption="Khối Tìm kiếm nâng cao, ô Loại công việc đang mở")
d.p("2.2.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Kỳ báo cáo", "Dropdown", "Enable", "Danh sách 8 giá trị", "Có", "Tháng này", [
        "- Mặc định: Tháng này",
        "- Ngày hôm nay · Tuần này · Tuần tiếp theo · Tháng này · Tháng tiếp theo · Quý này · Năm nay · Tuỳ chọn",
        "- Đứng đầu bộ lọc, không xoá trống được",
    ]),
    ("Thời gian", "Datepicker", "Enable / Ẩn", "dd/mm/yyyy", "Có khi Kỳ = Tuỳ chọn", "Ẩn", [
        "- Chỉ hiện khi Kỳ = Tuỳ chọn, 1 ô chọn khoảng ngày",
        "- Chưa đủ 2 ngày thì chưa tải lại báo cáo",
    ]),
    ("Công ty", "Dropdown", "Disable", "Danh sách", "Có", "Công ty đang làm việc", [
        "- Luôn khoá ở công ty đang làm việc (báo cáo không có cấp tổng công ty)",
    ]),
    ("Trạng thái", "Dropdown", "Enable", "Danh sách 4 giá trị", "Không", "Trống", [
        "- Đã hoàn thành · Đang thực hiện · Quá hạn · Dừng / Huỷ / Từ chối",
        "- Trống = tất cả",
    ]),
    ("Phòng ban", "Dropdown", "Enable", "Danh sách", "Không", "Trống", [
        "- Phòng ban trong phạm vi quyền; có nút ghim 🔒 giữ giá trị lọc cho lần sau",
    ]),
    ("Bộ phận", "Dropdown", "Enable", "Danh sách", "Không", "Trống", [
        "- Bộ phận thuộc phòng ban đang chọn; có nút ghim 🔒",
    ]),
    ("Nhân viên", "Dropdown", "Enable", "Danh sách", "Không", "Trống", [
        "- Nhân viên trong phạm vi, dạng “Tên nhân viên - Mã phòng - Mã nhân viên”",
    ]),
    ("Loại công việc", "Dropdown", "Enable", "Chọn nhiều, 5 giá trị", "Không", "Cả 5 loại", [
        "- Mặc định: cả 5 loại (Meeting, Task, Issue, Phiếu công tác, Phiếu giao việc), hiện dạng chip trên 1 dòng",
        "- Đứng cuối bộ lọc, rộng nửa hàng",
        "- Bấm ô → panel có ô tìm, ô tích từng loại, nút Chọn tất cả / Xóa tất cả",
        "- Bỏ hết loại → khung ô và nhãn đỏ, báo cáo trống",
        "- Loại tắt thì cột loại đó ẩn khỏi bảng",
    ]),
    ("Nút In danh sách · Xuất Excel · Cài đặt bộ lọc · Ẩn / Hiện tìm kiếm nâng cao", "Button", "Enable", "–", "–",
     "Hiển thị", ["- Trên thanh tiêu đề khối lọc; In / Xuất Excel: mục 2.7, 2.8; Cài đặt bộ lọc: mục 2.3"]),
    ("Nút Tìm kiếm", "Button", "Enable", "–", "–", "Hiển thị", ["- Tải lại báo cáo theo bộ lọc hiện tại"]),
    ("Nút Xóa lọc", "Button", "Enable", "–", "–", "Hiển thị", ["- Đưa mọi ô về mặc định (giữ công ty bị khoá)"]),
])
d.p("2.2.4 Danh sách event và xử lý event")
d.event_table([
    ("Chọn / bỏ giá trị ở một ô lọc", "Change",
     "Before:\n– Ô Công ty bị khoá thì bỏ qua thay đổi.\n"
     "During:\n– Kỳ đổi khác Tuỳ chọn → xoá khoảng ngày. Kỳ = Tuỳ chọn mà chưa đủ 2 ngày → dừng, chưa tải.\n"
     "After:\n– Tải lại báo cáo, về trang 1."),
    ("Tích / bỏ tích ở ô Loại công việc", "Change",
     "During:\n– Gộp các lần tích liên tiếp (0,2 giây) thành 1 lần tải.\n"
     "After:\n– Tải lại báo cáo; bảng chỉ còn cột của loại đang bật."),
    ("Bấm Tìm kiếm", "Click", "After:\n– Tải lại báo cáo, về trang 1."),
    ("Bấm Xóa lọc", "Click", "After:\n– Mọi ô về mặc định, cấp xem Đến Bộ phận, tải lại báo cáo."),
])

# ----------------------------------------------------------------- 2.3
d.h3("2.3 Cài đặt bộ lọc")
d.p("2.3.1 Biểu đồ Usecase")
d.uc_figure("FR-03", "Cài đặt bộ lọc", "view", actor=ACT, caption="Biểu đồ Use Case — FR-03 Cài đặt bộ lọc")
d.p("2.3.2 Giới thiệu")
d.rule_ref("- Cấu hình bộ lọc. Chỉ bổ sung danh sách tiêu chí lọc riêng của Báo cáo kế hoạch & kết quả làm việc theo "
           "nhân viên.", anchor="excel")
d.intro_table(
    ten="Cài đặt bộ lọc",
    mota="Cho mỗi người dùng tự chọn các ô lọc hiển thị và thứ tự của chúng. Cấu hình lưu riêng cho màn hình này.",
    tacnhan=TACNHAN,
    dieukien="Đang ở màn báo cáo.",
    chinh="1. Người dùng bấm nút Cài đặt bộ lọc.\n"
          "2. Hệ thống mở cửa sổ với 5 tiêu chí (Kỳ báo cáo, Công ty, Trạng thái, Phòng ban – Bộ phận – Nhân viên, Loại "
          "công việc), đánh số và tích theo cấu hình đang lưu.\n"
          "3. Người dùng tích / bỏ tích, kéo biểu tượng ⠿ để đổi thứ tự.\n"
          "4. Người dùng bấm Lưu → hệ thống lưu cấu hình, đóng cửa sổ và vẽ lại khối lọc.",
    phu="• Bấm Khôi phục mặc định → về thứ tự gốc, tích đủ 5 tiêu chí; phải bấm Lưu mới ghi.\n"
        "• Bấm Đóng hoặc × → bỏ mọi thay đổi chưa lưu.\n"
        "• Ẩn một ô đang có giá trị → giá trị của ô đó được xoá khỏi bộ lọc.\n"
        "• Ô Thời gian không có trong danh sách: nó là ô con của Kỳ báo cáo, chỉ hiện khi Kỳ = Tuỳ chọn.",
    dacbiet=None)
d.p("2.3.3 Layout màn hình")
d.layout(menu=MENU + " => Cài đặt bộ lọc", modal="Cài đặt bộ lọc", shot=shot("03-cai-dat-bo-loc.png"),
         shot_caption="Cửa sổ Cài đặt bộ lọc với 5 tiêu chí")
d.p("2.3.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Tiêu đề cửa sổ", "Label", "Hiển thị", "–", "–", "Cài đặt bộ lọc", ["- Kèm icon bánh răng"]),
    ("Dòng hướng dẫn", "Label", "Hiển thị", "–", "–", "Hiển thị",
     ["- “Tích chọn trường lọc muốn hiển thị; kéo ⠿ để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”"]),
    ("Ô tích từng tiêu chí", "Checkbox", "Enable", "Danh sách 5 tiêu chí", "Không", "Theo cấu hình đã lưu", [
        "- Kỳ báo cáo",
        "- Công ty",
        "- Trạng thái",
        "- Phòng ban – Bộ phận – Nhân viên",
        "- Loại công việc",
    ]),
    ("Tay kéo ⠿", "Icon Button", "Enable", "–", "–", "Hiển thị", ["- Kéo để đổi thứ tự"]),
    ("Nút Lưu", "Button", "Enable", "–", "–", "Hiển thị", ["- Lưu cấu hình"]),
    ("Nút Khôi phục mặc định", "Button", "Enable", "–", "–", "Hiển thị", ["- Chưa ghi, phải bấm Lưu"]),
    ("Nút Đóng / ×", "Button", "Enable", "–", "–", "Hiển thị", ["- Đóng, bỏ thay đổi chưa lưu"]),
])
d.p("2.3.5 Danh sách event và xử lý event")
d.event_table([
    ("Bấm Cài đặt bộ lọc", "Click", "After:\n– Mở cửa sổ, nạp cấu hình đang lưu."),
    ("Bấm Lưu", "Click",
     "During:\n– Ghi cấu hình (tiêu chí hiển thị + thứ tự) cho người dùng hiện tại.\n"
     "After:\n– Thành công: đóng cửa sổ, vẽ lại khối lọc. Lỗi: báo lỗi, giữ cửa sổ."),
    ("Bấm Khôi phục mặc định", "Click", "After:\n– Đưa danh sách về thứ tự gốc, tích đủ 5 tiêu chí."),
])

# ----------------------------------------------------------------- 2.4
d.h3("2.4 Chọn cấp xem và bung / thu gọn dòng")
d.p("2.4.1 Giới thiệu")
d.rule_ref("- Màn Danh sách và Cấu hình cột. Chỉ bổ sung cách bung / thu gọn bảng chi tiết báo cáo.", anchor="list")
d.intro_table(
    ten="Chọn cấp xem và bung / thu gọn dòng",
    mota="Chọn bảng hiển thị sẵn tới cấp nào, hoặc bung / thu từng dòng bằng mũi tên. Chỉ là cách xem, không tải lại "
         "số liệu.",
    tacnhan=TACNHAN,
    dieukien="Bảng có dữ liệu.",
    chinh="1. Người dùng mở ô chọn cấp trong tiêu đề cột Nội dung theo dõi.\n"
          "2. Người dùng chọn: Chỉ Phòng ban / Đến Bộ phận / Tất cả cấp (đến Nhân viên).\n"
          "3. Hệ thống bung các dòng tới đúng cấp đã chọn trên trang đang xem.",
    phu="• Bung theo TÊN CẤP: ở “Đến Bộ phận”, phòng có bộ phận thì bung ra bộ phận; nhân viên nằm thẳng dưới phòng "
        "(phòng không chia bộ phận / nhân viên chưa gán bộ phận) chưa hiện cho tới khi chọn “Tất cả cấp”.\n"
        "• Bấm mũi tên ở một dòng → chỉ bung / thu dòng đó, và hiện hết dòng con thật của nó.\n"
        "• Đổi trang, đổi bộ lọc → bảng áp lại đúng cấp đang chọn. Xóa lọc → về Đến Bộ phận.",
    dacbiet=None)
d.p("2.4.2 Layout màn hình")
d.layout(menu=MENU, shot=shot("04-tat-ca-cap.png"), shot_caption="Cấp xem “Tất cả cấp (đến Nhân viên)”")
d.p("2.4.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Ô chọn cấp xem", "Dropdown", "Enable", "Danh sách 3 giá trị", "Có", "Đến Bộ phận", [
        "- Mặc định: Đến Bộ phận",
        "- Chỉ Phòng ban",
        "- Đến Bộ phận",
        "- Tất cả cấp (đến Nhân viên)",
    ]),
    ("Mũi tên bung / thu", "Icon Button", "Enable", "–", "–", "Theo cấp đang chọn", [
        "- Ở dòng phòng ban, bộ phận có dòng con; xoay xuống khi đang bung",
        "- Rê chuột: “Hiện / Ẩn bộ phận / nhân viên”",
    ]),
    ("Thụt lề và vạch cấp", "Label", "Hiển thị", "3 cấp", "–", "Hiển thị", [
        "- Mỗi cấp lùi thêm một nấc, vạch trái nhạt dần theo cấp",
        "- Dòng đang bung tô nền xanh nhạt; dòng nhân viên chữ xám, nền trắng",
    ]),
])
d.p("2.4.4 Danh sách event và xử lý event")
d.event_table([
    ("Đổi ô chọn cấp xem", "Change", "After:\n– Bung / thu các dòng của trang đang xem theo cấp mới."),
    ("Bấm mũi tên ở một dòng", "Click", "After:\n– Bung hoặc thu riêng dòng đó."),
])

# ----------------------------------------------------------------- 2.5
d.h3("2.5 Xem danh sách đầu việc chi tiết")
d.p("2.5.1 Giới thiệu")
d.rule_ref("- Màn Danh sách, Kịch bản tìm kiếm, Bộ lọc, Sắp xếp dữ liệu bảng và Phân trang. Chỉ bổ sung các quy tắc "
           "riêng của popup danh sách đầu việc chi tiết.", anchor="list")
d.intro_table(
    ten="Xem danh sách đầu việc chi tiết",
    mota="Popup liệt kê phẳng từng đầu việc đứng sau con số vừa bấm, cùng phạm vi quyền và bộ lọc của báo cáo đang hiển "
         "thị; tìm, lọc, sắp xếp ngay trong popup; có khối tổng hợp riêng của danh sách đang xem.",
    tacnhan=TACNHAN,
    dieukien="Báo cáo đã tải xong; người dùng bấm một số đếm khác 0 (danh sách vị trí bấm: mục 2.1.7).",
    chinh="1. Người dùng bấm một con số ở khối tổng hợp, dòng TỔNG hoặc dòng phòng ban / bộ phận / nhân viên.\n"
          "2. Hệ thống mở popup, tải toàn bộ đầu việc của con số đó.\n"
          "3. Popup hiển thị danh sách, mặc định 20 dòng / trang, sắp theo Bắt đầu tăng dần.\n"
          "4. Người dùng gõ ô tìm / chọn ô lọc → danh sách lọc ngay, về trang 1; bấm tiêu đề cột → sắp tăng / giảm.",
    phu="• Ô lọc và cột đã bị con số cố định thì ẩn — từng trường hợp ở mục 2.5.6.\n"
        "• Danh sách chỉ gồm Phiếu công tác / Phiếu giao việc → không có cột Tên công việc; danh sách lẫn loại khác → "
        "dòng của 2 loại này để “—” ở cột Tên công việc.\n"
        "• Chọn Phòng ban / Bộ phận / Nhân viên trong popup → tải lại từ hệ thống; chọn Loại / Trạng thái / gõ ô tìm → "
        "lọc ngay trên danh sách đã tải.\n"
        "• Bấm chip ở khối “Phân bổ đầu việc theo cơ cấu” → lọc nhanh theo mục đó; bấm lần nữa → bỏ lọc.\n"
        "• Có ô lọc đang áp → hiện nút Xoá lọc. Ô trống luôn xếp cuối khi sắp xếp.\n"
        "• Mỗi lần mở là trạng thái sạch (không giữ tìm / lọc / sắp / trang của lần trước).",
    dacbiet=None)
d.p("2.5.2 Layout màn hình")
d.layout(menu=MENU, modal="Danh sách đầu việc chi tiết", shot=shot("06-popup-chi-tiet.png"),
         shot_caption="Popup mở từ ô Tổng ở dòng TỔNG: có cột Tên công việc, dòng phiếu công tác để “—”")
d.figure(shot("07-popup-phieu-cong-tac.png"), "Popup mở từ cột P. công tác: không có cột Tên công việc", width_in=6.2)
d.p("2.5.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Đầu popup", "Label", "Hiển thị", "–", "–", "Theo con số đã bấm", [
        "- Dòng 1: “Đang xem <chỉ tiêu> — toàn bộ báo cáo” hoặc “Đang xem <chỉ tiêu> theo <cấp>: <tên>” (mục 2.5.6)",
        "- Dòng 2: “<đường dẫn cấp cha> · a đầu việc · b lượt tham gia · hoàn thành c · quá hạn d · Kỳ <từ> – <đến>”",
        "- a = số dòng sau lọc trong popup; b = tổng số người trên các dòng (chỉ ghi khi khác a); c, d = số dòng nhóm Đã "
        "hoàn thành / Quá hạn",
    ]),
    ("Nút Phóng to / ×", "Icon Button", "Enable", "–", "–", "Hiển thị", ["- Phóng toàn màn hình / đóng popup"]),
    ("Ô tìm", "Textbox", "Enable", "0–255 ký tự", "Không", "Trống", [
        "- Placeholder “Tìm mã, tên công việc…”",
        "- Tìm không phân biệt hoa thường trong: tên công việc, mã/số phiếu, tên nhân viên, phòng ban, bộ phận",
    ]),
    ("Ô lọc Loại công việc · Phòng ban · Bộ phận · Nhân viên · Trạng thái", "Dropdown", "Enable / Ẩn", "Danh sách",
     "Không", "Trống (“<tên>: tất cả”)", [
         "- Mỗi ô ẩn khi chiều đó đã bị con số cố định (mục 2.5.6)",
         "- Danh mục lấy từ chính các dòng của popup",
     ]),
    ("Nút Xoá lọc", "Icon Button", "Enable / Ẩn", "–", "–", "Ẩn", ["- Chỉ hiện khi có ô lọc / ô tìm đang áp"]),
    ("Dòng đếm “x / y đầu việc”", "Label", "Hiển thị", "≥ 0", "–", "Theo dữ liệu", [
        "- x = số dòng sau tìm / lọc trong popup, y = tổng dòng của con số đã bấm",
        "- Số có dấu phẩy ngăn nghìn (4,049 / 4,049 đầu việc)",
    ]),
    ("Khối “Tổng hợp danh sách đang xem” + nút Xem tổng hợp / Thu gọn", "Text", "Hiển thị", "–", "–", "Thu gọn", [
        "- Mặc định thu gọn; bấm Xem tổng hợp để mở",
        "- Ô Tỷ lệ hoàn thành: “x%” + “c/a” + thanh tiến độ (x = c ÷ a)",
        "- Icon ⓘ: “CÔNG THỨC • Đã hoàn thành ÷ Tổng đầu việc trong danh sách đang lọc”",
        "- Ô Tỷ lệ quá hạn: “x%” + “d/a” + thanh tiến độ (x = d ÷ a)",
        "- Icon ⓘ: “CÔNG THỨC • Quá hạn ÷ Tổng đầu việc trong danh sách đang lọc”",
        "- Khối “Phân bổ đầu việc theo cơ cấu”: chip Loại công việc và Phòng ban, mỗi chip “tên · số · %”; bấm chip → "
        "lọc nhanh",
    ]),
    ("Cột STT", "Text", "Read-only", "–", "–", "Theo dữ liệu", ["- Chạy liên tục qua các trang"]),
    ("Cột Loại", "Text", "Read-only", "–", "–", "Theo dữ liệu",
     ["- Chấm màu + Meeting / Task / Issue / P. công tác / P. giao việc", "- Sắp xếp được"]),
    ("Cột Phòng ban · Bộ phận · Nhân viên", "Text", "Read-only", "–", "–", "Theo dữ liệu", [
        "- Người đại diện của đầu việc + “+N”: N = số người thực hiện còn lại (dòng gộp theo phiếu)",
        "- Rê chuột: danh sách đủ người thực hiện",
        "- Sắp xếp được",
    ]),
    ("Cột Mã/Số phiếu", "Text", "Read-only", "–", "–", "Theo dữ liệu", [
        "- Mã chứng từ của đầu việc (Meeting: mã meeting; Issue: mã vấn đề…)",
        "- Bấm mã → mở panel Chi tiết đầu việc bên phải (mục 2.6)",
    ]),
    ("Cột Tên công việc", "Text", "Read-only / Ẩn", "–", "–", "Theo dữ liệu", [
        "- Meeting / Task / Issue: tên đầu việc, bấm → mở panel Chi tiết đầu việc (mục 2.6)",
        "- Phiếu công tác / Phiếu giao việc: “—” (thông tin phiếu xem ở panel)",
        "- Ẩn cả cột khi danh sách chỉ gồm Phiếu công tác / Phiếu giao việc",
    ]),
    ("Cột Bắt đầu · Kết thúc/Hạn", "Text", "Read-only", "dd/mm/yyyy hh:mm", "–", "Theo dữ liệu",
     ["- Mốc thời gian của đầu việc (theo loại — mục 2.1.6)", "- Sắp xếp được; mặc định Bắt đầu tăng dần"]),
    ("Cột Trạng thái", "Badge", "Read-only", "–", "–", "Theo dữ liệu",
     ["- 1 trong 4 nhóm trạng thái, màu theo nhóm", "- Sắp xếp theo vòng đời: Đã hoàn thành → Đang thực hiện → Quá hạn → "
      "Dừng / Huỷ / Từ chối"]),
    ("Phân trang", "Pagination", "Enable", "Theo lựa chọn", "–", "20 dòng / trang", ["- “Hiển thị a–b / N đầu việc”"]),
    ("Nút In danh sách · Xuất Excel danh sách · Đóng", "Button", "Enable", "–", "–", "Hiển thị", [
        "- In / Xuất Excel đúng tập dòng đang hiện (con số đã bấm + ô lọc + ô tìm + cột đang sắp) — mục 2.7, 2.8",
        "- Đóng: tắt popup",
    ]),
])
d.p("2.5.4 Danh sách event và xử lý event")
d.event_table([
    ("Mở popup", "System",
     "During:\n– Tải toàn bộ đầu việc của con số đã bấm theo bộ lọc của báo cáo đang hiển thị.\n"
     "After:\n– Ẩn ô lọc / cột đã bị con số cố định, hiển thị trang 1 sắp theo Bắt đầu tăng dần."),
    ("Chọn Phòng ban / Bộ phận / Nhân viên trong popup", "Change",
     "After:\n– Tải lại danh sách từ hệ thống theo ô vừa chọn (lọc trên từng người rồi mới gộp theo phiếu)."),
    ("Gõ ô tìm / chọn Loại, Trạng thái / bấm chip phân bổ", "Change", "After:\n– Lọc tại chỗ, về trang 1, cập nhật x / y."),
    ("Bấm tiêu đề cột", "Click", "After:\n– Sắp trên toàn bộ dòng đã lọc rồi mới cắt trang."),
    ("Bấm mã/số phiếu hoặc tên công việc", "Click", "After:\n– Mở panel Chi tiết đầu việc nổi trên popup (mục 2.6)."),
    ("Bấm Đóng / ×", "Click", "After:\n– Đóng popup, giữ nguyên báo cáo (bộ lọc, trang, cấp đang bung)."),
])
d.p("2.5.5 Mục đích thiết kế popup")
d.bullets([
    "Trả lời câu hỏi “con số này gồm những đầu việc nào”: loại gì, của phòng / bộ phận / nhân viên nào, thời gian bắt "
    "đầu – kết thúc, đang ở trạng thái nào — để quản lý nhắc đúng người, đúng việc đang trễ.",
    "Là POPUP để giữ nguyên ngữ cảnh báo cáo: bộ lọc, trang và cấp đang bung không đổi, đóng popup là về đúng chỗ đang "
    "xem. Danh sách phẳng để tìm, lọc, sắp xếp, in và xuất đúng tập dòng đó.",
    "Khớp số: popup lấy cùng tập dữ liệu, cùng phạm vi quyền + bộ lọc của báo cáo đang hiển thị nên số dòng = con số đã "
    "bấm trước khi lọc thêm. Dòng phòng / bộ phận / TỔNG gộp theo phiếu (1 phiếu = 1 dòng, “+N” người); dòng nhân viên "
    "mỗi đầu việc 1 dòng.",
    "Từ popup người dùng làm tiếp: lọc theo phòng / bộ phận / nhân viên / loại / trạng thái, mở chi tiết đầu việc, in "
    "hoặc xuất Excel đúng danh sách. Mỗi lần mở là trạng thái sạch.",
])
d.p("2.5.6 Các biến thể theo con số bấm")
d.p("Cùng một popup; con số bấm vào quyết định tập dòng, tiêu đề và ô lọc / cột nào bị ẩn:")
d.popup_variant_table([
    ("Ô Tổng đầu việc (khối tổng hợp) / ô Tổng ở dòng TỔNG", "Mọi đầu việc của tập dữ liệu, gộp theo phiếu",
     "Đang xem Tổng đầu việc — toàn bộ báo cáo", "Không ẩn ô lọc nào"),
    ("Ô một nhóm trạng thái (khối tổng hợp) / ô Đã HT ở dòng TỔNG", "Đầu việc của đúng nhóm đó",
     "Đang xem Đầu việc <đã hoàn thành | đang thực hiện | quá hạn | dừng / huỷ / từ chối> — toàn bộ báo cáo",
     "Ẩn ô + cột Trạng thái"),
    ("Cột một loại ở dòng TỔNG", "Đầu việc của đúng loại đó", "Đang xem <Meeting | Task | Issue | Phiếu công tác | "
     "Phiếu giao việc> — toàn bộ báo cáo", "Ẩn ô + cột Loại; loại là P. công tác / P. giao việc → ẩn cột Tên công việc"),
    ("Số ở dòng Phòng ban", "Đầu việc có người thực hiện thuộc phòng, gộp theo phiếu",
     "Đang xem <chỉ tiêu> theo Phòng ban: <tên phòng>",
     "Ẩn ô + cột Phòng ban; phòng không chia bộ phận → ẩn thêm Bộ phận"),
    ("Số ở dòng Bộ phận", "Đầu việc có người thực hiện thuộc bộ phận, gộp theo phiếu",
     "Đang xem <chỉ tiêu> theo Bộ phận: <tên> (dòng 2 có “Phòng ban: <tên phòng>”)", "Ẩn ô + cột Phòng ban, Bộ phận"),
    ("Số ở dòng Nhân viên", "Đầu việc người đó có tên, mỗi đầu việc 1 dòng (không gộp)",
     "Đang xem <chỉ tiêu> theo Nhân viên: <tên> (dòng 2 có đường dẫn phòng › bộ phận)",
     "Ẩn ô + cột Phòng ban, Bộ phận, Nhân viên"),
])
d.p("2.5.7 Cách lấy dữ liệu và giải thích chỉ tiêu")
d.data_table([
    ("Tập dòng của popup", "Các cặp (đầu việc × người) của tập dữ liệu báo cáo, lọc theo phạm vi dòng đã bấm (phòng / bộ "
     "phận / nhân viên) và chỉ tiêu đã bấm (loại / nhóm trạng thái) TRƯỚC, rồi mới gộp theo phiếu (trừ dòng nhân viên) — "
     "nhờ vậy lọc 1 nhân viên không kéo theo người khác cùng phiếu.", "—"),
    ("a đầu việc · b lượt tham gia (đầu popup)", "a = số dòng sau lọc; b = tổng số người trên các dòng (dòng gộp: số "
     "người của phiếu).", "—"),
    ("hoàn thành c · quá hạn d", "Số dòng nhóm Đã hoàn thành / Quá hạn trong danh sách sau lọc.", "—"),
    ("Ô Tỷ lệ hoàn thành", "c ÷ a, 1 chữ số thập phân.", "CÔNG THỨC • Đã hoàn thành ÷ Tổng đầu việc trong danh sách đang lọc"),
    ("Ô Tỷ lệ quá hạn", "d ÷ a, 1 chữ số thập phân.", "CÔNG THỨC • Quá hạn ÷ Tổng đầu việc trong danh sách đang lọc"),
    ("Chip phân bổ (Loại công việc / Phòng ban)", "Đếm số dòng theo từng loại / phòng của người đại diện; % = số ÷ a.",
     "—"),
    ("Cột Phòng ban · Bộ phận · Nhân viên (+N)", "Người đại diện của phiếu và phòng / bộ phận theo hồ sơ hiện tại; +N = số "
     "người thực hiện còn lại.", "—"),
    ("Cột Bắt đầu · Kết thúc/Hạn", "Mốc thời gian theo loại (mục 2.1.6).", "—"),
    ("Cột Trạng thái", "Nhóm trạng thái (mục 2.1.6).", "—"),
])

# ----------------------------------------------------------------- 2.6
d.h3("2.6 Xem chi tiết đầu việc")
d.p("2.6.1 Giới thiệu")
d.rule_ref("- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung nội dung riêng của panel chi tiết đầu việc.", anchor="detail")
d.intro_table(
    ten="Xem chi tiết đầu việc",
    mota="Panel bên phải hiển thị thông tin của đầu việc đã bấm trong popup: thời gian, trạng thái, phòng ban, thành "
         "phần tham gia; với Phiếu công tác / Phiếu giao việc có thêm khối “Thông tin phiếu” lấy từ chính phiếu.",
    tacnhan=TACNHAN,
    dieukien="Đang mở popup danh sách đầu việc chi tiết; người dùng bấm mã/số phiếu hoặc tên công việc.",
    chinh="1. Người dùng bấm mã/số phiếu (hoặc tên công việc với Meeting / Task / Issue).\n"
          "2. Panel mở nổi trên popup, đầu panel nền gradient của báo cáo.\n"
          "3. Phiếu công tác / Phiếu giao việc: hệ thống tải khối Thông tin phiếu (“Đang tải…” trong lúc chờ).",
    phu="• Phiếu ngoài phạm vi quyền báo cáo → không tải được Thông tin phiếu (hệ thống chặn).\n"
        "• Trường nào phiếu để trống → không hiện dòng đó; phiếu không ghi thêm gì → “Phiếu chưa ghi thêm thông tin.”\n"
        "• Bấm nút Đóng / × / phím Esc / bấm ra ngoài → đóng panel, popup bên dưới giữ nguyên.",
    dacbiet=None)
d.p("2.6.2 Layout màn hình")
d.layout(menu=MENU, modal="Chi tiết đầu việc", shot=shot("09-panel-phieu-giao-viec.png"),
         shot_caption="Panel chi tiết Phiếu giao việc có khối Thông tin phiếu")
d.figure(shot("08-panel-phieu-cong-tac.png"), "Panel chi tiết Phiếu công tác", width_in=6.2)
d.figure(shot("10-panel-meeting.png"), "Panel chi tiết Meeting (không có khối Thông tin phiếu)", width_in=6.2)
d.p("2.6.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Tiêu đề panel", "Label", "Hiển thị", "–", "Theo dữ liệu", [
        "- Meeting / Task / Issue: tên đầu việc",
        "- Phiếu giao việc: tên công việc của phiếu",
        "- Phiếu công tác: “Phiếu công tác <mã phiếu>” (phiếu không có trường tên)",
    ]),
    ("Chip loại + mã phiếu · dòng thời gian", "Label", "Hiển thị", "dd/mm/yyyy hh:mm", "Theo dữ liệu",
     ["- “<Bắt đầu> – <Kết thúc/Hạn>”"]),
    ("Khối Thông tin đầu việc", "Text", "Read-only", "–", "Theo dữ liệu", [
        "- Trạng thái: nhóm trạng thái (badge màu)",
        "- Trạng thái chứng từ: trạng thái gốc của phiếu (vd Đã duyệt, Đã duyệt KQ, Hoàn thành)",
        "- Bắt đầu / Ngày họp; Kết thúc / Hạn hoàn thành",
        "- Tiến độ: chỉ Task có %, loại khác “—”; Meeting ghi “Biên bản họp: Đã chốt biên bản / Chưa có biên bản”",
        "- Phòng ban, Bộ phận của người đại diện",
    ]),
    ("Khối Thông tin phiếu (chỉ Phiếu công tác)", "Text", "Read-only / Ẩn", "–", "Theo dữ liệu", [
        "- Khách hàng: “mã - tên”",
        "- Địa điểm công tác",
        "- Hợp đồng: mã hợp đồng",
        "- Trưởng đoàn: tên người được đánh dấu trưởng đoàn",
        "- Nội dung công việc (cả hàng)",
        "- Ghi chú (cả hàng)",
        "- Trường trống thì ẩn",
    ]),
    ("Khối Thông tin phiếu (chỉ Phiếu giao việc)", "Text", "Read-only / Ẩn", "–", "Theo dữ liệu", [
        "- Tên công việc (cả hàng)",
        "- Khách hàng",
        "- Địa điểm",
        "- Người liên hệ: “tên - số điện thoại”",
        "- Phòng yêu cầu; Phòng thực hiện",
        "- Số giờ: “16 giờ”",
        "- Mô tả công việc (cả hàng, giữ xuống dòng)",
        "- Trường trống thì ẩn",
    ]),
    ("Khối Thành phần tham gia (N người)", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     ["- STT · Nhân viên · Phòng ban · Bộ phận", "- Dòng nhân viên (không gộp) → 1 người là chính nhân viên đó"]),
    ("Nút Đóng / ×", "Button", "Enable", "–", "Hiển thị", ["- Đóng panel, giữ popup"]),
], required=False)
d.p("2.6.4 Danh sách event và xử lý event")
d.event_table([
    ("Bấm mã/số phiếu hoặc tên công việc", "Click",
     "After:\n– Mở panel với dữ liệu của dòng đã bấm (không cần tải thêm)."),
    ("Mở panel Phiếu công tác / Phiếu giao việc", "System",
     "Before:\n– Hệ thống kiểm phiếu có ít nhất 1 người thực hiện trong phạm vi quyền báo cáo; không có → chặn.\n"
     "During:\n– Hiện “Đang tải…” ở khối Thông tin phiếu.\n"
     "After:\n– Hiện các trường có dữ liệu; mở phiếu khác trước khi xong thì bỏ kết quả cũ."),
    ("Bấm Đóng / × / Esc / ra ngoài panel", "Click", "After:\n– Đóng panel; popup bên dưới giữ nguyên."),
])
d.p("2.6.5 Mục đích thiết kế popup")
d.bullets([
    "Trả lời câu hỏi “đầu việc này cụ thể là gì”: ai tham gia, thời gian, trạng thái gốc; với Phiếu công tác / Phiếu giao "
    "việc là khách hàng nào, ở đâu, làm nội dung gì — thay cho cột Tên công việc (2 loại này không có tên rõ nghĩa).",
    "Là PANEL trượt bên phải, nổi trên popup danh sách: đọc chi tiết mà không mất danh sách đang lọc; đóng panel là về "
    "đúng dòng đang xem.",
    "Đối chiếu số: panel chỉ hiển thị, không tính lại số nào; thành phần tham gia khớp “+N” ở cột Nhân viên.",
    "Thông tin phiếu tải KHI MỞ panel (không nạp sẵn vào danh sách popup) để popup hàng nghìn dòng vẫn nhẹ.",
])
d.p("2.6.6 Các biến thể theo con số bấm")
d.popup_variant_table([
    ("Mã/tên Meeting", "Meeting đã bấm", "Tên meeting", "Không có khối Thông tin phiếu; Tiến độ = Biên bản họp"),
    ("Mã/tên Task / Issue", "Đầu việc đã bấm", "Tên đầu việc", "Không có khối Thông tin phiếu; Task có Tiến độ %"),
    ("Mã Phiếu công tác", "Phiếu đã bấm + Thông tin phiếu (tải khi mở)", "Phiếu công tác <mã>",
     "Có khối Thông tin phiếu (6 trường)"),
    ("Mã Phiếu giao việc", "Phiếu đã bấm + Thông tin phiếu (tải khi mở)", "<Tên công việc>",
     "Có khối Thông tin phiếu (8 trường)"),
])
d.p("2.6.7 Cách lấy dữ liệu và giải thích chỉ tiêu")
d.data_table([
    ("Trạng thái / Trạng thái chứng từ", "Nhóm trạng thái theo dõi (mục 2.1.6) / trạng thái gốc ghi trên phiếu.", "—"),
    ("Khách hàng (P. công tác)", "Mã + tên khách hàng ghi trên phiếu công tác.", "—"),
    ("Trưởng đoàn (P. công tác)", "Tên các nhân viên được đánh dấu trưởng đoàn trong danh sách đoàn.", "—"),
    ("Phòng yêu cầu / Phòng thực hiện (P. giao việc)", "Tên phòng ban ghi trên phiếu giao việc.", "—"),
    ("Số giờ (P. giao việc)", "Tổng số giờ ghi trên phiếu, bỏ số 0 thừa (16.00 → 16 giờ).", "—"),
    ("Thành phần tham gia", "Mọi người thực hiện của đầu việc trong phạm vi báo cáo (dòng gộp) hoặc chính nhân viên (dòng "
     "nhân viên).", "—"),
])

# ----------------------------------------------------------------- 2.7
d.h3("2.7 In danh sách")
d.p("2.7.1 Biểu đồ Usecase")
d.uc_figure("FR-07", "In danh sách", "io", actor=ACT, caption="Biểu đồ Use Case — FR-07 In danh sách")
d.p("2.7.2 Giới thiệu")
d.rule_ref("- Thông báo và UI/UX. Chỉ bổ sung bố cục và dữ liệu riêng của bản in Báo cáo kế hoạch & kết quả làm việc "
           "theo nhân viên.", anchor="notice")
d.intro_table(
    ten="In danh sách",
    mota="In khổ A4 ngang qua popup xem trước, ở 2 chế độ: In bảng theo dõi (Phòng ban ▸ Bộ phận ▸ Nhân viên, đủ mọi "
         "phòng) hoặc In danh sách chi tiết đầu việc (mỗi đầu việc một dòng, gộp theo phiếu).",
    tacnhan=TACNHAN,
    dieukien="Đang ở màn báo cáo (nút ở thanh tiêu đề khối lọc) hoặc popup danh sách chi tiết (nút ở chân popup).",
    chinh="1. Người dùng bấm In danh sách ở thanh tiêu đề.\n"
          "2. Hệ thống mở cửa sổ chọn chế độ, mặc định In bảng theo dõi.\n"
          "3. Người dùng chọn chế độ và bấm In.\n"
          "4. Hệ thống dựng bản in theo bộ lọc của báo cáo ĐANG HIỂN THỊ, lấy toàn bộ dữ liệu (không theo trang, không "
          "theo cấp đang bung).\n"
          "5. Popup xem trước hiện bản in; bấm In để mở hộp thoại in của trình duyệt.",
    phu="• Bấm In danh sách ở chân popup chi tiết → in danh sách chi tiết đúng tập dòng đang hiện trong popup (con số "
        "đã bấm + ô lọc + ô tìm + cột đang sắp).\n"
        "• Danh sách chi tiết vượt 2,000 dòng → không in, báo “Danh sách có N dòng, vượt mức in tối đa 2,000 dòng nên "
        "chưa in được. Vui lòng thu hẹp bộ lọc (khoảng thời gian, trạng thái…) rồi in lại, hoặc dùng Xuất Excel cho danh "
        "sách dài.”\n"
        "• Bấm Hủy hoặc × ở cửa sổ chọn chế độ → đóng, không in.",
    dacbiet="Bản in có letterhead công ty (theo công ty đang lọc), tiêu đề, dòng mô tả bộ lọc, dòng “a đầu việc (b lượt "
            "tham gia) — đếm theo PHIẾU…” và Ngày in. Số dùng dấu phẩy ngăn cách hàng nghìn.")
d.p("2.7.3 Layout màn hình")
d.layout(menu=MENU + " => In danh sách", modal="In danh sách", shot=shot("11-in-chon-che-do.png"),
         shot_caption="Cửa sổ chọn chế độ In danh sách")
d.figure(shot("12-ban-in-bang.png"), "Bản xem trước In bảng theo dõi (kỳ Năm nay)", width_in=6.2)
d.figure(shot("13b-ban-in-chi-tiet.png"), "Bản xem trước In danh sách chi tiết đầu việc (kỳ Tháng này)", width_in=6.2)
d.figure(shot("13-ban-in-chi-tiet.png"), "In danh sách chi tiết khi vượt 2,000 dòng: chỉ hiện thông báo", width_in=6.2)
d.p("2.7.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Nút In danh sách (thanh tiêu đề)", "Button", "Enable", "–", "–", "Hiển thị", ["- Mở cửa sổ chọn chế độ"]),
    ("Dòng ghi chú cửa sổ", "Label", "Hiển thị", "–", "–", "Hiển thị",
     ["- “Bản in A4 ngang, bám đúng bộ lọc báo cáo đang hiển thị.”"]),
    ("Chế độ in", "Radio", "Enable", "Danh sách 2 giá trị", "Có", "In bảng theo dõi", [
        "- Mặc định: In bảng theo dõi",
        "- In bảng theo dõi: “Bảng Phòng ban ▸ Bộ phận ▸ Nhân viên, đủ mọi phòng kèm dòng TỔNG — không theo trang hay cấp "
        "đang thu gọn trên màn.”",
        "- In danh sách chi tiết đầu việc: “Từng đầu việc một dòng (đã gộp theo phiếu): loại · người tham gia · thời gian "
        "· trạng thái, đúng bộ lọc báo cáo hiện tại.”",
    ]),
    ("Nút In · Hủy", "Button", "Enable", "–", "–", "Hiển thị", ["- In: dựng bản xem trước", "- Hủy: đóng cửa sổ"]),
    ("Bản in bảng theo dõi", "Table/Grid", "Read-only", "–", "–", "Theo dữ liệu", [
        "- Tiêu đề “BÁO CÁO KẾ HOẠCH & KẾT QUẢ LÀM VIỆC THEO NHÂN VIÊN”",
        "- Cột: STT · Nội dung theo dõi · các loại đang bật · Tổng · Đã HT · Tỷ lệ HT",
        "- Dòng TỔNG “TỔNG HỢP TOÀN CÔNG TY”, phòng (1), bộ phận / nhân viên (1.1), nhân viên dưới bộ phận (1.1.1)",
    ]),
    ("Bản in danh sách chi tiết", "Table/Grid", "Read-only", "–", "–", "Theo dữ liệu", [
        "- Tiêu đề “DANH SÁCH CHI TIẾT ĐẦU VIỆC”",
        "- Cột như popup (cột bị cố định thì bỏ; chỉ P. công tác / P. giao việc thì bỏ Tên công việc)",
    ]),
    ("Thông báo vượt trần in", "Toast / Alert", "Hiển thị", "> 2,000 dòng", "–", "Ẩn",
     ["- Nhắc thu hẹp bộ lọc hoặc dùng Xuất Excel"]),
])
d.p("2.7.5 Danh sách event và xử lý event")
d.event_table([
    ("Bấm In danh sách (thanh tiêu đề)", "Click",
     "Before:\n– Báo cáo chưa tải xong → báo “Báo cáo chưa tải xong, vui lòng thử lại.”\n"
     "After:\n– Mở cửa sổ chọn chế độ."),
    ("Bấm In trong cửa sổ chọn chế độ", "Click",
     "During:\n– Dựng toàn bộ dữ liệu theo bộ lọc của báo cáo đang hiển thị; danh sách chi tiết vượt 2,000 dòng → chỉ "
     "trả thông báo.\n"
     "After:\n– Mở popup xem trước."),
    ("Bấm In danh sách ở chân popup chi tiết", "Click",
     "After:\n– Mở xem trước danh sách chi tiết đúng tập dòng đang hiện trong popup."),
])

# ----------------------------------------------------------------- 2.8
d.h3("2.8 Xuất Excel")
d.p("2.8.1 Biểu đồ Usecase")
d.uc_figure("FR-08", "Xuất Excel", "io", actor=ACT, caption="Biểu đồ Use Case — FR-08 Xuất Excel")
d.p("2.8.2 Giới thiệu")
d.rule_ref("- Quy tắc Excel. Chỉ bổ sung bộ cột của file Excel Báo cáo kế hoạch & kết quả làm việc theo nhân viên.",
           anchor="excel")
d.intro_table(
    ten="Xuất Excel",
    mota="Tải file Excel của bảng theo dõi (nút ở thanh tiêu đề) hoặc của danh sách đầu việc chi tiết (nút ở chân popup), "
         "lấy toàn bộ dữ liệu theo bộ lọc. File tải trực tiếp từ hệ thống (dùng được trên Safari / ứng dụng).",
    tacnhan=TACNHAN,
    dieukien="Đang ở màn báo cáo hoặc popup danh sách chi tiết.",
    chinh="1. Người dùng bấm Xuất Excel ở thanh tiêu đề.\n"
          "2. Hệ thống dựng file bảng theo dõi theo bộ lọc đang hiển thị, đủ mọi cấp.\n"
          "3. Trình duyệt tải file “bao-cao-ke-hoach-lam-viec-nhan-vien.xlsx”.",
    phu="• Bấm Xuất Excel danh sách ở chân popup → tải “danh-sach-dau-viec.xlsx”, đúng tập dòng và thứ tự đang hiện "
        "trong popup (con số đã bấm + ô lọc + ô tìm + cột đang sắp).\n"
        "• Lỗi khi tạo đường tải → báo “Lỗi khi xuất Excel”.",
    dacbiet="File Excel không giới hạn số dòng. Ô số là số thật (cộng / lọc được trong Excel), hiển thị dấu phẩy ngăn "
            "cách hàng nghìn.")
d.p("2.8.3 Layout màn hình")
d.layout(menu=MENU + " => Xuất Excel", shot=shot("14-xuat-excel.png"),
         shot_caption="Nút Xuất Excel trên thanh tiêu đề khối lọc")
d.p("2.8.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Nút Xuất Excel (thanh tiêu đề)", "Button", "Enable", "–", "–", "Hiển thị", ["- Tải file bảng theo dõi"]),
    ("Nút Xuất Excel danh sách (chân popup)", "Button", "Enable", "–", "–", "Hiển thị",
     ["- Tải file danh sách đầu việc chi tiết"]),
    ("File bảng theo dõi", "Table/Grid", "Read-only", "–", "–", "Theo dữ liệu", [
        "- Cột: STT · Nội dung theo dõi · các loại đang bật · Tổng · Đã HT · Tỷ lệ HT",
        "- Dòng TỔNG, phòng, bộ phận, nhân viên; tên thụt lề theo cấp",
    ]),
    ("File danh sách chi tiết", "Table/Grid", "Read-only", "–", "–", "Theo dữ liệu", [
        "- Cột: STT + đúng bộ cột đang hiện của popup (Loại · Phòng ban · Bộ phận · Nhân viên · Mã/Số phiếu · Tên công "
        "việc · Bắt đầu · Kết thúc/Hạn · Trạng thái, bỏ cột bị cố định)",
        "- Chỉ P. công tác / P. giao việc → bỏ cột Tên công việc; lẫn loại → dòng 2 loại này ghi “—”",
    ]),
])
d.p("2.8.5 Danh sách event và xử lý event")
d.event_table([
    ("Bấm Xuất Excel", "Click",
     "Before:\n– Báo cáo chưa tải xong → báo “Báo cáo chưa tải xong, vui lòng thử lại.”\n"
     "After:\n– Tải file theo bộ lọc của báo cáo đang hiển thị."),
    ("Bấm Xuất Excel danh sách (popup)", "Click",
     "After:\n– Tải file theo đúng tập dòng đang hiện trong popup."),
])

# ================================================================= PHẦN 4
d.h1("Phần 4. Quy tắc nghiệp vụ")
d.rule_ref(". Phần này chỉ ghi các quy tắc đặc thù của Báo cáo kế hoạch & kết quả làm việc theo nhân viên; không lặp "
           "lại các quy tắc đã có trong SRS quy tắc chung.",
           anchor="list", head="Quy tắc áp dụng",
           lead="Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ")
d.rule_table([
    ("BR-01", "Đầu việc thuộc kỳ", [
        "– Đầu việc vào báo cáo khi khoảng thời gian của nó GIAO NHAU với kỳ (mốc theo loại — mục 2.1.6).",
        "– Phiếu giao việc thiếu ngày giao / hạn → lấy ngày tạo phiếu.",
        "– Kỳ Tuỳ chọn: ngày đầu > ngày cuối thì tự đảo.",
    ], ["Xem báo cáo", "Danh sách chi tiết", "In", "Xuất Excel"]),
    ("BR-02", "Người thực hiện được tính", [
        "– Ai có tên trong danh sách thực hiện của phiếu đều được tính như nhau; chỉ Meeting mới có người chủ trì.",
        "– Meeting: chủ trì + thành phần phía công ty; Task / Issue: người được giao; Phiếu công tác: cả đoàn; Phiếu giao "
        "việc: mọi người thực hiện.",
    ], ["Xem báo cáo", "Danh sách chi tiết"]),
    ("BR-03", "Cách đếm", [
        "– Dòng nhân viên: mỗi đầu việc +1 cho người đó.",
        "– Dòng phòng ban / bộ phận / TỔNG và khối tổng hợp: đếm theo phiếu (1 phiếu nhiều người = 1).",
        "– Phiếu có người ở 2 phòng được tính ở cả 2 phòng.",
    ], ["Xem báo cáo", "In", "Xuất Excel"]),
    ("BR-04", "Nhóm trạng thái", [
        "– 4 nhóm chia hết tổng: Đã hoàn thành · Đang thực hiện · Quá hạn · Dừng / Huỷ / Từ chối.",
        "– Quá hạn: chưa xong, chưa dừng / huỷ, hạn kết thúc đã qua đầu ngày hôm nay. Dừng / Huỷ / Từ chối không tính quá "
        "hạn (gồm Task Tạm dừng).",
    ], ["Xem báo cáo", "Tìm kiếm và lọc", "Danh sách chi tiết"]),
    ("BR-05", "Phạm vi dữ liệu theo quyền", [
        "– V1: mọi nhân viên của công ty đang làm việc. V2: nhân viên thuộc phòng được quản lý. V3: nhân viên thuộc bộ "
        "phận được quản lý.",
        "– Không có quyền nào: không vào được màn. Không có cấp tổng công ty: chỉ công ty đang làm việc.",
        "– Có nhiều quyền thì cấp cao nhất thắng; không có ngoại lệ cho Super admin.",
        "– Popup, panel, bản in, Excel cùng phạm vi với màn hình.",
    ], ["Toàn màn"]),
    ("BR-06", "Phòng ban / bộ phận theo hồ sơ nhân viên", [
        "– Gom cây theo phòng ban / bộ phận hiện tại trong hồ sơ của người thực hiện, không theo phòng ghi trên phiếu.",
        "– Chưa gán phòng → nhóm “Chưa phân phòng ban”; phòng không chia bộ phận → nhân viên nằm thẳng dưới phòng.",
    ], ["Xem báo cáo", "Tìm kiếm và lọc"]),
    ("BR-07", "Phân trang theo phòng ban", [
        "– Phân trang theo nhóm phòng ban (cỡ 10 / 20 / 50 / 100, mặc định 20); 1 phòng không bị cắt giữa 2 trang.",
        "– Khối tổng hợp và dòng TỔNG tính trên toàn bộ dữ liệu, không theo trang.",
    ], ["Xem báo cáo"]),
    ("BR-08", "Khớp số và ẩn chỉ tiêu bằng 0", [
        "– Tóm tắt, khối tổng hợp, dòng TỔNG, popup, bản in, Excel tính từ cùng một tập dữ liệu.",
        "– Khối Trạng thái xử lý không hiện nhóm bằng 0; ô Tổng đầu việc luôn hiện.",
    ], ["Xem báo cáo"]),
    ("BR-09", "Chỉ hiện nhân viên có việc", [
        "– Mặc định tích: ẩn dòng nhân viên có Tổng = 0; không đổi số ở khối tổng hợp và dòng TỔNG.",
    ], ["Xem báo cáo"]),
    ("BR-10", "Phiếu công tác / Phiếu giao việc không hiện Tên công việc", [
        "– Danh sách chỉ gồm 2 loại này → bỏ cột Tên công việc; lẫn loại khác → dòng 2 loại này ghi “—”.",
        "– Thông tin phiếu xem ở panel chi tiết, tải khi mở; chỉ phiếu có người trong phạm vi quyền mới xem được.",
    ], ["Danh sách chi tiết", "Xem chi tiết đầu việc", "In", "Xuất Excel"]),
    ("BR-11", "In và Excel lấy toàn bộ dữ liệu", [
        "– Lấy theo bộ lọc của báo cáo ĐANG HIỂN THỊ, đủ mọi phòng, đủ mọi cấp; từ popup thì đúng tập dòng + thứ tự đang "
        "hiện trong popup.",
        "– Bản in A4 ngang, danh sách chi tiết tối đa 2,000 dòng; Excel không giới hạn.",
    ], ["In danh sách", "Xuất Excel"]),
])


def split_hyperlink_rels(doc):
    """Mỗi đoạn "Quy tắc chung" một liên kết RIÊNG (python-docx gộp hyperlink cùng URL vào 1 quan hệ, khiến
    srs_selfcheck đếm thiếu). Khuôn `.plans/gop-db/bao-cao-tong-hop-cskh-tiem-nang/gen_srs.py`."""
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
d.save(update_fields=False)
